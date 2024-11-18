import Scheduler.scheduler 
import PrivateTasks.private_task_1 
import PrivateTasks.private_task_2 
import time
scheduler = Scheduler.scheduler.Scheduler()

scheduler.SCH_Init()


task1 = PrivateTasks.private_task_1.Task1()


task2 = PrivateTasks.private_task_2.Task2()


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

