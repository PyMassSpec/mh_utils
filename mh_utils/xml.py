#  !/usr/bin/env python
#
#  xml.py
"""
Functions and classes for handling XML files.
"""
#
#  Copyright © 2029-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import pathlib
from abc import ABC, abstractmethod
from typing import Optional

# 3rd party
import lxml  # type: ignore
from domdf_python_tools.typing import PathLike
from lxml import etree, objectify
from lxml.etree import _ElementTree  # type: ignore
from lxml.objectify import ObjectifiedElement  # type: ignore

__all__ = ["get_validated_tree", "XMLFileMixin"]


def get_validated_tree(xml_file: PathLike, schema_file: Optional[PathLike] = None) -> _ElementTree:
	"""
	Returns a validated lxml objectify from the given XML file, validated against the schema file.

	:param xml_file: The XML file to validate.
	:param schema_file: The schema file to validate against.

	:returns: An lxml ElementTree object. When .getroot() us called on the tree the root will be an instance of
		:class:`lxml.objectify.ObjectifiedElement`.
	"""

	if not isinstance(xml_file, pathlib.Path):
		xml_file = pathlib.Path(xml_file)

	if not xml_file.is_file():
		raise FileNotFoundError(f"XML file '{xml_file}' not found.")

	schema: Optional[etree.XMLSchema] = None

	if schema_file is not None:

		if not isinstance(schema_file, pathlib.Path):
			schema_file = pathlib.Path(schema_file)

		if not schema_file.is_file():
			raise FileNotFoundError(f"XML schema '{schema_file}' not found.")

		schema = etree.XMLSchema(etree.parse(str(schema_file)))

	parser = objectify.makeparser(schema=schema)
	tree: _ElementTree = objectify.parse(str(xml_file), parser=parser)

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
		root: ObjectifiedElement = tree.getroot()
		return cls.from_xml(root)

	@classmethod
	@abstractmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement):
		"""
		Construct an object from an XML element.
		"""
