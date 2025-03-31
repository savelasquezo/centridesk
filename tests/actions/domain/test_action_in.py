import unittest

from shared.exceptions.empty_object import EmptyObject
from shared.exceptions.invalid_type import InvalidType
from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.required_value import RequiredValue
from shared.infrastructure.b64 import encode_obj
from src.actions.domain.action_in import Action
from tests.shared.mock.data import MockData


class TestActionIn(unittest.TestCase):

    def setUp(self) -> None:
        self.mock = MockData()

    def test_desk_download_users_ok(self):
        action = Action(
            action='desk_download_users',
            account_id='c92a905edd7b422b93654e265fb3f895',
            info={"name": "lala"},
            requester_id=self.mock.user_id1
        )

        self.assertEqual(action.action, 'desk_download_users')
        self.assertEqual(action.account_id, 'c92a905edd7b422b93654e265fb3f895')
        self.assertEqual(action.info, {"filter": {'name': 'lala'}})
        self.assertEqual(action.info_encoded, encode_obj({"filter": {'name': 'lala'}}))
        self.assertEqual(action.requester_id, self.mock.user_id1)
        self.assertEqual(action.data, {
            'unique_id': action.unique_id,
            'action': 'desk_download_users',
            'account_id': 'c92a905edd7b422b93654e265fb3f895',
            'requester_id': self.mock.user_id1,
            'info': {"filter": {'name': 'lala'}},
            'result': 0,
            'pending': True,
            'in_progress': False,
            'created_at': action.created_at
        })

    def test_invalid_type_action(self):
        try:
            Action(
                action=1,
                account_id='c92a905edd7b422b93654e265fb3f895',
                info={"name": "lala"},
                requester_id=self.mock.user_id1
            )

        except InvalidType as ex:
            self.assertEqual(ex.message, 'Action has an invalid type.')

    def test_empty_action(self):
        try:
            Action(
                action=' ',
                account_id='c92a905edd7b422b93654e265fb3f895',
                info={"name": "lala"},
                requester_id=self.mock.user_id1
            )

        except RequiredValue as ex:
            self.assertEqual(ex.message, 'Action is required')

    def test_invalid_value_action(self):
        try:
            Action(
                action='invalid_action',
                account_id='c92a905edd7b422b93654e265fb3f895',
                info={"name": "lala"},
                requester_id=self.mock.user_id1
            )

        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Action has an invalid value.')

    def test_invalid_type_account_id(self):
        try:
            Action(
                action='desk_download_users',
                account_id=1,
                info={"name": "lala"},
                requester_id=self.mock.user_id1
            )

        except InvalidType as ex:
            self.assertEqual(ex.message, 'Account id has an invalid type.')

    def test_empty_account_id(self):
        try:
            Action(
                action='desk_download_users',
                account_id=' ',
                info={"name": "lala"},
                requester_id=self.mock.user_id1
            )

        except EmptyObject as ex:
            self.assertEqual(ex.message, 'Account id can not be empty.')

    def test_empty_info(self):
        try:
            Action(
                action='desk_download_users',
                account_id='c92a905edd7b422b93654e265fb3f895',
                info=None,
                requester_id=self.mock.user_id1
            )

        except RequiredValue as ex:
            self.assertEqual(ex.message, 'Info is required')

    def test_invalid_value_info(self):
        try:
            Action(
                action='desk_download_users',
                account_id='c92a905edd7b422b93654e265fb3f895',
                info=1,
                requester_id=self.mock.user_id1
            )

        except InvalidType as ex:
            self.assertEqual(ex.message, 'Info has an invalid type.')

    def test_invalid_type_requester_id(self):
        try:
            Action(
                action='desk_download_users',
                account_id='c92a905edd7b422b93654e265fb3f895',
                info={"name": "lala"},
                requester_id=1
            )

        except InvalidType as ex:
            self.assertEqual(ex.message, 'Requester id has an invalid type.')

    def test_empty_requester_id(self):
        try:
            Action(
                action='desk_download_users',
                account_id='c92a905edd7b422b93654e265fb3f895',
                info={"name": "lala"},
                requester_id=' '
            )

        except EmptyObject as ex:
            self.assertEqual(ex.message, 'Requester id can not be empty.')

    def test_desk_download_use_report_ok(self):
        action = Action(
            action='desk_download_use_report',
            account_id='c92a905edd7b422b93654e265fb3f895',
            info={
		        "from_date": "2023-08-01",
		        "to_date": "2023-08-16"
	        },
            requester_id=self.mock.user_id1
        )
        self.assertEqual(action.action, 'desk_download_use_report')
        self.assertEqual(action.account_id, 'c92a905edd7b422b93654e265fb3f895')
        self.assertEqual(action.info, {"from": "2023-08-01","to": "2023-08-16"})
        self.assertEqual(action.info_encoded, encode_obj({'from': '2023-08-01', 'to': '2023-08-16'}))
        self.assertEqual(action.requester_id, self.mock.user_id1)
        
    
    def test_invalid_type_account_id(self):
        try:
            Action(
                action='desk_download_use_report',
                account_id=1,
                info={
		            "from_date": "2023-08-01",
		            "to_date": "2023-08-16"
	            },
                requester_id=self.mock.user_id1
            )

        except InvalidType as ex:
            self.assertEqual(ex.message, 'Account id has an invalid type.')

    def test_empty_account_id(self):
        try:
            Action(
                action='desk_download_use_report',
                account_id=' ',
                info={
		            "from_date": "2023-08-01",
		            "to_date": "2023-08-16"
	            },
                requester_id=self.mock.user_id1
            )

        except EmptyObject as ex:
            self.assertEqual(ex.message, 'Account id can not be empty.')
    
    def test_empty_info(self):
        try:
            Action(
                action='desk_download_use_report',
                account_id='c92a905edd7b422b93654e265fb3f895',
                info=None,
                requester_id=self.mock.user_id1
            )

        except RequiredValue as ex:
            self.assertEqual(ex.message, 'Info is required')

    def test_invalid_value_info(self):
        try:
            Action(
                action='desk_download_use_report',
                account_id='c92a905edd7b422b93654e265fb3f895',
                info=1,
                requester_id=self.mock.user_id1
            )

        except InvalidType as ex:
            self.assertEqual(ex.message, 'Info has an invalid type.')

    def test_invalid_type_requester_id(self):
        try:
            Action(
                action='desk_download_use_report',
                account_id='c92a905edd7b422b93654e265fb3f895',
                info={
		            "from_date": "2023-08-01",
		            "to_date": "2023-08-16"
	            },
                requester_id=1
            )

        except InvalidType as ex:
            self.assertEqual(ex.message, 'Requester id has an invalid type.')
    
    def test_empty_requester_id(self):
        try:
            Action(
                action='desk_download_use_report',
                account_id='c92a905edd7b422b93654e265fb3f895',
                info={
		            "from_date": "2023-08-01",
		            "to_date": "2023-08-16"
	            },
                requester_id=' '
            )

        except EmptyObject as ex:
            self.assertEqual(ex.message, 'Requester id can not be empty.')
