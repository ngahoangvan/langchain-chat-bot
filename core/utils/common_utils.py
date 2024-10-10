import os
import tiktoken

def join_paths(*args):
    return os.path.join(*args)


def calculate_token(text: str) -> int:
    encoding = tiktoken.get_encoding("o200k_base")
    tokens = len(encoding.encode(text))
    return tokens
