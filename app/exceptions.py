class DuplicateUserError(Exception):
    """Raised when attempting to register an email that already exists."""

class InvalidCredentialsError(Exception):
    """Raised when attempting to login with invalid credentials (incorrect email and/or password)"""