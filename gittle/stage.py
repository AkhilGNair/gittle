from typing import Set

from gittle.paths import Paths

NEW_LINE = "\n"


def write(files: Set[str]) -> None:
    content = NEW_LINE.join(files) + NEW_LINE
    Paths.staging.write_text(content)


def read() -> Set[str]:
    content = Paths.staging.read_text().strip()
    return set(content.split(NEW_LINE)) if content else set()


def clear() -> None:
    Paths.staging.write_text("")
