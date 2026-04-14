# pytest-nodeid-to-filepath

[![Build Status](https://jenkins.heigit.org/buildStatus/icon?job=pytest-approval/main)](https://jenkins.heigit.org/job/pytest-nodeid-to-filepath/job/main/)
[![PyPI - Version](https://img.shields.io/pypi/v/pytest-approval)](https://pypi.org/project/pytest-nodeid-to-filepath/)
[![LICENSE](https://img.shields.io/github/license/GIScience/pytest-nodeid-to-filepath)](COPYING)
[![status: active](https://github.com/GIScience/badges/raw/master/status/active.svg)](https://github.com/GIScience/badges#active)

Get a filepath based on the current Pytest node ID.

The node ID of the current test is read from the environment variable
PYTEST_CURRENT_TEST and transformed to a string which can be used safely
as filename on any OS.

Optionally the directory argument can be given to resolve the path against
this directory. The directory needs to be relative to Pytest root.

## Installation

```sh
uv add pytest-nodeid-to-filepath
```

## Usage

```python
from pytest_nodeid_to_filepath import get_filepath

def test_basic():
    path = get_filepath(extension=".txt")
    assert path.name == "test_main.py--test_basic.txt"
    assert path.parent.name == "tests"
```


Filenames are unique if tests are parametrized.
Parameter are be part of the filename as plain text or as hash.

```python
import pytest
from pytest_nodeid_to_filepath import get_filepath

class Mydataclass:
    foo: str = "bar"

@pytest.mark.parametrize("number_as_string", ("one", "two"))
@pytest.mark.parametrize("number_as_int", (1, 2))
@pytest.mark.parametrize("my_object", (Mydataclass(), Mydataclass()))
def test_use_params_instead_of_hash(
    number_as_string: str,
    number_as_int: int,
    my_object: Mydataclass,
):
    path = get_filepath()
    assert path.name in (
        "test_main.py--test_use_params_instead_of_hash[my_object0-1-one]",
        "test_main.py--test_use_params_instead_of_hash[my_object1-2-two]",
        "test_main.py--test_use_params_instead_of_hash[my_object0-2-one]",
        "test_main.py--test_use_params_instead_of_hash[my_object1-1-two]",
        "test_main.py--test_use_params_instead_of_hash[my_object0-2-two]",
        "test_main.py--test_use_params_instead_of_hash[my_object1-1-one]",
        "test_main.py--test_use_params_instead_of_hash[my_object0-1-two]",
        "test_main.py--test_use_params_instead_of_hash[my_object1-2-one]",
    )
    assert path.parent.name == "tests"
```

More usage examples can be fount in [`tests/test_main.py`](tests/test_main.py).
