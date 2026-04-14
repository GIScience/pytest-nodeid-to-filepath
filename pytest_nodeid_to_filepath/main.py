import os
import re
import zlib
from pathlib import Path

ROOT_DIR: Path | None = None
DIRECTORY: str = ""
MAX_PARAM_LEN = 40
FILENAMES: list[str] = []  # keep track of duplicated filenames


def get_filepath(
    extension: str = "",
    directory: str | Path = "",
) -> Path:
    """Get a filepath based on the current Pytest node ID.

    The node ID of the current test is read from the environment variable
    PYTEST_CURRENT_TEST and transformed to a string which can be used safely
    as filename on any OS.

    Optionally the directory argument can be given to resolve the path against
    this directory. The directory needs to be relative to Pytest root.
    """
    if isinstance(directory, str) and directory != "":
        directory = Path(directory)
    elif DIRECTORY:
        directory = Path(DIRECTORY)

    # TODO: Try out with xdist
    node_id = os.environ["PYTEST_CURRENT_TEST"]

    if "[" in node_id and "]" in node_id:
        start = node_id.index("[") + 1
        end = node_id.rindex("]")
        params = node_id[start:end]
        pattern = "^[A-Za-z0-9_-]*$"  # letters, numbers, underscores and dashes
        if re.match(pattern, params) is not None and len(params) <= MAX_PARAM_LEN:
            hash_ = params
        else:
            hash_ = str(zlib.crc32(params.encode("utf-8")))
    else:
        params = ""
        hash_ = ""

    filepath = Path(
        node_id.replace(" (call)", "")
        .replace(" (setup)", "")
        .replace(" (teardown)", "")
        .replace("::", "--")
        .replace(params, hash_)
    )

    if isinstance(directory, Path):
        filepath = mirror_path_to_directory(filepath, directory)

    if ROOT_DIR is None:
        raise ValueError()
    else:
        filepath = ROOT_DIR / directory / filepath

    count_ = count(filepath.name + extension)  # With extension but without count
    return filepath.parent / (filepath.name + count_ + extension)


def mirror_path_to_directory(filepath: Path, directory: Path) -> Path:
    """Find common parents between given dir and file pathA and remove them.

    Both paths are expected to be relative to pytest root.
    """
    filepath = Path(filepath)
    for i, part in enumerate(directory.parts):
        if part == filepath.parts[i]:
            continue
        else:
            break
    else:
        i = 0
    return Path(*filepath.parts[i:])


def count(file_path: str) -> str:
    """Count generated names which are the same.

    This means a filename has been requested multiple times in one test function.
    """
    FILENAMES.append(file_path)
    count = FILENAMES.count(file_path)
    if count == 1:
        return ""
    else:
        return "." + str(count)
