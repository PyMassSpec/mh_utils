# stdlib
from uuid import UUID

# 3rd party
import pytest

# this package
from mh_utils.worklist_parser.classes import JobData
from tests.test_worklist_parser.test_parser import FakeSampleElement


@pytest.mark.parametrize(
		"id, job_type, run_status",
		[
				("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}", 7, 1),
				("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}", "7", "1"),
				(UUID("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}"), 7, 1),
				(UUID("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}"), "7", "1"),
				],
		)
def test_creation(id, job_type, run_status):  # noqa: A002
	data = JobData(
			id=id,
			job_type=job_type,
			run_status=run_status,
			)

	assert data.id == UUID("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}")
	assert data.job_type == 7
	assert data.run_status == 1
	assert data.sample_info == {}


@pytest.mark.parametrize(
		"id, job_type, run_status, sample_info",
		[
				("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}", 7, 1, {"foo": "a string"}),
				("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}", "7", "1", {"foo": "a string"}),
				(UUID("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}"), 7, 1, {"foo": "a string"}),
				(UUID("{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}"), "7", "1", {"foo": "a string"}),
				],
		)
def test_creation_sample_info(id, job_type, run_status, sample_info):  # noqa: A002
	data = JobData(
			id=id,
			job_type=job_type,
			run_status=run_status,
			sample_info=sample_info,
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


@pytest.fixture()
def sample_jobdata():
	return JobData(
			id="{B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C}",
			job_type=7,
			run_status=1,
			sample_info={"foo": "a string"},
			)


def test_dict(sample_jobdata):
	assert dict(sample_jobdata) == {
			"id": "B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C".lower(),
			"job_type": 7,
			"run_status": 1,
			"sample_info": {"foo": "a string"},
			}


def test_repr(sample_jobdata):
	assert str(sample_jobdata).startswith("JobData(")
	assert str(sample_jobdata).endswith(")")
	assert str(sample_jobdata) == (
			"JobData("
			f"id='{'B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C'.lower()}', "
			"job_type=7, run_status=1)"
			)
	assert repr(sample_jobdata).startswith("JobData(")
	assert repr(sample_jobdata).endswith(")")
	assert repr(sample_jobdata) == (
			"JobData("
			f"id='{'B1F6E4D5-A300-40DF-8FB0-2A26FD8B8C0C'.lower()}', "
			"job_type=7, run_status=1)"
			)
