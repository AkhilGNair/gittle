from pathlib import Path
import hashlib
import tempfile
import zipfile

from gittle.add import read_stage
from gittle.paths import get_repo_paths


def make_hash(content, hash_length=8):
    hash = hashlib.sha1(content)
    return hash.hexdigest()[:hash_length]


def create_blob():
    """Creates a blob from the staged files."""
    repo_paths = get_repo_paths()
    store = repo_paths["store"]

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    zip = zipfile.ZipFile(temp_file.name, "w", zipfile.ZIP_DEFLATED)

    staged_files = read_stage()
    if not staged_files:
        return 0, None

    for _file in staged_files:
        zip.write(_file)

    blob_name = make_hash(Path(temp_file.name).read_bytes())
    p = Path(temp_file.name).rename(Path(store / blob_name).with_suffix(".zip"))
    return len(staged_files), p.with_suffix("").name
