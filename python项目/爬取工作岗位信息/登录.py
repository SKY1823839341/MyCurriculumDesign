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


def login_first(self):
    # 淘宝首页链接 一开始使用https时request.get返回status_code为502
    # pageview_url = 'http://www.taobao.com/?spm=a1z02.1.1581860521.1.CPoW0X' 类属性中已经定义
    # PhantomJS与Chrome的差别在于Chrome可以启动浏览器，观察到代码操作的每一个步骤进行的页面操作PhantomJS模拟一个虚拟浏览器，即在不打开浏览器的前提下对浏览器进行操作
    # driver = webdriver.PhantomJS()
    # driver = webdriver.Chrome() 类属性中已经定义
    # 在get()步加载时间会很长 不知道是不是网络的问题，所以限制加载20秒以后停止加载
    self.driver.set_page_load_timeout(40)
    self.driver.set_script_timeout(40)
    try:
        self.driver.get(self.pagelogin_url)
    except:
        print("页面加载太慢，停止加载，继续下一步操作")
        self.driver.execute_script("window.stop()")
    # 此处需要设置等待，不然再页面缓存完之前就执行以下语句会导致找不到元素
    time.sleep(40)
    # 找到登陆按钮并点击
    # 原本在获取cookies后通过request库带着cookies访问需要登陆才可访问的页面，但是对于webdriver没有作用
    # wedriver元素定位的各种方法https://www.cnblogs.com/yufeihlf/p/5717291.html
    # 网页自动化最基本的要求就是先定位到各个元素，然后才能对各元素进行操作(输入、点击、清除、提交等)
    # XPath是一种XML文档中定位元素的语言。该定位方式也是比较常用的定位方式
    # 8.1通过属性定位元素 find_element_by_xpath("//标签名[@属性='属性值']")
    # 可能的属性：id、class、name、maxlength
    # 通过标签名定位属性：所有input标签元素find_element_by_xpath("//input")
    # 通过父子定位属性：所有input标签元素find_element_by_xpath("//span/input")
    # 通过元素内容定位：find_element_by_xpath("//p[contains(text(),'京公网')]")
    # 获取id="login"的标签下第一个div//’表示从任意节点搜索不必从根节点一节一节
    # 如何找到对应按钮或者页面的xpath内容：检查页面，点击左上角箭头标志，
    # 然后点击目标内容，会自动定位到Elements中该内容的标签属性，右键COPY Xpath即可
    # self.driver.find_element_by_xpath('//*[@class="btn-login ml1 tb-bg weight"]').click()

    # time.sleep(40)
    # 下行代码的目的：查找二维码登陆的源代码点击使用二维码登陆
    try:
        # 找到二维码登陆对应的属性并点击二维码登陆
        driver_data = self.driver.find_element_by_xpath('//*[@id="login"]/div[1]/i').click()

    except:
        pass
    # 通常需要停顿几秒钟，不然会被检测到是爬虫
    # 等待网页缓冲
    time.sleep(20)
    # 执行JS获得canvas的二维码
    # .通过tag_name定位元素
    JS = 'return document.getElementsByTagName("canvas")[0].toDataURL("image/png");'
    im_info = self.driver.execute_script(JS)  # 执行JS获取图片信息
    im_base64 = im_info.split(',')[1]  # 拿到base64编码的图片信息
    im_bytes = base64.b64decode(im_base64)  # 转为bytes类型
    time.sleep(2)
    with open('E:/学习‘/login.png', 'wb') as f:
        # 生成二维码保存
        f.write(im_bytes)
        f.close()
    # 打开二维码图片，需要手动扫描二维码登陆
    t = threading.Thread(target=self.opening, args=('E:/学习‘/login.png',))
    t.start()
    print("Logining...Please sweep the code!\n")
    # 获取登陆后的Cookie(只看到用户名，没有看到账号和密码)
    while (True):
        c = self.driver.get_cookies()
        if len(c) > 20:  # 登陆成功获取到cookies
            cookies = {}
            # 下面隐藏是因为对cookies只保留了name和value以后只能用于request，不能用于webdriver的add_cookies作用不然会报错InvalidCookieDomainException
            # for i in range(len(c)):
            # cookies[c[i]['name']] = c[i]['value']
            self.driver.close()
            print("Login in successfully!\n")
            # return cookies
        return c
        time.sleep(10)
