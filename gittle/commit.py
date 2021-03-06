from typing import Iterator, Optional, Set, Tuple
import hashlib
import json
import zlib

from gittle import references, stage
from gittle.paths import Paths, GITTLE

EMPTY_SNAPSHOT = dict(content="")


def find_files() -> Set[str]:
    root = Paths.root
    include = set(root.rglob("*"))
    exclude = set(root.rglob(f"{GITTLE}/**/*"))
    exclude.add(root / GITTLE)

    paths = set(include).difference(exclude)
    files = {str(p.relative_to(root)) for p in paths if p.is_file()}

    # Sorted for visual ordering in CLI
    return set(sorted(files))


def _detect_changes(files: Set[str], snapshot: Set[str]) -> Iterator[str]:
    for file in files:
        hash, _ = content_address(file)
        if hash not in snapshot:
            yield file


def detect_changes() -> Set[str]:
    snapshot = read_snapshot(commit=references.current_commit())
    changed = set(_detect_changes(files=find_files(), snapshot=snapshot["content"]))
    return changed


def make_hash(content: bytes, hash_length: int = 8) -> str:
    hash = hashlib.sha1(content)
    return hash.hexdigest()[:hash_length]


def _store(hash: str, blob: bytes) -> str:
    path = Paths.store / hash
    path.write_bytes(zlib.compress(blob))
    return hash


def content_address(file: str) -> Tuple[str, bytes]:
    content = (Paths.root / file).read_text()
    blob = as_blob({"file": file, "content": content})
    hash = make_hash(blob)
    return hash, blob


def store_file(file: str) -> str:
    return _store(*content_address(file))


def as_blob(details: dict) -> bytes:
    return json.dumps(details).encode()


def store_snapshot(hashes: Set[str], parents=Set[str]) -> str:
    content = sorted(list(hashes))
    parents = sorted(list(parents))
    blob = as_blob({"parents": parents, "content": content})
    hash = make_hash(blob)
    return _store(hash=hash, blob=blob)


def take_snapshot() -> str:
    """Creates a snapshot of the repository."""
    not_staged = set(detect_changes()).difference(stage.read())
    updated = find_files().difference(not_staged)

    hashes = {store_file(file) for file in updated}
    parent = references.current_commit()

    commit = store_snapshot(hashes=hashes, parents=[parent] if parent is not None else [])
    references.update(commit=commit)
    stage.clear()

    return commit


def read_blob(commit) -> dict:
    content = (Paths.store / commit).read_bytes()
    return json.loads(zlib.decompress(content).decode("utf-8"))


def read_snapshot(commit: Optional[str]) -> dict:
    # On the first commit, there is no previous snapshot
    return read_blob(commit) if commit is not None else EMPTY_SNAPSHOT
