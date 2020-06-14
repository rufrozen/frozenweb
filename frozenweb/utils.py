import os


def write_binary_file(path, content):
    with open(path, "wb") as f:
        f.write(content)


def read_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_binary_file(path):
    with open(path, "rb") as f:
        return f.read()


def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def to_bytes(text):
    return bytes(text, "utf-8")
