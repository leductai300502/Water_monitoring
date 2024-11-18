import enum

class Status(enum.Enum):
    INIT = 1
    PUMP_ON1 = 2
    PUMP_OFF1 = 3
    PUMP_ON2 = 4
    PUMP_OFF2 = 5
    PUMP_ON3 = 6
    PUMP_OFF3 = 7
    STABLE = 8
    IDLE = 9
    RELAY_IN = 12
    RELAY_OUT = 13
    SENSOR1 = 10
    SENSOR2 = 11

    DISTANCE = 14

class Monitoring:
    PUMP_ON_DELAY = [3000, 0, 5000, 1000, 1000, 0]
    PUMP_OFF_DELAY = [5000, 5000, 5000]
    STABLE_DELAY = 5000
    SENSING_DELAY = 500
    IDLE_DELAY = 10000
    BUTTON_STATE = []
    numButton = 8
    count = 0

    distance1_value = 15
    distance2_value = 30
    distance3_value = 0

    distanceMax_value = 30
    distanceRatio = 1000


    def __init__(self, _soft_timer, _rs485):
        self.status = Status.INIT
        self.distanceStatus = Status.INIT
        self.soft_timer = _soft_timer
        self.rs485 = _rs485
        for i in range(0, self.numButton):
            self.BUTTON_STATE.append(False)
        return
    
    def relayController(self, number, state):
        self.rs485.relayController(number, state)

    def distanceController(self, number):
        self.rs485.distanceController(number)

    def getDistanceAll(self):
        if self.distanceStatus == Status.INIT:
            self.soft_timer.setTimer(5, self.SENSING_DELAY)
            self.distanceStatus = Status.SENSOR1
            self.distanceController(9)
            print("Read sensor 9")
        elif self.distanceStatus == Status.SENSOR1:
            if self.soft_timer.isExpire(5) == 1:
                self.distance1_value = self.rs485.serial_read_data()/self.distanceRatio
                self.soft_timer.setTimer(5, self.SENSING_DELAY)
                self.distanceStatus = Status.SENSOR2
                self.distanceController(12)
                print("Read sensor 12")
        elif self.distanceStatus == Status.SENSOR2:
            if self.soft_timer.isExpire(5) == 1:
                self.distance2_value = self.rs485.serial_read_data()/self.distanceRatio
                self.distanceStatus = Status.INIT
                print("Sensor success")
                return 1
        else:
            print("Sensor fail")
            return 0

    def getDistance(self, number):
        if self.distanceStatus == Status.INIT:
            self.soft_timer.setTimer(5, self.SENSING_DELAY)
            self.distanceStatus = Status.SENSOR1
            self.distanceController(number)
            print("Read sensor ",number)
        elif self.distanceStatus == Status.SENSOR1:
            if self.soft_timer.isExpire(5) == 1:
                self.distance1_value = self.rs485.serial_read_data()/distanceRatio
                self.distanceStatus = Status.INIT
                print("Get sensor value success")
                return 1
        else:
            self.distanceStatus = Status.INIT
            print("Get sensor value fail")
            return 0

    def MonitoringTask_Run(self):
        if self.status == Status.INIT:
            print("Init")
            if self.PUMP_ON_DELAY[0] == 0:
                self.status = Status.PUMP_ON2
            else:
                self.soft_timer.setTimer(0, self.PUMP_ON_DELAY[0])
                self.status = Status.PUMP_ON1
                self.BUTTON_STATE[0] = True
                self.rs485.relayController(1, 1)

        elif self.status == Status.PUMP_ON1:
            if self.soft_timer.isExpire(0) == 1:
                print("pump_on1")
                self.soft_timer.setTimer(0, self.PUMP_OFF_DELAY[0])
                self.status = Status.PUMP_OFF1
                self.BUTTON_STATE[0] = False
                self.rs485.relayController(1, 0)

        elif self.status == Status.PUMP_OFF1:
            if self.soft_timer.isExpire(0) == 1:
                print("pump_off1")
                if self.PUMP_ON_DELAY[1] == 0:
                    self.status = Status.PUMP_ON3
                else:
                    self.soft_timer.setTimer(0, self.PUMP_ON_DELAY[1])
                    self.status = Status.PUMP_ON2
                    self.BUTTON_STATE[1] = True
                    self.rs485.relayController(2, 1)

        elif self.status == Status.PUMP_ON2:
            if self.soft_timer.isExpire(0) == 1:
                print("pump_on2")
                self.soft_timer.setTimer(0, self.PUMP_OFF_DELAY[1])
                self.status = Status.PUMP_OFF2
                self.BUTTON_STATE[1] = False
                self.rs485.relayController(2, 0)

        elif self.status == Status.PUMP_OFF2:
            if self.soft_timer.isExpire(0) == 1:
                print("pump_off2")
                if self.PUMP_ON_DELAY[2] == 0:
                    self.status = Status.STABLE
                    self.soft_timer.setTimer(0, self.STABLE_DELAY)
                else:
                    self.soft_timer.setTimer(0, self.PUMP_ON_DELAY[2])
                    self.status = Status.PUMP_ON3
                    self.BUTTON_STATE[2] = True
                    self.rs485.relayController(3, 1)

        elif self.status == Status.PUMP_ON3:
            if self.soft_timer.isExpire(0) == 1:
                print("pump_on3")
                self.soft_timer.setTimer(0, self.PUMP_OFF_DELAY[2])
                self.status = Status.PUMP_OFF3
                self.BUTTON_STATE[2] = False
                self.rs485.relayController(3, 0)

        elif self.status == Status.PUMP_OFF3:
            if self.soft_timer.isExpire(0) == 1:
                print("pump_off3")
                self.status = Status.STABLE
                self.soft_timer.setTimer(0, self.STABLE_DELAY)

        elif self.status == Status.STABLE:
            if self.soft_timer.isExpire(0) == 1:
                print("End")

        else:
            print("Invalid status")
        return

    def MonitoringTask_Run1(self):
        if self.status == Status.INIT:
            print("Init")
            if self.getDistanceAll():
                self.status = Status.RELAY_IN  
                self.soft_timer.setTimer(0, self.PUMP_ON_DELAY[0])
                self.soft_timer.setTimer(1, self.PUMP_ON_DELAY[1])
                self.soft_timer.setTimer(2, self.PUMP_ON_DELAY[2])
                if self.PUMP_ON_DELAY[0]:
                    print("1: On")
                    self.relayController(1, 1)
                    self.BUTTON_STATE[0] = True
                else:
                    self.count += 1
                if self.PUMP_ON_DELAY[1]:
                    print("2: On")
                    self.relayController(2, 1)
                    self.BUTTON_STATE[1] = True
                else:
                    self.count += 1
                if self.PUMP_ON_DELAY[2]:
                    print("3: On")
                    self.relayController(3, 1)
                    self.BUTTON_STATE[2] = True
                else:
                    self.count += 1      
        elif self.status == Status.RELAY_IN:
            if self.soft_timer.isExpire(0):
                print("1: Off")
                self.count += 1
                self.relayController(1, 0)
                self.BUTTON_STATE[0] = False
            if self.soft_timer.isExpire(1):
                print("2: Off")
                self.count += 1
                self.relayController(2, 0)
                self.BUTTON_STATE[1] = False
            if self.soft_timer.isExpire(2):
                print("3: Off")
                self.count += 1
                self.relayController(3, 0)
                self.BUTTON_STATE[2] = False

            if self.count >= 3:
                self.count = 0
                self.status = Status.STABLE
                self.soft_timer.setTimer(0, self.STABLE_DELAY)
        elif self.status == Status.STABLE:
            if self.soft_timer.isExpire(0):
                self.status == Status.RELAY_OUT
                self.soft_timer.setTimer(0, self.PUMP_ON_DELAY[3])
                self.soft_timer.setTimer(1, self.PUMP_ON_DELAY[4])
                self.soft_timer.setTimer(2, self.PUMP_ON_DELAY[5])
                if self.PUMP_ON_DELAY[3]:
                    print("4: On")
                    self.relayController(4, 1)
                    self.BUTTON_STATE[3] = True
                else:
                    self.count += 1
                if self.PUMP_ON_DELAY[4]:
                    print("5: On")
                    self.relayController(5, 1)
                    self.BUTTON_STATE[4] = True
                else:
                    self.count += 1
                if self.PUMP_ON_DELAY[5]:
                    print("6: On")
                    self.relayController(6, 1)
                    self.BUTTON_STATE[5] = True
                else:
                    self.count += 1
        elif self.status == Status.RELAY_OUT:
            if self.soft_timer.isExpire(0):
                print("4: Off")
                self.count += 1
                self.relayController(4, 0)
                self.BUTTON_STATE[4] = False
            if self.soft_timer.isExpire(1):
                print("5: Off")
                self.count += 1
                self.relayController(5, 0)
                self.BUTTON_STATE[5] = False
            if self.soft_timer.isExpire(2):
                print("6: Off")
                self.count += 1
                self.relayController(6, 0)
                self.BUTTON_STATE[6] = False

            if self.count >= 3:
                self.count = 0
                print("End")       
        else:
            self.status = Status.INIT





