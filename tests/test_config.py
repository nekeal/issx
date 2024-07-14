import attrs
from issx.domain.config import InstanceConfig


class TestInstanceConfig:
    def test_meaningful_fields(self):
        fields = attrs.fields(InstanceConfig)
        assert InstanceConfig.get_meaningful_fields() == [
            fields.backend,
            fields.url,
            fields.token,
        ]

    def test_as_toml(self):
        config = InstanceConfig(
            backend="gitlab",  # type: ignore
            url="http://example.com",
            token="123",
        )
        assert config.as_toml("test") == (
            "[test]\n"
            "backend = 'gitlab'\n"
            "url = 'http://example.com'\n"
            "token = '123'"
        )
