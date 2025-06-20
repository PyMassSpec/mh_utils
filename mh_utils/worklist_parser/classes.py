#  !/usr/bin/env python
#
#  classes.py
"""
Main classes for the worklist parser.
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
from pprint import pformat
from typing import Any, Dict, List, Optional, Sequence, Union
from uuid import UUID

# 3rd party
import attr
import lxml  # type: ignore
import pandas  # type: ignore
from attr_utils.docstrings import add_attrs_doc
from attr_utils.serialise import serde
from domdf_python_tools.doctools import prettify_docstrings

# this package
from mh_utils import Dictable
from mh_utils.utils import element_to_bool, strip_string
from mh_utils.worklist_parser.columns import Column, columns
from mh_utils.worklist_parser.enums import AttributeType
from mh_utils.worklist_parser.parser import parse_params, parse_sample_info
from mh_utils.xml import XMLFileMixin

__all__ = ["JobData", "Worklist", "Checksum", "Macro", "Attribute"]

pandas.DataFrame.__module__ = "pandas"


class JobData(Dictable):
	"""
	Represents an entry in the worklist.

	:param id: The ID of the job.
	:param job_type: The type of job. TODO: enum of values
	:param run_status: The status of the analysis.  TODO: enum of values
	:param sample_info: Optional ``key: value`` mapping of information about the sample.
	"""

	def __init__(
			self,
			id: Union[str, UUID],  # noqa: A002  # pylint: disable=redefined-builtin
			job_type: int,
			run_status: int,
			sample_info: Optional[dict] = None,
			):

		if isinstance(id, UUID):
			self.id = id
		else:
			self.id = UUID(str(id))

		self.job_type = int(job_type)
		self.run_status = int(run_status)

		if sample_info:
			self.sample_info = sample_info
		else:
			self.sample_info = {}

	__slots__ = ["id", "job_type", "run_status", "sample_info"]

	# dtypes
	# 8: Str
	# Inj Vol, Dilution and Equilib Time (min) 5

	@classmethod
	def from_xml(
			cls,
			element: lxml.objectify.ObjectifiedElement,
			user_columns: Optional[Dict[str, Column]] = None,
			) -> "JobData":
		"""
		Construct a :class:`~.JobData` object from an XML element.

		:param element: The XML element to parse the data from
		:param user_columns: Optional mapping of user column labels to
			:class:`~mh_utils.worklist_parser.columns.Column` objects.
		"""

		return cls(
				id=element.ID,
				job_type=element.JobType,
				run_status=element.RunStatus,
				sample_info=parse_sample_info(element.SampleInfo, user_columns),
				)

	def to_dict(self):
		"""
		Return a dictionary representation of the class.
		"""

		data = {}
		for key in self.__slots__:
			if key == "id":
				data[key] = str(self.id)
			else:
				data[key] = getattr(self, key)

		return data

	def __repr__(self) -> str:
		values = ", ".join(f"{key}={val!r}" for key, val in iter(self) if key != "sample_info")
		return f"{self.__class__.__name__}({values})"


@prettify_docstrings
class Worklist(XMLFileMixin, Dictable):
	"""
	Class that represents an Agilent MassHunter worklist.

	:param version: WorklistInfo version number
	:param locked_run_mode: Flag to indicate whether the data was acquired in locked mode. Yes = -1. No = 0.
	:param instrument_name: The name of the instrument.
	:param params: Mapping of parameter names to values. TODO: Check
	:param user_columns: Mapping of user columns to ??? TODO
	:param jobs:
	:param checksum: The checksum of the worklist file. The format is unknown.
	"""

	def __init__(
			self,
			version: float,
			locked_run_mode: bool,
			instrument_name: str,
			params: dict,
			user_columns: dict,
			jobs: Sequence[JobData],
			checksum: "Checksum",
			):

		self.version = float(version)
		self.locked_run_mode = bool(locked_run_mode)
		self.instrument_name = str(instrument_name)
		self.params = params
		self.user_columns = user_columns
		self.jobs = list(jobs)
		self.checksum = checksum

	__slots__ = ["version", "user_columns", "jobs", "checksum", "locked_run_mode", "instrument_name", "params"]

	def to_dict(self):
		"""
		Return a dictionary representation of the class.
		"""

		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Worklist":
		"""
		Construct a :class:`~.Worklist` object from an XML element.
		"""

		version = float(element.Version)
		checksum = Checksum.from_xml(element.Checksum)

		WorklistInfo = element.WorklistInfo

		if WorklistInfo.LockedRunMode == -1:
			locked_run_mode = True
		elif WorklistInfo.LockedRunMode == 0:
			locked_run_mode = False
		else:
			raise ValueError("Unknown value for 'LockedRunMode'")

		instrument_name = str(WorklistInfo.Instrument)
		params = parse_params(WorklistInfo.Params)

		attributes_list: List[Attribute] = []
		jobs_list: List[JobData] = []

		user_columns: Dict[str, Column] = {}

		for attribute in WorklistInfo.AttributeInformation.iterchildren("Attributes"):
			attribute = Attribute.from_xml(attribute)
			attributes_list.append(attribute)

			if attribute.attribute_type != AttributeType.SystemDefined:
				column = Column.from_attribute(attribute)
				user_columns[column.name] = column

		for job in WorklistInfo.JobDataList.iterchildren("JobData"):
			jobs_list.append(JobData.from_xml(job, user_columns))

		return cls(
				version=version,
				locked_run_mode=locked_run_mode,
				instrument_name=instrument_name,
				params=params,
				user_columns=user_columns,
				jobs=jobs_list,
				checksum=checksum,
				)

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({pformat(dict(self))})"

	def as_dataframe(self) -> pandas.DataFrame:
		"""
		Returns the :class:`~.Worklist` as a :class:`pandas.DataFrame`.

		:rtype:

		.. clearpage::
		"""

		headers = [col for col in columns] + [col for col in self.user_columns]
		data = []

		for job in self.jobs:
			row = []

			for header_label in headers:
				row.append(job.sample_info[header_label])

			data.append(row)

		# TODO: Sort columns by "reorder_id"

		return pandas.DataFrame(data, columns=headers)


@serde
@add_attrs_doc
@attr.s(slots=True)
class Checksum:
	"""
	Represents a checksum for a worklist.

	The format of the checksum is unknown.
	"""

	SchemaVersion: int = attr.ib(converter=int)
	ALGO_VERSION: int = attr.ib(converter=int)
	HASHCODE: str = attr.ib(converter=str)

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Checksum":
		"""
		Construct a :class:`~.Checksum` object from an XML element.
		"""

		return cls(
				SchemaVersion=element.attrib["SchemaVersion"],
				ALGO_VERSION=element.attrib["ALGO_VERSION"],
				HASHCODE=element.MAIN.attrib["HASHCODE"]
				)


@serde
@add_attrs_doc
@attr.s(slots=True, repr=False)
class Macro:
	"""
	Represents a macro in a worklist.

	:param output_parameter: .
	"""

	project_name: str = attr.ib(converter=strip_string)
	procedure_name: str = attr.ib(converter=strip_string)
	input_parameter: str = attr.ib(converter=strip_string)
	output_data_type: int = attr.ib(converter=int)
	output_parameter: str = attr.ib(converter=strip_string)
	"""
	.. clearpage::
	"""

	display_string: str = attr.ib(converter=strip_string)

	# TODO: enum for output_data_type

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Macro":
		"""
		Construct a :class:`~.Macro` object from an XML element.
		"""

		return cls(
				project_name=element.ProjectName,
				procedure_name=element.ProcedureName,
				input_parameter=element.InputParameter,
				output_data_type=element.OutputDataType,
				output_parameter=element.OutputParameter,
				display_string=element.DisplayString,
				)

	@property
	def undefined(self) -> bool:
		"""
		Returns whether the macro is undefined.
		"""

		return all([
				self.project_name == '',
				self.procedure_name == '',
				self.input_parameter == '',
				self.output_data_type == 0,
				self.output_parameter == '',
				self.display_string == '',
				])

	def __repr__(self) -> str:
		if self.undefined:
			return f"{self.__class__.__name__}(Undefined)"
		else:
			slots = self.__slots__
			values = ", ".join(f"{x}={getattr(self, x)!r}" for x in slots if x != "__weakref__")
			return f"{self.__class__.__name__}({values})"


@serde
@add_attrs_doc
@attr.s(slots=True)
class Attribute:
	r"""
	Represents an Attribute.

	.. raw:: latex

		\begin{multicols}{2}

	:param attribute_type: The attribute type identifier.
	:param field_type: The field type identifier.

	.. raw:: latex

		\end{multicols}

	.. clearpage::

	"""

	attribute_id: int = attr.ib(converter=int)

	attribute_type: AttributeType = attr.ib(converter=AttributeType)
	"""
	The attribute type identifier.

	Can be System Defined (``0``), System Used (``1``), or User Added (``2``).
	"""

	field_type: int = attr.ib(converter=int)
	"""
	The field type identifier.

	Each of the system defined columns have a field type starting from sampleid = 0 to reserved6 = 24.

	The system used column can be 'compound param' = 35, 'optim param' = 36,
	'mass param' = 37 and 'protein param' = 38.

	The User added columns start from 45.

	.. clearpage::
	"""

	system_name: str = attr.ib(converter=strip_string)
	header_name: str = attr.ib(converter=strip_string)

	# TODO: determine data_type and use it to cast the values and the default value
	# Perhaps
	# DataFileValuedata_type = bdict(
	# Unspecified=0,
	# Byte=1,
	# Int16=2,
	# Int32=3,
	# Int64=4,
	# Float32=5,
	# Float64=6,
	# )
	data_type: Any = attr.ib(converter=int)

	default_data_value: str = attr.ib(converter=strip_string)
	reorder_id: int = attr.ib(converter=int)
	show_hide_status: bool = attr.ib(converter=element_to_bool)
	column_width: int = attr.ib(converter=int)

	# TODO: enum for output_data_type

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Attribute":
		"""
		Construct an :class:`~.Attribute` object from an XML element.
		"""

		return cls(
				attribute_id=element.AttributeID,
				attribute_type=element.AttributeType,
				field_type=element.FieldType,
				system_name=element.SystemName,
				header_name=element.HeaderName,
				data_type=element.DataType,
				default_data_value=element.DefaultDataValue,
				reorder_id=element.ReorderID,
				show_hide_status=element.ShowHideStatus,
				column_width=element.ColumnWidth,
				)
