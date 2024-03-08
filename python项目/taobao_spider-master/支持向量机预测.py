from pyspark.ml.classification import LinearSVC
from pyspark.ml.linalg import Vectors
from pyspark.sql import SparkSession, Row
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


# 把文件拆分为标签列和特征列
def splitDF(x):
    rel = {}
    rel['features'] = Vectors.dense(int(x[0]), int(x[1]), int(x[2]), int(x[3]))
    rel['label'] = int(x[4])
    return rel


spark = SparkSession.builder.master("local").appName("double11").getOrCreate()
# 1.加载数据    封装为row对象，转换为dataframe类型，第一列为特征，第二列为标签
training = spark.sparkContext.textFile("hdfs://192.168.40.129:9870/taobao_data/dataset/train_after.txt").map(lambda line: line.split(',')).map(lambda p: Row(**splitDF(p))).toDF()
testing = spark.sparkContext.textFile("hdfs://192.168.40.129:9870/taobao_data/dataset/test_after.txt").map(lambda line: line.split(',')).map(lambda p: Row(**splitDF(p))).toDF()
# 2.构建模型
dsvc = LinearSVC(maxIter=10, regParam=0.1).setFeaturesCol("label").setFeaturesCol('features')
# 3.训练模型
dsvcModel = dsvc.fit(training)
dsvcPredictions = dsvcModel.transform(testing)
# 4.输出预测结果
preRel = dsvcPredictions.select("prediction", "label", "features").collect()
for item in preRel:
    print(str(item['label']) + ',' + str(item['features']) + ',prediction' + str(item['prediction']))
# 准确率
evaluator = MulticlassClassificationEvaluator().setLabelCol("label").setPredictionCol("prediction")
dAccuracy = evaluator.evaluate(dsvcPredictions)
print(dAccuracy)
