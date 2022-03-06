from gittle import paths


def read():
    content = paths.staging().read_text().strip()
    return content.split("\n") if content else []


def clear():
    paths.staging().write_text("")
