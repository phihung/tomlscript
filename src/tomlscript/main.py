import argparse
import importlib
import os
import subprocess
import sys
import tempfile

from tomlscript import __version__
from tomlscript.parser import Function, XRunConfig, parse_cfg
from tomlscript.utils import parse_args


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
        if func := cfg.get(args.function):
            if func.is_pyfunc:
                _execute_python(cfg, func, args.args, debug=args.debug)
            else:
                _execute_shell(cfg, func, args.args, debug=args.debug)
        else:
            sys.stderr.write(f"Error: Function '{args.function}' not found.")
            return 1
    else:
        for x in cfg.functions:
            if not x.hidden:
                print(f"\033[92m{x.name:15s}\033[0m: {x.doc or ''}")
        return 0


def _execute_shell(cfg: XRunConfig, func: Function, args: list[str], debug: bool = False):
    args = [repr(x) for x in args]
    script = "".join([cfg.script or "", "\n", func.code, " ", " ".join(args)])

    if debug:
        print("---", script.strip(), "---", sep="\n")

    """Execute the specified function from the shell script."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as fd:
        fd.write(script)

    subprocess.run(["bash", fd.name])


def _execute_python(cfg: XRunConfig, func: Function, args: list[str], debug: bool = False):
    module_name, func_name = func.code.split(":")
    module = importlib.import_module(module_name)
    pyfunc = getattr(module, func_name)
    if not args:
        if debug:
            print("---", f"{func.code}()", "---", sep="\n")
        pyfunc()
    else:
        func_args = parse_args(pyfunc, args)
        if debug:
            print(
                "---",
                f"{func.code}({', '.join(f'{k}={v!r}' for k, v in func_args.items())})",
                "---",
                sep="\n",
            )
        pyfunc(**func_args)


if __name__ == "__main__":  # pragma: no cover
    main()
