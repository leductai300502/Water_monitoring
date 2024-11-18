import serial.tools.list_ports
import time
import paho.mqtt.client as mqtt
import serial
from RS485_class import *

mqtt_broker_address = "mqtt_broker_address"
mqtt_topic = "sensor/data"


mqtt_client = mqtt.Client()
# def getPort():
#     ports = serial.tools.list_ports.comports()
#     N = len(ports)
#     commPort = "None"
#     for i in range(0, N):
#         port = ports[i]
#         strPort = str(port)
#         print(strPort) # print(strPort)
#         if "FT232R USB UART" in strPort:
#             splitPort = strPort.split(" ")
#             print("PortName:",strPort)
#             commPort = splitPort[0]
#     return commPort

SENSOR_9 = [9, 3, 0, 0, 0, 255, 4, 194]
# relay1_OFF = [1,6,0,0,0,0,137,202]

# portName = getPort()
# print("portName:",portName)
# if portName != "None":
#     ser = serial.Serial(port=portName, baudrate=9600)
# port ="/dev/ttyAMA2"
# baudrate = 9600
# print("Find port {} - baudate {}".format(port,baudrate))
# ser = serial.Serial(port,baudrate)
# print(ser)
# def serial_read_data(ser):
#     bytesToRead = ser.inWaiting()
#     if bytesToRead > 0:
#         out = ser.read(bytesToRead)
#         data_array = [b for b in out]
#         print(data_array)
#         if len(data_array) >= 7:
#             array_size = len(data_array)
#             value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
#             return value
#         else:
#             return -1
#     return 0
while True:
    start_time = time.time()  # Thời điểm bắt đầu lấy dữ liệu

    # Đọc dữ liệu từ cảm biến thông qua giao tiếp RS485
    RS485.send(SENSOR_9)  # Gửi yêu cầu đọc dữ liệu qua RS485
    sensor_data = RS485.read_data(RS485.serial)  # Đọc dữ liệu từ RS485

    # Gửi dữ liệu lên MQTT broker
    mqtt_client.publish(mqtt_topic, sensor_data)
    print(sensor_data)
    elapsed_time = time.time() - start_time  # Thời gian đã trôi qua để lấy và gửi dữ liệu
    remaining_time = max(0, 30 - elapsed_time)  # Thời gian còn lại cho đến khi cập nhật tiếp theo (30 giây)

    # RS485.send(relay1_ON)
    # print(RS485.read_data(RS485.serial))
    # RS485.send(relay1_OFF)
    # print(RS485.read_data(RS485.serial))

    time.sleep(remaining_time)  # Chờ thời gian còn lại trước khi cập nhật dữ liệu tiếp theo
    