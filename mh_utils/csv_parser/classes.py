#!/usr/bin/env python3
#
#  classes.py
"""
Classes to model parts of MassHunter CSV files.

.. versionadded:: 0.2.0
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
from collections import OrderedDict
from decimal import Decimal
from typing import Dict, Iterable, List, Optional, Tuple, Type, TypeVar

# 3rd party
import numpy
import pandas  # type: ignore
import sdjson
from cawdrey import AlphaDict
from domdf_python_tools import doctools
from domdf_python_tools.doctools import prettify_docstrings
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

# this package
from mh_utils import Dictable

__all__ = [
		"Sample",
		"Result",
		"SampleList",
		"BaseSamplePropertyDict",
		"SamplesAreaDict",
		"SamplesScoresDict",
		"encode_result_or_sample",
		"encode_set",
		"encode_decimal",
		"_S",
		"_SL",
		"_R",
		]

pandas.Series.__module_ = "pandas"

_S = TypeVar("_S", bound="Sample")
_SL = TypeVar("_SL", bound="SampleList")
_R = TypeVar("_R", bound="Result")


@prettify_docstrings
class Sample(Dictable):
	"""
	Represents a sample in a MassHunter CSV file.

	:param sample_name:
	:param sample_type:
	:param instrument_name:
	:param position:
	:param user:
	:param acq_method:
	:param da_method:
	:param irm_cal_status:
	:param filename:
	:param results:
	"""

	def __init__(
			self,
			sample_name,
			sample_type,
			instrument_name,
			position,
			user,
			acq_method,
			da_method,
			irm_cal_status,
			filename,
			results=None,
			):

		self.sample_name = sample_name
		self.sample_type = sample_type
		self.instrument_name = instrument_name
		self.position = position
		self.user = user
		self.acq_method = acq_method
		self.da_method = da_method
		self.irm_cal_status = irm_cal_status
		self.filename = filename

		self._results: Dict[float, Result]

		if results is None:
			self._results = {}
		elif isinstance(results, dict):
			self._results = {}

			for cpd_no, compound in results.items():
				if isinstance(compound, dict):
					self._results[cpd_no] = Result(**compound)
				else:
					self._results[cpd_no] = compound
		elif isinstance(results, list):
			self._results = {}

			for compound in results:
				if isinstance(compound, dict):
					tmp_result = Result(**compound)
					cpd_no = tmp_result.index
					self._results[cpd_no] = tmp_result
				else:
					self._results[compound.index] = compound
		else:
			raise TypeError(f"Unknown type for `results`: {type(results)}")

	def add_result(self, result):
		"""
		Add a result to the sample.

		:param result:
		"""

		self._results[result.index] = result

	@property
	def results_list(self) -> List["Result"]:
		"""
		Returns a list of results in the order in which they were identified.

		I.e. sorted by the ``Cpd`` value from the csv export.

		:rtype:

		.. clearpage::
		"""

		results_list = []

		for key in sorted(self._results.keys()):
			results_list.append(self._results[key])

		return results_list

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return (
					self.sample_name == other.sample_name and self.sample_type == other.sample_type
					and self.filename == other.filename and self.acq_method == other.acq_method
					)

	@classmethod
	def from_series(cls: Type[_S], series) -> _S:
		"""
		Constuct a :class:`~.Sample` from a :class:`pandas.Series`.

		:param series:
		:return:
		"""

		sample_name = series["Sample Name"]
		sample_type = series["Sample Type"]
		filename = series["File"]
		instrument_name = series["Instrument Name"]
		position = series["Position"]
		user = series["User Name"]
		acq_method = series["Acq Method"]
		da_method = series["DA Method"]
		irm_cal_status = series["IRM Calibration status"]

		return cls(
				sample_name,
				sample_type,
				instrument_name,
				position,
				user,
				acq_method,
				da_method,
				irm_cal_status,
				filename,
				)

	def __repr__(self):
		return f"Sample({self.sample_name})"

	def to_dict(self):
		"""
		Return a dictionary representation of the class.
		"""

		return AlphaDict(
				sample_name=self.sample_name,
				sample_type=self.sample_type,
				instrument_name=self.instrument_name,
				position=self.position,
				user=self.user,
				acq_method=self.acq_method,
				da_method=self.da_method,
				irm_cal_status=self.irm_cal_status,
				filename=self.filename,
				results=self.results_list
				)


@prettify_docstrings
class Result(Dictable):
	r"""
	Represents a Result in a MassHunter CSV file.

	.. raw:: latex

		\begin{multicols}{2}

	:param cas:
	:param name:
	:param hits:
	:param index:
	:param formula:
	:param score:
	:param abundance:
	:param height:
	:param area:
	:param diff_mDa:
	:param diff_ppm:
	:param rt:
	:param start:
	:param end:
	:param width:
	:param tgt_rt:
	:param rt_diff:
	:param mz:
	:param product_mz:
	:param base_peak:
	:param mass:
	:param average_mass:
	:param tgt_mass:
	:param mining_algorithm:
	:param z_count:
	:param max_z:
	:param min_z:
	:param n_ions:
	:param polarity:
	:param label:
	:param flags:
	:param flag_severity:
	:param flag_severity_code:

	.. raw:: latex

		\end{multicols}
	"""

	def __init__(
			self,
			cas,
			name: str,
			hits,
			index: int = -1,
			formula: str = '',
			score: float = 0.0,
			abundance: float = 0,
			height: float = 0,
			area: float = 0,
			diff_mDa: float = 0.0,
			diff_ppm: float = 0.0,
			rt: float = 0.0,
			start: float = 0.0,
			end: float = 0.0,
			width: float = 0.0,
			tgt_rt: float = 0.0,
			rt_diff: float = 0.0,
			mz: float = 0.0,
			product_mz: float = 0.0,
			base_peak: float = 0.0,
			mass: float = 0.0,
			average_mass: float = 0.0,
			tgt_mass: float = 0.0,
			mining_algorithm: str = '',
			z_count: int = 0,
			max_z: int = 0,
			min_z: int = 0,
			n_ions: int = 0,
			polarity: str = '',
			label: str = '',
			flags: str = '',
			flag_severity: str = '',
			flag_severity_code: int = 0,
			):

		# Possible also AL (ID Source) and AM (ID Techniques Applied)
		self._cas = cas
		self.name: str = str(name)
		self.hits = hits
		self.formula: str = str(formula)
		self.score: Decimal = Decimal(score)
		self.abundance: float = int(abundance)
		self.height: float = int(height)
		self.area: float = int(area)
		self.diff_mDa: Decimal = Decimal(diff_mDa)
		self.diff_ppm: Decimal = Decimal(diff_ppm)
		self.rt: Decimal = Decimal(rt)
		self.start: Decimal = Decimal(start)
		self.end: Decimal = Decimal(end)
		self.width: Decimal = Decimal(width)
		self.tgt_rt: Decimal = Decimal(tgt_rt)
		self.rt_diff: Decimal = Decimal(rt_diff)
		self.mz: Decimal = Decimal(mz)
		self.product_mz: Decimal = Decimal(product_mz)
		self.base_peak: Decimal = Decimal(base_peak)
		self.mass: Decimal = Decimal(mass)
		self.average_mass: Decimal = Decimal(average_mass)
		self.tgt_mass: Decimal = Decimal(tgt_mass)
		self.mining_algorithm: str = str(mining_algorithm)
		self.z_count: int = int(z_count)
		self.max_z: int = int(max_z)
		self.min_z: int = int(min_z)
		self.n_ions: int = int(n_ions)
		self.polarity: str = str(polarity)
		self.label: str = str(label)
		self.flags: str = str(flags)
		self.flag_severity: str = str(flag_severity)
		self.flag_severity_code: int = int(flag_severity_code)
		self.index: int = index  # Tracks the number of the result in the sample

	# "Score (Tgt)",
	@classmethod
	def from_series(cls: Type[_R], series: pandas.Series) -> _R:
		"""
		Consruct a :class:`~.classes.Result` from a :class:`pandas.Series`.

		:param series:

		:rtype:

		.. clearpage::
		"""

		cas = series["CAS"]
		name = series["Name"]
		index = series["Cpd"]
		hits = series["Hits"]
		formula = series["Formula"]
		score = series["Score"]
		abundance = series["Abund"]
		height = series["Height"]
		area = series["Area"]
		diff_mDa = series["Diff (Tgt, mDa)"]
		diff_ppm = series["Diff (Tgt, ppm)"]
		rt = series["RT"]
		start = series["Start"]
		end = series["End"]
		width = series["Width"]
		tgt_rt = series["RT (Tgt)"]
		rt_diff = series["RT Diff (Tgt)"]
		mz = series["m/z"]
		product_mz = series["m/z (prod.)"]
		base_peak = series["Base Peak"]
		mass = series["Mass"]
		average_mass = series["Avg Mass"]
		tgt_mass = series["Mass (Tgt)"]
		mining_algorithm = series["Mining Algorithm"]
		z_count = series["Z Count"]
		max_z = series["Max Z"]
		min_z = series["Min Z"]
		n_ions = series["Ions"]
		polarity = series["Polarity"]
		label = series["Label"]
		flags = series["Flags (Tgt)"]
		flag_severity = series["Flag Severity (Tgt)"]
		flag_severity_code = series["Flag Severity Code (Tgt)"]

		return cls(
				cas,
				name,
				hits,
				index,
				formula,
				score,
				abundance,
				height,
				area,
				diff_mDa,
				diff_ppm,
				rt,
				start,
				end,
				width,
				tgt_rt,
				rt_diff,
				mz,
				product_mz,
				base_peak,
				mass,
				average_mass,
				tgt_mass,
				mining_algorithm,
				z_count,
				max_z,
				min_z,
				n_ions,
				polarity,
				label,
				flags,
				flag_severity,
				flag_severity_code,
				)

	def __repr__(self):
		return f"Result({self.name}; {self.formula}; {self.rt}; {self.score})"

	def to_dict(self):
		"""
		Return a dictionary representation of the class.
		"""

		return AlphaDict(
				cas=self._cas,
				name=self.name,
				hits=self.hits,
				formula=self.formula,
				score=self.score,
				abundance=self.abundance,
				height=self.height,
				area=self.area,
				diff_mDa=self.diff_mDa,
				diff_ppm=self.diff_ppm,
				rt=self.rt,
				start=self.start,
				end=self.end,
				width=self.width,
				tgt_rt=self.tgt_rt,
				rt_diff=self.rt_diff,
				mz=self.mz,
				product_mz=self.product_mz,
				base_peak=self.base_peak,
				mass=self.mass,
				average_mass=self.average_mass,
				tgt_mass=self.tgt_mass,
				mining_algorithm=self.mining_algorithm,
				z_count=self.z_count,
				max_z=self.max_z,
				min_z=self.min_z,
				n_ions=self.n_ions,
				polarity=self.polarity,
				label=self.label,
				flags=self.flags,
				flag_severity=self.flag_severity,
				flag_severity_code=self.flag_severity_code,
				index=self.index,
				)

	def __eq__(self, other):
		if isinstance(other, str):
			return other.casefold() == self.name.casefold()
		else:
			return NotImplemented


class SampleList(List[Sample]):
	"""
	A list of :class:`mh_utils.csv_parser.classes.Sample` objects.
	"""

	@doctools.append_docstring_from(Sample.__init__)
	def add_new_sample(self, *args, **kwargs):
		"""
		Add a new sample to the list and return the
		:class:`~classes.Sample` object representing it.

		"""  # noqa: D400

		tmp_sample = Sample(*args, **kwargs)
		return self.add_sample(tmp_sample)

	def add_sample(self, sample: Sample) -> Sample:
		"""
		Add a :class:`~.Sample` object to the list.

		:param sample:

		:rtype:

		.. clearpage::
		"""

		if sample in self:
			return self[self.index(sample)]
		else:
			self.append(sample)
			return sample

	# def find_sample(self, sample_name: str) -> Optional[Sample]:
	# 	if sample_name in self:
	# 		return self[self.index(sample_name)]
	# 	else:
	# 		return None

	def add_sample_from_series(self, series: pandas.Series) -> Sample:
		"""
		Create a new sample object from a :class:`pandas.series` and add it to the list.

		:returns: The newly created :class:`~classes.Sample` object.

		:param series:
		"""

		tmp_sample = Sample.from_series(series)
		return self.add_sample(tmp_sample)

	def sort_samples(self, key: str, reverse: bool = False):
		"""
		Sort the list of :class:`~.Samples` in place.

		:param key: The name of the property in the sample to sort by.
		:param reverse: Whether the list should be sorted in reverse order.

		:rtype:

		.. clearpage::
		"""

		self.sort(key=lambda samp: getattr(samp, key), reverse=reverse)

	def reorder_samples(self, order_mapping: Dict, key: str = "sample_name"):
		"""
		Reorder the list of :class:`~.Samples` in place.

		:param order_mapping: A mapping between sample names and their new position in the list.
			For example:

				.. code-block:: python

					order_mapping = {
						"Propellant 1ug +ve": 0,
						"Propellant 1mg +ve": 1,
						"Propellant 1ug -ve": 2,
						"Propellant 1mg -ve": 3,
						}

		:param key: The name of the property in the sample to sort by.
		"""

		self.sort(key=lambda s: order_mapping[getattr(s, key)], reverse=True)

	def rename_samples(self, rename_mapping: Dict, key: str = "sample_name"):
		r"""
		Rename the samples in the list.

		:param rename_mapping: A mapping between current sample names and their new names.
		:param key: The name of the property in the sample to sort by.

		Use ``rename_mapping=``\:py:obj:`None` or omit the sample from the ``rename_mapping`` entirely
		to leave the name unchanged.

		For example:

		.. code-block:: python

			rename_mapping = {
				"Propellant 1ug +ve": "Alliant Unique 1µg/L +ESI",
				"Propellant 1mg +ve": "Alliant Unique 1mg/L +ESI",
				"Propellant 1mg -ve": None,
				}
		"""

		for sample in self:
			if getattr(sample, key) in rename_mapping and rename_mapping[getattr(sample, key)]:
				sample.sample_name = rename_mapping.pop(getattr(sample, key))

	def get_areas_and_scores(
			self,
			compound_name: str,
			include_none: bool = False,
			) -> Tuple[OrderedDict, OrderedDict]:
		"""
		Returns two dictionaries: one containing sample names and peak areas for the
		compound with the given name, the other containing sample names and scores.

		:param compound_name:
		:param include_none: Whether samples where the compound was not found
			should be included in the results.
		"""  # noqa: D400

		peak_areas: "OrderedDict[str, Optional[float]]" = OrderedDict()
		scores: "OrderedDict[str, Optional[Decimal]]" = OrderedDict()

		for sample in self:
			for result in sample.results_list:
				if result.name == compound_name:
					peak_areas[sample.sample_name] = result.area
					scores[sample.sample_name] = result.score
					break
			else:
				if include_none:
					peak_areas[sample.sample_name] = None
					scores[sample.sample_name] = None

		return peak_areas, scores

	def get_retention_times(self, compound_name: str, include_none: bool = False) -> OrderedDict:
		"""
		Returns a dictionary containing sample names and retention times for the
		compound with the given name.

		:param compound_name:
		:param include_none: Whether samples where the compound was not found
			should be included in the results.
		"""  # noqa: D400

		times = OrderedDict()

		for sample in self:
			for result in sample.results_list:
				if result.name == compound_name:
					times[sample.sample_name] = float(result.rt)
					break
			else:
				if include_none:
					times[sample.sample_name] = numpy.nan

		return times

	def get_peak_areas(self, compound_name: str, include_none: bool = False) -> OrderedDict:
		"""
		Returns a dictionary containing sample names and peak areas for the
		compound with the given name.

		:param compound_name:
		:param include_none: Whether samples where the compound was not found
			should be included in the results.
		"""  # noqa: D400

		return self.get_areas_and_scores(compound_name, include_none)[0]

	def get_areas_for_compounds(
			self,
			compound_names: Iterable[str],
			include_none: bool = False,
			) -> "SamplesAreaDict":
		"""
		Returns a dictionary containing sample names and peak areas for the
		compounds with the given names.

		:param compound_names:
		:param include_none: Whether samples where none of the specified compounds
			were found should be included in the results.
		"""  # noqa: D400

		all_areas, all_scores = self.get_areas_and_scores_for_compounds(compound_names, include_none)
		return all_areas

	def get_areas_and_scores_for_compounds(
			self,
			compound_names: Iterable[str],
			include_none: bool = False,
			) -> Tuple["SamplesAreaDict", "SamplesScoresDict"]:
		"""
		Returns two dictionaries: one containing sample names and peak areas for the
		compounds with the given names, the other containing sample names and scores.

		:param compound_names:
		:param include_none: Whether samples where none of the specified compounds
			were found should be included in the results.

		:rtype:

		.. clearpage::
		"""  # noqa: D400

		tmp_all_areas = SamplesAreaDict()
		tmp_all_scores = SamplesScoresDict()

		for name in compound_names:
			areas = self.get_peak_areas(name, True)
			scores = self.get_scores(name, True)

			for sample_name, area in areas.items():
				if sample_name not in tmp_all_areas:
					tmp_all_areas[sample_name] = dict()
					tmp_all_scores[sample_name] = dict()

				tmp_all_areas[sample_name][name] = area
				tmp_all_scores[sample_name][name] = scores[sample_name]

		if include_none:
			return tmp_all_areas, tmp_all_scores

		else:
			all_areas = SamplesAreaDict()
			all_scores = SamplesScoresDict()

			for sample_name, compound_areas in tmp_all_areas.items():
				if any(list(compound_areas.values())):
					all_areas[sample_name] = compound_areas
					all_scores[sample_name] = tmp_all_scores[sample_name]

			return all_areas, all_scores

	def get_compounds(self) -> List[str]:
		"""
		Returns a list containing the names of the compounds present in the samples in alphabetical order.
		"""

		compounds = set()

		for sample in self:
			for result in sample.results_list:
				compounds.add(result.name)

		return sorted(compounds)

	def get_scores(self, compound_name: str, include_none: bool = False) -> OrderedDict:
		"""
		Returns a dictionary containing sample names and scores for the
		compound with the given name.

		:param compound_name:
		:param include_none: Whether samples where the compound was not found
			should be included in the results.

		:rtype:

		.. clearpage::
		"""  # noqa: D400

		return self.get_areas_and_scores(compound_name, include_none)[1]

	def filter(  # noqa: A003  # pylint: disable=redefined-builtin
		self: _SL,
		sample_names: Iterable[str],
		key: str = "sample_name",
		exclude: bool = False,
		) -> _SL:
		"""
		Filter the list to only contain sample_names whose name is in ``sample_names``.

		:param sample_names: A list of sample names to include
		:param key: The name of the property in the sample to sort by.
		:param exclude: If :py:obj:`True`, any sample whose name is in ``sample_names``
			will be excluded from the output, rather than included.
		"""

		new_sample_list = self.__class__()

		for sample in self:
			if exclude:
				if getattr(sample, key) in sample_names:
					continue
			else:
				if getattr(sample, key) not in sample_names:
					continue

			new_sample_list.append(sample)

		return new_sample_list

	@property
	def sample_names(self) -> List[str]:
		"""
		Returns a list of sample names in the :class:`~.classes.SampleList`.
		"""

		return [sample.sample_name for sample in self]

	@classmethod
	def from_json_file(cls: Type[_SL], filename: PathLike, **kwargs) -> _SL:
		r"""
		Construct a :class:`~.classes.SampleList` from JSON file.

		:param filename: The filename of the JSON file.
		:param \*\*kwargs: Keyword arguments passed to :meth:`domdf_python_tools.paths.PathPlus.load_json`.
		"""

		all_samples = cls()

		for sample in PathPlus(filename).load_json(
				json_library=sdjson,  # type: ignore
				**kwargs,
				):
			all_samples.append(Sample(**sample))

		return all_samples


class BaseSamplePropertyDict(OrderedDict):
	"""
	OrderedDict to store a single property of a set of samples.

	Keys are the sample names and the values are dictionaries mapping compound names to property values.
	"""

	@property
	def sample_names(self) -> List[str]:
		"""
		Returns a list of sample names in the :class:`~.BaseSamplePropertyDict`.
		"""

		return list(self.keys())

	@property
	def n_samples(self) -> int:
		"""
		Returns the number of samples in the :class:`~.BaseSamplePropertyDict`.
		"""

		return len(self.keys())

	@property
	def n_compounds(self) -> int:
		"""
		Returns the number of compounds in the :class:`~.BaseSamplePropertyDict`.
		"""

		for val in self.values():
			return len(val)
		return 0


class SamplesAreaDict(BaseSamplePropertyDict):
	"""
	:class:`collections.OrderedDict` to store area information parsed from MassHunter results CSV files.
	"""

	def get_compound_areas(self, compound_name: str) -> List[float]:
		"""
		Get the peak areas for the given compound in every sample.

		:param compound_name:
		"""

		areas = []

		for sample_name, compound_areas in self.items():
			for name, area in compound_areas.items():
				if compound_name == name:
					if area is None:
						areas.append(0.0)
					else:
						areas.append(area)

		return areas


class SamplesScoresDict(BaseSamplePropertyDict):
	"""
	:class:`collections.OrderedDict` to store score information parsed from MassHunter results CSV files.
	"""

	def get_compound_scores(self, compound_name: str) -> List[float]:
		"""
		Get the peak scores for the given compound in every sample.

		:param compound_name:
		"""

		scores = []

		for sample_name, compound_scores in self.items():
			for name, score in compound_scores.items():
				if compound_name == name:
					if score is None:
						scores.append(0.0)
					else:
						scores.append(score)

		return scores


@sdjson.encoders.register(Sample)
@sdjson.encoders.register(Result)
def encode_result_or_sample(obj):  # noqa: D103
	return dict(obj)


@sdjson.encoders.register(set)
def encode_set(obj):  # noqa: D103
	return list(obj)


@sdjson.encoders.register(Decimal)
def encode_decimal(obj):  # noqa: D103
	return str(obj)
