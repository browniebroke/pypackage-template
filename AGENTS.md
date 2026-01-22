# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## Project Overview

This is a **Copier template** for generating Python packages. It is not a Python package itself, but a template that generates Python projects when users run `copier copy`.

## Development Commands

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run a single test
uv run pytest tests/test_generate_project.py::test_defaults_values

# Run pre-commit hooks
pre-commit run -a

# Format/lint (via pre-commit)
ruff check --fix .
ruff format .
```

## Architecture

### Template Structure

- `copier.yml` - Template configuration with all user-facing questions and post-generation tasks
- `project/` - The actual template files that get copied to generated projects
  - Files with `.jinja` extension are processed by Jinja2
  - Files/folders with `{% if condition %}` in names are conditionally included
  - `{{package_name}}` in paths gets replaced with user input
- `tests/` - Tests that verify template generation produces valid projects

### Key Template Options

The template supports several modes controlled by `copier.yml` questions:

- `is_django_package` - Adds Django-specific config (migrations, settings, tox for matrix testing)
- `has_cli` - Adds Typer CLI boilerplate
- `documentation` - Adds Sphinx/MyST documentation setup
- `open_source_license` - Generates appropriate LICENSE file

### Testing Strategy

Tests use `copier.run_copy()` to generate projects in temp directories, then verify:

- Expected files exist with correct content
- Conditional files are included/excluded properly based on options
- Generated projects are valid (CI also runs pytest/pre-commit/docs on generated output)

## Conventions

- Follow [conventional commits](https://www.conventionalcommits.org) for commit messages
- Ruff handles all Python linting and formatting
- Template uses Sybil for doctest support in generated projects (configured in `project/conftest.py`)
