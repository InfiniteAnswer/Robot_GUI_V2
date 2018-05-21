import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
from PIL import ImageTk, Image
import sys
from tkinter import filedialog
import pickle
import RR_CommandGenerator
import time
import threading
from threading import Thread

background_clr = "grey10"
foreground_clr = "white"
foreground_clr_off = "red"
foreground_clr_on = "green"
active_bg_clr = "green"
active_fg_clr = "black"
inactive_bg_clr = background_clr
inactive_fg_clr = foreground_clr
foreground_clr_banner = "grey50"
# button_font = ("Arial", 18)
button_font = "Arial 16 bold"
mapping_font = "Arial 16"
button_width = 30


class TilePrint():
    def __init__(self, parent, state):
        self.state = state
        background_image = Image.open("C:\\Users\\Finlay\\Documents\\Images\\grey10_480x315.jpg")
        self.background_image_tk = ImageTk.PhotoImage(background_image)
        self.info_tileprint = tk.Label(parent, image=self.background_image_tk, width=480, height=315)
        self.info_tileprint.place(x=130, y=135)

        self.banner = tk.Label(self.info_tileprint, text="Print Control",
                               bg=background_clr, fg=foreground_clr_banner)
        self.banner.place(x=0, y=0)

        self.button_loadfile = tk.Button(self.info_tileprint, text="Load File",
                                         bg=inactive_bg_clr, fg=inactive_fg_clr,
                                         activebackground=active_bg_clr,
                                         font=button_font,
                                         width=button_width,
                                         command=self.loadfile_callback)
        self.button_loadfile.place(x=40, y=20)

        self.button_start = tk.Button(self.info_tileprint, text="Start",
                                      bg=inactive_bg_clr, fg=inactive_fg_clr,
                                      activebackground=active_bg_clr,
                                      font=button_font,
                                      width=button_width,
                                      command=self.start_callback)
        self.button_start.place(x=40, y=70)

        self.button_pause = tk.Button(self.info_tileprint, text="Pause",
                                      bg=background_clr, fg=foreground_clr,
                                      activebackground=active_bg_clr,
                                      font=button_font,
                                      width=int(button_width / 2) - 1,
                                      command=self.pause_callback)
        self.button_pause.place(x=40, y=120)

        self.button_restart = tk.Button(self.info_tileprint, text="Restart",
                                        bg=background_clr, fg=foreground_clr,
                                        activebackground=active_bg_clr,
                                        font=button_font,
                                        width=int(button_width / 2) - 1,
                                        command=self.restart_callback)
        self.button_restart.place(x=440, y=120, anchor=tk.NE)

        self.button_abort = tk.Button(self.info_tileprint, text="Abort",
                                      bg=background_clr, fg=foreground_clr,
                                      activebackground=active_bg_clr,
                                      font=button_font,
                                      width=button_width)
        self.button_abort.place(x=40, y=170)

        self.print_speed = tk.Scale(self.info_tileprint, from_=10, to=100, resolution=10, orient=tk.HORIZONTAL,
                                    label="% of Max Speed",
                                    bd=0, highlightthickness=0, fg="yellow", bg="grey10", length=400)
        self.print_speed.bind("<ButtonRelease-1>", self.updatePrintSpeed_callback)
        self.print_speed.place(x=40, y=220)

        self.filename = ""
        self.image = []
        self.image_loaded = False

        self.info_tileprint.bind("<KeyPress>", self.keypress_callback)

    def loadfile_callback(self):
        # # OPTION 1: generate a new image from random tiles
        #     random_image_rows = 2
        #     random_image_columns = 2
        #     random_palette_tiles = 4
        #     self.image = list()
        #     for r in range(random_image_rows):
        #         new_row = list()
        #         for c in range(random_image_columns):
        #             new_row.append(randint(0, random_palette_tiles))
        #         self.image.append(new_row)

        # # OPTION 2: directly create 2 list of lists for the mosaic
        # self.image = [[0, 1, 0, 1, 0],
        #          [1, 0, 1, 0, 1],
        #          [0, 1, 0, 1, 0],
        #          [1, 0, 1, 0, 1],
        #          [0, 1, 0, 1, 0]]
        #
        self.image = [[0, 1, 0],
                      [1, 0, 1],
                      [0, 1, 0]]

        # self.image = [[0, 1],
        #              [1, 0]]
        #
        # self.image =[[0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0]]
        #
        # self.image = [[0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0]]

        # OPTION 3: load a file created by PxlRT
        # self.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
        #                                            filetypes=(("PxlRT files", "*.pkl"), ("all files", "*.*")))
        # # filename = "C:\\Users\\Victor\\Desktop\list_save.pkl"
        # self.image = pickle.load(open(self.filename, "rb"))
        self.image_loaded = True
        self.button_loadfile.config(bg=active_bg_clr, fg=active_fg_clr)

    def updatePrintSpeed_callback(self, e):
        self.state.printSpeed = self.print_speed.get()

    def start_callback(self):
        if (self.image_loaded and not self.state.printing):
            self.button_start.config(bg=active_bg_clr, fg=active_fg_clr)

            # grab focus on current window to ensure any key press is caught as an event
            # self.info_tileprint.grab_set()
            time.sleep(2)  # safety delay before interpreting keypress as request to pause

            self.state.printing = True
            th = Thread(target=self.start_sequence)
            th.start()
            self.info_tileprint.focus_set()
            self.info_tileprint.grab_set()

    def pause_callback(self):
        if (self.state.printing and not self.state.printpause):
            self.state.printpause = True
            self.button_pause.config(bg=active_bg_clr, fg=active_fg_clr)
            self.button_start.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
            self.button_restart.config(bg=inactive_bg_clr, fg=inactive_fg_clr)

    def restart_callback(self):
        if self.state.printpause:
            self.state.printpause = False
            self.button_pause.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
            self.button_start.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
            self.button_restart.config(bg=active_bg_clr, fg=active_fg_clr)

    def abort_callback(self):
        pass

    def keypress_callback(self, e):
        print("KEY PRESSED")
        if self.state.printing:
            self.pause_callback()

    def start_sequence(self):
        # gripper up
        # gripper wide open
        # pal under gripper
        # gripper over to pal pickup position
        # gripper down to pal
        # gripper close
        # gripper up
        # pal back to reload
        # gripper over to table dropoff position
        # gripper down
        # gripper open
        # gripper shuffle
        # REPEAT

        image_rows = len(self.image)
        image_cols = len(self.image[0])

        # add tile number to log file
        self.state.process_log += "Sequence for mosaic: " + str(self.state.mosaic_number) + "\n"
        print(self.state.process_log.split("\n")[-2])

        # gripper up
        self.state.ttPort.write(
            RR_CommandGenerator.ttMoveAbs(axis="100",
                                          speed=int(self.state.maxTTmovingSpeed / 100 * self.state.printSpeed),
                                          axis3_pos=self.state.param_robo["gripper_up"]))
        self.state.last_commanded_ax3 = self.state.param_robo["gripper_up"]
        unused_response = self.state.ttPort.readline()
        self.state.process_log += self.state.timestamped_msg("gripper up\n")
        print(self.state.process_log.split("\n")[-2])

        # moving?
        self.state.tt_pal_moving()
        self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
        print(self.state.process_log.split("\n")[-2])

        # open gripper
        ##    self.state.ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="1"))
        ##    unused_response = self.state.ttPort.readline()
        ##    self.state.ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="1", port="013E"))
        ##    unused_response = self.state.ttPort.readline()
        for i in range(3):
            self.state.cntrlPort.write(b"mgw$")
            time.sleep(0.5)
            self.state.cntrlPort.write(b"mgo$")
            time.sleep(0.5)
            self.state.cntrlPort.write(b"mgc$")
            time.sleep(0.5)
        time.sleep(1)
        self.state.cntrlPort.write(b"mgw$")
        # wait
        time.sleep(self.state.param_robo["gripper_open_wait"])
        self.state.process_log += self.state.timestamped_msg("gripper opened, paused: ") + \
                                  str(self.state.param_robo["gripper_open_wait"]) + "seconds\n"
        print(self.state.process_log.split("\n")[-2] + "\n")
        # nons=input("press enter")

        for row_i, row in enumerate(self.image):
            x, y = self.state.pixel2table(0, row_i)

            # move to next table row position
            self.state.ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="001",
                                                                  speed=int(
                                                                      self.state.maxTTmovingSpeed / 100 * self.state.printSpeed),
                                                                  axis1_pos=y))
            self.state.last_commanded_ax1 = y
            unused_response = self.state.ttPort.readline()
            self.state.process_log += self.state.timestamped_msg("tt moved to row: ") + str(row_i) + "\n"
            print(self.state.process_log.split("\n")[-2])
            # moving?
            self.state.tt_moving()
            self.state.process_log += self.state.timestamped_msg("tt robot finished moving\n")
            print(self.state.process_log.split("\n")[-2] + "\n")

            for col_i, col in enumerate(row):
                # Add tile number to log
                self.state.process_log += "Sequence for tile row: " + str(row_i) + " column: " + str(col_i) + "\n"
                print("\n\n-------------------------------------------------\n")
                print(self.state.process_log.split("\n")[-2] + "\n")

                x, y = self.state.pixel2table(col_i, row_i)
                c = self.state.colour2palette(self.image[row_i][col_i])

                # move to next colour palette position
                self.state.ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="010",
                                                                      speed=int(
                                                                          self.state.maxTTmovingSpeed / 100 * self.state.printSpeed),
                                                                      axis2_pos=c))
                self.state.last_commanded_ax2 = c
                unused_response = self.state.ttPort.readline()
                self.state.process_log += self.state.timestamped_msg("tt moved to colour: ") + \
                                          str(self.image[row_i][col_i]) + \
                                          " (axis 2 = " + str(c) + ")\n"
                print(self.state.process_log.split("\n")[-2] + "\n")
                # nons=input("press enter")
                # move palette under gripper
                cmd = self.state.pal_message["palSet_position_1"].encode("ascii")
                self.state.palPort.write(cmd)
                unused_response = self.state.palPort.readline()
                cmd = self.state.pal_message["palCSTR_off"].encode("ascii")
                self.state.palPort.write(cmd)
                unused_response = self.state.palPort.readline()
                cmd = self.state.pal_message["palCSTR_on"].encode("ascii")
                self.state.palPort.write(cmd)
                unused_response = self.state.palPort.readline()
                cmd = self.state.pal_message["palCSTR_off"].encode("ascii")
                self.state.palPort.write(cmd)
                unused_response = self.state.palPort.readline()
                self.state.process_log += self.state.timestamped_msg("palette moved to position 1\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # moving?
                self.state.tt_pal_moving()
                self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # nons=input("press enter")

                # move gripper down to palette
                self.state.ttPort.write(
                    RR_CommandGenerator.ttMoveAbs(axis="100",
                                                  speed=int(self.state.maxTTmovingSpeed / 100 * self.state.printSpeed),
                                                  axis3_pos=self.state.param_robo["gripper_down_palette"]))
                self.state.last_commanded_ax3 = self.state.param_robo["gripper_down_palette"]
                unused_response = self.state.ttPort.readline()
                self.state.process_log += self.state.timestamped_msg("gripper down to palette\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # moving?
                self.state.tt_pal_moving()
                self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # nons=input("press enter")

                # close gripper
                ##            self.state.ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="0"))
                ##            unused_response = self.state.ttPort.readline()
                ##            self.state.ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="0", port="013E"))
                ##            unused_response = self.state.ttPort.readline()
                self.state.cntrlPort.write(b"mgc$")
                # wait
                time.sleep(self.state.param_robo["gripper_open_wait"])
                self.state.process_log += self.state.timestamped_msg("gripper closed, paused: ") + str(
                    self.state.param_robo["gripper_open_wait"]) + "seconds\n"
                print(self.state.process_log.split("\n")[-2] + "\n")
                # nons=input("press enter")

                # move gripper up
                self.state.ttPort.write(
                    RR_CommandGenerator.ttMoveAbs(axis="100",
                                                  speed=int(self.state.maxTTmovingSpeed / 100 * self.state.printSpeed),
                                                  axis3_pos=self.state.param_robo["gripper_up"]))
                self.state.last_commanded_ax3 = self.state.param_robo["gripper_up"]
                unused_response = self.state.ttPort.readline()
                self.state.process_log += self.state.timestamped_msg("gripper up\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # moving?
                self.state.tt_pal_moving()
                self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # nons=input("press enter")

                # move palette away from gripper
                cmd = self.state.pal_message["palSet_position_2"].encode("ascii")
                self.state.palPort.write(cmd)
                unused_response = self.state.palPort.readline()
                cmd = self.state.pal_message["palCSTR_off"].encode("ascii")
                self.state.palPort.write(cmd)
                unused_response = self.state.palPort.readline()
                cmd = self.state.pal_message["palCSTR_on"].encode("ascii")
                self.state.palPort.write(cmd)
                unused_response = self.state.palPort.readline()
                cmd = self.state.pal_message["palCSTR_off"].encode("ascii")
                self.state.palPort.write(cmd)
                unused_response = self.state.palPort.readline()
                self.state.process_log += self.state.timestamped_msg("palette moved to position 2\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # moving?
                self.state.tt_pal_moving()
                self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # nons=input("press enter")

                # move gripper to selected column
                self.state.ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="010",
                                                                      speed=int(
                                                                          self.state.maxTTmovingSpeed / 100 * self.state.printSpeed),
                                                                      axis2_pos=x))
                self.state.last_commanded_ax2 = x
                unused_response = self.state.ttPort.readline()
                self.state.process_log += self.state.timestamped_msg("tt moved to table tile: ") + str(
                    col_i) + " (axis 2 = " + str(x) + ")\n"
                print(self.state.process_log.split("\n")[-2] + "\n")
                # moving?
                self.state.tt_pal_moving()
                self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # nons=input("press enter")

                # move gripper down to table
                self.state.ttPort.write(
                    RR_CommandGenerator.ttMoveAbs(axis="100",
                                                  speed=int(self.state.maxTTmovingSpeed / 100 * self.state.printSpeed),
                                                  axis3_pos=self.state.param_robo["gripper_down_table"]))
                self.state.last_commanded_ax3 = self.state.param_robo["gripper_down_table"]
                unused_response = self.state.ttPort.readline()
                self.state.process_log += self.state.timestamped_msg("gripper down to table\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # moving?
                self.state.tt_pal_moving()
                self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # nons=input("press enter")

                # open gripper
                ##            self.state.ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="1"))
                ##            unused_response = self.state.ttPort.readline()
                ##            self.state.ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="0", port="013E"))
                ##            unused_response = self.state.ttPort.readline()
                self.state.cntrlPort.write(b"mgo$")
                # wait
                time.sleep(self.state.param_robo["gripper_open_wait"])
                self.state.process_log += self.state.timestamped_msg("gripper opened, paused: ") + str(
                    self.state.param_robo["gripper_open_wait"]) + "seconds\n"
                print(self.state.process_log.split("\n")[-2] + "\n")
                # nons=input("press enter")

                # move gripper to selected column + 0.25mm to left
                # self.state.ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="010", axis2_pos=(x + 0.25)))
                # unused_response = self.state.ttPort.readline()
                # self.state.process_log += self.state.timestamped_msg("tt moved to left by 0.25mm\n")
                # print(self.state.process_log.split("\n")[-2] + "\n")
                # # moving?
                # self.state.tt_pal_moving()
                # self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
                # print(self.state.process_log.split("\n")[-2] + "\n")
                # # nons=input("press enter")

                # move gripper up
                self.state.ttPort.write(
                    RR_CommandGenerator.ttMoveAbs(axis="100",
                                                  speed=int(self.state.maxTTmovingSpeed / 100 * self.state.printSpeed),
                                                  axis3_pos=self.state.param_robo["gripper_up"]))
                self.state.last_commanded_ax3 = self.state.param_robo["gripper_up"]
                unused_response = self.state.ttPort.readline()
                self.state.process_log += self.state.timestamped_msg("gripper up\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # moving?
                self.state.tt_pal_moving()
                self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
                print(self.state.process_log.split("\n")[-2] + "\n")
                # nons=input("press enter")

                # open gripper
                ##            self.state.ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="1"))
                ##            unused_response = self.state.ttPort.readline()
                ##            self.state.ttPort.write(RR_CommandGenerator.ttOutputPortSet(on="1", port="013E"))
                ##            unused_response = self.state.ttPort.readline()
                self.state.cntrlPort.write(b"mgw$")
                # wait
                # time.sleep(self.state.param_robo["gripper_open_wait"])
                self.state.process_log += self.state.timestamped_msg("gripper opened, paused: ") + str(
                    self.state.param_robo["gripper_open_wait"]) + "seconds\n"
                print(self.state.process_log.split("\n")[-2] + "\n")
        self.button_start.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
        self.button_restart.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
        self.info_tileprint.grab_release()
        self.state.printing = False
