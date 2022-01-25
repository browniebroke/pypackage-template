# Contributing

Contributions are welcome, and they are greatly appreciated! Every little helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs to [our issue page][gh-issues].

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

{{ cookiecutter.project_name }} could always use more documentation, whether as part of the official {{ cookiecutter.project_name }} docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback [our issue page][gh-issues] on GitHub. If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Get Started!

Ready to contribute? Here's how to set yourself up for local development.

1. Fork the repo on GitHub.

2. Clone your fork locally:

   ```shell
   $ git clone git@github.com:your_name_here/{{ cookiecutter.project_slug }}.git
   ```

3. Install the project dependencies with [Poetry](https://python-poetry.org):

   ```shell
   $ poetry install
   ```

4. Create a branch for local development:

   ```shell
   $ git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass our tests:

   ```shell
   $ poetry run pytest
   ```

6. Linting is done through [pre-commit](https://pre-commit.com). Provided you have the tool installed globally, you can run them all as one-off:

   ```shell
   $ pre-commit run -a
   ```

   Or better, install the hooks once and have them run automatically each time you commit:

   ```shell
   $ pre-commit install
   ```

8. Commit your changes and push your branch to GitHub:

   ```shell
   $ git add .
   $ git commit -m "Your detailed description of your changes."
   $ git push origin name-of-your-bugfix-or-feature
   ```

9. Submit a pull request through the GitHub website or using the GitHub CLI (if you have it installed):

   ```shell
   $ gh pr create --fill
   ```

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.rst.
3. The pull request should work for Python 3.6, 3.7 and 3.8. Check the build and make sure that the tests pass for all supported Python versions.

## Tips

To run a subset of tests:

```shell
$ pytest tests
```

## Making a new release

The deployment should be automated and can be triggered from the Semantic Release workflow in GitHub. The next version will be based on [the commit logs](https://python-semantic-release.readthedocs.io/en/latest/commit-log-parsing.html#commit-log-parsing). This is done by [python-semantic-release](https://python-semantic-release.readthedocs.io/en/latest/index.html) via a GitHub action.

[gh-issues]: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues
