from scheduler import *
from Tasks.task1 import *
from Tasks.task2 import *
import time
scheduler = Scheduler()
scheduler.SCH_Init()


task1 = Task1()
task2 = Task2()

scheduler.SCH_Add_Task(task1.Task1_Run, 1000, 5000)
scheduler.SCH_Add_Task(task2.Task2_Run, 1000, 0)
scheduler.SCH_Add_Task(task1.Task1_Run, 1000, 5000)

# n = 0

while True:
    scheduler.SCH_Update()
    scheduler.SCH_Dispatch_Tasks()
    # n += 1
    # if n == 100:
    #     scheduler.SCH_Add_Task(task2.Task2_Run, 1000, 5000)
    time.sleep(0.1)

