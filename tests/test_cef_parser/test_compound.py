# stdlib
import copy

# 3rd party
import lxml.objectify  # type: ignore
import pytest
from domdf_python_tools.paths import PathPlus
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from mh_utils.cef_parser import Compound, CompoundList, Device, Molecule, Peak, RTRange, Score, Spectrum, parse_cef


@pytest.fixture()
def spectrum():
	return Spectrum(
			spectrum_type="FbF",
			algorithm="FindByFormula",
			saturation_limit=10000,
			scans=1,
			scan_type="Scan",
			ionisation="Esi",
			polarity='+',
			peaks=[Peak(170.0965, 172.1028, 890559.25, 1, "M+H")],
			rt_ranges=[RTRange(12, 34)],
			)


@pytest.fixture()
def molecule():
	return Molecule(name="Dimethyl Phthalate", formula="C10 H10 O4")


@pytest.fixture()
def compound(spectrum, molecule):
	return Compound(
			algo="FindByFormula",
			location={'m': 169.0893, "rt": 13.649, 'a': 29388223, 'y': 3377289},
			results=[molecule],
			spectra=[spectrum],
			compound_scores={"fbf": Score(62.90, flag_string="low score", flag_severity=2)},
			)


class TestCreation:

	def test_algo(self):
		assert Compound(algo="FindByFormula").algo == "FindByFormula"

	def test_location(self):
		assert Compound(
				algo="FindByFormula", location={'m': 169.0893, "rt": 13.649, 'a': 29388223, 'y': 3377289}
				).location == {'m': 169.0893, "rt": 13.649, 'a': 29388223, 'y': 3377289}
		assert Compound(
				algo="FindByFormula", location={'m': 169.0893, "rt": 13.649, 'a': 29388223, 'y': 3377289}
				).location == {'m': 169.0893, "rt": 13.649, 'a': 29388223, 'y': 3377289}
		assert Compound(algo="FindByFormula").location == {}

	@pytest.mark.parametrize(
			"scores",
			[
					{"fbf": Score(56.24, flag_string="low score; No H adduct", flag_severity=2)},
					{"fbf": Score(82.53, flag_string="No H adduct", flag_severity=2)},
					{"fbf": Score(60.62, flag_string="low score", flag_severity=2)},
					{"fbf": Score(62.90, flag_string="low score", flag_severity=2)},
					]
			)
	def test_compound_scores(self, scores):
		assert Compound(algo="FindByFormula", compound_scores=scores).compound_scores == copy.deepcopy(scores)
		assert Compound(algo="FindByFormula").compound_scores == {}

	def test_results(self, molecule):
		results = [molecule, molecule]
		assert Compound(algo="FindByFormula", results=results).results == copy.deepcopy(results)
		assert Compound(algo="FindByFormula", results=()).results == []
		assert Compound(algo="FindByFormula", results=[]).results == []
		assert Compound(algo="FindByFormula").results == []

	def test_spectra(self, spectrum):
		assert Compound(algo="FindByFormula", spectra=[spectrum]).spectra == [spectrum]
		assert Compound(algo="FindByFormula", spectra=(spectrum, )).spectra == [spectrum]
		assert Compound(algo="FindByFormula", spectra=()).spectra == []
		assert Compound(algo="FindByFormula", spectra=[]).spectra == []
		assert Compound(algo="FindByFormula").spectra == []


def test_dict(spectrum, molecule, compound):

	as_dict = {
			"algo": "FindByFormula",
			"location": {'m': 169.0893, "rt": 13.649, 'a': 29388223, 'y': 3377289},
			"results": [molecule],
			"spectra": [spectrum],
			"compound_scores": {"fbf": Score(62.90, flag_string="low score", flag_severity=2)},
			}

	assert dict(compound) == as_dict


def test_repr(compound, spectrum, molecule, file_regression: FileRegressionFixture):
	assert str(compound) == "Compound([Molecule(Dimethyl Phthalate, C10H10O4)])"
	assert repr(compound) == "<Compound([<Molecule(Dimethyl Phthalate, Formula({'C': 10, 'H': 10, 'O': 4}))>])>"

	compound = Compound(
			algo="FindByFormula",
			location={'m': 169.0893, "rt": 13.649, 'a': 29388223, 'y': 3377289},
			results=[molecule, molecule, molecule, molecule, molecule],
			spectra=[spectrum],
			compound_scores={"fbf": Score(62.90, flag_string="low score", flag_severity=2)},
			)
	file_regression.check(str(compound), encoding="UTF-8", extension="_str.txt")
	file_regression.check(repr(compound), encoding="UTF-8", extension="_repr.txt")


raw_xml = """
<Compound algo="FindByFormula">
	<Location m="169.0893" rt="13.649" a="29388223" y="3377289" />
	<CompoundScores>
		<CpdScore algo="fbf" score="99.79" />
	</CompoundScores>
	<Results>
		<Molecule name="Diphenylamine" formula="C12 H11 N">
			<MatchScores>
				<Match algo="overall" score="99.79" />
				<Match algo="tgt" score="99.79" />
			</MatchScores>
		</Molecule>
	</Results>
	<Spectrum type="FbF" cpdAlgo="FindByFormula">
		<MSDetails scanType="Scan" is="Esi" p="+" />
		<Device type="QuadrupoleTimeOfFlight" num="1" />
		<MSPeaks>
			<p x="170.0965" rx="170.0964" y="890559.25" z="1" s="M+H" />
			<p x="171.0998" rx="171.0996" y="114286.09" z="1" s="M+H+1" />
			<p x="172.1033" rx="172.1028" y="7151.12" z="1" s="M+H+2" />
			<p x="192.0831" rx="192.0784" y="490.62" z="1" s="M+Na" />
		</MSPeaks>
	</Spectrum>
	<Spectrum type="TOF-MS1" satLimit="16742400" scans="12" cpdAlgo="FindByFormula">
		<MSDetails scanType="Scan" is="Esi" p="+" fv="380.0V" />
		<RTRanges>
			<RTRange min="13.561" max="13.808" />
		</RTRanges>
		<Device type="QuadrupoleTimeOfFlight" num="1" />
		<MassCalibration>
			<CalStep form="Traditional">
				<Count>2</Count>
				<C_0>0.00034578342950490094</C_0>
				<C_1>1006.6218360029186</C_1>
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
			<p x="170.0965" rx="170.0964" y="890559.25" z="1" s="M+H" />
			<p x="171.0998" rx="171.0996" y="114286.09" z="1" s="M+H+1" />
			<p x="172.1033" rx="172.1028" y="7151.12" z="1" s="M+H+2" />
			<p x="192.0831" rx="192.0784" y="490.62" z="1" s="M+Na" />
		</MSPeaks>
	</Spectrum>
</Compound>
"""


@pytest.fixture()
def fbf_spectrum():
	return Spectrum(
			spectrum_type="FbF",
			algorithm="FindByFormula",
			scan_type="Scan",
			ionisation="Esi",
			polarity='+',
			device=Device(device_type="QuadrupoleTimeOfFlight", number=1),
			peaks=[
					Peak(170.0965, 170.0964, 890559.25, charge=1, label="M+H"),
					Peak(171.0998, 171.0996, 114286.09, charge=1, label="M+H+1"),
					Peak(172.1033, 172.1028, 7151.12, charge=1, label="M+H+2"),
					Peak(192.0831, 192.0784, 490.62, charge=1, label="M+Na"),
					],
			)


@pytest.fixture()
def tof_spectrum():
	return Spectrum(
			spectrum_type="TOF-MS1",
			algorithm="FindByFormula",
			saturation_limit=16742400,
			scans=12,
			scan_type="Scan",
			ionisation="Esi",
			polarity='+',
			voltage="380V",
			device=Device(device_type="QuadrupoleTimeOfFlight", number=1),
			peaks=[
					Peak(170.0965, 170.0964, 890559.25, charge=1, label="M+H"),
					Peak(171.0998, 171.0996, 114286.09, charge=1, label="M+H+1"),
					Peak(172.1033, 172.1028, 7151.12, charge=1, label="M+H+2"),
					Peak(192.0831, 192.0784, 490.62, charge=1, label="M+Na"),
					],
			rt_ranges=[RTRange(13.561, 13.808)],
			)


@pytest.fixture()
def expected_compound(fbf_spectrum, tof_spectrum):
	score = Score(99.79)

	return Compound(
			algo="FindByFormula",
			location={'m': 169.0893, "rt": 13.649, 'a': 29388223, 'y': 3377289},
			compound_scores={"fbf": score},
			results=[
					Molecule(
							name="Diphenylamine", formula="C12 H11 N", matches={
									"overall": score,
									"tgt": score,
									}
							)
					],
			spectra=[fbf_spectrum, tof_spectrum],
			)


@pytest.mark.usefixtures("fbf_spectrum", "tof_spectrum")
def test_from_xml(expected_compound):
	tree = lxml.objectify.fromstring(raw_xml)
	spec = Compound.from_xml(tree)
	assert spec == expected_compound


@pytest.mark.usefixtures("tof_spectrum", "fbf_spectrum")
def test_compound_list_from_xml(expected_compound):
	expects = CompoundList("LCQTOF", [expected_compound])

	tree = lxml.objectify.fromstring(f'<CompoundList instrumentConfiguration="LCQTOF">{raw_xml}</CompoundList>')
	spec = CompoundList.from_xml(tree)
	assert spec == expects


@pytest.mark.usefixtures("tof_spectrum", "fbf_spectrum")
def test_parse_cef(tmpdir, expected_compound):
	expects = CompoundList("LCQTOF", [expected_compound])

	(PathPlus(tmpdir) / "demo.cef").write_text(
			f"""\
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<CEF version="1.0.0.0">
<CompoundList instrumentConfiguration="LCQTOF">
	{raw_xml}
</CompoundList>
</CEF>
"""
			)

	cef = parse_cef(PathPlus(tmpdir) / "demo.cef")
	assert cef == expects

	assert parse_cef(PathPlus(__file__).parent / "example.cef")


def test_compoundlist_repr(expected_compound):
	compound_list = CompoundList("LCQTOF", [expected_compound])

	assert repr(compound_list) == f"[{expected_compound!r}]"
	assert str(compound_list) == f"CompoundList[{expected_compound!r}]"
