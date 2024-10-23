# Python Package Template

<a href="https://github.com/browniebroke/pypackage-template/actions/workflows/ci.yml?query=branch%3Amain">
  <img src="https://img.shields.io/github/actions/workflow/status/browniebroke/pypackage-template/ci.yml?branch=main&label=Test&logo=github&style=flat-square" alt="CI Status" >
</a>

Project template for a Python Package using Copier.

## Features

- Project for Python 3.8+.
- Testing with Pytest using GitHub actions.
- Packaging powered by [poetry].
- Optionally generates a CLI entry point powered by [Typer] and [Rich].
- Optionally makes it a Django package.
- Uses [Ruff] for formatting and linting.
- Comes with [pre-commit] hook config for [Ruff].
- Style guide enforced on CI.
- Dependencies kept up to date by [Renovate].
- Follow the [all-contributors] specification.
- Follow to [the conventional commits][conventional-commits] specification.
- Automated releasing using [python-semantic-release][python-semantic-release].
- Documentation configured with Sphinx and [MyST Parser][myst].
- Follows the contributor covenant code of conduct.
- Standardised list of GitHub labels synchronised on push to master using [the labels CLI][pylabels].

## Usage

First, install Copier and inject some dependencies:

```shell
pipx install copier
pipx inject copier jinja2-eval jinja2-env jinja2-time arrow
```

Next install GitHub CLI and set up `PYPACKAGE_TEMPLATE_GITHUB_TOKEN` environment variable with a [personal access token (PAT)][create-pat] with the `repo` scope.

```shell
set -x GITHUB_TOKEN ghp_...
```

Next set up [trusted publisher](#trusted-publisher-setup) and then generate a new project with:

```shell
copier copy --trust "gh:browniebroke/pypackage-template" path-to-project
```

This will prompt you for a few questions and create new directory with the name you used as project slug.

> _Note:_
> the `--trust` option is required because this template may execute some tasks after generating the project, like initialising the git repo, installing dependencies and so forth. These are all listed in the `copier.yml` of this repo, under the `_tasks` key. They are all optional and safe to run. You can take my word for it, or better, check the code yourself!
> go to [Applications Settings](https://github.com/settings/installations) and copy the id in the link (`https://github.com/organizations/<Organization-name>/settings/installations/<ID>`) for the `Configure` button for the GitHub Apps you want to have installed automatically. (You may want to install [Renovate](https://github.com/marketplace/renovate), [pre-commit ci](https://github.com/marketplace/pre-commit-ci), as AllContributors and Codecov can be installed globally)

### Start developing

The project uses [Poetry] for dependencies management and packaging. Make sure you have it installed in your development machine. To install the development dependencies in a virtual environment, type:

```shell
poetry install
```

This will also generate a `poetry.lock` file, you should track this file in version control. To execute the test suite, call pytest inside Poetry's virtual environment via `poetry run`:

```shell
poetry run pytest
```

Check out the [Poetry] documentation for more information on the available commands.

### GitHub Actions

When you first push to GitHub, it'll start a `ci` GitHub workflow that you can see in the "Actions" tab of your repository. This workflow runs a couple of jobs:

- The `test` job will run your test suite with Pytest against all Python version from 3.8 to 3.11
- A few things will run in the lint job:
  - Ruff format
  - Ruff lint with several flake8, isort and pyupgrade plugins.

A `labels` workflow will also run and synchronise the GitHub labels based on the `.github/labels.toml` file.

### Secrets

The workflows need [a few secrets][gh-secrets] to be setup in your GitHub repository:

- `GH_PAT` a [personal access token (PAT) with the `repo` scope][create-pat] for opening pull requests and updating the repository topics. This is used by the `poetry-upgrade` and `labels` workflows.
- `CODECOV_TOKEN` to upload coverage data to [codecov.io][codecov] in the Test workflow.

If you have the GitHub CLI installed and chose to set up GitHub, they will be created with a dummy value (`changeme`).

### Automated release

By following the conventional commits specification, we're able to completely automate versioning and releasing to PyPI. It runs on every push to your main branch, as part of the `release` job of the `ci.yml` workflow. You shouldn't need to create a token, but you'll need to setup [trusted publisher](https://docs.pypi.org/trusted-publishers/using-a-publisher/) for the project.

#### Trusted publisher setup

The first time you push, the workflow will try to create a release in PyPI, however the project doesn't exist there yet, which seems like a chicken and egg situation. Luckily, you can add a trusted publisher before creating the PyPI project here: https://pypi.org/manage/account/publishing/. Here are the infos that you should use:

- PyPI project name: what you've entered as "project slug"
- Owner: your GitHub username
- Repository name: what you've entered as "project slug"
- Workflow name: `ci.yml`
- Environment name: `release`

If the release phase failed the first time, you might have to remove the release and tag from GitHub, and perhaps tidy up the changelog.

#### How it works

Here is an overview of what it's doing:

- Check the commit log since the last release, and determine the next version to be released.
- If no significant change detected, stop here (e.g. just dependencies update).
- Otherwise, bump the version in code locations specified in `setup.cfg`.
- Update the `CHANGELOG.md` file.
- Commit changes.
- Create a git tag.
- Push to GitHub.
- Create a release in GitHub with the changes as release notes.
- Build the source and binary distribution (wheel).
- Upload the sources to PyPI and attach them to the Github release, using trusted publisher.

For more details, check out the [conventional commits website][conventional-commits] and [Python semantic release][python-semantic-release] GitHub action.

### Optional: Django package

If your package is a reusable Django app, you should answer "yes" to the question "Is the project a Django package?". This will generate a bit more boilerplate for you to make it easier to develop and test:

- At the root, you'll get a `manage.py` which is going to come handy if your package contain any models and you need to run migrations for it.
- Testing will use tox as the Django-Python support matrix can be complicated.
- Inside your package source, you'll get a `conf.py` to include your reusable app settings, for the users of your app to configure your app. This is following the pattern explained in [this blog post](https://overtag.dk/v2/blog/a-settings-pattern-for-reusable-django-apps/).
- The tests will come in with settings and URLs files, along with an test app with basic models.

#### Migrations

You should be able to use the provided `manage.py` to create migrations for your reusable app. Create or change your models and run `poetry run python manage.py makemigrations`.

### Pre-commit

The project comes with the config for [pre-commit]. If you're not familiar with it, follow their documentation on how to install it and set it up.

### Documentation

The project assumes that the documentation will be hosted on Read the Docs and written in Markdown with the [MyST parser for Sphinx][myst].

To enable it, you might need to go [into your dashboard][rtd-dashboard] and import the project from Github. Everything else should work out of the box.

### Dependencies update

The project dependencies are kept up to date with [Renovate] which requires [the Github app][renovate-gh-app] to be installed.

The main advantage of Renovate over Dependabot is the auto-merge option, which is configured to automatically merge minor/patch updates with all the CI checks passing. It supports a variety of package managers, including Poetry, GitHub actions and pre-commit hooks which are used by default.

### All contributors

This is a specification that help you highlight every open source contribution in your README. This is easy to maintain as it comes with a GitHub bot to do the updates for you, so more manual updates on the contributors file.

If you never used it before, you will have to [install the Github app][all-contribs-install] and give it access to your repo.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://browniebroke.com/"><img src="https://avatars.githubusercontent.com/u/861044?v=4?s=80" width="80px;" alt="Bruno Alla"/><br /><sub><b>Bruno Alla</b></sub></a><br /><a href="https://github.com/browniebroke/pypackage-template/commits?author=browniebroke" title="Code">💻</a> <a href="#ideas-browniebroke" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/browniebroke/pypackage-template/commits?author=browniebroke" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://cloudreactor.io/"><img src="https://avatars.githubusercontent.com/u/1079646?v=4?s=80" width="80px;" alt="Jeff Tsay"/><br /><sub><b>Jeff Tsay</b></sub></a><br /><a href="https://github.com/browniebroke/pypackage-template/commits?author=jtsay362" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/34j"><img src="https://avatars.githubusercontent.com/u/55338215?v=4?s=80" width="80px;" alt="34j"/><br /><sub><b>34j</b></sub></a><br /><a href="https://github.com/browniebroke/pypackage-template/commits?author=34j" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kroimon"><img src="https://avatars.githubusercontent.com/u/628587?v=4?s=80" width="80px;" alt="Stefan Rado"/><br /><sub><b>Stefan Rado</b></sub></a><br /><a href="https://github.com/browniebroke/pypackage-template/commits?author=kroimon" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/codejedi365"><img src="https://avatars.githubusercontent.com/u/17354856?v=4?s=80" width="80px;" alt="codejedi365"/><br /><sub><b>codejedi365</b></sub></a><br /><a href="https://github.com/browniebroke/pypackage-template/commits?author=codejedi365" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.habet.dev"><img src="https://avatars.githubusercontent.com/u/82916197?v=4?s=80" width="80px;" alt="Abe Hanoka"/><br /><sub><b>Abe Hanoka</b></sub></a><br /><a href="https://github.com/browniebroke/pypackage-template/issues?q=author%3Aabe-101" title="Bug reports">🐛</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

[poetry]: https://python-poetry.org
[Typer]: https://typer.tiangolo.com
[Rich]: https://rich.readthedocs.io
[Ruff]: https://pypi.org/project/ruff/
[pre-commit]: https://pre-commit.com/
[renovate]: https://docs.renovatebot.com/
[renovate-gh-app]: https://github.com/apps/renovate
[all-contributors]: https://github.com/all-contributors/all-contributors
[conventional-commits]: https://www.conventionalcommits.org
[python-semantic-release]: https://github.com/relekang/python-semantic-release
[myst]: https://myst-parser.readthedocs.io
[pylabels]: https://github.com/hackebrot/labels
[gh-secrets]: https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets
[codecov]: https://codecov.io/
[pypi]: https://pypi.org/
[create-pat]: https://github.com/settings/tokens/new?description=pypackage-template&scopes=repo
[rtd-dashboard]: https://readthedocs.org/dashboard/
[all-contribs-install]: https://allcontributors.org/docs/en/bot/installation
