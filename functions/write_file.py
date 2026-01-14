import os

def write_file(working_directory, file_path, content):
    
    working_directory = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_path.startswith(working_directory):
       return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
   
    if os.path.isdir(target_path):
       return f'Error: Cannot write to "{file_path}" as it is a directory'
   
    parent_dir = os.path.dirname(target_path)
    os.makedirs(parent_dir, exist_ok=True)
   
    with open(target_path, "w", encoding="utf-8") as file:
       file.write(content)
       
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'