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
    dst_path = tmp_path / "snake-farm"
    worker = copier.run_auto(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data=base_answers,
    )
    assert worker is not None
    assert tmp_path.exists()
    readme = dst_path / "README.md"
    assert readme.exists()
    assert "# Snake Farm" in readme.read_text()
