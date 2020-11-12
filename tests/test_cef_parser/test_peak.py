# stdlib
from datetime import timedelta

# 3rd party
import lxml.objectify  # type: ignore
import pytest

# this package
from mh_utils.cef_parser import Device, Peak, RTRange, make_timedelta


@pytest.mark.parametrize(
		"x, x_expects",
		[
				(170.0965, 170.0965),
				("170.0965", 170.0965),
				(170, 170.0),
				(171.0998, 171.0998),
				("171.0998", 171.0998),
				(171, 171.0),
				],
		)
@pytest.mark.parametrize(
		"rx, rx_expects",
		[
				(172.1028, 172.1028),
				("172.1028", 172.1028),
				(172, 172.0),
				(192.0784, 192.0784),
				("192.0784", 192.0784),
				(192, 192.0),
				],
		)
@pytest.mark.parametrize(
		"y, y_expects",
		[
				(890559.25, 890559.25),
				("890559.25", 890559.25),
				(890559, 890559.0),
				(7151.12, 7151.12),
				("7151.12", 7151.12),
				(7151, 7151.0),
				(490.62, 490.62),
				("490.62", 490.62),
				(490, 490.0),
				],
		)
@pytest.mark.parametrize(
		"charge, charge_expects",
		[
				(1, 1),
				(2, 2),
				(3, 3),
				(5, 5),
				(6, 6),
				(-1, -1),
				(-2, -2),
				(1.0, 1),
				(2.0, 2),
				(4.0, 4),
				(5.0, 5),
				(6.0, 6),
				('1', 1),
				('2', 2),
				('3', 3),
				('4', 4),
				('6', 6),
				],
		)
@pytest.mark.parametrize("label", ["M+H", "M+H+1", "M+H+2", "M+Na"])
def test_creation(
		x,
		x_expects,
		rx,
		rx_expects,
		y,
		y_expects,
		charge,
		charge_expects,
		label,
		):
	rt = Peak(x, rx, y, charge, label)
	assert rt.x == x_expects
	assert rt.rx == rx_expects
	assert rt.y == y_expects
	assert rt.charge == charge_expects
	assert rt.label == label


@pytest.mark.parametrize(
		"raw_xml, x, rx, y, charge, label",
		[
				(
						'<p x="170.0965" rx="170.0964" y="890559.25" z="1" s="M+H" />',
						170.0965,
						170.0964,
						890559.25,
						1,
						"M+H"
						),
				(
						'<p x="171.0998" rx="171.0996" y="114286.09" z="1" s="M+H+1" />',
						171.0998,
						171.0996,
						114286.09,
						1,
						"M+H+1",
						),
				(
						'<p x="172.1033" rx="172.1028" y="7151.12" z="1" s="M+H+2" />',
						172.1033,
						172.1028,
						7151.12,
						1,
						"M+H+2"
						),
				(
						'<p x="192.0831" rx="192.0784" y="490.62" z="1" s="M+Na" />',
						192.0831,
						192.0784,
						490.62,
						1,
						"M+Na"
						),
				],
		)
def test_from_xml(raw_xml, x, rx, y, charge, label):
	tree = lxml.objectify.fromstring(raw_xml)
	rt = Peak.from_xml(tree)
	assert rt.x == x
	assert rt.rx == rx
	assert rt.y == y
	assert rt.charge == charge
	assert rt.label == label
