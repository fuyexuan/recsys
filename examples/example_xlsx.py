import torch
from recsys.datatypes import QualityAssessmentInput
from recsys.quality_valuation import QualityAssessment
import pandas as pd
import os
import random

def get_intput(file_list):
    # 读取数据概括信息

    area_list = []
    model_list = []
    items_num_data = []
    text_features_data = []

    for file_path in file_list:
        file_name = os.path.basename(file_path)
        parts = file_name.split("+")
        df = pd.read_excel(file_path)

        # 提取A和B的值
        area_value = parts[0]
        model_value = parts[1]

        # 将值添加到相应的list中
        if area_value not in area_list:
            area_list.append(area_value)
            items_num_data.append(len(df.index))
        if model_value not in model_list:
            model_list.append(model_value)

    num_subjects = len(model_list)
    num_items = sum(items_num_data)

    # 打印结果
    print("A集合:", area_list)
    print("B集合:", model_list)
    print("题目数量:", items_num_data)
    print("num_subjects:", num_subjects)
    print("num_items:", num_items)

    # 读取数据具体信息

    prefix_item_sum = [0] * len(items_num_data)
    for i in range(len(items_num_data)-1):
        prefix_item_sum[i+1] = prefix_item_sum[i] + items_num_data[i]

    print("prefix_item_sum:", prefix_item_sum)

    subjects_data = []
    items_data = []
    responses_data = []


    for file_path in file_list:
        file_name = os.path.basename(file_path)
        parts = file_name.split("+")

        # 提取A和B的值
        area_value = parts[0]
        model_value = parts[1]

        # 读取文件
        df = pd.read_excel(file_path)

        df['自动评判结果'].replace({1: 0, 4: 1}, inplace=True)

        subject_id = model_list.index(model_value)
        area_id = area_list.index(area_value)

        # 将数据添加到相应的列表中
        subjects_data.extend([subject_id] * len(df))
        items_data.extend((df.index + prefix_item_sum[area_id]).tolist())
        responses_data.extend(df['自动评判结果'].tolist())
        text_features_data.extend(df['问题'].tolist())

    # 打印结果
    print("subjects_data: \n", subjects_data)
    print("items_data: \n", items_data)
    print("responses_data: \n", responses_data)
    print("text_features_data:", text_features_data)


    input = QualityAssessmentInput(subjects=subjects_data, items=items_data,
                                   responses=responses_data, text_features=text_features_data,
                                   num_subjects=num_subjects, num_items=num_items)

    return input

if __name__ == "__main__":
    file_list = ["C:/Users/17235/Desktop/fyx/LLM-Trade/recsys_linux/0102测试结果/万得-wind/不应拒答+wind+问答记录.xlsx",
                 "C:/Users/17235/Desktop/fyx/LLM-Trade/recsys_linux/0102测试结果/大智慧-xiaohui/不应拒答+xiaohui+问答记录.xlsx",
                 "C:/Users/17235/Desktop/fyx/LLM-Trade/recsys_linux/0102测试结果/大智慧-xiaohui/公正歧视+xiaohui+问答记录.xlsx",
                 ]

    quality_assessment_input = get_intput(file_list)

    quality_assessment_model = QualityAssessment(quality_assessment_input)

    quality_assessment_output = quality_assessment_model.run()

    print("Predicted Difficulties:", quality_assessment_output.combined_difficulty_scores)
    print("Top 10 Difficulties:", quality_assessment_output.top_k_diff)
    print("Predicted Difficulties with text:", quality_assessment_output.combined_difficulty_scores_with_text)
    print("Top 10 Difficulties with text:", quality_assessment_output.top_k_diff_with_text)
