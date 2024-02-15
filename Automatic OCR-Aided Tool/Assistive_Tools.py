#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/19 9:32
# @Author  : Phunsukh_Wangdu
# @FileName: Assistive_Tools.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/APPDREAMER?spm=1000.2115.3001.5343
from docx import Document
import tempfile
import cv2
import pytesseract
import numpy as np
import os
import subprocess
import pandas as pd
import re

from paddleocr import PaddleOCR, draw_ocr
from paddleocr import PPStructure, save_structure_res
import layoutparser as lp
from bs4 import BeautifulSoup

# 将doc文件转换为docx文件
def convert_doc_to_docx(doc_path):
    docx_path = os.path.splitext(doc_path)[0] + ".docx"
    subprocess.run(["F:\LibreOffice\program\soffice", "--headless", "--convert-to", "docx", doc_path, "--outdir", os.path.dirname(doc_path)])
    return docx_path

# 解析HTML表格，将其转换为DataFrame
def parse_html_table(html):
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 找到表格标签
    table = soup.find('table')

    # 使用pandas读取HTML表格
    df = pd.read_html(str(table), header=0)[0]

    return df

# 对图片进行OCR识别
def recognize_text(image):
    # Resize the image
    # image = cv2.resize(image, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    # Convert the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use adaptive thresholding
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Use Tesseract OCR to recognize text
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(binary, config=custom_config, lang='chi_sim')

    return text

# 从图像中提取橙色区域
def extract_orange_region(image):
    # Convert the image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for the color orange
    lower_orange = np.array([12, 176, 253])
    upper_orange = np.array([14, 178, 255])

    # Create a mask for the color orange
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Get the orange region from the image
    orange_region = cv2.bitwise_and(image, image, mask=mask)

    return orange_region

# 显示图像
def display_image(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 从PP-Structure识别出来结果中提取html内容
def extract_Info_from_structure_result(structure_result):
    html_contents = []  # 用于存储识别后的html代码内容

    # 获取到识别后的html代码内容
    for line in structure_result:
        res = line.get('res')
        if res:
            if isinstance(res, dict):
                html_contents.append(res.get('text'))
                html_contents.append(res.get('html'))
                # print(res.get('html'))
            elif isinstance(res, list):
                for r in res:
                    if isinstance(r, dict):
                        html_contents.append(r.get('text'))
                        html_contents.append(r.get('html'))
                        # print(r.get('html'))
                    else:
                        continue

    return html_contents

# 更改识别出来的result中的文件名
def change_result_index(result, counter):
    # 修改result中的文件名
    for item in result:
        bbox = item.get('bbox', [])
        if bbox:
            # 将bbox更新为序号
            item['bbox'] = [counter]

    return result

# 对识别出来的时间进行格式化
def format_date_time(date_time):
    # 使用正则表达式提取和整合日期和时间
    pattern = r"(\d{4}-\d{1,2}-\d{1,2})(\d{1,2}:\d{1,2}:\d{1,2})"
    # formatted_string = re.sub(pattern, r"\1 \2", date_time)
    formatted_string = re.search(pattern, date_time)
    # 提取到的日期和时间
    date = formatted_string.group(1)
    time = formatted_string.group(2)

    # 整合日期和时间
    result_string = f"{date} {time}"

    print(result_string)

    return result_string

# 存储中文路径的图像
def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    return cv_img

if __name__ == '__main__':
    string = "出院方式2008-1-30:00:00出院方式：正常"
    format_date_time(string)
