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


2. **推荐系统:**
   - 使用 `recsys.py` 实现基于ALS 协同过滤的推荐系统。
   - 参考 `example_recsys.py` 以了解如何使用推荐系统的示例。
     
## File Structure
- recsys: main code
- tests: test code
- examples: examples

## License
MIT
