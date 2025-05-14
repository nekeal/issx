import attr
from issx.domain.config import InstanceConfig


class TestInstanceConfig:
    def test_meaningful_fields(self):
        fields = attr.fields(InstanceConfig)
        assert InstanceConfig.get_meaningful_fields() == [
            fields.backend,
            fields.url,
            fields.token,
            fields.basic_auth_user,
            fields.basic_auth_password,
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
            "token = '123'\n"
            "basic_auth_user = None\n"
            "basic_auth_password = None"
        )

    def test_as_toml_with_basic_auth(self):
        config = InstanceConfig(
            backend="redmine",  # type: ignore
            url="http://example.com",
            token="123",
            basic_auth_user="myuser",
            basic_auth_password="mypassword",
        )
        assert config.as_toml("test") == (
            "[test]\n"
            "backend = 'redmine'\n"
            "url = 'http://example.com'\n"
            "token = '123'\n"
            "basic_auth_user = 'myuser'\n"
            "basic_auth_password = 'mypassword'"
        )
