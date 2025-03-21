import os
import pathlib
import shutil

import pytest


@pytest.fixture(scope="session")
def path_test_data() -> pathlib.Path:
    return pathlib.Path(__file__).parent


@pytest.fixture
def copy_testdata_tmpdir(path_test_data, tmp_path):
    def _copy_tree(path=None):
        path = path_test_data if path is None else path_test_data / path
        shutil.copytree(path, tmp_path, dirs_exist_ok=True)

    cwd = pathlib.Path.cwd()
    os.chdir(tmp_path)
    yield _copy_tree
    os.chdir(cwd)
