import pytest

from pytest_nodeid_to_filepath import main


def pytest_configure(config: pytest.Config) -> None:
    main.ROOT_DIR = config.rootpath
