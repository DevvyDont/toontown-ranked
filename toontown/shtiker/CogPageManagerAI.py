from direct.directnotify import DirectNotifyGlobal

from toontown.shtiker.CogPageGlobals import *
from toontown.suit import SuitDNA


class CogPageManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('CogPageManagerAI')

    def __init__(self, air):
        self.air = air

    def toonEncounteredCogs(self, toon, suitsEncountered, zoneId):
        # zoneId is unused, SAD
        cogStatus = toon.getCogStatus()
        for suit in suitsEncountered:
            if toon.getDoId() in suit['activeToons']:
                suitIndex = SuitDNA.suitHeadTypes.index(suit['type'])
                # Loop past suits we don't keep track of in gallery
                if suit['type'] in SuitDNA.notMainTypes:
                    continue
                if cogStatus[suitIndex] == COG_UNSEEN:
                    cogStatus[suitIndex] = COG_BATTLED

        toon.b_setCogStatus(cogStatus)

    def toonKilledCogs(self, toon, suitsKilled, zoneId):
        # Thank you zoneId, very cool!
        cogStatus = toon.getCogStatus()
        cogCount = toon.getCogCount()
        for suit in suitsKilled:
            if suit['isVP'] or suit['isCFO']:
                continue

            if toon.getDoId() in suit['activeToons']:
                
                # ik this is hacky, but it works for now with custom cogs as we dont have extra room for cog gallery besides the OG 32.
                try:
                    suitIndex = SuitDNA.suitHeadTypes.index(suit['type'])
                    cogQuota = get_min_cog_quota(toon)
                    buildingQuota = get_max_cog_quota(toon)

                    cogCount[suitIndex] += 1
                    cogStatus[suitIndex] = COG_DEFEATED

                    if cogQuota <= cogCount[suitIndex] < buildingQuota:
                        cogStatus[suitIndex] = COG_COMPLETE1
                    else:
                        cogStatus[suitIndex] = COG_COMPLETE2
                except:
                    pass

        toon.b_setCogStatus(cogStatus)

        self.updateRadar(toon)

    def updateRadar(self, toon):
        cogRadar = toon.getCogRadar()
        buildingRadar = toon.getBuildingRadar()

        for suitDept in range(len(SuitDNA.suitDepts)):
            if buildingRadar[suitDept] == 1:
                continue

            hasBuildingRadar = 1
            hasCogRadar = 1

            for suit in range(SuitDNA.suitsPerDept):
                cogStatus = toon.getCogStatus()[suitDept * SuitDNA.suitsPerDept + suit]
                if cogStatus != COG_COMPLETE2:
                    hasBuildingRadar = 0
                    if cogStatus != COG_COMPLETE1:
                        hasCogRadar = 0

            buildingRadar[suitDept] = hasBuildingRadar
            cogRadar[suitDept] = hasCogRadar

        toon.b_setBuildingRadar(buildingRadar)
        toon.b_setCogRadar(cogRadar)
