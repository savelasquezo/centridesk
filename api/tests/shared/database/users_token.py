from api.models.users.users_token import UsersToken
from api.tests.shared.mock_data import MockData


def create_by_centribot_user_id(mock: MockData, centribot_user_id):
    for user_token in mock.users_token:
        if user_token['centribot_user_id'] == centribot_user_id:
            __create(user_token)
            break


def create_all(mock):
    for user_token in mock.users_token:
        __create(user_token)


def __create(user_token):
    UsersToken.objects.create(
        centribot_user_id=user_token['centribot_user_id'],
        mobile_id=user_token['mobile_id'],
        key=user_token['key'],
        created_at=user_token['created_at'],
        updated_at=user_token['updated_at']
    )
