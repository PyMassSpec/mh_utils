# 3rd party
import pytest

# this package
from mh_utils.worklist_parser.classes import Attribute
from mh_utils.worklist_parser.enums import AttributeType


class FakeXMLElement:

	def __init__(self):
		self.AttributeID = "42"
		self.AttributeType = AttributeType.SystemDefined
		self.FieldType = "7"
		self.SystemName = "the system_name"
		self.HeaderName = "the header_name"
		self.DataType = "1"
		self.DefaultDataValue = "the default_data_value"
		self.ReorderID = "22"
		self.ShowHideStatus = "False"
		self.ColumnWidth = "250"


data_from_init = Attribute(
		attribute_id=42,
		attribute_type=AttributeType.SystemDefined,
		field_type=7,
		system_name="  the system_name",
		header_name="the header_name  ",
		data_type=1,
		default_data_value="  the default_data_value\t",
		reorder_id=22,
		show_hide_status="False",  # type: ignore
		column_width=250,
		)

element = FakeXMLElement()
data_from_element = data = Attribute.from_xml(element)


@pytest.mark.parametrize(
		"data", [
				pytest.param(data_from_init, id="from init"),
				pytest.param(data_from_element, id="from element"),
				]
		)
def test_attribute(data):

	assert data.attribute_id == 42
	assert data.attribute_type == AttributeType.SystemDefined
	assert data.field_type == 7
	assert data.system_name == "the system_name"
	assert data.header_name == "the header_name"
	assert data.data_type == 1
	assert data.default_data_value == "the default_data_value"
	assert data.reorder_id == 22
	assert data.show_hide_status is False
	assert data.column_width == 250
