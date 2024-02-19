import requests
from os import listdir
from os.path import isfile, join


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


if __name__ == '__main__':
    kws_list = load_keywords_google()
    urls = []

    for kw in kws_list:
        try:
            print('Processing keyword: ', kw)
            href_kw = 'https://marketplace.zoho.com/search?serviceName=home&page_limit=0&searchTerm=' + kw
            # Step 1: 获取JSON数据
            response = requests.get(href_kw)
            data = response.json()

            # Step 2: 解析JSON数据并构建URL列表
            for item in data['data']:
                service = item['service']
                namespace = item['namespace']
                url = f"https://marketplace.zoho.com/app/{service}/{namespace}"
                urls.append(url)
        except:
            continue

    print('Total not unique urls: ', len(urls))

    unique_urls = list(set(urls))
    unique_urls.sort()

    print('Total unique urls: ', len(unique_urls))

    # 将URL列表保存到文本文件中
    with open('zoho_urls.txt', 'w') as f:
        for url in unique_urls:
            f.write(url + '\n')
