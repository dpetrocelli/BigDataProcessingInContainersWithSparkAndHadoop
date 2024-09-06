from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Initialize Spark Session
spark = SparkSession.builder.appName("Adult Income Dataset Analysis").getOrCreate()

# Load the data
df = spark.read.csv("data/adult.data.csv", inferSchema=True, header=True)

# Show the schema to understand data types
df.printSchema()