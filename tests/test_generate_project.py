from __future__ import annotations

import re
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


def _check_file_contents(
    file_path: Path,
    expected_strs: Sequence[str] = (),
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
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data=base_answers,
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert tmp_path.exists()
    _check_file_contents(
        dst_path / "README.md",
        ["# Snake Farm"],
    )
    _check_file_contents(
        dst_path / "pyproject.toml",
        [
            'name = "snake-farm"',
            'version = "0.0.0"',
            'license = "MIT"',
        ],
    )
    upgrade_path = dst_path / ".github" / "workflows" / "poetry-upgrade.yml"
    assert upgrade_path.exists()
    content = upgrade_path.read_text()
    found = False
    for line in content.split("\n"):
        if "cron:" in line:
            found = True
            cron_expression = re.search(r"\d+ \d+ \d+ \* \*", line)
            assert cron_expression, f"Invalid cron expression: {line}"
    assert found, f"No cron expression in {content}"


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
    copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**base_answers, "open_source_license": license},
        defaults=True,
        unsafe=True,
    )

    assert tmp_path.exists()
    license_file = dst_path / "LICENSE"
    if expect_exists:
        _check_file_contents(
            license_file,
            expected_strs=expected_strs,
            unexpect_strs=unexpected_strs,
        )
    else:
        assert not license_file.exists()


@pytest.mark.parametrize("generate_doc", [True, False])
def test_documentation(
    tmp_path: Path,
    base_answers: dict[str, str | bool],
    generate_doc: bool,
):
    dst_path = tmp_path / "snake-farm"
    copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**base_answers, "documentation": generate_doc},
        defaults=True,
        unsafe=True,
    )

    assert tmp_path.exists()
    if generate_doc:
        _check_file_contents(
            dst_path / "docs" / "index.md",
            expected_strs=["# Welcome to Snake Farm documentation!"],
        )
        _check_file_contents(
            dst_path / ".readthedocs.yml",
            expected_strs=["configuration: docs/conf.py"],
        )
        _check_file_contents(
            dst_path / "pyproject.toml",
            expected_strs=["[tool.poetry.group.docs]"],
        )
    else:
        assert not (dst_path / "docs").exists()
        assert not (dst_path / ".readthedocs.yml").exists()
        _check_file_contents(
            dst_path / "pyproject.toml",
            unexpect_strs=["[tool.poetry.group.docs]"],
        )


@pytest.mark.parametrize(
    ("has_cli", "cli_name"),
    [
        (True, "mycli"),
        (False, ""),
    ],
)
def test_cli(
    tmp_path: Path,
    base_answers: dict[str, str | bool],
    has_cli: bool,
    cli_name: str,
):
    dst_path = tmp_path / "snake-farm"
    copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**base_answers, "has_cli": has_cli, "cli_name": cli_name},
        defaults=True,
        unsafe=True,
    )

    assert tmp_path.exists()
    if has_cli:
        _check_file_contents(
            dst_path / "src" / "snake_farm" / "__main__.py",
            expected_strs=['app(prog_name="mycli")'],
        )
        _check_file_contents(
            dst_path / "src" / "snake_farm" / "cli.py",
            expected_strs=["app = typer.Typer()"],
        )
        _check_file_contents(
            dst_path / "pyproject.toml",
            expected_strs=["[tool.poetry.scripts]", 'mycli = "snake_farm.cli:app"'],
        )
    else:
        assert not (dst_path / "src" / "snake_farm" / "__main__.py").exists()
        assert not (dst_path / "src" / "snake_farm" / "cli.py").exists()
        _check_file_contents(
            dst_path / "pyproject.toml",
            unexpect_strs=["[tool.poetry.scripts]", 'mycli = "snake_farm.cli:app"'],
        )
