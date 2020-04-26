from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import random_event


class Bye(CommonCommand):
    def __init__(self):
        names = ["пока", "бай", "bb", "бай-бай", "байбай", "бб", "досвидос", "до встречи", "бывай", 'пока-пока',
                 'пока((']
        super().__init__(names)

    def start(self):
        return random_event(self.names)
