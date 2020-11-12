import os
import re
from pathlib import Path

import pytest
from binaryornot.check import is_binary


@pytest.fixture
def base_context():
    return {
        "full_name": "Jeanne Deau",
        "email": "jeanne.deau@example.fr",
        "github_username": "jdeau",
        "project_name": "Snake Farm",
        "project_short_description": "A sample farming project",
        "run_poetry_install": "n",
    }


RE_OBJ = re.compile(r"{{(\s?cookiecutter)[.](.*?)}}")


def check_paths(paths):
    """Method to check all paths have correct substitutions."""
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(str(path)):
            continue

        with path.open() as fd:
            content = fd.read()
            match = RE_OBJ.search(content)
            assert match is None, f"cookiecutter variable not replaced in {path}"


def test_generate_project(cookies, base_context):
    result = cookies.bake(extra_context=base_context)

    assert result.exit_code == 0, result.exception
    assert result.exception is None
    assert result.project.basename == "snake-farm"
    assert result.project.isdir()

    paths = [
        Path(dirpath) / file_path
        for dirpath, subdirs, files in os.walk(result.project)
        for file_path in files
    ]
    assert paths
    check_paths(paths)
