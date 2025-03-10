"""DistributedMinigameTemplate module: contains the DistributedMinigameTemplate class"""
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State

from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.toonbase import TTLocalizer


class DistributedMinigameTemplate(DistributedMinigame):

    # define constants that you won't want to tweak here

    def __init__(self, cr):
        super().__init__(cr)

        self.gameFSM = ClassicFSM(self.__class__.__name__,
                               [
                                State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['play']),
                                State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['cleanup']),
                                State('cleanup',
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
        return TTLocalizer.MinigameTemplateTitle

    def getInstructions(self):
        return TTLocalizer.MinigameTemplateInstructions

    def getMaxDuration(self):
        # how many seconds can this minigame possibly last (within reason)?
        # this is for debugging only
        return 0

    def load(self):
        self.notify.debug("load")
        super().load()
        # load resources and create objects here

    def unload(self):
        self.notify.debug("unload")
        super().unload()
        # unload resources and delete objects from load() here
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

    def onstage(self):
        self.notify.debug("onstage")
        super().onstage()
        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons

    def offstage(self):
        self.notify.debug("offstage")
        # stop the minigame; parent things to hidden, stop the
        # music...

        # the base class parents the toons to hidden, so consider
        # calling it last
        super().offstage()

    def handleDisabledAvatar(self, avId):
        """This will be called if an avatar exits unexpectedly"""
        self.notify.debug("handleDisabledAvatar")
        self.notify.debug("avatar " + str(avId) + " disabled")
        # clean up any references to the disabled avatar before he disappears

        # then call the base class
        super().handleDisabledAvatar(avId)

    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if super().setGameReady():
            return
        # all of the remote toons have joined the game;
        # it's safe to show them now.

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        super().setGameStart(timestamp)
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

        # when the game is done, call gameOver()
        self.gameOver()

    def exitPlay(self):
        pass

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

    def exitCleanup(self):
        pass
