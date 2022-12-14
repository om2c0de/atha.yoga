from typing import Iterable


def setup_resource_attributes(
    instance: object, validated_data: dict, fields: Iterable[str] = ()
) -> None:
    for idx, val in validated_data.items():
        if fields and idx not in fields:
            continue
        setattr(instance, idx, validated_data.get(idx, getattr(instance, idx)))
