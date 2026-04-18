import os
from google.genai import types
def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory.'
        
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory.'

        target_dir = os.path.dirname(target_file)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written).'
    except Exception as e:
        return f"Error: {str(e)}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file in the specified directory relative to the working directory. If the file already exists, it will be overwritten.",
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