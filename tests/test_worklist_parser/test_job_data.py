# stdlib
from uuid import UUID

# this package
from mh_utils.worklist_parser.classes import JobData
from tests.test_worklist_parser.test_parser import FakeSampleElement


def test_creation():
	data = JobData(
			id="{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}",
			job_type=7,
			run_status=1,
			)

	assert data.id == UUID("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}")
	assert data.job_type == 7
	assert data.run_status == 1
	assert data.sample_info == {}

	data = JobData(
			id="{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}",
			job_type=7,
			run_status=1,
			sample_info={"foo": "a string"},
			)

	assert data.id == UUID("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}")
	assert data.job_type == 7
	assert data.run_status == 1
	assert data.sample_info == {"foo": "a string"}

	data = JobData(
			id=UUID("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}"),
			job_type="7",  # type: ignore
			run_status="1",  # type: ignore
			sample_info={"foo": "a string"},
			)

	assert data.id == UUID("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}")
	assert data.job_type == 7
	assert data.run_status == 1
	assert data.sample_info == {"foo": "a string"}


class FakeJobDataElement:

	def __init__(self):
		self.ID = "{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}"
		self.JobType = "7"
		self.RunStatus = "1"
		self.SampleInfo = FakeSampleElement()

	def iterchildren(self, *args, **kwargs):
		return ()


def test_from_xml():

	element = FakeJobDataElement()

	data = JobData.from_xml(element)
	assert data.id == UUID("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}")
	assert data.job_type == 7
	assert data.run_status == 1


def test_dict():
	data = JobData(
			id="{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}",
			job_type=7,
			run_status=1,
			sample_info={"foo": "a string"},
			)

	assert dict(data) == {
			"id": "B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C".lower(),
			"job_type": 7,
			"run_status": 1,
			"sample_info": {"foo": "a string"},
			}


def test_repr():
	data = JobData(
			id="{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}",
			job_type=7,
			run_status=1,
			sample_info={"foo": "a string"},
			)

	assert str(data).startswith("JobData(")
	assert str(data).endswith(")")
	assert str(data) == (
			"JobData("
			f"id='{'B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C'.lower()}', "
			"job_type=7, run_status=1)"
			)
	assert repr(data).startswith("JobData(")
	assert repr(data).endswith(")")
	assert repr(data) == (
			"JobData("
			f"id='{'B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C'.lower()}', "
			"job_type=7, run_status=1)"
			)
