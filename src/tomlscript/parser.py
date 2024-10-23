import importlib
import os
import re
import sys
from dataclasses import dataclass
from typing import List, Optional

from tomlscript import utils

try:
    import tomllib
except ImportError:
    import tomli as tomllib

SCRIPT = "source"


class Function:
    def __init__(self, name: str, code: Optional[str] = None, doc: Optional[str] = None):
        self.name = name
        self.code = code or name
        self.doc = doc or _shorten(self.code)

    def __repr__(self):  # pragma: no cover
        return f"Function(name={self.name!r}, code={self.code!r}, doc={self.doc!r})"

    def __eq__(self, other):
        if not isinstance(other, Function):  # pragma: no cover
            return NotImplemented
        return self.name == other.name and self.code == other.code and self.doc == other.doc

    @property
    def variables(self) -> dict[str, str | None]:
        return utils.extract_placeholders(self.code)

    @property
    def hidden(self):
        return self.name.endswith("_") or self.name.startswith("_")

    @property
    def is_pyfunc(self):
        if len(self.code) > 100 or "\n" in self.code or ":" not in self.code:
            return False
        parts = self.code.split(":")
        if len(parts) != 2:
            return False
        if os.getcwd() not in sys.path:
            sys.path.append(os.getcwd())
        try:
            module = importlib.import_module(parts[0])
        except ImportError:
            return False
        return hasattr(module, parts[1])


def _shorten(x: str, n: int = 40) -> str:
    x = x.replace("\n", " ")
    if len(x) < n:
        return x
    return x[:n] + "..."


@dataclass
class XRunConfig:
    script: str | None
    functions: list[Function]

    def get(self, name) -> Function:
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


def _extract_functions(script: str) -> List[Function]:
    """Extract bash function names and documentation from the bash script."""
    functions = []

    # First, find all functions that have comments
    for match in patterns_func_with_comment.finditer(script):
        func_name = match.group("func")
        doc = match.group("doc")
        functions.append(Function(name=func_name, doc=doc))

    # Then, find all functions without comments
    all_functions = {f.name for f in functions}  # Track functions with comments to avoid duplicates
    for match in pattern_func.finditer(script):
        func_name = match.group("func")
        if func_name not in all_functions:
            functions.append(Function(name=func_name))

    return functions


def parse_cfg(pyproject_path) -> XRunConfig:
    """Parse the pyproject.toml file."""
    with open(pyproject_path, "rb") as f:
        cfg = tomllib.load(f).get("tool", {}).get("tomlscript", {})
    script = cfg.pop(SCRIPT, None)
    functions = []
    if script:
        functions = _extract_functions(script)
    if cfg:
        with open(pyproject_path, "r") as f:
            lines = f.readlines()
        for k, v in cfg.items():
            functions.append(Function(name=k, code=v, doc=_find_doc(lines, k)))
    return XRunConfig(script=script, functions=functions)


def _find_doc(lines, func_name):
    for i, line in enumerate(lines):
        if line.startswith(f"{func_name} = ") and i > 0 and lines[i - 1].startswith("#"):
            return lines[i - 1].strip().lstrip("#").strip()
    return None
