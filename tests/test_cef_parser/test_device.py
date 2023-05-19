# 3rd party
import lxml.objectify  # type: ignore
import pytest

# this package
from mh_utils.cef_parser import Device


@pytest.mark.parametrize(
		"device_type, device_type_expects", [
				("hello world", "hello world"),
				("An Instrument", "An Instrument"),
				]
		)
@pytest.mark.parametrize(
		"number, number_expects",
		[
				(1, 1),
				(5, 5),
				(10, 10),
				(50, 50),
				(100, 100),
				(1.0, 1),
				(5.0, 5),
				(10.0, 10),
				(50.0, 50),
				(100.0, 100),
				('1', 1),
				('5', 5),
				("10", 10),
				("50", 50),
				("100", 100),
				],
		)
def test_creation(number, number_expects, device_type, device_type_expects):
	rt = Device(device_type, number)
	assert rt.number == number_expects
	assert rt.device_type == device_type_expects


@pytest.mark.parametrize(
		"raw_xml, device_type_expects, number_expects",
		[
				('<Device type="QuadrupoleTimeOfFlight" num="1" />', "QuadrupoleTimeOfFlight", 1),
				('<Device type="Hello World" num="20" />', "Hello World", 20),
				],
		)
def test_from_xml(raw_xml, device_type_expects, number_expects):
	tree = lxml.objectify.fromstring(raw_xml)
	rt = Device.from_xml(tree)
	assert rt.device_type == device_type_expects
	assert rt.number == number_expects
