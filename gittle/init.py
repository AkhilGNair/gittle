from gittle.paths import get_repo_paths


def create_repo() -> bool:
    paths = get_repo_paths()
    exists = paths["gittle"].exists()

    paths["store"].mkdir(parents=True, exist_ok=True)
    paths["workspace"].mkdir(parents=True, exist_ok=True)
    paths["head"].write_text("main")

    return exists
