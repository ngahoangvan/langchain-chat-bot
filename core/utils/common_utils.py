import os
import tiktoken

from core.constants import ENGINE_DICT


def join_paths(*args):
    return os.path.join(*args)


def calculate_token(text: str) -> int:
    encoding = tiktoken.get_encoding("o200k_base")
    tokens = len(encoding.encode(text))
    return tokens


def get_async_db_uri(uri) -> str:
    for key, value in ENGINE_DICT.items():
        if uri.startswith(f'{key}://'):
            uri = uri.replace(f'{key}://', f'{value}://')
            return uri

    raise ValueError('Invalid database URI: ' + uri)
