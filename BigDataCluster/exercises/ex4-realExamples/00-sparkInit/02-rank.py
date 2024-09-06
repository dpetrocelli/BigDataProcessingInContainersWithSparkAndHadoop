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
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, col
# construct a SparkSession, giving it a relevant appName
spark = SparkSession.builder.appName(
    "End of Chapter 2 exercises."
).getOrCreate()

# Create a more complex DataFrame
data = [("James", "Sales", 3000),
        ("Anna", "Sales", 4600),
        ("Lee", "Engineering", 5300),
        ("James2", "Sales", 1600),
        ("Maria", "Engineering", 3000)]
columns = ["EmployeeName", "Department", "Salary"]
df = spark.createDataFrame(data, columns)

# Define window spec
windowSpec = Window.partitionBy("Department").orderBy(col("Salary").desc())

# Apply window function
df.withColumn("rank", rank().over(windowSpec)).show()