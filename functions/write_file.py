import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    
    working_directory = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_path.startswith(working_directory + os.sep):
       return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
   
    if os.path.isdir(target_path):
       return f'Error: Cannot write to "{file_path}" as it is a directory'
   
    parent_dir = os.path.dirname(target_path)
    os.makedirs(parent_dir, exist_ok=True)
   
    with open(target_path, "w", encoding="utf-8") as file:
       file.write(content)
       
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'