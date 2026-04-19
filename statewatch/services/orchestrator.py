from sqlalchemy.orm import Session


class TransactionOrchestrator:
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
