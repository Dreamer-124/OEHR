#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/2/5 17:57
# @Author  : Phunsukh_Wangdu
# @FileName: Time_SHA.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/APPDREAMER?spm=1000.2115.3001.5343
import pandas as pd
import hashlib
import random

# 读取Excel文件
df = pd.read_excel('Save/All_Table/2008-付士友00174102/[6]_0.xlsx')  # 替换为你的Excel文件路径

# 选择要读取的行数（示例中选择第一行）
row_index = 0

# 读取指定行的内容
row_data = df.iloc[row_index].values.tolist()

# 将内容转换为字符串
row_string = ''.join(str(value) for value in row_data)

# 对内容进行SHA256加密
sha256_hash = hashlib.sha256(row_string.encode()).hexdigest()

print("SHA256 Hash:", sha256_hash)

# 随机采样
# sample_3 = random.sample(sha256_hash, 3)
# sample_2 = random.sample(sha256_hash, 2)
# sample_1 = random.sample(sha256_hash, 1)

sample_3 = sha256_hash[0:3]  # 采集字符串中索引为0到2的字符（共3个字符）
sample_2 = sha256_hash[32:34]  # 采集字符串中索引为0到1的字符（共2个字符）
sample_1 = sha256_hash[63]  # 采集字符串中索引为0的字符（共1个字符）

# 打印采样结果
print("Sample of 3 positions:", sample_3)
print("Sample of 2 positions:", sample_2)
print("Sample of 1 position:", sample_1)

# 转换采样结果为整数
sample_3_int = int(''.join(sample_3), 16)
sample_2_int = int(''.join(sample_2), 16)
sample_1_int = int(''.join(sample_1), 16)

# 打印采样结果
print("Sample of 3 positions (as integers):", sample_3_int)  # 年
print("Sample of 2 positions (as integers):", sample_2_int)  # 日
print("Sample of 1 position (as integers):", sample_1_int)  # 月

# 生成时间
year = 3000 + sample_3_int % 1000 + 1

month_31 = [1, 3, 5, 7, 8, 10, 12]
month_30 = [4, 6, 9, 11]

# 判断是否为闰年
if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    # 生成闰年的月份和日期
    month = sample_1_int % 12 + 1
    if month in month_31:
        day = sample_2_int % 31 + 1
    elif month in month_30:
        day = sample_2_int % 30 + 1
    else:
        # 闰年二月份的日期
        day = sample_2_int % 29 + 1
else:
    # 生成平年的月份和日期
    month = sample_1_int % 12 + 1
    if month in month_31:
        day = sample_2_int % 31 + 1
    elif month in month_30:
        day = sample_2_int % 30 + 1
    else:
        # 平年二月份的日期
        day = sample_2_int % 28 + 1

# 打印生成的带有格式的时间
print("Generated date:", f"{year}-{month:02d}-{day:02d}")
