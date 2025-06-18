import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    combined_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not combined_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(combined_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(combined_path, "r") as fh:
            file_content_string = fh.read(MAX_CHARS)
        return file_content_string
    except Exception as e:
        error_string = str(e)
        return f'Error: {error_string}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads content from the specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read content from, relative to the working directory.",
            ),
        },
    ),
)
