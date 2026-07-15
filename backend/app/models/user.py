from sqlachemy import Boolean, Column, integer, String

from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    role = Column(String(40), default="viewer", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)