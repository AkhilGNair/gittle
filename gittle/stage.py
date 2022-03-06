from typing import Set

from gittle import paths

NEW_LINE = "\n"


def write(files: Set[str]) -> None:
    stage = paths.staging()
    content = NEW_LINE.join(files) + NEW_LINE
    stage.write_text(content)


def read() -> Set[str]:
    content = paths.staging().read_text().strip()
    return set(content.split(NEW_LINE)) if content else set()


def clear() -> None:
    paths.staging().write_text("")
