import os
import tempfile
from typing import Tuple

def get_file_extension(filename: str) -> str:
    """
    Get the file extension from a filename
    Args:
        filename (str): Name of the file
    Returns:
        str: File extension without the dot
    """
    return os.path.splitext(filename)[1][1:].lower()

def create_temp_file(file_data: bytes, extension: str) -> Tuple[str, str]:
    """
    Create a temporary file with the given data and extension
    Args:
        file_data (bytes): File contents
        extension (str): File extension
    Returns:
        Tuple[str, str]: Tuple containing the temp file path and filename
    """
    with tempfile.NamedTemporaryFile(suffix=f'.{extension}', delete=False) as temp_file:
        temp_file.write(file_data)
        return temp_file.name, os.path.basename(temp_file.name)

def cleanup_temp_file(file_path: str) -> None:
    """
    Delete a temporary file
    Args:
        file_path (str): Path to the file to delete
    """
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        # Log error but don't raise - this is cleanup
        print(f"Error cleaning up temp file {file_path}: {str(e)}")
