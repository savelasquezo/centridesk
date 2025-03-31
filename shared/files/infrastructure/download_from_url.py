import urllib3


class FileFromUrl:

    def __init__(self, url=None):
        self.url = url

    def download(self):
        http = urllib3.PoolManager()
        response = http.request('GET', self.url, preload_content=False)

        return response.data if response.status == 200 else None
