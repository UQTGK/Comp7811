import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def load_add_on_urls():
    f = 'slackUrls.txt'
    lines = open(f, 'r').readlines()
    urls = [line.replace('\n', '') for line in lines]
    urls = list(set(urls))
    urls.sort()
    return urls


# Setup Chrome options
browser = webdriver.Chrome()

urls = load_add_on_urls()
current_time = datetime.now().strftime("%Y_%m_%d")
file_path = 'slack_add_on_info_' + current_time + '.txt'
out_f = open(file_path, 'a')

for url in urls:
    try:
        browser.get(url)
        # Wait for the element that contains the app name to be present in the DOM
        wait = WebDriverWait(browser, 10)
        app_name = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h2[class*="p-app_info_title margin_bottom_150"]'))).text
        app_details = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.p-app_directory_detail_additional_info__main'))).text.replace('\n', ' ')
        app_description = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.tsf_output.emoji_replace_on_load'))).text.replace('\n',
                                                                                                                 ' ')

        app_features_concatenated_text = ""
        try:
            browser.find_element(by=By.ID, value='js-features-tab').click()
            app_features = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.p-app_directory_detail_features')))

            for feature in app_features:
                app_features_concatenated_text += feature.text
                app_features_concatenated_text += " "

            app_features_concatenated_text = app_features_concatenated_text.replace('\n', ' ')
        except Exception as e:
            app_features_concatenated_text = ""
            print(e)

        time.sleep(0.5)




        try:
            browser.find_element(by=By.ID, value='js-settings-tab').click()
            app_permissions = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.c-button-unstyled.p-scope_info__group_toggle')))
            for permission in app_permissions:
                permission.click()

            app_permissions = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.p-scope_info'))).text.replace('\n', ' ')
        except Exception as e:
            app_permissions = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.c-tabs__tab_panels'))).text.replace('\n', ' ')
            print(e)

        time.sleep(0.5)
        try:
            browser.find_element(by=By.ID, value='js-security-compliance-tab').click()
            app_security_compliance = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.padding_top_50  ')))

            for security_compliance in app_security_compliance:
                security_compliance.click()

            app_security_compliance = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.padding_top_50  ')))

            app_security_compliance_text = ""
            for security_compliance in app_security_compliance:
                app_security_compliance_text += security_compliance.text
                app_security_compliance_text += " "
            app_security_compliance_text = app_security_compliance_text.replace('\n', ' ')
        except Exception as e:
            app_security_compliance_text = ""
            print(e)
        try:
            app_security_compliance_1 = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.p-app_directory_scopes__accordion-wrapper')))
            for security_compliance_1 in app_security_compliance_1:
                security_compliance_1.click()
            app_security_compliance_1 = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.p-app_directory_scopes__accordion-wrapper')))
            app_scope = ""
            for security_compliance_1 in app_security_compliance_1:
                app_scope += security_compliance_1.text
                app_scope += " "

            app_scope = app_scope.replace('\n', ' ')

        except Exception as e:
            app_scope = ""
            print(e)


        dictionary = {
            'app_name': app_name,
            'url': url,
            'app_details': app_details,
            'app_description': app_description,
            'app_features': app_features_concatenated_text,
            'app_permissions': app_permissions,
            'app_security_compliance': app_security_compliance_text,
            'app_scope': app_scope
        }
        json.dump(dictionary, out_f)
        out_f.write('\n')

    except:
        print('Error: ', url)
        continue

out_f.close()
browser.quit()


