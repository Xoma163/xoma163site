from django.contrib.auth.models import Group

from apps.API_VK.command.commands.AdminCommands.Ban import Ban
from apps.API_VK.command.commands.AdminCommands.Command import Command
from apps.API_VK.command.commands.AdminCommands.Control import Control
from apps.API_VK.command.commands.AdminCommands.DeBan import DeBan
from apps.API_VK.command.commands.AdminCommands.Reboot import Reboot
from apps.API_VK.command.commands.AdminCommands.Service.get_conversations import get_conversations
from apps.API_VK.command.commands.AdminCommands.Service.get_user_by_id import get_user_by_id
from apps.API_VK.command.commands.AdminCommands.Service.update_users import update_users
from apps.API_VK.command.commands.Bash import Bash
from apps.API_VK.command.commands.Birds import Birds
from apps.API_VK.command.commands.Cat import Cat
from apps.API_VK.command.commands.City import City
from apps.API_VK.command.commands.Conference import Conference
from apps.API_VK.command.commands.Counter import Counter
from apps.API_VK.command.commands.Counters import Counters
from apps.API_VK.command.commands.EasyCommands.Apologize import Apologize
from apps.API_VK.command.commands.EasyCommands.Bye import Bye
from apps.API_VK.command.commands.EasyCommands.Clear import Clear
from apps.API_VK.command.commands.EasyCommands.Discord import Discord
from apps.API_VK.command.commands.EasyCommands.Donate import Donate
from apps.API_VK.command.commands.EasyCommands.GameConference import GameConference
from apps.API_VK.command.commands.EasyCommands.Git import Git
from apps.API_VK.command.commands.EasyCommands.Hi import Hi
from apps.API_VK.command.commands.EasyCommands.Nya import Nya
from apps.API_VK.command.commands.EasyCommands.Shit import Shit
from apps.API_VK.command.commands.EasyCommands.Sho import Sho
from apps.API_VK.command.commands.EasyCommands.Sorry import Sorry
from apps.API_VK.command.commands.EasyCommands.Start_lada import Start_lada
from apps.API_VK.command.commands.EasyCommands.Thanks import Thanks
from apps.API_VK.command.commands.Find import Find
from apps.API_VK.command.commands.Fix import Fix
from apps.API_VK.command.commands.Games.Codenames import Codenames
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
from apps.API_VK.command.commands.Meme import Meme
from apps.API_VK.command.commands.Memes import Memes
from apps.API_VK.command.commands.ModeratorCommands.Debug import Debug
from apps.API_VK.command.commands.ModeratorCommands.Logs import Logs
from apps.API_VK.command.commands.ModeratorCommands.Restart import Restart
from apps.API_VK.command.commands.ModeratorCommands.Start import Start
from apps.API_VK.command.commands.ModeratorCommands.Stop import Stop
from apps.API_VK.command.commands.ModeratorCommands.Stop import Stop
from apps.API_VK.command.commands.ModeratorCommands.Temperature import Temperature
from apps.API_VK.command.commands.ModeratorCommands.Uptime import Uptime
from apps.API_VK.command.commands.ModeratorCommands.Words import Words
from apps.API_VK.command.commands.Notifies import Notifies
from apps.API_VK.command.commands.Notify import Notify
from apps.API_VK.command.commands.Permissions import Permissions
from apps.API_VK.command.commands.Praise import Praise
from apps.API_VK.command.commands.Quote import Quote
from apps.API_VK.command.commands.Quotes import Quotes
from apps.API_VK.command.commands.Random import Random
from apps.API_VK.command.commands.Register import Register
from apps.API_VK.command.commands.Scold import Scold
from apps.API_VK.command.commands.ShortLinks import ShortLinks
from apps.API_VK.command.commands.Status import Status
from apps.API_VK.command.commands.Stream import Stream
from apps.API_VK.command.commands.StudentCommands.GoogleDrive import GoogleDrive
from apps.API_VK.command.commands.StudentCommands.Mail import Mail
# from apps.API_VK.command.commands.StudentCommands.TimeTable import TimeTable
# from apps.API_VK.command.commands.StudentCommands.Week import Week
from apps.API_VK.command.commands.Time import Time
from apps.API_VK.command.commands.Translate import Translate
from apps.API_VK.command.commands.Transliteration import Transliteration
from apps.API_VK.command.commands.UnRegister import UnRegister
from apps.API_VK.command.commands.Uyu import Uyu
from apps.API_VK.command.commands.Weather import Weather
from apps.API_VK.command.commands.Where import Where
from apps.API_VK.command.commands.Who import Who
from apps.API_VK.command.commands.YandexChat import YandexChat
from apps.API_VK.command.commands.YesNo import YesNo

commands = [
    # Week(), TimeTable(),
    Conference(),
    YesNo(), Thanks(), Stream(), Where(), Birds(), Register(), UnRegister(), Petrovich(), Statistics(),
    Random(), Sorry(), Help(), Weather(), Praise(), Scold(), Quote(), Quotes(), Keyboard(), KeyboardHide(),
    Uyu(), Hi(), Bye(), Nya(), Shit(), Git(), Donate(), Discord(), Issue(), Issues(), Joke(),
    GoogleDrive(), Mail(), Ban(), DeBan(), Command(), Start(), Stop(), Restart(), Reboot(), Control(),
    get_user_by_id(), update_users(), get_conversations(), Logs(), Words(), Temperature(), Apologize(), Clear(),
    Find(), Rate(), Rates(), Translate(), Uptime(), Counter(), Counters(), TicTacToe(), Status(), Fix(), Debug(),
    Start_lada(), ShortLinks(), Time(), Transliteration(), Who(), Permissions(), Cat(), Sho(),
    Codenames(), GameConference(), Bash(), Meme(), Memes(), Notify(), Notifies(), City(), YandexChat()
]


# underscore_symbol = "̲"
# for command in commands:
#     if command.help_text:
#         find_dash = command.help_text.find('-') - 1
#         underscore_help_text = underscore_symbol.join(list(command.help_text[:find_dash]))
#         other_help_text = command.help_text[find_dash:]
#         command.help_text = underscore_symbol + underscore_help_text + other_help_text


def get_commands():
    return commands


def get_groups():
    groups = Group.objects.all().values('name')
    groups_names = [group['name'] for group in groups]
    return groups_names


GROUPS = get_groups()

HELP_TEXT = {group: "" for group in GROUPS}
API_HELP_TEXT = {group: "" for group in GROUPS}


def generate_help_text():
    help_text_list = {group: [] for group in GROUPS}
    api_help_text_list = {group: [] for group in GROUPS}
    for command in commands:
        if command.help_text:
            help_text = command.help_text
            if type(help_text) == str:
                help_text = {'for': command.access, 'text': help_text}

            if type(help_text) == dict:
                help_text = [help_text]

            if type(help_text) == list:
                for text in help_text:
                    help_text_list[text['for']].append(text['text'])
                    if command.api:
                        api_help_text_list[text['for']].append(text['text'])

    for group in GROUPS:
        help_text_list[group].sort()
        HELP_TEXT[group] = "\n".join(help_text_list[group])

        api_help_text_list[group].sort()
        API_HELP_TEXT[group] = "\n".join(api_help_text_list[group])


def get_keyboard():
    keys = {group: [] for group in GROUPS}
    for command in commands:
        key = command.keyboard
        if key:
            if type(key) == dict:
                key = [key]
            if type(key) == list:
                for elem in key:
                    if 'for' in elem:
                        keys[elem['for']].append(elem)
                    else:
                        keys[command.access].append(elem)

    buttons = {group: [] for group in GROUPS}
    for k in keys:
        keys[k] = sorted(keys[k], key=lambda i: (i['row'], i['col']))
    color_translate = {
        'red': 'negative',
        'green': 'positive',
        'blue': 'primary',
        'gray': 'secondary'
    }

    for k in keys:
        row = []
        current_row = 0
        for key in keys[k]:
            if not current_row:
                row = []
                current_row = key['row']

            elif key['row'] != current_row:
                buttons[k].append(row)
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
            buttons[k].append(row)
    return buttons


generate_help_text()
KEYBOARDS = get_keyboard()

EMPTY_KEYBOARD = {
    "one_time": False,
    "buttons": []
}
