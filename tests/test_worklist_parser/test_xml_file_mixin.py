# 3rd party
import lxml.etree
import lxml.objectify

# this package
from mh_utils.xml import XMLFileMixin
from tests.test_worklist_parser.test_integration import worklist_file


class MixinSubclass(XMLFileMixin):

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement):
		return element


def test_from_xml_file():
	assert MixinSubclass.from_xml_file(worklist_file).Version
	assert MixinSubclass.from_xml_file(worklist_file).WorklistInfo is not None
	assert isinstance(MixinSubclass.from_xml_file(worklist_file), lxml.objectify.ObjectifiedElement)
