import tempfile
import cv2
import numpy as np
import openpyxl
import os
import subprocess
import layoutparser as lp
import pandas as pd
import Assistive_Tools
import Process_Check
import Process_Addmissions
import Process_Diagnose
import Process_Advice
import Process_Nature

from openpyxl import Workbook
from docx import Document
from paddleocr import PPStructure, save_structure_res
from bs4 import BeautifulSoup

if __name__ == "__main__":
    dir_path = "D:\Desktop\研究生第一学期\SIGIR骨科数据集处理\骨科病历数据\原始病历\有入院记录划分\文件夹_3"  # 指定文件输入目录
    save_floder = "./Ouput/table"  # 保存结果的文件夹

    nature_info = 0
    admmision_info = 0
    diagnose_info = 0
    advice_info = 0
    check_info = 0
    other_info = 0
    counter = 0
    image_error_counter = 0

    # 遍历指定目录下的所有文件
    for root, dirs, files in os.walk(dir_path):
        # 报错处理
        try:
            for file in files:
                # 判断文件是否为.doc文件
                if file.endswith(".doc"):
                    doc_path = os.path.join(root, file)  # 获取文件的绝对路径

                    # 将.doc文件转换为.docx文件
                    docx_path = Assistive_Tools.convert_doc_to_docx(doc_path)
                    print("=====================当前处理.docx文件=========================")
                    print("docx_path: ", docx_path)

                    doc = Document(docx_path)  # 使用python-docx库读取.docx文件

                    # 遍历文档中的关联关系（rels），寻找类型为"image"的关联关系。当找到类型为"image"的关联关系时，获取关联目标（_target）和图像数据（blob）
                    for rel in doc.part.rels.values():
                        if "image" in rel.reltype:
                            image_part = rel._target
                            image_data = image_part.blob

                            # 使用tempfile库创建一个临时文件，将图像数据写入临时文件中，并获取临时文件的文件名。
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
                                temp.write(image_data)
                                temp_filename = temp.name

                            image = cv2.imread(temp_filename)  # 取临时文件中的图像数据，并将其存储在image变量中。

                            print("=====================对图片进行第一次识别=========================")
                            table_engine = PPStructure(show_log=False)  # 初始化引擎
                            result_1 = table_engine(image)  # 进行表格识别
                            # print('result_1: ', result_1)

                            # 保存识别结果
                            result_2 = []
                            result_2 = Assistive_Tools.extract_Info_from_structure_result(result_1)  # 提取识别结果
                            # print('result_2: ', result_2)
                            filtered_list = [item for item in result_2 if item is not None]  # 过滤掉None
                            print('filtered_list: ', filtered_list)

                            # 处理自然信息
                            if all(any(substring in item for item in filtered_list) for substring in ['通信地址', '邮政编码']):
                                print('=====================当前处理病例首页-自然信息=========================')
                                nature_info += 1
                                extract_nature = Process_Nature.extract_nature(image)
                                print('extract_nature: ', extract_nature)

                                data = {key: [value] for key, value in extract_nature.items()}

                                df = pd.DataFrame(data)
                                print('Save/All_Table/' + os.path.basename(doc_path).split('.')[0] + '/[' + str(counter + 1) + "]_0.xlsx")
                                os.makedirs('Save/All_Table/' + os.path.basename(doc_path).split('.')[0], exist_ok=True)  # 创建文件夹（如果不存在）
                                df.to_excel('Save/All_Table/'+ os.path.basename(doc_path).split('.')[0] + '/[' + str(counter + 1) + "]_0.xlsx", index=False)

                            # 处理住院情况
                            elif all(any(substring in item for item in filtered_list) for substring in ['所在科室', '转向科室']):
                                print('=====================当前处理病例首页-住院情况=========================')
                                admmision_info += 1
                                save_dir = 'Save/All_Table/'
                                img0 = Process_Addmissions.detect_lines_enhance(image)

                                table_engine = PPStructure(layout=False, show_log=True)
                                result = table_engine(img0)

                                # print('result:', result)
                                Assistive_Tools.change_result_index(result, counter + 1)
                                save_structure_res(result, save_dir, os.path.basename(doc_path).split('.')[0])

                                extracted_info = Process_Addmissions.extract_admissions(image)
                                print(extracted_info)

                                file_path = 'Save/All_Table/'+ os.path.basename(doc_path).split('.')[0] + '/[' + str(counter + 1) + "]_0.xlsx"

                                # 读取原有的 Excel 文件
                                df = pd.read_excel(file_path)

                                # 追加字典的键到原有行的后面
                                data = {key: [value] for key, value in extracted_info.items()}
                                df = pd.concat([df, pd.DataFrame(data)], axis=1)

                                # 保存修改后的 Excel 文件
                                df.to_excel(file_path, index=False)

                            # 处理诊断史
                            elif all(any(substring in item for item in filtered_list) for substring in ['诊断类别', '诊断序号']):
                                print('======================当前处理病例首页-诊断史==========================')
                                diagnose_info += 1
                                save_dir = 'Save/All_Table/'
                                cropped_image = Process_Diagnose.detect_lines_enhance(image)

                                table_engine = PPStructure(layout=False, show_log=True)
                                result = table_engine(cropped_image)

                                Assistive_Tools.change_result_index(result, counter + 1)
                                save_structure_res(result, save_dir, os.path.basename(doc_path).split('.')[0])

                            # 处理医嘱
                            elif all(any(substring in item for item in filtered_list) for substring in ['频次', '途径']):
                                print('===========================当前处理医嘱==============================')
                                advice_info += 1
                                if all(any(substring in item for item in filtered_list) for substring in ['显示范围']):
                                    print('当前医嘱图片异常，需要进行存储，不处理！')

                                    cv2.imencode('.png', image)[1].tofile('Save/Advice_Error/' + os.path.basename(doc_path).split('.')[0] + '_' + str(counter + 1) + '.png')  # 保存当前异常医嘱图片

                                    # 保存当前异常医嘱图片的路径和位置
                                    with open("error_advice_log.txt", "a") as file_error:
                                        file_error.write("Error: " + "当前医嘱图片异常，需要进行存储，不处理！" + " in " + os.path.join(root, file) + " 的第 " + str(counter+1) + " 张图片" + "\n")

                                    counter += 1
                                    continue
                                else:
                                    print('当前医嘱图片正常，进行处理！')
                                    save_dir = 'Save/All_Table/'
                                    cropped_image = Process_Advice.detect_lines_enhance(image)

                                    table_engine = PPStructure(layout=False, show_log=True)
                                    result = table_engine(cropped_image)

                                    Assistive_Tools.change_result_index(result, counter + 1)
                                    save_structure_res(result, save_dir, os.path.basename(doc_path).split('.')[0])

                            # 处理检查
                            elif all(any(substring in item for item in filtered_list) for substring in ['项目类别', '结果']):
                                print('===========================当前处理检查==============================')
                                check_info += 1
                                save_dir = 'Save/All_Table/'
                                img0 = Process_Check.detect_lines_enhance(image)

                                table_engine = PPStructure(layout=False, show_log=True)
                                result = table_engine(img0)

                                # print('result:', result)
                                Assistive_Tools.change_result_index(result, counter + 1)
                                save_structure_res(result, save_dir, os.path.basename(doc_path).split('.')[0])

                                topic = Process_Check.extract_check_topic(image)
                                extracted_info = {'检查主题':topic}
                                print(extracted_info)

                                file_path = 'Save/All_Table/'+ os.path.basename(doc_path).split('.')[0] + '/[' + str(counter + 1) + "]_0.xlsx"

                                # 读取原有的 Excel 文件
                                df = pd.read_excel(file_path)

                                # 追加字典的键到原有行的后面
                                data = {key: [value] for key, value in extracted_info.items()}
                                df = pd.concat([df, pd.DataFrame(data)], axis=1)

                                # 保存修改后的 Excel 文件
                                df.to_excel(file_path, index=False)

                            # 处理其他信息
                            else:
                                # 应对其他异常情况
                                print('============================其他不处理===============================')
                                other_info += 1
                                continue

                            counter += 1  # 计数器，用于记录当前处理的图片数量，同时也用于命名当前处理的图片以及存储的.xlsx文件名字

                    print('文件' + file + '中有' + str(nature_info) + '个自然信息，' + str(admmision_info) + '个住院情况，' + str(diagnose_info) + '个诊断史，' + str(advice_info) + '个医嘱，' + str(check_info) + '个检查，' + str(other_info) + '个其他信息。')
                    nature_info = 0
                    admmision_info = 0
                    diagnose_info = 0
                    advice_info = 0
                    check_info = 0
                    other_info = 0
                    counter = 0

        except Exception as e:
            # 捕获异常并记录错误信息
            error_message = str(e)
            with open("error_all_log.txt", "a") as file_error:
                file_error.write("Error: " + error_message + " in " + os.path.join(root, file) + "\n")
            continue

