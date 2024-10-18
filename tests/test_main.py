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
    out, err = capfd.readouterr()
    assert out.strip() == "111"
    assert err == ""


def test_run_command_with_args(capfd, pyproject):
    _main(["-c", str(pyproject), "bar", "hello 'world'"])
    out, err = capfd.readouterr()
    assert out.strip() == "hello 'world'"
    assert err == ""


def test_run_command_unknown(capfd, pyproject):
    _main(["-c", str(pyproject), "unknown"])
    out, err = capfd.readouterr()
    assert out == ""
    assert err.strip() == snapshot("Error: Function 'unknown' not found.")


def test_run_command_config_not_exists(capfd):
    _main(["-c", "blah.toml"])
    out, err = capfd.readouterr()
    assert out == ""
    assert err.strip() == snapshot("Error: blah.toml file not found.")


def test_version(capfd):
    try:
        main(["--version"])
        assert False
    except SystemExit as e:
        assert e.code == 0
        out, err = capfd.readouterr()
        assert out.strip() == f"xrun {__version__}"
        assert err == ""


@pytest.fixture
def pyproject(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""
[tool.xrun]
bar = 'echo "$1"'
# foo-doc
foo = "echo 111"
""")
    yield pyproject
