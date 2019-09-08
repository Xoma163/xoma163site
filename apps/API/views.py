import json

from django.http import HttpResponse

from apps.API.models import TelegramChatId, TelegramTrustIMEI, Log
from xoma163site.settings import tBot


# ToDo. Если сканируем одну и ту же метку, то меняем сообщение
def where_is_me(request):
    log = Log.objects.create()
    try:
        where = request.GET.get('where', None)
        log.event = where
        imei = request.GET.get('imei', None)
        log.imei = imei
        author = check_imei(imei)
        log.author = author
        if author is None:
            log.msg = "Wrong IMEI"
            log.save()
            return HttpResponse(json.dumps({'success': True, 'error': 'Wrong IMEI'}, ensure_ascii=False),
                                content_type="application/json")

        dictionary = {'home': 'дома', 'work': 'на работе'}
        msg = "Всё хорошо, я %s\n%s" % (dictionary[where], author.name)
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
