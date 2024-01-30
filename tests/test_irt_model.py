import unittest
import torch
import numpy as np
from quality_valuation import IRTModel  # Replace with the actual import path

class TestOneParamLogModel(unittest.TestCase):
    def setUp(self):
        self.num_subjects = 200
        self.num_items = 20

    def test_model_creation(self):
        model = IRTModel(self.num_subjects, self.num_items)
        self.assertIsInstance(model, IRTModel)

    def test_model_fit_predict(self):
        # Generate synthetic data for testing
        np.random.seed(42)
        models_data = torch.randint(0, self.num_subjects, (1000,))
        items_data = torch.randint(0, self.num_items, (1000,))
        responses_data = torch.randint(0, 2, (1000,))

        # Fit the model
        irt_model = IRTModel(self.num_subjects, self.num_items)
        irt_model.fit(models_data, items_data, responses_data)

        # Generate data for prediction
        subjects_to_predict = torch.randint(0, self.num_subjects, (10,))
        items_to_predict = torch.randint(0, self.num_items, (10,))

        # Predictions
        predictions = irt_model.predict(subjects_to_predict, items_to_predict)
        self.assertIsInstance(predictions, torch.Tensor)
        self.assertEqual(len(predictions), 10)

    def test_evaluate_accuracy(self):
        # Generate synthetic data for testing
        np.random.seed(42)
        models_data = torch.randint(0, self.num_subjects, (100,))
        items_data = torch.randint(0, self.num_items, (100,))
        responses_data = torch.randint(0, 2, (100,))

        # Fit the model
        irt_model = IRTModel(self.num_subjects, self.num_items)
        irt_model.fit(models_data, items_data, responses_data)

        # Generate data for evaluation
        subjects_to_evaluate = torch.randint(0, self.num_subjects, (50,))
        items_to_evaluate = torch.randint(0, self.num_items, (50,))
        true_responses_to_evaluate = torch.randint(0, 2, (50,))

        # Evaluate accuracy
        accuracy = irt_model.evaluate_accuracy(subjects_to_evaluate, items_to_evaluate, true_responses_to_evaluate)
        self.assertIsInstance(accuracy, float)
        self.assertGreaterEqual(accuracy, 0.0)
        self.assertLessEqual(accuracy, 1.0)

if __name__ == '__main__':
    unittest.main()
