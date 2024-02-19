import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
filename = 'githubUrls.txt'
with open(filename, 'a+', encoding='utf-8') as f1:
    for count in range(1, 44):
        url = 'https://github.com/marketplace?category=&query=&type=apps&verification=' + "&page=" + str(count)
        # Navigate to the current page of the current URL
        browser.get(url)
        wait = WebDriverWait(browser, 10)
        # After navigating to a new page, immediately find the elements again
        buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3[class*="h4"]')))
        # buttons = browser.find_elements(By.CSS_SELECTOR, 'a[class*="media_list_inner "]')
        # Process the buttons
        for button in buttons:  # Iterate by index to avoid stale reference
            # Find the buttons again on each iteration to avoid stale elements
            try:
                # Find the nested element with the 'canonical' rel attribute
                a_tag = button.find_element(By.CSS_SELECTOR, "a")  # Adjust the selector if needed
                href_value = a_tag.get_attribute('href')
                f1.write(href_value)
                f1.write('\n')
                print(href_value)
            except Exception as e:
                # Log the error and skip to the next button
                print("Error retrieving href: ", e)
                continue

f1.close()
browser.quit()
