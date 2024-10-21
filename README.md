# XRUN

A lightweight, dependency-free tool to manage your scripts directly from pyproject.toml

<div style="display: flex; justify-content: space-between;align-items: center;">
  <div style="width: 40%;">

**Usage**

```bash
# List commands
xrun

# Run a command
xrun publish
xrun dev

```

  </div>
  <div style="width: 55%;">

**Example configuration**

```toml
# pyproject.toml
[tool.tomlscript]
# Start dev server
dev = "uv run uvicorn --port 5001 superapp.main:app --reload"

# Publish to PyPI
publish = "rm -rf dist && uv build && uvx twine upload dist/*"
```

  </div>
</div>

## Installation

```bash
pip install tomlscript
uv add --dev tomlscript
```

## Running Commands

**Directly**

```bash
xrun
xrun function
xrun function arg1 --k2 v2
```

**Using uv / uvx**

```bash
uvx xrun
uvx xrun function arg1 --k2 v2

uv run xrun
uv run xrun function arg1 --k2 v2
```

## Configuration

For real world examples, see [pyproject.toml](./pyproject.toml) file.

```toml
[tool.tomlscript]
# This line is the documentation for `hello` function
hello = 'say_ "Hello world"'

# Lint and test
test = """
uv run ruff check
uv run pytest --inline-snapshot=review
"""

# Define multiple functions in the `[tool.tomlscript.source]` sections
source = """
# Documentation for `doc` function
doc() {
  say_ "Rendering documentation..."
}

# Functions end with _ will not show in the list
say_() {
  echo "$1"
}
"""
```
