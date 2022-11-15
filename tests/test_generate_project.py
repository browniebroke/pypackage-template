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
        "documentation": True,
        "run_poetry_install": False,
        "initial_commit": False,
        "setup_github": False,
        "setup_pre_commit": False,
        "add_me_as_contributor": False,
    }


def test_generate_project(tmp_path, base_context):
    worker = copier.run_auto(
        str(PROJECT_ROOT),
        tmp_path,
        data=base_context,
        defaults=True,
    )
    assert worker is not None
