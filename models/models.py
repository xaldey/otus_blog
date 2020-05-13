from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models import posts_tags_table
import hashlib
from flask_login import UserMixin
from .create_db import Base


class User(Base, UserMixin):
    username = Column(String(64), unique=True, nullable=False)
    _password = Column("password", String(32), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    posts = relationship('Post', back_populates='user')

    def __repr__(self):
        return f'<User #{self.id} {self.username}>'

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = self.hash_password(value)

    @classmethod
    def hash_password(cls, value: str) -> str:
        return hashlib.md5(value.encode("utf-8")).hexdigest()


class Post(Base):
    # __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    title = Column(String(40), nullable=False)
    text = Column(Text, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)

    user = relationship(User, back_populates='posts')
    tags = relationship('Tag', secondary=posts_tags_table, back_populates='posts')

    def __repr__(self):
        return f'<Post #{self.id} by {self.user_id} {self.title}>'


class Tag(Base):
    # __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)

    posts = relationship('Post', secondary=posts_tags_table, back_populates='tags')

    def __repr__(self):
        return f'<Tag #{self.id} {self.name}>'
