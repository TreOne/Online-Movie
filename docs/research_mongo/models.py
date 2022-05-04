from sqlalchemy import CHAR, INTEGER, TEXT, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserBookmarks(Base):
    __tablename__ = 'user_bookmarks'

    _id = Column(INTEGER, primary_key=True)
    user_id = Column(UUID(as_uuid=True))
    bookmarks = Column(CHAR)


class Movies(Base):
    """Модель соответствия данных в Iiko и Hana."""

    __tablename__ = 'movies'
    _id = Column(UUID(as_uuid=True), primary_key=True)
    rating = Column(INTEGER)
    scores_quantity = Column(INTEGER)
    scores_amount = Column(INTEGER)


class Reviews(Base):
    """Модель для хранения информации о магазинах."""

    __tablename__ = 'reviews'
    _id = Column(UUID(as_uuid=True), primary_key=True)
    movie_id = Column(CHAR)
    user_id = Column(CHAR)
    pub_date = Column(DateTime)
    text = Column(TEXT)
    movies_score_id = Column(CHAR)
    rating = Column(INTEGER)
    scores_quantity = Column(INTEGER)
    scores_amount = Column(INTEGER)


class MovieScores(Base):
    """Модель для хранения чеков."""

    __tablename__ = 'movie_scores'
    _id = Column(UUID(as_uuid=True), primary_key=True)
    movie_id = Column(CHAR)
    user_id = Column(CHAR)
    score = Column(INTEGER)


class ReviewScores(Base):
    """Модель для хранения чеков."""

    __tablename__ = 'review_scores'
    _id = Column(UUID(as_uuid=True), primary_key=True)
    review_id = Column(CHAR)
    user_id = Column(CHAR)
    score = Column(INTEGER)
