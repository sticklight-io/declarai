import importlib.util
import json
from typing import Any, Dict


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


def resolve_type_hints(typped):
    if importlib.util.find_spec("pydantic"):
        import jsonref
        from pydantic.main import ModelMetaclass

        if isinstance(typped, ModelMetaclass):
            resolved_schema = jsonref.loads(typped.schema_json())
            schema_def = resolved_schema["properties"]
            resolved_schema = resolve_pydantic_schema(schema_def)
            string_schema = json.dumps(resolved_schema, indent=4)
            string_schema = string_schema.replace("{", "{{").replace("}", "}}")
            return string_schema

    return str(typped).replace("typing.", "")
