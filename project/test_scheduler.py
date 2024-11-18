from scheduler import *
from Ni1.Tasks.task1 import *
from Ni1.Tasks.task2 import *
import time
scheduler = Scheduler()
scheduler.SCH_Init()

task1 = Task1()
task2 = Task2()
task3 = Task1()

# #normal test
# scheduler.SCH_Add_Task(task1.Task1_Run, 1000, 5000)
# scheduler.SCH_Add_Task(task2.Task2_Run, 3000, 5000)
# scheduler.SCH_Add_Task(task3.Task1_Run, 4000, 5000)
#one shot test
scheduler.SCH_Add_Task(task1.Task1_Run, 1000, 5000)
scheduler.SCH_Add_Task(task2.Task2_Run, 3000, 0)
scheduler.SCH_Add_Task(task3.Task1_Run, 4000, 5000)

while True:
    scheduler.SCH_Update()
    scheduler.SCH_Dispatch_Tasks()
    time.sleep(0.1)