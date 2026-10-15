# 1급 비서관 (secretary)

실시간 대화 비서 웹앱. 서버 없는 단일 HTML, GitHub Pages로 배포.

- 주소: https://cog200489-code.github.io/my-hub1/secretary/
- 현재 버전: v3.6 (화면 제목 옆 표시)
- 파일: `index.html`(앱 전체) · `sw.js`(오프라인 캐시, 배포 때 캐시 이름 올리기) · `manifest.webmanifest` · `icon.svg`
- AI: Google Gemini API 무료 키 (사용자가 설정에서 입력, 브라우저 localStorage에만 저장)
- 받아쓰기: 안드로이드 = MediaRecorder 15초 조각 → Gemini / 데스크톱 크롬 = Web Speech API
- 설계 원칙과 운영 규칙은 소유자의 옵시디언 볼트 「00_1급 비서관 인계서」 참고
