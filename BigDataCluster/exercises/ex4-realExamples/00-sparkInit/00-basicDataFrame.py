import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def create_spark_session(env):
    if env == 'local':
        return SparkSession.builder.appName("End of Chapter 2 exercises.").getOrCreate()
    elif env == 'docker':
        return SparkSession.builder \
            .appName("Count Lines in HDFS") \
            .master("spark://spark:7077") \
            .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
            .getOrCreate()
    elif env == 'aws':
        return SparkSession.builder \
            .appName("AWS Spark Example") \
            .master("yarn") \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .config("spark.hadoop.fs.s3a.access.key", "<YOUR_AWS_ACCESS_KEY>") \
            .config("spark.hadoop.fs.s3a.secret.key", "<YOUR_AWS_SECRET_KEY>") \
            .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
            .config("spark.hadoop.fs.defaultFS", "s3a://your-bucket/") \
            .getOrCreate()
    else:
        raise ValueError(f"Unsupported environment: {env}")

def parse_args():
    parser = argparse.ArgumentParser(description='Run PySpark script with specified parameters.')
    
    # Add arguments with default values
    parser.add_argument('--entorno', type=str, default='local', help='The environment to run the script (local, docker, aws).')
    
    args = parser.parse_args()
    
    # Parse key-value arguments
    params = {}
    for param in vars(args):
        if '=' in getattr(args, param):
            key, value = getattr(args, param).split('=')
            params[key.strip()] = value.strip()
        else:
            params[param] = getattr(args, param)
    
    return params

def main(params):
    env = params.get('entorno', 'local')
    
    # PASO 1 - armar un set de datos / leer un set de datos (input)
    data = [("James", 34), ("Anna", 28), ("Lee", 23), ("David", 105)]
    columns = ["Name", "Age"]
    spark = create_spark_session(env)
    
    # Crear un DataFrame
    df = spark.createDataFrame(data, columns)
    
    # Mostrar la estructura del DataFrame
    print("Mi dataframe tiene una estructura:")
    df.printSchema()

    # Paso 2 - Transformación / selección (código)
    print("Filtering by age > 25")
    resultado = df.filter(df["Age"] > 25)
    resultado.show()

if __name__ == "__main__":
    params = parse_args()
    main(params)
