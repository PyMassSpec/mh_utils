# stdlib
import itertools
import random
from functools import lru_cache
from itertools import permutations
from typing import List

# 3rd party
import pytest
from _pytest.mark import MarkDecorator
from domdf_python_tools.testing import testing_boolean_values
from domdf_python_tools.iterative import Len

whitespace = " \t\n\r"


@lru_cache(1)
def whitespace_perms_list() -> List[str]:
	chain = itertools.chain.from_iterable(permutations(whitespace, n) for n in Len(whitespace))
	return list(''.join(x) for x in chain)


def whitespace_perms(ratio: float = 0.5) -> MarkDecorator:
	perms = whitespace_perms_list()
	return pytest.mark.parametrize("char", random.sample(perms, int(len(perms) * ratio)))


def count(stop: int, start: int = 0, step: int = 1) -> MarkDecorator:
	return pytest.mark.parametrize("count", range(start, stop, step))


true_false_strings = testing_boolean_values(extra_truthy=[-1]).mark.args[1]

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
