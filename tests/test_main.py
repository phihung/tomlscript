import subprocess

import pytest
from inline_snapshot import snapshot

from tomlscript import __version__
from tomlscript.main import _main, main


def test_list_commands(capfd, pyproject):
    _main(["-c", pyproject])
    captured = capfd.readouterr()
    assert captured.out == snapshot("""\
\x1b[92mbar            \x1b[0m: echo
\x1b[92mfoo            \x1b[0m: foo-doc
\x1b[92mfoobar         \x1b[0m: echo a:b:c
\x1b[92mdev            \x1b[0m: uv run uvicorn --port 5001 superapp.main...
\x1b[92mpyfunc1        \x1b[0m: tests.myscript:run1
\x1b[92mpyfunc2        \x1b[0m: Say hello
""")
    assert captured.err == ""


def test_run_command(capfd, pyproject):
    _main(["-c", pyproject, "foo"])
    check_outerr(capfd, ":111")

    _main(["-c", pyproject, "foobar"])
    check_outerr(capfd, "a:b:c")


def test_run_command_with_args(capfd, pyproject):
    _main(["-c", pyproject, "bar", "hello 'world'"])
    check_outerr(capfd, "hello 'world'")


def test_run_command_with_debug(capfd, pyproject):
    _main(["-c", pyproject, "--debug", "1", "bar", "hello 'world'"])
    out, err = capfd.readouterr()
    assert out == snapshot("""\
---
echo "hello 'world'"
---
hello 'world'
""")
    assert err == ""

    _main(["-c", pyproject, "--debug", "1", "pyfunc1"])
    check_outerr(
        capfd,
        snapshot("""\
---
tests.myscript:run1()
---
Execute run1\
"""),
    )

    _main(["-c", pyproject, "--debug", "1", "pyfunc2", "--name", "Paul"])
    check_outerr(
        capfd,
        snapshot("""\
---
tests.myscript:run2(name='Paul', value=3.14)
---
Hello Paul. The value is 3.14\
"""),
    )


def test_run_python(capfd, pyproject):
    _main(["-c", pyproject, "pyfunc1"])
    check_outerr(capfd, "Execute run1")

    _main(["-c", pyproject, "pyfunc2", "--name", "Jean"])
    check_outerr(capfd, "Hello Jean. The value is 3.14")


def test_run_python_cwd(capfd, pyproject):
    o = subprocess.check_output(["tom", "-c", pyproject, "pyfunc1"])
    assert "Execute run1" == o.decode().strip()


def test_run_command_unknown(capfd, pyproject):
    _main(["-c", pyproject, "unknown"])
    check_outerr(capfd, "", snapshot("Error: Function 'unknown' not found."))


def test_run_command_config_not_exists(capfd):
    _main(["-c", "blah.toml"])
    check_outerr(capfd, "", snapshot("Error: blah.toml file not found."))


def test_version(capfd):
    try:
        main(["--version"])
        assert False
    except SystemExit as e:
        assert e.code == 0
        check_outerr(capfd, f"tomlscript {__version__}")


def test_help(capfd):
    try:
        main(["--help"])
        assert False
    except SystemExit as e:
        assert e.code == 0
        assert "functions" in capfd.readouterr().out


@pytest.fixture
def pyproject(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""
[tool.tomlscript]
bar = 'echo'
# foo-doc
foo = "echo :111"
foobar = "echo a:b:c"
                         
dev = "uv run uvicorn --port 5001 superapp.main:app --reload"

pyfunc1 = "tests.myscript:run1"
                         
# Say hello
pyfunc2 = "tests.myscript:run2"
""")
    yield str(pyproject)


def check_outerr(capfd, out, err=""):
    out_, err_ = capfd.readouterr()
    assert err_ == err
    assert out_.strip() == out
