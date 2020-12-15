# stdlib
import pathlib
from zipimport import zipimporter

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from importlib_resources import as_file, files
from lxml.etree import XMLSyntaxError, _ElementTree  # type: ignore

# this package
import tests.test_xml
from mh_utils.xml import get_validated_tree

try:
	# stdlib
	from zipfile import Path as ZipPath  # type: ignore
except ImportError:
	# 3rd party
	from zipp import Path as ZipPath  # type: ignore

test_xml_zipapp = zipimporter(files(tests.test_xml).joinpath("test_xml_zipapp.pyz")).load_module("test_xml_zipapp")

shiporder_filename: ZipPath = files(tests.test_xml).joinpath("shiporder.xml")
bad_file: ZipPath = files(tests.test_xml).joinpath("bad_file.xml")
schema_filename: ZipPath = files(tests.test_xml).joinpath("schema.xml")
bad_schema: ZipPath = files(tests.test_xml).joinpath("bad_schema.xml")
zipapp_shiporder_filename: ZipPath = files(test_xml_zipapp).joinpath("shiporder.xml")
zipapp_schema_filename: ZipPath = files(test_xml_zipapp).joinpath("schema.xml")

xml_files = pytest.mark.parametrize(
		"xml_file",
		[
				shiporder_filename,
				str(shiporder_filename),
				pathlib.Path(str(shiporder_filename)),
				pathlib.PurePosixPath(str(shiporder_filename)),
				PathPlus(str(shiporder_filename)),
				],
		)

schema_files = pytest.mark.parametrize(
		"schema_file",
		[
				schema_filename,
				str(schema_filename),
				pathlib.Path(str(schema_filename)),
				pathlib.PurePosixPath(str(schema_filename)),
				PathPlus(str(schema_filename)),
				],
		)


@xml_files
def test_get_validated_tree(xml_file: PathLike):
	tree = get_validated_tree(xml_file=xml_file)
	assert isinstance(tree, _ElementTree)


@schema_files
def test_get_validated_tree_from_zip(schema_file: PathLike):
	with as_file(zipapp_shiporder_filename) as unzipped_xml_file:
		xml_file = pathlib.Path(str(unzipped_xml_file))
		tree = get_validated_tree(xml_file=xml_file)
		assert isinstance(tree, _ElementTree)

	with as_file(zipapp_shiporder_filename) as unzipped_xml_file:
		xml_file = pathlib.Path(str(unzipped_xml_file))
		tree = get_validated_tree(xml_file=xml_file, schema_file=schema_file)
		assert isinstance(tree, _ElementTree)

	with as_file(zipapp_shiporder_filename) as unzipped_xml_file:
		xml_file = pathlib.Path(str(unzipped_xml_file))
		with as_file(zipapp_schema_filename) as unzipped_schema_file:
			schema_file = pathlib.Path(str(unzipped_schema_file))
			tree = get_validated_tree(xml_file=xml_file, schema_file=schema_file)
			assert isinstance(tree, _ElementTree)


@xml_files
@schema_files
def test_get_validated_tree_with_schema(xml_file: PathLike, schema_file: PathLike):
	tree = get_validated_tree(xml_file=xml_file, schema_file=schema_file)
	assert isinstance(tree, _ElementTree)


def test_get_validated_tree_invalid_file():
	with pytest.raises(XMLSyntaxError, match="Start tag expected, '<' not found, line 1, column 1"):
		get_validated_tree(xml_file=str(bad_file))


def test_get_validated_tree_missing_file():
	with pytest.raises(FileNotFoundError, match="XML file 'missing.xml' not found."):
		get_validated_tree(xml_file="missing.xml")


def test_get_validated_tree_invalid_schema():
	with pytest.raises(XMLSyntaxError, match="Start tag expected, '<' not found, line 1, column 1"):
		get_validated_tree(xml_file=shiporder_filename, schema_file=str(bad_schema))


def test_get_validated_tree_missing_schema():
	with pytest.raises(FileNotFoundError, match="XML schema 'missing_schema.xml' not found."):
		get_validated_tree(xml_file=shiporder_filename, schema_file="missing_schema.xml")
