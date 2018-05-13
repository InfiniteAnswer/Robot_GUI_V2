#setup
import time
polling_delay = 0.1
time_out_constant = 20

#open serial port
import serial
port = "COM3"
portPal = "COM7"
baud = 9600
baudPal = 9600

ser = serial.Serial(port, baud, timeout=1)
serPal = serial.Serial(portPal, baudPal, timeout=1)

#check ports are open
if ser.isOpen():
    print(ser.name + ' is open...')
if serPal.isOpen():
    print(serPal.name + ' is open...')

#send command to move ttRobot to 50,50
cmd = "!9923403000A000A000A0000C3500000C35000000000B8\r\n"
print(cmd)
message = cmd.encode('ascii')
ser.write(message)
out = ser.readline()
print('Receiving...')
print(out)

#send command to move Pallette robot to position 1
cmd = ":01060D030001E8\r\n"
print(cmd)
message = cmd.encode('ascii')
serPal.write(message)
outPal = serPal.readline()
print('Receiving...')
print(outPal)

cmd = ":01060D001000DC\r\n"
print(cmd)
message = cmd.encode('ascii')
serPal.write(message)
outPal = serPal.readline()
print('Receiving...')
print(outPal)

cmd = ":01060D001008D4\r\n"
print(cmd)
message = cmd.encode('ascii')
serPal.write(message)
outPal = serPal.readline()
print('Receiving...')
print(outPal)

#check if moving and wait until stopped
#check ttRobot
cmd = "!992120189\r\n"
print(cmd)
message = cmd.encode('ascii')
ser.write(message)
out = ser.readline()
print('Receiving...')
print(out)

#check Pallette robot
cmd = ":01039007000164\r\n"
print(cmd)
message = cmd.encode('ascii')
serPal.write(message)
outPal = serPal.readline()
print('Receiving...')
print(outPal)

response = '0x' + str(out)[10:12]
responsePal = '0x' + str(outPal)[11:12]
print(out, ', ', outPal)

timeout = time.time() + time_out_constant
print(' Moving...')
while ((eval(response) & 0b1) == 1) or ((eval(responsePal) & 0b10) == 2):
    #check ttRobot
    cmd = "!992120189\r\n"
    message = cmd.encode('ascii')
    ser.write(message)
    out = ser.readline()
    response = '0x' + str(out)[10:12]

    #check pallette robot
    cmd = ":01039007000164\r\n"
    message = cmd.encode('ascii')
    serPal.write(message)
    outPal = serPal.readline()
    responsePal = '0x' + str(outPal)[11:12]

    if time.time() > timeout:
        print('timed out')
        break
    time.sleep(polling_delay)
    print('repolling: ', ((eval(response) & 0b1) == 1), ', ', ((eval(responsePal) & 0b10) == 2))

print('Movement complete')

time.sleep(1)

#open gripper and wait 8 secs
#port 316 off
cmd = "!9924A013C041\r\n"
print(cmd)
message = cmd.encode('ascii')
ser.write(message)
out = ser.readline()
print('Receiving...')
print(out)

time.sleep(0.2)

print('OPENING GRIPPER')
#port 316 on
cmd = "!9924A013C142\r\n"
print(cmd)
message = cmd.encode('ascii')
ser.write(message)
out = ser.readline()
print('Receiving...')
print(out)

time.sleep(8)

print('CLOSING GRIPPER')
#port 316 off
cmd = "!9924A013C041\r\n"
print(cmd)
message = cmd.encode('ascii')
ser.write(message)
out = ser.readline()
print('Receiving...')
print(out)

time.sleep(1)

#send command to move to 75, 75
#cmd = "!9923403000A000A000A000124F8000124F800000000CC\r\n"

#send command to move to 55,55
cmd = "!9923403000A000A000A0000D6D80000D6D800000000EE\r\n"
print(cmd)
message = cmd.encode('ascii')
ser.write(message)
out = ser.readline()
print('Receiving...')
print(out)


#send command to move Pallette robot to position 2
cmd = ":01060D030002E7\r\n"
print(cmd)
message = cmd.encode('ascii')
serPal.write(message)
outPal = serPal.readline()
print('Receiving...')
print(outPal)


cmd = ":01060D001000DC\r\n"
print(cmd)
message = cmd.encode('ascii')
serPal.write(message)
outPal = serPal.readline()
print('Receiving...')
print(outPal)

cmd = ":01060D001008D4\r\n"
print(cmd)
message = cmd.encode('ascii')
serPal.write(message)
outPal = serPal.readline()
print('Receiving...')
print(outPal)


#check if moving and wait until stopped
#check ttRobot
cmd = "!992120189\r\n"
print(cmd)
message = cmd.encode('ascii')
ser.write(message)
out = ser.readline()
print('Receiving...')
print(out)

#check Pallette robot
cmd = ":01039007000164\r\n"
print(cmd)
message = cmd.encode('ascii')
serPal.write(message)
outPal = serPal.readline()
print('Receiving...')
print(outPal)

response = '0x' + str(out)[10:12]
responsePal = '0x' + str(outPal)[11:12]

timeout = time.time() + time_out_constant
print(' Moving...')
while ((eval(response) & 0b1) == 1) or ((eval(responsePal) & 0b10) == 2):
    #check ttRobot
    cmd = "!992120189\r\n"
    message = cmd.encode('ascii')
    ser.write(message)
    out = ser.readline()
    response = '0x' + str(out)[10:12]

    #check pallette robot
    cmd = ":01039007000164\r\n"
    message = cmd.encode('ascii')
    serPal.write(message)
    outPal = serPal.readline()
    responsePal = '0x' + str(outPal)[11:12]

    if time.time() > timeout:
        print('timed out')
        break
    time.sleep(0.1)

print('Movement complete')

print('Movement complete')


#reset pallette robot for next move
cmd = ":01060D001000DC\r\n"
print(cmd)
message = cmd.encode('ascii')
serPal.write(message)
outPal = serPal.readline()
print('Receiving...')
print(outPal)

#close serial port
ser.close()
serPal.close()
exit()
