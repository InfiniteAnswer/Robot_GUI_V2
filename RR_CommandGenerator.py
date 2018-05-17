def calcchecksum(message):
    messageSum = 0
    for letter in message:
        messageSum += ord(letter)
    messageSum_hex = hex(messageSum)
    checksum = messageSum_hex[-2:].upper()
    return (checksum)


def ttHome(station="99",
           axis="100",
           search_speed=3,
           creep_speed=3):
    axis_bytes = format(eval("0b" + axis), '02x').upper()
    search_bytes = format(search_speed, '03x').upper()
    creep_bytes = format(creep_speed, '03x').upper()
    message = "!" + station + "233" + axis_bytes + search_bytes + creep_bytes
    checksum = calcchecksum(message)
    message += checksum + '\r\n'
    return (message.encode('ascii'))


def ttMoveAbs(station="99",
              axis="111",
              accel=0.05,
              decel=0.05,
              speed=125,
              axis1_pos=0,
              axis2_pos=0,
              axis3_pos=0):
    accel_units = 0.01  # acceleration is given in units of 0.01G
    speed_units = 1  # speed is given in units of mm/s
    position_units = 0.001  # position is given in units of microns
    axis_bytes = format(eval("0b" + axis), '02x').upper()
    accel_bytes = format(int(accel / accel_units), '04x').upper()
    decel_bytes = format(int(decel / accel_units), '04x').upper()
    speed_bytes = format(int(speed / speed_units), '04x').upper()
    axis1_pos_bytes = format(int(axis1_pos / position_units), '08x').upper()
    axis2_pos_bytes = format(int(axis2_pos / position_units), '08x').upper()
    axis3_pos_bytes = format(int(axis3_pos / position_units), '08x').upper()

    if axis == "001":
        message = "!" + station + "234" + axis_bytes + accel_bytes + decel_bytes + speed_bytes + axis1_pos_bytes
    if axis == "010":
        message = "!" + station + "234" + axis_bytes + accel_bytes + decel_bytes + speed_bytes + axis2_pos_bytes
    if axis == "011":
        message = "!" + station + "234" + axis_bytes + accel_bytes + decel_bytes + speed_bytes + axis1_pos_bytes + axis2_pos_bytes
    if axis == "100":
        message = "!" + station + "234" + axis_bytes + accel_bytes + decel_bytes + speed_bytes + axis3_pos_bytes
    if axis == "101":
        message = "!" + station + "234" + axis_bytes + accel_bytes + decel_bytes + speed_bytes + axis1_pos_bytes + axis3_pos_bytes
    if axis == "110":
        message = "!" + station + "234" + axis_bytes + accel_bytes + decel_bytes + speed_bytes + axis2_pos_bytes + axis3_pos_bytes
    if axis == "111":
        message = "!" + station + "234" + axis_bytes + accel_bytes + decel_bytes + speed_bytes + axis1_pos_bytes + axis2_pos_bytes + axis3_pos_bytes

    checksum = calcchecksum(message)
    message += checksum + '\r\n'
    return (message.encode('ascii'))


def ttServo(station="99",
            axis="111",
            on=0):
    axis_bytes = format(eval("0b" + axis), '02x').upper()
    on_bytes = str(on)
    message = "!" + station + "232" + axis_bytes + on_bytes
    checksum = calcchecksum(message)
    message += checksum + '\r\n'
    return (message.encode('ascii'))


def ttMovingQuery(station="99",
                  axis="001"):
    axis_bytes = format(eval("0b" + axis), '02x').upper()
    message = "!" + station + "212" + axis_bytes
    checksum = calcchecksum(message)
    message += checksum + '\r\n'
    return (message.encode('ascii'))


def ttOutputPortSet(station="99",
                    port="013C",
                    on="0"):
    message = "!" + station + "24A" + port + on
    checksum = calcchecksum(message)
    message += checksum + '\r\n'
    return (message.encode('ascii'))

# ttHome(axis = '001')
# ttHome(axis = '010')
# ttHome(axis="100")
# ttHome(axis="111")
#
# ttMoveAbs(axis='011', accel=0.1, decel=0.1, speed=10,  axis1_pos = 50, axis2_pos = 50)
# ttMoveAbs(axis='011', accel=0.1, decel=0.1, speed=10,  axis1_pos = 55, axis2_pos = 55)
# ttMoveAbs(axis='011', accel=0.1, decel=0.1, speed=10,  axis1_pos = 75, axis2_pos = 75)
#
# ttServo(axis="111",on=0)
# ttServo(axis='111', on=1)
#
# ttMovingQuery()
# ttOutputPortSet(on=0)
# ttOutputPortSet(on=1)
