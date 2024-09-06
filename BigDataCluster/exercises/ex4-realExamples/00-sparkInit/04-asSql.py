
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Join DataFrame Example").getOrCreate()

# Create two DataFrames
emp = [("1", "Smith", 30), ("2", "Rose", 40), ("3", "Williams", 50), ("4", "Jones", 60)]
dept = [("Finance", 10), ("Marketing", 20), ("Sales", 30), ("IT", 40)]

empColumns = ["EmpID", "Name", "DeptID"]
deptColumns = ["DeptName", "DeptID"]

df_emp = spark.createDataFrame(emp, schema=empColumns)
df_dept = spark.createDataFrame(dept, schema=deptColumns)

# Register DataFrame as a SQL temporary view
df_emp.createOrReplaceTempView("employees")
df_dept.createOrReplaceTempView("departments")

# SQL Query
result = spark.sql("SELECT Name, DeptName FROM employees JOIN departments ON employees.DeptID = departments.DeptID")
result.show()