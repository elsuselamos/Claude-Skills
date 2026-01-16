#!/bin/bash

JAR_FILE="/home/ubuntu/projects/xxpay-service-1.0.0.jar"
BASE_DUBBO_PORT=20880
BASE_SERVER_PORT=8190
BASE_SERVER_NODE=1
INSTANCE_COUNT=3
CONFIG_FILE="/home/ubuntu/projects/application.properties"

APP_DIR_PREFIX="/home/ubuntu/projects/logs/app_"
WORK_DIR_PREFIX="/home/ubuntu/.dubbo/.dubbo_instance_"
CONFIG_AWS_JSK="/home/ubuntu/aws-truststore.jks"

# 进程停止 & 端口释放函数
kill_instance() {
  local instance_id=$1
  local APP_DIR="${APP_DIR_PREFIX}${instance_id}"
  local PID_FILE="${APP_DIR}/app.pid"
  local DUBBO_PORT=$(($BASE_DUBBO_PORT + $instance_id))
  local SERVER_PORT=$(($BASE_SERVER_PORT + $instance_id))

  if [ -f "$PID_FILE" ]; then
    local PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null; then
      echo "Gracefully stopping instance $instance_id (PID: $PID)..."
      kill -15 "$PID"
      sleep 5
      if ps -p $PID > /dev/null; then
        echo "Force killing PID $PID"
        kill -9 "$PID"
      fi
    fi
    rm -f "$PID_FILE"
  fi

  for port in $DUBBO_PORT $SERVER_PORT; do
    if ss -tulnp | grep ":$port " > /dev/null; then
      echo "Releasing port $port..."
      sudo fuser -k $port/tcp
      sleep 1
    fi
  done
}

start_instance() {
  local instance_id=$1
  local mode=$2
  local APP_DIR="${APP_DIR_PREFIX}${instance_id}"
  local DUBBO_PORT=$(($BASE_DUBBO_PORT + $instance_id))
  local SERVER_PORT=$(($BASE_SERVER_PORT + $instance_id))
  local SERVER_NODE="E$(($BASE_SERVER_NODE + $instance_id))"
  local PID_FILE="${APP_DIR}/app.pid"
  local WORK_DIR="${WORK_DIR_PREFIX}${instance_id}"
  local LOG_DIR="${APP_DIR}/logs"
  local HEAP_DUMP_PATH="${APP_DIR}/heapdump-${instance_id}-$(date +%F-%H%M%S).hprof"

  mkdir -p "$WORK_DIR" "$LOG_DIR"

  # JVM 配置
  JVM_OPTS="\
  -Xms1024m -Xmx1024m \
  -Xss512k \
  -XX:+UseCompressedOops \
  -XX:MaxDirectMemorySize=128m \
  -XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=256m \
  -XX:+UseG1GC -XX:G1HeapRegionSize=16m \
  -XX:InitiatingHeapOccupancyPercent=40 -XX:G1ReservePercent=10 \
  -XX:ConcGCThreads=1 -XX:G1ConcRefinementThreads=1 \
  -XX:MaxGCPauseMillis=50 \
  -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=${HEAP_DUMP_PATH} \
  -XX:+ExitOnOutOfMemoryError"

  JKS_OPTS="\
  -Djavax.net.ssl.trustStoreType=JKS \
  -Djavax.net.ssl.trustStore=${CONFIG_AWS_JSK} \
  -Djavax.net.ssl.trustStorePassword=changeit \
  -Dcom.sun.net.ssl.checkRevocation=false"

  # 清理旧日志
  for log_file in "$LOG_DIR/stdout.log" "$LOG_DIR/stderr.log"; do
    if [ -f "$log_file" ]; then
      tail -n 5000 "$log_file" > "${log_file}.tmp" && mv "${log_file}.tmp" "$log_file"
    fi
  done

  # 杀掉旧进程
  kill_instance "$instance_id"

  if [[ "$mode" == "foreground" ]]; then
    echo $$ > "$PID_FILE"
    exec java $JVM_OPTS $JKS_OPTS \
      -Duser.home="$WORK_DIR" \
      -jar "$JAR_FILE" \
      --dubbo.protocol.port=$DUBBO_PORT \
      --server.port=$SERVER_PORT \
      --NODE=$SERVER_NODE \
      --spring.config.additional-location=file:"$CONFIG_FILE" \
      --logging.filePath="$LOG_DIR"
  else
    nohup java $JVM_OPTS $JKS_OPTS \
      -Duser.home="$WORK_DIR" \
      -jar "$JAR_FILE" \
      --dubbo.protocol.port=$DUBBO_PORT \
      --server.port=$SERVER_PORT \
      --spring.config.additional-location=file:"$CONFIG_FILE" \
      --logging.filePath="$LOG_DIR" > "$LOG_DIR/stdout.log" 2> "$LOG_DIR/stderr.log" &
    echo $! > "$PID_FILE"
    echo "Instance $instance_id started (PID: $(cat $PID_FILE), Dubbo Port: $DUBBO_PORT, Server Port: $SERVER_PORT)"
  fi
}

# 主执行逻辑
if [[ "$1" =~ ^[0-2]$ ]]; then
  # systemd 模式：传入实例 ID 和 foreground 参数
  start_instance "$1" "$2"
else
  echo "Rolling restart all instances..."
  for i in $(seq 0 $(($INSTANCE_COUNT - 1))); do
    start_instance $i
    sleep 3
  done
fi
