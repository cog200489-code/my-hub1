---
name: second-brain
description: Use when 주인님 shares an inspiration, video/article link or summary, idea, or memo to save — or asks to find/organize past notes. Saves it as a note in 주인님's Obsidian vault on Google Drive (via the Google Drive connector), matching the vault's existing format.
---

# 제2의 뇌 (옵시디언 볼트 · 구글 드라이브)

주인님의 제2의 뇌는 **구글 드라이브에 있는 옵시디언 볼트**다. GitHub 저장소에는 노트를 두지 않는다.

## 볼트 위치 (Google Drive 폴더 ID)
- 볼트 루트: `1kF5P1t0D-cFQxaY74ZgnQ95Ha4CWzZBK`
- `Inbox`: `1swV2_fRrdQbHi55kVWylYhdUCBNfY5QG` — 어디 둘지 애매할 때
- `인사이트`: `131PmcnHLFPcTiQDlGUBKS6s701DvRC_B`
  - `AI도구`: `1C_PYbMyGGQXyb1da1zP0i2zWzMOMErQy`
  - 그 외 하위: 인생코칭, 성장마인드, 건강, 격투기
- `학원운영`: `1-aMCKkVAJKHHMzZnrU6P7zYLcziQ6xDE`
- `학습자료`: `1hg1IYlFjdw7Yy-gMySrxG4PEcaolUXqI`
- `일기`: `1cbQXqd0H_UDhet9dzHOltmIYwjfQmaxf`
- `보관`: `1-hA9Yri7MXQ1j9JgzFlgZI8ih3Wb_3Pe`

폴더 ID가 안 맞으면 Google Drive 검색으로 `.obsidian` 폴더의 부모를 찾아 볼트 루트를 다시 확인한다.

## 저장할 때
1. 저장 전에 같은 폴더의 최근 노트 하나를 읽어 형식을 맞춘다.
2. Google Drive `create_file`로 저장: 제목은 `한글 제목.md`, `contentMimeType: text/markdown`, `disableConversionToGoogleType: true`, 알맞은 폴더 ID를 `parentId`로.
3. 기본 형식 (스크랩):
   ```
   ---
   type: 스크랩
   source: 원본 링크
   channel: 채널/작성자
   scrap_date: YYYY-MM-DD
   verdict: 시도할 만함 | 일부 채택 | 보류 | 해당 없음
   tags: [스크랩, 주제 태그들]
   ---
   # 제목
   > 한 줄 요약
   ## 1. 핵심 내용
   ## 2. Claude의 생각   (좋은 점 / 빈틈·비판 / 주인님 적용 아이디어)
   ## 3. 판정
   ## 연결   ([[기존 노트 제목]] 링크)
   ```
4. 태그는 기존 노트에서 쓰는 태그를 먼저 재사용한다.
5. 주인님에게는 저장 위치·제목·판정 1~2줄만 보고한다.

## 찾을 때
Google Drive `search_files`로 볼트 안에서 제목·본문 검색 후 짧게 목록으로 보여준다.

## 원칙
- 확인 안 된 정보는 노트 끝에 ⚠️로 표시
- 기존 노트를 고치거나 지울 때는 먼저 주인님에게 확인
- Google Drive 커넥터가 없는 세션이면 그렇다고 말하고, 노트 내용을 채팅으로 주어 주인님이 붙여넣게 한다
