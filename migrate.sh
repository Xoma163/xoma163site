#!/bin/bash
/var/www/xoma163site/venv/bin/python3 /var/www/xoma163site/manage.py makemigrations
/var/www/xoma163site/venv/bin/python3 /var/www/xoma163site/manage.py migrate
systemctl restart xoma163site
