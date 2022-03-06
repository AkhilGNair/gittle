from typing import Set

from gittle import paths


def read() -> Set[str]:
    content = paths.staging().read_text().strip()
    return set(content.split("\n")) if content else set()


def clear() -> None:
    paths.staging().write_text("")
