from base64 import b64encode, b64decode
from json import dumps, loads


def encode_obj(text):
    return b64encode(bytes(dumps(text), 'utf-8')).decode() if text is not None else text


def decode_obj(text):
    return loads(b64decode(text).decode('utf-8')) if text else text


def encode_text(text):
    return b64encode(bytes(text, 'utf-8')).decode() if text else text


def decode_text(text):
    return b64decode(text.decode('utf-8')) if text else text
