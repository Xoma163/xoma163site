import datetime
import json

from django.http import HttpResponse

from apps.API.models import TelegramChatId, TelegramTrustIMEI, Log
from xoma163site.settings import tBot


def where_is_me(request):
    log = Log.objects.create()
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

        dictionary_on = {'home': 'дома', 'work': 'на работе'}
        dictionary_from = {'home': 'из дома', 'work': 'с работы'}

        today = datetime.datetime.now()
        today_logs = Log.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day,
                                        author=author)

        count_work = 0
        count_home = 0
        for today_log in today_logs:
            if today_log.event == 'work':
                count_work += 1
            if today_log.event == 'home':
                count_home += 1

        msg = None
        if event == 'work':
            if count_work % 2 == 0:
                msg = "Всё хорошо, я %s.\n%s" % (dictionary_on[event], author.name)
            else:
                msg = "Выдвигаюсь %s.\n%s" % (dictionary_from[event], author.name)
        elif event == 'home':
            if count_home % 2 == 0:
                msg = "Выдвигаюсь %s.\n%s" % (dictionary_from[event], author.name)
            else:
                msg = "Всё хорошо, я %s.\n%s" % (dictionary_on[event], author.name)

        if msg is None:
            log.msg = "Wrong event(?)"
            log.save()
            return HttpResponse(json.dumps({'success': True, 'error': 'Wrong IMEI'}, ensure_ascii=False),
                                content_type="application/json")

        log.msg = msg
        chats = TelegramChatId.objects.filter(is_active=True)

        for chat in chats:
            tBot.bot.send_message(chat.chat_id, msg)

        response_data = {'success': True, 'msg': msg}
        log.success = True
    except Exception as e:
        response_data = {'success': False, 'exeption': str(e)}
        log.msg = str(e)
    log.save()
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")


def check_imei(imei):
    imeis = TelegramTrustIMEI.objects.filter(is_active=True)
    for item in imeis:
        if imei == item.imei:
            return item
    return None
