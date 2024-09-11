#docker buildx build -f Dockerfile.3.4.0 -t dpetrocelli/hadoop-3.4.0 --push .
cd baseimage/base
#docker buildx build -f Dockerfile.3.4.0-arm -t dpetrocelli/hadoop-3.4.0-arm --push .
docker build -f Dockerfile.3.4.0-arm -t dpetrocelli/hadoop-3.4.0-arm .
cd ..
cd datanode/
docker build -f Dockerfile-arm -t dpetrocelli/datanode-hadoop-3.4.0-arm .
cd ..
cd namenode/
docker build -f Dockerfile-arm -t dpetrocelli/namenode-hadoop-3.4.0-arm .

docker push dpetrocelli/hadoop-3.4.0-arm 
docker push dpetrocelli/datanode-hadoop-3.4.0-arm
docker push dpetrocelli/namenode-hadoop-3.4.0-arm