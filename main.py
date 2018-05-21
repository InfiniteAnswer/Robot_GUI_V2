# Author
# Version

import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
from PIL import ImageTk, Image
import sys

import Initialise
import Manual
import Settings
import TilePrint
import Controls
import RuntimeState

from random import randint
import serial               # used for serial communications. came from <pip3.6 install pyserial>
import RR_CommandGenerator     # class developed to generate a limited number of TT robot commands
import time
import pickle

# initialise
# POLLING_DELAY = 0.1         # time in SECONDS between repeated requests to see if a robot is moving
# process_log = ""
# mosaic_number = 0
# LOG_file_save_location = "C:/Users/Finlay/Documents/iai_log_files/"


# def readImage():
#     # OPTION 1: generate a new image from random tiles
#     # random_image_rows = 2
#     # random_image_columns = 2
#     # random_palette_tiles = 4
#     # image = list()
#     # for r in range(random_image_rows):
#     #     new_row = list()
#     #     for c in range(random_image_columns):
#     #         new_row.append(randint(0, random_palette_tiles))
#     #     image.append(new_row)
#
#     # OPTION 2: directly create 2 list of lists for the mosaic
# ##    image = [[0, 1, 0, 1, 0],
# ##             [1, 0, 1, 0, 1],
# ##             [0, 1, 0, 1, 0],
# ##             [1, 0, 1, 0, 1],
# ##             [0, 1, 0, 1, 0]]
#
# ##    image =[[0, 1],
# ##            [1, 0]]
#
#     image =[[0,  1, 0],
#             [1, 0, 1],
#             [0, 1, 0]]
#
# ##    image =[[0, 0, 0, 0, 0],
# ##            [0, 0, 0, 0, 0]]
#
#     # image = [[0, 0, 0, 0, 0, 0, 0],
#     #          [0, 0, 0, 0, 0, 0, 0],
#     #          [0, 0, 0, 0, 0, 0, 0],
#     #          [0, 0, 0, 0, 0, 0, 0],
#     #          [0, 0, 0, 0, 0, 0, 0],
#     #          [0, 0, 0, 0, 0, 0, 0],
#     #          [0, 0, 0, 0, 0, 0, 0]]
#
#     # OPTION 3: load a file created by PXLRT
#     # filename = "C:\\Users\\Victor\\Desktop\list_save.pkl"
#     # image = pickle.load(open(filename, "rb"))
#     return image
#
#
# def pal_moving_query(palPort):
#     # ask pal if moving and save response
#     cmd = pal_message["palQuery_moving"].encode("ascii")
#     palPort.write(cmd)
#     response_pal = palPort.readline()
#
#     # perform logical test on response and generate true/false answers
#     response_pal = '0x' + str(response_pal)[11:12]
#     pal = (eval(response_pal) & 0b10) == 2
#     return (pal)
#
#
# def tt_moving(ttPort):
#     global process_log
#     timeout = time.time() + param_robo["moving_timeout"]
#     while (tt_moving_query(ttPort)):
#         if time.time() > timeout:
#             process_log += "WARNING! TT timed out. Unable to reach set-point after " +\
#                            str(param_robo["moving_timeout"]) + " seconds\n"
#             print(process_log.split("\n")[-2])
#             break
#         time.sleep(POLLING_DELAY)
#
#
# def pal_moving(palPort):
#     global process_log
#     timeout = time.time() + param_robo["moving_timeout"]
#     while (pal_moving_query(palPort)):
#         if time.time() > timeout:
#             process_log += "WARNING! PAL timed out. Unable to reach set-point after " +\
#                            str(param_robo["moving_timeout"]) + " seconds\n"
#             print(process_log.split("\n")[-2])
#             break
#         time.sleep(POLLING_DELAY)
#
#
# def tt_pal_moving(ttPort, palPort):
#     global process_log
#     timeout = time.time() + param_robo["moving_timeout"]
#     while (tt_moving_query(ttPort) or pal_moving_query(palPort)):
#         if time.time() > timeout:
#             process_log += "WARNING! TT or PAL timed out. Unable to reach set-point after " +\
#                            str(param_robo["moving_timeout"]) + " seconds\n"
#             print(process_log.split("\n")[-2])
#             break
#         time.sleep(POLLING_DELAY)
#
#
# def pixel2table(x_n, y_n):
#     table_x = param_tiles["tt_origin_x"] + x_n * (param_tiles["tile_width"] + param_tiles["inter_tile_hgap"])
#     table_y = param_tiles["tt_origin_y"] + y_n * (param_tiles["tile_height"] + param_tiles["inter_tile_vgap"])
#     return (table_x, table_y)
#
#
# def colour2palette(c_n):
#     palette_x = param_tiles["pal_origin_x"] + c_n * (param_tiles["palette_pitch"])
#     return palette_x
#
#
# def timestamped_msg(msg):
#     string = str(time.asctime(time.localtime(time.time()))) + ": " + msg
#     return (string)
#
#
# def initialise():
#     global process_log
#     ttPort, palPort, cntrlPort = open_ports()
#
#     # enable Modbus communications
#     cmd = pal_message["enableModbus"].encode("ascii")
#     palPort.write(cmd)
#     response_pal = palPort.readline()
#
#     # NOT YET DONE... connect to two robots and check connections with a test command
#
#     # enable tt robot servos
#     process_log += timestamped_msg("enabling servo for axis 1\n")
#     print(process_log.split("\n")[-2])
#     ttPort.write(RR_CommandGenerator.ttServo(axis="001", on=1))
#     unused_response = ttPort.readline()
#     process_log += timestamped_msg("enabling servo for axis 2\n")
#     print(process_log.split("\n")[-2])
#     ttPort.write(RR_CommandGenerator.ttServo(axis="010", on=1))
#     unused_response = ttPort.readline()
#     process_log += timestamped_msg("enabling servo for axis 3\n")
#     print(process_log.split("\n")[-2])
#     ttPort.write(RR_CommandGenerator.ttServo(axis="100", on=1))
#     unused_response = ttPort.readline()
#     time.sleep(1)   # DELAY of 1 SECOND to ensure the servos are active before proceeding
#
#     # check if axes of tt are homed
#     cmd = RR_CommandGenerator.ttMovingQuery(axis="001")
#     ttPort.write(cmd)
#     response_tt_1 = ttPort.readline()
#     cmd = RR_CommandGenerator.ttMovingQuery(axis="010")
#     ttPort.write(cmd)
#     response_tt_2 = ttPort.readline()
#     cmd = RR_CommandGenerator.ttMovingQuery(axis="100")
#     ttPort.write(cmd)
#     response_tt_3 = ttPort.readline()
#
#
#     # if not, home z axis of tt first for SAFETY reasons
#     response_tt_1 = '0x' + str(response_tt_1)[11]
#     response_tt_2 = '0x' + str(response_tt_2)[11]
#     response_tt_3 = '0x' + str(response_tt_3)[11]
#
#     tt_1_home_complete = ((eval(response_tt_1) & 0b0100) == 4)
#     tt_2_home_complete = ((eval(response_tt_2) & 0b0100) == 4)
#     tt_3_home_complete = ((eval(response_tt_3) & 0b0100) == 4)
#
#     if not(tt_3_home_complete):
#         process_log += timestamped_msg("executing TT home for z-axis...\n")
#         print(process_log.split("\n")[-2])
#         ttPort.write(RR_CommandGenerator.ttHome(axis="100"))
#         unused_response = ttPort.readline()
#         # moving?
#         tt_pal_moving(ttPort, palPort)
#     else:
#         process_log += timestamped_msg("TT z-axis already homed, no need to repeat\n")
#         print(process_log.split("\n")[-2])
#
#     if not(tt_2_home_complete):
#         process_log += timestamped_msg("executing TT home for y-axis...\n")
#         print(process_log.split("\n")[-2])
#         ttPort.write(RR_CommandGenerator.ttHome(axis="010"))
#         unused_response = ttPort.readline()
#         # moving?
#         tt_pal_moving(ttPort, palPort)
#     else:
#         process_log += timestamped_msg("TT y-axis already homed, no need to repeat\n")
#         print(process_log.split("\n")[-2])
#
#     if not(tt_1_home_complete):
#         process_log += timestamped_msg("executing TT home for x-axis...\n")
#         print(process_log.split("\n")[-2])
#         ttPort.write(RR_CommandGenerator.ttHome(axis="001"))
#         unused_response = ttPort.readline()
#         # moving?
#         tt_pal_moving(ttPort, palPort)
#     else:
#         process_log += timestamped_msg("TT x-axis already homed, no need to repeat\n")
#         print(process_log.split("\n")[-2])
#
#     # check to see if PAL is homed
#     cmd = pal_message["palQuery_home"].encode("ascii")
#     palPort.write(cmd)
#     response_pal = palPort.readline()
#     response_pal = '0x' + str(response_pal)[11]
#     pal = (eval(response_pal) & 0b01) == 1
#
#     # if PAL is not homed, perform home operation
#     if not(pal):
#         process_log += timestamped_msg("executing PAL home...\n")
#         print(process_log.split("\n")[-2])
#         cmd = pal_message["palHome"].encode("ascii")
#         palPort.write(cmd)
#         unused_response = palPort.readline()
#         # moving?
#         tt_pal_moving(ttPort, palPort)
#     else:
#         process_log += timestamped_msg("PAL already homed, no need to repeat\n")
#         print(process_log.split("\n")[-2])
#
#     return (ttPort, palPort, cntrlPort)


# def sequence(ttPort, palPort, cntrlPort, image):
#     # gripper up
#     # gripper wide open
#     # pal under gripper
#     # gripper over to pal pickup position
#     # gripper down to pal
#     # gripper close
#     # gripper up
#     # pal back to reload
#     # gripper over to table dropoff position
#     # gripper down
#     # gripper open
#     # gripper shuffle
#     # REPEAT
#
#     global process_log
#     image_rows = len(image)
#     image_cols = len(image[0])
#
#     # add tile number to log file
#     process_log += "Sequence for mosaic: " + str(mosaic_number) + "\n"
#     print(process_log.split("\n")[-2])
#
#     # gripper up
#     ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="100", axis3_pos=param_robo["gripper_up"]))
#     unused_response = ttPort.readline()
#     process_log += timestamped_msg("gripper up\n")
#     print(process_log.split("\n")[-2])
#
#     # moving?
#     tt_pal_moving(ttPort, palPort)
#     process_log += timestamped_msg("both robots finished moving\n")
#     print(process_log.split("\n")[-2])
#
#     # open gripper
# ##    ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="1"))
# ##    unused_response = ttPort.readline()
# ##    ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="1", port="013E"))
# ##    unused_response = ttPort.readline()
#     for i in range(3):
#         cntrlPort.write(b"mgw$");
#         time.sleep(0.5)
#         cntrlPort.write(b"mgo$");
#         time.sleep(0.5)
#         cntrlPort.write(b"mgc$");
#         time.sleep(0.5)
#     time.sleep(1)
#     cntrlPort.write(b"mgw$");
#     # wait
#     time.sleep(param_robo["gripper_open_wait"])
#     process_log += timestamped_msg("gripper opened, paused: ") + str(param_robo["gripper_open_wait"]) + "seconds\n"
#     print(process_log.split("\n")[-2] + "\n")
#     # nons=input("press enter")
#
#     for row_i, row in enumerate(image):
#         x, y = pixel2table(0, row_i)
#
#         # move to next table row position
#         ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="001", axis1_pos=y))
#         unused_response = ttPort.readline()
#         process_log += timestamped_msg("tt moved to row: ") + str(row_i) + "\n"
#         print(process_log.split("\n")[-2])
#         # moving?
#         tt_moving(ttPort)
#         process_log += timestamped_msg("tt robot finished moving\n")
#         print(process_log.split("\n")[-2] + "\n")
#
#         for col_i, col in enumerate(row):
#             # Add tile number to log
#             process_log += "Sequence for tile row: " + str(row_i) + " column: " + str(col_i) + "\n"
#             print("\n\n-------------------------------------------------\n")
#             print(process_log.split("\n")[-2] + "\n")
#
#             x, y = pixel2table(col_i, row_i)
#             c = colour2palette(image[row_i][col_i])
#
#             # move to next colour palette position
#             ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="010", axis2_pos=c))
#             unused_response = ttPort.readline()
#             process_log += timestamped_msg("tt moved to colour: ") + str(image[row_i][col_i]) + \
#                            " (axis 2 = " + str(c) + ")\n"
#             print(process_log.split("\n")[-2] + "\n")
#             # nons=input("press enter")
#             # move palette under gripper
#             cmd = pal_message["palSet_position_1"].encode("ascii")
#             palPort.write(cmd)
#             unused_response = palPort.readline()
#             cmd = pal_message["palCSTR_off"].encode("ascii")
#             palPort.write(cmd)
#             unused_response = palPort.readline()
#             cmd = pal_message["palCSTR_on"].encode("ascii")
#             palPort.write(cmd)
#             unused_response = palPort.readline()
#             cmd = pal_message["palCSTR_off"].encode("ascii")
#             palPort.write(cmd)
#             unused_response = palPort.readline()
#             process_log += timestamped_msg("palette moved to position 1\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # moving?
#             tt_pal_moving(ttPort, palPort)
#             process_log += timestamped_msg("both robots finished moving\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # nons=input("press enter")
#
#             # move gripper down to palette
#             ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="100", axis3_pos=param_robo["gripper_down_palette"]))
#             unused_response = ttPort.readline()
#             process_log += timestamped_msg("gripper down to palette\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # moving?
#             tt_pal_moving(ttPort, palPort)
#             process_log += timestamped_msg("both robots finished moving\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # nons=input("press enter")
#
#             # close gripper
# ##            ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="0"))
# ##            unused_response = ttPort.readline()
# ##            ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="0", port="013E"))
# ##            unused_response = ttPort.readline()
#             cntrlPort.write(b"mgc$");
#             # wait
#             time.sleep(param_robo["gripper_open_wait"])
#             process_log += timestamped_msg("gripper closed, paused: ") + str(
#                 param_robo["gripper_open_wait"]) + "seconds\n"
#             print(process_log.split("\n")[-2] + "\n")
#             # nons=input("press enter")
#
#             # move gripper up
#             ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="100", axis3_pos=param_robo["gripper_up"]))
#             unused_response = ttPort.readline()
#             process_log += timestamped_msg("gripper up\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # moving?
#             tt_pal_moving(ttPort, palPort)
#             process_log += timestamped_msg("both robots finished moving\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # nons=input("press enter")
#
#             # move palette away from gripper
#             cmd = pal_message["palSet_position_2"].encode("ascii")
#             palPort.write(cmd)
#             unused_response = palPort.readline()
#             cmd = pal_message["palCSTR_off"].encode("ascii")
#             palPort.write(cmd)
#             unused_response = palPort.readline()
#             cmd = pal_message["palCSTR_on"].encode("ascii")
#             palPort.write(cmd)
#             unused_response = palPort.readline()
#             cmd = pal_message["palCSTR_off"].encode("ascii")
#             palPort.write(cmd)
#             unused_response = palPort.readline()
#             process_log += timestamped_msg("palette moved to position 2\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # moving?
#             tt_pal_moving(ttPort, palPort)
#             process_log += timestamped_msg("both robots finished moving\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # nons=input("press enter")
#
#             # move gripper to selected column
#             ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="010", axis2_pos=x))
#             unused_response = ttPort.readline()
#             process_log += timestamped_msg("tt moved to table tile: ") + str(col_i) + " (axis 2 = " + str(x) + ")\n"
#             print(process_log.split("\n")[-2] + "\n")
#             # moving?
#             tt_pal_moving(ttPort, palPort)
#             process_log += timestamped_msg("both robots finished moving\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # nons=input("press enter")
#
#             # move gripper down to table
#             ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="100", axis3_pos=param_robo["gripper_down_table"]))
#             unused_response = ttPort.readline()
#             process_log += timestamped_msg("gripper down to table\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # moving?
#             tt_pal_moving(ttPort, palPort)
#             process_log += timestamped_msg("both robots finished moving\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # nons=input("press enter")
#
#             # open gripper
# ##            ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="1"))
# ##            unused_response = ttPort.readline()
# ##            ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="0", port="013E"))
# ##            unused_response = ttPort.readline()
#             cntrlPort.write(b"mgo$");
#             # wait
#             time.sleep(param_robo["gripper_open_wait"])
#             process_log += timestamped_msg("gripper opened, paused: ") + str(
#                 param_robo["gripper_open_wait"]) + "seconds\n"
#             print(process_log.split("\n")[-2] + "\n")
#             # nons=input("press enter")
#
#             # move gripper to selected column + 0.25mm to left
#             ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="010", axis2_pos=(x+0.25)))
#             unused_response = ttPort.readline()
#             process_log += timestamped_msg("tt moved to left by 0.25mm\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # moving?
#             tt_pal_moving(ttPort, palPort)
#             process_log += timestamped_msg("both robots finished moving\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # nons=input("press enter")
#
#             # move gripper up
#             ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="100", axis3_pos=param_robo["gripper_up"]))
#             unused_response = ttPort.readline()
#             process_log += timestamped_msg("gripper up\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # moving?
#             tt_pal_moving(ttPort, palPort)
#             process_log += timestamped_msg("both robots finished moving\n")
#             print(process_log.split("\n")[-2] + "\n")
#             # nons=input("press enter")
#
#             # open gripper
# ##            ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="1"))
# ##            unused_response = ttPort.readline()
# ##            ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="1", port="013E"))
# ##            unused_response = ttPort.readline()
#             cntrlPort.write(b"mgw$");
#             # wait
#             # time.sleep(param_robo["gripper_open_wait"])
#             process_log += timestamped_msg("gripper opened, paused: ") + str(
#                 param_robo["gripper_open_wait"]) + "seconds\n"
#             print(process_log.split("\n")[-2] + "\n")


# # initialise robots
# ttPort, palPort, cntrlPort = initialise()
# image = readImage()
#
# # run sequence
# sequence(ttPort, palPort, cntrlPort, image)
#
# # close serial port
# ttPort.close()
# palPort.close()
# cntrlPort.close()
#
# # save log file
# process_log += timestamped_msg("saving log file\n")
# process_log += timestamped_msg("PROGRAM END")
# LOG_filename = LOG_file_save_location + "Sequence for mosaic_" + str(mosaic_number) + "_" + timestamped_msg("")[:-1]  + ".txt"
# LOG_filename = LOG_filename[2:].replace(":", "_")
# LOG_filename = "C:" + LOG_filename.replace(" ", "_")
# file = open(LOG_filename, "w")
# print("saving log file: ", LOG_filename)
# file.write(process_log)
# file.close()
# print("log file saved\n\nPROGRAM END")
# exit()
#
# # read in the file with the mosaic tile image information
# # read in the file with the mosaic tile configuration information




root = tk.Tk()
root.withdraw()
state = RuntimeState.RuntimeState()

# Setup main window
background = tk.Toplevel(root, background='black', width=640, height=480)
background.title("PxlRT Studio")
background.geometry("640x480")

# Create 4 windows that can be displayed in the info panel
initialise_panel = Initialise.Initialise(background, state)
manual_panel = Manual.Manual(background, state)
settings_panel = Settings.Settings(background, state)
tileprint_panel = TilePrint.TilePrint(background, state)

# Create main controls
controls = Controls.Controls(background, initialise_panel, manual_panel, settings_panel, tileprint_panel, state)



root.mainloop()
