import argparse
import inspect
from typing import Any


def parse_args(func: Any, args: list[str]) -> dict:
    parser = argparse.ArgumentParser(description=func.__name__)
    signature = inspect.signature(func)
    for name, param in signature.parameters.items():
        arg_type = param.annotation if param.annotation != param.empty else str
        if param.default == param.empty:
            parser.add_argument(f"--{name}", required=True, type=arg_type)
        else:
            parser.add_argument(f"--{name}", default=param.default, type=arg_type)

    return vars(parser.parse_args(args))
