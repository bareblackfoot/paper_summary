#!/bin/bash

echo "=================================================="
echo "백업 파일 마이그레이션 스크립트"
echo "=================================================="
echo ""

# Python 실행
python3 migrate_backups_to_database.py

# 결과 확인
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 마이그레이션이 성공적으로 완료되었습니다."
    echo ""
    echo "생성된 파일 확인:"
    echo "- database/ 디렉토리:"
    ls -lh database/paper_week*.json 2>/dev/null | head -10
    echo ""
    echo "- static/database/ 디렉토리:"
    ls -lh static/database/paper_week*.json 2>/dev/null | head -10
else
    echo ""
    echo "❌ 마이그레이션 중 오류가 발생했습니다."
    echo "자세한 내용은 migrate_backups.log 파일을 확인하세요."
    exit 1
fi
