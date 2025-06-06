#########
mh_utils
#########

.. start short_desc

**Utilities for handing ancillary files produced by MassHunter.**

.. end short_desc


.. start shields

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

.. |docs| image:: https://img.shields.io/readthedocs/mh-utils/latest?logo=read-the-docs
	:target: https://mh-utils.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/PyMassSpec/mh_utils/workflows/Docs%20Check/badge.svg
	:target: https://github.com/PyMassSpec/mh_utils/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/PyMassSpec/mh_utils/workflows/Linux/badge.svg
	:target: https://github.com/PyMassSpec/mh_utils/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/PyMassSpec/mh_utils/workflows/Windows/badge.svg
	:target: https://github.com/PyMassSpec/mh_utils/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/PyMassSpec/mh_utils/workflows/macOS/badge.svg
	:target: https://github.com/PyMassSpec/mh_utils/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/PyMassSpec/mh_utils/workflows/Flake8/badge.svg
	:target: https://github.com/PyMassSpec/mh_utils/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/PyMassSpec/mh_utils/workflows/mypy/badge.svg
	:target: https://github.com/PyMassSpec/mh_utils/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/PyMassSpec/mh_utils/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/PyMassSpec/mh_utils/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/PyMassSpec/mh_utils/master?logo=coveralls
	:target: https://coveralls.io/github/PyMassSpec/mh_utils?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/PyMassSpec/mh_utils?logo=codefactor
	:target: https://www.codefactor.io/repository/github/PyMassSpec/mh_utils
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/mh_utils
	:target: https://pypi.org/project/mh_utils/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/mh_utils?logo=python&logoColor=white
	:target: https://pypi.org/project/mh_utils/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/mh_utils
	:target: https://pypi.org/project/mh_utils/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/mh_utils
	:target: https://pypi.org/project/mh_utils/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/mh_utils?logo=anaconda
	:target: https://anaconda.org/domdfcoding/mh_utils
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/mh_utils?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/mh_utils
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/PyMassSpec/mh_utils
	:target: https://github.com/PyMassSpec/mh_utils/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/PyMassSpec/mh_utils
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/PyMassSpec/mh_utils/v0.2.2
	:target: https://github.com/PyMassSpec/mh_utils/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/PyMassSpec/mh_utils
	:target: https://github.com/PyMassSpec/mh_utils/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2025
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/mh_utils
	:target: https://pypi.org/project/mh_utils/
	:alt: PyPI - Downloads

.. end shields

|

Installation
--------------

.. start installation

``mh_utils`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install mh_utils

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels https://conda.anaconda.org/conda-forge
		$ conda config --add channels https://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install mh_utils

.. end installation
