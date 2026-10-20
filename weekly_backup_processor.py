#!/usr/bin/env python3
"""
Weekly Backup Processor
매주 월요일에 실행되어 백업 파일 중 가장 최근 것을 해당 주차로 계산하여 database에 저장
"""

import os
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weekly_backup_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_week_number(date):
    """
    주어진 날짜의 주차를 계산 (ISO 8601 형식: YYYY-WNN)

    Args:
        date: datetime 객체

    Returns:
        str: "2025-W44" 형식의 주차 문자열
    """
    year, week, _ = date.isocalendar()
    return f"{year}-W{week:02d}"


def get_most_recent_backup(backup_dir='backups'):
    """
    백업 디렉토리에서 가장 최근 papers_*.json 파일을 찾음

    Args:
        backup_dir: 백업 파일이 저장된 디렉토리

    Returns:
        tuple: (파일 경로, 파일 날짜) 또는 (None, None)
    """
    backup_path = Path(backup_dir)

    if not backup_path.exists():
        logger.error(f"백업 디렉토리를 찾을 수 없습니다: {backup_dir}")
        return None, None

    # papers_YYYYMMDD_HHMMSS.json 형식의 파일 찾기
    backup_files = list(backup_path.glob('papers_*.json'))

    if not backup_files:
        logger.error("백업 파일을 찾을 수 없습니다.")
        return None, None

    # 파일명에서 타임스탬프 추출하여 정렬
    def get_timestamp(filepath):
        try:
            # papers_20251103_220807.json -> 20251103_220807
            filename = filepath.stem  # 확장자 제외
            timestamp_str = filename.replace('papers_', '')
            # YYYYMMDD_HHMMSS 형식을 datetime으로 변환
            return datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
        except Exception as e:
            logger.warning(f"파일 타임스탬프 파싱 실패: {filepath.name} - {e}")
            return datetime.min

    # 가장 최근 파일 찾기
    most_recent_file = max(backup_files, key=get_timestamp)
    file_date = get_timestamp(most_recent_file)

    logger.info(f"가장 최근 백업 파일: {most_recent_file.name} (날짜: {file_date})")

    return most_recent_file, file_date


def save_to_database(backup_file, week_number, database_dir='database'):
    """
    백업 파일을 주차별 데이터베이스 파일로 저장

    Args:
        backup_file: 백업 파일 경로
        week_number: 주차 번호 (예: "2025-W44")
        database_dir: 데이터베이스 디렉토리

    Returns:
        bool: 성공 여부
    """
    database_path = Path(database_dir)
    database_path.mkdir(exist_ok=True)

    # 목표 파일 경로
    target_file = database_path / f"paper_week{week_number}.json"

    try:
        # 백업 파일 읽기
        with open(backup_file, 'r', encoding='utf-8') as f:
            papers_data = json.load(f)

        logger.info(f"백업 파일에서 {len(papers_data)}개의 논문 로드됨")

        # 각 논문에 week 필드가 있는지 확인하고 없으면 추가
        for paper in papers_data:
            if 'week' not in paper:
                paper['week'] = week_number
                logger.debug(f"논문에 week 필드 추가: {paper.get('title', 'Unknown')}")

        # database 디렉토리에 저장
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(papers_data, f, ensure_ascii=False, indent=2)

        logger.info(f"[SUCCESS] 주차별 데이터베이스 저장 완료: {target_file}")
        logger.info(f"   - 주차: {week_number}")
        logger.info(f"   - 논문 수: {len(papers_data)}")

        # static/database 디렉토리에도 복사 (GitHub Pages용)
        static_database_path = Path('static') / 'database'
        static_database_path.mkdir(parents=True, exist_ok=True)
        static_target_file = static_database_path / f"paper_week{week_number}.json"

        shutil.copy2(target_file, static_target_file)
        logger.info(f"[SUCCESS] Static 데이터베이스에도 복사 완료: {static_target_file}")

        return True

    except json.JSONDecodeError as e:
        logger.error(f"백업 파일 JSON 파싱 실패: {e}")
        return False
    except Exception as e:
        logger.error(f"데이터베이스 저장 중 오류 발생: {e}")
        return False


def process_weekly_backup():
    """
    매주 월요일에 실행되는 메인 함수
    가장 최근 백업을 찾아 해당 주차로 계산하여 database에 저장

    Returns:
        bool: 성공 여부
    """
    logger.info("=" * 60)
    logger.info("주간 백업 처리 시작")
    logger.info("=" * 60)

    # 가장 최근 백업 파일 찾기
    backup_file, file_date = get_most_recent_backup()

    if backup_file is None:
        logger.error("처리할 백업 파일이 없습니다.")
        return False

    # 해당 주차 계산
    week_number = get_week_number(file_date)
    logger.info(f"계산된 주차: {week_number}")

    # 데이터베이스에 저장
    success = save_to_database(backup_file, week_number)

    if success:
        logger.info("=" * 60)
        logger.info("주간 백업 처리 완료!")
        logger.info("=" * 60)
    else:
        logger.error("주간 백업 처리 실패")

    return success


def main():
    """메인 함수"""
    try:
        success = process_weekly_backup()
        exit(0 if success else 1)
    except Exception as e:
        logger.error(f"예상치 못한 오류 발생: {e}", exc_info=True)
        exit(1)


if __name__ == "__main__":
    main()
