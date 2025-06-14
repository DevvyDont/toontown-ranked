from otp.ai.AIBase import *
from toontown.toonbase.ToontownGlobals import *
from direct.distributed.ClockDelta import *
from .TrolleyConstants import *
from direct.distributed import DistributedObjectAI
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from toontown.minigame import TrolleyHolidayMgrAI
from toontown.minigame import TrolleyWeekendMgrAI
from toontown.groups.DistributedGroupManagerAI import DistributedGroupManagerAI
from ..groups.DistributedGroupAI import DistributedGroupAI


class DistributedTrolleyAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTrolleyAI')
    NUM_SEATS = 16

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.seats = [None] * DistributedTrolleyAI.NUM_SEATS
        self.accepting = 0
        self.trolleyCountdownTime = simbase.config.GetFloat('trolley-countdown-time', TROLLEY_COUNTDOWN_TIME)
        self.fsm = ClassicFSM.ClassicFSM('DistributedTrolleyAI', [State.State('off', self.enterOff, self.exitOff, ['entering']),
         State.State('entering', self.enterEntering, self.exitEntering, ['waitEmpty']),
         State.State('waitEmpty', self.enterWaitEmpty, self.exitWaitEmpty, ['waitCountdown']),
         State.State('waitCountdown', self.enterWaitCountdown, self.exitWaitCountdown, ['waitEmpty', 'allAboard']),
         State.State('allAboard', self.enterAllAboard, self.exitAllAboard, ['leaving', 'waitEmpty']),
         State.State('leaving', self.enterLeaving, self.exitLeaving, ['entering'])], 'off', 'off')
        self.fsm.enterInitialState()
        return

    def delete(self):
        self.fsm.requestFinalState()
        del self.fsm
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def findAvailableSeat(self):
        for i in range(len(self.seats)):
            if self.seats[i] == None:
                return i
        return

    def findAvatar(self, avId):
        for i in range(len(self.seats)):
            if self.seats[i] == avId:
                return i

        return None

    def countFullSeats(self):
        avCounter = 0
        for i in self.seats:
            if i:
                avCounter += 1

        return avCounter

    def rejectingBoardersHandler(self, avId):
        self.rejectBoarder(avId)

    def rejectBoarder(self, avId):
        self.sendUpdateToAvatarId(avId, 'rejectBoard', [avId])

    def acceptingBoardersHandler(self, avId):
        self.notify.debug('acceptingBoardersHandler')
        seatIndex = self.findAvailableSeat()
        if seatIndex == None:
            self.rejectBoarder(avId)
        else:
            self.acceptBoarder(avId, seatIndex)
        return

    def acceptBoarder(self, avId, seatIndex):
        self.notify.debug('acceptBoarder')
        if self.findAvatar(avId) != None:
            return
        self.seats[seatIndex] = avId
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])
        self.timeOfBoarding = globalClock.getRealTime()
        self.sendUpdate('fillSlot', [seatIndex, avId])
        self.waitCountdown()
        return

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('Avatar: ' + str(avId) + ' has exited unexpectedly')
        seatIndex = self.findAvatar(avId)
        if seatIndex == None:
            pass
        else:
            self.clearFullNow(seatIndex)
            self.clearEmptyNow(seatIndex)
            if self.countFullSeats() == 0:
                self.waitEmpty()
        return

    def rejectingExitersHandler(self, avId):
        self.rejectExiter(avId)

    def rejectExiter(self, avId):
        pass

    def acceptingExitersHandler(self, avId):
        self.acceptExiter(avId)

    def acceptExiter(self, avId):
        seatIndex = self.findAvatar(avId)
        if seatIndex == None:
            pass
        else:
            self.clearFullNow(seatIndex)
            self.sendUpdate('emptySlot', [seatIndex, avId])
            if self.countFullSeats() == 0:
                self.waitEmpty()
            taskMgr.doMethodLater(TOON_EXIT_TIME, self.clearEmptyNow, self.uniqueName('clearEmpty-%s' % seatIndex), extraArgs=(seatIndex,))
        return

    def clearEmptyNow(self, seatIndex):
        self.sendUpdate('emptySlot', [seatIndex, 0])

    def clearFullNow(self, seatIndex):
        avId = self.seats[seatIndex]
        if avId == 0:
            self.notify.warning('Clearing an empty seat index: ' + str(seatIndex) + ' ... Strange...')
        else:
            self.seats[seatIndex] = None
            self.sendUpdate('fillSlot', [seatIndex, 0])
            self.ignore(self.air.getAvatarExitEvent(avId))
        return

    def d_setState(self, state):
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime()])

    def getState(self):
        return self.fsm.getCurrentState().getName()

    def findGroupManagers(self) -> list[DistributedGroupManagerAI]:
        """
        Finds all the group managers that are present on the server.
        """
        return self.air.doFindAllInstances(DistributedGroupManagerAI)

    def requestBoard(self, *args):
        self.notify.debug('requestBoard')
        avId = self.air.getAvatarIdFromSender()
        if self.findAvatar(avId) != None:
            self.notify.warning('Ignoring multiple requests from %s to board.' % avId)
            return
        av = self.air.doId2do.get(avId)

        if av:
            newArgs = (avId,) + args

            # If the toon is in a group, we can't let them board unless they are the host.
            for groupManager in self.findGroupManagers():
                group = groupManager.getGroup(av)
                if group is not None:
                    if group.getLeader() != avId:
                        self.rejectingBoardersHandler(avId)
                        av.d_setSystemMessage(0, "Only the leader can decide when to board!")
                        return
                    elif group.getLeader() == avId:
                        self.acceptingAllGroupBoardersHandler(group)
                        return

            if self.air.matchmaker.isPlayerInQueue(av):
                av.d_setSystemMessage(0, "You can't enter the trolley while in queue!")
                self.rejectingBoardersHandler(*newArgs)
                return

            elif av.hp > 0 and self.accepting:
                self.acceptingBoardersHandler(*newArgs)
            else:
                self.rejectingBoardersHandler(*newArgs)
        else:
            self.notify.warning('avid: %s does not exist, but tried to board a trolley' % avId)
        return

    def acceptingAllGroupBoardersHandler(self, group: DistributedGroupAI):
        """
        If all toons are ready, make them board the trolley. Otherwise, reject the leader.
        """
        notReady = group.getNumPlayersNotReady()
        if notReady >= 1:
            self.rejectingBoardersHandler(group.getLeader())
            group.announce(f"Attempted to board trolley, but there are {notReady} players who are not ready!")
            return

        for toon in group.getMembers():
            self.acceptingBoardersHandler(toon.avId)
        group.announce("All aboard!")

    def requestExit(self, *args):
        self.notify.debug('requestExit')
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            newArgs = (avId,) + args

            # If the toon is in a group, we can't let them board unless they are the host.
            for groupManager in self.findGroupManagers():
                group = groupManager.getGroup(av)
                if group is not None:
                    if group.getLeader() != avId:
                        self.rejectingExitersHandler(avId)
                        av.d_setSystemMessage(0, "Only the leader can decide to hop off!")
                        return
                    elif group.getLeader() == avId:
                        self.acceptingAllGroupExitersHandler(group)
                        return

            if self.accepting:
                self.acceptingExitersHandler(*newArgs)
            else:
                self.rejectingExitersHandler(*newArgs)
        else:
            self.notify.warning('avId: %s does not exist, but tried to exit a trolley' % avId)

    def acceptingAllGroupExitersHandler(self, group: DistributedGroupAI):
        """
        The leader has decided to hop off the trolley. Everyone who is in the group should do the same.
        """
        for toon in group.getMembers():
            self.acceptingExitersHandler(toon.avId)
        group.announce("The leader has made everyone hop off!")

    def start(self):
        self.enter()

    def enterOff(self):
        self.accepting = 0
        if hasattr(self, 'doId'):
            for seatIndex in range(4):
                taskMgr.remove(self.uniqueName('clearEmpty-' + str(seatIndex)))

    def exitOff(self):
        self.accepting = 0

    def enter(self):
        self.fsm.request('entering')

    def enterEntering(self):
        self.d_setState('entering')
        self.accepting = 0
        self.seats = [None] * DistributedTrolleyAI.NUM_SEATS
        taskMgr.doMethodLater(TROLLEY_ENTER_TIME, self.waitEmptyTask, self.uniqueName('entering-timer'))
        return

    def exitEntering(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('entering-timer'))

    def waitEmptyTask(self, task):
        self.waitEmpty()
        return Task.done

    def waitEmpty(self):
        self.fsm.request('waitEmpty')

    def enterWaitEmpty(self):
        self.d_setState('waitEmpty')
        self.accepting = 1

    def exitWaitEmpty(self):
        self.accepting = 0

    def waitCountdown(self):
        self.fsm.request('waitCountdown')

    def enterWaitCountdown(self):
        self.d_setState('waitCountdown')
        self.accepting = 1
        taskMgr.doMethodLater(self.trolleyCountdownTime, self.timeToGoTask, self.uniqueName('countdown-timer'))

    def timeToGoTask(self, task):
        if self.countFullSeats() > 0:
            self.allAboard()
        else:
            self.waitEmpty()
        return Task.done

    def exitWaitCountdown(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('countdown-timer'))

    def allAboard(self):
        self.fsm.request('allAboard')

    def enterAllAboard(self):
        self.accepting = 0
        currentTime = globalClock.getRealTime()
        elapsedTime = currentTime - self.timeOfBoarding
        self.notify.debug('elapsed time: ' + str(elapsedTime))
        waitTime = max(TOON_BOARD_TIME - elapsedTime, 0)
        taskMgr.doMethodLater(waitTime, self.leaveTask, self.uniqueName('waitForAllAboard'))

    def exitAllAboard(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('waitForAllAboard'))

    def leaveTask(self, task):
        if self.countFullSeats() > 0:
            self.leave()
        else:
            self.waitEmpty()
        return Task.done

    def leave(self):
        self.fsm.request('leaving')

    def enterLeaving(self):
        self.d_setState('leaving')
        self.accepting = 0
        taskMgr.doMethodLater(TROLLEY_EXIT_TIME, self.trolleyLeftTask, self.uniqueName('leaving-timer'))

    def trolleyLeftTask(self, task):
        self.trolleyLeft()
        return Task.done

    def trolleyLeft(self):
        numPlayers = self.countFullSeats()
        if numPlayers > 0:

            playerArray = []
            for i in self.seats:
                if i not in [None, 0]:
                    playerArray.append(i)

            startingVotes = None
            metagameRound = -1
            trolleyGoesToMetagame = simbase.config.GetBool('trolley-goes-to-metagame', 0)
            trolleyHoliday = bboard.get(TrolleyHolidayMgrAI.TrolleyHolidayMgrAI.PostName)
            trolleyWeekend = bboard.get(TrolleyWeekendMgrAI.TrolleyWeekendMgrAI.PostName)
            if trolleyGoesToMetagame or trolleyHoliday or trolleyWeekend:
                metagameRound = 0
                if simbase.config.GetBool('metagame-min-2-players', 1) and len(playerArray) == 1:
                    metagameRound = -1

            minigame = self.air.minigameMgr.createMinigame(playerArray, self.zoneId, hostId=playerArray[0])
            for seatIndex in range(len(self.seats)):
                avId = self.seats[seatIndex]
                if avId:
                    self.sendUpdateToAvatarId(avId, 'setMinigameZone', [minigame.zone, minigame.gameId])
                    self.clearFullNow(seatIndex)

        else:
            self.notify.warning('The trolley left, but was empty.')
        self.enter()
        return

    def exitLeaving(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('leaving-timer'))
