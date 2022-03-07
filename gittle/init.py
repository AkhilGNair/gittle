from gittle.paths import Paths


def create_repo() -> bool:
    exists = Paths.gittle.exists()
    Paths.gittle.mkdir(exist_ok=True)
    Paths.store.mkdir(exist_ok=True)
    Paths.head.write_text("main")
    return exists
