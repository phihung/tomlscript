import re
from pathlib import Path

from inline_snapshot import snapshot

from tomlscript.main import _main


def test_example_1(tmp_path, capfd):
    block = get_toml_blocks_from_readme("publish")
    fn = tmp_path / "pyproject.toml"
    fn.write_text(block)
    _main(["-c", str(fn)])
    out, err = capfd.readouterr()
    assert out == snapshot("""\
\x1b[92mdev            \x1b[0m: Start dev server
\x1b[92mpublish        \x1b[0m: Publish to PyPI
""")
    assert err == ""


def test_example_2(tmp_path, capfd):
    block = get_toml_blocks_from_readme("say_")
    fn = tmp_path / "pyproject.toml"
    fn.write_text(block)
    _main(["-c", str(fn)])
    check_outerr(
        capfd,
        snapshot("""\
\x1b[92mdoc            \x1b[0m: Documentation for `doc` function
\x1b[92mhello          \x1b[0m: This line is the documentation for `hello` function
\x1b[92mtest           \x1b[0m: Lint and test\
"""),
    )

    _main(["-c", str(fn), "hello"])
    check_outerr(capfd, "Hello world")

    _main(["-c", str(fn), "doc"])
    check_outerr(capfd, "Rendering documentation...")


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
