## Установка проекта

### 0. Клонирование проекта

`cd /var/www && git clone https://github.com/Xoma163/xoma163site.git`  

`cd xoma163site`

### 1. Подготовка группы в ВК
ToDo
<your_token>
<your_group_id>

### 2. Подготовка БД

-   `su - postgres` 
-   `psql` 

```postgresql
CREATE ROLE '<your_username>' WITH LOGIN ENCRYPTED PASSWORD '<your_password>';
CREATE DATABASE '<your_database>' WITH OWNER '<your_username>';
SET TIMEZONE='<your_timezone>';
```

### 3. Указание учётных данных
Внеси все свои данные по боту ВК и различным API в файл secrets/secrets.py  

За основу можно и нужно взять secrets/secrets_example.py  

`cp secrets/secrets_example.py secrets/secrets.py` 

В первую очередь нужно заполнить:
-   `django['secret_key']`
-   `db`
-   `vk['bot']`

### 4. Указание своих данных в конфигах
-   в config/xoma163bot.service нужно указать пользователя от имени которого будет выполняться служба 
-   в config/xoma163site.service нужно указать пользователя от имени которого будет выполняться служба 
-   в config/xoma163site_nginx.conf нужно указать имя сервера, на которое будет реагировать nginx и порт. 

### 5. Запуск автонастройки (создание окружение, установка зависимостей)
-   `chmod +x setup.sh`
-   `./setup.sh`

Обрати внимание. Скрипт заменяет некоторые абсолютные пути на тот путь, откуда ты будешь запускать скрипт. Рекомендуется это делать из папки проекта

### 6. Запуск
-   `systemctl start xoma163bot` - запуск бота
-   `systemctl start xoma163site` - запуск админки и сайта
