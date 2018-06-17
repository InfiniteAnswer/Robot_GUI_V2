import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
import time
from PIL import ImageTk, Image
import sys
import RR_CommandGenerator

background_clr = "grey10"
foreground_clr = "yellow"
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


class Initialise():
    def __init__(self, parent, state):
        self.state = state
        background_image = Image.open("C:\\Users\\Finlay\\Documents\\Images\\480x315_BLACK.jpg")
        self.background_image_tk = ImageTk.PhotoImage(background_image)
        self.info_initialise = tk.Label(parent, image=self.background_image_tk, width=480, height=315)
        self.info_initialise.place(x=130, y=135)

        self.banner = tk.Label(self.info_initialise, text="Initialisation Control",
                               bg=background_clr, fg=foreground_clr_banner)
        self.banner.place(x=0, y=0)

        # create and define REHOME_TT button
        self.rehome_TT_button_state = self.state.homeax1 and self.state.homeax2 and self.state.homeax3
        self.rehome_TT_button_bkclr = "green" if self.rehome_TT_button_state else "red"
        self.rehome_TT_button_fgclr = "white"
        self.button_rehome_TT = tk.Button(self.info_initialise, text="Rehome TT",
                                          bg=self.rehome_TT_button_bkclr, fg=self.rehome_TT_button_fgclr,
                                          activebackground=active_bg_clr,
                                          font=button_font,
                                          width=button_width,
                                          command=self.rehome_TT_callback)
        self.button_rehome_TT.place(x=40, y=20)

        # create and define REHOME_PAL button
        self.rehome_PAL_button_state = self.state.homeax4
        self.rehome_PAL_button_bkclr = "green" if self.rehome_PAL_button_state else "red"
        self.rehome_PAL_button_fgclr = "white"
        self.button_rehome_PAL = tk.Button(self.info_initialise, text="Rehome PAL",
                                           bg=self.rehome_PAL_button_bkclr, fg=self.rehome_PAL_button_fgclr,
                                           activebackground=active_bg_clr,
                                           font=button_font,
                                           width=button_width,
                                           command=self.rehome_PAL_callback)
        self.button_rehome_PAL.place(x=40, y=70)

        # create and define MAG2PAL_NEAR button
        self.button_Mag2PAL_near = tk.Button(self.info_initialise, text="Chute 2 Grip",
                                             bg=background_clr, fg=foreground_clr,
                                             activebackground=active_bg_clr,
                                             font=button_font,
                                             width=int(button_width / 2) - 1,
                                             command=self.Mag2PAL_near)
        self.button_Mag2PAL_near.place(x=40, y=120)

        # create and define MAG2PAL_FAR button
        self.button_Mag2PAL_far = tk.Button(self.info_initialise, text="Chute 2 Mag",
                                            bg=background_clr, fg=foreground_clr,
                                            activebackground=active_bg_clr,
                                            font=button_font,
                                            width=int(button_width / 2) - 1,
                                            command=self.Mag2PAL_far)
        self.button_Mag2PAL_far.place(x=40, y=170)

        self.button_pause = tk.Button(self.info_initialise, text="Load Tray",
                                      bg=background_clr, fg=foreground_clr,
                                      activebackground=active_bg_clr,
                                      font=button_font,
                                      width=int(button_width / 2) - 1,
                                      command=self.load_tray)
        self.button_pause.place(x=440, y=120, anchor=tk.NE)

        self.button_restart = tk.Button(self.info_initialise, text="Tray 2 Start",
                                        bg=background_clr, fg=foreground_clr,
                                        activebackground=active_bg_clr,
                                        font=button_font,
                                        width=int(button_width / 2) - 1,
                                        command=self.tray_home)
        self.button_restart.place(x=440, y=170, anchor=tk.NE)

        # create 8 entries for 8 cartridge mappings
        self.mapping_frame = tk.Frame(self.info_initialise, width=400, height=80, bg=background_clr, bd=2,
                                      relief=tk.RAISED)
        self.mapping_frame.place(x=40, y=220)
        self.cartridge_label = tk.Label(self.mapping_frame, text="Cartridge Mapping",
                                        bg=background_clr, fg=foreground_clr)
        self.cartridge_label.place(x=20, y=20)
        self.cartridge_label_mapping = []
        self.cartridge_label_mapping_entry = []
        for i in range(8):
            self.cartridge_label_mapping.append(tk.Label(self.mapping_frame, text=i,
                                                         bg=background_clr, fg=foreground_clr,
                                                         font=mapping_font))
            self.cartridge_label_mapping_entry.append(tk.Entry(self.mapping_frame, width=1, font=mapping_font))
            self.cartridge_label_mapping[i].place(x=140 + i * 30, y=0)
            self.cartridge_label_mapping_entry[i].place(x=140 + i * 30, y=33)

    def rehome_TT_callback(self):
        # check if axes of tt are homed
        cmd = RR_CommandGenerator.ttMovingQuery(axis="001")
        self.state.ttPort.write(cmd)
        response_tt_1 = self.state.ttPort.readline()
        cmd = RR_CommandGenerator.ttMovingQuery(axis="010")
        self.state.ttPort.write(cmd)
        response_tt_2 = self.state.ttPort.readline()
        cmd = RR_CommandGenerator.ttMovingQuery(axis="100")
        self.state.ttPort.write(cmd)
        response_tt_3 = self.state.ttPort.readline()

        # if not, home z axis of tt first for SAFETY reasons
        response_tt_1 = '0x' + str(response_tt_1)[11]
        response_tt_2 = '0x' + str(response_tt_2)[11]
        response_tt_3 = '0x' + str(response_tt_3)[11]

        tt_1_home_complete = ((eval(response_tt_1) & 0b0100) == 4)
        tt_2_home_complete = ((eval(response_tt_2) & 0b0100) == 4)
        tt_3_home_complete = ((eval(response_tt_3) & 0b0100) == 4)

        if not (tt_3_home_complete):
            self.state.process_log += self.state.timestamped_msg("executing TT home for z-axis...\n")
            print(self.state.process_log.split("\n")[-2])
            self.state.ttPort.write(RR_CommandGenerator.ttHome(axis="100"))
            unused_response = self.state.ttPort.readline()
            # moving?
            self.state.tt_pal_moving()
        else:
            self.state.process_log += self.state.timestamped_msg("TT z-axis already homed, no need to repeat\n")
            print(self.state.process_log.split("\n")[-2])

        if not (tt_2_home_complete):
            self.state.process_log += self.state.timestamped_msg("executing TT home for y-axis...\n")
            print(self.state.process_log.split("\n")[-2])
            self.state.ttPort.write(RR_CommandGenerator.ttHome(axis="010"))
            unused_response = self.state.ttPort.readline()
            # moving?
            self.state.tt_pal_moving()
        else:
            self.state.process_log += self.state.timestamped_msg("TT y-axis already homed, no need to repeat\n")
            print(self.state.process_log.split("\n")[-2])

        if not (tt_1_home_complete):
            self.state.process_log += self.state.timestamped_msg("executing TT home for x-axis...\n")
            print(self.state.process_log.split("\n")[-2])
            self.state.ttPort.write(RR_CommandGenerator.ttHome(axis="001"))
            unused_response = self.state.ttPort.readline()
            # moving?
            self.state.tt_pal_moving()
        else:
            self.state.process_log += self.state.timestamped_msg("TT x-axis already homed, no need to repeat\n")
            print(self.state.process_log.split("\n")[-2])

        # check if axes of tt are successfully homed
        cmd = RR_CommandGenerator.ttMovingQuery(axis="001")
        self.state.ttPort.write(cmd)
        response_tt_1 = self.state.ttPort.readline()
        cmd = RR_CommandGenerator.ttMovingQuery(axis="010")
        self.state.ttPort.write(cmd)
        response_tt_2 = self.state.ttPort.readline()
        cmd = RR_CommandGenerator.ttMovingQuery(axis="100")
        self.state.ttPort.write(cmd)
        response_tt_3 = self.state.ttPort.readline()

        response_tt_1 = '0x' + str(response_tt_1)[11]
        response_tt_2 = '0x' + str(response_tt_2)[11]
        response_tt_3 = '0x' + str(response_tt_3)[11]

        self.state.homeax1 = ((eval(response_tt_1) & 0b0100) == 4)
        self.state.homeax2 = ((eval(response_tt_2) & 0b0100) == 4)
        self.state.homeax3 = ((eval(response_tt_3) & 0b0100) == 4)

        self.rehome_TT_button_state = self.state.homeax1 and self.state.homeax2 and self.state.homeax3
        self.rehome_TT_button_bkclr = "green" if self.rehome_TT_button_state else "red"
        self.button_rehome_TT.config(bg=self.rehome_TT_button_bkclr)

    def rehome_PAL_callback(self):
        # check to see if PAL is homed
        cmd = self.state.pal_message["palQuery_home"].encode("ascii")
        self.state.palPort.write(cmd)
        response_pal = self.state.palPort.readline()
        response_pal = '0x' + str(response_pal)[11]
        pal = (eval(response_pal) & 0b01) == 1

        # if PAL is not homed, perform home operation
        if not (pal):
            self.state.process_log += self.state.timestamped_msg("executing PAL home...\n")
            print(self.state.process_log.split("\n")[-2])
            cmd = self.state.pal_message["palHome"].encode("ascii")
            self.state.palPort.write(cmd)
            unused_response = self.state.palPort.readline()
            # moving?
            self.state.tt_pal_moving()
        else:
            self.state.process_log += self.state.timestamped_msg("PAL already homed, no need to repeat\n")
            print(self.state.process_log.split("\n")[-2])

        # check to see if PAL is successfully homed
        cmd = self.state.pal_message["palQuery_home"].encode("ascii")
        self.state.palPort.write(cmd)
        response_pal = self.state.palPort.readline()
        response_pal = '0x' + str(response_pal)[11]
        self.state.homeax4 = (eval(response_pal) & 0b01) == 1
        self.rehome_PAL_button_state = self.state.homeax4

        self.rehome_PAL_button_bkclr = "green" if self.rehome_PAL_button_state else "red"
        self.button_rehome_PAL.config(bg=self.rehome_PAL_button_bkclr)

    def Mag2PAL_near(self):
        if (self.state.all_axes_homed and not self.state.printing) or (
                self.state.all_axes_homed and self.state.printpause):
            # move palette away from gripper
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
            self.state.process_log += self.state.timestamped_msg("palette moved to position 2\n")
            print(self.state.process_log.split("\n")[-2] + "\n")
            # moving?
            self.state.tt_pal_moving()
            self.state.process_log += self.state.timestamped_msg("both robots finished moving\n")
            print(self.state.process_log.split("\n")[-2] + "\n")
            self.button_Mag2PAL_near.config(bg=active_bg_clr, fg=active_fg_clr)
            self.button_Mag2PAL_far.config(bg=inactive_bg_clr, fg=inactive_fg_clr)

    def Mag2PAL_far(self):
        if (self.state.all_axes_homed and not self.state.printing) or (
                self.state.all_axes_homed and self.state.printpause):
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
            self.button_Mag2PAL_far.config(bg=active_bg_clr, fg=active_fg_clr)
            self.button_Mag2PAL_near.config(bg=inactive_bg_clr, fg=inactive_fg_clr)

    def load_tray(self):
        if (self.state.all_axes_homed and not self.state.printing) or (
                self.state.all_axes_homed and self.state.printpause):
            cmd = RR_CommandGenerator.ttMoveAbs(axis="001", axis1_pos=self.state.param_tiles["load_tray_ax1_pos"])
            self.state.ttPort.write(cmd)
            unused_response = self.state.ttPort.readline()

    def tray_home(self):
        if (self.state.all_axes_homed and not self.state.printing) or (
                self.state.all_axes_homed and self.state.printpause):
            cmd = RR_CommandGenerator.ttMoveAbs(axis="001", axis1_pos=self.state.param_tiles["tray_home_ax1_pos"])
            self.state.ttPort.write(cmd)
            unused_response = self.state.ttPort.readline()
