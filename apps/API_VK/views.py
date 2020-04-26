import datetime
import json

from django.http import HttpResponse, JsonResponse

from apps.API_VK.APIs.yandex_geo import get_address
from apps.API_VK.models import VkUser, Log, APIUser, APITempUser
from xoma163site.wsgi import vk_bot


def send_json(message):
    return JsonResponse(message, json_dumps_params={'ensure_ascii': False})


def where_is_me(request):
    from apps.API_VK.command.CommonMethods import localize_datetime

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

        today = localize_datetime(datetime.datetime.utcnow(), author.city.timezone.name)
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
    if isinstance(val, bool):
        return val

    if val.lower() == 'true':
        return True
    return False


def petrovich_api(request):
    def register(vk_id):
        vk_id = vk_id.replace('-', '').replace(' ', '')
        user_id = int(vk_id)
        vk_user = VkUser.objects.filter(user_id=user_id).first()
        if vk_user:
            yandex_temp_user = APITempUser.objects.filter(vk_user=vk_user).first()
            if yandex_temp_user:
                vk_bot.send_message(vk_user.user_id, yandex_temp_user.code)
                return "Отправил код повторно"
            else:
                yandex_temp_user = APITempUser(vk_user=vk_user, user_id=client_id)
                yandex_temp_user.save()
                vk_bot.send_message(vk_user.user_id, yandex_temp_user.code)
                return "Отправил код подтверждения в ВК. Пришлите мне его. Код {код}"
        else:
            return "Вы не зарегистрированы. Напишите боту в ВК любое сообщение"

    def confirm(code):
        code = code.replace('-', '').replace(' ', '')

        yandex_temp_user = APITempUser.objects.filter(user_id=client_id).first()
        if not yandex_temp_user:
            return "Вы не зарегистрированны. Пришлите ВК {ваш ид}"
        if yandex_temp_user.tries <= 0:
            return "Вы превысили максимальное число попыток"
        if yandex_temp_user.code != code:
            yandex_temp_user.tries -= 1
            yandex_temp_user.save()
            return f"Неверный код. Осталось попыток - {yandex_temp_user.tries}"
        APIUser(vk_user=yandex_temp_user.vk_user, user_id=yandex_temp_user.user_id).save()
        yandex_temp_user.delete()
        return "Успешно зарегистрировал. Можете пользоваться функционалом"

    from apps.API_VK.VkEvent import VkEvent

    if 'Client-Id' not in request.headers:
        return send_json({'error': 'empty header "Client-Id"'})

    if request.method == "GET":
        msg = request.GET.get('msg', None)
        send = check_bool(request.GET.get('send', False))
    else:
        return send_json({'error': 'GET request required'})
    if not msg:
        return send_json({'error': 'empty param msg'})
    if len(msg) == 0:
        return send_json({'error': 'empty msg'})

    client_id = request.headers['Client-Id']
    yandex_user = APIUser.objects.filter(user_id=client_id).first()

    if not yandex_user:
        msg_list = msg.split(' ')
        for i, _ in enumerate(msg_list):
            msg_list[i] = msg_list[i].lower()
        if msg_list and len(msg_list) >= 2:
            if msg_list[0] == 'вк':
                return send_json({'res': register(msg.split(' ', 1)[1])})
            elif msg_list[0] == 'код':
                return send_json({'res': confirm(msg.split(' ', 1)[1])})
        return JsonResponse({'res': "Вы не зарегистрированны. Пришлите ВК {ваш ид}"},
                            json_dumps_params={'ensure_ascii': False})
    else:
        user = yandex_user.vk_user
    chat = yandex_user.vk_chat

    vk_event = {
        'message': {
            'text': msg
        },
        'sender': user,
        'api': True,
        'yandex': {'client_id': client_id}
    }
    if chat:
        vk_event['chat'] = chat
        vk_event['peer_id'] = chat.chat_id
    else:
        vk_event['chat'] = None
        vk_event['peer_id'] = user.user_id

    vk_event_object = VkEvent(vk_event)
    res = vk_bot.menu(vk_event_object, send=False)
    if send:
        vk_bot.parse_and_send_msgs_thread(vk_event['peer_id'], f"{user}(Алиса):\n{msg}")
        vk_bot.parse_and_send_msgs_thread(vk_event['peer_id'], res)
    return send_json({'res': res})


def chat_api(request):
    if 'Client-Id' not in request.headers:
        return send_json({'error': 'empty header "Client-Id"'})
    client_id = request.headers['Client-Id']

    if request.method == "GET":
        msg = request.GET.get('msg', None)
        if msg is None:
            return send_json({'error': 'empty param msg'})
        if len(msg) == 0:
            return send_json({'error': 'empty msg'})
    else:
        return send_json({'error': 'GET request required'})

    yandex_user = APIUser.objects.filter(user_id=client_id).first()
    if not yandex_user:
        return send_json({'error': 'user not registered'})

    user = yandex_user.vk_user
    chat = yandex_user.vk_chat
    if not chat:
        return send_json({'error': 'User chat is not registered'})

    vk_bot.parse_and_send_msgs_thread(chat.chat_id, f"{user}:\n{msg}")
    return send_json({'res': 'success'})


def get_user_by_imei(imei):
    return VkUser.objects.filter(imei=imei).first()
