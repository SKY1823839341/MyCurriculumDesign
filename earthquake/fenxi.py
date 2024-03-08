
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()

# In[ ]:


df = spark.read.csv("earthquake_cleaned.csv",
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