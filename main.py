import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publishers'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=255), nullable=False)

    books = relationship('Book', back_populates='publisher')

class Book(Base):
    __tablename__ = 'books'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=255), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publishers.id'), nullable=False)

    publisher = relationship('Publisher', back_populates='books')
    stocks = relationship('Stock', back_populates='book')

class Stock(Base):
    __tablename__ = 'stocks'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('books.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shops.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship('Book', back_populates='stocks')
    shop = relationship('Shop', back_populates='stocks')
    sales = relationship('Sale', back_populates='stock')

class Shop(Base):
    __tablename__ = 'shops'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=255), nullable=False)

    stocks = relationship('Stock', back_populates='shop')

class Sale(Base):
    __tablename__ = 'sales'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stocks.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship('Stock', back_populates='sales')


def create_tables(engine):
    Base.metadata.create_all(engine)

# Пример использования
if __name__ == '__main__':
    DSN = "postgresql://postgres:root@localhost:5432/netology_bd"
    engine = sq.create_engine(DSN)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Создание объектов
    publisher = Publisher(name="Publisher Name")
    book = Book(title="Book Title", publisher=publisher)
    shop = Shop(name="Bookstore")
    stock = Stock(book=book, shop=shop, count=10)
    sale = Sale(price=20, date_sale='2024-02-02', stock=stock, count=5)

    session.add_all([publisher, book, shop, stock, sale])
    session.commit()

    # Запросы
    q = session.query(Publisher).join(Book).join(Stock).join(Shop).join(Sale).filter(Sale.count > 0)
    for pub in q.all():
        print(pub.name)
        for bk in pub.books:
            print(f"\t{bk.title}")
            for st in bk.stocks:
                print(f"\t\t{st.shop.name}: {st.count} copies sold on {st.sales[0].date_sale} for {st.sales[0].price}$ each")
