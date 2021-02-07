"""Tests for revisionary."""

from dataclasses import dataclass
from typing import Optional, Iterable

import pytest

import revisionary


@pytest.fixture
def repo(tmp_path) -> revisionary.Repository:
    repo = revisionary.Repository(tmp_path)
    repo._run(["git", "init"])
    return repo


@dataclass(frozen=True)
class Commit:
    msg: str = "good commit message"
    tag: Optional[str] = None


def create_commits(repo: revisionary.Repository, commits: Iterable[Commit]) -> None:
    for commit in commits:
        repo._run(["git", "commit", "-m", commit.msg, "--allow-empty"])
        if commit.tag:
            repo._run(["git", "tag", commit.tag])


@pytest.mark.parametrize(
    "commits,expected_tags",
    [
        ([Commit(tag="0.0.0")], ["0.0.0"]),
        ([Commit(tag="0.0.1"), Commit(tag="1.0.1"), Commit(tag="0.1.2")], ["1.0.1", "0.1.2", "0.0.1"]),
        ([Commit(), Commit(tag="0.0.1"), Commit()], ["0.0.1"]),
        ([Commit(tag="1.2.3"), Commit(msg="fish")], ["1.2.3"]),
    ]
)
def test_get_tags(repo, commits, expected_tags):
    """We can get tags from the repo, sorted by version, latest first."""
    create_commits(repo, commits)
    tags = repo.get_tags()
    assert tags == expected_tags


def test_repo_is_dirty(repo):
    """We can detect when the repo is dirty."""
    uncommitted_file = repo.path / "some_file"
    uncommitted_file.touch()

    assert repo.is_dirty() is True


def test_repo_is_clean(repo):
    """We can detect when the repo is clean."""
    assert repo.is_dirty() is False


@pytest.mark.parametrize(
    "commits,tag,expected_result",
    [
        ([Commit(tag="0.0.0")], "0.0.0", 0),
        ([Commit(tag="0.0.0"), Commit()], "0.0.0", 1),
        ([Commit(), Commit(tag="0.0.1")], "0.0.1", 0),
        ([Commit(tag="1.0.1"), Commit(), Commit()], "1.0.1", 2),
        ([Commit(tag="1.0.1"), Commit(), Commit(tag="1.1.1")], "1.0.1", 2),
    ]
)
def test_get_commits_since(repo, commits, tag, expected_result):
    """We can get number of commits since version tag."""
    create_commits(repo, commits)
    assert repo.get_commits_since(tag) == expected_result
