import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    absolute_full_path = os.path.abspath(full_path)
    absolute_working_path = os.path.abspath(working_directory)

    try:
        if not absolute_full_path.startswith(absolute_working_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif not os.path.exists(absolute_full_path):
            dir_path = os.path.dirname(absolute_full_path)
            os.makedirs(dir_path, exist_ok=True)
            with open(absolute_full_path, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        elif os.path.isfile(absolute_full_path):
            with open(absolute_full_path, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        else:
            return f"Error: {file_path} is a directory not a file"
    except Exception as e:
            return f"Error: {str(e)}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Write text content to a file in the working directory. Creates parent directories if needed and overwrites existing files. "
        "Paths must be relative to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to write. Example: 'data/output.txt'.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write.",
            ),
        },
        required=["file_path", "content"],
    ),
)