import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_add_on_urls():
    f = 'github_unique_urls.txt'
    lines = open(f, 'r').readlines()
    urls = [line.replace('\n', '') for line in lines]
    urls = list(urls)
    return urls

# Setup Chrome options
browser = webdriver.Chrome()

urls = load_add_on_urls()
current_time = datetime.now().strftime("%Y_%m_%d")
file_path = 'github_add_on_info_' + current_time + '.txt'
out_f = open(file_path, 'a')

for url in urls:
    try:
        browser.get(url)
        # Wait for the element that contains the app name to be present in the DOM
        wait = WebDriverWait(browser, 5)
        try:
            app_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.f00-light.lh-condensed.mb-3'))).text
        except Exception as e:
            print(e)
            app_name = ""
        try:
            app_info_categories = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[aria-labelledby="categories-heading"]'))).text
        except Exception as e:
            print(e)
            app_info_categories = ""
        try:
            app_type = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.py-3.lh-condensed'))).text
        except Exception as e:
            print(e)
            app_type = ""

        try:
            app_customers = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-hovercard-type="organization"]')))
            customers = []
            for customer in app_customers:
                customers.append(customer.get_attribute('href'))
        except Exception as e:
            print(e)
            customers = ""
        try:
            app_developers = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.d-flex.flex-items-center.css-truncate.css-truncate-target'))).text
        except Exception as e:
            print(e)
            app_developers = ""
        try:
            app_Verified_Domains = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[aria-labelledby="verified-domains-header"]'))).text
        except Exception as e:
            print(e)
            app_Verified_Domains = ""
        try:
            app_description = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.Details.markdown-body.mb-4.js-details-container'))).text
        except Exception as e:
            print(e)
            app_description = ""
        try:
            app_pricing_plan = wait.until(
                EC.presence_of_element_located((By.ID, 'pricing-plans-list'))).text
        except Exception as e:
            print(e)
            app_pricing_plan = ""

        try:
            ul_elements = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul[aria-labelledby="developer-links-header"]')))

            # Initialize a list to store all developer links
            developers_links = []

            # Loop through each 'ul' element
            for ul in ul_elements:
                # Find all 'a' elements within the current 'ul' with rel="nofollow"
                a_elements = ul.find_elements(By.CSS_SELECTOR, 'a[rel="nofollow"]')

                # Loop through each 'a' element and get the 'href'
                for a in a_elements:
                    href = a.get_attribute('href')
                    developers_links.append(href)  # Store the 'href' in the list
        except Exception as e:
            print(e)
            developers_links = ""

        dictionary = {
                    'app_name': app_name,
                    'url': url,
                    'app_info_categories': app_info_categories,
                    'app_type': app_type,
                    'app_developers': app_developers,
                    'app_Verified_Domains': customers,
                    'app_description:': app_description,
                    'app_pricing_plan': app_pricing_plan,
                    'developers_links': developers_links,
                    }
        json.dump(dictionary, out_f)
        out_f.write('\n')
    except:
        print('Error: ', url)
        continue

out_f.close()
browser.quit()