# Install python, python-venv and project requirements
sudo apt -y update
sudo apt -y upgrade
sudo apt install -y python3.8 python3.8-venv python3-venv
python3.8 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt

# systemd
sudo ln -s "$(pwd)/config/xoma163bot.service" /etc/systemd/system/
sudo systemctl daemon-reload

sudo apt install -y postgresql psycopg2-binary
