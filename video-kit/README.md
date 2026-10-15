# 더이룸 영상 자동편집 키트 (Whisper + FFmpeg)

영상 1개 → 한국어 자막(SRT) + 자막 입힌 세로 쇼츠(9:16)·가로(16:9)·정사각(1:1).

## 설치 (새 세션마다 1번, 약 1분)
```bash
cd video-kit
npm install --ignore-scripts
mkdir -p fonts && cp node_modules/pretendard/dist/public/static/Pretendard-ExtraBold.otf fonts/
```

## 사용
```bash
./make-video.sh 영상.mp4   # 결과는 output/
```
자주 틀리는 말은 `fixes.txt`에 `틀린말=바른말`로 추가.
