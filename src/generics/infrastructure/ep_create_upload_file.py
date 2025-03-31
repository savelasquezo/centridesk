from shared.aws_bucket.infrastructure.buckets import AwsBuckets
from shared.aws_bucket.infrastructure.url_files_mysql import UrlFilesMysql
from shared.email.infrastructure.mail_sender import MailSender
from shared.files.infrastructure.create_excel_file import CreateExcelFile
from shared.infrastructure.timestamps import get_timestamp


class EntrypointCreateUploadFile:

    def __init__(self, dataframe, file_name, file_type, superadmin, mail_template, requester_id=None, send_email=True,
                 extra_path=None):
        self.dataframe = dataframe
        self.file_name = file_name
        self.file_type = file_type

        self.superadmin = superadmin
        self.requester_id = requester_id

        self.mail_template = mail_template
        self.send_email = send_email
        self.extra_path = extra_path

    def run(self):
        # Create excel file
        excel_file_obj = CreateExcelFile(
            info=self.dataframe,
            file_name=self.file_name,
            lang=self.superadmin['lang'],
        )
        excel_file_obj.create()

        # Upload excel file to bucket s3
        urls_mysql = UrlFilesMysql(
            file_type=self.file_type
        )
        bucket_info = urls_mysql.get()

        bucket = AwsBuckets(self.file_type)
        bucket.upload(
            tmp_path=excel_file_obj.path,
            filename=excel_file_obj.file_name,
            filepath=f'{self.extra_path}/{excel_file_obj.file_name}'
        )

        # remove tmp file
        excel_file_obj.delete()

        # save url in table to delete passed 24h
        file_url = f"{bucket_info['base_url']}{self.extra_path}/{excel_file_obj.file_name}"
        urls_mysql.save_conversation_url(file_url, get_timestamp())

        # Send file by email
        if self.send_email:
            mail_sender = MailSender(
                requester_id=self.requester_id,
                superadmin=self.superadmin,
                template=self.mail_template,
                params={'url': file_url}
            )
            mail_sender.send()
