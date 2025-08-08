# Tomlscript

[![codecov](https://codecov.io/gh/phihung/tomlscript/branch/main/graph/badge.svg)](https://codecov.io/gh/phihung/tomlscript)

A lightweight, dependency-free tool to manage your scripts directly from pyproject.toml

<div style="display: flex; justify-content: space-between;align-items: center;">
  <div style="width: 30%;">

**Usage**

```bash
# alias tom = "uvx tomlscript"
# List commands
tom

# Run a command
tom dev --port 8000
tom publish
tom pyi


```

  </div>
  <div style="width: 65%;">

**Example Configuration**

```toml
# pyproject.toml
[tool.tomlscript]
# Start dev server (default on port 5001)
dev = "uv run uvicorn --port {port:5001} superapp.main:app --reload"

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

# Or better, run it directly with uvx without installation
# And use it to setup other dependencies
alias tom = "uvx tomlscript"
tom # List commands
tom setup_dev  # Run command to setup dev env
```

## Running Commands

**Directly**

```bash
# alias tom = "uvx tomlscript"
tom
tom function
tom function v1 --arg2 v2
```

**Using uv**

```bash
uv run tom
uv run tom function v1 --arg2 v2
```

## Configuration

### Basic

Commands are defined in the `[tool.tomlscript]` section of the `pyproject.toml` file.

The comment above a command serves as its documentation.

```toml
[tool.tomlscript]
# Linter check <= this line is the documentation for `lint` command
lint = "uv run ruff check"
```

Commands can be multi-line scripts:

```toml
[tool.tomlscript]
# Lint and test
test = """
uv run ruff check
uv run pytest
"""
```

You can define commands with arguments using the `{arg}` or `{arg:default}` syntax:

```toml
[tool.tomlscript]
# Start dev server (default on port 5001)
dev = "uv run uvicorn --port {port:5001} superapp.main:app --reload"
```

The above command can be used as

```bash
tom dev              # run on port 5001
tom dev --port 8000  # run on port 8000
```

You can also define commands as Python functions using the `module:function` syntax:

```toml
[tool.tomlscript]
# Run python function run2 from [tests.myscript module](./tests/myscript.py)
py_example = "tests.myscript:run2"
```

Arguments can be passed to Python functions:

```bash
tom py_example --name Paul
```

For complex shell scripts, you can use the `[tool.tomlscript.source]` section. Functions defined here can be reused across multiple commands:

```toml
[tool.tomlscript]
build = "clean && uv build"

source = """
# Clean up
clean() {
  say_ "Cleaning up..."
  rm -rf dist .eggs *.egg-info build
}

# Functions ending with _ are hidden from the command list
say_() {
  echo "$1"
}
"""
```

### Full example

For real world examples, see [development section](#development) and [pyproject.toml](./pyproject.toml) file.

```toml
[tool.tomlscript]
# This line is the documentation for `hello` function
hello = 'say_ "Hello world"'

# Run python function run2 from tests.myscript module
run2 = "tests.myscript:run2"

# A command with arguments and default values
dev = "uv run uvicorn --port {port:5001} superapp.main:app"

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

# Functions ending with _ are hidden from the command list
say_() {
  echo "$1"
}
"""
```

## Development

```bash
alias tom="uvx tomlscript"
tom
# setup_dev      : Setup dev env
# test           : Run tests with coverage
# publish        : Publish pypi package
# cov            : Open Cov report
# example        : Execute a simple python function

# Setup dev enviroment
tom setup_dev
```
