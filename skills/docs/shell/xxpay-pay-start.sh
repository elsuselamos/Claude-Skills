#!/bin/bash

JAR_FILE="xxpay-pay-1.0.0.jar"
BASE_DUBBO_PORT=23020
BASE_SERVER_PORT=3020
BASE_SERVER_NODE=1
INSTANCE_COUNT=3
CONFIG_FILE="./application.properties"

# 基础路径变量
APP_DIR_PREFIX="app_"
WORK_DIR_PREFIX="/home/ubuntu/.dubbo/.dubbo_instance_"


# **进程优雅停止**
stop_instance() {
  local INSTANCE_ID=$1
  local APP_DIR="${APP_DIR_PREFIX}${INSTANCE_ID}"
  local PID_FILE="${APP_DIR}/app.pid"

  if [ -f $PID_FILE ]; then
    local PID=$(cat $PID_FILE)
    if ps -p $PID > /dev/null; then
      echo "🔹 Stopping instance $INSTANCE_ID (PID: $PID)..."
      sudo kill -15 $PID  # 先尝试优雅关闭
      sleep 5  # 等待 5 秒让 Dubbo 触发优雅下线

      if ps -p $PID > /dev/null; then
        echo "⚠️ Process $PID still running, force killing..."
        wait $PID 2>/dev/null || sudo kill -9 $PID
      fi
    fi
    rm -f $PID_FILE
  else
    echo "⚠️ No PID file found for instance $INSTANCE_ID."
  fi
}

# **启动实例**
start_instance() {
  local INSTANCE_ID=$1
  local APP_DIR="${APP_DIR_PREFIX}${INSTANCE_ID}"
  local DUBBO_PORT=$(($BASE_DUBBO_PORT + $INSTANCE_ID))
  local SERVER_PORT=$(($BASE_SERVER_PORT + $INSTANCE_ID))
  local SERVER_NODE="D$(($BASE_SERVER_NODE + $INSTANCE_ID))"
  local PID_FILE="${APP_DIR}/app.pid"
  local WORK_DIR="${WORK_DIR_PREFIX}${INSTANCE_ID}"
  local LOG_DIR="${APP_DIR}/logs"



# JVM 优化参数（适配 4GB 服务器）
  local JVM_OPTS="
  -Xms512m -Xmx1G \
  -XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=50 -XX:G1ReservePercent=10 \
  -XX:G1HeapRegionSize=4m -XX:ConcGCThreads=1 -XX:G1ConcRefinementThreads=1 \
  -XX:MetaspaceSize=64m -XX:MaxMetaspaceSize=128m \
  -Xss512k -XX:+UseCompressedOops \
  -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=${APP_DIR}/heapdump.hprof \
  -XX:+ExitOnOutOfMemoryError"

# SSL 证书选项
  local JKS_OPTS="
  -Djavax.net.ssl.trustStoreType=JKS \
  -Djavax.net.ssl.trustStore=${CONFIG_AWS_JSK} \
  -Djavax.net.ssl.trustStorePassword=changeit \
  -Dcom.sun.net.ssl.checkRevocation=false
  "
  # **创建工作目录**
  mkdir -p $WORK_DIR
  mkdir -p $LOG_DIR

  # **清理日志，保留最近 5000 行**
  for log_file in "$LOG_DIR/stdout.log" "$LOG_DIR/stderr.log"; do
    if [ -f "$log_file" ]; then
      tail -n 5000 "$log_file" > "${log_file}.tmp" && mv "${log_file}.tmp" "$log_file"
    fi
  done

  # **启动 Java 进程**
  nohup java $JVM_OPTS $JKS_OPTS \
    -Duser.home=$WORK_DIR \
    -jar $JAR_FILE \
    --dubbo.protocol.port=$DUBBO_PORT \
    --server.port=$SERVER_PORT \
    --NODE=$SERVER_NODE \
    --spring.config.additional-location=file:"$CONFIG_FILE" \
    --spring.redis.lettuce.cluster.enabled=false \
    --logging.level.org.apache.activemq.transport.failover.FailoverTransport=WARN \
    --logging.filePath="$LOG_DIR" > "$APP_DIR/stdout.log" 2> "$APP_DIR/stderr.log" &

  echo $! > $PID_FILE
  echo "✅ Instance $INSTANCE_ID started (PID: $(cat $PID_FILE), Dubbo Port: $DUBBO_PORT, Server Port: $SERVER_PORT)"
}

# **滚动更新**
rolling_update_instances() {
  for i in $(seq 0 $(($INSTANCE_COUNT - 1))); do
    echo "🔄 Rolling restart for instance $i..."
    stop_instance $i
    start_instance $i
    sleep 5
  done
}

# **执行滚动更新**
