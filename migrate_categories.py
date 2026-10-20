#!/usr/bin/env python3
"""
기존 논문들에 카테고리 정보를 추가하는 마이그레이션 스크립트
"""

import json
import os
from paper_collector import generate_korean_summary


def migrate_existing_papers():
    """기존 논문들에 카테고리 정보를 추가"""

    # 기존 논문 로드
    if not os.path.exists("papers.json"):
        print("papers.json 파일이 없습니다.")
        return

    with open("papers.json", "r", encoding="utf-8") as f:
        papers = json.load(f)

    print(f"총 {len(papers)}개의 논문을 처리합니다.")

    # 카테고리가 없는 논문들 찾기
    papers_to_update = []
    for paper in papers:
        if not paper.get("categories"):
            papers_to_update.append(paper)

    print(f"카테고리 정보가 없는 논문: {len(papers_to_update)}개")

    if not papers_to_update:
        print("모든 논문에 이미 카테고리 정보가 있습니다.")
        return

    # 카테고리 정보 추가
    for i, paper in enumerate(papers_to_update, 1):
        print(f"\n처리 중: {i}/{len(papers_to_update)}")
        print(f"제목: {paper['title']}")

        try:
            # 카테고리 생성
            result = generate_korean_summary(paper["title"], paper["abstract"])
            if result and result.get("categories"):
                paper["categories"] = result["categories"]
                print(f"카테고리 추가됨: {result['categories']}")
            else:
                paper["categories"] = ["기타"]
                print("카테고리 생성 실패, '기타'로 설정")
        except Exception as e:
            print(f"오류 발생: {e}")
            paper["categories"] = ["기타"]

        # 진행상황 저장 (매 5개마다)
        if i % 5 == 0:
            with open("papers.json", "w", encoding="utf-8") as f:
                json.dump(papers, f, ensure_ascii=False, indent=2)
            print(f"진행상황 저장됨 ({i}/{len(papers_to_update)})")

    # 최종 저장
    with open("papers.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

    print(
        f"\n마이그레이션 완료! 총 {len(papers_to_update)}개 논문에 카테고리 정보가 추가되었습니다."
    )


if __name__ == "__main__":
    migrate_existing_papers()
