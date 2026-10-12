"""리뷰 감성 분석 모듈.

- 모델: monologg/koelectra-small-finetuned-nsmc
  네이버 영화 리뷰(NSMC, 20만 건)로 파인튜닝된 KoELECTRA-Small (약 14M 파라미터).
  영화 리뷰 도메인과 정확히 일치하고, base 모델(110M) 대비 1/8 크기로 CPU 추론에 적합.
- 경량화: ONNX 변환 + INT8 동적 양자화 (export_onnx.py로 사전 생성)
  MatMul 가중치를 FP32 → INT8로 변환해 모델 파일을 52.6MB → 13.6MB로 줄이고,
  서빙 시 torch/transformers 없이 onnxruntime + tokenizers만 사용해 메모리 사용량을 크게 줄임.
  (Render 무료 플랜 RAM 512MB 안에서 동작)
"""
import os
import threading
import time

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

MODEL_NAME = "monologg/koelectra-small-finetuned-nsmc"
MODEL_DIR = os.getenv("SENTIMENT_MODEL_DIR", os.path.join(os.path.dirname(__file__), "..", "model"))
MAX_LENGTH = 128


class SentimentAnalyzer:
    def __init__(self, model_dir: str = MODEL_DIR):
        self.model_dir = model_dir
        self._lock = threading.Lock()
        self.session: ort.InferenceSession | None = None
        self.tokenizer: Tokenizer | None = None
        self.info: dict = {}

    def load(self) -> None:
        model_path = os.path.join(self.model_dir, "model.int8.onnx")
        opts = ort.SessionOptions()
        opts.intra_op_num_threads = max(1, min(4, os.cpu_count() or 1))
        self.session = ort.InferenceSession(model_path, opts, providers=["CPUExecutionProvider"])
        self.tokenizer = Tokenizer.from_file(os.path.join(self.model_dir, "tokenizer.json"))
        self.tokenizer.enable_truncation(MAX_LENGTH)
        self.info = {
            "model": MODEL_NAME,
            "runtime": f"onnxruntime {ort.__version__}",
            "quantization": "INT8 dynamic (MatMul weights)",
            "original_fp32_size_mb": 52.57,
            "serving_size_mb": round(os.path.getsize(model_path) / 2**20, 2),
        }

    def predict(self, text: str) -> dict:
        if self.session is None:
            self.load()
        start = time.perf_counter()
        enc = self.tokenizer.encode(text)
        feeds = {
            "input_ids": np.array([enc.ids], dtype=np.int64),
            "attention_mask": np.array([enc.attention_mask], dtype=np.int64),
            "token_type_ids": np.array([enc.type_ids], dtype=np.int64),
        }
        with self._lock:
            logits = self.session.run(["logits"], feeds)[0][0]
        exp = np.exp(logits - logits.max())
        positive_prob = float(exp[1] / exp.sum())  # NSMC 레이블: 0=부정, 1=긍정
        return {
            "label": "positive" if positive_prob >= 0.5 else "negative",
            "positive_prob": round(positive_prob, 4),
            "score": round(positive_prob * 5, 2),
            "model": f"{MODEL_NAME} (ONNX INT8)",
            "inference_ms": round((time.perf_counter() - start) * 1000, 1),
        }


analyzer = SentimentAnalyzer()
