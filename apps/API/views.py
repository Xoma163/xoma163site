import json

# Create your views here.
from django.http import HttpResponse

from xoma163site.settings import tBot


def whereisme(request):
    try:
        where = request.GET.get('where', None)
        dictionary = {'home': 'дома', 'work': 'на работе'}
        msg = ("Всё хорошо, я %s" % dictionary[where])
        response_data = {'success': True, 'msg': msg}
        tBot.bot.send_message(tBot.XOMA163_CHAT_ID, msg)
        # bot.send_message(teleBot.LANA_CHAT_ID, msg)

    except Exception as e:
        response_data = {'success': False, 'exeption': str(e)}
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")

