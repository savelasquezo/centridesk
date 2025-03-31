import time

from shared.async_queue.infrastructure.sender_centridesk_generics import AsyncSenderGeneric
from shared.exceptions.generic import GenericException
from src.actions.domain.action_in import Action
from src.actions.infrastructure.actions_mysql import ActionsMysql


class CreateAction:

    def __init__(self, action: Action, actions_obj: ActionsMysql, async_sender_obj: AsyncSenderGeneric):
        self.action = action
        self.actions_obj = actions_obj
        self.async_sender_obj = async_sender_obj

        self.__rollback_project_action = False

        self.__available_parallel_actions = ['send_ticket_transcription']

    def create(self):
        self.actions_obj.account_id = self.action.account_id
        # check pending action
        if self.action.action not in self.__available_parallel_actions:
            if self.actions_obj.get_by_pending(True):
                raise GenericException("Pending Action")

            # check in_progress action
            if self.actions_obj.get_by_in_progress(True):
                raise GenericException("Action in progress")

        try:
            # save action in database
            self.actions_obj.create(self.action)
            self.__rollback_project_action = True

            # send message to async queue
            self.async_sender_obj.message = {
                "action": self.action.data,
                "account_id": self.action.account_id,
                "requester_id": self.action.requester_id
            }

            self.async_sender_obj.send()

        except Exception as ex:
            # rollback
            try:
                if self.__rollback_project_action:
                    self.actions_obj.action_id = self.action.unique_id
                    self.actions_obj.delete_by_id()

            except Exception as err:
                raise Exception(f'Rollback: {err}')

            raise ex

        time.sleep(1)
        self.actions_obj.action_id = self.action.unique_id
        return self.actions_obj.get_by_id()
