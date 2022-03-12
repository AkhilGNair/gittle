from gittle.paths import Paths


BRANCH_INITIAL = "main"


def create_repo() -> bool:
    exists = Paths.gittle.exists()
    Paths.gittle.mkdir(exist_ok=True)
    Paths.store.mkdir(exist_ok=True)
    Paths.head.write_text(BRANCH_INITIAL)
    return exists
