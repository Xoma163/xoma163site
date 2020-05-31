from wakeonlan import send_magic_packet

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.service.models import WakeOnLanUserData


class WOL(CommonCommand):
    def __init__(self):
        names = ["пробуди", 'wol', 'wakeonlan']
        help_text = "Пробуди - пробуждает ваше устройство"
        detail_help_text = "Пробуди - пробуждает ваше устройство\n" \
                           "Пробуди (название) - пробуждает ваше устройство\n" \
                           "Для того, чтобы я добавил ваше устройство в базу - сообщите админу данные устройства"
        super().__init__(names, help_text, detail_help_text, access=Role.TRUSTED)

    def start(self):
        wol_data = WakeOnLanUserData.objects.filter(user=self.vk_event.sender)

        if self.vk_event.args:
            device_name = " ".join(self.vk_event.args)
            wol_data = wol_data.filter(name__icontains=device_name)
        if not wol_data:
            return "Не нашёл устройства для пробуждения. Напишите админу, чтобы добавить"
        if wol_data.count() > 1:
            wol_data_str = "\n".join([x.name for x in wol_data])
            msg = "Нашел несколько устройств. Уточните какое:\n" \
                  f"{wol_data_str}"
            return msg
        else:
            wol_data = wol_data.first()
        send_magic_packet(wol_data.mac, ip_address=wol_data.ip, port=wol_data.port)
        return "Отправил"
