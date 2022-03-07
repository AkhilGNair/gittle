from typing import Optional

from gittle.paths import Paths


class MissingGittleFile(Exception):
    pass


def current_branch() -> str:
    try:
        return Paths.head.read_text()
    except FileNotFoundError:
        raise MissingGittleFile("The HEAD file is missing")


def current_commit() -> Optional[str]:
    try:
        return (Paths.branches / current_branch()).read_text()
    except FileNotFoundError:
        return None


def update(commit: str) -> None:
    Paths.branches.mkdir(parents=True, exist_ok=True)
    branch_ref = Paths.branches / current_branch()
    branch_ref.write_text(commit)
