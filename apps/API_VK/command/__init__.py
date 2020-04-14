import importlib
import os
import pkgutil


def import_all_commands():
    from xoma163site.settings import BASE_DIR

    BASE_COMMANDS_FOLDER_DIR = f"{BASE_DIR}/apps/API_VK/command/commands"
    COMMANDS_DIRS = []
    for path in os.walk(BASE_COMMANDS_FOLDER_DIR):
        if not path[0].endswith('__pycache__'):
            COMMANDS_DIRS.append(path[0])

    for (module_loader, name, ispkg) in pkgutil.iter_modules(COMMANDS_DIRS):
        package = module_loader.path.replace(BASE_DIR, '')[1:].replace('/', '.')
        importlib.import_module('.' + name, package)


def generate_commands():
    from apps.API_VK.command.CommonCommand import CommonCommand
    _commands = [cls() for cls in CommonCommand.__subclasses__()]

    for command in _commands:
        if not command.enabled:
            _commands.remove(command)
    _commands.sort(key=lambda x: x.priority, reverse=True)
    return _commands


import_all_commands()

commands = generate_commands()


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
    from django.contrib.auth.models import Group

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
                    if command.enabled:
                        help_text_list[text['for']].append(text['text'])
                        if command.api is None or command.api:
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
