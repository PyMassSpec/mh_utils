# 3rd party
import pytest

# this package
from mh_utils.worklist_parser.classes import Macro


@pytest.fixture()
def sample_macro():
	return Macro(
			project_name="the project_name",
			procedure_name="the procedure_name",
			input_parameter="the input_parameter",
			output_data_type=42,
			output_parameter="the output_parameter",
			display_string="the display_string",
			)


def test_creation(sample_macro):

	assert sample_macro.project_name == "the project_name"
	assert sample_macro.procedure_name == "the procedure_name"
	assert sample_macro.input_parameter == "the input_parameter"
	assert sample_macro.output_data_type == 42
	assert sample_macro.output_parameter == "the output_parameter"
	assert sample_macro.display_string == "the display_string"


class FakeXMLElement:

	def __init__(self):
		self.ProjectName = "the project_name"
		self.ProcedureName = "the procedure_name"
		self.InputParameter = "the input_parameter"
		self.OutputDataType = "42"
		self.OutputParameter = "the output_parameter"
		self.DisplayString = "the display_string"


def test_from_xml():
	element = FakeXMLElement()
	data = Macro.from_xml(element)

	assert data.project_name == "the project_name"
	assert data.procedure_name == "the procedure_name"
	assert data.input_parameter == "the input_parameter"
	assert data.output_data_type == 42
	assert data.output_parameter == "the output_parameter"
	assert data.display_string == "the display_string"


def test_undefined_and_repr(sample_macro):

	assert not sample_macro.undefined

	assert str(sample_macro) == (
			"Macro("
			"project_name='the project_name', "
			"procedure_name='the procedure_name', "
			"input_parameter='the input_parameter', "
			"output_data_type=42, "
			"output_parameter='the output_parameter', "
			"display_string='the display_string')"
			)

	assert repr(sample_macro) == (
			"Macro("
			"project_name='the project_name', "
			"procedure_name='the procedure_name', "
			"input_parameter='the input_parameter', "
			"output_data_type=42, "
			"output_parameter='the output_parameter', "
			"display_string='the display_string')"
			)

	macro = Macro(
			project_name="",
			procedure_name="",
			input_parameter="",
			output_data_type=0,
			output_parameter="",
			display_string="",
			)
	assert macro.undefined

	assert str(macro) != (
			"Macro("
			"project_name='', "
			"procedure_name='', "
			"input_parameter='', "
			"output_data_type=0, "
			"output_parameter='', "
			"display_string='')"
			)

	assert repr(macro) != (
			"Macro("
			"project_name='', "
			"procedure_name='', "
			"input_parameter='', "
			"output_data_type=0, "
			"output_parameter='', "
			"display_string='')"
			)

	assert str(macro) == "Macro(Undefined)"

	assert repr(macro) == "Macro(Undefined)"
