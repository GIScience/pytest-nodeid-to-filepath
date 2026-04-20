import os
import platform

import pytest

from pytest_nodeid_to_filepath import get_filepath


def get_filename_limit():
    system = platform.system()

    if system == "Windows":
        return 255  # NTFS file name limit
    elif system in ("Linux", "Darwin"):  # Darwin = macOS
        try:
            return os.pathconf(".", "PC_NAME_MAX")
        except (AttributeError, OSError, ValueError):
            return 255  # Fallback
    else:
        return 255  # Generic fallback for other OSes


def test_basic():
    path = get_filepath()
    assert path.name == "test_main.py--test_basic"
    assert path.parent.name == "tests"


def test_basic_count():
    path = get_filepath(count=True)
    assert path.name == "test_main.py--test_basic_count"
    assert path.parent.name == "tests"


def test_basic_no_count():
    path = get_filepath(count=False)
    assert path.name == "test_main.py--test_basic_no_count"
    assert path.parent.name == "tests"


def test_with_extension():
    path = get_filepath(extension=".txt")
    assert path.name == "test_main.py--test_with_extension.txt"
    assert path.parent.name == "tests"


def test_with_double_extension():
    path = get_filepath(extension=".approved.txt")
    assert path.name == "test_main.py--test_with_double_extension.approved.txt"
    assert path.parent.name == "tests"


def test_with_extension_and_count():
    path = get_filepath(extension=".txt", count=True)
    assert path.name == "test_main.py--test_with_extension_and_count.txt"
    assert path.parent.name == "tests"


def test_with_extension_and_no_count():
    path = get_filepath(extension=".txt", count=True)
    assert path.name == "test_main.py--test_with_extension_and_no_count.txt"
    assert path.parent.name == "tests"


def test_two_calls_numbered_names():
    path = get_filepath()
    assert path.name == "test_main.py--test_two_calls_numbered_names"
    assert path.parent.name == "tests"
    path = get_filepath()
    assert path.name == "test_main.py--test_two_calls_numbered_names.2"
    assert path.parent.name == "tests"


def test_two_calls_no_numbered_names():
    path = get_filepath()
    assert path.name == "test_main.py--test_two_calls_no_numbered_names"
    assert path.parent.name == "tests"
    path = get_filepath(count=False)
    assert path.name == "test_main.py--test_two_calls_no_numbered_names"
    assert path.parent.name == "tests"


def test_two_calls_different_extensions_no_numbered_names():
    path = get_filepath()
    assert (
        path.name
        == "test_main.py--test_two_calls_different_extensions_no_numbered_names"
    )
    assert path.parent.name == "tests"
    path = get_filepath(extension=".txt")
    assert (
        path.name
        == "test_main.py--test_two_calls_different_extensions_no_numbered_names.txt"
    )
    assert path.parent.name == "tests"


def test_with_directory_under_tests():
    path = get_filepath(directory="tests/approvals")
    assert path.name == "test_main.py--test_with_directory_under_tests"
    assert path.parent.name == "approvals"
    assert path.parent.parent.name == "tests"


def test_with_directory_under_root():
    path = get_filepath(directory="approvals")
    assert path.name == "test_main.py--test_with_directory_under_root"
    assert path.parent.name == "tests"
    assert path.parent.parent.name == "approvals"


def test_with_directory_under_tests_via_global(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("pytest_nodeid_to_filepath.main.DIRECTORY", "tests/approvals")
    path = get_filepath()
    assert path.name == "test_main.py--test_with_directory_under_tests_via_global"
    assert path.parent.name == "approvals"
    assert path.parent.parent.name == "tests"


def test_with_directory_under_root_via_global(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("pytest_nodeid_to_filepath.main.DIRECTORY", "approvals")
    path = get_filepath()
    assert path.name == "test_main.py--test_with_directory_under_root_via_global"
    assert path.parent.name == "tests"
    assert path.parent.parent.name == "approvals"


def test_with_a_long_name_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx():
    # fmt: off
    path = get_filepath()
    assert path.name == "test_main.py--test_with_a_long_name_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # noqa
    assert path.parent.name == "tests"
    # fmt: on


@pytest.mark.parametrize("_", ["a" * (get_filename_limit() + 1)])
def test_with_too_long_parameter_name(_: str):
    path = get_filepath()
    assert path.name == "test_main.py--test_with_too_long_parameter_name[2960995929]"
    assert path.parent.name == "tests"


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


@pytest.mark.parametrize("param", [".", "-", "_"])
def test_params_with_allowed_chars(param: str):
    path = get_filepath()
    assert path.name == f"test_main.py--test_params_with_allowed_chars[{param}]"
    assert path.parent.name == "tests"


@pytest.mark.parametrize("_", [" "])
def test_params_with_space(_: str):
    path = get_filepath()
    assert path.name == "test_main.py--test_params_with_space[_]"
    assert path.parent.name == "tests"


@pytest.mark.parametrize("param", [":"])
def test_params_with_special_chars(param: str):
    # Leading to hashing of param
    path = get_filepath()
    assert path.name == "test_main.py--test_params_with_special_chars[336475711]"
    assert path.parent.name == "tests"
