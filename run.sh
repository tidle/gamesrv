echo "Using venv..."
source env/bin/activate
echo "Starting server..."
python3 app.py > log.txt
echo ""
echo "Server stoped."
