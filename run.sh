t="loud"
if [ ! -z $1 ]
then
    t=$1
fi

if [ $t = "headless" ]
then
    source env/bin/activate
    python3 app.py > log.txt &
elif [ $t = "stop" ]
then
    ps aux | grep "python3 app.py" | head -n1 | awk '{print $2}' | xargs kill
elif [ $t = "loud" ]
then
    echo "Using venv..."
    source env/bin/activate
    echo "Starting server..."
    python3 app.py > log.txt
    echo ""
    echo "Server stoped."
else
    echo "Please choose a valid option:"
    echo "loud (default), headless, or stop"
fi
