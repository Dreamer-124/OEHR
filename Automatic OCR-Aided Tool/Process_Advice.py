#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/7 21:45
# @Author  : Phunsukh_Wangdu
# @FileName: Process_Advice.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/APPDREAMER?spm=1000.2115.3001.5343

import cv2
import numpy as np

from paddleocr import PPStructure, save_structure_res

# 将RGB转换为HSV
def RGB_Convert_HSV(r, g, b):
    '''
    Function: 将RGB转换为HSV

    param:
    r: int -> 红色通道值
    g: int -> 绿色通道值
    b: int -> 蓝色通道值

    return:
    h: int -> 色调
    s: int -> 饱和度
    v: int -> 明度
    '''
    # 创建一个包含单个像素的图像数组
    pixel = np.uint8([[[b, g, r]]])

    # 将RGB颜色值转换为HSV颜色空间
    hsv_pixel = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)

    # 提取HSV分量值
    h = hsv_pixel[0][0][0]
    s = hsv_pixel[0][0][1]
    v = hsv_pixel[0][0][2]

    return h, s, v

# 尝试使用颜色处理医嘱图片得到想要的区域
def process_advice(img_path):
    '''
    Function:
    处理医嘱图片

    param:
    img_path: str -> 图片路径

    return:
    None
    '''
    # 加载模型
    ocr_table = PPStructure(show_log=True)

    # 读取图片
    image = cv2.imread(img_path)

    # 将图片转换为HSV格式
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 设置指定颜色阈值区域
    lower_orange = np.array([0, 0, 210])
    upper_orange = np.array([129, 12, 210])

    # 根据阈值区域获取掩膜
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # 对原图像和掩膜进行位运算，得到结果区域图片（除了指定颜色区域外，像素值全为0）
    result = cv2.bitwise_and(image, image, mask=mask)

    # 显示结果区域图片
    cv2.imshow("result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # # 模型预测
    # result = ocr_table(img)
    # # 保存结果
    # save_structure_res(result, save_dir)

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
    # -------------------------------------------------1、使用HoughLinesP检测直线------------------------------------------------- #
    # # (整体直线检测效果不好，会有很多多余的直线被检测出来）
    # # 加载图片
    # img = cv2.imread(image_path)  # 注意路径中不能有中文
    #
    # # 截取图片中的固定区域
    # img = img[210:860, 290:1175]
    #
    # # 显示结果图片
    # cv2.imshow('result', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # # 转为灰度图
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # # 进行边缘检测
    # edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    #
    # # 进行霍夫变换，提取直线
    # lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    #
    # # 统计直线数量，判断是否有表格
    # if len(lines) > 10:
    #     print('图片中有表格')
    # else:
    #     print('图片中没有表格')
    #
    # # 绘制直线
    # for line in lines:
    #     x1, y1, x2, y2 = line[0]
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
    #
    # # 显示结果图片
    # cv2.imshow('result', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # -------------------------------------------------------------------------------------------------------------------------- #

    # -------------------------------------------------2、使用LSD算法检测直线------------------------------------------------- #
    # # 读取输入图片
    # img0 = cv2.imread(image_path)

    # 截取图片中的固定区域
    img0 = img0[210:860, 290:1175]

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
    # cv2.imwrite('Unenhanced_And_Enhanced_Image/Advice/advice_unenhance_8.jpg', img0)
    # cv2.imshow("LSD", img0)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return img0
    # -------------------------------------------------------------------------------------------------------------------------- #

# 示例用法
if __name__ == '__main__':
    # -----------------1.测试RGB转换为HSV----------------- #
    # # 获取HSV分量值
    # H, S, V = RGB_Convert_HSV(210, 210, 210)
    # print(f"H: {H}, S: {S}, V: {V}")
    # -------------------------------------------------- #

    # -----------------2.测试处理医嘱图片----------------- #
    # img_path = './Input/advice_0_Enhance.png'
    # # save_dir = 'Output'
    #
    # # 处理医嘱图片
    # process_advice(img_path)
    # ------------------------------------------------- #

    # -----------------3.测试检测直线----------------- #
    image_path = 'Input/Advice/advice_8.png'
    save_dir = 'Ouput/Advice_Out'
    image_path_1 = 'advice_8_Unenhance'

    # 读取输入图片
    img0 = cv2.imread(image_path)
    cropped_image = detect_lines_enhance(img0)

    table_engine = PPStructure(layout = False, show_log = True)
    result = table_engine(cropped_image)
    print('result: ', result)

    # save_structure_res(result, save_dir, image_path_1)
    # ---------------------------------------------- #