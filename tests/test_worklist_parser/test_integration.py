# stdlib
import pathlib

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus

# this package
from mh_utils.worklist_parser import read_worklist
from mh_utils.worklist_parser.classes import Worklist

worklist_file = pathlib.Path(__file__).parent / "test_worklist.wkl"


def test_integration():
	assert worklist_file.is_file()
	worklist = read_worklist(worklist_file)
	print(worklist)

	assert isinstance(worklist, Worklist)


@pytest.mark.parametrize(
		"xml_file",
		[
				"missing.xml",
				pathlib.Path("missing.xml"),
				pathlib.PurePosixPath("missing.xml"),
				PathPlus("missing.xml"),
				"/home/user/directory/missing.xml",
				pathlib.Path("/home/user/directory/missing.xml"),
				pathlib.PurePosixPath("/home/user/directory/missing.xml"),
				PathPlus("/home/user/directory/missing.xml"),
				],
		)
def test_read_worklist_missing_file(xml_file):
	with pytest.raises(FileNotFoundError, match="'.*' does not exist."):
		read_worklist(xml_file)
