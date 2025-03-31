from django.test import SimpleTestCase

from shared.exceptions.generic import GenericException
from shared.infrastructure.timestamps import from_timestamp_to_date
from src.actions.application.create import CreateAction
from src.actions.domain.action_in import Action
from tests.shared.mock.data import MockData
from tests.shared.mock.infrastructure.actions_mysql import ActionsMysql
from tests.shared.mock.infrastructure.rabbit_sender_centridesk_generics import RabbitMQCentrideskGenericsSender


class TestCreateAction(SimpleTestCase):

    def setUp(self) -> None:
        self.mock = MockData()

    def test_create_ok(self):
        action = Action(
            action="desk_download_users",
            info={"name": "lala"},
            account_id=self.mock.account_id1,
            requester_id=self.mock.user_id1
        )

        app = CreateAction(action, ActionsMysql(mock=self.mock), RabbitMQCentrideskGenericsSender())

        expected_output = {
            "id": action.unique_id,
            "action": action.action,
            "pending": True,
            "in_progress": False,
            "requester_id": self.mock.user_id1,
            "info": {"filter": {"name": "lala"}},
            "result": 0,
            "error": None,
            "created_at": from_timestamp_to_date(action.created_at),
            "initiated_at": None,
            "finished_at": None
        }

        self.assertEqual(app.create(), expected_output)

    def test_action_pending(self):
        action = Action(
            action="desk_download_users",
            info={"name": "lala"},
            account_id=self.mock.account_id3,
            requester_id=self.mock.user_id1
        )
        try:
            app = CreateAction(action, ActionsMysql(mock=self.mock), RabbitMQCentrideskGenericsSender())
            app.create()
        except GenericException as ex:
            self.assertEqual(ex.message, "Pending Action")

    def test_action_in_progress(self):
        action = Action(
            action="desk_download_users",
            info={"name": "lala"},
            account_id=self.mock.account_id2,
            requester_id=self.mock.user_id1
        )
        try:
            app = CreateAction(action, ActionsMysql(mock=self.mock), RabbitMQCentrideskGenericsSender())
            app.create()
        except GenericException as ex:
            self.assertEqual(ex.message, "Action in progress")

    def test_create_ok(self):
        action = Action(
            action="desk_download_use_report",
            info={
		        "from_date": "2023-08-01",
		        "to_date": "2023-08-16"
	        },
            account_id=self.mock.account_id1,
            requester_id=self.mock.user_id1
        )

        app = CreateAction(action, ActionsMysql(mock=self.mock), RabbitMQCentrideskGenericsSender())
        
        expected_output = {
            "id": action.unique_id,
            "action": action.action,
            "pending": True,
            "in_progress": False,
            "requester_id": self.mock.user_id1,
            "info": {"from": "2023-08-01","to": "2023-08-16"},
            "result": 0,
            "error": None,
            "created_at": from_timestamp_to_date(action.created_at),
            "initiated_at": None,
            "finished_at": None
        }

        self.assertEqual(app.create(), expected_output)
    
    def test_action_in_progress(self):
        action = Action(
            action="desk_download_use_report",
            info={
		        "from_date": "2023-08-01",
		        "to_date": "2023-08-16"
	        },
            account_id=self.mock.account_id2,
            requester_id=self.mock.user_id1
        )
        try:
            app = CreateAction(action, ActionsMysql(mock=self.mock), RabbitMQCentrideskGenericsSender())
            app.create()
        except GenericException as ex:
            self.assertEqual(ex.message, "Action in progress")

    def test_action_in_progress(self):
        action = Action(
            action="desk_download_use_report",
            info={
		        "from_date": "2023-08-01",
		        "to_date": "2023-08-16"
	        },
            account_id=self.mock.account_id2,
            requester_id=self.mock.user_id1
        )
        try:
            app = CreateAction(action, ActionsMysql(mock=self.mock), RabbitMQCentrideskGenericsSender())
            app.create()
        except GenericException as ex:
            self.assertEqual(ex.message, "Action in progress")
