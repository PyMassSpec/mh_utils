# stdlib
from datetime import timedelta

# 3rd party
import lxml.objectify  # type: ignore
import pytest

# this package
from mh_utils.cef_parser import RTRange, make_timedelta


@pytest.mark.parametrize(
		"end_time, end_expects",
		[
				(0, timedelta(minutes=0)),
				(2, timedelta(minutes=2)),
				(20, timedelta(minutes=20)),
				(60, timedelta(hours=1)),
				]
		)
@pytest.mark.parametrize(
		"start_time, start_expects",
		[
				(0, timedelta(minutes=0)),
				(2, timedelta(minutes=2)),
				(20, timedelta(minutes=20)),
				(60, timedelta(hours=1)),
				]
		)
def test_creation(start_time, start_expects, end_time, end_expects):
	rt = RTRange(start_time, end_time)
	assert rt.start == start_expects
	assert rt.end == end_expects


@pytest.mark.parametrize(
		"raw_xml, start_expects, end_expects",
		[
				('<RTRange min="13.561" max="13.808" />', 13.561, 13.808),
				('<RTRange min="0.123" max="12.345" />', 0.123, 12.345),
				]
		)
def test_from_xml(raw_xml, start_expects, end_expects):
	tree = lxml.objectify.fromstring(raw_xml)
	rt = RTRange.from_xml(tree)
	assert rt.start == timedelta(minutes=start_expects)
	assert rt.end == timedelta(minutes=end_expects)


@pytest.mark.parametrize(
		"value, expects",
		[
				(13.561, timedelta(minutes=13.561)),
				(13.808, timedelta(minutes=13.808)),
				(0.123, timedelta(minutes=0.123)),
				(12.345, timedelta(minutes=12.345)),
				(0, timedelta(minutes=0)),
				(2, timedelta(minutes=2)),
				(20, timedelta(minutes=20)),
				(60, timedelta(minutes=60)),
				("13.561", timedelta(minutes=13.561)),
				("13.808", timedelta(minutes=13.808)),
				("0.123", timedelta(minutes=0.123)),
				("12.345", timedelta(minutes=12.345)),
				("0", timedelta(minutes=0)),
				("2", timedelta(minutes=2)),
				("20", timedelta(minutes=20)),
				("60", timedelta(minutes=60)),
				(timedelta(minutes=13.561), timedelta(minutes=13.561)),
				(timedelta(minutes=13.808), timedelta(minutes=13.808)),
				(timedelta(minutes=0.123), timedelta(minutes=0.123)),
				(timedelta(minutes=12.345), timedelta(minutes=12.345)),
				(timedelta(minutes=0), timedelta(minutes=0)),
				(timedelta(minutes=2), timedelta(minutes=2)),
				(timedelta(minutes=20), timedelta(minutes=20)),
				(timedelta(minutes=60), timedelta(minutes=60)),
				]
		)
def test_make_timedelta(value, expects):
	assert make_timedelta(value) == expects
