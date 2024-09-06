from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    explode,
    greatest,
    length,
    lower,
    regexp_extract,
    split
)
from pyspark.sql.utils import AnalysisException
# construct a SparkSession, giving it a relevant appName
spark = SparkSession.builder.appName(
    "End of Chapter 2 exercises."
).getOrCreate()

# Create a DataFrame
data = [("James", 34), ("Anna", 28), ("Lee", 23)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)

# Show the DataFrame
print ("all df")
df.show()

# Select specific columns
print ("Only names")
df.select("Name").show()

# Filter rows based on condition
print ("filtering by age > 25")
df.filter(df["Age"] > 25).show()