from abc import abstractmethod

from shared.files.infrastructure.file_converter import FileConverter
from shared.files.infrastructure.files import Files
from shared.infrastructure.get_uuid import get_uuid


class ProcessAttachments:

    def __init__(self, account_id, attachments, get_file_obj, bucket_obj, platform, converter_obj: FileConverter = None,
                 files_obj: Files = None, ticket_id=None):
        self.account_id = account_id
        self.attachments = attachments
        self.get_file_obj = get_file_obj
        self.bucket_obj = bucket_obj
        self.platform = platform
        self.converter_obj = converter_obj
        self.files_obj = files_obj
        self.ticket_id = ticket_id
        self.attachment_id = get_uuid()

    @property
    def bucket_base_path(self):
        return f'centridesk/{self.account_id}/ticket/{self.ticket_id}/attachments/{self.attachment_id}.'

    def process_attachments(self):
        for attachment in self.attachments.attachments:
            file_data = self.get_file_data(attachment)
            if file_data:
                file_extension = None

                if self.platform == 'desk':
                    if attachment['filetype'] in ['video', 'audio']:
                        self.files_obj.content = file_data
                        self.files_obj.filename = attachment['filename']
                        self.files_obj.create_by_bytes()

                        self.converter_obj.filepath = self.files_obj.filepath

                        has_to_convert = self.converter_obj.has_to_convert()
                        has_to_resize = self.converter_obj.has_to_resize()

                        if has_to_convert or has_to_resize:
                            if has_to_convert and not has_to_resize:
                                self.converter_obj.convert()

                            elif has_to_resize:
                                self.converter_obj.convert_and_resize()

                            self.files_obj.filepath = self.converter_obj.converted_filepath
                            file_data = self.files_obj.read_bytes()
                            self.files_obj.delete()

                            file_extension = self.converter_obj.extension

                        self.files_obj.filepath = self.converter_obj.filepath
                        self.files_obj.delete()

                else:
                    if attachment['type'] == 'file':
                        attachment['filename'] = 'document.' + attachment['url'].split('.')[-1]

                file_s3_location = self.get_file_s3_location(attachment, extension=file_extension)
                self.bucket_obj.create(file_s3_location, file_data, attachment.get('mediatype'))
                attachment['url'] = self.bucket_obj.bucket['base_url'] + file_s3_location

        return self.attachments.attachments

    @abstractmethod
    def get_file_data(self, attachment):
        pass

    @abstractmethod
    def get_file_s3_location(self, attachment, extension=None):
        pass
