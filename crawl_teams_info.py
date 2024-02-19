import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_add_on_urls():
    f = 'teamsurls1.txt'
    lines = open(f, 'r').readlines()
    urls = [line.replace('\n', '') for line in lines]
    urls = list(urls)
    return urls

# Setup Chrome options
browser = webdriver.Chrome()

urls = load_add_on_urls()
current_time = datetime.now().strftime("%Y_%m_%d")
file_path = 'microsoft_teams_add_on_info_' + current_time + '.txt'
out_f = open(file_path, 'a')

for url in urls:
    try:
        browser.get(url)
        # Wait for the element that contains the app name to be present in the DOM
        wait = WebDriverWait(browser, 5)
        try:
            app_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ms-fontSize-28.ms-fontWeight-semibold.title'))).text
        except Exception as e:
            print(e)
            app_name = ""
        try:
            app_overview = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.appDetailContent'))).text
        except Exception as e:
            print(e)
            app_overview = ""

        try:
            buttons = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.defaultTab')))

            buttons[1].click()
        except Exception as e:
            print(e)
            continue
        try:
            app_rating_distribution = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ratingPercentagesDetails')))

            ratings_distribution = []
            for rating in app_rating_distribution:
                ratings_distribution.append(rating.text)
        except Exception as e:
            print(e)
            ratings_distribution = []

        try:
            app_rating = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.ratingSummaryAverageSection.ratingSummaryAverageSection-168'))).get_attribute(
                        'aria-label')
        except Exception as e:
            print(e)
            app_rating = ""

        try:
            buttons = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.defaultTab')))

            buttons[2].click()
        except Exception as e:
            print(e)
            continue

        try:
            app_details_support = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.columnCells')))

            app_details = app_details_support[0].text

            supports = app_details_support[1].find_elements(By.CLASS_NAME, 'c-hyperlink')

            app_supports = []
            for support in supports:
                app_supports.append((support.get_attribute('href'), support.text))

        except Exception as e:
            print(e)
            app_details = ""
            app_supports = []


        dictionary = {
                    'app_name': app_name,
                    'url': url,
                    'app_overview': app_overview,
                    'ratings_distribution': ratings_distribution,
                    'app_rating': app_rating,
                    'app_details': app_details,
                    'app_supports:': app_supports,
                    }
        json.dump(dictionary, out_f)
        out_f.write('\n')
    except:
        print('Error: ', url)
        continue

out_f.close()
browser.quit()