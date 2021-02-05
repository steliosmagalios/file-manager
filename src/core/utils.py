import os


def create_hidden_file(file_path: str, data: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)
    # TODO: Make the file ACTUALLY hidden
