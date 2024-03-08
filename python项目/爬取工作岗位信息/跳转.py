from bs4 import BeautifulSoup
from selenium import webdriver
#ActionChain是用来实现一些基础的自动化操作：比如鼠标移动、鼠标点击等，ActionChains可以实现一步操作多个步骤
from selenium.webdriver import ActionChains
import PIL
from PIL import Image
import time
import base64 #Base64编码是从二进制到字符的过程
import threading
import pandas as pd
def my_split(self, s, seps):
    """split移除多个字符"""
    res = [s]
    for sep in seps:
        t = []
        list(map(lambda ss: t.extend(ss.split(sep)), res))
        res = t
    return res


def is_Chinese(self, word):
    """判断是否中文"""
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def get_Cates(self):
    """登陆后默认跳转到我的页面，该段代码用户跳转到淘宝首页并且获取淘宝所有商品类别"""
    # 以上步骤已经实现淘宝登陆，并且进入到我的页面，点击淘宝网首页，跳转到首页
    time.sleep(10)
    # 查看源代码确定"淘宝网首页"的按钮对应的属性，使用click进行点击
    self.driver.find_element_by_xpath('//*[@class="site-nav-menu site-nav-home"]').click()
    # 跳转到首页后首先获取淘宝页面左边栏的所有品类

    # 检测到淘宝为动态JS，使用request库获取网页信息会与网页检查出来的数据不一致，所以需要用selenium包。
    # 辨别网页静态动态的方法：https://www.jianshu.com/p/236fc043db0b
    # 查看源码定位目标内容(即品类栏目)所对应的属性class
    driver_data = self.driver.find_element_by_xpath('//*[@class="screen-outer clearfix"]')
    html_doc = self.driver.page_source
    # driver.quit()
    # 利用beautifulSoup解析网页源代码
    soup = BeautifulSoup(html_doc, "lxml")
    # 找到淘宝主页中所有的主题，对应的class可通过查看class的范围确定
    cate_list = []
    soup_data_list = soup.find("div", attrs={'class': 'service J_Service'})
    # 获取源代码中的文本信息，即淘宝所有的物品主题
    # 通过自定义的split函数获取移除非法字符后的中文字符
    list_tuple = list(("\n", "\\", "\ue62e", "/", "\t", "  ", "              ", " "))
    cate_list = self.my_split(soup_data_list.text, list_tuple)
    # 使用自定义的is_Chinese函数仅保留中文文本
    keep_select = []
    # cate_list_final=[]
    for i in cate_list:
        keep_select = self.is_Chinese(i)
        if keep_select:
            self.cate_list_final.append(i)
    time.sleep(10)
    return self.cate_list_final
