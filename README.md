# Cookiecutter PyPackage

<a href="https://github.com/browniebroke/cookiecutter-pypackage/actions?query=workflow%3ACI">
  <img src="https://img.shields.io/github/workflow/status/browniebroke/cookiecutter-pypackage/CI?label=Test&logo=github&style=flat-square" alt="CI Status" >
</a>

Cookiecutter template for a Python Package.

## Features

- Project for Python 3.6+.
- Testing with Pytest using Github actions.
- Follows the [black] style guide with [flake8] and [isort].
- Comes with [pre-commit] hook config for black, isort, flake8 and [pyupgrade](https://github.com/asottile/pyupgrade).
- Style guide enforced on CI.
- Dependencies pinned with pip-compile and updated by [dependabot].
- Follow the [all-contributors] specification.
- Follow to [the conventional commits][conventional-commits] specification.
- Automated releasing using [python-semantic-release][python-semantic-release].
- Documentation configured with Sphinx and [MyST Parser][myst].
- Standardised list of Github labels synchronised on push to master using [the labels CLI][pylabels].

## Usage

Generate a new project with:

```shell
cookiecutter https://github.com/browniebroke/cookiecutter-pypackage
```

This will prompt you for a few questions and create new directory with the name you used as project slug.

### Next steps

When you first push to Github, it'll start a few Github workflows that you can see in the "Actions" tab of your repository:

- The test suite will run your tests with Pytest in the Test workflow
- A few things will run in the Lint workflow:
   - black in check mode
   - isort in check mode
   - flake8 with isort
   - pyupgrade, this will make sure you sure modern Python
- The labels workflow will synchronise Github labels based on the `.github/labels.toml` file.

### Secrets

The workflows need [2 secrets][gh-secrets] to be setup in your Github repository:

- `CODECOV_TOKEN` to upload coverage data to [codecov.io][codecov] in the Test workflow (optional for public repos).
- `PYPI_TOKEN` to publish a release to [PyPI][pypi] in the Publish to PyPI workflow.

### Automated release

By following the conventional commits specification, we're able to completely automate versioning and releasing to PyPI. This is handled by the `semantic-release.yml` workflow. It is triggered manually by default, but can be configured to run on every push to your main branch.

Here is an overview of its features:

- Check the commit log since the last release, and determine the next version to be released.
- If no significant change detected, stop here (e.g. just dependencies update).
- Otherwise, bump the version in code locations specified in `setup.cfg`.
- Update the `CHANGELOG.md` file.
- Commit changes.
- Create a git tag.
- Push to Github.
- Create a release in Github with the changes as release notes.
- Build the source and binary distribution (wheel).
- Upload the sources to PyPI and attach them to the Github release.

For more details, check out the [conventional commits website][conventional-commits] and [Python semantic release][python-semantic-release] Github action.

### Pre-commit

The project comes with the config for [pre-commit]. If you're not familiar with it, follow their documentation on how to install it and set it up.

### Documentation

The project assumes that the documentation will be hosted on Read the Docs and written in Markdown with the [MyST parser for Sphinx][myst]. 

To enable it, you might need to go [into your dashboard][rtd-dashboard] and import the project from Github. Everything else should work out of the box.

### All contributors

This is a specification that help you highlight all of the open source contributions on your README. This is easy to maintain as it comes with a Github bot to do the updates for you, so more manual updates on the contributors file.

If you never used it before, you will have to [install the Github app][all-contribs-install] and give it access to your repo.

[black]: https://github.com/psf/black
[flake8]: https://pypi.org/project/flake8/
[isort]: https://pypi.org/project/isort/
[pre-commit]: https://pre-commit.com/
[dependabot]: https://dependabot.com/
[all-contributors]: https://github.com/all-contributors/all-contributors
[conventional-commits]: https://www.conventionalcommits.org
[python-semantic-release]: https://github.com/relekang/python-semantic-release
[myst]: https://myst-parser.readthedocs.io
[pylabels]: https://github.com/hackebrot/labels
[gh-secrets]: https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets
[codecov]: https://codecov.io/
[pypi]: https://pypi.org/
[rtd-dashboard]: https://readthedocs.org/dashboard/
[all-contribs-install]: https://allcontributors.org/docs/en/bot/installation
