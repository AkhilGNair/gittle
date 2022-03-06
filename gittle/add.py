from typing import Set, Iterator

from gittle import paths
from gittle.commit import compute_address, read_snapshot
from gittle.references import current_commit

NEW_LINE = "\n"


def write_staging(files: Set[str]) -> None:
    stage = paths.staging()
    content = NEW_LINE.join(files) + NEW_LINE
    stage.write_text(content)


def find_files() -> Set[str]:
    root = paths.root()
    include = set(root.rglob("*"))
    exclude = set(root.rglob(f"{paths.GITTLE}/**/*"))
    exclude.add(root / paths.GITTLE)

    files = set(include).difference(exclude)
    files = {p.relative_to(root) for p in files}

    return set(sorted(str(fp) for fp in files if fp.is_file()))


def _detect_changes(files: Set[str], snapshot: Set[str]) -> Iterator[str]:
    for file in files:
        hash, _ = compute_address(file)
        if hash not in snapshot:
            yield file


def detect_changes() -> Set[str]:
    snapshot = read_snapshot(snapshot=current_commit())
    changed = set(_detect_changes(files=find_files(), snapshot=snapshot))
    return changed
