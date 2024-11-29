#!/bin/bash

# 定义变量
PID_FILE="manage.pid"
LOG_FILE="test.log"

# 检查是否有正在运行的 Django 进程
if [ -f $PID_FILE ]; then
    if ps -p $(cat $PID_FILE) > /dev/null; then
        echo "Stopping existing Django server..."
        kill -9 $(cat $PID_FILE)
        rm -f $PID_FILE
        echo "Django server stopped."
    else
        echo "No running Django server found."
        rm -f $PID_FILE
    fi
fi

# 启动新的 Django 服务器
echo "Starting Django server..."
nohup python3.8 manage.py runserver 0.0.0.0:8000 > $LOG_FILE 2>&1 &
echo $! > $PID_FILE
echo "Django server started with PID: $!"