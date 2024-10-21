from inline_snapshot import snapshot

from tomlscript.parser import BashFunction, parse_cfg


def test_parse_cfg(tmp_path):
    cfg_file = tmp_path / "test.toml"
    src = """\
# Say somethings
say() {
    echo "$1"
}

function bar() {
    echo "BAR"
}
"""
    cfg_file.write_text(f"""
[tool.tomlscript]
foo = "say 'FOO'"

source = '''
{src}
'''
""")
    out = parse_cfg(cfg_file)
    assert out.functions == snapshot(
        [
            BashFunction(name="say", code="say", doc="Say somethings"),
            BashFunction(name="bar", code="bar", doc=None),
            BashFunction(name="foo", code="say 'FOO'", doc=None),
        ]
    )
    assert out.script.strip() == src.strip()

    for x in out.functions:
        assert out.get(x.name) == x
    assert out.get("aaa") is None


def test_parse_cfg_2(tmp_path):
    cfg_file = tmp_path / "test.toml"
    cfg_file.write_text("""
[tool.tomlscript]
foo = "say 'FOO'"
# super bar
bar = "say 'BAR'"
""")
    out = parse_cfg(cfg_file)
    assert out.functions == snapshot(
        [
            BashFunction(name="foo", code="say 'FOO'", doc=None),
            BashFunction(name="bar", code="say 'BAR'", doc="super bar"),
        ]
    )
    assert out.script is None


def test_parse_cfg_3(tmp_path):
    cfg_file = tmp_path / "test.toml"
    cfg_file.write_text("foo = 'say FOO'")
    out = parse_cfg(cfg_file)
    assert out.functions == []
    assert out.script is None
