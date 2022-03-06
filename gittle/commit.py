from typing import Tuple, Set
from pathlib import Path
import hashlib
import zlib

from gittle import paths, references, stage


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
    hashes = {store_file(file) for file in stage.read()}
    commit = store_snapshot(hashes)
    references.update(commit=commit)
    stage.clear()
    return commit


def read_snapshot(snapshot: str) -> Set[str]:
    content = (paths.store() / snapshot).read_bytes()
    return set(zlib.decompress(content).decode("utf-8").split("\n"))
