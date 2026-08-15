#!/usr/bin/env bash
# doormaster.co.kr 4개 사이트 배포
# 사용법:  ./deploy.sh            또는   ./deploy.sh "문구 수정"
set -e
cd "$(dirname "$0")"

echo
echo "============================================"
echo "  doormaster.co.kr  4개 사이트 배포"
echo "============================================"
echo

echo "[1/3] HTML 생성 중..."
python3 build.py

echo
echo "[2/3] 변경사항 저장 중..."
git add -A

if git diff --cached --quiet; then
  echo "   바뀐 내용이 없습니다. 배포할 게 없습니다."
  exit 0
fi

MSG="${1:-사이트 수정}"
git commit -m "$MSG"

echo
echo "[3/3] GitHub 전송 중..."
git push

echo
echo "============================================"
echo "  완료! 1~2분 뒤 사이트에 반영됩니다."
echo
echo "  https://doormaster.co.kr"
echo "  https://door.doormaster.co.kr"
echo "  https://marble.doormaster.co.kr"
echo "  https://bath.doormaster.co.kr"
echo "============================================"
echo
