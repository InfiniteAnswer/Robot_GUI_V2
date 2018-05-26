import RR_CommandGenerator
import serial  # used for serial communications. came from <pip3.6 install pyserial>
import time


class RuntimeState():
    def __init__(self):
        self.homeax1 = False
        self.homeax2 = False
        self.homeax3 = False
        self.homeax4 = False
        self.printing = False
        self.printSpeed = 10    # This is the percentage of maxTTmovingSpeed
        self.maxTTmovingSpeed = 150
        self.abort = False
        self.magazineinitialised = False
        self.paletteinitialised = False
        self.fileloaded = False
        self.printpause = False
        self.axismoving = False
        self.process_log = ""
        self.last_commanded_ax1 = 0
        self.last_commanded_ax2 = 0
        self.last_commanded_ax3 = 0
        self.last_commanded_ax4 = 1

        self.POLLING_DELAY = 0.1  # time in SECONDS between repeated requests to see if a robot is moving
        self.mosaic_number = 0
        self.LOG_file_save_location = "C:/Users/Finlay/Documents/iai_log_files/"

        self.param_robo = {"tt_port": "COM4",
                           "pal_port": "COM3",
                           "cntrl_port": "COM5",
                           "tt_baud": 9600,
                           "pal_baud": 38400,
                           "cntrl_baud": 38400,
                           "tt_timeout": 1,
                           "pal_timeout": 1,
                           "cntrl_timeout": 1,
                           "gripper_open_wait": 0.25,
                           "gripper_close_wait": 0.4,
                           "gripper_up": 25,
                           "gripper_down_palette": 40.25,
                           "gripper_down_table": 73.5,
                           "gripper_safety_height": 10,
                           "moving_timeout": 90}

        self.param_tiles = {"tile_width": 20,
                            "tile_height": 20,
                            "inter_tile_hgap": 3,
                            "inter_tile_vgap": 3,
                            "palette_pitch": 30.48,
                            "tt_origin_x": 15,
                            "tt_origin_y": 15,
                            "pal_origin_x": 44.5}

        self.pal_message = {"palHome": ":01060D001010CC\r\n",
                            "palSet_position_1": ":01060D030001E8\r\n",
                            "palSet_position_2": ":01060D030002E7\r\n",
                            "palCSTR_off": ":01060D001000DC\r\n",
                            "palCSTR_on": ":01060D001008D4\r\n",
                            "palQuery_moving": ":01039007000164\r\n",
                            "palQuery_home": ":01039005000166\r\n",
                            "enableModbus": ":01050427FF00D0\r\n"}

        self.ttPort = serial.Serial(port=self.param_robo["tt_port"],
                                    baudrate=self.param_robo["tt_baud"],
                                    timeout=self.param_robo["tt_timeout"])
        self.palPort = serial.Serial(port=self.param_robo["pal_port"],
                                     baudrate=self.param_robo["pal_baud"],
                                     timeout=self.param_robo["pal_timeout"])
        self.cntrlPort = serial.Serial(port=self.param_robo["cntrl_port"],
                                       baudrate=self.param_robo["cntrl_baud"],
                                       timeout=self.param_robo["cntrl_timeout"])

        # enable Modbus communications
        cmd = self.pal_message["enableModbus"].encode("ascii")
        self.palPort.write(cmd)
        response_pal = self.palPort.readline()

        # NOT YET DONE... connect to two robots and check connections with a test command

        # enable tt robot servos
        self.process_log += self.timestamped_msg("enabling servo for axis 1\n")
        print(self.process_log.split("\n")[-2])
        self.ttPort.write(RR_CommandGenerator.ttServo(axis="001", on=1))
        unused_response = self.ttPort.readline()
        self.process_log += self.timestamped_msg("enabling servo for axis 2\n")
        print(self.process_log.split("\n")[-2])
        self.ttPort.write(RR_CommandGenerator.ttServo(axis="010", on=1))
        unused_response = self.ttPort.readline()
        self.process_log += self.timestamped_msg("enabling servo for axis 3\n")
        print(self.process_log.split("\n")[-2])
        self.ttPort.write(RR_CommandGenerator.ttServo(axis="100", on=1))
        unused_response = self.ttPort.readline()
        time.sleep(1)   # DELAY of 1 SECOND to ensure the servos are active before proceeding




    def tt_moving_query(self):
        # ask tt if moving and save response
        cmd = RR_CommandGenerator.ttMovingQuery(axis="001")
        self.ttPort.write(cmd)
        response_tt_1 = self.ttPort.readline()
        cmd = RR_CommandGenerator.ttMovingQuery(axis="010")
        self.ttPort.write(cmd)
        response_tt_2 = self.ttPort.readline()
        cmd = RR_CommandGenerator.ttMovingQuery(axis="100")
        self.ttPort.write(cmd)
        response_tt_3 = self.ttPort.readline()

        # perform logical tests on 3 responses and generate 3 true/false answers
        response_tt_1 = '0x' + str(response_tt_1)[10:12]
        response_tt_2 = '0x' + str(response_tt_2)[10:12]
        response_tt_3 = '0x' + str(response_tt_3)[10:12]
        tt_1 = (eval(response_tt_1) & 0b1) == 1
        tt_2 = (eval(response_tt_2) & 0b1) == 1
        tt_3 = (eval(response_tt_3) & 0b1) == 1
        tt = tt_1 or tt_2 or tt_3
        return (tt)


    def pal_moving_query(self):
        # ask pal if moving and save response
        cmd = self.pal_message["palQuery_moving"].encode("ascii")
        self.palPort.write(cmd)
        response_pal = self.palPort.readline()

        # perform logical test on response and generate true/false answers
        response_pal = '0x' + str(response_pal)[11:12]
        pal = (eval(response_pal) & 0b10) == 2
        return (pal)

    def printpause_sequence(self):
        # send stop command x
        # send stop cammand y
        # send stop command z

        # send stop command xyz
        cmd = RR_CommandGenerator.ttStop(axis="111")
        self.ttPort.write(cmd)
        response_tt_1 = self.ttPort.readline()
        self.process_log += self.timestamped_msg("tt robot motion stopped\n")
        print(self.process_log.split("\n")[-2] + "\n")

        # raise z to safety height
        time.sleep(1)
        self.ttPort.write(
            RR_CommandGenerator.ttMoveAbs(axis="100", axis3_pos=self.param_robo["gripper_safety_height"]))
        unused_response = self.ttPort.readline()
        self.process_log += self.timestamped_msg("gripper up to safety height\n")
        print(self.process_log.split("\n")[-2] + "\n")

        # safety delay of 3s
        time.sleep(3)

        while self.printpause:
            time.sleep(self.POLLING_DELAY)

        # goto last x position
        self.ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="001", axis1_pos=self.last_commanded_ax1))
        unused_response = self.ttPort.readline()
        self.process_log += self.timestamped_msg("returning ax1-table to last commanded position\n")
        print(self.process_log.split("\n")[-2])

        # goto last y position
        self.ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="010", axis2_pos=self.last_commanded_ax2))
        unused_response = self.ttPort.readline()
        self.process_log += self.timestamped_msg("returning ax2-bridge to last commanded position\n")
        print(self.process_log.split("\n")[-2])

        # goto last z position
        self.ttPort.write(RR_CommandGenerator.ttMoveAbs(axis="100", axis3_pos=self.last_commanded_ax3))
        unused_response = self.ttPort.readline()
        self.process_log += self.timestamped_msg("returning ax3-gripper to last commanded position\n")
        print(self.process_log.split("\n")[-2])


    def tt_moving(self):
        global process_log
        timeout = time.time() + self.param_robo["moving_timeout"]
        while (self.tt_moving_query()):
            if self.printpause:
                self.printpause_sequence()
            if time.time() > timeout:
                process_log += "WARNING! TT timed out. Unable to reach set-point after " + \
                               str(self.param_robo["moving_timeout"]) + " seconds\n"
                print(process_log.split("\n")[-2])
                break
            time.sleep(self.POLLING_DELAY)

    def pal_moving(self):
        global process_log
        timeout = time.time() + self.param_robo["moving_timeout"]
        while (self.pal_moving_query()):
            if self.printpause:
                self.printpause_sequence()
            if time.time() > timeout:
                process_log += "WARNING! PAL timed out. Unable to reach set-point after " + \
                               str(self.param_robo["moving_timeout"]) + " seconds\n"
                print(process_log.split("\n")[-2])
                break
            time.sleep(self.POLLING_DELAY)

    def tt_pal_moving(self):
        global process_log
        timeout = time.time() + self.param_robo["moving_timeout"]
        while (self.tt_moving_query() or self.pal_moving_query()):
            if self.printpause:
                self.printpause_sequence()
            if time.time() > timeout:
                process_log += "WARNING! TT or PAL timed out. Unable to reach set-point after " + \
                               str(self.param_robo["moving_timeout"]) + " seconds\n"
                print(process_log.split("\n")[-2])
                break
            time.sleep(self.POLLING_DELAY)

    def pixel2table(self, x_n, y_n):
        table_x = self.param_tiles["tt_origin_x"] + x_n * (self.param_tiles["tile_width"] + self.param_tiles["inter_tile_hgap"])
        table_y = self.param_tiles["tt_origin_y"] + y_n * (self.param_tiles["tile_height"] + self.param_tiles["inter_tile_vgap"])
        return (table_x, table_y)

    def colour2palette(self, c_n):
        palette_x = self.param_tiles["pal_origin_x"] + c_n * (self.param_tiles["palette_pitch"])
        return palette_x

    def timestamped_msg(self, msg):
        string = str(time.asctime(time.localtime(time.time()))) + ": " + msg
        return (string)

