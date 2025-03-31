from src.comments.application.process_attachments import ProcessAttachments


class ProcessAttachmentsSmooch(ProcessAttachments):

    def __init__(self, account_id=None, attachments=None, get_file_obj=None, bucket_obj=None, converter_obj=None,
                 ticket_id=None):
        super().__init__(account_id, attachments, get_file_obj, bucket_obj, platform='bot', converter_obj=converter_obj,
                         ticket_id=ticket_id)

    def get_file_data(self, attachment):
        self.get_file_obj.url = attachment['url']
        return self.get_file_obj.download()

    def get_file_s3_location(self, attachment, extension=None):
        return self.bucket_base_path + attachment['url'].split('.')[-1]
