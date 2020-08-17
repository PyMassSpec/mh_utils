# stdlib
from datetime import timedelta

# 3rd party
import lxml.objectify
import pytest

# this package
from mh_utils.cef_parser import Device, Peak, RTRange, Spectrum, make_timedelta


class TestCreation:

	def test_spectrum_type(self):
		assert Spectrum(spectrum_type="FbF").spectrum_type == "FbF"

	def test_algorithm(self):
		assert Spectrum(algorithm="FindByFormula").algorithm == "FindByFormula"

	def test_saturation_limit(self):
		assert Spectrum(saturation_limit=10000).saturation_limit == 10000
		assert Spectrum(saturation_limit="10000").saturation_limit == 10000

	def test_scans(self):
		assert Spectrum(scans=1).scans == 1
		assert Spectrum(scans="1").scans == 1

	def test_scan_type(self):
		assert Spectrum(scan_type="Scan").scan_type == "Scan"

	def test_ionisation(self):
		assert Spectrum(ionisation="Esi").ionisation == "Esi"

	def test_polarity(self):
		assert Spectrum(polarity="+").polarity == 1
		assert Spectrum(polarity="positive").polarity == 1
		assert Spectrum(polarity=1).polarity == 1
		assert Spectrum(polarity="-").polarity == -1
		assert Spectrum(polarity="negative").polarity == -1
		assert Spectrum(polarity=-1).polarity == -1
		assert Spectrum(polarity=0).polarity == 0
		assert Spectrum(polarity=22).polarity == 22

	def test_peaks(self):
		assert Spectrum().peaks == []
		assert Spectrum(peaks=[]).peaks == []
		assert Spectrum(peaks=()).peaks == []
		assert Spectrum(
				peaks=[Peak(170.0965, 172.1028, 890559.25, 1, "M+H")],
				).peaks == [Peak(170.0965, 172.1028, 890559.25, 1, "M+H")]

	def test_rt_ranges(self):
		assert Spectrum().rt_ranges == []
		assert Spectrum(rt_ranges=[]).rt_ranges == []
		assert Spectrum(rt_ranges=()).rt_ranges == []
		assert Spectrum(rt_ranges=[RTRange(12, 34)], ).rt_ranges == [RTRange(12, 34)]

	def test_voltage(self):
		assert Spectrum(voltage="1234V").voltage == 1234.0
		assert Spectrum(voltage="1234").voltage == 1234.0
		assert Spectrum(voltage="1234.0V").voltage == 1234.0
		assert Spectrum(voltage="1234.0").voltage == 1234.0
		assert Spectrum(voltage=1234.0).voltage == 1234.0
		assert Spectrum(voltage=1234).voltage == 1234.0
		assert Spectrum(voltage="ABCDEFG").voltage == 0


def test_dict():
	assert dict(
			Spectrum(
					spectrum_type="FbF",
					algorithm="FindByFormula",
					saturation_limit=10000,
					scans=1,
					scan_type="Scan",
					ionisation="Esi",
					polarity="+",
					peaks=[Peak(170.0965, 172.1028, 890559.25, 1, "M+H")],
					rt_ranges=[RTRange(12, 34)],
					)
			) == {
					"spectrum_type": "FbF",
					"algorithm": "FindByFormula",
					"saturation_limit": 10000,
					"scans": 1,
					"scan_type": "Scan",
					"ionisation": "Esi",
					"polarity": 1,
					"peaks": [Peak(170.0965, 172.1028, 890559.25, 1, "M+H")],
					"rt_ranges": [RTRange(12, 34)],
					"voltage": 0.0,
					"device": None,
					}


def test_repr():
	assert str(
			Spectrum(
					spectrum_type="FbF",
					algorithm="FindByFormula",
					saturation_limit=10000,
					scans=1,
					scan_type="Scan",
					ionisation="Esi",
					polarity="+",
					peaks=[Peak(170.0965, 172.1028, 890559.25, 1, "M+H")],
					rt_ranges=[RTRange(12, 34)],
					)
			) == "<Spectrum([Peak(x=170.0965, rx=172.1028, y=890559.25, charge=1, label='M+H')])>"

	assert repr(
			Spectrum(
					spectrum_type="FbF",
					algorithm="FindByFormula",
					saturation_limit=10000,
					scans=1,
					scan_type="Scan",
					ionisation="Esi",
					polarity="+",
					peaks=[Peak(170.0965, 172.1028, 890559.25, 1, "M+H")],
					rt_ranges=[RTRange(12, 34)],
					)
			) == "<Spectrum([Peak(x=170.0965, rx=172.1028, y=890559.25, charge=1, label='M+H')])>"


raw_xml_fbf = """
<Spectrum type="FbF" cpdAlgo="FindByFormula">
	<MSDetails scanType="Scan" is="Esi" p="+" />
	<Device type="QuadrupoleTimeOfFlight" num="1" />
	<MSPeaks>
		<p x="195.0612" rx="195.0652" y="690.56" z="1" s="M+H" />
		<p x="196.0679" rx="196.0686" y="22.97" z="1" s="M+H+1" />
		<p x="217.0466" rx="217.0471" y="1286.60" z="1" s="M+Na" />
		<p x="219.0532" rx="219.0524" y="44.93" z="1" s="M+Na+1" />
	</MSPeaks>
</Spectrum>
"""

fbf_expects = Spectrum(
		spectrum_type="FbF",
		algorithm="FindByFormula",
		scans=0,
		scan_type="Scan",
		ionisation="Esi",
		polarity="+",
		peaks=[
				Peak(x=195.0612, rx=195.0652, y=690.56, charge=1, label="M+H"),
				Peak(x=196.0679, rx=196.0686, y=22.97, charge=1, label="M+H+1"),
				Peak(x=217.0466, rx=217.0471, y=1286.60, charge=1, label="M+Na"),
				Peak(x=219.0532, rx=219.0524, y=44.93, charge=1, label="M+Na+1"),
				],
		device=Device("QuadrupoleTimeOfFlight", 1),
		)

raw_xml_tof = """
<Spectrum type="TOF-MS1" satLimit="16742400" scans="28" cpdAlgo="FindByFormula">
	<MSDetails scanType="Scan" is="Esi" p="+" fv="380.0V" />
	<RTRanges>
		<RTRange min="12.158" max="12.461" />
	</RTRanges>
	<Device type="QuadrupoleTimeOfFlight" num="1" />
	<MassCalibration>
		<CalStep form="Traditional">
			<Count>2</Count>
			<C_0>0.00034578342199811013</C_0>
			<C_1>1006.6240909968859</C_1>
		</CalStep>
		<CalStep form="Polynomial">
			<CoefficientUse>15</CoefficientUse>
			<Count>8</Count>
			<C_0>32433.019820064987</C_0>
			<C_1>113829.99741591697</C_1>
			<C_2>0.003090538282418261</C_2>
			<C_3>-2.1307283327743463E-07</C_3>
			<C_4>3.8289087857717937E-12</C_4>
			<C_5>-1.9689925889819158E-17</C_5>
			<C_6>0</C_6>
			<C_7>0</C_7>
		</CalStep>
	</MassCalibration>
	<MSPeaks>
		<p x="195.0612" rx="195.0652" y="690.56" z="1" s="M+H" />
		<p x="196.0679" rx="196.0686" y="22.97" z="1" s="M+H+1" />
		<p x="217.0466" rx="217.0471" y="1286.60" z="1" s="M+Na" />
		<p x="219.0532" rx="219.0524" y="44.93" z="1" s="M+Na+1" />
	</MSPeaks>
</Spectrum>
"""

tof_expects = Spectrum(
		spectrum_type="TOF-MS1",
		saturation_limit=16742400,
		algorithm="FindByFormula",
		voltage=380.0,
		scans=28,
		scan_type="Scan",
		ionisation="Esi",
		polarity="+",
		rt_ranges=[RTRange(12.158, 12.461)],
		peaks=[
				Peak(x=195.0612, rx=195.0652, y=690.56, charge=1, label="M+H"),
				Peak(x=196.0679, rx=196.0686, y=22.97, charge=1, label="M+H+1"),
				Peak(x=217.0466, rx=217.0471, y=1286.60, charge=1, label="M+Na"),
				Peak(x=219.0532, rx=219.0524, y=44.93, charge=1, label="M+Na+1"),
				],
		device=Device("QuadrupoleTimeOfFlight", 1),
		)


@pytest.mark.parametrize("raw_xml, expects", [
		(raw_xml_fbf, fbf_expects),
		(raw_xml_tof, tof_expects),
		])
def test_from_xml(raw_xml, expects):
	tree = lxml.objectify.fromstring(raw_xml)
	spec = Spectrum.from_xml(tree)
	assert spec == expects
