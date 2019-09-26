import datetime
import json

from django.http import HttpResponse

from apps.API_VK.models import VkChatId, TrustIMEI, Log
from apps.API_VK.yandex_geo import get_address
from xoma163site.wsgi import vkbot


def where_is_me(request):
    log = Log.objects.create()
    tries = 0
    response_data = []
    while log.success is not True and tries < 10:
        try:
            event = request.GET.get('where', None)
            log.event = event
            imei = request.GET.get('imei', None)
            log.imei = imei
            author = check_imei(imei)
            log.author = author
            if author is None:
                log.msg = "Wrong IMEI"
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

                # ToDo: Тяжелая операция для базы
                for today_log in today_logs:
                    if today_log.event in positions:
                        positions[today_log.event]['count'] += 1

                msg = positions[event][positions[event]['count'] % 2]

                if msg is None:
                    log.msg = "Wrong event(?)"
                    log.save()
                    return HttpResponse(json.dumps({'success': True, 'error': 'Wrong IMEI'}, ensure_ascii=False),
                                        content_type="application/json")

            log.msg = msg
            msg += "\n%s" % author
            chats = VkChatId.objects.filter(is_active=True)

            for chat in chats:
                vkbot.send_message(chat.chat_id, msg)

            response_data = {'success': True, 'msg': msg}
            log.success = True

        except Exception as e:
            response_data = {'success': False, 'exeption': str(e)}
            log.msg = str(e)
        tries += 1
        response_data['tries'] = tries

    log.save()
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")


def check_imei(imei):
    imeis = TrustIMEI.objects.filter(is_active=True)
    for item in imeis:
        if imei == item.imei:
            return item
    return None
