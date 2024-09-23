# Create Spark Session

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Create DF on fly") \
    .master("spark://spark:7077") \
    .getOrCreate()

# Create an Dataframe from range of values
df_range_1 = spark.range(5)
df_range_1.show(5, truncate = False)

# You can optionally specify start, end and steps as well
df_range_2 = spark.range(start = 1, end = 10, step = 2)
df_range_2.show(10, False)