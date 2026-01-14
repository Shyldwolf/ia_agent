import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file located within the working directory and returns "
        "its standard output and standard error"
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=None):
    
    try:
        working_directory = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))
    
        if not target_path.startswith(working_directory + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a file'
    
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
    
        command = ["python", target_path]
    
        if args:
            command.extend(args)


        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
            )
        
        output_parts = []
        
        
        if result.returncode != 0:
            output_parts.append(f"Process exited with code: {result.returncode}")

        if not result.stdout.strip() and not result.stderr.strip():
            output_parts.append("No output produced.")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)
    
    except Exception as e:
        return f"Error: {str(e)}"