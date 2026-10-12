"""감성 분석 단독 API (모델 서빙)."""
from fastapi import APIRouter

from ..schemas import SentimentOut, SentimentRequest
from ..sentiment import analyzer

router = APIRouter(prefix="/sentiment", tags=["Sentiment (감성 분석)"])


@router.post(
    "/analyze",
    response_model=SentimentOut,
    summary="문장 감성 분석",
    description="입력 문장을 저장하지 않고 감성 분석 결과(레이블, 긍정 확률, 0~5 점수, 추론 시간)만 반환합니다.",
)
def analyze(payload: SentimentRequest):
    return analyzer.predict(payload.text)


@router.get(
    "/model-info",
    summary="감성 분석 모델 정보",
    description="서빙 중인 모델명, 런타임(onnxruntime), 양자화 방식, 양자화 전/후 모델 크기(MB)를 반환합니다.",
)
def model_info():
    return analyzer.info
