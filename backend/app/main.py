"""FastAPI 애플리케이션 진입점."""
import os
from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select

from .database import Base, SessionLocal, engine
from .models import Movie, Review
from .routers import movies, reviews, sentiment
from .sentiment import analyzer


def _auto_seed() -> None:
    """DB가 비어 있으면 초기 데이터(영화 3편 + 리뷰)를 등록한다.

    Hugging Face Spaces처럼 재시작 시 디스크가 초기화되는 환경을 위한 옵션 (AUTO_SEED=1).
    """
    from seed_data import MOVIES

    with SessionLocal() as db:
        if db.scalar(select(func.count(Movie.id))):
            return
        for m in MOVIES:
            movie = Movie(**{k: v for k, v in m.items() if k != "reviews"})
            movie.release_date = date.fromisoformat(movie.release_date)
            db.add(movie)
            db.flush()
            for author, content in m["reviews"]:
                r = analyzer.predict(content)
                db.add(Review(movie_id=movie.id, author=author, content=content, sentiment_label=r["label"],
                              positive_prob=r["positive_prob"], sentiment_score=r["score"]))
        db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    analyzer.load()  # 서버 시작 시 모델을 한 번만 로드 (요청마다 로드하지 않음)
    if os.getenv("AUTO_SEED") == "1":
        _auto_seed()
    yield


app = FastAPI(
    title="Movie Review API",
    description=(
        "영화 정보, 사용자 리뷰, 리뷰 감성 분석을 제공하는 백엔드 API입니다.\n\n"
        "- **영화 관리**: 등록 / 전체·특정 조회 / 삭제 / 평점 조회\n"
        "- **리뷰 관리**: 등록(자동 감성 분석) / 전체·특정 영화 리뷰 조회 / 삭제\n"
        "- **감성 분석**: `monologg/koelectra-small-finetuned-nsmc` → ONNX 변환 + INT8 동적 양자화 (onnxruntime 서빙)"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(movies.router)
app.include_router(reviews.router)
app.include_router(sentiment.router)


@app.get("/health", tags=["Health"], summary="헬스 체크", description="서버 및 모델 로드 상태를 확인합니다.")
def health():
    return {"status": "ok", "model_loaded": analyzer.session is not None}
