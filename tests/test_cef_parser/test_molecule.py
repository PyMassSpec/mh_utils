# 3rd party
import lxml.objectify
import pytest
from chemistry_tools.formulae import Formula

# this package
from mh_utils.cef_parser import Molecule, Score, parse_match_scores


class TestCreation:

	def test_name(self):
		assert Molecule(name="Dimethyl Phthalate").name == "Dimethyl Phthalate"

	def test_formula(self):
		assert Molecule(
				name="Dimethyl Phthalate", formula="C10 H10 O4"
				).formula == Formula({"C": 10, "H": 10, "O": 4})
		assert Molecule(
				name="Dimethyl Phthalate", formula=Formula({"C": 10, "H": 10, "O": 4})
				).formula == Formula({"C": 10, "H": 10, "O": 4})
		assert Molecule(name="Dimethyl Phthalate").formula == Formula()

	def test_matches(self):
		assert Molecule(
				name="Dimethyl Phthalate",
				matches={
						"overall": Score(62.90),
						"tgt": Score(62.90, flag_string="low score", flag_severity=2),
						}
				).matches == {
						"overall": Score(62.90),
						"tgt": Score(62.90, flag_string="low score", flag_severity=2),
						}

		with pytest.raises(TypeError, match="'matches' must be a dictionary, not"):
			Molecule(name="Dimethyl Phthalate", matches="Hello World")  # type: ignore


def test_dict():
	assert dict(
			Molecule(
					name="Dimethyl Phthalate",
					formula="C10 H10 O4",
					matches={
							"overall": Score(62.90),
							"tgt": Score(62.90, flag_string="low score", flag_severity=2),
							},
					)
			) == {
					"name": "Dimethyl Phthalate",
					"formula": Formula({"C": 10, "H": 10, "O": 4}),
					"matches": {
							"overall": Score(62.90),
							"tgt": Score(62.90, flag_string="low score", flag_severity=2),
							},
					}


def test_repr():
	assert str(
			Molecule(
					name="Dimethyl Phthalate",
					formula="C10 H10 O4",
					matches={
							"overall": Score(62.90),
							"tgt": Score(62.90, flag_string="low score", flag_severity=2),
							},
					)
			) == "<Molecule(Dimethyl Phthalate, Formula({'C': 10, 'H': 10, 'O': 4}))>"
	# TODO: once fixed in chemistry tools)) == "<Molecule(Dimethyl Phthalate, C10H10O4)>"

	assert repr(
			Molecule(
					name="Dimethyl Phthalate",
					formula="C10 H10 O4",
					matches={
							"overall": Score(62.90),
							"tgt": Score(62.90, flag_string="low score", flag_severity=2),
							},
					)
			) == "<Molecule(Dimethyl Phthalate, Formula({'C': 10, 'H': 10, 'O': 4}))>"


raw_xml = """
<Molecule name="Dimethyl Phthalate" formula="C10 H10 O4">
	<MatchScores>
		<Match algo="overall" score="62.90" />
		<Match algo="tgt" score="62.90" tgtFlagsString="low score" tgtFlagsSeverity="2" />
	</MatchScores>
</Molecule>
"""

expects = Molecule(
		name="Dimethyl Phthalate",
		formula="C10 H10 O4",
		matches={
				"overall": Score(62.90),
				"tgt": Score(62.90, flag_string="low score", flag_severity=2),
				},
		)


@pytest.mark.parametrize("raw_xml, expects", [(raw_xml, expects)])
def test_from_xml(raw_xml, expects):
	tree = lxml.objectify.fromstring(raw_xml)
	spec = Molecule.from_xml(tree)
	assert spec == expects


raw_xml_1 = '<MatchScores><Match algo="fbf" score="86.30" /></MatchScores>'
raw_xml_2 = '<MatchScores><Match algo="fbf" score="56.24" tgtFlagsString="low score; No H adduct" tgtFlagsSeverity="2" /></MatchScores>'
raw_xml_3 = '<MatchScores><Match algo="fbf" score="82.53" tgtFlagsString="No H adduct" tgtFlagsSeverity="2" /></MatchScores>'
raw_xml_4 = '<MatchScores><Match algo="fbf" score="60.62" tgtFlagsString="low score" tgtFlagsSeverity="2" /></MatchScores>'
raw_xml_5 = '<MatchScores><Match algo="fbf" score="62.90" tgtFlagsString="low score" tgtFlagsSeverity="2" /></MatchScores>'
raw_xml_multiline = """
<MatchScores>
	<Match algo="fbf" score="62.90" tgtFlagsString="low score" tgtFlagsSeverity="2" />
	<Match algo="abc" score="12.34" />
</MatchScores>"""


@pytest.mark.parametrize(
		"raw_xml, expects",
		[
				(raw_xml_1, {"fbf": 86.3}),
				(raw_xml_2, {"fbf": 56.24}),
				(raw_xml_3, {"fbf": 82.53}),
				(raw_xml_4, {"fbf": 60.62}),
				(raw_xml_5, {"fbf": 62.90}),
				(raw_xml_multiline, {"fbf": 62.90, "abc": 12.34}),
				(raw_xml_1, {"fbf": Score(86.3)}),
				(raw_xml_2, {"fbf": Score(56.24, flag_string="low score; No H adduct", flag_severity=2)}),
				(raw_xml_3, {"fbf": Score(82.53, flag_string="No H adduct", flag_severity=2)}),
				(raw_xml_4, {"fbf": Score(60.62, flag_string="low score", flag_severity=2)}),
				(raw_xml_5, {"fbf": Score(62.90, flag_string="low score", flag_severity=2)}),
				(
						raw_xml_multiline,
						{"fbf": Score(62.90, flag_string="low score", flag_severity=2), "abc": Score(12.34)}
						),
				]
		)
def test_parse_match_scores(raw_xml, expects):
	tree = lxml.objectify.fromstring(raw_xml)
	assert parse_match_scores(tree) == expects
