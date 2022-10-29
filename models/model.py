from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Boolean

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


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    consist = Column(String, nullable=False)
    img = Column(String, nullable=False)
    price = Column(DECIMAL, default=200.00)
    category_id = Column(Integer, ForeignKey('category.id'))
    availability = Column(Boolean, default=True)
    order = relationship('Order', backref='dish', lazy=True)

    def __repr__(self):
        return self.name


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    dish = relationship('Dish', backref='category', lazy=True)

    def __repr__(self):
        return self.name


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, autoincrement=True, primary_key=True)
    item_id = Column(Integer, ForeignKey('dish.id'))
    table_No = Column(Integer, nullable=False)
