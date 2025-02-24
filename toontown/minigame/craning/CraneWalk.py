from direct.fsm import State
from direct.showbase.MessengerGlobal import messenger

from toontown.safezone.Walk import Walk


class CraneWalk(Walk):
    def __init__(self, doneEvent):
        super().__init__(doneEvent)
        self.fsm.addState(State.State('crane', self.enterCrane, self.exitCrane, ['walking']))
        walkState = self.fsm.getStateNamed('walking')
        walkState.addTransition('crane')

        self.fsm.addState(State.State('ouch', self.enterOuch, self.exitOuch, ['walking']))
        walkState.addTransition('ouch')
        craneState = self.fsm.getStateNamed('crane')
        craneState.addTransition('ouch')

        self.fsm.addState(State.State('squished', self.enterSquished, self.exitSquished, ['walking', 'crane']))
        walkState.addTransition('squished')
        craneState = self.fsm.getStateNamed('crane')
        craneState.addTransition('squished')

        self.fsm.addState(State.State('movie', self.enterMovie, self.exitMovie, ['walking', 'crane']))
        walkState.addTransition('movie')

    def enter(self, slowWalk = 0):
        base.localAvatar.laffMeter.start()
        self.fsm.request('walking')

    def exit(self):
        base.localAvatar.laffMeter.stop()
        self.fsm.request('off')

    def enterWalking(self):
        if base.localAvatar.hp <= 0:
            self.fsm.request('slowWalking')
            return

        base.localAvatar.startPosHprBroadcast()
        base.localAvatar.startBlink()
        shouldPush = 1
        if len(base.localAvatar.cameraPositions) > 0:
            shouldPush = not base.localAvatar.cameraPositions[base.localAvatar.cameraIndex][4]
        base.localAvatar.startUpdateSmartCamera(shouldPush)
        base.localAvatar.showName()
        base.localAvatar.collisionsOn()
        base.localAvatar.startGlitchKiller()
        base.localAvatar.enableAvatarControls()
        base.localAvatar.startTrackAnimToSpeed()
        base.localAvatar.setWalkSpeedNormal()
        base.localAvatar.beginAllowPies()

    def exitWalking(self):
        self.ignore(base.controls.JUMP)
        base.localAvatar.disableAvatarControls()
        base.localAvatar.stopUpdateSmartCamera()
        base.localAvatar.stopPosHprBroadcast()
        base.localAvatar.stopBlink()
        base.localAvatar.detachCamera()
        base.localAvatar.stopGlitchKiller()
        base.localAvatar.collisionsOff()
        base.localAvatar.controlManager.placeOnFloor()
        base.localAvatar.stopTrackAnimToSpeed()
        base.localAvatar.endAllowPies()
        base.localAvatar.finishLerpFov()

    def enterSlowWalking(self):
        self.accept(base.localAvatar.uniqueName('positiveHP'), self.__handlePositiveHP)
        base.localAvatar.startPosHprBroadcast()
        base.localAvatar.startBlink()
        shouldPush = 1
        if len(base.localAvatar.cameraPositions) > 0:
            shouldPush = not base.localAvatar.cameraPositions[base.localAvatar.cameraIndex][4]
        base.localAvatar.startUpdateSmartCamera(shouldPush)
        base.localAvatar.showName()
        base.localAvatar.collisionsOn()
        base.localAvatar.startGlitchKiller()
        base.localAvatar.enableAvatarControls()
        base.localAvatar.startTrackAnimToSpeed()
        base.localAvatar.setWalkSpeedSlow()

    def __handlePositiveHP(self):
        self.fsm.request('walking')

    def exitSlowWalking(self):
        self.ignore(base.localAvatar.uniqueName('positiveHP'))
        self.ignore(base.controls.JUMP)
        base.localAvatar.disableAvatarControls()
        base.localAvatar.stopUpdateSmartCamera()
        base.localAvatar.stopPosHprBroadcast()
        base.localAvatar.stopBlink()
        base.localAvatar.detachCamera()
        base.localAvatar.stopGlitchKiller()
        base.localAvatar.collisionsOff()
        base.localAvatar.controlManager.placeOnFloor()
        base.localAvatar.stopTrackAnimToSpeed()

    def enterCrane(self):
        base.localAvatar.collisionsOn()

    def exitCrane(self):
        base.localAvatar.collisionsOff()
        messenger.send('exitCrane')

    def enterMovie(self):
        pass

    def exitMovie(self):
        pass

    def enterOuch(self):
        pass

    def exitOuch(self):
        pass

    def enterSquished(self):
        base.localAvatar.b_setAnimState('Flattened')

    def exitSquished(self):
        pass
