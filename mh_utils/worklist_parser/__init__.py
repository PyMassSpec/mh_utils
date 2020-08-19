#!/usr/bin/env python3
#
#  __init__.py
"""
Parser for MassHunter worklists.

Only one function is defined here: :class:`~.read_worklist`,
which reads the reads the given worklist file and returns
a :class:`mh_utils.worklist_parser.classes.Worklist` file representing it.
The other functions and classes must be imported from submodules of this package.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# 3rd party
from domdf_python_tools.typing import PathLike

# this package
from mh_utils.worklist_parser.classes import Worklist

__all__ = ["read_worklist"]


def read_worklist(filename: PathLike) -> Worklist:
	"""
	Read the worklist from the given file.

	:param filename: The filename of the worklist.
	"""

	return Worklist.from_xml_file(filename)
