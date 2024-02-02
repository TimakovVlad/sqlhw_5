from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, Sale, Stock, Book, Shop, Publisher

DSN = "postgresql://postgres:root@localhost:5432/netology_bd"

engine = create_engine(DSN)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Очистка таблицы Sale
session.query(Sale).delete()
session.commit()

# Очистка таблицы Stock
session.query(Stock).delete()
session.commit()

# Очистка таблицы Book
session.query(Book).delete()
session.commit()

# Очистка таблицы Shop
session.query(Shop).delete()
session.commit()

# Очистка таблицы Publisher
session.query(Publisher).delete()
session.commit()
