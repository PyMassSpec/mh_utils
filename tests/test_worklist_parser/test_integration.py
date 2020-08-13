# stdlib
import pathlib

# this package
from mh_utils.worklist_parser import Worklist, read_worklist

worklist_file = pathlib.Path(__file__).parent / "test_worklist.wkl"


def test_integration():
	assert worklist_file.is_file()
	worklist = read_worklist(worklist_file)
	print(worklist)

	assert isinstance(worklist, Worklist)
