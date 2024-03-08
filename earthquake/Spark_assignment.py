#!/usr/bin/env python
#coding: utf-8


import pandas as pd
import numpy as np

rawData = pd.read_csv('D:/A.Lee/Three/Bigdata/earthquake/earthquake.csv')
rawData.head(10)
rawData.info()
# ## 清洗数据
# 这些属性都没有缺失值，但还存在一些格式不一致的现象，需要进行格式转换。
# ### 清洗Date数据
# Pandas提供了to_datetime()方法，可以将不同的日期格式转换为datetime 类型。设置errors='coerce'参数，遇到不能转换的格式时将其置为NaN。
# In[ ]:
rawData['Structed Date'] = pd.to_datetime(rawData['Date'],
                                          format="%m/%d/%Y",
                                          errors='coerce').dt.date

rawData.loc[3378, 'Structed Date'] = '1975-02-23'
rawData.loc[7512, 'Structed Date'] = '1985-04-28'
rawData.loc[20650, 'Structed Date'] = '2011-03-13'

del rawData['Date']

# ### 清洗Time数据

# In[ ]:


# 对时间进行格式转换
rawData['Structed Time'] = pd.to_datetime(rawData['Time'],
                                          format="%H:%M:%S",
                                          errors='coerce').dt.time

# In[ ]:

# In[ ]:


rawData.loc[3378, 'Structed Time'] = '2:58:41'
rawData.loc[7512, 'Structed Time'] = '2:53:41'
rawData.loc[20650, 'Structed Time'] = '2:23:34'

# In[ ]:


del rawData['Time']

# 修改完成后，将列名重新改回Date和Time。

# In[ ]:


rawData.rename(columns={'Structed Date': 'Date', 'Structed Time': 'Time'},
               inplace=True)
rawData.head(10)

# ### 根据经纬度获取地名
# 高德地图的逆地理编码API服务可以根据经纬度查询出该位置的地名信息。经过测试，这个API对于中国境外的坐标常常不能准确地返回结果，因此只获取在中国境内的坐标信息。坐标在中国境外时，就返回一个空值。如果坐标在海上，就获取海域的名称（如南海）；如果在陆地上，就获取省份的名称。

# In[ ]:


import requests
import json


def getProvince(lon, lat):
    u1 = 'http://restapi.amap.com/v3/geocode/regeo?output=json&'
    key = '&key=c8a747ca0df252b682af24300c69ba76'
    location = 'location=' + str(lon) + ',' + str(lat)
    url = u1 + location + key
    res = requests.get(url)
    json_data = json.loads(res.text)
    regeoinfo = json_data['regeocode']['addressComponent']

    if 'country' in regeoinfo and regeoinfo['country'] == '中国':
        if 'province' in regeoinfo and regeoinfo['province']:
            return regeoinfo['province']
        elif 'seaArea' in regeoinfo and regeoinfo['seaArea']:
            return regeoinfo['seaArea']

    return None


# 为每个经纬度坐标获取位置信息，需要花费十分钟左右的时间。

# In[ ]:


# for i in range(23411):
#     lon = rawData.loc[i, 'Longitude']
#     lat = rawData.loc[i, 'Latitude']
#     rawData.loc[i, 'Area'] = getProvince(lon, lat)
#     print(i)



# rawData["Area"].unique()
#
# # In[ ]:
#
#
# rawData.loc[rawData.Area.notnull()].sample(5)

# 查看Type属性中是否有异常。

# In[ ]:


# rawData.Type.unique()

# 至此，数据清洗工作完成。将数据保存到文件earthquake_cleaned.csv中，编码设为utf-8，防止spark读取的时候出现中文乱码。

# In[ ]:


# rawData.to_csv("earthquake_cleaned.csv",
#                encoding='utf-8',
#                index=False)

# 将其上传到HDFS，以便Spark对其进行数据分析。
# ## 数据分析
#

# In[ ]:


from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()

# In[ ]:


df = spark.read.csv("input/earthquake_cleaned.csv",
                    header=True,
                    inferSchema=True)
df = df.repartition(1)
df.show(10)

print("1")
# 显示数据部分行后发现Spark读取csv文件时将Date列读取成了1965-01-02 00:00:00的格式，因此还需要进一步对数据进行处理。对Date属性进行拆分，丢掉后面00:00:00的部分。

# In[ ]:


from pyspark.sql.functions import split

df = df.withColumn("newDate",
                   split(df['Date'], " ")[0]).drop("Date")
df.show(10)

# 这里将newDate命名为Date，这样数据就跟一开始预期的样子相一致了。

# In[ ]:


df = df.withColumnRenamed("newDate", "Date")
df.show(10)

# ### 将数据按年份、月份、日期计数
# 要完成这个目标就要对Date属性进行拆分，就能得到年月日的信息。

# In[ ]:


attrsName = ['Year', 'Month', 'Day']
for i in range(len(attrsName)):
    df = df.withColumn(attrsName[i],
                       split(df['Date'], "-")[i])
df.show(10)

# In[ ]:


df.printSchema()

# 此时年月日信息都是字符串类型，将其改为整型。

# In[ ]:


for x in attrsName:
    df = df.withColumn(x, df[x].cast('int'))

df.printSchema()

# In[ ]:


df.show(10)

# In[ ]:


countByYear = df.groupBy("Year").count().orderBy("Year")
countByYear.toPandas().to_csv("countByYear.csv",
                              encoding='utf-8',
                              index=False)
countByYear.show(10)

# In[ ]:


countByMonth = df.groupBy("Month").count().orderBy("Month")
countByMonth.toPandas().to_csv("countByMonth.csv",
                               encoding='utf-8',
                               index=False)
countByMonth.show(10)

# In[ ]:


countByDay = df.groupBy("Day").count().orderBy("Day")
countByDay.toPandas().to_csv("countByDay.csv",
                             encoding='utf-8',
                             index=False)
countByDay.show(10)

# ### 每个省份（海域）发生重大地震的次数
# 首先筛选出发生在中国境内地震的数据，之后画图用。

# In[ ]:


earthquakeC = df.filter("Area is not null")
earthquakeC.toPandas().to_csv("earthquakeC.csv",
                              encoding='utf-8',
                              index=False)
earthquakeC.show(10)

# 按Area属性对数据进行分组计数，要注意只筛选Area非空的数据。

# In[ ]:


countByArea = earthquakeC.groupBy("Area").count()
countByArea.toPandas().to_csv("countByArea.csv",
                              encoding='utf-8',
                              index=False)
countByArea.show(10)

# ### 不同类型地震的数量
# 分别计算出世界范围内和中国境内的不同地震类型的数量。

# In[ ]:


countByTypeC = earthquakeC.groupBy("Type").count()
countByTypeC.toPandas().to_csv("countByTypeC.csv",
                               encoding='utf-8',
                               index=False)
countByTypeC.show()

# In[ ]:


countByType = df.groupBy("Type").count()
countByType.toPandas().to_csv("countByType.csv",
                              encoding='utf-8',
                              index=False)
countByType.show()

# ### 震级前500的地震
# 根据震级进行降序排序，个人比较关注离现在更近的地震，因此再根据年份降序排列。由于使用take(500)之后返回一个RDD，其中每个元素都是Row对象。此时根据这个RDD生成DataFrame，再将其保存为csv文件。

# In[ ]:


mostPow = df.sort(df["Magnitude"].desc(), df["Year"].desc()).take(500)
mostPowDF = spark.createDataFrame(mostPow)
mostPowDF.toPandas().to_csv("mostPow.csv",
                            encoding='utf-8',
                            index=False)
mostPowDF.show(10)

# ### 震源深度前500的地震
# 这个步骤跟上面的差不多。区别在于当震源深度相同时，将震级更高的地震排在前面。

# In[ ]:


mostDeep = df.sort(df["Depth"].desc(), df["Magnitude"].desc()).take(500)
mostDeepDF = spark.createDataFrame(mostDeep)
mostDeepDF.toPandas().to_csv("mostDeep.csv",
                             encoding='utf-8',
                             index=False)
mostDeepDF.show(10)

# ### 震级与震源深度的关系
# 把DataFrame中的Magnitude属性和Depth属性选出来存到csv文件中。

# In[ ]:


df.select(df["Magnitude"], df["Depth"]).toPandas().to_csv("powDeep.csv",
                                                          encoding='utf-8',
                                                          index=False)

# 数据分析基本完成，此时将df也保存到csv文件中，用于数据可视化。

# In[ ]:


df.toPandas().to_csv("earthquake1.csv",
                     encoding='utf-8',
                     index=False)

# ## 数据可视化
# 可视化工具使用plotly，可以绘制可交互的图表，并可以完美兼容Jupyter Notebook。另外，用WordCloud绘制词云。
# ### 数据总览
# 首先将所有数据绘制到地图上。根据我们的常识，地震震级越高，地震的破坏力呈几何级数上升。为了画出更直观的图，使用exp(Magnitude)/100作为每个坐标的大小。

# In[ ]:


import plotly.express as px
import plotly.io as pio

data = pd.read_csv('earthquake1.csv')

fig1 = px.scatter_geo(data,
                      color=data.Magnitude,
                      color_continuous_scale=px.colors.sequential.Inferno,
                      lon=data.Longitude,
                      lat=data.Latitude,
                      hover_name=data.Type,
                      hover_data=["Longitude",
                                  "Latitude",
                                  "Date",
                                  "Time",
                                  "Magnitude",
                                  "Depth"
                                  ],
                      size=np.exp(data.Magnitude) / 100,
                      projection="equirectangular",
                      title='1965-2016年全球重大地震'
                      )
fig1.show()
pio.write_html(fig1, 'fig1.html')

# 可以很清楚地看到地震带的分布，重大地震也主要发生在地震带上。
# 
# plotly还可以实现以某个属性为帧生成动画。

# In[ ]:


fig2 = px.scatter_geo(data,
                      color=data.Magnitude,
                      color_continuous_scale=px.colors.sequential.Inferno,
                      lon=data.Longitude,
                      lat=data.Latitude,
                      animation_frame=data.Year,
                      hover_name=data.Type,
                      hover_data=["Longitude",
                                  "Latitude",
                                  "Date",
                                  "Time",
                                  "Magnitude",
                                  "Depth"
                                  ],
                      size=np.exp(data.Magnitude) / 100,
                      projection="equirectangular",
                      title='1965-2016年全球重大地震'
                      )
fig2.show()
pio.write_html(fig2, 'fig2.html')

# ### 每年份、月份、天份发生重大地震的次数
# 根据这些数据画出柱状图。

# In[ ]:


cntByYear = pd.read_csv('countByYear.csv')

fig3 = px.bar(cntByYear,
              x="Year",
              y="count",
              text="count",
              title='1965-2016年每年发生重大地震的次数'
              )
fig3.show()
pio.write_html(fig3, 'fig3.html')

# 前十多年的地震次数明显少于之后的，可能是早期地震监测技术比较落后的原因。

# In[ ]:


cntByMonth = pd.read_csv('countByMonth.csv')

fig4 = px.bar(cntByMonth,
              x="Month",
              y="count",
              text="count",
              title='1965-2016年每月发生重大地震的次数'
              )
fig4.show()
pio.write_html(fig4, 'fig4.html')

# 每月发生的地震次数基本上一致。

# In[ ]:


cntByDay = pd.read_csv('countByDay.csv')

fig5 = px.bar(cntByDay,
              x="Day",
              y="count",
              text="count",
              title='1965-2016年每个日期发生重大地震的次数'
              )
fig5.show()
pio.write_html(fig5, 'fig5.html')

# 由于有一半的月份没有31号，因此31号的次数明显较少。

# ### 1955-2016年中国境内不同省份的重大地震次数
# 首先画出中国境内地震数据的总览。

# In[ ]:


dataC = pd.read_csv('earthquakeC.csv')
dataC.head(10)

# In[ ]:


fig6 = px.scatter_geo(dataC,
                      color=dataC.Magnitude,
                      color_continuous_scale=px.colors.sequential.Inferno,
                      lon=dataC.Longitude,
                      lat=dataC.Latitude,
                      scope='asia',
                      center={'lon': 105.73, 'lat': 29.6},
                      hover_name=dataC.Type,
                      hover_data=["Longitude",
                                  "Latitude",
                                  "Date",
                                  "Time",
                                  "Magnitude",
                                  "Depth"
                                  ],
                      size=np.exp(dataC.Magnitude) / 100,
                      title='1965-2016年中国境内重大地震'
                      )
fig6.show()
pio.write_html(fig6, 'fig6.html')

# 再根据每个省份（海域）的数据生成柱状图和词云图。

# In[ ]:


cntByArea = pd.read_csv('countByArea.csv')

fig7 = px.bar(cntByArea,
              x="Area",
              y="count",
              text="count",
              title='1965-2016年各省份（海域）发生重大地震的次数'
              )
fig7.show()
pio.write_html(fig7, 'fig7.html')

# 生成词云图之前要记得下载一个中文字体，放入代码目录中，否则中文会出现乱码。

# In[ ]:


from wordcloud import WordCloud
import matplotlib.pyplot as plt

freq = dict(zip(cntByArea["Area"], cntByArea["count"]))

# In[ ]:


wc = WordCloud(font_path="MSYH.TTC",
               prefer_horizontal=0.7,
               width=800,
               height=600,
               scale=4,
               min_font_size=10,
               background_color="white",
               max_words=30)
wc.generate_from_frequencies(freq)
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()
wc.to_file('wordcloud.png')

# ### 震级前500的重大地震

# In[ ]:


pow500 = pd.read_csv('mostPow.csv')

fig8 = px.scatter_geo(pow500,
                      color=pow500.Magnitude,
                      color_continuous_scale=px.colors.sequential.Inferno,
                      lon=pow500.Longitude,
                      lat=pow500.Latitude,
                      hover_name=pow500.Type,
                      hover_data=["Longitude",
                                  "Latitude",
                                  "Date",
                                  "Time",
                                  "Magnitude",
                                  "Depth"
                                  ],
                      size=np.exp(pow500.Magnitude) / 100,
                      title='1965-2016年震级前500的重大地震'
                      )
fig8.show()
pio.write_html(fig8, 'fig8.html')

# ### 震源深度前500的重大地震

# In[ ]:


deep500 = pd.read_csv('mostDeep.csv')

fig9 = px.scatter_geo(deep500,
                      color=deep500.Depth,
                      color_continuous_scale=px.colors.sequential.Inferno,
                      lon=deep500.Longitude,
                      lat=deep500.Latitude,
                      hover_name=deep500.Type,
                      hover_data=["Longitude",
                                  "Latitude",
                                  "Date",
                                  "Time",
                                  "Magnitude",
                                  "Depth"
                                  ],
                      title='1965-2016年震源深度前500的重大地震'
                      )
fig9.show()
pio.write_html(fig9, 'fig9.html')

# ### 不同类型的地震
# Type共有四个元素，如下：

# In[ ]:


cntByType = pd.read_csv('countByType.csv')
cntByType["Type"].unique()

# 可以根据Type画出饼状图。

# In[ ]:


fig10 = px.pie(cntByType,
               names="Type",
               values="count",
               title='1965-2016年世界范围内不同类型的地震占比'
               )
fig10.show()
pio.write_html(fig10, 'fig10.html')

# 可见99.2%是天然形成的地震，不到1%是核爆或者爆炸形成的。同样地也可以画出中国境内不同类型的地震占比。

# In[ ]:


cntByTypeC = pd.read_csv('countByTypeC.csv')

fig11 = px.pie(cntByTypeC,
               names="Type",
               values="count",
               title='1965-2016年中国境内不同类型的地震占比'
               )
fig11.show()
pio.write_html(fig11, 'fig11.html')

# ### 震级和震源深度的关系


powAndDep = pd.read_csv('powDeep.csv')

fig12 = px.scatter(powAndDep,
                   x="Depth",
                   y="Magnitude",
                   title='震级与震源深度的关系'
                   )
fig12.show()
pio.write_html(fig12, 'fig12.html')

# 可见震级8.0以上的地震大部分震源深度较浅，但从整体看地震的震级与震源深度的相关性不大。
# 
# 至此数据可视化结束。
