from pyspark.sql import SparkSession
from py4j.java_gateway import java_import

def list_hdfs_path(hdfs, path, level=0):
    """ Recursively list files and directories in HDFS with indentation. """
    try:
        # Get the status of the path
        file_status_list = hdfs.listStatus(path)
        
        # Iterate through each item in the directory
        for file_status in file_status_list:
            # Get the path of the item
            item_path = file_status.getPath().toString()
            # Determine indentation based on directory depth
            indent = '  ' * level
            
            if file_status.isDirectory():
                print(f"{indent}Directory: {item_path}")
                # Recursively list contents of the directory
                list_hdfs_path(hdfs, file_status.getPath(), level + 1)
            elif file_status.isFile():
                print(f"{indent}File: {item_path}")
    except Exception as e:
        print(f"Failed to list path {path.toString()}: {e}")

# Crear la sesión de Spark
spark = SparkSession.builder \
    .appName("List HDFS Files and Folders") \
    .master("spark://spark:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

# Importar las clases necesarias desde el espacio de nombres Java
java_import(spark._jvm, "org.apache.hadoop.fs.Path")
java_import(spark._jvm, "org.apache.hadoop.fs.FileSystem")

# Ruta en HDFS que deseas listar
hdfs_path = "hdfs://namenode:9000/user/david"

try:
    # Obtener la configuración de Hadoop
    hadoop_conf = spark._jsc.hadoopConfiguration()
    
    # Obtener el sistema de archivos HDFS
    hdfs = spark._jvm.FileSystem.get(hadoop_conf)
    
    # Iniciar el listado desde el directorio raíz
    list_hdfs_path(hdfs, spark._jvm.Path(hdfs_path))
    
    print("Successfully listed files and directories in HDFS.")
except Exception as e:
    print(f"Failed to list files and directories in HDFS: {e}")

# Detener la sesión de Spark
spark.stop()
