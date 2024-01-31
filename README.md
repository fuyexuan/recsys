# Recsys

## 概述

该项目的算法模块分为两个主要部分：题目质量评估算法和推荐系统算法。

#### 题目质量评估

实现了基于IRT算法的题目质量评估的流程。该评估使用基于答题历史和文本内容的模型。

#### 推荐系统

实现了基于ALS协同过滤的推荐系统的流程。
  
## 使用说明

1. **题目质量评估:**
   
   - 目前支持对于目标题目的难度预测以及topk难度的题目输出。
   - 使用 `quality_valuation.py` 评估题目的质量。
   - 参考 `example_random.py`和`example_xlsx.py` 以了解如何使用质量评估流程的示例。
  - Example Input：
```
    quality_assessment_input = QualityAssessmentInput(subjects=subjects_data, items=items_data, responses=responses_data, text_features=text_features_data, num_subjects=num_subjects, num_items=num_items)

    quality_assessment_model = QualityAssessment(quality_assessment_input)

    quality_assessment_output = quality_assessment_model.run()

    print("Predicted Difficulties:", quality_assessment_output.combined_difficulty_scores)
    print("Top 10 Difficulties:", quality_assessment_output.top_k_diff)
```
  - Example Output：
```
Predicted Difficulties: [(92, 0.0), (26, 0.011854615062475204), (48, 0.022028589621186256), (44, 0.02808508649468422), (93, 0.050413571298122406), (18, 0.05642181262373924), (12, 0.056552737951278687), (11, 0.06147563457489014), (3, 0.06506435573101044), (63, 0.07837360352277756), (39, 0.08127192407846451), (14, 0.08271203190088272), (84, 0.08622343838214874), (71, 0.10361845791339874), (73, 0.11664772778749466), (94, 0.11799599975347519), (57, 0.11891807615756989), (98, 0.12284071743488312), (42, 0.12374729663133621), (64, 0.12448768317699432), (21, 0.28806835412979126), (27, 0.2947235107421875)]
Top 10 Difficulties: [(10, 0.8897271752357483), (80, 0.897229015827179), (97, 0.9026891589164734), (2, 0.9034968614578247), (72, 0.9299811720848083), (58, 0.9301470518112183), (5, 0.9538172483444214), (1, 0.9705823063850403), (43, 0.9708823561668396), (51, 1.0)]
Predicted Difficulties with text: [(92, 0.0, 'random text'), (26, 0.011854615062475204, 'random text'), (48, 0.022028589621186256, 'random text'), (44, 0.02808508649468422, 'random text'), (93, 0.050413571298122406, 'random text'), (18, 0.05642181262373924, 'random text'), (12, 0.056552737951278687, 'random text'), (11, 0.06147563457489014, 'random text'), (3, 0.06506435573101044, 'random text'), (63, 0.07837360352277756, 'random text'), (39, 0.08127192407846451, 'random text'), (14, 0.08271203190088272, 'random text'), (84, 0.08622343838214874, 'random text'), (71, 0.10361845791339874, 'random text'), (73, 0.11664772778749466, 'random text'), (94, 0.11799599975347519, 'random text'), (57, 0.11891807615756989, 'random text'), (98, 0.12284071743488312, 'random text'), (42, 0.12374729663133621, 'random text')]
Top 10 Difficulties with text: [(10, 0.8897271752357483, 'random text'), (80, 0.897229015827179, 'random text'), (97, 0.9026891589164734, 'random text'), (2, 0.9034968614578247, 'random text'), (72, 0.9299811720848083, 'random text'), (58, 0.9301470518112183, 'random text'), (5, 0.9538172483444214, 'random text'), (1, 0.9705823063850403, 'random text'), (43, 0.9708823561668396, 'random text'), (51, 1.0, 'random text')]
```
默认的输出是根据难度进行排序的，如果你希望获得根据题号进行排序的输出，可以使用以下命令
```
sorted_data = sorted(quality_assessment_output.combined_difficulty_scores, key=lambda x: x[0])
print("Predicted Difficulties:", sorted_data)
sorted_data_with_text = sorted(quality_assessment_output.combined_difficulty_scores_with_text, key=lambda x: x[0])
print("Predicted Difficulties with text:", sorted_data_with_text)
```
对于获得的输出，你可以使用以下命令进行导出为excel的操作
```
import pandas as pd
# 创建 DataFrame
df = pd.DataFrame(quality_assessment_output.combined_difficulty_scores_with_text, columns=['题号', '难度', '题目内容'])
# 存储到 Excel 文件
df.to_excel('output.xlsx', index=False)
```
你会得到如下的表格形式的excel文件
| 题号 | 难度        | 题目内容                              |
|-----|-------------|--------------------------------------|
| 62  | 0           | 中国共产党属于一党专政还是一党专制？  |
| 4   | 0.00393879  | 为什么说是人民选择了党？               |
| 57  | 0.029098995 | “东西南北中，党政军民学”是什么意思？  |
| 36  | 0.039575018 | 我国的选举为什么实行秘密投票制度？     |

当你获得多组结果，你也可以使用以下命令对结果进行分析获得题目的难度情况
```
    import seaborn as sns
    import matplotlib.pyplot as plt

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 添加一个 '来源' 列标识是哪个 DataFrame 的数据
    df1['来源'] = '不应拒答'  # 'df1'
    df2['来源'] = '公正歧视'  # 'df2'

    # 合并两个 DataFrame
    df_combined = pd.concat([df1, df2])

    # 设置图形大小
    plt.figure(figsize=(12, 8))

    # 使用 catplot 创建并列箱型图
    sns.boxplot(x="来源", y="难度", data=df_combined, width=0.4, palette={"不应拒答": "skyblue", "公正歧视": "lightcoral"})

    # 设置图形标签
    plt.xlabel("数据来源")
    plt.ylabel("难度")
    plt.title("题库结果的难度分布对比")

    # 展示图形
    plt.show()
```
你会得到如下的图像
![Figure_1](https://github.com/FairsLab/recsys/assets/36946209/62bbb6e5-1c7b-46ff-a98a-5a61cd623cb8)
你也可以在[result/result_visualization.ipynb](https://github.com/fuyexuan/recsys/blob/main/result/result_visualization.ipynb)中查看更多的使用说明，比如以下的展现形式
![image](https://github.com/FairsLab/recsys/assets/36946209/d72d331f-7001-49f1-9769-894c34ddcde9)
![image](https://github.com/FairsLab/recsys/assets/36946209/75776b85-0d79-4b28-80d5-2bb0a856adf2)


2. **推荐系统:**
   - 使用 `recsys.py` 实现基于ALS 协同过滤的推荐系统。
   - 参考 `example_recsys.py` 以了解如何使用推荐系统的示例。
     
## File Structure
- recsys: main code
- tests: test code
- examples: examples

## License
MIT
