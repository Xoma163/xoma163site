import json

from django.http import JsonResponse

from apps.web.models import Order, Product, User


def add_row(request):
    data = request.POST.copy()
    product = Product()
    product.session_id = data['sessionID']
    product_data = json.loads(data['product'])
    if product_data:
        product.name = product_data['name']
        product.count = product_data['count']
        if product_data['tareId'] and product_data['tareId'] != "None":
            product.tare_id = product_data['tareId']
        product.price = product_data['price']
        if product_data['userID'] and product_data['userID'] != "None":
            product.user_id = product_data['userID']
        product.is_bought = product_data['isBought']
    product.save()

    order = Order()
    order.session_id = data['sessionID']
    order.product = product
    order.save()
    return JsonResponse({'id': product.id}, json_dumps_params={'ensure_ascii': False})


def del_row(request):
    data = request.POST.copy()
    session_id = data['sessionID']
    _id = data['id']
    product = Product.objects.filter(id=_id, session_id=session_id).first()
    Order.objects.filter(session_id=session_id, product=product).delete()
    product.delete()
    return JsonResponse({'status': 'ok'}, json_dumps_params={'ensure_ascii': False})


def save_rows(request):
    data = request.POST.copy()
    session_id = data['sessionID']
    orders = json.loads(data['orders'])

    statistics = {'updated': 0, 'created': 0}
    for order in orders:
        product = order['product']
        for key in product:
            if product[key] == '' or product[key] == 'None':
                product[key] = None
        # [0] - игнорирование параметра created
        existed_product = Product.objects.update_or_create(session_id=session_id, id=product['id'],
                                                           defaults=product)[0]
        # order = Order.objects.filter(session_id=session_id, id=product['id']).update(**order)
        if existed_product:
            statistics['updated'] += 1
        elif existed_product:
            statistics['created'] += 1

    return JsonResponse({'status': 'ok', 'statistics': statistics}, json_dumps_params={'ensure_ascii': False})


def add_user(request):
    data = request.POST.copy()

    new_user = User()
    new_user.name = data['name']
    new_user.session_id = data['sessionID']
    new_user.save()

    return JsonResponse({'id': new_user.id}, json_dumps_params={'ensure_ascii': False})


def del_user(request):
    data = request.POST.copy()
    session_id = data['sessionID']
    _id = data['id']
    User.objects.filter(id=_id, session_id=session_id).first().delete()

    return JsonResponse({'status': 'ok'}, json_dumps_params={'ensure_ascii': False})


def save_users(request):
    data = request.POST.copy()
    session_id = data['sessionID']
    users = json.loads(data['users'])

    statistics = {'updated': 0, 'created': 0}
    for user in users:
        if user['id'] is not None and user['id'] != "None":
            User.objects.update_or_create(session_id=session_id,
                                          id=user['id'],
                                          defaults=user)
            statistics['updated'] += 1

        else:
            new_user = User()
            new_user.name = user['name']
            new_user.session_id = session_id
            new_user.save()
            statistics['created'] += 1

    return JsonResponse({'status': 'ok', 'statistics': statistics}, json_dumps_params={'ensure_ascii': False})


def get_calculate(request):
    data = request.POST.copy()
    session_id = data['sessionID']
    users = list(User.objects.filter(session_id=session_id).values('name'))
    users = {u['name']: {'money': 0} for u in users}

    orders = Order.objects.filter(session_id=session_id)

    for order in orders:
        users[order.product.user.name]['money'] += order.product.price

    users = dict(sorted(users.items(), key=lambda x: x[1]['money'], reverse=True))

    total_money = sum([users[user]['money'] for user in users])
    avg_money = round(total_money / len(users))

    #
    for key in users:
        user = users[key]
        user['debt'] = round(avg_money - user['money'])
    #
    users_list = []
    for key, value in users.items():
        temp = [key, value]
        users_list.append(temp)

    rows = []
    for i, user in enumerate(users_list):
        if i == 0:
            continue
        if user[1]['debt'] > 0:
            rows.append(f"{user[0]}\t\t→\t\t{users_list[0][0]}\t{user[1]['debt']} руб")
        elif user[1]['debt'] < 0:
            rows.append(f"{users_list[0][0]}\t\t→\t\t{user[0]}\t{abs(user[1]['debt'])} руб")

    rows.append("----------")
    rows.append(f"Общая сумма - {total_money}")
    rows.append(f"Средний чек - {avg_money}")

    return JsonResponse({'status': 'ok', 'result': rows}, json_dumps_params={'ensure_ascii': False})
