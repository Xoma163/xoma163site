import datetime
import json
import time

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.API_VK.APIs.yandex_geo import get_address
from apps.API_VK.models import VkUser, Log, Words
from xoma163site.wsgi import vk_bot


def where_is_me(request):
    log = Log()
    tries = 0
    response_data = []
    while log.success is not True and tries < 10:
        try:
            event = request.GET.get('where', None)
            log.event = event
            imei = request.GET.get('imei', None)
            log.imei = imei
            author = get_user_by_imei(imei)

            if author is None:
                log.msg = "Не найден IMEI"
                log.save()
                return HttpResponse(json.dumps({'success': True, 'error': 'Wrong IMEI'}, ensure_ascii=False),
                                    content_type="application/json")
            log.author = author

            recipients = get_recipients(author)
            if recipients is None:
                log.msg = "Не найден получатель"
                log.save()
                return HttpResponse(json.dumps({'success': True, 'error': 'Wrong IMEI'}, ensure_ascii=False),
                                    content_type="application/json")

            if event == 'somewhere':
                lat = request.GET.get('lat', None)
                lon = request.GET.get('lon', None)

                address = get_address(lat, lon)
                if address is not None:
                    msg1 = "Я нахожусь примерно тут:\n" \
                           "{}\n".format(address)
                else:
                    msg1 = ""
                msg2 = "Позиция на карте:\n" \
                       "https://yandex.ru/maps/?ll={1}%2C{0}&mode=search&text={0}%2C%20{1}&z=16\n".format(lat, lon)

                msg = msg1 + msg2
            else:
                positions = {
                    "home": {0: "Выхожу из дома", 1: "Я дома", "count": 0},
                    "work": {0: "Я на работе", 1: "Выхожу с работы", "count": 0},
                    "university": {0: "Я в универе", 1: "Выхожу из универа", "count": 0},
                }

                today = datetime.datetime.now()
                today_logs = Log.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day,
                                                author=author)
                for today_log in today_logs:
                    if today_log.event in positions:
                        positions[today_log.event]['count'] += 1
                msg = positions[event][positions[event]['count'] % 2]

                if msg is None:
                    log.msg = "Не найдено такое событие(?)"
                    log.save()
                    return HttpResponse(json.dumps({'success': True, 'error': 'Wrong IMEI'}, ensure_ascii=False),
                                        content_type="application/json")

            log.msg = msg
            msg += "\n%s" % author.name

            for recipient in recipients:
                if recipient.send_notify:
                    vk_bot.send_message(recipient.user_id, msg)

            response_data = {'success': True, 'msg': msg}
            log.success = True

        except Exception as e:
            response_data = {'success': False, 'exeption': str(e)}
            log.msg = str(e)
        tries += 1
        response_data['tries'] = tries

    log.save()
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")


@csrf_exempt
def add_new_words(request):
    if request.method == "POST":
        time1 = time.time()
        data = request.body
        if not data:
            response_data = {'status': 'error', 'status_code': 1, 'error': 'no data in request'}
            return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
        try:
            data = json.loads(data)
        except Exception as e:
            print(e)
            response_data = {'status': 'error', 'status_code': 2, 'error': 'cant parse json'}
            return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")

        if 'words' not in data:
            response_data = {'status': 'error', 'status_code': 3, 'error': 'no words in data'}
            return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
        words = data['words']

        statistics = {"total": 0, "added": 0, "updated": 0, "deleted": 0, "already_deleted": 0, "skipped": 0,
                      "errors": 0}
        errors = {"no_id_in_data": [], 'already_deleted': []}
        for word in words:
            if 'id' not in word:
                errors['no_id_in_data'].append(word)
                statistics['errors'] += 1
            else:
                new_word = Words.objects.filter(id=word['id'])

                if len(word) == 1:
                    if len(new_word) == 0:
                        errors['already_deleted'].append(word)
                        statistics['errors'] += 1
                    else:
                        new_word.delete()
                        statistics['deleted'] += 1
                else:
                    if len(new_word) == 0:
                        new_word = Words(**word)
                        new_word.save()
                        statistics['added'] += 1
                    else:
                        ex_word = list(new_word.values())[0]
                        ex_word = remove_none_in_dict(ex_word)
                        if ex_word == word:
                            statistics['skipped'] += 1
                        else:
                            new_word.update(**word)
                            statistics['updated'] += 1
            statistics['total'] += 1

        time2 = time.time()
        response_data = {'status': 'success', 'status_code': 200, 'time': time2 - time1,
                         'statistics': statistics, 'errors': errors}
        return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")


def remove_none_in_dict(old_dict):
    return {k: v for k, v in old_dict.items() if v is not None}


def get_user_by_imei(imei):
    return VkUser.objects.filter(imei=imei).first()


def get_recipients(user):
    return VkUser.objects.filter(get_notify_from=user)
