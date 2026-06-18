class PriceExistsError(Exception):
    """Raised when attempting to create a duplicate price record."""

    def __init__(self, message: str = "Price record already exists for the given date and asset."):
        super().__init__(message)
