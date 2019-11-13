import datetime
import json

from django.core.management.base import BaseCommand

from xoma163site.settings import BASE_DIR
from xoma163site.wsgi import vkbot

timetable = {'1': {'START': '9:00', 'END': '9:35'},
             '2': {'START': '9:45', 'END': '11:20'},
             '3': {'START': '11:30', 'END': '13:05'},
             '4': {'START': '13:30', 'END': '15:05'},
             '5': {'START': '15:15', 'END': '16:50'},
             '6': {'START': '17:00', 'END': '18:35'},
             }
BEFORE_MIN = 10


# ToDo: сделать расписание на каждую неделю и читать в нужную неделю нужное расписание (OMFG)
class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        # 6221 - 3, my - 2
        self.chat_id = 3
        self.first_discipline = None
        self.last_discipline = None

    def change_title_on_default(self):
        vk_title = '6221'
        vkbot.set_chat_title_if_not_equals(self.chat_id, vk_title)

    def handle(self, *args, **kwargs):
        with open(BASE_DIR + '/static/schedules/schedule.json') as json_file:
            schedule = json.load(json_file)
        now = datetime.datetime.now()
        now_weeknumber = str((now.isocalendar()[1]) % 2 + 1)
        now_weekday = str(now.weekday() + 1)

        # Проверяем есть ли сегодня пары
        if now_weeknumber not in schedule:
            self.change_title_on_default()
            return
        if now_weekday not in schedule[now_weeknumber]:
            self.change_title_on_default()
            return

        print(schedule[now_weeknumber][now_weekday])

        # Узнаём какая пара первая, а какая последняя
        for i in range(len(timetable)):
            if str(i + 1) in schedule[now_weeknumber][now_weekday]:
                if self.first_discipline is None:
                    self.first_discipline = str(i + 1)
                self.last_discipline = str(i + 1)

        new_min = now.minute
        new_hour = now.hour
        if new_min >= 60:
            new_min -= 60
            new_hour += 1
        if new_hour >= 24:
            new_hour -= 24

        now_1900 = datetime.datetime.strptime("%s:%s" % (new_hour, new_min), '%H:%M')
        print(now_1900)
        current_discipline = None
        for item in timetable:
            item_date_start = datetime.datetime.strptime(timetable[item]['START'], '%H:%M')
            item_date_end = datetime.datetime.strptime(timetable[item]['END'], '%H:%M')
            if item_date_start <= now_1900 <= item_date_end or \
                    datetime.timedelta(0) < item_date_start - now_1900 <= datetime.timedelta(minutes=BEFORE_MIN):
                # if item_date_start <= now_1900 <= item_date_end:
                current_discipline = str(item)
        if now_1900 <= datetime.datetime.strptime(timetable['1']['START'], '%H:%M'):
            current_discipline = 0
        elif now_1900 >= datetime.datetime.strptime(timetable['6']['END'], '%H:%M'):
            current_discipline = 7

        # Установка первой по расписанию пары
        if int(current_discipline) < int(self.first_discipline):
            vk_title = "6221|{} {} {}({})".format(
                timetable[self.first_discipline]['START'],
                schedule[now_weeknumber][now_weekday][self.first_discipline]['CABINET'],
                schedule[now_weeknumber][now_weekday][self.first_discipline]['TEACHER'],
                schedule[now_weeknumber][now_weekday][self.first_discipline]['TYPE'],
            )
            vkbot.set_chat_title_if_not_equals(self.chat_id, vk_title)
            return
        # Текущая пара
        elif int(self.first_discipline) <= int(current_discipline) <= int(self.last_discipline):
            if current_discipline in schedule[now_weeknumber][now_weekday]:
                vk_title = "6221|{} {} {}({})".format(
                    timetable[current_discipline]['START'],
                    schedule[now_weeknumber][now_weekday][current_discipline]['CABINET'],
                    schedule[now_weeknumber][now_weekday][current_discipline]['TEACHER'],
                    schedule[now_weeknumber][now_weekday][current_discipline]['TYPE'])
                vkbot.set_chat_title_if_not_equals(self.chat_id, vk_title)
                return
        # После пар
        elif int(current_discipline) > int(self.last_discipline):
            self.change_title_on_default()
        else:
            vkbot.set_chat_title_if_not_equals(self.chat_id, 'втф я сломался, АНДРЕЙ ЧИНИ')
