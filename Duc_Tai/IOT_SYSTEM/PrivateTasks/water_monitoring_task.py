import enum
from PrivateTasks.rapido_server_task import *
from Utilities.modbus485 import *


class WMR_Status(enum.Enum):
    INIT = 1
    PUMP_ON = 2
    PUMP_OFF = 3
    STABLE = 4
    READ_DIS1 = 5
    READ_DIS2 = 6
    IDLE = 7


class WaterMonitoringTask:
    # PUMP_ON_DELAY = 3000
    # PUMP_OFF_DELAY = 5000
    # STABLE_DELAY = 20000
    # SENSING_DELAY = 500
    # IDLE_DELAY = 10000
    # relay2_ON = [15, 6, 0, 0, 0, 255, 200, 164]
    # relay2_OFF = [15, 6, 0, 0, 0, 0, 136, 228]

    # PH_CMD = [0x02, 0x03, 0x00, 0x01, 0x00, 0x02, 0x95, 0xF8]
    # TEMP_CMD = [0x02, 0x03, 0x00, 0x03, 0x00, 0x02, 0x34, 0x38]
    # TSS_CMD = [0x03, 0x03, 0x00, 0x01, 0x00, 0x02, 0x94, 0x29]
    # NH3_CMD = [0x01, 0x03, 0x00, 0x01, 0x00, 0x02, 0x95, 0xCB]

    # TEMP_DHT_CMD = [0x0A, 0x03, 0x00, 0x00, 0x00, 0x01, 0x85, 0x71]
    # HUMI_DHT_CMD = [0x0A, 0x03, 0x00, 0x01, 0x00, 0x01, 0xD4, 0xB1]

    # PH_Value = 7
    # TSS_Value = 0
    # NH3_Value = 0
    # TEMP_Value = 0
    # TEMP_DHT_Value = 0
    # HUMI_DHT_Value = 0

    # rapidoServer = RapidoServerTask()
    PUMP_ON_DELAY = 3000
    PUMP_OFF_DELAY = 5000
    STABLE_DELAY = 5000
    SENSING_DELAY = 500
    IDLE_DELAY = 5000

    DIS_Value = [2999, 2900]
    BUTTON_STATE = []


    def __init__(self, _soft_timer, _rs485):
        self.status = WMR_Status.INIT
        self.soft_timer = _soft_timer
        self.rs485 = _rs485
        for i in range(0,8):
            self.BUTTON_STATE.append(True)
        print(self.rs485)
        return

    def setPumpOn(self):
        print("PUMP is ON")
        #self.rs485.relayController(1,1)
        return

    def setPumpOff(self):
        print("PUMP is OFF")
        #self.rs485.relayController(1,0)
        return

    def waterMoniteringTask_Run(self):
        #print("Monitering Water is Running!!")
        if self.status == WMR_Status.INIT:
            print("Pump is On")
            self.soft_timer.set_timer(0, self.PUMP_ON_DELAY)
            self.status = WMR_Status.PUMP_ON
            self.BUTTON_STATE = True
            self.rs485.relayController(1, 1)

        elif self.status == WMR_Status.PUMP_ON:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.soft_timer.set_timer(0, self.PUMP_OFF_DELAY)
                self.status = WMR_Status.PUMP_OFF
                self.BUTTON_STATE = False
                self.rs485.relayController(1, 0)
                print("Pump is Off")

        elif self.status == WMR_Status.PUMP_OFF:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.soft_timer.set_timer(0, self.STABLE_DELAY)
                self.status = WMR_Status.STABLE
                print("Stabilizing")

        elif self.status == WMR_Status.STABLE:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.soft_timer.set_timer(0, self.SENSING_DELAY)
                self.status = WMR_Status.READ_DIS1
                self.rs485.Requirement_Distance(9)
                print("Reading")

        elif self.status == WMR_Status.READ_DIS1:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.soft_timer.set_timer(0, self.SENSING_DELAY)
                self.status = WMR_Status.READ_DIS2
                self.DIS_Value[0] = self.rs485.Recive_Distance()
                self.rs485.Requirement_Distance(12)
                print("....")

        elif self.status == WMR_Status.READ_DIS2:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.soft_timer.set_timer(0, self.SENSING_DELAY)
                self.status = WMR_Status.IDLE
                self.DIS_Value[1] = self.rs485.Recive_Distance()
                print("distance = ", self.DIS_Value[0], self.DIS_Value[1])
                print("Idling")

        elif self.status == WMR_Status.IDLE:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.soft_timer.set_timer(0, self.IDLE_DELAY)
                self.status = WMR_Status.INIT
                print(">>>>>>")

        else:
            print("Invalid status")
        return
