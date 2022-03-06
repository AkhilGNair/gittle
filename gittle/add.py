from gittle.paths import GITTLE, get_repo_paths, path_staging

NEW_LINE = "\n"


def read_lines(path):
    return path.read_text().strip().split("\n")


def write_staging(files):
    stage = path_staging()
    content = NEW_LINE.join(files) + NEW_LINE
    stage.write_text(content)


def store_empty():
    paths = get_repo_paths()
    return not bool(len(list(paths["store"].rglob("*"))))


def find_files():
    root = get_repo_paths()["root"]

    include = set(root.rglob("*"))
    exclude = set(root.rglob(f"{GITTLE}/*"))
    exclude.add(root / GITTLE)

    paths = set(include).difference(exclude)
    paths = {p.relative_to(root) for p in paths}

    return sorted(str(p) for p in paths if p.is_file())
