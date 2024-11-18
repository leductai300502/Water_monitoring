import tkinter as tk
from tkinter import *
import time
class Main_UI:
    dataModel = None

    def __init__(self, data):
        self.dataModel = data
        print("Init the UI")
        self.is_on = True
        self.window = tk.Tk()
        self.on = PhotoImage(file="Images/on_button.png")
        self.off = PhotoImage(file="Images/off_button.png")
        self.logo = PhotoImage(file="Images/bku_s.png")

        self.window.attributes('-fullscreen', True)
        self.window.title("Rapido Project")
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        print("Size:", screen_width, screen_height)

        self.on_button = Button(self.window, image=self.on, bd=0, command=self.toggle_button_click, justify=CENTER)
        self.logo_button = Button(self.window, image = self.logo, bd=0, justify = RIGHT)

        self.labelAMONIACaption = tk.Label(text="AMONIA",
                                      fg="#0000ff",
                                      justify=CENTER,
                                      # bg = "#000",
                                      font="Helvetica 50 bold")

        self.labelAMONIACaption.place(x=0, y=0, width=screen_width / 3, height=120)

        self.labelTDSCaption = tk.Label(text="TDS",
                                   fg="#0000ff",
                                   justify=CENTER,
                                   # bg = "#000",
                                   font="Helvetica 50 bold")

        self.labelTDSCaption.place(x=screen_width / 3, y=0, width=screen_width / 3, height=120)

        self.labelPHCaption = tk.Label(text="PH",
                                  fg="#0000ff",
                                  justify=CENTER,
                                  # bg = "#000",
                                  font="Helvetica 50 bold")

        self.labelPHCaption.place(x=2 * screen_width / 3, y=0, width=screen_width / 3, height=120)

        self.labelAMONIAUnit = tk.Label(text="(PPM)",
                                   fg="#0000ff",
                                   justify=CENTER,
                                   # bg = "#000",
                                   font="Helvetica 15 bold")

        self.labelAMONIAUnit.place(x=0, y=130, width=screen_width / 3, height=50)

        self.labelTDSUnit = tk.Label(text="(NTU)",
                                fg="#0000ff",
                                justify=CENTER,
                                # bg = "#000",
                                font="Helvetica 15 bold")

        self.labelTDSUnit.place(x=screen_width / 3, y=130, width=screen_width / 3, height=50)

        self.labelPHUnit = tk.Label(text="( )",
                               fg="#0000ff",
                               justify=CENTER,
                               # bg = "#000",
                               font="Helvetica 15 bold")

        self.labelPHUnit.place(x=2 * screen_width / 3, y=130, width=screen_width / 3, height=50)

        self.labelAMONIAValue = tk.Label(text="5.12",
                                    fg="#0000ff",
                                    justify=CENTER,
                                    # bg = "#000",
                                    font="Helvetica 60 bold")

        self.labelAMONIAValue.place(x=0, y=200, width=screen_width / 3, height=100)

        self.labelTDSValue = tk.Label(text="20",
                                 fg="#0000ff",
                                 justify=CENTER,
                                 # bg = "#000",
                                 font="Helvetica 60 bold")

        self.labelTDSValue.place(x=screen_width / 3, y=200, width=screen_width / 3, height=100)

        self.labelPHValue = tk.Label(text="7.11",
                                fg="#0000ff",
                                justify=CENTER,
                                # bg = "#000",
                                font="Helvetica 60 bold")

        self.labelPHValue.place(x=2 * screen_width / 3, y=200, width=screen_width / 3, height=100)

        # define on and off stage of the toggle

        self.on_button.place(x=0, y=300, width=screen_width)
        self.logo_button.place(x=screen_width - 100, y=500, width=100)

    # define the click event of the toggle
    def toggle_button_click(self):
        # Determine is on or off
        if self.is_on:
            self.on_button.config(image = self.off)
            self.is_on = False
            self.dataModel.setPumpOff()
            self.dataModel.BUTTON_STATE = False
        else:
            self.on_button.config(image = self.on)
            self.is_on = True
            self.dataModel.setPumpOn()
            self.dataModel.BUTTON_STATE = True
        print("Button is clicked!!!")


    def UI_Refresh(self):
        self.UI_Set_Text(self.labelPHValue, self.dataModel.PH_Value)
        self.UI_Set_Text(self.labelTDSValue, self.dataModel.TSS_Value)
        self.UI_Set_Text(self.labelAMONIAValue, self.dataModel.NH3_Value)
        if self.dataModel.BUTTON_STATE == True:
            self.on_button.config(image = self.on)
            self.is_on = True
        else:
            self.on_button.config(image = self.off)
            self.is_on = False
        self.window.update()


    def UI_Set_Text(self,text_object, data):
        text_object.config(text="%.2f" % data)
