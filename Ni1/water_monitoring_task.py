import enum
from PrivateTasks.rapido_server_task import *


class WMR_Status(enum.Enum):
    INIT = 1
    PUMP_ON = 2
    PUMP_OFF = 3
    STABLE = 7
    READ_PH = 4
    READ_TSS = 5
    READ_NH3 = 6
    READ_TEMP = 12
    READ_DHT_TEMP = 10
    READ_DHT_HUMI = 11
    IDLE = 8


class WaterMonitoringTask:
    PUMP_ON_DELAY = 3000
    PUMP_OFF_DELAY = 5000
    STABLE_DELAY = 20000
    SENSING_DELAY = 500
    IDLE_DELAY = 10000
    relay2_ON = [15, 6, 0, 0, 0, 255, 200, 164]
    relay2_OFF = [15, 6, 0, 0, 0, 0, 136, 228]

    PH_CMD = [0x02, 0x03, 0x00, 0x01, 0x00, 0x02, 0x95, 0xF8]
    TEMP_CMD = [0x02, 0x03, 0x00, 0x03, 0x00, 0x02, 0x34, 0x38]
    TSS_CMD = [0x03, 0x03, 0x00, 0x01, 0x00, 0x02, 0x94, 0x29]
    NH3_CMD = [0x01, 0x03, 0x00, 0x01, 0x00, 0x02, 0x95, 0xCB]

    TEMP_DHT_CMD = [0x0A, 0x03, 0x00, 0x00, 0x00, 0x01, 0x85, 0x71]
    HUMI_DHT_CMD = [0x0A, 0x03, 0x00, 0x01, 0x00, 0x01, 0xD4, 0xB1]

    PH_Value = 7
    TSS_Value = 0
    NH3_Value = 0
    TEMP_Value = 0
    TEMP_DHT_Value = 0
    HUMI_DHT_Value = 0
    BUTTON_STATE = True

    rapidoServer = RapidoServerTask()

    def __init__(self, _soft_timer, _rs485):
        self.status = WMR_Status.INIT
        self.soft_timer = _soft_timer
        self.rs485 = _rs485
        return

    def setPumpOn(self):
        print("PUMP is ON")
        self.rs485.modbus485_send(self.relay2_ON)
        return

    def setPumpOff(self):
        print("PUMP is OFF")
        self.rs485.modbus485_send(self.relay2_OFF)
        return

    def WaterMonitoringTask_Run(self):
        if self.status == WMR_Status.INIT:
            self.soft_timer.set_timer(0, self.PUMP_ON_DELAY)
            self.status = WMR_Status.PUMP_ON
            print("PUMP is ON")
            self.BUTTON_STATE = True
            self.rs485.modbus485_send(self.relay2_ON)

        elif self.status == WMR_Status.PUMP_ON:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.status = WMR_Status.PUMP_OFF
                self.soft_timer.set_timer(0, self.PUMP_OFF_DELAY)
                print("PUMP is OFF...")
                self.BUTTON_STATE = False
                self.rs485.modbus485_send(self.relay2_OFF)

        elif self.status == WMR_Status.PUMP_OFF:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.status = WMR_Status.STABLE
                self.soft_timer.set_timer(0, self.STABLE_DELAY)
                print("STABLIZING...")

        elif self.status == WMR_Status.STABLE:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.status = WMR_Status.READ_PH
                self.soft_timer.set_timer(0, self.SENSING_DELAY)
                print("Sending PH command...")
                self.rs485.modbus485_send(self.PH_CMD)

        elif self.status == WMR_Status.READ_PH:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.PH_Value = self.rs485.modbus485_read_big_endian()
                print("Reading PH Value: ", self.PH_Value)

                self.status = WMR_Status.READ_TSS
                self.soft_timer.set_timer(0, self.SENSING_DELAY)
                print("Sending TSS command...")
                self.rs485.modbus485_send(self.TSS_CMD)

        elif self.status == WMR_Status.READ_TSS:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.TSS_Value = self.rs485.modbus485_read_big_endian()
                print("Reading TSS Value: ", self.TSS_Value)

                self.status = WMR_Status.READ_NH3
                self.soft_timer.set_timer(0, self.SENSING_DELAY)
                print("Sending NH3 command...")
                self.rs485.modbus485_send(self.NH3_CMD)

        elif self.status == WMR_Status.READ_NH3:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.NH3_Value = self.rs485.modbus485_read_big_endian()
                print("Reading NH3 Value: ", self.NH3_Value)

                self.soft_timer.set_timer(0, self.SENSING_DELAY)
                print("Sending DHT Temperature command...")
                self.rs485.modbus485_send(self.TEMP_DHT_CMD)
                self.status = WMR_Status.READ_DHT_TEMP


        elif self.status == WMR_Status.READ_DHT_TEMP:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.TEMP_DHT_Value = self.rs485.modbus485_read_adc() / 10.0
                print("Reading DHT Temperature Value: ", self.NH3_Value)

                self.soft_timer.set_timer(0, self.SENSING_DELAY)
                print("Sending DHT Humidity command...")
                self.rs485.modbus485_send(self.HUMI_DHT_CMD)
                self.status = WMR_Status.READ_DHT_HUMI

        elif self.status == WMR_Status.READ_DHT_HUMI:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.HUMI_DHT_Value = self.rs485.modbus485_read_adc() / 10.0
                print("Reading DHT Humidity Value: ", self.HUMI_DHT_Value)

                self.soft_timer.set_timer(0, self.SENSING_DELAY)
                print("Sending Water temperature command...")
                self.rs485.modbus485_send(self.TEMP_CMD)
                self.status = WMR_Status.READ_TEMP

        elif self.status == WMR_Status.READ_TEMP:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.TEMP_Value = self.rs485.modbus485_read_big_endian()
                print("Reading water temperature Value: ", self.TEMP_Value)

                self.status = WMR_Status.IDLE
                self.soft_timer.set_timer(0, self.IDLE_DELAY)
                print("*******************")
                print("PH: ", self.PH_Value, "TSS: ", self.TSS_Value, "NH3: ", self.NH3_Value)
                print("Water Temp: ", self.TEMP_Value)

                print("DHT Temp: ", self.TEMP_DHT_Value, "DHT HUMI: ", self.HUMI_DHT_Value)
                print("*******************")

                self.rapidoServer.uploadData(self.PH_Value, self.TSS_Value, self.NH3_Value, self.TEMP_Value,
                                             self.TEMP_DHT_Value, self.HUMI_DHT_Value)
                print("IDLING...")

        elif self.status == WMR_Status.IDLE:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.status = WMR_Status.INIT

        else:
            print("Invalid status!!!")
        return
