#!/usr/bin/env python3
"""
Backup Migration Script
기존의 모든 백업 파일들을 주차별로 그룹화하여 각 주차의 마지막 파일을 database에 저장
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migrate_backups.log'),
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


def parse_backup_filename(filepath):
    """
    백업 파일명에서 타임스탬프를 추출

    Args:
        filepath: Path 객체

    Returns:
        datetime 객체 또는 None
    """
    try:
        # papers_20251103_220807.json -> 20251103_220807
        filename = filepath.stem  # 확장자 제외
        timestamp_str = filename.replace('papers_', '')
        # YYYYMMDD_HHMMSS 형식을 datetime으로 변환
        return datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
    except Exception as e:
        logger.warning(f"파일 타임스탬프 파싱 실패: {filepath.name} - {e}")
        return None


def group_backups_by_week(backup_dir='backups'):
    """
    백업 파일들을 주차별로 그룹화

    Args:
        backup_dir: 백업 디렉토리 경로

    Returns:
        dict: {week_number: [(filepath, datetime), ...]}
    """
    backup_path = Path(backup_dir)

    if not backup_path.exists():
        logger.error(f"백업 디렉토리를 찾을 수 없습니다: {backup_dir}")
        return {}

    # papers_*.json 파일 찾기
    backup_files = list(backup_path.glob('papers_*.json'))

    if not backup_files:
        logger.error("백업 파일을 찾을 수 없습니다.")
        return {}

    logger.info(f"총 {len(backup_files)}개의 백업 파일 발견")

    # 주차별로 그룹화
    weekly_backups = defaultdict(list)

    for filepath in backup_files:
        file_date = parse_backup_filename(filepath)

        if file_date is None:
            continue

        week_number = get_week_number(file_date)
        weekly_backups[week_number].append((filepath, file_date))

    logger.info(f"총 {len(weekly_backups)}개의 주차로 그룹화됨")

    return weekly_backups


def get_latest_backup_for_week(week_backups):
    """
    주차별 백업 파일 중 가장 최근 것을 반환

    Args:
        week_backups: [(filepath, datetime), ...] 리스트

    Returns:
        (filepath, datetime) 튜플
    """
    return max(week_backups, key=lambda x: x[1])


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

        # 각 논문의 week 필드를 현재 주차로 업데이트
        for paper in papers_data:
            paper['week'] = week_number

        # database 디렉토리에 저장
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(papers_data, f, ensure_ascii=False, indent=2)

        logger.info(f"  [OK] {target_file.name} 저장 완료 ({len(papers_data)}개 논문)")

        # static/database 디렉토리에도 복사 (GitHub Pages용)
        static_database_path = Path('static') / 'database'
        static_database_path.mkdir(parents=True, exist_ok=True)
        static_target_file = static_database_path / f"paper_week{week_number}.json"

        shutil.copy2(target_file, static_target_file)

        return True

    except json.JSONDecodeError as e:
        logger.error(f"  [ERROR] JSON 파싱 실패: {e}")
        return False
    except Exception as e:
        logger.error(f"  [ERROR] 저장 중 오류: {e}")
        return False


def migrate_all_backups():
    """
    모든 백업 파일을 주차별로 그룹화하여 database에 마이그레이션

    Returns:
        tuple: (성공 수, 실패 수)
    """
    logger.info("=" * 70)
    logger.info("백업 파일 마이그레이션 시작")
    logger.info("=" * 70)

    # 주차별로 백업 그룹화
    weekly_backups = group_backups_by_week()

    if not weekly_backups:
        logger.error("마이그레이션할 백업이 없습니다.")
        return 0, 0

    # 주차 순서대로 정렬
    sorted_weeks = sorted(weekly_backups.keys())

    success_count = 0
    fail_count = 0

    logger.info(f"\n주차별 마이그레이션 시작 ({len(sorted_weeks)}개 주차)")
    logger.info("-" * 70)

    for week_number in sorted_weeks:
        week_files = weekly_backups[week_number]
        latest_file, latest_date = get_latest_backup_for_week(week_files)

        logger.info(f"\n[WEEK] {week_number}")
        logger.info(f"  - 백업 파일 수: {len(week_files)}개")
        logger.info(f"  - 최신 파일: {latest_file.name}")
        logger.info(f"  - 파일 날짜: {latest_date.strftime('%Y-%m-%d %H:%M:%S')}")

        # 데이터베이스에 저장
        if save_to_database(latest_file, week_number):
            success_count += 1
        else:
            fail_count += 1

    logger.info("\n" + "=" * 70)
    logger.info("마이그레이션 완료!")
    logger.info(f"  - 성공: {success_count}개 주차")
    logger.info(f"  - 실패: {fail_count}개 주차")
    logger.info("=" * 70)

    return success_count, fail_count


def main():
    """메인 함수"""
    try:
        success, fail = migrate_all_backups()

        # 결과 요약
        print("\n" + "=" * 70)
        print("마이그레이션 결과 요약")
        print("=" * 70)
        print(f"[SUCCESS] 성공: {success}개 주차")
        if fail > 0:
            print(f"[FAIL] 실패: {fail}개 주차")
        print(f"[INFO] 데이터베이스 디렉토리: database/")
        print(f"[INFO] Static 디렉토리: static/database/")
        print("=" * 70)

        exit(0 if fail == 0 else 1)

    except Exception as e:
        logger.error(f"예상치 못한 오류 발생: {e}", exc_info=True)
        exit(1)


if __name__ == "__main__":
    main()
