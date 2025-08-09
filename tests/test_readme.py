import re
from pathlib import Path
from unittest.mock import patch

from inline_snapshot import snapshot

from tomlscript.main import _main


@patch("subprocess.run")
def test_readme_example_1(mock, tmp_path, capfd):
    block = get_toml_blocks_from_readme("Start dev server")
    fn = tmp_path / "pyproject.toml"
    fn.write_text(block)

    _main(["-c", str(fn)])
    check_outerr(
        capfd,
        snapshot(
            """\
\x1b[92mdev            \x1b[0m: Start dev server
\x1b[92mtest           \x1b[0m: Run tests\
"""
        ),
    )

    _main(["-c", str(fn), "dev"])
    mock.assert_called_once_with(
        "uv run uvicorn --port 5000 superapp.main:app --reload", shell=True
    )

    mock.reset_mock()
    _main(["-c", str(fn), "dev", "--port", "8001"])
    mock.assert_called_once_with(
        "uv run uvicorn --port 8001 superapp.main:app --reload", shell=True
    )


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
