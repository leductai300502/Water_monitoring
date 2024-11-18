import time
from scheduler import *
from task import *
# from task2 import *


scheduler = Scheduler()
scheduler.SCH_Init()
task1 = Task1()
task2 = Task2()
task3 = Task3()
task4 = Task4()

scheduler.SCH_Add_Task(task1.Task1_Run, 1000,5000)
scheduler.SCH_Add_Task(task2.Task2_Run, 3000,0)

scheduler.SCH_Add_Task(task3.Task3_Run, 4000,5000)
scheduler.SCH_Add_Task(task4.Task4_Run, 1000,0)

while True:
    scheduler.SCH_Update()
    scheduler.SCH_Dispatch_Tasks()
    time.sleep(0.1)