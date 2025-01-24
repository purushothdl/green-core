# core/exceptions.py
class UserNotFoundError(Exception):
    """Raised when a user is not found in the database."""
    pass

class InvalidCredentialsError(Exception):
    """Raised when authentication fails."""
    pass