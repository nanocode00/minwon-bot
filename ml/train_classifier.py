"""data/faqs.csv로 CPU용 TF-IDF 카테고리 분류기를 학습한다."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "faqs.csv"
MODEL_PATH = Path(__file__).resolve().parent / "category_classifier.joblib"
RANDOM_STATE = 42
EXAMPLE_QUESTIONS = (
    "카드 결제 내역을 확인하고 싶습니다.",
    "휴대폰 요금제를 변경하려면 어떻게 해야 하나요?",
    "사업자 지원 신청 방법이 궁금합니다.",
)


def load_rows() -> tuple[list[str], list[str]]:
    with DATA_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        expected = ["category", "question", "answer", "source"]
        if reader.fieldnames != expected:
            raise ValueError(f"CSV 컬럼은 {expected} 순서여야 합니다.")
        rows = [row for row in reader if row["category"] and row["question"]]

    category_counts = Counter(row["category"] for row in rows)
    usable = [row for row in rows if category_counts[row["category"]] >= 2]
    questions = [row["question"] for row in usable]
    categories = [row["category"] for row in usable]
    if len(set(categories)) < 2:
        raise RuntimeError("학습 가능한 카테고리가 2개 미만입니다.")
    return questions, categories


def make_pipeline() -> Pipeline:
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer="char_wb",
                    ngram_range=(2, 5),
                    min_df=2,
                    max_features=120_000,
                    sublinear_tf=True,
                ),
            ),
            ("classifier", LinearSVC(class_weight="balanced")),
        ]
    )


def main() -> None:
    questions, categories = load_rows()
    class_count = len(set(categories))
    test_count = max(class_count, round(len(questions) * 0.2))
    if len(questions) - test_count < class_count:
        test_count = len(questions) - class_count
    if test_count < class_count:
        raise RuntimeError("계층화 평가에 필요한 데이터가 부족합니다.")

    x_train, x_test, y_train, y_test = train_test_split(
        questions,
        categories,
        test_size=test_count,
        random_state=RANDOM_STATE,
        stratify=categories,
    )
    model = make_pipeline()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    joblib.dump(
        {
            "model": model,
            "data_path": str(DATA_PATH.relative_to(PROJECT_ROOT)),
            "random_state": RANDOM_STATE,
            "accuracy": accuracy,
        },
        MODEL_PATH,
    )

    example_predictions = model.predict(EXAMPLE_QUESTIONS)
    print(f"Accuracy: {accuracy:.4f}")
    for index, (question, category) in enumerate(
        zip(EXAMPLE_QUESTIONS, example_predictions), start=1
    ):
        print(f'예측 예시 {index}: "{question}" -> {category}')


if __name__ == "__main__":
    main()
