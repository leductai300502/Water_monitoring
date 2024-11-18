import serial.tools.list_ports

on = 1
off = 0
numberRelay = 8

input0 = ["0106000000FF",    "010600000000",
         "0206000000FF",    "020600000000",
         "0306000000FF",    "030600000000",
         "0406000000FF",    "040600000000",
         "0506000000FF",    "050600000000",
         "0606000000FF",    "060600000000",
         "0706000000FF",    "070600000000",
         "0806000000FF",    "080600000000",
         "090600080000",    "090600000000",
         "0F06000000FF",    "0F0600000000",
         "0C0300050001",    "0C0600080009"]

relay_ON = [[1, 6, 0, 0, 0, 255, 201, 138],
[2, 6, 0, 0, 0, 255, 201, 185],
[3, 6, 0, 0, 0, 255, 200, 104],
[4, 6, 0, 0, 0, 255, 201, 223],
[5, 6, 0, 0, 0, 255, 200, 14],
[6, 6, 0, 0, 0, 255, 200, 61],
[7, 6, 0, 0, 0, 255, 201, 236],
[8, 6, 0, 0, 0, 255, 201, 19]]

relay_OFF = [[1, 6, 0, 0, 0, 0, 137, 202],
[2, 6, 0, 0, 0, 0, 137, 249],
[3, 6, 0, 0, 0, 0, 136, 40],
[4, 6, 0, 0, 0, 0, 137, 159],
[5, 6, 0, 0, 0, 0, 136, 78],
[6, 6, 0, 0, 0, 0, 136, 125],
[7, 6, 0, 0, 0, 0, 137, 172],
[8, 6, 0, 0, 0, 0, 137, 83]]

distance1_ON = [9, 3, 0, 5, 0, 1, 149, 67]
distance2_ON = [12, 3, 0, 5, 0, 1, 149, 22]

class RS485:
    # def __init__(self):
    #     self.serial
    #     return
    serial = None

    def __init__(self, port, baudrate):
        if port != "None":
            self.serial = serial.Serial(port, baudrate)
        else:
            print("Set serial faile!!!")

    def setSerial(self, port, baudrate):
        if port != "None":
            self.serial = serial.Serial(port, baudrate)
        else:
            print("Set serial faile!!!")

    def modbusCrc(self, msg:str) -> int:
        crc = 0xFFFF
        for n in range(len(msg)):
            crc ^= msg[n]
            for i in range(8):
                if crc & 1:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc
    
    def modbus(self, input):
        for turn in input:
            c2 = [int(turn[i:i + 2], 16) for i in range(0, len(turn), 2)]
            msg = bytes.fromhex(turn)
            crc = self.modbusCrc(msg)
            #print("0x%16X"%(crc))
            ba = crc.to_bytes(2, byteorder='little')
            c2.append(ba[0])
            c2.append(ba[1])
        return c2
    
    def getPort(self):
        ports = serial.tools.list_ports.comports()
        N = len(ports)
        commPort = "None"
        for i in range(0, N):
            port = ports[i]
            strPort = str(port)
            # print(strPort)
            if "/dev/ttyAMA2" in strPort:
                splitPort = strPort.split(" ")
                print("PortName:",strPort)
                commPort = splitPort[0]
        return commPort
    
    def serial_read_data(self):
        bytesToRead = self.serial.inWaiting()
        if bytesToRead > 0:
            out = self.serial.read(bytesToRead)
            data_array = [b for b in out]
            print(data_array)
            if len(data_array) >= 7:
                array_size = len(data_array)
                value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
                return value
            else:
                return -1
        return 0
    
    # def relayController(self):
    #     number = int(input("Enter relay number: "))
    #     state = int(input("Enter state: "))
    #     if state == 1:
    #         self.serial.write(relay_ON[number - 1])                                                                                                         
    #         print(self.serial_read_data(self.serial)) 
    #     else :
    #         self.serial.write(relay_OFF[number - 1])                                                                                                         
    #         print(self.serial_read_data(self.serial))
    
    def relayController(self, number, state):
        if number < numberRelay + 1:
            if state == 1:
                self.serial.write(relay_ON[number - 1])                                                                                                         
                print(self.serial_read_data()) 
            else :
                self.serial.write(relay_OFF[number - 1])                                                                                                         
                print(self.serial_read_data())
        else:
            print("Out of range of number Relay")
    
    def distanceController(self, number):
        if number == 9:
            self.serial.write(distance1_ON)                                                                                                         
            return (self.serial_read_data()) 
        elif number == 12:
            self.serial.write(distance2_ON)                                                                                                         
            return (self.serial_read_data())
        else:
            print("Wrong number distance sensor")