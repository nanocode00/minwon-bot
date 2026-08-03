# design.md — 네오브루탈리즘 화면 규칙

## 1. 방향
삼성생명의 신뢰감 있는 파랑에 굵은 테두리와 딱딱한 그림자를 결합한다. 장식보다 질문 → 근거 → 사람 확인 흐름을 우선한다.

## 2. 디자인 토큰
### 색상
- --ink: #0a0a0a
- --paper: #f8f5ec
- --blue: #0d63c9
- --yellow: #ffd84d
- --coral: #ff6b5e
- --mint: #6ee7b7
- --white: #ffffff
- --muted: #5b5b55

결과는 민트, 주의·담당자 확인은 코랄, 팁·면책은 노랑을 사용한다. 색상만으로 의미를 전달하지 않는다.

### 타이포그래피
- Pretendard, Apple SD Gothic Neo, Noto Sans KR, sans-serif
- 제목 font-weight 800, 모바일 36px/1.08, 데스크톱 64px/1.02
- 섹션 제목 28~36px, font-weight 800
- 본문 16~18px, line-height 1.65
- 보조 문구 14px 이상

### 간격
- 4px 기반: 4, 8, 12, 16, 24, 32, 48, 64
- 콘텐츠 최대 1180px
- 카드 여백 모바일 20px, 데스크톱 28~32px
- 조작 요소 최소 높이 48px

## 3. 핵심 스타일
### 카드·버튼·입력칸
- border: 3px solid var(--ink)
- box-shadow: 8px 8px 0 var(--ink), blur 0
- 배경은 paper, 카드 면은 white 또는 포인트 색
- 모서리는 0~12px로 제한하여 단단한 인상 유지

### 버튼
- 파랑 배경, 흰 글자, 굵은 테두리와 8px 그림자
- hover: translate(2px, 2px), 그림자 6px
- active: translate(6px, 6px), 그림자 2px
- disabled: 회색조, 작은 그림자, cursor not-allowed
- 과한 바운스·회전·반복 애니메이션 금지

### 입력
- 흰 배경, 굵은 label, 3px 테두리, 8px 그림자
- focus-visible에 4px 노랑 또는 파랑 outline
- 오류는 코랄 패널과 aria-invalid로 표시

### 카드·배지
- 답변 카드는 민트 헤더 또는 파랑 라벨 사용
- 근거 FAQ는 흰 카드와 파랑 번호 블록 사용
- 담당자 확인 필요 배지는 코랄 배경, 2px 검정 테두리, 4px 그림자
- 면책 배너는 노랑 배경과 검정 테두리

## 4. 레이아웃
- 상단 히어로 이미지 영역은 CSS 사각형·원·문서 카드로 질문 → FAQ → 확인을 표현
- 데스크톱 히어로 2열, 모바일은 텍스트 위·그래픽 아래 1열
- 질문 입력은 히어로 직후 가장 넓은 카드
- 결과와 근거는 별도 카드로 연속 배치
- 모바일은 전체 1열, 실행 버튼 전체 너비
- 추가 근거와 이용 안내는 Accordion으로 접기

## 5. 상태
- 초기: paper 배경과 흰 빈 상태
- 입력 중: 파랑 focus, 글자 수, 활성 버튼
- 로딩: 위치 이동 없는 진행 바
- 결과: 민트 답변 카드 + 파랑 FAQ 번호
- 오류·범위 밖: 코랄 패널 + 담당자 확인 필요 텍스트

## 6. 반응형·모션
- 전환은 120~180ms 위치·색상 변화만 허용
- 760px 이하 1열, 480px 이하 여백·제목 축소
- prefers-reduced-motion에서 transition과 animation 제거

## 7. 접근성
- 본문 대비 WCAG AA 이상
- focus-visible 제거 금지
- 터치 목표 최소 44×44px
- details/summary의 네이티브 키보드 동작 유지
- 시각 배치와 DOM 읽기 순서 일치
