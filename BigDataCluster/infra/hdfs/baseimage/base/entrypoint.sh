#!/bin/bash

# Debug: Print all environment variables
echo "Current Environment Variables:"
printenv

# Set default HDFS filesystem if not set
export CORE_CONF_fs_defaultFS=${CORE_CONF_fs_defaultFS:-hdfs://$(hostname -f):8020}

# Function to add a property to a Hadoop XML configuration file
addProperty() {
  local path=$1
  local name=$2
  local value=$3
  local entry="<property><name>$name</name><value>${value}</value></property>"
  local escapedEntry=$(echo $entry | sed 's/\//\\\//g')
  sed -i "/<\/configuration>/ s/.*/${escapedEntry}\n&/" "$path"
}

# Function to configure Hadoop XML files based on environment variables
configure() {
  local path=$1
  local module=$2
  local envPrefix=$3

  echo "Configuring $module"
  for c in $(printenv | perl -sne 'print "$1 " if m/^${envPrefix}_(.+?)=.*/' -- -envPrefix="$envPrefix"); do 
      name=$(echo "${c}" | perl -pe 's/___/-/g; s/__/@/g; s/_/./g; s/@/_/g;')
      var="${envPrefix}_${c}"
      value=${!var}
      echo " - Setting $name=$value"
      addProperty "$path" "$name" "$value"
  done
}

# Apply configurations to Hadoop XML files
configure /etc/hadoop/core-site.xml core CORE_CONF
configure /etc/hadoop/hdfs-site.xml hdfs HDFS_CONF
configure /etc/hadoop/yarn-site.xml yarn YARN_CONF
configure /etc/hadoop/httpfs-site.xml httpfs HTTPFS_CONF
configure /etc/hadoop/kms-site.xml kms KMS_CONF
configure /etc/hadoop/mapred-site.xml mapred MAPRED_CONF

# Configure multi-homed network if needed
if [ "$MULTIHOMED_NETWORK" = "1" ]; then
  echo "Configuring for multihomed network"
  addProperty /etc/hadoop/hdfs-site.xml dfs.namenode.rpc-bind-host 0.0.0.0
  addProperty /etc/hadoop/hdfs-site.xml dfs.namenode.servicerpc-bind-host 0.0.0.0
  addProperty /etc/hadoop/hdfs-site.xml dfs.namenode.http-bind-host 0.0.0.0
  addProperty /etc/hadoop/hdfs-site.xml dfs.namenode.https-bind-host 0.0.0.0
  addProperty /etc/hadoop/hdfs-site.xml dfs.client.use.datanode.hostname true
  addProperty /etc/hadoop/hdfs-site.xml dfs.datanode.use.datanode.hostname true

  addProperty /etc/hadoop/yarn-site.xml yarn.resourcemanager.bind-host 0.0.0.0
  addProperty /etc/hadoop/yarn-site.xml yarn.nodemanager.bind-host 0.0.0.0
  addProperty /etc/hadoop/yarn-site.xml yarn.timeline-service.bind-host 0.0.0.0

  addProperty /etc/hadoop/mapred-site.xml yarn.nodemanager.bind-host 0.0.0.0
fi

# Configure Ganglia if the host is specified
if [ -n "$GANGLIA_HOST" ]; then
  mv /etc/hadoop/hadoop-metrics.properties /etc/hadoop/hadoop-metrics.properties.orig
  mv /etc/hadoop/hadoop-metrics2.properties /etc/hadoop/hadoop-metrics2.properties.orig

  for module in mapred jvm rpc ugi; do
    echo "$module.class=org.apache.hadoop.metrics.ganglia.GangliaContext31"
    echo "$module.period=10"
    echo "$module.servers=$GANGLIA_HOST:8649"
  done > /etc/hadoop/hadoop-metrics.properties
  
  for module in namenode datanode resourcemanager nodemanager mrappmaster jobhistoryserver; do
    echo "$module.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31"
    echo "$module.sink.ganglia.period=10"
    echo "$module.sink.ganglia.supportsparse=true"
    echo "$module.sink.ganglia.slope=jvm.metrics.gcCount=zero,jvm.metrics.memHeapUsedM=both"
    echo "$module.sink.ganglia.dmax=jvm.metrics.threadsBlocked=70,jvm.metrics.memHeapUsedM=40"
    echo "$module.sink.ganglia.servers=$GANGLIA_HOST:8649"
  done > /etc/hadoop/hadoop-metrics2.properties
fi

# Function to wait for a service to be available
wait_for_it() {
  local serviceport=$1
  local service=${serviceport%%:*}
  local port=${serviceport#*:}
  local retry_seconds=5
  local max_try=100
  local i=1

  until nc -z "$service" "$port"; do
    echo "[$i/$max_try] ${service}:${port} is not available yet, retrying in ${retry_seconds}s..."
    sleep "$retry_seconds"
    ((i++))
    if [ "$i" -gt "$max_try" ]; then
      echo "[$i/$max_try] ${service}:${port} is still not available; giving up."
      exit 1
    fi
  done
  echo "[$i/$max_try] ${service}:${port} is available."
}

# Wait for all service preconditions
for i in "${SERVICE_PRECONDITION[@]}"; do
  wait_for_it "${i}"
done

# Run the command specified as arguments to the script
exec "$@"
