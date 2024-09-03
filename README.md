# Big Data Processing in Containers with Spark and Hadoop

## Overview

This project demonstrates a scalable and containerized environment for processing massive datasets using Apache Spark and Apache Hadoop. By leveraging Docker, the project encapsulates the necessary components in containers, ensuring easy deployment and consistency across different environments.

## Features

- **Containerized Environment:** Utilize Docker to containerize Spark, Hadoop, and other necessary tools, making it easier to deploy and manage.
- **Scalable Processing:** Leverage Spark's distributed computing capabilities along with Hadoop's HDFS for efficient data processing.
- **Modular Setup:** Each component is modularized, allowing for easy customization and extension of the environment.
- **Sample Data Pipeline:** Includes a sample pipeline that demonstrates how to process and analyze large datasets.

## Prerequisites

- Docker and Docker Compose installed on your system.
- Basic knowledge of Spark, Hadoop, and Docker.

# Getting Started

## Clone the Repository

```bash
git clone https://github.com/dpetrocelli/BigDataProcessingInContainersWithSparkAndHadoop.git
cd BigDataProcessingInContainersWithSparkAndHadoop
```

## Build the project

1. Go to hdfs folder and build the base image

```bash
cd BigDataCluster/infra/hdfs/baseimage/base/

docker build . -t hadoop-3.4.0 -f Dockerfile.3.4.0
or
docker buildx build -f Dockerfile.3.4.0 -t hadoop-3.4.0 --load .
then

docker image ls

REPOSITORY TAG IMAGE ID CREATED SIZE
hadoop-3.4.0 latest 604208ada6f6 13 seconds ago 3.39GB
....
```

2. Now go to datanode and namenode and build respective images

```bash
cd BigDataCluster/infra/hdfs/baseimage/docker-hadoop/datanode
docker build . -t datanode:hadoop-3.4.0
cd ../namenode
docker build . -t namenode:hadoop-3.4.0

```

## Start the cluster

```bash
cd BigDataCluster/infra/hdfs/

docker-compose -f final-cluster-compose-v1.yaml up

```
