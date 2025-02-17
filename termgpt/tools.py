import inspect
import subprocess
import os
from typing import Callable, get_type_hints, Any

def generate_json_schema(func: Callable) -> dict:
    """Given a function, generate an OpenAI tool compatible JSON schema.
    
    Handles special cases like AgentState and Enums.
    """
    # Extract function signature
    signature = inspect.signature(func)
    parameters = signature.parameters

    # Extract annotations
    type_hints = get_type_hints(func)

    # Initialize the schema structure
    schema = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__.split("\n")[0] if func.__doc__ else "",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }

    # Process each parameter
    for name, param in parameters.items():

        # Determine if this parameter is required (no default value)
        is_required = param.default == inspect.Parameter.empty

        # Get parameter type
        param_type = type_hints.get(name, Any)
        
        # Convert Python types to JSON schema types
        if param_type == str:
            json_type = "string"
        elif param_type == int:
            json_type = "integer"
        elif param_type == float:
            json_type = "number"
        elif param_type == bool:
            json_type = "boolean"
        else:
            json_type = "string"  # Default to string for complex types

        # Extract parameter description from docstring
        param_desc = ""
        if func.__doc__:
            for line in func.__doc__.split("\n"):
                if f"{name}:" in line:
                    param_desc = line.split(":", 1)[1].strip()
                    break

        # Build parameter schema
        param_schema = {
            "type": json_type,
            "description": param_desc
        }

        # Handle Enum types
        if hasattr(param_type, "__members__"):
            param_schema["enum"] = [e.value for e in param_type]

        # Add default value if present
        if param.default != inspect.Parameter.empty and param.default is not None:
            param_schema["default"] = param.default

        schema["function"]["parameters"]["properties"][name] = param_schema

        if is_required:
            schema["function"]["parameters"]["required"].append(name)

    return schema

def run_command(command: str) -> dict:
    completed_process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        shell=True,
        cwd=os.getcwd(),
    )
    exit_code = completed_process.returncode
    output = completed_process.stdout.strip()

    return {
        "exit_code": exit_code,
        "output": output,
    }