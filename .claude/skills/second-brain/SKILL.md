---
name: second-brain
description: Use when 원장님 shares an inspiration, video/article link or summary, idea, or memo to save — or asks to find/organize past notes. Files it as a tagged markdown note in brain/notes and updates brain/README.md.
---

# 제2의 뇌 정리

## 저장할 때
1. 파일: `brain/notes/YYYY-MM-DD-짧은-영문-슬러그.md` (오늘 날짜)
2. 맨 위 frontmatter:
   ```yaml
   ---
   title: 한글 제목
   date: YYYY-MM-DD
   source: 원본 링크 (없으면 생략)
   type: 영상요약 | 글요약 | 아이디어 | 메모
   tags: [3~6개, 한글, 띄어쓰기 없이]
   status: 📥 수집
   ---
   ```
3. 본문 순서: `> 한 줄 요약` → 핵심 내용(표나 짧은 목록) → `## 💡 나한테 쓸모` 체크리스트 → `## 🔗 연결` ([[태그]] 링크)
4. 태그는 `brain/README.md`의 기존 태그를 먼저 재사용. 새 태그만 목록에 추가.
5. `brain/README.md` 노트 목록 표 맨 위에 한 줄 추가.
6. 커밋하고 푸시. 원장님에게는 저장한 제목·태그·쓸모 1~2줄만 보고.

## 찾을 때
`brain/notes`에서 태그·제목·본문을 검색해 관련 노트를 짧게 목록으로 보여준다.

## 상태 바꾸기
원장님이 "써봤어", "적용했어" 하면 status를 `✅ 적용함`으로, "필요 없어" 하면 `🗄️ 보관`으로 바꾸고 README 표도 맞춘다.

## 원칙
- 확인 안 된 정보(링크, 저장소 주소 등)는 노트 끝에 ⚠️로 표시
- 짧게. 폰에서 한 화면에 핵심이 보이게
