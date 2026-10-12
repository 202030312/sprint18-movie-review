"""영화 관리 API."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Movie, Review
from ..schemas import MovieCreate, MovieOut, RatingOut, ReviewOut

router = APIRouter(prefix="/movies", tags=["Movies (영화 관리)"])


def _rating_stats(db: Session, movie_id: int | None = None):
    """영화별 (평균 감성 점수, 리뷰 수, 긍정 수) 집계."""
    stmt = select(
        Review.movie_id,
        func.avg(Review.sentiment_score),
        func.count(Review.id),
        func.sum(case((Review.sentiment_label == "positive", 1), else_=0)),
    ).group_by(Review.movie_id)
    if movie_id is not None:
        stmt = stmt.where(Review.movie_id == movie_id)
    return {row[0]: row[1:] for row in db.execute(stmt).all()}


def _to_out(movie: Movie, stats: dict) -> MovieOut:
    avg, count, _ = stats.get(movie.id, (None, 0, 0))
    out = MovieOut.model_validate(movie)
    out.average_rating = round(avg, 2) if avg is not None else None
    out.review_count = count
    return out


def _get_movie_or_404(db: Session, movie_id: int) -> Movie:
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"영화(id={movie_id})를 찾을 수 없습니다.")
    return movie


@router.post(
    "",
    response_model=MovieOut,
    status_code=status.HTTP_201_CREATED,
    summary="영화 등록",
    description="제목, 개봉일, 감독, 장르, 포스터 URL을 받아 새 영화를 등록합니다.",
)
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    movie = Movie(**payload.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return _to_out(movie, {})


@router.get(
    "",
    response_model=list[MovieOut],
    summary="전체 영화 조회",
    description="등록된 모든 영화를 등록순으로 반환합니다. 각 영화의 평균 평점(감성 점수 평균)과 리뷰 수가 포함됩니다.",
)
def list_movies(db: Session = Depends(get_db)):
    movies = db.scalars(select(Movie).order_by(Movie.id)).all()
    stats = _rating_stats(db)
    return [_to_out(m, stats) for m in movies]


@router.get(
    "/{movie_id}",
    response_model=MovieOut,
    summary="특정 영화 조회",
    description="영화 ID로 단일 영화 정보를 조회합니다. 존재하지 않으면 404를 반환합니다.",
    responses={404: {"description": "영화를 찾을 수 없음"}},
)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = _get_movie_or_404(db, movie_id)
    return _to_out(movie, _rating_stats(db, movie_id))


@router.delete(
    "/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="특정 영화 삭제",
    description="영화를 삭제합니다. 해당 영화에 달린 리뷰도 함께 삭제됩니다 (ON DELETE CASCADE).",
    responses={404: {"description": "영화를 찾을 수 없음"}},
)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = _get_movie_or_404(db, movie_id)
    db.delete(movie)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{movie_id}/reviews",
    response_model=list[ReviewOut],
    summary="특정 영화 리뷰 조회",
    description="특정 영화에 등록된 리뷰를 최신순으로 반환합니다.",
    responses={404: {"description": "영화를 찾을 수 없음"}},
)
def list_movie_reviews(movie_id: int, db: Session = Depends(get_db)):
    _get_movie_or_404(db, movie_id)
    return db.scalars(
        select(Review).where(Review.movie_id == movie_id).order_by(Review.created_at.desc(), Review.id.desc())
    ).all()


@router.get(
    "/{movie_id}/rating",
    response_model=RatingOut,
    summary="영화 평점 조회",
    description="해당 영화 리뷰들의 감성 분석 점수(0~5) 평균을 평점으로 반환합니다. 긍정/부정 리뷰 수도 함께 제공합니다.",
    responses={404: {"description": "영화를 찾을 수 없음"}},
)
def get_movie_rating(movie_id: int, db: Session = Depends(get_db)):
    _get_movie_or_404(db, movie_id)
    avg, count, positive = _rating_stats(db, movie_id).get(movie_id, (None, 0, 0))
    return RatingOut(
        movie_id=movie_id,
        average_rating=round(avg, 2) if avg is not None else None,
        review_count=count,
        positive_count=positive or 0,
        negative_count=count - (positive or 0),
    )
