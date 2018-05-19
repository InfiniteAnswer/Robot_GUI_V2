import RR_CommandGenerator
import serial  # used for serial communications. came from <pip3.6 install pyserial>


class RuntimeState():
    def __init__(self):
        self.homeax1 = False
        self.homeax2 = False
        self.homeax3 = False
        self.homeax4 = False
        self.printing = False
        self.abort = False
        self.magazineinitialised = False
        self.paletteinitialised = False
        self.fileloaded = False
        self.printpause = False
        self.axismoving = False
        self.process_log = ""

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
                           "gripper_up": 30,
                           "gripper_down_palette": 39.75,
                           "gripper_down_table": 73.5,
                           "moving_timeout": 90}

        self.param_tiles = {"tile_width": 20,
                            "tile_height": 20,
                            "inter_tile_hgap": 3,
                            "inter_tile_vgap": 3,
                            "palette_pitch": 30.48,
                            "tt_origin_x": 15,
                            "tt_origin_y": 15,
                            "pal_origin_x": 45.5}

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

    def pal_moving_query(palPort):
        # ask pal if moving and save response
        cmd = pal_message["palQuery_moving"].encode("ascii")
        palPort.write(cmd)
        response_pal = palPort.readline()

        # perform logical test on response and generate true/false answers
        response_pal = '0x' + str(response_pal)[11:12]
        pal = (eval(response_pal) & 0b10) == 2
        return (pal)

    def tt_moving(ttPort):
        global process_log
        timeout = time.time() + param_robo["moving_timeout"]
        while (tt_moving_query(ttPort)):
            if time.time() > timeout:
                process_log += "WARNING! TT timed out. Unable to reach set-point after " + \
                               str(param_robo["moving_timeout"]) + " seconds\n"
                print(process_log.split("\n")[-2])
                break
            time.sleep(POLLING_DELAY)

    def pal_moving_query(palPort):
        # ask pal if moving and save response
        cmd = pal_message["palQuery_moving"].encode("ascii")
        palPort.write(cmd)
        response_pal = palPort.readline()

        # perform logical test on response and generate true/false answers
        response_pal = '0x' + str(response_pal)[11:12]
        pal = (eval(response_pal) & 0b10) == 2
        return (pal)

    def tt_moving(ttPort):
        global process_log
        timeout = time.time() + param_robo["moving_timeout"]
        while (tt_moving_query(ttPort)):
            if time.time() > timeout:
                process_log += "WARNING! TT timed out. Unable to reach set-point after " + \
                               str(param_robo["moving_timeout"]) + " seconds\n"
                print(process_log.split("\n")[-2])
                break
            time.sleep(POLLING_DELAY)

    def pal_moving(palPort):
        global process_log
        timeout = time.time() + param_robo["moving_timeout"]
        while (pal_moving_query(palPort)):
            if time.time() > timeout:
                process_log += "WARNING! PAL timed out. Unable to reach set-point after " + \
                               str(param_robo["moving_timeout"]) + " seconds\n"
                print(process_log.split("\n")[-2])
                break
            time.sleep(POLLING_DELAY)

    def tt_pal_moving(ttPort, palPort):
        global process_log
        timeout = time.time() + param_robo["moving_timeout"]
        while (tt_moving_query(ttPort) or pal_moving_query(palPort)):
            if time.time() > timeout:
                process_log += "WARNING! TT or PAL timed out. Unable to reach set-point after " + \
                               str(param_robo["moving_timeout"]) + " seconds\n"
                print(process_log.split("\n")[-2])
                break
            time.sleep(POLLING_DELAY)

    def pixel2table(x_n, y_n):
        table_x = param_tiles["tt_origin_x"] + x_n * (param_tiles["tile_width"] + param_tiles["inter_tile_hgap"])
        table_y = param_tiles["tt_origin_y"] + y_n * (param_tiles["tile_height"] + param_tiles["inter_tile_vgap"])
        return (table_x, table_y)

    def colour2palette(c_n):
        palette_x = param_tiles["pal_origin_x"] + c_n * (param_tiles["palette_pitch"])
        return palette_x

    def timestamped_msg(msg):
        string = str(time.asctime(time.localtime(time.time()))) + ": " + msg
        return (string)

