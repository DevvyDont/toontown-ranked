from toontown.toonbase import TTLocalizer, ToontownGlobals

UNLOCKED = 0
TALK_TO_TOM = 1
DEFEAT_FLUNKY_HQ = 2
TALK_TO_HQ = 3
WRONG_DOOR_HQ = 4
GO_TO_PLAYGROUND = 5
DEFEAT_FLUNKY_TOM = 6
TALK_TO_HQ_TOM = 7
SUIT_APPROACHING = 8
BUILDING_TAKEOVER = 9
SB_DISGUISE_INCOMPLETE = 10
CB_DISGUISE_INCOMPLETE = 11
LB_DISGUISE_INCOMPLETE = 12
BB_DISGUISE_INCOMPLETE = 13


PLAYGROUND_ZONES = (
    ToontownGlobals.ToontownCentral,
    ToontownGlobals.DonaldsDock,
    ToontownGlobals.DaisyGardens,
    ToontownGlobals.MinniesMelodyland,
    ToontownGlobals.TheBrrrgh,
    ToontownGlobals.DonaldsDreamland
)

reasonDict = {
    UNLOCKED: TTLocalizer.FADoorCodes_UNLOCKED,
    TALK_TO_TOM: TTLocalizer.FADoorCodes_TALK_TO_TOM,
    DEFEAT_FLUNKY_HQ: TTLocalizer.FADoorCodes_DEFEAT_FLUNKY_HQ,
    TALK_TO_HQ: TTLocalizer.FADoorCodes_TALK_TO_HQ,
    WRONG_DOOR_HQ: TTLocalizer.FADoorCodes_WRONG_DOOR_HQ,
    GO_TO_PLAYGROUND: TTLocalizer.FADoorCodes_GO_TO_PLAYGROUND,
    DEFEAT_FLUNKY_TOM: TTLocalizer.FADoorCodes_DEFEAT_FLUNKY_TOM,
    TALK_TO_HQ_TOM: TTLocalizer.FADoorCodes_TALK_TO_HQ_TOM,
    SUIT_APPROACHING: TTLocalizer.FADoorCodes_SUIT_APPROACHING,
    BUILDING_TAKEOVER: TTLocalizer.FADoorCodes_BUILDING_TAKEOVER,
    SB_DISGUISE_INCOMPLETE: TTLocalizer.FADoorCodes_SB_DISGUISE_INCOMPLETE,
    CB_DISGUISE_INCOMPLETE: TTLocalizer.FADoorCodes_CB_DISGUISE_INCOMPLETE,
    LB_DISGUISE_INCOMPLETE: TTLocalizer.FADoorCodes_LB_DISGUISE_INCOMPLETE,
    BB_DISGUISE_INCOMPLETE: TTLocalizer.FADoorCodes_BB_DISGUISE_INCOMPLETE,
}
