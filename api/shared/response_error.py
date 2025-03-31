from inspect import stack
import traceback

from rest_framework import status

from centridesk.settings import BASE_DIR
from centribal.packages.utils.get_config import GetConfig
from centribal.packages.logger.log_manager import init_loggers


def response_error(view_obj, error, data=None, method=None):
    config = GetConfig.load_config(BASE_DIR)
    logger = init_loggers(**config.get_logs())
    error=traceback.format_exc()
    settings = config.get('settings')
    message = f"{error}" if settings.debug else 'Internal Server Error'
    method = method or stack()[1][3]
    logger.error(f"Error in response error:", extra={'data': data, 'message':message}, exc_info=True)
    return {'message': message}, status.HTTP_500_INTERNAL_SERVER_ERROR
