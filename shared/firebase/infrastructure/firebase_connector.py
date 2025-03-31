import os

import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.exceptions import FirebaseError, NOT_FOUND, PERMISSION_DENIED

from shared.exceptions.invalid_firebase_token import InvalidFirebaseToken
from centridesk.settings import BASE_DIR
from centribal.packages.utils.get_config import GetConfig
from centribal.packages.logger.log_manager import init_loggers


class FirebaseConnector:

    def __init__(self):
        if not firebase_admin._apps:
            file = os.path.join(os.getcwd(), 'plataforma-centribal-firebase-adminsdk-f9b5k-0d0af35198.json')
            json_credentials = credentials.Certificate(file)
            firebase_admin.initialize_app(json_credentials)

    def send_create_ticket_or_comment_notification(self, token, customer_id, customer_name):
        notification = {
            'title': 'Nuevo comentario',
            'body': f'{customer_name} ha hecho un nuevo comentario'
        }
        data = {
            'customerId': customer_id,
            'customerName': customer_name
        }
        return self.__send_notification(notification, data, token)

    def send_assignee_ticket_notification(self, token, customer_id, customer_name):
        notification = {
            'title': 'Nueva conversación asignada',
            'body': f'Se le ha asignado una conversación con el usuario {customer_name}'
        }
        data = {
            'customerId': customer_id,
            'customerName': customer_name
        }
        return self.__send_notification(notification, data, token)

    @staticmethod
    def __send_notification(notification, data, user_token):
        config = GetConfig.load_config(BASE_DIR)
        logger = init_loggers(**config.get_logs())
        try:
            message = messaging.Message(
                notification=messaging.Notification(**notification),
                data=data,
                token=user_token
            )
            return messaging.send(message)

        except FirebaseError as ex:
            # NOT_FOUND(404): Requested entity not found, PERMISSION_DENIED(403): SenderIdMismatch
            if ex.code not in [NOT_FOUND, PERMISSION_DENIED]:
                logger.error('Warning: Mobile push notification not sended',
                    extra={
                        'Notification': notification,
                        'Data': data,
                        'User token':user_token,
                        'Code': ex.code
                        },
                    exc_info=True)

            raise InvalidFirebaseToken(user_token)
