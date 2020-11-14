from subprocess import CalledProcessError

import pytest

from hooks.post_gen_project import run_poetry_install


@pytest.mark.parametrize(
    "side_effect",
    [
        FileNotFoundError(),
        CalledProcessError(1, ""),
    ],
)
def test_poetry_not_installed(mocker, side_effect):
    subprocess_run = mocker.patch("subprocess.run", side_effect=side_effect)

    run_poetry_install()

    subprocess_run.assert_called_once_with(
        ["poetry", "-h"], check=True, capture_output=True
    )


def test_poetry_installed(mocker):
    subprocess_run = mocker.patch("subprocess.run")

    run_poetry_install()

    assert subprocess_run.call_count == 2
    subprocess_run.assert_any_call(["poetry", "-h"], check=True, capture_output=True)
    subprocess_run.assert_any_call(["poetry", "install"], check=True)
