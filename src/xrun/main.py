import argparse
import os
import subprocess
import sys
import tempfile
from typing import Optional

from xrun import __version__
from xrun.parser import XRunConfig, parse_cfg


def main(argv=sys.argv[1:]):
    code = _main(argv)
    sys.exit(code)


def _main(argv):
    return _run(_parse_args(argv))


def _parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Execute functions from pyproject.toml [tool.xrun]"
    )
    parser.add_argument("function", nargs="?", help="The function to execute")
    parser.add_argument(
        "-v", "--version", nargs="?", const=True, default=False, help="Print the current version"
    )
    parser.add_argument(
        "-c",
        "--config",
        default="pyproject.toml",
        help="Path to pyproject.toml (default is current directory)",
    )
    parser.add_argument("--debug", nargs="?", const=False, help="Run in debug mode")
    parser.add_argument("args", nargs=argparse.REMAINDER, default=[])

    return parser.parse_args(argv)


def _run(args):
    if args.version:
        print(__package__, __version__)
        return 0
    if not os.path.exists(args.config):
        sys.stderr.write(f"Error: {args.config} file not found.")
        return 1

    cfg = parse_cfg(args.config)

    if args.function:
        if script := _get_script(cfg, args.function, args.args):
            if args.debug:
                print("---")
                print(script)
                print("---")
            _execute(script)
        else:
            sys.stderr.write(f"Error: Function '{args.function}' not found.")
            return 1
    else:
        for x in cfg.functions:
            if not x.hidden:
                print(f"\033[92m{x.name:15s}\033[0m: {x.doc or ''}")
        return 0


def _get_script(cfg: XRunConfig, function: str, args: list[str]) -> Optional[str]:
    if func := cfg.get(function):
        args = [repr(x) for x in args]
        return "".join([cfg.script or "", "\n", func.code, " ", " ".join(args)])
    return None


def _execute(script):
    """Execute the specified function from the shell script."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as fd:
        fd.write(script)

    subprocess.run(["bash", fd.name])


if __name__ == "__main__":  # pragma: no cover
    main()
