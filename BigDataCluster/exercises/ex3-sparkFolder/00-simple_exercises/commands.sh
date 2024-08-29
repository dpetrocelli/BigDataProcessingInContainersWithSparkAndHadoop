# Prepare the wordcount file
mkdir -p /tmp/hadoop/
pip install -r requirements.txt
python dynamicGenerator.py -l 5000000 -w 20   

# Copy the wordcount file and upload to HDFS
docker cp /tmp/hadoop/wordcount.txt namenode:/tmp/wordcount.txt
docker exec -it namenode hadoop fs -put /tmp/wordcount.txt /user/david/wordcount.txt 
docker exec -it namenode hadoop fs -ls /user/david/

# Copy python scripting files
docker cp simple_exercises/. hdfs-spark-1:/tmp

# connect to the container and install required package
pip install py4j
python X.py