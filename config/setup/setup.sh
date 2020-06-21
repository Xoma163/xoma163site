#!/bin/bash
# install python, python-venv and project requirements
sudo apt -y update
sudo apt install -y python3.7 python3.7-venv python3-venv python3.7-dev python3-wheel postgresql libpq-dev ffmpeg nginx build-essential python-opencv

python3.7 -m venv venv
set -e
source ./venv/bin/activate
pip install wheel
pip install --upgrade --user travis pip setuptools wheel virtualenv
pip install -r requirements.txt

# rename abs paths
old_path="/var/www/xoma163site/"
sed -i "s#$old_path#$PWD/#g" ./config/xoma163bot.service
sed -i "s#$old_path#$PWD/#g" ./config/xoma163site.service
sed -i "s#$old_path#$PWD/#g" ./config/xoma163site_nginx.conf

# systemd
rm /etc/systemd/system/xoma163bot.service || echo $
rm /etc/systemd/system/xoma163site.service || echo $
sudo ln -s "$PWD/config/xoma163bot.service" /etc/systemd/system/ || echo $
sudo ln -s "$PWD/config/xoma163site.service" /etc/systemd/system/ || echo $
sudo systemctl daemon-reload

# web
rm /etc/nginx/sites-available/xoma163site_nginx.conf || echo $
rm /etc/nginx/sites-enabled/xoma163site_nginx.conf || echo $
sudo ln -s "$PWD/config/xoma163site_nginx.conf" /etc/nginx/sites-available/ || echo $
sudo ln -s "$PWD/config/xoma163site_nginx.conf" /etc/nginx/sites-enabled/ || echo $
sudo systemctl restart nginx

# migrations
python manage.py migrate
python manage.py initial
