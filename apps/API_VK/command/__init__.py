from apps.API_VK.command.commands.AdminCommands.Ban import Ban
from apps.API_VK.command.commands.AdminCommands.Command import Command
from apps.API_VK.command.commands.AdminCommands.Control import Control
from apps.API_VK.command.commands.AdminCommands.DeBan import DeBan
from apps.API_VK.command.commands.AdminCommands.Reboot import Reboot
from apps.API_VK.command.commands.AdminCommands.Service.get_conversations import get_conversations
from apps.API_VK.command.commands.AdminCommands.Service.get_user_by_id import get_user_by_id
from apps.API_VK.command.commands.AdminCommands.Service.update_users import update_users
from apps.API_VK.command.commands.Birds import Birds
from apps.API_VK.command.commands.Counter import Counter
from apps.API_VK.command.commands.Counters import Counters
from apps.API_VK.command.commands.EasyCommands.Apologize import Apologize
from apps.API_VK.command.commands.EasyCommands.Bye import Bye
from apps.API_VK.command.commands.EasyCommands.Clear import Clear
from apps.API_VK.command.commands.EasyCommands.Discord import Discord
from apps.API_VK.command.commands.EasyCommands.Donate import Donate
from apps.API_VK.command.commands.EasyCommands.Git import Git
from apps.API_VK.command.commands.EasyCommands.Hi import Hi
from apps.API_VK.command.commands.EasyCommands.Nya import Nya
from apps.API_VK.command.commands.EasyCommands.Shit import Shit
from apps.API_VK.command.commands.EasyCommands.Sorry import Sorry
from apps.API_VK.command.commands.EasyCommands.Thanks import Thanks
from apps.API_VK.command.commands.Find import Find
from apps.API_VK.command.commands.Games.Petrovich import Petrovich
from apps.API_VK.command.commands.Games.Rate import Rate
from apps.API_VK.command.commands.Games.Rates import Rates
from apps.API_VK.command.commands.Games.Statistics import Statistics
from apps.API_VK.command.commands.Games.TicTacToe import TicTacToe
from apps.API_VK.command.commands.Help import Help
from apps.API_VK.command.commands.Issue import Issue
from apps.API_VK.command.commands.Issues import Issues
from apps.API_VK.command.commands.Joke import Joke
from apps.API_VK.command.commands.Keyboard import Keyboard
from apps.API_VK.command.commands.KeyboardHide import KeyboardHide
from apps.API_VK.command.commands.ModeratorCommands.Logs import Logs
from apps.API_VK.command.commands.ModeratorCommands.Restart import Restart
from apps.API_VK.command.commands.ModeratorCommands.Start import Start
from apps.API_VK.command.commands.ModeratorCommands.Stop import Stop
from apps.API_VK.command.commands.ModeratorCommands.Stop import Stop
from apps.API_VK.command.commands.ModeratorCommands.Temperature import Temperature
from apps.API_VK.command.commands.ModeratorCommands.Uptime import Uptime
from apps.API_VK.command.commands.ModeratorCommands.Words import Words
from apps.API_VK.command.commands.Praise import Praise
from apps.API_VK.command.commands.Quote import Quote
from apps.API_VK.command.commands.Quotes import Quotes
from apps.API_VK.command.commands.Random import Random
from apps.API_VK.command.commands.Register import Register
from apps.API_VK.command.commands.Scold import Scold
from apps.API_VK.command.commands.Status import Status
from apps.API_VK.command.commands.Stream import Stream
from apps.API_VK.command.commands.StudentCommands.GoogleDrive import GoogleDrive
from apps.API_VK.command.commands.StudentCommands.Mail import Mail
from apps.API_VK.command.commands.StudentCommands.TimeTable import TimeTable
from apps.API_VK.command.commands.StudentCommands.Week import Week
from apps.API_VK.command.commands.Translate import Translate
from apps.API_VK.command.commands.UnRegister import UnRegister
from apps.API_VK.command.commands.Uyu import Uyu
from apps.API_VK.command.commands.Weather import Weather
from apps.API_VK.command.commands.Where import Where
from apps.API_VK.command.commands.YesNo import YesNo

commands = [YesNo(), Thanks(), Stream(), Where(), Birds(), Register(), UnRegister(), Petrovich(), Statistics(),
            Random(), Sorry(), Help(), Weather(), Praise(), Scold(), Quote(), Quotes(), Keyboard(), KeyboardHide(),
            Uyu(), Hi(), Bye(), Nya(), Shit(), Git(), Donate(), Discord(), Issue(), Issues(), Joke(), TimeTable(),
            GoogleDrive(), Week(), Mail(), Ban(), DeBan(), Command(), Start(), Stop(), Restart(), Reboot(), Control(),
            get_user_by_id(), update_users(), get_conversations(), Logs(), Words(), Temperature(), Apologize(), Clear(),
            Find(), Rate(), Rates(), Translate(), Uptime(), Counters(), Counter(), TicTacToe(), Status()
            ]


def get_commands():
    return commands


def get_help_text(attr=None):
    texts = ""
    if attr:
        for command in commands:
            if getattr(command, attr):
                if command.help_text:
                    texts += "{}\n".format(command.help_text)
    else:
        for command in commands:
            if not command.for_moderator and not command.for_admin and not command.for_student:
                if command.help_text:
                    texts += "{}\n".format(command.help_text)
    return texts


def get_keyboard(attr):
    keys = []
    for command in commands:
        key = getattr(command, attr)
        if key:
            if type(key) == dict:
                keys.append(key)
            elif type(key) == list:
                for elem in key:
                    keys.append(elem)

    buttons = []
    if keys is None:
        return []
    keys = sorted(keys, key=lambda i: (i['row'], i['col']))
    color_translate = {
        'red': 'negative',
        'green': 'positive',
        'blue': 'primary',
        'gray': 'secondary'
    }
    row = []
    current_row = 0
    for key in keys:
        if not current_row:
            row = []
            current_row = key['row']

        elif key['row'] != current_row:
            buttons.append(row)
            current_row = key['row']
            row = []

        row.append(
            {
                "action": {
                    "type": "text",
                    "label": key['text']
                },
                "color": color_translate[key['color']]
            }
        )
    if len(row) > 0:
        buttons.append(row)
    return buttons


ADMIN_TEXTS = get_help_text('for_admin')
MODERATOR_TEXTS = get_help_text('for_moderator')
STUDENT_TEXTS = get_help_text('for_student')
COMMON_TEXTS = get_help_text()

ADMIN_BUTTONS = get_keyboard('keyboard_admin')
MODERATOR_BUTTONS = get_keyboard('keyboard_moderator')
STUDENT_BUTTONS = get_keyboard('keyboard_student')
USER_BUTTONS = get_keyboard('keyboard_user')

EMPTY_KEYBOARD = {
    "one_time": False,
    "buttons": []
}
