"""ORM 모델: movies, reviews 테이블."""
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    release_date: Mapped[date] = mapped_column(Date, nullable=False)
    director: Mapped[str] = mapped_column(String(100), nullable=False)
    genre: Mapped[str] = mapped_column(String(100), nullable=False)
    poster_url: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)  # 서버 로컬(KST) 시간

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="movie", cascade="all, delete-orphan", passive_deletes=True
    )


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sentiment_label: Mapped[str] = mapped_column(String(10), nullable=False)  # positive / negative
    positive_prob: Mapped[float] = mapped_column(Float, nullable=False)       # 0.0 ~ 1.0
    sentiment_score: Mapped[float] = mapped_column(Float, nullable=False)     # 0.0 ~ 5.0
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)

    movie: Mapped[Movie] = relationship(back_populates="reviews")
