#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/20 19:41
# @Author  : Phunsukh_Wangdu
# @FileName: Process_Diagnose.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/APPDREAMER?spm=1000.2115.3001.5343
import cv2
import numpy as np

from paddleocr import PPStructure, save_structure_res

# 对图像做直线检测增强
def detect_lines_enhance(img0):
    '''
    Function:
    检测图片中的直线

    param:
    image_path: str -> 图片路径

    return:
    None
    '''

    # -------------------------------------------------1、使用LSD算法检测直线------------------------------------------------- #
    # # 读取输入图片
    # img0 = cv2.imread(image_path)

    # 截取图片中的固定区域
    img0 = img0[305:725, 260:1006]

    # 将彩色图片转换为灰度图片
    img = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

    # 创建一个LSD对象
    lsd = cv2.createLineSegmentDetector(0)

    # 执行检测结果
    dlines = lsd.detect(img)

    # 绘制检测结果
    for dline in dlines[0]:
        x0 = int(round(dline[0][0]))
        y0 = int(round(dline[0][1]))
        x1 = int(round(dline[0][2]))
        y1 = int(round(dline[0][3]))
        cv2.line(img0, (x0, y0), (x1, y1), (255, 125, 255), 1, cv2.LINE_AA)
        # cv2.line(img0, (x0, y0), (x1, y1), (0, 255, 0), 1, cv2.LINE_AA)

    # 显示并保存结果
    cv2.imwrite('Unenhanced_And_Enhanced_Image/Diagnose/diagnose_enhance_0.jpg', img0)
    # cv2.imshow("LSD", img0)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return img0
    # -------------------------------------------------------------------------------------------------------------------------- #

# 示例用法
if __name__ == '__main__':
    # -----------------1.测试检测直线----------------- #
    image_path = 'Input/Diagnose/diagnose_0.png'
    save_dir = 'Ouput/Diagnose_Out'
    image_path_1 = 'Diagnose_0_Enhance'

    # 读取输入图片
    img0 = cv2.imread(image_path)
    cropped_image = detect_lines_enhance(img0)

    table_engine = PPStructure(layout = False, show_log = True)
    result = table_engine(cropped_image)

    save_structure_res(result, save_dir, image_path_1)
    # ---------------------------------------------- #