#  !/usr/bin/env python
#
#  columns.py
"""
Properties for columns in a Worklist.

.. autosummary::

	~mh_utils.worklist_parser.columns.Column
	~mh_utils.worklist_parser.columns.injection_volume
	~mh_utils.worklist_parser.columns.columns

"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Type, Union

# 3rd party
import attr
from attr_utils.docstrings import add_attrs_doc
from attr_utils.serialise import serde

# this package
from mh_utils.utils import as_path, strip_string
from mh_utils.worklist_parser.enums import AttributeType

if TYPE_CHECKING:
	# this package
	from mh_utils.worklist_parser.classes import Attribute

__all__ = ["injection_volume", "Column", "columns"]


def injection_volume(val: Union[float, str]) -> Union[int, str]:
	"""
	Handle special case for injection volume of ``-1``, which indicates "As Method".

	:param val:
	:type val:

	:return:
	:rtype:
	"""

	if val in {-1, "-1"}:
		return "As Method"
	else:
		return int(val)


@serde
@add_attrs_doc
@attr.s(slots=True)
class Column:
	"""
	Represents a column in a worklist.

	:param attribute_type: The attribute type identifier.
	:param dtype: The field datatype.
	:param field_type: The field type identifier.
	"""

	def __field_type_validator(self, the_attr: attr.Attribute, the_value):
		if self.field_type is None:
			self.field_type = self.attribute_id
		if self.reorder_id is None:
			self.reorder_id = self.attribute_id

	def __default_value_validator(self, the_attr: attr.Attribute, the_value):
		if self.dtype is not Any:
			self.default_value = self.dtype(self.default_value)

	#: The name of the column
	name: str = attr.ib(converter=strip_string)

	attribute_id: int = attr.ib(converter=int)

	attribute_type: AttributeType = attr.ib(converter=AttributeType)
	"""
	The attribute type identifier.

	Can be System Defined (``0``), System Used (``1``), or User Added (``2``).
	"""

	dtype: Callable = attr.ib()
	"""
	.. clearpage::
	"""

	default_value: Any = attr.ib(validator=__default_value_validator)

	field_type: Optional[int] = attr.ib(default=None, validator=__field_type_validator)
	"""
	The field type identifier.

	Each of the system defined columns have a field type starting from sampleid = 0 to reserved6 = 24.

	The system used column can be 'compound param' = 35, 'optim param' = 36,
	'mass param' = 37 and 'protein param' = 38.

	The User added columns start from 45.
	"""

	reorder_id: Optional[int] = attr.ib(default=None)

	def cast_value(self, value: Any):
		"""
		Cast ``value`` to the dtype of this column.
		"""

		if isinstance(value, str) and not value:
			return self.default_value

		if self.dtype is Any:
			return value
		else:
			return self.dtype(value)

	@classmethod
	def from_attribute(cls, attribute: "Attribute") -> "Column":
		"""
		Construct a column for a :class:`mh_utils.worklist_parser.classes.Attribute`.

		:param attribute: :class:`~mh_utils.worklist_parser.classes.Attribute`
		"""

		dtype: Union[Type, object]

		if attribute.data_type == 8:
			dtype = str
		elif attribute.data_type == 5:
			dtype = float
		else:
			dtype = Any

		return Column(
				name=attribute.header_name,
				attribute_id=attribute.attribute_id,
				attribute_type=attribute.attribute_type,
				dtype=dtype,  # type: ignore
				default_value=attribute.default_data_value,
				field_type=attribute.field_type,
				reorder_id=attribute.reorder_id,
				)


#: Mapping of column names to column objects.
columns: Dict[str, Column] = {
		col.name: col
		for col in [
				Column(
						name="Sample ID",
						attribute_id=0,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='', ),
				Column(
						name="Sample Name",
						attribute_id=1,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='', ),
				Column(
						name="Rack Code",
						attribute_id=2,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='', ),
				Column(
						name="Rack Position",
						attribute_id=3,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='', ),
				Column(
						name="Plate Code",
						attribute_id=4,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='', ),
				Column(
						name="Plate Position",
						attribute_id=5,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='', ),
				Column(
						name="Sample Position",
						attribute_id=6,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='', ),
				Column(
						name="Method",
						attribute_id=7,
						attribute_type=AttributeType.SystemDefined,
						dtype=as_path,
						default_value=None, ),
				Column(
						name="Override DA Method",
						attribute_id=8,
						attribute_type=AttributeType.SystemDefined,
						dtype=as_path,
						default_value=None, ),
				Column(
						name="Data File",
						attribute_id=9,
						attribute_type=AttributeType.SystemDefined,
						dtype=as_path,
						default_value=None, ),
				Column(
						name="Sample Type",
						attribute_id=10,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value="Unknown", ),
				Column(
						name="Method Type",
						attribute_id=11,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value="Method No Override",
						reorder_id=12, ),
				Column(
						name="Balance Override",
						attribute_id=12,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value="No Override",
						reorder_id=13, ),
				Column(
						name="Inj Vol (µl)",
						attribute_id=13,
						attribute_type=AttributeType.SystemDefined,
						dtype=injection_volume,
						default_value=5,
						reorder_id=14, ),
				Column(
						name="Equilib Time (min)",
						attribute_id=14,
						attribute_type=AttributeType.SystemDefined,
						dtype=int,
						default_value=0,
						reorder_id=15, ),
				Column(
						name="Dilution",
						attribute_id=15,
						attribute_type=AttributeType.SystemDefined,
						dtype=int,
						default_value=1,
						reorder_id=16, ),
				Column(
						name="Wt/Vol",
						attribute_id=16,
						attribute_type=AttributeType.SystemDefined,
						dtype=float,
						default_value=0,
						reorder_id=17, ),
				Column(
						name="Comment",
						attribute_id=17,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=18, ),
				Column(
						name="Barcode",
						attribute_id=18,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=19, ),
				Column(
						name="Reserved1",
						attribute_id=19,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=-1, ),
				Column(
						name="Reserved2",
						attribute_id=20,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=-1, ),
				Column(
						name="Reserved3",
						attribute_id=21,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=-1, ),
				Column(
						name="Reserved4",
						attribute_id=22,
						attribute_type=AttributeType.SystemDefined,
						dtype=float,
						default_value=0,
						reorder_id=-1, ),
				Column(
						name="Reserved5",
						attribute_id=23,
						attribute_type=AttributeType.SystemDefined,
						dtype=float,
						default_value=0,
						reorder_id=-1, ),
				Column(
						name="Reserved6",
						attribute_id=24,
						attribute_type=AttributeType.SystemDefined,
						dtype=float,
						default_value=0,
						reorder_id=-1, ),
				Column(
						name="Level Name",
						attribute_id=25,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=11, ),
				Column(
						name="Sample Group",
						attribute_id=26,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=20, ),
				Column(
						name="Info.",
						attribute_id=27,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=21, ), ]
		}
