# stdlib
from typing import Type, no_type_check

# 3rd party
import lxml.etree  # type: ignore[import-untyped]
import lxml.objectify  # type: ignore[import-untyped]
from typing_extensions import Self

# this package
from mh_utils.xml import XMLFileMixin
from tests.test_worklist_parser.test_integration import worklist_file


class MixinSubclass(XMLFileMixin):

	@classmethod
	def from_xml(cls: Type[Self], element: lxml.objectify.ObjectifiedElement) -> Self:
		return element


@no_type_check
def test_from_xml_file():
	assert MixinSubclass.from_xml_file(worklist_file).Version
	assert MixinSubclass.from_xml_file(worklist_file).WorklistInfo is not None
	assert isinstance(MixinSubclass.from_xml_file(worklist_file), lxml.objectify.ObjectifiedElement)
