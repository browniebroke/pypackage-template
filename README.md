# Cookiecutter PyPackage

<a href="https://github.com/browniebroke/cookiecutter-pypackage/actions?query=workflow%3ATest">
  <img src="https://img.shields.io/github/workflow/status/browniebroke/cookiecutter-pypackage/Test?label=Test&logo=github&style=flat-square" alt="GitHub Workflow Status" >
</a>

Cookiecutter template for a Python Package.

## Features

- Project for Python 3.6+
- Testing with Pytest using Github actions
- Follows the [Black](https://github.com/psf/black) style guide with [flake8](https://pypi.org/project/flake8/) and [isort](https://pypi.org/project/isort/)
- Comes with [pre-commit](https://pre-commit.com/) hook config for Black, isort, Flake8 and [Pyupgrade](https://github.com/asottile/pyupgrade)
- Style guide enforced on CI
- Dependencies pinned with pip-compile and updated by [Dependabot](https://dependabot.com/)
- Follow the [all-contributors](https://github.com/all-contributors/all-contributors) specification
- Automated release notes and changelog generation based on Pull requests
- Automated PyPI releases using Github actions
- Documentation configured with Sphinx and [MyST Parser](https://myst-parser.readthedocs.io)
- Standardised list of Github labels synchronised on push to master using [the labels CLI](https://github.com/hackebrot/labels).

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
   - Black in check mode
   - Flake8 with isort
   - Pyupgrade, this will make sure you sure modern Python
- The labels workflow will synchronise Github labels based on the `.github/labels.toml` file.

### Secrets

The workflows need [2 secrets](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets) to be setup in your Github repository:

- `CODECOV_TOKEN` to upload coverage data to [codecov.io](https://codecov.io/) in the Test workflow (optional for public repos).
- `PYPI_TOKEN` to publish a release to [PyPI](https://pypi.org/) in the Publish to PyPI workflow.

### Changelog generation

2 workflows are configured to:
 
- Generate the `CHANGELOG.md` file
- Create and update the next release in Github

They are both configured to mention merged pull requests. Pull requests are grouped in sections based on the label added to the pull requests. You can see the mapping of label/sections in `.github/release-drafter.yml` and `.github/workflows/changelog-generator.yml`.

You may exclude some pull requests by giving them the label `nochangelog`.

### Pre-commit

The project comes with the config for [Pre-Commit](https://pre-commit.com/). If you're not familiar with it, follow their documentation on how to install it and set it up.

### Documentation

The project assumes that the documentation will be hosted on Read the Docs and written in Markdown with the [MyST parser for Sphinx](https://myst-parser.readthedocs.io/en/latest/). 

To enable it, you might need to go [into your dashboard](https://readthedocs.org/dashboard/) and import the project from Github. Everything else should work out of the box.

### Releasing to PyPI

To make a release to PyPI, you need to follow the following steps

- Update the package version with [`bump2version`](https://pypi.org/project/bump2version/). If you're not familiar with the tool, best to check their documentation
- Push the changes with the tags to Github and wait for the build to complete.
- Go to the release tab, edit the latest draft release to point to the git tag you pushed earlier and then publish the release. 

  This will trigger a workflow to create the package and upload it to PyPI (you'd need to have set the `PYPI_TOKEN` secret).

### All contributors

This is a specification that help you highlight all of the open source contributions on your README. This is easy to maintain as it comes with a Github bot to do the updates for you, so more manual updates on the contributors file.

If you never used it before, you will have to [install the Github app](https://allcontributors.org/docs/en/bot/installation) and give it access to your repo.
