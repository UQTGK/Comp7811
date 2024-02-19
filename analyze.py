import os
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import spacy
from textblob import TextBlob
import numpy as np


def extract_json_objects(text):
    lines = text.splitlines()
    objs = []
    start_index = None

    for i, line in enumerate(lines):
        # 如果当前行只有一个开始大括号，那么这是一个新的JSON对象的开始
        if line.strip() == '{':
            start_index = i
        # 如果当前行只有一个结束大括号，并且我们之前找到了一个开始大括号，那么这是一个JSON对象的结束
        elif line.strip() == '}' and start_index is not None:
            obj_str = '\n'.join(lines[start_index:i + 1])
            objs.append(obj_str)
            start_index = None

    return objs


def is_negative_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity < -0.4


def review_check_with_nlp():
    keywords = ["phishing", "sensitive data", "fake", "redirect", "cannot",
                "uninstall", "watch out", "spy", "malware", "hijack", "virus",
                "spyware", "scam", "adware", "malicious", "don’t install", "do not install"]

    directory_path = 'F:/PycharmProjects/crawling/results'
    files_with_keywords = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                json_objects = extract_json_objects(content)
                for obj_str in json_objects:
                    try:
                        entry = json.loads(obj_str)
                        review = entry.get('review', '').lower()

                        # 使用spaCy进行NLP处理
                        doc = nlp(review)
                        lemmatized_review = ' '.join([token.lemma_ for token in doc])

                        # 判断评论的情感以及是否包含关键词
                        if is_negative_sentiment(lemmatized_review):
                            for keyword in keywords:
                                if keyword in lemmatized_review:
                                    files_with_keywords.append(filename)
                                    print(filename)
                                    break
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in {filename} for object: {obj_str}")

    count = len(set(files_with_keywords))
    print(count)
    for file in set(files_with_keywords):
        print(file)


def reviewcheck():
    # 定义你的词库
    keywords = ["phishing", "sensitive data", "fake", "redirect", "bad", "cannot", "uninstall", "watch out", "spy",
                "malware", "hijack", "virus", "spyware", "scam", "adware",
                "malicious", "cannot uninstall", "can’t uninstall", "don’t install", "do not install"]

    # 指定你的JSON文件所在的目录
    directory_path = 'F:/PycharmProjects/crawling/results'

    # 存储包含关键词的文件名
    files_with_keywords = []

    # 遍历目录中的每个文件
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                json_objects = extract_json_objects(content)
                for obj_str in json_objects:
                    try:
                        entry = json.loads(obj_str)
                        review = entry.get('review', '')
                        for keyword in keywords:
                            if keyword in review:
                                files_with_keywords.append(filename)
                                break
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in {filename} for object: {obj_str}")
                        # 打印错误发生时的上下文
                        start = max(0, obj_str.find("review") - 30)
                        end = min(len(obj_str), obj_str.find("review") + 1024)
                        print("Context:", obj_str[start:end])

    count = 0
    # 输出包含关键词的文件名
    for file in set(files_with_keywords):
        count += 1
        print(file)

    print(count)


def extract_rating(rating_text):
    return int(rating_text.split('：')[1][0])


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%B %d, %Y").date()
    except ValueError:
        print(f"Error: Unable to parse date from '{date_str}'.")
        return None


def parse_zoho_date(date_str):
    if date_str.endswith('S'):
        date_str = date_str[:-1].strip()
    try:
        return datetime.strptime(date_str, "%b %d, %Y").date()
    except ValueError:
        print(f"Error: Unable to parse date from '{date_str}'.")
        return None


# def detect_anomalies(ratings):
#     TRAIN_RATIO = 0.8
#     # 将评分转换为DataFrame，并进行时间排序
#     df = pd.DataFrame(ratings, columns=['date', 'rating'])
#     df = df.set_index('date').sort_index()
#
#     # 使用STL进行时间序列分解
#     stl = STL(df['rating'], seasonal=3, period=2, robust=True)
#     result = stl.fit()
#
#     # 获取残差部分
#     residuals = result.resid
#
#     # 训练数据的残差
#     train_residuals = residuals[:int(len(residuals) * TRAIN_RATIO)]
#
#     # 如果最近的残差与训练数据的标准偏差差异很大，返回True
#     if residuals[-1] < train_residuals.mean() - 2 * train_residuals.std():
#         return True
#     return False

def detect_anomalies_google(ratings):
    if np.mean([rating[1] for rating in ratings]) >= 4.5:
        return False
    TRAIN_RATIO = 0.8

    # 将评分转换为DataFrame，并进行时间排序
    df = pd.DataFrame(ratings, columns=['date', 'rating'])
    df = df.set_index('date').sort_index()

    # 计算指数移动平均和标准偏差
    span_size = 10  # 用于控制指数移动平均线的平滑程度，可以根据您的数据进行调整
    ema = df['rating'].ewm(span=span_size).mean()
    rolling_std = df['rating'].rolling(window=span_size).std()

    # 设定上下异常界限
    upper_bound = ema + 2*rolling_std
    lower_bound = ema - 2*rolling_std

    # 使用训练数据计算阈值
    last_train_idx = int(len(df) * TRAIN_RATIO)
    training_upper_bound = upper_bound[:last_train_idx].mean()
    training_lower_bound = lower_bound[:last_train_idx].mean()

    # 绘制图形
    df['rating'].plot(label='Actual Ratings')
    ema.plot(label=f'Exponential Moving Average (span={span_size})')
    upper_bound.plot(label='Upper Bound', linestyle='--')
    lower_bound.plot(label='Lower Bound', linestyle='--')
    plt.legend()
    plt.show()

    # 获取后20%的数据
    test_data = df.iloc[last_train_idx:]
    avg_latest_20_percent = test_data['rating'].mean()

    # 检查后20%评分的平均值是否超出界限
    if avg_latest_20_percent > training_upper_bound or avg_latest_20_percent < training_lower_bound:
        return True

    return False

def detect_anomalies_zoho(ratings):
    if np.mean([rating[1] for rating in ratings]) >= 4.5:
        return False
    TRAIN_RATIO = 0.8

    # 将评分转换为DataFrame，并进行时间排序
    df = pd.DataFrame(ratings, columns=['date', 'rating'])
    df = df.set_index('date').sort_index()

    # 计算指数移动平均和标准偏差
    span_size = 10  # 用于控制指数移动平均线的平滑程度，可以根据您的数据进行调整
    ema = df['rating'].ewm(span=span_size).mean()
    rolling_std = df['rating'].rolling(window=span_size).std()

    # 设定上下异常界限
    upper_bound = ema + 2*rolling_std
    lower_bound = ema - 2*rolling_std

    # 使用训练数据计算阈值
    last_train_idx = int(len(df) * TRAIN_RATIO)
    training_upper_bound = upper_bound[:last_train_idx].mean()
    training_lower_bound = lower_bound[:last_train_idx].mean()

    # 绘制图形
    df['rating'].plot(label='Actual Ratings')
    ema.plot(label=f'Exponential Moving Average (span={span_size})')
    upper_bound.plot(label='Upper Bound', linestyle='--')
    lower_bound.plot(label='Lower Bound', linestyle='--')
    plt.legend()
    plt.show()

    # 获取后20%的数据
    test_data = df.iloc[last_train_idx:]
    avg_latest_20_percent = test_data['rating'].mean()

    # 检查后20%评分的平均值是否超出界限
    if avg_latest_20_percent > training_upper_bound or avg_latest_20_percent < training_lower_bound:
        return True

    return False



def gradecheck():
    # 关键词和其他参数
    MIN_RATINGS = 50

    directory_path = 'D:/PycharmProjects/crawling/crwal_data/results'

    ratings_dict = {}

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                json_objects = extract_json_objects(content)
                for obj_str in json_objects:
                    try:
                        entry = json.loads(obj_str)
                        review_time = parse_date(entry.get('reviewTime', ''))
                        grade = int(entry.get('grade', '').split(" ")[-2])
                        if review_time:
                            ratings_dict.setdefault(filename, []).append((review_time, grade))
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in {filename} for object: {obj_str}")

    suspected_files = []

    # 对于每个文件，检查评分异常
    for filename, ratings in ratings_dict.items():
        if len(ratings) >= MIN_RATINGS:
            if detect_anomalies_google(ratings):
                suspected_files.append(filename)

    print("Files with suspected anomalies:")
    for file in suspected_files:
        print(file)


def zoho_gradecheck():
    # 关键词和其他参数
    MIN_RATINGS = 50

    directory_path = 'D:/PycharmProjects/crawling/zoho_results'

    ratings_dict = {}

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                for entry in data:
                    try:
                        review_time = parse_zoho_date(entry.get('Review Time', ''))
                        grade = int(entry.get('Review Rating'))
                        if grade == 0:
                            continue
                        if review_time:
                            ratings_dict.setdefault(filename, []).append((review_time, grade))
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in {filename} for object: {entry}")

    suspected_files = []

    # 对于每个文件，检查评分异常
    for filename, ratings in ratings_dict.items():
        if len(ratings) >= MIN_RATINGS:
            if detect_anomalies_zoho(ratings):
                suspected_files.append(filename)

    print("Files with suspected anomalies:")
    for file in suspected_files:
        print(file)


def classify_review(review):
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in review:
                return category
    return "other"


def review_check_with_nlp_category():
    directory_path = 'F:/PycharmProjects/crawling/results'
    app_categories = {}

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                json_objects = extract_json_objects(content)
                for obj_str in json_objects:
                    try:
                        entry = json.loads(obj_str)
                        review = entry.get('review', '').lower()
                        doc = nlp(review)
                        lemmatized_review = ' '.join([token.lemma_ for token in doc])

                        if is_negative_sentiment(lemmatized_review):
                            category = classify_review(lemmatized_review)
                            # 只为app分配一次类别，不覆盖已经分配的类别
                            if filename not in app_categories:
                                app_categories[filename] = category
                                print(f"File: {filename} | Category: {category}")
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in {filename} for object: {obj_str}")

    # 汇总并打印每个类别的apps
    for category, filenames in app_categories.items():
        print(f"\nCategory: {category}\n{'-' * 20}")
        unique_files = set(filenames)
        for file in unique_files:
            print(file)
        print(f"Total Apps in {category}: {len(unique_files)}")


def review_check_with_nlp_THRESHOLD():
    NEGATIVE_REVIEW_THRESHOLD = 0.20
    directory_path = 'D:/PycharmProjects/crawling/crwal_data/results'
    app_categories = {}
    app_review_counts = {}  # 新增一个字典来跟踪每个应用的评论数
    app_negative_review_counts = {}  # 新增一个字典来跟踪每个应用的负面评论数
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                json_objects = extract_json_objects(content)
                app_review_counts[filename] = len(json_objects)
                if app_review_counts[filename] <= 5:
                    continue
                category_scores = {cat: 0 for cat in CATEGORIES}
                for obj_str in json_objects:
                    try:
                        entry = json.loads(obj_str)
                        review = entry.get('review', '').lower()
                        doc = nlp(review)
                        lemmatized_review = ' '.join([token.lemma_ for token in doc])
                        if is_negative_sentiment(lemmatized_review):
                            for category, keywords in CATEGORIES.items():
                                for keyword in keywords:
                                    category_scores[category] += lemmatized_review.count(keyword)
                            app_negative_review_counts[filename] = app_negative_review_counts.get(filename, 0) + 1
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in {filename} for object: {obj_str}")
                # 只为app分配一次类别，不覆盖已经分配的类别
                # 根据得分选择最合适的类别
                sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
                best_category = sorted_categories[0][0]
                if sorted_categories[0][1] == 0:  # 如果最高得分为0，则类别为"other"
                    best_category = "other"
                try:
                    if filename not in app_categories and app_negative_review_counts[filename] \
                            / app_review_counts[filename] >= NEGATIVE_REVIEW_THRESHOLD:
                        app_categories[filename] = best_category
                        print(f"File: {filename} | Category: {best_category}")
                except:
                    continue
    # 创建一个反向映射
    category_to_files = {}
    for filename, category in app_categories.items():
        if category not in category_to_files:
            category_to_files[category] = []
        category_to_files[category].append(filename)

    # 汇总并打印每个类别的apps
    # 使用新的映射来输出结果
    for category, filenames in category_to_files.items():
        print(f"\nCategory: {category}\n{'-' * 20}")
        unique_files = set(filenames)
        for file in unique_files:
            print(file)
        print(f"Total Apps in {category}: {len(unique_files)}")

def modify_review_check_with_nlp_THRESHOLD():
    NEGATIVE_REVIEW_THRESHOLD = 0.17
    directory_path = 'D:/PycharmProjects/crawling/crwal_data/results'
    app_categories = {}
    app_review_counts = {}  # 新增一个字典来跟踪每个应用的评论数
    app_negative_review_counts = {}  # 新增一个字典来跟踪每个应用的负面评论数
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                json_objects = extract_json_objects(content)
                app_review_counts[filename] = len(json_objects)
                if app_review_counts[filename] <= 5:
                    continue
                category_scores = {cat: 0 for cat in CATEGORIES}
                for obj_str in json_objects:
                    try:
                        entry = json.loads(obj_str)
                        review = entry.get('review', '').lower()
                        doc = nlp(review)
                        lemmatized_review = ' '.join([token.lemma_ for token in doc])
                        if is_negative_sentiment(lemmatized_review) and contains_category_keywords(lemmatized_review):
                            for category, keywords in CATEGORIES.items():
                                for keyword in keywords:
                                    category_scores[category] += lemmatized_review.count(keyword)
                            app_negative_review_counts[filename] = app_negative_review_counts.get(filename, 0) + 1
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in {filename} for object: {obj_str}")
                # 只为app分配一次类别，不覆盖已经分配的类别
                # 根据得分选择最合适的类别
                sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
                best_category = sorted_categories[0][0]
                if sorted_categories[0][1] == 0:  # 如果最高得分为0，则类别为"other"
                    best_category = "other"
                try:
                    if filename not in app_categories and app_negative_review_counts[filename] \
                            / app_review_counts[filename] > NEGATIVE_REVIEW_THRESHOLD:
                        app_categories[filename] = best_category
                        print(f"File: {filename} | Category: {best_category}")
                except:
                    continue
    # 创建一个反向映射
    category_to_files = {}
    for filename, category in app_categories.items():
        if category not in category_to_files:
            category_to_files[category] = []
        category_to_files[category].append(filename)

    # 汇总并打印每个类别的apps
    # 使用新的映射来输出结果
    for category, filenames in category_to_files.items():
        print(f"\nCategory: {category}\n{'-' * 20}")
        unique_files = set(filenames)
        for file in unique_files:
            print(file)
        print(f"Total Apps in {category}: {len(unique_files)}")

def zoho_review_check_with_nlp_THRESHOLD():
    NEGATIVE_REVIEW_THRESHOLD = 0.15
    directory_path = 'D:/PycharmProjects/crawling/zoho_results'
    app_categories = {}
    app_review_counts = {}  # 新增一个字典来跟踪每个应用的评论数
    app_negative_review_counts = {}  # 新增一个字典来跟踪每个应用的负面评论数

    for filename in os.listdir(directory_path):
        print(filename)
        with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
            data = json.load(file)
            app_review_counts[filename] = len(data)
            if app_review_counts[filename] <= 5:
                continue
            category_scores = {cat: 0 for cat in CATEGORIES}
            for obj_str in data:
                try:
                    review = obj_str.get('Review Content', '').lower()
                    grade = int(obj_str.get('Review Rating'))
                    if grade == 0:
                        continue
                    doc = nlp(review)
                    lemmatized_review = ' '.join([token.lemma_ for token in doc])
                    if is_negative_sentiment(lemmatized_review) and contains_category_keywords(lemmatized_review):
                        for category, keywords in CATEGORIES.items():
                            for keyword in keywords:
                                category_scores[category] += lemmatized_review.count(keyword)
                        app_negative_review_counts[filename] = app_negative_review_counts.get(filename, 0) + 1
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in {filename} for object: {obj_str}")
            # 只为app分配一次类别，不覆盖已经分配的类别
            # 根据得分选择最合适的类别
            sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
            best_category = sorted_categories[0][0]
            if sorted_categories[0][1] == 0:  # 如果最高得分为0，则类别为"other"
                best_category = "other"
            try:
                if filename not in app_categories and \
                        app_negative_review_counts[filename] / app_review_counts[filename] >= NEGATIVE_REVIEW_THRESHOLD:
                    app_categories[filename] = best_category
                    print(f"File: {filename} | Category: {best_category}")
            except:
                continue
    # 创建一个反向映射
    category_to_files = {}
    for filename, category in app_categories.items():
        if category not in category_to_files:
            category_to_files[category] = []
        category_to_files[category].append(filename)

    # 汇总并打印每个类别的apps
    # 使用新的映射来输出结果
    for category, filenames in category_to_files.items():
        print(f"\nCategory: {category}\n{'-' * 20}")
        unique_files = set(filenames)
        for file in unique_files:
            print(file)
        print(f"Total Apps in {category}: {len(unique_files)}")

def contains_category_keywords(lemmatized_review):
    """检查是否包含任何分类中的关键词"""
    CATEGORIES = {
        "malicious": ["phishing", "phishe", "malware", "hijack", "redirect", "can’t uninstall", "bad",
                      "can not uninstall",
                      "uninstall", "spyware", "virus", "scam", "malicious", "spy", "steal", "stealing",
                      "sensitive data", "fake", "stealer", "steals", "stolen", "hijack", "hijacking", "hijacked",
                      "hijacker", "cheat", "cheating", "cheated", "fraud", "risk"],
        "adware": ["adware", "ad", "ads", "advert", "advertising", "advertise", "advertisement", "advertising",
                   "advertizing", "advertize", "advertizing", "advertized", "advertised"],
        "unusable": ["can not use", "doesn't work", "not working", "not work", "didn't work", "don’t install",
                     "do not install", "can't use"]
    }
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in lemmatized_review:
                return True
    return False


if __name__ == '__main__':
    # 分类关键词
    CATEGORIES = {
        "malicious": ["phishing", "phishe", "malware", "hijack", "redirect", "can’t uninstall", "bad",
                      "can not uninstall",
                      "uninstall", "spyware", "virus", "scam", "malicious", "spy", "steal", "stealing",
                      "sensitive data", "fake", "stealer", "steals", "stolen", "hijack", "hijacking", "hijacked",
                      "hijacker", "cheat", "cheating", "cheated", "fraud", "risk"],
        "adware": ["adware", "ad", "ads", "advert", "advertising", "advertise", "advertisement", "advertising",
                   "advertizing", "advertize", "advertizing", "advertized", "advertised"],
        "unusable": ["can not use", "doesn't work", "not working", "not work", "didn't work", "don’t install",
                     "do not install", "can't use"]
    }
    # 加载spaCy模型
    nlp = spacy.load("en_core_web_sm")
    # review = "I can't uninstall this app. It's stealing my data and it is phishing. didn't work"
    # doc = nlp(review)
    # lemmatized_review = ' '.join([token.lemma_ for token in doc])
    modify_review_check_with_nlp_THRESHOLD()
    gradecheck()
    zoho_review_check_with_nlp_THRESHOLD()
    zoho_gradecheck()
