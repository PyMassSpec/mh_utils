# stdlib
import functools
from typing import Any

# 3rd party
import pytest

# this package
from mh_utils.worklist_parser.classes import Attribute
from mh_utils.worklist_parser.columns import Column, injection_volume
from mh_utils.worklist_parser.enums import AttributeType
from tests.common import _test_strings, any_type_parametrize


@pytest.mark.parametrize("value, expects", [
		(-1, "As Method"),
		*[(x, x) for x in range(100)],
		])
def test_injection_volume(value, expects):
	assert injection_volume(value) == expects


class TestColumn:

	class _TestObj:

		def __init__(self):
			self.attribute_id = 1
			self.dtype = str
			self.default_value = -1
			self.field_type = None
			self.reorder_id = None

	def test_field_type_validator(self):
		validator = functools.partial(
				Column._Column__field_type_validator,  # type: ignore
				the_attr=None,
				the_value=None,
				)

		# Test for field_type being None
		obj = self._TestObj()
		assert obj.field_type is None
		validator(obj)
		assert obj.field_type == 1

		obj.field_type = 7
		validator(obj)
		assert obj.field_type == 7

		# Test for reorder_id being None
		obj = self._TestObj()
		assert obj.reorder_id is None
		validator(obj)
		assert obj.reorder_id == 1

		obj.reorder_id = 7
		validator(obj)
		assert obj.reorder_id == 7

	def test_default_value_validator(self):
		obj = self._TestObj()
		assert obj.default_value == -1
		Column._Column__default_value_validator(obj, None, None)  # type: ignore
		assert obj.default_value == "-1"

	@pytest.mark.parametrize("value, expects", [
			*_test_strings,
			('', "The Default"),
			])
	def test_cast_value(self, value, expects):
		c = Column(
				name="Test Column",
				attribute_id=1,
				attribute_type=AttributeType.SystemUsed,
				dtype=str,
				default_value="The Default"
				)

		assert c.cast_value(value) == expects

	@any_type_parametrize()
	def test_cast_value_any(self, value, expects):
		c = Column(
				name="Test Column",
				attribute_id=1,
				attribute_type=AttributeType.SystemUsed,
				dtype=Any,
				default_value="The Default"
				)

		assert c.cast_value(value) == expects

	@pytest.mark.parametrize(
			"data_type, dtype, default, default_expects",
			[
					(8, str, "  the default_data_value", "the default_data_value"),
					(5, float, "12.34  ", 12.34),
					(5, float, "12  ", 12.0),
					(1, Any, "the default_data_value", "the default_data_value"),
					(1, Any, "12.34  ", "12.34"),
					]
			)
	def test_from_attribute(self, data_type, dtype, default, default_expects):
		attribute = Attribute(
				attribute_id=42,
				attribute_type=AttributeType.SystemDefined,
				field_type=7,
				system_name="the system_name",
				header_name="the header_name",
				data_type=data_type,
				default_data_value=default,
				reorder_id=22,
				show_hide_status=False,
				column_width=250,
				)

		column = Column(
				name="the header_name",
				attribute_id=42,
				attribute_type=AttributeType.SystemDefined,
				dtype=dtype,
				default_value=default_expects,
				reorder_id=22,
				field_type=7,
				)

		assert Column.from_attribute(attribute) == column
