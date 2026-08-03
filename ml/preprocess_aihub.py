"""AI Hub 71844 질의응답 ZIP을 앱용 FAQ CSV로 전처리한다."""

from __future__ import annotations

import csv
import json
import re
import zipfile
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_PATH = DATA_DIR / "faqs.csv"
SOURCE_LABEL = "AI Hub 71844"

WHITESPACE_RE = re.compile(r"\s+")
TRANSCRIPT_PATTERNS = (
    re.compile(r"(?:위|해당|앞선|주어진|다음).{0,20}(?:대화|상담|통화|녹취|내용)"),
    re.compile(
        r"(?:대화|상담|통화|녹취).{0,20}"
        r"(?:내용|상황|과정|기록|기반|중|에서|따르면|통해)"
    ),
    re.compile(
        r"(?:고객|상담원|화자).{0,15}(?:말|언급|문의|요청|답변|설명).{0,12}"
        r"(?:무엇|어떤|어떻게|인가|했는가)"
    ),
)
INFORMAL_QUESTION_RE = re.compile(
    r"(?:했어|됐어|였어|이었어|있어|없어|맞아|아니야|뭐야|거야|"
    r"할까|했니|하니|했냐|하냐|해|돼|야)\s*[?？]+$"
)
SENSITIVE_PATTERNS = (
    re.compile(r"(?<!\d)\d{6}-[1-4]\d{6}(?!\d)"),
    re.compile(r"(?<!\d)01[016789]-?\d{3,4}-?\d{4}(?!\d)"),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"(?<!\d)(?:\d{4}[- ]?){3}\d{4}(?!\d)"),
)


def normalize_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return WHITESPACE_RE.sub(" ", value).strip()


def should_exclude(question: str, answer: str) -> bool:
    if not question or not answer:
        return True
    if any(pattern.search(question) for pattern in TRANSCRIPT_PATTERNS):
        return True
    if INFORMAL_QUESTION_RE.search(question):
        return True
    combined = f"{question}\n{answer}"
    return any(pattern.search(combined) for pattern in SENSITIVE_PATTERNS)


def iter_instruction_rows(document: dict[str, Any]) -> Iterable[dict[str, str]]:
    category = normalize_text(document.get("consulting_category"))
    if not category:
        return

    instructions = document.get("instructions")
    if not isinstance(instructions, list):
        return

    for instruction_group in instructions:
        if not isinstance(instruction_group, dict):
            continue
        items = instruction_group.get("data")
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            question = normalize_text(item.get("instruction"))
            answer = normalize_text(item.get("output"))
            if should_exclude(question, answer):
                continue
            yield {
                "category": category,
                "question": question,
                "answer": answer,
                "source": SOURCE_LABEL,
            }


def iter_documents() -> Iterable[dict[str, Any]]:
    zip_paths = sorted(DATA_DIR.rglob("*질의응답.zip"))
    if not zip_paths:
        raise FileNotFoundError("data/ 아래에서 AI Hub 질의응답 ZIP을 찾지 못했습니다.")

    for zip_path in zip_paths:
        with zipfile.ZipFile(zip_path) as archive:
            for name in sorted(archive.namelist()):
                if not name.lower().endswith(".json"):
                    continue
                with archive.open(name) as stream:
                    payload = json.loads(stream.read().decode("utf-8-sig"))
                if isinstance(payload, dict):
                    yield payload
                elif isinstance(payload, list):
                    for document in payload:
                        if isinstance(document, dict):
                            yield document


def main() -> None:
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for document in iter_documents():
        for row in iter_instruction_rows(document):
            identity = (row["category"], row["question"])
            if identity in seen:
                continue
            seen.add(identity)
            rows.append(row)

    if not rows:
        raise RuntimeError("전처리 후 저장할 FAQ가 없습니다.")

    rows.sort(key=lambda row: (row["category"], row["question"]))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=["category", "question", "answer", "source"]
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
