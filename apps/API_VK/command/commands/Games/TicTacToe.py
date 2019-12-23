import json
from threading import Lock

from django.db.models import Q

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import TicTacToeSession, Gamer

MORE_HIDE_KEYBOARD = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "label": "Крестики"
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": "Скрыть"
                },
                "color": "secondary"
            }
        ],
    ]
}

lock = Lock()


class TicTacToe(CommonCommand):
    def __init__(self):
        names = ["крестики", "крестики-нолики", "нолики"]
        super().__init__(names, check_int_args=[0, 1])

    def start(self):
        lock.acquire()
        sender = self.vk_event.sender

        if len(Gamer.objects.filter(user=sender)) == 0:
            Gamer(**{'user': sender}).save()

        session = TicTacToeSession.objects.filter(Q(user1=sender) | Q(user2=sender)).first()
        # Если существует такая сессия, где игрок находится в ней
        if session:
            # Если оба игрока существуют в сессии
            if session.user1 is not None and session.user2 is not None:
                # Если переданы аргументы
                if self.vk_event.args:
                    # Шаг игры
                    self.step_game(session)
                    lock.release()
                    return
                else:
                    # Возвращаем пользователю клавиатуру, если он её потерял
                    self.vk_bot.send_message(sender.user_id, "Да держи ты свою клаву, ё-моё",
                                             keyboard=get_keyboard_by_board(json.loads(session.board)))
                    lock.release()
                    return
            # Если игрок только один и 99.9% что это user1
            else:
                lock.release()
                return "Ты начал игру. Подожди, когда подключится второй игрок"
        # Если нет такой сессии, в которой есть игрок
        else:
            waiting_session = TicTacToeSession.objects.filter(user2=None).first()
            # Если есть сессия, где пустует второй игрок
            if waiting_session:
                # То стартуем игру
                self.start_game(waiting_session)
                lock.release()
                return
            # Никаких свободных сессий нет - создаём новую
            else:
                new_session = TicTacToeSession()
                new_session.user1 = sender
                new_session.save()
                lock.release()
                return "Начинаем игру. Ждём второго игрока"

    def step_game(self, session):

        sender = self.vk_event.sender
        args = self.vk_event.args
        if sender != session.next_step:
            self.vk_bot.send_message(sender.user_id, "Ход второго игрока")
            return

        elem = ''
        if session.user1 == sender:
            elem = 'x'
        elif session.user2 == sender:
            elem = 'o'

        table = json.loads(session.board)
        if table[args[0]][args[1]] != '':
            self.vk_bot.send_message(sender.user_id, "Сюда нельзя ставить")
            return
        else:
            table[args[0]][args[1]] = elem

        res = check_win(table)
        if res:
            session.delete()
            if res == 'x':
                self.vk_bot.send_message(session.user1.user_id,
                                         "Игра закончена. Победитель - {}\n{}".format(
                                             session.user1,
                                             print_table(table)),
                                         keyboard=MORE_HIDE_KEYBOARD)
                self.vk_bot.send_message(session.user2.user_id,
                                         "Игра закончена. Победитель - {}\n{}".format(
                                             session.user1,
                                             print_table(table)),
                                         keyboard=MORE_HIDE_KEYBOARD)
                gamer = Gamer.objects.get(user=session.user1)
                gamer.tic_tac_toe_points += 1
                gamer.save()
            elif res == 'o':
                self.vk_bot.send_message(session.user1.user_id,
                                         "Игра закончена. Победитель - {}\n{}".format(
                                             session.user2,
                                             print_table(table)),
                                         keyboard=MORE_HIDE_KEYBOARD)
                self.vk_bot.send_message(session.user2.user_id,
                                         "Игра закончена. Победитель - {}\n{}".format(
                                             session.user2,
                                             print_table(table)),
                                         keyboard=MORE_HIDE_KEYBOARD)
                gamer = Gamer.objects.get(user=session.user2)
                gamer.tic_tac_toe_points += 1
                gamer.save()
            return
        elif check_end(table):
            session.delete()
            self.vk_bot.send_message(session.user1.user_id, "Ничья\n{}".format(print_table(table)),
                                     keyboard=MORE_HIDE_KEYBOARD)
            self.vk_bot.send_message(session.user2.user_id, "Ничья\n{}".format(print_table(table)),
                                     keyboard=MORE_HIDE_KEYBOARD)
            return

        board = get_keyboard_by_board(table)

        if session.next_step == session.user1:
            self.vk_bot.send_message(session.user1.user_id, "Ход сделан, ждём хода второго игрока", keyboard=board)
            self.vk_bot.send_message(session.user2.user_id, "Второй игрок сделал ход", keyboard=board)
            session.next_step = session.user2
        elif session.next_step == session.user2:
            self.vk_bot.send_message(session.user1.user_id, "Второй игрок сделал ход", keyboard=board)
            self.vk_bot.send_message(session.user2.user_id, "Ход сделан, ждём хода второго игрока", keyboard=board)
            session.next_step = session.user1

        session.board = json.dumps(table)
        session.save()

    def start_game(self, session):
        session.user2 = self.vk_event.sender
        session.next_step = session.user1
        session.save()
        keyboard = get_keyboard_by_board(json.loads(session.board))
        self.vk_bot.send_message(session.user1.user_id,
                                 "Второй игрок - {}\n Ваш ход\nВы играете за ❌".format(session.user2),
                                 keyboard=keyboard)
        self.vk_bot.send_message(session.user2.user_id,
                                 "Второй игрок - {}\n Ход второго игрока\nВы играете за ⭕".format(session.user1),
                                 keyboard=keyboard)


def check_win(table):
    for i in range(len(table)):
        res = check_win_elems([row for row in table[i]])
        if res:
            return res
        res = check_win_elems([row[i] for row in table])
        if res:
            return res

    res = check_win_elems([table[i][i] for i in range(len(table))])
    if res:
        return res

    res = check_win_elems([table[i][len(table[i]) - 1 - i] for i in range(len(table))])
    if res:
        return res

    return False


def check_win_elems(*args):
    args = args[0]
    val = args[0]
    result = True

    for arg in args:
        result = (arg != '') and (arg == val) and result
        if not result:
            return False

    return val


def check_end(table):
    for row in table:
        for elem in row:
            if elem == '':
                return False
    return True


def get_keyboard_by_board(table):
    buttons = []
    for i, row in enumerate(table):
        rows = []
        for j, elem in enumerate(row):
            rows.append(get_elem(elem, i, j))
        buttons.append(rows)

    keyboard = {
        "one_time": False,
        "buttons": buttons
    }
    return keyboard


def get_elem(elem, row, col):
    if elem == 'x':
        label = "❌"
        # color = "negative"
    elif elem == 'o':
        label = "⭕"
        # color = "primary"
    else:
        label = "&#12288;"
        color = "secondary"

    return {
        "action": {
            "type": "text",
            "label": label,
            "payload": json.dumps({"command": "крестики", "args": {"row": row, "col": col}}, ensure_ascii=False)
        },
        "color": "secondary"
        # "color": color
    }


def print_table(table):
    result = ""
    for row in table:
        rows = ""
        for elem in row:
            if elem == '':
                elem = '—'
            rows += elem.upper()
        result += rows + "\n"
    return result
