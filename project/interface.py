import tkinter as tk
from tkinter import *
from PIL import Image
import time
class IotGateway_UI:
    dataModel = None
    def __init__(self,data):
        self.dataModel = data
        print("Init the UI!!")
        self.is_on = [False, False, False, False, False, False, False, False]
        self.window = tk.Tk()
        self.on = PhotoImage(file="on.png")
        self.off = PhotoImage(file="off.png")

        self.window.attributes('-fullscreen', True)
        self.window.title("IotGateway UI")
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        print("Size = ", screen_width, screen_height)

        self.button1 = Button(self.window, image=self.on, bd=0, command=lambda :self.toggle_button_click(1))
        self.button1.place(x=screen_width/4, y=210)

        self.Relay1 = Label(self.window, text="RELAY1",fg="#0000ff", font= "Helvetica 50 bold")
        self.Relay1.place(x=0, y=210, width=screen_width/4, height=100)

        self.button2 = Button(self.window, image=self.off, bd=0, command=lambda: self.toggle_button_click(2))
        self.button2.place(x=3* screen_width / 4, y=210)

        self.Relay2 = Label(self.window, text="RELAY2", fg="#0000ff", font="Helvetica 50 bold")
        self.Relay2.place(x=2* screen_width / 4, y=210, width=screen_width / 4, height=100)

        self.button3 = Button(self.window, image=self.off, bd=0, command=lambda: self.toggle_button_click(3))
        self.button3.place(x=screen_width / 4, y=310)

        self.Relay3 = Label(self.window, text="RELAY3", fg="#0000ff", font="Helvetica 50 bold")
        self.Relay3.place(x=0, y=310, width=screen_width / 4, height=100)

        self.button4 = Button(self.window, image=self.off, bd=0, command=lambda: self.toggle_button_click(4))
        self.button4.place(x=3*screen_width / 4, y=310)

        self.Relay4 = Label(self.window, text="RELAY4", fg="#0000ff", font="Helvetica 50 bold")
        self.Relay4.place(x=2*screen_width / 4, y=310, width=screen_width / 4, height=100)

        self.button5 = Button(self.window, image=self.off, bd=0, command=lambda: self.toggle_button_click(5))
        self.button5.place(x=screen_width / 4, y=410)

        self.Relay5 = Label(self.window, text="RELAY5", fg="#0000ff", font="Helvetica 50 bold")
        self.Relay5.place(x=0, y=410, width=screen_width / 4, height=100)

        self.button6 = Button(self.window, image=self.off, bd=0, command=lambda: self.toggle_button_click(6))
        self.button6.place(x=3*screen_width / 4, y=410)

        self.Relay6 = Label(self.window, text="RELAY6", fg="#0000ff", font="Helvetica 50 bold")
        self.Relay6.place(x=2*screen_width / 4, y=410, width=screen_width / 4, height=100)

        self.button7 = Button(self.window, image=self.off, bd=0, command=lambda: self.toggle_button_click(7))
        self.button7.place(x=screen_width / 4, y=510)

        self.Relay7 = Label(self.window, text="RELAY7", fg="#0000ff", font="Helvetica 50 bold")
        self.Relay7.place(x=0, y=510, width=screen_width / 4, height=100)

        self.button8 = Button(self.window, image=self.off, bd=0, command=lambda: self.toggle_button_click(8))
        self.button8.place(x=3*screen_width / 4, y=510)

        self.Relay8 = Label(self.window, text="RELAY8", fg="#0000ff", font="Helvetica 50 bold")
        self.Relay8.place(x=2*screen_width / 4, y=510, width=screen_width / 4, height=100)

        self.labelDistance1 = tk.Label(text="Distance1",
                                        fg="#0000ff",
                                        justify=CENTER,
                                        # bg = "#000",
                                        font="Helvetica 50 bold")

        self.labelDistance1.place(x=0, y=0, width=screen_width / 3, height=100)

        self.labelDistance1Unit = tk.Label(text="mm",
                                       fg="#0000ff",
                                       justify=CENTER,
                                       # bg = "#000",
                                       font="Helvetica 30 bold")

        self.labelDistance1Unit.place(x=screen_width / 3, y=0, width=screen_width / 3, height=100)

        self.labelDistance1Value = tk.Label(text="3000",
                                           fg="#0000ff",
                                           justify=CENTER,
                                           # bg = "#000",
                                           font="Helvetica 50 bold")

        self.labelDistance1Value.place(x=2 * screen_width / 3, y=0, width=screen_width / 3, height=100)

        self.labelDistance2 = tk.Label(text="Distance2",
                                       fg="#0000ff",
                                       justify=CENTER,
                                       # bg = "#000",
                                       font="Helvetica 50 bold")

        self.labelDistance2.place(x=0, y=110, width=screen_width / 3, height=100)

        self.labelDistance2Unit = tk.Label(text="mm",
                                           fg="#0000ff",
                                           justify=CENTER,
                                           # bg = "#000",
                                           font="Helvetica 30 bold")

        self.labelDistance2Unit.place(x=screen_width / 3, y=110, width=screen_width / 3, height=100)

        self.labelDistance2Value = tk.Label(text="3000",
                                            fg="#0000ff",
                                            justify=CENTER,
                                            # bg = "#000",
                                            font="Helvetica 50 bold")

        self.labelDistance2Value.place(x=2 * screen_width / 3, y=110, width=screen_width / 3, height=100)



    def toggle_button_click(self, number):
        print("Button is clicked!!")
        if self.is_on[number - 1]:
            #self.button.config(image=self.off)
            self.UI_Set_Button_text(number, self.off)
            self.is_on[number - 1] = False
            # gửi lệnh tắt relay
            self.dataModel.setPumpOff(number)
        else:
            #self.button.config(image=self.on)
            self.UI_Set_Button_text(number, self.on)
            self.is_on[number - 1] = True
            # gửi lệnh bật relay
            self.dataModel.setPumpOn(number)

    def UI_Refresh(self):
        self.UI_Set_Value_Text(self.labelDistance1Value, self.dataModel.DIS_Value[0])
        self.UI_Set_Value_Text(self.labelDistance2Value, self.dataModel.DIS_Value[1])
        if self.dataModel.BUTTON_STATE == True:
            self.button1.config(image = self.on)
            self.is_on[0] = True
        else:
            self.button1.config(image = self.off)
            self.is_on[0] = False
        self.window.update()

    def UI_Set_Value_Text(self, text_object, data):
        text_object.config(text="%.2f" % data)

    def UI_Set_Button_text(self, number, data):
        if number == 1:
            self.button1.config(image= data)
        elif number == 2:
            self.button2.config(image= data)
        elif number == 3:
            self.button3.config(image= data)
        elif number == 4:
            self.button4.config(image= data)
        elif number == 5:
            self.button5.config(image= data)
        elif number == 6:
            self.button6.config(image= data)
        elif number == 7:
            self.button7.config(image= data)
        elif number == 8:
            self.button8.config(image= data)