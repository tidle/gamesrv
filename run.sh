#!/bin/bash
cd `dirname $0`

t="start"
if [ ! -z $1 ]
then
    t=$1
fi

if [ $t = "start" ]
then
    echo "Using venv..."
    source env/bin/activate
    echo "Starting server..."
    python3 -u app.py &> log.txt &
elif [ $t = "stop" ]
then
    echo "Stopping server..."
    ps aux | grep "app.py" | head -n1 | awk '{print $2}' | xargs kill
elif [ $t = "restart" ]
then
    $0 stop
    $0 start
else
    echo "Please choose a valid option:"
    echo "start (default), or stop"
fi
