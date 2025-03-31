from os import path as os_path
from os import remove


class Files:

    def __init__(self, content=None, filename=None, path=None, filepath=None):
        self.content = content
        self.filename = filename
        self.path = path or '/tmp'
        self.filepath = filepath

    @property
    def filepath(self):
        return self.__filepath or os_path.join(self.path, self.filename)

    @filepath.setter
    def filepath(self, value):
        self.__filepath = value

    def create(self, mode='w'):
        with open(self.filepath, mode) as f:
            f.write(self.content)
            f.close()

    def read(self, mode='r'):
        with open(self.filepath, mode) as f:
            content = f.read()
            f.close()

        return content

    def create_by_bytes(self):
        self.create('wb')

    def read_bytes(self):
        return self.read('rb')

    def delete(self):
        remove(self.filepath)
