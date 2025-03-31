class AwsBuckets:

    def __init__(self, file_type, filepath=None, filename=None, content=None):
        self.file_type = file_type
        self.bucket_name = None
        self.bucket = {
            "base_url": "https://s3bucketurl.com/"
        }

    def create(self, filepath, content, mediatype=None):
        pass

    def upload(self, tmp_path, filepath, filename):
        pass

    def delete(self, filepath):
        pass

    def delete_by_url(self, url_file):
        pass