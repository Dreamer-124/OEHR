#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/20 16:08
# @Author  : Phunsukh_Wangdu
# @FileName: Process_Check.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/APPDREAMER?spm=1000.2115.3001.5343
import cv2
import numpy as np
import os
import pandas as pd
import Assistive_Tools

from paddleocr import PPStructure, save_structure_res, PaddleOCR

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
    # 截取图片中的固定区域
    img0 = img0[268:915, 257:1260]

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
    cv2.imwrite('Unenhanced_And_Enhanced_Image/Check/check_enhance_9.jpg', img0)

    return img0
    # -------------------------------------------------------------------------------------------------------------------------- #

#提取主题信息
def extract_check_topic(img1):
    '''
    Function:
    提取检验主题信息

    param:
    img1: str -> 图片路径

    return:
    topic: str -> 检验主题信息
    '''
    # 截取图片中的固定区域
    img1 = img1[170:247, 240:1020]

    #识别主题信息
    ocr=PaddleOCR(use_angle_cls = True,use_gpu= False, det= False) #使用CPU预加载，不用GPU
    result=ocr.ocr(img1,cls=True)  #打开图片文件
    topic=""

    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            if("检验主题" in line[1][0]):
                topic=line[1][0].split("：")[1]

    print(topic)
    return topic

# 示例用法
if __name__ == '__main__':
    # -----------------1.测试检测直线----------------- #
    image_path = 'Input/Check_Error/check_error_0.png'

    # 读取输入图片
    img0 = cv2.imread(image_path)

    save_dir = 'Save/All_Table/'

    topic = extract_check_topic(img0)
    extracted_info = {'检查主题': topic}
    print(extracted_info)

    img0 = detect_lines_enhance(img0)

    table_engine = PPStructure(layout=False, show_log=True)
    result = table_engine(img0)

    Assistive_Tools.change_result_index(result, 16)
    save_structure_res(result, save_dir, "sample")

    file_path = 'Save/All_Table/' + "sample" + '/[' + str(16) + "]_0.xlsx"

    # 读取原有的 Excel 文件
    df = pd.read_excel(file_path)

    # 追加字典的键到原有行的后面
    data = {key: [value] for key, value in extracted_info.items()}
    df = pd.concat([df, pd.DataFrame(data)], axis=1)

    # 保存修改后的 Excel 文件
    df.to_excel(file_path, index=False)
    # ---------------------------------------------- #
