from collections.abc import Iterable

import attr
from attr import define

from issx.domain import SupportedBackend


@define(kw_only=True)
class BaseConfig:
    """
    Base class for config classes. It contains a raw_config attribute
    that should store the raw dictionary that was used to create the object.
    """

    raw_config: dict = attr.ib(
        validator=attr.validators.instance_of(dict),
        factory=dict,
    )

    @classmethod
    def get_meaningful_fields(cls) -> Iterable[attr.Attribute]:
        """
        Get all fields except the raw_config field.

        Returns: Iterable of fields
        """
        fields = attr.fields(cls)
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
    backend: SupportedBackend = attr.ib(
        validator=attr.validators.in_(SupportedBackend.__members__.values())
    )
    url: str = attr.ib(validator=attr.validators.instance_of(str))
    token: str = attr.ib(validator=attr.validators.instance_of(str))


@define(kw_only=True)
class ProjectFlatConfig(BaseConfig):
    instance: str = attr.ib(validator=attr.validators.instance_of(str))
    project: str = attr.ib(validator=attr.validators.instance_of(str))
