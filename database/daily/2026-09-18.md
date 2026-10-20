# 오늘의 arXiv Top 15 — 2026-09-18 (금)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**
> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)

**신규 논문 수: 전체 485편 → 중복 제거 후 485편 (이번 평가 대상 485편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 101 |
| cs.LG | 107 |
| cs.RO | 116 |
| cs.CL | 72 |
| cs.AI | 89 |

*1차 스크리닝: 전체 485편을 제목/초록 기반으로 채점(Claude (scheduled agent)) → 상위 15편은 arXiv 원문을 내려받아 정밀 리뷰(Claude (scheduled agent)) 후 최종 점수 산정.*

---

## Top 15

### 1. [82점] JEPA-Anything: Learning Predictive Models across Different Worlds

- **분야**: World Model · **robotics relevance**: 6/10
- **arXiv**: [2609.20800](https://arxiv.org/abs/2609.20800) ([PDF](https://arxiv.org/pdf/2609.20800))
- **저자**: Taoyong Cui, Zhongyao Wang, Xinyue Xu, Weiyang Liu, Zhaochen Yu, Yuying Zhang, Qiang Gao, Mengyue Yang 외 5명
- **카테고리**: Computation and Language (cs.CL) · 신규 목록 게재: cs.CL
- **Comments**: Code: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 JEPA가 여러 예측 대상을 하나의 embedding에 뭉뚱그려 학습해 쉬운 신호가 지배하는 문제를 지적함. latent target을 직교하는 여러 factor로 분해해 각각 독립 predictor로 학습하고 필요시 합쳐 완전한 state로 복원하는 orthogonal predictive factorization(OPF)을 제안함.

**Core innovation & methodology**

- 하나의 monolithic target 대신 학습 가능한 projector K개로 latent target을 직교 부분공간으로 분해하고 각 factor를 별도 predictor로 예측함.
- factor 간·factor 내 orthogonality loss, factor activity loss, encoder variance loss를 추가해 예측 붕괴와 중복 factor를 방지함.
- 예측된 factor들을 의사역행렬(pseudoinverse) 합성으로 다시 하나의 latent state로 복원해 decoding·planning·rollout에 재사용 가능하게 함.
- projector가 정확히 직교일 때 정보 보존과 합성 안정성을 보장한다는 명제(Proposition 1, 2)를 제시해 이론적 근거를 붙임.

**Novelty vs. prior works**

- I-JEPA/V-JEPA의 단일 predictor 구조에 직교 부분공간 분해를 도입한 것이 핵심 차이임. Barlow Twins류 redundancy-reduction 원리를 예측 대상(target subspace)에 직접 적용한 점이 새로움.
- 도메인 하나에 특화된 개선이 아니라 vision부터 분자동역학·날씨·임상 데이터까지 동일 알고리즘을 그대로 적용해 world modeling의 일반 원리로 제시한 점이 강점임. 다만 factorized multi-head prediction 자체는 disentanglement 계열 연구와 개념적으로 닿아 있어 아이디어의 뿌리는 새롭지 않음.
- 직교성 유지 시 정보 손실이 없다는 이론적 보장을 실제 학습된 모델에서 조건수·중복도로 검증한 부분(Table 5)이 주장을 뒷받침하는 근거로 확실함.

**Benchmark results**

- CITRIS Interventional Pong에서 단일 intervention 예측 오차를 standard JEPA 대비 34.8% 감소(0.009541→0.006218), 조합 intervention은 12.9%, 6-step rollout은 8.6% 감소함.
- 10-task matched dynamics benchmark(CausalWorld, DMC, PDEBench, WeatherBench2) 전부에서 reported metric이 개선됨. PDEBench Burgers는 6-step rollout MSE가 0.006369에서 0.004014로 줄어듦.
- APEBench Burgers held-out MSE 49.5%, 카오스 비선형계인 Kuramoto-Sivashinsky는 13.2% 개선됨. 50-step 장기 rollout에서도 ID/OOD 모두 개선이 유지되나 step이 늘수록 폭은 좁아짐(H20 -5.8%→H50 -3.2%).
- 분자동역학 4개 시스템(물·석영·파라세타몰·벤젠) 100-step rollout에서 비교 방법 중 최저 오차를 달성했고, 단일 cell perturbation(Norman) Pearson은 0.787에서 0.814로 개선됨.
- continuous-control planning(CEM)은 Walker2d·HalfCheetah에서 우위지만 Hopper는 오히려 standard JEPA가 나음. 저자도 환경 의존적이라고 명시함.

**Top-tier conference 적합성 — 82/100 · 추천 venue: NeurIPS**

새로운 representation·learning paradigm이면서 이론적 보장과 7개 도메인 실험이 결합돼 top-tier general track에 적합함. 약점은 로봇 실제 실험이 없고 control 실험이 시뮬레이션 locomotion에 그쳐 embodied 관점에서는 간접적이라는 점, Hopper에서 개선이 역전돼 일관성 주장이 완벽하지 않다는 점임.

**추천 이유 & 누리랩 연구와의 연결점**

- world model 우선 주제에 정확히 맞음. 단일 latent state에 여러 예측 대상을 욱여넣는 대신 factor로 나눠 학습한다는 원리는 object-centric 3DGS나 scene graph 표현에도 적용해볼 만함.
- factor 하나만 masking해 rollout 저하를 확인하는 실험 설계는 failure detection·counterfactual reasoning 실험에 그대로 차용 가능함.
- test-time에 factor 조합을 바꿔가며 예측하는 구조는 test-time optimization/inference-time planning 연구와 접점이 있음.

---

### 2. [78점] Feeling Terrain Before Crossing: World Models for Off-Road Navigation

- **분야**: World Model / Navigation · **robotics relevance**: 9/10
- **arXiv**: [2609.19863](https://arxiv.org/abs/2609.19863) ([PDF](https://arxiv.org/pdf/2609.19863))
- **저자**: E-In Son, Dong-Wook Kim, Ji-Hoon Hwang, Kangsun Lee, Jisung Bae, Jung-Taak Kim, Seung-Woo Seo
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 8 pages, 6 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 카메라 특징만 예측하던 navigation world model에 proprioception을 입력·출력으로 추가해 로봇이 느낄 slip·tilt와 실패위험을 함께 예측하는 Feel-WM을 제안함. 시뮬레이션 두 종과 실제 Husky 로봇, 시뮬레이션 ANYmal 로봇에서 visual-only 모델과 end-to-end 정책보다 험지 주행 성공률이 높았음.

**Core innovation & methodology**

- 카메라 특징만 예측하는 기존 navigation world model에 proprioception(관성·바퀴/관절 인코더) 조건을 추가해, 로봇이 볼 것뿐 아니라 느낄 것(roughness, slip, angular instability 등)을 함께 예측하는 physical future 개념을 제안함
- frozen DINOv2 패치 토큰에 FiLM으로 action과 proprioceptive state를 주입하고, 하나의 causal dynamics transformer에서 visual head·proprioceptive head·failure risk head 세 갈래로 예측함
- failure label과 roughness/slip/slope 등 물리적 타깃을 사람 라벨 없이 로봇 자체 주행 기록에서 자동 계산해 self-supervised로 학습함
- planner는 CEM으로 후보 행동을 굴려 예측된 failure risk와 목표 유사도를 별도 항으로 분리한 score로 궤적을 선택함

**Novelty vs. prior works**

- DINO-WM도 proprioceptive state를 latent에 붙이지만 tabletop·maze 태스크에서 에이전트 configuration으로만 쓰고, 지형이 로봇에 가하는 물리적 영향으로는 쓰지 않음. Feel-WM은 이를 terrain-robot interaction 예측으로 전환한 것이 본질적 차이임
- Roth et al.의 forward dynamics model은 기하학적 지형 표현에서 물리적 미래를 예측하지만 별도 sampling planner가 필요함. Feel-WM은 카메라 특징 기반으로 이미지 목표까지 함께 예측·평가하는 통합 world model이라는 점에서 다름
- failure risk를 위치 고정 속성이 아니라 로봇 상태·행동에 조건화된 값으로 정의한 점은 velocity-conditioned traversability(MAT)와 문제의식은 비슷하나, world model rollout 안에 통합해 학습한 점이 새로움

**Benchmark results**

- TartanDrive open-loop 계획에서 ADE 1.666(TD1)·3.439(TD2)로 NWM(5.356/5.886), RAE-NWM(5.526/5.877) 대비 크게 낮음(NoMaD는 TD2에서 더 낮으나 모방학습 목표와 정렬된 지표 특성 때문으로 저자가 설명함)
- Gazebo forest route 성공률 84.0%로 visual-only world model 54.0%, proprioception만 뺀 ablation 74.0% 대비 우위를 확인함
- Isaac Sim zero-shot(학습에 없던 환경)에서도 rough terrain 성공률 78.3% vs visual-only 67.7%로 일반화를 확인함
- failure risk 항을 빼는 score ablation에서 hill route 성공률이 84.0%에서 62.0%로 떨어져 risk term의 기여를 직접 검증함
- 다리로봇(ANYmal-C, Isaac Sim) rough terrain에서 성공률 44.0% vs 31.0%로 확장 확인했고, 실제 Husky 필드 실험(3개 코스, 코스당 10회)에서 24/30 성공으로 NoMaD의 14/30을 앞섬

**Top-tier conference 적합성 — 75/100 · 추천 venue: RSS**

proprioception 조건 world model이라는 명확한 formulation novelty와, 시뮬레이션 2종에 실로봇(Husky, ANYmal-C)까지 이어지는 폭넓은 검증이 강점임. ablation과 zero-shot transfer 결과가 논지를 뒷받침해 RSS·CoRL 수준의 완성도이나, 학습 데이터가 자체 주행 기록에 한정돼 미지 지형 일반화는 저자도 한계로 인정함.

**추천 이유 & 누리랩 연구와의 연결점**

- world model에 failure risk를 별도 head로 명시적으로 예측하게 한 설계는 누리랩의 failure detection·diagnosis 연구와 바로 연결됨. manipulation에서도 접촉 실패를 proprioception 기반으로 예측하는 방향으로 확장 가능함
- proprioception을 world model conditioning에 쓰는 방식은 tactile·force 신호를 결합한 manipulation world model에도 적용할 만한 템플릿임
- 여러 action 후보를 굴려 failure risk와 goal similarity를 분리 평가하는 planner 구조는 test-time optimization·inference-time planning 우선주제와 직접 겹침

---

### 3. [76점] Diagnose, Recover, Certify: Task Readiness under Hidden Dynamics Changes

- **분야**: RL / Failure Detection · **robotics relevance**: 8/10
- **arXiv**: [2609.20304](https://arxiv.org/abs/2609.20304) ([PDF](https://arxiv.org/pdf/2609.20304))
- **저자**: Nguyen Viet Tuan Kiet, Huynh Thi Thanh Binh
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 정책이 잘 안 쓰는 액추에이터가 열화돼도 현재 task에서는 안 드러나는 dormant dynamics drift 문제를 새로 정식화하고, matched-filter 기반 진단과 심각도 추정을 분리하는 EG-MPT를 제안함. MuJoCo·Box2D 등 다수 시뮬레이터에서 baseline 7개 대비 대체로 우수했으나 일부 환경에서는 최고 baseline과 근접한 수준에 그쳤고 전부 시뮬레이션 검증임.

**Core innovation & methodology**

- 배포된 정책이 특정 액추에이터를 거의 안 써서 열화가 관측에 안 남는 문제를 dormant dynamics drift로 정의하고, 이를 task-agnostic 진단 예산 하에서 fault localization과 post-change recovery를 통합한 결정 문제로 정식화함
- Evidence-Gated Matched-Pulse Transport(EG-MPT)는 matched-filter score로 fault 위치에 대한 범주형 posterior를 유지하고, 이 범주형 증거가 특정 gate 조건을 통과할 때만 연속 진폭 정보를 심각도 posterior로 전달함
- Stage 1(위치 진단)과 Stage 2(회복 데이터 수집)를 미래 task 공개 이전에 분리 수행하고, 이후 task별로 recover-or-abstain 배포 결정과 신뢰도 하한(Cantelli bound)을 함께 출력함
- 위치 추정이 임의의 잘못된 심각도 모델 오차에 불변함(Proposition 1)과 transport가 fixed-budget에서 control risk를 늘리지 않음(Proposition 2, 3)을 증명함

**Novelty vs. prior works**

- non-stationary RL·changepoint detection은 정책이 변화를 관측할 수 있다고 가정하지만, 이 논문은 배포된 정책이 특정 액추에이터를 거의 안 써서 변화가 통계적으로 완전히 안 보이는 상황을 문제로 정의함. 탐지의 정보이론적 한계를 formulation 차원에서 짚은 것임
- SEPT·OPAX·ASID-FIM·Task-OED 같은 active system identification은 이미 알려진 task(분포)를 향해 탐색하지만, 이 논문은 미래 task가 공개되지 않은 상태에서 task-agnostic하게 진단·회복 데이터를 모으고 이후 task별로 배포를 인증하는 순서를 새로 도입함
- 위치 추정과 심각도 추정을 분리하고 gate를 통과한 매칭 진폭만 심각도 추정에 반영해, 잘못된 severity 모델이 fault localization을 오염시키지 않음을 이론으로 보장한 점이 baseline 대비 본질적 차이임

**Benchmark results**

- 6개 MuJoCo dormant-actuator 환경 중 selective return 기준 4개(HalfCheetah 0.9874, Hopper 0.9941, Walker2d 0.9905 등)에서 가장 우수했고 baseline들의 0.96대 수준을 앞섬
- 심한 고장(g=0.20)에서 return 0.850으로 최고 경쟁 baseline인 OPAX(0.687) 대비 큰 격차를 보였고, calibrated fault(g=0.35)에서도 0.940으로 baseline보다 0.14~0.17점 높음
- recovery budget이 0이거나 task 공개 전 probe가 2회뿐인 극단적 저자원 조건에서도 EG-MPT가 선두를 유지함(Regret 0.699 vs baseline 0.755~0.771)
- evidence gate를 제거하면 raw regret은 소폭 낮아지지만(0.0802 vs 0.0834) severity 오차·certificate violation이 악화되고 abstention이 0.6373에서 0.1529로 급감해 과잉 배포 위험이 커짐(ablation으로 확인)
- MuJoCo·Box2D(cross-physics)·Pendulum/Acrobot·11개 compact-plant(aircraft, quadrotor 등)로 폭넓게 검증했으나 전부 시뮬레이션이며 실로봇 실험은 없음

**Top-tier conference 적합성 — 72/100 · 추천 venue: NeurIPS**

새로운 decision problem 정식화와 세 개 정리로 뒷받침되는 이론적 근거, baseline 7개와의 광범위한 비교가 강점이라 NeurIPS·ICML급 이론+실험 논문 포맷에 맞음. 다만 모든 검증이 MuJoCo·Box2D·synthetic plant 시뮬레이션에 그쳐 실로봇 검증이 없고 단일 액추에이터 고장만 다뤄 다중 고장으로의 확장성이 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- dormant fault 문제의식은 매니퓰레이터의 특정 관절·그리퍼를 정책이 거의 안 써서 열화가 숨어있다가 새 task에서 드러나는 상황과 직접 대응돼, manipulation의 failure diagnosis·recovery 연구에 바로 적용 가능함
- task-agnostic 진단 예산으로 먼저 위치를 찾고 이후 task별 인증을 분리하는 2단계 구조는 VLA 정책을 새 task에 배포하기 전 test-time으로 액추에이터·그리퍼 이상을 점검하는 절차로 재구성할 수 있음
- intervention 기반 matched-filter 진단은 world model rollout으로 candidate probe를 시뮬레이션해 고르는 방식과 결합하면 counterfactual reasoning 기반 실패 진단 파이프라인으로 확장 가능함

---

### 4. [75점] MAGMA-GEN: Validated Recovery Supervision from Ambiguous Failures via Counterfactual Re-Execution

- **분야**: Manipulation · **robotics relevance**: 10/10
- **arXiv**: [2609.20056](https://arxiv.org/abs/2609.20056) ([PDF](https://arxiv.org/pdf/2609.20056))
- **저자**: Loan Bernat, Matthieu Grard, Ariane Herbulot, Florent Lamiraux
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **원문 검토**: PDF 전문 · 1차 스크리닝 78점

> 💡 실패한 rollout이 high-level 판단 오류인지 실행 노이즈인지 구분되지 않는 문제를 다룸. privileged coach가 원인을 진단해 국소 교정·복구 행동을 제안하고 동일 상태에서 재실행으로 검증된 것만 supervision으로 남겨 학습함.

**Core innovation & methodology**

- 장기 horizon manipulation에서 실패는 판단 오류·실행 실패·부분관측 중 무엇 때문인지 알 수 없다는 점(ambiguous failure)을 문제로 정의함.
- privileged coach(LLM)가 실패한 subtrajectory에서 결정 오류 지점을 진단하고 교정(correction) 또는 복구(recovery) 행동 후보를 제안함.
- 후보를 동일 상태·동일 조건에서 시뮬레이터 재실행으로 검증해 downstream 성공률이 오른 것만 supervised label로 채택함. coach 진단 자체는 정답으로 쓰지 않음.
- validated branch만 모아 표준 supervised fine-tuning으로 학습해 sparse reward와 비국소 credit assignment 문제를 우회함.

**Novelty vs. prior works**

- CLEANER(즉시 교정)·AutoTraj(사후 trajectory repair) 대비 진단과 재실행 검증을 분리한 것이 핵심 차이임. ablation에서 검증 없이 coach 제안만 쓰면 recovery가 26.25%에서 5.00%로 떨어져 이 분리의 기여가 확인됨.
- 다만 방법 자체는 DAgger 계열 aggregation과 counterfactual rollout 아이디어의 조합이며 완전히 새로운 learning paradigm은 아님. 진단+검증이라는 구조는 여러 선행 failure-recovery 연구에서 이미 다뤄진 개념의 재조합에 가까움.

**Benchmark results**

- ManiSkill3 시뮬레이션 180개 seeded task에서 recovery rate 26.25%로 최강 baseline(20B Best-of-N) 16.66% 대비 9.59%p 개선함. 4B rollout policy만 써도 20B baseline을 앞섬.
- CSR(16.79%)·CGC(30.74%)도 모두 최고치지만 recovery rate 26.25% 자체는 18-step horizon 기준으로 보면 여전히 낮음.
- branching factor B=2에서 CSR 38.35%, recovery 40.0%까지 상승. 같은 조건 Expert Rollout Distillation은 26.99%/18.33%에 그침.
- 실로봇 Franka 30 trial에서 MAGMA-GEN 15/30, Expert Distillation 12/30, CLEANER 11/30. checkpoint 1개·30회 시도로 통계적 우위보다는 전이 가능성 확인 수준임.
- mechanism ablation: coaching과 re-execution 둘 다 없으면 recovery 1.66%, 검증 없이 coach만 쓰면 5.00%, 둘 다 있으면 26.25%로 두 요소가 상호보완적임을 확인함.

**Top-tier conference 적합성 — 74/100 · 추천 venue: CoRL**

failure recovery·counterfactual reasoning이라는 CoRL 선호 주제에 정확히 맞고 ablation이 방법 기여를 명확히 분리해 보여줌. 다만 절대 성공률이 낮고 실로봇 검증이 checkpoint 1개·30 trial로 작아 통계적 설득력이 약함.

**추천 이유 & 누리랩 연구와의 연결점**

- failure detection/recovery·counterfactual reasoning 우선 주제와 직접 연결됨. coach 진단 후 재실행 검증이라는 구조는 test-time optimization 실험에도 그대로 응용 가능함.
- 4B rollout policy와 20B coach를 나눠 쓴 compute 효율적 data engine 설계는 recovery dataset 구축 파이프라인 참고 자료로 쓸 수 있음.

---

### 5. [71점] LIFD: Anchored Diffusion for 3D-Aware Scene Memory in Robotic Manipulation

- **분야**: Manipulation · **robotics relevance**: 9/10
- **arXiv**: [2609.19796](https://arxiv.org/abs/2609.19796) ([PDF](https://arxiv.org/pdf/2609.19796))
- **저자**: Wenbo Li, Yiteng Chen, Wenhao Li, Qingyao Wu
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 8 pages, 4 figures. Submitted to ICRA 2027
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 부분관측 조작에서 카메라 밖으로 나간 물체 정보를 유지하기 위해 multi-view로 학습한 scene token을 단일 RGB와 순환 메모리로부터 생성해 복원함. rectified flow로 scene token을 생성하되 현재 시야 조건을 앵커로 점점 강하게 붙잡아 근거 없는 완성을 방지함.

**Core innovation & methodology**

- 여러 시점 RGB에서 self-distillation으로 scene-level token(GST)을 학습해 단일 view보다 풍부한 장면 표현을 teacher로 확보함.
- 배포 시에는 단일 RGB의 local token(LST)과 GRU 기반 순환 메모리만으로 GST를 rectified flow로 생성해 복원함.
- Anchor-Guided Cross-Attention으로 flow 진행 정도(u)에 따라 현재 시야 가중치를 점점 높여 생성된 표현이 과거 메모리에만 의존해 근거 없는 내용을 만들지 않도록 함.
- 생성된 GST를 slot attention으로 압축한 compact slot feature로 policy에 연결하고, perception 학습과 control 학습을 분리(Staged)함.

**Novelty vs. prior works**

- TraceVLA·MemoryVLA·SAM2Act+·BridgeVLA++ 등 기존 memory 기반 VLA는 과거 feature를 저장·검색하는 방식인데, 제안 방법인 LIFD는 과거 정보를 조건으로 현재 시야에서 안 보이는 부분을 생성적으로 완성한다는 점이 다름.
- 다만 구성 요소(VGGT 기반 geometry encoder, self-distillation, rectified flow completion, slot attention)는 모두 기존 기법의 재조합이며 완전히 새로운 objective나 formulation은 아님. novelty는 조합 방식과 anchor 가중치 스케줄에 있음.
- teacher-relative SCI(Scene Contradiction Index)는 생성 표현이 teacher와 얼마나 일치하는지만 재는 지표로, 실제 3D 기하 정확도를 독립적으로 검증하지 못한다는 한계를 저자도 인정함.

**Benchmark results**

- LIBERO 4개 suite 평균 91.6%(Staged)로 Joint 대비 3.1%p 개선. 다만 OpenVLA-OFT(97.1%), π0.5(96.9%), GR00T N1.6(97.0%) 등 최신 VLA보다는 낮음.
- MetaWorld 79.8%로 π0.5(81.6%)보다 1.8%p 낮아 시뮬레이션에서 SOTA는 아님.
- 실로봇 UR5e 4개 task family(가림 추출·순서 조립·은닉물체 탐색·재배치)에서 평균 56.0%, OpenVLA-7B 40.5% 대비 15.5%p 개선. 단 재배치(LR) task는 28%로 여전히 어려움.
- LIBERO-Spatial ablation에서 FiLM만 쓰고 생성(rectified flow)을 빼면 성공률이 93.6%에서 30.8%로 급락해 생성적 완성이 핵심 기여임을 보여줌. anchor 제거는 -23.7%p, memory 제거는 -18.8%p.
- 가림 실험(0-60% occluder)에서 40% 이상 가림에도 OpenVLA-7B 대비 8-10%p 우위이고, 실로봇 통제된 가림-해제 실험에서 memory 제거 시 복구가 가장 느림(12 step vs 4 step).

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

robot memory·3D-aware representation이라는 우선 주제에 부합하고 ablation·occlusion intervention이 촘촘해 기여를 잘 분리해 보여줌. 약점은 시뮬레이션 성능이 최신 VLA baseline보다 낮고, 실로봇이 단일 플랫폼·소수 task로 제한적이며, geometric accuracy를 독립적으로 검증하지 못했다는 점임.

**추천 이유 & 누리랩 연구와의 연결점**

- robot memory·object-centric 3D representation 우선 주제와 직접 연결됨. anchor 가중치를 flow 진행에 따라 조절하는 방식은 partial observability 관련 실험에 참고할 만함.
- 생성적 완성이 memory 저장·검색 방식보다 나은지 비교하는 ablation 설계는 occlusion 후 재관측 상황에서의 test-time behavior 분석 틀로 재사용 가능함.

---

### 6. [70점] TraceFlow: Guiding Frozen Flow-Matching Robot Policies with Success and Failure Traces

- **분야**: VLA / Test-time optimization · **robotics relevance**: 9/10
- **arXiv**: [2609.20646](https://arxiv.org/abs/2609.20646) ([PDF](https://arxiv.org/pdf/2609.20646))
- **저자**: Jiaxuan Zhang, Ruizhe Liu, Yu Zhang, Yanchao Yang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 64점

> 💡 flow-matching 기반 VLA 정책은 배포 후 weight가 고정돼 과거 rollout의 성공·실패가 지금 생성되는 동작에 반영되지 않는다는 문제에서 출발함. 성공·실패 rollout을 terminal outcome bit 하나로만 저장해 flow 생성을 bounded 교정하는 TraceFlow를 제안함. real robot 순서 packing task에서 성공률을 21/50에서 39/50으로, 재학습 없는 stacking 이후 47/50까지 높임.

**Core innovation & methodology**

- flow-matching action expert는 weight가 고정되면 이전 rollout의 결과가 지금 chunk 생성에 영향을 줄 수 없다는 점을 문제로 삼음. 기존 test-time 방법들은 성공 경험만 검색하거나 별도로 학습된 critic·verifier·dynamics model을 필요로 함
- TraceBank는 state-action trace를 시간 순으로 저장하고 각 trace에 성공·실패를 나타내는 terminal bit 하나만 붙임. Similarity Gate가 cosine similarity로 top-K개의 성공·실패 trace를 검색하고, progress alignment로 현재와 같은 task 진행 단계의 action window만 골라냄
- 검색된 action window들로 kernel density를 만들어 성공 쪽은 끌어당기고 실패 쪽은 밀어내는 guidance term을 flow의 velocity에 더함. base velocity 대비 norm을 cap해 base policy를 무너뜨리지 않게 제한하고, 후반 solver step에서는 guidance를 0으로 줄여 최종 동작은 원래 정책이 결정하게 함
- weight 업데이트 없이 배포 라운드마다 TraceBank에 새 rollout을 추가하는 stacking으로 성능을 누적함

**Novelty vs. prior works**

- 가장 가까운 prior work는 성공 경험만 검색해 prior를 주입하는 Retrieve-then-Steer·OptimusVLA, 학습된 critic으로 유도하는 Guided Action Flow·test-time Q-guidance, verifier로 chunk를 선택하는 TACO·RoboMonkey, 학습된 dynamics model로 유도하는 DynaGuide, 같은 episode 내 실패만 negative guidance로 쓰는 CCDP임
- TraceFlow는 terminal bit 하나만으로 과거 실패 rollout 전체를 negative evidence로 삼아 별도의 학습된 critic·verifier·dynamics model 없이 nonparametric guidance field를 구성한다는 점에서 본질적으로 다름. progress alignment로 겉모습은 비슷하지만 진행 단계가 다른 trace를 걸러내는 설계도 차별점임
- 저자 스스로 concurrent method들과 head-to-head 비교를 하지 않았다고 명시함. 비교 대상은 guidance 없는 동일 checkpoint뿐이라, 제안 방식이 다른 test-time steering 방법보다 우수한지는 이 논문만으로 판단하기 어려움

**Benchmark results**

- real robot 순서대로 담기(3개 과일 packing) task에서 base 21/50, TraceFlow 39/50, 재학습 없이 한 라운드 stacking 후 47/50. 순서가 틀린 episode는 20/50에서 0/50으로 사라짐
- RoboMemArena Sequence(PrediMem backbone)에서 78.92%에서 91.50% TSR로, Transferring은 54.41%에서 62.00%로 개선(stacking 2라운드 시점)
- 26개 task 전체 aggregate는 거의 변화 없고(34.92→34.99), memory 의존적인 Counting·Occlusion suite는 오히려 1.12·1.42포인트 하락함. 실패 원인이 upstream 정보 부족일 때는 효과가 없다고 저자가 명시함
- guidance를 cap 없이 적용하면 base policy 성능이 오히려 무너짐(56.75→24.25 TSR). bounded guidance라야 57.75로 개선되어, cap 설계가 핵심 안전장치임을 ablation으로 확인함
- 10라운드 stacking 실험에서 모든 admission 방식이 R10 이전에 성능이 정점을 찍고 이후 하락해 이득이 유한함을 확인함. LIBERO-Plus(Long) OOD 개선폭(+1.27포인트)은 p=0.0733으로 통계적으로 애매함

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

test-time optimization으로 실패 경험을 weight 업데이트 없이 활용한다는 문제 설정이 명확하고, real robot에서 순서 오류를 실제로 없애는 강한 증거를 보임. 다만 concurrent 방법들과 직접 비교가 없고 real-world 평가가 소수 task·소수 trial(세 번째 task는 10회)에 그쳐 일반화 근거는 약함.

**추천 이유 & 누리랩 연구와의 연결점**

- test-time optimization·failure detection/recovery 우선 주제에 정확히 들어맞음. 실패 rollout을 terminal bit 하나로만 표시해 repulsion 신호로 쓰는 설계는 실로봇 failure recovery 연구에서 실패 원인을 세분화하지 않고도 재발을 줄이는 저비용 장치로 바로 응용 가능함
- TraceBank는 사실상 robot memory 시스템이라, memory·장기 실행 계획 연구와 결합해 실패 궤적을 누적하는 test-time 교정 모듈로 확장해볼 만함. Counting·Occlusion에서 효과가 없다는 결과는 이 방법이 동작 수준 교정이지 관측 실패 자체는 못 고친다는 경계를 보여줌

---

### 7. [68점] ParticleSplat: Self-supervised Object-centric Latent Particle Splatting

- **분야**: 3D Vision / Manipulation · **robotics relevance**: 8/10
- **arXiv**: [2609.19463](https://arxiv.org/abs/2609.19463) ([PDF](https://arxiv.org/pdf/2609.19463))
- **저자**: Lyuxing He, Daniel Guo, Elizabeth Terveen, Deepak Pathak, David Held, Tal Daniel
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: Project page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 65점

> 💡 2D self-supervised particle 표현인 Deep Latent Particles를 3D Gaussian Splatting으로 확장해, label 없이 object mask와 편집 가능한 3D object-centric latent를 얻는 ParticleSplat을 제안함. RLBench와 MimicGen manipulation task에서 기존 object-centric 표현과 3D Gaussian Splatting 기반 표현 모두를 큰 폭으로 앞섬.

**Core innovation & methodology**

- Deep Latent Particles(DLP, position·scale·depth·transparency·appearance를 가진 2D particle 기반 self-supervised 표현)의 속성 구조가 3D Gaussian primitive와 유사하다는 관찰에서 출발해, particle을 2D image space에서 3D scene space로 확장함
- multi-view encoder가 posed RGB(-D) 관측과 카메라 pose(Plücker ray embedding)를 입력받아 view별 latent particle을 추론하고, cross-view attention으로 depth와 appearance를 정제함
- decoder는 각 particle을 canonical patch의 Gaussian 집합으로 만든 뒤 affine 변환과 depth 속성으로 world-space 3D Gaussian으로 들어올리고, 전체 장면을 이 Gaussian들의 합성으로 렌더링함
- context/target view 재구성 항과 scene-level KL 항으로 구성된 multi-view 목적함수(evidence lower bound, ELBO)로 학습하며, particle의 position·scale을 직접 바꾸면 대응하는 3D Gaussian도 함께 움직여 object 단위 3D 편집이 가능함

**Novelty vs. prior works**

- 가장 가까운 prior work는 2D particle 기반 DLP와 feedforward 3D Gaussian Splatting(3DGS) 계열(pixelSplat, MVSplat, LatentSplat)임. 이들은 object-centric bottleneck이 없거나 압축된 latent를 downstream policy에 쓰는 실험이 없음
- ManiGaussian, GNFactor는 3DGS·NeRF를 쓰지만 action-conditioned dense voxel/feature field로, object 단위로 분리되지 않고 policy 학습과 함께 최적화됨
- ParticleSplat은 DLP의 particle 구조를 3D Gaussian에 그대로 정렬시켜 self-supervised로 label 없이 3D object mask와 조작 가능한 latent를 동시에 얻는데, 두 기존 프레임워크(particle 기반 object-centric learning과 feedforward 3DGS)를 구조적 유사성으로 연결한 조합이라 구성요소 각각의 신규성은 높지 않음

**Benchmark results**

- RLBench novel view synthesis에서 PSNR·SSIM·LPIPS 모두 GNFactor, ManiGaussian, VAE-GS baseline을 앞섬(2-view 기준 PSNR 28.77 vs VAE-GS 25.93)
- RLBench 10개 manipulation task의 imitation learning(EC-Diffuser policy) 평균 성공률이 73.0%로, GNFactor 31.7%, ManiGaussian 45.2%, VAE-GS 42.0%, 2D DLP 46.6%를 모두 크게 앞섬
- object-centric 추론과 정확한 3D geometry를 동시에 요구하는 task(put in drawer, stack blocks, close jar)에서 격차가 가장 크게 벌어짐
- 추가 benchmark인 MimicGen에서도 56.1%로 multi-view DLP(34.1%)를 앞섬
- particle 구조 제거, Gaussian decoder를 2D pixel decoder로 교체, pose conditioning 제거, depth fusion 제거 ablation이 모두 성능을 크게 낮춰 각 구성요소의 기여를 확인했으나 구체 수치는 appendix에 있어 본문에서 확인 불가함.
- 카메라 pose는 학습과 추론 모두 ground-truth로 주어져야 함

**Top-tier conference 적합성 — 68/100 · 추천 venue: CVPR**

self-supervised object-centric 3DGS라는 새로운 조합으로 novel view synthesis와 robot manipulation policy 성능을 동시에 개선한 강한 실험적 증거를 보임. 다만 카메라 pose를 항상 알고 있다고 가정하고 배경이 단순한 장면에 한정되어 있어, unposed 환경으로의 일반화는 향후 과제로 남음.

**추천 이유 & 누리랩 연구와의 연결점**

- object-centric 3D representation·3DGS 우선 주제에 직접 부합함. particle 단위로 3D 위치를 바꿔 장면을 편집할 수 있다는 점은 counterfactual reasoning이나 world model에서 물체를 가상으로 재배치해 결과를 예측하는 실험에 바로 응용할 만함
- label 없이 나오는 object mask와 compact latent는 scene graph·semantic mapping 연구에서 초기 object proposal로 쓸 수 있음. 다만 카메라 pose 필요 가정은 real-world 배포 시 추가 pose 추정 모듈을 요구함

---

### 8. [68점] MoWAM: Explicit Future Motion Prediction for Efficient World Action Models

- **분야**: World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.20709](https://arxiv.org/abs/2609.20709) ([PDF](https://arxiv.org/pdf/2609.20709))
- **저자**: Jiayu Wang, Bin Zhu, Yue Yu, Jingjing Chen
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 World Action Model의 추론 시 미래 video 생성을 없애면서도 명시적 미래 정보를 남기기 위해, keypoint 기반 end-effector motion을 미래의 압축 표현으로 예측하는 MoWAM을 제안함. LIBERO-Plus OOD 평균 성능을 Fast-WAM 대비 11.0%p, real-world 평균 성공률을 35%p 올리면서 지연은 Joint-WAM·IDM-WAM의 3분의 1 수준으로 낮춤.

**Core innovation & methodology**

- 추론 시 미래 video rollout을 제거하면 효율적이지만, 미래 정보가 observation feature에 암묵적으로만 남아 OOD에서 성능이 떨어짐. 명시적 미래 표현을 유지하면서 video 생성 비용을 없애는 것이 목표임.
- 손끝 2개와 palm 1개 keypoint를 이미지에 투영해 gripper center·span·relative offset의 시간적 변화(m_dyn, 6차원)와 기하 구조(m_str, 4차원)로 미래를 압축함. action을 이미지에 직접 투영한 값과 달리 실제 실행 결과에 가까운 예측값임(Table V, ADE 92.75% 감소로 확인).
- Video Transformer가 학습 시에만 미래 video denoising을 학습해 dynamics를 익히고, Action-Motion Transformer가 action과 motion을 flow matching으로 함께 생성하는 Mixture-of-Transformer 구조를 씀. 추론 시 Video Transformer는 관측을 한 번 인코딩하는 데만 쓰이고 video는 생성하지 않음.
- (action, motion) 후보 여러 개를 샘플링하고 motion-aware verifier(pairwise ranking loss로 학습)로 최고 점수 후보를 골라 실행함. motion이 저렴해 candidate 수를 늘려도 latency·memory 증가가 Fast-WAM 수준에 그침.

**Novelty vs. prior works**

- 가장 가까운 선행연구는 암묵적 미래만 남기는 Fast-WAM과 명시적 video rollout을 유지하는 Joint-WAM·IDM-WAM임. 본 논문은 그 중간 지점, 즉 명시적이면서도 저비용인 미래 표현을 채움.
- 압축된 latent future를 쓰는 LaWAM과 비교하면 motion은 해석 가능한 keypoint 기반 표현이라는 점에서 다르지만, LIBERO-Plus에서 LaWAM 대비 3.0%p 우위로 차이는 크지 않아 개념적 도약이라 보기는 어려움.
- motion representation 자체는 기존 hand/gripper pose 표현을 WAM의 미래 proxy로 재활용한 것이라 새로운 발명은 아니지만, explicit-but-cheap이라는 설계 공간을 실증적으로 채웠다는 기여는 분명함.

**Benchmark results**

- LIBERO 평균 성공률 98.9%로 Fast-WAM(96.5%) 대비 +2.4%p, embodied pretraining 없이도 pretraining 있는 π0.5(96.9%)를 웃돔.
- LIBERO-Plus(7종 OOD) 평균 81.43%로 Fast-WAM(70.43%) 대비 +11.0%p. 단 Initial·Camera 축에서는 full visual rollout 방식인 IDM-WAM·Joint-WAM보다 5~8%p 낮아 모든 분포 이동에서 우위는 아님.
- Latency: MoWAM 293.5ms vs Joint-WAM 766.3ms, IDM-WAM 995.4ms. 성능은 비슷한 수준이면서 지연은 2.6~3.4배 낮음.
- 실로봇 3과제(Franka Research 3) 평균 성공률 80%로 Fast-WAM(45%) 대비 +35%p, pretrained Motus(71.67%) 대비도 우세하면서 latency는 1621.9ms에서 293.5ms로 크게 줄어듦. 단 real-world는 3개 과제·20 trial로 규모가 작음.
- Ablation: motion supervision(dynamics+structure loss) 제거 시 76.0%에서 65.71%로 하락, 학습 시 video denoising loss를 아예 없애면 76.0%에서 33.14%로 급락함. video 학습이 핵심 dynamics 신호를 제공함을 확인함.

**Top-tier conference 적합성 — 60/100 · 추천 venue: CoRL**

OOD 강건성과 real-world 성능을 유지하면서 추론 비용을 크게 낮췄다는 실증이 탄탄함. 다만 motion representation 자체의 개념적 새로움은 제한적이고 LaWAM 등 compact-future 계열과 성능 차이가 크지 않아, top venue에서는 novelty보다 효율-강건성 trade-off의 실용적 기여로 평가받을 가능성이 큼.

**추천 이유 & 누리랩 연구와의 연결점**

- Test-time optimization/inference-time scaling 주제에 바로 적용 가능함. Motion-aware verifier로 후보를 늘려 성능을 올리는 방식은 다른 world model 기반 정책의 test-time search에도 이식 가능함.
- Explicit-but-compact future representation이라는 설계축은 '무엇을 예측할 것인가'를 재정의하는 world model 논의로 이어짐. object-centric 3DGS 기반 future prediction으로 확장할 수 있음.
- OOD에서 이득이 두드러진다는 결과는 failure detection·recovery 연구에서 명시적 미래 예측이 분포 밖 상황을 언제 더 잘 잡아내는지를 살펴볼 근거로 쓸 수 있음.

---

### 9. [64점] JEPA-WAM: Connecting Generated Visual Instructions to World Action Models through JEPA Latent Representations

- **분야**: VLA · **robotics relevance**: 9/10
- **arXiv**: [2609.20277](https://arxiv.org/abs/2609.20277) ([PDF](https://arxiv.org/pdf/2609.20277))
- **저자**: Tianbin Liu, Jian Zhu, Taiyi Su, Jianjun Zhang, Chong Ma, Zitai Huang, Yi Xu
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **Comments**: 11 pages, 4 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 World Action Model이 언어 지시보다 시각적 맥락에 의존해 지시를 제대로 따르지 않는 문제를 T2I로 생성한 다수의 목표 이미지로 보완함. 이 이미지를 frozen V-JEPA로 인코딩해 video·action expert에 조건으로 넣어 instruction-following을 개선함.

**Core innovation & methodology**

- 언어 지시 하나당 off-the-shelf T2I 모델(DreamLite)로 여러 seed의 task-completion 이미지 bank를 오프라인 구축함. T2I는 학습하지 않음.
- 학습 시 bank에서 이미지 하나를 샘플링해 frozen V-JEPA 2.1로 인코딩하고 spatial pooling 후 projector를 거쳐 goal token으로 압축함.
- goal token을 cross-attention으로 video expert와 action expert 양쪽에 동시에 조건을 줌. 기반 모델인 Fast-WAM(경량 World Action Model) 구조는 그대로 유지하고 조건만 추가함.
- 생성 이미지가 실제 작업공간과 외형이 달라도 V-JEPA의 latent prediction이 저수준 외형 차이를 걸러내고 공간 구조는 보존한다고 주장함.

**Novelty vs. prior works**

- 핵심은 기존 WAM(Fast-WAM)에 frozen T2I와 frozen V-JEPA를 붙여 goal-image conditioning 모듈을 추가한 것으로, 새 representation이나 새 objective를 제안하진 않음.
- GRIF·Interleave-VLA 같은 visual goal conditioning 계열과 목적은 같고, 차이는 goal image를 사람이 주지 않고 T2I로 생성한다는 점뿐임. formulation 신규성은 제한적임.
- behaviorally overlapping task로 구성한 ID/OOD-S(장면 변경)/OOD-I(지시 변경) 실로봇 벤치마크는 instruction grounding 실패를 드러내는 설계로, 평가 방법론 자체의 기여는 있음.

**Benchmark results**

- 11-task 실로봇 벤치마크에서 ID 87.3%, OOD-S 74.5%, OOD-I 80.9%로 Fast-WAM(77.3/47.3/66.4) 대비 10.0/27.2/14.5%p, π0(30.0/7.3/23.6) 대비 큰 폭으로 앞섬.
- 개선폭은 OOD-S에서 가장 큼(27.2%p). Sort Toys에서 학습에 없던 물체 카테고리에도 80.0% 성공(Fast-WAM 10.0%, π0 0.0%)해 시각적 shortcut 의존 완화를 보여줌.
- goal bank 크기를 64에서 1,024로 늘리면 OOD-I 성공률이 58.8%에서 75.0%로 상승하나 개별 task 단위로는 단조 증가하지 않음.
- 생성 이미지(J-64) 73.8%가 실제 demonstration keyframe(KF-64) 68.8%보다 높아 생성 이미지가 더 task-relevant한 신호를 준다고 주장하나 8-task subset의 작은 비교임.
- 학습 데이터 1,370개 real demo를 자체 수집한 소규모 벤치마크라 일반화 범위는 제한적임.

**Top-tier conference 적합성 — 58/100 · 추천 venue: ICRA**

VLA instruction grounding 문제를 다루고 실로봇 3-setting 벤치마크로 명확한 개선폭을 보여줌. 다만 방법이 frozen 기성 모델 두 개를 이어붙인 conditioning module 추가 수준이라 top-tier oral 후보로는 약함.

**추천 이유 & 누리랩 연구와의 연결점**

- VLA 우선 주제와 직결되나 방법보다 '언어 신호가 부족하면 시각적 shortcut에 의존한다'는 문제 진단이 더 유용함. instruction grounding 관련 실험의 진단 프레임으로 참고할 만함.
- OOD-S/OOD-I를 분리한 behaviorally overlapping benchmark 설계는 다른 VLA 평가에도 재사용 가능한 형식임.

---

### 10. [64점] AthenaZero: A low-inertia, bimanual robot for dynamic manipulation

- **분야**: Manipulation (Hardware) · **robotics relevance**: 8/10
- **arXiv**: [2609.19194](https://arxiv.org/abs/2609.19194) ([PDF](https://arxiv.org/pdf/2609.19194))
- **저자**: Andrew S. Morgan, Gregory Xie, Capprin Bass, Rachel Thomasson, Chunpeng Wang, Erfan Shahriari, Harrison Busa, Oluwaseun Araromi 외 18명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Videos attached as ancillary. Cover article to September 2026 issue of Science Robotics
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 관성을 사람 팔 수준으로 낮춘 quasi-direct drive 양팔 로봇 AthenaZero를 만들어 던지기·받기·타격 같은 밀리초 단위 동적 조작을 시연한 하드웨어 논문임. 테니스공 30.8m/s 던지기, 타격 82% 성공률 등 실로봇 성능을 정량 검증했으나 학습 알고리즘 기여는 없음.

**Core innovation & methodology**

- quasi-direct drive(QDD) 액추에이터와 mass remotization으로 관성을 사람 팔 수준(post-shoulder mass 5.99kg)까지 낮춘 22 액추에이터, 27 관절 양팔 로봇을 설계함
- q-axis current만으로 토크를 추정해 힘/토크 센서 없이 backdrivability와 torque transparency를 확보하는 액추에이터 구조를 씀
- 던지기·타격에는 direct collocation 기반 trajectory optimization(SNOPT)과 온라인 재조정을, 받기에는 anisotropic operational-space impedance 제어를 결합함
- effective mass를 human arm·Barrett WAM·Franka FR3·UR5e·iiwa14와 정량 비교해 낮은 관성이 control authority와 충돌 흡수에 미치는 영향을 이론·실측 양쪽으로 검증함

**Novelty vs. prior works**

- 저관성 매니퓰레이터 자체는 Barrett WAM, AMBIDEX 같은 선행 연구가 있으나, 이 논문은 복잡한 tendon-routing 없이 단순한 belt·parallel linkage 전달만으로 유사한 effective mass를 달성했다고 주장함
- 학습 기반 기여는 없음(저자도 명시). trajectory optimization과 impedance 제어는 기존 방법론을 적용한 수준이라 알고리즘 novelty보다 하드웨어 플랫폼 자체가 기여임
- baseline과의 본질적 차이는 관성을 compliance나 force-feedback으로 숨기는 방식이 아니라 실제로 줄이는 설계 철학이며, pendulum impact test로 FR3 대비 충돌력이 124N 대 208N으로 낮음을 직접 측정해 뒷받침함

**Benchmark results**

- 한 팔 기준 테니스공(57g) 던지기 최고 속도 30.8m/s, 정확한 양팔 던지기는 야구공(145g) 21.4m/s (25cm×25cm 타겟 내)
- 받기는 7.3m 거리에서 최대 18.3m/s(반응시간 0.398s) 성공했고, 18.4m 투수판 거리로 환산하면 46.1m/s에 해당하나 고속 구간에서는 성공률이 크게 떨어짐(손바닥 튕김 문제)
- 타격은 33회 스윙 중 27회 성공(82%), 13.4m/s 투구 기준
- 로봇 대 로봇 캐치볼은 최대 8회 연속, 로봇-인간은 12회 연속 성공, 타격 연습은 약 3분간 지속됨
- pendulum impact test에서 effective mass 0.83kg(실측)으로 FR3의 3.3kg 대비 약 4배 낮음을 정량 확인함

**Top-tier conference 적합성 — 58/100 · 추천 venue: RSS**

이미 Science Robotics 2026년 9월호 표지 논문으로 출판된 완성도 높은 시스템 논문임. 정량적 effective mass 분석과 반복 가능한 실로봇 dynamic task 실험이 강점이나 학습 알고리즘 기여가 없어 CoRL·NeurIPS 같은 ML 중심 학회보다는 RSS·ICRA 하드웨어·시스템 트랙에 적합함.

**추천 이유 & 누리랩 연구와의 연결점**

- 낮은 관성·backdrivable 하드웨어는 접촉 실패 후 회복 동작을 안전하게 시도할 수 있는 물리적 여유를 주므로 test-time failure recovery 실험 플랫폼으로 고려할 만함
- 던지기·받기처럼 밀리초 단위 타이밍이 중요한 태스크는 기존 VLA 정책의 반응 속도 한계를 드러내는 벤치마크로 쓸 수 있음
- q-axis current 기반 암묵적 토크 감지는 힘/tactile 센서 없이 접촉을 감지하는 저비용 대안으로, active perception이나 contact-rich manipulation 연구에 참고할 만함

---

### 11. [64점] CoRef-GS: Cooperative Referring Gaussian Splatting for Multi-Agent Scene Understanding

- **분야**: 3D Vision · **robotics relevance**: 8/10
- **arXiv**: [2609.20586](https://arxiv.org/abs/2609.20586) ([PDF](https://arxiv.org/pdf/2609.20586))
- **저자**: Zhikun Zhou, Kunyu Peng, Runyi Yang, Junhao Cai, Di Wen, Ruiping Liu, Danda Pani Paudel, Yi Zhou 외 2명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: The established benchmark and source code will be publicly released at this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 64점

> 💡 여러 로봇이 각자 만든 open-vocabulary Gaussian map을 정합·융합한 뒤에도 언어 지시를 풀 수 있게 만든 cooperative referring Gaussian splatting 방법임. Sim(3) 정합과 CLIP 기반 instance 매칭, view-conditioned relation graph를 결합함. real-world referring mIoU를 52.6%에서 68.8%로 올림.

**Core innovation & methodology**

- 문제를 cooperative referring Gaussian grounding으로 새로 정의함. 여러 로봇이 독립적으로 만든 semantic Gaussian map을 정합·융합한 뒤에도 geometric alignability, instance-level semantic comparability, view-conditioned relation reasoning이 동시에 성립해야 한다는 요구조건을 명시함.
- 각 agent는 OpenGaussian 방식으로 CLIP 정렬 semantic embedding과 instance codebook을 가진 local Gaussian map을 독립적으로 구축함. 모든 agent가 같은 CLIP 공간을 쓰기 때문에 별도 재학습 없이 cross-agent 비교가 가능함.
- Cross-Agent Alignment: NetVLAD/SuperPoint/LightGlue로 coarse Sim(3) 초기화를 구한 뒤, 두 맵을 렌더링해 RGB-depth photometric loss로 정합을 정밀화함(PhotoReg 방식 확장). 이후 semantic+geometric 유사도로 중복 instance를 매칭해 global identity를 부여함.
- Query 시점에는 scene별 referring feature를 새로 학습하지 않고, querying viewpoint에서 후보 instance mask를 렌더링한 뒤 방향성 있는 target-landmark relation graph를 GNN(ReLaGS 방식 차용, Replica 21개 predicate로 offline 학습)으로 추론함.

**Novelty vs. prior works**

- 가장 가까운 선행연구는 단일 맵 referring인 ReferSplat과 geometry/photometric만 다루는 RegGS·PhotoReg임. 본 논문은 '정합 후에도 언어 질의가 유효한가'라는 지점에서 두 갈래를 처음 연결함.
- 핵심 차별점은 새 architecture가 아니라 설계 원칙임. scene-specific referring feature 대신 공유 CLIP embedding과 query-time rendering을 써서 재학습 없이 query 호환성을 유지함. Tab.3a에서 ReferSplat은 정합 후 mIoU가 51.58% 상대적으로 떨어지는 반면 본 방법은 변화가 없어 이 설계 선택의 효과를 확인함.
- 다만 정합 파이프라인(coarse Sim3+photometric refinement)과 relation reasoning(GNN)은 각각 PhotoReg, ReLaGS의 구성요소를 그대로 가져와 multi-agent 세팅에 적용한 것이라 방법 자체의 새로움은 제한적임.

**Benchmark results**

- Simulation 정합 오차: coarse 초기화 2.58°에서 refinement 후 0.15°로 감소. real-world는 3.70°에서 3.39°로 개선폭이 작음.
- Real-world referring mIoU: ReferSplat 52.6%에서 68.8%로 개선, mAcc는 82.4%에서 89.0%로 개선.
- Cooperative fusion 효과: 개별 local map(Agent A 41.9%, Agent B 36.4% mIoU) 대비 fused map은 47.5%로, 더 나은 쪽인 Agent A 대비 상대적으로 13.4% 높음(Tab.3b, 논문이 보고한 relative gain 기준).
- Cross-map instance association ablation: 이 모듈을 빼면 mIoU가 47.54%에서 39.06%로 8.48%p 하락함. geometric alignment만으로는 중복 instance 문제가 해결되지 않음을 보여줌.
- CoQuad-Ref benchmark: 실제 quadruped 로봇(Unitree Go2/Go2-W) 8개 real-world scene과 7개 simulation scene으로 구성, MoCap 기반 reference pose 제공. real-world 데이터를 직접 수집한 점은 긍정적이나 2대 로봇·15개 scene으로 규모는 작음.

**Top-tier conference 적합성 — 55/100 · 추천 venue: CoRL**

실제 quadruped 두 대로 수집한 CoQuad-Ref benchmark와 real-world 정합·referring 성능 개선이 강점임. 다만 정합·relation reasoning 모듈이 대부분 기존 기법(PhotoReg, ReLaGS)의 재조합이라 방법론적 참신성은 제한적이고, 두 agent·15개 scene 규모라 확장성 검증이 부족해 rejection risk로 작용할 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- Multi-agent Gaussian map을 scene graph/semantic mapping 관점에서 다룬 사례로, 누리랩의 object-centric 3D representation·scene graph 연구와 직접 연결됨.
- 정합 후에도 query 호환성을 유지하는 아이디어는 robot memory나 multi-session mapping에서 재학습 없이 갱신되는 semantic map 문제로 확장 가능함.
- View-conditioned relation reasoning 모듈은 failure detection에서 로봇 시점 기준으로 실패 원인이 되는 물체를 지목하는 방식으로 재활용할 여지가 있음.

---

### 12. [62점] Agile-WAM: An Agile Tactile World Action Model for Contact-Rich Robot Control

- **분야**: World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.20761](https://arxiv.org/abs/2609.20761) ([PDF](https://arxiv.org/pdf/2609.20761))
- **저자**: Hanchu Zhou, Brendan Lynch, Raman Goyal, Dechen Gao, Begum Kasap, Boqi Zhao, Junshan Zhang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 큰 pretrained video backbone 없이 시각과 촉각을 하나의 latent로 융합해 곧바로 action·미래 vision·미래 tactile을 flow matching으로 생성하는 Agile-WAM을 제안함. 시각은 긴 horizon, 촉각은 다음 프레임으로 예측 시점을 분리함. 실로봇 5과제에서 baseline 대비 성공률이 높아졌고 지연은 표 기준 10.35ms임.

**Core innovation & methodology**

- 기존 tactile WAM(Tactile-WAM, VTAM, Dream-TAC)은 큰 pretrained video 생성 backbone에 tactile을 얹어 추론 비용이 크고 edge 배포가 어려움. 이를 경량 구조로 대체하는 것이 목표임.
- 현재 관측(RGB+tactile force field+proprioception)을 하나의 latent z0로 인코딩해 flow의 source로 직접 쓰고, cross-attention 조건부여 없이 z0에서 action·미래 vision·미래 tactile latent(z1)로 바로 velocity field를 학습함. 저자들의 이전 연구 VITA의 noise-free flow matching을 vision-tactile-action으로 확장한 구조임.
- vision은 실행되는 action chunk 길이만큼 먼 시점(h_vis=h)을, tactile은 다음 프레임(h_tac=1)을 예측하도록 supervision을 분리하는 multi-horizon 설계를 씀. 시각은 인접 프레임 간 중복이 크고 촉각은 접촉 시 급변한다는 관찰에 기반함.
- VITA처럼 action encoder/decoder로 latent action 공간을 만들고, ODE로 생성된 latent도 다시 decoder에 통과시켜 학습·추론 시 latent 불일치를 줄임.

**Novelty vs. prior works**

- 가장 가까운 선행연구는 저자들 자신의 VITA(vision-to-action flow matching, tactile 없음)와 큰 backbone을 쓰는 Tactile-WAM임. 본 논문은 VITA 구조에 tactile modality와 multi-horizon 예측을 얹은 확장에 가까움.
- 가장 본질적인 기여는 architecture 자체보다 '시각과 촉각은 다른 시간축에서 supervise해야 한다'는 관찰임. 동일 horizon을 쓰면 성능이 떨어진다는 ablation(Fig.5c)으로 이를 뒷받침함.
- Cross-attention 조건부여를 없애 latency를 낮춘 부분은 VITA의 핵심 아이디어를 그대로 재사용한 것이라 backbone 자체의 새로움은 제한적임.

**Benchmark results**

- Simulation(ManiFeel, 9과제)에서 대체로 VITA-VT·Tactile-WAM·DP류를 상회함. 예: Bulb Screw 92.67%(VITA-VT 87.33%, Tactile-WAM 4.00%), Nut Bolt Threading 92.67%(Tactile-WAM 13.33%).
- 실로봇 5과제(Flexiv Rizon 4) 성공률을 직접 평균하면 Agile-WAM 63%(0.80/0.55/0.65/0.30/0.85), VITA-VT 48%, VITA 33%임. 단 Peg Insertion에서는 VITA-VT(0.60)가 Agile-WAM(0.55)보다 높아 모든 과제에서 우위는 아님.
- 초록의 '29.4% relative gain, 11.9ms latency'는 Table III의 시뮬레이션 latency(10.35ms, RTX 4090)와 정확히 일치하지 않고 real-world 측정 조건이 본문에 별도로 명시되지 않아 상세 확인 불가.
- 추론 효율: Agile-WAM 10.35ms/96.62Hz로 VITA(9.71ms) 대비 1.07배 느린 수준에 그치고, DP(408.59ms) 대비 약 39배 빠름.
- Ablation: 양쪽 모두 같은 horizon을 쓰면 성능이 떨어지고, world modeling loss(vis+tac)를 제거해도 성능이 떨어져 multi-horizon 설계와 joint prediction 둘 다 기여함을 확인함.

**Top-tier conference 적합성 — 52/100 · 추천 venue: ICRA**

촉각과 시각을 서로 다른 시간축으로 예측하게 만든 설계와 실로봇 5과제에서의 접촉 유지형 회복 행동 시연이 설득력 있고, 10ms대 latency로 edge 배포 가능성을 보인 점이 실용적 강점임. 다만 backbone이 저자 자신의 선행연구 VITA를 tactile로 확장한 구조라 architecture 참신성이 낮고, 초록의 11.9ms 수치가 본문 표와 불일치해 실험 보고의 엄밀성에 의문이 남음.

**추천 이유 & 누리랩 연구와의 연결점**

- Tactile perception과 contact-rich manipulation은 누리랩 우선 주제와 직접 맞닿아 있고, multi-horizon 아이디어는 force·audio 등 다른 멀티모달 world model에도 그대로 적용 가능함.
- 실로봇에서 나타난 접촉 유지형 재탐색 행동은 failure detection·recovery 연구에서 촉각 기반 recovery policy 설계 참고 사례로 쓸 수 있음.
- VITA 계열의 noise-free flow matching은 candidate를 빠르게 여러 개 생성할 수 있어, MoWAM 식의 inference-time scaling과 결합하는 아이디어로 이어질 수 있음.

---

### 13. [59점] Imagine-TAMP: Imagination-Guided Task and Motion Planning in Partial Observability

- **분야**: Manipulation / TAMP · **robotics relevance**: 8/10
- **arXiv**: [2609.20396](https://arxiv.org/abs/2609.20396) ([PDF](https://arxiv.org/pdf/2609.20396))
- **저자**: Antareep Singha, Shivaram Kumar, Yoonwoo Kim, Yoonchang Sung
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 64점

> 💡 부분관측 상태에서 로봇이 관측할지 방해물을 치울지를 결정하는 문제를 다룸. VLM으로 얻은 semantic belief와 생성모델로 상상한 미관측 geometry를 결합해 symbolic plan skeleton에 non-unit cost를 매기는 TAMP(task and motion planning) 프레임워크 Imagine-TAMP를 제안함. 시야가 제한된 선반 환경에서 성공률을 46.0%에서 84.0%로 높임.

**Core innovation & methodology**

- 기존 PO-TAMP(partially observable TAMP)는 symbolic action 개수나 단순 heuristic으로 plan skeleton을 고르는데, 이는 특정 관측이 실제로 target을 드러낼 확률을 반영하지 못한다는 문제에서 출발함
- particle belief로 target pose 불확실성을 표현하고, VLM에 현재 RGB와 후보 occluder를 물어 얻은 semantic score로 particle weight를 재조정함(semantic belief shaping)
- 생성형 3D reconstruction 모델(SAM 3D)로 미관측 영역의 geometry를 상상해 결정론적 scene hypothesis(ghost target)를 만들고, 그 위에서 BFS(breadth-first search)로 여러 symbolic plan skeleton 후보를 생성함
- manipulation action은 정규화된 joint 거리로, DETECT action은 상상한 geometry를 렌더링한 segmentation mask 기반 visibility cost로 평가하는 non-unit cost를 매겨, cost가 가장 낮은 skeleton 하나만 continuous motion 단계로 넘김

**Novelty vs. prior works**

- 가장 가까운 prior work는 VLM 기반 semantic belief shaping만 쓰는 CoCo-TAMP, 정보 습득과 위험을 고려하는 TAMPURA, anticipatory cost로 plan을 구분하는 최근 연구임
- 본질적 차이는 어디에 있을 것 같은지를 정하는 semantic reasoning과 어떻게 노출시킬지를 정하는 geometric imagination을 분리해 결합한 점이며, 상상한 geometry를 실제 실행이 아니라 skeleton 비교용 heuristic으로만 쓴다는 점에서 amodal reconstruction 계열과도 다름
- 다만 cost 함수 자체는 joint 거리·픽셀 수 기반의 근사 heuristic이고 belief update·determinize-and-replan 골격은 SS-Replan·CoCo-TAMP를 그대로 따라, formulation 신규성보다는 기존 PO-TAMP 파이프라인에 두 개의 근사 cost 항을 끼워 넣은 조합에 가까움

**Benchmark results**

- 시야가 정면 grid로 제한된 선반 환경(occluder 9~15개, n=50 paired trial)에서 unit-cost 46.0%에서 motion-cost 84.0%로 성공률이 오르고, replan 횟수는 11.50회에서 4.50회로 줄어듦(p=3.8×10⁻⁶)
- 반구 형태로 시점을 자유롭게 고를 수 있는 tabletop 환경에서는 unit-cost도 96.0%로 이미 포화되어 있어 motion-cost의 이득(100.0%)이 크지 않음. 즉 이 방법의 효과는 시야가 제한된 상황에 국한됨
- occluder 개수를 5개에서 15개로 늘리면 unit-cost는 80.0%에서 35.0%로 급락하지만 motion-cost는 85~90%를 유지함
- visibility weight(λ_vis)를 0에서 5.0까지 바꿔도 성공률 자체는 84.0%로 고정되고 trajectory 길이·replan·제거 occluder 수만 줄어듦. manipulation을 허용하는 것 자체가 성공 회복의 주 요인이고 visibility 예측은 효율만 개선함
- semantic belief 추가 실험(n=30 cluster scene)에서 MC+Gemini 조합이 100.0% 성공, replan 1.40회로 MC 단독(83.3%, 6.30회)보다 크게 개선. 반대로 UC+VLM은 73.3%에 그쳐 geometry 평가 없이는 belief 개선만으로 한계가 있음을 보임
- real robot 검증은 4회 시행에 그쳐, geometry-only ablation 대비 replanning 3.25회에서 1.50회, planning time 232.0초에서 158.5초로 32% 줄었다는 결과의 통계적 신뢰도는 낮음

**Top-tier conference 적합성 — 55/100 · 추천 venue: ICRA**

관측 대 조작을 결정하는 문제를 관측이 실제로 정보를 줄 확률로 정량화한 문제 설정은 명확하고, 대규모 sim 실험에서 통계적으로 유의한 개선을 보임. 다만 cost 함수는 근사 heuristic 조합이라 formulation 자체의 신규성은 제한적이고 real robot 검증이 4회뿐이라 rejection risk가 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- active perception/NBV와 TAMP·long-horizon planning 우선 주제에 해당함. 관측 행동의 가치를 상상으로 미리 평가한다는 아이디어는 실패 감지 이후 재관측 여부를 결정하는 failure recovery 연구에 바로 옮겨볼 만함
- semantic belief와 geometric imagination을 분리해 결합하는 구조는 VLM의 상식적 판단과 3D reconstruction 모델의 기하학적 판단을 각각 다른 역할로 쓰는 설계로, world model 기반 test-time planning 연구에서 두 종류의 상상을 나눠 쓰는 참고 사례가 됨

---

### 14. [58점] Improving Cross-embodiment Transfer in Latent Action Models with Action-Similarity Supervision

- **분야**: VLA / Manipulation · **robotics relevance**: 8/10
- **arXiv**: [2609.19846](https://arxiv.org/abs/2609.19846) ([PDF](https://arxiv.org/pdf/2609.19846))
- **저자**: Maxime Alvarez, Renzo Caballero, Tatsuya Matsushima, Yusuke Iwasawa, Yutaka Matsuo
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 66점

> 💡 LAM(latent action model)에서 embodiment마다 latent가 다르게 인코딩되는 문제를 줄이려고, latent action 쌍의 유사도를 ground-truth action 쌍의 유사도에 맞추는 action-similarity supervision을 적용함. RoboTwin 2.0 두 bimanual robot 간 cross-embodiment 전이 실험에서 padded-action baseline 대비 성공률을 2.55배로 높임.

**Core innovation & methodology**

- LAM(latent action model)은 action label 없는 영상만으로 latent action을 학습해 여러 embodiment에 공유하려는 목적이지만, embodiment별 시각 특징이 섞여 같은 동작도 로봇마다 다른 latent로 인코딩됨
- action-similarity supervision을 적용함. 배치 안 latent action 쌍의 cosine similarity를 ground-truth action 시퀀스 쌍의 similarity에 맞추는 손실(L_sim)을 추가하되, ground-truth action 자체는 예측하지 않음
- ground-truth similarity는 절대 pose가 아니라 delta motion 기준으로 계산하고, 프레임 한두 개의 어긋남을 허용하는 temporal shift로 정렬함
- similarity 계산에 end-effector delta를 쓰고 cross-embodiment 쌍까지 포함하는 조합이 실험 중 가장 좋은 결과를 보임

**Novelty vs. prior works**

- 가장 가까운 prior work는 action prediction head를 auxiliary loss로 쓰는 LAOM, weighted InfoNCE에 structural alignment loss를 더한 VILA(원래 목적은 view-invariance)임
- 본 논문의 손실 항은 VILA의 global structural similarity term을 그대로 가져와 목적을 view-invariance에서 cross-embodiment transfer로 바꿔 적용한 것으로, 손실 함수 자체의 신규성은 제한적임
- 저자도 이 작업을 study로 규정함. RoboTwin 2.0의 두 embodiment(둘 다 bimanual gripper arm)로 범위가 좁고, 자체 비교에서도 ViLA-style InfoNCE가 제안 방식보다 근소하게 더 나은 transfer 성능(63.3% vs 61.3%)을 보임

**Benchmark results**

- RoboTwin 2.0 dual-arm sim에서 aloha와 franka에 각각 3개씩 disjoint task를 배정하고 서로의 task로 closed-loop 평가함(50 episode/pair)
- 제안 구성 중 가장 성능이 좋은 LAOM+sim-EE-X(end-effector delta 기반 similarity, cross-embodiment 쌍 포함)는 transfer 성공률 61.3%로 baseline인 ViLA-style InfoNCE(63.3%)에는 못 미치지만 ground-truth padded-action baseline(24.0%)의 2.55배이자 in-embodiment 성능(69.3%)의 88.5%를 유지함
- 같은 label로 action prediction supervision(LAOM+pred)과 비교하면 similarity supervision이 transfer에서 12.0포인트 더 높음(46.0% vs 34.0%)
- label을 10%로 줄여도 transfer 65.7%를 유지해 label efficiency를 보였으나, decoder 학습 데이터까지 함께 줄이면 31.0%로 떨어져 decoder 데이터가 별도 제약으로 남음
- 학습에 없던 3번째 embodiment(UR5)로 확장한 부록 실험에서는 decoder fit과 open-loop replay는 되지만 closed-loop 성공률이 0%로, 정책이 새 embodiment의 시각 관측으로 일반화하지 못하는 한계를 확인함

**Top-tier conference 적합성 — 50/100 · 추천 venue: ICRA**

cross-embodiment latent action 전이라는 로봇학습 핵심 병목을 통제된 실험으로 파고들어 여러 loss·backbone·정책 크기 조합을 체계적으로 비교한 점은 강점임. 다만 손실 함수 자체는 기존 VILA 항의 재적용이고 두 embodiment 모두 bimanual gripper로 이질성이 낮으며, 새 embodiment 일반화 실패까지 정직하게 보고해 신규성보다 실험적 정리에 가까움.

**추천 이유 & 누리랩 연구와의 연결점**

- cross-embodiment VLA와 latent action model 연구 라인에 직접 참고할 만함. ground-truth action을 직접 예측하지 않고 관계(similarity)만 맞추는 relational supervision 설계는 embodiment 특정 정보를 배제한 표현을 만들 때 응용 가능함
- UR5로의 closed-loop 실패는 latent action pretraining만으로는 새 embodiment의 시각 조건화가 해결되지 않음을 보여줌. VLA test-time adaptation·world model 연구에서 시각 조건과 latent action을 분리하는 문제로 이어붙일 수 있음

---

### 15. [58점] Astronex-World 1.0: Real-Time Interactive World Model Foundation

- **분야**: World Model · **robotics relevance**: 8/10
- **arXiv**: [2609.20034](https://arxiv.org/abs/2609.20034) ([PDF](https://arxiv.org/pdf/2609.20034))
- **저자**: Xin Zhou, Cong Miao
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: Technical report. 25 pages, 13 figures, 10 tables. Project page: this https URL ; Code: this https URL ; Weights: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 Wan2.2 5B 영상 prior에 카메라·액션·이벤트 조건을 통합하고 5단계 distillation recipe로 causal 실시간 world model을 만든 기술 리포트임. 2×L20 GPU만으로 학습해 WBench Full에서 13.6B~22B급 모델과 맞먹는 점수를 냈지만 핵심 구성요소는 대부분 기존 기법의 재조합이고 action 인터페이스는 로봇 데이터로 검증되지 않았음.

**Core innovation & methodology**

- 5B 모델 위에 카메라 조건(PRoPE, camera-as-relative-positional-encoding)·64차원 continuous action·embodiment ID를 30개 트랜스포머 레이어 전체에 주입하는 통합 control interface를 얹음
- bidirectional teacher와 block-causal student를 분리해, KV caching 기반 실시간 causal streaming과 오프라인 고품질 생성을 한 backbone family로 제공
- 5단계 학습 recipe(카메라/액션 control adaptation → block-causal 변환 → online UniPC trajectory distillation → mixed-domain causal SFT → asymmetric DMD/DMD2)로 5B 모델을 2×L20 GPU만으로 학습
- 롤아웃 중 특정 latent frame에 텍스트 이벤트를 삽입해 이미 생성된 히스토리는 보존하면서 이후 장면만 바꾸는 event 인터페이스를 제공

**Novelty vs. prior works**

- PRoPE(camera as relative positional encoding), Causal Forcing/Causal Forcing++, DMD/DMD2, attention sink 등 핵심 구성 요소는 모두 기존 연구에서 가져온 것으로, 이 논문의 기여는 새 알고리즘이 아니라 기존 기법을 한 파이프라인으로 재조합한 것임
- Wan2.2-TI2V-5B라는 강한 pretrained prior에 의존해 두 장 GPU로 13.6B~22B급 모델과 경쟁하는 효율적 재현 레시피를 보여준 것이 실질 기여이고, 새 representation이나 새 learning paradigm은 아님
- action-output(inverse dynamics decoder) 인터페이스는 "reserved"일 뿐 실제 로봇 데이터로 학습·평가되지 않아, embodied intelligence 관련 novelty 주장은 아직 검증되지 않은 잠재력에 머무름

**Benchmark results**

- WBench Full 289에서 70.0점(Quality 78.3, Setting 73.8, Interaction 47.6, Consistency 82.4, Physical 68.1)으로 같은 5B급 YUME 1.5(68.9)를 능가하고 13.6B LongCat-Video(69.9), 14B Helios(69.7)보다 높으며 22B LTX-2.3(70.9)에 0.9점 차로 근접함
- Interaction 항목은 WBench-Navi 서브셋(63.4)에서 WBench Full(47.6)로 크게 떨어져 event editing·subject action·perspective switching에 약함을 저자도 인정함
- DMD distillation 후 내부 basketball 시퀀스에서 subject motion 진폭이 bidirectional teacher 대비 19%까지 줄어드는 over-staticization 문제가 확인됨(공개 벤치마크 아니며 모델 간 비교 불가)
- VBench 1.0은 T2V 6220개 중 240개, I2V 5590개 중 118개만 생성한 부분 실행 결과로 전체 벤치마크 커버리지가 아님
- 실로봇/실주행 평가는 전무하고 action 인터페이스는 post-training 대상으로만 남겨둔 상태임

**Top-tier conference 적합성 — 38/100 · 추천 venue: CVPR**

효율적인 학습 레시피와 재현성은 강점이나 핵심 구성요소가 기존 기법의 조합이라 conceptual novelty가 약함. VBench를 일부만 실행해 완전성이 떨어지고 robot·driving 검증이 전무해 리뷰어가 "조합형 엔지니어링" 문제로 볼 위험이 큼.

**추천 이유 & 누리랩 연구와의 연결점**

- 64차원 continuous action과 embodiment ID를 world model 전 레이어에 주입하는 conditioning 방식은 VLA용 world model 설계 시 재사용할 만함
- event prompt로 롤아웃 도중 특정 시점에 상황을 삽입하는 인터페이스는 장애물 등장 같은 counterfactual 상황을 주입해 test-time에 recovery policy를 평가하는 데 응용 가능함
- action-output head가 실제 로봇 데이터로 검증되지 않았으므로, 누리랩에서 쓰려면 먼저 DROID 수준 이상의 실로봇 action grounding 성능을 확인해야 함

---

## 오늘의 핵심 연구 트렌드 종합

- **실패를 명시적 진단 대상으로 정식화** — [MAGMA-GEN](https://arxiv.org/abs/2609.20056)은 실패가 판단 오류인지 실행 노이즈인지 구분해 검증된 것만 학습에 쓰고, [Diagnose, Recover, Certify](https://arxiv.org/abs/2609.20304)는 정책이 안 쓰는 액추에이터의 열화(dormant fault)를 새 문제로 정의함. 둘 다 진단과 학습·배포 결정을 분리하는 구조를 취함.
- **World model이 예측 대상을 나눠서 다시 설계됨** — [JEPA-Anything](https://arxiv.org/abs/2609.20800)은 latent target을 직교 factor로 분해하고, [MoWAM](https://arxiv.org/abs/2609.20709)은 video 대신 keypoint motion으로 미래를 압축하고, [Agile-WAM](https://arxiv.org/abs/2609.20761)은 시각·촉각을 지평선 길이를 다르게 예측함. '무엇을 얼마나 예측할지'가 world model 설계의 공통 축임.
- **World model 예측을 test-time에 그대로 활용** — [Feeling Terrain Before Crossing](https://arxiv.org/abs/2609.19863)은 failure risk head로 후보 행동을 CEM으로 고르고, [Imagine-TAMP](https://arxiv.org/abs/2609.20396)는 상상한 geometry로 관측 행동의 가치를 미리 평가하고, [MoWAM](https://arxiv.org/abs/2609.20709)은 motion-aware verifier로 후보 action을 늘려 고름. 예측을 planning·verification에 바로 연결하는 방식이 반복됨.
- **Object-centric 3D 표현이 조작·다중로봇 이해로 확장됨** — [ParticleSplat](https://arxiv.org/abs/2609.19463)은 2D self-supervised particle을 3D Gaussian으로 확장해 편집 가능한 object latent를 얻고, [CoRef-GS](https://arxiv.org/abs/2609.20586)는 여러 로봇의 Gaussian map을 정합한 뒤에도 언어 지시를 풀게 만듦. 3DGS가 렌더링을 넘어 편집·grounding의 기반 표현으로 쓰임.
- **weight 고정 정책에 배포 후 경험을 되먹임** — [TraceFlow](https://arxiv.org/abs/2609.20646)는 성공·실패 trace를 retrieval-guidance로 flow 생성에 반영해 재학습 없이 성능을 누적함. robot memory를 test-time 교정 신호로 쓰는 접근임.

## 유망 연구 방향 및 프로젝트 제안

**검증된 재실행을 촉각·힘 기반 접촉 실패 진단으로 확장**
- research question: manipulation의 접촉 실패(미끄러짐, 그립 실패)에서 원인이 판단 오류인지 접촉 동역학 오차인지를 재실행으로 검증하며 구분할 수 있는가
- 접근·novelty: [MAGMA-GEN](https://arxiv.org/abs/2609.20056)의 진단-제안-재실행 검증 구조에 [Agile-WAM](https://arxiv.org/abs/2609.20761)류 촉각 world model의 contact-rich 예측을 결합해, coach(실패 원인을 진단해 복구 행동을 제안하는 LLM)가 제안한 복구 행동을 실제 재실행이 아니라 촉각 world model rollout으로 저비용 검증함
- 왜 지금·경쟁 prior works: MAGMA-GEN은 시뮬레이터 재실행 비용을 전제하는데 실로봇에서는 재실행 자체가 비쌈. world model rollout으로 검증을 대체하면 실로봇 적용이 가능해짐
- risk·target venue: world model rollout이 실제 접촉 결과와 다를 위험이 큼. 검증 정확도를 먼저 확인해야 함. CoRL을 겨냥함

**Dormant fault 진단을 VLA 배포 전 점검 절차로 재구성**
- research question: 새 task에 VLA 정책을 배포하기 전, 이전 task에서 거의 안 쓰인 관절·그리퍼의 이상을 짧은 probe만으로 찾아낼 수 있는가
- 접근·novelty: [Diagnose, Recover, Certify](https://arxiv.org/abs/2609.20304)의 task-agnostic 진단 예산과 recover-or-abstain 배포 결정을 VLA policy에 적용하고, probe 후보 선택에 world model rollout(counterfactual reasoning)을 결합함
- 왜 지금·경쟁 prior works: 원 논문은 MuJoCo·Box2D 시뮬레이션에서만 검증돼 실로봇 VLA에 적용된 사례가 없음. VLA 배포 안정성은 아직 이 각도로 다뤄지지 않음
- risk·target venue: 진단 예산과 정확도의 trade-off가 실로봇에서 얼마나 벌어지는지가 관건. RSS를 겨냥함

**Orthogonal factorization을 object-centric 3DGS에 적용**
- research question: [JEPA-Anything](https://arxiv.org/abs/2609.20800)의 factor 분해가 object-centric 3D 표현에서도 유지되는가, 즉 물체별 latent를 직교 factor로 나눠 하나만 바꿔도 나머지 물체 예측이 안 무너지는가
- 접근·novelty: [ParticleSplat](https://arxiv.org/abs/2609.19463)의 particle 단위 3D 표현에 orthogonal predictive factorization을 적용해, 물체 하나의 위치를 counterfactual하게 바꿨을 때 다른 물체 예측에 영향이 없는 조작 가능한 world model을 구성함
- 왜 지금·경쟁 prior works: ParticleSplat은 편집 가능하다는 것만 보였고 예측 붕괴 방지 기제는 없음. JEPA-Anything은 factorization을 일반 latent에서만 검증함
- risk·target venue: object 수가 늘면 factor 수도 늘어야 해 확장성이 문제될 수 있음. NeurIPS/CoRL을 겨냥함

**Robot memory의 실패 신호를 세분화해 재발 방지 정확도 높이기**
- research question: [TraceFlow](https://arxiv.org/abs/2609.20646)처럼 terminal success/fail bit 하나만 쓰는 대신, 실패 원인 태그(원문에서 확인된 Counting·Occlusion 실패 사례처럼 관측 실패 vs 동작 실패)를 구분해 guidance를 걸면 성능이 더 오르는가
- 접근·novelty: [MAGMA-GEN](https://arxiv.org/abs/2609.20056)의 coach 진단 결과를 TraceFlow의 trace 저장소인 TraceBank의 trace에 원인 라벨로 추가해, 원인별로 다른 guidance 전략(동작 교정 vs 재관측 유도)을 적용함
- 왜 지금·경쟁 prior works: TraceFlow는 원문에서 스스로 "Counting·Occlusion에서 효과 없음"을 한계로 밝혀, 원인 구분 없는 설계의 경계가 이미 드러나 있음
- risk·target venue: 원인 라벨링 비용이 늘면 TraceFlow의 저비용 장점이 사라짐. CoRL을 겨냥함

**상상 기반 관측 가치 평가를 실패 후 재관측 결정으로 확장**
- research question: 실패 감지 직후, 로봇이 바로 복구 동작을 시도할지 먼저 재관측할지를 상상한 geometry 기반 기대 정보 이득으로 결정할 수 있는가
- 접근·novelty: [Imagine-TAMP](https://arxiv.org/abs/2609.20396)의 semantic belief + 생성형 geometry 상상 구조를 failure recovery 시점으로 옮겨, DETECT action의 visibility cost 대신 recovery 성공확률 기대값으로 skeleton을 고름
- 왜 지금·경쟁 prior works: 기존 failure recovery 연구는 재관측 여부를 규칙 기반으로 결정하는 경우가 많고, 상상 기반 가치 평가를 이 결정에 쓴 사례는 없음
- risk·target venue: SAM 3D 기반 상상이 실패 상황(가려짐, 변형)에서도 신뢰할 수 있는지가 불확실함. ICRA를 겨냥함

## 오늘 반드시 읽어야 할 논문

- [JEPA-Anything](https://arxiv.org/abs/2609.20800) — world model의 예측 대상을 직교 factor로 나눈다는 설계 원리가 오늘 논문 중 가장 일반화 가능성이 큼
- [MAGMA-GEN](https://arxiv.org/abs/2609.20056) — 실패 원인을 재실행으로 검증해서만 학습에 쓰는 구조가 failure recovery 데이터 구축에 바로 참고됨
- [Feeling Terrain Before Crossing](https://arxiv.org/abs/2609.19863) — world model에 failure risk를 별도 head로 명시하고 실로봇 두 종에서 검증까지 마침
- [Diagnose, Recover, Certify](https://arxiv.org/abs/2609.20304) — dormant fault라는 새 문제 정식화와 이론적 보장이 결합돼 있어 검증 설계 참고용으로 유용함
- [TraceFlow](https://arxiv.org/abs/2609.20646) — weight 고정 정책에 배포 후 경험을 되먹이는 가장 단순하고 실용적인 test-time 교정 방법임
- [ParticleSplat](https://arxiv.org/abs/2609.19463) — object-centric 3D 표현을 label 없이 얻고 particle 단위로 편집까지 가능함을 보임
- [Imagine-TAMP](https://arxiv.org/abs/2609.20396) — 관측 행동의 가치를 상상으로 미리 평가한다는 아이디어가 active perception 연구에 직접 적용 가능함

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (485편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2609.20056'>MAGMA-GEN: Validated Recovery Supervision from Ambiguous Failures via Counterfactual Re-Execution</a></td><td>78</td><td>10</td><td>Manipulation</td><td>실패한 rollout의 원인을 privileged coach로 진단하고 counterfactual 재실행으로 검증된 recovery 데이터만 남기는 파이프라인이며 실로봇 장기 조작 실험까지 포함해 failure recovery·counterfactual reasoning 우선주제와 정확히 맞아떨어짐</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2609.20277'>JEPA-WAM: Connecting Generated Visual Instructions to World Action Models through JEPA Latent Representations</a></td><td>72</td><td>9</td><td>VLA</td><td>텍스트 지시를 T2I로 생성한 다수의 시각적 목표 이미지로 보강하고 V-JEPA로 인코딩해 World Action Model의 지시 이행력을 높인 방법이며 실로봇 벤치마크에서 pi0와 Fast-WAM을 큰 폭으로 앞섰고 VLA·world model 우선주제와 정확히 맞음</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2609.20800'>JEPA-Anything: Learning Predictive Models across Different Worlds</a></td><td>72</td><td>6</td><td>World Model</td><td>JEPA를 orthogonal predictive factorization으로 확장해 vision부터 control, 분자동역학까지 7개 도메인에 공통 적용한 world model 프레임워크이며 실험 스펙트럼이 넓고 world model 우선주제와 직결됨</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2609.19796'>LIFD: Anchored Diffusion for 3D-Aware Scene Memory in Robotic Manipulation</a></td><td>70</td><td>9</td><td>World Model</td><td>부분관측 상황에서 3D scene memory를 유지하는 manipulation 프레임워크임. rectified-flow로 미관측 영역을 보완하고 실로봇에서 OpenVLA-7B 대비 높은 성공률(56.0% vs 40.5%)을 보임. robot memory와 3D representation 우선주제에 부합함.</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2609.20034'>Astronex-World 1.0: Real-Time Interactive World Model Foundation</a></td><td>70</td><td>8</td><td>World Model</td><td>카메라 궤적과 action, embodiment identifier까지 조건화한 실시간 interactive world model로 5B 모델이 더 큰 모델들과 경쟁하는 성능을 보여 embodied intelligence post-training에 바로 쓸 수 있는 기반임</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2609.19194'>AthenaZero: A low-inertia, bimanual robot for dynamic manipulation</a></td><td>70</td><td>8</td><td>Manipulation</td><td>quasi-direct drive와 원격 전달로 관성을 사람 수준까지 낮춘 양팔 로봇으로 던지기·받기·타격을 실현. Science Robotics 표지 논문으로 하드웨어 기여가 크나 학습 알고리즘 novelty는 아님.</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2609.19863'>Feeling Terrain Before Crossing: World Models for Off-Road Navigation</a></td><td>68</td><td>9</td><td>World Model</td><td>카메라 예측에 proprioception 기반 physical future(slip, tilt 예측)를 추가한 off-road navigation world model임. Husky 실외 산길 주행에서 end-to-end policy가 실패하는 코스를 완주함. world model에 로봇이 느끼는 상태를 결합한 점이 새로움.</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2609.20304'>Diagnose, Recover, Certify: Task Readiness under Hidden Dynamics Changes</a></td><td>68</td><td>8</td><td>RL</td><td>휴면 상태의 액추에이터 열화를 소수의 상호작용으로 진단하고 정책 복구와 신뢰도 하한 인증까지 제공하는 프레임워크로 failure detection·diagnosis·recovery 우선주제와 직접 맞닿아 있고 여러 시뮬레이터에서 검증함</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2609.19846'>Improving Cross-embodiment Transfer in Latent Action Models with Action-Similarity Supervision</a></td><td>66</td><td>8</td><td>VLA</td><td>latent action model의 cross-embodiment 전이를 위해 action-similarity supervision을 제안함. 동일 라벨로도 auxiliary loss보다 성능이 좋고 cross-embodiment 성공률을 두 배 이상 높임. generalist policy의 핵심 병목인 embodiment 간 latent action 정렬 문제에 새 해법을 줌.</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2609.19463'>ParticleSplat: Self-supervised Object-centric Latent Particle Splatting</a></td><td>65</td><td>8</td><td>Manipulation</td><td>3D Gaussian 기반 latent particle로 장면을 object-centric하게 분해하고 robotic manipulation 하위 task 성능까지 검증한 self-supervised representation 연구임</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2609.20646'>TraceFlow: Guiding Frozen Flow-Matching Robot Policies with Success and Failure Traces</a></td><td>64</td><td>9</td><td>VLA</td><td>고정된 flow-matching VLA에 자신의 성공·실패 rollout을 terminal outcome bit 하나로 넣어 test-time guidance field를 만드는 방법임. 실로봇 순서 packing에서 21/50에서 39/50으로, 재학습 없이 47/50까지 개선함. 실패 경험을 가중치 갱신 없이 test-time 신호로 쓴다는 점이 test-time optimization 우선주제에 직접 부합함.</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2609.20396'>Imagine-TAMP: Imagination-Guided Task and Motion Planning in Partial Observability</a></td><td>64</td><td>8</td><td>Manipulation</td><td>VLM 기반 semantic belief와 generative scene 상상으로 관측이냐 조작이냐를 결정하는 TAMP 프레임워크임. viewpoint-constrained 실험에서 성공률이 46%에서 84%로 크게 개선되고 실로봇 계획시간도 32% 줄어듦. 관측 가치를 상상으로 미리 평가한다는 문제설정이 참신함.</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2609.20586'>CoRef-GS: Cooperative Referring Gaussian Splatting for Multi-Agent Scene Understanding</a></td><td>64</td><td>8</td><td>3D Vision</td><td>여러 로봇이 독립적으로 만든 open-vocabulary Gaussian map을 정합한 뒤 querying robot 시점에서 관계추론까지 수행하는 cooperative referring Gaussian splatting임. 회전오차를 2.58도에서 0.15도로 줄이고 real-world referring mIoU를 52.6%에서 68.8%로 개선함. 3DGS와 scene graph를 멀티에이전트 협업에 결합한 정식화가 새로움.</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2609.20709'>MoWAM: Explicit Future Motion Prediction for Efficient World Action Models</a></td><td>62</td><td>9</td><td>World Model</td><td>미래 비디오 생성 대신 구조화된 motion을 예측해 world action model의 추론 비용을 없애는 방법임. LIBERO와 실로봇에서 OOD 강건성이 개선되고 motion-aware verifier로 후보를 늘릴수록 성능이 오름. world model의 무거운 비디오 생성을 경량 motion 표현으로 대체한 점이 world model과 efficient inference 우선주제 모두에 부합함.</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2609.20761'>Agile-WAM: An Agile Tactile World Action Model for Contact-Rich Robot Control</a></td><td>62</td><td>9</td><td>World Model</td><td>시각과 촉각이 다른 시간축으로 변한다는 관찰에서 시각은 긴 offset, 촉각은 다음 프레임으로 예측하는 multi-horizon world action model임. 11.9ms의 낮은 지연으로 실로봇 5과제에서 29.4% 성공률 향상을 보임. 무거운 생성 backbone 없이 tactile world model을 경량화한 기여가 명확함.</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2609.19976'>Compliance for Free: Learning Identifiable Impedance via Bilateral Teleoperation</a></td><td>62</td><td>8</td><td>VLA</td><td>4채널 bilateral teleoperation의 leader arm을 별도 측정치로 써서 pose와 stiffness의 identifiability 문제를 해결하고 VLA에 compliance 출력을 추가함. 접촉력 조절이 가능한 유일한 정책으로 확인됨(p=0.023). contact-rich VLA의 근본적 한계를 겨냥한 참신한 문제 설정임.</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2609.20820'>Workspace Models: Lightweight Robotic Memory via Saliency-Driven Supervision</a></td><td>62</td><td>8</td><td>Manipulation</td><td>학습 시점에만 VLM으로 salient한 과거정보를 골라 경량 latent token으로 distill하고 배포시엔 VLM 없이 이 token만 쓰는 robot memory 방법임. 시뮬레이션과 실기 모두에서 기존보다 가볍고 성능도 더 좋음. VLM in-the-loop 비용을 train-time으로 옮긴 로봇 메모리 설계가 명확한 기여임.</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2609.19315'>GAVEL: Graph World Models for Verified and Efficient Long-Horizon LLM Task Planning</a></td><td>62</td><td>7</td><td>World Model</td><td>명시적 그래프 world model로 LLM plan을 실행 전 검증·수정해 BEHAVIOR-1K 단일태스크 성공률을 41.2%에서 91.8%로 끌어올림. world model 기반 verification·repair라는 formulation과 큰 성능 향상이 결합됨.</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2609.19674'>Conservation Buys Stability and Factoring Buys Counterfactuals in Physical World Models</a></td><td>62</td><td>3</td><td>World Model</td><td>장기 rollout 안정성과 counterfactual 일반화가 서로 다른 구조적 조건에서 나온다는 double dissociation을 물리 world model에서 통제 실험으로 보임. robot dynamics model 설계에 참고할 원리이나 로봇 실험은 없음.</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2609.19669'>Beyond Patch Removal: Persistent Adversarial Effects in Vision-Language-Action Policies</a></td><td>60</td><td>9</td><td>VLA</td><td>VLA policy에 대한 adversarial patch가 제거 후에도 지속되는 효과를 정량화하고 recovery adapter로 완화를 시도해 failure detection·recovery 주제와 직접 맞닿음</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2609.20649'>DexTouch-WM: Learning Action-Conditioned Tactile World Models from Human Touch for Dexterous Robot Manipulation</a></td><td>60</td><td>9</td><td>World Model</td><td>동일한 피에조저항 센서 레이아웃으로 사람과 로봇 촉각을 호환시켜 사람 접촉 데이터로 로봇 contact dynamics를 학습하는 world model임. 로봇 데이터 5시간 고정 후 사람 데이터를 0→100시간 늘리며 held-out 예측이 뚜렷이 개선됨. tactile world model의 데이터 확장축을 사람으로 옮긴 점이 참신함.</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2609.20107'>AnyViewDex: View-Invariant Dexterous Manipulation from RGB Observations</a></td><td>58</td><td>8</td><td>Manipulation</td><td>시뮬레이션에서만 3D geometric supervision을 주고 실제 배포는 monocular RGB만으로 view-invariant dexterous manipulation을 수행하는 방법임. xArm7+LEAP hand 480회 시행에서 76.7% 성공률을 보임. 3D 센싱 없이 뷰 불변성을 얻는 학습 신호 설계가 실용적임.</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2609.20776'>GeoAAC: Geometry-Based Adaptive Action Chunking from Denoising Trajectories in VLA Policies</a></td><td>58</td><td>8</td><td>VLA</td><td>flow matching denoising trajectory의 기하학적 변화가 예측 신뢰도와 양의 상관을 가진다는 점을 이용해 추가 학습 없이 action chunk 길이를 적응시키는 방법임. 실로봇 성공률을 53.3%에서 74.4%로 높임. 기존 생성과정에서 공짜로 얻는 불확실성 신호를 활용한 점이 test-time 우선주제에 부합함.</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2609.19413'>From Rollout to Reset: A Graph-Based Harness for Autonomous Long-Horizon Manipulation Evaluation</a></td><td>58</td><td>7</td><td>Manipulation</td><td>학습된 atomic reset skill 라이브러리와 scene graph 기반 LLM reasoning으로 long-horizon manipulation 평가의 reset을 자동화. AutoEval 대비 reset 성공률(76% vs 52%)과 compositional 일반화(74.7% vs 1.3%) 모두 크게 개선함.</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2609.19817'>RotateIt! Fast and Reliable Single-Arm Garment Unfolding via Online-Adaptive Dynamic Rotation</a></td><td>58</td><td>7</td><td>Manipulation</td><td>단일 팔로 옷을 축 회전시켜 펼치는 새로운 dynamic manipulation primitive를 제안함. sim2real 성공률 75.6%로 quasi-static 대비 큰 개선을 보임. manipulation primitive 자체의 참신성이 있음.</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2609.20575'>Accelerating Visual Policy Learning with Sampling-Based Model Predictive Control</a></td><td>58</td><td>7</td><td>RL</td><td>샘플링 기반 MPC로 행동을 정제하고 first-order policy gradient와 번갈아 학습해 differentiable simulation의 local optima 문제를 완화하는 방법임. 단일 GPU로 로코모션·조작 정책을 학습하고 실제 Go2에 제로샷 전이함. FoPG의 고질적 문제를 겨냥한 방법론적 기여가 뚜렷함.</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2609.20388'>Navi-Agent: Unlocalized Monocular Navigation Agent</a></td><td>56</td><td>8</td><td>Navigation</td><td>좌표 없이 시각 노드-엣지 topology만으로 장소를 추정하는 zero-shot VLN-CE 에이전트임. geometry 없이도 위치확인·진행검증·복구가 가능해 geometry-constrained 방법 중 SOTA를 보임. coordinate-free spatial state 표현이 새로움.</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2609.20659'>HIL-UMI: Bringing Human-in-the-Loop Post-Training of Vision-Language-Action Models to Universal Manipulation Interface</a></td><td>56</td><td>8</td><td>VLA</td><td>handheld UMI 시연 중 현재 정책을 실행 없이 조회해 Energy Score로 OOD 구간을 감지하고 advantage 기반 재학습을 하는 robot-free human-in-the-loop VLA post-training임. 실로봇 4과제에서 SFT 대비 일관된 개선을 보임. 로봇 배치 없이 interactive post-training을 가능케 한 설계가 실용적임.</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2609.20582'>V2-STRep: VLM-Grounded Structured Task Representations for Reusable Robot Skills Acquired from Generated Videos</a></td><td>56</td><td>7</td><td>VLA</td><td>생성된 비디오의 동작을 VLM으로 points·axes·planes 같은 구조화된 task representation으로 변환해 재사용 가능한 스킬로 만드는 zero-shot 프레임워크임. 실제 6개 조작 과제에서 새 장면 전이와 지시 변경 적응을 모두 보임. 비디오 생성-투-스킬 파이프라인에서 구조를 명시한 점이 참신함.</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2609.20669'>Learning Foresight without Explicit Trajectories for 3D Diffusion Policies</a></td><td>56</td><td>7</td><td>Manipulation</td><td>짧은 관측 이력에서 미래 gripper 상태를 예측하는 compact latent를 학습해 3D diffusion policy에 조건으로만 주는 방법임. 파라미터를 3.52%만 늘리고 LIBERO-40에서 37.08%→71.93%로 크게 개선함. 명시적 경로 없이 foresight를 latent로 제공한다는 아이디어가 단순하면서 효과적임.</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2609.20822'>Coding Agents with an Obstacle-Aware Harness for Safe Robot Manipulation</a></td><td>56</td><td>7</td><td>Manipulation</td><td>coding agent 기반 조작에서 안전 제약이 지켜지지 않는 원인을 route 단계와 contact 단계로 나눠 진단하고 각각 obstacle-aware harness로 보완한 논문임. 성공률 71.9%, 충돌회피 87.5%로 기존 SOTA 대비 각각 2.3배, 1.5배 개선함. LLM coding agent 안전성이라는 문제 자체를 새로 제기한 점이 의미 있음.</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2609.19969'>DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression</a></td><td>56</td><td>1</td><td>LG</td><td>cross-layer KV cache 재사용과 FP4 양자화로 552B MoE 모델의 KV cache footprint를 기존 대비 4분의 1(HBM)·8분의 1(영구저장)로 줄인 산업급 모델임. 토큰당 890바이트라는 구체적 수치와 함께 성능도 baseline보다 좋아 실용적 파급력이 큼.</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2609.20414'>TouchSight: Bare-Handed Tactile Prediction from Egocentric Video via Generative Visual Augmentation</a></td><td>55</td><td>8</td><td>Manipulation</td><td>장갑 착용 촉각 데이터를 generative video로 맨손 영상에 재현해 egocentric vision만으로 dense contact force를 예측하는 연구로 tactile perception 주제와 직접 연결되고 dexterous manipulation에 활용 가능함</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2609.20673'>FunArt: Decoding Functional Structure and Articulation from Generative 3D Latents</a></td><td>55</td><td>8</td><td>Manipulation</td><td>정적 RGB-D 관측만으로 물체의 움직이는 부품과 기능적 요소, 관절 운동을 함께 추정해 물리적 상호작용 전에 로봇 조작 계획에 쓸 수 있는 articulation-aware scene graph를 구성함</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2609.20817'>FAMOS: Feed-Forward 3D Articulation Modeling from Sparse Observations</a></td><td>55</td><td>8</td><td>Manipulation</td><td>sparse한 부분 point cloud만으로 관절 물체의 움직이는 부품과 joint parameter를 feed-forward로 예측해 물리적 상호작용 전 robotic perception 초기화에 쓸 수 있는 연구임</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2609.19666'>Towards High-DoF Dexterous Manipulation through VLA Post-Training</a></td><td>55</td><td>8</td><td>Manipulation</td><td>고자유도 손 동작 codec과 DAgger, residual RL을 결합한 4단계 VLA post-training 파이프라인. 5개 실로봇 태스크에서 각 20회 시행 기준 전부 100% 성공(시행 수가 적어 통계적 여유는 제한적).</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2609.19196'>DITTO: Dexterous Interface for Transparent TeleOperation</a></td><td>55</td><td>7</td><td>Manipulation</td><td>동일 기구학의 외골격과 로봇손을 1:1 매핑해 force feedback 있는 원격조작과 in-the-wild 데이터 수집을 한 플랫폼에서 지원. 데이터 수집의 force-feedback 대 embodiment gap trade-off를 하드웨어 공동설계로 해결한 실용적 기여.</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2609.19228'>Grasping by interconnection: robust closing motions from coarse object templates</a></td><td>55</td><td>7</td><td>Manipulation</td><td>거친 물체 템플릿만으로 컴플라이언트 closing motion을 설계해 피드백 없이도 25/27 조건에서 SOTA 데이터 기반 planner를 능가함. 강건성을 모션 자체에 설계한다는 formulation이 새로움.</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2609.19330'>SemSafe-3DGS: Semantic Risk-Aware Active Navigation in Uncertain 3D Gaussian Splatting Maps</a></td><td>55</td><td>7</td><td>3D Vision</td><td>3D Gaussian map의 semantic 속성으로 class별 위험 가중치를 부여해 CBF 기반 안전 항법과 active perception을 결합. 3DGS·active perception·안전 항법을 잇는 formulation이 우선 주제와 잘 맞음.</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2609.19340'>ViLoMan: Learning Visual-Proprioceptive Whole-Body Loco-Manipulation Skills for Humanoid Robots</a></td><td>55</td><td>7</td><td>Manipulation</td><td>부분적 인간 시연을 물리적으로 실행 가능한 궤적으로 변환한 뒤 teacher-student distillation으로 depth와 proprioception만으로 동작하는 whole-body loco-manipulation 정책을 학습. 실로봇 G1 문닫기로 sim-to-real을 검증함.</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2609.19554'>VABench: Measuring Embodied Spatial Intelligence through Visual Demonstrations, Active Perception, and Metric Control</a></td><td>55</td><td>7</td><td>Embodied AI</td><td>RGB 시연에서 절차를 학습하고 능동적으로 시점을 선택해 metric 명령을 내리는 embodied spatial intelligence 벤치마크. 최고 모델도 3회 평균 성공률 54%에 그쳐 MLLM의 능동 지각·공간 추론 한계를 명확히 드러냄.</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2609.19600'>WorldContact: A Contact-Centric World Model for Scalable Robot Learning</a></td><td>55</td><td>7</td><td>World Model</td><td>제한된 시연으로 구축한 contact-centric world model이 원본 시뮬레이터 대비 10배 빠르게 학습 데이터를 생성. 확장된 데이터로 fine-tuning한 VLA 정책이 실로봇 가방 들기 성공률을 65%에서 95%로 높임.</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2609.19613'>TacSushi: Tactile-Grounded World-Action Modeling for Dexterous Sushi Manipulation</a></td><td>55</td><td>7</td><td>VLA</td><td>손끝 tactile feature를 gated fusion으로 결합하고 미래 시각·접촉 결과를 예측하도록 학습하는 tactile-grounded world-action policy. 초밥 조작 실로봇 실험에서 future-consequence supervision의 기여를 ablation으로 입증함.</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2609.19659'>EmbodiedMind: Adaptive Data Curation and Prefix-Tree Reinforcement Learning for Efficient Embodied Intelligence</a></td><td>55</td><td>7</td><td>Embodied AI</td><td>난이도 기반 curriculum과 action prefix tree 기반 step-level advantage로 long-horizon credit assignment 문제를 완화한 embodied foundation model 학습 파이프라인. 18개 벤치마크 평균 SOTA를 보고함.</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2609.19824'>TADreamer: Zero-Shot Language-Guided 3D Navigation for Terrestrial-Aerial Bimodal Robots via Video Imagination</a></td><td>55</td><td>7</td><td>World Model</td><td>비디오 생성으로 상상한 경로를 실측 geometry에 정합시켜 지상-공중 겸용 로봇을 제로샷 내비게이션하는 프레임워크임. world model과 VLN을 잇는 아이디어이나 실내외 7개 시나리오로 검증 규모는 작음.</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2609.19878'>Uni-LaDiR: Latent Diffusion Unifies Multimodal Reasoning</a></td><td>55</td><td>5</td><td>Multimodal</td><td>여러 modality의 reasoning thought를 공유 latent 공간에서 diffusion으로 생성하는 프레임워크. VLA suite에서 robot manipulation 6.1% 개선을 보고했으나 주 평가는 VLM reasoning benchmark임.</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2609.19688'>LYRIC: Language-Driven Physics-Based Character Control for Contact-Rich Whole-Body Object Interaction</a></td><td>55</td><td>4</td><td>Embodied AI</td><td>language-driven whole-body object interaction을 task planner와 action generator로 분리한 flow-matching 컨트롤러임. OMOMO에서 baseline 대비 큰 성공률 개선을 보였으나 시뮬레이션 캐릭터 대상이라 실로봇 적용은 확인 안 됨.</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2609.19770'>TorchCraft: Unified binder design by inverting an all-atom structure predictor</a></td><td>55</td><td>0</td><td>CV</td><td>AlphaFold3를 역으로 이용해 binder를 설계하는 프레임워크로 실제 wet-lab 결합 실험까지 검증했으나 단백질 설계 문제이고 robotics 무관함</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2609.20078'>FlipToSee: A Probabilistic Stable Placement Prior for Active Visual Exploration via Regrasping</a></td><td>54</td><td>7</td><td>Manipulation</td><td>안정적 배치 방향을 S^2 위 vMF mixture로 표현해 regrasping 기반 능동 시각 탐색을 수행하는 논문임. YCB 제로샷 전이 성공률 90.0%로 active perception/NBV 우선주제에 부합함.</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2609.20114'>Universal Navigation Interface: Robot-Free Data for Wheeled Robot Navigation</a></td><td>54</td><td>7</td><td>Navigation</td><td>로봇 대신 롤레이터 보행기와 스마트폰으로 wheeled-feasible 주행 데이터를 수집하는 robot-free 데이터 수집 패러다임임. 37.2km 실외 데이터로 내비게이션 모델 예측오차를 17.4-24.8% 줄임. 데이터 수집 방식 자체의 참신성이 핵심임.</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2609.20791'>StageGuard: Learning Stage Transitions for Long-Horizon Robot Tasks via Agentic Distillation</a></td><td>54</td><td>7</td><td>Manipulation</td><td>teacher VLM의 추론을 학생 VLM에 distill해 stage transition을 경량으로 판단하는 방법임. BEHAVIOR-1K 통합과 실로봇 검증에서 성능이 개선됨. long-horizon skill chaining의 전환판단을 가볍게 만든 기여가 실용적임.</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2609.19906'>Learning and Transferring Closed-Loop Robot Software</a></td><td>54</td><td>6</td><td>Manipulation</td><td>coding agent가 생성한 policy 코드를 재사용 가능한 소프트웨어 아카이브로 축적해 새 과제에 전이하는 프레임워크임. RoboCasa에서 성공률이 크게 개선됨(28.3%→64.2%). 코드형 정책을 경험으로 재사용한다는 아이디어가 참신함.</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2609.20756'>OPTED: On-Policy Fine-Tuning for End-to-End Driving using a Render-Free Teacher</a></td><td>54</td><td>6</td><td>RL</td><td>3DGS로 재구성한 로그 위에서 privileged teacher를 RL로 학습하고 이를 render-free로 카메라 기반 student에 전달하는 closed-loop post-training 방법임. driving score가 최대 9.5배 개선되고 직접 RL 대비 상호작용을 1000분의 1 수준으로 줄임. RL과 post-training을 분리한 설계가 physical AI 전반에 적용 가능함.</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2609.19291'>Why Pretraining Fails to Share Cross-Lingual Knowledge</a></td><td>54</td><td>0</td><td>NLP</td><td>동일 언어를 서로 다른 토큰공간에 매핑하는 통제실험으로 disjoint token이 cross-lingual 지식전이를 막는 근본원인임을 밝힌 논문임. 공유 토큰공간으로 매핑하면 전이효율의 12.6%p를 회복함을 보여 원인분석이 명확함.</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2609.19542'>PerSeM: Persistent Semantic Memory for Long-Horizon Open-Vocabulary UAV Mapping</a></td><td>50</td><td>7</td><td>Embodied AI</td><td>UAV용 training-free persistent semantic memory로 장기간 일관된 open-vocab mapping을 구현해 robot memory 주제와 직접 맞닿음</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2609.20648'>SkipVLA: Skipping VLA Steps with Classical Planning for Fast Robot Manipulation</a></td><td>50</td><td>7</td><td>VLA</td><td>자유공간 이동은 classical planner에, contact-rich skill만 VLA에 맡기는 하이브리드 정책임. 얼려진 VLM backbone으로 목표 pose를 예측해 추가 시연 없이 학습함. LIBERO와 실기 YAM arm에서 최대 2.5배 빠른 완료를 보이는 효율성 중심 기여임.</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2609.19272'>Learning Safe Humanoid Navigation from Reduced Order Models</a></td><td>50</td><td>6</td><td>Navigation</td><td>축소 차수 모델로 학습한 항법 정책을 full-order humanoid dynamics에 이식하고 Poisson safety filter로 미지 장애물 안전성을 확보. 실로봇 G1에서 10m 수직 이동을 포함한 다층 지형 항법을 검증함.</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2609.20615'>INSPECT: Learning Robot View Selection from Assistant Use</a></td><td>50</td><td>6</td><td>Manipulation</td><td>스마트글래스 어시스턴트 사용기록에서 로봇의 view selection을 학습하는 방법임. presence-invariant paired intervention으로 evidence를 보정해 조립검사 verifiability를 34.8%에서 41.7%로 높임. VLM in-loop 없이 시점을 고르는 active perception 신호 설계가 흥미로움.</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2609.19610'>SIMLIFE: Pattern Understanding for Long-Horizon Human-Agent Partnership</a></td><td>50</td><td>5</td><td>Embodied AI</td><td>가정 내 장기 루틴을 시각·오디오로 시뮬레이션하고 규칙 추론을 평가하는 벤치마크로 embodied agent의 장기 패턴 이해 연구에 직접 닿아있음</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2609.19156'>Reflective Recovery: A Self-Supervised Method for Reasoning by Learning from Mistakes</a></td><td>50</td><td>2</td><td>NLP</td><td>실패한 추론 궤적의 앞부분을 학습데이터로 바꿔 오류 인식·복구 능력을 키우는 self-supervised 방법임. AIME 2025에서 30.0%→37.5%로 개선하고 imitation만으로는 못 넘던 scaling collapse를 깼다고 주장함. 실패에서 복구를 배운다는 아이디어는 로봇의 failure recovery 논의와 통하는 지점이 있음.</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2609.19149'>Subliminal Prompting Beyond Static Geometry: Causal Depth and Multi-Token Confounds</a></td><td>50</td><td>1</td><td>NLP</td><td>subliminal learning의 token entanglement 가설을 output-vector 유사도, readout, causal control로 나눠 각각 독립 측정한 해석가능성 연구임. donor-control로 인과적 개입 효과를 입증했으나(+0.286) 고정 기하학적 유사도는 오히려 예측력이 떨어짐을 보여 메커니즘이 하나가 아님을 시사함.</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2609.19868'>Zarya: A Hybrid Autoregressive--Masked Diffusion Language Model with Flexible Training and Dual-Mode Inference</a></td><td>50</td><td>1</td><td>LG</td><td>autoregressive와 masked diffusion 목적함수를 슬롯 단위 커리큘럼으로 한 아키텍처에 통합한 hybrid LM임. KV cache를 재사용하는 slotted speculative decoding으로 두 패러다임을 하나의 인터페이스로 묶은 점이 구조적으로 참신함.</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2609.20106'>AnyviewMeter: Adapting Robotic Reward Models with Camera Geometry and Multi-View Attention</a></td><td>48</td><td>8</td><td>Manipulation</td><td>카메라 기하와 multi-view attention으로 로봇 reward model을 뷰포인트 변화에 강인하게 적응시켜 실로봇 실험까지 검증한 연구임</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2609.20377'>MM-Future: Multi-Mode Joint World-Action Modeling for Autonomous Driving</a></td><td>48</td><td>6</td><td>World Model</td><td>다중 가설의 scene-action을 diffusion transformer로 co-evolve시키는 world-action model로 자율주행 planning에서 world model과 action을 결합한 시도임</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2609.19200'>ULOHA: An Underwater Bimanual Robot System for Robot Learning</a></td><td>48</td><td>6</td><td>Manipulation</td><td>수중 양팔 로봇 학습 플랫폼을 구축해 ACT·Diffusion Policy·SmolVLA를 평가. 공기 중 기법이 수중에서 겪는 한계를 실증한 새로운 실험 환경을 제공함.</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2609.19449'>Winning a Won Game: Strict Reach-Avoid-Stay Control Barrier Functions for High-Dimensional Black-Box Systems</a></td><td>48</td><td>6</td><td>RL</td><td>reach-avoid-stay를 만족하는 Q-CBF를 black-box 시스템에 일반화하고 사족보행 gap jumping과 F1TENTH 레이싱 실기로 검증. 안전 필터 이론과 실물 검증을 함께 갖춤.</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2609.19460'>Pose-aware Legged Robot Semantic Exploration with Omnidirectional Perception in Confined Unknown Environments</a></td><td>48</td><td>6</td><td>Navigation</td><td>다리 로봇의 자세 자유도를 활용한 omnidirectional 관측과 VLM 기반 viewpoint pruning으로 semantic exploration 효율을 높임. 실로봇 검증을 갖춘 active perception 기여임.</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2609.19588'>Quantifying Mechanical Intelligence in Legged Robots with Information Theory</a></td><td>48</td><td>6</td><td>Embodied AI</td><td>다리 로봇의 body dynamics를 계산·통신 채널로 보고 정보이론 지표로 mechanical intelligence를 정량화. compliance와 저기어비 전달의 trade-off를 이론적으로 규명한 새로운 틀임.</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2609.19850'>GR2PO: Group Relative Return Policy Optimization for Continuous Robot Control</a></td><td>48</td><td>6</td><td>RL</td><td>critic 없이 discounted return을 group-relative로 정규화해 연속제어에 적용한 RL 방법임. GRPO 계열을 continuous control로 확장한 것으로 설계 자체의 새로움은 크지 않음.</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2609.19974'>MaskHarness-WAM: Instance-Grounded Harnessing for Long-Horizon Robot Manipulation</a></td><td>48</td><td>6</td><td>Manipulation</td><td>instance mask로 고수준 계획과 저수준 정책을 연결해 동일 외형 물체의 순서 조작을 다루는 long-horizon 프레임워크임. 실로봇에서 baseline 대비 크게 개선되나 mask 기반 harness 설계는 기존 아이디어의 조합에 가까움.</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2609.20477'>Visual Sim-to-Real Learning for Robotic Insertion under Geometric Variations: Application to Rebar Installation</a></td><td>48</td><td>6</td><td>Manipulation</td><td>1.4mm 공차의 철근 삽입을 위해 특권 상태 teacher를 시뮬레이션에서 강화학습으로 학습하고 멀티뷰 student로 distill하는 sim-to-real 시스템임. 실공장 철근으로 91.3% 성공률을 보이나 단일 과제에 특화된 엔지니어링임.</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2609.20558'>Learning Slope-Adaptive Whole-Body Locomotion for Humanoid Robots in Roofing Construction</a></td><td>48</td><td>6</td><td>Embodied AI</td><td>인간 지붕공사 동작을 로봇에 리타겟팅하고 지붕 모델로 접촉을 grounding한 뒤 RL로 다듬는 휴머노이드 whole-body locomotion 논문임. Unitree G1 실기에서 여러 작업을 재현함. 특정 건설 응용에 특화된 학습 파이프라인임.</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2609.20638'>PROVIA: Procedure State Tracking for Online Mistake Detection in Egocentric Videos</a></td><td>48</td><td>5</td><td>Embodied AI</td><td>egocentric video에서 과거 프레임만으로 실수를 조기에 감지하고 회복 후에도 추적을 유지하는 procedure state tracking으로 failure detection 주제와 개념적으로 맞닿으나 로봇 실행이 아닌 사람 영상에 적용됨</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2609.19480'>Self-excited actuation enables adaptive and resilient flapping-wing flight</a></td><td>48</td><td>5</td><td>Embodied AI</td><td>곤충의 비동기 근육을 모사한 최초의 비행 가능 flapping-wing 로봇. 별도 센싱 없이 충돌에 즉각 반응하는 embodied 제어를 하드웨어로 구현함.</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2609.19589'>Form Over Content In Gradient-Based Data Attribution Methods</a></td><td>48</td><td>0</td><td>NLP</td><td>gradient 기반 data attribution이 task 의미보다 answer format을 더 강하게 따라간다는 것을 독립변인 통제로 입증한 논문임. LESS 같은 실사용 방법의 선택 결과가 포맷에 치우쳐 있음을 보여 해당 분야에 중요한 경고를 줌.</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2609.20191'>VLN on the Fly: An Onboard Vision-Language Navigation Stack for Aerial Robots</a></td><td>46</td><td>7</td><td>Navigation</td><td>grounding-planning-control을 분리된 단계로 유지한 채 항공로봇에 탑재한 온보드 VLN 스택임. 15회 비행 중 13회 목표 도달로 실비행 검증을 했으나 각 모듈은 기존 요소의 통합에 가까움.</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2609.20443'>Spatial-Semantic Uncertainty in VLM-Based Target Search: Balancing Exploration and Identification</a></td><td>46</td><td>7</td><td>Embodied AI</td><td>VLM 기반 target search에서 공간 불확실성과 의미 불확실성을 분리해 각각 정보이득으로 계획하는 논문임. EIG 기반 planner가 랜덤 대비 훨씬 높은 확신 도달률을 보임. 불확실성을 두 축으로 나눈 정식화가 명확함.</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2609.19946'>Execution-Aware Pre-Execution Ranking for Grasp-Conditioned Robotic Placement</a></td><td>46</td><td>6</td><td>Manipulation</td><td>grasp에 따라 달라지는 배치 실행가능성을 사전에 점수화하는 ranking 모델임. 실제 xArm7 전이에서 top-1 성공률이 개선되나 문제 자체는 기존 pipeline에 랭킹 모듈을 추가한 것임.</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2609.20227'>Strategic Transformer for Resource-Constrained Multi-Object Navigation in Ultra-Large-Scale Environments</a></td><td>46</td><td>6</td><td>Navigation</td><td>다중 물체 탐색을 Set Orienteering Problem으로 재정식화하고 경량 transformer로 조합최적화를 근사하는 방법임. ProcTHOR에서 메타휴리스틱 대비 94배 빠르나 문제 재정식화 이상의 개념적 도약은 제한적임.</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2609.20330'>RoboFind: Multi-Agent Personalized Object Search for People Who Are Blind or Have Low Vision</a></td><td>46</td><td>6</td><td>Embodied AI</td><td>스마트폰으로 타깃을 가르치고 사족보행 로봇이 탐색하는 시각장애인 지원 멀티에이전트 시스템임. 완료 전 검증 단계를 둬 false success를 75%에서 5%로 줄임. 응용 중심이나 검증-후-완료 설계가 실용적임.</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2609.20747'>MILER: Semantic Mid-Level Representation for Sim-to-Real Reinforcement Learning in Unstructured Autonomous Driving</a></td><td>46</td><td>5</td><td>RL</td><td>semantic mid-level representation을 시뮬레이터와 실차가 공유하게 해 비정형 자율주행에 정책을 제로샷 전이하는 RL 방법임. 실외 17.3km를 사람 개입 없이 주행함. trajectory-alignment로 인지와 제어를 함께 전이한 설계가 실용적임.</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2609.20480'>Worst-Case Hidden-Vehicle Trajectory Search in Spatiotemporal Occlusion Regions</a></td><td>46</td><td>4</td><td>CV</td><td>backward witness로 인증된 hidden-state mode 위에서 최악의 hidden-vehicle 궤적을 minimax로 탐색하는 occlusion reasoning 방법임. Waymo 8개 시나리오에서 6개의 회피 가능한 반례를 찾아냄. 자율주행 안전성 검증 도메인의 정식화가 견고함.</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2609.19164'>Advantage Scale Calibration Imbalance in Group-Relative Optimization under Low-Variance Rewards: Diagnosis and Bounded Recovery</a></td><td>46</td><td>3</td><td>RL</td><td>group-relative RL에서 advantage scale이 KL calibration에 미치는 영향을 진단하고 MaxNorm-AC로 보정하는 방법론 논문임. GRPO/RLOO 계열의 저분산 보상 문제를 다뤄 continuous robot RL에도 참고할 여지가 있음.</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2609.19877'>JustMem: Just-Enough Memory Access for Long-Term Conversations</a></td><td>46</td><td>2</td><td>NLP</td><td>질의마다 필요한 탐색 폭과 읽기 충실도가 다르다는 관찰로 memory access를 LOOKUP·COMPOSE·REPLAY로 나눈 장기대화 메모리 시스템임. 정확도와 회수율에서 최고 성능을 더 적은 토큰으로 달성함. 로봇 메모리 설계에도 참고할 만한 access 축 분리 아이디어임.</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2609.20252'>Lens: Bringing the Right Semantic Perspective into Focus for Training-Free Multimodal Representation Learning</a></td><td>46</td><td>2</td><td>Multimodal</td><td>readout에 쓰는 phrase를 과제 관점에 맞게 anchoring해 파라미터 학습 없이 멀티모달 표현을 뽑아내는 방법임. MMEB 36개 데이터셋에서 같은 backbone의 training-free baseline을 10.2점 앞섬. representation learning 우선주제에 해당하는 실용적 기여임.</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2609.20235'>Scene-Q: Confidence-Aware Coarse-to-Fine Querying of 3D Scenes with Selective VLM Reasoning</a></td><td>45</td><td>7</td><td>Embodied AI</td><td>실내 로봇의 open-vocab 3D scene query에서 confidence 기반으로 VLM reasoning을 선택적으로 호출해 정확도와 효율을 함께 높인 embodied perception 연구임</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2609.19881'>BinoGen: Scaling egocentric binocular data for embodied visual perception and learning</a></td><td>45</td><td>6</td><td>Embodied AI</td><td>embodiment 조건(시야각·양안 기하)을 반영한 대규모 egocentric binocular 데이터 생성 프레임워크로 embodied perception 학습에 직접 기여함</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2609.19414'>Improving Offline Goal-Conditioned Reinforcement Learning via Selective Reward Stimulation</a></td><td>45</td><td>6</td><td>RL</td><td>offline goal-conditioned RL에서 진행 상태에 보조 reward를 주입해 희소 보상 문제를 완화하는 non-hierarchical 방법으로 RL 주제와 직접 관련 있음</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2609.19378'>Task-Oriented Active Learning of Residual Dynamics for Model Predictive Path Integral Control</a></td><td>45</td><td>6</td><td>RL</td><td>MPPI rollout에서 이후 상태 불확실성 감소량을 태스크 관련성으로 가중해 GP residual dynamics를 능동적으로 학습. 오프로드 내비게이션에서 passive 학습 대비 19~27%p 성공률 개선을 보임.</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2609.19510'>PIVOT: Perception-aware Independent Viewpoint Online Optimization</a></td><td>45</td><td>6</td><td>Navigation</td><td>gimbal 등 motion-decoupled 센서의 시야 방향을 좌표계 특이점 없는 SO(3) 최적화로 실시간 선택. brute-force 대비 76~85배 가속과 실로봇 검증을 갖춘 active perception 기여임.</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2609.19661'>ReShoot: Generative Visual Domain Randomization of Recorded Robot Demonstrations for Visuomotor Policy Learning</a></td><td>45</td><td>6</td><td>Manipulation</td><td>기록된 시연을 VLM 캡션과 edge-conditioned 비디오 생성으로 외형만 바꿔 재렌더링해 시각 다양성을 합성. action label을 그대로 재사용해 LIBERO와 실로봇 모두에서 robustness 개선을 보임.</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2609.20819'>Can 4D Foundation Models Remember?</a></td><td>45</td><td>5</td><td>World Model</td><td>4D foundation model들이 시야를 벗어난 물체를 다시 봤을 때 정합성을 유지하는지 측정하는 PersistBench를 제안해 현재 모델들의 시각적 기억 한계를 드러낸 world model 평가 연구임</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2609.19358'>Open-vocabulary 3D object detection with promptable segmentation</a></td><td>45</td><td>4</td><td>3D Vision</td><td>SAM3 기반 training-free open-vocab 3D detection으로 LiDAR 대비 3D geometry 격차를 정밀하게 분석했으나 자율주행 perception 범위에 머무름</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2609.20012'>GRF-Recon: Global Ray-Field Optimization for Long-Sequence Feed-forward Reconstruction</a></td><td>45</td><td>4</td><td>3D Vision</td><td>긴 monocular 시퀀스에서 global ray-field 최적화로 누적 drift를 줄인 feed-forward reconstruction 방법으로 robot mapping에 활용 가능한 SLAM 대안임</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2609.19636'>Reach or Solve? Attributing Agentic RL Gains with Checkpoint Handoffs</a></td><td>45</td><td>3</td><td>RL</td><td>RL로 학습된 정책의 성능 향상이 도달 능력과 해결 능력 중 어디서 오는지 checkpoint handoff로 분리한 평가 방법론이며 ALFWorld 등 embodied 벤치마크에 적용 가능해 방법론적으로 흥미로움</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2609.19729'>Recency Forcing: Bridging the Long-Horizon Gap in Autoregressive Video Generation</a></td><td>45</td><td>2</td><td>Video</td><td>AR 비디오 생성의 KV eviction mismatch를 규명하고 zero-overhead attention bias로 long-horizon 생성을 개선한 분석이 탄탄함</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2609.19465'>Compositional Reasoning in Language Models under Reinforcement Learning Post-Training</a></td><td>45</td><td>1</td><td>RL</td><td>RL post-training이 decomposed에서 composed로는 전이 안 되고 반대 방향은 전이된다는 비대칭성을 데이터구조 태스크로 규명했으며 skill 조합 일반화 논의에 참고할 만함</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2609.19644'>ScientistTwo: Pioneering the Human Knowledge Frontier with Autonomous AI</a></td><td>45</td><td>0</td><td>AI</td><td>문제 제시만으로 가설 수립부터 논문 작성까지 자동화하는 AI 과학자 프레임워크로 top-tier 논문 벤치마크에서 사람보다 높은 리뷰 점수를 받았다고 주장하나 자동 리뷰 기준의 신뢰성이 불확실함</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2609.20620'>A Simulation Platform for AUV Fault Recovery: Exploring LLM-Based Diagnostic Strategies</a></td><td>44</td><td>7</td><td>Embodied AI</td><td>AUV 결함 진단·복구를 LLM에 맡기는 시뮬레이션 플랫폼과 앙상블 평가방법론임. frontier 모델이 로컬 모델보다 원인 진단을 훨씬 잘 찾아냄(85-90% vs 60-78%). 새 방법이라기보다 평가 인프라 논문임.</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2609.19923'>Co-VLA: Consensus-based Federated Training for Vision-Language-Action Models</a></td><td>44</td><td>6</td><td>VLA</td><td>federated learning으로 이기종 로봇 데이터를 중앙집중 없이 VLA에 학습시키는 방법임. ADMM consensus 적용이 새롭지만 성능은 중앙집중 학습과 비슷한 수준에 그침.</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2609.19962'>Hybrid Residual Reinforcement Learning for Contact-Rich Robotic Book Insertion</a></td><td>44</td><td>6</td><td>Manipulation</td><td>known geometry 기반 nominal controller에 residual PPO를 결합해 책 삽입 같은 contact-rich task를 다루는 논문임. 실기 xArm7 성공률이 26.7%에서 63.3%로 개선됐으나 단일 태스크에 특화된 엔지니어링임.</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2609.20407'>Resilient Motion Planning for Free-Flying Space Robots under Actuator Failures</a></td><td>44</td><td>6</td><td>Navigation</td><td>actuator failure를 Markov chain으로 모델링해 목표도달 확률을 최대화하는 free-flyer 모션플래닝임. 실제 하드웨어로 검증했으나 우주로봇이라는 좁은 도메인에 한정됨.</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2609.20566'>OmniMimic: Dynamics-completed Motion Augmentation for Multi-style Omnidirectional Quadruped Locomotion</a></td><td>44</td><td>6</td><td>RL</td><td>방향이 제한된 동물 시연을 시간역전·동역학보완으로 증강해 전방향 사족보행 정책을 학습하는 방법임. 시뮬레이션에서 속도추종 오차를 63.1% 줄이나 실로봇 검증은 없음.</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2609.19803'>HEROIC: Heterogeneous Evidential Reasoning for Open-Vocabulary Identification and Cross-Robot Collaboration</a></td><td>44</td><td>5</td><td>Embodied AI</td><td>공중-지상 이기종 로봇 팀의 자연어 기반 역할 재할당과 evidential belief 융합 탐색 시스템임. 실험 성공률이 높으나(84% vs 35-54%) 방법 자체는 엔지니어링 통합에 가까움.</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2609.20629'>RTK-Vision PPO for Autonomous Micro UAV Recovery on an Airborne Carrier</a></td><td>44</td><td>5</td><td>RL</td><td>RTK와 비전을 결합한 PPO로 소형 UAV의 공중 모선 회수를 수행하는 RL 논문임. PD baseline 대비 성공률이 크게 개선(99.55% vs 78.4%)되고 실외 14회 중 13회 성공함. 특정 임무에 특화된 엔지니어링 성격이 강함.</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2609.19799'>Evolution or Illusion? Rethinking Evaluation in LLM Evolutionary Search</a></td><td>44</td><td>1</td><td>NLP</td><td>LLM 진화탐색을 한 예산점에서만 평가하는 관행을 비판하고 seed와 iteration의 전체 격자를 스캔해야 순위가 바뀜을 보인 방법론 논문임. 진화적 코드탐색을 쓰는 로봇 보상·코드 설계 연구에도 참고할 방법론적 시사점이 있음.</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2609.19154'>Neo-Classic: A Benchmark for Evaluating Linguistic-Aesthetic Reasoning in Classical Chinese Poetry</a></td><td>44</td><td>0</td><td>NLP</td><td>현대 창작 고전시가로 LLM의 linguistic-aesthetic reasoning을 평가하는 벤치마크임. 역사 텍스트에서 현대 텍스트로 옮기면 정확도가 20-50%p 떨어짐을 보여 기존 벤치마크의 암기 의존성을 드러냄.</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2609.19504'>For Your Eyes Only: Evaluating Coordination Between Isolated Language Model Instances</a></td><td>44</td><td>0</td><td>NLP</td><td>공유 메모리 없이 같은 모델 인스턴스끼리 자연어로 은밀한 신호를 주고받을 수 있는지 평가하는 게임임. 일부 frontier 모델이 필터링 후에도 근완벽한 조정 능력을 유지해 스테가노그래피 위험을 시사함.</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2609.19452'>GLAMDRING: Gait Learning And Morphology co-Design via Reinforcement LearnING of CPGs</a></td><td>42</td><td>6</td><td>RL</td><td>형상과 CPG gait controller를 함께 최적화해 speed·CoT·payload 목적별 사족보행 로봇을 합성. 실물 시연을 갖춘 body-gait co-design 프레임워크임.</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2609.19541'>Navigate or Relocate? Planning Among Movable Obstacles in Unknown Environments</a></td><td>42</td><td>6</td><td>Manipulation</td><td>미지 환경에서 발견한 이동 가능 장애물에 대해 navigate와 relocate를 온라인으로 선택하고 LLM으로 샘플링을 편향시키는 NAMO 기법. TAMP 관련 주제와 맞으나 수치 시뮬레이션 중심 검증임.</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2609.19579'>Recovering Aggressively Pruned Vision-Language-Action Models with Offline Hidden-State Distillation</a></td><td>42</td><td>6</td><td>VLA</td><td>폭 pruning된 VLA의 hidden state를 teacher와 직접 맞추는 offline distillation으로 RL 없이 성능을 대부분 회복. 63% 압축에서 teacher와 3.5점 차, 실로봇 속도·메모리 개선까지 검증함.</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2609.20624'>SmellDiffusion: Diffusion-Based Quadruped Navigation with Olfactory Scene Graphs</a></td><td>42</td><td>6</td><td>Navigation</td><td>gas identity를 보존하며 소스를 추정하고 diffusion planner로 유도하는 후각 기반 사족보행 내비게이션임. gated correction으로 변위 오차를 60% 줄이나 diffusion planner의 실질 이득은 A*와 비슷한 수준임.</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2609.19518'>AMB3R-SLAM: Kilometer-scale SLAM with Hierarchical Backend</a></td><td>42</td><td>5</td><td>3D Vision</td><td>킬로미터급 monocular SLAM으로 동적 장면 처리와 LiDAR 확장성을 보였고 robot navigation backend로 활용 가능함</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2609.19662'>Towards Active Cross-View Object Geo-Localization</a></td><td>42</td><td>5</td><td>Embodied AI</td><td>cross-view object geo-localization에 능동적 viewpoint 선택을 도입해 active perception 주제와 연결되나 응용 범위가 제한적임</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2609.19204'>REACT: A Fully Spiking State-Space Model for Real-Time Event-Driven Temporal Perception</a></td><td>42</td><td>5</td><td>Embodied AI</td><td>이벤트를 누적하지 않고 spiking state-space model로 개별 처리해 4.6ms 지연의 충돌시간 추정을 달성. 저지연 반응형 지각이라는 점에서 로봇 perception에 실질적 기여를 함.</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2609.20605'>Bayesian Continuum Robot Dynamics and State Estimation</a></td><td>42</td><td>5</td><td>Robotics</td><td>Cosserat rod 동역학을 factor graph로 근사해 continuum robot의 동적 상태추정을 다루는 논문임. quasi-static 가정을 넘어 관성효과를 포함한 점이 방법론적으로 의미 있으나 적용 로봇 범위가 좁음.</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2609.20103'>Safety-Critical Scenanrio Emerges from Initial Scene</a></td><td>42</td><td>4</td><td>CV</td><td>surrounding agent 조작 대신 초기 장면 생성을 안전-critical 시나리오 문제로 재정의한 diffusion 기반 방법임. 초기화 문제로 재구성한 관점은 새롭지만 자율주행 시뮬레이션 도메인에 한정됨.</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2609.19421'>RGS: Reflection-aware Gaussian Splatting via Learning Geometry Continuity for Reflective Objects</a></td><td>42</td><td>3</td><td>3D Vision</td><td>반사 표면에서 3DGS 표면 붕괴를 3D foundation model prior로 완화한 연구로 object-centric 3D representation과 닿아있으나 novelty는 제한적임</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2609.20784'>RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning</a></td><td>42</td><td>3</td><td>RL</td><td>teacher를 적응적으로 은퇴시키는 self-distillation으로 ALFWorld·WebShop에서 RL 대비 큰 폭 개선했고 long-horizon agent 학습에 참고할 만함</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2609.19596'>Full-Duplex Speech Models Take the Floor When Asked, Not When Needed</a></td><td>42</td><td>1</td><td>NLP</td><td>full-duplex speech model이 허위정보나 위험상황보다 지목되었을 때나 침묵 후에만 주로 말을 꺼낸다는 것을 통제된 실험으로 보인 논문임. 능동적 개입 능력의 공백을 정량적으로 드러냄.</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2609.19880'>D-Quant: Driftable Entropy Coding for KV Cache Quantization</a></td><td>42</td><td>1</td><td>LG</td><td>KV cache의 비균일 분포를 엔트로피 코딩으로 압축하되 drift 메커니즘으로 고정길이 비트스트림을 만들어 병렬 attention 커널과 호환시킨 논문임. 추론 효율화 기여로 기술적으로 탄탄함.</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2609.19155'>Towards Proactive Detection of User-Side Implicit Conflicts in Human-LLM Dialogue</a></td><td>42</td><td>0</td><td>NLP</td><td>이전 발화와 암묵적으로 충돌하는 사용자 의도를 선제적으로 탐지하는 벤치마크와 제약공간 기반 합성법을 제안함. 소형 모델이 대형 범용 LLM을 능가함을 보였으나 문제 자체는 좁은 범위임.</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2609.20081'>Reading Emotions in the Token Space: Discriminative Adaptation of SpeechLLMs for Emotion Recognition</a></td><td>42</td><td>0</td><td>Multimodal</td><td>SpeechLLM의 generative decoder 대신 마지막 hidden state에 분류헤드를 다는 discriminative adaptation으로 감정인식의 hallucination을 없앤 논문임. 구조는 단순하나 해석가능성까지 확보한 점이 깔끔함.</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2609.20186'>To Copy or Not to Copy: Controlling Speculative Decoding via Intrinsic Model Signals</a></td><td>42</td><td>0</td><td>NLP</td><td>n-gram 중복이 실제 복사 의도를 반영 못 해 생기는 speculative decoding의 오탐을 내부 표현으로 학습한 probe(AUC&gt;0.99)로 걸러내는 방법임. neural drafting과 copy 전략을 상황에 맞게 전환해 처리량을 최대 15% 높임.</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2609.20475'>SenseFuse: Label-Free Fusion of Image and Shape Encoders for Open-Vocabulary 3D Instance Segmentation</a></td><td>40</td><td>6</td><td>3D Vision</td><td>2D 이미지와 3D shape encoder를 label-free로 결합해 open-vocab 3D instance segmentation을 개선한 연구로 로봇 scene understanding에 활용 가능함</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2609.19441'>Predict Before You Deploy: Offline Prediction of Quantization-Induced Task Degradation for World Action Models</a></td><td>40</td><td>6</td><td>VLA</td><td>closed-loop 평가 없이 offline action 편차만으로 world action model의 양자화 성능 저하를 예측하는 보정 프레임워크. Franka 로봇 450회 시행으로 검증한 실용적 배포 도구임.</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2609.19665'>Runtime Safety Filtering for Two-Terminal Hazards in Robotic Battery Recycling</a></td><td>40</td><td>6</td><td>Manipulation</td><td>두 단자가 동시에 접촉해야 발생하는 위험에 대해 predicate 구조와 fallback 전략을 분리 비교. predicate 구조보다 fallback 전략(retreat)이 안전-성능 trade-off를 더 크게 좌우함을 규명함.</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2609.20348'>EliGSiR: Continual RGB-D Mapping with Gaussian Splatting under Bounded Compute</a></td><td>40</td><td>5</td><td>3D Vision</td><td>제한된 연산 예산 하에서 online RGB-D Gaussian mapping을 지속적으로 수행하는 연구로 robot mapping에 활용 가능한 시스템 기여임</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2609.20589'>RawSLAM: Online HDR Gaussian SLAM from Linear Radiance</a></td><td>40</td><td>5</td><td>3D Vision</td><td>16비트 선형 HDR 영상에서 직접 동작하는 최초의 online Gaussian SLAM으로 극한 조명에서 기존 시스템의 tracking 실패를 제거해 robot 환경 강건성에 기여함</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2609.19328'>A Morphing Aerial Robot With Thruster-Integrated Flexible Continuum Links for Shape Adaptive Aerial Manipulation</a></td><td>40</td><td>5</td><td>Manipulation</td><td>추진기를 분산 배치한 연속체 링크로 형상 적응과 wrench space 확장을 동시에 달성한 비행 로봇. IROS 채택된 하드웨어 설계 기여임.</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2609.20035'>DR-MPC: Fast and Feasible Dynamics-Relaxed Model-Predictive Control for Legged Locomotion</a></td><td>40</td><td>5</td><td>Control</td><td>legged locomotion용 MPC를 동역학 제약을 이차페널티로 완화해 빠르게 푸는 solver 논문임. HPIPM 대비 16배 속도 향상을 보였으나 로봇러닝보다 최적화 솔버 기여에 가까움.</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2609.20694'>HOPHY: A Hierarchical Hypergraph Representation for Off-Road Path and Mission Planning</a></td><td>40</td><td>5</td><td>Navigation</td><td>off-road 지형을 계층적 hypergraph로 표현해 킬로미터급 반복 경로계획을 빠르게 갱신하는 방법임. pixel A* 대비 계산량을 79배 줄이고 실제 Jackal로 1.5km 임무를 완수함. 학습기반은 아니고 지형표현 자료구조 기여임.</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2609.19961'>Neuro-Symbolic Agentic AI for Networked Low-Altitude UAVs</a></td><td>40</td><td>5</td><td>Embodied AI</td><td>신경-기호 결합으로 UAV의 스킬 재사용과 근거 기반 의사결정을 지원하는 레퍼런스 아키텍처이며 화재 점검 케이스로 개념을 보였으나 정량 실험은 약함</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2609.19815'>SnapPhysics: A Physics-Aware Scene Graph from a Single View for Interactive Mixed Reality Scenes</a></td><td>40</td><td>4</td><td>3D Vision</td><td>단일 이미지에서 질량·마찰 등 물리 속성을 scene graph로 추정하는 training-free 방법으로 embodied physical reasoning에 활용 가능함</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2609.20323'>NeuSOGA3D: A Neuro-Symbolic Framework for Explainable 3D Geometric Reconstruction</a></td><td>40</td><td>3</td><td>3D Vision</td><td>포인트클라우드를 직교 평면에 투영해 symbolic spline으로 CAD 호환 3D 표상을 만드는 neuro-symbolic 재구성 방법으로 ModelNet40에서 검증했으며 object-centric 3D representation과 결이 닿아있으나 CAD 도메인 중심임</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2609.20634'>PAA: The Probabilistic Allen Algebra: A Generative and Complete Probabilistic Extension of Allen&#x27;s Interval Relations</a></td><td>40</td><td>3</td><td>AI</td><td>Allen의 구간 관계를 경계 불확실성 위에서 확률적으로 재구성한 이론으로 시간 추론 도구로 쓸 만하나 robotics 실험은 없음</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2609.19167'>To Memories and Beyond: From Remembering to Knowing You across Long-Term Multimodal Personal Archives</a></td><td>40</td><td>1</td><td>Multimodal</td><td>다년간 실제 개인 사진·기록을 쓴 장기 멀티모달 개인화 메모리 벤치마크임. predictive personalization이라는 새 평가축을 추가했으나 로봇 메모리와는 응용 영역이 다름.</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2609.19883'>PetriBench: Benchmarking LLM Reasoning over Dynamic State Spaces</a></td><td>40</td><td>1</td><td>NLP</td><td>Petri net을 이용해 동적 상태공간 추론을 평가하는 자기완결적 벤치마크임. 구조 복잡도에 따라 정확도가 매끄럽게 감소함을 보여 확장성 있는 평가체계를 제공함.</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2609.19150'>Sampling Reveals Style: Unsupervised, Training-Free Discovery of Prompt-Conditional Stylistic Axes in LLM Activations</a></td><td>40</td><td>0</td><td>NLP</td><td>단일 prompt를 고온 샘플링해 pooled activation에 PCA를 적용, 학습 없이 스타일 축을 찾는 방법임. 사람이 뽑은 스타일 차원과 72.8% precision으로 일치하나 모델별 편차가 커 일반화는 제한적임.</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2609.19158'>VisKG-LM: Compiling Knowledge Graphs into Visual Memory for Multiple-Choice Question Answering</a></td><td>40</td><td>0</td><td>Multimodal</td><td>검색된 지식그래프 서브그래프를 오프라인에 한 번 이미지로 렌더링해 캐싱하는 visual memory 방법임. GreaseLM 대비 QA에서 개선을 보이나 textualization만으로 설명 안 되는 이득의 근거가 약함.</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2609.19366'>The Role of Fine-grained Harm Signals in LLM Safety</a></td><td>40</td><td>0</td><td>NLP</td><td>카테고리별 harmfulness residual을 일반 harm 표현에서 분리해 안전거부에 미치는 영향을 분석한 해석가능성 연구임. 카테고리마다 거부 유도 패턴이 다르다는 결과는 흥미로우나 실무적 파급은 제한적임.</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2609.19417'>Less Is More: Graph-free Multimodal RAG via Multi-signal Late Fusion</a></td><td>40</td><td>0</td><td>Multimodal</td><td>그래프 없이 질문·이미지·VLM 쿼리 세 신호를 late fusion하는 멀티모달 RAG 방법임. 그래프 기반 대비 비용을 줄이면서 성능을 유지하고 웹 이미지 기반 AutoQA 벤치마크를 함께 제시함.</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2609.19778'>Learn Before You Judge: Progressive Knowledge-to-Decision Alignment for Explainable Hateful Meme Detection</a></td><td>40</td><td>0</td><td>Multimodal</td><td>설명 생성과 라벨 예측을 한 번에 학습하면 서로 방해한다는 점을 발견하고 지식학습-탐지학습-경계정렬 3단계로 분리한 hateful meme 탐지 논문임. 여러 벤치마크에서 SOTA를 달성함.</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2609.19942'>Intrinsic Sequence-Likelihood Confidence in Retrieval-Dominated Extractive QA: Two Pre-Specified Negatives, and What They Do and Do Not Attribute</a></td><td>40</td><td>0</td><td>NLP</td><td>검색이 이미 92-99.8%를 회수하는 세팅에서는 LLM confidence 기반 distillation·routing이 실질적 이득이 없음을 사전등록 실험으로 보인 논문임. confidence 신호를 과신하지 말라는 실무적 경고가 핵심임.</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2609.20581'>Limits of Confidence in Diffusion</a></td><td>40</td><td>0</td><td>LG</td><td>discrete diffusion에서 confidence 기반 위치 선택이 의존성 있는 토큰 그룹을 못 맞춘다는 것을 이론과 합성 태스크로 증명한 연구로 generative model 원리 분석이지만 robotics 적용은 없음</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2609.19512'>CoreSense: Traceable Failure Recall and Conflict-Aware Belief Gating for Auditable Robot Decisions</a></td><td>38</td><td>6</td><td>Embodied AI</td><td>과거 실패 사례의 유효성을 scope·시간·모순으로 검증한 뒤 진행 여부를 게이팅하는 아키텍처. failure recall과 robot memory 주제와 맞으나 물리 로봇을 직접 구동하지 않고 평가 결과도 태스크별로 혼재됨.</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2609.19911'>CitySTAR: Structured and Topology-Aware Reasoning for Open-Vocabulary Urban 3D Grounding</a></td><td>38</td><td>4</td><td>3D Vision</td><td>도시 규모 3D grounding을 구조화된 제약 추론으로 재정의하고 scene graph와 topology 검증을 결합했으나 도시 스케일 응용에 국한됨</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2609.19801'>DeliveryGym: An RL Environment for Long-Horizon Embodied Agent Planning with Adaptive Curriculum</a></td><td>38</td><td>3</td><td>Embodied AI</td><td>배달 기사 시뮬레이션 환경에서 long-horizon embodied agent를 RL로 학습시킴. embodied planning과 연결되나 물리 로봇이 아닌 게임형 환경이고 기여도 curriculum 기법에 한정됨.</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2609.19690'>UniExo: Unified Multi-Skill Policies for Musculoskeletal Locomotion and Co-Adaptive Exoskeleton Control</a></td><td>38</td><td>3</td><td>RL</td><td>멀티스킬 human policy로 exoskeleton을 co-adaptation시키는 프레임워크임. 응용은 참신하나 로봇러닝 우선순위 주제와는 거리가 있음.</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2609.19153'>Stop Removing Stopwords: How an Inherited Preprocessing Default Distorts Legal Text-as-Data</a></td><td>38</td><td>0</td><td>NLP</td><td>법률 텍스트 분석에서 불용어 제거라는 관행적 전처리가 성능에 도움이 안 됨을 exhaustive ablation으로 보인 논문임. 최적화된 불용어 목록조차 제거 안 함과 통계적으로 구분 안 된다는 결과가 실무적으로 유용함.</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2609.19606'>Chain-of-Thought Entropy as a Reliability Signal: A Preregistered Reproduction</a></td><td>38</td><td>0</td><td>NLP</td><td>chain-of-thought entropy의 모양이 정답 여부를 예측한다는 기존 결과를 사전등록 재현한 연구임. 모양 신호는 재현되지만 크기 신호는 설정에 따라 갈려 원 논문의 일반화 범위를 좁힘.</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2609.19827'>F$^{2}$DR: A Fine-Grained Full-Pipeline Reward Framework for DeepSearch Workflows</a></td><td>38</td><td>0</td><td>NLP</td><td>DeepSearch 워크플로우를 content·trajectory·answer 세 축으로 평가하는 fine-grained reward 프레임워크와 전용 벤치마크임. 기존 self-evaluation 기반보다 일관성이 높음.</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2609.19885'>Evaluating Communicative Success in Machine-Translated Conversation</a></td><td>38</td><td>0</td><td>NLP</td><td>번역 충실도가 아니라 의사소통 성공 여부를 semantic·pragmatic·cultural 3층 체크리스트로 평가하는 통역 에이전트 벤치마크임. 기존 MT 지표가 놓치는 실패를 잡아냄.</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2609.19887'>Generalization through Lexical Abstraction in Transformer Models: The Case of Functional Words</a></td><td>38</td><td>0</td><td>NLP</td><td>기능어(대명사 등)가 명사와 다른 임베딩 부분공간에 있다는 것을 병렬문장 실험으로 보인 해석가능성 연구임. lexicalized와 functional 문장을 섞어 학습해야 공유구조가 드러난다는 결과가 흥미로움.</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2609.19965'>Before the Arrest: Benchmarking LLMs on Criminal Profiling from Incomplete Evidence</a></td><td>38</td><td>0</td><td>NLP</td><td>용의자 미확정 상태의 불완전한 증거에서 범죄 프로파일링을 시키는 벤치마크임. 사실추출에서 암묵추론으로 갈수록 성능이 급격히 떨어지고 성별·연령 편향도 드러남.</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2609.20207'>Foundations of Stochastic Lexical Calculus: Semantic Descent and Random Dynamics on Probability Simplices</a></td><td>38</td><td>0</td><td>NLP</td><td>LLM의 prompt-조건부 확률에서 순차적 semantic state가 언제 성립하는지를 관측가능성 조건으로 정의한 이론 논문임. 수학적으로는 탄탄하나 실증 검증은 제한된 도메인에 그침.</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2609.20412'>Stress-testing Alignment Midtraining</a></td><td>38</td><td>0</td><td>NLP</td><td>alignment midtraining 효과를 110B 규모까지 체계적으로 검증하고 한계를 지적했으나 robotics 연관성 없음</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2609.19170'>Regularized Emphatic Temporal-Difference Learning: Stability under Constant Stepsizes</a></td><td>38</td><td>0</td><td>RL</td><td>off-policy TD의 constant stepsize 불안정성을 규명하고 RETD로 보정한 RL 이론 연구이나 robotics 적용은 없음</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2609.20116'>GPT-6-Astra in a Navigation Workflow: Behavioral Analysis in Zero-Shot Vision-and-Language Navigation in Continuous Environments</a></td><td>36</td><td>6</td><td>Navigation</td><td>GPT-6-Astra를 zero-shot VLN-CE 워크플로우에 붙여 행동을 분석한 논문임. 새로운 방법 제안 없이 프론티어 모델의 실패 양상을 분석하는 수준임.</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2609.19334'>A frontend-backend architecture for tool calls in full-duplex speech models</a></td><td>36</td><td>0</td><td>NLP</td><td>duplex speech 프론트엔드가 delegation token으로 텍스트 backend LLM에 tool call을 위임하는 아키텍처임. turn-taking을 유지하며 tool-call recall 92-97%를 달성한 시스템 논문임.</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2609.19475'>FASA: Feedback-Aware Sampling Adaptation for Efficient Diffusion-Based VLA Models</a></td><td>35</td><td>6</td><td>VLA</td><td>시각·grip force 피드백으로 diffusion VLA의 denoising step 수를 실시간 조정하는 training-free 프레임워크. 효율화 위주 기여로 새로운 학습 원리는 제한적임.</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2609.19582'>OmniCalib: Target-Free, Task-Structured Self-Calibration for Humanoid Robots</a></td><td>35</td><td>5</td><td>Embodied AI</td><td>타겟 없이 로봇 고유 동작만으로 휴머노이드 상하지·카메라 외부파라미터를 전부 보정. 실제 오프셋 주입 실험으로 정확도를 검증한 실용적 캘리브레이션 기법임.</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2609.20268'>Improving Online Reinforcement Learning via Bidirectional Behavior Prior Distillation</a></td><td>35</td><td>3</td><td>RL</td><td>CVAE로 고가치 행동 support set을 생성해 online RL 샘플 효율을 높이는 기법. pixel-based task까지 검증했으나 offline 사전학습 데이터 질에 의존함.</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2609.20818'>SplashSplat: Reconstructing Splashing Liquids from Real-World Multi-View Videos</a></td><td>35</td><td>2</td><td>3D Vision</td><td>실제 다중뷰 영상에서 물보라를 SDF와 Lagrangian carrier로 물리적으로 재구성하는 연구로 novelty는 있으나 로봇 적용은 없음</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2609.20302'>SAGG: Sample-Adaptive Gradient Gating for Robust Multimodal Learning under Heterogeneous Corruption</a></td><td>35</td><td>2</td><td>Multimodal</td><td>손상 패턴이 sample마다 다른 상황에서 gradient gating으로 멀티모달 학습을 강건화. unbiased 증명과 video 벤치마크 실험을 갖춤.</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2609.20715'>Don&#x27;t Mask the Environment: Observation Supervision Changes How Agents Explore Under RL</a></td><td>35</td><td>2</td><td>RL</td><td>관측 토큰까지 예측하도록 SFT를 확장하면 이후 GRPO 탐색이 개선됨을 보임. 코드·터미널 에이전트 벤치마크 중심으로 물리 로봇 실험은 없으나 action consequence 예측이라는 world-model적 아이디어는 참고할 만함.</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2609.19519'>An Architecture for Long-Horizon Agents: Levels, Ticks and Cascaded Intelligence</a></td><td>35</td><td>2</td><td>AI</td><td>수일짜리 장기 과제를 위한 계층적 harness 아키텍처를 10일 캠페인으로 검증했으며 robot memory와 맥락은 닿지만 물리 로봇 적용은 없음</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2609.19830'>Dual-Axis Policy Optimization for LLM Agents: Bayesian Feedback Attribution and Trajectory Mass Normalization</a></td><td>35</td><td>2</td><td>RL</td><td>RL 에이전트 학습의 attribution과 trajectory 정규화를 분리해 개선한 연구로 ALFWorld 등에서 실험했으나 알고리즘 튜닝 수준의 기여임</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2609.19212'>What Do Current Systematic Generalization Tasks Miss? A Reasoning-Centered Analysis</a></td><td>35</td><td>1</td><td>AI</td><td>deductive·inductive·abductive 추론을 함께 요구하는 systematic generalization 테스트베드로 기존 벤치마크의 허점을 잘 짚었으나 robotics 적용 논의는 없음</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2609.20179'>Sequential Contextual Fit Predicts Human Behavioural and Neural Dynamics Across Domains</a></td><td>35</td><td>1</td><td>CV</td><td>문맥 적합도라는 단일 지표로 언어·음악·도박·EEG 등 여러 도메인의 처리시간·신경반응 변화를 설명한 인지과학 연구로 흥미로우나 robotics 적용은 없음</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2609.19230'>Open ultrasound foundation model for robust segmentation and clinical measurement across heterogeneous settings</a></td><td>35</td><td>0</td><td>CV</td><td>초음파 segmentation foundation model로 novelty는 데이터 스케일과 일반화 검증에 있으나 로봇과 무관함</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2609.20408'>Xeno-Interpretability: Investigating the Alien Minds of LLMs</a></td><td>35</td><td>0</td><td>NLP</td><td>LLM 내부에 인간이 이름 붙이지 못한 표상이 있을 수 있다는 개념 제안이며 실증 없는 포지션 성격이 강함</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2609.20612'>What Does Privileged Information Add to On-Policy Self-Distillation?</a></td><td>35</td><td>0</td><td>RL</td><td>on-policy self-distillation에서 privileged reference의 기여를 분리 분석한 수학 추론 연구로 robotics 무관함</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2609.20734'>On-Demand Attention: Language Models Know When to Recall</a></td><td>35</td><td>0</td><td>LG</td><td>긴 컨텍스트에서 recall head로 global attention을 선택 호출해 속도를 높인 효율화 연구이며 robotics 적용 논의는 없음</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2609.19759'>Rethinking Multi-Agent Collaboration: When More Is Less</a></td><td>35</td><td>0</td><td>AI</td><td>멀티에이전트 협업이 언제 이득인지 경계를 분석하고 그래프 기반 경량 협업 기법을 제안했으나 robotics 무관함</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2609.19820'>Steering Equilibrium Selection in Regularized Self-Play via the Reference Policy</a></td><td>35</td><td>0</td><td>RL</td><td>self-play의 reference policy로 Nash 균형 중 원하는 지점을 고르는 이론 연구로 엄밀하나 robotics 무관함</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2609.19934'>Beyond Depth Truncation: Controlled Evaluation of Depth Utilization in Recursive Language Models</a></td><td>35</td><td>0</td><td>LG</td><td>depth truncation 평가가 여러 요인을 뒤섞는다는 것을 통제 실험으로 분리한 방법론 연구이며 아키텍처 분석에 유용하나 robotics 무관함</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2609.19944'>MaSCoD: A Multi-Agent Framework for Structural-Context-Guided Candidate Causal Graph Generation</a></td><td>35</td><td>0</td><td>AI</td><td>LLM 멀티에이전트로 candidate causal graph를 생성하는 방법이며 causal reasoning 주제와 닿아있으나 도메인이 표형 데이터이고 robotics 무관함</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2609.20804'>An Empirical Study of Harness Design for Coding Agents</a></td><td>35</td><td>0</td><td>AI</td><td>context 관리·planning·action space를 요소별로 176가지 조합으로 통제 비교한 실증 연구이며 harness 설계에 일반적 교훈을 주지만 robotics 무관함</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2609.19894'>Learning Reliable Parking Policies via Offline Reinforcement Learning with Quantized Action Representations</a></td><td>34</td><td>4</td><td>RL</td><td>LiDAR 특징을 조건화한 오프라인 RL로 주차 정책을 학습한 논문임. CARLA 시뮬레이션에 한정되며 offline RL 기법 자체는 기존 방법 조합에 가까움.</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2609.19152'>FakeSpotter: A content and strategy agnostic Viral Misinformation Detection Tool</a></td><td>34</td><td>0</td><td>NLP</td><td>진위판정 대신 misinformation의 구조적 지문을 측정해 바이럴 위험도를 추정하는 도구임. F1 0.79대로 준수하나 응용 시스템 성격이 강함.</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2609.19650'>Improving Cross-Lingual Transfer for Sequential Sentence Classification in Research Papers via Structural Similarity</a></td><td>34</td><td>0</td><td>NLP</td><td>13개 비영어권 논문 데이터셋으로 sequential sentence classification의 cross-lingual 전이 요인을 분석한 논문임. 언어적 유사성보다 label 분포 유사성이 전이를 더 잘 예측한다는 결과가 실용적임.</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2609.20223'>Before the Warning Comes Too Late: Incremental Phone-Scam Detection from Speech</a></td><td>34</td><td>0</td><td>NLP</td><td>통화 종료 전에 사기를 판별해야 하는 스트리밍 세팅에서 겹치는 윈도우와 순환모델로 10초 만에 첫 예측을 내는 시스템임. ROC-AUC 0.9953으로 응용 성능은 강하나 방법론적 새로움은 제한적임.</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2609.19592'>Selective Cotton Boll Localization for Robotic Harvesting: Evaluation of Deep Learning Vision Models Under Field Conditions</a></td><td>33</td><td>5</td><td>Manipulation</td><td>로봇 목화 수확을 위한 YOLO 계열 detection·segmentation 비교 평가이고 UR5e 실로봇 검증은 있으나 방법 novelty는 낮음</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2609.19745'>Region-Level Policy Optimization for Fine-grained MLLM Perception</a></td><td>33</td><td>1</td><td>Multimodal</td><td>RoI 탐지와 인식의 해상도 요구 차이를 이용해 region-level RL로 MLLM 토큰 예산을 줄인 연구이고 로봇 적용은 없음</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2609.20262'>Generative Verification: Rethinking the Uncertainty Signal for Active Learning of Object Detection</a></td><td>33</td><td>1</td><td>CV</td><td>독립적인 생성 모델로 detection label을 재도출해 disagreement를 active learning 신호로 쓰는 새로운 paradigm이나 로봇 적용은 없음</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2609.20283'>Queries Knew More Than We Thought: Uncovering Latent Knowledge in Segmentation Models</a></td><td>33</td><td>1</td><td>CV</td><td>frozen segmentation 모델이 이미 계산했지만 노출하지 않은 좋은 mask 후보를 선별 recover하는 selector를 제안했으나 로봇 적용은 없음</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2609.20751'>dQwen3.5: Hybrid-Attention Diffusion Language Models</a></td><td>33</td><td>0</td><td>NLP</td><td>hybrid-attention AR 모델을 diffusion LM으로 변환하는 적응 기법이며 robotics 무관함</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2609.19876'>SlugTrails: An Egocentric Benchmark for Floor Plan Localization in Large Buildings</a></td><td>32</td><td>4</td><td>Navigation</td><td>대형 건물의 floor plan localization 벤치마크로 기존 checkpoint 실패를 드러내고 fine-tuning 효과를 보였으나 방법보다 데이터셋 기여가 큼</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2609.20731'>Underwater Visual Target Tracking with Target-Specific Depth Estimation and Adaptive Model-Fusion Predictive Control</a></td><td>32</td><td>4</td><td>Control</td><td>target-specific depth 추출과 model-fusion MPC로 수중 표적을 추적하는 논문임. 실험 검증은 있으나 방법 자체는 기존 요소의 조합임.</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2609.19393'>WZPlanner: Safe End-to-End Path Planning for Autonomous Driving in Work Zones</a></td><td>32</td><td>3</td><td>Navigation</td><td>work zone 자율주행 경로계획 데이터셋과 모델 제안이나 특정 도메인 fine-tuning 성격이 강함</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2609.19628'>VGGT-GS SLAM: Uncalibrated Monocular Gaussian Splatting SLAM with Feed-Forward Priors</a></td><td>32</td><td>3</td><td>3D Vision</td><td>VGGT prior 기반 uncalibrated monocular Gaussian SLAM으로 baseline 성능 개선에 머무는 engineering 기여임</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2609.20300'>Improving Generalization and Robustness in Offline Reinforcement Learning via Boundary-Aware Data Augmentation</a></td><td>32</td><td>3</td><td>RL</td><td>경계 인접 상태 보간으로 offline RL의 in-distribution 일반화를 개선. 이론적 오차 경계와 실험을 함께 제시했으나 RL 벤치마크 중심 기여임.</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2609.19664'>VideoResearcher: Self-Improving Tool Design for Long-Video Understanding</a></td><td>32</td><td>2</td><td>Video</td><td>long video 이해를 위해 tool을 스스로 설계·개선하는 training-free multi-agent 프레임워크로 아이디어는 흥미로우나 로봇 적용은 없음</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2609.20139'>Cross-Modal Attention Acts as a Frequency Filter: Why Verbose Prompts Improve Robustness in Vision-Language Models</a></td><td>32</td><td>1</td><td>Multimodal</td><td>질문의 verbose함이 cross-modal attention의 주파수 필터로 작용해 VLM corruption robustness를 바꾼다는 분석이나 로봇 적용은 없음</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2609.20700'>Should This Case Be Adapted? Prediction Fragmentation Controls Test-Time Adaptation</a></td><td>32</td><td>1</td><td>CV</td><td>의료 영상 test-time adaptation에서 사례별 적용 여부를 판단하는 라우터를 제안해 무분별한 적응의 해를 줄인 연구이고 test-time optimization 주제와 닿으나 로봇 적용은 없음</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2609.19585'>CliniCIRCA: A Modular LLM Framework for Constructing Longitudinal Mental Health Patient Journeys from Raw EHR Narratives</a></td><td>32</td><td>0</td><td>NLP</td><td>정신건강 퇴원요약에서 사건의 시점을 복원하는 다단계 LLM 파이프라인임. 임상 응용 시스템 논문으로 일반 ML 기여는 제한적임.</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2609.19916'>KoNeoBench: A Curated Evaluation Dataset for LLM Understanding of Korean Neologisms</a></td><td>32</td><td>0</td><td>NLP</td><td>2020년 이후 한국어 신조어 1,785개로 LLM의 신조어 이해를 평가하는 벤치마크임. 최신 모델도 어원 분석과 정의 생성에서 뚜렷한 한계를 보임.</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2609.20104'>Design of the IBM Granite 5.0 TurboCTC ASR Model</a></td><td>32</td><td>0</td><td>NLP</td><td>4.7억 파라미터 encoder-only ASR 모델 Granite 5.0의 아키텍처·학습법 설계 논문임. 속도-정확도 파레토 프런티어를 달성했으나 시스템 엔지니어링 성격이 강함.</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2609.20530'>Relational Attention for Data-Efficient Language Modeling</a></td><td>32</td><td>0</td><td>NLP</td><td>relational attention을 언어모델에 결합해 데이터 효율을 높인 BabyLM 챌린지 제출물로 소규모 벤치마크에 한정됨</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2609.19336'>Dynamic-LIVO: A Dynamic-Aware LiDAR-Inertial-Visual Odometry System Using Spatio-Temporal Normals</a></td><td>30</td><td>4</td><td>Navigation</td><td>spatio-temporal normal로 동적 LiDAR 포인트를 지연 분류해 LIVO의 정적 매핑 품질을 개선. SLAM 엔지니어링 기여에 가까움.</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2609.19872'>PART: Learning 3D Part Assembly and Retrieval with Transformers</a></td><td>30</td><td>3</td><td>3D Vision</td><td>3D part retrieval과 6-DoF pose 예측을 set prediction으로 통합한 transformer 프레임워크로 object-centric 3D representation과 연결되나 조립·그래픽스 응용 중심임</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2609.19802'>Affective Shared Autonomy: Temporal Affect Dynamics and Subjective Evaluation in Bimanual Teleoperation Tasks</a></td><td>30</td><td>3</td><td>Embodied AI</td><td>원격조작 중 정서상태를 추정해 shared autonomy를 조절하는 시스템임. HRI 응용이며 로봇러닝 핵심 주제와는 거리가 있음.</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2609.20087'>Graph-Based Design of Soft Grippers with Multi-Objective Quality-Diversity Optimisation</a></td><td>30</td><td>3</td><td>Manipulation</td><td>그래프 기반 설계공간과 multi-objective quality-diversity 최적화로 범용 soft gripper를 설계하는 논문임. 설계 최적화 기여이며 로봇러닝 우선주제와는 거리가 있음.</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2609.20670'>MAGNETAR: Multipath-Guided Spatial Posteriors for Transmitter Pose Inference in the Upper Mid-Band</a></td><td>30</td><td>3</td><td>Navigation</td><td>upper mid-band RF multipath로 송신기 위치와 방향의 joint posterior를 추정하는 논문임. 로봇 로컬라이제이션에 쓰이지만 신호처리 기여가 중심이며 로봇러닝 우선주제와는 거리가 있음.</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2609.19437'>Bayesian Optimization with Rich Auxiliary Information via LLMs</a></td><td>30</td><td>2</td><td>LG</td><td>학습 곡선이나 전문가 노트 같은 풍부한 부가정보를 LLM으로 활용하는 Bayesian Optimization 방법으로 test-time optimization과 인접하나 로봇 적용은 없음</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2609.20004'>EPIG-Tree: Compute-Optimal Branching for Gradient-Efficient Reinforcement Learning</a></td><td>30</td><td>2</td><td>RL</td><td>policy gradient 분산 감소 기준으로 rollout tree branching을 배분하는 기법. MuJoCo continuous control에서도 검증했으나 주 타겟은 LLM RL임.</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2609.19391'>MAGS: Multi-agent Auto-formalization Guarantees Safety for Agentic Outputs</a></td><td>30</td><td>2</td><td>AI</td><td>Dafny 기반 formal verification으로 생성 코드의 안전성을 보장하는 프레임워크이며 로봇팔 태스크 20개를 포함하나 중심은 소프트웨어 검증임</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2609.19279'>Radio-Frequency Convolutional Neural Networks</a></td><td>30</td><td>1</td><td>LG</td><td>무선 라디오의 frequency mixer를 CNN convolution 연산으로 재활용하는 하드웨어 아이디어로 참신하나 로봇과 무관함</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2609.20398'>Schema-Anchored Latent Reasoning for Semantic Parsing-Based Knowledge Base Question Answering</a></td><td>30</td><td>0</td><td>NLP</td><td>KB schema를 latent reasoning에 정렬시켜 semantic parsing 오류 전파를 줄인 방법인데 개선폭이 작고 robotics와 무관함</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2609.20051'>DART: Distillation-Aware Reparameterization for Training-Free LoRA Reuse in Few-Step Video Diffusion Models</a></td><td>30</td><td>0</td><td>Video</td><td>few-step video diffusion에서 LoRA를 재보정 없이 재사용하는 방법으로 기능 보존 점수를 개선했으나 robotics 적용 논의는 없음</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2609.19447'>From Wizard-of-Oz Human-Robot Dialogue Collection to a Taxonomy of Robot Response Decisions: A Retrospective Analysis of Assistive Pilot Interactions</a></td><td>28</td><td>4</td><td>Embodied AI</td><td>Wizard-of-Oz 파일럿 40 에피소드를 분석해 로봇 응답 의사결정 taxonomy를 도출. 참가자 5명, 에피소드 40개로 표본이 작아 일반화는 제한적임.</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2609.19533'>SLAMSqueezeBench: Comparing SLAM Systems under Resource Constraints</a></td><td>28</td><td>4</td><td>Navigation</td><td>자원 제약 하에서 3DGS 포함 9개 SLAM 시스템을 비교하는 벤치마크 프레임워크. 벤치마크 인프라 기여임.</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2609.20604'>Semantic SLAM in Precision Agriculture using Bayesian Inference</a></td><td>28</td><td>4</td><td>Navigation</td><td>정밀농업용 Bayesian semantic SLAM 논문임. Spot 로봇으로 400주 이상 매핑을 검증했으나 기존 SLAM+object detection의 통합 수준임.</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2609.19973'>An Event Preserving Velocity Invariant Representation for Event Cameras</a></td><td>28</td><td>3</td><td>CV</td><td>이벤트 카메라의 velocity-invariant 표현을 제안한 연구로 로봇 perception에 쓰일 수 있으나 응용 검증은 UAV tiny object 탐지에 그침</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2609.20066'>PointEvent: Rethinking Event-based Tiny Object Detection via Serialized Motion Evidence Accumulation</a></td><td>28</td><td>3</td><td>CV</td><td>이벤트 기반 tiny UAV 탐지를 위한 serialized motion evidence accumulation 방법으로 로봇 perception에 참고할 수 있으나 UAV tiny object 응용에 국한됨</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2609.19527'>AURORA: A Natural Language-Driven Agentic Framework for Understanding, Reasoning, and Orchestrating Reliable Air-Ground Co-Simulation</a></td><td>28</td><td>3</td><td>Embodied AI</td><td>자연어로 air-ground 시나리오를 생성하고 실행 전후로 검증·수정하는 agentic 프레임워크. 시뮬레이션 도구 논문으로 robot learning 핵심 주제와는 거리가 있음.</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2609.20318'>LLM-Guided Transformation of Non-Critical Driving Scenes into Safety-Critical Scenarios Using Augmented Reality</a></td><td>28</td><td>3</td><td>CV</td><td>LLM과 AR로 안전 주행 장면을 안전-critical 시나리오로 변환하는 파이프라인임. 자율주행 테스트 도구이며 로봇러닝 핵심주제와는 거리가 있음.</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2609.19956'>Graph-Based Stochastic Power-UCT: Monte-Carlo Graph Search with Power Mean Estimation</a></td><td>28</td><td>2</td><td>RL</td><td>stochastic MDP에서 상태 공유 그래프 기반 MCTS를 개선한 planning 알고리즘. 로봇 TAMP에 간접 적용 가능하나 본문은 일반 planning benchmark에 한정됨.</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2609.20098'>CARE-VI: Conservative Adaptive Reliability Estimation for Value Improvement in Off-Policy Actor-Critic Learning</a></td><td>28</td><td>2</td><td>RL</td><td>off-policy actor-critic의 TD target 신뢰도를 conservative하게 조정하는 3단 모듈 조합. MuJoCo 4개 task로 검증했으나 module 결합형 engineering에 가까움.</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2609.19996'>Customizable and Jointly Optimized Route Planning: A Deep Architecture Enabling Differentiable Shortest-Path Search</a></td><td>28</td><td>2</td><td>Navigation</td><td>Pareto 최적 경로 집합을 학습해 경로 랭킹을 미분 가능하게 만든 내비게이션 연구로 자율주행 경로계획과 유사하나 로봇 내비게이션 실험은 아님</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2609.19747'>STAR: Structure-aware Test-time Adaptation for diffusion-based light field Reconstruction</a></td><td>28</td><td>1</td><td>CV</td><td>light field 복원에 test-time adaptation을 적용한 연구로 주제는 우선순위와 닿아있으나 응용이 이미징에 국한됨</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2609.19812'>Absence is Presence: Understanding Visual Scene Negative Events Under Safety Cognitive Constraint</a></td><td>28</td><td>1</td><td>Multimodal</td><td>안전 인지 제약 하 시각적 부재 사건을 counterfactual 재구성으로 포착하는 captioning 연구로 counterfactual reasoning 주제와 닿으나 로봇 적용은 없음</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2609.20248'>Distance to Class Prototypes: Active Learning for Object Detection</a></td><td>28</td><td>1</td><td>CV</td><td>supervised contrastive embedding 거리로 object detection active learning 신호를 만든 연구로 저비용이나 novelty는 제한적임</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2609.20067'>FCA-Guided Counterfactual Explanations for Multi-Modal Breast Cancer Diagnosis: A Framework Achieving Perfect Validity with Emergent Sparsity</a></td><td>28</td><td>1</td><td>Multimodal</td><td>formal concept analysis 격자를 제약으로 쓴 유방암 진단 counterfactual 설명 방법으로 validity는 완벽하나 도메인이 의료 XAI이고 robotics 무관함</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2609.19384'>Riemannian--Lorentz Fusion of Vision Transformers and State-Space Models</a></td><td>28</td><td>0</td><td>CV</td><td>ViT와 SSM을 hyperbolic 기하로 병합하는 방법이나 두 브랜치가 학습되어 training-free merge가 아니고 로봇과 무관함</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2609.19363'>Stiefel Attention: When the Geometry of Transformer Projection Matrices Dominates Optimizer Choice---and When It Does Not</a></td><td>28</td><td>0</td><td>LG</td><td>attention projection 행렬을 Stiefel manifold에 제약해 weight decay 영향을 없애는 최적화 연구로 흥미로운 이론이나 로봇과 무관함</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2609.19805'>Dictionary-Constrained Grapheme-to-Phoneme for Unsegmented Languages from LLM-Annotated Data</a></td><td>28</td><td>0</td><td>NLP</td><td>일본어 같은 비분절 언어의 G2P를 LLM 생성 200만 문장으로 보강한 CRF 기반 방법임. 정확도가 매우 높으나(99.62%) 응용 엔지니어링 성격이 강함.</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2609.20232'>The Public Discourse Corpus (PDC): A Speaker-Attributed Dataset for Valence and Epistemic Modality with Target Speaker Participation</a></td><td>28</td><td>0</td><td>NLP</td><td>공인 인터뷰 발화의 감정가·인식양상을 화자 단위로 주석한 데이터셋임. 화자 참여도를 5단계로 분류하는 TSP 체계를 제안했으나 자원 구축 논문 성격이 강함.</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2609.20779'>Harm Laundering in GPT Models: Evidence That Gender Discrimination Is Transformed Rather Than Reduced Across Safety-Trained Generations</a></td><td>28</td><td>0</td><td>NLP</td><td>GPT 세대별 gender bias가 사라진 게 아니라 형태만 바뀐다는 분석으로 안전성 연구지만 robotics 무관함</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2609.20821'>Embedding Models Measure in Peculiar Ways</a></td><td>28</td><td>0</td><td>NLP</td><td>임베딩이 물리량 유사성을 표면 문자열 유사도로만 반영한다는 분석이며 robotics 무관함</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2609.19387'>Do AI Agents Understand Computer Architecture?</a></td><td>28</td><td>0</td><td>AI</td><td>동일 문제를 의미 있는 프레이밍과 익명 변수로 각각 줘서 agent가 진짜 아키텍처를 이해하는지 측정한 설계는 흥미로우나 5~6회 반복의 예비 결과이고 robotics 무관함</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2609.19448'>The syntax and semantics of goals</a></td><td>28</td><td>0</td><td>AI</td><td>목표 표상을 언어의 syntax-semantics interface에 빗댄 이론적 종합 논문으로 실증 실험이 없음</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2609.19551'>Continual Enterprise World Model Discovery in Dynamic Systems</a></td><td>28</td><td>0</td><td>AI</td><td>제목은 world model이지만 실제로는 기업 시스템의 숨은 업무 규칙을 추론하는 문제이며 물리 world model과 무관함</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2609.19754'>AutoData: Agentic Search for Pre-training Data Selection</a></td><td>28</td><td>0</td><td>LG</td><td>사전학습 데이터 선별을 실행 가능한 알고리즘 탐색 문제로 재정의한 에이전트 연구로 robotics 무관함</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2609.20027'>Can Data Attribution Filter Out Subliminal Learning? Not Reliably</a></td><td>28</td><td>0</td><td>LG</td><td>gradient 기반 attribution이 subliminal learning을 걸러내는지 검증했고 EK-FAC이 부분적으로만 효과적이라는 결과로 robotics 무관함</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2609.20089'>UnifiedPlayers: Enhance Tool-Integrated Reasoning in Agentic Reinforcement Learning</a></td><td>28</td><td>0</td><td>RL</td><td>planning·execution·evaluation 세 역할을 GRPO로 공동학습시켜 tool-integrated reasoning을 개선한 연구로 robotics 무관함</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2609.20110'>Perception, Layout, and Validation: Calibrated Confidence for Reliable Straight-Through Processing of Financial Documents</a></td><td>28</td><td>0</td><td>Multimodal</td><td>VLM의 verbalized confidence 대신 지각·레이아웃·검증 채널을 분해해 conformal risk control로 문서처리 자동승인율을 크게 올린 연구로 robotics 무관함</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2609.20200'>JointMatch: A Unified Heterogeneous Graph Neural Solver for Large-Scale Ride-Sharing Matching</a></td><td>28</td><td>0</td><td>LG</td><td>라이드셰어링 매칭을 하나의 그래프로 합쳐 그래프신경망으로 푼 연구이며 뉴욕 택시 데이터로 검증했으나 robotics 무관함</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2609.20358'>Generating Heterogeneous 3D Geological Microstructures from 2D Images via a Stable Diffusion-Adversarial Model</a></td><td>28</td><td>0</td><td>CV</td><td>2D 이미지에서 3D 지질 미세구조를 생성하는 diffusion-adversarial 모델로 재료과학 도메인이며 robotics 무관함</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2609.20455'>SkillAA: Attribution-Guided Skill-Graph Updating with Targeted Validation and Rollback</a></td><td>28</td><td>0</td><td>AI</td><td>실패와 성공 실행을 대조해 skill graph의 특정 노드만 수정하는 attribution 기반 편집 방법으로 SearchQA 등에서 검증했으나 robotics 무관함</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2609.20474'>How Do Agent Harnesses Create Value? Planning Information and Release Control in Stateful LLM Agents</a></td><td>28</td><td>0</td><td>AI</td><td>고정 계획과 검증기가 성공률과 오탐률에 미치는 영향을 tau2-bench로 분리한 실증 연구로 robotics 무관함</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2609.20519'>SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness</a></td><td>28</td><td>0</td><td>AI</td><td>코딩 에이전트 harness를 재귀적으로 개선해 토큰 사용을 크게 줄인 연구로 robotics 무관함</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2609.20535'>FreqCondNorm: Towards Cross-domain Predictive Maintenance through a Frequency-Conditioned Transformer Foundation Model</a></td><td>28</td><td>0</td><td>LG</td><td>주파수 조건부 정규화로 여러 예지보전 데이터셋을 통합 학습한 파운데이션 모델이며 RUL 예측은 개선 안 됐고 robotics 무관함</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2609.20543'>Language-model groups overstate consensus when replaying human deliberation on a reasoning task</a></td><td>28</td><td>0</td><td>NLP</td><td>인간 토론을 LLM 멀티에이전트로 재현했더니 합의율이 사람보다 훨씬 높게 나온다는 실증 연구로 robotics 무관함</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2609.20722'>Deep Noir: Autonomous Steering Discovery via Architectural Chronometry in Transformer Models</a></td><td>28</td><td>0</td><td>NLP</td><td>logit lens와 causal head attribution으로 steering 지점을 자동 탐색하는 프레임워크이며 robotics 무관함</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2609.19912'>Distributed Model Predictive Control with Connectivity-based Contracts</a></td><td>26</td><td>3</td><td>Control</td><td>연결성을 보장하는 local contract 기반 분산 MPC 프레임워크임. 멀티로봇 제어이론 기여로 로봇러닝 우선주제와는 거리가 있음.</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2609.20435'>Time-Efficient Iterative Learning Planning for Safety-Critical Dynamic Obstacle Avoidance</a></td><td>26</td><td>3</td><td>Navigation</td><td>동적 장애물 회피를 위해 iterative learning planning에 risk-blended CBF를 결합한 논문임. 계산복잡도 분석은 있으나 방법론적 기여는 기존 요소의 결합 수준임.</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2609.20540'>Integrated Guidance and Control of a Mother-Child UAV-UGV System for Cooperative Missions</a></td><td>26</td><td>3</td><td>Control</td><td>모선-자선 UAV-UGV의 공중 회수 임무를 위한 통합 유도제어 시스템임. 실외 20회 임무 중 17회 성공한 시스템통합 논문으로 학습기반 기여는 없음.</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2609.20680'>Towards Scaling Marine Perception with Synthetic Data</a></td><td>26</td><td>3</td><td>CV</td><td>IsaacSim 기반 해양 시뮬레이터에 synthetic data generation 파이프라인을 더한 논문임. sim-to-real 실험은 있으나 새로운 학습방법론은 없음.</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2609.19742'>Equivariant Filter Design for Acoustic and Depth Aided Inertial Navigation Systems</a></td><td>26</td><td>2</td><td>Navigation</td><td>AUV용 tangent-group equivariant filter로 IMU bias를 다루는 상태추정 논문임. 필터링 이론 기여이나 로봇러닝과 거리가 있음.</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2609.19813'>Vehicle Trajectory Prediction via Neural Fusion of Multiple EKF-Based Trajectory Candidates</a></td><td>26</td><td>2</td><td>Navigation</td><td>EKF 기반 후보 경로를 신경망으로 late fusion해 차량 궤적 예측을 개선한 논문임. 개선폭은 있으나 기존 예측기에 모듈을 더한 수준의 기여임.</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2609.19553'>From Parameters to Behaviors: A Survey of Model Fusion for Large Language Models</a></td><td>26</td><td>0</td><td>NLP</td><td>LLM model fusion을 parameter·representation·behavior 세 층위로 정리한 서베이 논문임. 새로운 실험 결과는 없고 분류체계 정리에 그침.</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2609.19615'>Semantic Layer Induction from Raw Telemetry via Hierarchical LLM and RAG Abstraction</a></td><td>26</td><td>0</td><td>NLP</td><td>원시 텔레메트리에서 비즈니스 시맨틱 레이어를 LLM+RAG로 자동 구축하는 엔지니어링 파이프라인임. 실무적 효용은 크나 연구적 새로움은 제한적임.</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2609.19879'>VākQA: A Benchmark and Evaluation Study for Telugu Spoken Factoid Question Answering</a></td><td>26</td><td>0</td><td>NLP</td><td>텔루구어 음성 factoid QA 벤치마크임. LLM judge의 평가 신뢰도까지 검증한 점은 꼼꼼하나 저자원 언어 리소스 논문임.</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2609.20178'>MTF-Net: Multi-Modal Temporal Feature Fusion Network for Pedestrian Intention Prediction</a></td><td>25</td><td>3</td><td>Navigation</td><td>보행자 crossing intention을 multi-modal temporal fusion으로 예측하는 연구로 자율주행 안전과 관련 있으나 방법은 architecture 조합 수준임</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2609.19302'>OHRID-Retail: An Open Multimodal Dataset of Human Activity in Retail Environments</a></td><td>25</td><td>3</td><td>Embodied AI</td><td>로봇 안내 하에 소매환경 인간 행동을 IMU·EMG로 기록한 공개 데이터셋. 방법론 기여보다 데이터셋 공개가 핵심임.</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2609.19347'>Kinematics-Grounded Agentic AI for Robotic Additive Manufacturing Process Planning</a></td><td>25</td><td>3</td><td>Embodied AI</td><td>슬라이서·자세·역기구학 결정을 LLM 에이전트가 통합 평가해 로봇 적층제조 경로를 계획. 제조 도메인 특화로 로봇학습 핵심 주제와는 거리가 있음.</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2609.19367'>Design and Experimental Validation of a 3D Printed Torsional Series Elastic Actuator for Safe Human Robot Interaction</a></td><td>25</td><td>3</td><td>Embodied AI</td><td>TPU 3D 프린팅 토션 스프링으로 저비용 SEA를 제작해 안전한 물리적 상호작용을 구현. 액추에이터 설계 기여로 학습 요소는 없음.</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2609.19716'>GAPrompt++: Multi-Granular Geometry-Aware Point Cloud Prompt for 3D Vision Model</a></td><td>25</td><td>2</td><td>3D Vision</td><td>포인트 클라우드 PEFT용 geometry-aware prompt 방법으로 3D vision 모델 적응에 기여하나 로봇 적용 근거는 약함</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2609.19907'>GS-PI: An Optimization-Decoupled Appearance Decomposition Approach for Generating PBR Gaussian Assets</a></td><td>25</td><td>2</td><td>3D Vision</td><td>3DGS에서 PBR material을 point cloud 조건 diffusion으로 분리 생성하는 방법으로 그래픽스 응용 중심이고 로봇 적용은 약함</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2609.20623'>PhGS: Post-Hoc Pruning and Refinement of Single-View Feed-Forward 3D Gaussian Reconstructions</a></td><td>25</td><td>2</td><td>3D Vision</td><td>단일 뷰 feed-forward 3DGS의 중복 Gaussian을 post-hoc pruning·refinement로 압축하는 연구로 efficiency 중심이고 로봇 적용은 약함</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2609.19538'>Agentic AI Networking for Heterogeneous Unmanned Aerial Systems in Low-Altitude Wireless Networks</a></td><td>25</td><td>2</td><td>RL</td><td>LLM과 MARL을 결합한 저고도 무인기 네트워킹 프레임워크로 항공 자율성과 맞닿아 있으나 통신자원 배분이 중심이고 물리 조작·지각은 다루지 않음</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2609.19630'>From Intent to Action: Benchmarking LLM Safety in Vehicle Voice Command Authorization</a></td><td>25</td><td>2</td><td>Embodied AI</td><td>차량 음성 명령의 실행 여부를 판단하는 안전성 벤치마크로 cs.RO 태그가 있으나 실제로는 음성 인터페이스 안전 문제임</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2609.20349'>A Qualitative Model for Reasoning about Path and Support</a></td><td>25</td><td>2</td><td>Embodied AI</td><td>블록퍼즐 게임에서 무게중심 안정성 로직을 결합한 정성적 공간추론 모델로 embodied spatial reasoning과 결이 비슷하나 교육용 게임 튜터링이 목적임</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2609.19767'>Benchmarking MLLMs via Cognitive Expected Scene Graph for Safety-Critical Visual Negation Understanding</a></td><td>25</td><td>1</td><td>Multimodal</td><td>안전 인지 하 시각적 부정 이해 벤치마크로 기존 metric의 실패를 드러냈으나 로봇 적용은 없음</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2609.19383'>FCx: An algorithm for finding Feasible Counterfactual Explanations</a></td><td>25</td><td>1</td><td>LG</td><td>실행 가능성을 강제하는 counterfactual 설명 생성 방법으로 counterfactual reasoning 주제와 닿으나 tabular fairness 응용이고 로봇과 무관함</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2609.19521'>LSTM-UT and Recurrent-Depth Transformers on Cellular Automata</a></td><td>25</td><td>1</td><td>LG</td><td>cellular automata에서 recurrent-depth transformer의 정보 유지 방식을 비교해 bounded gated memory의 이점을 보인 연구로 일반 아키텍처 분석이고 로봇 적용은 없음</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2609.20538'>Refuse, Decompose, Refresh: A Claim-Safe Protocol for Closed-Loop AI Evaluation</a></td><td>25</td><td>1</td><td>AI</td><td>closed-loop 평가에서 재현성과 타당한 주장을 분리하는 claim-safe 프로토콜을 시뮬레이터로 검증한 방법론 연구로 robotics 평가에 참고할 만하나 실물 로봇 적용은 없음</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2609.19354'>Can Vision-Language Models Judge Olympic Diving? From Reasoning to Scores in Zero-Shot Action Quality Assessment</a></td><td>25</td><td>0</td><td>Multimodal</td><td>VLM으로 다이빙을 채점하는 zero-shot AQA 연구이고 novelty가 제한적이며 로봇과 무관함</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2609.19702'>Understanding and Exploiting Diagonal Attention Sparsity in Autoregressive Image Generation</a></td><td>25</td><td>0</td><td>CV</td><td>autoregressive 이미지 생성의 diagonal attention sparsity를 규명해 효율화한 연구로 로봇과 무관함</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2609.19991'>AVTrace: Diagnosing Audio-Visual Temporal Reasoning in Omni Models</a></td><td>25</td><td>0</td><td>Multimodal</td><td>omni model의 audio-visual 시간 추론을 진단하는 벤치마크로 모델들의 약점을 드러냈으나 로봇 적용은 없음</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2609.19288'>Learning-Induced Dynamical Transition in Recurrent Neural Networks</a></td><td>25</td><td>0</td><td>LG</td><td>학습이 RNN의 chaotic-to-stable 동역학 전이를 어떻게 만드는지 DMFT로 규명한 이론 연구로 로봇과 무관함</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2609.19356'>How to Guide Your Language Flow</a></td><td>25</td><td>0</td><td>LG</td><td>diffusion 모델의 내부 상태로 flow matching guidance를 만드는 probe guidance 기법으로 language diffusion에서 성능을 보였으나 로봇과 무관함</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2609.19476'>Search at the Cost of Sampling: Nearly-Instant Latent Space Bayesian Optimization</a></td><td>25</td><td>0</td><td>LG</td><td>구형 잠재공간의 선형 서러게이트로 Bayesian Optimization을 100배 가속한 방법으로 분자·이미지 생성 탐색에 쓰이고 로봇과 무관함</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2609.20166'>Small Enough to Know Everything: The Fully-Enumerable Transformer as an Instrument for the Science of Delayed Generalization</a></td><td>25</td><td>0</td><td>LG</td><td>완전 열거 가능한 소형 transformer로 grokking 법칙의 스케일 불변성을 검증. 과학적 방법론은 흥미로우나 로보틱스와 무관함.</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2609.20539'>Parallelism, critical windows, and separations among diffusion language models</a></td><td>25</td><td>0</td><td>NLP</td><td>masked·uniform·Gaussian diffusion LM 간 병렬 샘플링 능력 차이를 이론적으로 증명. LLM 이론으로 로보틱스와 무관함.</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2609.20541'>An Analysis of Training-Free Self-Reported Confidence in Language Models</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM의 verbalized confidence가 self-consistency보다 강하다는 분석이나 100문항 소규모 실험이고 robotics 무관함</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2609.20584'>SAFARI: An Industrial Benchmark for LLM-Assisted Hazard Analysis and Risk Assessment</a></td><td>25</td><td>0</td><td>NLP</td><td>자동차 ISO 26262 위험평가에 LLM을 적용한 산업 벤치마크인데 최고 성능도 F1 0.261로 낮고 robotics 무관함</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2609.19515'>LLM-as-an-Improver: Turning Verification into Better Candidates</a></td><td>25</td><td>0</td><td>NLP</td><td>verifier 피드백으로 후보 답을 재생성해 선택 폭을 넓히는 코드·추론 벤치마크 연구로 robotics 무관함</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2609.19671'>When2Think: Learning Difficulty-Aware Length Control for Efficient Hybrid Reasoning Models</a></td><td>25</td><td>0</td><td>LG</td><td>문제 난이도에 따라 추론 길이를 조절하는 효율화 기법으로 AIME에서 토큰을 줄이며 성능을 개선했으나 robotics 적용 논의는 없음</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2609.19843'>A Dual-Process Perspective on Nudge Susceptibility in LLM-Based GUI Agents</a></td><td>25</td><td>0</td><td>AI</td><td>GUI 에이전트가 인터페이스의 넛지에 취약하다는 행동경제학 실험으로 robotics 무관함</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2609.19866'>Reproducibility is not construct validity: LLM measurement of institutionally situated communication</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM 주석의 재현성과 construct validity가 별개임을 EU AI Act 설문으로 보인 방법론 연구로 robotics 무관함</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2609.20449'>The Organization of Inference: Information, Resource Constraints, and AI Production</a></td><td>25</td><td>0</td><td>AI</td><td>정보 제약이 있는 planning과 direct execution을 비교한 AI 생산 조직경제학 연구로 SWE 태스크 실험을 했으나 robotics 무관함</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2609.19903'>REARL: A Closed-loop Autonomous Driving Simulation Enhancement Framework with Real Traffic Data and Large Language Models</a></td><td>24</td><td>2</td><td>RL</td><td>실제 교통 데이터와 LLM으로 자율주행 시뮬레이터를 폐루프 보정하는 기법. 시뮬레이션 fidelity 개선 위주로 로봇 정책 학습과는 거리가 있음.</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2609.19726'>Decoupling Physical Speed from Path Parameterization in Singularity-Free Guiding Vector Fields</a></td><td>24</td><td>2</td><td>Navigation</td><td>특이점 없는 guiding vector field에 속도 추종 기능을 추가한 제어이론 논문임. 로봇러닝 우선순위와 관련 낮음.</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2609.19717'>Learn Your Own Thoughts: Abstract Token Curriculum</a></td><td>24</td><td>0</td><td>NLP</td><td>curriculum으로 continuous thought token을 학습시키는 LLM reasoning 기법. robotics relevance 낮음.</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2609.19989'>Benchmarking LLM Compliance with China AI Generated Content Regulations</a></td><td>24</td><td>0</td><td>NLP</td><td>중국 AI 생성물 규제 준수 여부를 20개 LLM으로 측정한 벤치마크임. 규제 동향 파악에는 유용하나 ML 방법론적 기여는 없음.</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2609.20303'>Viveka-Insight: a cross-lingual concept graph and citation-grounded retrieval resource over the complete works of Swami Vivekananda in English and Bengali</a></td><td>24</td><td>0</td><td>NLP</td><td>비베카난다 전집 영어-벵골어 판본을 개념그래프와 인용근거 검색으로 연결한 디지털 인문학 자원임. 언어자원 구축이며 ML 방법론 기여는 없음.</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2609.19867'>Socialized UAV Cross-Task Learning: Towards Cross-Granularity Collaboration through Hierarchical Interaction</a></td><td>22</td><td>3</td><td>Embodied AI</td><td>UAV의 detection·segmentation cross-task 학습에서 계층적 상호작용을 규제하는 연구이고 novelty가 제한적임</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2609.19577'>Tele-Traversability: Rethinking Traversability for Teleoperated Ground Robots in Terrain Navigation</a></td><td>22</td><td>3</td><td>Navigation</td><td>traversability 개념을 로봇 중심에서 인간 조작자 인지상태 중심으로 확장하자는 position paper. 실험이나 구체적 방법 제안 없이 개념 제시에 그침.</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2609.19927'>DirtyMoCap: Robust Motion Capture from Unconstrained Markers</a></td><td>22</td><td>2</td><td>CV</td><td>레이아웃 무관 marker로부터 강건하게 모션 캡처하는 연구로 imitation learning용 인간 동작 데이터 확보에 참고할 수 있으나 직접 로봇 적용은 없음</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2609.19681'>VAST: V2X/Dynamic Map-Aware Autonomous Driving Systems Validation Toolchain</a></td><td>22</td><td>2</td><td>Navigation</td><td>V2X·Dynamic Map 인지 자율주행 검증 툴체인으로 기존 시뮬레이터들을 연결. 새 알고리즘 없이 상호운용성 인프라 통합이 핵심임.</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2609.19954'>LapaTrack-3D: 6 DoF pre-operative shape tracking for laparoscopic surgery</a></td><td>22</td><td>2</td><td>CV</td><td>복강경 수술을 위한 6DoF pre-operative shape tracking 논문임. ORB-SLAM2를 의료 도메인에 맞게 수정한 수준으로 로봇러닝 우선주제와는 거리가 있음.</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2609.19236'>RAUL: Reference-Assisted Ureteroscopy Localization for Skill Assessment</a></td><td>22</td><td>1</td><td>CV</td><td>요관경 궤적 복원으로 수술 스킬을 평가하는 의료 응용이고 로봇learning과 관련 없음</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2609.20333'>Sharp Reconstruction Bounds for Autoencoders Using the Same Forward Map</a></td><td>22</td><td>1</td><td>3D Vision</td><td>동일 forward map을 쓰는 autoencoder의 복원 오차 하한을 이론적으로 유도하고 LiDAR 숲 스캔으로 검증. 3D point cloud에 적용했으나 로봇 태스크는 없는 이론 중심 논문임.</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2609.20807'>Score Centering Stabilizes Off-policy Reinforcement Learning</a></td><td>22</td><td>1</td><td>RL</td><td>학습-추론 엔진 불일치로 인한 drift를 상쇄하는 score centering 보정항. LLM RL 안정화 기법으로 로봇 RL에 원리상 적용 가능하나 본문은 LLM 중심임.</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2609.20082'>MATCH: Model-Aware Tool Learning with Curriculum Scheduling and Hierarchically Gated Rewards</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM tool-calling RL을 위한 curriculum과 계층적 gated reward. 도구 사용 벤치마크 중심으로 로봇과 무관함.</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2609.20278'>Labeled Incidence Structures for Native Transformer Modeling of Text, Knowledge Graphs, and Hypergraphs</a></td><td>22</td><td>0</td><td>LG</td><td>텍스트·지식그래프·하이퍼그래프를 하나의 incidence 표현으로 통합하는 transformer 인코딩. 일반 표현학습 이론으로 로보틱스와 직접 연결이 없음.</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2609.19148'>Modality Discrepancy Transformer for Ambivalence and Hesitancy Recognition</a></td><td>22</td><td>0</td><td>Multimodal</td><td>표정·음성·언어 세 채널의 불일치를 9-token discrepancy 표현으로 포착해 ambivalence를 인식하는 transformer임. baseline 대비 F1이 10점 이상 개선되나 로봇러닝과는 무관한 임상 감정인식 논문임.</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2609.20484'>Edustories: A Collection of Real-world Case Studies from Classroom Practices</a></td><td>22</td><td>0</td><td>NLP</td><td>교실 상황 케이스 데이터셋으로 LLM의 교사 개입 예측력을 측정했는데 전문가보다 낮고 robotics와 무관함</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2609.19244'>Characterizing Web Search by Conversational LLM Agents: From Search Decisions and Strategies to Results and Responses</a></td><td>22</td><td>0</td><td>NLP</td><td>ChatGPT 등 4개 플랫폼의 웹검색 행태를 실측 비교한 연구로 robotics 무관함</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2609.19425'>Closed-World Resolution Against Tool Hallucination in LLM Agents</a></td><td>22</td><td>0</td><td>NLP</td><td>존재하지 않는 tool 호출을 잡는 resolver와 벤치마크를 제시했으나 robotics 무관함</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2609.19472'>Safety Beyond the Interface: Detecting Harm via Latent States in Large Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>LLaMA 내부 activation으로 harmful prompt를 탐지하는 probe 연구로 robotics 무관함</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2609.19526'>Self Improvement via Fast Tree-search</a></td><td>22</td><td>0</td><td>AI</td><td>코딩 에이전트 self-improvement에 LLM judge 기반 tree search를 결합해 비용을 줄인 연구로 robotics 무관함</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2609.19789'>Contagion on the Trading Floor: How Adversarial Signals Spread in Multi-Agent Trading Systems</a></td><td>22</td><td>0</td><td>AI</td><td>LLM 트레이딩 멀티에이전트에 소셜미디어로 주입하는 적대적 공격을 분석한 연구로 robotics 무관함</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2609.19871'>Physical knowledge on historical data matters more than enforcing physical constraints on the forecast</a></td><td>22</td><td>0</td><td>LG</td><td>물리 방정식의 중간 변수까지 예측하는 물리정보 RNN으로 지하수위 예측에 적용했으며 robotics 무관함</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2609.20026'>FedeRICo: Federated Region-Influenced Coupling for Traffic Flow Prediction</a></td><td>22</td><td>0</td><td>LG</td><td>연합학습 기반 교통량 예측에서 경계 잔차 통신으로 공간 의존성을 복구한 연구로 robotics 무관함</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2609.20261'>When AI Agents Commit: Cognitive Serializability Across Data, Evidence, Policy, and Authority</a></td><td>22</td><td>0</td><td>AI</td><td>에이전트의 데이터·증거·정책 기반 커밋에 직렬화 가능성 개념을 도입한 분산시스템 이론 연구로 robotics 무관함</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2609.20570'>Walking on the Slope: Stable Bipedal Gaits with Genetic-Algorithm-Optimized Trajectories</a></td><td>20</td><td>3</td><td>Control</td><td>8자유도 이족보행의 기구학·동역학 모델링과 유전알고리즘 궤적 최적화 논문임. 학습기반 방법이 아니며 로봇러닝 우선주제와는 거리가 있음.</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2609.19216'>4D Radar Perception Algorithms for Autonomous Driving: A Review</a></td><td>20</td><td>2</td><td>Navigation</td><td>4D 레이더 인식 알고리즘 리뷰 논문. 서베이로 새로운 방법론 제안은 없음.</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2609.19985'>Past, Future, All at Once: Mitigating Stability-Plasticity Dilemma via Post-hoc JANUS Rectification</a></td><td>20</td><td>1</td><td>LG</td><td>post-hoc weight rectification으로 continual learning의 catastrophic forgetting을 완화. LLM fine-tuning 중심으로 로봇 lifelong learning과는 간접적으로만 연결됨.</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2609.20352'>COMPASS: Ordered Clustered Routing at 100K Scale</a></td><td>20</td><td>1</td><td>RL</td><td>대규모 ordered clustered TSP를 위한 탐색+학습 결합 라우팅 알고리즘. e-commerce 물류 응용으로 로봇 경로계획과는 거리가 있음.</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2609.20409'>The Bias of Nonlinear Two-Time-scale Stochastic Approximation under Constant Step-Sizes</a></td><td>20</td><td>1</td><td>RL</td><td>constant step-size 비선형 two-timescale stochastic approximation의 bias 상한 이론. RL 이론 도구이나 로봇 응용은 없음.</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2609.19444'>Seeing Abnormal from Normal: Glomerular Abnormality in Representations of Normal Renal Morphology</a></td><td>20</td><td>0</td><td>CV</td><td>정상 신사구체 표현만으로 이상을 탐지하는 의료 영상 연구로 로봇과 무관함</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2609.20427'>When Do Language-Grounded Explanations Help? A Graph-Bottleneck for Farm Monitoring Interpretable Sheep Facial Pain</a></td><td>20</td><td>0</td><td>CV</td><td>양 안면 통증 인식에서 언어 기반 설명이 실제로는 무의미함을 밝히고 concept bottleneck으로 교정한 해석가능성 연구이나 로봇과 무관함</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2609.20769'>FlowSGS: Improving Flow Matching Priors for Inverse Imaging with Stochastic Interpolants</a></td><td>20</td><td>0</td><td>CV</td><td>flow matching prior를 이용한 posterior sampling 방식의 inverse imaging 해법으로 로봇과 무관함</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2609.19709'>Odds-Ratio Thompson Sampling: A Specification and Design Guide for Contrast-Based Multi-Armed Bandits</a></td><td>20</td><td>0</td><td>RL</td><td>batched bandit에서 log-odds contrast를 따로 추적하는 기법. 이론은 탄탄하나 로봇 연구와 거리가 멂.</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2609.20162'>A Noise Optimum in Rehearsal-Free Continual Learning: Isolation, Mechanism, and Scope</a></td><td>20</td><td>0</td><td>LG</td><td>rehearsal-free continual learning에서 noise 주입 최적점을 시뮬레이션으로 분석. 신경과학적 기전 분석이나 로봇 응용 없음.</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2609.20269'>Placement Is Free, Composition Is Not: The Latin Square as a Provably-Balanced Construction for Heterogeneous Sequence-Mixer Stacks</a></td><td>20</td><td>0</td><td>LG</td><td>7개 sequence-mixer를 Latin square로 배치해 배치 순서와 조합 효과를 분리한 ablation 연구. LLM 아키텍처 연구로 로보틱스와 무관함.</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2609.20744'>Video DeltaNet: A Video-Native Hybrid Attention for Livestream Video Generation</a></td><td>20</td><td>0</td><td>Video</td><td>local softmax attention과 bidirectional linear memory를 결합한 비디오 생성 효율화 기법. 라이브스트림 비디오 생성 가속이 목적으로 로보틱스와 무관함.</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2609.19151'>What Users Think of Generative AI: A Cross-Platform NLP Analysis of Trust and Friction in App Store Reviews</a></td><td>20</td><td>0</td><td>NLP</td><td>6개 GenAI 앱스토어 리뷰 1.7만 건을 토픽모델링·감성분석한 시장조사성 논문임. 방법론적 새로움은 낮음.</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2609.20169'>Fine-Tuning Models for Biomedical Relation Extraction</a></td><td>20</td><td>0</td><td>NLP</td><td>변이-표현형 관계추출을 위한 생물의학 도메인 파인튜닝 논문임. DeBERTa와 Gemini Pro 파인튜닝 결과 비교 수준으로 방법론적 새로움은 낮음.</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2609.20593'>WiC is Not WSD: A Study on LLMs and Lexical Ambiguity Resolution</a></td><td>20</td><td>0</td><td>NLP</td><td>word sense 후보 제공이 WiC 성능을 높인다는 분석이며 어휘 의미론 연구로 robotics 무관함</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2609.20625'>Chronicle: Cut-Point Replay for Regression Testing of LLM Agents</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 에이전트의 비결정성을 기록·재생해 회귀 테스트로 바꾸는 엔지니어링 도구이며 robotics 무관함</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2609.19180'>BioPhys-Bridge: A Benchmark for Interdisciplinary Scientific Reasoning in Physics-Grounded Biological Research</a></td><td>20</td><td>0</td><td>NLP</td><td>생물물리 문헌에서 근거 기반 추론을 평가하는 벤치마크로 robotics 무관함</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2609.20005'>Geopolitical Divisions Across Languages in Large Language Models</a></td><td>20</td><td>0</td><td>NLP</td><td>112개 언어로 같은 질문을 던졌을 때 LLM 답변이 지정학적으로 갈린다는 대규모 실증 연구로 robotics 무관함</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2609.20077'>Tailored to you: longitudinal effects of personalising language models</a></td><td>20</td><td>0</td><td>NLP</td><td>992명 대상 5일간 개인화 LLM 상호작용을 추적한 종단 연구로 robotics 무관함</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2609.20321'>Implementation of Tightly-Coupled SLAM Fusion of GPS, IMU, and LiDAR for Autonomous Vehicles</a></td><td>18</td><td>3</td><td>Navigation</td><td>GPS-IMU-LiDAR를 FAST-LIO2와 GTSAM으로 결합한 SLAM 구현 논문임. 기존 요소기술의 조합이며 새로운 방법론은 없음.</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2609.19793'>AI Smart Glasses for Wearable Intelligence: From Egocentric Sensing to Agentic Personalization</a></td><td>18</td><td>2</td><td>Embodied AI</td><td>AI 스마트글래스를 wearable intelligence 관점에서 정리한 survey로 실험적 기여가 없음</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2609.19375'>Enhancing the Perception of Safety and Comfort during Physical Human-Robot Handshake Interactions by Integrating Flexible Elements into a Robotic Arm</a></td><td>18</td><td>2</td><td>Embodied AI</td><td>SEA 장착 로봇팔과 rigid 팔의 악수 상호작용을 10명 대상으로 비교한 사용자 연구. 표본이 작고 기여가 제한적임.</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2609.20048'>Mechanical Precision Weeding with a Quadruped Robot</a></td><td>18</td><td>2</td><td>Manipulation</td><td>사족보행 로봇에 milling bit를 부착해 기계적으로 잡초를 제거하는 응용 논문임. 프로토타입 수준이며 로봇러닝 기여는 거의 없음.</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2609.20499'>Towards AI-enhanced control: a numerical technique for trajectory smoothing of a parallel robot for pancreatic surgery</a></td><td>18</td><td>2</td><td>Control</td><td>췌장 수술용 parallel robot의 end-effector 궤적을 S-curve로 매끄럽게 만드는 수치기법 논문임. 시뮬레이션 수준이며 로봇러닝과는 거리가 있음.</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2609.20045'>Correct Now, Insufficient Later: Auditing Update Sufficiency in Context Compression</a></td><td>18</td><td>1</td><td>NLP</td><td>context compression 메모리가 이후 update를 반영하기에 충분한지 감사하는 평가 방법론. robot memory와 이름만 유사할 뿐 LLM 대화 메모리 문제로 로보틱스와 무관함.</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2609.20297'>Intact-to-Amputee Transfer in Surface-EMG Gesture Decoding: Training Source and Calibration Budget</a></td><td>18</td><td>1</td><td>Multimodal</td><td>정상인 학습 인코더를 절단 장애인에게 전이하는 검증 연구. 보조기기 분야로 로보틱스와 간접적으로만 관련됨.</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2609.19451'>Efficient Unified Multimodal Understanding (EUMU): Winning Solution for the MUMU Track at the 8th LSVOS Challenge</a></td><td>18</td><td>0</td><td>Multimodal</td><td>멀티모달 이해 챌린지 우승 솔루션으로 task별 head 조합 수준의 engineering이고 novelty가 낮음</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2609.19483'>SCOUT: Sim-to-Real Text-Based Person Retrieval by Embedding-Space Prediction over Frozen Video Features</a></td><td>18</td><td>0</td><td>Multimodal</td><td>frozen encoder로 text 기반 person retrieval을 하는 sim-to-real 연구이고 로봇과 무관함</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2609.19990'>QCPruner: Query-Conditioned Population Coverage for Visual Token Pruning</a></td><td>18</td><td>0</td><td>Multimodal</td><td>query 조건부 utility로 시각 토큰을 pruning하는 training-free 방법으로 submodular guarantee는 있으나 로봇 적용은 없음</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2609.20100'>A Smaller Transformer in Your Transformer</a></td><td>18</td><td>0</td><td>CV</td><td>ViT 레이어 중복을 융합해 depth를 줄이는 post-hoc 압축 방법으로 efficiency 중심이고 로봇과 무관함</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2609.20160'>Needles in a Raystack: Ultra-Sparse LiDAR Occupancy Detection for Bat Tracks</a></td><td>18</td><td>0</td><td>CV</td><td>박쥐 추적을 위한 초희소 LiDAR occupancy 탐지 연구로 로봇과 무관함</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2609.20267'>CleanVideo: Adaptive Concept Erasure for Text-to-Video Diffusion Models</a></td><td>18</td><td>0</td><td>Video</td><td>text-to-video diffusion에서 개념을 선택적으로 지우는 erasure 프레임워크로 로봇과 무관함</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2609.20299'>Not All Layers Are Equal: Dynamic Layer Routing for Reliable CLIP OOD Detection</a></td><td>18</td><td>0</td><td>CV</td><td>CLIP layer 선택을 학습하는 router로 OOD detection을 개선한 연구로 로봇과 무관함</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2609.20325'>AgriScope: Pixel-Grounded Multimodal Understanding for Agricultural Images</a></td><td>18</td><td>0</td><td>Multimodal</td><td>농업 이미지의 pixel-level grounding 멀티모달 프레임워크로 로봇과 무관함</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2609.20633'>Refinement Is Inherently Editable: Training-Free Prompt-to-Prompt Image Editing with Generative Refinement Network</a></td><td>18</td><td>0</td><td>CV</td><td>이진 이미지 코드 refinement로 편집 가능성을 확보한 training-free 이미지 편집 프레임워크로 로봇과 무관함</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2609.20662'>Earth Surface Immune System for Rapid Monitoring of Unknown Anomalies</a></td><td>18</td><td>0</td><td>CV</td><td>면역계 원리를 모방해 미지의 지구 표면 이상을 탐지·분류하는 원격탐사 시스템으로 로봇과 무관함</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2609.19499'>Sample Count Is Not Enough: Candidate-Generation Strategy Shapes the Energy and Performance of LLM Test-Time Scaling</a></td><td>18</td><td>0</td><td>LG</td><td>LLM test-time scaling에서 후보 생성 스케줄이 에너지 비용에 미치는 영향을 측정한 시스템 연구로 로봇과 무관함</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2609.19539'>Compressed Active Subspaces for Scalable Bayesian Inference</a></td><td>18</td><td>0</td><td>LG</td><td>고차원 모델의 active subspace를 압축된 공간에서 구성해 Bayesian inference를 확장하는 방법으로 로봇과 무관함</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2609.19915'>Amortizing Physics-Informed Neural Solvers via Graph Hypernetworks</a></td><td>18</td><td>0</td><td>LG</td><td>PDE별 PINN을 그래프 hypernetwork로 amortize하는 기법. 물리 시뮬레이션 도구로 로봇 적용 사례 없음.</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2609.20193'>When Does Retrieval Help Time-Series Forecasting?</a></td><td>18</td><td>0</td><td>LG</td><td>retrieval이 시계열 예측에 도움되는 조건을 window-period 비율로 규명. 방법론적으로 흥미로우나 forecasting 도메인에 한정됨.</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2609.20309'>Hypernetwork-Parameterized Spatially Adaptive Neural Operators for PDE Learning</a></td><td>18</td><td>0</td><td>LG</td><td>위치별로 다른 operator parameter를 생성하는 hypernetwork 기반 neural operator. PDE 학습 도구로 로보틱스와 무관함.</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2609.20511'>When EOS Tokens Disagree: Understanding Length Inflation in On-Policy Distillation</a></td><td>18</td><td>0</td><td>NLP</td><td>teacher-student EOS token 불일치가 on-policy distillation의 length inflation을 유발함을 규명. LLM 훈련 분석으로 로보틱스와 무관함.</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2609.20676'>Epidemiological Causal Graph Identification: Challenges, Identifiability and Algorithms</a></td><td>18</td><td>0</td><td>LG</td><td>순서형·지수족 혼합 변수의 인과 방향 식별 가능성을 증명. 역학 데이터 응용으로 로보틱스와 무관함.</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2609.20794'>PosteriorBench: From Point Estimates to Posterior Matching in Evaluating Generative Inverse Solvers</a></td><td>18</td><td>0</td><td>LG</td><td>과학적 inverse problem에서 생성모델의 posterior 전체 분포 복원 능력을 평가하는 벤치마크. 물리 시뮬레이션 도메인으로 로보틱스와 무관함.</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2609.20565'>Steering the Compass: Aligning Dynamic Psychological Counseling Conversations with Cognitive Behavioral Therapy Strategies</a></td><td>18</td><td>0</td><td>NLP</td><td>CBT 전략별 상담 대화 데이터셋 구축 논문으로 robotics와 무관함</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2609.20630'>UniPolicy: Unified Objective-Specific Policies for Generative Search Advertising</a></td><td>18</td><td>0</td><td>NLP</td><td>검색광고 다목적 정책 정렬 산업 시스템 논문이며 robotics 무관함</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2609.20684'>HerHealthEval: Evaluating Multilingual and Register-Sensitive Understanding of Women&#x27;s Health Communication</a></td><td>18</td><td>0</td><td>NLP</td><td>여성 건강 상담의 다국어 이해 평가 프레임워크로 robotics 무관함</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2609.19182'>What Do We Expect from LLMs? Mapping the Design of LLM Benchmarks</a></td><td>18</td><td>0</td><td>NLP</td><td>14767편 논문을 메타분석해 벤치마크 설계 트렌드를 정리한 서베이성 연구로 robotics 무관함</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2609.19203'>Position: It is Time to Virtualize Foundation Models with a Self-evolving Operating System Layer</a></td><td>18</td><td>0</td><td>AI</td><td>foundation model을 가상화하는 OS 레이어가 필요하다는 포지션 페이퍼로 구체 구현·실험이 없음</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2609.19523'>EconSkills: Studying Skill Transfer and Retrieval for Web Agents on Live Economic Data</a></td><td>18</td><td>0</td><td>NLP</td><td>웹 에이전트가 절차를 스킬로 추상화해 재사용하는지 평가한 연구로 robotics 무관함</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2609.19654'>Replan, Repair, or Edit? A Unified Empirical Evaluation of Travel Agents for Itinerary Revision under Resource Disruptions</a></td><td>18</td><td>0</td><td>NLP</td><td>여행 일정 재계획 방법 3종을 비교한 실증 연구로 robotics 무관함</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2609.19775'>Integrating knowledge from case reports: a medical ontology based multimodal information system with structured summary</a></td><td>18</td><td>0</td><td>Multimodal</td><td>케이스 리포트를 온톨로지로 구조화한 의료 정보 검색 시스템으로 robotics 무관함</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2609.19832'>MetaRTL: Meta-path Attention Enhanced Relational Table Learning</a></td><td>18</td><td>0</td><td>LG</td><td>관계형 테이블 학습을 경량화한 메타패스 방법으로 robotics 무관함</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2609.19897'>TRACE: Accountable Agentic Retrieval for Source Discovery in Digital Archives</a></td><td>18</td><td>0</td><td>NLP</td><td>역사 아카이브에서 출처 추적이 가능한 training-free 검색 에이전트로 robotics 무관함</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2609.19928'>From &quot;Who Is This User?&quot; to &quot;What Does This Purchase Mean?&quot;: A Deployed Pipeline for Semantic User Profiling at Bank Scale</a></td><td>18</td><td>0</td><td>NLP</td><td>거래 패턴 단위로 LLM 추론 비용을 줄인 은행 배포 파이프라인으로 robotics 무관함</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2609.19947'>Not All AI Agents Are Equal: Characterizing Resource and Performance Dynamics</a></td><td>18</td><td>0</td><td>LG</td><td>에이전트 서빙의 CPU·디스크 병목을 실측하고 자원 인지 스케줄링을 제안한 시스템 연구로 robotics 무관함</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2609.20001'>E-AVI: Evidence-Grounded Multimodal Assessment for Automated Video Interviews</a></td><td>18</td><td>0</td><td>Multimodal</td><td>화상 면접 평가에 근거 기반 멀티모달 attention을 도입한 산업 시스템으로 robotics 무관함</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2609.20091'>Solving Minimum Span Antibandwidth and Cyclic Antibandwidth Labeling Problems</a></td><td>18</td><td>0</td><td>AI</td><td>그래프 라벨링 문제를 SAT로 푸는 조합최적화 연구로 robotics 무관함</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2609.20152'>MTVA-Bench: Evaluating the Language Model Inside Cascaded Voice Agents</a></td><td>18</td><td>0</td><td>NLP</td><td>cascaded voice agent 내부 LLM만 분리 평가하는 벤치마크로 robotics 무관함</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2609.20271'>AI-Driven Real-Time Relay Optimisation in Smart Urban NR-V2X Networks via Learning-to-Optimise Graph Neural Networks</a></td><td>18</td><td>0</td><td>LG</td><td>차량 네트워크 릴레이 선택을 GNN으로 학습해 MILP 대비 크게 빠르게 근사한 연구로 robotics 무관함</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2609.20301'>AgentPProf: Semantic Profiler for Long Horizon AI Agents</a></td><td>18</td><td>0</td><td>AI</td><td>장기 실행 에이전트를 위한 semantic profiler로 pprof 호환 flame graph를 제공하는 개발 도구이며 robotics 무관함</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2609.20658'>Ownership in AI-Assisted Everyday Tasks</a></td><td>18</td><td>0</td><td>AI</td><td>AI와 함께한 작업에서 소유감이 언제 유지되는지 설문한 HCI 연구로 robotics 무관함</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2609.20754'>RAFT: A Stateful Retrieval-Augmented Framework for Troubleshooting Agents</a></td><td>18</td><td>0</td><td>NLP</td><td>과거 트러블슈팅 케이스를 상태 체인으로 쪼개 단계별로 검색하는 RAG로 robotics 무관함</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2609.20691'>Custom PX4 firmware for autonomous hybrid aerial-marine missions</a></td><td>16</td><td>2</td><td>Control</td><td>공중-수상 겸용 드론을 위한 PX4 펌웨어 확장 논문임. 시스템 구현이며 연구적 새로움은 낮음.</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2609.19736'>A Phonemically Comprehensive, ASCII-Only Romanization Scheme for Thai and Lao: Systematic Cross-Lingual Correspondence and Chinese-User-Friendly Design</a></td><td>16</td><td>0</td><td>NLP</td><td>태국어·라오어를 위한 ASCII 로마자 표기법 설계 논문임. 언어자원 엔지니어링이며 ML 방법론 기여는 없음.</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2609.19359'>Smart Insole Human Activity Recognition for Continuous Monitoring in Elderly Care</a></td><td>15</td><td>1</td><td>LG</td><td>스마트 인솔로 노인 낙상 전조 활동을 인식하는 연구로 wearable sensing이나 로봇과 무관함</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2609.20174'>Robust Federated Q-Learning with Almost No Communication</a></td><td>15</td><td>1</td><td>RL</td><td>일부 에이전트가 손상된 federated Q-learning의 강건 수렴 이론. 통신 효율 중심으로 로봇 응용 없음.</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2609.20296'>Personalising a Cross-User Surface Electromyography Encoder Under a Small Calibration Budget</a></td><td>15</td><td>1</td><td>Multimodal</td><td>소수 calibration 반복으로 사용자 맞춤 sEMG 인코더를 조정하는 4가지 방법을 비교. 보조기기 HCI 연구로 로봇 응용과는 거리 있음.</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2609.19377'>LinePilot Digitizer: Line-Plot Recovery with Manual and Automatic Calibration</a></td><td>15</td><td>0</td><td>CV</td><td>라인 플롯 디지타이징 도구로 로봇learning과 무관한 engineering 기여임</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2609.19555'>A Multi-Modal Generative Model for Tomato Disease Leaves Understanding</a></td><td>15</td><td>0</td><td>Multimodal</td><td>토마토 병해 진단용 멀티모달 생성 모델로 농업 응용이고 로봇과 무관함</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2609.19631'>Instance Segmentation and Fine-grained Classification for Urban Buildings with Adaptive Region Dividing and Spatially-Supervised Contrastive Learning</a></td><td>15</td><td>0</td><td>3D Vision</td><td>도시 건물 point cloud instance segmentation·분류 연구로 로봇과 무관함</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2609.19634'>Scientific Image Quality Assessment via Multi-modal Retrieval-Augmented Generation</a></td><td>15</td><td>0</td><td>Multimodal</td><td>과학 이미지 품질 평가용 RAG 프레임워크로 챌린지 1위 수준의 engineering임</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2609.19693'>IMFD: End-to-end Multi-Face Forgery Detection through Instruction-based Large Vision-Language Models</a></td><td>15</td><td>0</td><td>CV</td><td>instruction 기반 LVLM으로 다중 얼굴 딥페이크를 탐지하는 연구이고 로봇과 무관함</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2609.19719'>SeetaPsych v1.0: An Open-source Computer Vision Toolkit for Behavior-based Psychological Measurement</a></td><td>15</td><td>0</td><td>CV</td><td>행동 기반 심리측정용 오픈소스 CV 툴킷으로 로봇과 무관한 engineering 산출물임</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2609.19740'>Federated Learning Framework for Privacy-Preserving Kidney Stone Detection</a></td><td>15</td><td>0</td><td>CV</td><td>federated learning으로 신장결석 CT를 탐지하는 의료 응용이고 로봇과 무관함</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2609.19853'>PACE: Precise AI Cinematic Expression: A Typed Specification for Script-Grounded Previsualization and Geometric Conformance</a></td><td>15</td><td>0</td><td>CV</td><td>스크립트 기반 시네마틱 previsualization을 위한 typed spec으로 로봇과 무관함</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2609.19875'>BINDER: A Latent Variable Model for Probabilistic Medical Image Registration</a></td><td>15</td><td>0</td><td>CV</td><td>잠재변수 기반 의료 영상 정합 모델로 로봇과 무관함</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2609.19964'>Enhanced Knowledge Distillation for Detection Transformer via Teacher Prediction Refinement</a></td><td>15</td><td>0</td><td>CV</td><td>DETR distillation에서 teacher 예측을 정제하는 plug-and-play 모듈로 incremental engineering 성격이 강함</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2609.19966'>Beyond the Foreground: FOV-Aware Polyp Image Synthesis via Lesion-Guided Adaptive Mucosal Context Propagation</a></td><td>15</td><td>0</td><td>CV</td><td>용종 영상 합성으로 downstream segmentation을 개선하는 의료 데이터 증강 연구이고 로봇과 무관함</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2609.20088'>G^2RA-NET: Graph-based Cross-Slice Relation Modeling with Attention Gating for Medical Image Segmentation</a></td><td>15</td><td>0</td><td>CV</td><td>뇌·복부 영상 cross-slice segmentation을 위한 graph 기반 모델로 로봇과 무관함</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2609.20147'>Bridging Modalities on the Cortex: Surface-based MRI to PET Translation with a Diffusion Bridge</a></td><td>15</td><td>0</td><td>CV</td><td>피질 표면 기반 MRI-to-PET 변환을 diffusion bridge로 수행하는 의료 영상 연구로 로봇과 무관함</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2609.20150'>Task-Oriented Semantic Feature Transmission for Multi-Task Satellite Remote Sensing over Low-SNR Channels</a></td><td>15</td><td>0</td><td>CV</td><td>위성 원격 탐사의 저SNR 환경에서 task-oriented semantic feature 전송 연구로 로봇과 무관함</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2609.20151'>Ischemic Stroke Segmentation and Net Water Uptake Quantification on Multicenter Non-Contrast CT Using Supervised Target-Domain Adaptation</a></td><td>15</td><td>0</td><td>CV</td><td>다기관 NCCT에서 허혈성 뇌졸중 segmentation과 net water uptake 정량화 연구로 로봇과 무관함</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2609.20181'>MoSSGate: Memory-Modulated State-Space Gating for Skin Lesion Segmentation</a></td><td>15</td><td>0</td><td>CV</td><td>피부병변 segmentation용 memory-modulated state-space gating 모듈로 의료 영상 응용이고 로봇과 무관함</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2609.20245'>SAGE-Yoga: Multi-Cue Learning for Yoga Pose Classification and Joint-Level Correction</a></td><td>15</td><td>0</td><td>CV</td><td>요가 자세 분류와 관절 단위 교정 피드백을 위한 coarse-to-fine 프레임워크로 로봇과 무관함</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2609.20263'>AI or Real: Detecting Partially Altered Videos Under Resource-Constrained Environments</a></td><td>15</td><td>0</td><td>CV</td><td>edge 환경에서 부분 조작 영상을 탐지하는 경량 distillation 연구로 로봇과 무관함</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2609.20340'>FreqDINO++: A Frequency-Guided Multi-Task Routing Vision Foundation Model for Universal Ultrasound Analysis</a></td><td>15</td><td>0</td><td>CV</td><td>초음파 다중 task를 위한 frequency-guided foundation model로 의료 영상 응용이고 로봇과 무관함</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2609.20423'>WeVisDoc: From Coverage to Capability for Robust End-to-End Document Parsing</a></td><td>15</td><td>0</td><td>NLP</td><td>문서 파싱의 커버리지와 취약점을 분리해 데이터 중심으로 강건성을 높인 연구로 로봇과 무관함</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2609.20441'>Cross-Architecture Foundation-Model Distillation for Edge Flood Segmentation</a></td><td>15</td><td>0</td><td>CV</td><td>홍수 segmentation foundation model을 edge용으로 distillation한 연구로 efficiency 중심이고 로봇과 무관함</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2609.20508'>Grounded Product Understanding in Livestream Videos</a></td><td>15</td><td>0</td><td>Video</td><td>라이브스트림 영상에서 상품과 관련 구간을 함께 찾는 grounding 벤치마크로 로봇과 무관함</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2609.20562'>A Dual-Stream Regulated Reconstruction and Segmentation Network with Hierarchical Artifact-Prior Modeling for Ultra-Low-Field Pediatric Neuroimaging</a></td><td>15</td><td>0</td><td>CV</td><td>초저자장 소아 뇌 MRI의 재구성·segmentation·품질평가를 통합한 프레임워크로 로봇과 무관함</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2609.20574'>DocAttriBench: Benchmarking Answer Grounding in Document Visual Question Answering</a></td><td>15</td><td>0</td><td>Multimodal</td><td>문서 VQA의 답변 근거를 요소 단위로 grounding하는 벤치마크로 로봇과 무관함</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2609.20816'>Paint-Anything: Unified Any-Color Control for Image Generation and Editing</a></td><td>15</td><td>0</td><td>CV</td><td>헥스 색상값으로 이미지 생성·편집을 통제하는 any-color 프레임워크로 로봇과 무관함</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2609.19209'>Generative Query Suggestion via Intent Coverage and Query-Level Credit Assignment</a></td><td>15</td><td>0</td><td>LG</td><td>생성형 query suggestion에서 intent 커버리지와 query별 credit assignment를 다루는 추천시스템 연구로 로봇과 무관함</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2609.19213'>Layer-wise Curriculum Learning for Efficient LLM Compression</a></td><td>15</td><td>0</td><td>LG</td><td>LLM 압축을 위한 layer-wise curriculum learning으로 efficiency 중심이고 로봇과 무관함</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2609.19242'>Block Parallelism For Efficient Distributed Long-Context Diffusion Language Model Training</a></td><td>15</td><td>0</td><td>LG</td><td>block diffusion LM의 긴 컨텍스트 분산학습을 위한 새 parallelism 기법으로 시스템 최적화이고 로봇과 무관함</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2609.19337'>Personalized Federated Hierarchical Gaussian Processes for Privacy-Preserving Modeling of Heterogeneous Distributed Systems</a></td><td>15</td><td>0</td><td>LG</td><td>이질적 클라이언트를 위한 개인화 federated hierarchical Gaussian process로 로봇과 무관함</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2609.19453'>Sharpness-Aware Minimization (SAM) Improves Classification Accuracy of Bacterial Raman Spectral Data Enabling Portable Diagnostics</a></td><td>15</td><td>0</td><td>LG</td><td>박테리아 Raman 스펙트럼 분류에 SAM optimizer를 적용해 일반화를 높인 진단 연구로 로봇과 무관함</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2609.19559'>FedFIbOS: Fisher Importance based Optimal Submodelling for Heterogeneous Federated Learning</a></td><td>15</td><td>0</td><td>LG</td><td>Fisher 정보 기반으로 이질적 federated learning의 submodel을 선택하는 이론적 기준을 제시했으나 로봇과 무관함</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2609.19616'>The Complexity Kink: A Prompt-Side Structural Complexity Index for Code-Generation Reliability</a></td><td>15</td><td>0</td><td>LG</td><td>코드 생성 신뢰도를 prompt 쪽 구조적 복잡도로 예측하는 index를 제안했으나 로봇과 무관함</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2609.19670'>CoRe: Coherence and Relational Alignment for Multivariate Time Series Forecasting</a></td><td>15</td><td>0</td><td>LG</td><td>다변량 시계열 예측에서 pointwise loss 대신 주파수 일관성과 관계 구조를 보존하는 학습 목적함수로 로봇과 무관함</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2609.19768'>OceanMoE: Structured Conditional Sparse Computation for Long-Horizon Multivariate Ocean Forecasting</a></td><td>15</td><td>0</td><td>LG</td><td>해양 예측을 위한 conditional sparse MoE 구조 개선. 순수 engineering 기여임.</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2609.19858'>Expected Hypervolume Maximization for Multiobjective Optimization under Uncertainties</a></td><td>15</td><td>0</td><td>LG</td><td>다목적 최적화에서 hypervolume 기대값을 gradient로 최적화하는 이론적 기여. 로봇 응용 없음.</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2609.19891'>Online Adaptive Kernel Mixing for Gaussian Process Decision Making</a></td><td>15</td><td>0</td><td>LG</td><td>Gaussian Process kernel 선택을 online expert learning으로 접근한 이론. 로봇 응용 없음.</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2609.19955'>One Intervention per Component is Enough: Towards Identifiability in Linear Stochastic Dynamics from Steady State</a></td><td>15</td><td>0</td><td>LG</td><td>steady-state 데이터에서 OU process 식별 가능성을 증명한 이론. 유전자 섭동 실험 중심으로 로보틱스와 무관함.</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2609.20058'>Evaluating Explanation Methods by the Predictors They Induce</a></td><td>15</td><td>0</td><td>LG</td><td>설명 방법을 예측기로 복원 가능한지로 평가하는 XAI 기준. 로보틱스와 무관함.</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2609.20129'>Local Sparsity Enables Unsupervised LLM Safety Detection</a></td><td>15</td><td>0</td><td>LG</td><td>sparse autoencoder 국소성 기반 unsupervised LLM safety 탐지. 로보틱스와 무관함.</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2609.20199'>Towards a Unified Modality-Agnostic Multimodal Framework for Cognitive Workload Assessment</a></td><td>15</td><td>0</td><td>Multimodal</td><td>생체신호 5종 조합을 다루는 modality-agnostic transformer로 인지 부하를 평가. HCI 도메인으로 로보틱스와 직접 관련 없음.</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2609.20419'>SCGFM-ART: Amortized Relational Transport for Structure-Centric Graph Foundation Models</a></td><td>15</td><td>0</td><td>LG</td><td>이종 그래프를 공유 relational atlas로 정렬하는 amortized transport 기반 graph foundation model. 그래프 분류 벤치마크 중심으로 로보틱스와 무관함.</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2609.20548'>Mitigating Retaliatory Algorithmic Collusion in Repeated Games</a></td><td>15</td><td>0</td><td>RL</td><td>penal code 이론과 Q-learning collusion을 연결해 보복적 담합을 완화하는 reward shaping. 시장 설계 응용으로 로보틱스와 무관함.</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2609.20808'>Unifying Models of Intergroup Hostility in Online Discourse</a></td><td>15</td><td>0</td><td>NLP</td><td>온라인 담론의 적대적 수사를 6개 이론으로 통합 분석한 사회과학 연구로 robotics 무관함</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2609.19513'>QVAC Genesis III: A Large-Scale, High-Quality Open Synthetic STEM Corpus for Efficient Language Model Pre-Training</a></td><td>15</td><td>0</td><td>NLP</td><td>edge용 소형 모델을 위한 STEM 합성 코퍼스 구축 논문으로 robotics 무관함</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2609.19524'>A Unified Evaluation Framework for Trustworthy Large Language Models, Agentic AI, and Multimodal Systems</a></td><td>15</td><td>0</td><td>AI</td><td>LLM·에이전트·멀티모달을 아우르는 신뢰성 평가 프레임워크 제안이나 실증 검증은 향후 과제로 남아있고 robotics 무관함</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2609.19530'>When Hiring Becomes Agent-Mediated: Evaluating Access and Recurrence in Two-Agent Résumé Screening</a></td><td>15</td><td>0</td><td>NLP</td><td>이력서 심사를 양방향 에이전트로 바꿨을 때 합격률과 재현성이 어떻게 변하는지 측정한 연구로 robotics 무관함</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2609.19680'>FINSKILLOPS: A Self-Evolving Multi-Agent System for SEC Filing QA</a></td><td>15</td><td>0</td><td>NLP</td><td>SEC 공시 QA용 self-evolving 멀티에이전트 시스템으로 robotics 무관함</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2609.19721'>LearnActCoder: Role-Aware Error Memory for Adaptive Clinical Coding Agents</a></td><td>15</td><td>0</td><td>NLP</td><td>임상 코딩 에이전트에 오류 메모리를 추가한 연구로 robotics 무관함</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2609.19848'>Constraint-Safe Graph-Context Scoring for Stable Point-Feature Labels Under Text-Width and Accessibility-Inspired Profiles</a></td><td>15</td><td>0</td><td>CV</td><td>지도 라벨 배치 최적화 프로토타입으로 cs.RO 태그가 있으나 실제로는 지도 렌더링 UI 문제임</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2609.20080'>A Proposal for an Agentic AI Architecture to Support Multi-Domain Decision-Making in the Brazilian Armed Forces</a></td><td>15</td><td>0</td><td>AI</td><td>다영역 지휘통제를 위한 에이전트 아키텍처 제안이며 구현·실험 없는 개념 논문으로 robotics 무관함</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2609.20177'>PaGNet: A Panel-Aware GBDT--Neural Network for Multi-Target Corporate Tax Avoidance Proxy Forecasting</a></td><td>15</td><td>0</td><td>LG</td><td>기업 조세회피 프록시를 예측하는 GBDT-신경망 하이브리드로 robotics 무관함</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2609.20334'>Structured Four-Stage Legal Translation: From Natural-Language Traffic Rules to PROLOG</a></td><td>15</td><td>0</td><td>NLP</td><td>교통법규를 4단계로 나눠 PROLOG로 번역하는 프레임워크로 robotics 무관함</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2609.20732'>Q&amp;A on Any Spreadsheet Requires Interpreting Its Grid Structure</a></td><td>15</td><td>0</td><td>NLP</td><td>스프레드시트를 셀 역할로 청킹해 RAG에 넣는 방법의 한계를 보이고 2D를 1D로 축소해야 한다고 주장한 연구로 robotics 무관함</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2609.19695'>Opinion Dynamics-based Coalition Formation for Federated Learning in Heterogeneous IoT Systems</a></td><td>14</td><td>0</td><td>LG</td><td>federated learning coalition 형성 기법의 점진적 개선. 로봇·embodied AI와 무관함.</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2609.19842'>Beyond Flattened Tokens: Structure-Preserving EEG Decoding with Reusable TriDim Blocks</a></td><td>14</td><td>0</td><td>LG</td><td>EEG 디코딩을 위한 축별 attention block. 응용이 BCI로 로보틱스와 무관함.</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2609.19970'>CellRFT: Reinforcement Fine-Tuning for Single-Cell Perturbation Modeling</a></td><td>14</td><td>0</td><td>LG</td><td>단일세포 섭동 예측에 policy-gradient 기반 reinforcement fine-tuning을 적용. 생물학 도메인으로 로보틱스와 무관함.</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2609.20008'>Dynamic Generalized Gromov-Wasserstein Optimal Transport</a></td><td>14</td><td>0</td><td>LG</td><td>spatial transcriptomics를 위한 dynamic Gromov-Wasserstein OT 프레임워크. 로보틱스와 무관함.</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2609.19238'>YNU-HPCC at SemEval-2025 Task 11: Bridging the Gap in Text-Based Emotion Using Multiple Prediction Headers</a></td><td>14</td><td>0</td><td>NLP</td><td>SemEval-2025 감정인식 task 참가보고서임. 헤드 구조를 단순화한 정도의 기여로 연구적 새로움은 낮음.</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2609.20064'>A Free Lunch? Adapting PP-OCRv6 for Historical Text Recognition</a></td><td>12</td><td>0</td><td>NLP</td><td>역사 문헌 인식을 위한 compact OCR 모델 적응 연구로 로봇과 무관함</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2609.20222'>A Two-Stage Multi-Scale Attention-Based Network for Weakly Supervised Cataract Fundus Image Enhancement</a></td><td>12</td><td>0</td><td>CV</td><td>백내장 안저영상 enhancement를 위한 weakly supervised 2단계 네트워크로 의료 영상 응용이고 로봇과 무관함</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2609.20341'>Fast Cross-Strength Multi-Contrast Brain MRI Translation using Latent Bridge Matching</a></td><td>12</td><td>0</td><td>CV</td><td>필드 강도 간 뇌 MRI 변환을 위한 latent bridge matching 모델로 로봇과 무관함</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2609.19748'>Alliance Beats Isolation: Unifying Heterogeneous Allied Datasets Improves Classifier Performance</a></td><td>12</td><td>0</td><td>LG</td><td>이종 feature space를 가진 데이터셋을 matrix completion으로 통합하는 기법. 단순 분류 성능 개선 위주임.</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2609.19776'>PhyRestore: Physics-Structured Latent-Factor Restoration</a></td><td>12</td><td>0</td><td>LG</td><td>토양 유실 추정을 위한 physics-structured latent factor 복원 기법. 응용 도메인이 협소함.</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2609.19786'>Learning-Based Reconstruction of Optical Properties in Bilayered Media from Single-distance Time-Resolved Reflectance Measurements</a></td><td>12</td><td>0</td><td>LG</td><td>생체 조직 광학 특성 추정에 ML을 적용한 연구. 로보틱스와 무관한 응용임.</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2609.20086'>SETTer: Sparse-Encoder Transformer for Long-term Multivariate Time Series Forecasting</a></td><td>12</td><td>0</td><td>LG</td><td>장기 다변량 시계열 예측을 위한 sparse encoder transformer. 순수 forecasting 성능 개선임.</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2609.20123'>QoS-Aware Federated Learning for Multimodal In-Cabin Interaction in Smart Vehicles</a></td><td>12</td><td>0</td><td>LG</td><td>차량 내 멀티모달 상호작용을 위한 QoS-aware federated learning. 통신 효율화가 핵심으로 로보틱스와 무관함.</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2609.20156'>QUALS: Corpus Equilibrium for Universal Forecasting via Pattern Quantization and Learnability Synchronization</a></td><td>12</td><td>0</td><td>LG</td><td>foundation time series model의 데이터 샘플링 효율화 기법. forecasting 특화로 로보틱스와 무관함.</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2609.20217'>Explaining spatial information flow in short-term traffic forecasting models using a gated graph attention network</a></td><td>12</td><td>0</td><td>LG</td><td>graph attention network에 gate를 추가해 교통 예측의 spatial 정보 흐름을 설명. 로보틱스와 무관함.</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2609.20218'>Is It Still Worth Training a Classical Model in the Era of LLMs? A Crossover Benchmark on Tabular Data</a></td><td>12</td><td>0</td><td>LG</td><td>tabular 데이터에서 LLM 프롬프팅 대비 classical model 학습이 우위인 지점을 분석. 비즈니스 ML로 로보틱스와 무관함.</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2609.20310'>ZeroHAT: Behavior-Conditioned Zero-Shot Human Activity Trace Generation</a></td><td>12</td><td>0</td><td>LG</td><td>타 지역 행동 패턴을 전이해 zero-shot으로 인간 활동 궤적을 생성. 도시 모빌리티 응용으로 로보틱스와 무관함.</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2609.20404'>Learning Principal-Agent Contracts for Equitable Smallholder Carbon Farming under Moral Hazard and Adverse Selection</a></td><td>12</td><td>0</td><td>RL</td><td>탄소농업 계약설계를 POMDP와 RL로 최적화. 정책·경제 응용으로 로보틱스와 무관함.</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2609.20592'>CrystalMO-TuRBO: Multi-Objective Trust-Region Bayesian Optimization for High-precision Joint Crystal Structure Refinement</a></td><td>12</td><td>0</td><td>LG</td><td>X선·중성자 결정구조 정제를 위한 multi-objective trust-region Bayesian optimization. 재료과학 응용으로 로보틱스와 무관함.</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2609.20598'>COIN-GP: Cooperative Online Learning in Networked Distributed Systems with Partial Measurements via Gaussian Process Regression</a></td><td>12</td><td>0</td><td>LG</td><td>부분 관측 분산 센서망에서 observer 기반 협력 Gaussian Process 학습. 이론 중심으로 로봇 응용 사례는 없음.</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2609.20712'>Summarization Bias: The Directional Collapse of Objective Projection into Told-Mode Labels in Large Language Models --- A Conceptual Framework and Registered Test Protocol</a></td><td>12</td><td>0</td><td>NLP</td><td>LLM이 told-mode로 몰린다는 가설만 세우고 사전등록 단계에 머문 미검증 논문임</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2609.20057'>WiCleanData: Guaranteeing the Type Consistency of Wikidata by Taxonomy Refinement and Constraint Enforcement</a></td><td>12</td><td>0</td><td>NLP</td><td>Wikidata 택소노미 정제 파이프라인으로 robotics 무관함</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2609.20068'>Marginal utility, matrix factorization, and the Key-Value (KV) cache: a unified information-economic framework for sovereign geo-mining inference</a></td><td>12</td><td>0</td><td>LG</td><td>경제학의 한계효용과 matrix factorization, KV cache를 하나의 틀로 엮었다고 주장하며 지질 탐사 문서 추출에 적용했는데 핵심 실험이 아직 projection 단계로 측정되지 않아 신뢰도가 낮음</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2609.19840'>KoUniTalk: A Lightweight Articulation-Centered Korean-English 3D Talking Face Benchmark</a></td><td>10</td><td>0</td><td>CV</td><td>한국어-영어 3D talking face 벤치마크로 로봇과 무관함</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2609.20290'>TinyCNN: A 193K-Parameter Network for On-Device Plant Disease Detection, with a Cross-Dataset Robustness Diagnosis</a></td><td>10</td><td>0</td><td>CV</td><td>193K 파라미터 식물병 탐지 경량 CNN으로 efficiency 중심이고 로봇과 무관함</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2609.20386'>Compact Vision Models for Iris Presentation Attack Detection under Presentation Attack Instrument Shift and Environmental Degradation</a></td><td>10</td><td>0</td><td>CV</td><td>홍채 presentation attack 탐지용 경량 모델 비교 연구로 로봇과 무관함</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2609.20509'>Automated Goldsmith&#x27;s Mark Retrieval in Silverware</a></td><td>10</td><td>0</td><td>CV</td><td>은세공 마크 검색을 위한 metric learning 파이프라인으로 로봇과 무관함</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2609.20815'>ERCPMP-Gx: Endoscopic Image and Video Dataset for Morphological, Histopathological, and Genomic Characterization of Colorectal Polyposis</a></td><td>10</td><td>0</td><td>CV</td><td>유전성 용종증의 내시경·병리·유전체 통합 데이터셋으로 로봇과 무관함</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2609.19243'>Randomized SVD Approximations for Spectral Co-Clustering of Word-Document Matrices</a></td><td>10</td><td>0</td><td>LG</td><td>단어-문서 행렬 spectral co-clustering의 randomized SVD 근사 비교 연구로 로봇과 무관함</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2609.19374'>Machine-Learning Assessment of the Predictive Value of Inflammatory Biomarkers for Cognitive Impairment in an Older Hispanic Adult Cohort</a></td><td>10</td><td>0</td><td>LG</td><td>히스패닉 노인 코호트에서 염증 biomarker로 인지장애를 예측하는 해석가능 모델 연구로 로봇과 무관함</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2609.19466'>Enhanced Agriculture-informed Neural Network by Domain Knowledge</a></td><td>10</td><td>0</td><td>LG</td><td>농업 도메인 지식을 결합한 N2O 배출 예측 신경망으로 로봇과 무관함</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2609.19640'>A Policy Profile for Croissant: Refusal as a Property of the Dataset</a></td><td>10</td><td>0</td><td>LG</td><td>ML 데이터셋 메타데이터 표준인 Croissant에 거부 정책 평가 semantics를 추가한 연구로 로봇과 무관함</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2609.19865'>Pretrained Medical Representations for the Practical Screening of Drug Repositioning Candidates</a></td><td>10</td><td>0</td><td>LG</td><td>의료 코드 표현학습 기반 약물 재창출 스크리닝. 로보틱스와 무관함.</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2609.19913'>Digital Twins for Opinion Dynamics: A Generative LLM Framework for Social Networks</a></td><td>10</td><td>0</td><td>LG</td><td>트위터 여론 역학을 LLM 기반 digital twin으로 재현하는 연구. 로보틱스와 무관함.</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2609.20138'>Fast-varying Natural Frequencies and Damping Ratio Identification for Linear Time-Varying System</a></td><td>10</td><td>0</td><td>LG</td><td>풍력터빈 시변 고유진동수 추정을 위한 물리 결합 LSTM-EKF. 도메인 특화로 로보틱스와 무관함.</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2609.20171'>Support Thresholds, Not Algorithms, Limit Rare-Association Recovery in Co-Purchase Networks</a></td><td>10</td><td>0</td><td>LG</td><td>장바구니 분석에서 support threshold 대신 통계적 유의성 필터링을 비교. 로보틱스와 무관함.</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2609.20194'>SoftTri: Smooth Triangular Membership Functions for Adaptive Fuzzy Inference Systems</a></td><td>10</td><td>0</td><td>LG</td><td>미분 가능한 부드러운 삼각형 소속함수로 fuzzy 신경망을 개선. 로보틱스와 무관함.</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2609.20209'>Scene-Conditioned Relation Routing for urban cellular activity forecasting</a></td><td>10</td><td>0</td><td>LG</td><td>도시 셀룰러 트래픽 예측을 위한 scene-conditioned routing 기법. 로보틱스와 무관함.</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2609.20213'>Subdomain-aware representation compression for pretrained image embeddings</a></td><td>10</td><td>0</td><td>CV</td><td>사전학습 이미지 임베딩의 서브도메인별 차원 축소. 경량화 중심으로 우선 평가 대상이 아님.</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2609.20249'>Accuracy Is Not Enough: A Cross-Architecture Audit of Demographic Bias in Deep Knowledge Tracing</a></td><td>10</td><td>0</td><td>LG</td><td>deep knowledge tracing 아키텍처별 인구통계 편향을 감사. 교육 도메인으로 로보틱스와 무관함.</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2609.20298'>A Learning Algorithm for Threshold Boolean Networks with Prescribed Fixed Points</a></td><td>10</td><td>0</td><td>LG</td><td>지정된 fixed point를 갖는 threshold Boolean network 학습 알고리즘. 생물학적 네트워크 추론으로 로보틱스와 무관함.</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2609.20353'>Minimax-Optimal Online Contract Design with Unrestricted Bounded Contracts</a></td><td>10</td><td>0</td><td>LG</td><td>관측 불가능한 행동에 대한 online contract design의 minimax regret 분석. 로보틱스와 무관함.</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2609.20451'>Seismic Site Response Prediction from Sparse Observations Using Finite-Element-Pretrained Latent Dynamics</a></td><td>10</td><td>0</td><td>LG</td><td>지진 사이트 응답 예측을 위한 latent dynamics 보정 기법. 토목 응용으로 로보틱스와 무관함.</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2609.20465'>Training Neural Networks to Approach the Optimum Bayes Estimator in Dense Multi-Emitter Localization</a></td><td>10</td><td>0</td><td>LG</td><td>밀집 emitter 위치추정에서 베이즈 최적 추정기에 근접하는 신경망 학습. 현미경 응용으로 로보틱스와 무관함.</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2609.20467'>Deep Learning-Based Classification of Cognitive and Resting States Using Electroencephalography Signals</a></td><td>10</td><td>0</td><td>LG</td><td>EEG로 인지·휴식 상태를 분류하는 CNN-GRU 모델. BCI 응용으로 로보틱스와 무관함.</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2609.20501'>Distributionally Robust Federated Learning with Multi-Source Data</a></td><td>10</td><td>0</td><td>LG</td><td>다중 소스 federated learning의 분포 강건성 이론. 로보틱스와 무관함.</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2609.20650'>Multi-center Medical Data Mining with FL-Net - A One-stop Shop for Federated Learning</a></td><td>10</td><td>0</td><td>LG</td><td>다기관 임상 연구를 위한 federated learning 프레임워크 통합 도구. 인프라 논문으로 로보틱스와 무관함.</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2609.20677'>RISC-V and machine learning: a survey</a></td><td>10</td><td>0</td><td>LG</td><td>RISC-V 기반 ML 하드웨어 서베이. 경량화·하드웨어 리뷰로 우선 평가 대상이 아님.</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2609.20765'>Calibrated RF-Fingerprinting Under Interference With Heterogeneous Transmission Protocols</a></td><td>10</td><td>0</td><td>LG</td><td>co-channel 간섭 상황에서 RF fingerprinting으로 다중 송신기를 식별. 무선 통신 응용으로 로보틱스와 무관함.</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2609.19873'>AURA: Adaptive Uncertainty-Routed Analysis for Email Threat Detection</a></td><td>8</td><td>0</td><td>LG</td><td>이메일 피싱 탐지를 위한 불확실성 기반 라우팅 시스템. 도메인이 로보틱스와 무관함.</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2609.20198'>Evaluating Financial Sentiment in the Age of AI</a></td><td>8</td><td>0</td><td>NLP</td><td>금융 감성 분석에서 LLM과 특화 모델을 비교. 로보틱스와 무관함.</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2609.20250'>How Far Can Sub-3B Open Language Models Go in Zero-Shot Essay Scoring on an 8 GB Consumer GPU?</a></td><td>8</td><td>0</td><td>NLP</td><td>8GB GPU에서 sub-3B LLM의 에세이 채점 능력을 평가. 로보틱스와 무관함.</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2609.20313'>EviRec: Continual Evidence Learning for Dual Cold-Start POI Recommendation</a></td><td>8</td><td>0</td><td>LG</td><td>POI 추천에서 candidate별 신뢰도를 학습하는 continual cold-start 기법. 추천시스템 응용으로 로보틱스와 무관함.</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2609.20507'>Radio Frequency Detection and Classification of Microplastics in Water</a></td><td>8</td><td>0</td><td>LG</td><td>RF 유전 분광으로 물속 미세플라스틱을 분류. 환경 센싱 응용으로 로보틱스와 무관함.</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2609.20594'>Recursive Quantum Long Short-Term Memory for Stable Short-Horizon Temperature Forecasting</a></td><td>8</td><td>0</td><td>LG</td><td>재귀 구조의 quantum LSTM으로 단기 기온 예측 안정성을 개선. 니치 응용으로 로보틱스와 무관함.</td></tr>
</tbody></table>

</details>
