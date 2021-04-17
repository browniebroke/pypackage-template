from subprocess import CalledProcessError

import pytest

from hooks.post_gen_project import (
    add_me_as_contributor,
    check_command_exists,
    initial_commit,
    run_poetry_install,
    setup_github,
    setup_pre_commit,
)


@pytest.mark.parametrize(
    "side_effect",
    [
        FileNotFoundError(),
        CalledProcessError(1, ""),
    ],
)
def test_check_command_exists(mocker, side_effect):
    subprocess_run = mocker.patch("subprocess.run", side_effect=side_effect)

    assert check_command_exists("something") is False

    assert subprocess_run.call_count == 1
    subprocess_run.assert_any_call(["something", "-h"], check=True, capture_output=True)


def test_run_poetry_install(mocker):
    subprocess_run = mocker.patch("subprocess.run")

    run_poetry_install()

    assert subprocess_run.call_count == 2
    subprocess_run.assert_any_call(["poetry", "-h"], check=True, capture_output=True)
    subprocess_run.assert_any_call(["poetry", "install"], check=True)


def test_initial_commit(mocker):
    subprocess_run = mocker.patch("subprocess.run")

    initial_commit()

    assert subprocess_run.call_count == 3
    subprocess_run.assert_any_call(["git", "init"], check=True)
    subprocess_run.assert_any_call(["git", "add", "."], check=True)
    subprocess_run.assert_any_call(
        ["git", "commit", "-m", "'feat: initial commit'"], check=True
    )


def test_setup_github(mocker):
    subprocess_run = mocker.patch("subprocess.run")

    setup_github()

    assert subprocess_run.call_count == 2
    subprocess_run.assert_any_call(["gh", "-h"], check=True, capture_output=True)
    subprocess_run.assert_any_call(
        [
            "gh",
            "repo",
            "create",
            "{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}",
            "-y",
            "-d",
            "{{ cookiecutter.project_short_description }}",
            "--public",
            "--enable-wiki=false",
        ],
        check=True,
    )


def test_setup_pre_commit(mocker):
    subprocess_run = mocker.patch("subprocess.run")

    setup_pre_commit()

    assert subprocess_run.call_count == 2
    subprocess_run.assert_any_call(
        ["pre-commit", "-h"], check=True, capture_output=True
    )
    subprocess_run.assert_any_call(["pre-commit", "install"], check=True)


def test_add_me_as_contributor(mocker):
    subprocess_run = mocker.patch("subprocess.run")

    add_me_as_contributor()

    assert subprocess_run.call_count == 2
    subprocess_run.assert_any_call(["npx", "-h"], check=True, capture_output=True)
    subprocess_run.assert_any_call(
        [
            "npx",
            "all-contributors-cli",
            "add",
            "{{ cookiecutter.github_username }}",
            "code,ideas,doc",
        ],
        check=True,
    )
