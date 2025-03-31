from os import remove

import boto3
import mimetypes

from shared.aws_bucket.infrastructure.url_files_mysql import UrlFilesMysql
from shared.infrastructure.get_config import GetConfig


class AwsBuckets:

    def __init__(self, file_type):
        self.file_type = file_type
        self.bucket_name = None
        self.bucket = self.__get_bucket()
        self.__credentials = self.__get_credentials()

    @staticmethod
    def __get_credentials():
        config = GetConfig()
        return config.get_aws_buckets()

    def __get_bucket(self):
        url_db = UrlFilesMysql(file_type=self.file_type)
        bucket = url_db.get()
        self.bucket_name = bucket['bucket_name']
        return bucket

    def __get_client(self):
        if not self.bucket_name:
            self.bucket = self.__get_bucket()

        resource = boto3.resource(
            's3',
            aws_access_key_id=self.__credentials.key_id,
            aws_secret_access_key=self.__credentials.key
        )
        return resource.Bucket(self.bucket_name)

    def create(self, filepath, content, mediatype=None):
        try:
            __client = self.__get_client()
            if not mediatype:
                mediatype, encoding = mimetypes.guess_type(filepath)

            output = __client.put_object(
                Body=content,
                Bucket=self.bucket_name,
                Key=filepath,
                ACL='public-read',
                ContentType=mediatype
            )

        except Exception as ex:
            raise Exception(f"Error creating file in bucket. \n Exception: {ex}")

        return output.key

    def upload(self, tmp_path, filepath, filename):
        try:
            __client = self.__get_client()
            __client.meta.client.upload_file(
                f'{tmp_path}/{filename}',
                self.bucket_name,
                filepath,
                ExtraArgs={'ACL': 'public-read'}
            )
        except Exception as ex:
            raise Exception(f"Error uploading file to bucket. \n Exception: {ex}")

    def delete(self, filepath):
        try:
            __client = self.__get_client()
            __client.objects.filter(Prefix=filepath).delete()

        except Exception as ex:
            raise Exception(f"Error deleting file from bucket. \n Exception: {ex}")

    def delete_by_url(self, url_file):
        parts = url_file.replace('https://', '').split('amazonaws.com/')
        self.bucket_name = parts[0].split('.')[0]
        self.delete(parts[-1])

    @staticmethod
    def delete_tmp_file(tmp_path, filename):
        remove(f'{tmp_path}/{filename}')
