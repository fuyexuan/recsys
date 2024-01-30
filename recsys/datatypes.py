# datatypes.py
import torch

class QualityAssessmentInput:
    def __init__(self, subjects, items, responses, text_features, num_subjects, num_items, weight_irt=0.7, weight_text=0.3):
        self.subjects = torch.tensor(subjects)
        self.items = torch.tensor(items)
        self.responses = torch.tensor(responses)
        self.text_features = text_features
        self.num_subjects = num_subjects
        self.num_items = num_items
        self.weight_irt = weight_irt
        self.weight_text = weight_text

class QualityAssessmentOutput:
    def __init__(self):
        self.irt_scores = None
        self.text_scores = None
        self.combined_scores = None
        self.combined_difficulty_scores = None
        self.top_k_diff = None
        self.combined_difficulty_scores_with_text = None
        self.top_k_diff_with_text = None

class IRTInput:
    def __init__(self, subjects, items, responses, num_subjects, num_items):
        self.subjects = subjects
        self.items = items
        self.responses = responses
        self.num_subjects = num_subjects
        self.num_items = num_items

class TextAnalysisInput:
    def __init__(self, text_features, num_items):
        self.text_features = text_features
        self.num_items = num_items


from dataclasses import dataclass, field
from typing import List

# @dataclass
# class IRTInput:
#     subjects: List[int]
#     items: List[int]
#     responses: List[int]
#     num_subjects: int
#     num_items: int
#
# @dataclass
# class TextAnalysisInput:
#     text_features: List[float]
#     num_items: int
#
# @dataclass
# class QualityAssessmentInput:
#     subjects: List[int]
#     items: List[int]
#     responses: List[int]
#     text_features: List[float]
#     num_subjects: int
#     num_items: int
#     weight_irt: float
#     weight_text: float
#
# @dataclass
# class IRTOutput:
#     theta: List[float]
#     b: List[float]
#
# @dataclass
# class TextAnalysisOutput:
#     fc_output: List[float]
#
# @dataclass
# class QualityAssessmentOutput:
#     irt_scores: List[float]
#     text_scores: List[float]
#     combined_scores: List[float]
#     combined_difficulty_scores: List[float]
