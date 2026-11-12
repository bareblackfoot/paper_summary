# 오늘의 arXiv Top 15: 2026-10-27 (화)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**

**신규 논문 수: 전체 871편 → 중복 제거 후 871편 (이번 평가 대상 871편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 215 |
| cs.LG | 234 |
| cs.RO | 117 |
| cs.CL | 138 |
| cs.AI | 167 |

---

## Top 15

### 1. Adapt for Planning, Not just Prediction: Optimistic Test-Time World Model Adaptation (76점)

[arXiv](https://arxiv.org/abs/2610.35636) · [PDF](https://arxiv.org/pdf/2610.35636) · [alphaXiv](https://www.alphaxiv.org/abs/2610.35636) (요약 있음)

- **저자**: Akshay Mete, Dileep Kalathil, P. R. Kumar
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 82점
- **학회**: CoRL 2026 채택 · 근거: comments에 "Accepted at the CoRL 2026 Workshop on Pretrain to Adapt"
- **읽은 원문**: PDF 전문

> 배포 중 world model을 고칠 때 예측 오차에 더해 planner의 목표 도달 비용까지 줄이도록 갱신하는 OpTTA를 제안함. 분포가 바뀐 설정 중 predictor만 적응하는 8개 설정에서, frozen model 대비 평균 최종 성공률 향상이 prediction-only 적응(AdaJEPA)의 6.9퍼센트포인트에서 13.5퍼센트포인트로 커짐.

**무슨 문제인가**

latent world model은 offline으로 사전학습한 뒤 test time에는 고정해 쓰므로, 카메라 영상이나 환경이 바뀌면 rollout이 부정확해지고 planning 성공률이 내려감. 기존 방법 AdaJEPA는 배포 중 관측한 transition의 latent 예측 오차를 줄이도록 model을 갱신함. 그런데 이 loop에서 관측되는 transition은 planner가 이미 고른 행동의 결과뿐임. 그래서 model이 자기 행동의 결과는 잘 맞히면서도 목표에 닿는 다른 행동에 대해서는 계속 틀릴 수 있고, 예측 오차가 낮아도 planning이 나아지지 않을 수 있음(objective mismatch).

**어떻게 푸나**

OpTTA(Optimistic Test-Time Adaptation)는 adaptive control의 RBMLE를 world model 적응에 옮긴 방법임. RBMLE(reward-biased maximum likelihood)는 관측 likelihood와 달성 가능한 최적 reward를 함께 키우는 model 추정법임. 입력은 사전학습된 JEPA(관측을 latent로 encoding하고 다음 latent를 예측하는 구조) world model, 목표 이미지, 최근 관측 transition buffer이고, 출력은 매 replanning 단계마다 갱신된 model 파라미터임. 손실은 buffer에 대한 latent 예측 오차 L_pred와 가중치 α_k를 곱한 planning 비용 L_plan의 합임. L_plan은 CEM(후보 행동열을 뽑고 좋은 것 주변에서 다시 뽑는 planning 방법) 마지막 iteration의 후보 행동열 200개를 고정한 채, 그 행동열의 상상 궤적이 목표 latent와 얼마나 먼지를 평균한 값임. gradient는 행동이 아니라 predictor 파라미터로 흘려서, 후보 계획이 목표에 더 가깝게 도달한다고 보는 낙관적인 model 쪽으로 갱신함. α_k는 두 gradient 크기의 비에 맞춰 정하고 replanning 단계가 진행될수록 √(k/K_max)로 키움. 추가 환경 상호작용은 필요 없고, 각 과제가 끝나면 model을 사전학습 파라미터로 되돌림.

**결과**

- 세 JEPA world model(LeWM, DINO-WM, temporal straightening)과 시각 손상·색·모양·질량·감쇠 변화를 합친 15개 설정에서, OpTTA의 최종 성공률이 AdaJEPA보다 높은 경우는 14개임. predictor만 적응하는 8개 설정에서 frozen 대비 평균 향상은 OpTTA 13.5퍼센트포인트, AdaJEPA 6.9퍼센트포인트임.
- temporal straightening의 PushT(물체를 밀어 목표 자세로 옮기는 2D 조작 과제)에서 시각 손상 7종 평균 최종 성공률은 frozen 47.8%, AdaJEPA 58.3%, OpTTA 74.0%임(predictor만 적응).
- planning 항의 부호를 뒤집어 비관적으로 만들면 최종 성공률이 AdaJEPA보다 낮아짐. PushT darkening에서 32.7% 대 44.7%, LeWM Reacher(팔 끝을 목표 지점에 보내는 reaching 과제) darkening에서 60.7% 대 70.7%임.

**한계**

PushT, Reacher, TwoRoom, maze 같은 저차원 시뮬레이션 과제만 다뤘고 실로봇이나 고차원 조작 과제는 보이지 않음. TwoRoom처럼 적응이 오히려 성능을 내리는 과제가 있고, 어느 파라미터를 갱신할지와 α_k 설계는 과제마다 다르며 최적이 아님을 저자도 인정함. DINO-WM에서는 replan당 시간이 2,971ms에서 5,233ms로 늘어남.

**누리랩 연구와의 연결**

- world model 기반 MPC를 test time에 고치는 방법이라 누리랩의 test-time optimization, world model 주제와 바로 이어짐. 실패 후 재계획 loop에서 model을 갱신하는 failure recovery 연구에서 baseline으로 쓸 수 있음.
- 예측 오차가 낮아도 planning 성공률이 오르지 않는 사례를 보인 분석은, world model 정확도와 과제 성공을 따로 재야 하는 근거가 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 아래 실행 줄에서는 world model이 상상 rollout으로 행동을 골라 환경에서 실행함. 위 적응 줄에서는 buffer의 예측 손실과 후보 rollout의 optimistic 손실을 더해 world model을 갱신하고, 다시 계획하는 순환을 보여 줌.*

---

### 2. Video World Models Need Predictable Latents (76점)

[arXiv](https://arxiv.org/abs/2610.34663) · [PDF](https://arxiv.org/pdf/2610.34663) · [alphaXiv](https://www.alphaxiv.org/abs/2610.34663) (요약 있음) · [코드](https://github.com/mattia-scardecchia/predictable-latents)

- **저자**: Mattia Scardecchia, Sherry Yang
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> video world model의 autoencoder를 reconstruction과 temporal objective로 함께 fine-tuning하고, decoder가 과거 frame을 참조하게 함. 같은 학습 예산에서 예측 품질과 policy 평가 정확도가 함께 오르며, DDIM 2 step 기준 실제 성공률과의 Pearson 상관이 0.21에서 0.67로 오름.

**무슨 문제인가**

video world model은 대부분 reconstruction만으로 학습한 autoencoder의 latent 위에서 다음 장면을 예측함. reconstruction은 화면의 세부를 보존하게 만들 뿐, 시간에 따른 변화를 예측하기 쉽게 만들지는 않음. 반대로 TD-MPC2 같은 reconstruction-free world model은 예측하기 쉬운 latent를 배우지만 미래 장면을 이미지로 복원하지 못함. 이미지가 없으면 VLM이 rollout 영상을 보고 과제 성공을 판정하는 policy 평가에 쓸 수 없고, RL·planning에도 쓰기 어려움.

**어떻게 푸나**

학습은 두 단계로 나뉨. 첫 단계에서 FLUX.1의 사전학습 autoencoder를 action이 붙은 인접 frame 쌍으로 fine-tuning하며, reconstruction loss와 temporal objective를 가중치 λ로 섞음. temporal objective는 보조 head가 현재 latent와 action으로 다음 latent를 맞히는 latent prediction, 또는 두 latent로 action을 맞히는 inverse dynamics임. 같은 단계에서 decoder에 cross-attention을 붙여 직전 실제 frame을 참조하게 함(past-conditioned decoder). 그러면 latent는 과거 frame에 없는 변화분만 담으면 됨. 두 번째 단계에서 encoder를 고정하고, 그 latent 위에서 action-conditioned diffusion world model(diffusion forcing 방식 DiT)을 학습함. 생성할 때는 첫 context frame과 action 열을 받아 latent를 만들고, decoder가 첫 frame을 참조해 미래 frame을 복원함. 보조 head는 world model 추론에 쓰지 않음.

**결과**

- 학습 예산은 autoencoder 80,000 update, world model 100,000 update로 같게 맞추고 seed 3개로 잼. AutoEval(학습 데이터인 Bridge V2 로봇 조작 영상과 다른 로봇 셋업에서 찍은 조작 영상)에서 out-of-distribution LPIPS(지각적 거리, 낮을수록 좋음)를 비교함. LPIPS가 reconstruction만 쓴 기본 방식의 0.302에서 latent prediction은 0.257, inverse dynamics는 0.236으로 내려감.
- WorldGym 방식 policy 평가(OpenVLA·Octo·RT-1-X가 Bridge 과제 17개를 world model 안에서 수행하고 VLM이 성공을 판정)에서 실제 성공률과의 Pearson 상관을 잼. DDIM 2 step에서 기본 방식 0.21, past-conditioned decoder만 쓴 경우 0.15, latent prediction 0.67, inverse dynamics 0.51임. 이 비교는 world model 학습 seed 1개 결과임.
- temporal objective를 쓴 world model은 DDIM 2 step만으로 기본 방식의 10 step보다 LPIPS·SSIM이 좋음. 기본 방식의 최종 validation LPIPS에 도달하는 update 수는 7.6배(latent prediction), 8.8배(inverse dynamics) 적음. decoder만 바꾼 경우는 1.8배임.
- 학습 예산 대신 reconstruction 오차를 같게 맞춘 통제 실험도 함(두 방식 모두 과거 frame을 참조하지 않는 일반 decoder). 이때 latent prediction의 OOD pixel MSE가 reconstruction만 쓴 경우보다 14.0% 낮음. 대신 같은 reconstruction 수준에 도달하는 데 latent prediction은 reconstruction만 쓸 때보다 autoencoder update가 약 35배 더 듦.

**한계**

데이터는 합성 환경과 Bridge V2 계열 로봇 조작 영상뿐이고, 2D autoencoder만 다룸. world model 안에서 policy를 학습해 실로봇으로 옮기는 실험은 없고, policy 평가 비교도 학습 seed 1개임. 채택한 λ=0.7에서 latent prediction의 FID·FVD는 같은 past-conditioned decoder로 reconstruction만 학습한 경우(λ=0)보다 나쁨. world model을 키우면 긴 rollout에서의 이득이 줄어듦.

**누리랩 연구와의 연결**

- VLA를 world model 안에서 평가하거나 test-time planning에 쓰려는 연구에서, 적은 DDIM step으로도 실제 성공률과의 상관을 유지하는 latent 설계 방법으로 바로 비교·적용할 수 있음.
- 과거 frame이 변하지 않는 장면 세부를 맡고 latent가 변화분만 담는 구조는 failure detection용 world model이나 robot memory에서 정적 정보와 동적 정보를 나누는 설계의 근거가 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 왼쪽 단계는 temporal objective와 과거 frame을 참조하는 decoder로 autoencoder를 fine-tuning함. 가운데는 고정한 encoder의 latent로 world model을 학습하고, 오른쪽은 첫 frame과 action 열로 미래 frame을 생성함.*

---

### 3. RoboDuo: Attempt, Check and Atomic Recovery through Code for Vision-Language-Action Models (75점)

[arXiv](https://arxiv.org/abs/2610.34108) · [PDF](https://arxiv.org/pdf/2610.34108) · [alphaXiv](https://www.alphaxiv.org/abs/2610.34108) (요약 있음)

- **저자**: Jie Wang, Bo Zhang, Renzhi Lu, Jianyu Chen
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 74점
- **읽은 원문**: PDF 전문

> 고정된 VLA가 긴 과제를 한 번 시도하면 coding agent가 쓴 프로그램이 완료 여부를 검사하고, 실패하면 짧은 skill만 배운 별도 VLA가 남은 단계를 끝내게 함. full-task VLA 가중치를 바꾸지 않고 π0.5의 LIBERO-Long 성공률을 93.6%에서 96.2%로 올림.

**무슨 문제인가**

VLA는 instruction과 현재 관측을 받아 바로 행동을 내므로, 지금 관측이 목표를 만족하는지 검사하지 않음. 그래서 긴 과제에서 물체를 놓치는 등 한 단계가 실패해도 같은 instruction으로 계속 움직이고 나머지 단계는 끝나지 않음. 상위 VLM이 token이나 latent를 하위 policy에 넘기는 dual-system 방식은 실패 판정, 재시도, 실행 policy 교체를 표현하지 못함. code-as-policy 방식은 재시도를 표현하지만 처음부터 primitive나 skill로 쪼개 실행하므로 full-task VLA가 가진 긴 과제 수행 능력을 쓰지 않음.

**어떻게 푸나**

RoboDuo는 행동을 내는 두 VLA와 판단만 하는 coding agent, 완료 검사기(is_task_complete)로 이루어짐. 에피소드 시작 시 coding agent가 instruction과 첫 관측을 받아 Python 프로그램과 atomic plan(남은 단계를 짧은 skill instruction과 sub-goal로 적은 목록)을 한 번 씀. 프로그램은 먼저 고정된 full-task VLA에게 원래 instruction으로 과제 전체를 한 번 시도시키고, 끝난 관측에서 검사기로 완료 여부를 판정함. 실패로 판정되면 atomic VLA가 plan의 각 단계를 실행하고, 단계마다 sub-goal이 만족될 때까지 최대 3번 재시도함. 이후 제어는 full-task VLA로 돌아가지 않음. atomic VLA와 coding agent, 검사기를 학습시키려고 LIBERO demonstration을 VLM으로 grasp, place, pull 등 5개 primitive 구간으로 자르고 효과가 끝난 시점에 경계를 맞춤. 이 구간에서 LIBERO-Atomic(125개 과제, clip 9,214개), LIBERO-Code(목표 프로그램), LIBERO-Judge(프레임별 완료 여부 label)를 만듦. coding agent와 검사기는 Qwen3.5-2B 하나를 fine-tuning해 겸함.

**결과**

- LIBERO(시뮬레이션 조작 benchmark, 4개 suite 각 10개 과제, 과제당 50회)의 Long suite에서 4개 suite로 학습한 X-VLA의 성공률이 87.4%에서 91.6%로, π0.5는 93.6%에서 96.2%로 오름. 저자 계산으로 Long 실패의 33%와 41%를 없앴고, 다른 suite에서 성능이 내려간 경우는 없음.
- LIBERO-PRO(물체 위치를 바꾸거나 과제를 바꾼 LIBERO 변형 8개 조건)에서 4개 suite로 학습한 π0.5의 평균 성공률이 32.05%에서 39.33%로 오름. Object-T(LIBERO-Object suite에서 과제 자체를 바꾼 조건)는 25.2%에서 55.8%로 가장 크게 오름. 같은 조건의 X-VLA는 4.95%에서 5.70%로만 오름. 공식 leaderboard와 다른 instruction 입력 방식으로 잰 값임.
- 같은 VLA에 coding agent만 바꾸면 LIBERO-PRO 평균이 달라짐. 4개 suite 학습 π0.5에서 fine-tuning한 Qwen3.5-2B는 39.33%, GPT-6-Astra는 41.50%, GPT-6-Astra에 TAMP 도구를 붙이면 43.00%임. GPT-6-Astra 결과는 조건당 50회 평가라 몇 퍼센트포인트 차이는 경향으로만 봐야 함.
- 양팔 AgileX Piper의 과일 4개 바구니 담기에서 과일 초기 배치 3종을 배치당 10회씩 평가한 합산 성공이 30회 중 11회에서 16회로 늘고, 바구니에 든 과일 수 평균이 2.0개에서 2.8개로 늘어남. 세 번째 배치에서는 성공률이 40%로 같음.

**한계**

성공률만 보고하고, 검사기, atomic VLA, 재시도, 제어 이양 각각의 기여를 떼어 보는 ablation이 없음. 검사기 자체의 정확도와 추가 실행 시간도 본문에서 확인 불가함. 두 VLA가 고정이므로 어느 쪽도 못하는 skill은 복구하지 못하고, base 성공률이 거의 0인 조건(X-VLA의 LIBERO-PRO)에서는 효과가 거의 없음. 실로봇은 배치당 10회이며, 이때 완료 판정은 학습한 검사기가 아니라 GPT-6-Astra와 gripper monitor 규칙으로 함. 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- failure detection과 recovery를 policy 내부가 아니라 프로그램의 분기와 재시도로 분리한 구조임. 고정된 VLA 위에 test-time으로 실패 감지기와 복구 policy를 붙이는 연구의 baseline으로 쓸 수 있음.
- demonstration을 효과가 끝난 시점 기준으로 잘라 skill clip과 완료 label을 함께 만드는 절차는, 우리 실로봇 데이터에서 sub-goal 단위 failure detector를 학습시킬 때 그대로 적용해 볼 수 있음.

*대표 그림: 측정 결과 요약과 방법 구조를 한 장에 묶은 개요 그림으로, 가운데에 coding agent 작성, full-task VLA 실행, 완료 검사, atomic VLA 복구의 순환을 그림. 왼쪽은 기존 VLA, dual system, code-as-policy의 한계를, 오른쪽 막대는 LIBERO, LIBERO-PRO, 실로봇에서 고정된 base 대비 성공률 증가를 보여 줌.*

---

### 4. WorldFailBench: Do World Models Understand Policy Failures? (74점)

[arXiv](https://arxiv.org/abs/2610.33565) · [PDF](https://arxiv.org/pdf/2610.33565) · [alphaXiv](https://www.alphaxiv.org/abs/2610.33565) (요약 있음) · [코드](https://github.com/DAXIAORobotics/WorldFailBench)

- **저자**: Zheng Zhang, Xiaoyang Tang, Shuaiqi Cheng, Jiakai Huang, Zhongbo Wu, Ziyi Zhang, Yuan Si, Zeyu Liu 외 6명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 76점
- **읽은 원문**: PDF 전문

> world model로 robot policy를 평가할 때 성공률만 맞추는지, 실패의 유형·단계·조건까지 맞추는지를 따로 재는 benchmark WorldFailBench를 만듦. world model 7개를 시험한 결과, RoboTwin 실패 경계 비교 420건 중 95.2%에서 장면 변화에 따른 성공률 변화 폭을 실제보다 작게 예측함.

**무슨 문제인가**

world model을 policy 평가기로 쓰는 기존 benchmark(WorldArena, WMBench 등)는 world model 안과 실제 환경에서 잰 policy 성공률의 상관만 봄. 성공률이 맞아도 실패 양상은 다를 수 있음. 실제로는 잡은 물건을 떨어뜨렸는데 world model 안에서는 엉뚱한 물체를 잡으러 가면, 실행 문제를 계획 문제로 잘못 진단하게 됨. 또 world model이 작은 장면 변화에 따른 성공률 하락을 놓치면 policy가 실제보다 robust해 보임.

**어떻게 푸나**

WorldFailBench는 같은 policy, 같은 지시문, 대응되는 초기 조건으로 reference 환경(simulator 또는 실제 로봇)과 world model에서 각각 closed-loop rollout을 돌림. world model은 policy의 action을 받아 다음 관측을 생성해 policy에 돌려주므로, 두 쪽의 action 열은 서로 달라질 수 있음. 실패한 rollout마다 실패 유형(task planning failure: 목표·하위 목표·순서를 잘못 고름, action execution failure: 의도한 하위 목표 수행에 실패함)과 처음 결정적 실패가 난 단계를 붙임. 유형·단계별 실패 빈도의 오차(TFE, SFE)와, policy 간 빈도 차이가 보존되는지 보는 Pearson 상관(TPC, SPC)을 잼. 실패 경계 쌍은 물체 위치·방향·크기 중 하나만 바꾼 인접 장면 쌍 중 reference 성공률 차이가 30퍼센트포인트 이상인 것으로, 플랫폼당 60개를 고정해 씀. 이 쌍마다 변화 방향 정답률(OA: order accuracy)과 변화량 오차(GE: gap error)를 잼. 같은 reference 환경을 다시 돌린 Ref–Ref를 반복 변동의 기준선으로 둠.

**결과**

- RoboTwin(시뮬레이션 양팔 조작 과제 20개, policy 5개)에서 성공률 상관이 가장 높은 DW05(0.597)도 실패 단계 상관 SPC는 0.052임. 7개 모델의 SPC는 -0.123에서 0.095 사이이고, Ref–Ref는 성공률 상관 0.942, SPC 0.903임.
- 같은 RoboTwin에서 planning·execution 실패 빈도의 평균 오차(TFE)가 모델별로 15.9~33.5퍼센트포인트임. Ref–Ref는 6.1퍼센트포인트임. A2World는 planning 실패 상관 0.353, execution 실패 상관 -0.086으로 유형에 따라 부호가 바뀜.
- RoboTwin 실패 경계 60쌍에서 가장 좋은 world model의 OA는 위치 68.5%, 방향 59.0%, 크기 75.8%임. Ref–Ref의 OA는 95~100%임. LIBERO-10(시뮬레이션 단일 팔 장기 조작 과제 10개)에서는 world model의 OA가 0~17.5%에 그침.
- G1 humanoid 실로봇 과제 2개(쓰레기 쓸기, 옷 담기)에서는 가장 정확한 모델이 과제와 지표에 따라 바뀜. A2World의 TPC는 쓸기 과제 0.512, 옷 담기 과제 -0.209임.

**한계**

과제·policy·경계 조건 수가 한정되어 있고, 실패 경계 시험은 시뮬레이션에서만 함. 결과는 각 world model을 benchmark의 관측·action 형식에 맞추는 adapter와 rollout 설정을 포함한 world model 시스템 전체에 대한 것이라 어떤 구조 요소가 차이를 만드는지는 가르지 못함. 실패 label은 영상에서 보이는 행동을 사람이 붙인 것이고, failure fidelity를 높이면 policy 학습이 나아지는지는 보이지 않음.

**누리랩 연구와의 연결**

- world model을 failure detection·diagnosis에 쓰려는 연구에서, 성공률 상관만으로는 world model을 검증할 수 없다는 근거와 바로 쓸 수 있는 지표(TFE, SPC, OA, GE)를 줌.
- 실패 경계 쌍은 장면 조건을 조금 바꿨을 때의 결과를 묻는 시험이라, counterfactual reasoning이나 test-time planning에 쓰는 world model의 예측을 검증하는 데 그대로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 문제를 설명하는 개념도임. 옷 담기 과제의 실제 프레임으로 실패 유형이 다른 경우(A: 천을 놓침 대 바구니를 잡으려 함)와 실패 단계가 다른 경우(B: 배치 대 운반)를 보이고, C는 바구니 위치 변화에 따른 성공률 곡선을 schematic으로 그림.*

---

### 5. OmniBrain-0: A Unified Agentic Model for Embodied Intelligence (74점)

[arXiv](https://arxiv.org/abs/2610.36013) · [PDF](https://arxiv.org/pdf/2610.36013) · [alphaXiv](https://www.alphaxiv.org/abs/2610.36013) (요약 있음) · [프로젝트 페이지](https://public-bots.github.io/OmniBrain-0)

- **저자**: Xiaomi Embodied Intelligence Team, Yuechen Luo, Chong He, Fang Li, Shaoqing Xu, Jingkai Wang, Menglun Su, Jiaxin Liu 외 24명
- **분야**: Embodied AI · robotics relevance 9/10 · 1차 스크리닝 76점
- **학회**: ByteDance 자체 양식 · 근거: 글꼴 ByteSans, 학회 양식 아님
- **읽은 원문**: PDF 전문

> manipulation과 navigation의 skill 호출·진행 추적·실패 복구를 9B 모델 하나에 distillation으로 모은 high-level agent임. LIBERO-Pro 전체 성공률 65.5%로 π0.5(43.8%)를 넘고, 과제당 평균 소요 시간을 GPT-5.6-Sol의 13.8분에서 1.6분으로 줄임.

**무슨 문제인가**

π0.5 같은 VLA나 VLN policy는 개별 skill은 잘하지만, 여러 단계가 얽힌 과제나 분포가 바뀐 상황에서는 과제 단위 성공을 보장하지 못함. 큰 multimodal 모델이 skill을 tool로 부르고 피드백을 보며 계획을 고치는 agent harness 방식은 이 문제를 줄이지만, 매 단계 긴 추론을 하므로 느리고 비쌈. 작은 모델에 이 계획·복구 능력을 옮기려 해도, 고정된 demonstration에는 학생 모델이 실제로 마주치는 실패 상태가 잘 담기지 않음. 또 manipulation과 navigation은 장면·skill 인터페이스·과제 구조가 달라 따로 배운 능력을 한 모델에 합치는 일이 별도 문제로 남음.

**어떻게 푸나**

OmniBrain-0은 Qwen3.5-9B를 high-level planner로 쓰고, 지시·현재 관측·상호작용 기록을 입력받아 매 턴 tool 하나와 그 인자를 출력함. tool에는 perception, VLA 조작(π0.5, LingBot-VLA, RLDX-1), VLN 이동(SmartWay), 자세 제어가 있고 각 tool의 실행 결과가 다음 결정의 입력이 됨. 학습 데이터는 GPT-5.6-Sol과 GLM-5.3-Flash가 같은 harness에서 과제를 푼 기록이며, 실패 없는 성공과 실패 후 회복한 성공만 남기고 같은 행동만 반복한 궤적은 버림. 남긴 궤적의 추론 문장은 Phase·State·Evidence·Decision 네 칸 형식으로 다시 씀. 학습은 세 단계로, embodied VQA와 상호작용 데이터로 공통 base를 만들고, 여기서 manipulation 전문가와 navigation 전문가를 각각 SFT로 만듦. 마지막으로 MOPD(multi-teacher on-policy distillation)로 학생이 스스로 생성한 결정 문장 위에서 해당 도메인 전문가의 token 분포를 reverse KL로 따라가게 해 한 모델로 합침. 추가로 RSI(Rubric-Guided Recursive Self-Improvement)에서는 Meta-Agent(GPT-6.1-Sol)가 성공·실패 기록으로 rubric과 단계별 reminder 문구를 고침. 이어서 검증된 새 궤적으로 전문가를 다시 학습하고 MOPD로 다시 합침.

**결과**

- LIBERO-Pro(LIBERO 4개 suite에 지시 바꾸기와 물체 위치 바꾸기를 건 조작 benchmark, 800 episode)에서 전체 성공률이 65.5%임. 같은 tool을 쓰는 π0.5 단독은 43.8%, 같은 9B backbone의 few-shot agent는 15.6%임. 4B 모델도 62.4%를 기록함.
- 가장 강한 비교 대상인 few-shot GPT-5.6-Sol(experience library 사용)은 78.3%로 여전히 더 높음. LIBERO-Plus(7가지 교란을 넣은 LIBERO)에서는 OmniBrain-0 83.8%, GPT-5.6-Sol 86.2%임. RoboTwin 2.0(양팔 조작 benchmark)에서는 각각 88.2%, 91.2%임.
- RSI 한 바퀴를 돈 모델은 과제당 평균 소요 시간이 늘지 않은 채 LIBERO-Pro 69.3%, RoboCasa365(가정 주방 mobile manipulation 과제 모음) 43.2%로 오름. RoboCasa365에서 RSI 전 모델은 39.6%로 RLDX-1의 36.0%보다 높지만 GPT-5.6-Sol의 52.4%보다 낮음.
- R2R-CE Val-Unseen(연속 환경 언어 지시 navigation, 100 episode 부분집합) 성공률이 65.0%임. DualVLN 64.3%, StreamVLN 56.9%보다 높고 GPT-5.6-Sol 71.0%보다 낮음.

**한계**

low-level skill은 기존 VLA·VLN을 그대로 쓰므로, skill이 못하는 동작은 planner가 고칠 수 없음. 학습 데이터 전체가 closed-source teacher의 궤적에서 나오고, RSI에는 더 큰 Meta-Agent와 judge 모델이 필요함. 비교표의 teacher는 experience library를 쓰고 OmniBrain-0은 쓰지 않아 조건이 같지 않음. 실로봇 실험은 쌓기·사과 놓기·서랍 열기 3개 과제이고, 실로봇 성공률과 reminder ablation 수치는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- 실패 없는 성공과 실패 후 회복한 성공 궤적을 골라 Phase·State·Evidence·Decision 형식으로 학습시키는 방식은 failure detection/recovery를 VLA 위의 planner에 넣는 연구에서 데이터 구성 기준으로 쓸 수 있음.
- Meta-Agent가 단계별 reminder를 고치고 검증된 궤적으로 다시 학습하는 RSI 순환은 language feedback 기반 learning의 비교 대상이 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 위쪽은 embodied pretraining, 도메인별 전문가 distillation, reverse KL 기반 통합의 세 단계이고, 아래쪽은 Meta-Agent가 reminder를 고치고 검증된 궤적을 모아 다시 학습하는 RSI 순환임. 오른쪽 radar chart는 다섯 benchmark에서 baseline, OmniBrain-0, GPT-5.6-Sol의 성공률을 함께 보여 줌.*

---

### 6. RynnVLA-Latent: Scaling Robotic Manipulation Foundation Models with 3D-Grounded Latent Actions (74점)

[arXiv](https://arxiv.org/abs/2610.34356) · [PDF](https://arxiv.org/pdf/2610.34356) · [alphaXiv](https://www.alphaxiv.org/abs/2610.34356) (요약 있음) · [프로젝트 페이지](https://alibaba-damo-academy.github.io/RynnVLA-Latent.github.io) · [코드](https://github.com/alibaba-damo-academy/RynnVLA-Latent)

- **저자**: Haoyu Zhao, Xingyue Zhao, Zhian Su, Bohan Hou, Yinzhou Tang, Fengyi Wang, Kehan Li, Yuming Jiang 외 6명
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: Meta 자체 양식 · 근거: 글꼴 OptimisticDisp, 학회 양식 아님
- **읽은 원문**: PDF 전문

> 로봇 명령이 없는 사람·로봇·시뮬레이션 영상 약 30,100시간에서 3D 장면 움직임과 카메라 움직임을 나눈 latent action을 뽑아 4B VLA를 사전학습함. 사전학습한 policy를 각 로봇 action으로 맞춘 뒤 RoboTwin 2.0 양팔 과제 평균 성공률 88.6%를 얻음.

**무슨 문제인가**

VLA를 키우려면 관측과 언어를 action에 잇는 학습 신호가 많이 필요하지만, 로봇 demonstration은 모으기 비싸고 로봇마다 action의 차원과 좌표계가 다름. 사람 영상과 웹 영상은 양이 많지만 로봇 명령이 붙어 있지 않아 하나의 action 예측 목표로 묶을 수 없음. LAPA 같은 기존 latent action 방법은 두 프레임 사이 변화를 압축해 다음 프레임을 재구성하게 학습함. 이 변화에는 카메라 이동과 겉모습 변화도 섞이므로, 재구성을 잘하는 표현이 저수준 조작 action 예측에도 유용하다는 보장이 없음.

**어떻게 푸나**

RynnLAM(이 논문의 latent action model)은 Depth-Anything-3 위에 만든 encoder로, 두 RGB 프레임을 받아 608차원 descriptor를 냄. descriptor는 국소 motion token 8개(512차원), 전역 action latent(64차원), camera latent(32차원)로 나뉨. motion token은 다음 프레임 feature 자체가 아니라 두 프레임 feature의 차이(residual)를 예측하도록 학습되어 정적인 겉모습보다 변화를 담게 됨. action latent는 추정 depth·camera pose·optical flow로 만든 3D scene flow pseudo-label을 예측하며, 카메라 움직임을 빼고 나면 정적 영역의 flow는 0에 가까워야 함. camera latent는 두 프레임 사이 6-DoF camera pose를 예측함. action latent에는 gradient reversal을 걸어, 같은 pose decoder가 action latent에서 camera pose를 읽어 내지 못하게 함. 이 encoder로 25개 영상 출처를 오프라인 라벨링해 descriptor 745.52M개를 만듦. policy는 사전학습된 VLM인 RynnBrain에 폭이 좁은 action expert를 붙인 구조이며, flow matching으로 descriptor 6개 묶음(chunk)을 예측하도록 사전학습됨. 사전학습에는 로봇 action과 proprioception을 쓰지 않음. post-training에서는 backbone과 action expert를 그대로 쓰고 출력 projection만 각 로봇 action 차원으로 바꾸며 proprioception을 추가함.

**결과**

- LARY(얼어 있는 표현에서 MLP로 end-effector 움직임을 회귀하는 benchmark)의 상대 action 설정에서 4개 데이터셋 평균 MSE가 0.38임. 같은 조건에서 DreamDojo는 0.55, Moto는 0.77, LAPA는 0.93임. 4개 데이터셋 중 CALVIN(언어 지시 조작 시뮬레이션 데이터)에서는 DreamDojo가 0.35로 RynnLAM의 0.40보다 낮음.
- 같은 probe에서 구성 요소를 빼면 평균 MSE가 오름. motion token의 residual 예측을 빼면 0.57, 3D flow를 2D flow로 바꾸면 0.56이 됨.
- LIBERO-Plus(LIBERO 과제에 시점·초기 자세·언어·조명 등 7가지 교란을 건 robustness 평가)에서 추가 적응 없이 4B 모델 총 성공률이 84.7%로 π0.5의 84.4%와 비슷함. 카메라 교란은 72.9% 대 78.4%, 로봇 초기 상태 교란은 64.0% 대 73.6%로 π0.5보다 낮음.
- RoboTwin 2.0(양팔 조작 과제 50개, clean과 randomized 장면 demonstration을 함께 학습하는 Native protocol) 평균 성공률이 88.6%로 LingBot-VLA의 87.7%보다 약간 높음. 실로봇은 양손 dexterous hand 로봇과 바퀴 달린 양팔 gripper 로봇에서 과제 6개를 과제당 35회 평가함. 저자는 비교 방법 중 가장 높은 성공률이라고 보고하지만, 과제별 수치는 제공된 원문 텍스트에서 확인 불가임.

**한계**

사전학습이 영상만으로 되더라도 실행하려면 로봇별 demonstration이 필요하고, 실로봇 6개 과제에 3,850 episode를 모음. 3D flow·depth·camera pose는 모두 추정한 pseudo-label이고, 저자도 카메라 불변성이나 물리적 식별 가능성을 보장하지 않는다고 밝힘. 시뮬레이션 benchmark에서 앞선 폭은 LIBERO 평균 98.8%가 Xiaomi-Robotics-0 대비 0.1퍼센트포인트, LIBERO-Plus가 π0.5 대비 0.3퍼센트포인트로 작음. latent action 사전학습 유무와 데이터 규모에 따른 policy 비교는 제공된 원문 텍스트에서 수치를 확인할 수 없음.

**누리랩 연구와의 연결**

- 3D flow와 camera pose로 latent action을 grounding하는 설계는 사람 영상으로 VLA를 사전학습할 때 카메라 이동이 action 신호에 섞이는 문제를 다룸. 우리 VLA 사전학습이나 world model의 action 조건으로 RynnLAM descriptor를 바꿔 넣어 비교할 수 있음.
- LARY 상대 action probe는 latent action 표현이 정적 자세가 아니라 움직임을 담는지 policy 학습 없이 재는 방법임. 우리가 만드는 object-centric 표현이나 world model latent의 점검 도구로 쓸 수 있음.

*대표 그림: 사전학습 영상 묶음의 구성을 정리한 그림이며, 측정 결과가 아니라 데이터 통계를 보여 줌. 사람 영상 39.64%, 실로봇 39.97%, 시뮬레이션 20.38%의 비율과 데이터셋별 시간(HowTo100M 7,633시간이 가장 많음), 과제 문장의 물체·동작 단어 구름이 담겨 있음.*

---

### 7. Gaussian Episodic Memory for Long-Term Spatiotemporal Reasoning (74점)

[arXiv](https://arxiv.org/abs/2610.33158) · [PDF](https://arxiv.org/pdf/2610.33158) · [alphaXiv](https://www.alphaxiv.org/abs/2610.33158) · [프로젝트 페이지](https://abwerby.github.io/GEMS/)

- **저자**: Ling-Chia Chen, Abdelrhman Werby, Kaan Aytekin, Kai O. Arras
- **분야**: Embodied AI · robotics relevance 8/10 · 1차 스크리닝 83점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 8쪽
- **읽은 원문**: PDF 전문

> 로봇이 같은 공간을 여러 번 방문하며 본 장면을 3DGS 지도 하나에 바뀐 부분만 덧붙여 저장하고, LLM agent가 이 지도에서 원하는 시점·시각의 장면을 다시 렌더링해 보며 질문에 답하게 함. 저자가 만든 실세계 시공간 질의응답에서 LLM judge 점수가 가장 강한 baseline STaR의 44.8%에서 60.9%로 오름.

**무슨 문제인가**

집이나 사무실은 물건이 옮겨지고 서랍이 열리는 식으로 조금씩 바뀌므로, 오래 일하는 로봇은 언제 어디서 무엇이 바뀌었는지 기억해야 함. 기존 시공간 memory 중 3D scene graph 계열은 만들 때 잘라 둔 물체와 속성만 남기므로, 나중에 다른 물체나 세부를 물으면 답할 근거가 없음. 이미지를 저장하는 계열은 시각 정보는 남지만 찍었던 시점에서만 볼 수 있어, 두 방문을 같은 각도에서 비교하기 어려움. 3DGS 기반 memory도 정적 장면 하나만 다루거나 가장 최근 상태만 남겨 과거 상태를 물을 수 없었음.

**어떻게 푸나**

GEMS(Gaussian Episodic Memory)는 첫 방문의 posed RGB-D로 3DGS 지도를 만들고, 이후 방문마다 바뀐 영역만 고쳐 씀. 새 방문의 keyframe 자세에서 이전 지도를 렌더링하고, 실제 관측과의 SSIM 차이와 DINOv3 feature 차이를 합쳐 change mask를 얻음. mask의 각 연결 영역은 렌더링 depth와 관측 depth의 차이로 Add, Remove, Refine 중 하나로 분류되고, 해당 Gaussian만 다시 최적화함. 각 Gaussian은 생긴 방문과 지워진 방문을 담은 수명 구간 [b, d)를 가지므로, 특정 방문의 장면은 그때 살아 있던 Gaussian만 골라 복원함. 질문이 들어오면 LLM planner가 검색, 임의 자세·시각 렌더링, SAM3 분할과 3D 위치 추정 같은 도구를 차례로 불러 근거를 모음. 도구 사용 순서는 finite-state machine으로 제한하고, 모은 근거로 answer synthesizer가 답과 confidence를 냄.

**결과**

- GEMS-Bench(저자가 만든 다회 방문 시공간 질의응답 benchmark, 실세계 3개·합성 12개 장면, 473문항)에서 LLM judge 점수를 잼. 모든 방법이 같은 LLM(Qwen3.5)을 씀. GEMS는 실세계 60.9%, 합성 71.0%이고 가장 강한 baseline STaR(저장한 keyframe·텍스트 설명·물체 point cloud에서 과제에 맞춰 검색하는 memory)는 44.8%, 35.5%임.
- 모든 RGB-D frame을 저장하고 렌더링 도구 없이 같은 agent를 돌린 변형(GEMS-all-images)과 비교함. 합성 장면에서는 GEMS가 71.0% 대 63.8%로 높지만, 실세계에서는 60.9% 대 63.2%로 낮음.
- 렌더링 도구 두 개(time_view: 한 자세에서 여러 방문 시각을 렌더링, relook: 모호한 영역이 잘 보이게 자세를 고쳐 다시 렌더링)를 쓴 245문항을 따로 평가함. 두 도구를 끄면 점수가 65.1%에서 58.5%로 내려감.
- 실세계 장면 하나를 네 번 방문한 뒤 저장량은 GEMS가 1.95 GiB(fp32), 0.98 GiB(fp16)이고, keyframe만 저장하면 2.73 GiB, 전체 frame은 3.94 GiB임. 지도 갱신 한 번은 약 1분으로, depth로 오래된 Gaussian을 지우는 3DGS 갱신 방법 GaME보다 18~26배 빠름. 렌더링 화질(PSNR)은 GaME-Aria 데이터(posed RGB-D 실내 장면 2개)에서 29.23dB로, RGB만으로 변화를 찾아 갱신하는 O-SCD의 32.32dB보다 낮음.

**한계**

실세계 장면에서는 학습 궤적에서 먼 시점을 렌더링할 때 artifact가 생겨, 이미지를 모두 저장한 변형보다 점수가 낮음. 질의응답 benchmark는 저자가 만든 것이고 채점은 LLM judge에 기대며, 로봇이 이 memory로 행동한 실험은 없음. 입력으로 자세가 주어진 RGB-D를 가정하고, ablation은 두 렌더링 도구를 함께 꺼서 시점 보정과 시간 정렬의 기여를 나누지 못함.

**누리랩 연구와의 연결**

- 3DGS에 Gaussian별 수명 구간을 붙여 과거 장면을 복원하는 방식은 robot memory와 object-centric 3DGS를 잇는 구체적 설계임. scene graph memory와 비교 실험을 할 때 baseline으로 쓸 수 있음.
- 같은 자세에서 두 시각을 렌더링해 비교하는 도구는 failure detection에서 작업 전후 상태 변화를 확인하는 데 바로 옮겨 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 GEMS의 방법 구조를 그린 그림임. 왼쪽은 관측 RGB와 이전 지도 렌더링을 비교해 change mask를 얻고 Add, Remove, Refine으로 Gaussian을 고치는 과정이고, 오른쪽은 LLM planner가 memory 도구로 근거를 모아 답하는 과정임.*

---

### 8. Does VGGT Know What It Does Not Know? (73점)

[arXiv](https://arxiv.org/abs/2610.35806) · [PDF](https://arxiv.org/pdf/2610.35806) · [alphaXiv](https://www.alphaxiv.org/abs/2610.35806) (요약 있음)

- **저자**: Adityan Thirumani Srinivasan, David Nordström
- **분야**: 3D Vision · robotics relevance 6/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> VGGT는 camera pose가 틀려도 이를 알려 주는 uncertainty를 내지 않지만, 고정된 내부 feature에 linear probe를 붙이면 pose 실패를 읽어 낼 수 있음을 보임. 처음 보는 HardMatch 범주에서 실패 예측 ROC-AUC가 VGGT 자체 confidence의 79.7%보다 높은 93.5%임.

**무슨 문제인가**

VGGT 같은 feed-forward 3D reconstruction model은 한 번의 forward pass로 camera와 geometry를 예측함. depth와 point map에는 픽셀별 confidence를 내지만 camera pose에는 uncertainty를 내지 않음. 그래서 SLAM이나 mapping 같은 후속 시스템은 맞는 relative pose와 크게 틀린 pose를 구별하지 못함. 실제로 어려운 이미지 쌍을 모은 HardMatch에서 VGGT는 약 35%의 쌍에서 크게 틀림.

**어떻게 푸나**

VGGT-1B를 fine-tuning 없이 고정하고 이미지 두 장을 한 번에 넣음. 실패 label은 VGGT가 예측한 두 camera로 fundamental matrix를 만들고, 손으로 표시한 대응점의 epipolar 거리 중앙값이 50px를 넘으면 실패로 정함. 입력은 encoder 블록과 두 view를 섞는 aggregator 블록의 token을 이미지별로 평균한 뒤 두 이미지 벡터를 다시 평균한 feature임. 이 feature를 PCA로 128차원으로 줄이고 logistic regression(linear probe)으로 실패 확률을 출력함. 평가는 HardMatch 범주 단위로 묶은 10-fold cross-validation이라 test 범주는 학습에 나오지 않음. 비교 대상은 point-map confidence 같은 VGGT 출력값과, VGGT 출력 전부를 넣고 같은 방식으로 학습한 classifier임.

**결과**

- HardMatch(손으로 대응점을 표시한 어려운 이미지 쌍 903개, 97개 범주)에서 실패 예측 ROC-AUC를 비교함. VGGT point-map confidence 79.7%, VGGT 출력 전부로 학습한 classifier 77.7%, 마지막 global attention 블록의 probe 93.5%임. VGGT가 가장 자신 있어 하는 절반에서도 probe가 90.0%, confidence가 69.9%임.
- 블록별로 probe를 붙이면 이미지별 encoder에서는 65.2%를 넘지 않음. aggregator 10번 블록까지 63~66%에 머물다가 12번 블록에서 81%, 15번 블록에서 93%로 오르고 마지막 블록까지 93~94%를 유지함. 또 다른 feed-forward 3D reconstruction model인 π3에서도 같은 양상이 보임(마지막 decoder 블록 probe 91.7%, 자체 confidence 62.2%).
- probe가 가장 믿는 절반만 남기면 남은 쌍의 실패율이 3.8%임. VGGT confidence로 고르면 12.4%임.
- 재학습 없이 PhotoTourism(관광지 사진 쌍)의 15도 넘는 rotation 실패에 적용하면 ROC-AUC 97.5%로 confidence 90.6%보다 높음. 거의 겹치지 않는 쌍만 따로 봐도 probe가 89.5%로, 정답 co-visibility(두 이미지가 겹치는 정도)를 실패 예측에 쓴 75.7%보다 높음.

**한계**

ScanNet-1500(실내 이미지 쌍 1,500개)에서 두 카메라 사이 거리가 짧은 쌍의 translation 방향 실패에는 HardMatch probe가 44~48%로 옮겨 가지 않고, ScanNet에서 따로 학습해야 함. 16개 view를 넣으면 실패 자체가 드물어지고, probe로 view graph의 edge(이미지 쌍)를 걸러도 rotation averaging 오차는 거의 그대로임. 실험은 VGGT와 π3 두 모델뿐이고 probe 학습에는 실패 label이 필요함. 코드는 공개 예정이라고만 적혀 있음.

**누리랩 연구와의 연결**

- 고정된 3D foundation model의 중간 feature에서 실패 신호를 linear probe로 읽는 방식은 VLM·VLA backbone의 failure detection에 그대로 옮겨 볼 수 있음. 로봇이 다른 view를 요청하는 active perception의 판단 기준으로도 쓸 수 있음.
- 실패 신호가 view를 섞는 중간 블록에서 갑자기 생긴다는 층별 분석은, VLA 내부에서 실패 신호가 어디서 생기는지 찾는 실험의 설계 예시가 됨.

*대표 그림: HardMatch 이미지 쌍 다섯 개에서 위는 첫 이미지의 대응점, 아래는 VGGT 예측 camera로 그린 epipolar line을 보여 줌. 각 쌍 아래에 VGGT confidence 백분위, probe 실패 확률, epipolar 오차 중앙값이 적혀 있고, 자신 있게 틀린 세 쌍은 probe가 잡고 한 쌍(e)은 놓친 사례임.*

---

### 9. OSWAM: An Effective World Action Model with One-Step Action Generation (72점)

[arXiv](https://arxiv.org/abs/2610.35850) · [PDF](https://arxiv.org/pdf/2610.35850) · [alphaXiv](https://www.alphaxiv.org/abs/2610.35850) (요약 있음) · [프로젝트 페이지](https://gwenzhang.github.io/OSWAM)

- **저자**: Guowen Zhang, Liyi Chen, Xu Hu, Pengfei Wang, Jingfan Chen, Chenhang He, Lei Zhang
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 76점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> video DiT 기반 world action model이 action을 만들 때 Gaussian noise 대신 현재 관측으로 만든 action prior에서 출발하게 해서, action denoising을 10단계에서 1단계로 줄임. NAVSIM에서 10단계 SimWAM(Fast-WAM 구조를 주행에 옮긴 WAM)과 같은 PDMS 90.3을 내면서 H20 GPU 지연 시간을 410ms에서 136ms로 줄임.

**무슨 문제인가**

Fast-WAM 같은 direct-policy WAM(world action model)은 video 예측을 학습 신호로만 쓰고 추론 때는 미래 video를 만들지 않아서 빠름. 그러나 action은 여전히 flow matching으로 noise에서 10단계쯤 denoising해서 만들어야 하고, 이것이 남은 지연 시간의 대부분임. denoising을 1단계로 줄이면 Fast-WAM의 성능이 NAVSIM에서 약 20%, RoboTwin에서 약 40% 내려감. 저자는 그 원인을 Gaussian noise에 action의 시간적·물리적 구조가 없기 때문이라고 해석함. step distillation이나 rectified flow 같은 기존 few-step 기법도 Gaussian noise에서 출발하므로 이 구조를 채워 주지 못함.

**어떻게 푸나**

OSWAM(One-Step World Action Model)은 Wan2.2-5B video DiT와 그보다 작은 Action DiT를 shared attention으로 묶은 Fast-WAM 구조를 그대로 씀. 여기에 video DiT 입력으로 두 종류의 imagination token을 추가함. AIT(Action Imagination Token)는 action noise를 encoding한 token이고, 현재 frame의 visual token과 attention을 주고받은 뒤 AIT decoder를 거쳐 action prior가 됨. SIT(Scene Imagination Token)는 장면 문맥을 모아 AIT에 넘기는 보조 token이며, AIT를 거쳐서만 간접적으로 학습됨. action prior에 σ=0.5 수준의 noise를 다시 섞고, Action DiT가 한 번의 update로 최종 action chunk를 냄. 학습 때는 미래 frame 전체를 보는 teacher의 AIT feature를 student AIT에 맞추는 privileged-information distillation을 더함. 추론 때는 teacher를 버리고 현재 frame, 언어 지시, 주행이면 ego state만 입력으로 씀.

**결과**

- NAVSIM(실제 주행 로그 기반 계획 benchmark)에서 1단계 Fast-WAM을 baseline으로 구성 요소 ablation을 함. PDMS(NAVSIM 주행 점수: 충돌·주행 가능 영역·진행·충돌까지 남은 시간(TTC)·승차감을 곱하고 더한 값)가 AIT만 넣어도 71.04에서 89.81로 오름. distillation을 더하면 89.96, SIT를 더하면 90.28임. RoboTwin Clean 성공률도 AIT로 57.38%에서 87.42%로 오름.
- NAVSIM에서 PDMS는 10단계 SimWAM과 같은 90.3임. H20 GPU 지연 시간은 410ms에서 136ms로 줄어 3.01배 빠름. 같은 조건의 1단계 SimWAM은 68.9임.
- RoboTwin 2.0(양팔 조작 과제 50개 시뮬레이션)에서 평균 성공률은 90.00%로, 10단계 Fast-WAM의 91.83%보다 1.83퍼센트포인트 낮음. 지연 시간은 397ms에서 142ms로 줄어듦. RTX 5090에서 torch.compile을 쓰면 40.81ms까지 내려감.
- PiPER 로봇팔 실험(과제 2개, 과제당 demonstration 50개, 과제당 20회 평가)에서 성공률은 빵을 그릇에 넣기 85% 대 80%, 지우개를 서랍에 넣기 80% 대 75%로 Fast-WAM보다 조금 높음.

**한계**

조작 실험은 대부분 시뮬레이션이고 실로봇은 과제 2개, 과제당 20회뿐이라 5퍼센트포인트 차이를 우위로 보기 어려움. teacher noise 수준 ablation에서 미래 frame을 깨끗하게 넣은 경우(90.20)와 완전한 noise로 바꾼 경우(90.16)의 PDMS가 거의 같음. 그래서 distillation 이득이 미래 정보에서 온다는 저자 설명은 실험으로 확인되지 않음. 원문 1쪽에 Code 표기가 있으나 저장소 주소는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- VLA나 world model 기반 policy의 action head를 1단계로 줄이는 방법이라, test-time optimization에서 여러 후보 action을 rollout해 고를 때 후보 생성 비용을 줄이는 데 쓸 수 있음.
- 미래 관측을 보는 teacher를 학습 때만 쓰고 추론 때 버리는 privileged distillation 구조는 manipulation policy에 world model 지식을 옮기는 비교 대상이 됨.

*대표 그림: OSWAM 전체 구조를 그린 개념도로, 측정 결과가 아니라 방법 구조를 그린 그림임. 왼쪽 Action DiT, 가운데 AIT·SIT token, 오른쪽 video token이 attention으로 이어지고, Action·Auxiliary·Feature Distillation·Video Latent loss가 어디에 걸리는지 표시됨.*

---

### 10. MemVLN: Streaming Episodic Memory for Vision-Language Navigation (72점)

[arXiv](https://arxiv.org/abs/2610.35066) · [PDF](https://arxiv.org/pdf/2610.35066) · [alphaXiv](https://www.alphaxiv.org/abs/2610.35066) (요약 있음) · [프로젝트 페이지](https://memvln.github.io/)

- **저자**: Yan Wang, Jiangyong Huang, Siyuan Huang, Baoxiong Jia
- **분야**: Navigation · robotics relevance 8/10 · 1차 스크리닝 78점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> streaming VLM 기반 VLN agent에 크기가 고정된 episodic memory를 붙이고, memory만 보고 지나온 경로를 설명하게 하는 보조 과제로 그 memory를 학습시킴. 공식 R2R/RxR 궤적만 쓰는 조건에서 RxR-CE 성공률을 직전 최고 방법 JanusVLN의 51.4%에서 55.4%로 올림.

**무슨 문제인가**

VLN(vision-language navigation)은 agent가 언어 지시를 따라 3D 환경을 이동하는 과제임. 최근 VLM 기반 방법은 단안 RGB 영상을 매 step 받는 streaming 방식을 주로 쓰는데, 긴 경로에서는 오래전에 지나친 landmark나 출발 지점을 기억해야 함. 지나온 영상을 모두 VLM 입력에 넣으면 context 길이와 계산량이 경로 길이에 따라 늘어남. RNN hidden state 방식은 담을 수 있는 정보가 적고, panorama나 topological map에 묶인 explicit memory는 단안 streaming 입력에 바로 쓰기 어려움.

**어떻게 푸나**

MemVLN은 Qwen3-VL-4B에 memory module과 고정된 StreamVGGT geometry encoder(영상에서 3D 기하 특징을 뽑는 사전학습 모델)를 붙인 구조임. 매 step 현재 프레임의 visual feature를 timestep, 상대 pose와 함께 memory bank에 넣음. 상대 pose는 지금까지 실행한 discrete action을 누적해 계산하며, 정답 pose나 외부 odometry는 쓰지 않음. bank가 100칸을 다 채우면 patch 평균 cosine similarity가 가장 높은 이웃 두 프레임을 하나로 합침. memory perceiver는 ToMe(token merging)로 프레임당 patch 수를 줄인 bank 특징에 learnable query로 cross-attention을 걸어 memory token 300개를 만듦. 이때 bank 특징과 query 모두에 timestep과 상대 pose의 embedding을 더함. VLM은 memory token, 최근 최대 16프레임, 현재 프레임, 지시문을 입력받아 다음 action(전진 25/50/75cm, 좌우 회전 15/30/45도, 정지)을 텍스트로 출력함. 학습에서는 navigation과 함께 trajectory summarization을 보조 과제로 둠. 최근·현재 프레임 token을 모두 가리고 memory token만 보고 원래 지시문을 복원하게 함. FGR2R(R2R 지시문을 하위 지시문과 대응 waypoint로 나눈 annotation)으로 궤적을 잘게 나눠 여러 시간 단위의 요약도 함께 학습시킴.

**결과**

- RxR-CE Val-Unseen(긴 지시문을 따라 연속 환경을 이동하는 benchmark)에서 성공률이 JanusVLN의 51.4%에서 55.4%로 오름. nDTW(정답 경로와의 궤적 유사도)는 59.1에서 64.6으로 오르고, 도착 오차는 6.46m에서 5.59m로 내림. R2R-CE(R2R 지시문을 연속 환경에서 따라가는 benchmark)에서는 성공률이 52.8%에서 55.0%로 오름. 도착 오차는 MemVLN 5.19m, JanusVLN 5.17m로 비슷함. 두 비교 모두 공식 R2R/RxR 궤적 외 추가 학습 데이터가 없는 방법끼리 비교한 것임.
- 구성요소 ablation에서 memory만 더하면 RxR 성공률이 48.8%에서 53.3%로 오름. memory와 geometry를 쓴 모델에 summarization 보조 과제를 더하면 R2R 성공률이 49.7%에서 55.0%로 오름.
- 지시문의 쉼표·마침표가 10개를 넘는 RxR episode 1,498개에서 성공률이 base 40.5%, memory 추가 46.5%, 전체 MemVLN 49.1%로 오름. 되돌아가기 지시가 있는 episode 1,272개에서는 43.2%, 50.9%, 52.8%임.
- Unitree G1 실로봇에서 한 장소의 held-out 지시 6개를 5회씩 실행함(30회). 성공률이 base VLM 16.7%(5/30)에서 MemVLN 40.0%(12/30)로 오름. 같은 장소 demonstration 24개로 post-training하면 46.7%(14/30)가 됨.

**한계**

실로봇 평가는 한 장소의 지시 6개뿐이고, MemVLN과 post-training 모델 모두 충돌률이 46.7%로 높으며 다른 장소로의 일반화는 시험하지 않음. RxR에서는 geometry만 더한 모델의 성공률(56.3%)이 전체 모델(55.4%)보다 높아, memory와 보조 과제의 이득이 R2R만큼 뚜렷하지 않음. bank 정리와 memory 읽기가 지시와 무관하게 동작해 긴 episode에서 필요한 관측을 버릴 수 있고, RTX 4090에서 정책 latency가 503.2ms에서 691.0ms로 늘어남.

**누리랩 연구와의 연결**

- 경로 길이와 무관하게 token 수가 고정된 episodic memory를 VLM policy 입력에 넣는 설계임. robot memory 연구에서 KV cache 방식(JanusVLN)이나 MemoryVLA와 함께 비교 대상으로 쓸 수 있음.
- 현재 관측을 가리고 memory만으로 지나온 과정을 언어로 복원시키는 보조 과제는 long-horizon manipulation VLA의 memory 학습이나 failure diagnosis용 과거 요약에 옮겨 시험해 볼 수 있음.

*대표 그림: 논문 첫 그림으로, 왼쪽은 복도에서 sink까지 가라는 지시를 받은 G1 휴머노이드와 점선 경로를 보여 줌. 가운데는 token 압축 memory, KV buffer memory와 저자의 latent episodic memory(memory bank에서 perceiver가 memory token을 뽑는 구조)를 비교한 개념도임. 오른쪽 막대그래프는 RxR에서 base 대비 성공률 49 대 55, 도착 오차 6.9m 대 5.6m를 보여 줌. 지시 유형별 base 대비 성공률 상승폭도 함께 나타내며, 되돌아가기 지시 episode에서 최대 9.7퍼센트포인트임.*

*영상: [저자 프로젝트 페이지에 올라온 RxR 시뮬레이션 navigation rollout 영상임.](https://blog-media.assets.alphaxiv.org/videos/01a18007-0488-798f-b6ca-44b5f813caa8/27787008-729f-4009-92d5-a67c20cf9bfb) (alphaXiv 요약에서 가져옴)*

---

### 11. VaLoP: Value Gradient Lookahead and Pullback for Reward-Guided Diffusion (72점)

[arXiv](https://arxiv.org/abs/2610.35607) · [PDF](https://arxiv.org/pdf/2610.35607) · [alphaXiv](https://www.alphaxiv.org/abs/2610.35607) (요약 있음) · [프로젝트 페이지](https://real-lab-gist.github.io/valop)

- **저자**: Kwanyoung Kim
- **분야**: Generative Models · robotics relevance 7/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> VaLoP은 reward guidance에서 value gradient를 현재 noisy state가 아니라 한 sampler step 앞의 덜 noisy한 state에서 읽고, generator를 거쳐 현재 state로 되돌림. critic으로 SmolVLA를 guide하면 LIBERO 세 suite 평균 성공률이 base 61.4%에서 67.0%로 오름(VaLoP-Fast).

**무슨 문제인가**

Reward guidance는 학습된 diffusion·flow model을 고정한 채 매 step마다 value function(현재 noisy state에서 기대되는 최종 reward)의 gradient를 더해 출력을 reward가 높은 쪽으로 이끄는 방법임. 이 gradient는 보통 두 방식으로 추정함. 하나는 한 번에 denoise한 추정치에서 reward를 미분하는 DPS(diffusion posterior sampling)이고, 다른 하나는 StitchVM처럼 noisy state를 입력받는 value model을 학습하는 방식임. 두 추정 모두 noise가 큰 초기 step에서 가장 부정확한데, 샘플의 큰 구조와 어느 mode로 갈지는 바로 이 구간에서 정해짐. 저자는 두 오차가 모두 clean sample에 대한 posterior covariance의 형태임을 이론으로 보임. 그래서 clean sample의 불확실성이 큰 높은 noise 구간에서 두 오차가 함께 커짐.

**어떻게 푸나**

VaLoP(Value Gradient Lookahead and Pullback)은 현재 state z_t에서 deterministic sampler step 하나를 밟아 덜 noisy한 lookahead state z_s를 만듦. value model을 z_s에서 평가해 gradient를 얻고, 이를 sampler step의 Jacobian으로 z_t까지 되돌림(pullback). 되돌릴 때 붙는 보정 항은 generator velocity에 대한 vector-Jacobian product(VJP) 하나로 계산함. lookahead 비율 s/t가 1이면 기존 learned-value guidance, 0이면 DPS 형태가 되므로 두 기존 방법이 한 family의 양 끝이 됨. 이미지 실험에서는 비율 sweep을 거쳐 s=0.6t를 씀. VaLoP-Fast는 매 step의 VJP를 없애려고, generator와 value model을 고정한 채 보정 항을 예측하는 작은 head를 학습함. 보정 항은 reward가 아니라 generator에 따라 정해지므로, 이미지 모델에서는 HPSv2(사람 선호를 예측하는 이미지 점수, 높을수록 좋음) value로 학습한 head 하나를 다른 reward에도 그대로 씀. 로봇에서는 lookahead state를 denoise한 action chunk에 과제별 critic을 적용하고, VaLoP-Fast의 과제별 head가 guidance 전체를 예측함.

**결과**

- SD3.5-Medium(text-to-image 생성 모델)으로 DrawBench prompt 200개의 이미지를 만들며 HPSv2로 guide함. HPSv2가 unguided 0.286, DPS 0.361, DPS + StitchVM 0.366, VaLoP 0.382, VaLoP-Fast 0.387임. generator 3개와 reward 3개를 조합한 9개 설정 모두에서 VaLoP의 target reward가 두 baseline보다 seed 간 표준편차 이상 높음.
- 보정 항의 효과를 따로 잼. 같은 이미지 설정(seed 하나)에서 HPSv2는 VaLoP 0.382, lookahead 없음 0.358, lookahead만 하고 보정 항 없음 0.365임. SmolVLA를 guide한 LIBERO(시뮬레이션 조작 benchmark)에서도 보정 항이 없으면 Goal·Spatial·LIBERO-10 성공률이 76.6%·67.0%·46.4%로, lookahead가 없을 때(79.0%·69.0%·47.4%)보다도 낮음.
- 비교 대상 중 QGF·AGF는 critic gradient로 action sampling을 조정하는 기존 guidance 방법임. 과제당 50 episode로 잰 SmolVLA의 LIBERO 세 suite 평균 성공률이 base 61.4%, 가장 강한 baseline인 QGF·AGF 65.7%, VaLoP-Fast 67.0%임. π0.5의 RoboCasa365(대규모 조작 시뮬레이션 benchmark) atomic 과제 18개에서는 base 44.6%, QGF 47.1%, VaLoP와 VaLoP-Fast 47.4%임.
- H100 한 장에서 SD3.5-Medium 1024×1024 이미지 한 장 생성 시간이 VaLoP-Fast 15.4초, DPS + StitchVM 17.8초, VaLoP 30.4초임. SmolVLA의 action chunk 하나당 시간은 VaLoP-Fast와 AGF가 0.460초, VaLoP가 2.048초임.

**한계**

로봇 실험은 모두 시뮬레이션이고 실로봇 결과는 없음. 가장 강한 baseline과의 성공률 차이도 LIBERO 평균 1.3퍼센트포인트, RoboCasa 0.3퍼센트포인트로 작음. 방법은 미리 학습된 value model이나 과제별 critic에 기대며, 이미지 ablation은 seed 하나로 잰 값임.

**누리랩 연구와의 연결**

- 고정된 VLA를 다시 학습하지 않고 critic gradient로 action sampling을 조정하는 test-time optimization 방법임. π0 계열 flow policy에 critic guidance를 붙이는 연구에서 lookahead와 pullback을 바로 비교 대상으로 쓸 수 있음.
- noise가 큰 초기 step에서 value 추정이 부정확하다는 분석은, denoising 도중에 critic이나 failure detector를 읽을 때 어느 noise level에서 읽을지 정하는 근거가 됨.

*대표 그림: 측정 결과를 담은 그림임. (a)는 2차원 mixture toy에서 각 방법의 샘플과 target 분포와의 MMD²를 보이며, VaLoP가 0.084로 DPS 0.180, StitchVM 0.263, AGF 0.377보다 낮음. (b)는 noise level별 exact value gradient와의 cosine으로, 가장 높은 noise 구간에서 VaLoP만 0.9 이상을 유지함. (c)는 SD3.5-Medium에서 guided step 하나의 HPSv2 gain이며, VaLoP는 중간 noise에서 가장 크고 DPS·StitchVM은 높은 noise에서 낮음.*

---

### 12. What Does World Modeling Actually Improve in Robot Action Learning? (71점)

[arXiv](https://arxiv.org/abs/2610.34593) · [PDF](https://arxiv.org/pdf/2610.34593) · [alphaXiv](https://www.alphaxiv.org/abs/2610.34593) (요약 있음)

- **저자**: Hanwen Cui, Yuanyuan Li, Qing Guo, Zhida Zhang, Chao Chen, Xi Chen, Jie Cao
- **분야**: World Action Model · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> World Action Model(WAM)에서 미래 영상 예측 loss만 켜고 끄는 통제 실험으로, 이 loss가 익숙한 과제의 실행은 크게 올리지만 처음 보는 과제나 바뀐 환경으로는 일관되게 옮겨 가지 않음을 보임. OpenWAM의 학습 과제 10개 평균 성공률이 7.00%에서 79.91%로 오름.

**무슨 문제인가**

World Action Model(WAM)은 로봇 action과 함께 미래 장면 영상을 예측하도록 학습한 policy임. GR-1, PAD 같은 선행 연구는 이런 예측 학습이 성공률을 올린다고 보고했지만, 대부분 구조와 학습 설정이 함께 바뀐 전체 시스템끼리 비교함. 그래서 예측 loss 자체가 실행 행동의 어디를 바꾸는지, 그 이득이 새 과제와 새 환경에서도 남는지는 성공률 하나로 알 수 없었음. 이를 가려야 이후 VLA 설계에서 예측 loss를 어디에 쓸지 정할 수 있음.

**어떻게 푸나**

저자는 기존에 발표된 두 WAM인 FastWAM과 OpenWAM에서 전체 loss를 action loss에 미래 영상 예측 loss를 λ_video 배로 더한 형태로 두고, λ_video를 0 또는 1로만 바꿈. 구조, 초기화, 학습 데이터, 학습 step은 계열마다 고정하므로 λ_video=0이어도 world model 구조와 시각 표현은 그대로 남음. 학습은 RoboTwin 2.0(양팔 조작 시뮬레이션 benchmark)의 40개 과제, 과제당 demonstration 45개로 함. 학습 과제 평가는 이 40개 중 10개로 하고, 미학습 과제는 학습 데이터에서 뺀 과제임. 평가는 세 가지임. 학습 과제 성공률 비교, 궤적 clustering 분석, 학습 여부와 환경 무작위화를 교차한 네 조건 비교임. clustering 분석은 두 설정의 궤적을 함께 묶은 뒤 cluster 비중과 cluster 안 성공률을 따로 셈. 마지막으로 π0.5에 학습 때만 쓰고 추론 때 떼어 내는 미래 영상 예측 branch를 붙임. branch는 6층 Transformer와 사전학습된 Wan2.2-TI2V-5B DiT 두 가지이며, 둘 다 공유 vision-language 표현만 갱신하고 action expert는 직접 갱신하지 않음.

**결과**

- 학습 과제 10개, 원래 환경, 설정당 3,200회 rollout에서 평균 성공률이 FastWAM은 14.97%에서 39.34%로, OpenWAM은 7.00%에서 79.91%로 오름. OpenWAM은 10개 과제 모두 오르고, FastWAM은 2개 과제에서 약간 내림.
- FastWAM의 stack blocks two 과제에서 가장 큰 궤적 cluster의 비중은 90.4%에서 90.0%로 거의 그대로인데, 그 cluster 안 성공률은 50.2%에서 89.5%로 오름. 이득이 궤적 유형의 선택만이 아니라 비슷한 궤적 안에서의 실행에서도 나타남을 보임.
- 미학습 과제 10개에서 성공률 증가는 FastWAM이 0.28퍼센트포인트, OpenWAM이 23.38퍼센트포인트임. OpenWAM 이득은 open microwave, press stapler, place container plate 3개 과제에 몰림. 무작위화 환경에서는 두 계열 모두 성공률이 3.22% 이하이고 예측 loss를 켜도 오르지 않음.
- π0.5의 학습 과제 10개 평균 성공률이 원래 82.94%에서 6층 Transformer branch로 89.19%, Wan2.2-TI2V-5B branch로 86.97%로 오름. 원래 대비 95% 신뢰구간은 각각 2.31~10.31, 0.16~8.22퍼센트포인트이고, 두 branch 사이 차이의 구간은 0을 포함함.

**한계**

모든 실험이 RoboTwin 2.0 시뮬레이션의 양팔 조작이고 실로봇 실험은 없으며, 본문에서 코드 공개 주소는 확인 불가함. WAM 설정마다 학습은 한 번뿐이라 seed 간 재현성은 확인하지 않았고, 무작위화 환경은 성공률이 0에 가까워 예측 loss의 robustness 효과를 판정할 수 없음. OpenWAM은 예측 loss를 끈 설정의 성공률이 7.00%로 매우 낮아, 이 구조가 원래 영상 loss와 함께 학습되도록 짜인 영향이 섞였을 수 있음. 가벼운 branch도 frozen Wan2.2 VAE latent를 예측 target으로 쓰므로 사전학습 영상 표현이 필요 없다는 결론은 아님.

**누리랩 연구와의 연결**

- world model을 추론 때 planning에 쓰지 않고 학습 때 auxiliary loss로만 쓸 때의 효과와 한계를 같은 구조 안에서 잰 기준점임. VLA에 world model을 붙이는 연구에서 in-distribution 성능과 분포 변화 성능을 따로 보고해야 하는 근거로 쓸 수 있음.
- 궤적 cluster 비중과 cluster 안 성공률을 나누어 보는 분석은, manipulation policy의 failure가 전략 선택에서 오는지 실행 정밀도에서 오는지 가르는 failure diagnosis 도구로 옮겨 쓸 수 있음.

*대표 그림: 논문의 개요 그림으로, (a)는 λ_video를 0과 1로만 바꾼 두 학습 설정의 구조를 그린 도식임. (b)는 stack blocks two에서 cluster 비중 90.4%와 90.0%, cluster 안 성공률 50.2%와 89.5%를 적은 산점도임. 점 위치는 설명용으로 그린 것이고, 적힌 비중·성공률 숫자만 측정값임. (c)는 네 평가 조건별 성공률 차이 막대그래프, (d)는 π0.5 세 변형의 성공률 82.94%, 89.19%, 86.97% 막대그래프임.*

---

### 13. TurboWAM: Learning What Matters for Fast World Action Models (70점)

[arXiv](https://arxiv.org/abs/2610.33941) · [PDF](https://arxiv.org/pdf/2610.33941) · [alphaXiv](https://www.alphaxiv.org/abs/2610.33941) · [프로젝트 페이지](https://turbowam.github.io/)

- **저자**: Guile Wu, Shuangzhi Li, Xingxin Chen, Chengjie Huang, Sam Hosseini, Tongtong Cao, Yingxue Zhang, Dongfeng Bai
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 78점
- **읽은 원문**: PDF 전문

> World action model(WAM: video world model과 action 예측을 함께 학습하는 robot policy)의 action 예측에 world model 앞쪽 24개 층만 쓰고, 층별 합성 가중치와 action gradient를 조정함. LIBERO 평균 성공률 99.0%(Fast-WAM 97.6%)를 내면서 action chunk당 추론 시간을 Fast-WAM의 336.7ms에서 49.7ms로 줄임.

**무슨 문제인가**

WAM은 큰 video 생성 모델로 미래 장면을 반복 denoising해서 만들기 때문에 추론이 느려 실시간 제어에 쓰기 어려움. Fast-WAM은 미래 영상 학습은 학습 때만 하고 추론 때는 미래 영상 생성을 빼서 이 비용을 줄임. Faster-WAM은 여기에 더해 world model 모든 층의 key/value를 학습된 가중치로 합쳐 DiT block 하나짜리 action head에 넣음. 그러나 모든 층을 합치려면 추론 때도 backbone 전체를 돌려야 하고, 저자 분석에서는 층마다 action 예측 기여도가 다르고 denoising step마다 그 기여도가 바뀜. 또 가중합을 거쳐 역전파하면 가중치가 작은 층은 action loss gradient를 약하게 받음.

**어떻게 푸나**

TurboWAM은 현재 관측 이미지, 언어 지시, proprioception을 받아 길이 32의 action chunk를 출력함. 학습 때는 Wan2.2-5B video world model의 모든 층이 미래 관측 latent를 denoising하는 video co-training에 참여하고, action 예측에는 앞쪽 24개 층의 key/value만 씀. 추론 때는 미래 영상을 만들지 않고 앞쪽 24개 층을 한 번만 돌려 key/value를 cache에 두고, 모든 action denoising step에서 재사용함. 층별 합성 가중치는 두 점수를 더해 softmax로 만듦: 현재 noisy action latent의 평균을 투영해 층마다 둔 routing vector와 내적한 점수, 그리고 층마다 학습하는 고정 logit임. action head는 flow matching으로 학습됨. 이렇게 합친 key/value에 action head의 query가 attend해서, noisy action을 갱신할 velocity를 예측함. 학습 때는 각 층이 받는 action gradient를 층 평균 성분과 층별 잔차 성분으로 나누고, 각각 0.25와 0.05를 곱해 다시 합침(gradient modulation). 그 결과 층별 gradient 비중이 합성 가중치 분포와 균등 분포 사이 값이 되고, 이 조정은 학습 때만 적용되어 추론 비용이 늘지 않음.

**결과**

- LIBERO(시뮬레이션 조작 과제 4개 suite, 과제 40개)에서 평균 성공률 99.0%, action chunk당 추론 시간 49.7ms임. Fast-WAM은 97.6%와 336.7ms, Faster-WAM은 98.2%와 76.1ms임. 모든 방법을 같은 GPU 한 장에서 잼.
- RoboTwin 2.0(양팔 조작 과제 50개)에서 평균 성공률 90.5%, 추론 시간 47.1ms임. Fast-WAM은 91.8%와 437.2ms, LingBot-VA는 92.2%와 3328.0ms임. 성공률은 세 방법 중 TurboWAM이 가장 낮지만 추론 시간은 가장 짧음.
- gradient modulation을 빼면 LIBERO-Plus(카메라 시점·조명·배경 등 7가지 교란을 넣은 LIBERO, 추가 학습 없이 평가) 평균 성공률이 78.1%에서 69.2%로 내림. LIBERO에서는 99.0%에서 97.9%로 내림.
- 실로봇(팔 하나, 카메라 2대)에서 과제 3개를 과제당 20개 장면으로 평가함. 평균 성공률이 73.3%로 Fast-WAM 70.0%, Faster-WAM 66.7%보다 높고, 추론 시간은 66.5ms로 Fast-WAM의 358.8ms보다 짧음.

**한계**

성공률 차이는 대부분 이미 높은 LIBERO에서 1퍼센트포인트 안팎이고, RoboTwin 2.0에서는 Fast-WAM보다 낮음. 속도 이득의 상당 부분은 미래 영상 생성을 빼고 key/value를 cache하는 Fast-WAM·Faster-WAM 계열 설계에서 오며, 층 예산 24를 바꾼 실험은 본문에서 확인 불가함. 실로봇 실험은 과제 3개, 과제당 20회이고 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- VLA·world model policy를 실로봇 제어 주기에 맞추는 efficient inference 연구에서 비교 대상으로 쓸 수 있음.
- world model의 어느 층 표현을 action에 넘길지 denoising step마다 다르게 고르는 방식은, world model 내부 표현을 failure detection이나 planning에 재사용할 때 층 선택 근거로 참고할 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. video world model의 DiT block 1부터 m까지의 key/value를 K/V bank에 모아 합친 뒤 action head로 보내는 경로를 초록 화살표로 그림. 미래 관측 생성(video head)과 action supervision 경로는 학습 때만 쓰는 빨간 화살표로 구분함.*

---

### 14. EXE: Egocentric Cross-Embodiment Pretraining via Factorized Latent Actions for VLA Models (68점)

[arXiv](https://arxiv.org/abs/2610.33685) · [PDF](https://arxiv.org/pdf/2610.33685) · [alphaXiv](https://www.alphaxiv.org/abs/2610.33685) (요약 있음)

- **저자**: Qingyuan Cai, Bo Zhang, Yongzhen Huang, Jianyu Chen
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> 사람 1인칭 영상의 손목 3D 위치와 로봇 end-effector 3D 위치만 사람·로봇 공유 codebook으로 묶고, 손가락·gripper 정보는 domain별 codebook에 따로 두어 VLA를 pretraining함. RoboTwin 2.0 평균 성공률을 pretraining 없는 같은 모델의 66.8%에서 76.2%로 올림.

**무슨 문제인가**

VLA 학습에 쓸 로봇 demonstration은 teleoperation으로 모아야 해서 비싸고 장면·과제 다양성이 작음. 사람 1인칭(egocentric) 조작 영상은 많지만, 사람 손(MANO: 손 모양과 손가락 관절을 parameter로 나타내는 사람 손 모델)과 로봇(end-effector pose, gripper)의 action 공간이 달라 바로 맞출 수 없음. UniT처럼 action 전체를 codebook 하나에 넣으면 공유 code에 embodiment별 기하 정보가 섞임. LAPA처럼 영상 frame 변화에서 latent action을 뽑으면 배경·조명 같은 과제와 무관한 정보가 섞임.

**어떻게 푸나**

EXE(Egocentric Cross-Embodiment pretraining)는 세 단계로 학습함. Stage 1의 tokenizer는 action 차원을 고정된 routing table로 두 묶음으로 나눔. 하나는 카메라 좌표계의 손목 또는 end-effector 3D 위치이고, 다른 하나는 손목 회전·손가락 관절 또는 로봇 회전·gripper·손 관절임. 위치 묶음은 사람과 로봇이 함께 쓰는 shared codebook(크기 64, residual VQ)으로, 나머지는 domain별 codebook으로 양자화함. shared codebook에는 정렬 loss 두 개를 더함. 하나는 같은 code에 배정된 사람·로봇 latent를 서로 당기는 InfoNCE임. 다른 하나는 고정된 Qwen3-Embedding-8B로 만든 지시문 유사도를 action latent 유사도가 따라가게 해서, 같은 과제인 사람·로봇 동작을 가깝게 둠(언어는 tokenizer 학습 뒤 쓰지 않음). Stage 2에서는 지시문 뒤에 빈 token(placeholder)을 붙여 이미지와 함께 Florence-2-large VLM에 넣고, 각 placeholder 자리에서 shared code를 예측하게 학습함. 로봇 데이터에서는 로봇 전용 code도 예측함. Stage 3에서는 placeholder 자리의 hidden state(Bridge Feature)를 VLM feature와 함께 action expert에 넣어 연속 로봇 action을 회귀로 학습하고, 배포 때는 tokenizer를 쓰지 않음.

**결과**

- RoboTwin 2.0(ALOHA 양팔 로봇 탁상 과제 50개, 고정 장면 easy와 배경·조명·배치 무작위 hard 두 split)에서 두 split 평균 성공률이 EXE base(같은 X-VLA 구조, Stage 1·2 없음)의 66.8%에서 76.2%로 오름. 대규모 로봇 teleoperation 데이터로 pretraining한 X-VLA는 72.9%임.
- RoboCasa GR1(손가락 있는 humanoid 손으로 하는 가정 과제 24개)에서 평균 성공률이 EXE base 52.0%에서 56.6%로 오름. 같은 pretraining이 gripper와 dexterous hand 모두에 도움이 됨을 보인 비교임.
- RoboTwin 누적 ablation에서 평균 성공률이 기준 73.2%에서 InfoNCE 추가 시 73.8%, 언어 정렬 추가 시 74.1%, Bridge Feature 추가 시 76.2%로 오름. 언어 정렬 기여는 0.3퍼센트포인트로 작고, 가장 큰 상승은 Bridge Feature에서 나옴.
- 실제 AgileX Piper 양팔 로봇의 쓰레기 쓸기 과제 1개(teleoperation demonstration 2,450개로 fine-tuning)에서 조건별 10회 평가함. 학습 때 본 물체·위치에서 성공률이 EXE base 60%에서 EXE 80%로, 처음 보는 물체를 놓은 조건에서 10%에서 30%로 오름.

**한계**

ablation 기준값 73.2%와 본 실험의 EXE base 66.8%가 왜 다른지 본문에 설명이 없어, 성분별 기여와 pretraining 전체 효과를 같은 기준으로 읽기 어려움. 실로봇은 과제 1개, 조건별 10회뿐이고, UniT·LAPA 같은 다른 사람 영상 pretraining 방법과 직접 비교한 실험은 없음. 위치만 공유한다는 분할은 손으로 정한 정적 규칙이며, 사람 손 pose 추정 품질과 카메라 좌표계 정렬에 기댐. 본문에서 코드 공개 주소는 확인 불가함.

**누리랩 연구와의 연결**

- 사람 1인칭 영상을 VLA pretraining에 쓸 때 action을 embodiment 공유 부분과 고유 부분으로 나누는 설계는, 누리랩 VLA·manipulation 연구에서 사람 시연 데이터를 넣을 때 비교 대상으로 쓸 수 있음.
- 언어 embedding 유사도로 action latent 공간을 맞추는 방식은 language feedback 기반 학습과 이어지지만, 이 논문에서 그 효과는 0.3퍼센트포인트로 작아 근거로 쓰기는 약함.

*대표 그림: 측정 결과가 아니라 Stage 1 factorized action tokenizer의 구조를 그린 그림임. 사람 action(102차원)과 로봇 action(20차원)이 각각 shared·specific encoder로 나뉨. 3D 손목과 end-effector 위치는 가운데 shared codebook으로, 회전·관절·gripper는 양쪽의 domain별 codebook으로 가는 흐름을 보여 줌.*

---

### 15. I Won't Know Until I Try: Interactive Information Gathering for Long-Horizon Manipulation (66점)

[arXiv](https://arxiv.org/abs/2610.33959) · [PDF](https://arxiv.org/pdf/2610.33959) · [alphaXiv](https://www.alphaxiv.org/abs/2610.33959)

- **저자**: Linfei Yuan, Rachel Holladay
- **분야**: TAMP · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 8쪽
- **읽은 원문**: PDF 전문

> 겉모습으로 알 수 없는 물체 성질(움직이는지, 펜에 잉크가 있는지 등)을 밀기·써 보기 같은 상호작용으로 확인하면서 계획을 이어 가는 TAMP 방법임. 실행 중 계획이 어긋나면 남은 계획을 버리지 않고 끊긴 부분만 다시 이어, 어려운 용기 과제의 전체 소요 시간을 매번 처음부터 다시 계획하는 방식 대비 약 65% 줄임.

**무슨 문제인가**

긴 조작 과제는 물체가 움직이는지, 서랍이 잠겼는지, 불투명한 용기가 비었는지처럼 보기만 해서는 모르는 성질에 기대는 경우가 많음. 이런 성질은 직접 밀거나 들어 봐야 드러나는데, 그 상호작용이 물체 위치나 로봇 자세도 바꿔 버림. 기존 belief-space TAMP나 정보 수집 계획은 관측 행동이 물리 상태를 바꾸지 않는다고 보는 경우가 많음. 그래서 성질 확인 뒤 남은 계획이 그대로 실행 가능한지, 어긋났을 때 어디서부터 다시 계획할지를 함께 다루는 틀이 필요함.

**어떻게 푸나**

PDDLStream(이산 행동과 grasp·궤적 같은 연속 변수를 함께 푸는 TAMP 프레임워크)을 바탕으로 함. 성질 X마다 CheckedX(확인했는지)와 IsX(결과가 참인지) 두 predicate를 두어 모름, 참, 거짓의 세 상태를 구분함. 확인 행동(push, 시험 필기, 서랍 당기기, 들어서 무게 재기)은 결과가 참이라고 낙관적으로 가정한 effect로 모델링하고, 뒤 행동이 IsX를 precondition으로 가지므로 planner가 확인 행동을 알아서 앞에 넣음. 실행 중에는 매 단계 상태를 관측하고, VALIDATOR가 남은 계획을 앞으로 따라가며 precondition이 성립하지 않거나 충돌이 생긴 행동을 지움. 다음 행동이 바로 실행 불가하면 RECOVERYREPLAN이 현재 상태에서 남은 행동 중 가장 앞선 것의 precondition까지 잇는 짧은 bridge 계획을 찾고, 실패하면 더 뒤 행동을 목표로 삼음. 어느 행동에도 이어지지 않을 때만 처음부터 다시 계획함. 확인 행동 뒤에는 관측 결과로 CheckedX·IsX를 기록하고, 거짓으로 밝혀진 물체는 목표 집합에서 빼는 식으로 goal도 고침.

**결과**

- PyBullet 시뮬레이션의 4개 domain(물체 이동 가능 여부, 펜 잉크, 서랍 열림, 용기 비었는지)을 각각 쉬움(물체 2~3개)과 어려움(4~6개)으로 나눠 조건당 20회 시험함. 비교 대상은 상태가 어긋날 때마다 처음부터 다시 계획하는 Global임. 남은 계획을 재사용하며 실행 중 재계획하는 기존 TAMP 방법 SS-Replan·TAMPER와는 직접 비교하지 않음.
- 두 방법이 모두 성공한 시행에서 제안 방법의 전체 소요 시간이 8개 조건 중 7개에서 Global보다 짧음. 용기 과제(어려움)는 367.49초에서 128.26초로, 물체 이동 과제(어려움)는 902.73초에서 507.94초로 줄어듦. 서랍 과제(쉬움)만 Global이 더 빠름.
- 과제 완료율은 쉬움에서 두 방법이 비슷하고, 용기 과제(어려움)에서 제안 방법 19/20, Global 13/20으로 차이가 가장 큼. 제안 방법이 성공한 152회에서 국소 복구가 실패해 처음부터 다시 계획한 경우는 14번임.
- 용기 과제(쉬움, 10회)에서 실행 중 물체를 옮기거나 집기를 일부러 실패시켜도 10/10 완료함. Franka FR3 실로봇에서는 물체 2개짜리 장면 3개를 영상으로 시연했고 성공률은 보고하지 않음.

**한계**

확인 결과를 결정적으로 보고 확률이나 신뢰도를 다루지 않으므로, 잉크 판별이나 무게 측정이 틀리면 그대로 잘못된 계획이 이어짐. 비교는 자체 Global ablation 하나뿐이고, 실로봇 결과는 정량 평가 없는 시연임. 실로봇에서도 물체 mesh와 category label을 미리 주고 FoundationPose(mesh 기반 물체 6-DoF 자세 추정 모델)로 자세를 추정하는 설정임. 본문에 코드 공개 주소는 없음.

**누리랩 연구와의 연결**

- 실행 중 precondition 위반을 감지하고 남은 계획에 bridge로 다시 잇는 구조는 failure detection·recovery 연구에서 VLA 같은 학습 policy 실행 위에 얹을 수 있는 symbolic 기준선이 됨.
- 행동이 정보도 주고 상태도 바꾸는 상황을 다루므로, active perception을 조작 과제와 함께 계획하는 연구에서 문제 설정과 domain 구성을 참고할 수 있음.

*대표 그림: Franka 로봇팔이 종이 위에 펜으로 선을 그어 잉크가 나오는지 시험하는 실로봇 사진임. 빨간 원과 확대 사진은 그리퍼가 쥔 펜과 종이에 남은 선을 보여 줌.*

---

## 오늘의 흐름

- **world model을 policy 평가와 실패 예측의 도구로 검증함**: world model이 성공률만 맞추는지, 실패의 유형과 조건까지 맞추는지를 따로 재는 연구가 함께 나옴. [WorldFailBench](https://arxiv.org/abs/2610.33565)는 world model 대부분이 장면 조건을 바꿨을 때의 성공률 변화를 실제보다 작게 예측함을 보임. [Video World Models Need Predictable Latents](https://arxiv.org/abs/2610.34663)는 latent 설계를 바꿔, world model 안에서 잰 policy 성공률과 실제 성공률의 상관을 0.21에서 0.67로 올림.
- **World Action Model의 비용과 효과를 따져 봄**: video world model과 action 예측을 함께 학습하는 WAM에서 추론 시간을 줄이는 연구와, world model loss가 실제로 무엇을 올리는지 재는 통제 실험이 나옴. [TurboWAM](https://arxiv.org/abs/2610.33941)은 world model 앞쪽 층만 action 예측에 써서, [OSWAM](https://arxiv.org/abs/2610.35850)은 action denoising을 1단계로 줄여서 지연 시간을 줄임. [What Does World Modeling Actually Improve](https://arxiv.org/abs/2610.34593)는 world model loss를 더하면 학습에 쓴 과제의 성공률은 크게 오르지만 처음 보는 과제나 바뀐 환경으로는 일관되게 옮겨 가지 않음을 보임.
- **실행 policy 위에 실패 감지와 복구를 붙임**: 실행 policy를 다시 학습하지 않고 실행 결과를 검사해 다시 시도하는 구조가 여럿 나옴. [RoboDuo](https://arxiv.org/abs/2610.34108)는 고정된 VLA의 결과를 프로그램으로 검사하고, [OmniBrain-0](https://arxiv.org/abs/2610.36013)은 복구 궤적으로 high-level agent를 학습함. [I Won't Know Until I Try](https://arxiv.org/abs/2610.33959)는 TAMP(task and motion planning) 계획이 실행 중 어긋나면 남은 계획을 버리지 않고 어긋난 부분만 다시 계획함.
- **test time에 model이나 sampling을 고침**: 배포 중에 다시 학습하지 않고 성능을 올리는 방법이 world model과 VLA action sampling 양쪽에서 나옴. [OpTTA](https://arxiv.org/abs/2610.35636)는 planning 비용까지 줄이도록 world model을 갱신함. [VaLoP](https://arxiv.org/abs/2610.35607)는 value gradient를 한 sampler step 앞의 덜 noisy한 상태에서 읽어 VLA의 action sampling을 조정함.
- **memory를 고정된 크기나 3D 지도로 둠**: 지나온 경로나 장면 변화를 저장하는 방식으로 [MemVLN](https://arxiv.org/abs/2610.35066)은 크기가 고정된 episodic memory를 씀. [GEMS](https://arxiv.org/abs/2610.33158)는 Gaussian마다 장면에 존재한 시간 구간을 붙인 3DGS 지도를 씀.

## 해볼 만한 연구

### world model의 실패 예측 정확도와 test-time 적응을 함께 재기

- 질문: 배포 중 world model을 planning 비용 기준으로 갱신하면, 장면 조건에 따른 성공률 변화도 더 정확히 예측하는지 밝힘.
- 첫 실험: RoboTwin(양팔 조작 시뮬레이션 benchmark)에서 물체 조건 하나만 달라 성공률이 크게 갈리는 장면 쌍을 씀. frozen world model, 예측 오차만 줄이는 적응, OpTTA식 적응의 성공률 변화 예측 오차를 비교함.
- 가장 가까운 연구: [WorldFailBench](https://arxiv.org/abs/2610.33565)는 world model을 고정한 채 재기만 하고, [OpTTA](https://arxiv.org/abs/2610.35636)는 planning 성공률만 봄. 이 둘을 같은 실험에서 잇는 것이 다름.

### 고정 VLA 내부 feature로 실패를 감지하고 복구 skill을 부르기

- 질문: 프로그램 검사나 외부 VLM 없이, 고정된 VLA 중간 feature에 붙인 linear probe만으로 sub-goal 실패를 감지할 수 있는지 밝힘.
- 첫 실험: LIBERO-Long(여러 단계로 이어진 장기 조작 과제 모음)에서 π0.5 층별 feature에 linear probe를 학습함. 이 probe와 RoboDuo의 코드 검사를 실패 감지 ROC-AUC와 복구 후 성공률로 비교함.
- 가장 가까운 연구: [Does VGGT Know What It Does Not Know?](https://arxiv.org/abs/2610.35806)는 3D 복원 model VGGT의 camera pose 실패만 다루고, [RoboDuo](https://arxiv.org/abs/2610.34108)는 감지를 코드에 맡김. 감지 신호를 policy 내부에서 읽는 점이 다름.

### Gaussian 3D memory를 manipulation 실패 진단에 쓰기

- 질문: 작업 전후 장면을 3DGS memory에서 같은 시점으로 렌더링해 비교하면, 어떤 물체가 어긋나 실패했는지 VLM이 더 정확히 짚는지 밝힘.
- 첫 실험: 실로봇 정리 과제의 실패 episode에서 GEMS식 memory 렌더링 비교와 현재 이미지 한 장만 주는 경우의 실패 원인 판정 정확도를 비교함.
- 가장 가까운 연구: [GEMS](https://arxiv.org/abs/2610.33158)는 질의응답만 평가했고, [MemVLN](https://arxiv.org/abs/2610.35066)의 memory는 언어 경로 설명에만 쓰임. memory를 실패 원인 판정에 쓰는 점이 다름.

## 꼭 읽을 논문

- [WorldFailBench: Do World Models Understand Policy Failures?](https://arxiv.org/abs/2610.33565): 성공률 상관만으로는 world model을 검증할 수 없다는 근거와, 실패 유형·단계·조건별 예측 지표를 줌.
- [OpTTA: Adapt for Planning, Not just Prediction](https://arxiv.org/abs/2610.35636): 예측 오차가 낮아도 planning이 나아지지 않는 경우를 보이고, test time에 world model을 planning 비용으로 고치는 방법을 줌.
- [RoboDuo](https://arxiv.org/abs/2610.34108): 고정된 VLA 위에 실패 검사와 짧은 복구 skill을 붙이는 구조라 failure recovery 연구의 baseline으로 쓰기 좋음.
- [What Does World Modeling Actually Improve in Robot Action Learning?](https://arxiv.org/abs/2610.34593): VLA에 world model loss를 붙일 때 학습 과제와 분포 변화 성능을 따로 재야 하는 근거가 됨.
- [Video World Models Need Predictable Latents](https://arxiv.org/abs/2610.34663): 적은 denoising step에서도 실제 성공률과 상관을 유지하는 latent 설계라 world model 기반 평가에 바로 쓸 수 있음.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (871편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2610.33158'>Gaussian Episodic Memory for Long-Term Spatiotemporal Reasoning</a></td><td>83</td><td>8</td><td>Embodied AI</td><td>3DGS 지도를 변화 영역만 갱신하고 agentic 추론으로 novel view를 렌더링해 시공간 질의에 답하는 robot memory 연구임</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2610.35636'>Adapt for Planning, Not just Prediction: Optimistic Test-Time World Model Adaptation</a></td><td>82</td><td>9</td><td>World Model</td><td>latent world model을 planning 목적에 맞춰 test time에 optimistic하게 적응시키는 OpTTA로 우선 주제 둘에 정확히 맞음</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2610.33941'>TurboWAM: Learning What Matters for Fast World Action Models</a></td><td>78</td><td>9</td><td>VLA</td><td>world action model의 layer 집계 범위를 제한하고 gradient 분배를 개선해 추론 지연을 줄임. 로봇 policy 효율화에 직결됨</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2610.35066'>MemVLN: Streaming Episodic Memory for Vision-Language Navigation</a></td><td>78</td><td>8</td><td>Navigation</td><td>VLN용 streaming episodic memory임. robot memory와 navigation 직결</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2610.35850'>OSWAM: An Effective World Action Model with One-Step Action Generation</a></td><td>76</td><td>9</td><td>VLA</td><td>noise 초기화에 structured action prior를 넣어 world action model의 one-step action 생성을 노림. 주행·embodied control 대상임</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2610.33565'>WorldFailBench: Do World Models Understand Policy Failures?</a></td><td>76</td><td>9</td><td>World Model Eval</td><td>world model이 policy 실패의 이유, 단계, 경계를 재현하는지 7개 모델로 평가함. LIBERO, RoboTwin, G1 실작업을 포함해 failure 진단과 world model 교차점을 직접 다룸</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2610.36013'>OmniBrain-0: A Unified Agentic Model for Embodied Intelligence</a></td><td>76</td><td>9</td><td>VLA</td><td>manipulation과 navigation을 공유 high-level decision model로 묶는 compact embodied agent OmniBrain-0임. 진행 추적·실패 복구와 multi-teacher on-policy distillation, rubric 기반 RSI data flywheel을 쓰고 LIBERO-Pro/RoboCasa365/RoboTwin2.0/R2R-CE와 실로봇을 평가해 누리랩 주제와 직결됨. 다만 기술 보고서 성격이라 개별 기여 분리가 어려움.</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2610.34108'>RoboDuo: Attempt, Check and Atomic Recovery through Code for Vision-Language-Action Models</a></td><td>74</td><td>9</td><td>VLA Recovery</td><td>coding agent가 full-task VLA를 시도, 완료 검사, atomic VLA로 남은 단계를 복구하는 프로그램을 씀. 가중치 갱신 없이 LIBERO 장기 과제와 실로봇 복구에서 이득을 보여 failure recovery 주제와 직결됨</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2610.34663'>Video World Models Need Predictable Latents</a></td><td>72</td><td>9</td><td>World Model</td><td>로봇 데이터 video world model에서 예측 가능한 latent와 past-conditioned decoder가 같은 예산에서 일관되게 개선함을 보임, 세부 수치는 확인 필요함</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2610.33685'>EXE: Egocentric Cross-Embodiment Pretraining via Factorized Latent Actions for VLA Models</a></td><td>72</td><td>9</td><td>VLA</td><td>egocentric 사람 영상에서 공유 행동과 embodiment 특이 신호를 분리한 latent action으로 사전학습함. 그리퍼와 dexterous hand 모두 RoboTwin, RoboCasa, 실로봇에서 이득을 보여 주제에 부합함</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2610.33959'>I Won&#x27;t Know Until I Try: Interactive Information Gathering for Long-Horizon Manipulation</a></td><td>72</td><td>9</td><td>Active Perception/TAMP</td><td>PDDLStream에 상호작용 정보 수집 행동을 넣고 실행 중 검증과 부분 재계획을 함. 움직임, 잉크, 서랍, 빈 용기 판별을 실로봇까지 보여 active perception 주제와 맞음</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2610.34356'>RynnVLA-Latent: Scaling Robotic Manipulation Foundation Models with 3D-Grounded Latent Actions</a></td><td>72</td><td>9</td><td>VLA</td><td>30.1K시간 영상에서 camera 보정 3D flow로 latent action을 학습해 4B VLA를 사전학습함. LIBERO 98.8%, LIBERO-Plus 84.7%이고 로봇 제어 없는 영상 활용이 핵심이나 scale 의존이 큼</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2610.34593'>What Does World Modeling Actually Improve in Robot Action Learning?</a></td><td>72</td><td>9</td><td>World Action Model</td><td>FastWAM과 OpenWAM에서 미래 영상 loss를 ablation해 성공률이 24.38, 72.91점 오름을 보이고 분포 변화에서는 이득이 일관되지 않음을 밝힘. 통제된 분석으로 world model 주제와 직결됨</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2610.35607'>VaLoP: Value Gradient Lookahead and Pullback for Reward-Guided Diffusion</a></td><td>72</td><td>7</td><td>Generative Models</td><td>diffusion 샘플링에서 value gradient를 한 step 앞에서 평가해 pullback하는 VaLoP를 제안함. critic-guided robot policy에도 적용해 LIBERO와 RoboCasa 최고 성공률을 보고함. inference-time guidance 원리이나 로봇은 부가 실험임.</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2610.35806'>Does VGGT Know What It Does Not Know?</a></td><td>72</td><td>6</td><td>3D Vision</td><td>VGGT frozen feature에 linear probe를 붙여 pose 실패를 ROC-AUC 93.5%로 예측함. 3D 인지 failure detection으로 로봇에 유용함</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2610.33863'>RoboLongR: Causally Consistent Rewards Teach Robots to Progressively Master Long-Horizon Manipulation</a></td><td>70</td><td>9</td><td>Long-horizon RL</td><td>실행 순서에 민감한 history 의존 reward를 stage-shuffle로 학습함. 보지 않은 18개 장기 과제 성공률이 31.8%로 최강 baseline보다 9.2점 높고 실로봇 4개 과제도 57.5%임</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2610.34186'>HuGe: Scaling Humanoid Generalist Vision-Language-Action Models with Egocentric Experience</a></td><td>70</td><td>9</td><td>VLA</td><td>2,000시간 이상 egocentric 사람·로봇 데이터로 humanoid VLA를 3단계 학습하고 pseudo-proprioception으로 격차를 줄임. 기존 VLA 구조 3종을 재사용해 데이터 scale-up 성격이 있으나 실험 범위가 넓음</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2610.36011'>E0.5: From Reconstructive to Future-Predictive 3D Foundations for Robotic World-Action Modeling</a></td><td>70</td><td>9</td><td>World Action Model</td><td>VGGT 같은 3D 모델을 보조 입력이 아니라 world-action model의 주 backbone으로 삼는 방향임. 3D 기하와 world model의 결합이 주제 부합이나 초록 잘려 정량 근거 확인 필요함</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2610.33487'>ReSight: Task-Driven Self-Improving Memory for Embodied Agents</a></td><td>70</td><td>8</td><td>Robot Memory</td><td>keyframe 기반 memory에 coding agent가 탐색 기록에서 도구와 skill을 증류(EDM)해 확장함. FindingDory 성공률 38.3%에서 63.8%로 오르고 실로봇 patrol memory까지 보여 robot memory 주제와 직결됨</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2610.34921'>PhysEvolve: Verifier-grounded Self-evolution for Physical Reasoning with Executable Worlds</a></td><td>70</td><td>7</td><td>Physical Reasoning</td><td>VLM이 실행 가능한 world 프로그램을 제안하고 physics engine이 counterfactual 분기를 만들어 GRPO로 학습하는 PhysEvolve임. ContPhy Goal-Pit 24.4pt 상승 등 counterfactual 물리 추론에 직접 맞고 simulation 검증이 강점임.</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2610.33558'>GeoLift: Grounding Video Spatial Reasoning in Explicit 3D Maps</a></td><td>70</td><td>6</td><td>Embodied AI</td><td>route planning에서 turn 수가 늘면 MLLM이 무작위 수준이 되는 문제를 feed-forward 3D 재구성 map으로 푸는 training-free 방법임</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2610.35604'>RoboDoctor: Training-Free Recursive Self-Improvement for Robot Policies</a></td><td>68</td><td>9</td><td>Failure Recovery/Self-improvement</td><td>정책과 agent 사이 제어 배분, 개입 시점, 방법 개선, 경험 기록을 연결한 training-free 틀임. 가중치 고정 상태에서 실행 피드백으로 적응하는 점이 failure 진단과 맞음. 수치는 초록 잘려 확인 불가임</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2610.33650'>TAD: Distilling Vision-Language-Action Policies from Teacher Trajectories Alone</a></td><td>68</td><td>9</td><td>VLA</td><td>teacher의 action score 없이 joint-position 궤적 feature만으로 discriminator 보상을 만들어 VLA를 on-policy distill하는 TAD임. ManiSkill에서 OpenVLA-OFT 성공률 26.2%에서 76.6%로 오르며 white-box OPD 81.6%에 근접함. 다만 상호작용 5배 소모하고 한 과제·시뮬레이션 평가임.</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2610.33317'>Active Reachability Learning for Humanoid Recoverability Monitoring</a></td><td>68</td><td>8</td><td>Failure Detection</td><td>humanoid 회복 불가능 낙상을 예측하는 recoverability monitor를 uncertainty 기반 active exploration으로 학습함. G1 실로봇 zero-shot 전이까지 보여 failure detection 주제와 직결됨</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2610.33546'>MOON: Learning When to Forget and How to Move On in Vision-and-Language Navigation</a></td><td>68</td><td>8</td><td>VLN</td><td>VLN 이탈 시 history를 지울 시점을 판단하는 judge와 GRPO recovery policy를 frozen policy에 붙임. R2R-CE 성공률 5.2 상승, 지울 시점이 핵심이라는 개입 분석이 설득력 있음</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2610.35385'>EmbodiedLab: Benchmarking Embodied Agents That Act to Know</a></td><td>68</td><td>8</td><td>Embodied Benchmark</td><td>5개 분야 30개 실험에서 로봇이 알기 위해 행동하는 능력을 평가함. 결과를 미리 알 수 없게 resample해 active perception 주제와 맞음. 수치는 초록에서 확인 불가임</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2610.33857'>TrackTok: Object-Centric Video Tokenization with Semantically Persistent Tokens</a></td><td>68</td><td>6</td><td>Video</td><td>object-centric 의미 지속 video tokenization임. object-centric 표현과 연결</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2610.33494'>RBGA: Residual-Budget Guide Arbitration for Offline-to-Online Safe Reinforcement Learning in Dexterous Manipulation</a></td><td>66</td><td>9</td><td>Manipulation</td><td>dexterous manipulation의 offline-to-online safe RL에서 남은 안전 예산으로 guide와 online policy를 중재하는 방식으로 주제에 직접 맞음</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2610.34453'>Scaling Dexterous Manipulation via Action Representation Pretraining</a></td><td>66</td><td>9</td><td>Dexterous Pretraining</td><td>사람 조작 데이터로 action encoder를 사전학습하고 130M 생성 backbone을 얹는 ARPG임. DexJoCo SOTA를 주장하나 표현과 생성 분리 효과의 독립 검증은 본문 확인 필요함</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2610.34251'>Variational Cognitive Memory Abstraction for Long-Horizon Vision-Language-Action Models</a></td><td>66</td><td>9</td><td>VLA</td><td>long-horizon VLA에 variational information compression 기반 latent memory를 붙이는 CogMemory임. 3.45M 추가 파라미터로 여러 VLA backbone에 붙고 robot memory 주제와 직결됨. 초록만으로는 수치와 실로봇 여부를 확인할 수 없고 benchmark 개선 폭이 불명확함.</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2610.34028'>Explaining Navigation Decisions: Stage-Aware Visual Attribution for Vision-Language Navigation</a></td><td>66</td><td>8</td><td>Navigation</td><td>VLN 결정에 대한 단계 인지 시각 attribution임. 설명 가능성과 실패 진단에 연결</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2610.33794'>One Scan is Enough: Demonstration-Free Adaptation for Language-Guided Navigation</a></td><td>66</td><td>8</td><td>VLN</td><td>iPhone 스캔 한 번으로 학습 환경과 지시를 합성하고 closed-form utility로 policy를 적응시킴. 실환경 5곳에서 85% 대 49%로 오르고 미스캔 구역도 82%임. test-time 적응 관점이 좋음</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2610.34105'>X-World: Transferring Video Priors to Variable-View Robot Control</a></td><td>66</td><td>8</td><td>Video Prior Policy</td><td>video diffusion 백본을 1~3 시점으로 확장해 shared action expert에 연결함. LIBERO 98.5%, 이중팔 실과제 81.7%이나 카메라 변화 약점이 있음</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2610.35051'>VISTA: Active Exploration for Self-Improvement in Embodied Agents</a></td><td>66</td><td>8</td><td>Embodied Agent</td><td>harness graph를 두고 meta-agent가 능동 탐색으로 harness를 개선함. rollout 사후 반성에서 자기 탐색으로 넘어간 점이 새로움. 정량 수치는 초록에서 확인 불가임</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2610.35075'>Zero-HLM: Generalizable Humanoid Loco-Manipulation without Real Robot Data</a></td><td>66</td><td>8</td><td>Humanoid Loco-Manip</td><td>스마트폰 캡처에서 real-to-sim 4,800개 시연을 만들어 G1 3개 과제 zero-shot 전이함. GR00T 66.7%로 실데이터 46.7%보다 높고 일반화 설정에서도 23%에서 69%로 오름</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2610.35172'>RetroNav: Scene-Grounded Retrospection and Retry for Self-Evolving Lifelong Navigation</a></td><td>66</td><td>8</td><td>Lifelong Navigation</td><td>훈련 없이 scene memory와 과거 항법 경험을 연결해 실패 후 회고 agent가 재시도 근거를 만듦. memory와 failure 반성 주제에 맞으나 정량 결과는 초록에서 확인 불가임</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2610.35659'>Environment Edits as a Corrective Signal for Reward Learning</a></td><td>66</td><td>8</td><td>Reward Learning</td><td>로봇 움직임을 고정하고 사용자가 장면 물체를 옮기는 환경 편집을 교정 신호로 쓰는 FERRET임. 물체 속성 선호처럼 로봇 교정으로 못 나타내는 feature를 구분함. language feedback류 learning 주제와 맞음</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2610.33658'>Power-of-Two Leaky Integrate-and-Fire Neurons for Event-Driven Vision-Language-Action Inference</a></td><td>66</td><td>8</td><td>VLA</td><td>pretrained π0.5의 projection에 power-of-two 스파이크 뉴런 PoT-LIF를 넣어 event-driven VLA 추론을 구현함. LIBERO 96.90%로 dense 96.70%와 같으면서 산술 에너지 약 86.95% 감소함. 에너지 효율 추론이 새롭지만 시뮬레이션 평가뿐이고 실제 하드웨어 측정 아님.</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2610.34149'>Humans in Space: Can MLLMs Construct Human-Centric Spatial Understanding via Active Exocentric Exploration?</a></td><td>66</td><td>6</td><td>Embodied AI</td><td>MLLM이 능동적 exocentric 탐색으로 인간 중심 공간 이해를 만드는지 평가함</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2610.36022'>Learning and Reasoning with Geometry: How Generation Helps Spatial Understanding</a></td><td>66</td><td>6</td><td>Embodied AI</td><td>생성 모델이 기하 추론으로 공간 이해를 돕는 방식을 연구함</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2610.33868'>RelateGS: Reliable Semantic and Relational Evidence for 3D Scene Understanding with Gaussian Splatting</a></td><td>65</td><td>6</td><td>3D Vision</td><td>3DGS에 신뢰할 만한 semantic·relation 증거를 넣은 장면 이해임</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2610.33589'>Mix Forcing: Causal Pre-Training via Mixture Attention for Interactive World Models</a></td><td>65</td><td>5</td><td>World Model</td><td>interactive world model용 causal 사전학습 mixture attention임</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2610.33718'>RoboJev: An Open Vision-Language Judge for Robot Success Detection</a></td><td>64</td><td>8</td><td>Success Detection</td><td>27B open VLM judge가 SO-101 held-out에서 AUROC 0.993이고 미지 랩 데이터에서 0.890임. 성공 판정과 reward 용도로 유용하나 기반 모델 대비 개선폭이 작음</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2610.34051'>BEHAVIOR-Spatial Benchmark: Evaluating Spatial Understanding for Robotics</a></td><td>64</td><td>8</td><td>Spatial Reasoning</td><td>BEHAVIOR-1K 기반으로 VLM 공간 QA, grounding, VLA 행동을 함께 평가함. 지시 변경 시 성공률 16.1%로 떨어져 공간 지시 수행 평가 필요성을 보임</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2610.35010'>JevVLA: Jev-Inspired Energy-Based Adaptation for Vision-Language-Action Policies</a></td><td>62</td><td>9</td><td>VLA Adaptation</td><td>frozen VLA 위에 행동 선호 energy를 학습해 이산 후보 선택과 연속 행동 gradient 보정에 함께 씀. test-time 보정 관점이 흥미로우나 초록의 정량 결과는 잘려 본문 확인 필요함</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2610.34151'>Execution Logs Sway VLM Judges of Robot Progress</a></td><td>62</td><td>8</td><td>Embodied AI</td><td>VLM judge가 로봇 영상 옆 로그 한 줄에 판정이 10~35퍼센트포인트 뒤집힘을 보여 progress 판정과 failure detection 신뢰성에 직결됨</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2610.34280'>AdaPolicy: Action-Driven Anticipatory Robot Policies via Next-Chunk Prediction</a></td><td>62</td><td>8</td><td>Policy Learning</td><td>다음 action chunk를 cascade로 예측해 미래 관측 없이 foresight를 학습하고 추론 오버헤드가 0임. 단순하고 일반적이나 초록의 실험 결과가 잘려 정량 근거는 본문 확인 필요함</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2610.34519'>TRIAGE: Efficient Vision-Language-Action Inference Needs Both Reuse and Pruning</a></td><td>62</td><td>8</td><td>Efficient VLA</td><td>token drift로 KV 재사용과 pruning 중 무엇이 나은지 가르는 training-free 가속임. drift 이상에서 재사용 오차가 pruning의 최대 4.4배라는 진단이 근거로 설득력 있음</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2610.34649'>RobotAgentBench: Towards Open-world Robot Autonomy</a></td><td>62</td><td>8</td><td>Embodied Benchmark</td><td>50개 가정 환경, 과제 120여 개의 real-to-sim 벤치마크로 task discovery와 recovery까지 평가함. 구성이 넓으나 평가 중심 기여임</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2610.34839'>Behavioural Quality Is Not Learning Utility: Objective Mismatch in Human Behaviour Models for Robot Learning</a></td><td>62</td><td>8</td><td>Human Model/RL</td><td>행동 현실성 지표가 하위 RL 정책 성능을 일관되게 예측하지 못함을 주행과 handover에서 보임. 시뮬 사람 모델 평가 관점에서 통찰이 있음</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2610.35817'>Pretraining Knows What, Simulation Teaches How: Compositional Generalization for Agentic Robotics</a></td><td>62</td><td>8</td><td>Agentic Robotics</td><td>시뮬 primitive 과제와 모델 자체 성공에서 motion skill을 학습하는 ZAP로 실과제 96.7%를 달성함. 실로봇 데이터 없이 GPT-6 Astra에 맞먹는다는 주장이나 harness 의존이고 평가 범위 확인 필요함</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2610.33894'>WMEval: Evaluating Interactive World Models Grounded on Physical Simulations</a></td><td>62</td><td>6</td><td>World Model</td><td>물리 시뮬레이션 기반 interactive world model 평가 벤치마크임</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2610.33802'>ProMo3D: Probing Motion Cues in Frozen 3D Foundation Models</a></td><td>62</td><td>5</td><td>3D Vision</td><td>frozen 3D foundation model에서 motion cue를 probing해 4D 이해에 씀</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2610.33169'>World-in-Context: Interactive Video World Modeling with In-Context Conditioning</a></td><td>62</td><td>4</td><td>World Model</td><td>view·action·camera를 in-context로 조건화한 interactive video world model임. 로봇 직접성은 낮음</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2610.33288'>Tiny Recursive Policy: Recursive Latent Refinement for Visuomotor Control</a></td><td>60</td><td>8</td><td>Manipulation Policy</td><td>persistent latent carry와 재귀 latent refinement를 결합한 소형 BC policy임. LIBERO-Mem 등 장기·문맥 의존 과제에서 이득을 보이고 carry perturbation 분석이 있어 robot memory 주제와 맞음</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2610.33705'>Open-World Law-to-Action: Vision-Language Priors and Touch for Parts with Hidden Physics</a></td><td>60</td><td>8</td><td>Manipulation/Tactile</td><td>VLM prior를 촉각 기반 Bayesian 회귀로 덮어쓰며 관절 부품의 물리를 식별함. 모든 실험이 시뮬이고 held-out 설계가 신중하나 실로봇 검증 없음</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2610.33807'>RoboWorM: Evaluating Movement Realism, Consistency and Acceleration Affects in Embodied Video World Models</a></td><td>60</td><td>8</td><td>World Model Eval</td><td>로봇 기구학 prior로 VLM 없이 움직임 일관성을 재는 KIVA, RIGIS 지표와 1,605 에피소드 벤치마크임. 가속 기법 9종이 물리 제약을 조용히 해침을 보임</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2610.33852'>AdaDexTrack: Dynamic Modulation for Adaptive and Generalizable Dexterous Manipulation Tracking</a></td><td>60</td><td>8</td><td>Dexterous Tracking</td><td>증류된 generalist tracker에 reference, object latent, 목표 위치를 RL로 조절하는 modulator를 붙임. unseen 물체에서 우세하고 zero-shot sim2real 이득이 있음</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2610.35626'>Robot-Aligned 3D Gaussian Splatting for Precise Reaching with Wrist-Camera VLA Policies</a></td><td>60</td><td>8</td><td>VLA/3DGS</td><td>3DGS로 작업 공간을 복원해 robot-aligned wrist 시점을 렌더링하고 reaching 궤적과 짝지어 VLA 적응 데이터를 만듦. 전자폐기물 분해 pre-contact 한정이나 3DGS 데이터 생성 아이디어가 유용함</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2610.33745'>POD-RoPE: Rotary Position Encoding over Physical Observation Distributions for Embodied AI</a></td><td>60</td><td>7</td><td>Representation</td><td>token 관측 footprint를 분포로 두는 RoPE임. Fast-WAM 적용 시 실로봇 성공률 32.5%에서 52.5%로 오르고 4개 policy에서 검증하나 RoboTwin 개선은 1.05점으로 작음</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2610.34126'>HumanoidNDM: Closing the Training-Deployment Gap of Motion Tracking via Humanoid Neural Dynamics Model</a></td><td>60</td><td>7</td><td>Humanoid Adaptation</td><td>실데이터 neural dynamics model의 gradient로 G1 추적 정책을 MoCap 없이 온라인 fine-tuning함. 데이터 효율 있는 sim2real 적응이나 정량 수치가 초록에 없음</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2610.34745'>SceneAgent: An Agentic Pipeline from 3D and 4D Captures to Simulation Environments</a></td><td>60</td><td>7</td><td>Sim Environment</td><td>3DGS, LiDAR, 4D 영상을 시뮬 환경으로 바꾸는 agentic 파이프라인이고 digital sisters와 scripted demo를 생성함. GraspClutter6D에서 F1 60.75% 대 6.9%이나 시스템 조합임</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2610.35852'>DiffContact: Differentiable Contact Dynamics for Policy Learning and Contact-Implicit Trajectory Optimization</a></td><td>60</td><td>7</td><td>Differentiable Contact</td><td>backward만 central-path로 완화해 마찰 접촉의 smooth gradient를 얻고 forward는 hard contact를 유지함. 접촉 모드 사이 gradient가 새롭고 locomotion 정책과 trajectory 최적화에 적용함</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2610.33356'>Tight Learned Event-Inertial Odometry (TLEIO): a Transformer-Based Architecture for End-to-End Motion from Event Streams</a></td><td>60</td><td>6</td><td>3D Vision</td><td>event-inertial odometry를 transformer로 end-to-end 학습함. 로봇 state estimation에 유용</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2610.35044'>DriveUniTok: A Unified Multimodal Tokenizer for Driving World-Action Models</a></td><td>60</td><td>6</td><td>World Model</td><td>주행 world-action model용 통합 멀티모달 tokenizer임</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2610.35563'>High-resolution tactile observation makes hidden racket-control mechanisms learnable</a></td><td>60</td><td>6</td><td>Tactile</td><td>864-node 촉각 glove로 70명 14,000회 스윙을 기록해 숙련 제어 메커니즘을 분석하고 코칭에 적용함, 사람 대상이라 로봇 직접성은 낮음</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2610.33566'>Distilling Dense Trajectory Teachers For Large-Motion Video World Models</a></td><td>60</td><td>5</td><td>World Model</td><td>큰 camera motion video world model을 dense trajectory teacher로 distill함</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2610.33172'>RAIWAY: A Large-Wheeled Bipedal Robot with Contact-Informed Blind Locomotion</a></td><td>58</td><td>8</td><td>Locomotion</td><td>20인치 바퀴 이족 로봇 RAIWAY와 시뮬레이션 접촉 정보를 latent로 증류해 proprioception만으로 추론하는 제어기를 실로봇 계단과 자갈에서 검증함</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2610.33480'>MDPO: Multi-constraint Dexterous Policy Optimization with Reinforcement Learning</a></td><td>58</td><td>8</td><td>Dexterous RL</td><td>누적 비용과 state-wise 제약을 모두 다루는 projection 기반 dexterous 정책 최적화임. ReDMan 시뮬 결과만 있고 실로봇 없음, 안전 RL 관점에서 유용함</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2610.34031'>ElevateHead: Decide Once, Then Commit: When the Action Head Matters for Multimodal Imitation</a></td><td>58</td><td>8</td><td>Imitation Policy</td><td>한 번 결정해 에피소드 동안 mode에 commit하는 action head임. Franka Kitchen 완주 45.2% 대 29.3%이나 다른 과제에서 재현 안 됨, 실로봇 없음이라 솔직한 진단 연구임</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2610.33866'>Late Breaking Results: Audio-Language-Action Models with Direct Speech Conditioning for Robotic Manipulation</a></td><td>58</td><td>7</td><td>VLA</td><td>π0.5에 raw speech를 audio token으로 직접 넣어 ASR 대비 지연 3배 감소, LIBERO 성능 유지함. late-breaking 규모임</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2610.34452'>AuRA: From Atoms to Bits through Autonomous Robot Interaction</a></td><td>58</td><td>7</td><td>Real2Sim</td><td>자율 grasp와 gripper 움직임 측정으로 PhysTwin digital twin 데이터를 수집해 사람 노동을 88.5% 줄임. 변형 물체 13개에서 재구성 지표 대부분 개선함</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2610.34711'>Intervene, Calibrate, Discover: Learning Causal Structure from Pixels</a></td><td>58</td><td>6</td><td>Causal/World Model</td><td>픽셀에서 인과 그래프를 학습하되 개입으로 시각 readout을 보정하고 counterfactual 이미지를 생성함. Pick-and-Place·CausalWorld를 포함해 counterfactual 추론 주제와 맞지만 장난감 환경 중심임.</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2610.33656'>FreeView: Robust 3D Reconstruction from Uncurated Views</a></td><td>58</td><td>5</td><td>3D Vision</td><td>uncurated view에서 feed-forward 3D 재구성을 강건화함</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2610.34093'>LegoOcc++: Towards Consistent Open-Vocabulary 3D Occupancy Prediction</a></td><td>58</td><td>5</td><td>3D Vision</td><td>open-vocabulary 3D occupancy 일관성 개선임. embodied agent 대상</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2610.34845'>PosePlaner: Denoising Any Feed-Forward Pose Predictor from Pairwise Planar Geometry</a></td><td>58</td><td>5</td><td>3D Vision</td><td>feed-forward pose predictor를 pairwise planar geometry로 denoise함</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2610.35203'>OrthoRF: Exploring Orthogonality in Object-Centric Representations</a></td><td>58</td><td>4</td><td>Object-Centric</td><td>object-centric 표현의 orthogonality 탐구임</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2610.34833'>Streaming Recurrent Memory</a></td><td>56</td><td>6</td><td>Memory</td><td>저장 없이 streaming으로 학습되는 recurrent memory SRM을 제안해 robot memory와 온라인 학습에 연결 가능하나 로봇 실험 여부는 확인 필요함</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2610.34893'>MMGNet: Multi-Modal 6-DoF Grasp Synthesis for Cluttered Scenes</a></td><td>55</td><td>8</td><td>Grasping</td><td>이미지 특징을 3D 표현에 계층적으로 주입하고 접근 방향과 회전을 함께 예측함. GraspNet-1Billion AP 60.34로 우세하나 module 추가 수준임</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2610.34837'>Beyond Behaviour: A Stimulus-Response Safety Evaluation of Vision-Language-Action Models</a></td><td>55</td><td>8</td><td>VLA</td><td>VLA 3종의 내부 표현과 행동 경향을 위험 자극에 대해 조사해 위험을 인식하고도 task 수행을 기본 반응으로 유지함을 보임. VLA 안전 주제로 관련 높으나 초록이 짧고 분석 범위가 좁아 보임.</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2610.33446'>MOTIO: Agentic Skill Engineering for Reality-Grounded Humanoid Loco-Manipulation</a></td><td>55</td><td>7</td><td>Humanoid Loco-Manip</td><td>영상과 3D asset에서 agent가 humanoid 프로그램을 만들고 물리 피드백으로 고침. G1 101초 실행과 BC/DAgger 증류를 보이나 사람 승인 의존의 시스템 통합 성격임</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2610.34370'>ThinkLocoManip: A Whole-Body Control Agentic Harness for Legged Loco-Manipulation</a></td><td>55</td><td>7</td><td>Loco-manipulation</td><td>reasoning-acting 교차로 perception, navigation, manipulation, locomotion tool을 조합하는 agentic harness임. locomotion을 tool로 넣은 점이 차별점이나 시스템 통합이고 정량 수치가 초록에 없음</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2610.35576'>Preemptive Instruction Following with Resumption</a></td><td>55</td><td>7</td><td>Embodied Navigation</td><td>긴 항법 중 우선 지시 끼어들기와 재개를 평가하는 PIFR 벤치마크와 간단한 baseline임. 새 문제 설정이나 방법 기여는 작음</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2610.34041'>T-ConSG: A LiDAR-Based Real-Time Temporal Construction Scene Graph for Dynamic and Evolving Environments</a></td><td>55</td><td>6</td><td>Scene Graph</td><td>LiDAR로 free-space, 정적·동적 물체, 설치/제거 이벤트를 담는 시간적 scene graph임. scene graph 주제와 맞으나 건설 현장 응용 중심이고 정량 비교 약함</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2610.34283'>ChronoReplay: One Answer Interface Is Not Enough for Streaming Spatial Intelligence</a></td><td>55</td><td>5</td><td>Embodied AI</td><td>streaming 공간 VLM의 metric 변위 보존 학습임</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2610.35522'>Generative Structure from Motion with Native 3D Diffusion</a></td><td>55</td><td>4</td><td>3D Vision</td><td>native 3D diffusion 기반 generative SfM임</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2610.35001'>More Memory, Better Videos? A Controlled Study of Visual Memory in Long-Video Generation</a></td><td>55</td><td>3</td><td>Video</td><td>long-video 생성에서 visual memory 효과를 통제 연구함. memory 관련 분석</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2610.33241'>ORBIT: A Modular Multi-finger Robotic Hand Platform with Rotational Finger Reconfiguration</a></td><td>52</td><td>7</td><td>Dexterous Hardware</td><td>회전 knuckle로 1초 미만에 손가락 배치를 바꾸는 모듈형 손임. 11개 물체 pilot 파지 비교뿐이라 하드웨어 플랫폼 기여에 그침</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2610.33508'>MimicAll: Structured Embodiment Conditioning for Cross-Humanoid Whole-Body Motion Tracking</a></td><td>52</td><td>7</td><td>Humanoid Tracking</td><td>embodiment descriptor 조건으로 16개 humanoid 계열 4096 변형을 한 policy로 추적함. 464개 body 벤치마크가 있으나 시뮬 중심 motion tracking임</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2610.33778'>RoboReason: Boosting Robotics-Relevant VLM Reasoning Through Scalable Data Generation</a></td><td>52</td><td>7</td><td>VLM Reasoning</td><td>프레임 순서와 깊이 순서 과제에서 VLM이 약함을 보이고 자동 생성 데이터로 SFT와 RL 개선함. 데이터 생성 scale-up 성격이 강함</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2610.34286'>ScheNav: Schematic-Guided Object Goal Navigation</a></td><td>52</td><td>7</td><td>Navigation</td><td>2D 평면도에서 만든 33k 환경과 SchemaField로 도식 지도를 탐색 가치장으로 융합함. 시뮬 학습 기반이고 스케치 지도 활용이 신선하나 실세계 검증 확인 필요함</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2610.34717'>VLA-HWBench: Where the Time Goes When VLA Models Run on Edge Hardware</a></td><td>52</td><td>7</td><td>Efficient VLA</td><td>VLA 18종을 Jetson과 AMD에서 7단계로 지연 분해함. action 생성 방식이 모델 크기보다 지연을 좌우한다는 통찰이 있으나 측정 벤치마크임</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2610.35252'>Labference: Benchmarking the Reasoning-Action Connection in Robotic Laboratories</a></td><td>52</td><td>7</td><td>Benchmark</td><td>실험실 로봇에서 관측된 물리 결과가 이후 선택을 어떻게 바꾸는지 평가하는 벤치마크임. outcome 적응 평가 관점이 있으나 수치는 초록에서 확인 불가임</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2610.35462'>DEX-PHD: A Dexterous Portable Handheld Device for Multimodal Data Collection</a></td><td>52</td><td>7</td><td>Data Collection</td><td>dexterous hand를 단 휴대 장치로 고유수용·접촉·손목 영상을 기록함. 휴머노이드 open-loop replay만 확인해 학습 정책 검증은 없음</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2610.35686'>FISRF: Flexible Instructional Scaffolding Reflection Framework for Robotics Task Planning with Large Language Model</a></td><td>52</td><td>7</td><td>LLM Task Planning</td><td>학습자의 ZPD를 추정해 반성 전략과 mentor 지도를 고르는 agent-mentor 구조임. ALFWorld와 실로봇에서 오류 교정 라운드 37% 감소, 성공률 8점 상승이나 개선폭 작음</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2610.34208'>CORMA: Constraint-Routed Decision Mamba for Generalizable Multi-Constraint Offline Safe Reinforcement Learning</a></td><td>52</td><td>6</td><td>RL</td><td>multi-constraint offline safe RL을 Decision Mamba와 constraint routing으로 푸는 연구로 안전 제어와 이어지나 벤치마크 중심임</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2610.35468'>Multi-Horizon Future Discovery for Physics-Informed Exploration</a></td><td>52</td><td>6</td><td>RL</td><td>multi-horizon temporal contrastive critic과 Hamiltonian 구조로 물리 제어 탐색 보상을 만드는 HTC2로 RL 탐색과 이어짐</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2610.35501'>Learning Scene Coordinate Reconstruction from Unposed Images via Pose Graph Optimization</a></td><td>52</td><td>4</td><td>3D Vision</td><td>unposed 이미지 scene coordinate 재구성을 pose graph로 개선함</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2610.34385'>Outcome-Aware Agents: When Does Causal Structure Help a Forward Model Foresee the Consequences of Actions?</a></td><td>52</td><td>4</td><td>World Model</td><td>action을 do-intervention으로 둔 AC-LSCM이 합성 SCM에서 forward model 예측과 안전 위반을 줄임, 합성 환경만 검증함</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2610.34523'>How Humans Learn Unfamiliar Worlds: A Think-Aloud Dataset on ARC-AGI-3</a></td><td>52</td><td>4</td><td>Embodied AI</td><td>인간 64명의 think-aloud 궤적과 LLM agent 궤적을 ARC-AGI-3에서 비교해 world model 형성·오류 복구 과정을 분석한 데이터셋임. 로봇은 아니나 탐색·복구 분석이 참고됨.</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2610.33777'>InfiniteWorld: Separating Visual Evidence from Familiar Physics</a></td><td>52</td><td>3</td><td>Video</td><td>시뮬레이터 비디오의 물리 파라미터를 바꿔 VLM이 시각 증거를 따르는지 재는 InfiniteWorld 벤치마크임. 법칙 식별·counterfactual 비교를 포함하고 모델이 익숙한 지구 물리 규칙을 고집함을 보이나 평가 벤치마크이고 로봇 정책은 아님.</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2610.34781'>Uncovering the Turing Test&#x27;s Latent Signal: Indistinguishability as a Reward</a></td><td>52</td><td>2</td><td>RL</td><td>teacher가 student 응답을 자기 것으로 오인하는 확률을 RL reward로 써서 정답 없이 Qwen2.5-1.5B를 개선함. 새로운 reward 발상이나 평가가 LLM 4개 도메인에 한정됨.</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2610.34147'>PS-DLO: Property- and Spatially Aware Deformable Linear Object Manipulation Policy</a></td><td>50</td><td>7</td><td>Manipulation</td><td>대조 학습으로 DLO 물성 prior를 주고 SAM3 mask feature를 action expert에 증류함. 실로봇 9개 과제 평균 68.9%로 최강 baseline보다 20.0점 높으나 DLO 특화임</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2610.35103'>The Language of Deformation: Semantic Failure Analysis as a Prerequisite for Dexterous Manipulation of Deformable Objects</a></td><td>50</td><td>7</td><td>Deformable Failure Analysis</td><td>변형 물체 조작에서 의미론적 failure 분석이 선행돼야 한다는 입장과 proof-of-concept임. failure 주제와 맞으나 실험 규모 작음</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2610.35730'>SPECOLA: A Tool for Specification Driven Robot Evaluation</a></td><td>50</td><td>7</td><td>Evaluation</td><td>STL 명세로 성공 여부 이상의 여유와 위반을 재는 Specola 도구임. 평가 방법론 기여이나 학습 방법 아님</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2610.35832'>Profiling a Frontier Agent with EBench: From Direct Control to Harness with Policy</a></td><td>50</td><td>7</td><td>Agent Evaluation</td><td>GPT-6-Astra를 직접 제어와 VLA·WAM 호출 구성으로 EBench에서 평가함. 단기 과제에 강하다는 프로파일링 보고임. 평가 중심이고 한 모델 기준임</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2610.34674'>Benchmarking Obstacle-Conditioned Safety in Household Robot Navigation</a></td><td>50</td><td>6</td><td>Navigation Benchmark</td><td>장애물 종류만 다른 시나리오로 VLM·VLA가 안전 순서를 움직임에 반영하는지 SSI로 잼. 인식은 맞으나 행동에 반영 못 함을 보인 평가 연구임</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2610.35312'>OVM-Occ: Open-Vocabulary Monocular Occupancy Prediction via Geometry-Aware Vision-Language Distillation</a></td><td>50</td><td>5</td><td>3D Vision</td><td>실내 open-vocabulary 단안 occupancy 예측임</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2610.34473'>PhysCreator: Creating Physically-Attributed 3D Assets at Will</a></td><td>50</td><td>4</td><td>3D Generation</td><td>물리 속성을 가진 3D asset 생성임. 시뮬레이션 자산에 유용</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2610.33420'>An Empirical Study of Reinforcement Learning Scaling Laws</a></td><td>50</td><td>4</td><td>RL</td><td>Starpilot, Craftax에서 RL scaling law를 계산량 두 자릿수 범위로 예측하는 실증 연구이며 로봇 실험은 없음</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2610.34868'>GADAR: Generalizing Across Domains via Action Ranking for Classical Planning</a></td><td>50</td><td>4</td><td>Planning</td><td>도메인 기술 D를 입력으로 받아 보지 못한 classical planning domain에서 search 없이 action을 고르는 GADAR임. zero-shot 22.6%로 일반화 한계가 있으나 도메인 일반화 정책은 TAMP 쪽과 닿음.</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2610.33688'>Rescuing Your Pruning: Rethinking Visual Token Pruning and Post-Training Recovery in MLLMs</a></td><td>50</td><td>3</td><td>Multimodal</td><td>MLLM visual token pruning 후 recovery 학습임. efficient inference</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2610.34564'>FlockWorld: Toward Population-Scale Multi-Agent Video World Models through Artificial Life Simulation</a></td><td>50</td><td>3</td><td>World Model</td><td>다수 agent video world model임. 인공 생명 시뮬레이션 기반</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2610.34662'>StreamVibe: Proactive Video Agents for Evolving User Intent</a></td><td>50</td><td>3</td><td>Video</td><td>능동적 video agent의 사용자 의도 추적임</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2610.35002'>DUET4D: Self-Corrective Coupled Guidance for Sparse-View 4D Reconstruction</a></td><td>50</td><td>3</td><td>4D Reconstruction</td><td>sparse-view 4D 재구성 self-corrective 가이던스임</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2610.35229'>Joint Latent Reasoning and Observation for Agentic Video Understanding</a></td><td>50</td><td>3</td><td>Video</td><td>latent reasoning과 관측을 결합한 agentic video 이해임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2610.35854'>FL4N: Feed-forward Latent Model for 4D Novel View Synthesis</a></td><td>50</td><td>3</td><td>4D Reconstruction</td><td>feed-forward latent 4D NVS임</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2610.34384'>AndroidFlux: Evaluating and Reward Modeling Failure Recovery Capabilities in Mobile Use Multimodal Agents</a></td><td>50</td><td>3</td><td>Agents</td><td>AndroidWorld 위 failure-recovery 벤치마크와 reward 모델링 및 offline RL 데이터셋을 내놓음, 주제는 맞으나 GUI 에이전트임</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2610.34073'>Memory Tax: Dissecting the Net Value of Agent Memory</a></td><td>50</td><td>3</td><td>Agent Memory</td><td>전용 memory 시스템 다수가 naive RAG보다 낮아 순가치가 음수임을 대규모로 보이고 memory benefit과 tax로 분해함. memory 설계 판단에 참고되는 분석이나 LLM agent 한정임</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2610.33223'>The Locality Trade-off in Masked Patch Self-Distillation</a></td><td>50</td><td>2</td><td>Representation</td><td>masked patch self-distillation의 locality trade-off 분석임. 표현 학습 관점에서 약한 연결</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2610.34092'>Learning the Autoregressive: Direct Score-Difference Estimation with Amortized Future Credit for Video Distillation</a></td><td>50</td><td>2</td><td>Video</td><td>AR 비디오 few-step 증류임</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2610.34575'>Cumulative Marginal Matching for One-Step Diffusion</a></td><td>50</td><td>2</td><td>Generative</td><td>flow matching marginal 누적 불일치를 직접 맞추는 one-step 생성 목적함수이며 로봇 policy 가속에 일반적 가치가 있음</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2610.33764'>All the Facts, Still the Wrong Answer: Integration Gaps in Vision-Language Models</a></td><td>50</td><td>2</td><td>Multimodal</td><td>VLM이 개별 사실은 맞히면서 종합 판단은 틀리는 multi-evidence integration gap을 분석함. Gemma-3-27B가 8-item 전역 정확도 19.75%에 그치고 probe·activation replacement로 진단하나 로봇 과제는 아님.</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2610.33486'>Learning Dexterous Manipulation: Hands, Simulators, Training, and Evaluation</a></td><td>48</td><td>8</td><td>Dexterous Survey</td><td>113편 dexterous 학습 서베이로 RL+증류 recipe와 teleop VLA 분기를 정리함. 코드와 사양 대조에서 나온 관찰이 유용하나 신규 방법 없음</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2610.34527'>LLM4Robot-Bench: How Far Can GPT-6 Astra Go in Robotic Manipulation? A Hierarchical, Paired Sim-Real Benchmark</a></td><td>48</td><td>7</td><td>Benchmark</td><td>접촉 조작 16개 과제의 sim-real 쌍 벤치마크로 GPT-6 Astra zero-shot 성공이 L1 80%, L3 0%로 떨어짐. 과제당 3회 시행이라 통계력이 약하고 한 모델 평가임</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2610.35458'>RoKON: Efficient and Adaptive Data-Enabled Predictive Control for Robotic Manipulation</a></td><td>48</td><td>6</td><td>Predictive Control</td><td>Gaussian kernel DeePC에 damped Gauss-Newton과 hybrid buffer를 추가함. MuJoCo Franka 블록 밀기 시뮬뿐이라 실용 근거 약함</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2610.34650'>Dream to Assist: Intent-Conditioned World Models for Shared Vehicle Control</a></td><td>48</td><td>5</td><td>World Model/Shared Control</td><td>RSSM world model에 의도 추론을 넣어 공유 제어 보조 정책을 학습함. 인간 대상 연구 3건이나 차량·고속 도메인 중심임</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2610.34033'>Fovea-JEPA: Overcoming Geometric Blind Spots in V-JEPA for Camera Motion Recognition</a></td><td>48</td><td>3</td><td>Video</td><td>V-JEPA 카메라 움직임 인식 개선임</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2610.34952'>DimFlow: Bidirectional Grid-Expert Learning for Dynamic Gaussian Reconstruction</a></td><td>48</td><td>3</td><td>3D Vision</td><td>동적 Gaussian 재구성 grid-expert임</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2610.33353'>Detecting Temporal Concepts in Video Transformers via a No-False-Positives Test</a></td><td>48</td><td>2</td><td>Video</td><td>video transformer의 시간 개념 탐지 검증 방법임</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2610.35536'>EARS: Evidence-Aware Retrieval via Sound and Motion for Budgeted Video Reasoning</a></td><td>48</td><td>2</td><td>Video</td><td>소리와 motion으로 budgeted video 추론용 증거를 검색함</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2610.35954'>Curriculum-Driven Deep Reinforcement Learning for Autonomous Far-Range Rocket Landing</a></td><td>46</td><td>5</td><td>RL</td><td>로켓 수직 착륙을 3단계 curriculum과 critic warm-up, rehearsal로 학습하는 RL 응용이며 새로움은 제한적임</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2610.33816'>Memory or a Clock? Auditing a Memory Advantage in XLand-MiniGrid with Seeds, Maps and Evaluation Noise Apart</a></td><td>46</td><td>4</td><td>RL</td><td>XLand-MiniGrid의 LSTM 이득 25점 중 상당 부분이 time step 정보 덕임을 60회 실행으로 밝혀 robot memory 평가 방법에 참고됨</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2610.34501'>Best Policy Tracking in Reinforcement Learning</a></td><td>46</td><td>4</td><td>RL</td><td>RL 학습 중 성능 진동 때문에 최종 policy 선택이 부정확함을 연속 제어 벤치마크에서 진단하며 평가 방법론에 도움됨</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2610.34668'>Hierarchical Task Network planning in the Goal Lifecycle</a></td><td>46</td><td>4</td><td>Planning</td><td>HTN planning을 Goal Lifecycle 전 단계에 적용한 goal reasoning agent를 제안하고 자율 주행 시뮬레이션에서 시연함. 기대와 실제 결과의 불일치 처리는 replanning과 연결되나 규모가 작음.</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2610.34767'>The Right Fact, the Wrong Decision: SciValidityBench for Scientific Agent Memory</a></td><td>46</td><td>2</td><td>Agent Memory</td><td>과학 agent 메모리에서 기억한 사실을 결정에 써도 되는지를 보는 SciValidityBench를 만들고 counterfactual 쌍으로 검증함. memory 평가 관점은 흥미로우나 과학 도메인임.</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2610.34094'>From Document Layout to Causal Topology: An End-to-End Architecture for Temporal Causal Reasoning</a></td><td>46</td><td>1</td><td>NLP</td><td>시간 인과 추론을 causal topology로 바꿔 TCR-Agent와 attention mask 기반 TCR-Former로 구현함. counterfactual truncation을 symbolic intervention으로 수행하나 텍스트 benchmark 한정임.</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2610.33947'>Learning Functional Specialisation for Bimanual Robotic Control</a></td><td>45</td><td>6</td><td>Bimanual Control</td><td>근골격 시뮬에서 목적과 손 할당에 따른 기능 분화를 2x2로 비교함. 시뮬 단일 과제 분석이라 로봇 일반화 근거 약함</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2610.34929'>Learning Direct Control from Optimization for Dynamic Target Tracking</a></td><td>45</td><td>6</td><td>Navigation</td><td>최적화를 offline으로 증류해 미분 가능 기구학으로 직접 제어 정책을 학습하고 안전 fallback을 둠. jerk 14.1-31.2% 감소이나 시뮬 추적 응용임</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2610.35687'>TrySee: Modular Perception-Enhanced VLM Grounding for Closed-Loop Robot Task Planning in Specialized Domains</a></td><td>45</td><td>6</td><td>VLM Planning</td><td>도메인별 vision 전처리를 붙인 모듈형 closed-loop VLM 계획 파이프라인임. 5개 도메인에서 평가하나 기존 구성요소의 조합임</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2610.35489'>TP-JSCC: Efficient Token Pruning and Joint Source-Channel Coding for LVLMs-based 3D-VQA in Cloud-Edge Collaboration</a></td><td>45</td><td>5</td><td>Embodied AI</td><td>embodied agent 3D-VQA를 cloud-edge로 token pruning과 JSCC 처리함</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2610.33584'>HA-DiPO: Diffusion Policy Optimization for Heterogeneous Cooperative Transport</a></td><td>45</td><td>5</td><td>Multi-agent RL</td><td>이종 사족 협동 운반에 high-level diffusion 정책을 CTDE로 학습함. 시뮬과 실 협동 운반 시연이 있으나 응용 중심임</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2610.34271'>Robust Single-Parameter Point Cloud Registration using Truncated Lp Functions</a></td><td>45</td><td>4</td><td>3D Vision</td><td>단일 파라미터 point cloud registration임</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2610.34689'>RSKD: Grounding Semantic Consistency in Driving VLMs via Distillation</a></td><td>45</td><td>4</td><td>Autonomous Driving</td><td>주행 VLM 의미 일관성 증류임</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2610.35621'>Synthetic Deformable Tubular Benchmark: A mechanically annotated dataset for evaluating deformable 3D reconstruction</a></td><td>45</td><td>4</td><td>3D Vision</td><td>변형 튜브 3D 재구성 합성 벤치마크임. surgical 시나리오</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2610.35448'>Model-Aware Generation of Safety-Critical Scenes for Robust End-to-End Driving via Distilled Planner Surrogates</a></td><td>45</td><td>4</td><td>Driving Failure</td><td>충돌의 95.9%가 planning 실패임을 보이고 planner별 BEV surrogate로 위험 장면을 생성해 fine-tuning함. 실패 모드 분석 접근이 좋으나 주행 도메인임</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2611.03685'>LOLPlay: Benchmarking Real-Time Visual Agents in League of Legends</a></td><td>45</td><td>4</td><td>Embodied AI</td><td>리그 오브 레전드에서 스크린샷과 마우스·키보드로 조작하는 실시간 visual agent 벤치마크 LOLPlay임. 추론 증가가 실시간 제어에 불리함을 보임. 게임 환경이나 시각 추론-행동 지연 문제는 embodied agent와 닿음.</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2610.33492'>Explicit Frictional Contact Modeling in Neural Garment Simulation</a></td><td>45</td><td>3</td><td>Simulation</td><td>neural garment simulation에 마찰 접촉을 명시 모델링함. 변형체 조작과 약한 연결</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2610.33704'>E3tereo: Improving Stereo Matching at Depth Boundaries with Learned Geometric Edges</a></td><td>45</td><td>3</td><td>3D Vision</td><td>stereo depth boundary 개선임</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2610.35110'>Understanding and Repairing Cooperative Perception under Adverse Weather</a></td><td>45</td><td>3</td><td>Perception</td><td>악천후 협력 인지 실패 원인 분석과 수리임. failure diagnosis 요소</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2610.33237'>Each Insufficient in Its Own Way: Calibrating Language Models Across Varying Evidence States</a></td><td>45</td><td>3</td><td>LM Calibration</td><td>증거 상태에 따라 정답 확률 추정이 달라져야 함을 보이고 답할지 증거를 더 모을지 결정을 다룸. 능동 정보 수집과 약하게 연결됨</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2610.33274'>FlexA-Mem: Budget-Adaptive Agentic Memory for LLM Agents</a></td><td>45</td><td>3</td><td>Agent Memory</td><td>대화 사실과 다단계 과제 흔적 등 시나리오별 memory 요구를 예산에 따라 적응시키는 구조임. memory 설계 참고는 되나 LLM agent 한정임</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2610.33645'>PreView: Enhancing GUI Grounding with Preprocessed Views and Cues</a></td><td>45</td><td>2</td><td>Multimodal</td><td>GUI grounding 전처리 view 기법임</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2610.34233'>BoundedGS: Memory-Efficient High-Resolution Training for 3D Gaussian Splatting</a></td><td>45</td><td>2</td><td>3D Vision</td><td>3DGS 고해상도 학습 메모리 절감임</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2610.35090'>Test-Time Prompt-Agnostic Decomposition</a></td><td>45</td><td>2</td><td>Test-Time Adaptation</td><td>prompt-agnostic 분해 기반 TPT임</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2610.35823'>Back to Basics: A Skill-Centric Approach to Generalist Web Agents</a></td><td>45</td><td>2</td><td>Agent</td><td>웹 agent skill 중심 학습과 MiniWeb임</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2610.34191'>Timing Matters Twice: When to Query and When to Skip in Flow-Matching On-Policy Distillation</a></td><td>45</td><td>1</td><td>Generative</td><td>flow matching on-policy distillation 타이밍임</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2610.35594'>Beyond Distribution Matching: Self-Supervised Representation Forcing for Few-Step Video Generation</a></td><td>45</td><td>1</td><td>Video</td><td>few-step video 생성 representation forcing임</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2610.34977'>Adaptive Memory Index Evolution for Agents</a></td><td>44</td><td>3</td><td>Agents</td><td>에이전트 memory의 접근 상태를 plug-in으로 진화시키는 AMIE로 robot memory와 개념만 비슷하고 텍스트 에이전트 대상임</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2610.34677'>Curriculum-Guided Acquisition of Hierarchical Task Knowledge from LLM-Generated Experience</a></td><td>44</td><td>3</td><td>Planning</td><td>LLM이 만든 검증된 풀이 trace로 HTN method 학습용 curriculum을 자동 생성해 토큰 비용을 줄임. 계층적 task 지식 습득은 long-horizon planning과 맞닿으나 평가가 소규모 planning domain임.</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2610.35013'>Multiscale Policy Optimization for Long-Horizon LLM Agents</a></td><td>44</td><td>3</td><td>RL</td><td>LLM agent의 turn 단위 critic 값 변화에 맞춰 token 단위 credit을 나누는 MPO를 제안함. 장기 horizon RL credit assignment이나 평가가 search·tool-use임.</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2610.34797'>TimeWorld: Towards Action-Conditioned Multimodal World Models for Time Series Forecasting</a></td><td>44</td><td>2</td><td>World Model</td><td>시계열 예측용 action-conditioned world model 벤치마크이며 로봇이 아님</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2610.34724'>Harness-Model Collaboration for Long-Horizon Continual Learning</a></td><td>44</td><td>2</td><td>Agent Memory</td><td>전략 카드 기반 외부 경험과 파라미터 적응을 결합한 HaMo로 Web agent의 continual learning 유지·적응을 개선함. memory와 continual learning 아이디어는 맞으나 Web agent 한정임.</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2610.35679'>CounterFlow: Target-Conditioned Flow Matching for Visual Counterfactuals</a></td><td>44</td><td>1</td><td>Generative</td><td>target 조건 flow matching으로 시각 counterfactual을 만드나 XAI 목적임</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2610.35706'>TriTile: Three-Tier Attention for Video Diffusion Transformers</a></td><td>44</td><td>1</td><td>Video</td><td>video DiT attention을 3단계 정밀도로 근사해 가속하는 방법이며 world model 추론에 간접 도움됨</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2610.33432'>ConMem: Counterfactual Multi-Scenario Probing for Resolving LLM Memory Misalignment</a></td><td>44</td><td>1</td><td>AI</td><td>LLM agent 장기 메모리의 보존 판단을 counterfactual 시나리오로 사전 감사하는 ConMem과 MemAlign 벤치마크(1,079건)임. counterfactual+memory 조합은 누리랩 주제와 개념상 닿으나 대화 에이전트 한정이고 정확도 75.16%로 개선 폭이 작음.</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2610.33811'>Rectified Language Flow</a></td><td>44</td><td>0</td><td>LG</td><td>rectified flow로 token embedding을 생성하는 언어 모델 ReLF를 제안함. 16 NFE에서 AR 대비 15-19배 빠른 생성을 보이는 generative model이나 언어 한정임.</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2610.35058'>3D-Force Estimation for Dual-arm Manipulation of Deformable Linear Objects via Factor Graphs</a></td><td>42</td><td>6</td><td>Deformable Estimation</td><td>factor graph로 DLO의 3D 힘과 형상을 단일 센서로 추정함. 노이즈 시뮬 평가뿐이라 실로봇 근거 약함</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2610.34060'>Learning Interaction-Aware Path Corrections from Unlabeled Trajectories: A LiDAR-Based Sim-to-Real GNN Framework for Construction Robots</a></td><td>42</td><td>5</td><td>Social Navigation</td><td>LiDAR만으로 비라벨 시연에서 GNN 경로 보정을 학습함. 경로 불규칙성 39.2% 감소이나 건설 bricklaying 한정임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2610.33789'>Segmentation of Moving Objects During Camera Motion Using the OWL Function</a></td><td>42</td><td>4</td><td>3D Vision</td><td>OWL 함수 기반 이동 물체 분할 해석적 프레임워크임</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2610.34819'>Selective Monocular Precession Estimation under Geometric and Evaluation Ambiguity: An Auditable Synthetic Study with ORBIT-SCOUT</a></td><td>42</td><td>4</td><td>3D Vision</td><td>단안 관측으로 회전 물체 축 추정의 모호성을 감사함</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2610.34403'>No Cones, No Duals: A Fast and Scalable Solver for NRSfM</a></td><td>42</td><td>3</td><td>3D Vision</td><td>NRSfM 빠른 solver임</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2610.34850'>Recovering Black-Box Point Cloud Models from Pose Shifts via Derivative-Free Optimization</a></td><td>42</td><td>3</td><td>3D Vision</td><td>black-box point cloud 모델 pose shift를 derivative-free로 복구함. test-time 적응</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2610.33412'>Performance Gaps Between Open-Loop, Certainty-Equivalent, and Optimal Control Under Action-Dependent Observations</a></td><td>42</td><td>3</td><td>Control</td><td>관측이 행동에 의존할 때 certainty-equivalent 제어의 격차를 LQ 시스템에서 증명하는 이론으로 active sensing과 약하게 이어짐</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2610.33568'>Trajectory2Gym: Decision-Grounded Compositional Interaction Synthesis for Tool-Use Agents</a></td><td>42</td><td>3</td><td>Tool-use Agents</td><td>성공 trajectory도 조합 커버리지와 결정 근거가 부족하면 쓸모없음을 지적해 환경 합성함. 데이터 설계 아이디어는 참고되나 tool-use 한정임</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2610.34644'>SlowLab: Benchmarking Autonomous AI Agents on a Year of Experiments They Cannot Undo</a></td><td>42</td><td>3</td><td>Agent</td><td>1년짜리 온실 실험 캠페인에서 되돌릴 수 없는 실험을 설계하는 agent 벤치마크임. LLM agent가 Bayesian 최적화 baseline보다 낮음을 보인 순차 의사결정 평가라 약간 관련됨.</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2610.34799'>Centralized Critics for N-Agent Ad Hoc Teamwork</a></td><td>42</td><td>3</td><td>MARL</td><td>N-agent ad hoc teamwork에서 비통제 팀원의 history를 critic에 넣으면 advantage 분산이 줄어듦을 증명하고 실험함. MARL 이론이나 로봇 적용은 없음.</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2610.35439'>Omni-InteractScope: Benchmarking Proactive and Agentic Interaction in Continuous Omnimodal Streams</a></td><td>42</td><td>3</td><td>Multimodal</td><td>연속 오디오·비디오 스트림에서 Omni-LLM의 선제적 개입 시점을 재는 Omni-InteractScope 벤치마크임. 12개 모델이 on-time 도구 호출 40% 이하로 실패함. 스트리밍 비서 쪽이라 로봇 관련은 약함.</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2610.33575'>CADonatello: Towards Real-World Multi-Part 3D CAD Reconstruction</a></td><td>42</td><td>2</td><td>3D Vision</td><td>다부품 CAD 재구성임. 제조 응용 중심</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2610.34235'>ParetoGS: High-Quality Continuous-Budget 3D Gaussian Splatting with Sparse Adapted Anchors</a></td><td>42</td><td>2</td><td>3D Vision</td><td>3DGS 연속 budget anchor 모델임</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2610.34344'>Birth-Death Structural Learning for 3D Gaussian Splatting</a></td><td>42</td><td>2</td><td>3D Vision</td><td>3DGS birth-death 구조 학습임</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2610.35053'>LOCUS: Locate Once, Check Until Settled. Draft-and-Verify Visual Grounding with a Box Head and Coordinate-Token Verification</a></td><td>42</td><td>2</td><td>Multimodal</td><td>VLM grounding draft-and-verify 추론임</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2610.35347'>CVTSplat: Multi-view Reconstruction Using an Adaptive Centroidal Voronoi Tessellation</a></td><td>42</td><td>2</td><td>3D Vision</td><td>Voronoi 기반 다시점 재구성임</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2610.33215'>Vision Token Pruning via Query-Vision Interaction Decomposition</a></td><td>42</td><td>2</td><td>Efficient Inference</td><td>VLM visual token pruning 분해임</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2610.33311'>When Does Pre-Trained Capacity Help Causal Learning? From Scalar Prediction to Counterfactual Post-Training</a></td><td>42</td><td>2</td><td>LG</td><td>Qwen 0.5B/1.5B 두 모델만으로 causal post-training 용량 효과를 보며 저자도 일반 법칙이 아니라고 인정함, 로봇 연결 약함</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2610.35497'>When Fine-Grained Credit Assignment Helps and Hurts: Multimodal Agentic Reinforcement Learning through Video Editing</a></td><td>42</td><td>2</td><td>Multimodal</td><td>멀티모달 에이전트 RL에서 fine-grained credit assignment의 득실을 분석하며 연결 약함</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2610.33799'>MTA-Zero: Self-Improving Multimodal Deep Search via Online QA-Solver Co-training</a></td><td>42</td><td>2</td><td>Multimodal Agents</td><td>QA 생성기와 solver를 online으로 co-training해 멀티모달 심층 검색 agent를 self-improve함. 고정 코퍼스 한계를 푸는 점은 좋으나 웹 검색 agent라 로봇 연결 약함</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2610.33539'>CoEvolve: Counterfactual-Guided Co-Evolution of Memory and Collaboration in Multi-Agent Systems</a></td><td>42</td><td>2</td><td>Agent</td><td>multi-agent LLM의 memory와 collaboration을 원본·counterfactual trajectory 비교로 함께 진화시키는 CoEvolve임. counterfactual+memory는 누리랩 주제와 닿으나 ALFWorld·WebShop 텍스트 환경 평가에 그침.</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2610.33540'>Patch-Derived or Register Tokens? Comparing Variable-Length Image Tokenizers</a></td><td>42</td><td>1</td><td>Generative</td><td>가변 길이 image tokenizer 비교 연구임</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2610.33810'>Grounded Exploration for Open-Ended Image Editing</a></td><td>42</td><td>1</td><td>Generative</td><td>open-ended 이미지 편집의 grounded exploration임</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2610.33841'>Grounding on Request: Learning Modality Control in Vision-Language Models</a></td><td>42</td><td>1</td><td>Multimodal</td><td>VLM modality 제어 학습임</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2611.09957'>HALMES: Knowing When to Intervene in LVLM Hallucination Mitigation</a></td><td>42</td><td>1</td><td>Multimodal</td><td>LVLM hallucination 개입 시점 선택임</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2610.34828'>Transporting Quantiles to Codebook: Scalable Vector Quantization without Codebook Collapse</a></td><td>42</td><td>1</td><td>Representation</td><td>quantile을 codebook으로 수송해 VQ collapse를 막는 이산 표현 기법임</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2610.35697'>MiRL: Error-Targeted Reinforcement Learning for Correcting Terminal Agent Misbehaviors</a></td><td>42</td><td>1</td><td>Agents</td><td>터미널 에이전트의 반복 오류를 찾아 그 지점부터 RL로 고치는 MiRL로 failure correction 개념은 있으나 로봇이 아님</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2610.34180'>Write What Matters: Disentangling Token Selection from Slot Allocation in Recurrent Memory</a></td><td>42</td><td>1</td><td>Memory Architecture</td><td>recurrent memory에서 token 선택과 slot 수 배정을 분리한 Factorized Write Routing임. 쓰기 정책을 분리한 구조 통찰이 있으나 LM 구조 연구임</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2610.35804'>Learning When to Commit: Schedule Distillation for Fast Diffusion Language Models</a></td><td>42</td><td>1</td><td>LG</td><td>dLLM에서 어떤 token을 먼저 commit할지 unmasking schedule을 만들어 distill함. GSM8K에서 10.12배 가속을 보이는 efficient inference이나 LM 한정임.</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2610.33625'>RAQ-MLA: Role-Aware Quantization for Multi-Head Latent Attention Caches</a></td><td>42</td><td>1</td><td>LG</td><td>MLA KV cache의 latent와 positional key 역할이 달라 각각 다른 변환으로 양자화하는 RAQ-MLA임. 학습 없이 약 2.5bit, 6.5배 용량을 내는 efficient inference이나 LLM 한정임.</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2610.33292'>KINESYS: Test-Time Adaptation for Reference-Based Effect Editing in Images</a></td><td>42</td><td>0</td><td>Generative</td><td>reference 기반 효과 편집의 test-time adaptation임</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2610.35494'>Enhancing Deep Reinforcement Learning for Robotic Motion Planning via Task Decomposition</a></td><td>40</td><td>6</td><td>RL</td><td>첫 층 critic 전이와 reward 재설계로 Pick-and-Place 학습 단계를 0.75M에서 0.20M으로 줄임. 전이는 장애물 Pick-and-Place에서 오히려 낮아 PyBullet 소규모 결과임</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2610.33227'>Causal-based approaches to explain and learn from self-extension - A review</a></td><td>40</td><td>5</td><td>Causal/Review</td><td>self-aware 로봇의 인과 설명과 실패 원인 학습을 다룬 리뷰임. causal reasoning 주제와 맞으나 신규 방법과 실험 없음</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2610.33574'>Memory-Aware Keyframe Management for Dense Maps on Memory-Constrained Robots</a></td><td>40</td><td>5</td><td>Semantic Mapping</td><td>메모리 예산을 직접 제한하고 방/복도 단위로 keyframe을 적재함. Jetson에서 OOM 없이 query 위치 추정이 6-9점 높음. 시스템 엔지니어링이나 semantic zone 아이디어 있음</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2610.33916'>Real-Time Human Trajectory Prediction from RGB-D for Mobile Robots Using Bi-Mamba</a></td><td>40</td><td>5</td><td>Human Prediction</td><td>Bi-Mamba와 GRU로 262K 파라미터 궤적 예측을 만들고 학습-배포 입력 분포를 맞춤. TIAGo 배포 확인했으나 ADE 0.29m로 새롭진 않음</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2610.35062'>PushAround: Collaborative Path Clearing via Physics-Informed Hybrid Search</a></td><td>40</td><td>5</td><td>NAMO</td><td>connectivity graph와 짧은 물리 시뮬을 결합해 장애물 밀기 계획함. 최대 4대 로봇 시뮬이고 고전 planning임</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2610.35289'>Reward-Guided RRT* for Budgeted Task and Motion Planning</a></td><td>40</td><td>5</td><td>TAMP</td><td>reward 유도 RRT*로 task 선택과 motion을 함께 계획함. VNS-PRM*와 비슷한 해를 더 적은 샘플로 얻는 고전 planning 개선임</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2610.35554'>Metric Scale for Insta360 Structure-from-Motion from the Camera&#x27;s Embedded IMU</a></td><td>40</td><td>4</td><td>3D Vision</td><td>360 카메라 IMU로 metric scale 복원임</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2611.09959'>A four-view smartphone video dataset of a robot-held flexible strip, with camera poses and a 3D LaGSplat baseline</a></td><td>40</td><td>4</td><td>Dataset</td><td>로봇이 잡은 유연 strip 다시점 비디오 데이터셋과 LaGSplat baseline임</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2610.34574'>Conditional Diffusion Generation of DVL and Inertial Signals for Underwater Navigation</a></td><td>40</td><td>4</td><td>Navigation</td><td>AUV의 DVL과 관성 신호를 conditional diffusion으로 합성해 속도 추정을 학습시키며 항법 데이터 증강으로만 약하게 연결됨</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2610.34538'>Dual Gradient Consensus for Adaptive Learning to Transient Out-of-Distribution Disturbances in Quadrotor Control</a></td><td>40</td><td>4</td><td>Quadrotor Adaptation</td><td>gradient 기억 비교로 단기 out-domain residual의 적응 오염을 억제함. 수치 시뮬 RMSE만 평가해 쿼드로터 제어 특화 개선임</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2610.33726'>Human-Feedback-Guided Multi-Agent Inverse Reinforcement Learning for Interactive Driving Behavior Modeling</a></td><td>40</td><td>4</td><td>RL</td><td>운전자 감정 피드백을 ordinal preference로 넣은 multi-agent maximum-entropy IRL(HFG-MAIRL)임. language/human feedback 기반 reward 학습이나 AIDE 데이터셋 중심이고 규모 작음.</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2610.33351'>Real Time Motion Detection in Video Inspired by Photonic Time Stretch</a></td><td>40</td><td>3</td><td>Video</td><td>광학 time stretch 영감의 실시간 motion detection임</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2610.33760'>C-DFF: Concept-Level Diagnostics for Mechanism Parity in Simulation-Based Validation of Autonomous Driving Perception</a></td><td>40</td><td>3</td><td>Autonomous Driving</td><td>시뮬레이션 검증용 concept-level 진단임</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2610.34632'>RIDE-Splat: Reflection Removal for In-the-Wild Driving Environments</a></td><td>40</td><td>3</td><td>3D Vision</td><td>차량 3DGS 반사 제거임</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2610.35361'>SG-Splat: Stable Geometry Learning under Pose Uncertainty for Pose-Free 3D Gaussian Splatting</a></td><td>40</td><td>3</td><td>3D Vision</td><td>pose-free 3DGS 기하 안정화임</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2610.34321'>TopX: Text-to-Motion for Unseen Skeletons from the Skeleton File Alone</a></td><td>40</td><td>2</td><td>Generative</td><td>unseen skeleton text-to-motion임</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2610.34926'>Supervising the Visible State: Separating Representation from View Selection in Streaming Video</a></td><td>40</td><td>2</td><td>Video</td><td>streaming video에서 표현과 view 선택을 분리해 감독함</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2610.34959'>GUIFlow: Temporal Redundancy-Aware Incremental Inference for GUI Agents</a></td><td>40</td><td>2</td><td>Efficient Inference</td><td>GUI agent 시간 중복 incremental 추론임</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2610.33477'>A Unified Analysis of Importance-Corrected Momentum Actor-Critic over a Markovian Trajectory</a></td><td>40</td><td>2</td><td>RL</td><td>ridge LSTD critic과 importance-corrected momentum actor의 수렴 이론으로 로봇 실험은 없음</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2610.33956'>Continual Learning Exam: Benchmarking Long-Horizon RSI and Experiential Learning in LLM Agents</a></td><td>40</td><td>2</td><td>Agents</td><td>LLM 에이전트의 장기 continual learning 벤치마크이며 로봇이 아님</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2610.33201'>Position, Role or Label? A Controlled Study of Instruction Conflicts in LLM Agents</a></td><td>40</td><td>2</td><td>Agent Instruction</td><td>position, role, label을 분리한 WhoWins 1,080 시나리오로 LLM agent의 지시 충돌 우선순위를 통제 실험함. 로봇 직접 관련 없으나 지시 계층 분석은 참고 가능함</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2610.33495'>Five Architectures, One Shared Space Cross-Model Representational Alignment Without Weight Merging</a></td><td>40</td><td>2</td><td>Representation</td><td>서로 다른 구조 5개 frozen 모델이 가중치 병합 없이 활성만으로 공유 공간에 정렬됨을 permutation test로 보임. 표현 정렬 관점이 흥미로우나 로봇 연결 약함</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2610.33512'>Eat Your Precision: Precision Objective Mitigates Reward Hacking in Rubric-based RL</a></td><td>40</td><td>2</td><td>RL</td><td>rubric reward가 recall만 키워 장황해지는 문제를 precision 목적으로 완화함. reward hacking 통찰은 RL 일반에 참고되나 LM 한정임</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2610.33624'>RSI Arena: Towards Recursive Self-Improvement with Human Feedback</a></td><td>40</td><td>2</td><td>Self-improvement</td><td>frontier 모델 10개가 GPU 1,000시간으로 자율 post-training하고 사용자 피드백으로 개선하는 연구임. 자기 개선 주제이나 LM 학습임</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2610.34507'>The Price of Scale in Proactive Memory Recall</a></td><td>40</td><td>2</td><td>Memory</td><td>memory 회상 gate가 저장소 크기 N에 따라 다중 검정 문제로 악화됨을 LongMemEval에서 보임. 회상 임계의 이론 분석이 좋으나 대화 assistant 한정임</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2610.33528'>SkillShift-Bench: Benchmarking Skill Learning under Environment Evolution for Web Agents</a></td><td>40</td><td>2</td><td>Agent</td><td>web agent skill이 환경 변화(context/perceptual/execution shift)에서 얼마나 깨지는지 재는 SkillShift-Bench임. 비정상 환경 하 skill 실패를 test-time adaptation으로 줄이는 점이 skill chaining 연구와 개념상 닿으나 웹 한정임.</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2610.34728'>SKALOS: Learning to Distinguish Similar Skills with Capability Graphs</a></td><td>40</td><td>2</td><td>Agent</td><td>능력 그래프로 유사한 skill을 구분하는 reranker SKALOS를 제안함. NDCG@10 2.68pt 상승, ALFWorld 성공률 22%에서 29%로 오름. skill 선택 쪽이라 약하게 관련됨.</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2610.34855'>DecoyCount: Evaluating Visual-Reasoning Misalignment in Counting</a></td><td>40</td><td>2</td><td>Multimodal</td><td>VLM의 counting 오류를 decoy 이미지 1,586장으로 분석해 reasoning-alignment gap 12.1~22.1pt를 보임. 시각 추론 진단이나 로봇 직접 관련은 약함.</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2610.35398'>Belief-Conditioned Multi-Agent Actor Critic for Decentralized LLM Collaboration</a></td><td>40</td><td>2</td><td>MARL</td><td>belief를 조건으로 하는 multi-agent actor-critic BCMAAC로 분산 LLM 협업을 학습함. Minecraft·웹 검색 실험이고 워크숍 수준 규모임.</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2610.33203'>Of Chains and Gains: What Reinforcement Learning changes on Reasoning-based Image Quality Assessment</a></td><td>40</td><td>1</td><td>Multimodal</td><td>RLVR이 IQA에서 바꾸는 것을 분석함. 로봇 관련성 낮음</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2610.33564'>What Remains OOD? OODConceptBench for Open-World Concept Recognition in Vision-Language Models</a></td><td>40</td><td>1</td><td>Multimodal</td><td>VLM 개념 OOD 벤치마크임</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2610.33798'>Whispers from the Neighbors: Rethinking Caption Consensus as Inference-Time Evidence for Vision-Language Retrieval</a></td><td>40</td><td>1</td><td>Multimodal</td><td>caption consensus를 retrieval 추론 증거로 사용함</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2610.34545'>VTC-AUDIT: An Interventional Reliability Audit for Visual-Token Compression under Paired Image Shifts</a></td><td>40</td><td>1</td><td>Multimodal</td><td>visual token 압축 신뢰성 audit임</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2610.35756'>VidEdit3D: Flexible 3D Gaussian Editing with Video Diffusion</a></td><td>40</td><td>1</td><td>3D Vision</td><td>video diffusion 3DGS 편집임</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2610.33337'>Information-Theoretic Scaling Laws for Generative Diffusion Training</a></td><td>40</td><td>1</td><td>Generative</td><td>diffusion 학습의 유한 데이터 scaling을 정보이론으로 분석하나 로봇 연결 약함</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2610.34678'>Exploring perceptual straightness in learned visual representations</a></td><td>40</td><td>1</td><td>CV</td><td>학습된 시각 표현의 perceptual straightness 분석이며 연결 약함</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2610.35801'>FOCUS: Active Critic Learning for Long-Horizon Language Model Agents</a></td><td>40</td><td>1</td><td>Agents</td><td>selective branching으로 critic을 active learning해 장기 LLM 에이전트의 credit assignment를 개선하며 로봇은 아님</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2610.34103'>T2D: Target-to-Draft Model Pruning &amp; Adaptation for Efficient Speculative Decoding</a></td><td>40</td><td>1</td><td>Efficient Inference</td><td>target 모델을 pruning해 draft 모델을 만들어 speculative decoding의 정렬과 지연을 맞춤. LLM 가속 기법이고 로봇 직접 연결 약함</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2610.35295'>Did the Model Use That? Counterfactual Training Boosts Self-Attribution in Language Models</a></td><td>40</td><td>1</td><td>Counterfactual/LM</td><td>counterfactual 학습으로 모델이 외부 정보 영향을 정확히 자기 귀속하게 함. counterfactual 관점은 닿으나 LM 해석 연구임</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2610.35556'>LoopFold: Parallelizing Recurrent Depth in Looped Transformers</a></td><td>40</td><td>1</td><td>LG</td><td>looped Transformer 후속 loop 입력을 predictor로 예측해 병렬화하고 corrector로 보정해 decoding latency를 46% 줄임. efficient inference 기여나 LM 한정임.</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2610.34500'>CaliMem: Search-Efficient Data Agent via Calibrated Memory</a></td><td>40</td><td>1</td><td>Agent</td><td>데이터 curation 정책을 실행 전에 결과를 예측해 calibration하는 CaliMem임. 예측 오차로 기억 주장을 수정해 과일반화를 줄이는 test-time curation이나 생물·LLM post-training 데이터 한정임.</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2610.33581'>UltraFlash: Accelerating Megapixel Visual Synthesis</a></td><td>40</td><td>0</td><td>Generative</td><td>megapixel diffusion 가속임</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2610.34704'>Stable Continuous-Time Consistency Distillation: An Empirical Study with a Multistep Extension</a></td><td>40</td><td>0</td><td>Generative</td><td>continuous-time consistency distillation 안정화 경험 연구임</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2610.33755'>Computer Vision Navigation for an Autonomous Vehicle Model Using Reinforcement Learning</a></td><td>38</td><td>5</td><td>RL</td><td>PPO로 소형 자율주행 차량 제어함. 단순 응용 수준</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2610.35670'>Continuous-Time Safe Planning and Control for Agile Quadrupeds</a></td><td>38</td><td>5</td><td>Quadruped Planning</td><td>Bernstein 다항식으로 SE(2) 전체 구간의 충돌 회피와 입력 제한을 인증하는 연속시간 planner임. 이론은 탄탄하나 최적화 기반 planning임</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2610.33174'>Bracketing Shows the Way: Adaptive Multi-Exposure Policy as Input for Robust Visual SLAM</a></td><td>38</td><td>4</td><td>SLAM</td><td>multi-exposure bracketing 정책과 factor graph로 터널 출구에서 상태추정 오차를 AE 대비 78% 줄임. 주행 SLAM 응용이고 코드 공개함</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2610.33640'>HARP: Handoff-Aware Recovery Planning for Active Target Acquisition in Multi-UAV Handoff</a></td><td>38</td><td>4</td><td>Active Perception UAV</td><td>다중 UAV 핸드오프에서 실패 유형별 시점을 생성하는 복구 planner임. 시뮬 49회 모두 성공하나 좁은 UAV 응용임</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2610.34040'>Cut a Wall, See a Wall: Identity Substitution in Occluded Point-Cloud Perception for Construction Robots</a></td><td>38</td><td>4</td><td>3D Perception</td><td>가림에서 분할망이 숨은 물체를 한 sink class로 오라벨하는 현상을 분석하고 기하 feature 14개로 복원함. 현상 분석은 흥미로우나 건설 도메인 한정임</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2610.34043'>Holding a Steady Course: Knowledge Evolution from Expertise and Lessons for Continual Agent Learning</a></td><td>38</td><td>2</td><td>Agents</td><td>LLM 에이전트가 경험과 교훈으로 지식을 진화시키는 continual 학습이며 로봇 직접성 낮음</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2610.34045'>Minimax Regret for Sobolev Kernel-Based Reinforcement Learning</a></td><td>38</td><td>2</td><td>RL</td><td>Sobolev RKHS kernel RL의 minimax regret 이론이며 로봇 응용은 약함</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2610.35733'>Multi-Objective Reinforcement Learning Using Routed Ensembles and Trajectory Attribution</a></td><td>38</td><td>2</td><td>RL</td><td>objective-conflict 계수와 routed ensemble로 multi-objective RL regret을 줄이며 로봇 제어를 응용으로만 언급함</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2610.35967'>Data-driven Discovery of Lie Symmetries and First Integrals with Latent ODEs</a></td><td>38</td><td>2</td><td>LG</td><td>latent ODE로 Lie 대칭과 first integral을 발견하는 LatentLieODE이며 물리 구조 학습과 약하게 이어짐</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2610.35616'>Hierarchical Skill Evolution for Coding Agent</a></td><td>38</td><td>2</td><td>NLP</td><td>coding agent의 trajectory에서 task·repo·cross-repo 계층으로 skill을 distill함. 실패 trajectory 활용 면에서 agent skill 연구와 약하게 닿으나 로봇은 아님.</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2610.33877'>Semantic Concept Steering Breaks the Explanation Drift Loop in Continual Learning</a></td><td>38</td><td>1</td><td>LG</td><td>continual learning의 설명 drift 완화임</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2610.34037'>What Sketches Tell Us about LVLMs: Conventions, Grounding, and Localisation</a></td><td>38</td><td>1</td><td>Multimodal</td><td>스케치로 LVLM 분석함</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2610.34263'>RacerGS: Residual-Autoregressive Context for 3D Gaussian Splatting Compression</a></td><td>38</td><td>1</td><td>3D Vision</td><td>3DGS 압축임</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2610.33577'>Variational Atlas Autoencoders and Self-Supervised Chart Selection</a></td><td>38</td><td>1</td><td>Representation</td><td>manifold를 여러 chart로 나누는 Variational Atlas Autoencoder이며 로봇 연결 약함</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2610.34590'>Sparse Sum-of-Squares Layers for Certified Learning</a></td><td>38</td><td>1</td><td>LG</td><td>sparse sum-of-squares layer로 인증 학습을 하며 연결 약함</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2610.33517'>One Model, Two Paths: Balancing Single-Pass and Looped Performance in Language Models</a></td><td>38</td><td>1</td><td>LM Architecture</td><td>looped와 single-pass 가중치 공유 학습 간 품질 충돌을 가중 loss로 다룸. 효율 추론 관련 있으나 LM 구조 연구임</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2610.33282'>Estimation of Propagated Risk in LLM-based Multi-Agent Systems</a></td><td>38</td><td>1</td><td>AI</td><td>multi-agent LLM 실행 trace에서 upstream 오류가 downstream으로 전파되는 위험을 추정하는 IE-Prop임. AUROC가 약 0.05 오르는 failure 예측 성격이나 개선 폭이 작고 로봇은 아님.</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2610.33817'>EnvLunch: The Environment as a Free Lunch for Learning to Interact</a></td><td>38</td><td>1</td><td>Agent</td><td>환경 최종 관측에서 동치 trajectory를 복원하게 하는 라벨 없는 warm-up EnvLunch임. DB 에이전트에서 평균 9점 이상 앞서나 데이터 분석 도메인 한정임.</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2610.34941'>Stop or Clarify? Experience-Conditioned Active Fact Verification</a></td><td>38</td><td>1</td><td>Agent</td><td>증거가 충분한지 멈출지 질문할지 정하는 SEAC 정책을 fact verification에 적용함. 소규모 SciFact 개선은 결론 불확실하다고 저자도 인정함.</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2610.35579'>Infinity Machine: a self-improving AI agent for research</a></td><td>38</td><td>1</td><td>Agent</td><td>양자 정보 등 검증 가능 문제를 푸는 self-improving 연구 agent Infinity Machine임. 일부 SOTA 결과를 주장하나 로봇과 무관함.</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2610.34563'>Recursive CLIP: Vision-Language Distillation with Looped Transformer Blocks</a></td><td>38</td><td>0</td><td>Multimodal</td><td>CLIP looped transformer 증류임</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2610.33904'>Counterfactual Test-Time Augmentation for Shortcut Removal in Language Models</a></td><td>38</td><td>0</td><td>NLP</td><td>LLM shortcut 제거에 counterfactual test-time augmentation을 쓰나 텍스트 분류 대상임</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2610.34577'>Rethinking Verification in Agent Harnesses</a></td><td>38</td><td>0</td><td>Agent</td><td>코딩 agent harness의 verification 설계 17종을 Terminal-Bench 등에서 비교한 test-time scaling 연구임. 독립 critic 리뷰가 효율적이라는 결과이나 로봇과 거리 있음.</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2610.35309'>Shared Context, Separate Engines: Stateful Streaming Inference for Multimodal LLMs on Edge SoCs</a></td><td>36</td><td>2</td><td>Multimodal</td><td>엣지 SoC에서 MLLM streaming 추론을 여러 엔진에 분산하는 시스템이며 온보드 배치에 약하게 도움됨</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2610.33845'>Build, Don&#x27;t Play: Self-Improving LLM Research Agents Develop a Hearthstone Battlegrounds AI That Rivals Top Players</a></td><td>36</td><td>2</td><td>RL</td><td>LLM 연구 agent가 Hearthstone Battlegrounds 시뮬레이터와 PPO 정책을 스스로 구축하는 AutoTavern임. 상위 플레이어를 넘는 결과이나 게임 한정이고 로봇 무관함.</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2610.34015'>The Information Geometry of Representation Formation</a></td><td>36</td><td>1</td><td>Representation</td><td>표현이 형성되는 과정을 information geometry로 측정하며 연결 약함</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2610.33861'>ReGE: Stronger Agents through Experience Synthesis</a></td><td>36</td><td>1</td><td>Agent</td><td>과거 실행 기록을 coach 한 번 호출로 안내문으로 합성해 새 시도를 돕는 ReGE임. 평균 정확도가 약 9-10퍼센트포인트 오르나 LLM 에이전트 한정임.</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2610.34298'>Matched Capabilities, Different Behaviors: A Controlled Study of MCP and CLI Interfaces for Language Agents</a></td><td>36</td><td>1</td><td>Agent</td><td>MCP와 CLI 인터페이스가 같은 능력인데도 agent 행동을 다르게 만드는지 MICA로 통제 비교함. 2,004개 중 94.3%에서 궤적이 갈리며 DART 수리로 점수가 최대 9.0점 오르나 tool 인터페이스 한정임.</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2610.34616'>CSI-TextBench: A Dataset and Benchmark for Language-Grounded Ambient Sensing Perception</a></td><td>36</td><td>1</td><td>Multimodal</td><td>WiFi CSI를 자연어와 정렬하는 데이터셋과 벤치마크를 구축하고 contrastive 정렬을 비교함. 실내 센싱 쪽이라 로봇 직접 관련은 약함.</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2610.35434'>Skill$^{\infty}$: Recursive Self-Improvement for Agent Skill Optimization</a></td><td>36</td><td>1</td><td>Agent Skill</td><td>메타 skill이 자기 자신을 최적화하는 Skill-infinity를 제안함. SkillsBench 83개 과제 pass rate 60.7%로 사람 skill 56.4% 대비 소폭 개선임.</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2610.33360'>LSTM-Style Looped Transformers with Shared KV Caches</a></td><td>36</td><td>0</td><td>LG</td><td>looped transformer가 KV cache를 공유해 파라미터를 40.4% 줄이는 효율화이며 로봇 무관함</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2610.33740'>A Distribution-Matching Perspective on LLM Training Algorithms</a></td><td>36</td><td>0</td><td>NLP</td><td>LLM 학습 알고리즘을 distribution matching으로 통합하는 관점이며 로봇 무관함</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2610.34005'>Steering the Teacher: Improving On-Policy Self-Distillation for Thinking Models</a></td><td>36</td><td>0</td><td>NLP</td><td>thinking model용 on-policy self-distillation teacher steering이며 로봇 무관함</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2610.34514'>Ambiguous Fits: The Rashomon Effect and Challenges in Scaling Law Estimation</a></td><td>36</td><td>0</td><td>LG</td><td>scaling law 추정의 Rashomon 불확실성 분석임</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2610.35793'>Quantifying Claim Smoothing by LLM Research Agents</a></td><td>36</td><td>0</td><td>NLP</td><td>deep research 에이전트가 상충 근거를 매끄럽게 뭉뚱그리는 smoothing을 claim 단위로 측정하는 SmoothScore를 제안함. 평가 도구이고 로보틱스 무관함.</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2610.33667'>SWE-Ladder: Learning to Localize, Reproduce, and Patch via Progressive Privileged Self-Distillation</a></td><td>36</td><td>0</td><td>AI</td><td>SWE agent를 localize·reproduce·patch 단계별 privileged self-distillation으로 학습하는 SWE-Ladder임. pass@1 9.6%에서 16.4%이며 코딩 한정임.</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2610.34491'>What Effort Level Should I Choose? On the Economics of Reasoning Effort in LLM Agents</a></td><td>36</td><td>0</td><td>AI</td><td>reasoning effort를 올려도 낮은 effort가 푼 과제를 놓치고 비용만 최대 42배 드는 현상을 counterfactual로 측정함. 실패 시 단계적으로 올리는 정책이 대안이며 test-time compute 분석이나 LLM 한정임.</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2610.34721'>Prefetch-Steered Routing: Deterministic Cache-Aware Expert Selection for Offloaded Mixture-of-Experts Decoding</a></td><td>36</td><td>0</td><td>Efficient Inference</td><td>offloaded MoE 디코딩에서 prefetch를 결정적 logical cache로 묶는 PSR 라우팅으로 2.2배 가속함. 효율 추론이지만 로봇 맥락은 없음.</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2610.35615'>Context-Aware Generation and Modulation of Expressive Motion Behavior using Multimodal Foundation Models</a></td><td>35</td><td>5</td><td>HRI Motion</td><td>애니메이션 원칙을 DMP로 구현하고 foundation model로 표현 동작을 생성함. 해석 가능하고 morphology 간 쓰이나 사용자 연구 중심 응용임</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2610.34054'>Extended LASMP: Language Aided Subset Sampling Based Motion Planner for Drone Navigation</a></td><td>35</td><td>4</td><td>Drone Planning</td><td>LLM이 해석한 지시로 3D 샘플링 영역을 제한하는 RRT 확장임. 시뮬 샘플 수 감소만 보이고 incremental임</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2610.35642'>VPR-Space: A Benchmark for Visual Place Recognition in Space Analog Domains</a></td><td>35</td><td>4</td><td>Place Recognition</td><td>달·화성 유사 환경 VPR 데이터셋 16개와 정답 생성 방법을 제안함. 데이터셋 기여이고 방법 새로움은 작음</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2610.33758'>Road Infrastructure Perception for Autonomous Driving: Taxonomy, Representations, Tasks, and Challenges</a></td><td>35</td><td>3</td><td>Survey</td><td>도로 인프라 인지 서베이임</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2610.34976'>Sparse Recovery Bird&#x27;s-Eye View Model Soup for Robust Camera-Based 3D Object Detection</a></td><td>35</td><td>3</td><td>3D Vision</td><td>BEV 3D 검출 model soup 강건화임</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2610.35018'>Zero-Shot Monocular Depth Estimation for Visual Perception in Lower-Limb Prostheses</a></td><td>35</td><td>3</td><td>CV</td><td>의족용 단안 깊이 zero-shot 평가임</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2610.33445'>From Intelligence to Autonomy: Foundations and Construction of Autonomous Agents for Future Intelligent Systems</a></td><td>35</td><td>3</td><td>Agents</td><td>자율 에이전트의 기반과 구성을 논하는 개괄 성격이며 새 방법과 실험 근거가 약함</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2610.33484'>Can One Hear Geometry? Gauge-Invariant Spectral Descriptors for Text-to-B-rep Retrieval</a></td><td>35</td><td>1</td><td>3D Vision</td><td>B-rep 텍스트 검색용 spectral descriptor임</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2610.33909'>Rank-1 Weight-Corrected Trainable Weight Averaging for Out-of-Distribution Detection</a></td><td>35</td><td>1</td><td>LG</td><td>OOD 탐지 weight averaging 기법임</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2610.34144'>Reversion, Retention, and Semantic Intervention: Measuring Functional Content in CLIP Fine-Tuning Deltas</a></td><td>35</td><td>1</td><td>Multimodal</td><td>CLIP fine-tuning delta 해석임</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2610.34846'>Seeing Before Naming: Context-Grounded Learning of Novel Visual Concepts</a></td><td>35</td><td>1</td><td>Multimodal</td><td>새 시각 개념 맥락 학습임</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2610.33299'>The Emergence and Sparsification of a Syntactic Circuit</a></td><td>35</td><td>1</td><td>Interpretability</td><td>pythia에서 주어-동사 일치 circuit이 일찍 학습된 뒤에도 재조직됨을 학습 동안 추적함. 해석가능성 분석이고 로봇 무관함</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2610.33442'>Adaptive Transfer of Representational Signatures for LLM Reliability Detection</a></td><td>35</td><td>1</td><td>LLM Reliability</td><td>표현 signature를 새 도메인으로 적응시켜 라벨 적은 환각 탐지를 함. 신뢰도 탐지 아이디어는 failure detection과 개념적으로만 닿음</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2610.33776'>TriageRAG: Failure-Aware Self-Training for Adapting Retrieval-Augmented Language Models to Specialized Domains</a></td><td>35</td><td>1</td><td>RAG</td><td>unlabeled 도메인 코퍼스에서 실패 인지 self-training으로 RAG를 적응함. 도메인 적응 기법임</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2610.35201'>DTCA: Denoising Token Credit Assignment for Reinforcement Learning in Diffusion Language Models</a></td><td>35</td><td>1</td><td>Diffusion LM RL</td><td>denoising 단계마다 token credit을 배분하는 DLM RL임. credit assignment 아이디어는 일반적이나 LM 한정임</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2610.34878'>ClinVerse: A Realistic Multi-Agent Diagnostic Environment for Training and Evaluating Medical Agents</a></td><td>35</td><td>1</td><td>Agent</td><td>실제 EHR 15만 건 기반 의료 진단 multi-agent 환경 ClinVerse임. 능동 정보 획득과 reward 설계는 흥미로우나 의료 도메인임.</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2610.33194'>Support-guided OOD Removal with Diffusion</a></td><td>35</td><td>0</td><td>Generative</td><td>diffusion 기반 국소 OOD 제거로 로봇과 무관함</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2610.34177'>Freeze What Is Settled, Cache What Is Smooth: Spatial Freezing Keeps Step Caching in Its Low-Error Regime</a></td><td>35</td><td>0</td><td>Generative</td><td>편집 diffusion 가속임</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2610.34303'>EditDistill: Is It Possible to Guide Video Editing with Image Editing?</a></td><td>35</td><td>0</td><td>Video</td><td>이미지 편집으로 비디오 편집 유도함</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2610.34333'>CrossPair: Unlocking Generalist Visual Transformation Learning in Image Editors</a></td><td>35</td><td>0</td><td>Generative</td><td>이미지 편집기 일반 변환 학습임</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2610.34782'>ToDoPro: Faster and Better Reference-Based Generation: Early Token Reduction via Downsampled Self-Probing</a></td><td>35</td><td>0</td><td>Generative</td><td>reference 생성 token 축소임</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2610.34785'>Natural Jammers: When Non-Robust Features Become Antagonistic</a></td><td>35</td><td>0</td><td>LG</td><td>non-robust feature 적대 분석임</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2610.35077'>Improving VLMs on Scientific Chart Analysis via Autonomous Evolution</a></td><td>35</td><td>0</td><td>Multimodal</td><td>과학 차트 VLM 자율 진화임</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2610.35857'>Do vision models know that three is three?</a></td><td>35</td><td>0</td><td>Representation</td><td>비전 모델 수 개념 표현 분석임</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2610.33208'>Lower expected Fisher rank implies better PAC generalization</a></td><td>35</td><td>0</td><td>LG</td><td>Fisher rank PAC 일반화 이론임</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2610.33217'>Neyman Orthogonal Activation Steering</a></td><td>35</td><td>0</td><td>LG</td><td>Neyman 직교 activation steering임</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2610.34553'>How Much Information Can We Fit inside a Transformer?</a></td><td>35</td><td>0</td><td>LG</td><td>랜덤 사실 triple 암기에 필요한 transformer 차원이 사실 수의 로그로 늘어난다는 실증 분석임. 로봇과 무관한 용량 연구임.</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2610.33186'>Interpretable Collision Avoidance and Feasibility Guarantees through an Uncertainty Aware Pipeline</a></td><td>34</td><td>3</td><td>Autonomous Driving</td><td>충돌 확률을 상류에서 풀어 convex safe set으로 feasibility를 보장함. 교차로 시뮬과 Jackal 실험이나 모듈형 주행 planner라 학습 relevance 낮음</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2610.33654'>Physics-Informed Graph-Based Safe RL with Constraint-Specific Critics for Community Battery Coordination in Distribution Network</a></td><td>34</td><td>3</td><td>RL</td><td>배전망 커뮤니티 배터리를 physics-informed graph와 constraint별 critic PPO로 제어함. voltage 위반 최대 80.5% 감소하나 전력계통 응용이며 로봇 아님.</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2610.33842'>Approximate Universal Prediction under Interaction</a></td><td>34</td><td>1</td><td>RL</td><td>근사 보편 예측과 planning 에이전트의 상호작용 이론으로 AIXI 계열이며 연결 약함</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2610.35303'>InterQ-RL: Interaction-Aware Correction of Execution Mismatch in Quantized Agentic RL</a></td><td>34</td><td>1</td><td>RL</td><td>양자화 agentic RL의 실행 불일치를 보정하며 LLM 대상임</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2610.35426'>Intent-Preserving Adversarial User Simulation for Multi-Turn Agent Evaluation</a></td><td>34</td><td>1</td><td>Agents</td><td>멀티턴 에이전트 평가용 의도 보존 adversarial 사용자 시뮬레이터임</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2610.35720'>Quantifying the failure of symmetry learning in linear diffusion models due to initialization and finite-sample effects</a></td><td>34</td><td>1</td><td>Generative</td><td>선형 diffusion에서 대칭 학습 실패를 정량화하는 이론이며 연결 약함</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2610.33702'>Seeing the Options: What Should a Visual Candidate See?</a></td><td>34</td><td>1</td><td>Multimodal</td><td>이미지 후보 선택에서 후보가 request를 보는 것이 성능 차이의 주 원인임을 분석함. 순서 불변성을 증명하며 GUI 후보 선택 한정임.</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2610.33907'>OS-Wizard: Scaling Computer-Using Agents to Specialized Software via Knowledge-Guided Exploration</a></td><td>34</td><td>1</td><td>Agent</td><td>전문 데스크톱 앱에서 튜토리얼 기반 트리 탐색과 GUI-Code 혼합 행동으로 궤적 10.9K개를 수집하는 OS-Wizard임. 64.1% 정확도이나 GUI agent 데이터 수집 위주임.</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2610.34167'>Task Success Is Not Enough: Side-effect-Aware Evaluation of Tool-Using Language Model Agents</a></td><td>34</td><td>1</td><td>Agent</td><td>tool 사용 agent가 목표를 달성하면서 허가 없는 부수 행동을 하는 collateral damage를 재는 SABench임. 11개 모델에서 15.2% 발생을 보이는 안전성 평가이며 이메일·티켓 도메인 한정임.</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2610.35226'>Trainable Boundary-Keeping Where No Formal Answer Exists: A Controlled Knock-In Study of Reward Training in Evidence-Sufficiency Judgment</a></td><td>34</td><td>1</td><td>LLM RL</td><td>증거 충분성 판단에서 SFT 후 GRPO로 boundary-keeping 거절 행동을 학습시킴. 14B 단일 계열 통제 연구이고 로봇과 무관함.</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2610.35500'>Test-Time Confidence Adaptation under RL-Induced Trajectory Shift</a></td><td>34</td><td>1</td><td>LLM</td><td>agentic RL 이후 바뀐 trajectory 분포에서 안정성 기반으로 confidence를 test-time 적응하는 StaR-TTA임. QA 한정이고 AUROC 0.721임.</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2610.33368'>Multiple Importance Sampling for Guided Speculative Inference</a></td><td>34</td><td>0</td><td>NLP</td><td>소형 LLM 앙상블 draft를 검증하는 test-time scaling 확장으로 로봇 무관함</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2610.33527'>Implicit Beliefs as Scalable Process Rewards for Strategic Persuasion</a></td><td>34</td><td>0</td><td>NLP</td><td>LLM 설득 대화에 implicit belief를 process reward로 쓰는 연구로 로봇 무관함</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2610.33826'>Reactive Optimizers</a></td><td>34</td><td>0</td><td>LG</td><td>LM 에이전트가 학습 중 optimizer 코드를 고쳐 쓰는 시도로 로봇 무관함</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2610.33882'>Intervention-Certified Amplification: A Validity Gate for $σ$-Weighted Post-Training</a></td><td>34</td><td>0</td><td>NLP</td><td>SFT/RL 혼합 post-training의 증폭 행동을 검증하는 게이트이며 MATH 대상으로 로봇 무관함</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2610.34044'>A Sign Law for Entropy Drift under Sampler Mismatch in RLVR</a></td><td>34</td><td>0</td><td>RL</td><td>RLVR에서 sampler 불일치가 entropy 부호를 정하는 이론이며 LLM 대상임</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2610.34056'>INTRA: Interleaved Non-contiguous Token spaRse Attention</a></td><td>34</td><td>0</td><td>LG</td><td>비연속 token sparse attention으로 이차 비용을 줄이는 효율화임</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2610.34137'>Self-Evolution Reasoner: Continuous Optimization via Policy-Intrinsic Exploration and Exploitation</a></td><td>34</td><td>0</td><td>NLP</td><td>RLVR에 self-distillation을 결합한 추론 모델 최적화이며 로봇 무관함</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2610.34182'>Entropic Control for Homeostatic Optimization: Pre-empting Catastrophic Forgetting via Dynamic Feedback</a></td><td>34</td><td>0</td><td>NLP</td><td>LLM SFT의 forgetting을 feedback 제어로 완화하며 로봇 무관함</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2610.34310'>Birth, Death and Diff: Insertion-Based Sequence Generation with Corrections</a></td><td>34</td><td>0</td><td>Generative</td><td>삽입 기반 masked diffusion의 교정 가능한 시퀀스 생성임</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2610.34477'>Finite-Sample Sensitivity of Kernel Metrics for Generative Evaluation</a></td><td>34</td><td>0</td><td>Generative</td><td>KID 같은 kernel 생성 평가 지표의 유한 표본 민감도 분석임</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2610.35544'>StateLoop: Persistent State for Looped Transformers</a></td><td>34</td><td>0</td><td>NLP</td><td>looped Transformer에 token별 persistent state와 gate를 추가해 perplexity를 낮춤. 작은 module 추가 수준이고 LM 한정임.</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2610.35694'>Not One Belief: Answer Payloads, Persistence, and Dissociated Confidence Signals in Conversational Question Answering</a></td><td>34</td><td>0</td><td>NLP</td><td>대화형 QA에서 사용자 반박 시 답이 바뀌는 조건을 speech act와 payload로 나눠 분석함. confidence 신호 4종이 불일치함을 보이나 로보틱스 무관함.</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2610.33684'>More: Mode-Optimized Reasoning with Self-Adaptive Effort for Self-Evolving Agents</a></td><td>34</td><td>0</td><td>AI</td><td>과제마다 reasoning 형태와 effort를 고르는 MORE를 MATE-PPO로 학습함. 응답 길이와 추론 시간은 줄지만 LLM 한정임.</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2610.34425'>CTXAgent - Self-Controlled Context Management of LLM Agents</a></td><td>34</td><td>0</td><td>Agent</td><td>모델이 직접 compact 시점과 보존 내용을 정하는 context 관리 CTXAgent임. 비용 34% 절감을 보이나 coding agent 한정이고 로보틱스 무관함.</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2610.33471'>SCET-CBF: Speed-Calibrated Soft Guidance for One-Step Dynamic Navigation</a></td><td>33</td><td>3</td><td>Navigation Control</td><td>속도 보정 CBF soft guidance로 동적 장애물 완주율을 49.8%에서 72.8%로 올림. 조향 제한 차량 제어 개선이라 incremental임</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2610.34085'>Doppler-aided Position-Velocity Tracking of Hidden Objects using mmWave Radar</a></td><td>33</td><td>3</td><td>Radar Perception</td><td>RAD 전체를 쓰는 mmWave NLoS 추적과 576 시퀀스 데이터셋임. 위치 오차 8.95cm이나 센싱 특화임</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2610.33515'>Collective Collaboration of Recursive Autonomous Agents</a></td><td>33</td><td>2</td><td>Agents</td><td>스마트 팩토리 생산 과제를 재귀 에이전트로 협업시키는 시스템이며 로봇 학습 연결 약함</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2610.33939'>Stable and Calibrated Latent Force ODE Filters</a></td><td>33</td><td>2</td><td>LG</td><td>latent force ODE filter의 안정성과 보정이며 물리 시스템 힘 추정과 약하게 이어짐</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2610.33396'>Fast Instinct, Slow Reason: A Dual-Speed Agentic Framework for Self-Configuring Multi-Object Tracking in Satellite Video</a></td><td>33</td><td>1</td><td>CV</td><td>위성 영상 다중 객체 추적 agentic 프레임워크임</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2610.34886'>ThinkBit: Search Codewords, Recalibrate Scales, Select by Reasoning</a></td><td>33</td><td>1</td><td>Efficient Inference</td><td>reasoning 보존을 목표로 2-bit scalar 양자화를 하는 ThinkBit임. Qwen3-1.7B MATH-500 46.7점. 효율 추론이나 로봇 맥락은 없음.</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2610.33460'>Semantic-First: Temporal Scheduling in Flow Matching for Reliable Emotional Image Generation</a></td><td>33</td><td>0</td><td>Generative</td><td>감정 이미지 생성 flow matching 스케줄링임</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2610.33379'>One Call Ahead: Packed Self-Speculative Decoding with Diffusion Drafting</a></td><td>33</td><td>0</td><td>NLP</td><td>diffusion drafter로 self-speculative decoding을 가속하는 LLM 추론 연구임</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2610.33483'>Error-Subspace Calibration for Multi-Task Model Merging</a></td><td>33</td><td>0</td><td>LG</td><td>multi-task model merging 후 오차 부분공간 보정으로 incremental임</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2610.34961'>C-SafeGen: Certified Safe LLM Generation with Claim-Based Streaming Guardrails</a></td><td>33</td><td>0</td><td>LLM Safety</td><td>claim 단위 streaming guardrail과 conformal 위험 보증을 결합한 C-SafeGen 디코딩임. 이론 보증은 있으나 로봇과 무관함.</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2610.33476'>A Differentiable Chassis Safety Layer for Intelligent Vehicle Motion Control</a></td><td>32</td><td>3</td><td>Vehicle Control</td><td>타이어 힘 제약을 QP로 넣은 미분 가능 안전 레이어와 모방+위험 지도 학습임. 차량 섀시 한정이라 manipulation과 거리 있음</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2610.33731'>How Geometry Shapes Generative Model Evaluation on Riemannian Manifolds</a></td><td>32</td><td>1</td><td>Generative</td><td>Riemannian manifold 생성 모델 평가 지표의 기하 의존성 분석이며 연결 약함</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2610.33950'>What Makes a Question Curious? Measuring Model Curiosity in Human-LLM Interactions</a></td><td>32</td><td>1</td><td>NLP</td><td>호기심형 질문을 이론 기반 분류로 정의하고 4개 대화 데이터에서 측정함. 능동 질문 관점이 약하게 닿으나 로봇 무관함</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2610.34238'>$Δτ$-Bench: Pushing Agents Toward a Moving Capability</a></td><td>32</td><td>1</td><td>Agent Benchmark</td><td>tool 생태계가 진화할 때 효율적 경로를 찾고 수정하는지 평가함. 변화에 적응하는 agent 평가이나 tool-use 한정임</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2610.34335'>CoLink: Global Compression and Knowledge Linking for Multi-Turn Dialogue Modeling</a></td><td>32</td><td>1</td><td>Dialogue Memory</td><td>전역 압축과 지식 연결로 장기 대화 정보를 추출함. 대화 memory 기법이고 로봇 무관함</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2610.34537'>STEP: Soft Trajectory Estimation of Prediction Correctness via Per-Step Probability Scoring</a></td><td>32</td><td>1</td><td>Calibration</td><td>중간 추론 단계 확률로 정답 여부를 training-free로 추정함. 신뢰도 추정이 failure 예측과 닿으나 LLM 한정임</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2610.34894'>What Outcome RL Buys: Finishing, Reliability, Rarely Reach</a></td><td>32</td><td>1</td><td>RL</td><td>RL 모델 20개의 pass@1 이득을 finishing, reliability, reach로 분해함. 이득이 새 지식이 아니라는 분석으로 RL 해석에 참고되나 LM 한정임</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2610.35328'>Constrained Decoding: Harmful or Beneficial? Revisiting Its Impact on LLM Performance</a></td><td>32</td><td>1</td><td>NLP</td><td>constrained decoding이 추론을 해치는지 3가지 제약 유형으로 분류해 인과 ablation함. 성능 저하 대부분이 prompt/format 불일치 때문이라는 분석이나 로보틱스와 거리 멂.</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2610.34714'>SearchHorizonBench: A Benchmark for Search Value in AI Agents</a></td><td>32</td><td>1</td><td>Agent</td><td>agent가 추가 검색의 가치를 판단하도록 45,632회 실행을 모은 SearchHorizonBench임. 로봇과 무관한 검색 agent 벤치마크임.</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2610.35125'>When Fusion Order Matters: Insights on Progressive Multimodal Representation Learning for Cross-modal Retrieval</a></td><td>32</td><td>1</td><td>Multimodal</td><td>텍스트-비디오 검색에서 modality 융합 순서를 UniPRO로 분석해 MSR-VTT-9k R@1 97.9를 달성함. 검색 벤치마크 중심이라 로봇과 거리 있음.</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2610.35767'>Free to Look, Free to Reason: Simple LLM Harnesses Outdiagnose Hand-Crafted Root Cause Analysis Agents</a></td><td>32</td><td>1</td><td>Agent</td><td>마이크로서비스 장애 RCA에서 단순 LLM harness가 수작업 agent보다 PR@1이 높음을 보임. 장애 진단이라는 주제는 닿으나 로봇과 무관함.</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2610.33430'>Dynamic Query as Budgeting for Tiny Object Detection</a></td><td>32</td><td>0</td><td>CV</td><td>tiny object detection의 query budgeting임</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2610.33472'>Qwen-Image-PE: Learning Visual Design for Text-to-Image Prompt Enhancement</a></td><td>32</td><td>0</td><td>Generative</td><td>T2I prompt enhancement 모델임</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2610.35684'>OmniShowcase: Omnidirectional Subject-Consistent Video Generation from Multi-View Images</a></td><td>32</td><td>0</td><td>Video</td><td>subject 일관 비디오 생성임</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2610.33840'>Sliding Networks: A Family of Residual Structures Preserving Feature Learning and Feature Diversity</a></td><td>32</td><td>0</td><td>LG</td><td>residual 구조의 width/depth scaling에서 feature 다양성을 유지하는 연구로 무관함</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2610.33968'>Hierarchical Cooperative GFlowNets</a></td><td>32</td><td>0</td><td>LG</td><td>계층 협력 GFlowNet의 탐색 개선으로 무관함</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2610.34272'>DoubleFree:Exploiting Exploration History for Rollout-Free Multi-Task LLMs Training</a></td><td>32</td><td>0</td><td>NLP</td><td>multi-task LLM RL에서 탐색 이력을 재사용하는 효율화임</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2610.34375'>Whether or Where? Tail Calibration Signals Finite-Budget Reward Hacking in Best-of-N Selection</a></td><td>32</td><td>0</td><td>NLP</td><td>best-of-N에서 tail calibration으로 reward hacking을 진단하며 로봇 무관함</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2610.34427'>ScaleRLT: Exact Log-Probabilities and Fast Deferred Rollouts for Reinforcement Learning on Looped Transformers</a></td><td>32</td><td>0</td><td>NLP</td><td>looped LM의 정확한 log-prob와 deferred rollout RL 시스템임</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2610.34617'>Valid Early Detection of Memorization in Diffusion Models</a></td><td>32</td><td>0</td><td>Generative</td><td>diffusion 모델 memorization을 조기 탐지하는 통계 방법임</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2610.34862'>Priority-Preserving Advantage Aggregation for Multi-Reward Policy Optimization</a></td><td>32</td><td>0</td><td>NLP</td><td>LLM 다중 보상의 우선순위를 보존하는 advantage 집계임</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2610.34949'>Correlation-Aware Exploration for Long-Trace Reasoning</a></td><td>32</td><td>0</td><td>NLP</td><td>긴 추론 trace의 GRPO 탐색에 상관을 고려하는 LLM 연구임</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2610.34951'>Improving Reasoning with Rollout Agreement for Group-Based Policy Optimization</a></td><td>32</td><td>0</td><td>NLP</td><td>RLVR에서 rollout 합의로 추론을 개선하는 LLM 연구임</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2610.35059'>Reinforcement Learning Done Right for Explicit Confidence Targets</a></td><td>32</td><td>0</td><td>NLP</td><td>LLM 신뢰도 목표를 위한 RL 설계로 무관함</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2610.35518'>S3AC: Stabilized, Selective, and Scalable Actor-Critic for LLM Reasoning</a></td><td>32</td><td>0</td><td>NLP</td><td>LLM RLVR의 안정적 선택적 actor-critic임</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2610.35962'>h1: A Taste of the Bitter Lesson in Automated Theorem Proving</a></td><td>32</td><td>0</td><td>NLP</td><td>정리 증명에 bitter lesson을 적용한 LLM 연구임</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2610.35533'>An Algorithmic Account of Few-Shot Concept Induction in Language Models</a></td><td>32</td><td>0</td><td>NLP</td><td>few-shot concept induction을 amortized direction accentuation 가설로 설명하고 LM에서 검증함. 해석 이론 성격이며 로보틱스 무관함.</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2610.33267'>Scoped Semantic Invariance as a Foundation for LLM Reliability</a></td><td>32</td><td>0</td><td>AI</td><td>LLM의 의미 동치 질의 불일치를 scoped semantic invariance로 정식화하고 KG hotspot 구조로 분석함. 이론·분석 성격이고 로보틱스 무관함.</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2610.34260'>MultiEvoSkill: Structure-Aware Multi-Agent Skill Evolution for Generalizable Skill Artifacts</a></td><td>32</td><td>0</td><td>Agent</td><td>skill 문서를 typed graph로 만들고 다중 agent 토론으로 진화시키는 MultiEvoSkill임. LLM agent skill 최적화이며 로봇 skill과는 거리 멂.</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2610.34994'>Why Are LLMs Confidently Wrong? Correcting Overconfident Errors via Causal Head Intervention</a></td><td>32</td><td>0</td><td>LLM</td><td>attention head 개입으로 LLM의 과신 오류를 줄이는 CoCHI임. calibration 지표만 개선했고 로봇과 무관함.</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2610.35530'>CANS: Capability-Preserving Neuron Steering for Large Language Models</a></td><td>32</td><td>0</td><td>LLM</td><td>closed-form neuron scaling으로 능력을 보존하며 LLM 행동을 조향하는 CANS임. HarmBench 공격 성공률 15.5%에서 1.75%로 감소함. 로봇과 무관함.</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2610.33930'>EnerGNN: Learning Optimization-Compatible Energy Functions for Exact Constrained Combinatorial Inference</a></td><td>31</td><td>1</td><td>LG</td><td>조합 최적화용 energy GNN으로 로봇 연결 약함</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2610.34740'>Networked Humanoid Intelligence: Communication, Coordination, Collaboration, and Social Interaction</a></td><td>30</td><td>5</td><td>Survey</td><td>networked humanoid의 통신, 협업, 사회 지능 서베이임. 구조는 있으나 학습 방법 관점의 기여 없음</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2610.34534'>Multimodal Socially Aware Framework for Human-Robot Interaction in Virtual Reality</a></td><td>30</td><td>4</td><td>HRI</td><td>음성·시각·촉각을 합친 사회적 로봇을 VR에서 18명으로 평가함. 원격조종 baseline보다 낮게 평가된 결과 보고이고 기술 기여 약함</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2610.35429'>MATE-BT: A Behavior-Tree-Based Framework for Hierarchically Decentralized Mission Autonomy in Heterogeneous Multi-Robot Teams</a></td><td>30</td><td>4</td><td>Multi-robot</td><td>BT 기반 leader 전환과 분산 할당으로 로봇 고장에도 임무를 지속함. Jetson 온보드 실험이 있으나 시스템 아키텍처임</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2610.35629'>From Language to Drives: A Multimodal Framework for Aligning Autonomous Robots with Human Purposes</a></td><td>30</td><td>4</td><td>Alignment</td><td>LLM과 VLM으로 인간 목적을 로봇 mission과 drive로 변환하는 3층 구조임. 개념 설계 위주이고 정량 근거는 초록에 없음</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2610.35092'>Uncertainty Evaluation to Support Safety of the Intended Functionality Analysis for Determining the Applicability of Performance Targets Across Triggering Conditions in ML-Based LiDAR Object Detection</a></td><td>30</td><td>3</td><td>Autonomous Driving</td><td>LiDAR 검출 SOTIF 불확실성 평가임</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2610.33271'>Neuromorphic Decision Dynamics for Deadlock-free Safe Navigation in Congested Environments</a></td><td>30</td><td>3</td><td>Multi-agent Navigation</td><td>neuromorphic 분산 제어로 혼잡 환경 deadlock-free 통과를 이론적으로 보장함. 학습 없는 제어 이론이라 relevance 낮음</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2610.34084'>DSGN: A Dual-Stream Gated Network for Scalable Simultaneous Surveillance and Containment</a></td><td>30</td><td>3</td><td>Multi-robot RL</td><td>감시와 봉쇄 stream을 분리하고 gating하는 DRL 구조임. 시뮬 확장성 평가 중심이고 architecture 변형 수준임</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2610.34466'>IntNet: A Communication-Driven Multi-Agent Reinforcement Learning Framework for Cooperative Autonomous Driving</a></td><td>30</td><td>3</td><td>Driving MARL</td><td>의도 전송과 적응형 통신 scheduling을 결합한 협동 주행 MARL임. 주행 도메인이고 baseline 비교 위주임</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2610.33504'>FreqPKC: Frequency-Aware PeakConv for Radar Semantic Segmentation</a></td><td>30</td><td>2</td><td>CV</td><td>radar semantic segmentation 모듈 개선임</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2610.34218'>From Presence Labels to Bounding Boxes: Can Multimodal Large Language Models Scale Surgical Instrument Localization?</a></td><td>30</td><td>2</td><td>Multimodal</td><td>수술 도구 localization MLLM 평가임</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2610.35637'>SeeRF: Learning to See Beyond Fields of View via Generative Image Registration and Fusion</a></td><td>30</td><td>2</td><td>CV</td><td>생성적 이미지 정합 융합임</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2610.34861'>AgriDefend: A $205 Offline Edge Device that Detects Crop Stress Before Visible Symptoms via Multimodal AI Fusion</a></td><td>30</td><td>2</td><td>LG</td><td>저가 오프라인 장치로 작물 스트레스를 탐지하는 시스템으로 로봇 학습과 무관함</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2610.33338'>TinyFlow: Breaking the Warping Bottleneck for Edge Optical Flow</a></td><td>30</td><td>2</td><td>Optical Flow</td><td>warp 없는 1.26M 파라미터 INT8 optical flow임. 엣지 배포용 효율 설계이고 VO 평가도 있으나 로봇 학습 relevance 낮음</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2610.34759'>From Belief Inference to Task Action: A Multi-Level Evaluation of Theory of Mind on Verifiable Tasks</a></td><td>30</td><td>2</td><td>Theory of Mind</td><td>믿음 추론이 가사 협업 과제의 행동으로 이어지는지 다단계 평가함. 협업 에이전트와 약하게 닿으나 LM 평가임</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2610.33265'>Image Clustering with Vision-Language Model Embeddings</a></td><td>30</td><td>1</td><td>CV</td><td>VLM 임베딩 이미지 클러스터링 비교 연구임</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2610.33478'>MarineLife-16K: An Attribute-Rich Video-Text Dataset for Motion-Aware Marine Video Understanding</a></td><td>30</td><td>1</td><td>Video</td><td>해양 영상-텍스트 데이터셋임</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2610.34190'>GeoPrompt: Geometry-Conditioned Prompt Learning for Underwater Open-Vocabulary Instance Segmentation</a></td><td>30</td><td>1</td><td>CV</td><td>수중 open-vocabulary segmentation임</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2610.34897'>SGDB: Semantic-Geometric Decoupling and Evidence Binding for Logical Anomaly Detection</a></td><td>30</td><td>1</td><td>CV</td><td>logical anomaly 탐지임</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2610.34993'>Reason or Recite: Complementary Specialists with an LLM Judge for Traffic Anomaly Reasoning</a></td><td>30</td><td>1</td><td>Video</td><td>교통 이상 추론 specialist 조합임</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2610.35152'>Complexity-guided Regularization for Generalizable Human Gaussian Splatting</a></td><td>30</td><td>1</td><td>3D Vision</td><td>human Gaussian splatting 정규화임</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2610.35374'>GIFT: Representation Geometry Matters for Single-Domain Generalized Object Detection</a></td><td>30</td><td>1</td><td>CV</td><td>단일 도메인 일반화 검출 표현 기하임</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2610.35724'>MatAnyone-E: Sparse Memory Propagation for Efficient High-Resolution Video Matting</a></td><td>30</td><td>1</td><td>Video</td><td>효율적 비디오 matting임</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2610.33354'>The Clustering Occupation Kernel (CLOCK) Method for Time Series Arising from Dynamical Systems</a></td><td>30</td><td>1</td><td>LG</td><td>동역학 시계열을 RKHS occupation kernel로 군집화하는 방법이며 연결 약함</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2610.33366'>Distill, Debate, Discover: Grounding Multi-Agent Research Ideation in Graph-Distilled Insights</a></td><td>30</td><td>1</td><td>Agents</td><td>연구 지식 그래프에서 증류한 전문성으로 multi-agent 아이디어 토론을 함. 과학 발견 도구이고 로봇 무관함</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2610.33511'>Towards a Learnable Retriever for Textual Graph Question Answering</a></td><td>30</td><td>1</td><td>GraphRAG</td><td>retriever 자체를 학습 가능하게 하는 GraphQA 구조임. 지식 그래프 QA 특화임</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2610.33608'>Mycelium: A Meta-Study of Hallucination Detection Across Provenance, Typology, and Granularities</a></td><td>30</td><td>1</td><td>Hallucination</td><td>환각 탐지 벤치마크를 정의 방식별로 정리한 메타 연구임. 평가 해석성 기여이고 LLM 한정임</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2610.33766'>StateWise: Teaching Language Models to Track and Obey Evolving Constraints in Multi-Turn Dialogue</a></td><td>30</td><td>1</td><td>Dialogue</td><td>지속 제약 누락과 철회 제약 재발을 다중 턴 대화에서 추적하도록 학습함. 상태 추적 문제이나 로봇 무관함</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2610.33806'>IntentDelta: A Human-Constructed Benchmark for Evolving User Intent</a></td><td>30</td><td>1</td><td>Agents</td><td>WebShop, TravelPlanner 638 trajectory로 진화하는 사용자 의도 추적을 11개 agent에서 평가함. 언어 agent 벤치마크임</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2610.33962'>Beyond Belief: Evaluating and Mitigating LLM Susceptibility to Misinformation</a></td><td>30</td><td>1</td><td>Agent Safety</td><td>신뢰도 낮다고 평가한 공지에도 모델이 27-99% 해로운 tool call을 함을 보임. 행동과 판단 불일치 관찰이 있으나 LLM 보안 연구임</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2610.34336'>Improving the Chain-of-Thought Compressibility of Pruned Reasoning Models via Long--Short Contrastive Pruning</a></td><td>30</td><td>1</td><td>Efficient Reasoning</td><td>pruning과 CoT 압축이 서로 간섭하는 문제를 long-short 대조 pruning으로 다룸. LM 서빙 효율임</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2610.35482'>Beyond Words Alone: Disentangling Distributed Evidence for Visually Grounded Cultural Translation</a></td><td>30</td><td>1</td><td>Multimodal</td><td>SNS 번역에서 이미지·문화 증거 분산 정도를 진단하는 Culture-MMT 벤치마크를 만듦. 시각 grounding 효과를 분리해 보이나 로보틱스와는 멂.</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2610.33375'>AgentOrch: How Close Can Global Orchestration Come to Step-by-Step Interaction?</a></td><td>30</td><td>1</td><td>AI</td><td>enterprise workflow에서 global orchestration과 step-by-step 상호작용 간 정확도 격차를 벤치마크함. 사전 계획 대 반응형 비교라는 점만 planning과 닿고 로봇은 아님.</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2610.33594'>Counterfactual Model Testing Under Distribution Shift</a></td><td>30</td><td>1</td><td>LG</td><td>분포 이동 하에서 모델 성능을 counterfactual로 재현해 추정하는 online model testing 방법임. 모니터링 관점이 failure diagnosis와 약하게 닿으나 tabular 중심임.</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2610.35150'>LongSearchEval: Evaluating Long-Horizon Web Search Capabilities of Large Language Models via a Trajectory-Aware Agent Framework with Failure-Node Localization</a></td><td>30</td><td>1</td><td>Agent Eval</td><td>LLM 웹 검색 agent 16종의 궤적에서 failure node를 자동 위치 추정하는 평가 프레임워크임. 실패 지점 국소화 아이디어는 failure diagnosis와 닿으나 웹 도메인임.</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2610.35280'>Self-Supervised Pretraining for PHM: What Transfers, What Does Not, and What Federating It Costs</a></td><td>30</td><td>1</td><td>Time Series</td><td>PHM 47개 데이터셋에서 self-supervised 사전학습의 전이를 측정함. 분류에는 효과, RUL에는 불확실하다는 negative 결과도 보고함. 로봇 직접 관련은 약함.</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2610.34610'>Do Words Matter? What Text Contributes to Few and Full-Shot Vision-Language Anomaly Detection</a></td><td>30</td><td>0</td><td>Multimodal</td><td>VL 이상 탐지 텍스트 기여 분석임</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2610.34901'>LE-GDA: Layer Ensemble Gaussian Discriminant Analysis for Training-Free Few-Shot CLIP Adaptation</a></td><td>30</td><td>0</td><td>Multimodal</td><td>training-free few-shot CLIP 적응임</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2610.35219'>Multi-Agent Relay Thinking</a></td><td>30</td><td>0</td><td>NLP</td><td>multi-agent relay thinking임</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2610.35827'>Seeing Through Distractions: Context-Stable Attribution via the Least Core</a></td><td>30</td><td>0</td><td>Interpretability</td><td>attribution Shapley 대안임</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2610.33331'>Augmentation-Guided Adversarial Training via Local Stability-Based Sample Selection</a></td><td>30</td><td>0</td><td>LG</td><td>국소 안정성 기반 샘플 선택으로 adversarial training 비용을 줄이는 incremental 기여임</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2610.33404'>COPE: Composable Performance Emulation for Mixture-of-Experts Offloading Policies</a></td><td>30</td><td>0</td><td>LG</td><td>MoE offloading 정책의 성능 에뮬레이션 시스템 연구임</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2610.33496'>FedSEAM: Federated Continual Learning of LLMs via Subspace Expert Agreement Merging</a></td><td>30</td><td>0</td><td>NLP</td><td>federated continual LLM의 expert merging으로 로봇 무관함</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2610.33922'>Learning Population Dynamics with Variational Doob-Wasserstein Flow</a></td><td>30</td><td>0</td><td>LG</td><td>WFR manifold의 population dynamics 학습 이론으로 무관함</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2610.33926'>Multitask Interactions in Recurrent Dynamics across 100 Cognitive Tasks</a></td><td>30</td><td>0</td><td>LG</td><td>RNN으로 100개 인지 과제의 상호작용을 분석하는 neuroscience 성격임</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2610.34158'>Last-Iterate Stationarity of Muon with Finitely Many Newton-Schulz Iterations</a></td><td>30</td><td>0</td><td>LG</td><td>Muon의 유한 Newton-Schulz 단계 수렴 이론임</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2610.34199'>SRA: Selective Residual Adaptation for LLM Reasoning Enhancement</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 추론 증류에 선택적 residual 적응을 더한 incremental임</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2610.34242'>Alignment via Generalization</a></td><td>30</td><td>0</td><td>LG</td><td>AI alignment를 일반화 관점으로 논하는 개념 논의임</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2610.34329'>SHIFT-JEV: Certified Abstention and Gain-Gated Continual Adaptation for LLM-Based Decision Models under Distribution Shift</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 의사결정 모델의 certified abstention 기법으로 무관함</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2610.34386'>ParetoRSI-Gym: Can AI Agents Improve Language Models Across Multiple Domains?</a></td><td>30</td><td>0</td><td>Agents</td><td>AI 에이전트의 LM 개선 능력을 재는 gym으로 무관함</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2610.34409'>Dynamic Multi-Step Decoding for Time-Series Foundation Models</a></td><td>30</td><td>0</td><td>LG</td><td>시계열 foundation model의 동적 multi-step 디코딩임</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2610.34440'>Speculative Decoding for Mixture-of-Experts Models: Expert Bytes, Kernel Bandwidth and the Best Draft Length</a></td><td>30</td><td>0</td><td>NLP</td><td>MoE 모델 speculative decoding의 expert bytes 분석임</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2610.34488'>Models Verify Sufficiency, Not Validity: Usable Falsehoods Evade the Checks that Gaps Trigger</a></td><td>30</td><td>0</td><td>NLP</td><td>모델이 충분성만 검증하고 타당성은 못 본다는 LLM 분석임</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2610.34566'>Error Diffusion Replaces Latent Weights: Training Binary-Weight Language Models on a Few Bits of Dithered State</a></td><td>30</td><td>0</td><td>LG</td><td>error diffusion으로 binary weight LM을 학습하는 효율화임</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2610.34679'>AT-AT: Automatic Tool Optimization from Agent Traces</a></td><td>30</td><td>0</td><td>Agents</td><td>agent trace로 도구를 자동 최적화하는 연구로 무관함</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2610.34690'>IsoAct: Geometry-Aware Post-hoc Debiasing via Isometric Actions</a></td><td>30</td><td>0</td><td>LG</td><td>isometric action으로 post-hoc debiasing을 하는 연구로 무관함</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2610.34756'>Mechanistic Insights into LoRA: Layer Sparsity for Adaptive Fine-Tuning via Path Patching</a></td><td>30</td><td>0</td><td>NLP</td><td>path patching으로 LoRA layer sparsity를 분석하는 연구임</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2610.34915'>End-to-End MXFP8 Reinforcement Learning on Blackwell: What Matching Buys, When It Pays Off, and How It Fails</a></td><td>30</td><td>0</td><td>RL</td><td>Blackwell에서 LLM RL을 MXFP8로 학습하는 시스템 연구임</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2610.34945'>Relational Composition as Parallel Transport: What Per-Entity Frames Force in Attention</a></td><td>30</td><td>0</td><td>LG</td><td>attention의 관계 합성을 parallel transport로 보는 이론임</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2610.35023'>BellowsKV: One Latent for Many Layers, Expanded on Demand</a></td><td>30</td><td>0</td><td>NLP</td><td>여러 layer가 하나의 latent KV를 공유하는 LLM 압축임</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2610.35101'>Spherical Brownian Diffusion for Language Modeling</a></td><td>30</td><td>0</td><td>NLP</td><td>구면 Brownian diffusion 언어 모델링임</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2610.35457'>Prior Predictive Matching for Bayesian LoRA</a></td><td>30</td><td>0</td><td>LG</td><td>Bayesian LoRA의 prior predictive matching임</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2610.35480'>GPDPO: Learning from Reward Conflicts via Group Pareto-Dominance Policy Optimization</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 다중 보상 충돌을 Pareto dominance로 푸는 정렬 연구임</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2610.35716'>Audit Where Hacks Pay: Budgeted Strong-Verifier Audits Against Reward Hacking in GRPO</a></td><td>30</td><td>0</td><td>RL</td><td>GRPO reward hacking에 strong verifier 감사를 예산 배분함, LLM 대상임</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2610.35787'>Selective Tie Learning: Mitigating Spurious Correlations in Preference Optimization</a></td><td>30</td><td>0</td><td>NLP</td><td>선호 최적화의 spurious 상관을 tie 학습으로 완화함</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2610.34971'>SVD-Attention: Efficiently Analyzing Attention Blocks in Transformers</a></td><td>30</td><td>0</td><td>Efficient Inference</td><td>head별 query-key 상호작용의 SVD 모드를 점수화해 low-rank 정도를 진단함. transformer 분석임</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2610.35411'>The Geometry of Emotion Representations Across Scale, Depth, and Instruction Tuning</a></td><td>30</td><td>0</td><td>NLP</td><td>Gemma 2 여섯 모델의 emotion representation geometry를 스케일·깊이·instruction tuning별로 분석함. 해석 연구이나 로보틱스 무관함.</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2610.35558'>EXCISE: Locating and Excising Distracting Sentences in Medical Question Answering</a></td><td>30</td><td>0</td><td>NLP</td><td>의료 QA에서 방해 문장을 hidden state 불일치로 찾아 attention을 막는 EXCISE를 제안함. 도메인 특화 inference-time 기법이며 로보틱스 무관함.</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2610.33178'>AOS-Bench: Can LLM Agents Manage Dynamic Workloads?</a></td><td>30</td><td>0</td><td>AI</td><td>coding agent가 CPU·메모리 제한 하에서 작업 스트림을 관리하는 능력을 재는 AOS-Bench임. 평가 벤치마크이며 로보틱스 무관함.</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2610.33180'>Propensities Please: Exposing Alignment-Faking LLMs using Synthetic Document Finetuning</a></td><td>30</td><td>0</td><td>AI</td><td>synthetic document finetuning으로 alignment-faking 모델의 잠재 misaligned 성향을 드러내는 방법임. LLM 안전성 연구이며 로보틱스 무관함.</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2610.33245'>AdaPRA: Process Reward Agents with Adaptive Rubrics for Data Science</a></td><td>30</td><td>0</td><td>AI</td><td>data science agent에 task별 rubric을 적응시키는 process reward agent AdaPRA임. DSPredict에서 순위 백분위가 오르나 로보틱스 무관함.</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2610.33330'>TempShap: When and How Much a Feature Matters in Time-Series Forecasting</a></td><td>30</td><td>0</td><td>LG</td><td>시계열 예측에서 입력 cell 단위 Shapley로 시점·horizon별 기여를 구하는 TempShap임. XAI 기여이며 로보틱스 무관함.</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2610.33391'>How To Build A Modern Diffusion Language Model</a></td><td>30</td><td>0</td><td>LG</td><td>discrete diffusion LLM 구축법을 개괄하는 튜토리얼·서베이임. 새 방법 없고 로보틱스 무관함.</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2610.33465'>LegoSR: A Unified Framework for Self-improving Agent-Guided Scientific Discovery</a></td><td>30</td><td>0</td><td>AI</td><td>7개 방정식 발견 방법을 묶은 agent 기반 LegoSR와 experience library임. 과학적 발견 응용이고 로보틱스 무관함.</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2610.33544'>Learning When to Collaborate: Selective Multi-Agent Medical Reasoning via Uncertainty-Aware Routing</a></td><td>30</td><td>0</td><td>Multimodal</td><td>의료 VQA에서 불확실할 때만 expert agent를 호출하는 SMART-Med을 GRPO로 학습함. 추론 시간 3.8배 감소하나 의료 도메인 한정임.</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2610.33771'>An actively trained neural operator for near-explicit atmospheric chemistry</a></td><td>30</td><td>0</td><td>LG</td><td>대기화학 near-explicit 메커니즘을 FNO-MoE로 emulate하고 expert 불일치로 active sampling함. 과학 시뮬레이션 응용이며 로보틱스 무관함.</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2610.34582'>HobbyLM: A Sparse Mixture-of-Experts Model Family on a Hobby Budget</a></td><td>30</td><td>0</td><td>LLM</td><td>저예산 sparse MoE 모델군 HobbyLM의 학습 경험을 기술한 보고임. 새로운 원리 없이 엔지니어링 위주임.</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2610.34640'>InferPriv: Evaluating Inferential Privacy Leakage in LLM Assistants</a></td><td>30</td><td>0</td><td>AI Safety</td><td>LLM 비서 답변에서 민감 속성이 간접 추론되는 inferential leakage를 재는 벤치마크임. 로봇과 무관함.</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2610.34659'>AdaTutor: Adaptive Tutoring through Pedagogical Strategy Selection</a></td><td>30</td><td>0</td><td>NLP</td><td>학생 오류에 맞는 교수 전략을 고르도록 학습하는 CPS 튜터링 프레임워크임. 수학·과학 데이터셋 평가이고 로봇과 무관함.</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2610.34722'>CEPO: A General Framework for Improving Prompt Optimization in Multi-Agent Systems</a></td><td>30</td><td>0</td><td>Agent</td><td>multi-agent 프롬프트 최적화에서 coordinator와 executor 프롬프트를 분리하는 CEPO임. 프롬프트 수준의 incremental 기여임.</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2610.34836'>Collective Emergent Alignment: Measuring and Amplifying Interaction-Induced Reasoning Alignment in Multi-Agent LLMs</a></td><td>30</td><td>0</td><td>Multi-agent LLM</td><td>multi-agent LLM 상호작용에서 생기는 reasoning alignment를 REMAP으로 정량화하고 사실 단위 통신을 제안함. 로봇과 무관함.</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2610.34866'>UniGFM-RAG: Unify Graph Foundation Models and Large Language Models for End-to-End Retrieval and Reasoning</a></td><td>30</td><td>0</td><td>NLP</td><td>GFM retriever와 LLM generator를 differentiable bridge로 end-to-end 학습하는 GraphRAG임. multi-hop QA 중심이고 로봇과 무관함.</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2610.35093'>Improving Instruction Hierarchy by Learning from Goal-Goal Conflicts</a></td><td>30</td><td>0</td><td>LLM Safety</td><td>goal-goal 충돌 예시로 Qwen3.5-9B 등을 fine-tuning해 instruction hierarchy를 개선함. 새 충돌 유형 지적은 있으나 로봇과 무관함.</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2610.35586'>Linear Probes Transfer from Base to Distilled Language Models despite Rotation</a></td><td>30</td><td>0</td><td>LLM Safety</td><td>base 모델에서 학습한 linear probe가 distilled·instruct 모델로 전이됨을 보임. 방향이 17~35도 회전해도 AUC 변화는 작음. 로봇과 무관함.</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2610.35595'>Agentic Algorithm Design: LLMs that Propose, Formalise, and Prove Runtime Bounds for Evolutionary Algorithms in Lean</a></td><td>30</td><td>0</td><td>Theory</td><td>LLM이 진화 알고리즘을 설계하고 Lean에서 runtime 상한을 증명하는 파이프라인임. 흥미로우나 로봇과 무관함.</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2610.35598'>Evolve on Graph: Self-Evolving Knowledge Graph Reasoning without Question Annotations</a></td><td>30</td><td>0</td><td>KG Reasoning</td><td>Proposer와 Solver self-play로 QA 주석 없이 KG 추론을 학습하는 Evolve on Graph임. 로봇과 무관함.</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2610.35690'>EvoRouter: Cost-Efficient Multi-Agent Routing via Insight-Guided On-Policy Distillation</a></td><td>30</td><td>0</td><td>Multi-agent</td><td>multi-agent 구성을 고르는 EvoRouter를 on-policy distillation으로 학습해 비용 50.95% 절감함. 로봇과 무관함.</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2610.33722'>Latent dynamics for reconstructing fine-scale PDE trajectories from coarse observations</a></td><td>29</td><td>0</td><td>LG</td><td>coarse 관측에서 PDE 궤적을 복원하는 latent dynamics로 무관함</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2610.33679'>Energy-Based Fault Detection and Isolation Framework for Flat Port-Hamiltonian Mechanical Systems</a></td><td>28</td><td>3</td><td>Fault Diagnosis</td><td>port-Hamiltonian 전력 잔차와 CWT-CNN으로 Kinova 고장 분류함. 정확도 84.7%로 momentum observer 97.2%보다 낮고 시뮬뿐임</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2610.33735'>Floor Friction Assessment from Robot Tire-Surface Interaction</a></td><td>28</td><td>3</td><td>Mobile Robot</td><td>IMU와 휠 odometry 속도 불일치 스펙트럼으로 5개 바닥 재질을 97.1% 분류함. 센싱 응용으로 학습 기여 약함</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2610.34128'>Semantic-Coupled Perception Framework for Autonomous Laparoscope Control</a></td><td>28</td><td>3</td><td>Surgical Robot</td><td>수술 phase 인식과 시각 추적을 결합한 복강경 FoV 제어임. 의료 특화이고 phantom 검증 수준임</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2610.35165'>How Tuning, Reference Preview, Actuator Modeling, and Fallback Policies Change Quadrotor Controller Comparisons: A Reproducible Simulation Study</a></td><td>28</td><td>3</td><td>Quadrotor</td><td>6종 제어기 비교가 tuning과 fallback에 따라 순위가 바뀜을 재현 가능하게 보임. 통제 연구이나 쿼드로터 제어 한정임</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2611.00097'>Pano2BIM: A Geometry-Constrained Vision-Language Agent for As-Built BIM Generation from a Floor Plan and a Single 360$^\circ$ Image</a></td><td>28</td><td>2</td><td>3D Vision</td><td>파노라마 BIM 생성 agent임</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2610.34789'>ISB-NMPC: Interception-Oriented Spherical-Bearing Nonlinear Model Predictive Control for Quadrotors</a></td><td>28</td><td>2</td><td>UAV Control</td><td>spherical-bearing NMPC로 쿼드로터 요격함. 시뮬 30회 86.7%와 실외 비행이 있으나 UAV 제어 특화임</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2610.33635'>DROA-CLIPSeg: Prompt-Guided Thin Crack Segmentation in Low-Light Conditions</a></td><td>28</td><td>1</td><td>CV</td><td>저조도 균열 분할임</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2610.34387'>From Human Intent to In-Orbit Action: A Self-Learning Large Language Model Agent for 6G Satellite Networks</a></td><td>28</td><td>1</td><td>Agents</td><td>6G 위성망 제어용 LLM 에이전트로 로봇과 무관함</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2610.34737'>LADDER: Diagnosing Domain-Level Self-Assessment Under Noisy Feedback</a></td><td>28</td><td>1</td><td>LLM Calibration</td><td>노이즈 피드백에서 모델이 도메인 자기평가를 형성하는지 진단함. 상호작용 경험에서 믿을 만한 자기평가를 못 만든다는 관찰이나 LM 한정임</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2610.35079'>Toward Fast Human Reaction Modeling from High-Frequency Digital Interaction Data</a></td><td>28</td><td>1</td><td>Behavior Modeling</td><td>Counter-Strike 2 telemetry로 빠른 반응 행동을 예측하는 EMBER·ORBIT 모델을 학습함. 탐색적이고 신경과학 해석은 저자도 가설 수준이라 함.</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2610.33263'>Explaining Basketball Shot Classifications with Grad-CAM: An Investigation of Shortcut Reliance with Spatiotemporal Correlations</a></td><td>28</td><td>0</td><td>CV</td><td>농구 슛 분류 Grad-CAM 분석임</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2610.33402'>Bidirectional Cross-frequency Domain Interaction Network for UHD Low-Light Image Enhancement</a></td><td>28</td><td>0</td><td>CV</td><td>UHD 저조도 개선 네트워크임</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2610.33551'>Cross-Scale Sparse Attention for Referring Segmentation in Remote Sensing</a></td><td>28</td><td>0</td><td>CV</td><td>원격탐사 referring segmentation임</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2610.34461'>Task Relevance-Driven Prompt Expansion for Federated Continual Learning</a></td><td>28</td><td>0</td><td>LG</td><td>federated continual learning prompt임</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2610.34520'>Conviction Without Evidence: Verdict Stability Is Independent of Visual Grounding in Medical Vision--Language Models</a></td><td>28</td><td>0</td><td>Multimodal</td><td>의료 VLM 시각 grounding 분석임</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2610.34685'>Good Rankings, Poor Choices? Rethinking Language-Only Vision-Language Model Selection</a></td><td>28</td><td>0</td><td>Multimodal</td><td>VLM 선택 재고찰임</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2610.35148'>Temporal Slice Learning for AI-Generated Video Detection with 400$\times$ Fewer FLOPs</a></td><td>28</td><td>0</td><td>Video</td><td>AI 생성 비디오 탐지 경량화임</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2610.33315'>MLIPDiff: Guiding Denoising Diffusion Models for Structure-Based Drug Design via Machine-Learned Interatomic Potentials</a></td><td>28</td><td>0</td><td>LG</td><td>물리 포텐셜로 약물 설계 diffusion을 유도하는 연구로 로봇과 무관함</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2610.33381'>The Cost of an Unknown Horizon for the Last Iterate of Clipped SGD under Heavy-Tailed Noise</a></td><td>28</td><td>0</td><td>LG</td><td>heavy-tail noise에서 clipped SGD last iterate 이론 분석임</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2610.33456'>FG-ConvNO: A Geometry-Aware Neural Operator for Propeller CFD Prediction</a></td><td>28</td><td>0</td><td>LG</td><td>프로펠러 CFD를 예측하는 geometry-aware neural operator로 무관함</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2610.33599'>H-GLow: Accelerating Graph Generation via Hazard-Guided Discrete Flow Matching</a></td><td>28</td><td>0</td><td>Generative</td><td>그래프 생성 discrete flow matching 가속으로 무관함</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2610.33880'>DIGEST: Discovery-Guided LLM Tuning for Symbolic Regression</a></td><td>28</td><td>0</td><td>LG</td><td>LLM 튜닝으로 기호 회귀를 돕는 연구로 무관함</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2610.34011'>Cross-User Adaptation for sEMG Gesture Recognition via Continual Learning</a></td><td>28</td><td>0</td><td>LG</td><td>sEMG 제스처 인식의 cross-user continual adaptation이며 보조기기 응용만 약하게 연결됨</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2610.34365'>SEEK: Skill Extraction with Evolving Knowledge against Frontier Science Agents</a></td><td>28</td><td>0</td><td>Agents</td><td>과학 에이전트의 skill 추출 기법으로 무관함</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2610.34682'>Beyond Multiplicity Correction: Sharp Retrieval Thresholds for Attention with Correlated Distractors</a></td><td>28</td><td>0</td><td>LG</td><td>상관된 distractor 하의 attention 검색 임계 이론임</td></tr>
<tr><td>486</td><td><a href='https://arxiv.org/abs/2610.34709'>Sparse Reconstruction by Direct Measurement-to-Field Generation in Function Space</a></td><td>28</td><td>0</td><td>Generative</td><td>측정값에서 필드를 직접 생성하는 희소 복원으로 무관함</td></tr>
<tr><td>487</td><td><a href='https://arxiv.org/abs/2610.34891'>Checkpoint Reload Explains Most of the Measured State Gap in Two State Discovery Reproductions</a></td><td>28</td><td>0</td><td>LG</td><td>state discovery 재현에서 checkpoint reload 영향을 밝힌 재현 연구임</td></tr>
<tr><td>488</td><td><a href='https://arxiv.org/abs/2610.35020'>Attention under Bounded Key-Query Similarity: Space Complexity and Transformer Anisotropy</a></td><td>28</td><td>0</td><td>NLP</td><td>KV 압축을 위한 key-query 유사도 한계의 공간 복잡도 이론임</td></tr>
<tr><td>489</td><td><a href='https://arxiv.org/abs/2610.35036'>Mapping the Solution-Set Structure of Grokking on Latin Squares</a></td><td>28</td><td>0</td><td>LG</td><td>Latin square에서 grokking 해 집합 구조를 분석함</td></tr>
<tr><td>490</td><td><a href='https://arxiv.org/abs/2610.35130'>TUON: A Tensor-Aware Optimizer Utilizing Tensor-SVD and Polarization for Large Language Model Pretraining</a></td><td>28</td><td>0</td><td>LG</td><td>tensor-SVD 기반 LLM 사전학습 optimizer임</td></tr>
<tr><td>491</td><td><a href='https://arxiv.org/abs/2610.35209'>Understanding Practical Optimization in Machine Learning</a></td><td>28</td><td>0</td><td>LG</td><td>실용 최적화 방법을 서술한 개괄 성격임</td></tr>
<tr><td>492</td><td><a href='https://arxiv.org/abs/2610.35504'>Model reduction in time: Learning flow maps for reducing stochastic dynamical systems in time</a></td><td>28</td><td>0</td><td>LG</td><td>확률 동역학을 시간 축으로 줄이는 flow map 연구임</td></tr>
<tr><td>493</td><td><a href='https://arxiv.org/abs/2610.35715'>Quantitative Generalization Bounds for Multi-Layer Transformers: A Few Long Strings can Beat Many Short Ones</a></td><td>28</td><td>0</td><td>LG</td><td>transformer 길이 일반화 한계 이론임</td></tr>
<tr><td>494</td><td><a href='https://arxiv.org/abs/2610.35955'>ResCom: Activation Residual Compensation for Large Language Model Quantization</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM 양자화의 activation residual 보상임</td></tr>
<tr><td>495</td><td><a href='https://arxiv.org/abs/2610.34027'>When Does GEPA Merge Help? A Mechanism-Level Diagnostic</a></td><td>28</td><td>0</td><td>NLP</td><td>GEPA merge 불안정이 설정 문제일 수 있음을 9개 구성 sweep으로 보임. prompt 최적화 진단임</td></tr>
<tr><td>496</td><td><a href='https://arxiv.org/abs/2610.34146'>Rethinking Retrieval in the Long-Context Era: Training-Free Semantic Trees for Adaptive Context Construction</a></td><td>28</td><td>0</td><td>RAG</td><td>전체 문서를 넣는 long-context 시대에 semantic tree로 증거를 선택함. 문맥 구성 기법임</td></tr>
<tr><td>497</td><td><a href='https://arxiv.org/abs/2610.34350'>Beyond the Opening: Tracing the First Token&#x27;s Persistent Influence on Reasoning Length</a></td><td>28</td><td>0</td><td>Reasoning</td><td>첫 토큰이 이후 생성을 거쳐 추론 길이에 지속 영향을 주는 경로를 분석함. 추론 모델 해석 연구임</td></tr>
<tr><td>498</td><td><a href='https://arxiv.org/abs/2610.35698'>From Self-Confidence to Statistical Accuracy: Scaling Human-in-the-Loop Evaluation with Direct and LLM-Assisted Auditing</a></td><td>28</td><td>0</td><td>LG</td><td>confidence 층화 샘플링과 LLM judge 오차 보정으로 정확도를 추정하는 통계 프레임워크임. 평가 방법론이며 로보틱스 무관함.</td></tr>
<tr><td>499</td><td><a href='https://arxiv.org/abs/2610.33470'>The Future Is Finer: Multivariate Time Series Super-Resolution Forecasting</a></td><td>28</td><td>0</td><td>LG</td><td>거친 해상도 시계열에서 세밀한 미래를 예측하는 MTS-SRF 과제와 TimeMagnifier를 제안함. 15개 baseline 대비 MSE 12.3% 감소이나 웹 시계열 한정이고 로보틱스 무관함.</td></tr>
<tr><td>500</td><td><a href='https://arxiv.org/abs/2610.33690'>PACE: Research Proving Agent for Adaptive Conjecture Exploration</a></td><td>28</td><td>0</td><td>AI</td><td>수학 conjecture 연구용 proving agent PACE와 evidence-tracking memory임. 51개 증명 과제 평가이며 로보틱스 무관함.</td></tr>
<tr><td>501</td><td><a href='https://arxiv.org/abs/2610.34614'>A Battery for AI Propensity Measurement: Rubrics, Synthetic Item Banks, and Annotations</a></td><td>28</td><td>0</td><td>AI Eval</td><td>AI 성향 28종 평가용 rubric과 합성 데이터셋을 공개한 자원 논문임. 로봇과 무관함.</td></tr>
<tr><td>502</td><td><a href='https://arxiv.org/abs/2610.34683'>Topic-Level Fairness in Retrieval-Augmented Generation</a></td><td>28</td><td>0</td><td>NLP</td><td>RAG에서 topic별 공정성을 맞추려 topic마다 reranker를 Bradley-Terry로 적응시킴. 로봇과 무관함.</td></tr>
<tr><td>503</td><td><a href='https://arxiv.org/abs/2610.34826'>TrustJev: Separating Policy Authority from Untrusted Evidence in LLM-Based Decisions</a></td><td>28</td><td>0</td><td>Security</td><td>지시 삽입 공격에 대비해 정책 점수와 외부 증거 보정을 분리하는 TrustJev임. 로봇과 무관한 LLM 보안 연구임.</td></tr>
<tr><td>504</td><td><a href='https://arxiv.org/abs/2610.35425'>From Denoising Dynamics to Endpoint Uncertainty in Diffusion Language Models</a></td><td>28</td><td>0</td><td>LM Uncertainty</td><td>diffusion 언어 모델의 denoising 궤적 수렴과 최종 출력 불확실성의 관계를 분석함. 로봇과 무관함.</td></tr>
<tr><td>505</td><td><a href='https://arxiv.org/abs/2611.03684'>Functional-Group Knowledge Is Structured in Language Models Before It Is Spoken</a></td><td>28</td><td>0</td><td>LLM Interpretability</td><td>LLM 내부 표현에서 작용기 지식이 출력보다 먼저 구조화됨을 분석함. 로봇과 무관함.</td></tr>
<tr><td>506</td><td><a href='https://arxiv.org/abs/2610.33413'>AV-FABLE: Audio-Visual Manipulation Forensics in Long-Form Videos</a></td><td>27</td><td>0</td><td>Video</td><td>오디오-비주얼 조작 포렌식임</td></tr>
<tr><td>507</td><td><a href='https://arxiv.org/abs/2610.33333'>Gaussian Approximation for Composition and Subsampling of Differentially Private Algorithms</a></td><td>27</td><td>0</td><td>LG</td><td>DP-SGD 합성 프라이버시의 Gaussian 근사 이론으로 로봇과 무관함</td></tr>
<tr><td>508</td><td><a href='https://arxiv.org/abs/2610.33668'>Beyond Affine Reconstruction: Multi-Resolution Transformer DeepONets for the Radiative Transfer Equation</a></td><td>27</td><td>0</td><td>LG</td><td>복사 전달 방정식용 multi-resolution DeepONet으로 무관함</td></tr>
<tr><td>509</td><td><a href='https://arxiv.org/abs/2610.33769'>CFL-aware edge design for graph neural solvers of hyperbolic transport</a></td><td>27</td><td>0</td><td>LG</td><td>쌍곡 PDE용 CFL 인지 GNN edge 설계로 무관함</td></tr>
<tr><td>510</td><td><a href='https://arxiv.org/abs/2610.33822'>Learning What to Share: Expert Specialization for Time-Series Forecasting</a></td><td>27</td><td>0</td><td>LG</td><td>시계열 예측에서 MoE 공유와 전문화를 다룬 연구로 무관함</td></tr>
<tr><td>511</td><td><a href='https://arxiv.org/abs/2610.33403'>Faithful Federated Tabular Data Synthesis</a></td><td>26</td><td>0</td><td>LG</td><td>federated 표 데이터 합성 연구로 로봇 무관함</td></tr>
<tr><td>512</td><td><a href='https://arxiv.org/abs/2610.33426'>Exact Unlearning After Data Curation</a></td><td>26</td><td>0</td><td>LG</td><td>데이터 curation 후 정확한 unlearning에 필요한 저장량 분석이며 무관함</td></tr>
<tr><td>513</td><td><a href='https://arxiv.org/abs/2610.33482'>Climate downscaling with likelihood functional flow matching</a></td><td>26</td><td>0</td><td>LG</td><td>기후 downscaling용 likelihood functional flow matching으로 무관함</td></tr>
<tr><td>514</td><td><a href='https://arxiv.org/abs/2610.33671'>Extraction meets Distillation - cryptanalytic techniques to recover parameters from a Deep Neural Network</a></td><td>26</td><td>0</td><td>LG</td><td>암호분석과 증류로 신경망 파라미터를 복원하는 연구로 무관함</td></tr>
<tr><td>515</td><td><a href='https://arxiv.org/abs/2610.33738'>Polynomial Residual Networks are Generically Identifiable</a></td><td>26</td><td>0</td><td>LG</td><td>다항 활성화 residual network의 식별성 증명임</td></tr>
<tr><td>516</td><td><a href='https://arxiv.org/abs/2610.33846'>When is early stopping beneficial under label noise? A phase diagram for kernel gradient flow</a></td><td>26</td><td>0</td><td>LG</td><td>label noise에서 early stopping 이득의 phase diagram 이론임</td></tr>
<tr><td>517</td><td><a href='https://arxiv.org/abs/2610.33872'>Stable Dimensionality Reduction via Isometric Centroid-Encoder</a></td><td>26</td><td>0</td><td>LG</td><td>class 기하를 고정하는 centroid-encoder 차원축소로 무관함</td></tr>
<tr><td>518</td><td><a href='https://arxiv.org/abs/2610.33967'>Performance of Neural Operator Baselines on &#x27;The Well&#x27; Dataset</a></td><td>26</td><td>0</td><td>LG</td><td>The Well 데이터셋의 neural operator baseline 재평가임</td></tr>
<tr><td>519</td><td><a href='https://arxiv.org/abs/2610.33985'>Constrained Gradient Equilibrium: Approachability under Locally Constrained Adversaries</a></td><td>26</td><td>0</td><td>LG</td><td>제약 online learning의 gradient equilibrium 이론임</td></tr>
<tr><td>520</td><td><a href='https://arxiv.org/abs/2610.34052'>Leveraging Dale&#x27;s Principle as an Inductive Bias in Recurrent Neural Networks</a></td><td>26</td><td>0</td><td>LG</td><td>Dale 원리를 RNN inductive bias로 쓰는 연구로 무관함</td></tr>
<tr><td>521</td><td><a href='https://arxiv.org/abs/2610.34140'>Decoupled Prune-and-Reconstruct: Training on a Compact Core with Double-Layer Sparsification</a></td><td>26</td><td>0</td><td>LG</td><td>GNN 메모리 절감을 위한 prune-and-reconstruct로 무관함</td></tr>
<tr><td>522</td><td><a href='https://arxiv.org/abs/2610.34173'>Reasoning or Just Prompting? Probing the Mechanism of Latent Chemical Reasoning</a></td><td>26</td><td>0</td><td>LG</td><td>화학 latent reasoning이 실제 추론인지 prompt 효과인지 분석으로 무관함</td></tr>
<tr><td>523</td><td><a href='https://arxiv.org/abs/2610.34639'>Cross-Loop Query Handoff: How Later Loops Redirect Two-Hop Retrieval in the Ouro Looped Language Models</a></td><td>26</td><td>0</td><td>NLP</td><td>Ouro looped LM의 two-hop 검색 메커니즘 분석임</td></tr>
<tr><td>524</td><td><a href='https://arxiv.org/abs/2610.34801'>When Does Data Value Reduce to Class Balance? A Coverage View of Per-Point Data Valuation</a></td><td>26</td><td>0</td><td>LG</td><td>per-point data valuation이 class balance로 환원되는 조건 분석임</td></tr>
<tr><td>525</td><td><a href='https://arxiv.org/abs/2610.34816'>Can System-1-Style Decision Models Replace Dedicated Rerankers in RAG? A Systems Evaluation</a></td><td>26</td><td>0</td><td>NLP</td><td>RAG에서 System-1 결정 모델이 reranker를 대체하는지 평가함</td></tr>
<tr><td>526</td><td><a href='https://arxiv.org/abs/2610.35112'>Subspace Crystallization in Grokking: Rank Compression Tracks the Phase Transition</a></td><td>26</td><td>0</td><td>LG</td><td>grokking 전이를 rank 압축으로 추적하는 분석임</td></tr>
<tr><td>527</td><td><a href='https://arxiv.org/abs/2610.35345'>Should Pseudo-Labels Share Mini-Batches with Labeled Examples? Semi-Supervised Continual Active Learning with Limited Training Cost</a></td><td>26</td><td>0</td><td>LG</td><td>pseudo-label과 labeled 배치 공유를 보는 소규모 continual AL 연구임</td></tr>
<tr><td>528</td><td><a href='https://arxiv.org/abs/2610.35356'>Benchmarking uncertainty quantification for engineering regression under graded distribution shift</a></td><td>26</td><td>0</td><td>LG</td><td>공학 회귀의 분포 이동 UQ 벤치마크임</td></tr>
<tr><td>529</td><td><a href='https://arxiv.org/abs/2610.35472'>Amplify, Locate, Estimate (ALE) on Rare-Failure Rates of Fine-Tuned LLMs</a></td><td>26</td><td>0</td><td>NLP</td><td>안전 fine-tuning된 LLM의 희귀 실패율 추정 방법임</td></tr>
<tr><td>530</td><td><a href='https://arxiv.org/abs/2610.35766'>Improving Signals, Declining Encoder: A Known-Answer Test of Label-Free Monitoring in Self-Supervised Learning</a></td><td>26</td><td>0</td><td>LG</td><td>SSC 학습의 label-free 모니터링 신호가 틀릴 수 있음을 검증함</td></tr>
<tr><td>531</td><td><a href='https://arxiv.org/abs/2610.35957'>Distributed LLM Inference via Communication-Efficient Speculative Decoding</a></td><td>26</td><td>0</td><td>NLP</td><td>기기-서버 분산 speculative decoding 통신 효율화임</td></tr>
<tr><td>532</td><td><a href='https://arxiv.org/abs/2610.35985'>Let the Gate Decide: Per-Lookup Precision for Quantized Conditional Memory in LLMs</a></td><td>26</td><td>0</td><td>NLP</td><td>LLM conditional memory 조회별 정밀도 선택임</td></tr>
<tr><td>533</td><td><a href='https://arxiv.org/abs/2610.35743'>SEMA-Auto: Sighted and Efficient Multi-Turn Attack with Autonomy</a></td><td>26</td><td>0</td><td>NLP</td><td>multi-turn jailbreak attacker SEMA-Auto를 합성 bootstrap과 decision-supervised RL로 학습함. 공격 성공률 개선 위주이며 로보틱스 무관함.</td></tr>
<tr><td>534</td><td><a href='https://arxiv.org/abs/2610.33623'>Graph-dependent pooling: adaptive granularity in hierarchical graph neural networks</a></td><td>26</td><td>0</td><td>LG</td><td>그래프별로 pooling 단위를 정하는 GDPool을 제안함. 분자·MOF 그래프 벤치마크 한정이고 로보틱스 무관함.</td></tr>
<tr><td>535</td><td><a href='https://arxiv.org/abs/2610.34203'>MatOS: An Agent Operating System for Materials Research</a></td><td>26</td><td>0</td><td>AI</td><td>재료 연구용 agent 운영체제 MatOS와 asset graph·evolution임. 도메인 특화 시스템이며 로보틱스 무관함.</td></tr>
<tr><td>536</td><td><a href='https://arxiv.org/abs/2610.34747'>Query-Driven Learning for Lifted Reasoning</a></td><td>26</td><td>0</td><td>Reasoning</td><td>lifted 수준의 query-driven 학습·추론에서 필요충분조건과 quasi-polynomial 알고리즘을 증명한 이론 논문임. 로봇과 무관함.</td></tr>
<tr><td>537</td><td><a href='https://arxiv.org/abs/2610.34873'>Localization-Uncertainty-Aware UAV Swarm Search for GNSS-Denied Maritime Surveillance</a></td><td>25</td><td>3</td><td>UAV Swarm</td><td>cascading 위치 공분산을 Fisher 정보로 근사해 CBF에 반영함. GNSS 부재 swarm 탐색 제어이며 학습 요소 약함</td></tr>
<tr><td>538</td><td><a href='https://arxiv.org/abs/2610.35040'>Context-dependent Runtime Construction of Safe Regions of Attraction from Design-Time Identification for Multi-Candidate Simplex Architectures</a></td><td>25</td><td>3</td><td>Safe Control</td><td>contraction 기반 RoA 인증과 context별 safe RoA 구성임. 안전 제어 이론이고 로봇 학습과 거리 있음</td></tr>
<tr><td>539</td><td><a href='https://arxiv.org/abs/2610.35231'>Thermal-Headroom Routing for Efficient Robot Perception in Extreme Heat</a></td><td>25</td><td>3</td><td>Efficient Perception</td><td>RC 열 모델로 throttling을 피하는 detector 선택 정책임. 시뮬 지연 3.9-7.5점 감소이고 시스템 엔지니어링임</td></tr>
<tr><td>540</td><td><a href='https://arxiv.org/abs/2610.34130'>StickFigure: Enabling Pose-Only IoT Cameras for Privacy-Preserving Edge Vision</a></td><td>25</td><td>2</td><td>CV</td><td>pose 전용 프라이버시 카메라임</td></tr>
<tr><td>541</td><td><a href='https://arxiv.org/abs/2610.34795'>Towards Spatio-Temporal Intelligence Systems in Urban Space: A Twin-Agent Perspective</a></td><td>25</td><td>2</td><td>LG</td><td>도시 시공간 지능 twin-agent 관점 글임</td></tr>
<tr><td>542</td><td><a href='https://arxiv.org/abs/2610.33715'>Quantum Closed Loop Inverse Kinematics Through Hilbert-Space Encoding of Robot Kinematics</a></td><td>25</td><td>2</td><td>Quantum Kinematics</td><td>양자 회로로 기구학과 Jacobian을 표현하고 폐루프 IK를 제시함. 이론적 equivalence만 있고 실용성과 relevance 낮음</td></tr>
<tr><td>543</td><td><a href='https://arxiv.org/abs/2610.33906'>Sybil-Resilient Multi-Drone Exploration of Indoor and Confined Spaces</a></td><td>25</td><td>2</td><td>Multi-drone Security</td><td>Sybil 공격에 대한 센서 기반 방어를 70개 지도에서 평가함. 보안 중심이고 학습 요소 없음</td></tr>
<tr><td>544</td><td><a href='https://arxiv.org/abs/2610.34583'>The German Tank Problem &amp; Navigating by Scent</a></td><td>25</td><td>2</td><td>Olfactory Search</td><td>German tank 추정기로 최대 농도와 도착 여부를 판단하는 간단한 통계 규칙임. 우아하나 후각 탐색 틈새 주제임</td></tr>
<tr><td>545</td><td><a href='https://arxiv.org/abs/2610.34163'>Reinforcement Learning for Adaptive Crowd Flow Control Using Dynamic Barriers</a></td><td>25</td><td>1</td><td>RL</td><td>군중 흐름 제어 RL 응용임</td></tr>
<tr><td>546</td><td><a href='https://arxiv.org/abs/2610.34210'>MIS-VQA: An Annotation-Driven Surgical Vision-Language Dataset for Complex Surgical Understanding</a></td><td>25</td><td>1</td><td>Multimodal</td><td>수술 VQA 데이터셋임</td></tr>
<tr><td>547</td><td><a href='https://arxiv.org/abs/2610.34597'>Finetuning Prompt-Based Image Editor for Geometry-Consistent Room Defurnishing</a></td><td>25</td><td>1</td><td>Generative</td><td>방 가구 제거 편집임</td></tr>
<tr><td>548</td><td><a href='https://arxiv.org/abs/2610.35450'>OBB-PBD: Extending Parallel Box Decoding to Oriented Bounding Boxes for Referring Expression Grounding in Aerial Imagery</a></td><td>25</td><td>1</td><td>Multimodal</td><td>항공 영상 oriented box grounding임</td></tr>
<tr><td>549</td><td><a href='https://arxiv.org/abs/2610.34735'>iPrefBench: A User-Centric Benchmark for Personalized Mobile Use Agents</a></td><td>25</td><td>1</td><td>Agents</td><td>사용자 이력에서 빠진 정보를 추론하고 필요 시 묻는 모바일 agent 벤치마크임. 언어 agent 평가임</td></tr>
<tr><td>550</td><td><a href='https://arxiv.org/abs/2610.34790'>BehaviorMem: Building and Evaluating User Memory from Real-World E-Commerce Behavior Streams</a></td><td>25</td><td>1</td><td>User Memory</td><td>전자상거래 행동 로그에서 user memory를 구축하고 평가함. 개인화 응용임</td></tr>
<tr><td>551</td><td><a href='https://arxiv.org/abs/2610.35773'>A Unified Arena for LLM Agents across Diverse Eurogame</a></td><td>25</td><td>1</td><td>Agent Eval</td><td>Eurogame 10종에서 LLM agent 12개 구성을 비교하는 DECE arena임. 로봇과 무관함.</td></tr>
<tr><td>552</td><td><a href='https://arxiv.org/abs/2610.33340'>Compression of Vision Foundation Models for Retinal OCT via Growing-Neural-Gas Codebooks and Graph-Guided Masked Image Modeling</a></td><td>25</td><td>0</td><td>CV</td><td>망막 OCT 모델 압축임</td></tr>
<tr><td>553</td><td><a href='https://arxiv.org/abs/2610.33398'>Rethinking Microscopy Generation: Co-Designed Diffusion for Biologically Interpretable Single-Cell Synthesis</a></td><td>25</td><td>0</td><td>Generative</td><td>현미경 단일 세포 합성 diffusion임</td></tr>
<tr><td>554</td><td><a href='https://arxiv.org/abs/2610.33518'>Component Pooling Trained Across Orientations for Few-Shot Remote Sensing Scene Classification</a></td><td>25</td><td>0</td><td>CV</td><td>원격탐사 few-shot 분류임</td></tr>
<tr><td>555</td><td><a href='https://arxiv.org/abs/2610.33520'>Promise and Limits of Cross-Architecture Knowledge Distillation for Lightweight Medical Vision Transformers (LiteMed-ViT)</a></td><td>25</td><td>0</td><td>CV</td><td>의료 ViT 지식 증류 분석임</td></tr>
<tr><td>556</td><td><a href='https://arxiv.org/abs/2610.33639'>UniQuery: Unifying Vision Models with a Joint Query Head for Cross-Domain Pedestrian Attribute Recognition</a></td><td>25</td><td>0</td><td>CV</td><td>보행자 속성 인식임</td></tr>
<tr><td>557</td><td><a href='https://arxiv.org/abs/2610.33641'>LENS: Likelihood Evaluation and Neighbor Smoothing for Attribute-Based Person Retrieval on Unseen Cameras</a></td><td>25</td><td>0</td><td>CV</td><td>속성 기반 사람 검색임</td></tr>
<tr><td>558</td><td><a href='https://arxiv.org/abs/2610.33695'>Scalable Unrolled Chains for MRI Reconstruction</a></td><td>25</td><td>0</td><td>CV</td><td>MRI 재구성 unrolled 학습임</td></tr>
<tr><td>559</td><td><a href='https://arxiv.org/abs/2610.33910'>Texture-Aware Strategies for Subregion Style Transfer Augmentation</a></td><td>25</td><td>0</td><td>CV</td><td>style transfer augmentation임</td></tr>
<tr><td>560</td><td><a href='https://arxiv.org/abs/2610.34305'>Learning Discriminative Prototypes via Boundary Repulsion MixUp for Object Re-Identification</a></td><td>25</td><td>0</td><td>CV</td><td>object re-ID prototype 학습임</td></tr>
<tr><td>561</td><td><a href='https://arxiv.org/abs/2610.34346'>Spatially-Aware Self-Organizing Graph Autoencoders via Localized Hebbian Learning</a></td><td>25</td><td>0</td><td>LG</td><td>Hebbian graph autoencoder임</td></tr>
<tr><td>562</td><td><a href='https://arxiv.org/abs/2610.34432'>On Detection Reliability for Small Object Segmentation</a></td><td>25</td><td>0</td><td>CV</td><td>작은 물체 분할 신뢰도 연구임</td></tr>
<tr><td>563</td><td><a href='https://arxiv.org/abs/2610.34561'>GRASP: Group-Adaptive Hybrid RL-SFT Post-Training for Medical VQA without Reasoning Annotations</a></td><td>25</td><td>0</td><td>Multimodal</td><td>의료 VQA RL-SFT 후학습임</td></tr>
<tr><td>564</td><td><a href='https://arxiv.org/abs/2610.34618'>P2P-Former: Bridging the Supervision Gap Between Point and Proposal in Temporal Action Localization</a></td><td>25</td><td>0</td><td>Video</td><td>point-supervised 행동 localization임</td></tr>
<tr><td>565</td><td><a href='https://arxiv.org/abs/2610.34734'>FGD2HF: Frequency-guided Dual-domain Hypergraph Fusion for Semantic Segmentation</a></td><td>25</td><td>0</td><td>CV</td><td>주파수 hypergraph 분할임</td></tr>
<tr><td>566</td><td><a href='https://arxiv.org/abs/2610.34765'>Efficient Multi-modal Video Fusion Network with Dynamic Region-Guided Temporal Interaction</a></td><td>25</td><td>0</td><td>Video</td><td>다중 모달 비디오 융합임</td></tr>
<tr><td>567</td><td><a href='https://arxiv.org/abs/2610.34766'>Factorized Gradients for Scalable Highly-expressive Parametric Diffeomorphisms</a></td><td>25</td><td>0</td><td>LG</td><td>diffeomorphism gradient 분해임</td></tr>
<tr><td>568</td><td><a href='https://arxiv.org/abs/2610.35017'>When Pointing Becomes Profiling: Social Bias and Refusal in Text-Steerable Visual Encoders</a></td><td>25</td><td>0</td><td>Multimodal</td><td>text-steerable 인코더 편향 분석임</td></tr>
<tr><td>569</td><td><a href='https://arxiv.org/abs/2610.35566'>Copying As Defense: Protecting Images from Editing By Eliciting Model Copying</a></td><td>25</td><td>0</td><td>Generative</td><td>편집 방어 이미지 보호임</td></tr>
<tr><td>570</td><td><a href='https://arxiv.org/abs/2610.33514'>Overlap-Aware Sub-hypergraph Pattern Frequencies for Hypergraph-Level Classification</a></td><td>25</td><td>0</td><td>LG</td><td>hypergraph 분류용 sub-hypergraph 패턴 빈도 기법으로 무관함</td></tr>
<tr><td>571</td><td><a href='https://arxiv.org/abs/2610.33784'>Greedy Orthogonal Polynomial Manifolds with Lipschitz Control for Dimensionality Reduction and Reduced Modeling</a></td><td>25</td><td>0</td><td>LG</td><td>polynomial manifold 차원축소로 무관함</td></tr>
<tr><td>572</td><td><a href='https://arxiv.org/abs/2610.33258'>Two Uncertainties Are Not One: Disagreement versus Decision-Risk in Cheap Structured Content Moderation</a></td><td>25</td><td>0</td><td>NLP</td><td>저가 frozen 모델의 콘텐츠 중재 판정을 142,658건 라벨로 외부 감사함. 불확실성 분해 관점이나 로봇 무관함</td></tr>
<tr><td>573</td><td><a href='https://arxiv.org/abs/2610.33371'>How Does Post-Training Shape LLM Value Preferences?</a></td><td>25</td><td>0</td><td>NLP</td><td>post-training 경로별 의견 혼합이 가치 선호에 미치는 영향을 통제 실험함. 정렬 분석이고 로봇 무관함</td></tr>
<tr><td>574</td><td><a href='https://arxiv.org/abs/2610.33441'>Quantifying Meaning with SCAPE-T: Semantic Complexity from Encoder-Only Transformer Attention</a></td><td>25</td><td>0</td><td>NLP</td><td>attention 기반 코드 길이로 의미 복잡도를 재는 SCAPE-T 지표임. 언어학 응용이고 로봇 무관함</td></tr>
<tr><td>575</td><td><a href='https://arxiv.org/abs/2610.34809'>Position Matters More Than Channel: Talking a Language Model Out of a Correct Answer</a></td><td>25</td><td>0</td><td>NLP</td><td>조언의 위치, 작성자, 모델 자신의 이전 답 중 무엇이 정답을 흔드는지 분리함. LM 설득 취약성 분석임</td></tr>
<tr><td>576</td><td><a href='https://arxiv.org/abs/2610.35142'>CalibraRL: Confidence-Calibrated Reinforcement Learning for Mitigating Hallucinations in RAG</a></td><td>25</td><td>0</td><td>RAG RL</td><td>신뢰도별 보상으로 과신 오류와 불필요한 기권을 줄이는 RL임. RAG 환각 완화이고 로봇 무관함</td></tr>
<tr><td>577</td><td><a href='https://arxiv.org/abs/2610.34623'>One Mean Log-Mel Vector per Phoneme: Simple and Fast Text Injection for Speech Recognition</a></td><td>25</td><td>0</td><td>Speech</td><td>음소별 평균 log-mel 벡터로 TTS 대신 text injection을 해 ASR 학습을 1.8배 빠르게 함. 로봇과 무관한 음성 인식 연구임.</td></tr>
<tr><td>578</td><td><a href='https://arxiv.org/abs/2610.35160'>AutoEnergyDesign: An LLM-Driven Agent for Automatic Energy System Design Optimization</a></td><td>25</td><td>0</td><td>Agent</td><td>LLM agent가 시뮬레이션 결과를 보고 건물 에너지 시스템 설계를 반복 개선하는 AutoEnergyDesign임. 최적화 baseline 대비 소폭 개선이고 로봇과 무관함.</td></tr>
<tr><td>579</td><td><a href='https://arxiv.org/abs/2610.35316'>RSIV-Harness: A Recursive Self-Improvement Harness Framework for Open-Domain Conversational Text-to-Visualization</a></td><td>25</td><td>0</td><td>Agent</td><td>실패 trace로 harness를 재귀적으로 고치는 RSIV-Harness와 text-to-visualization 벤치마크임. 로봇과 무관함.</td></tr>
<tr><td>580</td><td><a href='https://arxiv.org/abs/2610.35582'>Distributed Predictive Flocking for a Swarm of Miniature Vibration-Driven Robots in a Confined Arena</a></td><td>24</td><td>2</td><td>Swarm</td><td>분산 NMPC flocking에서 CBF 안전 formulation 6종을 bristlebot digital twin으로 비교함. 학습 요소 없는 swarm 제어 비교임</td></tr>
<tr><td>581</td><td><a href='https://arxiv.org/abs/2610.35212'>One-Shot Federated Model Editing for Device Dynamics at the Edge</a></td><td>24</td><td>1</td><td>LG</td><td>device dynamics를 one-shot federated로 편집하며 로봇 연결 약함</td></tr>
<tr><td>582</td><td><a href='https://arxiv.org/abs/2610.33557'>Nowcasting aerosol particle size distributions from PM2.5 with physics-regularized flow matching</a></td><td>24</td><td>0</td><td>LG</td><td>PM2.5로 에어로졸 크기 분포를 nowcasting하는 flow matching으로 무관함</td></tr>
<tr><td>583</td><td><a href='https://arxiv.org/abs/2610.33619'>Geodesic-SVDD Latent Mixup for One-Shot Distributed Tabular Learning</a></td><td>24</td><td>0</td><td>LG</td><td>분산 표 학습용 latent mixup 기법으로 무관함</td></tr>
<tr><td>584</td><td><a href='https://arxiv.org/abs/2610.33832'>EEGBiFormer: Real-Time EEG Attention Classification via Hybrid CNN-Transformer with EEG-Informed Auditory Protocol Validation</a></td><td>24</td><td>0</td><td>LG</td><td>EEG 주의 분류 CNN-Transformer로 무관함</td></tr>
<tr><td>585</td><td><a href='https://arxiv.org/abs/2610.33835'>Hessian-Similar Optimization with Capped Participation: Lower Bounds and Virtual Masters</a></td><td>24</td><td>0</td><td>LG</td><td>client 참여 제한 하의 Hessian-similar 최적화 하한 이론임</td></tr>
<tr><td>586</td><td><a href='https://arxiv.org/abs/2610.33885'>Min-Marginal Power Indices for Multi-Objective Feature Selection</a></td><td>24</td><td>0</td><td>LG</td><td>feature selection의 min-marginal 지표 연구로 무관함</td></tr>
<tr><td>587</td><td><a href='https://arxiv.org/abs/2610.34018'>BriLLM-MetaPred: A Representation-Prediction Unity Language Model with Adaptive Self-Measurement</a></td><td>24</td><td>0</td><td>NLP</td><td>BriLLM-MetaPred 언어모델로 이론 근거가 약함</td></tr>
<tr><td>588</td><td><a href='https://arxiv.org/abs/2610.34023'>The Symmetry of Differential Neural Tangent Kernel under the Orthogonal Group</a></td><td>24</td><td>0</td><td>LG</td><td>differential NTK의 직교군 대칭성 이론임</td></tr>
<tr><td>589</td><td><a href='https://arxiv.org/abs/2610.34495'>Approximate Unlearning in Prototype-based-classifiers</a></td><td>24</td><td>0</td><td>LG</td><td>prototype 분류기 근사 unlearning으로 무관함</td></tr>
<tr><td>590</td><td><a href='https://arxiv.org/abs/2610.34934'>A Certified Robustness Framework for Backdoor Poisoning Attacks using $f$-Divergences</a></td><td>24</td><td>0</td><td>LG</td><td>f-divergence 기반 backdoor poisoning 인증 강건성 이론임</td></tr>
<tr><td>591</td><td><a href='https://arxiv.org/abs/2610.34962'>Beyond feature attribution: Recovering latent interaction structures in machine learning models via localized CBFI</a></td><td>24</td><td>0</td><td>LG</td><td>표 모델의 잠재 상호작용 구조 복원으로 무관함</td></tr>
<tr><td>592</td><td><a href='https://arxiv.org/abs/2610.35108'>FlowGenesis: Representation-Driven Self-Organization of Neural Architectures</a></td><td>24</td><td>0</td><td>LG</td><td>표현 기반 아키텍처 자기조직화이며 근거가 약함</td></tr>
<tr><td>593</td><td><a href='https://arxiv.org/abs/2610.35113'>UTA: Universal Training Adaptive Learning Rate Decay</a></td><td>24</td><td>0</td><td>LG</td><td>범용 learning rate decay 제안으로 incremental임</td></tr>
<tr><td>594</td><td><a href='https://arxiv.org/abs/2610.35551'>Balanced Sampling in Stochastic Multi-objective Bandits</a></td><td>24</td><td>0</td><td>RL</td><td>stochastic multi-objective bandit의 balanced sampling 이론임</td></tr>
<tr><td>595</td><td><a href='https://arxiv.org/abs/2610.35652'>Active Learning of Conditional Generative Models via the Transport Neural Tangent Kernel</a></td><td>24</td><td>0</td><td>Generative</td><td>transport NTK로 조건부 생성 모델을 active learning함</td></tr>
<tr><td>596</td><td><a href='https://arxiv.org/abs/2610.35845'>Work Agents: Systems, Capabilities, and Optimization</a></td><td>24</td><td>0</td><td>Agents</td><td>digital work agent 개괄 서베이임</td></tr>
<tr><td>597</td><td><a href='https://arxiv.org/abs/2610.35989'>Layerwise Repacking: Variable-Length Hybrid-Attention Training without an Extra Redistribution Pass</a></td><td>24</td><td>0</td><td>NLP</td><td>가변 길이 hybrid attention 학습의 layerwise repacking임</td></tr>
<tr><td>598</td><td><a href='https://arxiv.org/abs/2610.36009'>DuplexTune: Coupled-State Replay for Memory-Efficient Mixture-of-Experts Adaptation</a></td><td>24</td><td>0</td><td>NLP</td><td>MoE adaptation의 coupled-state replay 메모리 절감임</td></tr>
<tr><td>599</td><td><a href='https://arxiv.org/abs/2610.35475'>MANTIS: Multi-Axis News Transformations for Instance-Wise Stress Testing and Worst-Case Training in Fake News Detection</a></td><td>24</td><td>0</td><td>NLP</td><td>fake news 탐지용 다축 rewrite 공격 벤치마크와 instance-adaptive worst-case 학습을 제안함. 로보틱스 무관한 robustness 연구임.</td></tr>
<tr><td>600</td><td><a href='https://arxiv.org/abs/2610.35846'>Preserve to Expand: Source-Aware Adaptation and Model Merging for Multilingual LLM-Based ASR</a></td><td>24</td><td>0</td><td>NLP</td><td>speech LLM connector를 새 언어로 확장할 때 source 언어 forgetting을 막는 merging 전략(SSU-Wanda+TIES)을 비교함. 다국어 ASR 한정임.</td></tr>
<tr><td>601</td><td><a href='https://arxiv.org/abs/2610.33592'>Auditing evaluation artifacts and data leakage in large language model systems for rare disease diagnosis</a></td><td>24</td><td>0</td><td>AI</td><td>희귀질환 진단 LLM 평가의 데이터 누수를 감사해 Recall@1이 54.3%에서 40.3%로 내려감을 보임. 평가 방법론 비판이며 로보틱스 무관함.</td></tr>
<tr><td>602</td><td><a href='https://arxiv.org/abs/2610.33674'>Meta-CLIP: Metadata-Conditioned Contrastive Learning for Zero-Shot Disease Inference</a></td><td>24</td><td>0</td><td>Multimodal</td><td>DICOM 메타데이터로 CLIP negative를 reweight하는 Meta-CLIP임. CT-RATE AUROC 1.41 상승의 의료 도메인 소폭 개선임.</td></tr>
<tr><td>603</td><td><a href='https://arxiv.org/abs/2610.34107'>Can LLMs Trust Appropriately? Evaluating Calibrated Reliance on Imperfect Partners</a></td><td>24</td><td>0</td><td>AI</td><td>LLM이 불완전한 파트너 증거로 신뢰·검증 결정을 얼마나 최적에 가깝게 하는지 324개 시나리오로 평가함. 로보틱스 무관함.</td></tr>
<tr><td>604</td><td><a href='https://arxiv.org/abs/2610.34185'>R2A-Sales: A Policy-Atom-Matched Benchmark for Rule-to-Action Gaps in Goal-Directed Sales Agents</a></td><td>24</td><td>0</td><td>AI</td><td>판매 agent가 규칙을 말할 수 있어도 행동에서는 지키지 못하는 rule-to-action 격차 벤치마크 R2A-Sales임. 중국어 판매 도메인 한정이며 로보틱스 무관함.</td></tr>
<tr><td>605</td><td><a href='https://arxiv.org/abs/2610.35193'>Trustworthy Recursive Self-Improvement in the Era of Large Models: Foundation, Risks, Evaluation and Open Challenges</a></td><td>24</td><td>0</td><td>Survey</td><td>대형 모델의 recursive self-improvement 신뢰성에 대한 survey임. 로봇과 무관함.</td></tr>
<tr><td>606</td><td><a href='https://arxiv.org/abs/2610.35630'>Revisiting Direct Control: A Field Evaluation of Sensor Fusion Efficacy in Teleoperating Full-Scale Autonomous Vehicles via Bird&#x27;s Eye View</a></td><td>22</td><td>3</td><td>Teleoperation</td><td>실제 차량에서 18명으로 카메라, LiDAR BEV, 융합 BEV 인터페이스를 비교한 현장 실험임. HCI 평가이고 학습 무관함</td></tr>
<tr><td>607</td><td><a href='https://arxiv.org/abs/2610.34034'>Enabling Motion-Induced WiFi-CSI Sensing in Multi-Robot Systems: A Simulation Framework</a></td><td>22</td><td>2</td><td>Sensing Sim</td><td>WiFi-CSI 센싱을 Gazebo에 통합한 시뮬 프레임워크임. 도구 기여이고 학습과 무관함</td></tr>
<tr><td>608</td><td><a href='https://arxiv.org/abs/2610.34059'>Lightweight Change Detection for Adaptive Collective Perception in Dynamic Environments</a></td><td>22</td><td>2</td><td>Swarm</td><td>상수 메모리 변화 감지로 swarm 집단 인지를 개선함. Webots 시뮬이고 로봇 학습 무관함</td></tr>
<tr><td>609</td><td><a href='https://arxiv.org/abs/2610.34653'>Heard Enough to Act: Early Tool Calling in Spoken Dialogue Systems</a></td><td>22</td><td>1</td><td>Spoken Agents</td><td>발화가 충분히 실행 가능해지는 가장 이른 시점을 합성 데이터로 감독함. 음성 agent 지연 문제임</td></tr>
<tr><td>610</td><td><a href='https://arxiv.org/abs/2610.33200'>Isharah-Selfie: Continuous Sign Language Recognition Dataset for One-handed Signing</a></td><td>22</td><td>1</td><td>CV</td><td>스마트폰 셀피 촬영 아랍 수어 데이터셋 Isharah-Selfie(8,997 클립)를 구축하고 CSLR/SLT 벤치마크함. 데이터 기여 위주임.</td></tr>
<tr><td>611</td><td><a href='https://arxiv.org/abs/2610.35516'>Learning High-Quality Pseudo-Labels for Point-Supervised Temporal Action Localization</a></td><td>22</td><td>0</td><td>Video</td><td>point-supervised 행동 pseudo-label임</td></tr>
<tr><td>612</td><td><a href='https://arxiv.org/abs/2610.33531'>Clustering of High-Dimensional Human Gene Score Data for Target Cell Classification</a></td><td>22</td><td>0</td><td>LG</td><td>유전자 점수 데이터 군집 수 비교 연구로 무관함</td></tr>
<tr><td>613</td><td><a href='https://arxiv.org/abs/2610.33609'>Satellite-derived bathymetry of Arabian Gulf ports under leakage-free validation: a multi-site benchmark of empirical, machine-learning and deep-learning models against 285,000 multibeam soundings, with an outlook for UAE waters</a></td><td>22</td><td>0</td><td>LG</td><td>아라비아만 위성 수심 측정의 누수 없는 검증 벤치마크로 무관함</td></tr>
<tr><td>614</td><td><a href='https://arxiv.org/abs/2610.33964'>QECGBERT: A Scalable ECG Foundation Model Based on Self-Supervised Language Learning via VQ-VAE Waveform Tokenization</a></td><td>22</td><td>0</td><td>LG</td><td>ECG foundation model로 무관함</td></tr>
<tr><td>615</td><td><a href='https://arxiv.org/abs/2610.33994'>Resolving the Mobility-Equity-Emissions Trilemma: A Causal Machine Learning Framework for Dynamic Tolling Policy</a></td><td>22</td><td>0</td><td>LG</td><td>동적 도로 요금 정책용 인과 ML로 무관함</td></tr>
<tr><td>616</td><td><a href='https://arxiv.org/abs/2610.34154'>Edge-Centric Adaptive Neural Activation via Parametric Tanh Functions</a></td><td>22</td><td>0</td><td>LG</td><td>parametric tanh 활성화 제안으로 기여가 작음</td></tr>
<tr><td>617</td><td><a href='https://arxiv.org/abs/2610.34227'>Interpretable and Steerable Molecular Graph Generation using Concept Bottlenecks</a></td><td>22</td><td>0</td><td>LG</td><td>concept bottleneck 분자 그래프 생성으로 무관함</td></tr>
<tr><td>618</td><td><a href='https://arxiv.org/abs/2610.35052'>Risk-Aware Output Control Should be the Focus of Machine Unlearning</a></td><td>22</td><td>0</td><td>LG</td><td>risk-aware output control을 주장하는 unlearning position paper임</td></tr>
<tr><td>619</td><td><a href='https://arxiv.org/abs/2610.35147'>Locked In: Multi-Objective RL for the AI Data Center Build-Out</a></td><td>22</td><td>0</td><td>RL</td><td>AI 데이터센터 건설의 다목적 RL로 무관함</td></tr>
<tr><td>620</td><td><a href='https://arxiv.org/abs/2610.35164'>Accelerating SO(2)-Equivariant Materials Models through Low-Precision Emulation</a></td><td>22</td><td>0</td><td>LG</td><td>SO(2) 등변 재료 모델의 저정밀 가속으로 무관함</td></tr>
<tr><td>621</td><td><a href='https://arxiv.org/abs/2610.35190'>LEAP: a Latent Embedding Anomaly Patch-Transformer for time-series anomaly detection</a></td><td>22</td><td>0</td><td>LG</td><td>latent patch transformer 시계열 이상 탐지로 무관함</td></tr>
<tr><td>622</td><td><a href='https://arxiv.org/abs/2610.35215'>SkillLifeBench: Benchmarking Security Across the Lifecycle of Agent Skills</a></td><td>22</td><td>0</td><td>Agents</td><td>웹 에이전트 skill 수명주기 보안 벤치마크임</td></tr>
<tr><td>623</td><td><a href='https://arxiv.org/abs/2610.35545'>Efficient probabilistic weather forecasting at quarter-degree resolution with two-sided transport attention</a></td><td>22</td><td>0</td><td>LG</td><td>quarter-degree 확률 날씨 예측 transport로 무관함</td></tr>
<tr><td>624</td><td><a href='https://arxiv.org/abs/2610.35568'>ExCal: Optimization-Free Multivariate Time Series Anomaly Detection via Excess Calibration</a></td><td>22</td><td>0</td><td>LG</td><td>normal-only 시계열 이상 탐지 ExCal로 무관함</td></tr>
<tr><td>625</td><td><a href='https://arxiv.org/abs/2610.35663'>SCAFFOLD under Hessian Similarity: Sharp Convergence Rates</a></td><td>22</td><td>0</td><td>LG</td><td>SCAFFOLD의 Hessian similarity 수렴률 이론임</td></tr>
<tr><td>626</td><td><a href='https://arxiv.org/abs/2610.35693'>GNN-VIEW: Visual Inspection and Explanation of Graph-based Earth-System Models</a></td><td>22</td><td>0</td><td>LG</td><td>지구시스템 GNN 시각 검사 도구임</td></tr>
<tr><td>627</td><td><a href='https://arxiv.org/abs/2610.35727'>TRACE: Memory-Efficient Time Series Class-Incremental Learning via Temporal-Spectral Reconstruction</a></td><td>22</td><td>0</td><td>LG</td><td>시계열 class-incremental 메모리 효율 방법으로 무관함</td></tr>
<tr><td>628</td><td><a href='https://arxiv.org/abs/2610.35740'>LUCID: Local Understanding of Covariate Importance with Conditional Density Estimation</a></td><td>22</td><td>0</td><td>LG</td><td>조건부 밀도 추정 기반 변수 중요도 방법임</td></tr>
<tr><td>629</td><td><a href='https://arxiv.org/abs/2610.33969'>&quot;High-Quality&quot; Data for Early-Stage Instruction Tuning: An Empirical Study of Data Quality Metrics</a></td><td>22</td><td>0</td><td>NLP</td><td>instruction tuning 데이터 품질 지표별 구간 fine-tuning으로 유용성을 비교함. 데이터 선택 경험 연구임</td></tr>
<tr><td>630</td><td><a href='https://arxiv.org/abs/2610.34074'>Identically Trained Language Models Break on Different Jailbreaks</a></td><td>22</td><td>0</td><td>NLP</td><td>같은 데이터 pretraining도 seed마다 깨지는 jailbreak가 다름을 150개 모델로 보임. 안전 평가 분석임</td></tr>
<tr><td>631</td><td><a href='https://arxiv.org/abs/2610.35082'>CoSA: The Conflict of Skills Attack in Real-World LLM Agent Ecosystems</a></td><td>22</td><td>0</td><td>Agent Security</td><td>Skill을 조합할 때 재사용된 산출물이 권한 제한을 잃는 Conflict of Skills를 분석함. agent 보안임</td></tr>
<tr><td>632</td><td><a href='https://arxiv.org/abs/2610.35671'>Evaluating DeepSeek V4.1 Flash-1017 for loss of control and harmful manipulation risks</a></td><td>22</td><td>0</td><td>NLP</td><td>DeepSeek V4.1 Flash의 loss of control·manipulation 위험을 34개 벤치마크로 평가함. 안전성 평가 보고서이며 로보틱스 무관함.</td></tr>
<tr><td>633</td><td><a href='https://arxiv.org/abs/2610.35826'>Understanding Jev-Style System One Models: Does Structure Reduce Selection Bias?</a></td><td>22</td><td>0</td><td>NLP</td><td>Jev 계열 System One 모델의 선택지 순서 편향을 option shuffle 8회로 측정함. 정확도는 같아도 실패 집합이 27.3-28.5% 커진다는 분석이나 로보틱스 무관함.</td></tr>
<tr><td>634</td><td><a href='https://arxiv.org/abs/2610.33323'>AI Teaches Humans to Handle Complexity in the Game of Go</a></td><td>22</td><td>0</td><td>AI</td><td>바둑에서 spectral radius 기반 strategic tension 지표로 인간·AI 의사결정 차이를 분석함. 로보틱스와 거리 멂.</td></tr>
<tr><td>635</td><td><a href='https://arxiv.org/abs/2610.33617'>When Generated Information Returns: Error Persistence in LLM-Mediated Information Ecosystems</a></td><td>22</td><td>0</td><td>AI</td><td>LLM이 쓴 글이 재입력될 때 오류가 남는 현상을 통제 실험으로 분석함. 로보틱스 무관함.</td></tr>
<tr><td>636</td><td><a href='https://arxiv.org/abs/2610.33767'>Local Entropy Fluctuations for Black-Box LLM-Generated Text Detection</a></td><td>22</td><td>0</td><td>NLP</td><td>entropy 궤적의 국소 peak로 LLM 생성 텍스트를 탐지하는 RelPPR임. 로보틱스 무관함.</td></tr>
<tr><td>637</td><td><a href='https://arxiv.org/abs/2610.34701'>Movable-Element Multi-Functional RIS-Assisted Hybrid RSMA-NOMA: A Constrained Hybrid Reinforcement Learning Approach</a></td><td>22</td><td>0</td><td>RL</td><td>movable-element RIS 무선 통신의 에너지 효율을 hybrid MARL로 최적화함. RL 응용이나 통신 도메인이라 로봇과 무관함.</td></tr>
<tr><td>638</td><td><a href='https://arxiv.org/abs/2610.35403'>NeSySpec: Neuro-Symbolic Technical Intelligence for Auditing Engineering Specifications with an Application to Aircraft</a></td><td>22</td><td>0</td><td>Neuro-symbolic</td><td>Logic Tensor Network로 항공기 사양 오류를 진단하고 수정하는 NeSySpec임. 도메인 특화이고 로봇과 무관함.</td></tr>
<tr><td>639</td><td><a href='https://arxiv.org/abs/2610.35486'>ShutdownMod: Turning Any Trajectory into a Shutdown Evaluation</a></td><td>22</td><td>0</td><td>AI Safety</td><td>agent trajectory에 shutdown 요청을 주입해 종료 순응도를 재는 ShutdownMod임. 코딩 agent 평가이고 로봇과 무관함.</td></tr>
<tr><td>640</td><td><a href='https://arxiv.org/abs/2610.33713'>Traffic-Context-Aware Driver Emotion Recognition with Expectation-Deviation-Driven Inference</a></td><td>20</td><td>1</td><td>CV</td><td>운전자 감정 인식임</td></tr>
<tr><td>641</td><td><a href='https://arxiv.org/abs/2610.33448'>BoardSafety: AI-Ready Data from Manufacturer Documentation for Development-Board Safety</a></td><td>20</td><td>1</td><td>AI</td><td>개발 보드 데이터시트에서 안전 규칙을 뽑아 LLM 안전 판단을 평가하는 BoardSafety 벤치마크임. 하드웨어 실험 보조 맥락이나 로보틱스와 거리 멂.</td></tr>
<tr><td>642</td><td><a href='https://arxiv.org/abs/2610.33243'>Automated identification of ivory carvings using machine learning: A proof-of-concept approach to detecting the illegal wildlife trade</a></td><td>20</td><td>0</td><td>CV</td><td>상아 조각 식별 응용 연구임</td></tr>
<tr><td>643</td><td><a href='https://arxiv.org/abs/2610.33691'>PathKGen: Pathology Knowledge Assisted MLLM for Explainable Histopathology</a></td><td>20</td><td>0</td><td>Multimodal</td><td>병리 MLLM임</td></tr>
<tr><td>644</td><td><a href='https://arxiv.org/abs/2610.33988'>Hybrid Mamba-Transformer Network for Single-Shot 3D Reconstruction from Fringe Patterns</a></td><td>20</td><td>0</td><td>3D Vision</td><td>fringe 투영 3D 재구성임</td></tr>
<tr><td>645</td><td><a href='https://arxiv.org/abs/2610.34221'>CropReward: A Human-Preference Benchmark and Reward Model for Aesthetic Image Cropping</a></td><td>20</td><td>0</td><td>CV</td><td>이미지 크롭 reward 모델임</td></tr>
<tr><td>646</td><td><a href='https://arxiv.org/abs/2610.34939'>Fed-MAPTrack: Federated Modality-aware Prompt Tuning for RGB-X Tracking</a></td><td>20</td><td>0</td><td>CV</td><td>federated RGB-X tracking임</td></tr>
<tr><td>647</td><td><a href='https://arxiv.org/abs/2610.35368'>Shared-Factor-Conditioned Diffusion for Low-Rank Tensor Recovery</a></td><td>20</td><td>0</td><td>LG</td><td>low-rank tensor 복원 diffusion임</td></tr>
<tr><td>648</td><td><a href='https://arxiv.org/abs/2610.35375'>ACSAN: All-Convolutional Self-Attention Network Integrating Convolutional Operations with Vision Transformer</a></td><td>20</td><td>0</td><td>CV</td><td>ViT와 conv 결합 구조임</td></tr>
<tr><td>649</td><td><a href='https://arxiv.org/abs/2610.35491'>S$^2$-RL: Sample-Set Dual Reinforcement Learning for Generative Semantic Segmentation Dataset Distillation</a></td><td>20</td><td>0</td><td>CV</td><td>분할 dataset distillation RL임</td></tr>
<tr><td>650</td><td><a href='https://arxiv.org/abs/2610.35515'>HiFiPix: Bringing High-Fidelity Real-World Super-Resolution Back to Pixel Space</a></td><td>20</td><td>0</td><td>CV</td><td>초해상 pixel space임</td></tr>
<tr><td>651</td><td><a href='https://arxiv.org/abs/2610.33298'>All-in-One: A Composable Attack on LLM Transformations</a></td><td>20</td><td>0</td><td>LG</td><td>LLM 변환 composable 공격임</td></tr>
<tr><td>652</td><td><a href='https://arxiv.org/abs/2610.33739'>A quantum k-nearest neighbors implementation using magnitude-aware comparisons</a></td><td>20</td><td>0</td><td>LG</td><td>양자 kNN 구현 연구로 무관함</td></tr>
<tr><td>653</td><td><a href='https://arxiv.org/abs/2610.34159'>Single-Cycle Battery Remaining Useful Life Prediction with Compressed Continuous Wavelet Features and Deep Neural Networks</a></td><td>20</td><td>0</td><td>LG</td><td>배터리 잔여 수명 예측으로 무관함</td></tr>
<tr><td>654</td><td><a href='https://arxiv.org/abs/2610.34459'>From Explaining to Enabling: Actionable Transparency in Algorithmic Insurance Pricing</a></td><td>20</td><td>0</td><td>LG</td><td>보험 가격 알고리즘의 actionable transparency로 무관함</td></tr>
<tr><td>655</td><td><a href='https://arxiv.org/abs/2610.34549'>MOFjson: An Explicit Topological Representation of Metal-Organic Frameworks for Language Models</a></td><td>20</td><td>0</td><td>LG</td><td>MOF 구조를 json으로 표현하는 언어모델 연구로 무관함</td></tr>
<tr><td>656</td><td><a href='https://arxiv.org/abs/2610.34812'>Precedence-Aware Resource Allocation: Extending the AUTOC Framework to Multi-Level Treatments</a></td><td>20</td><td>0</td><td>LG</td><td>다단계 처치 자원 할당 통계 방법으로 무관함</td></tr>
<tr><td>657</td><td><a href='https://arxiv.org/abs/2610.34950'>MINT: Mitigating Structural Inconsistency via Attentive Message Passing for Financial Anomaly Detection</a></td><td>20</td><td>0</td><td>LG</td><td>금융 이상 계정 탐지 GNN으로 무관함</td></tr>
<tr><td>658</td><td><a href='https://arxiv.org/abs/2610.35032'>AutoPRL: Automated Path Representation Learning via a Learnable View Generator</a></td><td>20</td><td>0</td><td>LG</td><td>경로 표현 학습의 view generator로 무관함</td></tr>
<tr><td>659</td><td><a href='https://arxiv.org/abs/2610.35128'>STeP-TS: Shared Temporal Filters with Pruning for Time Series</a></td><td>20</td><td>0</td><td>LG</td><td>시계열 예측용 공유 시간 필터와 pruning으로 무관함</td></tr>
<tr><td>660</td><td><a href='https://arxiv.org/abs/2610.35175'>DAC-Loop: Distillation-Aware Compression for Remote Sensing CNN</a></td><td>20</td><td>0</td><td>CV</td><td>원격탐사 CNN 증류 압축으로 무관함</td></tr>
<tr><td>661</td><td><a href='https://arxiv.org/abs/2610.35211'>Efficient Exact Unlearning for Federated Zeroth-Order Optimization</a></td><td>20</td><td>0</td><td>LG</td><td>federated zeroth-order 최적화의 정확한 unlearning임</td></tr>
<tr><td>662</td><td><a href='https://arxiv.org/abs/2610.35262'>Conversational Generalized Linear Bandits with Hybrid Feedback</a></td><td>20</td><td>0</td><td>LG</td><td>conversational bandit 이론으로 무관함</td></tr>
<tr><td>663</td><td><a href='https://arxiv.org/abs/2610.35313'>CoPE-CGL: Community-aware Prototype Extraction for Replay-Free Continual Graph Learning</a></td><td>20</td><td>0</td><td>LG</td><td>continual graph learning prototype 추출로 무관함</td></tr>
<tr><td>664</td><td><a href='https://arxiv.org/abs/2610.35355'>OneEEG: A Unified Signal-Visual Multimodal Language Model with Task-Aware Mixture of Projectors for Multi-Task EEG Understanding</a></td><td>20</td><td>0</td><td>Multimodal</td><td>EEG 신호-시각 멀티모달 언어모델로 무관함</td></tr>
<tr><td>665</td><td><a href='https://arxiv.org/abs/2610.35658'>A Hybrid Framework for Explainable Aviation Risk: Causal Chain Extraction from Safety Reports with Physics-Based Failure Quantification and Interventional Analysis</a></td><td>20</td><td>0</td><td>NLP</td><td>항공 안전 보고서의 인과 사슬 추출로 무관함</td></tr>
<tr><td>666</td><td><a href='https://arxiv.org/abs/2610.35785'>A theory of noisy linear recurrent neural network learning dynamics</a></td><td>20</td><td>0</td><td>LG</td><td>noisy linear RNN 학습 동역학 이론임</td></tr>
<tr><td>667</td><td><a href='https://arxiv.org/abs/2610.35958'>Exponential Wake-Up Overshoot in Explicit Gaussian Point-Process Filters</a></td><td>20</td><td>0</td><td>LG</td><td>점과정 필터의 wake-up overshoot 이론임</td></tr>
<tr><td>668</td><td><a href='https://arxiv.org/abs/2610.35965'>Generalization in Learning: Eyring Formula and Predator-prey Model</a></td><td>20</td><td>0</td><td>LG</td><td>일반화를 포식자-피식자 모델로 비유해 근거가 약함</td></tr>
<tr><td>669</td><td><a href='https://arxiv.org/abs/2610.33239'>Hey, guess what: CUES lead to inferences about typicality</a></td><td>20</td><td>0</td><td>NLP</td><td>사건 전형성 추론을 위한 코퍼스 EventTyp을 구축하고 사람과 모델을 비교함. 언어학 연구임</td></tr>
<tr><td>670</td><td><a href='https://arxiv.org/abs/2610.33433'>Examining form-based linguistic productivity in people and large language models</a></td><td>20</td><td>0</td><td>NLP</td><td>새 동사를 쓰는 형태 기반 생산성을 사람과 LM이 어떻게 일반화하는지 비교함. 인지언어학 연구임</td></tr>
<tr><td>671</td><td><a href='https://arxiv.org/abs/2610.33542'>SEDATE: Do Large Language Models Share an Aggression Circuit Across Languages?</a></td><td>20</td><td>0</td><td>NLP</td><td>다국어 공격성 circuit 공유 여부를 분석함. 안전 해석가능성 연구이고 무관함</td></tr>
<tr><td>672</td><td><a href='https://arxiv.org/abs/2610.33741'>Beyond Prompts: A Systematic Study of LLM-Based Machine Translation Evaluators</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 번역 평가자의 지시, few-shot, 모델 선택 효과를 WMT24·25에서 분석함. MT 평가 연구임</td></tr>
<tr><td>673</td><td><a href='https://arxiv.org/abs/2610.34294'>Factual Yet One-Sided: Stance Poisoning and Evidence Balancing in Retrieval-Augmented Generation</a></td><td>20</td><td>0</td><td>RAG Security</td><td>사실은 맞되 입장이 한쪽인 문서를 주입하면 RAG 응답 stance가 쏠림을 보임. RAG 공격 연구임</td></tr>
<tr><td>674</td><td><a href='https://arxiv.org/abs/2610.34768'>DynEdit: Dynamic Entropy-Guided Sequential Editing for Large Language Models</a></td><td>20</td><td>0</td><td>NLP</td><td>token entropy로 편집 노력을 배분하는 지식 편집임. LLM 편집 기법임</td></tr>
<tr><td>675</td><td><a href='https://arxiv.org/abs/2610.34875'>RubriX: A Fast, Fine-Tunable Non-Autoregressive Rubric Judge</a></td><td>20</td><td>0</td><td>NLP</td><td>encoder 임베딩과 cosine softmax로 rubric 수준을 빠르게 판정함. 평가 모델 효율화임</td></tr>
<tr><td>676</td><td><a href='https://arxiv.org/abs/2610.35083'>Ask Before You Answer: A Question-Driven Evidence Reasoning Architecture (QERA) for In-Context Learning</a></td><td>20</td><td>0</td><td>NLP</td><td>요청이 규격이 아니라는 관찰로 질문 기반 증거 추론을 설계함. 생활 문맥 학습 응용임</td></tr>
<tr><td>677</td><td><a href='https://arxiv.org/abs/2610.35416'>ImgMT: Wikipedia-based Dataset For Evaluating Text-in-Image Translation</a></td><td>20</td><td>0</td><td>NLP</td><td>Wikimedia SVG 기반 text-in-image 번역 벤치마크 ImgMT(129개 언어)를 구축함. 데이터셋 기여이며 로보틱스 무관함.</td></tr>
<tr><td>678</td><td><a href='https://arxiv.org/abs/2610.35461'>A Contextual Measure of Ambiguity in Prescriptive Text</a></td><td>20</td><td>0</td><td>NLP</td><td>규정 텍스트의 ambiguity를 이해관계자 간 해석 불일치로 정량화하는 측도를 제안함. 법·정책 NLP이고 로보틱스 무관함.</td></tr>
<tr><td>679</td><td><a href='https://arxiv.org/abs/2610.33277'>GEMS-RAG: Graph-grounded Engineering Multimodal Standards Retrieval-Augmented Generation</a></td><td>20</td><td>0</td><td>AI</td><td>공학 표준 문서용 multimodal graph RAG인 GEMS-RAG를 MUTCD에 적용함. 문서 QA 도메인 특화임.</td></tr>
<tr><td>680</td><td><a href='https://arxiv.org/abs/2610.33451'>A Comprehensive Framework for All Stages of Large-Model Training: From Data and Tokenization, through Pretraining, to Post-Training Alignment</a></td><td>20</td><td>0</td><td>AI</td><td>LLM 학습 전 단계를 395개 참고문헌으로 정리한 서베이임. 로보틱스 무관함.</td></tr>
<tr><td>681</td><td><a href='https://arxiv.org/abs/2610.33644'>AlphaIdeaBench: Benchmarking Automated Research Idea Generation under Feasibility Constraints with Peer Review Alignment</a></td><td>20</td><td>0</td><td>AI</td><td>자원 제약 하 research ideation agent 평가 벤치마크 AlphaIdeaBench(100개 과제)임. 로보틱스 무관함.</td></tr>
<tr><td>682</td><td><a href='https://arxiv.org/abs/2610.33651'>Jointly Modeling Preferences and Imperfect Decision-Making in Large Language Models</a></td><td>20</td><td>0</td><td>AI</td><td>LLM의 선호와 불완전 최적화를 inverse game으로 추정하는 PBM임. 사회 딜레마 게임 분석이며 로보틱스 무관함.</td></tr>
<tr><td>683</td><td><a href='https://arxiv.org/abs/2610.33788'>Unlocking the Specialization Capability of PPG Foundation Models for Wearable Signals through Structured Pruning and Adaptive Fine-Tuning</a></td><td>20</td><td>0</td><td>LG</td><td>PPG foundation model을 structured pruning 후 fine-tuning하는 SPAFT임. 웨어러블 생체신호 도메인 한정임.</td></tr>
<tr><td>684</td><td><a href='https://arxiv.org/abs/2610.33804'>Beyond Static Structures: Linking Protein Dynamics to Function via DynaReason-Pro</a></td><td>20</td><td>0</td><td>LG</td><td>단백질 conformational ensemble에서 GO term과 기능 rationale을 예측하는 DynaReason-Pro임. 생물 도메인이며 로보틱스 무관함.</td></tr>
<tr><td>685</td><td><a href='https://arxiv.org/abs/2610.33929'>WebViSE: Scaling Visual Design Intelligence from the Open Web for LLM Website Generation</a></td><td>20</td><td>0</td><td>AI</td><td>웹사이트에서 Visual Skill을 추출해 DAG 라이브러리로 만드는 WebViSE임. 웹 디자인 생성이며 로보틱스 무관함.</td></tr>
<tr><td>686</td><td><a href='https://arxiv.org/abs/2610.34705'>Safe by Benchmark, Unsafe in Practice: Lessons from 1331 Child-Related AI Incidents</a></td><td>20</td><td>0</td><td>AI Safety</td><td>아동 관련 AI 사고 1331건을 코딩해 피해 분류 체계를 만든 사회적 분석임. 로봇과 무관함.</td></tr>
<tr><td>687</td><td><a href='https://arxiv.org/abs/2610.34777'>Scope-Gap Injection: Exploiting Evaluator Channel Blind Spots in the OpenClaw Agent Security Competition</a></td><td>20</td><td>0</td><td>AI Safety</td><td>첨부 파일 경로로 LLM agent 안전 평가를 우회하는 Scope-Gap Injection 공격 보고임. 로봇과 무관함.</td></tr>
<tr><td>688</td><td><a href='https://arxiv.org/abs/2610.34956'>Decision Model Factory: Building Specialized Sovereign Decision Models</a></td><td>20</td><td>0</td><td>LLM</td><td>일본어 등 특화 결정 모델을 만드는 Decision Model Factory 워크플로우 보고임. 엔지니어링 중심이고 로봇과 무관함.</td></tr>
<tr><td>689</td><td><a href='https://arxiv.org/abs/2610.35080'>Zero-Shot Multi-Class Wafer Map Classification with Rule-Ordered Prompts for Large Multimodal Models</a></td><td>20</td><td>0</td><td>CV</td><td>웨이퍼 맵 결함을 rule 순서 프롬프트로 zero-shot 분류함. 산업 응용 프롬프트 설계이고 로봇과 무관함.</td></tr>
<tr><td>690</td><td><a href='https://arxiv.org/abs/2610.35138'>Co-Design Bench: Multimodal Collaborative Coding Evaluation for Agentic Models</a></td><td>20</td><td>0</td><td>Benchmark</td><td>실사용자 코딩 세션에서 뽑은 273개 과제의 Co-Design Bench임. 로봇과 무관한 코딩 agent 평가임.</td></tr>
<tr><td>691</td><td><a href='https://arxiv.org/abs/2610.35218'>MuSID-KD: Multigranularity Knowledge Distillation for Generative Recommendation with Semantic IDs</a></td><td>20</td><td>0</td><td>RecSys</td><td>semantic ID 생성형 추천의 multi-granularity distillation MuSID-KD임. 로봇과 무관함.</td></tr>
<tr><td>692</td><td><a href='https://arxiv.org/abs/2610.35430'>Faithful Explanations under Missing Modalities in Multimodal Dementia Prognosis</a></td><td>20</td><td>0</td><td>Medical</td><td>결측 modality에서 치매 예후 설명의 faithfulness를 평가함. 로봇과 무관함.</td></tr>
<tr><td>693</td><td><a href='https://arxiv.org/abs/2610.35606'>ArchiveLens: A Generative Spatial Knowledge Framework for Semantic Reconstruction of Historical Maps</a></td><td>20</td><td>0</td><td>GIS</td><td>역사 지도 Sanborn 445장을 건물 분할과 VLM 속성 파싱으로 구조화하는 ArchiveLens임. 로봇과 무관함.</td></tr>
<tr><td>694</td><td><a href='https://arxiv.org/abs/2610.35753'>CLOSURE: Cross-Channel Closure for Multivariate Time Series Anomaly Detection</a></td><td>20</td><td>0</td><td>Time Series</td><td>복원과 채널 간 일관성을 따로 평가하는 시계열 이상 탐지 CLOSURE임. 로봇과 무관함.</td></tr>
<tr><td>695</td><td><a href='https://arxiv.org/abs/2610.34849'>Physics-Informed and Data-Driven Composite Disturbance Separation and Predictive Control for Airborne Electro-Optical Gimbals with Multiple Constraints</a></td><td>18</td><td>2</td><td>Control</td><td>주기·비주기 외란을 분리한 gimbal MPC임. LSTM 예측이 들어가나 항공 광학 제어 특화임</td></tr>
<tr><td>696</td><td><a href='https://arxiv.org/abs/2610.34913'>Quantile-Based Command-Reserve MPC for Current-Command Gimbal Pointing</a></td><td>18</td><td>2</td><td>Control</td><td>quantile 외란 예측과 tube MPC로 gimbal 지향 제어함. 하드웨어 검증은 있으나 학습 relevance 낮음</td></tr>
<tr><td>697</td><td><a href='https://arxiv.org/abs/2610.35342'>VisGeo-PipeTrack: A Visual Geometric Servo Control Framework with MPC-RCAPID Control for UAV-Based Dynamic Pipes Tracking</a></td><td>18</td><td>2</td><td>UAV Servo</td><td>YOLOv5 라벨과 MPC-RCAPID로 움직이는 파이프 추적함. 응용 제어이고 새로운 학습 아이디어 없음</td></tr>
<tr><td>698</td><td><a href='https://arxiv.org/abs/2610.34304'>Real-Time Conveyor Belt Defect Detection via Edge TPU-Accelerated YOLOv11 on Raspberry Pi 5</a></td><td>18</td><td>1</td><td>CV</td><td>컨베이어 결함 검출 엣지 배포임</td></tr>
<tr><td>699</td><td><a href='https://arxiv.org/abs/2610.34569'>Agentic AI Orchestration Framework for Spatial Intelligence: Supply Chain Deployment</a></td><td>18</td><td>1</td><td>Agent</td><td>공급망 공간 의사결정용 multi-agent 오케스트레이션 아키텍처의 현장 POC 보고임. 통제 실험 없고 로봇 관련성 낮음.</td></tr>
<tr><td>700</td><td><a href='https://arxiv.org/abs/2610.33416'>How Robust Are CNNs and Vision Transformers for Alzheimer&#x27;s MRI Classification Across Datasets?</a></td><td>18</td><td>0</td><td>CV</td><td>알츠하이머 MRI 분류 robustness 비교임</td></tr>
<tr><td>701</td><td><a href='https://arxiv.org/abs/2610.33479'>Energy Efficient Lung Tumor Segmentation with a modified CBAM ENet Skip Model</a></td><td>18</td><td>0</td><td>CV</td><td>폐 종양 분할 경량 모델임</td></tr>
<tr><td>702</td><td><a href='https://arxiv.org/abs/2610.33554'>End-to-end prostate lesion segmentation and detection from undersampled diffusion-weighted MRI</a></td><td>18</td><td>0</td><td>CV</td><td>전립선 병변 분할임</td></tr>
<tr><td>703</td><td><a href='https://arxiv.org/abs/2610.33580'>ZoomSEM: accelerating large-scale brain connectomics with intelligent SEM super-resolution</a></td><td>18</td><td>0</td><td>CV</td><td>SEM 초해상 응용임</td></tr>
<tr><td>704</td><td><a href='https://arxiv.org/abs/2610.34148'>MuSTEL: A Large-Scale Multilingual Synthetic Text-Line Image Dataset for OCR</a></td><td>18</td><td>0</td><td>CV</td><td>OCR 합성 데이터셋임</td></tr>
<tr><td>705</td><td><a href='https://arxiv.org/abs/2610.34742'>From Sentinel-2 to 1-m Imagery: Real-World $\times 10$ Cross-Sensor Super-Resolution via Visual Autoregressive Modeling</a></td><td>18</td><td>0</td><td>CV</td><td>위성 초해상임</td></tr>
<tr><td>706</td><td><a href='https://arxiv.org/abs/2610.34876'>CoDeRNet: Selective Cross-Task Routing under Heterogeneous Supervision for Change Detection and Captioning</a></td><td>18</td><td>0</td><td>CV</td><td>원격탐사 변화 탐지 및 캡셔닝임</td></tr>
<tr><td>707</td><td><a href='https://arxiv.org/abs/2610.34879'>LayoutMamba: Efficient Document Layout Analysis with Hybrid Mamba-Transformer Networks</a></td><td>18</td><td>0</td><td>CV</td><td>문서 레이아웃 분석임</td></tr>
<tr><td>708</td><td><a href='https://arxiv.org/abs/2610.34925'>Rethinking Data Imbalance in Class Incremental Surgical Instrument Segmentation</a></td><td>18</td><td>0</td><td>CV</td><td>수술 기구 class-incremental 분할임</td></tr>
<tr><td>709</td><td><a href='https://arxiv.org/abs/2611.00099'>A Novel Lightweight Multi-Scale Branching Encoder for Few-Shot Image Classification</a></td><td>18</td><td>0</td><td>CV</td><td>few-shot 경량 인코더임</td></tr>
<tr><td>710</td><td><a href='https://arxiv.org/abs/2610.33209'>Model-agnostic predictability quantification of multivariable time series</a></td><td>18</td><td>0</td><td>LG</td><td>시계열 예측 가능성 정량화임</td></tr>
<tr><td>711</td><td><a href='https://arxiv.org/abs/2610.34123'>Enhancing Type 2 Diabetes Diagnosis with Evolutionary Algorithms and Machine Learning</a></td><td>18</td><td>0</td><td>LG</td><td>진화 알고리즘으로 당뇨 진단을 돕는 연구로 무관함</td></tr>
<tr><td>712</td><td><a href='https://arxiv.org/abs/2610.34258'>Recovering Business Rules as Cascade Lookups for Enterprise Field Prediction</a></td><td>18</td><td>0</td><td>LG</td><td>기업 주문 필드를 cascade lookup으로 예측해 무관함</td></tr>
<tr><td>713</td><td><a href='https://arxiv.org/abs/2610.34843'>When Respondents Are Scarce: LLM-Derived Semantic Priors for Bayesian Confirmatory Factor Analysis</a></td><td>18</td><td>0</td><td>LG</td><td>LLM prior를 쓴 Bayesian 요인분석으로 무관함</td></tr>
<tr><td>714</td><td><a href='https://arxiv.org/abs/2610.35084'>A JiT-Based Denoising Defense Method Against Adversarial Examples for Radio Signal Automatic Modulation Classification</a></td><td>18</td><td>0</td><td>LG</td><td>전파 신호 변조 분류의 JiT 기반 방어로 무관함</td></tr>
<tr><td>715</td><td><a href='https://arxiv.org/abs/2610.35167'>Biology-Guided Context-Aware Residual Propagation for Spatial Gene Expression Prediction from Histology</a></td><td>18</td><td>0</td><td>CV</td><td>병리 영상에서 공간 유전자 발현 예측으로 무관함</td></tr>
<tr><td>716</td><td><a href='https://arxiv.org/abs/2610.35304'>Inference Latency-Aware Tsetlin Machine Training</a></td><td>18</td><td>0</td><td>LG</td><td>Tsetlin machine 추론 지연 학습으로 무관함</td></tr>
<tr><td>717</td><td><a href='https://arxiv.org/abs/2610.35484'>Evaluating Bayesian deep learning for robust biomedical time-series classification under distribution shift: A sleep scoring case study</a></td><td>18</td><td>0</td><td>LG</td><td>생의학 시계열 Bayesian deep learning 평가로 무관함</td></tr>
<tr><td>718</td><td><a href='https://arxiv.org/abs/2610.35540'>Beyond Modeling Order: Dual-Path Spatiotemporal Representation Learning for Cross-Subject EEG Emotion Recognition</a></td><td>18</td><td>0</td><td>LG</td><td>EEG 감정 인식 dual-path 표현 학습으로 무관함</td></tr>
<tr><td>719</td><td><a href='https://arxiv.org/abs/2610.35560'>Multi-Fidelity Training Reshapes Uncertainty Decomposition in Atomistic Models</a></td><td>18</td><td>0</td><td>LG</td><td>원자 모델의 multi-fidelity UQ 분해로 무관함</td></tr>
<tr><td>720</td><td><a href='https://arxiv.org/abs/2610.35617'>Distilling neural networks into equations to predict planetary instability</a></td><td>18</td><td>0</td><td>LG</td><td>신경망을 수식으로 증류해 행성 불안정을 예측함</td></tr>
<tr><td>721</td><td><a href='https://arxiv.org/abs/2610.35710'>Detecting bus delays and service anomalies in Niterói with autoencoder latent feature representations</a></td><td>18</td><td>0</td><td>LG</td><td>버스 지연 autoencoder 이상 탐지로 무관함</td></tr>
<tr><td>722</td><td><a href='https://arxiv.org/abs/2610.35721'>Can JEV Support Clinical Trial Criteria Assessment?</a></td><td>18</td><td>0</td><td>NLP</td><td>임상시험 기준 평가용 JEV로 무관함</td></tr>
<tr><td>723</td><td><a href='https://arxiv.org/abs/2610.35963'>Condition-Enhanced Generative Adversarial Network for Aerodynamic Configuration Design of Commercial Aircraft</a></td><td>18</td><td>0</td><td>LG</td><td>항공기 공력 형상 설계용 GAN으로 무관함</td></tr>
<tr><td>724</td><td><a href='https://arxiv.org/abs/2610.35975'>A Graph-informed Kriging model for sample-efficient Bayesian optimization of wind farm layouts</a></td><td>18</td><td>0</td><td>LG</td><td>풍력 단지 배치 Bayesian 최적화로 무관함</td></tr>
<tr><td>725</td><td><a href='https://arxiv.org/abs/2610.33440'>Perturbation-Based Data Selection for Medical Question Answering</a></td><td>18</td><td>0</td><td>NLP</td><td>Gaussian 섭동 기반 prediction-change 신호로 의료 QA 학습 부분집합을 선택함. 데이터 선택 소규모 기법임</td></tr>
<tr><td>726</td><td><a href='https://arxiv.org/abs/2610.33749'>Refined Assessment for Translation Evaluation: Rethinking Machine Translation Evaluation in the Era of Human-Level Systems</a></td><td>18</td><td>0</td><td>NLP</td><td>MQM, ESA 한계를 짚고 번역 평가 방법을 재설계함. MT 평가 연구임</td></tr>
<tr><td>727</td><td><a href='https://arxiv.org/abs/2610.33813'>Task Format as a Factor in Adaptation: A Controlled Comparison of LoRA and Full Fine-Tuning for Prompt-Safety Classification</a></td><td>18</td><td>0</td><td>NLP</td><td>400M 모델에서 task format에 따라 LoRA가 full FT보다 2-3점 낮음을 통제 비교함. 분류 fine-tuning 비교 연구임</td></tr>
<tr><td>728</td><td><a href='https://arxiv.org/abs/2610.34490'>Efficient Proof Generation for Lean Statements with Multiple Candidate Answers</a></td><td>18</td><td>0</td><td>Math</td><td>여러 후보 답에 대한 Lean 증명을 한 번에 탐색해 중복 계산을 줄임. 형식 수학 연구임</td></tr>
<tr><td>729</td><td><a href='https://arxiv.org/abs/2610.34872'>Adaptive Retrieval, Selective Answers: Evaluating Conformal Factuality in Agentic RAG</a></td><td>18</td><td>0</td><td>RAG</td><td>agentic RAG에서 claim 수준 conformal factuality를 평가함. 사실성 보장 연구임</td></tr>
<tr><td>730</td><td><a href='https://arxiv.org/abs/2610.35432'>Probing the phon* representations of the Mimi codebooks</a></td><td>18</td><td>0</td><td>NLP</td><td>Mimi codec 첫 codebook이 phoneme을 어떻게 담는지 PNMI로 probing함. 음성 표현 분석이며 로보틱스 무관함.</td></tr>
<tr><td>731</td><td><a href='https://arxiv.org/abs/2610.35654'>Improving JEV Entailment Reranking with Span Readouts and Selective Adaptation</a></td><td>18</td><td>0</td><td>NLP</td><td>JEV entailment reranking에 mean-span readout과 선택적 LoRA를 적용함. 작은 설계 변경이고 로보틱스 무관함.</td></tr>
<tr><td>732</td><td><a href='https://arxiv.org/abs/2610.33355'>BenchBench-Cloning: Evaluating Molecular Cloning Design and Protocol Development</a></td><td>18</td><td>0</td><td>AI</td><td>분자 클로닝 실험 계획 LLM 벤치마크(65개 과제)임. 최고 점수 30.6%로 미포화이나 로보틱스 무관함.</td></tr>
<tr><td>733</td><td><a href='https://arxiv.org/abs/2610.33775'>The Hitchhiker&#x27;s Guide to System 1 Models: Fast Decision-Making Beyond LLMS</a></td><td>18</td><td>0</td><td>LG</td><td>System 1 decision model을 5개 계열로 분류하고 calibration 이론을 정리한 실무 가이드(190개 참고문헌)임. 새 방법 없고 로보틱스 무관함.</td></tr>
<tr><td>734</td><td><a href='https://arxiv.org/abs/2610.33801'>Are We Done with UMLS Injection into Language Models for Medical Question Answering?</a></td><td>18</td><td>0</td><td>NLP</td><td>의료 QA에서 UMLS 지식 주입이 왜 효과가 작은지 문헌 리뷰와 분리 실험으로 분석함. 로보틱스 무관함.</td></tr>
<tr><td>735</td><td><a href='https://arxiv.org/abs/2610.35011'>Critic&#x27;s Eye: Review-Grounded Graph Reasoning for Long-Form Motif Discovery</a></td><td>18</td><td>0</td><td>NLP</td><td>희곡 모티프 발견을 narrative graph 추론으로 푸는 Critic&#x27;s Eye임. 로봇과 무관함.</td></tr>
<tr><td>736</td><td><a href='https://arxiv.org/abs/2610.35069'>Beyond Single-Attribute Auditing: A Configurable Multi-Attribute Benchmark for Intersectional Fairness in LLMs</a></td><td>18</td><td>0</td><td>Fairness</td><td>LLM의 교차 속성 공정성을 479,066개 인스턴스로 감사하는 ComFair 벤치마크임. 로봇과 무관함.</td></tr>
<tr><td>737</td><td><a href='https://arxiv.org/abs/2610.35074'>A Diagnostic Protocol for GNNs in Electricity Load Forecasting: Separating Parameter Sharing from Neighborhood Access</a></td><td>18</td><td>0</td><td>Time Series</td><td>전력 부하 예측에서 GNN의 이득이 파라미터 공유인지 이웃 접근인지 가르는 진단 프로토콜임. 로봇과 무관함.</td></tr>
<tr><td>738</td><td><a href='https://arxiv.org/abs/2610.35288'>Proof-of-Agentness: Towards Verifying Agents on the Web</a></td><td>18</td><td>0</td><td>Web Agent</td><td>웹에서 agent와 단순 봇을 구분하는 Proof-of-Agentness를 제안함. 로봇과 무관함.</td></tr>
<tr><td>739</td><td><a href='https://arxiv.org/abs/2610.35293'>AgenticCity-Bench: Longitudinal Multimodal Observations of Urban Dynamics with Agentic Reasoning</a></td><td>18</td><td>0</td><td>Benchmark</td><td>16개 도시 18개 modality의 도시 동역학 벤치마크 AgenticCity-Bench임. 로봇과 무관함.</td></tr>
<tr><td>740</td><td><a href='https://arxiv.org/abs/2610.35400'>AdaTrendLike: Adaptive Hierarchical Detrending and Trend Likelihood Scoring for Time Series Anomaly Detection</a></td><td>18</td><td>0</td><td>Time Series</td><td>trend likelihood로 시계열 이상 탐지를 하는 AdaTrendLike임. 로봇과 무관함.</td></tr>
<tr><td>741</td><td><a href='https://arxiv.org/abs/2610.35464'>EvoBench: An Evolving, Diagnostic Benchmark Framework for Environmental Modeling</a></td><td>18</td><td>0</td><td>Benchmark</td><td>환경 모델링 실패 지점을 추적하는 EvoBench와 유량 예측 사례임. 로봇과 무관함.</td></tr>
<tr><td>742</td><td><a href='https://arxiv.org/abs/2610.35593'>SAP-ViT: A Self-Attributing Patch Vision Transformer for Medical Image Classification</a></td><td>18</td><td>0</td><td>Medical CV</td><td>CLS 대신 patch embedding 합산으로 설명 가능한 ViT를 만든 SAP-ViT임. 로봇과 무관함.</td></tr>
<tr><td>743</td><td><a href='https://arxiv.org/abs/2610.35246'>NOMAD-EEG: Native Omni-Montage Adaptive Diffusion</a></td><td>16</td><td>0</td><td>LG</td><td>EEG montage 가변 diffusion 생성으로 무관함</td></tr>
<tr><td>744</td><td><a href='https://arxiv.org/abs/2610.35378'>TransECG-SSL: Hybrid Self-Supervised Representation Learning for ECG Arrhythmia Classification</a></td><td>16</td><td>0</td><td>LG</td><td>ECG 부정맥 SSL 표현 학습으로 무관함</td></tr>
<tr><td>745</td><td><a href='https://arxiv.org/abs/2610.35645'>Proofs of strong forms of the Bovdi--Geche universality conjecture and a complex analogue</a></td><td>16</td><td>0</td><td>LG</td><td>단일 뉴런 신경망 보편성 정리 증명임</td></tr>
<tr><td>746</td><td><a href='https://arxiv.org/abs/2610.35972'>Multiple Leak Localization in Water Distribution Networks through Graph Neural Networks</a></td><td>16</td><td>0</td><td>LG</td><td>상수도 다중 누수 위치를 GNN으로 찾는 연구임</td></tr>
<tr><td>747</td><td><a href='https://arxiv.org/abs/2610.35423'>INVAR-Agri: Detecting Discrepancies in Multilingual Operator Manuals of Agricultural Implements with a Fine-Tuned LLM</a></td><td>16</td><td>0</td><td>NLP</td><td>농기계 매뉴얼 다국어 번역 오류를 1.7B LLM으로 탐지하는 proof of concept임. 소규모 응용이고 로보틱스 무관함.</td></tr>
<tr><td>748</td><td><a href='https://arxiv.org/abs/2610.36006'>MedJev: Evaluating Zero-Shot System-One Decision Making in Medicine</a></td><td>16</td><td>0</td><td>NLP</td><td>Jev형 System One 모델 MedJev를 의료 벤치마크 10개로 평가하고 2-parameter recalibration을 제안함. 의료 응용이고 로보틱스 무관함.</td></tr>
<tr><td>749</td><td><a href='https://arxiv.org/abs/2610.33233'>Distilling Expert Judgment at Scale</a></td><td>16</td><td>0</td><td>AI</td><td>전문가 판단을 자동 judge로 distill하는 방법론을 AI 뉴스 평가에 적용함. 로보틱스 무관함.</td></tr>
<tr><td>750</td><td><a href='https://arxiv.org/abs/2610.33240'>NewsBench: Expert-Grounded Evaluation of Epistemic Quality in AI News Reporting</a></td><td>16</td><td>0</td><td>AI</td><td>전문가 편집 기준에 근거한 AI 뉴스 품질 벤치마크 NewsBench(약 3,000 프롬프트)임. 로보틱스 무관함.</td></tr>
<tr><td>751</td><td><a href='https://arxiv.org/abs/2610.33410'>Benchmarking System One Models for Time-Series Decision Making: A Case Study of Jev</a></td><td>16</td><td>0</td><td>AI</td><td>Jev 1.13.0을 시계열 분류·주가 방향 예측에 평가한 사례 연구임. 상당수 과제에서 chance 수준이며 로보틱스 무관함.</td></tr>
<tr><td>752</td><td><a href='https://arxiv.org/abs/2610.33536'>FraudSociety: A Generative Agent-Based Society for the Financial-Fraud Economy</a></td><td>16</td><td>0</td><td>AI</td><td>금융사기 생태계를 LLM agent로 시뮬레이션하는 FraudSociety임. 사회 시뮬레이션이며 로보틱스 무관함.</td></tr>
<tr><td>753</td><td><a href='https://arxiv.org/abs/2610.34393'>On Distributed Sensing and Adversarial Localization of Narrowband Acoustic Sources for Offshore Data Center Monitoring</a></td><td>15</td><td>1</td><td>Acoustic Localization</td><td>aliased TDOA를 이동 수신기 anchor로 풀어 협대역 음원을 추적함. 로봇은 수신기 이동 수단일 뿐이고 학습과 무관함</td></tr>
<tr><td>754</td><td><a href='https://arxiv.org/abs/2610.33626'>Allocation Before the Clock: Graph, Set and Game Theory of Professional League of Legends Objective Setups</a></td><td>15</td><td>0</td><td>LG</td><td>리그 오브 레전드 분석임</td></tr>
<tr><td>755</td><td><a href='https://arxiv.org/abs/2610.33627'>ONOT/TONO-Print: A Paired Benchmark for Identity-Document Portrait Quality under Document Production Shift</a></td><td>15</td><td>0</td><td>CV</td><td>신분증 초상 품질 벤치마크임</td></tr>
<tr><td>756</td><td><a href='https://arxiv.org/abs/2610.33661'>Tracking Is Not Sensing: Artifact-Aware Thermal Video Respiration Estimation in Head-Free Marmosets</a></td><td>15</td><td>0</td><td>CV</td><td>마모셋 호흡 추정임</td></tr>
<tr><td>757</td><td><a href='https://arxiv.org/abs/2610.33965'>Accuracy Is Not Enough: An Efficiency- and Statistics-Aware Benchmark of ResNet50 and Vision Transformer for Explainable Multi-Class Gastrointestinal Diseases Classification</a></td><td>15</td><td>0</td><td>CV</td><td>위장관 분류 벤치마크임</td></tr>
<tr><td>758</td><td><a href='https://arxiv.org/abs/2610.34214'>StaX-Net: Stackelberg Interleaved Asymmetric Network for Cross-Modality Medical Image Translation</a></td><td>15</td><td>0</td><td>CV</td><td>의료 영상 변환임</td></tr>
<tr><td>759</td><td><a href='https://arxiv.org/abs/2610.34854'>Learning Dual-Camera Smooth Zoom via Decoupled Geometric-Photometric Data Synthesis</a></td><td>15</td><td>0</td><td>CV</td><td>스마트폰 듀얼 카메라 줌임</td></tr>
<tr><td>760</td><td><a href='https://arxiv.org/abs/2610.34884'>MedAdaptAgent: An Automatic Harness for Adapting Medical Imaging Models to New Sites</a></td><td>15</td><td>0</td><td>CV</td><td>의료 영상 사이트 적응 agent임</td></tr>
<tr><td>761</td><td><a href='https://arxiv.org/abs/2610.35005'>Shifted Window Temporal Transformer for YOLO-Guided Phase Recognition in Laparoscopic Cholecystectomy Surgery</a></td><td>15</td><td>0</td><td>Video</td><td>복강경 수술 단계 인식임</td></tr>
<tr><td>762</td><td><a href='https://arxiv.org/abs/2610.35065'>Kronecker-Structured Video Completion with Cross-Fitted Self-Supervised Residual Learning</a></td><td>15</td><td>0</td><td>CV</td><td>비디오 completion임</td></tr>
<tr><td>763</td><td><a href='https://arxiv.org/abs/2610.35414'>Unveil the Mask: Jointly-Optimized Diffusion Masked Pretraining for Appearance-Agnostic Operator Verification</a></td><td>15</td><td>0</td><td>CV</td><td>아바타 조작자 검증임</td></tr>
<tr><td>764</td><td><a href='https://arxiv.org/abs/2611.00102'>Demystifying Prompt Stealing Attacks against Synthetic Video</a></td><td>15</td><td>0</td><td>Video</td><td>합성 비디오 prompt stealing 공격임</td></tr>
<tr><td>765</td><td><a href='https://arxiv.org/abs/2610.33248'>Reinforcement Learning for Controller Parameters in the Auto-Bidding System at Pinterest</a></td><td>15</td><td>0</td><td>RL</td><td>광고 입찰 제어 RL임</td></tr>
<tr><td>766</td><td><a href='https://arxiv.org/abs/2610.33259'>RadonBench: A Benchmark of Classical and Learning-Guided Search Techniques for Problems in Combinatorial Geometry</a></td><td>15</td><td>0</td><td>LG</td><td>조합 기하 탐색 벤치마크임</td></tr>
<tr><td>767</td><td><a href='https://arxiv.org/abs/2610.33285'>Individual Fairness via Local Predictive Consistency</a></td><td>15</td><td>0</td><td>LG</td><td>개인 공정성 일관성임</td></tr>
<tr><td>768</td><td><a href='https://arxiv.org/abs/2610.33279'>Multi-Agent Retrieval-Augmented Causality Assessment (MARCA) of Individual Case Safety Reports in Pharmacovigilance</a></td><td>15</td><td>0</td><td>NLP</td><td>약물 부작용 인과 평가를 4-agent RAG로 자동화함. 의료 약물감시 응용이라 무관함</td></tr>
<tr><td>769</td><td><a href='https://arxiv.org/abs/2610.33357'>Preference Optimization Improves Definition Generation: Semantic Change in EU Institutional Sustainable Finance Disclosures</a></td><td>15</td><td>0</td><td>NLP</td><td>DPO로 정의 생성기의 과도한 의미 분할을 줄여 어휘 의미 변화 탐지에 씀. 특정 도메인 NLP임</td></tr>
<tr><td>770</td><td><a href='https://arxiv.org/abs/2610.33493'>Small Edits, Shifting Decisions: Benchmarking LLM Accuracy and Reliability on French Input Variants</a></td><td>15</td><td>0</td><td>NLP</td><td>프랑스어 철자 변형 4,200쌍으로 LLM 정확도와 신뢰도 변화를 측정함. 언어 특화 벤치마크임</td></tr>
<tr><td>771</td><td><a href='https://arxiv.org/abs/2610.33583'>When the Weakest Language Keeps Moving: ARMOR-DP for Multilingual BabyLM</a></td><td>15</td><td>0</td><td>NLP</td><td>가장 약한 언어를 검증 손실로 추적해 다국어 BabyLM 샘플링을 바꿈. 로봇 무관함</td></tr>
<tr><td>772</td><td><a href='https://arxiv.org/abs/2610.33765'>RoleHear: Pseudo-Labeling for Semi-Supervised Role-Attributed Streaming Speech Recognition</a></td><td>15</td><td>0</td><td>Speech</td><td>streaming ASR에 화자 역할을 의사 라벨로 귀속함. 음성 응용이고 무관함</td></tr>
<tr><td>773</td><td><a href='https://arxiv.org/abs/2610.34281'>Transformer to GPT-5: Advancements, Limitations, and Future Directions in Large Language Model Design</a></td><td>15</td><td>0</td><td>Survey</td><td>BERT에서 GPT-5까지 LLM 분류와 한계 서베이임. 신규 기여 없음</td></tr>
<tr><td>774</td><td><a href='https://arxiv.org/abs/2610.34791'>Text Is the Bottleneck: A Small-Scale Replication of LLM Game Playing in Riichi Mahjong</a></td><td>15</td><td>0</td><td>Games</td><td>text 병목 때문에 CNN 보드 인코더가 text LLM보다 낫다고 재현함. 마작 소규모 재현임</td></tr>
<tr><td>775</td><td><a href='https://arxiv.org/abs/2610.34991'>Diagnosing and Mitigating Long-Session Degradation in Full-Duplex Speech Models</a></td><td>15</td><td>0</td><td>Speech</td><td>full-duplex 음성 모델의 장기 세션 열화를 진단하고 완화함. 음성 대화 연구임</td></tr>
<tr><td>776</td><td><a href='https://arxiv.org/abs/2610.35269'>MechAlign: Evaluating Semantic Alignment at the Project Level in Mathematical Formalization</a></td><td>15</td><td>0</td><td>Math</td><td>Lean 형식화가 원 수학 주장과 의미 정렬되는지 프로젝트 수준으로 검토함</td></tr>
<tr><td>777</td><td><a href='https://arxiv.org/abs/2610.35512'>MATCHA: A Chinese Multi-Disorder Mental Health Dataset with Cross-Lingual Analyses on Social Media</a></td><td>15</td><td>0</td><td>NLP</td><td>중국어 Weibo 정신건강 다질환 데이터셋 MATCHA를 구축함. 데이터 자원이며 로보틱스 무관함.</td></tr>
<tr><td>778</td><td><a href='https://arxiv.org/abs/2610.34778'>Arya Forge: Auditing Validation and Release Approval for Financial Instruction Data</a></td><td>15</td><td>0</td><td>Data Pipeline</td><td>금융 instruction 데이터의 검증과 릴리스 승인을 감사하는 Arya Forge 사례 연구임. 로봇과 무관함.</td></tr>
<tr><td>779</td><td><a href='https://arxiv.org/abs/2610.34829'>Logic Hijacking of RAG: Single-Document Poisoning via Local Optimization</a></td><td>15</td><td>0</td><td>Security</td><td>논리 하이재킹으로 RAG 단일 문서를 오염시키는 MONOLOGUE 공격임. 로봇과 무관함.</td></tr>
<tr><td>780</td><td><a href='https://arxiv.org/abs/2610.34871'>DocTalk: Enhancing Medical Knowledge Retrieval via Fine-tuned Large Language Models with Chain-of-Thought Reasoning for Robust Clinical Decision Support</a></td><td>15</td><td>0</td><td>Medical NLP</td><td>퇴원 요약 기반 의료 QA용 LoRA 튜닝 시스템 DocTalk임. dataset fine-tuning 위주이고 로봇과 무관함.</td></tr>
<tr><td>781</td><td><a href='https://arxiv.org/abs/2610.35031'>PatentAgentBench: Benchmarking LLM Agents with Professional Patent Task Suites</a></td><td>15</td><td>0</td><td>Benchmark</td><td>특허 업무 8종을 다루는 PatentAgentBench임. 로봇과 무관함.</td></tr>
<tr><td>782</td><td><a href='https://arxiv.org/abs/2610.35298'>LLM-Enhanced Heterogeneous Graph Learning with Business Semantics for Financial Fraud Detection</a></td><td>15</td><td>0</td><td>Graph Learning</td><td>금융 사기 탐지용 LLM 보강 이종 그래프 모델 SemHGT임. 로봇과 무관함.</td></tr>
<tr><td>783</td><td><a href='https://arxiv.org/abs/2610.35704'>Explainable Multimodal AI Approach to Reduce Unnecessary Breast Biopsies</a></td><td>15</td><td>0</td><td>Medical</td><td>유방 생검 예측을 ViT와 DeBERTa late fusion으로 함. AUC 0.72로 낮고 로봇과 무관함.</td></tr>
<tr><td>784</td><td><a href='https://arxiv.org/abs/2610.35960'>From Slices to Volumes: Comparing 2D, 2.5D, and 3D Residual Networks for Pulmonary Nodule Malignancy-Risk Classification</a></td><td>14</td><td>0</td><td>CV</td><td>폐결절 악성도에 2D/2.5D/3D ResNet을 비교한 의료 영상 연구임</td></tr>
<tr><td>785</td><td><a href='https://arxiv.org/abs/2610.35961'>Knowledge distillation across teacher architectures for compact diabetic retinopathy grading</a></td><td>14</td><td>0</td><td>CV</td><td>망막 질환 등급용 지식증류로 무관함</td></tr>
<tr><td>786</td><td><a href='https://arxiv.org/abs/2610.36020'>Exploratory creative pre-ranking: Hierarchical empirical-Bayes Thompson sampling for real-time creative optimization</a></td><td>14</td><td>0</td><td>LG</td><td>광고 creative 선택의 Thompson sampling으로 무관함</td></tr>
<tr><td>787</td><td><a href='https://arxiv.org/abs/2610.35358'>Agreement Between Reconstructed and Native GDELT GKG Records: A Field-Level Baseline</a></td><td>14</td><td>0</td><td>NLP</td><td>GDELT GKG 레코드를 재구성한 오픈소스 도구와 원본 간 필드별 일치도 측정함. 데이터 자원 성격이고 로보틱스 무관함.</td></tr>
<tr><td>788</td><td><a href='https://arxiv.org/abs/2610.35609'>Making Reasoning Visible: Configuration-Aware Diagnostic Modeling for Adaptive Scaffolding in Structured Reasoning Tasks</a></td><td>14</td><td>0</td><td>NLP</td><td>문법 학습 게임의 행동 시퀀스로 학생 추론 상태를 진단하는 프레임워크임. 교육 응용이고 로보틱스 무관함.</td></tr>
<tr><td>789</td><td><a href='https://arxiv.org/abs/2610.33405'>Data Optimization for LLMs: A Survey</a></td><td>14</td><td>0</td><td>AI</td><td>LLM 데이터 선택·증강·reweighting을 정리한 서베이임. 로보틱스 무관함.</td></tr>
<tr><td>790</td><td><a href='https://arxiv.org/abs/2610.34009'>Fed-Universe: A Semantic-Geometric-Topological-Human (S-G-T-H) Stack for Negotiated Alignment in Federated Systems</a></td><td>14</td><td>0</td><td>LG</td><td>federated learning에 semantic-geometric-topological-human 스택을 제안한 5쪽짜리 개념 논문임. 합성 임상 네트워크 시뮬레이션만 검증함.</td></tr>
<tr><td>791</td><td><a href='https://arxiv.org/abs/2610.34708'>Resource-Performance Trade-offs in Intra-Aisle Robotic Picking: A Discrete-Event Simulation Comparison of Shuttle Configurations With and Without an Onboard Tote Lift</a></td><td>12</td><td>1</td><td>Logistics</td><td>창고 shuttle 구성의 이산 사건 시뮬레이션 비교임. lift 구성이 사이클 시간 11.27% 길다는 결과이고 로봇 학습과 무관함</td></tr>
<tr><td>792</td><td><a href='https://arxiv.org/abs/2610.33737'>A SegFormer-based model for spatial Daylight Factor prediction with comprehensive obstruction encoding and regulatory validation</a></td><td>12</td><td>0</td><td>CV</td><td>일조율 예측 응용임</td></tr>
<tr><td>793</td><td><a href='https://arxiv.org/abs/2610.34352'>A Computationally Efficient Non-Interpolation Virtual Trellis Approach for Mammogram Gradient-based Patterns Analysis</a></td><td>12</td><td>0</td><td>CV</td><td>유방촬영 패턴 분석임</td></tr>
<tr><td>794</td><td><a href='https://arxiv.org/abs/2610.34599'>An Agentic AI Workflow for Liver Lesion Segmentation and Structured Radiology Reporting</a></td><td>12</td><td>0</td><td>Multimodal</td><td>간 병변 agentic 워크플로임</td></tr>
<tr><td>795</td><td><a href='https://arxiv.org/abs/2610.34600'>FlexiMIND: Combined Pretrained Vision Features and Local Structure for Training-Free Deformable Medical Image Registration</a></td><td>12</td><td>0</td><td>CV</td><td>의료 영상 정합임</td></tr>
<tr><td>796</td><td><a href='https://arxiv.org/abs/2610.35240'>Reading Beyond OCR Noise: Robust Cross-Lingual RAG for Legislative Archives</a></td><td>12</td><td>0</td><td>NLP</td><td>입법 아카이브 RAG임</td></tr>
<tr><td>797</td><td><a href='https://arxiv.org/abs/2610.35244'>Beyond Vision-Language Models: Visual-Semantic Affect Graphs for Emotion Recognition in Artworks</a></td><td>12</td><td>0</td><td>CV</td><td>예술 감정 인식임</td></tr>
<tr><td>798</td><td><a href='https://arxiv.org/abs/2610.33899'>When Personas Become Harmful: Guiding LLMs with Global Citizenship Values Alignment</a></td><td>12</td><td>0</td><td>NLP</td><td>persona 조건 요청의 유해성을 글로벌 시민 가치로 정렬함. LLM 안전 연구임</td></tr>
<tr><td>799</td><td><a href='https://arxiv.org/abs/2610.33946'>Schema-Free Text-to-SQL: Learning Enterprise Database Structure from Query Logs</a></td><td>12</td><td>0</td><td>NLP</td><td>문서 없이 쿼리 로그에서 DB 구조를 학습하는 text-to-SQL임. 기업 DB 응용임</td></tr>
<tr><td>800</td><td><a href='https://arxiv.org/abs/2610.34013'>The Patient Is Always Right? Evaluating Sycophancy in Medical Diagnosis with Graded Patient Beliefs</a></td><td>12</td><td>0</td><td>NLP</td><td>환자 믿음에 맞춰 진단을 바꾸는 9개 모델의 sycophancy를 평가함. 의료 LLM 안전 연구임</td></tr>
<tr><td>801</td><td><a href='https://arxiv.org/abs/2610.34212'>Higher Reasoning Effort Improves Reference Verifiability and Changes Reasoning Summaries in GPT-5.5</a></td><td>12</td><td>0</td><td>NLP</td><td>GPT-5.5의 reasoning effort가 참고문헌 검증 가능성에 미치는 영향을 봄. 과학 글쓰기 응용임</td></tr>
<tr><td>802</td><td><a href='https://arxiv.org/abs/2610.34278'>A Russian, a Brazilian, and a German Walk into a Bar, Ask the Same Question-- And Get Three Different Answers: Profiling LLM Perspective Diversity on Contested Topics</a></td><td>12</td><td>0</td><td>NLP</td><td>18개 언어 PerspectivesQA로 LLM의 논쟁 주제 관점 다양성을 측정함. 사회 언어 연구임</td></tr>
<tr><td>803</td><td><a href='https://arxiv.org/abs/2610.34589'>HARP-LoRA: Hierarchy-Conditioned Rank Projection for Low-Rank Adaptation in Scientific Table Understanding</a></td><td>12</td><td>0</td><td>NLP</td><td>계층 정보를 조건으로 한 LoRA로 약동학 표를 추출함. 과학 표 이해 응용임</td></tr>
<tr><td>804</td><td><a href='https://arxiv.org/abs/2610.34591'>Does the Outfit Change the Price? Context Halo in Vision-Language Model Valuation of an Identical Low-Cost Necklace</a></td><td>12</td><td>0</td><td>VLM</td><td>같은 목걸이를 착용 맥락에 따라 6개 모델이 1.9-3.3배 다르게 가격 매김. 맥락 후광 편향 관찰임</td></tr>
<tr><td>805</td><td><a href='https://arxiv.org/abs/2610.35042'>SimPOTrans: Self-Adaptation for Offline-to-Simultaneous Speech Translation via Reinforcement Learning</a></td><td>12</td><td>0</td><td>Speech</td><td>동시 음성 번역을 RL로 자기 적응함. 번역 지연 최적화임</td></tr>
<tr><td>806</td><td><a href='https://arxiv.org/abs/2610.35111'>Rethinking Evaluation for Principled Generalization Using a Kripkean Challenge to Meaning as Use</a></td><td>12</td><td>0</td><td>NLP</td><td>의미 사용론의 규칙 따르기 문제로 OOD 평가를 재해석하는 철학적 논의임</td></tr>
<tr><td>807</td><td><a href='https://arxiv.org/abs/2610.33860'>Numina Fuse: Interactive Autoformalization in Lean 4</a></td><td>12</td><td>0</td><td>AI</td><td>Lean 4 autoformalization용 agent 애플리케이션 Numina Fuse임. 시스템 설명이며 로보틱스 무관함.</td></tr>
<tr><td>808</td><td><a href='https://arxiv.org/abs/2610.35208'>Same Story, Different Lens: A Multi-Agent System for Cross-Outlet News Framing Analysis</a></td><td>12</td><td>0</td><td>NLP</td><td>17개 언론사 뉴스 프레이밍을 비교하는 multi-agent 프로토타입임. 로봇과 무관함.</td></tr>
<tr><td>809</td><td><a href='https://arxiv.org/abs/2610.35267'>Before Blaming the LLM, Diagnose the Workflow: A Role-Level Difficulty Profile for Translating Natural Language into Ontology-Grounded Statements</a></td><td>12</td><td>0</td><td>NLP</td><td>NL-to-DSL 온톨로지 번역의 난이도를 역할별로 진단하는 정성 프로파일임. 로봇과 무관함.</td></tr>
<tr><td>810</td><td><a href='https://arxiv.org/abs/2610.35453'>Beyond Federated Learning: Decentralized Agentic Systems for Self-Evolving Clinical Intelligence</a></td><td>12</td><td>0</td><td>Medical</td><td>병원 간 추론 경험을 공유하는 Decentralized Agentic Systems perspective임. 로봇과 무관함.</td></tr>
<tr><td>811</td><td><a href='https://arxiv.org/abs/2610.35761'>Beyond Physical Illness: Can Clinical Narratives Reveal Emerging Mental Health Risks in Chronically Ill Patients?</a></td><td>12</td><td>0</td><td>Medical</td><td>MIMIC-III 임상 서술로 정신건강 위험을 예측함. 로봇과 무관함.</td></tr>
<tr><td>812</td><td><a href='https://arxiv.org/abs/2610.35847'>Patient-specific rubric-based evaluation of large language models across longitudinal cancer care</a></td><td>12</td><td>0</td><td>Medical</td><td>비인두암 진료 단계별 LLM 평가 벤치마크 NPC-RubricBench임. 로봇과 무관함.</td></tr>
<tr><td>813</td><td><a href='https://arxiv.org/abs/2610.35984'>Enhancing Deep Learning Model Performance through Data Generation Strategies: Classification of Olive Tree Diseases</a></td><td>12</td><td>0</td><td>CV</td><td>올리브 병해 분류에 DCGAN·MixUp 등 데이터 증강을 비교함. 로봇과 무관한 incremental 연구임.</td></tr>
<tr><td>814</td><td><a href='https://arxiv.org/abs/2610.34645'>Regional prediction of hematoma expansion from non-contrast computed tomography in spontaneous intracerebral hemorrhage patients</a></td><td>10</td><td>0</td><td>CV</td><td>혈종 확장 예측임</td></tr>
<tr><td>815</td><td><a href='https://arxiv.org/abs/2610.34825'>Interpretable Brain Age Prediction Using White Matter Fiber Orientation Distributions with Rotation-Equivariant Deep Learning</a></td><td>10</td><td>0</td><td>CV</td><td>뇌 나이 예측임</td></tr>
<tr><td>816</td><td><a href='https://arxiv.org/abs/2610.34917'>DiffAuction: An Auction-Driven Framework for Generative Image Advertising</a></td><td>10</td><td>0</td><td>Generative</td><td>광고 생성 경매임</td></tr>
<tr><td>817</td><td><a href='https://arxiv.org/abs/2610.35038'>Revealing Imaging Characteristics of Thermal Wakes from Underwater Vehicles Without Cooling-Water Discharge</a></td><td>10</td><td>0</td><td>CV</td><td>수중 비행체 열 후류 영상임</td></tr>
<tr><td>818</td><td><a href='https://arxiv.org/abs/2610.35076'>Blendshape Generation for Models with Disconnected Parts: Adding ARKit/MediaPipe Blendshapes to Anime-Style Character Models</a></td><td>10</td><td>0</td><td>Graphics</td><td>애니메이션 모델 blendshape 생성임</td></tr>
<tr><td>819</td><td><a href='https://arxiv.org/abs/2610.35085'>Reading the Registers of Honorius III without Manual Line Transcription: Forced-Aligned HTR, End to End, Modular or Hybrid</a></td><td>10</td><td>0</td><td>CV</td><td>중세 필사본 HTR임</td></tr>
<tr><td>820</td><td><a href='https://arxiv.org/abs/2610.35132'>Domain-Adapted Latent Diffusion Models for CT-to-PET Image Translation</a></td><td>10</td><td>0</td><td>CV</td><td>CT-PET 변환임</td></tr>
<tr><td>821</td><td><a href='https://arxiv.org/abs/2610.35220'>O2D-MedNet: An Optimization-Aware Dual-Domain Framework for Robust Medical Image Segmentation</a></td><td>10</td><td>0</td><td>CV</td><td>의료 분할임</td></tr>
<tr><td>822</td><td><a href='https://arxiv.org/abs/2610.35682'>Printed and Scanned: Exposing the Fragility of Single-Image Morphing Attack Detectors under Print-Scan Degradation</a></td><td>10</td><td>0</td><td>CV</td><td>morphing 공격 탐지임</td></tr>
<tr><td>823</td><td><a href='https://arxiv.org/abs/2611.09954'>DiffusedSplitFed: Latent Diffusion-based Obfuscation for Reconstruction-Resilient Split Federated Medical Image Segmentation</a></td><td>10</td><td>0</td><td>CV</td><td>의료 분할 split federated 난독화임</td></tr>
<tr><td>824</td><td><a href='https://arxiv.org/abs/2611.09956'>MAPA: Mode-Aware Prototype Allocation for Latent Dataset Distillation in 3D Medical Classification</a></td><td>10</td><td>0</td><td>CV</td><td>3D 의료 dataset distillation임</td></tr>
<tr><td>825</td><td><a href='https://arxiv.org/abs/2610.33464'>Propasafe-Hybrid: A Text-Based Hybrid Propaganda Detection Tool</a></td><td>10</td><td>0</td><td>NLP</td><td>문장 단위 선전 기법 분류와 설명 도구임. 응용 시스템이고 무관함</td></tr>
<tr><td>826</td><td><a href='https://arxiv.org/abs/2610.33488'>Incremental Predictive Value of LLM Tutoring Interactions for Student Performance</a></td><td>10</td><td>0</td><td>NLP</td><td>LLM 튜터 상호작용 feature로 학생 점수 예측을 평가함. 교육 데이터 분석임</td></tr>
<tr><td>827</td><td><a href='https://arxiv.org/abs/2610.33694'>Embedding-Based Educational Taxonomies</a></td><td>10</td><td>0</td><td>NLP</td><td>임베딩으로 교육 taxonomy를 만드는 연구임. 교육 응용임</td></tr>
<tr><td>828</td><td><a href='https://arxiv.org/abs/2610.33697'>Gender Associations in LLM-Mediated ADHD Self-Diagnosis</a></td><td>10</td><td>0</td><td>NLP</td><td>GPT-4o의 ADHD 자가진단 성별 연관을 CAT로 평가함. 사회 편향 연구임</td></tr>
<tr><td>829</td><td><a href='https://arxiv.org/abs/2610.33839'>EdgeDeID: A 0.6B Clinical De-identifier Trained Without Real Patient Data</a></td><td>10</td><td>0</td><td>NLP</td><td>합성 노트만으로 0.6B 임상 비식별화 모델을 학습함. 의료 응용이고 로봇 무관함</td></tr>
<tr><td>830</td><td><a href='https://arxiv.org/abs/2610.34012'>Reversible Pseudonymisation of Documents Sent to External LLMs: an Open Bilingual Benchmark and an Engine</a></td><td>10</td><td>0</td><td>NLP</td><td>가명처리 도구 5종 벤치마크와 엔진임. 개인정보 응용임</td></tr>
<tr><td>831</td><td><a href='https://arxiv.org/abs/2610.34080'>The LALA Benchmark: Evaluating Literary and Linguistic Analysis in LLMs</a></td><td>10</td><td>0</td><td>NLP</td><td>문학·언어학 전문가 질문 236개 벤치마크임. 인문 평가임</td></tr>
<tr><td>832</td><td><a href='https://arxiv.org/abs/2610.34215'>Synthetic linguistic data</a></td><td>10</td><td>0</td><td>NLP</td><td>합성 언어 데이터를 정원 비유로 분류한 용어 항목임</td></tr>
<tr><td>833</td><td><a href='https://arxiv.org/abs/2610.34343'>Xing USP: A Cross-Family Semantic Contract for Information Extraction and Intent-Slot Parsing</a></td><td>10</td><td>0</td><td>NLP</td><td>NER, 관계, 이벤트 추출을 공통 계약으로 묶는 정보 추출 틀임</td></tr>
<tr><td>834</td><td><a href='https://arxiv.org/abs/2610.34746'>DecisionTraceBench: Tracking Decision-Critical Information in Multi-Party Spoken Conversations</a></td><td>10</td><td>0</td><td>NLP</td><td>다자 대화에서 결정 정보 변화를 추적하는 음성 벤치마크임</td></tr>
<tr><td>835</td><td><a href='https://arxiv.org/abs/2610.34860'>Semantic Atoms for Scalable Text Analysis in Data Analytics in the Era of LLM-Based Agents</a></td><td>10</td><td>0</td><td>NLP</td><td>텍스트 열 분석을 위한 semantic atom을 제안함. 데이터 분석 응용임</td></tr>
<tr><td>836</td><td><a href='https://arxiv.org/abs/2610.34889'>FATE-5: Faithful Alignment of Trait Expression for Continuous Big Five Personality Control</a></td><td>10</td><td>0</td><td>NLP</td><td>soft prompt와 naturalness 정렬 2단계로 Big Five 성격을 제어함. 대화 개인화임</td></tr>
<tr><td>837</td><td><a href='https://arxiv.org/abs/2610.35029'>Synthetic Child-Adult Interactions Are Not Developmentally Plausible</a></td><td>10</td><td>0</td><td>NLP</td><td>합성 아동-성인 대화가 자연 발화의 단편성을 과소 반영함을 보임. 언어 습득 연구임</td></tr>
<tr><td>838</td><td><a href='https://arxiv.org/abs/2610.35102'>Useful Diversity or Hallucinated Variety? Persona-Conditioned Synthetic Query Generation for E-Commerce Search</a></td><td>10</td><td>0</td><td>NLP</td><td>persona 조건 합성 쿼리가 parser F1을 높임을 보임. 전자상거래 검색 응용임</td></tr>
<tr><td>839</td><td><a href='https://arxiv.org/abs/2610.35254'>Style over Substance? Linguistic Bias in LLM-based Peer Review</a></td><td>10</td><td>0</td><td>NLP</td><td>문체가 LLM 논문 리뷰 평가에 미치는 편향을 통제 실험함</td></tr>
<tr><td>840</td><td><a href='https://arxiv.org/abs/2610.35635'>Offline Language-Based Support System for Tactical Decision-Making in Air Combat Operations</a></td><td>10</td><td>0</td><td>NLP</td><td>공중전 교범 RAG 기반 오프라인 질의응답 도구 MATE를 조종사 3명이 평가함. 소규모 응용이고 로보틱스 무관함.</td></tr>
<tr><td>841</td><td><a href='https://arxiv.org/abs/2610.35685'>Adapting LLM-SC to Living Sacred Heritage: Domain-Specific Extraction, Semantic Networks and Human Evaluation on Pashupatinath Temple Reviews</a></td><td>10</td><td>0</td><td>NLP</td><td>네팔 사원 리뷰에 LLM-SC 프레임워크를 적용해 개체·관계를 추출함. entity F1 28.4%의 도메인 적용이며 로보틱스 무관함.</td></tr>
<tr><td>842</td><td><a href='https://arxiv.org/abs/2610.33205'>Scaling Qualitative Analysis with Large Language Models: Development and Validation of the Smart Coder Framework for Human-LLM Collaborative Coding</a></td><td>10</td><td>0</td><td>AI</td><td>교사 인터뷰 질적 코딩에 LLM을 쓰는 Smart Coder Framework임. 교육 연구 응용이고 로보틱스 무관함.</td></tr>
<tr><td>843</td><td><a href='https://arxiv.org/abs/2610.34481'>From Outranking Flow Scores to Linear Programs: Group Decision Making in PROMETHEE II</a></td><td>10</td><td>0</td><td>AI</td><td>PROMETHEE II 순위의 weight·preference 역분석과 합의 분석을 선형계획으로 정식화함. 의사결정론이며 로보틱스 무관함.</td></tr>
<tr><td>844</td><td><a href='https://arxiv.org/abs/2610.35143'>Sexual dimorphism and sex-specific features of pediatric hand bone shapes via statistical shape modeling</a></td><td>8</td><td>0</td><td>CV</td><td>손뼈 형태 통계 모델임</td></tr>
<tr><td>845</td><td><a href='https://arxiv.org/abs/2610.35271'>Low-rank MERA Decomposition of 3D OCT Image Volume for Compression, Denoising, Feature Extraction and Diagnosis of Retinal Diseases</a></td><td>8</td><td>0</td><td>CV</td><td>OCT 텐서 분해임</td></tr>
<tr><td>846</td><td><a href='https://arxiv.org/abs/2610.35339'>Targeted Deep Regression - Initial Applications in Whole-Body Water-Fat MRI in UK Biobank</a></td><td>8</td><td>0</td><td>CV</td><td>MRI 회귀 응용임</td></tr>
<tr><td>847</td><td><a href='https://arxiv.org/abs/2610.35396'>Toward Clinical Translation of Deep Learning-Based Intracranial Super-Resolution 4D Flow MRI Using Multi-Cohort Transfer Learning</a></td><td>8</td><td>0</td><td>CV</td><td>4D flow MRI 초해상임</td></tr>
<tr><td>848</td><td><a href='https://arxiv.org/abs/2610.35580'>Hyperspectral Unmixing using a Structured Linear Mixing Model with Additive Spectral Variability</a></td><td>8</td><td>0</td><td>CV</td><td>하이퍼스펙트럴 unmixing임</td></tr>
<tr><td>849</td><td><a href='https://arxiv.org/abs/2611.09955'>RadAI: Gaze-Intention Fusion Pipeline for Attention-Guided Educational Videos in Chest X-Ray Interpretation</a></td><td>8</td><td>0</td><td>CV</td><td>흉부 X-ray 교육용 시선 융합임</td></tr>
<tr><td>850</td><td><a href='https://arxiv.org/abs/2611.09958'>HippoMamba: A Mamba-augmented network for hippocampal segmentation and serial volumetry in Alzheimers disease</a></td><td>8</td><td>0</td><td>CV</td><td>해마 분할임</td></tr>
<tr><td>851</td><td><a href='https://arxiv.org/abs/2610.33168'>How Much Fresh Data Should CTR Recalibration Use? A Temporal Evaluation of Post-hoc Calibration</a></td><td>8</td><td>0</td><td>LG</td><td>CTR 보정 평가임</td></tr>
<tr><td>852</td><td><a href='https://arxiv.org/abs/2610.33307'>Tree Depth and Sample-Quality-Associated Features: Two Hidden Factors in Boruta Selection for RNA-Seq Data Classification</a></td><td>8</td><td>0</td><td>LG</td><td>RNA-seq 특징 선택임</td></tr>
<tr><td>853</td><td><a href='https://arxiv.org/abs/2610.33586'>Words Are the Voice of the Mind: Depression Severity Estimation from Social Traces via Mental-Guided Evidence Reasoning</a></td><td>8</td><td>0</td><td>NLP</td><td>소셜 미디어 글로 우울증 심각도를 추정함. 의료 응용으로 무관함</td></tr>
<tr><td>854</td><td><a href='https://arxiv.org/abs/2610.33931'>HerHealthGPT: An Evidence-Grounded Conversational AI System for Women&#x27;s Reproductive Health</a></td><td>8</td><td>0</td><td>NLP</td><td>RAG와 명확화 질문을 결합한 여성 건강 챗봇임. 응용 시스템임</td></tr>
<tr><td>855</td><td><a href='https://arxiv.org/abs/2610.34572'>RefinedGAW: A Refined German Academic Web Dataset</a></td><td>8</td><td>0</td><td>Dataset</td><td>독일어 학술 웹 3,140억 토큰 코퍼스임. 데이터 자원이고 무관함</td></tr>
<tr><td>856</td><td><a href='https://arxiv.org/abs/2610.34585'>Large Language Models: A Plain-Language Overview for Engineers</a></td><td>8</td><td>0</td><td>Overview</td><td>엔지니어용 LLM 개요 글임. 신규 기여 없음</td></tr>
<tr><td>857</td><td><a href='https://arxiv.org/abs/2610.34626'>Entity Matching using Decision Models</a></td><td>8</td><td>0</td><td>NLP</td><td>LLM decision model로 entity matching을 함. 데이터 통합 응용임</td></tr>
<tr><td>858</td><td><a href='https://arxiv.org/abs/2610.34887'>NumTrace: Auditing the Number Provenance of Financial Analyst Agents</a></td><td>8</td><td>0</td><td>NLP</td><td>금융 agent의 숫자 출처를 SEC 문서 540문항으로 감사하는 벤치마크임</td></tr>
<tr><td>859</td><td><a href='https://arxiv.org/abs/2610.35008'>When the Persona Contradicts the Line: Diagnosing Plan-to-Synthesis Failures in Chain-of-Thought TTS</a></td><td>8</td><td>0</td><td>Speech</td><td>persona와 대사 감정이 충돌할 때 CoT TTS 계획이 어디서 어긋나는지 진단함</td></tr>
<tr><td>860</td><td><a href='https://arxiv.org/abs/2610.35054'>From Questions to Queries to Insights: A Schema-Grounded Agentic Workflow for Natural-Language Crash Data Analysis</a></td><td>8</td><td>0</td><td>NLP</td><td>충돌 DB를 자연어로 질의하는 로컬 agent workflow임. 교통 데이터 응용임</td></tr>
<tr><td>861</td><td><a href='https://arxiv.org/abs/2610.35179'>High Scores, Hidden Failures: Evaluating Codebook-Based LLM Content Analysis</a></td><td>8</td><td>0</td><td>NLP</td><td>LLM 코드북 분석 파이프라인의 안정성과 강건성 실패 모드를 분석함</td></tr>
<tr><td>862</td><td><a href='https://arxiv.org/abs/2610.35261'>The Lay of the Land in Idiom-Translation Quality Estimation</a></td><td>8</td><td>0</td><td>NLP</td><td>9개 언어 관용구 번역 품질 추정 데이터셋임</td></tr>
<tr><td>863</td><td><a href='https://arxiv.org/abs/2610.33605'>Data Governance for Generative and Agentic AI : Technology, Law, Economics, and Security</a></td><td>8</td><td>0</td><td>AI</td><td>생성·agentic AI 데이터 거버넌스를 법·경제 관점에서 다룬 책 형식 문서임. 로보틱스 무관함.</td></tr>
<tr><td>864</td><td><a href='https://arxiv.org/abs/2610.35294'>Application of Artificial Intelligence in the Management of Climate Change-Related Health Issues in Africa</a></td><td>8</td><td>0</td><td>Policy</td><td>아프리카 기후 관련 건강 문제에 대한 AI 문헌 계량 분석임. 로봇과 무관함.</td></tr>
<tr><td>865</td><td><a href='https://arxiv.org/abs/2610.35802'>Game theory of academic effort and hiring in the age of AI</a></td><td>8</td><td>0</td><td>Game Theory</td><td>AI 시대 학계 노력과 채용을 게임이론으로 모델링함. 로봇과 무관함.</td></tr>
<tr><td>866</td><td><a href='https://arxiv.org/abs/2610.34499'>Can Statistics Tell Whether an Undeciphered Text Is Language? Calibrated Tests on the Voynich Manuscript</a></td><td>5</td><td>0</td><td>NLP</td><td>Voynich 필사본이 언어인지 보정된 통계 검정으로 따짐. 로봇과 무관함</td></tr>
<tr><td>867</td><td><a href='https://arxiv.org/abs/2610.34987'>AskGLP1: A Knowledge Graph LLM Agent for Exploring GLP-1 Experience from Online Patient Narratives</a></td><td>5</td><td>0</td><td>NLP</td><td>환자 서술에서 GLP-1 경험 지식 그래프를 만드는 응용임</td></tr>
<tr><td>868</td><td><a href='https://arxiv.org/abs/2610.35094'>RAGing Against Misogyny: Improving Implicit Misogyny Explanations</a></td><td>5</td><td>0</td><td>NLP</td><td>백과, 속어, 페미니즘 지식 RAG로 암묵적 여성혐오를 설명함</td></tr>
<tr><td>869</td><td><a href='https://arxiv.org/abs/2610.35114'>Quality over Quantity: Rethinking Data and Model Assumptions for Bengali Coreference Resolution</a></td><td>5</td><td>0</td><td>NLP</td><td>벵골어 coreference에서 다국어 모델 일반화 가정을 검증함</td></tr>
<tr><td>870</td><td><a href='https://arxiv.org/abs/2610.35168'>Do Language Models Understand Igbo Culture? Beyond Multiple Choice</a></td><td>5</td><td>0</td><td>NLP</td><td>이그보 토착 문화 출처로 CAB-Igbo 벤치마크를 만듦</td></tr>
<tr><td>871</td><td><a href='https://arxiv.org/abs/2610.35191'>Lost in Translation: Investigating Systematic Discrepancies between Parallel English and Chinese Names of American Chinese Restaurants</a></td><td>3</td><td>0</td><td>NLP</td><td>미국 중식당 영중 이름 불일치를 분석함. 로봇 무관함</td></tr>
</tbody></table>

</details>
