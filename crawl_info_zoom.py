import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_add_on_urls():
    f = 'zoomUrls.txt'
    lines = open(f, 'r').readlines()
    urls = [line.replace('\n', '') for line in lines]
    urls = list(set(urls))
    urls.sort()
    return urls

# Setup Chrome options
browser = webdriver.Chrome()

urls = load_add_on_urls()
current_time = datetime.now().strftime("%Y_%m_%d")
file_path = 'zoom_add_on_info_' + current_time + '.txt'
out_f = open(file_path, 'a')

for url in urls:
    try:
        browser.get(url)
        # Wait for the element that contains the app name to be present in the DOM
        wait = WebDriverWait(browser, 10)
        app_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2[class*="MuiBox-root"]'))).text
        app_info = wait.until(EC.presence_of_element_located((By.ID, 'appInfo')))
        app_info_overview = app_info.find_element(By.CSS_SELECTOR, 'h2[class*="text-2xl"]').text
        app_info_categories = app_info.find_element(By.CSS_SELECTOR, '.MuiBox-root.css-2imjyh').text
        wait.until(EC.presence_of_element_located((By.ID, 'description-content')))
        # 使用JavaScript来获取所有`p`标签的内容
        app_description = browser.execute_script(
            "var descriptionContent = document.getElementById('description-content');"
            "var paragraphs = descriptionContent.getElementsByTagName('p');"
            "var allText = '';"
            "for (var i = 0; i < paragraphs.length; i++) {"
            "  allText += paragraphs[i].textContent + ' ';"
            "}"
            "return allText;"
        )


        requirements = wait.until(EC.presence_of_element_located((By.ID, 'whoCanInstall'))).text.replace('\n', ' ')

        permissions = wait.until(EC.presence_of_element_located((By.ID, 'appPermission'))).text.replace('\n', ' ')

        app_scopes = wait.until(EC.presence_of_element_located((By.ID, 'appScopes'))).text.replace('\n', ' ')

        dictionary = {
                    'app_name': app_name,
                    'url': url,
                    'app_overview': app_info_overview,
                    'app_categories': app_info_categories,
                    'app_description': app_description,
                    'requirements': requirements,
                    'permissions:': permissions,
                    'app_scopes': app_scopes,
                    }
        json.dump(dictionary, out_f)
        out_f.write('\n')
    except:
        print('Error: ', url)
        continue

out_f.close()
browser.quit()

