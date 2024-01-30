import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt

class RecommenderSystem:
    def __init__(self, input_data, test_size=0.2, k=10, max_iter=100, lambda_=0.1, tol=0.001):
        self.input_data = input_data
        self.test_size = test_size
        self.k = k
        self.max_iter = max_iter
        self.lambda_ = lambda_
        self.tol = tol
        self.R = None
        self.P = None
        self.Q = None

    def als(self, R, k, max_iter=100, lambda_=0.1, tol=0.001):
        """
        使用交替最小二乘法实现ALS矩阵分解

        参数:
        - R: 用户-物品评分矩阵，未评分的地方用0填充
        - k: 隐含特征的数量
        - max_iter: 最大迭代次数
        - lambda_: 正则化参数
        - tol: 收敛阈值

        返回:
        - P: 用户特征矩阵
        - Q: 物品特征矩阵
        """

        m, n = R.shape  # m是用户数量，n是物品数量

        # 初始化用户和物品特征矩阵
        P = np.random.rand(m, k)
        Q = np.random.rand(n, k)

        # 迭代优化
        for _ in range(max_iter):
            # 优化用户特征矩阵P
            for i in range(m):
                # 找到用户i已评分的物品索引
                rated_items = np.where(R[i, :] > 0)[0]
                if len(rated_items) == 0:
                    continue

                # 提取用户i已评分的物品特征和评分
                Q_rated = Q[rated_items, :]
                R_rated = R[i, rated_items]

                # 使用最小二乘法优化用户i的特征
                P[i, :] = np.linalg.solve(np.dot(Q_rated.T, Q_rated) + lambda_ * np.eye(k), np.dot(Q_rated.T, R_rated))

            # 优化物品特征矩阵Q
            for j in range(n):
                # 找到评分物品j的用户索引
                rated_users = np.where(R[:, j] > 0)[0]
                if len(rated_users) == 0:
                    continue

                # 提取物品j已评分的用户特征和评分
                P_rated = P[rated_users, :]
                R_rated = R[rated_users, j]

                # 使用最小二乘法优化物品j的特征
                Q[j, :] = np.linalg.solve(np.dot(P_rated.T, P_rated) + lambda_ * np.eye(k), np.dot(P_rated.T, R_rated))

            # 计算误差
            R_hat = np.dot(P, Q.T)
            error = np.sum((R - R_hat) ** 2)
            if error < tol:
                break

        return P, Q

    def load_data(self):
        # 加载数据集，这里使用MovieLens数据集
        data = self.input_data
        return data

    def prepare_data(self):
        data = self.load_data()

        # 创建用户-物品评分矩阵
        user_item_matrix = data.pivot(index='userId', columns='itemId', values='rating').fillna(0)

        # 划分训练集和测试集
        train_data, test_data = train_test_split(user_item_matrix, test_size=self.test_size, random_state=42)

        return train_data.values, test_data.values

    def fit(self):
        # 准备数据
        train_data, _ = self.prepare_data()

        # 运行ALS算法
        self.P, self.Q = self.als(train_data, k=self.k, max_iter=self.max_iter, lambda_=self.lambda_, tol=self.tol)

    def predict(self, user_id, item_id):
        # 预测用户对物品的评分
        user_index = user_id - 1  # 用户ID从1开始，数组索引从0开始
        item_index = item_id - 1  # 物品ID从1开始，数组索引从0开始

        if self.P is None or self.Q is None:
            raise ValueError("Model not trained. Call fit() first.")

        if user_index >= self.P.shape[0] or item_index >= self.Q.shape[0]:
            raise ValueError("User or item index out of bounds.")

        predicted_rating = np.dot(self.P[user_index, :], self.Q[item_index, :])
        return predicted_rating

    def evaluate(self):
        _, test_data = self.prepare_data()

        # 遍历测试集，计算均方根误差
        predictions = []
        ground_truth = []
        for i in range(test_data.shape[0]):
            for j in range(test_data.shape[1]):
                if test_data[i, j] > 0:
                    user_id = i + 1
                    item_id = j + 1
                    predicted_rating = self.predict(user_id, item_id)
                    predictions.append(predicted_rating)
                    ground_truth.append(test_data[i, j])

        rmse = sqrt(mean_squared_error(ground_truth, predictions))
        return rmse

    def recommend_top_k(self, user_id, k=5):
        if self.P is None or self.Q is None:
            raise ValueError("Model not trained. Call fit() first.")

        user_index = user_id - 1  # 用户ID从1开始，数组索引从0开始

        if user_index >= self.P.shape[0]:
            raise ValueError("User index out of bounds.")

        # 计算用户对所有物品的预测评分
        all_items = np.arange(1, self.Q.shape[0] + 1)
        predicted_ratings = np.dot(self.P[user_index, :], self.Q.T)

        # 找到Top K的物品索引
        top_k_indices = np.argsort(predicted_ratings)[::-1][:k]

        # 获取Top K的物品ID和对应的预测评分
        top_k_items = all_items[top_k_indices]
        top_k_ratings = predicted_ratings[top_k_indices]

        return list(zip(top_k_items, top_k_ratings))

