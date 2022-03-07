from pathlib import Path
from typing import Optional

from gittle.paths import branches, head


def current_branch() -> str:
    return head().read_text()


def current_commit() -> Optional[str]:
    try:
        return (branches() / current_branch()).read_text()
    except FileNotFoundError:
        return None


def update(commit: str) -> None:
    Path(branches()).mkdir(parents=True, exist_ok=True)
    branch_ref = branches() / current_branch()
    branch_ref.write_text(commit)
