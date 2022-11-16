from __future__ import annotations

from pathlib import Path
from typing import Sequence

import copier
import pytest

PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture
def base_answers():
    return {
        "full_name": "Jeanne Deau",
        "email": "jeanne.deau@example.fr",
        "github_username": "jdeau",
        "project_name": "Snake Farm",
        "project_short_description": "A sample Snake farming project.",
        "version": "0.0.1",
        "open_source_license": "MIT",
        "documentation": True,
        "run_poetry_install": False,
        "initial_commit": False,
        "setup_github": False,
        "setup_pre_commit": False,
        "add_me_as_contributor": False,
    }


def _check_file_contains(
    file_path: Path,
    expected_strs: Sequence[str],
    unexpect_strs: Sequence[str] = (),
):
    assert file_path.exists()
    file_content = file_path.read_text()
    for content in expected_strs:
        assert content in file_content
    for content in unexpect_strs:
        assert content not in file_content


def test_defaults_values(
    tmp_path: Path,
    base_answers: dict[str, str | bool],
):
    dst_path = tmp_path / "snake-farm"
    worker = copier.run_auto(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data=base_answers,
        defaults=True,
    )
    assert worker is not None
    assert tmp_path.exists()
    _check_file_contains(
        dst_path / "README.md",
        ["# Snake Farm"],
    )
    _check_file_contains(
        dst_path / "pyproject.toml",
        [
            'name = "snake-farm"',
            'version = "0.0.1"',
            'license = "MIT"',
        ],
    )


@pytest.mark.parametrize(
    ("license", "expect_exists", "expected_strs", "unexpected_strs"),
    [
        (
            "MIT",
            True,
            ["MIT License"],
            ["Apache License", "GNU GENERAL PUBLIC LICENSE"],
        ),
        (
            "Apache Software License 2.0",
            True,
            ["Apache License"],
            ["MIT License", "GNU GENERAL PUBLIC LICENSE"],
        ),
        (
            "GNU General Public License v3",
            True,
            ["GNU GENERAL PUBLIC LICENSE"],
            ["MIT License", "Apache License"],
        ),
        (
            "Not open source",
            False,
            [],
            [],
        ),
    ],
)
def test_licenses(
    tmp_path: Path,
    base_answers: dict[str, str | bool],
    license: str,
    expect_exists: bool,
    expected_strs: list[str],
    unexpected_strs: list[str],
):
    dst_path = tmp_path / "snake-farm"
    copier.run_auto(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**base_answers, "open_source_license": license},
        defaults=True,
    )

    assert tmp_path.exists()
    license_file = dst_path / "LICENSE"
    if expect_exists:
        _check_file_contains(
            license_file,
            expected_strs=expected_strs,
            unexpect_strs=unexpected_strs,
        )
    else:
        assert not license_file.exists()
