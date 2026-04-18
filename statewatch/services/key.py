from sqlalchemy.orm import Session

from statewatch.db.models import Key


class KeyService:
    def __init__(
        self,
        db_session: Session,
    ):
        """
        Initialize the key service for API key management.

        Parameters
        ----------
        db : Session
            Active SQLAlchemy session.
        """
        self.db = db_session

    def does_key_exist(self, api_key: str) -> bool:
        """
        Check if the provided API key exists in the database.

        Parameters
        ----------
        api_key : str
            The API key to check for existence.

        Returns
        -------
        bool
            True if the API key exists, False otherwise.
        """
        return self.db.query(Key).filter(Key.api_key == api_key).first() is not None
