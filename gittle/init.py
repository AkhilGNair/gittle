from gittle import paths


def create_repo() -> bool:
    exists = paths.gittle().exists()

    paths.store().mkdir(parents=True, exist_ok=True)
    paths.workspace().mkdir(parents=True, exist_ok=True)
    paths.head().write_text("main")

    return exists
