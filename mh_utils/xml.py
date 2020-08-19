#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  xml.py
"""
Functions and classes for handling XML files.
"""
#
#  Copyright © 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

# stdlib
from abc import ABC, abstractmethod
from typing import Optional

# 3rd party
import lxml
from domdf_python_tools.typing import PathLike
from lxml import etree, objectify

__all__ = ["get_validated_tree", "XMLFileMixin"]


def get_validated_tree(xml_file: PathLike, schema_file: Optional[PathLike] = None):  # TODO: rtype
	"""
	Returns a validated lxml objectify from the given XML file, validated against the schema file.

	:param xml_file: The XML file to validate.
	:param schema_file: The schema file to validate against.
	"""

	schema = None
	if schema_file:
		schema = etree.XMLSchema(etree.parse(str(schema_file)))

	parser = objectify.makeparser(schema=schema)
	tree = objectify.parse(str(xml_file), parser=parser)

	if schema:
		assert schema.validate(tree)

	return tree


class XMLFileMixin(ABC):
	"""
	ABC mixin to provide a function for instantiating the class from an XML file.
	"""

	_schema: Optional[str] = None

	@classmethod
	def from_xml_file(cls, filename: PathLike):
		"""
		Generate an instance of this class by parsing an from an XML file.

		:param filename: The filename of the XML file.
		"""

		tree = get_validated_tree(filename, cls._schema)
		root = tree.getroot()
		return cls.from_xml(root)

	@classmethod
	@abstractmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement):
		"""
		Construct an object from an XML element.
		"""
