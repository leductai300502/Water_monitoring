import tkinter as tk
from PIL import Image as PILImage, ImageTk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mbox

import time
import math
import enum
import cv2
import tensorflow as tf
from tensorflow import keras
import threading

from keras.models import load_model  # TensorFlow is required for Keras to work
import numpy as np


class page_Status(enum.Enum):
    HOME_PAGE = 0
    AUTOMATIVE_PAGE = 1
    MANUAL_PAGE = 2
    AI_PAGE = 3
class Main_UI:
    dataModel = None
    frame = None
    image_pil = None
    image_tk = None
    numButton = 8
    camera_url = None
    camera_url_2 = None
    check_device_flag = False
    camera_2_flag = False
    cap_2_flag = False
    continute = 0
    break_thread = False
    is_on = []
    on_button = []
    inputRatio = []
    outputRatio = []
    list_device = []
    models = []
    range_of_camera =[]
    class_names = []
    ratio_value = [0,1,2,3,4,5]
    cap = None
    cap_2 = None
    # processing_thread = threading.Thread(target=self.process_image)
    
    page = page_Status.HOME_PAGE
    
    def __init__(self, data):
        self.dataModel = data
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)
        # self.list_device.append('hehe')
        # Gọi hàm để đọc từng dòng của file và gán vào danh sách
        self.processing_thread = threading.Thread(target=self.process_image)

        # self.processing_thread_2 = threading.Thread(target=self.process_image_2)
        # self.processing_thread_2.start()
        # Tạo thread để xử lý hình ảnh 
        self.processing_thread_1 = threading.Thread(target=self.Predict_image)
        self.strart_flag = False
        # Tạo cờ
        self.update_image_flag = False
        self.update_image_flag_2 = False
        self.lines_list = self.read_text_file_to_list('IOT_SYSTEM\Save_Url\preparetion_url.txt')
        

        # Kiểm tra và in từng dòng trong danh sách
        if self.lines_list is not None:
            print("Danh sách các dòng trong file:")
            for line in self.lines_list:
                self.list_device.append(line)
                print(line.strip())  # Sử dụng strip() để loại bỏ ký tự xuống dòng (newline) ở cuối mỗi dòng

        self.window = Tk()
       

        for i in range(0, self.numButton):
            self.is_on.append(True)
            self.on_button.append(Button(self.window, bd=0, justify=RIGHT))
            # self.on_button[i].config(command=lambda:self.toggle_button_click(i))

        self.window.attributes('-fullscreen', True)
        # self.window.geometry("1024x600")
        self.window.title("Rapido Project")
        self.window.configure(bg='SlateGrey', highlightbackground='SlateGrey',
                              highlightthickness=10)

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        # print("Size:", self.screen_width, self.screen_height)

        
        self.option_frame = tk.Frame(self.window)

        self.option_frame.pack(side = 'left')
        self.option_frame.pack_propagate(False)
        self.option_frame.configure(width = self.screen_width / 5, height = self.screen_height,
                               bg = 'dark gray',
                               highlightbackground='Black',
                               highlightthickness=10)

        self.main_frame = tk.Frame(self.window)

        self.main_frame.pack(side = 'right')
        self.main_frame.pack_propagate(False)
        self.main_frame.configure(width = 4*self.screen_width / 5 - 5, height = self.screen_height,
                             bg = 'dark grey',
                             highlightbackground='Black',
                             highlightthickness=10)
        
        # Home button
        self.home_button = Button(self.option_frame, text='Home', font="Helvetica 14 bold",
                                  command=lambda: self.indicate(self.home_button,self.home_page),
                                  activebackground = 'gray',
                                  width = 15, height = 1,
                                  foreground = 'White',
                                  bg = 'MediumBlue',
                                  bd = 5)
        self.home_button.pack(side='top', pady = 20)

        # Auto button
        self.auto_button = Button(self.option_frame, text='Automative', font="Helvetica 14 bold",
                                  command=lambda: self.indicate(self.auto_button, self.automative_page),
                                  activebackground = 'gray',
                                  width = 15, height = 1,
                                  foreground = 'White',
                                  bg = 'RoyalBlue',
                                  bd = 5)
        self.auto_button.pack(side='top', pady = 20)

        # manual button
        self.manual_button = Button(self.option_frame, text='Manual', font="Helvetica 14 bold",
                                    command=lambda: self.indicate(self.manual_button, self.manual_page),
                                    activebackground = 'gray',
                                    width = 15, height = 1,
                                    foreground = 'White',
                                    bg = 'RoyalBlue',
                                    bd = 5)
        self.manual_button.pack(side='top', pady = 20)

        # AI button
        self.ai_button = Button(self.option_frame, text='AI', font="Helvetica 14 bold",
                                command=lambda: self.indicate(self.ai_button, self.ai_page),
                                activebackground = 'gray',
                                width = 15, height = 1,
                                foreground = 'White',
                                bg = 'RoyalBlue',
                                bd = 5)
        self.ai_button.pack(side='top', pady = 20)

        # Exit button
        self.exit_button = Button(self.option_frame, text='Exit', font="Helvetica 14 bold",
                                    command=lambda: self.Destroy(),
                                  activebackground = 'gray',
                                  width = 15, height = 1,
                                  foreground = 'White',
                                  bg = 'Red',
                                  bd = 5)
        self.exit_button.pack(side="bottom", pady = 20)

        # first time come to GUI
        self.indicate(self.home_button,self.home_page)
    
    def Destroy(self):
        self.break_thread = True
        self.window.destroy()
    
    def indicate(self, lb, page):
        # unHighlight buttons
        self.home_button.config(bg = 'RoyalBlue')
        self.auto_button.config(bg = 'RoyalBlue')
        self.manual_button.config(bg = 'RoyalBlue')
        self.ai_button.config(bg = 'RoyalBlue')

        # Highlight Button
        lb.config(bg = 'MediumBlue')

        # Refresh main page
        for frame in self.main_frame.winfo_children():
            frame.destroy()

        page()

    def home_page(self):
        self.page = page_Status.HOME_PAGE
        

        self.home_frame = tk.Frame(self.main_frame)
        self.home_lb = tk.Label(self.home_frame, text="gioi thieu\n\npage 1", font="Helvetica 12 bold")
        self.home_lb.pack()
        self.home_frame.pack()
    
    def automative_page(self):
        self.page = page_Status.AUTOMATIVE_PAGE
        
        self.top_manual_frame = tk.LabelFrame(self.main_frame)
        self.top_manual_frame.pack(side = 'top')
        self.top_manual_frame.pack_propagate(False)
        self.top_manual_frame.configure(width = self.main_frame.winfo_screenwidth(), 
                                    height=self.main_frame.winfo_screenheight()/3,
                                    bg='dark gray', padx= 10, pady= 10)
        
        self.bottom_manual_frame = tk.LabelFrame(self.main_frame)
        self.bottom_manual_frame.pack(side = 'top')
        self.bottom_manual_frame.pack_propagate(False)
        self.bottom_manual_frame.configure(width = self.main_frame.winfo_screenwidth(), 
                                            height=2*self.main_frame.winfo_screenheight()/3,
                                            bg='dark gray', padx= 10, pady= 20)

        self.liquidBox(self.top_manual_frame)

        self.bottom_manual_frame.rowconfigure(2, weight=4)
        # self.bottom_manual_frame.rowconfigure(1, weight=3)

        # Setting input liquid
        self.ratioLabel = tk.Label(self.bottom_manual_frame, text="Input",
                               width=10, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.ratioLabel.grid(column=0, row=0, padx=12, pady=2, sticky=tk.NS)

        self.ratioLabel0 = tk.Label(self.bottom_manual_frame, text="Ratio",
                               width=10, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.ratioLabel0.grid(column=0, row=1, padx=12, pady=2, sticky=tk.NS)

        self.ratioLabel1 = tk.Label(self.bottom_manual_frame, text="Liquid 1",
                               width=10, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.ratioLabel1.grid(column=1, row=0, padx=12, pady=2, sticky=tk.NS)

        self.ratioLabel2 = tk.Label(self.bottom_manual_frame, text="Liquid 2 ",
                               width=10, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.ratioLabel2.grid(column=2, row=0, padx=12, pady=2, sticky=tk.NS)

        self.ratioLabel3 = tk.Label(self.bottom_manual_frame, text="Liquid 3",
                               width=10, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.ratioLabel3.grid(column=3, row=0, padx=12, pady=2, sticky=tk.NS)

        self.ratioBox1 = ttk.Combobox(self.bottom_manual_frame, values=self.ratio_value)
        self.ratioBox1.current(0)
        self.ratioBox1.grid(column=1, row=1, padx=12, pady=2, sticky=tk.NS)

        self.ratioBox2 = ttk.Combobox(self.bottom_manual_frame, values=self.ratio_value)
        self.ratioBox2.current(0)
        self.ratioBox2.grid(column=2, row=1, padx=12, pady=2, sticky=tk.NS)

        self.ratioBox3 = ttk.Combobox(self.bottom_manual_frame, values=self.ratio_value)
        self.ratioBox3.current(0)
        self.ratioBox3.grid(column=3, row=1, padx=12, pady=2, sticky=tk.NS)

        self.totalLiquid = tk.Label(self.bottom_manual_frame, text="Total liquid volume",
                               width=14, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.totalLiquid.grid(column=0, row=2, padx=12, pady=10, sticky=tk.NS, columnspan=2)
        self.totalBox = ttk.Combobox(self.bottom_manual_frame, values=[1000,2000,3000])
        self.totalBox.current(0)
        self.totalBox.grid(column=2, row=2, padx=12, pady=10, sticky=tk.NS)

        self.unitLabel = tk.Label(self.bottom_manual_frame, text="ml",
                               width=14, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.unitLabel.grid(column=3, row=2, padx=12, pady=10, sticky=tk.W)
        # Setting output liquid
        self.outputLabel = tk.Label(self.bottom_manual_frame, text="Output",
                               width=10, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.outputLabel.grid(column=0, row=3, padx=12, pady=2, sticky=tk.NS)

        self.outputLabel0 = tk.Label(self.bottom_manual_frame, text="Ratio",
                               width=10, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.outputLabel0.grid(column=0, row=4, padx=12, pady=2, sticky=tk.NS)

        self.outputLabel1 = tk.Label(self.bottom_manual_frame, text="Relay 1",
                               width=10, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.outputLabel1.grid(column=1, row=3, padx=12, pady=2, sticky=tk.NS)

        self.outputLabel2 = tk.Label(self.bottom_manual_frame, text="Relay 2 ",
                               width=10, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.outputLabel2.grid(column=2, row=3, padx=12, pady=2, sticky=tk.NS)

        self.outputLabel3 = tk.Label(self.bottom_manual_frame, text="Relay 3",
                               width=10, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.outputLabel3.grid(column=3, row=3, padx=12, pady=2, sticky=tk.NS)

        self.outputRatioBox1 = ttk.Combobox(self.bottom_manual_frame, values=self.ratio_value)
        self.outputRatioBox1.current(0)
        self.outputRatioBox1.grid(column=1, row=4, padx=12, pady=2, sticky=tk.NS)

        self.outputRatioBox2 = ttk.Combobox(self.bottom_manual_frame, values=self.ratio_value)
        self.outputRatioBox2.current(0)
        self.outputRatioBox2.grid(column=2, row=4, padx=12, pady=2, sticky=tk.NS)

        self.outputRatioBox3 = ttk.Combobox(self.bottom_manual_frame, values=self.ratio_value)
        self.outputRatioBox3.current(0)
        self.outputRatioBox3.grid(column=3, row=4, padx=12, pady=2, sticky=tk.NS)

        self.outputEnter = tk.Button(self.bottom_manual_frame, text="Enter values",
                                     command=lambda:self.get_value(),
                                     width = 15, height = 1)
        self.outputEnter.grid(column=1, row=5, padx=12, pady=10, sticky=tk.N, columnspan=2)
    
    def manual_page(self):
        # self.break_thread = True
        self.page = page_Status.MANUAL_PAGE

        self.top_manual_frame = tk.LabelFrame(self.main_frame)
        self.top_manual_frame.pack(side = 'top')
        self.top_manual_frame.pack_propagate(False)
        self.top_manual_frame.configure(width = self.main_frame.winfo_screenwidth(), 
                                    height=self.main_frame.winfo_screenheight()/3,
                                    bg='dark gray', padx= 10, pady= 10)
        
        self.bottom_manual_frame = tk.LabelFrame(self.main_frame)
        self.bottom_manual_frame.pack(side = 'top')
        self.bottom_manual_frame.pack_propagate(False)
        self.bottom_manual_frame.configure(width = self.main_frame.winfo_screenwidth(), 
                                            height=2*self.main_frame.winfo_screenheight()/3,
                                            bg='dark gray', padx= 10, pady= 20)

        self.liquidBox(self.top_manual_frame)

        ### Button 

        # Relay1
        self.relay1 = tk.Label(self.bottom_manual_frame, text="Relay 1",
                               width=6, height=1, bg='dark gray',
                               font="Helvetica 18 bold")
        self.relay1.grid(column=0, row=0, padx=12, pady=10, sticky=tk.NS)

        self.on_button[0] = tk.Button(self.bottom_manual_frame,text="ON",
                                       command=lambda:self.toggle_button_click(0),
                                       width=6, height=1,
                                       bg="LimeGreen", fg="White",
                                       font="Helvetica 16 bold")
        self.on_button[0].grid(column=1, row=0, padx=12, pady=10)

        # Relay2
        self.relay2 = tk.Label(self.bottom_manual_frame, text="Relay 2",
                               width=6, height=1, bg='dark gray',
                               font="Helvetica 18 bold")
        self.relay2.grid(column=2, row=0, padx=12, pady=10, sticky=tk.NS)

        self.on_button[1] = tk.Button(self.bottom_manual_frame,text="ON",
                                      command=lambda:self.toggle_button_click(1),
                                      width=6, height=1,
                                      bg="LimeGreen", fg="White",
                                      font="Helvetica 16 bold")
        self.on_button[1].grid(column=3, row=0, padx=12, pady=10)

        # Relay3
        self.relay3 = tk.Label(self.bottom_manual_frame, text="Relay 3",
                               width=6, height=1, bg='dark gray',
                               font="Helvetica 18 bold")
        self.relay3.grid(column=4, row=0, padx=12, pady=10, sticky=tk.NS)

        self.on_button[2] = tk.Button(self.bottom_manual_frame,text="ON",
                                      command=lambda:self.toggle_button_click(2),
                                      width=6, height=1,
                                      bg="LimeGreen", fg="White",
                                      font="Helvetica 16 bold")
        self.on_button[2].grid(column=5, row=0, padx=12, pady=10)
        
        # Relay4
        self.relay4 = tk.Label(self.bottom_manual_frame, text="Relay 4",
                               width=6, height=1, bg='dark gray',
                               font="Helvetica 18 bold")
        self.relay4.grid(column=0, row=1, padx=12, pady=10, sticky=tk.NS)

        self.on_button[3] = tk.Button(self.bottom_manual_frame,text="ON",
                                       command=lambda:self.toggle_button_click(3),
                                       width=6, height=1,
                                       bg="LimeGreen", fg="White",
                                       font="Helvetica 16 bold")
        self.on_button[3].grid(column=1, row=1, padx=12, pady=10)
        # Relay5
        self.relay5 = tk.Label(self.bottom_manual_frame, text="Relay 5",
                               width=6, height=1, bg='dark gray',
                               font="Helvetica 18 bold")
        self.relay5.grid(column=2, row=1, padx=12, pady=10, sticky=tk.NS)

        self.on_button[4] = tk.Button(self.bottom_manual_frame,text="ON",
                                      command=lambda:self.toggle_button_click(4),
                                      width=6, height=1,
                                      bg="LimeGreen", fg="White",
                                      font="Helvetica 16 bold")
        self.on_button[4].grid(column=3, row=1, padx=12, pady=10)

        # Relay6
        self.relay6 = tk.Label(self.bottom_manual_frame, text="Relay 6",
                               width=6, height=1, bg='dark gray',
                               font="Helvetica 18 bold")
        self.relay6.grid(column=4, row=1, padx=12, pady=10, sticky=tk.NS)

        self.on_button[5] = tk.Button(self.bottom_manual_frame,text="ON",
                                      command=lambda:self.toggle_button_click(5),
                                      width=6, height=1,
                                      bg="LimeGreen", fg="White",
                                      font="Helvetica 16 bold")
        self.on_button[5].grid(column=5, row=1, padx=12, pady=10)

        # Bump1
        self.bump1 = tk.Label(self.bottom_manual_frame, text="Bump 1",
                               width=6, height=1, bg='dark gray',
                               font="Helvetica 18 bold")
        self.bump1.grid(column=0, row=2, padx=12, pady=10, sticky=tk.NS, columnspan=2)

        self.on_button[6] = tk.Button(self.bottom_manual_frame,text="ON",
                                       command=lambda:self.toggle_button_click(6),
                                       width=6, height=1,
                                       bg="LimeGreen", fg="White",
                                       font="Helvetica 16 bold")
        self.on_button[6].grid(column=1, row=2, padx=12, pady=10, columnspan=2)

        # Bump2
        self.bump2 = tk.Label(self.bottom_manual_frame, text="Bump 2",
                               width=6, height=1, bg='dark gray',
                               font="Helvetica 18 bold")
        self.bump2.grid(column=2, row=2, padx=12, pady=20, sticky=tk.NS, columnspan=2)

        self.on_button[7] = tk.Button(self.bottom_manual_frame,text="ON",
                                      command=lambda:self.toggle_button_click(7),
                                      width=6, height=1,
                                      bg="LimeGreen", fg="White",
                                      font="Helvetica 16 bold")
        self.on_button[7].grid(column=3, row=2, padx=12, pady=10, columnspan=2)

    def ai_page(self):
        self.page = page_Status.AI_PAGE
        if self.strart_flag == False:
            self.processing_thread.start()
            self.processing_thread_1.start()
            self.strart_flag == True
        self.ai_frame = tk.Frame(self.main_frame)
        self.ai_lb = tk.Label(self.ai_frame, text="Upcoming", font="Helvetica 12 bold")

       
        self.ai_lb.pack()
        self.ai_frame.pack()
        #set form frame in main_frame
        self.form_ipCamera_frame = tk.LabelFrame(self.main_frame,text='Top Form')
        self.form_ipCamera_frame.pack(side = 'top')
        self.form_ipCamera_frame.pack_propagate(False)
        self.form_ipCamera_frame.grid_propagate(False)
        self.form_ipCamera_frame.configure(width = self.main_frame.winfo_screenwidth() , 
                                    height=self.main_frame.winfo_screenheight()/3 - 5,
                                    bg='gray', padx= 20, pady= 20,highlightbackground='white',highlightthickness=5)
        #set connect form 
        self.Connect_Frame = tk.Frame(self.form_ipCamera_frame)
        self.Connect_Frame.pack(side='left')
        self.Connect_Frame.grid_propagate(False)
        self.Connect_Frame.pack_propagate(False)
        self.Connect_Frame.configure(width = self.form_ipCamera_frame.winfo_screenwidth()/4 -10 , 
                                    height=self.form_ipCamera_frame.winfo_screenheight(),
                                    bg='dark gray', padx= 0, pady= 10,highlightbackground='white',highlightthickness=5)
        #lable for IP Area
        self.IP = tk.Label(self.Connect_Frame, text="IP Adress",
                               width=10, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.IP.grid(column=0, row=0, padx=12, pady=2, sticky=tk.EW)

        self.Area_IP = tk.Entry(self.Connect_Frame, 
                               width=30)
        self.Area_IP.grid(column=1, row=0, padx=12, pady=2, sticky=tk.EW)
        #lable for Port
        self.Port = tk.Label(self.Connect_Frame, text="Port",
                               width=10, height=1, bg='dark gray',
                               font="Helvetica 12 bold")
        self.Port.grid(column=0, row=1, padx=12, pady=10, sticky=tk.EW)

        self.Area_Port = tk.Entry(self.Connect_Frame, 
                               width=30)
        self.Area_Port.grid(column=1, row=1, padx=12, pady=2, sticky=tk.EW)
        #button submit
        self.button_submit = tk.Button(self.Connect_Frame,text="Connect",
                                      command=lambda:self.get_url(),
                                      width=6, height=1,
                                      bg="LimeGreen", fg="White",
                                      font="Helvetica 16 bold")
        self.button_submit.grid(column=0,row=2, padx=12, pady=2, sticky=tk.EW)

        #chose device frame
        self.Chose_Device_Frame = tk.Frame(self.form_ipCamera_frame)
        self.Chose_Device_Frame.pack(side='right')
        self.Chose_Device_Frame.grid_propagate(False)
        self.Chose_Device_Frame.configure(width = self.form_ipCamera_frame.winfo_screenwidth()/2 , 
                                    height=self.form_ipCamera_frame.winfo_screenheight(),
                                    bg='dark gray', padx= 10, pady= 10,highlightbackground='white',highlightthickness=5)
        # print(self.form_ipCamera_frame.winfo_screenwidth()/2)
        for i, text in enumerate(self.list_device):
            self.range_of_camera.append(str('Camera_'+str(i)))
            lable = tk.Button(self.Chose_Device_Frame, text=text,command=lambda button_name=str('Camera_'+str(i)):self.show_ip_camera_chosed(button_name),
                                width=10, height=2, bg='green',cursor='hand2',
                                font="Helvetica 12 bold")
            lable.grid(column=int(i%3),row= int(i/3),padx = 10)
        
        # self.Device = tk.Label(self.Chose_Device_Frame, text="IP Adress",
        #                        width=10, height=1, bg='dark gray',
        #                        font="Helvetica 12 bold")
        # self.Device.grid(column=0, row=0, padx=12, pady=2, sticky=tk.EW)
        #set camera frame in main_frame
        self.Show_Capture_frame = tk.LabelFrame(self.main_frame)
        self.Show_Capture_frame.pack(side = 'top')
        self.Show_Capture_frame.pack_propagate(False)
        self.Show_Capture_frame.configure(width = self.main_frame.winfo_screenwidth() , text="show_camera",
                                            height=2*self.main_frame.winfo_screenheight()/2 -5,
                                            bg='dark gray', padx= 10, pady= 20,highlightbackground='white',highlightthickness=5)

        #get width of show_capture_frame
        # self.Show_Capture_frame_width = self.Show_Capture_frame.winfo_width()
        self.Frame_camera = tk.Frame(self.Show_Capture_frame)
        self.Frame_camera.pack(side = 'left')
        self.Frame_camera.pack_propagate(False)
        self.Frame_camera.grid_propagate(False)
        self.Frame_camera.configure(width = self.Show_Capture_frame.winfo_screenwidth()/2, height = self.Show_Capture_frame.winfo_screenwidth(),
                               bg = 'green',
                               highlightbackground='Black',
                               highlightthickness=10)

        self.Camera_lable_left = tk.Label(self.Frame_camera)
        self.Camera_lable_left.pack(side='left')
        self.Camera_lable_left.configure(bg='red')

        self.Camera_lable_right = tk.Label(self.Frame_camera)
        self.Camera_lable_right.pack(side='right')
        self.Camera_lable_right.configure(bg='red')
        # self.Frame_camera.pack(side='top')
        #set right frame in show capture frame
        self.Select_Model_Frame = tk.Frame(self.Show_Capture_frame)
        self.Select_Model_Frame.pack(side = 'right')
        self.Select_Model_Frame.pack_propagate(False)
        self.Select_Model_Frame.grid_propagate(False)
        self.Select_Model_Frame.configure(width =self.Show_Capture_frame.winfo_screenwidth() - self.Show_Capture_frame.winfo_screenwidth()/2 - 10, height = self.Show_Capture_frame.winfo_screenwidth(),
                               bg = 'dark gray',
                               highlightbackground='Black',
                               highlightthickness=10)
        
        self.label_text = "📁 Model 1"
        self.Model_1_Frame = tk.Button(self.Select_Model_Frame,width= 12, height= 6,command=lambda:self.on_label_click(1),
                                bg= 'gray' , text=self.label_text, font=('Arial', 12))
        self.Model_1_Frame.config(cursor="hand2",)
        self.Model_1_Frame.grid(column= 0 , row = 0 , padx=12, pady=12)
        # self.Model_1_Frame.bind("<Button-1>", self.on_label_click(1))

        label_text_2 = "📁 Model 2"
        self.Model_2_Frame = tk.Button(self.Select_Model_Frame,width= 12, height= 6,command=lambda:self.on_label_click(2),
                                bg= 'gray' , text=label_text_2, font=('Arial', 12))
        self.Model_2_Frame.config(cursor="hand2",)
        self.Model_2_Frame.grid(column= 1 , row = 0 , padx=12, pady=12)


    def on_label_click(self,nums):
        if nums == 1:
            self.models.append('IOT_SYSTEM\Model\keras_model_DTai.h5')
            self.class_names.append('IOT_SYSTEM\Lable\labels_DTai.txt')
        else:
            self.models.append('IOT_SYSTEM\Model\keras_model_Hand.h5')
            self.class_names.append('IOT_SYSTEM\Lable\labels_Hand.txt')
    def show_ip_camera(self,ip,port):
        if self.camera_url == None:
            self.camera_url = 'http://'+ip+':'+port+'/video'
            self.cap = cv2.VideoCapture(self.camera_url)
        elif self.cap_2_flag == True:
            self.camera_url_2 = 'http://'+ip+':'+port+'/video'
            self.cap_2 = cv2.VideoCapture(self.camera_url_2)
            print(self.camera_url_2)
        print(self.camera_url)
        self.stream_video()
    def show_ip_camera_chosed(self,url):
        if self.camera_url == None:
            for i in range(0,len(self.range_of_camera)):
                if self.range_of_camera[i] == url:
                    self.camera_url = self.list_device[i]
                    print('camera: ',self.range_of_camera[i])
                    break
            # self.camera_url = url
            print(self.camera_url)
            self.cap = cv2.VideoCapture(self.camera_url)
        else:
            for i in range(0,len(self.range_of_camera)):
                if self.range_of_camera[i] == url:
                    self.camera_url_2 = self.list_device[i]
                    print('camera: ',self.range_of_camera[i])
                    break
            # self.camera_url_2 = url
            print(self.camera_url_2)
            self.cap_2 = cv2.VideoCapture(self.camera_url_2)
        # if self.cap_2_flag == True:
        #     self.cap_2 = cv2.VideoCapture(self.camera_url)
        self.stream_video()

    def process_image(self):
        while True:
            if self.cap is not None:
                if self.cap_2_flag == False:
                    self.cap_2_flag = True
                ret, frame = self.cap.read()
                if ret:
                    # Resize hình ảnh về kích thước mong muốn (224, 224)
                    self.image = cv2.resize(frame, (224, 224))
                    self.image_pil = PILImage.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
                    # Đánh dấu cần cập nhật hình ảnh lên giao diện
                    self.image_pil = self.image_pil
                    self.update_image_flag = True
                    # self.update_image()  # Cập nhật hình ảnh lên giao diện
            if self.cap_2 is not None:
                ret2, frame2 = self.cap_2.read()
                if ret2:
                    # Resize hình ảnh về kích thước mong muốn (224, 224)
                    self.image_2 = cv2.resize(frame2, (224, 224))
                    self.image_pil_2 = PILImage.fromarray(cv2.cvtColor(self.image_2, cv2.COLOR_BGR2RGB))
                    # Đánh dấu cần cập nhật hình ảnh lên giao diện
                    self.image_pil_2 = self.image_pil_2
                    self.update_image_flag_2 = True
                    # self.update_image()  # Cập nhật hình ảnh lên giao diện
            
            if self.break_thread == True:
                break

            # time.sleep(0.1)
      
    def update_image(self):
        if self.update_image_flag:
            self.image_tk = ImageTk.PhotoImage(image=self.image_pil)
            self.Camera_lable_left.config(image=self.image_tk)
            self.update_image_flag = False  # Đặt lại cờ cập nhật hình ảnh
        if self.update_image_flag_2:
            self.image_tk_2 = ImageTk.PhotoImage(image=self.image_pil_2)
            self.Camera_lable_right.config(image=self.image_tk_2)
            self.update_image_flag_2 = False  # Đặt lại cờ cập nhật hình ảnh
    
    def Predict_image(self):
        while True:
            if len(self.models):
                model = load_model(self.models[0], compile=False)
                # Load the labelslabels.txt
                class_names = open(self.class_names[0], "r").readlines()
                image_array = np.array(self.image)

                prediction = model.predict(np.expand_dims(image_array, axis=0))
                index = np.argmax(prediction)
                class_name = class_names[index]
                confidence_score = prediction[0][index]
                print("Class:", class_name[2:], end="")
                print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            if len(self.models) == 2:
                model2 = load_model(self.models[1], compile=False)
                # Load the labelslabels.txt
                class_names2 = open(self.class_names[1], "r").readlines()
                image_array2 = np.array(self.image_2)

                prediction2 = model2.predict(np.expand_dims(image_array2, axis=0))
                index2 = np.argmax(prediction2)
                class_name2 = class_names2[index2]
                confidence_score2 = prediction2[0][index2]
                print("Class:", class_name2[2:], end="")
                print("Confidence Score:", str(np.round(confidence_score2 * 100))[:-2], "%")
            if self.break_thread == True:
                break

            time.sleep(0.5)
    
    def check_device(self):
        for check in self.list_device:
            if self.camera_url in check:
                self.check_device_flag = True
                break
        if self.check_device_flag == False:
            try:
                # Mở tệp văn bản để ghi thêm vào cuối tệp
                with open('IOT_SYSTEM\Save_Url\preparetion_url.txt', "a") as file:
                    # Ghi URL của camera vào cuối tệp
                    file.write(self.camera_url + "\n")  # Thêm "\n" để xuống dòng sau khi ghi URL
                print("Lưu URL vào tệp thành công.")
            except Exception as e:
                print("Đã xảy ra lỗi:", str(e))
        self.check_device_flag = True

    def stream_video(self):
        # Lên lịch cập nhật hình ảnh lên GUI sau 100ms trong luồng chính

        # Kiem tra chuoi co ton tai chua
        if self.check_device_flag == False:
            self.check_device()


        self.Frame_camera.after(10, self.stream_video)
        # self.update_image_flag_1 = True
        self.update_image()  # Cập nhật hình ảnh lên giao diện
        # self.update_image_2()  # Cập nhật hình ảnh lên giao diện


    def get_url(self):
        #get IP
        self.IP_input = self.Area_IP.get()
        print("Dữ liệu nhập vào:", self.IP_input)
        #get port
        self.Port_input = self.Area_Port.get()
        print("Dữ liệu nhập vào:", self.Port_input)
        self.show_ip_camera(self.IP_input,self.Port_input)

        # Private_Tasks.run_ip_camera.add_url(self.IP_input,self.Port_input)

    def read_text_file_to_list(self,file_path):
        try:
            # Mở file văn bản để đọc
            with open(file_path, "r") as file:
                # Đọc từng dòng của file và lưu vào danh sách
                self.lines_list = file.readlines()

            return self.lines_list
        except FileNotFoundError:
            print("File không tồn tại.")
        except Exception as e:
            print("Đã xảy ra lỗi:", str(e))
            return None


        
    def liquidBox(self, frame):
        # Liquid 1
        self.liquid1 = tk.Button(frame, text="LIQUID 1",
                                 bg="Chocolate", fg="White",
                                 font="Helvetica 16 bold")
        self.liquid1.grid(column=0, row=1, padx=60, pady=5)

        self.boxLiquid1 = tk.Label(frame, text="100%",
                                    width=6, height=1, bg="Chocolate",
                                    font="Helvetica 20 bold")
        self.boxLiquid1.grid(column=0, row=0, padx=60, pady=10, sticky=tk.NS)

        self.boxLiquid1_1 = Canvas(frame, width = 90, height=10, bg="white")
        self.boxLiquid1_1.create_rectangle(4, 52, 89, 161, fill="Chocolate")
        self.boxLiquid1_1.create_text(50,150,text="60%",font="Helvetica 14 bold")
        self.boxLiquid1_1.grid(column=0, row=0, padx=60, pady=10, sticky=tk.NS)
        
        # Liquid 2
        self.liquid2 = tk.Button(frame, text="LIQUID 2",
                                 bg="DodgerBlue", fg="White",
                                 font="Helvetica 16 bold")
        self.liquid2.grid(column=1, row=1, padx=60, pady=5)

        self.boxLiquid2 = tk.Label(frame, text="100%",
                                   width=6, height=1, bg="DodgerBlue",
                                   font="Helvetica 20 bold")
        self.boxLiquid2.grid(column=1, row=0, padx=60, pady=10, sticky=tk.NS)

        self.boxLiquid2_1 = Canvas(frame, width = 90, height=10, bg="white")
        self.boxLiquid2_1.create_rectangle(4, 52, 89, 161, fill="DodgerBlue")
        self.boxLiquid2_1.create_text(50,150,text="60%",font="Helvetica 14 bold")
        self.boxLiquid2_1.grid(column=1, row=0, padx=60, pady=10, sticky=tk.NS)

        # Liquid 3
        self.liquid3 = tk.Button(frame,text="LIQUID 3",
                                bg="Brown", fg="White",
                                font="Helvetica 16 bold")
        self.liquid3.grid(column=2, row=1, padx=60, pady=5)

        self.boxLiquid3 = tk.Label(frame, text="100%",
                               width=6, height=5, bg="Brown",
                               font="Helvetica 20 bold")
        self.boxLiquid3.grid(column=2, row=0, padx=60, pady=10, sticky=tk.NS)

        self.boxLiquid3_1 = Canvas(frame, width = 90, height=10, bg="white")
        self.boxLiquid3_1.create_rectangle(4, 52, 89, 161, fill="Brown")
        self.boxLiquid3_1.create_text(50,150,text="60%",font="Helvetica 14 bold")
        self.boxLiquid3_1.grid(column=2, row=0, padx=60, pady=10, sticky=tk.NS)

    def get_value(self):
        if int(self.ratioBox1.get()) + int(self.ratioBox2.get()) + int(self.ratioBox3.get()) != 0:
            self.inputRatio.append(self.ratioBox1.get())
            self.inputRatio.append(self.ratioBox2.get())
            self.inputRatio.append(self.ratioBox3.get())

            self.outputRatio.append(self.outputRatioBox1.get())
            self.outputRatio.append(self.outputRatioBox2.get())
            self.outputRatio.append(self.outputRatioBox3.get())
            
            if int(self.outputRatioBox1.get()) + int(self.outputRatioBox2.get()) + int(self.outputRatioBox3.get()) == 0:
                response = mbox.askquestion("Output setting", "Are you sure to not activate any relay for output?")
                if response == "yes":
                    print(self.inputRatio)
                    print(self.outputRatio)
                elif response == "no":
                    print("The user said no.")
                else:
                    print("The user canceled.")
            else:
                response = mbox.askquestion("Output setting", "Are you sure to enter these values?")
                if response == "yes":
                    print(self.inputRatio)
                    print(self.outputRatio)
                elif response == "no":
                    print("The user said no.")
                else:
                    print("The user canceled.")
        else:
            mbox.showwarning("Ratio", "Please setting ratio value!!!")

        

    def UI_Refresh(self):
        # self.UI_Set_Text(self.labelDistance1, self.dataModel.distance1_value)
        # self.UI_Set_Text(self.labelDistance2, self.dataModel.distance2_value)
        
        if self.page == page_Status.MANUAL_PAGE:
            for i in range(0, self.numButton):
                if self.dataModel.BUTTON_STATE[i] == True:
                    self.on_button[i].config(text="ON", bg="LimeGreen")
                    self.is_on[i] = True
                else:
                    self.on_button[i].config(text="OFF", bg="gold")
                    self.is_on[i] = False
        # if self.page == page_Status.AI_PAGE:
        #     self.stream_video()
        self.window.update()


    def UI_Set_Text(self,text_object, data):
        text_object.config(text="%.2f" % data)

    # define the click event of the toggle
    def toggle_button_click(self, number):
        # Determine is on or off
        if self.is_on[number]:
            self.on_button[number].config(text="OFF", bg="gold")
            self.is_on[number] = False
            # self.dataModel.relayController(number, state = 0)
            self.dataModel.BUTTON_STATE[number] = False
        else:
            self.on_button[number].config(text="ON", bg="gold")
            self.is_on[number] = True
            # self.dataModel.relayController(number, state = 1)
            self.dataModel.BUTTON_STATE[number] = True
        print("Button is" + str(number) + " clicked!!!")
        print(self.is_on[number])

    

