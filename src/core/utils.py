import os


def create_hidden_file(file_path: str, data: str, encoding='utf-8'):
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(data)
    # TODO: Make the file ACTUALLY hidden
