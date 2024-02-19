from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import os
import time
import re
# 读取test文件中的每一行
with open('zoho_urls.txt', 'r') as file:
    urls = file.readlines()
    file.close()
# 确保zoho_results文件夹存在
if not os.path.exists('zoho_results'):
    os.makedirs('zoho_results')

# 初始化webdriver
driver = webdriver.Chrome()

for url in urls:
    try:
        url = url.strip()
        url = url + '#ratingsReview'
        driver.get(url)
        span_text = driver.find_element(by=By.ID, value='avgrating-wrapper')
        nested_span_text = span_text.find_elements(by=By.TAG_NAME, value='span')
        number = nested_span_text[-1].text
        number = re.findall(r'\d+', number)
        if int(number[0]) == 0:
            continue
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'individual-review')))

        # 获取页面源代码
        html = driver.page_source

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 找到所有的 individual-review 标签
        reviews = soup.find_all('div', class_='individual-review')
        # 创建一个列表来存储所有评论的字典
        data = []
        # 遍历每个评论
        for review in reviews:
            review_data = {}
            # 提取用户的名字
            user_name = review.find('div', class_='user-extn-review general-txt review-user-name')
            if user_name:
                review_data['User Name'] = user_name.get_text()

            # 提取评论评分
            rating_elements = review.find_all('a', class_='rated selectorIcon')
            review_data['Review Rating'] = len(rating_elements)

            # 提取评论时间
            review_time = review.find('div', class_='reviewer-info general-txt')
            if review_time:
                review_data['Review Time'] = review_time.get_text()[:12]

            # 提取评论内容
            review_content = review.find('div', class_='user-extn-review general-txt')
            if review_content:
                review_data['Review Content'] = review_content.get_text()

            data.append(review_data)

        # 获取URL的名字作为文件名
        file_name = 'zoho_results/' + url.split('/')[-1].split('#')[0] + '.json'
        # 将数据保存到JSON文件中
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.close()
    except Exception as e:
        print(e)
        continue

# 关闭webdriver
driver.quit()
