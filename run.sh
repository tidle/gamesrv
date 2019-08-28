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
    python3 -u app.py 2&> log.txt &
elif [ $t = "stop" ]
then
    ps aux | grep "app.py" | head -n1 | awk '{print $2}' | xargs kill
else
    echo "Please choose a valid option:"
    echo "start (default), or stop"
fi
