from functools import wraps
from typing import Any, Callable

from lark import Lark, Token, Tree

from ..utils import clean_type


def ast_to_str(node: Tree | Token | None, is_root: bool = False) -> str:
    if node is None:
        return ''

    if isinstance(node, Tree):
        rule_name = clean_type(node.data)
        children_strs = [
            ast_to_str(child)
            for child in node.children
            if child is not None
        ]

        ENTRYPOINTS = {"start", "file_input", "single_input", "eval_input"}
        if is_root and rule_name in ENTRYPOINTS:
            return ", ".join(children_strs)

        if not children_strs:
            return rule_name

        return f"{rule_name}({', '.join(children_strs)})"

    if isinstance(node, Token):
        return str(node.value)

    return str(node)


def assert_ast_structure(start: str = "file_input", crop_root: bool = True) -> Callable[..., Any]:
    need_format = start != "eval_input"

    def decorator(func: Callable[..., None]) -> Callable[..., None]:
        @wraps(func)
        def wrapper(moon_parser: Lark, source: str, *args: Any, **kwargs: Any) -> None:
            if need_format and not source.endswith('\n'):
                source += '\n'

            expected_ast: str = kwargs.get("expected_ast", args[0] if args else None)
            
            if expected_ast is None:
                raise ValueError(f"Test for source '{source}' did not provide an 'expected_ast'.")

            tree: Tree = moon_parser.parse(source, start=start)
            actual_ast = ast_to_str(tree, is_root=crop_root)

            assert actual_ast == expected_ast, (
                f"\nIncorrect AST structure for '{source}' (start='{start}')\n"
                f"Expected : {expected_ast}\n"
                f"Got      : {actual_ast}"
            )

            return func(moon_parser, source, *args, **kwargs)
        return wrapper
    return decorator