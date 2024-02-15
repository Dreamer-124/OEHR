#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/22 16:42
# @Author  : Phunsukh_Wangdu
# @FileName: Process_Nature.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/APPDREAMER?spm=1000.2115.3001.5343
import cv2
import numpy as np
from paddleocr import PaddleOCR, PPStructure, save_structure_res

#提取信息
def extract_nature(img):
    img=img[250:750, 240:1030]
    # cv2.imwrite('nature_1.jpg', img)

    #识别自然信息
    ocr=PaddleOCR(use_angle_cls = True,use_gpu= False, det= False) #使用CPU预加载，不用GPU
    result=ocr.ocr(img,cls=True)  #打开图片文件

    # 初始化信息列表
    extracted_info = {
        "病人ID": "",
        "住院号": "",
        "性别": "",
        "年龄": "",
        "婚姻状态": "",
        "姓名": ""
    }

    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line[1][0])
            if "男" in line[1][0]:
                extracted_info["性别"] = "男"
            elif "女" in line[1][0]:
                extracted_info["性别"] = "女"
            elif "龄" in line[1][0]:
                extracted_info["年龄"] = line[1][0].split("：")[1]
            elif "病人ID" in line[1][0]:
                extracted_info["病人ID"] = line[1][0].split("：")[1]
            elif "住院号" in line[1][0]:
                extracted_info["住院号"] = line[1][0].split("：")[1]
            elif "姻" in line[1][0]:
                extracted_info["婚姻状态"] = line[1][0].split("：")[1]
            elif "名" in line[1][0]:
                extracted_info["姓名"] = line[1][0].split("：")[1]
    print('===========================================')
    print("病人ID:", extracted_info["病人ID"])
    print("住院号:", extracted_info["住院号"])
    print("性别:", extracted_info["性别"])
    print("年龄:", extracted_info["年龄"])
    print("婚姻状态:", extracted_info["婚姻状态"])
    print("姓名:", extracted_info["姓名"])

    return extracted_info

# 示例用法
if __name__ == '__main__':
    # -----------------1.测试检测直线----------------- #
    image_path = 'Input/Nature/nature_0.png'
    save_dir = 'Ouput/Nature_Out'

    # 读取输入图片
    img = cv2.imread(image_path)
    extract_nature =extract_nature(img)
    # ---------------------------------------------- #