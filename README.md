# Cookiecutter PyPackage

<a href="https://github.com/browniebroke/cookiecutter-pypackage/actions?query=workflow%3ATest">
  <img src="https://img.shields.io/github/workflow/status/browniebroke/cookiecutter-pypackage/Test?label=Test&logo=github&style=flat-square" alt="GitHub Workflow Status" >
</a>

Cookiecutter template for a Python Package.

## Features

- Project for Python 3.6+
- Testing with Pytest using Github actions
- Follows the Black style guide with iSort
- Comes with pre-commit hook config for Black, Flake8 and Pyupgrade
- Style guide enforced on CI
- Dependencies pinned with pip-compile and updated by Dependabot
- Follow the [all-contributors](https://github.com/all-contributors/all-contributors) specification
- Automated release notes and changelog generation based on Pull requests
- Automated PyPI releases using Github actions
- Documentation configured with Sphinx and [MyST Parser](https://myst-parser.readthedocs.io)
- Standardised list of Github labels synchronised on push to master using [the labels CLI](https://github.com/hackebrot/labels).
