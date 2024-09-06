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

def non_type_columns(df, target_type="string"):
    # define the target type we (don't) want to count

    # Get the columns of the target type
    target_columns = [col for col, dtype in df.dtypes if dtype != target_type]

    # Count the number of columns of the target type
    num_columns = len(target_columns)

    return num_columns

exo2_2_df = spark.createDataFrame([["test", "more test", 10_000_000_000]], ["one", "two", "three"])

target_type = "string"
print(f"Number of non-{target_type} columns: {non_type_columns(exo2_2_df, target_type)}")

