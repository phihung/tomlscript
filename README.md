# Tomlscript

A lightweight, dependency-free tool to manage your scripts directly from pyproject.toml

<div style="display: flex; justify-content: space-between;align-items: center;">
  <div style="width: 30%;">

**Usage**

```bash
# List commands
tom

# Run a command
tom publish
tom dev
tom pyi



```

  </div>
  <div style="width: 65%;">

**Example Configuration**

```toml
# pyproject.toml
[tool.tomlscript]
# Start dev server
dev = "uv run uvicorn --port 5001 superapp.main:app --reload"

# Publish to PyPI
publish = "rm -rf dist && uv build && uvx twine upload dist/*"

# Generate pyi stubs (python function)
pyi = "mypackage.typing:generate_pyi"
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
# alias tom = "uv run tom"
tom
tom function
tom function arg1 --k2 v2
```

**Using uv / uvx**

```bash
uvx tomlscript
uvx tomlscript function arg1 --k2 v2

uv run tom
uv run tom function arg1 --k2 v2
```

## Configuration

For real world examples, see [pyproject.toml](./pyproject.toml) file.

```toml
[tool.tomlscript]
# This line is the documentation for `hello` function
hello = 'say_ "Hello world"'

# Run python function run2 from tests.myscript module
run2 = "tests.myscript:run2"

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

## Development

```bash
# Install dependencies
uv sync
alias tom="uv run tom"

# List the commands
tom
```
