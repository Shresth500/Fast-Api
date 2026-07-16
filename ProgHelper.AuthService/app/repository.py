from sqlmodel import Session, select
from models import User

class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str):
        return self.session.exec(
            select(User).where(User.email == email)
        ).first()

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_all(self):
        return self.session.exec(select(User)).all()
    
    def get_by_id(self, user_id: int):
        return self.session.exec(
            select(User).where(User.id == user_id)
        ).first()