# Install python, python-venv and project requirements
sudo apt -y update
sudo apt install -y python3.7 python3.7-venv python3-venv postgresql libpq-dev ffmpeg
python3.7 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt

# systemd
sudo ln -s "$(pwd)/config/xoma163bot.service" /etc/systemd/system/
sudo systemctl daemon-reload

mv secrets/secrets_example.py secrets/secrets.py
