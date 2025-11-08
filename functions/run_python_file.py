import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    absolute_full_path = os.path.abspath(full_path)
    absolute_working_path = os.path.abspath(working_directory)

    try:
        if not absolute_full_path.startswith(absolute_working_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.exists(absolute_full_path):
            return f'Error: File "{file_path}" not found.'
        elif not absolute_full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        else:
            try:
                result = subprocess.run(["uv", "run", file_path, *args], 
                cwd=absolute_working_path, 
                capture_output=True, 
                timeout=30, 
                text=True)
            
            except subprocess.TimeoutExpired:
                return "Error: Execution timed out after 30 seconds."

            except Exception as e:
                return f"Error: executing Python file: {e}"   

            stdout_txt = (result.stdout or "").rstrip("\n")
            stderr_txt = (result.stderr or "").rstrip("\n")

            parts = []

            if stdout_txt:
                parts.append(f"STDOUT: {stdout_txt}")
            if stderr_txt:
                parts.append(f"STDERR: {stderr_txt}")
            if result.returncode != 0:
                parts.append(f"Process exited with code {result.returncode}.")

            if not parts:
                return "No output produced."

            return "\n".join(parts)

            





    except Exception as e:
            return f"Error: {str(e)}" 
