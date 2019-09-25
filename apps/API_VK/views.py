import datetime
import json

from django.http import HttpResponse

from apps.API_VK.models import VkChatId, TrustIMEI, Log
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

            positions = {
                "home": {"on": "дома", "from": "из дома", "count": 0},
                "work": {"on": "на работе", "from": "с работы", "count": 0},
                "university": {"on": "в универе", "from": "из универа", "count": 0},
            }

            today = datetime.datetime.now()
            today_logs = Log.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day,
                                            author=author)

            # ToDo: Тяжелая операция для базы
            for today_log in today_logs:
                if today_log.event in positions:
                    positions[today_log.event]['count'] += 1

            msg = None
            if positions[event]['count'] % 2 == 0:
                msg = "Выдвигаюсь {}.".format(positions[event]['from'])
            elif positions[event]['count'] % 2 == 1:
                msg = "Я {}.".format(positions[event]['on'])

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
