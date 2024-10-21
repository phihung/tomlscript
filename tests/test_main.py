import pytest
from inline_snapshot import snapshot

from xrun import __version__
from xrun.main import _main, main


def test_list_commands(capfd, pyproject):
    _main(["-c", str(pyproject)])
    captured = capfd.readouterr()
    assert captured.out == snapshot("""\
\x1b[92mbar            \x1b[0m: 
\x1b[92mfoo            \x1b[0m: foo-doc
""")
    assert captured.err == ""


def test_run_command(capfd, pyproject):
    _main(["-c", str(pyproject), "foo"])
    check_outerr(capfd, "111")


def test_run_command_with_args(capfd, pyproject):
    _main(["-c", str(pyproject), "bar", "hello 'world'"])
    check_outerr(capfd, "hello 'world'")


def test_run_command_with_debug(capfd, pyproject):
    _main(["-c", str(pyproject), "--debug", "1", "bar", "hello 'world'"])
    out, err = capfd.readouterr()
    assert out == snapshot("""\
---

echo "hello 'world'"
---
hello 'world'
""")
    assert err == ""


def test_run_command_unknown(capfd, pyproject):
    _main(["-c", str(pyproject), "unknown"])
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
        check_outerr(capfd, f"xrun {__version__}")


@pytest.fixture
def pyproject(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""
[tool.xrun]
bar = 'echo'
# foo-doc
foo = "echo 111"
""")
    yield pyproject


def check_outerr(capfd, out, err=""):
    out_, err_ = capfd.readouterr()
    assert out_.strip() == out
    assert err_ == err
