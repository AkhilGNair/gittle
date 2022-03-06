from pathlib import Path

from gittle.paths import branches, head


def current_branch() -> str:
    return head().read_text()


def last_commit() -> str:
    return (branches() / current_branch()).read_text()


def update(commit: str) -> None:
    Path(branches()).mkdir(parents=True, exist_ok=True)
    branch_ref = branches() / current_branch()
    branch_ref.write_text(commit)
