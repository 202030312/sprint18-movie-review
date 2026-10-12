# Movie Review API (Sprint 18 백엔드)

FastAPI 백엔드입니다. 영화와 리뷰를 관리하고, 리뷰 감성 분석을 합니다.

- API 문서: `/docs`
- 감성 분석: `monologg/koelectra-small-finetuned-nsmc`를 ONNX로 변환하고 INT8 양자화한 모델(`model/`)을 onnxruntime으로 서빙합니다. torch는 필요 없습니다.
- `AUTO_SEED=1`이면 시작할 때 DB가 비어 있을 경우 영화 3편과 리뷰 33개를 자동으로 등록합니다.

```bash
pip install -r requirements.txt
uvicorn app.main:app --port 8001
# 모델 재생성(선택): pip install -r requirements-dev.txt && python export_onnx.py
```
