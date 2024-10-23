import pytest
from inline_snapshot import snapshot

from tomlscript.parser import Function, parse_cfg


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
            Function(name="say", code="say", doc="Say somethings"),
            Function(name="bar", code="bar", doc="bar"),
            Function(name="foo", code="say 'FOO'", doc="say 'FOO'"),
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
bar = "say '{msg: BAR }'"
""")
    out = parse_cfg(cfg_file)
    assert out.functions == snapshot(
        [
            Function(name="foo", code="say 'FOO'", doc="say 'FOO'"),
            Function(name="bar", code="say '{msg: BAR }'", doc="super bar"),
        ]
    )
    assert out.script is None


def test_parse_cfg_3(tmp_path):
    cfg_file = tmp_path / "test.toml"
    cfg_file.write_text("foo = 'say FOO'")
    out = parse_cfg(cfg_file)
    assert out.functions == []
    assert out.script is None


@pytest.mark.parametrize(
    "code,exp",
    [
        ("say 'FOO'", {}),
        ("say '{msg: FOO }'", {"msg": " FOO "}),
        ("say '{msg:a:b:c}'", {"msg": "a:b:c"}),
        ("uvicorn run main:app --port {port}", {"port": None}),
        ("uvicorn run main:app --port {port:1234}", {"port": "1234"}),
        ("uvicorn run main:app --reload {reload:1} --port {port}", {"port": None, "reload": "1"}),
    ],
)
def test_variables(code, exp):
    func = Function(name="foo", code=code)
    assert func.variables == exp
