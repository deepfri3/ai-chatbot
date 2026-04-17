import os 
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="If a Python file is provided relative to the working_directory then run it with the provided arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file to run (It must be valid python",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
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
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args != None:
            #print(f'args: {args}')
            command.extend(args)
        #print(f'command: {command}')
        command_result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=30)
        result_string = f'Process exited with code {command_result.returncode}'
        if command_result.stdout == None and command_result.stderr == None:
            result_string += '\nNo output produced'
        else:
            result_string += f'\nSTDOUT: {command_result.stdout}'
            result_string += f'\nSTDERR: {command_result.stderr}'
        return result_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
