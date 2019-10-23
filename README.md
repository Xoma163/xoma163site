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