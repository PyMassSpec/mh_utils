#!/usr/bin/env python3
#
#  utils.py
"""
CSV utility functions.
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
from typing import Optional

# 3rd party
import pandas  # type: ignore
import sdjson
from domdf_python_tools.typing import PathLike

# this package
from mh_utils.csv_parser import Sample, SampleList

__all__ = ["drop_columns", "reorder_columns", "concatenate_json"]

pandas.DataFrame.__module__ = "pandas"


def drop_columns(df: pandas.DataFrame, *, axis: int = 1, inplace: bool = True, **kwargs) -> pandas.DataFrame:
	"""
	Drop columns from the MassHunter CSV file.

	:param df: The :class:`pandas.DataFrame` to drop columns in.
	:param axis: Which axis to drop columns on.
	:param inplace: Whether to modify the :class:`pandas.DataFrame` in place.
	:param kwargs: Additional keyword arguments passed to :meth:`pandas.DataFrame.drop`.

	.. versionadded:: 0.2.0
	"""

	# Columns where I have no idea what they represent
	unknown_cols = [
			"HMP",
			"KEGG",
			"LMP",
			"METLIN",
			"Notes",
			"Swiss-Prot",
			"CE",
			"Tgt Hit Pos",
			"Score Diff",
			"FV",
			"Saturated",
			"Vol",
			"Cpds/Group",
			"Group",
			"Std Dev",
			"Score (MFE)",
			"Vol %",
			"EIC/TIC% Area",
			"EIC/TIC% Height",
			"TIC% Area",
			"TIC% Height",
			"TWC% Area",
			"TWC% Height",
			"Purity Comments",
			"Purity Result",
			"Purity Value",
			"Score (Frag Coelution)",
			"FIs Conf.",
			"FIs Conf. %",
			"Score (Frag Ratio)",
			"FragMassDiff(ppm)",
			"FIs Eval.",
			"Source",
			"Flags",
			]

	db_cols = [
			"Mass (DB)",
			"Diff (DB, mDa)",
			"Diff (DB, ppm)",
			"RT (Lib/DB)",
			"RT Diff (Lib/DB)",
			"Score (DB)",
			"Shared (DB)",
			"Unique (DB)",
			]

	mfg_cols = [
			"Diff (MFG, mDa)",
			"Mass (MFG)",
			"Diff (MFG, ppm)",
			"Score (MFG)",
			]

	lib_cols = ["Lib/DB", "Score (Lib)"]

	new_df = df.drop([
			*unknown_cols,
			*db_cols,
			*mfg_cols,
			*lib_cols,
			], axis=axis, inplace=inplace, **kwargs)

	if inplace:
		return df
	else:
		return new_df


def reorder_columns(df: pandas.DataFrame) -> pandas.DataFrame:
	"""
	Reorder columns from the MassHunter CSV file.

	:param df: The :class:`pandas.DataFrame` to reorder columns in.

	.. versionadded:: 0.2.0
	"""

	# Make sure to remove columns that got deleted above
	output_col_order = [
			"Sample Name",
			"Cpd",
			"CAS",
			"Name",
			"Hits",
			"Abund",
			"Mining Algorithm",
			"Area",
			"Base Peak",
			"Mass",
			"Avg Mass",
			"Score",
			"m/z",
			"m/z (prod.)",
			"RT",
			"Start",
			"End",
			"Width",
			"Diff (Tgt, mDa)",
			"Diff (Tgt, ppm)",
			"Score (Tgt)",
			"Flags (Tgt)",
			"Flag Severity (Tgt)",
			"Flag Severity Code (Tgt)",
			"Mass (Tgt)",
			"RT (Tgt)",
			"RT Diff (Tgt)",
			"Sample Type",
			"Formula",
			"Height",
			"Ions",
			"Polarity",
			"Z Count",
			"Max Z",
			"Min Z",
			"Label",
			"File",
			"Instrument Name",
			"Position",
			"User Name",
			"Acq Method",
			"DA Method",
			"IRM Calibration status",
			]

	# Omitted columns
	# "ID Source", "ID Techniques Applied"
	# "MS/MS Count",		because blank

	return df[output_col_order]


def concatenate_json(*files: PathLike, outfile: Optional[PathLike] = None) -> SampleList:
	r"""
	Concatenate multiple JSON files together and return a list of :class:`Sample`
	objects in the concatenated json output.

	:param \*files: The files to concatenate.
	:param outfile: The file to save the output as. If :py:obj:`None` no file will be saved.

	.. versionadded:: 0.2.0
	"""  # noqa: D400

	all_samples = SampleList()

	for json_file in files:
		with open(json_file) as fp:
			samples = sdjson.load(fp)

		for sample in samples:
			all_samples.append(Sample(**sample))

	if outfile is not None:
		with open(outfile, 'w') as fp:
			sdjson.dump(all_samples, fp, indent=2)

	return all_samples
