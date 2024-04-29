from unittest import mock

from attr import define
from issx.cli_utils import RichConfigReader
from issx.domain.config import BaseConfig
from rich.prompt import Prompt


@define
class TestConfig(BaseConfig):
    name: str
    age: int


class TestRichConfigReader:
    def test_read_config(self, monkeypatch):
        m_ask = mock.Mock(side_effect=["name", 12])
        monkeypatch.setattr(Prompt, "ask", m_ask)
        config = RichConfigReader().read(TestConfig)
        assert config.name == "name"
        assert config.age == 12
