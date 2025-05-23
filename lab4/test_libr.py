import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqllibr import Base, User, Book, Booking, delete_booking


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_add_user(db_session):
    """Тест добавления пользователя"""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    result = db_session.query(User).filter_by(email="test@example.com").first()
    assert result is not None
    assert result.name == "Test User"
    assert result.email == "test@example.com"


def test_add_book(db_session):
    """Тест добавления книги"""
    book = Book(title="Test Book", author="Test Author", copies_available=5)
    db_session.add(book)
    db_session.commit()

    result = db_session.query(Book).filter_by(title="Test Book").first()
    assert result is not None
    assert result.author == "Test Author"
    assert result.copies_available == 5


def test_create_booking(db_session):
    """Тест создания бронирования"""
    user = User(name="Booking User", email="booking@test.com")
    book = Book(title="Booking Book", author="Booking Author", copies_available=3)
    db_session.add_all([user, book])
    db_session.commit()

    from sqllibr import create_booking
    create_booking(user.id, book.id, db_session)

    # Проверяем результаты
    updated_book = db_session.query(Book).get(book.id)
    assert updated_book.copies_available == 2

    booking = db_session.query(Booking).first()
    assert booking is not None
    assert booking.user_id == user.id
    assert booking.book_id == book.id


def test_delete_booking(db_session, capsys):
    """Комплексный тест удаления бронирования"""
    with db_session.begin():
        user = User(name="Test User", email="test@example.com")
        book = Book(title="Test Book", author="Author", copies_available=1)
        db_session.add_all([user, book])
        db_session.flush()

        booking = Booking(
            user_id=user.id,
            book_id=book.id,
            booking_date=date.today()
        )
        db_session.add(booking)
        db_session.commit()

    with db_session.begin():
        assert db_session.query(Booking).count() == 1
        assert db_session.query(Book).get(book.id).copies_available == 1

    with db_session.begin():
        result = delete_booking(booking.id, db_session)

    with db_session.begin():
        assert result is True
        assert db_session.query(Booking).count() == 0
        updated_book = db_session.query(Book).get(book.id)
        assert updated_book.copies_available == 2

    output = capsys.readouterr().out
    assert "Успешно: Бронирование" in output
    assert "возвращена" in output

    with db_session.begin():
        db_session.query(Booking).delete()
        db_session.query(Book).delete()
        db_session.query(User).delete()

def test_booking_unavailable_book(db_session, capsys):
    """Тест бронирования недоступной книги"""
    user = User(name="No Book User", email="nobook@test.com")
    book = Book(title="Unavailable Book", author="No Author", copies_available=0)
    db_session.add_all([user, book])
    db_session.commit()
    from sqllibr import create_booking
    create_booking(user.id, book.id, db_session)

    captured = capsys.readouterr()
    assert "Нет доступных экземпляров этой книги" in captured.out
    assert db_session.query(Booking).count() == 0