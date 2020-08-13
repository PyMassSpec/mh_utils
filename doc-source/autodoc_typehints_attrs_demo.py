# Demo for autodoc_typehints_attrs

# stdlib
from typing import Any, Dict, List, Tuple

# 3rd party
import attr
from autodoc_typehints_attrs import add_attrs_annotations


def my_converter(arg: List[Dict[str, Any]]):
	return arg


def untyped_converter(arg):
	return arg


@attr.s
class SomeClass:
	a_string: str = attr.ib(converter=str)
	custom_converter: Any = attr.ib(converter=my_converter)
	untyped: Tuple[str, int, float] = attr.ib(converter=untyped_converter)


add_attrs_annotations(SomeClass)

print(SomeClass.__init__.__annotations__)
