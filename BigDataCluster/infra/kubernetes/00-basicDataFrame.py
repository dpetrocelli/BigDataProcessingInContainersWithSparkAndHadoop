import argparse
from pyspark.sql import SparkSession
from pyspark import SparkContext
import socket

def create_spark_session(env):
    if env == 'local':
        return SparkSession.builder.appName("End of Chapter 2 exercises.").getOrCreate()
    elif env == 'docker':
        return SparkSession.builder \
            .appName("Count Lines in HDFS") \
            .master("spark://spark:7077") \
            .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
            .getOrCreate()
    elif env == 'kubernetes':
        return SparkSession.builder \
            .appName("Count Lines in HDFS") \
            .master("spark://192.168.1.33:7077") \
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

def log_node_information(df):
    """
    This function adds the node (executor) information to each partition processed.
    """
    def process_partition(iterator):
        # Get the hostname of the executor node
        executor_node = socket.gethostname()
        # Yield each row with the executor node information
        for row in iterator:
            yield (row.Name, row.Age, executor_node)
    
    # Apply the process_partition function to each partition
    df_with_node_info = df.rdd.mapPartitions(process_partition).toDF(["Name", "Age", "Executor_Node"])
    return df_with_node_info

def run_spark_job(env):
    # PASO 1 - armar un set de datos / leer un set de datos (input)
    data = [("James", 34), ("Anna", 28), ("Lee", 23), ("David", 105)]
    columns = ["Name", "Age"]
    spark = create_spark_session(env)
    
    # Increase the display width for the DataFrame columns
    spark.conf.set("spark.sql.repl.eagerEval.truncate", 0)
    
    # Crear un DataFrame
    df = spark.createDataFrame(data, columns)
    
    # Mostrar la estructura del DataFrame
    print(f"Running Spark job in {env} environment.")
    df.printSchema()

    # Paso 2 - Transformación / selección (código) con información de nodos
    print("Adding node information to the DataFrame")
    df_with_node_info = log_node_information(df)
    df_with_node_info.show(truncate=False)  # Ensure full columns are shown

def main(params):
    env = params.get('entorno', 'local')
    num_executions = params.get('num_executions', 1)
    
    # Ejecutar en paralelo
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_executions) as executor:
        futures = [executor.submit(run_spark_job, env) for _ in range(num_executions)]
    
    # Esperar a que todos terminen
    for future in futures:
        future.result()

if __name__ == "__main__":
    import argparse
    
    def parse_args():
        parser = argparse.ArgumentParser(description='Run PySpark script with specified parameters.')
        
        # Add arguments with default values
        parser.add_argument('--entorno', type=str, default='local', help='The environment to run the script (local, docker, kubernetes, aws).')
        parser.add_argument('--num-executions', type=int, default=1, help='The number of times to run the script.')
        
        args = parser.parse_args()
        
        # Return parsed arguments as a dictionary
        return vars(args)
    
    params = parse_args()
    main(params)
