import os
from pathlib import Path

import copier
import pytest

PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture
def base_context():
    return {
        "full_name": "Jeanne Deau",
        "email": "jeanne.deau@example.fr",
        "github_username": "jdeau",
        "project_name": "Snake Farm",
        "project_short_description": "A sample farming {{ package_name }}",
        "run_poetry_install": "n",
        "setup_github": "n",
    }


def test_generate_project(tmp_path, base_context):
    worker = copier.run_auto(
        str(PROJECT_ROOT),
        tmp_path,
        data=base_context,
        defaults=True,
    )
    breakpoint()
    assert worker is not None

    assert result.exit_code == 0, result.exception
    assert result.exception is None
    assert result.project_path.name == "snake-farm"
    assert result.project_path.is_dir()

    paths = [
        Path(dirpath) / file_path
        for dirpath, subdirs, files in os.walk(result.project_path)
        for file_path in files
    ]
    assert paths
    check_paths(paths)


@pytest.mark.parametrize(
    ("docs_opt", "expect_present"),
    [
        ("y", True),
        ("n", False),
    ],
)
def test_generate_documentation_option(cookies, base_context, docs_opt, expect_present):
    result = cookies.bake(
        extra_context={
            **base_context,
            "documentation": docs_opt,
        }
    )

    assert result.exit_code == 0, result.exception
    root = result.project_path
    assert (root / "docs").exists() is expect_present
    assert (root / ".readthedocs.yml").exists() is expect_present
    assert (
        "img.shields.io/readthedocs" in (root / "README.md").read_text()
    ) is expect_present
    assert ("Sphinx" in (root / "pyproject.toml").read_text()) is expect_present
