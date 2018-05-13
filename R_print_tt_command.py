import CommandGenerator
# initialise
POLLING_DELAY = 0.1
process_log = ""
mosaic_number = 0

param_tiles = {"tile_width": 20,
               "tile_height": 20,
               "inter_tile_hgap": 2,
               "inter_tile_vgap": 2,
               "palette_pitch": 25,
               "tt_origin_x": 0,
               "tt_origin_y": 0,
               "pal_origin_x": 0}

param_robo = {"tt_port": "COM4",
              "pal_port": "COM3",
              "tt_baud": 9600,
              "pal_baud": 38400,
              "tt_timeout": 1,
              "pal_timeout": 1,
              "gripper_open_wait": 2,
              "gripper_close_wait": 2,
              "gripper_up": 0,
              "gripper_down_palette": 10,
              "gripper_down_table": 15,
              "moving_timeout": 15}

pal_message = {"palHome": ":01060D001010CC\r\n",
               "palSet_position_1": ":01060D030001E8\r\n",
               "palSet_position_2": ":01060D030002E7\r\n",
               "palCSTR_off": ":01060D001000DC\r\n",
               "palCSTR_on": ":01060D001008D4\r\n",
               "palQuery_moving": ":01039007000164\r\n",
               "palQuery_home": ":01039005000166\r\n",
               "enableModbus": ":01050427FF00D0\r\n"}

program = ["palCSTR_OFF",
           "palHome",
           "ttHome"
           "moving",
           "convertSourceColour",
           "convertTargetPosition",
           "ttGripperUp",
           "moving",
           "ttMoveAbs:TargetX,TargetY"]


cmd = CommandGenerator.ttMovingQuery(axis="01")

print(cmd)