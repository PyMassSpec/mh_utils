# 3rd party
import lxml.objectify  # type: ignore
import pytest

# this package
from mh_utils.cef_parser import Flag, Score, parse_compound_scores

raw_xml_1 = '<CompoundScores><CpdScore algo="fbf" score="86.30" /></CompoundScores>'
raw_xml_2 = '<CompoundScores><CpdScore algo="fbf" score="56.24" tgtFlagsString="low score; No H adduct" tgtFlagsSeverity="2" /></CompoundScores>'
raw_xml_3 = '<CompoundScores><CpdScore algo="fbf" score="82.53" tgtFlagsString="No H adduct" tgtFlagsSeverity="2" /></CompoundScores>'
raw_xml_4 = '<CompoundScores><CpdScore algo="fbf" score="60.62" tgtFlagsString="low score" tgtFlagsSeverity="2" /></CompoundScores>'
raw_xml_5 = '<CompoundScores><CpdScore algo="fbf" score="62.90" tgtFlagsString="low score" tgtFlagsSeverity="2" /></CompoundScores>'
raw_xml_multiline = """
<CompoundScores>
	<CpdScore algo="fbf" score="62.90" tgtFlagsString="low score" tgtFlagsSeverity="2" />
	<CpdScore algo="abc" score="12.34" />
</CompoundScores>"""


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
				],
		)
def test_parse_compound_scores(raw_xml, expects):
	tree = lxml.objectify.fromstring(raw_xml)
	assert parse_compound_scores(tree) == expects


class TestScore:

	def test_creation(self):
		assert Score(7) == 7
		assert Score(7, flag_string="Hello") == 7
		assert Score(7, flag_string="Hello", flag_severity=3) == 7

	def test_equals(self):
		assert Score(7) == Score(7)
		assert Score(7) != Score(8)
		assert Score(7, flag_string="Hello") != Score(8)
		assert Score(7, flag_string="Hello", flag_severity=3) != Score(8)
		assert Score(7, flag_string="Hello") == Score(7, flag_string="Hello")
		assert Score(7, flag_string="Hello", flag_severity=3) == Score(7, flag_string="Hello", flag_severity=3)
		assert Score(7.5, flag_string="Hello", flag_severity=3) == Score(7.5, flag_string="Hello", flag_severity=3)
		assert Score(7, flag_string="Hello") != Score(7, flag_string="World")
		assert Score(7, flag_string="Hello", flag_severity=2) != Score(7, flag_string="Hello", flag_severity=3)

		score = Score(56.24, Flag("low score; No H adduct", severity=2))
		assert score == Score(56.24, Flag("low score; No H adduct", severity=2))

	def test_str(self):
		assert str(Score(7)) == "7.0"
		assert str(Score(7, flag_string="Hello", flag_severity=8)) == "7.0"

		assert repr(Score(7)) == "Score(7.0)"
		assert repr(Score(7, flag_string="Hello", flag_severity=8)) == "Score(7.0, Flag('Hello', severity=8))"

	def test_float(self):
		assert float(Score(7)) == 7.0
		assert float(Score(7, flag_string="Hello", flag_severity=8)) == 7.0


class TestFlag:

	def test_creation(self):
		assert Flag("Hello", 3) == "Hello"

	def test_equals(self):
		assert Flag("Hello", 3) == Flag("Hello", 3)
		assert Flag("Hello", 3) != Flag("World", 3)
		assert Flag("Hello", 3) != Flag("Hello", 8)

	def test_str(self):
		assert str(Flag("Hello", 3)) == "Hello"
		assert repr(Flag("Hello", 3)) == "Flag('Hello', severity=3)"

	def test_severity(self):
		assert Flag("Hello", 3).severity == 3
		assert Flag("Hello", 4).severity == 4
		assert Flag("Hello", 5).severity == 5
