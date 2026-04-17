
import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write provided content to the provided file relative to the working_directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Write content to this file (parent dirs will be created if they don't exist)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that will be writtent to the provided file_path",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):

    try:
        wd_path = os.path.abspath(working_directory)
        full_path = os.path.join(wd_path, file_path)
        target_file = os.path.normpath(full_path)
        parent_dir = os.path.dirname(target_file)
        # Checking if target_dir falls within the absolute working_directory path
        #print(f'workdir: {wd_path}')
        #print(f'parent_dir: {parent_dir}')
        #print(f'target_file: {target_file}')
        valid_target_file = os.path.commonpath([wd_path, target_file]) == wd_path
        if valid_target_file is False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(parent_dir, mode=0o775, exist_ok=True)

        with open(target_file, "w") as fs:
            fs.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing to file: {e}"
