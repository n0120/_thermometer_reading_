import cv2
import datetime
import schedule
import time
import glob
import shutil

def record_camera():
    
        folder = "C:\_thermometer_reading_\_camera_\_"
        
        deviceid=1 # PCの場合は0が内蔵、1がwebカメラ
        capture = cv2.VideoCapture(deviceid)
        def job():
            ret, frame = capture.read()
            strdate=datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
            fname="image_" + strdate + ".jpg"
            cv2.imwrite(folder + fname, frame) 
            print(fname + " is created.")
        schedule.every(2).seconds.do(job)
        # 11秒間だけ実行
        t_end = time.time() + 11
        while time.time() < t_end:
            schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    record_camera()