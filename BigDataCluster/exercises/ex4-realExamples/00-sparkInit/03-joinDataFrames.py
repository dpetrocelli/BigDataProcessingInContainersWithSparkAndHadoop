from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("Join DataFrame Example").getOrCreate()

# Create two DataFrames
emp = [("1", "Smith", 30), ("2", "Rose", 40), ("3", "Williams", 50), ("4", "Jones", 60)]
dept = [("Finance", 10), ("Marketing", 20), ("Sales", 30), ("IT", 40)]
vtas = [("1", 100), ("2", 200), ("3", 300), ("4", 400),("4", 700) ]
empColumns = ["EmpID", "Name", "DeptID"]
deptColumns = ["DeptName", "DeptID"]
vtasColumns = ["EmpID", "Amount"]

df_emp = spark.createDataFrame(emp, schema=empColumns)
df_dept = spark.createDataFrame(dept, schema=deptColumns)
df_vtas = spark.createDataFrame(vtas, schema=vtasColumns)

# Perform inner join
# Realiza el inner join entre df_emp y df_vtas
df_joined = df_emp.join(df_vtas, df_emp.EmpID == df_vtas.EmpID, "inner")

# Selecciona las columnas que quieres conservar, renombrando la columna 'EmpID' duplicada
df_joined_cleaned = df_joined.select(
    col("df_emp.EmpID").alias("EmpID"),  # Selecciona y renombra la columna EmpID de df_emp
    col("Amount")  # Selecciona la columna Amount
)

# Muestra el DataFrame limpio
df_joined_cleaned.show()

# Agrupa por EmpID y calcula la suma de Amount
df_sum = df_joined_cleaned.groupBy("EmpID").sum("Amount")

# Muestra el resultado
df_sum.show()