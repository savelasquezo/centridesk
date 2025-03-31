from src.comments.application.process_attachments import ProcessAttachments


class ProcessAttachmentsDesk(ProcessAttachments):

    def __init__(self, account_id=None, attachments=None, get_file_obj=None, bucket_obj=None, converter_obj=None,
                 files_obj=None, ticket_id=None):
        super().__init__(account_id, attachments, get_file_obj, bucket_obj, platform='desk', converter_obj=converter_obj,
                         files_obj=files_obj, ticket_id=ticket_id)

    def get_file_data(self, attachment):
        return attachment['content']

    def get_file_s3_location(self, attachment, extension=None):
        e = extension or attachment['filename'].split('.')[-1]
        return self.bucket_base_path + e
