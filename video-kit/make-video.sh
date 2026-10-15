#!/usr/bin/env bash
# 사용법: ./make-video.sh 입력영상.mp4
# 결과: output/이름_자막.srt, 이름_세로쇼츠.mp4(9:16), 이름_가로.mp4(16:9), 이름_정사각.mp4(1:1)
set -euo pipefail
IN="$(realpath "$1")"
cd "$(dirname "$0")"
NAME="$(basename "${IN%.*}")"; OUT=output; mkdir -p "$OUT"
SRT="$OUT/${NAME}_자막.srt"

echo "① 자막 생성 (Whisper)"; node transcribe.mjs "$IN" "$SRT" >/dev/null
echo "② 교정 사전 적용"
grep -v '^#' fixes.txt | while IFS='=' read -r a b; do [ -n "$a" ] && sed -i "s/${a}/${b}/g" "$SRT"; done

STYLE="FontName=Pretendard ExtraBold,Fontsize=13,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=1.6,Shadow=0,Alignment=2,MarginV=60"
SUB="subtitles=${SRT}:fontsdir=fonts:force_style='${STYLE}'"
ENC="-c:v libx264 -preset veryfast -crf 21 -c:a aac -b:a 128k -movflags +faststart"

echo "③ 세로 쇼츠 9:16"
ffmpeg -v error -y -i "$IN" -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,${SUB}" $ENC "$OUT/${NAME}_세로쇼츠.mp4"
echo "④ 가로 16:9 (흐린 배경)"
ffmpeg -v error -y -i "$IN" -filter_complex "[0:v]split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:5[bg];[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,${SUB}" $ENC "$OUT/${NAME}_가로.mp4"
echo "⑤ 정사각 1:1"
ffmpeg -v error -y -i "$IN" -filter_complex "[0:v]split[a][b];[a]scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080,boxblur=30:5[bg];[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,${SUB}" $ENC "$OUT/${NAME}_정사각.mp4"
echo "완료 → $OUT/"; ls -la "$OUT" | grep "$NAME"
