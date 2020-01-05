import datetime
import json

from django.http import HttpResponse, JsonResponse

from apps.API_VK.APIs.yandex_geo import get_address
from apps.API_VK.models import VkUser, Log, VkChat
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
            if imei is None or imei == "":
                log.msg = "IMEI None"
                log.save()
                return HttpResponse(json.dumps({'success': True, 'error': 'None IMEI'}, ensure_ascii=False),
                                    content_type="application/json")
            author = get_user_by_imei(imei)

            if author is None:
                log.msg = "Не найден IMEI"
                log.save()
                return HttpResponse(json.dumps({'success': True, 'error': 'Wrong IMEI'}, ensure_ascii=False),
                                    content_type="application/json")
            log.author = author

            recipients = author.send_notify_to.all()
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


def petrovich(request):
    from apps.API_VK.command.commands.Games.Petrovich import Petrovich

    chat = VkChat.objects.get(chat_id=2000000002)
    command = Petrovich()
    res = command.start_real(chat)
    vk_bot.parse_and_send_msgs(res, chat.chat_id, with_wrapper=True)
    return JsonResponse({'res': res}, json_dumps_params={'ensure_ascii': False})


def get_user_by_imei(imei):
    return VkUser.objects.filter(imei=imei).first()
