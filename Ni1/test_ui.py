from scheduler import  *
from monitoring import *
from Utilities.RS485 import *
from Utilities.SoftwareTimer import *
from Utilities.Main_ui import *
import time

rs485 = RS485
# rs485.setSerial(rs485, rs485.getPort(rs485), 9600)
RS485 = RS485(port="/dev/ttyAMA2", baudrate=9600)

monitoring_timer = SoftwareTimer()

scheduler = Scheduler()
scheduler.SCH_Init()
soft_timer = SoftwareTimer()

monitoring = Monitoring(monitoring_timer, rs485)
main_ui = Main_UI(monitoring)

scheduler.SCH_Add_Task(main_ui.UI_Refresh, 1, 100)
scheduler.SCH_Add_Task(monitoring_timer.timerRun, 1, 100)
# scheduler.SCH_Add_Task(monitoring.MonitoringTask_Run1, 1, 1)

while True:
    scheduler.SCH_Update()
    scheduler.SCH_Dispatch_Tasks()
    time.sleep(0.1)