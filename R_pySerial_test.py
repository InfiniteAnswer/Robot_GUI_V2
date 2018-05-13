import serial

port = "COM3"
baud = 9600

ser = serial.Serial(port, baud, timeout=1)

if ser.isOpen():
    print(ser.name + ' is open...')

while True:
    cmd = input("Enter command or 'exit':")
    if cmd == 'exit':
        ser.close()
        exit()
    else:
        cmd += '\r\n'
        print(cmd)
        message = cmd.encode('ascii')
        ser.write(message)
        out = ser.readline()

        print(message)
        print('Receiving...')
        print(out)