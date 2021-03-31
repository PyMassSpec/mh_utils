#!/usr/bin/env python
#
#  utils.py
"""
General utility functions.
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
#  camel_to_snake based on https://stackoverflow.com/a/1176023/3092681
#  CC BY-SA 4.0
#

# stdlib
import datetime
import pathlib
import re
from typing import Any, Optional, Union

# 3rd party
from domdf_python_tools.utils import strtobool

__all__ = [
		"as_path",
		"element_to_bool",
		"camel_to_snake",
		"strip_string",
		"make_timedelta",
		]


def as_path(val: Any) -> Optional[pathlib.PureWindowsPath]:
	"""
	Returns ``val`` as a :class:`~pathlib.PureWindowsPath`,
	or :py:obj:`None` if the value is empty/:py:obj:`None`/:py:obj:`False`.

	:param val: The value to convert to a path
	"""  # noqa: D400

	if not val:
		return None

	val = str(val).strip()

	if val:
		return pathlib.PureWindowsPath(val)
	else:
		return None


def element_to_bool(val: Union[str, bool]) -> bool:
	"""
	Returns the boolean representation of ``val``.

	Values of ``-1`` are counted as :py:obj:`True` for the purposes of this function.

	:py:obj:`True` values are ``'y'``, ``'yes'``, ``'t'``, ``'true'``, ``'on'``, ``'1'``, ``1``, ``-1``, and ``'-1'``.

	:py:obj:`False` values are ``'n'``, ``'no'``, ``'f'``, ``'false'``, ``'off'``, ``'0'``, and ``0``.

	:raises: :py:exc:`ValueError` if 'val' is anything else.
	"""

	val = str(val).strip()
	if val == "-1":
		return True
	else:
		return bool(strtobool(val))


def camel_to_snake(name: str) -> str:
	"""
	Convert ``name`` from ``CamelCase`` to ``snake_case``.

	:param name: The ``CamelCase`` string to convert to ``snake_case``.
	"""

	name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
	name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
	return name.lower()


def strip_string(val: str) -> str:
	"""
	Returns ``val`` as a string, without any leading or trailing whitespace.

	:param val:
	"""

	return str(val).strip()


def make_timedelta(minutes: Union[float, datetime.timedelta]) -> datetime.timedelta:
	"""
	Construct a timedelta from a value in minutes.

	:param minutes:

	:rtype:

	.. versionchanged:: 0.1.0

		Moved from :mod:`mh_utils.cef_parser`.
	"""

	if not isinstance(minutes, datetime.timedelta):
		minutes = datetime.timedelta(minutes=float(minutes))

	return minutes
