#!/data/data/com.termux/files/usr/bin/bash
# 인스타 영상 다운로더 설치 (Termux에서 한 번만 실행)
set -e
RAW="https://raw.githubusercontent.com/cog200489-code/my-hub1/${BRANCH:-ccr-8ba1dedb-hj0w8k}/tools/insta-dl"

echo "▶ 1/4 저장소 권한 (팝업이 뜨면 '허용')"
[ -d ~/storage/downloads ] || termux-setup-storage
for i in $(seq 1 20); do [ -d ~/storage/downloads ] && break; sleep 1; done

echo "▶ 2/4 프로그램 설치 (몇 분 걸려요)"
pkg update -y
pkg upgrade -y -o Dpkg::Options::="--force-confnew"
pkg install -y python ffmpeg curl

echo "▶ 3/4 yt-dlp 설치"
pip install -U yt-dlp

echo "▶ 4/4 공유 버튼 연결"
mkdir -p ~/bin
curl -fsSL "$RAW/termux-url-opener" -o ~/bin/termux-url-opener
chmod +x ~/bin/termux-url-opener

echo ""
echo "✅ 끝! 인스타 영상 → 공유 → Termux 누르면"
echo "   내 파일 > 다운로드 > Instagram 에 저장돼요."
