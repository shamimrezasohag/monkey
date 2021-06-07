import os

from monkey_island.cc.server_utils.consts import (
    DEFAULT_DATA_DIR,
    DEFAULT_LOG_LEVEL,
    DEFAULT_START_MONGO_DB,
)
from monkey_island.cc.setup.island_config_options import IslandConfigOptions

TEST_CONFIG_FILE_CONTENTS_SPECIFIED = {
    "data_dir": "/tmp",
    "log_level": "test",
    "mongodb": {"start_mongodb": False},
}

TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED = {}

TEST_CONFIG_FILE_CONTENTS_NO_STARTMONGO = {"mongodb": {}}


def test_data_dir_specified():
    assert_data_dir_equals(TEST_CONFIG_FILE_CONTENTS_SPECIFIED, "/tmp")


def test_data_dir_uses_default():
    assert_data_dir_equals(TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED, DEFAULT_DATA_DIR)


def test_data_dir_expanduser(monkeypatch, tmpdir):
    set_home_env(monkeypatch, tmpdir)
    DATA_DIR_NAME = "test_data_dir"

    assert_data_dir_equals(
        {"data_dir": os.path.join("~", DATA_DIR_NAME)}, os.path.join(tmpdir, DATA_DIR_NAME)
    )


def test_data_dir_expandvars(monkeypatch, tmpdir):
    set_home_env(monkeypatch, tmpdir)
    DATA_DIR_NAME = "test_data_dir"

    assert_data_dir_equals(
        {"data_dir": os.path.join("$HOME", DATA_DIR_NAME)}, os.path.join(tmpdir, DATA_DIR_NAME)
    )


def set_home_env(monkeypatch, tmpdir):
    monkeypatch.setenv("HOME", str(tmpdir))


def assert_data_dir_equals(config_file_contents, expected_data_dir):
    assert_island_config_option_equals(config_file_contents, "data_dir", expected_data_dir)


def test_log_level():
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_SPECIFIED)
    assert options.log_level == "test"
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED)
    assert options.log_level == DEFAULT_LOG_LEVEL


def test_mongodb():
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_SPECIFIED)
    assert not options.start_mongodb
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED)
    assert options.start_mongodb == DEFAULT_START_MONGO_DB
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_NO_STARTMONGO)
    assert options.start_mongodb == DEFAULT_START_MONGO_DB


def assert_island_config_option_equals(config_file_contents, option_name, expected_value):
    options = IslandConfigOptions(config_file_contents)
    assert getattr(options, option_name) == expected_value
