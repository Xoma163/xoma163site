from vk_api import vk_api, VkUpload

from secrets.secrets import secrets


class VkUserClass:
    def __init__(self):
        super().__init__()
        self.id = secrets['vk']['user']['id']
        vk_session = vk_api.VkApi(secrets['vk']['user']['login'],
                                  secrets['vk']['user']['password'],
                                  auth_handler=self.auth_handler)
        vk_session.auth()
        self.upload = VkUpload(vk_session)
        self.vk = vk_session.get_api()

    @staticmethod
    def auth_handler():
        key = input("Enter authentication code: ")
        remember_device = True
        return key, remember_device