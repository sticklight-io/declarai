import importlib.util
import json
import typing
from typing import Any, Dict, Optional

from pydantic import schema_json_of


def resolve_pydantic_schema(schema_def: Dict[str, Any]) -> Dict[str, Any]:
    schema = {}
    for k, v in schema_def.items():
        v_type = v.get("type")
        if v_type == "object":
            schema[k] = resolve_pydantic_schema(v["properties"])
        elif v_type == "array":
            item_type = v["items"].get("type")
            if item_type == "object":
                schema[k] = [resolve_pydantic_schema(v["items"]["properties"])]
            else:
                schema[k] = [item_type]
        else:
            schema[k] = v_type

    return schema


def resolve_type_hints(type_) -> Optional[str]:
    if type_.__module__ == "builtins":
        if type_ in (str, int, float, bool):
            return type_.__name__

    if importlib.util.find_spec("pydantic"):
        import jsonref
        from pydantic.main import ModelMetaclass

        if isinstance(type_, typing._GenericAlias):
            for sub_type in type_.__args__:
                if isinstance(sub_type, ModelMetaclass):
                    resolved_schema = jsonref.loads(schema_json_of(type_))
                    if "items" in resolved_schema:
                        schema_def = resolved_schema["items"]["properties"]
                    else:
                        schema_def = resolved_schema["properties"]
                    resolved_schema = resolve_pydantic_schema(schema_def)
                    string_schema = json.dumps(resolved_schema, indent=4)
                    string_schema = string_schema.replace("{", "{{").replace("}", "}}")
                    return string_schema
        if isinstance(type_, ModelMetaclass):
            resolved_schema = jsonref.loads(type_.schema_json())
            schema_def = resolved_schema["properties"]
            resolved_schema = resolve_pydantic_schema(schema_def)
            string_schema = json.dumps(resolved_schema, indent=4)
            string_schema = string_schema.replace("{", "{{").replace("}", "}}")
            return string_schema

    return str(type_).replace("typing.", "")
