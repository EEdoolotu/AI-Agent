import os
from google.genai import types

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    absolute_full_path = os.path.abspath(full_path)
    absolute_working_path = os.path.abspath(working_directory)

    if not absolute_full_path.startswith(absolute_working_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(absolute_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        try:
            MAX_CHARS = 10000
            with open(absolute_full_path, "r", encoding="utf-8") as f:
                text = f.read(MAX_CHARS + 1)
                count = len(text)
                if count <= MAX_CHARS:
                    return text
                else:
                   return text[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'

                

        except Exception as e:
            return f"Error: {str(e)}"
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Read the text content of a file within the working directory. "
        "Paths must be relative to the working directory. Content may be truncated to 10,000 characters."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file. Example: 'src/main.py'.",
            ),
        },
        required=["file_path"],
    ),
)
