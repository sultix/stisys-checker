sudo apt-get install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install requests
pip install bs4

python main.py