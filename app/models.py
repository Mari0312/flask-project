import datetime

from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import Column, String, DateTime

from database.database import session, Base


class User(Base):
    __tablename__ = "users"

    name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    hashed_password = Column(String(300), nullable=False)

    def __init__(self, *args, password, birthday, **kwargs):
        date_birthday = datetime.date.fromisoformat(birthday)
        super().__init__(hashed_password=self.generate_hash(password), birthday=date_birthday, *args, **kwargs)

    @classmethod
    def find_by_name(cls, name):
        return session.query(cls).filter_by(name=name) \
            .order_by(cls.id).all()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "birthday": self.birthday
        }
