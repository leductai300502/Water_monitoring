import time
import serial.tools.list_ports

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        print(strPort) # print(strPort)
        if "/dev/ttyAMA2" in strPort:
            splitPort = strPort.split(" ")
            print("PortName:",strPort)
            commPort = splitPort[0]
    return commPort

def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0

def setDevice1(state):
    serial_read_data(ser)
    #print(ser)
    if state == True:
        ser.write(relay1_ON)
        # client.publish(AIO_FEED_ID[2],1)
    else:
        ser.write(relay1_OFF)
        # client.publish(AIO_FEED_ID[2],0)

portName = getPort()
print("portName:",portName)
if portName != "None":
    ser = serial.Serial(port=portName, baudrate=9600)

relay1_ON = [1, 6, 0, 0, 0, 255, 201, 138]
relay1_OFF = [1, 6, 0, 0, 0, 0, 137, 202]

# relay6_ON = [1, 6, 0, 0, 0, 255, 201, 138]
# relay6_OFF = [1, 6, 0, 0, 0, 0, 137, 202]

distance1_ON = [9, 3, 0, 5, 0, 1, 149, 67]
distance2_ON = [12, 3, 0, 5, 0, 1, 149, 22]
# distance2_OFF = [12, 6, 0, 8, 0, 9, 201, 19]

distance1_passive = [9, 8, 0, 20, 0, 1, 96, 135]

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

def relayController():
    number = int(input("Enter relay number: "))
    state = int(input("Enter state: "))
    if state == 1:
        ser.write(relay_ON[number - 1])                                                                                                         
        print(serial_read_data(ser)) 
    else :
        ser.write(relay_OFF[number - 1])                                                                                                         
        print(serial_read_data(ser)) 

while True:
    # relayController()
    # time.sleep(2)

    # ser.write(distance1_passive) 
    ser.write(distance1_ON) 
    time.sleep(2)  

    print(serial_read_data(ser))                                                                                                

    # ser.write(distance2_ON)                                                                                                         
    # print(serial_read_data(ser))                                                                                                
    # time.sleep(2)