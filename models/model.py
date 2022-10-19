from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    user = relationship('Staff', backref='post', lazy=True)

    def __repr__(self):
        return self.name


class Staff(Base):
    __tablename__ = 'staff'

    id = Column(Integer, autoincrement=True, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'))

    def get_login(self):
        return self.login

    def __repr__(self):
        return f'{self.name} - {self.post}'

