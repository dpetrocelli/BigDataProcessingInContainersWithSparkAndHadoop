#Basic Hadoop Activities
#Create Directories in HDFS:
which hadoop

hdfs dfs -mkdir /user
# Way 1 - Connect to the container and execute commands
hdfs dfs -mkdir /user/david

#Upload Data to HDFS:
# container hdfs cli 
docker cp /tmp/localfile.txt datanode:/tmp
docker cp /tmp/wordcount.txt datanode:/tmp

hdfs dfs -put /tmp/localfile.txt /user/david/
hdfs dfs -ls /user/david/
hdfs dfs -cat /user/david/localfile.txt

# upload the wordcount example to HDFS
hdfs dfs -put /tmp/wordcount.txt /user/david/

# Way 2 - Execute commands from host using the remote exec 
#add files to hdfs
docker exec -it namenode hadoop fs -mkdir -p /hdfs/dir/
docker exec -it namenode hadoop fs -ls /hdfs/dir/
docker cp /Users/david/Documents/code/newfolder/unlu2024/vfinal/kubernetes/docker2/BigDataCluster/README.md namenode:/tmp 
docker exec -it namenode hadoop fs -put /tmp/README.md /hdfs/dir/README.md
docker exec -it namenode hadoop fs -ls /hdfs/dir/


# check replicas
docker exec -it namenode hadoop fs -stat %r /hdfs/dir/README.md
docker exec -it namenode hdfs fsck /hdfs/dir/README.md -files -blocks -locations

# check dfs status
hdfs dfsadmin -report
#Propiedades de los Archivos y Directorios
hdfs dfs -stat "%n: %b bytes, modified on %y" /hdfs/dir/file.txt
