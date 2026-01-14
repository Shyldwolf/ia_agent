import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    try:
        # Obtener la ruta absoluta del working_directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construir la ruta absoluta normalizada del archivo objetivo
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Verificar que el archivo objetivo esté dentro del working_directory
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Verificar que sea un archivo
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" is not a file'

        # Leer el contenido del archivo
        with open(target_file, "r", encoding="utf-8") as file:
            content = file.read()

        # After reading the first MAX_CHARS...
        
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    
    except Exception as e:
        return f"Error: {str(e)}"