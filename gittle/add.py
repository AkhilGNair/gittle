from gittle.paths import GITTLE, get_repo_paths, path_staging

NEW_LINE = "\n"


def read_stage():
    content = path_staging().read_text().strip()
    return content.split("\n") if content else []


def write_staging(files):
    stage = path_staging()
    content = NEW_LINE.join(files) + NEW_LINE
    stage.write_text(content)


def find_files():
    root = get_repo_paths()["root"]

    include = set(root.rglob("*"))
    exclude = set(root.rglob(f"{GITTLE}/**/*"))
    exclude.add(root / GITTLE)

    paths = set(include).difference(exclude)
    paths = {p.relative_to(root) for p in paths}

    return sorted(str(p) for p in paths if p.is_file())
