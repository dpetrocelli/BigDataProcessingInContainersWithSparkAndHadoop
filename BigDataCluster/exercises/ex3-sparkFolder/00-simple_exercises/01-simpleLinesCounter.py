from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Count Lines in HDFS") \
    .master("spark://spark:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

# Leer un archivo de texto desde HDFS
rdd = spark.sparkContext.textFile("hdfs://namenode:9000/user/david/output/part-r-00000")

# Contar el número de líneas
line_count = rdd.count()
print(f"Number of lines: {line_count}")

spark.stop()