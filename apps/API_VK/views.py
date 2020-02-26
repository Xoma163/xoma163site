import datetime
import json
import threading

from django.http import HttpResponse, JsonResponse

from apps.API_VK.APIs.yandex_geo import get_address
from apps.API_VK.models import VkUser, Log, VkChat
from xoma163site.wsgi import vk_bot


def where_is_me(request):
    log = Log()
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
            msg1 = f"Я нахожусь примерно тут:\n" \
                   f"{address}\n"
        else:
            msg1 = ""
        msg2 = f"Позиция на карте:\n" \
               f"https://yandex.ru/maps/?ll={lon}%2C{lat}&mode=search&text={lat}%2C%20{lon}&z=16\n"

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

    log.save()
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")


def check_bool(val):
    if type(val) is bool:
        return val

    if val.lower() == 'true':
        return True
    return False


def petrovich(request):
    from apps.API_VK.VkBot import parse_msg
    from apps.API_VK.VkEvent import VkEvent

    if request.method == "GET":
        msg = request.GET.get('msg', None)
        test = check_bool(request.GET.get('test', False))
        send = check_bool(request.GET.get('send', False))
        from_chat = check_bool(request.GET.get('from_chat', True))
    elif request.method == "POST":
        msg = request.POST.get('msg', None)
        test = check_bool(request.POST.get('test', False))
        send = check_bool(request.POST.get('send', True))
        from_chat = check_bool(request.POST.get('from_chat', True))
    else:
        return JsonResponse({'error': 'only get or post'}, json_dumps_params={'ensure_ascii': False})

    if not msg:
        return JsonResponse({'error': 'empty param msg'}, json_dumps_params={'ensure_ascii': False})
    if len(msg) == 0:
        return JsonResponse({'error': 'empty msg'}, json_dumps_params={'ensure_ascii': False})

    user = VkUser.objects.get(user_id=3379762)
    if test:
        chat = VkChat.objects.get(chat_id=2000000002)
    else:
        chat = VkChat.objects.get(chat_id=2000000001)

    vk_event = {
        'parsed': parse_msg(msg),
        'sender': user,
        'api': True
    }
    if from_chat:
        vk_event['chat'] = chat
        vk_event['peer_id'] = chat.chat_id
    else:
        vk_event['chat'] = None
        vk_event['peer_id'] = user.user_id

    vk_event_object = VkEvent(vk_event)

    res = vk_bot.menu(vk_event_object, send=False)
    if send:
        x1 = threading.Thread(target=send_messages,
                              args=(vk_bot, vk_event['peer_id'], f"{user}(Алиса):\n{msg}",))
        x1.start()
        x2 = threading.Thread(target=send_messages, args=(vk_bot, vk_event['peer_id'], res,))
        x2.start()

    return JsonResponse({'res': res}, json_dumps_params={'ensure_ascii': False})


def send_messages(vk_bot, peer_id, msgs):
    vk_bot.parse_and_send_msgs(peer_id, msgs)


def chat(request):
    msg = request.GET.get('msg', None)
    test = check_bool(request.GET.get('test', False))

    if not msg:
        return JsonResponse({'error': 'empty param msg'}, json_dumps_params={'ensure_ascii': False})
    if len(msg) == 0:
        return JsonResponse({'error': 'empty msg'}, json_dumps_params={'ensure_ascii': False})

    user = VkUser.objects.get(user_id=3379762)
    if test:
        chat = VkChat.objects.get(chat_id=2000000002)
    else:
        chat = VkChat.objects.get(chat_id=2000000001)

    vk_bot.parse_and_send_msgs(chat.chat_id, f"{user}:\n{msg}")

    return JsonResponse({'res': 'success'}, json_dumps_params={'ensure_ascii': False})


def get_user_by_imei(imei):
    return VkUser.objects.filter(imei=imei).first()
