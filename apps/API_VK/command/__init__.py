from apps.API_VK.command.commands.AdminCommands.Ban import Ban
from apps.API_VK.command.commands.AdminCommands.Command import Command
from apps.API_VK.command.commands.AdminCommands.Control import Control
from apps.API_VK.command.commands.AdminCommands.DeBan import DeBan
from apps.API_VK.command.commands.AdminCommands.Service.get_user_by_id import get_user_by_id
from apps.API_VK.command.commands.AdminCommands.Service.update_users import update_users
from apps.API_VK.command.commands.AdminCommands.Start import Start
from apps.API_VK.command.commands.AdminCommands.Stop import Stop
from apps.API_VK.command.commands.AdminCommands.Stop import Stop
from apps.API_VK.command.commands.Birds import Birds
from apps.API_VK.command.commands.EasyCommands.Bye import Bye
from apps.API_VK.command.commands.EasyCommands.Donate import Donate
from apps.API_VK.command.commands.EasyCommands.Git import Git
from apps.API_VK.command.commands.EasyCommands.Hi import Hi
from apps.API_VK.command.commands.EasyCommands.Nya import Nya
from apps.API_VK.command.commands.EasyCommands.Shit import Shit
from apps.API_VK.command.commands.EasyCommands.Sorry import Sorry
from apps.API_VK.command.commands.EasyCommands.Thanks import Thanks
from apps.API_VK.command.commands.Help import Help
from apps.API_VK.command.commands.Issue import Issue
from apps.API_VK.command.commands.Issues import Issues
from apps.API_VK.command.commands.Joke import Joke
from apps.API_VK.command.commands.Keyboard import Keyboard
from apps.API_VK.command.commands.KeyboardHide import KeyboardHide
from apps.API_VK.command.commands.Petrovich import Petrovich
from apps.API_VK.command.commands.Praise import Praise
from apps.API_VK.command.commands.Quote import Quote
from apps.API_VK.command.commands.Quotes import Quotes
from apps.API_VK.command.commands.Random import Random
from apps.API_VK.command.commands.Register import Register
from apps.API_VK.command.commands.Scold import Scold
from apps.API_VK.command.commands.Statistics import Statistics
from apps.API_VK.command.commands.Stream import Stream
from apps.API_VK.command.commands.StudentCommands.GoogleDrive import GoogleDrive
from apps.API_VK.command.commands.StudentCommands.Mail import Mail
from apps.API_VK.command.commands.StudentCommands.TimeTable import TimeTable
from apps.API_VK.command.commands.StudentCommands.Week import Week
from apps.API_VK.command.commands.Uyu import Uyu
from apps.API_VK.command.commands.Weather import Weather
from apps.API_VK.command.commands.Where import Where
from apps.API_VK.command.commands.YesNo import YesNo

commands = [Thanks(), Stream(), Where(), Birds(), Register(), Petrovich(), Statistics(), Random(), Sorry(), Help(),
            Weather(), Praise(), Scold(), Quote(), Quotes(), Keyboard(), KeyboardHide(), Uyu(), Hi(), Bye(), Nya(),
            Shit(), Git(), Donate(), Issue(), Issues(), Joke(), TimeTable(), GoogleDrive(), Week(), Mail(), Ban(),
            DeBan(), Command(), Start(), Stop(), Control(), get_user_by_id(), update_users(), YesNo()]


def get_commands():
    return commands


# ToDo: сохранение
def get_help_admin_texts():
    texts = ""
    for command in commands:
        if command.for_admin:
            if command.help_text:
                texts += "{}\n".format(command.help_text)
    return texts


def get_help_student_texts():
    texts = ""
    for command in commands:
        if command.for_student:
            if command.help_text:
                texts += "{}\n".format(command.help_text)
    return texts


def get_help_moderator_texts():
    texts = ""
    for command in commands:
        if command.for_moderator:
            if command.help_text:
                texts += "{}\n".format(command.help_text)
    return texts


def get_help_texts():
    texts = ""
    for command in commands:
        if not command.for_moderator and not command.for_admin and not command.for_student:
            if command.help_text:
                texts += "{}\n".format(command.help_text)
    return texts
