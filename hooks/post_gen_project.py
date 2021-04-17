import subprocess


def run_cmd(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def check_command_exists(cmd):
    try:
        run_cmd([cmd, "-h"], capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{cmd} command is not installed")
        return False
    return True


def run_poetry_install():
    if not check_command_exists("poetry"):
        return

    run_cmd(["poetry", "install"])


def initial_commit():
    # Init local repo
    run_cmd(["git", "init"])
    run_cmd(["git", "add", "."])
    run_cmd(["git", "commit", "-m", "'feat: initial commit'"])


def setup_github():
    """Create Github repo and set it up as remote."""
    if not check_command_exists("gh"):
        return

    # Create it on Github
    github_username = "{{ cookiecutter.github_username }}"
    project_slug = "{{ cookiecutter.project_slug }}"
    run_cmd(
        [
            "gh",
            "repo",
            "create",
            f"{github_username}/{project_slug}",
            "-y",
            "-d",
            "{{ cookiecutter.project_short_description }}",
            "--public",
            "--enable-wiki=false",
        ]
    )


def setup_pre_commit():
    if not check_command_exists("pre-commit"):
        return

    # Run pre-commit install
    run_cmd(["pre-commit", "install"])


def add_me_as_contributor():
    if not check_command_exists("npx"):
        return

    # Run pre-commit install
    run_cmd(
        [
            "npx",
            "all-contributors-cli",
            "add",
            "{{ cookiecutter.github_username }}",
            "code,ideas,doc",
        ]
    )


def main():
    if "{{ cookiecutter.run_poetry_install }}" == "y":
        run_poetry_install()

    if "{{ cookiecutter.initial_commit }}" == "y":
        initial_commit()

    if "{{ cookiecutter.setup_github }}" == "y":
        setup_github()

    if "{{ cookiecutter.setup_pre_commit }}" == "y":
        setup_pre_commit()

    if "{{ cookiecutter.add_me_as_contributor }}" == "y":
        add_me_as_contributor()


if __name__ == "__main__":
    main()
