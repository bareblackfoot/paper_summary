# 오늘의 arXiv Top 15: 2026-10-28 (수)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**

**신규 논문 수: 전체 484편 → 중복 제거 후 484편 (이번 평가 대상 484편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 124 |
| cs.LG | 137 |
| cs.RO | 74 |
| cs.CL | 52 |
| cs.AI | 97 |

---

## Top 15

### 1. Rollback: Experience Backtracking in World Models for Policy Improvement (85점)

[arXiv](https://arxiv.org/abs/2610.36068) · [PDF](https://arxiv.org/pdf/2610.36068) · [alphaXiv](https://www.alphaxiv.org/abs/2610.36068) (요약 있음) · [프로젝트 페이지](https://rollback-wm.github.io/)

- **저자**: Jiayi Luo, Yang Zhang, Liliang Chen, Nan Wang, Chen Gao, Boxiang Qiu, Zhuoxuan Li, Baorui Peng 외 8명
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 88점
- **읽은 원문**: PDF 전문

> 학습된 world model 안에서 과거 결정 시점으로 돌아가 다른 action을 시험하고, 결과 차이로 action 단위 학습 label을 만들어 로봇 policy를 개선함. 실로봇 과제 3개의 평균 성공률이 57.93%로, 같은 world model로 처음부터 앞으로만 rollout하는 기존 방법 RISE(저자 재현)의 46.72%보다 높음.

**무슨 문제인가**

action-conditioned world model로 robot policy를 RL 학습하는 기존 방법은 world model을 실제 환경처럼 처음부터 앞으로만 굴리는 데 씀. 이 방식은 결과를 가른 소수의 결정 지점을 골라 다시 시험하지 못하고, 궤적마다 공통 앞부분을 다시 생성하느라 계산을 씀. 궤적 끝의 성공/실패만으로는 중간 action 중 무엇이 결과를 정했는지 알 수 없고, 이를 메우려고 value model을 따로 학습하면 추정 편향이 들어감. 또 policy가 좋아질수록 world model 학습 데이터에 드물던 상태로 가게 되어, policy가 world model의 예측 오차를 성공으로 잘못 배울 수 있음.

**어떻게 푸나**

Rollback은 world model의 temporal context를 action chunk 경계마다 저장하고, 저장된 지점에서 다른 action chunk로 이어 생성하는 experience backtracking을 씀. 입력은 실제 로봇의 성공·실패 궤적이며, π0.5 policy가 그 궤적의 중간 결정 지점에서 대안 action chunk를 샘플링하고 world model(GE-Sim 2.0)이 세 카메라 영상과 관절 상태를 함께 예측함. MCTS(Monte Carlo tree search)는 형제 action의 결과가 갈리는 지점에 생성 예산을 더 주고, 끝난 rollout은 과제별로 fine-tuning한 reward model이 성공/실패로 판정함. 같은 부모에서 나온 형제 action마다 하위 tree 성공률을 구하고, 가장 좋은 형제 대비 비율을 5개 bin으로 나눠 상대 품질 label을 만듦. policy는 이 label을 prompt 조건으로 받는 RECAP(advantage label 조건부 policy 학습) 방식으로 학습되므로 별도 value model이 없음. 동시에 실제 로봇이 최신 policy로 모은 궤적으로 world model을 LoRA SFT와 DMD(distribution matching distillation, 적은 step 생성기로 증류)로 계속 보정함. 저자는 이 보정을 test-time physics grounding이라 부름.

**결과**

- AGIBOT Genie-02 양팔 로봇의 과제 3개(Jenga 탑에서 블록 빼기, 공을 던져 양동이에 넣기, 사람과 돌 2개씩 겨루는 탁상 curling)에서 평가함. 평균 성공률이 Rollback 57.93%, 같은 GE-Sim 2.0으로 앞으로만 rollout하는 RISE 재현 46.72%임. 과제별 차이는 10.67, 11.11, 11.85퍼센트포인트이고, 모든 방법은 π0.5에서 시작해 로봇 1대로 약 8시간 학습함.
- 실제 로봇 RL인 RECAP의 평균 성공률은 44.22%, SFT는 40.30%임. RECAP이 SFT 대비 3.92퍼센트포인트, RISE 재현이 RECAP 대비 2.49퍼센트포인트를 더한 반면 Rollback은 RISE 재현 대비 11.21퍼센트포인트를 더함.
- Block Extraction ablation에서 성공률은 전체 Rollback 69.33%, 하위 tree 평균 대신 rollout 하나의 reward로 label을 매기면 59.33%, world model 보정을 끄면 64.67%임. 탑을 넘어뜨리지 않고 연속으로 뺀 블록 수는 2.60에서 1.90(보정 끔)으로 내려감.
- world model 보정을 끈 변형은 부록 기준 공 던지기 26.67%(Rollback 40.00%), curling 52.59%(Rollback 64.44%)임. 평가는 과제당 시작 위치 6개(curling 9개), 위치당 15회(블록 빼기 25회)이며 신뢰구간은 보고하지 않음.

**한계**

로봇 1대에서 과제마다 단일 과제 policy만 학습했고, 학습 seed 반복이나 신뢰구간이 없음. 탐색에 H200 GPU 40개(전체 48개)를 쓰며, 과제별 reward model과 긴 접촉 구간의 world model 정확도에 기댐. 사람 평균 성공률을 넘었다는 주장과 학습 곡선, world model 정확도 분석(6.4~6.7절)은 받은 텍스트에서 중간이 잘려 수치를 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- world model을 counterfactual 실험 장치로 쓰는 구체적 구현임. 실패한 실제 궤적의 결정 지점에서 분기해 어떤 action chunk가 실패를 만들었는지 가리는 구조라 failure diagnosis·recovery 연구에 그대로 가져올 수 있음.
- 형제 action 간 하위 tree 성공률 비교로 value model 없이 VLA에 chunk 단위 label을 주는 방식은, world model 기반 test-time search나 VLA RL fine-tuning의 비교 기준으로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 사람이 Jenga 탑을 다시 쌓아야 하는 실제 로봇 RL, world model 안에서 독립 rollout만 앞으로 굴리는 방식, 핵심 결정 지점으로 돌아가 분기한 tree의 결과 차이로 policy를 고치는 Rollback을 비교함. 아래 줄은 실험 과제 3개(블록 빼기, 공 던지기, 탁상 curling)의 실제 로봇 장면임.*

---

### 2. How Much Can Best-of-N Help a World Action Model? Measuring Selectable Headroom and Realizing It in Closed Loop (83점)

[arXiv](https://arxiv.org/abs/2610.37196) · [PDF](https://arxiv.org/pdf/2610.37196) · [alphaXiv](https://www.alphaxiv.org/abs/2610.37196) (요약 있음)

- **저자**: Haojia Gao, Yue Cao, Yumin Liu, Haohua Que, Mingkai Liu, Guanqiu Guo, Zhuo Zou, Bokui Chen 외 1명
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 80점
- **읽은 원문**: PDF 전문

> world action model이 후보 행동 여럿의 미래를 상상해 하나를 고르는 best-of-N에서, 후보마다 이후 실행을 여러 번 반복해 무작위성의 영향을 빼고 실제로 고를 수 있는 이득을 다시 잼. 이 측정을 바탕으로 실패가 예측될 때만 다른 행동으로 바꾸는 selector를 만들어 LIBERO-Plus 학습 과제의 폐루프 성공률을 76.9%에서 81.6%로 올림.

**무슨 문제인가**

WAM(world action model)은 action chunk, 그 chunk를 실행한 뒤 장면의 예측, value 추정을 한 번에 내는 모델임. 그래서 후보 chunk를 여러 개 뽑아 각 미래를 상상하고 가장 좋아 보이는 것을 실행하는 best-of-N 선택을 바로 쓸 수 있음. 선택으로 얻는 이득은 후보 중 최선이 실제로 얼마나 나은지로 제한되고, 저자들은 이 양을 selectable headroom이라 부름. 기존 측정법(Yuan et al.)은 같은 시뮬레이터 상태에서 후보마다 끝까지 한 번만 실행해 가장 좋은 결과를 고르므로, 후보의 품질과 뒤이은 policy 실행의 운을 구분하지 못함. 같은 무작위 결과로 고르고 채점하면 이득이 부풀려지는 optimizer's curse가 생김.

**어떻게 푸나**

저자들은 denoised counterfactual protocol이라는 측정 절차를 만듦. MuJoCo 상태와 난수 상태를 바이트 단위로 똑같이 되돌리는 snapshot에서 후보 chunk K개를 각각 실행하고, 그 뒤를 policy로 J번 이어 실행해(continuation) 성공·실패 표를 얻음. held-out oracle은 일부 continuation 결과로 후보를 고르고 고를 때 쓰지 않은 continuation에서 채점하므로, 실제 selector가 얻을 이득의 하한이 됨. 같은 결과로 고르고 채점하는 in-sample oracle은 상한이 됨. 후보는 policy가 낸 독립 샘플(native)과, policy chunk를 로봇 축 6방향으로 크기 κ만큼 옮긴 structured 후보 두 종류를 비교함. 측정 결과를 바탕으로 만든 fail-gated selector에서는 먼저 failure gate(logistic readout)가 WAM이 policy chunk를 상상할 때의 내부 표현을 읽어 실패 점수 q를 냄. q가 기준값 θ를 넘을 때만 축 6방향을 κ 두 값(0.1, 0.5)으로 옮긴 offset 12개의 미래를 상상하고, ranker(ridge readout)가 그중 하나를 골라 실행함. 두 readout 모두 value head가 아니라 branch 실행 결과로 학습함.

**결과**

- RoboCasa(가정 주방 조작 시뮬레이션 과제 모음) 과제 3개에서 기존 절차를 재현하면, native 후보 16개 중 최선의 실현 결과를 고를 때 성공률이 46.1%에서 58.3%로 오름. 같은 결정 시점에서 continuation 3개로 고르고 새 continuation에서 채점한 held-out oracle은 이 이득의 8.6%만 얻음. 후보 간 결과 차이의 98%는 continuation 난수가 바뀌면 새로 정해짐.
- LIBERO-Plus(LIBERO 조작 과제에 물체 배치·로봇 초기 자세 등의 교란을 넣은 벤치마크)를 포함한 두 벤치마크에서 비율을 잼. held-out oracle 이득이 in-sample oracle 이득에서 차지하는 비율은 native 후보에서 4개 WAM 모두 22% 이하임. structured 후보(κ=0.5)에서는 이 비율이 67~95%임. LIBERO-Plus의 Cosmos Policy에서 held-out oracle은 policy chunk보다 11.2퍼센트포인트 높음.
- Cosmos Policy가 상상한 미래의 표현에 linear probe를 붙이면 후보 순위와 약한 양의 상관을 보임. RoboCasa 11개 조건 평균 within-decision Spearman ρ는 상상한 미래 0.19, 실제 미래 0.15, value head 출력 0.01임.
- Cosmos Policy, LIBERO-Plus 폐루프에서 학습 과제의 별도 episode 성공률이 76.9%에서 81.6%로 오름(사전 등록 검정). 로봇 초기 자세 교란에서는 65.1%에서 75.8%로 오르고, 물체 배치 교란에서는 88.6% 대 87.4%로 이득이 없음. selector 학습에 쓰지 않은 과제에서는 62.6%에서 69.8%로 오름.

**한계**

모든 실험은 MuJoCo 기반 시뮬레이션 벤치마크 두 개에서만 했고, 실로봇에서는 반복 reset으로 측정을 근사할 수 있다고 저자가 주장만 함. selector는 Cosmos Policy 하나로만 만들었고, selector는 episode당 policy 호출 12회에 더해 WAM 상상 계산을 평균 17.5회 더 씀. policy가 이미 잘하는 물체 배치 교란에서는 성공률을 올리지 못함. 측정 도구와 데이터(HeadroomBench)는 공개 예정이라고만 하고 주소는 본문에 없음.

**누리랩 연구와의 연결**

- test-time optimization과 world model 기반 planning에서 best-of-N 이득을 보고할 때, 후보당 continuation 하나를 더 써서 held-out oracle을 함께 재는 평가 절차를 그대로 가져다 쓸 수 있음.
- 실패 예측 gate가 언제 개입할지를 정하고 그때만 대안 행동을 상상해 고르는 구조는 failure detection/recovery와 직접 이어짐. value head 출력이 아니라 WAM 내부 표현에 실패 정보가 있다는 결과는 VLA 실패 예측기를 설계할 때 비교 기준이 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. (a)는 snapshot에서 후보 K개를 J번씩 이어 실행한 성공·실패 표에서 열마다 최선을 고르는 O1(in-sample oracle, 주황)과 다른 열로 고르고 남긴 열로 채점하는 OL(held-out oracle, 파랑)을 비교함. (b)는 failure gate의 점수 q가 θ를 넘을 때만 offset 12개를 ranker로 골라 실행하는 selector 흐름을 보여 줌.*

---

### 3. Dexterous In-Hand Object Pose Reaching with Learned Safety Filters (82점)

[arXiv](https://arxiv.org/abs/2610.37652) · [PDF](https://arxiv.org/pdf/2610.37652) · [alphaXiv](https://www.alphaxiv.org/abs/2610.37652) (요약 있음) · [프로젝트 페이지](https://ian-chuang.github.io/dexsafe/)

- **저자**: Ian Chuang, Hiya Shah, Vamsi Chilamkur, Iman Soltani, Claire Tomlin
- **분야**: Dexterous Manipulation · robotics relevance 10/10 · 1차 스크리닝 84점
- **학회**: IEEE 학술지 계열 양식 (추정) · 근거: IEEE 2단 양식, 26쪽
- **읽은 원문**: PDF 전문

> LEAP hand가 손 안의 물체를 손목 방향과 상관없이 연속된 목표 위치·자세로 옮기는 policy를 사람 데이터 없이 시뮬레이션에서 학습해 실로봇으로 옮기고, 그 위에 따로 학습한 residual safety filter를 얹어 물체를 놓치는 횟수를 줄임. 실로봇 1,200개 목표에서 state policy의 drop이 16회에서 4회로 줄고, 목표 도달률은 95.2%에서 91.5%로 내려감.

**무슨 문제인가**

학습 기반 in-hand 조작은 대부분 손바닥이 위를 향한 한 가지 손목 방향에서 물체를 축 둘레로 돌리는 수준에 머묾. 물체를 원하는 위치까지 옮기려면 손바닥 받침 없이 손가락 끝으로만 쥐는 자세가 자주 필요하고, 이때 물체를 놓치기 쉬움. 그런데 기존 연구는 짧은 시행만 보고하고, 물체를 놓치지 않는 안전성은 reward shaping에 맡기거나 아예 재지 않음. in-hand 6D 자세 도달을 학습한 가장 가까운 선행연구 POISE도 실로봇에서 가장 긴 연속 목표가 7개이고, palm-down 방향은 시험하지 않았음.

**어떻게 푸나**

과제는 in-hand object pose reaching으로, 물체를 손 기준 목표 위치·자세로 옮긴 뒤 reset 없이 다음 목표로 이어 가는 것임. 목표와 초기 상태는 grasp 생성 도구 LightningGrasp로 생성한 grasp를 RRT 방식으로 넓힌 물체당 42만~45만 개 grasp 데이터셋에서 뽑음. 처음에는 손끝 마찰을 비현실적으로 높게 두고 성공률에 맞춰 실제 범위로 낮추는 adaptive friction curriculum으로 privileged teacher를 PPO로 학습함. teacher를 DAgger로 motion capture 물체 자세를 입력받는 state policy로 옮기고 PPO로 다시 미세조정한 뒤, 손목 depth 카메라만 쓰는 depth policy로 한 번 더 distillation함. 서보는 직접 측정한 데이터로 맞춘 DC 모터 모델(BAM)과 지연 보정으로 시뮬레이션에 넣어 zero-shot으로 실로봇에 옮김. 안전 쪽은 ResSafe(고정된 policy 위에 보정 행동을 더하도록 학습하는 residual safety filter)를 가져옴. filter는 물체가 손에서 0.3 m 안에 있는 동안 보정이 작을수록 큰 reward를 받음. 보정 가중치 w를 입력으로 넣어 한 네트워크로 배치 시점에 보수성을 조절하며, filter는 목표를 보지 않음.

**결과**

- 실로봇 평가는 물체 4개(칼, 전구, 고무 오리, 와인잔), 손목 방향 6개, filter 유무와 state·depth policy 조합으로 50개 연속 목표 run 96개, 총 4,800개 처음 보는 목표(13.3시간)임. state policy는 coarse 도달률(2 cm·0.4 rad 이내 도달 비율)이 filter 없이 95.2%, filter(w=0.5) 적용 시 91.5%이고, drop은 1,200개 목표 중 16회에서 4회로 줄어 75% 감소함.
- 같은 조건에서 filter는 첫 drop까지 평균 시간을 334초에서 465초로, 첫 drop 전 도달한 목표 수를 50개 중 31.8개에서 42.9개로 늘림. depth policy는 drop이 88회에서 46회로 줄었지만 와인잔만 보면 51회에서 40회임.
- 시뮬레이션 고무 오리 state policy(환경 1,024개 × 목표 50개)에서 ResSafe(w=0.5)는 coarse 도달률 91.3%, drop 비율 4.5%임. drop 비율이 비슷한 Hamilton-Jacobi 기반 학습 filter HCSF는 82.0%(drop 4.8%)이고, 위험 시 fallback 행동으로 바꾸는 LRSF는 79.3%(drop 8.2%)임.
- depth policy는 실로봇 coarse 도달률이 전구 95%, 오리 88%로 시뮬레이션과 비슷하지만 칼 54%, 와인잔 50%로 시뮬레이션의 90%, 84%보다 낮음. 저자는 실제 depth 영상에서 칼과 와인잔의 자세 추정 오차가 크게 나오는 경우가 많은 것을 원인 후보로 듦.

**한계**

policy와 filter 모두 물체마다 따로 학습하고, filter는 자기가 얹힌 task policy에 묶여 있음. 학습된 filter이므로 drop이 없다는 보장은 없고, HCSF(Hamilton-Jacobi 기반 filter)와의 비교는 시뮬레이션의 물체 하나·state policy 하나에서만 했음. 코드와 checkpoint는 공개 예정이라고만 적혀 있고 본문에 저장소 주소는 없음.

**누리랩 연구와의 연결**

- task policy를 고정한 채 실패(물체 놓침)를 막는 residual 보정만 따로 학습하고 w 하나로 성능과 안전을 조절하는 구조임. VLA 같은 고정된 generalist policy 위에 failure prevention 모듈을 얹는 연구에서 비교 대상으로 쓸 수 있음.
- 4,800개 목표에 걸쳐 도달률, drop 수, 첫 drop까지 시간을 함께 보고하는 평가 방식은 dexterous manipulation과 failure detection 연구의 실로봇 평가 설계에 참고가 됨.

*대표 그림: 실험 하드웨어 사진으로, 측정 결과가 아니라 장비 구성을 보여 주는 그림임. (a) motion capture 카메라로 둘러싼 공간 안의 UR5 팔과 LEAP hand, (b) 손과 손목에 단 stereo 카메라, (c) 작업 공간 카메라 시점, (d) 초록색 오리를 쥔 손을 본 손목 카메라 시점이 보임.*

*영상: [프로젝트 페이지 소개 영상으로, 물체별 policy가 여러 손목 방향에서 연속 목표 3개로 물체를 옮기고 도달하면 목표 윤곽선이 초록색으로 바뀌는 장면을 찍은 것임.](https://blog-media.assets.alphaxiv.org/videos/01a1a4fc-a86f-72ce-8a92-8c2330dc0537/81b9c982-d5a4-4b61-945b-df8b971d636b) (alphaXiv 요약에서 가져옴)*

---

### 4. TAPESTRY: A Single Backbone for Video Generation and Robot Control (82점)

[arXiv](https://arxiv.org/abs/2610.36823) · [PDF](https://arxiv.org/pdf/2610.36823) · [alphaXiv](https://www.alphaxiv.org/abs/2610.36823) (요약 있음) · [프로젝트 페이지](https://tapestry-wam.github.io)

- **저자**: Jeremy A. Collins, Seungjae Lee, Rachanon Wachakorn, Krishnan Srinivasan, Animesh Garg, Vitor Campagnolo Guizilini, Paarth Shah
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 80점
- **학회**: CoRL 2026 채택 · 근거: comments에 "Accepted to Conference on Robot Learning (CoRL) 2026"
- **읽은 원문**: PDF 전문

> pretrained video diffusion transformer에 robot action을 VAE latent patch 하나로 넣어, video를 만들지 않고 DDIM 1 step으로 action chunk를 내는 policy를 만듦. RTX 5090에서 chunk당 84 ms로 DreamZero보다 약 44배 빠르고, 실로봇 분포 밖 조건 15회 중 10회 성공함.

**무슨 문제인가**

video generation model은 대량의 영상에서 물체가 어떻게 움직이는지에 대한 prior를 배우므로, demonstration이 적은 robot policy의 출발점으로 쓰임. 기존 방법은 video를 먼저 생성하고 inverse dynamics model로 action을 뽑거나, backbone 중간 feature에 처음부터 학습한 action head를 붙임. 앞의 방식은 추론마다 video를 생성해야 해서 느리고, 뒤의 방식은 pretrained weight가 action을 직접 처리하지 않음. video와 action을 한 backbone에서 같이 denoise하는 DreamZero, Cosmos Policy도 추론 때 video token 전체를 다루거나 action chunk를 112번 복제해 넣으므로 chunk 하나에 수 초가 걸림.

**어떻게 푸나**

TAPESTRY(Tokenizing Actions as Video Patches in a Shared Transformer Policy)는 text-to-video DiT인 CogVideoX-2B 전체를 fine-tuning해 policy로 씀. 각 시점의 20차원 action을 linear projection으로 VAE latent patch 크기로 바꾸고, affine 없는 LayerNorm으로 VAE latent와 평균·분산을 맞춘 뒤 video와 같은 patchify convolution에 넣음. 그래서 action 한 시점이 token 하나가 되고, 새로 추가되는 parameter는 projection의 1,280개뿐임. 학습에는 세 objective를 섞음. video diffusion은 robot·사람·인터넷 video로 dynamics prior를 유지하고, joint diffusion은 robot demonstration의 video와 action을 같은 timestep으로 같이 denoise함. action-only diffusion은 현재 이미지와 언어만 조건으로 action만 denoise하며 추론 때와 같은 형태임. joint diffusion에서는 action token이 video token을 보지만 video token은 action token을 보지 못하게 attention mask를 둠. 추론 때는 현재 관측과 언어 지시를 받아 순수 noise에서 DDIM 1 step으로 16-step action chunk를 출력하고, video token과 VAE decoder는 쓰지 않음.

**결과**

- LIBERO(시뮬레이션 조작 benchmark)의 learning-from-video 설정에서 평가함. 이 설정은 LIBERO-90에만 action label을 주고 LIBERO-10·Object·Spatial·Goal은 video만 줌. 4개 suite 평균 성공률은 76%이고 가장 강한 baseline인 Cosmos Policy와 DreamZero는 둘 다 70%임(suite당 100 rollout). LIBERO-10에서는 55%로 Cosmos Policy의 70%보다 낮고, video pretraining 없이 같은 구조를 학습하면 평균 58%임.
- 20-DoF 양팔 YAM 로봇의 분포 밖 조건 3개(croissant를 오븐 안이 아니라 투명 오븐 문 위에 둔 뒤 집어 접시에 놓기, 처음 보는 그릇의 골프공 붓기, 처음 보는 Lego를 boomerang 위에 놓기)에서 조건당 5회 평가함. 전체 성공은 15회 중 10회이고 DreamZero는 4회임. 이 차이는 p=0.07로 통계적으로 유의하지 않음. Lego 조건은 5회 모두 성공했고 비교한 다른 방법은 모두 0회임.
- 같은 로봇의 학습 과제 3개(과제당 10회)에서는 30회 중 28회 성공함. 처음부터 학습한 Diffusion Policy는 15회, 대규모 video 공동 학습을 뺀 TAPESTRY는 20회임.
- RTX 5090 한 장에서 16-action chunk 하나를 84 ms, GPU memory 9 GB로 만듦. 5B 모델인 DreamZero는 같은 GPU에서 공개 코드로 약 20초, 저자가 최적화한 뒤 3.7초가 걸림.

**한계**

1 step 출력은 noise와 거의 무관한 조건부 평균 action chunk 하나이므로 정답 행동이 여러 갈래인 과제에서는 평균 쪽으로 치우칠 수 있고, 이를 확인한 실험은 같은 croissant 두 개를 둔 시험(10회 중 8회 성공) 하나뿐임. 저자는 여러 step denoising이 action chunk에 고주파 jitter를 더해 실행을 해친다고 측정해 1 step을 택함. 1 step이 성립하는 근거는 CogVideoX의 zero terminal SNR v-prediction schedule이며, rectified flow를 쓰는 Wan backbone에서는 성립하지 않았음. 실로봇 평가는 한 플랫폼에서 학습 과제 3개, 분포 밖 조건당 5회뿐이고 코드 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- video world model의 weight를 video 생성 없이 바로 policy로 쓰는 구성이라, world model 기반 VLA를 실시간 manipulation 제어에 넣을 때 비교 기준이 됨. 같은 weight가 joint mode로 video 예측도 하므로, 평소에는 action만 내고 필요할 때만 video를 예측해 failure detection에 쓰는 구성을 시험해 볼 수 있음.
- video로 pretrain된 backbone에서 여러 step denoising이 action에 고주파 jitter를 더한다는 측정은, 같은 종류의 backbone 위에서 test-time optimization이나 반복 sampling을 설계할 때 먼저 확인할 점임.

*대표 그림: 측정 결과가 아니라 방법 구조를 주로 그린 그림으로, video patch와 action patch가 같은 patch embed, pretrained video model, patch unembed를 거치는 흐름과 세 학습 objective를 보임. 오른쪽 아래 막대그래프만 측정값으로, action 출력 빈도를 Cosmos Policy 0.20 Hz, DreamZero 0.27 Hz, Fast-WAM 5.3 Hz, TAPESTRY 12.0 Hz로 비교함.*

---

### 5. Vision-Language-Action or World-Action? Just Action Models (79점)

[arXiv](https://arxiv.org/abs/2610.37219) · [PDF](https://arxiv.org/pdf/2610.37219) · [alphaXiv](https://www.alphaxiv.org/abs/2610.37219) (요약 있음) · [프로젝트 페이지](https://y0uroy.github.io/JAM)

- **저자**: Yonghao Yu, Lang Huang, Runyi Li, Toshihiko Yamasaki
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 82점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> world-action model의 이미지·영상 생성 loss를, 현재 관측 feature로 미래 관측의 고정 표현을 예측하게 하는 foresight loss로 바꿔도 성공률이 유지되거나 오름을 보임. 구조를 고정한 비교에서 LIBERO-Plus 성공률이 FastWAM 55.31%에서 64.54%로, ImageWAM 65.27%에서 79.95%로 오름.

**무슨 문제인가**

VLA는 vision-language model에서 출발해 action만 배우고, WAM(world-action model)은 이미지·영상 generator에서 출발해 미래 관측 생성도 함께 배움. 두 계열의 성공률 차이에는 backbone 초기화, 기록된 미래 관측에 거는 학습 목표, 추론 때 남기는 모듈이라는 세 선택이 섞여 있음. 그래서 성공률만 비교해서는 어느 선택이 차이를 만들었는지 가릴 수 없음. FastWAM과 ImageWAM은 추론 때 생성을 없앴지만 학습 때는 생성 loss를 그대로 쓰므로, 미래 관측으로 배우는 데 생성이 꼭 필요한지는 확인되지 않은 상태였음.

**어떻게 푸나**

JAM(Just Action Model)은 사전학습 visual backbone과 flow matching action expert로 이루어지고, action loss와 foresight loss로 학습함. 입력은 현재 관측, robot state, 언어 지시이고 출력은 action chunk임. 학습 때는 고정된 future anchor(기록된 미래 관측을 target feature로 바꾸는 frozen encoder)가 미래 관측을 encoding함. 작은 transformer prediction head가 backbone 중간 층(약 60% 깊이)의 현재 관측 token에서 이 target을 예측하고, 둘의 cosine distance를 foresight loss로 씀. gradient는 head와 backbone으로 흐르지만 미래 관측은 action 경로의 입력으로 들어가지 않음. 학습이 끝나면 anchor와 head를 버리므로 배포 구조는 baseline과 같고, target은 미리 계산해 cache할 수 있음. 생성을 하지 않으므로 backbone은 생성 모델(Wan2.2-5B, Ovis-U1), self-supervised encoder(DINOv2), VLM(Qwen3.5-2B) 중 무엇이든 쓸 수 있음.

**결과**

- FastWAM·ImageWAM의 구조, 데이터, optimizer, 학습 budget을 고정하고 생성 loss만 foresight loss로 바꿈. LIBERO-Plus(LIBERO 과제에 카메라·robot 초기 상태·조명·배치 등 7종 교란을 건 benchmark, 1,506개 과제 subset)에서 성공률이 55.31%에서 64.54%로, 65.27%에서 79.95%로 오름. 학습 3회 반복의 표준편차는 0.37과 0.43퍼센트포인트이고, 두 비교 모두 성공률 차이의 task bootstrap 95% 신뢰구간이 0을 포함하지 않음.
- 예측할 target의 시간 위치에 따라 성공률이 10퍼센트포인트 넘게 달라짐. Ovis-U1에서 현재 프레임 target은 LIBERO-Plus 69.65%, 16 step 뒤 프레임 target은 79.95%, 둘을 함께 쓰면 72.58%임. Wan backbone 자체 feature를 target으로 쓰면 objective 교체만으로는 55.31%에서 55.58%로 거의 같지만, target을 현재 위치에서 미래 위치로 옮기면 44.62%에서 55.58%로 오름.
- VLM backbone에도 같은 loss가 통함. Qwen3.5-2B에서 같은 구조·설정의 action-only 학습 대비 LIBERO-Plus 성공률이 77.03%에서 81.14%로 오름. DINOv2-L에서는 68.26%에서 70.39%로 오름.
- RoboTwin 2.0(양팔 조작 과제 50개, Clean·Randomized 설정 평균)에서는 FastWAM 91.2% 대 JAM 91.4%, FLUX.2 backbone의 ImageWAM 92.9% 대 JAM 93.1%로 거의 같음. target을 cache하면 sample당 update당 추정 online 학습 연산이 15.52에서 4.19 TFLOPs로 73.0% 줄어듦.

**한계**

모든 실험이 시뮬레이션(LIBERO, LIBERO-Plus, RoboTwin 2.0)이고 실로봇 결과는 없음. 가장 좋은 target(Wan은 VAE latent, Ovis-U1은 사전학습된 Yak image-editing backbone의 feature)과 offset은 같은 평가 benchmark 결과로 고른 것이며, 구조마다 달라 새 backbone에서는 다시 찾아야 함. backbone 간 비교는 구조와 action interface가 달라 사전학습 효과만 떼어 볼 수 없다고 저자도 밝힘.

**누리랩 연구와의 연결**

- world model을 생성기로 쓰지 않고 미래 표현 예측을 학습 때만 쓰는 보조 loss로 다룬 VLA 학습법임. 추론 비용을 늘리지 않으므로 우리 VLA fine-tuning에 바로 붙여 비교해 볼 수 있음.
- 학습 후 버리는 prediction head는 미래 표현을 예측하도록 학습되어 있음. 이 head를 남겨 예측과 실제 관측 표현의 차이를 failure detection 신호로 쓰는 확장은 저자가 다루지 않았으므로 시험해 볼 만함.

*대표 그림: 측정 결과가 아니라 세 계열의 학습 구조를 한 장에 비교해 그린 그림임. (a) VLA는 미래 관측을 쓰지 않고 action loss만 쓰며, (b) WAM은 visual generator가 미래 관측을 만드는 생성 loss를 더함. (c) JAM은 학습 때만 쓰는 future anchor와 prediction head로 foresight loss를 줌.*

---

### 6. RoboAuto: Autonomous Robot Program Search through Multi-Level Physical Understanding (78점)

[arXiv](https://arxiv.org/abs/2610.36533) · [PDF](https://arxiv.org/pdf/2610.36533) · [alphaXiv](https://www.alphaxiv.org/abs/2610.36533) (요약 있음) · [프로젝트 페이지](https://roboauto-ai.github.io/)

- **저자**: Buzhao Liu, Jianing Ye, Xiu Yuan, Yangtong Feng, Chengsong Huang, Tyler Dinh, Yevgeniy Vorobeychik, Ning Zhang 외 1명
- **분야**: Manipulation · robotics relevance 10/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> LLM coding agent가 로봇 프로그램을 고쳐 가며 찾을 때, 물체별 물리 지식을 꺼내 현재 장면에서 값을 재고 단계마다 상태 변화를 확인하게 함. 여러 단계 조작 과제인 LIBERO-PRO Long의 평균 성공률이 가장 강한 coding agent baseline ASPIRE의 30.8%에서 73.4%로 오름.

**무슨 문제인가**

Code-as-Policy는 로봇 행동을 perception·control primitive를 조합한 프로그램으로 쓰게 하고, CaP-Agent0·ASPIRE 같은 agent는 프로그램을 실행해 보고 그 결과로 다시 고침. 이런 방법은 실행 결과만 보고 고치므로 실패 원인이 잡는 방식인지, 기하 값인지, 앞 단계 미완료인지를 가리지 못함. 저자들의 baseline 실행에서는 책을 위에서 잡는 시도를 되풀이하거나, 다른 머그의 잡는 높이를 그대로 써서 허공을 잡거나, 버너가 안 켜졌는데 팬을 올리는 실패가 나옴. 그래서 물체를 어떻게 다룰지, 장면 기하가 행동을 어떻게 제한하는지, 왜 실패했는지를 아는 물리 이해가 프로그램 탐색에 필요하다고 봄.

**어떻게 푸나**

RoboAuto는 세 부분으로 프로그램을 찾음. 첫째, 계층형 knowledge base는 물체 종류별로 affordance(그 물체를 다루기 알맞은 방식), 공간 관계, 행동의 효과와 전제 조건을 적은 항목과, 검증된 프로그램을 모은 skill library를 따로 둠. 물리 지식 항목은 LIBERO-90(시뮬레이션 조작 과제 90개 모음) 시연 영상에서 만들고, 수치는 적지 않고 장면마다 재야 할 양(open quantity)과 재는 법만 적음. 둘째, scene grounding은 지시문과 현재 관측을 받아 관련 물체와 역할을 고르고, Molmo2·SAM 3·depth 카메라로 잡는 위치, 크기, 방향 같은 값을 잼. 필요하면 팔을 움직여 더 나은 시점을 얻음. 셋째, 과제를 물체 상태 변화 단위의 단계로 나누고, 단계마다 프로그램과 함께 새 관측으로 결과를 판정하는 verifier 코드를 써서 통과해야 다음 단계로 넘어감. 실패 원인이 불확실하면 경쟁 가설을 세우고 과제 전체가 아닌 짧은 실험 코드를 따로 돌려 가설을 가리며, 그 결과로 지식 항목을 고치고 검증된 프로그램은 새 skill로 저장함.

**결과**

- LIBERO-PRO Long(위치·과제 교란을 넣은 LIBERO 장기 과제 10개 설정)의 평균 성공률이 73.4%로, ASPIRE의 30.8%보다 42.6퍼센트포인트 높음. 프로그램 탐색과 최종 평가는 서로 다른 장면에서 함.
- 5개 과제 누적 ablation에서 프로그램을 통째로 고치는 기본 루프는 5.2%임. 단계별 verifier와 가설 실험으로 탐색하는 Search and Exploration을 더하면 19.2%, knowledge base를 더하면 38.4%, scene grounding까지 더한 전체는 91.2%로 오름.
- LIBERO에서 만든 knowledge base를 양팔 조작 과제를 담은 다른 simulator benchmark인 RoboTwin 2.0의 과제 4개에 옮김. 평균 성공률이 knowledge base 없이 24.5%, 있을 때 91.5%임.
- 실제 WidowX AI 팔의 장기 과제 3개(공 분류, 그릇 쌓기, 칠판 지우기)를 과제당 20회 평가함. 단계 완료 점수가 RoboAuto 100%, 100%, 95.83%이고 ASPIRE는 30%, 3.75%, 0%, π0.5는 모두 0%임.

**한계**

프로그램 탐색이 자율로 돌아가는 것은 시뮬레이션뿐이고, 실로봇에서는 사람이 매 rollout마다 장면을 되돌리고 성공 여부를 판정함. ablation은 5개 과제의 누적 추가 방식이라 각 부분의 효과를 따로 떼어 보지 않았고 분산도 제시되지 않음. 실로봇 점수는 전체 과제 성공이 아니라 단계 완료 비율이며, 과제 3개뿐이고 코드 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- 단계별 verifier, 실패한 실행 영상을 다시 보고 verifier 판정을 바로잡는 독립 auditor, 실패 가설을 구별하는 실험 코드는 failure detection·diagnosis·recovery를 프로그램 탐색 안에서 구현한 사례임. 실패 원인을 가설로 세우고 개입 실험으로 확인하는 절차는 counterfactual reasoning 연구의 비교 대상이 됨.
- 수치 없이 재야 할 양만 적은 object-centric 지식 항목은 robot memory와 test-time optimization 설계에서 VLA 학습 없이 일반화하는 방식으로 참고할 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 왼쪽은 affordance·공간 관계·효과 항목과 executable skill로 된 knowledge base, 가운데는 Molmo2·SAM 3·depth로 머그 테두리 반지름 4.3 cm 같은 값을 재는 scene grounding임. 오른쪽은 4단계 검증과, 도달 한계와 충돌 중 어느 쪽이 실패 원인인지 가리는 실험을 보여 줌.*

*영상: [저자 프로젝트 페이지의 접시를 스토브에 올리는 과제 최종 rollout 영상으로, 잡는 방식을 고친 뒤 grasp 단계 통과와 접시 위치를 보고하는 장면임.](https://blog-media.assets.alphaxiv.org/videos/01a18059-3958-79de-b85a-0d290ba3ebe0/9e91fa5c-032b-4987-9e90-671587127a6e) (alphaXiv 요약에서 가져옴)*

---

### 7. CARD: Contact-Anchored Retargeting for Dexterous Manipulation (78점)

[arXiv](https://arxiv.org/abs/2610.36539) · [PDF](https://arxiv.org/pdf/2610.36539) · [alphaXiv](https://www.alphaxiv.org/abs/2610.36539) (요약 있음) · [프로젝트 페이지](https://card-retargeting.github.io/)

- **저자**: Cunxi Dai, Botao He, Francois R Hogan, Wei Pan, Rao Fu, Wen-Han Hsieh, Ruoshi Liu, Jitendra Malik 외 2명
- **분야**: Manipulation · robotics relevance 9/10 · 1차 스크리닝 76점
- **읽은 원문**: PDF 전문

> 사람 시연을 로봇 손으로 옮길 때 관절 자세 대신 손가락 부위별 접촉 위치, 미는 방향, 힘을 맞추는 retargeting 방법을 제안함. 객체 모델과 simulator 없이 시연 접촉을 43~78% 프레임에서 재현하며, kinematic retargeting은 10% 미만에 그침.

**무슨 문제인가**

사람 손 시연을 로봇 손으로 옮기는 기존 retargeting은 손끝 위치나 관절 각도를 맞추는 kinematic 문제로 다룸. 손 모양이 몇 mm만 달라도 로봇 손가락이 물체 위에 떠 있거나, 미끄러지거나, 물체를 잘못된 방향으로 누름. 접촉을 보존하려는 최근 방법들은 물체 mesh, 물체 자세 추정, 또는 과제마다 physics simulator를 요구함. 그래서 영상이나 장갑으로 모은 사람 시연을 접촉이 많은 조작 과제에 그대로 쓰기 어려움.

**어떻게 푸나**

CARD(Contact-Anchored Retargeting)는 먼저 영상, 촉각 장갑, motion capture 시연을 공통 표현으로 바꿈. 이 표현은 MANO(사람 손 parametric mesh 모델) 손 mesh 시퀀스와, 손을 16개 부위로 나눈 뒤 프레임마다 부위당 최대 1개 두는 접촉 목표로 이루어짐. 접촉 목표는 압력 중심 위치, 물체 안쪽으로 미는 단위 방향, 힘 크기의 세 값임. 단안 영상에는 접촉 정보가 없으므로 영상 기반 접촉 추정 모델 Vid-HACO가 MANO 정점 778개의 접촉 확률을 예측하고, 힘은 grasp 균형 조건으로 합성함. 이어서 사람 관절 각도를 로봇 골격에 바로 옮긴 자세를 초기값으로 둠. 그 뒤 로봇 손가락 패드를 접촉 목표 위치에 두고 패드 법선을 미는 방향에 맞추는 비용을 프레임마다 CEM(sampling 기반 최적화)으로 최소화함. 출력은 로봇 관절 궤적과 손가락별 목표 힘임. 실기에서는 tactile tracking controller가 손끝 힘 오차를 적분해 손가락을 더 오므리고 feedforward torque로 목표 힘을 가함.

**결과**

- 22-DoF SHARPA Wave 손으로 옮겼을 때 시연 접촉을 재현한 프레임 비율(접촉 목표가 로봇 패드 2 mm 안에 있는 비율)이 단안 영상 20개 clip에서 61.4%이고, 촉각 장갑·motion capture 시연에서는 78%임. 같은 조건에서 kinematic 방법 DexPilot은 9.7%, AnyTeleop 두 변형은 8.3%와 7.6%임.
- GRAB(사람 손-물체 grasp 동작 공개 데이터셋, 100개 clip)에서 CARD의 접촉 재현 비율은 43.1%임. 물체 mesh를 입력으로 받는 접촉 보존 방법 ReGrind는 22.5%이고, 물체 관통 깊이 중앙값도 CARD 7.96 mm 대 ReGrind 9.80 mm임.
- 실제 SHARPA Wave에서 같은 CARD 궤적을 open-loop로 재생함(망치 들기, 컵 들기, 머스터드 짜기 과제당 10회). tactile tracker를 켜면 30회 중 25회 성공하고, 위치 제어만 쓰면 4회 성공함.
- simulation 기반 retargeting SPIDER에 CARD의 접촉 목표와 비용을 넣은 CARD-physics는 GRAB 50개 clip의 엄격 과제 성공률을 12%에서 32%로 올림. motion capture 48개 시연에서는 40%에서 52%로 오름.

**한계**

주 지표인 접촉 재현 비율은 기하적 접촉 일치도이고 과제 성공을 직접 재지 않음. 실기 성공률은 SHARPA Wave 한 손의 과제 3개, 과제당 10회뿐이며 Wuji Hand 2와 Unitree Dex3-1은 성공 횟수 없이 재생 사진만 제시함. 영상 시연의 힘은 측정값이 아니라 합성값이고, open-loop 재생이라 물체가 크게 밀리면 복구하지 못하며 policy 학습은 보이지 않음.

**누리랩 연구와의 연결**

- 사람 영상과 촉각 장갑 시연을 관절 궤적과 손가락별 목표 힘이 함께 붙은 로봇 데이터로 바꾸는 도구임. dexterous manipulation용 imitation learning이나 force를 출력하는 VLA의 학습 데이터 생성에 바로 쓸 수 있음.
- 위치 제어만으로는 같은 궤적이 미끄러짐으로 실패한다는 실기 비교는, 목표 힘과 측정 힘의 차이를 failure detection 신호로 쓰는 연구의 출발점이 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 촉각 장갑의 24×31 taxel 압력이 MANO 손 위의 접촉 지도와 엄지 끝마디 접촉 목표로 바뀌고, 기하 초기화와 friction cone 정렬을 거쳐 SHARPA 손 자세가 됨. 이 자세의 관절 목표와 힘 목표를 tactile tracker가 받아 Rubik's Cube 조작을 재생하는 흐름을 보여 줌.*

---

### 8. RynnWorld-Latent: A Cross-Embodiment World Model Conditioned on Universal Latent Actions (76점)

[arXiv](https://arxiv.org/abs/2610.36791) · [PDF](https://arxiv.org/pdf/2610.36791) · [alphaXiv](https://www.alphaxiv.org/abs/2610.36791) (요약 있음) · [프로젝트 페이지](https://alibaba-damo-academy.github.io/RynnWorld-Latent.github.io) · [코드](https://github.com/alibaba-damo-academy/RynnWorld-Latent)

- **저자**: Haoyu Zhao, Yinzhou Tang, Zixuan Wang, Minghao Zhu, Dongchi Huang, Xingyue Zhao, Qin Zhao, Kehan Li 외 6명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 78점
- **학회**: Meta 자체 양식 · 근거: 글꼴 OptimisticDisp, 학회 양식 아님
- **읽은 원문**: PDF 전문

> 로봇마다 다른 action 공간 대신 영상에서 뽑은 latent action을 조건으로 써서, 사람·로봇·시뮬레이션 영상 23개 데이터셋을 한 video world model에 함께 학습시킴. 이 모델로 만든 합성 데이터로 mid-training한 π0.5는 실제 Astribot-S1의 접시 회수 과제 성공률을 45.71%에서 68.57%로 올림.

**무슨 문제인가**

action으로 조건을 거는 video world model은 로봇마다 관절 수, 좌표계, 제어 주기가 달라 여러 로봇 데이터를 한 모델에 모으기 어려움. 사람 손 영상은 상호작용 장면이 많지만 로봇 제어 label이 없음. 언어 지시로 조건을 걸면 과제 목표만 정해지고, 그리퍼가 물체를 잡는 시점 같은 프레임 단위 동작은 정해지지 않음. 그래서 영상의 출처와 상관없이 쓸 수 있는 공통 action 표현이 필요함.

**어떻게 푸나**

RynnWorld-Latent는 첫 프레임과 연속 latent action 열을 받아 이후 영상 latent를 만드는 text-free video world model임. latent action은 같은 저자들의 고정된 encoder RynnLAM이 4프레임 간격의 두 프레임 사이 변화를 608차원 벡터(motion 512, 전역 action 64, camera 32)로 요약한 것임. 이 간격이 video VAE의 시간 압축률 4와 같아서, latent action 하나가 미래 영상 latent 프레임 하나에 정확히 대응함. backbone은 Cosmos3-Edge(사전학습된 video diffusion transformer)이고, action token을 joint self-attention에 넣는 전역 경로와 해당 프레임의 vision token만 조절하는 지역 경로를 함께 씀. 지역 경로는 0으로 초기화해 학습 시작 시점에는 영상 token을 바꾸지 않음. 사전학습 뒤에는 목표 로봇 demonstration으로 post-training하면서 실제 로봇 action을 token으로 바꾸는 encoder를 따로 붙임. 이 모델로 두 방식의 데이터를 만듦. digital teleoperation은 조작자 입력을 로봇 action으로 바꿔 영상을 생성하고, action과 생성 영상을 함께 기록함. latent-action synthesis는 사람 영상의 첫 프레임을 로봇 장면으로 편집하고 원래 latent action으로 rollout을 만듦. 여기에 retargeting과 IK(inverse kinematics)로 얻은 pseudo action을 붙임.

**결과**

- DreamDojo가 만든 영상 예측 평가셋 3종(사람 영상 사전학습이 로봇 학습 데이터에 없던 물체 상호작용으로 옮겨지는지 봄) 중 EgoDex Eval에서 LPIPS가 기존 world model DreamDojo-14B의 0.21에서 0.19로 내림. PSNR은 20.53에서 20.89로 오름. baseline 수치는 문헌 값이라 backbone·데이터 차이는 분리되지 않음.
- 자체 Marvin-WUJI(양팔 dexterous hand 로봇) 평가에서 LPIPS는 전체 모델 0.12, frame-aligned 지역 경로 제거 시 0.18, latent action 대신 text 조건 시 0.30임. Astribot-S1(바퀴 달린 양팔 그리퍼 로봇)에서는 각각 0.34, 0.41, 0.55임. 둘 다 목표 로봇 post-training 뒤 학습에 쓰지 않은 episode로 잰 값임.
- 실제 로봇 4개 과제에서 π0.5를 RynnWorld-Latent로 만든 합성 데이터셋(RynnWorld-Latent-80M)으로 mid-training한 뒤 실제 데이터로 학습함. 성공률이 실제 데이터만 쓴 경우보다 접시 닦기 77.14%에서 97.14%로, 스테이크 서빙 40.00%에서 60.00%로, 접시 회수 45.71%에서 68.57%로 오름. 과제마다 35회 시도로 잼.
- 실제 데이터에 digital teleoperation 데이터를 더한 π0.5는 접시 닦기 성공률이 91.43%로 실제 데이터만 쓴 77.14%보다 높음. digital teleoperation 데이터만 쓰면 4개 과제 모두 실제 데이터만 쓴 경우보다 낮음(접시 놓기 57.14% 대 82.86%).

**한계**

모든 실로봇 수치는 해당 로봇 데이터로 post-training한 뒤의 결과이며, 평가셋도 학습에 들어간 과제의 다른 episode임. 영상 예측 지표는 화면 유사도라서 접촉의 물리적 정확도나 실행 가능한 action 추종은 재지 않음. 합성 mid-training 비교는 데이터 양과 학습 계산량이 함께 늘어난 비교라 latent action 자체의 효과와 분리되지 않음. 초록에 적힌 LIBERO·LIBERO-Plus 성공률 수치는 받은 원문 텍스트의 생략 구간에 있어 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- world model을 policy 학습용 데이터 생성기로 쓰고, 사람 영상의 첫 프레임만 로봇 장면으로 바꿔 동작을 옮기는 방식은 VLA 학습 데이터 확장 연구에서 비교 대상으로 쓸 수 있음.
- 같은 첫 프레임에 다른 latent action을 넣어 다른 미래를 만드는 구조라서, counterfactual rollout이나 world model 기반 failure detection 실험의 backbone 후보가 됨. 다만 action 추종은 정성 예시로만 보였음.

*대표 그림: 사전학습 데이터 구성을 요약한 그림이며 측정 결과나 방법 구조가 아님. 사람 영상, 실제 로봇, 시뮬레이션 예시 장면과 총 6190시간·23개 데이터셋·257만 episode 표기, 물체와 동작 단어 구름, 데이터셋별 시간을 log 축 막대로 나타낸 그래프가 보임.*

---

### 9. Adapting Video Models for Robot Control via Motion-guided Asymmetric Prediction (74점)

[arXiv](https://arxiv.org/abs/2610.36624) · [PDF](https://arxiv.org/pdf/2610.36624) · [alphaXiv](https://www.alphaxiv.org/abs/2610.36624) (요약 있음) · [프로젝트 페이지](https://ismty0805.github.io/mogap/)

- **저자**: Taeyoung Kim, Junyoung Sung, Heeseung Kwon, Minseop Kim, Jinwoo Shin
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> video model 기반 robot policy를 학습할 때 움직이는 영역에 noise를 더 세게 걸어 그 영역을 맞히게 하는 보조 예측 과제를 더함. GR-1 Tabletop 24개 과제 평균 성공률이 Cosmos3-Nano 기반 WAM에서 52.3%였던 것이 62.3%로 오름.

**무슨 문제인가**

WAM(World Action Model)은 사전학습된 video diffusion model 위에서 미래 영상과 action chunk를 함께 예측하는 robot policy임. 미래 영상 예측 loss는 video 사전학습에서 물려받은 형태라 화면의 모든 영역을 같은 비중으로 감독함. 탁자 무늬 같은 정적 배경은 시각적으로 복잡해도 제어와 관련이 적고, 손과 물체의 움직임은 작은 영역에서 일어남. 기존 보완책은 DINOv2, VGGT 같은 외부 teacher나 depth·3D 같은 추가 modality에 기대는 방식이었음.

**어떻게 푸나**

MoGAP(Motion-Guided Asymmetric Prediction)은 움직이는 영역을 예측 대상으로, 정적 영역을 맥락으로 나누는 보조 예측 과제임. 저자는 먼저 latent 시간 차이가 큰 위치에 loss 가중치만 더 줘도 두 WAM의 GR-1 Tabletop 성공률이 오르는 것을 확인함(Fast-WAM 38.8%에서 41.8%, Cosmos3 52.3%에서 57.7%). MoGAP은 연속한 video latent의 차이로 위치별 motion score를 구하고, 시간 slice마다 공간 평균보다 큰 위치를 동적 영역으로 정함. 동적 영역에는 기본 timestep보다 큰 noise를, 정적 영역에는 기본 noise를 주고, 덜 가려진 배경을 맥락으로 써서 많이 가려진 움직임 영역을 복원하게 함. 이 입력은 같은 backbone 안의 보조 경로로 처리하고, attention mask로 원래 WAM 경로가 보조 token을 보지 못하게 함. 추가 파라미터는 없고 inference 때는 보조 token을 빼므로 추론 절차는 그대로임.

**결과**

- RoboCasa GR-1 Tabletop(GR-1 humanoid 손으로 하는 탁상 조작 과제 24개, 과제당 50회 평가)에서 평균 성공률이 Cosmos3-Nano 52.3%에서 MoGAP 62.3%로 10.0퍼센트포인트 오름. 표에 있는 가장 높은 VLA인 RLDX-1의 58.7%보다도 높음. Fast-WAM(Wan2.2-5B)에서도 38.8%에서 47.5%로 오름.
- 같은 Cosmos3-Nano에 외부 teacher로 표현을 정렬하는 방법들을 붙인 비교에서 가장 높은 것은 V-JEPA2.1-L을 쓴 VideoREPA의 59.2%이고 MoGAP은 teacher 없이 62.3%임.
- 구성 요소 제거 실험에서 noise 비대칭을 없애면 55.3%, 방향을 뒤집어 정적 영역에 noise를 더 주면 55.2%, 보조 경로 없이 주 loss를 대체하면 54.4%로 내림. 학습 시간을 맞추려 Cosmos3를 22K step 학습한 경우도 55.8%로 MoGAP(16K step) 62.3%보다 낮음.
- 실제 OpenArm humanoid(7-DoF 팔 2개, 5손가락 손)에서 실행 중 사람이 물체를 옮기는 과제의 성공률이 그림 6 기준으로 set I의 경우 45.8%에서 87.5%로 오름. 더 멀리 옮기는 set II의 수치는 본문에서 확인 불가임. 학습 데이터에는 물체를 옮기는 demonstration이 없었고 과제당 24회 평가임.

**한계**

보조 token 때문에 학습 시간이 1.26배 늘어 H200 4장 기준 14.7시간이 18.5시간이 됨. motion score가 latent 시간 차이에 기대므로 카메라가 움직이면 신호가 흐려지며, RoboCasa-Kitchen(단일 팔 로봇의 주방 조작 과제 24개)에서는 wrist camera token을 전부 높은 noise 쪽에 넣는 수작업 규칙으로 처리함. attention 비율 분석은 정책이 움직임 영역을 더 본다는 상관만 보이고, 성능 향상의 원인임을 따로 검증하지는 않음.

**누리랩 연구와의 연결**

- world model을 policy 학습용 보조 감독으로 쓸 때 어떤 영역을 예측시키는지가 성능을 바꾼다는 결과임. VLA나 WAM 학습에서 object-centric 또는 manipulation 영역 위주의 감독을 설계할 때 바로 비교할 수 있는 baseline임.
- 실행 중 물체 이동에 대한 반응이 좋아진 결과는 failure recovery 연구에서 학습 목표만 바꿔 외란 대응을 개선하는 방향의 근거로 쓸 수 있음.

*대표 그림: 왼쪽 (a)는 탁상 배경과 손·물체가 있는 영역을 나눠, 기존 WAM의 균일 감독과 움직임 영역을 강조하는 MoGAP의 비대칭 감독을 비교한 방법 구조 그림임. 오른쪽 (b)는 GR-1 Tabletop 성공률 막대그래프로 Fast-WAM은 38.8에서 47.5, Cosmos3-Nano는 52.3에서 62.3으로 오른 값을 보여 줌.*

---

### 10. World Dreamer v5-lite: A Multi-Robot World Action Model with One Dreamer (72점)

[arXiv](https://arxiv.org/abs/2610.37518) · [PDF](https://arxiv.org/pdf/2610.37518) · [alphaXiv](https://www.alphaxiv.org/abs/2610.37518) (요약 있음)

- **저자**: Guoning Wu, Zijian Cai, Yuhang Zhang, Ying Liu, Yongbin Zheng
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 74점
- **읽은 원문**: PDF 전문

> 여러 로봇의 카메라 영상을 작업 공간 좌표의 공유 world state 하나에 모으고, 로봇마다 action stream은 따로 두는 multi-robot world action model을 제안함. RoboFactory 3개 과제 평균 성공률이 74.0%로, 가장 강한 baseline인 π0.5의 50.3%보다 23.7퍼센트포인트 높음.

**무슨 문제인가**

VLA와 world action model은 대부분 로봇 한 대의 action만 예측함. 여러 로봇이 한 작업 공간에서 협업하면 카메라가 로봇마다 따로 움직이고, 다른 카메라의 image patch끼리는 같은 물리 위치를 가리키지 않음. 카메라 token을 이어 붙이기만 하면 view 사이의 공간 대응이 생기지 않고, 로봇별 policy를 따로 두면 동료 로봇이 본 장면을 쓰지 못함. 또 학습 때 모든 카메라가 다 보이면, 자기 카메라가 가려졌을 때 남의 view를 쓰도록 배울 이유가 없음.

**어떻게 푸나**

입력은 언어 지시, 보정된(calibrated) 카메라들의 현재·최근 RGB, 로봇별 proprioception이고, 출력은 로봇마다 30 step 길이의 action chunk임. Qwen3-VL 기반 VLM이 지시와 현재 이미지 뒤에 로봇마다 하나씩 붙인 학습 가능한 agent query를 함께 처리해, 로봇별 query와 장면 KV cache를 만듦. 동시에 사전학습된 video encoder의 patch feature를 카메라 내·외부 파라미터로 3D에 올리고, depth가 없으면 시선 ray 위 후보 점 8개로 나눠 XY·XZ·YZ 세 평면(16×16 격자)에 씀. 이 평면 묶음이 공유 world state ϕ이며, 현재 프레임에서 보인 위치만 gate로 갱신하므로 카메라 수가 늘어도 크기가 같음. Action Decoder는 층마다 query가 ϕ를 읽고, 각 로봇의 action stream이 VLM cache를 참조하고, 로봇 사이 상대 pose로 편향된 attention으로 query만 주고받음. 학습 때는 한 로봇의 카메라 전부나 일부 view를 VLM 입력과 video encoder 입력 양쪽에서 함께 가리되 모든 로봇의 action target은 남기는 masked-view cooperative training을 씀.

**결과**

- RoboFactory(ManiSkill 기반 다중 로봇 협업 조작 benchmark, 각 로봇이 자기 카메라만 받도록 저자가 설정을 바꿈)에서 2·3·4대 로봇 과제 3개 평균 성공률이 74.0%임. 가장 강한 baseline π0.5는 50.3%, 3D Gaussian 기반 다중 로봇 policy인 Global GauDP는 17.0%임. 과제당 장면 100개로 평가함.
- 로봇 수가 가장 많은 Take Photo(4대)에서 성공률이 50%로, π0.5의 26%보다 24퍼센트포인트 높음.
- 실로봇 과제 4개(LeKiwi 2대 과제 2개, LeKiwi 2대와 OpenArm 1대 과제 2개)의 평균 성공률이 78.8%임. π0.5는 65.0%, 추론 때 video 생성을 건너뛰는 world action model인 Fast-WAM은 63.5%이며 과제당 100회 시도로 잼.
- 단일 로봇 가정용 benchmark RoboCasa365(주방 장면 조작 과제 모음, 50개 과제 평가)에서 전체 성공률이 58.08%로, leaderboard 최고 비교 대상 PatchWAM의 47.6%보다 10.48퍼센트포인트 높음.

**한계**

공유 world state, masked-view 학습, query 교환을 하나씩 뺀 ablation이 없어서 어느 설계가 성능을 올렸는지 알 수 없음. 10,000시간이 넘는 자체 사전학습 데이터와 Qwen3-VL·video model backbone 효과도 baseline과 분리되지 않았고, RoboFactory는 저자가 카메라 설정을 바꾼 3개 과제뿐임. 모든 카메라의 보정 정보가 있어야 하며, 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- 이동하는 여러 카메라의 feature를 작업 공간 평면에 누적하고 보인 위치만 갱신하는 방식은, 가려진 영역을 기억하는 robot memory와 다중 시점 world model 표현 설계에 그대로 비교 대상이 됨.
- 일부 view를 가린 채 action을 학습시키는 masked-view 학습은 카메라 가림이나 센서 고장 상황의 failure recovery 실험 설정으로 가져다 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 로봇 4대의 카메라 이미지와 언어 지시가 VLM으로, 로봇별 시간 순 영상이 video encoder와 카메라 geometry를 거쳐 ϕ로 들어가고, Action Decoder가 로봇별 noisy action에서 flow velocity를 내는 흐름을 보여 줌.*

---

### 11. When, Where, and What to Correct: Human-Guided Adaptive Residual Correction for Robot Policies (72점)

[arXiv](https://arxiv.org/abs/2610.37547) · [PDF](https://arxiv.org/pdf/2610.37547) · [alphaXiv](https://www.alphaxiv.org/abs/2610.37547) (요약 있음)

- **저자**: Anukriti Singh, Maxime Caniot, Pratap Tokekar, Firas Abi-Farraj
- **분야**: RL · robotics relevance 10/10 · 1차 스크리닝 72점
- **학회**: CoRL 2026 채택 · 근거: 1쪽에 "10th Conference on Robot Learning (CoRL 2026)"
- **읽은 원문**: PDF 전문

> 고정된 imitation policy가 정밀한 마지막 구간에서만 실패할 때, 사람의 드문 교정으로 보정을 켤 시점과 탐색할 관절 방향을 정하고 실제 보정량은 task reward로 배움. 실로봇 정밀 조작 과제 3개의 평균 성공률이 33.3%에서 75.0%로 오름.

**무슨 문제인가**

ACT(Action Chunking with Transformers) 같은 imitation policy는 과제 대부분을 잘 수행해도 쟁반 정렬이나 좁은 홈에 마커 꽂기처럼 짧은 정밀 구간에서 실패함. policy 전체를 다시 학습하거나 demonstration을 더 모으는 것은 국소적인 실패를 전체 학습 문제로 다루는 셈임. 기존 residual RL은 base policy를 고정하고 추가 행동만 배우지만, 궤적 전체에서 보정이 켜져 잘 되던 구간을 망칠 수 있고 행동 공간 전체를 탐색해 실로봇 시행을 낭비함. 사람 교정을 쓰는 기존 방법은 교정 행동을 그대로 따라 배우는데, 그 순간에 그럴듯한 교정이 과제 성공으로 이어지는지는 반영하지 못함.

**어떻게 푸나**

ARC(Adaptive Residual Correction)는 고정된 base policy의 7관절 행동에 gate가 켜졌을 때만 residual을 더하는 plug-in module임. 먼저 사람이 자율 rollout 도중 SpaceMouse로 base 행동에 보정을 더하는 rollout을 과제당 약 8~10개 모음. WHEN 단계에서는 사람 교정이 시작되기 직전, 로봇이 혼자 움직이던 마지막 5개 timestep의 상태를 positive로 삼아 곧 교정이 필요할지를 예측하는 gate classifier를 학습하고, 교정 중인 상태는 학습에서 뺌. WHERE 단계에서는 사람 교정 residual의 2차 moment 행렬에서 주요 고유벡터 2~3개를 뽑아 저차원 교정 basis로 고정함. WHAT 단계에서는 이 basis 안의 계수를 출력하는 residual actor를 gate가 열린 구간에서만 자율 탐색하며 TD3로 task reward에 맞춰 학습함. 사람 교정 궤적은 replay buffer에 넣지 않고 gate와 basis를 만드는 데만 씀.

**결과**

- Miroki 휴머노이드 오른팔로 쟁반 쌓기, 마커 꽂기, 컵 쌓기를 과제당 12회 평가함. 세 과제 평균 성공률이 고정 ACT의 33.3%에서 ARC의 75.0%로 오름. 과제별로는 7/12에서 12/12, 3/12에서 7/12, 2/12에서 8/12임.
- 같은 교정 데이터로 7관절 사람 residual을 직접 회귀한 supervised baseline은 3/12, 5/12, 3/12에 그침. 세 과제를 합치면 11/36으로 base ACT의 12/36보다도 낮음.
- 교정 직전 상태로 학습한 gate는 별도로 모은 자율 rollout 10개 모두에서 켜졌지만, 교정 중 상태로 학습한 gate는 하나에서도 켜지지 않음. 자율 탐색 중 gate가 열린 시간은 마커 8.5%, 컵 21.3%임.
- 사람 교정은 7차원 관절 행동 공간에서 2~3개 방향에 몰려 있음. 쟁반 3차원, 마커와 컵 2차원 basis가 교정 크기 제곱합의 97.3%, 96.0%, 97.7%를 담음.

**한계**

실로봇 과제 3개, 방법당 과제별 12회 평가뿐이고, 95% Wilson 신뢰구간이 넓어 과제별 차이는 불확실함. 같은 basis 안에서 사람 교정을 회귀한 비교 policy는 residual 크기와 방향만 비교했고 task 성공률은 보고하지 않음. ResiP나 FlowDAgger 같은 기존 residual RL·교정 학습 방법과의 실험 비교는 없고, gate는 과제별·작업자별 교정 시점에 기댐.

**누리랩 연구와의 연결**

- gate는 사람이 곧 개입할 상태를 예측하는 classifier라서, failure detection을 recovery 동작과 직접 묶은 사례로 볼 수 있음. 저자도 이 gate를 VLM monitor로 바꾸는 방향을 제시함.
- VLA 같은 큰 policy를 고정한 채 language feedback이나 사람 교정으로 test-time 보정을 붙이는 연구에서, 교정을 학습 목표가 아니라 탐색 범위로 쓰는 설계를 비교 대상으로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 위쪽은 ACT가 혼자 실행해 국소 실패로 끝나는 경우이고, 아래쪽은 gate(WHEN), 사람 교정에서 얻은 basis(WHERE), reward로 학습한 residual actor(WHAT)가 고정된 ACT 행동에 보정을 더해 과제를 성공시키는 흐름을 보여 줌.*

*영상: [저자가 올린 실제 로봇의 쟁반 쌓기 과제에서 ARC가 동작하는 영상임.](https://blog-media.assets.alphaxiv.org/videos/01a18068-d31e-7daf-afb8-306a5395bbd7/230d62d3-db1c-4db0-b927-f0964c526002) (alphaXiv 요약에서 가져옴)*

---

### 12. Learning Quality-Controllable Robot Policies with Iterative Hindsight Relabeling (72점)

[arXiv](https://arxiv.org/abs/2610.37393) · [PDF](https://arxiv.org/pdf/2610.37393) · [alphaXiv](https://www.alphaxiv.org/abs/2610.37393) (요약 있음) · [프로젝트 페이지](https://sinnnj.github.io/qcp)

- **저자**: Sinjae Kang, Dong Kyu Shin, Jaehong Kim, Kamin Lee, Hyoeun Kim, Kaixin Wang, Li Zhao, Seonghyeon Ye 외 1명
- **분야**: IL · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> 속도·부드러움 같은 실행 품질을 라벨로 받아 inference 때 고를 수 있는 robot policy를 만들고, 자기 rollout을 실제 품질로 다시 라벨링해 되풀이 학습함. 실제 컨베이어 과제에서 분당 집은 캔 수를 BC의 8.2개에서 13.0개로 올림.

**무슨 문제인가**

behavior cloning(BC)은 성공한 demonstration을 모두 같은 정답으로 보므로 빠른 시연과 느린 시연, 부드러운 시연과 거친 시연을 평균 내어 따라 함. 그래서 컨베이어에서는 빠르게, 와인 잔 운반에서는 흔들림 없이처럼 배치 현장이 요구하는 실행 방식을 policy에 지정할 수 없음. 품질을 조건으로 받는 기존 policy도 고정된 demonstration으로만 학습하므로, 시연에 없던 수준의 속도나 부드러움은 낼 수 없음.

**어떻게 푸나**

QCP(Quality-Controllable Policy)는 궤적마다 속도·action jerk·관절 경로 길이 같은 품질을 규칙 기반 점수 함수로 계산함. 점수를 데이터셋 안에서 같은 개수씩 나눈 4개 구간(quantile bin)으로 바꿔 품질 라벨 0~3을 붙임. policy는 관측 이력과 품질 라벨을 입력으로 받아 action chunk를 출력하는 flow matching policy이고, VLA인 π0.5에는 라벨을 "quality level: 3" 같은 문장으로 프롬프트에 넣음. 반복 hindsight relabeling에서는 가장 높은 라벨로 rollout을 모으고, 성공한 것만 요청 라벨이 아닌 실제로 잰 점수로 다시 라벨링해 데이터셋에 더함. 이어서 원래 demonstration을 포함한 전체 궤적의 구간 경계를 새로 계산하고 policy를 처음부터 다시 학습함. 좋은 rollout이 쌓일수록 최고 라벨이 뜻하는 품질이 올라가고, 품질 측정이 규칙 기반이라 사람의 품질 주석은 필요 없음.

**결과**

- Robomimic(시뮬레이션 조작 benchmark) Square 과제의 속도 조건에서 5회 반복 후 QCP는 성공률 82.2%, 성공까지 평균 120.3 step임. 오프라인 RL로 스타일을 조건화하는 SCIQL은 68.7%, 206.5 step임. 다만 online RL baseline인 EXPO는 성공률 96.0%로 더 높고 162.5 step임(3 seed 평균).
- Square 과제 부드러움 조건에서, 재학습 없이 iteration 0 policy로 rollout 1,800개를 모으면 성공한 rollout 중 어느 것도 반복 학습 최종 policy의 부드러움 중앙값에 이르지 못함. 품질 향상이 샘플 수가 아니라 재라벨링 후 재학습에서 온다는 저자 주장의 근거임.
- 실제 Franka 로봇에서 3초마다 캔이 오는 컨베이어 과제의 분당 집은 캔 수가 BC 8.2개에서 QCP 2회 반복 후 13.0개로 오름. 상위 20% 궤적만 골라 학습한 BC는 6.3개로 일반 BC보다도 낮음(3 seed 평균, π0.5 fine-tuning).
- 쟁반에 와인 잔을 올려 옮기는 과제에서 성공률이 BC 16.0%에서 QCP 42.0%로 오르고, 평균 기울기는 0.0660 rad에서 0.0482 rad로 27.0% 줄어듦. 시연 수집 때 사람 원격조작 성공률은 13.1%임.

**한계**

품질이 규칙 기반 점수로 잴 수 있고 성공 여부를 자동으로 판정할 수 있어야 하며, 매 iteration마다 수백 개의 online rollout과 처음부터의 재학습이 필요함. 실로봇 검증은 과제 2개, 2회 반복뿐임. 실로봇 rollout의 성공 판정 방식과 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- 성공/실패만 보던 VLA 학습에 실행 품질을 프롬프트 라벨로 넣어 inference 때 고르는 방식이라, π0.5 같은 VLA를 배치 조건에 맞춰 조절하는 연구에 바로 쓸 수 있는 baseline임.
- 자기 rollout을 실제 결과로 다시 라벨링해 데이터를 키우는 루프는, failure detection으로 판정한 결과를 라벨로 붙여 policy를 개선하는 self-improvement 실험의 출발점이 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 왼쪽은 같은 관측에서 품질 토큰(q_low, q_high)만 바꿔 거친 동작과 부드러운 동작을 내는 QCP, 오른쪽은 rollout 수집 → 품질 점수 → 성공 궤적 추가 → 구간 재계산으로 도는 반복 루프이고, 아래는 컨베이어와 와인 운반 활용 예시를 그린 삽화임.*

---

### 13. Which Hand Was Late? Diagnosis for Robot Failure Recovery in Bimanual Tool Use (72점)

[arXiv](https://arxiv.org/abs/2610.37533) · [PDF](https://arxiv.org/pdf/2610.37533) · [alphaXiv](https://www.alphaxiv.org/abs/2610.37533) (요약 있음)

- **저자**: Baptiste Bonin, Caro Strickland, Audrey Durand
- **분야**: Failure Detection · robotics relevance 9/10 · 1차 스크리닝 70점
- **학회**: CoRL 양식 (추정) · 근거: 1단 구성, 초록 아래 'Keywords:' 줄
- **읽은 원문**: PDF 전문

> 양팔 도구 사용 실패에서 어느 센서가 어떤 실패 원인을 담는지 채널별로 측정함. 원인을 구별할 수 없을 때 두 교정을 차례로 거는 복구 정책이 문이 열리지 않은 시도 386건 중 297건을 고쳐, 참 원인을 아는 oracle과 같은 수를 고침.

**무슨 문제인가**

AHA, RoboFAC 같은 VLM 기반 실패 진단기는 팔 하나가 물체 하나를 다루고 원인이 화면에 보이는 실패로 학습·평가됨. 양팔 도구 사용에서는 두 손이 각각 맞는 동작을 했어도 시점이 어긋나면 실패하므로, 원인이 한 팔이 아니라 두 팔 사이의 관계에 있음. 한 시도가 늦었고 힘도 모자랐던 것처럼 원인이 둘인 실패도 생기며, 원인을 잘못 짚으면 복구 동작도 틀림. 진단기가 무엇을 관측해야 늦은 손을 가릴 수 있는지, VLM이 그 정보를 답으로 내놓는지는 측정된 적이 없음.

**어떻게 푸나**

저자는 새 진단기를 만들지 않고, 진단기가 무엇을 관측해야 하는지를 재는 시험대를 만듦. ManiSkill3 시뮬레이션에서 Franka Panda 두 대가 문을 마주함: 한 팔은 사각 key-tool을 잠금 소켓에 끼워 돌리고, 다른 팔은 문을 밂. key는 놓으면 되돌아가므로, key가 돌아간 동안 미는 힘이 숨은 기준값 τ(시도마다 뽑고 관측에 없음)를 넘어야 문이 열림. scripted controller가 시도마다 결함 하나(얕은 삽입, 축 어긋남, 한 팔 지연 등)를 넣고, 각 실패의 원인은 사람이 아니라 기록된 메커니즘 궤적에서 판정함. 실패는 wrong(동작 미전달, 공구가 쥔 채 소켓에서 빠지는 cam-out 포함), timing(두 손 시점 어긋남), force(겹쳤지만 힘 부족), 두 원인 동시로 나뉨. 같은 L2 logistic regression probe를 센서 채널 하나씩, 그리고 Qwen3-VL 8B의 내부 상태와 답 각각에 적용해 within-door AUC(같은 문 안에서 한 클래스 시도를 다른 클래스보다 높게 매길 확률, 0.5가 우연)로 비교함.

**결과**

- 늦은 손 식별(timing 실패 대 force 실패, 시도 전체 구간 기준)에서 두 팔 자세 probe는 공구 손 지연 1.000, 미는 손 지연 0.970임. 공구 손 wrist torque는 1.000과 0.753, 미는 손 wrist force는 0.398과 0.966으로 자기 손의 지연만 주로 읽음. 단, 두 팔 시작 시점을 무작위로 바꾼 별도 400회 실험에서는 두 팔 자세·명령·영상 모두 0.65 이하로 내려감.
- 공구 손이 늦은 시도에서는 관측만으로 timing 실패와 원인 둘인 실패가 구별되지 않아 AUC 상한이 우연 수준인 0.500임. 로봇이 쓸 수 있는 채널은 모두 0.554 이하로 이 상한 근처에 머묾. 숨은 기준값 τ를 관측에 넣은 비교용 입력(latch-state oracle)만 1.000임.
- 같은 세계에서 최대 두 번 재시도해 막힌 시도 386건을 복구함. 두 손의 동작 시점이 겹쳤는지만 판정하고, 맞는 교정 후에도 실패하면 두 교정을 다 거는 escalation 정책이 297건을 고침. 원인 하나만 고르는 정책은 211건임. 참 원인 oracle과 모든 교정 동시 적용도 297건임. escalation은 첫 시도 복구가 200건으로 oracle의 289건보다 적고, 더 세게 민 횟수는 323회로 모든 교정 동시 적용의 386회보다 적음.
- Qwen3-VL 8B에 앞 카메라 두 프레임과 예/아니오 질문을 줌. 마지막 층 내부 상태에 건 linear probe는 늦은 손을 0.987과 0.984로 읽음. 질문 문구 세 가지에 대한 답의 중앙값은 0.497과 0.604임.

**한계**

모든 결과가 시뮬레이션의 scripted open-loop controller, 과제 하나, 문 17개에서 나왔고 learned policy와 실로봇은 시험하지 않음. 두 팔 채널의 우위는 정해진 지연 스케줄에서만 성립하고 시작 시점을 무작위로 하면 사라짐. 숨은 원인을 드러내는 active diagnosis는 향후 과제로 남겼고, 코드 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- failure detection·diagnosis·recovery 연구에서 실패 원인을 궤적에서 자동 판정하고 센서별 식별 가능성을 재는 평가 틀로 바로 쓸 수 있음. 수동 관측으로는 원인을 알 수 없는 경우를 명시하고 escalation으로 복구하는 설계는 active perception과 counterfactual 복구 연구의 비교 기준이 됨.
- VLM 내부 상태에는 늦은 손 정보가 있지만 답은 문구에 따라 흔들린다는 측정은, VLA·VLM을 실패 진단기로 쓸 때 답 대신 내부 상태 probe를 함께 확인해야 하는 근거가 됨.

*대표 그림: 측정 결과가 아니라 과제와 실패 분류 구조를 그린 그림임. 위 줄은 t=0부터 t=151까지 공구를 잡고 소켓에 끼워 돌리는 장면임. 아래 칸은 wrong gesture(삽입 실패, cam-out), force block, timing failure(공구 손 지연, 미는 손 지연), success를 key 회전·미는 힘 타임라인 막대와 함께 보여 줌.*

---

### 14. Retrieve to Act: Motion Primitive Graph Retrieval for Robust VLA Execution (70점)

[arXiv](https://arxiv.org/abs/2610.37215) · [PDF](https://arxiv.org/pdf/2610.37215) · [alphaXiv](https://www.alphaxiv.org/abs/2610.37215) (요약 있음) · [프로젝트 페이지](https://retrieve2act.github.io/r2a/) · [코드](https://anonymous.4open.science/r/r2a)

- **저자**: Pham Tri Quang, Bao-Ngoc Dao, Minh Duc Nguyen, Duc-Duy Nguyen, Hung T. Ho, Linh Dang Le, Trong-Bao Ho, Thien-Loc Ha 외 10명
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 68점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> 학습 demonstration을 이미지 없이 관절·자세 정보만으로 이은 motion primitive graph로 만들고, 실행 중 지금 움직임에 맞는 다음 동작을 검색해 고정된 VLA의 action을 보정함. LIBERO-Plus 7개 perturbation 범주 평균 성공률이 GR00T N1.7 기준 77.1%에서 89.0%로 오름.

**무슨 문제인가**

VLA는 과제 지시는 잘 따르지만 camera 각도, 조명, 배경, 로봇 시작 자세가 학습 때와 달라지면(OOD) action이 성공 궤적에서 벗어남. perturbation마다 데이터를 모아 fine-tuning하는 방법은 변형 종류가 많아 비용이 큼. 기존 test-time 방법(BYOVLA, VLS, SDN 등)은 이미지에서 과제와 무관한 시각 정보를 지우거나 외부 vision 모델로 action을 조정하는 데 집중함. 이 방법들은 학습 demonstration에 이미 들어 있는 성공한 움직임을 실행 중에 다시 꺼내 쓰지 않음.

**어떻게 푸나**

R2A(Retrieve to Act)는 VLA 가중치를 고정한 채 세 모듈을 덧붙임. 오프라인에서 성공 demonstration을 짧은 구간으로 잘라 node로 만들고, node에는 관절각, 관절 변위, gripper 상태, demonstration 안의 시간 위치만 넣음. 같은 demonstration의 몇 step 뒤 구간은 temporal edge로, 다른 과제라도 end-effector 자세가 가까운 구간은 spatial edge로 이음. 시작 자세가 학습 분포 밖이면, 과제 지시를 조건으로 한 diffusion model이 정상 시작 자세를 샘플하고 로봇을 먼저 그 자세로 옮김. 실행 중에는 VLA의 자세 예측과 최근 로봇 상태·실행 action으로 query를 만들고, query-dependent GNN(query에 따라 message passing이 바뀌는 graph neural network)이 지금의 과제와 진행 단계를 추정함. 상위 K개 구간의 다음 자세를 가중 평균해 reference motion을 만들고, 학습된 gate가 자세 차원마다 0~1 가중치로 VLA 예측을 reference 쪽으로 옮기며 gripper 명령은 그대로 둠.

**결과**

- LIBERO-Plus(LIBERO 조작 과제에 camera, 시작 자세, 언어, 조명, 배경, sensor noise, 물체 배치 7종 perturbation을 건 benchmark)에서 평균 성공률이 오름. GR00T N1.7은 77.1%에서 89.0%로, StableVLA는 78.1%에서 89.5%로, π0.5는 85.9%에서 90.4%로 오름. 가장 큰 상승은 시작 자세 범주로, GR00T N1.7이 45.8%에서 94.9%가 됨.
- LIBERO-Long(LIBERO의 여러 단계 조작 과제 10개)에 같은 7종 perturbation을 건 조건에서 test-time OOD 방법과 비교함. GR00T N1.7 평균 성공률이 R2A 82.1%, SDN 70.5%, 검색한 관측의 설명을 넣는 in-context learning 74.5%, VLS 57.3%, base 67.0%임. step당 지연은 base 138ms, R2A 159ms, VLS 807ms임.
- 구성 요소 제거 실험(GR00T N1.7)에서 gate 없이 검색 동작을 그대로 실행하면 평균 성공률이 1.2%로 내려감. GNN 대신 가장 비슷한 node를 바로 고르면 63.8%로 base 77.1%보다 낮음. LIBERO-Long의 시작 자세 범주에서 diffusion 시작 자세 보정을 빼면 87.5%가 49.9%로 내려감.
- 실제 Mobile ALOHA에서 과제 2개를 시작 자세 perturbation으로 시험함. base는 과제별 demonstration 150개로 미리 fine-tuning한 GR00T N1.7임. Banana2Pot 성공률은 30%에서 80%(SDN 55%), Cube2Drawer는 10%에서 45%(SDN 30%)로 오름.

**한계**

평균 상승의 상당 부분은 시작 자세 범주에서 나옴. 표 1에서 이 범주를 빼고 6개 범주를 평균하면 GR00T N1.7은 약 5.7퍼센트포인트, π0.5는 약 1.6퍼센트포인트 오름. 실로봇 실험은 과제 2개와 시작 자세 perturbation 하나뿐이고, 과제당 시행 횟수는 본문에서 확인 불가함. graph에 장면 형상이 없어 새 장애물을 직접 반영하지 못하고, demonstration에 없는 복구 동작은 만들 수 없음을 저자도 한계로 적음.

**누리랩 연구와의 연결**

- 학습 demonstration을 graph 형태의 robot memory로 두고, 고정된 VLA의 action을 test-time에 보정하는 구조임. failure recovery와 test-time optimization 연구에서 VLA를 건드리지 않는 비교 baseline으로 쓸 수 있음.
- gate 값은 VLA 예측과 검색 동작의 차이를 보고 정해지므로 OOD 감지 신호로 쓸 여지가 있음. 다만 논문은 gate를 failure detection 지표로 평가하지 않았음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림으로, 위쪽은 demonstration의 구간별 kinematic feature로 motion primitive graph를 만드는 오프라인 단계임. 아래쪽은 OOD 시작 자세를 diffusion으로 보정한 뒤, kinematic query로 검색한 reference motion을 VLA 예측과 gate로 합치는 실행 단계임.*

---

### 15. Tokens of Motion: Primitive Motion Learning for Human-Humanoid Skill Transfer (55점)

[arXiv](https://arxiv.org/abs/2610.37330) · [PDF](https://arxiv.org/pdf/2610.37330) · [alphaXiv](https://www.alphaxiv.org/abs/2610.37330) (요약 있음) · [프로젝트 페이지](https://tinyurl.com/ykxkbu3z)

- **저자**: Hanwen Ren, Meng Zheng, Wenzhe Cui, Benjamin Planche, Zhongpai Gao, Anwesa Choudhuri, Terrence Chen, Ziyan Wu
- **분야**: Manipulation · robotics relevance 10/10 · 1차 스크리닝 70점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> 사람 손 궤적을 짧은 구간으로 나눠 로봇과 무관한 motion primitive 표현으로 배우고, 새 로봇에는 작은 decoder만 다시 학습시켜 옮김. 사람 데이터로 배운 표현을 고정하고 decoder만 맞춘 G1 humanoid 데이터에서 구간 끝점 이동 오차 중앙값이 3.442cm임.

**무슨 문제인가**

사람 영상은 양이 많고 다양한 조작 행동을 담지만, 사람 손 움직임에는 로봇이 바로 실행할 action이 없음. 사람 손과 로봇은 형태와 kinematics가 달라서 사람 궤적을 그대로 따라 하면 로봇이 실행할 수 없는 동작이 나올 수 있음. 기존 human-to-robot 전이 방법은 궤적 전체나 의미 단위 subtask를 옮기므로, 여러 과제에 반복해 나오는 짧은 동작이 과제 순서와 장면 맥락에 묶여 다시 쓰기 어려움.

**어떻게 푸나**

M-PACT(Motion Primitives for Action Composition and Transfer)는 동작 표현 학습과 로봇별 실행을 분리함. 먼저 SkillSeg가 손목 위치, 손목 회전, 엄지와 검지 끝 거리(aperture)로 된 3D 손 궤적을 구간 label 없이 짧은 구간으로 나눔. SkillSeg는 구간 경계에 따라 달라지는 변위 복원 오차를 줄이도록 self-supervised로 학습됨. 다음으로 EPMT(Embodied Primitive Motion Tokenization)가 각 구간을 이동 code 16개 중 하나, aperture code 4개 중 하나, 3차원 연속 회전 latent로 바꿈. decoder는 이 표현과 구간 시작 시점의 손 상태를 받아 구간 전체의 이동, 회전, aperture 변화량을 출력함. 새 로봇으로 옮길 때는 로봇 궤적을 사람 손 좌표계로 맞춘 뒤 SkillSeg와 EPMT를 고정하고 parameter 27,399개짜리 decoder만 새로 학습함.

**결과**

- EgoDex(사람 egocentric 조작 영상에서 뽑은 손 궤적 데이터)로 배운 EPMT를 고정하고 decoder만 다시 학습한 HumanoidEveryday(G1 humanoid 조작 데이터)에서 구간 끝점 이동 오차 중앙값이 3.442cm임. 움직임 크기 중앙값으로 나눈 정규화 오차는 0.454로, 1보다 작아 움직이지 않는다고 예측하는 것보다 나음. 회전 오차는 0.901도임. aperture 오차는 0.229cm이지만 정규화 오차가 1.388로 움직이지 않는다는 예측보다 못함.
- decoder 적응 없이 HoloAssist(다른 사람 egocentric 영상 데이터)에 그대로 쓰면 이동 오차가 3.123cm(정규화 0.811), 회전 오차가 2.732도(정규화 0.152)임. 학습 데이터인 EgoDex의 2.658cm, 0.931도보다 높아 데이터 분포 차이의 영향이 보임.
- CC-EPMT(구간 시작 시점의 상태, 이미지, 과제 이름으로 다음 primitive를 예측하는 확장)를 held-out EgoDex 구간 292,806개에서 평가함. 이동 code top-1 정확도가 state만 쓸 때 36.37%에서 이미지와 과제 이름을 더해 40.42%로 오름. 가장 흔한 code를 고르는 baseline은 35.01%임. 예측한 표현으로 복원한 회전 오차는 20.28도로, 실제 구간에서 뽑은 표현의 0.93도보다 훨씬 큼.
- 로봇 데이터에서 이동 code를 고르는 분류기는 과제 이름과 state를 함께 쓸 때 top-1 정확도 33.98%임. 가장 흔한 code baseline은 22.56%, 사람 데이터 분류기를 그대로 쓰면 7.48%임. 모두 seed 1개 결과이고 실행 성공이 아니라 code 예측 정확도임.

**한계**

모든 정량 결과는 오프라인 복원 오차와 code 예측 정확도이고, 실제 humanoid 실험 4가지는 성공률 없이 정성 결과만 제시됨. 초록의 약 100개 robot demonstration으로 적응한다는 주장은 본문 표에서 확인 불가임. 본문의 G1 decoder는 HumanoidEveryday 4,064 episode를 85/15로 나눠 학습함. 다른 human-to-robot 전이 방법이나 action tokenizer와 직접 비교한 실험은 없음.

**누리랩 연구와의 연결**

- 손 궤적을 이동, 회전, aperture 단위의 구간 token으로 나누는 방식은 manipulation VLA의 action 표현이나 skill chaining 단위로 비교해 볼 수 있음. 다만 과제 성공률 검증이 없어 그대로 가져다 쓸 근거는 약함.
- primitive 하나를 예측하고 실행한 뒤 다시 관측하는 반복 구조는 구간 단위로 예측과 실제 결과를 대조할 수 있어 failure detection의 판정 단위로 검토할 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림이며, 왼쪽은 robot demonstration으로 VLA를 학습하거나 사람 궤적을 retarget하는 기존 방식임. 오른쪽은 egocentric 영상의 3D 손 궤적을 reach, lift, tilt/pour, place 같은 구간으로 나눠 token으로 바꾼 뒤 humanoid에서 실행하는 M-PACT 흐름임.*

---

## 오늘의 흐름

- **world model을 상상 장치가 아니라 학습 신호로 씀**: video world model로 미래를 길게 만들어 보는 대신, 미래 관측 표현 예측을 보조 loss로 쓰거나 움직이는 영역에 noise를 더 크게 걸어 그 영역을 예측하게 하는 방식이 나옴. 추론 때는 video를 만들지 않고 action만 냄. [Just Action Models](https://arxiv.org/abs/2610.37219), [Motion-guided Asymmetric Prediction](https://arxiv.org/abs/2610.36624), [TAPESTRY](https://arxiv.org/abs/2610.36823)
- **world model 안에서 다른 행동을 시험해 보고 고름**: 과거 결정 시점으로 돌아가 다른 action chunk를 넣어 보고, 결과 차이로 어느 action이 나았는지 label을 만듦. 후보 행동 여럿의 미래를 상상해 실패가 예측될 때만 행동을 바꾸는 방법도 나옴. 두 논문 모두 world model을 counterfactual 실험에 씀. [Rollback](https://arxiv.org/abs/2610.36068), [Best-of-N for World Action Model](https://arxiv.org/abs/2610.37196)
- **고정된 policy 위에 실패를 막는 보정만 따로 붙임**: task policy는 그대로 두고 residual safety filter, 사람 교정으로 범위를 정한 residual RL, demonstration graph 검색으로 action을 고침. 큰 policy를 다시 학습하지 않고 실패를 줄이는 방향임. [Learned Safety Filters](https://arxiv.org/abs/2610.37652), [Human-Guided Adaptive Residual Correction](https://arxiv.org/abs/2610.37547), [Retrieve to Act](https://arxiv.org/abs/2610.37215)
- **실패 원인을 먼저 구별하고 나서 복구함**: 어느 센서가 어떤 실패 원인을 담는지 재고, 원인을 구별할 수 없을 때 교정을 차례로 거는 복구 정책이 나옴. 로봇 제어 코드를 쓰는 coding agent가 단계마다 상태 변화를 확인하고, 가설을 실험 코드로 확인하며 프로그램을 고치는 방법도 같은 흐름임. [Which Hand Was Late?](https://arxiv.org/abs/2610.37533), [RoboAuto](https://arxiv.org/abs/2610.36533)
- **로봇이 바뀌어도 쓰는 공통 표현**: 영상에서 뽑은 latent action, 손가락 부위별 접촉, 사람 손 궤적의 motion primitive처럼 로봇 관절 공간과 무관한 표현으로 데이터를 모음. 로봇마다 그 표현을 관절 명령으로 옮기는 부분만 따로 맞춤. [RynnWorld-Latent](https://arxiv.org/abs/2610.36791), [CARD(접촉 기준 retargeting)](https://arxiv.org/abs/2610.36539), [Tokens of Motion](https://arxiv.org/abs/2610.37330)

## 해볼 만한 연구

### world model 분기 실험으로 VLA 실패 원인 구별하기
- 질문: 실패한 실제 궤적에서 어느 action chunk가 실패를 만들었는지, world model 안의 분기 실험만으로 구별할 수 있는지 밝힘.
- 첫 실험: LIBERO-Plus(LIBERO 조작 과제에 카메라·조명·물체 배치 등 7종 교란을 더한 평가 모음)의 실패 episode에서 결정 시점마다 다른 chunk로 분기해 성공률 차이가 가장 큰 시점을 고름. 이 시점을 사람이 표시한 실패 시점과 비교하고, 그 시점만 바꿔 다시 실행했을 때의 복구율을 무작위 시점 교체와 비교함.
- 가장 가까운 연구: [Rollback](https://arxiv.org/abs/2610.36068)은 같은 분기를 policy 학습 label로만 쓰고 실패 진단 정확도는 재지 않음. [Best-of-N for World Action Model](https://arxiv.org/abs/2610.37196)은 행동을 고르기만 하고 실패 원인을 말하지 않음.

### 버려지는 미래 예측 head를 실패 감지기로 쓰기
- 질문: 학습 때 미래 관측 표현을 예측하는 보조 loss(foresight loss)용으로 붙였다가 추론 때 버리는 head의 예측 오차가 실행 중 실패를 미리 알리는지 밝힘.
- 첫 실험: foresight loss로 학습한 VLA에서 head를 남겨 두고, 예측한 미래 표현과 실제 관측 표현의 거리를 매 step 기록함. 이 거리의 실패 예측 AUROC를 value head 출력, action 분산과 비교함.
- 가장 가까운 연구: [Just Action Models](https://arxiv.org/abs/2610.37219)는 head를 학습 후 버림. [Best-of-N for World Action Model](https://arxiv.org/abs/2610.37196)은 WAM(미래 관측과 action을 함께 예측하는 world action model)의 내부 표현에 실패 정보가 있음을 보였지만, 미래 예측 오차를 신호로 쓰지 않음.

### 원인을 모를 때 탐색 동작으로 원인부터 확인하는 복구
- 질문: 로봇이 따로 움직이지 않고 센서만 보는 passive 관측으로 실패 원인을 구별할 수 없을 때, 원인을 드러내는 짧은 탐색 동작을 먼저 하면 복구가 빨라지는지 밝힘.
- 첫 실험: 양팔 도구 사용 과제에서 힘을 살짝 더 주거나 한 팔을 멈춰 보는 탐색 동작 후보를 둠. 첫 시도 복구율을 교정을 차례로 거는 escalation 정책, 참 원인을 미리 아는 oracle 정책과 비교함.
- 가장 가까운 연구: [Which Hand Was Late?](https://arxiv.org/abs/2610.37533)는 이런 active diagnosis를 향후 과제로 남겼음. [RoboAuto](https://arxiv.org/abs/2610.36533)는 가설을 확인하는 실험 코드를 쓰지만 프로그램 탐색 안에서만 하고, 실행 중 복구에는 쓰지 않음.

## 꼭 읽을 논문

- [Rollback: Experience Backtracking in World Models](https://arxiv.org/abs/2610.36068): world model 안에서 과거 결정 시점으로 돌아가 action을 바꿔 보는 counterfactual 분기를 실로봇 policy 개선까지 이어서 보임.
- [How Much Can Best-of-N Help a World Action Model?](https://arxiv.org/abs/2610.37196): test-time 행동 선택의 이득을, 같은 후보를 여러 번 실행할 때 생기는 우연한 차이와 분리해 재는 절차를 제시함.
- [Dexterous In-Hand Object Pose Reaching with Learned Safety Filters](https://arxiv.org/abs/2610.37652): 고정된 policy 위에 실패 방지 보정을 얹고, 실로봇에서 물체 목표 자세 4,800개에 도달하는 시도로 평가함.
- [TAPESTRY](https://arxiv.org/abs/2610.36823): video diffusion backbone을 video 생성 없이 1 step으로 action을 내는 policy로 씀. action chunk 하나를 만드는 시간이 DreamZero의 3.7초에서 84 ms로 줄어듦.
- [Which Hand Was Late?](https://arxiv.org/abs/2610.37533): 실패 원인을 센서별로 구별할 수 있는지부터 재는 진단 평가 틀을 제시함.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (484편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2610.36068'>Rollback: Experience Backtracking in World Models for Policy Improvement</a></td><td>88</td><td>10</td><td>World Model</td><td>world model을 되감아 counterfactual 분기로 action 단위 credit을 주는 policy improvement 패러다임이며 실로봇 3과제와 world model 보정까지 보임</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2610.37652'>Dexterous In-Hand Object Pose Reaching with Learned Safety Filters</a></td><td>84</td><td>10</td><td>Dexterous Manipulation</td><td>사람 데이터 없이 시뮬레이션에서 in-hand pose reaching을 학습해 4,800개 실로봇 목표에서 95.2% 도달하고 학습된 safety filter로 drop을 75% 줄여 강한 실증을 보임</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2610.37219'>Vision-Language-Action or World-Action? Just Action Models</a></td><td>82</td><td>10</td><td>VLA</td><td>VLA와 WAM 논쟁의 세 선택지를 분리해 생성 없이 foresight loss만 쓰는 JAM으로 통합하고 LIBERO와 LIBERO-Plus에서 FastWAM 대비 성공률을 올리며 학습 FLOPs 73% 절감한 강한 정리와 증거임</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2610.36823'>TAPESTRY: A Single Backbone for Video Generation and Robot Control</a></td><td>80</td><td>10</td><td>VLA</td><td>action을 video latent의 single-patch token으로 넣어 pretrained video DiT를 policy로 바꾸는 world action model이며 video 생성 없이 1-step 추론하고 CoRL 수준의 실로봇 결과를 보임</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2610.37196'>How Much Can Best-of-N Help a World Action Model? Measuring Selectable Headroom and Realizing It in Closed Loop</a></td><td>80</td><td>10</td><td>World Model</td><td>WAM의 best-of-N 선택 가능 headroom을 denoised counterfactual protocol로 정량화하고 실패 예측 gate로 폐루프 성공률을 올린 test-time selection 연구이며 가설 검증이 엄밀함</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2610.36791'>RynnWorld-Latent: A Cross-Embodiment World Model Conditioned on Universal Latent Actions</a></td><td>78</td><td>9</td><td>World Model</td><td>universal latent action으로 human과 robot과 simulation 영상을 553M frame 규모로 함께 pretrain한 cross-embodiment world model이며 policy 성공률과 실로봇 이득을 보임</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2610.36539'>CARD: Contact-Anchored Retargeting for Dexterous Manipulation</a></td><td>76</td><td>9</td><td>Dexterous Manipulation</td><td>human 데이터를 contact force 목표로 retarget하는 새 formulation과 tactile tracking controller, video-to-contact 모델까지 갖췄고 실기 replay로 확인함</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2610.37518'>World Dreamer v5-lite: A Multi-Robot World Action Model with One Dreamer</a></td><td>74</td><td>10</td><td>VLA</td><td>공유 world state 하나로 여러 로봇의 action을 예측하는 multi-robot world action model이며 RoboFactory에서 23.7퍼센트포인트 우위와 실로봇 4과제 결과를 보임</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2610.36533'>RoboAuto: Autonomous Robot Program Search through Multi-Level Physical Understanding</a></td><td>72</td><td>10</td><td>Manipulation</td><td>물리 이해를 object와 scene과 interaction 수준으로 조직한 code-as-policy 프로그램 탐색이며 self-designed experiment로 가설을 검증하고 실로봇 장기 과제에서 pi0.5보다 낫다고 보임</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2610.37547'>When, Where, and What to Correct: Human-Guided Adaptive Residual Correction for Robot Policies</a></td><td>72</td><td>10</td><td>IL</td><td>sparse human correction으로 residual RL의 when과 where를 구조화해 frozen policy를 후학습하며 실로봇 3과제에서 33.3%를 75.0%로 올림</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2610.36624'>Adapting Video Models for Robot Control via Motion-guided Asymmetric Prediction</a></td><td>72</td><td>9</td><td>World Model</td><td>WAM의 시각 예측 supervision을 동적 영역에 비대칭 noise로 집중시키는 단순하고 일반적인 아이디어이며 GR-1에서 두 WAM 구조 모두 성공률을 8~10퍼센트포인트 올렸음</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2610.37393'>Learning Quality-Controllable Robot Policies with Iterative Hindsight Relabeling</a></td><td>72</td><td>9</td><td>IL</td><td>속도와 안정성 같은 품질을 inference 시 조절하는 policy와 반복 hindsight relabeling을 제안해 초기 demonstration 품질을 넘고 실로봇 이득도 보임</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2610.37330'>Tokens of Motion: Primitive Motion Learning for Human-Humanoid Skill Transfer</a></td><td>70</td><td>10</td><td>VLA</td><td>인간 손 궤적에서 embodiment와 무관한 motion primitive를 배우고 로봇별 decoder로 옮김. 스크리닝 당시 다른 논문 초록이 붙어 있어 점수는 정밀 리뷰에서 다시 매김</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2610.37533'>Which Hand Was Late? Diagnosis for Robot Failure Recovery in Bimanual Tool Use</a></td><td>70</td><td>9</td><td>Failure Detection</td><td>bimanual 도구 사용 실패를 센서 채널별로 어느 손이 늦었는지 식별 가능성까지 분석하고 식별 불가 시 escalate하는 복구 정책을 보인 진단 연구이며 시뮬레이션 한정임</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2610.37215'>Retrieve to Act: Motion Primitive Graph Retrieval for Robust VLA Execution</a></td><td>68</td><td>10</td><td>VLA</td><td>학습 demo를 motion primitive graph로 만들어 test-time에 검색하고 frozen VLA 행동과 gating으로 합쳐 OOD 강건성을 올렸으며 세 VLA와 실로봇에서 검증함</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2610.36420'>SO-101 Bench: Accessible Spatial Manipulation</a></td><td>68</td><td>9</td><td>Manipulation</td><td>SO-101용 시뮬레이션 벤치마크로 digital twin이 실로봇 정책 순위를 그대로 재현함을 보이고 VLA 9종과 LLM agent를 비교한 재현 가능한 평가 자원임</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2610.36840'>Trace-WAM: Learning to Act via 3D Motion Prediction for World Action Models</a></td><td>68</td><td>9</td><td>VLA</td><td>world action model에 미래 3D motion 예측을 보조 목표로 넣어 추론 비용 없이 일반화를 높였고 LIBERO-Plus에서 이득을 보임, 실로봇은 확인 불가임</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2610.36859'>ActiveAlign: Aligning Egocentric Manipulation via Active Perception</a></td><td>68</td><td>9</td><td>Active Perception</td><td>능동적 손 동작과 촉각으로 real2sim 정렬 간극을 줄이는 active perception 접근이며 G1 실로봇의 mm 단위 조작으로 검증함</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2610.37091'>GAWM: A Compact Latent World-Action Model for Multi-Task Robot Manipulation</a></td><td>68</td><td>9</td><td>VLA</td><td>100M 미만 파라미터의 latent world-action model이 billion 규모 WAM을 RoboTwin에서 넘고 이중 팔 실기에서 지연도 낮춰 효율 측면 증거가 좋음</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2610.37543'>Rendering-Free Event Frame Simulation for Fast Reinforcement Learning of Autonomous Robot Navigation</a></td><td>68</td><td>8</td><td>Navigation</td><td>렌더링 없는 analytic event simulator로 RL을 400배 빠르게 학습시키고 56g Crazyflie에서 zero-shot 비행에 성공해 원리와 실기 증거가 모두 좋음</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2610.37557'>Learning Visuomotor Quadrotor Flight Through Dynamic Narrow Gaps via Differentiable Simulation</a></td><td>68</td><td>8</td><td>RL</td><td>미분 가능한 moving-gap 정식화로 teacher 없이 시각 policy를 처음부터 학습해 실제 쿼드로터가 움직이는 틈을 통과해 원리와 실기 증거가 있음, 실기 10회 시도임</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2610.36270'>Learning Multi-Phase Robot Loco-Manipulation via Phase-Conditioned Policy Optimization</a></td><td>66</td><td>9</td><td>RL</td><td>phase-conditioned critic과 reset curriculum으로 multi-phase loco-manipulation을 PPO로 학습해 G1과 Spot 실기에서 검증함</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2610.36694'>TOPS: Reshaping Flow Source and Transport for Multi-Task Robot Manipulation</a></td><td>66</td><td>9</td><td>VLA</td><td>flow policy의 source prior와 transport schedule을 과제별로 바꾸는 formulation으로 1-step 추론과 pi0.5 이식, 실로봇 이득을 보임</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2610.37378'>VLA-Stem: A Lightweight Safety Mechanism for Vision-Language-Action Models via Reinforcement Learning</a></td><td>66</td><td>9</td><td>VLA</td><td>VLA를 고정한 채 RL stem 정책이 action chunk를 장애물 회피로 보정하는 안전 모듈이며 충돌 없는 성공률 52.8% 대 23.7%와 실기 결과가 있음</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2610.37170'>From 12 to 200 Demonstrations: How ACT, Diffusion Policy, SmolVLA and $π_{0.5}$ Scale on a Low-Cost Arm</a></td><td>64</td><td>9</td><td>IL</td><td>ACT와 DP와 SmolVLA와 pi0.5를 demonstration 수별로 1,340 실로봇 에피소드에서 비교한 재현성 높은 실증 연구이며 평가 노이즈까지 계량함</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2610.36662'>SWIM: Learning What Matters from Behaviors for JEPA World Models</a></td><td>64</td><td>8</td><td>World Model</td><td>inverse dynamics로 state feature 가중치를 학습해 JEPA world model의 planning을 개선했으나 시뮬레이션 5과제뿐임</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2610.37381'>PDRVLA: A Vision-Language-Action Model with Physical Dynamics Representations</a></td><td>62</td><td>9</td><td>VLA</td><td>physical dynamics 토큰으로 미래 RGB와 depth와 flow를 예측해 video 생성 없이 action을 조건화한 VLA이며 여러 benchmark 수치가 높으나 실로봇은 확인 불가임</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2610.36374'>HIDRA: Hierarchical Dual-Routing Attention for Replay-Free Lifelong Imitation Learning</a></td><td>62</td><td>8</td><td>IL</td><td>replay-free lifelong imitation learning에서 dual-attention expert routing과 key 정규화를 제안했고 LIBERO에서 baseline을 넘어섬</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2610.37203'>Remember Where You Walk: Learning Spatial Memory for End-to-End Legged Robot Exploration</a></td><td>62</td><td>8</td><td>Robot Memory</td><td>위치 기반 memory cell을 가진 Hadamard memory로 legged 탐색에서 미로 구조를 기억하게 했으며 robot memory 주제와 맞으나 미로 시뮬레이션뿐임</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2610.37437'>Representing the Unseen: Rethinking Visual Imagination for Spatial Reasoning</a></td><td>62</td><td>6</td><td>Embodied AI</td><td>world model이 상상한 상태의 표현(RGB, depth, top-down)이 공간 추론에 미치는 영향을 통제 비교하고 test-time 표현 선택 GEARS를 제안해 embodied spatial reasoning과 잘 맞으나 로봇 실험은 없음</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2610.37588'>Understanding the limits of latent world models</a></td><td>62</td><td>6</td><td>World Model</td><td>latent world model의 faithfulness를 transition과 latent dynamics의 equivariance로 정의하고 LRC 지표를 제안함, 기존 모델이 환경을 충실히 모사하지 못함을 보임</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2610.36925'>Vision-Language Agents Can Learn in Their Own Latent Worlds</a></td><td>62</td><td>6</td><td>World Model</td><td>VLM agent가 latent world에서 경험 학습함. world model 방향이나 로봇 검증 불확실함</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2610.36452'>Whole-Body Humanoid Control via Stochastic Motion Tokenization</a></td><td>60</td><td>8</td><td>Humanoid</td><td>stochastic motion tokenizer로 텍스트 조건 whole-body 모션을 G1 실기에서 실행했고 FSQ와 VQ-VAE보다 복원이 낫다고 보임</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2610.36507'>GRAFT: Geometry-Aware Residual Adaptation for Foundation Trackers</a></td><td>60</td><td>8</td><td>Humanoid</td><td>frozen humanoid tracker 위에 지형 적응 residual adapter를 얹어 G1 실기에서 계단을 오름, 접근은 실용적이나 모듈 성격임</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2610.36852'>When Black-Box Robot Policies Fail: Online Sensor Diagnosis and Repair with a Transparent Surrogate</a></td><td>60</td><td>8</td><td>Failure Detection</td><td>frozen black-box policy의 센서 고장을 투명 surrogate로 진단하고 복구하는 문제 설정이 좋으나 Go2 시뮬레이션과 정책 하나에 한정됨</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2610.36247'>Freeze, Don&#x27;t Clone: Fine-Tuning with Expressive Policies Without Retaining Offline Data</a></td><td>60</td><td>6</td><td>RL</td><td>offline 데이터 없이 online fine-tuning할 때 BC가 prior를 지우는 actor 쪽 실패를 짚고 prior 동결로 개선함, OGBench 7개 도메인에서 FQL·QC에 적용함</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2610.36250'>cuArms: GPU-Accelerated Conflict-Based Planning for Multi-Arm Manipulation</a></td><td>58</td><td>8</td><td>Manipulation</td><td>GPU 병렬 conflict-based multi-arm 계획기로 실시간 해를 냈고 실제 산업 과제도 보였으나 고전 planning 계열임</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2610.36598'>OpenJaws: An Open Hardware UMI Framework with Stereo Localization for Generalist Manipulation</a></td><td>58</td><td>8</td><td>Manipulation</td><td>UMI 데이터 수집 장치에 stereo 위치추정과 open hardware를 더해 localization 정확도를 높였고 benchmark와 실로봇 배포를 보임, 시스템 기여임</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2610.36825'>HC2Robot: Hyper-Connection Transformers with Predicted Foresight for Multi-Terrain Humanoid Parkour</a></td><td>58</td><td>8</td><td>Humanoid</td><td>다음 touchdown을 예측하는 foresight 모듈로 privileged 정보 간극을 줄인 humanoid parkour이나 실험이 시뮬레이션 위주임</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2610.36968'>Omni-IGN: Onboard Image-Goal Navigation for Drones with Omnidirectional Vision</a></td><td>58</td><td>8</td><td>Navigation</td><td>quad-fisheye와 attention RL policy로 드론 image-goal navigation을 온보드로 수행하고 zero-shot sim-to-real을 보였으나 새로운 원리는 약함</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2610.37509'>Ego-CEVR: Learning Cross-Embodiment Visual Representations from Human Egocentric Videos</a></td><td>58</td><td>8</td><td>Representation Learning</td><td>human egocentric 영상으로 global 표현을, 로봇 데이터로 interaction 표현을 따로 학습하는 구조이나 초록에 정량 결과가 없음</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2610.36615'>HumiMimic: Mimetic Embodiment Transfer of Human-Humanoid Interaction from In-the-Wild Videos</a></td><td>58</td><td>7</td><td>Humanoid</td><td>in-the-wild human-human 상호작용 영상을 humanoid 상호작용으로 retarget하는 파이프라인과 데이터셋이며 실로봇 실행도 확인함</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2610.37098'>SplatScout: Query-Driven Part-Level Referring Segmentation in Gaussian Scenes</a></td><td>58</td><td>6</td><td>3D Vision</td><td>VLM이 view 선택, 분할, 3D 결과 검수를 폐루프로 수행하는 part 단위 referring segmentation으로 active perception 성격이 있으나 평가가 ScanNet++ 12개 장면 규모임</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2610.37299'>Structured Representation Probing for Risk Anticipation in End-to-End Autonomous Driving</a></td><td>58</td><td>6</td><td>Embodied AI</td><td>end-to-end 주행 policy의 내부 표현을 선형 probe로 읽어 실패를 미리 경고함, Bench2Drive에서 3개 모델에 적용한 failure anticipation임</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2610.36371'>BoxWorld: Let World Engines Control and Video Generators Render</a></td><td>58</td><td>4</td><td>World Model</td><td>규칙을 코드 엔진으로 분리해 객체 상태를 제어하고 video generator는 렌더링만 맡기는 world model 설계가 참신하나 게임 영상 기반이고 로봇 검증은 없음</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2610.36685'>RoboSTD: Zero-Shot Single-to-Dual Transfer via Sagittal Mirroring for Bimanual Learning</a></td><td>56</td><td>8</td><td>Manipulation</td><td>단일 팔 데이터를 sagittal mirroring과 LLM 제약으로 bimanual 의사 demonstration으로 바꾸는 데이터 생성 아이디어이며 실기 평가는 얕음</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2610.36546'>REACH: An RL-based Hierarchical Humanoid Crawling Framework for Adaptable Confined Space Traversal</a></td><td>55</td><td>8</td><td>Humanoid</td><td>G1 humanoid의 가변 높이 보행과 crawling 계층 RL을 실기에서 검증했으나 개별 skill 조합의 engineering 성격임</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2610.36961'>Keeping Contact: Task-Adaptive Friction Margins for Bimanual Non-Prehensile Manipulation</a></td><td>55</td><td>8</td><td>Manipulation</td><td>friction margin을 task에 맞게 정하는 SOCP 기반 bimanual non-prehensile 계획으로 실기에서 확인했으나 모델 기반 고전 접근임</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2610.37550'>Kinematic Constraint-Referenced Evaluation for Articulated Object Manipulation</a></td><td>55</td><td>8</td><td>Evaluation</td><td>성공률 대신 관절 축 기준 twist로 articulated 조작을 평가하는 지표 제안으로 실패 원인 구분에 유용하나 시뮬레이션뿐임</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2610.37111'>RAVEN: A Unified Active SLAM System for Rapid Autonomous Visual Exploration with Aerial Robots under Localization Uncertainty</a></td><td>55</td><td>7</td><td>Active SLAM</td><td>탐색과 loop closure 균형을 조절하는 쿼드로터 active SLAM 프레임워크로 field 실험까지 했으나 구성요소 통합 성격임</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2610.37619'>Perceiving and Predicting Dynamic Sports: Spatiotemporal Intelligence in Vision Models for Egocentric Tennis Video</a></td><td>55</td><td>6</td><td>Embodied AI</td><td>egocentric 테니스 영상으로 선수와 공의 위치, 미래 궤적, 접촉 시점 예측에 대해 vision encoder들을 비교하고 실시간 동작 생성까지 연결해 agile robot 관점이 있으나 데이터와 로봇 실험 규모가 작음</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2610.36309'>Bridging Exploration and Loss of Plasticity in On-Policy Reinforcement Learning</a></td><td>55</td><td>6</td><td>RL</td><td>PPO의 policy 표준편차가 loss of plasticity에 미치는 영향을 이론과 실험으로 분석하고 7자유도 로봇팔 배포까지 보임</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2610.36837'>ExecDiffuser: Closing the Sample-to-Execution Gap in Diffusion Planning</a></td><td>55</td><td>6</td><td>Autonomous Driving</td><td>sample과 execution 간극을 줄이는 diffusion 계획으로 nuPlan에서 개선했으나 benchmark 점수 개선 성격임</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2610.37441'>Multi-Agent Reinforcement Learning of Co-Adaptive Hip Exoskeleton Control (MARL-Exo) for Metabolic Energy Reduction</a></td><td>55</td><td>6</td><td>RL</td><td>musculoskeletal 인체 모델과 exoskeleton 정책을 MARL로 함께 학습해 사용자 8명에게 튜닝 없이 적용한 증거가 있으나 보조기기 특화임</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2610.36150'>Any3R: Feedforward 3D Reconstruction from Any Camera Type</a></td><td>55</td><td>5</td><td>3D Vision</td><td>ray field 기반 positional encoding과 solid-angle loss로 임의 central camera를 재학습 없이 처리하는 feed-forward 재구성이며 로봇 다중 카메라 활용 가능성은 있으나 직접 연결은 약함</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2610.36462'>ClusterSplat: Semantic Cluster Selection for 3D Visual Grounding in Gaussian Splatting</a></td><td>55</td><td>5</td><td>3D Vision</td><td>3DGS 위 referring grounding을 클러스터 후보 선택으로 재정식화해 불안정한 임계값 문제를 줄였고 scene representation에 유용하나 로봇 평가는 없음</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2610.36765'>Evaluation-Guided Demonstration Refinement for Vision-Language-Action Policies: The Winning Entry in the MetaFine Open Competition</a></td><td>52</td><td>8</td><td>VLA</td><td>pi0.5 fine-tuning에서 실패 사례를 보고 demonstration을 수정하고 expert continuation을 추가한 실용적 대회 우승 기록으로 새 방법론은 약하나 failure 기반 데이터 보강 사례로 참고됨</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2610.36285'>ASPEN: Adaptive Semantic Reasoning via Command Persistence Prediction for Efficient Navigation VLAs</a></td><td>52</td><td>7</td><td>Navigation</td><td>navigation VLA의 reasoning 호출을 persistence 예측으로 줄이는 scheduler이나 절감폭이 9.5%로 작음</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2610.36853'>LingGS: Decoupling Feed-Forward Geometry Prediction from Camera Tracking for High-Fidelity Gaussian SLAM</a></td><td>52</td><td>6</td><td>3D Vision</td><td>frozen 3D foundation model을 가상 RGB-D로 쓰고 기하 solver로 pose를 추적해 Gaussian SLAM을 7 FPS로 구동하며 online mapping에 쓸 만하나 구성 요소 조합 성격이 강함</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2610.37326'>ScIntBench: Physical Interaction Plausibility in 3D Scene Generation</a></td><td>52</td><td>6</td><td>Embodied AI</td><td>생성된 3D 실내 장면에서 push, open 같은 조작을 시뮬레이션으로 실행해 interaction readiness를 재는 벤치마크이며 정적 타당성이 상호작용 성공과 맞지 않음을 12개 시스템으로 보임</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2610.36079'>Closed-Loop Aware Planning via Imitation-Free Speed Scoring for End-to-End Autonomous Driving</a></td><td>52</td><td>6</td><td>Autonomous Driving</td><td>imitation-free speed scoring head로 test-time 속도 제어를 가능하게 했으나 주행 벤치마크 중심의 plug-in 모듈임</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2610.36592'>LabWorld: Learning Interactive 4D Worlds for Scientific Experimentation</a></td><td>52</td><td>5</td><td>3D Vision</td><td>단안 영상에서 객체 상태와 이벤트가 있는 4D 실험실 세계를 Real2Sim으로 복원하는 구성이 흥미로우나 baseline 대비 향상 폭이 작고 평가 규모가 작음</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2610.37451'>Interpretable Meta-Policies for Neural Decision Making</a></td><td>52</td><td>5</td><td>RL</td><td>object-centric 관측 위에 신경 skill과 symbolic meta-policy를 쌓은 계층 RL이며 해석성과 정렬을 보임, 게임 환경 한정임</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2610.36729'>Hy-Nomas: Towards Free-form Interactive World Generation</a></td><td>52</td><td>4</td><td>World Model</td><td>8B video world model이 구조화 caption과 action-aware causal attention으로 다중 턴 상호작용과 카메라 제어를 지원하고 가중치를 공개했으나 평가가 human eval 중심임</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2610.36425'>Repulsive Population Policy Gradients for Behaviorally Diverse Reinforcement Learning</a></td><td>52</td><td>4</td><td>RL</td><td>PPO를 population 단위 repulsive reward로 확장한 QD-RL로 pixel·LLM까지 확장 시도함, 로봇 과제 직접 검증은 약함</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2610.36210'>Diagnosing and Correcting Bias in MLLM for Long Video Understanding</a></td><td>52</td><td>3</td><td>Video</td><td>counterfactual view로 편향 효과를 추정하고 hidden state를 개입하는 training-free 추론으로 test-time 관점은 흥미로우나 장시간 비디오 QA에 국한됨</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2610.36471'>When to Intervene? An Empirical Study of Errors and Self-Recovery in LLM Agents</a></td><td>52</td><td>3</td><td>AI</td><td>LLM agent 오류와 자기복구 시점의 실증 연구임. failure recovery 관점이나 웹 agent 한정임</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2610.36537'>A Trainable CPG Framework for Quadruped Locomotion</a></td><td>50</td><td>7</td><td>Locomotion</td><td>8뉴런 CPG와 execution network로 5개 gait 전환을 Go2 실기에서 보였으나 locomotion 제어의 점진적 개선임</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2610.36535'>A generalist policy for muscle-driven control across individual musculoskeletal models</a></td><td>50</td><td>5</td><td>Control</td><td>개인별 musculoskeletal 모델에 일반화되는 morphology-conditioned policy로 시뮬레이션 중심이고 로봇 manipulation과는 거리가 있음</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2610.37037'>Zooming without Zooming v2: From Seeing Details to Connecting Evidence for Generalizable Multimodal Perception</a></td><td>50</td><td>4</td><td>Multimodal</td><td>zoom 영역으로 증거 연결 질문을 합성하고 RLVR로 학습해 spatial 및 embodied spatial reasoning까지 전이를 보이나 데이터 합성과 RL 조합 위주임</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2610.37633'>Repurposing Video Diffusion Transformers for Cross-View Temporal Object Correspondence</a></td><td>50</td><td>4</td><td>Video</td><td>video DiT를 cross-view temporal 객체 대응에 재활용하고 pseudo-label로 dense 학습해 ego-exo 객체 추적에 쓸 만하나 평가 범위가 좁음</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2610.37567'>Gym-Anything-RT: Scaling Real-Time Environments for Vision-Language Agents</a></td><td>50</td><td>4</td><td>Embodied AI</td><td>환경이 진행되는 실시간 상호작용에서 vision-language agent 능력을 재는 minigame 벤치마크이며 일시 정지 대조 설계가 유용함, 시뮬 게임 한정임</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2610.37255'>Your Policy Is Secretly a Harness: The Decision Geometry of Agent Interfaces</a></td><td>50</td><td>3</td><td>RL</td><td>agent harness를 KL 정규화 제어로 분해해 ceiling과 mismatch 개념을 세움, MiniWoB++와 Terminal-Bench에서 예측이 맞음</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2610.37175'>MLE-World: Predicting Machine Learning Experiment Outcomes with a Learned World Model</a></td><td>50</td><td>2</td><td>World Model</td><td>코드와 데이터만으로 ML 실험 결과를 예측하는 world model로 test-time scaling을 저렴하게 만듦, 로봇 영역은 아닌 연구임</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2610.36384'>SOMA: A Benchmark for Fine-Grained Egocentric Behavior and Body-Motion Understanding</a></td><td>48</td><td>4</td><td>Video</td><td>egocentric 영상에서 신체 동작 이해를 재는 SOMA 벤치마크와 학습 데이터로 37개 MLLM 약점을 진단하나 방법 기여는 작음</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2610.37046'>Learning to Code the World: Harness Evolution for Compositional 3D Reconstruction</a></td><td>48</td><td>4</td><td>3D Vision</td><td>3D scene을 실행 코드로 표현하고 harness를 진화시켜 작은 모델로 대형 모델을 앞서는 구성이 흥미로우나 모델과 비교 대상이 가변적이라 증거 해석에 주의 필요함</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2610.37257'>GameVerse: A Minute-Scale Gameplay Dataset for Long-Horizon Interactive World Modeling</a></td><td>48</td><td>4</td><td>World Model</td><td>2분 길이 연속 게임 영상과 event 기반 caption 1,655시간 규모 데이터셋으로 long-horizon world model 학습을 겨냥하나 데이터 자원 중심이고 로봇 영상은 아닌 점이 한계임</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2610.36959'>Live-OPSD: On-Policy Self-Distillation for Proactive Streaming Large Video Models</a></td><td>48</td><td>3</td><td>Video</td><td>streaming video 비서가 언제 응답할지를 privileged hint 기반 on-policy self-distillation으로 학습함, 로봇 직접 실험은 없음</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2610.37195'>Action-Value Calibration via Continuation Sharing for Long-Horizon Agentic Reinforcement Learning</a></td><td>48</td><td>3</td><td>RL</td><td>long-horizon agent RL의 credit assignment를 continuation 공유로 보정함, ALFWorld·WebShop 소형 모델 개선임</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2610.36077'>The Trinity: Capability-Driven Recursive Self-Improvement for Multimodal Agents</a></td><td>48</td><td>3</td><td>Multimodal</td><td>multimodal agent 재귀적 자기개선 프레임워크임. 주장 위주이고 로봇 연결 약함</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2610.36544'>Monitor Accuracy Isn&#x27;t the Answer: A Decision-Value Framework for Evaluating AI Agent Restart Monitors</a></td><td>48</td><td>3</td><td>AI</td><td>agent 재시작 monitor의 decision-value 평가 틀임. failure detection 관점에서 참고 가능함</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2610.36467'>Confident First, Reflective Second: Reinforcement Learning of Confidence-Preserving Reflection for Video Understanding</a></td><td>48</td><td>2</td><td>Video</td><td>RL에서 초기 답이 약해지는 confidence erosion을 발견하고 세 경로별 완화책을 제시한 분석이 좋으나 비디오 QA 점수 개선 폭은 1.7점으로 작음</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2610.37211'>Uncovering Shortcut Amplification in Video RLVR through the Lens of Perceptual Uncertainty Collapse</a></td><td>48</td><td>2</td><td>Video</td><td>video RLVR에서 text prior로 쏠리는 perceptual uncertainty collapse를 분석하고 self-distillation으로 완화하는 점은 의미 있으나 비디오 QA 범위임</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2610.37471'>PerceptRL: Making Visual Perception Rewardable in MLLMs from Answers to Interactions</a></td><td>48</td><td>2</td><td>Multimodal</td><td>caption 오류에서 검증 가능한 QA를 만들고 tool 기반 multi-turn 인식 RL을 하는 pipeline으로 구성이 길고 새 원리보다 조합 성격임</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2610.37146'>Variational Optimal Control for Diffusion Guidance</a></td><td>48</td><td>2</td><td>Generative</td><td>diffusion guidance와 reward 적응을 optimal control의 pullback으로 통합하고 ImageNet FID 개선을 보임</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2610.36761'>Making Self-Driving Laboratories Auditable:A Unified Framework for Hybrid Actions,Measurements, and Safe Execution</a></td><td>46</td><td>6</td><td>VLA</td><td>실험실 자동화용 VLA 확장과 안전 runtime 틀을 제안했으나 정량 결과 없이 설계 제안 수준임</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2610.36789'>A fully articulated humanoid dexterous hand with human-level joint structure enabled by linkage-based actuation</a></td><td>46</td><td>6</td><td>Hardware</td><td>21-DoF linkage 구동 humanoid hand 하드웨어 설계로 학습 기여는 없음</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2610.36877'>GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents</a></td><td>46</td><td>3</td><td>Multimodal</td><td>JEPA latent를 GUI agent 빠른 action policy로 씀. 로봇 아닌 GUI 한정임</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2610.37470'>Autonomous fixed-wing interception using reinforcement learning</a></td><td>45</td><td>6</td><td>RL</td><td>단안 시각에서 actuator 명령까지 PPO로 학습한 고정익 요격기를 실제 비행으로 검증했으나 석사 논문 수준의 응용임</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2610.37582'>EgoThumb: A Vision-Driven Supernumerary Robotic Thumb for Autonomous Grasp and Holding Assistance</a></td><td>45</td><td>6</td><td>Manipulation</td><td>egocentric 영상으로 동작하는 supernumerary thumb 하드웨어와 imitation policy이며 보조기기 응용임</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2610.37000'>GPA-VGGT: Geometry-Preserving Acceleration of VGGT</a></td><td>45</td><td>4</td><td>3D Vision</td><td>VGGT 초기 block의 global attention을 frame attention과 공유 K/V로 바꿔 pose 정확도 99% 이상을 유지하는 training-free 가속으로 로봇 3D perception 효율화에 쓸 만함</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2610.36785'>OmniGlimpse: Asymmetric Identity Memory for Online Multi-View Tracking</a></td><td>45</td><td>3</td><td>CV</td><td>propose-verify 구조로 적응 표현과 안정 memory를 분리한 온라인 다중 시점 identity 유지가 설계상 흥미로우나 추적 벤치마크에 한정됨</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2610.37093'>Learning to Look Beyond Screens: Transferable Visual Observation from GUI Grounding</a></td><td>45</td><td>3</td><td>Multimodal</td><td>GUI grounding 궤적으로 crop-and-inspect 관찰 행동을 SFT와 RL로 학습해 다른 벤치마크로 전이시킨 active perception 연구이나 로봇 환경은 아닌 점이 한계임</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2610.37364'>EmbeddingGemma 2: Unified and Efficient Multimodal Representations</a></td><td>45</td><td>3</td><td>Multimodal</td><td>텍스트·이미지·오디오·비디오를 한 공간에 넣는 오픈 임베딩 모델이며 기술 보고 성격임</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2610.37649'>Can LLMs Uncover Hidden Physical Laws through Free Exploration?</a></td><td>45</td><td>3</td><td>NLP</td><td>바뀐 물리법칙을 탐색으로 발견하는 LLM 평가임. 물리 추론 관점에서 약한 연결임</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2610.36415'>Verifiable Efficiency Limits of Innate LLM Planning in Sliding Puzzles</a></td><td>45</td><td>3</td><td>AI</td><td>슬라이딩 퍼즐로 LLM 고유 planning 한계를 검증함. planning 연결 약함</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2610.36493'>AC-JEPA: Anchored Cross-Modal Joint Embedding Predictive Architecture for Visual-to-Symbolic Translation</a></td><td>45</td><td>3</td><td>Representation</td><td>JEPA로 시각-기호 변환함. representation 관점이나 로봇 검증 없음</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2610.36269'>Cross-modal Steering Vectors Exist Across Both Image and Text Generation</a></td><td>45</td><td>2</td><td>Multimodal</td><td>통합 멀티모달 모델에서 steering vector가 modality 간 zero-shot 전이됨을 인과적으로 보인 분석이나 로봇 적용은 불명확함</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2610.36554'>PRISM-BENCH: Diagnosing Grounded and Faithful Multimodal Reasoning Beyond Final-Answer Accuracy</a></td><td>45</td><td>2</td><td>Multimodal</td><td>추론 trace로 grounding 실패와 효율을 진단하는 벤치마크로 VLM 실패 원인 분석이 유용하나 로봇 연결은 약함</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2610.36671'>Look Only When Needed: Certificate-Guided Visual Routing for Efficient Diffusion VLMs</a></td><td>45</td><td>2</td><td>Multimodal</td><td>이미지 없이 예측한 토큰과 비교해 이미지 처리 여부를 결정하는 training-free 추론 효율화로 FLOPs를 35%로 줄였으나 diffusion VLM 한정임</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2610.37613'>VideoLVR: Latent Visual Reasoning over Grounded Video Evidence</a></td><td>45</td><td>2</td><td>Video</td><td>video 추론 중 관련 순간의 latent visual evidence를 생성해 재방문하는 방식이 흥미로우나 비디오 벤치마크 범위임</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2610.36628'>The Batch Size Can Be One: Test-Time Adaptation from Classifier Geometry</a></td><td>45</td><td>2</td><td>CV</td><td>batch size 1 test-time adaptation을 classifier 기하에서 풀며 corruption 벤치마크 전반에서 안정적임, 분류 과제 한정임</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2610.36419'>SpeeDiff: Scalable Pixel-Anchored End-to-End Latent Diffusion Model</a></td><td>45</td><td>1</td><td>Generative</td><td>VAE와 diffusion을 end-to-end로 학습하는 Tweedie 복원 loss로 학습 속도를 크게 높였으나 이미지 생성 한정임</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2610.36831'>Right Click, Wrong Box: Grading GUI Grounding by What a Click Does</a></td><td>45</td><td>1</td><td>Multimodal</td><td>GUI grounding 클릭을 실행 결과로 채점해 box 평가가 정답을 과소 집계함을 보인 평가 분석이나 GUI 도메인이고 RL 보상 개선은 불안정함</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2610.36312'>SG^2SLAM: Spatial Geometry-Informed 3D Gaussian Splatting SLAM for Monocular Outdoor Navigation</a></td><td>42</td><td>6</td><td>3D Vision</td><td>streaming geometry prior와 ray-conditioned 3DGS를 결합한 단안 SLAM으로 KITTI와 Waymo 평가의 incremental 기여임</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2610.37535'>Predict the Swing, Match the Speed: Robotic Pipe Stabbing With Learned Stereo Vision and Residual Reinforcement Learning</a></td><td>42</td><td>6</td><td>RL</td><td>시추 파이프 stabbing에 stereo 인식과 residual RL을 적용했으나 1:4 스케일 MuJoCo 모델 결과뿐임</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2610.36681'>From Biological Curves to Soft Modular Robots: Learning-Based Inverse Design with Uncertainty-Guided Refinement</a></td><td>42</td><td>5</td><td>Soft Robotics</td><td>soft modular robot의 surrogate 기반 inverse design으로 속도 향상은 크지만 응용이 좁음</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2610.36726'>Learning Side-by-Side Navigation for Personal Mobility Vehicles from Human Drivers</a></td><td>42</td><td>5</td><td>Navigation</td><td>두 대의 개인 이동 장치가 나란히 가는 계획을 IRL로 학습했으나 시뮬레이션만 평가함</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2610.36876'>HoloRecon: Incremental Reconstruction of Long-Range Panoramas with Global Consistency</a></td><td>42</td><td>4</td><td>3D Vision</td><td>feed-forward 국소 기하로 원거리 loop 매칭을 3D 검증해 파노라마 pose graph를 최적화하며 SLAM 문제에 맞으나 새 benchmark와 평가 규모가 작음</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2610.36760'>GeoGSplat: Geometry-Grounded Non-Pixel-Aligned Gaussian Splatting</a></td><td>42</td><td>3</td><td>3D Vision</td><td>non-pixel-aligned feed-forward Gaussian에 anchor와 triplane geometry prior를 넣어 큰 시점 변화에서 이점을 보이나 DTU와 NRGBD 평가에 그쳤음</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2610.37019'>V-LUMEN: Visual Lookup Memory for Embedding Scaling in Vision-Language Models</a></td><td>42</td><td>2</td><td>Multimodal</td><td>VLM에 비파라미터 visual lookup memory를 붙여 용량 축을 분리함, 추론 벤치마크 중심이며 로봇 검증 없음</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2610.36308'>When Retrieval Is Not Enough: Obsolete Facts in Agent Memory</a></td><td>42</td><td>2</td><td>NLP</td><td>agent memory에서 폐기된 사실 처리 benchmark임. memory 평가 관점이나 텍스트 한정임</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2610.36484'>CogArena: Benchmarking Multimodal Agents on Interactive Behavioral Experiments</a></td><td>42</td><td>2</td><td>Multimodal</td><td>multimodal agent 행동실험 benchmark임. 인지 평가 위주임</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2610.36570'>CASEL: Consequence-Aware Selective Execution for Reliable Long-Horizon Tool-Using Agents</a></td><td>42</td><td>2</td><td>AI</td><td>결과 인지형 선택적 실행으로 tool agent 신뢰성 높임. 로봇 검증 없음</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2610.36652'>Remembering Is Not Enough: Refining Memories and Learning When to Use Them in Multi-Agent Systems</a></td><td>42</td><td>2</td><td>AI</td><td>multi-agent memory 정제와 사용 시점 학습임. 텍스트 agent 한정임</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2610.36793'>Visual Autoregressive Generation with Next Token Imagination</a></td><td>42</td><td>1</td><td>Generative</td><td>AR 생성에서 GT 다음 토큰 밖을 탐색하는 NTI를 제안했으나 ImageNet 생성 fidelity 개선에 국한됨</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2610.36477'>Proposing Better Rollouts for On-Policy Distillation</a></td><td>42</td><td>1</td><td>NLP</td><td>on-policy distillation의 rollout policy를 student와 teacher의 mixture로 설계함, 16개 벤치마크에서 이득이나 LLM 한정임</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2610.36794'>Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training</a></td><td>42</td><td>1</td><td>NLP</td><td>In-Place TTT의 fast weight 쓰기 강도를 query 관련도로 조절함, long-context QA 한정이며 test-time 학습 관점은 흥미로운 시도임</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2610.37041'>Guided-RLVR: Guided Exploration in Reinforcement Learning with Verifiable Rewards</a></td><td>42</td><td>1</td><td>RL</td><td>RLVR에 guided exploration 도입함. LLM 추론 한정임</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2610.37626'>Know, then Draw: A New Learning Paradigm for Visual Generation</a></td><td>42</td><td>0</td><td>Generative</td><td>AR 사전학습과 diffusion 후학습으로 나누는 생성 paradigm과 scaling law 분석이 체계적이나 T2I 한정임</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2610.36725'>On Shaky Ground: Characterising Non-Rigid Base Effects in Mobile Manipulation</a></td><td>40</td><td>6</td><td>Mobile Manipulation</td><td>경량 모바일 manipulator의 base 비강성 효과를 sanding 사례로 측정한 특성 분석이며 학습 기여는 없음</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2610.37217'>KEPT: Conformal Keepouts Kept in Planning for Enclosed-Space Navigation in Degraded Sensing</a></td><td>40</td><td>6</td><td>Navigation</td><td>저하된 센서에서 conformal keepout 마진을 severity별로 조건화했으나 시뮬레이션과 녹화 데이터 중심임</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2610.36143'>Program-Level Adversarial Co-Adaptive Self-Play for Robotic Security</a></td><td>40</td><td>5</td><td>Robot Security</td><td>coding agent가 공격과 방어 프로그램을 공진화시키는 사례 연구로 한계를 인정했고 증거가 약함</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2610.36599'>Camera-to-Quadruped Robot Pose Estimation from Sequential Images</a></td><td>40</td><td>5</td><td>CV</td><td>외부 카메라 영상으로 quadruped 18-DoF 자세를 추정하는 모델과 합성 benchmark이며 실로봇 학습과는 거리가 있음</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2610.37350'>Generalizable Target-Less Joint Intrinsic-Extrinsic Camera-LiDAR Calibration using Deep Pixel-Point Correspondences</a></td><td>40</td><td>5</td><td>3D Vision</td><td>camera-LiDAR 내부와 외부 파라미터를 함께 구하는 target-less 보정으로 실용적이나 perception 보정 영역임</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2610.36625'>Polarity--Time Interaction and Multi-Level Reliability for Event-Based Spacecraft Pose Estimation</a></td><td>40</td><td>4</td><td>3D Vision</td><td>event camera 기반 위성 pose 추정임. 기하 신뢰도 활용이나 우주 응용임</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2610.36168'>PrinGS: Privacy Preservation in Gaussian Splatting</a></td><td>40</td><td>3</td><td>3D Vision</td><td>학습된 3DGS에서 민감 영역을 1초 내 익명화하는 문제 설정은 새롭지만 로봇 학습과 거리가 멀고 평가가 얼굴/OCR 지표에 한정됨</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2610.37149'>GCSR-OCC: Geometry Calibration and Semantic Routing for Open-Vocabulary Occupancy Prediction</a></td><td>40</td><td>3</td><td>3D Vision</td><td>Gaussian에서 voxel occupancy로 바꿀 때 scale inflation과 의미 혼합을 보정한 open-vocabulary occupancy로 실내 장면 이해에 쓸 만하나 모듈 개선 수준임</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2610.37202'>3D-SceneQ: Empowering 3D LLM With Query-Guided Adaptive Pruning and Multi-Modal Feature Enhancement</a></td><td>40</td><td>3</td><td>3D Vision</td><td>3D LLM에서 query 기반 object token pruning과 2D feature 보강을 넣어 Scan2Cap과 SQA3D 점수를 올린 모듈 추가 수준임</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2610.36824'>Who Knows What - and What Does It Support? Perspective-Bounded Evidence Calibration for Multimodal Theory of Mind</a></td><td>40</td><td>3</td><td>Multimodal</td><td>멀티모달 Theory of Mind 증거 보정임. 로봇 HRI와 약한 연결임</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2610.36986'>LearnPrunerV2: Learnable Progressive Token Pruning for Vision-Language Models</a></td><td>40</td><td>2</td><td>Multimodal</td><td>층마다 학습형 모듈로 visual token을 77.8% 줄이면서 성능 99.8%를 유지하나 token pruning 계열의 incremental 개선임</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2610.36469'>CoHARL: Co-Evolving Agent Policies and Executable Harnesses with Reinforcement Learning</a></td><td>40</td><td>2</td><td>RL</td><td>LLM agent policy와 harness 코드를 함께 진화시키는 RL이며 SWE 과제 한정임</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2610.36449'>A Heart Means Recursion: Exploring Visual Meaning and Communication in VLMs</a></td><td>40</td><td>2</td><td>Multimodal</td><td>VLM의 시각적 의미 소통 능력 예비 분석임. 로봇 연결 약함</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2610.37482'>From Interaction to Capability: Task Advancement as State and Supervision for GUI Agents</a></td><td>40</td><td>2</td><td>AI</td><td>GUI agent의 과제 진행 상태 memory와 supervision임. 로봇 아닌 GUI 한정임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2610.36466'>Nemotron-Labs-Diffusion-Uni: Elastic Self-Refining Unified Diffusion LLM with Cross-Paradigm On-Policy Distillation</a></td><td>40</td><td>1</td><td>Multimodal</td><td>통합 diffusion LLM에 on-policy distillation과 progressive self-refine을 적용했으나 이미지 이해와 생성 벤치마크 중심임</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2610.36593'>WithinVAE: Compact Visual Autoencoding with Self-Distilled Semantics</a></td><td>40</td><td>1</td><td>Representation</td><td>외부 인코더 없이 자기 증류로 compact autoencoder에 의미 구조를 학습시키는 표현 학습이나 ImageNet 재구성 지표 중심임</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2610.37341'>CodeCap-Bench: Can Code Serve as a Good Video Caption?</a></td><td>40</td><td>1</td><td>Video</td><td>코드를 비디오 caption으로 쓰는 발상이 새로우나 구조화된 2D 콘텐츠에 한정된 벤치마크임</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2610.36849'>When All Rollouts Fail: Policy-Compatible Joint Decoding for Hard-Problem Reasoning</a></td><td>40</td><td>1</td><td>NLP</td><td>모든 rollout이 실패하는 어려운 문제에서 expert 정보를 policy 호환 decoding으로 주입하는 RLVR임</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2610.37553'>Collective Dynamics of Self-Reinforcement: How Cross-Task Coupling Drives Policy Collapse in Unsupervised RLVR</a></td><td>40</td><td>0</td><td>RL</td><td>label-free RLVR의 policy collapse가 문제 수와 공유 결합으로 생김을 이론으로 설명함</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2610.36454'>SVIn+: Multi-Modal Framework for Robust Underwater State Estimation using 3D Sonar, Visual-Inertial, Water-Pressure, and DVL</a></td><td>38</td><td>5</td><td>State Estimation</td><td>수중 AUV용 sonar와 VIO와 DVL 융합 SLAM으로 현장 검증은 있으나 전통 센서 융합의 확장임</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2610.37602'>RESPLE2: Inertial-Informed Recursive Non-Uniform Spline Estimation for Multi-Sensor Odometry with Global Refinement</a></td><td>38</td><td>5</td><td>State Estimation</td><td>B-spline 기반 recursive multi-sensor odometry로 여러 플랫폼 평가를 했으나 고전 상태 추정의 개선임</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2610.37218'>TopoField: Technical Report for ECCV 2026 SceneFun3D Challenge</a></td><td>38</td><td>4</td><td>3D Vision</td><td>SceneFun3D 기능 부품 분할에서 확률장을 인스턴스로 디코딩하는 deterministic decoder이며 챌린지 2위 기록으로 일반화 근거는 약함</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2610.36610'>4D Reconstruction with Events &amp; RGB</a></td><td>38</td><td>3</td><td>3D Vision</td><td>Monst3R에 event 입력 가지를 단순 추가해 Abs Rel을 3.4% 낮춘 예비 연구로 개선이 작고 증거가 얇음</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2610.36203'>UT-HMR: Uncertainty-Guided Temporal Modeling for Robust 3D Human Mesh Recovery</a></td><td>38</td><td>2</td><td>CV</td><td>low-rank 공분산 기반 불확실성과 시간 융합으로 HMR을 개선했으나 스포츠 데이터 위주 incremental 개선임</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2610.37036'>GraftRay: Physically Based Mesh Insertion into Gaussian Splatting Scenes via Path Tracing</a></td><td>38</td><td>2</td><td>3D Vision</td><td>3DGS 장면에 mesh를 path tracing으로 물리 기반 삽입하는 렌더링 기법이며 합성 데이터 용도 외 로봇 연결은 약함</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2610.37545'>GroundControl: Satellite-Conditioned Multi-View Diffusion for Reconstruction-Free Novel View Synthesis</a></td><td>38</td><td>2</td><td>3D Vision</td><td>위성 영상을 조건으로 multi-view diffusion의 장면 외삽 환각을 줄이나 reconstruction 없는 생성 방식이고 로봇 연결은 약함</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2610.37430'>When Visual Evidence Is Insufficient: How Instructions, Post-Training, and Internal Activations Shape Refusal in Multimodal Language Models</a></td><td>38</td><td>2</td><td>Multimodal</td><td>MLLM이 시각 증거 부족 시 거절하는 양상을 지시·post-training·activation 개입으로 분석함</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2610.37609'>EnvSched: Environment-Aware Scheduling for Rollout-Efficient Agent Reinforcement Learning</a></td><td>38</td><td>2</td><td>RL</td><td>agentic RL의 환경 단위 task 스케줄링으로 rollout 효율을 높임, 언어 agent 벤치마크 한정임</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2610.36967'>Proactive Memory for Event-Driven LLM Agents</a></td><td>38</td><td>2</td><td>AI</td><td>event 기반 proactive agent memory임. 텍스트 agent 한정임</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2610.36192'>Beyond the Estimate: Wiener-Informed Decoding for Easier Training of Pixel-Space Flow Models</a></td><td>38</td><td>1</td><td>Generative</td><td>Wiener 통계로 pixel-space flow 학습을 가속하는 생성 모델 기법이며 ImageNet 수치 중심이고 로봇 관련성 없음</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2610.36545'>FrameForge: Harnessing Priors of Video Foundation Models for Unified Image Generation</a></td><td>38</td><td>1</td><td>Generative</td><td>비디오 모델의 시간 위치를 입력 적응형으로 바꿔 통합 이미지 생성을 개선했으나 로봇과 거리가 멀고 benchmark 개선 위주임</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2610.36809'>Latent Visual Contrastive Reasoning with Multi-Branch Exploration</a></td><td>38</td><td>1</td><td>Multimodal</td><td>latent visual 가지를 contrastive로 정렬하는 추론 기법이며 backbone 대비 개선이 평범함</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2610.36109'>Beyond Update Counts: A Control Map for Evaluating Test-Time Model Updates</a></td><td>38</td><td>1</td><td>NLP</td><td>test-time 모델 업데이트의 이력을 기록해 acquisition·retention·locality를 따로 평가하는 틀이며 LLM 편집 범위에 한정됨</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2610.36870'>Tail Cues, Principal Corrections: Plug-and-Play Rectification for Open-Set Test-Time Adaptation</a></td><td>38</td><td>1</td><td>CV</td><td>open-set test-time adaptation용 backward-free 보정 모듈이며 ImageNet-C 개선 중심임</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2610.37642'>Metacognitive Decoding: Efficient Inference for Diffusion Language Agents</a></td><td>38</td><td>1</td><td>NLP</td><td>diffusion LM agent 효율 추론 디코딩임. 로봇 연결 약함</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2610.37422'>Beyond the Readout: A Latent Numerical Frame Shared Across Modality and Operation</a></td><td>38</td><td>1</td><td>Multimodal</td><td>텍스트·이미지 수치 연산이 공유하는 latent frame 분석임. 해석 연구임</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2610.36874'>AdaGround: Token-Normalized Adaptive Zooming with Verifier-in-the-Loop Refinement for GUI Grounding</a></td><td>38</td><td>0</td><td>Multimodal</td><td>GUI grounding용 training-free 적응 zoom과 verifier로 7~20점 올렸으나 GUI 특화 pipeline임</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2610.37110'>A First-Step Bias Restores Lost Diversity in Diffusion Model Distillation</a></td><td>38</td><td>0</td><td>Generative</td><td>증류 모델의 첫 denoising step만 보정해 다양성을 회복하는 가벼운 adapter이며 로봇과 무관함</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2610.36202'>Base Models Can Detect Hidden Intentions that Prompted Classifiers Miss</a></td><td>38</td><td>0</td><td>NLP</td><td>base model likelihood로 숨은 의도를 읽는 감사 방법이 흥미로우나 LLM 안전 영역임</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2610.36847'>Conservative Policy Iteration For Zero-Sum POSGs</a></td><td>36</td><td>2</td><td>RL</td><td>zero-sum POSG용 conservative policy iteration임. 이론 위주이고 로봇 연결 약함</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2610.37658'>When Should We Intervene at Test Time?</a></td><td>36</td><td>1</td><td>LG</td><td>test-time adaptation 개입 시점과 label 질의를 정하는 controller를 제안했으나 이미지 분류 중심임</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2610.36146'>From Structural Feedback to Prompt Policies: Learning Faithful Text-to-Image Prompt Editors</a></td><td>36</td><td>1</td><td>Generative</td><td>T2I prompt 편집기를 구조적 피드백으로 학습함. 로봇 연결 약함</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2610.37645'>Multi-State Linear Attention with Generalized Second-Order Routing</a></td><td>36</td><td>0</td><td>NLP</td><td>linear attention 변형임. 일반 효율 아키텍처로 로봇 연결 약함</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2610.36445'>From Solver Trajectories to Teaching Trajectories: Cognition-Aligned Reasoning Distillation</a></td><td>36</td><td>0</td><td>NLP</td><td>reasoning distillation 궤적 재구성임. 로봇과 무관함</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2610.37127'>MCP-Net: Real-Time Coronary Perception Network and Topological Analysis for Robotic Guidewire Navigation</a></td><td>35</td><td>4</td><td>Embodied AI</td><td>시뮬레이션 형광투시에서 혈관 분할과 guidewire 위치로 roadmap을 만드는 perception 파이프라인이나 실제 제어와 실환경 검증이 없음</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2610.36450'>Ground Sample Distance Constrained k-Coverage Viewpoint Planning via Set Multi-Cover Formulation</a></td><td>35</td><td>4</td><td>Active Perception</td><td>GSD 제약 k-coverage viewpoint를 set multi-cover로 정식화했으나 greedy 휴리스틱 수준임</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2610.36658'>SAGE: Semantic-Augmented Geometric Experts for Point Cloud Registration</a></td><td>35</td><td>3</td><td>3D Vision</td><td>고정된 semantic 표현을 MoE routing에 넣어 저중첩 point cloud 정합을 개선한 모듈 추가 수준임</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2610.36075'>Jaxnasium: Embracing PyTrees For Any-Agent, Cross-Suite Reinforcement Learning</a></td><td>35</td><td>3</td><td>RL</td><td>JAX RL을 PyTrees 기반으로 여러 suite와 multi-agent에 통합하는 라이브러리로 연구 편의 도구이며 방법론 기여는 없음</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2610.36327'>Training-Free Inference Acceleration for Video Large Language Models: Methods, Trade-offs, and Evaluation</a></td><td>35</td><td>2</td><td>Video</td><td>Video LLM의 training-free 추론 가속 기법을 정리한 survey로 새 방법론은 없고 효율 추론 참고 자료 수준임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2610.36183'>Learning Human Sports Motion Feasibility via Quantile Regression on Tracking Data</a></td><td>35</td><td>2</td><td>LG</td><td>스포츠 선수 도달 시간 quantile regression임. 로봇 연결 약함</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2610.36838'>MVRCap: Towards Comprehensive Video Captioning via Hierarchical Multi-Dimensional Verifiable Rewards</a></td><td>35</td><td>1</td><td>Video</td><td>검증 가능한 보상으로 비디오 캡션을 RL 학습했으나 caption benchmark 점수 개선 위주임</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2610.37579'>As the Story Unfolds: Watching a Film and Identifying Characters as a Human Does</a></td><td>35</td><td>1</td><td>Video</td><td>영화에서 등장인물 이름을 점진적으로 식별하는 새 과제이나 로봇과 거리가 멀음</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2610.37523'>The Structure Gap: When More Data Cannot Replace Structured Reasoning</a></td><td>35</td><td>1</td><td>LG</td><td>구조가 정해진 문제에서 데이터만으로는 구조 정보를 대체하기 어려움을 이론과 소규모 실험으로 보임</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2610.36826'>When the Critic Falls Behind: Co-Evolving Rubrics and Harnesses for Continual Agent Self-Improvement</a></td><td>35</td><td>1</td><td>AI</td><td>rubric과 harness 공진화 agent 자기개선임. 로봇 연결 약함</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2610.36587'>Efficient Quantization Training with Stochastic Rounding via Structured Subspace Randomness</a></td><td>35</td><td>0</td><td>LG</td><td>stochastic rounding 난수 비용을 줄여 INT8 학습을 가속함, LLM 효율 학습 기여임</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2610.36617'>Balanced State Subspaces with Spectral Rank Allocation for Mamba-2 State Compression</a></td><td>35</td><td>0</td><td>NLP</td><td>Mamba-2 상태를 balanced truncation으로 압축하는 방법이며 효율 추론 기여임</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2610.36807'>SetGRPO: Calibrating Grader-Induced Policy Optimization</a></td><td>35</td><td>0</td><td>NLP</td><td>rubric 기반 GRPO의 grader 노이즈를 set-valued 보정으로 다룸, LLM 한정임</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2610.36950'>DCKV: Learned Transform Coding of the Prompt KV Cache in Hybrid Language Models</a></td><td>35</td><td>0</td><td>NLP</td><td>hybrid LM의 prompt KV cache를 end-to-end 학습 codec으로 압축함, 효율 추론 기여임</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2610.37115'>Self-Regularized Flow Language Models</a></td><td>35</td><td>0</td><td>NLP</td><td>continuous flow LM의 noisy-to-clean self-distillation으로 학습 가속함</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2610.37390'>LinMix: Data Mixing as Linear Domain Attribution</a></td><td>35</td><td>0</td><td>NLP</td><td>data mixing을 선형 domain attribution으로 보고 vertex sampling을 제안함, 설계 근거는 탄탄하나 LLM 한정임</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2610.36918'>TrawMem: Reframing Agent Memory as Task-Oriented Role-Adaptive Workspaces</a></td><td>34</td><td>1</td><td>NLP</td><td>agent memory를 task 역할별 workspace로 재구성했으나 대화 QA 평가이며 robot memory와 거리가 있음</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2610.37651'>GEPA-Curator: Curated Learning for Self Improving Agents</a></td><td>34</td><td>1</td><td>NLP</td><td>agent 자기개선용 학습 데이터 큐레이션임. incremental임</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2610.36980'>AutoVend: Benchmarking LLM Agents on Long-Horizon Autonomous Vending Operations</a></td><td>34</td><td>1</td><td>AI</td><td>자판기 운영 장기 과제 LLM benchmark임. long-horizon이나 로봇 아님</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2610.36444'>RouteDRAG: Learning to Route and Control Agentic Execution for Multimodal Document RAG</a></td><td>34</td><td>0</td><td>Multimodal</td><td>멀티모달 문서 RAG routing임. 로봇과 무관함</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2610.37375'>Agent-Conditioned Routing: Diverse Reasoning Paths Within One Frozen Model</a></td><td>34</td><td>0</td><td>NLP</td><td>단일 frozen model 내 다양한 추론 경로 routing임. 로봇과 무관함</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2610.36139'>SpatialPC: Deep Computation with Sublinear Local Credit Propagation</a></td><td>33</td><td>1</td><td>LG</td><td>local learning의 credit 전파 지연을 기하로 분석한 이론 결과이나 MNIST 수준 검증임</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2610.36994'>CaLLM: Continual Adaptation of LLMs via Non-Parametric Adapter Routing</a></td><td>33</td><td>1</td><td>NLP</td><td>prototype 기반 adapter 라우팅으로 LLM continual adaptation을 함, 벤치마크 비교 위주임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2610.37429'>Bayes-Adaptive MDPs for Rollout Allocation to Enhance GRPO Training</a></td><td>33</td><td>1</td><td>RL</td><td>GRPO의 rollout 예산을 난이도별로 Bayes-adaptive MDP로 배분함, LLM 한정임</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2610.36778'>Does LLM Pre-Training Typically Occur at the Edge of Stability?</a></td><td>33</td><td>0</td><td>LG</td><td>LLM pretraining에서 Edge of Stability와 Edge of Convexity를 분석한 최적화 이론 연구임</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2610.36901'>HiLo-RD: Cross-Budget Self-Distillation for Masked Diffusion Language Models</a></td><td>33</td><td>0</td><td>NLP</td><td>masked diffusion LM의 큰 window 궤적을 작은 window로 증류함</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2610.36940'>TDLM: Adaptive Temporal Integration for Diffusion Language Models</a></td><td>33</td><td>0</td><td>NLP</td><td>diffusion LM에 hidden state 시간 이력 attention을 더해 생성 속도를 높임</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2610.36983'>Advancement or Acceleration? How Data Curation Improves LLM Training</a></td><td>33</td><td>0</td><td>NLP</td><td>data curation이 advancement인지 acceleration인지 구분하는 Δ-test 제안, LLM 데이터 한정임</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2610.37062'>EnergyCal: Taming Loss Spikes in Muon-Family Optimizers for Sparse MoE Training</a></td><td>33</td><td>0</td><td>NLP</td><td>Muon 계열 optimizer의 MoE loss spike를 줄이는 경량 규칙임</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2610.37085'>On the Sparsity of Direct Preference Optimization: Weight Disentanglement in the NTK Regime</a></td><td>33</td><td>0</td><td>NLP</td><td>DPO 업데이트의 희소성을 NTK 관점에서 설명하는 이론임</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2610.37126'>Mechanistic Failure Modes of Weight Pruning in Transformer Language Models</a></td><td>33</td><td>0</td><td>NLP</td><td>pruning이 IOI circuit을 어떻게 망가뜨리는지 보인 GPT-2 분석임</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2610.37386'>Channel Selection for Mixture-of-Experts Decoding Needs No Calibration Data</a></td><td>33</td><td>0</td><td>NLP</td><td>MoE decoding의 channel 선택에 calibration이 필요 없음을 보이고 커널을 구현함, 효율 추론 엔지니어링임</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2610.37481'>Follow the Gradient: Tracing Safety Degradation Back to Training Data</a></td><td>33</td><td>0</td><td>NLP</td><td>gradient 임베딩으로 안전성을 깎는 fine-tuning 데이터를 추적하고 필터링함</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2610.37517'>Orthogonal and Parametrized Multi-Attribute Steering of LLMs</a></td><td>33</td><td>0</td><td>NLP</td><td>LLM activation steering의 직교화와 강도 매개화 방법임</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2610.37443'>ETAMem: Decoupling and Aligning Heterogeneous Memory for Long-Term Conversational Agents</a></td><td>32</td><td>1</td><td>NLP</td><td>대화 에이전트용 이질적 memory 분리·정렬임. robot memory와 거리 있음</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2610.36509'>ARISE: Authentic Reference-Informed Stability Enhancement for Continual Multimodal Forgery Detection</a></td><td>32</td><td>0</td><td>Multimodal</td><td>attack-incremental continual 위조 검출 설정과 replay 기법은 정리되었으나 로봇과 무관함</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2610.36858'>Forget the Data, Keep the Capability: Switchable Unlearning for Retrieval</a></td><td>32</td><td>0</td><td>CV</td><td>core와 parasitic 파라미터를 분리해 re-ID unlearning을 스위치로 처리하는 구조가 영리하나 로봇과 무관함</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2610.37566'>ReferStream: Interactive Subject Injection for Streaming Video Generation</a></td><td>32</td><td>0</td><td>Video</td><td>스트리밍 비디오 생성에 새 subject를 training-free로 주입하는 cache 기법임</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2610.36751'>Generative Refinement Learning for Temporal Interpolation in Scientific Machine Learning</a></td><td>32</td><td>0</td><td>LG</td><td>수치 보간 위에 residual을 diffusion으로 생성하는 과학 데이터 시간 보간임</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2610.36405'>kw-bench: Breaking Frontier Harnesses on Real-World Tasks</a></td><td>32</td><td>0</td><td>AI</td><td>frontier harness 실세계 과제 benchmark임. 로봇과 무관함</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2610.37369'>Uncovering Why LLMs Fail: From Internal Mechanisms to Adversarial Reasoning Trajectories</a></td><td>32</td><td>0</td><td>NLP</td><td>LLM 실패의 내부 메커니즘 분석임. 로봇과 무관함</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2610.37153'>FastBEVFusion: Simple Multi-Modal Fusion for 3D Object Detection at 50 FPS</a></td><td>30</td><td>3</td><td>CV</td><td>자율주행 LiDAR 카메라 BEV 융합을 50 FPS로 구동했으나 단순 구조의 속도 개선 위주임</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2610.36582'>Structured Maps for Landmark-Based Route Instructions with LLMs</a></td><td>30</td><td>2</td><td>NLP</td><td>지도 SVG 텍스트로 LLM이 landmark 기반 경로 안내를 하게 한 연구로 navigation 주변이나 실제 로봇은 없음</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2610.36195'>Learning to Read Braille: Benchmarking and Improving Braille Recognition Capabilities of VLMs</a></td><td>30</td><td>1</td><td>Multimodal</td><td>점자 인식 벤치마크와 합성 데이터 학습이 기여이며 접근성 과제 특화라 로봇 연관이 거의 없음</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2610.36506'>GarmentSegAgent: Autonomous Garment Segmentation for Web Fashion Images via Textual Self-Refinement</a></td><td>30</td><td>1</td><td>CV</td><td>TextGrad로 의류 분할 지시문을 개선하는 agent로 패션 도메인 특화임</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2610.36719'>SAGE: Saliency-Annealed Gated Encoder for Universal Vision Recognition</a></td><td>30</td><td>1</td><td>CV</td><td>ViT-Adapter 백본 개선과 학습 스케줄 조합으로 dense prediction 점수를 올린 engineering임</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2610.36655'>Log-Derivative Trick for Parametric Markov Chains</a></td><td>30</td><td>1</td><td>RL</td><td>parametric Markov chain에 log-derivative trick을 일반화한 불편 gradient 추정으로 이론 성격이 강함</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2610.37284'>Bayesian Inference of Expensive Simulators: Survey and Comparison of Design Choices</a></td><td>30</td><td>1</td><td>LG</td><td>비싼 simulator의 Bayesian 추론 설계 선택을 조사하고 proxy variable을 제안함</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2610.37656'>Attention as Lattice Gauge Theory: Relations Interact Only Through Wilson Loops</a></td><td>30</td><td>1</td><td>LG</td><td>attention을 gauge 대칭성으로 유도한 이론 흥미는 있으나 workshop 수준이고 로봇 연결 약함</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2610.36734'>CAMR: Compatibility-Aware Memory Replay for Continual Learning in Large Language Models</a></td><td>30</td><td>1</td><td>NLP</td><td>LLM continual learning의 replay 정책을 학습하는 방법으로 로봇 continual learning과 직접 연결은 약함</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2610.37161'>WorkFactory: Turning Professional Intents into Executable Work for Scalable Agent Training</a></td><td>30</td><td>1</td><td>AI</td><td>전문 업무 agent 학습 데이터 합성임. 로봇과 무관함</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2610.36460'>Full Collapse Is Suboptimal: Controlled Partial Neural Collapse for Long-Tailed Recognition</a></td><td>30</td><td>0</td><td>CV</td><td>long-tailed 인식용 partial neural collapse 설계로 분류 정확도 개선 수준임</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2610.36665'>Haste Makes Waste? Towards Safe Few-Step Text-to-Image Models</a></td><td>30</td><td>0</td><td>Generative</td><td>few-step T2I 모델의 안전성 저하를 분석하고 erasure를 제안했으나 로봇과 무관함</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2610.36082'>How Much Does the Hint Matter? Scope Conditions for Hindsight Self-Distillation in Financial Reasoning</a></td><td>30</td><td>0</td><td>NLP</td><td>금융 추론용 self-distillation 레시피이며 이득이 힌트 내용이 아니라 감독 위치에서 나옴을 보인 분석임, 로봇 연관 없음</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2610.36095'>Instruction Capacity: Behavior and Degradation of Language Models under Controlled Load</a></td><td>30</td><td>0</td><td>NLP</td><td>지시문 규칙 수에 따른 LLM 성능 저하를 측정하는 계측 도구이며 GPT-4o mini 한 모델 측정에 한정됨</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2610.36113'>Scaling and Renormalization in Neural Networks: An Effective Renormalization-Group Description of Grokking</a></td><td>30</td><td>0</td><td>LG</td><td>grokking을 재규격화군으로 기술한 이론 분석이며 modular addition 소규모 실험에 한정됨</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2610.36576'>Less is more: learning what to profile for GPU kernel optimization</a></td><td>30</td><td>0</td><td>LG</td><td>GPU kernel 최적화에서 무엇을 profile할지 학습하는 방법이며 KernelBench 한정임</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2610.36585'>Recall or Relearn? A Mixture of In-Context Experts for Recurring Concept Drift</a></td><td>30</td><td>0</td><td>LG</td><td>tabular foundation model의 recurring drift 대응이며 이론은 있으나 로봇 연관 없음</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2610.36618'>Dream-COP: Guiding Algorithm Discovery for Combinatorial Optimization Problems in an Experience World</a></td><td>30</td><td>0</td><td>LG</td><td>LLM 알고리즘 탐색을 experience world replay로 안내함, 조합 최적화 한정임</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2610.36640'>When Does Perturbation Consistency Add Information Beyond Softmax Confidence? Theory and Evidence for the Decision Consistency Framework</a></td><td>30</td><td>0</td><td>CV</td><td>perturbation consistency가 softmax confidence보다 나은 조건을 분석함, 대부분 negative 결과임</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2610.36718'>Nonlinear Direct Feedback Alignment for Scalable Backpropagation-Free Training</a></td><td>30</td><td>0</td><td>LG</td><td>direct feedback alignment에 비선형 surrogate를 더한 BP-free 학습이며 이미지 분류 한정임</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2610.37001'>Meta Models: Models that Model Learning</a></td><td>30</td><td>0</td><td>LG</td><td>학습 곡선을 예측하는 meta-model에 TabPFN을 쓰는 실증이며 human-scale 새 formulation은 약함</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2610.37058'>Exploring the Limits of the Delta Learning Hypothesis: Single-Pair Generator Biases in Direct Preference Optimization</a></td><td>30</td><td>0</td><td>NLP</td><td>단일 모델 쌍 DPO 데이터의 generator 편향을 분석함</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2610.37225'>Sharpness-Aware Muon: Matrix-Aware Optimization with Momentum-Guided Perturbations</a></td><td>30</td><td>0</td><td>LG</td><td>Muon에 sharpness-aware 항을 더한 optimizer 변형임</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2610.37336'>CoS-VQ: Coordinated Shared-Scale Vector Quantization for Large Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 가중치 vector quantization의 joint index-scale 갱신이며 효율 기여임</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2610.37719'>What a Weight Update Buys: Leverage Across Training Stages</a></td><td>30</td><td>0</td><td>NLP</td><td>post-training 가중치 변화의 leverage 측정 분석으로 흥미롭지만 로봇과 무관함</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2610.36511'>Do AI Scientists Know What&#x27;s New?</a></td><td>30</td><td>0</td><td>NLP</td><td>AI scientist의 novelty 검사 평가와 claim 단위 모듈이며 로봇과 무관함</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2610.36709'>Is Token Confidence Just Chain Length? A Signal-Processing Audit of Reasoning Traces</a></td><td>30</td><td>0</td><td>NLP</td><td>token confidence가 chain 길이를 반영할 뿐임을 신호 처리로 보인 비판적 분석이며 로봇과 무관함</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2610.36169'>Don&#x27;t Pick a Winner: Knowledge Conflicts Need a Prior, Not a Rule</a></td><td>30</td><td>0</td><td>NLP</td><td>지식 충돌 처리에 prior 필요성 논함. 로봇과 무관함</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2610.36188'>Skill Dreaming: Evolving Repository Skills through Pull Request Streams</a></td><td>30</td><td>0</td><td>NLP</td><td>PR 스트림으로 repo skill 진화시키는 SW agent임. 로봇과 무관함</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2610.36435'>Your Agent Acts Differently When You&#x27;re Around: How User Presence Changes Agent Behavior in Negotiation</a></td><td>30</td><td>0</td><td>AI</td><td>사용자 존재가 negotiation agent 행동에 미치는 영향 분석임. 로봇과 무관함</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2610.36595'>Learning to Formalize: Bridging Open-Ended Workloads and Fast Decision Models</a></td><td>30</td><td>0</td><td>AI</td><td>개방형 과제를 빠른 결정 모델로 공식화함. 로봇과 무관함</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2610.37121'>Prospector: learning a compact graph traversal policy for scientific reasoning</a></td><td>30</td><td>0</td><td>AI</td><td>과학 추론용 그래프 탐색 policy임. 로봇과 무관함</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2610.37201'>Does Your Generalist Skill Optimizer Really Incentivize Agentic Tasks? Rethinking Skill Optimization via Bipartite Attribution</a></td><td>30</td><td>0</td><td>AI</td><td>skill optimizer 평가 재고임. 로봇과 무관함</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2610.37571'>TeamGym: A Gym for Team Decision-Making by AI Agents with Distributed Information</a></td><td>30</td><td>0</td><td>AI</td><td>분산 정보 팀 의사결정 gym임. 로봇과 무관함</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2610.37585'>Timestral</a></td><td>30</td><td>0</td><td>LG</td><td>시계열 foundation model Timestral임. 로봇과 무관함</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2610.37043'>State estimation for a hybrid rigid-continuum space manipulator system</a></td><td>28</td><td>4</td><td>State Estimation</td><td>hybrid rigid-continuum 우주 manipulator의 factor graph 상태 추정으로 시뮬레이션 검증뿐임</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2610.37199'>A Bi-level Co-design Framework for Lunar Monoped with 2D Jump and Landing Control</a></td><td>28</td><td>4</td><td>Control</td><td>달 환경 monoped 형태와 제어 bi-level co-design으로 시뮬레이션 중심임</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2610.37519'>Leveraging Distributed Sensing and Hyperdimensional Computing for Non-Line-of-Sight Passive Object Sensing</a></td><td>28</td><td>4</td><td>Perception</td><td>무선 channel 측정과 hyperdimensional computing으로 시야 밖 물체를 분류하는 ISAC 연구로 시뮬레이션 중심임</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2610.37403'>AuRaSim: A Ray-Tracing Based Automotive FMCW Radar Simulator for Dynamic Scenarios</a></td><td>28</td><td>3</td><td>Simulation</td><td>자동차 FMCW radar ray-tracing 시뮬레이터로 도구 성격이며 로봇 학습과 거리가 있음</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2610.36337'>CRLoMTL: Conflict-Resolution through Low-rank matrices for Multi-Task Learning</a></td><td>28</td><td>1</td><td>CV</td><td>LoRA 공간에서 SVD로 task 충돌을 푸는 multi-task 학습이며 소폭 개선의 incremental 기법임</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2610.36832'>Drop the Details, Get the Gist: Dynamic Conceptual Representation for Video Recognition</a></td><td>28</td><td>1</td><td>Video</td><td>segment 단위 concept score 시퀀스로 절차 영상을 분류하는 작은 확장이며 평가가 좁음</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2610.37321'>Hierarchical Sparse Graph for Multi-dimensional Assignment in Event-based Tracking</a></td><td>28</td><td>1</td><td>CV</td><td>event 기반 tracklet 연관을 fuzzy graph partition으로 푸는 training-free 기법이며 추적 벤치마크 한정임</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2610.36708'>Conservative Dueling Bandits: Preference Learning under Baseline Constraints</a></td><td>28</td><td>1</td><td>LG</td><td>baseline 제약이 있는 conservative dueling bandit 이론이며 preference learning과 간접 연결됨</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2610.37145'>Beyond Parameter Protection: Fisher-Shaped EWC for Replay-Free Continual Learning</a></td><td>28</td><td>1</td><td>LG</td><td>EWC에 Fisher 민감도 제어를 더한 연속학습 개선이며 incremental임</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2610.37442'>CRISP: Co-designing Pruning and Scheduling for Efficient MoE Inference on Edge Servers</a></td><td>28</td><td>1</td><td>NLP</td><td>엣지 MoE 추론을 위한 pruning과 scheduling 공동 설계이며 시스템 엔지니어링임</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2610.37648'>Scaling Laws for Tool-Use Agents via Controllable Environment Synthesis</a></td><td>28</td><td>1</td><td>NLP</td><td>tool-use agent 학습 데이터 구성의 scaling law를 보인 연구로 로봇과 거리가 멂</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2610.36523'>Benchmarking Task Takeover Across Agent Handoffs</a></td><td>28</td><td>1</td><td>NLP</td><td>agent 간 task handoff 연속성 benchmark로 로봇과 거리가 멂</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2610.36948'>Self-Keyed In-Parameter Memorization for External Memory-Free Dialogue Recall in Frozen Language Models</a></td><td>28</td><td>1</td><td>NLP</td><td>대화를 모델 파라미터에 쓰는 in-parameter memorization이며 흥미로운 memory 발상이나 로봇과 거리가 멂</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2610.36536'>ATEMPO: Amortized Transfer Entropy Model Per-lag Over-Time</a></td><td>28</td><td>1</td><td>LG</td><td>시계열 transfer entropy 지연별 모델임. 로봇 연결 약함</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2610.36456'>LociArt: A Unified Paradigm for Free-Style Local Video Stylization</a></td><td>28</td><td>0</td><td>Video</td><td>국소 비디오 스타일화용 마스크 조건과 데이터셋 구축이며 로봇과 무관함</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2610.37576'>The Noise Plane: A Diffusion Bridge Across Exponent and Dispersion</a></td><td>28</td><td>0</td><td>Generative</td><td>Tweedie 노이즈 계열을 통합한 diffusion bridge로 센서 노이즈 복원 응용임</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2611.09960'>SceneShifter: Training-free Multi-Scene Temporal Control for Audio-driven Human Animation</a></td><td>28</td><td>0</td><td>Video</td><td>오디오 기반 인물 애니메이션의 장면 전환을 attention 조절로 제어하는 training-free 기법임</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2610.36255'>What Should an Information Bottleneck Encoder Learn? Separating Representation Learning from Rate Control</a></td><td>28</td><td>0</td><td>LG</td><td>information bottleneck에서 representation과 rate control을 분리하는 이론이며 소규모 이미지 실험임</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2610.36412'>Persistence, Exposure, and Credit Routing in Linear Temporal Predictive Coding</a></td><td>28</td><td>0</td><td>LG</td><td>선형 temporal predictive coding의 credit 이론 분석이며 워크숍 수준임</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2610.36520'>Folding Attention Biases into Keys Makes Compacted KV Caches Run on Standard Kernels</a></td><td>28</td><td>0</td><td>NLP</td><td>compacted KV cache의 bias를 key에 접어 표준 커널에서 돌리는 엔지니어링임</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2610.36553'>NextEval: An Agent-Based Solver and Benchmark for Derivative-Free Optimization</a></td><td>28</td><td>0</td><td>LG</td><td>LLM agent 기반 derivative-free optimization solver이며 저차원 문제만 다룬 연구임</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2610.36755'>Robust LLM Data Selection via Content-Invariant Gradient Attribution</a></td><td>28</td><td>0</td><td>NLP</td><td>instruction 데이터 선택용 gradient attribution의 표면 형식 편향 보정임</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2610.37276'>Where Should the Evaluation Budget Go in LLM-Driven Agent Scaffold Evolution?</a></td><td>28</td><td>0</td><td>NLP</td><td>agent scaffold 진화의 평가 예산 배분 방법임</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2610.37524'>GTFormer: A Syntax-Free Graph Network Alternative to Transformers for 8192$\times$ Length Extrapolation in Linear Time</a></td><td>28</td><td>0</td><td>LG</td><td>계층 그래프 네트워크로 Transformer를 대체해 선형 시간 외삽을 주장함, 평가 범위가 좁음</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2610.36353'>Detect Before You Disambiguate: Perturbation-Based Input Ambiguity Detection in LLMs</a></td><td>28</td><td>0</td><td>NLP</td><td>perturbation으로 입력 모호성을 탐지하는 LLM 방법이나 로봇과 무관함</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2610.36437'>CONCUR: Concordant Auxiliary Rewards for Multi-Task, Multi-Reward Reinforcement Learning</a></td><td>28</td><td>0</td><td>NLP</td><td>multi-reward RL advantage 추정을 조정하는 LLM 학습 기법으로 로봇과 무관함</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2610.36524'>Causal Localization of Evidence Effects in Transformers</a></td><td>28</td><td>0</td><td>NLP</td><td>symbolic 입력으로 증거 집계 attention head를 인과적으로 찾는 interpretability 연구임</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2610.36811'>Weakness Localization Is Not Enough: State-Aware Recursive Knowledge Improvement for Large Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>knowledge-state에 따라 개입을 고르는 LLM 지식 개선 틀로 로봇과 무관함</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2610.36328'>How Stable Are LLM-Generated Proofs Under Program Refactoring? A Stress Test for Verifiable Code Generation</a></td><td>28</td><td>0</td><td>NLP</td><td>리팩터링 후 LLM 증명 유효성 stress test임. 로봇과 무관함</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2610.36355'>WAKMan: Workload Aware KVCache Manager</a></td><td>28</td><td>0</td><td>LG</td><td>LLM 서버 KVCache 관리 시스템임. 로봇과 무관함</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2610.36386'>LoRA on a Budget: Function-Aware Post-Hoc Compression for Adapter Fleets</a></td><td>28</td><td>0</td><td>LG</td><td>LoRA adapter 사후 압축임. 일반 효율 기법임</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2610.36453'>Correction or Manipulation? Measuring Epistemic Vigilance in LLM Agents Under User Pressure</a></td><td>28</td><td>0</td><td>NLP</td><td>사용자 압박 아래 LLM agent의 epistemic vigilance 측정임. 로봇과 무관함</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2610.36660'>The View from Nowhere: Population-Centered Agent Evolution</a></td><td>28</td><td>0</td><td>AI</td><td>population 중심 agent 진화임. 로봇과 무관함</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2610.36672'>Learning Where to Trust: Reliability-Guided Expert Routing and Velocity Gating for 3D Deformable Registration</a></td><td>28</td><td>0</td><td>CV</td><td>3D 변형 정합용 expert routing임. 의료영상 incremental임</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2610.36767'>Can LLMs Reliably Grade Olympiad Proofs? A Study of Mathematical Verification with LLMs</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM의 올림피아드 증명 채점 신뢰성 연구임. 로봇과 무관함</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2610.36774'>Batching the Reflective Optimization Loop: Parallel Proposals Make GEPA Faster and Better</a></td><td>28</td><td>0</td><td>NLP</td><td>GEPA 반영 최적화 루프 배치화임. incremental임</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2610.36848'>Evolving Agent Teams</a></td><td>28</td><td>0</td><td>AI</td><td>GPU 커널 최적화 evolving agent team임. 로봇과 무관함</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2610.37624'>Rare, Relevant, and Still Wrong: How Memory Fails LLM Group Decisions</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM 그룹 결정 memory 실패 분석임. 로봇과 무관함</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2610.37720'>LRMoE: Demand-Side Load Re-Calibration for Efficient MoE Training on Memory-Constrained Nodes</a></td><td>28</td><td>0</td><td>LG</td><td>MoE 학습 부하 재조정임. 로봇과 무관함</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2610.37323'>UCVE: Graph Structured Retrieval for Compliance Validation</a></td><td>26</td><td>0</td><td>NLP</td><td>그래프 구조 retrieval 기반 규정 검증임. 로봇과 무관함</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2610.37732'>ThinkJev: One Thought, Every Budget for Calibrated Typed Decisions</a></td><td>26</td><td>0</td><td>NLP</td><td>typed decision 확률 보정임. 로봇과 무관함</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2610.36882'>Hyperparameter and Neural Architecture Search via Evolutionary Optimization for Reinforcement Learning: HPNAS-RL</a></td><td>25</td><td>3</td><td>RL</td><td>자율주행 RL의 NAS와 HPO를 진화적으로 함께 탐색함, 시뮬레이터 한정이며 incremental임</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2610.37216'>Zhengrong-Spatial-Aware 1.0: Advancing 3D Multimodal Intelligence</a></td><td>25</td><td>2</td><td>Multimodal</td><td>3D spatial VQA용 fine-tuning 파이프라인 보고서로 engineering 위주이며 새 기여가 약함</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2610.36249'>Hierarchical Multimodal Interaction Reasoning for Dyadic Relationship Recognition</a></td><td>25</td><td>1</td><td>Multimodal</td><td>dyadic 관계 인식용 계층 MoE와 loss 설계이며 소셜 벤치마크 점수 개선 수준임</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2610.36340'>CrowdCC: Jointly Benchmarking Corruption Robustness and Deployment Quantization in Crowd Counting</a></td><td>25</td><td>1</td><td>CV</td><td>군중 계수의 corruption 및 양자화 벤치마크로 평가 위주이며 로봇과 무관함</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2610.36844'>AxisQ: Depth-Adaptive Channel--Frequency Quantization for Camouflaged Object Detection</a></td><td>25</td><td>1</td><td>CV</td><td>위장 객체 검출 모델의 깊이별 bit 할당 양자화로 특정 과제 한정임</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2610.37097'>TriDifNet: A Unified Three-Task Diffusion Network for End-to-End RGB-T Perception</a></td><td>25</td><td>1</td><td>CV</td><td>RGB-T 정합, 융합, 검출을 diffusion 모듈로 묶은 보행자 검출 pipeline으로 특정 데이터셋 개선임</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2610.37309'>MvT: Event-based Multi-view Projection for Multiple Object Tracking</a></td><td>25</td><td>1</td><td>CV</td><td>event camera 다중 객체 추적용 multi-view 투영과 training-free 연관이며 응용 범위가 좁음</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2610.36190'>Bayesian Evidence Accumulation for Graph-Based Learning in Dynamic Data-Driven Applications Systems</a></td><td>25</td><td>1</td><td>LG</td><td>sequential evidence accumulation GNN이며 CIFAR10 실험뿐이라 증거가 약함</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2610.36395'>When Can a Learned Design Surrogate Be Trusted in a Self-Driving Microfluidics Laboratory? An Offline Closed-Loop Framework Built and Tested on Six Public Tables</a></td><td>25</td><td>1</td><td>LG</td><td>microfluidics 자율 실험실용 surrogate 신뢰 판단 프레임워크이며 공개 표 기반 오프라인 평가임</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2610.36633'>Deep Bayesian Filtering for Nonlinear Structural System Identification: A Tutorial on Structural and Physical Inductive Biases</a></td><td>25</td><td>1</td><td>LG</td><td>구조물 시스템 식별용 deep Bayesian filtering 튜토리얼임</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2610.36510'>Identity or Evidence? Auditing Evidence Dependence in Agentic Life-Science Benchmarks</a></td><td>25</td><td>0</td><td>NLP</td><td>생명과학 agent 벤치마크가 이름에 의존하는지 감사한 분석으로 로봇과 무관함</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2610.37015'>RePAIR: Inverting Backdoor Attacks in Semantic Segmentation</a></td><td>25</td><td>0</td><td>CV</td><td>분할 모델 backdoor 방어로 로봇과 무관함</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2610.37138'>MixSIS: Mixed-supervised instance segmentation</a></td><td>25</td><td>0</td><td>CV</td><td>여러 annotation 수준을 섞는 instance segmentation 설정이며 annotation 비용 절감 응용임</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2610.37290'>Taming Noise Initialization for Zero-shot Video Restoration with Image Diffusion Priors</a></td><td>25</td><td>0</td><td>Video</td><td>zero-shot 비디오 복원용 noise 초기화 기법으로 로봇과 무관함</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2610.37503'>ALADDIN: Adversarial Latent Diffusion Distillation for One-Step Identity Swapping</a></td><td>25</td><td>0</td><td>Generative</td><td>face swap을 one-step adversarial 증류로 가속했으며 로봇과 무관함</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2610.37583'>Zero-Shot Multimodal Event Spotting in Soccer Broadcasts</a></td><td>25</td><td>0</td><td>Video</td><td>축구 중계 이벤트를 zero-shot MLLM으로 검출하는 응용으로 3경기 평가임</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2611.00107'>Dynamic Merging Mutually-Distilled Multi-View Networks for RGB-Event-based Representation Learning</a></td><td>25</td><td>0</td><td>CV</td><td>RGB-event 표현을 mutual distillation과 모델 병합으로 융합한 기법이며 일반 개선 수준임</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2610.36110'>Dirichlet Process Mixtures within Semiparametric Bayesian Networks: A Novel Conditional Density Estimation Approach</a></td><td>25</td><td>0</td><td>LG</td><td>Bayesian network의 CPD를 DPM으로 바꾼 확률 모델 개선이며 로봇 연관 없음</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2610.36180'>Dynamical coarse-graining of neural-network training</a></td><td>25</td><td>0</td><td>LG</td><td>신경망 학습의 dynamical coarse-graining 정리이며 단일 ReLU 사례만 보임</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2610.36204'>Concorde: Geometry-Aware Link Prediction via Decoupled Energy Minimization</a></td><td>25</td><td>0</td><td>LG</td><td>그래프 link prediction용 energy 기반 모델이며 로봇 연관 없음</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2610.36245'>Three Worlds for the Price of a Logarithm: Baseline-Protected Best-of-Both-Worlds Combinatorial Semi-Bandits</a></td><td>25</td><td>0</td><td>LG</td><td>semi-bandit의 baseline 보호 regret 이론이며 로봇 연관 없음</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2610.36311'>Confidence Is Not a Promise: A Reference Audit of Typed Decision Models</a></td><td>25</td><td>0</td><td>LG</td><td>typed decision model의 confidence 보증을 감사하는 연구이며 로봇 연관 없음</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2610.36517'>PRISM: Pathology Reliability In Scarce-label Medicine. A Tile-level Benchmark of Pathology Foundation Models</a></td><td>25</td><td>0</td><td>CV</td><td>병리 foundation model의 보정과 label 효율 벤치마크이며 워크숍 수준임</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2610.36801'>API-TAIL: Detecting Model Substitution in LLM APIs through Temperature-Aligned Likelihood Tails</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM API 모델 치환을 탐지하는 감사 방법임</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2610.36806'>LLM knowledge for improved Out-of-Distribution Tabular Prediction - A Cross-Validated Regularisation Approach</a></td><td>25</td><td>0</td><td>LG</td><td>LLM이 낸 계수 prior로 tabular OOD 예측을 개선하나 효과는 제한적이라고 스스로 밝힌 연구임</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2610.36933'>Provenance Signatures for Low Rank Adaptations of Image Diffusion Models</a></td><td>25</td><td>0</td><td>CV</td><td>diffusion LoRA 출처를 intrinsic dimension으로 검정함</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2610.37159'>Physics-Guided Flow Matching: A Generative AI Framework for Global Total Electron Content Forecasting</a></td><td>25</td><td>0</td><td>LG</td><td>물리 가이드 flow matching 기반 전리층 TEC 예측임</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2610.37206'>SimplexLoRA: Dynamic Rank Updating via Alternating Minimization with Simplex Projection</a></td><td>25</td><td>0</td><td>NLP</td><td>LoRA rank를 simplex 가중치로 배분하는 incremental 개선임</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2610.37329'>WCC: A Learning-Based Framework for Deciding When to Apply Cooperative Coevolution in Large-Scale Optimization</a></td><td>25</td><td>0</td><td>RL</td><td>대규모 최적화에서 cooperative coevolution 적용 시점을 RL로 결정함</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2610.37388'>Para-Gaussian Approximations of Random Deep Neural Networks</a></td><td>25</td><td>0</td><td>LG</td><td>무작위 초기화 신경망의 para-Gaussian 근사 이론임</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2610.37413'>Displacement Moments and Path-Terminal Separation in Brownian Interpolant Sampling</a></td><td>25</td><td>0</td><td>LG</td><td>Brownian interpolant 샘플링의 KL 보장 이론임</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2610.37456'>An Input Skip Can Reparameterize a VAE Without Improving the Generator</a></td><td>25</td><td>0</td><td>LG</td><td>VAE input skip이 생성기를 개선하지 않고 재매개화일 뿐임을 보인 워크숍 논문임</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2610.36191'>LLM Hallucination Detection via Low-rank Multilinear Decomposition</a></td><td>25</td><td>0</td><td>NLP</td><td>hidden state의 Tucker 분해로 LLM hallucination을 탐지하는 방법으로 로봇과 무관함</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2610.36797'>Language Models Keep Abandoned Analyses: Residue and Adaptation after Garden-Path Sentences</a></td><td>25</td><td>0</td><td>NLP</td><td>언어 모델의 garden-path 잔여 분석으로 로봇과 무관함</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2610.37292'>Multi-Label Agreement: A Flexible Framework for Inter-Annotator Reliability</a></td><td>25</td><td>0</td><td>NLP</td><td>multi-label 주석자 일치도 지표 제안임. 로봇과 무관함</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2610.36298'>Are Spiking Neural Networks Harder to Steal? The Role of Stochastic Encoding in Model Extraction</a></td><td>25</td><td>0</td><td>LG</td><td>SNN의 model extraction 방어 효과 분석임. 로봇과 무관함</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2610.36574'>ADTGuard: Adaptive Depth-Time Safeguard for Streaming Inference in Large Language Models</a></td><td>25</td><td>0</td><td>NLP</td><td>스트리밍 LLM 안전장치임. 로봇과 무관함</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2610.36580'>Follow the Herd: A Data-Driven Approach for Actionable Recourse</a></td><td>25</td><td>0</td><td>LG</td><td>actionable recourse 데이터 기반 방법임. 로봇과 무관함</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2610.37070'>Correctness Conditioning as Selection in Chain-of-Thought Faithfulness Evaluation</a></td><td>25</td><td>0</td><td>NLP</td><td>CoT faithfulness 평가의 선택 편향 분석임. 로봇과 무관함</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2610.37169'>Rènyi-Regularized Flow-Based Variational Inference for Bayesian Calibration</a></td><td>25</td><td>0</td><td>LG</td><td>Renyi 정규화 flow VI임. 로봇과 무관함</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2610.37631'>What Improves During Pretraining? Tracking Knowledge Acquisition with Point-in-Time Models</a></td><td>25</td><td>0</td><td>NLP</td><td>pretraining 중 지식 습득 추적임. 로봇과 무관함</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2610.37380'>Same Verdict, Different Readers: Personalizing Fact-Checking Explanations from Relative Preferences</a></td><td>24</td><td>0</td><td>NLP</td><td>독자별 팩트체크 설명 개인화임. 로봇과 무관함</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2610.36335'>OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning</a></td><td>24</td><td>0</td><td>NLP</td><td>온톨로지 기반 agentic RAG임. 로봇과 무관함</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2610.36623'>God Does Not Play Dice: Enforcing Batch Invariance in Agentic Kernel Generation</a></td><td>24</td><td>0</td><td>LG</td><td>배치 불변 커널 생성임. 로봇과 무관함</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2610.36900'>Natural Hard-Negative Mining from Positives for Instruction-Following Retrieval</a></td><td>24</td><td>0</td><td>NLP</td><td>instruction retrieval hard-negative mining임. 로봇과 무관함</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2610.37242'>Grounding LLM Agents in Business Processes: Process-Aware Knowledge Graphs for Reliable Multi-Step Service Invocation</a></td><td>24</td><td>0</td><td>AI</td><td>프로세스 인지 지식그래프로 API agent 개선함. 로봇과 무관함</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2610.36812'>Gradient flow of magnetic inclination and intensity as a GPS-free guidance mechanism</a></td><td>22</td><td>3</td><td>Navigation</td><td>지자기 inclination과 intensity의 gradient flow 유도로 제어 이론 중심이며 학습 로봇과 거리가 멂</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2610.36996'>Structure-Actuation Co-Design of All-Electric Heavy-Duty Robotic Manipulators</a></td><td>22</td><td>3</td><td>Design</td><td>중장비 manipulator 구조와 구동 co-design 최적화로 학습 기반 로보틱스와 거리가 멂</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2610.37190'>Acoustic Signature Optimisation for Bioinspired Flapping-Wing Micro Aerial Vehicles</a></td><td>22</td><td>3</td><td>Design</td><td>flapping-wing 날개 vein 배치로 소음을 줄인 설계 연구로 학습 로봇과 거리가 멂</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2611.00105'>Detector-Integrated Multi-Cue Association for Occlusion-Aware UAV Multi-Object Tracking</a></td><td>22</td><td>1</td><td>CV</td><td>YOLOv8n에 embedding head를 붙인 UAV 추적으로 incremental 개선임</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2610.36896'>PREEN: Exemplar-Based Color Style Transfer with Smartphone Editor Presets</a></td><td>22</td><td>0</td><td>CV</td><td>색 스타일 전이를 editor preset 회귀로 푸는 응용이며 로봇과 무관함</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2610.36978'>Explicit Regional Representations For Video Quality Assessment</a></td><td>22</td><td>0</td><td>Video</td><td>VQA를 위한 regional heatmap 표현이며 로봇과 무관함</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2610.37186'>VGIQA: Fine-Grained Image Quality Assessment with Visual Grounding Rewards</a></td><td>22</td><td>0</td><td>Multimodal</td><td>IQA에 국소 평가 reward를 쓰는 RL이며 로봇과 무관함</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2610.37236'>HDVS: semi-supervised semantic segmentation via heterogeneous dual-branch voting supervision</a></td><td>22</td><td>0</td><td>CV</td><td>semi-supervised 분할의 voting pseudo-label 기법으로 incremental 개선임</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2610.37267'>GradCO: Behavior-Aware Gradient-Conflict Offloading for Text-Based Person Anomaly Search</a></td><td>22</td><td>0</td><td>Multimodal</td><td>텍스트 기반 이상 행동 보행자 검색용 MoE와 loss 설계로 로봇과 무관함</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2610.37599'>MoI-Bench: A Benchmark for Image Generation and Editing on Mobile Devices</a></td><td>22</td><td>0</td><td>Generative</td><td>모바일 기기 이미지 편집 벤치마크로 로봇과 무관함</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2610.36097'>Minimax-Optimal Small-Loss Bounds for Online Linear Optimisation on $\ell_p$ Balls</a></td><td>22</td><td>0</td><td>LG</td><td>online linear optimisation의 minimax 이론 결과로 로봇 학습과 거리가 먼 주제임</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2610.36280'>EVA-Flow: Learning Shared Chemistry for Unified Environment-Aware Molecular Conformation Generation</a></td><td>22</td><td>0</td><td>LG</td><td>환경 조건부 분자 conformer 생성 모델이며 로봇 연관 없음</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2610.36321'>AHEAD: Adaptive Neural Acceleration for Large-Scale Linear Programming</a></td><td>22</td><td>0</td><td>LG</td><td>대규모 LP 풀이 가속용 step size 예측기이며 로봇 연관 없음</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2610.36470'>Underdamped Anchored Langevin Dynamics</a></td><td>22</td><td>0</td><td>LG</td><td>비미분 target용 underdamped Langevin 샘플러 이론임</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2610.36572'>Learning from Points and Patches: A Pre-trained Hybrid Attention Transformer for Time Series Analysis</a></td><td>22</td><td>0</td><td>LG</td><td>시계열 pretraining용 attention 구조이며 incremental임</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2610.36650'>TACO-Graph: Automated Construction of Text-Atributed Graphs</a></td><td>22</td><td>0</td><td>LG</td><td>text-attributed graph 구성 선택을 decision tree로 학습함</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2610.36703'>RankFormer: Rethinking Time Series Transformers through Representation Capacity Analysis and Progressive Decoding</a></td><td>22</td><td>0</td><td>LG</td><td>시계열 transformer 구조 개선이며 incremental임</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2610.37005'>Compote: Collapse-Resistant Multiple Hypothesis Learning For Sequential Recommendation</a></td><td>22</td><td>0</td><td>LG</td><td>순차 추천용 multi-hypothesis 학습이며 로봇 연관 없음</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2610.37139'>Generative Replay for Equilibrium Propagation: Toward Edge-Friendly Continual Learning in Hopfield Networks</a></td><td>22</td><td>0</td><td>LG</td><td>Hopfield 네트워크의 EqProp 연속학습이며 MNIST·CIFAR 규모임</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2610.37239'>When Is a Relation Worth Trusting? Manipulation Costs, Exposure, and the Trust Trap in Multi-Relational Graph Learning</a></td><td>22</td><td>0</td><td>LG</td><td>multi-relational graph 탐지기의 조작 비용 분석이며 로봇 연관 없음</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2610.37373'>Euclidean Crowding-Driven Adaptive Euclidean-Hyperbolic Graph Learning</a></td><td>22</td><td>0</td><td>LG</td><td>유클리드와 쌍곡 공간을 적응 융합하는 그래프 학습임</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2610.37598'>GAS-PFN: Graph-Aware Spatiotemporal Prior-Data Fitted Networks for Zero-Shot Traffic Forecasting</a></td><td>22</td><td>0</td><td>LG</td><td>교통 예측용 그래프 인식 PFN이며 로봇 연관 없음</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2610.37647'>MuonGS: Pretraining LLMs with Relaxed Weight-Norm Control</a></td><td>22</td><td>0</td><td>LG</td><td>Muon 계열 optimizer의 weight-norm 제어를 이론으로 분석한 LLM pretraining 연구로 로보틱스와 무관함</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2610.37657'>Heads of Security: Learned Attention Gates Improve Prompt Injection Robustness</a></td><td>22</td><td>0</td><td>NLP</td><td>attention gate로 prompt injection을 방어하는 LLM 보안 연구로 로봇과 무관함</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2610.36178'>3, 7, 14, 17, 42: Instruction Tuning Installs and Sharpens Number-Choice Heuristics in Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>instruction tuning이 난수 선택 편향을 만드는 현상을 측정한 분석으로 로봇과 무관함</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2610.36759'>DocSkill: Skill-Integrated Agentic Reasoning for Multilingual Multi-Hop Document Question Answering</a></td><td>22</td><td>0</td><td>NLP</td><td>다국어 문서 QA agent와 benchmark로 로봇과 무관함</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2610.36805'>Personality Latents: Conditioning Frozen Language Models on Individuals from Their Own Writing</a></td><td>22</td><td>0</td><td>NLP</td><td>글에서 개인 latent를 학습해 frozen LM에 soft prefix로 넣는 성격 조건화임</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2610.37068'>Hierarchical Low-Rank Reparameterization for Parameter-Efficient Fine-Tuning</a></td><td>22</td><td>0</td><td>NLP</td><td>PEFT 파라미터를 계층적 low-rank로 더 압축하는 incremental 기법임</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2610.37265'>REGLAT at ArGuard Shared Tasks: An Ensemble-Based Model Integrating NER for Harmful Content Detection in Arabic</a></td><td>22</td><td>0</td><td>NLP</td><td>아랍어 유해 콘텐츠 공유과제 앙상블 시스템임. 로봇과 무관함</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2610.37465'>What Carries Forward? Pretraining Disclosure Across Language Model Releases</a></td><td>22</td><td>0</td><td>NLP</td><td>LM 릴리스별 pretraining 공개 정보 분석임. 로봇과 무관함</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2610.36116'>Why and How to Do Science When AI Is Better at It: A Framework Grounded in Human Understanding and Direction</a></td><td>22</td><td>0</td><td>AI</td><td>AI 시대 과학의 역할을 논하는 position 성격임. 로봇과 무관함</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2610.36329'>Plenty of Room in the Middle: Revealing Opportunities on a GPU Cluster via Fine-Grained Monitoring</a></td><td>22</td><td>0</td><td>LG</td><td>GPU 클러스터 세밀 모니터링 분석임. 로봇과 무관함</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2610.36589'>InfraDev: Can Coding Agents Develop AI Infrastructure, and How Can We Tell?</a></td><td>22</td><td>0</td><td>AI</td><td>AI 인프라 개발 coding agent benchmark임. 로봇과 무관함</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2610.36776'>Dependency Graphs of Mathematical Arguments: Representation, Structural Measurement, and Proof Review</a></td><td>22</td><td>0</td><td>AI</td><td>수학 논증 의존 그래프 표현임. 로봇과 무관함</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2610.36878'>RubricAtlas: Mining Type-Level Rubrics from Expert Reports to Evaluate Deep Research Agents</a></td><td>22</td><td>0</td><td>NLP</td><td>deep research agent 평가 rubric임. 로봇과 무관함</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2610.36888'>Noise Steering: Exploiting Wake Steering and Acoustic Directivity for Noise-Constrained Wind Farm Control via Reinforcement Learning</a></td><td>22</td><td>0</td><td>LG</td><td>풍력단지 소음 제약 제어임. 로봇과 무관함</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2610.36991'>SpectRAG: Weighted Chunk Graphs for Token-Budgeted Context Selection in Multi-Hop Retrieval-Augmented Generation</a></td><td>22</td><td>0</td><td>NLP</td><td>chunk 그래프 기반 RAG context 선택임. 로봇과 무관함</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2610.37281'>RPSD: Retrieval-Privileged On-Policy Self-Distillation with Optimal Transport</a></td><td>22</td><td>0</td><td>LG</td><td>순차 추천 self-distillation임. 로봇과 무관함</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2610.37405'>Clearing the FoG: Training KG Agents to Retrieve the Evidence Behind Their Answers</a></td><td>22</td><td>0</td><td>NLP</td><td>KG agent 근거 검색 학습임. 로봇과 무관함</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2610.37461'>Concordat: Typed Sessions for LLM Agents</a></td><td>22</td><td>0</td><td>AI</td><td>LLM agent typed session임. 로봇과 무관함</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2610.37731'>Amortized Localized Posterior Inference for Model Calibration with Application to an Ocean Turbulence Closure</a></td><td>22</td><td>0</td><td>LG</td><td>해양 난류 closure 보정용 amortized 추론임. 로봇과 무관함</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2610.37739'>OpenFrontiers: A Collection of Open Research Problems and a Benchmark for Scientific Rediscovery</a></td><td>22</td><td>0</td><td>AI</td><td>과학 재발견 benchmark임. 로봇과 무관함</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2610.36743'>Readout and Operating-Point Sensitivity in Event-Stream Candidate Selection</a></td><td>20</td><td>1</td><td>CV</td><td>event stream 후보 선택의 readout 민감도를 따진 신중한 평가이나 기여가 부정적 결과 위주임</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2610.36569'>Decoupling Consistency and Conflict across MLLM Layers for Fake News Detection</a></td><td>20</td><td>0</td><td>Multimodal</td><td>가짜 뉴스 검출용 MLLM 층별 분리 기법으로 로봇과 무관함</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2610.36756'>Efficient Remote Sensing Image-Text Retrieval via Interaction-Free Recall and Text-Guided Reranking</a></td><td>20</td><td>0</td><td>CV</td><td>원격탐사 이미지 텍스트 검색의 recall 후 rerank 효율화로 로봇과 무관함</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2610.36951'>Dense Representation Learning and Differentiable Shape Modeling for Spine Landmark Detection</a></td><td>20</td><td>0</td><td>CV</td><td>척추 landmark 검출을 pixel 대조 학습으로 재정식화했으나 의료 영상 한정임</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2610.37135'>Physics Guided Diffusion Model Based Exposure Interpolation for High Dynamic Range Imaging</a></td><td>20</td><td>0</td><td>CV</td><td>HDR용 노출 보간 diffusion으로 로봇과 무관함</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2610.37178'>INTR++: INterpretable TRansformer with better Accuracy, Interpretability, and Adaptability</a></td><td>20</td><td>0</td><td>CV</td><td>interpretable transformer에 prompt adapter를 추가한 소규모 개선임</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2610.37226'>Subspace Clifford Networks</a></td><td>20</td><td>0</td><td>CV</td><td>Clifford network의 grouped subspace 재구성이며 CIFAR-100 중심 아키텍처 효율화임</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2610.37431'>Segmentation Confidence for Arbitrary CNNs</a></td><td>20</td><td>0</td><td>CV</td><td>의료 분할 CNN의 confidence 점수 추정으로 로봇과 무관함</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2610.37510'>A note on data-efficient finetuning of vision foundation models</a></td><td>20</td><td>0</td><td>LG</td><td>visual prompting과 LoRA 등 전이 방법의 경험적 비교 노트임</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2610.36383'>From Generation to Scoring: Scaling LLM-Based Semantic Labeling at LinkedIn</a></td><td>20</td><td>0</td><td>NLP</td><td>LinkedIn 라벨링을 scoring으로 바꾼 산업 시스템 보고임</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2610.36393'>SpecLST: Spectral-Enhanced Long-Short Term Spatio-Temporal Multimodal Modeling for Traffic Forecasting</a></td><td>20</td><td>0</td><td>LG</td><td>교통 예측용 주파수 도메인 모델이며 incremental 개선임</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2610.36465'>Split Federated Unlearning</a></td><td>20</td><td>0</td><td>LG</td><td>split federated unlearning 문제 정의와 초기 방법이며 로봇 연관 없음</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2610.36616'>Normalized Cuts and Data Clustering via Matrix Fractional Programming</a></td><td>20</td><td>0</td><td>LG</td><td>Normalized cut의 fractional programming 풀이이며 로봇 연관 없음</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2610.36649'>When Is a Cheap Fairness Edit Safe? Screening Post-Hoc Edits in Two-Sided Matching Markets</a></td><td>20</td><td>0</td><td>LG</td><td>matching market의 fairness 편집 안전성 선별이며 로봇 연관 없음</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2610.36696'>HeteGCD: Statistics-Aware Dual-Prototype Learning for Generalized Category Discovery on Heterophilous Graphs</a></td><td>20</td><td>0</td><td>LG</td><td>heterophilous graph의 category discovery이며 로봇 연관 없음</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2610.36935'>Gaussian Process Bandits for Constraint Black Box Lever Optimization</a></td><td>20</td><td>0</td><td>LG</td><td>예산 배분용 GP-UCB 적용 산업 사례임</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2610.37389'>How Many and How Much? Contrastive Learning with Negative Samples for Knowledge Graph Embedding</a></td><td>20</td><td>0</td><td>LG</td><td>지식 그래프 임베딩의 negative sample 배분 개선임</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2610.37157'>What Survives Distillation? A Mechanistic Interpretability Study of GPT-2 and DistilGPT-2</a></td><td>20</td><td>0</td><td>NLP</td><td>GPT-2와 DistilGPT-2의 circuit을 비교한 interpretability 소규모 연구임</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2610.37484'>Teach reality, not ethics: a drop-in continued-pretraining corpus installs coupled human-biosphere-AI welfare dispositions across model families</a></td><td>20</td><td>0</td><td>NLP</td><td>생태 윤리 continued-pretraining 코퍼스임. 로봇과 무관함</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2610.36100'>CohortFlow: A Steerable Clinical Cohort Curation Agent with Localized Semantic Correction</a></td><td>20</td><td>0</td><td>NLP</td><td>임상 코호트 선별 agent임. 로봇과 무관함</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2610.36239'>BehaveRec: When Does Long-Term Behavioral History Help Sequential Recommendation? A Study with Session, History, and Community Signals</a></td><td>20</td><td>0</td><td>LG</td><td>순차 추천에서 장기 이력 효과 연구임. 로봇과 무관함</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2610.36325'>Ontology-guided multi-agent reasoning for explainable differential diagnosis</a></td><td>20</td><td>0</td><td>NLP</td><td>온톨로지 기반 감별진단 multi-agent임. 로봇과 무관함</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2610.36389'>MAREval: A Multi-Agent Framework for Evaluating Natural Language Recommendation Explanations</a></td><td>20</td><td>0</td><td>NLP</td><td>추천 설명 평가용 multi-agent임. 로봇과 무관함</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2610.36764'>Beyond the Evidence Coherence Trap: Agent-Driven Evidence Selection for Temporally Disordered Fake News Detection</a></td><td>20</td><td>0</td><td>NLP</td><td>시간 뒤섞인 가짜뉴스 탐지임. 로봇과 무관함</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2610.36820'>An Incremental Knowledge-Graph Learner Digital Twin for Evidence-Grounded Early Warning</a></td><td>20</td><td>0</td><td>AI</td><td>학습자 조기경보용 지식그래프 digital twin임. 로봇과 무관함</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2610.36962'>Do bots feel bad? Assessing empirical evidence for functional valence in LLMs</a></td><td>20</td><td>0</td><td>AI</td><td>LLM 기능적 valence 증거 평가임. 로봇과 무관함</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2610.37316'>ReForest: Interpretability Meets Reasoning in Isolation Forest</a></td><td>20</td><td>0</td><td>LG</td><td>Isolation Forest 해석 추론 결합임. 로봇과 무관함</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2610.37407'>Constraining the Commit Boundary: A DIO/ODI-Informed Authorization Guardrail for Agentic Entity Resolution</a></td><td>20</td><td>0</td><td>AI</td><td>entity resolution agent 권한 guardrail임. 로봇과 무관함</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2610.37655'>KPPax: preprocess differentiable kinetic ODE for machine learning in atmospheric chemistry</a></td><td>20</td><td>0</td><td>LG</td><td>대기화학 미분가능 ODE임. 로봇과 무관함</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2610.37310'>Spiking Neuromorphic Control for Periodic Orbits Stabilization in Underactuated Robots: A Greedy Lyapunov-Based Approach</a></td><td>18</td><td>3</td><td>Control</td><td>spiking 신경망 제어기의 orbital stabilization 이론으로 학습 로봇 주제와 거리가 멂</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2610.36363'>Reliability-Aware Short-Term Glycemic Risk Prediction Using an Anchor-Based Comparative Framework of Sequence, Multimodal, and State-Updating Digital-Twin Models</a></td><td>18</td><td>0</td><td>LG</td><td>혈당 위험 예측 모델 비교이며 유의한 성능 차이도 없음</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2610.36440'>Learning atomic interactions for the thermodynamics of liquid mixtures</a></td><td>18</td><td>0</td><td>LG</td><td>액체 혼합물 활동도계수용 GNN이며 로봇 연관 없음</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2610.36558'>Holomorphic Cauchy Networks for Efficient Stationary Tail Computation in High-Dimensional Reflected Brownian Motions</a></td><td>18</td><td>0</td><td>LG</td><td>reflected Brownian motion tail 계산용 네트워크이며 로봇 연관 없음</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2610.36970'>On the VC Dimension of Autoregressive Linear Threshold Functions</a></td><td>18</td><td>0</td><td>LG</td><td>autoregressive LTF의 VC dimension 이론임</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2610.36981'>GNN-Guided Network Reduction for Centralized Urban Traffic Routing</a></td><td>18</td><td>0</td><td>LG</td><td>도시 교통 경로 최적화용 GNN 네트워크 축소임</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2610.37365'>TRIDENT-Seq: Profile-Matched Prefix-Future Contrast for Label-Efficient Payment Risk Modeling</a></td><td>18</td><td>0</td><td>LG</td><td>결제 사기 위험용 거래 시퀀스 pretraining 산업 사례임</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2610.37561'>When uncertainty quantification fails: structural vulnerabilities and corrections for selective prediction under clinical class imbalance</a></td><td>18</td><td>0</td><td>LG</td><td>임상 클래스 불균형 하의 selective prediction 불확실성 문제임</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2610.37737'>Anisotropic Trust Region Warping for Prior-Data Fitted Networks in Bayesian Optimisation</a></td><td>18</td><td>0</td><td>LG</td><td>PFN 기반 Bayesian optimisation의 입력 warping 보정으로 workshop 수준의 작은 기여임</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2610.36668'>A Quantitative Approach to Asch Conformity in Frontier Large Language Models</a></td><td>18</td><td>0</td><td>NLP</td><td>LLM의 Asch conformity를 분포 비교로 정량화한 연구임</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2610.36915'>Do We Need an LLM to Know Why Sources Conflict? Decision Models for Knowledge-Conflict Typing in RAG</a></td><td>18</td><td>0</td><td>NLP</td><td>RAG 지식 충돌 유형 분류에 decision model을 쓰는 비용 비교임</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2610.36234'>MARQ: A Modular, LLM-Agnostic Requirement Quality Assessor Infused with Systems Engineering Knowledge</a></td><td>18</td><td>0</td><td>AI</td><td>요구사항 품질 평가 도구임. 로봇과 무관함</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2610.36433'>LM-DSB: A Lightweight Multi-agent System for Automated Daily Safety Bulletin Generation in Construction</a></td><td>18</td><td>0</td><td>AI</td><td>건설 안전 일일 브리핑 생성 multi-agent임. 로봇과 무관함</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2610.36513'>MedConstBench: Benchmarking How Constitutions Steer LLMs in Medical Ethics</a></td><td>18</td><td>0</td><td>NLP</td><td>의료 윤리 constitution 영향 benchmark임. 로봇과 무관함</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2610.36631'>The uneven rise of AI-generated web content</a></td><td>18</td><td>0</td><td>AI</td><td>AI 생성 웹 콘텐츠 증가 측정임. 로봇과 무관함</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2610.36689'>PsyJev: Psychological Analysis via System-1 Judgment</a></td><td>18</td><td>0</td><td>NLP</td><td>심리 분석 System-1 판단임. 로봇과 무관함</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2610.37166'>LiveSearch: Questions as Executable Verifier Code for a Live Benchmark of Professional-Source Financial Search Agents</a></td><td>18</td><td>0</td><td>NLP</td><td>금융 검색 live benchmark임. 로봇과 무관함</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2610.37237'>GraphRAGProv: GraphRAG Meets How-Provenance</a></td><td>18</td><td>0</td><td>AI</td><td>GraphRAG provenance임. 로봇과 무관함</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2610.36990'>The State and Fate of Multilingual, Contextual Evaluation in the NLP World</a></td><td>16</td><td>0</td><td>NLP</td><td>다국어 benchmark 감사 연구임</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2610.36407'>A 2-DOF MultiBody Track Joint for Race Car Optimization</a></td><td>15</td><td>2</td><td>Robotics</td><td>Modelica 레이스카용 트랙 joint 컴포넌트로 시뮬레이션 도구 성격이 강함</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2610.36379'>Evaluating Federated Vision-Language and Vision-Only Models for Privacy-Aware Breast Cancer Imaging</a></td><td>15</td><td>0</td><td>CV</td><td>유방 영상 federated learning 평가로 로봇과 무관함</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2610.36411'>ORBITAL: Optimization of Robust Brain--Computer Inference Through Architecture-Aware Low-Precision Compression</a></td><td>15</td><td>0</td><td>LG</td><td>EEG 디코더 압축과 적대적 강건성 연구로 로봇과 무관함</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2610.36487'>Spatial-Frequency Learning for Scanning Transmission Electron Microscopy Image Enhancement</a></td><td>15</td><td>0</td><td>CV</td><td>전자현미경 이미지 복원이며 로봇과 무관함</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2610.36540'>Frugal Handwritten Text Recognition for Sub-Saharan Civil-Status Registers: A Smartphone-to-Records Pipeline with CPU-Only Inference</a></td><td>15</td><td>0</td><td>CV</td><td>아프리카 수기 문서 인식 파이프라인이며 단일 등기소 범위의 실현 가능성 연구임</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2610.36722'>Progressively Refining SAM for Accurate Phytoplankton Segmentation</a></td><td>15</td><td>0</td><td>CV</td><td>SAM 기반 식물성 플랑크톤 분할로 5쪽 소규모 응용임</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2610.36750'>Multi-task Disentangling Fusion Mamba-CNN for MODIS Spectral-Temporal Unmixing with Endmember Variability Modeling</a></td><td>15</td><td>0</td><td>CV</td><td>MODIS 분광 unmixing 응용으로 로봇과 무관함</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2610.36781'>CVBL-CCTV-Face Dataset for Real-World Face Enhancement and Recognition in Surveillance</a></td><td>15</td><td>0</td><td>CV</td><td>CCTV 얼굴 초해상 데이터셋으로 로봇과 무관함</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2610.36857'>Evaluating AlphaEarth Embeddings for Crop Classification: Separability, Temporal Dynamics, and Cross-Regional Transferability</a></td><td>15</td><td>0</td><td>LG</td><td>AlphaEarth 임베딩의 작물 분류 평가로 로봇과 무관함</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2610.36873'>RangeRectQuant: Compressing Scientific Fields for Every Future Rectangular Sum</a></td><td>15</td><td>0</td><td>CV</td><td>과학 래스터의 직사각형 합 보존 양자화 알고리즘으로 로봇과 무관함</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2610.37021'>Ground-to-Satellite Knowledge Distillation for Crop Classification under Temporal and Geographic Shift</a></td><td>15</td><td>0</td><td>CV</td><td>지상 사진으로 위성 작물 분류를 증류하는 응용임</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2610.37074'>Systematic Morphometric Brain Autoencoding for Representation Learning in Neurodegenerative Diseases</a></td><td>15</td><td>0</td><td>CV</td><td>뇌 MRI self-supervised 사전학습으로 로봇과 무관함</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2610.37297'>TRUCO: A Scalable Lock-Free Algorithm for Parallel Contour Extraction</a></td><td>15</td><td>0</td><td>CV</td><td>병렬 contour 추출 알고리즘으로 시스템 최적화 성격임</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2610.37349'>TimeLineXR: An Interactive Exploration of Time in Vision-Language Models</a></td><td>15</td><td>0</td><td>Multimodal</td><td>VLM 시간 축 시각화 인터랙티브 데모로 연구 기여가 작음</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2610.36427'>Property-Based Testing for Robust Softmax and Cross-Entropy</a></td><td>15</td><td>0</td><td>LG</td><td>softmax 수치 오류를 property-based test로 고친 6쪽 기술 노트임</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2610.36429'>Simulated petrological labels enable probabilistic mineralogy prediction from whole-rock geochemistry</a></td><td>15</td><td>0</td><td>LG</td><td>지구화학 광물 조성 예측이며 로봇 연관 없음</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2610.36442'>High-Fidelity Aerostructural Dataset of Transonic Wings in Cruise Conditions</a></td><td>15</td><td>0</td><td>LG</td><td>천음속 날개 공력-구조 데이터셋 공개임</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2610.36583'>MM-Net: A Multimodal Multi-Task Network for Sleep Staging and Sleep Apnea Assessment After Ischemic Stroke</a></td><td>15</td><td>0</td><td>LG</td><td>뇌졸중 수면 단계 분류 의료 모델이며 로봇 연관 없음</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2610.36941'>Algorithmic Monoculture in Machine Learning-based Site-Specific Fertilizer Recommendation</a></td><td>15</td><td>0</td><td>LG</td><td>비료 추천 모델의 monoculture 경제 분석 워크숍 논문임</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2610.37338'>Normative Deviation Modeling for EEG-based Depression Detection</a></td><td>15</td><td>0</td><td>LG</td><td>EEG 우울증 탐지용 normative deviation 모델이며 로봇 연관 없음</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2610.37563'>Pneuma: A Large-Scale Real-World Time Series Benchmark for Commercial Aircraft Predictive Maintenance</a></td><td>15</td><td>0</td><td>LG</td><td>항공기 예지 정비 시계열 벤치마크 공개임</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2610.37712'>Moment-Guided Optimizers for Noisy Deep Learning: MGO-SC as a Simple Consistency Gate for Adam-Style Updates</a></td><td>15</td><td>0</td><td>LG</td><td>Adam에 sign-consistency gate를 붙인 작은 optimizer 수정으로 CIFAR-10 실험뿐임</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2610.36184'>Lipi-Ghor: A Large-Scale, Diarized, Multi-Domain Bengali Speech Corpus and a Scalable Pipeline for Building It</a></td><td>15</td><td>0</td><td>NLP</td><td>벵골어 음성 corpus 구축으로 로봇과 무관함</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2610.36230'>Beyond IceBERT: Open-Data ModernBERT Encoders for Icelandic from 12M to 1B Parameters</a></td><td>15</td><td>0</td><td>NLP</td><td>아이슬란드어 ModernBERT encoder 학습과 비교 연구임</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2610.36432'>No Tokenizer, Still a Gap: Cross-Lingual Fairness of Homoglyph and Invisible-Character Watermarking</a></td><td>15</td><td>0</td><td>NLP</td><td>homoglyph 워터마크의 언어 간 공정성 분석임</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2610.36538'>Agentic Data Sampling Framework for Multilingual ASR via Linguistic-Aware Error-Driven Optimization</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM agent로 다국어 ASR 데이터 샘플링을 고르는 방법으로 로봇과 무관함</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2610.36813'>Words or Deeds? How LLMs Predict Users&#x27; Decisions in Human-Agent Dialogue</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM이 사용자 결정을 예측할 때 발언을 과신하는지 본 행동 분석임</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2610.36910'>Nothing Left Behind: Embedding Retrieval and Language Model Screening for High Recall Evidence Search</a></td><td>15</td><td>0</td><td>NLP</td><td>체계적 문헌 검토용 embedding 검색과 LLM 선별 응용임</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2610.37229'>Decision Models as Judges for Hallucination Detection</a></td><td>15</td><td>0</td><td>NLP</td><td>hallucination 탐지에 decision model을 judge로 쓰는 비교 연구임</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2610.37494'>semanticfa: An R Package for Response-Free Semantic Factor Analysis of Psychometric Scales</a></td><td>15</td><td>0</td><td>NLP</td><td>심리측정 척도용 R 패키지임. 로봇과 무관함</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2610.36287'>A Smart Instant Book Filter Model based on Dual-Objective Optimization</a></td><td>15</td><td>0</td><td>LG</td><td>숙박 플랫폼 필터 모델임. 로봇과 무관함</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2610.36341'>Executable Archaeology of Programs That Model Programming: Reanimating the Heuristic Compiler (1961) and KBEmacs (1984)</a></td><td>15</td><td>0</td><td>AI</td><td>1961년 초기 AI 프로그램 재구현임. 로봇과 무관함</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2610.37045'>AI-Assisted Discovery of CNOT Decompositions for Quantum Permutations on Constrained Topologies</a></td><td>15</td><td>0</td><td>AI</td><td>양자 회로 CNOT 분해 탐색임. 로봇과 무관함</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2610.37081'>OpenGray: a benchmark for evaluating the decisions of radiotherapy planning agents</a></td><td>15</td><td>0</td><td>AI</td><td>방사선치료 계획 agent benchmark임. 로봇과 무관함</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2610.37243'>TCM-DiagCommit: A TCM-SD-Derived Benchmark for Evidence-Conditioned Syndrome Selection and Commitment</a></td><td>15</td><td>0</td><td>AI</td><td>한의학 증후 선택 benchmark임. 로봇과 무관함</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2610.37342'>Aligning Institutional Power and Operational Ability</a></td><td>15</td><td>0</td><td>AI</td><td>agentic AI 제도 권한과 능력 정렬 논의임. 로봇과 무관함</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2610.37459'>M4Bench: Evaluating Procedural Specification for Clinical EHR Derivation Agents</a></td><td>15</td><td>0</td><td>AI</td><td>임상 EHR 파생변수 benchmark임. 로봇과 무관함</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2610.36430'>A Singularity Avoiding Track Model for Race Car Optimization</a></td><td>14</td><td>2</td><td>Robotics</td><td>레이스 트랙 표면 모델 fitting 파이프라인으로 학습 로봇 주제와 거리가 멂</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2610.37727'>Predicate Neuron: Differentiable Quantization of Predicate Relations in Gradient-based Learning</a></td><td>14</td><td>0</td><td>LG</td><td>미분 가능한 predicate neuron 모듈로 MNIST 수준 평가의 incremental 기여임</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2610.36679'>Specialization, Diversity, and Scaling in Child-Scale Language Models</a></td><td>14</td><td>0</td><td>NLP</td><td>아동 규모 언어 모델의 특화와 다양성 연구로 로봇과 무관함</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2610.36929'>DocXEval: A Systematic Evaluation of Explainability in Multimodal Document Understanding</a></td><td>14</td><td>0</td><td>CV</td><td>문서 이해 모델의 XAI 방법 평가 프레임워크임</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2610.36428'>FORESEE-MS: Toward Prospective Spatial Forecasting of Future Multiple Sclerosis Lesions from Baseline FLAIR MRI</a></td><td>12</td><td>0</td><td>CV</td><td>다발성 경화증 병변 예측 평가 프로토콜로 39명 소규모이며 로봇과 무관함</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2610.36850'>uTHCD-C: A Corruption-Robustness Benchmark for Tamil Handwritten Character Recognition</a></td><td>12</td><td>0</td><td>CV</td><td>타밀 손글씨 인식 corruption 벤치마크로 로봇과 무관함</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2610.37118'>Multibranch Ensemble Head in Vision Foundation Models for Efficient Cucumber Phenological Stage Classification</a></td><td>12</td><td>0</td><td>CV</td><td>오이 생육 단계 분류용 앙상블 head로 농업 응용임</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2610.37134'>MRI-to-CT Translation of Spinal Images via Anatomy-Guided Pseudo-Pairing and Adversarial Diffusion</a></td><td>12</td><td>0</td><td>CV</td><td>척추 MRI에서 CT 합성하는 의료 영상 응용임</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2610.37406'>CTBakeGS: training-free baking of photorealistic CT volume renderings into 3D Gaussian splats</a></td><td>12</td><td>0</td><td>3D Vision</td><td>CT 볼륨 렌더링을 3DGS로 변환하는 의료 시각화 응용임</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2610.37570'>LCM-Promo: An LLM-Based Uplift Model for Promotion Allocation</a></td><td>12</td><td>0</td><td>LG</td><td>프로모션 할당용 LLM uplift 모델 4쪽 산업 보고임</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2610.37726'>Threshold Compatibility and Support-Selection Diagnostics in Neural Discovery of Partial Differential Equations</a></td><td>12</td><td>0</td><td>LG</td><td>neural PDE discovery의 threshold 진단으로 범위가 좁고 로봇과 무관함</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2610.36083'>FinLLM-KG: Knowledge Graph-Enhanced LLMs for Financial Sentiment Analysis in Algorithmic Trading</a></td><td>12</td><td>0</td><td>NLP</td><td>금융 감성 분석에 knowledge graph를 붙인 LLM 응용으로 로봇과 무관함</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2610.36527'>ETC-Bench: A Multilingual Benchmark for Evaluation-Side Transcript Canonicalization</a></td><td>12</td><td>0</td><td>NLP</td><td>다국어 transcript 정규화 benchmark로 로봇과 무관함</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2610.36937'>JevRec: Linguistic Encoding with Jev-like Decision Modeling for LLM-based Generative Recommendation</a></td><td>12</td><td>0</td><td>NLP</td><td>가변 길이 SID를 쓰는 LLM 생성 추천 기법으로 로봇과 무관함</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2610.37123'>SFE-O: An Ontology for Knowledge-Grounded AI in Supercritical CO$_2$ Biomass Extraction and Fractionation</a></td><td>12</td><td>0</td><td>AI</td><td>초임계 CO2 추출 온톨로지임. 로봇과 무관함</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2610.36956'>Mining the Nineteenth Century for the Thirteenth: Register-Scale Forced Alignment and HTR Bootstrapping via Legacy Regesta and Antiquarian Editions</a></td><td>10</td><td>0</td><td>NLP</td><td>중세 문서 HTR 보강 연구로 로봇과 무관함</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2610.37026'>Interpretable Deep Learning Models for Breast Cancer Diagnosis Using Medical Imaging</a></td><td>10</td><td>0</td><td>CV</td><td>유방암 진단 CNN 벤치마크와 설명 기법 적용이며 로봇과 무관함</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2610.37314'>A Lightweight Attention-Based CNN with Saliency-Map Interpretability for Skin Cancer Detection</a></td><td>10</td><td>0</td><td>CV</td><td>피부암 분류용 경량 CNN이며 로봇과 무관함</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2610.37472'>How Reliable Is Individualized Functional-Network Attribution in Resting-State fMRI Cognitive Prediction in ADNI?</a></td><td>10</td><td>0</td><td>CV</td><td>fMRI 속성 attribution 신뢰도 평가로 로봇과 무관함</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2610.37022'>Crop Yield Prediction Using Regression Models: A Comparative Evaluation of Model Performance</a></td><td>10</td><td>0</td><td>LG</td><td>회귀 모델 비교 수준의 작물 수확량 예측임</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2610.37733'>Selective Transfer Learning for Groundwater Level Anomaly Forecasting: Accuracy-Risk Trade-offs</a></td><td>10</td><td>0</td><td>LG</td><td>지하수 수위 예측의 선택적 transfer learning으로 도메인 응용이며 로봇과 무관함</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2610.36187'>Frankly Speaking: The Company Election Integrity Keeps in Congressional Communication</a></td><td>10</td><td>0</td><td>NLP</td><td>의회 뉴스레터의 선거 용어를 word embedding으로 분석한 정치 담론 연구임</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2610.36717'>A Harness Reducing over-Defensive Writing in Agents by Isolating Objections</a></td><td>10</td><td>0</td><td>NLP</td><td>agent 보고서의 과방어 문체를 줄이는 harness로 평가가 작고 로봇과 무관함</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2610.36911'>Developing a Speech Language Model for Basque</a></td><td>10</td><td>0</td><td>NLP</td><td>바스크어 speech language model 구축 보고임</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2610.37105'>Text Generation in Low-Resource Languages Using Human-Curated Vocabularies</a></td><td>10</td><td>0</td><td>NLP</td><td>저자원 언어 합성 텍스트 생성 연구임</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2610.37245'>Aligning Large Language Models for Safety in African Languages: A Case Study of Hausa</a></td><td>10</td><td>0</td><td>NLP</td><td>하우사어 safety alignment 데이터와 SFT 및 DPO 비교임</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2610.36816'>Integrated Design and Reproducible Feasibility Analysis of a Four-Wheel Rover with Packet-Commanded Imaging, LiDAR Ranging, and Learning-Assisted Target Recognition</a></td><td>8</td><td>2</td><td>Robotics</td><td>교육용 rover 설계 분석으로 실제 시험도 없고 연구 기여가 약함</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2610.37452'>Electric-Field Induction Motor with Discrete Circuit Elements and Improved Rotor Dynamics</a></td><td>8</td><td>2</td><td>Hardware</td><td>전기장 induction motor 회로 설계로 로보틱스 학습과 무관함</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2610.36360'>AK_QMUL at ArGuard Shared Tasks: A Single Fine-Tuned JAIS for Arabic Harmful-Prompt Detection</a></td><td>8</td><td>0</td><td>NLP</td><td>아랍어 유해 프롬프트 shared task 제출 기술 보고임</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2610.36667'>Japanese Discourse Structure Analysis Based on Segmented Discourse Representation Theory Using LLMs</a></td><td>8</td><td>0</td><td>NLP</td><td>일본어 SDRT 담화 구문 분석 연구임</td></tr>
</tbody></table>

</details>
