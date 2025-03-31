from json import dumps, loads

from urllib3 import PoolManager

from shared.infrastructure.get_config import GetConfig


class CentribotRequests:

    def __init__(self, project_id=None, channel_id=None, external_id=None, ticket_id=None, comment_id=None,
                 message=None, attachments=None, requester_id=None):
        self.__config = GetConfig()
        self.__centribot = self.__config.get('platform.centribot')
        self.project_id = project_id
        self.channel_id = channel_id
        self.external_id = external_id
        self.ticket_id = ticket_id
        self.comment_id = comment_id
        self.message = message
        self.attachments = attachments
        self.requester_id = requester_id

    def __make_request(self, method, path, data, headers=None):
        url = f"{self.__centribot.url}/{path}"

        http = PoolManager()
        response = http.request(method, url, body=dumps(data).encode('utf-8'), headers=headers)

        output = loads(response.data.decode('utf-8'))

        if response.status != 200:
            raise Exception(f"Centribot Response: \nStatus: {response.status} \nMessage: {output}")

        return output

    def send_message(self):
        path = f"api/v1/projects/{self.project_id}/desks/outgoing"

        payload = {
            "platform": self.__centribot.platform,
            "external_id": self.external_id,
            "centribot_project_id": self.project_id,
            "centribot_channel_id": self.channel_id,
            "ticket_id": self.ticket_id,
            "comment_id": self.comment_id,
            "text": self.message,
            "attachments": self.attachments,
            "requester_id": self.requester_id
        }

        self.__make_request('POST', path, payload)

    def update_solved_status(self):
        path = f"api/v1/projects/{self.project_id}/sessions/status"

        payload = {
            "platform": self.__centribot.platform,
            "external_id": self.external_id,
            "centribot_channel_id": self.channel_id,
            "ticket_id": self.ticket_id
        }

        self.__make_request('POST', path, payload)
