import re
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import *

# Initialize Spark Session
spark = SparkSession.builder.appName("Adult Income Dataset").getOrCreate()

# Function to read and parse the names file
def parse_names_file(filepath):
    attributes = []
    with open(filepath, 'r') as file:
        for line in file:
            if ":" in line and not line.startswith('|'):  # Ensuring it's a field definition
                attr_name = line.split(":")[0].strip()
                attributes.append(attr_name)
    return attributes

# Define the schema dynamically based on the names file
def create_schema(attribute_names):
    schema = StructType()
    for attr_name in attribute_names:
        # Assuming all fields as StringType for simplicity; adjust types as needed
        schema.add(StructField(attr_name, StringType(), True))
    return schema

# Path to the names file
names_file_path = 'data/adult.names'
attributes = parse_names_file(names_file_path)
schema = create_schema(attributes)
print (schema)
print ("----------")
# Path to the CSV data file
data_file_path = 'data/adult.data.csv'

# Load the data with the dynamically created schema
df = spark.read.csv(data_file_path, schema=schema, header=False)

# Show the DataFrame to verify it loaded correctly
df.show(5)

# Check for missing values
df.select([count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in df.columns]).show()

# Create a new column "label" where income ">50K" is 1, and "<=50K" is 0
df = df.withColumn("label", when(col("income").contains(">50K"), 1).otherwise(0))

# Group by income to see average age and maximum education num
result = df.groupBy("income").agg(avg("age").alias("average_age"),
                                  max("education_num").alias("max_education_num"))

# Show the result
result.show()

# Stop the Spark session
spark.stop()