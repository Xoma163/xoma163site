from django.shortcuts import render, redirect

# Create your views here.
from apps.web.models import Order, Tare, User, Session


def index(request):
    return render(request, "web/index.html")


def calc(request):
    if request.method == "POST":
        session = Session()
        session.name = request.POST['name']
        session.save()
        return redirect('/calc/{}'.format(session.id))
    else:
        sessions = Session.objects.all()
        return render(request, "web/sessions.html", {'sessions': sessions})


def calc_session(request, session_id):
    order = Order.objects.filter(session_id=session_id)
    tares = Tare.objects.all()
    users = User.objects.filter(session_id=session_id)
    return render(request, "web/calc.html", {"order": order, "tares": tares, "users": users, "session_id": session_id})
