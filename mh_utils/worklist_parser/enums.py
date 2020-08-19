#!/usr/bin/env python
#
#  enums.py
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# 3rd party
from enum_tools import IntEnum
from enum_tools.documentation import document_enum

__all__ = ["AttributeType"]


@document_enum
class AttributeType(IntEnum):
	"""
	Enumeration of values for column/attribute types.
	"""

	SystemDefined = 0  # doc: Attributes defined by the system.
	SystemUsed = 1  # doc: Attributes used by the system.
	UserAdded = 2  # doc: Attributes added by the user.
