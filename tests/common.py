# stdlib
from itertools import chain, permutations
from pathlib import PureWindowsPath
from typing import Any, Iterable

# 3rd party
import pytest

# this package
from mh_utils.utils import as_path, camel_to_snake, element_to_bool

whitespace = " \t\n\r"


def double_chain(iterable: Iterable[Iterable]):
	yield from chain.from_iterable(chain.from_iterable(iterable))


class Len(Iterable[int]):
	"""
	Shorthand for ``range(len(obj))``

	:param obj: The object to iterate over the length of
	:param start: The start value of the range.
	:param step: The step of the range.
	"""

	def __init__(self, obj: Any, start: int = 0, step: int = 1):
		self._members = range(start, len(obj), step)

	def __iter__(self):
		yield from self._members


whitespace_perms = pytest.mark.parametrize(
		"char", "".join(double_chain(permutations(whitespace, n) for n in Len(whitespace)))
		)

counts = pytest.mark.parametrize("count", range(0, 100))

true_false_strings = [
		(True, True),
		("True", True),
		("true", True),
		("tRUe", True),
		('y', True),
		('Y', True),
		("YES", True),
		("yes", True),
		("Yes", True),
		("yEs", True),
		("ON", True),
		("on", True),
		('1', True),
		(1, True),
		(-1, True),
		(False, False),
		("False", False),
		("false", False),
		("falSE", False),
		('n', False),
		('N', False),
		("NO", False),
		("no", False),
		("nO", False),
		("OFF", False),
		("off", False),
		("oFF", False),
		('0', False),
		(0, False),
		]

_test_strings = [
		("foo", "foo"),
		(True, "True"),
		(False, "False"),
		(None, "None"),
		(1234, "1234"),
		(12.34, "12.34"),
		]


def any_type_parametrize():
	return pytest.mark.parametrize(
			f"value, expects", [
					("foo", "foo"),
					(1234, 1234),
					(12.34, 12.34),
					(True, True),
					]
			)
