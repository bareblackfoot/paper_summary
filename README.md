# Daily arXiv Top-30 for Robot Learning / Embodied AI

매일 arXiv의 5개 카테고리 신규 목록을 전수 확인하고, robot learning / embodied AI 관점에서
가장 중요한 **상위 논문(기본 15편)을 PDF 원문 기반으로 정밀 평가**하는 자동화 파이프라인입니다.

🌐 **Live Demo**: [https://bareblackfoot.github.io/paper_summary/](https://bareblackfoot.github.io/paper_summary/)

## 동작 방식

매일 아침 **Claude Code 예약 에이전트**가 `/daily-papers` 스킬(`.claude/skills/daily-papers/`)을
실행합니다. 평가(스크리닝·정밀 리뷰·트렌드 종합)는 Claude가 구독 토큰으로 직접 수행하므로
OpenAI API 비용이 들지 않습니다. 흐름:

1. **전수 수집** — 아래 5개 목록의 **New submissions 전체**를 수집합니다.
   - [cs.CV](https://arxiv.org/list/cs.CV/new) · [cs.LG](https://arxiv.org/list/cs.LG/new) · [cs.RO](https://arxiv.org/list/cs.RO/new) · [cs.CL](https://arxiv.org/list/cs.CL/new) · [cs.AI](https://arxiv.org/list/cs.AI/new)
   - **cross-list와 replacement는 집계에서 제외**하고, 여러 목록에 나타난 중복 논문은 1편으로 병합합니다.
2. **1차 스크리닝** — 모든 신규 논문을 제목/초록 기반으로 100점 만점 채점합니다.
   - 핵심 기준: novelty와 conceptual leap, potential impact, technical/empirical conviction,
     top-tier conference oral/highlight 수준 여부, 그리고 **robot learning / embodied AI relevance**
   - VLA·manipulation·world model·test-time optimization·failure recovery·robot memory·
     3DGS·scene graph·tactile·VLN 등 우선 주제는 가점, 단순 benchmark 개선·incremental engineering·
     단순 scale-up은 감점합니다.
3. **정밀 리뷰 (Top 15)** — 상위 15편(기본값, `config.TOP_K`)은 **arXiv PDF 원문을 내려받아**
   method/related work/experiments/ablations/limitations까지 검토한 뒤, 종합 점수·novelty 비교
   분석·benchmark 수치·학회 적합성 점수·연구 연관성을 항목별로 작성합니다.
4. **종합 분석** — 상위 논문을 관통하는 연구 트렌드 종합, 연구실을 위한 유망 연구 방향 제안,
   오늘 반드시 읽어야 할 논문 목록을 생성합니다.
5. **배포** — `database/daily/{날짜}.md`/`.json` 저장 후 git push → GitHub Actions(deploy.yml)가
   GitHub Pages 배포와 Notion('논문 목록' DB) 게시를 수행합니다.

파이프라인 단계는 `agent_pipeline.py`가 담당합니다:
`prepare`(수집·배치 생성) → Claude 스크리닝 → `select`(Top-K 선정·PDF 텍스트 추출) →
Claude 정밀 리뷰·종합 → `assemble`(리포트·사이트 생성).
OpenAI API 기반 완전 자동 버전(`paper_collector.py`)도 fallback으로 유지됩니다
(`.github/workflows/paper_collector.yml`, 수동 실행).

## Installation

```bash
git clone [repository-url]
cd paper_summary
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`.env` 파일에 OpenAI API 키를 설정합니다.

```
OPENAI_API_KEY=your_openai_api_key
# 선택: 모델 변경 (기본값: 스크리닝 gpt-5-nano / 정밀 리뷰 gpt-5-mini)
# OPENAI_SCREEN_MODEL=gpt-5-nano
# OPENAI_DEEP_MODEL=gpt-5-mini
```

## Usage

```bash
# 전체 파이프라인 (수집 → 스크리닝 → Top 30 정밀 리뷰 → 종합 → 저장)
python paper_collector.py

# 수집/파싱만 확인 (LLM 호출 없음)
python paper_collector.py --collect-only

# 디버그: 논문 8편만, Top 2만, 파일 저장 없이
python paper_collector.py --max-papers 8 --top-k 2 --dry-run

# 정적 사이트 생성 (static/ 폴더)
python static_generator.py
```

주요 옵션: `--top-k N`(정밀 리뷰 수), `--force`(이미 평가한 논문 재평가),
`--no-synthesis`(트렌드/전략 섹션 생략), `--dry-run`, `--collect-only`, `--max-papers N`

## Output

- `database/daily/{YYYY-MM-DD}.md` — 일간 리포트 (Top 30 상세 + 트렌드 + 연구 방향 + 필독 논문 + 전체 스크리닝 표)
- `database/daily/{YYYY-MM-DD}.json` — 전체 평가 데이터 (스크리닝 점수, 정밀 리뷰 필드 전체)
- `database/seen_ids.json` — 평가 완료 논문 ID (주말/중복 실행 시 재평가 방지)
- `static/` — GitHub Pages 정적 사이트 (일자별 아카이브 포함)

## 자동 실행 설정

- **기본**: Claude Code 예약 에이전트(routine)가 매일 아침 `/daily-papers` 실행 — 구독 토큰 사용, API 비용 $0
- **GitHub Actions Secrets**: `NOTION_TOKEN`, `NOTION_DATABASE_ID` (deploy.yml의 노션 게시용),
  `OPENAI_API_KEY` (fallback 워크플로용, 선택)
- **OpenAI fallback**: `.github/workflows/paper_collector.yml`을 수동 실행(workflow_dispatch)하면
  API 기반으로 전체 파이프라인 수행 (기본 gpt-5-nano/gpt-5-mini, 하루 ~$0.3~0.5)

## Tech Stack

- Python · BeautifulSoup4 (arXiv listing 파싱) · pypdf (PDF 원문 추출)
- OpenAI API (스크리닝 + 정밀 리뷰 + 트렌드 종합)
- Jinja2 + Markdown (정적 사이트 생성) · GitHub Actions + GitHub Pages

## Legacy

이 저장소는 원래 Hugging Face weekly papers 요약 서비스였습니다. 이전 코드 일부(`app.py`,
`notion_auto_publisher.py`, `migrate_categories.py`, `database/paper_week*.json`)는 레거시로 남아 있으며
현재 파이프라인에서는 사용하지 않습니다.

## License

MIT License
