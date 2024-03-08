import random
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

plt.rcParams['font.sans-serif'] = ['SimHei']
# 训练集
train_x = []
train_y = []
for i in range(100):
    train_x.append([random.randint(150, 200)])
    train_y.append([(train_x[i][0] - 100) * random.randint(85, 95) / 100])
# 测试集
test_x = []
test_y = []
for i in range(30):
    test_x.append([random.randint(150, 200)])
    test_y.append([(test_x[i][0] - 100) * random.randint(85, 95) / 100])
plt.scatter(train_x, train_y, color='red')

# 训练单变量回归学习器
regressor = LinearRegression()
regressor.fit(train_x, train_y)

# 预测结果
result = regressor.predict(test_x)

# 可视化图表
plt.scatter(train_x, train_y, color='red')
plt.plot(train_x, regressor.predict(train_x), color='blue')
plt.title('散点图与回归方程')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
