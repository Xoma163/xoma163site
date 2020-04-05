from apps.API_VK.command.CommonCommand import CommonCommand


class Test(CommonCommand):
    def __init__(self):
        names = ["test"]
        super().__init__(names, access='admin')

    def start(self):
        attachments = []
        attachments.append("audio371745455_456519050")
        return {"msg": "test", "attachments": attachments}
