from rest_framework import status
from rest_framework.response import Response

from api.shared import permissions
from api.shared.response_error import response_error
from shared.exceptions.generic import GenericException
from shared.exceptions.in_use import InUse
from shared.exceptions.invalid_filter import InvalidFilter
from shared.exceptions.invalid_format import InvalidFormat
from shared.exceptions.invalid_order import InvalidOrder
from shared.exceptions.invalid_sort import InvalidSort
from shared.exceptions.invalid_type import InvalidType
from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.not_found import NotFound
from shared.exceptions.required_value import RequiredValue
from shared.exceptions.too_big_number import TooBigNumber
from shared.exceptions.type_error import TypeErrorValue
from shared.exceptions.unauthorized import Unauthorized
from shared.exceptions.user_not_allowed import UserNotAllowed


def api_handler(func):
    def handler(*args, **kwargs):
        try:
            # check user permissions
            account_id = kwargs.get('account_id', None)
            requester = getattr(args[1], 'user')

            permissions.check_by_account(account_id, requester)

            # execute method
            output = func(*args, **kwargs)

            # return api response
            response = Response(output, status.HTTP_200_OK)

        except NotFound as ex:
            response = Response({'message': ex.message}, status.HTTP_404_NOT_FOUND)

        except (TypeErrorValue, InvalidFilter, InvalidValue, RequiredValue, TooBigNumber, InvalidFormat,
                InvalidType) as ex:
            response = Response({'message': ex.message}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        except (GenericException, InUse, InvalidSort, InvalidOrder) as ex:
            response = Response({'message': ex.message}, status.HTTP_400_BAD_REQUEST)

        except (UserNotAllowed,) as ex:
            response = Response({'message': ex.message}, status.HTTP_403_FORBIDDEN)

        except (Unauthorized,) as ex:
            response = Response({'message': ex.message}, status.HTTP_401_UNAUTHORIZED)

        except Exception as ex:
            data = f"- Kwargs: {kwargs}"
            if args[1].body:
                try:
                    data += f"\n- Body: {args[1].body.decode('utf-8')}"
                except:
                    data += f"\n- Body: {args[1].body}"

            output, code = response_error(args[0], ex, data, method=func.__name__)
            response = Response(output, code)

        return response

    return handler
