#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/20 9:26
# @Author  : Phunsukh_Wangdu
# @FileName: Process_Addmissions.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/APPDREAMER?spm=1000.2115.3001.5343
import tempfile
import cv2
import numpy as np
import os
import re
import subprocess
import layoutparser as lp
import pandas as pd
import Assistive_Tools

from docx import Document
from paddleocr import PPStructure, save_structure_res, PaddleOCR
from bs4 import BeautifulSoup

# 处理住院情况信息
import cv2
import numpy as np

from paddleocr import PPStructure, save_structure_res


# 把住院情况分成两个表进行处理，第一个表手动绘制，第二个表自动增强

# 对下方表格做直线检测增强
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
    img0 = img0[527:725, 263:1005]

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
    cv2.imwrite('Unenhanced_And_Enhanced_Image/Admissions/admissions_enhance_1.jpg', img0)
    # cv2.imshow("LSD", img0)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return img0
    # -------------------------------------------------------------------------------------------------------------------------- #


# 第一个表paddleocr识别
def extract_admissions(img):
    # 截取图片中的固定区域
    img = img[300:530, 240:1020]
    cv2.imwrite('admissions3.jpg', img)

    # 识别自然信息
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, det=False)  # 使用CPU预加载，不用GPU
    result = ocr.ocr(img, cls=True)  # 打开图片文件

    # 初始化信息列表
    extracted_info = {
        "入院日期": "",
        "出院日期": "",
        "入院病情": "",
        "入院科室": "",
        "出院科室": "",
        "过敏药物": "",
        "门诊诊断": "",
        "入院诊断": "",
        "门诊日期": "",
        "接诊日期": "",
        "诊断日期": ""
    }

    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line[1][0])
            if "入院日期" in line[1][0]:
                string_replaced = line[1][0].replace("：", ":")
                string_replaced = string_replaced.replace(" ", "")
                print(string_replaced)
                extracted_info["入院日期"] = Assistive_Tools.format_date_time(string_replaced)
            elif "出院日期" in line[1][0]:
                string_replaced = line[1][0].replace("：", ":")
                string_replaced = string_replaced.replace(" ", "")
                extracted_info["出院日期"] = Assistive_Tools.format_date_time(string_replaced)
            elif "入院病情" in line[1][0]:
                extracted_info["入院病情"] = line[1][0].split("：")[1]
            elif "入院科室" in line[1][0]:
                extracted_info["入院科室"] = line[1][0].split("：")[1]
            elif "出院科室" in line[1][0]:
                extracted_info["出院科室"] = line[1][0].split("：")[1]
            elif "过敏药物" in line[1][0]:
                string_replaced = line[1][0].replace("：", ":")
                index = string_replaced.find("过敏药物:")
                allergen = string_replaced[index + len("过敏药物:"):].strip()
                if allergen:
                    extracted_info["过敏药物"] = allergen
                else:
                    extracted_info["过敏药物"] = "无"
            elif "门诊诊断" in line[1][0]:
                extracted_info["门诊诊断"] = line[1][0].split("：")[1]
            elif "入院诊断" in line[1][0]:
                extracted_info["入院诊断"] = line[1][0].split("：")[1]
            elif "门诊日期" in line[1][0]:
                string_replaced = line[1][0].replace("：", ":")
                string_replaced = string_replaced.replace(" ", "")
                extracted_info["门诊日期"] = Assistive_Tools.format_date_time(string_replaced)
            elif "接诊日期" in line[1][0]:
                string_replaced = line[1][0].replace("：", ":")
                string_replaced = string_replaced.replace(" ", "")
                extracted_info["接诊日期"] = Assistive_Tools.format_date_time(string_replaced)
            elif "诊断日期" in line[1][0]:
                string_replaced = line[1][0].replace("：", ":")
                string_replaced = string_replaced.replace(" ", "")
                extracted_info["诊断日期"] = Assistive_Tools.format_date_time(string_replaced)

    return extracted_info


# 分别对两个表进行PPStruructure处理
# 示例用法
if __name__ == '__main__':
    # -----------------1.测试检测直线----------------- #
    image_path = 'Input/Admissions/admissions_1.png'
    save_dir = 'Ouput/Admissions_Out'
    image_path_1 = 'admissions_1_Enhance'

    # 读取输入图片
    img = cv2.imread(image_path)
    img0 = detect_lines_enhance(img)

    table_engine = PPStructure(layout = False, show_log = True)
    result = table_engine(img0)
    print('result:', result)
    save_structure_res(result, save_dir, image_path_1)

    extracted_info = extract_admissions(img)
    print(extracted_info)
    # ---------------------------------------------- #