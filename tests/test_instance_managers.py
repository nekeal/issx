import tomllib
from pathlib import Path

import pytest
from issx.instance_managers import GenericConfigParser


class MemoryGenericConfigParser(GenericConfigParser):
    def __init__(self, data: dict):
        self._data = data

    def add_instance(self):
        pass


class TestGenericConfigParser:
    @pytest.fixture
    def empty_config_toml(self):
        return "[instances]\n[projects]\n"

    @pytest.fixture
    def empty_config(self, empty_config_toml):
        return tomllib.loads(empty_config_toml)

    @pytest.fixture
    def tmp_file(self, tmp_path):
        return tmp_path / "file"

    def test_config_parser_parses_provided_file(
        self, empty_config_toml, empty_config, tmp_file
    ):
        tmp_file.write_text(empty_config_toml)

        parser = GenericConfigParser(tmp_file)

        assert parser._data == empty_config

    def test_config_parse_auto_finds_config_file(self, empty_config, empty_config_toml):
        try:
            Path("issx.toml").write_text(empty_config_toml)
            parser = GenericConfigParser()
        finally:
            Path("issx.toml").unlink(missing_ok=True)
        assert parser.config_file == Path("issx.toml")
        assert parser._data == empty_config

    def test_config_parse_raises_error_when_no_config_file_found(self, monkeypatch):
        monkeypatch.setattr(Path, "exists", lambda _: False)
        with pytest.raises(FileNotFoundError):
            GenericConfigParser()

    def test_get_instance_config(self):
        instance_config = {"backend": "redmine"}
        config_parser = MemoryGenericConfigParser(
            {"instances": {"test": instance_config}}
        )

        assert config_parser.get_instance_config("test") == instance_config

    def test_get_project_config(self):
        project_config = {"instance": "test", "token": "token"}
        config_parser = MemoryGenericConfigParser(
            {"projects": {"test": project_config}}
        )

        assert config_parser.get_project_config("test") == project_config
