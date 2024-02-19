import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
browser = webdriver.Chrome()

urls = ["https://slack.com/apps/category/At0G5YTKU2-analytics",
        "https://slack.com/apps/category/At0EFT6869-communication",
        "https://slack.com/apps/category/At0EFRCDQC-customer-support",
        "https://slack.com/apps/category/At0EFX4CCE-design",
        "https://slack.com/apps/category/At0EFRCDNY-developer-tools",
        "https://slack.com/apps/category/At0EFRCDPW-file-management",
        "https://slack.com/apps/category/At0MRS55PA-health-wellness",
        "https://slack.com/apps/category/At0EFT6893-hr-team-culture",
        "https://slack.com/apps/category/At0EFRCDQU-marketing",
        "https://slack.com/apps/category/At0EFWTRAM-office-management",
        "https://slack.com/apps/category/At0EFX9EF9-finance",
        "https://slack.com/apps/category/At0EFXUU6N-productivity",
        "https://slack.com/apps/category/At0EFY3MJ4-project-management",
        "https://slack.com/apps/category/At0G5VPH19-sales",
        "https://slack.com/apps/category/At0EFWTRA5-security-compliance",
        "https://slack.com/apps/category/At0EFXUU0J-social-fun",
        "https://slack.com/apps/category/At0QUNV823-travel",
        "https://slack.com/apps/category/At7KGP7Z3N-voice-video",
        "https://slack.com/apps/category/At7KK5H6AZ-media-news"]

filename = 'slackUrls.txt'
with open(filename, 'a+', encoding='utf-8') as f1:
    for url in urls:
        count = 1 # Start with the first page
        while count <= 50:
            # Navigate to the current page of the current URL

            browser.get(url + "?page=" + str(count))
            wait = WebDriverWait(browser, 10)
            # After navigating to a new page, immediately find the elements again
            buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class*="media_list_inner "]')))
            # buttons = browser.find_elements(By.CSS_SELECTOR, 'a[class*="media_list_inner "]')
            # Process the buttons
            for button in buttons:  # Iterate by index to avoid stale reference
                # Find the buttons again on each iteration to avoid stale elements
                try:
                    # Find the nested element with the 'canonical' rel attribute
                    href_value = button.get_attribute('href')
                    f1.write(href_value)
                    f1.write('\n')
                    print(href_value)
                except Exception as e:
                    # Log the error and skip to the next button
                    print("Error retrieving href: ", e)
                    continue

            # Increment the count to move to the next page
            count += 1

f1.close()