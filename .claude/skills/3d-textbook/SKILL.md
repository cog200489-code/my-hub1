---
name: 3d-textbook
description: Use when building or extending a 더이룸 3D 교과서 page — a textbook unit (science/math) turned into a single-page interactive 3D web lesson with direct manipulation, missions and 도장 (stamps), published as a Claude Artifact. Covers the reusable unit template, Three.js setup that works inside Artifacts, phone/tablet performance, fact-checking of numbers, and the test pass before showing 주인님.
---

# 더이룸 3D 교과서

교과서 한 단원을 **3D로 보고 → 직접 만져 보고 → 미션으로 확인하고 → 도장 받는** 웹 교재 한 장으로 만든다.
시제품: 3D 발전소(에너지 전환), 3D 일주 운동(지구과학).

## 원칙
1. **효과의 핵심은 3D가 아니라 「먼저 예측 → 조작해서 확인 → 도장」.** 3D는 개념을 눈으로 보여 줄 때만 쓴다. 3D가 필요 없는 단원은 덮개 퀴즈(HTML)로 만든다.
2. **단원마다 새로 만들지 말고 틀을 재사용**한다(아래 「단원 틀」). 주인님은 한 단원이 되면 바로 다른 단원으로 넓히신다.
3. **숫자는 사실 확인 후 넣는다.** 별 좌표·효율·궤도 같은 값은 울프럼 커넥터(`mcp__Wolfram__WolframAlpha`)나 공식 자료로 확인하고, 어림값이면 화면에 「어림값」이라고 적는다. 근거 없는 홍보 통계(예: "시각 자료 기억률 65%")는 넣지 않는다.
4. **교육과정 용어는 한국 중·고 교과서 표현**을 쓴다(예: 일주 운동, 천구, 역학적 에너지 보존). 영어 용어는 괄호로만.
5. **학생 개인정보를 담지 않는다.** 이름·점수 저장이 필요하면 원격수업팀장과 상의한다.

## 단원 틀 (페이지 구조)
- 펼친 책 모양: **왼쪽 = 3D 장면**, **오른쪽 = 설명·조작판·미션** (폰에서는 위아래로 쌓기)
- 조작판: 시점 버튼(밖에서/정면/위 등), 시간 재생·슬라이더, 핵심 변수 1~2개(위도, 에너지원 등), 켜고 끄기(자취·라벨)
- 미션 3~5개: 각 미션은 「질문 → 학생이 조작 → 조건이 맞으면 자동 통과 → 도장」. 마지막 미션은 「왜 그럴까?」 서술 대신 보기 고르기
- 도장판: 「참 잘했어요」 빨간 원형 도장, 모두 모으면 완료 화면
- 틀린 답은 오답 장부 연결 자리(지금은 화면 아래 목록)
- 맨 아래: 단원명·학년·「선생님 확인 전 시범판」 표시

새 단원은 시제품 아티팩트를 `Artifact action:"read"`로 읽어 와서 **장면·변수·미션 데이터만 바꾼다.** 공통 부분(책 레이아웃, 도장, 조작판 스타일)은 그대로 둔다.

## Three.js를 아티팩트에서 쓰는 법
- 아티팩트는 정해진 CDN만 허용: `cdnjs.cloudflare.com`(우선), `cdn.jsdelivr.net/npm/`, `unpkg.com`. **버전을 정확히 고정**한다(예: `three@0.160.0`). 최신 2주 이내 버전 금지.
- ES 모듈을 쓸 때는 `<script type="importmap">`으로 `three`와 `three/addons/`를 jsDelivr 고정 버전 주소에 연결하고 `OrbitControls`는 addons에서 가져온다.
- 텍스처·모델 파일은 외부에서 못 불러온다 → 도형(구·원기둥·선)으로 만들거나 data URI로 넣는다. 글자 라벨은 CSS2D/HTML 오버레이나 캔버스 텍스처.
- 화면 테마(밝음/어두움) 토큰을 지키고, `prefers-reduced-motion`이면 자동 회전을 멈춘다.

## 폰·저사양 태블릿 성능
- `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`, 그림자는 꼭 필요할 때만
- 화면에 안 보이거나 정지 상태면 렌더 루프를 멈춘다(`IntersectionObserver` + 변경 있을 때만 그리기)
- 폴리곤은 적게(구 segment 32 이하), 별 수천 개는 `Points` 하나로
- 터치: OrbitControls 한 손가락 회전·두 손가락 확대, 페이지 스크롤과 싸우지 않게 캔버스에 `touch-action: none`은 3D 영역에만

## 보여 드리기 전 점검 (한 번만)
Playwright가 설치돼 있다(`require('playwright')`, 설치 명령 금지). 폰(390×844)·PC(1280×800)에서 한 번씩 찍어 본다.
- 첫 화면에 3D가 보이는가, 가로 스크롤이 없는가, 콘솔 오류가 없는가
- 미션을 스크립트로 한 번씩 통과시켜 도장이 찍히는가
문제를 한 번에 고치고 끝낸다(무한 반복 금지).

## 넘길 곳
- 수업 적용·학생 반응: 원격수업팀장 (판단 기준 「학생이 실제로 더 배우는가」)
- 오답 장부 연결: 전산개발실(오답 첨삭)
- 도구가 더 필요하면: 클로드 도구 관리 담당(`session_01CDd9Zx8ntVYvZFXJcdMAXf`)
