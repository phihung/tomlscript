import re
from pathlib import Path
from unittest.mock import patch

from inline_snapshot import snapshot

from tomlscript.main import _main


@patch("subprocess.run")
def test_example_1(mock, tmp_path, capfd):
    block = get_toml_blocks_from_readme("publish")
    fn = tmp_path / "pyproject.toml"
    fn.write_text(block)

    _main(["-c", str(fn)])
    check_outerr(
        capfd,
        snapshot("""\
\x1b[92mdev            \x1b[0m: Start dev server (default on port 5001)
\x1b[92mpublish        \x1b[0m: Publish to PyPI
\x1b[92mpyi            \x1b[0m: Generate pyi stubs (python function)\
"""),
    )

    _main(["-c", str(fn), "dev"])
    mock.assert_called_once_with(
        "uv run uvicorn --port 5001 superapp.main:app --reload", shell=True
    )

    mock.reset_mock()
    _main(["-c", str(fn), "dev", "--port", "8000"])
    mock.assert_called_once_with(
        "uv run uvicorn --port 8000 superapp.main:app --reload", shell=True
    )


def test_example_2(tmp_path, capfd):
    block = get_toml_blocks_from_readme("Rendering documentation")
    fn = tmp_path / "pyproject.toml"
    fn.write_text(block)
    _main(["-c", str(fn)])
    check_outerr(
        capfd,
        snapshot("""\
\x1b[92mdoc            \x1b[0m: Documentation for `doc` function
\x1b[92mhello          \x1b[0m: This line is the documentation for `hello` function
\x1b[92mrun2           \x1b[0m: Run python function run2 from tests.myscript module
\x1b[92mdev            \x1b[0m: A command with arguments and default values
\x1b[92mtest           \x1b[0m: Lint and test\
"""),
    )

    _main(["-c", str(fn), "hello"])
    check_outerr(capfd, "Hello world")

    _main(["-c", str(fn), "doc"])
    check_outerr(capfd, "Rendering documentation...")

    _main(["-c", str(fn), "--debug", "1", "doc"])
    assert "Rendering documentation..." in capfd.readouterr().out


def test_all(tmp_path, capfd):
    fn = Path("README.md")
    blocks = re.findall(r"^```toml\n(.*?)\n```", fn.read_text(), re.MULTILINE | re.DOTALL)
    for block in blocks:
        fn = tmp_path / "pyproject.toml"
        fn.write_text(block)
        _main(["-c", str(fn)])
        assert capfd.readouterr().err == ""


def get_toml_blocks_from_readme(substr: str):
    fn = Path("README.md")
    blocks = re.findall(r"^```toml\n(.*?)\n```", fn.read_text(), re.MULTILINE | re.DOTALL)
    for block in blocks:
        if substr in block:
            return block
    raise ValueError(f"No block found containing {substr!r}")


def check_outerr(capfd, out, err=""):
    out_, err_ = capfd.readouterr()
    assert out_.strip() == out
    assert err_ == err
