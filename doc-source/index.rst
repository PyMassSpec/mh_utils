#########
mh_utils
#########

.. start short_desc

.. documentation-summary::
	:meta:

.. end short_desc

.. start shields

.. only:: html

	.. list-table::
		:stub-columns: 1
		:widths: 10 90

		* - Docs
		  - |docs| |docs_check|
		* - Tests
		  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
		* - PyPI
		  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
		* - Anaconda
		  - |conda-version| |conda-platform|
		* - Activity
		  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
		* - QA
		  - |codefactor| |actions_flake8| |actions_mypy|
		* - Other
		  - |license| |language| |requires|

	.. |docs| rtfd-shield::
		:project: mh-utils
		:alt: Documentation Build Status

	.. |docs_check| actions-shield::
		:workflow: Docs Check
		:alt: Docs Check Status

	.. |actions_linux| actions-shield::
		:workflow: Linux
		:alt: Linux Test Status

	.. |actions_windows| actions-shield::
		:workflow: Windows
		:alt: Windows Test Status

	.. |actions_macos| actions-shield::
		:workflow: macOS
		:alt: macOS Test Status

	.. |actions_flake8| actions-shield::
		:workflow: Flake8
		:alt: Flake8 Status

	.. |actions_mypy| actions-shield::
		:workflow: mypy
		:alt: mypy status

	.. |requires| image:: https://dependency-dash.repo-helper.uk/github/PyMassSpec/mh_utils/badge.svg
		:target: https://dependency-dash.repo-helper.uk/github/PyMassSpec/mh_utils/
		:alt: Requirements Status

	.. |coveralls| coveralls-shield::
		:alt: Coverage

	.. |codefactor| codefactor-shield::
		:alt: CodeFactor Grade

	.. |pypi-version| pypi-shield::
		:project: mh_utils
		:version:
		:alt: PyPI - Package Version

	.. |supported-versions| pypi-shield::
		:project: mh_utils
		:py-versions:
		:alt: PyPI - Supported Python Versions

	.. |supported-implementations| pypi-shield::
		:project: mh_utils
		:implementations:
		:alt: PyPI - Supported Implementations

	.. |wheel| pypi-shield::
		:project: mh_utils
		:wheel:
		:alt: PyPI - Wheel

	.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/mh_utils?logo=anaconda
		:target: https://anaconda.org/domdfcoding/mh_utils
		:alt: Conda - Package Version

	.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/mh_utils?label=conda%7Cplatform
		:target: https://anaconda.org/domdfcoding/mh_utils
		:alt: Conda - Platform

	.. |license| github-shield::
		:license:
		:alt: License

	.. |language| github-shield::
		:top-language:
		:alt: GitHub top language

	.. |commits-since| github-shield::
		:commits-since: v0.2.2
		:alt: GitHub commits since tagged version

	.. |commits-latest| github-shield::
		:last-commit:
		:alt: GitHub last commit

	.. |maintained| maintained-shield:: 2024
		:alt: Maintenance

	.. |pypi-downloads| pypi-shield::
		:project: mh_utils
		:downloads: month
		:alt: PyPI - Downloads

.. end shields

.. container:: bullet-less-space

	The current utilities are as follows:

	* :mod:`mh_utils.cef_parser`: Parse Agilent MassHunter Compound Exchange Format files (``*.cef`` files).
	* :mod:`mh_utils.csv_parser`: Parser for CSV result files produced by MassHunter Qualitative.
	* :mod:`mh_utils.worklist_parser`: Parse Agilent MassHunter Worklists (``*.wkl`` files).


Installation
---------------

.. start installation

.. installation:: mh_utils
	:pypi:
	:github:
	:anaconda:
	:conda-channels: conda-forge, domdfcoding

.. end installation


API Reference
----------------

.. html-section::

.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:glob:

	api/*
	api/*/index

.. sidebar-links::
	:caption: Links
	:github:
	:pypi: mh_utils

	Contributing Guide<https://contributing-to-pyms.readthedocs.io/en/latest/>
	Source
	license

.. start links

.. only:: html

	View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

	:github:repo:`Browse the GitHub Repository <PyMassSpec/mh_utils>`

.. end links
