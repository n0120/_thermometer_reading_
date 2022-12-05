import cv2
import numpy as np
import statistics
import pyexiv2
import json
import glob
import shutil

def thermometer_reading(imga_path):

    # cv2.HoughLines() 関数

    img = cv2.imread(imga_path) # 画像の読み込み

    # 画像の大きさを取得

    height, width, channels = img.shape[:3]

    # 二値化

    threshold = 100

    ret,img_thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

    # エッジ画像へ変換(ハフ変換で直線を求めるため)

    edges = cv2.Canny(img_thresh,50,200,apertureSize = 3)

    cv2.imwrite('houghlines2.jpg',edges)

    cv2.imwrite('houghlines1.jpg',img_thresh)



    # 自動的に直線が2本となるパラメータを検出

    # minn：何点の点が並んでいたら、直線を引くか？のパラメーター値

    for m in range(10,161,1):

        lines = cv2.HoughLines(edges,1,np.pi/180,m)

        if lines is None:

            break

       # print(len(lines))



        if len(lines)==2:

            minn = m



    ##print('minn = ', minn)

    lines = cv2.HoughLines(edges,1,np.pi/180,minn)



    theta_t = [] # 原点から直線に向かって下した法線と、水平線との角度 (ラジアン) を格納する配列

    aa = []   # 直線の傾きを格納する配列

    bb = []   # 直線の切片を格納する配列



    i = 0



    for i in range(len(lines)):

       for rho,theta in lines[i]:

     ##       print('rho = ', rho)

     ##       print('theta = ', theta)

            theta_t.append(theta)

            a = np.cos(theta)

            b = np.sin(theta)

            x0 = a*rho

            y0 = b*rho

            x1 = int(x0 + 1000*(-b))

            y1 = int(y0 + 1000*(a))

            x2 = int(x0 - 1000*(-b))

            y2 = int(y0 - 1000*(a))

            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)



            # 2点を通る直線の式は、y = (y2-y1)/(x2-x1)x - (y2-y1)/(x2-x1)x1 + y1

            # 傾き a = (y2-y1)/(x2-x1) 、 b = y1 - (y2-y1)/(x2-x1)x1



            a0 = (y2 - y1) / (x2 - x1)

            b0 = y1 - (y2 - y1) / (x2 - x1)* x1



            aa.append(a0)

            bb.append(b0)



    # 針が画像の左上、左下、右上、右下 のどこにいるかを、2直線の交点の位置で判断し、角度の式を変更

    # なお、針の中心は画像の中心にあるとして、計算

    # 交点の式は、((b[1] - b[0]) / (a[0] - a[1]) , (a[0] * b[1] - b[0] * a[1]) / (a[0] - a[1]) )



    x_t = (bb[1] - bb[0]) / (aa[0] - aa[1])

    y_t = (aa[0] * bb[1] - bb[0] * aa[1]) / (aa[0] - aa[1])



    if x_t < width/2: # 針が左上か左下にいるとき

        theta_hor = statistics.mean(theta_t)*180/np.pi

    else: # 針が右上か右下にいるとき

        theta_hor = 270 - (90 - statistics.mean(theta_t)*180/np.pi)



    _thermometer_=(theta_hor-152.5)/2.75

    print(_thermometer_,"℃")

    ##cv2.imwrite('thermo_00_output.jpg',img)

    # 画像に_thermometer_の値を埋め込む
    dic_info = {"temperature": _thermometer_}
    json_str = json.dumps(dic_info)
    with pyexiv2.Image(imga_path) as img:
        img.modify_exif({'Exif.Image.ImageDescription': json_str})

def _camera_to_comp_():
    thermometer_path = glob.glob("C:\_thermometer_reading_\_camera_\*.jpg")
    print(thermometer_path)

    # フォルダ内のフォルの数を取得しておく
    thermometer_num = len(thermometer_path)

    # フォルダ内のファイルを全て処理する
    for i in range(thermometer_num):
        thermometer_path_one = thermometer_path[i]
        thermometer_reading(thermometer_path_one)
    
    # 画像を_comp_フォルダに移動させる
    for j in range(thermometer_num):
        thermometer_path_one = thermometer_path[j]
        shutil.move(thermometer_path_one, "C:\_thermometer_reading_\_comp_//")

if __name__ == '__main__':
    # imga_path = 'C:\_thermometer_reading_\_camera_\IMG_0387.jpg'
    # thermometer_reading(imga_path)
    # # 画像のjsonファイルをprintする
    # with open('thermo_00_output.json', 'r') as f:
    #     json_str = json.load(f)
    # print(json_str)
    
    _camera_to_comp_()