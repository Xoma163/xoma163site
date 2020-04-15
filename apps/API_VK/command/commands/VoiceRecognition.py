from apps.API_VK.APIs.wit_ai import get_text_from_audio_file
from apps.API_VK.command.CommonCommand import CommonCommand


class VoiceRecognition(CommonCommand):
    def __init__(self):
        names = ["распознай", "голос", "голосовое"]
        super().__init__(names, fwd=True)

    def start(self):
        from apps.API_VK.VkBotClass import parse_attachments

        attachments = parse_attachments(self.vk_event.fwd[0]['attachments'])
        audio_message = None
        for attachment in attachments:
            if attachment['type'] == 'audio_message':
                audio_message = attachment
                break
        if not audio_message:
            return "Не нашел аудио в пересланных сообщениях"

        return get_text_from_audio_file(audio_message)
