import functools
import random

from direct.distributed import DistributedSmoothNode
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.showbase.MessengerGlobal import messenger
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import CollisionPlane, Plane, Vec3, Point3, CollisionNode, NodePath, CollisionPolygon, BitMask32, \
    VBase3
from panda3d.physics import LinearVectorForce, ForceNode, LinearEulerIntegrator, PhysicsManager

from libotp.nametag import NametagGlobals
from otp.otpbase import OTPGlobals
from toontown.coghq import CraneLeagueGlobals
from toontown.coghq.ActivityLog import ActivityLog
from toontown.coghq.BossSpeedrunTimer import BossSpeedrunTimedTimer, BossSpeedrunTimer
from toontown.coghq.CashbotBossScoreboard import CashbotBossScoreboard
from toontown.coghq.CraneLeagueHeatDisplay import CraneLeagueHeatDisplay
from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.minigame.craning.CraneWalk import CraneWalk
from toontown.toonbase import TTLocalizer, ToontownGlobals


class DistributedCraneGame(DistributedMinigame):

    # define constants that you won't want to tweak here
    BASE_HEAT = 500

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)

        self.cranes = {}
        self.safes = {}
        self.goons = []

        self.boss = None
        self.bossRequest = None

        # hack for quick access while debugging
        base.boss = self

        self.wantCustomCraneSpawns = False
        self.customSpawnPositions = {}
        self.ruleset = CraneLeagueGlobals.CFORuleset()  # Setup a default ruleset as a fallback
        self.modifiers = []
        self.heatDisplay = CraneLeagueHeatDisplay()
        self.heatDisplay.hide()
        self.spectators = []
        self.localToonSpectating = False
        self.endVault = None

        self.warningSfx = None

        self.latency = 0.5  # default latency for updating object posHpr

        self.activityLog = ActivityLog()

        self.toonSpawnpointOrder = [i for i in range(8)]
        self.stunEndTime = 0
        self.myHits = []
        self.tempHp = self.ruleset.CFO_MAX_HP
        self.processingHp = False

        self.bossSpeedrunTimer = BossSpeedrunTimer()
        self.bossSpeedrunTimer.hide()

        # The crane round scoreboard
        self.scoreboard = CashbotBossScoreboard(ruleset=self.ruleset)
        self.scoreboard.hide()

        self.walkStateData = CraneWalk('walkDone')

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedMinigameTemplate',
                               [
                                State.State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['play']),
                                State.State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['victory', 'cleanup']),
                                State.State('victory',
                                            self.enterVictory,
                                            self.exitVictory,
                                            ['cleanup']),
                                State.State('cleanup',
                                            self.enterCleanup,
                                            self.exitCleanup,
                                            []),
                                ],
                               # Initial State
                               'off',
                               # Final State
                               'cleanup',
                               )

        # it's important for the final state to do cleanup;
        # on disconnect, the ClassicFSM will be forced into the
        # final state. All states (except 'off') should
        # be prepared to transition to 'cleanup' at any time.

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

    def getTitle(self):
        return TTLocalizer.CraneGameTitle

    def getInstructions(self):
        return TTLocalizer.CraneGameInstructions

    def getMaxDuration(self):
        # how many seconds can this minigame possibly last (within reason)?
        # this is for debugging only
        return 0

    def load(self):
        self.notify.debug("load")
        DistributedMinigame.load(self)
        # load resources and create objects here

        self.music = base.loader.loadMusic('phase_7/audio/bgm/encntr_suit_winning_indoor.ogg')
        self.winSting = base.loader.loadSfx("phase_4/audio/sfx/MG_win.ogg")
        self.loseSting = base.loader.loadSfx("phase_4/audio/sfx/MG_lose.ogg")

        base.cr.forbidCheesyEffects(1)

        self.loadEnvironment()

        # Set up a physics manager for the cables and the objects
        # falling around in the room.
        self.physicsMgr = PhysicsManager()
        integrator = LinearEulerIntegrator()
        self.physicsMgr.attachLinearIntegrator(integrator)
        fn = ForceNode('gravity')
        self.fnp = self.geom.attachNewNode(fn)
        gravity = LinearVectorForce(0, 0, -32)
        fn.addForce(gravity)
        self.physicsMgr.addLinearForce(gravity)

        self.warningSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_GOON_tractor_beam_alarmed.ogg')

    def loadEnvironment(self):
        self.endVault = loader.loadModel('phase_10/models/cogHQ/EndVault.bam')
        self.lightning = loader.loadModel('phase_10/models/cogHQ/CBLightning.bam')
        self.magnet = loader.loadModel('phase_10/models/cogHQ/CBMagnetBlue.bam')
        self.sideMagnet = loader.loadModel('phase_10/models/cogHQ/CBMagnetRed.bam')
        if base.config.GetBool('want-legacy-heads'):
            self.magnet = loader.loadModel('phase_10/models/cogHQ/CBMagnet.bam')
            self.sideMagnet = loader.loadModel('phase_10/models/cogHQ/CBMagnetRed.bam')
        self.craneArm = loader.loadModel('phase_10/models/cogHQ/CBCraneArm.bam')
        self.controls = loader.loadModel('phase_10/models/cogHQ/CBCraneControls.bam')
        self.stick = loader.loadModel('phase_10/models/cogHQ/CBCraneStick.bam')
        self.safe = loader.loadModel('phase_10/models/cogHQ/CBSafe.bam')
        self.cableTex = self.craneArm.findTexture('MagnetControl')

        # Position the two rooms relative to each other, and so that
        # the floor is at z == 0
        self.geom = NodePath('geom')
        self.endVault.setPos(84, -201, -6)
        self.endVault.reparentTo(self.geom)

        # Clear out unneeded backstage models from the EndVault, if
        # they're in the file.
        self.endVault.findAllMatches('**/MagnetArms').detach()
        self.endVault.findAllMatches('**/Safes').detach()
        self.endVault.findAllMatches('**/MagnetControlsAll').detach()

        # Flag the collisions in the end vault so safes and magnets
        # don't try to go through the wall.
        self.disableBackWall()

        # Get the rolling doors.

        # This is the door from the end vault back to the mid vault.
        # The boss makes his "escape" through this door.
        self.door3 = self.endVault.find('**/SlidingDoor/')

        # Find all the wall polygons and replace them with planes,
        # which are solid, so there will be zero chance of safes or
        # toons slipping through a wall.
        walls = self.endVault.find('**/RollUpFrameCillison')
        walls.detachNode()
        self.evWalls = self.replaceCollisionPolysWithPlanes(walls)
        self.evWalls.reparentTo(self.endVault)

        # Initially, these new planar walls are stashed, so they don't
        # cause us trouble in the intro movie or in battle one.  We
        # will unstash them when we move to battle three.
        self.evWalls.stash()

        # Also replace the floor polygon with a plane, and rename it
        # so we can detect a collision with it.
        floor = self.endVault.find('**/EndVaultFloorCollision')
        floor.detachNode()
        self.evFloor = self.replaceCollisionPolysWithPlanes(floor)
        self.evFloor.reparentTo(self.endVault)
        self.evFloor.setName('floor')

        # Also, put a big plane across the universe a few feet below
        # the floor, to catch things that fall out of the world.
        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, -50)))
        planeNode = CollisionNode('dropPlane')
        planeNode.addSolid(plane)
        planeNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.geom.attachNewNode(planeNode)
        self.geom.reparentTo(render)

    def replaceCollisionPolysWithPlanes(self, model):
        newCollisionNode = CollisionNode('collisions')
        newCollideMask = BitMask32(0)
        planes = []
        collList = model.findAllMatches('**/+CollisionNode')
        if not collList:
            collList = [model]
        for cnp in collList:
            cn = cnp.node()
            if not isinstance(cn, CollisionNode):
                self.notify.warning('Not a collision node: %s' % repr(cnp))
                break
            newCollideMask = newCollideMask | cn.getIntoCollideMask()
            for i in range(cn.getNumSolids()):
                solid = cn.getSolid(i)
                if isinstance(solid, CollisionPolygon):
                    # Save the plane defined by this polygon
                    plane = Plane(solid.getPlane())
                    planes.append(plane)
                else:
                    self.notify.warning('Unexpected collision solid: %s' % repr(solid))
                    newCollisionNode.addSolid(plane)

        newCollisionNode.setIntoCollideMask(newCollideMask)

        # Now sort all of the planes and remove the nonunique ones.
        # We can't use traditional dictionary-based tricks, because we
        # want to use Plane.compareTo(), not Plane.__hash__(), to make
        # the comparison.
        threshold = 0.1
        planes.sort(key=functools.cmp_to_key(lambda p1, p2: p1.compareTo(p2, threshold)))
        lastPlane = None
        for plane in planes:
            if lastPlane is None or plane.compareTo(lastPlane, threshold) != 0:
                cp = CollisionPlane(plane)
                newCollisionNode.addSolid(cp)
                lastPlane = plane

        return NodePath(newCollisionNode)

    def disableBackWall(self):
        if self.endVault is None:
            return

        try:
            cn = self.endVault.find('**/wallsCollision').node()
            cn.setIntoCollideMask(OTPGlobals.WallBitmask | ToontownGlobals.PieBitmask)  # TTCC No Back Wall
        except:
            print('[Crane League] Failed to disable back wall.')

    def enableBackWall(self):
        if self.endVault is None:
            return

        try:
            cn = self.endVault.find('**/wallsCollision').node()
            cn.setIntoCollideMask(OTPGlobals.WallBitmask | ToontownGlobals.PieBitmask | BitMask32.lowerOn(3) << 21) #TTR Back Wall
        except:
            print('[Crane League] Failed to enable back wall.')

    def setToonsToBattleThreePos(self):
        """
        Places each toon at the desired position and orientation without creating
        or returning any animation tracks. The position and orientation are
        applied immediately.
        """
        if self.wantCustomCraneSpawns:
            for toonId in self.avIdList:
                toon = base.cr.doId2do.get(toonId)
                if toon:
                    if toonId in self.customSpawnPositions:
                        # Use the stored custom position for this toon
                        toonWantedPosition = self.customSpawnPositions[toonId]
                    else:
                        # Or pick a random spot if it doesn't exist
                        toonWantedPosition = random.randrange(0, 7)

                    # Retrieve the position/HPR from the global constants
                    posHpr = CraneLeagueGlobals.TOON_SPAWN_POSITIONS[toonWantedPosition]
                    pos = Point3(*posHpr[0:3])
                    hpr = VBase3(*posHpr[3:6])

                    # Instantly set the toon’s position/orientation
                    toon.setPosHpr(pos, hpr)
        else:
            # Otherwise, use the pre-defined spawn-point order
            for i, toonId in enumerate(self.avIdList):
                toon = base.cr.doId2do.get(toonId)
                if toon:
                    spawn_index = self.toonSpawnpointOrder[i]
                    posHpr = CraneLeagueGlobals.TOON_SPAWN_POSITIONS[spawn_index]
                    pos = Point3(*posHpr[0:3])
                    hpr = VBase3(*posHpr[3:6])
                    toon.setPosHpr(pos, hpr)

    def unload(self):
        self.notify.debug("unload")
        DistributedMinigame.unload(self)

        self.geom.removeNode()
        del self.geom

        self.bossSpeedrunTimer.cleanup()
        del self.bossSpeedrunTimer

        self.fnp.removeNode()
        self.physicsMgr.clearLinearForces()
        self.music.stop()
        self.scoreboard.cleanup()
        self.heatDisplay.cleanup()

        base.cr.forbidCheesyEffects(0)
        localAvatar.chatMgr.chatInputSpeedChat.removeCFOMenu()
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        self.music.stop()
        taskMgr.remove(self.uniqueName('physics'))

        # unload resources and delete objects from load() here
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

    def onstage(self):
        self.notify.debug("onstage")
        DistributedMinigame.onstage(self)
        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons
        base.localAvatar.reparentTo(render)
        base.localAvatar.loop('neutral')
        base.camLens.setFar(450.0)
        base.transitions.irisIn(0.4)
        NametagGlobals.setMasterArrowsOn(1)
        camera.reparentTo(render)
        camera.setPosHpr(119.541, -275.886, 35, 180, -30, 0)

        self.setToonsToBattleThreePos()

        DistributedSmoothNode.activateSmoothing(1, 1)

    def offstage(self):
        self.notify.debug("offstage")
        # stop the minigame; parent things to hidden, stop the
        # music...
        DistributedSmoothNode.activateSmoothing(1, 0)
        NametagGlobals.setMasterArrowsOn(0)
        base.camLens.setFar(ToontownGlobals.DefaultCameraFar)

        # the base class parents the toons to hidden, so consider
        # calling it last
        DistributedMinigame.offstage(self)

    def handleDisabledAvatar(self, avId):
        """This will be called if an avatar exits unexpectedly"""
        self.notify.debug("handleDisabledAvatar")
        self.notify.debug("avatar " + str(avId) + " disabled")
        # clean up any references to the disabled avatar before he disappears

        # then call the base class
        DistributedMinigame.handleDisabledAvatar(self, avId)

    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if DistributedMinigame.setGameReady(self):
            return
        # all of the remote toons have joined the game;
        # it's safe to show them now.
        self.setToonsToBattleThreePos()

        # Enable the special CFO chat menu.
        localAvatar.chatMgr.chatInputSpeedChat.addCFOMenu()

        for i in range(self.numPlayers):
            avId = self.avIdList[i]
            avatar = self.getAvatar(avId)
            if avatar:
                avatar.startSmooth()

        self.setToonsToBattleThreePos()

        base.localAvatar.d_clearSmoothing()
        base.localAvatar.sendCurrentPosition()
        base.localAvatar.b_setAnimState('neutral', 1)
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def calculateHeat(self):
        bonusHeat = 0
        # Loop through all modifiers present and calculate the bonus heat
        for modifier in self.modifiers:
            bonusHeat += modifier.getHeat()

        return self.BASE_HEAT + bonusHeat

    def updateRequiredElements(self):
        self.bossSpeedrunTimer.cleanup()
        self.bossSpeedrunTimer = BossSpeedrunTimedTimer(
            time_limit=self.ruleset.TIMER_MODE_TIME_LIMIT) if self.ruleset.TIMER_MODE else BossSpeedrunTimer()
        self.bossSpeedrunTimer.hide()
        # If the scoreboard was made then update the ruleset
        if self.scoreboard:
            self.scoreboard.set_ruleset(self.ruleset)

        self.heatDisplay.update(self.calculateHeat(), self.modifiers)

    def setRawRuleset(self, attrs):
        self.ruleset = CraneLeagueGlobals.CFORuleset.fromStruct(attrs)
        self.updateRequiredElements()
        print(('ruleset updated: ' + str(self.ruleset)))

    def getRawRuleset(self):
        return self.ruleset.asStruct()

    def getRuleset(self):
        return self.ruleset

    def __doPhysics(self, task):
        dt = globalClock.getDt()
        self.physicsMgr.doPhysics(dt)
        return task.cont

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigame.setGameStart(self, timestamp)
        # all players have finished reading the rules,
        # and are ready to start playing.
        # transition to the appropriate state
        self.gameFSM.request("play")

    # these are enter and exit functions for the game's
    # fsm (finite state machine)

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        self.walkStateData.enter()

        self.evWalls.unstash()

        localAvatar.orbitalCamera.start()
        localAvatar.setCameraFov(ToontownGlobals.BossBattleCameraFov)

        base.playMusic(self.music, looping=1, volume=0.9)

        # It is important to make sure this task runs immediately
        # before the collisionLoop of ShowBase.  That will fix up the
        # z value of the safes, etc., before their position is
        # distributed.
        taskMgr.add(self.__doPhysics, self.uniqueName('physics'), priority=25)

        # Display Boss Timer
        self.bossSpeedrunTimer.reset()
        self.bossSpeedrunTimer.start_updating()
        self.bossSpeedrunTimer.show()

        # Display Modifiers Heat
        self.heatDisplay.update(self.calculateHeat(), self.modifiers)
        self.heatDisplay.show()

        # Make all laff meters blink when in uber mode
        messenger.send('uberThreshold', [self.ruleset.LOW_LAFF_BONUS_THRESHOLD])

        # Setup the scoreboard
        self.scoreboard.clearToons()
        for avId in self.avIdList:
            if avId in base.cr.doId2do:
                self.scoreboard.addToon(avId)

        self.accept("LocalSetFinalBattleMode", self.toFinalBattleMode)
        self.accept("LocalSetOuchMode", self.toOuchMode)
        self.accept("ChatMgr-enterMainMenu", self.chatClosed)

    def exitPlay(self):
        if self.boss is not None:
            self.boss.cleanupBossBattle()

        self.walkStateData.exit()

    def enterVictory(self):
        if self.victor == 0:
            return

        victor = base.cr.getDo(self.victor)
        if self.victor == self.localAvId:
            base.playSfx(self.winSting)
        else:
            base.playSfx(self.loseSting)
        camera.reparentTo(victor)
        camera.setPosHpr(0, 8, victor.getHeight() / 2.0, 180, 0, 0)

        victor.setAnimState("victory")

        taskMgr.doMethodLater(5, self.gameOver, self.uniqueName("craneGameVictory"), extraArgs=[])

    def exitVictory(self):
        taskMgr.remove(self.uniqueName("craneGameVictory"))
        camera.reparentTo(render)

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

    def exitCleanup(self):
        pass

    """
    Updates from server to client
    """

    def setBossCogId(self, bossCogId: int) -> None:
        self.boss = base.cr.getDo(bossCogId)
        self.boss.prepareBossForBattle()

    def killingBlowDealt(self, avId):
        self.scoreboard.addScore(avId, self.ruleset.POINTS_KILLING_BLOW, CraneLeagueGlobals.KILLING_BLOW_TEXT)

    def updateDamageDealt(self, avId, damageDealt):
        self.scoreboard.addScore(avId, damageDealt)
        self.scoreboard.addDamage(avId, damageDealt)

    def updateStunCount(self, avId, craneId):
        crane = base.cr.doId2do.get(craneId)
        if crane:
            self.scoreboard.addScore(avId, crane.getPointsForStun(), CraneLeagueGlobals.STUN_TEXT)
            self.scoreboard.addStun(avId)

    def updateGoonsStomped(self, avId):
        self.scoreboard.addScore(avId, self.ruleset.POINTS_GOON_STOMP, CraneLeagueGlobals.GOON_STOMP_TEXT)
        self.scoreboard.addStomp(avId)

    def updateSafePoints(self, avId, points):
        self.scoreboard.addScore(avId, points,
                                 CraneLeagueGlobals.PENALTY_SAFEHEAD_TEXT if points < 0 else CraneLeagueGlobals.DESAFE_TEXT)

    def updateMaxImpactHits(self, avId):
        self.scoreboard.addScore(avId, self.ruleset.POINTS_IMPACT, CraneLeagueGlobals.IMPACT_TEXT)

    def updateLowImpactHits(self, avId):
        self.scoreboard.addScore(avId, self.ruleset.POINTS_PENALTY_SANDBAG, CraneLeagueGlobals.PENALTY_SANDBAG_TEXT)

    def updateCombo(self, avId, comboLength):
        self.scoreboard.setCombo(avId, comboLength)

    def awardCombo(self, avId, comboLength, amount):
        self.scoreboard.addScore(avId, amount, reason='COMBO x' + str(comboLength) + '!')

    def goonKilledBySafe(self, avId):
        self.scoreboard.addScore(avId, amount=self.ruleset.POINTS_GOON_KILLED_BY_SAFE,
                                 reason=CraneLeagueGlobals.GOON_KILLED_BY_SAFE_TEXT)

    def updateUnstun(self, avId):
        self.scoreboard.addScore(avId, amount=self.ruleset.POINTS_PENALTY_UNSTUN,
                                 reason=CraneLeagueGlobals.PENALTY_UNSTUN_TEXT)

    def updateTimer(self, secs):
        self.bossSpeedrunTimer.override_time(secs)
        self.bossSpeedrunTimer.update_time()

    def declareVictor(self, avId: int) -> None:
        self.victor = avId
        self.gameFSM.request("victory")

    """
    Everything else!!!!
    """

    def deactivateCranes(self):
        # This locally knocks all toons off cranes.
        for crane in self.cranes.values():
            crane.demand('Free')

    def hideBattleThreeObjects(self):
        # This turns off all the goons, safes, and cranes on the local
        # client. It's played only during the victory movie, to get
        # these guys out of the way.
        for goon in self.goons:
            goon.demand('Off')

        for safe in self.safes.values():
            safe.demand('Off')

        for crane in self.cranes.values():
            crane.demand('Off')

    def toonDied(self, avId):
        self.scoreboard.addScore(avId, self.ruleset.POINTS_PENALTY_GO_SAD, CraneLeagueGlobals.PENALTY_GO_SAD_TEXT,
                                 ignoreLaff=True)
        self.scoreboard.toonDied(avId)

    def revivedToon(self, avId):
        self.scoreboard.toonRevived(avId)
        if avId == base.localAvatar.doId:
            self.boss.localToonIsSafe = False
            base.localAvatar.stunToon()

    def debug(self, doId='system', content='null'):
        if self.ruleset.GENERAL_DEBUG:
            self.addToActivityLog(doId, content)

    def goonStatesDebug(self, doId='system', content='null'):
        if self.ruleset.GOON_STATES_DEBUG:
            self.addToActivityLog(doId, content)

    def safeStatesDebug(self, doId='system', content='null'):
        if self.ruleset.SAFE_STATES_DEBUG:
            self.addToActivityLog(doId, content)

    def craneStatesDebug(self, doId='system', content='null'):
        if self.ruleset.CRANE_STATES_DEBUG:
            self.addToActivityLog(doId, content)

    def addToActivityLog(self, doId, content):
        doObj = base.cr.doId2do.get(doId)

        try:
            name = doObj.getName()
        except:
            name = doId

        msg = '[%s]' % name
        msg += ' %s' % content
        self.activityLog.addToLog(msg)

    def getBoss(self):
        return self.boss

    def toCraneMode(self):
        self.walkStateData.fsm.request('crane')

    def toFinalBattleMode(self):
        self.walkStateData.fsm.request('walking')

    def toOuchMode(self):
        self.walkStateData.fsm.request('ouch')

    def chatClosed(self):
        if self.walkStateData.fsm.getCurrentState().getName() == "walking":
            base.localAvatar.enableAvatarControls()