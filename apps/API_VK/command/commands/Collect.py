from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_attachments_from_attachments_or_fwd


def parting(_list, items_count):
    return [_list[d:d + items_count] for d in range(0, len(_list), items_count)]


class Collect(CommonCommand):
    def __init__(self):
        names = ["собрать"]
        super().__init__(names, enabled=False)

    def start(self):
        attachments = get_attachments_from_attachments_or_fwd(self.vk_event, from_first_fwd=False)
        attachments = [att['vk_url'] for att in attachments]
        if len(attachments) == 0:
            return "Не нашёл вложений"
        attachments_parts = parting(attachments, 10)
        msgs = [{'attachments': attachments_part} for attachments_part in attachments_parts]
        return msgs
