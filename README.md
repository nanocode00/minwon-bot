# ○○생명 민원 지식봇 (수강생 빌드)

질문 → 분류(TF-IDF) → 검색(Supabase) → 답변(OpenRouter, 예정) → 근거·상담사 연결. 공개·가상·더미.

## 실행
1. `.env`에 `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY`, `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`, `OPENROUTER_MODEL`을 입력합니다.
2. `python server.py`를 실행합니다.
3. 브라우저에서 `http://127.0.0.1:8000`을 엽니다.

질문과 환경변수 값은 서버 로그에 출력하지 않습니다.

`POST /api/answer`는 서버에서 FAQ를 검색한 뒤, 검색된 내용만 OpenRouter에 전달해 참고 답변과 근거 FAQ 번호를 반환합니다. 이전 설정과의 호환을 위해 `BIZROUTER_API_KEY`, `BIZROUTER_BASE_URL`, `BIZROUTER_MODEL`도 인식하지만 OpenRouter 변수를 우선합니다.

신뢰성을 위해 답변 근거가 FAQ 1건으로 좁혀지면 원문 기반 엄격 모드로 답변하며, 여러 FAQ를 결합해야 할 때만 LLM 요약을 사용합니다. 검색 후보와 실제 인용은 `faqs`와 `cited_faq_ids`로 구분됩니다.

## 공개 저장소 데이터 정책

AI Hub 원본·파생 전체 데이터와 학습 모델은 재배포하지 않습니다. 로컬에 `ml/category_classifier.joblib`이 있으면 TF-IDF 분류기를 사용하고, 공개 체크아웃처럼 모델이 없으면 카테고리를 `미분류`로 표시한 뒤 Supabase 전체 FAQ 검색으로 안전하게 폴백합니다. 공개 저장소에는 합성 샘플 `data/sample_faqs.csv`만 포함됩니다.

## 산출물
docs/(prd·customer·architecture·design·progress) · AGENTS.md · tests/test_cases.md · skills/minwon-answer/SKILL.md · index.html · data/
