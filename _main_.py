import cv2
import numpy as np
import statistics
import datetime
import schedule
import time
import glob
import shutil
from _recording_from_camera_ import record_camera
from _thermometer_reading_ import thermometer_reading, _camera_to_comp_
import pyexiv2

def main():

    # カメラから画像を取得（11秒間）
    # record_camera()
    # print("record_camera is done.")

    # _camera_フォルダにある画像を温度計認証を行い、認証済みの画像を_comp_フォルダへ移動
    _camera_to_comp_()

    # _comp_フォルダにあるすべての画像のexif情報にある"temperature"、printする
    comp_path = glob.glob("C:\_thermometer_reading_\_comp_\*.jpg")
    for i in comp_path:
        with pyexiv2.Image(i) as img:
            print(img.read_exif()['Exif.Image.ImageDescription'])

if __name__ == "__main__":
    main()