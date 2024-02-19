import time
from selenium.webdriver.common.by import By
from selenium import webdriver

browser = webdriver.Chrome()

urls = ["https://marketplace.zoom.us/apps?category=analytics",
        "https://marketplace.zoom.us/apps?category=broadcasting-streaming",
        "https://marketplace.zoom.us/apps?category=business-system-integrator",
        "https://marketplace.zoom.us/apps?category=crm",
        "https://marketplace.zoom.us/apps?category=carrier-provider-exchange",
        "https://marketplace.zoom.us/apps?category=team-collaborations",
        "https://marketplace.zoom.us/apps?category=customer-service",
        "https://marketplace.zoom.us/apps?category=eCommerce",
        "https://marketplace.zoom.us/apps?category=education",
        "https://marketplace.zoom.us/apps?category=eventmanagement",
        "https://marketplace.zoom.us/apps?category=financialServices",
        "https://marketplace.zoom.us/apps?category=games",
        "https://marketplace.zoom.us/apps?category=government",
        "https://marketplace.zoom.us/apps?category=health-wellness",
        "https://marketplace.zoom.us/apps?category=health-care",
        "https://marketplace.zoom.us/apps?category=human-resources",
        "https://marketplace.zoom.us/apps?category=learning-development",
        "https://marketplace.zoom.us/apps?category=marketing",
        "https://marketplace.zoom.us/apps?category=note-taking",
        "https://marketplace.zoom.us/apps?category=presentations",
        "https://marketplace.zoom.us/apps?category=productivity",
        "https://marketplace.zoom.us/apps?category=project-management",
        "https://marketplace.zoom.us/apps?category=recording-transcriptions",
        "https://marketplace.zoom.us/apps?category=sales-automation",
        "https://marketplace.zoom.us/apps?category=scheduling-calendar",
        "https://marketplace.zoom.us/apps?category=content-and-compliance",
        "https://marketplace.zoom.us/apps?category=social-activities",
        "https://marketplace.zoom.us/apps?category=surveys-polls",
        "https://marketplace.zoom.us/apps?category=transcription-translation",
        "https://marketplace.zoom.us/apps?category=virtual-backgrounds-scenes",
        "https://marketplace.zoom.us/apps?category=whiteboards",
        "https://marketplace.zoom.us/apps?category=workflow-automation"]

filename = 'zoomUrls.txt'
with open(filename, 'a+', encoding='utf-8') as f1:
    for url in urls:
        count = 1 # Start with the first page
        while True:
            # Navigate to the current page of the current URL

            browser.get(url + "&page=" + str(count))

            # After navigating to a new page, immediately find the elements again
            buttons = browser.find_elements(By.CSS_SELECTOR, ".MuiBox-root.css-2vd5av")
            time.sleep(2)
            # If no buttons are found, then it's time to move to the next URL
            try:
                button1 = browser.find_element(By.CSS_SELECTOR, ".MuiBox-root.css-2vd5av")
            except:
                break
            # Process the buttons
            for i in range(len(buttons)):  # Iterate by index to avoid stale reference
                # Find the buttons again on each iteration to avoid stale elements
                buttons = browser.find_elements(By.CSS_SELECTOR, ".MuiBox-root.css-2vd5av")
                try:
                    button = buttons[i]
                    # Find the nested element with the 'canonical' rel attribute
                    time.sleep(0.2)
                    href_value = button.find_element(By.CSS_SELECTOR, "a[rel='canonical']").get_attribute('href')
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
