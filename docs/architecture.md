# architecture.md — 입력 → 처리 → 출력  〔D5 핵심〕

> D4 핵심기능을 동작 구조로. 시작 초안 — STEP에서 확정.

| 섹션 | 내용 |
|---|---|
| Goal | 질문에 근거 있는 참고용 답변을 준다 |
| Input | 고객 질문(텍스트) · data/ FAQ(공개·더미) |
| Process | ① (선택)카테고리 분류 → ② 관련 FAQ 검색(Supabase) → ③ 근거로 LLM 답변(BizRouter, 서버 /api/answer) |
| Tools | Supabase(검색) · BizRouter LLM · (선택)분류기 |
| Output | 화면 답변 + 근거 FAQ + '담당자 확인 필요'(escalate) |
| HITL | 고객 발송 전 직원 확인 / 금액·범위 밖 → 상담사 |
| Failure | 검색 0건·근거 없음 → 단정 금지·상담사 연결 / LLM 실패 → '잠시 후 다시' |
| Cost | gpt-5-nano, 질문당 ≈1원 |
