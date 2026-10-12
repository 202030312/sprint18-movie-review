# Hugging Face Spaces (Docker SDK) 배포용 이미지
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TZ=Asia/Seoul \
    HF_HOME=/home/user/.cache/huggingface AUTO_SEED=1 \
    DATABASE_URL=sqlite:////home/user/app/movies.db
RUN apt-get update && apt-get install -y --no-install-recommends tzdata && rm -rf /var/lib/apt/lists/*

# Spaces는 UID 1000 사용자로 컨테이너를 실행
RUN useradd -m -u 1000 user
USER user
WORKDIR /home/user/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user torch --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir --user -r requirements.txt
ENV PATH=/home/user/.local/bin:$PATH

# 모델 가중치를 이미지 빌드 시 미리 받아 콜드 스타트 단축
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification as M; n='monologg/koelectra-small-finetuned-nsmc'; AutoTokenizer.from_pretrained(n); M.from_pretrained(n)"

COPY --chown=user . .
EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
