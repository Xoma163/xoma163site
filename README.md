[![Codacy Badge](https://api.codacy.com/project/badge/Grade/902a018f7e0c4e5d9a823e974a972742)](https://app.codacy.com/manual/Xoma163/xoma163site?utm_source=github.com&utm_medium=referral&utm_content=Xoma163/xoma163site&utm_campaign=Badge_Grade_Settings)

## VkBot Petrovich

Этот проект бот ВКонтакте, созданный в первую очередь для личных целей, но так вышло, что и для развлечения.

### FAQ

***

Q: **Где лежит сам бот в этом django проекте?**

A: apps/API_VK/. Обработка запросов - VkBotClass.py, API - views.py, команды - command/

***

Q: **Куда контрибьютить свою команду?**

A: В папке apps/API_VK/command/commands/ нужно добавить свою команду, унаследованную от CommonCommand. 
Команду следует положить в ту папку, в которую она подходит логически (пример: команда для админа в AdminCommands, простая команда с простым ответом - EasyCommands, Игра - Games, ...)

***

Q: **Правила оформления команд**

A : Любая команда должна содержать метод \_\_init\_\_ внутри которой происходит инициализация команды. Обязательным параметром является список names - имена, на которые будет откликаться команда.

Возможные параметры конструктора:
-   names - обязательное поле, имена команды. Список
-   help_text - текст отображения в команде /помощь
-   detail_help_text - текст отображения в команде /помощь (имя команды)
-   keyboard - вывод кнопки(ок) на клавиатуру
-   access - требуемый уровень прав для использования команды (user/student/terraria/minecraft/moderator/admin)
-   pm - команда будет работать только в лс
-   conversation - команда будет работать только в конфе
-   fwd - требуются пересылаемые сообщения
-   args - требуются аргументы (количество в int)
-   int_args - требуются int аргументы (список, указать позиции)
-   api - будет ли команда работать для API (по умолчанию True) 
-   attachments - требуются ли вложения 
-   enabled - будет ли команда работать (по умолчанию True)
-   priority - место в списке команд (больше - раньше команда подключится) (по умолчанию 0)

Список полей конструктора может отличаться от вышеуказанного. Уточняйте в CommonCommand

### Формат keyboard
{'for': 'moderator', 'text': 'Логи', 'color': 'blue', 'row': 1, 'col': 1}
-   for - для кого предназначена команда (поле access по умолчанию
-   text - текст кнопки
-   color - цвет кнопки
-   row - индекс в строке
-   col - индекс в столбце

Также должен быть переопределён метод start, в котором содержится тело команды.

Возможно переопределить метод accept, чтобы изменить срабатывание команды (см. Conference)

Внутри любой команды есть две переменные - vk_bot и vk_event

#### vk_bot
Данная переменная - экземпляр VkBot со всеми методами для работы. Вероятность того, что потребуется в работе команд - 5%

#### vk_event
Данная переменная - экземпляр VkEvent со всеми полями, необходимыми для работы. 

-   sender - сущность VkUser, который отправил сообщение
-   chat  - сущность VkChat, из которого отправили сообщение (при наличии)
-   peer_id - куда отправлять ответ (для юзеров - id, для чатов - 2000000000 + chat_id(у каждого чата уникален и начинается с 1))
-   action - какой-либо action (например по добавлению бота в конфу)
-   payload - скрытая информация с клавиатур
-   msg - полное сообщение без изменений
-   command - команда
-   args - аргументы(список) (при наличии) 
-   original_args - аргументы без команды (строка) 
-   attachments - вложения (список словарей)
-   fwd - пересланные сообщения (список словарей)
-   from_chat - True если сообщение из чата 
-   from_user - True если сообщение от юзера
-   from_api - True если сообщение из API

Список полей VkEvent может отличаться от вышеуказанного. Уточняйте в VkEvent(vk_bot.py)

#### Формат fwd
`[{'text':'...','from_id':'...'},...]`
-   text - Текст сообщения
-   from_id - если положительный, то от пользователя, если отрицательный, то это group_id бота

#### Формат attachments

-   `{'photo':{'download_url':'...','size':{'width':'...','height'...'}}}`
-   `{'video':{'url':'...','title':'...'}}`
-   `{'audio':{'owner_id':'...', 'id':'...', 'url':'...', 'artist':'...', 'title':'...', 'duration':'...', 'download_url':'...' }}`
-   `{'doc':{'title':'...', 'ext':'...', 'download_url':'...'}}`
-   `{'wall':{'attachments':[...], 'copy_history':'...'}}`
-   `{'audio_message':{'id':'...', 'owner_id':'...', 'download_url':'...', 'duration':'...'}}`

***

Q: **Как возвращать ответ команды?**

A:
-   return `"сообщение"` - отправляет одно сообщение
-   return `{'msg':'сообщение', 'attachments':'[вложения]','keyboard':'[клавиатура]'}` (в таком виде обязателен только msg) - отправляет вложение или клавиатуру
-   return `['сообщение1','сообщение2',...]`
-   return `[{'msg':'сообщение', 'attachments':'[вложения]','keyboard':'[клавиатура]'},{...},...]` - отправляет несколько сообщений подряд с вложениями или клавиатурой

---

Q: **Какие существуют методы для упрощения разработки команд**

A: В CommonCommand есть следующие методы:
-   `check_sender(role)` - Проверяет роль пользователя
-   `check_args(count)` - Проверяет количество аргументов
-   `check_number_arg_range(arg,val1,val2,banned_list)` - Проверяет вхождение аргумента в диапазон `[val1;val2]` и также проверяет, чтобы значение не входило в banned_list 
-   `parse_args(type)` - Проверяет на type(int/float) выбранные позиции аргументов (параметр int_args/float_args)
-   `check_pm` - Проверяет на личные сообщения боту
-   `check_conversation` - Проверяет на беседу
-   `check_fwd` - Проверяет, есть ли пересланные сообщения 
-   `check_command_time(name,time)` - Проверяет, не вышло ли время для повторного использования какого-либо функционала (см Start/Stop/Restart в ModeratorCommand)
-   `check_attachments` - Проверяет, есть ли вложения

---

Q: **Как работать с API?**

A: 

<https://api.xoma163.xyz/> - Присылает ответ на запрос

Обязательные параметры
-   msg - сообщение боту

Обязательные заголовки
-   Client-Id - уникальный идентификатор клиента

Дополнительные параметры
-   send=False - отправляет сообщение или нет

<https://api.xoma163.xyz/chat> - Ретранслирует сообщение в чат без обработки

Обязательные параметры
-   msg - сообщение боту

---

Q: **Как работать с базой данных?**

A: Вкратце - в models.py у каждого приложения есть классы - модели. (Пример VkUser, VkChat, ...). Внутри этого файла описываются поля модели. Короткий гайд по работе с сущностями:
-   `Model.objects.all()` - все записи
-   `Model.objects.filter(fieldname = value, fieldname2 = value2)` - фильтрация по полям
-   `Model(**dict)` или 
``` python
model = Model();
model.field=value
model.save()
```
Создание сущности и её сохранение

[Более подробно](https://docs.djangoproject.com/en/2.2/topics/db/models/)