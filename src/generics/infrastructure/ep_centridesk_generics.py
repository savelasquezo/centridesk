import time

from centridesk.settings import BASE_DIR
from centribal.packages.utils.get_config import GetConfig
from centribal.packages.logger.log_manager import init_loggers
from src.actions.infrastructure.actions_mysql import ActionsMysql

from src.generics.infrastructure.ep_download_use_report import EntrypointDownloadUseReport
from src.generics.infrastructure.ep_download_users import EntrypointDownloadUsers
from src.generics.infrastructure.ep_send_ticket_transcription import EpSendTicketTranscription


class EntrypointGenerics:
    def __init__(self, message, params=None):
        self.message = message
        self.params = params

    def run(self):
        config = GetConfig.load_config(BASE_DIR)
        logger = init_loggers(**config.get_logs())
        actions_obj = ActionsMysql(self.message['account_id'], self.message['action']['unique_id'])
        try:
            # check action registry exists
            action = actions_obj.get_by_id()

            if not action:
                time.sleep(1)
                action = actions_obj.get_by_id()

            if not action:
                raise Exception('Action ID not found in db.')

            if action['result'] == 0:
                actions_obj.update_initiated()

                if self.message['action']['action'] == 'desk_download_users':
                    _ep = EntrypointDownloadUsers(
                        account_id=self.message['account_id'],
                        requester_id=self.message['requester_id'],
                        info=self.message['action']['info'],
                    )
                    _ep.run()

                elif self.message['action']['action'] == 'send_ticket_transcription':
                    _ep = EpSendTicketTranscription(
                        account_id=self.message['account_id'],
                        **self.message['action']['info'],
                    )
                    _ep.run()

                elif self.message['action']['action'] == 'desk_download_use_report':
                    _ep = EntrypointDownloadUseReport(
                        account_id=self.message['account_id'],
                        info=self.message['action']['info'],
                        requester_id=self.message['requester_id']
                    )
                    _ep.run()

                else:
                    raise Exception('Action not recognized')
            else:
                raise Exception(f'Action ID already processed: {action}')

            actions_obj.update_finished()

        except Exception as ex:
            logger.error('Error processing message from Centridesk Generics',
                    extra={
                        'account_id': self.message['account_id'],
                        'Message': self.message
                        },
                    exc_info=True)
            actions_obj.update_error(ex)
