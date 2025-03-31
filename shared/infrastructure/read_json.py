import json


class ReadJson:

    def __init__(self, file, path, in_object=True):
        self.file = f"{file}.json"
        self.path = path
        self.object = in_object
        self.data = self._open_file()

    def _open_file(self):
        json_path = f"{self.path}/{self.file}"

        with open(json_path) as f:
            data = json.load(f)

        return data

    def get(self, key):
        try:
            data = self.data
            key_list = key.split(".")

            for key in key_list:
                key1 = data.get(key, None)

                if key1:
                    data = key1
                else:
                    raise Exception(f"Key {key} not found.")

            if isinstance(data, dict):
                a = Struct(**data) if self.object else data
            else:
                a = data

        except Exception as ex:
            raise Exception(f"{ex}")

        return a


class Struct(object):
    def __init__(self, **entry):
        self.__dict__.update(entry)
