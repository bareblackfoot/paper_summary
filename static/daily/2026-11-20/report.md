# 오늘의 arXiv Top 15: 2026-11-20 (금)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**

**신규 논문 수: 전체 547편 → 중복 제거 후 547편 (이번 평가 대상 547편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 176 |
| cs.LG | 119 |
| cs.RO | 79 |
| cs.CL | 64 |
| cs.AI | 109 |

---

## Top 15

### 1. CoachSI: Self-Improvement of Robot Policies with a Language Coach (76점)

[arXiv](https://arxiv.org/abs/2611.25529) · [PDF](https://arxiv.org/pdf/2611.25529) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25529) · [프로젝트 페이지](https://tlxhlll.github.io/CoachSI/)

- **저자**: Jiachen Tao, Gengyu Zhang, Haoxuan Wang, Bing Liu, Yan Yan
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 74점
- **읽은 원문**: PDF 전문

> 장기 과제 중간에 멈춘 robot policy에 고정된 VLM coach가 다음 단계 지시문을 골라 주고, 성공한 rollout은 지시문만 원래 과제 지시문으로 바꿔 fine-tuning함. RoboCasa365 장기 과제 18개에서 coach 없이 낸 성공률이 47.4%에서 56.8%(영상 coach)와 59.3%(simulator 상태 coach)로 오름.

**무슨 문제인가**

generalist robot policy는 단일 skill은 잘 수행하지만 skill 여러 개를 이어야 하는 장기 과제에서는 실패가 많음. policy 혼자 모은 성공 rollout으로 다시 학습하면 이미 할 수 있는 행동만 반복해서 배우게 됨. 이를 넘으려면 사람 operator의 교정 행동, 별도로 학습한 reward·value model, 또는 배포 때마다 붙어 있는 상위 VLM planner가 필요했음. 저자는 실패 rollout을 분석해, 로봇이 이미 올바른 물체 앞에 있고 skill도 갖췄는데 다음 동작을 시작하지 않고 멈추는 경우가 많다고 보고함.

**어떻게 푸나**

CoachSI는 고정된 VLM(Qwen3.8-27B)을 language coach로 쓰는 self-improvement 방법임. 과제마다 policy의 단일 skill 지시문 형식으로 쓴 다음 단계 후보 목록이 미리 주어짐. coach는 action chunk(32 step)가 끝날 때마다 과제 지시문, 후보 목록, policy와 같은 카메라 영상 3개를 받음. 영상 대신 simulator 상태를 읽는 coach 변형도 비교용으로 씀. coach는 아직 끝나지 않은 첫 단계를 고르거나, 모든 단계가 끝났으면 원래 지시문을 유지함. coach는 행동을 내지 않으므로 rollout의 모든 행동은 고정된 policy가 만듦. 성공한 rollout은 관측과 행동을 그대로 두고 지시문만 원래 과제 지시문으로 바꿈(hindsight relabeling). 이 데이터를 사람 demonstration과 섞어 World Action Model(WAM: 미래 영상을 예측하는 video backbone과 이를 참조해 행동을 내는 action backbone으로 된 policy)을 fine-tuning함. 이때 video backbone의 self-attention 층만 video loss로 학습하고 action backbone은 고정함. 배포 때는 coach 없이 과제 지시문만 줌.

**결과**

- 실험은 모두 RoboCasa365(주방 장면의 단일 skill 과제와 이를 이은 복합 과제를 담은 시뮬레이션 benchmark)에서 함. WAM(OpenWAM)과 VLA(Xiaomi-Robotics-1)가 멈춘 상태 500개(과제 15개)에서, simulator 판정으로 고른 정답 다음 단계 지시문을 policy에 줌. 320 step 안에 다음 subgoal을 끝내는 비율이 과제 지시문 대비 4.6배(10.5퍼센트포인트) 오름. 같은 과제 지시문을 바꿔 말하기만 하면 1.3퍼센트포인트로 유의하지 않음.
- 카메라 영상만 보는 VLM coach는 상태 261개에서 정답 지시문이 낸 향상의 91%를 냄.
- 장기 과제 18개, 처음 보는 장면 20개, 총 1,080 episode에서 coach 없이 평가함. fine-tuning 데이터에서 과제 데이터가 차지하는 비율을 같게 맞췄을 때 성공률은 pretrained 47.4%, 사람 demonstration 추가 49.4%, policy 자체 성공 rollout 51.9%임. CoachSI는 simulator 상태를 읽는 coach로 59.3%, 영상만 보는 coach로 56.8%임.
- coach를 배포 때도 붙여 두는 계층형 방식은 41.9%로 pretrained보다 5.5퍼센트포인트 낮음. hindsight relabeling을 빼면 성공률이 59.3%에서 51.7%로 내림.

**한계**

실험은 RoboCasa365 시뮬레이션뿐이고 실로봇 실험이 없으며, 본문에 코드 주소가 없음. fine-tuning은 WAM 하나에서 한 번만 했고, VLA는 멈춘 상태 분석에만 쓰임. 과제별 다음 단계 후보 목록을 사람이 미리 써 주므로, 과제 분해를 coach가 스스로 하는 경우는 보이지 않았음.

**누리랩 연구와의 연결**

- 멈춘 상태를 찾아 다음 단계 지시문으로 되살리는 과정은 failure detection·recovery를 language feedback 기반 학습으로 바꾸는 사례임. VLA의 장기 과제 실패 분석과 복구 연구에서 비교 대상으로 쓸 수 있음.
- action backbone을 고정하고 video backbone만 고쳐 성공률을 올린 결과는, world model의 미래 예측을 바꿔 행동을 바꾸는 test-time steering 연구와 이어 볼 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 개념도임. (a)는 고정된 VLM coach가 후보 지시문 중 다음 단계를 골라 고정된 policy에 주는 수집 단계임. (b)는 지시문을 과제 지시문으로 바꿔 video backbone만 학습하는 단계, (c)는 처음 보는 장면에서 coach 없이 배포하는 단계이고, 각 단계를 action chunk 단위 막대로 보여 줌.*

---

### 2. MAWAM: A Multi-Agent World-Action Model for Coordinated Manipulation (76점)

[arXiv](https://arxiv.org/abs/2611.25105) · [PDF](https://arxiv.org/pdf/2611.25105) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25105) (요약 있음) · [프로젝트 페이지](https://research-staging.nvidia.com/labs/lpr/mawam)

- **저자**: Xianzhe Fan, Chi-Pin Huang, Fu-En Yang, Jing Wang, Yecheng Wu, Yu-Cheng Chou, Johan Bjorck, Linxi "Jim" Fan 외 5명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 73점
- **읽은 원문**: PDF 전문

> 로봇 여러 대의 action chunk와 각 로봇 카메라의 미래 장면을 한 번의 생성으로 함께 만드는 multi-agent world-action model을 제안함. 실제 로봇 2대의 협업 과제 3개에서 평균 성공률 67.8%로, 같은 데이터로 학습한 multi-agent VLA baseline(MA-VLA)보다 18.9퍼센트포인트 높음.

**무슨 문제인가**

협업 조작에서는 한 로봇의 행동이 공유 환경을 바꾸고, 그 변화가 다른 로봇이 다음에 할 수 있는 일을 정함. 로봇마다 policy를 따로 두는 decentralized 방식은 강하게 맞물린 과제에서 서로 기다리거나 동작이 엇갈릴 수 있음. 여러 로봇의 궤적이나 행동을 함께 생성하는 방법과 LLM·temporal logic으로 역할을 나누는 방법은 공동 행동이 만들 시각적 결과를 예측하지 않음. 반대로 multi-agent video world model은 행동을 조건으로만 받으므로 바로 실행할 수 있는 행동을 내지 못함.

**어떻게 푸나**

MAWAM은 단일 로봇용 world-action model인 GR00T 2를 출발점으로, 모든 로봇의 action token과 미래 장면 token을 하나의 Transformer에서 flow matching으로 함께 denoising함. 입력은 각 로봇의 private camera 영상, state, task role이고, 출력은 로봇별 24 step action chunk와 각 private view의 미래 frame 8장임. 로봇마다 view·state·action을 하나의 stream으로 묶고, 모든 stream 사이에 dense cross-agent attention을 둠. 어느 view가 어느 로봇 것인지는 video RoPE에 agent 축을 추가하고, regular simplex 꼭짓점 좌표를 identity code로 넣어 구분함. 로봇이 맡은 일은 별도의 role embedding으로 주므로, 두 로봇이 같은 role을 가져도 state와 action은 따로 유지됨. 학습은 로봇 한 대씩 데이터로 카메라와 controller에 맞추는 warm-up 뒤, 동기화된 팀 demonstration으로 identity를 무작위 배정하며 team training을 함. 실행 때는 24 step 중 앞 8 step을 모든 로봇이 동시에 실행하고 새 관측으로 다시 생성함.

**결과**

- 실로봇(Galaxea R1 Pro 2대, 로봇당 카메라 3대, 공유 전역 카메라 없음) 과제 3개를 과제당 30회 평가함. 평균 성공률은 MAWAM 67.8%, π0.5로 다시 구현한 MA-VLA 48.9%, CLS-DP 37.8%, GauDP 28.9%임. 세탁 가방에 옷 넣기 과제에서 차이가 가장 커서 53.3% 대 30.0%임.
- RoboFactory(팔 2~4개가 협업하는 시뮬레이션 조작 과제 8개 모음)에서 과제당 100회 평균 성공률이 90.3%임. MA-VLA 논문 보고값 83.4%보다 높지만, baseline 수치는 각 논문 보고값임. Long Pipeline Delivery에서는 95.0%로 MA-VLA 97.0%보다 낮음.
- cross-agent attention을 빼면 팔 4개가 신발을 차례로 넘기는 Long Pipeline Delivery 성공률이 95.0%에서 39.0%로 내려감. 실로봇 평균도 67.8%에서 52.2%로 내려감.
- team training에서 미래 영상 loss만 빼면 RoboFactory의 Place Food 과제 성공률이 78.0%에서 47.0%로 내려감. 테스트 때 미래 장면 token을 denoising하지 않고 남겨 두면 성공률은 비슷하지만, token 자체를 빼면 Long Pipeline Delivery가 0.0%가 됨.

**한계**

실험은 팔 4개 이하의 고정된 팀이고, 이종 로봇이나 실행 중 팀 구성 변화는 다루지 않았다고 저자가 밝힘. 실로봇 결과는 같은 기종 로봇 2대, 과제 3개, 과제당 30회이며 표준오차가 5퍼센트포인트 안팎임. 미래 장면을 끝까지 생성하지 않아도 성공률이 비슷하므로, 성능 향상이 장면 예측 자체에서 오는지 학습 신호로서의 효과인지는 가려지지 않음. 본문에 코드 주소는 없음.

**누리랩 연구와의 연결**

- world-action model을 multi-robot manipulation으로 넓힌 사례라, world model 기반 VLA 연구에서 여러 팔·여러 로봇 설정의 비교 대상으로 쓸 수 있음.
- 로봇별 미래 장면 예측이 행동과 함께 나오므로, 예측과 관측의 차이로 협업 실패를 감지하는 failure detection 연구에 바로 붙여 볼 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. team training에서 로봇별 stream(identity, state, role, action, future view)이 cross-agent attention을 거쳐 video head와 action head로 함께 학습되는 구조를 보여 줌. 아래쪽은 24 step 중 앞 8 step을 함께 실행하고 다시 생성하는 추론 과정을 그림.*

---

### 3. Learning What Actions Change: Action Effect Matching for Dynamics-Faithful World Models (76점)

[arXiv](https://arxiv.org/abs/2611.25980) · [PDF](https://arxiv.org/pdf/2611.25980) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25980) (요약 있음)

- **저자**: John Won, Yonghoon Dong, Jinwoo Shin
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 72점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> 행동을 조금 바꿨을 때 영상이 어떻게 달라지는지를 world model이 실제와 같게 따라가도록 하는 보조 loss AFFECT를 제안함. DROID(대규모 로봇 조작 데이터셋)가 제안한 Franka 하드웨어 구성의 실로봇에서 world model 속 policy 성공률과 실제 성공률의 Pearson 상관이 0.468에서 0.790으로 오름.

**무슨 문제인가**

video diffusion 기반 robot world model은 그럴듯한 영상을 만들지만, 행동이 조금 달라질 때 결과가 달라지는 것은 잘 반영하지 못함. 같은 장면에서 접근 경로가 약간만 달라져도 물체를 잡거나 놓치거나 밀어내는 결과가 갈리는데, 모델은 이 차이를 무시한 비슷한 영상을 내는 경향이 있음. 이런 모델은 policy 평가에서 실제 성공률과 다른 점수를 주고, planning에서 잘못된 행동을 고르게 함. 기존 보완책은 같은 초기 상태에서 반복 실행한 counterfactual rollout이나 결과 label·reward가 필요해서 실로봇에서 규모를 키우기 어려움.

**어떻게 푸나**

먼저 사람이 과제 없이 자유롭게 물체를 다룬 teleoperation(play data)으로 play policy를 학습하고, 이 policy를 자율로 돌리며 action chunk마다 시간 상관이 있는 noise를 더해 실행함(perturbation play). 이때 더한 noise를 기록하고, world model 입력은 현재 관측과 실행된 action뿐이며 noise는 loss 계산에만 씀. AFFECT는 고정된 두 encoder로 noise 특징(합, 제곱합 등)과 영상 latent 특징(채널 평균 변화 등)을 뽑음. noise 특징에서 기대값을 빼서 중심화한 뒤 영상 특징과 곱하면, 같은 장면 안에서 영상이 noise를 따라 얼마나 움직이는지를 재는 공분산이 됨. 실제 영상의 이 공분산과 생성 영상의 공분산이 같아지도록 차이의 제곱합을 flow loss에 더함. 생성 영상은 실제 미래를 보지 않고 Gaussian noise에서 짧은 미분 가능한 Euler sampler로 만듦. 계산 비용 때문에 AFFECT loss는 8 iteration마다 한 번만 더함. 저자는 이 loss가 유한 특징 MMD(maximum mean discrepancy)와 같고, 장면에만 달린 오차는 상쇄됨을 증명함.

**결과**

- 두 action 조건 rectified-flow video world model DreamDojo와 Cosmos3에 AFFECT를 붙여 비교함. 실제 Franka(DROID 구성)에서 DreamDojo backbone의 Pearson 상관이 0.468에서 0.790으로, Cosmos3는 0.425에서 0.583으로 오름. FVD(Fréchet Video Distance: 생성 영상과 실제 영상의 분포 차이, 낮을수록 좋음)는 각각 807에서 622로, 910에서 744로 내림.
- 실제 ALOHA-2에서 Cosmos3의 상관이 0.298에서 0.694로, DreamDojo는 0.325에서 0.490으로 오름. 다만 DreamDojo의 FVD는 183에서 188로 조금 오름.
- DreamDojo로 후보 action chunk를 상상해 고르는 planning에서 UR5e 시뮬레이션 pick-and-place 과제 5개 평균 성공률이 60.0%에서 68.3%로 오름. 무작위 선택은 46.7%임. ALOHA-2 실로봇 장기 과제 1개(subtask 3개)에서는 평균 72.2%에서 80.6%로 오름.
- Cosmos3를 perturbation play data로 1만 iteration만 학습한 ablation에서 AFFECT 없이 학습한 FVD는 284임(embodiment는 본문에 명시되지 않음). noise 특징을 episode 사이에서 섞은 placebo matching은 FVD를 460으로, noise 없이 영상 특징 평균만 맞춘 matching은 451로 올림. AFFECT는 256으로 내림.

**한계**

상관 평가는 embodiment마다 2개 과제, checkpoint 4개, 12 episode 규모이고 성공 여부는 사람이 영상을 보고 매김. planning 실로봇 실험은 ALOHA-2 장기 과제 1개이고 시행 횟수는 본문에서 확인 불가하며, ablation은 영상 지표만 보고함. loss는 손으로 정한 특징이 잡는 반응만 제약하고 장면에만 달린 오차는 고치지 못함(저자 명시). 본문에 코드 주소가 없음.

**누리랩 연구와의 연결**

- world model을 policy 평가기나 test-time planning에 쓸 때 행동 차이를 반영하는지가 병목이라는 점을 수치로 보임. 누리랩 world model 기반 VLA 평가·planning 연구에서 학습 loss로 바로 붙여 볼 수 있음.
- 반복 실행 없이 기록된 noise만으로 행동 효과를 감독하는 방식은 counterfactual reasoning과 failure detection(잡기 실패·밀어내기 예측) 연구의 학습 신호로 이어 볼 수 있음.

*대표 그림: 측정 결과가 아니라 문제 설정을 그린 개념도임. 시뮬레이션 UR5e가 같은 초기 상태에서 좁은 action 분포의 작은 차이로 빨간 cube를 잡거나 놓치거나 밀어내는 세 결과로 갈리는 모습을 보여 줌.*

---

### 4. Search or Scoring? Diagnosing Why Visual World-Model Planners Fail (75점)

[arXiv](https://arxiv.org/abs/2611.25347) · [PDF](https://arxiv.org/pdf/2611.25347) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25347)

- **저자**: Haoxuan Jia, Yang Liu, Shang Luo, Chenhao Wu, Zixiang Ni, Yingguang Yang, Feng Zhang, Chongyang Zhang 외 5명
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 74점
- **읽은 원문**: PDF 전문

> visual world model planner의 실패를 optimizer가 좋은 행동을 시도하지 못한 경우(search failure)와 cost가 나쁜 행동을 고른 경우(scoring failure)로 가르는 진단법을 만듦. 진단에 맞춰 Metaworld 새 과제 168개에서 검색한 demonstration 행동 window 30개의 평균을 model 없이 실행하면 127개를 풂. world model로 고르면 최대 92개임.

**무슨 문제인가**

DINO-WM, JEPA-WM 같은 visual world model은 고정된 DINOv2 feature 공간에서 action의 결과를 예측함. CEM(cross-entropy method)은 예측 결과와 goal image의 거리(cost)가 가장 작은 action sequence를 찾음. 계획이 실패하는 원인은 optimizer가 cost가 선호할 행동을 한 번도 시도하지 않은 경우와, 예측 위에서 계산한 cost가 나쁜 행동을 1등으로 매긴 경우로 나뉨. 앞의 경우는 search를 늘려야 하고 뒤의 경우는 model을 고쳐야 하지만, planner는 어느 쪽이 일어났는지 기록하지 않음. 그래서 원인을 확인하지 않은 채 search를 늘리거나 encoder·predictor를 바꾸는 대응이 쓰여 왔음.

**어떻게 푸나**

진단은 CEM이 평가한 후보를 simulator에서 실제로 실행하고, 과제를 만든 expert action(known solution)을 planner 자신의 cost로 채점함. 같은 cost를 예측 결과와 실제 도달 frame에 각각 적용한 값도 비교함. known solution의 cost가 CEM 후보 전부보다 낮으면 search failure, 아니면 scoring failure로 표시함. 저자는 cost를 실제 cost와 예측 오차의 합으로 놓고, 오차가 작으면 search failure가, 크면 scoring failure가 나온다는 명제를 고정 후보 집합 가정 아래 증명함. 진단을 시험하는 DemoProp은 현재·goal proprioception을 key로 demonstration의 action window를 검색함. 검색한 window는 search failure가 많은 설정(search regime)과 scoring failure가 많은 설정(scoring regime)에서 다르게 씀. search regime에서는 가까운 window 100개를 CEM 첫 population에 넣는 warm start를 씀. scoring regime에서는 가장 가까운 window 30개의 평균을 model 없이 실행하는 Average를 씀. 어느 쪽도 학습이나 reward를 쓰지 않음.

**결과**

- known solution 채점에서 PushT(2-D 평면에서 T자 블록 밀기) 공식 평가 episode 중 full success에 실패한 경우에서 search failure는 DINO-WM 29/34, JEPA-WM 23/28임. Metaworld(3-D 조작 benchmark)에서 30 step 구간을 떼어 만든 window 과제에서는 0/67, 0/85로 모두 scoring failure임. Metaworld에서 cost의 성공·실패 구분 AUROC는 실제 도달 frame에서 0.94, 예측 frame에서 0.54임.
- 검색한 window를 CEM 후보에 더하는 warm start(논문 이름 Expand)는 PushT 96 episode의 full success를 DINO-WM에서 62에서 78로, JEPA-WM에서 68에서 82로 올리고 CEM의 성공을 하나도 잃지 않음. 반대로 population을 4배 늘린 CEM은 Metaworld DINO-WM에서 full success가 45에서 43으로 내림.
- Metaworld 새 과제 168개에서 같은 window 30개를 쓸 때 Average는 127개를 풂. 같은 window로 warm start한 CEM은 92개와 89개, model이 고른 window(Restrict)는 84개와 87개임(DINO-WM, JEPA-WM 순).
- PushT에서 predictor만 6·5·4·3 bit로 quantize하자 실패가 scoring 쪽으로 옮겨가고 더 나은 사용법도 바뀜. 진단 결과에 따라 warm start와 Average 중 하나를 고르도록 미리 고정한 규칙은 새 episode 960개 중 678개를 풀고, 항상 warm start는 517개, 항상 Average는 530개임.

**한계**

모든 실험이 시뮬레이션이고 실로봇 실험은 없으며, search regime은 PushT와 Wall이라는 단순한 2-D 과제에만 근거함. 진단에는 과제마다 known solution이 필요하고, Metaworld는 공식 long-horizon protocol이 아닌 30-step window 과제로만 시험함. 저자도 성공률을 비교해 사용법을 고르면 같은 결과가 나온다고 밝혀, 진단은 선택을 개선하기보다 이유를 설명하는 데 그침. Metaworld에서는 같은 demonstration으로 학습한 BC policy가 128개로 Average와 비슷하고, 본문에 코드 공개 주소는 없음.

**누리랩 연구와의 연결**

- world model 기반 test-time planning이 실패할 때 원인을 실패 하나 단위로 가르는 측정 절차임. failure detection·diagnosis 연구에서 known solution 채점과 예측·실제 cost 비교를 그대로 가져다 쓸 수 있음.
- 예측 오차가 크면 후보를 늘릴수록 model이 과대평가한 행동을 고른다는 결과는, VLA proposal을 world model로 재순위하는 방식을 설계할 때 확인해야 할 조건임.

*대표 그림: CEM이 실패한 경우마다 known solution의 cost를 CEM 최선 후보의 cost로 나눈 비율을 log 축에 점으로 찍은 측정 결과 그림임. PushT와 Wall의 점은 대부분 1 아래(search failure, 예: DINO official 29/34)에 있고, Metaworld와 RoboCasa의 점은 모두 1 이상(scoring failure, 0/67 등)에 있음.*

---

### 5. ActMem: From Latent Memory Reasoning to Grounded Robotic Action (74점)

[arXiv](https://arxiv.org/abs/2611.25461) · [PDF](https://arxiv.org/pdf/2611.25461) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25461) (요약 있음) · [코드](https://github.com/LigphiDonk/ActMem)

- **저자**: Linfeng Dong, Jianwei Niu, Jiuyi Zhao, Ruibing Feng, Xinghao Wu, Wu Yang, Shuai Tao, Wulong Liu 외 1명
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 74점
- **읽은 원문**: PDF 전문

> 기억이 필요한 조작 과제에서, VLM이 과거 영상을 보고 현재 subtask를 추론할 때 생긴 hidden state를 action expert의 조건으로 넘기고 현재 화면은 별도 cross-attention으로 읽게 함. RoboMemArena 26개 과제의 task success가 71.1%로, 가장 강한 baseline SimpleMemVLA보다 7.5퍼센트포인트 높음.

**무슨 문제인가**

VLA 대부분은 현재 frame만 보고 행동하므로, 컵 밑에 숨긴 블록이나 이미 열어 본 서랍처럼 화면에 남지 않은 사건을 다루지 못함. 휴지를 몇 장 뽑았는지처럼 어느 한 frame에도 보이지 않고 frame 사이 관계에서만 추론되는 정보도 있음. 기존 memory bank·retrieval 방식(MemoryVLA, MemER)은 과거 관측을 저장해 넘기지만, 그 관측이 지금 무엇을 뜻하는지는 action module이 알아내야 함. native-video 방식(SimpleMemVLA)은 VLM 안에서 과거 영상을 추론하지만, 같은 context에 현재 화면도 들어 있어 기록이 길어질수록 현재 화면의 세부 정보가 action에 덜 전달된다고 저자가 지적함.

**어떻게 푸나**

ActMem은 공개 VLA 코드베이스 starVLA 위에 Qwen3-VL-4B backbone과 16층 flow-matching DiT action expert를 붙인 구조임. 입력은 timestamp가 붙은 앞 카메라 과거 영상(RoboMemArena에서 1 fps, 최대 126초), 현재 wrist 카메라 이미지, 언어 지시임. backbone은 이를 한 context로 읽고 현재 subtask 문구(예: lift the cup)를 autoregressive하게 생성함. 생성된 subtask token의 마지막 층 hidden state와 token embedding을 Latent Memory CoT(기억 추론 결과를 담은 잠재 상태, 이하 Memory CoT)라 부름. action expert는 과거 frame token 대신 이것만 조건으로 받음. Perception Attention은 DiT의 3, 7, 11, 15층에 넣은 zero-init gated cross-attention으로, 현재 화면 token의 backbone 출력을 읽음. 학습은 subtask 문구 cross-entropy와 flow matching loss를 함께 쓰고, 출력은 16 step action chunk 중 10 step을 실행한 뒤 다시 추론함. 추론 때는 과거 부분의 KV cache를 재사용하고 직전 subtask를 초안으로 넣어 한 번의 병렬 pass로 검증하므로(speculative decoding 검증 규칙) 출력은 같고 계산만 줄어든다고 저자가 밝힘.

**결과**

- RoboMemArena(기억 의존 시뮬레이션 조작 과제 26개, 과제당 51회)에서 task success 71.1%, completion success 80.8%임. SimpleMemVLA는 63.6%, 72.1%이고 baseline 수치는 이전 논문 보고값임. Transferring 범주는 42.6%로 FrameSamp+Modul 63.8%보다 낮음.
- 40k iteration 학습, 과제당 10회 평가 ablation에서 task success는 full 52.3%임. subtask text embedding만 조건으로 쓰면 40.4%, action expert가 prompt token 전체를 읽으면 38.8%, Perception Attention을 빼면 47.7%, 과거를 빼면 17.7%임.
- MIKASA-Robo(화면에서 사라진 정보를 기억해야 하는 시뮬레이션 과제 5개, 과제당 100회) 평균 성공률이 73.8%로, 저자가 재현한 SimpleMemVLA 71.4%보다 2.4퍼센트포인트 높음. MIKASA-Robo 과제 중 하나인 RC-5에서는 49% 대 53%로 SimpleMemVLA보다 낮음.
- 실제 ARX LIFT2 로봇에서 과제 4개를 과제당 40회 평가함. 평균 성공률이 68.8%로 SimpleMemVLA 58.8%, MemoryVLA 55.0%, MEM-π0.5 48.8%보다 높음. 과제별로는 Cup-and-Block과 Scissor Retrieval 75%, Tissue Counting 65%, Cabinet Search 60%임.

**한계**

benchmark마다 학습 모델 1개로 평가하고 분산을 보고하지 않았으며, RoboMemArena baseline은 이전 논문 수치라 학습 조건이 같은지 본문에서 확인 불가임. 결정 1회 latency 중앙값이 0.33~0.52초로 고정 크기 memory를 쓰는 π0.5 계열 0.08~0.09초보다 느리고, 모든 과거 frame을 context에 두므로 수십 분 과제는 다루지 못한다고 저자가 밝힘. 학습에 subtask 주석이 필요하고(실로봇은 Qwen3-VL이 만든 라벨을 사람이 일부 확인함), 본문에 GitHub 주소는 있으나 코드와 checkpoint는 공개 예정으로만 적혀 있음.

**누리랩 연구와의 연결**

- robot memory를 과거 관측 저장이 아니라 subtask 추론의 hidden state로 넘기는 설계라, 기억 의존 VLA 연구에서 SimpleMemVLA와 함께 비교 대상이 됨. 같은 subtask 문구를 강제해도 첫 번째와 두 번째로 붓는 시점의 Memory CoT끼리 cosine 유사도가 0.25에 그침. 이 분석은 잠재 상태에 진행도가 담긴다는 근거로 쓸 수 있음.
- 실패가 가장 많은 Cabinet Search(이미 연 서랍 기억, 60%)는 자기 행동 이력 추적이 약하다는 결과라, subtask 추론 오류를 감지해 고치는 failure detection·recovery 연구로 이어 볼 수 있음.

*대표 그림: 측정 결과와 방법 개념을 함께 담은 그림임. 위쪽은 과거 경험과 현재 화면을 Memory CoT와 Perception Attention으로 나눠 VLA에 넣는 방법 구조를 그림. 아래쪽은 RoboMemArena task success 대 completion success 산점도(ActMem은 71.1%와 80.8%)와 범주별 성공률 radar chart를 보여 줌.*

---

### 6. WEVO: World Model-Enabled VLA Optimization for Whole-Body Loco-Manipulation (74점)

[arXiv](https://arxiv.org/abs/2611.25251) · [PDF](https://arxiv.org/pdf/2611.25251) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25251) (요약 있음) · [프로젝트 페이지](https://qianzhong-chen.github.io/wevo.github.io/)

- **저자**: Qianzhong Chen, Muyuan Lin, Yuyin Sun, Mac Schwager, Cheng-Hao Kuo, Roberto Martín-Martín
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 74점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> 휴머노이드 Unitree G1의 whole-body VLA를 teleoperation 없이 action-conditioned video world model 안에서 RL로 post-training함. 실로봇 과제 3개의 평균 성공률이 23.3%에서 75.0%로 오르고, 같은 실로봇 데이터로 직접 RL을 한 경우는 48.3%임.

**무슨 문제인가**

VLA를 RL로 개선하려면 많은 시행이 필요하지만, 휴머노이드가 실제 환경에서 탐색하면 넘어지거나 부딪힐 위험이 큼. 3DGS로 배치 장면을 다시 만든 simulator에서 RL을 하면, policy가 simulator와 실제 화면의 남은 차이를 이용해 성능이 오히려 내려갈 수 있음. 기존 video world model 기반 RL(VLAW, WMPO 등)은 고정된 팔의 탁상 조작에 머물렀고 학습에 사람의 teleoperation 데이터를 썼음. 그래서 걷기와 조작을 함께 하는 휴머노이드 VLA를 어디서 안전하게 개선할지에 대한 방법이 없었음.

**어떻게 푸나**

WEVO는 simulator와 video world model에 서로 다른 일을 맡김. 먼저 LEGS simulator(3DGS 배경과 MuJoCo 접촉을 합친 G1용 데이터 생성기)에서 과제당 합성 demonstration 200개를 만들어 GR00T N1.7 VLA를 학습함. 이 VLA를 실로봇에서 자율로 돌려 과제당 성공 10개와 실패 10개, 총 20개 궤적을 남김. world model은 DreamDojo(Cosmos 기반, 관절 상태를 조건으로 다음 egocentric frame을 만드는 2B 모델)에서 시작함. simulator에서 만든 manipulation·locomotion play data 11시간으로 mid-training하고, 과제별로 합성 demonstration과 실로봇 궤적 20개로 fine-tuning함. RL 단계에서는 VLA가 18차원 task-space 목표 chunk를 내고, whole-body controller인 SONIC WBC와 MuJoCo가 이를 43차원 관절 상태로 바꾸고, world model이 그 관절 상태로 다음 화면을 만듦. 생성된 영상은 SARM 계열 progress 모델이 진행도로 바꾸고, 그 증가분을 dense reward로 써서 DICE-RL·ReinFlow·AWR로 action head를 갱신함.

**결과**

- 실로봇 과제 3개(병 집어 상자에 넣기, 병 들고 돌아서 바닥 바구니에 넣기, 양손으로 바구니 옮기기)를 과제당 20회 평가함. world model 안의 DICE-RL 평균 성공률이 75.0%이고, 시작 BC는 23.3%, 같은 실로봇 궤적 20개로 DICE-RL을 한 Real RL은 48.3%임.
- LEGS simulator에서 직접 RL을 한 Sim RL은 성공률이 BC보다 세 과제 모두 내려가 30%, 0%, 0%가 됨. 저자는 이를 simulator와 실제 화면의 차이를 policy가 이용한 결과로 해석함.
- 같은 world model을 쓰는 기존 방법과 비교하면 평균 성공률이 VLAW 33.3%, WMPO 40.0%, DICE-RL 75.0%임. DICE-RL에서 dense reward를 종료 시점 성공 신호로 바꾸면 45.0%, 매 round 다시 rollout하지 않고 고정 buffer를 쓰면 58.3%로 내려감.
- play data mid-training을 빼면 평균 성공률이 75.0%에서 63.3%로 내려감. 같은 45,000 step 조건에서 play data로 mid-training하면 손과 물체 영역의 PSNR(iPSNR)이 세 과제 평균 1.17 dB 높음.

**한계**

실로봇 과제는 3개이고 방법·과제마다 학습을 한 번만 돌려 seed 간 편차가 없음. world model과 reward 모델을 과제마다 따로 fine-tuning하고, G1 전용 인터페이스라 다른 휴머노이드로 바로 옮길 수 없다고 저자가 밝힘. RL 한 번에 H100 8장으로 약 12시간, world model 과제별 fine-tuning에 17시간이 들고, 본문에 코드 주소는 없음.

**누리랩 연구와의 연결**

- video world model을 VLA RL 환경으로 쓸 때 dense progress reward, 매 round rollout 재수집, 실로봇 성공·실패 궤적으로 world model 맞추기가 각각 성공률에 주는 영향을 ablation으로 보임. world model 기반 VLA post-training 연구의 설계 기준으로 쓸 수 있음.
- simulator RL은 실로봇 성공률을 낮추고 world model RL은 실로봇 성공률을 올린다는 비교는, 어떤 학습 환경이 실제 배치 성능을 예측하는지 판단하는 failure 분석 연구와 이어짐.

*대표 그림: G1 휴머노이드가 실제 실험실에서 세 과제(병 집어 넣기, 병 들고 돌아서 바구니에 넣기, 양손으로 바구니 옮기기)를 하는 사진과, 과제별 성공률 막대그래프임. 막대그래프는 Base BC, Real RL, Ours를 비교하며 세 과제 모두 Ours가 가장 높게 그려져 있음.*

---

### 7. LoopedWAM: Looped World Action Models for Elastic Inference (72점)

[arXiv](https://arxiv.org/abs/2611.25595) · [PDF](https://arxiv.org/pdf/2611.25595) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25595) · [프로젝트 페이지](https://anhdao69.github.io/LoopedWAM) · [코드](https://github.com/anhdao69/LoopedWAM)

- **저자**: Anh Dao, Xinxin Liu, Hang Yu, Jeffrey A Chan Santiago, Yuzhang Shang
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> world action model의 video·action expert가 공유 block 묶음을 반복 실행하게 해 0.58B parameter로 줄이고, 한 checkpoint에서 추론 깊이와 sampling step 수를 test time에 고르게 함. LoopedWAM-E는 LIBERO 평균 성공률 96.0%를 H100에서 query당 27.6 ms에 내고, 같은 2 step의 Fast-WAM(37.1 ms)보다 1.3배 빠름.

**무슨 문제인가**

World action model(WAM)은 사전학습된 video diffusion model에서 출발해 video expert와 action expert를 함께 학습하고 로봇 행동을 내는 policy임. 지금의 WAM은 대개 2B에서 14B parameter이고, 깊은 action expert를 sampling step마다 다시 실행하므로 closed-loop 제어의 memory·latency 조건을 맞추기 어려움. 층 사이에 가중치를 공유하면 저장하는 parameter는 줄지만 같은 깊이를 실행하는 시간은 그대로임. sampling step을 줄이면 빨라지지만, 적은 step으로 학습하지 않은 policy는 행동 품질이 내려갈 수 있음.

**어떻게 푸나**

LoopedWAM은 Fast-WAM 구조를 따름. 입력은 카메라 영상, proprioception, 언어 지시이고, 출력은 action 32개로 된 action chunk임. video expert는 현재 frame을 query당 한 번 encoding해 key·value를 저장하고, action expert는 이를 읽으며 N번의 Euler step으로 chunk를 만듦. 각 expert는 Wan2.1-T2V-1.3B(30 block)에서 복사한 block 12개만 저장함: 앞 3개(prelude), 반복해 쓰는 공유 core 6개, 뒤 3개(coda)임. core를 4번 반복하면 실행 깊이가 복사 원본인 Wan2.1과 같은 30층이 됨. video loop 수 Kv와 action loop 수 Ka는 따로 정할 수 있고, late alignment 규칙으로 action의 마지막 loop가 항상 가장 깊은 video loop를 읽게 함. LoopedWAM-E는 elastic self-distillation으로 만든 단일 checkpoint임. 고정된 LoopedWAM(10 step)을 teacher로 두고, student의 action expert가 Ka 1·2·4와 N 2·5·10의 9개 조합을 번갈아 학습함. 각 step의 target은 student 자신의 중간 상태에서 출발한 teacher의 적분 결과이므로, student는 계산을 줄여 생긴 오차를 고치도록 학습됨.

**결과**

- LIBERO(시뮬레이션 조작 과제 40개, 6,000 episode)에서 LoopedWAM의 평균 성공률은 96.1%임. 저자가 같은 protocol로 재평가한 Fast-WAM(약 6B)은 96.6%, Faster-WAM(약 6.3B)은 98.7%임. 차이는 LIBERO-Long에 몰려 있음(90.1% 대 93.5%, 98.1%). RoboTwin 2.0(양팔 과제 50개)은 91.9%로 Fast-WAM 논문값 91.8%와 비슷함.
- 같은 H100 측정에서 peak GPU memory는 2.05GB로 Fast-WAM의 15.25GB보다 7.4배 작음. full depth latency는 91.8ms 대 107.5ms로 1.2배 차이뿐임. LoopedWAM-E(Ka=2, N=2)는 27.6ms에 96.0%임. Fast-WAM도 2 step에서 96.0%를 37.1ms에 내므로, step 수를 맞추면 속도 차이는 1.3배임.
- elastic 학습 없이 action loop를 1개로 줄이면 LIBERO 성공률이 12.3%로 내림(짧은 학습 schedule 기준). 같은 설정에서 LoopedWAM-E는 93.7%를 유지함. Ka=4, N=2에서는 LIBERO, RoboTwin 2.0, RoboCasa-GR1 모두 teacher와 0.5퍼센트포인트 이내임. Ka=1은 RoboCasa-GR1(humanoid 탁상 과제 24개 모음)에서 최대 9.0퍼센트포인트 내림.
- 실제 AgileX PiPER 팔에서 과제 4개를 과제당 20회 평가함. LoopedWAM과 Fast-WAM 모두 71.3%(57/80)이고, memory는 3.7GB 대 12.7GB임. LoopedWAM-E(2, 2)는 67.5%로 내리지만 latency는 160ms에서 46ms로 줄어듦.

**한계**

LIBERO-Long과 RoboCasa-GR1(52.2%)에서는 큰 모델보다 낮고, 속도 이득의 상당 부분은 step 수를 줄인 데서 나옴. 실로봇은 과제 4개, 과제당 20회이며, 실패 23건 중 19건이 접촉 단계에서 났고 잡기에 실패해도 policy가 알아채지 못하는 경우가 있었음. 본문에 GitHub 주소는 있으나 상세 학습 recipe는 코드와 함께 공개할 예정이라고만 적혀 있음.

**누리랩 연구와의 연결**

- world model 기반 policy의 추론 계산량을 test time에 고르는 방법이라, test-time optimization이나 계산 예산을 상황에 따라 바꾸는 VLA 연구의 비교 대상이 됨. video 깊이가 action 깊이보다 중요하다는 ablation은 world model 경량화 설계에 바로 쓸 수 있음.
- 저자가 보고한 실패 유형(잡지 못한 채 다음 동작으로 넘어감)은 failure detection·recovery 모듈을 붙여 볼 구체적인 사례임.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 개념도임. (a)는 video expert가 공유 core를 Kv번, action expert가 Ka번 반복하며 late alignment로 video key·value를 읽는 구조를 보여 줌. (b)는 frozen teacher가 student 자신의 상태에서 출발해 만든 target으로 student를 학습하는 elastic self-distillation을 보여 줌.*

---

### 8. Bridging vision-language reasoning and learned control for legged navigation in the wild (72점)

[arXiv](https://arxiv.org/abs/2611.25215) · [PDF](https://arxiv.org/pdf/2611.25215) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25215) · [프로젝트 페이지](https://roam-hiking.github.io) · [영상](https://youtu.be/xcqVpbgklD4)

- **저자**: Takahiro Miki, Robin Schmid, Manthan Patel, Turcan Tuna, Julia Richter, Julian Nubert, Joonho Lee, Matthias Müller 외 1명
- **분야**: Navigation · robotics relevance 8/10 · 1차 스크리닝 70점
- **읽은 원문**: PDF 전문

> VLM에게는 장면 속 지형 이름과 위험도 값만 내게 하고, 공간 판단과 제어는 segmentation·elevation map·RL policy에 맡기는 사족 보행 로봇 주행 시스템 ROAM을 만듦. 스위스 알프스 10.1 km 산길에서 시간 기준 자율 비율 96.7%를 기록함.

**무슨 문제인가**

기존 야외 traversability 추정은 기하 정보에 기대므로 높은 풀, 물, 진흙처럼 형상으로 드러나지 않는 위험을 놓침. 정해진 길로 다녀야 한다는 규범도 반영하지 못하고, 고정 label set으로 학습한 semantic segmentation은 처음 보는 환경에 맞추기 어려움. VLM은 이런 상식 판단을 할 수 있지만, 관절 명령을 직접 내는 VLA는 사족 로봇 demonstration이 부족하고 고주파 보행 제어를 따라가기에 느림. VLM이 waypoint나 pixel 좌표를 직접 내게 하는 방법은 정밀한 공간 추론을 요구하는데, 저자들은 현재 VLM이 이 부분에서 약하다고 봄.

**어떻게 푸나**

ROAM(Robust Open-world Autonomous Mobility)은 VLM에게 공간 판단을 맡기지 않고 장면의 의미 해석만 맡김. VLM은 RGB 영상, 로봇 설명, 출력 값 범위, 이전 질의와 응답을 입력으로 받음. 출력은 장면 속 지형·물체 label과 label마다 붙은 risk, steppable, preferred 값(각각 0~1)임. open-vocabulary segmentation이 이 label로 label별 heatmap을 만들고, 이를 합쳐 dense한 risk·steppable·preferred 영상을 만든 뒤 2.5D elevation map에 투영함. 보행 policy는 steppable 층을 보고 발 디딜 곳을 고르며 속도 명령을 따르고, 지역 주행 policy는 risk 층과 preferred 층을 보고 목표까지 가는 속도 명령을 냄. 두 policy는 시뮬레이션에서 무작위로 만든 height·steppable·risk scan으로 RL 학습하므로 사진 수준의 시뮬레이터가 필요 없음.

**결과**

- 스위스 알프스 Zermatt 산길(10.1 km, 고도차 1220 m)에서 시간 기준 자율 비율이 96.7%임. 사람 개입은 2번이었고, 둘 다 공사 구역에서 segmentation이 울타리와 공사 지형을 제대로 가르지 못해 생김. Seealpsee 호수 둘레 2.38 km 경로에서는 97.5%임.
- VLM 출력 형태 비교(정지 영상 27장, 사람이 표시한 안전·선호 영역 기준)에서 경로 pixel 중 안전 영역 비율은 ROAM label에 A*로 경로를 짠 경우 0.991임. VLM이 pixel 좌표를 직접 낸 두 방식은 0.714와 0.670, 직선 경로는 0.900임. 선호 영역 비율은 0.868 대 0.398·0.363·0.550이고, 목표 도달은 27장 중 27장 대 3~5장임.
- 취리히 캠퍼스 1.2 km 코스에서 기하 정보만 쓰는 Field Local Planner, 목표 영상을 따르는 ViNT와 비교함. ROAM은 공사 표지판을 읽고 풀밭으로 돌아간 뒤 종료 표지판을 보고 길로 돌아왔고, 두 baseline은 표지판에 반응하지 않음. 길에 눕힌 마네킹은 두 baseline 모두 밟음.
- 계단 사진 27장(실측 높이 13.0~18.0 cm)에서 Gemini 3.0·3.5의 높이 추정 평균 절대 오차는 약 0.7 cm, Gemini 2.5는 약 1.8 cm임. 15 cm 제한을 주면 최신 모델도 15.5~16.0 cm 계단을 낮은 위험으로 판정함. 저자들은 이를 근거로 물리 한계 판단은 elevation map과 policy가 맡아야 한다고 주장함.

**한계**

장거리 실험은 경로마다 1회이고, 자율 비율은 시간 기준이라 실패 횟수를 직접 보여 주지 않음. baseline과의 실로봇 비교는 상황별 1회 정성 시연뿐이라 성공률 수치가 없고, 정량 비교는 RL policy 대신 A*를 쓴 정지 영상 실험임. 현장 실험은 클라우드 상용 VLM에 기대고 추론 지연을 메우려고 별도 sign detector를 덧붙였으며, 코드 저장소 주소는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- VLM 출력을 label과 값으로 제한한 설계는 VLN과 semantic mapping 연구에서 VLM 출력 단위를 정할 때 비교 기준으로 쓸 수 있음.
- VLM이 pixel 좌표를 직접 낼 때 안전 비율이 0.714에 그치고 cm 단위 높이 판단이 틀린다는 결과는, VLA에 공간 추론까지 맡길 때 생기는 failure mode를 진단하는 근거가 됨.

*대표 그림: 측정 결과가 아니라 ROAM의 처리 구조를 그린 그림임. 카메라 영상을 VLM이 분석해 label별 risk·steppable·preferred 값을 내고, segmentation과 elevation map을 거쳐 보행 policy와 지역 주행 policy로 이어지는 흐름과 단계별 동작 주기가 적혀 있음.*

---

### 9. Stuck in Place: Stall Diagnosis and Remedies for JEPA Planners (72점)

[arXiv](https://arxiv.org/abs/2611.25415) · [PDF](https://arxiv.org/pdf/2611.25415) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25415) · [코드](https://github.com/jhlee0619/unstick)

- **저자**: Junhyeok Lee, Dongheon Lee, Kyu Sung Choi
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 70점
- **읽은 원문**: PDF 전문

> JEPA world model로 MPC planning을 하는 agent의 실패 대부분이, 물체는 그대로인데 model은 진전을 예측하며 같은 계획을 되풀이하는 정지 상태(stall)임을 closed loop 추적으로 보임. 배포 전 fine-tuning에 더해 실행 중에는 가중치를 고정한 채 이 반복을 끊는 Unstick으로 PushObj T 모양 성공률을 53.3%에서 78.7%로 올림.

**무슨 문제인가**

JEPA(joint-embedding predictive architecture) world model은 미래 frame의 embedding을 예측하고, MPC가 이 예측으로 goal embedding에 다가가는 action을 매 step 다시 최적화함. 이런 planner가 실패하면 test-time adaptation 연구들은 distribution shift에서 생긴 model 오차로 보고, 실행 중인 episode로 가중치를 갱신함. 그러나 MPC는 자기 행동이 만든 상태에서 다시 계획하므로, 상태를 바꾸지 못하는 오차는 매 replan마다 되풀이될 수 있음. 기존 분석은 계획이나 후보 action의 점수만 보았고, 실행되는 planning loop 자체에서 실패가 어떻게 생기는지는 확인하지 않았음.

**어떻게 푸나**

저자는 먼저 진단 단계에서 실행된 action을 simulator에 다시 넣어 실제 상태를 복원하고, MPC step 20~30 동안 block이 5 px·5도 미만으로 움직인 episode를 stall로 분류함. stall 상태에서는 model이 제자리에 머무는 계획을 실제보다 좋게 평가하고, 이전 계획에서 warm start하는 gradient descent(GD) planner가 같은 상태에서 거의 같은 계획을 다시 내놓아 고정점에 빠짐. 이 두 원인에 맞춰 Unstick은 배포 전 on-policy fine-tuning과 가중치를 고정한 test-time loop breaker 하나(Unstick-Mem 또는 Unstick-ReInit)를 묶음. on-policy fine-tuning은 별도 episode에서 base planner가 실행한 궤적으로 predictor 마지막 block과 encoder projection head를 미리 학습함. Unstick-Mem의 residual memory는 실행한 chunk마다 (latent, action) key와 one-step 예측 오차를 저장하고, 계획 중 가까운 입력의 예측에 kernel 가중 평균으로 그 오차를 더함. 그래서 제자리 chunk를 다시 고르면 model도 제자리에 머문다고 예측함. Unstick-ReInit은 warm start 대신 매 replan을 무작위 계획에서 시작해 같은 상태에서 같은 계획이 나오지 않게 함.

**결과**

- 진단: PushT(T자 block을 목표 자세로 미는 과제)와 PushObj(여러 모양 block을 미는 과제)의 15개 설정 중 12개에서 실패의 96% 이상이 stall임. T 모양 stall에서 model은 chunk당 0.030의 cost 감소를 예측하지만 실제 감소는 0임. MPC step 25의 stall 101개 중 planner가 더 좋은 계획을 찾지 못해서 생긴 경우는 없었음.
- PushObj(block을 목표 자세로 미는 과제, 학습 모양 4개·처음 보는 모양 3개)의 T 모양에서 GD 성공률이 base 53.3%에서 Unstick-Mem 78.7%, Unstick-ReInit 76.0%로 오름. 매 chunk 가중치를 갱신하는 AdaJEPA는 84.7%임.
- AdaJEPA가 base 대비 얻은 성공률 향상 중 Unstick-Mem이 되찾은 비율은 모양 7개에서 91%, 시각 조건 7개에서 72%임. Unstick-ReInit은 각각 88%, 31%임. MPC step당 시간은 Unstick-Mem 7.4초, base 6.7초, AdaJEPA 8.3초임.
- 다른 world model에서는 효과가 줄어듦. DINO-WM에서 Unstick-Mem 성공률은 base와 같은 52.0%임. PointMaze-Medium에서는 fine-tuning을 붙이면 두 방법 모두 base보다 낮아짐.

**한계**

모든 실험은 2D 시뮬레이션(PushT, PushObj, PointMaze)이고 실로봇 실험은 없으며, 진단은 한 JEPA 계열과 GD planner 위주임. CEM planner에서는 memory가 fine-tuning에 더하는 효과가 작고, encoder가 block 각도를 잃는 red block 조건이나 objective의 local minimum이 원인인 PointMaze에서는 두 방법 모두 거의 효과가 없음. memory는 episode 길이에 따라 커지고, fine-tuning에는 평가와 별도인 base planner 실행 데이터가 필요함.

**누리랩 연구와의 연결**

- world model planner의 실패를 open-loop 예측 오차가 아니라 closed loop에서 상태 변화와 계획 반복으로 판정하는 진단 절차임. failure detection·recovery 연구에서 latent MPC 기반 manipulation policy를 점검하는 기준으로 쓸 수 있음.
- 가중치 갱신 없이 episode 안의 예측 오차를 저장해 쓰는 residual memory는 test-time optimization과 robot memory를 잇는 간단한 baseline임. test-time adaptation 방법과 비교할 때 함께 넣어 볼 만함.

*대표 그림: PushObj T 모양 한 episode에서 MPC step별 latent cost를 base GD와 Unstick-Mem으로 비교한 그림임. base GD는 약 step 8 이후 실제 cost가 변하지 않는 stall 구간에서 예측 cost만 낮게 유지되고, Unstick-Mem은 짧은 stall 구간을 거쳐 step 20 무렵 성공에 도달함.*

---

### 10. One Prior, Two Dynamics: Repurposing Video Diffusion Transformers for Self-Supervised Latent Action Learning (70점)

[arXiv](https://arxiv.org/abs/2611.26617) · [PDF](https://arxiv.org/pdf/2611.26617) · [alphaXiv](https://www.alphaxiv.org/abs/2611.26617) (요약 있음) · [프로젝트 페이지](https://showlab.github.io/o2laf)

- **저자**: Yuxin Jiang, Wenqiang Sun, Jiaqi Li, Yuchao Gu, Lvmin Zhang, Ivor Tsang, Mike Zheng Shou
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> 사전학습된 video DiT 하나를 inverse dynamics와 forward dynamics 양쪽의 초기값으로 써서, 행동 라벨 없는 영상에서 latent action을 학습함. 사람 손 영상만으로 학습했는데도 GR-1 휴머노이드 로봇 end-effector 동작의 linear probing R²가 0.277로, 기존 latent action 방법 DreamDojo의 0.149보다 높음.

**무슨 문제인가**

Latent action learning은 두 frame 사이의 행동을 추정하는 IDM(inverse dynamics model)과, 그 행동으로 다음 frame을 예측하는 FDM(forward dynamics model)을 함께 학습함. 기존 방법은 IDM을 처음부터 학습하거나 고정된 visual feature 위에서 학습하므로, 영상 변화에 대한 사전 지식을 IDM에서 거의 쓰지 못함. 사전학습된 video generator를 FDM으로 쓰는 방법도 있음. 다만 일반 diffusion 학습 방식을 그대로 쓰면 generator가 latent action을 무시하고 noisy target만으로 미래를 맞힐 수 있음. 라벨 없는 대규모 영상에서 로봇에 옮겨 쓸 행동 표현을 얻으려면 두 모델에 사전 지식을 넣으면서 각 모델이 보는 정보를 통제해야 함.

**어떻게 푸나**

O2LaF(One Prior, Two Dynamics Latent Action Framework)는 IDM과 FDM을 같은 Wan2.2-TI2V-5B video DiT에서 시작해 각각 rank-128 LoRA로 따로 적응시킴. IDM은 영상 latent를 한 번만 forward pass하고, 전이 x_i→x_{i+1}마다 학습되는 action query 하나를 둠. 각 query는 두 끝 frame만 읽고 다른 query나 video token에 정보를 넘기지 않음. query 출력은 Gaussian head를 거쳐 32차원 latent action이 됨. FDM은 깨끗한 첫 frame과 latent action 열을 받아 이후 frame 전체를 한 번에 denoise하고, frame-causal attention으로 뒤 frame을 보지 못하게 함(causal joint prediction). 이전 frame을 깨끗하게 주는 autoregressive 예측은 앞 frame을 복사하는 shortcut이 생기므로 쓰지 않음. FDM의 flow timestep은 높은 noise 쪽에 몰아서, noisy target에 남은 정보로 미래를 맞히는 경로를 줄임. 두 모델은 flow matching loss와 KL 항으로 end-to-end 학습됨. 추론 때 FDM은 다른 첫 frame에 latent action을 넣어 영상을 만드는 world model로 쓰임.

**결과**

- In-lab Eval(DreamDojo의 GR-1 로봇 demonstration 평가 세트)에서 고정된 latent action에 Ridge regression probe를 붙여 양팔 end-effector 이동·회전을 맞힘. EgoDex 사람 손 영상만으로 학습한 O2LaF의 EEF(end-effector) R²는 0.277임. 대규모 1인칭 사람 영상으로 학습해 공개된 기존 latent action 방법 DreamDojo는 같은 평가에서 0.149임.
- MIND(1인칭·3인칭 camera navigation 평가 세트)에서 reference 영상의 latent action을 다른 첫 frame에 옮겨 영상을 생성함. 3인칭 회전 오차(RPE)는 0.330으로, 기존 latent action 방법 Olaf-World의 0.701보다 낮음. 1인칭 이동 오차(NRMSE)는 1.289 대 1.627임. 공정한 비교를 위해 각 방법의 latent action마다 같은 구조의 bidirectional FDM을 따로 학습해 영상을 생성함.
- 사람 영상의 latent action을 로봇 첫 frame에 옮겨 영상을 만들고, 다시 사람 첫 frame으로 되돌려 원본과 비교함. 이 cycle 재구성 PSNR은 24.30으로 DreamDojo 22.61보다 높음. 로봇→사람→로봇 cycle에서는 PSNR 18.85 대 18.35, LPIPS 0.163 대 0.165로 차이가 작음.
- FDM 설계 비교에서 MIND 1인칭 영상의 camera 동작을 latent action으로 맞히는 probing 정확도(k=50, exact match)는 FDM을 causal joint로 두면 87.95%, autoregressive로 두면 70.13%임. IDM의 출발점을 자기지도 예측 영상 encoder V-JEPA2로 바꾸면 같은 MIND 1인칭 probing 정확도가 88.62%로 더 높음. 그러나 latent action에서 원본 장면 밝기가 R² 0.514로 복원되어 외관 정보가 섞여 들어감.

**한계**

실험은 모두 오프라인 영상 평가(linear probing, 영상 생성, cycle 재구성)이고, latent action으로 policy를 학습하거나 실로봇에서 closed-loop로 실행한 결과는 없음. 로봇 평가는 GR-1 demonstration 영상에 한정되고, 사람과 로봇 사이 직접 전이는 정성 평가만 있음. FDM을 policy 검증에 쓰는 부록 실험은 사례 3개의 정성 결과이며, 본문에는 project page 주소만 있고 코드 주소는 확인 불가임.

**누리랩 연구와의 연결**

- 라벨 없는 사람 영상에서 로봇 end-effector 동작과 선형으로 대응되는 latent action을 얻는 방법이라, VLA의 latent action pretraining(LAPA 계열)에서 IDM을 바꿔 볼 후보임.
- 부록에서 FDM rollout이 simulator 결과와 어긋나는 경우를 실행 전 경고로 쓰는데, world model 기반 failure detection 연구의 비교 사례로 볼 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 개념도임. 기존 latent action 학습을 사전학습 prior가 들어가는 위치에 따라 네 가지로 나누고, O2LaF는 같은 video DiT를 IDM과 FDM 양쪽에 fine-tuning해 쓴다는 차이를 보여 줌.*

---

### 11. Risk-Controlled Test-Time Adaptation for Vision-Language-Action Models (68점)

[arXiv](https://arxiv.org/abs/2611.26438) · [PDF](https://arxiv.org/pdf/2611.26438) · [alphaXiv](https://www.alphaxiv.org/abs/2611.26438)

- **저자**: Zixuan Liu, Hashem Haghbayan, Zizhan Zheng, Siavash Khajavi
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 75점
- **읽은 원문**: PDF 전문

> retrieval-augmented VLA가 직접 행동할지 전문가에게 행동을 요청할지를 학습된 uncertainty로 정하고, 그 threshold를 사용자가 정한 task 실패율을 통계적으로 만족하도록 calibration함. LIBERO 4개 suite에서 π0-FAST 기준 평균 성공률이 기존 retrieval 방식 RICL의 62.8%에서 72.0%로 오르고, 이때 step의 49.0%에서 expert 행동을 받음.

**무슨 문제인가**

RICL(Re-training for In-Context Learning)은 VLA 가중치를 바꾸지 않고, 현재 화면과 DINOv2 특징이 가까운 expert demonstration frame을 검색해 context로 넣어 새 과제에 적응함. 그런데 같은 과제의 관련 demonstration을 검색해도 VLA가 그 정보를 잘못 써서 실패하는 경우가 있음. 논문 그림 1에서는 RICL이 그릇을 cabinet 반대쪽으로 옮겨 시간 제한에 걸림. 따라서 검색 품질을 높이는 것만으로는 성공이 보장되지 않고, 배치할 때 요구 성공률을 지키려면 VLA가 언제 틀릴지 알아야 함.

**어떻게 푸나**

R2-VLA는 먼저 RICL 방식으로 VLA를 학습한 뒤 고정하고, 가벼운 MLP uncertainty head만 따로 학습함. 이 head는 첫 action token 위치에서 VLA 마지막 층의 hidden state를 입력받아, 예측 action chunk와 expert action 사이의 차원별 표준편차로 정규화한 RMSE를 예측함. 잘못 검색된 경우의 높은 오차도 배우도록, 학습 데이터의 30~50%에는 다른 과제, 다른 단계, 같은 장면의 다른 목표, 무작위 demonstration을 일부러 검색해 넣음. 배포 때는 매 step 예측 uncertainty가 threshold λ 이하면 VLA 행동을 실행(ACT)하고, 넘으면 expert 행동을 요청(ASK)함. λ는 Learn-then-Test 방식으로 정함: 후보 λ마다 보정용 episode를 실제로 돌려 실패 수를 세고, binomial 검정과 Bonferroni 보정을 통과한 후보 중 ASK 비율이 가장 낮은 것을 고름. 연속 적응 단계에서는 ASK로 받은 expert 행동을 검색 buffer에 추가하고, 새 보정 episode로 λ를 다시 정함. 저자는 실패 위험의 상한(Theorem 1)과 buffer 갱신 뒤에도 위험 보장이 유지됨(Theorem 2)을 증명함.

**결과**

- LIBERO(Franka 팔 시뮬레이션 조작 benchmark, Spatial·Object·Goal·Long 4개 suite)에서 과제당 100회 평가함. 평균 성공률이 RICL 대비 MiniVLA 51.8%에서 62.8%, π0-FAST 62.8%에서 72.0%, OpenVLA 57.4%에서 68.6%로 오름. 이때 평균 ASK 비율은 각각 20.8%, 49.0%, 33.3%임.
- VLA 3개와 suite 4개의 12개 조합마다 목표 성공률을 RICL보다 5퍼센트포인트 안팎 높게 잡았고, 11개 조합에서 목표를 달성함. π0-FAST의 Object suite는 78.9%로 목표 80.0%에 못 미침.
- 같은 ASK 비율로 무작위 시점에 expert를 부르는 Random ASK와 비교하면 평균 성공률이 π0-FAST 72.0% 대 65.5%, MiniVLA 62.8% 대 54.9%, OpenVLA 68.6% 대 60.3%임.
- 같은 risk control에 다른 uncertainty 신호를 쓴 경우, π0-FAST에서 DINO 거리는 성공률 68.1%·ASK 59.6%, action entropy는 70.2%·59.1%이고 R2-VLA는 72.0%·49.0%임.

**한계**

실험은 LIBERO 시뮬레이션뿐이고 실로봇 실험이 없으며, ASK 때 행동을 주는 expert는 사람이 아니라 따로 학습한 expert policy임. π0-FAST의 Long suite에서는 decision point의 66.3%에서 expert를 불러, 목표 달성의 상당 부분을 expert가 맡음. 후보 threshold마다 보정 episode(기본 200개)를 실제로 돌려야 하고 보정 episode가 배포 분포에서 독립으로 뽑힌다고 가정하며, 본문에 코드 주소가 없음.

**누리랩 연구와의 연결**

- VLA 행동 단위의 failure prediction을 task 단위 성공률 보장과 묶은 예라, VLA failure detection·recovery 연구에서 threshold를 정하는 절차의 비교 기준으로 쓸 수 있음.
- expert 교정을 검색 buffer에 쌓고 위험 보장을 유지하며 다시 calibration하는 구조는, robot memory 기반 test-time adaptation에서 memory 갱신 뒤 안전 기준을 다시 맞추는 문제와 바로 이어짐.

*대표 그림: LIBERO-Goal의 그릇을 cabinet 위에 올리는 과제에서 RICL과 R2-VLA를 비교한 사례 그림임. 위쪽은 RICL이 step 85에 demonstration 4개를 검색하고도 그릇을 cabinet 반대쪽으로 옮겨 step 300에 실패하는 장면임. 아래쪽은 R2-VLA가 uncertainty가 threshold 0.66을 넘은 구간에서 expert 행동을 받아 step 96에 성공하는 장면과 step별 uncertainty 곡선임.*

---

### 12. Don't Lose the Future: Latent-Aware 4-Bit Quantization of World Action Models (68점)

[arXiv](https://arxiv.org/abs/2611.25614) · [PDF](https://arxiv.org/pdf/2611.25614) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25614)

- **저자**: Yichen Guo, Yanlong Chen, Xinyue Zhang, Mohan Liu, Song Zhang, Yawei Li
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 70점
- **읽은 원문**: PDF 전문

> world action model(WAM)을 4-bit로 양자화할 때 action만이 아니라 예측된 미래 latent를 보존 대상으로 삼고, 한 번 생긴 반올림 오차가 이후 denoising step에서 몇 번 다시 쓰이는지에 따라 token마다 정밀도를 다르게 줌. LIBERO-Plus에서 Fast-WAM 평균 성공률이 76.4%로 BF16 모델(77.6%)과 1.2퍼센트포인트 차이임.

**무슨 문제인가**

WAM은 장면이 어떻게 변할지 예측한 미래 latent를 만들고, 이 미래를 조건으로 action을 냄. Fast-WAM은 parameter가 6B이고 BF16 weight만 12 GB라서, 16 GB를 로봇 프로그램과 나눠 쓰는 Jetson Orin NX에 올리기 어려움. 그래서 weight·activation·key-value cache를 모두 4-bit로 두는 W4A4KV4가 필요함. 기존 WAM 양자화 방법은 최종 action에 대한 민감도를 denoising step 하나씩 따로 재서 action 경로를 보호함. 저자들은 Fast-WAM에서 action 경로를 보호해도 action 오차가 16%만 줄고, 예측 미래를 BF16 값으로 바꿔 넣으면 남은 action 오차의 71.2%가 사라짐을 보임.

**어떻게 푸나**

LAQ(Latent-Aware Quantization)는 학습 없이 BF16 WAM과 calibration context 80개를 받아 W4A4KV4 모델을 내는 post-training quantization임. 저자는 예측 미래를 action으로 바꾸는 계산을 reader라 부르고, 미래 latent 오차를 reader 출력 변화로 재는 Gauss-Newton 행렬(reader metric)을 추정함. read count는 한 번 생긴 반올림 오차가 몇 개 denoising step에서 다시 읽히는지를 센 값이며, weight·cache·변하지 않는 관측 token의 오차를 매 step 새로 생기는 오차보다 크게 가중함. 두 값을 action 오차·미래 오차·reader 오차를 합친 목표식에 넣으면, activation과 cache 중 어떤 token에 정밀도를 더 줄지가 임계값 하나로 정해짐. 실행 중에는 gaze-guided refinement가 선택된 token의 1차 4-bit 양자화 잔차를 한 번 더 4-bit로 양자화함. 선택할 token은 직전 control step에서 action token이 각 token에 준 attention(gaze)으로 고르며, 모든 weight는 4-bit이고 16-bit branch나 과제별 재보정은 없음.

**결과**

- LIBERO-Plus(LIBERO 4개 suite에 카메라 시점·센서 noise 등 7종 교란을 더한 시뮬레이션 조작 benchmark)에서 Fast-WAM 평균 성공률은 LAQ 76.4%, BF16 77.6%임. 가장 강한 baseline인 diffusion 모델용 양자화 방법 SVDQuant는 73.0%임. baseline은 cache를 BF16으로 두고, LAQ는 cache도 4-bit로 둔 조건임.
- parameter 2B인 다른 WAM Cosmos-Policy에서는 LAQ 83.3%, BF16 83.5%, diffusion 모델용 양자화 방법 ViDiT-Q와 SVDQuant 82.9%로 baseline과의 차이가 0.4퍼센트포인트임. 원래 LIBERO에서는 BF16과 모든 baseline이 98% 근처라 방법 간 차이가 거의 없음.
- Fast-WAM ablation에서 같은 budget으로 token 선택 기준만 바꾸면, 기존 WAM 양자화 방식인 step별 action 민감도는 72.9%, 무작위 선택은 72.5%, LAQ는 76.4%임. reader metric을 단위행렬로 바꾸면 73.6%, read count를 모두 1로 두면 74.0%로 내려감.
- 실제 AgileX PiPER 팔에서 Fast-WAM으로 과제 3개를 과제·방법당 25회 평가함. 평균 성공률은 과제 3개를 항목 4개(pick-and-place의 사과 넣기와 두 물체 모두 넣기, 선반 넣기, 상자 쌓기)로 나눠 잰 값의 평균임. LAQ 47.0%, BF16 52.0%, 범용 양자화 방법 QuaRot 17.0%임. A100에서 policy peak memory는 14.0 GB에서 6.0 GB로, 1회 호출 지연은 1475 ms에서 888 ms로 내려감.

**한계**

효율은 A100에서만 측정했고, 동기로 든 Jetson Orin NX에서의 메모리·지연은 본문에서 확인 불가임. Cosmos-Policy에서 baseline과의 차이는 0.4퍼센트포인트로 작고, 반복 seed나 분산은 보고하지 않음. 기존 WAM 전용 양자화 방법 3개는 공개 구현이 없어 전체 방법으로는 비교하지 못했고, token 선택 기준만 ablation에서 재현함. 실로봇은 Fast-WAM 하나에 과제 3개이며 본문에 코드 주소가 없음.

**누리랩 연구와의 연결**

- world model 기반 policy를 실로봇에 올릴 때의 메모리·지연 문제를 다룬 사례임. reader metric이 팔과 gripper 주변 token에 몰린다는 분석은 world model의 예측 중 어느 부분이 action에 실제로 쓰이는지 볼 때 참고가 됨.
- 예측 미래를 BF16으로 바꿔 넣어 action 오차 기여를 나누는 실험 방식은, world model 예측 오류가 action 실패로 이어지는 경로를 진단하는 failure detection 연구에 그대로 쓸 수 있음.

*대표 그림: 측정값 하나를 요약한 개념도이며 방법 구조나 전체 결과표는 아님. BF16, W4A4KV4, W4A4KV4에 BF16 예측 미래를 바꿔 넣은 경우를 위에서 아래로 세 줄로 그림. 미래를 되돌리면 action 오차가 71.2% 줄어든다는 것을 막대로 표시함.*

---

### 13. A$^2$-VLA: Adapting Vision-Language-Action Policies to New Tools through Agentic Affordance Discovery (66점)

[arXiv](https://arxiv.org/abs/2611.25656) · [PDF](https://arxiv.org/pdf/2611.25656) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25656) (요약 있음)

- **저자**: Chenyuan Zhou, Chaoyi Huang, Zibo Wang, Zhiyuan Li, Yong-Lu Li
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> 새 도구에서 어느 부분이 일을 하는지(affordance)를 agent가 시뮬레이션 실험으로 찾아 12차원 벡터로 만들고, 이 벡터를 π0.5에 조건으로 넣음. 실로봇 과제 3개에서 처음 보는 도구의 평균 성공률이 π0.5의 4.7%에서 35.3%로 오름.

**무슨 문제인가**

모양이 다른 도구라도 갈고리 끝이나 날처럼 같은 일을 하는 부분이 있지만, VLA는 학습 데이터에 없던 도구 형상을 만나면 성공률이 크게 내려감. 그래서 새 도구마다 demonstration을 다시 모아 fine-tuning해야 함. MimicFunc 같은 기존 도구 전이 방법은 keypoint와 function frame 규칙을 사람이 미리 정해 두므로, 과제마다 어떤 기하 특징이 필요한지를 스스로 정하지 못함. language나 keypoint만으로 도구 기하를 VLA에 전달하는 계층형 방법도 도구의 세부 형상을 다 담지 못함.

**어떻게 푸나**

A2-VLA는 도구 affordance를 agent가 세우고 시험하고 고치는 가설로 다룸. 먼저 agent(GPT-6 Astra)가 원본 도구 몇 개로 찍은 teleoperation demonstration과 보정된 카메라·로봇 모델로 장면을 시뮬레이션에 다시 만듦(real-to-sim). 이어서 원본 도구들을 비교해 과제에 필요한 기능 부위와 그 기하 특징(위치, 접선 방향, 오목한 쪽 방향 등)을 정하고, 이를 뽑아내는 실행 가능한 extraction skill을 작성함. 다른 도구의 기능 부위 자세가 원본 궤적의 기능 부위 자세를 따라가도록 궤적을 다시 계획(retargeting)하고 시뮬레이션에서 실행함. 실패하면 접촉 정보와 화면을 보고 기능 부위나 skill을 고치며, 통과한 skill은 skill library에 쌓음. VLA 쪽은 π0.5에 12차원 affordance 벡터를 token 하나로 더 넣고, 앞으로의 affordance 궤적을 예측하는 보조 head를 붙여 학습함. 기능 부위 자세를 일부러 흔든 뒤 원래 궤적으로 돌아가게 다시 계획한 counterfactual 데이터를 10% 섞어, policy가 주어진 affordance를 따르도록 함.

**결과**

- 재구성한 시뮬레이션에서 처음 보는 도구로 궤적을 retargeting한 과제 3개 평균 성공률이 86.1%임. 같은 GPT-6 Astra가 시뮬레이션 시험 없이 affordance를 바로 예측한 Raw VLM은 37.8%, 가장 강한 기존 방법인 물체 간 상대 자세 예측 방법 TAX-Pose는 26.9%임.
- 실로봇(Dobot Nova 2 양팔, 과제 3개)에서 처음 보는 도구의 평균 성공률이 35.3%임. affordance 없는 π0.5는 4.7%, 시뮬레이션 수정 단계를 뺀 변형은 22.0%임.
- 사람이 준 affordance로 학습·추론한 Human Oracle은 처음 보는 도구에서 47.3%임. agent가 찾은 affordance와 사람이 준 affordance 사이에 12퍼센트포인트 차이가 남음.
- agent가 VLA 없이 직접 로봇을 움직인 Agent-Only는 처음 보는 도구에서 25.0%(과제당 20회)임. Cut Sand(도구 날로 모래를 잘라 그릇에 옮기는 과제)에서는 Agent-Only 30%가 A2-VLA 26%보다 높음.

**한계**

실로봇 성공률은 VLA 방법이 과제당 50회, Agent-Only가 20회로 평가 횟수가 다르고 seed 수는 본문에서 확인 불가임. 시뮬레이션 비교는 agent가 재구성한 장면에서 재므로, 같은 장면을 쓴 수정 단계와 평가가 얼마나 분리됐는지 본문에서 확인 불가임. 저자는 retargeting으로 풀 수 있는 도구 전이에만 적용된다고 밝혔고, 본문에 코드 주소가 없음.

**누리랩 연구와의 연결**

- 시뮬레이션에서 실패를 보고 affordance와 extraction skill을 고치는 반복 과정은 failure diagnosis를 VLA 입력 수정으로 잇는 사례임. 배포 전에 시뮬레이션으로 policy 입력을 검증하는 연구의 비교 대상으로 쓸 수 있음.
- 기능 부위를 위치·방향 벡터로 만들어 VLA에 넣는 설계는 object-centric 표현을 manipulation policy 조건으로 쓰는 연구와 바로 이어짐.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 개념도임. 위쪽은 장면 재구성, affordance 추출, 시뮬레이션 retargeting 시험, 실패 피드백으로 돌아가는 반복 과정을 그림. 아래쪽은 affordance encoder 출력이 이미지·언어·로봇 상태와 함께 π0.5 action expert의 조건으로 들어가는 구조를 보여 줌.*

---

### 14. Verify2Act: Critic-Guided Latent World Models for Verifying Language-Conditioned Manipulation Plans (66점)

[arXiv](https://arxiv.org/abs/2611.25243) · [PDF](https://arxiv.org/pdf/2611.25243) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25243)

- **저자**: Chrisantus Eze, Christopher Crick
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 72점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 7쪽
- **읽은 원문**: PDF 전문

> VLM이 낸 후보 plan을 DINOv2 feature 공간의 world model로 실행 전에 미리 굴려 보고, critic이 검사한 plan만 실행하게 함. 저가 로봇 팔의 블록 조작 과제 6개에서 평균 과제 성공률이 VLM 단독 53.3%에서 83.3%로 오름.

**무슨 문제인가**

VLM은 여러 단계 조작 plan을 잘 내지만, 행동하면 장면이 어떻게 바뀔지 예측하는 모델이 없어 틀린 plan을 그대로 실행함. 이를 확인하려고 pixel 공간에서 미래 영상을 만드는 world model을 붙이면 계산이 오래 걸리고, 단계가 길어질수록 이미지가 원래 장면에서 벗어남. DINOv2 feature 위에서 dynamics를 배우는 latent world model(DINO-WM, RLA-WM)은 더 가볍지만, 언어 명령을 특정 물체에 연결하지 못함. 또한 직전 frame만 보는 Markovian 구조라 gripper가 물체를 가리면 그 물체 정보를 잃음.

**어떻게 푸나**

Verify2Act는 plan 제안, latent 상상, critic 검증의 세 단계를 반복함. 먼저 GPT-4o가 현재 RGB 영상과 언어 목표를 받아 primitive skill 문자열로 된 후보 plan 3개(각 4단계)를 한 번의 호출로 냄. V2A-WM(이 논문의 world model)은 고정된 DINOv2 patch feature를 상태로 쓰고, 두 frame 사이 feature 차이를 autoencoder로 압축한 latent를 flow matching으로 예측함. RLA-WM과 달리, CLIP으로 인코딩한 행동 문장 token에 patch feature가 cross-attention하므로 명령이 해당 물체 patch에 연결됨. 또한 과거 몇 frame과 각 frame이 실제로 있는지 표시하는 validity mask를 함께 보는 causal history window를 둬서 가려진 물체 정보를 유지함. critic의 temporal consistency head는 이웃한 상상 상태가 이어지는지 점수와 불확실도를 내고, goal head는 마지막 상상 상태의 patch token과 목표 문장으로 목표 달성 확률을 냄. 두 점수의 가중합이 기준값을 넘는 plan을 실행하고, 없으면 VLM에 reflection을 요청해 최대 2번 다시 제안받음. 실로봇용 world model과 critic은 MuJoCo로 만든 작업대 digital twin 데이터로만 학습하고, 실행 때는 카메라 영상에서 블록·카메라 자세를 맞춰 twin 영상으로 다시 그려 입력함(real2sim alignment).

**결과**

- Yahboom DOFBOT 실로봇에서 블록 과제 6개를 과제당 10회 실행함. 평균 과제 성공률은 Verify2Act 83.3%, latent world model RLA-WM 61.7%, VLM 단독 53.3%, pixel diffusion world model 46.7%임. 모든 방법이 같은 GPT-4o, prompt, low-level skill을 씀.
- plan 자체의 정답률은 VLM 단독도 93.3%였고 Verify2Act는 100%임. 그래서 성공률 차이 대부분은 정답 plan을 실행하다 실패한 비율에서 생김. 전체 episode 대비 실행 실패 비율은 VLM 단독 43.3%, Verify2Act 16.7%임. 다만 원문 표의 VLM 단독 값은 성공률·plan 실패 비율과 합이 맞지 않음. 같은 skill을 쓰는데 왜 실행 실패가 줄었는지는 본문에서 설명하지 않음.
- 실제 장면 42개에서 가능한 plan을 모두 시뮬레이션해 정답을 매기고 plan 순위를 비교함. real2sim 없이 카메라 영상만 넣었을 때 정답 plan을 1위로 고른 비율이 V2A-WM 71.4%, RLA-WM 23.8%, 무작위 약 6%임.
- CALVIN(언어 지시 조작 과제 5개를 연속 수행하는 시뮬레이션 benchmark)에서 5개 모두 성공한 비율이 75%로, 영상 예측 사전학습 policy GR-1의 73.1%와 VLM 단독 70%보다 높음. 성공률 차이는 몇 개 sequence 수준이라 결정적 증거가 아니라고 저자도 밝힘. CALVIN 평가 전체에서 VLM reflection 호출은 15회로 pixel diffusion world model의 444회보다 적음.

**한계**

실로봇 평가는 책상 위 블록 4개와 pick-and-place skill 3종, 과제당 10회뿐임. 계획 한 번에 24초가 걸려 VLM 단독의 3.4초보다 길고, real2sim alignment는 책상 위에 놓인 블록에만 적용됨. Cluttered Nut Assembly는 robosuite에서 너트 여러 개가 흩어진 장면의 너트 조립 시뮬레이션 과제임. 여기서는 critic이 통과시킨 plan의 성공률(precision)이 Verify2Act 61.8%로 pixel diffusion world model 78.9%보다 낮음. 코드 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- world model을 policy 학습이 아니라 실행 전 plan 검증에 쓴 구조임. failure detection과 test-time plan selection 연구에서 latent world model 기반 baseline으로 쓸 수 있음.
- 실제 장면에서 가능한 plan을 모두 시뮬레이션해 정답을 매기고 top-1 순위를 재는 평가 방식은, 실행 noise와 분리해 verifier 품질만 재는 실험 설계로 가져다 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림으로, 왼쪽에 VLM의 후보 plan 제안과 V2A-World Model의 latent 상상이 있음. 오른쪽은 goal head와 temporal consistency head의 점수로 plan을 고르고, 그 결과가 beam search로 후보 plan에 다시 돌아가는 경로를 보여 줌.*

---

### 15. GEMS: Generation and Experience Memory for Subgoal-Guided Long-Horizon World Model Planning (66점)

[arXiv](https://arxiv.org/abs/2611.25134) · [PDF](https://arxiv.org/pdf/2611.25134) · [alphaXiv](https://www.alphaxiv.org/abs/2611.25134)

- **저자**: Yangchen Zhao, Ali Payani, Caiwen Ding
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 70점
- **읽은 원문**: PDF 전문

> 고정된 latent world model로 먼 목표를 계획할 때, 생성한 중간 subgoal과 학습 데이터에서 찾은 실제 frame 중 하나를 거리 기준으로 골라 planner의 목표로 씀. planner는 행동 후보를 표본 추출해 좋은 것을 남기는 CEM(cross-entropy method)임. 150 step 앞 목표를 주는 Cube에서 성공률이 가장 강한 baseline SAGE의 68.8%에서 92.8%로 오름.

**무슨 문제인가**

visual world model planning은 후보 행동의 예측 결과를 목표 이미지의 latent와 비교해 행동을 고름. 목표가 멀면 rollout 오차가 쌓이고, 먼 목표와의 latent 거리로는 후보 간 우열을 가리기 어려움. 이를 줄이려고 중간 subgoal을 쓰는 방법이 두 갈래로 있음. 생성 모델로 만든 subgoal은 물체 위치나 시점이 틀릴 수 있고, 저장된 경험에서 고르는 방법은 데이터가 덮는 범위에 묶이며 다음에 어느 상태를 목표로 할지 고를 기준이 약함.

**어떻게 푸나**

GEMS(Generation and Experience Memory for Subgoal planning)는 encoder와 world model(LeWM)을 고정하고 subgoal generator와 CEM에 초기 행동 분포를 주는 action prior만 학습함. generator는 최근 관측 3개의 latent, 목표 latent, 목표까지 남은 step 수 Δ, 다음 subgoal까지의 step 수 τ(기본 15)를 받아 τ step 뒤의 latent를 출력함. Δ와 τ는 함께 정규화하지 않고 따로 Fourier feature로 embedding함. 출력은 현재 latent와 목표 latent 사이를 min(τ/Δ, 1) 비율로 보간한 anchor에 Transformer decoder가 예측한 residual을 더한 값임. 이 subgoal로 LEM(Latent Experience Memory: 학습 궤적의 모든 frame을 같은 encoder로 인코딩해 둔 저장소)에서 가장 가까운 latent를 찾음. 둘의 거리가 임계값 λ 이하이면 저장된 frame을, 넘으면 생성한 subgoal을 CEM의 비용 목표로 씀. λ는 과제마다 후보 4개(0, 무한대, subgoal과 메모리 frame 거리의 중앙값, generator 오차의 중앙값) 중 validation 성공 수가 가장 많은 값으로 정하고, τ step마다 다시 계획함.

**결과**

- 조작 과제 4개에서 성공률이 가장 높음. Cube(OGBench의 단일 큐브 집어 옮기기, 목표 150 step 앞)에서 92.8%로 SAGE의 68.8%보다 24.0퍼센트포인트 높음. Meta-World(조작 과제 6개 모음)에서는 54.1% 대 31.9%임.
- Cube-double(큐브 2개, 목표 75~255 step 앞)에서는 17.7%이고 다른 방법은 모두 1% 미만임. 같은 조건에서 전문가의 실제 미래 frame을 subgoal로 쓰는 기준선은 35.6%라서 아직 차이가 큼.
- Cube에서 큐브를 먼저 잡아야 하는 test query 236개의 성공률은 87.9%이고 baseline은 모두 48.4% 이하임. 경험 메모리를 빼면 79.4%로 내림.
- ablation에서 Δ·τ를 따로 embedding하면 메모리 없이도 Cube 성공률이 67.6%에서 87.7%로 오름. 메모리를 더하면 Meta-World는 46.2%에서 54.1%로 오르지만 Push-T(T자 block을 목표 자세로 미는 과제)는 70.4%에서 68.4%로 내림.

**한계**

모든 실험은 시뮬레이션이고 실로봇 실험은 없으며, 본문에 코드 주소가 없음. 경험 메모리는 test와 같은 분포의 학습 궤적에 기대고, 큐브 2개처럼 상태 조합이 많은 과제에서는 메모리 frame의 큐브 위치가 26~32 cm 어긋남. 메모리 사용 여부를 정하는 λ를 과제마다 validation으로 골라야 하고, TwoRoom·Reacher(navigation·reaching)에서는 기존 방법 대비 이득이 없음.

**누리랩 연구와의 연결**

- world model 기반 test-time planning에 robot memory를 붙이는 구체적 설계임. 생성 subgoal과 저장 frame 중 무엇을 믿을지 거리로 고르는 gate는 world model 예측의 신뢰도 판단 연구에서 비교 대상으로 쓸 수 있음.
- 큐브 잡기 전 단계를 건너뛰는 subgoal 비율을 latent probe로 잰 분석(15.5%에서 3.2%로 내림)은 long-horizon manipulation의 실패 원인 진단 방법으로 참고할 만함.

*대표 그림: Cube 과제에서 최종 목표만 보고 계획하면 큐브를 끝내 집지 못하고, GEMS는 경험 메모리에서 고른 실제 frame을 subgoal로 따라가 목표에 도달하는 rollout 예시임. 오른쪽 그래프는 목표가 25~150 step 앞일 때 GEMS와 최종 목표만 쓰는 계획의 Cube 성공률을 비교함.*

---

## 오늘의 흐름

- **world model을 실행 전 검사와 실패 진단에 씀**: world model planner가 왜 실패하는지 가르거나, 실행 전에 plan과 후보 행동을 검사하는 데 씀. 오늘 Top 15 중 네 편이 이 쓰임새임: [Search or Scoring?](https://arxiv.org/abs/2611.25347), [Stuck in Place](https://arxiv.org/abs/2611.25415), [Verify2Act](https://arxiv.org/abs/2611.25243), [AFFECT](https://arxiv.org/abs/2611.25980)(world model 속 성공률이 실제 성공률을 따르도록 행동에 따른 영상 변화를 맞추는 보조 loss).
- **실로봇 데이터 없이 policy를 post-training함**: WEVO는 video world model 속 rollout으로 VLA를 RL로 고침. CoachSI는 VLM coach가 고른 지시문으로 simulator에서 얻은 성공 rollout을 모아 WAM을 fine-tuning함. WAM(world action model)은 미래 영상과 action을 함께 내는 모델임. 두 편 모두 post-training 전 policy보다 높은 성공률을 보고함: [WEVO](https://arxiv.org/abs/2611.25251), [CoachSI](https://arxiv.org/abs/2611.25529).
- **WAM을 가볍게 하거나 넓힘**: WAM의 추론 비용을 같은 block 반복 사용(LoopedWAM)과 4-bit 양자화(Don't Lose the Future)로 줄임. 로봇 여러 대로도 넓힘(MAWAM): [LoopedWAM](https://arxiv.org/abs/2611.25595), [Don't Lose the Future](https://arxiv.org/abs/2611.25614), [MAWAM](https://arxiv.org/abs/2611.25105).
- **memory를 policy와 planner의 조건으로 넣음**: memory를 subtask 추론의 hidden state(ActMem), planner의 목표 frame(GEMS), 검색 buffer(R2-VLA) 형태로 넣음. GEMS의 planner는 CEM(cross-entropy method: 후보 action을 뽑아 좋은 것만 남기며 반복하는 방법)임: [ActMem](https://arxiv.org/abs/2611.25461), [GEMS](https://arxiv.org/abs/2611.25134), [R2-VLA](https://arxiv.org/abs/2611.26438).
- **VLA를 새 조건에 맞추는 방법**: 새 도구의 기능 부위를 시뮬레이션 시험으로 찾아 VLA에 넣거나, 불확실할 때 전문가에게 행동을 요청하는 threshold를 실패율 상한을 지키도록 calibration으로 정함: [A2-VLA](https://arxiv.org/abs/2611.25656), [R2-VLA](https://arxiv.org/abs/2611.26438).

## 해볼 만한 연구

### world model 검증기가 틀리는 경우를 먼저 가려내기

- 질문: world model로 VLA 후보 action chunk 순위를 다시 매길 때, AFFECT loss가 scoring failure를 줄여 성공률을 올리는지 밝힘.
- 첫 실험: LIBERO(시뮬레이션 조작 benchmark)에서 VLA 후보 여러 개를 world model cost로 고름. 과제의 정답 행동(known solution)을 같은 cost로 채점해, 좋은 후보를 시도하지 못한 경우는 search failure, 정답 행동보다 나쁜 후보에 더 낮은 cost를 준 경우는 scoring failure로 나눔. AFFECT loss를 넣은 world model과 넣지 않은 world model의 scoring failure 비율을 비교함.
- 가장 가까운 연구: [Search or Scoring?](https://arxiv.org/abs/2611.25347)은 CEM planner만 진단했고 VLA proposal은 다루지 않음. [AFFECT](https://arxiv.org/abs/2611.25980)는 world model 학습 loss만 바꾸고 planner 실패 유형은 재지 않음.

### 실행 중 정지 상태를 감지해 language coach를 부르기

- 질문: policy가 같은 행동을 되풀이하는 정지 상태를 실행 중에 world model 예측과 관측의 차이로 감지할 수 있는지 밝힘. 감지할 때만 coach를 불러도 같은 복구 효과가 나오는지도 확인함.
- 첫 실험: RoboCasa365(주방 장면의 단일 skill 과제와 이를 이은 복합 과제를 담은 시뮬레이션 benchmark) 장기 과제에서 비교함. CoachSI처럼 매 action chunk마다 coach를 부르는 조건과, world model이 예측한 과제 진행과 실제 관측의 진행이 어긋날 때만 부르는 조건의 성공률과 coach 호출 수를 잼.
- 가장 가까운 연구: [CoachSI](https://arxiv.org/abs/2611.25529)는 coach를 매 action chunk마다 부름. [Stuck in Place](https://arxiv.org/abs/2611.25415)는 simulator로 실제 상태를 복원해 정지 상태(stall)를 사후에 분류했고, 실행 중 감지기는 만들지 않음. 실험도 2D 시뮬레이션의 JEPA(관측을 latent로 바꿔 다음 latent를 예측하는 world model) planner뿐임.

### hidden state형 memory VLA에 실패율 보장 붙이기

- 질문: subtask 추론의 hidden state를 memory로 쓰는 VLA에서도, 사용자가 정한 실패율 상한을 지키며 전문가 요청 비율을 줄일 수 있는지 밝힘.
- 첫 실험: ActMem에 R2-VLA의 uncertainty 예측 head와, 실패율 상한을 지키도록 threshold를 정하는 calibration을 붙임. 검색 buffer형 memory를 쓰는 R2-VLA와 실패율, ASK 비율(전문가에게 행동을 요청한 비율)로 비교함.
- 가장 가까운 연구: [R2-VLA](https://arxiv.org/abs/2611.26438)는 검색 buffer를 갱신한 뒤 threshold를 다시 정해 실패율 보장을 유지하지만, memory는 검색 buffer뿐임. [ActMem](https://arxiv.org/abs/2611.25461)은 실패율 보장 없이 평균 성공률만 보고함.

## 꼭 읽을 논문

- [Search or Scoring? Diagnosing Why Visual World-Model Planners Fail](https://arxiv.org/abs/2611.25347): world model planner의 실패를 실패 하나 단위로 search와 scoring으로 나누는 절차를 그대로 가져다 쓸 수 있음.
- [Learning What Actions Change](https://arxiv.org/abs/2611.25980): AFFECT loss를 넣으면 world model 속 성공률과 실제 Franka 로봇 성공률의 Pearson 상관이 0.468에서 0.790으로 오름.
- [Self-Improvement with a Language Coach (CoachSI)](https://arxiv.org/abs/2611.25529): VLM coach가 language feedback으로 다음 단계를 지시하고, 그 성공 rollout으로 다시 학습하는 failure recovery 구조임.
- [World Model-Enabled VLA Optimization (WEVO)](https://arxiv.org/abs/2611.25251): video world model 속 RL로 휴머노이드 VLA의 실로봇 성공률을 올렸고, 설계 선택별 ablation이 있음.
- [A Multi-Agent World-Action Model (MAWAM)](https://arxiv.org/abs/2611.25105): WAM을 로봇 2대로 넓히고 실로봇 협업 과제로 검증함.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (547편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2611.26438'>Risk-Controlled Test-Time Adaptation for Vision-Language-Action Models</a></td><td>75</td><td>9</td><td>VLA</td><td>retrieval 기반 VLA의 test-time adaptation에 task-level risk control과 전문가 호출을 도입함. LIBERO 3개 backbone에서 성공률 9.2~11.2퍼센트포인트 상승함. 실로봇 확인 불가함</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2611.25461'>ActMem: From Latent Memory Reasoning to Grounded Robotic Action</a></td><td>74</td><td>10</td><td>VLA</td><td>ActMem이 RoboMemArena 71.1%(+7.5pt), MIKASA-Robo 73.8%, 실로봇 memory 과제 68.8%(+10.0pt)를 보임. memory VLA에서 추론과 perception을 분리한 설계가 우선 주제에 직접 부합함</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2611.25529'>CoachSI: Self-Improvement of Robot Policies with a Language Coach</a></td><td>74</td><td>9</td><td>VLA</td><td>frozen VLM이 다음 단계를 언어로 알려 long-horizon 자기개선을 함. 성공률 47.4%에서 59.3%로 오르고 human demo fine-tuning보다 9.8점 높아 language feedback 주제에 직접 부합함</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2611.25347'>Search or Scoring? Diagnosing Why Visual World-Model Planners Fail</a></td><td>74</td><td>8</td><td>World Model</td><td>DemoProp: 4개 환경 3개 world model에서 계획 실패를 search/scoring으로 분해해 진단하고 규칙으로 처방함. Metaworld 168개 신규 과제 127개 해결 등 증거 강함</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2611.25251'>WEVO: World Model-Enabled VLA Optimization for Whole-Body Loco-Manipulation</a></td><td>74</td><td>8</td><td>VLA</td><td>video world model 안에서 humanoid VLA를 RL로 후처리함. 실로봇 3개 과제 평균 성공률이 23.3%에서 75.0%로 오르고 실로봇 RL(48.3%)보다 높아 증거가 강함</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2611.25105'>MAWAM: A Multi-Agent World-Action Model for Coordinated Manipulation</a></td><td>73</td><td>9</td><td>World Model</td><td>여러 로봇의 행동과 미래 시야를 cross-agent attention으로 함께 생성하는 multi-agent world-action model임. 실로봇 3개 과제 평균 67.8%로 MA-VLA보다 18.9퍼센트포인트 높고 4팔 시뮬레이션까지 검증함</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2611.25595'>LoopedWAM: Looped World Action Models for Elastic Inference</a></td><td>72</td><td>9</td><td>World Model</td><td>LoopedWAM이 0.58B 파라미터로 LIBERO 96.1%, RoboTwin 91.9%, 실로봇 PiPER 4과제 71.3%를 보이며 메모리 7.4배 절감함. 단일 elastic checkpoint 설계도 참신함</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2611.25656'>A$^2$-VLA: Adapting Vision-Language-Action Policies to New Tools through Agentic Affordance Discovery</a></td><td>72</td><td>9</td><td>VLA</td><td>agent가 affordance를 가설로 세우고 검증해 VLA를 새 도구에 적응시킴. 실로봇 3개 과제에서 π0.5보다 30.7퍼센트포인트 높아 문제 설정과 증거가 모두 좋음</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2611.26617'>One Prior, Two Dynamics: Repurposing Video Diffusion Transformers for Self-Supervised Latent Action Learning</a></td><td>72</td><td>8</td><td>World Model</td><td>사전학습 video DiT를 inverse/forward dynamics 양쪽 prior로 재사용하는 latent action 학습임. navigation·조작에서 few-shot probing SOTA와 embodiment 간 zero-shot 전이를 보임</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2611.25243'>Verify2Act: Critic-Guided Latent World Models for Verifying Language-Conditioned Manipulation Plans</a></td><td>72</td><td>8</td><td>World Model</td><td>VLM 계획을 latent world model과 critic으로 실행 전에 검증함. 실로봇 6개 과제 성공률 83.3% 대 VLM 단독 53.3%이고 CALVIN에서도 우위라 failure 예방 관점에서 근거가 강함</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2611.25980'>Learning What Actions Change: Action Effect Matching for Dynamics-Faithful World Models</a></td><td>72</td><td>8</td><td>World Model</td><td>행동 교란에 대한 영상 변화 분포를 맞추는 보조 목표로 world model의 행동 민감도를 높임. DROID에서 policy 평가 상관이 0.47에서 0.79로 오르고 실로봇 설정을 포함해 증거가 강함</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2611.25614'>Don&#x27;t Lose the Future: Latent-Aware 4-Bit Quantization of World Action Models</a></td><td>70</td><td>9</td><td>VLA/Efficient</td><td>WAM W4A4KV4 양자화로 LIBERO-Plus에서 16bit 대비 1.2퍼센트포인트 이내, 1.66배 빠름. 실제 PiPER 팔 실험까지 있어 온보드 배포 근거 강함</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2611.25134'>GEMS: Generation and Experience Memory for Subgoal-Guided Long-Horizon World Model Planning</a></td><td>70</td><td>8</td><td>World Model</td><td>생성 subgoal과 latent experience memory를 거리 게이트로 선택해 frozen world model의 long-horizon planning을 개선함. Cube 92.8%, Push-T 68.4%, Meta-World 54.1%로 baseline보다 7.3~24.0퍼센트포인트 높음. 시뮬레이션 한정임</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2611.25215'>Bridging vision-language reasoning and learned control for legged navigation in the wild</a></td><td>70</td><td>8</td><td>Navigation</td><td>VLM 위험 지도로 RL locomotion·local planning을 조건화해 km 단위 실외 보행 navigation을 함. 실로봇 검증이 강하나 구조는 모듈 결합임</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2611.25415'>Stuck in Place: Stall Diagnosis and Remedies for JEPA Planners</a></td><td>70</td><td>8</td><td>World Model</td><td>JEPA planner 실패의 96% 이상이 정체(stall)임을 계획 루프에서 직접 보여 TTA의 원인 가정을 반박함. 진단 중심의 새 관점이나 pushing 과제에 한정됨</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2611.25946'>Point Dynamics as Proxy for Robotic World Models</a></td><td>68</td><td>10</td><td>World Model</td><td>3D point dynamics를 proxy로 dynamics와 rendering을 분리해 DROID에서 물체 운동 오차를 8.6% 줄이고 실제 양팔 로봇에서 8.1% 개선함. 조작 world model 핵심 문제에 부합하나 개선폭은 보통임</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2611.26341'>Reasoning on Call: Efficient Agentic Robot Control for Long-Horizon Robot Manipulation</a></td><td>68</td><td>9</td><td>VLA</td><td>event-triggered agent 검토로 실행 복구와 계획 수정을 나눠 호출 비용을 줄임. RMBench에서 성공률 24.0퍼센트포인트 오르고 토큰 65.3% 감소하며 실로봇 3개 과제 검증이 있음</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2611.26434'>HumanCOIN: A 12,500-Hour Dataset for Human Intent in Egocentric Manipulation</a></td><td>68</td><td>8</td><td>Manipulation</td><td>12,500시간 egocentric 조작에 gaze·EMG·EEG intent 층을 붙인 대규모 데이터셋임. 정책 학습에서의 효과 검증은 초록에 없어 데이터셋 기여로 평가함</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2611.26405'>TacInno: Teaching Vision-Language-Action Models the Contact Dynamics Beyond Vision and Action</a></td><td>68</td><td>8</td><td>VLA</td><td>시각·행동으로 설명되지 않는 촉각 변화만 학습 목표로 삼는 TacInno임. 실로봇 4개 과제 70.5%로 visuo-tactile baseline보다 9.0퍼센트포인트 높고 배포 시 추가 module이 없음</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2611.25500'>PRIO: Pre-trained Representation for Interactive Objects in 4D Worlds</a></td><td>68</td><td>7</td><td>World Model</td><td>PRIO가 정적 형상에서 단일 forward로 configuration space를 예측해 Lagrangian 동역학으로 상호작용 가능하게 함. 4D 생성보다 빠르고 robot manipulation 시연 있음</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2611.25179'>Phantom Success, Silent Failure: Auditing the Success Checkers of Simulated Manipulation Benchmarks</a></td><td>66</td><td>8</td><td>Manipulation</td><td>LLM 기반 SimAudit으로 RoboTwin 2.0 등 3개 benchmark success checker에서 61개 결함(거짓 성공 40, 거짓 실패 21)을 찾음. 평가 신뢰성 문제를 실증함</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2611.25320'>Improving Imitation Policies for Multi-Phase Tasks through Residual Learning Allocation</a></td><td>66</td><td>8</td><td>RL</td><td>multi-phase 과제에서 completion gain으로 residual RL 예산을 phase별 배분함. 양팔 조립 시뮬레이션에서 release 단계 완료율 16.9% 개선이나 실로봇 없음</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2611.25199'>VG-Steer: Visual-Geometric Policy Steering from In-Context Aligned Abstractions</a></td><td>66</td><td>8</td><td>Manipulation</td><td>VLM과 기하 거리쌍으로 성공 rollout의 움직임을 옮겨 frozen policy를 보정함. 실로봇에서 학습 범위 밖 케이블 배치 성공률이 2배 넘게 오르나 과제 수는 확인 불가함</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2611.25366'>Learning to Move from and for Manipulation Policies: Spatializing Latent Action Representations for Goal-Pose-Free Mobile Manipulation</a></td><td>66</td><td>8</td><td>Manipulation</td><td>사전학습된 manipulation policy의 hidden representation으로 pose별 성공 가능성을 학습해 goal pose 없는 이동을 함. RoboCasa 8개 과제 성공률 26.5%에서 47.0%로 오르나 시뮬레이션 위주임</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2611.25683'>TipDex-VTLA: Learning When to Refine Actions with Touch for Dexterous Manipulation</a></td><td>66</td><td>8</td><td>Manipulation</td><td>시각 신뢰도와 촉각 예측 불일치로 행동 refinement 시점을 조절함. 실로봇 4개 과제에서 낯선 조명 아래 73.8%를 유지해 tactile 주제와 맞음</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2611.25777'>Hindsight Self-Distillation: Teaching Robots to Act from the Present</a></td><td>66</td><td>8</td><td>Imitation</td><td>미래 프레임을 teacher에게 보여 현재 관측에서 뽑을 정보를 증류함. LIBERO 98.5%, RoboTwin 2.0 92.3%로 높으나 비교 baseline 확인 필요함</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2611.26414'>ZeroVLN: Learning to Navigate without Supervised Fine-Tuning of the VLM Brain</a></td><td>66</td><td>8</td><td>Navigation/VLN</td><td>VLM brain을 SFT 없이 tool-calling과 closed-loop RL로 학습해 VLN-CE에서 SFT 기반을 능가함. 일반 능력 보존이 장점이며 수치는 초록에서 확인 불가함</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2611.25553'>TwoPass: Draft-Guided Few-Step Video Prediction for Robotic Manipulation</a></td><td>64</td><td>9</td><td>World Model</td><td>TwoPass가 자기 draft로 4 NFE만에 Bridge/Language Table에서 SOTA 행동 조건 비디오 예측을 달성함(기존 50-59 NFE). 실로봇 평가는 없음</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2611.25400'>Dune: A Zeroth-Order Optimizer with Time-Conditioned Historical Error Regression for VLA Test-Time Adaptation</a></td><td>64</td><td>8</td><td>VLA</td><td>zeroth-order TTA의 장기 불안정을 과거 오차 회귀로 안정화함. LIBERO와 실로봇에서 낮은 메모리로 개선하나 수치는 초록에서 확인 불가함</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2611.26105'>PhysVAM: Physics-oriented Future Value Action Model for Dynamic Object Manipulation</a></td><td>64</td><td>8</td><td>Manipulation</td><td>미래 task value를 예측해 동적 물체 조작 행동을 유도함. 시뮬레이션과 실로봇 모두 가장 강한 baseline보다 약 27퍼센트포인트 높음</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2611.25667'>CauSyncVLA: Causal Latent World Modeling for Asynchronous Robot Control</a></td><td>62</td><td>8</td><td>VLA</td><td>인과 latent world model로 비동기 VLA의 오래된 memory와 chunk 단절을 보정함. LIBERO-10 93.8%에 처리량 5.04배이나 시뮬레이션 한정임</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2611.26161'>One View, One Action: Spatially Generalizable VLAs through Observation-Aligned Experts and Cross Graph Consistency</a></td><td>62</td><td>8</td><td>VLA</td><td>각 view의 카메라 프레임에서 행동을 예측해 multi-view VLA의 시점 일반화를 개선함. 실로봇 공간 shift에서 π0.5 28.3%에서 58.3%로 오르나 과제 3개뿐임</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2611.26385'>Beyond the Sink Interpretation: Radial Attention in Flow-Based VLA Policies</a></td><td>62</td><td>8</td><td>VLA</td><td>radial action sink 해석을 한 checkpoint에서 마스킹·값 치환으로 반증하고 실제 기능을 분석함. 통계 검정을 갖춘 엄밀한 해석 연구이나 checkpoint 하나에 한정됨</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2611.25719'>SteerTrace: Tracing How Target Attacks Steer World Action Models</a></td><td>62</td><td>7</td><td>World Model</td><td>SteerTrace가 8개 WAM(LIBERO, RoboTwin)에서 단일 perturbation으로 성공률을 거의 0으로 만들고 내부 영향 경로를 추적함. WAM 취약성 분석으로 가치 있음</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2611.25927'>Fast-JEPA: Advancing the Success-Latency Frontier for Latent World Models</a></td><td>62</td><td>7</td><td>World Model</td><td>전체 후보 결과를 직접 예측해 latent world model planning의 지연을 줄임. INTACT 대비 2.41배 빠르고 성공률 96.5%이나 PushT 등 단순 과제 위주임</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2611.26420'>Awaken-HI: Scaling Humanoid Intelligence with Whole-Body Human Experience</a></td><td>62</td><td>7</td><td>Humanoid</td><td>50,000시간 egocentric 영상과 전신 동작 데이터로 humanoid VLA를 사전학습함. 실로봇 평균 93.75%이고 GR00T·π0.5보다 높으나 데이터 scale 의존이 큼임</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2611.25671'>LATER: Learning Action-Conditioned Temporal Evidence Retrieval for Predictive World Models</a></td><td>62</td><td>7</td><td>World Model</td><td>action-conditioned memory 검색으로 PushT 후반 예측을 개선하는 world model임. memory 관점이 새로우나 소규모 시뮬레이션뿐이고 실로봇 없음</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2611.25849'>EgoWitness: Benchmarking Instance-Level Spatial Memory and Reasoning in Egocentric Video Streams</a></td><td>62</td><td>6</td><td>Embodied AI</td><td>EgoWitness가 324시간 egocentric 영상으로 instance 단위 공간 memory를 평가하고 SFT+GRPO agent로 23.6%에서 72.7%로 올림. robot memory 관점에서 의미 있으나 인간 영상임</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2611.26389'>ViDecide: Teaching Video Diffusion Models to Reason and Plan Step by Step</a></td><td>62</td><td>5</td><td>Video</td><td>video diffusion을 결정 단위로 학습하고 실패를 자기 성공 continuation으로 교정하는 CFT를 제안함. 다단계 로봇 planning 벤치마크 포함 평균 성공률 83.8%로 강하나 실로봇 검증 확인 불가함</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2611.25695'>DMT-Attack: Diffusion-Prior Texture Search for Closed-Loop Vision-Language-Action Policies</a></td><td>60</td><td>8</td><td>VLA</td><td>diffusion prior 텍스처로 pi0.5·OpenVLA-OFT 공격 성공률 57.9%(기존 44.7%), 탐지율 낮음. VLA 취약성 분석으로 관련 높으나 공격 연구임</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2611.25279'>Accord: Universal Online Metric Localization and Dense Mapping from one Camera and an IMU</a></td><td>60</td><td>7</td><td>3D Vision</td><td>단안 카메라+IMU로 metric 밀집 지도와 localization을 online으로 수행함. 로봇 SLAM에 실용적임</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2611.26516'>Plan4D: Generative Plannable 4D Worlds</a></td><td>60</td><td>6</td><td>World Model</td><td>Depth Anything 3와 비디오 생성기를 결합해 RGB와 4D geometry를 함께 예측하는 plannable world model임. 액션이 텍스트 지정이고 로봇 정책 평가는 불명확함</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2611.26177'>SpatialScout-V2: Can VLM Agents Actively Explore Real-World 3D Scenes and Localize Objects?</a></td><td>58</td><td>8</td><td>Embodied AI</td><td>실내 100곳 3,171개 물체를 능동 탐색해 위치를 추정하는 benchmark로 최고 모델도 mIoU 22.5%에 그침. active perception 과제로 적합하나 방법 기여 없는 benchmark임</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2611.26239'>Teaching Vision-Language-Action Models to Stop Safely</a></td><td>58</td><td>8</td><td>VLA</td><td>VLA가 금지 과제를 안전하게 멈추도록 fallback 목표를 학습함. LIBERO에서 takeover 후 금지 과제 성공이 1.3%로 줄고 물리 사고 없으나 시뮬레이션 한정임</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2611.25336'>MoRE: Mixture-of-Experts for Multi-Physics Robotic World Models</a></td><td>58</td><td>7</td><td>World Model</td><td>MoE로 이질적 물리 동역학을 다루는 3D robotic world model임. 방법은 타당하나 module 확장 성격임</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2611.25413'>WAMotor: Accelerating World Action Models via Speculative Inference under Dual Nonuniform Denoising Dynamics</a></td><td>58</td><td>7</td><td>World Model</td><td>world action model에 speculative inference를 넣어 가속함. 효율화 엔지니어링 성격이 강함</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2611.25587'>Cognitive-Horizon Action Chunking: Memory-Guided Adaptive Reasoning for Embodied Navigation</a></td><td>58</td><td>7</td><td>Navigation</td><td>memory 기반으로 VLM 호출 횟수를 줄이는 training-free chunking임. R2R-CE에서 성공률이 10.82포인트 내려 대가가 있고 실로봇 4개 과제는 개선됨</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2611.26103'>UniVEP: Unifying Velocity and Endpoint Prediction for Robot Manipulation</a></td><td>58</td><td>7</td><td>Imitation</td><td>velocity와 endpoint 예측을 노이즈 구간별로 통합함. RoboTwin에서 1회 추론이 16회 baseline을 넘고 지연 77.1% 감소하나 학습 목표 변경 수준임</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2611.26366'>World Models Favor Learned Priors over Visual Evidence</a></td><td>58</td><td>6</td><td>World Model</td><td>world model이 시각 증거 대신 학습 prior를 따르는 편향을 TailWorld로 측정하고 RIFT로 줄임. 문제 정의는 좋으나 합성 환경 중심임</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2611.25626'>Physical Laws without Physics Loss? Probing Learned Dynamics in Video World Models through Forced Response</a></td><td>58</td><td>5</td><td>World Model</td><td>6개 I2V 모델이 물리 loss 없이 비선형 강제 응답까지 학습했는지 3단 탐침으로 진단함. 설계가 엄밀하나 로봇 직접 연결은 간접적임</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2611.25387'>TuringSpace: Grounding Spatial Intelligence in Action with Interactive CAPTCHAs</a></td><td>58</td><td>5</td><td>Embodied AI</td><td>인터랙티브 CAPTCHA 125종으로 MLLM의 공간 추론과 행동 후 교정을 측정하고 fine-tuning 시 VSI-Bench 9.9점 상승을 보임. 로봇 행동은 아니나 embodied 공간 추론과 연결됨</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2611.26596'>PGX: Physically Grounded Execution for Long-Horizon Humanoid Loco-Manipulation</a></td><td>56</td><td>8</td><td>VLA</td><td>물리 기반 실행으로 humanoid long-horizon loco-manipulation을 함. 과제 어려움은 높으나 증거 확인 필요함</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2611.26196'>EmbodyAgent: Post-Training Embodied VLM Agents via Distillation, SFT, and RL</a></td><td>56</td><td>7</td><td>Embodied AI</td><td>증류·SFT·RL로 9B VLM을 code-as-policy agent로 후처리함. LIBERO Spatial 10개 과제에서 0/100에서 84/100으로 오르나 단일 suite 평가임</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2611.26376'>Alignment Drives Reuse: Learning Generalizable Robot-Use Agents from Heterogeneous Experience</a></td><td>56</td><td>7</td><td>Embodied AI</td><td>이질 경험에서 일반화되는 robot-use agent를 학습함. 정렬 주장은 흥미로우나 증거 확인 필요함</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2611.26565'>PhyDEX: A Benchmark for Physical Reasoning in Vision-Language-Action Models via Dynamic Extrinsic Dexterity</a></td><td>56</td><td>7</td><td>Benchmark</td><td>던지기로 물리 추론을 평가하는 벤치마크임. 세 VLA 모두 성공률 3% 미만이고 물리 속성을 주면 2배 가까이 올라 physical blindness를 보임</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2611.26313'>Actor-Predictor Architecture for Reinforcement Learning with Formal Specification Objectives</a></td><td>56</td><td>6</td><td>RL</td><td>automaton 없이 logic progress를 predictor로 학습해 LTL과 비정규 명세 모두 처리함. Isaac Lab 로봇 과제 포함하나 실로봇 없음</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2611.25210'>Recurrent Vision Language Models Solve the Shell Game</a></td><td>56</td><td>4</td><td>Video</td><td>RecurrentVLM이 VET-Bench 100%, 50-swap 99%로 shell game을 풀고 길이 일반화도 보임. 상태 추적 원리 분석은 좋으나 합성 과제 한정임</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2611.25632'>What One Sample Cannot See: Why Fewer Denoising Steps Can Score Higher on Physics Benchmarks</a></td><td>56</td><td>4</td><td>World Model</td><td>Physics-IQ가 분산 감소를 보상하는 문제를 분해로 증명하고 Kernel Physics-IQ를 제안함. world model 평가 통찰이 좋으나 범위는 비디오 생성 평가에 한정됨</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2611.25398'>RefreshGrad: An Online Adaptive Data-sampling Method for Diffusion-based Visuomotor Learning</a></td><td>55</td><td>7</td><td>Imitation</td><td>diffusion visuomotor 학습의 온라인 적응 데이터 샘플링임. 작은 학습 기법 수준임</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2611.25575'>Trajectory-Calibrated Merging of Embodied Policies</a></td><td>55</td><td>7</td><td>VLA</td><td>궤적 보정 기반 embodied policy 병합임. 흥미로우나 model merging 확장 성격임</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2611.26046'>Agentic Scaling of Embodied Tasks in Simulation for Synthetic Data Collection and Policy Evaluation</a></td><td>55</td><td>7</td><td>Embodied AI</td><td>agent 기반 시뮬레이션 과제 확장으로 합성 데이터와 평가를 함. 데이터 확장 도구 성격임</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2611.26444'>Mind2Act World: A Diagnostic Benchmark for Embodied Mind, Physical Action, and Mind-Action Composition in Robotic Manipulation</a></td><td>55</td><td>7</td><td>Benchmark</td><td>Mind·Act·Mind2Act 세 시점으로 실패 원인을 분해하는 진단 벤치마크임. 최고 agent가 Mind 52.7%, Act 39.0%지만 조합은 12.0%로 조합 문제를 드러냄임</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2611.26613'>AgentRoboCritic: Understanding the Capability of Frontier Agents on Direct Robot Control</a></td><td>55</td><td>7</td><td>Embodied AI</td><td>frontier agent의 직접 로봇 제어 능력 평가임. 평가 위주임</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2611.25567'>Online Mistake Detection in Instruction-Conditioned Procedural Video</a></td><td>55</td><td>6</td><td>Video</td><td>지시문 조건 절차 영상에서 online 실수 탐지를 함. failure detection과 개념적으로 이어지나 인간 영상 중심임</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2611.25865'>Thinking in Streams: Proactive Spatial Reasoning with Vision-Language Models</a></td><td>55</td><td>6</td><td>Embodied AI</td><td>스트리밍 영상에서 공간 조건 성립 시점을 능동 감지하는 proactive spatial reasoning임. embodied spatial reasoning에 부합함</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2611.25728'>What&#x27;s in the box? Revealing Object Layouts Inside Opaque Boxes via Contactless Vibration Excitation and Sensing</a></td><td>55</td><td>5</td><td>Perception</td><td>표면 진동 관측으로 불투명 상자 안 물체 배치를 추정함. 새로운 sensing 문제 설정이나 로봇 통합은 약함</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2611.26433'>AdaPixFlow: Learning Continuous-Time 3D Dynamics Across Scenes from Sparse Multi-view Observations</a></td><td>55</td><td>4</td><td>3D Vision</td><td>sparse multi-view에서 scene 간 연속시간 3D dynamics operator 학습으로 4D 표현 관점에서 관련 있음</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2611.24963'>Physics of Language Models: Part 4.2, Canon Layers at Scale where Synthetic Pretraining Resonates in Reality</a></td><td>55</td><td>0</td><td>NLP</td><td>64회 from-scratch pretraining으로 구조 차이를 측정한 대규모 연구임. 증거는 강하나 로봇 무관함</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2611.25925'>SpatialMem: Building Quantitative Spatial Reasoning Agents with Hierarchical Memory</a></td><td>54</td><td>6</td><td>Embodied AI</td><td>SpatialMem이 2단 memory로 도구 조합 경험을 축적해 MetricBench에서 VLM baseline 대비 32% 향상함. memory 효과 9.1% 증거가 있으나 로봇 평가 없음</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2611.25963'>MorphTwin: Enriching Deformable Material Responses from Videos for Morphable and Interactive Physical Twins</a></td><td>54</td><td>5</td><td>3D Vision</td><td>MorphTwin이 PhysTwin 대비 Poisson 비 오차 75.8% 감소, 실세계 추적 오차 최대 14.4% 감소를 보임. 변형체 physical twin으로 로봇 시뮬레이션에 간접 유용함</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2611.25474'>TuringPAI: A Foundation for On-Device Physical AI</a></td><td>52</td><td>8</td><td>Embodied AI</td><td>LIBERO 96.8%, 12Hz Orin-X 주행 구동 등 on-device 기술 보고서임. 로봇 관련성은 높으나 novelty는 구조 조합이며 실로봇 증거 없음</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2611.25460'>LoongForge-Embodied: A Unified Framework for Training Heterogeneous Embodied Models</a></td><td>52</td><td>8</td><td>VLA</td><td>VLA와 WAM 학습 처리량 1.47~4.38배, 평가 4.1~23.2배 가속함. 시스템 엔지니어링 중심이라 novelty 제한적이나 실용성 있음</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2611.25417'>MIR-Depth: Multi-Range Refinement for Single-View RGB-D Depth Completion of Transparent Objects</a></td><td>52</td><td>7</td><td>Manipulation</td><td>투명 물체 depth completion이 5개 데이터셋에서 baseline보다 낮은 오차를 보이고 실로봇 6-DoF grasp 확인도 있음. 모듈 개선 성격은 남음</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2611.26218'>MixReact: Physics-Based Reactive Humanoid Control from Multimodal Cues via a Discrete-Continuous Mixture of Transformers</a></td><td>52</td><td>7</td><td>Embodied AI</td><td>다중 모달 단서에 반응하는 physics 기반 humanoid 제어임. 시뮬레이션 humanoid 계열이며 실로봇 증거는 없음</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2611.25679'>LeCompass: Task-Level Execution through State-Indexed Interfaces</a></td><td>52</td><td>7</td><td>World Model</td><td>state-indexed 인터페이스로 JEPA 기반 task 실행을 함. 아이디어는 있으나 근거 확인 필요함</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2611.25778'>ECHO: In-Context Behavior foundation model for Humanoid Whole-Body Control</a></td><td>52</td><td>7</td><td>Humanoid</td><td>in-context behavior foundation model로 humanoid 전신 제어를 함. 기존 BFM 개선 성격임</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2611.26056'>Less Than Meets the Eye: Action-Set Identifiability and Principled Abstention for 3D Physical Geometry</a></td><td>52</td><td>5</td><td>3D Vision</td><td>Intervene3D가 카메라 이동으로 거울·디스플레이 가설을 가르고 불확실하면 abstain함. 문제 정식화가 좋으나 합성 benchmark 중심이고 로봇 연결은 약함</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2611.26048'>AGE-Capture: Autonomous, General, and Efficient UAV Capture for High-Fidelity Scene Reconstruction</a></td><td>52</td><td>5</td><td>Active Perception</td><td>UAV 장면 재구성용 자율 촬영 시점 획득임. NBV 성격이나 UAV 도메인임</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2611.26211'>SpecWM: Turning Verification into Refinement for Streaming World Models</a></td><td>52</td><td>4</td><td>World Model</td><td>SpecWM이 latent velocity로 검증과 refinement를 겸해 1.63배 가속하며 NavScore 75.99를 85.63으로 올림. 추론 효율 아이디어이나 로봇 평가 없음</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2611.26493'>SGAR: Feed-Forward 3D Reconstruction via Sparse Geometry-Guided Attention</a></td><td>52</td><td>4</td><td>3D Vision</td><td>sparse attention으로 feed-forward 3D 재구성 확장성을 높인 효율 개선임</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2611.26603'>Depth Pro 2: Sharp and Temporally Consistent Metric Monocular Depth</a></td><td>52</td><td>4</td><td>3D Vision</td><td>metric depth의 시간 일관성과 경계 선명도를 함께 개선해 로봇 perception에 유용하나 incremental임</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2611.25594'>Bradley-Terry Training Can Distort Outcome Probabilities of Initially Accurate Language World Models</a></td><td>52</td><td>4</td><td>LG</td><td>Bradley-Terry 학습이 언어 world model의 결과 확률을 왜곡함을 시뮬레이션 robot push에서 보임. 분석은 흥미로우나 단순 설정임</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2611.25543'>Efficient Multimodal Agents for Auditing 3D Worlds</a></td><td>52</td><td>4</td><td>Embodied AI</td><td>소형 VLM explorer 여럿과 frontier reviewer로 3D 세계 glitch를 감사해 WorldAuditBench 55.9%, 비용 1/4 미만임. 실제 스캔 embodied QA도 시험했으나 로봇 제어는 아님</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2611.26024'>ForeSeek: Foresight-Driven Reasoning for Long-Form Video Understanding</a></td><td>52</td><td>3</td><td>Video</td><td>long video 이해에 foresight 기반 추론을 도입함. video 이해 방법이나 로봇 직접 연결 약함</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2611.25722'>DACA: Dual-Anchor Collaborative Agent for Zero-Shot 3D Visual Grounding</a></td><td>50</td><td>6</td><td>Embodied AI</td><td>zero-shot 3D visual grounding agent임. embodied 기반 능력이나 benchmark 개선 성격이 강함</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2611.25801'>Fast and Accurate Body Estimation in Pixels, World Space and Scenes</a></td><td>50</td><td>6</td><td>3D Vision</td><td>FAB가 SAM 3D Body 대비 4.6배 빠른 인체 추정과 G1 humanoid retargeting을 제공함. 파이프라인 엔지니어링 성격이 강함</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2611.25675'>Minimal Memory for Correctable Visual Continuation</a></td><td>50</td><td>5</td><td>World Model</td><td>visual continuation에서 수정 가능한 memory의 비트 하한과 CAM을 제시함. 이론이 흥미로우나 신경망 실험이 제한적이고 로봇 평가 없음</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2611.26615'>ScaleWorld: High-Resolution World Generation through Shared Prediction and Refinement</a></td><td>50</td><td>5</td><td>World Model</td><td>고해상도 world model 생성의 계산 효율 개선으로 로봇 의사결정 연결은 약함</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2611.25061'>Infer3D: Inverse Generative Modeling Enables Robust 3D Reconstruction</a></td><td>50</td><td>3</td><td>3D Vision</td><td>inverse generative modeling과 adaptive test-time compute로 OOD 3D 복원을 개선함. 아이디어는 좋으나 로봇 평가 없음</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2611.25742'>Goal-Guided Reinforcement Learning via Fine-Tuning Vision-Language Models</a></td><td>50</td><td>3</td><td>RL</td><td>VLM에 목표 선호 정렬(KLTDPO)로 Craftax RL 탐험을 돕는 방법임. 게임 환경뿐이라 로봇 연결 약함</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2611.25989'>Policy Improvement-Guided Replay for Continual Reinforcement Learning</a></td><td>50</td><td>3</td><td>RL</td><td>policy 개선 관점의 replay 선택(CoLiR)으로 VLM의 continual RL 망각을 줄임. 로봇이 아닌 VLM 추론 과제임</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2611.25138'>Old-School Planners Drive (Sometimes) Better Than Learned Ones</a></td><td>50</td><td>3</td><td>Navigation</td><td>교과서식 planner 16종이 UniAD 학습 planner보다 HUGSIM에서 더 높은 점수를 얻음을 보이는 실증 비교임. novelty는 낮으나 증거 설계가 엄밀함</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2611.26627'>RL Post-Training in Diffusion Transformers Is Activation Steering</a></td><td>50</td><td>1</td><td>Generative</td><td>RL post-training 이득의 90% 이상이 prompt 무관한 고정 steering vector로 복원된다는 흥미로운 분석임. 이미지·비디오 생성 한정이라 로봇 관련성 낮음</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2611.25530'>Keystone: Judging Previews at Key Steps for Test-Time Search in Diffusion Models</a></td><td>50</td><td>1</td><td>Generative</td><td>typed question으로 preview를 판정해 GenEval에서 best-of-8을 절반 미만 연산으로 능가함. 이미지 생성 한정이나 test-time search 설계가 새로움</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2611.25011'>Near-Quadratic Sample Compression for All VC Classes</a></td><td>50</td><td>0</td><td>LG</td><td>sample compression 약한 추측을 O(d^2 log^2 d) 크기로 증명한 학습이론 결과로 중요하나 로봇과 무관함</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2611.25819'>SCCV-6D: Sparse Canonical Coordinate Voting for Holistic Multi-View RGB-D 6D Pose Estimation in Robotic Bin Picking</a></td><td>48</td><td>7</td><td>Manipulation</td><td>bin picking용 다시점 RGB-D 6D pose 투표 방식임. 산업 로봇에 실용적이나 pose 추정 개선 수준임</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2611.26293'>LocoMuJoCo: A Comprehensive Imitation Learning Benchmark for Whole-Body Control</a></td><td>48</td><td>7</td><td>Imitation</td><td>전신 제어 IL 벤치마크 라이브러리임. 도구로 유용하나 방법 novelty는 없음</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2611.26519'>ACE-Brain-0.7: Learning Execution-Grounded Reasoning for Embodied Agents</a></td><td>48</td><td>7</td><td>Embodied AI</td><td>실행 기반 추론을 하는 9B embodied VLM임. 모델 공개형 scale 성격이 있음</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2611.26165'>StreamEgo: Streaming Exocentric-to-Egocentric Video Generation</a></td><td>48</td><td>6</td><td>Video</td><td>StreamEgo가 24.3 FPS로 exo2ego 영상을 생성함. 로봇 demonstration 합성을 언급하나 로봇 실험은 없음</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2611.25788'>Collision-Free Is Not Enough: Passage-Conditioned Navigation for Wheeled-Legged Robots</a></td><td>48</td><td>6</td><td>Navigation</td><td>교육 시연의 진입 방향을 기억해 통로 진입을 강제하는 training-free navigation임. 대회 실로봇 6회 완주로 실용성은 있으나 학습 기여는 작음</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2611.25197'>From Self-Play RL to Constrained Control: Distilling DiffMPC Students with DAgger</a></td><td>48</td><td>5</td><td>RL</td><td>self-play RL 주행 policy를 DiffMPC student로 DAgger 증류함. 제약 보장은 장점이나 주행 도메인이고 참신성 보통임</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2611.25166'>CoRelate: Coordinated Human-Object Motion Synthesis through Interaction Relations</a></td><td>48</td><td>4</td><td>Generative</td><td>상호작용 관계 기반 human-object 동작 합성임. 접촉 유지 문제 설정은 괜찮으나 로봇 직접 적용은 없음</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2611.25802'>World-delta: Continually Integrating Observations for Incremental 3D Scene Generation</a></td><td>48</td><td>4</td><td>3D Vision</td><td>새 관측이 들어올 때 3D 장면을 점진적으로 확장·수정하는 생성 방식임. persistent 장면 표현 측면은 있으나 로봇 평가 없음</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2611.25172'>MV-JEPA: Post-Training Video Encoders for Cross-View Understanding</a></td><td>48</td><td>3</td><td>Video</td><td>9천 step 단일 GPU post-training으로 cross-view 대응을 강화함. 효율적이나 로봇 연결 약하고 개선폭이 검색 지표 위주임</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2611.25408'>FG-GraphBench: Benchmarking and Enhancing Fine-Grained Visual Understanding with Multimodal Scene Graphs</a></td><td>48</td><td>3</td><td>Multimodal</td><td>scene graph로 MLLM 세밀 시각 이해를 평가·향상하나 로봇 연결은 간접적임</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2611.26504'>Grid Cells as Spectral Successor Features: A Reusable Basis for Continual Reinforcement Learning</a></td><td>48</td><td>3</td><td>RL</td><td>grid cell 고유벡터를 successor feature 기저로 써 목표 변경에 선형 회귀로 적응함. 2목표 gridworld뿐이라 규모가 작음</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2611.25005'>Inhabitant: An Agent Framework for Long-Horizon Human-Scene Interaction with Spatial Control and Quantitative Feedback</a></td><td>48</td><td>3</td><td>Embodied AI</td><td>training-free LLM agent가 위치·경로·자세 제어와 정량 피드백으로 장기 인간-장면 상호작용을 생성함. 가상 인체 동작이며 로봇 실험은 없음</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2611.25670'>Efficient Latent Reasoning for Vision-Language Model via Dynamics-Aware Quantization and Distillation</a></td><td>48</td><td>3</td><td>VLM</td><td>VLM latent CoT를 양자화와 distillation으로 효율화함. 효율 추론이나 로봇 검증 없음</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2611.25123'>Forget Freely, Grep Later: Lossless, Index-Free Memory for Long-Horizon LLM Agents</a></td><td>48</td><td>2</td><td>Agent</td><td>전체 이력을 plain-text log로 두고 grep으로 회상하는 agent memory임. ContextBench 95-97%로 강하나 텍스트 agent 한정임</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2611.25191'>Blind Spots Travel, Knowledge Stays Home: What RL Inherits from an LLM Judge</a></td><td>48</td><td>0</td><td>NLP</td><td>814회 RL 실험으로 LLM judge가 상속시키는 편향을 보임. 기여는 분명하나 로봇 무관함</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2611.25513'>Mesh-Free Keypoint Learning for Category-Level 6D Object Pose Estimation</a></td><td>47</td><td>6</td><td>3D Vision</td><td>mesh 없이 category-level 6D pose 키포인트를 학습함. manipulation 하위 인식이나 pose 추정 개선 수준임</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2611.25604'>PAD: Policy-Aware Data Valuation for Autonomous Driving</a></td><td>47</td><td>5</td><td>Autonomous Driving</td><td>주행 학습용 policy 인지 data valuation임. 데이터 선택 아이디어는 좋으나 주행 도메인임</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2611.25889'>EvoMem: Self-Evolving Skills for Time-Aware Long Video Memory Agents</a></td><td>47</td><td>4</td><td>Video</td><td>장편 영상 memory agent의 self-evolving skill임. memory 요소는 있으나 로봇이 아닌 영상 QA임</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2611.26072'>DfD-GS: Defocus Image Prior for Metric-Scale Single-View Depth Estimation and View Synthesis</a></td><td>47</td><td>4</td><td>3D Vision</td><td>defocus 단서로 단안 metric depth와 view synthesis를 함. 단안 metric 문제에 새 단서를 쓰나 로봇 평가 없음</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2611.25265'>Real Cameras are Radiometric</a></td><td>47</td><td>3</td><td>3D Vision</td><td>기하 카메라를 radiometric 모델로 확장한 이론적 기여임. 로봇 직접 활용은 제한적임</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2611.26054'>Reference-Free Humanoid Skateboarding via Termination-Shaped Reinforcement Learning</a></td><td>46</td><td>5</td><td>RL</td><td>termination 설계로 reference 없는 humanoid 스케이트보드 RL을 함. 흥미로운 과제이나 locomotion 한정임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2611.26294'>BADAS-3.0: Real-Time Driving Perception and Planning from One Camera</a></td><td>46</td><td>4</td><td>Embodied AI</td><td>BADAS-3.0이 단일 카메라 50ms 미만으로 5개 궤적 benchmark에서 minADE 44% 감소를 보임. 이득이 학습 안 한 카메라 rig에서 나온다고 저자가 밝힘. 주행 응용임</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2611.25385'>Drifting, Discriminating, and Directioning for Action Coordination in Higher-dimensional Action Space</a></td><td>46</td><td>4</td><td>RL</td><td>drifting model에 action coordination을 학습시키는 RL policy로 locomotion 3개 과제에서 sample efficiency가 오름. 시뮬레이션 한정임</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2611.25340'>SceneAnything: Agentic Reconstruction of Large-Scale Mesh Scenes from a Single Video</a></td><td>46</td><td>3</td><td>3D Vision</td><td>agent가 프로그램을 써서 단일 영상에서 대규모 mesh 장면을 복원함. 편집 가능한 장면 표현은 흥미로우나 로봇 평가는 없음</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2611.26252'>The Stability Gap in Continual Reinforcement Learning</a></td><td>46</td><td>3</td><td>RL</td><td>continual RL에서 신규 과제 도입 직후 이전 과제 성능이 떨어지는 stability gap을 간단한 벤치마크로 보임. 장난감 수준 설정임</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2611.25067'>Mapping the Wind to Find the Source: Online Physics-Informed Gas Source Localization with Mobile Robots</a></td><td>45</td><td>5</td><td>Navigation</td><td>이동 로봇이 풍향장을 online 복원하고 belief map으로 informative path planning을 하는 가스 근원 탐색임. 실내 실험이 있으나 적용 범위가 좁음</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2611.26269'>Tracking Objects Through Assembly and Decomposition</a></td><td>45</td><td>4</td><td>Video</td><td>조립·분해 중 물체를 추적하는 문제 설정임. 상태 변화 추적은 manipulation과 닿으나 로봇 평가는 약함</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2611.25958'>Learning optimal gaits and styles for terrain-adaptive quadruped locomotion</a></td><td>45</td><td>4</td><td>Locomotion</td><td>지형 적응 사족 보행 gait와 style을 학습함. 보행 도메인이고 novelty 보통임</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2611.25568'>AeroBelief: Budgeted First-Action Verification for Evidence-Guided Aerial Sensing</a></td><td>45</td><td>4</td><td>Embodied AI</td><td>UAV closed-loop 960회 실행에서 world model 질의를 91.81% 줄이고 완료율 75.42% 유지함. 능동 센싱 관련하나 도메인 특수함</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2611.26040'>Streaming-AAA: Streaming AAA Game Video Generation at High Resolution, High Frame Rate, and Low Latency</a></td><td>45</td><td>3</td><td>World Model</td><td>고해상도 고프레임 스트리밍 게임 영상 생성임. 상호작용 world model 계열이나 게임 도메인이며 엔지니어링 비중 큼</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2611.25208'>ϕTD: Distributional Reinforcement Learning using Characteristic Functions</a></td><td>45</td><td>3</td><td>RL</td><td>characteristic function 기반 distributional RL로 RL 방법론 기여가 있으나 로봇 검증 없음</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2611.26084'>RL Can Only Reinforce What It Sees Succeed</a></td><td>45</td><td>1</td><td>RL</td><td>outcome-reward RL이 사전지식과 관측 사이 균형을 바꾸는 분석으로 RL 이해에 흥미 있으나 LM 퍼즐뿐임</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2611.26347'>OffBeat: Multicoset Sampling for 4D Capture Beyond the Camera Frame Rate</a></td><td>44</td><td>3</td><td>3D Vision</td><td>OffBeat가 카메라 트리거 시차 설계로 동적 영역 PSNR을 3.04dB 올림. 센싱 설계 아이디어는 좋으나 로봇 연결 약함</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2611.26380'>EgoCaptioner: Towards Comprehensive and Fine-Grained Egocentric Video Captioning</a></td><td>44</td><td>3</td><td>Video</td><td>egocentric 비디오 캡셔닝 개선으로 embodied 데이터에 간접 연결되나 증거 평범함</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2611.25589'>GraF-VTA: Neuro-Symbolic Trajectory Generation from Vision and Temporal Logic via Graph-Based Fusion</a></td><td>42</td><td>5</td><td>Planning</td><td>비전과 STL을 그래프로 융합해 궤적을 생성함. neuro-symbolic이나 증거 약함</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2611.25866'>From Sequence to Space: Explicit Spatial Belief with Vision-Language Distillation for Active Geo-Localization</a></td><td>42</td><td>5</td><td>Navigation</td><td>명시적 공간 belief와 VL 증류로 active geo-localization을 함. active perception 맛이 있으나 항공 격자 한정임</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2611.26127'>Spatially Conditioned Trajectory Diffusion</a></td><td>42</td><td>5</td><td>Planning</td><td>공간 조건 diffusion으로 다중 로봇 경로 계획함. 기존 diffusion planner 개선 수준임</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2611.24995'>EgoPass-Bench: Identifying Objects That May Affect the Wearer&#x27;s Passage in Egocentric Video</a></td><td>42</td><td>4</td><td>Embodied AI</td><td>egocentric 영상에서 착용자 통행에 영향 주는 물체를 찾는 benchmark임. 평가 중심이라 방법론 기여는 제한적임</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2611.26035'>Fixing the Twin, Not the Detector: Sim-to-Real Roadside LiDAR Detection from Digital-Twin Data</a></td><td>42</td><td>4</td><td>3D Vision</td><td>digital twin에서 실센서로 sim-to-real LiDAR 검출을 함. 도로변 인프라 응용이라 로봇 연결 제한적임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2611.25696'>LIFT: Lifting Language-Controlled Image Fusion to Free-Viewpoint 3D Scenes</a></td><td>42</td><td>3</td><td>3D Vision</td><td>언어 제어 이미지 융합을 자유 시점 3D 장면으로 확장함. 3D 표현 시도는 있으나 로봇 연결 약함</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2611.25934'>AGSR: Aperture-Guided Super-Resolution for Gaussian Splatting</a></td><td>42</td><td>3</td><td>3D Vision</td><td>3DGS의 aperture 유도 super-resolution임. 3DGS 개선이나 렌더링 품질 중심임</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2611.26321'>FirstCross: Convex Single-Photon 3D Reconstruction from Sparse Views</a></td><td>42</td><td>3</td><td>3D Vision</td><td>FirstCross가 convex 문제로 단광자 3D 복원을 1분 내 수행하고 1% 광자에서도 우수함. 방법 우아하나 센서 특수하고 로봇 연결 약함</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2611.25160'>Bayesian $κ$-Explorer for Minimax Model Estimation in MDPs</a></td><td>42</td><td>3</td><td>RL</td><td>MDP 탐색 minimax 추정의 Bayesian 이론으로 RL 이론이나 로봇 실험 없음</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2611.26109'>SenseAlign: Learning Decision-Aligned Predictive Representations for Active Urban Sensing with UAVs</a></td><td>42</td><td>3</td><td>Active Sensing</td><td>privileged teacher로 결정 정렬 표현을 학습해 UAV 능동 센싱 RL을 개선함. 바르셀로나 도로망 시뮬레이션뿐이고 도메인 특수함</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2611.25747'>SAM 3 Sees More Than It Detects: Promptable Concept Maps Beyond Categories</a></td><td>42</td><td>2</td><td>CV</td><td>SAM 3의 promptable concept map을 클래스 비의존 dense 과제로 확장함. 분석 흥미로우나 로봇 연결 약함</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2611.26045'>PaveSplat: Resolution-Robust Feed-Forward Gaussian Splatting with Residually Corrected Surface-Aligned Covariances</a></td><td>42</td><td>2</td><td>3D Vision</td><td>해상도에 강건한 feed-forward Gaussian splatting임. 렌더링 개선 수준임</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2611.26427'>MemFolder: Structure-Guided Memory Folding for Efficient Agent Memory Management</a></td><td>42</td><td>2</td><td>Agent Memory</td><td>agent memory를 접어 record 50% 감소에도 성능 99.0% 유지함. M3-Bench-robot 포함하나 LLM agent memory 중심임</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2611.25950'>GaussTrans: A Gaussian Interface Framework for Multi-Layer Refractive Transport</a></td><td>42</td><td>2</td><td>3D Vision</td><td>Gaussian으로 다층 굴절 투명 계면을 모델링함. 3DGS 계열이나 로봇 연결 약함</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2611.25257'>Keel: A Frontier Model Teaches a Vision-Language Model by Rewriting Its Weights</a></td><td>42</td><td>1</td><td>Multimodal</td><td>frontier 모델이 VLM 가중치를 직접 고치는 설정이 독특함. 로봇과 무관하고 범위가 좁음</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2611.25776'>Suppressing the Shortcut Hidden Behind the Gains of VideoLLM Fine-Tuning</a></td><td>42</td><td>1</td><td>Video</td><td>VideoLLM SFT의 텍스트 shortcut 억제임. 문제 진단은 좋으나 로봇 무관함</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2611.26511'>Direct3D-V3: Latent-Free Diffusion Transformers in the Native Voxel Domain</a></td><td>42</td><td>1</td><td>3D Vision</td><td>latent 없는 voxel 3D 생성 diffusion으로 로봇 관련성 낮음</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2611.25476'>WeightCode: Installing New Capabilities into Neural Networks via Weight-Space Programming</a></td><td>42</td><td>1</td><td>LG</td><td>frozen LM이 weight program을 작성해 gradient 없이 신경망에 능력을 설치하는 새 접근임. 설치된 pickup 행동이 gridworld 수준이라 로봇 증거는 약함</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2611.26423'>Seer: Guiding Small Deep-Research Agents with Shared Decision Models</a></td><td>42</td><td>1</td><td>Agent</td><td>tool-response simulator와 value estimator로 소형 agent의 inference-time 탐색을 안내해 GAIA 13.6%에서 41.7%로 올림. 로봇 planning과 구조 유사하나 LLM agent 한정임</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2611.25998'>Reinforcing Few-Step Diffusion Models via Shadow Posterior Matching</a></td><td>42</td><td>0</td><td>Generative</td><td>few-step diffusion의 black-box reward RL 문제를 다루나 로봇 무관함</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2611.26275'>dLoop: Looped Diffusion Language Models via Recurrent Latent Refinement</a></td><td>42</td><td>0</td><td>NLP</td><td>diffusion LM에 recurrent latent refinement를 넣어 step을 줄임. 효율 기법이나 로봇 무관함</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2611.26031'>Close&amp;Safe: Maximal Task Preservation for Redundant Manipulators via C-Space Boundary Detour</a></td><td>40</td><td>6</td><td>Manipulation</td><td>C-space 경계 우회로 중복 자유도 매니퓰레이터 과제를 보존함. 고전 계획 기법임</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2611.26074'>Controlling the Humanoid Robot H1-2 With a Simulated Biologically Plausible Network</a></td><td>40</td><td>6</td><td>Robot Control</td><td>휴머노이드 H1-2를 spiking 신경망으로 제어함. 로봇 실증은 있으나 학습·일반화 근거 약하고 소규모임</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2611.25445'>Stereo Visual Odometry with In-the-Loop Geometric Feed-Forward Models Towards Dense Metric Mapping</a></td><td>40</td><td>5</td><td>3D Vision</td><td>stereo VO에 geometric feed-forward model을 결합함. 조합형 기여로 novelty 낮음</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2611.26242'>FastRoverVLA: Fast Vision-Language-Action Execution for Off-Road Autonomous Driving</a></td><td>40</td><td>5</td><td>VLA</td><td>오프로드 주행 VLA의 추론 재사용으로 가속함. 효율화 중심임</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2611.25712'>SkillLens: Action-Guided Dense Visual Dynamics for Proficiency Estimation</a></td><td>40</td><td>3</td><td>Video</td><td>행동 기반 시각 dynamics로 숙련도 추정함. 인간 영상 분석이며 로봇 연결은 약함</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2611.25838'>ContextRenderer: Dynamic-Context Video Generation for Interactive Game Worlds</a></td><td>40</td><td>3</td><td>World Model</td><td>게임 world model용 동적 컨텍스트 비디오 생성임. 게임 도메인이며 로봇 연결 약함</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2611.26491'>FLUID: Flexible, Evidence-Grounded Situated Task Guidance</a></td><td>40</td><td>3</td><td>Multimodal</td><td>HoloAssist 등 실제 안내 데이터로 개입 시점을 평가하고 실시간 agent를 만듦. egocentric 안내 관련하나 로봇 아님</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2611.26145'>Can World Models Predict Rice Growth? Toward Agricultural World Models</a></td><td>40</td><td>2</td><td>World Model</td><td>AgroWM이 벼 생육 단계 예측에서 Stage R@1 54.6%로 baseline 34.8%를 능가함. 새 도메인 정식화이나 로봇 연결 약함</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2611.25338'>VideoRNG: Relightable Neural Gaussians from Generative Video Models</a></td><td>40</td><td>1</td><td>3D Vision</td><td>비디오 생성 모델로 relightable neural Gaussian 자산을 만듦. 그래픽스 성격이 강함</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2611.26107'>HiUni: Harmonizing Understanding and Generation in Shared Visual Space</a></td><td>40</td><td>1</td><td>Multimodal</td><td>이해와 생성을 공유 시각 공간에서 통합함. 통합 모델 일반 연구로 로봇 연결 약함</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2611.26199'>Learning to Think with Images Faithfully via Adaptive Data Selection</a></td><td>40</td><td>1</td><td>Multimodal</td><td>thinking with images의 충실성을 위한 데이터 선택임. 로봇 무관함</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2611.26409'>WeMM-Video: Pushing the Frontiers of Open-Source Omni-Modal Video Understanding</a></td><td>40</td><td>1</td><td>Multimodal</td><td>omni-modal video 모델 리포트로 scale-up 성격 강함</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2611.25235'>Some Memories Must Fade: Persistence and Decay of User Memories in Model Parameters</a></td><td>40</td><td>1</td><td>NLP</td><td>LoRA 기반 파라메트릭 기억에 시간 감쇠와 정책 controller를 두는 LLM 사용자 기억 연구로 robot memory와 간접 관련임</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2611.26296'>SKILL.PNG: Learning Agent Skills in Pixel Space</a></td><td>40</td><td>1</td><td>NLP</td><td>VLM 이미지 입력 픽셀을 gradient로 최적화해 agent skill로 쓰는 새 아이디어이며 텍스트 skill보다 토큰이 적음. 로봇 검증 없음</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2611.24969'>Global Importance Estimation for KV Cache Eviction</a></td><td>40</td><td>1</td><td>LLM</td><td>KV cache 제거용 전역 중요도 추정임. 효율 추론이나 로봇 연결 약함</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2611.25429'>Evolve Where It Matters: Coverage-Guided Self-Evolution of Agent Skills</a></td><td>40</td><td>1</td><td>Agent</td><td>coverage 기반 agent skill 자기진화임. skill 개념은 있으나 NLP agent임</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2611.25433'>RoCoKV: Accelerating LLM Inference Serving through Uncertainty and Redundancy Aware KV Cache Compression</a></td><td>40</td><td>1</td><td>LLM</td><td>불확실성·중복 인지 KV cache 압축임. 효율화이고 로봇 무관함</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2611.25583'>DriftGuard: Online Memory-Drift Detection via Causal Attribution for LLM Agents</a></td><td>40</td><td>1</td><td>AI Agent</td><td>paired counterfactual replay로 drift 유발 memory 귀속을 학습해 online 검출함. 로봇 memory와 접점 있으나 LLM agent 한정임</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2611.26003'>AI agents can redesign engineering parts with more than a thousand CAD parameters and nonlinear simulations</a></td><td>40</td><td>1</td><td>Engineering</td><td>GPT-6 Astra가 CAD 1,650개 값을 15회 시뮬레이션으로 수정해 스텐트 변형률 32% 낮춤. 설계 최적화이며 로봇 무관함</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2611.25454'>Lossless Latent Diffusion Models</a></td><td>40</td><td>0</td><td>Generative</td><td>픽셀 단위 복원이 가능한 lossless latent diffusion임. 생성 모델 원리 측면은 있으나 로봇 무관함</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2611.25000'>Watch Where You Linearize: Predicting and Correcting Model-Merging Interference</a></td><td>40</td><td>0</td><td>LG</td><td>model merging 간섭 예측 지표로 로봇 무관함</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2611.25292'>Cross-Question Reliable Reinforcement Learning</a></td><td>40</td><td>0</td><td>NLP</td><td>LLM 질문 간 신뢰도 RL로 abstention 학습하나 로봇 무관함</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2611.25135'>Calibrated Decision Rewards: Training Language Models with a Judge That Knows How Sure It Is</a></td><td>40</td><td>0</td><td>LG</td><td>확률 보정된 judge로 LLM RL 보상을 만듦. 로봇 무관하나 보상 설계 아이디어 있음</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2611.25462'>Demonstration-Free Skill Composition for Navigation and Manipulation</a></td><td>38</td><td>6</td><td>RL</td><td>demonstration 없는 hierarchical skill 조합을 MiniGrid와 조작에서 평가함. 평가 위주로 참신성 낮음</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2611.25637'>Beyond Easy Clients: Difficulty- and Improvement-Aware Aggregation for Federated Reinforcement Learning in Robot Navigation</a></td><td>38</td><td>5</td><td>RL</td><td>federated RL의 난이도·개선 인지 집계로 navigation 학습함. incremental 성격임</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2611.26167'>Planning to Stop: Factored Certification and Terminal Repair for Noncircular Robots</a></td><td>38</td><td>5</td><td>Planning</td><td>비원형 로봇의 정지 인증과 복구 계획임. 고전 계획 기반임</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2611.26065'>Domain-Aware Conformal Prediction for Trustworthy Spacecraft Pose Estimation under Sim-to-Real Shift</a></td><td>38</td><td>4</td><td>CV</td><td>우주선 pose 추정의 conformal prediction 신뢰도임. 불확실성 측면은 있으나 특수 응용임</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2611.25373'>Differentiable Hydrodynamics for Whole-Body MPC of Underwater Robots</a></td><td>38</td><td>4</td><td>Control</td><td>수중 로봇 whole-body MPC용 미분 가능 유체역학 모델임. 전문 도메인 제어 연구임</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2611.26390'>SpecFlow: Flow Matching in the Acceleration Spectrum for Multi-Agent Trajectory Forecasting</a></td><td>38</td><td>4</td><td>Forecasting</td><td>가속도 스펙트럼 flow matching으로 다중 에이전트 궤적을 예측함. 로봇 직접성 낮음</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2611.25113'>Do Deep Stereo Models Learn Shape Priors?</a></td><td>38</td><td>3</td><td>3D Vision</td><td>stereo 모델의 shape prior 학습 여부를 분석함. embodied 언급은 있으나 분석 범위가 좁음</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2611.25458'>RemoteVLPG: How to Obtain a Specific VLM for Language-Guided Path Generation on Remote Sensing Images?</a></td><td>38</td><td>3</td><td>Navigation</td><td>원격탐사 이미지에서 언어 지시 기반 경로 생성 VLM임. 항법 요소는 있으나 도메인 특수함</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2611.25232'>Ferrofluid Shape Control with Deep Reinforcement Learning</a></td><td>38</td><td>3</td><td>RL</td><td>ferrofluid 형상 제어에 deep RL 적용함. 특수 소재 응용이라 로봇 학습 일반성은 낮음</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2611.26007'>System-One RSI: Building Muscle Memory for Interactive Agents through Guided Practice</a></td><td>38</td><td>3</td><td>Agent/Control</td><td>빠른 결정 모델과 OODA loop에 외부 muscle memory를 쌓음. 게임 3종 실험이며 로봇 검증 없음</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2611.25414'>Watertight Mesh Optimization of Textured Objects</a></td><td>38</td><td>2</td><td>3D Vision</td><td>텍스처 물체의 watertight mesh 최적화임. 자산 품질 개선이며 로봇 연결은 약함</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2611.26120'>Better Retrieval, Not Better Binding: Pretraining Exposure in Egocentric Video Retrieval</a></td><td>38</td><td>2</td><td>Video</td><td>egocentric 영상 검색에서 사전학습 노출이 binding이 아닌 retrieval만 돕는다는 분석임. 로봇 연결 약함</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2611.26478'>SHUSH: Emission-Aware Reward Design for Proactive Video Assistants</a></td><td>38</td><td>2</td><td>Video</td><td>proactive video assistant의 발화 시점 reward 설계로 로봇 연결 약함</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2611.26384'>A Complete Geometric Message-Passing Architecture for Point Clouds</a></td><td>38</td><td>2</td><td>3D Vision</td><td>point cloud용 완전 기하 message-passing 아키텍처로 3D 표현 이론 기여임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2611.25282'>MS-Point: Multi-Modal Hierarchical Spectral Learning for Point Cloud Understanding</a></td><td>38</td><td>2</td><td>3D Vision</td><td>point-image 정렬에 계층 spectral 학습을 적용한 점군 표현 학습임. 개선 폭 작은 incremental 성격임</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2611.25523'>Multi-View Relighting with Mergeable Radiance Fields</a></td><td>38</td><td>1</td><td>3D Vision</td><td>파라미터 병합으로 radiance field relighting을 함. 그래픽스 성격이 강함</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2611.26318'>ResVision: Spectrum-Matched Resizing and Context-Preserving Inspection for Visual Reasoning</a></td><td>38</td><td>1</td><td>Multimodal</td><td>agentic visual reasoning의 해상도 조정 방식임. incremental임</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2611.24977'>CANDID: Candidate-Driven Intervention for Disciplined Execution in Local Computer-Use Agents</a></td><td>38</td><td>1</td><td>Agent</td><td>로컬 computer-use agent 실행 제어임. 실패 방지 관점은 있으나 로봇 아님임</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2611.25407'>ChronoDossier: Long-Form Personas as Temporal Memory Representations</a></td><td>38</td><td>1</td><td>Agent</td><td>장기 persona를 temporal memory 표현으로 씀. memory 관련이나 텍스트 한정임</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2611.25705'>STARK: Moving towards Personalized Agents That Truly Learn and Remember</a></td><td>38</td><td>1</td><td>Agent</td><td>개인화 agent의 장기 기억과 이유 추론임. memory 개념은 있으나 텍스트 한정임</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2611.26590'>Probing the &quot;Conscious&quot; Mind: Selective Access and Global Workspace in Vision-Language Models</a></td><td>38</td><td>1</td><td>Multimodal</td><td>VLM의 global workspace 선택적 접근 probe임. 분석 연구이며 로봇 연결 약함</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2611.25457'>CANDOR: Contrastive Self-Denoising Rewards for Label-Free Text-to-Image Post-Training</a></td><td>38</td><td>0</td><td>Generative</td><td>레이블 없는 T2I post-training 자기 보상임. 로봇 무관함</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2611.25814'>What Does Anti-Hallucination Training Buy? Saying Less, Cheap Pruning, and the Rest</a></td><td>38</td><td>0</td><td>Multimodal</td><td>hallucination 감소 훈련이 실제로 무엇을 사는지 분석함. 평가 통찰은 좋으나 로봇 무관함</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2611.26629'>Posterior Matching Distillation</a></td><td>38</td><td>0</td><td>Generative</td><td>diffusion distillation 목적함수 개선으로 일반 생성 모델 incremental임</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2611.25003'>A Model of Diverse Sampling from Language Models</a></td><td>38</td><td>0</td><td>NLP</td><td>DPP 기반 LM 다양성 샘플링 이론으로 로봇 무관함</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2611.25165'>Separating Interpretability and Reconstruction in Sparse Autoencoders</a></td><td>38</td><td>0</td><td>LG</td><td>SAE 해석성과 복원 분리로 로봇 무관함</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2611.26172'>Budget Internalization: Fixed-Budget RLVR Trades Test-Time Scaling for In-Budget Accuracy</a></td><td>38</td><td>0</td><td>NLP</td><td>고정 budget RLVR이 test-time scaling을 줄이는 분석으로 로봇 무관함</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2611.25813'>Efficient and Robust Drafting with Multi-Token Prediction</a></td><td>38</td><td>0</td><td>LLM</td><td>multi-token prediction 기반 speculative drafting임. 효율화이고 로봇 무관함</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2611.26584'>Represented but misread: Post-training changes how language models read out what they represent</a></td><td>38</td><td>0</td><td>NLP</td><td>post-training이 표현 read-out을 바꾸는지 probe로 분석함. 로봇 무관함</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2611.25171'>A Verifier from the Past: Test-Time Compute for Time Series Foundation Models</a></td><td>38</td><td>0</td><td>Time Series</td><td>시계열 foundation model에 test-time compute와 verifier를 적용함. 로봇 직접 연결 약함</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2611.25895'>One Schedule Does Not Fit All: Adaptive Inference Schedules for Diffusion Language Models</a></td><td>38</td><td>0</td><td>Efficient</td><td>diffusion LM 적응적 inference schedule임. 효율 기법이나 로봇 무관함</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2611.25926'>ROAM-GRPO: Enforcing Reasoning Diversity in GRPO via Routed Off-mode Approach Mining</a></td><td>38</td><td>0</td><td>RL</td><td>GRPO 추론 다양성 강제임. LLM RL이며 로봇 무관함</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2611.26503'>JARVIS: An Agent That Designs, Builds, and Tests Circuit Boards on Its Own</a></td><td>36</td><td>3</td><td>Agent</td><td>회로 기판을 설계·제작·시험하는 agent임. 로봇 학습과 방향이 다름임</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2611.25703'>From Geographic Memory to Spatial Generalization in Large Language Models</a></td><td>36</td><td>1</td><td>NLP</td><td>LLM의 지리 기억에서 공간 일반화로의 구분 분석임. 공간 추론 주제나 텍스트 한정임</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2611.26464'>Monte Carlo Pass Search for Setpieces</a></td><td>36</td><td>1</td><td>World Model</td><td>world model에서 counterfactual 전달과 배치를 Monte Carlo로 탐색함. 축구 세트피스 응용이며 로봇 무관함</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2611.26510'>AutoMaster: Autonomous Post-Training by Making the Same Model a Better Teacher</a></td><td>36</td><td>0</td><td>NLP</td><td>skill 지시로 teacher 궤적을 교정해 SFT 성능을 1.42~8.99퍼센트포인트 올림. LLM post-training이며 로봇 무관함</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2611.26600'>A Tutorial on Complementarity-Based Contact Models for Robotics</a></td><td>35</td><td>5</td><td>Simulation</td><td>상보성 기반 접촉 모델 튜토리얼임. 새 방법이 아니라 교육 자료임</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2611.26276'>I See You: Initial Multi-Robot LiDAR Registration with Mutual-Observation Checks</a></td><td>35</td><td>4</td><td>SLAM</td><td>다중 로봇 LiDAR 초기 정합용 상호 관측 검사임. 고전 SLAM 영역임</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2611.26302'>Exposure-Aware Informative Path Planning Using Deep Reinforcement Learning</a></td><td>35</td><td>4</td><td>Planning</td><td>노출 인지 informative path planning에 deep RL 적용함. 특수 문제 설정임</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2611.25297'>ScaleDiag: Diagnosing the Limits of Test-Time Scaling in GUI Grounding</a></td><td>35</td><td>2</td><td>Multimodal</td><td>GUI grounding의 test-time scaling 한계를 진단함. 로봇과 거리가 있음</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2611.25274'>DS3M: Deep structured state space models for nonlinear system identification on modern hardware</a></td><td>35</td><td>2</td><td>LG</td><td>신경 상태공간 system identification 학습 속도 개선으로 제어와 약하게 관련됨</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2611.26440'>Learning to Defer under Expert Drift</a></td><td>35</td><td>2</td><td>LG</td><td>expert 변동을 고려한 learning to defer로 human-in-the-loop 관점에서 약하게 관련됨</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2611.26598'>Active Feature Acquisition by Distilling an Oracle Teacher</a></td><td>35</td><td>2</td><td>LG</td><td>oracle teacher 증류 active feature acquisition으로 active perception과 약하게 관련됨</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2611.25773'>Duopra: From Full-Duplex Conversation to Full-Duplex Agency</a></td><td>35</td><td>2</td><td>Speech/Agent</td><td>full-duplex 대화에 task agency를 더함. 로봇 연결 약함</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2611.25069'>VisAlloc: Allocating Visual Supervision for On-Policy Self-Distillation</a></td><td>35</td><td>1</td><td>Multimodal</td><td>MLLM on-policy self-distillation의 토큰별 감독 배분 개선임. incremental 수준이며 로봇과 무관함</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2611.25369'>Fold the Loop: Decoding-Time KV Memory for Looped Vision-Language Models</a></td><td>35</td><td>1</td><td>Multimodal</td><td>looped VLM의 decoding KV memory 압축임. 효율 개선 위주이며 로봇 무관함</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2611.25389'>Zero to Four Views: Unified Panorama Generation and Preference RL for Unobserved Regions</a></td><td>35</td><td>1</td><td>Generative</td><td>0~4개 뷰 조건 파노라마 생성과 preference RL임. 생성 응용이며 로봇 연결 약함</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2611.25419'>DiLE: Discrimination-Aware Latent-Space Learning for Universal Multimodal Embeddings</a></td><td>35</td><td>1</td><td>Multimodal</td><td>multimodal 임베딩의 discrimination 인지 학습임. 표현학습 benchmark 개선 위주임</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2611.25537'>Query-Aware vs. Query-Agnostic Training-Free Video Token Pruning in Multimodal LLMs</a></td><td>35</td><td>1</td><td>Video</td><td>query-aware 대 agnostic 비디오 token pruning 비교 분석임. 효율 연구로 로봇 연결 약함</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2611.25713'>Interpreting DeepStack-Style Vision-Language Models: Do Input or Deeper-Layer Visual Tokens Drive Answers?</a></td><td>35</td><td>1</td><td>Multimodal</td><td>DeepStack형 VLM의 later visual token 역할 해석임. 분석 위주이며 로봇 무관함</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2611.25834'>Rank2Replace: VLM-Ranked Slot Replacement for Out-of-Distribution Generalization</a></td><td>35</td><td>1</td><td>CV</td><td>VLM 순위 기반 slot 교체로 OOD 일반화를 개선함. 일반 분류 문제임</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2611.26595'>Coda-DaVinci: Reimagining Video Generation with Code2Video</a></td><td>35</td><td>1</td><td>Video</td><td>code 기반 3D proxy로 비디오 생성을 제어하는 분석으로 로봇 연결 약함</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2611.24999'>PsyWorld: Profile-Conditioned World Modeling for Human Behavior Prediction</a></td><td>35</td><td>1</td><td>LG</td><td>프로필 조건 world model로 행동과학 응용이며 로봇 무관함</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2611.25100'>HapBO: Harnessed $α$-$π$ Bayesian Optimization via Expert Natural Language Priors</a></td><td>35</td><td>1</td><td>LG</td><td>자연어 prior를 쓰는 Bayesian optimization으로 로봇 연결 약함</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2611.26157'>NariQ: Sub-3-Bit Quantization for Long-Horizon Agentic Tasks</a></td><td>35</td><td>1</td><td>NLP</td><td>long-horizon agent용 sub-3-bit 양자화로 효율 연구이나 로봇 무관함</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2611.25363'>Stop Going in Circles:Loop-Triggered Routing for System 1 Decision Agents</a></td><td>35</td><td>1</td><td>AI Agent</td><td>System 1 결정 모델 loop 시 상위 모델로 라우팅함. 로봇 연결 약함</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2611.25644'>MambaLIFT: Reference-Based Mechanism-Aware Attribution for VMamba</a></td><td>35</td><td>1</td><td>CV</td><td>VMamba 귀속 기법임. 해석 가능성 도구이며 로봇 무관함</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2611.25119'>Auditing Learned Dynamics in Weather Models</a></td><td>35</td><td>0</td><td>LG</td><td>기상 모델 SAE feature 감사로 로봇 무관함</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2611.25167'>Game-Theoretic Data Allocation for Expert Specialization and Routing</a></td><td>35</td><td>0</td><td>NLP</td><td>LoRA expert 데이터 할당·라우팅 게임이론으로 로봇 무관함</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2611.25211'>Learning to Read Events for Exact State Tracking with Frozen Language Models</a></td><td>35</td><td>0</td><td>NLP</td><td>frozen LM으로 event 상태 추적하는 외부 register 방식으로 로봇 연결 약함</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2611.25538'>Towards Autoregressive Neural Network Parameter Generation</a></td><td>35</td><td>0</td><td>LG</td><td>autoregressive 신경망 파라미터 생성으로 로봇 연결 약함</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2611.25763'>Closing Performance Gap for Diffusion Language Models under Low Inference Budgets</a></td><td>35</td><td>0</td><td>NLP</td><td>저예산 diffusion LM 성능 격차 축소임. 로봇 무관함</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2611.26077'>Same Judgement, Different Scores: Numerical Scoring Topology in LLM-as-a-Judge Evaluation</a></td><td>35</td><td>0</td><td>NLP</td><td>LLM-as-a-Judge 점수 척도 설계 분석임. 로봇 무관하고 분석 위주임</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2611.26282'>What If Chain-of-Thought Is Not Enough?</a></td><td>35</td><td>0</td><td>NLP</td><td>CoT의 내부 사고 모델 변경 가능성을 탐구함. 로봇 무관함</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2611.26358'>Beam Model Technical Report</a></td><td>35</td><td>0</td><td>NLP</td><td>501B MoE 기술 보고서임. agentic 용도이나 로봇 무관하고 새 원리 약함</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2611.25811'>Inject Where It Matters: Objective-Dependent Feature Control in Rectified-Flow Image Editing</a></td><td>35</td><td>0</td><td>Generative</td><td>FLUX 편집에서 목적별 feature 주입 제어임. 로봇 무관함</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2611.26342'>Training LLMs to Follow Reasoning Instructions with Minimal Edits</a></td><td>35</td><td>0</td><td>NLP</td><td>최소 편집으로 추론 지시 따르도록 학습함. 로봇 무관함</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2611.26586'>ProtoDiffusion: Token-per-Layer Generative Modeling of Multi-Layer Images</a></td><td>35</td><td>0</td><td>Generative</td><td>다층 RGBA 이미지 token-per-layer 생성임. 로봇 무관함</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2611.25254'>Plan your Self-Adaptation! Ontology-Mediated Task and Architecture Co-adaptation Planning for Robots</a></td><td>33</td><td>4</td><td>Planning</td><td>ontology 기반 과제·아키텍처 공동 적응 계획임. 소프트웨어 공학 성격이 강함</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2611.26090'>Dynamic Human-Robot Role Allocation through Entropy-Based Monitoring and LLM Reasoning</a></td><td>33</td><td>4</td><td>HRI</td><td>엔트로피 모니터링과 LLM으로 인간-로봇 역할을 배분함. 증거 약함</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2611.26350'>PUPPET: Physical-Unified Platform for Presence, Embodiment, and Teleoperation</a></td><td>33</td><td>4</td><td>Teleoperation</td><td>원격 로봇 접근과 데이터 기록 플랫폼임. 시스템 도구 수준임</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2611.25475'>SegAnyFruit: Learning Generalizable and Edge Deployable Fruit Instance Segmentation at Scale</a></td><td>33</td><td>3</td><td>CV</td><td>과일 instance segmentation의 edge 배포용 모델임. 농업 응용 데이터 중심임</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2611.25771'>Driver Gaze Target Identification via Gaze Estimation and Structured Driving Scene Understanding</a></td><td>33</td><td>3</td><td>CV</td><td>운전자 시선 대상 식별임. 자율주행 응용으로 로봇 연결 약함</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2611.25248'>Branch Caching After Step Distillation in Four- and Eight-Step Image Generators</a></td><td>33</td><td>1</td><td>Generative</td><td>step distillation 이후 branch caching 가속 연구임. 효율 개선 위주이며 로봇 연결 없음</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2611.25436'>Raptor: Rejection-aware Adaptive Tree based on Speculative Decoding</a></td><td>33</td><td>1</td><td>Multimodal</td><td>VLM speculative decoding 트리 개선임. 추론 효율 incremental임</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2611.25524'>Contrast Where It Matters: Visual Evidence-Guided Decoding for Mitigating Hallucinations in LVLMs</a></td><td>33</td><td>1</td><td>Multimodal</td><td>LVLM hallucination 완화 decoding임. 로봇 무관하고 incremental함</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2611.25574'>VidToC: Rethinking Video Token Compression for Multimodal Large Language Models</a></td><td>33</td><td>1</td><td>Video</td><td>MLLM 비디오 token 압축 재고임. 효율 incremental임</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2611.25680'>Beyond Entity Recognition: Vision-Centric Knowledge Visual Question Answering</a></td><td>33</td><td>1</td><td>Multimodal</td><td>시각 중심 지식 VQA benchmark임. 로봇 무관함</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2611.25689'>D3-Cache: Accelerating Diffusion Models with Dynamic Mode Decomposition</a></td><td>33</td><td>1</td><td>Generative</td><td>Dynamic mode decomposition 기반 diffusion caching임. 가속 incremental임</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2611.25815'>What Places an Action Boundary? Structure-Aware Attribution for Temporal Action Localization</a></td><td>33</td><td>1</td><td>Video</td><td>행동 경계 attribution 분석임. 로봇 무관하고 범위가 좁음</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2611.25847'>TrajCal: Trajectory-Calibrated Time Schedules for Few-Step Flow Sampling</a></td><td>33</td><td>1</td><td>Generative</td><td>few-step flow 샘플링 시간 스케줄 보정임. 효율 incremental임</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2611.26334'>Online Temporal Rotations for 2 Bit KV-Cache Quantization in Video Diffusion Transformers</a></td><td>33</td><td>1</td><td>Generative</td><td>video DiT KV cache 2비트 양자화임. 효율 incremental임</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2611.25382'>Text Lives in the Guidance: Preventing Silent Text Rewriting in Cached Diffusion Transformers</a></td><td>33</td><td>0</td><td>Generative</td><td>캐시된 DiT에서 텍스트 왜곡을 막는 기법임. 로봇 무관함</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2611.25620'>CaT-Movie: Balancing Global Planning and Local Rendering for Long Multi-Shot Video Generation</a></td><td>33</td><td>0</td><td>Video</td><td>장편 multi-shot 영상 생성의 전역 계획과 지역 렌더링임. 로봇 무관함</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2611.25930'>Why Flat Drafts Stay Flat: Region-Mean Latents Govern Texture in Flow-Based Image Generation</a></td><td>33</td><td>0</td><td>Generative</td><td>flat draft 질감을 region-mean latent로 설명함. 로봇 무관함</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2611.26095'>Approximate Adjoint Models for Memory and Compute-Efficient Online Learning of Hybrid Models</a></td><td>32</td><td>2</td><td>LG</td><td>hybrid 모델 online 학습용 근사 adjoint로 제어와 약하게 관련됨</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2611.26463'>Neural Conditional Gaussian Model: Efficient Data Assimilation with Sequential Uncertainty Quantification for Nonlinear Dynamics</a></td><td>32</td><td>2</td><td>LG</td><td>비선형 data assimilation 불확실성 추정으로 상태 추정과 약하게 연결됨</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2611.25868'>Generalist Meets Specialists: An Evolving Multimodal Agent with Persistent Tool Orchestration for Traffic Scenario Understanding</a></td><td>32</td><td>2</td><td>Multimodal</td><td>교통 장면 이해용 진화형 tool agent임. 로봇 연결 약함</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2611.25204'>Identity World Model: Recognizing People in an Imagined Latent World</a></td><td>32</td><td>1</td><td>CV</td><td>전신 사람 재식별을 latent world로 풀어냄. 로봇 관련성 낮고 응용 한정임</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2611.25296'>CalibCache: Cache-to-Full Feature Dynamics Calibration for Diffusion Transformers</a></td><td>32</td><td>1</td><td>Generative</td><td>DiT feature caching 보정 기법임. 가속 incremental 수준임</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2611.25628'>RelGeo: Pair-Conditioned Relational Calibration for Frozen Diffusion Correspondence</a></td><td>32</td><td>1</td><td>CV</td><td>frozen diffusion 대응점 매칭 보정임. incremental 수준임</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2611.25673'>CompAct-Bench: A Benchmark for Working-Context Compaction in Long-Horizon Agent Tasks</a></td><td>32</td><td>1</td><td>AI Agent</td><td>agent 작업 컨텍스트 압축 benchmark임. 로봇 연결 약함</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2611.25551'>Anchored Inertial Proposals with Objective Verification for Diffusion-Prior Inverse Problems</a></td><td>32</td><td>0</td><td>Generative</td><td>diffusion prior 역문제 샘플링 개선임. 로봇 무관함</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2611.25430'>Interference Bounds and Merge-Aware Training Dynamics for Composable Fine-Tuned Models</a></td><td>32</td><td>0</td><td>LG</td><td>fine-tuned 모델 합성 간섭 이론으로 로봇 무관함</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2611.25560'>Is a Description Worth a Thousand Demonstrations? Specificity and Reliability of Task Descriptions in In-Context Learning</a></td><td>32</td><td>0</td><td>NLP</td><td>ICL 과제 설명의 구체성 이론으로 로봇 무관함</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2611.25938'>DTS: Delta-Based Tile Scoring for Efficient Long-Context Sparse Attention</a></td><td>32</td><td>0</td><td>NLP</td><td>LLM 장문 sparse attention tile scoring 효율 개선임</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2611.26187'>Invertible Transport Between Sample-Only Distributions via Projected Characteristic Functions</a></td><td>32</td><td>0</td><td>LG</td><td>sample-only 분포 간 invertible transport로 로봇 무관함</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2611.26363'>HiSA: Sparsifying the Hidden Dimension of RoPE Attention in LLMs</a></td><td>32</td><td>0</td><td>NLP</td><td>RoPE attention hidden dim sparsification 효율 개선임</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2611.24994'>What the model knows but does not say: monitoring medical LLMs through verbalized thoughts</a></td><td>32</td><td>0</td><td>NLP</td><td>의료 LLM의 verbalized thought 모니터링임. 로봇 무관함</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2611.26075'>Understanding MoE Decisions Beyond Gradients</a></td><td>32</td><td>0</td><td>NLP</td><td>MoE 결정 해석을 gradient 너머로 확장함. 로봇 무관함</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2611.25539'>COVERAGE-TRACE: Source-Side Counterfactual Tracing for Detecting Omissions in LLM Summaries</a></td><td>32</td><td>0</td><td>NLP</td><td>원문 쪽 counterfactual 추적으로 요약 누락을 검출함. 로봇 무관함</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2611.25566'>Diagnosis is not a policy: a state-transition audit of caoability-conditioned test-time inference</a></td><td>32</td><td>0</td><td>AI</td><td>test-time 오류 대응 감사 프로토콜임. 로봇 무관함</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2611.25613'>Can an LLM Fix a Language Model Without Training It?</a></td><td>32</td><td>0</td><td>LG</td><td>외부 LLM이 모델 가중치를 수리하는 방식 평가임. 로봇 무관함</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2611.25793'>When Safety Rationales Hallucinate: Diagnosing and Grounding Multimodal Safety Guards</a></td><td>32</td><td>0</td><td>Multimodal</td><td>멀티모달 safety guard rationale 환각 진단임. 로봇 무관함</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2611.25861'>Decoupled Knowledge Retrieval and Compact Memory Enable Reliable Lifelong Model Editing</a></td><td>32</td><td>0</td><td>NLP</td><td>lifelong model editing용 검색과 compact memory 분리임. 로봇 무관함</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2611.26545'>The Geometry of Lies: Knowledge and Persona Directions for Detecting Deception in Large Language Models</a></td><td>32</td><td>0</td><td>NLP</td><td>지식·persona 방향으로 LLM 거짓말 검출함. 로봇 무관함</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2611.25904'>Multiple-Camera Tracking of Rigid Objects</a></td><td>30</td><td>4</td><td>3D Vision</td><td>윤곽 정렬 기반 다중 카메라 강체 추적임. 고전적 방법임</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2611.25787'>GeoPillars: A Large-Kernel Pillar Detector for Single-Sweep LiDAR Under Point Sparsity, and a Decomposition of Its Gain</a></td><td>30</td><td>3</td><td>3D Vision</td><td>GeoPillars 이득 대부분이 head 해상도 때문이며 nuScenes zero-shot에서 전이 안 됨을 저자가 인정함. 정직한 분석이나 기여가 작음</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2611.25480'>Learning Ankle Exoskeleton Control for Reactive Standing Balance Through Neuromusculoskeletal Simulation</a></td><td>30</td><td>2</td><td>Exoskeleton</td><td>근골격 시뮬레이션으로 외골격 균형 제어를 학습함. 로봇 학습 주제와 거리 있음</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2611.25126'>TALD: Transferability-Aware Logit Disentanglement for Cross-Modal Knowledge Distillation</a></td><td>30</td><td>1</td><td>LG</td><td>cross-modal distillation의 logit 분리 기법임. 일반 분류 개선이며 로봇 연결 없음</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2611.25239'>Beyond Restoration: Content-Degradation Factor Unfolding for Real-World Concealed Object Segmentation</a></td><td>30</td><td>1</td><td>CV</td><td>은닉 물체 분할의 degradation 분리 기법임. incremental 모듈 수준임</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2611.25711'>Calibrate in Context: Efficient Data-Free Quantization from Small Synthetic Pools</a></td><td>30</td><td>1</td><td>LG</td><td>data-free quantization용 합성 pool임. 효율 incremental임</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2611.26431'>FFGaussType: Feed-Forward Conversion of Glyph and SVG Geometry into Compact Gaussian Assets</a></td><td>30</td><td>1</td><td>3D Vision</td><td>glyph/SVG를 Gaussian asset으로 변환하는 그래픽스 응용으로 로봇 무관함</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2611.25424'>Coordinate Basis Linear Bandits with Sublinear Regret over Low-Rank Clusters</a></td><td>30</td><td>1</td><td>LG</td><td>linear bandit 계산 효율 이론으로 로봇 연결 약함</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2611.26232'>Time Series Structure Learning with Local Causal Parent Discovery</a></td><td>30</td><td>1</td><td>LG</td><td>시계열 인과 부모 탐색으로 로봇 연결 약함</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2611.26607'>Bio-PM-Guided Synthetic IMU Generation</a></td><td>30</td><td>1</td><td>LG</td><td>생체역학 기반 합성 IMU 생성으로 HAR 응용임</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2611.25526'>MATE: Mobile Agent Trustworthy Execution for Safe and Efficient Mobile Control</a></td><td>30</td><td>1</td><td>Agent</td><td>모바일 agent 안전 실행 계층임. 로봇 아님임</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2611.25855'>HabitusMem: Belief Memory over Evolving User Preferences for LLM Agents</a></td><td>30</td><td>1</td><td>Agent Memory</td><td>사용자 선호 belief memory임. 로봇 연결 약함</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2611.26361'>How Much Should an Agent Remember? Deployment Lessons from Self-Distilled Memory for LLM Agents</a></td><td>30</td><td>1</td><td>Agent Memory</td><td>LLM agent self-distilled memory 배포 교훈임. 로봇 연결 약함</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2611.26509'>GLiDE: A Fast, Calibrated Decision Model Distilled from Reasoning Teachers</a></td><td>30</td><td>1</td><td>LG</td><td>추론 teacher에서 distill한 빠른 decision model임. 로봇 연결 약함</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2611.25168'>What a Calibrated Probability Hides: Belief-Level Post-Training for Decision Models</a></td><td>30</td><td>0</td><td>LG</td><td>의사결정 모델의 belief 수준 post-training임. 로봇과 무관하고 비전 연결도 약함</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2611.25535'>Support-Guided Triadic Decoding for Hallucination Mitigation in Multimodal Dialogue with LVLMs</a></td><td>30</td><td>0</td><td>Multimodal</td><td>멀티턴 대화 hallucination 완화 decoding임. 로봇 무관함</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2611.25635'>AesDistill: Distilling Generative Aesthetics for Image Color Enhancement</a></td><td>30</td><td>0</td><td>Generative</td><td>이미지 색 보정을 위한 생성 미학 distillation임. 로봇 무관함</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2611.25648'>TRACE: Attribute Execution for Sequential Image Editing</a></td><td>30</td><td>0</td><td>Generative</td><td>순차 이미지 편집의 attribute 실행임. 로봇 무관함</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2611.25979'>Multi-View Transformer with Geometry-Guided Multi-Modal ControlNet for 3D Virtual Try-On</a></td><td>30</td><td>0</td><td>3D Vision</td><td>3DGS 가상 피팅임. 로봇 무관함</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2611.26058'>One-to-Many: Diverse and Bidirectional Image-to-Image Translation via Rectified Flow</a></td><td>30</td><td>0</td><td>Generative</td><td>rectified flow 기반 일대다 image translation임. 로봇 무관함</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2611.26098'>Frequency-Synchronized Boundary Coupling for Training-Free Multi-Prompt Long Video Generation</a></td><td>30</td><td>0</td><td>Video</td><td>training-free multi-prompt 장편 영상 생성임. 로봇 무관함</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2611.26164'>MultiBinder: Preventing Multi-Subject Identity Leakage in Personalized Video Generation</a></td><td>30</td><td>0</td><td>Video</td><td>개인화 영상 생성의 다중 주체 identity 누출 방지임. 로봇 무관함</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2611.26408'>Training Vision Models for LLM-Driven Weight-Space Programming</a></td><td>30</td><td>0</td><td>LG</td><td>LLM weight-space programming 벤치마크로 로봇 무관함</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2611.26437'>Asuka-FM: A System-Architectural Co-Design Framework for Efficient Text-to-Image Pretraining on Consumer Hardware</a></td><td>30</td><td>0</td><td>CV</td><td>소비자 GPU용 T2I 사전학습 시스템 설계로 로봇 무관함</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2611.25252'>Moving Generality from Model to Modeler: LLM Agents for PHM on a Deployment-Style Benchmark</a></td><td>30</td><td>0</td><td>LG</td><td>PHM용 LLM coding agent 벤치마크로 로봇 무관함</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2611.25597'>Decision-Focused Reinforcement Learning for LLM Post-Training</a></td><td>30</td><td>0</td><td>NLP</td><td>downstream 최적화를 위한 LLM RL post-training으로 로봇 무관함</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2611.26059'>Complete-SVD: A Functional Norm Approach to Low-Rank LLM Compression</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM low-rank 압축 norm 개선으로 로봇 무관함</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2611.25071'>FinVeriQA: Financial Research Agents for Question Answering: Routing, Retrieval, MCP Tool Use, and Provenance-Aware Evidence Verification</a></td><td>30</td><td>0</td><td>NLP</td><td>금융 QA agent 라우팅과 검증임. 로봇 무관함</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2611.25289'>LLMs Are Already Confidence-Aware Zero-Shot Classifiers</a></td><td>30</td><td>0</td><td>NLP</td><td>zero-shot LLM의 신뢰도 인지 분류 분석임. 로봇 무관함</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2611.25588'>Rubric Semantics or Numerical Priors? Auditing Scale-Direction Bias in LLM Judges</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM judge의 척도 방향 편향 감사임. 로봇 무관함</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2611.25717'>VR-SparseQuant: Accurate FP4 Quantization with 2:4 Sparsity on Vera Rubin</a></td><td>30</td><td>0</td><td>LLM</td><td>FP4와 2:4 sparsity 양자화임. 효율화이고 로봇 무관함</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2611.25916'>Many Solutions, One Answer: Search Order Shapes the Default Solutions of Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>탐색 순서가 LM 기본 해를 정함을 분석함. 로봇 무관함</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2611.26009'>Evaluating safeguarding in multi-turn conversations with AI assistants</a></td><td>30</td><td>0</td><td>NLP</td><td>다중 턴에서 cue가 분산되면 안전 응답 비율이 3-6%까지 떨어짐을 7,400회 대화로 보임. 증거는 강하나 로봇 무관함</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2611.26216'>Frontier models need only one text to unmask its human or AI author</a></td><td>30</td><td>0</td><td>NLP</td><td>단일 텍스트로 저자 식별 가능함을 보인 분석임. 로봇 무관함</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2611.25088'>BuggyMLE: Scaling Machine Learning Engineering Difficulty with Bug Injection</a></td><td>30</td><td>0</td><td>AI Agent</td><td>bug 주입으로 MLE agent benchmark 난이도 조절함. 로봇 무관함</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2611.25214'>Steering Automated Scientific Discovery via Audited Epistemic Exploration</a></td><td>30</td><td>0</td><td>AI Agent</td><td>과학 발견 agent의 가설 탐색 감사임. 로봇 무관함</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2611.25357'>Pro$^2$ Agent: Scientific Problem Probing for Autonomous AI R&amp;D</a></td><td>30</td><td>0</td><td>AI Agent</td><td>문제 구조 probing으로 AI R&amp;D agent 개선함. 로봇 무관함</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2611.25380'>Beyond Weight Updates: Evolving Agent Harnesses for Domain Specialization</a></td><td>30</td><td>0</td><td>AI Agent</td><td>가중치 대신 agent harness를 진화시켜 도메인 특화함. 로봇 무관함</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2611.25388'>Falsifiable Compositional Reasoning in Time Series Forecasting</a></td><td>30</td><td>0</td><td>Time Series</td><td>시계열 조합 추론 반증 가능성 연구임. 로봇 무관함</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2611.25586'>Learning Networked Dynamical Systems via Neural ODE-based Graph Structure Inference</a></td><td>30</td><td>0</td><td>LG</td><td>neural ODE로 동역학 그래프 구조 추론함. 로봇 무관함</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2611.25658'>SiliconGym: A Versatile Reinforcement Learning Environment for Agentic EDA</a></td><td>30</td><td>0</td><td>RL</td><td>EDA용 RL 환경임. 로봇 무관함</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2611.26191'>Backbone Matters: Benchmarking Encoder-Decoder Networks for Semantic Segmentation of Driving Scenes on BDD100K</a></td><td>28</td><td>3</td><td>CV</td><td>주행 장면 분할 encoder-decoder benchmark 비교임. 새로움이 작음</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2611.25854'>Learning-Based System Identification for DVL-Constrained AUV Localization</a></td><td>28</td><td>3</td><td>Localization</td><td>AUV DVL 제약 위치추정용 학습 기반 system identification임. 특수 도메인임</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2611.26083'>Reference-Twist-Based Velocity-Domain Spatiotemporal Calibration for mmWave Radar, Event Camera, and IMU</a></td><td>28</td><td>3</td><td>Calibration</td><td>mmWave·event·IMU 속도 영역 보정임. 센서 보정 연구임</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2611.25873'>WHU-Road3D: A dataset and benchmark towards fine-grained road surface mapping</a></td><td>28</td><td>2</td><td>CV</td><td>도로 표면 매핑 dataset임. 데이터셋 기여로 로봇 연결 약함</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2611.25309'>VoxForge: A Unified Foundation Model for Dense 3D Features Across MRI, CT and PET</a></td><td>28</td><td>0</td><td>CV</td><td>MRI/CT/PET 3D 의료 foundation model임. 로봇 무관함</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2611.25391'>HOPD: Historical On-Policy Distillation for SAR MLLM Continual Learning</a></td><td>28</td><td>0</td><td>Multimodal</td><td>SAR MLLM continual learning용 on-policy distillation임. 특수 도메인임</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2611.25444'>VisualTalk-Bench: Evaluating Question-Driven Avatar-Led Video Explanations</a></td><td>28</td><td>0</td><td>Video</td><td>아바타 기반 영상 설명 평가 benchmark임. 로봇 무관함</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2611.25478'>TAP: Tapping the Discriminative Potential of Frozen Representations for Class-Incremental Learning</a></td><td>28</td><td>0</td><td>LG</td><td>frozen 표현 기반 class-incremental learning임. 일반 CL이며 incremental함</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2611.25506'>Carry the Fine Print: Budget-Aware Visual Token Compression for Document OCR</a></td><td>28</td><td>0</td><td>Multimodal</td><td>문서 OCR용 visual token 압축임. 로봇 무관함</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2611.25621'>DAWN: Robust Neural Blind Deconvolution via Alternating Wiener Guidance</a></td><td>28</td><td>0</td><td>CV</td><td>blind deconvolution용 Wiener guidance임. 로봇 무관함</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2611.25731'>Towards High-Fidelity Learned Video Compression</a></td><td>28</td><td>0</td><td>Video</td><td>학습 기반 비디오 압축 고충실도 연구임. 로봇 무관함</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2611.26159'>When Foundation Models Disagree: Representational Heterogeneity for Calibrated Uncertainty in Whole-Slide Image Classification</a></td><td>28</td><td>0</td><td>CV</td><td>병리 foundation model 불일치 기반 불확실성 보정임. 로봇 무관함</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2611.26178'>FlexVSR: Continuous-Scale Super-Resolution for Streaming Video Generation</a></td><td>28</td><td>0</td><td>Video</td><td>streaming 영상 생성용 연속 스케일 super-resolution임. 로봇 무관함</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2611.26370'>Fast Self-Supervised Generative CT Denoising via Few-Step Sampling</a></td><td>28</td><td>0</td><td>CV</td><td>CT 영상 denoising으로 로봇과 무관하며 few-step 샘플링 적용 수준임</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2611.26540'>AURA: AUdio-dRiven streaming Avatar</a></td><td>28</td><td>0</td><td>Video</td><td>audio 기반 streaming avatar 생성으로 로봇 무관함</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2611.25130'>Temporal Extrapolation of Elastic Seismic Wave Propagation in Layered Media Using Neural Operators</a></td><td>28</td><td>0</td><td>LG</td><td>지진파 neural operator 응용으로 로봇 무관함</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2611.25151'>Rate-distortion Assessment for Hierarchical Content Summarization</a></td><td>28</td><td>0</td><td>LG</td><td>계층적 요약 rate-distortion 평가로 로봇 무관함</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2611.25185'>PDE-State Conditioning for Learned Optimization Using Physics-Informed Neural Networks</a></td><td>28</td><td>0</td><td>LG</td><td>PINN 학습 optimizer 조건화로 로봇 무관함</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2611.25271'>Learning to Verify: Signature-Guided Training for Adaptive Adversarial Detection</a></td><td>28</td><td>0</td><td>LG</td><td>adversarial 탐지 verifier 학습으로 로봇 무관함</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2611.25735'>PosteriorBench: Evaluating Behavior Posterior Sampling in Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>LM 희귀 행동 posterior sampling 벤치마크로 로봇 무관함</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2611.25780'>RouteVerify: Routing Interventions for Step-Level Verification in Mixture-of-Experts Models</a></td><td>28</td><td>0</td><td>NLP</td><td>MoE routing 개입으로 step 검증 해석하는 분석으로 로봇 무관함</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2611.26081'>Learning to Compare Neural Representations from Parameterized Computation Graphs</a></td><td>28</td><td>0</td><td>LG</td><td>신경망 표현 비교 학습으로 로봇 무관함</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2611.26101'>Revealing Pathway Interactions in Network Computations with Complete Path Contribution</a></td><td>28</td><td>0</td><td>LG</td><td>경로 기여 해석 방법으로 로봇 무관함</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2611.26228'>Attention Head Specialization: Phase Transitions in Sample Complexity</a></td><td>28</td><td>0</td><td>LG</td><td>attention head 특화 이론으로 로봇 무관함</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2611.26413'>Sequential Anytime Valid Tests for Efficient Inference-Time Alignment</a></td><td>28</td><td>0</td><td>NLP</td><td>Best-of-N 순차 검정으로 연산 절감하나 로봇 무관함</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2611.26475'>A new algorithmic approach for finding flat minima: critically damped Polyak stepsizes</a></td><td>28</td><td>0</td><td>LG</td><td>flat minima Polyak stepsize 최적화로 로봇 무관함</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2611.24943'>LLM Complexity: Towards a Computational Complexity View of Large Language Model Inference</a></td><td>28</td><td>0</td><td>LLM</td><td>LLM 추론의 계산 복잡도 관점 정리임. 로봇과 무관함</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2611.24971'>The ROI of Small Examples: Optimizing In-Context Learning Under Token Budgets</a></td><td>28</td><td>0</td><td>NLP</td><td>토큰 예산 하 in-context learning 최적화임. 로봇 무관함</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2611.25361'>Incorporating argumentation frameworks for LLM decision-making: Task-specific design and evaluation</a></td><td>28</td><td>0</td><td>NLP</td><td>argumentation framework 기반 LLM 의사결정임. 로봇 무관함</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2611.25582'>AutoRAGBench: A Benchmark for LLM Agents Automating RAG System Development</a></td><td>28</td><td>0</td><td>Agent</td><td>RAG 개발 자동화 agent 벤치마크임. 로봇 무관함</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2611.26286'>Twice-Told Critiques: Claim-Level Homogenization of Peer Review in the LLM Era</a></td><td>28</td><td>0</td><td>NLP</td><td>리뷰 비평의 동질화 측정 연구임. 로봇 무관함</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2611.26317'>Language-Oriented Semantic Modeling for Target Language Extraction</a></td><td>28</td><td>0</td><td>Audio/NLP</td><td>목표 언어 음성 추출 모델링임. 로봇 무관함</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2611.25087'>SailSearch: Agent-Assisted Discovery in Combinatorial Optimization</a></td><td>28</td><td>0</td><td>AI Agent</td><td>조합 최적화에서 agent 보조 알고리즘 탐색임. 로봇 무관함</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2611.25228'>MKA: Evaluating Multimodal Knowledge Agents on end-to-end professional tasks</a></td><td>28</td><td>0</td><td>AI Agent</td><td>시각 이해 기반 전문 업무 agent benchmark임. 로봇 무관함</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2611.25360'>AppSci-Bench: Can LLMs Build AI Agents and Make Them Better?</a></td><td>28</td><td>0</td><td>AI Agent</td><td>LLM의 agent 구축 능력 benchmark임. 로봇 무관함</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2611.25534'>How Feedback-Free Self-Evolution Reshapes Agent Skills: A Systematic Study</a></td><td>28</td><td>0</td><td>AI Agent</td><td>feedback 없는 agent skill 자기 진화 분석임. 로봇 무관함</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2611.25721'>MemMend: A Selective Revision Framework for Memory Question Answering</a></td><td>28</td><td>0</td><td>NLP</td><td>메모리 QA 선택적 수정 프레임워크임. 로봇 무관함</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2611.25896'>The Price of an Explanation: What Demanding Verifiable Artifacts Costs, and What It Buys Back</a></td><td>28</td><td>0</td><td>AI</td><td>검증 가능한 artifact 요구 비용 분석임. 로봇 무관함</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2611.26132'>Sage-Evolve-Preview:Adaptive Observation for Post-Training Self-Improvement</a></td><td>28</td><td>0</td><td>AI Agent</td><td>post-training 자기 개선 적응 관측임. 로봇 무관함</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2611.26248'>TwinLab-Bench: Evaluating AI Scientists in Agentic Twins of Real Labs</a></td><td>28</td><td>0</td><td>AI Agent</td><td>AI scientist 평가용 lab twin benchmark임. 로봇 연결 약함</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2611.26450'>A CPU Inside an LLM: Zero-Gradient Compilation of Exact Circuits into Pretrained Weights</a></td><td>28</td><td>0</td><td>LLM</td><td>사전학습 가중치에 정확 회로를 이식함. 호기심 끄는 방법이나 로봇 무관함</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2611.26557'>MM-SystemOneBias: Evaluating Bias in Multimodal Jev-Style System One Decision Models</a></td><td>28</td><td>0</td><td>Multimodal</td><td>멀티모달 System One 결정 모델 편향 평가임. 로봇 무관함</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2611.25453'>Beyond Resemblance: Image Fusion Reimagined</a></td><td>27</td><td>1</td><td>CV</td><td>이미지 융합 목적함수 재정의임. 로봇과 거리 있음</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2611.25639'>LG-FiLM: Local-Global Mixture-of-Experts Modulation for RAW-to-RGB Reconstruction</a></td><td>27</td><td>1</td><td>CV</td><td>RAW-to-RGB 복원의 MoE 변조임. 로봇 무관하고 incremental임</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2611.25333'>MoGloss: Joint Motion and Pseudo-Gloss Pretraining for American Sign Language Understanding</a></td><td>27</td><td>0</td><td>CV</td><td>수어 이해를 위한 motion/pseudo-gloss 사전학습임. 응용 한정이며 로봇 무관함</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2611.25406'>Decision Boundaries Matter: Graph-Regularized Residual Adaptation for Cross-Domain Fake Image Detection</a></td><td>27</td><td>0</td><td>CV</td><td>fake image 탐지의 cross-domain 적응임. 로봇 무관함</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2611.25418'>Bilateral Evidence Selection and Reasoning for Mammography Vision--Language Models</a></td><td>27</td><td>0</td><td>Multimodal</td><td>유방촬영 VLM의 증거 선택임. 의료 응용으로 로봇 무관함</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2611.25555'>UniReFP: Robust Unified Fingerprinting for Vision Models against Cross-Task Repurposing Attacks</a></td><td>27</td><td>0</td><td>CV</td><td>비전 모델 fingerprint의 cross-task 재활용 공격 대응임. 로봇 무관함</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2611.26116'>Learning Reconstruction Errors as Spatiotemporal Evidence for AI-Generated Video Detection</a></td><td>27</td><td>0</td><td>Video</td><td>AI 생성 영상 탐지임. 로봇 무관함</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2611.26234'>Attention Drift Regularization with Adaptive Initialization for Domain-Robust Visual Recognition</a></td><td>27</td><td>0</td><td>CV</td><td>source-free domain adaptation의 attention drift 정규화임. 일반 분류임</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2611.25665'>GNetSS: Towards Learning GNSS Corrections without Ground Truth</a></td><td>25</td><td>2</td><td>Localization</td><td>라벨 없이 GNSS 보정을 학습함. 로봇 학습 관련성 낮음</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2611.25283'>Persistent Identity in Person Tracking: Online Enrollment and Registered Recognition</a></td><td>25</td><td>1</td><td>CV</td><td>사람 추적 재식별 확장임. 평가가 GT box 기반이고 기여가 작음</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2611.26388'>GateTrace: Where Do Crowd Crossings Go Missing Under Occlusion?</a></td><td>25</td><td>1</td><td>CV</td><td>군중 추적 occlusion 진단 분석으로 novelty와 로봇 관련성 낮음</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2611.25965'>Power Setpoint Tracking for Large-Scale EV Charging: Transformer-Constrained Charging Policy Learning with Self-Tuning Constraint Prices</a></td><td>25</td><td>1</td><td>RL</td><td>EV 충전 제약 RL 정책 학습으로 로봇 무관함</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2611.25043'>Closing the Analyze-to-Design Gap: An Authorization-Bounded Agent for Self-Driving Laboratories</a></td><td>25</td><td>1</td><td>AI Agent</td><td>자율 실험실 agent의 권한 제한 설계임. 로봇 연결 약함</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2611.25325'>Pandora&#x27;s Toolbox Or Why Agent Safety Cannot Be Verified</a></td><td>25</td><td>1</td><td>AI Safety</td><td>LLM agent 안전성 검증 불가능성 이론 논증임. 로봇 연결 약함</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2611.26624'>PlayCraft: Designing Engaging Games from Agent Play Experience</a></td><td>25</td><td>1</td><td>Game AI</td><td>agent 플레이 기반 게임 설계임. 로봇 무관함</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2611.25371'>A Unified Framework for Image Manipulation Localization Under Multi-Type Weak Supervision</a></td><td>25</td><td>0</td><td>CV</td><td>약한 감독 하 이미지 조작 위치 추정 통합 프레임워크임. 로봇 무관하고 incremental임</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2611.25437'>Wearable Logo, Silent Hijack: Stealthy Cross-Modal Semantic Attacks on Visible--Infrared Vision-Language Models</a></td><td>25</td><td>0</td><td>CV</td><td>가시광-적외선 모델에 대한 로고 공격임. 로봇 무관함</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2611.25469'>A Wolf in Sheep&#x27;s Pixels: Visual Camouflage Attacks via HDR Gain Maps</a></td><td>25</td><td>0</td><td>CV</td><td>HDR gain map 이용한 시각 위장 공격임. 로봇 무관함</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2611.25708'>Slide2PPT: Native PowerPoint Reconstruction with Localization-Guided Refinement</a></td><td>25</td><td>0</td><td>CV</td><td>이미지에서 PowerPoint 재구성임. 로봇 무관한 응용임</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2611.25724'>Verifying Before Enhancing: Target Evidence Chain Verification for Infrared Small Target Detection</a></td><td>25</td><td>0</td><td>CV</td><td>적외선 소형 표적 탐지의 증거 검증임. 로봇 무관함</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2611.25822'>Limits of local curvature for constructing search subspaces in segmentation models</a></td><td>25</td><td>0</td><td>LG</td><td>분할 모델 local curvature subspace 한계 분석임. 로봇 무관함</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2611.26179'>RegionAgent: Two-Stage Preference Optimization for Regional Image Restoration</a></td><td>25</td><td>0</td><td>CV</td><td>영역별 이미지 복원의 preference 최적화임. 로봇 무관함</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2611.26254'>Prism: Hierarchical Text Detection with Minimalist Design</a></td><td>25</td><td>0</td><td>CV</td><td>계층적 텍스트 검출임. 로봇 무관함</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2611.25001'>Density Feedback Control for Transferability of Generative Sparse Adversarial Attacks</a></td><td>25</td><td>0</td><td>LG</td><td>sparse adversarial attack 밀도 제어로 로봇 무관함</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2611.25108'>Long-Range Video Presentation Attack Detection: A Three-Class Benchmark Across 1-100 m and Two Sensor Types</a></td><td>25</td><td>0</td><td>CV</td><td>원거리 얼굴 PAD 벤치마크로 로봇 무관함</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2611.25273'>Scone: Symmetry-aware Neural Combinatorial Optimization for Graph Coloring</a></td><td>25</td><td>0</td><td>LG</td><td>graph coloring neural CO로 로봇 무관함</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2611.25311'>Prescribed Bayesian Efficiency under Lifetime Adjustment Costs</a></td><td>25</td><td>0</td><td>LG</td><td>조정 비용 하 Bayesian 학습 이론으로 로봇 무관함</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2611.25463'>Dimension-Free Buffer Bounds for Compressed-Momentum Error Feedback</a></td><td>25</td><td>0</td><td>LG</td><td>error feedback 최적화 이론으로 로봇 무관함</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2611.25650'>Extending Rademacher Complexity-Based Generalization Theory to Domain Generalization</a></td><td>25</td><td>0</td><td>LG</td><td>domain generalization Rademacher 이론으로 로봇 무관함</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2611.26020'>FrontierReplay: Split-Free Exact Prefix Caching for Hybrid Language Models</a></td><td>25</td><td>0</td><td>NLP</td><td>hybrid LM prefix caching 시스템 최적화로 로봇 무관함</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2611.26055'>When Do Rankings Beat Signs? Gradient Direction Recovery under Even Nuisance</a></td><td>25</td><td>0</td><td>LG</td><td>gradient 방향 복원 ranking 이론으로 로봇 무관함</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2611.26201'>Learn, Freeze, and Transfer an Activation Function Across Architectures</a></td><td>25</td><td>0</td><td>CV</td><td>활성화 함수 전이 연구로 로봇 무관함</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2611.26319'>A Control-Theoretic Approximation to Predictive Coding Dynamics</a></td><td>25</td><td>0</td><td>LG</td><td>predictive coding 제어이론 근사로 로봇 무관함</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2611.26359'>Learning from Context: Leave-One-Out Prediction in Jump Diffusions</a></td><td>25</td><td>0</td><td>Generative</td><td>jump diffusion 이산 데이터 생성 이론으로 로봇 무관함</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2611.24960'>TETHER: Training-Free, Elastic, ToC-Anchored Hierarchy Extraction and Recovery in Design-Driven Long Documents</a></td><td>25</td><td>0</td><td>NLP</td><td>긴 문서 계층 구조 추출 방법임. 로봇 무관하고 공학적임</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2611.24970'>HireWatch: Evaluating LLM Compliance with U.S. Employment Law Under Contextual Pressure</a></td><td>25</td><td>0</td><td>NLP</td><td>채용 법규 준수 LLM 평가 벤치마크임. 로봇 무관함</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2611.25557'>The Coverage Selection Gap: Ranking, Not Generation, Limits LLM Rubric Construction</a></td><td>25</td><td>0</td><td>NLP</td><td>rubric 생성에서 순위 선정이 한계임을 분석함. 로봇 무관함</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2611.25643'>TRAC: Efficient Diffusion Language Models for Machine Translation via Length-Aware Decoding</a></td><td>25</td><td>0</td><td>NLP</td><td>diffusion LM 기계번역 길이 인지 디코딩임. 로봇 무관함</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2611.25653'>ColorRef: Calibrating Verbal Feedback for Color Revision</a></td><td>25</td><td>0</td><td>NLP</td><td>색상 수정 언어 피드백 보정임. 언어 피드백 주제와 약하게 닿으나 로봇 무관함</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2611.25970'>The Depth of a Prediction: Where Language Models Resolve a Word Predicts Human Reading Time</a></td><td>25</td><td>0</td><td>NLP</td><td>LM 예측 해소 깊이와 읽기 시간의 관계임. 로봇 무관함</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2611.26000'>Xing-Audio-NVVASR: Scaling and Refining Supervision for Joint Recognition of Speech and Non-Verbal Vocalizations</a></td><td>25</td><td>0</td><td>Speech</td><td>음성과 비언어 발성 공동 인식임. 로봇 무관함</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2611.26073'>AltRA-Test: An Alternative Annotator Test for LLM Judges Without Shared Annotators</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM judge 대체의 통계 검정임. 로봇 무관함</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2611.26255'>STAGE: Spatio-Temporal Augmented Graph Expansion for Weakly Supervised Cross-Tweet Event Causality Discovery</a></td><td>25</td><td>0</td><td>NLP</td><td>재난 트윗 간 인과 발견 약지도 방법임. 도메인 특수하고 로봇 무관함</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2611.26336'>One Framework to Diagnose Them All: A Stratified Benchmark for Bengali LLM Hallucination</a></td><td>25</td><td>0</td><td>NLP</td><td>벵골어 환각 benchmark임. 로봇 무관함</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2611.25146'>EverydayBench: Evaluating Satisfactory Completion of Live User-Facing Digital Work</a></td><td>25</td><td>0</td><td>AI Agent</td><td>일상 디지털 작업 평가 benchmark임. 로봇 무관함</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2611.25492'>Why Do LLMs Help with Scientific Misconduct Requests and What to Do About It?: Increasing the Trustworthiness of AI for Science</a></td><td>25</td><td>0</td><td>AI Safety</td><td>과학 부정행위 요청에 대한 LLM 대응 연구임. 로봇 무관함</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2611.25891'>Meta-RTL: Evolving Agent Harnesses for RTL Optimization</a></td><td>25</td><td>0</td><td>AI Agent</td><td>RTL 최적화 agent harness 진화임. 로봇 무관함</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2611.25903'>From Cases to Criteria: Reusing Evaluation Knowledge for Task-Specific Rubric Generation</a></td><td>25</td><td>0</td><td>NLP</td><td>과제별 rubric 생성임. 로봇 무관함</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2611.26012'>When Agents Play Differently: Localizing Human--Agent Behavioral Divergence with Conditional Distributional Testing</a></td><td>25</td><td>0</td><td>Evaluation</td><td>인간과 agent 행동 분포 차이 검정임. 로봇 무관함</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2611.26171'>The FrontierOR Challenge: Agentic Algorithm Design for Operations Research</a></td><td>25</td><td>0</td><td>AI Agent</td><td>OR 알고리즘 설계 agent 챌린지임. 로봇 무관함</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2611.26335'>ClosureBench: A Benchmark for Reasoning under Closure Assumptions</a></td><td>25</td><td>0</td><td>NLP</td><td>closure 가정 추론 benchmark임. 로봇 무관함</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2611.26485'>An Open-Source ROS 2 Framework for Shared Control in Surgical Teleoperation: Integrating the Haply Inverse3 with the da Vinci Research Kit</a></td><td>22</td><td>3</td><td>Teleoperation</td><td>수술 원격조작 ROS 2 공유 제어 프레임워크임. 학습 연구와 거리 있음</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2611.25578'>QFT-Based Hybrid PointNet-Quantum Neural Networks for LiDAR Point-Cloud Classification</a></td><td>22</td><td>2</td><td>LG</td><td>양자-고전 하이브리드 LiDAR 분류임. 실용성과 증거가 약함</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2611.26262'>Digitization of Analogue Gauges using Computer Vision</a></td><td>22</td><td>2</td><td>CV</td><td>아날로그 계기판 판독 CV 응용임. 단순 응용임</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2611.25508'>Persona Lenses: What Makes a Vision-Language Model See Through Its Persona&#x27;s Eyes?</a></td><td>22</td><td>0</td><td>Multimodal</td><td>VLM persona의 시선 시뮬레이션 분석임. 로봇 무관함</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2611.25593'>Characterizing Age-Conditioned Affective Reasoning in Vision-Language Models</a></td><td>22</td><td>0</td><td>Multimodal</td><td>VLM 연령 조건 감정 추론 분석임. 로봇 무관함</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2611.25730'>CGM: Chaos-Guided Graph Attention and Expert Routing for Autism Stereotypy Detection</a></td><td>22</td><td>0</td><td>CV</td><td>자폐 상동행동 탐지용 skeleton attention임. 로봇 무관함</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2611.25761'>AdaptReg: Skip-level FiLM Adapter for Task-Specific Adaptation of a Frozen Registration Foundation Model</a></td><td>22</td><td>0</td><td>CV</td><td>PET/CT 정합용 adapter임. 의료이며 로봇 무관함</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2611.25840'>Harnessing Medical Visual-Language Models with Agentic Evidence Management</a></td><td>22</td><td>0</td><td>Multimodal</td><td>의료 VLM agent의 증거 관리임. 로봇 무관함</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2611.25902'>Does It Depend on the Split? Frozen Satellite Features vs. Fine-Tuned CNNs for Tree Species Mapping</a></td><td>22</td><td>0</td><td>CV</td><td>위성 frozen feature 대 fine-tuned CNN 비교임. 로봇 무관함</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2611.25935'>TwinD: Generalizing Deepfake Detection from Blending to Entire Face Synthesis</a></td><td>22</td><td>0</td><td>CV</td><td>deepfake 탐지의 전체 얼굴 합성 일반화임. 로봇 무관함</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2611.25975'>Sample-efficient end-to-end Optical Music Recognition through Active Learning</a></td><td>22</td><td>0</td><td>CV</td><td>악보 인식의 active learning임. 로봇 무관함</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2611.26128'>CryoGaussian: Heterogeneous Cryo-EM Reconstruction Made Explicit with Gaussian Splatting</a></td><td>22</td><td>0</td><td>3D Vision</td><td>cryo-EM 이종 재구성에 Gaussian splatting 적용임. 로봇 무관함</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2611.26316'>C-LiTE: A Lightweight Foundation Model for Cellular feature learning in Histopathology</a></td><td>22</td><td>0</td><td>CV</td><td>조직병리 세포 foundation model임. 로봇 무관함</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2611.26386'>SEEC: A Large-Scale Dataset and Benchmark for Self-Supervised External-Eye Representation Learning</a></td><td>22</td><td>0</td><td>CV</td><td>안구 외부 사진 자기지도 데이터셋으로 로봇 무관함</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2611.25004'>On the Impact of Feature Reduction Techniques on Adversarial Attacks</a></td><td>22</td><td>0</td><td>LG</td><td>feature reduction과 adversarial attack 영향 실험으로 novelty 낮음</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2611.25264'>Process-Knowledge-Guided Latent Diffusion for Generative Design of Porous Architectures: A Case Study in Aerosol Jet Printing</a></td><td>22</td><td>0</td><td>Generative</td><td>다공성 구조 생성 설계 응용으로 로봇 무관함</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2611.25570'>Reinforcement-Aligned Probabilistic Weather Forecasting with Discrete Tokens</a></td><td>22</td><td>0</td><td>LG</td><td>이산 토큰 기상 예보로 로봇 무관함</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2611.25624'>Deviations from the NTK Regime in CNNs under Joint Depth-Width Scaling</a></td><td>22</td><td>0</td><td>LG</td><td>CNN NTK 이론으로 로봇 무관함</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2611.26018'>Does the Workspace Do the Work? A Causal Protocol for Verifying Global-Workspace Computation in a Language Model</a></td><td>22</td><td>0</td><td>NLP</td><td>global workspace 인과 검증 프로토콜로 로봇 무관함</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2611.26104'>How Network Topology and Data Heterogeneity Shape Decentralized Learning: A Spectral Analysis</a></td><td>22</td><td>0</td><td>LG</td><td>분산 학습 토폴로지 스펙트럼 분석으로 로봇 무관함</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2611.26419'>FEA solver integration of a composite World Model with a Spiking Neural Network memory Block for computationally efficient modelling of defects and variabilities</a></td><td>22</td><td>0</td><td>LG</td><td>복합재 FEA와 spiking memory world model 응용으로 로봇 무관함</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2611.24959'>ICARE: cross-domain text classification with incremental class-aware representation and distillation learning</a></td><td>22</td><td>0</td><td>NLP</td><td>NLI 교차 도메인 분류의 증분 표현·증류임. incremental 성격이고 로봇 무관함</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2611.25314'>Enhancing Understanding of Language Models with Varied Explanations</a></td><td>22</td><td>0</td><td>NLP</td><td>다양한 설명이 LM 이해에 주는 영향임. 로봇 무관함</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2611.25446'>PAIR-MED: Policy-reward Alternation for Iterative Refinement in Multilingual Medical Reasoning</a></td><td>22</td><td>0</td><td>NLP</td><td>다국어 의료 추론용 policy-reward 교대 학습임. 로봇 무관함</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2611.25459'>PILAPS: A Bilingual Benchmark for Evaluating Pragmatic Inference across Phenomena and Settings</a></td><td>22</td><td>0</td><td>NLP</td><td>이중 언어 화용 추론 벤치마크임. 로봇 무관함</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2611.25521'>DRVEXO-4B-Unified: Design and Evaluation of a Modular Speech-Vision System</a></td><td>22</td><td>0</td><td>Multimodal</td><td>4B 음성·비전 모듈형 시스템 설계·평가임. 로봇 무관함</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2611.25853'>TableRoute: Capability-Aware Routing for Scalable Table Question Answering</a></td><td>22</td><td>0</td><td>NLP</td><td>표 QA 능력 인지 라우팅임. 로봇 무관함</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2611.26069'>SheetAlign: Grounded Interaction and Stage-Isolated Learning for Spreadsheet Agents</a></td><td>22</td><td>0</td><td>Agent</td><td>스프레드시트 agent 학습임. 로봇 무관함</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2611.26492'>Multimodal Error Detection in Chest X-ray Reports: A Large Language Model Reading Image Evidence</a></td><td>22</td><td>0</td><td>Medical NLP</td><td>흉부 X-ray 보고서 오류 검출임. 로봇 무관함</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2611.25109'>CoMPASS: A Multi-Turn Benchmark for Measuring LLM Reinforcement of Parasocial Behavior</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM의 parasocial 행동 강화 benchmark임. 로봇 무관함</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2611.25111'>DSFlow: A Neuro-Symbolic Data Workflow Agent with Statistical Diagnostic Guardrails</a></td><td>22</td><td>0</td><td>AI Agent</td><td>데이터 워크플로 agent 응용임. 로봇 무관함</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2611.25404'>Toward a Science of AI Agent Societies</a></td><td>22</td><td>0</td><td>AI Agent</td><td>AI agent 사회 과학 position 논문임. 로봇 무관함</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2611.25651'>MatVerse: A Foundation Model for Materials Science</a></td><td>22</td><td>0</td><td>Science FM</td><td>재료과학 foundation model임. 로봇 무관함</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2611.25669'>Ask in the Crowd: Differentially Private LLM Inference via Dummy-Augmented Shuffling</a></td><td>22</td><td>0</td><td>Privacy</td><td>LLM 추론 차등 프라이버시임. 로봇 무관함</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2611.25839'>Self-Replicating Language Models</a></td><td>22</td><td>0</td><td>AI</td><td>자기복제 언어 모델 논의임. 로봇 무관함</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2611.26332'>Rigel-Ladon: An Option-Count Law for a One-Pass Decision Encoder, Tested on Held-Out Option Counts and Held-Out Schemas</a></td><td>22</td><td>0</td><td>LG</td><td>one-pass decision encoder option 수 법칙임. 로봇 무관함</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2611.26346'>Context as a Resource</a></td><td>22</td><td>0</td><td>AI Agent</td><td>agent 세션 컨텍스트 자원 관리임. 로봇 무관함</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2611.26146'>A Practical Proprioceptive Data Collection Utility for the Unitree GO1</a></td><td>20</td><td>3</td><td>Tool</td><td>Unitree Go1 고유감각 데이터 수집 유틸리티임. 엔지니어링 도구임</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2611.25249'>A Synthetic Multi-Modal Testbed for Security Stress Testing of Agentic Counter-UAS Systems</a></td><td>20</td><td>2</td><td>Security</td><td>counter-UAS 보안 stress test용 synthetic testbed임. 로봇 학습과 거리 멀고 기여는 도구 수준임</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2611.25558'>Communication-Aware UAV Spatio-Temporal Relay Cooperation and Planning in Complex Urban Environments</a></td><td>20</td><td>2</td><td>UAV</td><td>통신 인지 UAV 릴레이 계획임. 학습 로봇 주제와 거리 멀음</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2611.25921'>A Lightweight Hybrid Approach for Milling Force Reconstruction from Internal Machine Signals</a></td><td>20</td><td>1</td><td>LG</td><td>밀링 힘 복원 하이브리드 접근으로 제조 응용임</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2611.25672'>SEAF: Selective Semantic Enrichment and Visual Evidence Fusion for Multimodal Sarcasm Detection</a></td><td>20</td><td>0</td><td>NLP</td><td>멀티모달 풍자 탐지임. 로봇 무관함</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2611.25824'>Fusing Multimodal CNN Features with Structurally-Masked Transformers for Hierarchical Sub-Pixel Tree Species Mapping</a></td><td>20</td><td>0</td><td>CV</td><td>위성 초분광 산림 수종 매핑임. 로봇 무관함</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2611.26249'>Beyond Covers and Titles: Evidence-First Ranking for Robust Cold-Start Recommendation</a></td><td>20</td><td>0</td><td>CV</td><td>cold-start 추천 공격임. 로봇 무관함</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2611.26456'>Fixing the Last Mile: Failure-Aware Image Restoration with Region-Specific Guidance</a></td><td>20</td><td>0</td><td>CV</td><td>이미지 복원의 국소 실패 보정으로 incremental이며 로봇 무관함</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2611.25288'>Intelligent Embedding Pruning for Large-Scale Recommendation Models</a></td><td>20</td><td>0</td><td>LG</td><td>추천 모델 embedding pruning으로 로봇 무관함</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2611.25514'>Sequential Probability Assignment against Smoothed Adversaries with Unknown Base Measure</a></td><td>20</td><td>0</td><td>LG</td><td>smoothed adversary 확률 할당 이론으로 로봇 무관함</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2611.25603'>On the Informativeness of Structural Stability Bounds for GNNs: GINs versus GATs</a></td><td>20</td><td>0</td><td>LG</td><td>GNN 안정성 bound 이론으로 로봇 무관함</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2611.25848'>Interpretable Prototype-Conditioned Adaptation for Weather Forecasting</a></td><td>20</td><td>0</td><td>CV</td><td>프로토타입 조건 기상 예보로 로봇 무관함</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2611.26355'>Mamba Flow Matching Neural Processes: Linear-Time Inference for Irregularly Observed Spatial Fields</a></td><td>20</td><td>0</td><td>LG</td><td>Mamba flow matching 공간장 보간으로 로봇 무관함</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2611.25258'>When Objectives and Evaluators Disagree: Evaluating Transfer for Post-hoc Demographic Framing Mitigation</a></td><td>20</td><td>0</td><td>NLP</td><td>인구통계 프레이밍 완화 전이 평가임. 로봇 무관함</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2611.25808'>Language models represent more about emphasis than they can tell you</a></td><td>20</td><td>0</td><td>NLP</td><td>LM의 강조 표현 분석임. 로봇 무관함</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2611.25898'>Verifiable Logic in Medical LLMs: A Critical Review of Agentic Clinical Reasoning Optimization and Neuro-Symbolic Grounding</a></td><td>20</td><td>0</td><td>NLP</td><td>의료 LLM 추론 검증 가능성 리뷰임. 서베이이고 로봇 무관함</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2611.25070'>An LLM-Agentic Framework for Intelligent Work Order Management in Industrial Maintenance</a></td><td>20</td><td>0</td><td>AI Agent</td><td>산업 정비 작업지시 LLM agent 응용임. 로봇 무관함</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2611.25393'>The Coevolution and Coexistence of Humans and AI</a></td><td>20</td><td>0</td><td>AI</td><td>인간과 AI 공진화 논의글임. 로봇 무관함</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2611.25489'>When Should a Voice Agent Speak? End-of-Turn Detection in Turkish</a></td><td>20</td><td>0</td><td>Speech</td><td>터키어 end-of-turn 검출임. 로봇 무관함</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2611.25619'>Cyber-Physical RSI for AI-RAN: A Case Study</a></td><td>20</td><td>0</td><td>Wireless</td><td>AI-RAN 사례 연구임. 로봇 무관함</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2611.26029'>Serialization Tax in Shared-Latent Exchangeable Decisions</a></td><td>20</td><td>0</td><td>LG</td><td>그룹 결정 확률 직렬화 이론임. 로봇 무관함</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2611.26339'>Sirius-Tiamat: How Small Can a One-Pass Decision Encoder Get Before Its Decisions Change?</a></td><td>20</td><td>0</td><td>LG</td><td>decision encoder 축소 한계 실험임. 로봇 무관함</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2611.26343'>DeepQuest: From Knowledge Gaps to Scientific Discovery in Alzheimer&#x27;s Disease</a></td><td>20</td><td>0</td><td>AI Agent</td><td>알츠하이머 지식 공백 agent임. 로봇 무관함</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2611.26562'>Multi-institutional grading of Barrett&#x27;s esophagus dysplasia without stain normalization using a pathology foundation model and multiple instance learning</a></td><td>18</td><td>0</td><td>CV</td><td>병리 이미지 등급 판정 임상 연구로 로봇 무관함</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2611.25300'>Federated Learning of Car Aerodynamics Surrogates with Spectral Optimizers</a></td><td>18</td><td>0</td><td>LG</td><td>자동차 공력 surrogate의 federated 학습으로 로봇 무관함</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2611.25301'>SplitReAlign: Partition-Aware Representation Realignment for Split Federated Unlearning</a></td><td>18</td><td>0</td><td>LG</td><td>split federated unlearning으로 로봇 무관함</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2611.25342'>Class-Conditional Conformal Triage for ICAO Face-Image Compliance under Class Imbalance</a></td><td>18</td><td>0</td><td>CV</td><td>얼굴 이미지 compliance conformal triage로 로봇 무관함</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2611.25396'>Protein Functional Semantic Alignment via Representation Rectification</a></td><td>18</td><td>0</td><td>LG</td><td>단백질 언어모델 표현 정렬로 로봇 무관함</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2611.25592'>From Data Alignment to Parameter Generation: Few-Shot Cross-City Traffic Prediction with Conditional Diffusion</a></td><td>18</td><td>0</td><td>LG</td><td>도시 간 트래픽 예측 파라미터 생성으로 로봇 무관함</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2611.25607'>PSTO: A PDE-structured transport operator with shared implicit updates for multiscale CDR systems</a></td><td>18</td><td>0</td><td>LG</td><td>PDE transport operator surrogate로 로봇 무관함</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2611.25692'>Measurable Does Not Imply Transportable: A Prospective Audit of Model Explanations in Multi-Year Field Trials</a></td><td>18</td><td>0</td><td>LG</td><td>설명 전이성 현장 audit으로 로봇 무관함</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2611.25831'>Beyond Alignment: Whitening Geometry, Profile Synthesis, and Heterogeneous Ensembles for Cross-Environment WiFi Action Recognition</a></td><td>18</td><td>0</td><td>LG</td><td>WiFi 행동 인식 도메인 일반화로 로봇 무관함</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2611.25874'>Parameter-Efficient Adaptation of Self-supervised Vision Backbones Survives Distribution Shift in Radar Micro-Doppler HAR</a></td><td>18</td><td>0</td><td>LG</td><td>레이더 micro-Doppler HAR PEFT 비교로 로봇 무관함</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2611.25942'>Gradient Boosting with Kolmogorov-Arnold Units for Interpretable Regression beyond Pairwise Interactions</a></td><td>18</td><td>0</td><td>LG</td><td>Kolmogorov-Arnold 단위 gradient boosting 회귀로 로봇 무관함</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2611.25986'>Seeing Beyond the Obvious: Complementary Semantic Guidance for Salient Single-Positive Multi-Label Learning</a></td><td>18</td><td>0</td><td>CV</td><td>single-positive multi-label 학습으로 로봇 무관함</td></tr>
<tr><td>486</td><td><a href='https://arxiv.org/abs/2611.26060'>Iterative Scarcity-Guided Exploration: Bootstrapping Generative Auto-bidding from Narrow Support</a></td><td>18</td><td>0</td><td>LG</td><td>auto-bidding 탐험으로 로봇 무관함</td></tr>
<tr><td>487</td><td><a href='https://arxiv.org/abs/2611.26333'>OceanCoder: A Verification-Guided Large Language Model for Automated Simulation Modelling in Ocean Engineering</a></td><td>18</td><td>0</td><td>NLP</td><td>해양공학 시뮬레이션 LLM 코드 생성으로 로봇 무관함</td></tr>
<tr><td>488</td><td><a href='https://arxiv.org/abs/2611.26351'>TRCF: Temporal-Reference Complementary Forecasting for Irregular Multivariate Time Series</a></td><td>18</td><td>0</td><td>LG</td><td>불규칙 시계열 예측으로 로봇 무관함</td></tr>
<tr><td>489</td><td><a href='https://arxiv.org/abs/2611.26383'>Evidence from a Multi-Regime Causal Discovery Benchmark: UCMT Algorithms, Comparative Performance, and Controlled Ablation Studies</a></td><td>18</td><td>0</td><td>LG</td><td>인과 탐색 알고리즘 내부 벤치마크로 로봇 무관함</td></tr>
<tr><td>490</td><td><a href='https://arxiv.org/abs/2611.24972'>No-Harm-Jury A Jury-Based Multi-Dimensional Harm Evaluation Framework for Medical AI Responses</a></td><td>18</td><td>0</td><td>NLP</td><td>의료 AI 응답 피해 평가 프레임워크임. 로봇 무관함</td></tr>
<tr><td>491</td><td><a href='https://arxiv.org/abs/2611.24981'>Quantifying Cultural-Psychological Constructs in Four Centuries of Ottoman Court Registers</a></td><td>18</td><td>0</td><td>NLP</td><td>오스만 문서의 문화 심리 구성 정량화임. 로봇 무관함</td></tr>
<tr><td>492</td><td><a href='https://arxiv.org/abs/2611.25184'>An AI-Powered Multiverse Analysis of Empirical Finance Research: Evidence from Reused Natural Experiments</a></td><td>18</td><td>0</td><td>AI Agent</td><td>금융 연구 multiverse 분석임. 로봇 무관함</td></tr>
<tr><td>493</td><td><a href='https://arxiv.org/abs/2611.25198'>When AI Analysts Disagree: Agentic Multiverse Analysis and the Robustness of Empirical Research</a></td><td>18</td><td>0</td><td>AI Agent</td><td>실증 연구 robustness agentic 분석임. 로봇 무관함</td></tr>
<tr><td>494</td><td><a href='https://arxiv.org/abs/2611.25502'>Coordinated Use of Large Language Models in Academic Research</a></td><td>18</td><td>0</td><td>AI</td><td>다중 LLM 학술 활용 방법론 글임. 로봇 무관함</td></tr>
<tr><td>495</td><td><a href='https://arxiv.org/abs/2611.25590'>Measuring Hallucination in Large Language Models for Cyber Threat Intelligence: An Exploratory Study</a></td><td>18</td><td>0</td><td>NLP</td><td>사이버 위협 정보 LLM 환각 측정임. 로봇 무관함</td></tr>
<tr><td>496</td><td><a href='https://arxiv.org/abs/2611.25754'>ADAPT: Adaptive Decision and Abstention with Pool-Size-Aware Thresholds for Service Routing</a></td><td>18</td><td>0</td><td>NLP</td><td>서비스 라우팅 abstention임. 로봇 무관함</td></tr>
<tr><td>497</td><td><a href='https://arxiv.org/abs/2611.25818'>Anchor and Check: Deterministic Cross-Prompt, Cross-Model Reconciliation for Auditable LLM Decisions</a></td><td>18</td><td>0</td><td>NLP</td><td>LLM 결정 감사 reconciliation임. 로봇 무관함</td></tr>
<tr><td>498</td><td><a href='https://arxiv.org/abs/2611.25905'>Validation-driven Deployment of LLM Inference Platforms for Agentic Workloads</a></td><td>18</td><td>0</td><td>Systems</td><td>LLM 추론 플랫폼 검증임. 로봇 무관함</td></tr>
<tr><td>499</td><td><a href='https://arxiv.org/abs/2611.25725'>On the Hamel Coefficients and the Boltzmann-Hamel Equations for the Rigid Body</a></td><td>15</td><td>1</td><td>Dynamics</td><td>강체 Boltzmann-Hamel 방정식 이론 분석임. 학습 로봇과 무관함</td></tr>
<tr><td>500</td><td><a href='https://arxiv.org/abs/2611.25798'>Design and Validation of a Telescopic Chassis-Assisted Stair-Climbing Mechanism for Powered Wheelchairs</a></td><td>15</td><td>1</td><td>Mechanism</td><td>휠체어 계단 오르기 기구 설계임. 학습 연구와 무관함</td></tr>
<tr><td>501</td><td><a href='https://arxiv.org/abs/2611.26195'>A version of the Cloude/van Zyl decomposition for full/quad pol synthetic aperture radar data</a></td><td>15</td><td>0</td><td>CV</td><td>편광 SAR 분해 기법임. 로봇 무관함</td></tr>
<tr><td>502</td><td><a href='https://arxiv.org/abs/2611.26367'>Contactless Estimation of Respiratory Frequency Using 3D-CNN on Thermal Images</a></td><td>15</td><td>0</td><td>CV</td><td>열화상 호흡수 추정임. 로봇 무관함</td></tr>
<tr><td>503</td><td><a href='https://arxiv.org/abs/2611.26522'>Deterministic Temporal Embedding for Calcium Imaging Trace Extraction</a></td><td>15</td><td>0</td><td>CV</td><td>calcium imaging trace 추출로 로봇 무관함</td></tr>
<tr><td>504</td><td><a href='https://arxiv.org/abs/2611.25327'>Now You See Me Now You Don&#x27;t: A Framework To Detect and Reduce Proxy Capacity</a></td><td>15</td><td>0</td><td>LG</td><td>대출 공정성 proxy 탐지로 로봇 무관함</td></tr>
<tr><td>505</td><td><a href='https://arxiv.org/abs/2611.25403'>Antom 3-in-1 Transformer: A Payment Foundation Model</a></td><td>15</td><td>0</td><td>LG</td><td>결제 foundation model로 로봇 무관함</td></tr>
<tr><td>506</td><td><a href='https://arxiv.org/abs/2611.25422'>From Sequence Uncertainty to Phenotype Hypotheses: Uncertainty-Conditioned Inference over Biomedical Knowledge Graphs</a></td><td>15</td><td>0</td><td>LG</td><td>유전체 지식그래프 추론으로 로봇 무관함</td></tr>
<tr><td>507</td><td><a href='https://arxiv.org/abs/2611.25452'>FamilySpace: From Emergent Chemical Semantics to Controllable Crystal Generation</a></td><td>15</td><td>0</td><td>Generative</td><td>결정 구조 생성 모델로 로봇 무관함</td></tr>
<tr><td>508</td><td><a href='https://arxiv.org/abs/2611.25796'>How Reliable Are Explanations of Language Models That Detect Insider Threats?</a></td><td>15</td><td>0</td><td>LG</td><td>내부자 위협 탐지 설명 신뢰성으로 로봇 무관함</td></tr>
<tr><td>509</td><td><a href='https://arxiv.org/abs/2611.25826'>A Sparse Low-Rank Biclique Decomposition for Graphs</a></td><td>15</td><td>0</td><td>LG</td><td>그래프 biclique 분해로 로봇 무관함</td></tr>
<tr><td>510</td><td><a href='https://arxiv.org/abs/2611.25917'>LIFT: Latent Flow Matching for Probabilistic Cell Fate Dynamics with Single Cell Snapshots</a></td><td>15</td><td>0</td><td>LG</td><td>세포 운명 flow matching으로 로봇 무관함</td></tr>
<tr><td>511</td><td><a href='https://arxiv.org/abs/2611.26030'>The Delayed Societal Cost of Unfairness</a></td><td>15</td><td>0</td><td>LG</td><td>공정성의 지연된 사회적 비용으로 로봇 무관함</td></tr>
<tr><td>512</td><td><a href='https://arxiv.org/abs/2611.26114'>Loss-Guided Tsetlin Machines: Making the Learning Objective Explicit</a></td><td>15</td><td>0</td><td>LG</td><td>Tsetlin Machine 손실 명시로 로봇 무관함</td></tr>
<tr><td>513</td><td><a href='https://arxiv.org/abs/2611.26323'>Predicting Surface Displacement Fields of Laser Powder Bed Fusion Parts Using STL-Derived Graphs and Part-Level Descriptors</a></td><td>15</td><td>0</td><td>LG</td><td>LPBF 변형 예측 GAT로 로봇 무관함</td></tr>
<tr><td>514</td><td><a href='https://arxiv.org/abs/2611.26521'>The Window Lever: Longer Observation Windows Outweigh the Observed Effects of Data, Capacity, and Architecture in Customer Behavior Forecasting</a></td><td>15</td><td>0</td><td>LG</td><td>고객 행동 예측 관측 창 분석으로 로봇 무관함</td></tr>
<tr><td>515</td><td><a href='https://arxiv.org/abs/2611.25682'>FoodReact-AR: Learning Audience Reactions that Zero-Shot LLMs Miss in Arabic Food-Insecurity Discourse</a></td><td>15</td><td>0</td><td>NLP</td><td>아랍어 식량 불안 담론 반응 학습임. 로봇 무관함</td></tr>
<tr><td>516</td><td><a href='https://arxiv.org/abs/2611.25745'>Verification Behavior Across Five Qwen2.5-Instruct Checkpoints</a></td><td>15</td><td>0</td><td>NLP</td><td>Qwen2.5 검증 행동 소규모 평가임. 증거 약하고 로봇 무관함</td></tr>
<tr><td>517</td><td><a href='https://arxiv.org/abs/2611.25862'>HALTT: A HAte Lexicon Through Time</a></td><td>15</td><td>0</td><td>NLP</td><td>시간에 따른 혐오 어휘 사전임. 로봇 무관함</td></tr>
<tr><td>518</td><td><a href='https://arxiv.org/abs/2611.25909'>The Linguistic Structure of Dependency-Conditioned Embeddings</a></td><td>15</td><td>0</td><td>NLP</td><td>의존 조건 임베딩의 언어 구조 분석임. 로봇 무관함</td></tr>
<tr><td>519</td><td><a href='https://arxiv.org/abs/2611.25955'>Web search in Latin America: language models use less local and diverse news than search engines</a></td><td>15</td><td>0</td><td>NLP</td><td>중남미 뉴스 검색에서 LM의 지역 다양성 분석임. 로봇 무관함</td></tr>
<tr><td>520</td><td><a href='https://arxiv.org/abs/2611.25236'>A Neurosymbolic Multimodal Framework for 30-Day Diabetic Readmission Prediction: Integrating Structured EHR Data, Dense Clinical Embeddings, and Knowledge-Grounded Symbolic Extraction</a></td><td>15</td><td>0</td><td>Medical</td><td>당뇨 재입원 예측 응용임. 로봇 무관함</td></tr>
<tr><td>521</td><td><a href='https://arxiv.org/abs/2611.25531'>LM-based Personalized Travel Planner</a></td><td>15</td><td>0</td><td>AI Agent</td><td>여행 계획 LLM 응용임. 로봇 무관함</td></tr>
<tr><td>522</td><td><a href='https://arxiv.org/abs/2611.26309'>Client Exits - A Way to Increase LLM Transparency on the Client Side</a></td><td>15</td><td>0</td><td>LLM</td><td>LLM 투명성 Client Exits임. 로봇 무관함</td></tr>
<tr><td>523</td><td><a href='https://arxiv.org/abs/2611.26538'>LLM GerryMandering: Separating Interactions from Additive Effects in LLM Audits</a></td><td>15</td><td>0</td><td>Fairness</td><td>LLM 교차 편향 감사임. 로봇 무관함</td></tr>
<tr><td>524</td><td><a href='https://arxiv.org/abs/2611.25114'>Fast and Memory-Light Evaluation of Density-Based Clusterings with the DISCO Index in R</a></td><td>12</td><td>0</td><td>LG</td><td>R 패키지 클러스터링 지표 구현으로 연구 기여 낮음</td></tr>
<tr><td>525</td><td><a href='https://arxiv.org/abs/2611.25577'>Design and Evaluation of Epira: An Automated Interview System for Case Investigation and Contact Tracing</a></td><td>12</td><td>0</td><td>NLP</td><td>접촉 추적 자동 인터뷰 시스템으로 로봇 무관함</td></tr>
<tr><td>526</td><td><a href='https://arxiv.org/abs/2611.25625'>QUBO-based feature selection for MRI undersampling pattern design</a></td><td>12</td><td>0</td><td>LG</td><td>MRI undersampling QUBO 설계로 로봇 무관함</td></tr>
<tr><td>527</td><td><a href='https://arxiv.org/abs/2611.25629'>NIMIS: A Structure-Agnostic, Chemically Informed Slot-Attention Framework for Demixing 1D $^1$H-NMR Mixture Spectra</a></td><td>12</td><td>0</td><td>LG</td><td>NMR 스펙트럼 분리로 로봇 무관함</td></tr>
<tr><td>528</td><td><a href='https://arxiv.org/abs/2611.25681'>Explainability of genotype embedding models through observed cohort paths</a></td><td>12</td><td>0</td><td>LG</td><td>유전자 embedding 설명성으로 로봇 무관함</td></tr>
<tr><td>529</td><td><a href='https://arxiv.org/abs/2611.25765'>Disentangling Monitor Hardware Artifacts and Smoothing Lag for Shift-Robust Intraoperative EEG and Hemodynamic Risk Calibration</a></td><td>12</td><td>0</td><td>LG</td><td>수술 중 EEG 위험 보정으로 로봇 무관함</td></tr>
<tr><td>530</td><td><a href='https://arxiv.org/abs/2611.25870'>X Hedging: towards an eXplainable artificial intelligence option Hedging framework</a></td><td>12</td><td>0</td><td>LG</td><td>옵션 hedging 설명가능 프레임워크로 로봇 무관함</td></tr>
<tr><td>531</td><td><a href='https://arxiv.org/abs/2611.26183'>Thermodynamically Consistent Neural Networks for a Universal Fluid Gibbs Free Energy Equation of State</a></td><td>12</td><td>0</td><td>LG</td><td>유체 상태방정식 신경망으로 로봇 무관함</td></tr>
<tr><td>532</td><td><a href='https://arxiv.org/abs/2611.26369'>From Benchmarks to the Bench: Preference, Correspondence and Selectivity in Bidirectional Drug-Target Screening</a></td><td>12</td><td>0</td><td>LG</td><td>약물-표적 스크리닝 평가로 로봇 무관함</td></tr>
<tr><td>533</td><td><a href='https://arxiv.org/abs/2611.26514'>Hybrid Retrieval for Government Scheme Search in English and Marathi</a></td><td>12</td><td>0</td><td>NLP</td><td>정부 제도 검색 시스템으로 로봇 무관함</td></tr>
<tr><td>534</td><td><a href='https://arxiv.org/abs/2611.25976'>Energy estimates of open-weight large language models across stated food weights: a dose-response evaluation</a></td><td>12</td><td>0</td><td>NLP</td><td>음식 중량별 LLM 에너지 추정 평가임. 로봇 무관함</td></tr>
<tr><td>535</td><td><a href='https://arxiv.org/abs/2611.25652'>Multiple Criteria Decision Making Under XORness</a></td><td>12</td><td>0</td><td>Decision</td><td>다기준 의사결정 이론임. 로봇 무관함</td></tr>
<tr><td>536</td><td><a href='https://arxiv.org/abs/2611.25841'>Whose Risks Count? What 1,901 AI Incidents Reveal About Corporate Disclosures</a></td><td>12</td><td>0</td><td>AI Policy</td><td>AI 사고 공시 분석임. 로봇 무관함</td></tr>
<tr><td>537</td><td><a href='https://arxiv.org/abs/2611.25879'>Coherent belief and opinion propagation produces more echo chambers: corrected version</a></td><td>12</td><td>0</td><td>Social</td><td>echo chamber 정정 논문임. 로봇 무관함</td></tr>
<tr><td>538</td><td><a href='https://arxiv.org/abs/2611.25884'>Trustworthy Geospatial AI Workflows: Reproducible Maritime Analytics and Forecasting on Open-Source AIS Data</a></td><td>12</td><td>0</td><td>Geospatial</td><td>해양 AIS 분석 재현성임. 로봇 무관함</td></tr>
<tr><td>539</td><td><a href='https://arxiv.org/abs/2611.25894'>Explainable AI for Solar PV Power Forecasting: From Model Selection to Trustworthy, Reproducible Deployment</a></td><td>12</td><td>0</td><td>Application</td><td>태양광 발전 예측 XAI임. 로봇 무관함</td></tr>
<tr><td>540</td><td><a href='https://arxiv.org/abs/2611.25991'>From AI Surrogate to Engineering Tool: Toward Production Use of Fiber-Orientation Prediction in Crash CAE</a></td><td>12</td><td>0</td><td>Engineering</td><td>충돌 CAE 섬유 배향 예측임. 로봇 무관함</td></tr>
<tr><td>541</td><td><a href='https://arxiv.org/abs/2611.26033'>SEOYUN: Refusal-Inducing Exam Documents for AI-Glasses Pipelines</a></td><td>12</td><td>0</td><td>Security</td><td>시험 문서 VLM 거부 유도임. 로봇 무관함</td></tr>
<tr><td>542</td><td><a href='https://arxiv.org/abs/2611.26235'>Physics-Informed Feature Representations and Pretrained Tabular Foundation Models for Generalizable Melt Pool Geometry Prediction</a></td><td>12</td><td>0</td><td>Manufacturing</td><td>용융 풀 형상 예측임. 로봇 무관함</td></tr>
<tr><td>543</td><td><a href='https://arxiv.org/abs/2611.26422'>Reasoning-Trace Analysis Using Large Language Models for Interpretable Q-Matrix Construction</a></td><td>12</td><td>0</td><td>Education</td><td>Q-matrix 구성 추론 분석임. 로봇 무관함</td></tr>
<tr><td>544</td><td><a href='https://arxiv.org/abs/2611.25450'>Inverse ECG Reconstruction via a Preconditioned Variational Quantum Linear Solver</a></td><td>10</td><td>0</td><td>LG</td><td>양자 선형 solver로 ECG 복원하는 의료 응용으로 로봇 무관함</td></tr>
<tr><td>545</td><td><a href='https://arxiv.org/abs/2611.26108'>Pareto-Optimal and Strategyproof Data-Sharing Between Competitors</a></td><td>10</td><td>0</td><td>Game Theory</td><td>기업 간 데이터 공유 메커니즘임. 로봇 무관함</td></tr>
<tr><td>546</td><td><a href='https://arxiv.org/abs/2611.26261'>Similarity-based OSF Logic for Flexible SPARQL Query Answering</a></td><td>10</td><td>0</td><td>Knowledge</td><td>퍼지 OSF 논리 SPARQL 추론기임. 로봇 무관함</td></tr>
<tr><td>547</td><td><a href='https://arxiv.org/abs/2611.26050'>Studying AI Act Mentions: A first look at the impact of the European Union&#x27;s AI regulation on Hugging Face</a></td><td>8</td><td>0</td><td>Policy</td><td>AI Act 언급 분석임. 로봇 무관함</td></tr>
</tbody></table>

</details>
