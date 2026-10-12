"""감성 분석 모델을 ONNX로 변환하고 INT8 동적 양자화를 적용한다 (개발용 1회 실행).

서빙 서버(Render 무료 플랜, RAM 512MB)에서는 torch 없이 onnxruntime + tokenizers만으로 추론한다.
사용법: pip install -r requirements-dev.txt && python export_onnx.py
결과물: model/model.int8.onnx, model/tokenizer.json
"""
import os
import shutil
import tempfile

import torch
from onnxruntime.quantization import QuantType, quantize_dynamic
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "monologg/koelectra-small-finetuned-nsmc"
OUT_DIR = os.path.join(os.path.dirname(__file__), "model")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)  # fast tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).eval()

    # onnx 양자화 도구가 비ASCII(한글) 경로를 처리하지 못해 임시 폴더에서 작업
    tmp = tempfile.mkdtemp()
    fp32_path = os.path.join(tmp, "model.fp32.onnx")
    dummy = tokenizer("영화 정말 재밌어요", return_tensors="pt")
    torch.onnx.export(
        model,
        (dummy["input_ids"], dummy["attention_mask"], dummy["token_type_ids"]),
        fp32_path,
        input_names=["input_ids", "attention_mask", "token_type_ids"],
        output_names=["logits"],
        dynamic_axes={k: {0: "batch", 1: "seq"} for k in ["input_ids", "attention_mask", "token_type_ids"]},
        opset_version=17,
        dynamo=False,
    )
    # MatMul 가중치를 INT8로 양자화 (활성값은 추론 시 동적 양자화)
    int8_path = os.path.join(tmp, "model.int8.onnx")
    quantize_dynamic(fp32_path, int8_path, weight_type=QuantType.QInt8)
    shutil.move(int8_path, os.path.join(OUT_DIR, "model.int8.onnx"))
    shutil.rmtree(tmp, ignore_errors=True)
    tokenizer.backend_tokenizer.save(os.path.join(OUT_DIR, "tokenizer.json"))
    for f in os.listdir(OUT_DIR):
        print(f, round(os.path.getsize(os.path.join(OUT_DIR, f)) / 2**20, 2), "MB")


if __name__ == "__main__":
    main()
