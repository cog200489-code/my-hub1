# 인스타 영상 다운로더 (갤럭시용)

인스타 앱에서 **공유 → Termux** 한 번이면 영상이 `내 파일 > 다운로드 > Instagram`에 저장된다.
설명글은 같은 이름의 `.md` 메모(태그 `#인스타 #영감`)로 같이 저장되어 옵시디언 볼트에 바로 옮길 수 있다.

## 설치 (한 번만)
1. Termux 설치: F-Droid 또는 https://github.com/termux/termux-app/releases (플레이스토어 판은 오래됨)
2. Termux를 열고 아래 한 줄 붙여넣기 → 엔터 → 저장소 권한 팝업 "허용"

```
curl -fsSL https://raw.githubusercontent.com/cog200489-code/my-hub1/ccr-8ba1dedb-hj0w8k/tools/insta-dl/setup.sh | bash
```

## 쓰기
릴스·게시물 → 종이비행기(공유) → 앱 목록에서 **Termux** → 끝.

## 안 될 때
- 실패하면 yt-dlp를 자동 업데이트하고 한 번 더 시도한다.
- 그래도 "로그인 필요"가 뜨면 인스타 쿠키 파일을 `~/.insta-cookies.txt`에 두면 쓴다(선택).
- 본인 영상이나 개인 참고용으로만 쓴다. 남의 영상을 다시 올리면 저작권 문제.
