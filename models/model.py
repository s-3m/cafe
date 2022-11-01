from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Boolean, Sequence

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

    def get_order(self):
        return len(self.orders)

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
    order = relationship('OrderItems', backref='dish', lazy=True)

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
    number = Column(Integer, autoincrement=True)
    table_No = Column(Integer, nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.id'))

    order = relationship('Staff', backref='orders', lazy=True)


class OrderItems(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, autoincrement=True, primary_key=True)
    item_id = Column(Integer, ForeignKey('dish.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))

    order_items = relationship('Order', backref='order_items', lazy=True)
