#!/usr/bin/env python3
#
#  __init__.py
"""
Parser for MassHunter Compound Exchange Format ``.cef`` files.

A CEF file represents a file identified in LC-MS data by MassHunter Qualitative.
It consists of a list of compounds encapsulated in a :class:`~.CompoundList`.

A :class:`~.CompoundList` consists of :class:`~.Compound` objects representing the
individual compounds identified in the data. Each :class:`~.Compound` object contains
information on the location of that compound within the LC data (:attr:`~.Compound.location`),
the scores indicating the confidence of the match (:attr:`~.Compound.compound_scores`),
a list of possible matching compounds (:attr:`~.Compound.results`),
and the matching mass spectrum extracted from the LC-MS data (:attr:`~.Compound.spectra`).

The following diagram represents this structure:

* :class:`CompoundList`

	+ :class:`Compound`

		- :attr:`Compound.algo` ⇨ :class:`str`
		- :attr:`Compound.location` ⇨ :class:`~typing.Optional` [:class:`LocationDict` ]
		- :attr:`Compound.compound_scores` ⇨ :class:`~typing.Optional` [:class:`~typing.Dict` [:class:`str`, :class:`~.Score` ] ]
		- :attr:`Compound.results` ⇨ :class:`~typing.List`

			- :class:`~.Molecule`
			- Another :class:`~.Molecule`
			- ``...``

		- :attr:`Compound.spectra` ⇨ :class:`~typing.List`

			- :class:`~.Spectrum`
			- Another :class:`~.Spectrum`
			- ``...``



	+ Another :class:`Compound`
	+ ``...``

"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import datetime
import re
from pprint import pformat
from typing import Dict, Iterable, List, Optional, Sequence, Type, Union

# 3rd party
import attr
import lxml.objectify
from attr_utils.docstrings import add_attrs_doc
from chemistry_tools.formulae import Formula
from domdf_python_tools.bases import Dictable, NamedList
from domdf_python_tools.typing import PathLike
from lxml import objectify
from typing_extensions import TypedDict

__all__ = [
		"Molecule",
		"Device",
		"Peak",
		"Spectrum",
		"make_timedelta",
		"RTRange",
		"Flag",
		"Score",
		"parse_compound_scores",
		"parse_match_scores",
		"LocationDict",
		"Compound",
		"CompoundList",
		"parse_cef",
		]


class Molecule(Dictable):
	"""
	Represents a molecule in a CEF file.


	:param name: The name of the compound
	:param formula: The formula of the compound.
		If a string it must be parsable	by :class:`chemistry_tools.formulae.Formula`
	:param matches: Dictionary of also:score match values
	"""

	def __init__(
			self,
			name: str,
			formula: Union[str, Formula, None] = None,
			matches: Optional[Dict[str, "Score"]] = None,
			):

		super().__init__()

		self.name = str(name)
		if isinstance(formula, Formula):
			self.formula = formula
		elif formula is not None:
			self.formula = Formula.from_string(formula)
		else:
			self.formula = Formula()

		if isinstance(matches, dict):
			self.matches = matches
		elif matches is None:
			self.matches = {}
		else:
			raise TypeError(f"'matches' must be a dictionary, not {type(matches)}")

	@property
	def __dict__(self):
		return dict(
				name=self.name,
				formula=self.formula,
				matches=self.matches,
				)

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Molecule":
		"""
		Construct a :class:`~.Molecule` object from an XML element.

		:param element: a Molecule XML element
		"""

		return cls(
				name=element.attrib["name"],
				formula=element.attrib["formula"],
				matches=parse_match_scores(element.MatchScores),
				)

	def __repr__(self):
		return f"<Molecule({self.name}, {str(self.formula)})>"


@add_attrs_doc
@attr.s(slots=True)
class Device:
	"""
	Represents the device that acquired a :class:`~.Spectrum`.

	:param device_type: String identifying the type of device.
	:param number:
	"""

	device_type: str = attr.ib(converter=str)
	number: int = attr.ib(converter=int)

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Device":
		"""
		Construct a :class:`~.Device` object from an XML element.

		:param element: a ``<Device>`` XML element from a CEF file
		"""

		device_type = element.attrib["type"]
		number = element.attrib["num"]
		return cls(device_type=device_type, number=number)


@add_attrs_doc
@attr.s(slots=True)
class Peak:
	"""
	A peak in a Mass Spectrum

	:param x:
	:param rx:
	:param y:
	:param charge:
	:type charge: int
	:param label:
	:type label: str
	"""

	x: float = attr.ib(converter=float)
	rx: float = attr.ib(converter=float)
	y: float = attr.ib(converter=float)
	charge: int = attr.ib(converter=int, default=0)  #: The charge on the peak.
	label: str = attr.ib(converter=str, default='')  #: The label of the peak, e.g. "M+H"

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Peak":
		"""
		Construct a :class:`~.Peak` object from an XML element.

		:param element: a ``<p>`` XML element from an <MSPeaks> element of a CEF file
		"""

		data = dict(element.attrib)
		data["charge"] = data.pop("z", 0)
		data["label"] = data.pop("s", '')
		return cls(**data)


class Spectrum(Dictable):
	"""
	Agilent cef Spectrum

	:param spectrum_type: The type of spectrum e.g. "FbF"
	:param algorithm: The algorithm used to identify the compound
	:param saturation_limit: Unknown. Might mean saturation limit?
	:param scans: Unknown. Presumably the number of scans that make up the spectrum?
	:param scan_type:
	:param ionisation: The type of ionisation e.g. ESI
	:param polarity: The polarity of the ionisation
	:param device: The device that acquired the data
	:param peaks: A list of identified peaks in the mass spectrum
	:param rt_ranges: A list of retention time ranges for the mass spectrum
	"""

	def __init__(
			self,
			spectrum_type: str = '',
			algorithm: str = '',
			saturation_limit: int = 0,
			scans: int = 0,
			scan_type: str = '',
			ionisation: str = '',
			polarity: Union[str, int] = 0,
			voltage: Union[str, float] = 0.0,
			device: Optional[Device] = None,
			peaks: Optional[Sequence[Peak]] = None,
			rt_ranges: Optional[Sequence["RTRange"]] = None,
			):
		super().__init__()

		self.spectrum_type = str(spectrum_type)
		self.saturation_limit = int(saturation_limit)
		self.scans = int(scans)
		self.algorithm = str(algorithm)
		self.scan_type = str(scan_type)
		self.ionisation = str(ionisation)

		if isinstance(voltage, str):
			m = re.match(r"([0-9]+\.?[0-9]*)", voltage)
			if m is not None and m.group(1):
				self.voltage = float(m.group(1))
			else:
				self.voltage = 0
		else:
			self.voltage = float(voltage)

		self.polarity: int

		if polarity in {"+", 1, "1"}:
			self.polarity = 1
		elif polarity in {"-", -1, "-1"}:
			self.polarity = -1
		elif isinstance(polarity, str) and polarity.lower() == "positive":
			self.polarity = 1
		elif isinstance(polarity, str) and polarity.lower() == "negative":
			self.polarity = -1
		else:
			self.polarity = int(polarity)

		self.device = device

		if peaks is None:
			self.peaks = []
		else:
			self.peaks = list(peaks)

		if rt_ranges is None:
			self.rt_ranges = []
		else:
			self.rt_ranges = list(rt_ranges)

	__slots__ = [
			"spectrum_type",
			"saturation_limit",
			"scans",
			"algorithm",
			"scan_type",
			"ionisation",
			"voltage",
			"polarity",
			"device",
			"peaks",
			"rt_ranges",
			]

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Spectrum":
		"""
		Construct a :class:`~.Spectrum` object from an XML element.

		:param element: a Spectrum XML element from a CEF file
		"""

		data = {}

		data["spectrum_type"] = element.attrib["type"]
		data["algorithm"] = element.attrib["cpdAlgo"]

		if "satLimit" in element.attrib:
			data["saturation_limit"] = element.attrib["satLimit"]
		if "scans" in element.attrib:
			data["scans"] = element.attrib["scans"]

		data["scan_type"] = element.MSDetails.attrib["scanType"]
		data["ionisation"] = element.MSDetails.attrib["is"]
		data["polarity"] = element.MSDetails.attrib["p"]
		if "fv" in element.MSDetails.attrib:
			data["voltage"] = element.MSDetails.attrib["fv"]

		data["device"] = Device.from_xml(element.Device)
		data["peaks"] = [Peak.from_xml(p) for p in element.MSPeaks.findall("p")]

		if element.findall("RTRanges"):
			data["rt_ranges"] = [RTRange.from_xml(r) for r in element.RTRanges.findall("RTRange")]

		# TODO: <MassCalibration>

		return cls(**data)

	def __repr__(self):
		return f"<Spectrum({pformat(self.peaks)})>"


def make_timedelta(minutes: Union[float, datetime.timedelta]):
	"""
	Construct a timedelta from a value in minutes.

	:param minutes:
	"""

	if not isinstance(minutes, datetime.timedelta):
		minutes = datetime.timedelta(minutes=float(minutes))

	return minutes


@add_attrs_doc
@attr.s(slots=True)
class RTRange:
	"""
	Represents an ``<RTRange>`` element from a CEF file.

	:param start: start time in minutes
	:param end: end time in minutes
	"""

	start: datetime.timedelta = attr.ib(converter=make_timedelta, default=0.0)  # type: ignore
	end: datetime.timedelta = attr.ib(converter=make_timedelta, default=0.0)  # type: ignore

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "RTRange":
		"""
		Construct ab :class:`~.RTRange` object from an XML element.

		:param element: The ``<RTRange>`` XML element to parse the data from.
		"""

		start = element.attrib["min"]
		end = element.attrib["max"]

		return cls(start, end)


class Flag(str):
	"""
	Represents a flag in a score, to warn that the identification of a compound is poor.

	:param string: The text of the flag
	:param severity: The severity of the flag
	"""

	severity: int

	def __new__(cls: Type["Flag"], string: str, severity: int) -> "Flag":
		obj = super().__new__(cls, str(string))  # type: ignore
		obj.severity = int(severity)

		return obj

	def __eq__(self, other) -> bool:
		if isinstance(other, Flag):
			return str(self) == str(other) and self.severity == other.severity
		else:
			return super().__eq__(other)

	def __ne__(self, other) -> bool:
		return NotImplemented

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({str(self)!r}, severity={self.severity})"

	def __bool__(self) -> bool:
		return bool(str(self)) and bool(self.severity)


class Score(float):
	"""
	A score indicating how well the compound matches the observed spectrum.

	:param score: The score
	:param flag_string: Optional flag. See :class:`~.Flag` for details.
	:param flag_severity: The severity of the flag.
	"""

	flag: Flag

	def __init__(self, score, flag_string: str = '', flag_severity: int = 0):
		float.__init__(float(score))

	def __new__(cls, score, flag_string: str = '', flag_severity: int = 0) -> "Score":
		obj = super().__new__(cls, float(score))  # type: ignore
		obj.flag = Flag(flag_string, flag_severity)

		return obj

	def __repr__(self) -> str:
		if self.flag:
			return f"{self.__class__.__name__}({str(self)}, {self.flag!r})"
		else:
			return f"{self.__class__.__name__}({str(self)})"

	def __str__(self) -> str:
		return str(float(self))

	def __eq__(self, other) -> bool:
		if isinstance(other, Score):
			return float(self) == float(other) and self.flag == other.flag
		else:
			return super().__eq__(other)

	def __ne__(self, other) -> bool:
		return NotImplemented


def parse_compound_scores(element: lxml.objectify.ObjectifiedElement) -> Dict[str, Score]:
	"""
	Parse a ``<CompoundScores>`` element into a dictionary mapping algorithms to scores.

	:param element: a CompoundScores XML element.
	"""

	compound_scores: Dict[str, Score] = {}

	for score in element.findall("CpdScore"):
		algo: str = score.attrib["algo"]
		score = Score(
				score.attrib["score"],
				score.attrib.get("tgtFlagsString", ''),
				score.attrib.get("tgtFlagsSeverity", 0),
				)
		compound_scores[algo] = score

	return compound_scores


def parse_match_scores(element: lxml.objectify.ObjectifiedElement) -> Dict[str, Score]:
	"""
	Parse a ``<MatchScores>`` element into a dictionary mapping algorithms to scores.

	:param element: a MatchScores XML element.
	"""

	match_scores: Dict[str, Score] = {}

	for score in element.findall("Match"):
		algo: str = score.attrib["algo"]
		score = Score(
				score.attrib["score"],
				score.attrib.get("tgtFlagsString", ''),
				score.attrib.get("tgtFlagsSeverity", 0),
				)
		match_scores[algo] = score

	return match_scores


class LocationDict(TypedDict, total=False):
	"""
	:class:`~typing.TypedDict` representing the location of a spectrum within mass spectrometry data.
	"""

	m: float  #: the accurate mass of the compound, determined from the observed mass spectrum.
	rt: float  #: The retention time at which the compound was detected.
	a: float  #: The area of the peak in the EIC.
	y: float  #: The height of the peak in the EIC.


class Compound(Dictable):
	"""
	Represents a compound identified in mass spectral data by MassHunter Qualitative.

	:param algo: The algorithm used to identify the compound.
	:param location: A dictionary of information to locate the compound in the spectral data
	:param compound_scores: A dictionary of compound scores
	:param results: A list of molecules that match the spectrum.
	:param spectra: A list of spectra for the compound.
	"""

	algo: str  #: The algorithm used to identify the compound.
	location: Optional[LocationDict]  #: A dictionary of information to locate the compound in the spectral data
	compound_scores: Optional[Dict[str, "Score"]]  #: A dictionary of compound scores
	results: Optional[List[Molecule]]  #: A list of molecules that match the spectrum.
	spectra: Optional[List[Spectrum]]  #: A list of spectra for the compound.

	def __init__(
			self,
			algo: str = '',
			location: Optional[LocationDict] = None,
			compound_scores: Optional[Dict[str, "Score"]] = None,
			results: Optional[Sequence[Molecule]] = None,
			spectra: Optional[Sequence[Spectrum]] = None,
			):
		super().__init__()

		self.algo = str(algo)

		if location:
			self.location = location
		else:
			self.location = {}

		if compound_scores:
			self.compound_scores = compound_scores
		else:
			self.compound_scores = {}

		if results:
			self.results = list(results)
		else:
			self.results = []

		if spectra:
			self.spectra = list(spectra)
		else:
			self.spectra = []

	@property
	def __dict__(self):
		return dict(
				algo=self.algo,
				location=self.location,
				compound_scores=self.compound_scores,
				results=self.results,
				spectra=self.spectra,
				)

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Compound":
		"""
		Construct a :class:`~.Compound` object from an XML element.

		:param element: a Compound XML element from a CEF file.
		"""

		location: LocationDict = {}
		if "m" in element.Location.attrib:
			location["m"] = float(element.Location.attrib["m"])
		if "rt" in element.Location.attrib:
			location["rt"] = float(element.Location.attrib["rt"])
		if "a" in element.Location.attrib:
			location["a"] = int(element.Location.attrib["a"])
		if "y" in element.Location.attrib:
			location["y"] = int(element.Location.attrib["y"])

		results: List[Molecule] = []
		for molecule in element.Results.findall("Molecule"):
			results.append(Molecule.from_xml(molecule))

		spectra: List[Spectrum] = []
		for spectrum in element.findall("Spectrum"):
			spectra.append(Spectrum.from_xml(spectrum))

		return cls(
				algo=element.attrib["algo"],
				location=location,
				compound_scores=parse_compound_scores(element.CompoundScores),
				results=results,
				spectra=spectra,
				)

	def __repr__(self):
		return f"<Compound({pformat(self.results)})>"


class CompoundList(NamedList):
	"""
	A list of Compound objects parsed from a CEF file.

	The full :class:`list` API is available for this class.

	:param instrument: String identifying the instrument that acquired the data.
	:param compounds: List of compounds identified in the mass spectrometry data.
	"""

	instrument: str  #: The type of instrument that obtained the data, e.g. ``"LCQTOF"``.

	def __init__(self, instrument: str = '', compounds: Optional[Iterable[Compound]] = None):
		super().__init__(compounds)
		self.instrument = str(instrument)

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "CompoundList":
		"""
		Construct a :class:`~.CompoundList` object from an XML element.

		:param element: The XML element to parse the data from.
		"""

		return cls(
				instrument=element.attrib["instrumentConfiguration"],
				compounds=(Compound.from_xml(compound) for compound in element.findall("Compound")),
				)

	def __str__(self) -> str:
		"""
		Returns the list as a string.
		"""

		return f"{self.__class__.__name__}{pformat(list(self))}"


def parse_cef(filename: PathLike) -> CompoundList:
	"""
	Construct an :class:`~.CompoundList` object from the given ``.cef`` file.

	:param filename: The filename of the CEF file to read.
	"""

	tree = objectify.parse(str(filename))
	root = tree.getroot()
	version = root.attrib["version"]
	compounds = CompoundList.from_xml(root.CompoundList)

	return compounds
