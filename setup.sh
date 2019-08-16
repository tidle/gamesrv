echo "Installing venv"
python3 -m venv env
source env/bin/activate
echo "Python is:"
which python
echo "installing required pakcages"
pip3 install -r requirements.txt
