import time
from scheduler import *
from softwaretimer import *
#from Task1 import *
#from Task2 import *
from interface import *
from rs485 import *
from water_monitoring_task import *

scheduler = Scheduler()
scheduler.SCH_Init()
soft_timer = softwaretimer()

input0 = ["0106000000FF", "010600000000",
          "0206000000FF", "020600000000",
          "0306000000FF", "030600000000",
          "0406000000FF", "040600000000",
          "0506000000FF", "050600000000",
          "0606000000FF", "060600000000",
          "0706000000FF", "070600000000",
          "0806000000FF", "080600000000",
          "090600080000", "090600000000",
          "0F06000000FF", "0F0600000000",
          "0C0300050001", "0C0600080009"]

rs485 = RS485(input0)
port = rs485.getPort()
rs485.setSerial(port, 9600)

watermonitoring_timer = softwaretimer()

watermonitoring = waterMonitoringTask(rs485, watermonitoring_timer)
iotgateway_ui = IotGateway_UI(watermonitoring)
# task1 = Task1()
# task2 = Task2()
# task3 = Task1()

scheduler.SCH_Add_Task(iotgateway_ui.UI_Refresh, 1, 100)
scheduler.SCH_Add_Task(watermonitoring_timer.Timer_Run, 1, 100)
scheduler.SCH_Add_Task(watermonitoring.waterMoniteringTask_Run,1 ,100)
# scheduler.SCH_Add_Task(task1.Task1_Run, 1000, 5000)
# scheduler.SCH_Add_Task(task2.Task2_Run, 3000, 0)
# scheduler.SCH_Add_Task(task3.Task1_Run, 4000, 5000)

# import time
# from scheduler import *
# from Task1 import *
# from Task2 import *
#
# scheduler = Scheduler()
# scheduler.SCH_Init()
#
# task1 = Task1()
# task2 = Task2()
# task3 = Task1()
#
# scheduler.SCH_Add_Task(task1.Task1_Run, 1000, 5000)
# scheduler.SCH_Add_Task(task2.Task2_Run, 3000, 0)
# scheduler.SCH_Add_Task(task3.Task1_Run, 4000, 5000)

while True:
    scheduler.SCH_Update()
    scheduler.SCH_Dispatch_Tasks()
    time.sleep(0.1)
