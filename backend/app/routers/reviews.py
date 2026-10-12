"""리뷰 관리 API."""
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Movie, Review
from ..schemas import ReviewCreate, ReviewOut
from ..sentiment import analyzer

router = APIRouter(prefix="/reviews", tags=["Reviews (리뷰 관리)"])


@router.post(
    "",
    response_model=ReviewOut,
    status_code=status.HTTP_201_CREATED,
    summary="리뷰 등록 (+ 자동 감성 분석)",
    description=(
        "영화 ID, 작성자 이름, 리뷰 내용을 받아 리뷰를 등록합니다. "
        "등록 시 감성 분석 모델이 자동 실행되어 감성 레이블(positive/negative), "
        "긍정 확률, 감성 점수(0~5)가 함께 저장됩니다."
    ),
    responses={404: {"description": "영화를 찾을 수 없음"}},
)
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)):
    if db.get(Movie, payload.movie_id) is None:
        raise HTTPException(status_code=404, detail=f"영화(id={payload.movie_id})를 찾을 수 없습니다.")
    result = analyzer.predict(payload.content)
    review = Review(
        **payload.model_dump(),
        sentiment_label=result["label"],
        positive_prob=result["positive_prob"],
        sentiment_score=result["score"],
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get(
    "",
    response_model=list[ReviewOut],
    summary="전체 리뷰 조회 (최신순)",
    description="전체 리뷰를 최신 등록순으로 반환합니다. `limit`으로 개수를 제한할 수 있습니다 (예: 최근 10개 → limit=10).",
)
def list_reviews(
    limit: int | None = Query(None, ge=1, le=1000, description="반환할 최대 리뷰 수"),
    db: Session = Depends(get_db),
):
    stmt = select(Review).order_by(Review.created_at.desc(), Review.id.desc())
    if limit:
        stmt = stmt.limit(limit)
    return db.scalars(stmt).all()


@router.get(
    "/{review_id}",
    response_model=ReviewOut,
    summary="특정 리뷰 조회",
    description="리뷰 ID로 단일 리뷰를 조회합니다.",
    responses={404: {"description": "리뷰를 찾을 수 없음"}},
)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail=f"리뷰(id={review_id})를 찾을 수 없습니다.")
    return review


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="리뷰 삭제",
    description="리뷰 ID로 리뷰를 삭제합니다.",
    responses={404: {"description": "리뷰를 찾을 수 없음"}},
)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail=f"리뷰(id={review_id})를 찾을 수 없습니다.")
    db.delete(review)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
