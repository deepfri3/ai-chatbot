
import os 
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Provide content of a file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File looking for content",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        wd_path = os.path.abspath(working_directory)
        full_path = os.path.join(wd_path, file_path)
        target_file = os.path.normpath(full_path)
        # Checking if target_dir falls within the absolute working_directory path
        valid_target_file = os.path.commonpath([wd_path, target_file]) == wd_path
        if valid_target_file is False:
            return f'    Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        print(f'file: {target_file}')
        # Read only up to 10000 characters from the file, in case it's very large.
        # The .read() method of file objects makes this easy – 
        # just pass in the maximum number of characters to read as an argument.
        # You'll get a string value representing either the full contents of the 
        # file or the first n characters, whichever is smaller.
        with open(target_file, "r") as fs:
            file_contents = fs.read(MAX_CHARS)
            if fs.read(1):
                file_contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_contents
    except Exception as e:
        return f"Error reading file: {e}"
        
