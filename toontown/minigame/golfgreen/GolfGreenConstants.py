# How long does the game last?
GAME_DURATION = 90

# How long to wait until dragging the board forward?
DRAG_BOARD_FWD_TIME = 3  # 10

# Should a player completing a board reward other players with a bomb?
WANT_GIFTS = True

# Map each ball type to an integer value.
TRANSLATE_DATA = {'r': 0, 'b': 1, 'g': 2, 'w': 3, 'k': 4, 'l': 5, 'y': 6, 'o': 7, 'a': 8, 's': 9, 'R': 10, 'B': 11}

# Board data, indicates what golf balls to spawn at which positions.
BOARD_DATA = [
    ('rbygl', 'r_______b', 'byyywgggr', 'r_______b', 'bggyyyggr', 'r_______b', 'byylllyyr', 'r_______b', 'Blllllllr'),
    ('rgby', 'rrrgggbbb', 'rwrgggbwb', 'rrryyybbb', 'bByyyyyRr'),
    ('bygr', 'b_y_b_y__', 'b_y_b_yw_', '_b_y_b_y_', '_b_y_b_g_', '__b_g_r__', '__b_g_r__', '___b_g_r_', '___b_g_R_'),
    ('rgb', '_b__g____', '_r__g____', '_r__r____', '_w__R____'),
    ('lbryg', '___bbb___', '___bwb___', '__lgggr__', 'rrgggggll', '_ybbbbby_', '__ryyyr__', '_________', '_________'),
    ('lbryg', 'l_rr__b__', 'l__w__b__', 'b__b__b__', 'b__b__r__', 'l__g__r__', 'l__g__b__', 'y__y__B__', '_________'),
    ('byr', 'R_______y', 'ygggwgggR', 'B_______B', 'Rgggggggy', 'y_______R', 'BgggggggB', 'R_______y', 'BgggggggR'),
    ('bygr', '____bb___', '___bwb___', '_y__y____', '_y__y____', '_yggg_bbb', '____y____', '____y____', '__b_y__b_', '__b_y__b_', '__rrRrrr_'),
    ('bryg', 'b_yr_by_r', 'by_rb_yr_', 'r_gbwrg_y', 'rg_br_gy_', 'b_yg_yr_b', 'by_gy_Rb_', '_________', '_________'),
    ('lyg', '__lyyyyl_', '__lywyl__', '___lyyl__', '___lyl___', '____ll___', '__ygyg___', 'lyl___lyl', '_________'),
    ('rgbyl', 'l_______r', 'brbrbw__r', 'r_______r', 'r__ylblbl', 'r_______b', 'lglgly__b', '________b', '___yrgrgr'),
    ('rgbyl', 'b_______r', 'bbbw_wrrr', '___b__r__', '__b__r___', '___b__r__', '__g__y___', '___y__g__', 'rrrr_bbbb', 'lbyy_ggrl'),
    ('yrbg', 'ry_____yb', '_yrwwby__', '___yyy___', '_rl__gb__', 'lr_____bg', 'ylyg_gyly', '_________', '_________'),
    ('bylr', 'rrr_r_r_r', '_w__r_r_r', '____r_r_r', 'ggggR_r_r', '______r_r', 'ggggggR_r', '________r', 'ggggggggR', '_________'),
    ('rgbl', '__y_bb_y_', '_y__w_y__', 'yyy____yy', 'y_gyyyr_y', 'y_______y', 'byyyyyyl_', '_________', '_________', '_________', '_________'),
    ('o', 'b_bb_bb_b', 'wb_bb_bw_', 'b_bbbbb_b', 'bb_bb_bb_', 'b_bb_bb_b', 'bb_bb_bb_', '_________', '_________'),
    ('oa', 's________', 'sw_______', 's________', 's________', 's________', 's________', 'ssssss___', '_________')
]
