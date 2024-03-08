import csv
import os
import time
from random import random

import wordcloud
from selenium import webdriver
from selenium.webdriver.common.by import By


def tongji():
    prices = []
    with open('前十页销量和金额.csv', 'r', encoding='utf-8', newline='') as f:
        fieldnames = ['价格', '销量', '店铺位置']
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for index, i in enumerate(reader):
            if index != 0:
                price = float(i['价格'].replace('¥', ''))
                prices.append(price)
    DATAS = {'<10': 0, '10~30': 0, '30~50': 0,
             '50~70': 0, '70~90': 0, '90~110': 0,
             '110~130': 0, '130~150': 0, '150~170': 0, '170~200': 0, }
    for price in prices:
        if price < 10:
            DATAS['<10'] += 1
        elif 10 <= price < 30:
            DATAS['10~30'] += 1
        elif 30 <= price < 50:
            DATAS['30~50'] += 1
        elif 50 <= price < 70:
            DATAS['50~70'] += 1
        elif 70 <= price < 90:
            DATAS['70~90'] += 1
        elif 90 <= price < 110:
            DATAS['90~110'] += 1
        elif 110 <= price < 130:
            DATAS['110~130'] += 1
        elif 130 <= price < 150:
            DATAS['130~150'] += 1
        elif 150 <= price < 170:
            DATAS['150~170'] += 1
        elif 170 <= price < 200:
            DATAS['170~200'] += 1

    for k, v in DATAS.items():
        print(k, ':', v)


def get_the_top_10(url):
    top_ten = []
    # 获取代理
    ip = zhima1()[2][random.randint(0, 399)]
    # 运行quicker动作（可以不用管）
    os.system('"C:\Program Files\Quicker\QuickerStarter.exe" runaction:5e3abcd2-9271-47b6-8eaf-3e7c8f4935d8')
    options = webdriver.ChromeOptions()
    # 远程调试Chrome
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    options.add_argument(f'--proxy-server={ip}')
    driver = webdriver.Chrome(options=options)
    # 隐式等待
    driver.implicitly_wait(3)
    # 打开网页
    driver.get(url)
    # 点击部分文字包含'销量'的网页元素
    driver.find_element(By.PARTIAL_LINK_TEXT, '销量').click()
    time.sleep(1)
    # 页面滑动到最下方
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(1)
    # 查找元素
    element = driver.find_element(By.ID, 'mainsrp-itemlist').find_element(By.XPATH, './/div[@class="items"]')
    items = element.find_elements(By.XPATH, './/div[@data-category="auctions"]')
    for index, item in enumerate(items):
        if index == 10:
            break
        # 查找元素
        price = item.find_element(By.XPATH, './div[2]/div[1]/div[contains(@class,"price")]').text
        paid_num_data = item.find_element(By.XPATH, './div[2]/div[1]/div[@class="deal-cnt"]').text
        store_location = item.find_element(By.XPATH, './div[2]/div[3]/div[@class="location"]').text
        store_href = item.find_element(By.XPATH, './div[2]/div[@class="row row-2 title"]/a').get_attribute(
            'href').strip()
        # 将数据添加到字典
        top_ten.append(
            {'价格': price,
             '销量': paid_num_data,
             '店铺位置': store_location,
             '店铺链接': store_href
             })

    for i in top_ten:
        print(i)


def get_top_10_comments(url):
    with open('排名前十评价.txt', 'w+', encoding='utf-8') as f:
        pass
    # ip = ipidea()[1]
    os.system('"C:\Program Files\Quicker\QuickerStarter.exe" runaction:5e3abcd2-9271-47b6-8eaf-3e7c8f4935d8')
    options = webdriver.ChromeOptions()
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    # options.add_argument(f'--proxy-server={ip}')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    driver.get(url)
    driver.find_element(By.PARTIAL_LINK_TEXT, '销量').click()
    time.sleep(1)
    element = driver.find_element(By.ID, 'mainsrp-itemlist').find_element(By.XPATH, './/div[@class="items"]')
    items = element.find_elements(By.XPATH, './/div[@data-category="auctions"]')
    original_handle = driver.current_window_handle
    item_hrefs = []
    # 先获取前十的链接
    for index, item in enumerate(items):
        if index == 10:
            break
        item_hrefs.append(
            item.find_element(By.XPATH, './/div[2]/div[@class="row row-2 title"]/a').get_attribute('href').strip())
    # 爬取前十每个商品评价
    for item_href in item_hrefs:
        # 打开新标签
        # item_href = 'https://item.taobao.com/item.htm?id=523351391646&ns=1&abbucket=11#detail'
        driver.execute_script(f'window.open("{item_href}")')
        # 切换过去
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])

        # 页面向下滑动一部分，直到让评价那两个字显示出来
        try:
            driver.find_element(By.PARTIAL_LINK_TEXT, '评价').click()
        except Exception as e1:
            try:
                x = driver.find_element(By.PARTIAL_LINK_TEXT, '评价').location_once_scrolled_into_view
                driver.find_element(By.PARTIAL_LINK_TEXT, '评价').click()
            except Exception as e2:
                try:
                    # 先向下滑动100，放置评价2个字没显示在屏幕内
                    driver.execute_script('var q=document.documentElement.scrollTop=100')
                    x = driver.find_element(By.PARTIAL_LINK_TEXT, '评价').location_once_scrolled_into_view
                except Exception as e3:
                    driver.find_element(By.XPATH, '/html/body/div[6]/div/div[3]/div[2]/div/div[2]/ul/li[2]/a').click()
        time.sleep(1)
        try:
            trs = driver.find_elements(By.XPATH, '//div[@class="rate-grid"]/table/tbody/tr')
            for index, tr in enumerate(trs):
                if index == 0:
                    comments = tr.find_element(By.XPATH, './td[1]/div[1]/div/div').text.strip()
                else:
                    try:
                        comments = tr.find_element(By.XPATH,
                                                   './td[1]/div[1]/div[@class="tm-rate-fulltxt"]').text.strip()
                    except Exception as e:
                        comments = tr.find_element(By.XPATH,
                                                   './td[1]/div[1]/div[@class="tm-rate-content"]/div[@class="tm-rate-fulltxt"]').text.strip()
                with open('排名前十评价.txt', 'a+', encoding='utf-8') as f:
                    f.write(comments + '\n')
                    print(comments)
        except Exception as e:
            lis = driver.find_elements(By.XPATH, '//div[@class="J_KgRate_MainReviews"]/div[@class="tb-revbd"]/ul/li')
            for li in lis:
                comments = li.find_element(By.XPATH, './div[2]/div/div[1]').text.strip()
                with open('排名前十评价.txt', 'a+', encoding='utf-8') as f:
                    f.write(comments + '\n')
                    print(comments)


def get_top_10_comments_wordcloud():
    file = '排名前十评价.txt'
    f = open(file, encoding='utf-8')
    txt = f.read()
    f.close()

    w = wordcloud.WordCloud(width=1000,
                            height=700,
                            background_color='white',
                            font_path='msyh.ttc')
    # 创建词云对象，并设置生成图片的属性

    w.generate(txt)
    name = file.replace('.txt', '')
    w.to_file(name + '词云.png')
    os.startfile(name + '词云.png')


def get_10_pages_datas():
    with open('前十页销量和金额.csv', 'w+', encoding='utf-8', newline='') as f:
        f.write('\ufeff')
        fieldnames = ['价格', '销量', '店铺位置']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    infos = []
    options = webdriver.ChromeOptions()
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    # options.add_argument(f'--proxy-server={ip}')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    driver.get(url)
    # driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    element = driver.find_element(By.ID, 'mainsrp-itemlist').find_element(By.XPATH, './/div[@class="items"]')
    items = element.find_elements(By.XPATH, './/div[@data-category="auctions"]')
    for index, item in enumerate(items):
        price = item.find_element(By.XPATH, './div[2]/div[1]/div[contains(@class,"price")]').text
        paid_num_data = item.find_element(By.XPATH, './div[2]/div[1]/div[@class="deal-cnt"]').text
        store_location = item.find_element(By.XPATH, './div[2]/div[3]/div[@class="location"]').text
        infos.append(
            {'价格': price,
             '销量': paid_num_data,
             '店铺位置': store_location})
    try:
        driver.find_element(By.PARTIAL_LINK_TEXT, '下一').click()
    except Exception as e:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        driver.find_element(By.PARTIAL_LINK_TEXT, '下一').click()
    for i in range(9):
        time.sleep(1)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        element = driver.find_element(By.ID, 'mainsrp-itemlist').find_element(By.XPATH, './/div[@class="items"]')
        items = element.find_elements(By.XPATH, './/div[@data-category="auctions"]')
        for index, item in enumerate(items):
            try:
                price = item.find_element(By.XPATH, './div[2]/div[1]/div[contains(@class,"price")]').text
            except Exception:
                time.sleep(1)
                driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                price = item.find_element(By.XPATH, './div[2]/div[1]/div[contains(@class,"price")]').text
            paid_num_data = item.find_element(By.XPATH, './div[2]/div[1]/div[@class="deal-cnt"]').text
            store_location = item.find_element(By.XPATH, './div[2]/div[3]/div[@class="location"]').text
            infos.append(
                {'价格': price,
                 '销量': paid_num_data,
                 '店铺位置': store_location})
        try:
            driver.find_element(By.PARTIAL_LINK_TEXT, '下一').click()
        except Exception as e:
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            driver.find_element(By.PARTIAL_LINK_TEXT, '下一').click()
        # 一页结束
        for info in infos:
            print(info)
        with open('前十页销量和金额.csv', 'a+', encoding='utf-8', newline='') as f:
            fieldnames = ['价格', '销量', '店铺位置']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            for info in infos:
                writer.writerow(info)


if __name__ == '__main__':
    url = 'https://s.taobao.com/search?q=%E5%B0%8F%E9%B1%BC%E9%9B%B6%E9%A3%9F&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.21814703.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=4&ntoffset=4&p4ppushleft=2%2C48&s=0'
    get_10_pages_datas()
    #tongji()
    #get_the_top_10(url)
    #get_top_10_comments(url)
    #get_top_10_comments_wordcloud()
