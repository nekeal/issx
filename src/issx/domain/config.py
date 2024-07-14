from collections.abc import Iterable
from typing import cast

import attrs
from attrs import define, field

from issx.domain import SupportedBackend


@define(kw_only=True)
class BaseConfig:
    """
    Base class for config classes. It contains a raw_config attribute
    that should store the raw dictionary that was used to create the object.
    """

    raw_config: dict = field(
        validator=attrs.validators.instance_of(dict),
        factory=dict,
    )

    @classmethod
    def get_meaningful_fields(cls) -> Iterable[attrs.Attribute]:
        """
        Get all fields except the raw_config field.

        Returns: Iterable of fields
        """
        fields = attrs.fields(cls)
        return [field for field in fields if field != fields.raw_config]

    def as_toml(self, key: str) -> str:
        """
        Convert the object to a TOML string.
        Args:
            key: Key to use for the TOML table

        Returns: TOML string
        """
        nl = "\n"
        header = f"[{key}]"
        attributes = [
            f"{field.name} = {repr(getattr(self, field.name))}"
            for field in self.get_meaningful_fields()
        ]
        return f"{header}\n{nl.join(attributes)}"


@define(kw_only=True)
class InstanceConfig(BaseConfig):
    backend: SupportedBackend = field(
        validator=attrs.validators.in_(SupportedBackend.__members__.values())
    )
    url: str = field(validator=attrs.validators.instance_of(str))
    token: str = field(validator=attrs.validators.instance_of(str))


@define(kw_only=True)
class ProjectFlatConfig(BaseConfig):
    instance: str = field(validator=attrs.validators.instance_of(str))
    project: str = field(validator=attrs.validators.instance_of(str))
    issue_title_template: str | None = field(
        default=cast(
            str | None, "{title}"
        ),  # to satisfy mypy https://github.com/python-attrs/attrs/issues/799
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
    )
