import os
from google.genai import types
def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path.endswith(".py") == False:
            return f'Error: "{file_path}" is not a Python file.'
        
        import subprocess
        command = ["python", target_file]
        if args:
            command.extend(args)
        
        result = subprocess.run(command,cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file in the specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)