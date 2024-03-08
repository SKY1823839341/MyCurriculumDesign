import pandas as pd
import pymysql
from pyecharts import Bar,Pie,Line,Scatter,Map
TABLE_COMMENTS = '****'
TABLE_USERS = '****'
DATABASE = '****'
conn = pymysql.connect(host='localhost', user='****', passwd='****', db=DATABASE, charset='utf8mb4')
sql_users = 'SELECT id,gender,age,city FROM '+TABLE_USERS
sql_comments = 'SELECT id,time FROM '+TABLE_COMMENTS
comments = pd.read_sql(sql_comments, con=conn)
users = pd.read_sql(sql_users, con=conn)
# 评论时间(按天)分布分析
comments_day = comments['time'].dt.date
data = comments_day.id.groupby(comments_day['time']).count()
line = Line('评论时间(按天)分布')
line.use_theme('dark')
line.add(
    '',
    data.index.values,
    data.values,
    is_fill=True,
)
line.render(r'./评论时间(按天)分布.html')
# 评论时间(按小时)分布分析
comments_hour = comments['time'].dt.hour
data = comments_hour.id.groupby(comments_hour['time']).count()
line = Line('评论时间(按小时)分布')
line.use_theme('dark')
line.add(
    '',
    data.index.values,
    data.values,
    is_fill=True,
)
line.render(r'./评论时间(按小时)分布.html')
# 评论时间(按周)分布分析
comments_week = comments['time'].dt.dayofweek
data = comments_week.id.groupby(comments_week['time']).count()
line = Line('评论时间(按周)分布')
line.use_theme('dark')
line.add(
    '',
    data.index.values,
    data.values,
    is_fill=True,
)
line.render(r'./评论时间(按周)分布.html')
# 用户年龄分布分析
age = users[users['age']>0]  # 清洗掉年龄小于1的数据
age = age.id.groupby(age['age']).count()    # 以年龄值对数据分组
Bar = Bar('用户年龄分布')
Bar.use_theme('dark')
Bar.add(
    '',
    age.index.values,
    age.values,
    is_fill=True,
)
Bar.render(r'./用户年龄分布图.html')   # 生成渲染的html文件
# 用户地区分布分析
# 城市code编码转换
def city_group(cityCode):
    city_map = {
        '11': '北京',
        '12': '天津',
        '31': '上海',
        '50': '重庆',
        '5e': '重庆',
        '81': '香港',
        '82': '澳门',
        '13': '河北',
        '14': '山西',
        '15': '内蒙古',
        '21': '辽宁',
        '22': '吉林',
        '23': '黑龙江',
        '32': '江苏',
        '33': '浙江',
        '34': '安徽',
        '35': '福建',
        '36': '江西',
        '37': '山东',
        '41': '河南',
        '42': '湖北',
        '43': '湖南',
        '44': '广东',
        '45': '广西',
        '46': '海南',
        '51': '四川',
        '52': '贵州',
        '53': '云南',
        '54': '西藏',
        '61': '陕西',
        '62': '甘肃',
        '63': '青海',
        '64': '宁夏',
        '65': '新疆',
        '71': '台湾',
        '10': '其他',
    }
    return city_map[cityCode[:2]]
city = users['city'].apply(city_group)
city = city.id.groupby(city['city']).count()
map_ = Map('用户地区分布图')
map_.add(
    '',
    city.index.values,
    city.values,
    maptype='china',
    is_visualmap=True,
    visual_text_color='#000',
    is_label_show=True,
)
map_.render(r'./用户地区分布图.html')