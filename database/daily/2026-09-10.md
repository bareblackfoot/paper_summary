# 오늘의 arXiv Top 15 — 2026-09-10 (목)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**
> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)

**신규 논문 수: 전체 316편 → 중복 제거 후 316편 (이번 평가 대상 316편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 80 |
| cs.LG | 79 |
| cs.RO | 42 |
| cs.CL | 64 |
| cs.AI | 51 |

*1차 스크리닝: 전체 316편을 제목/초록 기반으로 채점(Claude (scheduled agent)) → 상위 15편은 arXiv 원문을 내려받아 정밀 리뷰(Claude (scheduled agent)) 후 최종 점수 산정.*

---

## Top 15

### 1. [72점] Programmable World Model

- **분야**: World Model · **robotics relevance**: 6/10
- **arXiv**: [2609.10540](https://arxiv.org/abs/2609.10540) ([PDF](https://arxiv.org/pdf/2609.10540))
- **저자**: Zheng-Hui Huang, Guixu Lin, Jiacheng Lin, Yi-Chuan Huang, Ruihan Yu, Muyao Niu, Siqi Yang, Yu-Lun Liu 외 3명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: Homepage: this https URL GitHub: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 60점

> 💡 비디오 월드모델이 지속적인 world state를 기억하지 못한다는 문제에서 출발해, 자연어 지시를 실행가능한 프로그램으로 변환해 state를 explicit engine으로 관리하고 이를 3D bounding box(OBB) 기반 조건 신호로 압축해 영상 생성기에 넣는 Programmable World Model을 제안함. 자체 제작한 CombatStateBench에서 Count Accuracy 94%, State Accuracy 98%로 기존 interactive video world model들을 크게 앞섬.

**Core innovation & methodology**

- world-state evolution을 explicit engine으로 분리하고 video model은 그 state를 조건으로 받아 렌더링만 담당하도록 문제를 재정의함
- 자연어 지시를 coding agent가 entity state·transition rule을 담은 실행가능한 world program으로 변환하고, lightweight engine이 이를 실행해 canonical state를 관리함
- state-augmented 3D oriented bounding box(OBB)를 world state와 visual generation을 잇는 중간 표현으로 도입, deterministic state compiler가 target camera 궤적에 맞춰 pixel-aligned identity/semantic/direction map으로 컴파일함
- 사전학습된 camera-controlled video model(LingBot-World-v1)에 trainable Structured Spatial ControlNet을 붙이고, chunk-autoregressive 방식과 geometry-aligned spatial memory로 long-horizon rendering을 지원함

**Novelty vs. prior works**

- 비교 대상인 StatePlay는 state 자체를 모델이 예측해 오차가 누적될 수 있는데, 본 논문은 state transition을 학습된 예측이 아니라 프로그램된 규칙으로 결정론적으로 실행해 오차 누적 문제를 구조적으로 피함
- MASS도 authoritative shared state를 두지만 transition은 learned Logic Engine이 담당하는 반면, 본 논문은 transition 자체를 rule engine이 담당해 상태 진화를 검증 가능하게 만든 점이 본질적 차이임
- representation 선택을 training-inference asymmetry로 분석하고 OBB를 중간 지점으로 정당화한 논리는 설득력 있으나, OBB 자체는 기존 3D detection 표현의 재활용이라 표현 방식 자체의 새로움은 제한적임

**Benchmark results**

- 자체 제작 CombatStateBench(50 clip)에서 Count Accuracy 94.00%, State Accuracy 98.00%로 LingBot-World-V2(40.75%, 8.00%)와 YUME(32.00%, 58.00%)를 큰 차이로 앞섬
- VBench 기반 Imaging Quality·Subject Consistency·Background Consistency·Temporal Stability 네 지표 모두 최고치를 기록했으나 Imaging Quality는 67.62 vs 67.46으로 baseline과 거의 차이 없음
- 비교 baseline들은 instance-level state interface가 없어 prompt switching으로만 state를 전달했다는 한계가 있어, 비교 자체가 본 논문에 유리하게 설계됐을 가능성이 있음
- Cyberpunk 2077·Forza Horizon 6·GTA V 게임 영상으로만 학습·평가한 sim/게임 전용 설정이며 실로봇 검증은 없음, 코드와 프로젝트 페이지는 공개됨
- 정량적 ablation 표는 없고 Figure 4, 5의 정성적 비교로만 기여도를 제시해 각 구성요소(identity/semantic/direction map)의 개별 효과는 확인 불가

**Top-tier conference 적합성 — 66/100 · 추천 venue: CVPR**

world-state와 visual generation을 분리한다는 problem formulation이 명확하고 자체 벤치마크에서 개선폭이 크다는 점은 강점임. 다만 벤치마크가 자체 제작 50 clip에 그치고 baseline이 state interface 없이 비교됐다는 점, real-robot이나 물리적 상호작용 검증이 전혀 없다는 점이 rejection risk이며 video generation 커뮤니티(CVPR/SIGGRAPH 계열) 적합도가 embodied AI 커뮤니티보다 높음.

**추천 이유 & 누리랩 연구와의 연결점**

- world state를 explicit rule engine으로 분리하는 아이디어는 robot manipulation에서 task progress·inventory 같은 symbolic state 관리와 failure detection 시 state mismatch 검증 신호로 응용 가능함
- entity를 persistent OBB와 attribute로 관리하는 방식은 scene graph/semantic mapping의 node 표현과 맞닿아 있어, object-centric 3DGS 연구와 결합해볼 수 있음
- rule engine이 state transition을 결정론적으로 실행한다는 점은 counterfactual reasoning 기반 test-time planning에서 특정 action이 world state에 미치는 영향을 시뮬레이션하는 데 아이디어를 빌릴 수 있음

---

### 2. [70점] Show-Harness: Just a VLM Agent Can Play Robots

- **분야**: VLA / Embodied AI · **robotics relevance**: 9/10
- **arXiv**: [2609.10522](https://arxiv.org/abs/2609.10522) ([PDF](https://arxiv.org/pdf/2609.10522))
- **저자**: Yanzhe Chen, Zechen Bai, Zhijun Cao, Wenzheng Zeng, Kevin Qinghong Lin, Yiqi Lin, Guoqiang Liang, Kevin Yuchen Ma 외 2명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Project website: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 54점

> 💡 VLM이 로봇을 직접 제어하도록 방향·회전·grasp 단위의 이산 semantic action 어휘와 embodiment별 결정론적 interpreter로 구성된 Show-Harness를 제안함. 같은 인터페이스로 closed-source VLM은 zero-shot, 2B급 open VLM은 몇 GPU-hour LoRA로 로봇을 조작하며 VLA·agent baseline 대비 일관되게 높은 성공률을 보임.

**Core innovation & methodology**

- VLM에 노출되는 action space를 8개 이산 semantic unit(MV_*, ROTATE_*, GRASP/RELEASE, DONE)으로 제한해 VLM이 native vocabulary로 직접 예측하게 함. ablation상 성능을 견인하는 건 이 이산 convention 자체이고 semantic 이름은 보조적 요인임.
- embodiment별 interpreter가 semantic unit을 6-DoF Cartesian pose delta로 결정론적으로 변환해, VLM이 fine-grained 물리 결정에 계속 책임을 지게 함.
- perceive-reason-act 3단계 harness에 subtask planning, situated planning, action chunking, adaptive step, failure recovery 등 plugin을 붙여 closed-loop 실행을 구성함.
- 같은 semantic action space를 GUI 조작(GUMI)에도 노출해 사람·VLM 모두 teleoperation 하드웨어 없이 시연 데이터를 모으게 함.

**Novelty vs. prior works**

- 기존 VLA는 VLM을 continuous/discretized low-level action에 fine-tuning해 semantic 지식을 opaque mapping으로 무너뜨리고, 기존 agentic 시스템은 VLM이 상위 결정만 하고 실제 물리 실행은 불투명한 하위 컨트롤러에 맡김.
- Show-Harness는 VLM이 fine-grained 물리 결정을 직접 내리되 표현은 여전히 이산 semantic 단위라는 점에서 두 극단의 중간을 채움.
- action space 표현 ablation에서 성능을 견인하는 건 명시적 convention이고 semantic 이름 자체는 보조적 prior에 가까워, 이름 자체의 의미가 핵심이라는 주장을 스스로 제한함.

**Benchmark results**

- 10개 real-robot task 평균 성공률은 ZS 89%, FT 86%로 baseline 최고인 RATS 57.0%, π0.5 39.0%, GR00T 35.0%를 크게 상회함.
- cross-environment(배경·조명·시점·방해물·sim-to-real) 평균은 ZS 100%, FT 88%인데, π0.5·GR00T는 sim-to-real에서 20회 모두 실패(0/20)함.
- cross-embodiment(Franka·AgileX)에서 ZS 93%, FT 87%로 baseline 최고인 RATS 52%를 상회함.
- interpreter step을 2cm에서 1cm로 줄이기만 해도 VLM action interface 변경이나 재훈련 없이 ZS는 60%에서 82%, FT는 40%에서 65%로 오르지만, π0.5는 같은 FT 시연 데이터로는 18%에 그치고 정밀 동작 전용으로 추가 fine-tuning해야 62%까지 오름.
- 검증 범위는 Franka·AgileX 두 embodiment, parallel-jaw gripper only, task 10종 중심이며 code·모델·데이터셋은 공개하나 humanoid·dexterous hand로는 미검증임.

**Top-tier conference 적합성 — 74/100 · 추천 venue: CoRL**

다수 baseline과 다축 generalization, 세밀한 plugin ablation을 갖춰 로봇학습 학회 기준을 충족함. 다만 frontier VLM(Gemini-3.1 Pro) 의존도가 높고 8개 이산 unit이 고속·정밀 동작으로 확장될 때의 한계는 다루지 않아 그 지점이 reject 위험으로 남음.

**추천 이유 & 누리랩 연구와의 연결점**

- continuous action regression 대신 이산 semantic unit과 deterministic interpreter로 나누는 설계는 누리랩 VLA formulation 논의에서 action tokenization 대안으로 참고할 수 있음.
- Failure Recovery plugin(빈 grasp 감지 후 rollback)은 단순하지만 바로 재현 가능한 실패 복구 baseline으로 쓸 수 있음.
- thinking effort와 backbone 선택에 따른 성능-지연 trade-off 분석은 test-time optimization 연구에 직접 참고 가능함.

---

### 3. [68점] JEPA Policy: Diffusion-Free Imitation Learning via Paired Action and Future Representation Prediction

- **분야**: VLA · **robotics relevance**: 9/10
- **arXiv**: [2609.09630](https://arxiv.org/abs/2609.09630) ([PDF](https://arxiv.org/pdf/2609.09630))
- **저자**: Jie Xu, Kangjin Yu, Ziyi Jin, Junjie Gao, Liqing Chen, Yixian Li, Shuai Tian, Zhongpu Xia
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 17 pages. Code: this https URL . Project page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 58점

> 💡 standard behavior cloning이 action만 supervise하고 그 결과 도달하는 미래 상태는 제약하지 않는다는 문제에서 출발해, action chunk와 관찰된 미래 표현을 하나의 shared Transformer에서 함께 예측하는 diffusion-free JEPA Policy를 제안함. 9개 시뮬레이션 task에서 action-only MIP 대비 평균 성공률 5.6점 개선했고 Diffusion Policy 대비로도 전 task에서 앞섰으며, 5-task 630-episode 실로봇 실험에서도 같은 순위를 재현함.

**Core innovation & methodology**

- action chunk와 demonstration에서 관찰된 미래 표현(future representation)을 짝지어 하나의 shared Transformer에 넣고 매 self-attention layer에서 상호작용하게 해 future 예측이 action 표현을 직접 형성하도록 설계함
- minimal iterative policy(MIP)의 coarse-to-refined 2-step 방식을 action과 future representation 예측에 동시에 확장해, diffusion 없이 두 번의 forward pass만으로 추론함
- future target은 pixel 재구성이 아니라 같은 encoder에서 얻은 latent이며 stop-gradient만 적용하고, EMA/frozen target encoder나 variance-covariance regularizer 없이 action loss 자체를 collapse 방지 제약으로 사용함
- 배포 시 예측된 미래 표현과 실제 실행 후 관찰된 미래 표현의 차이(future-consistency error)를 rollout-level 진단 신호로 제공함

**Novelty vs. prior works**

- 가장 가까운 ACT-JEPA는 context encoder는 공유하지만 predictor·decoder가 분리된 두 branch라 attention 상호작용이 없고 EMA target encoder로 collapse를 막는데, 본 논문은 이를 하나의 attention stack으로 합치고 EMA 없이 action loss만으로 collapse를 막는다는 구조적 차이를 Dual-independent·Dual-cross ablation으로 직접 검증함
- VLA-JEPA, JEPA-VLA는 사전학습 VLM·video representation을 활용하는 반면 본 논문은 encoder를 처음부터 task demonstration만으로 학습해 사전학습 표현의 기여를 배제하고 topology 효과만 분리했는데, 그만큼 대규모 VLA 백본 스케일로의 일반화는 검증되지 않음
- future-consistency error를 failure diagnostic으로 쓰는 아이디어는 Sentinel, FAIL-Detect 같은 기존 runtime monitoring 연구와 유사한 문제를 다루지만, 학습 목적함수의 부산물로 얻는다는 실용성이 있는 대신 저자도 task별로 calibrate해야 하는 좁은 범위의 신호라고 인정함

**Benchmark results**

- LIBERO·robomimic·MimicGen 9개 task, 3 seed 평균에서 9-task 평균 성공률 83.0%로 action-only MIP(77.4%) 대비 +5.6점, 9개 task 전부 양의 개선이며 sign test p=0.0039
- Diffusion Policy(10-step) 대비 9개 task 전부 우위이나 Tool Hang(75.0% vs 46.7%)이 격차의 상당 부분을 차지해 이 task를 빼면 평균 차이는 +5.4점으로 줄어듦
- shared-attention topology 자체가 기여의 핵심임을 보이는 ablation에서, 같은 future loss를 분리된 branch(Dual-independent 76.3%, Dual-cross 77.6%)로 넣으면 MIP 대비 이득이 거의 사라짐
- 실로봇 5-task 630-episode 실험에서 Diffusion Policy 대비 30개 중 29개 checkpoint-task 조합에서 우위(p≈1.22e-4)이나, MIP 대비는 15개 중 9승 4패 2무로 방향성만 있고 통계적으로 유의하지 않음(p=0.27)
- decision latency는 MIP 대비 0.29ms(2.2%) 추가에 그쳐 13.2ms로 Diffusion Policy(439.5ms) 대비 33배 빠르나, 실험 전체가 ResNet-18/DINOv2 기반 소규모 encoder 세팅이고 대규모 VLA 백본에서의 검증은 없음

**Top-tier conference 적합성 — 65/100 · 추천 venue: CoRL**

topology 통제 ablation, collapse audit, 통계 검정, 실로봇 검증까지 갖춘 실험적 엄밀성이 강점이라 CoRL·RSS 심사에서 설득력이 있음. 다만 JEPA 기반 imitation learning 자체는 ACT-JEPA·VLA-JEPA·JEPA-VLA 등 동시 연구가 다수라 개념적 새로움보다 구조 비교의 엄밀함이 기여 중심이고, 실로봇에서 MIP 대비 우위가 통계적으로 유의하지 않다는 점이 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- future-consistency error를 이용한 rollout-level 진단 신호는 failure detection/recovery 연구에 바로 붙일 수 있고, task-conditioned threshold를 학습해 실패 예측 성능을 높이는 후속 실험이 가능함
- shared attention을 통해 future 예측이 action 표현을 형성한다는 결과는 world model 예측과 policy를 분리하지 않고 하나의 표현으로 묶는 설계로, test-time optimization에서 future prediction error를 보고 action을 온라인으로 재조정하는 방향에 활용 가능함
- diffusion-free 2-step 구조라 low-latency가 필요한 robot memory·실시간 replanning 세팅에 적합하며, 다른 action을 가정했을 때의 future representation 차이를 보는 counterfactual reasoning 확장도 가능함

---

### 4. [66점] Time-Frequency Geometric Cross-Attention for Chunked Vision-Language-Action Models

- **분야**: VLA · **robotics relevance**: 9/10
- **arXiv**: [2609.09925](https://arxiv.org/abs/2609.09925) ([PDF](https://arxiv.org/pdf/2609.09925))
- **저자**: Shengye Dong, Haochen Niu, Hao Liu, Peiwen Lin, Chuang Wang, Shanmin Pang
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 action chunk를 시간-주파수로 분해하고 dot product와 wedge product를 함께 쓰는 cross-attention 모듈 TFGCA를 제안함. 기존 VLA(π0.5)에 drop-in으로 붙여 LIBERO·LIBERO-Plus·RoboTwin·실로봇 AgiBot A2에서 일관되게, 특히 분포 밖(OOD) 조건에서 크게 성능을 올림.

**Core innovation & methodology**

- action chunk 안에서 reach·contact·grasp 같은 단계별 움직임이 표현 공간에서 서로 거의 직교(near-orthogonal)한다는 관찰에서 출발함(TO-DoL: 단계별 action의 시간-직교성을 재는 저자 정의 지표).
- dot product attention은 정렬(similarity)만 보고 직교 관계에는 둔감하다는 한계를 지적하고, wedge product 크기(∥q∧k∥² = ∥q∥²∥k∥² − (q⊤k)²)를 추가 점수 채널로 씀.
- action을 per-dimension learnable stationary wavelet transform(SWT)으로 분해해 시간-주파수 토큰을 만들고, 시간 토큰이 이 토큰들을 dot+wedge 블렌드로 조회함.
- 출력 projection을 0으로 초기화해 초기 상태에서는 base 모델과 동일하게 동작하도록 설계, 사전학습된 VLA에 이어 붙여 fine-tune 가능함.

**Novelty vs. prior works**

- frequency decomposition(Autoformer, FEDformer, SimpleTM)과 geometric attention(Geometric Algebra Transformer)은 시계열 예측에서 이미 쓰이던 기법이고, 이를 VLA action chunk에 처음 결합한 응용 성격이 강함.
- FAST(DCT 기반 action tokenization)와 달리 frequency를 압축·토큰화가 아니라 연속적 flow-matching attention의 key로 쓴다는 차별점은 있으나, 핵심은 기존 두 아이디어의 재조합임.
- wedge product의 근접-직교 민감성은 이론적으로 증명(Proposition 1)했지만, cross-phase 관계가 실제로 wedge 채널이 잡아내는 방향에 놓인다는 인과적 증거(Q/K routing 분석)는 제시하지 못하고 향후 과제로 남김.

**Benchmark results**

- LIBERO 4-suite 평균: π0.5 재현 96.7% → TFGCA 98.2% (+1.5pt), 이미 거의 saturate된 벤치마크라 gap이 작음.
- LIBERO-Plus(7종 OOD perturbation) Total: 66.7% → 73.0% (+6.3pt), Noise·Robot·Camera에서 개선폭이 큼.
- RoboTwin 2.0 domain randomization 6-task 평균: clean +3.7pt, randomized +28.5pt (42.7%, 학습 시 미노출 조건에서 zero-shot 개선).
- 실로봇 AgiBot A2 3개 task, 총 60회 시행: 50.00% → 61.67% (+11.67pt), 티슈 뽑기 task에서 +15pt로 가장 큼.
- component ablation(w/o SWT, w/o geometry, w/o alignment) 모두 제거 시 성능이 하락함. LIBERO에서는 alignment loss가, LIBERO-Plus에서는 geometry(wedge) 채널이 가장 중요해 역전됨.
- 코드·모델 공개 여부는 본문에서 확인 불가.

**Top-tier conference 적합성 — 60/100 · 추천 venue: CoRL**

action chunk 표현에 이론적 근거(Proposition 1)와 4개 벤치마크·실로봇 일관된 개선을 갖춰 CoRL 수준의 견고한 empirical paper로 보임. 다만 핵심 기법이 시계열 예측 분야의 wavelet+geometric attention을 VLA에 재조합한 성격이 강해 conceptual novelty에서 top-tier oral 경쟁력은 약하고, LIBERO 개선폭이 작아 in-distribution에서의 기여는 제한적임.

**추천 이유 & 누리랩 연구와의 연결점**

- action chunk를 시간-주파수로 나누는 아이디어는 failure detection에도 응용 가능함 — 고주파 correction 성분이 비정상적으로 커지는 순간을 접촉 실패나 재시도 신호로 쓸 수 있음.
- chunk 재계획 주기를 frequency 정보로 정하자는 저자들의 future work는 test-time optimization 방향과 직접 연결됨.
- wedge product로 근접-직교 관계를 포착하는 설계는 scene graph에서 서로 다른 물체·관계 임베딩 간 상보성을 다루는 attention에도 적용해볼 만함.

---

### 5. [65점] Semigroup-JEPA: Latent Dynamics Consistency for Zero-Shot Physics Generalization

- **분야**: World Model · **robotics relevance**: 7/10
- **arXiv**: [2609.10464](https://arxiv.org/abs/2609.10464) ([PDF](https://arxiv.org/pdf/2609.10464))
- **저자**: Andy Zeyi Liu, Haoran Sun, Lucas Baker, Randall Balestriero, John Sous
- **카테고리**: Machine Learning (cs.LG) · 신규 목록 게재: cs.LG
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 SG-JEPA는 JEPA world model의 encoder와 predictor를 중력 스칼라로 조건화하고 multi-step autoregressive rollout loss로 함께 학습해 훈련 범위 밖 중력장으로 zero-shot 일반화시킴. DINO-WM 대비 2D open-loop 예측 오차를 최대 2배, 3D 로봇 task의 diffusion policy 제어 성공률을 최대 2.5배 개선함.

**Core innovation & methodology**

- world model에 물리 법칙을 지배하는 파라미터(중력 스칼라)를 action에 concat해 조건화하고, teacher-forcing 대신 H프레임 history에서 K스텝을 재귀적으로 굴리는 rollout loss로 encoder와 predictor를 공동 학습함
- encoder 잠재벡터의 1차원 무작위 투영이 표준 정규분포를 따르도록 규제하는 SIGReg를 함께 적용함
- GRU·SSM·Transformer 세 predictor 변형을 비교하고, action-free trajectory에서 반복 적용되는 update가 이산 semigroup을 이룬다는 점에서 이름을 붙임
- 국소 법칙 오차(local law-conditioned error)와 rollout에 따른 누적 증폭을 분리하는 선형 feature model을 제시하고, encoder·predictor를 교차 재학습하는 실험으로 이득의 원인을 규명함

**Novelty vs. prior works**

- 가장 가까운 prior work인 DINO-WM(고정 DINOv2 encoder + action-conditioned predictor)과 LeWorldModel(one-step teacher-forced loss) 대비, encoder까지 학습하며 multi-step rollout loss로 물리 파라미터의 OOD 일반화를 정면으로 검증한 것이 본질적 차이임
- world model이 실제로 물리 동역학을 학습했는지를 중력이라는 단일 물리 파라미터로 통제된 실험으로 검증하는 problem formulation은 world model 평가 방법론 측면에서 새로운 시도임
- 다만 새로 얹은 것은 기존 JEPA 프레임워크(LeWM)에 gravity conditioning과 rollout loss를 더한 것으로, representation이나 objective 자체의 근본적 신규성은 제한적이고 action-conditioning 방식도 스칼라 하나를 이어붙이는 단순한 형태임

**Benchmark results**

- MuJoCo 8개 데이터셋(2D rigid body freefall 4개, 3D projectile, 로봇팔 제어 3개) 중 6개를 본문 실험에 사용, sim-only이며 real-robot 검증 없음
- 2D square shape 44-step rollout 기준 SG-JEPA(GRU)가 DINO-WM 대비 position·velocity·rotation 오차를 31-48% 감소시킴
- 3D Approach Ball에서 position 오차를 DINO-WM 대비 약 34%, Original LeWM 대비 약 50% 감소시킴
- 제어 task 3개에서 frozen encoder 위에 diffusion policy를 학습, 성공률이 Arm Catcher Ball 9.5%→23.3%, Franka Paddle-to-Basket 27.4%→30.5%, Arm Paddle Ball 17.7%→23.8%로 DINO-WM 대비 개선됨
- ablation에서 encoder를 고정하고 predictor만 새로 학습해도 이득이 유지되고, teacher-forced 단계에서 이미 원거리 OOD 중력값 기준 국소 오차가 약 32% 낮아 이득의 원인이 encoder 표현 학습임을 확인함. triangle rotation 등 일부 지표는 DINO-WM이 근소 우위인 경우도 있음

**Top-tier conference 적합성 — 70/100 · 추천 venue: ICLR**

선형 feature model로 국소 오차와 rollout 증폭을 분리한 이론과, encoder·predictor 교차 재학습 실험으로 이득의 원인을 규명한 점이 결합돼 통찰의 깊이가 있음. 다만 실험이 MuJoCo 시뮬레이션에 한정되고 물리 파라미터가 중력 하나뿐이며 실로봇 검증이 없어 일반화 주장의 외적 타당성이 약함. ICLR·NeurIPS spotlight급은 가능하나 oral 경쟁에는 실증 범위가 부족함.

**추천 이유 & 누리랩 연구와의 연결점**

- world model이 훈련 분포 밖 물리 조건으로 실제 일반화하는지 검증하는 실험 프로토콜(단일 물리 파라미터를 통제 변수로 스윕)은 누리랩 world model 연구의 평가 설계에 참고할 수 있음
- rollout loss가 encoder 표현을 바꾼다는 분석은 policy 실패 원인이 predictor 문제인지 representation 문제인지 가르는 진단법으로 failure detection/recovery 연구에 응용 가능함
- gravity 대신 마찰·질량 등 다른 물리 파라미터나 로봇 매니퓰레이션의 object dynamics로 확장하면 counterfactual reasoning(파라미터를 바꿨을 때 결과가 어떻게 달라지는가) 연구와 직접 연결됨

---

### 6. [65점] Grounding Generated Video Plans in Simulation Towards Versatile Dexterous Controllers

- **분야**: Manipulation / Dexterous Manipulation (Video-conditioned) · **robotics relevance**: 9/10
- **arXiv**: [2609.10050](https://arxiv.org/abs/2609.10050) ([PDF](https://arxiv.org/pdf/2609.10050))
- **저자**: Tianyue Wu, Boyuan An, Shuqi Zhao, Heyu Guo, Wanli Xing, Yi Ma, Kaifeng Zhang, Ruihai Wu 외 1명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Project website: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 58점

> 💡 생성 비디오에서 손-물체(HOI) 궤적을 복원해 시뮬레이션 학습용 참조로 쓰고, 이를 추적하는 RL 컨트롤러 GALATEA를 학습해 배포 시 새 비디오 플랜을 실행함. 시뮬레이션 학습 단계에서 baseline 대비 성공률 25%p 이상 향상했고, 실로봇 미학습 궤적 40개 중 27개에서 성공함.

**Core innovation & methodology**

- 실제 첫 프레임 이미지와 언어로 조건화한 생성 비디오(Seedance 2.0)에서 foundation model perception, 스테레오 depth, joint hand-object optimization을 결합해 손·물체 궤적을 동시에 복원함
- 손가락 단위 동작과 물체 6-DoF 궤적을 함께 grounding해, 물체 궤적만 쓰는 기존 방식과 달리 functional grasp까지 제어함
- contact-aware reward(근접·다중 손가락 접촉·lift reward)와 접근·post-contact 30% reference augmentation, SAPG optimizer로 노이즈 있는 다중 궤적에서도 tracking RL을 안정화함
- object-category expert 정책들을 behavior cloning + DAgger로 단일 controller에 distillation함

**Novelty vs. prior works**

- LVP는 손 동작만, Dex4D는 point track만 추적해 상호작용 전략이 불명확했는데, GALATEA는 손·물체를 함께 복원·추적해 grasp 의도를 보존함
- 소수 모션캡처나 in-the-wild 비디오를 참조로 쓴 기존 line과 달리, 생성 비디오 2500개를 대규모 참조원으로 삼아 노이즈 있는 다중 궤적 학습이 가능함을 실증함
- HOI reconstruction과 tracking RL의 구성 요소 자체는 기존 방법(HOLD, ManipTrans, SAPG)의 재조합에 가까워 새로운 학습 패러다임 제시라기보다는 시스템 통합의 기여가 큼

**Benchmark results**

- HOI reconstruction 인간 평가 480회 중 417회(87%) 1위, mean rank 1.17로 VideoManip(2.16)·DO AS I DO(2.88)·EgoInfinity(3.47)를 상회함
- H2O/HO-Cap ADD-S 4.82cm/3.88cm으로 baseline 대비 최저, 생성 클립 2500개 중 83%가 재구성 품질 기준을 통과함
- 42개 학습 물체 기준 expert 정책 성공률 78.6%(macro mean)이며, distillation 후 미학습 궤적 66.6%·novel object 54.2%로 하락하나 전이가 유지됨
- 10-object benchmark에서 Ours 77.4%(mean)로 ManipTrans·ReGrind·DO AS I DO·PPO 대비 최고, two-stage variant도 ManipTrans 대비 평균 13.2%p 우위
- 실로봇 4개 task(jar pose-adjust, jar grasp-move, mug push/pull)에서 task당 10회씩 총 27/40(67.5%) 성공, 코드·영상 공개됨(sim-to-real gap 존재, contact transition 직후 실패 다수)

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

HOI reconstruction과 tracking RL 양쪽 모두에서 baseline·ablation 비교가 촘촘하고 실로봇 폐루프 검증까지 갖춰 CoRL/RSS 수준의 empirical rigor를 보임. 다만 핵심 구성 요소(joint hand-object optimization, SAPG tracking RL, distillation)가 각각 선행연구의 조합이라 conceptual leap은 제한적이고, in-hand manipulation은 다루지 못해 oral보다는 poster급으로 판단됨.

**추천 이유 & 누리랩 연구와의 연결점**

- 생성 비디오를 시뮬레이션 grounding 참조로 쓰는 파이프라인은 world model 기반 test-time planning 연구에서 참조 궤적 증강 축으로 붙일 수 있음
- HOI joint optimization 구조는 object-centric 3DGS나 scene graph 기반 contact 추론에 재사용 가능함
- 실로봇 실패 사례(contact transition 이탈 후 미복구)는 failure detection/recovery 연구의 test-time recovery 데이터로 활용 가능함

---

### 7. [63점] Assembling Two Parts in One Hand

- **분야**: Dexterous Manipulation · **robotics relevance**: 9/10
- **arXiv**: [2609.10137](https://arxiv.org/abs/2609.10137) ([PDF](https://arxiv.org/pdf/2609.10137))
- **저자**: Liuao Pei, Tianyue Wu, Hui Zhang, Ping Luo, Jie Song
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: To appear on Conference on Robot Learning (CoRL) 2026. Project website: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 55점

> 💡 다섯 손가락 손 하나로 두 부품을 맞추는 in-hand assembly를 관계 목표 자세 기반 RL로 학습함. 손가락 역할 분리 보조 보상과 사람 자세 스냅샷 초기화로 Bottle·Syringe·Marker 세 과제 모두에서 시뮬레이션 정책을 real robot에 zero-shot 전이함.

**Core innovation & methodology**

- 고정구도 제2 arm도 없이 한 손 안에서 두 물체를 정렬하는 in-hand assembly를 POMDP로 정식화함.
- 손가락을 held set(엄지·검지)과 fixed set(중지·약지·소지)으로 나누고 pinch·grasp·pose 품질 신호의 곱으로 보조 보상을 구성함.
- 사람 시연 한 장에서 리타겟팅한 자세로 초기 상태를 만들고 섭동력으로 randomize해 학습 상태 커버리지를 넓힘.
- 관측은 FoundationPose 기반 물체 pose와 proprioception뿐이며, 깊이 일관성 게이트로 손 가림에 의한 추정 오류를 걸러내는 RNN 정책을 씀.

**Novelty vs. prior works**

- 기존 in-hand manipulation은 물체 하나의 회전·이동에 국한되거나 여러 물체를 쥘 때도 손가락을 독립 gripper처럼 나눠 쓰는 수준이라 두 물체 간 능동적 정렬을 다루지 않음.
- 기존 로봇 조립은 거의 전부 parallel-jaw gripper와 고정구·제2 arm을 전제하는데, 이 논문은 그 구조 없이 단일 의인화 손으로 조립을 완결함.
- 방법 자체는 RL·보조 보상·domain randomization이라는 확립된 요소의 재조합이라 알고리즘 신규성은 제한적이고, novelty는 problem formulation과 시스템 통합에 있음.

**Benchmark results**

- closed-loop 정책의 20회 시행 중 align 성공은 Bottle 18, Syringe 18, Marker 16인 반면 open-loop replay는 각각 2, 1, 0에 그침.
- Marker task ablation(500 episode)에서 전체 정책 성공률 65%, proprioception-only 11%, finger reward 제거 27%, pose reward 제거 40%로 두 보상 모두 필요함.
- 관측 노이즈 표준편차 3cm에서도 두 task 성공률은 60% 이상을 유지하나, Syringe는 offset noise가 커지면 proprioception-only baseline보다 낮아짐.
- 4종 손(Sharpa, Wuji, Allegro, XHand) 비교에서 5지 고자유도 손만 삽입에 성공해 in-hand assembly가 hand morphology benchmark로 기능함을 보임.
- 검증 범위는 3개 task, real-robot 시행 task당 20회, 시뮬레이터는 IsaacSim 전용이며 code·영상은 공개하나 task 수가 3개로 제한적임.

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

실로봇 검증과 촘촘한 ablation을 갖춘 시스템 논문으로 CoRL이 요구하는 실증 수준을 충족하고 실제로 CoRL 2026 게재가 확정됨. 다만 3개 task와 단일 손 형태에 국한돼 일반화 범위가 좁고 알고리즘적 개념 도약은 크지 않다는 점이 약점임.

**추천 이유 & 누리랩 연구와의 연결점**

- perturbation 복구 실험(정렬 흐트러짐·plunger 빠짐 회복)은 실패 복구 정책 설계에 참고할 real-robot 사례임.
- 손가락 역할 분리(held/fixed) 보상 설계는 manipulation 연구에서 multi-contact 역할 할당 문제로 일반화할 수 있음.
- FoundationPose 기반 occlusion robust pose tracking과 깊이 일관성 게이트는 누리랩 pose estimation·active perception 파이프라인에 참고 가능함.

---

### 8. [63점] DUET-DINO: Simultaneous Cross-View World Modeling for Latent Planning in Robot Manipulation

- **분야**: World Model / Manipulation · **robotics relevance**: 10/10
- **arXiv**: [2609.10506](https://arxiv.org/abs/2609.10506) ([PDF](https://arxiv.org/pdf/2609.10506))
- **저자**: Nisarga Nilavadi, Ralf Römer, Moritz Reuss, Michael Krawez, Tobias Jülg, Angela P. Schoellig, Rudolf Lioutikov, Wolfram Burgard
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Preprint, Project Page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 60점

> 💡 DUET-DINO는 정면(side)·손목(wrist) 카메라를 latent 공간에서 cross-attention으로 상호 조건화하는 dual-view world model로, 7-DoF 전체 action space에 대한 latent planning을 가능하게 함. DROID·RoboArena로 학습해 reach 92%, angled-reach 72.5%, lift 60.0% 성공률을 달성했고 DINOv3 encoder가 V-JEPA 2보다 action-conditioned 변화를 더 잘 포착함을 보임.

**Core innovation & methodology**

- side-view·wrist-view 관측을 각각 frozen DINOv3 encoder로 인코딩한 뒤, cross-attention block으로 서로의 latent를 query해 보완 정보를 주입하고 view별 predictor head가 각자의 다음 latent를 예측함
- teacher-forcing loss와 K=2 step autoregressive rollout loss를 결합한 dual-view prediction loss로 cross-attention block과 predictor head를 처음부터 공동 학습함(encoder는 고정)
- 7-DoF action(translation·rotation·gripper) 전체에 대해 CEM으로 action sequence를 최적화하되, side·wrist 각 view의 goal latent 거리를 zero-action rollout 기준으로 정규화해 합산한 dual-view goal cost를 사용함
- 기존 V-JEPA 2-AC·DINO-WM이 단일 view·translation 위주 planning에 머물렀던 것과 달리, 두 view를 동시에 조건화해 rotation·gripper까지 포함한 fine-grained control로 latent world model planning을 확장함

**Novelty vs. prior works**

- 가장 가까운 prior work인 V-JEPA 2-AC, DINO-WM은 단일 카메라 view로 coarse translation 위주 planning만 다뤘는데, DUET-DINO는 두 view를 cross-attention으로 상호 조건화한 것이 핵심 차이임
- ablation에서 cross-attention을 뺀 independent dual-view(단순 두 predictor 병렬)는 reach 78%(DUET-DINO 92%), angled-reach 55.0%(DUET-DINO 72.5%)로 격차가 커, 단순 view 결합이 아니라 cross-view conditioning 자체가 이득의 원인임을 확인함
- 다만 world model 아키텍처 자체(JEPA류 predictor, CEM planning)는 V-JEPA 2 프레임워크를 그대로 가져온 것이고 새로 더한 것은 cross-attention 융합과 dual-view cost뿐이라 representation·objective 수준의 신규성은 중간 정도임

**Benchmark results**

- RoboLab 시뮬레이터에서 reach(100회×10 task), angled-reach(40회×4 task, distribution shift 100회, hardware 30회), angled-lift(40회×4 task) 평가. DROID 62,877 + RoboArena 5,856 trajectory로 학습, 코드·체크포인트는 공개 예정(아직 미공개)
- reach 성공률: DUET-DINO(DINOv3) 92% vs independent dual-view 78% vs wrist-view 단일 79% vs V-JEPA 2-AC 공식 checkpoint 55%
- angled-reach 성공률: DUET-DINO 72.5% vs DINOv3 independent dual-view 55.0% vs V-JEPA 2 계열 전부 25% 이하
- 실로봇(Franka, DROID hardware setup) angled-reach 3 task 30회 평가에서 DUET-DINO 26.7% vs independent dual-view 16.7%로 우위는 유지하나 절대 성공률은 낮고, CEM 예산을 시뮬레이션 대비 축소(1 iteration, 500 후보)한 조건임
- angled grasp+lift task에서 DUET-DINO는 angled-reach 75.0%→lift 60.0%로 단계 진행 중 격차가 커짐(independent dual-view는 60.0%→57.5%). dual-view 모델은 single-view 대비 추론 속도 약 2배 느림

**Top-tier conference 적합성 — 65/100 · 추천 venue: CoRL**

실로봇 하드웨어 평가와 조밀한 ablation(cross-attention 유무, 카메라 교란, encoder 종류)으로 실증 근거가 탄탄하고, 7-DoF 전체 action에 대한 latent planning이라는 실질적 병목을 정면으로 다룸. 다만 방법론은 기존 V-JEPA 2 predictor에 cross-attention 융합을 더한 수준이라 formulation 신규성은 크지 않고, 실로봇 성공률(26.7%)이 시뮬레이션 대비 크게 낮아 sim-to-real gap이 남아있음. CoRL·ICRA poster급은 무난하나 oral 경쟁은 어려움.

**추천 이유 & 누리랩 연구와의 연결점**

- latent world model에서 rotation·gripper 같은 fine-grained action이 예측되지 않는 문제를 정면으로 다뤄, policy의 fine-grained control 실패를 진단하는 failure detection 연구와 직접 연결됨
- side-view·wrist-view cross-attention 구조는 어느 view가 현재 task에 더 정보량이 큰지 학습하는 active perception baseline으로 쓸 수 있고, object-centric 3DGS와 결합해 두 view를 3D 표현으로 통합하는 확장도 가능함
- DINOv3가 V-JEPA 2보다 action-conditioned 변화를 잘 포착한다는 분석은 world model·VLA용 visual encoder 선택 시 참고할 실증 근거로 활용 가능함

---

### 9. [62점] SwingBot: Learning Whole-Body Brachiation for Humanoid Robots

- **분야**: Locomotion / Whole-body Control (Humanoid) · **robotics relevance**: 8/10
- **arXiv**: [2609.10283](https://arxiv.org/abs/2609.10283) ([PDF](https://arxiv.org/pdf/2609.10283))
- **저자**: Yujie Xiong, Peng Zhai, Taixian Hou, Quancheng Qian, Cunwang Liu, Kangmai Hu, Long Yang, Zhiyan Dong 외 1명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: CORL2026
- **원문 검토**: PDF 전문 · 1차 스크리닝 56점

> 💡 영장류 brachiation(구름대 이동) 영상에서 뽑은 release-swing-capture 키프레임을 초기 탐색의 residual guidance로 쓰고, RSSM 기반 world model로 배포 시 관측 불가능한 몸통 변위·훅 접촉 상태를 추정해 20-DoF 휴머노이드의 연속 brachiation을 학습함. 실로봇에서 payload·외란·bar 간격 변화에도 연속 이동을 실증한 첫 사례임.

**Core innovation & methodology**

- release-swing-capture 3단계를 sparse keyframe guidance(KFG)로 만들어 학습 초반엔 keyframe이 행동을 지배하다, epoch에 따라 blending 계수 β_e를 0→1로 annealing해 정책이 점차 제어권을 넘겨받게 함
- 배포 시 접근 불가능한 privileged 변수(구간 내 상대 변위, 좌우 훅 접촉)를 RSSM(recurrent state-space model)으로 추정해 proprioception 4프레임 history만으로 latent를 계산함
- 양쪽 훅이 접촉하는 구간 경계에서만 encoder로 latent를 보정하고, 구간 내에서는 recurrent dynamics로만 전파해 long-horizon drift를 제한함
- 성공한 handoff 종료 상태를 반대쪽 리딩 핸드 command의 초기 상태로 재사용하는 adaptive sampling으로 연속 전환 학습을 도움

**Novelty vs. prior works**

- 기존 brachiation 로봇(AcroMonk, RicMonk)은 2~3-link 저자유도 전용 기구에 model-based 제어를 썼는데, SwingBot은 20-DoF humanoid 전신에 순수 RL 정책을 적용한 점이 본질적으로 다름
- keyframe guidance는 기존 reference-guided RL(teleoperation·imitation prior)의 연장선이고 RSSM도 DreamWaQ 등 기존 privileged latent 추정 기법의 재구성이라, 개별 구성요소의 신규성은 제한적이며 조합과 첫 실로봇 실증이 기여의 핵심임
- 비교 대상이 자체 ablation(w/o KFG, w/o RSSM, teacher)뿐이고 외부 baseline이나 대안적 exploration 기법과의 비교가 없어 방법 우위의 일반성 검증은 제한적임

**Benchmark results**

- KFG 없이는 20개 학습 seed 전부에서 all-8(8회 연속 전환) 프로토콜을 완료하지 못함(성공률 0)
- KFG에 RSSM latent를 더하면 all-8 성공률이 1.5s 전환 간격에서 57.28%→61.27%(+3.99%p), 1.0s 간격에서 43.12%→48.86%(+5.74%p) 상승, privileged 정보를 쓰는 teacher(65.78%/53.21%)가 상한선임
- 실로봇 정량 평가(조건당 5회 연속 시행, 시행마다 최대 8회 swing): nominal 조건 개별 swing 기준 single-swing 성공률 92.86%(26/28), 5회 시행 전부 8회 swing을 성공한 all-8 성공률은 60%(3/5)
- 1kg payload·외란 조건에서는 all-8 성공률이 40%로 하락, 반복 시행 시 어깨 모터 발열로 토크 부족이 주요 실패 원인으로 보고됨
- bar 간격 변화 조건에서 single-swing 94.12%(32/34)로 가장 높으나, 실험 범위(22~28cm) 밖 일반화는 검증되지 않았고 외부 시각 지각 없이 blind policy로 동작함

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

고자유도 휴머노이드의 첫 실로봇 brachiation이라는 명확한 하드웨어 기여와, ablation으로 keyframe·RSSM 각각의 기여도를 분리한 점이 CoRL의 실증 중심 기준에 부합함. 다만 외부 baseline 비교 부재와 시각 지각 없는 bar 간격 일반화 한계가 rejection risk로 남음(논문은 CoRL 2026 accept로 표기돼 있으나 본 평가는 독립적으로 판단함).

**추천 이유 & 누리랩 연구와의 연결점**

- privileged world model이 배포 시 관측 불가능한 상태(접촉·상대 변위)를 latent로 추정하는 구조는 manipulation의 접촉 상태 추정이나 failure detection에서 관측 불가능한 실패 신호 추정에 응용 가능함
- keyframe을 초기 탐색의 residual bias로 쓰고 점진적으로 annealing하는 방식은 long-horizon manipulation skill chaining에서 sparse reward 문제를 완화하는 curriculum 설계에 참고할 수 있음
- 구간 경계에서만 encoder로 보정하고 구간 내에는 recurrent dynamics로 전파하는 방식은 robot memory나 world model의 partial observability 처리 설계에 직접 참조 가능함

---

### 10. [62점] Frequency-Conditioned Flow Matching for Vision-Language-Action Models

- **분야**: VLA · **robotics relevance**: 10/10
- **arXiv**: [2609.10405](https://arxiv.org/abs/2609.10405) ([PDF](https://arxiv.org/pdf/2609.10405))
- **저자**: Haochen Niu, Shengye Dong, Hao Liu, Peiwen Lin, Wang Chuang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 58점

> 💡 robot 궤적의 주파수 성분이 매우 불균일한 에너지 분포를 가진다는 관찰에서 출발해, Flow Matching 기반 VLA의 source distribution·training objective·CFG guidance 세 단계 전부를 DCT 주파수 좌표로 조건화하는 FreqFM을 제안함. LIBERO-Plus에서 최대 9.3점, VLA-Arena 총점 4.2점을 개선했고 6개 실로봇 task에서도 효과를 확인함.

**Core innovation & methodology**

- action frequency를 trajectory의 implicit한 속성이 아니라 explicit conditioning 축으로 올려 Flow Matching pipeline 전 단계에 일관되게 적용함
- 학습 action의 per-frequency power spectrum으로 source distribution의 주파수별 scale을 맞춰 source와 target의 spectral 구조를 일치시킴(spectrum-matched source)
- 주파수별 회귀 손실을 PSD로 정규화한 뒤 likelihood 기반 multi-task weighting으로 재조정하는 adaptive objective를 도입함
- classifier-free guidance의 추가 residual을 주파수별 reference transport scale 단위로 측정해, 허용 범위(budget ball) 안으로 clip하는 STB-CFG(spectral transport-budget CFG, 주파수별 허용 크기 안으로 guidance를 제한하는 기법)로 고주파 영역의 과도한 외삽을 억제함

**Novelty vs. prior works**

- FAST, FreqPolicy, FocalPolicy, FGO, FAFM 등 이미 다수 연구가 DCT·주파수 구조를 action tokenization·consistency·smoothness 목적으로 활용해왔고, 본 논문은 related work에서 이를 직접 인용하며 자신을 이들과 구분함
- 차별점은 주파수 조건화를 tokenization 한 단계가 아니라 source·objective·guidance 세 단계 전체에 걸쳐 적용했다는 범위이며, 개별 요소(spectrum matching, PSD 정규화, guidance budget)는 이미지 diffusion의 FreSca·frequency-decoupled guidance와 유사한 기법을 action domain에 옮긴 조합에 가까워 근본적으로 새로운 problem formulation은 아님

**Benchmark results**

- LIBERO 4개 suite에서 π0 대비 +0.7점, π0.5 대비 +1.2점으로 이미 성능이 포화된 벤치마크라 개선폭이 작음
- LIBERO-Plus(7종 perturbation, 1만개 이상 perturbed instance)에서 π0 +5.5점, π0.5 +9.3점으로 가장 큰 개선을 보였고, 개선폭은 baseline이 약한 Camera·Robot·Noise perturbation에 집중됨(baseline 성능과 개선폭 상관 −0.81~−0.95)
- VLA-Arena 11개 task 총점에서 π0 +2.6점, π0.5 +4.2점 개선했으나 Extrapolation category(unseen object 등)는 두 backbone 모두 오히려 하락, 학습 spectrum과 어긋난 task에서의 한계로 저자도 인정함
- AgiBot Expedition A2 휴머노이드 6개 실로봇 task(각 30 trial)에서, 정밀 정렬이 필요한 task(컵 쌓기 +23.3, 폴더 삽입 +13.4, 우표 집기 +13.3)의 개선폭이 크고 여유 있는 배치 task는 +6.7/+3.3으로 작음
- ablation에서 spectrum-matched source 제거 시 LIBERO-Plus 성공률이 4.2점 하락해 가장 크게 기여했고, transport budget은 성공률 기여는 작지만(1.9점) 실행 궤적의 jerk를 56% 줄임(0.442→0.193)

**Top-tier conference 적합성 — 58/100 · 추천 venue: ICRA**

3개 시뮬레이션 벤치마크와 실로봇 6개 task에 걸친 일관된 개선, 통계적으로 정리된 ablation이 강점이라 top-tier venue 심사를 통과할 실험적 근거는 갖춤. 다만 핵심 기여가 기존 frequency-domain 기법들을 pipeline 전반에 조합 적용한 것에 가깝고 Extrapolation task에서 규칙적으로 regression이 나타나 novelty와 일반화 한계 양쪽에서 reviewer 지적 위험이 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- action을 주파수 영역에서 explicit하게 다루는 관점은 test-time optimization에서 실패 시 고주파(local correction) 성분만 재보정하는 inference-time 수정 전략으로 확장 가능함
- 저주파는 global motion, 고주파는 local correction이라는 분해는 failure detection에서 오차가 어느 스케일에서 발생했는지 진단하는 신호로 쓸 수 있음
- STB-CFG의 reference-transport budget 개념은 test-time planning에서 policy가 학습 분포를 벗어나는 정도를 주파수별로 제한하는 안전장치로 응용해볼 수 있음

---

### 11. [62점] Identifying Habit, Physics, and Nuisance in Robot World Models

- **분야**: World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.09210](https://arxiv.org/abs/2609.09210) ([PDF](https://arxiv.org/pdf/2609.09210))
- **저자**: Jinting Hang, Zhenhui Cai
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 teleoperation 시연의 다양성이 operator habit·물리 법칙·관측 nuisance 세 요인이 뒤섞인 결과라는 구조적 인과모델(SCM)을 세우고, action 개입 실험으로 각 요인을 분리함. 공유된 물리 법칙(dynamics)을 고정하고 얇은 인터페이스만 적응시키는 규칙이 StackCube·DROID·RH20T에서 적은 데이터로도 scratch 학습보다 나은 전이 성능을 보임.

**Core innovation & methodology**

- a=g(h,z,u), z'=f(z,a), o=r(z,c)라는 SCM으로 habit(h)은 action에만, nuisance(c)는 관측(o)에만 영향을 주고 물리(f)는 상태에서 상태로만 이어진다는 두 exclusion 제약을 둠.
- action을 무작위로 바꾸거나 다른 operator의 action으로 교체하는 개입은 물리 예측 오차를 크게 늘려야 하고, 외형·카메라 시점 변화는 그러면 안 된다는 가설을 설계해 검증함.
- 적응 규칙은 학습된 물리 readout f*를 얼려두고 얇은 인터페이스 g(또는 pixel 모델의 delta head)만 업데이트하는 것으로, LoRA류 parameter-efficient adaptation과 형태는 비슷하되 causal 근거로 정당화함.
- 과거 상태·action 후보를 물리 우도와 habit 우도로 함께 채점하는 reverse scoring으로, 정답 과거에 확률 질량을 더 싣는지 확인함(hard operator identification이 아니라 ranking 보조 용도로 한정).

**Novelty vs. prior works**

- Dreamer류 world model은 P(o'|o)를 하나의 예측기로 뭉뚱그려 학습하는데, 이 논문은 그 안에 섞인 habit·physics·nuisance를 causal graph와 개입 실험으로 명시적으로 분리하는 identification 문제로 재정의함 — 새로운 problem formulation에 해당함.
- LAPO·AdaWorld 같은 latent action 추출 방법과 목적이 다르다고 저자가 직접 구분함: latent action은 영상에서 복원한 controllable bottleneck이고, 이 논문의 habit은 operator의 action 선택 성향으로 별개 개념임.
- freeze+adapt 규칙 자체는 LoRA 등 기존 parameter-efficient tuning과 근본적으로 같은 형태라 새롭지 않고, novelty는 그 규칙을 언제 써도 되는지에 대한 causal 정당화와 실패 조건(과도하게 성긴 command interface, cross-task 전이 불가 등)을 실험으로 구획한 데 있음.

**Benchmark results**

- StackCube 시뮬레이션: action을 다른 후보로 섞으면 one-step 상태 오차가 약 10.4배 증가, N=16 적응에서 freeze+g가 finetune·scratch보다 낮은 오차(0.00089 vs 0.00115 vs 0.00169)를 보임.
- StackCube closed-loop 성공률(N=128, 8 seed, 40 episode): freeze+g 0.22±0.09 vs scratch 0.10±0.07로, 절대 성공률 자체는 privileged 상한 0.80에 크게 못 미침.
- DROID proprioception: 잘못된 action 오차비 약 13배, N=32에서 freeze+g가 scratch보다 오차가 낮음(0.00030 vs 0.00039).
- RH20T 멀티 오퍼레이터: 다른 operator의 action으로 바꾸면 오차가 약 1362배 증가해 무작위 셔플(1352배)과 거의 같은 수준 — habit을 action 단에서 분리하기 어렵다는 뜻이고, operator 식별 정확도도 0.52(chance 0.25)로 낮음.
- DROID pixel 실험: 외형 변화는 오차비 0.988로 거의 무영향, 카메라 시점 교체는 1.42배로 더 어려움.
- 저자도 cross-task habit 전이는 win rate 약 57%로 결론이 미확정(weak)이라 명시함. closed-loop 검증은 시뮬레이션에 한정되며 실로봇 배치는 하지 않음.

**Top-tier conference 적합성 — 52/100 · 추천 venue: RSS**

world model의 예측 다양성을 causal identification 문제로 재정의한 문제설정은 신선하고 실패 조건까지 정직하게 구획해 RSS류 causal/embodied 세션에 어울림. 다만 실험이 작은 MLP dynamics·toy OT-CFM·StackCube 저성능(22%) 중심의 진단적 검증에 머물고 실로봇 검증이 전혀 없어, top-tier full paper보다는 짧은 analysis 트랙이나 workshop에 더 맞는 규모임.

**추천 이유 & 누리랩 연구와의 연결점**

- habit·physics·nuisance 분리 SCM은 nurilab의 counterfactual/causal reasoning 주제와 정확히 맞물림 — world model 학습 시 시연자 습관을 물리 법칙과 분리해 학습 데이터 다양성을 다루는 원칙으로 쓸 수 있음.
- freeze-physics-adapt-interface 규칙은 test-time optimization/few-shot adaptation에 적용 가능함 — 새 로봇·새 사용자 데이터가 적을 때 world model을 고치지 않고 얇은 층만 적응시키는 전략으로 재현 가능함.
- reverse scoring으로 과거 상태·action의 타당성을 채점하는 방식은 robot memory에서 과거 시연을 신뢰도로 재정렬하거나 failure recovery 시 원인(습관적 실수 vs 물리적 실패)을 구분하는 진단 도구로 확장할 수 있음.

---

### 12. [61점] GTA-2: A Multi-VLM Framework for Synthesizing Robot Manipulation Skills via Grounded Task Axes

- **분야**: Manipulation / VLA · **robotics relevance**: 9/10
- **arXiv**: [2609.09808](https://arxiv.org/abs/2609.09808) ([PDF](https://arxiv.org/pdf/2609.09808))
- **저자**: M. Yunus Seker, Shobhit Aggarwal, Ruwan Wickramarachchi, Jonathan Francis, Oliver Kroemer
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 64점

> 💡 GTA-2는 4개의 VLM 에이전트가 task 분해·controller 조합·파라미터 할당·시각적 grounding을 단계별로 맡아 재사용 가능한 task-axis skill을 zero-shot으로 생성하는 프레임워크임. 실로봇 14개 task에서 최강 baseline인 Code-as-Policies 대비 zero-shot 성공률을 31.4%p 앞섰고, 단계별 human feedback으로 90.7%까지 끌어올림.

**Core innovation & methodology**

- 매니퓰레이션 skill을 task-relevant keypoint·axis에 기반한 task-axis controller의 구조화된 조합으로 표현하고, abstract(lifted) skill synthesis와 scene-specific grounding을 분리함
- Task Decomposer·Skill Generator·Parameter Setter·Vision Module 4개의 전문화된 VLM 에이전트가 각각 subtask 분해, controller 조합 생성, 수치 파라미터 할당, RGB-D 기반 keypoint·axis grounding을 담당함
- action을 end-to-end로 예측하지 않고 subtask·skill recipe·parameter·grounding을 명시적 중간 출력으로 남겨 각 단계를 개별 검증·수정 가능하게 만듦
- 오류가 발생한 stage에만 targeted human feedback을 줘서 나머지 올바른 구성요소는 보존한 채 해당 agent만 재실행함

**Novelty vs. prior works**

- 가장 가까운 prior work인 GTA-1(Grounded Task-Axes) 대비 본질적 차이는 task decomposition·controller 선택·파라미터 튜닝을 수작업에서 4단계 VLM 파이프라인 자동화로 옮긴 것임
- Code-as-Policies 계열은 perception·grounding·control을 단일 생성 프로그램 안에서 한 번에 처리하는데, GTA-2는 이를 전문 에이전트로 분리해 단계 간 결합도를 낮춘 것이 핵심 차이임
- 다만 사용하는 task-axis controller representation 자체는 GTA-1·Sharma & Kroemer의 기존 개념을 그대로 가져온 것이라, representation 수준의 신규성은 제한적이고 기여는 주로 자동화·모듈화에 있음

**Benchmark results**

- 실로봇 UR5e, 14개 매니퓰레이션 task(pick-and-place, articulated object, contact-rich, tool use, constrained motion), task당 20회 평가
- GTA-2 zero-shot 평균 성공률 73.9%로 최강 baseline인 CaP-Primitive(42.5%) 대비 31.4%p 우위, targeted refinement 후 90.7%까지 상승
- 독립 생성 210회 중 feedback 없이 154회(73.3%) 성공, 1회 feedback 후 181/210(86.2%), 2회 후 208/210(99.0%), 3회 이내 전원 성공
- 동일 task-axis controller를 쓰는 CaP-TAC은 GTA-2보다 낮지만 pouring·cutting·sweeping 등 contact-rich task에서 CaP-Primitive를 능가함
- VLM은 Gemini 3.1 Pro 단일 모델, task-specific demonstration·fine-tuning 없음. 단일 UR5e·단일 gripper·단일 센서 구성에서만 검증되어 embodiment 일반화는 미검증

**Top-tier conference 적합성 — 62/100 · 추천 venue: CoRL**

실로봇 14개 task와 세 baseline 비교로 실증 근거는 탄탄하고, stage별 human feedback을 통한 targeted refinement라는 실용적 기여가 있음. 다만 GTA-1의 task-axis 표현을 VLM 자동화로 확장한 정도라 formulation 신규성은 제한적이고, 단일 robot·단일 VLM 백본에서만 검증돼 일반화 근거가 약함. CoRL 수준 poster급은 무난하나 oral 경쟁에는 부족함.

**추천 이유 & 누리랩 연구와의 연결점**

- 단계별 명시적 중간 표현은 실패 지점을 자동 진단하는 orchestrator VLM으로 확장 가능해 failure detection/recovery 연구와 직접 연결됨(논문도 future work로 언급)
- object-centric task-axis 표현을 keypoint·axis grounding에 object-centric 3DGS나 scene graph를 결합해 대체하는 연구로 이어질 수 있음
- 현재는 human feedback으로 stage를 재생성하는데, 이를 실행 모니터링 기반 자동 진단 loop로 바꾸면 test-time optimization 연구가 됨

---

### 13. [58점] Learning Terrain-Adaptive Humanoid Locomotion on Granular Terrain

- **분야**: Locomotion (Humanoid, Granular Terrain) · **robotics relevance**: 8/10
- **arXiv**: [2609.10286](https://arxiv.org/abs/2609.10286) ([PDF](https://arxiv.org/pdf/2609.10286))
- **저자**: Junnosuke Kamohara, Feiyang Wu, Andy Ningan Zong, Daniel I. Goldman, Yashwanth Nakka, Seth Hutchinson, Ye Zhao
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 57점

> 💡 발-지반 접촉을 3D resistive force theory(RFT)로 물리 기반 모델링한 granular contact model을 만들어 시뮬레이션에서 RL 정책을 학습하고, teacher-student 구조로 지반 강성을 latent로 추정해 휴머노이드가 다양한 알갱이 지형에 적응하게 함. Unitree G1 하드웨어로 basalt·마른 모래·해변 모래에서 agile 휴머노이드 보행을 처음 실증함.

**Core innovation & methodology**

- 기존 방법이 법선 방향엔 RFT나 heuristic cone model, 접선 방향엔 Coulomb friction 등을 별도로 조합한 것과 달리, 단일 3D RFT 정식화(면적당 깊이당 반력, 실험 데이터 fit)로 법선·접선 반력을 일관되게 도출함
- 각 발의 접촉점 격자에서 힘·모멘트를 합산해 net wrench만 whole-body dynamics에 반영하고 IsaacLab에 통합해 대규모 병렬 RL 학습을 가능하게 함
- teacher policy는 privileged 정보(지반 강성 등)를 VAE encoder로 압축한 latent를 쓰고, student policy는 proprioceptive history만으로 TCN encoder가 이 latent를 추정해 배포함
- VAE reconstruction target을 media-dependent scaling coefficient η 하나로 제한해 latent가 지반 재질 정보에 특화되도록 유도함

**Novelty vs. prior works**

- 선행 연구(Cone-RFT 기반 quadruped, mattress용 Mild)는 법선 방향만 물리 기반이고 접선은 heuristic이었는데, 3D RFT는 접선 반력까지 자연스럽게 도출되며 lateral force response 재현으로 이를 확인함
- teacher-student로 지반 강성을 proprioception만으로 추정하는 구조 자체는 quadruped terrain-adaptive locomotion 연구의 확장에 가까워 학습 패러다임 자체의 새로움은 제한적임
- 휴머노이드에 물리 기반 granular contact를 결합해 주행·점프까지 다룬 것은 처음이라고 주장하나, 기여의 핵심은 새 알고리즘보다 정확한 물리 모델의 최초 humanoid 적용에 가까움

**Benchmark results**

- 35kg 강체 관입 실험에서 3D-RFT가 MPM(연속체 기준) 대비 수평 이동거리·침하량이 가장 근접함. Heuristic-RFT·Cone-RFT-Multi는 과도한 수평 이동을 보임
- MPM poppy seed 평가(Table I)에서 deep sand 성공률이 3D-RFT 85% vs Heuristic-RFT 3% vs Cone-RFT-Multi 8%로 큰 격차 보임
- basalt/sand/poppy seed 3종 지형(Table II)에서 Rigid contact로 학습한 정책은 sand·poppy seed 성공률 0%인 반면, 3D-RFT 기반 정책은 100% 성공하며 teacher-student(Ours)가 tracking error에서 가장 우수함
- 실로봇(Unitree G1) dry sand에서 Rigid는 1.5m/s 이상 보행 실패, basalt에서는 전 속도 구간 실패한 반면 Ours는 0.5~2.5m/s 전 구간 성공하며 최저 tracking error 기록
- jumping 실증은 시뮬레이션에서만 수행됨(PPO-Rigid는 착지 전 미끄러짐 보정 실패, PPO-3D-RFT는 성공), 실로봇 점프 검증은 없음

**Top-tier conference 적합성 — 60/100 · 추천 venue: ICRA**

물리 기반 3D RFT contact model을 시뮬레이터에 통합하고, 하드웨어에서 rigid-contact 정책이 실패하는 조건을 명확히 반박하는 실험 구조가 설득력 있음. 다만 학습 알고리즘(teacher-student+VAE)은 기존 terrain-adaptive locomotion 틀의 재적용이고 시각 정보 없이 3개 지형·좁은 속도 구간으로만 검증돼, top-tier venue의 oral보다는 poster급으로 판단됨.

**추천 이유 & 누리랩 연구와의 연결점**

- heuristic 없이 물리 기반으로 접촉을 통일한 3D RFT 접근은 manipulation의 contact-rich task에서 접촉력 예측 world model 설계에 참고할 수 있음
- teacher-student로 관측 불가능한 물리 파라미터(지반 강성)를 latent로 추정하는 구조는 물체 물성 추정을 위한 active perception이나 test-time adaptation 연구에 직접 적용 가능함
- Rigid contact 정책이 알갱이 지형에서 전면 실패하는 결과는 sim-to-real gap 발생 조건을 물리 기반으로 예측한 사례로, failure detection 연구에 인용 가능함

---

### 14. [57점] HaWMPO: Hallucination-Aware World Model-based Policy Optimization for Generalist Robot Policy

- **분야**: World Model/VLA · **robotics relevance**: 10/10
- **arXiv**: [2609.09941](https://arxiv.org/abs/2609.09941) ([PDF](https://arxiv.org/pdf/2609.09941))
- **저자**: Zengjue Chen, Peidong Liu, Jiawei Li, Qi Wang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 world model 기반 RL(imagined rollout)에서 생기는 hallucination을 action 조건부로 점수화하는 HAM을 만들고, 이 점수로 GRPO 보상을 깎는 Reward-Soft 기법(HaWMPO)을 제안함. LIBERO 3개 suite에서 base 대비 +15.0pt, 가장 강한 baseline 대비 +2.8pt 개선했고 G1 실로봇 2개 task에서도 성능이 올랐음.

**Core innovation & methodology**

- world model(action-conditioned Wan2.2 기반)이 생성한 8프레임 rollout의 신뢰도를 DINOv3 유사도·depth consistency·optical-flow trajectory consistency·MUSIQ 4개 지표의 평균으로 정의한 hallucination target으로 지도학습함(HAM).
- HAM은 예측 영상·현재/기준 이미지·action을 fusion transformer로 합쳐 chunk 단위 hallucination score를 0~1로 출력함.
- Reward-Soft 기법으로 raw reward R을 (1−α·H)·R로 깎아, hallucination이 심한 action chunk의 보상 영향을 줄이고 GRPO advantage 계산에 반영함.
- world model, HAM, reward model, GRPO를 묶은 closed-loop pipeline으로 OpenVLA-OFT를 8개 병렬 imagined environment에서 online 학습시킴.

**Novelty vs. prior works**

- 저자 스스로 WoVR을 baseline으로 삼아 그 world model(Wan2.2 action-conditioned)을 그대로 가져다 쓰고, HAM과 Reward-Soft만 새로 얹은 구조로, world model 자체나 RL 알고리즘(GRPO)은 기존 것을 그대로 씀.
- hallucination을 다중 지표 조합의 continuous score로 정의한 점은 WoVR의 keyframe 기반 접근과 달리 명시적 검증(AUROC 0.9375)을 거쳤다는 차별점이 있음.
- reward를 hallucination으로 downweight하는 아이디어 자체는 world model RL 문헌에서 이미 논의되던 방향이라, 새로운 problem formulation이라기보다 기존 파이프라인의 구성요소 교체·보강에 가까움.

**Benchmark results**

- LIBERO 3개 suite(Spatial/Goal/Object) 평균: OpenVLA-OFT-base 48.7% → WMPO 56.8% → WoVR* 60.9% → HaWMPO 63.7% (base 대비 +15.0pt, 최강 baseline 대비 +2.8pt).
- WoVR*는 원 논문의 PACE 전략을 뺀 재현판이라 공정 비교를 위한 조정이며, 원 WoVR 논문 수치와는 다름(저자 명시).
- G1 실로봇 2개 task, task당 20회: base 67.5% → WoVR 72.5% → HaWMPO 80.0% (WoVR 대비 +7.5pt), 시행 수가 적어 변동 폭이 큼.
- HAM 단독 검증: 50개 LIBERO chunk(hallucinated 18/non 32, 사람 라벨) 기준 AUROC 0.9375로 DINO-only(0.9062)·Depth-only(0.8941)·Trajectory-only(0.8872)보다 높고 MUSIQ-only(0.3056)는 크게 낮음.
- ablation(HAM 제거): Spatial에서는 8.0~11.6pt 하락해 HAM의 기여가 뚜렷하지만, Goal에서는 오히려 HAM 제거 시 최대 2.4pt 상승(HAM이 있을 때 더 낮은 성능)해 task별 α 튜닝이 필요함을 보여줌.

**Top-tier conference 적합성 — 46/100 · 추천 venue: CoRL**

world model rollout의 hallucination을 명시적으로 점수화하고 실로봇까지 검증한 점은 실용적 기여지만, world model과 RL 알고리즘을 WoVR·GRPO에서 그대로 가져와 novelty가 구성요소 교체 수준임. LIBERO는 4개 suite 중 3개만, 실로봇은 task 2개·20회씩만 평가해 top-tier에서는 실험 규모와 baseline 재현 공정성(WoVR*가 PACE 제외 축소판)에 대한 지적을 받을 위험이 큼.

**추천 이유 & 누리랩 연구와의 연결점**

- hallucination score를 학습해 world model rollout 신뢰도를 정량화하는 방식은 nurilab의 failure detection·recovery 연구에 그대로 가져다 쓸 수 있음 — 실행 전 rollout 신뢰도로 재시도·개입 시점을 판단하는 test-time 안전장치로 응용 가능함.
- world model 기반 policy optimization은 test-time optimization/inference-time planning 주제와 직접 연결되며, HAM 같은 신뢰도 모델을 counterfactual reasoning(가상 rollout의 타당성 검증)으로 확장할 수 있음.
- 4개 지표(DINOv3, depth, optical flow, MUSIQ) 조합 설계는 world model 평가나 robot memory에 rollout을 저장할 때 품질 필터링 기준으로도 재사용 가능함.

---

### 15. [55점] No Free Checker: A Survey of Verifiers for Robot Policies

- **분야**: Robot Policy Verification (Survey) · **robotics relevance**: 8/10
- **arXiv**: [2609.09250](https://arxiv.org/abs/2609.09250) ([PDF](https://arxiv.org/pdf/2609.09250))
- **저자**: Yang Wan, Xihang Yue, Zhirui Liu, Ziyuan Chu, Shuxun Wang, Yuhan Chen, Xiaonan Jiang, Xukun Zhu 외 2명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Survey. 31 pages, 5 figures, 7 tables, 187 references. Covers reward models, success and failure detection, temporal-logic and formal verification, world-model evaluation, and reward hacking. Project page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 55점

> 💡 로봇 정책을 평가·훈련하는 verifier 약 150개를 availability(비용·시점·빈도)와 credibility(점수 신뢰도) 두 축으로 체계화한 survey임. human, rule-based/formal, learned/pretrained, model-intrinsic 네 계열 모두에서 availability가 오르면 credibility가 떨어진다는 공통 trade-off를 보임.

**Core innovation & methodology**

- verifier를 (context, candidate) -> score 매핑으로 정식화하고 판정 주체 기준 4개 계열로 분류함.
- availability와 credibility 두 축을 도입해 계열이 달라도 트레이드오프를 같은 잣대로 비교하게 함.
- 각 계열의 점수가 실제로 무엇을 주장하는지(task success·progress·safety·failure·데이터 가치)를 표로 정리함.
- verifier 자체의 신뢰도를 검증하는 세 기준(사람 라벨 일치, 훈련된 정책 성능, reward hacking 하의 행동)을 정리함.

**Novelty vs. prior works**

- 기존 survey는 주로 reward model이나 success detection 한 갈래만 다루는데, 이 논문은 human부터 model-intrinsic까지 네 갈래를 한 축 위에서 통일해 비교함.
- 가용성과 신뢰도를 동시에 만족하는 verifier는 없다는 트레이드오프 명제는 새 실험으로 증명한 것이 아니라 기존 약 150편 결과를 재조직해 관찰한 것이라 empirical novelty는 크지 않음.
- 새 verifier나 새 실험을 제안하지 않아 기여는 taxonomy와 검증 가능성 체크리스트 정리에 한정됨.

**Benchmark results**

- 이 논문 자체의 새 실험은 없고 기존 약 150편의 결과를 인용해 정리함.
- 인용 사례로 SimpleVLA-RL은 시뮬레이터 success bit만을 reward로 GRPO를 적용해 task당 시연 1개로 초기화한 정책이 near-perfect 성능에 도달한다고 보고함(정확한 성공률은 본 survey 텍스트에서 확인 불가).
- 인용 사례로 HIL-SERL은 human-gated 개입을 replay buffer에 섞어 정밀 조작 task를 몇 시간 안에 near-perfect 성공률로 학습한다고 보고함.
- survey 범위는 약 150편, 검색 마감은 2026년 7월 초이며 2026년 논문 수는 상반기 관측치의 2배로 추정함.
- section 6의 구체적 9개 checkability metric 본문은 PDF 텍스트 추출 중 손실돼 본 리뷰에서 확인 불가.

**Top-tier conference 적합성 — 48/100 · 추천 venue: IJRR**

verifier taxonomy를 체계적으로 정리해 실용적 참고가치는 크지만 새 실험·방법 제안이 없어 CoRL·RSS 같은 학회 oral 기준과는 결이 다름. reject 위험은 기여가 기존 결과 재배열에 가깝고, 검증 메트릭 섹션의 구체적 근거가 이 텍스트에서 확인되지 않는 점임.

**추천 이유 & 누리랩 연구와의 연결점**

- failure detection·verifier가 누리랩 우선 주제이므로 availability-credibility 축을 test-time verifier·world model rollout 평가 설계에 그대로 적용할 수 있음.
- world model 기반 verifier(WorldEval, GVL 등) 정리는 world model 연구에서 reward·평가 설계 참고 자료로 쓸 수 있음.
- reward hacking 측정 논의는 VLA post-training에서 verifier를 reward로 쓸 때 과최적화 점검 체크리스트로 재사용할 수 있음.

---

## 오늘의 핵심 연구 트렌드 종합

- **world model 신뢰도 진단이 독립 연구 대상으로 부상** — [HaWMPO](https://arxiv.org/abs/2609.09941), [JEPA Policy](https://arxiv.org/abs/2609.09630), [Semigroup-JEPA](https://arxiv.org/abs/2609.10464), [Identifying Habit, Physics, and Nuisance](https://arxiv.org/abs/2609.09210) 네 편 모두 world model을 그대로 쓰는 대신 그 rollout이나 latent dynamics가 실제로 무엇을 학습했는지 점수화·분리·검증하는 데 초점을 맞춤.
- **action 표현을 주파수 영역에서 다루는 흐름 재부상** — [TFGCA](https://arxiv.org/abs/2609.09925), [FreqFM](https://arxiv.org/abs/2609.10405) 둘 다 DCT·wavelet으로 action chunk를 시간-주파수로 분해해 Flow Matching VLA에 조건화함. FAST·FreqPolicy 등 선행 연구가 이미 있어 조합형 기여 성격이 강함.
- **매니퓰레이션 파이프라인의 모듈화·명시적 중간표현** — [GTA-2](https://arxiv.org/abs/2609.09808)(4-agent VLM 파이프라인), [Show-Harness](https://arxiv.org/abs/2609.10522)(이산 semantic action+interpreter), [Programmable World Model](https://arxiv.org/abs/2609.10540)(rule engine+video renderer) 세 편 모두 end-to-end 대신 단계를 명시적으로 분리해 검증·수정 가능하게 만듦.
- **휴머노이드 whole-body 제어에 물리 기반 모델과 latent 추정 결합** — [SwingBot](https://arxiv.org/abs/2609.10283), [granular terrain locomotion](https://arxiv.org/abs/2609.10286) 두 편 모두 reference/keyframe guidance와 teacher-student latent 추정으로 배포 시 관측 불가능한 물리 상태(접촉·지반 강성)를 다룸.
- **생성 비디오·소량 시연을 시뮬레이션 학습 참조로 활용** — [GALATEA](https://arxiv.org/abs/2609.10050)(생성 비디오에서 HOI 궤적 복원), [Assembling Two Parts in One Hand](https://arxiv.org/abs/2609.10137)(사람 시연 한 장 리타겟팅) 두 편 모두 대규모 teleoperation 없이 참조 궤적을 만들어 RL을 학습시킴.
- **평가 방법론 자체가 연구 대상화** — [No Free Checker](https://arxiv.org/abs/2609.09250) survey가 verifier를 구하기 쉬운 정도(availability)와 그 판정을 믿을 수 있는 정도(credibility) 사이의 상충을 정리함. 위 world model 진단 트렌드와 문제의식이 맞물림.

## 유망 연구 방향 및 프로젝트 제안

**world model rollout 신뢰도를 test-time recovery 트리거로 통합**
- research question: HaWMPO의 hallucination score와 JEPA Policy의 future-consistency error를 하나의 runtime monitor로 결합해 실행 전/중 실패 예측 신호로 쓸 수 있는가.
- 접근·novelty: 두 신호를 하나의 monitor로 합치고, task별 threshold를 수동 calibrate하는 대신 counterfactual reasoning(다른 action을 가정했을 때 신뢰도 변화)으로 자동 조정함.
- 왜 지금·경쟁 prior works: 두 논문 모두 신뢰도 신호를 자기 pipeline 안에서만 검증했고 범용 failure detector로 확장하지 않음. No Free Checker가 지적한 availability-credibility trade-off를 정면 공략하는 지점이 비어 있음.
- risk·target venue: 서로 다른 world model에 신뢰도 모델이 이식되는지가 관건이며, threshold calibration에 실패하면 신호가 무의미해짐. CoRL/RSS.

**habit-physics-nuisance 분리를 매니퓰레이션 world model에 적용**
- research question: teleoperation 데이터의 operator habit을 분리해 학습한 world model이 실제로 다른 operator·embodiment에 더 잘 전이하는가.
- 접근·novelty: SCM+개입 실험을 DROID 같은 표준 매니퓰레이션 벤치마크로 확장하고, 물리 부분은 고정하고 인터페이스만 새 로봇에 맞춰 적응시키는 규칙(원 논문의 freeze-physics-adapt-interface)을 few-shot new-robot adaptation으로 검증함.
- 왜 지금·경쟁 prior works: 원 논문은 StackCube 단일 task이고 실로봇 검증이 없음. 이 공백을 채우는 것이 기여점임.
- risk·target venue: action은 habit과 physics의 합, 관측은 nuisance라는 causal 가정이 contact-rich task에서 깨질 위험이 있음. RSS/CoRL.

**action frequency 분해 기반 test-time 재계획 트리거**
- research question: action chunk의 고주파 correction 성분 급증이 실제 실패·contact anomaly를 예측하는 조기 신호로 쓰일 수 있는가.
- 접근·novelty: TFGCA·FreqFM이 future work로만 남긴 아이디어(고주파 성분으로 재계획 주기 결정)를 실제 구현하고, TFGCA의 고주파 attention 신호 급증을 재시도 트리거로 사용함.
- 왜 지금·경쟁 prior works: 두 논문 다 이 방향을 실험 없이 future work로 남겨 둠. FAST 계열도 online monitoring까지는 확장하지 않음.
- risk·target venue: 주파수 신호가 task-specific이라 범용 threshold 설계가 어려움. ICRA/CoRL.

**dual-view world model과 object-centric 3DGS 결합한 active perception**
- research question: [DUET-DINO](https://arxiv.org/abs/2609.10506)(side·wrist 카메라를 상호 조건화하는 dual-view latent world model)의 cross-view 조건화를 3DGS 표현과 결합하면 특정 순간에 필요한 view를 능동적으로 선택할 수 있는가.
- 접근·novelty: cross-attention 가중치를 view informativeness 신호로 재활용해 next-best-view 선택에 사용함.
- 왜 지금·경쟁 prior works: DUET-DINO는 고정된 두 view만 쓰고 view 선택 문제 자체는 다루지 않음. 3DGS·scene graph 결합은 검증되지 않음.
- risk·target venue: 3DGS 렌더링 비용이 real-time planning에 부담됨. latency 검증이 관건임. CoRL/ICRA.

**명시적 중간표현 파이프라인의 자동 실패 진단 orchestrator**
- research question: GTA-2·Show-Harness처럼 단계별 명시적 출력을 남기는 파이프라인에서 human feedback 대신 자동 orchestrator VLM이 실패 단계를 진단·재실행할 수 있는가.
- 접근·novelty: 두 논문 모두 human feedback으로 stage를 재실행하는데, 이를 실행 모니터링 기반 자동 진단 loop로 대체함.
- 왜 지금·경쟁 prior works: 두 논문 다 future work로만 언급했고 실제 구현 사례가 없음.
- risk·target venue: 진단 정확도가 낮으면 무한 재시도 루프에 빠질 위험이 있음. CoRL.

## 오늘 반드시 읽어야 할 논문

- [Programmable World Model](https://arxiv.org/abs/2609.10540) — world state를 explicit rule engine으로 분리해 오차 누적을 구조적으로 피한 설계로, 오늘 최고점을 받음.
- [Show-Harness: Just a VLM Agent Can Play Robots](https://arxiv.org/abs/2609.10522) — 이산 semantic action+deterministic interpreter로 VLM이 직접 물리 결정을 내리게 한 구조가 VLA formulation 논의에 참고할 만함.
- [JEPA Policy](https://arxiv.org/abs/2609.09630) — future-consistency error를 학습 목적함수의 부산물로 얻어 failure detection에 바로 붙일 수 있는 실용적 진단 신호를 제공함.
- [Time-Frequency Geometric Cross-Attention (TFGCA)](https://arxiv.org/abs/2609.09925) — action chunk를 시간-주파수로 분해하는 관점이 failure detection·test-time optimization에 응용 가능함.
- [Semigroup-JEPA](https://arxiv.org/abs/2609.10464) — world model이 훈련 분포 밖 물리 조건으로 실제 일반화하는지 검증하는 실험 프로토콜 자체가 평가 설계에 참고할 가치가 있음.
- [Grounding Generated Video Plans (GALATEA)](https://arxiv.org/abs/2609.10050) — 생성 비디오를 시뮬레이션 grounding 참조로 쓰는 파이프라인, 실패 사례가 test-time recovery 데이터로 쓸 만함.
- [DUET-DINO](https://arxiv.org/abs/2609.10506) — dual-view cross-attention으로 rotation·gripper까지 포함한 fine-grained latent planning을 처음 다룸.
- [Identifying Habit, Physics, and Nuisance in Robot World Models](https://arxiv.org/abs/2609.09210) — teleoperation 데이터의 operator habit을 물리 법칙과 분리하는 causal formulation이 counterfactual reasoning 주제와 정확히 맞물림.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (316편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2609.09925'>Time-Frequency Geometric Cross-Attention for Chunked Vision-Language-Action Models</a></td><td>70</td><td>9</td><td>VLA</td><td>action chunk를 wavelet으로 시간-주파수 분해하고 wedge product로 위상 간 near-orthogonal 관계를 포착하는 cross-attention 모듈임. LIBERO·LIBERO-Plus·RoboTwin과 실로봇 AgiBot A2에서 일관된 개선을 보여 증거가 강하고 기존 VLA에 drop-in 가능한 새 representation 설계임</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2609.09941'>HaWMPO: Hallucination-Aware World Model-based Policy Optimization for Generalist Robot Policy</a></td><td>68</td><td>10</td><td>World Model/VLA</td><td>world model rollout의 hallucination을 점수화해 GRPO 보상에 반영하는 VLA post-training, LIBERO와 실로봇 G1 모두에서 개선을 확인함</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2609.09210'>Identifying Habit, Physics, and Nuisance in Robot World Models</a></td><td>68</td><td>9</td><td>World Model</td><td>teleoperation 시연의 multimodality를 습관·물리·관측 nuisance로 분리하는 구조적 인과모델을 제안하고 action 개입 실험으로 검증함. world model의 next-obs predictor가 세 요인을 뒤섞는 문제를 새 formulation으로 짚었고 StackCube/DROID/RH20T에서 low-shot 전이 개선을 보임.</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2609.09808'>GTA-2: A Multi-VLM Framework for Synthesizing Robot Manipulation Skills via Grounded Task Axes</a></td><td>64</td><td>9</td><td>Manipulation/VLA</td><td>4개 VLM이 task-axis를 분해·grounding해 zero-shot 매니퓰레이션 스킬을 만드는 프레임워크, 실로봇 14개 task에서 baseline 대비 31.4%p 앞섬</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2609.10464'>Semigroup-JEPA: Latent Dynamics Consistency for Zero-Shot Physics Generalization</a></td><td>62</td><td>7</td><td>World Model</td><td>JEPA world model에 물리 파라미터를 action-conditioning으로 주입해 미지 중력장으로 제로샷 일반화시킴. DINO-WM 대비 open-loop 오차를 2배, 3D 로봇 태스크에서 diffusion policy 제어 성공률을 최대 2.5배 개선하고 이득의 원인이 인코더 표현 개선임을 분석적으로 보임.</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2609.10506'>DUET-DINO: Simultaneous Cross-View World Modeling for Latent Planning in Robot Manipulation</a></td><td>60</td><td>10</td><td>World Model/Manipulation</td><td>정면·손목 카메라를 동시에 조건화하는 cross-view latent world model로 7-DoF 전체 액션 공간의 latent planning을 가능케 함, DINOv3가 V-JEPA2보다 action-conditioned 변화를 잘 포착함을 보임</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2609.10540'>Programmable World Model</a></td><td>60</td><td>6</td><td>World Model</td><td>자연어를 실행가능한 상태전이 프로그램으로 변환해 world state를 시각생성과 분리하는 새로운 formulation을 제시했고 world model의 지속성·제어가능성에 본질적으로 기여함</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2609.10405'>Frequency-Conditioned Flow Matching for Vision-Language-Action Models</a></td><td>58</td><td>10</td><td>VLA</td><td>flow matching 기반 VLA의 액션 생성을 DCT 주파수 성분별로 조건화하는 방법, LIBERO-Plus에서 9.3점 개선과 실로봇 6개 task로 검증함</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2609.09630'>JEPA Policy: Diffusion-Free Imitation Learning via Paired Action and Future Representation Prediction</a></td><td>58</td><td>9</td><td>VLA</td><td>diffusion 없이 action chunk와 미래 표현을 짝지어 예측하는 JEPA 기반 모방학습 정책을 제안함. 9개 시뮬레이션 태스크와 5태스크 630 episode 실기체 실험에서 Diffusion Policy를 능가하며 지연시간을 0.29ms만 추가해 low-latency VLA 대안으로 실용성이 큼.</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2609.10050'>Grounding Generated Video Plans in Simulation Towards Versatile Dexterous Controllers</a></td><td>58</td><td>9</td><td>Manipulation/Video</td><td>생성한 HOI 비디오를 시뮬레이션 tracker로 grounding해 1500개 이상 참조 동작을 확보하는 파이프라인, 실로봇 폐루프 실험까지 검증함</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2609.10286'>Learning Terrain-Adaptive Humanoid Locomotion on Granular Terrain</a></td><td>57</td><td>8</td><td>Locomotion</td><td>3D resistive force theory 기반 물리적 granular contact 모델로 RL을 학습해 실제 자갈·모래 지형에서 agile 휴머노이드 보행을 처음 시연함</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2609.10283'>SwingBot: Learning Whole-Body Brachiation for Humanoid Robots</a></td><td>56</td><td>8</td><td>Locomotion</td><td>휴머노이드에 수동 손목 훅으로 brachiation을 학습시킨 첫 사례, biomimetic keyframe으로 탐색을 유도해 하드웨어에서 연속 바 이동을 시연함</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2609.10137'>Assembling Two Parts in One Hand</a></td><td>55</td><td>9</td><td>Dexterous Manipulation</td><td>한 손 안에서 두 부품을 조립하는 in-hand assembly를 RL로 학습, CoRL 2026 게재 확정이며 3개 task에서 sim-to-real zero-shot을 확인함</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2609.09250'>No Free Checker: A Survey of Verifiers for Robot Policies</a></td><td>55</td><td>8</td><td>Manipulation</td><td>로봇 정책 검증기 약 150개를 availability와 credibility 두 축으로 체계화한 서베이임. failure detection·verifier 우선 주제와 직결되고 신규 실험은 없지만 검증 가능한 9개 메트릭을 제시해 실용적 참고가치가 큼.</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2609.10522'>Show-Harness: Just a VLM Agent Can Play Robots</a></td><td>54</td><td>9</td><td>VLA/Embodied AI</td><td>semantic action unit 인터페이스로 VLM이 직접 로봇을 제어하게 하는 프레임워크, closed-source VLM의 zero-shot 제어와 소형 VLM의 경량 파인튜닝을 모두 지원함을 보임</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2609.09918'>ViBe: Visual Behavior Adaptation for Perceptive Humanoid Whole-Body Control</a></td><td>54</td><td>8</td><td>Embodied AI/Locomotion</td><td>사전학습 visual encoder를 LoRA로 motion tracker에 이식해 perceptive humanoid 제어를 post-training함, 4개 task sim-to-real 검증했으나 파라미터 효율화 범주의 기여임</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2609.10033'>What Symmetry Buys a Learned Motion Planner</a></td><td>53</td><td>7</td><td>Motion Planning</td><td>start-goal 좌표계 하나로 SE(3) 대칭의 대부분을 공짜로 얻는다는 것을 실험적으로 분리해 보임, 충돌회피율을 14.6%에서 51.1%로 크게 개선함</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2609.10307'>View-Structured Conformal Prediction for 3D Gaussian Splatting</a></td><td>52</td><td>5</td><td>3D Vision</td><td>3D Gaussian Splatting 렌더링에 conformal prediction으로 view별 coverage 보장을 부여함. object-centric 3D representation의 불확실성 정량화로 active perception/NBV에 실용적이고, 13개 실 scene과 Mip-NeRF360에서 폭을 20% 이상 줄이며 216-280 FPS를 유지함.</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2609.09394'>OmniPoint: Universal Monocular Metric Pointcloud from Any Camera</a></td><td>52</td><td>4</td><td>3D Vision</td><td>카메라 모델 무관 metric point cloud 통합 프레임워크로 decoupled ray-distance representation을 제안했고 robot perception에 활용 가능함</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2609.09163'>World-Time Compute with Verified Code World Models</a></td><td>52</td><td>4</td><td>World Model</td><td>코드로 검증가능한 world model을 대량 생성해 학습시키는 새로운 training-time compute 패러다임이고 world model 일반화에 통찰을 주나 symbolic state로 범위가 제한됨</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2609.10243'>FolDeX: A Physical-World Benchmark for Long-Horizon Robotic Manipulation of Deformable Objects</a></td><td>50</td><td>9</td><td>Manipulation/Benchmark</td><td>옷 접기 중심 장기 horizon deformable manipulation 실로봇 벤치마크로 2000시간 이상 데이터를 공개, 벤치마크 기여라 방법론적 신규성은 제한적임</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2609.10210'>Through the Looking Glass: Directly Reading and Writing Transformers</a></td><td>50</td><td>0</td><td>NLP/Interpretability</td><td>signed contribution 기준으로 예측을 지탱하는 부분집합이 모델 크기와 무관하게 수십 개 수준임을 12개 모델에서 보이고, 학습 없이 개념을 유닛에 설치하는 편집까지 시연한 견고한 해석가능성 연구임</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2609.09507'>RoMa-$Ω$: What Feed-Forward 3D Models Know About Image Matching</a></td><td>49</td><td>3</td><td>3D Vision</td><td>feed-forward 3D 모델의 매칭 능력을 분석해 강한 matcher로 재훈련했고 visual localization에 유용하나 robotics 직접 검증은 없음</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2609.09597'>Compact Visuotactile World Models for Lifting: Prediction, Reward Alignment, and Force Constraints</a></td><td>48</td><td>8</td><td>World Model</td><td>touch를 더한 compact visuotactile world model로 접촉력 예측과 force-constrained lifting 제어를 분석함. tactile perception과 world model 우선 주제에 부합하고 force budget 내 성공률에서 force feedback 이득을 정량화했으나 MuJoCo 시뮬레이션에 한정됨.</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2609.09492'>Actuator Dynamics Curricula for Narrow-Viability Tasks in Legged Robot Learning</a></td><td>48</td><td>7</td><td>RL</td><td>관절 강성을 점진적으로 조여 viability kernel을 넓히는 actuator dynamics 커리큘럼을 제안하고 Spot의 handstand 전이를 실기체로 검증함. CoRL 2026 accept, 탐색 실패가 termination에서 오는 narrow-viability task에 새 축을 제시함.</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2609.10021'>RoboDrop: Curating VLA Post-Training Data via Local Gradient Compatibility</a></td><td>47</td><td>7</td><td>VLA/Data Curation</td><td>gradient compatibility로 VLA post-training 데이터를 자동 정제하는 방법, 실로봇 성공률을 35%에서 67.5%로 크게 올렸지만 데이터 큐레이션 범주의 기여임</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2609.09528'>MotionBlind: Probing the Illusion of Motion Understanding in Video-LLMs</a></td><td>46</td><td>5</td><td>Video</td><td>video-LLM이 속도·방향 같은 운동정보를 읽지 못함을 보인 벤치마크이고 world model의 perceptual frontend 신뢰성에 직접적 시사점을 줌</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2609.10308'>Deformable Object Manipulation under Partial Observability via Real-Time Full-Shape Estimation</a></td><td>45</td><td>7</td><td>Manipulation</td><td>corner 관측만으로 변형체 전체 형상을 실시간 추정하는 경량 cRVAE를 MPC에 결합, Go2 로봇에서 XPBD보다 수백 배 빠른 추론으로 검증함</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2609.09491'>Learning Global Camera Poses from Noisy View-Graphs for Structure from Motion</a></td><td>44</td><td>3</td><td>3D Vision</td><td>GNN 기반 view-graph 집계로 global SfM pose를 학습했고 robot navigation·mapping에 활용 가능한 3D reconstruction 기여임</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2609.10036'>Belief-State Engine: Augmenting LLMs for Principled Planning Under Partial Observability</a></td><td>42</td><td>4</td><td>Embodied AI</td><td>LLM agent에 POMDP belief state를 명시적으로 유지시키는 아키텍처임. Bellman optimality를 증명하는 이론적 기여가 있으나 Tiger POMDP·공격그래프 도메인이고 실로봇 검증은 없음</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2609.09985'>VLX-VR: An Agentic-Aware Video Reasoning Model</a></td><td>42</td><td>3</td><td>Video/Multimodal</td><td>Think-Memory-Observation 루프로 비디오 증거를 능동적으로 조회하는 agentic video reasoning 모델, MINERVA에서 78.79%로 SOTA를 냈으나 로봇 도메인은 아님</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2609.10377'>Data-Driven Risk Fields for Safer End-to-End Autonomous Driving</a></td><td>40</td><td>5</td><td>Autonomous Driving</td><td>규칙 기반 안전 prior를 pairwise risk label로 바꿔 end-to-end 주행 계획에 상대적 위험 순서를 학습시킴, Bench2Drive에서 개선을 보였으나 자율주행 도메인 특화임</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2609.10531'>Guiding Image-to-3D Generation with Test-Time Partial Observations</a></td><td>40</td><td>3</td><td>3D Vision</td><td>test-time에 부분 관측을 ray-consistent likelihood로 주입해 image-to-3D 기하 충실도를 개선했고 test-time optimization 주제와 직접 연관됨</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2609.10052'>Direct Diversity Optimization for Diverse Successful Trajectories in Preference Post-Training</a></td><td>40</td><td>3</td><td>RL/Agents</td><td>동일 결정 상태에서 분기한 성공 궤적들을 보존하도록 offline post-training하는 방법, BabyAI·WebShop 등 텍스트 에이전트에서 검증했고 로봇 스킬 다양성 확보에 참고할 만함</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2609.09682'>Settling: Equilibrium Inference for Non-Convex Validity Sets</a></td><td>40</td><td>2</td><td>LG</td><td>다봉 분포에서 conditional mean collapse를 막는 equilibrium 기반 추론 연산자를 제안함. VLA의 multimodal action 예측에도 시사점 있으나 검증이 toy geometric 세팅에 머무름.</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2609.09745'>PccDiffuser: Multi-solution Motion Planning for Continuum Robots</a></td><td>38</td><td>6</td><td>Manipulation</td><td>연속체 로봇을 위한 diffusion 기반 multi-solution 모션 플래너로 미분가능 운동학을 denoising에 결합함. 실기체 3분절 텐던 로봇 실험을 포함하나 기존 diffusion planning을 continuum robot에 적용한 수준임.</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2609.10322'>Geometry Without Coordinates: LiDAR Diffusion as a 3D Feature Bridge</a></td><td>38</td><td>3</td><td>3D Vision</td><td>2D foundation model 지식을 LiDAR 조건부 diffusion으로 3D에 전이해 구조화된 표현을 학습했고 robot perception에 유용한 3D representation 분석임</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2609.09206'>MLLMs Hallucinate when Information Distribution Drifts in Synergy Heads</a></td><td>38</td><td>1</td><td>Multimodal</td><td>MLLM hallucination을 head-level 정보드리프트로 설명하는 해석가능성 기여이나 robotics와 무관함</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2609.09902'>Contrastive Projection: Reading Transformer Internals by Differencing Logit Lenses</a></td><td>38</td><td>0</td><td>NLP/Interpretability</td><td>매칭된 프롬프트 쌍의 hidden state 차이를 logit lens로 읽어 공통 성분을 제거하는 학습 없는 해석 기법, activation patching으로 교차검증했지만 로봇과는 무관함</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2609.09778'>ROAM: Robust Organization of Atomic Memories for Agents through Semantic Relations</a></td><td>36</td><td>2</td><td>NLP/Agent Memory</td><td>LLM 에이전트의 atomic memory를 관계 기반으로 분류·융합해 관리하는 프레임워크, 로봇 메모리 설계에 참고할 수 있으나 언어 에이전트 대상 연구임</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2609.09213'>Geometry Conditioning in an Embodied SLM: Training Controls and Robustness Diagnostics in a 0.8B Hybrid Model</a></td><td>35</td><td>6</td><td>VLA</td><td>0.8B 하이브리드 embodied SLM에서 기하 조건화 방식별 성공률을 LIBERO-Spatial로 비교함. 학습시 기하 정렬이 일관된 이득을 주지 않는다는 negative result이고 모델·태스크 규모가 작아 일반화는 제한적임.</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2609.09650'>A Risk-Sensitive and Uncertainty-Aware Decision-Making and Control Framework for Safe and Robust Autonomous Driving</a></td><td>35</td><td>5</td><td>RL</td><td>분포적 risk-sensitive RL과 불확실성 인지 CBF 안전필터를 결합한 무신호 교차로 자율주행 프레임워크임. 안전-효율 균형은 보이나 기존 요소들의 조합 성격이 강함.</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2609.10215'>Adaptive Shared Control with Online Bounded-Rational Human Behavior Estimation</a></td><td>35</td><td>5</td><td>HRI/Control</td><td>level-k bounded rationality로 인간 행동을 온라인 추정해 공유제어에 반영하는 제어이론 연구, 로봇 정책학습과는 다른 트랙임</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2609.09418'>Valerant: An Automatic Navigable Game Map Generator via Action-Conditioned World Model Exploration</a></td><td>35</td><td>3</td><td>World Model</td><td>action-conditioned world model rollout과 SLAM을 결합해 3D 게임 맵을 구성하는 training-free 프레임워크임. world model 활용 방식은 흥미롭지만 실로봇 검증이 없고 게임 도메인 한정임</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2609.10315'>TRACE: Training Reasoning Agents for Causal Exploration with Synthesized Rewards</a></td><td>35</td><td>3</td><td>RL</td><td>시뮬레이터에 개입을 주입해 oracle reward를 만들고 RL로 진단 reasoning을 학습시키는 방법임. counterfactual 개입 기반 검증 가능한 reward 설계는 실패 진단에 응용 가능한 아이디어이나 광고 도메인 한정임</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2609.09676'>Muon-C: Operator-Aligned Muon for Convolutional Kernels</a></td><td>35</td><td>1</td><td>LG</td><td>convolution kernel에 맞춘 operator-aligned Muon optimizer로 FID를 크게 개선함. 최적화 이론 기여이나 로보틱스와 직접 관련은 없음.</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2609.09899'>Strangers to Themselves: What Language Models Say About Themselves Is Generic</a></td><td>35</td><td>1</td><td>NLP</td><td>LLM의 자기 행동 예측이 실제로는 일반 AI 에이전트 이론일 뿐 자기 지식이 아님을 9개 실험으로 보임. self-report 신뢰성 문제로 agent 평가에 시사점 있으나 로보틱스와 직접 관련은 낮음.</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2609.10166'>Future-Aware Flow Planning for Safe UAV Target Following</a></td><td>34</td><td>5</td><td>Navigation</td><td>타겟 미래 경로를 조건으로 한 UAV flow planning으로 안전-추적 트레이드오프를 개선하나 누리랩 핵심 주제와는 거리가 있음</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2609.09881'>CLFTv2: Efficient Camera-LiDAR Fusion for Semantic Segmentation via Hierarchical Feature Pyramids</a></td><td>34</td><td>4</td><td>3D Vision</td><td>자율주행용 카메라-라이다 계층적 융합 분할이고 효율성 중심 엔지니어링 개선임</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2609.09606'>RouteBridge: Reliability-Routed Bidirectional Distillation Between Neural Radiance Fields and 3D Gaussian Splatting</a></td><td>34</td><td>2</td><td>3D Vision</td><td>NeRF-3DGS 양방향 distillation으로 렌더링 품질을 개선했고 object-centric 3D representation과 연관되나 벤치마크 개선 수준임</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2609.09989'>Stable Answers, Unfinished Reasoning: Why Self-Consensus Is Not a Safe Early-Exit Signal</a></td><td>34</td><td>1</td><td>NLP/LLM Reasoning</td><td>self-consensus가 추론 종료 신호로 안전하지 않음을 3520개 규칙 사전등록 스윕으로 보인 견고한 실증 연구, robotics와는 무관함</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2609.09949'>Vague2Detect: Handling Ambiguous Prompts in Knowledge-Based Open-World Detection</a></td><td>33</td><td>3</td><td>Embodied AI</td><td>LLM 지식베이스로 모호한 프롬프트를 open-world detection에 연결했고 가정환경 객체탐지로 embodied 응용과 연관되나 파이프라인 조합 수준임</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2609.09184'>Evidence-Order Calibration for Selective Visual Reasoning under Progressive Loss of Question-Critical Evidence</a></td><td>33</td><td>1</td><td>Multimodal</td><td>VLM 신뢰도 보정 벤치마크 분석이고 robotics와 무관하며 방법론적 기여가 제한적임</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2609.09448'>Do Agents Know When They Succeed? Calibrating Agent Confidence from Internal Representations</a></td><td>32</td><td>3</td><td>AI</td><td>internal representation으로 agent의 성공 여부를 예측하는 방법임. failure detection과 맥락이 닿지만 bash·SQL·Python agent 대상이고 로봇 실험은 없음</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2609.09737'>Distilling Image Prototypes for Guided Test-Time Adaptation</a></td><td>32</td><td>2</td><td>CV</td><td>test-time adaptation에서 synthetic prototype으로 forgetting과 오류누적을 억제했고 test-time optimization 주제와 연관되나 일반 분류 TTA에 그침</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2609.09417'>Vision-language models know more about agriculture than they show and rubric-grounded verifications close the gap</a></td><td>32</td><td>1</td><td>Multimodal</td><td>rubric 기반 test-time verification으로 VLM 잠재지식을 끌어내는 기법이나 농업 도메인 특화임</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2609.09478'>Unthrottling the Tanh Jacobian in SAC: A Negative Result on Bang-Bang Control and MetaDrive</a></td><td>31</td><td>4</td><td>RL</td><td>SAC의 tanh Jacobian이 bang-bang control 성능을 저해한다는 가설을 반증한 negative result이고 MetaDrive 주행 제어에서 검증됨</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2609.09468'>Building the Harness Automatically: Self-Play in Code Distills a Text Harness for Black-Box Optimization</a></td><td>31</td><td>1</td><td>LG</td><td>코드 self-play로 블랙박스 최적화 전략을 텍스트로 증류해 LLM 간 전이시킨 연구이고 에이전트 자기개선 관점에서 흥미로움</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2609.09217'>Design and Attitude Control of an Underwater Quadruped Robot</a></td><td>30</td><td>5</td><td>Manipulation</td><td>수중 사족 로봇의 방수 관절 설계와 SO(3) 자세 제어를 구현하고 수조 실험으로 검증함. 하드웨어 엔지니어링 중심이고 학습적 novelty는 낮음.</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2609.09234'>Learning to Fly: Stable Vision-Guided UAV Servoing with Compact Target-Centric Cues and Reinforcement Learning</a></td><td>30</td><td>5</td><td>RL</td><td>타겟 중심 저차원 관측으로 UAV 비주얼 서보잉을 RL로 학습하고 커리큘럼 세 가지를 비교함. 견고성 개선은 보이나 기존 커리큘럼 RL의 조합 수준임.</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2609.09380'>AccelMPC: High-Rate, Low-Power FPGA-Accelerated Model Predictive Control for Tiny Drones</a></td><td>30</td><td>5</td><td>Manipulation</td><td>FPGA 가속 ADMM MPC를 35g 드론에 탑재해 1kHz 제어를 달성한 하드웨어 co-design 논문임. 임베디드 제어 엔지니어링 중심이고 학습 기반 기여는 없음.</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2609.09403'>A Decade of Bayesian Optimization for Controller Tuning and Robot Learning: Tutorial, Review, and Future Prospects</a></td><td>30</td><td>5</td><td>RL</td><td>controller tuning과 robot learning에서의 Bayesian optimization 10년을 정리한 튜토리얼·리뷰이고 벤치마크 제안을 포함함. 신규 실험 없는 서베이임.</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2609.09612'>MuJoCable: Reduced-Order Surface-Routed Cable Transmission for Tendon-Driven Robots</a></td><td>30</td><td>5</td><td>Manipulation</td><td>MuJoCo에 표면 라우팅 케이블 전달을 추가한 reduced-order 시뮬레이션 플러그인임. tendon 로봇 sim-to-real 격차를 다루는 유용한 툴이나 학습적 기여는 아님.</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2609.10339'>A Confidence-Aware Multimodal Fusion Framework for Industrial Human-Robot Collaboration</a></td><td>30</td><td>5</td><td>HRI</td><td>산업용 HRC에서 4개 모달리티를 신뢰도 기반으로 융합해 의도를 예측하는 BiLSTM 프레임워크로 응용 엔지니어링 수준임</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2609.09752'>HiRAD: A Flexible Large-Scale AGV Routing System</a></td><td>30</td><td>4</td><td>RL</td><td>연속공간 AGV 대규모 라우팅을 계층적 RL과 비동기 이벤트 파이프라인으로 가속한 산업 시스템임. makespan과 지연시간 개선이 크지만 물류 MAPF 문제로 매니퓰레이션·embodied 연구와는 거리가 있음.</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2609.09359'>DensePol: Dense-Angle Polarization Dataset for Learning-Based Polarimetric Vision</a></td><td>30</td><td>2</td><td>3D Vision</td><td>고밀도 편광 데이터셋 구축 논문이고 robot perception에 잠재적으로 유용하나 데이터셋 성격에 가까움</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2609.09790'>LogiScope-VQA: Benchmarking Vision-Language Models for Logistics Hazard Identification in Industrial Scenarios</a></td><td>30</td><td>2</td><td>Multimodal</td><td>물류창고 위험식별 VQA 벤치마크이고 산업현장 인지라는 점에서 embodied 맥락과 약하게 연관됨</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2609.10292'>Isotropic Embedding Perturbations for Robust Vision Language Encoders</a></td><td>30</td><td>1</td><td>Multimodal</td><td>임베딩 공간에서의 등방적 perturbation augmentation으로 vision-language encoder를 정규화한 기법임</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2609.10158'>CoGe-GCD: Reframing Generalized Category Discovery with Compositional Generalization</a></td><td>30</td><td>1</td><td>CV</td><td>패치 토큰을 primitive 어휘로 구조화해 구성적 일반화 기반 category discovery를 재구성함. ICML 2026 accept, 표현학습 기여이나 embodied 적용은 없음.</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2609.09776'>Proof-Carrying Cognition: Closing the Verification Gap with Reality-Settled Reward</a></td><td>30</td><td>1</td><td>RL</td><td>reasoning RL의 verification gap을 이론과 실험으로 분석한 연구임. reward hacking 이론은 탄탄하나 robotics 적용은 없음</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2609.09909'>Interpreting Object-Dependent Concept Brittleness in Text-to-Image Diffusion Models</a></td><td>30</td><td>0</td><td>CV</td><td>text-to-image 모델의 object별 개념 실패를 sparse autoencoder로 해석·교정한 연구이고 robotics와 무관함</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2609.09595'>Teacher Geometry Shapes Learnability in Teacher-Student Networks</a></td><td>30</td><td>0</td><td>LG</td><td>teacher-student 네트워크에서 teacher 파라미터 기하구조가 학습 가능성을 좌우함을 이론적으로 분석함. 흥미로운 이론이나 로보틱스 적용성은 낮음.</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2609.10154'>CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts</a></td><td>30</td><td>0</td><td>NLP</td><td>cross-family on-policy distillation에서 teacher-family offset을 제거해 전이 효과를 개선함. LLM distillation 기여이나 로보틱스와 무관함.</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2609.10357'>A Later Test Set Is Not a New Domain: Pretraining Familiarity Survives a Contamination-Free Hold-Out</a></td><td>30</td><td>0</td><td>LG</td><td>시계열 foundation model의 hold-out이 사실 사전학습 코퍼스 친숙도를 반영할 뿐 새 도메인이 아님을 실증함. 벤치마크 오염 문제를 잘 짚은 negative result이나 로보틱스와 무관함.</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2609.09696'>When Auditors Fabricate: Batch-Size Degradation and Confident Hallucination in LLM Detection of Planted Document Contamination</a></td><td>30</td><td>0</td><td>NLP/LLM Reliability</td><td>LLM 문서 감사 시 배치 크기가 커지면 탐지율이 급락하고 없는 오염을 지어내는 실패 양상을 실증함, 로봇과 무관하나 신뢰성 분석으로 흥미로움</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2609.09477'>LeCor: Learning to Be Corrected by Meta-Learned Test-Time Training for Interactive 3D Lung-Tumour Segmentation</a></td><td>29</td><td>2</td><td>CV</td><td>meta-learned test-time training으로 상호작용 분할을 개선했고 test-time optimization 관점에서 의미는 있으나 의료 도메인 한정임</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2609.10008'>Beyond Similarity: Foundation Models as an Efficient Backbone for Training-Free Composed Video Retrieval</a></td><td>29</td><td>1</td><td>Video</td><td>훈련없이 foundation model을 난이도별로 orchestrate하는 composed video retrieval이고 retrieval 벤치마크 개선 수준임</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2609.10224'>UOT-Gap: A Variational Principle for the Modality Gap in Vision-Language Models via Unbalanced Optimal Transport</a></td><td>29</td><td>0</td><td>Multimodal</td><td>unbalanced optimal transport로 CLIP modality gap을 진단하는 training-free 분석이고 robotics와 무관함</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2609.09410'>Benchmarking Hybrid Deep Research Across Database Querying and Web Search</a></td><td>29</td><td>0</td><td>NLP/Agents</td><td>웹 검색과 SQL을 함께 요구하는 deep research 벤치마크로 SOTA 모델도 hard subset에서 50% 내외에 그침을 보임</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2609.09627'>Seven Sources of Physical AI Capability Formation</a></td><td>28</td><td>4</td><td>Embodied AI</td><td>Physical AI 능력이 형성되는 7가지 원천을 분류한 taxonomy 논문임. robot learning 패러다임 정리에는 유용하나 새 방법론 제안은 없음</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2609.09898'>Grounded Evaluation and Repair for NL-to-PDDL Problem Generation</a></td><td>28</td><td>3</td><td>Embodied AI</td><td>자연어 계획 설명을 PDDL 문제로 변환·검증·수리하는 파이프라인임. TAMP에 쓰이는 PDDL grounding 도구로 유용하나 robot 실험은 없음</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2609.10297'>TRACE: Trajectory-robust Admission with Evidence Ordering for Efficient GUI Agents</a></td><td>28</td><td>2</td><td>Multimodal</td><td>GUI agent용 궤적강건 토큰 pruning이고 VLA의 효율적 추론과 유사한 문제구조이나 도메인은 GUI에 한정됨</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2609.09774'>Procedural Memory Under Change: Reuse and Interference in Controlled Web Tasks</a></td><td>28</td><td>2</td><td>AI</td><td>저장된 절차적 memory가 상황 변화 시 오작동하는지 통제 실험한 연구임. robot skill reuse와 맥락이 통하나 web agent 대상이고 결과도 비확정적임</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2609.09895'>Can We Trust Video Hallucination Detectors? VidHalLoc for Evaluating the Evaluators</a></td><td>28</td><td>1</td><td>Multimodal</td><td>비디오 hallucination 탐지기의 신뢰성을 평가하는 진단적 벤치마크임</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2609.09764'>SocialRL: Refining LLMs&#x27; Social Intelligence through Multi-turn Reinforcement Learning and Reward Design</a></td><td>28</td><td>1</td><td>NLP/RL</td><td>다중 턴 대화에서 목표-관계 균형을 위한 6개 프로세스 보상으로 PPO를 학습, 언어 에이전트 대상이라 로봇 RL과는 거리 있음</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2609.10155'>From Retrieval to Weights: Parametric Individualization of Small Language Models with Individual Text Corpora</a></td><td>28</td><td>1</td><td>NLP/Personalization</td><td>개인 검색 이력을 DoRA로 소형 LM 가중치에 주입하는 인지모사 연구, 지식은 더해지지만 답변 정합 자체는 개선되지 않음을 보임</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2609.10221'>Why Sample What You Can Enumerate? Exact Policy Optimization for Genomic Tool Selection</a></td><td>28</td><td>1</td><td>RL</td><td>tool 부분집합이 열거 가능할 때 GRPO의 advantage 소실 문제를 exact policy optimization으로 해결한 연구임. genomic tool 선택 도메인이나 RL 알고리즘 통찰은 일반화 가능함</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2609.09486'>Efficient Fairness Auditing Across Guidance Scales in Text-to-Image Diffusion Models via Causal Abstraction</a></td><td>28</td><td>0</td><td>CV</td><td>T2I diffusion guidance scale에 대한 causal abstraction 기반 fairness 감사 프레임워크임. 방법은 참신하나 robotics와 무관한 fairness auditing 문제임.</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2609.10299'>A Dominant Diffuse Phase in the Sparse Autoencoder Phase Diagram</a></td><td>28</td><td>0</td><td>LG</td><td>sparse autoencoder가 이론적 merge 상 대신 diffuse phase로 수렴함을 대규모 실험으로 보인 해석가능성 연구임. 음의 결과를 rigorous하게 규명했으나 로보틱스와 무관함.</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2609.09233'>Subagents vs Agent Skills: Executing Reusable Knowledge for Long-Horizon Agentic Tasks</a></td><td>28</td><td>0</td><td>AI</td><td>long-horizon agent task에서 skill을 subagent로 실행하는 게 유리함을 보인 연구임. 실용적 통찰이나 순수 LLM agent 엔지니어링 범위임</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2609.09589'>A Function-Space Approach to the Statistical Mechanics of Learning Dynamics</a></td><td>28</td><td>0</td><td>LG</td><td>학습 동역학을 function space에서 통계역학적으로 기술한 이론 연구임. 이론적 깊이는 있으나 실험적 검증이 약하고 robotics 응용은 없음</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2609.10336'>Odometer-Agnostic Drift Correction Using OpenStreetMap Lane Geometry</a></td><td>27</td><td>4</td><td>SLAM</td><td>OSM 차선 중심선에 궤적을 정렬해 odometry drift를 보정하는 경량 방법으로 로봇학습과는 거리가 있는 엔지니어링 기여임</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2609.10095'>LinearMask-GS: Stable-Mask Importance Pruning for Compact 3D Gaussian Splatting</a></td><td>27</td><td>2</td><td>3D Vision</td><td>Gumbel-Sigmoid 대신 선형증분 활성화로 3DGS pruning 마스크를 안정화한 compression 성격의 점진적 개선임</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2609.09300'>Video-MOPD: Multi-Teacher On-Policy Distillation for Video Understanding</a></td><td>27</td><td>1</td><td>Video</td><td>multi-teacher distillation 기반 비디오 이해 모델이고 엔지니어링 성격이 강함</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2609.09626'>Hyperbolic Geometry for Open-World Object Detection in Remote Sensing Imagery</a></td><td>27</td><td>1</td><td>CV</td><td>원격탐사 open-world detection에 hyperbolic geometry를 적용한 도메인 특화 연구임</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2609.09876'>From Pixels to Hierarchical Sequences: Quadtree Mask Encoding for Vision-Language Binary Change Detection</a></td><td>27</td><td>1</td><td>Multimodal</td><td>quadtree 토큰화로 VLM 변화탐지 마스크를 생성했고 원격탐사 응용에 그침</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2609.10346'>Beyond One-Size-Fits-All: Sample-Adaptive Strategy Routing for Vision Token Pruning in MLLMs</a></td><td>27</td><td>1</td><td>Multimodal</td><td>MLLM 비전토큰 pruning 전략을 샘플별로 라우팅하는 효율화 기여임</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2609.09766'>CARRE: Counterfactual Action Retrieval and Reason Evaluation for Explainable Churn Prescription</a></td><td>27</td><td>1</td><td>NLP/Business Analytics</td><td>고객 이탈 방지를 위한 counterfactual 액션 검색과 LLM 설명 결합 프레임워크, 비즈니스 응용이라 로봇 연구와 무관함</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2609.09338'>Osprey: Target-agnostic Pre-training Makes Stronger Drafters in Speculative Decoding</a></td><td>27</td><td>0</td><td>NLP/Efficient Inference</td><td>target-agnostic 사전학습으로 재사용 가능한 speculative decoding drafter를 만드는 연구, LLM 추론 가속 주제로 로봇과 무관함</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2609.09363'>Do LLMs Make More Mistakes If They Do Not Believe the Input Data?</a></td><td>27</td><td>0</td><td>NLP</td><td>LLM이 입력 데이터를 얼마나 신뢰하는지에 따른 hallucination 경향을 다국어로 분석한 연구임</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2609.09691'>Looped GPT-BERT: Trading Parameters for Computation in Small Language Modeling</a></td><td>27</td><td>0</td><td>NLP/LM Architecture</td><td>물리적 레이어 수를 줄이고 순환 적용 횟수를 늘려 파라미터를 계산으로 대체하는 소형 LM 연구, BabyLM 세팅에 한정된 실험임</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2609.10372'>PACE: Perceived-Latency-Aware Cascading Service Routing and Filler Control for QoE-Efficient Retrieval-Augmented Dialogue Serving</a></td><td>26</td><td>3</td><td>Robotics</td><td>휴머노이드 로봇 대화서비스에 배포된 지연시간 최적화 라우팅이고 로봇 인지·제어 자체에 대한 기여는 아니며 서빙 시스템 최적화 성격임</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2609.09884'>Albedo Estimation via Latent Bridge Matching</a></td><td>26</td><td>1</td><td>CV</td><td>latent bridge matching 기반 albedo 추정으로 intrinsic decomposition을 개선했고 robotics와 무관함</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2609.09973'>Putting Captions to the Test: Evaluating Video Caption Quality through Multiple-Choice Question Answering</a></td><td>26</td><td>1</td><td>Multimodal</td><td>reference-free 비디오 캡션 품질평가를 MCQ로 재정의한 평가지표 기여임</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2609.10356'>Spot-the-shift: Evaluating Grounded Image Difference Captioning of Long-term Changes</a></td><td>26</td><td>1</td><td>Multimodal</td><td>장기 변화에 대한 grounded image difference captioning 벤치마크이고 도시 인프라 모니터링 응용임</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2609.10376'>Shape-guided Gaussian Splatting for Sparse-View X-ray 3D Reconstruction</a></td><td>26</td><td>1</td><td>3D Vision</td><td>해부학적 형태 사전으로 sparse-view X-ray 3DGS 재구성을 개선한 의료영상 응용임</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2609.09901'>Deep and shallow biases in language models</a></td><td>26</td><td>0</td><td>NLP/Interpretability</td><td>reframing에도 살아남는 deep bias와 프롬프트에 의존하는 shallow bias를 구분하는 지표를 제안, SFT·디바이어싱에 대한 저항성 차이를 분석함</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2609.10142'>Active Adaptation, Not Static Defense: Temporal Dynamics of Preventative Steering in Adversarial Fine-Tuning</a></td><td>26</td><td>0</td><td>NLP/Safety</td><td>적대적 파인튜닝 방어에서 persona steering이 정적 방어가 아니라 능동적 적응임을 분석하고 강도를 점진적으로 높이는 스케줄을 제안함</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2609.09692'>CT-SAFR: Safe and Interpretable Chain-of-Thought Reasoning for Autonomous Robots: A Multi-Layered Verification Framework for Trustworthy AI-Driven Robotic Decision Making</a></td><td>25</td><td>5</td><td>Manipulation</td><td>로봇 chain-of-thought 추론의 안전성·충실성을 다층 검증하는 프레임워크임. 창고 로봇 단일 사례연구로 검증 범위가 좁고 제시된 수치의 재현성 근거가 약함.</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2609.10400'>A traffic management system for large and heterogeneous vehicles in narrow industrial environments</a></td><td>25</td><td>4</td><td>Multi-robot Planning</td><td>NURBS 로드맵과 L-MAPF 기반 산업용 AGV 교통관리 시스템으로 학습 요소 없는 응용 알고리즘 논문임</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2609.09187'>AgenticGen: Reward-Guided Agentic Video Generation for Advertising</a></td><td>25</td><td>1</td><td>Video</td><td>광고 영상 생성에 DPO·GRPO를 적용한 산업 응용 수준이고 robotics와 무관함</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2609.10363'>SceneHI: High-Resolution 3D-Consistent Scene Texturing with Controllable Illumination</a></td><td>25</td><td>1</td><td>3D Vision</td><td>2D diffusion prior를 3D 장면 텍스처링에 고해상도로 전이한 그래픽스 파이프라인임</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2609.09783'>BRACE: Anchored Bellman-Residual Correction for Stale Critics in Asynchronous RL</a></td><td>25</td><td>1</td><td>RL</td><td>비동기 RL에서 stale critic 편향을 anchored Bellman-residual로 보정함. agentic LLM RL 인프라 기여이나 로보틱스와 직접 관련은 낮음.</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2609.10296'>The Semantic Bottleneck: Leveraging Semantic Representations for Non-Invasive Speech Decoding</a></td><td>25</td><td>1</td><td>NLP</td><td>MEG 신호를 semantic embedding으로 우회 디코딩하는 방법임. 아이디어는 흥미로우나 non-robot 뇌신호 해독 문제임</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2609.09578'>CityPlanner: A Sandbox Agent for Executable Urban Planning</a></td><td>25</td><td>1</td><td>AI</td><td>도시계획 문제를 sandbox agent와 atomic-task RL로 푸는 연구임. task decomposition RL 아이디어는 있으나 도메인이 robotics 밖임</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2609.09678'>Safe to Stop? Risk-Constrained Stopping for Sequential Clinical Diagnosis Agents</a></td><td>25</td><td>1</td><td>AI</td><td>임상 진단 agent가 언제 멈춰야 하는지 통계적으로 보장하는 stopping 기법임. 불확실성 하 의사결정 문제로 방법론은 흥미로우나 의료 도메인 한정임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2609.10001'>From Few-Shot Segmentation to Clinician-in-the-Loop Medical Image Analysis</a></td><td>25</td><td>0</td><td>CV</td><td>few-shot 의료영상분할을 순차적 임상의-모델 의사결정으로 재구성한 관점논문이고 실험적 실증이 없음</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2609.10287'>Training Trajectories Determine Circuit Removability in Annealable Soft-Prior Transformers</a></td><td>25</td><td>0</td><td>LG</td><td>soft positional prior의 학습 궤적이 회로 제거 가능성을 좌우함을 소형 Transformer로 분석함. mechanistic interpretability 연구이나 toy task에 국한됨.</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2609.10311'>One Loop, Two Gains: Can Active Learning win the Lottery for Free?</a></td><td>25</td><td>0</td><td>LG</td><td>active learning의 반복 재학습 루프에 magnitude pruning을 끼워 넣어 거의 추가 비용 없이 sparse winning ticket을 얻음. 두 기존 패러다임의 결합이고 로보틱스와 무관함.</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2609.09554'>BuzzASR: A Swarm of 100+ Monolingual Speech Recognition Models</a></td><td>25</td><td>0</td><td>NLP/Speech</td><td>102개 언어에 대해 Whisper를 모노링구얼로 파인튜닝한 ASR 모델 모음으로 스케일업 위주 기여임</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2609.09835'>HyperTrace: Hypothesis-Based Preference Tracing for Online LLM Personalization</a></td><td>25</td><td>0</td><td>NLP/Personalization</td><td>SMC 방식으로 장단기 선호 가설을 갱신하는 학습 없는 LLM 개인화 프레임워크임</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2609.10060'>Reference-Based Bias Detection in LLMs via Relative Representations of Hidden States</a></td><td>25</td><td>0</td><td>LG</td><td>hidden state의 상대적 표상으로 파인튜닝 전후 편향 변화를 감사하는 방법임. 해석가능성 방법론이나 robotics 연관 없음</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2609.10484'>Coastal Environment Generation with HoloOcean</a></td><td>24</td><td>3</td><td>Simulation Tool</td><td>항공 이미지로부터 해안 시뮬레이션 환경을 자동 생성하는 UE5 파이프라인으로 로봇 학습 자체 기여는 아님</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2609.09396'>VANTAGE-Bench: Evaluating the Infrastructure AI Gap in Vision-Language Models</a></td><td>24</td><td>1</td><td>Multimodal</td><td>고정 카메라 인프라 모니터링 벤치마크이고 embodied action과 무관함</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2609.09736'>IAE-VTG: Interaction-Aligned Action-Entity Video Temporal Grounding</a></td><td>24</td><td>1</td><td>Video</td><td>action-entity 상호작용 정합 기반 video temporal grounding이고 벤치마크 개선 수준임</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2609.10156'>ScopeMamba-YOLO: Widening the Perceptual Scope Inward and Outward for Small Object Detection in Remote Sensing Imagery</a></td><td>24</td><td>1</td><td>CV</td><td>UAV 원격탐사 소형객체 탐지에 off-path selective scanning을 적용한 탐지 벤치마크 개선임</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2609.10317'>Decoupled Self-Forcing Distillation for Streaming Talking Head Generation</a></td><td>24</td><td>1</td><td>Video</td><td>스트리밍 토킹헤드 생성을 위한 모션-렌더러 분리 distillation이고 아바타 생성 응용임</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2609.10498'>Field Converter: Geometry-Initialized Temporal Residual Refinement for World-Grounded Player Pose Estimation from Soccer Broadcasts</a></td><td>24</td><td>1</td><td>CV</td><td>축구 중계 영상에서 world-grounded 선수 3D pose를 추정한 스포츠 응용 연구임</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2609.09166'>X-CoSD: Communication-Efficient Cross-Vocabulary Collaborative Speculative Decoding</a></td><td>24</td><td>1</td><td>NLP/Efficient Inference</td><td>이종 vocabulary 간 협업 speculative decoding으로 통신량을 줄이는 방법, LLM 추론 효율화 연구로 로봇 관련성이 낮음</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2609.09832'>SkNeXt enables topology-guided neuronal reconstruction from petabyte-scale microscopy data</a></td><td>24</td><td>0</td><td>CV</td><td>petabyte급 뉴런 재구성을 위한 topology-first 프레임워크이고 신경과학 응용이며 robotics와 무관함</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2609.10002'>What Makes Adversarial Examples Transfer Across Deepfake Detectors?</a></td><td>24</td><td>0</td><td>CV</td><td>deepfake 탐지기 간 적대적 전이가능성을 분석한 연구이고 robotics와 무관함</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2609.10456'>Advanced Brain Tissue Imaging with Data-Consistent Diffusion Priors in Laminographic X-Ray Nanoimaging</a></td><td>24</td><td>0</td><td>CV</td><td>laminography 뇌조직 영상에서 diffusion prior 기반 missing-cone 복원이고 뉴로이미징 응용임</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2609.09367'>Explaining f-Divergence-Based Regularization via Local Curvature and Sharpness-Aware Minimization</a></td><td>24</td><td>0</td><td>LG</td><td>divergence 정규화와 SAM의 국소곡률 관계를 다룬 이론분석이고 robotics와 무관함</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2609.09356'>Auditable Emergency Triage for Maternal and Newborn Care in India</a></td><td>24</td><td>0</td><td>NLP/Applied</td><td>산모·신생아 응급 트리아지를 위해 LLM 추출과 규칙엔진을 결합한 배포 시스템 보고서로 연구적 신규성은 제한적임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2609.09552'>TEFM: Token-Efficient Faithful Modeling for Structured Data</a></td><td>24</td><td>0</td><td>NLP/Efficient Modeling</td><td>구조화 데이터를 Behavioral Code로 압축해 토큰 효율과 충실도를 동시에 얻는 프레임워크, 임상·보안 도메인 응용임</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2609.09684'>Which Medical Questions Deserve Rationales? Perturbation-Sensitive Selection for Robust QA</a></td><td>24</td><td>0</td><td>NLP/Medical QA</td><td>고정된 토큰 예산 하에서 rationale을 부여할 질문을 선별하는 방법, 효과는 일부 데이터셋에서만 통계적으로 유의함</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2609.09719'>StreamAlign: Streaming Text-Aligned Speech Tokenization</a></td><td>24</td><td>0</td><td>NLP/Speech</td><td>문자 단위 RNN-T 정렬과 단어 단위 ASR 가이드를 결합해 스트리밍 text-aligned 음성 토큰화를 구현한 연구임</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2609.09772'>SymbolicLight V2: Hybrid Neuromorphic Architecture and Sparse Execution for Low-Energy Language Inference</a></td><td>24</td><td>0</td><td>NLP/Efficient Hardware</td><td>이벤트 희소성 기반 뉴로모픽 아키텍처를 FPGA·ARM에서 구현해 토큰당 에너지를 줄였으나 동일 성능 비교는 아니라고 스스로 명시함</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2609.09953'>Improving Cross-Lingual Token Representations by Adding a Pinch of SALT</a></td><td>24</td><td>0</td><td>NLP/Representation</td><td>문장 인코더에 span-level supervision을 주입해 토큰 표현을 개선하는 경량 post-training 방법임</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2609.09890'>StreetDiff: Multi-view Street Scenes Generation via Cross-view Consistent Multi-view Stable Diffusion with Structure Prompts</a></td><td>23</td><td>1</td><td>3D Vision</td><td>파노라마 정렬 기반 다중뷰 거리풍경 생성이고 데이터셋·생성품질 개선 중심임</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2609.09466'>Exact-Form Regret for Gradient Descent, Mirror Descent and Follow-the-Regularized-Leader</a></td><td>23</td><td>0</td><td>LG</td><td>온라인학습 알고리즘별 편차류를 기하학적으로 특성화한 이론연구이고 robotics와 무관함</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2609.09264'>StochBench: A Domain-Specific Benchmark for Stochastic Processes in Lean</a></td><td>23</td><td>0</td><td>NLP/Formal Math</td><td>Lean 4 기반 대학원 수준 확률과정 정리증명 벤치마크로 robotics와 무관함</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2609.09503'>Agentic AI-enabled Semantic Commissioning of a Cognitive Digital Twin for Reconfigurable Manufacturing</a></td><td>22</td><td>3</td><td>Manipulation</td><td>LangGraph 멀티에이전트로 RAG와 MCP를 결합해 디지털트윈 커미셔닝을 자동화한 산업 응용 사례임. 배포 시간은 단축했으나 연구적 novelty보다 시스템 통합 성격이 강함.</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2609.10263'>What Should an Agent Forget? Separating What Is Stored from What Is Used</a></td><td>22</td><td>2</td><td>AI</td><td>agent가 저장하는 것과 답변에 쓰는 것을 분리하는 memory framework임. robot memory 문제와 개념적으로 닿지만 대화형 LLM agent 대상임</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2609.10139'>TransGaze-Object: Transformer Based Driver Gaze Object Prediction Framework in Real Driving</a></td><td>22</td><td>1</td><td>CV</td><td>운전자 시선-객체 예측 transformer이고 자동차 응용이며 robotics manipulation과는 무관함</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2609.09257'>Accountable and uncertainty-aware evaluation of sensor-based AI under distribution shift: devices, subjects, and nearly three years underground</a></td><td>22</td><td>1</td><td>LG</td><td>지하 광산 센서 AI의 장기간 분포변화 하 신뢰성 평가 프로토콜이고 배포후 평가방법론에 대한 기여임</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2609.09476'>From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls</a></td><td>22</td><td>1</td><td>NLP</td><td>차량 에이전트 함수호출에서 schema-in-prompt 대 functional token을 비교한 온디바이스 SLM 응용임</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2609.10413'>Fortunate Recall: Ontology-Driven Memory Lifecycle Management for Persistent Coherence in LLMs</a></td><td>22</td><td>1</td><td>AI</td><td>개인 사실을 행동 유형별로 분류해 memory 수명주기를 관리하는 정책 계층임. LLM 개인화 memory 벤치마크이고 robot memory와는 거리가 있음</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2609.09705'>Cross-Species Animal Re-Identification with Semantic Consistency Learning</a></td><td>22</td><td>0</td><td>CV</td><td>종간 동물 재식별 표현학습 연구이고 robotics와 무관함</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2609.09863'>Pretraining and Distillation Matter More Than Architecture Family for Label-Free Single-Cell Classification</a></td><td>22</td><td>0</td><td>CV</td><td>label-free 단일세포 분류에서 pretraining이 architecture보다 중요함을 보인 통제 벤치마크이고 robotics와 무관함</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2609.10261'>When Fusion Fails: Corruption-Aware Rebalanced Fusion for Multi-Modal Medical Image Segmentation</a></td><td>22</td><td>0</td><td>CV</td><td>손상 인지 재균형 융합 기반 다중모달 의료영상분할이고 robotics와 무관함</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2609.10518'>BrainTaskonomy: Learning How to Pretrain and What to Transfer in fMRI Foundation Models</a></td><td>22</td><td>0</td><td>LG</td><td>fMRI foundation model의 pretraining curriculum과 transfer taskonomy를 구성한 신경영상 도메인 연구임</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2609.09349'>SWORD: Wikidata-based Distortions Reveal Hidden Cross-Lingual Inconsistencies in LLM Factual Error Rejection</a></td><td>22</td><td>0</td><td>NLP/Multilingual Eval</td><td>Wikidata 기반 distortion으로 다국어 LLM의 사실 오류 거부 일관성을 평가하는 벤치마크 논문임</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2609.09425'>Edu-QuRating: Multi-Dimensional Educational Data Curation with Distilled Pairwise Judgements</a></td><td>22</td><td>0</td><td>NLP/Data Curation</td><td>교육 데이터를 다차원 rubric으로 채점하는 curation 파이프라인, pretraining과 GRPO에 적용했으나 데이터 필터링 범주의 기여임</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2609.09561'>Towards Automatic Evolution Tree Generation from Citation Graphs</a></td><td>22</td><td>0</td><td>NLP/Scientometrics</td><td>인용 그래프에서 방법론 진화 트리를 자동 생성하는 연구로 로봇 연구와는 무관함</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2609.09575'>Beyond Top Words: MonoTM for Topic Modeling with Interpretable Monosemantic Features</a></td><td>22</td><td>0</td><td>NLP/Interpretability</td><td>sparse autoencoder로 토픽 모델의 해석가능성과 추론 품질을 분리하는 프레임워크임</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2609.09672'>SEA-SpeechBench: A Large-Scale Multitask Benchmark for Speech Understanding Across Southeast Asia</a></td><td>22</td><td>0</td><td>NLP/Speech</td><td>동남아 11개 언어 음성이해 멀티태스크 벤치마크로 데이터셋 구축 기여 위주임</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2609.10122'>ProbPlug: A Plugin Uncertainty Network for Reliable Confidence in LLM Binary Classification</a></td><td>22</td><td>0</td><td>NLP/Calibration</td><td>고정된 LLM의 내부 토큰 특징으로 이진분류 신뢰도를 추정하는 플러그인 네트워크임</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2609.10434'>Do speech foundation models really learn words?</a></td><td>22</td><td>0</td><td>NLP</td><td>speech foundation model이 단어를 형태와 독립적으로 표상하는지 분석한 연구임. representation 분석은 흥미롭지만 speech 도메인 한정임</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2609.09395'>The Menu Is an Execution Prior: State-Path Tool Menus for Online Agents</a></td><td>22</td><td>0</td><td>AI</td><td>agent에게 제시할 tool 메뉴를 실행 상태 경로 기반으로 구성하는 방법임. LLM agent tool-use 문제로 robotics와 직접 연관은 낮음</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2609.10333'>Learning to Adapt and Calibrate: Score Distribution Alignment for Few-Shot Uncertainty Prediction in Medical VLMs</a></td><td>21</td><td>0</td><td>CV</td><td>few-shot 의료 VLM conformal prediction 정합 연구이고 robotics와 무관함</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2609.10433'>Multi-Agent Reinforcement Learning for Autonomous UAV Exploration in Wildfire Response</a></td><td>20</td><td>5</td><td>RL/Navigation</td><td>산불 대응 UAV 탐색에 DRL을 적용한 초기 단계 연구로 정량적 근거가 약하고 방법론적 기여가 크지 않음</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2609.10082'>Automatic Reproducible Camera Intrinsic Calibration</a></td><td>20</td><td>3</td><td>CV/Tool</td><td>카메라 내부 파라미터 캘리브레이션 자동화 도구 논문으로 robot learning 기여는 아님</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2609.10169'>Multi-Robot Scanner for Automated Full-Body Dermoscopic Imaging</a></td><td>20</td><td>3</td><td>Applied Robotics</td><td>UR10 4대로 전신 피부를 스캔하는 의료응용 시스템 논문으로 학습 기반 기여가 없음</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2609.09885'>Decision Transformer for UAV-Mounted RIS-Assisted Dynamic D2D Communications</a></td><td>20</td><td>2</td><td>RL</td><td>UAV-RIS 통신 최적화에 Decision Transformer를 적용한 연구임. cs.RO 태그이나 manipulation·embodied 문제가 아닌 통신 공학 문제임</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2609.09513'>AnimalLift: Reconstructing Animatable 3D Animals from a Single Image by Learning Canonical Shape, Texture, and Fur Maps</a></td><td>20</td><td>1</td><td>3D Vision</td><td>단일 이미지 기반 애니메이션 가능한 3D 동물 자산 복원이고 그래픽스 응용 중심임</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2609.09826'>Freezing of Gait Prediction Under Spatial Occlusion: An IMU-Supervised Cross-Modal Distillation Approach</a></td><td>20</td><td>1</td><td>CV</td><td>파킨슨 보행동결 예측을 위한 IMU-비디오 cross-modal distillation이고 의료 도메인 특화임</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2609.10355'>Why Is Video Still So Expensive? A Survey of Inference-Efficiency Mechanisms in Video and Audiovisual LLMs</a></td><td>20</td><td>1</td><td>Video</td><td>비디오 LLM 추론효율화 기법 서베이이고 원저작 기여가 없음</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2609.10017'>Structure-Aware Unsupervised Anomaly Detection for Spacecraft Telemetry with Adaptive EVT Thresholding</a></td><td>20</td><td>1</td><td>LG</td><td>위성 원격측정 이상 탐지를 라벨 없이 EVT 임계값으로 수행하는 프레임워크임. failure detection과 개념적으로 맞닿으나 우주 원격측정 도메인이라 로봇 매니퓰레이션과는 거리가 있음.</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2609.09664'>PRAGMA: Evaluating Personalized Guidance with Memory Alignment in Lifelong Conversations</a></td><td>20</td><td>1</td><td>AI</td><td>장기 대화에서 개인화된 조언 능력을 평가하는 벤치마크임. 대화형 memory 문제이고 robot memory와는 거리가 있음</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2609.10144'>Kernel-Managed Shared Memory for System-Wide Personalization</a></td><td>20</td><td>1</td><td>AI</td><td>multi-agent 시스템에서 memory 접근·프라이버시를 kernel이 관리하는 구조를 제안함. shared memory 아이디어는 robot memory와 약하게 연관되나 개인화 비서 응용임</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2609.09462'>Low-Rank Prompt Learning for Vision-Language Models with Fixed-Token Bases</a></td><td>20</td><td>0</td><td>CV</td><td>CLIP prompt learning 파라미터 효율화 연구이고 경량화 성격이며 robotics와 무관함</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2609.10278'>FreqFLD: Towards All-in-One Facial Landmark Detection via Frequency Modulation</a></td><td>20</td><td>0</td><td>CV</td><td>주파수 변조 기반 범용 얼굴 랜드마크 검출이고 robotics와 무관함</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2609.10495'>Cross-Model Agreement as a Deployment-Time Reliability Signal for Automatic Polyp Segmentation</a></td><td>20</td><td>0</td><td>CV</td><td>모델간 합치도를 이용한 용종분할 신뢰도 추정이고 robotics와 무관함</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2609.09299'>Literati: Towards Anytime Optimal Shape Generalized Trees via AO*</a></td><td>20</td><td>0</td><td>LG</td><td>AO* 기반 최적 shape generalized tree 탐색이고 표형데이터 해석가능성 연구이며 robotics와 무관함</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2609.09388'>XAI-Refine: An Automated Explanation-Knowledge Loop for Brain-Age Prediction</a></td><td>20</td><td>0</td><td>LG</td><td>뇌연령예측 설명-지식 루프를 자동화한 신경영상 도메인 연구임</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2609.09547'>A Statistical Approach to Estimating Sample Size of Machine Learning Models</a></td><td>20</td><td>0</td><td>LG</td><td>ML 모델 표본 크기를 국소 선형화로 추정하는 통계적 프레임워크임. 이론적 정리 수준이고 로보틱스와 무관함.</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2609.09659'>Cascading Gradient Inversion via LT-Code Inspired Peeling in Federated Learning</a></td><td>20</td><td>0</td><td>LG</td><td>erasure-correcting code 이론으로 federated learning의 gradient inversion 공격을 강화함. 프라이버시 보안 주제로 로보틱스와 무관함.</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2609.09796'>A practical DIRECT-type algorithm for medium-scale black-box global optimization</a></td><td>20</td><td>0</td><td>LG</td><td>DIRECT류 black-box 최적화에 동적 분할과 hill-climbing을 결합한 알고리즘 개선임. 벤치마크 수치 개선 위주로 novelty가 제한적임.</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2609.09809'>Online Inverse Integer Linear Optimization via Small-Gradient Skipping: Constant Regret and Finite Mistakes</a></td><td>20</td><td>0</td><td>LG</td><td>online inverse linear optimization에서 update skip으로 regret과 mistake를 동시에 줄이는 이론 논문임. 순수 이론이고 로보틱스와 무관함.</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2609.09907'>Meta-LinEXP3: Online-within-Online Learning for Adversarial Linear Contextual Bandits</a></td><td>20</td><td>0</td><td>LG</td><td>adversarial linear contextual bandit에 meta-learning으로 task 간 prior를 전이하는 이론 논문임. 순수 bandit 이론이고 로보틱스와 무관함.</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2609.09912'>Development and Validation of a Physics-Guided Machine Learning Extrapolation Framework Using a Classical Transient Diffusion Benchmark</a></td><td>20</td><td>0</td><td>LG</td><td>물리 기반 좌표변환과 BiLSTM/PINN을 결합해 확산 벤치마크 외삽을 개선함. 공학 벤치마크이고 로보틱스와 무관함.</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2609.10196'>An Exponential Deterministic--Randomized Gap in ERM-Oracle Complexity for Thresholds on an Unknown Order</a></td><td>20</td><td>0</td><td>LG</td><td>미지 순서 threshold의 online inverse learning에서 결정론/무작위 알고리즘 간 지수적 격차를 증명함. 순수 학습이론이고 로보틱스와 무관함.</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2609.10490'>Learning with Covariance Matrices: Principal Component Analysis Meets Learning with Graphs</a></td><td>20</td><td>0</td><td>LG</td><td>공분산 행렬 기반 GNN(coVariance neural network)과 PCA의 이론적 등가성을 정리한 튜토리얼 논문임. 신규 실험 없는 서베이형이고 로보틱스와 무관함.</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2609.09852'>$S^3$-Bench: Evaluating Speech Interaction Models as Scientific Voice Assistants</a></td><td>20</td><td>0</td><td>NLP/Speech</td><td>과학 분야 음성 어시스턴트 평가 벤치마크로 10개 학문 분야를 다루는 데이터셋 기여 위주임</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2609.09887'>When Does Defendant Statement Matter? A Study of Bias and Persuasion in LLM-Simulated Jurors</a></td><td>20</td><td>0</td><td>NLP/Social Science</td><td>LLM 배심원 시뮬레이션에서 피고인 진술의 설득 효과와 배경 편향을 분석한 사회과학적 연구임</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2609.09203'>OpenDiscoveryTrace: Process Traces for Evaluating AI Scientist Workflows</a></td><td>20</td><td>0</td><td>AI</td><td>AI scientist agent의 추론 과정을 기록한 trace 데이터셋임. 프로세스 레벨 평가 자원 제공 수준의 기여임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2609.09370'>Constraint-Aware Discrete Black-Box Optimization Using Tensor Decomposition</a></td><td>19</td><td>0</td><td>LG</td><td>제약인지 이산 블랙박스 최적화에 텐서분해 대리모델을 적용한 연구임</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2609.09677'>X2-NativeCursor: Native-Token Text Progress Tracking for Incremental-Text Streaming Codec TTS</a></td><td>19</td><td>0</td><td>NLP/Speech</td><td>스트리밍 TTS에서 native token 기반으로 텍스트 진행상황을 추적하는 경량 옵저버 모듈임</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2609.09368'>The Living Library: Transforming Archival Collections into Conversational Knowledge Systems -- Lessons from the Theodore Roosevelt Presidential Library</a></td><td>18</td><td>1</td><td>Multimodal</td><td>박물관 전시용 대화형 디지털 휴먼 시스템 구축 리포트이고 연구적 novelty는 낮음</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2609.10387'>Enhanced Deformable Convolution with Center-invariant Offset and Edge-aware Mask</a></td><td>18</td><td>1</td><td>CV</td><td>deformable convolution 개선으로 semantic segmentation을 향상시킨 점진적 모듈 추가 성격임</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2609.09971'>Deep Neural Networks for Learning Intent from sEMG Signals to Support Hardware Devices for Post-Stroke Neurorehabilitation</a></td><td>18</td><td>1</td><td>LG</td><td>뇌졸중 재활을 위해 sEMG로 손가락별 동작 의도를 디코딩하는 경량 모델임. 보조기기 제어와 맞닿아 있으나 의료 재활 응용이고 매니퓰레이션과는 거리가 있음.</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2609.10321'>On-Policy Distillation for Vision-Language Model Adaptation, an Effective Paradigm on Low-Quality Multimodal Data</a></td><td>18</td><td>1</td><td>Multimodal</td><td>VLM distillation target을 policy로 학습하는 방법임. 기존 distillation 파이프라인 위 incremental 개선에 가까움</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2609.09413'>Decision-Focused Active Learning for Scale-Aware Critical-Materials Recovery</a></td><td>18</td><td>1</td><td>AI</td><td>희토류 회수 공정 스케일업을 위한 decision-focused active learning 연구임. cs.RO 태그이나 재료·화학 공정 문제로 robot learning과 거리가 있음</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2609.10177'>Beyond Surface Imitation: Contrastive Modeling for Reasoning Path Alignment in Multimodal In-Context Learning</a></td><td>18</td><td>1</td><td>Multimodal</td><td>잘못된 응답과 개선된 응답을 대조시켜 multimodal in-context learning의 reasoning path를 정렬하는 방법임. VQA 개선 수준의 incremental 기여임</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2609.09827'>Layerwise Tunable Lifting Scheme for the Convolutional Neural Network</a></td><td>18</td><td>0</td><td>CV</td><td>CNN용 tunable wavelet lifting scheme이고 분류·이상탐지 성능 개선이며 robotics와 무관함</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2609.09924'>Multimodal Emotion Recognition in Conversations via Class-Wise Adaptive Modality Fusion and Affective Geometry</a></td><td>18</td><td>0</td><td>Multimodal</td><td>대화 감정인식에서 modality fusion을 개선한 연구이고 robotics와 무관함</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2609.09162'>Physics-informed neural networks by Gradient-Guided Gaussian Adaptive Sampling (3GAS-PINNs)</a></td><td>18</td><td>0</td><td>LG</td><td>gradient 기반 gaussian adaptive sampling으로 PINN 수렴을 개선한 PDE 솔버 응용임</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2609.09434'>Tensor-Train Weak SINDy: Identifying High-Dimensional Nonlinear Dynamics</a></td><td>18</td><td>0</td><td>LG</td><td>텐서트레인 기반 고차원 비선형동역학 식별이고 robotics와 무관한 수치기법임</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2609.09891'>ProMeta: Few-shot PROTAC-targeted degradation prediction across E3 ligases</a></td><td>18</td><td>0</td><td>LG</td><td>few-shot meta-learning으로 E3 ligase 간 PROTAC 분해 활성을 예측함. 신약 개발 응용이고 로보틱스와 무관함.</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2609.10016'>MetroLLM-Bench: Evaluating Language Models as Transit Kiosk Runtimes</a></td><td>18</td><td>0</td><td>NLP</td><td>지하철 키오스크 정책 레이어로서 LLM을 평가하는 벤치마크임. LLM agent 평가이고 로보틱스와 무관함.</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2609.10529'>A positive resolution of the gap-entropy conjecture</a></td><td>18</td><td>0</td><td>LG</td><td>best-arm identification에서 gap-entropy 추측을 증명한 이론 논문임. 순수 bandit 이론이고 로보틱스와 무관함.</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2609.09716'>Scaling E-Commerce Attribute Extraction with Parallel Decoding</a></td><td>18</td><td>0</td><td>NLP/Applied</td><td>구매 판별에 중요한 속성 스키마를 먼저 발견한 뒤 소형 LLM으로 병렬 추출하는 산업 응용 파이프라인임</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2609.09889'>Leveraging Fine-grained Error Correction in Korean Speech Recognition for Consultation Services</a></td><td>18</td><td>0</td><td>NLP/Speech</td><td>한국어 콜센터 ASR 오류를 텍스트만으로 교정하는 탐지-교정 파이프라인과 벤치마크 데이터셋 논문임</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2609.09999'>SalamandraTA at WMT 2026 Terminology Shared Task: Hard Examples Are Better Teachers</a></td><td>18</td><td>0</td><td>NLP/Machine Translation</td><td>용어집과 모순되는 예시만 골라 학습시켜 terminology 정확도를 78.7%에서 89.9%로 높인 WMT 공유과제 제출 논문임</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2609.10049'>MedDeID enables locally governed clinical-text de-identification from real or synthetic training data</a></td><td>18</td><td>0</td><td>NLP/Applied</td><td>실제·합성 데이터로 학습하는 임상 텍스트 비식별화 온프레미스 프레임워크로 응용 시스템 논문임</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2609.10113'>Data-Centric Post-Training for Financial Reasoning: Mining, Distillation, and Verifiable Learning</a></td><td>18</td><td>0</td><td>NLP/Applied</td><td>금융 도메인 데이터 마이닝과 self-distillation, 모델 병합으로 SFT의 성능 저하를 막는 데이터 중심 파이프라인임</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2609.10266'>KVShareArena: KV-Cache Reuse Across Contexts and Model Checkpoints</a></td><td>18</td><td>0</td><td>LG</td><td>KV-cache 재사용 벤치마크임. 시스템 최적화 문제로 방법론적 새로움보다 측정 도구 제공에 가까움</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2609.10305'>RiLM: Parameter-Efficient Language Modeling via Geodesic Decoding</a></td><td>18</td><td>0</td><td>LG</td><td>출력층을 geodesic distance로 대체하는 경량 언어모델임. 초소형 모델·제한된 벤치마크로 scope가 좁음</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2609.10539'>IdeaAMBIG: Benchmarking Implementation-Critical Gaps in Research-Idea Specifications</a></td><td>18</td><td>0</td><td>NLP</td><td>연구 아이디어 명세의 구현 가능성을 측정하는 벤치마크임. meta-science 벤치마크이고 robotics와 무관함</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2609.09458'>ContractEval: Query-Conditioned Execution Matching for Procedural Instruction Conformance</a></td><td>18</td><td>0</td><td>AI</td><td>절차적 지시 준수 여부를 진단하는 프레임워크임. 평가 도구 제안이고 robotics와 무관함</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2609.09565'>Multi-Agent Agentic Graph Learning via Structural Signatures</a></td><td>18</td><td>0</td><td>AI</td><td>그래프를 커뮤니티로 나눠 agent별로 담당시키는 multi-agent graph reasoning 방법임. 그래프 QA 벤치마크 개선 수준의 기여임</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2609.09646'>RobustSGPO: Search-Space Control for Agent Harness Evolution</a></td><td>18</td><td>0</td><td>AI</td><td>agent harness를 prompt-gradient로 진화시키는 search-space 제어 기법임. agent 엔지니어링 최적화 수준의 기여임</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2609.09707'>Which Tokens Should SFT Actually Learn? A Token-Trimming Perspective on Mathematical Reasoning</a></td><td>18</td><td>0</td><td>NLP</td><td>수학 reasoning SFT에서 토큰별 loss를 logit gap 기준으로 조정하는 기법임. 학습 트릭 수준의 incremental 기여임</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2609.09815'>UnitBoost: Managing Compound LLM Systems with a Merge Operator, Not a Model</a></td><td>18</td><td>0</td><td>AI</td><td>compound LLM 시스템의 manager를 생성형 대신 결정적 merge operator로 대체하는 방법임. multi-agent 조율 엔지니어링 수준의 기여임</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2609.09928'>Structural Process Supervision for Latent Chain-of-Thought Reasoning</a></td><td>18</td><td>0</td><td>NLP</td><td>latent chain-of-thought에 prototype 기반 process supervision을 추가한 방법임. reasoning 효율화 기법으로 robotics와 무관함</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2609.10335'>From Symbolic Perception to Logical Deduction: A Framework for Guiding Language Models in Geometric Reasoning</a></td><td>18</td><td>0</td><td>NLP</td><td>기하 도형을 symbolic parser로 변환 후 solver로 푸는 LLM 프레임워크임. 특정 시험 문제 벤치마크 한정의 기여임</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2609.10441'>ConvMem: Convolutional Memory for Long-Context Reasoning</a></td><td>18</td><td>0</td><td>NLP</td><td>긴 문맥을 계층적 convolution처럼 요약해 reasoning path를 단축하는 training-free 방법임. long-context QA 벤치마크 개선 수준의 기여임</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2609.09670'>Recovering Biomechanical Signals from Missing Keypoints Using Temporal Interpolation in Monocular Gait Analysis</a></td><td>17</td><td>1</td><td>CV</td><td>단순 시간보간으로 결손 keypoint를 복원했고 방법론적 기여가 미미함</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2609.09241'>Distribution-Consistent Inference for Dynamic Sparse Mixture-of-Experts</a></td><td>17</td><td>0</td><td>LG</td><td>dynamic top-k MoE 라우팅의 분포 불일치를 보정하는 추론시 정렬이고 효율화 기여임</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2609.09569'>Reproducing Omitted Temporal Expressions in Japanese News for Retrieval-Augmented Applications</a></td><td>17</td><td>0</td><td>NLP/Applied</td><td>일본어 뉴스의 생략된 시간 표현을 발행일 기준으로 복원하는 규칙 기반 파이프라인, RAG 검색 개선에 초점을 둔 응용 연구임</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2609.10018'>Elastoformer: Enabling Dynamic Adaptivity via Elastic Model Transformation</a></td><td>16</td><td>1</td><td>CV</td><td>엣지 디바이스용 동적 신축 신경망이고 효율성 중심 기여임</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2609.09188'>Lensless Gaze Is Not Private by Default: Auditing Identity Leakage Across Disclosure Surfaces</a></td><td>16</td><td>0</td><td>CV</td><td>렌즈리스 시선센서 프라이버시 감사 연구이고 robotics와 무관함</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2609.09711'>VFNet: Multi-View Spatio-Temporal Model for Void Fraction Estimation in Gas-Liquid Two-Phase Flow</a></td><td>16</td><td>0</td><td>CV</td><td>기액 이상유동 void fraction 추정 CNN이고 robotics와 무관함</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2609.09429'>Applying foundation model embeddings towards urban livability evaluation</a></td><td>16</td><td>0</td><td>LG</td><td>위성 foundation model 임베딩으로 도시 삶의질을 예측한 연구이고 robotics와 무관함</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2609.09433'>Efficient Leakage-Free Neural Architecture Search under Leave-One-Subject-Out Evaluation</a></td><td>16</td><td>0</td><td>LG</td><td>LOSO 평가하의 효율적 NAS이고 생체신호 분류 응용이며 robotics와 무관함</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2609.10192'>Who Argues What? Joint Argument-Entity Detection and Classification in Political Debates</a></td><td>16</td><td>0</td><td>NLP/Applied</td><td>정치 토론에서 논증과 개체명을 동시에 태깅하는 생성형 프레임워크로 응용 태스크 범주임</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2609.10187'>3rd Place Solution to Human Motion Challenges in Real-World and Clinical Settings (MoCha) @ECCV2026: Language-Aligned Motion Representations for Domain-Generalizable UPDRS-Gait Severity Estimation</a></td><td>15</td><td>1</td><td>CV</td><td>챌린지 3위 솔루션 리포트이고 임상 보행중증도 추정이며 novelty가 낮음</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2609.10200'>Robust Beam Prediction for V2X Networks with Multi-Modal Sensing</a></td><td>15</td><td>1</td><td>Multimodal</td><td>카메라·라이다·레이더·GPS를 융합해 V2X 빔을 예측하는 Transformer임. 통신 응용이고 로보틱스와는 거리가 있음.</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2609.09374'>An Autonomous GeoAI Agent for Arctic Eco-Navigation</a></td><td>15</td><td>1</td><td>Embodied AI</td><td>북극 항로 계획을 위한 multi-agent GeoAI 시스템임. 응용 라우팅 시스템이고 robot learning 방법론적 기여는 약함</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2609.09482'>Infra-Bench CLS: A Global, Open-Source Benchmark for Critical Infrastructure Classification with Earth Observation Foundation Models</a></td><td>15</td><td>0</td><td>CV</td><td>위성영상 인프라 분류 벤치마크이고 robotics와 무관함</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2609.09762'>MethaneFuse: Learning from Multi-Sensor Satellite Observations for Methane Plume Detection</a></td><td>15</td><td>0</td><td>CV</td><td>다중센서 위성관측 기반 메탄 플룸 탐지 연구이고 robotics와 무관함</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2609.10303'>SynThermFace: Amplifying Limited Paired Data for Visible-Thermal Face Recognition via Synthetic Data Generation</a></td><td>15</td><td>0</td><td>CV</td><td>가시광-열화상 얼굴인식을 위한 합성데이터 생성이고 robotics와 무관함</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2609.09240'>Scaling Post-Training Ternarisation to Qwen3-8B Capability Retention, Reproduction, Lossless Packing, and Packed Execution</a></td><td>15</td><td>0</td><td>LG</td><td>post-training ternarisation 스케일업 특성화 연구이고 경량화 중심 엔지니어링이며 robotics와 무관함</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2609.09254'>DiffLUT-Net: Differentiable Training of FPGA LUT Networks with Learnable Connectivity</a></td><td>15</td><td>0</td><td>LG</td><td>FPGA LUT 네트워크 미분가능 학습이고 하드웨어 효율화 성격이며 robotics와 무관함</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2609.09432'>SCCM : Stream Cruise Control Method for Automated Drift Detection and Adaptation</a></td><td>15</td><td>0</td><td>LG</td><td>스트림 드리프트 자동탐지·적응 프레임워크이고 온라인 회귀 응용이며 robotics와 무관함</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2609.09564'>Robust Industrial Cyber Physical Classification Using Neuromorphic Temporal Embeddings and Hybrid SNN XGBoost Under Machine Unlearning Attacks</a></td><td>15</td><td>0</td><td>LG</td><td>SNN과 XGBoost를 결합한 산업 IDS를 구현하고 unlearning attack 견고성을 평가함. 엔지니어링 응용이고 novelty가 낮음.</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2609.09567'>Positional task conditioning for scalable defect detection across product families in large product catalogs</a></td><td>15</td><td>0</td><td>NLP</td><td>제품 카탈로그 결함 탐지를 LLM sub-task 분해와 distillation으로 해결한 산업 응용 사례임. 로보틱스와 무관하고 engineering 중심임.</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2609.09662'>PELM: Power Efficient On-Device LLM Inference with Speculative Decoding and Dynamic Voltage Frequency Scaling</a></td><td>15</td><td>0</td><td>LG</td><td>on-device LLM 추론에 speculative decoding과 DVFS를 결합한 전력 최적화 기법임. efficiency 위주 엔지니어링이고 우선 주제가 아님.</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2609.09685'>ALIGN-HOLD: Experience Alignment for Real-Time Hold Control in Large-Scale Ride-Hailing Matching at DiDi</a></td><td>15</td><td>0</td><td>LG</td><td>DiDi 라이드헤일링 매칭에서 implicit preference로 hold 정책을 학습하는 산업 배포 사례임. A/B 검증은 강하나 로보틱스와 무관함.</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2609.09698'>Kernel-Complexity Edge Sanitization for Training-Free Defense against Structural Graph Attacks</a></td><td>15</td><td>0</td><td>LG</td><td>그래프 커널 복잡도 기반으로 GNN 구조적 적대 공격을 방어하는 training-free 기법임. 이론적 근거는 있으나 로보틱스와 무관함.</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2609.09728'>EEGBind: Detecting Source-Level Interictal Epileptiform Discharges via EEG-Centric Multimodal Binding</a></td><td>15</td><td>0</td><td>Multimodal</td><td>EEG 중심 멀티모달 결합으로 간질파를 소스 수준에서 분류함. 의료 응용이고 로보틱스와 무관함.</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2609.09786'>NEXUS-MI: Communication-Aware Federated Personalization for Gateway-Coordinated Motor-Imagery Brain-Computer Interfaces</a></td><td>15</td><td>0</td><td>LG</td><td>게이트웨이 조정 기반 federated 운동 심상 BCI 개인화 프레임워크임. 의료 BCI 응용으로 로보틱스와 무관함.</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2609.09860'>Exact Degeneracy Under Balanced k-Shot Sampling:Consequences for Small-Sample Discriminant Analysis on LLM Embeddings</a></td><td>15</td><td>0</td><td>LG</td><td>balanced k-shot 샘플링에서 discriminant analysis 추정량의 퇴화를 이론적으로 규명함. 소표본 분류 이론이고 로보틱스와 무관함.</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2609.09904'>Beyond Conventional Federated Learning via High-Order Regularization</a></td><td>15</td><td>0</td><td>LG</td><td>FedProx의 이차 정규화를 power-type으로 일반화해 client drift 대비 성능을 개선함. federated learning 엔지니어링이고 로보틱스와 무관함.</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2609.09920'>Multi-Pass, Multi-View Blended Learning for High-Fidelity Volumetric CT Synthesis from Chest X-Rays</a></td><td>15</td><td>0</td><td>CV</td><td>단일 흉부 X-ray로부터 3D CT를 합성하는 multi-pass multi-view 학습법임. 의료 영상 재구성이고 로보틱스와 무관함.</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2609.10032'>Field-level prediction of mid-plane stress tensor fields in concrete target penetration: a cross-velocity graph neural operator surrogate</a></td><td>15</td><td>0</td><td>LG</td><td>콘크리트 관통 중 응력장을 그래프 신경 연산자로 예측하는 시뮬레이션 대체 모델임. 물리 시뮬레이션 응용이고 로보틱스와 직접 관련은 낮음.</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2609.10099'>A Systematic Evaluation of Molecule Generation Models for De Novo Drug Design: From Benchmarks to Practical Insights</a></td><td>15</td><td>0</td><td>LG</td><td>신약 설계용 분자 생성 모델 82종을 정리한 리뷰 논문임. 서베이이고 로보틱스와 무관함.</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2609.10225'>Hierarchical and Permutation-Invariant Feature Transformation Learning via Policy-Guided Embedding Search</a></td><td>15</td><td>0</td><td>LG</td><td>정책 유도 강화학습으로 테이블 데이터의 계층적·순열불변 특징 변환을 탐색함. AutoML 응용이고 로보틱스와 무관함.</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2609.10364'>OmniMed-FL: A Robust Multimodal Federated Learning Framework for Clinical Diagnosis</a></td><td>15</td><td>0</td><td>Multimodal</td><td>흉부영상과 합성 임상노트를 federated로 융합하는 다기관 임상 진단 시스템 연구임. 의료 응용이고 로보틱스와 무관함.</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2609.10439'>Forgetting Only What Matters: Layer-Selective Unlearning toward Robust LLMs</a></td><td>15</td><td>0</td><td>NLP</td><td>forget-retain 유의도로 transformer layer를 선택해 unlearning하는 기법임. LLM 안전성 기여이고 로보틱스와 무관함.</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2609.09791'>MUCnoHARM@GermEval Shared Task 2026: Retrieval-based In-Context Learning for Defamatory Offences, and Where It Falls Short</a></td><td>15</td><td>0</td><td>NLP/Applied</td><td>독일 명예훼손 탐지를 위한 retrieval-based in-context learning shared task 참가 논문임</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2609.09964'>5-Dialects-BN: Unmasking the Impact of Transliteration on Bangla Dialectal LLMs</a></td><td>15</td><td>0</td><td>NLP/Benchmark</td><td>벵골어 5개 방언에 대한 다중 주석 벤치마크 데이터셋 구축 논문임</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2609.09974'>Towards Stress-Aware Sentence-Level Filipino G2P With Weakly-Supervised ByT5 Fine-Tuning</a></td><td>15</td><td>0</td><td>NLP/Speech</td><td>문장 수준 필리핀어 G2P를 ByT5로 파인튜닝해 강세 예측을 개선한 응용 연구임</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2609.09984'>Multi-Functional Embedding Models for Funder Name Disambiguation in Scientific Publication Records</a></td><td>15</td><td>0</td><td>NLP/Applied</td><td>연구비 지원기관명을 ROR ID에 매칭하는 다국어 임베딩 모델 연구로 응용 엔지니어링 수준임</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2609.10153'>YallaMorph: A Benchmark for Evaluating Arabic Morphological Generation in Large Language Models</a></td><td>15</td><td>0</td><td>NLP/Benchmark</td><td>아랍어 형태론적 생성을 평가하는 대규모 벤치마크 데이터셋 논문임</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2609.10198'>Politics of Feelings: Emotional Expression and Legislative Effectiveness in the U.S. Congress</a></td><td>15</td><td>0</td><td>NLP/Computational Social Science</td><td>170만 건 미 의회 연설의 감정 표현과 입법 효과성 관계를 분석한 계산사회과학 연구임</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2609.10226'>$Φ$-Bench: Can Large Language Models Engineer the Infrastructure That Powers Them?</a></td><td>15</td><td>0</td><td>LG</td><td>LLM 인프라 엔지니어링 벤치마크임. robotics·embodied AI와 무관하고 벤치마크 구축 수준의 기여임</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2609.10237'>The Answer Path and the Grounding Instruction in LLM Question Answering over Knowledge Graphs</a></td><td>15</td><td>0</td><td>NLP</td><td>KG-QA 프롬프트 구성 요소별 ablation 연구임. 자체 오류 정정은 정직하지만 범위가 좁은 실증 분석임</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2609.10253'>DiSCo: A Distribution-First Steering and Cultural Prior Evaluation Framework for Measuring Cultural Preference Bias in LLMs</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM의 문화적 선호 편향 측정 프레임워크임. 벤치마크 제안 수준이고 robotics 연관 없음</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2609.10410'>Can Foundation Models Moderate Online Content? Evaluating Instruction- vs. Example-Driven Policy Operationalization</a></td><td>15</td><td>0</td><td>NLP</td><td>VLM 기반 콘텐츠 모더레이션 비교 벤치마크임. 응용 평가 연구이고 robotics와 무관함</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2609.10445'>Building Multilingual Bridges: Data Mixing as the Pillar of Generalization for In-Language Reasoning</a></td><td>15</td><td>0</td><td>NLP</td><td>다국어 reasoning 전이를 위한 SFT 데이터 혼합 연구임. 데이터 레시피 수준의 기여임</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2609.10494'>IBIB: A Protocol for Measuring Enterprise AI Systems by Serving Route, Not Model Identifier</a></td><td>15</td><td>0</td><td>LG</td><td>엔터프라이즈 AI 시스템 평가 프로토콜 제안임. 측정 방법론 논문으로 robotics 연관 없음</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2609.09428'>XAI-Arena: Can LLMs Assess the Quality of XAI Explanations?</a></td><td>15</td><td>0</td><td>AI</td><td>LLM을 judge로 써서 XAI 설명 품질을 비교하는 프레임워크임. 평가 도구 제안 수준의 기여임</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2609.09647'>Black-Box Red Teaming of Agentic AI: A Taxonomy-Driven Framework for Automated Risk Discovery</a></td><td>15</td><td>0</td><td>AI</td><td>agentic AI에 대한 black-box red teaming 프레임워크임. 보안 평가 벤치마크이고 robotics와 무관함</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2609.09754'>LexAgentHallu: A Hierarchical Benchmark for Profiling Hallucinations in Legal Agents</a></td><td>15</td><td>0</td><td>NLP</td><td>법률 agent의 hallucination을 세분류하는 벤치마크임. 도메인 특화 진단 벤치마크 수준의 기여임</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2609.09875'>AgentAudit: An Open, Extensible Framework for Full-Lifecycle Trust Evaluation of AI Agents</a></td><td>15</td><td>0</td><td>AI</td><td>AI agent의 전체 실행 trace를 신뢰성 기준으로 감사하는 프레임워크임. 평가 도구 제안이고 robotics와 무관함</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2609.09882'>Scored vs. Generated Readouts in Behavioral Language Models: An Empirical Study of Elicitation Format</a></td><td>15</td><td>0</td><td>NLP</td><td>행동예측 LLM에서 scored 출력과 generated rationale 출력을 비교한 실증 연구임. 고객행동 예측 도메인 한정 분석임</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2609.10092'>RAP: Research Attention Prediction Reveals Target-Conditioned Evidence Acquisition Biases</a></td><td>15</td><td>0</td><td>AI</td><td>AI/ML 연구 주제의 향후 6개월 비중을 예측하는 벤치마크임. meta-science 예측 문제로 robotics와 무관함</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2609.10451'>JarvisGUI: Towards Cross-Device GUI Agents with Dynamic Task Composition</a></td><td>15</td><td>0</td><td>AI</td><td>여러 기기를 넘나드는 GUI agent 워크플로우 벤치마크임. cross-device GUI 평가이고 robotics와 무관함</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2609.10024'>AXON: A ROS 2 RMW with Shared-Memory/QUIC Transport and QKD/ML-KEM Key Establishment</a></td><td>14</td><td>2</td><td>Robotics Infra</td><td>ROS2 미들웨어에 QUIC·QKD 키교환을 적용한 통신보안 연구로 robot learning과 무관함</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2609.09185'>Integrating Unimodal and Vision-Language Representations in Latent Space for Multi-Label Chest X-Ray Classification</a></td><td>14</td><td>0</td><td>CV</td><td>흉부 X-ray 다중라벨 분류 논문이고 robotics와 무관함</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2609.09610'>Marker-free eye-gaze estimation using a single image and depth from defocus</a></td><td>14</td><td>0</td><td>CV</td><td>단일 카메라 depth-from-defocus 기반 시선추정이고 robotics와 무관함</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2609.10371'>Beyond Weak Labels: Prompt-Guided Local Refinement for Weakly Supervised Water Segmentation in High-Resolution Multispectral Imagery</a></td><td>14</td><td>0</td><td>CV</td><td>약지도 수계 분할 정제 연구이고 robotics와 무관함</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2609.09451'>Uncertainty-Aware Sea-Ice Type Mapping with Multiple Ice Charts</a></td><td>14</td><td>0</td><td>LG</td><td>해빙 유형 매핑의 라벨-모델 불확실성을 정량화한 연구이고 robotics와 무관함</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2609.09634'>LightMedSeg-ISLES: Stroke Lesion Segmentation with 81x Fewer Parameters than nnU-Net</a></td><td>13</td><td>0</td><td>CV</td><td>경량 뇌졸중 병변 분할 논문이고 경량화 중심 기여이며 robotics와 무관함</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2609.10125'>SA-Profile: Automated Sulcus Angle Profiling from Super-Resolution MRI</a></td><td>13</td><td>0</td><td>CV</td><td>MRI 기반 활차구각 자동측정 연구이고 robotics와 무관함</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2609.10230'>CougarTail &amp; CUB: A General-Purpose Mast and Central Utility Board for Cylindrical Underwater Enclosures</a></td><td>12</td><td>2</td><td>Hardware</td><td>수중로봇용 원형 PCB와 마스트 하드웨어 설계 논문으로 학습 요소가 없음</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2609.09186'>M2LG-DG: A Multi-modal Local-Global Domain Generalization Framework for Cross-site Major Depressive Disorder Classification</a></td><td>12</td><td>0</td><td>CV</td><td>fMRI 기반 우울증 분류 도메인 일반화 연구이고 robotics와 무관함</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2609.09424'>Longitudinal tracking of multiple sclerosis lesions in the spinal cord: A validation study</a></td><td>12</td><td>0</td><td>CV</td><td>척수 다발성경화증 병변 종단추적 비교연구이고 robotics와 무관함</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2609.10469'>AgroVisNet: A lightweight Convolutional Network and the BD-PlantDX Expert-Validated Benchmark for Radish, Potato and Pointed Gourd Disease Classification</a></td><td>12</td><td>0</td><td>CV</td><td>경량 작물질병 분류 네트워크이고 경량화 중심이며 robotics와 무관함</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2609.09159'>Spectral origin of the topological gap exponent d + η: mechanism, kernel, decomposition, and scope</a></td><td>12</td><td>0</td><td>LG</td><td>통계역학 topological persistence 지수의 스펙트럼 기원을 분석한 이론물리 성격 연구이고 robotics와 무관함</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2609.09721'>EFQ-Softmax: Exp-Free Quantization for Softmax</a></td><td>12</td><td>0</td><td>LG</td><td>attention softmax 경로를 exp 없이 저비트 양자화하는 커널 기법임. 순수 추론 효율화로 우선 주제가 아님.</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2609.09768'>Fine-Tuning a KV Cache Concatenation-Aware Model or Recomputing KV Caches? Why Not Both?</a></td><td>12</td><td>0</td><td>NLP</td><td>RAG의 긴 컨텍스트에서 KV cache 재사용과 선택적 재계산을 결합해 TTFT를 줄임. LLM serving 최적화이고 로보틱스와 무관함.</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2609.09788'>Evaluating Model Retraining under Drift: Paired Comparisons of Cumulative Subgroup Disparity</a></td><td>12</td><td>0</td><td>LG</td><td>재학습 정책별 subgroup fairness gap 누적을 비교 평가한 방법론 논문임. 공정성 평가 방법론이고 로보틱스와 무관함.</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2609.09794'>Privacy-Preserving Split Learning for Federated LLM Fine-Tuning</a></td><td>12</td><td>0</td><td>NLP</td><td>federated LLM fine-tuning에서 split learning의 활성화 유출을 학습된 obfuscation으로 방어함. 프라이버시 엔지니어링이고 로보틱스와 무관함.</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2609.09824'>In Medical Claims Data, Enhancing Predictive Performance for Major Adverse Cardiovascular Events Using Cross Attention</a></td><td>12</td><td>0</td><td>LG</td><td>의료 청구 데이터에 cross-attention을 적용해 심혈관 사건 예측 성능을 높임. 의료 예측 모델이고 로보틱스와 무관함.</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2609.09840'>TempTPI: Informer-Based trajectory prediction for maritime vessels</a></td><td>12</td><td>0</td><td>LG</td><td>Informer 기반으로 선박 궤적을 장기 예측하는 응용 논문임. 해양 응용이고 방법론 novelty가 낮음.</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2609.09883'>Forward-Free LLM Depth Pruning via Weight Redundancy</a></td><td>12</td><td>0</td><td>NLP</td><td>체크포인트 가중치 유사도로 LLM depth pruning을 수행하는 forward-free 기법임. 효율화 엔지니어링이고 우선 주제가 아님.</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2609.09910'>A Kernel-Based Modular Discriminant Analysis Framework for Small-Sample Learning</a></td><td>12</td><td>0</td><td>LG</td><td>KLPCDA discriminant analysis 변형들의 상호작용을 소표본 다도메인에서 체계적으로 분석함. 실험적 study 위주로 novelty가 제한적임.</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2609.09945'>Adversarial Training for Tabular Credit Scoring: A Multi-Attack Robustness Evaluation in P2P Lending</a></td><td>12</td><td>0</td><td>LG</td><td>P2P 대출 신용평가에서 여러 공격 유형에 대한 adversarial training 견고성을 벤치마크함. 표 데이터 보안 평가이고 로보틱스와 무관함.</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2609.10012'>An Explainable Machine Learning Framework for Predicting Blood-Brain Barrier Permeability Using Molecular Descriptors</a></td><td>12</td><td>0</td><td>LG</td><td>분자 기술자 기반으로 혈뇌장벽 투과성을 예측하고 SHAP으로 해석함. 신약 스크리닝 응용이고 로보틱스와 무관함.</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2609.10026'>Beyond Contact Sensors: Deep learning with Pseudo-Labeling for remote Photoplethysmography</a></td><td>12</td><td>0</td><td>CV</td><td>신호처리 기반 pseudo-label로 rPPG 심박 추정 학습 데이터 의존도를 낮춤. 의료 영상 응용이고 로보틱스와 무관함.</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2609.10089'>Hybrid Quantum-Classical NLP Classification with Compact Semantic Representations: An Experimental Analysis of Representation Compression</a></td><td>12</td><td>0</td><td>NLP</td><td>문장 임베딩을 양자 회로 입력으로 압축해 분류 성능을 비교함. 양자 ML 니치 주제이고 로보틱스와 무관함.</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2609.10108'>A Trust-Network-Based Federated Learning Framework for Multi-Center Aging Clock Prediction</a></td><td>12</td><td>0</td><td>LG</td><td>신뢰 네트워크 기반 federated learning으로 다기관 노화시계를 예측함. 의생명 응용이고 로보틱스와 무관함.</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2609.10112'>Storage-Scalable Progressive Semantic Communication via Knowledge-Base Reuse</a></td><td>12</td><td>0</td><td>LG</td><td>다단계 시맨틱 통신에서 지식베이스를 재사용해 저장공간을 줄이는 기법임. 통신 시스템 엔지니어링이고 로보틱스와 무관함.</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2609.10505'>Quantum Feature Engineering for Credit Default Prediction: When and Why IQP Circuits Help Linear Classifiers</a></td><td>12</td><td>0</td><td>LG</td><td>IQP 양자 회로 특징을 신용평가 로지스틱 회귀에 추가해 F1을 소폭 개선함. 양자 ML 니치 응용이고 로보틱스와 무관함.</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2609.10293'>GANDR: Claim Auditing for Verifiable Legal Answer Generation</a></td><td>12</td><td>0</td><td>NLP</td><td>법률 답변의 인용 검증을 위한 2-agent 파이프라인임. 특정 도메인 엔지니어링 수준의 기여임</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2609.09702'>Decision Shifts, Lost Label Functionality, and an Inconclusive Grounding Audit in Correctness-Gated Multi-Teacher Distillation</a></td><td>12</td><td>0</td><td>NLP</td><td>correctness-gated distillation의 부작용을 보고한 실패 분석 논문임. 결과가 inconclusive하다고 스스로 인정함</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2609.09853'>The Era by Eon Benchmark: A Generated Enterprise Estate with Exact Ground Truth for Benchmarking LLM Agents</a></td><td>12</td><td>0</td><td>AI</td><td>정답이 명확한 가상 기업 환경에서 enterprise agent를 평가하는 벤치마크임. 벤치마크 구축 논문이고 robotics와 무관함</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2609.09864'>Shifting Relational Paradigms for Affective Computing: Affective Resonance, Vitality Affects, and Vocal Interaction Fields</a></td><td>12</td><td>0</td><td>NLP</td><td>음성 상호작용에서 감정적 공명을 관계적 관점으로 측정한 예비 연구임. 작은 proof-of-concept 수준의 기여임</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2609.10055'>OntologyAligner: Ontology-Aligned Retrieval and Hierarchy-Guided Large Language Model Reranking for Biomedical Ontology Normalization</a></td><td>12</td><td>0</td><td>NLP</td><td>생물의학 온톨로지 정규화를 위한 검색·재순위 프레임워크임. 도메인 특화 응용 논문으로 robotics와 무관함</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2609.09625'>From State Synchronization to Cognitive Self-Evolution: An Operational Architecture for Cognitive Digital Twins</a></td><td>10</td><td>1</td><td>AI</td><td>Cognitive Digital Twin 4-layer 아키텍처 제안임. 개념적 프레임워크 논문이고 실증 근거가 lightweight 시뮬레이션 하나뿐임</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2609.10334'>Dimensionality Reduction for Hyperspectral Image Classification</a></td><td>10</td><td>0</td><td>CV</td><td>PCA·LDA와 KNN·SVM·RF를 비교한 고전적 비교연구이고 novelty가 없음</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2609.09496'>The Mutations of Machine Speech</a></td><td>10</td><td>0</td><td>NLP/Law&amp;Society</td><td>알고리즘 발화의 법적 함의를 다루는 이론적 에세이로 기술적 기여가 없음</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2609.10244'>Two-Token Features and Small-Large Ensembles for VLM Hallucination Detection</a></td><td>10</td><td>0</td><td>Multimodal</td><td>VLM hallucination 탐지 shared task 참가 시스템 설명임. 순위 경쟁용 엔지니어링 리포트에 가까움</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2609.09657'>RESCUE-BENCH: Towards Relation-Aware Multi-Party Emotional Support Conversation Systems</a></td><td>10</td><td>0</td><td>NLP</td><td>다자간 관계를 고려한 감정지원 대화 벤치마크임. robotics와 무관한 NLP 응용 연구임</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2609.10350'>Cyber-Financial Contagion: Modeling the Propagation of an AI Vendor Compromise Through the Banking System</a></td><td>10</td><td>0</td><td>AI</td><td>AI 벤더 침해가 은행 시스템으로 전파되는 과정을 네트워크 모델로 시뮬레이션한 연구임. 금융 리스크 모델링이고 robotics와 무관함</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2609.10489'>Artificial Intelligence Literacy and Sustainable Development: An Ethical Governance and Development Goals Framework</a></td><td>8</td><td>0</td><td>기타</td><td>AI 리터러시와 지속가능발전 거버넌스를 다룬 설문연구이고 CV 논문이 아니며 robotics와 무관함</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2609.10524'>Precision in Rice Variety Classification using Stacking-Based Ensemble Learning</a></td><td>8</td><td>0</td><td>CV</td><td>쌀 품종 분류 스태킹 앙상블이고 novelty가 없는 응용 논문임</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2609.10487'>Nonmaximal sums of maximally monotone operators under Rockafellar&#x27;s constraint qualification</a></td><td>8</td><td>0</td><td>LG</td><td>단조 연산자 합의 maximal성에 대한 Rockafellar 추측 반례를 구성한 순수 함수해석학 논문임. 로보틱스·ML 응용과 무관함.</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2609.10395'>Rosetta at AlexandriaX-2026: LoRA-Adapted NileChat for Context-Aware Dialectal Arabic Dialogue Translation</a></td><td>8</td><td>0</td><td>NLP</td><td>아랍어 방언 번역 shared task LoRA 파인튜닝 리포트임. 참가 시스템 기술 수준의 기여임</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2609.09306'>Gradland: On Phenomenal Experience, Differentiated Across Many Dimensions</a></td><td>8</td><td>0</td><td>AI</td><td>미분 가능 함수로 이루어진 가상 세계에서 현상적 경험을 측정하겠다는 사변적 논문임. 실증적 robotics 기여 없음</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2609.09735'>Can Artificial Intelligence Support Healthcare and Mental Health Through Early Cyberbullying Detection ? The Impact of Emotion-Aware AI on Proactive Online Safety</a></td><td>8</td><td>0</td><td>NLP</td><td>사이버불링 조기 탐지를 위한 감정인지 필터링 시스템임. 응용 엔지니어링 수준이고 robotics와 무관함</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2609.10135'>Agent-Based ML-LLM Fusion with Self-Optimizing Prompts for Plateau Weather Alerts</a></td><td>8</td><td>0</td><td>AI</td><td>고원 지역 날씨 경보를 위한 ML-LLM 융합 agent 시스템임. 응용 시스템 리포트 수준의 기여임</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2609.09226'>Adaptive Entangled Game Modules in Artificial General Intelligence</a></td><td>5</td><td>0</td><td>AI</td><td>양자·뇌 얽힘 가설을 주식시장 데이터로 검증한다는 주장임. 과학적 근거가 약하고 AGI·robotics 연결이 사변적임</td></tr>
</tbody></table>

</details>
