#!/usr/bin/env python3

# This file is managed by 'repo_helper'. Don't edit it directly.

# stdlib
import os
import re
import sys

# 3rd party
from sphinx.locale import _

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))

from __pkginfo__ import __version__

# User-configurable lines
# End of user-configurable lines

github_url = "https://github.com/domdfcoding/mh_utils"

rst_prolog = f""".. |pkgname| replace:: mh_utils
.. |pkgname2| replace:: ``mh_utils``
.. |browse_github| replace:: `Browse the GitHub Repository <{github_url}>`__
"""

author = "Dominic Davis-Foster"
project = "mh_utils"
slug = re.sub(r'\W+', '-', project.lower())
release = version = __version__
copyright = "2020 Dominic Davis-Foster"  # pylint: disable=redefined-builtin
language = 'en'
package_root = "mh_utils"

extensions = [
	'sphinx.ext.intersphinx',
	'sphinx.ext.autodoc',
	'sphinx.ext.mathjax',
	'sphinx.ext.viewcode',
	'sphinxcontrib.httpdomain',
	'sphinxcontrib.extras_require',
	'sphinx.ext.todo',
	'sphinxemoji.sphinxemoji',
	'notfound.extension',
	'sphinx_tabs.tabs',
	'sphinx-prompt',
	'sphinx.ext.autosummary',
	'autodocsumm',
	'sphinx_copybutton',
	'sphinxcontrib.default_values',
	'sphinxcontrib.toctree_plus',
	'seed_intersphinx_mapping',
	'enum_tools.autoenum',
	'attr_utils.autodoc_typehints',
	]

sphinxemoji_style = 'twemoji'
todo_include_todos = bool(os.environ.get("SHOW_TODOS", 0))
gitstamp_fmt = "%d %b %Y"

templates_path = ['_templates']
html_static_path = ['_static']
source_suffix = '.rst'
exclude_patterns = []

master_doc = 'index'
suppress_warnings = ['image.nonlocal_uri']
pygments_style = 'default'

intersphinx_mapping = {
		'python': ('https://docs.python.org/3/', None),
		'sphinx': ('https://www.sphinx-doc.org/en/stable/', None),
		'rtd': ('https://docs.readthedocs.io/en/latest/', None),
		"h5py": ('https://docs.h5py.org/en/latest/', None),
		"sarge": ('https://sarge.readthedocs.io/en/latest/', None),
		}

html_theme = 'domdf_sphinx_theme'
html_theme_options = {
		'logo_only': False,
		}
html_theme_path = ["../.."]
html_show_sourcelink = True  # True will show link to source

html_context = {
		'display_github': True,
		'github_user': 'domdfcoding',
		'github_repo': 'mh_utils',
		'github_version': 'master',
		'conf_py_path': '/doc-source/',
		}

htmlhelp_basename = slug

latex_documents = [('index', f'{slug}.tex', project, author, 'manual')]
man_pages = [('index', slug, project, [author], 1)]
texinfo_documents = [('index', slug, project, author, slug, project, 'Miscellaneous')]


autodoc_default_options = {
		'members': None,  # Include all members (methods).
		'special-members': None,
		"autosummary": None,
		'exclude-members': ','.join([   # Exclude "standard" methods.
				"__dict__",
				"__dir__",
				"__weakref__",
				"__module__",
				"__annotations__",
				"__orig_bases__",
				"__parameters__",
				"__subclasshook__",
				"__init_subclass__",
				"__attrs_attrs__",
				"__init__",
				"__new__",
				"__getnewargs__",
				"__abstractmethods__",
				"__hash__",
				])
		}


# Extensions to theme docs
def setup(app):
	from sphinx.domains.python import PyField
	from sphinx.util.docfields import Field

	app.add_object_type(
			'confval',
			'confval',
			objname='configuration value',
			indextemplate='pair: %s; configuration value',
			doc_field_types=[
					PyField(
							'type',
							label=_('Type'),
							has_arg=False,
							names=('type', ),
							bodyrolename='class',
							),
					Field(
							'default',
							label=_('Default'),
							has_arg=False,
							names=('default', ),
							),
					]
			)
