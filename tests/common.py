# 3rd party
import pytest
from domdf_python_tools.testing import testing_boolean_values

true_false_strings = testing_boolean_values(extra_truthy=[-1]).mark.args[1]

_test_strings = [
		("foo", "foo"),
		(True, "True"),
		(False, "False"),
		(None, "None"),
		(1234, "1234"),
		(12.34, "12.34"),
		]


def any_type_parametrize():
	return pytest.mark.parametrize(
			f"value, expects", [
					("foo", "foo"),
					(1234, 1234),
					(12.34, 12.34),
					(True, True),
					]
			)
