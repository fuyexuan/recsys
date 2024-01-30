import torch
from torch.optim import Adam
from recsys.datatypes import QualityAssessmentOutput

class IRTModel:
    # model for assessment based on answer history
    def __init__(self, num_subjects, num_items):
        self.num_subjects = num_subjects
        self.num_items = num_items
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialize_model()

    def _initialize_model(self):
        self.theta = torch.randn(self.num_subjects, requires_grad=True, device=self.device)
        self.b = torch.randn(self.num_items, requires_grad=True, device=self.device)

    def fit(self, subjects, items, responses, num_epochs=1000, lr=0.1):
        optimizer = Adam([self.theta, self.b], lr=lr)
        responses_float = responses.float()

        for epoch in range(num_epochs):
            logits = self.theta[subjects] - self.b[items]
            probs = torch.sigmoid(logits)
            loss = -torch.distributions.Bernoulli(probs=probs).log_prob(responses_float).sum()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if epoch % 100 == 0:
                print(f"[IRT Epoch {epoch}] Loss: {loss.item():.4f}")

        print(f"[IRT Epoch {epoch}] Loss: {loss.item():.4f}")

    def predict(self, subjects, items):
        logits = self.theta[subjects] - self.b[items]
        output = torch.sigmoid(logits)
        return output


class TextAnalysisModel:
    def __init__(self, num_items):
        self.num_items = num_items
        self.fc = torch.nn.Linear(num_items, 1)

    def fit(self, text_features, num_epochs=1000, lr=0.01):
        pass

    def predict(self, text_features):
        output = torch.squeeze(self.fc(text_features), dim=1)
        return output


class QualityAssessment:
    def __init__(self, input_data):
        self.irt_model = IRTModel(input_data.num_subjects, input_data.num_items)
        self.text_model = TextAnalysisModel(input_data.num_items)
        self.weight_irt = input_data.weight_irt
        self.weight_text = input_data.weight_text
        self.input = input_data
        self.output = QualityAssessmentOutput()

    def run(self):
        self.fit(self.input.subjects, self.input.items, self.input.responses, self.input.text_features)

        self.predict_item_difficulty(self.input.items)
        self.get_top_k_item_difficulty()
        # self.predict_score()

        return self.output

    def fit(self, subjects, items, responses, text_features, num_epochs_irt=1000, num_epochs_text=1000, lr_irt=0.1, lr_text=0.01):
        # Fit IRT model
        self.irt_model.fit(subjects, items, responses, num_epochs=num_epochs_irt, lr=lr_irt)

        # Fit Text Analysis model
        self.text_model.fit(text_features, num_epochs=num_epochs_text, lr=lr_text)

    def predict_item_difficulty(self, items):
        # 获取每个项目的难度得分
        # irt_difficulty_scores = -self.irt_model.b[items].detach().cpu().numpy()
        irt_difficulty_scores = -self.irt_model.b[items].detach()

        text_difficulty_scores = torch.zeros_like(self.irt_model.b[items], dtype=torch.float32, device=self.irt_model.device)

        # text_difficulty_scores = np.zeros_like(irt_difficulty_scores, dtype=np.float32)

        combined_difficulty_scores = (self.weight_irt * irt_difficulty_scores) + (self.weight_text * text_difficulty_scores)

        normalized_difficulty_scores = self.normalize_scores(combined_difficulty_scores)

        # return normalized_difficulty_scores.tolist()

        # Create a list of tuples (item_index, difficulty_score)
        score_pairs = list(zip(items.tolist(), normalized_difficulty_scores.tolist()))

        # Sort the list based on difficulty scores
        sorted_score_pairs = sorted(score_pairs, key=lambda x: x[1])

        self.output.combined_difficulty_scores = sorted_score_pairs
        self.output.combined_difficulty_scores_with_text = self.add_text_features_to_pairs(sorted_score_pairs)

        return sorted_score_pairs

    def get_top_k_item_difficulty(self, k=10):
        items = torch.arange(self.input.num_items)
        item_difficulties = self.predict_item_difficulty(items)
        self.output.top_k_diff = item_difficulties[-k:]
        self.output.top_k_diff_with_text = self.add_text_features_to_pairs(self.output.top_k_diff)

        return self.output.top_k_diff



    def predict_score(self, subjects, items, text_features):
        # Get IRT scores
        irt_scores = self.irt_model.predict(subjects, items)
        print("irt_scores.shape")
        print(irt_scores.shape)

        # Get Text Analysis scores
        text_scores = self.text_model.predict(text_features)
        print("text_scores.shape")
        print(text_scores.shape)

        # Combine results
        combined_scores = self.combine_scores(irt_scores, text_scores)

        return combined_scores.tolist()

    def combine_scores(self, irt_scores, text_scores):
        # Combine results using weighted average
        combined_scores = (self.weight_irt * irt_scores) + (self.weight_text * text_scores)
        return combined_scores

    def normalize_scores(self, scores):
        # Assuming scores is a 1D tensor
        normalized_scores = (scores - scores.min()) / (scores.max() - scores.min())
        return normalized_scores

    def add_text_features_to_pairs(self, sorted_score_pairs):
        # Assuming self.input.text_features is a tensor
        text_features = self.input.text_features

        # Iterate through each tuple in sorted_score_pairs and add text features
        updated_score_pairs = []
        for item_index, difficulty_score in sorted_score_pairs:
            text_feature = text_features[item_index]
            updated_score_pairs.append((item_index, difficulty_score, text_feature))

        return updated_score_pairs

#