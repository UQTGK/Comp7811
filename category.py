import json
import os
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import spacy
from textblob import TextBlob
import numpy as np




# Function to categorize an add-on based on its permissions
def categorize_add_on(permissions):
    categories = []

    for category, patterns in permission_patterns.items():
        for pattern in patterns:
            if any(pattern in permission for permission in permissions):
                categories.append(category)
                break  # No need to check other patterns for this category

    return categories
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
    return analysis.sentiment.polarity < -0.5

def review_check_with_nlp_THRESHOLD():
    NEGATIVE_REVIEW_THRESHOLD = 0.15
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
                    if filename not in app_categories and app_negative_review_counts[filename] / app_review_counts[
                        filename] >= NEGATIVE_REVIEW_THRESHOLD:
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

    return category_to_files


if __name__ == '__main__':

    CATEGORIES = {
        "malicious": ["phishing", "phishe", "malware", "hijack", "redirect", "can’t uninstall", "bad",
                      "can not uninstall",
                      "uninstall", "spyware", "virus", "scam", "malicious", "spy", "steal", "stealing",
                      "sensitive data", "fake", "stealer", "steals", "stolen", "hijack", "hijacking", "hijacked",
                      "hijacker", "doesn't work", "not working", "not work", "didn't work", "do not work",
                      "does not work",
                      "cheat", "cheating", "cheated", "fraud", "risk"],
        "adware": ["adware", "ad", "ads", "advert", "advertising", "advertise", "advertisement", "advertising",
                   "advertizing", "advertize", "advertizing", "advertized", "advertised"],
        "unusable": ["can not use", "doesn't work", "not working", "not work", "didn't work", "don’t install",
                     "do not install", "can't use"]
    }
    # 加载spaCy模型
    nlp = spacy.load("en_core_web_sm")
    # Read the data from the txt file
    with open('D:/PycharmProjects/crawling/crwal_data/add_on_info_2023_09_29.txt', 'r') as file:
        # Assuming each line in the txt file is a separate JSON string
        lines = file.readlines()

    # Parse each line as JSON
    data = [json.loads(line) for line in lines]

    permission_patterns = {
        "Calendar": ["calendar", "Google Calendar", "Calendar add-on"],
        "external service": ["external service"],
        "Google Apps Script deployments": ["Google Apps Script deployments"],
        "run third-party web content": ["third-party"],
        "Background process": ["not present"],
        "Application linked data access": ["View and manage data associated with the application"],
        "email": ["Manage drafts and send emails when you interact with the add-on",
                  "View your email messages when the add-on is running", "Run as a Gmail add-on",
                  "Send email on your behalf", "Read, compose, send, and permanently delete all your email from Gmail"],
        "Google Drive": ["Google Drive", "Google Sheets", "manage spreadsheets", "Google Apps Script",
                         "Google Workspace Apps"],
        "see personal info": ["Google Account email address", "personal info", "application's licensing information"],
        "contact": ["contacts"],
        "domain": ["domain"],
        "google photo": ["Google Photos"],
        "google classroom": ["Google Classroom", "classes"]
    }

    category_info = {}
    # Apply the categorization to each add-on in the data
    categorized_data = {}
    for add_on in data:
        categorized_data[add_on["name"].lower()] = categorize_add_on(add_on["perm_text"])

    # Print the categorized data
    for name, categories in categorized_data.items():
        print(f"{name}: {', '.join(categories)}")

    category_to_files = review_check_with_nlp_THRESHOLD()

    for category, filenames in category_to_files.items():
        unique_files = set(filenames)
        for file in unique_files:
            desired_part = file.split('.')[-3].replace('_', ' ')
            if desired_part == 'zone pdf editor converter':
                desired_part = 'zone pdf editor & converter'
            if desired_part == 'face age gender detect':
                desired_part = 'face, age, gender detect'
            for i in categorized_data[desired_part]:
                category_info.setdefault(i, set()).add(desired_part + ":" + category)

    for category, addons in category_info.items():
        print(f"\nCategory: {category}\n{'-' * 20}")
        for addon in addons:
            print(addon)
        print(f"Total Apps in {category}: {len(addons)}")

