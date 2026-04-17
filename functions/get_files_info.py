
import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        wd_path = os.path.abspath(working_directory)
        full_path = os.path.join(wd_path, directory)
        target_dir = os.path.normpath(full_path)
        # Checking if target_dir falls within the absolute working_directory path
        valid_target_dir = os.path.commonpath([wd_path, target_dir]) == wd_path
        if valid_target_dir is False:
            return f"    Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        files_info = []
        files_list = os.listdir(target_dir)
        for file in files_list:
            file_path = os.path.join(target_dir, file)
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            files_info.append(f"  - {file}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"

    
    

