from panda3d.core import *
from direct.interval.IntervalGlobal import *
from . import ToonHood
from toontown.town import TTTownLoader
from toontown.safezone import TTSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *
from . import SkyUtil
from direct.directnotify import DirectNotifyGlobal

class TTHood(ToonHood.ToonHood):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTHood')

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = ToontownCentral
        self.townLoaderClass = TTTownLoader.TTTownLoader
        self.safeZoneLoaderClass = TTSafeZoneLoader.TTSafeZoneLoader
        self.storageDNAFile = 'phase_4/dna/storage_TT.dna'
        self.holidayStorageDNADict = {WINTER_DECORATIONS: ['phase_4/dna/winter_storage_TT.dna', 'phase_4/dna/winter_storage_TT_sz.dna'],
         WACKY_WINTER_DECORATIONS: ['phase_4/dna/winter_storage_TT.dna', 'phase_4/dna/winter_storage_TT_sz.dna'],
         HALLOWEEN_PROPS: ['phase_4/dna/halloween_props_storage_TT.dna', 'phase_4/dna/halloween_props_storage_TT_sz.dna'],
         SPOOKY_PROPS: ['phase_4/dna/halloween_props_storage_TT.dna', 'phase_4/dna/halloween_props_storage_TT_sz.dna']}
        self.spookySkyFile = 'phase_3.5/models/props/BR_sky'
        self.titleColor = (1.0, 0.5, 0.4, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('TTHood').addChild(self.fsm)
        base.camLens.setFar(9999)

    def unload(self):
        self.parentFSM.getStateNamed('TTHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)

    def skyTrack(self, task):
        pass

    def startSky(self):
        pass

    def startSpookySky(self):
        pass
