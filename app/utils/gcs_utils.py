import uuid


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate unique filenames for a file.
    """
    file_extension = original_filename.split(".")[-1]
    return f"{uuid.uuid4()}.{file_extension}"