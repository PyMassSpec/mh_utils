# stdlib
from pathlib import PureWindowsPath
from pprint import pformat
from typing import List
from uuid import UUID

# 3rd party
import pandas  # type: ignore
import pytest

# this package
from mh_utils.utils import camel_to_snake
from mh_utils.worklist_parser import read_worklist
from mh_utils.worklist_parser.classes import Checksum, JobData, Worklist
from mh_utils.worklist_parser.columns import columns
from tests.test_worklist_parser.test_checksum import FakeChecksumElement
from tests.test_worklist_parser.test_integration import worklist_file
from tests.test_worklist_parser.test_job_data import FakeJobDataElement
from tests.test_worklist_parser.test_parser import FakeParamsElement


def test_creation():
	data = Worklist(
			version=2,
			locked_run_mode=True,
			instrument_name="The Instrument",
			params={
					"a param": "a value",
					"another param": 1234,
					},
			user_columns={},
			jobs=[],
			checksum=Checksum(
					SchemaVersion=1,
					ALGO_VERSION=2,
					HASHCODE="abcdefg",
					),
			)

	assert data.version == 2.0
	assert isinstance(data.version, float)

	assert data.locked_run_mode is True
	assert isinstance(data.locked_run_mode, bool)

	assert data.instrument_name == "The Instrument"
	assert data.params == {
			"a param": "a value",
			"another param": 1234,
			}
	assert data.user_columns == {}
	assert data.jobs == []
	assert data.checksum == Checksum(
			SchemaVersion=1,
			ALGO_VERSION=2,
			HASHCODE="abcdefg",
			)

	data = Worklist(
			version="2.3",  # type: ignore
			locked_run_mode=0,  # type: ignore
			instrument_name="The Instrument",
			params="not a dict ;)",  # type: ignore
			user_columns={},
			jobs=[],
			checksum="not a checksum ;)",  # type: ignore
			)

	assert data.version == 2.3
	assert isinstance(data.version, float)

	assert data.locked_run_mode is False
	assert isinstance(data.locked_run_mode, bool)

	assert data.instrument_name == "The Instrument"
	assert data.params == "not a dict ;)"
	assert data.user_columns == {}
	assert data.jobs == []
	assert data.checksum == "not a checksum ;)"


class FakeJobDataListElement(List[FakeJobDataElement]):

	def iterchildren(self, *args, **kwargs):
		return iter(self)


class FakeWorklistInfoElement:

	def __init__(self):
		self.LockedRunMode = -1
		self.Instrument = "The Instrument"
		self.Params = FakeParamsElement()
		self.AttributeInformation = FakeAttributeInformationElement()
		self.JobDataList = FakeJobDataListElement([FakeJobDataElement()])


class FakeAttributeInformationElement:

	def __init__(self):
		pass

	def iterchildren(self, *args, **kwargs):
		return ()


class FakeWorklistElement:

	def __init__(self):
		self.Version = "2.6"
		self.Checksum = FakeChecksumElement()
		self.WorklistInfo = FakeWorklistInfoElement()

	def iterchildren(self, *args, **kwargs):
		return ()


def test_locked_run_mode():
	element = FakeWorklistElement()

	element.WorklistInfo.LockedRunMode = -1
	data = Worklist.from_xml(element)
	assert data.locked_run_mode

	element.WorklistInfo.LockedRunMode = 0
	data = Worklist.from_xml(element)
	assert not data.locked_run_mode

	for mode in range(-100, -1, 1):
		element.WorklistInfo.LockedRunMode = mode
		with pytest.raises(ValueError, match="Unknown value for 'LockedRunMode'"):
			Worklist.from_xml(element)

	for mode in range(1, 101):
		element.WorklistInfo.LockedRunMode = mode
		with pytest.raises(ValueError, match="Unknown value for 'LockedRunMode'"):
			Worklist.from_xml(element)


def test_from_xml():
	element = FakeWorklistElement()

	data = Worklist.from_xml(element)

	# Version
	assert isinstance(data.version, float)
	assert data.version == 2.6

	# checksum
	assert isinstance(data.checksum, Checksum)
	assert data.checksum.SchemaVersion == 1
	assert data.checksum.ALGO_VERSION == 2
	assert data.checksum.HASHCODE == "abcdefg"

	# instrument_name
	assert isinstance(data.instrument_name, str)
	assert data.instrument_name == "The Instrument"

	# params
	assert isinstance(data.params, dict)

	assert data.params[camel_to_snake("OperatorName")] == "the OperatorName"
	assert data.params[camel_to_snake("RunType")] == 1234
	assert data.params[camel_to_snake("MethodExecutionType")] == "the MethodExecutionType"
	assert data.params[camel_to_snake("AcqMethodPath")] == PureWindowsPath("AcqMethodPath")
	assert data.params[camel_to_snake("DAMethodPath")] == PureWindowsPath("DAMethodPath")
	assert data.params[camel_to_snake("ExportOutputPath")] == PureWindowsPath("ExportOutputPath")
	assert data.params[camel_to_snake("CombineExportOutput")] is False
	assert data.params[camel_to_snake("CombinedExportOutputFile")] == PureWindowsPath("CombinedExportOutputFile")
	assert data.params[camel_to_snake("CombineOutputByPlate")] is True
	assert data.params[camel_to_snake("SynchronousExecution")] is False
	assert data.params[camel_to_snake("StopWorklistOnDAError")] is True
	assert data.params[camel_to_snake("OverlappedInjections")] is False
	assert data.params[camel_to_snake("UseBarcode")] is True
	assert data.params[camel_to_snake("InjectOnBarcodeMismatch")] is False
	assert data.params[camel_to_snake("ThresholdDiskSpace")] == 5678
	assert data.params[camel_to_snake("ReadyTimeOut")] == 9101112
	assert data.params["clear_run_checkbox"] is True
	assert data.params[camel_to_snake("UsePreWorklistMacro")] is False
	assert data.params[camel_to_snake("UsePostWorklistMacro")] is True
	assert data.params[camel_to_snake("RunAcqCleanMacroOnError")] is False
	assert data.params[camel_to_snake("UsePostAnalysisMacro")] is True
	assert data.params[camel_to_snake("Description")] == "the Description"
	assert data.params[camel_to_snake("PlateBarCodes")] == "any type"

	# user_columns
	assert data.user_columns == {}

	# Job Data
	assert isinstance(data.jobs[0], JobData)
	assert data.jobs[0].id == UUID("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}")
	assert data.jobs[0].job_type == 7
	assert data.jobs[0].run_status == 1


the_worklist = pytest.mark.parametrize(
		"data",
		[
				Worklist(
						version=2,
						locked_run_mode=True,
						instrument_name="The Instrument",
						params={
								"a param": "a value",
								"another param": 1234,
								},
						user_columns={},
						jobs=(),
						checksum=Checksum(
								SchemaVersion=1,
								ALGO_VERSION=2,
								HASHCODE="abcdefg",
								),
						)
				],
		)


@the_worklist
def test_dict(data: Worklist):
	assert dict(data) == {
			"version": 2.0,
			"locked_run_mode": True,
			"instrument_name": "The Instrument",
			"params": {
					"a param": "a value",
					"another param": 1234,
					},
			"user_columns": {},
			"jobs": [],
			"checksum": Checksum(
					SchemaVersion=1,
					ALGO_VERSION=2,
					HASHCODE="abcdefg",
					),
			}


@the_worklist
def test_repr(data: Worklist):
	assert str(data).startswith("Worklist(")
	assert str(data).endswith(')')
	assert str(data) == f"Worklist({pformat(dict(data))})"
	assert repr(data).startswith("Worklist(")
	assert repr(data).endswith(')')
	assert repr(data) == f"Worklist({pformat(dict(data))})"


@the_worklist
def test_as_dataframe(data: Worklist):
	df = data.as_dataframe()
	assert isinstance(df, pandas.DataFrame)

	# TODO: test with actual data

	assert df.columns.tolist() == [col for col in columns]
	assert df.empty


def test_as_dataframe_with_data():
	assert worklist_file.is_file()
	worklist = read_worklist(worklist_file)

	df = worklist.as_dataframe()
	print(df)
	assert isinstance(df, pandas.DataFrame)

	# TODO: test with actual data

	assert df.columns.tolist() == [
			"Sample ID",
			"Sample Name",
			"Rack Code",
			"Rack Position",
			"Plate Code",
			"Plate Position",
			"Sample Position",
			"Method",
			"Override DA Method",
			"Data File",
			"Sample Type",
			"Method Type",
			"Balance Override",
			"Inj Vol (µl)",
			"Equilib Time (min)",
			"Dilution",
			"Wt/Vol",
			"Comment",
			"Barcode",
			"Reserved1",
			"Reserved2",
			"Reserved3",
			"Reserved4",
			"Reserved5",
			"Reserved6",
			"Level Name",
			"Sample Group",
			"Info.",
			"Drying Gas",
			"Gas Temp",
			"Nebulizer",
			]
	assert not df.empty

	assert not df.iloc[0]["Sample ID"]
	assert df.iloc[0]["Sample Name"] == "Methanol Blank +ve"
	assert not df.iloc[0]["Rack Code"]
	assert not df.iloc[0]["Rack Position"]
	assert df.iloc[0]["Plate Code"] == "PlateOrVial"
	assert not df.iloc[0]["Plate Position"]
	assert df.iloc[0]["Sample Position"] == "P2-A3"
	assert df.iloc[0]["Method"] == PureWindowsPath(
			r"D:\MassHunter\Methods\Dominic Davis-Foster\Maitre Gunshot Residue Positive.m"
			)
	assert not df.iloc[0]["Override DA Method"]
	assert df.iloc[0]["Data File"] == PureWindowsPath(
			r"D:\MassHunter\Data\Dominic Davis-Foster\Methanol_Blank_+ve_191121-0001-r001.d"
			)
	assert df.iloc[0]["Sample Type"] == "Sample"
	assert df.iloc[0]["Method Type"] == "Method No Override"
	assert df.iloc[0]["Balance Override"] == "No Override"
	assert df.iloc[0]["Inj Vol (µl)"] == "As Method"
	assert df.iloc[0]["Equilib Time (min)"] == 0
	assert df.iloc[0]["Dilution"] == 1
	assert df.iloc[0]["Wt/Vol"] == 0
	assert not df.iloc[0]["Comment"]
	assert not df.iloc[0]["Barcode"]
	assert not df.iloc[0]["Reserved1"]
	assert not df.iloc[0]["Reserved2"]
	assert not df.iloc[0]["Reserved3"]
	assert df.iloc[0]["Reserved4"] == 0
	assert df.iloc[0]["Reserved5"] == 0
	assert df.iloc[0]["Reserved6"] == 0
	assert not df.iloc[0]["Level Name"]
	assert not df.iloc[0]["Sample Group"]
	assert not df.iloc[0]["Info."]
	assert not df.iloc[0]["Drying Gas"]
	assert not df.iloc[0]["Gas Temp"]
	assert not df.iloc[0]["Nebulizer"]

	assert df.iloc[11]["Sample Name"] == "Propellant 1ug gas 200"
	assert df.iloc[11]["Gas Temp"] == "200"
