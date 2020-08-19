#!/usr/bin/env python
#
#  utils.py
"""
General utility functions.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  camel_to_snake based on https://stackoverflow.com/a/1176023/3092681
#  CC BY-SA 4.0

# stdlib
import pathlib
import re
from typing import Any, Callable, Dict, Optional, Union

# 3rd party
from domdf_python_tools.utils import strtobool

__all__ = ["as_path", "element_to_bool", "camel_to_snake", "strip_string"]


def as_path(val: Any) -> Optional[pathlib.PureWindowsPath]:
	"""
	Returns ``val`` as a :class:`~pathlib.PureWindowsPath`,
	or :py:obj:`None` if the value is empty/:py:obj:`None`/:py:obj:`False`.

	:param val: The value to convert to a path
	"""

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

	name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
	name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
	return name.lower()


def strip_string(val: str) -> str:
	"""
	Returns ``val`` as a string, without any leading or trailing whitespace.

	:param val:
	"""

	return str(val).strip()
