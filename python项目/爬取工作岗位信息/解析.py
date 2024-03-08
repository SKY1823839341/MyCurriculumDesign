from bs4 import BeautifulSoup
import time

def search_Taobao(self, cate):
    print("正在搜索的品类是：%s" % cate)

    # 点击淘宝网首页跳转到首页页面，不管是在我的首页和各类别搜索下的首页，需要点击跳回淘宝网首页的class不变，所以把点击首页的代码放在这里"
    time.sleep(10)

    # 在首页搜索栏输入需要搜索的内容，并点击搜索
    # 一个输入框两个input，两个input重叠的情况，先单点value提示字的input后，才会显示真正要输入框的input，这时再向这个input输值
    # 首先需要点击搜索框'//*[@class="search-combobox-input-wrap"]'，使得其为可交互状态
    self.driver.find_element_by_xpath('//*[@class="search-combobox-input-wrap"]').click()
    # 再找到输入搜索框的class名，输入要搜索的内容，找到搜索对应的class点击搜索
    driver_input_data = self.driver.find_element_by_xpath('//*[@class="search-combobox-input"]')
    # 填写需要搜索的品类 不知道为什么 带着cookies这一步还是需要登陆
    # driver_input_data.send_keys('女装')
    driver_input_data.send_keys(cate)
    # 停顿3秒，否则速度过快会被识别出为爬虫
    time.sleep(8)
    # 查找页面上”搜索“的按钮
    try:
        submit = self.driver.find_element_by_xpath('//*[@class="search-button"]')
        submit.click()
    except:
        pass

    time.sleep(5)


def get_Catinfo(self, cate):
    # self.login_first()
    time.sleep(20)
    self.search_Taobao(cate)
    # 登陆后进入了对应搜索品类的页面，获取按销量降序后的第一页的商品信息
    time.sleep(50)

    # 查找到按销量排序的元素，并进行点击得到降序排列的商品信息
    submit_order = self.driver.find_element_by_xpath('//*[@class="J_Ajax link  "]')
    submit_order.click()
    time.sleep(5)
    # 获取整个页面源码
    html_doc = self.driver.page_source

    # 通过页面源码获取各个商品的必要信息
    soup = BeautifulSoup(html_doc, "lxml")
    shop_data_list = soup.find('div', class_="grid g-clearfix").find_all_next('div', class_="items")
    for shop_data in shop_data_list:
        # 不同的信息分布在以下两个不同的class下
        shop_data_a = shop_data.find_all("div", class_="ctx-box J_MouseEneterLeave J_IconMoreNew")
        shop_data_b = shop_data.find_all("div", class_="pic-box J_MouseEneterLeave J_PicBox")
        for goods_contents_b in shop_data_b:
            # 另起一列为爬取的商品类别
            self.shop_cate_list.append(cate)
            # 0.获取商品名称
            goods_name = goods_contents_b.find("div", class_="pic").find_all("img", class_="J_ItemPic img")[0]["alt"]
            self.goods_name_list.append(goods_name)
            # 0.获取商品图片
            goods_pic = goods_contents_b.find("div", class_="pic").find_all("img", class_="J_ItemPic img")[0]["src"]
            self.goods_pic_list.append(goods_pic)

        for goods_contents_a in shop_data_a:
            # 2.获取商品价格trace-price
            goods_price = goods_contents_a.find_all("a", class_="J_ClickStat")[0]["trace-price"]
            self.goods_price_list.append(goods_price)
            # goods_price = goods_contents_a.find("div",class_="price g_price g_price-highlight")
            # goods_price_list.append(goods_price)
            # 1.获取商品销量
            goods_salenum = goods_contents_a.find("div", class_="deal-cnt")
            self.goods_salenum_list.append(goods_salenum)
            # 2.获取商品id
            goods_id = goods_contents_a.find_all("a", class_="J_ClickStat")[0]["data-nid"]
            self.goods_id_list.append(goods_id)
            # 2.获取商品链接
            goods_href = goods_contents_a.find_all("a", class_="J_ClickStat")[0]["href"]
            self.goods_href_list.append(goods_href)
            # 2.获取店铺名称
            goods_store = goods_contents_a.find("a", class_="shopname J_MouseEneterLeave J_ShopInfo").contents[3]
            # goods_store = goods_contents.find_all("span",class_="dsrs")
            self.goods_store_list.append(goods_store)
            # 4.获取店铺地址
            goods_address = goods_contents_a.find("div", class_="location").contents
            self.goods_address_list.append(goods_address)

            # 爬取结果整理成dataframe形式
    for j in range(min(
            len(self.goods_name_list), len(self.goods_id_list), len(self.goods_price_list)
            , len(self.goods_salenum_list), len(self.goods_pic_list), len(self.goods_href_list)
            , len(self.goods_store_list), len(self.goods_address_list)
    )
    ):
        self.data.append(
            [self.shop_cate_list[j], self.goods_name_list[j], self.goods_id_list[j], self.goods_price_list[j]
                , self.goods_salenum_list[j], self.goods_pic_list[j], self.goods_href_list[j]
                , self.goods_store_list[j], self.goods_address_list[j]
             ])
    # out_df = pd.DataFrame(self.data,columns=['goods_name'
    #                                  ,'goods_id'
    #                                  ,'goods_price'
    #                                 ,'goods_salenum'
    #                                  ,'goods_pic'
    #                                  ,'goods_href'
    #                                  ,'goods_store'
    #                                  ,'goods_address'])

    # self.Back_Homepage()
    # 如果不休眠的话可能会碰到页面还没来得及加载就点击造成点击错误
    time.sleep(20)
    self.driver.find_element_by_xpath('//*[@class="site-nav-menu site-nav-home"]').click()
    return self.data
