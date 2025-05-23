from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    bookings = relationship("Booking", back_populates="user")

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    copies_available = Column(Integer)

    bookings = relationship("Booking", back_populates="book")

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    booking_date = Column(Date)

    user = relationship("User", back_populates="bookings")
    book = relationship("Book", back_populates="bookings")


engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)

def add_user(name, email, session):
    """Добавление нового пользователя"""
    try:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        print(f"Пользователь {name} успешно добавлен.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении пользователя: {e}")

def add_book(title, author, copies_available, session):
    """Добавление новой книги"""
    try:
        book = Book(title=title, author=author, copies_available=copies_available)
        session.add(book)
        session.commit()
        print(f"Книга '{title}' успешно добавлена.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении книги: {e}")


def create_booking(user_id, book_id, session):
    """Создание бронирования книги"""
    try:
        book = session.query(Book).get(book_id)
        if not book:
            print("Книга не найдена.")
            return
        if book.copies_available <= 0:
            print("Нет доступных экземпляров этой книги.")
            return

        user = session.query(User).get(user_id)
        if not user:
            print("Пользователь не найден.")
            return

        booking = Booking(
            user_id=user_id,
            book_id=book_id,
            booking_date=date.today()
        )

        book.copies_available -= 1

        session.add(booking)
        session.commit()
        print(f"Бронирование создано. Осталось {book.copies_available} экз. книги '{book.title}'.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при создании бронирования: {e}")


def delete_booking(booking_id, session):
    """Удаление бронирования с гарантированным возвратом книги"""
    try:
        if not booking_id:
            print("Ошибка: Не указан ID бронирования")
            return False

        booking = session.query(Booking). \
            with_for_update(). \
            filter(Booking.id == booking_id). \
            first()

        if not booking:
            print("Бронирование не найдено.")
            return False

        if not booking.book_id:
            print("Ошибка: Бронирование не привязано к книге")
            return False

        book = session.query(Book). \
            with_for_update(). \
            filter(Book.id == booking.book_id). \
            first()

        if not book:
            print(f"Ошибка: Книга с ID {booking.book_id} не найдена")
            return False

        book.copies_available += 1
        session.delete(booking)

        print(f"Успешно: Бронирование {booking_id} отменено, книга '{book.title}' возвращена")
        return True

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        session.rollback()
        return False

if __name__ == "__main__":
    try:
        add_user("Иван Иванов", "ivan@example.com")
        add_user("Петр Петров", "petr@example.com")

        add_book("Война и мир", "Лев Толстой", 3)
        add_book("Преступление и наказание", "Федор Достоевский", 2)

        create_booking(1, 1)
        create_booking(2, 1)
        create_booking(1, 2)

        delete_booking(1)

    except Exception as ex:
        print(f"Произошла ошибка: {ex}")

