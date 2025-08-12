# Tomlscript

[![codecov](https://codecov.io/gh/phihung/tomlscript/branch/main/graph/badge.svg)](https://codecov.io/gh/phihung/tomlscript)

**Run and manage project scripts straight from `pyproject.toml` — no extra dependencies, no fuss.**

---

## 🚀 Quick Example

**1. Define commands in `pyproject.toml`:**

```toml
[tool.tomlscript]
# Start dev server
dev = "uv run uvicorn --port {port:5000} superapp.main:app --reload"

# Run tests
test = """
uv run ruff check
uv run pytest
"""
```

**2. Run them instantly (no install needed):**

```bash
alias tom="uvx tomlscript"

tom dev              # defaults to port 5000
tom dev --port 8001  # override port
tom test
tom                  # list all commands
```

Done. No custom scripts folder, no Makefile, no shell-specific quirks.

---

## ⚙️ Features in Action

### Arguments with Defaults

```toml
[tool.tomlscript]
# Start dev server (default port 5001)
dev = "uv run uvicorn --port {port:5001} superapp.main:app --reload"
```

```bash
tom dev              # → port 5001
tom dev --port 8000
```

### Python Functions as Commands

```toml
[tool.tomlscript]
hello = "mypackage.scripts:say_hello"
```

```bash
tom hello --name Alice
```

### Multi-line Scripts

```toml
[tool.tomlscript]
test = """
uv run ruff check
uv run pytest
"""
```

### Shared Helpers

```toml
[tool.tomlscript]
build = "clean && uv build"

source = """
clean() {
  echo "Cleaning..."
  rm -rf dist build *.egg-info
}
"""
```

For a full working setup, see [pyproject.toml](./pyproject.toml).

---

## 🛠 Development

```bash
tom setup_dev   # setup dev environment
tom test        # run tests with coverage
tom publish     # build + upload to PyPI
```
