import dataclasses
import tomllib
from pathlib import Path

import pytest
from issx.instance_managers import (
    SupportedBackend,
)
from issx.instance_managers.config_parser import (
    GenericConfig,
    GenericConfigParser,
    InstanceConfig,
    ProjectFlatConfig,
)


@dataclasses.dataclass
class ConfigDto:
    instance_name: str
    project_name: str
    data_dict: dict


class TestGenericConfigParser:
    @pytest.fixture
    def empty_config_toml(self):
        return "[instances]\n[projects]\n"

    @pytest.fixture
    def empty_config(self, empty_config_toml):
        return tomllib.loads(empty_config_toml)

    @pytest.fixture
    def instance_config_dict(self) -> dict[str, dict]:
        return {
            "instance_name": {
                "backend": "gitlab",
                "url": "https://gitlab.com",
                "token": "token",
            }
        }

    @pytest.fixture
    def project_config_dict(self, instance_config_dict):
        return {
            "project_name": {
                "instance": "instance_name",
                "project": "project_id",
            }
        }

    @pytest.fixture
    def config_dto(self, instance_config_dict, project_config_dict) -> ConfigDto:
        return ConfigDto(
            instance_name="instance_name",
            project_name="project_name",
            data_dict={
                "instances": instance_config_dict,
                "projects": project_config_dict,
            },
        )

    @pytest.fixture
    def tmp_file(self, tmp_path):
        return tmp_path / "file"

    def test_config_parser_parses_provided_file(
        self, empty_config_toml, empty_config, tmp_file
    ):
        tmp_file.write_text(empty_config_toml)

        parser = GenericConfigParser.from_file(tmp_file)

        assert parser._data == GenericConfig(instances={}, projects={})

    def test_config_parse_auto_finds_config_file(self, empty_config, empty_config_toml):
        exists = Path("issx.toml").exists()
        try:
            Path("issx.toml").write_text(empty_config_toml)
            parser = GenericConfigParser.from_file()
        finally:
            if not exists:
                Path("issx.toml").unlink(missing_ok=True)
        assert parser._data == GenericConfig(instances={}, projects={})

    def test_config_parse_raises_error_when_no_config_file_found(self, monkeypatch):
        monkeypatch.setattr(Path, "exists", lambda _: False)
        with pytest.raises(FileNotFoundError):
            GenericConfigParser.from_file()

    def test_from_dict_raises_error_when_instance_does_not_exist(
        self, config_dto: ConfigDto
    ):
        config_dto.data_dict["instances"] = {}
        with pytest.raises(ValueError):
            GenericConfigParser.from_dict(config_dto.data_dict)

    def test_from_dict_raises_error_when_there_is_missing_required_field(
        self, config_dto: ConfigDto
    ):
        config_dto.data_dict["instances"]["instance_name"].pop("url")
        with pytest.raises(TypeError):
            GenericConfigParser.from_dict(config_dto.data_dict)

    def test_get_instance_config(self, config_dto):
        parser = GenericConfigParser.from_dict(config_dto.data_dict)

        assert parser.get_instance_config(config_dto.instance_name) == InstanceConfig(
            backend=SupportedBackend.gitlab, url="https://gitlab.com", token="token"
        )

    def test_get_project_config(self, config_dto):
        parser = GenericConfigParser.from_dict(config_dto.data_dict)

        assert parser.get_project_config(config_dto.project_name) == ProjectFlatConfig(
            instance="instance_name", project="project_id"
        )
