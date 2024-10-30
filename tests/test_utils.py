from enum import Enum

import pytest

from tomlscript import utils


def test_parse_args_for_python(capfd):
    assert utils.parse_args_for_python(func1, "--a y --b 2 --c 3 --d 4".split()) == dict(
        a=True, b=2, c="3", d=4.0, e=[], f={}
    )

    try:
        utils.parse_args_for_python(func1, "--a y --b 2 --c 3".split())
    except SystemExit as e:
        assert e.code == 2
        assert "required: --d" in capfd.readouterr().err.strip()


@pytest.mark.parametrize(
    "arg, expected",
    [
        ("y", True),
        ("n", False),
        ("yes", True),
        ("no", False),
        ("true", True),
        ("false", False),
        ("True", True),
        ("False", False),
        ("1", True),
        ("0", False),
    ],
)
def test_parse_args_for_python_bool(arg: str, expected: bool):
    assert utils.parse_args_for_python(func2, f"--a {arg}".split()) == dict(a=expected)


def test_parse_args_for_python_bool_error():
    with pytest.raises(SystemExit):
        utils.parse_args_for_python(func2, "--a maybe".split())


def test_parse_args_for_python_enum():
    assert utils.parse_args_for_python(func3, "--a red".split()) == dict(a=Color.RED)

    with pytest.raises(SystemExit):
        utils.parse_args_for_python(func3, "--a green".split())


def func1(a: bool, b: int, c: str, d: float, e: list[str] = [], f: dict = {}):
    pass


def func2(a: bool):
    pass


class Color(Enum):
    RED = "red"
    BLUE = "blue"


def func3(a: Color):
    pass
