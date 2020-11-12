import subprocess


def run_cmd(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def run_poetry_install():
    try:
        run_cmd(["poetry", "-h"], capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("poetry command is not installed")
        return

    run_cmd(["poetry", "install"])


def main():
    if "{{ cookiecutter.run_poetry_install }}" == "y":
        run_poetry_install()


if __name__ == "__main__":
    main()
