# XRUN

A tiny tool (no dependency!) to manage your scripts directly from [pyproject.toml]()

<div style="display: flex; justify-content: space-between;align-items: center;">
  <div style="width: 40%;">

```bash
# List commands
xrun

# Run a command
xrun publish
xrun dev

```

  </div>
  <div style="width: 55%;">

```toml
# pyproject.toml
[tool.xrun]
# Start dev server
dev = "uv run uvicorn --port 5001 superapp.main:app --reload"

# Publish pypi package
publish = "rm -rf dist && uv build && uvx twine upload dist/*"
```

  </div>
</div>

## Install

```bash
pip install xrun
uv add --dev xrun
```

## Run

**Directly**

```bash
xrun
xrun function
xrun function arg1 --k2 v2
```

**With uv / uvx**

```bash
uvx xrun
uvx xrun function arg1 --k2 v2

uv run xrun
uv run xrun function arg1 --k2 v2
```

## Configuration

```toml
[tool.xrun]
source = """
# Build and render documentation
doc() {
    echo "Rendering documentation..."
    # quarto render docs --execute
}

# Rebuild docker image
docker_dev() {
    docker build -t ....
    docker run --rm ...
}

say() {
    echo "$1"
}
"""

# Say something nice
foo = 'say'
```
