from {{ cookiecutter.package_name }} import add


def test_add():
    assert add(1, 1) == 2
