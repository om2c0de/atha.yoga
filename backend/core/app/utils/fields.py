import datetime
import json
import logging
from dataclasses import asdict, is_dataclass
from json import JSONEncoder, JSONDecoder
from typing import Type, Any, Optional, Protocol, Dict, Union, List

from dacite import from_dict, Config
from django.db import models
from django.db.backends.postgresql.base import DatabaseWrapper
from django.db.models.expressions import Col


class IsDataclass(Protocol):
    # as already noted in comments, checking for this attribute is currently
    # the most reliable way to ascertain that something is a dataclass
    __dataclass_fields__: Dict


class JSONParsedField(models.JSONField):
    def __init__(
        self,
        parse_to: Optional[Type[IsDataclass]] = None,
        verbose_name: Optional[str] = None,
        name: Optional[str] = None,
        encoder: Optional[JSONEncoder] = None,
        decoder: Optional[JSONDecoder] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(verbose_name, name, encoder, decoder, **kwargs)
        self.parse_to = parse_to

    def convert(self, data: dict) -> IsDataclass:
        return from_dict(
            data_class=self.parse_to,
            data=data,
            config=Config(
                type_hooks={
                    datetime.time: lambda x: datetime.datetime.strptime(
                        x, "%H:%M:%S"
                    ).time()
                }
            ),
        )

    def from_db_value(
        self, value: str, expression: Col, connection: DatabaseWrapper
    ) -> Optional[Union[IsDataclass, List[IsDataclass]]]:
        if not self.parse_to:
            logging.getLogger(__name__).warning(
                "Undefined dataclass for parsing json field, return None"
            )
            return None
        data = super().from_db_value(value, expression, connection)
        if not data:
            return data
        if isinstance(data, list):
            return [self.convert(data=i) for i in data]
        return self.convert(data=data)

    def get_prep_value(self, value: Any) -> Optional[str]:
        if value is None:
            return value
        result_value = value
        if isinstance(value, list):
            result_value = [asdict(i) if is_dataclass(i) else i for i in value]
        elif not isinstance(value, dict):
            result_value = asdict(value)
        return json.dumps(result_value, cls=self.encoder, default=str)
