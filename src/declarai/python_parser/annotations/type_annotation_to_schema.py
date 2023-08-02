import json
import typing
from typing import Any, Dict, Optional

import jsonref
from pydantic import schema_json_of
from pydantic.main import ModelMetaclass


def resolve_pydantic_schema_recursive(schema_def: Dict[str, Any]) -> Any:
    obj_type = schema_def.get("type")
    if obj_type not in ("array", "object"):
        return obj_type

    schema = {}
    if obj_type == "object":
        if "properties" in schema_def:
            for k, v in schema_def["properties"].items():
                schema[k] = resolve_pydantic_schema_recursive(v)
        elif "additionalProperties" in schema_def:
            return resolve_pydantic_schema_recursive(schema_def["additionalProperties"])
    elif obj_type == "array":
        return [resolve_pydantic_schema_recursive(schema_def["items"])]

    return schema


def resolve_to_json_schema(type_: Any) -> Dict:
    if isinstance(type_, ModelMetaclass):
        unresolved = type_.schema_json()
    else:
        unresolved = schema_json_of(type_)
    return jsonref.loads(unresolved)


def schema_to_string_for_prompt(schema: str) -> str:
    schema = schema.replace("{", "{{").replace("}", "}}")
    return schema


def type_annotation_to_str_schema(type_) -> Optional[str]:
    """
    This method accepts arbitrary types defined in the return annotation of a functions.
    Then creates a string representation of the annotation schema to be passed to the model.
    """
    if type_.__module__ == "builtins":
        if type_ in (str, int, float, bool):
            return type_.__name__

    if isinstance(type_, typing._GenericAlias):
        root_name = type_._name
        if not root_name:
            if type_.__origin__ == typing.Union:
                root_name = "Union"
        properties = []
        for sub_type in type_.__args__:
            resolved_schema = resolve_to_json_schema(sub_type)
            properties.append(resolve_pydantic_schema_recursive(resolved_schema))

        if len(properties) > 1:
            resolved_str_schema = f"{root_name}[{properties[0]}, {properties[1]}]"
        else:
            resolved_str_schema = f"{root_name}[{properties[0]}]"
        return schema_to_string_for_prompt(resolved_str_schema)

    resolved_schema = resolve_to_json_schema(type_)
    resolved_schema = resolve_pydantic_schema_recursive(resolved_schema)
    str_schema = json.dumps(resolved_schema, indent=4)
    return schema_to_string_for_prompt(str_schema)
