import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
import random

file_path = r'./104_web_ETL_collection'
if not os.path.exists(file_path):
    os.mkdir(file_path)

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)

headers = {'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

#keyword search
keyword = '數據分析'
page = 1

while True:
    if page > 150:
        break
    else:
        url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%s&order=1&asc=0&page=%s&mode=s&jobsource=2018indexpoc' %(keyword,page)

        #response the search page
        res = requests.get(url, headers=headers)

        soup = BeautifulSoup(res.text,'html.parser')

        title_Content = soup.select('div.b-block__left h2.b-tit a')

        #The title content of List
        for content in title_Content:
            title = content.text                          #title
            tmp_titleUrl = content['href'].split('/')[2:]
            titleUrl ='https://'+'/'.join(tmp_titleUrl)   #titleUrl
            print(title)
            print(titleUrl)

            if titleUrl == 'https://' or len(titleUrl)<10:
                continue
            time.sleep(random.uniform(1, 3))

            #article content
            driver.get(titleUrl)
            res_article = driver.execute_script("return document.getElementsByTagName('html')[0].outerHTML")
            articleContentSoup = BeautifulSoup(res_article, 'html.parser')

            try:
                company = articleContentSoup.select('title')[0].text.split('｜')[1]
            except IndexError:
                company = 'unknown'

            try:
                job_content = articleContentSoup.select('p[data-v-ebf385de=""]')[0].text
            except IndexError:
                job_content = 'null'

            try:
                job_require = articleContentSoup.select('div[data-v-726fdbe7=""]')[0].text
            except IndexError:
                job_require = 'null'

            try:
                job_welfare = articleContentSoup.select('div[data-v-d31d0296=""]')[0].text
            except IndexError:
                job_welfare = 'null'

            try:
                job_contact = articleContentSoup.select('div[data-v-d919c298=""]')[0].text
            except IndexError:
                job_contact = 'null'

            articleContent =  '---split---'+'\n'+title+'\n'\
                             +'---split---'+'\n'+company+'\n'\
                             +'---split---'+'\n'+titleUrl+'\n'\
                             +'---split---'+'\n'+job_content+'\n'\
                             +'---split---'+'\n'+job_require+'\n'\
                             +'---split---'+'\n'+job_welfare+'\n'\
                             +'---split---'+'\n'+job_contact+'\n'

            #article save
            try:
                with open(r'%s/%s.txt' % (file_path, title+'_'+company), 'w', encoding='utf-8') as f:
                    f.write(articleContent)
                    print('Save Done')
            except FileNotFoundError:
                title = title.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_') \
                    .replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_').replace('?', '_')

                company = company.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_') \
                    .replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_').replace('?', '_')

                try:
                    with open(r'%s/%s.txt' % (file_path, title+'_'+company), 'w', encoding='utf-8') as f:
                        f.write(articleContent)
                        print('Save Done')
                except:
                    print('error')
                    pass
            except:
                print('error')
                pass



            print('========================')
    page += 1
print('爬蟲結束')