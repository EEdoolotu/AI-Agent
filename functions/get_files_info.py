import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    absolute_full_path = os.path.abspath(full_path)
    absolute_working_path = os.path.abspath(working_directory)
    

    if not absolute_full_path.startswith(absolute_working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(absolute_full_path):
        return  f'Error: "{directory}" is not a directory'
    else:
        try:
            files = os.listdir(absolute_full_path)
            result = ""
            for file in files:
                file_path = os.path.join(absolute_full_path, file)
                size = os.path.getsize(file_path)
                is_directory = os.path.isdir(file_path)
                result += f"- {file}: file_size={size} bytes, is_dir={is_directory} \n"
            return result
        except Exception as e:
            return f"Error: {str(e)}"

        
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)       




