import attr
from attr import define

from issx.domain import SupportedBackend


@define
class InstanceConfig:
    backend: SupportedBackend = attr.ib(validator=attr.validators.in_(SupportedBackend))
    url: str = attr.ib(validator=attr.validators.instance_of(str))
    token: str = attr.ib(validator=attr.validators.instance_of(str))
    raw_config: dict = attr.ib(
        validator=attr.validators.instance_of(dict), factory=dict
    )


@define
class ProjectFlatConfig:
    instance: str = attr.ib(validator=attr.validators.instance_of(str))
    project: str = attr.ib(validator=attr.validators.instance_of(str))
    raw_config: dict = attr.ib(
        validator=attr.validators.instance_of(dict), factory=dict
    )
