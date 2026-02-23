from __future__ import annotations

import textwrap
from collections.abc import Sequence
from os import environ
from pathlib import Path

import copier
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
CI = environ.get("CI", "false").lower() == "true"


@pytest.fixture
def base_answers():
    return {
        "full_name": "Jeanne Deau",
        "email": "action@github.com",
        "github_username": "actions-user",
        "project_name": "Snake Farm",
        "project_short_description": "A sample Snake farming project.",
        "version": "0.0.1",
        "open_source_license": "MIT",
        "documentation": True,
        "run_uv_sync": False,
        "initial_commit": True,
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
            "Apache-2.0",
            True,
            ["Apache License"],
            ["MIT License", "GNU GENERAL PUBLIC LICENSE"],
        ),
        (
            "GPL-3.0-only",
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
            expected_strs=["{include} ../README.md"],
        )
        _check_file_contents(
            dst_path / ".readthedocs.yml",
            expected_strs=[
                "configuration: docs/conf.py",
                "uv sync --frozen --no-dev --group docs",
            ],
        )
        _check_file_contents(
            dst_path / "pyproject.toml",
            expected_strs=["docs = [", "sphinx==", "myst-parser"],
        )
        _check_file_contents(
            dst_path / "docs" / "conf.py",
            expected_strs=[
                textwrap.dedent(
                    """
                    from pathlib import Path
                    from typing import Any

                    from sphinx.application import Sphinx
                    from sphinx.ext import apidoc

                    # -- Project information"""
                )
            ],
        )
    else:
        assert not (dst_path / "docs").exists()
        assert not (dst_path / ".readthedocs.yml").exists()
        _check_file_contents(
            dst_path / "pyproject.toml",
            unexpect_strs=["docs = [", "sphinx==", "myst-parser"],
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
            expected_strs=['scripts.mycli = "snake_farm.cli:app"'],
        )
    else:
        assert not (dst_path / "src" / "snake_farm" / "__main__.py").exists()
        assert not (dst_path / "src" / "snake_farm" / "cli.py").exists()
        _check_file_contents(
            dst_path / "pyproject.toml",
            unexpect_strs=['scripts.mycli = "snake_farm.cli:app"'],
        )


def test_django_package_yes(
    tmp_path: Path,
    base_answers: dict[str, str | bool],
):
    dst_path = tmp_path / "snake-farm"
    copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={
            **base_answers,
            "project_name": "Django Snake Farm",
            "is_django_package": True,
            "documentation": True,
        },
        defaults=True,
        unsafe=True,
    )

    assert tmp_path.exists()
    assert (
        dst_path / "src" / "django_snake_farm" / "migrations" / "__init__.py"
    ).exists()
    _check_file_contents(
        dst_path / "pyproject.toml",
        expected_strs=[
            '"Framework :: Django :: 4.2",',
            '"Framework :: Django :: 5.0",',
            '"Framework :: Django :: 5.1",',
            '"Framework :: Django :: 5.2",',
            '"Framework :: Django :: 6.0",',
            '"django>=4.2"',
            "pytest-django==",
            'DJANGO_SETTINGS_MODULE = "tests.settings"',
            "django60 = [ \"django>=6.0a1,<6.1; python_version>='3.12'\" ]",
            'django42 = [ "django>=4.2a1,<5" ]',
        ],
    )
    _check_file_contents(
        dst_path / "manage.py",
        expected_strs=[
            'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")',
        ],
    )
    _check_file_contents(
        dst_path / "src" / "django_snake_farm" / "conf.py",
        expected_strs=[
            "All attributes prefixed ``SNAKE_FARM_*``",
            "class AppSettings:",
            "app_settings = AppSettings()",
        ],
    )
    _check_file_contents(
        dst_path / "src" / "django_snake_farm" / "apps.py",
        expected_strs=[
            "class SnakeFarmAppConfig(AppConfig):",
            '"""App config for Django Snake Farm."""',
            'name = "django_snake_farm"',
            'verbose_name = _("snake farm")',
        ],
    )
    _check_file_contents(
        dst_path / "tests" / "settings.py",
        expected_strs=[
            'SECRET_KEY = "NOTASECRET"  # noqa S105',
            '    "django_snake_farm",',
            "MIDDLEWARE = [",
            "TEMPLATES = [",
            'DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"',
        ],
    )
    _check_file_contents(
        dst_path / "tests" / "urls.py",
        expected_strs=[
            "urlpatterns = [",
            '    path("admin/", admin.site.urls),',
        ],
    )
    _check_file_contents(
        dst_path / "tests" / "testapp" / "apps.py",
        expected_strs=[
            "class TestAppConfig(AppConfig):",
            '    name = "tests.testapp"',
            '    verbose_name = "Test App"',
        ],
    )
    _check_file_contents(
        dst_path / "tests" / "testapp" / "models.py",
        expected_strs=[
            "class Blog(models.Model):",
        ],
    )
    _check_file_contents(
        dst_path / "docs" / "conf.py",
        expected_strs=[
            textwrap.dedent(
                """
                from pathlib import Path
                from typing import Any

                from django.conf import settings
                from sphinx.application import Sphinx
                from sphinx.ext import apidoc

                settings.configure(USE_I18N=False)

                # -- Project information"""
            )
        ],
    )
    _check_file_contents(
        dst_path / "docs" / "index.md",
        expected_strs=["configuration"],
    )
    _check_file_contents(
        dst_path / "docs" / "configuration.rst",
        expected_strs=[".. automodule:: django_snake_farm.conf"],
    )
    _check_file_contents(
        dst_path / "docs" / "installation.md",
        expected_strs=["Add the app to your `INSTALLED_APPS`:"],
    )
    _check_file_contents(
        dst_path / "tox.ini",
        expected_strs=[
            "django42: django42",
            "django50: django50",
            "django51: django51",
            "django52: django52",
            "django60: django60",
        ],
    )
    _check_file_contents(
        dst_path / ".github" / "ISSUE_TEMPLATE" / "1-bug-report.yml",
        expected_strs=["id: django_version"],
    )
    _check_file_contents(
        dst_path / ".github" / "workflows" / "ci.yml",
        expected_strs=[
            "run: tox -f py$(echo ${{ matrix.python-version }} | tr -d .)",
        ],
        unexpect_strs=["uv run pytest"],
    )


def test_django_package_no(
    tmp_path: Path,
    base_answers: dict[str, str | bool],
):
    dst_path = tmp_path / "snake-farm"
    copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**base_answers, "is_django_package": False, "documentation": True},
        defaults=True,
        unsafe=True,
    )

    assert tmp_path.exists()
    assert not (dst_path / "src" / "snake_farm" / "migrations" / "__init__.py").exists()
    assert not (dst_path / "manage.py").exists()
    assert not (dst_path / "src" / "snake_farm" / "conf.py").exists()
    assert not (dst_path / "src" / "snake_farm" / "apps.py").exists()
    assert not (dst_path / "tests" / "settings.py").exists()
    assert not (dst_path / "tests" / "urls.py").exists()
    assert not (dst_path / "tests" / "testapp").exists()
    assert not (dst_path / "docs" / "configuration.rst").exists()
    _check_file_contents(
        dst_path / "pyproject.toml",
        unexpect_strs=[
            '"Framework :: Django :: 4.2",',
            '"Framework :: Django :: 5.0",',
            '"Framework :: Django :: 5.1",',
            '"Framework :: Django :: 5.2",',
            '"django>=4.2"',
            "pytest-django>=4.5,<5",
        ],
    )
    _check_file_contents(
        dst_path / ".gitignore", unexpect_strs=["requirements-dev.txt"]
    )
    _check_file_contents(
        dst_path / ".github" / "ISSUE_TEMPLATE" / "1-bug-report.yml",
        unexpect_strs=["id: django_version"],
    )
    _check_file_contents(
        dst_path / ".github" / "workflows" / "ci.yml",
        expected_strs=["uv run pytest"],
        unexpect_strs=[
            "run: tox -f py$(echo ${{ matrix.python-version }} | tr -d .)",
        ],
    )


@pytest.mark.skipif(CI, reason="GitHub API rate limit")
def test_add_me_as_contributor(
    tmp_path: Path,
    base_answers: dict[str, str | bool],
):
    dst_path = tmp_path / "snake-farm"
    copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**base_answers, "add_me_as_contributor": True},
        defaults=True,
        unsafe=True,
    )
    assert tmp_path.exists()
    _check_file_contents(
        dst_path / "README.md",
        expected_strs=[f"commits?author={base_answers['github_username']}"],
    )
    _check_file_contents(
        dst_path / ".all-contributorsrc",
        expected_strs=[f"{base_answers['github_username']}"],
    )
