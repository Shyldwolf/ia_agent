import os


def get_files_info(working_directory, directory="."):
    try:
        # Obtener la ruta absoluta del working_directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construir la ruta absoluta normalizada del directorio objetivo
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        # Verificar que el directorio objetivo esté dentro del working_directory
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Verificar que sea un directorio
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Listar el contenido del directorio
        lines = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)

            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path)

            lines.append(
                f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {str(e)}"
