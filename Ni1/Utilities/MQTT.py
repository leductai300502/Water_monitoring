import paho.mqtt.client as mqtt
import serial

class RS485:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.serial = serial.Serial(port, baudrate, timeout=timeout)

    def send(self, data):
        self.serial.write(data)

    def receive(self, num_bytes):
        return self.serial.read(num_bytes)

    def close(self):
        self.serial.close()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe("rs485/commands")

def on_message(client, userdata, msg):
    print("Received message: " + msg.payload.decode())

    # Gửi dữ liệu đến RS485
    rs485.send(msg.payload)

    # Nhận dữ liệu từ RS485 và gửi lại lên MQTT
    data = rs485.receive(1024)
    client.publish("rs485/data", data)

mqtt_client = mqtt.Client()

# Thiết lập các hàm callback cho sự kiện kết nối và nhận tin nhắn MQTT
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Kết nối đến MQTT broker
mqtt_client.connect("mqtt_broker_address", 1883, 60)

# Khởi tạo đối tượng RS485
rs485 = RS485("/dev/ttyUSB0", baudrate=9600, timeout=1)

# Vòng lặp chính để duy trì kết nối MQTT và thực hiện việc nhận và gửi dữ liệu RS485
mqtt_client.loop_forever()