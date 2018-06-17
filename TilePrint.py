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
        background_image = Image.open("C:\\Users\\Finlay\\Documents\\Images\\480x315_BLACK.jpg")
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
                                         width=int(button_width / 2) - 1,
                                         command=self.loadfile_callback)
        self.button_loadfile.place(x=40, y=20)

        self.button_start = tk.Button(self.info_tileprint, text="Start",
                                      bg=inactive_bg_clr, fg=inactive_fg_clr,
                                      activebackground=active_bg_clr,
                                      font=button_font,
                                      width=int(button_width / 2) - 1,
                                      command=self.start_callback)
        self.button_start.place(x=440, y=20, anchor=tk.NE)

        self.button_pause = tk.Button(self.info_tileprint, text="Pause",
                                      bg=background_clr, fg=foreground_clr,
                                      activebackground=active_bg_clr,
                                      font=button_font,
                                      width=int(button_width / 2) - 1,
                                      command=self.pause_callback)
        self.button_pause.place(x=40, y=70)

        self.button_restart = tk.Button(self.info_tileprint, text="Restart",
                                        bg=background_clr, fg=foreground_clr,
                                        activebackground=active_bg_clr,
                                        font=button_font,
                                        width=int(button_width / 2) - 1,
                                        command=self.restart_callback)
        self.button_restart.place(x=440, y=70, anchor=tk.NE)

        self.button_pal2grip = tk.Button(self.info_tileprint, text="Pal2Grip",
                                         bg=background_clr, fg=foreground_clr,
                                         activebackground=active_bg_clr,
                                         font=button_font,
                                         width=int(button_width / 2) - 1,
                                         command=self.pal2grip_callback)
        self.button_pal2grip.place(x=40, y=120)

        self.button_pal2mag = tk.Button(self.info_tileprint, text="Pal2Mag",
                                        bg=background_clr, fg=foreground_clr,
                                        activebackground=active_bg_clr,
                                        font=button_font,
                                        width=int(button_width / 2) - 1,
                                        command=self.pal2mag_callback)
        self.button_pal2mag.place(x=440, y=120, anchor=tk.NE)

        self.button_abort = tk.Button(self.info_tileprint, text="Abort",
                                      bg=background_clr, fg=foreground_clr,
                                      activebackground=active_bg_clr,
                                      font=button_font,
                                      width=button_width,
                                      command=self.abort_callback)
        self.button_abort.place(x=40, y=170)

        self.print_speed = tk.Scale(self.info_tileprint, from_=10, to=100, resolution=10, orient=tk.HORIZONTAL,
                                    label="% of Max Speed",
                                    bd=0, highlightthickness=0, fg="yellow", bg="grey10", length=400)
        self.print_speed.bind("<ButtonRelease-1>", self.updatePrintSpeed_callback)
        self.print_speed.place(x=40, y=220)

        self.filename = ""
        self.image = []
        self.image_loaded = False

        th_error_server = Thread(target=self.error_server)
        th_error_server.start()

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

        # OPTION 2: directly create 2 list of lists for the mosaic
        self.image = [[0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
                      [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0],
                      [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
                      [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2],
                      [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
                      [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0],
                      [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
                      [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2],
                      [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
                      [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0],
                      [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
                      [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2]]

        ##        self.image = [[2, 2, 2, 2, 2],
        ##                      [2, 2, 2, 2, 2]]

        # self.image = [[0, 1, 0],
        #               [1, 0, 1],
        #               [0, 1, 0]]

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
        if (self.image_loaded and not self.state.printing and self.state.all_axes_homed):
            self.button_start.config(bg=active_bg_clr, fg=active_fg_clr)

            # grab focus on current window to ensure any key press is caught as an event
            # self.info_tileprint.grab_set()
            time.sleep(2)  # safety delay before interpreting keypress as request to pause

            self.state.printing = True
            th = Thread(target=self.start_sequence)
            th.start()
            ##            th_error_server = Thread(target=self.error_server)
            ##            th_error_server.start()
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
            self.button_pause.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
            self.button_start.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
            self.button_restart.config(bg=active_bg_clr, fg=active_fg_clr)
            if self.state.printing:
                self.state.recovery_initiated = True
                self.move_last_commanded_xyz()

    def abort_callback(self):
        # only possible from printpause state
        if self.state.printpause:
            # add log message to say aborted
            self.state.process_log += self.state.timestamped_msg("print job aborted\n")
            print(self.state.process_log.split("\n")[-2] + "\n")

            # change state to not printing
            # add log message to say lock parameters are reset
            self.state.printing = False
            sleep(0.5)
            self.state.printpause = False

    def pal2grip_callback(self):
        if self.state.printpause:
            self.state.palette_motion_during_printpause = True
            time.sleep(0.25)
            self.palette_to_gripper()
            time.sleep(1)
            self.state.palette_motion_during_printpause = False

    def pal2mag_callback(self):
        if self.state.printpause:
            self.state.palette_motion_during_printpause = True
            time.sleep(0.25)
            self.palette_to_magazine()
            time.sleep(1)
            self.state.palette_motion_during_printpause = False

    def keypress_callback(self, e):
        print("KEY PRESSED")
        if self.state.printing:
            self.pause_callback()

    def start_sequence(self):
        image_rows = len(self.image)
        image_cols = len(self.image[0])

        # add tile section number to log file
        self.state.process_log += "Sequence for mosaic: " + str(self.state.mosaic_number) + "\n"
        print(self.state.process_log.split("\n")[-2])

        # gripper up
        if self.state.printing:
            self.gripper_to_safety_height()

        # gripper startup routine, ending in wide open gripper
        self.gripper_startup_routine()

        for row_i, row in enumerate(self.image):
            x, y = self.state.pixel2table(0, row_i)

            # move to next table row position
            if self.execute_next_command():
                self.move_axis1(y, row_i)

            for col_i, col in enumerate(row):
                # Add tile row number to log
                self.state.process_log += "Sequence for tile row: " + str(row_i) + " column: " + str(col_i) + "\n"
                print("\n\n-------------------------------------------------\n")
                print(self.state.process_log.split("\n")[-2] + "\n")

                x, y = self.state.pixel2table(col_i, row_i)
                c = self.state.colour2palette(self.image[row_i][col_i])

                # move to next colour palette position
                if self.execute_next_command():
                    self.move_axis2_colour(c, row_i, col_i)

                # move palette under gripper
                if self.execute_next_command():
                    self.state.last_commanded_ax4 = 1
                    self.palette_to_gripper()

                # move gripper down to palette
                if self.execute_next_command():
                    self.gripper_to_palette()

                # close gripper
                if self.execute_next_command():
                    self.close_gripper()

                # move gripper up
                if self.execute_next_command():
                    self.gripper_to_safety_height()

                # move palette away from gripper
                if self.execute_next_command():
                    self.state.last_commanded_ax4 = 2
                    self.palette_to_magazine()

                # move gripper to selected column
                if self.execute_next_command():
                    self.move_axis2_column(x, col_i)

                # move gripper down to table
                if self.execute_next_command():
                    self.gripper_to_table()

                # open gripper
                if self.execute_next_command():
                    self.open_gripper()

                # move gripper up
                if self.execute_next_command():
                    self.gripper_to_safety_height()

                # open gripper wide
                if self.execute_next_command():
                    self.open_gripper_wide()

        self.button_start.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
        self.button_pause.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
        self.button_restart.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
        self.info_tileprint.grab_release()
        self.state.printing = False
        self.state.process_log += self.state.timestamped_msg("JOB COMPLETE!\n")
        print(self.state.process_log.split("\n")[-2] + "\n")
        # save log file
        self.state.process_log += self.state.timestamped_msg("preparing new log file save name\n")
        LOG_filename = self.state.LOG_file_save_location + "Sequence for mosaic_" + str(
            self.state.mosaic_number) + "_" + self.state.timestamped_msg("")[:-1] + ".txt"
        LOG_filename = LOG_filename[2:].replace(":", "_")
        LOG_filename = "C:" + LOG_filename.replace(" ", "_")
        file = open(LOG_filename, "w")
        print("saving log file: ", LOG_filename)
        file.write(self.state.process_log)
        file.close()
        print("file saved")
        print("clearing process log for next print job")
        self.state.process_log = ""
        print("READY!")

    def error_server(self):
        msg = ""
        time.sleep(1)
        self.state.cntrlPort.flushOutput()
        while True:
            # c = c+self.state.cntrlPort.read().decode("utf-8")
            c = self.state.cntrlPort.read()
            try:
                c_decoded = c.decode("utf-8")
                msg += c_decoded
                # print("raw: ", c)
                # print("decoded: ", c.decode("utf-8"))
                if c == b'':
                    time.sleep(1)
                # else:
                #   print(c, end='')
                if c == b'\n':
                    # print("Error message starting")
                    # print(msg)
                    # print("Error message ended")
                    if msg[:3] == "mf0":
                        self.state.process_log += self.state.timestamped_msg("paused because of empty cartridge\n")
                        print(self.state.process_log.split("\n")[-2] + "\n")
                        self.state.printpause = True
                        self.button_pause.config(bg=active_bg_clr, fg=active_fg_clr)
                        self.button_start.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
                        self.button_restart.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
                    if msg[:3] == "gf0":
                        self.state.process_log += self.state.timestamped_msg("paused because of gripper crash\n")
                        print(self.state.process_log.split("\n")[-2] + "\n")
                        self.state.printpause = True
                        self.button_pause.config(bg=active_bg_clr, fg=active_fg_clr)
                        self.button_start.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
                        self.button_restart.config(bg=inactive_bg_clr, fg=inactive_fg_clr)
                    msg = ""
            except:
                pass

    def gripper_startup_routine(self):
        for i in range(3):
            self.state.cntrlPort.write(b"mgw$")
            time.sleep(0.5)
            self.state.cntrlPort.write(b"mgo$")
            time.sleep(0.5)
            self.state.cntrlPort.write(b"mgc$")
            time.sleep(0.5)
        time.sleep(1)
        self.state.cntrlPort.write(b"mgw$")
        time.sleep(self.state.param_robo["gripper_open_wait"])
        self.state.process_log += self.state.timestamped_msg("gripper opened, paused: ") + \
                                  str(self.state.param_robo["gripper_open_wait"]) + "seconds\n"
        print(self.state.process_log.split("\n")[-2] + "\n")
        self.state.process_log += self.state.timestamped_msg("gripper startup sequence complete\n")
        print(self.state.process_log.split("\n")[-2] + "\n")

    def move_axis1(self, y, row_i):
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

    def move_axis2_colour(self, c, row_i, col_i):
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

    def move_axis2_column(self, x, col_i):
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

    def move_last_commanded_xyz(self):
        # goto last pal position
        if self.state.last_commanded_ax4 == 1:
            self.palette_to_gripper()
        if self.state.last_commanded_ax4 == 2:
            self.palette_to_magazine()

        # goto last x position
        self.state.ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="001", axis1_pos=self.state.last_commanded_ax1))
        unused_response = self.state.ttPort.readline()
        self.state.process_log += self.state.timestamped_msg("returning ax1-table to last commanded position\n")
        print(self.state.process_log.split("\n")[-2])
        # moving?
        self.state.tt_pal_moving()
        self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
        print(self.state.process_log.split("\n")[-2] + "\n")

        # goto last y position
        self.state.ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="010", axis2_pos=self.state.last_commanded_ax2))
        unused_response = self.state.ttPort.readline()
        self.state.process_log += self.state.timestamped_msg("returning ax2-bridge to last commanded position\n")
        print(self.state.process_log.split("\n")[-2])
        # moving?
        self.state.tt_pal_moving()
        self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
        print(self.state.process_log.split("\n")[-2] + "\n")

        # goto last z position
        self.state.ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="100", axis3_pos=self.state.last_commanded_ax3))
        unused_response = self.state.ttPort.readline()
        self.state.process_log += self.state.timestamped_msg("returning ax3-gripper to last commanded position\n")
        print(self.state.process_log.split("\n")[-2])
        # moving?
        self.state.tt_pal_moving()
        self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
        print(self.state.process_log.split("\n")[-2] + "\n")

        self.state.recovery_initiated = False
        self.state.printpause = False

    def palette_to_gripper(self):
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
        self.button_pal2grip.config(bg=active_bg_clr, fg=active_fg_clr)
        self.button_pal2mag.config(bg=inactive_bg_clr, fg=inactive_fg_clr)

    def palette_to_magazine(self):
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
        self.button_pal2mag.config(bg=active_bg_clr, fg=active_fg_clr)
        self.button_pal2grip.config(bg=inactive_bg_clr, fg=inactive_fg_clr)

    def gripper_to_palette(self):
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

    def gripper_to_safety_height(self):
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

    def gripper_to_table(self):
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

    def close_gripper(self):
        self.state.cntrlPort.write(b"mgc$")
        time.sleep(self.state.param_robo["gripper_open_wait"])
        self.state.process_log += self.state.timestamped_msg("gripper closed, paused: ") + str(
            self.state.param_robo["gripper_open_wait"]) + "seconds\n"
        print(self.state.process_log.split("\n")[-2] + "\n")

    def open_gripper(self):
        self.state.cntrlPort.write(b"mgo$")
        time.sleep(self.state.param_robo["gripper_open_wait"])
        self.state.process_log += self.state.timestamped_msg("gripper opened, paused: ") + str(
            self.state.param_robo["gripper_open_wait"]) + "seconds\n"
        print(self.state.process_log.split("\n")[-2] + "\n")

    def open_gripper_wide(self):
        self.state.cntrlPort.write(b"mgw$")
        time.sleep(self.state.param_robo["gripper_open_wait"])
        self.state.process_log += self.state.timestamped_msg("gripper opened wide, paused: ") + str(
            self.state.param_robo["gripper_open_wait"]) + "seconds\n"
        print(self.state.process_log.split("\n")[-2] + "\n")

    def execute_next_command(self):
        while self.state.printpause:
            sleep(self.state.POLLING_DELAY)
        return self.state.printing
