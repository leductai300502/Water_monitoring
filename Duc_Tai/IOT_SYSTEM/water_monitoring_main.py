import PrivateTasks.private_task_1
import PrivateTasks.private_task_2
import PrivateTasks.main_ui_task
import PrivateTasks.led_blinky_task
import PrivateTasks.water_monitoring_task
import PrivateTasks.rapido_server_task
import Utilities.modbus485
import serial.tools.list_ports
import serial

from Scheduler.scheduler import  *
from Utilities.softwaretimer import *
from Utilities.modbus485 import *
import time

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


rs485 = Utilities.modbus485.RS485(input0)
port = rs485.getPort()
rs485.setSerial(port,9600)
watermonitoring_timer = softwaretimer()

scheduler = Scheduler()
scheduler.SCH_Init()
soft_timer = softwaretimer()

task1 = PrivateTasks.private_task_1.Task1()
task2 = PrivateTasks.private_task_2.Task2()

# ledblink = PrivateTasks.led_blinky_task.LedBlinkyTask(soft_timer)

watermonitoring = PrivateTasks.water_monitoring_task.WaterMonitoringTask(watermonitoring_timer, rs485)
main_ui = PrivateTasks.main_ui_task.Main_UI(watermonitoring)
# rapidoserver = PrivateTasks.rapido_server_task.RapidoServerTask()
# main_ui.init_fun(watermonitoring)
# main_ui.init_fun()
# main_ui.UI_Refresh()

#scheduler.SCH_Add_Task(task1.Task1_Run, 1000,2000)
#scheduler.SCH_Add_Task(task2.Task2_Run, 1000,4000)
# scheduler.SCH_Add_Task(soft_timer.Timer_Run, 1, 1)
# scheduler.SCH_Add_Task(ledblink.LedBlinkyTask_Run, 1, 1)


# scheduler.SCH_Add_Task(main_ui.UI_Refresh, 1, 100)

scheduler.SCH_Add_Task(main_ui.UI_Refresh, 1, 100)

#scheduler.SCH_Add_Task(rapidoserver.uploadData, 1, 1000)
# scheduler.SCH_Add_Task(watermonitoring.WaterMonitoringTask_Run, 1, 1)
# scheduler.SCH_Add_Task(watermonitoring.WaterMonitoringTask_Run, 1, 1)
#
# main_ui.i(watermonitoring)
while True:
    # main_ui.UI_Refresh()
    scheduler.SCH_Update()
    scheduler.SCH_Dispatch_Tasks()

    time.sleep(0.1)