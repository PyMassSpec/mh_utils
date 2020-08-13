# 3rd party
import pytest

# this package
from mh_utils.worklist_parser.classes import Checksum


@pytest.mark.parametrize("SchemaVersion, SchemaVersion_expects", [
		(1, 1),
		("1", 1),
		(1.2, 1),
		])
@pytest.mark.parametrize("ALGO_VERSION, ALGO_VERSION_expects", [
		(2, 2),
		("2", 2),
		(2.5, 2),
		])
def test_creation(SchemaVersion, SchemaVersion_expects, ALGO_VERSION, ALGO_VERSION_expects):
	data = Checksum(
			SchemaVersion=SchemaVersion,
			ALGO_VERSION=ALGO_VERSION,
			HASHCODE="abcdefg",
			)

	assert data.SchemaVersion == SchemaVersion_expects
	assert data.ALGO_VERSION == ALGO_VERSION_expects
	assert data.HASHCODE == "abcdefg"


class FakeChecksumElement:

	def __init__(self):
		self.attrib = dict(SchemaVersion="1", ALGO_VERSION="2", HASHCODE="abcdefg")
		self.MAIN = self


def test_from_xml():

	element = FakeChecksumElement()
	data = Checksum.from_xml(element)

	assert data.SchemaVersion == 1
	assert data.ALGO_VERSION == 2
	assert data.HASHCODE == "abcdefg"
