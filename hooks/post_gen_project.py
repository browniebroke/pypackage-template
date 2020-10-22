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


def setup_github():
    """Create Github repo and set it up as remote."""
    if not check_command_exists("gh"):
        return

    # Init local repo
    run_cmd(["git", "init"])
    run_cmd(["git", "add", "."])

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
        ]
    )


def main():
    if "{{ cookiecutter.run_poetry_install }}" == "y":
        run_poetry_install()

    if "{{ cookiecutter.setup_github }}" == "y":
        setup_github()


if __name__ == "__main__":
    main()
