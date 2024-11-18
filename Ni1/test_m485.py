from Utilities.RS485 import *
from Utilities.SoftwareTimer import *
import serial.tools.list_ports
from tkinter import *
import time

# input = ["0106000000FF"]

# rs485 = RS485(input)

# if rs485.getPort() != "None":
#     ser = serial.Serial(port=rs485.getPort(), baudrate=9600)
# a = Tk()
# a.title("Bản điều khiển")
# a.geometry('700x500')
# name = Label(a, font = ('Arial', 14), text = 'Bật relay 1 ',bg = 'red')
# name.place(x = 30,y = 30)
# but = Button(a, text = 'Bật', width = 5, height = 1, bg = 'blue', fg = 'white', font = ('Arial', 14))
# but.place(x = 250,y = 25)
# a.mainloop()

STimer = SoftwareTimer()
STimer.setTimer(0, 5000)
STimer.setTimer(1, 1000)
n = 0 
a = 1
while True:
    if n == 0:
        if STimer.isExpire(0) == True:  
            print("task0")
            STimer.setTimer(2, 5000)  
            STimer.setTimer(4, 5000)         
            n = 1
    if n == 1:
        if STimer.isExpire(2) == True:  
            print("task2")
            STimer.setTimer(0, 3000)
            n = 0
        if STimer.isExpire(4) == True:  
            print("task4")
            STimer.setTimer(0, 3000)
            n = 0
    # if STimer.isExpire(1) == True:  
    #         print("n: " + str(n))
    #         STimer.setTimer(1, 10)
    STimer.timerRun()
    time.sleep(0.1)
    
