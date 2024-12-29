from direct.directnotify import DirectNotifyGlobal
from . import HoodDataAI
from toontown.toonbase import ToontownGlobals
from ..building.DistributedBoardingPartyAI import DistributedBoardingPartyAI
from ..building.DistributedCFOElevatorAI import DistributedCFOElevatorAI
from ..coghq.LobbyManagerAI import LobbyManagerAI
from ..suit.DistributedCashbotBossAI import DistributedCashbotBossAI


class TTHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTHoodDataAI')

    def __init__(self, air, zoneId=None):
        hoodId = ToontownGlobals.ToontownCentral
        if zoneId is None:
            zoneId = hoodId
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)
        self.lobbyManager: LobbyManagerAI | None = None
        self.elevator: DistributedCFOElevatorAI | None = None
        self.boardingParty: DistributedBoardingPartyAI | None = None
        return

    def _createDistributedObjects(self, _=None):
        self.lobbyManager = LobbyManagerAI(self.air, DistributedCashbotBossAI)
        self.lobbyManager.generateWithRequired(self.zoneId)
        self.addDistObj(self.lobbyManager)
        self.elevator = DistributedCFOElevatorAI(self.air, self.lobbyManager, self.zoneId, antiShuffle=1)
        self.elevator.generateWithRequired(self.zoneId)
        self.addDistObj(self.elevator)
        self.boardingParty = DistributedBoardingPartyAI(self.air, [self.elevator.doId], 8)
        self.boardingParty.generateWithRequired(self.zoneId)
        self.addDistObj(self.boardingParty)

    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)
        self._createDistributedObjects()
        # taskMgr.doMethodLater(1, self._createDistributedObjects, 'TTHoodDataAI-createDistributedObjects')
        messenger.send('TTHoodSpawned', [self])

    def shutdown(self):
        HoodDataAI.HoodDataAI.shutdown(self)
        messenger.send('TTHoodDestroyed', [self])
