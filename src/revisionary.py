#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
from packaging.version import Version, InvalidVersion
from typing import Union


class Repository:
    """
    Git repository.

    :path: Path to the root of an existing git repository

    """

    def __init__(self, path: Union[str, Path] = os.curdir):
        self.path = Path(path)

    def _run(self, cmd: list) -> str:
        return subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=self.path).stdout

    def get_tags(self) -> list:
        if output := self._run(["git", "tag", "--sort=-version:refname", "--merged"]):
            return output.splitlines()
        return []

    def is_dirty(self) -> bool:
        output = self._run(["git", "status", "--short"])
        return bool(output)

    def get_commits_since(self, commitish: str) -> int:
        output = self._run(["git", "rev-list", "--count", f"{commitish}..HEAD"])
        return int(output.strip())

    def get_sha(self) -> str:
        output = self._run(["git", "rev-parse", "--short", "HEAD"])
        return output.strip()

    def __repr__(self):
        return f"Repository(path='{self.path}')"


def is_valid(version: str) -> bool:
    try:
        _ = Version(version)
    except InvalidVersion:
        return False
    return True


def get_version(repo: Repository) -> str:
    """Get the latest version string from the repo."""
    tags =  repo.get_tags()

    if not tags:
        raise RuntimeError("No tags found in the repo.")

    tag = tags[0]

    if not is_valid(tag):
        raise RuntimeError("Latest version tag is not pep440 compatible")

    dev = ""
    if commits_since := repo.get_commits_since(tag):
        dev = f".dev{commits_since}+git.{repo.get_sha()}"

    dirty = ""
    if repo.is_dirty():
        dirty = ".dirty"

    version_string = f"{tag}{dev}{dirty}"
    return version_string


if __name__ == '__main__':
    repo = Repository()
    version = get_version(repo)
    assert is_valid(version)
    print(version)
