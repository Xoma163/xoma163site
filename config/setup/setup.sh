#!/bin/bash
# Install python, python-venv and project requirements
sudo apt -y update
sudo apt install -y python3.7 python3.7-venv python3-venv python3.7-dev python3-wheel postgresql libpq-dev ffmpeg nginx build-essential

python3.7 -m venv venv
set -e
source ./venv/bin/activate
pip install wheel
pip install --upgrade --user travis pip setuptools wheel virtualenv
pip install -r requirements.txt

_pwd=$pwd

# systemd
sudo ln -s "$_pwd/config/xoma163bot.service" /etc/systemd/system/
sudo ln -s "$_pwd/config/xoma163site.service" /etc/systemd/system/
sudo systemctl daemon-reload

cp secrets/secrets_example.py secrets/secrets.py

#web
sudo ln -s "$_pwd/config/xoma163site_nginx.conf" /etc/nginx/sites-available/
sudo ln -s "$_pwd/config/xoma163site_nginx.conf" /etc/nginx/sites-enabled/
sudo systemctl restart nginx

python manage.py migrate
python manage.py initial

old_path="/var/www/xoma163site/"
sed -i "s#$old_path#$_pwd#g" ./service/xoma163bot_copy.service
sed -i "s#$old_path#$_pwd#g" ./service/xoma163site.service
sed -i "s#$old_path#$_pwd#g" ./service/xoma163site_nginx.conf
