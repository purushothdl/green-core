# core/exceptions.py


## User Exceptions
class UserNotFoundError(Exception):
    """Raised when a user is not found in the database."""
    pass

class InvalidCredentialsError(Exception):
    """Raised when authentication fails."""
    pass

## Org Exceptions
class OrgNotFoundError(Exception):
    pass

class DuplicateRatingError(Exception):
    """Raised when a user tries to rate an org more than once."""
    pass