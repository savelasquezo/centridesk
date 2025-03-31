from os import path

from shared.infrastructure.read_json import ReadJson


class GetConfig:

    def __init__(self):
        self.file = 'config'
        self.path = f"{path.dirname(path.abspath(__file__))}/../.."
        self.config = self._open_file()

    def _open_file(self):
        try:
            read = ReadJson(self.file, self.path)
        except Exception as ex:
            raise Exception(f"{ex}")

        return read

    def get(self, key):
        try:
            output = self.config.get(key)
        except Exception as ex:
            raise Exception(f"{ex}")

        return output

    def get_aws_buckets(self):
        return self.get('providers.aws.buckets')

    def get_rmq(self):
        return self.get('platform.rabbitmq')

    def is_kubernetes(self):
        return self.get('platform.kubernetes')
    
    def get_logs(self): 
            logs_config = self.get('logs')
            settings = {
                'log_json_format': logs_config.log_json_format,
                'log_level': logs_config.log_level,
                'env': self.get('settings.env'),
                'kubernetes': self.get('platform.kubernetes')
            }

            return {
                'app_name': self.get('settings.project'),
                'settings': settings
            }

