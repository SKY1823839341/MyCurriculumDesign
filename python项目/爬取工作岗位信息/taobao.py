import requests
#import bs4
import re
import json


def open(keywords, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

    payload = {'q': keywords, 'sort': "sale-desc", 's': (page - 1) * 44}
    url = "https://s.taobao.com/search"

    res = requests.get(url, params=payload)
    return res


def get_item(res):
    g_page_config = re.search(r'g_page_config = (.*?);\n', res.text)
    page_config_json = json.loads(g_page_config.group(1))
    page_item = page_config_json['mods']['itemlist']['data']['auctions']

    result = []  # 整理出我们关注的信息(ID,标题，链接，售价，销量和商家)
    for each in page_item:
        dict1 = dict.fromkeys(('id', 'title', 'link', 'price', 'sale', 'shoper'))
        dict1['id'] = each['nid']
        dict1['title'] = each['title']
        dict1['link'] = each['detail_url']
        dict1['price'] = each['view_price']
        dict1['sale'] = each['view_sales']
        dict1['shoper'] = each['nick']
        result.append(dict1)

    return result


def count_sales(items):
    count = 0
    for each in items:
        if '###' in each['title']:  # 规定只取标题中‘###'的商品
            count += int(re.search(r'\d+', each['sale']).group())

    return count


def main():
    keywords = input("请输入搜索关键词：")  # 可以为各种商品名称
    length = 10  # 淘宝商品页数
    total = 0

    for each in range(length):
        res = open(keywords, each + 1)
        items = get_item(res)
        total += count_sales(items)  # 销售总量
    print(total)


if __name__ == "__main__":
    main()