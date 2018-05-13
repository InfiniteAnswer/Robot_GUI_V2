while True:
    cmd = input("Enter command or 'exit':")
    if cmd == 'exit':
        exit()
    else:
        # cmd += '\r\n'
        print(cmd)
        message = cmd.encode('ascii')
        print(message)
        messageSum = 0

        for letter in cmd:
            print(letter, ':', ord(letter), ' = ', hex(ord(letter)))
            messageSum += ord(letter)

        print('sum in decimal: ', messageSum)
        print('sum in hex: ', hex(messageSum))
        print()