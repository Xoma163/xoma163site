secrets = {
    'django': {
        # random 50 symbols
        'SECRET_KEY': '!!!!!!!! SET RANDOM 50 SYMBOLS HERE. IMPORTANT !!!!!!!!'
    },
    # your database user
    'db': {
        'NAME': '<your_database>',
        'USER': '<your_username>',
        'PASSWORD': '<your_password>',
        'HOST': 'localhost',
        'PORT': '5432'
    },
    # vk credentials
    'vk': {
        'bot': {
            # long-poll token
            'TOKEN': '<your_token>',
            'group_id': '<your_group_id>',
            # mentions that the bot responds to
            'mentions': ["[club123|@short_group_name]",
                         "[club123|@club123]",
                         "[club123|Название группы]",
                         "[club123|Translate Name]"],
        },
        # user access (for audio-upload only)
        'user': {
            'id': '123',
            # email/phone
            'login': '',
            'password': '',
        },
        # extra security check
        'admin_id': '123',
        'mention_me': "[id123|Имя]"

    },
    'yandex': {
        'geo': '',
        'weather': '',
        'translate': '',
    },
    'donationalert': {
        'api_key': '',
        'access_token': '',
        'refresh_token': ''

    },
    'everypixel': {
        'client_id': '',
        'client_secret': ''
    },
    'timezonedb': {
        'api_key': ''
    }

}
