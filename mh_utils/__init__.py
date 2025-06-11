#!/usr/bin/env python3
#
#  __init__.py
"""
Utilities for handing ancillary files produced by MassHunter.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from abc import abstractmethod
from typing import Dict, Iterable, Iterator, Tuple, TypeVar

# 3rd party
from domdf_python_tools._is_match import is_match_with
from domdf_python_tools.doctools import prettify_docstrings

__all__ = ["Dictable"]

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020-2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.2.2"
__email__: str = "dominic@davis-foster.co.uk"

_V = TypeVar("_V")


@prettify_docstrings
class Dictable(Iterable[Tuple[str, _V]]):
	"""
	The basic structure of a class that can be converted into a dictionary.
	"""

	@abstractmethod
	def __init__(self, *args, **kwargs):
		pass

	def __repr__(self) -> str:
		return super().__repr__()

	def __str__(self) -> str:
		return self.__repr__()

	def __iter__(self) -> Iterator[Tuple[str, _V]]:
		"""
		Iterate over the attributes of the class.
		"""

		yield from self.to_dict().items()

	def __getstate__(self) -> Dict[str, _V]:
		return self.to_dict()

	def __setstate__(self, state):
		self.__init__(**state)  # type: ignore[misc]

	def __copy__(self):
		return self.__class__(**self.to_dict())

	def __deepcopy__(self, memodict={}):
		return self.__copy__()

	@abstractmethod
	def to_dict(self):
		"""
		Return a dictionary representation of the class.
		"""

		return {}  # pragma: no cover (abc)

	def __eq__(self, other) -> bool:
		if isinstance(other, self.__class__):
			return is_match_with(other.to_dict(), self.to_dict())

		return NotImplemented
