class InvalidCredentialsError(Exception):
    """Exception raised when provided credentials are invalid."""

    def __init__(self, message: str = "Could not validate credentials."):
        self.message = message
        super().__init__(self.message)
