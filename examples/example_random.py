from recsys.datatypes import QualityAssessmentInput
from recsys.quality_valuation import QualityAssessment

import random

import pandas as pd

# 随机初始化样例

num_subjects = 10
num_items = 100

subjects_data = [random.randint(0, num_subjects-1) for _ in range(100)]
items_data = [random.randint(0, num_items-1) for _ in range(100)]
responses_data = [random.randint(0, 1) for _ in range(100)]

# 通过 randn 方法创建 text_features 数据
text_features_data = ["random text" for _ in range(num_items)]

# 打印列表数据
print("subjects_data 列表:", subjects_data)
print("items_data 列表:", items_data)
print("responses_data 列表:", responses_data)
print("text_features_data 列表:", text_features_data)

# 运行算法

quality_assessment_input = QualityAssessmentInput(subjects=subjects_data, items=items_data, responses=responses_data, text_features=text_features_data, num_subjects=num_subjects, num_items=num_items)

quality_assessment_model = QualityAssessment(quality_assessment_input)

quality_assessment_output = quality_assessment_model.run()

print("Predicted Difficulties:", quality_assessment_output.combined_difficulty_scores)
print("Top 10 Difficulties:", quality_assessment_output.top_k_diff)
print("Predicted Difficulties with text:", quality_assessment_output.combined_difficulty_scores_with_text)
print("Top 10 Difficulties with text:", quality_assessment_output.top_k_diff_with_text)

sorted_data = sorted(quality_assessment_output.combined_difficulty_scores_with_text, key=lambda x: x[0])
print("Predicted Difficulties with text:", sorted_data)


# 创建 DataFrame
df = pd.DataFrame(quality_assessment_output.combined_difficulty_scores_with_text, columns=['题号', '难度', '题目内容'])

# 存储到 Excel 文件
df.to_excel('output.xlsx', index=False)

