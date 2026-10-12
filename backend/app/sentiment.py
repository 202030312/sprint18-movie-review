"""리뷰 감성 분석 모듈.

- 모델: monologg/koelectra-small-finetuned-nsmc
  네이버 영화 리뷰(NSMC, 20만 건)로 파인튜닝된 KoELECTRA-Small (약 14M 파라미터).
  영화 리뷰 도메인과 정확히 일치하고, base 모델(110M) 대비 1/8 크기로 CPU 추론에 적합.
- 경량화: PyTorch 동적 양자화(Dynamic Quantization)
  nn.Linear 가중치를 FP32 → INT8로 변환하여 모델 메모리를 줄이고 CPU 추론 속도를 높임.
  재학습/캘리브레이션 데이터가 필요 없어 서빙 단계에서 바로 적용 가능.
"""
import os
import threading
import time

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = os.getenv("SENTIMENT_MODEL", "monologg/koelectra-small-finetuned-nsmc")
MAX_LENGTH = 128


def _model_size_mb(model: torch.nn.Module) -> float:
    total = 0
    for t in list(model.state_dict().values()):
        if isinstance(t, torch.Tensor):
            total += t.numel() * t.element_size()
        elif isinstance(t, tuple):  # 양자화된 Linear의 packed params
            total += sum(x.numel() * x.element_size() for x in t if isinstance(x, torch.Tensor))
    return total / 1024 / 1024


class SentimentAnalyzer:
    def __init__(self, model_name: str = MODEL_NAME, quantize: bool = True):
        self.model_name = model_name
        self.quantize = quantize
        self._lock = threading.Lock()
        self.tokenizer = None
        self.model = None
        self.info: dict = {}

    def load(self) -> None:
        torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        model.eval()
        fp32_mb = _model_size_mb(model)
        if self.quantize:
            model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
        self.model = model
        self.info = {
            "model": self.model_name,
            "quantized": self.quantize,
            "fp32_size_mb": round(fp32_mb, 2),
            "serving_size_mb": round(_model_size_mb(model), 2),
        }

    @torch.inference_mode()
    def predict(self, text: str) -> dict:
        if self.model is None:
            self.load()
        start = time.perf_counter()
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=MAX_LENGTH)
        with self._lock:
            logits = self.model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]
        positive_prob = float(probs[1])  # NSMC 레이블: 0=부정, 1=긍정
        return {
            "label": "positive" if positive_prob >= 0.5 else "negative",
            "positive_prob": round(positive_prob, 4),
            "score": round(positive_prob * 5, 2),
            "model": self.model_name + (" (int8 dynamic quantized)" if self.quantize else ""),
            "inference_ms": round((time.perf_counter() - start) * 1000, 1),
        }


analyzer = SentimentAnalyzer(quantize=os.getenv("SENTIMENT_QUANTIZE", "1") != "0")
