from transformers import pipeline
import pandas as pd
from glob import glob
import yaml
from loguru import logger
import sys
import time

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)
logger.add("logs.log", rotation="50 MB", compression="zip")


class Model:
    def __init__(self) -> None:
        with open("config.yml") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        self.prepare_context()
        self.load_model()

    def prepare_context(self):
        items = glob(self.config["dataset_path"])
        context = ""
        qa_count = 0
        for item in items:
            data = pd.read_json(item)
            qa_count += data.shape[0]
            for idx, row in data.iterrows():
                context += row["question"] + " " + row["answer"] + "\n"
        logger.info(f"Context created from {len(items)} files and {qa_count} QAs")
        self.context = context

    def load_model(self):
        model_name = self.config["model_name_or_path"]
        self.model = pipeline(
            "question-answering", model=model_name, tokenizer=model_name
        )
        logger.info("Model loaded")

    def ask_question(self, question: str):
        s = time.perf_counter()
        r = self.model(
            question=question, context=self.context, device="cpu", use_fast=False
        )
        answer = " ".join(
            [token.strip() for token in r["answer"].strip().split() if token.strip()]
        )
        score = r["score"]
        elapsed_time = round((time.perf_counter() - s), 1)
        logger.info(
            f"Q: {question}, S: {round(score, 4)}, T: {elapsed_time}s, A: {answer}"
        )
        return answer


if __name__ == "__main__":
    model = Model()
    questions = [
        "چطوری میتونم افتتاح حساب کنم؟",
        "رمز دوم همون رمز حساب است؟",
        "سقف کارت به کارت چقدره؟",
        "طرح مهربانی چیه؟",
        "برای چک بدون امضا گواهی عدم پرداخت میدن؟",
    ]
    for question in questions:
        answer = model.ask_question(question)
