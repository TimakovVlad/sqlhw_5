from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Publisher, Book, Sale, Shop, Stock

DSN = "postgresql://postgres:root@localhost:5432/netology_bd"

engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

publisher_name_or_id = input("Введите имя или идентификатор издателя: ")

# Пробуем преобразовать введенное значение в целое число
try:
    publisher_id = int(publisher_name_or_id)
    publisher = session.query(Publisher).filter_by(id=publisher_id).first()
except ValueError:
    # Если не удалось преобразовать введенное значение в целое число, ищем по имени
    publisher = session.query(Publisher).filter_by(name=publisher_name_or_id).first()

if publisher:
    result = session.query(
        Book.title,
        Shop.name,
        Sale.price,
        Sale.date_sale
    ).join(
        Stock, Book.id == Stock.id_book
    ).join(
        Sale, Stock.id == Sale.id_stock
    ).join(
        Shop, Stock.id_shop == Shop.id
    ).filter(
        Book.id_publisher == publisher.id
    ).all()

    for row in result:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
else:
    print("Издатель не найден.")
