from typing import List

from direct.directnotify import DirectNotifyGlobal
from . import HoodDataAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import BRTreasurePlannerAI

class BRHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('BRHoodDataAI')

    def __init__(self, air, zoneId=None):
        hoodId = ToontownGlobals.TheBrrrgh
        if zoneId == None:
            zoneId = hoodId
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)
        return

    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)
        trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        trolley.generateWithRequired(self.zoneId)
        trolley.start()
        self.addDistObj(trolley)
        self.treasurePlanner = [
                                BRTreasurePlannerAI.BRTreasurePlannerAI(self.zoneId)
        ]
        for planner in self.treasurePlanner:
            planner.start()

    def getStreetClerkZoneIds(self) -> List[int]:
        return [3115, 3235, 3309]  # Walrus, Sleet, Polar

    def getFishingZoneIds(self) -> List[int]:
        return [3136, 3236, 3329]  # Walrus, Sleet, Polar