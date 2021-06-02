from pathlib import Path


def join_relative_path(path: Path, rel_path: str) -> Path:
    for node in rel_path.split('/'):
        path /= node
    return path
