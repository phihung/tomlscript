import re
from dataclasses import dataclass
from typing import List, Optional

try:
    import tomllib
except ImportError:
    import tomli as tomllib


SCRIPT = "source"


class BashFunction:
    def __init__(self, name: str, code: Optional[str] = None, doc: Optional[str] = None):
        self.name = name
        self.code = code or name
        self.doc = doc

    def __repr__(self):  # pragma: no cover
        return f"BashFunction(name={self.name!r}, code={self.code!r}, doc={self.doc!r})"

    def __eq__(self, other):
        if not isinstance(other, BashFunction):  # pragma: no cover
            return NotImplemented
        return self.name == other.name and self.code == other.code and self.doc == other.doc

    @property
    def hidden(self):
        return self.name.endswith("_") or self.name.startswith("_")


@dataclass
class XRunConfig:
    script: str | None
    functions: list[BashFunction]

    def get(self, name) -> BashFunction:
        for x in self.functions:
            if x.name == name:
                return x
        return None


# Regex patterns
patterns_func_with_comment = re.compile(
    r"^#\s*(?P<doc>.*)\n\s*(function )?\s*(?P<func>[a-zA-Z\-_0-9]+)\(\)\s*{",
    re.MULTILINE,
)

pattern_func = re.compile(r"\s*(function )?\s*(?P<func>[a-zA-Z\-_0-9]+)\(\)\s*{")


def _extract_functions(script: str) -> List[BashFunction]:
    """Extract bash function names and documentation from the bash script."""
    functions = []

    # First, find all functions that have comments
    for match in patterns_func_with_comment.finditer(script):
        func_name = match.group("func")
        doc = match.group("doc")
        functions.append(BashFunction(name=func_name, doc=doc))

    # Then, find all functions without comments
    all_functions = {f.name for f in functions}  # Track functions with comments to avoid duplicates
    for match in pattern_func.finditer(script):
        func_name = match.group("func")
        if func_name not in all_functions:
            functions.append(BashFunction(name=func_name))

    return functions


def parse_cfg(pyproject_path) -> XRunConfig:
    """Parse the pyproject.toml file."""
    with open(pyproject_path, "rb") as f:
        cfg = tomllib.load(f).get("tool", {}).get("xrun", {})
    script = cfg.pop(SCRIPT, None)
    functions = []
    if script:
        functions = _extract_functions(script)
    if cfg:
        with open(pyproject_path, "r") as f:
            lines = f.readlines()
        for k, v in cfg.items():
            functions.append(BashFunction(name=k, code=v, doc=_find_doc(lines, k)))
    return XRunConfig(script=script, functions=functions)


def _find_doc(lines, func_name):
    for i, line in enumerate(lines):
        if line.startswith(f"{func_name} = ") and i > 0 and lines[i - 1].startswith("#"):
            return lines[i - 1].strip().lstrip("#").strip()
    return None
