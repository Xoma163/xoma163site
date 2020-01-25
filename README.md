# xoma163site
My website and telegram/vk bot

For opencv2
apt-get install -y libsm6 libxext6 libxrender-dev


Для исправления бага, когда спустя время загибался сервер сначала с 504, а потом с 502:

mcedit /etc/sysct.conf

append:

>net.core.somaxconn = 20000
>net.core.netdev_max_backlog = 65535

>sysctl -p

>service php-fpm restart


ln -s /var/www/xoma163.site/uWSGI_nginx/xoma163site.service /etc/systemd/system/
ln -s /var/www/xoma163.site/uWSGI_nginx/xoma163bot.service /etc/systemd/system/

https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx

ln -s /var/www/xoma163.site/uWSGI_nginx/xoma163site_nginx.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/xoma163site_nginx.conf /etc/nginx/sites-enabled/

cloc . -exclude-list-file=.clocignore