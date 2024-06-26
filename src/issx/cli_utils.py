import inspect
from enum import Enum
from typing import Any, TypeVar

from attr import Attribute
from rich.prompt import Prompt

from issx.domain.config import BaseConfig

TConfig = TypeVar("TConfig", bound=BaseConfig)


class RichConfigReader:
    def read(self, config_class: type[TConfig]) -> TConfig:
        fields = config_class.get_meaningful_fields()
        result: dict[Any, Any] = {}
        for field in fields:
            result[field.name] = self._read_field(field)
        return config_class(**result)

    @staticmethod
    def _read_field(field: Attribute) -> str:
        choices = (
            (
                [str(v) for v in field.type.__members__.values()]
                if issubclass(field.type, Enum)
                else None
            )
            if field.type and inspect.isclass(field.type)
            else None
        )
        ask_kwargs = {}
        if field.default:
            ask_kwargs["default"] = str(field.default)
        return Prompt.ask(
            f"Enter [bold]{field.name}[/bold]",
            default=str(field.default) if field.default else ...,  # type: ignore[arg-type]
            choices=choices,
        )
