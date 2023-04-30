from inspect import Signature, signature
from typing import Any, List, Optional


def generic_str(
    self: Any,
    ignored_keywords: Optional[List[str]] = None,
    explicit_keywords: Optional[List[str]] = None,
) -> str:
    newlines: bool = True
    newline_or_space: str = "\n" if newlines else " "
    newline_or_nothing: str = "\n" if newlines else ""
    string: str = f"{self.__class__.__name__}({newline_or_nothing}"
    dir: List[str] = []
    self_signature: Signature = signature(self.__init__)
    ignored_keywords = (ignored_keywords or []) + ["self"]
    for i in self_signature.parameters:
        if i not in ignored_keywords:
            dir.append(i)
    if explicit_keywords:
        for i in explicit_keywords:
            if i not in self_signature.parameters:
                dir.append(i)
    if dir:
        for i in dir:
            string += f'{"    " if newlines else ""}{i}='
            lines = repr(getattr(self, i)).splitlines()
            string += f"{lines.pop(0)}{newline_or_space}"
            for j in lines:
                string += f'{"    "}{j}{newline_or_space}'
            string = f"{string[:-1]},{newline_or_space}"
        string = string[:-1]
    return f"{string[:-1]}{newline_or_nothing})"
