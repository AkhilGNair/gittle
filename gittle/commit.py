from pathlib import Path
from typing import Iterator, Set, Tuple
import hashlib
import zlib

from gittle import paths, references, stage
from gittle.references import last_commit


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
    try:
        snapshot = read_snapshot(snapshot=last_commit())
    except FileNotFoundError:
        # On the first commit, there are no previously snapshotted files.
        snapshot = set()

    changed = set(_detect_changes(files=find_files(), snapshot=snapshot))
    return changed


def make_hash(content: bytes, hash_length: int = 8) -> str:
    hash = hashlib.sha1(content)
    return hash.hexdigest()[:hash_length]


def _store(hash: str, content: bytes) -> str:
    path = paths.store() / hash
    path.write_bytes(zlib.compress(content))
    return hash


def compute_address(file: str) -> Tuple[str, bytes]:
    content = Path(file).read_bytes()
    hash = make_hash(content)
    return hash, content


def store_file(file: str) -> str:
    return _store(*compute_address(file))


def store_snapshot(hashes: Set[str]) -> str:
    content = "\n".join(hashes).encode()
    hash = make_hash(content)
    return _store(hash=hash, content=content)


def take_snapshot() -> str:
    """Creates a snapshot of the repository."""
    to_leave = set(detect_changes()).difference(stage.read())
    to_snapshot = find_files().difference(to_leave)
    hashes = {store_file(file) for file in to_snapshot}
    commit = store_snapshot(hashes)

    references.update(commit=commit)
    stage.clear()

    return commit


def read_snapshot(snapshot: str) -> Set[str]:
    content = (paths.store() / snapshot).read_bytes()
    return set(zlib.decompress(content).decode("utf-8").split("\n"))
