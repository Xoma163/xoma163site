from django.shortcuts import render, redirect

from apps.web.models import Order, Tare, User, Session
from secrets.secrets import secrets


def index(request):
    return render(request, "web/index.html")


def calc(request):
    if request.method == "POST":
        sessions = Session.objects.all()
        if len(sessions) >= 100:
            return render(request, "web/sessions.html", {'sessions': sessions})
        session = Session()
        session.name = request.POST['name']
        session.save()
        return redirect(f'/calc/{session.id}')
    else:
        sessions = Session.objects.all()
        return render(request, "web/sessions.html", {'sessions': sessions})


def calc_session(request, session_id):
    order = Order.objects.filter(session_id=session_id)
    tares = Tare.objects.all()
    users = User.objects.filter(session_id=session_id)
    return render(request, "web/calc.html", {"order": order, "tares": tares, "users": users, "session_id": session_id})


def chat(request):
    petrovich_group_id = secrets['vk']['bot']['group_id']
    return render(request, "web/chat.html", {'petrovich_group_id': petrovich_group_id})


def eugene(request):
    return render(request, "web/eugene.html")
