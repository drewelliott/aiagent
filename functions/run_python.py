import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    combined_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not combined_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(combined_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        results = subprocess.run(['python3', file_path], cwd=working_directory, timeout=30, capture_output=True)
        if not results.stdout and not results.stderr:
            return "No output produced."
    except Exception as e:
        error_string = str(e)
        return f'Error: {error_string}'

    stdout = f'STDOUT: {results.stdout.decode('utf-8')}\n'
    stderr = f'STDERR: {results.stderr.decode('utf-8')}\n'

    output = stdout + stderr

    if results.returncode != 0:
        output += f'Process exited with code {results.returncode}\n'

    return output

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to be run, relative to the working directory.",
            ),
        },
    ),
)
