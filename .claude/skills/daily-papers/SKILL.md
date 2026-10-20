---
name: daily-papers
description: 오늘의 arXiv 신규 논문(cs.CV/LG/RO/CL/AI) 전수 평가 → Top 15 원문·alphaXiv 요약·그림을 읽고 정밀 리뷰 → 문체 검사·교차 검수 → 일간 리포트/사이트 생성 → push → 옵시디언 vault(nurilab-vault) 반영. 매일 아침 예약 실행되며 수동으로도 /daily-papers 로 실행 가능.
---

# 오늘의 arXiv 논문 평가 파이프라인

너(Claude)가 LLM 평가자 역할을 직접 수행한다. OpenAI API는 사용하지 않는다.
평가 기준·스키마·문체는 반드시 `.claude/skills/daily-papers/criteria.md`를 먼저 읽고 따른다.

## 0. 준비

```bash
pip install -r requirements.txt   # 이미 설치돼 있으면 생략 가능
python agent_pipeline.py prepare
```

- `ALPHAXIV_BLOCKED`가 출력되면 alphaXiv 없이 계속하고, 최종 보고에 그 줄을 그대로 남긴다.
- `NO_NEW_PAPERS`가 출력되면 (주말/공휴일/이미 처리됨) **1~5단계를 건너뛴다.** 단, 중단 전에
  `database/daily/`의 최신 리포트가 옵시디언 vault에 반영됐는지 확인하고(6단계의 대상 경로 참조),
  빠져 있으면 **6단계만 수행해 백필**한 뒤 그 사실을 보고한다. 이미 반영돼 있으면 그대로 중단·보고한다.
- 출력된 `WORK_DIR`(이하 `$WD`, 예: `database/daily/work/2026-08-20`)를 이후 단계에서 사용한다.

## 1. 스크리닝 (전수 채점)

`$WD/screen_batches/batch_*.json` (배치당 ~25편)을 **모두** 채점해서
같은 파일명으로 `$WD/screen_results/`에 저장한다. 스키마는 criteria.md 참조.

- 병렬 subagent를 사용한다: general-purpose 에이전트 3~4개를 동시에 띄우고
  배치 파일을 나눠 맡긴다. **스크리닝 subagent는 `model: "sonnet"`으로 띄운다** (초록만 보는 채점이라 충분함).
  각 subagent 프롬프트에는 다음을 포함한다:
  - criteria.md를 먼저 읽을 것
  - 맡은 배치 파일 목록과 결과 저장 경로
  - "모든 논문을 빠짐없이 채점하고, id는 그대로 복사할 것"
- 전 배치 완료 후 결과 파일 수가 배치 파일 수와 같은지 확인한다.

## 2. Top-K 선정 + 자료 모으기

```bash
python agent_pipeline.py select
```

- 스크리닝을 병합해 Top 15를 뽑고, 논문마다 다음을 만든다:
  - `$WD/texts/<id>.txt`: PDF 전문 텍스트 (사실·수치의 정본)
  - `$WD/figs/<id>.png`: 카드에 실릴 대표 그림
  - `$WD/alphaxiv/<id>.md`: alphaXiv 요약 글과 그 글의 그림·영상 캡션 (alphaXiv에 요약이 있을 때만)
  - 학회 판정 (`venue_detect.py`: comments → PDF 문구 → LaTeX 양식). 리뷰에서 학회를 따로 쓰지 않는다.
- 누락 경고가 나오면 해당 배치를 다시 채점한 뒤 재실행한다.

## 3. 정밀 리뷰 (Top 15)

먼저 alphaXiv 요약을 한 번 더 받는다 (스크리닝 동안 새로 생긴 것):

```bash
python agent_pipeline.py alphaxiv
```

각 Top 논문에 대해 criteria.md의 정밀 리뷰 스키마대로 `$WD/deep/<arxiv_id>.json`을 작성한다.
이 단계가 리포트 글의 품질을 정한다. **정밀 리뷰 subagent는 model을 지정하지 않고 띄워 루틴 모델(Opus)을 그대로 쓴다.**

- 논문당 subagent 1개, 4~5개씩 병렬로 실행한다. 각 subagent 프롬프트에 포함:
  - criteria.md 경로 (특히 「읽을 자료」, 「문체」, 「견본」 절을 따를 것)
  - 그 논문의 `$WD/texts/<id>.txt`, `$WD/alphaxiv/<id>.md`(있으면), `$WD/figs/<id>.png`(있으면) 경로와
    `$WD/papers.json`에서 그 논문의 메타데이터(제목·저자·comments)
  - 그림 PNG는 Read 도구로 직접 보고 figure_caption을 쓸 것
  - alphaXiv 요약은 설명 순서와 결정적 비교를 고르는 데 참고만 하고, 번역해서 옮기지 말 것.
    수치는 원문 텍스트에서 확인한 것만 쓸 것
  - links(프로젝트·코드·영상)는 원문 텍스트에 주소가 그대로 있을 때만 넣을 것
  - 결과를 JSON 파일로 저장할 것 (유효한 JSON인지 확인)

## 4. 트렌드 종합

`$WD/papers.json`의 top_ids와 `$WD/deep/*.json`(headline, method, lab_relevance)을 바탕으로
criteria.md의 종합 형식에 맞춰 `$WD/synthesis.md`를 작성한다.

## 4.3 기계 검사

```bash
python agent_pipeline.py check
```

- 빈 칸·JSON 오류·금지어·줄표·`~다`/`~습니다` 어미·150자 넘는 문장을 잡는다.
- 지적된 문장만 고치고 다시 돌린다. `CHECK: 0건`이 될 때까지 반복한다 (최대 3회).
  낱말이 실제 뜻으로 쓰였으면(캐비닛을 닫음 등) 그대로 두고, 남은 건수와 이유를 보고에 적는다.

## 4.5 교차 검수 (게시 전)

글을 쓴 에이전트가 아닌 **새 subagent**가 검수한다. criteria.md의 판정 기준이
"안 읽은 사람이 2분 안에 이해하지 못하면 실패"이므로, 검수자는 그 글이 어떻게 나왔는지
모르는 상태여야 한다. 3단계에서 쓴 subagent를 재사용하지 않는다.

1. 검수 subagent 3개를 병렬로 띄운다. general-purpose 에이전트를 쓴다.
   - 2개는 Top-15를 나눠 맡는다 (각 7~8편).
   - 1개는 `$WD/synthesis.md`를 맡는다.
2. 각 subagent 프롬프트에 포함할 것:
   - criteria.md를 먼저 읽고 **문체 절과 견본을 검수 기준으로 삼을 것**
   - 맡은 `$WD/deep/<id>.json`(또는 synthesis.md) 경로 목록
   - 검수 관점은 다섯으로 제한: (1) 문체 규칙 위반, (2) 한 번에 이해 안 되는 문장,
     (3) 정의 없이 나온 약어·방법 이름·benchmark 이름, (4) 같은 논문 안에서 칸끼리 되풀이되거나 어긋나는 서술,
     (5) 숫자·단위·링크 표기 이상
   - **원문 PDF를 읽지 말 것.** 사실이 의심되면 "원문 확인 필요"로만 표시한다.
     처음 읽는 사람의 눈을 유지하는 것이 이 단계의 목적이다.
   - 취향 수준의 지적 금지. 고치면 명확히 나아지는 것만. 전면 재작성 제안 금지.
     문장 단위로만 고치고, 지적마다 수정안을 한 줄로 제시할 것
   - 파일을 직접 고치지 말고 `$WD/review/review_<n>.md`에 지적만 쓸 것.
     형식: `### <arxiv_id>` 아래 `- [높음|낮음] <지적> → 수정안: <문장>`
3. 결과를 읽고 **타당한 지적만** `deep/*.json`과 `synthesis.md`에 반영한다:
   - 스키마(칸 구성·불릿 형식)는 유지한다. 지적된 문장만 고친다.
   - "원문 확인 필요" 지적은 `$WD/texts/<id>.txt`에서 확인되는 경우에만 반영한다.
   - 문체 지적이 옳은지 헷갈리면 criteria.md 문체 절이 우선한다.
   - 반영/기각 건수를 세어 둔다 (7단계 보고에 쓴다).
4. 반영 뒤 `python agent_pipeline.py check`를 다시 돌려 0건인지 확인한다.

## 5. 조립·배포

```bash
python agent_pipeline.py assemble
git add database/ static/
git commit -m "Update daily arXiv report [claude-agent] $(date +%Y-%m-%d)"
git push
```

- push되면 GitHub Actions(deploy.yml)가 GitHub Pages 배포와 Notion 게시를 수행한다.

## 6. 옵시디언 vault 반영

일간 리포트를 누리랩 옵시디언 vault(`bareblackfoot/nurilab-vault`)에도 넣는다.
루틴 실행 시 vault는 paper_summary와 **나란히 clone**되어 있다(`../nurilab-vault`).
clone이 없으면 이 단계를 건너뛰되, 최종 보고에 "vault 반영 실패: nurilab-vault clone 없음"을 반드시 남긴다.

1. 대상 파일: `../nurilab-vault/00.Raw/논문/일간요약/<날짜>.md`
2. 내용: 아래 frontmatter 뒤에 빈 줄 하나, 그 다음 `database/daily/<날짜>.md` **전문을 그대로** 붙인다.
   vault의 `00.Raw/`는 불변 원본 보관소다. 내용을 요약하거나 다듬지 않는다.
   **`01.Wiki/`, `index.md`, `log.md` 등 vault의 다른 파일은 절대 건드리지 않는다.**

   ```yaml
   ---
   ingest: skip
   source_type: "paper-summary"
   title: "일간 arXiv Top 15 <날짜>"
   date: "<날짜>"
   url: "https://bareblackfoot.github.io/paper_summary/daily/<날짜>/"
   generated_by: "daily-arxiv-papers 루틴 (bareblackfoot/paper_summary)"
   ---
   ```

   (`ingest: skip`은 vault 규약이다. 매일 15편이 미처리 집계를 덮지 않게 한다. 빼먹지 말 것.)
3. commit·push. vault는 다른 기기들이 15분마다 동기화하므로 **반드시 rebase 후 push**한다:

   ```bash
   git -C ../nurilab-vault pull --rebase
   git -C ../nurilab-vault add "00.Raw/논문/일간요약/"
   git -C ../nurilab-vault commit -m "일간 arXiv 요약 <날짜> [claude-agent]"
   git -C ../nurilab-vault push
   ```

   push가 거부되면 `pull --rebase` 후 1회 재시도한다.
4. 이 단계가 실패해도 파이프라인 전체를 실패로 처리하지 않는다. 대신 **최종 보고에
   vault 반영 성공/실패를 반드시 한 줄로 명시한다** (조용히 넘어가지 말 것).

## 7. 보고

마지막으로 음슴체로 보고한다: 전체/카테고리별 논문 수, Top 5 제목·점수,
사이트 주소(https://bareblackfoot.github.io/paper_summary/),
**alphaXiv 요약을 쓴 논문 수(n/15)와 ALPHAXIV_BLOCKED 여부**,
**학회 판정 결과(채택·투고·양식 추정·판정 못 함 편수)**,
**기계 검사 결과(마지막 CHECK 건수)**, **교차 검수 결과(지적 n건 중 m건 반영)**,
**vault 반영 결과(성공한 파일 경로 또는 실패 사유)**.

## 문제 발생 시

- arXiv 접속 실패: 3초 간격으로 2~3회 재시도 후, 그래도 실패하면 중단하고 보고.
- alphaXiv 접속 실패: 그 논문은 alphaXiv 없이 리뷰한다. 파이프라인은 멈추지 않는다.
- 특정 논문 텍스트 추출 실패: arXiv PDF → arXiv HTML → alphaXiv 추출 전문 순으로 자동 시도함.
  셋 다 실패하면 초록만으로 리뷰하고 text_source에 그렇게 기록됨. 계속 진행.
- assemble 경고(리뷰 누락): 누락분을 채우고 재실행. 정말 불가하면 `--allow-missing` 사용.
- 검수 subagent 실패(4.5단계): 파이프라인을 멈추지 말고 진행하되, 최종 보고에
  "교차 검수 생략: <사유>"를 남긴다. 조용히 넘어가지 말 것.
