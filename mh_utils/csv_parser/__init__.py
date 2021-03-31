#!/usr/bin/env python3
#
#  __init__.py
"""
Parser for CSV result files produced by MassHunter Qualitative.

.. versionadded:: 0.2.0
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from typing import Iterable

# 3rd party
import pandas  # type: ignore
import sdjson
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

# this package
from mh_utils.csv_parser.classes import Result, Sample, SampleList
from mh_utils.csv_parser.utils import drop_columns, reorder_columns

__all__ = ["ResultParser", "parse_masshunter_csv", "Result", "SampleList", "Sample"]


class ResultParser:
	"""
	Given a directory of CSV results exported from MassHunter, parse them to CSV and JSON.

	:param raw_results_dir: The directory in which the raw exports from MassHunter are stored.
	:param json_results_dir: The directory to store the output json files in.
	:param csv_results_dir: The directory to store the output csv files in.
	"""

	def __init__(self, raw_results_dir: PathLike, json_results_dir: PathLike, csv_results_dir: PathLike):

		self.raw_results_dir = PathPlus(raw_results_dir)

		self.json_results_dir = PathPlus(json_results_dir)
		self.json_results_dir.maybe_make(parents=True)

		self.csv_results_dir = PathPlus(csv_results_dir)
		self.csv_results_dir.maybe_make(parents=True)

	def parse_for_directory(self, directory: PathLike):
		"""
		Convert the "CSV Results.csv" file in the given directory to CSV and JSON.

		:param directory:
		"""

		(self.json_results_dir / directory).maybe_make()
		(self.csv_results_dir / directory).maybe_make()

		infile = self.raw_results_dir / directory / "CSV Results.csv"
		csv_outfile = self.csv_results_dir / directory / "CSV Results Parsed.csv"
		json_outfile = self.json_results_dir / directory / "results.json"
		print(f"{infile} -> {csv_outfile}")
		print(f"{' ' * len(str(infile))} -> {json_outfile}")

		parse_masshunter_csv(infile, csv_outfile, json_outfile)

	def parse_directory_list(self, directory_list: Iterable[PathLike]):
		"""
		Runs :meth:`.~ResultsParser.parse_for_directory` for each directory in ``directory_list``.

		:param directory_list: A list of directories to process.
		"""

		for directory in directory_list:
			print(f"Processing directory {directory}")
			self.parse_for_directory(directory)


def parse_masshunter_csv(csv_file: PathLike, csv_outfile: PathLike, json_outfile: PathLike):
	"""
	Parse CSV results files created by MassHunter.

	:param csv_file:
	:param csv_outfile:
	:param json_outfile:
	"""

	# Read CSV file to data frame
	results_df = pandas.read_csv(csv_file, header=1, index_col=False, dtype=str)

	# drop unneeded columns
	drop_columns(results_df)

	rearranged_results_df = reorder_columns(results_df)
	rearranged_results_df.to_csv(csv_outfile, index=False)

	samples = SampleList()

	for row_idx, result in rearranged_results_df.iterrows():
		sample = samples.add_sample_from_series(result)
		tmp_result = Result.from_series(result)
		sample.add_result(tmp_result)

	PathPlus(json_outfile).dump_json(
			samples,
			json_library=sdjson,  # type: ignore
			indent=2,
			)
	# TODO: https://github.com/python/mypy/issues/5018
	# If it ever gets fixed
