#!/bin/bash
/var/www/xoma163.site/venv/bin/python3 /var/www/xoma163.site/manage.py makemigrations
/var/www/xoma163.site/venv/bin/python3 /var/www/xoma163.site/manage.py migrate
systemctl restart xoma163site