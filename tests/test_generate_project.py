from pathlib import Path

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
        "project_slug": "snake-farm",
        "package_name": "snake_farm",
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


def test_generate_project(tmp_path, base_answers):
    worker = copier.run_auto(
        str(PROJECT_ROOT),
        tmp_path,
        data=base_answers,
    )
    assert worker is not None
    assert tmp_path.exists()
    readme = tmp_path / "snake-farm" / "README.md"
    assert readme.exists()
    assert "# Snake Farm" in readme.read_text()
