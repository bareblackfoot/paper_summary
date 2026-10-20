# 논문 평가 기준 (누리랩 / NuRI Lab)

## 종합 점수 (100점 만점)
1. 기존 방식 대비 novelty와 conceptual leap
2. 해당 학계에 미칠 potential impact
3. technical / empirical conviction (방법의 타당성, 실험적 증거의 강도)
4. CVPR/ICCV/ECCV/NeurIPS/ICML/ICLR/AAAI/ACL/EMNLP/NAACL/CoRL/RSS/ICRA/IROS 같은
   top-tier conference에서 oral/highlight로 선정될 만한 수준인지
5. robot learning, embodied AI 및 아래 우선 주제와의 relevance (중요한 평가 요소)

## 우선적으로 높게 평가할 주제
VLA(vision-language-action)·generalist robot policy, manipulation/dexterous manipulation,
world models, test-time optimization/inference-time planning, failure detection·diagnosis·recovery,
counterfactual/causal reasoning, robot memory, language feedback 기반 learning, RL/IL,
skill chaining·long-horizon planning·TAMP, active perception/NBV,
object-centric 3D/4D representation·3DGS, scene graph/semantic mapping, tactile perception,
navigation/VLN, embodied spatial reasoning.
video understanding, multimodal foundation models, representation learning, generative models,
efficient inference도 robotics 문제에 새로운 원리·방법론을 제공하면 높게 평가.

## 감점 / 가점
- 감점: 단순 benchmark 점수 개선, 작은 module 추가 수준의 incremental engineering,
  단순 scale-up, 특정 dataset fine-tuning 위주의 기여
- 가점: 새로운 problem formulation, 새로운 representation, 새로운 learning/inference paradigm,
  일반화 가능한 이론·도구, 강한 실험적 증거

## 주의
- 논문에 학회 accept/oral/highlight 정보가 있어도 점수가 그 사실에 끌려가지 않게 독립 평가.
- **학회를 추측해서 쓰지 않음.** 학회 표시는 `venue_detect.py`가 comments·PDF 문구·LaTeX 양식으로
  판정해 따로 붙임. 리뷰 글에 "CoRL에 맞음" 같은 문장을 넣지 않음.
- 수치는 제공된 텍스트에서 확인된 것만 쓰고, 확인 불가하면 "본문에서 확인 불가"로 표시.
- 저자의 주장(claim)과 실제 실험 결과를 구분.

## 읽을 자료 (정밀 리뷰)

1. `$WD/texts/<id>.txt`: 원문 텍스트. 사실·수치의 정본임.
2. `$WD/alphaxiv/<id>.md` (있을 때만): alphaXiv가 만든 영어 요약 글과 그 글이 고른 그림·영상 캡션.
   - 무엇을 결정적 비교로 고를지, 어떤 순서로 설명할지 참고함.
   - 문장을 번역해 옮기지 않음. 우리 칸 구성과 문체로 새로 씀.
   - 수치는 원문 텍스트에서 다시 확인된 것만 씀. 어긋나면 원문을 따름.
3. `$WD/figs/<id>.png` (있을 때만): 카드에 실릴 대표 그림. **Read 도구로 직접 보고** figure_caption을 씀.
   그림에 실제로 보이는 것만 씀. 개념도면 "측정 결과가 아니라 방법 구조를 그린 그림"임을 밝힘.

## 문체 (모든 한국어 텍스트 칸 공통)

김누리의 글쓰기 규칙을 따른다. 정본은 nurilab-vault의 `03.System/Feedback Rules.md`(글쓰기·문체 절)이다.
판정 기준 하나: **이 논문을 안 읽은 로봇 학습 대학원생이 카드 하나를 2분 안에 읽고,
이 논문이 무엇을 했는지 남에게 설명할 수 있어야 한다.** 못 하면 실패다.

글의 짜임 (alphaXiv 요약 글에서 가져온 방식)
- 순서는 문제 → 방법 → 결과 → 한계. 한 칸에는 그 칸의 내용만 씀.
  headline에 쓴 문장을 다른 칸에서 되풀이하지 않음.
- problem·method는 **문단**으로 씀. 불릿을 쓰지 않음. 앞 문장이 뒤 문장의 전제가 되게 이어 씀.
- results는 **결정적 비교 2~4개**만 고름. 주장을 가장 직접 보여 주는 비교, 가장 강한 baseline과의 비교,
  실로봇 결과 순서로 고름. 나머지 표 숫자는 버림.
- 수치는 「무엇을 잰 값인지 → 이 방법 값 → 비교 대상 값 → 조건」 순서로 씀.
  예: "8개 과제 평균 성공률이 10.4%에서 74.9%로 오름." `+11.1pt`·`%p` 같은 약식 대신 "11.1퍼센트포인트".
- 논문이 새로 만든 이름(D2R, FDM 등)은 처음 쓸 때 무엇인지 풀어 씀.
  처음 나오는 benchmark는 무엇을 시키는지 괄호로 한 번 적음 (LIBERO-90: 시뮬레이션 조작 과제 90개 모음).
- 저자가 주장한 것과 실험으로 보인 것을 가름. 실험 범위(시뮬레이션만인지, 실로봇 과제 몇 개인지,
  코드 공개 여부)는 results나 limits에 적음.

문장
- 두괄식. 각 칸의 첫 문장이 그 칸의 결론임.
- 한 문장 = 한 내용. 150자를 넘는 문장은 쪼갬. 방법 설명과 수치 비교를 한 문장에 같이 넣지 않음.
- 모든 문장은 음슴체로 끝냄 (~함 / ~임 / ~됨 / ~보임). `~다`, `~습니다` 금지.
  `~음`은 문장 끝에만 쓰고, 문장 안의 주어·목적어·조사는 다 씀.
- 기술 용어는 영어 그대로 (VLA, world model, imitation learning, rollout, reward).
  널리 쓰이지 않는 약어는 첫 등장에서 한 줄로 정의함.
- 조어·비유 금지. 원래 그 뜻이 아닌 말에 새 뜻을 붙이지 않음 (`천장`, `축이 닫힌다`, `무너졌다`).
  수치는 오름·내림·유지로 씀. 뜻이 갈리는 한자어(계기, 단서 등)도 쓰지 않음.
- AI 티 나는 문체 금지: 정형화된 도입부("본 논문은 ~를 제안함"으로 칸마다 시작), 과장된 형용사
  (획기적, 혁신적, 핵심적인 역할), 끝맺음 상투구("~라는 점에서 의의가 있음", "~를 시사함" 남발).
- 줄표(—)와 원문자(①②③) 금지. 이어 쓸 때는 문장을 끊거나 콜론(:)을 씀.
- 금지어·문체는 `python agent_pipeline.py check`가 기계로 검사함. 0건이 될 때까지 고침.

## 스크리닝 결과 스키마 (screen_results/batch_XXX.json, JSON 배열)
```json
[
  {
    "id": "<arxiv_id 그대로>",
    "score": 0-100 정수,
    "robotics_relevance": 0-10 정수,
    "field": "VLA | Manipulation | World Model | Embodied AI | 3D Vision | Navigation | RL | Video | Multimodal | CV | NLP | LG 등",
    "reason": "한 줄 평가 근거 (한국어, 음슴체)"
  }
]
```

## 정밀 리뷰 스키마 (deep/<arxiv_id>.json, JSON 객체)
```json
{
  "score": 0-100 정수 (종합 평가),
  "field": "분야",
  "headline": "1~2문장. 무엇을 해서 무엇이 좋아졌는지. 핵심 수치 하나를 넣음",
  "problem": "문단 2~4문장. 기존 방법으로 무엇이 안 됐고 왜 중요한지",
  "method": "문단 3~6문장. 방법이 어떻게 동작하는지 순서대로. 입력과 출력이 무엇인지 적음",
  "results": "'- ' 불릿 2~4개. 결정적 비교만. 불릿마다 무엇을 잰 값인지 + 수치 + 조건",
  "limits": "1~3문장. 실험 범위의 한계, 저자가 보이지 않은 것, 방법이 기대는 가정",
  "lab_relevance": "'- ' 불릿 1~2개. 누리랩 주제(VLA, failure detection/recovery, test-time optimization, world model, counterfactual reasoning, robot memory, manipulation, active perception, object-centric 3DGS, scene graph)와 구체적으로 어떻게 이어지는지. 연결이 약하면 '직접 연결 약함'이라고 한 줄만",
  "figure_caption": "1~2문장. figs/<id>.png 를 직접 보고 그림이 무엇을 보여 주는지. 그림 파일이 없으면 빈 문자열",
  "video_caption": "1문장. alphaxiv/<id>.md 에 영상이 있을 때만. alphaXiv 캡션을 보고 무엇을 찍은 영상인지. 없으면 빈 문자열",
  "links": {
    "project": "원문 텍스트·comments에 그대로 적힌 프로젝트 페이지 주소, 없으면 \"\"",
    "code": "코드 저장소 주소 (github 등), 없으면 \"\"",
    "video": "영상 주소 (YouTube 등), 없으면 \"\""
  }
}
```
- links는 텍스트에 주소가 그대로 있을 때만 넣음. 주소를 추측해서 만들지 않음.
  (arXiv comments의 `this https URL`은 주소가 가려진 것이라 쓰지 않음. 본문 1쪽·각주에서 찾음.)

## 견본 (2610.13816 Dream to Remember)

```json
{
  "score": 80,
  "field": "World Model",
  "headline": "로봇 policy에 새 과제를 차례로 가르칠 때 예전 과제를 잊는 문제를, world model이 예전 과제 장면을 상상으로 다시 만들어 복습시키는 방식으로 줄임. LIBERO-90 새 과제 8개의 평균 성공률을 10.4%에서 74.9%로 올리면서 원래 잘하던 과제 성능도 유지함.",
  "problem": "π0 같은 generalist robot policy는 demonstration을 따라 배우므로 demonstration에 없던 과제는 잘 못함. RL로 보완하는 방법은 policy 가중치를 직접 fine-tuning하거나, policy는 그대로 두고 입력 noise만 바꾸는 작은 steering module을 학습하는 것임. 과제가 하나씩 차례로 들어오면 두 방법 모두 새 과제를 배우는 동안 예전 과제 성능이 낮아짐(catastrophic forgetting).",
  "method": "D2R(Dream to Remember)은 policy를 고정하고 steering module만 학습함. steering module은 policy에 넣을 noise를 고르고, 실제 행동은 고정된 policy가 만듦. 새 과제를 배우는 동안 고정된 world model이 예전 과제의 첫 관측에서 출발해 장면을 상상으로 이어 만듦(imagined rollout). 이 상상 장면에서 지금 steering의 출력이 예전 steering의 출력과 달라지면 KL penalty를 줌. 그래서 예전 과제는 첫 관측만 저장하면 되고 궤적 전체나 reward는 저장하지 않음. world model이 충분히 정확하면 새 과제도 상상 속에서 배우고, 부정확하면 새 과제는 실제 환경에서 배우고 world model은 복습에만 씀.",
  "results": "- LIBERO-90(시뮬레이션 조작 과제 90개 모음)에서 처음 보는 과제 8개를 차례로 배움. 8개 과제 평균 성공률이 고정된 π0의 10.4%에서 74.9%로 오름. π0가 이미 fine-tuning된 LIBERO suite 4개의 성능은 시작보다 1.6퍼센트포인트 높게 끝남.\n- 복습 없이 noise만 바꾸는 기존 방법 DSRL은 같은 조건에서 새 과제 평균 16.9%에 그치고, 기존 suite 4개에서 30.8퍼센트포인트를 잃음.\n- 예전 궤적을 저장해 두고 복습하는 DSRL + replay KL과 성공률은 비슷함(73.9% 대 74.9%). 저장하는 양은 약 59,000 frame 대 약 400 frame임.\n- 실제 Franka 로봇에서 과제 3개(서랍 열기, 슬라이더 옮기기, LED 켜기)를 차례로 상상 속에서만 배움. 과제당 20회 평가에서 base policy보다 평균 30퍼센트포인트 높은 성공률을 유지함. 복습 없는 DSRL은 15퍼센트포인트임.",
  "limits": "예전 과제마다 첫 관측은 저장해야 하고, 복습할 때마다 world model 계산이 듦. LIBERO 실험에 쓴 world model(A2World)은 새 과제 학습용으로는 부정확했음. 같은 behavior cloning에서 실제 demonstration으로 배우면 74.9%, world model이 다시 만든 장면으로 배우면 19.6%임. 실로봇 실험은 과제 3개뿐임.",
  "lab_relevance": "- world model을 policy 학습이 아니라 예전 행동을 기억해 두는 용도로 쓴 사례임. robot memory와 continual VLA adaptation 연구에서 비교 대상으로 쓸 수 있음.\n- 부정확한 world model도 복습용으로는 쓸 수 있다는 결과는, failure detection처럼 world model 정확도가 덜 중요한 쓰임새를 찾을 때 근거가 됨.",
  "figure_caption": "(그림 파일을 직접 보고 씀)",
  "video_caption": "저자가 올린 실제 Franka 로봇의 서랍 열기 시연 영상임.",
  "links": {"project": "https://d2r.cs.uni-freiburg.de", "code": "", "video": ""}
}
```

## 종합(synthesis.md) 형식
정확히 아래 세 개의 `## ` 헤딩. 논문 언급 시 [제목 일부](https://arxiv.org/abs/<id>) 링크. 문체 규칙은 위와 같음.
- `## 오늘의 흐름`: 불릿 3~5개. 각 `**흐름 이름**: 1~2문장`. 어느 논문들이 그 흐름인지 링크로 붙임.
- `## 해볼 만한 연구`: 2~3개. 각 `### 제목` 아래 불릿 3개:
  `질문:` 무엇을 밝히려는지 / `첫 실험:` 무엇으로 무엇을 비교하는지 / `가장 가까운 연구:` 오늘 논문 중 어느 것과 무엇이 다른지
- `## 꼭 읽을 논문`: 3~5편. `- [제목](링크): 한 줄 이유`
