# stdlib
import re

# 3rd party
from domdf_python_tools.paths import PathPlus
from mathematical.utils import concatenate_csv
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from mh_utils.csv_parser import ResultParser
from mh_utils.csv_parser.utils import concatenate_json


def test_csv_parser(tmp_pathplus, file_regression: FileRegressionFixture):
	raw_results_dir = PathPlus(__file__).parent / "raw_results"

	json_results_dir = tmp_pathplus / "json_results"
	csv_results_dir = tmp_pathplus / "csv_results"

	parser = ResultParser(raw_results_dir, json_results_dir, csv_results_dir)

	dates = [
			"191121",
			"191126",
			"191128",
			"191206",
			"191211",
			"200124",
			"200128",
			"200129",
			"200206",
			"200218",
			"200221",
			"200227",
			"200303",
			]

	dates = ['-'.join(re.findall("..", date)) for date in dates]
	parser.parse_directory_list(dates)

	csv_files = []
	json_files = []

	for date in dates:
		csv_files.append(csv_results_dir / date / "CSV Results Parsed.csv")
		json_files.append(json_results_dir / date / "results.json")

	concatenate_csv(*csv_files, outfile=tmp_pathplus / "All CSV Results.csv")
	concatenate_json(*json_files, outfile=tmp_pathplus / "All Results.json")

	file_regression.check((tmp_pathplus / "All CSV Results.csv").read_text(), encoding="UTF-8", extension=".csv")
	file_regression.check((tmp_pathplus / "All Results.json").read_text(), encoding="UTF-8", extension=".json")
