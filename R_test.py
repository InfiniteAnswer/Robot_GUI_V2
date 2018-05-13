#setup
import time
import serial

pallette_wait_delay = 0.1

#open serial port
import serial
port = "COM3"
portPal = "COM6"
baud = 9600
baudPal = 9600

ser = serial.Serial(port, baud, timeout=1)
serPal = serial.Serial(portPal, baudPal, timeout=1)

#check ports are open
if ser.isOpen():
    print(ser.name + ' is open...')
if serPal.isOpen():
    print(serPal.name + ' is open...')

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


#close serial port
ser.close()
serPal.close()
exit()