import argparse
import inspect
import re
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


# Regular expression pattern to match placeholders in the template
# Support: {name} and {name:default}
patterns_variable_template = re.compile(r"\{(\w+)(?::([^\}]+))?\}")


def extract_placeholders(template: str) -> dict[str, str | None]:
    return {
        match.group(1): match.group(2) for match in patterns_variable_template.finditer(template)
    }


def resolve_template(code: str, variables: dict[str, str | None], args: list[str]) -> str:
    parser = argparse.ArgumentParser(description="Script")
    for name, default in variables.items():
        if default is None:
            parser.add_argument(f"--{name}", required=True)
        else:
            parser.add_argument(f"--{name}", default=default)

    values = vars(parser.parse_args(args))

    def replacer(match):
        arg_name = match.group(1)
        return values[arg_name]

    # Substitute the placeholders with the values from argparse
    return patterns_variable_template.sub(replacer, code)
