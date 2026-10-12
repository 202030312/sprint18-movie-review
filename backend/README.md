---
title: Movie Review API
emoji: 🎬
colorFrom: red
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Movie Review API (Sprint 18 백엔드)

FastAPI 백엔드입니다. 영화와 리뷰를 관리하고, 리뷰 감성 분석을 합니다.

- API 문서: `/docs`
- 감성 분석 모델: `monologg/koelectra-small-finetuned-nsmc`에 INT8 동적 양자화를 적용
- 시작할 때 DB가 비어 있으면 초기 데이터를 자동으로 등록합니다 (`AUTO_SEED=1`): 영화 3편과 리뷰 33개

로컬 실행:
```bash
pip install -r requirements.txt
uvicorn app.main:app --port 8001
```
