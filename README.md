# 🎬 영화 리뷰 & 감성 분석 서비스 (Sprint 18 미션)

| 구분 | 기술 | 배포 |
|---|---|---|
| `frontend/` | Streamlit | Streamlit Community Cloud |
| `backend/` | FastAPI + SQLite + KoELECTRA-Small 감성 분석 (ONNX INT8, onnxruntime) | Render (render.yaml) |

## 로컬 실행
```bash
# 백엔드
cd backend && pip install -r requirements.txt
uvicorn app.main:app --port 8001
python seed_data.py http://localhost:8001   # 초기 데이터 (또는 AUTO_SEED=1)

# 프론트엔드
cd frontend && pip install -r requirements.txt
BACKEND_URL=http://localhost:8001 streamlit run app.py
```

## Streamlit Cloud 설정
- Main file path: `frontend/app.py`
- Secrets: `BACKEND_URL = "https://<render 서비스 주소>"`
