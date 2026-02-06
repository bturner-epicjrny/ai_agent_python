import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory with optional string arguments and returns captured stdout/stderr",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the Python file",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]
        if args:
            command.extend(args)

        completed = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        stdout = (completed.stdout or "").strip()
        stderr = (completed.stderr or "").strip()

        parts = []

        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")

        if not stdout and not stderr:
            parts.append("No output produced")
        else:
            if stdout:
                parts.append(f"STDOUT:\n{stdout}")
            if stderr:
                parts.append(f"STDERR:\n{stderr}")

        return "\n".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
