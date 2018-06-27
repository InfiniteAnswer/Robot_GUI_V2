from threading import Thread, Lock
from time import sleep, ctime, asctime

echo_queries = False


class Serial:
    def __init__(self, port="PortName", baudrate=9600, timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.target = "none"  # Options are "tt", "pal", or "controller"

        # Create dictionaries of valid commands and the time (seconds) they take to execute
        self.tt_commands = {"233": 0.25,  # ttHome
                            "234": 0.25,  # ttMoveAbs
                            "232": 0.25,  # ttServo
                            "212": 0.1,  # ttMoving Query
                            "238": 0.1}  # ttStop

        self.pal_commands = {":01060D001010CC": 0.25,  # palHome
                             ":01060D030001E8": 0.25,  # palSet_position_1
                             ":01060D030002E7": 0.25,  # palSet_position_2
                             ":01060D001000DC": 0.1,  # palCSTR_off
                             ":01060D001008D4": 0.1,  # palCSTR_on
                             ":01039007000164": 0.1,  # palQuery_moving
                             ":01039005000166": 0.1,  # palQuery_home
                             ":01050427FF00D0": 0.1}  # enableModbus

        self.command_buffer = list()
        self.process_time = list()
        self.returned_message = list()
        self.axis_busy_state = list()
        self.ready_for_next_command = list()
        self.thread_list = list()

        if port == "COM3":
            self.target = "pal"
            self.pal_home = False
            self.command_buffer.append(list())
            self.axis_busy_state.append(False)
            self.ready_for_next_command.append(True)
            self.process_time.append(0)
            th = Thread(target=self.axis_server, args=(0,))
            th.daemon = True
            self.thread_list.append(th)
            self.thread_list[0].start()

        if port == "COM4":
            self.target = "tt"
            self.tt_home = [False, False, False]
            for i in range(3):
                self.command_buffer.append(list())
                self.axis_busy_state.append(False)
                self.ready_for_next_command.append(True)
                self.process_time.append(0)
                th = Thread(target=self.axis_server, args=(i,))
                th.daemon = True
                self.thread_list.append(th)
                self.thread_list[i].start()

        if port == "COM5":
            self.target = "controller"

    def write(self, msg):
        axis = 0
        msg = str(msg)[2:-1]
        if self.target == "tt":
            # Extract command from serial message
            msg_command = msg[3:6]
            # If command is valid AND not a query, add to command buffer
            if msg_command in self.tt_commands:
                # Determine relevant axis in message
                if msg[7] == "1":
                    axis = 0
                if msg[7] == "2":
                    axis = 1
                if msg[7] == "4":
                    axis = 2
                # If command is not a query, add command and command duration to command_buffer
                if msg_command != "212":
                    self.command_buffer[axis].append((msg_command,
                                                      list(self.tt_commands.values())[
                                                          list(self.tt_commands.keys()).index(msg_command)]))
                    self.returned_message.append(msg_command)
                    print("Message sent: {} at time: {}".format(msg, ctime()))
                    if msg_command == "233":
                        self.tt_home[axis] = True
                # If command is a query for busy state, add busy state to returned message
                else:
                    self.returned_message.append(msg_command)
                    self.returned_message.append(self.axis_busy_state[axis])
                    self.returned_message.append(self.tt_home[axis])
            else:
                append_msg = "invalid pal command: " + msg
                self.returned_message.append(append_msg)

        if self.target == "pal":
            print("processing PAL command")
            msg_command = msg[0:15]
            if msg_command in self.pal_commands:
                # If command is valid AND not a query, add to command buffer
                if msg_command != ":01039007000164" and msg_command != ":01039005000166":
                    self.command_buffer[0].append((msg_command,
                                                   list(self.pal_commands.values())[
                                                       list(self.pal_commands.keys()).index(msg_command)]))
                    self.returned_message.append(msg_command)
                    print("Message sent: {} at time: {}".format(msg, ctime()))
                    if msg_command == ":01060D001010CC":
                        self.pal_home = True
                # If command is a query for busy state, add busy state to returned message
                else:
                    self.returned_message.append(msg_command)
                    self.returned_message.append(self.axis_busy_state[0])
                    self.returned_message.append(self.pal_home)
            else:
                append_msg = "invalid pal command: " + msg
                self.returned_message.append(append_msg)

    def readline(self):
        msg = self.returned_message[0]

        # If command is a query for tt axis moving...
        if msg == "212":
            moving_state = 0b1 if self.returned_message[1] else 0b0
            home_state = 0b100 if self.returned_message[2] else 0b0
            if echo_queries:
                print("Echo message: ", self.returned_message)
            msg = "xxxxxxxxxx0" + str(moving_state + home_state)
            del self.returned_message[0:3]

        # If command is a query for pal axis moving...
        elif msg == ":01039007000164":
            moving_state = 0b10 if self.returned_message[1] else 0b0
            home_state = 0b1 if self.returned_message[2] else 0b0
            if echo_queries:
                print("Echo message: ", self.returned_message)
            msg = "xxxxxxxxxxx" + str(moving_state + home_state)
            del self.returned_message[0:3]

        elif msg == ":01039005000166":
            moving_state = 0b10 if self.returned_message[1] else 0b0
            home_state = 0b1 if self.returned_message[2] else 0b0
            if echo_queries:
                print("Echo message: ", self.returned_message)
            msg = "xxxxxxxxxxx" + str(moving_state + home_state)
            del self.returned_message[0:3]

        else:
            print("Echo message: ", msg)
            del self.returned_message[0:1]
        return msg

    def axis_server(self, axis=0):
        while True:
            # Check if command exists in buffer and axis is ready to execute next command
            if self.command_buffer[axis] and self.ready_for_next_command[axis]:
                print("\nStarting command {} for {} axis {} at  {}\n".format(self.command_buffer[axis][0],
                                                                             self.target,
                                                                             axis,
                                                                             ctime()))
                self.axis_busy_state[axis] = True
                self.ready_for_next_command[axis] = False
                self.process_time[axis] = self.command_buffer[axis][0][1]
                sleep(self.process_time[axis])
                print("\nCompleted command {} for {} axis {} at  {}\n".format(self.command_buffer[axis][0],
                                                                              self.target,
                                                                              axis,
                                                                              ctime()))
                del self.command_buffer[axis][0]
                self.ready_for_next_command[axis] = True
                if not self.command_buffer[axis]:
                    self.axis_busy_state[axis] = False
            else:
                # to avoid axis_server running so fast it consumes all resources...
                sleep(0.1)
