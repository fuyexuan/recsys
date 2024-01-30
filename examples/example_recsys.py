import os
import pandas as pd

from recsys.recsys import RecommenderSystem
def get_all_files_in_folder(folder_path, prefix=''):
    all_files = []

    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # 构建文件的完整路径
            file_path = os.path.join(root, file_name)
            # 检查文件名是否以指定前缀开头
            if file_name.startswith(prefix):
                # 将文件路径添加到列表中
                all_files.append(file_path)

    return all_files

folder_path = r'C:\Users\17235\Desktop\fyx\LLM-Trade\recsys_linux\0102测试结果'  # 替换为你的文件夹路径

# 获取文件夹及其所有子文件夹中以'AAA'开头的所有文件
file_list = get_all_files_in_folder(folder_path, prefix='不应拒答')

# 打印文件列表
for file_path in file_list:
    print(file_path)

df = pd.read_excel(file_path)

print(df.head(5))
print(len(df))

directory_path = folder_path

user_folders = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]

A_values = ['不应拒答', '侵害他人合法权益', '公正歧视', '商业违法违规', '应拒答', '特定安全需求', '违反社会主义核心价值观']

print(user_folders)

# 创建一个空的数据框来存储结果
result_df = pd.DataFrame()
# 遍历每个用户文件夹
for user_folder in user_folders:
    tmp_df = pd.DataFrame()
    # 构建当前用户文件夹的完整路径
    user_folder_path = os.path.join(directory_path, user_folder)

    # 获取当前用户文件夹下的文件路径（假设所有文件都是.xlsx文件）
    files_in_folder = [os.path.join(user_folder_path, file) for file in os.listdir(user_folder_path) if
                       file.endswith('.xlsx')]

    # 遍历每个文件
    for file_path in files_in_folder:
        # 读取文件
        df = pd.read_excel(file_path, usecols=['自动评判结果'])

        area_name = os.path.basename(file_path).split('+')[0]

        # 添加用户信息列
        df['userId'] = user_folders.index(user_folder)

        # 修改列名为 'rating'
        df = df.rename(columns={'自动评判结果': 'rating'})

        # 合并到结果数据框
        tmp_df = pd.concat([tmp_df, df], ignore_index=True)

    tmp_df = tmp_df.rename_axis('itemId')
    tmp_df = tmp_df.reset_index()
    result_df = pd.concat([result_df, tmp_df], ignore_index=True)

# 现在，result_df 中包含了所有用户文件夹中文件的数据，并包括了用户信息列 'user_id'
print(result_df)

#######    上面都是数据处理

recommender = RecommenderSystem(result_df)
recommender.fit()
rmse = recommender.evaluate()
print("Root Mean Squared Error on test set:", rmse)

user_id = 1
item_id = 1

predicted_rating = recommender.predict(user_id, item_id)
print(f"Predicted rating for user {user_id} and item {item_id}: {predicted_rating}")


user_id = 1
top_k_recommendations = recommender.recommend_top_k(user_id, k=5)

print(f"Top 5 recommendations for user {user_id}:")
for item_id, predicted_rating in top_k_recommendations:
    print(f"Item {item_id}: Predicted Rating = {predicted_rating}")