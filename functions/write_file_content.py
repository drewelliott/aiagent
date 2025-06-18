import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    combined_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not combined_path.startswith(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(combined_path):
        try:
            os.makedirs(combined_path)
            with open(os.path.join(combined_path, content), 'w') as fh:
                fh.write(content)
        except Exception as e:
            error_string = str(e)
            return f'Error: {error_string}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be written to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written into the file.",
            ),
        },
    ),
)
