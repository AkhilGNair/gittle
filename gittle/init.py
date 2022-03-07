from gittle import paths


def create_repo() -> bool:
    exists = paths.gittle().exists()
    paths.gittle().mkdir(exist_ok=True)
    paths.store().mkdir(exist_ok=True)
    paths.head().write_text("main")
    return exists
