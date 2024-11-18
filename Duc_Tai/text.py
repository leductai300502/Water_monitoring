import threading
import cv2
import numpy as np
from PIL import Image as PILImage, ImageTk
from tensorflow.keras.models import load_model

class YourClassName:
    def __init__(self):
        self.frame = None
        self.image_pil = None
        self.image_tk = None
        self.processing_thread = threading.Thread(target=self.process_image)
        self.processing_thread.start()

    def process_image(self):
        while True:
            if self.cap is not None:
                ret, frame = self.cap.read()
                if ret:
                    # Resize hình ảnh về kích thước mong muốn (224, 224)
                    image = cv2.resize(frame, (224, 224))
                    image_pil = PILImage.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                    # Đánh dấu cần cập nhật hình ảnh lên giao diện
                    self.image_pil = image_pil
                    self.update_image_flag = True

    def update_image(self):
        if self.update_image_flag:
            self.image_tk = ImageTk.PhotoImage(image=self.image_pil)
            self.Camera_lable.config(image=self.image_tk)
            self.update_image_flag = False  # Đặt lại cờ cập nhật hình ảnh

    def stream_video(self):
        # Lên lịch cập nhật hình ảnh lên GUI sau 100ms trong luồng chính
        self.Frame_camera.after(100, self.stream_video)
        self.update_image()  # Cập nhật hình ảnh lên giao diện

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
