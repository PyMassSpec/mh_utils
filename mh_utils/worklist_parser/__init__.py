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
import os

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

	if not os.path.isfile(filename):
		raise FileNotFoundError(f"'{filename}' does not exist.")

	return Worklist.from_xml_file(filename)
