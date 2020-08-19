# stdlib
import random
from datetime import datetime, timezone
from pathlib import PureWindowsPath

# 3rd party
import pytest

# this package
from mh_utils.utils import camel_to_snake
from mh_utils.worklist_parser.classes import Macro
from mh_utils.worklist_parser.parser import parse_datetime, parse_params, parse_sample_info
from tests.common import _test_strings, count, true_false_strings, whitespace_perms


class FakeMacroElement:

	def __init__(self):
		self.ProjectName = "the ProjectName"
		self.ProcedureName = "the ProcedureName"
		self.InputParameter = "the InputParameter"
		self.OutputDataType = 1234
		self.OutputParameter = "the OutputParameter"
		self.DisplayString = "the DisplayString"


class FakeParamsElement:

	def __init__(self):
		self.OperatorName = "the OperatorName"
		self.RunType = 1234
		self.MethodExecutionType = "the MethodExecutionType"
		self.AcqMethodPath = PureWindowsPath("AcqMethodPath")
		self.DAMethodPath = PureWindowsPath("DAMethodPath")
		self.ExportOutputPath = PureWindowsPath("ExportOutputPath")
		self.CombineExportOutput = False
		self.CombinedExportOutputFile = PureWindowsPath("CombinedExportOutputFile")
		self.CombineOutputByPlate = True
		self.SynchronousExecution = False
		self.StopWorklistOnDAError = True
		self.OverlappedInjections = False
		self.UseBarcode = True
		self.InjectOnBarcodeMismatch = False
		self.ThresholdDiskSpace = 5678
		self.ReadyTimeOut = 9101112
		self.ClearRunCheckBox = True
		self.UsePreWorklistMacro = False
		self.PreWorklistMacro = FakeMacroElement()
		self.UsePostWorklistMacro = True
		self.PostWorklistMacro = FakeMacroElement()
		self.RunAcqCleanMacroOnError = False
		self.AcqCleanMacro = FakeMacroElement()
		self.UsePostAnalysisMacro = True
		self.PostAnalysisMacro = FakeMacroElement()
		self.Description = "the Description"
		self.PlateBarCodes = "any type"


def macro_type_parametrize():
	e = FakeMacroElement()

	m = Macro(
			project_name="the ProjectName",
			procedure_name="the ProcedureName",
			input_parameter="the InputParameter",
			output_data_type=1234,
			output_parameter="the OutputParameter",
			display_string="the DisplayString",
			)

	return pytest.mark.parametrize(f"value, expects", [
			(e, m),
			])


class __TestParseParams_str:
	param_under_test: str
	param_dict_name: str
	param_type = str

	@pytest.mark.parametrize(f"value, expects", _test_strings)
	def test_parse_params(self, value, expects):
		e = FakeParamsElement()
		setattr(e, self.param_under_test, value)
		params = parse_params(e)
		assert params[self.param_dict_name] == expects
		assert isinstance(params[self.param_dict_name], self.param_type)


class TestOperatorName(__TestParseParams_str):
	param_under_test = "OperatorName"
	param_dict_name = camel_to_snake(param_under_test)


class TestMethodExecutionType(__TestParseParams_str):
	param_under_test = "MethodExecutionType"
	param_dict_name = camel_to_snake(param_under_test)


class TestDescription(__TestParseParams_str):
	param_under_test = "Description"
	param_dict_name = camel_to_snake(param_under_test)


class __TestParseParams_int:
	param_under_test: str
	param_dict_name: str
	param_type = int

	@pytest.mark.parametrize(f"value, expects", [
			(1234, 1234),
			("1234", 1234),
			(12.34, 12),
			])
	def test_parse_params(self, value, expects):
		e = FakeParamsElement()
		setattr(e, self.param_under_test, value)
		params = parse_params(e)
		assert params[self.param_dict_name] == expects
		assert isinstance(params[self.param_dict_name], self.param_type)


class TestRunType(__TestParseParams_int):
	param_under_test = "RunType"
	param_dict_name = camel_to_snake(param_under_test)


class TestThresholdDiskSpace(__TestParseParams_int):
	param_under_test = "ThresholdDiskSpace"
	param_dict_name = camel_to_snake(param_under_test)


class TestReadyTimeOut(__TestParseParams_int):
	param_under_test = "ReadyTimeOut"
	param_dict_name = camel_to_snake(param_under_test)


class __TestParseParams_path:
	param_under_test: str
	param_dict_name: str
	param_type = PureWindowsPath

	@pytest.mark.parametrize(
			f"value, expects",
			[
					("foo", PureWindowsPath("foo")),
					("foo/bar", PureWindowsPath("foo/bar")),
					("foo/bar/file.txt", PureWindowsPath("foo/bar/file.txt")),
					("C:/foo/bar/file.txt", PureWindowsPath("C:/foo/bar/file.txt")),
					]
			)
	def test_parse_params(self, value, expects):
		e = FakeParamsElement()
		setattr(e, self.param_under_test, value)
		params = parse_params(e)
		assert params[self.param_dict_name] == expects
		assert isinstance(params[self.param_dict_name], self.param_type)


class TestAcqMethodPath(__TestParseParams_path):
	param_under_test = "AcqMethodPath"
	param_dict_name = camel_to_snake(param_under_test)


class TestDAMethodPath(__TestParseParams_path):
	param_under_test = "DAMethodPath"
	param_dict_name = camel_to_snake(param_under_test)


class TestExportOutputPath(__TestParseParams_path):
	param_under_test = "ExportOutputPath"
	param_dict_name = camel_to_snake(param_under_test)


class TestCombinedExportOutputFile(__TestParseParams_path):
	param_under_test = "CombinedExportOutputFile"
	param_dict_name = camel_to_snake(param_under_test)


class __TestParseParams_bool:
	param_under_test: str
	param_dict_name: str
	param_type = bool

	@pytest.mark.parametrize(f"value, expects", random.sample(true_false_strings, 3))
	def test_parse_params(self, value, expects):
		e = FakeParamsElement()
		setattr(e, self.param_under_test, value)
		params = parse_params(e)  # type: ignore
		assert params[self.param_dict_name] == expects
		assert isinstance(params[self.param_dict_name], self.param_type)


class TestCombineExportOutput(__TestParseParams_bool):
	param_under_test = "CombineExportOutput"
	param_dict_name = camel_to_snake(param_under_test)


class TestCombineOutputByPlate(__TestParseParams_bool):
	param_under_test = "CombineOutputByPlate"
	param_dict_name = camel_to_snake(param_under_test)


class TestSynchronousExecution(__TestParseParams_bool):
	param_under_test = "SynchronousExecution"
	param_dict_name = camel_to_snake(param_under_test)


class TestStopWorklistOnDAError(__TestParseParams_bool):
	param_under_test = "StopWorklistOnDAError"
	param_dict_name = camel_to_snake(param_under_test)


class TestOverlappedInjections(__TestParseParams_bool):
	param_under_test = "OverlappedInjections"
	param_dict_name = camel_to_snake(param_under_test)


class TestUseBarcode(__TestParseParams_bool):
	param_under_test = "UseBarcode"
	param_dict_name = camel_to_snake(param_under_test)


class TestInjectOnBarcodeMismatch(__TestParseParams_bool):
	param_under_test = "InjectOnBarcodeMismatch"
	param_dict_name = camel_to_snake(param_under_test)


class TestClearRunCheckBox(__TestParseParams_bool):
	param_under_test = "ClearRunCheckBox"
	param_dict_name = "clear_run_checkbox"


class TestUsePreWorklistMacro(__TestParseParams_bool):
	param_under_test = "UsePreWorklistMacro"
	param_dict_name = camel_to_snake(param_under_test)


class TestUsePostWorklistMacro(__TestParseParams_bool):
	param_under_test = "UsePostWorklistMacro"
	param_dict_name = camel_to_snake(param_under_test)


class TestRunAcqCleanMacroOnError(__TestParseParams_bool):
	param_under_test = "RunAcqCleanMacroOnError"
	param_dict_name = camel_to_snake(param_under_test)


class TestUsePostAnalysisMacro(__TestParseParams_bool):
	param_under_test = "UsePostAnalysisMacro"
	param_dict_name = camel_to_snake(param_under_test)


class __TestParseParams_macro:
	param_under_test: str
	param_dict_name: str
	param_type = Macro

	@macro_type_parametrize()
	def test_parse_params(self, value, expects):
		e = FakeParamsElement()
		setattr(e, self.param_under_test, value)
		params = parse_params(e)  # type: ignore
		assert params[self.param_dict_name] == expects
		assert isinstance(params[self.param_dict_name], self.param_type)


class TestPreWorklistMacro(__TestParseParams_macro):
	param_under_test = "PreWorklistMacro"
	param_dict_name = camel_to_snake(param_under_test)


class TestPostWorklistMacro(__TestParseParams_macro):
	param_under_test = "PostWorklistMacro"
	param_dict_name = camel_to_snake(param_under_test)


class TestAcqCleanMacro(__TestParseParams_macro):
	param_under_test = "AcqCleanMacro"
	param_dict_name = camel_to_snake(param_under_test)


class TestPostAnalysisMacro(__TestParseParams_macro):
	param_under_test = "PostAnalysisMacro"
	param_dict_name = camel_to_snake(param_under_test)


# TODO: # PlateBarCodes
# class TestPlateBarCodes(__TestParseParams_):
# 	param_under_test = "PlateBarCodes"
# 	param_dict_name = camel_to_snake(param_under_test)


class FakeSampleElement:

	def __init__(self):
		self.AcqTime = "2019-11-21T11:36:57.9473494+00:00"
		self.SampleLockedRunMode = "True"
		self.RunCompletedFlag = "False"
		self.Label = "The run label"

		self.Identifier = "the Identifier"
		self.Name = "the Name"
		self.RackCode = "the RackCode"
		self.RackPosition = "the RackPosition"
		self.PlateCode = "the PlateCode"
		self.PlatePosition = "the PlatePosition"
		self.SamplePosition = "the SamplePosition"
		self.AcqMethod = "foo"  # PureWindowsPath
		self.DAMethod = "bar"  # PureWindowsPath
		self.DataFileName = "baz"  # PureWindowsPath
		self.SampleType = "the SampleType"
		self.MethodExecutionType = "the MethodExecutionType"
		self.BalanceType = "the BalanceType"
		self.InjectionVolume = 1
		self.EquilibrationTime = 2
		self.DilutionFactor = 3
		self.WeightPerVolume = 4.5
		self.Description = "the Description"
		self.Barcode = "the Barcode"
		self.Reserved1 = "the Reserved1"
		self.Reserved2 = "the Reserved2"
		self.Reserved3 = "the Reserved3"
		self.Reserved4 = 5.6
		self.Reserved5 = 7.8
		self.Reserved6 = 9.0
		self.CalibLevelName = "the CalibLevelName"
		self.SampleGroup = "the SampleGroup"
		self.SampleInformation = "the SampleInformation"

	def iterchildren(self, *args, **kwargs):
		return ()


class __TestParseSampleInfo_bool:
	param_under_test: str
	param_dict_name: str
	param_type = bool

	@pytest.mark.parametrize(f"value, expects", random.sample(true_false_strings, 3))
	def test_parse_params(self, value, expects):
		e = FakeSampleElement()
		setattr(e, self.param_under_test, value)
		sample_info = parse_sample_info(e)  # type: ignore
		assert sample_info[self.param_dict_name] == expects
		assert isinstance(sample_info[self.param_dict_name], self.param_type)


class __TestParseSampleInfo_str:
	param_under_test: str
	param_dict_name: str
	param_type = str

	@pytest.mark.parametrize(f"value, expects", _test_strings)
	def test_parse_params(self, value, expects):
		e = FakeSampleElement()
		setattr(e, self.param_under_test, value)
		sample_info = parse_sample_info(e)  # type: ignore
		assert sample_info[self.param_dict_name] == expects
		assert isinstance(sample_info[self.param_dict_name], self.param_type)


class TestSampleInfo_SampleLockedRunMode(__TestParseSampleInfo_bool):
	param_under_test = "SampleLockedRunMode"
	param_dict_name = "Sample Locked Run Mode"


class TestSampleInfo_RunCompletedFlag(__TestParseSampleInfo_bool):
	param_under_test = "RunCompletedFlag"
	param_dict_name = "Run Completed"


class TestSampleInfo_Label(__TestParseSampleInfo_str):
	param_under_test = "Label"
	param_dict_name = "Label"


class TestParseDatetime:
	dates = pytest.mark.parametrize(
			"date, expects",
			[
					(
							"2019-11-21T11:36:57.9473494+00:00",
							datetime(
									year=2019,
									month=11,
									day=21,
									hour=11,
									minute=36,
									second=57,
									tzinfo=timezone.utc
									),
							),
					(
							"2019-11-26T15:13:58.1815504+00:00",
							datetime(
									year=2019,
									month=11,
									day=26,
									hour=15,
									minute=13,
									second=58,
									tzinfo=timezone.utc
									),
							),
					(
							"2020-02-06T11:21:16.2434446+00:00",
							datetime(
									year=2020, month=2, day=6, hour=11, minute=21, second=16, tzinfo=timezone.utc
									),
							),
					(
							"",
							datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc),
							),
					]
			)

	@whitespace_perms()
	@count(100)
	def test_whitespace(self, char: str, count: int):
		assert parse_datetime(char * count) == datetime(
				year=1970, month=1, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc
				)

	@pytest.mark.parametrize("whitespace_pos", ["left", "right", "both"])
	@count(100)
	@whitespace_perms()
	@dates
	def test(
			self,
			whitespace_pos,
			count,
			char,
			date,
			expects,
			):

		if whitespace_pos == "left":
			with_whitespace = f"{char * count}{date}"
		elif whitespace_pos == "right":
			with_whitespace = f"{date}{char * count}"
		elif whitespace_pos == "both":
			with_whitespace = f"{char * count}{date}{char * count}"
		else:
			with_whitespace = date

		assert parse_datetime(with_whitespace) == expects

	@dates
	def test_no_whitespace(
			self,
			date,
			expects,
			):

		assert parse_datetime(date) == expects
