"""요청/응답 스키마 (Pydantic)."""
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# ---------- Movie ----------
class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="영화 제목", examples=["오디세이"])
    release_date: date = Field(..., description="개봉일 (YYYY-MM-DD)", examples=["2026-08-05"])
    director: str = Field(..., min_length=1, max_length=100, description="감독", examples=["크리스토퍼 놀란"])
    genre: str = Field(..., min_length=1, max_length=100, description="장르", examples=["액션, 모험, 판타지"])
    poster_url: str = Field(..., min_length=1, max_length=500, description="포스터 이미지 URL (나무위키 참고)")


class MovieOut(MovieCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="영화 ID")
    created_at: datetime = Field(..., description="등록 일시")
    average_rating: float | None = Field(None, description="리뷰 감성 점수 평균 (0~5, 리뷰가 없으면 null)")
    review_count: int = Field(0, description="등록된 리뷰 수")


class RatingOut(BaseModel):
    movie_id: int = Field(..., description="영화 ID")
    average_rating: float | None = Field(None, description="감성 점수(0~5) 평균. 리뷰가 없으면 null")
    review_count: int = Field(..., description="평균 계산에 사용된 리뷰 수")
    positive_count: int = Field(..., description="긍정 리뷰 수")
    negative_count: int = Field(..., description="부정 리뷰 수")


# ---------- Review ----------
class ReviewCreate(BaseModel):
    movie_id: int = Field(..., description="리뷰를 남길 영화 ID", examples=[1])
    author: str = Field(..., min_length=1, max_length=50, description="작성자 이름", examples=["홍길동"])
    content: str = Field(..., min_length=1, max_length=2000, description="리뷰 내용", examples=["영상미가 압도적이에요!"])


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="리뷰 ID")
    movie_id: int = Field(..., description="영화 ID")
    author: str = Field(..., description="작성자 이름")
    content: str = Field(..., description="리뷰 내용")
    sentiment_label: Literal["positive", "negative"] = Field(..., description="감성 분석 결과")
    positive_prob: float = Field(..., description="긍정 확률 (0~1)")
    sentiment_score: float = Field(..., description="감성 점수 (0~5) = 긍정 확률 × 5")
    created_at: datetime = Field(..., description="등록 일시")


# ---------- Sentiment ----------
class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, description="분석할 문장", examples=["정말 재밌었어요"])


class SentimentOut(BaseModel):
    label: Literal["positive", "negative"] = Field(..., description="감성 레이블")
    positive_prob: float = Field(..., description="긍정 확률 (0~1)")
    score: float = Field(..., description="감성 점수 (0~5)")
    model: str = Field(..., description="사용 모델명")
    inference_ms: float = Field(..., description="추론 소요 시간(ms)")
