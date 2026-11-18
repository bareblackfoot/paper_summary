# 오늘의 arXiv Top 15: 2026-11-17 (화)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**

**신규 논문 수: 전체 942편 → 중복 제거 후 942편 (이번 평가 대상 942편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 285 |
| cs.LG | 252 |
| cs.RO | 110 |
| cs.CL | 160 |
| cs.AI | 135 |

---

## Top 15

### 1. ResWAM: Learning What Changes, Not What Stays, for World-Action Models (74점)

[arXiv](https://arxiv.org/abs/2611.19559) · [PDF](https://arxiv.org/pdf/2611.19559) · [alphaXiv](https://www.alphaxiv.org/abs/2611.19559) (요약 있음)

- **저자**: Chongyu Fan, Gaowen Liu, Ramana Rao Kompella, Jason Corso, Sijia Liu
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> world-action model의 보조 예측 대상을 미래 장면 전체에서 현재와 미래 DINOv3 feature의 차이(residual)로 바꿈. 같은 계산량에서 미래 feature 전체를 예측할 때보다 RoboTwin 2.0 평균 성공률이 90.9%에서 93.8%로 오름.

**무슨 문제인가**

world-action model(WAM)은 VLA에 미래 장면 예측을 붙여 policy가 행동의 결과를 미리 고려하게 하는 모델임. 기존 WAM은 미래 프레임이나 미래 feature 전체를 맞히도록 학습함. 그런데 action chunk 하나 동안 장면은 거의 변하지 않음. LIBERO에서 현재와 미래 DINOv3 feature의 평균 cosine similarity가 0.96임. 그래서 미래 예측 loss의 대부분이 정지한 배경을 베끼는 데 쓰이고, 로봇과 물체의 움직임을 배우는 신호는 약해짐. 또 기존 WAM은 큰 video generation model이나 별도 world model을 써서 학습·추론 계산량이 커 closed-loop 제어에 부담이 됨.

**어떻게 푸나**

ResWAM(Residual World-Action Model)은 현재 이미지, proprioception, 언어 지시를 받아 action chunk와 visual residual을 함께 출력함. visual residual은 고정된 DINOv3 encoder로 뽑은 H step(action chunk 길이) 뒤 프레임의 patch token에서 현재 프레임의 patch token을 뺀 값임. VLM backbone은 RynnBrain-1.1-2B이고, 그 위에 action branch와 residual branch로 된 0.5B 크기의 DiT(Diffusion Transformer)를 붙임. 두 branch는 각자 noise에서 출발하고 joint attention으로 정보를 주고받으며, VLM 출력과 현재 DINOv3 token에 cross-attention함. 학습은 두 branch 모두 conditional flow matching으로 하고, residual loss에는 0.1의 가중치를 줌. 추론 때는 두 branch를 10번의 Euler step으로 함께 denoise하며 pixel 복원이나 미래 프레임 decoding은 하지 않음. 전체 parameter는 2.3B이고 외부 로봇 데이터로 사전학습(robot pretraining)하지 않음.

**결과**

- RoboTwin 2.0(양팔 조작 과제 50개 시뮬레이션 benchmark) ablation에서 평균 성공률이 residual 예측 93.8%, 미래 DINOv3 feature 전체 예측 90.9%, residual branch 없는 action 전용 모델 89.9%임. VLM vision tower feature로 residual을 만들면 91.6%임.
- LIBERO-Plus(LIBERO 과제에 카메라·조명·배경 등 7종 교란을 건 10,030 episode)에서 평균 성공률 81.1%로 가장 높음. 가장 강한 VLA인 VLA-JEPA는 79.5%, 가장 강한 WAM인 LaWAM은 76.6%임. 학습은 교란 없는 LIBERO demonstration으로만 함.
- 계산량은 RTX A6000 한 장 기준으로 LIBERO-Plus에서 추론 1.0 TFLOPs, chunk당 지연 92.2ms로 비교 방법 중 가장 낮음. LaWAM은 198.1ms, video 생성 WAM인 Motus는 2,769.5ms임.
- 실제 Franka Research 3 로봇의 과제 3개(서랍을 열어 지우개를 넣은 뒤 다시 밀어 넣기, 오이를 접시에 놓기, 블록 3개 쌓기)에서 과제당 30회 평균 성공률이 80.0%임. π0.5는 70.0%, LaWAM은 68.9%임.

**한계**

핵심 ablation은 RoboTwin 2.0 한 곳에서만 했고, seed별 분산이나 신뢰구간은 보고하지 않음. residual branch를 뺀 모델도 89.9%로 π0.5(79.8%)보다 높아서, 다른 방법과의 차이 중 상당 부분은 RynnBrain backbone 덕일 수 있음. 비교 대상들은 backbone과 robot pretraining 여부가 달라 조건이 맞춰진 비교가 아님. residual이 왜 action 성능을 올리는지는 rank와 saliency 시각화로 설명할 뿐 직접 검증하지 않았고, 실로봇 과제는 3개임.

**누리랩 연구와의 연결**

- world model을 rollout 생성기가 아니라 VLA 학습의 보조 신호로 쓰는 가벼운 설계임. VLA에 world model을 붙이는 연구에서 미래 전체 대신 변화량을 예측하는 baseline으로 바로 쓸 수 있음.
- 예측한 residual이 로봇 팔과 조작 물체에 몰리므로, 예측 residual과 실제 residual의 차이를 failure detection 신호로 쓰는 실험을 해 볼 만함. 논문은 이 용도를 다루지 않음.

*대표 그림: (a)(b)는 VLA, 기존 WAM 두 종류, ResWAM의 예측 대상과 구조를 비교한 개념도임. (c)(d)는 측정 결과로, residual의 effective rank가 미래 feature보다 높은 막대그래프, 로봇 팔에 몰린 saliency map, 세 benchmark의 성공률·지연 비교를 보여 줌.*

*영상: [저자가 올린 영상으로, 로봇이 물체를 옮기는 동안 실제 DINOv3 residual을 이미지 위에 투영해 보여 줌.](https://blog-media.assets.alphaxiv.org/videos/01a1e883-aafe-7cc1-b29d-2c07cbecd08b/a07162d0-7309-4355-9c60-7ec3662201fd) (alphaXiv 요약에서 가져옴)*

---

### 2. PlanDiv: Test-Time Scaling with Latent Plans for Vision-Language-Action Models (74점)

[arXiv](https://arxiv.org/abs/2611.20010) · [PDF](https://arxiv.org/pdf/2611.20010) · [alphaXiv](https://www.alphaxiv.org/abs/2611.20010)

- **저자**: Hanbo Zhang, Lianlei Shan, Liuhaichen Yang, Zezhi Tang
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> VLA test-time scaling에서 후보 행동을 한 decoder로 여러 번 뽑는 대신, 학습된 latent plan마다 하나씩 뽑아 후보끼리 계획 자체가 다르게 만듦. CALVIN ABC→D에서 5개 과제 연속 성공률이 후보 1개일 때 56.9%에서 후보 8개일 때 69.9%로 오르고, 같은 수의 재샘플링 후보는 최대 64.9%에 그침.

**무슨 문제인가**

Test-time scaling은 VLA가 행동 후보를 여러 개 만들고 가장 좋은 것을 실행해 재학습 없이 성능을 올리는 방법임. RoboMonkey, MG-Select 같은 기존 방법은 후보를 고르는 점수만 바꾸고, 후보는 모두 한 decoder에서 temperature sampling이나 noise로 다시 뽑음. 저자들은 같은 학습 조건에서 재샘플링 방식 3가지를 비교해, 후보를 4개에서 8개로 늘려도 CALVIN 평균 완료 과제 수가 0.06~0.07만 오름을 보임. 한 계획 아래 뽑은 후보 8개 중 하나라도 성공하는 비율도 86%에 그쳐, 정책이 잘못된 접근 방향이나 하위 목표 순서를 고르면 어떤 선택기도 이를 고칠 수 없음.

**어떻게 푸나**

PlanDiv(plan diversity)는 OpenVLA backbone은 그대로 두고 action head만 바꿈. backbone을 한 번 통과시켜 action token 위치의 hidden state와 이를 평균한 context를 얻음. 작은 MLP planner가 학습된 seed K개와 context로 latent plan K개와 각 plan의 prior를 만들고, 서로 비슷한 plan에는 repulsion penalty를 줌. 공유된 masked-diffusion executor(가린 action token을 4단계에 걸쳐 채워 넣는 decoder)가 plan마다 8-step action chunk 하나씩을 만듦. 정책은 token 평균 log-probability가 가장 높은 후보를 실행하며, 별도 verifier나 reward model은 쓰지 않음. plan label 없이 demonstration만으로 학습하며, 각 plan의 복원 loss와 prior로 soft EM 방식의 가중치(responsibility)를 매겨 demonstration chunk를 잘 설명하는 plan이 더 많이 학습되게 함. prior 순위 상위 K개만 decode하므로 checkpoint 하나로 K_max 이하의 어떤 후보 수에도 씀.

**결과**

- CALVIN ABC→D(학습하지 않은 환경 D에서 5개 지시를 연속 수행하는 1000개 chain)에서 후보 8개의 평균 완료 과제 수가 PlanDiv 4.13, 재샘플링 3가지 3.93~3.97임. 같은 checkpoint에서 plan 하나만 고정하고 다시 뽑은 same-z는 3.95로, 차이가 plan에서 온다는 대조군 역할을 함.
- LIBERO-Long(장기 조작 과제 10개, 500 episode)에서 후보 4개 성공률이 PlanDiv 91.8%, 재샘플링 87.6~89.2%임. 후보 1개일 때의 실패 중 제거한 비율은 40% 대 18~21%임.
- decoder noise를 모두 고정하고 plan만 바꾸면 하위 과제 결과가 16.2%의 시작 상태에서 바뀜. noise만 바꾸면 7.2%임.
- 실제 Franka 팔에서 해법이 둘인 과제 2개(블록 두 개를 순서 상관없이 트레이에 넣기, 장애물 양옆 중 한쪽으로 캔 옮기기)의 성공이 PlanDiv 51/54, OpenVLA-OFT+ 40/54임. 해법이 하나인 그릇 밀기는 25/25 대 24/25로 비슷함.

**한계**

backbone은 OpenVLA-7B 하나, 로봇 팔도 하나뿐이며 저자도 이를 한계로 적음. 표의 수치에 seed 반복이나 분산이 없어 0.1~0.2 수준의 평균 완료 과제 수 차이가 얼마나 안정적인지 본문에서 확인 불가함. 실로봇은 과제 3개, 과제당 21~33회 시도이고, 기존 test-time scaling 방법과의 비교는 base policy가 서로 달라 실패 제거 비율만 비교함.

**누리랩 연구와의 연결**

- test-time optimization에서 후보 선택기보다 후보를 만드는 쪽이 성능 상한을 정한다는 측정 결과임. 우리 VLA inference-time planning 연구에서 후보 생성 쪽 baseline으로 바로 쓸 수 있음.
- plan만 바꿔 결과가 바뀌는지 보는 fixed-noise intervention은 counterfactual 분석 도구로 쓸 수 있음. 실패한 plan을 감지하고 다른 plan으로 바꾸는 failure recovery로도 이어짐.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 위쪽은 추론 과정으로, OpenVLA backbone 출력에서 planner가 plan K개를 만들고 공유 executor가 plan마다 후보를 채워 넣은 뒤 점수가 가장 높은 후보를 실행함. 아래쪽은 학습 과정으로, plan별 복원 loss로 responsibility 가중치를 매겨 전체 목적 함수를 만드는 흐름을 보임.*

---

### 3. ReuseMem: One Memory, Multiple Goals in Robot Manipulation (74점)

[arXiv](https://arxiv.org/abs/2611.21115) · [PDF](https://arxiv.org/pdf/2611.21115) · [alphaXiv](https://www.alphaxiv.org/abs/2611.21115) (요약 있음)

- **저자**: Yoonseok Kang, Dayeon Jung, Seunghoon Jeon, Wonjib Kim, Dongchul Park
- **분야**: Manipulation · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> 로봇이 나중에 올 요청을 모르는 채 기록한 시각 memory 하나를, 요청마다 다른 과거 장면을 골라 조작에 쓰도록 학습함. 시뮬레이션 과제 4개에서 한 기록에 딸린 두 요청을 모두 성공한 비율이 균등 선택 memory의 36.0%에서 60.5%로 오름.

**무슨 문제인가**

기존 memory-augmented policy는 대개 과제마다 따로 쌓은 history로 그 과제 하나를 푸는 상황에서 평가됨. 실제 보조 로봇은 장면을 볼 때 그 기록이 나중에 어떤 요청에 쓰일지 모름. 같은 기록에서 어떤 요청은 물체의 정체를, 다른 요청은 물체의 원래 위치를 꺼내 써야 함. 앞선 행동으로 장면이 바뀌어도 과거 사실은 그대로이므로, 무엇을 꺼낼지와 지금 어디를 잡을지를 함께 학습해야 함.

**어떻게 푸나**

ReuseMem은 목표와 무관하게 기록하는 Writer, 요청마다 과거 관측을 고르는 Reader, 고른 관측을 현재 장면과 합치는 action interface로 구성됨. Writer는 frozen encoder로 프레임마다 16×1024 시각 feature를 뽑고, 비슷한 feature는 한 번만 저장하되 시간 entry는 프레임마다 따로 둠. Reader는 언어 요청을 query로 삼아 reference 관측 4개와 reference마다 support 관측 3개를 고르고, 고른 간격의 coverage 프레임 8개를 더해 과거 관측 24칸을 채움. Reader의 학습 신호는 expert action 예측 loss임. 후보 선택을 최대 4개 만들어 고정된 policy가 여러 현재 장면에서 expert action을 얼마나 잘 예측하는지 비교하고, loss가 낮은 후보 쪽으로 Reader 점수를 맞춤. 그다음 갱신된 Reader의 greedy 선택을 입력으로 과거 관측과 현재 장면을 합치는 작은 fusion 층(폭 32)과 policy를 조정하는 low-rank 보정(rank 8)만 학습하고, π0.5 기반 기존 memory policy인 MME-VLA는 고정함. MME-VLA는 기억이 필요한 시뮬레이션 조작 benchmark RoboMME에서 낸 모델임.

**결과**

- RoboMME 장면을 바꿔 한 기록에 요청 2개를 붙인 시뮬레이션 과제 4개(과제당 테스트 기록 50개)에서 평가함. 같은 기록에서 환경을 매번 초기화하고 두 요청을 따로 실행했을 때 둘 다 성공한 비율(All-goal)이 Uniform-Memory 36.0%에서 60.5%로 오름. Uniform-Memory는 같은 bank, 같은 24칸, 같은 action 적응에서 고른 간격 프레임만 쓰는 비교 대상임. reset 없이 이어서 수행한 Sequence 성공률은 35.0%에서 58.0%로 오름.
- Reader 학습을 빼면 All-goal이 36.5%로 Uniform-Memory 수준이 됨. 현재 장면 하나로만 검색 선호를 만들면 53.0%임. 현재 장면 fusion을 빼면 All-goal은 55.5%, Sequence는 47.0%로 Sequence 쪽이 더 크게 내림.
- VLM이 keyframe을 고르고 subgoal을 내는 MemER(RoboMME 재현판)의 All-goal은 20.0%이고, 새 요청에 응답하는 시간은 ReuseMem 175 ms, MemER 1,112 ms임. 외부 시스템은 원래 memory·policy 구조를 그대로 써서 통제된 비교는 아님.
- 실제 SO101 팔(저가형 오픈소스 로봇 팔)로 시나리오 2개(케이스 옮기고 되돌리기, 장난감 옮기고 원래 자리 솔질 후 되돌리기)를 기록 20개씩 평가함. 세 요청을 모두 성공한 비율이 두 시나리오 모두 70%이고, Uniform-Memory는 45%와 60%임. 연속 수행 성공률은 65% 대 50%, 65% 대 55%임.

**한계**

시뮬레이션 과제는 저자가 RoboMME를 바꿔 만든 4개이고 요청은 기록당 2개, 실로봇은 시나리오 2개에 기록 20개씩임. 가려진 물체가 뒤바뀌는 VideoUnmaskSwap의 All-goal은 30%에 그치고, 정답 과거 관측을 직접 넣은 진단 조건(All-goal 72.0%)과도 차이가 남음. 고정된 Reader 구조(24칸) 외의 구조와 memory bank 상한인 2,048 entry를 넘는 긴 기록은 시험하지 않았고, 코드 공개 주소는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- robot memory 연구에서 한 기록을 여러 후속 요청에 재사용하는 평가 틀(All-goal, Sequence)과, 검색을 expert action 예측 loss로 감독하는 방식을 VLA memory의 비교 기준으로 쓸 수 있음.
- 실패 후 recovery도 물체의 원래 위치 같은 과거 관측을 다시 꺼내야 하는 경우가 많음. 같은 bank에서 recovery 요청을 읽는 실험으로 failure recovery와 이을 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 개요 그림으로, 케이스가 열린 장면(t1~t4)과 덮인 뒤 옮겨진 장면(t5~t8)이 Writer를 거쳐 시간 entry 8개의 memory bank로 저장됨. Reader가 USB 케이스 옮기기 요청에는 t2·t3·t6을, 원위치 요청에는 t1·t2·t7을 골라 현재 장면과 함께 action policy에 넣음.*

---

### 4. Certify, Then Select: Viability-Aware Runtime Steering of Frozen Diffusion Policies (74점)

[arXiv](https://arxiv.org/abs/2611.19047) · [PDF](https://arxiv.org/pdf/2611.19047) · [alphaXiv](https://www.alphaxiv.org/abs/2611.19047) · [프로젝트 페이지](https://clmoro.github.io/cast)

- **저자**: Angelo Moroncelli, Loris Roveda
- **분야**: Manipulation · robotics relevance 8/10 · 1차 스크리닝 70점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> 고정된 diffusion policy가 뽑은 action chunk 중 실행 중 들어온 제약을 통과한 것만 남기고, value ensemble이 그중 하나를 고르게 해서 재학습 없이 제약과 과제를 함께 지킴. robomimic Can의 제약 5종에서 joint success가 output filter의 0.37~0.61에서 0.70~0.89로 오름.

**무슨 문제인가**

diffusion policy는 배포 뒤 demonstration에 없던 제약(사람 팔, 선반, 힘 사용량 한도)을 만나고, 제약마다 재학습하기는 어려움. 기존 safety filter는 policy가 낸 action을 제약을 만족하도록 최소한으로 고치지만, 고칠 때 과제 완수 여부는 보지 않음. 고치는 양이 크면 로봇이 policy가 학습하지 않은 상태로 가서 멈춤. 또 지금 안전한 action이 있어도 몇 step 뒤에는 policy가 안전한 action을 하나도 못 뽑는 막다른 상태에 들어갈 수 있음.

**어떻게 푸나**

CAST(Certified Action Selection at Test time)는 매 결정 시점에 고정된 policy에서 action chunk N개(기본 8개)를 한 번에 뽑음. 각 chunk를 robot predictor와 hazard forecast로 앞을 예측해 control barrier function 조건(chunk 뒤 정지용 backup 구간 포함)으로 인증함. 인증된 chunk 중 value ensemble(작은 network 5개, 고정 policy rollout의 과제 성공률을 회귀)이 가장 높게 매긴 것을 실행함. 인증된 chunk가 없을 때만 output filter의 수정이나 backup으로 넘어감. CAST-V는 후보 chunk 뒤에서 model rollout을 돌려, 다음 L번의 결정에서도 인증된 sample이 계속 나올 확률(viability)이 기준 이상인 후보만 고름. CAST-VL은 rollout 대신 critic 없는 인증 controller의 log로 viability를 예측하는 network를 학습함. 이론으로는 인증된 step은 critic과 무관하게 안전하고, 실행 chunk 분포와 인증 조건부 policy 사이의 KL이 log N nats 이하임을 보임.

**결과**

- robomimic Can(시뮬레이션에서 캔을 집어 옮기는 조작 과제), 제약 5종, 조건마다 200 episode에서 joint success(과제 완수와 제약 준수를 둘 다 만족한 비율)를 잼. output filter는 0.37~0.61, CAST는 0.70~0.89이고 최대 위반율은 2.5%에서 0.5%로 내림. critic이 없는 방법들(DPCC, latent noise 최적화 등)은 힘 사용량 한도 조건을 빼면 filter와 0.08 이내였음.
- 같은 sample과 critic으로 순서만 바꾼 select-then-filter(먼저 고르고 나중에 수정)와 비교함. 새 힘 사용량 한도 2개에서 CAST 0.68, select-then-filter 0.46임. 장애물처럼 수정량이 작은 조건에서는 둘 다 0.88로 같았고, robomimic Square(사각 너트를 기둥에 끼우는 과제)의 한도 조건에서는 CAST가 0.04 낮았음.
- unicycle에서 학습 때 없던 금지 구역이 경로 하나를 막는 조건, policy마다 500 episode임. joint success는 filter 0.72, CAST 0.81, MPPI(model·지도·목표를 쓰는 planner) 0.91, CAST-V 0.99, CAST-VL 0.95임. sample 수만 1024개로 늘린 CAST는 0.14로 내림.
- planar quadrotor의 처음 보는 비행 금지 구역에서 filter는 56% episode에서 추락해 0.44임. MPPI 0.61, CAST 0.68, CAST-V 0.93, model rollout 없는 CAST-VL 0.98임.

**한계**

모든 실험이 시뮬레이션이고 실로봇 결과는 없음. manipulation 과제에서는 CAST-V가 CAST보다 나아지지 않았고, CAST-V는 결정당 계산 시간이 CAST의 10~50배임. 안전 보장은 robot에 반응하지 않는 hazard와 정지 상태까지의 passive safety로 한정되고, policy가 애초에 뽑지 않는 행동은 만들 수 없음.

**누리랩 연구와의 연결**

- VLA나 diffusion policy를 고정한 채 test-time에 sample을 뽑고 인증하고 고르는 구조임. 우리 test-time optimization 연구에서 critic 오차가 N이 커질수록 커지는 현상(N=8의 0.87이 N=32에서 0.77로 내림)을 같이 다뤄야 함을 보여 줌.
- viability는 앞으로 안전한 sample이 남을지를 미리 재는 값이라, failure detection과 recovery에서 막다른 상태를 실패 전에 잡는 신호로 쓸 수 있음.

*대표 그림: 금지 구역(zone)이 unicycle policy의 경로 하나를 막을 때 (a) safety filter는 zone 앞에서 멈추고, (b)(c) CAST-V와 CAST-VL은 viability 지도를 따라 막다른 경로를 피함. (d) 막대그래프는 처음 보는 zone에서의 joint success로 Filter 0.72, MPPI 0.91, CAST 0.81, CAST-V 0.99, CAST-VL 0.95임.*

---

### 5. TMA: Sim-to-Real Forceful Humanoid Manipulation via Tactile-Driven Motor Adaptation (73점)

[arXiv](https://arxiv.org/abs/2611.18976) · [PDF](https://arxiv.org/pdf/2611.18976) · [alphaXiv](https://www.alphaxiv.org/abs/2611.18976) (요약 있음) · [프로젝트 페이지](https://humanoid-tma.github.io)

- **저자**: Yiting Chen, Kelin Yu, Sarthak Kaingade, Bryan Trinh, Kaiyu Hang, Roberto Martin-martin, Nima Fazeli, X. Alice Wu
- **분야**: Manipulation · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> humanoid가 다섯 손가락 손으로 둥근 문손잡이를 돌려 문을 여는 policy를 시뮬레이션에서만 학습하고, 손끝 촉각의 2초 이력으로 행동을 조정해 실로봇에 그대로 옮김. 실제 문손잡이 4종 40회 시도에서 문을 연 횟수가 제안 방법 TMA 27회, 촉각 없는 기존 적응 방법 RMA 0회, 접촉 여부만 보는 reactive policy 6회임.

**무슨 문제인가**

둥근 문손잡이는 레버 손잡이와 달리 잡는 위치만 맞춰서는 열리지 않음. 여러 손가락으로 수직 힘을 나눠 주고, 미끄러지지 않을 만큼 마찰 torque를 만들어 spring과 latch 저항을 이겨야 함. 기존 humanoid loco-manipulation은 접촉 위치와 동작 궤적 위주로 설계되어 손가락 단위 힘 조절을 다루지 않았음. 마찰 계수나 spring 강성은 영상과 관절 각도로 보이지 않고, 안정된 grasp와 곧 미끄러질 grasp가 겉보기로 거의 같다는 점이 문제임.

**어떻게 푸나**

TMA(Tactile-Driven Motor Adaptation)는 RMA의 2단계 구조에 촉각을 넣은 것임. RMA(Rapid Motor Adaptation)는 시뮬레이션의 숨은 물리값을 latent로 압축하고, 배포 때는 최근 관측 이력으로 그 latent를 추정하는 방식임. 손끝 4개(엄지, 검지, 중지, 약지)의 3축 힘을 friction cone 좌표로 바꿔 손끝마다 수직 하중, 수직 대비 전단 각도, 전단 방향의 sin과 cos 4개 값을 만듦. 1단계에서는 knob 강성, preload, 마찰, 문 질량, 손잡이·문 각도 같은 privileged information 14차원을 8차원 latent로 압축하는 encoder와 policy를 PPO로 함께 학습함. 2단계에서는 두 모듈을 고정하고, 촉각·proprioception·손잡이 자세를 담은 2초(100 step) 관측 이력에서 그 latent를 회귀하는 adaptation encoder를 학습함. reward는 엄지와 다른 손가락 2개 이상이 센서 영역 안에서 손잡이를 잡았을 때만 회전·문 열림 보상을 온전히 주도록 걸어 둠. 출력은 오른팔 7관절과 손 구동 관절 6개의 위치 증분이고, 다리와 허리는 미리 학습된 locomotion controller가 고정된 채 균형을 잡음.

**결과**

- 시뮬레이션 촉각 입력 ablation(3 seed, 설정당 4,096 episode)에서 문 열림 성공률이 cone 좌표 표현 80.9%, 접촉 여부만 쓰면 73.6%, 수직 하중만 쓰면 74.2%, 전단 성분만 쓰면 65.1%임. grasp 성공률도 91.3%로 네 설정 중 가장 높음.
- 실제 Unitree G1과 BrainCo Revo2 손으로 시판 문손잡이 4종에서 손잡이당 10회씩, 실세계 fine-tuning 없이 평가함. 문을 연 횟수가 TMA 27/40, reactive policy 6/40, RMA 0/40임.
- reactive policy(3 frame 접촉 여부, latent adaptation 없음)는 grasp는 23회 성공했지만 문 열기로 이어진 것은 6회임. 촉각 없는 RMA는 grasp 자체를 1회만 유지했고, 저자는 back-drive가 안 되는 손이라 접촉 힘이 관절 각도에 드러나지 않기 때문이라고 해석함.

**한계**

실로봇 baseline 둘 다 TMA와 두 가지 이상이 다르고, 촉각 표현은 그대로 두고 이력만 뺀 ablation이 없음. 그래서 실세계 차이가 촉각 표현 때문인지 adaptation 이력 때문인지 가를 수 없음. 실험은 AprilTag로 손잡이 자세를 주고 손잡이 테두리에 마찰을 높이는 테이프를 붙인 조건이며, 과제는 문 열기 하나뿐임. 손끝 패드가 손상되면 성능이 크게 낮아졌다고 저자가 적었으나 수치는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- 촉각 이력으로 숨은 접촉 조건(마찰, 기구 저항)을 추정해 행동을 바꾸는 구조라, tactile 기반 manipulation과 미끄러짐 같은 failure를 미리 감지하는 연구에서 비교 대상이 됨.
- friction cone 좌표 촉각 표현은 접촉 여부나 힘 크기만 쓰는 표현보다 시뮬레이션에서 일관되게 높았으므로, dexterous manipulation policy의 촉각 입력 설계에 바로 가져다 쓸 수 있음.

*대표 그림: 실험에 쓴 문 구조를 그린 개념도이며 측정 결과가 아님. 왼쪽은 spring이 걸린 손잡이 관절 θK, 가운데는 열린 문의 hinge 관절 θD, 오른쪽 확대 그림은 손잡이 회전에 연동되어 움직이는 latch를 보여 줌.*

*영상: [저자가 올린 실로봇 영상으로, humanoid가 끝이 가늘어지는 원통형 1번 손잡이를 여러 손가락으로 잡아 돌리고 문을 밀어 여는 자율 실행 장면을 1배속으로 찍은 것임.](https://blog-media.assets.alphaxiv.org/videos/01a1e7c2-4f57-7474-9727-a3f5892f9fb4/c32d881a-53ee-418f-8b66-762c560c00ee) (alphaXiv 요약에서 가져옴)*

---

### 6. Lost in the Hallway: Benchmarking Persistent Spatial Memory Across Revisits (70점)

[arXiv](https://arxiv.org/abs/2611.21485) · [PDF](https://arxiv.org/pdf/2611.21485) · [alphaXiv](https://www.alphaxiv.org/abs/2611.21485)

- **저자**: Henry Zheng, Weibo Gong, Yang Yue, Rui Huang, Yang Zhang, Gao Huang
- **분야**: Embodied AI · robotics relevance 8/10 · 1차 스크리닝 74점
- **학회**: ByteDance 자체 양식 · 근거: 글꼴 ByteSans, 학회 양식 아님
- **읽은 원문**: PDF 전문

> 같은 집의 방을 여러 번 다시 들어가는 egocentric 영상에서 MLLM이 지금 방이 예전에 들른 어느 방인지 알아보는지를 재는 benchmark ReSpaceBench를 만듦. 가장 강한 zero-shot 모델도 450문항 부분집합에서 52.2%로 사람의 90.1%에 크게 못 미침.

**무슨 문제인가**

로봇이나 웨어러블 기기는 같은 방에 시점이 바뀐 채로, 다른 방을 거친 뒤에, 물건이 바뀐 뒤에 다시 들어옴. 이때 새 관측을 올바른 물리적 방에 연결해야 기억을 갱신할 수 있음. 기존 video spatial benchmark는 방을 다시 들렀는지를 따로 묻지 않음. 비슷한 OVO-S-Bench는 방이 화면에 잠깐 비치기만 해도 방문으로 셈. 같은 종류의 다른 방(침실 두 개 등)을 혼동 대상으로 일부러 넣지도 않음.

**어떻게 푸나**

ReSpaceBench는 3D-FRONT·ProcTHOR 합성 집, FARO 레이저 스캔한 실제 집, PICO 헤드셋으로 찍은 실제 집 영상으로 만든 benchmark임. 방문은 방에 실제로 들어간 것만 세고, 복도와 계단은 세지 않음. 질문 template이 질문과 함께 필요한 이동 경로를 정하고, Habitat navmesh로 그 경로를 따라가는 카메라 궤적을 만들어 BlenderProc으로 렌더링함. 방에 들어갈 때마다 6~9초 동안 270도를 둘러봄. 정답은 scene metadata와 실제 방 진입 순서에서 다시 계산하고, 규칙 검사와 사람 검수로 영상과 어긋나는 문항을 지움. 과제는 9개이며 association(T1~T3: 지금 방이 예전 어느 방인지, 몇 번 왔는지), persistent state(T4~T7: 방·물건 개수, 세션 간 물건 변화), reasoning(T8~T9: 문으로 이어진 방, 다음에 들른 방)으로 나뉨. 모델 입력은 전체 영상과 질문이고, 답은 선택지 글자나 숫자임. 따로 ProcTHOR 학습 장면에서 만든 30,018문항 학습셋 RS-30K도 제공하며, benchmark와 장면·경로·영상·template이 겹치지 않음.

**결과**

- 590개 장면, 3,244문항에서 32개 모델을 평가함. 9개 과제 평균 정확도는 GPT-5.6 Sol이 50.5%로 가장 높고, open-source 중 최고는 Qwen3-VL-32B의 41.3%임. 영상 없이 질문만 준 Blind baseline은 27.4%이고, spatial 특화 모델 5개는 22.0~28.8%에 그침.
- 과제당 50문항인 ReSpaceBench-mini에서 사람 3명 평균은 90.1%, GPT-5.6 Sol은 52.2%임. 같은 GPT-5.6 Sol을 backbone으로 쓴 agentic 영상 이해 framework는 AVP 44.0%, DVD 44.0%, VideoAgent 30.0%로 직접 추론보다 낮음.
- T1(질문 영상의 방을 예전 방문 방과 짝짓기)에서 proprietary 모델 6개의 오류 중 66.5~88.3%가 들른 방 중 다른 방을 고른 경우임. 들렀는지 여부는 무작위보다 잘 가리지만, 들른 방 질문의 44.8~58.0%에서 엉뚱한 방을 고름.
- RS-30K로 Qwen3-VL-8B를 fine-tuning하면 평균 정확도가 35.5%에서 60.4%로 오름. 학습에 없던 3D-FRONT는 21.9퍼센트포인트, 실제 집 218문항은 14.8퍼센트포인트 오름. 같은 ProcTHOR 장면군은 39.8퍼센트포인트 올라 상승 폭이 가장 큼.

**한계**

기여는 benchmark와 학습 데이터이고, 공간 기억을 위한 새 모델 구조는 제안하지 않음. 문항의 93%가 합성 장면이고 실제 집 문항은 218개뿐이며, 로봇이 직접 움직이는 closed-loop 과제는 없음. RS-30K만으로 학습하면 일부 외부 benchmark 성능이 내려가 일반 데이터와 섞어야 했고, 본문에 코드·데이터 공개 주소는 적혀 있지 않음.

**누리랩 연구와의 연결**

- robot memory와 scene graph 연구에서 방 단위 재식별(loop closure에 해당)을 MLLM 수준에서 재는 평가 도구로 쓸 수 있음. room ID를 정답으로 주면 T7 정확도가 47.0%에서 51.9%로만 올라, identity 외 상태 추적 문제도 따로 남아 있음을 보임.
- 128프레임 고정 예산에서 방 진입·둘러보기·복도 구간을 하나씩 남기는 sampling이 GPT-5.6 Sol 기준 55.3%로 uniform sampling 47.6%보다 높음. active perception이나 memory 압축에서 어떤 관측을 남길지 정할 때 참고가 됨.

*대표 그림: 왼쪽은 같은 방을 다른 시점에서 알아보기, 비슷하지만 다른 방 가르기, 다시 들렀을 때 바뀐 상태 알아보기라는 세 가지 어려움을 집 단면도와 방 사진으로 보임. 오른쪽 radar chart는 450문항 부분집합의 9개 과제에서 사람(90.1%)과 MLLM 5종(GPT-5.6 Sol 52.2%, Qwen3-VL-8B 41.1% 등)의 정확도를 비교함.*

---

### 7. JEPA4R: Embodied JEPA World Models with 4D Point Planning (68점)

[arXiv](https://arxiv.org/abs/2611.19771) · [PDF](https://arxiv.org/pdf/2611.19771) · [alphaXiv](https://www.alphaxiv.org/abs/2611.19771) (요약 있음)

- **저자**: Jiarui Dong, Zhiheng Liang, Yanjun Li, Zeyu Zhang, Heejeong Nam, Haoyu Chen, Hao Tang
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> JEPA world model의 입력을 RGB 이미지에서 depth camera 하나로 만든 색 point cloud로 바꾸고, 고정된 latent 위에 policy head를 학습함. OGBench Cube-Double 성공률이 가장 강한 2D 이미지 기반 JEPA world model인 PLDM의 3.6%에서 41.6%로 오름.

**무슨 문제인가**

JEPA world model은 픽셀 대신 미래 latent를 예측하고 latent 공간에서 planning함. 지금까지 나온 모델은 대부분 2D 이미지를 입력으로 받아서, 조작에 필요한 거리·위치 정보(metric geometry)를 외관과 원근에서 추론해야 함. 또 latent는 복원용으로 학습되지 않아서 모델이 무엇을 상상하는지 사람이 확인하기 어려움. 평가도 주로 시뮬레이션의 짧은 goal-reaching planning이라, latent가 policy 학습에 얼마나 쓸모 있는지는 잘 드러나지 않음.

**어떻게 푸나**

JEPA4R은 고정된 eye-to-hand depth camera 영상을 world 좌표 점으로 올리고, 작업 공간 밖과 책상·바닥을 지운 뒤 xyz와 rgb를 가진 점 1,200개를 뽑아 입력으로 씀. PointNet encoder(5.51M parameter, 비교 대상 ViT-tiny와 크기를 맞춤)가 이 점 집합을 192차원 latent로 바꿈. transformer predictor가 최근 latent 3개와 action block을 받아 다음 latent를 예측함. 학습에는 기존 2D JEPA world model인 LeWM과 같은 예측 loss와 SIGReg(latent 분포를 Gaussian에 맞춰 collapse를 막는 정규화)로 학습함. encoder를 고정한 채 policy head를 따로 학습해 latent에서 바로 action을 냄. 이 구조를 저자는 4D point planning이라 부름. 학습이 끝난 world model 위에 PAGE-4D(동적 장면용 feed-forward 3D 복원 모델)를 바탕으로 한 decoder를 붙여, 관측 latent나 상상한 latent를 다시 점 1,200개로 되돌림. decoder는 확인용이고 planning과 제어에는 쓰지 않음.

**결과**

- OGBench(시뮬레이션 goal-conditioned 조작 benchmark)에서 같은 시뮬레이션 rollout을 이미지와 point cloud로 짝지어 학습하고 같은 policy head로 비교함. 고정 latent 위 policy 성공률이 Cube-Single에서 PLDM 46.8%에서 78.4%로, Scene에서 46.1%에서 64.8%로 오름. Puzzle 4×5에서는 2D 이미지 encoder인 LeJEPA(96.4%)보다 낮은 68.0%이고, Cube-Quadruple은 모든 encoder가 0%임.
- CortexBench(적은 demonstration으로 behavior cloning해 표현을 비교하는 benchmark)의 Adroit Relocate(손으로 공을 집어 목표로 옮기는 과제)에서 성공률이 88.0%로, 다음 순위 R3M의 65.3%보다 높음. MetaWorld 과제 5개 평균은 98.4%, R3M은 96.0%임. 성공률은 20번 평가 중 최고값임.
- decoder로 상상한 rollout을 되돌렸을 때, 관측 점과의 평균 최근접 거리가 200 environment step에서 0.89cm임. 다른 episode의 action을 넣으면 같은 step에서 11.46cm로 커짐(OGBench Cube, 64 episode 평균).
- 실제 RealMan RM75-B arm에서 digital twin에서만 학습한 모델로 gripper 집기·밀기와 dexterous hand로 물체 빼내기를 zero-shot 실행함. 실행 장면 8개만 그림으로 보이고 성공률이나 시도 횟수는 본문에서 확인 불가임.

**한계**

point cloud 쪽은 renderer의 segmentation으로 배경과 고정물을 지운 입력을 받지만, 2D JEPA는 전체 이미지를 받으므로 입력 modality 외의 차이가 섞여 있음. LeWM과 predictor·loss·planner를 모두 맞춘 CEM planning 비교에서는 JEPA4R 대 LeWM이 UR5e에서 65.2% 대 69.4%, RM75-B twin에서 79.8% 대 73.8%임. 저자도 이 차이가 50회 추정의 오차(약 6퍼센트포인트) 안이라고 밝힘. 실로봇은 정성적 시연뿐이고, 본문에 코드 주소가 없음.

**누리랩 연구와의 연결**

- 상상한 latent rollout을 metric 단위 point cloud로 되돌려 실행 전에 확인하는 구조라, world model 기반 failure detection과 실행 전 안전 확인에 바로 쓸 수 있는 도구임. action이 틀리면 decode 오차가 0.89cm에서 11.46cm로 벌어지는 결과는 이상 감지 신호로 시험해 볼 만함.
- planning 성공률만이 아니라 고정 latent 위 policy 성공률로 world model 표현을 비교하는 평가 방식은, object-centric 3D 표현이나 3DGS 기반 world model을 평가할 때 그대로 가져다 쓸 수 있음.

*대표 그림: OGBench Cube-Single 장면 하나를 흰 세로선 기준으로 나눠, 왼쪽은 2D JEPA가 받는 카메라 이미지, 오른쪽은 JEPA4R이 받는 색 point cloud로 보여 줌. 측정 결과가 아니라 두 입력 형태를 비교한 그림이고, gripper는 보라색, 큐브는 빨간색 점으로 보임.*

---

### 8. Conditional Optimal Transport and Triangular Maps for Imitation Learning (68점)

[arXiv](https://arxiv.org/abs/2611.19815) · [PDF](https://arxiv.org/pdf/2611.19815) · [alphaXiv](https://www.alphaxiv.org/abs/2611.19815) · [코드](https://github.com/Mohd9485/transport-policies)

- **저자**: Mohammad Al-Jarrah, Yuhang Mei, Karen Leung, Bamdad Hosseini, Amirhossein Taghvaei
- **분야**: Manipulation · robotics relevance 8/10 · 1차 스크리닝 74점
- **학회**: CoRL 양식 (추정) · 근거: 1단 구성, 초록 아래 'Keywords:' 줄
- **읽은 원문**: PDF 전문

> Diffusion Policy처럼 Gaussian noise에서 행동을 만들지 않고, demonstration에서 뽑은 action chunk 하나를 현재 관측에 맞는 action chunk로 옮기는 방식으로 imitation learning policy를 만듦. Push-T에서 0.23M 파라미터 network를 한 번만 평가해 점수 0.943을 얻어 Diffusion Policy의 0.915보다 높음.

**무슨 문제인가**

Diffusion Policy(DP)는 같은 관측에서 여러 행동이 가능한 경우를 다루려고 행동 분포 전체를 diffusion model로 배움. 그런데 행동 하나를 만들 때마다 Gaussian noise에서 출발해 큰 network를 수십에서 100번 평가해야 해서 실시간 실행에 부담이 큼. Consistency Policy(CP) 같은 distillation이나 flow matching은 평가 횟수를 줄이지만 여전히 과제 정보가 없는 Gaussian에서 출발함. 출발 분포를 더 유익하게 바꾼 기존 연구는 따로 학습한 모델, 사전 지식, 또는 과거 실행 행동과의 짝짓기가 필요했음.

**어떻게 푸나**

저자들은 policy를 조건부 sampling 문제로 다시 씀. 관측 이력 s와 reference sample z를 받아 (s, T(s, z))를 내놓는 triangular map을 학습함. 이 map이 (관측, reference) 곱분포를 (관측, action chunk) 결합분포로 옮기면, T(s, ·)는 조건부 행동 분포를 만듦. 이 틀에서 DP와 CP는 reference가 Gaussian인 특수한 경우가 되고, reference는 설계 변수가 됨. 저자들은 reference를 demonstration action chunk들의 경험 분포 P_A로 둠. 실행 시 매 re-planning 시점마다 demonstration에서 action chunk 하나를 관측과 무관하게 새로 뽑고, T가 이를 현재 관측에 맞는 action chunk로 옮김. map T를 배우는 방식에 따라 세 가지 policy가 나옴. OTP(optimal transport policy)는 max–min 문제로 조건부 OT map을 배워 network 1회 평가로 행동을 냄. FMP(flow matching policy)와 SIP(stochastic interpolant policy)는 regression으로 vector field를 배우고, 실행 때 ODE와 SDE를 network 200회 평가로 적분함.

**결과**

- Push-T(평면에서 원형 end effector로 T자 블록을 목표 자세로 미는 과제, state 입력)에서 seed 3개 × 초기 조건 500개 평균 점수가 SIP 0.965, FMP 0.947, OTP 0.943임. DP는 0.915, CP 1-step은 0.938임. OTP는 0.23M 파라미터에 학습 10.6분이고, DP는 65.8M 파라미터에 학습 268.3분임.
- reference의 효과를 따로 본 비교에서 OTP의 reference를 P_A에서 Gaussian으로 바꾸면 Push-T 점수가 0.943에서 0.380으로 내림. 적분을 쓰는 policy들은 step 100에서 두 reference가 비슷하고, step 수를 줄일수록 P_A 쪽이 점수를 더 잘 유지함.
- robomimic Square(로봇 팔로 사각 너트를 집어 기둥에 끼우는 시뮬레이션 과제)에서 수정 없는 OTP 성공률은 0.768로 SIP 0.913, DP 0.938보다 낮음. 학습 중 로봇 state에 noise를 넣고 sample 8개의 평균 chunk를 실행하면 OTP는 0.895가 되어 CP 1-step 0.900과 비슷함.
- 같은 Square 설정에서 OTP의 episode당 시간은 0.12초이고 SIP와 DP는 1.24초임. 두 수정을 모두 적용하면 DP 성공률은 0.947로 OTP 0.895보다 0.052 높음.

**한계**

실험은 state 기반 시뮬레이션 과제 2개뿐이고, Push-T는 같은 관측에서 행동 분포가 거의 하나의 mode라서 이 틀의 출발점인 multimodal 행동 분포 표현은 직접 검증되지 않았음. baseline은 공개 설정을 그대로 썼고 제안 방법만 이 연구에 맞춰 설정을 골랐음. Square에서 쓴 평균 chunk 실행은 multimodal 분포에서는 mode 사이 행동을 낼 수 있고, 이미지 입력과 실로봇 평가는 이후 과제로 남음.

**누리랩 연구와의 연결**

- VLA의 flow matching action head를 Gaussian이 아닌 demonstration action chunk에서 출발시키는 설계로 바로 옮겨 볼 수 있음. 1회 평가 OTP는 inference 비용을 줄이는 비교 대상이 됨.
- OTP는 같은 관측에서 sample 여러 개를 한 번의 batch 평가로 얻으므로, 이 sample들의 분산을 failure detection 신호로 쓰거나 test-time에 sample을 고르는 규칙과 묶어 볼 수 있음. 저자들도 Square 실패 episode의 대부분에서 연속 chunk 사이 큰 위치 jump를 관찰함.

*대표 그림: Push-T의 같은 관측에서 시작한 한 episode를 OTP(왼쪽)와 CP 1-step(오른쪽)으로 비교한 그림임. 회색 선은 각 chunk의 reference sample, 점선은 reference와 변환된 행동을 잇고, 실행된 행동은 실행 후 점수로 색칠됨. CP의 Gaussian sample은 화면 밖까지 퍼져 있고 OTP의 reference는 작업 공간 안의 궤적 모양임.*

---

### 9. Bring Back Language to Actions: Restoring VLM capabilities in VLA Models via Parameter Merging (68점)

[arXiv](https://arxiv.org/abs/2611.18891) · [PDF](https://arxiv.org/pdf/2611.18891) · [alphaXiv](https://www.alphaxiv.org/abs/2611.18891)

- **저자**: Mohamed Salim Aissi, Olivier Sigaud, Laure Soulier, Nicolas Thome
- **분야**: VLA · robotics relevance 8/10 · 1차 스크리닝 72점
- **학회**: ACL 계열 양식 (추정) · 근거: A4 용지, 2단 구성
- **읽은 원문**: PDF 전문

> VLA로 fine-tuning하면서 잃은 VLM의 언어 능력을, 두 모델 가중치 차이를 SVD 성분별 계수로 VLM에 다시 더하는 방식으로 되살림. π0.5 기반 merged model은 COCO caption ROUGE-L을 9.4에서 29.5로 올리면서 LIBERO 성공률은 원래 VLA와 비슷하게 유지함.

**무슨 문제인가**

VLA는 VLM을 robot demonstration으로 fine-tuning해서 만들며, 이 과정에서 장면 설명이나 VQA 같은 원래 언어 능력을 거의 잃음(catastrophic forgetting). 이를 막는 기존 방법은 구조를 바꾸거나 언어 데이터와 action 데이터를 섞어 다시 학습해야 해서, 이미 학습된 VLA에 나중에 적용하기 어려움. VLM과 VLA 가중치를 한 계수로 섞는 model merging은 재학습이 없지만, 언어와 action 중 하나를 크게 잃는 결과가 나옴.

**어떻게 푸나**

같은 backbone(PaliGemma-3B)을 공유하는 VLM과 VLA를 모두 고정하고, 층마다 VLA 가중치에서 VLM 가중치를 뺀 task vector를 구함. 이 task vector를 SVD로 나눠 singular component마다 0과 1 사이의 계수 α를 하나씩 둠. merged model의 가중치는 VLM 가중치에 각 component를 α만큼 곱해 더한 값이고, action head는 VLA 것을 그대로 씀. α는 네 항의 합을 Adam으로 줄여서 학습함: VLM이 단 caption에 대한 NLL, VLA가 낸 action에 대한 loss, VLM 출력 분포와의 KL, VLA 출력 분포와의 KL. 학습 데이터는 LIBERO demonstration 관측에 VLM caption을 붙인 5,000개와 VLA action chunk를 붙인 5,000개임. 학습하는 값은 약 38만 개의 α뿐이고, H100 1장에서 약 3시간 걸림.

**결과**

- π0.5(flow matching VLA)에 적용한 merged model은 COCO caption ROUGE-L 29.5, VQAv2 정확도 48.7을 얻음. 원래 π0.5는 9.4와 8.2, VLM은 33.6과 53.8임. LIBERO(시뮬레이션 조작 benchmark) Spatial/Goal/Object 성공률은 89.3/88.1/93.3%로, 원래 π0.5의 88/90/96%와 비슷함.
- 층마다 계수 하나만 같은 목적함수로 학습하는 AdaMerging은 ROUGE-L 28.1까지 올리지만 LIBERO 성공률이 6.2/2.9/3.7%로 내려감. 고정 계수로 섞는 기존 merging 방법들(Model Soup α≤0.7, 일부 성분만 남기는 DARE, 구면 보간 SLERP)은 LIBERO 세 suite 모두 0%임.
- autoregressive VLA인 π0-FAST에서는 복원 폭이 작음. ROUGE-L은 1.2에서 18.6으로 오르고, LIBERO 성공률은 원래 70/82/88%에서 61.2/73.1/79.8%로 내려감.
- SVD rank를 줄이는 ablation에서 ROUGE-L은 rank 16부터 약 30에서 더 오르지 않음. LIBERO 평균 성공률은 rank 16 이하에서 0%, 256에서 64%이고, 1024 이상에서야 90%를 넘음.

**한계**

실험은 모두 시뮬레이션이며, 학습용 언어·action 데이터를 LIBERO 하나에서 두 원래 모델의 출력으로 만들었음. 그래서 다른 과제·embodiment·실로봇에서의 일반화는 보이지 않았고, RoboCasa 과제 3개 결과만 부록에 있음. 언어와 action을 함께 다시 학습하는 co-training 방법과의 직접 비교는 없고, 코드는 accept 후 공개 예정이라고만 적혀 있음.

**누리랩 연구와의 연결**

- VLA가 언어 능력을 되찾으면 실행 중 장면 설명이나 실패 원인 서술 같은 질의에 같은 모델로 답할 수 있음. VLA failure detection과 language feedback 연구에서 별도 VLM 없이 쓰는 baseline 후보임.
- 언어는 상위 singular direction 몇 개에, action은 넓은 하위 성분에 퍼져 있다는 rank 분석은 VLA fine-tuning 시 어떤 성분을 고정할지 정하는 근거로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법의 목적을 그린 개념도임. 같은 LIBERO 장면에서 VLM은 장면 설명만 하고 action을 못 내며, VLA는 action 열만 내고 글을 못 쓰며, merging 결과는 둘 다 하는 모습을 막대 그림과 함께 보여 줌.*

---

### 10. FAVR: Flow-Aware Visual Residual Alignment for Vision-Language-Action Policies (67점)

[arXiv](https://arxiv.org/abs/2611.20971) · [PDF](https://arxiv.org/pdf/2611.20971) · [alphaXiv](https://www.alphaxiv.org/abs/2611.20971)

- **저자**: Qixuan Wu, Xiaole Yang, Yuguang Yang, Canyu Chen, Linlin Yang, Haixia Pan, Guodong Guo, Baochang Zhang
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 74점
- **읽은 원문**: PDF 전문

> 고정된 flow-based VLA의 action head 바로 앞에 video encoder 특징을 넣고, 특징의 채널별 gate를 flow step마다 velocity 오차를 줄이는 최적화로 다시 계산함. RoboTwin 2.0에서 LingBot-VLA의 평균 성공률을 87.12%에서 90.04%로 올림.

**무슨 문제인가**

V-JEPA 같은 video 사전학습 표현은 장면의 시간 변화를 담고 있어 VLA에 넣으면 조작 성능이 오른다는 보고가 있음. 그런데 π0.5 같은 flow-based policy는 action chunk를 여러 flow step에 걸쳐 velocity를 반복 계산해 만듦. 시각 문맥은 chunk 안에서 고정이어도 noisy action과 policy 특징은 step마다 바뀌므로, 시각 특징이 기여해야 할 양도 step마다 달라질 수 있음. 기존 방법(JEPA-VLA, PVI)은 이 기여를 학습으로 암묵적으로 맞출 뿐, 넣은 특징이 velocity를 어떻게 바꾸는지 직접 따지지 않음.

**어떻게 푸나**

FAVR(Flow-Aware Visual Residual Alignment)는 VLA와 V-JEPA 2.1 video encoder를 모두 고정하고 작은 interface만 학습함. 최근 10 frame의 video 특징은 linear TTT(Test-Time Training: 입력이 들어올 때마다 key-to-value 행렬 S를 gradient 한 번으로 갱신하는 recurrent state)에 누적됨. 각 flow step에서 action expert의 마지막 hidden feature h가 S를 query해 시각 특징 x를 읽어 옴. action head가 affine(v = Wh + b)이므로 x에 gate g를 곱해 더하면 velocity 변화가 W·diag(x)·g로 정확히 계산됨. 작은 predictor는 정답 velocity와 base velocity의 차이(residual)를 추정하도록 학습됨. gate g∈[0,1]은 velocity 변화가 이 추정 residual에 맞도록 box-constrained least squares로 풂. 풀이는 FISTA(가속 proximal gradient 반복 알고리즘)를 8~128회 반복하거나, 채널 간 상호작용을 버린 대각 근사 후 스칼라 하나로 크기를 맞추는 closed-form 근사(FAVR-CF)로 함.

**결과**

- flow step마다 gate를 다시 푸는 효과: RoboTwin 2.0 과제 5개, 1,000 step 학습, 과제당 50회 평가에서 평균 성공률이 첫 step gate를 모든 step에 재사용할 때 72.0%, FAVR 82.0%임. 고정 LingBot-VLA는 68.8%임.
- RoboTwin 2.0(양팔 조작 과제 50개, 과제당 100 rollout): LingBot-VLA 성공률이 교란 없는 데이터로 학습해 교란 없는 장면에서 평가하면 87.12%에서 90.04%로, 무작위 교란 장면에서 평가하면 86.88%에서 89.38%로 오름. 이 benchmark에서 다른 video 주입 방법과의 비교는 없음.
- LIBERO-Plus(카메라·조명·배치 등 7종 교란 10,030개 시나리오): 같은 고정 π0.5에 붙였을 때 FAVR 85.05%, PVI 83.63%, JEPA-VLA 81.96%, 고정 π0.5 84.22%임. 학습 parameter는 FAVR 2.190M, JEPA-VLA 24.129M, PVI 444.445M임.
- 실로봇(Cobot Magic 양팔, 과제당 demonstration 35개, 20회 평가): 같은 추가 학습량에서 block pick-and-place 15/20 대 continued fine-tuning 12/20, 종이컵 잡기 13/20 대 11/20임.

**한계**

개선 폭이 작음: 고정 π0.5 대비 LIBERO 평균 성공률은 97.40%에서 98.60%로 1.2퍼센트포인트, LIBERO-Plus는 0.83퍼센트포인트 오르고 seed 반복이나 분산은 보고되지 않음. 핵심 ablation은 과제 5개를 1,000 step만 학습한 조건이고, 고정 baseline 값은 이전 평가 결과를 가져다 씀. 기억이 필요한 실로봇 과제 2개는 각 7/10에 그쳤고, 과제 학습이 안 된 base policy에 붙이면 조작이 되지 않아 base policy 능력에 기댐. 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- 고정 VLA의 affine action head에서 넣은 특징의 velocity 변화를 식으로 바로 계산하는 방식임. policy 가중치를 건드리지 않는 test-time steering이나 inference-time 보정 연구에 가져다 쓸 수 있음.
- open microwave 과제에서 wrist camera video를 더하면 gripper 미끄러짐을 보고 성공률이 45%에서 64%로 오름. 접촉 상태 변화를 감지해 recovery로 이어 가는 failure detection 연구의 비교 사례가 됨.

*대표 그림: 같은 video 문맥에서 τ=1.0부터 0.1까지 다섯 flow step의 채널 gate 값을 heatmap으로 비교한 그림임. 공유 gate는 다섯 step이 같은 패턴이고 평균 성공률 72.0%, flow-aware gate는 τ가 0에 가까울수록 1에 가까운 채널이 늘어나며 평균 성공률 82.0%로 표시됨.*

---

### 11. Successive Convexification in Learned World Models for Safe Offline Planning (66점)

[arXiv](https://arxiv.org/abs/2611.19466) · [PDF](https://arxiv.org/pdf/2611.19466) · [alphaXiv](https://www.alphaxiv.org/abs/2611.19466) · [코드](https://github.com/youngers2006/scwm)

- **저자**: Samuel Younger
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 74점
- **학회**: L4DC 2027 투고 · 근거: comments에 "28 pages, 13 figures. Under review at L4DC 2027"
- **읽은 원문**: PDF 전문

> offline 데이터로 학습한 latent world model 안에서 안전 planning을 sampling 대신 successive convex programming으로 풀고, 학습한 barrier 함수를 매 step 제약으로 넣음. 같은 계산 시간에 128배 많은 sample을 쓰는 MPPI·CEM과 비교하면, 위반율은 Lipschitz 상한 1.5 모델에서만 3~4퍼센트포인트 낮고 유의하지 않음. 대신 매 step 계획이 KKT point인지 보고함.

**무슨 문제인가**

offline 데이터로 학습한 world model에서 쓰는 planner는 대부분 CEM, MPPI 같은 sampling 방식임. 이 방식은 안전 제약을 penalty로 점수에 섞거나 위반한 sample을 버리는 방식으로만 다루므로, 제약이 탐색 방향을 정하지 못함. 그래서 안전한 영역이 좁아지거나 horizon이 길어지면 안전한 action sequence를 찾을 확률이 낮아짐. 또 sample이 모두 위반일 때 안전한 계획이 원래 없는지, sample이 모자란지 구분하지 못함.

**어떻게 푸나**

관측을 JEPA(Joint-Embedding Predictive Architecture) encoder로 latent z에 넣고, 같은 latent에서 dynamics, reward, value, barrier network를 offline 데이터로 학습함. barrier network는 장애물까지 거리를 회귀하고, 이를 써서 discrete-time CBF(control barrier function) 조건을 horizon의 매 step 제약으로 둠. 이 최적 제어 문제를 SCP(successive convex programming)로 풂: 기준 궤적 주변에서 network를 선형화해 convex QP를 풀고, trust region을 조절하며 반복함. SCP가 수렴을 보장받으려면 network가 매끄러워야 하므로, MaxMin activation을 매끄럽게 바꾸고 spectral normalization으로 layer별 Lipschitz 상한을 걺. 저자는 이 상한과 smoothing 폭으로 선형화 오차의 상한을 증명함(Proposition 1). SCP는 시작점에 따라 결과가 달라지므로 작은 MPPI(512개 sequence, 6 round)의 계획에서 시작함(SCP+MPPI). 출력은 첫 action과 함께, 계획이 certified(제약을 모두 만족한 KKT point), slack이 남은 채 수렴(근처에 안전한 계획 없음), 미수렴 중 어느 것인지임.

**결과**

- Safety-Gymnasium PointGoal1·PointGoal2(점 로봇이 hazard를 피해 goal에 도달하는 2차원 action 과제)에서 비교함. Lipschitz 상한 1.5 모델, horizon 10, 안전 여유 0.1 m 이상을 묶은 240쌍에서 SCP+MPPI의 위반율은 21%, 같은 시간의 MPPI·CEM은 25%임. 차이 3.8과 3.3퍼센트포인트 모두 95% 신뢰구간이 0을 포함해 통계적으로 유의하지 않음.
- 같은 비교를 6개 모델 전체(720쌍)로 넓히면 MPPI 대비 0.1퍼센트포인트 낮고 CEM 대비 0.7퍼센트포인트 높아 차이가 없음. 위반율 우위는 상한 1.5 모델에 한정됨.
- 시작점의 효과는 분명함. 이전 계획에서 시작한 plain SCP의 위반율은 58%로 SCP+MPPI의 21%보다 높고, 6개 모델 모두에서 덜 안전함.
- PointGoal1에서 horizon을 20과 30으로 늘리면 return 차이가 유의해짐. horizon 20에서 같은 시간의 MPPI·CEM보다 0.65와 0.93, horizon 30에서 1.13과 0.98 높음. 다만 horizon마다 다른 world model을 학습해 horizon 효과와 모델 효과가 섞임.

**한계**

안전은 학습한 모델 안에서만 보장되며, 실제로 에피소드의 5분의 1에서 4분의 1이 위반으로 끝나고 이때 쓸 fallback이 없음. 실험은 2차원 action의 시뮬레이션 과제 2개, 설정별 모델 1개, 설정당 30 에피소드뿐이고 실로봇은 없음. planning에 step당 0.4~0.7초(horizon 10), 2.2~3.6초(긴 horizon)가 들고, barrier 학습에는 관측에 장애물 거리 측정이 있어야 함.

**누리랩 연구와의 연결**

- slack이 남은 채 수렴하면 근처에 안전한 계획이 없다고 알려 주는 신호는 world model 기반 failure detection과 recovery 트리거로 바로 쓸 수 있음. 위반의 93~98%가 barrier를 못 맞춘 계획 뒤에 일어났다는 결과도 같은 근거임.
- sampling planner를 gradient 기반 test-time optimization으로 바꿀 때 network에 Lipschitz·smoothness 제약을 거는 방법과 선형화 오차 상한을 참고할 수 있음. 고차원 action의 manipulation으로 옮겨질지는 검증되지 않음.

*대표 그림: 실험에 쓴 두 과제 PointGoal1과 PointGoal2를 위에서 본 장면임. 빨간 점 로봇, 초록 goal, 보라색 원형 hazard, 하늘색 상자 vase가 보이며 PointGoal2가 hazard와 vase가 더 많음. 측정 결과가 아니라 환경 배치를 보여 주는 그림임.*

---

### 12. MetricHand: Geometry-Aware Flow Matching for 4D Hand Reconstruction in Metric World Space (66점)

[arXiv](https://arxiv.org/abs/2611.21060) · [PDF](https://arxiv.org/pdf/2611.21060) · [alphaXiv](https://www.alphaxiv.org/abs/2611.21060) (요약 있음) · [프로젝트 페이지](https://bieber1205.github.io/MetricHand/)

- **저자**: Yibo Bai, Likui Zhang, Jinglei Zhang, Zhengbin Pang, Xingshen Song, Xiaoqing Yin, Jinsheng Deng
- **분야**: 3D Vision · robotics relevance 8/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> egocentric 영상에서 두 손의 4D 움직임을 metric world 좌표로 복원할 때, 추정 depth를 손 관절별 조건으로 묶어 flow matching의 모든 단계에 넣음. HOT3D에서 world 좌표 절대 관절 오차가 HaWoR의 28.88mm에서 20.58mm로 내림.

**무슨 문제인가**

사람 손 영상을 dexterous manipulation이나 VLA 사전학습의 supervision으로 쓰려면, 손목 위치가 metric 단위의 world 좌표에서 정확하고 움직임이 매끄러워야 함. 기존 방법(HaMeR, WiLoR)은 한 장면을 weak perspective로 보고 손 크기와 crop 크기에서 깊이를 거꾸로 계산함. 카메라 가까이 있는 손은 관절마다 깊이가 달라서, 이 근사가 위치·방향·관절 자세 오차를 함께 만듦. HaWoR, HandFlow 같은 시간 축 방법은 이렇게 치우친 프레임별 추정을 받아 world로 옮기므로, 가려짐이 있으면 오차가 그대로 남음.

**어떻게 푸나**

MetricHand의 입력은 단안 egocentric 영상과 카메라 intrinsics이고, 출력은 두 손 각각의 MANO(손 모양과 관절을 파라미터로 나타내는 표준 손 mesh 모델) 파라미터(world 좌표 손목 위치, 전역 방향, 관절 회전 15개, 모양)임. 먼저 고정된 단안 metric depth 모델과 고정된 DROID-SLAM이 depth와 카메라 궤적을 줌. RGB 특징에 depth 특징을 gated residual로 더하고, Metric Head가 이 특징과 depth 통계로 손의 거친 위치를 viewing ray와 log-depth 좌표에서 고침. 다음으로 거친 MANO 관절 21개를 이미지에 투영해 기준점으로 삼고, 각 관절 주변의 RGB-D 특징과 손·물체 표면 형상을 deformable sampling으로 모음(topology-aware sampling). 학습된 quality score가 믿기 어려운 관측의 비중을 낮추고, FIFO memory queue가 같은 관절의 특징을 이전 window에서 이어 줌. 마지막으로 DiT 블록 6개로 된 flow matching 모델이 Gaussian noise에서 출발해 Euler 3단계로 손 상태를 만들고, 매 단계에서 이 조건들을 cross-attention으로 읽음.

**결과**

- depth를 어디까지 쓰는지 비교한 ablation이 주장을 가장 직접 보여 줌. ARCTIC(두 손으로 물체를 다루는 egocentric 데이터셋)의 카메라 좌표 MPJPE(관절 위치 평균 오차)가 전체 설계에서 17.54mm임. depth를 거친 추정에만 쓰면 38.95mm, flow 첫 단계에만 넣으면 28.95mm임. world 가속도 오차도 4.39, 8.19, 6.28 m/s²로 같은 순서임.
- HOT3D(움직이는 egocentric 카메라로 찍은 손·물체 추적 데이터셋)에서 world 좌표 절대 MPJPE가 HaWoR의 28.88mm에서 20.58mm로, 손목 오차가 14.99mm에서 7.72mm로 내림.
- world 가속도 오차는 가장 강한 baseline과 비교하면 차이가 줄어듦. 카메라 intrinsics를 주는 설정의 ACE-EgoHand 대비로는 HOT3D 4.13에서 3.11, ARCTIC 6.76에서 4.39 m/s²임. HaWoR 대비로는 HOT3D 5.57에서 3.11, ARCTIC 12.28에서 4.39 m/s²임.
- 같은 SLAM 궤적 아래 비교한 결과임. 로봇 학습이나 retargeting 같은 downstream 실험은 없음.

**한계**

world 좌표 정확도는 DROID-SLAM 궤적과 단안 depth 정확도에 그대로 기댐. ARCTIC에서 카메라 좌표 MPJPE는 17.54mm인데 world 절대 MPJPE는 120.86mm로 남음. 저자는 DexYCB, HO3D, HOI4D zero-shot 결과도 기여로 적었지만 본문에서 확인 불가함. 평가는 HOT3D와 ARCTIC 두 데이터셋에 한정되고, 코드 공개 여부도 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- 사람 egocentric 영상에서 손목 궤적과 손가락 자세를 뽑아 VLA나 dexterous manipulation 데이터로 쓰는 파이프라인의 전처리 단계로 바로 비교해 볼 수 있음.
- 관절 기준점 주변의 depth와 물체 표면을 모아 가려진 관절을 복원하는 방식은 object-centric 3D 표현과 hand-object 접촉 추정에 참고가 됨.

*대표 그림: HOT3D와 ARCTIC 입력 프레임 위쪽에, world 좌표로 복원한 손 mesh를 시간 순서로 겹쳐 그린 정성 비교 그림임. 초록 GT에 대해 HaWoR(주황)는 위치가 어긋나 흩어져 있고, MetricHand(파랑)는 GT와 더 가깝게 겹쳐 보임.*

---

### 13. UNITE: Consolidating Embodied VLM Specialists via Shared-Anchor One-Bit Factorization (66점)

[arXiv](https://arxiv.org/abs/2611.20767) · [PDF](https://arxiv.org/pdf/2611.20767) · [alphaXiv](https://www.alphaxiv.org/abs/2611.20767)

- **저자**: Tao Tao, Anke Tang, Enneng Yang, Zhi Hou, Xiaogang Wang, Dacheng Tao
- **분야**: Embodied AI · robotics relevance 8/10 · 1차 스크리닝 72점
- **학회**: IEEE 학술지 계열 양식 (추정) · 근거: IEEE 2단 양식, 33쪽
- **읽은 원문**: PDF 전문

> 같은 Qwen3-VL-8B에서 fine-tuning한 embodied VLM 전문가 4개의 FFN을 MoE expert로 모으고, expert들을 공유 anchor와 1비트 부호 편차로 압축함. 전체 저장 용량은 20.3GB로 전문가 하나(17.5GB)의 1.16배이고, R2R 항법 성공률은 59.6%로 항법 전문가(57.5%)보다 높음.

**무슨 문제인가**

grounding, 공간 추론, 항법, 주행 이해 같은 embodied 능력은 보통 과제별로 VLM을 따로 fine-tuning한 전문가 모델에 나뉘어 있음. 전문가를 따로 두면 저장 용량이 과제 수만큼 늘어 Qwen3-VL-8B 4개에 70.1GB가 듦. 하나의 dense 모델로 static merging하면 과제별 업데이트가 같은 파라미터에서 충돌함. 실제로 6개 static merging 방법 모두 R2R(실내 언어 지시 항법 benchmark) 성공률이 항법 전문가 57.5%보다 낮고 최고가 55.2%임. 전문가 FFN을 expert로 두는 MoE는 충돌을 피하지만 50.2GB로 커짐.

**어떻게 푸나**

UNITE는 세 단계로 동작함. 먼저 각 decoder layer에서 전문가 4개의 FFN(gate, up, down projection)을 그대로 expert로 두고, attention 등 나머지 파라미터는 평균 내어 공유 backbone으로 합침. 다음으로 layer와 weight group마다 각 expert 행렬을 공유 floating-point anchor C와 expert별 행 단위 scale 곱하기 ±1 부호 행렬의 합으로 근사함. anchor를 평균 weight로 고정하지 않고, 부호와 scale을 구하는 closed-form 해와 anchor를 평균으로 다시 구하는 해를 번갈아 10회 적용함. 이 과정은 원본 weight만 쓰고 calibration data나 gradient가 필요 없으며, expert 4개 기준 weight당 약 5비트가 듦. 마지막으로 router를 원본 weight 차이의 SVD 방향으로 초기화한 뒤, backbone과 압축 expert는 고정하고 router 589,824개 파라미터만 55,757개 sample로 supervised 학습함. 입력은 이미지·다중 시점·영상과 텍스트 지시이고, 출력은 각 과제의 텍스트 답임.

**결과**

- 압축 오차: anchor를 함께 최적화하면 평균 anchor로 고정한 경우보다 36개 layer 중앙값 기준 재구성 오차가 20%(gate·up), 22%(down) 줄어듦. 저장량은 같음.
- 압축 손실: 압축 전 MoE(50.2GB) 대비 1비트 MoE(20.3GB)는 22개 benchmark 중 VSI-Bench(영상 기반 공간 추론)를 빼면 어떤 점수도 1.2점 넘게 내리지 않음. 같은 용량의 INT4 양자화보다 22개 중 17개에서 높음.
- static merging 대비: R2R Val-Unseen(실내 언어 지시 항법) 성공률이 59.6%로 최고 static 방법 55.2%보다 높음. Scan2Cap(3D 장면 물체 설명) CIDEr는 102.1로 최고 static 86.4보다 높음. 최고 전문가 점수 대비 평균 유지율은 98.8%로 static 방법들(98.6~98.9%)과 비슷함.
- 손실 사례: VSI-Bench는 압축 전 62.4에서 46.7로 내림. 입력 frame을 4개에서 64개로 늘리면 압축 전 모델은 48.1에서 65.0으로 오르나 1비트 모델은 46.8~48.8에 머묾.

**한계**

모든 평가는 질의응답과 R2R 시뮬레이션 항법이고 실로봇 실험은 없음. router 학습 데이터에 R2R, RefSpatial, MindCube, SAT 등 평가 과제의 학습 데이터가 들어 있어, 항법에서 전문가를 넘은 결과가 router 학습 덕분일 수 있음. 1비트 압축이 영상의 여러 frame 정보 활용을 떨어뜨리는 문제는 router 학습으로 회복되지 않았고, 저자는 해결을 이후 과제로 남김.

**누리랩 연구와의 연결**

- 과제별로 fine-tuning한 VLA나 embodied VLM 여러 개를 한 GPU에 올려 상황에 따라 고르는 구성에 바로 쓸 수 있는 압축 방법임. 다만 action head가 있는 VLA에서는 검증되지 않음.
- 1비트 압축이 영상의 시간 정보 활용을 특히 해친다는 VSI-Bench 분석은, robot memory나 영상 기반 failure detection 모델을 경량화할 때 확인할 항목임.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 왼쪽은 텍스트 지시와 단일 이미지·다중 시점·영상의 세 가지 시각 입력, 가운데는 공간·grounding·항법·주행 전문가 4개, 오른쪽은 이들을 합친 UNITE 모델이 공간 질의응답, 물체 영역 지정, 경로 예측, 주행 궤적 예측을 하는 모습을 보여 줌.*

---

### 14. What Makes a Good Move? Learning to Act from Experience in Visual Worlds (63점)

[arXiv](https://arxiv.org/abs/2611.21065) · [PDF](https://arxiv.org/pdf/2611.21065) · [alphaXiv](https://www.alphaxiv.org/abs/2611.21065) (요약 있음)

- **저자**: Cehao Yang, Ziyi He, Jing Yi, Jian Guo, Hui Xiong
- **분야**: RL · robotics relevance 9/10 · 1차 스크리닝 70점
- **읽은 원문**: PDF 전문

> VLM 게임 agent가 같은 게임 상태에서 가능한 행동을 하나씩 실행해 보고 짧은 rollout 점수 이득을 비교한 표로 RL을 함. 2048 한 게임에서 모은 상태 1,024개로 학습한 Qwen3.5-4B의 GameWorld 34개 게임 평균 진행도(progress)가 11.3%에서 40.5%로 오름.

**무슨 문제인가**

VLM agent가 게임을 하며 쌓은 경험은 trajectory 단위 결과로만 남아, 어느 행동이 좋았는지 알려 주지 않음. 같은 상태에서 다른 행동을 했을 때의 결과는 기록되지 않고, 최종 점수에는 좋은 수와 나쁜 수가 섞여 있음. 또 사전학습 policy로 탐색하면 비슷한 상황만 반복해서 방문해, 학습에 쓸 결정 상태가 좁은 범위에 몰림.

**어떻게 푸나**

LightAct는 탐색 단계와 학습 단계로 나뉨. 먼저 고정된 Qwen3.5가 2048을 플레이한 기록을 짧은 구간으로 자르고, 같은 모델이 구간마다 상황·행동·결과를 요약한 experience entry를 씀. 이 entry들을 다시 하나의 텍스트 skill(예: 판이 안 바뀌면 다른 방향을 시도)로 합쳐 탐색 prompt에 넣음. skill을 넣은 policy로 모은 상태 중 중복을 뺀 최대 1,024개를 결정 root로 저장함. 각 root에서 게임 snapshot을 복원하고 모든 행동을 하나씩 실행한 뒤, 고정된 같은 policy로 최대 10 decision을 이어 감. 환경 점수 이득을 4회 평균해 행동 가치를 추정하고, root 안에서 min-max 정규화해 0~1 reward 표를 만듦. 학습 때는 policy가 root의 화면·history를 입력받아 낸 답을 행동으로 parse하고, 표의 reward(형식이 틀리면 0)로 GRPO 등 RL을 함. 평가 때는 rollout 없이 학습된 policy가 바로 행동함.

**결과**

- GameWorld(브라우저 게임 34개, 과제 170개, 5개 범주) 전체 progress가 2B는 13.3%에서 36.9%로, 4B는 11.3%에서 40.5%로, 9B는 28.8%에서 41.8%로 오름. 2B는 성공률도 3.7%에서 13.9%로 올라 사전학습 9B(10.0%)보다 높음.
- 9B의 전체 progress 41.8%는 GameWorld 논문이 보고한 Gemini-3-Flash-Preview 41.9%와 비슷하나 성공률은 18.4% 대 21.2%로 낮음. 비교 대상은 greedy decoding 1회, LightAct는 temperature 1.0으로 3회 평균이라 조건이 같지 않음.
- 같은 reward 표로 GRPO, REINFORCE++, DAPO를 쓴 9개 설정 모두 전체 progress가 10.8~29.2퍼센트포인트 오름.
- skill을 넣고 탐색하면 root를 모은 2048 게임의 평균 점수가 186.6에서 280.2로 오름. 이 root로 학습한 2B의 progress는 GRPO에서 32.98%에서 36.90%로 오르나, REINFORCE++에서는 34.60%에서 34.55%로 차이가 없음.

**한계**

rollout reward를 즉시 점수 이득이나 trajectory 단위 reward와 직접 비교한 ablation이 없어, 행동별 rollout 비교 자체의 기여는 2048 사례 그림으로만 보여 줌. 방법은 게임 snapshot 복원과 환경 점수 접근을 전제로 하며, 연속 행동 공간과 긴 horizon 과제는 저자도 다루지 못했다고 밝힘. source 게임은 주로 2048 하나(일부 Tetris)이고 2048도 평가 게임에 포함되며, 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- 상태를 복원하고 행동마다 고정 policy로 짧게 이어 가 본 결과를 reward 표로 만드는 방식은, 시뮬레이터에서 VLA의 행동 후보를 비교해 counterfactual supervision을 만드는 연구의 비교 대상이 됨.
- 실패 패턴을 텍스트 skill로 요약해 탐색을 넓히는 부분은 language feedback 기반 learning, robot memory와 이어지나, 연속 제어와 실로봇 검증은 없음.

*대표 그림: 2048에서 LightAct-2B가 내린 한 결정을 보여 주는 사례 그림임. step 45와 46의 판이 같은 상황에서 모델이 판이 안 바뀐다고 설명하고 move_right를 골라, 2+2·8+8·2+2가 합쳐지며 점수가 204에서 228(+24)로 오름.*

---

### 15. When Backdoors Can Be Switched Off: Suppression-Aware Backdoor Attacks on Vision-Language-Action Models (52점)

[arXiv](https://arxiv.org/abs/2611.19774) · [PDF](https://arxiv.org/pdf/2611.19774) · [alphaXiv](https://www.alphaxiv.org/abs/2611.19774)

- **저자**: Nur Afsa Syeda, Mohamed Elmahallawy
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 70점
- **학회**: ACL 계열 양식 (추정) · 근거: A4 용지, 2단 구성
- **읽은 원문**: PDF 전문

> VLA policy의 backdoor를 언어 token 하나로 켜고 끌 수 있게 만든 data poisoning 공격을 SmolVLA와 OpenVLA에서 시험함. 같은 물리 trigger 아래에서 [RESTORE] token으로 바꾸면 SO-100의 네 조건 모두에서 fail action 일치율이 61~69%에서 0%로 내려감.

**무슨 문제인가**

VLA policy는 demonstration으로 fine-tuning되므로 학습 데이터 일부를 오염시키면 backdoor를 심을 수 있음. 기존 VLA backdoor(State Backdoor, BadVLA 등)는 대부분 trigger 하나가 보이면 항상 악성 행동을 냄. 이렇게 무조건 켜지는 backdoor는 같은 입력을 반복해 넣거나 action 분포를 보면 이상 행동이 드러나기 쉬움. 저자는 여러 modality가 동시에 맞아야 켜지고, 물리 trigger가 남아 있어도 공격자가 끌 수 있는 backdoor가 가능한지를 질문으로 삼음.

**어떻게 푸나**

모든 공격은 학습 demonstration의 20%를 오염시키는 training-time data poisoning이고, 모델 구조와 추론 과정은 건드리지 않음. 공통 trigger는 episode 첫 관절 상태에 작은 offset을 더한 initial-pose state trigger이며, offset은 PGA(projected gradient ascent) 기반 최적화로 찾음. Attack A(Cross-Modal Trigger)는 state trigger와 영상 trigger가 함께 있을 때만 fail action을 내게 학습함. 영상 trigger는 seed가 다른 8×8 checkerboard noise 두 개를 더한 것이고, 한쪽만 있거나 state만 있는 frame에는 원래 action label을 붙여 단독으로는 켜지지 않게 함. Attack B(Self-Suppressing Trigger)는 같은 state trigger에 instruction 끝 [DISRUPT]를 붙이면 fail action, [RESTORE]를 붙이면 원래 action을 label로 줌. Attack C(Multi-Trigger)는 state, 영상, [DISRUPT] 세 조건이 모두 맞아야 켜지고, 여섯 가지 부분 조합과 [RESTORE]에는 원래 action을 줌. 입력은 관절 상태, 카메라 영상, instruction이고 출력은 50 step action chunk임.

**결과**

- SmolVLA를 SO-100 데이터셋 두 개(LeRobot의 6자유도 팔 단일 과제 데이터: Cube Sorting, Pick and Place)로 학습하고 held-out frame 100개의 첫 step 예측으로 잼. trigger가 모두 있을 때 fail action을 낸 비율(primary ASR, 공격 성공률)은 Attack B와 C에서 63~71%이고 clean frame 정확도는 100%임. [RESTORE]를 붙였을 때 clean 예측과 가까운 비율은 86~95%임.
- Isolation Forest(action 예측의 이상치 검출) 검출률은 State Backdoor 96~98%에서 Attack B 1~9%, Attack C 3~18%로 내려감. 다만 같은 입력을 두 번 넣는 repetition 검사와 action 분포의 KL 검사(ADS)는 SO-100에서 A, B, C를 모두 검출함.
- OpenVLA(7B)를 LIBERO(시뮬레이션 조작 suite 4개)에 LoRA로 fine-tuning해도 [RESTORE] 조건의 fail 일치율은 3% 이하로 유지됨. primary ASR은 24.2~54.8%로 SO-100보다 낮고, 여기서는 state trigger를 prompt 문자열로 넣음.
- 영상 trigger를 두 조각으로 나누지 않고 한 번에 넣으면 Attack A의 Isolation Forest 검출률이 11%에서 100%로 오르고, 영상만 있을 때 ASR이 0%에서 12%로 오름(Cube Sorting).

**한계**

모든 정량 결과는 저장된 frame에 대한 첫 step 또는 chunk 예측 일치로 잰 것이고, closed-loop rollout으로 실제 과제를 망가뜨렸는지는 보이지 않음. DOFBOT Pro 실로봇 결과는 학습된 poisoned policy가 아니라 손으로 짠 동작을 보여 주는 시연이며 정량 평가는 하지 않음. 실험한 방어는 STRIP, repetition, ADS, Isolation Forest뿐이고, SO-100에서는 repetition과 ADS에 검출되므로 '탐지 회피'라는 주장은 Isolation Forest와 STRIP에 한정됨.

**누리랩 연구와의 연결**

- VLA를 실제로 배포할 때의 안전 문제를 다룸. 학습 데이터 출처를 검증하기 어려운 상황에서 failure detection 모듈이 언어 조건부 이상 행동을 잡을 수 있는지 시험하는 사례로 쓸 수 있음.
- 같은 관측에서 instruction token만 바꿔 행동을 비교하는 평가는 VLA의 language grounding을 counterfactual 방식으로 점검하는 실험 설계와 이어짐.

*대표 그림: DOFBOT Pro 데스크톱 로봇 팔의 받침부와 옆 모니터를 찍은 사진임. 모니터에는 작업대 위 작은 물체를 내려다본 카메라 화면과 터미널 출력이 보이며, 측정 결과를 담은 그림은 아님.*

---

## 오늘의 흐름

- **고정된 policy를 재학습 없이 실행 시점에 고침**: 세 편은 VLA나 diffusion policy를 다시 학습하지 않고 실행 시점에 후보 행동을 고르거나 입력 특징을 더함. 한 편은 VLA 가중치와 원래 VLM 가중치를 섞어 잃은 언어 능력을 되살림. [PlanDiv](https://arxiv.org/abs/2611.20010), [Certify, Then Select](https://arxiv.org/abs/2611.19047), [FAVR](https://arxiv.org/abs/2611.20971), [Bring Back Language to Actions](https://arxiv.org/abs/2611.18891)
- **world model을 rollout 생성기가 아니라 보조 신호와 검증 도구로 씀**: 한 편은 미래 장면 전체 대신 현재와 미래 feature의 차이만 예측하게 함. 다른 두 편은 상상한 latent를 point cloud로 되돌려 확인하거나, 위험 상태를 가르는 control barrier function을 학습해 planning 제약으로 넣음. [ResWAM](https://arxiv.org/abs/2611.19559), [JEPA4R](https://arxiv.org/abs/2611.19771), [Successive Convexification in Learned World Models](https://arxiv.org/abs/2611.19466)
- **기록해 둔 관측을 나중에 다시 꺼내 쓰는 memory**: 어떤 요청이 올지 모르는 채로 기록한 memory에서 요청마다 필요한 과거 장면을 고르는 학습 방법이 나옴. 같은 방에 다시 들어왔을 때 multimodal LLM(MLLM)이 그 방을 알아보는지 재는 benchmark도 나왔고, 가장 강한 모델의 정확도가 52.2%로 사람의 90.1%보다 낮음. [ReuseMem](https://arxiv.org/abs/2611.21115), [Lost in the Hallway](https://arxiv.org/abs/2611.21485)
- **손과 접촉 정보**: 손끝 촉각 이력으로 숨은 마찰과 기구 저항을 추정해 humanoid 문 열기를 시뮬레이션에서 실로봇으로 옮긴 연구와, egocentric 영상에서 두 손 움직임을 metric 좌표로 복원하는 연구가 있음. [TMA](https://arxiv.org/abs/2611.18976), [MetricHand](https://arxiv.org/abs/2611.21060)

## 해볼 만한 연구

### 다양한 후보 생성과 제약 인증을 묶은 test-time steering
- 질문: 후보 action chunk를 latent plan마다 하나씩 만들면, 실행 중 들어온 제약을 통과하는 후보가 하나도 없는 경우가 줄어드는지 밝힘.
- 첫 실험: robomimic Can(깡통을 집어 상자에 넣는 시뮬레이션 과제)의 제약 5종에서 같은 diffusion policy로 i.i.d. 재샘플링 후보 N개와 plan별 후보 N개를 만듦. 같은 인증 필터와 value 선택기를 붙여, 제약과 과제를 함께 만족한 비율과 통과 후보가 0개인 비율을 비교함.
- 가장 가까운 연구: [Certify, Then Select](https://arxiv.org/abs/2611.19047)는 후보를 i.i.d.로 뽑고, [PlanDiv](https://arxiv.org/abs/2611.20010)는 제약 없이 log-probability로만 후보를 고름.

### world model 예측 오차를 실행 중 failure detection 신호로 쓰기
- 질문: ResWAM처럼 feature 변화량을 예측하는 world model에서 예측값과 실제값의 차이가 실패보다 몇 step 앞서 커지는지 밝힘.
- 첫 실험: RoboTwin 2.0(양팔 조작 시뮬레이션 benchmark) rollout에서 step마다 예측한 feature 변화량과 실제 DINOv3 feature 변화량의 차이를 기록함. 실패 episode를 가르는 AUROC를 action 분산 기반 detector와 비교함.
- 가장 가까운 연구: [ResWAM](https://arxiv.org/abs/2611.19559)은 residual을 학습 보조 신호로만 쓰고, [JEPA4R](https://arxiv.org/abs/2611.19771)은 틀린 action에서 decode 오차가 커짐을 보였지만 실행 중 감지는 시험하지 않음.

### 요청을 모르고 기록한 memory로 failure recovery 하기
- 질문: 어떤 요청이 올지 모르는 채로 기록한 memory에서 물체의 원래 위치 같은 recovery용 과거 관측을 꺼낼 수 있는지 밝힘.
- 첫 실험: ReuseMem의 시뮬레이션 과제에서 물체를 옮긴 뒤 원래 자리로 되돌리라는 요청을 더함. 요청에 맞는 과거 장면을 고르도록 학습된 ReuseMem의 Reader, 균등 선택, 최근 프레임만 쓰는 memory의 성공률을 비교함.
- 가장 가까운 연구: [ReuseMem](https://arxiv.org/abs/2611.21115)은 recovery 요청을 다루지 않고, [Lost in the Hallway](https://arxiv.org/abs/2611.21485)는 MLLM의 방 재식별만 재고 행동은 다루지 않음.

## 꼭 읽을 논문

- [PlanDiv](https://arxiv.org/abs/2611.20010): 같은 후보 수에서 재샘플링보다 plan 다양화가 CALVIN(언어 지시 조작 과제를 연달아 수행하는 시뮬레이션 benchmark)의 5개 과제 연속 성공률을 더 올림. VLA test-time scaling의 후보 생성 쪽 baseline으로 쓸 수 있음.
- [Certify, Then Select](https://arxiv.org/abs/2611.19047): 고정된 diffusion policy에 실행 중 제약을 거는 방법임. 제약 통과와 과제 성공을 함께 재는 평가 방식도 가져다 쓸 수 있음.
- [ResWAM](https://arxiv.org/abs/2611.19559): world model을 VLA 학습의 보조 신호로 쓸 때 미래 전체보다 변화량을 예측하는 편이 나음을 같은 계산량에서 보임.
- [TMA](https://arxiv.org/abs/2611.18976): 실제 문손잡이 40회 시도에서 촉각 기반 적응 policy TMA는 27회, 촉각 없는 기존 적응 방법 RMA(Rapid Motor Adaptation)는 0회 성공함. tactile 입력 표현 설계의 비교 기준이 됨.
- [ReuseMem](https://arxiv.org/abs/2611.21115): 한 번 기록한 memory를 여러 후속 요청에 재사용하는 robot memory 평가 틀을 제시함.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (942편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2611.20971'>FAVR: Flow-Aware Visual Residual Alignment for Vision-Language-Action Policies</a></td><td>74</td><td>9</td><td>VLA</td><td>사전학습 video 표현의 flow 정보를 VLA policy에 residual 정렬로 통합해 조작에 시간 정보를 주입하는 직접 관련 연구임</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2611.21485'>Lost in the Hallway: Benchmarking Persistent Spatial Memory Across Revisits</a></td><td>74</td><td>8</td><td>Embodied AI</td><td>재방문 공간 기억을 보는 ReSpaceBench를 제안하고 32개 모델이 50.5%로 사람 90.1%에 크게 못 미침을 보였으며 agent의 방 연관 오류를 분석함</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2611.19466'>Successive Convexification in Learned World Models for Safe Offline Planning</a></td><td>74</td><td>8</td><td>World Model</td><td>학습된 world model latent에서 control barrier function 제약을 둔 successive convex program으로 안전 오프라인 planning을 하고 KKT 가능성까지 보고함</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2611.19815'>Conditional Optimal Transport and Triangular Maps for Imitation Learning</a></td><td>74</td><td>8</td><td>Manipulation</td><td>imitation learning을 triangular transport 조건부 샘플링으로 통일하고 reference를 demonstration action chunk 분포로 둠. Push-T와 Square에서 Diffusion Policy와 경쟁하며 0.23M 파라미터 1회 평가 policy도 가능함. 실로봇은 없음</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2611.18976'>TMA: Sim-to-Real Forceful Humanoid Manipulation via Tactile-Driven Motor Adaptation</a></td><td>72</td><td>9</td><td>Manipulation</td><td>촉각 기반 motor adaptation으로 humanoid의 힘 주는 조작을 sim-to-real함. tactile과 humanoid manipulation 결합이 강점임</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2611.19559'>ResWAM: Learning What Changes, Not What Stays, for World-Action Models</a></td><td>72</td><td>9</td><td>World Model</td><td>world-action model이 변하는 부분만 residual로 예측하게 함. 변화량 학습이라는 formulation이 신선하며 VLA 주제와 직결됨</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2611.19771'>JEPA4R: Embodied JEPA World Models with 4D Point Planning</a></td><td>72</td><td>9</td><td>World Model</td><td>JEPA world model에 4D point 기반 planning을 결합함. 2D 한계를 3D/4D 표현으로 보완하는 방향이 world model 주제와 직결됨</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2611.20010'>PlanDiv: Test-Time Scaling with Latent Plans for Vision-Language-Action Models</a></td><td>72</td><td>9</td><td>VLA</td><td>VLA test-time scaling의 수확 체감을 latent plan 다양성으로 개선함. inference-time planning 주제와 직결됨</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2611.21115'>ReuseMem: One Memory, Multiple Goals in Robot Manipulation</a></td><td>72</td><td>9</td><td>Manipulation</td><td>하나의 시각 memory를 이후 여러 조작 목표에 재사용함. goal-independent 기록과 검색 supervision이 robot memory 주제와 직결됨. 실로봇은 시나리오 2개뿐임</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2611.21060'>MetricHand: Geometry-Aware Flow Matching for 4D Hand Reconstruction in Metric World Space</a></td><td>72</td><td>8</td><td>Manipulation</td><td>egocentric 손 동작을 metric world space 4D로 복원해 dexterous manipulation과 VLA 사전학습 supervision으로 직접 연결됨</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2611.20767'>UNITE: Consolidating Embodied VLM Specialists via Shared-Anchor One-Bit Factorization</a></td><td>72</td><td>8</td><td>Embodied AI</td><td>embodied VLM 전문가 4개(Qwen3-VL-8B)를 shared-anchor one-bit factorization MoE로 합쳐 단일 dense 모델의 1.16배 저장으로 줄임. 3D 장면 이해 5개와 R2R 항법에서 원본 전문가를 넘으나 VSI-Bench는 열화됨</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2611.18891'>Bring Back Language to Actions: Restoring VLM capabilities in VLA Models via Parameter Merging</a></td><td>72</td><td>8</td><td>VLA</td><td>VLA fine-tuning으로 잃은 VLM 능력을 task vector SVD 성분별 계수 학습으로 복원하는 parameter merging을 제안함. 재학습 없이 action과 vision-language 능력을 함께 유지하는 실용적 접근이나 평가 범위가 초록상 제한적임</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2611.19774'>When Backdoors Can Be Switched Off: Suppression-Aware Backdoor Attacks on Vision-Language-Action Models</a></td><td>70</td><td>9</td><td>VLA</td><td>VLA에 대한 끌 수 있는 backdoor 공격으로 VLA 안전성 취약점을 다루는 새 문제 설정임</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2611.21065'>What Makes a Good Move? Learning to Act from Experience in Visual Worlds</a></td><td>70</td><td>9</td><td>RL</td><td>시각 환경에서 경험으로부터 행동 단위 가치를 학습하는 policy 학습 formulation으로 RL과 직접 연결됨</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2611.19047'>Certify, Then Select: Viability-Aware Runtime Steering of Frozen Diffusion Policies</a></td><td>70</td><td>8</td><td>Manipulation</td><td>고정 diffusion policy를 runtime에 viability 인증 후 선택해 제약을 만족시킴. inference-time steering과 안전성 결합이 좋음</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2611.20460'>Stochastic Self-Distillation for Flow-Based Vision-Language-Action Models</a></td><td>68</td><td>9</td><td>VLA</td><td>flow 기반 VLA의 on-policy RL fine-tuning을 stochastic self-distillation으로 안정화함. RL로 VLA 개선 주제와 직결됨</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2611.20718'>TaF-Foundation: Wrench-Grounded Cross-Sensor Tactile Representations</a></td><td>68</td><td>9</td><td>Tactile</td><td>wrench에 grounded된 cross-sensor 촉각 표현을 학습함. 센서 간 전이가 tactile 주제의 핵심 문제임</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2611.18734'>Is It Still There? Place-Registered Verification Makes VLMs Reliable Scene-Change Detectors</a></td><td>68</td><td>8</td><td>Embodied AI</td><td>로봇 재방문 시 장면 변화 검출에서 VLM 오류를 place-registered 검증으로 줄이는 실용적 문제 설정임</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2611.19901'>Remember, Replay, Adapt: Learning from Past Experience in Online Vision-and-Language Navigation</a></td><td>68</td><td>8</td><td>Navigation</td><td>online VLN에서 과거 피드백을 기억하고 replay로 적응시켜 language feedback과 memory 학습에 해당함</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2611.21104'>GRAZE: Text-Free Grasp Synthesis for Unseen Objects from Human Gaze</a></td><td>68</td><td>8</td><td>Manipulation</td><td>사람 시선으로 unseen 물체 텍스트 없는 grasp 합성이라는 새 조건 formulation으로 manipulation 데이터와 연결됨</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2611.19034'>Refinement vs. Replanning: Inference Compute Allocation in Robot Policies</a></td><td>68</td><td>8</td><td>VLA</td><td>고정된 chunked policy의 inference compute를 refinement와 replanning으로 배분하는 문제를 분석함. test-time compute 관점이 유용함</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2611.20244'>Right Goal, Wrong Body: Re-grounding Frozen VLAs under Actuation Shift</a></td><td>68</td><td>8</td><td>VLA</td><td>actuation 변화 시 고정 VLA를 re-grounding함. 실패 원인 진단과 적응 측면에서 실용적임</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2611.21517'>Lazy-MOSAIC: Accelerating Skill-Centric Manipulation Planning with Learned Skill-Effect World Models</a></td><td>68</td><td>8</td><td>TAMP</td><td>학습된 skill-effect world model로 skill-centric 조작 planning을 가속함. 시뮬레이터 질의를 줄이면서 성공률 유지하는 점이 좋음. 실로봇 시연 있음</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2611.20433'>ReScene: Incremental Scene Chronology from Sparse Revisits</a></td><td>68</td><td>7</td><td>3D Vision</td><td>희소 재방문에서 시간별 장면 변화를 증분 복원하는 scene chronology로 장기 지도와 변화 추적에 직접 연결됨</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2611.21479'>LynnReal-Hand: Unlocking World Interaction with Hand Control</a></td><td>68</td><td>6</td><td>World Model</td><td>손 제어 interactive video world model을 100K 상호작용 clip, few-step distillation, 경량 VAE로 실시간 구동하고 FVD와 MANO Dice를 보임</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2611.19796'>The Sense Paradigm for World Models</a></td><td>68</td><td>6</td><td>World Model</td><td>방향 거리 기반 단일 cross-entropy loss로 latent world model의 collapse를 막고 비가역 전이를 AUC 0.95-1.00으로 탐지함. TwoRoom planning 100% 성공하나 단순 환경 위주임</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2611.20202'>DAPPT: Domain-Aware Policies from Procedural Trajectories for Sim-to-Real Dexterous Tool Use</a></td><td>66</td><td>9</td><td>Manipulation</td><td>절차적 궤적으로 sim-to-real dexterous tool use를 달성함. rigid-body 한계 밖 과제를 다루는 점이 좋음</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2611.20939'>TacBridge: Learning Unified Tactile Representations through Cross-Sensor Correspondence</a></td><td>66</td><td>9</td><td>Tactile</td><td>cross-sensor 대응으로 통합 촉각 표현을 학습함. 센서 전이 주제이나 TaF류와 유사한 방향임</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2611.19183'>WA-JEPA: Goal-Aware Predictive Feedback Action Refinement for a World-Action Model</a></td><td>66</td><td>8</td><td>World Model</td><td>JEPA world-action model에서 후보 탐색 없이 goal-aware feedback으로 행동을 정제해 planning 비용을 줄이는 방향임</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2611.21033'>POKE: Probe Offline, Keep Efficiently for Vision-Language-Action Models</a></td><td>66</td><td>8</td><td>VLA</td><td>VLA visual token pruning을 attention 점수 대신 offline probing 영향으로 선택해 VLA 추론 효율을 다룸</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2611.19904'>DiffWAM: Learning World Action Model from Consecutive Visual Difference</a></td><td>66</td><td>8</td><td>World Model</td><td>연속 프레임 차이로 world action model을 학습함. 변화 표현이라는 관점이 새롭고 WAM 주제와 맞으나 ResWAM과 유사한 방향임</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2611.20465'>ReRead: Wrong Predictions, Useful Representations - Correcting Frozen Robot Policies by Re-reading Their Own Representations</a></td><td>66</td><td>8</td><td>VLA</td><td>고정 policy의 실패를 자체 표현을 다시 읽어 교정함. backbone 재학습 없이 failure 교정하는 점이 흥미로움</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2611.21143'>WinDEX: Metric 3D Hand Motion Reconstruction in the Wild for Dexterous Teleoperation and Policy Learning</a></td><td>66</td><td>8</td><td>Manipulation</td><td>야외 영상에서 metric 3D 손 모션을 복원해 dexterous 원격조작과 policy 학습에 씀. 인간 데이터 확보 측면에서 유용함</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2611.21258'>ThinkWAM: Rethinking Latent Futures for Action Refinement</a></td><td>66</td><td>8</td><td>World Model</td><td>WAM의 latent future로 action을 refinement함. 초기 action의 오류를 미래 예측으로 고치는 접근이 test-time 개선과 맞음</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2611.19803'>Pros4D: Modeling Evolving 4D Worlds in Latent Space for Dynamic Spatial Reasoning</a></td><td>66</td><td>7</td><td>Embodied AI</td><td>단안 영상에서 진화하는 4D 세계를 latent로 모델링해 VLM의 동적 공간 추론을 높이는 embodied 관련 연구임</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2611.21302'>Déjà-Events: Multi-view 3D Geometry with Event Cameras via Sparsity-Aware Adaptive Gating</a></td><td>66</td><td>6</td><td>3D Vision</td><td>RGB feed-forward 3D 모델을 event 카메라 모델로 distillation하고 sparsity-aware gating을 넣어 DSEC에서 오차를 절반으로 줄임</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2611.19332'>NI-ACT: A Neural Intent Interface for Brain-Embodied Manipulation</a></td><td>66</td><td>6</td><td>Embodied AI</td><td>피질 신경 신호를 task-level intent token으로 받아 visuomotor policy를 조건화하는 BCI 조작 프레임워크를 제안함, 신경 intent 교체에 따른 counterfactual 파지 실험이 흥미로우나 1~2개체 기록 기반이라 일반화 근거는 약함</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2611.20481'>Lift, See, Act: Hierarchical Robot Policy Pretraining with 3D Foundation Models</a></td><td>65</td><td>8</td><td>VLA</td><td>3D foundation model로 인간 영상에서 계층적 robot policy를 pretrain함. action label 부재 문제를 3D로 해결하나 검증 범위는 확인 필요함</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2611.21057'>WiTac: Wrist-Informed Tactile Representations for Contact-Rich Manipulation</a></td><td>64</td><td>9</td><td>Tactile</td><td>손목 정보와 결합한 촉각 표현으로 contact-rich 조작을 개선함. 촉각과 자세 통합이 합리적임</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2611.19952'>CRAFT: A Robot-Agent Harness with Scope-Aware Adaptation</a></td><td>64</td><td>8</td><td>Embodied AI</td><td>사용자 거절 교정이 어느 범위에 적용되는지 판단하는 scope-aware adaptation harness임. language feedback 학습과 맞음</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2611.19822'>The Flip Test: Video World Models Fail to Learn the World State</a></td><td>64</td><td>7</td><td>World Model</td><td>video world model이 world state를 못 배운다는 counterfactual flip test로 진단 가치가 큼</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2611.19380'>Test-Time Constraint-Aware Diffusion Predictive Control</a></td><td>64</td><td>7</td><td>Planning</td><td>사전학습 diffusion 제어기를 재학습 없이 새 안전 제약에 맞추는 test-time exponential tilting과 MALA 샘플링을 제안함</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2611.18919'>Correcting Persistent Failures in Point-Cloud Grasping Policies using Human Demonstrations in Virtual Reality</a></td><td>62</td><td>8</td><td>Manipulation</td><td>point cloud grasping policy의 지속 실패를 VR 시연으로 교정함. failure recovery 주제와 맞으나 grasping에 한정됨</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2611.19196'>Ego2Sim2Humanoid: Agentic Real-to-Sim for Learning Loco-Manipulation VLAs without Robot Demonstrations</a></td><td>62</td><td>8</td><td>VLA</td><td>egocentric 영상에서 agentic real-to-sim으로 로봇 시연 없이 humanoid loco-manipulation VLA를 학습함. 데이터 확보 관점에서 흥미로움</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2611.19274'>HospitalBench: Diagnosing Where and Why Embodied Agents Fail on Long Hospital Task Chains</a></td><td>62</td><td>8</td><td>Embodied AI</td><td>병원 장기 과제에서 embodied agent의 실패 위치와 원인을 진단하는 benchmark임. failure diagnosis 주제와 맞으나 benchmark 중심임</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2611.19324'>MARS: Dynamic Routing of Reinforcement-Learned Atomic Skills for Multi-Stage Robotic Manipulation</a></td><td>62</td><td>8</td><td>Manipulation</td><td>RL로 학습한 atomic skill을 동적으로 routing해 multi-stage 조작을 수행함. skill chaining과 VLA 정밀도 보완 주제와 맞음</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2611.19709'>Cache or Denoise Less? Residual Reuse in a Flow-Matching World Action Model</a></td><td>62</td><td>8</td><td>World Model</td><td>flow-matching world action model에서 residual 재사용과 denoise 감소를 비교함. 효율 추론 분석이 실용적임</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2611.20137'>Cleanly-DINO: Efficiently Learning Visual Task Spaces for Robotics</a></td><td>62</td><td>8</td><td>Manipulation</td><td>DINO 특징에서 과제 관련 변화를 담는 visual task space를 효율적으로 학습함. 소수 시연 조작과 표현 학습 측면이 맞음</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2611.20676'>Learning and Verifying Progress: Closed-Loop Agentic Planning with Progress-Enhanced Execution for Long-Horizon Vision-Language Navigation</a></td><td>62</td><td>8</td><td>Navigation</td><td>장기 VLN에서 진행도를 학습해 검증하는 closed-loop agentic planning임. 오류 복구 측면이 맞음</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2611.20741'>Robotic Reward Models in the Foundation-Model Era</a></td><td>62</td><td>8</td><td>Robot Learning</td><td>robotic reward model의 출력 유형을 정리하는 survey 성격임. 개념 정리는 유용하나 새 방법은 없음</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2611.21099'>ForceHarness: Turning Force into Action and Physics for Frozen Frontier Models</a></td><td>62</td><td>8</td><td>Manipulation</td><td>frontier 모델에 force 정보를 action과 physics로 넣어 줌. zero-shot 조작에 접촉력을 도입하는 관점이 맞음</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2611.20011'>ReactBench-AD: Do Driving VLAs and World-Action Models React to Imminent Hazards in Their Path?</a></td><td>62</td><td>7</td><td>VLA</td><td>driving VLA와 world-action model이 임박한 위험에 반응하는지 진단하는 벤치마크로 failure 분석 성격임</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2611.18979'>Probing Where Surprise Happens: Localized Violation-of-Expectation Evaluation of Video World Models</a></td><td>62</td><td>6</td><td>World Model</td><td>video world model 직관 물리를 위치 국소화한 VOE로 평가해 world model 진단에 유용함</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2611.19621'>Toward Planning Representations That Separate Task Structure from Visual Content</a></td><td>62</td><td>6</td><td>Representation</td><td>planning 표현에서 task 구조와 시각 내용을 분리해 representation learning으로 planning에 접근함</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2611.19825'>Foundation Pareto Flow Policy for Multi-Objective Reinforcement Learning</a></td><td>62</td><td>6</td><td>RL</td><td>연속 제어 offline MORL용 diffusion transformer flow policy를 pre/mid/post-training 3단계로 학습해 D4MORL에서 SOTA를 보고함. 시뮬레이션 locomotion 위주이고 training recipe 성격임</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2611.19179'>Isolating Perception for Multi-View Planning under Occlusion-Induced Partial Observability</a></td><td>62</td><td>6</td><td>Embodied AI</td><td>가림이 있는 multi-view planning에서 perception을 분리해 VLM의 depth 모호성을 다룸. 공간 추론과 active perception 주제와 연결됨</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2611.18578'>VidEngram: Agentic Long-Term Video Understanding via Structured Hierarchical Memory</a></td><td>62</td><td>5</td><td>Video</td><td>긴 영상 질의응답용 계층 memory 재사용 구조로 agent memory와 연결되나 로봇 실험 없음</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2611.21253'>QuantileGS: Quantile-Based Conformal Bounds on RGB Rendering Errors for Novel View Synthesis with 3D Gaussian Splatting</a></td><td>62</td><td>5</td><td>3D Vision</td><td>3DGS 렌더링 오차에 conformal 보정으로 커버리지를 보장하는 상한을 제안하고 active view selection, SLAM 응용을 보임</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2611.20314'>NF-VLA: A Normalizing-Flow Baseline for Vision-Language-Action Learning</a></td><td>60</td><td>8</td><td>VLA</td><td>normalizing flow 기반 VLA baseline을 제시함. 단일 likelihood 목적 학습이 흥미로우나 baseline 성격임</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2611.20792'>TRR: A Thermal Interaction Engine for Robot Simulation and RGBT Data Generation</a></td><td>60</td><td>7</td><td>Manipulation</td><td>로봇 행동이 남기는 열 상태를 모델링하는 thermal 시뮬레이션과 RGBT 데이터 생성 엔진으로 새 센서 modality 제공임</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2611.18702'>Robustness as a Transferable Skill: Cross-Task Adversarial Defense for Vision-Language-Action Policies</a></td><td>60</td><td>7</td><td>VLA</td><td>VLA의 adversarial 방어를 과제 간 전이시키는 문제를 다룸. 실용적 주제이나 방법은 incremental일 수 있음</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2611.19251'>Physics-Informed Causal Reasoning for Nonstationary Robot Dynamics</a></td><td>60</td><td>7</td><td>Robotics</td><td>비정상 로봇 dynamics에서 physics-informed causal reasoning을 함. causal reasoning 주제와 맞음</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2611.19979'>Practice Is Not Free: Measuring the Embodied Cost of Reset-Free Robot Practice</a></td><td>60</td><td>7</td><td>RL</td><td>reset-free 로봇 practice의 시간, 마모, 개입 비용을 측정함. 학습 스케줄러 평가 관점이 유용함</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2611.21383'>The Mask Is Not the Object: Volumetric Supervision for 3D Gaussian Segmentation</a></td><td>60</td><td>5</td><td>3D Vision</td><td>3DGS 분할이 렌더링 마스크만 감독해 가려진 Gaussian을 놓치는 문제를 깊이 군집 기반 부피 감독 VODA로 해결하고 Removal-3D를 제안함</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2611.20278'>Visual Marking as a Native Reasoning Capability for Multimodal LLMs</a></td><td>60</td><td>4</td><td>Multimodal</td><td>MLLM이 시각 marking을 native reasoning으로 쓰는 방식으로 중간 공간 상태 유지에 새 formulation을 제시함</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2611.19998'>MoViC: Real-Time Humanoid Whole-Body Control from Monocular Video Streams</a></td><td>58</td><td>8</td><td>Humanoid</td><td>monocular 영상 스트림에서 실시간 humanoid whole-body 제어를 수행함. 통합 시스템이며 tracker 개선 위주임</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2611.20273'>DexFormer 2.0: Towards a Cross-Embodiment Foundation Policy for Dexterous Grasping</a></td><td>58</td><td>8</td><td>Manipulation</td><td>cross-embodiment dexterous grasping foundation policy임. 주제는 맞으나 scale-up 성격이 있음</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2611.20631'>Instructions Before Actions: Prospective and Retrospective Language Supervision for Driving Vision-Language-Action Data</a></td><td>58</td><td>7</td><td>VLA</td><td>driving VLA가 지시를 실제 따르는지 prospective/retrospective language supervision으로 학습해 language 기반 learning에 해당함</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2611.19081'>RoboCoEvo: Expanding Robot Capabilities through Agent-Policy Co-Evolution</a></td><td>58</td><td>7</td><td>Embodied AI</td><td>MLLM agent와 robot foundation model을 co-evolution시켜 능력을 확장함. 아이디어는 흥미로우나 검증 범위 불확실함</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2611.19287'>VLN-Flash: Parallel Action Decoding with Adaptive Execution for Vision-and-Language Navigation</a></td><td>58</td><td>7</td><td>Navigation</td><td>VLN policy의 action을 병렬 디코딩하고 실행을 적응시켜 지연을 줄임. 효율 개선이며 novelty는 중간임</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2611.19688'>Physics-Grounded STL Monitoring from Image Observations</a></td><td>58</td><td>7</td><td>Manipulation</td><td>이미지 관측에서 물리 기반 STL monitoring을 수행함. failure detection과 연결 가능하나 범위 제한적임</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2611.19912'>AgenticJevNav: Agentic Object Search and Navigation via Event-Driven Verification</a></td><td>58</td><td>7</td><td>Navigation</td><td>이벤트 기반 검증으로 agentic 물체 탐색 navigation을 수행함. 실행 실패 대응 관점이 있으나 시스템 통합 성격임</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2611.19153'>ImpedanceMimic: Learned Impedance as Action Space for Force-Accurate Motion Imitation</a></td><td>58</td><td>6</td><td>Control</td><td>학습된 impedance를 action space로 써 힘 정확한 motion imitation을 함. 접촉력 복원 문제 설정이 적절함</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2611.18761'>Frame First, Decode Once: Object-Centric Coordinates and Single-Pass Decoding for System-1 World Models</a></td><td>58</td><td>5</td><td>World Model</td><td>객체 중심 좌표와 single-pass 디코딩으로 빠른 System-1 시각 planning 설계 요소를 분석함</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2611.19857'>PanDWM: Panoramic 4D Driving World Models</a></td><td>58</td><td>5</td><td>World Model</td><td>파노라마 4D driving world model로 멀티뷰 일관성을 구조적으로 해결하나 자율주행 영상 생성임</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2611.20385'>DominoBench: Evaluating Multi-Step Physical Reasoning from Still Images</a></td><td>58</td><td>5</td><td>Embodied AI</td><td>정지 이미지로 연쇄 반응 다단계 물리 추론을 묻는 벤치마크로 physical reasoning 평가임</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2611.19681'>RIFT: Reward Improvement Field Transfer for Cross-Domain Offline RL</a></td><td>58</td><td>5</td><td>RL</td><td>저보상과 고보상 source 전이 차이를 affine field로 학습해 cross-domain offline RL 데이터를 증강함. locomotion dynamics shift만 검증함</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2611.20230'>A Matrix with Steps: An Episodic and Procedural Memory Method for Tool-Using Agents and Robots</a></td><td>58</td><td>5</td><td>Robot Memory</td><td>episode를 외부 검증된 결과로만 기록하고 delta rule 행렬과 step record로 절차 memory를 구성함, 시뮬레이션 로봇의 자기판단 성공 보고 96% 대비 실제 해결 35%가 외부 검증으로 79%가 됨을 보여 robot memory와 연결되나 합성 환경 중심임</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2611.21539'>Seen but Unsaid: Locating and Repairing Cross-Image Comparison in Vision-Language Models</a></td><td>58</td><td>4</td><td>Multimodal</td><td>VLM의 두 이미지 대응 실패를 attention head 몇 개로 추적하고 파라미터 0.02% 수정으로 SPair-71k를 28.3점 올린 해석 연구임</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2611.20655'>MetaAct: Self-Evolving Executable Action Constraints for Embodied Language Agents</a></td><td>58</td><td>4</td><td>Embodied AI</td><td>experience에서 실행 가능한 action 제약 rule(GEAR)을 합성해 ScienceWorld 위반을 70%에서 0%로 줄임. embodied text 환경의 action admissibility 문제를 다루나 텍스트 시뮬레이션 한정임</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2611.19663'>When AI Agents Should Repair, Replan, or Abandon: A Threshold Theory of Plan Commitment</a></td><td>58</td><td>4</td><td>Planning</td><td>계획이 깨졌을 때 repair, replan, abandon을 결정하는 임계 정책을 이론적으로 유도함, failure recovery 의사결정에 대한 형식적 분석이나 실제 로봇/agent 실험 검증은 수치 검사기 수준임</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2611.21366'>ALIVE: Making Streaming Video Models Interactive</a></td><td>58</td><td>3</td><td>Multimodal</td><td>streaming video LLM에 능동 모니터링과 되묻기를 학습시키는 SFT와 RL 방식이며 상호작용 agent와는 이어지나 로봇 실험은 없음</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2611.19700'>Where Should LLM Agents Adapt at Test Time? In Context, in Weights, or Both</a></td><td>58</td><td>3</td><td>LLM Agent</td><td>LLM agent의 test-time 적응을 ICL, GRPO, SDPO로 14가지 비교해 ICL+GRPO 조합이 가장 좋음을 보임. 코드, 앱 환경 한정이나 test-time adaptation 관점은 참고됨</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2611.18696'>ARC-VLN: Adaptive Recursive Computing-based Visual-Language Navigation</a></td><td>56</td><td>6</td><td>Navigation</td><td>항공 VLN용 recursive computation으로 효율화하나 token-type 기법 중심임</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2611.20737'>CLIFT: Contrastive LiDAR Instance Features for 3D Pedestrian Tracking</a></td><td>56</td><td>6</td><td>3D Vision</td><td>social robot용 LiDAR 보행자 tracking에 contrastive instance feature를 쓰나 tracking 개선 범위임</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2611.19329'>Gradient-Based Co-Design of Systems and Reinforcement Learning Policies with Differentiable Simulators</a></td><td>56</td><td>6</td><td>RL</td><td>시스템 설계와 RL policy의 co-design을 implicit function theorem으로 설계 기울기를 구해 BO와 ES보다 낫게 보였으나 networked system 벤치마크 한정임</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2611.19078'>Assume/Guarantee Contracts for the Compositional Multi-Agent Reinforcement Learning of Heterogeneous Teams</a></td><td>56</td><td>6</td><td>RL</td><td>heterogeneous 팀 MARL에 assume/guarantee contract와 automaton으로 task 할당·재사용을 가능하게 하는 IHA-MARL을 제안함. 합성 가능한 abstraction이 좋고 학습 시간이 7~11배 짧으나 benchmark 3개 규모임</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2611.19429'>Prepare Lighter and Faster for Open-Vocabulary Queries: A Query-Wise 3D Segmenter for Gaussian Splatting</a></td><td>56</td><td>5</td><td>3D Vision</td><td>Gaussian splatting open-vocab 3D 분할을 query-wise로 가볍게 해 semantic map과 연결됨</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2611.18723'>Acting by Intent, Reacting by Sight: Visual Conditioned Reflexes for Real-Time VLM Agents</a></td><td>56</td><td>4</td><td>Agent</td><td>VLM agent에 시각 반사 제어를 더해 실시간 제어 문제를 다루나 게임 환경임</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2611.20090'>Latent World Modeling for Point-Cloud Video Pretraining</a></td><td>56</td><td>4</td><td>Video</td><td>point cloud video 사전학습에 latent world modeling을 적용해 masked modeling 정보 누수 문제를 다룸</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2611.19537'>Continuation-Guided LLM Evolution of Program Policies and Goal Compilers in Craftax</a></td><td>56</td><td>4</td><td>RL</td><td>Craftax에서 feedback cascade로 코드 policy를 진화시키고 재사용 가능한 goal compiler를 학습해 zero-shot으로 긴 과제에 전이함, long-horizon 계획 관점은 관련되나 게임 환경 한정임</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2611.21600'>How VLMs Plan What&#x27;s Next</a></td><td>56</td><td>3</td><td>Multimodal</td><td>VLM이 다음 객체를 고르는 binding head, cursor, gaze head 메커니즘을 causal patching으로 밝혀 multi-step planning 해석에 닿음</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2611.18747'>Video-as-Experience: Learning Computer Use via Audio-Visual Understanding</a></td><td>56</td><td>3</td><td>Multimodal</td><td>튜토리얼 영상의 시청각 정보로 computer-use agent를 학습하는 VEX와 AGGO를 제안해 OSWorld 성공률을 22% 상대 개선함. watch-act-rewatch로 자기 실행을 검증하는 구조가 흥미로우나 GUI 도메인임</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2611.20100'>EgoSwarm: Learning Decentralized Robot Swarm Intelligence from Human Swarm Demonstrations</a></td><td>55</td><td>7</td><td>Multi-robot</td><td>인간 swarm 시연에서 분산 swarm 지능을 학습함. 새 설정이나 검증 범위 불확실함</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2611.20692'>ARMFUL: Learning Whole-Arm Grasp Configurations for Single-Arm Pickup of Large Objects</a></td><td>55</td><td>7</td><td>Manipulation</td><td>큰 물체를 한 팔로 감싸 드는 whole-arm grasp configuration을 학습함. 신선한 문제이나 범위 좁음</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2611.20984'>VASR: Vector-Aware Assembly Planning with Equivalent Structures and Repair-Cost Feedback</a></td><td>55</td><td>5</td><td>Embodied AI</td><td>SVG 인코더와 VLM을 융합하고 repair-cost 피드백 RL(RHPO)로 가구 조립 계층을 예측함. 장기 조립 계획과 연결되나 로봇 실행 없이 IKEA 파생 데이터의 계층 예측임</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2611.19227'>Can an Agent Rethink What It Knows? Selective Scene Memory Updates in a Changing World</a></td><td>55</td><td>5</td><td>Embodied AI</td><td>물리 환경 변화에서 LoRA로 장면 semantic memory를 갱신할 때 교정과 보존을 함께 측정하는 프로토콜을 제시함. 예산 8에서 32로 늘리면 joint 성공이 6.25%에서 94.79%로 오르나 합성 4필드 설정이고 4B 텍스트 모델 한정임</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2611.21094'>Conflict-Aware Multi-Teacher On-Policy Distillation in Aligned Action Spaces for Cross-Game Generalization</a></td><td>55</td><td>4</td><td>Embodied AI</td><td>여러 게임 teacher를 정렬된 action space에서 충돌 인지 on-policy distillation으로 합쳐 pixel 입력 VLM이 미지 게임을 zero-shot 제어함, 일반 policy 통합 관점은 관련되나 게임 환경 4B 모델 실험임</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2611.20922'>Experience Rot: Experienced Agents Fail Where Novices Succeed</a></td><td>55</td><td>3</td><td>NLP</td><td>도구 정의가 조용히 바뀔 때 경험 많은 agent가 이전 호출을 복사해 신입 agent보다 더 실패하는 Experience Rot을 보임. memory 기반 agent의 실패 모드를 잘 드러내나 해결책은 제시하지 않음</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2611.18642'>Agents Cannot Hand Over What They Have Not Yet Understood</a></td><td>55</td><td>3</td><td>Embodied AI</td><td>숨은 규칙이 있는 56개 상호작용 세계에서 300자 인수인계 노트가 학습 내용을 잃는 handoff loss를 분해해 반복 압축이 주원인임을 보임. 장기 memory와 지식 전달 관점이 있으나 텍스트 agent 실험임</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2611.20916'>EviBridge: Encoding Predictive Visual Evidence for Proactive Interaction</a></td><td>54</td><td>6</td><td>Embodied AI</td><td>tool handover에서 선제 준비를 위한 predictive visual evidence 인코딩으로 HRI 문제 설정이 새로움</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2611.18743'>Recognizing Events Is Not Enough: Why Streaming VLMs Struggle in Compositional Instruction Triggering</a></td><td>54</td><td>5</td><td>Video</td><td>스트리밍 VLM의 조건부 compositional 지시 트리거 실패 분석으로 진단 성격이 있고 embodied 모니터링과 연결됨</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2611.21126'>IGRecon4D: Dynamic-Object-Aware Feed-Forward Reconstruction of Driving Scenes</a></td><td>54</td><td>5</td><td>3D Vision</td><td>동적 객체 인지 feed-forward 4D 주행 장면 복원으로 4D representation이나 주행 특화임</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2611.19341'>A Think Block Is Conditioning, Not a Plan</a></td><td>54</td><td>2</td><td>Generative</td><td>chain-of-thought가 계획이 아닌 conditioning이라는 치환 실험 분석으로 통찰은 있음</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2611.19198'>Self-Calibrating Vision-Agent-Action: Deploying Pick-and-Place to New Robot Cells without Demonstrations or Fine-Tuning</a></td><td>52</td><td>7</td><td>Manipulation</td><td>사전학습 VLM 기반 agent가 시연과 fine-tuning 없이 새 robot cell에 self-calibrate함. 시뮬레이션 범위로 보임</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2611.20452'>XMimic and XSoma: Learning Humanoid Motion Tracking and Locomotion in Under a Minute</a></td><td>52</td><td>7</td><td>Humanoid</td><td>humanoid motion tracking과 locomotion을 1분 내 학습함. 속도 개선 위주의 engineering임</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2611.20557'>AsymEEF: Bimanual Manipulation with Asymmetric End Effectors</a></td><td>52</td><td>7</td><td>Manipulation</td><td>비대칭 end effector bimanual 조작에서 시연 재사용을 시도함. 문제는 적절하나 incremental함</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2611.20719'>ACiT: Proprioceptive-Prior Action Chunking with Inverted Transformers</a></td><td>52</td><td>7</td><td>Imitation</td><td>proprioceptive prior와 inverted transformer로 action chunking을 개선함. 작은 module 수준 개선임</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2611.20648'>Competent Autonomous Driving Through Fine Tuning Vision Language Action Models with Symbolic Traffic Rules</a></td><td>52</td><td>6</td><td>VLA</td><td>driving VLA를 symbolic 교통 규칙으로 fine-tuning해 규칙 준수를 높이나 도메인 특화임</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2611.18644'>Minari: Infrastructure for Collaborative Reinforcement Learning Datasets</a></td><td>52</td><td>6</td><td>RL</td><td>Minari는 offline RL 데이터셋 생성과 공유 라이브러리로 D4RL을 재생성했고 재현성에 기여하나 학습 방법 기여는 아님</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2611.19563'>Sharp First-Hit Identification from Finite Depth Samples</a></td><td>52</td><td>6</td><td>3D Vision</td><td>유한한 깊이 샘플에서 새 시점의 first-hit 깊이가 결정되는 집합을 Lipschitz 장 이론으로 정확히 규정했으나 학습 깊이 가정이 자주 깨짐을 인정함</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2611.19616'>Towards Probabilistically Safe Reinforcement Learning: Theory and Deployment on Humanoid and Aerial Robots</a></td><td>52</td><td>6</td><td>RL</td><td>확률적 안전 RL의 이론과 humanoid, 항공 로봇 배치를 다룸. 실로봇 검증은 장점이나 방법은 기존 안전 RL 틀임</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2611.19775'>Recovery-Guided Model-Based Diffusion for Safety-Critical Legged Locomotion</a></td><td>52</td><td>6</td><td>Locomotion</td><td>복구 지향 model-based diffusion으로 고속 legged locomotion의 안전성을 높임. 문제 설정은 적절하나 locomotion 한정임</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2611.20558'>Vision-Language Grounded Semantic Navigation for Autonomous Mobile Robots</a></td><td>52</td><td>6</td><td>Navigation</td><td>VL 기반 의미 navigation 시스템임. 기존 구성요소 통합 위주임</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2611.21035'>FlowRow: Learning Navigation Behaviors in Agricultural Environments with Long-Horizon Goal-Conditioned Flow Matching Policies</a></td><td>52</td><td>6</td><td>Navigation</td><td>goal-conditioned flow matching으로 농업 환경 navigation을 학습함. 도메인 특화 적용임</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2611.19184'>Do VLMs Really Look at the Road? A Diagnostic Evaluation for Autonomous Driving</a></td><td>52</td><td>5</td><td>Embodied AI</td><td>VLM이 도로를 실제로 보는지 진단 평가로 자율주행 진단이나 벤치마크 성격임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2611.20076'>SGIP: Learning Scene-Grounded Interaction Priors for Scene-Aware Human Motion Prediction</a></td><td>52</td><td>5</td><td>Embodied AI</td><td>장면 grounded 상호작용 prior로 인간 모션 예측을 개선하며 HRI와 연결되나 incremental함</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2611.18807'>Recovered or Memorized? Investigating Dynamical Consistency and Faithfulness in World Model Latents</a></td><td>52</td><td>5</td><td>World Model</td><td>TD-MPC2 latent가 진자 동역학에 충실한지 Frechet 거리와 개입으로 검증하는 ARC를 제안했으나 pendulum 하나뿐임</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2611.21465'>Warm Starting Neural Dynamics Models From Few Jacobian Samples</a></td><td>52</td><td>5</td><td>RL</td><td>소수 Jacobian 샘플로 neural dynamics model을 warm start함. MBRL 샘플 효율 측면에서 유의미하나 범위 제한적임</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2611.21183'>Seeing Isn&#x27;t Resolving: Visual and Linguistic Disambiguation with Conversational Grounding</a></td><td>52</td><td>5</td><td>Embodied AI</td><td>인간-로봇 대화에서 시각·언어 모호성 해소를 보는 일본어 JAG-D benchmark로 VLM의 dialogue 문맥 활용을 평가함. HRI 관점의 grounding이지만 소규모 평가이고 로봇 실행은 없음</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2611.20953'>Same Fix, Different Weights: Replicating Weight-Space Programming with Claude</a></td><td>52</td><td>4</td><td>LLM Agent</td><td>GPT-6 Astra의 weight-space programming을 Claude로 재현해 MountainCar 정책을 0%에서 100%로 고침. 가중치 편집으로 제어기를 쓰는 흥미로운 결과이나 단일 연구자의 재현이고 단순 RL 환경 위주임</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2611.19461'>Program Distillation: Transferring LLM Capability from System 2 to System 0</a></td><td>52</td><td>4</td><td>RL</td><td>LLM이 학습 중 프로그램 policy를 만들고 배포 시 CPU 프로그램만 실행하는 Program Distillation과 27개 제어 과제 PDBench를 제안함, PPO를 넘는 결과가 흥미로우나 장난감 제어 환경 중심임</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2611.20970'>Hilbert States for Decision-Making under Partial Observability</a></td><td>52</td><td>4</td><td>Theory</td><td>부분 관측 의사결정에서 hidden state 복원 없이 최적 행동을 보존하는 3차원 Hilbert state를 평면 목표 비용에서 유도함, POMDP 정보 한계에 대한 이론이나 실험은 SAR 이미지와 시뮬레이션에 한정됨</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2611.21471'>Subprocess-Constrained Markov Decision Processes</a></td><td>52</td><td>4</td><td>RL</td><td>모든 reachable history에서 연속 비용 한계를 만족해야 하는 subprocess-constrained MDP를 정의하고 history-dependent 다항시간 알고리즘을 제시함, safe RL 형식화로 새로우나 순수 이론이며 실험 규모가 작음</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2611.18718'>Editable Video Context: Mid-Context KV-Cache Reuse for Context-Managing Video LLMs</a></td><td>52</td><td>3</td><td>Video</td><td>video LLM의 KV-cache 중간 재사용으로 efficient inference이며 memory 관리와 연결됨</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2611.20936'>ReAccess: Look Once, Stay Focused with Efficient Test Time Memory</a></td><td>52</td><td>3</td><td>Multimodal</td><td>VLM test-time memory로 한 번 보고 근거 유지하는 효율 기법으로 test-time 기법이나 로봇 검증 없음</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2611.21605'>ViRA: Toward Ultra-High-Resolution Visual Agents via Cross-Input Relative Policy Optimization</a></td><td>52</td><td>3</td><td>Multimodal</td><td>정답을 찍는 shortcut을 막는 contrast set 기반 RL(CrossRPO)로 초고해상도 visual agent를 학습시켰으나 대상이 VQA임</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2611.20666'>Conditional Diffusion Models for Amortized Bayesian System Identification</a></td><td>52</td><td>3</td><td>LG</td><td>conditional diffusion transformer로 hidden Markov model의 상태와 파라미터를 amortized 추론함. 5배 긴 기록에도 정확도를 유지하나 시스템 식별 benchmark 4개 한정임</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2611.19752'>StaleBench: Isolating Stale Retrieval in Agent Memory, and Pricing the Fix</a></td><td>52</td><td>3</td><td>NLP</td><td>agent memory에서 오래된 사실이 검색되는 stale retrieval을 분리해 재는 StaleBench와 Contamination@5 지표를 제안함. memory 평가 관점은 있으나 텍스트 한정임</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2611.20759'>Instant Weight-Space Consolidation for Long-Term Memory in LLMs</a></td><td>52</td><td>3</td><td>NLP</td><td>recurrent hypernetwork가 세션 activation을 gradient 없이 low-rank adapter로 consolidate하는 CLAM을 제안함. 장기 memory의 parametric 접근이 새롭고 LoCoMo에서 강하나 텍스트 대화 한정임</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2611.18668'>UMM-JEPA: Generative Pretraining via Masked Next-Scale Representation Prediction for Unified Multimodal Models</a></td><td>52</td><td>2</td><td>Multimodal</td><td>통합 멀티모달 모델 생성 사전학습을 표현 예측으로 바꾼 시도로 이해 성능 개선 위주임</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2611.18746'>VTG-RAG: Long-Video Reasoning via Query-Adaptive Coarse-to-Fine Sampling and Temporal Graph Retrieval</a></td><td>52</td><td>2</td><td>Video</td><td>장영상 추론용 coarse-to-fine 샘플링과 temporal graph 검색으로 incremental함</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2611.20000'>What Matters for Cross-Modal Alignment</a></td><td>52</td><td>2</td><td>Representation</td><td>cross-modal alignment에 중요한 요소 분석으로 Platonic 가설 검증이나 로봇 연결 약함</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2611.19064'>Policy Optimization With Multiple Verifiers via Pareto Rankings</a></td><td>52</td><td>1</td><td>RL</td><td>다중 verifier 결과를 Pareto 부분 순서로 두고 가능한 모든 ranking 확률을 최대화하는 POLPO를 제안함. scalar reward 집계를 피하는 새 objective이나 코드·지시 이행 평가 한정임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2611.20427'>Fuzzy Explainable Continual Hierarchical Reinforcement Learning for Robotic Navigation</a></td><td>50</td><td>7</td><td>Navigation</td><td>fuzzy critic과 2단계 behavior cloning으로 continual 계층 RL 로봇 항법의 설명 가능성을 다룸. 순차 시나리오 항법을 다루나 비교 근거가 약하고 시뮬레이션 위주로 보임</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2611.20791'>QTOP: Scaling Humanoid Motion Tracking with Quantile Critics</a></td><td>50</td><td>7</td><td>Humanoid</td><td>quantile critic으로 humanoid motion tracking을 확장함. RL 개선 incremental함</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2611.20888'>Driving the Style: Velocity-Conditioned Whole-Body Control from Motion Demonstrations</a></td><td>50</td><td>7</td><td>Humanoid</td><td>속도 조건 whole-body 제어를 시연에서 학습함. adversarial imitation 계열 incremental함</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2611.21059'>Multi-CONDOR: Learning Multistable Motion Primitives from Demonstration</a></td><td>50</td><td>7</td><td>Imitation</td><td>시연에서 multistable 모션 프리미티브를 학습함. DS 기반 고전 계열 확장임</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2611.20196'>DoF-Query Transformer for Adaptive Fusion of Egocentric Vision and Forearm HD-sEMG in Continuous Hand Kinematics</a></td><td>50</td><td>6</td><td>Manipulation</td><td>egocentric 영상과 sEMG 융합 연속 손 kinematics 추정으로 인간 조작 데이터 수집과 연결됨</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2611.19318'>Residual Reinforcement Learning for Visual Servo Control with Zero-Shot Sim-to-Real Transfer</a></td><td>50</td><td>6</td><td>RL</td><td>residual RL로 컨베이어 위 물체 추적 visual servo를 zero-shot sim-to-real함. 응용 위주임</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2611.19095'>DEFDVO: Deformable Deep Visual Odometry for Equirectangular Images</a></td><td>50</td><td>5</td><td>3D Vision</td><td>360도 영상용 deformable deep VO로 로봇 odometry와 연결되나 incremental함</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2611.20518'>What the Averages Hide: Monocular Metric Depth Models Still Fail in Everyday Scenes, Mostly on Scale</a></td><td>50</td><td>5</td><td>3D Vision</td><td>metric depth 모델이 일상 장면에서 주로 scale 오류를 낸다는 평균 뒤 실패 분석으로 로봇 depth 활용에 유용함</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2611.20107'>SAFER: Navigating the Exploration-Exploitation Dilemma in World-Model-Based Planning for Autonomous Driving</a></td><td>50</td><td>5</td><td>Autonomous Driving</td><td>world model 기반 주행 planning의 탐험 활용 균형을 다룸. world model 활용이나 도메인 한정임</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2611.20402'>Making Koopman Control Guarantees Hold on Robots</a></td><td>50</td><td>5</td><td>Control</td><td>Koopman 제어 보증을 실제 비선형 plant에서 성립시킴. 이론적 의미 있으나 적용 범위 좁음</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2611.20593'>JEPTERA: A Platform Agnostic JEPA-Assisted Model Predictive Planner for Urban UAV Navigation</a></td><td>50</td><td>5</td><td>Navigation</td><td>JEPA 보조 MPC로 도시 UAV navigation을 함. JEPA 활용은 흥미로우나 도메인 한정임</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2611.20929'>Transferable Neural CBFs via Generalized Closure</a></td><td>50</td><td>5</td><td>Safety</td><td>transferable neural CBF의 일반화 closure를 제시함. 이론 기여가 있으나 로봇 학습 연결 약함</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2611.19409'>SplatFlow3D: Learning Scene Flow via 3D Motion Feature Splatting</a></td><td>50</td><td>4</td><td>3D Vision</td><td>3D motion feature splatting 기반 multi-frame scene flow로 동적 장면 이해에 도움됨</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2611.19830'>Beyond Vehicle-Centric Data: Scaling Autonomous Driving through Roadside-to-Vehicle Generation</a></td><td>50</td><td>4</td><td>Embodied AI</td><td>로드사이드 영상으로 차량 시점 주행 데이터를 생성해 scale하는 아이디어이나 생성 데이터 중심임</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2611.19572'>Spectral Steering: Local Inverse Geometry for Frozen Diffusion Generators</a></td><td>50</td><td>4</td><td>Generative</td><td>frozen diffusion generator의 guidance 방향을 국소 역기하로 보정하는 spectral steering이며 로봇과 제어 응용을 포함함</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2611.20019'>D&#x27;BEAST: Logged Bad Experiences as Explanation for Autonomous Driving Agents</a></td><td>50</td><td>4</td><td>RL</td><td>tabular RL agent의 결정을 나쁜 경험 replay 제거 실험으로 설명하고 CARLA 주행에 적용함. 실패 원인 추적 관점은 관련되나 tabular agent 한정임</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2611.19684'>Early Readability of Trajectory Quality in Diffusion Driving Planners</a></td><td>50</td><td>4</td><td>Autonomous Driving</td><td>diffusion 주행 planner의 내부 상태로 후보 궤적 품질을 조기 예측함. 분석 성격이나 test-time 선택에 활용 가능함</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2611.21596'>SADL: On the Demand-Supply Geometry of Representation Collapse</a></td><td>50</td><td>4</td><td>Representation</td><td>JEPA의 representation collapse 수요-공급 기하 분석임. 이론적 통찰이나 로봇 직접 연결 약함</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2611.18708'>TopSDF: Topological Signed Distance Field for High-Quality Triangle Mesh Extraction from 3D Gaussian Splatting</a></td><td>50</td><td>3</td><td>3D Vision</td><td>3DGS에서 watertight mesh 추출 topological SDF로 3D 표현 개선이나 렌더링 중심임</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2611.18715'>T2T Technical Report: Synthesizing GUI Agent Trajectories at Scale from Video Tutorials</a></td><td>50</td><td>3</td><td>Agent</td><td>영상 튜토리얼에서 GUI agent trajectory 합성으로 데이터 생성이나 로봇 아님</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2611.19642'>Beyond the Training Cameras: Coverage-Controlled Probes of Viewing Direction in Frozen Vision Models</a></td><td>50</td><td>3</td><td>3D Vision</td><td>frozen vision model이 시점 방향을 인코딩하는지 coverage 통제 probe로 분석해 공간 표현 이해에 유익함</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2611.20446'>LEDGE: Separating Critic and Editor Failures in Text-to-Image Self-Correction</a></td><td>50</td><td>3</td><td>Generative</td><td>T2I 자기 교정에서 critic과 editor 실패를 분리 진단해 failure diagnosis 관점이 있으나 이미지 생성임</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2611.20899'>SciWorldBench: Do Video World Models Really Understand Scientific Experiments?</a></td><td>50</td><td>3</td><td>World Model</td><td>video world model의 과학 실험 이해를 평가하는 벤치마크로 진단 성격이나 과학 도메인임</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2611.20715'>Calibrate Once, Grow the Vocabulary: Candidate-Independent Scores for Conformal Risk Control in Open-Vocabulary Segmentation</a></td><td>50</td><td>3</td><td>CV</td><td>open-vocabulary segmentation에서 어휘가 늘어도 conformal risk 보장이 유지되도록 고정 reference bank 점수를 제안함. 보장 이론은 견고하나 로봇 직접 연결은 약함</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2611.19823'>EfficientSkill: Learning Skills for Token-Efficient Multi-Turn Agents</a></td><td>50</td><td>3</td><td>NLP</td><td>reflective skill optimizer의 prompt 비대화를 pruning과 코드 offload로 줄여 token을 최대 80% 절감함. ALFWorld 평가가 있으나 LLM agent 최적화 수준임</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2611.21019'>MemDoctor: Stage-wise Error Attribution and Repair for MLLM Agent Memory</a></td><td>50</td><td>3</td><td>Multimodal</td><td>MLLM agent memory를 Write·Update·Retrieve·Answer 4단계로 나눠 오류 원인을 역추적·수리하는 MemDoctor를 제안함. memory 실패 진단 관점이 있고 4B가 8B baseline을 앞서나 대화 memory 한정임</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2611.18685'>ThinkWise: Learning When to Think in Large Multimodal Reasoning Models via Visual and Difficulty Perception</a></td><td>50</td><td>2</td><td>Multimodal</td><td>멀티모달 reasoning 모델의 사고 여부 학습으로 efficient inference 측면은 있으나 로봇 연결 약함</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2611.21392'>VideoNexus: Video Perception Beyond the Reasoning Context</a></td><td>50</td><td>2</td><td>Video</td><td>긴 영상 이해에서 지각과 계획을 분리한 training-free agent 프레임워크이며 API 기반 benchmark 개선 중심임</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2611.19244'>Agentic On-Policy Distillation Implicitly Reshapes LLMs&#x27; ReAct Patterns</a></td><td>50</td><td>2</td><td>RL</td><td>on-policy distillation이 ReAct 패턴을 바꾸고 ALFWorld 학습이 tau2 정확도를 41.5%에서 6.6%로 낮추는 negative transfer를 보임. 선택적 OPD로 완화를 시도하며 agent 도메인 간 전이 분석이 유용함</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2611.21301'>Latent Bridge: Asking for Help Without Words</a></td><td>50</td><td>1</td><td>LG</td><td>큰 모델은 prefill만 하고 작은 모델이 decode하며 hidden state를 KV로 전달하는 POND를 제안함. 큰 모델 decoding 비용을 줄이는 representation transfer가 흥미로우나 추론·코딩 benchmark만 평가함</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2611.18564'>Check Token: Real-Time Self-Verification and Precise Truncation in LLM Reasoning</a></td><td>50</td><td>0</td><td>LG</td><td>&lt;CHECK&gt; 토큰으로 LLM 추론 중 자가 검증과 절단을 학습시키는 방법이며 로봇과 무관함</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2611.19800'>Multi-Branch Transformer</a></td><td>50</td><td>0</td><td>NLP</td><td>Transformer block을 병렬 branch로 구성해 같은 compute에서 손실 개선과 처리량 51.4% 증가를 보임. 언어 모델 아키텍처 연구임</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2611.20404'>Latent Feedback Is a Compute and Data Amplifier</a></td><td>50</td><td>0</td><td>NLP</td><td>latent feedback이 같은 compute에서 최대 48% 연산과 47% 데이터를 절약함을 scaling law로 보임. 근거는 탄탄하나 언어 모델 사전학습 연구임</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2611.19720'>Sim-to-Real Room-Mediated Object-Goal Navigation with ROS 2 and Nav2</a></td><td>48</td><td>6</td><td>Navigation</td><td>room 매개 ObjectNav를 ROS 2와 Nav2로 sim-to-real 평가함. 시스템 통합 위주임</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2611.20185'>RoboKit: Accelerating Parallel Differentiable Optimization for Robot Learning</a></td><td>48</td><td>6</td><td>Tools</td><td>병렬 미분 가능 최적화 toolkit임. 유용한 도구이나 연구 novelty는 중간임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2611.21209'>BoBDeLaN: Bounded-Bandwidth Context Adaptation for Deep Lagrangian Robot Control</a></td><td>48</td><td>6</td><td>Control</td><td>Deep Lagrangian 제어의 bounded-bandwidth 맥락 적응임. 제어 중심 개선임</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2611.19190'>Distilling Safety Filters for Filter-free Multi-agent RL</a></td><td>48</td><td>5</td><td>RL</td><td>CBF safety filter를 distill해 filter 없는 multi-agent RL을 만듦. 실용적이나 incremental함</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2611.19247'>GameWM: Toward Next-Generation Video Games with Interaction-Centric World Models</a></td><td>48</td><td>3</td><td>World Model</td><td>게임용 상호작용 중심 world model로 interactive video model이나 로봇 검증 없음</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2611.21553'>BLIP-Live: Balancing Timeliness &amp; Firing Precision in Proactive Streaming Video Agents</a></td><td>48</td><td>3</td><td>Video</td><td>proactive streaming 영상 agent의 응답 시점과 정밀도를 다루는 데이터, 지표, 학습 묶음임</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2611.18671'>Thinking from Another Side of the Box: Spacetime Images for Computer Vision</a></td><td>48</td><td>2</td><td>Video</td><td>영상을 spacetime image로 보는 새 표현 제안이나 로봇 검증 없음</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2611.21478'>Jetriever: Shifting Agent Memory Retrieval from Similarity to Utility</a></td><td>48</td><td>2</td><td>NLP</td><td>agent memory 검색을 유사도 대신 Jev decision score의 유용성으로 순위화하는 Jetriever를 제안함. 간접 질의에서 gold를 1위로 84.8% 올리나 소규모 평가이고 특정 모델에 의존함</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2611.20605'>AdMem: Expectation-Grounded Procedural Memory for Long-Horizon Task-Solving Agents</a></td><td>48</td><td>2</td><td>LLM Agent</td><td>행동 전 기대 결과를 두고 critic이 실제와 비교해 procedural memory 항목에 credit과 utility를 부여하는 AdMem을 제안함, AgentBoard 707개 과제에서 441 대 388로 ReAct 대비 오르며 memory 수명주기 설계가 참고할 만하나 텍스트 환경 한정임</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2611.20087'>Does Learning Order Explain Forgetting? The Lie Bracket as an Early-Warning Signal for Catastrophic Forgetting Without Old Data</a></td><td>48</td><td>1</td><td>LG</td><td>Lie bracket이 old data 없이 catastrophic forgetting을 조기 예측하는지 검증하고 task-incremental에서 rho 0.70-0.81을 얻음. MNIST, CIFAR 규모이고 적용 조건이 좁음</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2611.20148'>Centered Ablation: Why Last-Layer Directional Ablation Under-Fires or Collapses, and a Closed-Form Fix</a></td><td>48</td><td>1</td><td>NLP</td><td>last-layer directional ablation이 logit bias와 같음을 보이고 common mode를 제거하는 closed-form 수정을 제안함. 분석이 깔끔하나 LLM refusal 제어 한정임</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2611.19762'>When Does an AUROC Comparison Survive a Change in Population Mix?</a></td><td>47</td><td>2</td><td>LG</td><td>failure detector의 AUROC 비교가 집단 혼합 변화에서 유지되는지 증명과 감사 방법으로 다룸. failure detection 평가 방법론이나 로봇 실험은 없음</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2611.20872'>MVSTF: Multi-View Spatio-Temporal Fusion for LiDAR-Based Moving Object Segmentation</a></td><td>46</td><td>5</td><td>3D Vision</td><td>이동 로봇용 LiDAR moving object segmentation multi-view 융합이나 incremental함</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2611.19839'>Passable for Whom? Few-Shot Personal Calibration of Sidewalk Accessibility Perception</a></td><td>46</td><td>4</td><td>Embodied AI</td><td>보행 가능성 판단의 사용자별 few-shot 보정으로 개인화 navigation 인식 문제를 다룸</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2611.20507'>VoxSAOR: Semantic-Aware Occupancy Robustification via Aleatoric Uncertainty Modeling</a></td><td>46</td><td>4</td><td>3D Vision</td><td>occupancy 예측에 aleatoric 불확실성으로 강건성을 높여 embodied 인식과 연결되나 incremental함</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2611.20788'>VA-Assembly: View-Aligned Score Guidance for Training-Free 3D Part Assembly</a></td><td>46</td><td>4</td><td>3D Vision</td><td>view-aligned score guidance로 training-free 3D part assembly를 해 part 구조 표현과 연결됨</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2611.20906'>Can Image Generators Hold a Scene Together When Space Is Broken Apart?</a></td><td>46</td><td>3</td><td>Generative</td><td>공간이 분리될 때 image generator의 장면 일관성 분석으로 공간 reasoning 진단임</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2611.18639'>SynthDCB: World Distillation for Scalable Device Control Benchmarking</a></td><td>46</td><td>3</td><td>Embodied AI</td><td>기기 제어용 상태 보유 실행 world를 증류로 합성해 SynthDCB를 만들었으나 도구 호출 agent 평가임</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2611.18656'>ECOD: Experience-Calibrated On-Policy Distillation for Multi-Turn Agents</a></td><td>46</td><td>3</td><td>RL</td><td>ALFWorld와 WebShop 에이전트의 on-policy distillation 감독 강도를 경험 기반으로 보정해 소폭 개선함</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2611.19200'>LogT: Logically Think with Images for Visual Search</a></td><td>46</td><td>2</td><td>Multimodal</td><td>zoom-in 시각 탐색용 논리 사슬 SFT 데이터 엔진으로 적은 데이터와 GPU로 기존 성능을 넘었으나 VQA 범위임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2611.20071'>The Silent Cost of Conversation History in LLM Reasoning</a></td><td>46</td><td>2</td><td>NLP</td><td>대화 history가 LLM 추론 정확도를 크게 낮추고 state summary가 이를 회복함을 사전등록 실험으로 보임. 장기 상태 추적 시사점은 있으나 텍스트 한정임</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2611.18680'>Spread Too Thin: How Higher Resolution Dilutes a Vision Transformer&#x27;s Attention, and a Training-Free Rescaling</a></td><td>46</td><td>1</td><td>CV</td><td>ViT 고해상도 attention 희석 보정으로 training-free 기법이나 로봇과 거리 있음</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2611.18648'>Rethinking Offline On-Policy Distillation: From Scalar Advantages to Distributional Supervision</a></td><td>46</td><td>1</td><td>NLP</td><td>offline on-policy distillation에서 scalar advantage가 분포를 평탄화함을 보이고 분포 감독 DistOPD를 제안했으나 에이전트 검색 LLM 범위임</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2611.19100'>Leaning Over to Reach Far-Away Objects</a></td><td>45</td><td>6</td><td>Control</td><td>humanoid가 환경에 몸을 기대 도달 범위를 넓히는 whole-body MPC임. 학습 요소 약함</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2611.19131'>Wireless Edge-Assisted Adaptive Latent Reasoning for Vision-Language-Action Models in Physical AI</a></td><td>45</td><td>6</td><td>VLA</td><td>무선 edge 지원 VLA의 적응형 latent reasoning임. 시스템 최적화 성격이 강함</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2611.21198'>Cooperative Mobile Manipulation using Learned Dynamical Systems</a></td><td>45</td><td>6</td><td>Mobile Manipulation</td><td>학습된 dynamical system으로 협력 mobile manipulation을 함. 고전 DS 계열임</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2611.18877'>Passage-Focused Soft Coordination for Hierarchical Multi-Robot Navigation in Bottleneck Environments</a></td><td>45</td><td>5</td><td>Navigation</td><td>병목 환경 multi-robot navigation에서 통로 중심 soft 조율을 제안함. 고전적 접근의 개선임</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2611.19660'>PSK: A Matrix-Free Single-Loop Method for K-Level Physics-Based Control</a></td><td>45</td><td>5</td><td>Control</td><td>implicit physics step 미분을 matrix-free로 수행하는 단일 루프 방법임. 최적화 중심임</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2611.21076'>Counting What Matters: Reducing Redundant Object Detections in Overlapping UAV Mapping Imagery for Disaster Response</a></td><td>45</td><td>5</td><td>3D Vision</td><td>UAV 매핑 영상에서 겹치는 검출을 sparse reconstruction 3D 위치와 DINOv3 임베딩으로 병합함, 재난 대응 로봇용 응용으로 YOLO fine-tuning과 엔지니어링 비중이 큼</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2611.21524'>Algorithm Distillation for Safe In-Context Reinforcement Learning</a></td><td>45</td><td>4</td><td>RL</td><td>Safe in-context RL을 algorithm distillation으로 구현함. 제약 하 적응이나 로봇 실험은 없음</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2611.19138'>SuperGlance: Driving at a Glance with a Vision-Language Model</a></td><td>45</td><td>4</td><td>Autonomous Driving</td><td>VLM 주행 plan을 한 번에 생성해 지연을 줄임. 주행 도메인 효율화임</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2611.20730'>Selective Sensor Acquisition for Multimodal Place Recognition</a></td><td>45</td><td>4</td><td>SLAM</td><td>multimodal place recognition의 선택적 센서 획득임. 효율 아이디어이나 도메인 한정임</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2611.18679'>Shared Mobile AR Without Depth Sensors from Monocular Point Maps</a></td><td>45</td><td>2</td><td>3D Vision</td><td>모노큘러 point map으로 깊이센서 없는 AR 기하 복원이며 공간 인식과 일부 연결됨</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2611.21339'>MovieRoll: A Systematic Framework for Rolling Out Long-Form Videos</a></td><td>45</td><td>2</td><td>Video</td><td>streaming 장편 영상 생성에서 KV cache 압축과 long-rollout distillation을 묶은 엔지니어링 중심 프레임워크임</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2611.21559'>Reference Forcing: Long Video Generation with Region-Guided Drift Correction</a></td><td>45</td><td>2</td><td>Video</td><td>초기 프레임을 참조로 쓰고 KV cache 값을 보정해 긴 영상 생성의 drift를 줄이는 방법으로 생성 품질 개선 중심임</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2611.19911'>&quot;Don&#x27;t Leave the Task Unfinished&quot;: Persistence-Driven Violations under Quiet Oversight</a></td><td>45</td><td>2</td><td>LLM Agent</td><td>persistence가 LLM agent의 제약 위반율을 29.2%에서 58.3%로 올림을 보임. 감독 방식에 따른 위반 분석은 흥미로우나 embodied 연결은 약함</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2611.18585'>Read, Route, Patch: Robust Test-Time Evolution for LLM Agents</a></td><td>45</td><td>2</td><td>NLP</td><td>LLM agent의 test-time evolution 강건화임. 로봇 연결 약함</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2611.20595'>Invariant-Aware Harness Enforcement to Protect LLM Agents from Silent API Failures</a></td><td>45</td><td>2</td><td>NLP</td><td>API가 조용히 실패해도 harness가 invariant로 결과를 막는 SilentGuard로 오답을 74.0%에서 1.7%로 줄임. 도구 호출 신뢰성 관점은 있으나 텍스트 agent 한정이고 abstain만 함</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2611.20569'>ToolGraph as a Q-Function for Test-Time Scaling of Tool-Use Agents</a></td><td>45</td><td>2</td><td>LLM Agent</td><td>tool 의존 graph를 interventional probe로 만들고 goal 조건 Q 함수로 test-time scaling에 쓰는 ToolGraph를 제안함, LLM 추정기가 PageRank 대비 평균 8.3점 오르나 tool-use 벤치마크 한정임</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2611.21541'>SciResearch-Eval: Evaluating Scientific Judgment in Autonomous Experimental Agents</a></td><td>45</td><td>2</td><td>LLM Agent</td><td>결함 있는 시뮬레이터로 열 물성을 재는 agent가 실험을 설계하고 보정된 구간을 보고하는지 2,511 episode로 평가함, active experiment design과 보정 관점이 있으나 단일 물리 과제임</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2611.19634'>Multi-Objective Causal Bandits: Minimal Intervention Space and Policy-Level Learning</a></td><td>45</td><td>1</td><td>LG</td><td>multi-objective causal bandit의 Pareto 최적 개입 집합을 그래프로 특성화하는 이론 연구임. 로봇 연결은 약함</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2611.19676'>Score-Based Stochastic Closure Modeling via Offline Indirect Learning and Online Data Assimilation</a></td><td>45</td><td>1</td><td>LG</td><td>score 기반 diffusion으로 확률적 closure를 간접 학습하고 data assimilation을 결합함. 난류 실험만 있어 로봇과는 거리 있음</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2611.20430'>TrainExplorer: Autonomous LLM Post-Training via Plan-and-Decouple Exploration</a></td><td>45</td><td>1</td><td>LLM Agent</td><td>plan-and-decouple 탐색으로 LLM post-training을 자동화해 PostTrainBench에서 Claude Code보다 7.32점 높음. agent 자동화 연구이고 로봇 연결은 약함</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2611.21241'>Anytime-Valid PAC-Bayes Certificates for Adaptive Test-Time Scaling</a></td><td>45</td><td>1</td><td>LG</td><td>adaptive test-time scaling에 대한 PAC-Bayes 보증을 제시함. 이론적이나 로봇 적용 없음</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2611.19560'>SemMask: Semantic-Prioritized Progressive Masking for Diffusion Language Models</a></td><td>45</td><td>1</td><td>NLP</td><td>diffusion LM에서 gradient로 고른 semantic token을 먼저 복원하게 하는 masking fine-tuning을 제안함. 텍스트·코드 생성 한정이며 로봇과 무관함</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2611.19388'>SARGO: Agreement-Gated Reinforcement and Suppression via On-Policy Self-Guidance for Visual Hallucination Mitigation</a></td><td>45</td><td>1</td><td>Multimodal</td><td>VLM 환각을 줄이려 토큰별 advantage를 agreement로 gate하는 post-training SARGO를 제안함, 환각 벤치마크 개선 위주의 incremental 기여임</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2611.19871'>Interactive Structured Environment Scaling for Large Language Model Agentic Reasoning</a></td><td>45</td><td>1</td><td>RL</td><td>KG 질의응답 RL에서 사전 필터링된 subgraph가 정답을 누설함을 지적하고 전체 DB 상호작용 환경 RISE를 제안함, LLM agent RL 환경 개선이며 로보틱스와 거리가 있음</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2611.21003'>K2-Horizon: A Frontier Fleet of Open Source Language Models</a></td><td>45</td><td>1</td><td>LLM</td><td>0.9B~375B-A23B 완전 공개 언어 모델 6종과 MoVA attention, diffusion adapter를 공개함, 개방성은 크나 로보틱스와 직접 연결은 없음</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2611.20693'>Fast at the Frontier, Wrong at the Fallback: A Commit-Level Analysis of Threshold Decoding in Diffusion Language Models</a></td><td>45</td><td>0</td><td>NLP</td><td>diffusion LM의 threshold decoding을 commit 단위로 추적해 fallback commit이 실패를 시작함을 보이고 frontier 전용 commit으로 복구함. 분석이 구체적이나 텍스트 생성 한정임</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2611.18866'>Découpage: Directorial Audio-Visual Control for Long Multi-Shot Video Generation</a></td><td>45</td><td>0</td><td>Video</td><td>시각·음향 경계를 분리해 장편 다중 샷 audio-video를 생성하는 Decoupage를 제안함. 영화 연출 제어에 특화된 생성이며 로봇과 무관함</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2611.21607'>ScaleVLA: Scaling Vision-Language-Action Models to 552 Billion Parameters</a></td><td>44</td><td>7</td><td>VLA</td><td>552B VLM backbone을 VLA에 연결해 scale 효과를 비교함. 단순 scale-up 성격이며 일부 결과만 제시됨. 일부 결과는 흥미로움</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2611.18597'>Skill-Latent Rewards: LLM-Guided Reward Formulation for Hierarchical Reinforcement Learning</a></td><td>44</td><td>5</td><td>RL</td><td>VLM이 subgoal을 식별하고 LLM이 latent reward를 만드는 계층 RL이나 MiniGrid와 BabyAI에서만 검증함</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2611.19358'>RETR: A Structure-Preserving RGB-Event Transformer for Robust 3D Lane Detection</a></td><td>44</td><td>3</td><td>3D Vision</td><td>RGB-Event 3D lane 검출로 자율주행 인식 incremental함</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2611.19593'>Learning Spatially Aware Audio-Visual Features from Videos with Mono Audio</a></td><td>44</td><td>3</td><td>Multimodal</td><td>모노 오디오 영상에서 공간 audio-visual 특징 학습으로 공간 인식에 일부 연결됨</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2611.20241'>EvoMem3D: Adaptive-Depth Temporal Representation Memory for Multi-Camera 3D Detection</a></td><td>44</td><td>3</td><td>3D Vision</td><td>멀티카메라 3D 검출 적응 깊이 temporal memory로 추론 효율 개선이나 incremental함</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2611.20797'>Correspondence-Free Camera Pose Estimation by Matching Moments</a></td><td>44</td><td>3</td><td>3D Vision</td><td>대응 없는 PnP를 moment 매칭으로 풀어 이론적 기여가 있으나 가정이 강함</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2611.21044'>Body of Evidence: Triangulating 3D Human Pose with Geometry-Conditioned Depth</a></td><td>44</td><td>3</td><td>3D Vision</td><td>멀티카메라 가림에서 geometry 조건 depth로 3D 인체 pose triangulation으로 incremental함</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2611.20644'>Instrumenting Failure: Scoring Language Model Agents at Every Decision Node in Imperfect-Information Games</a></td><td>44</td><td>2</td><td>LLM Agent</td><td>불완전 정보 게임에서 LLM의 모든 결정 노드를 CFR+ 기준으로 채점해 belief와 행동의 불일치를 보임. 결정 단위 failure 진단 관점은 흥미로우나 게임 한정임</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2611.19275'>Beyond Clumsy Agentic Tool Calling: How Cueing and Spotting Make the Difference</a></td><td>44</td><td>2</td><td>NLP</td><td>tool 호출 중 무시된 피드백과 반복 호출을 감지해 개입하는 middleware ToolPulse를 제안함. 행동 교정률은 높으나 최종 수정 성공률은 baseline과 비슷함</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2611.18670'>Evidence-Calibrated Selective Decoding for Reliable Visual Question Answering</a></td><td>44</td><td>1</td><td>Multimodal</td><td>VQA contrastive decoding 보정으로 incremental함</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2611.18861'>Guided Group Featurizers (GGF): Improving Block-Sparse Featurizers with Object-Guided Learning</a></td><td>44</td><td>1</td><td>CV</td><td>block-sparse featurizer에 객체 guidance 추가로 해석 가능성 개선이며 incremental함</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2611.19121'>DecoEdit: Beyond Flat Control for 3D-Aware Unified Image Editing</a></td><td>44</td><td>1</td><td>Generative</td><td>3D 인지 이미지 편집 프레임워크로 생성 중심임</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2611.20006'>Glance, then Select: Evidence-Tempered Visual Token Selection for Extremely Compressed Multimodal LLMs</a></td><td>44</td><td>1</td><td>Multimodal</td><td>MLLM visual token 선택 극단적 압축으로 효율화 incremental함</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2611.20505'>How Reliable Is Visual Token Selection? Rethinking Pruning in Multimodal LLMs</a></td><td>44</td><td>1</td><td>Multimodal</td><td>MLLM visual token pruning 신뢰성 재검토로 분석 위주임</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2611.18649'>Algebraic Interaction: A Recipe for Neural Architecture Generation</a></td><td>44</td><td>1</td><td>LG</td><td>convolution, attention, SSM을 대수 구조로 통합하고 feature algebra만 바꿔 속도와 equivariance를 얻는 설계 틀을 제시함</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2611.20981'>Breaking feature collapse in self-supervised time series encoders</a></td><td>44</td><td>1</td><td>LG</td><td>시계열 encoder의 feature collapse를 self-distillation과 KoLeo 정규화로 막아 143개 데이터셋에서 경쟁함. 표현 학습 개선이나 시계열 한정임</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2611.21056'>Evaluation-Free Recursive Self-Improvement for Coding Agents</a></td><td>44</td><td>1</td><td>NLP</td><td>downstream 평가 없이 구현 mechanism을 통합해 coding agent를 진화시키는 ELITE가 SWE-bench Pro를 60.0%에서 85.6%로 올림. 평가 비용 절감이 새롭지만 DGM·HGM에는 못 미치고 코딩 한정임</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2611.19173'>When Does Confidence Reveal Problem Difficulty?</a></td><td>44</td><td>1</td><td>AI</td><td>confidence 신호 중 perturbation inconsistency와 semantic entropy가 문제 난이도와 강하게 연관됨을 보임. 정답 여부를 넘어선 신호라는 분석이 유용하나 LLM 한정임</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2611.20335'>When Should Decision Models Compare Candidates?</a></td><td>43</td><td>2</td><td>NLP</td><td>agent의 후보 action 선택에서 pointwise·setwise·candidate attention scoring을 비교해 후보 간 비교가 항상 이득이 아님을 보임. 통제된 합성 실험이 있으나 텍스트 agent 한정임</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2611.20016'>GEM-MM: Reducing VLM Hallucination with Entropy-Guided Preference Alignment</a></td><td>43</td><td>1</td><td>Multimodal</td><td>VLM preference 최적화가 policy 불확실성을 무시한다고 보고 entropy 높은 fork token에 보상하는 GEM-MM을 제안함, 환각 지표 소폭 개선 위주임</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2611.20306'>Ontology-Compiled Control Barrier Functions for Heterogeneous Robot Teams</a></td><td>42</td><td>5</td><td>Safety</td><td>ontology로 compile한 CBF로 이질 로봇 팀 안전 필터를 만듦. 설계 중심임</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2611.20710'>SG-ODOM: Event-Driven Proprioceptive State Estimation with Stability-Gated Contact Updates for Legged Robots</a></td><td>42</td><td>5</td><td>Legged</td><td>legged 로봇 proprioceptive 상태 추정의 접촉 갱신 gating임. 고전 추정 개선임</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2611.20950'>ROSE: A Shared Cross-Embodiment Facial-Motion Latent Space for Humanoid Robot Expression</a></td><td>42</td><td>5</td><td>HRI</td><td>humanoid 얼굴 표정을 위한 cross-embodiment 모션 latent 공간임. 응용 특화임</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2611.21598'>Mitigating Catastrophic Forgetting with Physics-Indexed Specialist Memory: the Evolutionary Neuroplastic Agent</a></td><td>42</td><td>4</td><td>RL</td><td>continual RL에서 physics-indexed specialist memory로 forgetting을 완화함. 소규모 설정으로 보임</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2611.19922'>Lao Siji: Adapting openpilot to Closed-Loop End-to-End Driving in Neural Reconstruction</a></td><td>42</td><td>4</td><td>Autonomous Driving</td><td>openpilot을 neural reconstruction closed-loop 주행에 적응시킨 챌린지 보고임. 엔지니어링 중심임</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2611.19969'>Value and Policy Calibration from Execution Feedback for Socially Compatible Driving</a></td><td>42</td><td>4</td><td>Autonomous Driving</td><td>실행 feedback으로 value와 policy를 보정해 사회적 주행을 학습함. 주행 도메인임</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2611.20510'>WTR-Drive: World-Task Decomposition with Structured Risk Supervision for End-to-End Driving</a></td><td>42</td><td>4</td><td>Autonomous Driving</td><td>객체 단위 위험 supervision을 쓰는 end-to-end 주행임. 도메인 특화임</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2611.21163'>Polygraph: Large-Scale Multi-Session Trajectory Optimization using Pose Graphs</a></td><td>42</td><td>4</td><td>SLAM</td><td>pose graph 기반 대규모 multi-session 궤적 최적화임. SLAM 중심 incremental함</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2611.19188'>Calibrating the Uncertainty of Self-Supervised Monocular Depth without Labels</a></td><td>42</td><td>3</td><td>3D Vision</td><td>self-supervised depth 불확실성 라벨 없는 보정으로 유용하나 incremental함</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2611.18818'>What to Practice Next? Latent Profile-Guided Task Selection for Skill-Evolving LLM Agents</a></td><td>42</td><td>3</td><td>RL</td><td>LLM 에이전트의 연습 과제를 MIRT 프로파일로 고르는 curriculum이며 ALFWorld와 WebShop에서 1~13점 향상함</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2611.20570'>OrthoMark: Place Recognition with Point-Anchored Orthographic Height Mark</a></td><td>42</td><td>3</td><td>SLAM</td><td>LiDAR place recognition 표현 개선임. 해당 분야 incremental함</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2611.18770'>AerialOcc: Unified 3D Aerial Perception without Task-Specific Head</a></td><td>42</td><td>2</td><td>3D Vision</td><td>항공 3D 인식 통합 모델로 task head 제거이나 항공 특화임</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2611.19485'>PALIN: Pixel-Aligned LiDAR-NIR Multimodal 3D Object Detection with Benchmark</a></td><td>42</td><td>2</td><td>3D Vision</td><td>LiDAR-NIR 3D 검출 및 벤치마크로 센서 융합 incremental함</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2611.20703'>Efficient Multi-View Generation with Iterative Global-Local Proxy Attention</a></td><td>42</td><td>2</td><td>3D Vision</td><td>효율적 multi-view 생성 attention으로 3D 복원 보조이며 incremental함</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2611.19733'>Sample-Efficient Ensemble Reinforcement Learning at Scale</a></td><td>42</td><td>2</td><td>RL</td><td>MeanQ ensemble을 BBF에 결합해 Atari 100K에서 규모 확대 이득을 얻음. 이산 게임 한정의 incremental 연구임</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2611.20835'>Hierarchical Regime-Conditioned Dynamics for Spatiotemporal Graphs</a></td><td>42</td><td>2</td><td>LG</td><td>이산 regime과 연속 entity 동역학으로 분해하는 시공간 그래프 생성 모델 HERON을 제안함. regime 조건 시뮬레이션은 흥미로우나 로봇 응용 근거는 없음</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2611.21249'>Heteroscedastic Gaussian Process Q-learning for Sample Efficient Experimentation</a></td><td>42</td><td>2</td><td>RL</td><td>GP 기반 Q-learning으로 소수 실험에서 제어 학습함. 실험실 자동화 대상이며 incremental함</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2611.18627'>FlashREINFORCE: Critic-Free Single-Rollout Asynchronous RL for Agentic Language Models</a></td><td>42</td><td>2</td><td>RL</td><td>비동기 critic-free 단일 rollout RL로 agentic LM을 학습함. RL 효율 측면이나 언어 도메인임</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2611.19859'>When Facts Change, Which Decisions Break? Dependency-Aware Context Graphs for Agents</a></td><td>42</td><td>2</td><td>LLM Agent</td><td>사실이 바뀔 때 의존하는 결정만 고치도록 agent read trace에서 field 단위 dependency graph를 추출함, agent memory 갱신 관점은 있으나 절차적 workflow 한정임</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2611.20711'>AgentFaultBench: State-Verified Evaluation of Tool-Fault Recovery</a></td><td>42</td><td>2</td><td>LLM Agent</td><td>tool 실패 후 recovery 조언이 agent 성공을 올리는지 GitLab 환경에서 1,944회 실행으로 검증함, failure recovery를 다루나 수동 근거가 약하고 조언 효과가 모델별로 갈림</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2611.18666'>ReMoVe: Refining a Video Model&#x27;s Own Motion for Coherent Human Video Generation</a></td><td>42</td><td>1</td><td>Video</td><td>인간 영상 생성의 motion 정제 기법으로 로봇 연결 약함</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2611.18701'>What Does Hard-Negative Fine-Tuning Teach Multimodal Large Language Models? Controlled Evidence from a Compositional Benchmark</a></td><td>42</td><td>1</td><td>Multimodal</td><td>hard-negative fine-tuning이 가르치는 것 분석으로 통제 실험은 있으나 로봇 연결 낮음</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2611.19044'>Hard or Mislabeled? Failure Screens Enrich Vision Benchmarks for Label Errors</a></td><td>42</td><td>1</td><td>CV</td><td>벤치마크 label error 스크리닝 분석으로 데이터 품질 관점임</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2611.19213'>Incremental Learning of Vision-Language Models via Task Subspace Projection and Dynamic LoRA</a></td><td>42</td><td>1</td><td>Multimodal</td><td>VLM 증분학습 subspace projection과 dynamic LoRA로 incremental함</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2611.19745'>TIVS: Mapping the Sensitivity Landscape of Visual Token Transformations in MLLMs</a></td><td>42</td><td>1</td><td>Multimodal</td><td>MLLM visual token 변환 민감도 지도로 efficient inference 분석임</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2611.21029'>Sparse Attention for Visual Generation: Toward Algorithm-System Co-Design</a></td><td>42</td><td>1</td><td>Generative</td><td>생성용 sparse attention 알고리즘-시스템 공동 설계로 efficient inference이나 survey 성격임</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2611.21457'>Out of Sight, Into Memory: Compact Visual Latents Retain Local Evidence in Ultra-High-Resolution Remote Sensing</a></td><td>42</td><td>1</td><td>Multimodal</td><td>초고해상도 원격탐사 QA에서 압축 visual latent가 지역 증거를 유지하는지 진단했으나 적용 분야가 좁음</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2611.19999'>MOBO-CAPS: Multi-Objective Bayesian Optimization with Cardinality-Aware Pareto Selection</a></td><td>42</td><td>1</td><td>LG</td><td>고정 개수 M개 해를 고르는 cardinality-aware 다목적 Bayesian optimization을 제안하고 regret bound를 증명함. 로봇 연결은 약함</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2611.20119'>CECAR: Cache &amp; Expert Co-Aware Routing Accelerates On-Device Inference of MoE LLMs</a></td><td>42</td><td>1</td><td>LG</td><td>MoE LLM의 on-device 추론에서 캐시와 expert 라우팅을 함께 고려해 4.5배 가속함. 시스템 최적화이고 로봇 연결은 약함</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2611.20937'>Learning What the True Labels Would Teach: Posterior Analytic Class-Incremental Learning with Unlabeled Data</a></td><td>42</td><td>1</td><td>CV</td><td>CLIP 기반 unlabeled class-incremental learning에서 label posterior를 soft label로 쓰는 PACIL을 제안함. 이론 증명은 있으나 분류 benchmark 개선임</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2611.21216'>MiSTiQ: MicroScaling Trellis Quantization for Extreme KV Cache Compression</a></td><td>42</td><td>1</td><td>LG</td><td>KV cache 양자화 개선임. 효율 추론이나 로봇 문제와 직접 연결 없음</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2611.19913'>The Vocabulary Tax: Safely Trimming Unused Tokens from LLMs for On-Device Use</a></td><td>42</td><td>1</td><td>LG</td><td>LLM vocabulary에서 안 쓰는 embedding 행을 BPE merge closure와 Good-Turing 인증서로 안전하게 제거함. on-device 효율화에 실용적이나 로봇과는 간접적임</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2611.19403'>Confidence Without Cause: Predicting and Localizing Physics-Shortcut Sensitivity in Language Model Hidden States</a></td><td>42</td><td>1</td><td>NLP</td><td>물리 문제에 무관한 distractor를 넣은 certified counterfactual 세트로 LLM hidden state probe의 민감도 예측과 attention head 위치 특정을 보임, 소규모 LLM 해석 연구이고 로보틱스 연결은 약함</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2611.20815'>ForeSay: Tell the Future in Words, Branch the Details in Noise for Precipitation Nowcasting</a></td><td>42</td><td>1</td><td>Video</td><td>강수 nowcasting에서 VLM이 텍스트로 거시 시나리오를 예측하고 Rectified Flow가 세부를 branch하는 ForeSay를 제안함, 앙상블 비용 절감 아이디어가 있으나 기상 도메인임</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2611.18916'>Simplify, Agree, Distill: Label-Free Self-Distillation with Stepping Stones</a></td><td>42</td><td>0</td><td>NLP</td><td>정답 없이 쉬운 관련 문제를 만들어 자기 증류하는 LLM 수학 추론 방법임</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2611.19649'>LoopFill: Pipelined Multi-Token Speculative Decoding for Looped Transformers</a></td><td>42</td><td>0</td><td>NLP</td><td>looped Transformer용 training-free speculative decoding으로 최대 5.85배 가속하나 LLM 디코딩 전용 engineering임</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2611.19692'>MathaMAGICal: Validating Trajectory Data Attribution During Capability Acquisition</a></td><td>42</td><td>0</td><td>LG</td><td>trajectory data attribution(MAGIC)이 짧은 checkpoint 구간에서만 재학습과 맞음을 검증하는 소규모 모델 분석임</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2611.19896'>LoopSkim: Lossless Multi-Depth Speculative Decoding for Looped Language Models</a></td><td>42</td><td>0</td><td>NLP</td><td>looped LM용 lossless speculative decoding으로 LoopSpec 대비 1.73배 가속을 보고함. 직전 LoopFill류와 같은 디코딩 engineering임</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2611.19925'>Learning When to Continue and When to Stop: Termination-Aware OPSD</a></td><td>42</td><td>0</td><td>NLP</td><td>OPSD의 종료 불일치를 진단하고 stop/continue distillation과 repetition unlikelihood를 추가함. 수학 추론 소규모 모델 개선이고 robotics 무관함</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2611.20258'>Microfitting: Continual Learning via Cached Test-Time Training</a></td><td>42</td><td>0</td><td>NLP</td><td>문서별 작은 adapter를 캐시하는 test-time training으로 enterprise Q&amp;A에서 상대 38.2% 개선함. LLM 기업 문서 응용이고 로봇 연결은 약함</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2611.20524'>GaugeRoPE: RoPE-Compatible Executable Latent Attention</a></td><td>42</td><td>0</td><td>NLP</td><td>RoPE와 호환되는 latent KV 표현으로 Mistral-7B에서 5.85배 압축과 2.48배 처리량을 얻음. LLM 추론 효율 연구임</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2611.20691'>SpeCal: Spectral Calibration for Unsupervised RLVR</a></td><td>42</td><td>0</td><td>NLP</td><td>hidden-state 스펙트럼으로 unsupervised RLVR 보상을 보정하는 SpeCal을 제안함. LLM reasoning 한정임</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2611.20156'>Risk-certified prompt optimization for LLM-as-a-judge guardrails</a></td><td>42</td><td>0</td><td>NLP</td><td>LLM judge guardrail prompt를 missed-attack 상한 인증 하에서 선택하는 CPS·CRISP를 제안함. 통계적 보증은 있으나 prompt 선택 수준이고 로봇과 무관함</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2611.21384'>Stability-Compensated Threshold Calibration for Selection-Conditioned Risk Control in Large Language Models</a></td><td>42</td><td>0</td><td>NLP</td><td>selective prediction에서 LEC 임계값 선택이 SCER 보장을 깨는 반례를 만들고 SC-LEC 인증서를 제시함. 이론 기여는 있으나 QA 한정이고 보수적임</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2611.19122'>Agent-Guided Process Verification for Mathematical Self-Correction</a></td><td>42</td><td>0</td><td>NLP</td><td>수학 풀이를 핵심 claim 단위로 검증하고 첫 오류 지점부터 재유도하는 AGPV로 평균 정확도를 13.5퍼센트포인트 올림. 오류 위치 검증 구조가 있으나 수학 추론 한정임</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2611.19292'>Zero-Shot Weight-Space Programming for Prediction and Classification of Target Variables in Structured Datasets</a></td><td>42</td><td>0</td><td>LG</td><td>LLM이 데이터셋을 보고 신경망 가중치를 직접 써서 선형 최적과 동등한 성능을 내는지 사전등록으로 검증함. 흥미로운 실험이나 표 데이터 소규모 문제임</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2611.20770'>Non-Imaging Optical Tactile Sensors for Robotics: Transduction Principles, System Integration, and Robotic Applications</a></td><td>40</td><td>6</td><td>Tactile</td><td>비이미징 광학 촉각 센서 survey임. 참고 자료 성격임</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2611.18982'>Robot Demonstration Videos Should Include Transparency Disclosures</a></td><td>40</td><td>5</td><td>Embodied AI</td><td>로봇 시연 영상 공개 시 투명성 공시를 주장하는 position paper임. 재현성 측면 의미는 있으나 기술 기여 없음</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2611.20075'>Prompt Re-Specification and Target-Mask Availability in Mask-Conditioned Visual Reinforcement Learning for Moving-Platform Landing</a></td><td>40</td><td>5</td><td>RL</td><td>이동 플랫폼 착륙 visual RL의 mask 조건과 prompt 재지정 분석임. 좁은 설정임</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2611.21311'>A2A-UAV: A Multimodal Air-to-Air Dataset for UAV Detection and Identification</a></td><td>40</td><td>3</td><td>CV</td><td>UAV 탐지용 공대공 다중 센서 데이터셋을 공개했으나 데이터 수집 기여에 그침</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2611.21530'>DuoFlow: Towards Synchronized Speech and Motion Generation with Fine-Grained Control</a></td><td>40</td><td>3</td><td>CV</td><td>음성과 모션을 동기 생성하는 dual-stream flow transformer와 benchmark이며 embodied speaker 쪽 응용임</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2611.20078'>Infrastructure-Based Multi-Agent Reinforcement Learning with Attention for Highway Ramp Merging</a></td><td>40</td><td>3</td><td>RL</td><td>고속도로 합류용 attention MARL 제어기로 SUMO에서 세 baseline보다 우수함. 인프라 중앙 제어이고 incremental 응용임</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2611.20574'>ExtremeDrive: A Real-World Dataset and Benchmark for Critical Driving</a></td><td>40</td><td>3</td><td>Autonomous Driving</td><td>극한 주행 데이터셋과 benchmark임. 데이터 기여 중심임</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2611.21069'>CoopDistill: Equilibrium-Guided Multi-Agent Policy Distillation for Cooperative Driving</a></td><td>40</td><td>3</td><td>Autonomous Driving</td><td>협력 주행 policy distillation임. 도메인 특화임</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2611.20207'>AstroPIE-53: Towards Understanding Failure Modes of Human Pose Estimation in Space</a></td><td>40</td><td>2</td><td>CV</td><td>우주 인간 포즈 추정 실패 모드 분석으로 진단 성격이 있으나 도메인 특화임</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2611.20283'>CiGS: Conduction in Gaussian Splats for Interior Temperature Field from Thermal Images</a></td><td>40</td><td>2</td><td>3D Vision</td><td>Gaussian splat에 열전도를 결합한 내부 온도장 추정으로 새 표현이나 niche함</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2611.20321'>Unreasonable Confidence from Simulator Misspecification: Directional Robustness on the SPEED+ Sim-to-Real Benchmark</a></td><td>40</td><td>2</td><td>CV</td><td>우주 pose sim-to-real 시뮬레이터 오지정 신뢰도 분석으로 우주 특화임</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2611.20786'>ThermoSight: From Appearance to Internal Thermofluid Fields via Physics-Guided Neural Reconstruction</a></td><td>40</td><td>2</td><td>3D Vision</td><td>외형에서 내부 열유동장을 복원하는 physics-guided neural 재구성으로 niche함</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2611.18654'>Earth World Model: Physics-constrained latent dynamics for forecasting and environmental scenario analysis</a></td><td>40</td><td>2</td><td>World Model</td><td>태양광과 풍력 예측용 물리 제약 latent world model로 개입 응답 충실도를 따로 평가하나 로봇과 거리가 멂</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2611.20811'>Auditing World-Model Explanations in Retail Forecasting: Faithfulness, Accuracy and Price Response</a></td><td>40</td><td>2</td><td>World Model</td><td>소매 예측 world model의 설명 신뢰도를 8개 점검으로 감사해 lift가 1.33-1.40배 과대 추정됨을 보임. 도메인이 소매이고 world model은 이름만 공유함</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2611.18624'>Skill Transfer: Adapting Agent Skills from Strong to Weak Agents</a></td><td>40</td><td>2</td><td>NLP</td><td>강한 agent의 skill을 약한 agent로 이전함. skill 개념은 유사하나 언어 agent임</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2611.20145'>Rank, Don&#x27;t Regress: A 279M Text Ranker Beats 2B and 7B VLMs on Referential Urdu GUI Grounding</a></td><td>40</td><td>2</td><td>NLP</td><td>coordinate 회귀 대신 DOM 후보를 고르는 279M cross-encoder로 우르두어 GUI grounding에서 VLM을 앞섬. 좁은 언어·도메인 설정이며 GUI 에이전트와 약하게 연결됨</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2611.20771'>Nemotron 3.5 Bolt E4B 4GB: An Open and Efficient Small Language Model for Fast Conversational Agents</a></td><td>40</td><td>2</td><td>NLP</td><td>Gemma-4-E4B를 post-training한 소형 대화 agent 모델 Nemotron Bolt를 공개함. 로봇·Jetson 인터페이스를 언급하나 모델 릴리스 보고서임</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2611.20144'>HEAMS: Holistic Evaluation of Agent Memory Systems</a></td><td>40</td><td>2</td><td>LLM Agent</td><td>agent memory 시스템을 성능뿐 아니라 보안, 프라이버시, 사용자 주권으로 평가하는 HEAMS 벤치마크를 제안함, 평가 틀 기여이며 로봇 memory와는 간접 연결임</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2611.20844'>DetourBench: Trajectory-Level Evaluation of Interactive Agents with Exact Minimum-Action Bounds</a></td><td>40</td><td>2</td><td>LLM Agent</td><td>부분 관측 전이계에서 최소 행동 수를 정확히 계산해 agent 경로 효율을 재는 DetourBench를 제안함, 25개 과제 규모이고 텍스트 환경 평가임</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2611.18692'>Beyond Raw Similarity: Prior-Aware Fusion for Out-of-Distribution Detection</a></td><td>40</td><td>1</td><td>Multimodal</td><td>VLM OOD 검출 fusion 개선으로 incremental함</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2611.18735'>AITHER: Authority-Informed Evidence Routing for Mixed-Authority Vision-Language Reasoning</a></td><td>40</td><td>1</td><td>Multimodal</td><td>혼합 권한 입력 증거 라우팅으로 VLM reasoning 제어이며 로봇 연결 약함</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2611.18750'>Feature-Space Latent Forecasting for Endoscopic Surgical Video Understanding</a></td><td>40</td><td>1</td><td>Video</td><td>수술 영상 feature-space 예측으로 도메인 특화임</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2611.19786'>Fine-Grained RLAIF for Visual Safety: Learning to Zoom into Hazards for Multimodal Safety Alignment</a></td><td>40</td><td>1</td><td>Multimodal</td><td>시각 안전 정렬 fine-grained RLAIF로 VLM 안전 incremental함</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2611.20461'>LiveView: Real-Time Camera-Controlled Re-filming of Streaming Videos</a></td><td>40</td><td>1</td><td>Video</td><td>스트리밍 영상 실시간 camera-controlled re-filming으로 생성 응용임</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2611.20885'>ProSE: Probing Reconstruction Error for Semantic-guided Expert Skipping in MoE-MLLMs</a></td><td>40</td><td>1</td><td>Multimodal</td><td>MoE-MLLM expert skipping으로 efficient inference이나 로봇 연결 약함</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2611.21363'>Symmetry Detection with Patch Embedding Models by Means of a Scalar Product Transform</a></td><td>40</td><td>1</td><td>CV</td><td>사전학습 patch embedding의 내적으로 대칭을 검출하는 학습 불필요 방법이나 활용 범위가 좁음</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2611.21459'>Balanced Twin Weight Factorization for Efficient MLLMs</a></td><td>40</td><td>1</td><td>LG</td><td>공유 basis weight factorization으로 MLLM 지연을 줄이는 압축 방법이며 일반 효율화 수준의 개선임</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2611.18856'>Self-Improvement Memory Enables Continual Recursive Self-Improvement</a></td><td>40</td><td>1</td><td>NLP</td><td>harness 최적화기에 편집 이력을 기록하는 memory를 붙인 continual self-improvement 연구임</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2611.19658'>Mesoscale Neural Operators: Learning Nonlinear Constitutive Laws from Molecular Dynamics for Scalable Fracture Predictions</a></td><td>40</td><td>1</td><td>LG</td><td>MD 데이터에서 nonlocal 구성 법칙을 학습하는 neural operator로 물리 일관성은 있으나 재료 파괴 도메인 한정임</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2611.20441'>Abstention Direction in Large Language Models: Mechanistic Interpretability of Abstention Across Query Ambiguity, Knowledge Limits, and Safety Alignment</a></td><td>40</td><td>1</td><td>NLP</td><td>abstention을 모호성·지식 한계·안전 세 관점에서 counterfactual pair로 방향 추출하고 steering함. 방향이 공유됨을 보이나 refusal direction 확장 수준임</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2611.20733'>MemEmo: Evaluating Emotion in Memory Systems</a></td><td>40</td><td>1</td><td>NLP</td><td>memory system의 감정 정보 처리를 4개 차원으로 평가하는 MemEmo benchmark를 만듦. memory 평가이나 대화 감정 도메인 한정임</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2611.20755'>GPRM: Global Perspective Process Reward Model</a></td><td>40</td><td>1</td><td>NLP</td><td>과거·미래 step까지 보는 process reward model GPRM으로 PRMBench에서 7.8점 개선함. 소규모 데이터로 baseline을 앞서나 PRM 개선 수준임</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2611.21152'>From Repositories to Training Environments: Scaling Long-Horizon Coding Agents with Environment Evolution Loop</a></td><td>40</td><td>1</td><td>NLP</td><td>저장소를 검증 가능한 환경으로 바꾸고 proxy 피드백으로 진화시키는 RepoFactory로 환경 10,159개를 만듦. 환경 합성 scale-up이며 코딩 한정임</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2611.21211'>Teaching Language Models to Adapt Answer Granularity to Their Confidence</a></td><td>40</td><td>1</td><td>NLP</td><td>모델이 confidence에 따라 답변 granularity를 조절하도록 consistency 기반 supervision으로 학습함. 불확실성 처리 아이디어가 있으나 시간·지리 질문 한정이고 이득이 모델별로 다름</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2611.21449'>Replicating and Extending Weight-Space Programming: Frontier LLMs Compile Programs into Weights and Read Input Layers</a></td><td>40</td><td>1</td><td>LG</td><td>frontier LLM이 작은 신경망 가중치를 직접 작성·판독하는 MIT 결과를 재현하고 확장함. 가중치 감사가 얕다는 한계를 보이며 재현 연구 성격이 강함</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2611.18963'>SpecRelay: Amortize or Avoid the Round Trip in Edge-Cloud Speculative Decoding</a></td><td>40</td><td>1</td><td>LG</td><td>edge-cloud speculative decoding의 round trip을 비동기 검증과 router로 줄이는 SpecRelay를 제안함. 시스템 최적화이고 throughput 최대 1.95배이며 로봇 관련성은 간접적임</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2611.19841'>Asking the right question is key to AI discovery in a chain of hypotheses</a></td><td>40</td><td>1</td><td>LLM Agent</td><td>AI scientist가 모델 불일치 위치만 탐색해 좁은 peak를 놓치는 능동 탐색 실패를 32회 trial로 보임, active exploration 관점은 흥미로우나 물리 실험 한정임</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2611.20488'>EVIDENT: Evaluating Evidence Grounding in GUI Agents</a></td><td>40</td><td>1</td><td>Multimodal</td><td>GUI agent가 웹 증거에 근거해 답했는지 TSR, ESR, GSR로 분리 평가하는 EVIDENT 220개 과제를 제안함, 벤치마크이며 로보틱스와 거리가 있음</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2611.20736'>GainCtrl: Predicting Remaining Gains for Efficient LLM Agent Execution</a></td><td>40</td><td>1</td><td>LLM Agent</td><td>Best-of-N agent 실행에서 남은 이득을 CPU predictor로 예측해 중단 시점을 정하는 GainCtrl을 제안함, trajectory replay 기반 비용 절감이며 로보틱스와 거리가 있음</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2611.21020'>SWE-OPD: On-Policy Distillation for Agentic Coding</a></td><td>40</td><td>1</td><td>LLM Agent</td><td>대형 teacher에서 소형 student로 coding agent 능력을 on-policy distillation하는 SWE-OPD를 연구함, SWE-bench Pro 35.9%에서 39.4%로 오르는 incremental 결과임</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2611.18727'>Latent Fusion: Channel Stacking for Structure-Preserving Image Editing</a></td><td>40</td><td>0</td><td>Generative</td><td>이미지 편집 conditioning 방식 channel stacking으로 incremental함</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2611.18849'>Scaling Channel-Adaptive Self-Supervised Learning</a></td><td>40</td><td>0</td><td>CV</td><td>채널 적응 SSL scale-up으로 현미경 등 특화임</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2611.20478'>Beyond Seeing: Fine-Grained Preference Validation and Severity-Aware Alignment for Mitigating Visual Hallucinations in Vision-Language Models</a></td><td>40</td><td>0</td><td>Multimodal</td><td>LVLM hallucination preference 정렬로 incremental함</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2611.19768'>PISG: Constraint-Aligned Signal Amplification for Diffusion-Based Combinatorial Optimization</a></td><td>40</td><td>0</td><td>LG</td><td>diffusion 기반 조합 최적화(TSP, MIS)에 training-free guidance를 추가해 약간 개선함. 작은 module 수준임</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2611.19848'>A phase diagram for training and inference in language models</a></td><td>40</td><td>0</td><td>LG</td><td>언어 모델 표현 기하를 phase diagram으로 분석함. 해석 관점은 새로우나 robotics와 무관함</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2611.20403'>Attention Sinks as Spectral Spikes: A Mechanism Analysis of Gated Attention</a></td><td>40</td><td>0</td><td>LG</td><td>gated attention이 attention sink를 spectral mode 수축으로 줄이는 메커니즘을 분석함. robotics 무관함</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2611.20549'>RoShift: Lazy Shift and Weight-aware Rotation for Activation Sparsity in LLM Inference</a></td><td>40</td><td>0</td><td>NLP</td><td>SiLU LLM에 lazy shift와 rotation으로 활성 희소성을 높여 1.72배 가속함. 추론 효율 engineering임</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2611.20635'>Contrastive Activation-Guided Zeroth-Order Preference Optimisation for Memory-Efficient LLM Alignment</a></td><td>40</td><td>0</td><td>NLP</td><td>chosen과 rejected의 activation 차이로 zeroth-order DPO 부분공간을 만들어 메모리를 59% 줄임. 소형 모델 정렬 연구임</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2611.20687'>Rethinking Supervision Scaling in On-Policy Distillation: From Dense Supervision to Stochastic Horizons</a></td><td>40</td><td>0</td><td>NLP</td><td>on-policy distillation의 rollout horizon을 무작위로 바꿔 비용을 45%로 줄임. LLM 학습 효율 연구임</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2611.20608'>Same Papers, Different Verdicts: Tracing Version Drift in LLM Peer Review</a></td><td>40</td><td>0</td><td>NLP</td><td>LLM 논문 심사 점수가 모델 버전에 따라 크게 달라짐을 ICLR 제출본으로 측정함. 흥미로운 감사 연구이나 로봇과 무관함</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2611.19214'>STaSBO: LLM-Guided Strategy Planning and Configuration Selection for Bayesian Optimization</a></td><td>40</td><td>0</td><td>LG</td><td>LLM 메타 컨트롤러가 Bayesian optimization의 surrogate-acquisition 설정을 선택하는 STaSBO를 제안함. 22개 task 평균 순위가 1위이나 BO 하이퍼 설정 수준임</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2611.19413'>PMR: MoE Routing with Shared Prototypes and Congestion Pricing</a></td><td>40</td><td>0</td><td>LG</td><td>MoE 라우팅을 prototype과 congestion price로 분리한 PMR을 제안함, 0.4~1.2B 사전학습 소규모 이득이며 로보틱스와 무관함</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2611.18935'>Optimal Operating-Point Selection for Single-Linearization Trajectory Planning of Nonlinear Robot Manipulators</a></td><td>38</td><td>5</td><td>Control</td><td>단일 선형화 궤적 계획의 operating point 선택임. 고전 최적화 중심임</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2611.19535'>Cooperative Gradient Estimation for Multi-Robot Source Seeking with Heteroskedastic Measurements</a></td><td>38</td><td>4</td><td>Multi-robot</td><td>이질 측정 잡음 하 multi-robot source seeking의 협력 gradient 추정임. 고전 제어 중심임</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2611.19731'>Cooperative Transport of Unknown Objects by Distributed Effort Regulation in Multi-agent Systems</a></td><td>38</td><td>4</td><td>Multi-robot</td><td>미지 물체의 분산 협력 운반 전략임. 고전 제어 중심임</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2611.19785'>DynLimit: A Simulation Benchmark for Dynamics-Critical Planning and Control</a></td><td>38</td><td>4</td><td>Benchmark</td><td>차량 한계 주행용 시뮬레이션 benchmark임. 요청, 실행, 완료를 분리 평가하나 로봇 학습과 거리 있음</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2611.20324'>High-Speed Forward and Reverse Tractor-Trailer Driving with Learned Vehicle Dynamics</a></td><td>38</td><td>4</td><td>Control</td><td>학습된 동역학으로 트랙터-트레일러 주행을 함. 도메인 특화임</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2611.21309'>Safe Physical Interaction of All-Electric Heavy-Duty Robotic Manipulators via Control Barrier Functions and Variable Impedance Control</a></td><td>38</td><td>4</td><td>Control</td><td>중장비 로봇 CBF와 variable impedance 안전 상호작용임. 고전 제어 중심임</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2611.19387'>Long-Horizon Causal Inertial Odometry in Multistory Buildings</a></td><td>38</td><td>3</td><td>Localization</td><td>다층 건물의 장기 inertial odometry임. 로봇 학습과 연결 약함</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2611.19172'>EviRef: Evidence-Specific Memories for Logical Anomaly Detection across Capture Conditions</a></td><td>38</td><td>2</td><td>CV</td><td>논리적 이상 검출용 evidence memory로 산업 검사 응용임</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2611.19493'>Beyond Paired Inputs: Learning to Leverage RGB-T Cross-Modal Relations in Multimodal Large Language Models</a></td><td>38</td><td>2</td><td>Multimodal</td><td>RGB-열화상 MLLM cross-modal 관계 학습으로 응용 위주임</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2611.18637'>ReVision: Selective Intrinsic Reasoning for Tool-Augmented, Reasoning-Intensive VQA</a></td><td>38</td><td>2</td><td>Multimodal</td><td>도구 증강 VQA에서 선택적 내재 추론을 함. multimodal 추론이나 로봇 연결 약함</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2611.19359'>One Run Is Not Enough: Reminding a small Gemma 4 coding agent of its last finding made no measurable difference in a paired test</a></td><td>38</td><td>2</td><td>NLP</td><td>coding agent에 마지막 발견을 다시 주입하는 memory의 효과가 98쌍 paired test에서 없었다는 null 결과 보고임, 엄밀하나 기여가 부정적 결과이며 소형 모델 한정임</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2611.20573'>Dynamic Shaping: Acquiring Interfaces and Constructing Execution over Frozen Pretrained Components</a></td><td>38</td><td>2</td><td>RL</td><td>고정된 사전학습 컴포넌트를 rebind하는 Dynamic Shaping을 제안함, ViZDoom Basic 단일 환경 검증이며 일반성 근거가 약함</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2611.18732'>ShiftGuard: Evaluating Confidence and Feature Distance for Risk-Controlled Image Classification</a></td><td>38</td><td>1</td><td>CV</td><td>분류기 abstention 점수 비교로 risk control이나 일반 분류임</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2611.18894'>CISyn: Human Mesh Recovery in Close Interactions with Physics-Simulated Synthetic Data</a></td><td>38</td><td>1</td><td>3D Vision</td><td>근접 상호작용 HMR 합성 데이터로 physics 시뮬레이션 활용이나 데이터셋 중심임</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2611.19261'>dit.xpu : Taming DiT Sparse Inference on Mobile SoCs</a></td><td>38</td><td>1</td><td>Generative</td><td>모바일 SoC DiT sparse 추론 최적화로 시스템 엔지니어링임</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2611.20619'>From Joint Risk to Decision Invariance: Decision-Preserving Regularization for Exemplar-Free Class-Incremental Learning</a></td><td>38</td><td>1</td><td>LG</td><td>exemplar-free class-incremental 정규화로 continual learning incremental함</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2611.21292'>AnachroBench: Evaluating Historical Consistency in Large Vision-Language Models</a></td><td>38</td><td>1</td><td>Multimodal</td><td>역사 시대 일관성을 보는 LVLM benchmark를 제안했으나 로봇과 거리가 멀고 benchmark 기여에 그침</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2611.18638'>GRAFT: Cross-Backbone LoRA Reuse for Continual Language and Multimodal Learning</a></td><td>38</td><td>1</td><td>Multimodal</td><td>LLM LoRA를 선형 bridge로 VLM backbone에 옮기는 방법이나 개선 폭과 범위가 작음</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2611.20818'>Tight PAC-Bayes Generalisation Guarantees for Large Language Model Judges</a></td><td>38</td><td>1</td><td>NLP</td><td>LLM 안전 판정기에 compression 기반 PAC-Bayes certificate를 적용하고 LoRA-GT를 제안함. 안전 oversight 이론이고 로봇과는 거리 있음</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2611.21268'>In-Context Estimation and Prediction for Parametric ODEs</a></td><td>38</td><td>1</td><td>LG</td><td>parametric ODE에 대한 in-context 추정 연구임. 로봇 연결 약함</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2611.21538'>Optimistic Verifiers Get Hacked: Reward Hacking Under an Exact Process Oracle</a></td><td>38</td><td>1</td><td>RL</td><td>정확한 process oracle에서도 optimistic verifier가 reward hacking됨을 분석함. 이론 중심이며 로봇과 거리 있음</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2611.19960'>Anatomy of an Agent Harness: Decisions, Invariants and Corner Cases</a></td><td>38</td><td>1</td><td>NLP</td><td>agent harness 설계 결정 30개를 invariant와 테스트로 정리함. 저자 본인 시스템 위주의 소프트웨어 공학 문서이며 실험 근거가 약함</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2611.20976'>Living Context Graphs: Continual Semantic Learning for Enterprise Data Reasoning</a></td><td>38</td><td>1</td><td>NLP</td><td>enterprise 데이터용 context graph를 지속 학습해 text-to-SQL held-out 정확도를 22.6점 올림. continual learning 설정이나 SQL 도메인 한정임</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2611.18905'>Ask Precisely, Assume Wisely: Interactive Evaluation of Ambiguity Resolution in Large Language Models</a></td><td>38</td><td>1</td><td>NLP</td><td>모호성 해소를 선호 기반 simulated user로 평가하고 불만 신호로 prompt를 최적화함. HRI 관련 질의 전략이나 텍스트 평가임</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2611.20049'>The Frontier Must Grow - Self-proposed, interpreter-labelled training roughly doubles a 4B model&#x27;s accuracy on a fresh exam as its verified frontier grows</a></td><td>38</td><td>1</td><td>LLM</td><td>Qwen3-4B가 Lua 프로그램을 스스로 제안하고 인터프리터로 라벨링해 학습하는 루프를 시험함, 정확도 8.3%에서 16.7%로 오르나 base 제안 데이터 대비 이득이 불확실함</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2611.20688'>VIVID: A Visual Harness for Agentic Video Editing</a></td><td>38</td><td>1</td><td>Video</td><td>coding agent에 영상 검사와 오디오 분석 도구를 붙인 visual harness VIVID를 제안함, Codex 평균 점수가 38.4%에서 58.6%로 오르나 영상 편집 응용임</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2611.21072'>Sage S2.1 Flash Technical Report</a></td><td>38</td><td>1</td><td>Multimodal</td><td>분자 그래프와 스펙트럼 encoder를 붙인 320B MoE 과학 agent 모델 기술 보고서임, OSWorld 등 GUI 결과는 있으나 로보틱스와 무관함</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2611.18678'>Not All Steps Matter: Temporally Adaptive Spectral Control for Concept Removal in Diffusion Models</a></td><td>38</td><td>0</td><td>Generative</td><td>diffusion 개념 제거 spectral 제어로 incremental함</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2611.19009'>Role-Separated Diffusion Transformers: Global Rule Isolation and Deterministic Sampling Manifold Compression</a></td><td>38</td><td>0</td><td>Generative</td><td>diffusion transformer 구조 변경으로 이미지 생성 중심임</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2611.20021'>FastGRN: Few-Step Generative Refinement Networks</a></td><td>38</td><td>0</td><td>Generative</td><td>GRN few-step화로 이미지 생성 가속이며 무관함</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2611.20307'>PoCoAttn: Position-Content Collaborative Sparse Attention for Fast and High-Fidelity Video Generation</a></td><td>38</td><td>0</td><td>Video</td><td>video DiT sparse attention 가속으로 로봇 무관함</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2611.21440'>[CLS] and [EOS] Tokens are not Enough for CLIP-based Class-Incremental Learning</a></td><td>38</td><td>0</td><td>CV</td><td>CLIP class-incremental learning에서 patch와 token 단위 특징을 쓰는 소폭 개선 방법임</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2611.18974'>Bilateral Log-Linear Attention</a></td><td>38</td><td>0</td><td>LG</td><td>log-linear attention에 원점 기준 계층을 더해 recall을 높인 효율적 attention 변형임</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2611.19794'>Eliciting Research Taste in LLMs through Future Research Direction Choice</a></td><td>38</td><td>0</td><td>NLP</td><td>LLM의 research taste를 80개 쌍 비교로 측정하는 소규모 평가이고 robotics와 무관함</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2611.20064'>Decode Early, Verify Late: Streaming Offline Speech Recognizers Without Accuracy Loss</a></td><td>38</td><td>0</td><td>Speech</td><td>ASR 스트리밍을 draft와 turn-end 검증으로 offline 출력과 동일하게 유지함. 음성 서빙 engineering임</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2611.20174'>Weights &amp; Caches: LLMs Can Program Tabular Foundation Models</a></td><td>38</td><td>0</td><td>LG</td><td>LLM이 tabular foundation model의 가중치와 KV cache를 직접 프로그래밍함. 아이디어는 신선하나 tabular 한정이고 robotics 무관함</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2611.20288'>Protecting Safety during Reasoning Training with Low-Rank Fisher Regularisation</a></td><td>38</td><td>0</td><td>NLP</td><td>safety subspace로 투영한 EWC(SP-EWC)로 reasoning fine-tuning 중 안전성을 유지함. LLM 안전성 연구임</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2611.20331'>LENS: Replacing LayerNorm and Softmax in Transformers with Learnable Normalization States</a></td><td>38</td><td>0</td><td>LG</td><td>LayerNorm과 Softmax를 작은 MLP로 대체해 GEMM 친화적으로 만듦. 성능은 대체로 유지되는 수준이고 하드웨어 지향임</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2611.20384'>JointQ: Joint Scale-and-Integer Quantization for Large Language Models</a></td><td>38</td><td>0</td><td>NLP</td><td>GPTQ에 scale과 정수를 함께 최적화하는 JointQ를 더해 저비트 정확도를 개선함. 양자화 solver의 incremental 개선임</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2611.20562'>One-Shot Calibration via Model Editing</a></td><td>38</td><td>0</td><td>NLP</td><td>사용자 응답의 불확실성을 쓰는 model editor SoftEdit으로 one-shot calibration을 함. LLM과 VLM 편집 연구임</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2611.21251'>The Price of Choosing Examples: Context Overfitting in Adaptive In-Context Learning</a></td><td>38</td><td>0</td><td>LG</td><td>adaptive in-context learning의 과적합 이론임. 로봇 연결 약함</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2611.21285'>The Price of Not Planning: Parallel Sampling Depth Peaks at the Reconstruction Threshold</a></td><td>38</td><td>0</td><td>LG</td><td>masked diffusion의 plan 기반 병렬 샘플링 이론임. 로봇 연결 약함</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2611.21307'>Programmable Semantic Interventions: Learning Causal Carriers from Behavioral Programs</a></td><td>38</td><td>0</td><td>LG</td><td>causal abstraction 정렬을 위한 행동 프로그램 학습임. 로봇과 거리 있음</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2611.19636'>ROUNDS: Source-Framed Diagnostic Revision after Multi-Turn Clinical Evidence</a></td><td>38</td><td>0</td><td>NLP</td><td>다중 턴 임상 증거에서 LLM 진단이 외부 의견에 흔들리는 정도를 재는 평가 프레임워크임. 의료 평가이며 방법론 기여는 작음</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2611.20674'>LEAF-OPD: Learning to Forget from Privileged Contexts via On-Policy Distillation</a></td><td>38</td><td>0</td><td>NLP</td><td>privileged context를 teacher로 쓰는 on-policy distillation으로 LLM unlearning을 수행함. TOFU·RWKU 개선이나 로봇과 무관함</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2611.21095'>SWE-WhatIf: Simulating Real Users of Coding Agents from Recorded Session</a></td><td>38</td><td>0</td><td>NLP</td><td>녹화된 coding agent 세션의 사용자 의도를 모델링해 simulator로 재생하는 SWE-WhatIf를 제안함. 사용자 시뮬레이션 평가이며 코딩 도메인임</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2611.19108'>Guiding AI Agents to Generate Conjectures by Encoding How Theorems Build on One Another</a></td><td>38</td><td>0</td><td>AI</td><td>정리 간 발전 관계를 Theorem Evolution Graph로 인코딩해 conjecture를 생성함. 평가가 LLM judge와 전문가 선호에 의존하고 plausibility는 baseline이 앞섬</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2611.19115'>Learning inadequacy of Bayesian neural operators for PDE-constrained inference and design</a></td><td>38</td><td>0</td><td>LG</td><td>PDE 잔차 오차 추정으로 operator inadequacy를 학습하는 RI-BNO를 제안함. 시뮬레이션 수를 절반으로 줄이는 과학 계산 ML이며 로봇과 간접적임</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2611.19230'>CompoundingKernel: Self-Improving from Zero to First</a></td><td>38</td><td>0</td><td>LG</td><td>agent가 GPU kernel을 search로 작성하는 CompoundingKernel이 SOL-ExecBench 1위를 기록함. 코드 생성 시스템이며 로봇과 무관함</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2611.20616'>GEAR$^2$: Pruned Experts Live On through Gated Reuse of Activated Experts and a Missing-Mass Residual</a></td><td>38</td><td>0</td><td>LLM Efficiency</td><td>pruned MoE expert를 남은 expert 출력의 gated reuse와 잔차로 복원하는 GEAR를 제안함, 최대 2.75pp 개선의 incremental 기여이며 로보틱스와 무관함</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2611.20891'>From Recursion to Convolution: Parallel Self-Improvement for Multi-Agent Systems</a></td><td>38</td><td>0</td><td>LLM Agent</td><td>multi-agent self-improvement를 latent 공간 convolution으로 병렬화하는 ConvRSI를 제안함, MATH-500 한정 효율 개선이며 로보틱스와 무관함</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2611.21250'>Stream of Belief: Eliciting Collective Intelligence through Latent Belief Dynamics</a></td><td>38</td><td>0</td><td>LLM Agent</td><td>multi-agent 추론을 latent 믿음 동역학의 균형으로 보는 Stream of Belief를 제안함, 설명과 근거가 초록에 부족하고 로보틱스와 무관함</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2611.21232'>A Generative AI-Driven Architecture for Whole-Home Intelligent Services: Edge Models, Memory Management, and Household Applications</a></td><td>36</td><td>3</td><td>Embodied AI</td><td>홈 로컬 서버 중심 생성형 AI 가정 서비스 설계 survey와 5차원 평가 틀을 제안함. 물리 행동 안전을 다루나 실험 없는 review임</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2611.18733'>LiNO: Lightweight Network for Occupancy Estimation</a></td><td>36</td><td>2</td><td>3D Vision</td><td>경량 occupancy 추정으로 incremental함</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2611.18880'>RAVEN-Bench: A Paired EO-IR Video QA Benchmark for Aerial Multimodal Understanding</a></td><td>36</td><td>2</td><td>Multimodal</td><td>항공 EO-IR 영상 QA 벤치마크로 데이터셋 기여임</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2611.19381'>AcousticBEV: Acoustic BEV Object Localization for Intelligent Vehicles</a></td><td>36</td><td>2</td><td>3D Vision</td><td>음향 BEV 객체 위치 추정으로 새 센서이나 niche함</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2611.20203'>Radar Panoptic Transformer: Semantic-Guided Mask Queries for Dynamic Scene Understanding</a></td><td>36</td><td>2</td><td>3D Vision</td><td>레이더 panoptic transformer로 센서 특화 incremental함</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2611.21438'>Power Line Detection in Point Clouds with Point-SAM and RANSAC</a></td><td>36</td><td>2</td><td>3D Vision</td><td>항공 LiDAR 전선 검출에 Point-SAM과 3D catenary RANSAC을 적용하고 데이터셋을 공개한 응용 연구임</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2611.19836'>AGPF: Dynamic Source Selection for Feature Pyramid Fusion</a></td><td>36</td><td>1</td><td>CV</td><td>feature pyramid 동적 source 선택으로 incremental함</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2611.19812'>Reasoning in the loop: antibody lead optimization by probing mechanism and measurement</a></td><td>36</td><td>1</td><td>LG</td><td>Claude agent가 항체 lead 최적화 캠페인에서 측정 metric 문제를 찾아냄. 바이오 사례 보고이고 robotics와 무관함</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2611.21372'>Learning What Pairs Miss for Higher-Order Multimodal Alignment</a></td><td>36</td><td>1</td><td>Multimodal</td><td>고차 multimodal contrastive 정렬 개선임. 로봇 연결 약함</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2611.19199'>What Moves a LoCoMo Score? Memory Context, Answer Prompts and Judges</a></td><td>36</td><td>1</td><td>NLP</td><td>LoCoMo 점수가 judge와 answer prompt에 따라 최대 7~9점 움직임을 측정함. memory benchmark 신뢰성 점검이나 한 시스템 평가임</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2611.19237'>Auditable Authorization for LLM Agents: Empirical Evidence Across Model, Harness, and Workflow Layers</a></td><td>36</td><td>1</td><td>AI</td><td>LLM agent 사람 승인 흐름에서 거부 안전성과 완결성을 감사해 일부 승인 누락을 발견함. 안전 감사 연구이며 소프트웨어 workflow 한정임</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2611.18740'>TyphoonWorld: A Residual Token World Model for Probabilistic Forecasting of Typhoon Imagery</a></td><td>36</td><td>0</td><td>World Model</td><td>태풍 위성영상 token world model로 도메인 특화임</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2611.18822'>LongCat-Video-Avatar 1.6 Technical Report</a></td><td>36</td><td>0</td><td>Video</td><td>아바타 영상 생성 기술 보고서로 로봇 무관함</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2611.19427'>Memorization Lives in a Few Attention Heads: Mitigating Memorization in Diffusion Models via Projection-Based Suppression</a></td><td>36</td><td>0</td><td>Generative</td><td>diffusion 암기를 attention head 투영으로 완화하나 로봇 무관함</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2611.19827'>When Does Reusing Layers Help Multimodal Embeddings?</a></td><td>36</td><td>0</td><td>Multimodal</td><td>멀티모달 임베딩 layer 재사용 실험으로 검색 중심임</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2611.19933'>SAGE-VQA: A Training-Free, Self-Evolving Agentic Framework with Grounded Evidence for Knowledge-Based Visual Question Answering</a></td><td>36</td><td>0</td><td>Multimodal</td><td>training-free agentic KB-VQA로 incremental함</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2611.20351'>BlockAlign: Preference Optimization for Trajectory-Distilled Video Generation</a></td><td>36</td><td>0</td><td>Video</td><td>few-step video 생성 preference 최적화로 incremental함</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2611.20653'>RAMP: Rethinking Multimodal Evaluation through Answer Readout Protocols</a></td><td>36</td><td>0</td><td>Multimodal</td><td>MLLM 평가 answer readout protocol 분석으로 평가 방법론임</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2611.21038'>ScoutCache: Efficient Few-Step Autoregressive Video Diffusion via Conditional Readout and Selective Caching</a></td><td>36</td><td>0</td><td>Video</td><td>few-step autoregressive video diffusion 캐싱으로 가속 위주임</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2611.21373'>WeVisForensics: Self-Evolving Agent for Omni AI-Generated Video Detection</a></td><td>36</td><td>0</td><td>Video</td><td>AI 생성 영상 탐지를 위한 self-evolving 에이전트로 forensic 분야에 한정됨</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2611.18641'>HIMX: mixed-format matrix multiplication based on customized HIFLOAT4 representations</a></td><td>36</td><td>0</td><td>LG</td><td>HiFloat4 혼합 mantissa로 W4A4 LLM 양자화 손실을 줄이는 하드웨어 지향 소폭 개선임</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2611.19127'>Empowering Masked Diffusion Models to Self-Correct with Leave-One-Out Transformers</a></td><td>36</td><td>0</td><td>NLP</td><td>hollow transformer 구조로 masked diffusion LM의 자기 수정을 가능하게 한 언어 모델 연구임</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2611.20371'>Pretty Linear Liars: Unregularized Probes Favor Intervention-Unfaithful Features</a></td><td>36</td><td>0</td><td>LG</td><td>선형 probe 정규화가 intervention faithfulness에 미치는 영향을 이론과 Llama-2-7B로 분석함. 해석성 연구이고 robotics 무관함</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2611.20565'>Memory-Efficient Speculative Decoding with Quantized Draft KV Cache</a></td><td>36</td><td>0</td><td>NLP</td><td>speculative decoding의 draft KV cache를 K4V4로 양자화해 draft 메모리를 66.20% 줄임. 소규모 engineering임</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2611.20003'>The novelty exposed: ablation, reproducibility and transparency in 40 technical reports of open-weight large language models (LLMs)</a></td><td>36</td><td>0</td><td>NLP</td><td>LLM 기술 보고서 40편의 ablation·재현성 공개 수준을 조사함. 메타 연구로 유용하나 로봇과 무관함</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2611.20191'>Do We Still Need Fine-Tuned Classifiers? Swapping Typed Decision Models into 24 ACL-Venue Papers</a></td><td>36</td><td>0</td><td>NLP</td><td>typed decision model로 ACL 논문 24편의 fine-tuned classifier를 대체할 수 있는지 조사함. 특정 제품 평가 성격이 강하고 로봇과 무관함</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2611.20415'>Augmenting Pretrained Language Models with N-gram Embeddings through Incremental Training</a></td><td>36</td><td>0</td><td>NLP</td><td>n-gram embedding을 기존 LLM에 incremental training으로 붙이는 설정을 탐색함. 설정 탐색 위주이며 기여가 작음</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2611.21519'>Embedding Cosine Measures Text Length Before It Measures Homogenization</a></td><td>36</td><td>0</td><td>NLP</td><td>embedding cosine 동질화 지표가 텍스트 길이를 재는 것임을 placebo로 보임. 측정 오류 지적이 설득력 있으나 사회과학 지표 문제임</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2611.18883'>SPLICE: Structured Prompt Local Iterative Combinatorial Evolution</a></td><td>36</td><td>0</td><td>NLP</td><td>prompt를 block 단위 제약 탐색으로 최적화하는 SPLICE를 제안함. 이론 보장이 있으나 prompt 최적화 수준임</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2611.19299'>Staged Semantic Distillation: Preserving Free-Form Semantics in a Low-Compute Non-LLM Surrogate of a Staged LLM Agent</a></td><td>36</td><td>0</td><td>LG</td><td>LLM agent 시장 시뮬레이터를 1.3천만 파라미터 non-LLM student로 증류함. 한 시뮬레이터와 한 trace 사례 연구임</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2611.21529'>Procedure without Judgment: What Small Language Models Learn under an Exact Verifier</a></td><td>36</td><td>0</td><td>LLM</td><td>정확한 verifier 아래에서 4B 모델이 policy 충분 이유 탐색 절차를 배우나 일반화하지 못함을 보임, 흥미로운 negative 결과이나 접근 제어 설명 과제 한정임</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2611.19534'>Depth-Aware Path Planning and Collision Avoidance for Robotic Nursing Assistants Using Real-Time 3D Vision</a></td><td>35</td><td>4</td><td>Navigation</td><td>간호 보조 로봇의 depth 기반 경로 계획임. 고전적 응용 엔지니어링임</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2611.19818'>Drone Navigation for Fast, Safe Emergency Response</a></td><td>35</td><td>4</td><td>Navigation</td><td>재난 대응 드론 navigation임. 응용 위주이며 novelty 낮아 보임</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2611.19894'>EasyNav: A Modular Architecture for Real-Time Navigation Across Heterogeneous Robot Environments</a></td><td>35</td><td>4</td><td>Navigation</td><td>모듈형 navigation 소프트웨어 아키텍처임. 시스템 엔지니어링 중심임</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2611.19463'>Semantics First, Pixels Later: Mission-Driven Event Streams for Drone Video over Bandwidth-Starved Links</a></td><td>35</td><td>3</td><td>Robotics</td><td>드론 영상을 의미 이벤트로 전송하는 대역폭 절감 기법임. 로봇 학습과 거리 있음</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2611.19765'>M-CROSS: A Multisensor Simulation Dataset for SLAM across Water--Land Transitions</a></td><td>35</td><td>3</td><td>SLAM</td><td>수륙 전환 SLAM용 시뮬레이션 센서 데이터셋임. 데이터셋 기여 중심임</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2611.21264'>Hybrid Optimization-Generative Motion Planning for Multiagent Affine Formations</a></td><td>35</td><td>3</td><td>Multi-robot</td><td>affine formation 계획에 생성 모델을 결합함. 응용 위주임</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2611.20124'>QA-CMIF:Accurate and Lightweight Cross-Modal Latent Imputation and Fusion for Fault-Tolerant sEMG-Inertial Hand Gesture Recognition</a></td><td>35</td><td>2</td><td>LG</td><td>sEMG와 관성 센서의 채널 손상 대응 융합 네트워크로 Ninapro에서 gate-only 대비 1.29-4.15 퍼센트포인트 개선함. 의수 제어 응용이고 incremental임</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2611.20268'>GNN-Based Deep Reinforcement Learning for Coastal Emergency Response under Extreme Water Levels</a></td><td>35</td><td>2</td><td>RL</td><td>베네치아 해안 비상 대응에 GNN과 PPO를 적용했으나 규칙 기반 시스템과 비슷한 수준이고 그래프 구조 이득도 없음</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2611.21178'>TRACK: Tool-Augmented Reasoning over Time Series for Fault Diagnosis in Power Management System</a></td><td>35</td><td>2</td><td>LG</td><td>시계열 encoder와 소형 언어 모델에 tool을 붙여 전력 관리 시스템 고장 진단 보고서를 만듦. 시뮬레이션 15개 고장 클래스 한정임</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2611.21404'>Efficient Modeling of Multi-Agent Systems via Structure-Aware Physics-Informed Learning</a></td><td>35</td><td>2</td><td>LG</td><td>multi-agent 시스템의 physics-informed 모델링임. 로봇 연결 약함</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2611.21096'>Inference Equivalence and Quotient Coding</a></td><td>35</td><td>2</td><td>Theory</td><td>관측과 양립하는 해석 집합에서 유효한 결론을 보존하는 최소 코드를 quotient coding으로 정의함, 이론적이나 SAR 이미지 외 로봇 적용은 없음</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2611.18672'>Exists, Valid: Calibrated Validity of Stored 3D Geometry Across Long Observation Gaps</a></td><td>35</td><td>1</td><td>3D Vision</td><td>항공 LiDAR 지오메트리 유효성 추정으로 로봇 관련 낮음</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2611.21223'>Oriented Semi-DETR for Semi-Supervised Aerial Object Detection</a></td><td>35</td><td>1</td><td>CV</td><td>회전 박스의 2대1 파라미터 모호성을 semi-supervised DETR에서 제거하는 항목 세 개를 제안했으나 항공 검출 한정의 incremental 개선임</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2611.20464'>AdaModalX: Synchronization-Free MFM Inference for Distributed Multimodal Mobile Sensing via Progressive Data Orchestration</a></td><td>35</td><td>1</td><td>Multimodal</td><td>비동기 모달리티 도착에서 utility 기반으로 MFM 추론을 시작해 정확도 26.97% 향상과 지연 64.75% 감소를 보고함. 모바일 센싱 시스템 연구임</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2611.20609'>Newton-PINet: A fast physics-informed neural network with Newton linearization for meta-learning nonlinear PDEs</a></td><td>35</td><td>1</td><td>LG</td><td>Newton 선형화를 쓴 meta-learning PINN으로 비선형 PDE를 빠르게 풂. 반응-확산 benchmark 한정임</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2611.21015'>A physics-constrained emulator for time-discretised landslide runout modelling</a></td><td>35</td><td>1</td><td>LG</td><td>물리 제약 손실을 둔 산사태 runout emulator로 50배 이상 가속함. 지반 도메인 응용임</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2611.18611'>Understanding Failures in LLM Reasoning by Learning Structured Representations of Chain-of-Thought</a></td><td>35</td><td>1</td><td>NLP</td><td>CoT 구조 표현으로 LLM 추론 실패를 분석함. 실패 진단 관점이나 언어 도메인임</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2611.20955'>Jev-as-a-Reward: Validating Probabilistic Safety Judges for Reinforcement Learning</a></td><td>35</td><td>1</td><td>RL</td><td>RL 안전 judge가 높은 확신으로 통과시키는 harm의 blind spot을 훈련 전후로 검증하는 프로토콜을 제안함, LLM 안전 정렬 주제이며 로봇 안전과는 거리가 있음</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2611.19624'>Well-Log Reconstruction with Pre-trained Geological Knowledge: A Knowledge-Conditioned Large-Language-Model Generative Agent</a></td><td>35</td><td>0</td><td>LG</td><td>LLM의 지질 prior로 well-log 결측을 복원하는 도메인 특화 응용이며 robotics와 무관함</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2611.19698'>Data Attribution Should Steer Pretraining</a></td><td>35</td><td>0</td><td>LG</td><td>pretraining 데이터 attribution이 curation을 이끌어야 한다는 position paper이며 실험 증거가 없음</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2611.19742'>Exploration of Reinforcement Learning in Generative Recommendation Models</a></td><td>35</td><td>0</td><td>RL</td><td>추천 모델의 GRPO 불안정성을 진단해 gradient-bounded 목적함수를 제안함. 추천 도메인 한정임</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2611.19937'>AllocFlow: End-to-End Portfolio Trading Action Generation from Raw Market Data</a></td><td>35</td><td>0</td><td>RL</td><td>flow matching과 group-relative RL로 포트폴리오 배분을 생성하는 금융 응용임. robotics 무관함</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2611.19972'>The structure of variational autoencoder latent spaces and its consequences for representation and optimization</a></td><td>35</td><td>0</td><td>LG</td><td>VAE latent space 구조를 Flory-Huggins 이론과 대응시켜 분석하는 이론 연구임. robotics와는 거리 있음</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2611.20334'>Residual-Tail-Informed Flow Matching for Time Series Anomaly Detection</a></td><td>35</td><td>0</td><td>LG</td><td>잔차 tail 가중 flow matching으로 시계열 이상 탐지의 rare-normal 오탐을 줄임. 시계열 benchmark 한정임</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2611.20417'>When the Cheapest Feasible Router Fails: Auditing Deployment Commitments in Cost-Aware LLM Routing</a></td><td>35</td><td>0</td><td>NLP</td><td>비용 인지 LLM routing에서 가장 싼 feasible router가 held-out 계약을 32.22% 위반함을 감사하고 MARC를 제안함. 서비스 운영 주제임</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2611.20663'>ParGLU: Partial Gating Improves Language Modeling in MoE Transformers</a></td><td>35</td><td>0</td><td>NLP</td><td>MoE FFN에 SwiGLU와 ReLU^2 부분 게이팅을 적용해 NLL을 0.02 줄임. 소규모 모델의 작은 개선임</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2611.20696'>Conic Structure of the Cross-Entropy Loss at the Final Layer and Its Absence in Rectifier Backbones</a></td><td>35</td><td>0</td><td>LG</td><td>softmax cross-entropy loss의 conic 구조와 rectifier backbone의 kink 부재를 증명함. 순수 이론이고 robotics 무관함</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2611.19763'>Ambiguous Examples Help, But Full Data Wins: Revisiting Dataset Cartography for Extractive Adversarial QA</a></td><td>35</td><td>0</td><td>NLP</td><td>dataset cartography의 ambiguous subset 주장을 extractive QA에서 재검증함. 전체 데이터가 더 낫다는 재현 연구이며 새 방법은 없음</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2611.20643'>Safety-Preserving Medical LLM Fine-Tuning via Bilevel Data Selection</a></td><td>35</td><td>0</td><td>NLP</td><td>bilevel data selection으로 의료 SFT의 안전성 저하를 줄임. safe rate 개선이 3~4.6점 수준이며 도메인 특화임</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2611.20846'>EDITORS Know Your Style! Editing LoRA Subspaces for Stylistic Attribution and Imitation</a></td><td>35</td><td>0</td><td>NLP</td><td>content 부분공간을 진단한 뒤 LoRA activation에서 제거하는 EDITORS로 저자 판별·문체 모방을 개선함. 문체 도메인 한정임</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2611.18908'>MemeEconomy: Do LLM Agents Trade Ethics for Survival?</a></td><td>35</td><td>0</td><td>Multimodal</td><td>LLM agent가 생존 압력 하에서 유해 meme 선택률이 15퍼센트포인트 오름을 시뮬레이션으로 보임. 안전성 평가이며 로봇과 무관함</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2611.19323'>The Data Debt of Stockouts: Partial Identification and Minimax-Regret Inventory Control</a></td><td>35</td><td>0</td><td>AI</td><td>재고 stockout 로그의 부분 식별과 minimax-regret 정책의 이론 분석임. OR 도메인 이론이며 로봇과 무관함</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2611.21299'>Turing Agent: Agentic Formal Verification for Mathematical Research</a></td><td>35</td><td>0</td><td>LLM Agent</td><td>연구 수준 수학 증명의 형식 검증을 조율하는 Turing Agent를 제안함, 인상적인 사례가 있으나 수학 정리 증명 도메인이며 로보틱스와 무관함</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2611.21315'>Benchleaking Is Accelerating: Benchmark contamination has worsened sharply in the past month -- from post-training down to pre-training base models</a></td><td>35</td><td>0</td><td>LLM Eval</td><td>벤치마크 test 예시가 사전학습 base 모델까지 누설되는 benchleaking을 Anti-Hack 점수로 정량화함, 평가 신뢰성 이슈는 중요하나 로보틱스와 무관함</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2611.21472'>Event-Triggered Visual Perception for Real-Time Harvest Outcome Estimation in Mechanical Blueberry Harvesting</a></td><td>34</td><td>3</td><td>CV</td><td>블루베리 수확기에서 숙도를 이벤트 기반 영상으로 추정하는 농업 응용 시스템임</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2611.19566'>Bellman Residual Bracketing: Resolving the Sample Complexity of Discounted and Average-Reward RL</a></td><td>34</td><td>3</td><td>RL</td><td>generative model RL의 plug-in 방식 sample complexity를 minimax 수준으로 정리한 이론 연구임</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2611.18813'>RescueVLM: Model-Agnostic Vision-Language Framework for Rescue Drone Imagery</a></td><td>34</td><td>2</td><td>Multimodal</td><td>구조 드론 영상 VLM 프레임워크로 응용 위주임</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2611.20864'>LiDSeg: Linear DehazeFormer Guidance for Efficient Semantic Segmentation in Adverse Weather Conditions</a></td><td>34</td><td>2</td><td>CV</td><td>악천후 분할 경량 dehaze guidance로 incremental함</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2611.21365'>Exploring the link between predictive uncertainty and the sim-to-real gap in deep learning models utilizing synthetic data</a></td><td>34</td><td>2</td><td>CV</td><td>합성 데이터 학습 모델의 예측 불확실성과 sim-to-real 격차 관계를 ensemble로 본 산업 검사 소규모 실험임</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2611.18725'>Detection Is Not the Finish Line: Multiscale Decoding and Constraint-Aware Global Association for Multi-Camera 3D Tracking</a></td><td>34</td><td>1</td><td>3D Vision</td><td>멀티카메라 3D tracking 챌린지 솔루션으로 engineering 위주임</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2611.19773'>SemLite-GS: Semantic-Selective Parallel Gaussian Splatting for Lightweight Building Reconstruction from UAV Oblique Imagery</a></td><td>34</td><td>1</td><td>3D Vision</td><td>UAV 건물 경량 3DGS 복원으로 도시 응용임</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2611.20092'>Geo2Gcode: From 3D Geometry to CNC Programs through Structured Machining Primitives</a></td><td>34</td><td>1</td><td>Generative</td><td>3D 형상에서 CNC 프로그램 생성으로 제조 응용임</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2611.20680'>Room for Supervision: Training-Free Dataset Distillation for Object Detection</a></td><td>34</td><td>1</td><td>CV</td><td>detection dataset distillation training-free로 incremental함</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2611.18690'>Perceptual Weight Space Programming for Diffusion Super-Resolution</a></td><td>34</td><td>0</td><td>Generative</td><td>LLM 기반 SR 가중치 편집으로 로봇 무관함</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2611.19076'>SearchChord: Prompt Preselection and Field Recomposition for One-Step Image Editing</a></td><td>34</td><td>0</td><td>Generative</td><td>one-step 이미지 편집 prompt 탐색으로 무관함</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2611.19440'>Few-Shot Visual Concept Extraction for Steering Diffusion Transformers</a></td><td>34</td><td>0</td><td>Generative</td><td>DiT few-shot 개념 steering으로 생성 제어임</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2611.19747'>How Far Is Too Far? Object Recognition Declines Monotonically with Semantic Distance</a></td><td>34</td><td>0</td><td>CV</td><td>객체-배경 의미 거리와 인식 저하 분석으로 로봇 관련 낮음</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2611.20537'>SmoothShift: Disrupting Visual Adversarial Attacks on LVLMs at Test Time</a></td><td>34</td><td>0</td><td>Multimodal</td><td>LVLM adversarial test-time 교란으로 보안 incremental함</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2611.20553'>Learning a Task-Adaptive Low-Dimensional Semantic Space for Improved Visual Classification</a></td><td>34</td><td>0</td><td>CV</td><td>분류용 저차원 semantic space로 incremental함</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2611.21168'>Beyond Token Stacking: Multi-scale Visual Modulation and Adaptive Fused-feature Calibration for MLLMs</a></td><td>34</td><td>0</td><td>Multimodal</td><td>MLLM visual modulation 융합 보정으로 incremental함</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2611.18646'>RSIMed: Scaling Medical Foundation Models beyond Limited Clinical Data via Retrieval-Grounded Self-Evolution</a></td><td>34</td><td>0</td><td>LG</td><td>의료 희귀질환 진단용 self-evolving 학습 파이프라인으로 로봇과 무관함</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2611.18652'>MeltKV: Memory-Aligned KV Cache Compression via Variable-Bit Packed Vector Quantization for Long-Context LLMs</a></td><td>34</td><td>0</td><td>LG</td><td>KV cache를 variable-bit VQ로 압축해 메모리와 지연을 줄이는 LLM 서빙 최적화임</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2611.19037'>The Critic Can Hurt: On the Safety of Critics in LLM-Guided AutoML Search</a></td><td>34</td><td>0</td><td>LG</td><td>LLM critic이 AutoML 탐색을 해칠 수 있음을 fault injection으로 감사한 연구임</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2611.19587'>Explicit Regularization for Flow Matching</a></td><td>34</td><td>0</td><td>Generative</td><td>flow matching에 속도장 미분 정규화를 넣어 암기를 막는 이론으로 1, 2차원 실험에 그침</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2611.20405'>Refusal Register is Causally Steerable: Decomposing the Refusal Direction into Category-Aligned Components in Gemma-2-9B-IT</a></td><td>34</td><td>0</td><td>NLP</td><td>Gemma-2-9B에서 refusal 방향을 category별 성분으로 분해해 refusal 어투가 조절됨을 보임. 단일 모델 interpretability 분석임</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2611.19016'>Match and Correct: A Repeated Computational Motif in Evoformer Layers</a></td><td>34</td><td>0</td><td>LG</td><td>Evoformer 층별 probe로 삼각 부등식 위반이 두 단계로 줄어듦을 보임. 단백질 모델 해석 연구이며 로봇과 무관함</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2611.19932'>From Companion to Guardian: Designing an Emergency Support System Using a Quadruped Robot for Older Adults</a></td><td>33</td><td>4</td><td>HRI</td><td>사족 로봇 노인 응급 지원 시스템 설계임. HRI 응용이며 학습 기여 약함</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2611.20360'>Flow Matching for Sampled-Data Control of Angular Distributions</a></td><td>33</td><td>2</td><td>LG</td><td>진동자 위상 분포 제어에 flow matching과 MeanFlow를 비교하는 이론 분석임. 100개 위상 실험만 있음</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2611.19917'>Delayed Heuristic-Behavior-Target Coupling for Off-Policy Reinforcement Learning in Inventory Control</a></td><td>33</td><td>1</td><td>RL</td><td>재고 관리용 off-policy RL(HBPO)로 휴리스틱 지도를 behavior policy에 반영함. 재고 도메인 한정임</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2611.20451'>Generative AI-Driven Parametric Design Optimization Framework for Vehicle Closure Systems</a></td><td>33</td><td>1</td><td>Generative</td><td>diffusion과 flow matching으로 차량 테일게이트 CAD를 생성하고 질량을 7.1% 줄임. 설계 최적화 응용임</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2611.21370'>Federated TD Learning in Heterogeneous Environments with Average Rewards: A Two-timescale Approach with Polyak-Ruppert Averaging</a></td><td>33</td><td>1</td><td>RL</td><td>federated TD learning 수렴 이론임. 로봇 적용 없음</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2611.19614'>A Hierarchical Statistical Framework for Evaluating Agent Reliability</a></td><td>33</td><td>1</td><td>LG</td><td>agent 신뢰도 평가를 scenario-instance-sample 계층으로 나눠 pass@k 분산 전파를 유도함, 통계 도구로서 유용하나 로봇 평가와 직접 연결은 약함</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2611.18643'>FedFit: Federated Dynamic Sparse Training via Fisher Information scoring</a></td><td>33</td><td>0</td><td>LG</td><td>federated 동적 sparse 학습에 Fisher 정보 기준을 쓰는 incremental 방법임</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2611.19625'>Robust Well-Log Reconstruction Across Point Gaps and Whole Wells via Boundary-Gated Soft-Thresholding Kalman Fusion</a></td><td>33</td><td>0</td><td>LG</td><td>웨이블릿 수축과 Kalman 융합으로 well-log 간격을 복원하는 지구물리 응용이고 방법도 incremental임</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2611.20180'>UrbanROI: Causal Modeling for Regional ROI Forecasting under POI Entry</a></td><td>33</td><td>0</td><td>LG</td><td>POI 진입 후 지역 ROI를 counterfactual 그래프로 예측하는 광고 도메인 응용임</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2611.20377'>Halting in Recurrent Sequence Models</a></td><td>33</td><td>0</td><td>LG</td><td>RNN과 SSM이 EOS 종료를 결정하는 메커니즘을 단순 복사 과제에서 분석함. robotics 무관함</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2611.20419'>Reasoning Again with a Quarter of the Experts: Retry First, Then Train</a></td><td>33</td><td>0</td><td>NLP</td><td>expert 4분의 3을 제거한 MoE의 reasoning loop를 재시도와 adapter로 복구하나 단일 모델, 단일 benchmark임</td></tr>
<tr><td>486</td><td><a href='https://arxiv.org/abs/2611.20714'>MSAR: Next-Scale Autoregressive Forecasting for Time Series via Modular Multi-Scale Decoupling</a></td><td>33</td><td>0</td><td>LG</td><td>시계열 예측을 scale-wise autoregression으로 바꾼 모델 비의존 설계이며 개선이 incremental임</td></tr>
<tr><td>487</td><td><a href='https://arxiv.org/abs/2611.21111'>Searching for Autoregressive Neural Architectures from Fundamental Operations</a></td><td>33</td><td>0</td><td>LG</td><td>기본 연산으로 autoregressive 구조를 찾는 NAS search space(einspaceAR)를 확장함. 효용 근거가 약함</td></tr>
<tr><td>488</td><td><a href='https://arxiv.org/abs/2611.19767'>Logical AI OS: A Training-Free Governance Layer Outside the Model for Instruction Following -- Benefits, Costs, Failures, and the Calibration of the Measuring Instrument Itself</a></td><td>33</td><td>0</td><td>NLP</td><td>외부 규칙 기반 검사·수정 층으로 소형 LLM의 지시 이행을 높이는 효과를 측정함. 중국어·Qwen 소형 모델 한정이고 구현 비공개임</td></tr>
<tr><td>489</td><td><a href='https://arxiv.org/abs/2611.19900'>Attribute or Abstain: Evaluating Evidence-Grounded Retrieval on the Low-Resource African Business Web</a></td><td>33</td><td>0</td><td>NLP</td><td>아프리카 기업 정보 검색에서 근거 기반 답변과 abstain을 재는 benchmark임. 단순 baseline이 agent보다 낫다는 결과이며 로봇과 무관함</td></tr>
<tr><td>490</td><td><a href='https://arxiv.org/abs/2611.20094'>FRAAC: A French Multimodal Large Language Model and Dataset forPictogram-Based Augmentative and Alternative Communication</a></td><td>33</td><td>0</td><td>NLP</td><td>pictogram AAC용 프랑스어 합성 코퍼스 1.4M쌍과 MLLM을 만듦. 접근성 도메인 dataset 구축이며 로봇과 무관함</td></tr>
<tr><td>491</td><td><a href='https://arxiv.org/abs/2611.21155'>Edit Recommendation: Can LLMs Anticipate Edit Requests from Users, and When?</a></td><td>33</td><td>0</td><td>NLP</td><td>사용자의 edit 요청을 예측하는 EditRecBench와 gating을 제안함. 대화 로그 기반 응용 과제임</td></tr>
<tr><td>492</td><td><a href='https://arxiv.org/abs/2611.20447'>The Logic Chain Breaking Point: A Controlled-Variable Benchmark for Reasoning Degradation in Open-Weight Language Models</a></td><td>33</td><td>0</td><td>NLP</td><td>2의 거듭제곱 길이로 연역 추론 사슬 붕괴를 재는 벤치마크를 제안함, 모순 전제에서 거의 0점인 점은 흥미로우나 로보틱스와 무관함</td></tr>
<tr><td>493</td><td><a href='https://arxiv.org/abs/2611.21053'>System 1 agents: a method for local, reliable and fast agentic AI</a></td><td>33</td><td>0</td><td>LLM Agent</td><td>도구 호출을 객관식 질문으로 컴파일해 텍스트 생성 없이 고르는 System 1 agent를 제안함, 생의학 tool 선택 한정이며 로보틱스와 무관함</td></tr>
<tr><td>494</td><td><a href='https://arxiv.org/abs/2611.18855'>Technical Report of Auriga&#x27;s 1:10 Scale Autonomous Vehicle Robot</a></td><td>32</td><td>3</td><td>Robotics</td><td>1:10 자율주행 로봇 플랫폼 기술 보고서임. 연구 novelty 낮음</td></tr>
<tr><td>495</td><td><a href='https://arxiv.org/abs/2611.19238'>Continuous Lower-Limb Joint-Angle Estimation from sEMG and IMU: The Conditional Value of Cross-Activity and Cross-Subject Data under Update-Matched Controls</a></td><td>32</td><td>3</td><td>Robotics</td><td>sEMG와 IMU로 하지 관절각을 추정함. 외골격 도메인이며 로봇 학습과 거리 있음</td></tr>
<tr><td>496</td><td><a href='https://arxiv.org/abs/2611.19730'>AlphaTruck: A Platform for High-Speed Off-Road Autonomy on Unstructured Terrain</a></td><td>32</td><td>3</td><td>Robotics</td><td>고속 오프로드 자율주행 플랫폼 소개임. 연구 novelty 낮음</td></tr>
<tr><td>497</td><td><a href='https://arxiv.org/abs/2611.19897'>HIVE-ECIA: Identity-Aware Historical Evidence Acquisition for Bandwidth-Efficient Multi-Object Tracking</a></td><td>32</td><td>2</td><td>CV</td><td>파노라마 MOT 대역폭 효율 증거 획득으로 incremental함</td></tr>
<tr><td>498</td><td><a href='https://arxiv.org/abs/2611.21162'>DRaGAN: Dynamic Graph Attention Network for Multi-Radar Point Cloud Encoding in Automotive Radar Perception</a></td><td>32</td><td>2</td><td>3D Vision</td><td>레이더 point cloud 인코딩 graph attention으로 센서 특화임</td></tr>
<tr><td>499</td><td><a href='https://arxiv.org/abs/2611.20851'>artist: A Python package for differentiable ray tracing and gradient-based optimization of solar tower power plant operation</a></td><td>32</td><td>2</td><td>LG</td><td>태양광 타워 발전소용 미분 가능 ray tracing 파이썬 패키지로 digital twin의 역모델링을 함. 소프트웨어 도구이고 robotics는 약함</td></tr>
<tr><td>500</td><td><a href='https://arxiv.org/abs/2611.21507'>GHySSeg: Real-Time Geometric Ground and Road Segmentation for Hybrid Solid-State LiDAR</a></td><td>32</td><td>2</td><td>Perception</td><td>hybrid solid-state LiDAR 지면 분할임. 기여 좁음</td></tr>
<tr><td>501</td><td><a href='https://arxiv.org/abs/2611.18753'>Conv-Reluplex: A Verification Framework For Convolution Neural Networks</a></td><td>32</td><td>1</td><td>LG</td><td>CNN 형식 검증 확장으로 안전 검증 도구이나 로봇 실험 없음</td></tr>
<tr><td>502</td><td><a href='https://arxiv.org/abs/2611.19146'>Puzzle: One Pass Is Not Enough for Open-Vocabulary Remote Sensing Segmentation</a></td><td>32</td><td>1</td><td>CV</td><td>원격탐사 open-vocab 분할 다중 pass로 incremental함</td></tr>
<tr><td>503</td><td><a href='https://arxiv.org/abs/2611.20361'>Structure-Guided Multi-Granularity Spatiotemporal Transformer for Efficient Monocular 3D Human Pose Estimation</a></td><td>32</td><td>1</td><td>CV</td><td>단안 3D 인간 pose 효율 transformer로 incremental함</td></tr>
<tr><td>504</td><td><a href='https://arxiv.org/abs/2611.20425'>InterRSGaussian: Interactive Multi-view Instance Segmentation for 3D Remote Sensing Scenes</a></td><td>32</td><td>1</td><td>3D Vision</td><td>원격탐사 3DGS interactive 분할로 응용임</td></tr>
<tr><td>505</td><td><a href='https://arxiv.org/abs/2611.21283'>PLECTA: Overlap-aware instance segmentation of dense strand networks from binary masks</a></td><td>32</td><td>1</td><td>CV</td><td>겹친 strand 네트워크를 최대가중 매칭으로 분리하는 재료 현미경용 방법이라 로봇과 무관함</td></tr>
<tr><td>506</td><td><a href='https://arxiv.org/abs/2611.19575'>Risk-Averse Decision-Focused Learning: Minimizing CVaR of Regret</a></td><td>32</td><td>1</td><td>LG</td><td>CVaR 기반 위험 회피 decision-focused learning으로 조합 최적화 위주임</td></tr>
<tr><td>507</td><td><a href='https://arxiv.org/abs/2611.18622'>RGFC: Registry Grounded Function Calling with stage-decomposed evaluation</a></td><td>32</td><td>1</td><td>NLP</td><td>function calling의 단계 분해 평가임. 실패 원인 분해 관점이나 언어 도메인임</td></tr>
<tr><td>508</td><td><a href='https://arxiv.org/abs/2611.18629'>Decision 1.0: Towards Open Decision Foundation Models</a></td><td>32</td><td>1</td><td>NLP</td><td>제어 흐름용 decision foundation model임. 로봇과 거리 있음</td></tr>
<tr><td>509</td><td><a href='https://arxiv.org/abs/2611.19165'>From Sensors to Silicon: Causal Cross-Layer Self-Healing Edge AI for Secure and Energy-Adaptive IoT Systems</a></td><td>32</td><td>1</td><td>AI</td><td>센서부터 하드웨어까지 telemetry로 이상 원인을 인과 추정하는 self-healing Edge-AI 프레임워크임. 원인 진단 관점은 있으나 초록상 정량 결과가 없고 IoT 한정임</td></tr>
<tr><td>510</td><td><a href='https://arxiv.org/abs/2611.19311'>Macro Control and Capability Evaluation of Black-Box World Models: A Two-Regime Framework for LLM-Agent Markets</a></td><td>32</td><td>1</td><td>AI</td><td>LLM agent 시장을 black-box world model로 보고 거시 제어와 2단계 평가를 제안함. 금융 시뮬레이션 한정이고 world model 의미가 로봇과 다름</td></tr>
<tr><td>511</td><td><a href='https://arxiv.org/abs/2611.20535'>VAHBench: A Harness Benchmark for Agentic Long-Video Generation</a></td><td>32</td><td>1</td><td>Video</td><td>agent가 단편 드라마 영상을 끝까지 제작하는 능력을 240회 실행으로 평가하는 VAHBench를 제안함, 영상 생성 agent 벤치마크이며 로보틱스와 무관함</td></tr>
<tr><td>512</td><td><a href='https://arxiv.org/abs/2611.18673'>Robust-GCD</a></td><td>32</td><td>0</td><td>CV</td><td>GCD 노이즈 강건성으로 incremental함</td></tr>
<tr><td>513</td><td><a href='https://arxiv.org/abs/2611.19248'>Size-Matched Nulls Reveal What Block Ablation Measures in MambaVision</a></td><td>32</td><td>0</td><td>CV</td><td>MambaVision block ablation 분석으로 로봇 무관함</td></tr>
<tr><td>514</td><td><a href='https://arxiv.org/abs/2611.20349'>Words Speak Louder? Exploring the Language Shortcut of LLM-Driven Incomplete Multimodal Learning</a></td><td>32</td><td>0</td><td>Multimodal</td><td>LLM 불완전 멀티모달 언어 shortcut 분석으로 무관함</td></tr>
<tr><td>515</td><td><a href='https://arxiv.org/abs/2611.20637'>Counterfactual Feature Steering for Adjacency-Preserving Identity Unlearning</a></td><td>32</td><td>0</td><td>Generative</td><td>identity unlearning counterfactual steering으로 무관함</td></tr>
<tr><td>516</td><td><a href='https://arxiv.org/abs/2611.20704'>QASK-Edit: Adaptive Sparse Attention Across Queries and Key Sources for Efficient Video Editing</a></td><td>32</td><td>0</td><td>Video</td><td>video 편집 sparse attention 가속으로 무관함</td></tr>
<tr><td>517</td><td><a href='https://arxiv.org/abs/2611.21604'>FaceJev: Direct Visual Decisions for Face Forgery Detection</a></td><td>32</td><td>0</td><td>CV</td><td>MLLM의 부위별 직접 판단으로 얼굴 위조를 탐지하는 방법이라 로봇과 무관함</td></tr>
<tr><td>518</td><td><a href='https://arxiv.org/abs/2611.18647'>Screen Before You Add: Reducing Candidate Inference in Model Ensembles</a></td><td>32</td><td>0</td><td>LG</td><td>앙상블에 후보 모델을 추가할 때 조기 기각하는 스크리닝 이론 연구로 로봇과 무관함</td></tr>
<tr><td>519</td><td><a href='https://arxiv.org/abs/2611.18768'>Can a Vision-Language Model Tune Clustering In Context?</a></td><td>32</td><td>0</td><td>LG</td><td>VLM이 클러스터링 결과 도식을 보고 k-means 하이퍼파라미터를 조정하는 합성 데이터 탐색 실험임</td></tr>
<tr><td>520</td><td><a href='https://arxiv.org/abs/2611.19656'>BadGCL: Towards Persistent Backdoor Attack on Graph Continual Learning Systems</a></td><td>32</td><td>0</td><td>LG</td><td>그래프 continual learning에 대한 지속형 backdoor 공격을 제안함. 보안 주제이고 robotics 무관함</td></tr>
<tr><td>521</td><td><a href='https://arxiv.org/abs/2611.19701'>Multiaccuracy as an Error Benchmark for Learning with Distribution Shift</a></td><td>32</td><td>0</td><td>LG</td><td>TDS 학습의 shift multiaccuracy 오차 기준을 제안하는 순수 학습 이론임</td></tr>
<tr><td>522</td><td><a href='https://arxiv.org/abs/2611.20435'>iEEG Can Help EEG: Improving Clinical Scalp EEG Analysis through Intracranial Priors</a></td><td>32</td><td>0</td><td>LG</td><td>iEEG로 학습한 prior를 고정해 두피 EEG를 보정하는 ReBrain을 제안함. 생체 신호 도메인이고 robotics 무관함</td></tr>
<tr><td>523</td><td><a href='https://arxiv.org/abs/2611.20472'>Model Immunization Beyond Condition Numbers: The Importance of Plateau Regions</a></td><td>32</td><td>0</td><td>NLP</td><td>Hessian plateau 영역을 고려한 model immunization으로 유해 fine-tuning을 방어함. LLM 안전성 연구임</td></tr>
<tr><td>524</td><td><a href='https://arxiv.org/abs/2611.19643'>SG-LegalClarify: A Large-Scale Benchmark for Legal Reasoning and Ambiguity Recognition in Singapore Law</a></td><td>32</td><td>0</td><td>NLP</td><td>싱가포르 법률 추론과 모호성 인식을 보는 benchmark임. 도메인 특화 데이터셋이며 로봇과 무관함</td></tr>
<tr><td>525</td><td><a href='https://arxiv.org/abs/2611.20579'>Language Models Meet Vibration Testing for LEO Constellation Satellites with Calibrated Response Prediction from Few-show Sweeps</a></td><td>32</td><td>0</td><td>NLP</td><td>LLM 설정 추출에 deterministic validation gate를 두어 위성 진동시험 분석 오류를 막음. 특정 공학 도메인 응용이며 로봇과 무관함</td></tr>
<tr><td>526</td><td><a href='https://arxiv.org/abs/2611.20821'>CuRSE-Bench: A Benchmark for Probing Cultural Blind Spots in Text-to-Image Safety Evaluation</a></td><td>32</td><td>0</td><td>Multimodal</td><td>T2I 안전 평가의 문화별 blind spot을 보는 CuRSE-Bench를 만듦. persona judge 비교 중심의 benchmark이며 로봇과 무관함</td></tr>
<tr><td>527</td><td><a href='https://arxiv.org/abs/2611.20568'>sqrtVINS-Based 360 Visual-Inertial SLAM Systems: Hilti-Trimble SLAM Challenge 2026 Entry</a></td><td>30</td><td>3</td><td>SLAM</td><td>Hilti SLAM 챌린지 참가 보고서임. novelty 낮음</td></tr>
<tr><td>528</td><td><a href='https://arxiv.org/abs/2611.18778'>Third-Place Solution for the UCF UrbanTwin V2X-Real Track at ECCV 2026: Synthetic Point Cloud Generation and Sim-to-Real 3D Object Detection</a></td><td>30</td><td>2</td><td>3D Vision</td><td>V2X LiDAR 챌린지 솔루션 보고서로 engineering 위주임</td></tr>
<tr><td>529</td><td><a href='https://arxiv.org/abs/2611.21233'>A Study on Performance Enhancement of a Webcam-Based Real-Time Eye-Tracking System</a></td><td>30</td><td>2</td><td>CV</td><td>웹캠 시선 추적에 보정과 잔차 보정을 얹은 시스템이며 참가자 1명 예비 실험뿐이라 근거가 약함</td></tr>
<tr><td>530</td><td><a href='https://arxiv.org/abs/2611.19931'>Does synthetic pre-training pay off on a microcontroller? Accuracy, latency and energy across two MCUs</a></td><td>30</td><td>2</td><td>LG</td><td>마이크로컨트롤러에서 synthetic pre-training의 효과를 측정해 실제 데이터가 충분하면 이득이 없음을 보임. 임베디드 분류 사례 보고임</td></tr>
<tr><td>531</td><td><a href='https://arxiv.org/abs/2611.19703'>Real-Time Air Pollution Monitoring and Tracking via Adaptive Density-Driven Multi-UAV Coordination</a></td><td>30</td><td>2</td><td>Multi-UAV</td><td>다중 UAV 대기오염 모니터링의 density-driven 조율임. 고전적 응용임</td></tr>
<tr><td>532</td><td><a href='https://arxiv.org/abs/2611.21129'>Linglong Agent Service: A Runtime for Centralized Agent Reasoning and Distributed Execution</a></td><td>30</td><td>2</td><td>Systems</td><td>LLM agent runtime 설계임. 로봇 학습과 무관한 시스템 기여임</td></tr>
<tr><td>533</td><td><a href='https://arxiv.org/abs/2611.19529'>Ultra-CAN: A Lightweight Blind ISAC Receiver for Chaos-Based Telemetry and Local-Seed Ranging in the Internet of Drones</a></td><td>30</td><td>2</td><td>Signal Processing</td><td>드론 군집용 chaos 기반 blind ISAC 수신기를 마이크로컨트롤러에서 구동함, 통신 신호처리 주제이며 로봇 학습과는 거리가 있음</td></tr>
<tr><td>534</td><td><a href='https://arxiv.org/abs/2611.18869'>UnSPAD: Uncertainty-aware Single Photon Burst Photography</a></td><td>30</td><td>1</td><td>CV</td><td>단일광자 burst 촬영 불확실성 인지 복원으로 영상 처리임</td></tr>
<tr><td>535</td><td><a href='https://arxiv.org/abs/2611.19746'>Event-based object detection under adverse lighting and motion: lessons for construction sites</a></td><td>30</td><td>1</td><td>CV</td><td>건설현장 event 카메라 검출 분석으로 응용임</td></tr>
<tr><td>536</td><td><a href='https://arxiv.org/abs/2611.20127'>Aerial Person Detection under Edge Constraints: Held-Out Evaluation and Edge-Ground Verification</a></td><td>30</td><td>1</td><td>CV</td><td>드론 사람 검출 edge 평가로 응용임</td></tr>
<tr><td>537</td><td><a href='https://arxiv.org/abs/2611.20412'>Training-Free Anonymization of Driving Data with Promptable Segmentation and 3D Human Mesh Recovery</a></td><td>30</td><td>1</td><td>CV</td><td>주행 데이터 익명화 training-free 파이프라인으로 응용임</td></tr>
<tr><td>538</td><td><a href='https://arxiv.org/abs/2611.20879'>Multi-Rate Flow Matching for Point Cloud Upsampling</a></td><td>30</td><td>1</td><td>3D Vision</td><td>point cloud upsampling multi-rate flow matching으로 incremental함</td></tr>
<tr><td>539</td><td><a href='https://arxiv.org/abs/2611.18655'>Beveridge: Open Weight System One Decision Models with Calibrated Probabilities</a></td><td>30</td><td>1</td><td>LG</td><td>문서 의사결정용 보정된 확률 모델 계열을 공개했으나 로봇과 무관한 산업 응용임</td></tr>
<tr><td>540</td><td><a href='https://arxiv.org/abs/2611.19586'>SLiDE: Structured Linear Dynamics for Forecasting with Exogenous Inputs</a></td><td>30</td><td>1</td><td>LG</td><td>외생 입력 시계열 예측을 위한 Koopman 영감 선형 latent 구조임</td></tr>
<tr><td>541</td><td><a href='https://arxiv.org/abs/2611.19770'>Exact Sparse Assignment with Costly Target Embeddings: Fixed-Realization Certificates and an Empirical Audit</a></td><td>30</td><td>1</td><td>CV</td><td>검출-트랙 연관에 쓰는 sparse assignment의 최적성 certificate를 제안하나 실험은 텍스트 entity matching이고 속도 이득도 없음</td></tr>
<tr><td>542</td><td><a href='https://arxiv.org/abs/2611.19826'>Where Is Rank-1 DiM Refusal Intervenable in Multimodal LM Derivatives?</a></td><td>30</td><td>1</td><td>Multimodal</td><td>VLM 파생 모델에서 rank-1 DiM refusal 개입이 텍스트 디코더에서만 통함을 보이는 안전성 감사임. robotics 무관함</td></tr>
<tr><td>543</td><td><a href='https://arxiv.org/abs/2611.20150'>Symmetry Fingerprinting with Geometric Learnable Invariants Transformers</a></td><td>30</td><td>1</td><td>LG</td><td>학습 중 필요한 대칭만 선택하는 soft equivariant 구조와 symmetry fingerprint를 제안함. 이미지 분류 소규모 시연뿐임</td></tr>
<tr><td>544</td><td><a href='https://arxiv.org/abs/2611.20607'>DNA: A Double-Helix Hierarchical Deep Interaction Network Architecture for Industrial Digital Twin</a></td><td>30</td><td>1</td><td>LG</td><td>기계론적 모델과 데이터 모델을 엮은 DNA 구조로 MAE를 약 3% 줄임. 산업 digital twin 응용임</td></tr>
<tr><td>545</td><td><a href='https://arxiv.org/abs/2611.20877'>Markov-Equivalent Conditional Independence Graphs on Path Spaces</a></td><td>30</td><td>1</td><td>LG</td><td>잠재 교란이 있는 연속시간 과정의 W-separation과 Markov 동치류를 특성화하는 인과 이론임</td></tr>
<tr><td>546</td><td><a href='https://arxiv.org/abs/2611.20991'>FH-Sampling: Frequency-aware Hypergraph-driven Oversampling for Imbalanced Time-Series Classification</a></td><td>30</td><td>1</td><td>LG</td><td>hypergraph와 wavelet 주파수 성분으로 불균형 시계열 oversampling을 함. 항공기 궤적 생성 시연이 있으나 incremental임</td></tr>
<tr><td>547</td><td><a href='https://arxiv.org/abs/2611.21486'>Differentiable Exact Learning</a></td><td>30</td><td>1</td><td>LG</td><td>외부 환경과 상태 추적 controller의 differentiable exact learning임. 로봇 연결 약함</td></tr>
<tr><td>548</td><td><a href='https://arxiv.org/abs/2611.18612'>When Helpful Agents Cause Financial Harm: Evaluating LLM Agent Safety in Executable Economic Worlds</a></td><td>30</td><td>1</td><td>NLP</td><td>LLM agent의 경제적 피해 안전성 평가임. 로봇과 거리 있음</td></tr>
<tr><td>549</td><td><a href='https://arxiv.org/abs/2611.19202'>Omni-Workspace: Benchmarking Omni-Modal AI Assistants on Multimodal Workspace Tasks</a></td><td>30</td><td>1</td><td>Multimodal</td><td>omni-modal assistant workspace benchmark임. 로봇과 거리 있음</td></tr>
<tr><td>550</td><td><a href='https://arxiv.org/abs/2611.19273'>B-OPSD: On-Policy Self-Distillation with Self-Generated Problem Briefs</a></td><td>30</td><td>1</td><td>NLP</td><td>자기 생성 brief로 on-policy self-distillation함. 로봇과 거리 있음</td></tr>
<tr><td>551</td><td><a href='https://arxiv.org/abs/2611.19345'>Information Limits of Replay-Free Recurrent State Migration</a></td><td>30</td><td>1</td><td>LG</td><td>recurrent 모델 교체 시 상태 이전에 필요한 최소 메모리를 선형 계 이론으로 도출함, 이론은 깔끔하나 로보틱스 연결과 실험 규모가 작음</td></tr>
<tr><td>552</td><td><a href='https://arxiv.org/abs/2611.19795'>Lossless First-Action Menus for Linear-Reward Planning</a></td><td>30</td><td>1</td><td>Planning</td><td>선형 보상 계획에서 첫 행동 menu의 무손실 조건을 기하적으로 특성화하고 복잡도를 증명함, 순수 이론이며 로봇 적용 근거는 없음</td></tr>
<tr><td>553</td><td><a href='https://arxiv.org/abs/2611.19807'>MAPS: A Multimodal Agentic Framework for POI Data Production Based on Crowdsourced Street-view Imagery</a></td><td>30</td><td>1</td><td>Multimodal</td><td>거리 사진에서 POI를 추출하고 DB를 갱신하는 MAPS agent를 제안하고 Kuaishou에 배포함, 응용 시스템이며 로보틱스와는 거리가 있음</td></tr>
<tr><td>554</td><td><a href='https://arxiv.org/abs/2611.20398'>Deploying a Control-Logic LLM Assistant in Air-Gapped Power Plants: Lessons in Source Authority and Bounded Retrieval</a></td><td>30</td><td>1</td><td>LLM Agent</td><td>발전소 제어 로직 LLM 보조에서 VLM 추출을 결정적 그래프 연산으로 대체한 배포 교훈을 보고함, 산업 사례 보고이며 로보틱스와는 거리가 있음</td></tr>
<tr><td>555</td><td><a href='https://arxiv.org/abs/2611.21105'>CivilBench: Benchmarking Vision-Language Models for Multimodal Information Integration in Civil Engineering</a></td><td>30</td><td>1</td><td>Multimodal</td><td>토목 공학 재난 평가용 VLM 벤치마크 CivilBench를 제안함, 도메인 벤치마크이며 로보틱스와 거리가 있음</td></tr>
<tr><td>556</td><td><a href='https://arxiv.org/abs/2611.18667'>Speaking-Clock Mamba: Phoneme-Conditioned State-Space Modeling for Visual Forced Alignment</a></td><td>30</td><td>0</td><td>Multimodal</td><td>입모양 영상 forced alignment용 Mamba 모델로 로봇과 무관함</td></tr>
<tr><td>557</td><td><a href='https://arxiv.org/abs/2611.18682'>PolarGait: Constructing Complementary Views from a Single Human Sketch for Gait Recognition</a></td><td>30</td><td>0</td><td>CV</td><td>스케치 기반 gait 인식으로 무관함</td></tr>
<tr><td>558</td><td><a href='https://arxiv.org/abs/2611.19285'>Generate, Align, and Restore: MLLM-Empowered Diffusion for Generalizable Low-light Image Enhancement</a></td><td>30</td><td>0</td><td>CV</td><td>저조도 향상 MLLM diffusion으로 무관함</td></tr>
<tr><td>559</td><td><a href='https://arxiv.org/abs/2611.19754'>Input-Space versus Feature-Level Conditioning for Robust Facial Expression Recognition</a></td><td>30</td><td>0</td><td>CV</td><td>표정 인식 조건화 비교로 무관함</td></tr>
<tr><td>560</td><td><a href='https://arxiv.org/abs/2611.19828'>PRISM: Primitive-Integrated Separable Modulation with Priority Visual Memory Queue for Compositional Zero-Shot Learning</a></td><td>30</td><td>0</td><td>CV</td><td>CZSL primitive 모듈 추가로 incremental함</td></tr>
<tr><td>561</td><td><a href='https://arxiv.org/abs/2611.20582'>SCoRe: Support-Calibrated Role Fusion for Training-Free Cross-Domain Few-Shot Segmentation</a></td><td>30</td><td>0</td><td>CV</td><td>cross-domain few-shot 분할 training-free fusion으로 incremental함</td></tr>
<tr><td>562</td><td><a href='https://arxiv.org/abs/2611.20623'>Example-Based Spatial Guidance for Training-Free Concept Erasure in Diffusion Models</a></td><td>30</td><td>0</td><td>Generative</td><td>diffusion 개념 삭제 spatial guidance로 무관함</td></tr>
<tr><td>563</td><td><a href='https://arxiv.org/abs/2611.20897'>Certified, Not Explained: Exact Token Erasure in Gated Vision State Space Models</a></td><td>30</td><td>0</td><td>CV</td><td>Mamba token erasure 인증 설명으로 로봇 무관함</td></tr>
<tr><td>564</td><td><a href='https://arxiv.org/abs/2611.20942'>vividRGB: Various visual cue detection in RGB photographs with forced focused attention</a></td><td>30</td><td>0</td><td>CV</td><td>forced focused attention 시각 단서 검출로 incremental함</td></tr>
<tr><td>565</td><td><a href='https://arxiv.org/abs/2611.21177'>RAGE: Residual-Adaptive Gating for Flow-Based Image Editing</a></td><td>30</td><td>0</td><td>Generative</td><td>flow 기반 이미지 편집 gating으로 incremental함</td></tr>
<tr><td>566</td><td><a href='https://arxiv.org/abs/2611.21290'>FM-Recon: Exploring Foundation Model Features for Accelerated Cardiac Cine MRI Reconstruction</a></td><td>30</td><td>0</td><td>CV</td><td>foundation model 특징을 cine MRI 복원 unrolled 네트워크에 넣어 본 의료 영상 탐색 연구임</td></tr>
<tr><td>567</td><td><a href='https://arxiv.org/abs/2611.21403'>Portrait Fitness as a Pretext: Probing Implicit Demographic Bias in VLMs</a></td><td>30</td><td>0</td><td>Multimodal</td><td>VLM의 얼굴 기반 인구통계 편향을 감사하는 연구라 로봇과 무관함</td></tr>
<tr><td>568</td><td><a href='https://arxiv.org/abs/2611.18769'>Gradient-Guided Hardware-Native MIXFP4</a></td><td>30</td><td>0</td><td>LG</td><td>NVFP4 타일별 E2M1과 E0M3 형식을 학습해 PPL 격차를 줄이는 양자화 커널 연구임</td></tr>
<tr><td>569</td><td><a href='https://arxiv.org/abs/2611.18933'>Geometrically Disentangling Concept Learning from the Language Modeling Loss</a></td><td>30</td><td>0</td><td>NLP</td><td>Concept Energy로 LM pretraining 중 개념 학습 시점을 보는 해석 연구임</td></tr>
<tr><td>570</td><td><a href='https://arxiv.org/abs/2611.19042'>Understanding the Role of Reasoning Data in Pretraining</a></td><td>30</td><td>0</td><td>LG</td><td>pretraining에서 atomic fact와 reasoning trace의 비중을 이론과 실험으로 분석함</td></tr>
<tr><td>571</td><td><a href='https://arxiv.org/abs/2611.19446'>Architectures and KV Replay for Depth-Recurrent Language Models</a></td><td>30</td><td>0</td><td>LG</td><td>depth-recurrent LM의 KV cache 공유로 메모리를 줄이는 구조 연구임</td></tr>
<tr><td>572</td><td><a href='https://arxiv.org/abs/2611.19477'>Grokking Can Be Steered: Selecting Desirable Solutions By Choice Of Learning Rule</a></td><td>30</td><td>0</td><td>LG</td><td>grokking에서 learning rule이 회로 크기를 정함을 보인 이론 분석임</td></tr>
<tr><td>573</td><td><a href='https://arxiv.org/abs/2611.19686'>Elicited Adaptation: Auditable Localized Fairness via Pairwise Queries</a></td><td>30</td><td>0</td><td>LG</td><td>공정성 기준 변경 시 점수 이동 비용을 분석하는 이론 연구이고 robotics와 무관함</td></tr>
<tr><td>574</td><td><a href='https://arxiv.org/abs/2611.19784'>How Should Parallel Langevin Chains Share Noise?</a></td><td>30</td><td>0</td><td>LG</td><td>병렬 Langevin chain의 noise 공유 방식을 분석하는 샘플링 이론임</td></tr>
<tr><td>575</td><td><a href='https://arxiv.org/abs/2611.19975'>Federated Dataset Simulation: Inducing Label-Free Heterogeneity Across Tasks</a></td><td>30</td><td>0</td><td>LG</td><td>라벨 없이 federated dataset 이질성을 만드는 시뮬레이션 방법을 제안함. robotics와 무관함</td></tr>
<tr><td>576</td><td><a href='https://arxiv.org/abs/2611.20020'>Improving fine-grained expressivity of graph neural networks</a></td><td>30</td><td>0</td><td>LG</td><td>GNN 표현력과 대칭 구조를 다룬 학위논문 요약이고 robotics와 무관함</td></tr>
<tr><td>577</td><td><a href='https://arxiv.org/abs/2611.20060'>Communication-Efficient Distributionally Robust Federated Averaging with Multi-Source Data</a></td><td>30</td><td>0</td><td>LG</td><td>Wasserstein ambiguity 혼합을 쓰는 distributionally robust federated averaging 이론이고 수요 예측 시뮬레이션만 검증함</td></tr>
<tr><td>578</td><td><a href='https://arxiv.org/abs/2611.20445'>Explainable Federated Learning via Global-Local Attribution Alignment</a></td><td>30</td><td>0</td><td>LG</td><td>federated learning에서 전역-지역 attribution을 정렬하는 설명 프레임워크임. robotics 무관함</td></tr>
<tr><td>579</td><td><a href='https://arxiv.org/abs/2611.20468'>Tabular Foundation Models as Emulators for Forecasting Terrestrial Ecosystem Dynamics</a></td><td>30</td><td>0</td><td>LG</td><td>TabPFN-3.5를 생태계 동역학 emulator로 DeepED와 비교함. 기후 도메인 응용임</td></tr>
<tr><td>580</td><td><a href='https://arxiv.org/abs/2611.20521'>LINK: Lightweight and Inductive Node-to-Node Propagation Rule Learning for Traffic Kriging</a></td><td>30</td><td>0</td><td>LG</td><td>traffic kriging의 node-to-node 전파 규칙 학습 LINK와 benchmark를 제안함. 교통 도메인 응용임</td></tr>
<tr><td>581</td><td><a href='https://arxiv.org/abs/2611.21215'>Open-fMIND: A Large-Scale Open-Access fMRI Corpus for Pretraining Brain Foundation Models</a></td><td>30</td><td>0</td><td>LG</td><td>fMRI 사전학습용 데이터 코퍼스 구축임. 로봇과 무관함</td></tr>
<tr><td>582</td><td><a href='https://arxiv.org/abs/2611.21267'>Conformal Expert Pools: Training-Free Probabilistic Time-Series Forecasting Beyond Seasonality</a></td><td>30</td><td>0</td><td>LG</td><td>학습 없는 시계열 예측 conformal pool임. 로봇과 무관함</td></tr>
<tr><td>583</td><td><a href='https://arxiv.org/abs/2611.21319'>Wavelet-Energy-Driven Dynamic Patching for Time Series Forecasting</a></td><td>30</td><td>0</td><td>LG</td><td>wavelet 기반 동적 patching 시계열 예측임. incremental함</td></tr>
<tr><td>584</td><td><a href='https://arxiv.org/abs/2611.21344'>TEMPO: Regime-Aware Operator Learning with Locally Adapted POD Bases</a></td><td>30</td><td>0</td><td>LG</td><td>PDE operator learning의 국소 POD 기저임. 로봇과 무관함</td></tr>
<tr><td>585</td><td><a href='https://arxiv.org/abs/2611.21348'>Representational Change Under Self-Consuming Training: A Sparse Autoencoder Analysis</a></td><td>30</td><td>0</td><td>LG</td><td>self-consuming 학습의 SAE 분석임. 로봇과 무관함</td></tr>
<tr><td>586</td><td><a href='https://arxiv.org/abs/2611.21352'>Specificity-Guided Knowledge Diversion for Decomposable Generative Models</a></td><td>30</td><td>0</td><td>LG</td><td>분해 가능한 생성 모델 사전학습 기법임. 로봇과 무관함</td></tr>
<tr><td>587</td><td><a href='https://arxiv.org/abs/2611.21584'>CertiSum: Bitwise-Identical MXFP4 Training Across Platforms and Parallelism Layouts</a></td><td>30</td><td>0</td><td>LG</td><td>MXFP4 학습의 bitwise 재현성 확보임. 로봇과 무관함</td></tr>
<tr><td>588</td><td><a href='https://arxiv.org/abs/2611.21597'>Optimal Autoregressive Chain-of-Thought Learning via Bagging</a></td><td>30</td><td>0</td><td>LG</td><td>CoT 학습의 bagging 기반 최적성 이론임. 로봇과 무관함</td></tr>
<tr><td>589</td><td><a href='https://arxiv.org/abs/2611.18592'>Endogenous Preferences as Vulnerability Signals: Discovering Universal Adversarial Triggers for LLM Utility Degradation</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 효용 저하용 universal adversarial trigger 탐색임. 로봇과 거리 있음</td></tr>
<tr><td>590</td><td><a href='https://arxiv.org/abs/2611.18617'>Intrinsic Attention as Navigator: A Non-Generative Retrieval Method for Multi-Hop Queries</a></td><td>30</td><td>0</td><td>NLP</td><td>attention 기반 multi-hop retrieval임. 로봇과 무관함</td></tr>
<tr><td>591</td><td><a href='https://arxiv.org/abs/2611.19840'>Grounding Language Models in Speech Does Not Fix &quot;AI Flavor&quot;: Calibrated LLM Judges, Goodhart Traps, and a Preference-Tuning Fix</a></td><td>30</td><td>0</td><td>NLP</td><td>음성 grounding이 중국어 AI flavor를 줄이지 못한다는 부정 결과와 LLM judge 기반 DPO를 보고함. 0.6B 소규모 실험이고 로봇과 무관함</td></tr>
<tr><td>592</td><td><a href='https://arxiv.org/abs/2611.19862'>Bioformer-RetroMAE: retrieval-oriented pretraining of a compact biomedical language model for literature search</a></td><td>30</td><td>0</td><td>NLP</td><td>RetroMAE 사전학습으로 43M 생의학 retrieval encoder를 만들어 BioASQ에서 BioBERT 대비 개선함. 기존 기법의 도메인 적용임</td></tr>
<tr><td>593</td><td><a href='https://arxiv.org/abs/2611.20129'>Can decision models extract clinical data from cancer pathology reports? An evaluation of accuracy, calibration, and failure modes</a></td><td>30</td><td>0</td><td>NLP</td><td>decision model이 암 병리 보고서 필드 추출에서 생성 모델과 비슷한 정확도를 내는지 평가함. 임상 평가 연구이며 로봇과 무관함</td></tr>
<tr><td>594</td><td><a href='https://arxiv.org/abs/2611.20216'>FIDEL: Abugida-Aware Pre-tokenization for Ethiopic Languages</a></td><td>30</td><td>0</td><td>NLP</td><td>에티오피아 abugida 문자용 pre-tokenization FIDEL을 제안함. 저자원 언어 tokenizer 개선이며 task별 결과가 엇갈림</td></tr>
<tr><td>595</td><td><a href='https://arxiv.org/abs/2611.20566'>Weight-Space Programming Changes How an LLM Uses Python for Computational Biology</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM이 다른 모델 가중치를 직접 편집해 Python 계산생물학 문제 성능을 높임. 0.8B 모델과 50문제 한정이며 일반성이 약함</td></tr>
<tr><td>596</td><td><a href='https://arxiv.org/abs/2611.20695'>IndustrialKnowEval: A Benchmark for Evaluating Multi-Level Industrial Knowledge in LLMs</a></td><td>30</td><td>0</td><td>NLP</td><td>산업 지식 QA benchmark 43,282개와 ICCG 지표를 제시함. 도메인 benchmark 구축이며 로봇과 무관함</td></tr>
<tr><td>597</td><td><a href='https://arxiv.org/abs/2611.20728'>ANCHOR: Cluster-Grounded 5W1H Extraction via Large-Small Model Collaboration</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM과 소형 모델을 결합한 cluster 기반 5W1H 추출 ANCHOR와 dataset을 제안함. 정보 추출 엔지니어링임</td></tr>
<tr><td>598</td><td><a href='https://arxiv.org/abs/2611.20924'>Navital Gym: Rule-Graded Agent Environments for Indian Workflows</a></td><td>30</td><td>0</td><td>NLP</td><td>인도 워크플로 6개 환경 321개 과제의 rule 채점 agent gym을 공개함. 지역 특화 benchmark이며 Opus가 321개 중 315개를 풀어 변별력이 약함</td></tr>
<tr><td>599</td><td><a href='https://arxiv.org/abs/2611.21001'>Does the Voice Matter? Evaluating Frustration Detection on Deployed Clinical Voice-Agent Calls</a></td><td>30</td><td>0</td><td>NLP</td><td>임상 음성 agent 통화에서 전사만으로 좌절 감지가 되는지 평가함. 소규모 표본이며 audio 이득이 모델별로 엇갈림</td></tr>
<tr><td>600</td><td><a href='https://arxiv.org/abs/2611.21458'>A Scalable Multi Task Learning Framework for Modeling Demographic Disagreements in Annotation Tasks</a></td><td>30</td><td>0</td><td>NLP</td><td>annotator 인구집단 간 불일치를 gradient routing multi-task로 모델링하는 SAJ-MTL을 제안함. 독성 탐지 한정임</td></tr>
<tr><td>601</td><td><a href='https://arxiv.org/abs/2611.18971'>Three Invisible Failure Modes in Speech-Based Age Estimation for Child Safety</a></td><td>30</td><td>0</td><td>AI</td><td>음성 기반 아동 나이 추정에서 세 가지 조용한 실패 모드를 발견함. 파이프라인 보고 성격이고 로봇과 무관함</td></tr>
<tr><td>602</td><td><a href='https://arxiv.org/abs/2611.19166'>LABEL: Literature Asymmetry between Efficacy and Limits in Drug Knowledge and Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>약물 금기 사실이 문헌에서 적게 기록되어 LLM이 이를 반영함을 보임. 의료 분석이며 로봇과 무관함</td></tr>
<tr><td>603</td><td><a href='https://arxiv.org/abs/2611.19215'>Mem2Fair: Online Fairness Control for Text-to-Video Generation via Fair Memory</a></td><td>30</td><td>0</td><td>Video</td><td>T2V 생성의 인구통계 공정성을 Fair Memory로 online 제어함. 로봇과 무관한 공정성 응용임</td></tr>
<tr><td>604</td><td><a href='https://arxiv.org/abs/2611.19779'>Read Before You Fit: Text-Derived Constraints for Discovering Differential Equations from Noisy Biological Data</a></td><td>30</td><td>0</td><td>LG</td><td>생물 시스템 ODE 발견에 텍스트 제약을 쓰는 P2C agent를 제안함, 소수 ODE 시스템 평가이며 로보틱스와 무관함</td></tr>
<tr><td>605</td><td><a href='https://arxiv.org/abs/2611.20423'>FinVerify: A Verification Framework for Financial Agents</a></td><td>30</td><td>0</td><td>LLM Agent</td><td>금융 agent의 수치 주장을 결정적 검증기와 Z3로 확인하는 FinVerify를 제안함, 금융 도메인이며 로보틱스와 무관함</td></tr>
<tr><td>606</td><td><a href='https://arxiv.org/abs/2611.20484'>Agent-Guided Configuration Tuning for SMT Solvers</a></td><td>30</td><td>0</td><td>LLM Agent</td><td>LLM agent가 cvc5 SMT 설정을 튜닝해 일부 division에서 향상시킴, 솔버 튜닝이며 로보틱스와 무관함</td></tr>
<tr><td>607</td><td><a href='https://arxiv.org/abs/2611.20779'>EEGProbe: Do Vision-Language Models Really Understand EEG? A Benchmark for Signal-Grounded EEG Signals Evaluation</a></td><td>30</td><td>0</td><td>Multimodal</td><td>VLM이 EEG 신호를 이해하는지 620문항으로 재는 EEGProbe 벤치마크임, 최고 모델이 41.63%에 그치나 생체신호 도메인이며 로보틱스와 무관함</td></tr>
<tr><td>608</td><td><a href='https://arxiv.org/abs/2611.20882'>Accelerate Bench: Evaluating Agents for Application-Level Program Optimization</a></td><td>30</td><td>0</td><td>LLM Agent</td><td>CPU 프로그램 최적화 32개 과제로 coding agent를 평가하는 Accelerate Bench를 제안함, 소프트웨어 최적화 벤치마크이며 로보틱스와 무관함</td></tr>
<tr><td>609</td><td><a href='https://arxiv.org/abs/2611.21407'>Harness Leverage Across Model Size: A Ladder of Five Local Agent Harnesses from 0.75B to 4.7B</a></td><td>30</td><td>0</td><td>LLM Agent</td><td>0.75B~4.7B 로컬 모델 위에서 agent harness 5종의 효과를 360개 셀로 비교함, 엄밀한 paired 비교이나 로보틱스와 무관함</td></tr>
<tr><td>610</td><td><a href='https://arxiv.org/abs/2611.20720'>AVD: A Multi-Sensor Teleoperated Wheelchair Platform with Safety-Aware Control</a></td><td>28</td><td>3</td><td>Robotics</td><td>원격 조종 휠체어 플랫폼임. 시스템 설명 위주임</td></tr>
<tr><td>611</td><td><a href='https://arxiv.org/abs/2611.20978'>Inverse Kinematics in Endoscopic Scenarios using MoveIt</a></td><td>28</td><td>3</td><td>Robotics</td><td>내시경 IK의 MoveIt 솔버 benchmark임. 기여 약함</td></tr>
<tr><td>612</td><td><a href='https://arxiv.org/abs/2611.19640'>Floorplan-Context-Aware Cross-Environment Human Activity Recognition from mmWave Radar Point Clouds</a></td><td>28</td><td>1</td><td>CV</td><td>mmWave 활동 인식 도면 context로 센서 응용임</td></tr>
<tr><td>613</td><td><a href='https://arxiv.org/abs/2611.20431'>UrbanTwin Sim2Real LiDAR Challenge 2026: Site-Calibrated Synthetic Data and Multi-Detector Fusion for Roadside 3D Detection</a></td><td>28</td><td>1</td><td>3D Vision</td><td>LiDAR sim2real 챌린지 보고서로 engineering 위주임</td></tr>
<tr><td>614</td><td><a href='https://arxiv.org/abs/2611.20853'>Motor Imagery Classification Using Hybrid Cross-Subject Class Mixup and Selective Attention</a></td><td>28</td><td>1</td><td>LG</td><td>EEG-fNIRS motor imagery 분류에 cross-subject mixup과 selective attention을 적용함. BCI 응용이고 개선이 incremental임</td></tr>
<tr><td>615</td><td><a href='https://arxiv.org/abs/2611.20686'>UbiHearo: Bringing Scenario-Aware Sound Guidance to DHH Users with Mobile Agents</a></td><td>28</td><td>1</td><td>Multimodal</td><td>청각장애 사용자를 위한 모바일 소리 안내 agent UbiHearo를 제안함, HCI 응용이며 로보틱스와 거리가 있음</td></tr>
<tr><td>616</td><td><a href='https://arxiv.org/abs/2611.18669'>LogicEye: Agent Driven Multimodal Dataset for Interpretable Ophthalmic Diagnosis</a></td><td>28</td><td>0</td><td>CV</td><td>안과 진단 데이터셋으로 도메인 특화임</td></tr>
<tr><td>617</td><td><a href='https://arxiv.org/abs/2611.18729'>SCALE: Towards whole-slide counterfactual explanations in pathology</a></td><td>28</td><td>0</td><td>CV</td><td>병리 counterfactual 설명으로 로봇 무관함</td></tr>
<tr><td>618</td><td><a href='https://arxiv.org/abs/2611.18865'>FiReIQ: Field-Level Confidence Estimation with Reasoning and Image Quality in Document Extraction</a></td><td>28</td><td>0</td><td>Multimodal</td><td>문서 추출 필드 confidence 추정으로 무관함</td></tr>
<tr><td>619</td><td><a href='https://arxiv.org/abs/2611.19156'>From zero-target transfer to target-site personalization: multi-source training across fall-detection models</a></td><td>28</td><td>0</td><td>CV</td><td>낙상 검출 다중 소스 학습으로 응용 위주임</td></tr>
<tr><td>620</td><td><a href='https://arxiv.org/abs/2611.19527'>PathLoop: Self-Evolving Multi-Agent Reasoning for Evidence-Grounded Whole-Slide Image Analysis</a></td><td>28</td><td>0</td><td>Multimodal</td><td>병리 WSI multi-agent 추론으로 무관함</td></tr>
<tr><td>621</td><td><a href='https://arxiv.org/abs/2611.19780'>A Threshold-Free Visual-Semantic Matching Metric for Evaluating Consistency in Subject-Driven Image Generation</a></td><td>28</td><td>0</td><td>Generative</td><td>subject-driven 생성 일관성 지표로 무관함</td></tr>
<tr><td>622</td><td><a href='https://arxiv.org/abs/2611.20992'>MedJev: A System One Vision-Language Decision Model for Fast and Effective Medical Image Understanding</a></td><td>28</td><td>0</td><td>Multimodal</td><td>의료 VLM System-1 결정 모델로 도메인 특화임</td></tr>
<tr><td>623</td><td><a href='https://arxiv.org/abs/2611.21077'>MORE: Merge Once, Route Early for Training-Free Multi-Subject Composition from Large LoRA Pools</a></td><td>28</td><td>0</td><td>Generative</td><td>LoRA 다중 주체 합성 training-free로 무관함</td></tr>
<tr><td>624</td><td><a href='https://arxiv.org/abs/2611.21132'>Region-VAD: Video Anomaly Localization and Detection via Region Selection</a></td><td>28</td><td>0</td><td>Video</td><td>video anomaly 지역 선택으로 incremental함</td></tr>
<tr><td>625</td><td><a href='https://arxiv.org/abs/2611.21304'>Fix, Don&#x27;t Retake: Physics-Simulated Training for Correcting Patient Positioning Errors in Dental Panoramic Radiographs</a></td><td>28</td><td>0</td><td>CV</td><td>치과 파노라마 촬영 위치 오류를 시뮬레이션 데이터로 교정하는 의료 응용 비교 연구임</td></tr>
<tr><td>626</td><td><a href='https://arxiv.org/abs/2611.21412'>Flexible Multi-Stack Super-Resolution of Clinical Brain MRI Using Hetero-Orientation Variational Encoding: Expert Reader Evaluation in a Nigerian Cohort</a></td><td>28</td><td>0</td><td>CV</td><td>다중 스택 뇌 MRI 초해상도 방법으로 의료 영상 분야임</td></tr>
<tr><td>627</td><td><a href='https://arxiv.org/abs/2611.21565'>When Do Histology Foundation Models Need Geometric Test-Time Augmentation?</a></td><td>28</td><td>0</td><td>CV</td><td>조직병리 foundation model에서 D4 TTA의 이득을 측정한 벤치마크 연구임</td></tr>
<tr><td>628</td><td><a href='https://arxiv.org/abs/2611.18598'>Not All Data Leakage Is Equal: A Controlled Benchmark of Evaluation Inflation in Tabular Classification</a></td><td>28</td><td>0</td><td>LG</td><td>표 형식 분류에서 데이터 누수 유형별 평가 부풀림을 측정한 통제 실험임</td></tr>
<tr><td>629</td><td><a href='https://arxiv.org/abs/2611.18657'>SART: Sign-Absolute Reformulation Theory for Binary Variable Reduction in Neural Network Verification</a></td><td>28</td><td>0</td><td>LG</td><td>ReLU 신경망 검증의 이진 변수 수를 줄이는 이론이며 로봇 안전 검증과 간접적으로만 이어짐</td></tr>
<tr><td>630</td><td><a href='https://arxiv.org/abs/2611.19020'>Advancing the Calibration-Compute Frontier of LLM Classifiers via Asymmetric Duos</a></td><td>28</td><td>0</td><td>LG</td><td>큰 모델과 작은 모델의 logit 융합으로 LLM 분류기 보정을 개선하는 단순 방법임</td></tr>
<tr><td>631</td><td><a href='https://arxiv.org/abs/2611.19072'>Nahual: A Sequence Model for Language and Atoms</a></td><td>28</td><td>0</td><td>LG</td><td>텍스트와 3D 분자를 함께 다루는 autoregressive diffusion 모델로 화학 분야임</td></tr>
<tr><td>632</td><td><a href='https://arxiv.org/abs/2611.19542'>Func-JEPA: Learning a Sobolev Space of Functions as Latent Vectors</a></td><td>28</td><td>0</td><td>LG</td><td>함수를 Sobolev 공간 latent로 학습하는 JEPA이며 기호 수학 분야임</td></tr>
<tr><td>633</td><td><a href='https://arxiv.org/abs/2611.19650'>With the Right Representation, Classical Machine Learning Rivals Deep Models for Olfactory Mixture Similarity</a></td><td>28</td><td>0</td><td>LG</td><td>후각 혼합물 유사도에서 비교 feature를 쓴 XGBoost가 deep model에 맞먹는다는 소규모 분석임</td></tr>
<tr><td>634</td><td><a href='https://arxiv.org/abs/2611.19965'>Evaluating Near-Perfect Accuracy Claims in Machine-Learning-Based Leak Detection for Two-Phase Pipelines: A Condition-Blocked Audit</a></td><td>28</td><td>0</td><td>LG</td><td>two-phase 파이프라인 누수 탐지의 평가 프로토콜 감사로 정확도가 93.3%에서 59.1%로 떨어짐을 보임. 도메인 한정임</td></tr>
<tr><td>635</td><td><a href='https://arxiv.org/abs/2611.20036'>Machine Learning for Near Real-Time Identification of Wildfire Burned Areas</a></td><td>28</td><td>0</td><td>CV</td><td>pix2pix로 Landsat 지수에서 산불 소실 확률을 근사하는 위성 응용이며 방법이 단순함</td></tr>
<tr><td>636</td><td><a href='https://arxiv.org/abs/2611.20352'>EPI-SST: Renewal-Structured State-Space Transformers for Epidemic Forecasting</a></td><td>28</td><td>0</td><td>LG</td><td>renewal 구조 state-space transformer로 독감 예측 RMSE를 낮추는 역학 도메인 응용임</td></tr>
<tr><td>637</td><td><a href='https://arxiv.org/abs/2611.20493'>A Temporal Convolutional Network with Multi-Head Attention Model: A Surrogate for Parallel DEVS Semiconductor Fab Simulation</a></td><td>28</td><td>0</td><td>LG</td><td>반도체 fab 시뮬레이션 대리 모델로 TCN과 attention을 결합한 도메인 응용임</td></tr>
<tr><td>638</td><td><a href='https://arxiv.org/abs/2611.20621'>GPromptShield: Elevating Resilience in Graph Prompt Tuning against Adversarial Attacks</a></td><td>28</td><td>0</td><td>LG</td><td>그래프 prompt tuning의 적대적 공격 방어를 제안함. robotics 무관함</td></tr>
<tr><td>639</td><td><a href='https://arxiv.org/abs/2611.20975'>STORMGUIDE-FL: Stochastic Remote Guidance for Efficient Mining of Federated Streaming Data</a></td><td>28</td><td>0</td><td>LG</td><td>federated 스트리밍 데이터의 concept drift를 서버 guidance로 줄이는 최적화 프레임워크임</td></tr>
<tr><td>640</td><td><a href='https://arxiv.org/abs/2611.20996'>Explaining Cross-Label Decision Structure in Multi-Output Tree Ensembles</a></td><td>28</td><td>0</td><td>LG</td><td>multi-output 트리 앙상블의 label 간 공유 결정 구조를 설명하는 ms-DPG를 제안함. robotics 무관함</td></tr>
<tr><td>641</td><td><a href='https://arxiv.org/abs/2611.21276'>Classical structural priors improve neural molecular representations in molecule language models</a></td><td>28</td><td>0</td><td>LG</td><td>분자 언어 모델에 고전 구조 prior 추가임. 로봇과 무관함</td></tr>
<tr><td>642</td><td><a href='https://arxiv.org/abs/2611.21310'>Can AI Mature a Model&#x27;s Geometry? Training-Free Weight Baking in LLMs</a></td><td>28</td><td>0</td><td>LG</td><td>LLM 가중치 geometry를 training-free로 조정함. 근거 약함</td></tr>
<tr><td>643</td><td><a href='https://arxiv.org/abs/2611.21562'>Severe but Harmless: Stress-Testing Shift Severity for Frozen Time-Series Forecasters</a></td><td>28</td><td>0</td><td>LG</td><td>시계열 foundation model의 shift 강건성 평가임. 로봇과 무관함</td></tr>
<tr><td>644</td><td><a href='https://arxiv.org/abs/2611.21608'>Latent Lattice Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>latent lattice로 토큰당 계산을 늘리는 LM 구조임. 로봇과 무관함</td></tr>
<tr><td>645</td><td><a href='https://arxiv.org/abs/2611.18588'>Automating literature screening and knowledge synthesis with large language models</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM으로 문헌 스크리닝과 지식 종합을 자동화함. 로봇과 무관함</td></tr>
<tr><td>646</td><td><a href='https://arxiv.org/abs/2611.18601'>Jailbreak LLMs with Linguistic Style as a Hidden Attack Surface</a></td><td>28</td><td>0</td><td>NLP</td><td>언어 스타일 기반 jailbreak 공격임. 로봇과 무관함</td></tr>
<tr><td>647</td><td><a href='https://arxiv.org/abs/2611.18663'>Criterion-Activated Preference Synthesis: Attribution-Preserving Preference Data from Explicit Standards</a></td><td>28</td><td>0</td><td>NLP</td><td>기준 기반 선호 데이터 합성으로 DPO 개선함. 로봇과 무관함</td></tr>
<tr><td>648</td><td><a href='https://arxiv.org/abs/2611.18851'>KUDEX: A Zero-Shot Decompositional Framework for Logical Analysis in Natural Language</a></td><td>28</td><td>0</td><td>NLP</td><td>zero-shot 논리 분해 프레임워크임. 로봇과 무관함</td></tr>
<tr><td>649</td><td><a href='https://arxiv.org/abs/2611.19075'>The Geometry of Conceptors in Neural-Activation Spaces</a></td><td>28</td><td>0</td><td>NLP</td><td>conceptor의 활성 공간 geometry임. 로봇과 무관함</td></tr>
<tr><td>650</td><td><a href='https://arxiv.org/abs/2611.19802'>Machine interpreting competitiveness: a discourse-sensitive comparison of meaning and target-language quality in English-Chinese simultaneous interpreting</a></td><td>28</td><td>0</td><td>NLP</td><td>상용 기계 통역과 사람 통역사를 영중 동시통역에서 비교한 언어학 연구임. ML 기여와 로봇 관련성이 없음</td></tr>
<tr><td>651</td><td><a href='https://arxiv.org/abs/2611.19858'>Bridging the Terminology Gap: A Data-Centric Alignment Framework for Multilingual Translation in Cross-Border Corporation</a></td><td>28</td><td>0</td><td>NLP</td><td>용어 정렬 데이터 합성과 SFT+RL로 기업 번역 용어 정확도를 높임. 산업 배포용 데이터 중심 엔지니어링임</td></tr>
<tr><td>652</td><td><a href='https://arxiv.org/abs/2611.20062'>Mandarin Wh-Indefinites Follow Nonveridicality in Multilingual LLMs, Unlike English any</a></td><td>28</td><td>0</td><td>NLP</td><td>다국어 LLM이 만다린 wh-indefinite의 nonveridical 허가를 영어 any와 다르게 다루는지 조사함. 언어학 분석이며 로봇과 무관함</td></tr>
<tr><td>653</td><td><a href='https://arxiv.org/abs/2611.20158'>Who Can You Hide Behind? Author-Conditioned Style Transfer and the Evasion of a Commercial AI-Text Detector</a></td><td>28</td><td>0</td><td>NLP</td><td>저자 문체 prompt로 AI 텍스트 탐지기를 회피한 현상을 한 탐지기에서만 측정함. baseline과 의미 보존 평가가 없음</td></tr>
<tr><td>654</td><td><a href='https://arxiv.org/abs/2611.20734'>Can LLMs Give Good Product Advice? A Framework for Diagnosing Failures</a></td><td>28</td><td>0</td><td>NLP</td><td>제품 추천 실패를 19개 failure mode로 진단하는 프레임워크를 제안함. 평가 설계가 주이고 로봇과 무관함</td></tr>
<tr><td>655</td><td><a href='https://arxiv.org/abs/2611.19061'>Large Language Models for AI Infrastructure</a></td><td>28</td><td>0</td><td>AI</td><td>AI 인프라용 LLM 방법을 정리한 survey임. 로봇과 무관함</td></tr>
<tr><td>656</td><td><a href='https://arxiv.org/abs/2611.19110'>CLEAR: Legible and Steerable Recommendation via Grounded Natural-Language Interests</a></td><td>28</td><td>0</td><td>LG</td><td>편집 가능한 자연어 관심사 계층의 추천 시스템 CLEAR를 Meta에 배포함. 산업 추천 시스템이며 로봇과 무관함</td></tr>
<tr><td>657</td><td><a href='https://arxiv.org/abs/2611.19525'>Objectify, Don&#x27;t Delete: Complaint-Derived Evaluation of Ambient Clinical Notes</a></td><td>28</td><td>0</td><td>NLP</td><td>임상 노트 평가 기준을 complaint에서 추출해 objectify하는 파이프라인을 제안함, 의료 NLP로 로보틱스와 무관함</td></tr>
<tr><td>658</td><td><a href='https://arxiv.org/abs/2611.19564'>Behavioral Assurance for Socially Deployed AI Agents</a></td><td>28</td><td>0</td><td>LLM Agent</td><td>사회적 배치 AI agent의 행동 일관성을 다섯 축으로 측정하는 평가 틀을 제안함, 예비 분석 수준이고 로보틱스와 무관함</td></tr>
<tr><td>659</td><td><a href='https://arxiv.org/abs/2611.20031'>Towards Agentic Scientific Discovery in Distributed Systems</a></td><td>28</td><td>0</td><td>LLM Agent</td><td>분산 클라이언트에서 공통 수식을 찾는 query 조건부 tool 선택 Query-ATLAS를 제안함, 개선이 과제 의존적이고 로보틱스와 무관함</td></tr>
<tr><td>660</td><td><a href='https://arxiv.org/abs/2611.20983'>GRACE: Parallel Best-of-N Multi-Agent Analysis of Closed-Form Questions over Dataframes with Guardrail Selection and Adaptive Retry</a></td><td>28</td><td>0</td><td>LLM Agent</td><td>dataframe 질의에 병렬 best-of-N과 guardrail 선택을 쓰는 GRACE를 제안함, 데이터 분석 파이프라인이며 로보틱스와 무관함</td></tr>
<tr><td>661</td><td><a href='https://arxiv.org/abs/2611.21235'>Language-model agents&#x27; beliefs can be manipulated via truthful evidence in open channel</a></td><td>28</td><td>0</td><td>LLM Agent</td><td>진실한 트윗 조각을 몽타주로 배열해 LLM agent가 루머를 65% 이상 수용하게 만드는 Generative Montage를 보임, 사회적 조작 연구이며 로보틱스와 무관함</td></tr>
<tr><td>662</td><td><a href='https://arxiv.org/abs/2611.21273'>CAE-Bench: Benchmarking AI Agents for Reusable CAE Solver Development</a></td><td>28</td><td>0</td><td>LLM Agent</td><td>CAE solver 개발 agent의 held-out 일반화를 80개 과제로 평가하는 CAE-Bench를 제안함, 수치해석 도메인이며 로보틱스와 무관함</td></tr>
<tr><td>663</td><td><a href='https://arxiv.org/abs/2611.21382'>VisualArtifactSpec 1.0: Evaluating Visual Artifacts under Task Specifications</a></td><td>28</td><td>0</td><td>LLM Agent</td><td>슬라이드, 영상, 웹 등 시각 산출물 211개 과제를 평가하는 VisualArtifactSpec을 제안함, 로보틱스와 무관함</td></tr>
<tr><td>664</td><td><a href='https://arxiv.org/abs/2611.21441'>Learning to Reason with Predictive Gains for Generative Recommendation</a></td><td>28</td><td>0</td><td>RecSys</td><td>추천 reasoning을 Semantic ID log-likelihood 변화로 문장 단위 보상하는 GainReason을 제안함, 추천 시스템 벤치마크 개선이며 로보틱스와 무관함</td></tr>
<tr><td>665</td><td><a href='https://arxiv.org/abs/2611.21520'>Safe Resemblance, Silent Propagation: Limits of Text-Similarity Guardrails for AI Agent Safety</a></td><td>28</td><td>0</td><td>LLM Safety</td><td>텍스트 유사도 guardrail이 agent 간 prompt injection 전파를 놓침을 3-agent 이메일 릴레이로 보임, 보안 평가이며 로보틱스와 무관함</td></tr>
<tr><td>666</td><td><a href='https://arxiv.org/abs/2611.21545'>Right Reason, Wrong Advice: Evaluating Recourse in LLM Explanations of Denied Requests</a></td><td>28</td><td>0</td><td>NLP</td><td>거부 설명이 따라 해도 결정이 바뀌지 않는 recourse validity를 정확히 계산해 LLM 20종을 평가함, 정책 설명 주제이며 로보틱스와 무관함</td></tr>
<tr><td>667</td><td><a href='https://arxiv.org/abs/2611.19385'>Does a completed simulation run mean a usable urban wind result for AI agents?</a></td><td>27</td><td>0</td><td>LLM Agent</td><td>urban wind CFD를 LLM agent가 수행할 때 결과 검증을 붙인 벤치마크와 WindPilot을 제안함, 도메인 특화이고 로보틱스와 무관함</td></tr>
<tr><td>668</td><td><a href='https://arxiv.org/abs/2611.19530'>LLM Trading Agents Earn Beta, Not Alpha: A Look-Ahead-Free Benchmark</a></td><td>27</td><td>0</td><td>LLM Agent</td><td>LLM 트레이딩 agent가 alpha 없이 beta만 얻음을 look-ahead 없는 백테스트로 보임, 금융 평가이며 로보틱스와 무관함</td></tr>
<tr><td>669</td><td><a href='https://arxiv.org/abs/2611.18965'>Contextual Non-Convex Bandit Optimization with Two-Point Feedback</a></td><td>26</td><td>1</td><td>LG</td><td>two-point feedback contextual bandit의 regret 이론으로 로봇과 직접 연결은 약함</td></tr>
<tr><td>670</td><td><a href='https://arxiv.org/abs/2611.19027'>HeteroWear: Sensor-Aware Self-Supervised Learning for Heterogeneous Wearable Activity Recognition</a></td><td>26</td><td>1</td><td>LG</td><td>이종 웨어러블 센서 활동 인식용 self-supervised 사전학습 방법임</td></tr>
<tr><td>671</td><td><a href='https://arxiv.org/abs/2611.19561'>Read, Then Shade? How Visual Evidence Changes Incentive-Driven Misreporting in Vision-Language Advisors</a></td><td>26</td><td>1</td><td>Multimodal</td><td>VLM 보고자가 보상에 따라 값을 왜곡하는지 합성 장면으로 본 소형 모델 실험임</td></tr>
<tr><td>672</td><td><a href='https://arxiv.org/abs/2611.18717'>LVRE: A Local Visual Reasoning and Editing Agent for Optical Chemical Structure Recognition</a></td><td>26</td><td>0</td><td>Multimodal</td><td>화학 구조 인식 agent로 무관함</td></tr>
<tr><td>673</td><td><a href='https://arxiv.org/abs/2611.18771'>Agri-MRAG: Parameter-Enhanced Multimodal Retrieval-Augmented Generation for Agricultural Visual Question Answering</a></td><td>26</td><td>0</td><td>Multimodal</td><td>농업 VQA RAG로 도메인 특화임</td></tr>
<tr><td>674</td><td><a href='https://arxiv.org/abs/2611.18790'>Same Evidence, Different Verdicts: Delivery of CT Images and DICOM Metadata Changes VLM Quality-Control Decisions</a></td><td>26</td><td>0</td><td>Multimodal</td><td>CT와 DICOM 메타데이터 VLM 품질관리 분석으로 무관함</td></tr>
<tr><td>675</td><td><a href='https://arxiv.org/abs/2611.19475'>StyleJudge: A Human-Validated, In-Context-Learning Vision-Language Evaluator for Artistic Style Transfer</a></td><td>26</td><td>0</td><td>Multimodal</td><td>스타일 전이 평가 VLM으로 무관함</td></tr>
<tr><td>676</td><td><a href='https://arxiv.org/abs/2611.19576'>Consistency-Aware Map Generation at Multiple Zoom Levels Using Aerial Image</a></td><td>26</td><td>0</td><td>CV</td><td>항공영상 다중 줌 지도 생성으로 무관함</td></tr>
<tr><td>677</td><td><a href='https://arxiv.org/abs/2611.19939'>Two-Stage Prompt Learning: A Unified Framework for Person ReID without Clothing Hypothesis</a></td><td>26</td><td>0</td><td>CV</td><td>의류 무관 ReID prompt 학습으로 무관함</td></tr>
<tr><td>678</td><td><a href='https://arxiv.org/abs/2611.20183'>GeoReVis: Learning Selective Revision and Evidence Consolidation for Remote Sensing Segmentation</a></td><td>26</td><td>0</td><td>CV</td><td>원격탐사 언어 분할 revision으로 무관함</td></tr>
<tr><td>679</td><td><a href='https://arxiv.org/abs/2611.20625'>ASCG: Adaptive Spatial Classifier Guidance for Surgical Concept Suppression in Diffusion Models</a></td><td>26</td><td>0</td><td>Generative</td><td>수술 개념 억제 diffusion 가이던스로 무관함</td></tr>
<tr><td>680</td><td><a href='https://arxiv.org/abs/2611.20805'>An Efficient Training Paradigm for Image Restoration via Improved Fréchet Loss</a></td><td>26</td><td>0</td><td>CV</td><td>영상 복원 Fréchet loss 학습으로 무관함</td></tr>
<tr><td>681</td><td><a href='https://arxiv.org/abs/2611.21107'>Source-Free Domain Adaptation for Multi-Label Image Classification: A Framework, Baselines, and Benchmark</a></td><td>26</td><td>0</td><td>CV</td><td>다중 라벨 SFDA 벤치마크로 무관함</td></tr>
<tr><td>682</td><td><a href='https://arxiv.org/abs/2611.21131'>How to Explain your Unexplainable Video Anomaly Detector</a></td><td>26</td><td>0</td><td>Video</td><td>video anomaly 검출기 설명으로 무관함</td></tr>
<tr><td>683</td><td><a href='https://arxiv.org/abs/2611.21419'>Quality and Similarity Indicators for Video-Based Heart Rate and Respiratory Rate Fusion: A Controlled Evaluation</a></td><td>26</td><td>0</td><td>CV</td><td>영상 기반 심박과 호흡 추정 융합 지표를 비교한 생체신호 평가 연구임</td></tr>
<tr><td>684</td><td><a href='https://arxiv.org/abs/2611.21563'>Wildfire-SSR: Geolocation-Aware Multimodal Fusion for Structure-Level Wildfire Risk Assessment</a></td><td>26</td><td>0</td><td>CV</td><td>위성과 거리뷰를 합친 산불 건물 위험 평가 응용 연구임</td></tr>
<tr><td>685</td><td><a href='https://arxiv.org/abs/2611.18640'>SERAG: SEmantical and Relational approach for Anomaly detection on knowledge Graphs</a></td><td>26</td><td>0</td><td>NLP</td><td>지식 그래프 이상 탐지에 의미와 관계 점수를 융합한 합성 이상 중심 연구임</td></tr>
<tr><td>686</td><td><a href='https://arxiv.org/abs/2611.19207'>On-policy distillation as a Backdoor Propagation Channel</a></td><td>26</td><td>0</td><td>NLP</td><td>on-policy distillation이 backdoor 전파 통로가 될 수 있음을 보인 보안 연구임</td></tr>
<tr><td>687</td><td><a href='https://arxiv.org/abs/2611.19250'>Learning Graph-Conditioned Predictors in Weight Space</a></td><td>26</td><td>0</td><td>LG</td><td>노드 구조에 따라 predictor 가중치를 생성하는 그래프 학습 방법임</td></tr>
<tr><td>688</td><td><a href='https://arxiv.org/abs/2611.19304'>A Backdoor Trigger Is Legible in Fine-Tune Weights</a></td><td>26</td><td>0</td><td>LG</td><td>fine-tune 가중치만 읽어 backdoor trigger 토큰을 찾는 정적 통계량을 제시한 LLM 보안 연구임</td></tr>
<tr><td>689</td><td><a href='https://arxiv.org/abs/2611.20587'>Stability Principle Inherent in Wheel Gait of Planar X-shaped Walker Generated Using Constant Torque Drive and Mechanical Stoppers</a></td><td>25</td><td>2</td><td>Mechanism</td><td>X자 walker의 수동 보행 안정성 분석임. 학습 무관함</td></tr>
<tr><td>690</td><td><a href='https://arxiv.org/abs/2611.18636'>Predictive maintenance in manufacturing: The operational value of continual machine learning</a></td><td>25</td><td>1</td><td>LG</td><td>제조 예지 정비에 continual learning을 적용해 Bosch 데이터로 비용 지표를 비교한 응용 연구임</td></tr>
<tr><td>691</td><td><a href='https://arxiv.org/abs/2611.18674'>SynPanZ: A Synthetic Dataset to Improve Multi-Animal Pose Estimation in Chimpanzees (Pan troglodytes)</a></td><td>25</td><td>0</td><td>CV</td><td>침팬지 pose 합성 데이터셋으로 로봇 무관함</td></tr>
<tr><td>692</td><td><a href='https://arxiv.org/abs/2611.18686'>3D Cell Morphology--Clinical Text Contrastive Learning with Voxel Swin Transformer and Finding Encoder Domain-Adaptation</a></td><td>25</td><td>0</td><td>CV</td><td>3D 세포 형태 대조학습으로 의료 특화임</td></tr>
<tr><td>693</td><td><a href='https://arxiv.org/abs/2611.18587'>Quantize, Qualify, Rerank: A Recipe for Compressing LLMs Without Losing Quality</a></td><td>25</td><td>0</td><td>NLP</td><td>WMT 번역 모델 압축 대회 제출 보고로 양자화와 reranking 조합 결과임</td></tr>
<tr><td>694</td><td><a href='https://arxiv.org/abs/2611.19798'>Barron Approximation and locally optimal weight densities for shallow neural networks</a></td><td>25</td><td>0</td><td>LG</td><td>얕은 신경망의 Barron 근사와 mean field 이론으로 robotics와 무관함</td></tr>
<tr><td>695</td><td><a href='https://arxiv.org/abs/2611.19821'>GraphPass: A Study of Graph Neural Networks for Compiler Pass Selection</a></td><td>25</td><td>0</td><td>LG</td><td>컴파일러 pass 선택 GNN인데 라벨이 프로그램 family에 의해 정해져 단순 family 인식 과제로 판명됨. robotics와 무관함</td></tr>
<tr><td>696</td><td><a href='https://arxiv.org/abs/2611.20109'>MT-RGCN-DTI: A Multi-Task Relational Graph Convolutional Network for Drug-Target Interaction Prediction</a></td><td>25</td><td>0</td><td>LG</td><td>RGCN 기반 약물-표적 상호작용 예측으로 도메인 응용이고 robotics 무관함</td></tr>
<tr><td>697</td><td><a href='https://arxiv.org/abs/2611.20259'>Scaling large language model-assisted line-of-therapy adjudication with human-in-the-loop evidence-calibrated selection</a></td><td>25</td><td>0</td><td>NLP</td><td>종양 치료 라인 판정에 LLM과 clinician review를 결합하는 의료 응용임</td></tr>
<tr><td>698</td><td><a href='https://arxiv.org/abs/2611.20368'>HoloGene: Learning to Lift Sliced Spatial Transcriptomics to Holistic 3D Gene Fields</a></td><td>25</td><td>0</td><td>LG</td><td>공간 전사체 슬라이스를 3D 유전자 field로 올리는 INR이고 생물 도메인 응용임</td></tr>
<tr><td>699</td><td><a href='https://arxiv.org/abs/2611.20602'>Quantum Computing-Based Wasserstein Generative Adversarial Networks for Airfoil Parameterization</a></td><td>25</td><td>0</td><td>LG</td><td>양자 회로 WGAN으로 익형을 파라미터화하나 고전 WGAN과 성능이 비슷함</td></tr>
<tr><td>700</td><td><a href='https://arxiv.org/abs/2611.20660'>Enhancing Mixed Oil Length Prediction through Graph Representation Learning</a></td><td>25</td><td>0</td><td>LG</td><td>샘플 의존성을 그래프로 넣어 혼합유 길이 예측 RMSE를 10% 줄이는 파이프라인 응용임</td></tr>
<tr><td>701</td><td><a href='https://arxiv.org/abs/2611.21159'>When Feature Representation Changes Local Explanations: A Controlled Comparison of SHAP and LIME under Numerical Discretization</a></td><td>25</td><td>0</td><td>LG</td><td>이산화가 SHAP과 LIME 설명에 주는 변화를 UCI Adult 하나로 비교한 소규모 분석임</td></tr>
<tr><td>702</td><td><a href='https://arxiv.org/abs/2611.21295'>Deep Learning for Physicists: From Linear Regression to Reasoning Models</a></td><td>25</td><td>0</td><td>LG</td><td>딥러닝 강의 노트임. 연구 기여 없음</td></tr>
<tr><td>703</td><td><a href='https://arxiv.org/abs/2611.21399'>MegNIST, A Benchmark for Non-Invasive Inner Speech Decoding</a></td><td>25</td><td>0</td><td>LG</td><td>MEG inner speech 데이터셋임. 로봇과 무관함</td></tr>
<tr><td>704</td><td><a href='https://arxiv.org/abs/2611.21408'>Do Embedding-Map Distances Guide LLM Ideation? Four Tests Against What Came Next</a></td><td>25</td><td>0</td><td>LG</td><td>LLM ideation에서 embedding 거리 검증임. 로봇과 무관함</td></tr>
<tr><td>705</td><td><a href='https://arxiv.org/abs/2611.21423'>Emergent Steering Beyond Endpoint Alignment in Chemical Reaction Models</a></td><td>25</td><td>0</td><td>LG</td><td>화학 반응 모델 분석임. 로봇과 무관함</td></tr>
<tr><td>706</td><td><a href='https://arxiv.org/abs/2611.21432'>Just sort it! A note on the LP behind rank-one anti-loop edits</a></td><td>25</td><td>0</td><td>LG</td><td>reasoning 모델 loop 제거용 rank-one 편집의 LP 노트임. 무관함</td></tr>
<tr><td>707</td><td><a href='https://arxiv.org/abs/2611.21434'>Variational Monte Carlo for Quantum Excited States via Nested Low-Rank Approximation</a></td><td>25</td><td>0</td><td>LG</td><td>양자 여기 상태 VMC임. 로봇과 무관함</td></tr>
<tr><td>708</td><td><a href='https://arxiv.org/abs/2611.21439'>A Reinforcement Learning Method to Navigate SMEFT Operator Space</a></td><td>25</td><td>0</td><td>RL</td><td>입자물리 SMEFT 탐색용 RL임. 로봇과 무관함</td></tr>
<tr><td>709</td><td><a href='https://arxiv.org/abs/2611.18583'>&quot;I Am Not a Kiddo!&quot;: Quantifying Epistemic Infantilization in Large Language Models via Multi-Metric Bias Analysis</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM의 epistemic infantilization 편향 측정임. 로봇과 무관함</td></tr>
<tr><td>710</td><td><a href='https://arxiv.org/abs/2611.18589'>OmniTag-LLM: Multilingual Multitask Speech Tagging</a></td><td>25</td><td>0</td><td>NLP</td><td>다국어 다중 과제 speech tagging MLLM임. 로봇과 무관함</td></tr>
<tr><td>711</td><td><a href='https://arxiv.org/abs/2611.18591'>Where Language Models Fail Like Aphasic Patients and Where They Don&#x27;t</a></td><td>25</td><td>0</td><td>NLP</td><td>언어 모델과 실어증 환자의 실패 양상 비교임. 로봇과 무관함</td></tr>
<tr><td>712</td><td><a href='https://arxiv.org/abs/2611.18600'>ScopeBench: Evaluating Cultural Norm Scope Awareness in LLMs</a></td><td>25</td><td>0</td><td>NLP</td><td>문화 규범 범위 인식 benchmark임. 로봇과 무관함</td></tr>
<tr><td>713</td><td><a href='https://arxiv.org/abs/2611.18609'>Many Paths to the Same Mistake: Generating Diverse Reasoning Paths Behind the Same Student Mistake</a></td><td>25</td><td>0</td><td>NLP</td><td>같은 학생 오류에 대한 다양한 추론 경로 생성임. 무관함</td></tr>
<tr><td>714</td><td><a href='https://arxiv.org/abs/2611.18621'>Which Mathematical Context Supports Target-Aligned Conjecture Generation? A Paired Ablation Study</a></td><td>25</td><td>0</td><td>NLP</td><td>수학 conjecture 생성 맥락 ablation임. 무관함</td></tr>
<tr><td>715</td><td><a href='https://arxiv.org/abs/2611.18728'>Wrong with Confidence: Measuring Hallucination, Overconfidence and Identity-Conditioned Behaviour in Large Language Models</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM의 hallucination과 과신 측정임. 무관함</td></tr>
<tr><td>716</td><td><a href='https://arxiv.org/abs/2611.18987'>PREFACE: Separating Shared Corrections from Prefix Conditioning in PEFT</a></td><td>25</td><td>0</td><td>NLP</td><td>PEFT 조건화 효과 분리 분석임. 무관함</td></tr>
<tr><td>717</td><td><a href='https://arxiv.org/abs/2611.19176'>A Bag of Concepts? Testing Role-Filler Binding in the Verbalizable Workspace</a></td><td>25</td><td>0</td><td>NLP</td><td>verbalizable workspace의 role-filler binding 검증임. 무관함</td></tr>
<tr><td>718</td><td><a href='https://arxiv.org/abs/2611.19220'>Revisiting What Makes a Good Context Subset: A Sparse Latent Basis Perspective</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM context subset의 sparse latent basis 관점임. 무관함</td></tr>
<tr><td>719</td><td><a href='https://arxiv.org/abs/2611.19455'>Text Speeding Itself Up: Recency and Restraint in Session-Local Drafting</a></td><td>25</td><td>0</td><td>NLP</td><td>speculative decoding 세션 로컬 drafting임. 로봇과 무관함</td></tr>
<tr><td>720</td><td><a href='https://arxiv.org/abs/2611.19499'>Do Probing and Steering Favor the Same Directions Within and Across Language Models?</a></td><td>25</td><td>0</td><td>NLP</td><td>probing과 steering 방향 비교임. 로봇과 무관함</td></tr>
<tr><td>721</td><td><a href='https://arxiv.org/abs/2611.19507'>Evaluating and Improving Natural Language Autoencoders</a></td><td>25</td><td>0</td><td>NLP</td><td>natural language autoencoder 평가임. 무관함</td></tr>
<tr><td>722</td><td><a href='https://arxiv.org/abs/2611.19849'>NoLBERT-Calls: Reading Earnings Calls Without Hindsight</a></td><td>25</td><td>0</td><td>NLP</td><td>hindsight 없는 encoder를 earnings call 질의응답 매칭에 적응시킴. 금융 도메인 특화이고 로봇과 무관함</td></tr>
<tr><td>723</td><td><a href='https://arxiv.org/abs/2611.20012'>Offline-First Quantized AI: Design and Evaluation of an On-Device Maternal-Health Assistant for Low-Connectivity Environments</a></td><td>25</td><td>0</td><td>NLP</td><td>오프라인 안드로이드 산모 건강 도우미를 구현하고 소형 LLM 두 개를 비교함. 응용 사례 보고이며 새 방법은 없음</td></tr>
<tr><td>724</td><td><a href='https://arxiv.org/abs/2611.20305'>Hochschild Cocycle and Universality of Merge</a></td><td>25</td><td>0</td><td>NLP</td><td>Merge 연산의 Hochschild cocycle 보편성을 대수적으로 증명함. 언어학 이론 수학이며 실험과 로봇 관련성이 없음</td></tr>
<tr><td>725</td><td><a href='https://arxiv.org/abs/2611.20803'>What Do Digital Traces Predict? Task Effects, Student Differences, and Critical Online Reasoning</a></td><td>25</td><td>0</td><td>NLP</td><td>디지털 trace가 학생 성과를 예측하는지 보았으나 사전등록 12개 검정이 모두 유의하지 않았음. 교육 분석이며 로봇과 무관함</td></tr>
<tr><td>726</td><td><a href='https://arxiv.org/abs/2611.20823'>Medical question answering collapses in Hausa: a pre-registered pilot on three small open models</a></td><td>25</td><td>0</td><td>NLP</td><td>Hausa 의료 QA에서 소형 모델이 최빈 선택지 baseline도 못 넘음을 사전등록 pilot으로 보임. 부정 결과 보고이며 방법 기여가 없음</td></tr>
<tr><td>727</td><td><a href='https://arxiv.org/abs/2611.21208'>Validating LLM-Based Essay Scorers: A Comparative Analysis in Critical Online Reasoning in Medical Education</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM essay scorer 앙상블이 의학 교육 글쓰기 사람 평점을 근사하는지 봄. 교육 평가 응용임</td></tr>
<tr><td>728</td><td><a href='https://arxiv.org/abs/2611.21291'>Benchmarking Large Language Models for Linguistic Annotation</a></td><td>25</td><td>0</td><td>NLP</td><td>언어 주석용 LLM benchmark 도구 dhAIBench와 293회 실행 결과를 제시함. 도구·평가 보고임</td></tr>
<tr><td>729</td><td><a href='https://arxiv.org/abs/2611.21300'>LATTE-WordSeg-Lite: Multi-Granularity Thai Word Segmentation on a CPU, with a Reproducible Benchmark</a></td><td>25</td><td>0</td><td>NLP</td><td>태국어 단어 분절 모델을 1.17M CPU 모델로 distillation함. 저자원 언어 도구이며 로봇과 무관함</td></tr>
<tr><td>730</td><td><a href='https://arxiv.org/abs/2611.21393'>Train After You Measure: a Pre-Registered Learning Curve for Fine-Tuning Typed Decision Models on One User&#x27;s Labels</a></td><td>25</td><td>0</td><td>NLP</td><td>한 사용자의 이메일 label로 decision model을 fine-tuning해도 logistic regression 기준을 못 넘는다는 사전등록 연구임. 부정 결과이며 범위가 매우 좁음</td></tr>
<tr><td>731</td><td><a href='https://arxiv.org/abs/2611.21422'>Rubric-Based AES with LLM Ensembles: Scoring of Student Responses in Critical Online Reasoning Using Ensembles of LLMs</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM 앙상블로 독일어 학생 답안 rubric 채점이 사람 평가자 일치도를 유지하는지 봄. 교육 응용 평가임</td></tr>
<tr><td>732</td><td><a href='https://arxiv.org/abs/2611.21535'>Evaluating Cultural Reasoning and Robustness in LLMs for Spanish Political Discourse</a></td><td>25</td><td>0</td><td>NLP</td><td>스페인 정치 담론 감성 분석에서 LLM 강건성을 counterfactual로 평가함. 지역 도메인 dataset임</td></tr>
<tr><td>733</td><td><a href='https://arxiv.org/abs/2611.18958'>Dual-Stage Channel-Posterior Integration for MLM-Aided Token Communications</a></td><td>25</td><td>0</td><td>LG</td><td>MLM 기반 token 통신의 채널 posterior 통합 수신기를 제안함. 통신 분야 응용이며 로봇과 무관함</td></tr>
<tr><td>734</td><td><a href='https://arxiv.org/abs/2611.19099'>Instructor-designed AI improves learning in a randomized trial across 19 universities</a></td><td>25</td><td>0</td><td>AI</td><td>교수 설계 AI가 학습을 개선하는지 19개 대학 7,200명 RCT로 보임. 교육 정책 연구이며 로봇과 무관함</td></tr>
<tr><td>735</td><td><a href='https://arxiv.org/abs/2611.19116'>A Hybrid State Space-Attention Architecture for Forecasting the Trajectories of Battery Degradation</a></td><td>25</td><td>0</td><td>LG</td><td>배터리 열화 궤적을 예측하는 소형 state-space·attention 모델 DecayFormer를 제안함. 도메인 특화 예측임</td></tr>
<tr><td>736</td><td><a href='https://arxiv.org/abs/2611.19157'>FundingClaw: Automated Grant Proposal Writing Agents System</a></td><td>25</td><td>0</td><td>AI</td><td>grant 제안서 작성 multi-agent FundingClaw를 제안함. 10개 주제 rubric 평가이며 로봇과 무관함</td></tr>
<tr><td>737</td><td><a href='https://arxiv.org/abs/2611.19319'>Hardening Agentic Web Populations Through Multi-Criterion Competitive Co-Evolution: Lessons from Wargame Strategy Optimization</a></td><td>25</td><td>0</td><td>AI</td><td>jailbreak와 guardrail을 두 population의 경쟁 공진화로 다루자는 position paper임. 실험이 없음</td></tr>
<tr><td>738</td><td><a href='https://arxiv.org/abs/2611.19339'>From Mutation to Medication: Characterizing Failures of Clinical LLMs to Respect Genomic Resistance</a></td><td>25</td><td>0</td><td>NLP</td><td>임상 LLM이 유전체 내성 근거를 무시하고 항암제를 추천하는 실패율을 측정한 평가 연구임, 로보틱스와 무관함</td></tr>
<tr><td>739</td><td><a href='https://arxiv.org/abs/2611.19546'>Evidence-Conditioned Completion and Synthesis of Electronic Health Records</a></td><td>25</td><td>0</td><td>LG</td><td>EHR 완성과 합성을 evidence-conditioned latent diffusion bridge로 통합한 EHRDiB를 제안함, 의료 데이터이며 로보틱스와 무관함</td></tr>
<tr><td>740</td><td><a href='https://arxiv.org/abs/2611.19623'>Data-Driven Heuristic-Guided Business Process Redesign</a></td><td>25</td><td>0</td><td>LLM Agent</td><td>event log와 BPMN에 LLM으로 redesign heuristic을 적용하는 DH-BPR을 제안함, 비즈니스 프로세스 주제이며 로보틱스와 무관함</td></tr>
<tr><td>741</td><td><a href='https://arxiv.org/abs/2611.19982'>Autonomous Multi-modal Agents for ITOps Observability</a></td><td>25</td><td>0</td><td>LLM Agent</td><td>ITOps observability용 multi-agent 시스템을 구축하고 에이전트별 평가를 보고함, 시스템 보고서 성격이며 로보틱스와 무관함</td></tr>
<tr><td>742</td><td><a href='https://arxiv.org/abs/2611.20111'>When Valid Decisions Are Not Enough: Evaluating Structural Constraints in Knowledge-Guided Generative Systems</a></td><td>25</td><td>0</td><td>LG</td><td>음악 화성 생성에서 구조 제약이 맥락별로 일치도를 올리거나 내림을 보임, 로보틱스와 무관함</td></tr>
<tr><td>743</td><td><a href='https://arxiv.org/abs/2611.20915'>Multi-LLM Agentic AI at the Edge: Joint Agent Scheduling and Resource Allocation</a></td><td>25</td><td>0</td><td>LLM Agent</td><td>edge 환경에서 LLM worker agent 선택과 자원 할당을 최적화하는 구조를 제안함, 무선 자원 최적화 중심이며 로보틱스와 무관함</td></tr>
<tr><td>744</td><td><a href='https://arxiv.org/abs/2611.21218'>InclusionMed: Benchmarking AI for Inclusive Healthcare</a></td><td>25</td><td>0</td><td>NLP</td><td>의료 AI를 역할과 능력별로 평가하는 InclusionMed 지수를 제안함, 로보틱스와 무관함</td></tr>
<tr><td>745</td><td><a href='https://arxiv.org/abs/2611.18775'>Quantum-inspired orthogonal adapters for certifiably robust medical image classification</a></td><td>24</td><td>0</td><td>CV</td><td>의료 이미지 certified robustness 어댑터로 무관함</td></tr>
<tr><td>746</td><td><a href='https://arxiv.org/abs/2611.18791'>From Retouched Images to Paired Videos: A Synthetic Benchmark for Face Video Retouching</a></td><td>24</td><td>0</td><td>Video</td><td>얼굴 영상 retouching 합성 벤치마크로 무관함</td></tr>
<tr><td>747</td><td><a href='https://arxiv.org/abs/2611.18811'>CARET: Clinical Assertion-Aware Residual Calibration for Medical Image-Text Alignment</a></td><td>24</td><td>0</td><td>Multimodal</td><td>의료 영상-텍스트 정렬 보정으로 무관함</td></tr>
<tr><td>748</td><td><a href='https://arxiv.org/abs/2611.19089'>FDAM: A Frequency-Direction-Aware Multi-Task Framework for Pavement Crack Grid Localization</a></td><td>24</td><td>0</td><td>CV</td><td>도로 균열 위치 추정으로 도메인 특화임</td></tr>
<tr><td>749</td><td><a href='https://arxiv.org/abs/2611.19232'>Beyond Alignment: Supervising the Generator for EEG-to-Image Reconstruction</a></td><td>24</td><td>0</td><td>Generative</td><td>EEG-to-image 복원으로 무관함</td></tr>
<tr><td>750</td><td><a href='https://arxiv.org/abs/2611.19284'>LC-ISP Benchmark: Learning Advanced ISP with Live and Capture Streams</a></td><td>24</td><td>0</td><td>CV</td><td>RAW-to-sRGB ISP 벤치마크로 무관함</td></tr>
<tr><td>751</td><td><a href='https://arxiv.org/abs/2611.19316'>SAR-TopoGuard: Training-Free, Speckle-Aware Topological Verification for Structure-Preserving SAR-to-Optical Translation</a></td><td>24</td><td>0</td><td>CV</td><td>SAR-광학 변환 검증으로 무관함</td></tr>
<tr><td>752</td><td><a href='https://arxiv.org/abs/2611.19394'>Detecting Small Space Objects for Space Situational Awareness with Collaborative Edge AI</a></td><td>24</td><td>0</td><td>CV</td><td>우주 물체 검출 edge AI로 무관함</td></tr>
<tr><td>753</td><td><a href='https://arxiv.org/abs/2611.19981'>Morphology-Decoupled Segmentation for Multiple Tunnel Defects Under Complex Environments</a></td><td>24</td><td>0</td><td>CV</td><td>터널 결함 분할로 응용임</td></tr>
<tr><td>754</td><td><a href='https://arxiv.org/abs/2611.20192'>GlyphAtlas: Disentangling Stroke Detail from Layout for Scene Text Synthesis</a></td><td>24</td><td>0</td><td>Generative</td><td>장면 텍스트 합성으로 무관함</td></tr>
<tr><td>755</td><td><a href='https://arxiv.org/abs/2611.20372'>VisDrone-ReID: A Unified Multi-Category Object Re-Identification Benchmark</a></td><td>24</td><td>0</td><td>CV</td><td>VisDrone ReID 벤치마크로 무관함</td></tr>
<tr><td>756</td><td><a href='https://arxiv.org/abs/2611.20628'>PixelBench: Evaluating Language Models for Pixel-Art Creation</a></td><td>24</td><td>0</td><td>NLP</td><td>pixel-art 생성 LLM 벤치마크로 무관함</td></tr>
<tr><td>757</td><td><a href='https://arxiv.org/abs/2611.20629'>Event-Guided Stereo Video Super-Resolution</a></td><td>24</td><td>0</td><td>Video</td><td>event 기반 stereo 영상 SR로 무관함</td></tr>
<tr><td>758</td><td><a href='https://arxiv.org/abs/2611.21085'>State-Message Interaction Adapter for Cross-Domain Few-Shot Segmentation</a></td><td>24</td><td>0</td><td>CV</td><td>cross-domain few-shot 분할 adapter로 무관함</td></tr>
<tr><td>759</td><td><a href='https://arxiv.org/abs/2611.18658'>Rethinking the Verification of Machine Unlearning</a></td><td>24</td><td>0</td><td>LG</td><td>machine unlearning 검증을 출력이 아닌 내부 표현으로 옮기는 보안 연구임</td></tr>
<tr><td>760</td><td><a href='https://arxiv.org/abs/2611.18898'>Factorized Self-Supervised Speech Tokenization</a></td><td>24</td><td>0</td><td>LG</td><td>화자 정보를 분리한 음성 tokenizer로 음성 분야임</td></tr>
<tr><td>761</td><td><a href='https://arxiv.org/abs/2611.18994'>Large language models as oncology world models</a></td><td>24</td><td>0</td><td>LG</td><td>LLM의 종양학 world model 한계를 환자 시나리오로 분석한 연구임</td></tr>
<tr><td>762</td><td><a href='https://arxiv.org/abs/2611.19085'>DynaDFlash: Dynamic Feature Projection for Block Diffusion Speculators</a></td><td>24</td><td>0</td><td>LG</td><td>block diffusion speculator의 층별 gate로 수학 도메인 acceptance를 5% 올린 소규모 실험임</td></tr>
<tr><td>763</td><td><a href='https://arxiv.org/abs/2611.19135'>How Much Determinism Can Fine-Tuning Buy? Margin Regularisation Against Batch-Induced Token Flips</a></td><td>24</td><td>0</td><td>NLP</td><td>배치로 인한 token flip을 margin 정규화로 줄이는 LLM 결정성 연구이며 정확도를 잃음</td></tr>
<tr><td>764</td><td><a href='https://arxiv.org/abs/2611.19276'>ReCALM: A Residual-enhanced Crowdsourced Analytic Learning Mechanism for Distributed Continual Service Construction</a></td><td>24</td><td>0</td><td>LG</td><td>gradient 없는 analytic learning에 residual block을 넣은 crowdsourced continual learning임</td></tr>
<tr><td>765</td><td><a href='https://arxiv.org/abs/2611.19349'>SMELL: Sparsity-aware Memory Efficient Federated Fine-tuning for Long-context LLMs</a></td><td>24</td><td>0</td><td>LG</td><td>long-context LLM의 federated fine-tuning 메모리를 줄이는 시스템 기법임</td></tr>
<tr><td>766</td><td><a href='https://arxiv.org/abs/2611.19548'>Random Cut Forests, Games and Diffusion over Approximately Nested Anisotropic Local Geometry</a></td><td>24</td><td>0</td><td>LG</td><td>random cut forest 기하를 에너지와 게임으로 다루는 이론 연구임</td></tr>
<tr><td>767</td><td><a href='https://arxiv.org/abs/2611.20422'>A Structural Framework for Succession: Continuation, Recognition, and Realization</a></td><td>24</td><td>0</td><td>AI Theory</td><td>fine-tuning된 AI의 동일성 승계를 상태 그래프로 형식화함, 철학적 이론이며 로보틱스와 무관함</td></tr>
<tr><td>768</td><td><a href='https://arxiv.org/abs/2611.20603'>BiGSyn: A Bi-Level Heterogeneous Graph Contrastive Learning Framework for Interpretable Drug Synergy Prediction</a></td><td>24</td><td>0</td><td>LG</td><td>약물 시너지 예측용 이중 수준 이질 그래프 contrastive 학습 BiGSyn을 제안함, 바이오 응용이며 로보틱스와 무관함</td></tr>
<tr><td>769</td><td><a href='https://arxiv.org/abs/2611.20726'>PEETS: Preference-aware Embeddings with Explicit Tree Structure for Auxiliary Product Bundling</a></td><td>24</td><td>0</td><td>RecSys</td><td>보조 상품 번들링용 tree 구조 contrastive 임베딩 PEETS를 제안함, 추천 시스템이며 로보틱스와 무관함</td></tr>
<tr><td>770</td><td><a href='https://arxiv.org/abs/2611.20732'>Routing Beyond Task Categories: A Cost-Aware LAB-Bench Study</a></td><td>24</td><td>0</td><td>LLM</td><td>생물 질문의 비용 인지 모델 routing을 LAB-Bench로 시험했으나 기준 미달임, 로보틱스와 무관함</td></tr>
<tr><td>771</td><td><a href='https://arxiv.org/abs/2611.20794'>Regularizing Treatment Leakage for LLM-based Uplift Estimation</a></td><td>24</td><td>0</td><td>LG</td><td>LLM 기반 uplift 추정의 treatment 누설을 CLUB 페널티로 줄이는 LULR을 제안함, 개선이 통계적으로 유의하지 않고 로보틱스와 무관함</td></tr>
<tr><td>772</td><td><a href='https://arxiv.org/abs/2611.20700'>Design of the Secure Smart Scooter with Automatic Lane Detection</a></td><td>22</td><td>1</td><td>Robotics</td><td>스마트 스쿠터 차선 인식 프로토타입임. 연구 기여 약함</td></tr>
<tr><td>773</td><td><a href='https://arxiv.org/abs/2611.18689'>PACTHub: a large-scale structured experimental dataset for three-dimensional photoacoustic computed tomography</a></td><td>22</td><td>0</td><td>CV</td><td>광음향 CT 데이터셋으로 무관함</td></tr>
<tr><td>774</td><td><a href='https://arxiv.org/abs/2611.18699'>Where Does an On-Device Prescription Reader Lose Medications? A Frozen-Replay Study, from a 270M Language Model to a 2B Vision-Language Model</a></td><td>22</td><td>0</td><td>Multimodal</td><td>처방전 판독 on-device 분석으로 무관함</td></tr>
<tr><td>775</td><td><a href='https://arxiv.org/abs/2611.18706'>Small Data in Long-Term Environmental Vision: Annotation Noise, Gamification, and Label-Budget Scaling</a></td><td>22</td><td>0</td><td>CV</td><td>웹캠 환경 어노테이션 연구로 무관함</td></tr>
<tr><td>776</td><td><a href='https://arxiv.org/abs/2611.18707'>Different Timescales, Different Signals: Multimodal Landmark-Visibility Prediction in a Long-Term Webcam Network</a></td><td>22</td><td>0</td><td>Multimodal</td><td>후지산 가시성 예측으로 무관함</td></tr>
<tr><td>777</td><td><a href='https://arxiv.org/abs/2611.18710'>Whole-Slice Misses Escape Round-Trip Filtering and Volumetric Dice in a Source-Free Flow-Matching Segmenter</a></td><td>22</td><td>0</td><td>CV</td><td>의료 분할 품질 게이트 감사로 무관함</td></tr>
<tr><td>778</td><td><a href='https://arxiv.org/abs/2611.18741'>Target-Free Autocalibration of Stereo PIV Camera Systems via Persistent-State Motion Representations</a></td><td>22</td><td>0</td><td>CV</td><td>PIV 스테레오 자동 캘리브레이션으로 무관함</td></tr>
<tr><td>779</td><td><a href='https://arxiv.org/abs/2611.19495'>Vegetation Health Classification for Low-Data and Edge Hardware Deployment</a></td><td>22</td><td>0</td><td>CV</td><td>식생 건강 분류 edge 배포로 무관함</td></tr>
<tr><td>780</td><td><a href='https://arxiv.org/abs/2611.19578'>EndoComparer: Comparative Surgical Video Question Answering with Pseudo-Siamese Visual Adaptation and Perceive-then-Compare Reasoning</a></td><td>22</td><td>0</td><td>Video</td><td>수술 영상 비교 QA로 도메인 특화임</td></tr>
<tr><td>781</td><td><a href='https://arxiv.org/abs/2611.19737'>From Cloud to Edge: A Fully Local Pipeline for Pothole Risk Assessment and Driver Warning Generation</a></td><td>22</td><td>0</td><td>Multimodal</td><td>포트홀 위험 평가 로컬 파이프라인으로 응용임</td></tr>
<tr><td>782</td><td><a href='https://arxiv.org/abs/2611.19756'>Drift-Conditioned Structural Replay for Continual Cardiac Ultrasound Segmentation</a></td><td>22</td><td>0</td><td>CV</td><td>심장 초음파 연속학습 replay로 의료 특화임</td></tr>
<tr><td>783</td><td><a href='https://arxiv.org/abs/2611.19889'>Illusion of Explainability: A Sanity Check for Spectral Band Attribution in Satellite Time-Series Crop Classification</a></td><td>22</td><td>0</td><td>CV</td><td>위성 작물 분류 attribution 점검으로 무관함</td></tr>
<tr><td>784</td><td><a href='https://arxiv.org/abs/2611.19976'>CreaTrace: Video Creative Plagiarism Detection and Evidence Tracing</a></td><td>22</td><td>0</td><td>Video</td><td>영상 창작 표절 탐지로 무관함</td></tr>
<tr><td>785</td><td><a href='https://arxiv.org/abs/2611.20381'>Trait Collapse in Text-to-Image Generation: Evaluating and Mitigating Personality Inconsistency in Visual Storytelling</a></td><td>22</td><td>0</td><td>Generative</td><td>스토리 생성 성격 일관성으로 무관함</td></tr>
<tr><td>786</td><td><a href='https://arxiv.org/abs/2611.20502'>Pointillist Maize: 3D Reconstruction of Field-Grown Maize Using RGB UAV Imagery</a></td><td>22</td><td>0</td><td>3D Vision</td><td>옥수수 UAV 3D 복원으로 농업 특화임</td></tr>
<tr><td>787</td><td><a href='https://arxiv.org/abs/2611.20575'>PerturbJEPA: Joint-Embedding Predictive Learning of Cellular Perturbation Responses</a></td><td>22</td><td>0</td><td>Representation</td><td>세포 perturbation JEPA로 무관함</td></tr>
<tr><td>788</td><td><a href='https://arxiv.org/abs/2611.21114'>VAE Rhythm: Temporal Decoding Traces for AI-Generated Video Detection</a></td><td>22</td><td>0</td><td>Video</td><td>생성 영상 탐지 VAE 흔적으로 무관함</td></tr>
<tr><td>789</td><td><a href='https://arxiv.org/abs/2611.18599'>Mechanistic Interpretability of Mambas Selective Gate in Financial Markets: A Leakage-Controlled Study</a></td><td>22</td><td>0</td><td>LG</td><td>금융 시계열 Mamba의 SAE 해석 결과가 라벨 오염 artifact임을 보인 연구임</td></tr>
<tr><td>790</td><td><a href='https://arxiv.org/abs/2611.18635'>Multimodal Fusion with Pre-trained Models for Psychotherapy Outcome Prediction from Emotional Dynamics</a></td><td>22</td><td>0</td><td>LG</td><td>심리치료 결과를 사전학습 임베딩과 고전 모델로 예측한 소규모 임상 연구임</td></tr>
<tr><td>791</td><td><a href='https://arxiv.org/abs/2611.18662'>Stagewise Adaptive Boosting</a></td><td>22</td><td>0</td><td>LG</td><td>stagewise boosting에 구조적 sparsity를 넣는 통계 방법론임</td></tr>
<tr><td>792</td><td><a href='https://arxiv.org/abs/2611.18868'>SLICES: A Benchmark and Evaluation Framework for Self-Supervised Learning on Sparse ICU Time Series</a></td><td>22</td><td>0</td><td>LG</td><td>ICU 시계열 self-supervised learning 비교 benchmark임</td></tr>
<tr><td>793</td><td><a href='https://arxiv.org/abs/2611.19005'>AdaMenu: Query-Adaptive Menus for Decision Models over Large Label Spaces</a></td><td>22</td><td>0</td><td>NLP</td><td>큰 label 공간에서 후보 메뉴를 검색으로 줄이는 분류 방법임</td></tr>
<tr><td>794</td><td><a href='https://arxiv.org/abs/2611.19065'>A Fast Algorithm for the Familywise Loss</a></td><td>22</td><td>0</td><td>LG</td><td>familywise loss의 기울기를 O(K)에 계산하는 커널 개선임</td></tr>
<tr><td>795</td><td><a href='https://arxiv.org/abs/2611.19218'>Neural Dual Bounds: Valid-by-Construction JGLP Warm-Starts for MAP and Constrained MAP</a></td><td>22</td><td>0</td><td>LG</td><td>MAP 추론 상한을 신경망 한 번으로 내 warm-start하는 그래프 모델 방법임</td></tr>
<tr><td>796</td><td><a href='https://arxiv.org/abs/2611.19451'>Efficient and Accurate Causal Validation of Training Data Attribution</a></td><td>22</td><td>0</td><td>LG</td><td>training data attribution 인과 검증에 필요한 재학습 횟수를 줄이는 통계 보정임</td></tr>
<tr><td>797</td><td><a href='https://arxiv.org/abs/2611.19985'>When Zero Is Competitive: A Descriptive Pilot of Transformer and Gate-Graph Surrogates on Random-Angle Quantum Circuits</a></td><td>22</td><td>0</td><td>LG</td><td>양자 회로 기댓값 예측에서 zero predictor가 경쟁력 있다는 descriptive pilot이고 데이터도 비공개임</td></tr>
<tr><td>798</td><td><a href='https://arxiv.org/abs/2611.20261'>Estimating Outpatient Visit Prices from Hospital Price Transparency Data using Large Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>병원 가격 데이터에 RAG를 적용한 비용 추정 응용임</td></tr>
<tr><td>799</td><td><a href='https://arxiv.org/abs/2611.20390'>Architectural Principles for Parameter-Efficient Unitary Transformations in Coherent Optical Neural Networks</a></td><td>22</td><td>0</td><td>LG</td><td>광학 신경망의 butterfly 위상 구조 설계이고 robotics 무관함</td></tr>
<tr><td>800</td><td><a href='https://arxiv.org/abs/2611.20567'>Calibrated Functional Prediction from Overlapping Nonlinear Observations</a></td><td>22</td><td>0</td><td>LG</td><td>표 상태에서 비선형 audit functional을 예측하는 매우 특수한 통계 연구임</td></tr>
<tr><td>801</td><td><a href='https://arxiv.org/abs/2611.21079'>SemiNovo: Learning Beyond Search-Identified Spectra for De Novo Peptide Sequencing</a></td><td>22</td><td>0</td><td>LG</td><td>질량 분석 스펙트럼의 de novo peptide sequencing에 semi-supervised 학습을 적용한 생물 응용임</td></tr>
<tr><td>802</td><td><a href='https://arxiv.org/abs/2611.21554'>Reading or Remembering? Measuring Temporal Contamination in Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM의 시간적 contamination 측정임. 로봇과 무관함</td></tr>
<tr><td>803</td><td><a href='https://arxiv.org/abs/2611.21571'>DynSurvX: Time-Resolved Explanations for Dynamic Survival Predictions</a></td><td>22</td><td>0</td><td>LG</td><td>생존 예측 설명 기법임. 로봇과 무관함</td></tr>
<tr><td>804</td><td><a href='https://arxiv.org/abs/2611.18586'>Human vs Machine Translation Detection: A Cross-Model, Cross-Domain, and Low-Resource Analysis</a></td><td>22</td><td>0</td><td>NLP</td><td>인간 번역과 기계 번역 탐지 분석임. 로봇과 무관함</td></tr>
<tr><td>805</td><td><a href='https://arxiv.org/abs/2611.18595'>Profiling Hallucinations in Frontier LLMs for Entity Linking to Medical Ontologies</a></td><td>22</td><td>0</td><td>NLP</td><td>의료 온톨로지 entity linking의 hallucination 분석임. 무관함</td></tr>
<tr><td>806</td><td><a href='https://arxiv.org/abs/2611.18602'>Internal Verdicts Track Evidence: A Template-Controlled Neutrosophic Reading of Epistemic States in Large Language Models via the Jacobian Lens</a></td><td>22</td><td>0</td><td>NLP</td><td>neutrosophic logic으로 LLM 인식 상태를 해석함. 무관함</td></tr>
<tr><td>807</td><td><a href='https://arxiv.org/abs/2611.18610'>NYUAD at ImageEval Shared Tasks: A Multimodal LLM for Audio-Visual Question Answering and Hallucination Detection in English and Modern Standard Arabic</a></td><td>22</td><td>0</td><td>Multimodal</td><td>오디오-비주얼 QA shared task 참가 보고임. 로봇과 거리 있음</td></tr>
<tr><td>808</td><td><a href='https://arxiv.org/abs/2611.18613'>Bridging Semantics and Utilities: A Controllable and Scalable Market Simulation</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM 기반 시장 시뮬레이션임. 무관함</td></tr>
<tr><td>809</td><td><a href='https://arxiv.org/abs/2611.18616'>The Judge Is Not Impartial: Self-Preference in Medical LLM Evaluation</a></td><td>22</td><td>0</td><td>NLP</td><td>의료 LLM 평가에서 judge self-preference 분석임. 무관함</td></tr>
<tr><td>810</td><td><a href='https://arxiv.org/abs/2611.18620'>CondRelBench: A Mixed-Domain Benchmark for Condition-Scoped Relation Understanding</a></td><td>22</td><td>0</td><td>NLP</td><td>조건 범위 관계 이해 benchmark임. 무관함</td></tr>
<tr><td>811</td><td><a href='https://arxiv.org/abs/2611.19136'>Low-Latency LLM-Based Streaming Multi-Talker ASR with Verifiable Rewards</a></td><td>22</td><td>0</td><td>NLP</td><td>스트리밍 multi-talker ASR임. 무관함</td></tr>
<tr><td>812</td><td><a href='https://arxiv.org/abs/2611.19286'>On Representational and Functional Alignment of Training Data Attribution Methods for Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>training data attribution 정렬 분석임. 무관함</td></tr>
<tr><td>813</td><td><a href='https://arxiv.org/abs/2611.20044'>A Dataset for Misogyny Detection in Polish Social Media: Transferability of Hateful Speech Detection from General to Specific Types of Hate</a></td><td>22</td><td>0</td><td>NLP</td><td>폴란드어 misogyny 탐지 dataset과 일반-특수 hate 전이를 평가함. 도메인 dataset 위주이며 로봇과 무관함</td></tr>
<tr><td>814</td><td><a href='https://arxiv.org/abs/2611.20126'>A Corpus-Driven SentencePiece Unigram Tokenizer for Sindhi: Design and Benchmark Against Fourteen Existing Tokenizers</a></td><td>22</td><td>0</td><td>NLP</td><td>Sindhi용 SentencePiece tokenizer를 학습하고 14개와 비교함. intrinsic 지표만 보고 margin이 작음</td></tr>
<tr><td>815</td><td><a href='https://arxiv.org/abs/2611.20868'>It Depends on the Task: Rethinking Rhetorical Segmentation of Dutch Judicial Decisions</a></td><td>22</td><td>0</td><td>NLP</td><td>네덜란드 판결문 문장 단위 rhetorical role dataset을 구축하고 분류 전략을 비교함. 법률 도메인 dataset이며 로봇과 무관함</td></tr>
<tr><td>816</td><td><a href='https://arxiv.org/abs/2611.21303'>Syllable- and Word-Level Evaluation of Tibetan OCR</a></td><td>22</td><td>0</td><td>CV</td><td>티베트어 OCR을 음절·단어 단위 오류율로 평가함. 평가 지표 연구이며 로봇과 무관함</td></tr>
<tr><td>817</td><td><a href='https://arxiv.org/abs/2611.21362'>What You Post Is What You Symptom: Estimating Psychometric Networks from Social Media Discourse</a></td><td>22</td><td>0</td><td>NLP</td><td>소셜미디어 글에서 증상 네트워크를 추정하는 심리측정 연구임. 로봇과 무관함</td></tr>
<tr><td>818</td><td><a href='https://arxiv.org/abs/2611.21586'>Beyond Job Titles: Interpreting Early-Career Job Advertisements with Sparse Autoencoders and Semantic Clustering</a></td><td>22</td><td>0</td><td>NLP</td><td>SAE와 클러스터링으로 신입 채용 공고를 해석함. 로봇과 무관한 텍스트 분석 응용임</td></tr>
<tr><td>819</td><td><a href='https://arxiv.org/abs/2611.18714'>How to make a moral agent: sentimentalism and rationalism as lenses on AI</a></td><td>22</td><td>0</td><td>AI</td><td>AI의 도덕적 행위자 가능성을 철학적으로 논의하는 연구 프로그램 제안임. 실험이 없고 로봇과 무관함</td></tr>
<tr><td>820</td><td><a href='https://arxiv.org/abs/2611.18793'>Multimodal Fusion: A Review of Breast Cancer Advanced and Traditional Modalities</a></td><td>22</td><td>0</td><td>AI</td><td>유방암 다중 영상 융합 review임. 로봇과 무관한 의료 survey임</td></tr>
<tr><td>821</td><td><a href='https://arxiv.org/abs/2611.18930'>Between Rigor and Reality: How AI Safety Benchmark Developers Understand Benchmark Use and Maintenance</a></td><td>22</td><td>0</td><td>AI</td><td>AI 안전 benchmark 개발자 5명 인터뷰 연구임. 질적 연구이며 로봇과 무관함</td></tr>
<tr><td>822</td><td><a href='https://arxiv.org/abs/2611.19082'>CONTEXT-PCa: Evaluating the role of clinical context in MRI-based AI for detecting clinically significant prostate cancer (study protocol)</a></td><td>22</td><td>0</td><td>CV</td><td>전립선 MRI AI에 임상 변수를 더하는 연구의 사전 protocol임. 결과가 없고 로봇과 무관함</td></tr>
<tr><td>823</td><td><a href='https://arxiv.org/abs/2611.19348'>Attention U-Net Cellular Automata for Multi-Class Land Use and Land Cover Change Simulation in Lucknow, India: Evaluation Against Null and Classical Baselines</a></td><td>22</td><td>0</td><td>CV</td><td>Lucknow 토지이용 변화 cellular automata에 Attention U-Net을 적용했으나 null 모델을 못 넘고 attention 이득도 없음, 로보틱스와 무관함</td></tr>
<tr><td>824</td><td><a href='https://arxiv.org/abs/2611.19872'>Who Writes the Codebook? An Eight-Step Framework for Auditing LLM-Generated Category Systems</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM이 만든 codebook의 변동을 인터뷰 668건으로 감사하는 8단계 틀을 제안함, 질적 연구 방법론이며 로보틱스와 무관함</td></tr>
<tr><td>825</td><td><a href='https://arxiv.org/abs/2611.20935'>Razavi-Bench: Tracking AI Progress in Analog Circuit Reasoning</a></td><td>22</td><td>0</td><td>Multimodal</td><td>아날로그 회로 해석 50문항 Razavi-Bench로 MLLM 진전을 추적함, 점수 포화 상태이며 로보틱스와 무관함</td></tr>
<tr><td>826</td><td><a href='https://arxiv.org/abs/2611.20988'>Hivemind: A Federated Protocol for AI-Mediated Tacit Knowledge Sharing in Organisations</a></td><td>22</td><td>0</td><td>LLM Agent</td><td>조직 내 AI agent가 암묵지를 교환하는 federated 프로토콜 Hivemind를 제안함, 개념 증명 수준이며 로보틱스와 무관함</td></tr>
<tr><td>827</td><td><a href='https://arxiv.org/abs/2611.21405'>Shaping AI&#x27;s Beliefs Before It Generates: Human Sense of Agency in Creative AI</a></td><td>22</td><td>0</td><td>HCI</td><td>생성 전에 AI의 믿음을 사용자가 수정하게 하는 PaCC 시스템을 소규모 사용자 연구로 보임, 창작 HCI이며 로보틱스와 무관함</td></tr>
<tr><td>828</td><td><a href='https://arxiv.org/abs/2611.18744'>Neural Latent Gaussian Process for 3D reconstruction of Mouse Brain Lipids</a></td><td>20</td><td>0</td><td>LG</td><td>마우스 뇌 지질 3D 복원으로 무관함</td></tr>
<tr><td>829</td><td><a href='https://arxiv.org/abs/2611.19193'>Ref-MIL: Plug-and-Play Posterior Refinement for Multiple Instance Learning in QSM-Based Brain Disease Classification</a></td><td>20</td><td>0</td><td>CV</td><td>QSM 뇌질환 MIL로 무관함</td></tr>
<tr><td>830</td><td><a href='https://arxiv.org/abs/2611.19325'>Unlocking Fine-Grained Cell Representations via Soft-Interior Rim Dense-Grid Pooling in Pathology Foundation Models</a></td><td>20</td><td>0</td><td>CV</td><td>병리 foundation model 세포 표현으로 무관함</td></tr>
<tr><td>831</td><td><a href='https://arxiv.org/abs/2611.19630'>Where slide-level foundation-model classifiers fail on atypical breast lesions</a></td><td>20</td><td>0</td><td>CV</td><td>유방 병변 슬라이드 분류 실패 분석으로 무관함</td></tr>
<tr><td>832</td><td><a href='https://arxiv.org/abs/2611.19958'>Multimodal AI in Healthcare: Review of Vision-Language Foundation Models for Real-World Medical Applications</a></td><td>20</td><td>0</td><td>Multimodal</td><td>의료 VLM 리뷰로 무관함</td></tr>
<tr><td>833</td><td><a href='https://arxiv.org/abs/2611.20065'>MARLIN: Multiscale And Directional Sparse Representation Learning for Imbalanced SAR Ship Classification</a></td><td>20</td><td>0</td><td>CV</td><td>SAR 선박 분류로 무관함</td></tr>
<tr><td>834</td><td><a href='https://arxiv.org/abs/2611.20382'>Signs of Wear: Evaluating Intelligent Speed Assistance Under Synthetic Adverse Conditions</a></td><td>20</td><td>0</td><td>CV</td><td>속도 표지판 합성 악조건 평가로 무관함</td></tr>
<tr><td>835</td><td><a href='https://arxiv.org/abs/2611.20458'>VISTA: A Framework for Vision-Informed Semantic Traffic Awareness</a></td><td>20</td><td>0</td><td>CV</td><td>IoT 교통 인식 프레임워크로 무관함</td></tr>
<tr><td>836</td><td><a href='https://arxiv.org/abs/2611.20476'>Improving X-Ray Baggage Instance Segmentation with Shared Point-Based Mask Refinement</a></td><td>20</td><td>0</td><td>CV</td><td>X선 수하물 분할로 무관함</td></tr>
<tr><td>837</td><td><a href='https://arxiv.org/abs/2611.20787'>PhaseCLIP: Phase-Aware Frequency-Domain Adaptation of Vision-Language Models for Few-Shot Remote-Sensing Classification</a></td><td>20</td><td>0</td><td>CV</td><td>원격탐사 CLIP phase 적응으로 무관함</td></tr>
<tr><td>838</td><td><a href='https://arxiv.org/abs/2611.18792'>Hybrid Compression for Memory-Efficient Matrix-Vector Multiplication</a></td><td>20</td><td>0</td><td>LG</td><td>행렬 벡터 곱을 위한 문법과 엔트로피 혼합 무손실 압축 알고리즘임</td></tr>
<tr><td>839</td><td><a href='https://arxiv.org/abs/2611.18803'>Clustering-Based Artificial Tree Ensembles for Random Forest Approximation</a></td><td>20</td><td>0</td><td>LG</td><td>random forest 근사용 대표 트리 앙상블 군집 비교 연구임</td></tr>
<tr><td>840</td><td><a href='https://arxiv.org/abs/2611.18809'>LEAP-LLM: Preserving lead-time structure for question-conditioned ECG interpretation</a></td><td>20</td><td>0</td><td>LG</td><td>질문에 맞춰 ECG 특징을 뽑는 ECG-LLM 의료 응용임</td></tr>
<tr><td>841</td><td><a href='https://arxiv.org/abs/2611.18996'>Revealing the Biases of Large Language Models By Inferring Prior Distributions</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 편향을 베이지안 역문제로 prior 추정하는 연구임</td></tr>
<tr><td>842</td><td><a href='https://arxiv.org/abs/2611.19480'>Probing SAM Perturbations Through Statistical Replay</a></td><td>20</td><td>0</td><td>LG</td><td>SAM perturbation을 통계 재생으로 진단한 소규모 예비 실험임</td></tr>
<tr><td>843</td><td><a href='https://arxiv.org/abs/2611.20255'>Deep Sequence Model for Genome Wide Discovery of Coding and Regulatory Element Signatures</a></td><td>20</td><td>0</td><td>LG</td><td>경량 CNN과 gradient 분석으로 유전체 coding 구간을 분류하는 소규모 데모 수준 연구임</td></tr>
<tr><td>844</td><td><a href='https://arxiv.org/abs/2611.21149'>Cap-Aware Boosting for Green Day-Ahead Electricity Price Forecasting</a></td><td>20</td><td>0</td><td>LG</td><td>인도 전력 시장 가격 예측용 LightGBM 파이프라인으로 도메인 응용이고 robotics 무관함</td></tr>
<tr><td>845</td><td><a href='https://arxiv.org/abs/2611.21196'>Determining Concentration from Raman Spectroscopy with Manifold Learning and Y-shaped Conformal Autoencoders</a></td><td>20</td><td>0</td><td>LG</td><td>Raman 스펙트럼에서 농도를 예측하는 manifold learning 화학 공정 응용이며 기존 방법보다 약간 낮음</td></tr>
<tr><td>846</td><td><a href='https://arxiv.org/abs/2611.21602'>Quantifying the added value of human forecaster discussions for tropical cyclone intensity prediction</a></td><td>20</td><td>0</td><td>LG</td><td>허리케인 예보 토론의 부가 가치 분석임. 로봇과 무관함</td></tr>
<tr><td>847</td><td><a href='https://arxiv.org/abs/2611.18596'>Between the Lines: Multi-turn Contextual Investment Advice Detection</a></td><td>20</td><td>0</td><td>NLP</td><td>투자 조언 탐지임. 무관함</td></tr>
<tr><td>848</td><td><a href='https://arxiv.org/abs/2611.18603'>Retrieval-Augmented Generation for Clinical Decision Support in Gait Analysis: A Proof-of-Concept</a></td><td>20</td><td>0</td><td>NLP</td><td>보행 분석 임상 RAG proof-of-concept임. 로봇과 무관함</td></tr>
<tr><td>849</td><td><a href='https://arxiv.org/abs/2611.18606'>Syntactic Complexity Convergence in Dialogue: Analysis of the Phenomenon and Application to LLM Detection</a></td><td>20</td><td>0</td><td>NLP</td><td>대화 구문 복잡도 수렴 분석임. 무관함</td></tr>
<tr><td>850</td><td><a href='https://arxiv.org/abs/2611.18607'>Justification of Emotional Appeal in Computational Argumentation</a></td><td>20</td><td>0</td><td>NLP</td><td>논증에서 감정 호소의 정당화 연구임. 무관함</td></tr>
<tr><td>851</td><td><a href='https://arxiv.org/abs/2611.18623'>Evaluating the Robustness of Fact-Checking LLMs on Multilingual Evidence</a></td><td>20</td><td>0</td><td>NLP</td><td>다국어 증거 하 fact-checking LLM 강건성 평가임. 무관함</td></tr>
<tr><td>852</td><td><a href='https://arxiv.org/abs/2611.18653'>Winning the Leaderboard, Losing the Distribution: Diagnosing and Mitigating Acoustic Narrowing in Low-Resource ASR</a></td><td>20</td><td>0</td><td>NLP</td><td>저자원 ASR leaderboard 편향 분석임. 무관함</td></tr>
<tr><td>853</td><td><a href='https://arxiv.org/abs/2611.19029'>SurveyWeave: An Agentic Framework for Automated Survey Generation</a></td><td>20</td><td>0</td><td>NLP</td><td>자동 survey 생성 agent임. 무관함</td></tr>
<tr><td>854</td><td><a href='https://arxiv.org/abs/2611.19104'>EEGHyena2: Fixation-Inspired Joint Lexical-Grammatical Conditional Random Field for Interpretable EEG-to-Text Decoding</a></td><td>20</td><td>0</td><td>NLP</td><td>EEG-to-text 디코딩 CRF임. 무관함</td></tr>
<tr><td>855</td><td><a href='https://arxiv.org/abs/2611.19350'>When Does Label-Free Deconfounding of Document Embeddings Work?</a></td><td>20</td><td>0</td><td>NLP</td><td>문서 embedding label-free deconfounding임. 무관함</td></tr>
<tr><td>856</td><td><a href='https://arxiv.org/abs/2611.21160'>PlainPairs: A Corpus Pairing the Prescriber and Patient Texts of U.S. Prescription Medicine Labels</a></td><td>20</td><td>0</td><td>NLP</td><td>처방전 prescriber·환자 문서 쌍 코퍼스 PlainPairs를 공개함. 자원 논문이며 로봇과 무관함</td></tr>
<tr><td>857</td><td><a href='https://arxiv.org/abs/2611.19111'>Conditional Endorsement: Simulating How Adults with Different Skills Evaluate Canada&#x27;s National AI Strategy</a></td><td>20</td><td>0</td><td>AI</td><td>생성형 agent 3,200개로 캐나다 AI 전략 정책 반응을 시뮬레이션함. 정책 연구임</td></tr>
<tr><td>858</td><td><a href='https://arxiv.org/abs/2611.20894'>Which AI Use Cases Deserve a Pilot? A Risk and Value Framework for Funding, Scoping, and Scaling AI</a></td><td>20</td><td>0</td><td>AI Governance</td><td>AI use case의 위험과 가치를 보는 pilot 의사결정 틀을 합성 데이터로 시연함, 로보틱스와 무관함</td></tr>
<tr><td>859</td><td><a href='https://arxiv.org/abs/2611.20926'>Advancing Cognitive Pairwise Comparisons for Human-Centric Artificial Intelligence and Data Science: A Human-in-the-Loop Framework</a></td><td>20</td><td>0</td><td>HCI</td><td>pairwise comparison으로 사용자 선호를 끌어내는 human-in-the-loop 틀을 MovieLens에 적용함, 로보틱스와 무관함</td></tr>
<tr><td>860</td><td><a href='https://arxiv.org/abs/2611.18751'>From Hosted Service to Field-Owned Infrastructure: Open, Self-Hosted Real-Time Camera-Trap Alerting with Regional Open-Weight Models</a></td><td>18</td><td>0</td><td>CV</td><td>camera trap 알림 인프라로 무관함</td></tr>
<tr><td>861</td><td><a href='https://arxiv.org/abs/2611.18949'>Effects of Conventional, Adaptive, and AI-Powered Upscaling on the Legibility of License Plates</a></td><td>18</td><td>0</td><td>CV</td><td>번호판 upscaling 효과 비교로 무관함</td></tr>
<tr><td>862</td><td><a href='https://arxiv.org/abs/2611.19472'>InvarOrd: Self-Supervised Ordinal Knowledge Distillation with Rank-Invariant Alignment for Label-Efficient Cross-Species Hyperspectral Fish Freshness Assessment</a></td><td>18</td><td>0</td><td>CV</td><td>물고기 신선도 hyperspectral로 무관함</td></tr>
<tr><td>863</td><td><a href='https://arxiv.org/abs/2611.19511'>DBHiCo: Dual-Branch Hierarchical Contrastive Learning for MRI Image Classification</a></td><td>18</td><td>0</td><td>CV</td><td>MRI 분류 대조학습으로 무관함</td></tr>
<tr><td>864</td><td><a href='https://arxiv.org/abs/2611.19757'>Spatiotemporal Reconstruction of Auroral Precipitations with Neural Fields</a></td><td>18</td><td>0</td><td>3D Vision</td><td>오로라 neural field 복원으로 무관함</td></tr>
<tr><td>865</td><td><a href='https://arxiv.org/abs/2611.19905'>HEmIF-Bench: Benchmarking H&amp;E-to-mIF Models BeyondVirtual-StainFidelity</a></td><td>18</td><td>0</td><td>CV</td><td>H&amp;E-mIF 벤치마크로 무관함</td></tr>
<tr><td>866</td><td><a href='https://arxiv.org/abs/2611.20645'>Defect-Aware Masked Autoencoders for Unsupervised Clustering of Steel Surface Defects</a></td><td>18</td><td>0</td><td>CV</td><td>강판 결함 군집화로 무관함</td></tr>
<tr><td>867</td><td><a href='https://arxiv.org/abs/2611.20769'>Deep Learning for Satellite-Based Mountain Hazard Screening: A Retrospective Failure Analysis on the 2021 Chamoli Rock-Ice Avalanche</a></td><td>18</td><td>0</td><td>CV</td><td>산악 위험 위성 분석으로 무관함</td></tr>
<tr><td>868</td><td><a href='https://arxiv.org/abs/2611.21102'>Beyond Family Labels: A Taxonomic Ornstein-Uhlenbeck Prior for Avian 3D Shape Recovery</a></td><td>18</td><td>0</td><td>3D Vision</td><td>조류 3D 형상 복원으로 무관함</td></tr>
<tr><td>869</td><td><a href='https://arxiv.org/abs/2611.18785'>Setting Optimal Reserve Prices using Fine-Tuned Language Models</a></td><td>18</td><td>0</td><td>LG</td><td>경매 reserve price를 fine-tuned 언어 모델로 정하는 계량경제 응용임</td></tr>
<tr><td>870</td><td><a href='https://arxiv.org/abs/2611.18914'>How Much Do Foundation Models Add to Gradient Boosting on Financial Event Sequences?</a></td><td>18</td><td>0</td><td>LG</td><td>금융 이벤트 시퀀스에서 foundation model이 boosting 대비 더하는 이득을 측정한 연구임</td></tr>
<tr><td>871</td><td><a href='https://arxiv.org/abs/2611.19379'>$β$-number and Its Applications to Data Science</a></td><td>18</td><td>0</td><td>LG</td><td>PCA를 일반화하는 beta-number 지표를 제안한 이론 중심 데이터 과학 연구임</td></tr>
<tr><td>872</td><td><a href='https://arxiv.org/abs/2611.19419'>Do Pretraining Optimizer Gains Transfer to KL Distillation?</a></td><td>18</td><td>0</td><td>LG</td><td>pretraining optimizer 이득이 KL distillation에 이어지는지 본 비교 실험임</td></tr>
<tr><td>873</td><td><a href='https://arxiv.org/abs/2611.19597'>Synthetic Neurosymbolic Task Generation with Controlled Constraint Complexity</a></td><td>18</td><td>0</td><td>LG</td><td>제약 복잡도를 조절하는 neurosymbolic 합성 과제 생성기임</td></tr>
<tr><td>874</td><td><a href='https://arxiv.org/abs/2611.20467'>On the Applicability of $p$-adic Numbers in Computational Modules for Neural Networks</a></td><td>18</td><td>0</td><td>LG</td><td>p-adic 산술을 선형 회귀에 끼워 보니 복원이 실패했다는 부정적 결과 보고임</td></tr>
<tr><td>875</td><td><a href='https://arxiv.org/abs/2611.20752'>Who Benefits from Telemonitoring? Uplift Modelling of a Nationwide Home Blood Pressure Monitoring Programme</a></td><td>18</td><td>0</td><td>LG</td><td>싱가포르 원격 혈압 모니터링의 uplift 모델링을 다루는 의료 통계 연구임</td></tr>
<tr><td>876</td><td><a href='https://arxiv.org/abs/2611.18594'>Whose Side Are You On? Measuring Stance at Scale for Reddit Discourse Analysis During the Israel-Gaza War</a></td><td>18</td><td>0</td><td>NLP</td><td>Reddit 담론 stance 측정임. 무관함</td></tr>
<tr><td>877</td><td><a href='https://arxiv.org/abs/2611.18605'>Enhanced English-Sanskrit Translation using Multilingual NMT Approach</a></td><td>18</td><td>0</td><td>NLP</td><td>영어-산스크리트 번역임. 무관함</td></tr>
<tr><td>878</td><td><a href='https://arxiv.org/abs/2611.18608'>NYUAD at ArGuard Shared Tasks: Multimodal Embedding Models for Detecting Arabic Hateful Memes and Unsafe Prompts</a></td><td>18</td><td>0</td><td>NLP</td><td>아랍어 혐오 밈 shared task 참가 보고임. 무관함</td></tr>
<tr><td>879</td><td><a href='https://arxiv.org/abs/2611.18615'>Self-Evolving Dual-Role Deliberation for Medication Recommendation from Clinical Records</a></td><td>18</td><td>0</td><td>NLP</td><td>전자의무기록 기반 약물 추천임. 무관함</td></tr>
<tr><td>880</td><td><a href='https://arxiv.org/abs/2611.18619'>Assisting Patients with Reliable Information Gathering: A Guide to Building Efficient QA Systems for Medical Use</a></td><td>18</td><td>0</td><td>NLP</td><td>환자용 의료 QA 시스템 구축 가이드임. 무관함</td></tr>
<tr><td>881</td><td><a href='https://arxiv.org/abs/2611.18626'>Interpretability-Guided Auditing for Clinical Language Models for Discharge Prediction</a></td><td>18</td><td>0</td><td>NLP</td><td>임상 퇴원 예측 모델 감사임. 무관함</td></tr>
<tr><td>882</td><td><a href='https://arxiv.org/abs/2611.18628'>EmoTrace: Recursive Trace-Factorized Generation for Emotional Support Conversation</a></td><td>18</td><td>0</td><td>NLP</td><td>감정 지원 대화 생성임. 무관함</td></tr>
<tr><td>883</td><td><a href='https://arxiv.org/abs/2611.18631'>Beyond Binary Audits: Does Guideline Grounding Mitigate Decision-Space Framing in LLM Opioid Prescribing?</a></td><td>18</td><td>0</td><td>NLP</td><td>오피오이드 처방 LLM 편향 감사임. 무관함</td></tr>
<tr><td>884</td><td><a href='https://arxiv.org/abs/2611.19030'>Beyond Controllability: Speaker Diversity in Instruction-Guided Text-to-Speech</a></td><td>18</td><td>0</td><td>NLP</td><td>instruction TTS 화자 다양성 분석임. 무관함</td></tr>
<tr><td>885</td><td><a href='https://arxiv.org/abs/2611.19118'>Latency, Speech Recognition and Turn-Taking in Voice Agents for Spanish Phone Negotiation: An Externally Measured Comparison of Pipecat, LiveKit and GPT-Live</a></td><td>18</td><td>0</td><td>NLP</td><td>전화 협상 voice agent 지연 비교임. 무관함</td></tr>
<tr><td>886</td><td><a href='https://arxiv.org/abs/2611.19145'>A Systematic Study of Cross-Token Transfer for Data-Efficient Non-Verbal Text-to-Speech</a></td><td>18</td><td>0</td><td>NLP</td><td>비언어 TTS cross-token 전이 연구임. 무관함</td></tr>
<tr><td>887</td><td><a href='https://arxiv.org/abs/2611.19155'>Personalized Language Models for One-to-Many Private Communications</a></td><td>18</td><td>0</td><td>NLP</td><td>개인화 응답 예측 언어 모델임. 무관함</td></tr>
<tr><td>888</td><td><a href='https://arxiv.org/abs/2611.19375'>CausalGloss: Multi-Evidence Action Control for a Simultaneous Mandarin Speech-to-ASL Gloss Cascade</a></td><td>18</td><td>0</td><td>NLP</td><td>동시 음성-수화 gloss 번역임. 무관함</td></tr>
<tr><td>889</td><td><a href='https://arxiv.org/abs/2611.19393'>From Facts to Personas: Interpretable Role Unlearning in LLMs via Mixture-of-Experts</a></td><td>18</td><td>0</td><td>NLP</td><td>MoE 기반 role unlearning임. 무관함</td></tr>
<tr><td>890</td><td><a href='https://arxiv.org/abs/2611.19167'>Executable Archaeology: Reanimating the Logic Theorist</a></td><td>18</td><td>0</td><td>AI</td><td>Logic Theorist를 IPL로 재구현한 컴퓨팅 역사 연구임. 로봇과 무관함</td></tr>
<tr><td>891</td><td><a href='https://arxiv.org/abs/2611.21240'>How Developer Personality Shapes the Use of AI Coding Assistants</a></td><td>18</td><td>0</td><td>HCI</td><td>개발자 성격과 AI 코딩 보조 인식의 관계를 29명, 11명 설문으로 탐색함, 로보틱스와 무관함</td></tr>
<tr><td>892</td><td><a href='https://arxiv.org/abs/2611.21306'>Share your Screen and Talk to Gemini: How Young Learners Interact with Multimodal GenAI While Solving Scratch Tasks</a></td><td>18</td><td>0</td><td>HCI</td><td>초등 고학년 23명이 Scratch에서 Gemini 튜터와 나눈 대화를 분석함, 교육 연구이며 로보틱스와 무관함</td></tr>
<tr><td>893</td><td><a href='https://arxiv.org/abs/2611.19550'>Lesion-Aware Explainable AI for Diabetic Retinopathy Grading from Fundus Images</a></td><td>16</td><td>0</td><td>CV</td><td>당뇨망막병증 설명 가능 AI로 무관함</td></tr>
<tr><td>894</td><td><a href='https://arxiv.org/abs/2611.20089'>See the Lives of Stars in a Handful of Light</a></td><td>16</td><td>0</td><td>CV</td><td>은하 진화 영상 복원으로 무관함</td></tr>
<tr><td>895</td><td><a href='https://arxiv.org/abs/2611.20103'>Trading Parameters for Accuracy in MambaVision for Chest Radiograph Classification</a></td><td>16</td><td>0</td><td>CV</td><td>흉부 X선 MambaVision 파라미터 분석으로 무관함</td></tr>
<tr><td>896</td><td><a href='https://arxiv.org/abs/2611.20522'>AFRNet: Adaptive Frequency Redistribution Network for Image Deraining</a></td><td>16</td><td>0</td><td>CV</td><td>이미지 deraining으로 무관함</td></tr>
<tr><td>897</td><td><a href='https://arxiv.org/abs/2611.20745'>A Seismic Foundation Model for Dense Feature Extraction</a></td><td>16</td><td>0</td><td>CV</td><td>지진 foundation model로 무관함</td></tr>
<tr><td>898</td><td><a href='https://arxiv.org/abs/2611.20841'>Vision-Language Model-Based Phase-OTDR Event Classification</a></td><td>16</td><td>0</td><td>Multimodal</td><td>Phase-OTDR VLM 분류로 무관함</td></tr>
<tr><td>899</td><td><a href='https://arxiv.org/abs/2611.20854'>When Is the Expensive Method Worth It? A Content-Driven Analysis of Classical Bayer Demosaicing</a></td><td>16</td><td>0</td><td>CV</td><td>demosaicing 분석으로 무관함</td></tr>
<tr><td>900</td><td><a href='https://arxiv.org/abs/2611.21054'>Dataset Distillation for Handwritten Text Recognition: An Empirical Study</a></td><td>16</td><td>0</td><td>CV</td><td>필기 인식 dataset distillation으로 무관함</td></tr>
<tr><td>901</td><td><a href='https://arxiv.org/abs/2611.19297'>Where Mixture Recognition Fails: An Ingredient-Level Audit of Unseen Combinations in SmellNet</a></td><td>16</td><td>0</td><td>LG</td><td>전자코 혼합물 인식 benchmark의 평가 프로토콜 결함을 감사한 연구임</td></tr>
<tr><td>902</td><td><a href='https://arxiv.org/abs/2611.19609'>Before the Word: Name Information in Description-Derived States of Small Language Models, With and Without Naming Failure</a></td><td>16</td><td>0</td><td>NLP</td><td>작은 언어 모델의 이름 정보 상태를 tip-of-the-tongue 비유로 조사한 해석 연구임</td></tr>
<tr><td>903</td><td><a href='https://arxiv.org/abs/2611.18802'>Actuarial-Informed Neural Networks: Constrained Deep Learning for Sex-Specific Multi-Population Longevity Forecasting</a></td><td>15</td><td>0</td><td>LG</td><td>보험수리 제약을 넣은 LSTM 장수 예측 연구라 로봇과 무관함</td></tr>
<tr><td>904</td><td><a href='https://arxiv.org/abs/2611.19106'>Knowledge-Guided Local-to-Global Anomaly Learning for Longitudinal Medication Trajectories</a></td><td>15</td><td>0</td><td>LG</td><td>의료 투약 궤적 이상 탐지 응용 연구임</td></tr>
<tr><td>905</td><td><a href='https://arxiv.org/abs/2611.18593'>Theoretical Foundations of Computational Islamic Jurisprudence (Fiqh)</a></td><td>15</td><td>0</td><td>NLP</td><td>전산 이슬람 법학 이론 체계임. 무관함</td></tr>
<tr><td>906</td><td><a href='https://arxiv.org/abs/2611.18604'>One Question, Four Voices: How Advice for Alzheimer&#x27;s Caregiving Differs Between Caregivers, Clinicians, and Large Language Models</a></td><td>15</td><td>0</td><td>NLP</td><td>알츠하이머 간병 조언 비교 분석임. 무관함</td></tr>
<tr><td>907</td><td><a href='https://arxiv.org/abs/2611.18630'>All the Pieces Matter! A Six-stage Analysis of an Underground Fraud Ecosystem on Dread</a></td><td>15</td><td>0</td><td>NLP</td><td>사기 생태계 분석임. 무관함</td></tr>
<tr><td>908</td><td><a href='https://arxiv.org/abs/2611.18847'>Mapping the Afterlife of Future Work Statements in NLP Research</a></td><td>15</td><td>0</td><td>NLP</td><td>NLP 논문의 future work 추적임. 무관함</td></tr>
<tr><td>909</td><td><a href='https://arxiv.org/abs/2611.18981'>GPBam: A Retrieval-Aware German Public Law Exam Benchmark</a></td><td>15</td><td>0</td><td>NLP</td><td>독일 공법 시험 benchmark임. 무관함</td></tr>
<tr><td>910</td><td><a href='https://arxiv.org/abs/2611.19151'>MarineSparkLM-4B: A Lightweight Language Model for Marine and Offshore Engineering Built by Parameter-Efficient Adaptation</a></td><td>15</td><td>0</td><td>NLP</td><td>해양 공학 소형 언어 모델임. 무관함</td></tr>
<tr><td>911</td><td><a href='https://arxiv.org/abs/2611.19343'>OmitEHR: Scalable Omission Detection in LLM-Generated Clinical Summaries</a></td><td>15</td><td>0</td><td>NLP</td><td>임상 요약 누락 탐지임. 무관함</td></tr>
<tr><td>912</td><td><a href='https://arxiv.org/abs/2611.19360'>Leakage-aware calibrated decision-level fusion for mental-health text classification</a></td><td>15</td><td>0</td><td>NLP</td><td>정신건강 텍스트 분류 융합임. 무관함</td></tr>
<tr><td>913</td><td><a href='https://arxiv.org/abs/2611.19439'>Do Rule-Based Tools Help LLMs Translate Endangered Uralic Languages in the Prompt or over MCP?</a></td><td>15</td><td>0</td><td>NLP</td><td>소수 우랄어 번역에 규칙 기반 도구 활용임. 무관함</td></tr>
<tr><td>914</td><td><a href='https://arxiv.org/abs/2611.19512'>Sada-ASR: A Production Multidialectal Arabic Speech Recognition System</a></td><td>15</td><td>0</td><td>NLP</td><td>아랍어 방언 ASR 시스템임. 무관함</td></tr>
<tr><td>915</td><td><a href='https://arxiv.org/abs/2611.20826'>Conversing with a Conversational Agent: A Real Conversation, Not a Simulated One</a></td><td>15</td><td>0</td><td>AI Philosophy</td><td>LLM과의 대화가 시뮬레이션이 아닌 실제 대화라고 기호학적으로 논증함, 철학 에세이이며 로보틱스와 무관함</td></tr>
<tr><td>916</td><td><a href='https://arxiv.org/abs/2611.21476'>Generative AI and the Crisis of Higher Education Assessments: Examining &#x27;AI-Proofing&#x27; Strategies for College-Level Assessments</a></td><td>15</td><td>0</td><td>Education</td><td>AI-resistant 대학 평가 문항 75개에서 LLM 성능을 분석함, 교육 정책 주제이며 로보틱스와 무관함</td></tr>
<tr><td>917</td><td><a href='https://arxiv.org/abs/2611.19748'>SEAT: Sign-Type Evidence-Audited Transport for Multi-Label Tongue Diagnosis</a></td><td>14</td><td>0</td><td>CV</td><td>혀 진단 다중 라벨로 무관함</td></tr>
<tr><td>918</td><td><a href='https://arxiv.org/abs/2611.19956'>FinVision: Multimodal AI for Visualizing Financial Narratives</a></td><td>14</td><td>0</td><td>Multimodal</td><td>금융 서술 시각화로 무관함</td></tr>
<tr><td>919</td><td><a href='https://arxiv.org/abs/2611.19988'>KneeFS-Net: A Lightweight Deep Learning Model for Knee Osteoarthritis Severity Assessment with Cross-Domain External Validation</a></td><td>14</td><td>0</td><td>CV</td><td>무릎 골관절염 등급 분류로 무관함</td></tr>
<tr><td>920</td><td><a href='https://arxiv.org/abs/2611.20025'>acuSimNet: Multi-View Self-Occlusion-Awared Visibility Learning for Cranio-Cervical Acupuncture Points</a></td><td>14</td><td>0</td><td>CV</td><td>침술 혈위 위치 추정으로 무관함</td></tr>
<tr><td>921</td><td><a href='https://arxiv.org/abs/2611.20219'>Ocular Recognition: Interoperability, Multi-Resolution, and Spectrum Challenges</a></td><td>14</td><td>0</td><td>CV</td><td>홍채 인식 과제로 무관함</td></tr>
<tr><td>922</td><td><a href='https://arxiv.org/abs/2611.20269'>Self-supervised learning for zebrafish embryo phenotype evaluation: Systematic comparison of algorithms, label-efficient classification, and transfer learning</a></td><td>14</td><td>0</td><td>CV</td><td>제브라피시 SSL 비교로 무관함</td></tr>
<tr><td>923</td><td><a href='https://arxiv.org/abs/2611.20698'>STARS: Stage-Adaptive Responsibility Separation for Shadow Removal in Remote Sensing Images</a></td><td>14</td><td>0</td><td>CV</td><td>원격탐사 그림자 제거로 무관함</td></tr>
<tr><td>924</td><td><a href='https://arxiv.org/abs/2611.20840'>Interpretable deep concepts of organoid morphology</a></td><td>14</td><td>0</td><td>CV</td><td>organoid 형태 개념으로 무관함</td></tr>
<tr><td>925</td><td><a href='https://arxiv.org/abs/2611.20913'>Palmprint Decomposer: Interpretable and Editable Factorization via Synthetic Learning and Instance-Wise Refinement</a></td><td>14</td><td>0</td><td>CV</td><td>손바닥 무늬 분해로 무관함</td></tr>
<tr><td>926</td><td><a href='https://arxiv.org/abs/2611.21146'>Model-based neural network for global floodplains analysis</a></td><td>14</td><td>0</td><td>CV</td><td>홍수 원격탐사 SR로 무관함</td></tr>
<tr><td>927</td><td><a href='https://arxiv.org/abs/2611.19298'>NetBreaker: Benchmarking Network Dismantling across Objectives, Scales, and Toplogoies</a></td><td>14</td><td>0</td><td>LG</td><td>네트워크 dismantling 방법 30개를 비교한 benchmark임</td></tr>
<tr><td>928</td><td><a href='https://arxiv.org/abs/2611.19588'>PBit1: One Programmable P-Bit per Parameter - A Finite-Control Representation of Pretrained Networks</a></td><td>14</td><td>0</td><td>LG</td><td>pretrained 가중치를 p-bit로 표현하는 하드웨어 지향 구성임</td></tr>
<tr><td>929</td><td><a href='https://arxiv.org/abs/2611.20993'>Digits in Notation Are Not Numbers: A Scoring Pitfall in PDF-to-Markdown Conversion of Japanese Technical Documents (Preliminary Evaluation)</a></td><td>12</td><td>0</td><td>NLP</td><td>PDF 변환 숫자 채점 함정으로 무관함</td></tr>
<tr><td>930</td><td><a href='https://arxiv.org/abs/2611.21098'>MedicalDPO: Multi-Objective Direct Preference Optimization for CT to PET Translation</a></td><td>12</td><td>0</td><td>CV</td><td>CT-PET 변환 DPO로 무관함</td></tr>
<tr><td>931</td><td><a href='https://arxiv.org/abs/2611.18844'>Identification and external validation of the sets of 4-, 6-, 8-, 12-, and 24-hour CGM motifs</a></td><td>12</td><td>0</td><td>LG</td><td>혈당 CGM 모티프 집합의 외부 검증 연구임</td></tr>
<tr><td>932</td><td><a href='https://arxiv.org/abs/2611.18931'>OverclusterDRG: a Deterministic, LP-Free Heuristic for Robust $k$-Center</a></td><td>12</td><td>0</td><td>LG</td><td>robust k-center를 위한 결정적 휴리스틱 알고리즘임</td></tr>
<tr><td>933</td><td><a href='https://arxiv.org/abs/2611.19330'>Benchmarking the State of AI for Crop Yield Forecasting: A Global Assessment Across Modeling Paradigms</a></td><td>12</td><td>0</td><td>LG</td><td>작물 수확량 예측 방법론을 비교한 벤치마크임</td></tr>
<tr><td>934</td><td><a href='https://arxiv.org/abs/2611.19421'>Federated versus Centralized PV Capacity-Factor Forecasting: A Non-Inferiority Study Across Seven Stations in North Macedonia</a></td><td>12</td><td>0</td><td>LG</td><td>태양광 발전 예측에서 federated와 centralized 학습의 비열등성을 본 연구임</td></tr>
<tr><td>935</td><td><a href='https://arxiv.org/abs/2611.18661'>Non-Deterministic Finite Automata for Telugu Letters and Visualizations for Metrical Poetry</a></td><td>12</td><td>0</td><td>NLP</td><td>텔루구어 운율 자동기계임. 무관함</td></tr>
<tr><td>936</td><td><a href='https://arxiv.org/abs/2611.19094'>What Transfers Across Cuneiform? Script-Level Substrate and Language-Specific Regularities via Segmentation and Representation</a></td><td>12</td><td>0</td><td>NLP</td><td>쐐기문자 전이 분석임. 무관함</td></tr>
<tr><td>937</td><td><a href='https://arxiv.org/abs/2611.19356'>A Comparative Evaluation of BERT-Based and LLM-Based Models for Indic Sentence Similarity</a></td><td>12</td><td>0</td><td>NLP</td><td>인도어 문장 유사도 모델 비교임. 무관함</td></tr>
<tr><td>938</td><td><a href='https://arxiv.org/abs/2611.19418'>Real-World End-to-End Product Entity Resolution</a></td><td>12</td><td>0</td><td>NLP</td><td>상품 entity resolution임. 무관함</td></tr>
<tr><td>939</td><td><a href='https://arxiv.org/abs/2611.19509'>Formalizing Formal Semantics: The Formal Atlas</a></td><td>12</td><td>0</td><td>NLP</td><td>형식 의미론 증명 보조기 시스템임. 무관함</td></tr>
<tr><td>940</td><td><a href='https://arxiv.org/abs/2611.18713'>Technical Challenges for Ultra Fine Pitch Hybrid Bonding</a></td><td>10</td><td>0</td><td>LG</td><td>hybrid bonding 반도체 패키징으로 범위 밖임</td></tr>
<tr><td>941</td><td><a href='https://arxiv.org/abs/2611.19302'>Does Lifestyle Information Improve Hypertension Prediction? A Leakage-Controlled Evaluation on NHANES</a></td><td>10</td><td>0</td><td>LG</td><td>생활습관 정보가 고혈압 예측에 주는 이득을 NHANES로 평가한 연구임</td></tr>
<tr><td>942</td><td><a href='https://arxiv.org/abs/2611.18915'>The Human Side of ML Engineering: Analyzing the Collaboration and Communication Skills in ML Job Postings</a></td><td>8</td><td>0</td><td>LG</td><td>ML 채용 공고의 협업과 소통 요구를 분석한 연구로 기술 기여가 없음</td></tr>
</tbody></table>

</details>
