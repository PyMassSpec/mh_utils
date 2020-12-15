#!/usr/bin/env python3
#
#  __init__.py
"""
Parser for CSV result files produced by MassHunter Qualitative.

.. versionadded:: 0.2.0
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
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
	:param csv_results_dir: The directory to store the output csvfiles in.

	.. versionadded:: 0.2.0
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

	.. versionadded:: 0.2.0
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

	with open(json_outfile, 'w') as fp:
		sdjson.dump(samples, fp, indent=2)
