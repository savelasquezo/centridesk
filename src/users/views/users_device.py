from json import loads

from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from shared.exceptions.generic import GenericException
from shared.infrastructure.b64 import encode_obj
from src.auth.infrastructure.users_token_orm import UsersTokenOrm
from src.users.application.delete_device_by_token import DeleteUserDeviceByKey
from src.users.domain.users_device_edit_in import UsersDeviceEditIn


class UsersDevice(APIView):
    permission_classes = [PermissionsStaticUserToken]

    @api_handler
    def put(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))

        mobile_id = data.get('mobile_id', None)

        if not mobile_id:
            GenericException('Mobile id has an invalid value')

        user_device = UsersDeviceEditIn(mobile_id)

        token = request.headers['Authentication'].split(' ')[1]

        users_token_obj = UsersTokenOrm(key=token)
        user = users_token_obj.get_by_key()
        mobile_ids = user.get('mobile_id')

        if not mobile_ids:
            users_token_obj.mobile_id = encode_obj([user_device.mobile_id])

        else:
            mobile_ids.append(user_device.mobile_id)
            users_token_obj.mobile_id = encode_obj(list(set(mobile_ids)))

        users_token_obj.updated_at = user_device.timestamp_at
        users_token_obj.update_mobile_id_by_key()

        return {'message': 'success'}

    @api_handler
    def delete(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))
        user_device = UsersDeviceEditIn(data.get('mobile_id', None))

        token = request.headers['Authentication'].split(' ')[1]

        delete_device_app = DeleteUserDeviceByKey(
            key=token,
            user_device=user_device,
            userstoken_obj=UsersTokenOrm()
        )
        delete_device_app.delete()

        return {'message': 'success'}
