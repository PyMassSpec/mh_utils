# 3rd party
from betamax import Betamax
from domdf_python_tools.paths import PathPlus

pytest_plugins = ("domdf_python_tools.testing", )

with Betamax.configure() as config:
	config.cassette_library_dir = PathPlus(__file__).parent / "cassettes"
