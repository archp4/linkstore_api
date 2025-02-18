from api.database import Base  # Relative import within the package
import uuid
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship  # Import Base from database.py

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)  # Hash this in a real app!
    imageUrl = Column(String, nullable=True)
    username = Column(String, unique=True, index=True)
    links = relationship("Link", back_populates="user")

    __table_args__ = (UniqueConstraint('email', name='_email_uc'),
                       UniqueConstraint('username', name='_username_uc'))


class Link(Base):
    __tablename__ = "links"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    url = Column(String)
    tags = Column(String)  # Comma-separated or separate table
    category = Column(String)
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="links")