import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import urllib.request
import os
import json
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from os import listdir
from os.path import isfile, join
import sys
import logging

def load_keywords_google():
    kw_dir = './google-10000-english'  # google-10000-english is a folder contain all keywords files
    ## https://github.com/first20hours/google-10000-english
    kw_fs = [f for f in listdir(kw_dir) if isfile(join(kw_dir, f))]
    des_kws = []
    for kw_f in kw_fs:
        if kw_f.endswith('.md'):
            continue
        lines = open(join(kw_dir, kw_f), 'r').readlines()

        kws = [line.replace('\n', '') for line in lines]
        des_kws.extend(kws)

    kws_set = set(des_kws)
    des_kws = list(kws_set)
    des_kws.sort()
    return des_kws


def find_all_workspace_href(driver):
    elems = driver.find_elements(by='xpath', value="//a[@href]")
    # print(elems)
    add_on_urls = []

    for elem in elems:
        add_on_url = elem.get_attribute("href")

        if '/marketplace/app/' not in add_on_url:
            continue
        add_on_urls.append(add_on_url)
        # print(add_on_url)
    return add_on_urls


def collect_based_kw(driver):
    log = open("/home/myprog.log", "a")
    sys.stdout = log
    # driver.get('https://workspace.google.com/marketplace')
    output_f = '/home/add_on_urls_based_10000_kw.txt'

    f = open(output_f, 'w')
    kws_list = load_keywords_google()
    print('len of keywords:', len(kws_list))

    for kw in kws_list:
        # driver.get('https://workspace.google.com/marketplace')
        # driver.find_element(by='xpath', value= "//input[@type='text']").send_keys(kw)
        # driver.find_element(by='xpath', value= "//button[@aria-label='Search']").click()
        href_kw = 'https://workspace.google.com/marketplace/search/' + kw
        try:
            driver.get(href_kw)
        except Exception as err:
            print(err)
            continue
        timeout = 2
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            # time.sleep(1)
            WebDriverWait(driver, timeout).until(element_present)

        except:
            print("Timed out waiting for page to load: ", kw)
        finally:
            print("Page loaded: ", kw)

        try:
            add_on_urls = find_all_workspace_href(driver)
            print('len of href: ', len(add_on_urls))

            for ele in add_on_urls:
                f.write(ele + "\n")

            print('__________________________________________________________________________')
        except Exception as err:
            print(err)
            continue
    f.close()
    log.close()


def storeReviewCount(reviewCount, filename):
    with open(filename, 'w+', encoding='utf-8') as f1:
        f1.write(reviewCount)
        f1.write('\n')
        f1.close()


def getReviews(pageCount, browser, filename):
    for i in range(pageCount):
        profileElements = browser.find_elements(by=By.CLASS_NAME, value='mJsQBe')
        for profile in profileElements:
            keys = ['Name', 'reviewTime', 'review', 'grade', 'userImg']
            name = profile.find_element(by=By.CLASS_NAME, value='iLLAJe')
            userImg = profile.find_element(by=By.CLASS_NAME, value='c02Hg')
            review = profile.find_element(by=By.CLASS_NAME, value='bR5MYb')
            reviewTime = profile.find_element(by=By.CLASS_NAME, value='wzBhKb')
            try:
                grade = profile.find_element(by=By.CLASS_NAME, value='b479ib')
            except Exception as err1:
                # print(err1)
                continue
            else:
                values = [name.text, reviewTime.text, review.text, grade.get_attribute('aria-label'),
                          userImg.find_element(by=By.CLASS_NAME, value='wj0Ame').get_attribute('src')]
                dict1 = dict(zip(keys, values))
                with open(filename, 'a+', encoding='utf-8') as f1:
                    f1.write(json.dumps(dict1, ensure_ascii=False, indent=1))
                    f1.write('\n')

        browser.find_element(by=By.CLASS_NAME, value='awToQ').find_element(by=By.XPATH,
                                                                           value="//div[@jsname='ViaHrd']").click()
        time.sleep(2.5)
    f1.close()
    # browser.close()


def getReviews1(pageCount, browser, filename, k):
    k1 = k % 10
    k2 = k1
    for i in range(pageCount):
        if i == pageCount - 1:
            profileElements = browser.find_elements(by=By.CLASS_NAME, value='mJsQBe')
            for m in range(k1):
                try:
                    profileElements[m].find_element(by=By.CLASS_NAME, value='b479ib')
                except Exception as err1:
                    # print(err1)
                    k2 = k2 + 1
                    continue
            for m in range(k2):
                keys = ['Name', 'reviewTime', 'review', 'grade', 'userImg']
                name = profileElements[m].find_element(by=By.CLASS_NAME, value='iLLAJe')
                userImg = profileElements[m].find_element(by=By.CLASS_NAME, value='c02Hg')
                review = profileElements[m].find_element(by=By.CLASS_NAME, value='bR5MYb')
                reviewTime = profileElements[m].find_element(by=By.CLASS_NAME, value='wzBhKb')
                try:
                    grade = profileElements[m].find_element(by=By.CLASS_NAME, value='b479ib')
                except Exception as err1:
                    # print(err1)
                    continue
                else:
                    values = [name.text, reviewTime.text, review.text, grade.get_attribute('aria-label'),
                              userImg.find_element(by=By.CLASS_NAME, value='wj0Ame').get_attribute('src')]
                    dict1 = dict(zip(keys, values))
                    with open(filename, 'a+', encoding='utf-8') as f1:
                        f1.write(json.dumps(dict1, ensure_ascii=False, indent=1))
                        f1.write('\n')
            f1.close()
            # browser.close()
        else:
            profileElements = browser.find_elements(by=By.CLASS_NAME, value='mJsQBe')
            for profile in profileElements:
                keys = ['Name', 'reviewTime', 'review', 'grade', 'userImg']
                name = profile.find_element(by=By.CLASS_NAME, value='iLLAJe')
                userImg = profile.find_element(by=By.CLASS_NAME, value='c02Hg')
                review = profile.find_element(by=By.CLASS_NAME, value='bR5MYb')
                reviewTime = profile.find_element(by=By.CLASS_NAME, value='wzBhKb')
                try:
                    grade = profile.find_element(by=By.CLASS_NAME, value='b479ib')
                except Exception as err1:
                    # print(err1)
                    continue
                else:
                    values = [name.text, reviewTime.text, review.text, grade.get_attribute('aria-label'),
                              userImg.find_element(by=By.CLASS_NAME, value='wj0Ame').get_attribute('src')]
                    dict1 = dict(zip(keys, values))
                    with open(filename, 'a+', encoding='utf-8') as f1:
                        f1.write(json.dumps(dict1, ensure_ascii=False, indent=1))
                        f1.write('\n')

            browser.find_element(by=By.CLASS_NAME, value='awToQ').find_element(by=By.XPATH,
                                                                               value="//div[@jsname='ViaHrd']").click()
            time.sleep(2.5)


def save_html_page(driver):
    return


def collect_rating_download(driver):
    try:
        rating_avg = driver.find_element(by='xpath', value="//meta[@itemprop='ratingValue']").get_attribute("content")
    except NoSuchElementException:
        rating_avg = 'no grade'
    try:
        rating_worst = driver.find_element(by='xpath', value="//meta[@itemprop='worstRating']").get_attribute("content")
    except NoSuchElementException:
        rating_worst = 'no grade'
    try:
        rating_best = driver.find_element(by='xpath', value="//meta[@itemprop='bestRating']").get_attribute("content")
    except NoSuchElementException:
        rating_best = 'no grade'
    try:
        rating_persons = driver.find_element(by='xpath', value="//span[@itemprop='ratingCount']").text
    except NoSuchElementException:
        rating_persons = 'the count of grade is zero'
    try:
        download_num = driver.find_element(by='xpath', value="//div[@class='EqjhYe']/div").text
    except NoSuchElementException:
        download_num = 'the count of download is zero'

    found = get_element(driver, 'xpath', "//div[@class='bVxKXd']")
    last_updated = ''
    if found:
        last_updated = driver.find_element(by='xpath', value="//div[@class='bVxKXd']").text

    return rating_avg, rating_worst, rating_best, rating_persons, download_num, last_updated


def collect_host_app(driver):
    elems = []
    try:
        elems = driver.find_elements(by='xpath', value="//img[@class='W7Dtjd']")
    except NoSuchElementException:
        print('unable to find NAME attribute: ')
    except:
        print("Something else went wrong")
    host_apps = []
    for elem in elems:
        host_apps.append(elem.get_attribute("alt"))

    return host_apps


def switch_tab_panel(driver, tab_name):
    if tab_name == 'reviewsTab':
        driver.find_element(by='xpath', value="//button[@id='reviewsTab']").click()
    if tab_name == 'permissionsTab':
        driver.find_element(by='xpath', value="//button[@id='permissionsTab']").click()
    if tab_name == 'overviewTab':
        driver.find_element(by='xpath', value="//button[@id='overviewTab']").click()
    return


def collect_review(driver):
    switch_tab_panel(driver, 'reviewsTab')


def collect_overview(driver):
    switch_tab_panel(driver, 'overviewTab')
    overview_des = driver.find_element(by=By.XPATH, value="//pre[@class='nGA4ed']").text

    ## collect demo images
    images_elems = driver.find_elements(by=By.XPATH, value="//div[@jsname='UXbvIb']")
    images_urls = []
    for image_ele in images_elems:
        found = get_element(image_ele, By.TAG_NAME, "img")
        found_iframe = get_element(image_ele, By.TAG_NAME, "iframe")
        image_url = ''
        if found:
            image_url = image_ele.find_element(by=By.TAG_NAME, value="img").get_attribute("src")
        elif found_iframe:
            image_url = image_ele.find_element(by=By.TAG_NAME, value="iframe").get_attribute("src")
        images_urls.append(image_url)

    return overview_des, images_urls


def collect_permissions(driver):
    switch_tab_panel(driver, 'permissionsTab')

    perm_ele = driver.find_element(by='xpath', value="//div[@class='wrzTpc']")

    permissions = perm_ele.find_elements(by='xpath', value="//div[@jsdata]")
    perms_text = driver.find_elements(by='xpath', value="//span[@class='jyBTLc']")

    scopes = []
    texts = []
    for perm in permissions:
        scopes.append(perm.get_attribute('jsdata'))
    for visual in perms_text:
        texts.append(visual.text)

    return scopes, texts


def get_element(driver, by_val, xpath_val):
    try:
        ele = driver.find_element(by=by_val, value=xpath_val)
    except NoSuchElementException:
        return False
    except:
        return False

    return True


def get_elements(driver, xpath_val):
    try:
        eles = driver.find_elements(by='xpath', value=xpath_val)
    except NoSuchElementException:
        return False, ''
    except:
        return False, ''

    return True, eles


def collect_developer_info(driver):
    elems = driver.find_elements(by='xpath', value="//a[@class=' DmgOFc Sm1toc']")
    href, aria_label = '', ''
    developer_info = dict()

    for ele in elems:
        href = ele.get_attribute('href')
        try:
            aria_label = ele.get_attribute('aria-label')
        except NoSuchElementException:
            aria_label = ele.text
        except:
            aria_label = ele.text
            print('Something else went wrong')
        if type(aria_label) == type(None):
            aria_label = 'not'
        developer_info[aria_label] = href

    potential_price = []
    pricing = driver.find_elements(by='xpath', value="//span[@class='P0vMD']")
    for ele in pricing:
        potential_price.append(ele.text)

    return developer_info, potential_price


def collect_name_description(driver, url):
    name, short_des = '', ''
    try:
        name = driver.find_element(by='xpath', value="//span[@itemprop='name']").text
    except NoSuchElementException:
        print('unable to find NAME attribute: ', url)
    except:
        print("Something else went wrong")

    try:
        short_des = driver.find_element(by='xpath', value="//div[@class='kmwdk']").text
    except NoSuchElementException:
        print('unable to find DESC attribute: ', url)
    except:
        print("Something else went wrong")

    return name, short_des


def load_add_on_urls():
    f = '/home/add_on_urls_based_10000_kw.txt'
    lines = open(f, 'r').readlines()

    urls = [line.replace('\n', '') for line in lines]
    urls = [x for x in urls if '/marketplace/app/' in x]
    urls = list(set(urls))
    urls.sort()
    return urls


def collect_all_infos(driver):
    log = open("/home/collect_all_infos.log", "a")
    sys.stdout = log
    urls = load_add_on_urls()
    current_time = datetime.now().strftime("%Y_%m_%d")
    file_path = '/home/add_on_info_' + current_time + '.txt'
    out_f = open(file_path, 'a')

    # urls = ['https://workspace.google.com/marketplace/app/photos_to_slides/859164198261',
    # 'https://workspace.google.com/marketplace/app/extensis_fonts/568288816452',
    # ]

    # break_point = 'https://workspace.google.com/marketplace/app/data_splitter/1072254773617'
    # break_point = 'https://workspace.google.com/marketplace/app/majestic/80143568879'

    # counter = 0
    # for url in urls:
    # if break_point != url:
    # counter += 1
    # else:
    # break

    # urls = urls[counter+1:]
    # out_f.write(str(datetime.now()) + ":")
    # out_f.write('\n')
    for url in urls:
        try:
            # print(url)
            driver.get(url)
            # found = get_element(driver, 'xpath', "//div[@class='bVxKXd']")
            # last_updated = ''
            # if found:
            #     last_updated = driver.find_element(by='xpath', value="//div[@class='bVxKXd']").text
            #     dt_datetime = datetime.strptime(last_updated[16:], '%B %d, %Y').strftime("%Y-%m-%d")
            #     currentTime = datetime.now()
            #     currentTime = currentTime.strftime("%Y-%m-%d")
            #     d1 = datetime.strptime(currentTime, '%Y-%m-%d')
            #     d2 = datetime.strptime(dt_datetime, '%Y-%m-%d')
            #     # run every three days
            #     if (d1 - d2).days > 3:
            #         dictionary1 ={
            #             'add_on_url': url,
            #             'status': "not update",
            #         }
            #         json.dump(dictionary1, out_f)
            #         out_f.write('\n')
            #         continue
            timeout = 2
            try:
                element_present = EC.presence_of_element_located((By.ID, 'main'))
                # time.sleep(1)
                WebDriverWait(driver, timeout).until(element_present)

            except:
                print("Timed out waiting for page to load: ", url)
            finally:
                print("Page loaded: ", url)

            name, desc = collect_name_description(driver, url)
            if name == '' and desc == '':
                continue
            developer_info, potential_price = collect_developer_info(driver)
            host_apps = collect_host_app(driver)
            rating_avg, rating_worst, rating_best, rating_persons, download_num, last_updated = collect_rating_download(
                driver)
            overview, images_urls = collect_overview(driver)
            permissions, explain = collect_permissions(driver)

            dictionary = {
                'add_on_url': url,
                'name': name,
                'short_des': desc,
                'developer_infos': developer_info,
                'price': potential_price,
                'overview': overview,
                'images:': images_urls,
                'host_apps': host_apps,
                'permissions': permissions,
                'perm_text': explain,
                'rating_avg': rating_avg,
                'rating_worst': rating_worst,
                'rating_best': rating_best,
                'rating_persons': rating_persons,
                'download_num': download_num,
                'last_updated': last_updated,

            }

            json.dump(dictionary, out_f)
            out_f.write('\n')
        except Exception as err:
            # print(err)
            continue
    out_f.close()
    log.close()


if __name__ == '__main__':
    while True:
        logging.basicConfig(filename='/home/output.log', level=logging.INFO,
                                format='%(asctime)s - %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
        options = Options()
        options.add_argument('--headless')
        logging.info('start to collect urls')
        browser2 = webdriver.Firefox(options=options)
        collect_based_kw(browser2)
        browser2.quit()
        output_file = '/home/unique_urls.txt'
        urls = load_add_on_urls()
        with open(output_file, 'w') as file:
            for url in urls:
                file.write(url + '\n')
        file.close()
        logging.info('start to collect all infos')
        browser1 = webdriver.Firefox(options=options)
        collect_all_infos(browser1)
        browser1.quit()
        browser = webdriver.Firefox(options=options)
        logging.info('start to collect reviews')
        for webUrl in urls:
            try:
                filename = '/home/results/' + webUrl.replace('//', '').replace(':', '-').replace('/', '.') + '.json'
                filename1 = '/home/results/' + webUrl.replace('//', '').replace(':', '-').replace('/', '.') + '.log'
                url = webUrl
                try:
                    browser.get(url)
                    status = urllib.request.urlopen(url).code
                    # print(status)
                except Exception as err:
                    # print(err)
                    # print(url + ": this url doesn't work")
                    with open(filename1, 'w+', encoding='utf-8') as f3:
                        f3.write("this url doesn't work")
                        f3.close()
                    # browser.close()
                    continue
                else:
                    button = browser.find_element(by=By.ID, value='reviewsTab')
                    button.click()
                    time.sleep(0.5)
                    button1 = browser.find_element(by=By.CLASS_NAME, value='ry3kXd')
                    button1.click()
                    time.sleep(0.5)
                    ActionChains(browser).send_keys(Keys.DOWN).perform()
                    time.sleep(0.5)
                    ActionChains(browser).send_keys(Keys.ENTER).perform()
                    time.sleep(1.5)
                    if os.path.exists(filename1):
                        with open(filename1, 'r', encoding='utf-8') as f4:
                            lines = f4.readlines()
                            reviewCount_Pre = lines[0]
                            f4.close()
                    else:
                        reviewCount_Pre = 0
                    reviewCount = browser.find_element(by=By.XPATH, value="//span[@jsname='n7Ucd']").text
                    if reviewCount == '':
                        with open(filename1, 'w+', encoding='utf-8') as f2:
                            f2.write("0")
                            f2.write('\n')
                            f2.write("app no comments")
                            f2.close()
                        # browser.close()
                        continue
                    else:
                        if int(reviewCount_Pre) == 0:
                            if int(reviewCount) % 10 == 0:
                                pageCount = int(int(reviewCount) / 10)
                                storeReviewCount(reviewCount, filename1)
                                getReviews(pageCount, browser, filename)
                            else:
                                pageCount = int(int(reviewCount) / 10) + 1
                                storeReviewCount(reviewCount, filename1)
                                getReviews(pageCount, browser, filename)
                        else:
                            if int(reviewCount) > int(reviewCount_Pre):
                                button2 = browser.find_elements(by=By.CLASS_NAME, value='ry3kXd')
                                button2[1].click()
                                time.sleep(0.5)
                                ActionChains(browser).send_keys(Keys.DOWN).perform()
                                time.sleep(0.5)
                                ActionChains(browser).send_keys(Keys.ENTER).perform()
                                time.sleep(1.5)
                                k = int(reviewCount) - int(reviewCount_Pre)
                                if k % 10 == 0:
                                    pageCount = int(k / 10)
                                    storeReviewCount(reviewCount, filename1)
                                    getReviews1(pageCount, browser, filename, k)
                                else:
                                    pageCount = int(k / 10) + 1
                                    storeReviewCount(reviewCount, filename1)
                                    getReviews1(pageCount, browser, filename, k)
            except Exception as err:
                # print(err)
                # print(webUrl + ": this url doesn't work")
                continue
        logging.info('all finish')
        browser.quit()
        time.sleep(24 * 60 * 60)
