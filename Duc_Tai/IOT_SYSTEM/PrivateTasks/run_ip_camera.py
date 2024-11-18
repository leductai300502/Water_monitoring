import cv2

def run_ip_camera(camera_url):
    cap = cv2.VideoCapture(camera_url)
    print("run camera")
    while True:
        # Đọc frame từ IP camera
        ret, frame = cap.read()

        if not ret:
            print("Không thể đọc frame từ IP camera.")
            break

        # Hiển thị video từ IP camera
        cv2.imshow('IP Camera', frame)

        # Để thoát vòng lặp, nhấn 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng các tài nguyên
    cap.release()
    cv2.destroyAllWindows()

def add_url(ip,port):
        # Điền địa chỉ IP hoặc URL của camera trong tham số camera_url
        camera_url = 'http://'+ip+':'+port+'/video'
        print(camera_url)
        run_ip_camera(camera_url)
