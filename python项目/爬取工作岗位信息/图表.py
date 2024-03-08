#coding=utf-8 #使 utf8 中文有效识别
import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.linear_model import LinearRegression
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
xtrain = []
ytrain = []
for i in range(100) :
    xtrain.append([random.randint(150,200)])
    ytrain.append([(xtrain[i][0]-100)*random.randint(85,95)/100])
x = np.array(xtrain)
y = np.array(ytrain)
# print(xtrain)
plt.scatter(x,y,marker='.',color='blue')
plt.title('样本数据散点图')
plt.show()
model = LinearRegression() #创建线性回归模型
model.fit(x.reshape(-1, 1),y) #放入参数,需要将 xtrain 转换为列维度，因为是矩阵运算
#查看结果
# 说明：
#model.coef_
#查看斜率，即 y=ax+b 中的 a
#model.intercept_
#查看截距，即 y=ax+b 中的 b
print('参数 a=%f,b=%f'%(model.coef_,model.intercept_))
print('拟合函数为 y = %f * x + %f'%(model.coef_,model.intercept_))
#进行测试
xtest = np.linspace(0,10,100) #返回一个等差数列
ytest = model.predict(xtest.reshape(-1,1)) #使用 predict 进行预测
ytest = model.predict(xtest.reshape(-1,1)) #使用 predict 进行预测
#新建一个预测值的图表
fig=plt.figure(figsize=(10,5))
plt.scatter(x,y,marker='.',color='k',label=u'原值')
plt.plot(xtest,ytest,color='r',label=u"拟合线")
plt.title(u"回归函数与原值")
plt.legend()
plt.show()