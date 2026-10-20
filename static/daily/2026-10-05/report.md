# 오늘의 arXiv Top 15 — 2026-10-05 (월)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**
> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)

**신규 논문 수: 전체 542편 → 중복 제거 후 542편 (이번 평가 대상 542편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 99 |
| cs.LG | 197 |
| cs.RO | 59 |
| cs.CL | 63 |
| cs.AI | 124 |

*1차 스크리닝: 전체 542편을 제목/초록 기반으로 채점(Claude (scheduled agent)) → 상위 15편은 arXiv 원문을 내려받아 정밀 리뷰(Claude (scheduled agent)) 후 최종 점수 산정.*

---

## Top 15

### 1. [80점] EyeRobot 2.0: Active Gaze for Precise Manipulation without Wrist Cameras

- **분야**: Manipulation / Active Perception · **robotics relevance**: 9/10
- **arXiv**: [2610.03710](https://arxiv.org/abs/2610.03710) ([PDF](https://arxiv.org/pdf/2610.03710))
- **저자**: Kush Hari, Justin Kerr, Nidhya Shivakumar, Samarth Mahapatra, Carmelo Sferrazza, Jiahui Lei, Jitendra Malik, C. Karen Liu 외 2명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Project Page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 스테레오 카메라 한 대로 두 눈 시점을 3D 지점에 수렴시키는 Active Visual Fixation(AVF, 능동 시선 고정)으로 손목 카메라 없이 정밀 bimanual 조작을 수행하는 프레임워크를 제안함. 실제 로봇 1000회 이상 trial에서 passive stereo 대비 40%p 높은 성공률을 냈고, 잡은 물체가 손목 카메라를 가리는 과제에서는 ego+wrist 대비 2배 성능을 보임.

**Core innovation & methodology**

- 스테레오 카메라 한 대만으로 두 눈 시점을 3D fixation point에 수렴시켜 손목 카메라 없이 정밀 조작을 수행하는 AVF 프레임워크를 제안함
- gaze를 두 단계로 나눠 학습함: 목표 물체에 수렴하는 저수준 gaze servoing 정책(기하학적 reward로 RL 학습)과 과제 진행에 따라 볼 곳을 정하는 고수준 target selector(RL, BC gripper 정책의 예측 오차를 reward로 co-training)
- fixation 지점 주변에 더 많은 visual token을 배정하는 foveated multi-resolution crop 표현으로 연산을 과제 관련 영역에 집중시킴
- gripper proprioception과 action chunk를 고정된 월드 좌표가 아니라 회전하는 fixation-relative SE(3) 프레임으로 정준화해 학습할 action 분포의 크기를 줄임

**Novelty vs. prior works**

- 가장 가까운 선행연구는 저자 자신들의 EyeRobot(360도 카메라 기반 gaze 정책)이며, 이 논문은 이를 스테레오 카메라로 옮기고 foveation·fixation-relative action·계층적 target selector를 추가해 더 정밀한 bimanual task에 적용한 체계적 확장에 가까움
- gaze demonstration 없이 BC-RL co-training으로 gaze 시퀀스를 발견하는 핵심 아이디어는 EyeRobot에서 이미 제시됐고, 2.0의 기여는 스테레오 영상을 광학 중심 회전만으로 워핑해 fixation을 합성한 점(3D reconstruction 불필요)과 fixation 프레임 action canonicalization에 있음
- 손목 카메라를 아예 없애고 ego 카메라만으로 손목 카메라 수준 성능을 재현한다는 문제 설정은 실용적으로 새롭고, active vision을 viewpoint selection이 아니라 fine-grained eye movement 자체에 쓴 점에서 기존 active vision 연구와 구분됨

**Benchmark results**

- 실제 로봇 7개 과제에서 1000회 이상, 시뮬레이션 6개 과제에서 1800회 trial로 비교함
- passive stereo(No Gaze) 대비 real 평균 +40%p, sim 평균 +20%p 향상시켰고, wrist 카메라 제거 시 No Gaze는 real 성공률이 52%에서 27%로 떨어짐
- wrist 카메라가 가려지지 않는 과제(marker, tea, toaster, wrench)에서는 ego+wrist와 비슷함(69% vs 64%), 잡은 물체가 wrist 카메라를 가리는 과제(boba, pot)에서는 ego+wrist 대비 2배 이상 성능(48% vs 22%)
- ablation: foveation 제거 시 real 평균 -20%p 하락
- ablation: action을 world frame으로 바꾸면 sim에서 gaze-free baseline 수준으로 떨어짐(-21%p)
- ablation: stereo 대신 mono+깊이 제거 시 real 평균 -18%p 하락
- distractor를 섞은 상황에서 첫 grasp 성공률이 ego-only·ego+wrist보다 높음(wrench 과제 기준 AVF 20/25 vs ego-only 10/25 vs ego+wrist 3/25)

**Top-tier conference 적합성 — 80/100 · 추천 venue: CoRL**

실제 로봇 1000회 이상 trial과 다수 ablation, failure mode 분석(Sankey diagram)까지 갖춰 empirical conviction이 강하고 CoRL이 선호하는 real-robot 중심 기여와 잘 맞음. 다만 과제별로 별도 정책을 학습하는 task-specific 세팅이고 자사 이전 연구(EyeRobot)의 확장이라 conceptual leap은 제한적이어서, NeurIPS/ICML급 oral보다는 CoRL oral/highlight 수준으로 보임.

**추천 이유 & 누리랩 연구와의 연결점**

- active perception 주제와 직결됨: 과제 진행에 따라 볼 곳을 정하는 target selector 구조를 VLA 정책의 subgoal·attention 선택 모듈로 가져올 수 있음
- failure detection/recovery 연구에 연결 가능: fixation point의 3D 추정 오차나 gaze가 머무는 위치를 모니터링해 조작 실패 징후를 조기에 포착하는 신호로 쓸 수 있음
- object-centric 3DGS·scene graph 연구와 접점이 있음: 현재는 스테레오 depth로 fixation point를 추정하는데, 이를 object-centric 3D representation으로 대체하면 더 일반화된 gaze target 선택이 가능할 것으로 보임

---

### 2. [79점] Keep the Effect, Drop the Actor: Programmable Effect-to-Execution World-Action Models

- **분야**: World Model / Manipulation · **robotics relevance**: 9/10
- **arXiv**: [2610.02398](https://arxiv.org/abs/2610.02398) ([PDF](https://arxiv.org/pdf/2610.02398))
- **저자**: Junyi Hu, Zhewen He, Zhenhua Li, Yi Fang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 76점

> 💡 로봇 시연에서 객체에 일어난 변화만 남기고 로봇 팔의 움직임은 버리는 effect program(객체 keypoint 궤적, grasp를 나타내는 contact point 2개, 종료 상태)을 정의해서 world-action model PEWAM을 학습시킴. 이 program을 조건으로 매 4 step마다 재계산(closed loop)하면 한 번의 시연만으로 held-out task를 풂.

**Core innovation & methodology**

- effect program 정의: 객체의 box keypoint 9개, grasp를 나타내는 contact point 2개, 종료 상태(terminal state)로 시연을 로봇 geometry 없이 표현함.
- DiT backbone 하나(71.5M)가 effect(E), end-effector execution(R), native action(A), terminal state(G) 네 스트림을 각각 독립된 flow-matching time으로 학습해서, 어느 스트림을 clean으로 고정하느냐에 따라 같은 가중치로 inverse/goal/forward/inverse-dynamics 네 질의에 전부 응답함.
- inference를 program(E, G)을 clamp하고 execution(R, A)만 sampling하는 것으로 재정의해 "programming"이라 부르고, 매 4 control step마다 라이브 장면에서 다시 풂.
- progress를 로봇이 일으킨 effect로만 인정하는 engagement gate를 둬서, 밀침(push) 같은 외란을 실패가 아니라 program을 다시 풀어야 할 새 observation으로 흡수함.
- program은 로봇 팔 4종에 재학습 없이 옮겨 타고, 사람이 program 좌표를 직접 편집할 수 있음.

**Novelty vs. prior works**

- 가장 가까운 선행연구는 Im2Flow2Act(object flow로 task 전달, flow는 별도 모델이 생성하고 flow-conditioned policy로 실행)와 UWM(독립 timestep의 video-action diffusion). PEWAM은 flow를 따로 생성하지 않고 시연 자체에서 읽어내며, contact point와 terminal state를 더해 grasp와 도착 상태까지 하나의 program에 담은 점이 실질적 차이임.
- contact를 affine weight가 아니라 좌표 점으로 둬야 편집이 가능하다는 것을 ablation으로 직접 보임(weight로 인코딩하면 회전 명령 부호와 반대로만 실현됨, Table 5·Appendix N). representation 설계 수준의 기여임.
- "demonstration에서 actor를 떼고 effect만 남긴다"는 전제 자체는 object-centric manipulation 계열(Track2Act, General Flow, ReKep 등)이 이미 공유하는 아이디어라 problem formulation의 새로움은 제한적이고, 새로움은 주로 four-stream 단일 모델 설계와 contact-as-point 편집 가능성 쪽에 있음.

**Benchmark results**

- LIBERO-Goal held-out task 3개(90 episode)에서 program 조건 40/90(44.4%) 완료, 공개된 demonstration-conditioned method는 모두 더 낮음(UWM 21.1%, Instant Policy 5.6%, ATM·Zero-WAM 0%).
- 같은 held-out task에서 시연을 그대로 replay하면 96.7% 성공 — program 방식이 demonstrator 동작을 그대로 복사하는 것보다 본질적으로 약하다는 걸 저자가 직접 인정함(§5 limitation).
- Meta-World held-out class 중 shelf-place·sweep-into·bin-picking에서는 공개 baseline(DAMI 등)을 모두 상회하지만, 5-class 평균에서는 DAMI보다 낮음(ML10 49.8 vs 56.8, ML45 34.0 vs 37.5).
- RLBench 24개 held-out task에서 program은 160/720(22.2%)로 no-program 108/720(15%)보다는 낫지만, 전문 방법 Instant Policy의 575/720(79.9%)에는 크게 못 미침.
- push 후 재계산 23/60 성공 vs demo replay 6/60.
- 로봇 팔 4종(Panda/KUKA IIWA/Kinova3/UR5e 순서) 재학습 없이 bowl task 27·24·22·16/30.
- 실제 Franka 팔(다른 task 156개 real demo로 fine-tune)에서 사람 비디오로 만든 program이 36/40, 동일 backbone에 마지막 프레임을 goal image로 준 경우는 22/40.

**Top-tier conference 적합성 — 72/100 · 추천 venue: CoRL**

actor-free effect program과 독립 flow-matching stream 설계를 4개 로봇 팔·real Franka 검증까지 갖춰 CoRL 수준의 실험적 증거는 확보함. 다만 RLBench에서 specialist 대비 격차가 크고 Meta-World 5-class 평균에서 기존 baseline보다 낮으며, 대부분의 셀이 30 episode 단일 training이라 replicate 간 차이가 보고된 결과 차이만큼 크다는 점(저자가 명시)이 oral 심사에서 지적될 약점임.

**추천 이유 & 누리랩 연구와의 연결점**

- test-time optimization/failure recovery: program을 매 4 step 재계산하는 구조와 push를 "새 observation"으로 재해석하는 engagement gate는 누리랩의 test-time re-planning·failure recovery 연구와 바로 연결됨.
- object-centric 3DGS/scene graph: 현재 entity는 rigid box keypoint로만 표현되는데, 이를 object-centric 3DGS나 scene graph로 교체하면 비강체 객체·다중 객체 상호작용까지 program으로 확장할 여지가 있음.
- VLA와의 역할 분리: actor-free program을 VLA의 중간 출력으로 쓰고 PEWAM류 executor가 재계산 실행을 맡는 구조를 누리랩 VLA 연구에서 검토할 만함.

---

### 3. [78점] World-Calibrated Proposal-to-Action Flow for Vision-Language-Action Models

- **분야**: VLA / Manipulation · **robotics relevance**: 9/10
- **arXiv**: [2610.02323](https://arxiv.org/abs/2610.02323) ([PDF](https://arxiv.org/pdf/2610.02323))
- **저자**: Jie He, Wei Li, Junwen Tong, Rui Shao, Wei-Shi Zheng, Liqiang Nie
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 25 pages, 10 figures. Project page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 Flow 기반 VLA가 매번 isotropic Gaussian에서 액션을 생성하느라 최근 동작의 연속성과 미래 예측 정보를 못 쓰는 문제를 지적함. 최근 동작을 proposal로 만들고 world model이 그 proposal을 얼마나·어느 방향으로 고칠지 계산해 source 분포 자체를 바꾸는 ProAct를 제안함. π0.5 대비 denoising step을 50% 줄이면서 성능도 올림.

**Core innovation & methodology**

- propose-calibrate-refine 구조: Gaussian noise 대신 최근 액션을 모션 외삽 후 flow-matching 한 스텝으로 scene-aware proposal을 만들어 생성 시작점을 demonstration 액션 매니폴드 근처로 당김
- World Expert가 frozen V-JEPA 2 latent future를 예측 타깃으로 쓰면서, 동시에 proposal과 실제 demonstration의 residual로부터 교정 정도(extent)와 방향(low-rank geometry)을 추론함
- extent·geometry로 translation/rotation/gripper 차원에 걸친 anisotropic covariance를 구성해 source 분포를 교체하되, 기존 flow 기반 VLA의 transport parameterization 자체는 그대로 둠
- bounded per-step extent와 trace-normalized low-rank에 condition-number budget(S_max)을 걸어 source가 한 방향으로 퇴화하거나 과도하게 좁아지는 것을 막음

**Novelty vs. prior works**

- source를 informative하게 만드는 방향은 Streaming Flow Policy, A2A, VITA 등 선행 연구에도 있음. ProAct의 차별점은 proposal을 그대로 쓰지 않고 world model이 예측한 미래와의 compatibility로 '얼마나·어느 방향으로' 벗어날지를 계산해 covariance 자체를 결정한다는 점임
- DreamVLA·WorldVLA·VLA-JEPA 같은 world model 결합 VLA는 미래 예측을 조건으로만 쓰는데, ProAct는 미래 예측 결과를 source의 extent·geometry라는 구체적 수치로 변환해 생성 과정에 직접 개입시킴
- 다만 flow-matching proposal step, frozen V-JEPA 2 latent target, low-rank covariance는 각각 선행 요소들의 재조합에 가까워서 완전히 새로운 패러다임이라기보다 기존 조각들을 하나의 보정 인터페이스로 엮은 설계에 가까움

**Benchmark results**

- LIBERO: 평균 98.4%로 backbone π0.5(96.9%) 대비 +1.5점, Long suite에서는 격차가 3.6점으로 더 커짐
- LIBERO-Plus(재학습 없이 7종 perturbation 평가): 86.8%로 π0.5 대비 +13.2점, 최강 경쟁 baseline 평균 대비 +7.3점, Noise/Camera/Robot shift에서 가장 큰 개선(14.8~18.1점)
- RoboTwin 2.0(50 task 학습, zero-shot randomized hard 평가): 평균 60.3%로 π0.5(28.6%) 대비 +31.7점, 최강 baseline(Spatial Forcing 34.6%) 대비 +25.7점
- real-world 2개 플랫폼(Galaxea R1 Lite, AgileX Cobot Magic) 6 task 25회 시행: π0.5 대비 overall TSR/CSR이 Galaxea에서 +8.7/+6.4점, AgileX에서 +10.0/+8.3점
- 효율성: denoising step 50% 감소, latency -25.8%(sim)/-16.3%(real), throughput +34.8%/+19.5%. ablation상 World Expert 제거 시 성능 하락폭이 가장 큼(LIBERO -1.9점, real-world -8.0점)

**Top-tier conference 적합성 — 70/100 · 추천 venue: CoRL**

실로봇 2개 embodiment, sim 3개 benchmark, component별 ablation까지 갖춘 실험 강도가 높고 효율성 수치도 구체적이라 CoRL/ICRA급 robotics venue에 적합함. 다만 핵심 메커니즘이 기존 source-design·world-model VLA 계열의 조합에 가까워 개념적 도약보다는 탄탄한 엔지니어링 기여로 보여서, oral/highlight까지는 novelty 측면에서 다소 약할 위험이 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- World Expert가 산출하는 extent(U)는 proposal-미래 compatibility 신호라서, 값이 크게 튀는 순간을 failure detection/online anomaly 신호로 재활용하는 실험이 가능함
- 논문이 스스로 한계로 명시한 부분: factual trajectory만으로 학습해 proposal을 바꿨을 때 실제 결과가 어떻게 달라지는지는 보지 않음. 이는 counterfactual reasoning 쪽 연구 공백과 바로 연결됨
- 50% denoising step 감소는 test-time optimization/inference-time efficiency 연구와 바로 이어지는 결과라, world model 기반 source calibration을 다른 test-time 기법과 결합해 보는 방향이 있음

---

### 4. [76점] Native Action-Prior Learning from Videos for World Action Models

- **분야**: World Model / VLA (Manipulation) · **robotics relevance**: 9/10
- **arXiv**: [2610.03391](https://arxiv.org/abs/2610.03391) ([PDF](https://arxiv.org/pdf/2610.03391))
- **저자**: Zhaochong An, Fei Zhang, Menglin Jia, Duncan Frost, Zijian Zhou, Yikai Wang, Xudong Wang, Aditya Patel 외 5명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: Project Page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 Observation-only 비디오로 action policy(Action-DiT)를 직접 사전학습해서 video representation이나 latent-action 같은 중간 인터페이스를 없앤 world action model임. 특히 OOD 세팅(RoboTwin2.0 Random)과 실로봇 Franka FR3에서 기존 joint WAM·latent-action 방법 대비 큰 폭으로 성능이 좋아짐.

**Core innovation & methodology**

- native action-prior learning 제안: 중간 representation이나 latent-action model 없이, observation-only 비디오의 future-video flow-matching objective로 Action-DiT 파라미터를 직접 최적화함
- Mixture-of-Transformers 구조에서 Video-DiT와 Action-DiT가 joint attention으로 상호작용하되, pretraining 때는 Video-DiT를 freeze하고 Action-DiT만 학습함
- transition-structured joint attention으로 clean 과거 state·noised 미래 state·action 토큰을 하나의 segment로 묶어, 명시적 latent action 변수 없이 attention 안에서 inverse-forward dynamics를 암묵적으로 구현함
- post-training 단계에서는 asymmetric attention으로 비디오 스트림을 action 스트림과 분리해 video KV를 캐싱하고, action만 반복 denoising해서 future video를 생성하지 않고도 효율적인 action-only inference를 가능하게 함

**Novelty vs. prior works**

- 가장 가까운 비교군은 latent-action learning 계열(LAPO, LAPA, Motus, RepWAM)인데, 이들은 별도의 latent-action 모델과 shortcut 방지용 구조적 제약이 필요함. 이 논문은 그 중간 인터페이스를 attention mask 설계로 대체한 것이 핵심 차이임
- vision representation learning 계열(R3M, VPP, V-JEPA2)과 비교하면 사전학습 단계에서 실제로 업데이트되는 파라미터가 policy 자체(Action-DiT)라는 점에서 representation-to-control 간접 전이 문제를 구조적으로 없앴다는 주장은 설득력 있음
- 다만 architecture(MoT), objective(flow matching), inverse-forward factorization(LAPO 기반)는 모두 기존 요소를 조합한 것이고, 새로움은 pretraining 단계의 attention masking 설계 하나에 집중되어 있어 paradigm 수준의 전환이라기보다는 기존 joint WAM 계열(DreamZero, Fast-WAM) 안에서의 정교한 변형에 가까움

**Benchmark results**

- LIBERO 99.0%/LIBERO-Plus(OOD) 83.5%로 ID는 최고 baseline(Being-H0.7 99.2%)과 비슷하고 OOD는 소폭 앞섬(+1.4%p)
- RoboTwin2.0에서 Clean 88.5%/Random(OOD) 73.6%로, 최강 baseline MV-WAM(84.0/55.7) 대비 Clean +4.5%p, Random +17.9%p로 OOD 격차가 큼
- 실로봇 Franka FR3 3개 tabletop task(5 trial씩, 총 15 trial)에서 93.3% 성공, DreamZero 66.7%·π0.5 53.3% 대비 우위. task·trial 수가 적어 통계적 여유는 크지 않음
- action-label 효율성: RoboTwin2.0에서 25 demo/task만으로 72.0% 달성, representation-based(60.6%)·latent-action-based(65.0%) 대비 우위이고 이 baseline들의 50-demo 결과보다도 높음
- ridge-regression R2로 측정한 action-relevance에서 0.247~0.329로 representation-based(0.08~0.157)·latent-action-based(0.052~0.203)보다 크게 높아, 학습된 표현이 실제 action과 더 직접 연관됨을 보임
- inference 연산량은 4.30 TFLOPs로 Image-WAM(4.09)·Fast-WAM(3.56)과 비슷한 수준이면서 OOD 성능은 크게 앞섬

**Top-tier conference 적합성 — 78/100 · 추천 venue: CoRL**

LIBERO/LIBERO-Plus·RoboTwin2.0 두 benchmark family의 ID/OOD 비교, pretraining 방식별 통제 ablation, 실로봇 배포까지 갖춰 실험적 증거가 탄탄함. 다만 novelty가 attention masking을 통한 암묵적 inverse-forward dynamics 구현 하나에 집중돼 있고 실로봇 평가가 3 task·15 trial로 작은 편이라, top-tier 중에서도 oral보다는 포스터급 accept 가능성이 더 높아 보임. 본문에서 명시적 limitations 섹션은 확인 안 됨.

**추천 이유 & 누리랩 연구와의 연결점**

- world model 라인에서 future-video prediction을 policy 자체에 직접 공급하는 방식은, 우리 lab의 failure detection/recovery 연구에서 video 예측을 암묵적 상태 진단 신호로 쓰는 데 참고할 만함
- test-time optimization 관점에서, video branch를 action 생성 전 저비용 rollout 검증 수단으로 확장하면 inference-time replanning이나 실패 사전 감지에 활용 가능함
- label efficiency 결과(25 demo로 baseline의 50-demo 능가)는 실로봇 데이터 수집이 비싼 manipulation 과제에서 demo 수를 줄이는 사전학습 전략으로 바로 참고 가능함

---

### 5. [74점] Rethinking World-Action Model for Compositional and In-Context Robotic Manipulation

- **분야**: World Model (Robotic Manipulation) · **robotics relevance**: 9/10
- **arXiv**: [2610.02368](https://arxiv.org/abs/2610.02368) ([PDF](https://arxiv.org/pdf/2610.02368))
- **저자**: Shukai Gong, Xuanran Zhai, Yintianrun Zhang, Ruopeng Cui, Ye Huang, Yiyang Fu, Dexuan Lyu, Chaojie Li 외 11명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 19 pages, 9 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 world-action model을 visual subgoal planner와 subgoal executor로 나눠서 long-horizon compositional manipulation을 처리하는 ViGAR를 제안함. subgoal 이미지를 명시적 중간 목표로 써서 RoboTwin에서 기존 최강 baseline보다 평균 12.86%p 높은 성공률을 냈고, 실로봇 7개 task에서도 일관되게 앞섬.

**Core innovation & methodology**

- compositional manipulation을 long-term future selection(subgoal planner)과 short-term future realization(executor)으로 분해하고, 둘 다 같은 pretrained world model(Cosmos3-Nano)에서 초기화해 물리 지식을 공유함.
- subgoal planner는 이미지 editing 문제로 재정의해서, 현재 관측과 전역 instruction으로 다음 subgoal 이미지를 flow matching으로 생성함.
- subtask 경계에서 subgoal이 혼동되는 문제를 막기 위해 subgoal look-ahead rule을 둠 — 현재 subtask 끝자락 프레임의 학습 타깃을 다음 subgoal로 재할당함.
- executor는 예측된 subgoal을 VAE latent로 변환해 generator branch에 직접 주입(geometric route)하고, video와 action을 하나의 flow matching objective로 동시 생성함.

**Novelty vs. prior works**

- 가장 가까운 선행연구인 BagelVLA, RxBrain도 subtask text·subgoal image를 interleaved로 생성하지만, 그 예측이 implicit feature로만 policy에 영향을 주거나 planning 출력에 그침. ViGAR는 subgoal을 policy의 explicit 조건(VAE latent)으로 직접 주입한다는 점에서 차별화됨.
- in-context robotic manipulation 개념도 재정의임 — Zero-WAM, HOST, Skild S1 같은 기존 robot ICL은 시연 영상으로 '어떻게' 할지 지정하지만, ViGAR는 global goal image로 '무엇이' 될지만 지정하고 subtask 분해는 모델이 알아서 함.
- 다만 architecture 자체는 기존 pretrained world model(Cosmos3-Nano) 위에 이미 확립된 post-training recipe를 그대로 쓴 것이고, look-ahead rule·ROI weighting은 formulation 참신성에 비해 구현 디테일에 가까워서 technical novelty는 제한적임.

**Benchmark results**

- RoboTwin Clean2Random에서 Clean 82.00%, Random 67.02%, 평균 74.51%로, 가장 강한 baseline인 4D-WAM(평균 61.65%)보다 12.86%p 높음.
- 같은 Cosmos3-Nano backbone에서 subgoal guidance만 뺀 Cosmos3-Nano-RoboTwin은 Random에서 22.46%에 그쳐서, 성능 향상 대부분이 subgoal conditioning 덕분임을 보여줌.
- 실로봇 5개 compositional task(AgiBot A2, task당 20 rollout) 평균 progress score는 ViGAR 0.69로, π0.5 0.60·Cosmos3-Nano-Policy 0.54보다 높음.
- in-context task(Fruit Arrangement, Desktop Item Storage)는 in-domain 평균 progress 0.72~0.83이지만 OOD global goal에서는 0.43~0.52로 떨어져 ICL 일반화에는 한계가 있음.
- ablation에서 subgoal look-ahead와 EEF ROI weighting을 둘 다 빼면 평균 성공률이 74.51%에서 62.54%로 떨어져 두 구현 디테일의 기여가 확인됨.

**Top-tier conference 적합성 — 70/100 · 추천 venue: CoRL**

RoboTwin sim 벤치마크와 real-world 7개 task(5 compositional + 2 in-context)를 모두 갖춰 실험적 증거가 탄탄하고, in-context robotic manipulation이라는 새 문제 설정을 던져서 CoRL·RSS 커뮤니티의 관심을 끌 만함. 다만 backbone이 기존 Cosmos3-Nano 재사용에 의존하고 subgoal guidance 자체는 BagelVLA·RxBrain과 아이디어가 겹쳐서, oral보다는 poster·spotlight 수준으로 보이고 reject risk는 technical depth 약함 쪽에 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- subgoal을 명시적 decision variable로 쓰는 방식은 failure detection/recovery로 바로 확장 가능함 — 예측 subgoal과 실제 진행 상태의 괴리를 test-time에 모니터링해서 실패를 조기에 감지하는 데 쓸 수 있음.
- in-context robotic manipulation(terminal goal image만으로 subtask decomposition 유도)은 counterfactual reasoning과 연결됨 — '이 목표였다면 어떤 경로를 택했을까'를 묻는 test-time 질의로 확장할 수 있음.
- subgoal이 2D pixel 수준에 머물러 있어서, object-centric 3DGS나 scene graph로 subgoal을 표현하면 occlusion·viewpoint 변화에 더 강건한 compositional manipulation으로 이어질 수 있음.

---

### 6. [74점] PointWAM: 3D World Action Modeling for Dexterous Robotic Manipulation

- **분야**: World Model (Dexterous Manipulation) · **robotics relevance**: 9/10
- **arXiv**: [2610.02840](https://arxiv.org/abs/2610.02840) ([PDF](https://arxiv.org/pdf/2610.02840))
- **저자**: Chunghyun Park, Beomjun Kim, Seungcheol Park, Heeseung Kwon, Yashu Shukla, Seunghoon Sim, Jinwoo Shin, Minsu Cho
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Preprint. Project page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 76점

> 💡 PointWAM은 월드를 scene(환경)과 hands(행위자)로 나눠 하나의 공유 3D space-time 좌표계에서 point trajectory로 함께 예측하는 world action model임. 사람 시연 비디오로 backbone을 사전학습한 뒤 예측된 hand trajectory를 로봇 action으로 retargeting해서, DexJoCo 10-task에서 기존 최강 baseline보다 11.7%p 높은 성공률을 보임.

**Core innovation & methodology**

- 월드를 scene(환경)과 hands(행위자)로 명시적으로 분리하고, 둘 다 같은 공유 3D space-time 좌표계에서 3D point trajectory(변위)로 동시에 예측함.
- frozen Mosaic3D 3D encoder로 scene point feature를, MLP로 hand keypoint(손당 10개) feature를 뽑아 transformer encoder에서 함께 처리하고, scene trajectory U와 hand trajectory V를 각각 MLP head로 예측함.
- action retargeter는 예측된 hand trajectory V와 로봇 state만 입력받아 transformer decoder로 action chunk(엔드이펙터 pose+손가락 joint)를 뽑음 — scene forecast는 backbone 학습에만 쓰이고 retargeter에는 들어가지 않음.
- 사람 시연 비디오(EgoDex+VITRA, 총 1.15M episode)에서 CoTracker3+깊이 추정으로 scene/hand trajectory를 뽑아 backbone을 먼저 사전학습하고, 로봇 시연으로 trajectory loss+action loss를 더해 fine-tuning하는 2단계 학습임. scene head가 모든 관측 point를 대상으로 하기 때문에 task별 object·keypoint를 미리 고를 필요가 없음.

**Novelty vs. prior works**

- 가장 가까운 prior work인 EgoWAM, PointWorld, PointZero, Pri4R과 비교해 scene과 hand를 하나의 backbone·동일한 3D point trajectory 표현으로 동시에 예측하고 별도 planner 없이 바로 action까지 retarget하는 게 차별점임. EgoWAM은 hand motion을 parallel-jaw gripper 6-DoF pose+gripper state로만 매핑해 개별 손가락 움직임을 못 담고, PointWorld·PointZero는 action을 아예 예측하지 않거나 future robot trajectory를 입력으로 받는 별도 planner가 필요함.
- 다만 "3D point trajectory로 world와 action을 함께 모델링"한다는 문제의식 자체는 2026년 동시기에 나온 여러 논문(3PoinTr, DyWA, 4D-WAM, WSA1, Dexterous World Model 등 저자들이 직접 인용)과 겹쳐서, 패러다임 자체의 신규성보다는 dexterous hand에 맞춘 정교한 조합·실증에 가까운 기여임.
- scene-trajectory supervision과 3D encoder 선택이 실제로 성능에 기여한다는 점은 ablation으로 보였지만(각각 +10.9%p, +5.4%p), 이는 설계 선택의 유효성 검증이지 새로운 learning principle을 제시한 건 아님.

**Benchmark results**

- DexJoCo 10-task multi-task 정책 기준 평균 성공률 69.0%로, 최강 baseline GR00T N1.6(57.3%) 대비 11.7%p, π0.5(50.0%) 대비 19.0%p 높음. sim-only 벤치마크임.
- EgoDex pretraining 유무 비교에서 PointWAM은 12.1%→60.1%로 거의 5배 상승했는데, GR00T N1.6/Fast-WAM/PointACT는 최대 1.4%p밖에 안 오름 — pretraining 전이 효과가 baseline 대비 압도적으로 큼.
- human demo를 324K(EgoDex)에서 1.15M(EgoDex+VITRA)까지 늘리면 60.1%→69.0%, trainable parameter를 39M→655M로 늘리면 52.3%→69.0%로 데이터·모델 스케일링이 둘 다 확인됨.
- RoboDojo-Precision(parallel-jaw gripper, 8 task)에서는 평균 score 8.8/SR 4.8%로 1위지만, GR00T N1.6도 6.2/2.3%에 그칠 만큼 전체 성공률 자체가 매우 낮아 일반화 강도는 제한적임.
- 실로봇(OpenArm humanoid) 2 task 24 trial에서 banana PnP out-of-domain 58.3% (GR00T 16.7%, π0.5 25.0%), square-peg insertion 50.0% (GR00T 16.7%, π0.5 25.0%)로 큰 격차를 보였으나 task당 trial 수가 24회로 적어 통계적 여유는 크지 않음.

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

DexJoCo·RoboDojo-Precision·실로봇 세 세팅에서 일관된 큰 폭 개선과 체계적 ablation(vision encoder, world modeling 유무, hand representation, voxel size, data/model scaling)을 갖춰 CoRL 수준 submission으로는 설득력 있음. 다만 같은 시기에 나온 유사한 3D point trajectory 기반 world action model이 다수 존재해(EgoWAM, PointWorld, PointZero, 3PoinTr 등) reviewer가 조합형 기여로 볼 위험이 있고, RoboDojo-Precision 성공률 자체가 한 자릿수에 그쳐 real-world 일반화 주장은 조심스럽게 읽어야 함.

**추천 이유 & 누리랩 연구와의 연결점**

- scene(환경)과 actor(손)를 분리해서 같은 3D 표현으로 공동 예측하는 설계는 object-centric 3DGS·scene graph 작업에서 "환경 표현을 행위자 표현과 분리해 따로 추적"하는 아이디어로 가져올 수 있음.
- scene trajectory forecast와 실제 rollout 결과의 괴리를 모니터링하면 contact 실패를 사전에 감지하는 test-time 신호로 쓸 수 있어 보이는데, 이 논문은 failure detection 방향은 다루지 않음.
- 로봇 데이터 없이 사람 시연 비디오 pretraining만으로 training-from-scratch 대비 평균 56.9%p 개선(다른 설정에서의 ablation은 12.1%→60.1%, +48.0%p)을 낸 결과는 VLA나 robot memory 연구에서 "로봇 데이터 부족을 사람 비디오로 메운다"는 전략의 구체적 근거 사례로 인용할 만함.

---

### 7. [72점] World Action Learning via Interaction-Centric Spectral Latent Guidance

- **분야**: VLA / World Action Model (egocentric video 기반 robot transfer) · **robotics relevance**: 9/10
- **arXiv**: [2610.03607](https://arxiv.org/abs/2610.03607) ([PDF](https://arxiv.org/pdf/2610.03607))
- **저자**: Zhiming Liu, Yikun Miao, Ying Chen, Hongrui Yin, Fangqi Zhu, Xiaoyi Pang, Quanxin Shou, Zhengyang Yan 외 2명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 WING은 egocentric video에서 카메라 모션과 hand-object interaction 모션을 point tracking으로 분리해 interaction-centric latent action을 학습하고, 이 latent trajectory를 DCT로 분해해 저주파 성분만 로봇 action 생성의 guidance로 씀. LIBERO 99.20%, RoboTwin 2.0 93.80%, RoboCasa-GR1 57.7%를 달성해 π0.5·LingBot-VA 등 baseline을 능가하며, real-world bimanual task는 standard setting에서 앞서지만 generalization setting에서는 success rate가 π0.5와 비슷함.

**Core innovation & methodology**

- interaction-motion decoupling: offline point tracker로 배경 track과 hand-object interaction track을 분리하고, 배경 track으로 global affine warp(카메라 모션 target)을 추정한 뒤 나머지 residual displacement를 interaction motion target으로 씀.
- teacher-student distillation: tracking·warp 같은 privileged cue로 학습한 teacher의 interaction latent를 RGB-only student에 distill하고, camera-perturbed view에 대한 consistency loss로 student latent의 camera-invariance를 강제함.
- spectral latent guidance: latent action trajectory를 DCT(discrete cosine transform)로 분해해 저주파 K개 성분만 guidance target으로 남김. lightweight predictor가 현재 observation·instruction에서 이 저주파 guidance를 추정해 action model에 gated cross-attention으로 주입함.
- 2단계 학습: egocentric video로 video model과 guidance predictor를 먼저 pretrain한 뒤, robot demonstration으로 action expert와 guidance predictor를 fine-tuning함 (WING-LAM encoder는 freeze).

**Novelty vs. prior works**

- 가장 가까운 prior work은 action-irrelevant variation 제거를 노리는 CD-LAM, 그리고 DreamDojo·LAPA·UniVLA 같은 latent action model임. WING은 일반적인 debiasing이 아니라 point tracking 기반 global/local motion 명시적 분해 + teacher-student distillation으로 카메라 모션을 구조적으로 제거한다는 점이 다름. 논문 Fig3(a)에서 CD-LAM도 자신들 평가 기준으로는 여전히 카메라 모션 정보를 많이 보존한다고 보여 차별점을 실증함.
- 저주파 DCT 성분이 cross-embodiment로 더 잘 대응한다는 관찰(Fig3d)은 경험적으로는 새롭지만, DCT 자체는 표준 신호처리 도구라 novelty는 "발견 + latent action pipeline에의 적용" 수준이지 새로운 learning paradigm은 아님. 기존 latent-action+world-action-model 구조에 분해·필터링 모듈 두 개를 추가한 형태에 가까움.
- 카메라-interaction 분리가 point tracker와 단일 global affine warp에 의존하는데, 저자도 limitation에서 강한 parallax·큰 depth 변화·3D 카메라 모션에서는 이 근사가 부정확해질 수 있다고 인정함.

**Benchmark results**

- LIBERO 평균 99.20%로 π0.5(96.90%), LingBot-VA(98.50%), Fast-WAM(97.60%), LaWAM(98.60%) 대비 소폭 우위이며 long-horizon suite(99.00%)에서 격차가 상대적으로 큼.
- RoboTwin 2.0 평균 93.80%로 LingBot-VA(92.20%), Fast-WAM(91.83%), LaWAM(91.22%)보다 clean·randomized 양쪽 모두에서 높음.
- RoboCasa-GR1(humanoid) 57.7%로 저자 재현 FastWAM(51.9%), LDA-1B(55.4%) 대비 우위지만 절대 성공률은 여전히 60% 미만.
- Real-world bimanual task 4개: standard setting 평균 75.0%로 비교군 중 최고, generalization setting에서는 π0.5와 success rate는 비슷하고 progress score만 소폭 우위 — 완전한 우위는 아님.
- Ablation(ego-pretraining 없는 controlled 세팅, Table 3): WING-LAM과 DCT 모두 적용 시 real-world base/gen 72.5%/45.0%, 둘 다 제거 시 65.0%/36.0%로 두 모듈 모두 일관되게 기여함. DCT 계수 수는 K=4가 {2,4,8} 중 최적.

**Top-tier conference 적합성 — 65/100 · 추천 venue: CoRL**

LIBERO·RoboTwin·RoboCasa 세 시뮬레이션 벤치마크와 실로봇 4개 task를 모두 포함하고 representation-level 분석(motion decodability, 주파수별 semantic similarity)까지 갖춰 실험 강도는 CoRL/RSS 수준에 충분함. 다만 방법 자체는 기존 latent action model과 world-action-model pipeline에 모션 분해·주파수 필터링 모듈을 결합한 것이라 conceptual leap은 제한적이라 oral/highlight보다는 regular accept 가능성이 높아 보임.

**추천 이유 & 누리랩 연구와의 연결점**

- egocentric video로 world model/VLA를 pretrain하는 저비용 데이터 전략과 직접 연결됨. Fig5(b)의 pretraining 전략 비교(video-only vs hand-pose vs latent-action-target vs spectral guidance)는 우리 lab world model 학생 연구에서 ego-video 활용 방식을 정할 때 참고할 baseline 세트로 쓸 수 있음.
- 카메라(관찰자) 모션과 상호작용 모션을 point tracking으로 분리하는 방식은 active perception·object-centric representation에서 "관찰자 motion vs 물체 motion" 분리 문제에도 적용 가능함.
- 저주파 latent guidance가 느리게 변하는 task-level 구조만 cross-embodiment로 전이된다는 관찰은, robot memory나 failure detection에서 "빠른 noise"와 "느린 task state"를 분리하는 표현 설계에 응용할 수 있음.

---

### 8. [70점] World Action Modeling with Progressive Visual Planning

- **분야**: World Model / VLA · **robotics relevance**: 9/10
- **arXiv**: [2610.02508](https://arxiv.org/abs/2610.02508) ([PDF](https://arxiv.org/pdf/2610.02508))
- **저자**: Fei Zhang, Zhaochong An, Duncan Frost, Yikai Wang, Pengfei Liu, Ya Zhang, Michal Drozdzal, Amir Bar
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **Comments**: Project Page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 82점

> 💡 ProWAM은 world action model(WAM)이 조건으로 쓰는 미래 시각 정보를 sparse sub-goal 시퀀스로 바꿈. 이 시퀀스는 dense video rollout과 단일 종료 프레임 사이를 절충해, 현재 관측 기준 진행률(progress) r로 인덱싱하고 한 번의 video backbone forward로 캐싱해 action expert에 공급함. LIBERO-Plus·RoboTwin-Random 같은 OOD 벤치마크와 실로봇 4개 task에서 기존 WAM 대비 큰 폭의 성능 향상을 보임.

**Core innovation & methodology**

- 최종 목표 프레임 하나만 예측하는 기존 Image-WAM 방식(final-goal prediction, FGP)을 일반화해서, 현재 관측 기준 상대 진행률 r∈[0,1]로 인덱싱된 k개의 sparse visual sub-goal을 순서대로 예측함
- video expert와 action expert를 mixture-of-transformers(MoT, attention head를 공유하는 구조)로 묶고, action 토큰이 video 쪽에 영향을 못 주게 asymmetric attention mask를 둬서 video backbone의 generative prior를 보존함
- action-free 대규모 비디오로 video expert를 먼저 사전학습(sub-goal 예측 포함)하고, 로봇 시연 데이터로 video-action을 joint fine-tuning하는 2단계 학습을 씀
- 추론 시 sub-goal의 key-value feature를 한 번의 video-expert forward로 캐싱해 재사용하고 action denoising만 반복해서, 매 스텝 video backbone을 다시 돌리는 기존 full-imagination WAM보다 연산을 크게 줄임

**Novelty vs. prior works**

- 가장 가까운 선행연구인 Image-WAM(단일 종료 프레임 조건)과 DreamZero류 full-imagination WAM(dense rollout 조건) 사이의 설계 공간을 메우는 것이 핵심 기여고, 저자 스스로도 FGP를 k=1인 특수 케이스로 명시함
- trajectory 길이와 무관하게 sub-goal을 일관되게 배치하는 진행률 정규화(r=0~1)와, 별도 high-level planner 없이 video backbone 안에서 native하게 sub-goal을 내는 구조는 HALO 등 modular hierarchical VLA 대비 실질적 차이임
- 다만 sparse keyframe/sub-goal로 장기 과제를 구조화한다는 아이디어 자체는 hierarchical diffusion planning 계열의 연장이라, 패러다임 전환보다는 WAM 구조에 이를 자연스럽게 이식한 쪽에 가까움

**Benchmark results**

- LIBERO-Plus(OOD)에서 85.8%로 SOTA 달성, 가장 강한 baseline ABot-M0(80.5%)·Image-WAM(83.1%) 대비 우위를 보임. ID LIBERO는 98.8%로 거의 포화 상태라 변별력이 낮음
- RoboTwin random(OOD)에서 75.7%로, 가장 강한 WAM baseline MV-WAM(55.7%) 대비 +20.0%p 향상. video-only pretrain을 뺀 ProWAM-Base는 67.4%로 떨어져 사전학습이 OOD robustness에 기여함을 보임
- RoboCasa365에서는 overall 48.1%, Composite-Unseen 18.2%로 공개 method 5개 중 4위(abstract·Table 3 기준)인데, 본문 서술은 2위라고 적어 abstract·Table 3의 4위 표기와 어긋남. 표 기준으로는 상위 3개 method(Paimon-0, Xiaomi-Robotics-1, Phasor-m7) 대비 뒤처짐
- 실로봇 DROID 기반 zero-shot 4-task 평가에서 70.0% 성공률로 DreamZero(14B, 55.0%) 대비 +15.0%p(상대 +27.3%) 앞섬. ProWAM 모델 크기는 5B로 DreamZero보다 작음
- ablation에서 KV-cache 방식이 naive joint denoising 대비 FLOPs 84% 절감(115.5→18.7 TFLOPs), latency 46% 절감(581→313ms)하면서 OOD 성공률은 오히려 3.3%p 높았고, sub-goal horizon은 Near([0.1,0.5]) 설정이 Far([0.5,0.9])보다 OOD에서 +7.3%p 우수함

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

실로봇 4-task zero-shot 평가와 3개 sim benchmark에 걸친 광범위한 ablation으로 실험적 근거는 탄탄해 CoRL이나 RSS급 심사를 통과할 만함. 다만 RoboCasa365에서 4위에 그치고 본문과 abstract의 순위 서술이 어긋나는 점, 핵심 아이디어가 Image-WAM의 자연스러운 확장이라는 점은 oral보다는 포스터급 risk로 작용함.

**추천 이유 & 누리랩 연구와의 연결점**

- progress-indexed sub-goal 표현은 failure detection에 바로 쓸 수 있음: 논문 Figure 3처럼 sub-goal의 contact geometry가 흐려지는 패턴을 실패 예측 신호로 삼아 recovery trigger에 연결 가능함
- sub-goal을 2D latent 대신 object-centric 3DGS나 scene graph로 예측하게 바꾸면, 기하학적으로 검증 가능한 중간 목표를 줄 수 있어 누리랩의 object-centric representation 방향과 결합할 여지가 있음
- 매 replanning마다 sub-goal을 재예측하는 구조라, 다른 진행률·경로를 가정해 sub-goal을 다시 그려보는 test-time counterfactual search를 얹는 확장이 가능함

---

### 9. [70점] KungfuAthleteBot: learning high-dynamic humanoid motion from video with unified robust recovery

- **분야**: RL / Humanoid Motion Control · **robotics relevance**: 8/10
- **arXiv**: [2610.03388](https://arxiv.org/abs/2610.03388) ([PDF](https://arxiv.org/pdf/2610.03388))
- **저자**: Zhongxiang Lei, Lulu Cao, Xuyang Wang, Tianyi Qian, Jinyan Liu, Xuesong Li
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 영상에서 복원한 동작 데이터를 로봇이 쓸 수 있게 만드는 문제를 물리적 비일관성·액추에이션 정보 부재·낙상 복구 부재라는 세 가지 결함으로 나누고, 각각을 물리 기반 보정·physics-driven 샘플링·통합 정책으로 해결함. Unitree G1 실로봇에서 쿵푸 동작을 추적하면서 임의의 낙상에서 약 0.7초 만에 복구하는 성능을 보임.

**Core innovation & methodology**

- 영상 기반 동작 복원의 결함을 물리적 비일관성(C1), 액추에이션 정보 부재(C2), 낙상/복구 모델 부재(C3) 세 가지로 분해하고 각각에 전용 해법을 제시함
- 물리 기반 포물선 보정(parabolic correction)으로 공중 동작의 root height floating·지면 관통·고주파 지터를 제거함 — 기존 연구처럼 점프 구간을 버리지 않고 복원함
- pseudo-low-kinetic-energy(LKE) sampling 제안: 정책의 추적 오차가 아니라 레퍼런스 자체의 운동에너지 proxy로 초기 상태 분포를 정함. 오차 기반 적응 샘플링이 실행 불가능한 자세에 계속 재초기화되는 문제를 피함
- 추적·외란 거부·낙상 복구를 단일 정책 안에서 하나의 목적함수로 학습하는 formulation 제시. 복구 전용 레퍼런스 데이터나 수동 모드 전환 없이, shoulder height 편차 기반 indicator로 복구 보상을 켬

**Novelty vs. prior works**

- 가장 가까운 선행연구인 KungfuBot·OmniXtreme은 처리 후 레퍼런스가 학습 가능하다고 가정하고 불가능한 구간을 필터링·마스킹으로 버림. KAB는 가장 역동적인 점프 구간을 버리지 않고 수리와 보정을 동시에 건다는 점에서 차별화됨
- LKE sampling 자체는 새로운 학습 패러다임이라기보다 초기화 분포 설계를 error-driven에서 physics-driven으로 바꾼 것이라 아이디어 비약은 크지 않음. 다만 video-derived reference라는 구체적 세팅에서 이 설계가 필요한 이유는 논증이 분명함
- recovery를 사람 get-up 레퍼런스 없이 tracking과 같은 목적함수·같은 정책으로 학습한 점은 BFM-Zero·Heracles·StableMimic 대비 실질적 차이임. 다만 tracking과 recovery를 한 정책에 통합한다는 틀 자체는 이 선행연구들에서 이미 시도된 방향이라 완전히 새로운 문제 설정은 아님

**Benchmark results**

- 7개 고난도 동작에서 기존 teleoperation 시스템(TWIST, GMT, SONIC) 대비 mean per-joint position error(논문 표기 E_mpjpe, 단위 10^-3 rad)가 현저히 낮음. Motion 78 기준 KAB 24.7±12.1 vs SONIC 71.9±17.2, TWIST 85.2±23.8, GMT 68.3±17.3, success rate는 6/6으로 전부 성공한 반면 TWIST·GMT는 전 동작에서 0/6
- 3단계 커리큘럼 vs single-stage BeyondMimic 베이스라인 비교에서 Motion 468(360도 측면 플립) 기준 reward가 54.6 vs 7.8로, single-stage는 조기 종료로 local optimum에 갇힘
- 낙상 복구 시간 0.692±0.136초로 비교 대상 중 가장 빠름 — HumanUP 6.708초, HoST 2.055초, FIRM 1.729초, BFM-Zero 1.566초, Heracles 2.471초이며, StableMimic은 코드·모델 비공개로 시간 자체를 보고하지 않음
- ablation: recovery reward를 추가해도 tracking-only 대비 episode length·오차는 거의 그대로 유지되나 수렴은 느려짐(~16k vs ~2.5k iteration). height reward 제거 시 tracking은 부분적으로 되지만 복구는 실패하고, root-orientation reward 제거 시 ~5k iteration에서 학습이 붕괴함
- 실로봇(Unitree G1) 검증은 낙상 4종(prone/supine/lateral/twisted)과 5분짜리 Tai Chi 장시간 시퀀스에서 수행됨. 다만 정량 비교(Table 5)의 baseline은 teleoperation 계열이고, 가장 직접적 경쟁자인 KungfuBot·BeyondMimic·OmniXtreme과는 정량 벤치마크가 아니라 정성적 positioning으로만 비교함

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

실로봇 검증, 구체적 수치 비교, 각 구성요소를 끄고 확인한 ablation이 갖춰져 있어 CoRL/ICRA 수준의 실험적 설득력은 있음. 다만 포물선 보정·physics-driven sampling·통합 recovery 각각이 기존 아이디어의 조합에 가깝고 핵심 경쟁자(KungfuBot, OmniXtreme, BeyondMimic)와의 정량 비교가 빠져 있어 oral·highlight보다는 regular accept 수준으로 판단함.

**추천 이유 & 누리랩 연구와의 연결점**

- tracking 정책 안에 recovery를 같은 목적함수로 묶는 formulation은 manipulation에서 파지 실패·충돌 후 복구를 다루는 failure detection/recovery 정책 설계에 참고할 만함
- 레퍼런스 신뢰도가 낮은 구간을 버리지 않고 물리 기반으로 수리한다는 아이디어는, VLA 학습에서 noisy demonstration이나 web video를 다룰 때 필터링 대신 보정을 택하는 선택지로 확장 가능함
- 오차가 아니라 물리량(에너지) 기반으로 학습 샘플링을 설계하는 LKE 방식은 world model 기반 test-time planning에서 롤아웃 초기화 전략에 응용해볼 수 있음

---

### 10. [70점] Multi-Fidelity Policy Gradients Stabilize Data-Scarce Reinforcement Learning

- **분야**: RL · **robotics relevance**: 8/10
- **arXiv**: [2610.02505](https://arxiv.org/abs/2610.02505) ([PDF](https://arxiv.org/pdf/2610.02505))
- **저자**: Xinjie Liu, Ruihan Zhao, Anirban Chaudhuri, Cyrus Neary, Ufuk Topcu, David Fridovich-Keil
- **카테고리**: Machine Learning (cs.LG) · 신규 목록 게재: cs.LG
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 비싼 고정밀(high-fidelity, HF) 로봇 데이터가 적을 때 저렴한 저정밀(low-fidelity, LF) 시뮬레이터 데이터를 policy gradient의 control variate로만 써서 분산을 줄이는 MFPG-PPO를 제안함. LF 데이터로 목적함수를 직접 최적화하지 않아 LF 편향에 강하고, Isaac Lab locomotion과 업데이트당 4 에피소드만 쓰는 실제 Franka 로봇 실험에서 PPO HF-only 대비 거의 모든 세팅에서 더 좋거나 같은 성능을 보임.

**Core innovation & methodology**

- REINFORCE 기반이던 기존 MFPG(Liu et al., TMLR 2026) control variate 프레임워크를 PPO/actor-critic으로 확장하면서, 짧은 rollout·desynchronized parallel env·서로 다른 dynamics 때문에 cross-fidelity correlation이 깨지는 문제를 분석함
- coupled LF rollout을 HF rollout 시작 상태로 주기적으로 재동기화하고 action noise를 공유하며, coupled/uncoupled LF critic을 분리하고 GAE horizon을 HF와 맞춰 correlation을 보존함
- coefficient c를 매 minibatch마다 재적합하고 bootstrap confidence interval로 correlation이 0과 구별되는지, 분산이 실제로 줄었는지 모니터링해서 증거가 부족하면 c=0으로 HF-only PPO로 fallback함
- 샘플 비용이 다를 때 MFMC(multi-fidelity Monte Carlo) 할당 이론을 기반으로 HF/LF 샘플 수를 매 iteration 온라인으로 재분배하는 budget-aware 버전(MFPG-PPO-BA)을 제시함

**Novelty vs. prior works**

- 핵심 이론(LF 데이터를 control variate로 써서 unbiased하게 분산만 줄인다는 아이디어)은 이 논문 것이 아니라 Liu et al. 2026(TMLR)의 REINFORCE 기반 MFPG 프레임워크에서 가져온 것임
- 저자들 스스로 PPO로 단순 치환한 초기 preprint(Liu et al. 2025)가 REINFORCE보다 나을 게 없었다고 밝힘 — 이번 논문의 기여는 그 실패를 고치는 엔지니어링(재동기화, 분리된 critic, 모니터링)이지 새로운 learning paradigm은 아님
- 다만 GPU-parallel actor-critic으로의 확장과 실제 로봇 검증은 이 분야 최초이고, naive 확장이 분산을 1000배까지 키운다는 걸 ablation으로 보여준 것은 실질적 기여임

**Benchmark results**

- H1 Rough(가장 어려운 task)에서 HF budget 1/256일 때 PPO HF-only는 거의 0으로 붕괴하지만 MFPG-PPO-FR은 평균 return 약 40을 유지하고, 가장 작은 3개 budget 전부에서 HF 16배 더 쓴 PPO HF-only와 동등한 성능을 보임
- 4개 task(H1/ANYmal-D × Rough/Flat) × HF budget 1/64~1/8의 16개 조합 중 MFPG-PPO-FR은 14개에서 PPO HF-only를 능가하고 나머지 2개도 더 나쁘지 않음, MFPG-PPO-BA(cost ratio w_high/w_low=10 가정)는 16개 전부에서 능가함
- 실제 Franka cube-picking에서 업데이트당 4 에피소드만으로 MFPG-PPO-FR은 성공률 91.7%(seed별 90~95%)로, PPO HF-only 55.0%(seed별 30~70%)를 모든 seed에서 앞섬. sim-only warm-start 정책은 40.0%
- ablation(1/8×, 1/32× 두 budget만 비교)에서 coefficient 재적합과 모니터링을 둘 다 빼면 1/8× budget에서 학습이 붕괴하고, 이 둘이 없으면 variance ratio가 1000배 넘게 커지는 iteration이 다수 발생함
- LF-to-HF transfer가 쉬운 ANYmal-D에서는 DARC·Co-training 같은 LF를 직접 최적화에 쓰는 baseline이 오히려 더 큰 이득을 봄 — MFPG-PPO는 절대 손해 안 보는 reliability를 사는 대신 쉬운 세팅에서의 최대 이득은 포기하는 trade-off가 있음

**Top-tier conference 적합성 — 65/100 · 추천 venue: CoRL**

실제 로봇 실험, 4개 시뮬레이션 task 전반의 체계적 비교, bias-variance trade-off에 대한 이론적 분석(Lemma 포함)까지 갖춰 CoRL/ICRA 수준의 설득력은 있음. 다만 핵심 control variate 이론은 선행 TMLR 논문에서 가져온 것이고 실로봇 task가 cube picking 1개·3 seed뿐이라 oral/highlight급 novelty로 보기는 어려움.

**추천 이유 & 누리랩 연구와의 연결점**

- 누리랩의 real robot RL/IL 실험에서 데이터 수집 비용 문제에 바로 적용 가능 — VLA나 manipulation policy를 소량 real rollout과 풍부한 sim rollout으로 안정적으로 학습시키는 데 control variate 아이디어를 가져올 수 있음
- coefficient를 증거(correlation 유의성·분산 감소 확인)가 있을 때만 적용하고 아니면 fallback하는 monitoring 설계는, test-time optimization에서 world model 예측의 신뢰도를 판단해 개입 여부를 정하는 메커니즘에 참고할 만함
- failure detection/recovery, object-centric 3DGS, scene graph 등 누리랩 다른 주제와의 직접적 연결점은 약함 — 이 논문은 policy gradient 추정 안정화에만 집중함

---

### 11. [68점] CriticHack: Evaluating Visual Rewards Under Robot Policy Optimization

- **분야**: RL / Reward Model Evaluation (Manipulation) · **robotics relevance**: 8/10
- **arXiv**: [2610.02527](https://arxiv.org/abs/2610.02527) ([PDF](https://arxiv.org/pdf/2610.02527))
- **저자**: Jiaxuan Luo, Xingguo Xu, Shanshan Wang, Yuhan Zhou, Zhen Zhang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 60 pages
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 학습된 visual reward(Robometer)로 diffusion policy를 fine-tuning하면 task success와 wrong-object failure(엉뚱한 물체를 조작해 실패하는 유형)가 함께 늘어남을 보임. reward와 success 두 지표만 보면 건강해 보이는 착시가 생기는데, KL-regularized 최적화의 tilt 모델로 이 현상이 언제 나타나는지 예측하고 frozen success verifier로 reward를 보정하면 바로잡을 수 있음을 확인함.

**Core innovation & methodology**

- reward 상승·task success 상승·wrong-object failure 상승이 동시에 일어나는 상황(coexistence regime)을 simulator state 기반 독립 라벨(success/wrong-object failure/other failure)로 분리해서 정량적으로 드러냄.
- Robometer reward로 diffusion policy 전체 denoiser(251.7M parameter)를 PPO로 fine-tuning한 5회 학습에서 success와 wrong-object failure가 함께 오르는 반면, 같은 세팅에서 simulator ground-truth completion reward로 학습하면 wrong-object failure는 거의 안 늚을 대조로 보임.
- KL-regularized 최적화에서 최적 정책이 초기 정책의 exponential tilt(π_β ∝ π_0 · e^{r/β})가 된다는 기존 결과를 이용해, "초기 정책 기준 평균 reward가 population 평균보다 높은 outcome이 더 자주 나온다"는 예측 모델을 세움.
- frozen task-specific success verifier로 critic reward를 곱해서 보정(critic×verifier)하는 진단적 개입(diagnostic intervention)을 제시하고, verifier만 단독으로 써도 같은 효과가 남을 확인함.

**Novelty vs. prior works**

- 가장 가까운 선행연구 Liang et al. 2026(Robometer/RoboReward)은 wrong-object false positive가 online RL에서 잘못된 행동을 강화한다는 걸 보였는데, 이 논문은 그 현상이 success rate 상승과 동시에 일어나서 practitioner가 보는 두 지표(reward, task success)로는 못 잡힌다는 점을 추가로 규명함. 현상의 발견보다 "왜 표준 모니터링이 못 잡는가"를 규명한 쪽이 기여임.
- tilt model 자체(KL-regularized 최적화가 reference policy의 exponential tilt라는 결과)는 Korbak et al. 2022, Rafailov et al. 2023의 기존 결과를 가져온 것이고, 저자의 기여는 이를 success/wrong-object/other 세 outcome 단위의 예측 도구로 재구성해 26개 세팅에서 검증한 것임. 이론적으로는 새 paradigm이 아니라 기존 결과의 응용에 가까움.
- reward overoptimization과 hidden stratification 개념은 LLM·diffusion alignment 쪽에 이미 있던 것으로, 로봇 visual reward에 체계적으로 처음 적용했다는 점이 novelty임. 방법론 기여보다 진단(diagnosis) 기여가 핵심이라 novelty 수준은 제한적임.

**Benchmark results**

- supervised initialization에서 Robometer로 5회 학습: success +10.2pp[6.9,13.6], wrong-object failure +10.9pp[7.3,14.4] (512 evaluation seed). 동일 세팅 ground-truth completion reward 5회 학습은 success +13.9pp, wrong-object +1.6pp[-1.9,5.2] — 두 reward 차이 9.2pp[5.6,13.0], 순열검정 p=.008(8회 반복 시 p=.0002).
- warm-start 정책에서도 critic-only 학습은 success +8.4pp, wrong-object +3.8pp가 함께 상승. critic×verifier(Product)는 success +15.5pp, wrong-object -0.6pp[-3.4,2.1]로, critic-only 대비 success +7.1pp, wrong-object -4.4pp[-7.1,-1.8] 개선.
- Robometer는 전체 success/failure 구분 AUROC 0.813로 양호하지만 wrong-object failure 대 success AUROC 0.372(평균 점수 success 0.65, wrong-object 0.70)로 순위가 역전됨. other failure가 negative의 75%를 차지하고 그쪽만 거의 완벽히 분리(AUROC 0.959)해서 aggregate 지표가 역전을 가림.
- constrained noise-selector 26개 세팅(drawer/stacking × Robometer/LIV × PPO/GRPO)에서 tilt 모델 예측과 측정치 Spearman ρ=0.89(wrong-object), 0.79(success). drawer Robometer GRPO에서는 success -12.5pp, wrong-object +71.9pp로 고전적 overoptimization 패턴도 같은 모델로 재현함.
- real robot(Franka Research 3, 정책당 40 trial) case study: critic-trained 정책은 wrong-object failure가 22.5%→37.5%로 늘고 success는 30.0%→25.0%로 시뮬레이션과 반대 방향(n=40이라 통계적으로 미확정). completion-trained 정책은 success 30.0%→40.0%, wrong-object 22.5%→17.5%로 시뮬레이션과 일치함.

**Top-tier conference 적합성 — 70/100 · 추천 venue: RSS**

독립 학습 run을 다수 확보하고 bootstrap CI를 꼼꼼히 보고했으며, closed-form tilt 모델을 26개 세팅에서 교차검증하고 real-robot case study까지 갖춰 RSS 수준의 실험적 증거는 확보함. 다만 시뮬레이션 과제가 drawer·stacking 두 개뿐이고 real-robot은 조건당 학습 1회의 case study 수준이라, 일반화 범위에 대한 지적이 rejection 사유로 나올 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- failure detection/recovery: wrong-object failure는 겉보기에 그럴듯한 조작인데 엉뚱한 물체를 다루는 실패 유형이라, reward·success 신호만으로는 못 잡는 실패 카테고리로 누리랩 failure diagnosis 연구에 바로 활용 가능함.
- VLA RL fine-tuning: learned visual reward로 VLA를 RL fine-tuning할 때, 이 논문의 tilt 진단(초기 정책 기준 outcome별 평균 reward가 population 평균보다 높은지 사전 점검)을 학습 전 체크리스트로 쓸 수 있음.
- frozen outcome verifier로 training-time reward를 보정하는 구조는 test-time optimization에서 verifier 기반 reranking으로 확장할 수 있고, 같은 초기 상태에서 outcome별 reward 분포를 비교하는 방식은 counterfactual reasoning 연구와도 연결됨.

---

### 12. [60점] Imagine the Future, Internalize the Gist: Efficient VLA Reasoning via Internalized Spatiotemporal Imagination

- **분야**: VLA · **robotics relevance**: 8/10
- **arXiv**: [2610.02626](https://arxiv.org/abs/2610.02626) ([PDF](https://arxiv.org/pdf/2610.02626))
- **저자**: Shenglan Li, Zhendong Mi, Hengyi Zhu, Jingwu Luo, Chun Kit Chan, Geng Yuan, Yanzhi Wang, Pu Zhao 외 1명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 IG-VLA는 미래 장면 변화를 pixel-level video 생성 없이 visual latent space에서 직접 예측해서 action 생성을 돕는 VLA reasoning framework임. 이 reasoning 과정을 Scene Gist Token 하나로 압축해 추론 시 future rollout 없이도 거의 같은 성공률을 169.5ms 만에 낼 수 있음을 보임.

**Core innovation & methodology**

- future scene 변화를 pixel-level video 생성 없이 visual representation space에서 직접 예측하는 Latent Spatiotemporal Reasoning 모듈을 제안함. SigLIP latent에서 미래 K=10 step의 visual transition(미래-현재 차분)을 예측함
- 예측한 미래 latent를 현재 multimodal context와 결합해 action을 생성하는 reasoning policy를 둬서, action prediction이 anticipated future dynamics에 조건화되게 함
- reasoning policy가 만든 reasoning-enhanced representation을 단일 Scene Gist Token으로 압축하는 gist compressor를 두고, 현재 관측만으로 이 gist를 예측하는 gist encoder를 따로 학습시켜 추론 시 future rollout을 생략하게 함. 2단계 학습임 — reasoning policy를 먼저 학습해 freeze한 뒤 gist 모듈을 학습함
- gist encoder는 representation alignment loss와 action consistency loss로 학습해서, reasoning policy가 내는 action을 그대로 재현하도록 behavioral knowledge를 distillation함

**Novelty vs. prior works**

- latent space에서 미래를 예측해 action을 guide한다는 아이디어는 CoT-VLA(visual subgoal), WorldVLA·DreamVLA(world model 기반 VLA)와 문제의식이 같고, "추론을 압축해서 inference 때 생략한다"는 방향도 저자가 직접 baseline으로 비교한 Fast-WAM·ImageWAM(둘 다 2026년 상반기 공개, "test-time future imagination이 정말 필요한가"를 똑같이 묻는 논문)이 이미 다루고 있음
- IG-VLA의 차별점은 미래를 image/video feature가 아니라 visual transition으로 예측하고, 이를 action-matching distillation(2-loss, 2단계 학습)으로 단일 token에 압축하는 구조임. 다만 이게 Fast-WAM/ImageWAM의 feature caching 방식과 본질적으로 다른 paradigm인지, 아니면 distillation 방식만 바꾼 변형인지는 본문만으로 명확히 구분되지 않음
- 따라서 novelty는 "future reasoning을 하나의 token으로 internalize한다"는 concept 자체보다 구현 디테일(transition 예측 + action-consistency distillation)에 있다고 보임. formulation 신규성은 제한적임

**Benchmark results**

- LIBERO 평균 성공률 98.9%로 가장 강한 baseline ACoT-VLA(98.5%)보다 0.4%p 높음. reasoning policy와 gist policy가 동일하게 98.9%를 기록해 gist 압축으로 인한 성능 손실이 없음을 보임
- LIBERO-Plus(robustness benchmark) 평균은 88.5% vs ACoT-VLA 88.0%로 차이가 작지만, language variation suite에서는 85.6% vs 79.7%로 5.9%p 개선함(논문 표현으로는 "nearly 6%")
- VLABench에서는 평균 Intention Score 66.68로 ACoT-VLA(63.5)보다 3.18점 높지만, 평균 Progress Score는 46.11로 ACoT-VLA(47.40)보다 오히려 낮음 — 저자도 이 부분은 인정함
- 추론 속도는 gist policy 기준 action chunk당 169.5ms로 FastWAM-IDM(1,081ms) 대비 6.38배, ImageWAM(263ms) 대비 1.55배 빠름. GPU 시간 분해 분석에서 gist predictor 자체의 추가 연산은 0.13ms에 불과함
- ablation에서 미래 keyframe 수 K=10이 최적이고 K=15에서는 97.8%로 저하됨(예측 오차 누적 추정). directional loss 가중치 λdir=0.1을 벗어나 0.5 이상으로 키우면 성공률이 37.0%까지 급락함 — 학습이 hyperparameter에 민감함을 시사함
- 실로봇 검증은 dual-arm UR3 pick-and-place 과제 1개, 방법당 16회 시행으로 IG-VLA 62.5%, π0.5 56.2%, ACoT-VLA 50.0%를 기록함. task 1개·trial 16회로 샘플이 작아 일반화 근거로는 약함

**Top-tier conference 적합성 — 55/100 · 추천 venue: CVPR**

LIBERO·LIBERO-Plus·VLABench 세 benchmark에서 일관된 개선과 real robot 검증까지 갖춰 CVPR/ICCV/CoRL급 투고에 필요한 실험량은 충족함. 다만 핵심 문제의식이 같은 해 공개된 Fast-WAM·ImageWAM·ACoT-VLA와 상당히 겹치고 LIBERO 개선폭도 0.4%p 수준으로 작아, oral/highlight급 conceptual leap으로 보기는 어려움.

**추천 이유 & 누리랩 연구와의 연결점**

- latent future prediction 구조 자체를 failure detection/recovery나 test-time optimization에 재사용할 수 있음 — 예측한 미래 latent와 실제 관측의 차이를 failure signal로 쓰는 방향으로 확장 가능함
- Scene Gist Token처럼 reasoning 결과를 하나의 token으로 압축하는 distillation 기법은 robot memory(장기 경험을 compact representation으로 누적)나 scene graph 기반 semantic memory 연구에 참고할 만함
- 지금 IG-VLA는 미래를 하나만 예측하고 다른 action을 선택했을 때의 결과는 비교하지 않음. 이 구조에 counterfactual reasoning(여러 action에 대한 latent future를 비교)을 더하면 world model과 결합한 새로운 formulation으로 발전시킬 여지가 있음

---

### 13. [58점] Keeping JEPA World Models Plannable When Little of the Frame Moves

- **분야**: World Model · **robotics relevance**: 9/10
- **arXiv**: [2610.03137](https://arxiv.org/abs/2610.03137) ([PDF](https://arxiv.org/pdf/2610.03137))
- **저자**: Florian Strohm, Patrick Wagner, Jannik Schwab, Marco Huber
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 JEPA 기반 world model LeWM이 멀티오브젝트 pushing 벤치마크 SLIM에서 1% 미만 성공률로 실패하는 이유가 encoder latent가 action에 거의 반응하지 않는 collapse임을 probe로 밝힘. encoder latent와 predicted latent 둘 다에 거는 inverse-dynamics 보조 손실 하나로 성공률을 0.3%에서 35%로 올리고, 복구된 latent 위에 얹은 작은 language-goal head로 문장만으로 계획을 세울 수 있음을 보임(단, pushing은 단일 문장 성공률이 낮고 단계별 문장일 때만 oracle 수준에 도달함).

**Core innovation & methodology**

- SLIM이라는 새 benchmark를 제시함: 작은 object 여러 개와 동일 장면에 대한 visual goal·language goal을 짝지은 멀티오브젝트 pushing task이며, PushT와 같은 연산량대에서 pusher가 object를 거의 못 건드려 frame의 0.37%만 바뀌는 체제를 만들어냄.
- 네 가지 probe(action sensitivity, rollout error, position decodability, cost landscape)로 LeWM encoder의 latent collapse를 진단함: action에 거의 무반응이고(spread/motion 3.8e-4), pusher·object 위치를 전혀 디코딩 못 하고, rollout이 현재 latent를 그대로 복사하는 수준이며, cost landscape probe에서도 planning에 쓸 만한 뚜렷한 최솟값이 나타나지 않음.
- 수정법은 encoder latent 쌍과 predicted latent 쌍 양쪽에 공유 inverse-dynamics head(IDM)로 action을 예측시키는 보조 손실이며, 이 head는 테스트 시 버림. ablation으로 encoder 쪽 gradient가 개선분의 약 85%를 차지하고 predictor 쪽은 보조적임을 확인함.
- world model은 그대로 두고 frozen encoder 위에 작은 language-goal head(cross-attention, 1.1M parameter)만 추가해 문장에서 goal latent를 뽑아 CEM planner에 넣음. 단일 문장만으로는 pushing이 약하지만 push를 단계별 문장으로 쪼개 주면 goal-frame oracle 수준까지 올라감.

**Novelty vs. prior works**

- IDM 보조 손실 자체는 신규성이 제한적임. 저자들이 본문 Concurrent work 절에서 DA-LeWM, ATM, SMWM, Delta-JEPA, AC-MTM 등 2026년 동시 발표 논문 다수가 거의 같은 아이디어(encoder latent에 inverse-dynamics loss)를 LeWM류 모델에 쓴다고 직접 밝힘.
- 차별점은 '얼마나 적게 움직여야 collapse가 나는가'를 SLIM이라는 통제된 벤치마크로 분리해 측정한 것과, shuffled-action null·frozen-encoder cap·encoder-vs-predictor disentangle 같은 control로 gradient 기여를 분리한 것임. 동시 발표 논문들은 이런 메커니즘 분석이나 language goal을 다루지 않는다는 것은 저자 주장이고 본 리뷰에서 교차검증은 못 함.
- language-goal head는 world model 재학습 없이 frozen latent 위에 얹는다는 점에서 LAGO(Barbeau et al., 2026)와 가장 가까우며, paraphrase·unseen noun 평가를 추가한 점이 차이지만 head 구조 자체(cross-attention MLP)는 architecture적으로 새롭지 않음.

**Benchmark results**

- SLIM에서 LeWM(plain) 성공률 0.3% 대비 LeWM+I 34.8±1.6% (hard tier 15.7%, very hard는 둘 다 0%); 같은 world model이 PushT에서는 98% 성공해 벤치마크 난이도 차이를 보여줌.
- ablation에서 encoder-IDM만 적용 시 29.8%(전체 개선분의 약 85%), predictor-IDM만 적용 시 1.0%(plain과 통계적으로 무차별, McNemar p=0.13), shuffled-action null 0.3%(=plain 수준)으로 encoder gradient가 핵심임을 확인함.
- action-sensitivity probe(spread/motion)는 필요조건이지 충분조건은 아님. 학습한 28개 설정 중 임계값 0.05 이하는 전부 실패했고, 그 위에서는 성공률이 1~83%로 편차가 큼.
- language-goal head는 navigation에서 oracle 100% 대비 84%, decoy 테스트 300/300에서 decoy에 속지 않았고, train-pool paraphrase에서 성공률의 92%, unseen noun paraphrase에서 84%를 유지함.
- 단일 goal sentence로는 pushing 성공률이 medium 6%/hard 4%에 그치지만(oracle 30%/17%), push를 3단계 문장으로 나눠 주면 medium/hard가 25%로 올라 goal-frame oracle(27%/16%) 수준에 도달하며, 이는 simulator 없이 latent 거리만으로 stage를 전환해도 동일하게 재현됨.

**Top-tier conference 적합성 — 55/100 · 추천 venue: ICLR**

probe 4종·McNemar 검정·3 seed·다양한 ablation(loss weight sweep, response-to-actions sweep)을 갖춘 메커니즘 분석은 top-tier 급 실험적 conviction을 보임. 다만 전부 2D pymunk toy 시뮬레이션이고 real-robot 검증이 전혀 없으며, 핵심 아이디어인 IDM 보조 손실이 2026년 동시 출간 논문 여럿과 겹쳐 리뷰어가 novelty 약점으로 지적할 위험이 큼.

**추천 이유 & 누리랩 연구와의 연결점**

- world model latent collapse를 action-sensitivity probe로 진단하는 방식은 failure detection/diagnosis 연구에 바로 쓸 수 있음. plan을 돌리기 전에 latent가 action에 반응하는지 체크하는 test-time gate로 활용 가능함.
- language-goal head를 world model 재학습 없이 frozen latent 위에 얹는 구조는 VLA의 test-time optimization/inference-time planning 방향과 바로 연결됨. 우리 world model에도 같은 방식으로 언어 목표 조건부 planning을 추가해볼 수 있음.
- staged instruction(단계별 문장)으로 push를 쪼개 success를 끌어올린 결과는 skill chaining·long-horizon planning에 참고할 만함. 다만 unseen vocabulary에서는 staged 이득이 거의 사라져 robot memory·언어 feedback 쪽으로 확장하려면 추가 보완이 필요함.

---

### 14. [57점] MobiAgent: Dual-Loop Recursive Policy Self-Improvement for Long-Horizon Mobile Manipulation

- **분야**: VLA / long-horizon mobile manipulation agentic framework · **robotics relevance**: 9/10
- **arXiv**: [2610.03476](https://arxiv.org/abs/2610.03476) ([PDF](https://arxiv.org/pdf/2610.03476))
- **저자**: Chenzhi Liu, Yue Zhang, Jiehong Lin, Jianan Wang, Bo Wang, Zhongrui Wang, Xiaojuan Qi
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Accepted at the Conference on Robot Learning (CoRL) 2026. Project page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 MobiAgent는 atomic skill을 매 스텝 재조합하는 VLM 플래너, 공유 VLM backbone에 skill별 flow-matching expert를 쓰는 실행기, 실패 시 전체 계획을 다시 짜는 critic으로 이뤄진 dual-loop 에이전트임. 배포 중 쌓인 rollout을 사람 라벨 없이 VLM·LLM으로 segment·verify·clustering해 skill 정책을 재학습시키는 outer loop를 둠. BEHAVIOR-1K에서 task 전용 baseline 대비 22.5%p, 실로봇에서 32.5%→57.5%까지 성능이 오름.

**Core innovation & methodology**

- Inner Loop의 Task Planner는 고정된 sub-task 리스트가 아니라 atomic skill을 receding-horizon으로 매 스텝 재생성·조합해 open-ended planning을 함
- Skill Executor는 π0.5 VLM backbone은 공유하고 skill별 flow-matching action expert를 따로 둬서, capacity interference를 줄이면서 동일 skill(pick 등)을 여러 task에서 재사용함
- Reflection Critic이 매 C개 action chunk마다 관찰 윈도우를 보고 complete/incomplete/error와 next/retry/replan을 함께 판정해 local retry와 global replanning을 분리함
- Outer Loop는 VLM이 rollout을 segment·caption하고 verify한 뒤 LLM이 instruction을 clustering해 atomic skill vocabulary를 만들고, 이 데이터로 skill 정책을 사람 라벨 없이 지속 fine-tuning함

**Novelty vs. prior works**

- plan-execute-verify 계층형 에이전트 자체는 ReAct, VoxPoser, Hi-Robot, RoboClaw 라인의 연장이고, 차별점은 sub-task를 고정 정책에 매핑하지 않고 atomic skill 조합으로 바꾸면서 그 skill들이 하나의 VLM backbone을 공유하는 flow-matching expert라는 점임
- Outer Loop의 VLM 기반 segment-verify-cluster-finetune 파이프라인은 RoboClaw의 자동 데이터 수집을 한 단계 더 밀어 skill vocabulary 자체를 재귀적으로 갱신하는 것인데, 구성요소 각각(VLM captioning, LLM clustering, behavior cloning)은 기존 기법의 조합임
- 두 루프를 묶어 배포→학습→배포를 닫는 recursive self-improvement 프레이밍은 시스템 레벨에서 정리된 기여이지만, representation이나 학습 알고리즘 자체에 새로운 원리를 제시하지는 않아 engineering integration에 가까움

**Benchmark results**

- BEHAVIOR-1K 4개 task 평균 성공률 65.0%로, task별 전용 모델을 쓰는 π0.5-TA(2025 BEHAVIOR Challenge 우승, 42.5%) 대비 +22.5%p, 가장 긴 fetch-beer에서는 +50%p임
- RoboCasa Composite-Seen에서 baseline π0.5 7.50%, CaP-X 5.00% 대비, outer loop 반복 후 R1 18.75%에서 R3 27.50%까지 오르지만 R4~R6는 25.00~27.50%로 saturate함
- 실로봇(Astribot S1) 4개 task·trial 10회 기준, π0.5 10.0% → MobiAgent bootstrap 32.5% → R2 40.0% → R3 57.5%로, round당 약 20개 rollout만 자동 큐레이션해 사람 라벨 없이 개선됨
- Ablation에서 Reflection Critic 제거 시 65.0%→10.0%로 가장 크게 떨어지고, skill-specific expert를 단일 action head로 바꾸면 65.0%→42.5%, planner를 고정 sub-task로 바꾸면 65.0%→20.0%, global replanning 제거 시 65.0%→40.0%임
- BEHAVIOR-1K는 task 4개·trial 10회, 실로봇도 task 4개·trial 10회 규모라 표본이 작고, RoboCasa 포함 sim 2종 + real 4 task 수준의 검증임

**Top-tier conference 적합성 — 60/100 · 추천 venue: CoRL**

RoboCasa·BEHAVIOR-1K 두 sim benchmark와 real-world(Astribot S1) 평가, component ablation, 실패 모드 분석까지 갖춘 systems paper로 CoRL에는 적합함. 다만 Planner·Critic·Data Curator·Skill Generator 전부가 GPT-5.4·Gemini-3.1-Pro 같은 비공개 프런티어 모델에 의존해 재현성이 낮고, real-robot trial이 task당 10회로 적어 oral/highlight급으로 보기엔 증거가 다소 약함.

**추천 이유 & 누리랩 연구와의 연결점**

- Reflection Critic의 complete/incomplete/error 판정과 local retry·global replan 분리는 누리랩의 failure detection·recovery 연구에 설계 참고가 됨
- episodic memory에 critic의 공간적 단서를 누적해 replanning에 쓰는 구조는 test-time에 축적되는 robot memory 활용 사례로 볼 수 있음
- 논문 스스로 limitation에서 explicit geometric perception(object pose estimation, monocular geometry) 부재를 인정하므로, object-centric 3DGS나 scene graph를 critic·executor에 결합하는 후속 연구로 이어질 수 있음

---

### 15. [47점] SocialVLA: A Social Perception Gateway for Human-Reaction-Based Failure Detection and Recovery in VLA Manipulation

- **분야**: VLA Failure Detection & Recovery (Human-Robot Interaction) · **robotics relevance**: 9/10
- **arXiv**: [2610.02360](https://arxiv.org/abs/2610.02360) ([PDF](https://arxiv.org/pdf/2610.02360))
- **저자**: Sofya Konstantinova, Miguel Altamirano Cabrera, Artem Lykov, Dzmitry Tsetserukou
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 VLA 조작 실패를 로봇 내부 신호가 아니라 옆에서 지켜보는 사람의 음성·표정·명시적 stop phrase 반응으로 감지해 실행을 멈추는 외부 게이트 SocialVLA를 제안함. Unitree G1 실로봇에서 16명 참가자로 평가했고, 고정(frozen) 시스템 기준 recall 54.6%·precision 69.5%, 미지 참가자 1명 대상 prospective 평가에서는 recall 59.5%·precision 91.7%를 달성함.

**Core innovation & methodology**

- 사람의 음성·표정·명시적 stop phrase 반응을 VLA 실행 중 runtime intervention 신호로 바꾸는 policy-agnostic 외부 게이트를 제안함 — VLA 내부 activation이나 uncertainty 접근 불필요함
- causal fast/extended-context 음성 감지, visual reaction, 명시적 stop phrase(Vosk), robot-relevance 추정을 별도 채널로 두고 asynchronous first-event fusion으로 결합함 — 가장 먼저 확신이 임계값을 넘는 신호가 즉시 VLA hold를 요청함
- robot relevance는 별도 video-only logistic head로 추정해 reaction confidence를 최대 30%만 깎는 contextual cue로만 씀(hard veto 아님). 명시적 stop phrase는 0.85 floor를 둬서 relevance가 불확실해도 항상 threshold를 넘게 설계함
- hold 이후 별도 Vosk 로깅 세션이 verbal correction을 기록해 participant가 이어서 재개·재시작·새 instruction 지시를 할 수 있게 함 — 이 기록을 향후 failure-aware policy learning supervision으로 쓸 수 있다고 제안함

**Novelty vs. prior works**

- 가장 가까운 선행연구는 Stiber et al.(얼굴·음성·명시적 피드백·robot-error context를 결합한 proactive 시스템, arXiv:2501.05723)임. SocialVLA는 VLA 내부 접근 없이 외부 게이트로 붙음. reaction recognition과 robot-relevance를 분리 학습해 cross-modal label leakage를 막고, first-event async fusion으로 멀티모달 합의를 기다리지 않는다는 점도 다름
- SAFE·FAIL-Detect·AHA 같은 VLA 내부 기반 실패탐지와는 정보원 자체가 다른 상호보완 관계고, 저자도 직접 경쟁이 아니라 상호보완 관계라고 명시함
- 분류기 자체는 ExtraTrees 같은 고전적 shallow classifier와 기존 pretrained 모델(wav2vec2 기반 Aniemore, MobileFaceNet, YuNet, Vosk)의 조합이라 알고리즘 novelty는 낮음. novelty는 주로 problem formulation(인간 반응을 VLA의 runtime gate로 쓴다)과 fusion/relevance 분리 아키텍처에 있음

**Benchmark results**

- Unitree G1 + GR00T policy, ball pick-and-place 단일 task, 15명 참가자 238개 intervention episode + 1.038h non-intervention 데이터로 offline replay한 결과 frozen cascade recall 54.6%, precision 69.5%, 500ms 이내 timely recall은 45.4%에 그침
- ablation에서 audio-fast 단독 recall 48.3%, video 단독 22.3%, audio+video fusion은 recall 64.3%(+16.0%p)로 올리지만 false stop이 100건 발생함. relevance 모듈 추가로 false stop 100→57(43%감소), precision 60.5%→69.8%, FPR 41.1%→27.8%로 개선되나 true positive도 153→132로 일부 손실됨
- 16번째 unseen 참가자 대상 prospective 배포에서는 recall 59.5%, precision 91.7%, non-intervention FPR 9.5%, false stops/h 20.9를 기록함 — 다만 단 1명 세션 기준이라 표본이 매우 작음
- latency는 detector→fusion 중앙값 47.9ms, VLA gate→physical hold 336ms, reaction onset→physical hold 중앙값 1.021s(매칭 이벤트 n=14)로, 지연 대부분이 detector emission 이전(반응이 확신 있는 신호로 누적되는 구간)에서 발생함
- 평가가 pick-and-place 단일 task·단일 VLA policy(GR00T)·러시아어 stop phrase 기준으로 한정돼 있고, 저자도 language·culture·age·neurodiversity에 대한 일반화는 이 연구로 검증되지 않는다고 명시함

**Top-tier conference 적합성 — 38/100 · 추천 venue: ICRA / IEEE RA-L (또는 ACM/IEEE HRI)**

실로봇(Unitree G1)과 실제 사용자 16명을 포함한 end-to-end 평가, latency까지 측정한 systems 기여는 실험적 설득력이 있음. 다만 감지 모듈 자체가 고전적 shallow classifier 조합이라 방법론적 새로움이 작고, 단일 task·단일 policy·작은 표본(특히 prospective 평가는 1명)이라 CoRL·RSS·NeurIPS 수준 oral보다는 ICRA/IROS나 HRI 계열의 regular paper에 더 맞는 수준으로 판단함.

**추천 이유 & 누리랩 연구와의 연결점**

- failure detection/recovery 연구 라인에 직접 연결됨 — SAFE·FAIL-Detect 같은 robot-internal monitor와 SocialVLA식 external social-reaction 채널을 결합하는 hybrid failure detector로 확장하는 아이디어 검토할 만함
- reaction-centered intervention record(반응 시각, 활성 VLA action, correction transcript)는 robot memory나 test-time optimization 연구에서 '실패로 이어질 뻔한 순간'의 supervision으로 쓸 수 있음 — 실패 직전 상태를 기록해 두는 방식과 연결됨
- object-centric 3DGS나 scene graph와는 직접 연결이 약하지만, robot-relevance 추정(사람이 로봇 어디를 보는지)을 active perception·semantic mapping의 attention 신호로 재활용하는 방향은 고려할 만함

---

## 오늘의 핵심 연구 트렌드 종합

- **world-action model(WAM)의 중간 표현 경쟁** — Top 15 중 7편이 미래 시각 상태와 action을 함께 예측하는 WAM 계열임. 표현 방식은 sparse sub-goal 프레임([ProWAM](https://arxiv.org/abs/2610.02508)), 객체 keypoint effect program([PEWAM](https://arxiv.org/abs/2610.02398)), 3D point trajectory([PointWAM](https://arxiv.org/abs/2610.02840)), latent future([IG-VLA](https://arxiv.org/abs/2610.02626), [ProAct](https://arxiv.org/abs/2610.02323)), subgoal 이미지([ViGAR](https://arxiv.org/abs/2610.02368)), spectral latent([WING](https://arxiv.org/abs/2610.03607))로 갈라지는 중임.
- **사람 영상을 로봇 action prior로 직접 전이** — [NAVA-WAM](https://arxiv.org/abs/2610.03391)은 observation-only 비디오로 action policy를 중간 표현 없이 직접 사전학습함(위 7편과 달리 WAM 중에서도 중간 표현 자체가 없는 예외임). [WING](https://arxiv.org/abs/2610.03607)은 카메라 모션을 분리해 interaction만 남기고, [KungfuAthleteBot](https://arxiv.org/abs/2610.03388)은 영상 복원 결함을 직접 수리함. 셋 다 "영상을 더 모으기"가 아니라 "영상의 결함을 다루는 방식"을 핵심 기여로 삼음.
- **실패 신호의 다각화** — 실패를 보는 관점이 내부 reward([CriticHack](https://arxiv.org/abs/2610.02527), wrong-object failure 증폭 진단), 외부 사람 반응([SocialVLA](https://arxiv.org/abs/2610.02360)), world model latent collapse([JEPA plannability](https://arxiv.org/abs/2610.03137))로 나뉘어 각자 다른 실패 유형을 잡아냄. 세 신호를 한 시스템에서 합치는 연구는 아직 없음.
- **능동 지각(active perception)의 하드웨어 단순화** — [EyeRobot 2.0](https://arxiv.org/abs/2610.03710)은 손목 카메라 없이 스테레오 한 대의 시선을 움직여 정밀 조작을 수행함. 카메라를 늘리는 대신 움직이는 방향의 연구로, 오늘 배치에서 가장 실험 증거가 강함(실로봇 1,000회 이상).
- **데이터 희소 상황의 안정화 기법** — [Multi-Fidelity Policy Gradients](https://arxiv.org/abs/2610.02505)는 저정밀 시뮬레이터 데이터를 control variate로 써서 PPO 분산을 줄임. 실제 Franka에서는 업데이트당 4 에피소드로 학습이 안정화됨. WAM 열풍과 별개로, real-robot RL의 실질적 비용 문제를 다룸.
- **장기 과제의 자율 자기개선** — [MobiAgent](https://arxiv.org/abs/2610.03476)는 고정 sub-task 대신 atomic skill을 매 스텝 재조합하고, 배포 중 rollout을 사람 라벨 없이 clustering해 skill을 계속 재학습함. 개별 요소는 기존 라인의 조합이지만 통합 파이프라인으로서의 실증이 탄탄함.

## 유망 연구 방향 및 프로젝트 제안

**WAM 예측-실제 괴리를 범용 실패 조기 감지 신호로 쓰기**
- research question: world-action model이 예측한 미래 표현(sub-goal, point trajectory, latent)과 실제 rollout의 괴리가 조작 실패를 몇 스텝 전에 예고할 수 있는가?
- 접근·novelty: ProWAM·PointWAM·ProAct 모두 "예측 대 실제" 신호를 갖고 있지만 failure detection에 쓰지 않음(각 논문의 recommendation에서 공통으로 지적된 공백). 이 괴리를 정량화해 test-time 모니터로 쓰는 게 신규 지점임.
- 왜 지금·경쟁 prior works: SAFE·FAIL-Detect 같은 기존 failure detector는 action 자체의 uncertainty만 봄. WAM이 이미 world prediction을 갖고 있으니 추가 모델 없이 공짜로 얻는 신호라는 점이 차별점.
- risk·target venue: WAM 종류별로 괴리의 의미(2D sub-goal vs 3D point vs latent)가 달라 일반화가 안 될 위험이 있음. target: CoRL/RSS.

**object-centric 3DGS를 WAM의 중간 표현으로 교체**
- research question: PointWAM의 point trajectory나 PEWAM의 keypoint effect program을 object-centric 3DGS로 바꾸면 non-rigid object·occlusion 상황에서 더 잘 버티는가?
- 접근·novelty: 두 논문 모두 rigid keypoint/point cloud 기반이라 변형체·얇은 물체에 약함(두 deep review의 recommendation에서 공통 지적). 3DGS는 형상·외형을 함께 표현해 이 한계를 메울 후보임.
- 왜 지금·경쟁 prior works: PointWAM(scene-actor 분리), PEWAM(effect-centric)이 바로 이번 주 공개돼 아직 3DGS 결합 시도가 없음. 선점 가능.
- risk·target venue: 3DGS 렌더링·최적화 비용이 WAM의 실시간 inference 요구와 충돌할 위험이 있음. target: CoRL/RSS, 실로봇 검증 필수.

**counterfactual world-action calibration**
- research question: ProAct는 factual trajectory만 학습해 proposal을 바꿨을 때 결과가 어떻게 달라지는지 모른다는 한계가 있음. counterfactual 학습 신호를 추가하면 (action 생성 시작점 분포를 교정하는 모듈인) World Expert의 교정 정확도가 오르는가?
- 접근·novelty: 같은 장면에서 다른 proposal을 가정했을 때의 결과를 world model로 시뮬레이션해 counterfactual pair를 만들고, 이를 World Expert 학습에 추가하는 방향.
- 왜 지금·경쟁 prior works: ProAct·DreamVLA·WorldVLA 계열이 모두 factual-only. counterfactual reasoning은 누리랩이 이미 우선순위로 두는 주제와 직결됨.
- risk·target venue: counterfactual rollout의 품질이 world model 자체의 한계에 묶여 악순환할 위험이 있음. target: NeurIPS/ICLR.

**내부 reward 신호와 외부 사람 반응 신호를 합친 hybrid failure detector**
- research question: CriticHack이 찾은 wrong-object failure(reward는 오르는데 엉뚱한 물체를 조작)를, SocialVLA의 사람 반응 채널이 몇 초 더 빨리 잡아내는가?
- 접근·novelty: 두 신호가 서로 다른 실패 유형(reward 착시 vs 관찰자가 보기에 명백한 오류)을 잡을 가능성이 높아, 단순 병렬 결합만으로도 recall 개선 여지가 큼.
- 왜 지금·경쟁 prior works: SocialVLA 저자도 robot-internal monitor와의 결합을 future work로 남겨둠. 경쟁자 없음.
- risk·target venue: 사람 관찰자가 상시 배치되는 상황이 제한적이어서 일반적 배포 시나리오에서 활용도가 낮을 위험이 있음. target: IROS/ICRA.

**sim-to-real control variate를 VLA test-time 적응에 적용**
- research question: Multi-Fidelity Policy Gradients의 control variate 아이디어를, VLA fine-tuning이 아니라 배포 중 test-time replanning의 신뢰도 추정에 쓸 수 있는가?
- 접근·novelty: world model의 sim rollout(저정밀)과 실제 관측(고정밀) 간 상관을 모니터링해, 상관이 깨지면 world model 예측에 기반한 replanning을 꺼버리는 fallback 게이트로 응용.
- 왜 지금·경쟁 prior works: 원 논문은 RL 학습 단계에만 적용함. test-time 적응 쪽은 미개척.
- risk·target venue: 분산 감소 이론이 학습 중 gradient 추정을 전제로 해서 inference-time으로 옮길 때 재유도가 필요함. target: CoRL, 빠른 산출 트랙에 적합.

## 오늘 반드시 읽어야 할 논문

- [EyeRobot 2.0: Active Gaze for Precise Manipulation without Wrist Cameras](https://arxiv.org/abs/2610.03710) — 손목 카메라 없이 능동 시선으로 정밀 조작을 수행해 오늘 배치에서 실험 증거가 가장 강함.
- [Keep the Effect, Drop the Actor: Programmable Effect-to-Execution World-Action Models](https://arxiv.org/abs/2610.02398) — 시연을 actor 없는 effect program으로 바꾸는 발상이 신선하고, 사람이 program을 직접 편집할 수 있다는 점에서 robot memory·test-time re-planning과 바로 연결됨.
- [World-Calibrated Proposal-to-Action Flow for Vision-Language-Action Models](https://arxiv.org/abs/2610.02323) — world model로 flow-matching source 자체를 교정해 효율성과 성능을 동시에 잡은 드문 사례임.
- [Native Action-Prior Learning from Videos for World Action Models](https://arxiv.org/abs/2610.03391) — action-free 비디오에서 action policy를 중간 단계 없이 직접 학습하는 구조로, 대규모 비디오 활용의 scalable path를 제시함.
- [PointWAM: 3D World Action Modeling for Dexterous Robotic Manipulation](https://arxiv.org/abs/2610.02840) — world를 scene과 actor로 명시적으로 분리하는 3D 표현이 object-centric representation 연구에 직접 참고가 됨.
- [Rethinking World-Action Model for Compositional and In-Context Robotic Manipulation](https://arxiv.org/abs/2610.02368) — subgoal planner와 executor를 world model 표현으로 공유시켜 long-horizon compositional task를 푸는 구조임.
- [World Action Learning via Interaction-Centric Spectral Latent Guidance](https://arxiv.org/abs/2610.03607) — egocentric video에서 카메라 모션과 interaction을 분리하는 전처리 방식이 다른 video-to-robot 연구에도 바로 적용 가능함.
- [Multi-Fidelity Policy Gradients Stabilize Data-Scarce Reinforcement Learning](https://arxiv.org/abs/2610.02505) — 업데이트당 실제 로봇 에피소드 4개로 학습을 안정화시킨 결과가 실질적이라 real-robot RL 비용 문제에 바로 쓸 수 있음.
- [CriticHack: Evaluating Visual Rewards Under Robot Policy Optimization](https://arxiv.org/abs/2610.02527) — learned reward로 정책을 최적화할 때 생기는 wrong-object failure 착시를 엄밀하게 입증해, reward 기반 VLA RL fine-tuning을 하는 모든 연구가 점검해야 할 함정을 보여줌.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (542편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2610.02508'>World Action Modeling with Progressive Visual Planning</a></td><td>82</td><td>9</td><td>World Model</td><td>sparse visual sub-goal을 예측해 action을 anchor하는 world action model로 실로봇 zero-shot 70% 성공을 보여 world model·manipulation 우선 주제에 정확히 부합함</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2610.02398'>Keep the Effect, Drop the Actor: Programmable Effect-to-Execution World-Action Models</a></td><td>76</td><td>9</td><td>World Model</td><td>데모에서 actor를 제거하고 object effect만 추출해 programmable하게 재조합하는 새로운 world-action representation이며 네 개 팔에서 재학습 없이 전이되고 실로봇 수치도 강함.</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2610.02840'>PointWAM: 3D World Action Modeling for Dexterous Robotic Manipulation</a></td><td>76</td><td>9</td><td>World Model</td><td>장면과 손을 분리해 3D point trajectory로 공동 예측하는 world-action model로 사람 영상 사전학습만으로 DexJoCo 성공률을 56.9%p 올리고 실로봇에서도 강한 VLA를 능가함.</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2610.03391'>Native Action-Prior Learning from Videos for World Action Models</a></td><td>72</td><td>9</td><td>VLA</td><td>관찰 전용 비디오에서 직접 action policy를 사전학습하는 native action-prior 학습으로 action 라벨 없는 robot 데이터 확장성을 보여주고 real-robot 일반화를 입증함</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2610.02368'>Rethinking World-Action Model for Compositional and In-Context Robotic Manipulation</a></td><td>72</td><td>9</td><td>World Model</td><td>world-action model에 subgoal 단위 계층 구조를 도입해 compositional·in-context manipulation을 다루고 RoboTwin과 실로봇에서 baseline 대비 큰 성능 향상을 보임.</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2610.03710'>EyeRobot 2.0: Active Gaze for Precise Manipulation without Wrist Cameras</a></td><td>70</td><td>9</td><td>Manipulation</td><td>스테레오 카메라만으로 두 눈이 응시점을 능동적으로 좇게 해 wrist camera 없이도 정밀 양팔 조작을 가능케 한 active gaze 방식으로 1000회 이상 실로봇 시험에서 손목카메라 가림 상황을 두 배 이상 능가함.</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2610.03137'>Keeping JEPA World Models Plannable When Little of the Frame Moves</a></td><td>70</td><td>9</td><td>World Model</td><td>JEPA world model이 action-insensitive latent 때문에 planning에 실패하는 원인을 진단하고 inverse-dynamics 보조 손실로 language-goal pushing 성공률을 0.003에서 0.35로 끌어올린 연구임</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2610.02626'>Imagine the Future, Internalize the Gist: Efficient VLA Reasoning via Internalized Spatiotemporal Imagination</a></td><td>70</td><td>8</td><td>VLA</td><td>VLA가 미래 scene을 latent 공간에서 상상하고 압축해 reasoning 비용을 6배 줄이는 test-time efficiency 기여로 robot manipulation과 직결됨</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2610.02527'>CriticHack: Evaluating Visual Rewards Under Robot Policy Optimization</a></td><td>70</td><td>8</td><td>RL</td><td>학습된 visual reward가 성공률과 task-irrelevant 실패(wrong-object)를 동시에 올릴 수 있음을 정량적으로 보여 reward hacking의 숨은 메커니즘을 규명한 rigorous한 분석임.</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2610.02323'>World-Calibrated Proposal-to-Action Flow for Vision-Language-Action Models</a></td><td>68</td><td>9</td><td>VLA</td><td>flow 기반 VLA의 생성 시작점을 최근 행동과 예측 미래에 맞춰 보정하는 ProAct로 파이-0.5 대비 denoising step을 절반으로 줄이면서 sim·실로봇 성능을 모두 높인 VLA formulation 연구임</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2610.02360'>SocialVLA: A Social Perception Gateway for Human-Reaction-Based Failure Detection and Recovery in VLA Manipulation</a></td><td>68</td><td>9</td><td>VLA</td><td>사람의 반응을 실패 감지 신호로 쓰는 새로운 failure detection 문제 설정이며 실제 15명 참가자·실로봇 실험으로 뒷받침됨.</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2610.03476'>MobiAgent: Dual-Loop Recursive Policy Self-Improvement for Long-Horizon Mobile Manipulation</a></td><td>68</td><td>9</td><td>Manipulation</td><td>고수준 추론과 저수준 flow-matching 실행을 분리하고 배포 rollout을 자동 세분화해 스킬 라이브러리를 지속 학습하는 dual-loop 프레임워크로 RoboCasa 성공률을 7.5%에서 27.5%로 끌어올림.</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2610.03607'>World Action Learning via Interaction-Centric Spectral Latent Guidance</a></td><td>68</td><td>9</td><td>World Model</td><td>에고센트릭 영상에서 카메라 모션을 분리하고 손-물체 상호작용만 latent action으로 증류한 뒤 저주파 스펙트럼 성분으로 로봇 행동을 가이드하는 방법으로 LIBERO 99.2%, RoboTwin 93.8%의 강한 결과를 보임.</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2610.02505'>Multi-Fidelity Policy Gradients Stabilize Data-Scarce Reinforcement Learning</a></td><td>68</td><td>8</td><td>RL</td><td>저충실도 시뮬레이터 데이터를 control variate로 활용해 고충실도 데이터 효율을 높인 PPO 변형이며 실제 Franka 로봇팔에서 4회 에피소드만으로 안정적 학습을 보임</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2610.03388'>KungfuAthleteBot: learning high-dynamic humanoid motion from video with unified robust recovery</a></td><td>68</td><td>8</td><td>RL</td><td>영상에서 추출한 비물리적 trajectory를 물리적으로 교정하고 pseudo-low-kinetic-energy 샘플링으로 실현 가능한 초기화를 유도해 단일 정책이 임의의 낙상에서 0.7초 만에 복구하는 humanoid 고난도 모션 학습 결과임.</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2610.03079'>RIFAR: Reliability and Forgetting-Aware Replay for Continual Robot Learning</a></td><td>68</td><td>8</td><td>Manipulation</td><td>world-action model의 생성 replay에서 행동-시각 일관성을 걸러내는 RIFAR로 LIBERO와 실로봇에서 continual robot learning의 forgetting을 줄인 연구임</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2610.02759'>Proprioceptive Sketches as Long-Horizon Intent for Generative Action Policies</a></td><td>66</td><td>8</td><td>Manipulation</td><td>시간이 아닌 호길이로 매개화한 compact한 proprioceptive sketch로 장기 의도를 표현하는 새로운 representation이며 real bimanual task에서 47.5%에서 75%로 성공률을 크게 올림.</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2610.03333'>Equivariant Visual-Tactile Diffusion Policy for Contact-Rich Manipulation</a></td><td>65</td><td>8</td><td>Manipulation</td><td>시각·촉각을 구형 토큰으로 투영해 equivariant하게 융합하는 CoRL 2026 논문으로 contact-rich 과제에서 데이터 효율을 크게 높임.</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2610.03516'>XGenAct: Geometry-Enhanced World Action Models through Cross-Task Generation</a></td><td>65</td><td>8</td><td>World Model</td><td>RGB·action뿐 아니라 depth·normal·segmentation까지 하나의 video diffusion transformer로 통합 예측하는 world-action model로 RLBench 외부 비교에서 52% 대 26%로 baseline을 크게 앞섬.</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2610.02801'>VIGOR: Zero-Shot Visual Generalization via Latent-Space Consistency in Model-Based Reinforcement Learning</a></td><td>65</td><td>7</td><td>World Model</td><td>model-based RL의 latent-space consistency로 시각적 분포 변화에 대한 zero-shot 일반화를 개선하고 DMC·Robosuite에서 검증한 world model 연구임</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2610.02521'>Spatial Memory Intelligence: Endowing World Models with Understanding-Driven Long-Term Memory</a></td><td>65</td><td>6</td><td>World Model</td><td>world model의 장기 spatial memory를 MLLM 기반 understanding으로 관리하는 프레임워크로 robot memory와 직결됨</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2610.02459'>OpenRUA: Robot-Use Agents Are Zero-Shot Visuomotor Policies</a></td><td>64</td><td>8</td><td>VLA</td><td>코딩 에이전트에 ROS2 터미널 접근만 주고 별도 추상화 없이 zero-shot visuomotor policy로 쓰는 새로운 패러다임이며 CaP-Bench 99%, LIBERO-PRO 87%로 기존 전용 파이프라인 필요성에 의문을 제기함.</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2610.02691'>DeltaWorld: Physically Consistent Interactive World Simulators via Action-Conditioned Latent Increment Learning</a></td><td>64</td><td>8</td><td>World Model</td><td>다음 latent state 전체 대신 action 유도 변화량(delta)만 예측해 object interpenetration 등 물리적 비일관성을 줄인 world model이며 cross-robot 데이터셋에서 FVD 46.6% 개선함.</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2610.02804'>SARI: Phase-Split Sim-Real Co-Training for Contact-Rich Manipulation</a></td><td>63</td><td>8</td><td>Manipulation</td><td>자유공간 접근은 시뮬레이션에서, contact 상호작용은 소수 실데모에서 학습하는 phase-split 전략으로 실데이터 수집시간을 34.3% 줄이면서 미지 배치에서 baseline이 전부 실패하는 상황에서 27.5% 성공함.</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2610.02338'>SoTa: Soft Tactile Skins for Dexterous Manipulation</a></td><td>62</td><td>9</td><td>Manipulation</td><td>사람과 로봇 손에 공통 레이아웃으로 부착 가능한 저가 정전식 촉각 피부(SoTa)로 사람 데모를 섞어 조작 성공률을 22.8%에서 45.9%로 두 배 이상 올린 tactile perception 연구임</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2610.02784'>SimpleTouch: Can Vision-Language-Action Models Master Contact-Rich Manipulation Without Tactile Policy Pretraining?</a></td><td>62</td><td>8</td><td>VLA</td><td>tactile policy 사전학습이나 별도 정합 없이 π0.5에 tactile expert만 추가해도 contact-rich manipulation이 가능함을 보여 기존 가정에 반례를 제시함.</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2610.02788'>Skill2Real: Agentic Skill Learning for Zero-Shot Sim-to-Real Robot Manipulation</a></td><td>62</td><td>8</td><td>Manipulation</td><td>Cerebellum-Brain 계층으로 로컬 스킬과 과제 조합을 분리 학습해 zero-shot sim-to-real을 달성했고 LIBERO-Pro Long에서 2%에서 56.3%로 큰 향상을 보임.</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2610.03132'>Safe Streaming Flow Planning by Aligning Sampling Dynamics with Execution Dynamics</a></td><td>62</td><td>8</td><td>RL</td><td>flow sampling dynamics를 execution dynamics와 맞춰 실행 단계에만 고차 control barrier function을 적용하는 CoRL 2026 논문으로 안전성과 재계획 지연을 동시에 개선함.</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2610.03587'>AVL-JEPA: Preventing Causal Dynamics Information Collapse In Joint Embedding Predictive Architecture World Models</a></td><td>62</td><td>8</td><td>World Model</td><td>JEPA가 동작의 물리적 결과 정보를 버리는 causal dynamics collapse를 식별하고 action-grounded anchor와 vision-invariance pathway로 방지하는 방법으로 시각 교란 하에서도 성공률을 크게 지킴.</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2610.03615'>Bridging Frontier Reasoning and Robot Execution: From Autonomous Demonstration Generation to Dense Language Supervision</a></td><td>62</td><td>8</td><td>VLA</td><td>frontier 모델로 교정 데모를 자동 생성해 로컬 정책을 학습시키고 세 단계 조밀 언어 지도까지 결합한 이중 bridge 구조로 RoboCasa 365·BEHAVIOR-1K 장기과제에서 효과를 보임.</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2610.02860'>Counterfactual Action Evaluation, Observation Bottlenecks, and Representation Geometry in Joint-Embedding Predictive World Models</a></td><td>62</td><td>7</td><td>World Model</td><td>JEPA 기반 world model이 action의 결과를 실제로 구별하는지 simulator state fork로 검증해 observation bottleneck과 action-path 활용 부족을 밝힌 counterfactual 평가 연구임</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2610.03154'>Does Physics Live in the Activations? Localizing Physical Quantities in Video Diffusion Models</a></td><td>62</td><td>5</td><td>World Model</td><td>video diffusion model의 내부 activation에서 물리량이 denoising 중 능동적으로 구성됨을 probing으로 밝혀 world model의 물리 이해를 규명함</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2610.02322'>SCION: Scene Composition with Instanced Neural Primitives</a></td><td>62</td><td>4</td><td>3D Vision</td><td>3DGS를 재사용 가능한 primitive와 instance로 압축하는 구조로 object-centric 3D representation에 기여함</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2610.02341'>Filter-Aware Fine-Tuning for Safe Humanoid Whole-Body Tracking</a></td><td>60</td><td>7</td><td>RL</td><td>안전 필터와 추적 정책 간 불일치를 분석하고 CoFiT로 보강한 연구로 Unitree G1 실기 검증까지 포함하나 문제 자체는 기존 안전필터 통합의 engineering 개선에 가까움.</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2610.03620'>UniIntervene++: An Adaptive Intervention Agent for Efficient Real-World Reinforcement Learning</a></td><td>58</td><td>8</td><td>Manipulation</td><td>policy 역량 변화에 맞춰 자율 실행과 보조 개입 비율을 semi-MDP option으로 학습하는 UniIntervene++로 5개 실로봇 조작 과제에서 성공률 89.67%, 개입 0.77%를 달성한 연구임</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2610.02898'>MixVLA: Adaptive Mixing of Non-Invariant Information for Generalizable Vision-Language-Action Models</a></td><td>58</td><td>8</td><td>VLA</td><td>task-irrelevant 비불변 정보를 적응적으로 섞어 정규화하는 model-agnostic 학습법으로 LIBERO-Plus·RoboTwin perturbation·실로봇 전반에서 OOD robustness를 개선함.</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2610.03538'>RATE: Risk-Aware Tactile Encoding for Contact-rich Robotic Manipulation</a></td><td>58</td><td>8</td><td>Manipulation</td><td>비슷한 촉각 신호라도 task 위험도가 다를 수 있음을 반영해 history 기반으로 위험을 인코딩하는 tactile representation으로 벤치마크 전반에서 성공률을 높임.</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2610.02697'>GeoScaffold: Learning Compact Geometric Latents via Reconstruction for Efficient Vision-Language Navigation</a></td><td>58</td><td>7</td><td>Navigation</td><td>학습 시에만 기하 정보를 내재화하고 추론 시 깊이 센서나 3D 인코더를 없애는 VLN 프레임워크로 지오메트리 scaffold 아이디어가 새로우나 경량화 지향이 평가에서 가점 요인은 아님.</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2610.02717'>RoboBridge: A Self-Evolving Embodied Agent Framework for Sim-to-Real Transfer</a></td><td>58</td><td>7</td><td>Embodied AI</td><td>sim-to-real 전이를 절차적 스킬의 지속적 적응 문제로 재정의하고 VLA를 도구로 감싸 재학습 없이 실행 보정하는 구조가 흥미로움.</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2610.03196'>Beyond Reward Hacking: Proxy Divergence Across Four Layers of a Staged Humanoid Learning Pipeline</a></td><td>58</td><td>7</td><td>RL</td><td>reward뿐 아니라 curriculum gate·평가 통계·reference motion 모두를 proxy로 보고 각 층의 divergence 메커니즘을 정식화한 개념적 확장으로 단일 humanoid 학습 사례로 구체적 반례를 보임.</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2610.03374'>EVEWorld: Physical Evolution Supervision for Embodied World Models</a></td><td>58</td><td>6</td><td>World Model</td><td>embodied world model이 시각적 그럴듯함만 좇는 Model Laziness를 process-level supervision으로 줄여 물리적으로 일관된 객체 진화를 학습함</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2610.03716'>MoSE3: Learning World-Space SE(3) at Every Pixel</a></td><td>58</td><td>6</td><td>3D Vision</td><td>단안 비디오에서 픽셀 단위 6-DoF SE(3) 모션을 point track과 rigidity로 복원해 관절체 객체의 강체 그룹을 함께 추정함</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2610.02274'>Awomo-SimDataEngine: Agentic Simulation-ReadyWorld Generation</a></td><td>56</td><td>8</td><td>Manipulation</td><td>asset·scene 생성부터 로봇 데모 합성까지 묶은 agentic 시뮬레이션 데이터 엔진(Awomo)으로 LIBERO-Plus에서 World-Action Model 성공률을 77%에서 89%로 올린 실용적 데이터 생성 연구임</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2610.03278'>DexJoCo-X: Benchmarking Action Representations for Multi-Hand Dexterous Manipulation</a></td><td>56</td><td>8</td><td>Manipulation</td><td>일곱 종 dexterous hand에 걸친 action representation을 통제 비교한 벤치마크로 cross-embodiment 학습이 좌표·사전학습·아키텍처 전체의 조합에 달려 있음을 보임.</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2610.02662'>Mind the Refinement Gap: When Safe High-Level Robot Plans Produce Unsafe Executions</a></td><td>55</td><td>8</td><td>Embodied AI</td><td>semantic-graph 기반 고수준 plan이 안전하다고 판정되어도 실제 refined trace에서는 불안전해지는 refinement gap을 RoboGuard로 실증한 robot safety 연구임</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2610.02339'>NEEDLEWORK: Offline Rewriting of Robot Data with Verified Local Stitches</a></td><td>55</td><td>8</td><td>Manipulation</td><td>RGB와 proprioception만으로 실패·비효율 구간을 짧은 검증된 action bridge로 이어붙여 오프라인에서 로봇 데이터를 보강하는 NEEDLE로 실로봇 과제 성공률을 평균 21%p 올린 연구임</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2610.03013'>RYOPO: Bringing End-to-End Category-Level Object Pose Estimation into Real Time</a></td><td>55</td><td>7</td><td>Manipulation</td><td>RGB-D 기반 category-level 9-DoF object pose를 end-to-end로 실시간 추정해 manipulation의 pose 전처리 비용을 줄임</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2610.03031'>CrowdOcc: Monocular Semantic Scene Completion for Quadruped Robots in Crowded Indoor Environments</a></td><td>55</td><td>7</td><td>Navigation</td><td>사족보행 로봇을 위한 crowded indoor 환경의 단안 semantic scene completion 데이터셋·방법으로 ICRA 제출 로봇 연구임</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2610.02366'>Co-design Gym: A Unified Benchmark for Embodiment-Policy Co-optimization</a></td><td>55</td><td>7</td><td>RL</td><td>로봇 조작·보행 등 20개 도메인에서 embodiment와 policy를 공동 최적화하는 벤치마크로 co-design 연구의 기준점을 제공함</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2610.02802'>ManiPhysicsBench: Physics-Based Assessment of Object Preservation in VLA Manipulation</a></td><td>55</td><td>7</td><td>Manipulation</td><td>task 성공과 물리적 객체 보존을 분리 평가하는 새로운 benchmark로 VLA가 성공은 해도 물체를 손상시킬 수 있음을 드러낸 유의미한 평가축 제안임.</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2610.02811'>Learning Reflexive Behavior for Contact-Rich Manipulation</a></td><td>55</td><td>7</td><td>Manipulation</td><td>스프링·평면·레일 같은 단순 상호작용에서 학습한 proprioceptive reflex를 고수준 제어기 아래 고정층으로 두는 아이디어로 peg insertion 성공률을 22%에서 58%까지 끌어올림.</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2610.02813'>Register-Routed Delayed Fusion: Rewiring Shortcut-Prone Observation Fusion in Visuomotor Imitation</a></td><td>55</td><td>7</td><td>Manipulation</td><td>압축 신호가 시각 토큰에 조기 개입하는 경로를 register 기반으로 지연시켜 cross-modal shortcut을 억제한 fusion topology 연구로 appearance shift에서 ACT 대비 일관되게 우위를 보임.</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2610.03717'>Less Decoder is More Encoder: Geometric Representation Learning from Novel View Synthesis</a></td><td>55</td><td>6</td><td>Manipulation</td><td>novel view synthesis의 decoder 표현력을 제한해 transferable geometric representation을 학습시키고 robot manipulation 등 5개 과제에서 검증함</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2610.02985'>On Representational Alignment among Embodied Agents</a></td><td>55</td><td>6</td><td>Embodied AI</td><td>여러 embodied agent 간 표상이 항상 정렬될 필요는 없고 interaction-relevant한 모호성만 해소하면 된다는 relational sufficiency 이론을 정식화한 일반화 가능한 틀임.</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2610.03664'>ProAR: Learning Prospective Reasoning with Autoregressive Video Models</a></td><td>55</td><td>5</td><td>World Model</td><td>목표 프레임 예측과 미래 표현 self-alignment로 autoregressive 비디오 생성을 goal-directed reasoning으로 전환하고 embodied reasoning 적용 가능성을 제시함</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2610.02876'>Seeing, Saying, but Not Using: From Reportable Spatial Facts to Usable States in Multimodal Large Language Models</a></td><td>55</td><td>4</td><td>Embodied AI</td><td>MLLM이 공간 사실을 보고는 하지만 변환 추론에 사용하지 못하는 availability-utilization gap을 밝힌 embodied spatial reasoning 연구임</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2610.03498'>Detect and Suppress: A Mechanistic Defense against Adversarial Patches in VLA Models</a></td><td>54</td><td>7</td><td>VLA</td><td>sparse autoencoder로 adversarial patch에 반응하는 내부 feature를 찾아 공격 탐지 시에만 억제하는 mechanistic defense로 fine-tuning 없이 VLA 강건성을 높임.</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2610.03563'>A Unified Framework for Empowerment and Predictive Control</a></td><td>54</td><td>6</td><td>RL</td><td>probing 정책과 실행 정책을 하나로 통합해 1차 미분만으로 계산 가능한 empowerment를 표준 MPC에 결합한 일반화 가능한 공식화임.</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2610.03622'>CORNAV: Construction-Aware Reasoning for Robot Navigation on Active Worksites</a></td><td>52</td><td>7</td><td>Navigation</td><td>CAD 도면과 공사 일정을 open-vocabulary scene graph에 정렬해 건설현장 내비게이션 성공률을 13%에서 72.2%로 올린 실용적 프레임워크임.</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2610.02554'>Test-time Multi-agent Coordination by Decomposed Value Gradient Flow</a></td><td>52</td><td>5</td><td>RL</td><td>offline MARL에서 flow-matching prior와 test-time Stein variational gradient로 고가치 영역을 탐색하는 test-time optimization 기법으로 우선주제와 연결되나 robot 실험은 없음</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2610.03632'>World Embedding Benchmark</a></td><td>52</td><td>4</td><td>World Model</td><td>유체·강체 등 물리 현상 8천 사례로 비디오 표현이 물리 정보를 얼마나 담는지 평가하는 world model 벤치마크임</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2610.03395'>Bidirectional Voronoi-biased Exploration Curriculum for Reinforcement Learning</a></td><td>50</td><td>7</td><td>Manipulation</td><td>시작·목표 상태를 양방향으로 확장해 sparse reward 장기 과제를 푸는 BVER 커리큘럼으로 사족보행 박스 등반과 로봇팔 ring-on-peg 조립까지 실로봇형 과제에서 검증된 exploration 기법임</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2610.02803'>LOCUS: Landmark-Oriented Container Discrimination Using Spatial Graphs</a></td><td>50</td><td>7</td><td>Embodied AI</td><td>scene graph 위에서 GNN으로 CLIP 임베딩을 갱신해 공간·의미 정보를 함께 쓰는 container 탐색 방법으로 CLIP 단독 대비 우수하고 실로봇 탐색까지 보임.</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2610.03248'>EmbPASS: Towards Cross-Embodiment Open Panoramic Segmentation</a></td><td>50</td><td>6</td><td>Embodied AI</td><td>차량·드론·웨어러블·사족보행 플랫폼 전반의 cross-embodiment panoramic segmentation 벤치마크와 방법을 제시함</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2610.03537'>Autonomous Robotic Navigation for Endovascular Brain-Computer Interface Access</a></td><td>50</td><td>6</td><td>RL</td><td>뇌혈관 내 BCI 접근을 위한 최초의 자율 로봇 내비게이션으로 도메인은 새롭지만 SAC와 failure prediction은 기존 기법의 의료 로봇 적용에 가까움.</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2610.02660'>SpectralCache: Accelerating Diffusion-Based World Models via Spectral Feature Caching</a></td><td>50</td><td>4</td><td>World Model</td><td>diffusion 기반 world model의 spectral feature caching으로 추론을 5배 가속하는 world model 효율화 기여임</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2610.03604'>Mastering Atari 2600 Games with Discovered Options</a></td><td>50</td><td>4</td><td>RL</td><td>Laplacian representation으로 option을 자동 발견해 탐색·credit assignment·일반화를 동시에 개선한 Wayfarer로 Montezuma&#x27;s Revenge 등에서 state-of-the-art를 달성한 skill 발견 연구임</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2610.02260'>MintFlow: Minimal Trajectory Intervention for Constrained Flow Matching</a></td><td>50</td><td>4</td><td>LG</td><td>학습된 flow field는 그대로 두고 중간 상태에 최소 개입만 가해 제약을 만족시키는 adjoint 기반 닫힌해 방법으로 flow-matching 기반 로봇 정책의 test-time 제약 충족에 응용될 여지가 있음.</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2610.02542'>How To Train Your World Model: Fine-tuning vs RAG for LM-based World Modeling</a></td><td>50</td><td>4</td><td>World Model</td><td>embodied·web nav 환경에서 LM 기반 world model의 fine-tuning 대 RAG를 체계 비교한 실증 연구임</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2610.02825'>TerrainForge: Physics-Grounded road geometry Editing for Counterfactual Autonomous Driving</a></td><td>50</td><td>3</td><td>CV</td><td>도로 기하구조 편집이 차량 동역학에 전파되도록 한 물리 기반 counterfactual 자율주행 시뮬레이션임</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2610.02666'>CHASE-VLA: Post-Training Quantization Framework for Vision-Language-Action Models with Chunk-Aware Scale Estimation</a></td><td>48</td><td>6</td><td>VLA</td><td>VLA의 diffusion action expert를 chunk 인식 기반으로 W4A4 양자화해 FP16 성능을 유지하는 효율화 기여임</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2610.03015'>OmniAct3D: Leveraging Foundation Geometry and Evidence-Grounded Reasoning for Panoramic 3D Detection</a></td><td>48</td><td>6</td><td>Embodied AI</td><td>360도 파노라마 영상에 VFM을 적응시킨 mobile embodied agent용 3D 탐지로 surround perception에 기여함</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2610.02706'>AdaTempo: Learning Shared Relative Tempo from Demonstrations for Faster Robot Manipulation</a></td><td>48</td><td>6</td><td>Manipulation</td><td>데모 간 공유된 상대적 tempo를 찾아 가속 프로파일을 학습하는 방법으로 최대 3.57배 속도 향상을 보이나 기존 imitation policy 위에 얹는 모듈 수준 기여임.</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2610.02728'>Around the World: Unified Learned Locomotion on a 270 g Continuous-Rotation Quadruped</a></td><td>48</td><td>6</td><td>RL</td><td>270g 연속회전 다리 쿼드러페드에서 단일 posture-conditioned RL 정책으로 직립·역보행·착지복구를 통합한 결과가 인상적이나 로봇러닝 핵심 주제보다는 하드웨어·로코모션 쪽 기여임.</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2610.02750'>CSIR: Contextually and Socially Informed Robots for Efficient Person Goal Navigation</a></td><td>48</td><td>6</td><td>Navigation</td><td>거리와 의미 정보를 신뢰도로 가중한 사람찾기 내비게이션 프레임워크로 실로봇 검증은 있으나 방법론적 새로움은 제한적임.</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2610.03713'>What Should World Models Forget? Stratified Retention for Continual Adaptation</a></td><td>48</td><td>5</td><td>World Model</td><td>world model이 무엇을 잊어야 하는지를 불변 시간축 기준으로 계층화해 물리·object permanence는 보존하고 인스턴스 사실은 갱신해야 한다고 제안한 continual world model 연구임</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2610.02594'>How Causality Bridges the Semantic Gap</a></td><td>48</td><td>4</td><td>CV</td><td>causal graph로부터 변수 의미를 복원하는 구조적 정렬 기법을 세 가지 robotics 시나리오에서 검증했으나 핵심 기여는 causal semantic labeling이고 robot action과는 직접 연결되지 않음</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2610.03312'>Optimal Planning in a Dynamic World</a></td><td>48</td><td>4</td><td>Navigation</td><td>실행 시작 시각을 모르는 상태에서 compound arrival time function으로 동적 환경 planning을 일반화한 이론 연구로 SIPP류 로봇 경로계획에 적용 가능함</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2610.02388'>Octrees as an Explicit 3D Language</a></td><td>48</td><td>3</td><td>3D Vision</td><td>octree occupancy token으로 3D를 명시적 언어처럼 다루는 새 representation을 제시함</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2610.03308'>T3lescope: Arbitrary-Resolution High-Fidelity Generative Surface Reconstruction from Images</a></td><td>48</td><td>3</td><td>3D Vision</td><td>단일 fixed-resolution generator를 coarse-to-fine cascade로 적용해 객체부터 도시 규모까지 일관된 메시를 생성함</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2610.02478'>Tropical Reinforcement Learning</a></td><td>48</td><td>2</td><td>RL</td><td>RL의 기대값 합산을 max 연산으로 바꾸는 tropical semiring 제안은 새로운 paradigm이나 LLM 추론에 한정됨</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2610.03453'>I2CD: Direct Image-to-Convex Decomposition for Simulation-Ready Collision Geometry</a></td><td>46</td><td>6</td><td>3D Vision</td><td>이미지에서 바로 convex decomposition을 예측해 물리 시뮬레이션용 충돌 geometry를 0.5초에 생성하는 효율적 도구로 실로봇 pick-and-place에도 적용되나 핵심은 엔지니어링 파이프라인 개선임.</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2610.02601'>Real-time Event-camera Stereo Visual Odometry via Keytime Gaussian Process Regression</a></td><td>46</td><td>5</td><td>3D Vision</td><td>이벤트카메라 stereo VO에 continuous-time GP를 결합해 상태 수를 줄이면서 ES-PTAM 대비 정확도를 크게 높였으나 로봇러닝 우선순위 주제와는 거리가 있는 perception 인프라 기여임.</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2610.02874'>SceneFactory-3D: Lifting 2D Traffic Scenes into 3D Physical Counterfactuals for Scalable Physically Grounded Safety Evaluation</a></td><td>46</td><td>5</td><td>Multimodal</td><td>타이어-노면 물리를 반영한 GPU 배치 주행 시뮬레이터로 도로 조건 physical counterfactual을 대규모 병렬 평가하는 인프라 기여이나 자율주행 도메인이라 로봇러닝 우선순위와는 다소 거리가 있음.</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2610.02343'>SCOPE-4D: Endoscopic 4D Geometry Foundation Models</a></td><td>45</td><td>4</td><td>3D Vision</td><td>내시경 4D geometry foundation model로 robotic assistance를 언급하나 의료 도메인 중심 기여임</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2610.03715'>4DCodeBench: Benchmarking Agents on Inverse Graphics of Dynamic Scenes</a></td><td>45</td><td>4</td><td>World Model</td><td>변형·유체·파괴 등 동역학을 비디오에서 실행 가능한 그래픽스 코드로 재구성하는 agent 벤치마크로 물리적 world model 이해를 평가함</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2610.02726'>SymRegFlow: Symmetry-Regularized Flow Matching for Video World Models</a></td><td>45</td><td>3</td><td>World Model</td><td>다중 뷰 world model을 연속 카메라 포즈로 확장하는 symmetry regularization 기법으로 자율주행 영상 생성에 적용됨</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2610.03047'>Parasitic Co-Denoising: Unlocking 3D Human Motion Generation in a Frozen Video Diffusion Model</a></td><td>45</td><td>3</td><td>Video</td><td>frozen video diffusion model의 중간 상태에서 3D human motion을 추출하는 parasitic decoding 패러다임으로 implicit physical/motion prior 활용이 흥미로움</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2610.02994'>Sentry: Learning to Recover from LLM Agent Failures at Test Time</a></td><td>45</td><td>3</td><td>Embodied AI</td><td>LLM 에이전트 실패 지식을 조건부로만 노출해 복구를 돕는 Sentry 레이어로 failure detection·recovery 우선주제와 직결되나 robot 실험은 없고 LLM agent 벤치마크에 한정됨</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2610.02331'>World Editing: Intervening on Executable Worlds at Increasing Depth</a></td><td>45</td><td>3</td><td>World Model</td><td>실행 가능한 게임 world를 속성·개체·역학·시스템 깊이별로 편집하는 IGMBench를 제시해 world editing을 world generation과 구분되는 능력으로 정식화했으나 물리 로봇 world model과는 도메인이 다름.</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2610.02832'>FastOPD: On-Policy Distillation for Lightweight VLA Deployment</a></td><td>44</td><td>6</td><td>VLA</td><td>on-policy distillation으로 대형 VLA를 경량화하는 방법으로 추론 지연을 78% 줄였으나 경량화·효율화 지향 기여라 우선 평가 대상은 아님.</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2610.02765'>Localized Conformal Safety Monitoring with Vision-Language Models for Autonomous Driving</a></td><td>44</td><td>5</td><td>Multimodal</td><td>frozen VLM 위에 conformal prediction 보정층을 얹어 충돌 예측 신뢰도를 높인 방법으로 CARLA 1.5만 trajectory에서 효과를 보였으나 5페이지 extended abstract로 깊이는 제한적임.</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2610.02708'>RoboChemGym: A Protocol-Driven Generative Simulation Framework for Long-Horizon Chemical Manipulation</a></td><td>42</td><td>6</td><td>Manipulation</td><td>화학 실험 프로토콜 기반 장기 조작 데모를 자동 생성하는 시뮬레이션 프레임워크로 도메인은 새롭지만 방법론 자체는 기존 task synthesis 기법의 적용에 가까움.</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2610.02848'>Permutation Robustness Is Not Enough: Action Collapse in Multi-Agent Transformer Policies</a></td><td>42</td><td>5</td><td>RL</td><td>순열 일관성 지표만으로는 agent가 똑같은 행동만 고르는 action collapse를 놓칠 수 있음을 보인 진단 연구로 통찰은 유효하나 합성 내비게이션 과제 범위가 좁음.</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2610.02974'>From Language Priors to Field Adaptation: Preference Learning for Traversability Estimation</a></td><td>42</td><td>5</td><td>Navigation</td><td>언어 prior와 소수 상대 이미지 주석으로 traversability를 도메인 적응시키는 샘플효율적 방법으로 실용적이나 novelty는 기존 preference learning 틀 안에 머무름.</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2610.02715'>Ego2World: Compiling Egocentric Cooking Videos into Executable Worlds for Belief-State Planning</a></td><td>42</td><td>4</td><td>Embodied AI</td><td>egocentric 요리 영상을 실행 가능한 belief-state planning 환경으로 변환한 벤치마크로 embodied planning과 맞닿아 있음</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2610.02597'>GRAFT: Growing Agglomerative Foundation Models via Continual Teacher Distillation</a></td><td>42</td><td>3</td><td>CV</td><td>여러 foundation model 지식을 continual distillation으로 통합하는 방법으로 범용 perception backbone에 기여함</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2610.02744'>EpiWorld: Grounding LLM Policy Agents in Epidemiological World Models</a></td><td>42</td><td>3</td><td>World Model</td><td>학습된 역학 world model과 정책 에이전트를 묶어 반사실적 rollout으로 정책을 개선하는 closed-loop 구조가 world model 활용 측면에서 로봇 연구에 참고될 수 있으나 도메인은 역학 정책임.</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2610.03515'>Learning from Repaired Reasoning: Root-Cause-Guided On-Policy Distillation</a></td><td>42</td><td>3</td><td>NLP</td><td>학생 모델의 추론에서 최초 오류 지점을 찾아 국소 수정하고 이어 학습시키는 root-cause 증류법으로 failure diagnosis 방법론 측면에서 로봇 실패복구 연구에 참고될 수 있음.</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2610.03695'>Language Models that Play Chess and Explain Their Moves</a></td><td>42</td><td>3</td><td>Multimodal</td><td>silent expert 체스 인코더와 LM을 cross-attention으로 묶고 Bellman-update 방식 distillation으로 설명 가능한 체스 모델을 만든 구조로 저자들이 로봇 등 silent expert encoder가 있는 도메인에 일반화 가능하다고 제시함.</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2610.02330'>Choosing Before Acting: Comparative Value Estimation for Long-Horizon Tool-Use Agents</a></td><td>42</td><td>3</td><td>RL</td><td>다음 도구 호출의 장기가치를 실행 전에 비교추정하는 CITA 프레임워크로 장기 과제의 credit assignment 문제에 접근한다는 점에서 robot skill chaining의 가치추정에 개념적으로 참고될 수 있음.</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2610.03626'>Depth as Time in One-Step Generative Models</a></td><td>42</td><td>0</td><td>Video</td><td>one-step 생성모델의 단일 forward pass 안에 multi-step denoising 계산이 depth 축으로 재배치됨을 보인 흥미로운 메커니즘 분석이나 robotics 적용은 없음</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2610.03530'>DR-IPC: Disturbance-Resilient Integrated Planning and Control for LiDAR-Based Quadrotor Navigation</a></td><td>40</td><td>5</td><td>Navigation</td><td>외란 관측기와 NMPC를 통합해 LiDAR 쿼드로터 내비게이션의 단일 계층 제어를 구현한 시스템으로 성능은 우수하나 로봇러닝 우선 주제와는 거리가 있는 고전 제어 기여임.</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2610.02298'>EditHero: A Benchmark for Long-Horizon Part-Level 3D Editing and Vibe Modeling</a></td><td>40</td><td>3</td><td>3D Vision</td><td>3D 편집 벤치마크로 LLM/VLM 에이전트 기반 편집을 분석했으나 robot learning과는 거리가 있음</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2610.03123'>Foresight: planning future perception in streaming VLMs without retraining</a></td><td>40</td><td>3</td><td>Multimodal</td><td>streaming VLM이 미래를 선제적으로 예측해 연산을 동적으로 재구성하는 training-free 기법으로 embodied streaming perception에 참고될 수 있음</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2610.03473'>UniDynamics: Event-RGB Fusion for Unified Future 4D Dynamic Scene Generation</a></td><td>40</td><td>3</td><td>World Model</td><td>event-RGB 융합으로 미래 RGB·depth·flow를 동시 예측하는 4D 동적 장면 생성 연구로 world model의 미래 예측에 관련됨</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2610.03120'>In-Distribution Forcing for Long Video Generation at Test Time</a></td><td>40</td><td>2</td><td>Video</td><td>AR 비디오 생성에서 KV 캐시가 분포를 벗어나는 문제를 self-caching으로 해결해 minute급 영상 생성을 안정화함</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2610.02525'>Learning What to Investigate Next: Meta-Reasoning for Long-Horizon Research Agents</a></td><td>40</td><td>2</td><td>RL</td><td>연구 배분과 실행을 분리하는 meta-reasoning 구조로 long-horizon planning에 닿아있으나 대상이 연구 agent이지 로봇이 아님</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2610.02252'>Counterfactual Predictions in Scientific Emulators Without Controlled Experiments</a></td><td>40</td><td>1</td><td>LG</td><td>부분적 메커니즘 지식과 사실 데이터만으로 과학 에뮬레이터의 counterfactual 예측을 가능하게 한 causal 방법론임</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2610.02344'>Drive vs. Decay: On the Training Dynamics of Joint-Embedding Predictive Architectures</a></td><td>40</td><td>1</td><td>LG</td><td>JEPA의 representation collapse를 초기 학습 동역학 이론으로 설명하고 안정화 predictor를 제안해 world model 기반 표현학습에 기여함</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2610.02799'>FUSEye: Training-Light Fisheye Detection with Overlapping Views and Zero-Initialized Adapters</a></td><td>38</td><td>5</td><td>CV</td><td>이동 로봇용 fisheye 탐지기를 frozen backbone에 경량 adapter로 적응시킨 실용적 연구임</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2610.03119'>How to Find and Reuse Policies for Continuous Adaptation in Lifelong Reinforcement Learning</a></td><td>38</td><td>5</td><td>RL</td><td>Wasserstein task embedding으로 유사도를 추정해 이전에 학습한 policy를 선택·조합하는 lifelong RL 기법(AMSC)으로 robot learning의 지속적 skill 재사용과 연결됨</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2610.03616'>LLA-MPC on Embedded Hardware: Rapid Adaptive Control with Thousands of Parallel Models</a></td><td>38</td><td>5</td><td>RL</td><td>수천 개 후보 모델을 실시간 평가하는 look-back/look-ahead 적응 MPC를 임베디드 F1TENTH에서 검증한 연구로 시뮬레이션에 머물던 기존 기법을 실기로 확장한 수준임.</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2610.02580'>Physical AI Smart Spaces: A Large-Scale Benchmark for Multi-Camera 3D Perception in Smart Spaces</a></td><td>38</td><td>3</td><td>3D Vision</td><td>창고·병원 등 smart space용 대규모 multi-camera 3D 추적 벤치마크로 embodied 환경 인식에 참고 가능함</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2610.03252'>COSMI: COmpositional Synthesis of Multi-object Interactions</a></td><td>38</td><td>3</td><td>3D Vision</td><td>단일 객체 캡처를 조합해 다중 객체 human-object interaction 데이터를 합성 생성하는 방법으로 manipulation 학습 데이터 확보에 참고될 수 있음</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2610.03636'>LoGo: Local-Global Rewards for Consistent Long-Horizon Video Generation</a></td><td>38</td><td>3</td><td>World Model</td><td>카메라 제어 비디오 생성의 3D 일관성을 위해 local·global reward를 결합한 post-training 기법임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2610.02774'>LatticeSMC: Where to Spend Inference-Time Compute in Chunked Sequence Generators</a></td><td>38</td><td>3</td><td>Video</td><td>chunk 단위로 생성되는 음악·모션·비디오에 Feynman-Kac steering을 2차원 lattice로 확장한 inference-time compute 배분 기법으로 test-time planning 우선주제와 연결되나 robot action에는 적용 안 됨</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2610.02320'>DeskForge: Dense Supervision from Desktop Environments for Computer-Use Agents</a></td><td>38</td><td>2</td><td>Multimodal</td><td>컴퓨터 사용 에이전트용 GUI grounding 데이터셋으로 embodied robot과 무관한 digital agent 연구임</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2610.02819'>Text-Centric Post-Training for Omni-Modal Reasoning</a></td><td>38</td><td>2</td><td>Multimodal</td><td>텍스트 전용 post-training만으로 omni 모델의 추론 능력을 56.6% 적은 GPU 시간으로 끌어올린 결과로 멀티모달 학습 전략에 참고될 수 있으나 로봇 도메인과는 거리가 있음.</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2610.03002'>Recursive Self-Improvement in Unified Multimodal Models</a></td><td>38</td><td>2</td><td>Multimodal</td><td>통합 멀티모달 모델이 이미지 생성과 이해를 서로의 학습 데이터로 삼고 프로그램 실행으로 검증하는 recursive self-improvement 루프로 차트 도메인에서 성능을 크게 올렸으나 로봇 도메인 검증은 없음.</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2610.03190'>Not Until the Evidence Says So: Teaching LLM Investigators When to Close a Case</a></td><td>38</td><td>2</td><td>NLP</td><td>증거가 충분할 때만 사건을 종결하도록 LLM investigator를 학습시킨 연구로 로봇의 실패 진단·종결 판단에 개념적으로 참고될 수 있음.</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2610.02687'>Decoupling Memory from Context: Structured Memory for Token-Efficient Test-Time Continual Learning</a></td><td>38</td><td>2</td><td>LG</td><td>메모리 갱신을 context 최적화로 재정의하고 graph 기반 메모리를 제안했으나 robot memory가 아닌 LLM agent 메모리에 적용됨</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2610.03519'>Reasoning Models Are Accurate but Unsound on Identification</a></td><td>38</td><td>2</td><td>NLP</td><td>reasoning model이 식별 불가능한 인과 질의에도 틀린 수식을 제시하는 unsoundness를 형식적으로 검증한 연구로 causal reasoning 평가에 기여하나 robotics 적용은 없음</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2610.02665'>Large Language Continuous Diffusion Models</a></td><td>38</td><td>1</td><td>LG</td><td>이산 대신 연속 ODE/SDE latent로 동작하는 대규모 diffusion 언어모델을 제시해 steering과 distillation에서 구조적 장점을 보이나 적용 영역이 텍스트에 한정됨.</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2610.02372'>Traversing the Satisfaction-Diversity Frontier in Text-to-Image Diffusion</a></td><td>38</td><td>0</td><td>CV</td><td>reward floor와 diversity cutoff를 분리하는 satisficing formulation은 새롭지만 text-to-image 생성에 국한됨</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2610.02702'>Silent Dissent: LLM Agents That Yield to the Majority Still Represent Their Original Premise</a></td><td>36</td><td>2</td><td>NLP</td><td>다수 의견에 굴복한 LLM agent도 내부 표상에는 원래 전제를 유지한다는 것을 Jacobian lens로 보인 해석가능성 연구로 counterfactual reasoning에 참고될 수 있으나 로봇 도메인은 아님.</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2610.02999'>OmniConfess: Eliciting Token Confessions to Mitigate Omni-Modal Hallucination</a></td><td>36</td><td>2</td><td>Multimodal</td><td>응답을 토큰 단위로 재점수화해 어떤 근거에 의존했는지 드러내는 training-free hallucination 완화법으로 VLA의 grounding 문제에 아이디어로 참고될 수 있음.</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2610.03439'>Depth Hypothesis Guided Iterative Refinement for Event-Image Monocular Depth Estimation</a></td><td>35</td><td>3</td><td>3D Vision</td><td>이벤트·이미지 융합으로 depth hypothesis volume 기반 단안 깊이 추정을 반복 정제하는 실시간 가능 연구임</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2610.02982'>PLCWorld: Benchmarking LLM-Generated PLC Programs in Closed-Loop Plant Simulation</a></td><td>35</td><td>3</td><td>Embodied AI</td><td>LLM이 생성한 PLC 프로그램을 closed-loop 공장 시뮬레이션에서 검증하는 벤치마크로 산업 제어 분야의 embodied 평가에 해당함</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2610.02451'>A Simulation-Grounded Agentic VLM Framework for Wildfire Monitoring and Reporting</a></td><td>35</td><td>2</td><td>Multimodal</td><td>시뮬레이션 기반 VLM 멀티에이전트로 산불 모니터링을 수행하며 메모리 활용 방식이 참고할만함</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2610.02513'>From Fragments to Global Maps: Learning Vectorized Map Aggregation with Large Language Models</a></td><td>35</td><td>2</td><td>Navigation</td><td>LLM 기반 vectorized HD map aggregation으로 자율주행 매핑에 기여하나 robot learning 핵심과는 거리가 있음</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2610.02718'>Revisiting Visual Representation Enhancement of VLMs via Kernel Canonical Correlation Analysis</a></td><td>35</td><td>2</td><td>Multimodal</td><td>CLIP의 fine-grained visual representation을 KCCA로 정렬하는 방법으로 범용 VLM 개선에 해당함</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2610.02903'>ViTok: Improving Dense Semantics in AM-RADIO-Style Multi-Teacher Distillation with PHI-S and Masked Image Modelling</a></td><td>35</td><td>2</td><td>CV</td><td>DINOv3·SigLIP2 멀티티처 증류로 dense semantic과 global semantic을 동시에 보존하는 backbone 연구임</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2610.03141'>Behavior Pack Optimization for Video MLLM Post-Training</a></td><td>35</td><td>2</td><td>Video</td><td>counterfactual view 묶음에 대한 일관된 reward로 video MLLM의 시간적 근거 사용을 강제하는 post-training 기법임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2610.03192'>PocketSplat: Mobile Gaussian Reconstruction via World-Space Latent Allocatio</a></td><td>35</td><td>2</td><td>3D Vision</td><td>모바일 기기 예산에 맞춘 feed-forward Gaussian 재구성 방법으로 자원 제약 하 3D 표현에 기여함</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2610.03522'>Feedforward Novel View Synthesis for Heterogeneous Cameras</a></td><td>35</td><td>2</td><td>3D Vision</td><td>fisheye·파노라마 등 이기종 카메라 혼재 상황에서 feed-forward novel view synthesis를 가능하게 한 연구로 multi-sensor 로봇 시스템에 참고될 수 있음</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2610.03691'>FlowHMR: Physically Plausible Motion Capture from Video</a></td><td>35</td><td>2</td><td>CV</td><td>flow matching과 물리 기반 tracking reward의 GRPO 후훈련으로 물리적으로 그럴듯한 human motion capture를 생성함</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2610.02769'>When History Fails to Become Experience: Action Calibration in Language Agents</a></td><td>35</td><td>2</td><td>NLP</td><td>과거 행동-결과 대응을 명시적으로 라벨링하면 language agent의 과제 성공률이 오른다는 결과로 robot memory·failure learning에 아이디어로 참고될 수 있음.</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2610.03102'>Ask, Relax, or Act? Evaluating Actionable Indeterminacy in LLM Preference Reasoning</a></td><td>35</td><td>2</td><td>NLP</td><td>행동·명확화·제약 수정 중 언제 무엇을 해야 하는지 정식화한 actionable indeterminacy 연구로 로봇의 불확실성 하 의사결정에 개념적으로 참고될 수 있음.</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2610.02887'>Revealing Epistemic Uncertainty in MLLMs via Causal-Invariant Masking</a></td><td>35</td><td>1</td><td>Multimodal</td><td>MLLM의 epistemic uncertainty를 causal-invariant masking으로 분리하는 방법으로 범용 신뢰도 추정에 해당함</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2610.02523'>Hypothesis-guided discovery of cognitive algorithms via program refinement</a></td><td>35</td><td>1</td><td>AI</td><td>확률적 프로그램을 LLM으로 개선하는 cognitive algorithm 발견 파이프라인이나 robotics 적용은 없음</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2610.02975'>Reliable Self-Evolution with Imperfect Proxy Rewards</a></td><td>35</td><td>1</td><td>LG</td><td>conformal inference로 calibrated reward interval을 만들어 self-evolving search의 false positive를 줄인 일반화 가능한 기법임</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2610.02557'>How to Have a Sensitive Debate: An Instance-Optimal Protocol for AI Debate</a></td><td>35</td><td>0</td><td>AI</td><td>AI debate 프로토콜의 instance-optimal 보장을 증명한 이론 논문이며 robotics와 무관함</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2610.02945'>Continual Graph Memory for Mathematical Research Agents</a></td><td>35</td><td>0</td><td>NLP</td><td>graph 기반 memory로 장기 수학 연구 agent의 탐색을 재사용하는 시스템으로 성과는 크지만 domain이 수학 연구임</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2610.03025'>Verifiable, Articulable, and Tacit Components of Preference</a></td><td>35</td><td>0</td><td>NLP</td><td>창작 선호의 검증·articulable·tacit 요소를 대규모로 분리 측정한 연구로 RLHF 전반에 함의가 있으나 robotics와는 무관함</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2610.03251'>Learning a Fact Is Not Learning How to Retrieve It</a></td><td>35</td><td>0</td><td>NLP</td><td>사실 학습과 그 인출 능력이 분리됨을 context state로 보인 해석가능성 연구임</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2610.03105'>A Benchmark for Spatially Grounded Gesture Generation</a></td><td>32</td><td>3</td><td>CV</td><td>포인팅 제스처의 공간적 grounding을 평가하는 벤치마크로 HRI의 referential 소통에 관련됨</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2610.03389'>From Patching to Pruning Visual Computation in Vision Language Models</a></td><td>32</td><td>2</td><td>Multimodal</td><td>activation patching을 진단 도구에서 추론 가속 기법으로 전환해 VLM 시각 연산을 레이어별로 생략함</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2610.02545'>Reward Inflation: A Healthy Stimulus for Reinforcement Learning</a></td><td>32</td><td>2</td><td>RL</td><td>reward를 점진적으로 키우는 reward inflation으로 RL plasticity 유지에 도움되나 범용 기법이라 robotics 특화 기여는 아님</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2610.02472'>APDMem: Agent-Controlled Progressive Disclosure for Query-Adaptive Long-Term Memory</a></td><td>32</td><td>2</td><td>NLP</td><td>대화 기록을 네 단계로 점진 공개하며 조회하는 장기 메모리 구조로 robot memory 설계에 참고할 만하나 적용 도메인은 LLM assistant임.</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2610.02981'>Safeguarding Mutual Correction in Source-Free Domain Adaptation via Cut Statistics</a></td><td>32</td><td>2</td><td>CV</td><td>source-free domain adaptation에서 cut statistic으로 상호 보정 방향을 게이팅하는 일반적 기법으로 로봇 인식의 domain shift에도 적용 가능함</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2610.03452'>Causal Representation Learning with Instantaneous and Lagged Relations via Nonstationarity</a></td><td>32</td><td>1</td><td>World Model</td><td>비정상성을 이용해 즉시적·지연적 인과관계를 함께 가진 latent state를 식별하는 causal representation learning 기법(iCReN)으로 world representation 우선주제와 연결되나 robotics 검증은 없음</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2610.02425'>Finding the Move Is Not Winning the Game: XiangqiBench for Closed-Loop Evaluation of LLM Agents</a></td><td>32</td><td>1</td><td>NLP</td><td>장기수 체스에서 수를 맞혀도 게임을 이기지 못하는 closed-loop 평가 격차를 보인 벤치마크로 에이전트 평가 방법론 통찰은 있으나 로봇 도메인과는 무관함.</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2610.02878'>Evaluating VQA in Vision Language Models using Cooperative Principles</a></td><td>32</td><td>1</td><td>Multimodal</td><td>Grice 격률을 어긴 질문에서 VLM 성능이 떨어진다는 결과로 embodied spatial reasoning의 질문 이해에 참고될 수 있으나 로봇 적용은 없음.</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2610.03039'>HyperThink: Text-to-Parameter Hypernetworks for Efficient Reasoning</a></td><td>32</td><td>1</td><td>LG</td><td>긴 추론 과정을 hypernetwork의 파라미터 업데이트 한 번으로 압축하는 효율화 기법으로 경량화 지향이라 우선 평가 대상은 아님.</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2610.02351'>DeReAct: Decomposed Reasoning and Acting for Reliable AI Agents</a></td><td>32</td><td>1</td><td>NLP</td><td>LLM agent의 action 검증과 completion 판단을 분리한 아키텍처 개선이나 robotics와 무관함</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2610.03631'>NeutronGym: Physics-Graded Neutron Instrument Design for LLM Agents</a></td><td>32</td><td>1</td><td>RL</td><td>물리 시뮬레이터로 채점되는 중성자 기기 설계 RL 환경을 구축해 agent 성능을 11%에서 77%로 끌어올린 연구로 과학 설계용 RL 환경 패러다임을 보여주나 robotics는 아님</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2610.02588'>Open-Endedness Bench: Measuring Epistemic Process from Agent Records</a></td><td>32</td><td>0</td><td>AI</td><td>agent의 가설-검증-수정 과정을 실행 기록만으로 평가하는 벤치마크 방법론이나 robotics 적용은 없음</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2610.02694'>Who Went Where When on the Lunar Surface: Forensic Trajectory Analysis to Identify Byzantine Rovers</a></td><td>30</td><td>4</td><td>Robotics</td><td>행성 탐사 로버의 악의적 trajectory 식별 문제로 흥미롭지만 로봇러닝 우선 주제와는 무관한 niche multi-agent 보안 문제임.</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2610.03283'>HexVIO: Towards All-Day Stereo-Inertial Tracking Through Commodity DSPs</a></td><td>30</td><td>4</td><td>Navigation</td><td>VIO 프론트엔드를 스마트폰 DSP로 오프로드해 전력을 67% 절감한 하드웨어 최적화 기여로 로봇러닝 핵심 주제와는 거리가 있음.</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2610.03065'>Learning Transferable Policies from Action-free Time Series Through Dynamical Embeddings</a></td><td>30</td><td>3</td><td>RL</td><td>action-free 시계열에서 시스템 간 공유 동역학을 임베딩으로 학습해 제어 정책을 전이하는 계층적 model-based RL로 Lorenz·이중진자 등 비로봇 시스템에서만 검증됨</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2610.02740'>Prospective Hindsight: Self-Calibrating Reinforcement Learning via Prediction-Reality Gaps</a></td><td>30</td><td>2</td><td>RL</td><td>prospective prediction과 retrospective 평가의 차이로 surprise 신호를 만들어 policy gradient를 보정하는 self-calibration 기법으로 범용 agent 학습에 적용되나 robot 실험은 없음</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2610.03372'>SCAD: Structured Credit Assignment and Distillation for Long-Horizon Agents</a></td><td>30</td><td>2</td><td>RL</td><td>planning과 subtask 실행을 분리해 교차 rollout으로 credit을 정교화하는 장기 호라이즌 에이전트 학습 기법(SCAD)으로 skill chaining 우선주제와 맞닿아 있으나 로봇 실험은 없음</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2610.03356'>ReFract: Benchmarking Perspective Awareness in Language Model Agents with Text World Models</a></td><td>30</td><td>2</td><td>Embodied AI</td><td>산업 설비 유지보수 상황에서 사용자 역할에 맞춰 행동을 조정하는 perspective awareness 벤치마크임</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2610.02507'>MeshQuery: Agentic Seam Planning for UV Parametrization</a></td><td>30</td><td>1</td><td>CV</td><td>training-free VLM 에이전트로 UV seam을 계획하는 그래픽스 도구 연구임</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2610.02753'>Correcting Guided Diffusion Trajectories with Spectral Alignment</a></td><td>30</td><td>1</td><td>CV</td><td>classifier-free guidance 궤적을 spectral alignment로 보정하는 training-free 이미지 생성 기법임</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2610.02779'>TRAC: Trajectory-aware Reuse and Adaptive Correction for Efficient Autoregressive Video Generation</a></td><td>30</td><td>1</td><td>Video</td><td>autoregressive 비디오 생성의 캐싱과 보정을 결합한 효율화 기법으로 robotics 적용은 없음</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2610.02959'>TerraVis: Towards Evaluation of World-Grounded Visual Consistency in Text-to-Image Generation via MLLM Workflows</a></td><td>30</td><td>1</td><td>CV</td><td>텍스트-이미지 생성의 world-grounded 시각적 일관성을 평가하는 MLLM 기반 metric 연구임</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2610.03400'>Beyond Entropy: Self-Diagnostic Multi-Role Token Optimization for Video Reasoning</a></td><td>30</td><td>1</td><td>Video</td><td>video reasoning RL에서 모델 자신의 성공·실패 rollout으로부터 동적 counterfactual 신호를 도출하는 token 수준 credit assignment 기법임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2610.03698'>Decoding the Functional Roles of Register and High-Norm Patch Tokens in Vision Transformers</a></td><td>30</td><td>1</td><td>CV</td><td>DINOv2의 register token과 high-norm outlier token의 기능적 역할을 sparse autoencoder로 분리한 해석가능성 연구임</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2610.02267'>Fast Models, Slow Evidence: A Paired and Self-Audited Evaluation of System-1 Decision Models for LLM Agent Harnesses</a></td><td>30</td><td>1</td><td>NLP</td><td>에이전트 하네스용 System-1 결정모델을 자기감사까지 거쳐 재평가하며 기존 배포 주장의 분석 오류를 드러낸 rigorous한 재현 연구로 평가방법론적 가치는 있으나 로봇 도메인은 아님.</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2610.03363'>Geometry Meets Physics: Data-Efficient Pre-Training for Unstructured Neural PDE Solvers</a></td><td>30</td><td>1</td><td>3D Vision</td><td>비정형 3D 기하 PDE solver를 위한 데이터 효율적 사전학습 기법으로 물리 시뮬레이션에 한정됨</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2610.03258'>Mapping and Advancing the Scalability-Accuracy Frontier of Nonlinear Causal Discovery</a></td><td>30</td><td>0</td><td>LG</td><td>비선형 causal discovery의 정확도-속도 trade-off를 분석하고 spline 기반 SPADE로 확장성을 크게 높인 causal reasoning 도구 연구임</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2610.03052'>The Geometry of Knowledge Accessibility in Large Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>질의가 지식 접근 가능 중심에서 멀수록 회상이 어려워진다는 기하학적 구조를 밝힌 해석가능성 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2610.03109'>Emergent Structure in the Marginal Attention Space of Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>post-softmax attention을 marginalize해 KV 캐시 예산 배분에 활용한 해석가능성 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2610.02428'>Autonomous mobile robot operations logistics: a dataset of jobs, dispatch events and robot states</a></td><td>28</td><td>4</td><td>Robotics</td><td>AMR 운영 로그 데이터셋 공개가 핵심으로 새로운 방법론 없이 benchmark 자원 제공에 그침.</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2610.02469'>RUL-Aware RRT*: Degradation-Balanced Motion Planning for Robotic Manipulators</a></td><td>28</td><td>4</td><td>Manipulation</td><td>관절 잔여수명을 모션플래닝에 반영한 RRT* 변형으로 아이디어는 실용적이나 로봇러닝 핵심 주제와는 거리가 있는 점진적 엔지니어링임.</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2610.03093'>LS-AR: Future-Predictive Latent Steering in Autoregressive LLMs</a></td><td>28</td><td>2</td><td>NLP</td><td>FiLM 조건화로 macro-objective와 token decoding을 분리한 dual-channel AR 아키텍처로 Blocksworld planning에서 평가했으나 텍스트 에이전트에 한정됨</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2610.03454'>Measure Less, Know More: Self-Supervised Test-Time Feature Acquisition</a></td><td>28</td><td>2</td><td>Multimodal</td><td>foundation model의 내부 표현을 proxy target으로 써서 어떤 modality를 측정할지 RL로 순차 선택하는 test-time feature acquisition 기법임</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2610.03510'>Weave Forcing: Compositional Memory Routing for Interactive Long Video Generation</a></td><td>28</td><td>1</td><td>Video</td><td>LLM 기반 semantic slot routing으로 장편 비디오 생성에서 캐릭터·배경 메모리를 선택적으로 재사용하는 training-free 기법임</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2610.02410'>Efficient Neural Field Learning via Adaptive Coverage and Focused Sampling</a></td><td>28</td><td>1</td><td>LG</td><td>implicit neural representation 학습을 coverage와 importance를 분리해 가속하는 적응적 샘플링 기법임</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2610.02695'>Test-time Calibration Learning for Large Language Model Reasoning</a></td><td>28</td><td>1</td><td>NLP</td><td>label 없이 test-time에 LLM reasoning의 정확도와 calibration을 동시에 개선하는 기법으로 test-time optimization 원리는 있으나 robotics 적용은 없음</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2610.03012'>Rethinking Fixed Temporal Grids: Frequency-Disentangled Motion Generation</a></td><td>28</td><td>0</td><td>CV</td><td>모션 생성을 주파수 대역으로 분해하는 scale-adaptive motion representation 연구임</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2610.03202'>Contextual Flow Matching: Adaptive Step Selection in Flow Models for Efficient Visual Generation</a></td><td>28</td><td>0</td><td>CV</td><td>flow matching의 denoising step 수를 입력에 맞춰 적응적으로 선택하는 추론 가속 기법임</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2610.02616'>VERSE: Verified Self-Evolving Optimizer for Agent Harnesses</a></td><td>28</td><td>0</td><td>NLP</td><td>agent harness를 검증 기반으로 self-evolve시키는 최적화 기법으로 SWE 작업에 한정됨</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2610.02793'>PAPER2LLM++: Continual Self-Evolution of LLMs from Research Papers</a></td><td>28</td><td>0</td><td>LG</td><td>연구 논문에서 발견된 모델 한계를 지속적으로 학습에 반영하는 self-evolution 프레임워크임</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2610.02808'>ROUTEAUDIT: Interaction-Aware Identification for Budgeted Multi-Verifier Routing</a></td><td>28</td><td>0</td><td>LG</td><td>verifier routing을 contract-conditioned identification 문제로 정식화한 방법론 논문임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2610.03055'>hacktrace: behavior-supervised detection of reward hacking during code generation</a></td><td>28</td><td>0</td><td>LG</td><td>코드 생성에서 reward hacking을 행동 기반으로 탐지하는 모니터링 기법임</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2610.03634'>Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents</a></td><td>28</td><td>0</td><td>LG</td><td>명령어 간 read-write 의존성 그래프로 credit assignment를 수행하는 terminal agent RL 기법임</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2610.02835'>All Work And No Play Makes Jack a Dull Boy: Understanding and Preventing Catastrophic Strategy Collapse in RLVR</a></td><td>27</td><td>1</td><td>NLP</td><td>RLVR 후반부에 전략 다양성이 붕괴하는 현상을 정보이론으로 분석하고 Mesh Learning으로 방지한 LLM RL 연구임</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2610.03085'>Light Entropic Optimal Transport on Riemannian Manifolds</a></td><td>25</td><td>3</td><td>LG</td><td>구면·SO(3)·SE(3) 등 매니폴드 위에서 닫힌 형태로 샘플링 가능한 entropic optimal transport를 제시해 robot pose 표현에 쓰일 수 있는 범용 도구이나 robotics 실험은 없음</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2610.02497'>LiteEMG-FM: An Efficient and Deployable Foundation Model for Robust EMG Sensing</a></td><td>25</td><td>2</td><td>LG</td><td>다양한 EMG 데이터셋으로 사전학습한 경량 웨어러블 foundation model로 HCI·보조기기에 활용 가능함</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2610.02957'>Understanding Trajectory Heterogeneity in Federated World Model Learning</a></td><td>25</td><td>2</td><td>World Model</td><td>임상 코호트에 대한 federated world model 학습에서 trajectory 소유권 제약이 장기 예측 커버리지를 제한함을 보인 벤치마크 연구로 world model이라는 용어는 쓰이나 embodied robotics와는 무관함</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2610.03036'>WebFovea: When the Model Is Right but the Click Is Wrong -- Reliable Round Trips for Vision-Based Web Agents on Live Websites</a></td><td>25</td><td>2</td><td>Embodied AI</td><td>vision 기반 웹 에이전트가 모델의 reasoning이 아니라 harness 단계에서 실패하는 지점을 분석하고 고친 엔지니어링 보고서임</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2610.02364'>Confidence-Controlled XAI Auditing for Pedestrian Detection under Domain Shift</a></td><td>25</td><td>1</td><td>CV</td><td>보행자 탐지 XAI의 confidence 보정 문제를 다룬 안전성 감사 연구로 robot learning과 거리가 있음</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2610.02382'>FactorSplat: Appearance-Controllable Gaussian Proxies for Medical Volume Rendering</a></td><td>25</td><td>1</td><td>3D Vision</td><td>의료 볼륨 렌더링용 Gaussian splatting으로 transfer function 제어를 다룬 응용 연구임</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2610.02567'>DAGS: Disentangled Appearance-and-Geometry Steering of a Frozen Image DiT for Temporally Stabilized Generative Rendering</a></td><td>25</td><td>1</td><td>CV</td><td>frozen diffusion transformer로 temporally stable한 generative rendering을 수행하는 그래픽스 연구임</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2610.02943'>Kinematics-Induced Multimodal 3D Human Pose Estimation with Subject-Level Privacy</a></td><td>25</td><td>1</td><td>CV</td><td>RGB·LiDAR·mmWave 융합 3D human pose estimation에 subject-level 프라이버시 감사를 결합한 연구임</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2610.02946'>When Predicting Nothing Beats SAM 3: Revisiting Evaluation in Video Object Segmentation</a></td><td>25</td><td>1</td><td>CV</td><td>희소 가시성 조건에서 VOS 평가지표의 결함을 지적하고 새 metric을 제안한 벤치마크 연구임</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2610.03099'>Beyond Single Videos: Benchmarking and Active Evidence Seeking for E-Commerce Cross-Video Reasoning</a></td><td>25</td><td>1</td><td>Multimodal</td><td>전자상거래 cross-video reasoning을 위한 agentic 증거 탐색 프레임워크로 능동적 tool 사용 방식이 참고할만함</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2610.03370'>LAS-CLIP: A Lightweight Adapter Steering Approach for CLIP&#x27;s Visual Encoder</a></td><td>25</td><td>1</td><td>Multimodal</td><td>CLIP을 고정한 채 경량 adapter로 region-level attention을 유도하는 효율적 steering 기법임</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2610.03445'>Corrupted but Correct: Why Vision-Language Models Lie to Themselves Internally</a></td><td>25</td><td>1</td><td>Multimodal</td><td>적대적 섭동에도 VLM이 자유생성 시 정답을 내는 train/inference gap을 메커니즘 수준에서 분석한 연구임</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2610.02399'>VisAudit: Evaluating Multimodal Agents for Visual Diagnosis and Repair</a></td><td>25</td><td>1</td><td>Multimodal</td><td>멀티모달 에이전트가 시각화 오류를 진단·수정·검증하는 벤치마크로 자가진단 루프 구조가 failure detection과 유사함</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2610.02520'>Instance-Dependent Regret for CMDPs with Step-Wise Constraints</a></td><td>25</td><td>1</td><td>RL</td><td>step-wise constraint가 있는 CMDP regret bound 이론 연구로 robotics 적용 사례 없음</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2610.02960'>Dirac-Interconnected Neural Elements: Discovering Modularity in Physical Systems Without Reduction</a></td><td>25</td><td>1</td><td>LG</td><td>물리 시스템의 상호연결을 Dirac structure로 학습해 reduction 없이 모듈을 재구성하는 신경망 모델임</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2610.03092'>ULTRADISCOVERY: Abductive Exploration in an Interconnected, Epistemically Open Universe</a></td><td>25</td><td>1</td><td>LG</td><td>표상이 열려 있고 증거가 흩어진 세계에서 abductive exploration 능력을 측정한 LLM agent 벤치마크임</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2610.02664'>A GHOST in Long-Horizon Agents: Governance Hazard from Overlooked Safety Constraints across Turns</a></td><td>25</td><td>1</td><td>AI</td><td>long-horizon agent가 이전 턴의 안전 제약을 잊는 governance hazard를 정의하고 방어책을 제안했으나 대상이 LLM agent임</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2610.02867'>TACD: Distilling Efficient Text-to-Motion Models via Terminal Amplification Control</a></td><td>25</td><td>1</td><td>Video</td><td>text-to-motion 모델을 few-step으로 distill하는 효율화 연구로 인간 모션 생성에 국한되고 로봇 제어는 아님</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2610.02897'>Interpreting at Write Time: A Policy Ablation for Multi-Goal Agent Memory</a></td><td>25</td><td>1</td><td>NLP</td><td>다중 목표를 가진 assistant 메모리 요약 정책을 비교한 ablation 연구로 robot memory는 아님</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2610.03273'>EVOL: Simulator-Guided Evolutionary Expert Synthesis for Deployment-Free Learning Path Recommendation</a></td><td>25</td><td>1</td><td>RL</td><td>로보틱스의 simulator 기반 demonstration learning 기법을 학습경로 추천에 차용했으나 적용 domain은 교육임</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2610.02914'>Custom Forcing: Training-Free Subject Customization for Autoregressive Video Generation</a></td><td>25</td><td>0</td><td>Video</td><td>frozen autoregressive 비디오 모델에 KV 캐시 기반 subject customization을 더한 생성 기법임</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2610.02967'>Post-Training Frontier Text-to-Image Models by Composing Preference and Rubric Rewards</a></td><td>25</td><td>0</td><td>CV</td><td>preference reward와 rubric reward를 결합해 T2I 모델을 post-training하는 생성 모델 연구임</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2610.03167'>Geometry-Aligned Semantic Matching for Cross-Modal Planar Image Registration</a></td><td>25</td><td>0</td><td>CV</td><td>DINOv3 기반 cross-modal planar image registration으로 기하학적 대응을 개선한 연구임</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2610.03221'>VDOT++: Unified Few-Step Video Generation via Unbalanced Optimal Transport Distillation</a></td><td>25</td><td>0</td><td>Video</td><td>unbalanced optimal transport로 few-step 비디오 생성을 안정화한 distillation 기법임</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2610.02283'>MuLoRA: Spectrally Balanced Low-Rank Adaptation for Continual Learning</a></td><td>25</td><td>0</td><td>LG</td><td>지속학습에서 LoRA의 spectral plasticity collapse를 해결하는 적응 용량 배분 기법임</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2610.02324'>Slow-Fast Multi-Teacher On-Policy Distillation for Capability Preservation</a></td><td>25</td><td>0</td><td>Multimodal</td><td>멀티모달 LLM의 멀티티처 증류에서 일반 능력 저하를 slow-fast 모델로 완화하는 기법임</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2610.02345'>Mitigating Convergence Collapse in Fixed-Target Anomaly Detectors via Kernel-Anchored Locality Regularization</a></td><td>25</td><td>0</td><td>LG</td><td>fixed-target 이상탐지기의 수렴 붕괴를 kernel 기반 locality 정규화로 해결한 연구임</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2610.02614'>What Is Lost in Post-Training? Default Collapse and the Loss of In-Context Steerability Across Diverse Perspectives</a></td><td>25</td><td>0</td><td>NLP</td><td>post-training이 LLM의 in-context steerability를 떨어뜨리는 default collapse 현상을 분석한 alignment 연구임</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2610.02856'>Adaptive Mutual Distillation for Balanced Multi-Task Post-Training of Large Language Models</a></td><td>25</td><td>0</td><td>LG</td><td>서로 다른 task-balancing 전략의 모델끼리 상호 증류하는 다중과제 post-training 기법으로 로봇러닝과 무관함.</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2610.02300'>Keep It CALM: Analyzing the Limits of Global Unsafety in Text-to-Image Generation</a></td><td>25</td><td>0</td><td>AI</td><td>text-to-image 안전장치의 coverage-selectivity trade-off를 분석하고 지역적 counterfactual 보정을 제안한 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2610.02405'>When Terminal-Agent Training Stalls: Demystifying Data Generation and Verification Challenge</a></td><td>25</td><td>0</td><td>NLP</td><td>terminal agent RL 학습 파이프라인의 실패 원인을 진단한 분석 논문임</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2610.02480'>MEA: A Reward-Driven Multi-Agent System for Faithful Model Explanations</a></td><td>25</td><td>0</td><td>Multimodal</td><td>모델 설명을 위한 multi-agent 프레임워크로 robotics와 무관함</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2610.02491'>What Does a Token Cost? A Mixture-of-Agents Measurement of Sufficient Per-Token Compute</a></td><td>25</td><td>0</td><td>LG</td><td>토큰별 필요 연산량을 측정한 효율화 연구로 우선순위가 낮은 efficiency 주제임</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2610.02568'>Mitigating Social Sycophancy via Pluralistic Preference Optimization</a></td><td>25</td><td>0</td><td>NLP</td><td>다중 이해관계자 관점을 반영해 사회적 아첨을 줄이는 선호 최적화로 robotics와 무관함</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2610.02638'>Batched Speech Decisions Without Decoding: Single-Token Supervision Lets a Frozen LLM Hear Beyond the Transcript</a></td><td>25</td><td>0</td><td>Multimodal</td><td>음성 agent의 단일 토큰 결정으로 디코딩을 생략하는 효율화 기법으로 robotics와 무관함</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2610.02684'>Large language models exhibit unreliable updating of clinical judgment as patient evidence evolves</a></td><td>25</td><td>0</td><td>NLP</td><td>환자 증거 변화에 따른 LLM 임상 판단 갱신의 신뢰성 부족을 분석한 연구임</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2610.02792'>Law And Order: Tax Law Autoformalization</a></td><td>25</td><td>0</td><td>NLP</td><td>세법 문서를 실행 가능한 기호 프로그램으로 변환하는 neuro-symbolic 프레임워크임</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2610.02824'>MetaRubric: Learning to Reward for Rubric-Based Reinforcement Learning</a></td><td>25</td><td>0</td><td>NLP</td><td>rubric 기반 RL에서 vacuous credit 문제를 교정한 의료 QA RL 기법임</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2610.02826'>Scaling Trajectories for Complex Tasks through Recursive Self-Rewrite</a></td><td>25</td><td>0</td><td>NLP</td><td>성공한 terminal agent 궤적을 일반 harness용으로 재구성하는 학습 데이터 증강 기법임</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2610.02831'>AMBER: Multi-View Adaptive Budget Allocation for Listwise Vision-Language Reranking</a></td><td>25</td><td>0</td><td>Multimodal</td><td>VLM listwise reranking의 예산 배분을 Elo 업데이트로 최적화한 검색 효율화 기법임</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2610.02853'>Bounded Reachability &amp; Jailbreak Detection via Contraction-Constrained State Space Models</a></td><td>25</td><td>0</td><td>LG</td><td>state space model 기반 safety head의 형식적 강건성 조건을 증명한 이론 연구임</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2610.02858'>Harness-Aware Distillation for Small Language Model Agents</a></td><td>25</td><td>0</td><td>NLP</td><td>harness 정보를 제외한 teacher 고유 기여만 distill하는 agent 경량화 기법임</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2610.02902'>LUMOS: Tracing Parametric Knowledge from Training Data to Behavioral Outputs in LLMs</a></td><td>25</td><td>0</td><td>NLP</td><td>학습 데이터 노출과 behavioral output을 인과적으로 추적한 지식 진단 프레임워크임</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2610.02976'>Relevant Evidence Decoding for Audio-Visual Hallucination Mitigation</a></td><td>25</td><td>0</td><td>Multimodal</td><td>질문에 필요한 modality 증거를 PMI로 식별해 audio-visual hallucination을 줄인 training-free 디코딩 기법임</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2610.03020'>DyadMem: A Long-Term Memory Benchmark of How Agents Work with Users</a></td><td>25</td><td>0</td><td>NLP</td><td>사용자별 관계적 agent 메모리를 평가하는 장기 기억 벤치마크임</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2610.03056'>MOF-VERIFY: A Failure-Aware Agentic Harness for MOF Hypothesis Verification</a></td><td>25</td><td>0</td><td>AI</td><td>MOF 가설 검증을 위한 failure-aware agentic harness로 재료과학 도메인에 한정됨</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2610.03185'>Gains and Collapse in On-Policy Distillation:A Reinforcement Learning Perspective</a></td><td>25</td><td>0</td><td>NLP</td><td>on-policy distillation의 성능 향상과 붕괴를 teacher의 암묵적 보상 관점에서 설명한 분석 연구임</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2610.03316'>Multi-Task Evolution for Zero-Shot Cross-Problem Generalization using LLMs</a></td><td>25</td><td>0</td><td>LG</td><td>LLM 기반 진화적 휴리스틱을 조합최적화 문제 간 zero-shot 전이시키는 프레임워크임</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2610.03458'>A Near-Zero Monitor Readout Is Not Evidence of Behavioral Control</a></td><td>25</td><td>0</td><td>LG</td><td>monitor 점수가 낮아도 행동 통제가 보장되지 않음을 보인 reward hacking 분석 연구임</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2610.03509'>Efficient Reasoning Training Does Not Always Harm CoT Faithfulness and Monitorability</a></td><td>25</td><td>0</td><td>NLP</td><td>효율적 추론 학습이 CoT 충실성과 모니터링 가능성에 미치는 영향을 분석한 연구임</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2610.03548'>Recursive Harness Self-Improvement for Frontier Reasoning Data Synthesis</a></td><td>25</td><td>0</td><td>LG</td><td>task와 harness를 함께 진화시켜 더 어려운 추론 학습 데이터를 합성하는 기법임</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2610.02668'>A Passive AI System for Verifying Physical State on Automated Liquid Handlers</a></td><td>24</td><td>3</td><td>CV</td><td>액체 핸들러 deck 세팅 검증용 수동 비전 시스템으로 실용적이나 연구적 novelty는 제한적임.</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2610.02991'>Subject-Specific Predictive Musculoskeletal Simulations of Lower-Limb Exoskeleton Assistance: Metabolic and Biomechanical Effects of Joint Assistance Strategies</a></td><td>24</td><td>3</td><td>Robotics</td><td>하지 외골격 보조 전략의 대사 효과를 근골격 시뮬레이션으로 분석한 연구로 로봇러닝 주제와는 무관한 biomechanics 기여임.</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2610.02739'>Beyond Correctness: Resolving Underspecification in Agentic Text-to-SQL</a></td><td>24</td><td>1</td><td>NLP</td><td>text-to-SQL 에이전트가 모호성 해소 질문을 섣불리 중단하는 문제를 다룬 연구로 로봇 과제의 명확화 전략에 참고는 되나 도메인은 SQL임.</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2610.03289'>Architecture-Dependent Fusion Pathways in MLLMs</a></td><td>24</td><td>0</td><td>Multimodal</td><td>concatenation과 native 멀티모달 아키텍처의 fusion 경로 차이를 기계적으로 분석한 해석 연구임</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2610.03468'>A Vision-Language Model (VLM)-based Pipeline for End-to-End Procedural Modeling of Field-Grown Maize from Point Clouds</a></td><td>22</td><td>1</td><td>3D Vision</td><td>포인트클라우드로부터 옥수수 procedural 3D 모델을 VLM 주석으로 자동 생성하는 농업 응용 연구임</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2610.02846'>Understanding Enrichment in Reinforcement Learning</a></td><td>22</td><td>1</td><td>RL</td><td>sparse reward에서 hint로 생성한 rollout의 importance weight 보정 효과를 분석한 RLVR 이론 연구임</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2610.03662'>Forecasting from Counterfactual Simulator Rollouts: A Sim2Real Evaluation</a></td><td>22</td><td>1</td><td>LG</td><td>새 정책의 반사실 시뮬레이션 rollout으로 cold-start 수요예측을 학습하고 실제 배치 데이터로 보정하는 sim2real 연구로 재고관리 도메인에 한정됨</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2610.03423'>OuroReward: Sequential Reward Scheduling for Reinforcement Learning in Text-to-3D Generation</a></td><td>22</td><td>0</td><td>3D Vision</td><td>text-to-3D RL에서 보상 차원 간 간섭을 줄이는 순차적 reward scheduling 기법임</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2610.03543'>DuoMatching: Joint-Marginal Distribution Matching for Few-Step Video Generation</a></td><td>22</td><td>0</td><td>Video</td><td>joint-marginal distribution matching으로 few-step 비디오 생성 품질을 높인 distillation 기법임</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2610.02251'>Rank-Aware Speculative Sampling for Diffusion Draft Trees</a></td><td>22</td><td>0</td><td>LG</td><td>diffusion draft tree의 rank 기반 speculative sampling으로 생성 가속을 개선한 효율화 연구임</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2610.02593'>Fisher-Guided Submodular Data Selection for Continual Pre-Training of Large Language Models</a></td><td>22</td><td>0</td><td>LG</td><td>continual pretraining에서 forgetting을 줄이는 Fisher 기반 data selection 기법으로 LLM 학습 효율화에 한정됨</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2610.02700'>Learning from Evolving Errors: Adaptive Iterative Repair for On-Policy Distillation</a></td><td>22</td><td>0</td><td>NLP</td><td>on-policy self-distillation에서 오류별 repair guidance를 반복 제공하는 수학 추론 학습 기법임</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2610.02864'>NeuroLens: Learning Latent Embeddings of Neural Semantics from Chronic Recordings</a></td><td>22</td><td>0</td><td>CV</td><td>만성 신경 기록에서 표상 가소성과 기록 불안정성을 분리하는 JEPA 기반 모델로 neuroscience 응용 연구임</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2610.03502'>Certified Mechanistic Edits: Behavioral Guarantees for Skill Removal and Preservation</a></td><td>22</td><td>0</td><td>LG</td><td>회로를 비활성화해 특정 skill만 제거되고 다른 skill은 보존됨을 continuous 입력 영역 전체에서 증명하는 인증 가능한 모델 편집 연구임</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2610.02444'>Counterexample Generation via Per-Theorem Symbolic Verifiers: When Imitation Hurts and Reinforcement Repairs</a></td><td>22</td><td>0</td><td>NLP</td><td>반례 생성 SFT가 정리 인식 능력을 붕괴시키고 RLVR가 이를 복구한다는 수학 추론 연구로 로봇러닝과는 거리가 멂.</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2610.03063'>HARPO: Hallucination-Aware Reinforcement Learning for Faithful and Creative Language Generation</a></td><td>22</td><td>0</td><td>NLP</td><td>환각 인식 보상모델로 충실성과 창의성을 동시에 최적화하는 RL 기법으로 로봇러닝과 무관함.</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2610.02586'>Labels Override Definitions in Jev-Style Typed Decision Models</a></td><td>22</td><td>0</td><td>NLP</td><td>typed decision model이 정의 대신 라벨 이름에 의존하는 편향을 분석한 연구임</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2610.02654'>Coherence-Driven Belief Formation and Population Dynamics of Contagion in LLM Agents</a></td><td>22</td><td>0</td><td>Multimodal</td><td>LLM agent 집단에서 신념 확산 동역학을 측정한 사회적 전염 연구임</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2610.02678'>Spend Teacher Tokens Where They Matter: Success-Referenced On-Policy Distillation</a></td><td>22</td><td>0</td><td>NLP</td><td>성공 rollout을 참조해 teacher 감독을 선택적으로 배분하는 distillation 효율화 기법임</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2610.02703'>Learning to Revise Reasoning with Segment-wise On-Policy Distillation</a></td><td>22</td><td>0</td><td>NLP</td><td>teacher가 재작성한 추론 구간으로 학생을 학습시키는 segment-wise distillation 기법임</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2610.02762'>Dynamic LLM Routers are Often Misguided</a></td><td>22</td><td>0</td><td>LG</td><td>상용 LLM 라우터가 무작위 라우팅보다 못하다는 부정적 결과를 보인 분석 연구임</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2610.02828'>FSPO: Policy-Consistent Risk and Pareto-Feasible Control for Budgeted LLM RL Post-Training</a></td><td>22</td><td>0</td><td>LG</td><td>예산 제약 하 LLM RL post-training 액추에이터 제어 기법으로 robotics와 무관함</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2610.02844'>DNAlign: Dynamic Null-Space Safe Alignment for LLMs</a></td><td>22</td><td>0</td><td>NLP</td><td>null-space projection으로 안전성과 효용의 trade-off를 완화한 정렬 기법임</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2610.02885'>PsyEvo: A Personalized Counseling Agent That Self-Evolves at Test Time</a></td><td>22</td><td>0</td><td>NLP</td><td>test-time에 개인화되는 LLM 상담 agent 프레임워크임</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2610.02925'>Positive-Unlabeled Learning for Agent Safety False Alarm Auditing</a></td><td>22</td><td>0</td><td>LG</td><td>safety monitor의 false alarm을 positive-unlabeled 학습으로 감사하는 기법임</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2610.03296'>JOVE: Joint Execution and Verification for Resource-Aware LLM Task Graphs</a></td><td>22</td><td>0</td><td>LG</td><td>LLM task graph의 executor 배정과 유료 검증을 온라인으로 균형잡는 프레임워크임</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2610.03315'>Lightweight, Rubric-Guided Trajectory Evaluation for Production AI Agents</a></td><td>22</td><td>0</td><td>NLP</td><td>production LLM agent의 경량 trajectory 평가 아키텍처로 로봇 trajectory가 아님</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2610.03320'>Refinement Buys Intelligibility, Search Buys Identity: What Test-Time Compute Buys in Masked-Diffusion TTS</a></td><td>22</td><td>0</td><td>NLP</td><td>masked-diffusion TTS에서 test-time compute가 명료도와 화자 정체성에 비대칭으로 작용함을 보인 분석 연구임</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2610.03326'>Preserving Mathematical Reasoning in Compressed Diffusion Language Models via Trajectory-Aware Low-Rank Approximation</a></td><td>22</td><td>0</td><td>LG</td><td>diffusion LM 압축 시 trajectory 분포를 고려한 calibration으로 수학 추론 성능을 보존하는 기법임</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2610.03430'>Jumping the Line: Exploiting Length Predictions in LLM Scheduling</a></td><td>22</td><td>0</td><td>LG</td><td>LLM 서빙 스케줄러의 길이 예측을 속이는 적대적 공격 기법임</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2610.03591'>HazardWeaver: Scientific Route Selection for Hazard Analysis Agents</a></td><td>22</td><td>0</td><td>AI</td><td>자연재해 분석을 위해 과학적 방법론 경로를 선택하는 agent 프레임워크임</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2610.02670'>LEAP: Learning Efficient Action Proposals For LLM Agents</a></td><td>20</td><td>1</td><td>NLP</td><td>LLM agent의 action 단계를 speculative decoding으로 가속하는 LEAP 기법으로 robot action이 아닌 LLM agent rollout에 한정됨</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2610.02906'>Tangent Schrödinger Bridge Matching: Learning Stochastic Transport with Mechanistic Sensitivities</a></td><td>20</td><td>1</td><td>LG</td><td>파라미터 민감도를 함께 학습하는 Tangent Schrödinger Bridge Matching으로 Navier-Stokes 등 물리 시스템 개입 반응을 예측하는 연구임</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2610.03001'>Neural Data Needs Semantic Tokenization: Behavioral Events as Boundaries of Session-Transferable Tokens</a></td><td>20</td><td>1</td><td>CV</td><td>behavioral event를 경계로 신경 집단 활동을 토큰화해 세션 간 전이를 가능케 한 neural tokenizer 연구임</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2610.03165'>Sample complexity of variance-reduced policy gradient: weaker assumptions and lower bounds</a></td><td>20</td><td>1</td><td>RL</td><td>variance-reduced policy gradient의 표본복잡도 하한과 defensive importance sampling 알고리즘을 제시한 이론 연구임</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2610.03223'>AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning</a></td><td>20</td><td>1</td><td>RL</td><td>step-level advantage의 신뢰도를 분산 비율로 조정하는 credit assignment 기법으로 ALFWorld 등 텍스트 embodied 환경에서 검증됨</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2610.03361'>Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT</a></td><td>20</td><td>1</td><td>RL</td><td>critic 없이 cross-entropy method로 GRPO를 대체하는 보수적 정책 개선 알고리즘(FTW)임</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2610.03475'>Single or Multiple Policies for Phase-Structured Reinforcement Learning?</a></td><td>20</td><td>1</td><td>RL</td><td>phase 구조를 가진 RL에서 단일 정책과 다중 정책 중 무엇이 나은지 분석한 이론·실험 연구임</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2610.03383'>CVE2AP: Automated Generation of PDDL-Encoded Attack Paths via Large Language Models</a></td><td>20</td><td>1</td><td>AI</td><td>CVE 설명을 PDDL 공격 경로로 자동 변환하는 기법으로 PDDL을 쓰지만 도메인은 사이버보안임</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2610.03570'>Learning to Assess Heartbeat Observability for mmWave Heart-Rate Sensing</a></td><td>20</td><td>1</td><td>CV</td><td>mmWave 레이더로 심박 관측 가능성을 평가하는 센싱 기법으로 robotics 지각과는 거리가 있음</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2610.02375'>EviDent-CBCT: Evidence-Bottlenecked Report Generation from Dental CBCT under Non-Exhaustive Report Supervision</a></td><td>20</td><td>0</td><td>NLP</td><td>치과 CBCT 리포트 생성을 위한 evidence-bottleneck 프레임워크로 의료 NLP 분야 기여임</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2610.02880'>Found but Not Read: When Extracted Text Closes the Retrieval-Reading Gap in Document Vision-Language Models</a></td><td>20</td><td>0</td><td>Multimodal</td><td>문서 VLM에서 검색된 증거를 읽지 못하는 retrieval-reading gap을 분석한 연구로 robotics와 무관함</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2610.03068'>Where to Look Is Not How to Fix: Pre-Denoising Diagnostics and Modality-Dependent Control in Diffusion Composition</a></td><td>20</td><td>0</td><td>CV</td><td>text-to-image 합성 실패의 진단 위치와 교정 위치가 다르다는 diffusion composition 분석 연구임</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2610.03218'>VisionMX: Unlocking Microscaling Post-Training Quantization for Vision Models</a></td><td>20</td><td>0</td><td>CV</td><td>비전 모델용 microscaling 양자화 오류 원인을 분석하고 보정한 효율화 연구임</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2610.03261'>Consecutive Posterior Fusion for Diffusive Recovery of Unobservable Image Structures</a></td><td>20</td><td>0</td><td>CV</td><td>diffusion posterior sampling에서 연속적 측정 추정치를 융합해 ill-posed 역문제를 개선한 영상 복원 연구임</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2610.03512'>ProgressNet: Sketching and Prompting with a Frozen Text-to-Image Model</a></td><td>20</td><td>0</td><td>CV</td><td>frozen T2I 모델이 스케치를 점진적으로 따라가게 하는 대화형 드로잉 프레임워크임</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2610.02254'>Overcoming Challenges of Interpretive Structural Modeling with Large Language Models</a></td><td>20</td><td>0</td><td>LG</td><td>LLM을 활용한 causal graph discovery로 interpretive structural modeling을 자동화한 연구임</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2610.02517'>Learning the Latent Structure: A Feature-Centric Approach to Graph Data Augmentation</a></td><td>20</td><td>0</td><td>LG</td><td>그래프 결측 구조 복원을 위한 feature-centric augmentation으로 robot learning과 무관한 그래프 data augmentation 기법임</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2610.02528'>Autoregressive Differentiable Method for Integer Programming</a></td><td>20</td><td>0</td><td>LG</td><td>0-1 integer program을 transformer로 autoregressive 생성하는 solver로 robotics와 무관함</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2610.02563'>OpenGameEval: Benchmarking Agentic Programming and Exploration in a Stateful Game Engine</a></td><td>20</td><td>0</td><td>LG</td><td>Roblox Studio 안에서 LLM 에이전트의 agentic coding·탐색을 측정하는 벤치마크로 robot learning과 무관함</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2610.02632'>Online Verification of Language Model Responses Under Cost Constraints</a></td><td>20</td><td>0</td><td>NLP</td><td>비용 제약 하에서 복수 weak verifier를 온라인으로 선택하는 LLM 검증 알고리즘으로 robotics와 무관함</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2610.02781'>OPD Before RL: Warm-Starting Rubric-Based RL with On-Policy Distillation</a></td><td>20</td><td>0</td><td>NLP</td><td>rubric 기반 RL 전에 teacher distillation으로 warm-start하는 2단계 LLM post-training 기법임</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2610.02839'>To Explore The Strange New World Beyond Data Distribution: System Behavior, Causality Tax, and Non-causal Base Model</a></td><td>20</td><td>0</td><td>NLP</td><td>언어모델의 causality가 최적이 아닐 수 있다는 system behavior 이론(SBD)을 제시한 연구임</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2610.03034'>Adaptive Second-Order Solvers for Fast Stochastic Diffusion Sampling</a></td><td>20</td><td>0</td><td>CV</td><td>diffusion sampling의 step 크기를 PI 제어로 조정하는 adaptive solver 연구임</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2610.03035'>Balancing Multimodal Learning via Functional Progress</a></td><td>20</td><td>0</td><td>Multimodal</td><td>modality별 function-space progress를 측정해 멀티모달 불균형을 교정하는 FGMO 기법임</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2610.03503'>Getting Your Guidance Weights Right in diffusion and flow-matching posterior sampling</a></td><td>20</td><td>0</td><td>CV</td><td>diffusion·flow-matching posterior sampling의 guidance weight를 2차원 최소제곱으로 오프라인 최적화하는 기법임</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2610.03529'>Divergence controls entropy in distillation</a></td><td>20</td><td>0</td><td>NLP</td><td>forward/reverse KL이 distillation에서 student entropy를 각각 부풀리고 줄임을 증명한 이론 분석 연구임</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2610.03667'>Planning to Learn</a></td><td>20</td><td>0</td><td>LG</td><td>exact policy gradient가 근시안적임을 보이고 cross-entropy를 patient accuracy로 재해석해 horizon loss를 제안한 이론 연구임</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2610.02460'>CUEing User Simulators: Calibrated User Embeddings for Multi-Turn Benchmarking</a></td><td>20</td><td>0</td><td>NLP</td><td>페르소나 기반 사용자 시뮬레이터의 결과 보정 문제를 다룬 연구로 로봇 도메인과 무관함.</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2610.02612'>Learning When to Commit from Partial Speech for End-to-End Simultaneous Speech Translation</a></td><td>20</td><td>0</td><td>NLP</td><td>동시통역에서 언제 커밋할지를 학습하는 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2610.02713'>WakeKV: Reactive, Reversible KV Residency for Heads That Change Their Minds</a></td><td>20</td><td>0</td><td>LG</td><td>KV 캐시 헤드를 reversible하게 관리하는 효율화 기법으로 로봇러닝과 무관함.</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2610.02829'>Clinical Concept Centers in LLMs</a></td><td>20</td><td>0</td><td>NLP</td><td>임상 LLM 내부에 개념 중심 회로가 존재함을 보인 해석가능성 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2610.02877'>Evaluating LLM-as-a-Judge Beyond Score Alignment: A Psychometric Analysis of Residual Judging Difficulty</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 심사자와 인간 심사자의 판단 난이도 구조를 심리측정학적으로 비교한 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2610.03163'>Predicting Steering Vectors and Adapter Weights for Few-Shot Author-Style Transfer</a></td><td>20</td><td>0</td><td>NLP</td><td>소수 예시로 저자 스타일을 전이하는 steering·hypernetwork 비교 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2610.03195'>Source Preference in the Wild: How LLM Agents Favor Items by Source, and How to Reduce It</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 에이전트가 출처에 따라 상품을 편향적으로 선호한다는 분석으로 로봇러닝과 무관함.</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2610.03421'>CLIMB: Confidence-Guided Complementary Evidence for Multimodal Retrieval-Augmented Generation</a></td><td>20</td><td>0</td><td>Multimodal</td><td>멀티모달 RAG에서 신뢰도 기반으로 근거를 보강하는 training-free 기법으로 로봇러닝과 무관함.</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2610.02395'>FlashSinkhorn 2: Block-Sparse Entropic Optimal Transport</a></td><td>20</td><td>0</td><td>LG</td><td>GPU 기반 optimal transport solver의 엔지니어링 개선이며 robotics 관련성 없음</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2610.02504'>HXAI: Hierarchical Privacy-Preserving Explainable AI in Distributed Energy Systems</a></td><td>20</td><td>0</td><td>LG</td><td>에너지 시스템의 privacy-preserving XAI 프레임워크이며 robotics와 무관함</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2610.02627'>Lost in the Request: How Communication Variation Disrupts Retrieval and Action in Email Agents</a></td><td>20</td><td>0</td><td>NLP</td><td>요청 표현 방식 변화에 따른 이메일 agent의 강건성을 측정한 평가 연구임</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2610.02704'>Label-Efficient Time Series Classification at Scale: A Dual-Stream OSSE-LSTM with Counterfactual Attribution</a></td><td>20</td><td>0</td><td>LG</td><td>소수 레이블로 시계열을 분류하는 episodic metric-learning 기법으로 robotics와 무관함</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2610.02741'>On the Chain-of-Thought Monitorability of Looped Language Models</a></td><td>20</td><td>0</td><td>NLP</td><td>looped language model의 chain-of-thought 모니터링 가능성을 평가한 해석가능성 연구임</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2610.02827'>MLCommons Jailbreak Benchmark v1.0</a></td><td>20</td><td>0</td><td>NLP</td><td>jailbreak 공격에 대한 LLM 강건성 평가 벤치마크 방법론임</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2610.02910'>Frequency Is Not Sensitivity Identifying Safety-Sensitive Experts in Sparse MoE LLM</a></td><td>20</td><td>0</td><td>LG</td><td>sparse MoE에서 안전 관련 expert를 식별하는 보안 취약점 분석 연구임</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2610.02920'>HASTE: Evolving Agent Harnesses Against Emerging Attacks Using Sparse Evidence</a></td><td>20</td><td>0</td><td>NLP</td><td>희소한 위협 증거로부터 agent harness를 진화시키는 방어 프레임워크임</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2610.02932'>When to Compile a Computer-Use Agent? Measuring Payback and Making Compilation Decisions for Token Efficiency</a></td><td>20</td><td>0</td><td>NLP</td><td>GUI agent 절차를 프로그램으로 컴파일할지 결정하는 토큰 효율화 시스템임</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2610.02968'>Reasoning with Evidence, Not Merely Rationales: Verifiable Preference Proofs for LLM-Based Recommendation</a></td><td>20</td><td>0</td><td>NLP</td><td>추천 시스템에서 선호 근거와 실제 영향력을 분리 검증하는 프레임워크임</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2610.02979'>RASPER: Reward-Aligned Summarization of Clinical Notes for EHR Outcome Prediction</a></td><td>20</td><td>0</td><td>NLP</td><td>downstream 예측 보상으로 임상 노트 요약을 최적화하는 RL 기법임</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2610.03033'>When Numbers Start Talking: Numerical Signalling and Strategic Behaviour Among LLMs</a></td><td>20</td><td>0</td><td>Multimodal</td><td>LLM agent 간 전략적 게임에서 신호 전달의 영향을 측정한 행동 연구임</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2610.03095'>Peer Influence across Heterogeneous AI Models</a></td><td>20</td><td>0</td><td>Multimodal</td><td>이종 LLM 간 설득력이 모델 크기로 예측되지 않음을 보인 상호작용 연구임</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2610.03213'>Toward SLM-based agentic task-tool intent matching</a></td><td>20</td><td>0</td><td>NLP</td><td>소형 언어모델로 agent의 tool 선택이 과제 의도에 맞는지 검증하는 기법임</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2610.03367'>Multilingual GSM-Symbolic: What determines capability transfer across languages?</a></td><td>20</td><td>0</td><td>NLP</td><td>언어 간 수학 능력 전이를 결정하는 요인을 분석한 다국어 벤치마크 연구임</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2610.03387'>Benchmarking Candidate Coverage in Typed Decision Models</a></td><td>20</td><td>0</td><td>NLP</td><td>typed decision model의 후보 누락 인식 능력을 측정한 벤치마크 연구임</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2610.03574'>HyperBrowseComp: A Multilingual and Multimodal Stress Test for Web-Browsing Agents</a></td><td>20</td><td>0</td><td>NLP</td><td>다국어·다중모달 웹 브라우징 agent 스트레스 테스트 벤치마크임</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2610.03693'>Transcriptome-informed multi-modal AI for predicting neoadjuvant therapy response from breast cancer biopsies</a></td><td>20</td><td>0</td><td>Multimodal</td><td>병리 영상에서 transcriptome을 추론해 유방암 항암치료 반응을 예측하는 의료 AI 연구임</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2610.02730'>Bellman Error Minimization Via Linear Programming Normalization</a></td><td>18</td><td>1</td><td>RL</td><td>신경망과 선형계획법을 결합해 Bellman error를 줄이는 근사 기법으로 robotics 적용 없이 revenue management에 적용됨</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2610.02951'>Dynamic Expert Pruning for Multi-Agent Systems</a></td><td>18</td><td>1</td><td>LG</td><td>멀티에이전트 시스템에서 prompt만으로 필요한 MoE expert를 예측해 동적으로 가지치기하는 서빙 최적화 기법임</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2610.03642'>On the Convergence of Success Conditioning for Policy Optimization</a></td><td>18</td><td>1</td><td>RL</td><td>성공한 행동의 확률을 높이는 success conditioning의 수렴성과 수렴율을 증명한 이론 연구임</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2610.02378'>THPL: A Vision-to-Language Decision Support Framework for Rainbow Trout Feeding Management in RAS</a></td><td>18</td><td>1</td><td>Multimodal</td><td>양식업 사료 관리를 위한 vision-to-language 의사결정 지원으로 응용 범위가 좁음</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2610.02452'>Reinforcement Learning Techniques for the Optimization of Target Polarization in Nuclear Physics Scattering Experiments</a></td><td>18</td><td>1</td><td>RL</td><td>핵물리 실험 장비 튜닝에 RL을 적용한 narrow domain 응용 논문임</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2610.03084'>NegT2IBench: When Negation Changes the Picture. A Polarity Benchmark for Text-to-Image Models</a></td><td>18</td><td>0</td><td>CV</td><td>T2I 모델의 부정(negation) 처리 능력을 측정하는 벤치마크로 robotics와 무관함</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2610.03224'>Uncertainty as a Proxy for Semantic Correctness in Diffusion-Based Medical Image Synthesis</a></td><td>18</td><td>0</td><td>CV</td><td>비조영 CT에서 조영 CT 합성 시 uncertainty를 해부학적 정확성의 proxy로 쓰는 의료 영상 연구임</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2610.03276'>Moving Forward with Video Saliency: A New Dataset and Benchmark where Motion Matters</a></td><td>18</td><td>0</td><td>CV</td><td>동적 콘텐츠에서 정적 baseline이 설명하지 못하는 video saliency 벤치마크임</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2610.03441'>ChromaGS: Text-Driven Semantic Editing of 4D Gaussian Avatars</a></td><td>18</td><td>0</td><td>3D Vision</td><td>4D Gaussian 아바타의 텍스트 기반 색상 편집 기법으로 robotics와 무관함</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2610.03577'>Rethinking What to Cache in Few-Step Diffusion Transformers: Solver-Aware Target Selection</a></td><td>18</td><td>0</td><td>CV</td><td>few-step diffusion transformer에서 어떤 텐서를 캐싱할지 solver 인식 기반으로 선택하는 효율화 연구임</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2610.03599'>ManifoldSplat: Language-Guided Semantic Shape Editing of 3D Gaussian Head Avatars</a></td><td>18</td><td>0</td><td>3D Vision</td><td>FLAME manifold 내에서 3D Gaussian 아바타의 형상을 언어로 편집하는 그래픽스 연구임</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2610.03617'>DEPICT: Scoring Text-to-Image Alignment by Answer Agreement</a></td><td>18</td><td>0</td><td>Multimodal</td><td>이미지-캡션 답변 일치도로 text-to-image alignment를 측정하는 training-free metric 연구임</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2610.02255'>MACTS-EM: Multi-Agent Collaborative Time Series Forecasting with Emergent Memory</a></td><td>18</td><td>0</td><td>LG</td><td>멀티에이전트 협업과 emergent memory 기반 시계열 예측 프레임워크로 robotics와 무관함</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2610.02383'>The Surprising Effectiveness of Shared Memory in Looped Transformers</a></td><td>18</td><td>0</td><td>LG</td><td>looped transformer가 메모리를 공유해도 품질 손실 없이 KV 캐시를 줄이는 아키텍처 연구임</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2610.02396'>Inherit-MAS: Test-Time Evolution of Multi-Agent Systems through Workflow and Execution Inheritance</a></td><td>18</td><td>0</td><td>LG</td><td>워크플로우·실행 상속을 통해 멀티에이전트 시스템을 test-time에 진화시키는 기법으로 robotics와 무관함</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2610.02427'>Geometry-Aware Time Reparameterization for Flow-Map Distillation</a></td><td>18</td><td>0</td><td>LG</td><td>flow-map distillation에서 기하 인식 시간 재매개변수화로 학습을 쉽게 만드는 생성모델 연구임</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2610.02488'>Harnessing LLMs as Agents: What Does It Cost?</a></td><td>18</td><td>0</td><td>LG</td><td>LLM 에이전트 하네스의 연산 자원 비용을 pebbling 이론으로 정식화한 연구임</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2610.02574'>DISSOLVR: An Interpretable and Fast Framework for Aqueous and Organic Solubility Prediction</a></td><td>18</td><td>0</td><td>LG</td><td>분자 용해도 예측을 위한 해석 가능한 프레임워크로 robotics와 무관한 화학 응용 연구임</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2610.02611'>Scale-Recursive Rectified Flows for Few-Step Precipitation Ensembles</a></td><td>18</td><td>0</td><td>CV</td><td>강수 다운스케일링을 위한 scale-recursive rectified flow로 robotics와 무관한 기상 응용 연구임</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2610.02657'>Context-Tower Conversion Preserves Generation While Freezing Retains Knowledge: Low-Budget AR-to-Diffusion Conversion of MoE LLMs</a></td><td>18</td><td>0</td><td>NLP</td><td>AR MoE LLM을 diffusion LM으로 변환하는 저비용 레시피 비교 연구로 robotics와 무관함</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2610.02661'>AIGS: Adaptive Incremental Gating System for Online Representation Learning in Non-Stationary Data Streams</a></td><td>18</td><td>0</td><td>LG</td><td>엣지 환경 온라인 표현학습을 위한 적응형 gating 시스템으로 스마트시티 센서 스트림에 적용됨</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2610.02722'>Structural-Functional Brain Connectivity Generation via Multimodal Hypergraph-based Flow Matching</a></td><td>18</td><td>0</td><td>LG</td><td>뇌의 구조-기능 연결성을 hypergraph flow matching으로 생성하는 신경영상 응용 연구임</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2610.02768'>No-Free-Graph: Learning When Multimodal Data Should Be Graphified</a></td><td>18</td><td>0</td><td>Multimodal</td><td>그래프 구조를 도입할지 여부를 사전에 판단하는 MAG-SCOUT 프레임워크로 멀티모달 그래프학습 효율화 연구임</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2610.02780'>Controlling Polar Exposure to Delay Memorization in Diffusion Models</a></td><td>18</td><td>0</td><td>CV</td><td>diffusion model이 학습 데이터를 암기하기 전 generalization 구간을 늘리는 update geometry 제어 기법임</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2610.02795'>Efficient Memory Crystallization for Graph Learning under Non-Stationary Distribution Shifts</a></td><td>18</td><td>0</td><td>LG</td><td>비정상 분포 변화 하에서 그래프 메모리를 생성 대신 closed-form으로 압축하는 test-time 적응 기법임</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2610.02816'>Gated Slot Attention-2: Two-Sided Associative Memory Correction in Linear Attention</a></td><td>18</td><td>0</td><td>NLP</td><td>linear attention의 고정 크기 메모리를 key/value 양쪽에서 교정하는 Gated Slot Attention-2 아키텍처임</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2610.02822'>Adaptive Spectral-Koopman Dynamics Modeling for Temporal Domain Generalization</a></td><td>18</td><td>0</td><td>LG</td><td>시간에 따라 분포가 변하는 데이터를 위한 spectral-Koopman 동역학 모델링 기법임</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2610.02881'>Toward Omni Multimodal Graph Foundation Model: A Topology-Driven Binding Approach</a></td><td>18</td><td>0</td><td>Multimodal</td><td>그래프 토폴로지로 멀티모달 바인딩을 유도하는 GraphBind 기반 모델임</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2610.02907'>Do ResNets Route? Sparse Interaction Experts in Residual Networks</a></td><td>18</td><td>0</td><td>CV</td><td>ResNet의 residual branch 기여를 Möbius inversion으로 분해해 암묵적 routing을 밝힌 해석 연구임</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2610.02990'>Differentiable Koopman Operator for Contrastive Learning on Dynamic Graphs</a></td><td>18</td><td>0</td><td>LG</td><td>Koopman operator를 동적 그래프 대조학습에 내재화해 이상탐지하는 KAIROS 기법임</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2610.03000'>Temporal Geometry of Deep Networks: Hyperbolic Representations of Training Dynamics for Intrinsic Explainability</a></td><td>18</td><td>0</td><td>LG</td><td>MLP 학습 동역학을 쌍곡기하학으로 표현해 self-organization을 설명하는 해석가능성 연구임</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2610.03071'>Learn Feasibility Once, Optimize All Objectives: Derivative-Free Diffusion Models for Chance-Constrained Programming</a></td><td>18</td><td>0</td><td>LG</td><td>risk-conditioned diffusion으로 feasibility를 한 번만 학습해 목적함수 무관하게 재사용하는 chance-constrained 최적화 기법임</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2610.03432'>OptiSelect: How does the Optimizer Shape Data Curriculum?</a></td><td>18</td><td>0</td><td>LG</td><td>optimizer가 online data selection의 효과를 어떻게 좌우하는지 분석한 LLM pretraining 연구임</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2610.03480'>Metropolis-Hastings Dominates Importance Resampling for Policy Composition</a></td><td>18</td><td>0</td><td>NLP</td><td>여러 reward 정책을 decoding 시점에 합성할 때 importance resampling보다 Metropolis-Hastings가 낫다는 분석 연구임</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2610.03526'>Beyond Trained Models: Compiling GNNs for a Sound Explainer Benchmark</a></td><td>18</td><td>0</td><td>LG</td><td>graded modal logic을 GNN 가중치로 직접 컴파일해 explainer를 정확한 ground truth로 평가하는 벤치마크(Gracr)임</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2610.03551'>Objects Without Morphisms: What LLMs for Mathematics Do Not Represent</a></td><td>18</td><td>0</td><td>NLP</td><td>LLM이 수학 하위분야 간 번역에서 가설의 일반성 수준을 올리는 쪽으로 편향됨을 보인 분석 연구임</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2610.03556'>Get a GRIP, this will be a long TRIP: A Quantifiable Long-Range Framework for Verifying Over-squashing</a></td><td>18</td><td>0</td><td>LG</td><td>GNN의 long-range interaction 벤치마크가 실제로 장거리성을 갖추는지 검증하는 공리 기반 프레임워크(TRIP/GRIP)임</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2610.03641'>IDRF: Inverse-Distilled Reward Fine-tuning of Masked Discrete Diffusion Models</a></td><td>18</td><td>0</td><td>LG</td><td>intractable sequence likelihood 문제를 inverse-distillation으로 우회해 few-step diffusion LM을 reward fine-tuning하는 기법임</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2610.03665'>Pivot-SD: Efficient Self-Distillation for Masked Diffusion Language Models</a></td><td>18</td><td>0</td><td>NLP</td><td>denoising 중 불확실성을 크게 줄이는 pivot token만 선별해 self-distillation하는 masked diffusion LM 기법임</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2610.02293'>HakemBench: A Turkish Benchmark of Typed Decisions</a></td><td>18</td><td>0</td><td>NLP</td><td>터키어 typed decision 벤치마크 공개로 로봇러닝과 무관한 평가 자원 기여임.</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2610.02486'>From Retrieval to Typed Decisions: Calibrated System One Models from Biomedical Sentence Encoders</a></td><td>18</td><td>0</td><td>NLP</td><td>생의학 검색 인코더를 typed decision 모델로 바꾸는 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2610.02549'>Evaluating Multi-Dimensional Generalization of Large Language Models in Temporal Extraction Tasks</a></td><td>18</td><td>0</td><td>NLP</td><td>시간·이벤트 추출 과제의 일반화를 다차원으로 평가한 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2610.02736'>TPBench: A Turning-Point Benchmark for Dialogue Compression</a></td><td>18</td><td>0</td><td>NLP</td><td>대화 압축에서 turning point 유실을 측정하는 벤치마크로 로봇러닝과 무관함.</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2610.02772'>Improving Atomic-Fact Recall via Focused Views in Unstructured Knowledge Editing</a></td><td>18</td><td>0</td><td>NLP</td><td>비구조적 지식 편집에서 문맥 의존성을 줄이는 기법으로 로봇러닝과 무관함.</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2610.02841'>How Robust Is Multimodal Claim Verification to LLM Rewriting?</a></td><td>18</td><td>0</td><td>Multimodal</td><td>LLM 재작성이 멀티모달 주장 검증 정확도에 미치는 영향을 분석한 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2610.02886'>Misinformation Without Triggers: From Factual Answers to Downstream Decisions</a></td><td>18</td><td>0</td><td>NLP</td><td>트리거 없는 허위정보가 사실 응답과 하위 의사결정 사이에 감사 격차를 만든다는 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2610.02986'>OLMo-Detect: A Multi-Stage, Confounder-Controlled Benchmark for Membership Inference on Large Language Models</a></td><td>18</td><td>0</td><td>NLP</td><td>LLM 훈련 데이터 포함 여부를 추정하는 membership inference 벤치마크로 로봇러닝과 무관함.</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2610.03136'>Investigating the Role of Reasoning-Language Alignment in Monolingual Retrieval-Augmented Generation</a></td><td>18</td><td>0</td><td>NLP</td><td>단일언어 RAG에서 추론 언어와 검색 언어 정렬 효과를 분석한 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2610.03176'>Hindsight-Guided Rationale Distillation for Rare Disease Diagnosis</a></td><td>18</td><td>0</td><td>NLP</td><td>희귀질환 진단을 위한 hindsight 증류 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2610.03329'>SyntaxBench: A Statistical Diagnostic Framework for Character-Level Reasoning in Large Language Models</a></td><td>18</td><td>0</td><td>NLP</td><td>문자 단위 추론 진단 벤치마크로 로봇러닝과 무관함.</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2610.03625'>FALCON: A Model and Dataset Agnostic Framework for Synthetic Data Generation for NL2SQL Pairs</a></td><td>18</td><td>0</td><td>NLP</td><td>모호성을 반영한 NL2SQL 합성 데이터 생성 프레임워크로 로봇러닝과 무관함.</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2610.02492'>Right Order, Wrong Scale: Auditing LLM Judges for Occupational AI Measurement</a></td><td>18</td><td>0</td><td>NLP</td><td>LLM judge의 순위 합치와 절대 수용률 불일치를 감사한 측정 연구임</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2610.02608'>Time Series Forecasting Benchmarks Need Scenario-Grounded Stress Testing</a></td><td>18</td><td>0</td><td>LG</td><td>시계열 예측 벤치마크의 평가 방법론을 제안하는 position paper임</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2610.02622'>CuBEs: Culturally-Situated Behavioral Evaluations and the Limitations of Culture-Blind LLM Judges</a></td><td>18</td><td>0</td><td>NLP</td><td>문화권별 LLM 행동 평가 벤치마크로 robotics와 무관함</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2610.02796'>Modeling Shared and Individual Structure for Cross-Subject Continuous Affect Regression from EEG-fNIRS</a></td><td>18</td><td>0</td><td>CV</td><td>EEG-fNIRS 기반 피험자 간 감정 회귀 예측 연구로 robotics와 무관함</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2610.02800'>BitNest: Bit-Nested Speculative Decoding for Memory-Efficient LLM Inference Acceleration</a></td><td>18</td><td>0</td><td>LG</td><td>저정밀 draft를 고정밀 표현에 내장하는 speculative decoding 메모리 효율화 기법임</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2610.02815'>iS-KV: Online Low-Rank KV Cache Compression via Block-Incremental SVD</a></td><td>18</td><td>0</td><td>LG</td><td>온라인 저랭크 KV cache 압축 기법으로 긴 추론 효율화에 국한됨</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2610.03029'>SoftGene: Protein Language Model-Enhanced Soft Prompting for Interpretable Gene Set Annotation</a></td><td>18</td><td>0</td><td>NLP</td><td>단백질 서열 정보를 soft prompt로 활용한 유전자 세트 주석 프레임워크임</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2610.03098'>Predictor-Guided Latent Space Codon Optimization for Maximizing Protein Expression</a></td><td>18</td><td>0</td><td>LG</td><td>mRNA 언어모델 latent space에서 코돈 최적화를 수행하는 생명공학 응용 연구임</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2610.03128'>Trading Strategy Optimization via Textual Gradient</a></td><td>18</td><td>0</td><td>AI</td><td>textual gradient로 거래 전략을 최적화하는 금융 응용 프레임워크임</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2610.03198'>KV$^2$: A Self-Refining KV Cache</a></td><td>18</td><td>0</td><td>NLP</td><td>재사용 가능한 KV cache를 선택적으로 재구성해 압축하는 효율화 기법임</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2610.03651'>MRVQ: One Resident Index for Dimension- and Rate-Elastic Vector Search</a></td><td>18</td><td>0</td><td>LG</td><td>차원·비트레이트에 걸쳐 재사용 가능한 vector quantization 검색 인덱스 효율화 기법임</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2610.02771'>Nearly Optimal Fixed-Confidence Best-Arm Identification with 1-Bit Feedback</a></td><td>17</td><td>0</td><td>LG</td><td>1-bit feedback 환경에서 최적 arm을 찾는 bandit 알고리즘의 이론적 하한과 알고리즘을 제시한 연구임</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2610.03265'>SPEAR: A Spectral-Disentangled MoE Neural Operator with Knowledge-Guided Expert Aggregation for Large-Scale PDE Pretraining</a></td><td>16</td><td>0</td><td>LG</td><td>저주파·고주파 성분을 분리한 spectral-disentangled MoE neural operator로 PDE 사전학습을 하는 연구임</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2610.03679'>Simulation-Free Learning of Population Dynamics with Wasserstein Lagrangian Residuals</a></td><td>16</td><td>0</td><td>LG</td><td>Clebsch 변분원리로 시뮬레이션 없이 Wasserstein Lagrangian dynamics를 학습하는 Double-Stitch 기법임</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2610.03712'>RNADyn: A Benchmark for Generating and Understanding RNA Dynamics</a></td><td>16</td><td>0</td><td>LG</td><td>RNA 동역학 궤적 생성과 이해를 하나의 backbone으로 묶은 벤치마크·모델(RNADyn)임</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2610.02421'>An AI-Based Multi-Stage Approach for Androgenetic Alopecia Assessment from Low-Magnification Scalp Images</a></td><td>15</td><td>0</td><td>CV</td><td>탈모 진단용 CV 파이프라인으로 robot learning과 무관한 의료 응용임</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2610.02494'>DeepStratNet: A Context-Aware Coordinate Regression Framework for Seismic Horizon Tracking under Sparse Labels</a></td><td>15</td><td>0</td><td>CV</td><td>지진파 horizon tracking을 좌표 회귀로 재정식화한 지구물리 응용 연구임</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2610.02647'>Capturing Dynamics: The 4D Facial Expression Intensity Dataset</a></td><td>15</td><td>0</td><td>CV</td><td>4D 표정 강도 데이터셋으로 robot learning과 무관한 affective computing 연구임</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2610.02755'>FiberGeoText: A Vision-Language Model for Population- Level Organization of Superficial White Matter</a></td><td>15</td><td>0</td><td>CV</td><td>뇌 백질 다발을 클러스터링하는 VLM으로 robot learning과 무관한 신경영상 연구임</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2610.03022'>ReSCUE: Re-translation with Sentence Commitment for Unsegmented Long-Form Simultaneous Sign Language Translation</a></td><td>15</td><td>0</td><td>NLP</td><td>비분할 장시간 수어 동시통역 프레임워크로 robot learning과 무관함</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2610.03142'>CalCErt: Bin-wise Certification of Confidence Calibration in Medical Image Classification</a></td><td>15</td><td>0</td><td>CV</td><td>의료 영상 분류기의 신뢰도 보정을 적대적 섭동 하에서 인증하는 방법으로 robotics와 무관함</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2610.03403'>ForestQuery: Boundary-Aware and Spatially Anchored Query Learning for Unified Forest Point Cloud Segmentation</a></td><td>15</td><td>0</td><td>3D Vision</td><td>산림 포인트클라우드의 경계 인식 query 학습 기반 분할 연구로 robotics와 무관함</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2610.03649'>On-Board Anomaly Detection for Efficient Marine Environmental Monitoring</a></td><td>15</td><td>0</td><td>CV</td><td>위성 기반 해양 환경 이상 탐지를 위한 온보드 경량 파이프라인으로 robotics와 무관함</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2610.03689'>SigLIP2 for aerial fire risk classification</a></td><td>15</td><td>0</td><td>CV</td><td>항공 영상 화재 위험 분류를 위한 SigLIP2 전이학습 연구로 robotics와 무관함</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2610.02253'>Approximation Property of Dropout Neural Networks: Sobolev Rates and Confidence Bounds</a></td><td>15</td><td>0</td><td>LG</td><td>dropout 신경망의 Sobolev 근사율과 신뢰구간을 다룬 이론 연구로 robotics와 무관함</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2610.02292'>Diffusion-Based Synthetic Data Pretraining for Enhancing Activity Recognition</a></td><td>15</td><td>0</td><td>LG</td><td>diffusion 합성 데이터로 사전학습한 활동 인식 모델 연구로 robotics와 거리가 있음</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2610.02353'>Does Every User Need a Private LoRA? Decoupling Personalization from Per-User Adaptation</a></td><td>15</td><td>0</td><td>NLP</td><td>사용자별 LoRA 대신 재사용 가능한 공유 개인화 용량을 학습하는 LLM 개인화 기법임</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2610.02359'>Lexicographic Multi-Objective On-Policy Distillation</a></td><td>15</td><td>0</td><td>NLP</td><td>RLVR에서 보상 우선순위를 명시적으로 보호하는 lexicographic 멀티티처 증류 기법임</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2610.02381'>Latent-MOPD: Latent Multi-Teacher On-Policy Distillation</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM 멀티티처 증류를 hidden state 수준까지 확장한 representation-level distillation 연구임</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2610.02391'>Hesitation Has a Geometry: Entropy-Trained Hyperbolic Probes for Sparse Activation Steering</a></td><td>15</td><td>0</td><td>NLP</td><td>수학 추론의 분기점에서 hyperbolic 공간 probe로 activation을 steering하는 기법임</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2610.02404'>Trained Agentic Context Management</a></td><td>15</td><td>0</td><td>NLP</td><td>장문맥 LLM을 self-call 도구로 학습시켜 적은 context로도 성능을 내는 연구임</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2610.02417'>The AI Theorist reveals excitonic structure in $α$-RuCl$_3$</a></td><td>15</td><td>0</td><td>LG</td><td>AI 에이전트가 양자 물질의 엑시톤 구조를 자율적으로 규명한 과학 발견 사례 연구임</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2610.02440'>Bandits via Additive Quantized Representations</a></td><td>15</td><td>0</td><td>RL</td><td>quantized representation으로 contextual bandit의 비선형성과 메모리 효율을 동시에 달성한 연구임</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2610.02462'>Capability Scaling-Down Laws for LLM Compression</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM 압축 방법별 능력 저하를 예측하는 scaling law 연구로 robotics와 무관함</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2610.02487'>Threshold-Aware Conformal Routing</a></td><td>15</td><td>0</td><td>LG</td><td>결정 임계값 인식 conformal routing으로 시뮬레이터 호출을 줄이는 방법론 연구임</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2610.02524'>BaCP: Backbone Contrastive Pruning for Preserving Representations in Extremely Sparse Neural Networks</a></td><td>15</td><td>0</td><td>LG</td><td>extreme sparsity pruning에서 representation 붕괴를 막는 기법으로 전형적 경량화 연구임</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2610.02584'>Dense Mixture-of-Experts as a Reparameterized Wide FFN: A Granularity Sweep at Fixed Compute</a></td><td>15</td><td>0</td><td>LG</td><td>고정 연산량에서 dense MoE의 granularity를 분석한 ablation 성격 연구로 새로운 formulation은 아님</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2610.02598'>Activation Sparsity with Weight Approximation for Faster LLM Decoding on Offloaded Weights</a></td><td>15</td><td>0</td><td>LG</td><td>offloaded weight 환경에서 activation sparsity로 LLM decoding을 가속하는 경량화 기법임</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2610.02659'>Distributed Learning with Selective State Space Models: Architecture-Aware Convergence Analysis</a></td><td>15</td><td>0</td><td>LG</td><td>selective state space model의 연합학습 수렴 분석으로 architecture-aware bound를 제시하나 robotics 적용은 없음</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2610.02683'>RAOA: Alternating-Operator Neural Computation with Programmable Radio Propagation</a></td><td>15</td><td>0</td><td>LG</td><td>프로그래머블 radio propagation을 연산 깊이로 쓰는 새로운 아날로그 컴퓨팅 구조로 robotics와 무관함</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2610.02705'>MuonIO: Principled Norm-Aware Descent for Embedding Tables and Language Model Heads</a></td><td>15</td><td>0</td><td>LG</td><td>Muon optimizer를 embedding table과 LM head에 확장한 최적화 기법으로 robotics와 무관함</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2610.02754'>Jumping up and down: Denoiser diffusion models for discrete ordinal data</a></td><td>15</td><td>0</td><td>LG</td><td>이산 ordinal 데이터를 위한 양방향 perturbation diffusion denoiser 모델임</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2610.02764'>A Controlled Audit of Personal AI Memory for Rating Prediction</a></td><td>15</td><td>0</td><td>LG</td><td>개인화 AI 메모리가 평점 예측에서 실제로 이력 연관을 쓰는지 감사한 진단 연구임</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2610.02766'>Exact Memory-Time Optimization for Prefix-Cached Language Model Serving</a></td><td>15</td><td>0</td><td>LG</td><td>prefix cache 메모리-시간 트레이드오프를 최소컷으로 최적화하는 LLM serving 기법임</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2610.02798'>Muon Learns Facts Better: Understanding the Role of Spectral Orthogonalization</a></td><td>15</td><td>0</td><td>LG</td><td>spectral orthogonalization이 factual recall 학습 순서에 미치는 영향을 분석한 Muon 메커니즘 연구임</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2610.02882'>DyRA: Dynamic Residual Approximation for Efficient Matrix Multiplication in DNNs</a></td><td>15</td><td>0</td><td>LG</td><td>구조적 행렬곱 근사의 출력 오차를 input-adaptive하게 보정하는 경량화 기법임</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2610.02909'>Constraint-Aware Training</a></td><td>15</td><td>0</td><td>NLP</td><td>constrained decoding에서 쓰는 분석을 학습 목적함수에 내재화한 program synthesis 기법임</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2610.02911'>Probe the Harness: Setup Checks for Stale-Data RL Comparisons in Language Models</a></td><td>15</td><td>0</td><td>LG</td><td>stale-data RL 비교에서 harness 설정 오류가 결과를 뒤집는 사례를 보인 방법론 점검 연구임</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2610.02953'>SlimKV: Joint Token-Feature KV Cache Compression with Reconstruction-Free Beacon Attention</a></td><td>15</td><td>0</td><td>NLP</td><td>token과 feature 차원을 함께 압축하는 KV cache 기법으로 long-context LLM serving 효율화 연구임</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2610.03007'>AvoKV-E: Payload-Aware KV Cache Eviction for Long Reasoning</a></td><td>15</td><td>0</td><td>NLP</td><td>value payload를 고려한 reasoning trace용 KV cache eviction 정책임</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2610.03027'>Tailoring the Quantization Space for 1-Bit KV Cache Compression</a></td><td>15</td><td>0</td><td>NLP</td><td>1-bit KV cache 양자화를 위한 채널별 타겟 공간 설계 기법임</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2610.03057'>When Does Synthetic Relational Data Teach Models to Use Relations? Tracing Predictive Structure from Pretraining Data to Model Behavior</a></td><td>15</td><td>0</td><td>LG</td><td>synthetic relational pretraining 데이터의 어떤 속성이 모델의 관계적 계산을 유도하는지 추적한 분석 연구임</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2610.03127'>Coverage You Can Steer: Online Conformal Calibration for RL-Driven Hardware-Aware NAS</a></td><td>15</td><td>0</td><td>LG</td><td>RL 기반 NAS에서 conformal prediction coverage를 온라인으로 제어하는 기법임</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2610.03135'>Page-EntroKV: Hardware-Aligned, Entropy-Weighted KV-Cache Eviction under Grouped-Query Attention</a></td><td>15</td><td>0</td><td>NLP</td><td>grouped-query attention 구조에 맞춘 entropy 기반 KV cache eviction 기법임</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2610.03199'>Predicting and Repairing Merge Collapse in Large Language Models</a></td><td>15</td><td>0</td><td>NLP</td><td>task vector merge가 붕괴할지 사전에 예측하고 PRISM으로 복구하는 모델 병합 기법임</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2610.03226'>D2K-Bench: Can LLM Agents Turn Expert Designs into Efficient GPU Kernels?</a></td><td>15</td><td>0</td><td>NLP</td><td>전문가 설계 가이드를 주었을 때 LLM agent의 GPU 커널 생성 품질이 얼마나 느는지 측정한 벤치마크임</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2610.03303'>S$^{2}$-PINN: Stochastic Separable Physics-Informed Neural Networks</a></td><td>15</td><td>0</td><td>LG</td><td>random PDE의 불확실성 정량화를 위한 stochastic separable PINN 구조임</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2610.03306'>Training-Loss Guarantees for Muon with Finite-Step Newton--Schulz Orthogonalization</a></td><td>15</td><td>0</td><td>LG</td><td>유한 step Newton-Schulz 직교화를 쓰는 Muon의 training-loss 도달 보장을 증명한 이론 연구임</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2610.03396'>A Unified Framework for Bayesian Data Assimilation with Generative Models and Observation Interpolants</a></td><td>15</td><td>0</td><td>LG</td><td>사전학습된 생성모델을 재학습 없이 posterior sampler로 바꾸는 데이터 동화 프레임워크임</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2610.03413'>AIBL: Augmented Instance-Based Learning with Structured Memory and Neural Embeddings</a></td><td>15</td><td>0</td><td>LG</td><td>symbolic instance-based learning을 신경 임베딩 유사도로 일반화한 AIBL 모델임</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2610.03418'>Rethinking Epistemic Uncertainty in Node Classification through Information Growth</a></td><td>15</td><td>0</td><td>LG</td><td>정보 증가에 따라 epistemic uncertainty가 실제로 줄어드는지 검증하는 그래프 EDL 평가 프레임워크임</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2610.03500'>Below what training size do deep tabular generators stop beating trivial baselines? A preregistered benchmark on a size ladder of clinical and standard datasets</a></td><td>15</td><td>0</td><td>LG</td><td>작은 임상 데이터셋에서 딥러닝 tabular generator가 단순 baseline을 못 이긴다는 preregistered 벤치마크 연구임</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2610.03558'>Cephalonauts One: A deep fMRI dataset for decoding naturalistic speech in the human brain</a></td><td>15</td><td>0</td><td>CV</td><td>podcast 청취 중 30시간 분량 fMRI를 모은 뇌-음성 디코딩 데이터셋 및 벤치마크임</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2610.02455'>FinDialogLens: Event Extraction over Multi-Party Dialogue for Missed-Trade Identification in Financial Chatrooms</a></td><td>15</td><td>0</td><td>NLP</td><td>금융 채팅방 이벤트 추출 산업 적용 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2610.02529'>A generative-informed neuro-symbolic framework for syntactic ambiguity resolution: Evidence from Arabic DPs</a></td><td>15</td><td>0</td><td>NLP</td><td>아랍어 구문 중의성 해소를 위한 neuro-symbolic 프레임워크로 로봇러닝과 무관함.</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2610.02770'>AptMQL-Bench: From Text-to-SQL to Text-to-MQL via Access-Pattern Schema Design and Data-Preserving Migration</a></td><td>15</td><td>0</td><td>NLP</td><td>text-to-SQL을 text-to-MQL로 변환하는 벤치마크로 로봇러닝과 무관함.</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2610.02775'>Automatic Evaluation of Mental Health Stigma in Online Communication</a></td><td>15</td><td>0</td><td>NLP</td><td>정신건강 낙인 탐지 벤치마크로 로봇러닝과 무관함.</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2610.02873'>ConvoDrift: A Multi-Turn Conversational Dataset for Modeling Stylistic Tone Evolution</a></td><td>15</td><td>0</td><td>NLP</td><td>대화 스타일 변화 모델링 데이터셋으로 로봇러닝과 무관함.</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2610.02875'>Query-aware routing for Cross-lingual performance gains in Encoders</a></td><td>15</td><td>0</td><td>NLP</td><td>핀란드어·스웨덴어 교차언어 검색 라우팅 기법으로 로봇러닝과 무관함.</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2610.02926'>Output Language Confusion under Multilingual Prompt Contamination</a></td><td>15</td><td>0</td><td>NLP</td><td>다국어 프롬프트 오염에서 출력 언어 혼동을 측정한 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2610.02949'>Enhancing Biomedical Named Entity Recognition via Multiple Programming Languages Instruction Tuning and Ensemble Method</a></td><td>15</td><td>0</td><td>NLP</td><td>다중 프로그래밍 언어 instruction tuning으로 생의학 개체명 인식을 개선한 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2610.02970'>A Guideline-Augmented Multi-Agent Framework for Schema-as-Code Biomedical Named Entity Recognition</a></td><td>15</td><td>0</td><td>NLP</td><td>가이드라인 증강 멀티에이전트 BioNER 프레임워크로 로봇러닝과 무관함.</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2610.03077'>Unmasking Propaganda: A Comparative Analysis of Masked and Causal Language Models</a></td><td>15</td><td>0</td><td>NLP</td><td>프로파간다 기법 탐지에서 MLM과 causal LM을 비교한 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2610.03078'>An automated pipeline for standardised speech-unit annotation in spontaneous dialogue</a></td><td>15</td><td>0</td><td>NLP</td><td>자연대화에서 발화 단위를 자동 주석하는 파이프라인으로 로봇러닝과 무관함.</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2610.03110'>Ontological Instability and Statistical Amplification: The Paradox of &quot;Humanizing&quot; LLM-Generated Text</a></td><td>15</td><td>0</td><td>NLP</td><td>AI 텍스트를 사람처럼 바꿀수록 오히려 탐지가 쉬워진다는 역설을 분석한 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2610.03112'>Building Interpretable Feature Representations for Resume-Vacancy Matching by Distilling Production LLM Signals</a></td><td>15</td><td>0</td><td>NLP</td><td>이력서-채용공고 매칭을 위한 해석가능한 특징 표현 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2610.03215'>StanceEval 2026: The Second Stance Detection Shared Task</a></td><td>15</td><td>0</td><td>NLP</td><td>아랍어 소셜미디어 입장 탐지 공유과제 보고서로 로봇러닝과 무관함.</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2610.03240'>Collective Bias Mitigation via Model Routing and Collaboration</a></td><td>15</td><td>0</td><td>NLP</td><td>모델 라우팅으로 편향을 완화하는 협업 프레임워크로 로봇러닝과 무관함.</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2610.03268'>Shrome at Touché: Soft-Vote Ensembling and Counter-Causal Augmentation for Causality Extraction</a></td><td>15</td><td>0</td><td>NLP</td><td>반사실적 인과 주장 추출 공유과제 참가 보고서로 로봇러닝과 무관함.</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2610.03324'>To Jev or Not? Evaluating the Accuracy and Efficiency of Structured Decision Models for Hate-Speech Moderation</a></td><td>15</td><td>0</td><td>NLP</td><td>혐오발언 탐지용 구조화 decision model 평가 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2610.03482'>Single-Pass Uncertainty Heads for Claim-Level Hallucination Detection in Persian Medical Language Models</a></td><td>15</td><td>0</td><td>NLP</td><td>페르시아어 의료 LM의 단일패스 환각 탐지 헤드 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2610.03525'>Structured Composition of Verifiable Atomic Insights for Table-to-Report Generation</a></td><td>15</td><td>0</td><td>NLP</td><td>테이블에서 검증 가능한 원자적 insight를 조합해 보고서를 생성하는 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2610.03531'>Author Representation Strategies for Zero-Shot Authorship Attribution: A Comparative Study of LLM-Based and Embedding-Based Approaches</a></td><td>15</td><td>0</td><td>NLP</td><td>zero-shot 저자 식별을 위한 저자 표현 전략 비교 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2610.03565'>Writerslogic at PAN 2026: Process over Content for Robust Detection under Domain Shift</a></td><td>15</td><td>0</td><td>NLP</td><td>PAN 2026 참가 보고서로 도메인 이동에 강인한 생성 텍스트 탐지 기법을 다루나 로봇러닝과 무관함.</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2610.03567'>Writerslogic at the CLEF 2026 SimpleText Track: Multi-Candidate LLM Simplification and Stacked Complexity Spotting</a></td><td>15</td><td>0</td><td>NLP</td><td>CLEF 2026 SimpleText 참가 보고서로 텍스트 단순화·오생성 탐지를 다루나 로봇러닝과 무관함.</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2610.02281'>The AI Risk Observatory: What Can We Learn from AI Disclosures in Annual Reports About Societal Resilience?</a></td><td>15</td><td>0</td><td>AI</td><td>연차보고서의 AI 리스크 공시를 LLM으로 분석한 사회과학 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2610.02342'>A Multi Method Importance and Performance Efficiency Analysis of Topological Metrics for Natural Visibility Graph Based Cyber Attack Detection</a></td><td>15</td><td>0</td><td>AI</td><td>네트워크 가시성 그래프 기반 사이버공격 탐지의 특징 중요도 분석 연구로 로봇러닝과 무관함.</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2610.02576'>Answering clinicians&#x27; questions over trial evidence tables with verifiable, feedback-driven language models</a></td><td>15</td><td>0</td><td>NLP</td><td>임상시험 근거표 질의응답 프레임워크로 의료 응용에 한정됨</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2610.02599'>TasteBench: Multimodal Benchmark for Sensory Prediction, from Molecules to Sustainable Foods</a></td><td>15</td><td>0</td><td>Multimodal</td><td>식품 대체 단백질의 감각 예측 벤치마크로 robotics와 무관함</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2610.02972'>CreateScore: Domain-Theory-Informed Bayesian Routing for LLM-Based CV Screening</a></td><td>15</td><td>0</td><td>LG</td><td>이력서 심사를 위한 Bayesian LLM 라우팅 시스템으로 비용 절감 엔지니어링에 가까움</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2610.03017'>Personalized Automatic Speech Recognition for a Dysarthric and Tracheostomic Speaker using Artificial Conversations</a></td><td>15</td><td>0</td><td>NLP</td><td>구음장애 화자 맞춤 음성 인식 시스템으로 robotics와 무관함</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2610.03524'>From Benchmarks to Production: A Text-to-SQL System for Complex Financial Data</a></td><td>15</td><td>0</td><td>NLP</td><td>금융 데이터베이스向 Text-to-SQL 프로덕션 시스템 사례 연구임</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2610.03564'>Knowledge or Calculator? Decomposing the Skill Premium in Verifiable Financial Agent Workflows</a></td><td>15</td><td>0</td><td>NLP</td><td>금융 agent 워크플로우에서 지식과 도구 기여를 분해한 벤치마크 연구임</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2610.03618'>Low-Cost Video--Time Priors as a Strong Baseline for EEG--fNIRS Emotion Regression on Familiar Videos</a></td><td>15</td><td>0</td><td>CV</td><td>친숙한 영상에서 video-time prior가 EEG-fNIRS 감정 회귀의 강한 baseline임을 보인 연구임</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2610.02894'>When Can We Trust the Matching Principle? Robust Deployment Geometry Under Finite-Sample and Model Uncertainty</a></td><td>14</td><td>0</td><td>LG</td><td>추정 불확실성과 스펙트럼 분리도의 비율로 매칭 원리의 신뢰 여부를 정하는 이론 연구임</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2610.03054'>RIPPLE in Still Water: Zero-Shot Clustering in Federated Learning with Wavelet Scattering Transform</a></td><td>14</td><td>0</td><td>LG</td><td>wavelet scattering으로 클라이언트를 오프라인에서 클러스터링하는 연합학습 기법임</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2610.03211'>HyperFuse: Fast Self-Supervised Node Embeddings for Attributed Hypergraphs</a></td><td>14</td><td>0</td><td>LG</td><td>spectral modularity로 빠르게 hypergraph 임베딩을 생성하는 self-supervised 기법임</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2610.03330'>Cordial Learning: Distributed Training with Correlated Data</a></td><td>14</td><td>0</td><td>LG</td><td>상관된 데이터를 가진 분산 에이전트의 저차원 출력 공유 학습을 다룬 게임이론적 분산학습 연구임</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2610.03378'>Operator-informed initialization for Fourier features physics-informed neural networks</a></td><td>14</td><td>0</td><td>LG</td><td>Fourier feature PINN의 spectral bias를 줄이는 operator-informed 초기화 기법임</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2610.03546'>ZeroMAG: Zero-Shot Multimodal Adapter Generation for Plug-and-Play EEG Foundation Models</a></td><td>14</td><td>0</td><td>LG</td><td>EEG foundation model을 동반 생리신호로 확장하는 zero-shot adapter 생성 기법임</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2610.03597'>A Path Integral Surrogate for Multi-Step Gradient Inversion in Federated Learning</a></td><td>14</td><td>0</td><td>LG</td><td>FedAvg의 누적 업데이트를 경로적분으로 근사해 gradient inversion 공격을 강화한 연구임</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2610.03640'>Broken scale symmetries in undercomplete linear autoencoders</a></td><td>14</td><td>0</td><td>LG</td><td>undercomplete linear autoencoder에서 SGD가 scale symmetry를 깨는 방향성을 분석한 이론 연구임</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2610.03646'>When May a Bandit Leave Its Anchor? E-Process-Authorized Thompson Sampling under Non-stationarity</a></td><td>14</td><td>0</td><td>RL</td><td>e-process로 비정상성 적응 시점을 통계적으로 승인하는 Thompson sampling 변형(e-ATS)임</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2610.03702'>LESSER: Post-Training Data Selection with Output-Layer Gradients</a></td><td>14</td><td>0</td><td>LG</td><td>출력층 gradient만으로 post-training data selection을 근사해 비용을 줄이는 LESSER 기법임</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2610.02701'>Conditional Capacity and Routing in Mixture-of-Experts Particle Transformers</a></td><td>13</td><td>0</td><td>LG</td><td>입자물리 분류를 위한 MoE transformer의 routing 용량을 분석한 도메인 특화 연구임</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2610.02865'>On Unlearning for Time-series Forecasting</a></td><td>13</td><td>0</td><td>LG</td><td>시계열 예측 모델의 machine unlearning을 위한 residual diffusion 기법임</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2610.03193'>Bridging Research and Practice: A Systematic Evaluation of Generalist and Dermatology-Specific Models in Clinical Skin Lesion Classification</a></td><td>12</td><td>0</td><td>CV</td><td>피부병변 분류 모델의 임상 일반화를 평가한 벤치마크 연구로 robotics와 무관함</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2610.03332'>A Fully Automatic Pipeline for 3D Dendrite Instance Segmentation in SBF-SEM</a></td><td>12</td><td>0</td><td>CV</td><td>SBF-SEM 영상에서 수상돌기를 자동 분할하는 신경과학 영상 파이프라인으로 robotics와 무관함</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2610.03380'>Interpretable Deepfake Detection in Videos via Explicit Forensic Features and Temporal Modeling</a></td><td>12</td><td>0</td><td>CV</td><td>명시적 forensic feature 기반 해석 가능한 딥페이크 탐지 연구로 robotics와 무관함</td></tr>
<tr><td>486</td><td><a href='https://arxiv.org/abs/2610.03467'>Preserving Anatomical Continuity: Three-Stage Pipeline for Colon Segmentation in 3D Abdominal CT Scans</a></td><td>12</td><td>0</td><td>CV</td><td>복부 CT 대장 분할의 위상 보존 파이프라인으로 robotics와 무관한 의료 영상 연구임</td></tr>
<tr><td>487</td><td><a href='https://arxiv.org/abs/2610.03474'>Fed-ADApt: Federated Anytime Depth Adaptation for Resource-Aware Medical Image Segmentation</a></td><td>12</td><td>0</td><td>LG</td><td>연합학습 환경에서 자원별 depth 적응 의료 영상 분할 프레임워크로 robotics와 무관함</td></tr>
<tr><td>488</td><td><a href='https://arxiv.org/abs/2610.02248'>State-Space Unlearning for Non-Stationary Bias in Land Surface Forecasting</a></td><td>12</td><td>0</td><td>LG</td><td>지표면 예측용 Mamba 상태공간모델의 비정상 편향을 제거하는 machine unlearning 연구임</td></tr>
<tr><td>489</td><td><a href='https://arxiv.org/abs/2610.02258'>Parameter-Free Interval-Dynamic Regret under Heavy-Tailed Noise</a></td><td>12</td><td>0</td><td>LG</td><td>중noise 환경에서 파라미터 없는 interval regret 온라인 볼록최적화 이론 연구임</td></tr>
<tr><td>490</td><td><a href='https://arxiv.org/abs/2610.02299'>$Ψ$-Resilience: Model-Free Feature Importance from 1D Topological Signals</a></td><td>12</td><td>0</td><td>LG</td><td>1차원 위상 신호 기반 model-free feature importance 설명 기법 연구임</td></tr>
<tr><td>491</td><td><a href='https://arxiv.org/abs/2610.02347'>From Behavior to Provenance: Attributing Tabular Foundation Models to Synthetic Pretraining Data</a></td><td>12</td><td>0</td><td>LG</td><td>합성 사전학습 데이터에 대한 tabular foundation model의 training-data attribution 검증 연구임</td></tr>
<tr><td>492</td><td><a href='https://arxiv.org/abs/2610.02355'>Why Does Adaptive Batching Help LLM Pretraining? A Perspective from Unbounded Variance</a></td><td>12</td><td>0</td><td>LG</td><td>LLM 사전학습에서 adaptive batching이 돕는 이유를 unbounded variance 관점에서 분석한 이론 연구임</td></tr>
<tr><td>493</td><td><a href='https://arxiv.org/abs/2610.02363'>ArrivalBench: Agent-Generated Data Pipelines Are Correct Once and Wrong Under Time</a></td><td>12</td><td>0</td><td>LG</td><td>agent가 생성한 데이터 파이프라인이 시간 경과 후 재실행 시 실패하는 문제를 재현 벤치마크로 측정함</td></tr>
<tr><td>494</td><td><a href='https://arxiv.org/abs/2610.02413'>Prompted to Discriminate: Generalizing Malicious-Input Probes in the Wild</a></td><td>12</td><td>0</td><td>LG</td><td>activation probe 기반 악성 입력 탐지에서 분류 suffix의 효과를 분석한 안전 연구임</td></tr>
<tr><td>495</td><td><a href='https://arxiv.org/abs/2610.02431'>CRISP: A Framework for Clause-Reconstructed Interpretable NeuroSymbolic Propositions</a></td><td>12</td><td>0</td><td>LG</td><td>이진 신경망의 마지막 레이어를 Tsetlin Machine 명제로 재구성하는 해석가능성 연구임</td></tr>
<tr><td>496</td><td><a href='https://arxiv.org/abs/2610.02438'>Are you Synthesizing or Recalling? Evaluating LLMs on Algorithmic Code Retrieval</a></td><td>12</td><td>0</td><td>NLP</td><td>LLM이 알고리즘 코드를 합성하는지 암기해 검색하는지 구분하는 벤치마크 연구임</td></tr>
<tr><td>497</td><td><a href='https://arxiv.org/abs/2610.02439'>A Generative Model of Complex Networks Using Graphons and Neural Inverse Operators</a></td><td>12</td><td>0</td><td>LG</td><td>graphon과 neural inverse operator로 복잡 네트워크를 생성하는 방법론 연구로 robotics와 무관함</td></tr>
<tr><td>498</td><td><a href='https://arxiv.org/abs/2610.02516'>Student-Guided Teacher Distillation for Efficient LLM Task Routing: Positioning Against Jev-Style System-1 Classifiers</a></td><td>12</td><td>0</td><td>NLP</td><td>LLM task routing을 위한 student-guided teacher distillation 효율화 연구임</td></tr>
<tr><td>499</td><td><a href='https://arxiv.org/abs/2610.02559'>Neuron merging via inverse-activation regression for post-training compression of sigmoid neural networks</a></td><td>12</td><td>0</td><td>LG</td><td>sigmoid network의 neuron merging 압축 기법으로 robotics와 무관한 경량화 연구임</td></tr>
<tr><td>500</td><td><a href='https://arxiv.org/abs/2610.02716'>Differential Privacy of Gradient Descent on Perturbed Objectives</a></td><td>12</td><td>0</td><td>LG</td><td>perturbed objective 위에서 gradient descent의 차등 프라이버시를 분석한 이론 연구임</td></tr>
<tr><td>501</td><td><a href='https://arxiv.org/abs/2610.02738'>Inner Momentum for Differentially Private Muon</a></td><td>12</td><td>0</td><td>LG</td><td>differentially private Muon의 clipping 왜곡을 줄이는 inner momentum 기법임</td></tr>
<tr><td>502</td><td><a href='https://arxiv.org/abs/2610.02868'>Distributionally Robust Survival Models under Subpopulation Shift and Outlier Contamination</a></td><td>12</td><td>0</td><td>LG</td><td>부분집단 이동과 이상치 오염을 동시에 다루는 분포강건 생존분석 모델임</td></tr>
<tr><td>503</td><td><a href='https://arxiv.org/abs/2610.02872'>Peer Effects in Signed Networks: Separating Influence Through Positive and Negative Ties</a></td><td>12</td><td>0</td><td>LG</td><td>긍정·부정 관계를 분리해 peer effect를 추정하는 signed network 인과추론 연구임</td></tr>
<tr><td>504</td><td><a href='https://arxiv.org/abs/2610.03087'>Zephon: Elastic Determinism for Online, Stateful Foundation Model Data Loading Pipelines</a></td><td>12</td><td>0</td><td>LG</td><td>온라인 stateful foundation model 데이터 파이프라인의 결정론적 재현성을 보장하는 시스템 연구임</td></tr>
<tr><td>505</td><td><a href='https://arxiv.org/abs/2610.03117'>Exploring the Trade-Off Between Structured Pruning and Fault Tolerance in Deep Neural Networks for Space Applications</a></td><td>12</td><td>0</td><td>LG</td><td>structured pruning이 우주용 DNN의 bit-flip 내성에 미치는 트레이드오프를 실험한 연구임</td></tr>
<tr><td>506</td><td><a href='https://arxiv.org/abs/2610.03419'>Deep Bayesian REFoCUS</a></td><td>12</td><td>0</td><td>LG</td><td>초음파 multistatic 복원을 Bayesian 딥러닝으로 다루는 의료영상 연구임</td></tr>
<tr><td>507</td><td><a href='https://arxiv.org/abs/2610.03456'>Beyond Random Splits: Evaluating Drug-Target Affinity Models Under Chemically and Biologically Motivated Distribution Shifts Copy</a></td><td>12</td><td>0</td><td>LG</td><td>약물-표적 친화도 모델을 화학적·생물학적 분포이동 조건에서 재평가한 벤치마크 연구임</td></tr>
<tr><td>508</td><td><a href='https://arxiv.org/abs/2610.03491'>Dual-Context Analog Retrieval for Time Series Forecasting</a></td><td>12</td><td>0</td><td>LG</td><td>과거 유사 상태를 검색해 미래 구간을 패치 단위로 정교화하는 analog 시계열 예측 모델임</td></tr>
<tr><td>509</td><td><a href='https://arxiv.org/abs/2610.03494'>Most-Recent Anchoring with Recurrent Ordering for Time Series Forecasting</a></td><td>12</td><td>0</td><td>LG</td><td>최근 패치를 anchor로 recurrent하게 처리하는 장기 시계열 예측 모델임</td></tr>
<tr><td>510</td><td><a href='https://arxiv.org/abs/2610.02496'>&quot;I just assumed that it would translate&quot;: examining MT risk awareness among healthcare staff with abbreviations as a use case</a></td><td>12</td><td>0</td><td>NLP</td><td>의료진의 기계번역 위험 인식을 다룬 질적 연구로 기술적 기여가 작음</td></tr>
<tr><td>511</td><td><a href='https://arxiv.org/abs/2610.02510'>On-Premises Multi-Course RAG Tutoring for Business Education: Hardware-Software Trade-offs in a Campus AI Tutor</a></td><td>12</td><td>0</td><td>NLP</td><td>캠퍼스 RAG 튜터 배포 사례 연구로 연구적 novelty가 낮음</td></tr>
<tr><td>512</td><td><a href='https://arxiv.org/abs/2610.02631'>Designing the Future of User Feedback for Generative AI</a></td><td>12</td><td>0</td><td>NLP</td><td>생성 AI 사용자 피드백 UX 설계 사례 연구로 기술적 기여가 작음</td></tr>
<tr><td>513</td><td><a href='https://arxiv.org/abs/2610.02679'>DataWeave: Deploying Human-LLM Analytics for Exploratory Structured Data Analysis</a></td><td>12</td><td>0</td><td>NLP</td><td>데이터 저널리즘을 위한 human-LLM 협업 분석 도구의 배포 사례 연구임</td></tr>
<tr><td>514</td><td><a href='https://arxiv.org/abs/2610.03639'>Do Large Language Models Know Colombian Law? A Reliability Benchmark for the Colombian Legal System</a></td><td>12</td><td>0</td><td>NLP</td><td>콜롬비아 법체계에 대한 LLM 신뢰성 벤치마크로 robotics와 무관함</td></tr>
<tr><td>515</td><td><a href='https://arxiv.org/abs/2610.02561'>Oracle headroom without signal: null-calibrated evaluation of candidate selection for thermal heart rate estimation</a></td><td>10</td><td>0</td><td>CV</td><td>열화상 심박 추정에서 oracle 평가의 통계적 함정을 지적한 방법론 논문으로 robotics와 무관함</td></tr>
<tr><td>516</td><td><a href='https://arxiv.org/abs/2610.03051'>BeeWhere: Segmenting Bumble Bee Colonies to Quantify Behavioral Effects</a></td><td>10</td><td>0</td><td>CV</td><td>꿀벌 군집 행동 분석을 위한 instance segmentation 연구로 robotics와 무관함</td></tr>
<tr><td>517</td><td><a href='https://arxiv.org/abs/2610.02224'>Hybrid Machine Learning-Assisted Raman Spectroscopy with Generative Feature Augmentation for Pharmaceutical Identification</a></td><td>10</td><td>0</td><td>LG</td><td>라만 분광법 기반 의약품 식별을 위한 하이브리드 ML 프레임워크로 robotics와 무관함</td></tr>
<tr><td>518</td><td><a href='https://arxiv.org/abs/2610.02249'>Nearest-neighbour baselines for fingerprint prediction from MS/MS spectra under different assumptions</a></td><td>10</td><td>0</td><td>LG</td><td>MS/MS 스펙트럼 분자 지문 예측의 nearest-neighbour 베이스라인 비교 연구로 robotics와 무관함</td></tr>
<tr><td>519</td><td><a href='https://arxiv.org/abs/2610.02256'>TRACE: A Reproducible Benchmark for Electricity Price Forecasting with Official Operational Text</a></td><td>10</td><td>0</td><td>LG</td><td>전력가격 예측에 운영 텍스트를 결합한 벤치마크로 robotics와 무관함</td></tr>
<tr><td>520</td><td><a href='https://arxiv.org/abs/2610.02268'>From Mathematical to Executable Certificates for Machine Unlearning</a></td><td>10</td><td>0</td><td>LG</td><td>머신 언러닝의 수학적 인증을 실행 가능한 아티팩트로 연결하는 보안 연구임</td></tr>
<tr><td>521</td><td><a href='https://arxiv.org/abs/2610.02278'>CLEAN: Psychometrically Consistent Incremental Cognitive Diagnosis under Concept-Space Expansion via Architectural Isolation</a></td><td>10</td><td>0</td><td>LG</td><td>개념 공간 확장 하의 인지진단 모델을 위한 architectural isolation 연구로 교육 도메인에 한정됨</td></tr>
<tr><td>522</td><td><a href='https://arxiv.org/abs/2610.02303'>PowerBench: Measuring Language Model Bias in Power-shifting Requests</a></td><td>10</td><td>0</td><td>LG</td><td>LLM의 power-shifting 요청에 대한 편향을 측정하는 벤치마크로 robotics와 무관함</td></tr>
<tr><td>523</td><td><a href='https://arxiv.org/abs/2610.02397'>Validated Data Onboarding for AI Demand Forecasting on U.S. Building Meter Data: Design, Controlled Evaluation, and a Corrected Negative Result</a></td><td>10</td><td>0</td><td>LG</td><td>건물 전력 수요 예측용 데이터 정제 파이프라인 연구로 robotics와 무관함</td></tr>
<tr><td>524</td><td><a href='https://arxiv.org/abs/2610.02511'>Post-Training Quantization of Autoregressive Weather Models</a></td><td>10</td><td>0</td><td>LG</td><td>자기회귀 기상 예측 모델의 post-training 양자화 연구로 robotics와 무관함</td></tr>
<tr><td>525</td><td><a href='https://arxiv.org/abs/2610.02763'>A Two-Stage Cascade for Near-Real-Time Forest Anomaly Detection from Sentinel-1 SAR Time Series</a></td><td>10</td><td>0</td><td>CV</td><td>Sentinel-1 SAR 시계열로 산림 손실을 탐지하는 이상탐지 시스템으로 robotics와 무관함</td></tr>
<tr><td>526</td><td><a href='https://arxiv.org/abs/2610.02866'>DIVINE: Simple Cross-Market Stock Pretraining via Diverse Indicator Reconstruction</a></td><td>10</td><td>0</td><td>LG</td><td>기술지표 재구성으로 cross-market 주식 사전학습을 하는 경량 인코더 연구임</td></tr>
<tr><td>527</td><td><a href='https://arxiv.org/abs/2610.02954'>Hyperparameter selection for equation learning with biologically-informed neural networks</a></td><td>10</td><td>0</td><td>LG</td><td>생물학적으로 정보화된 PINN의 hyperparameter 선택을 위한 진단 워크플로임</td></tr>
<tr><td>528</td><td><a href='https://arxiv.org/abs/2610.03019'>Signal Simplification Is Not Predictive Simplification: Diagnosing Residual Neural Forecasting in Short-Horizon Volatility</a></td><td>10</td><td>0</td><td>LG</td><td>통계적 1단계 예측 성공이 residual LSTM 학습을 돕지 않음을 보인 변동성 예측 진단 연구임</td></tr>
<tr><td>529</td><td><a href='https://arxiv.org/abs/2610.03216'>Kernel Singular Value Decomposition with Extension to Multiple Data Sources</a></td><td>10</td><td>0</td><td>LG</td><td>비대칭 커널에 대한 KSVD를 다중 데이터 소스로 확장한 커널 방법 연구임</td></tr>
<tr><td>530</td><td><a href='https://arxiv.org/abs/2610.03225'>The Neuro-Physical Inverter: A Modular Framework for Magnetotelluric Inversion Coupling Ensemble Conditioning with Residual Learning</a></td><td>10</td><td>0</td><td>LG</td><td>ensemble 조건화와 residual 학습을 결합한 지구물리 역산 프레임워크임</td></tr>
<tr><td>531</td><td><a href='https://arxiv.org/abs/2610.03425'>Becoming Suspicious Across Borders: Algorithmic Extraterritoriality and AI-Driven Financial Surveillance</a></td><td>10</td><td>0</td><td>NLP</td><td>AI 기반 금융감시의 역외관할권 문제를 다룬 정책·사회과학 논문임</td></tr>
<tr><td>532</td><td><a href='https://arxiv.org/abs/2610.02225'>The Price of Greenwashing: Algorithmic Verification and Market Discipline using Conformal Machine Learning</a></td><td>8</td><td>0</td><td>LG</td><td>ESG 그린워싱을 conformal ML로 검증하는 금융 계량경제 연구로 robotics와 무관함</td></tr>
<tr><td>533</td><td><a href='https://arxiv.org/abs/2610.02284'>Effects of interpulse-interval variation on deep-learning classification of bat vocalizations</a></td><td>8</td><td>0</td><td>LG</td><td>박쥐 울음소리 분류에서 interpulse interval의 효과를 분석한 음향 연구로 robotics와 무관함</td></tr>
<tr><td>534</td><td><a href='https://arxiv.org/abs/2610.02442'>AI-driven Thermal-aware Data Center Capacity Planning</a></td><td>8</td><td>0</td><td>LG</td><td>데이터센터 열 관리를 위한 AI 기반 용량 계획 연구로 robotics와 무관함</td></tr>
<tr><td>535</td><td><a href='https://arxiv.org/abs/2610.02461'>A Composable AI-Accelerated Iterative Solver for 3D-IC Thermal Modeling</a></td><td>8</td><td>0</td><td>LG</td><td>3D-IC 열 해석을 위한 조립식 AI 가속 반복 솔버 연구로 robotics와 무관함</td></tr>
<tr><td>536</td><td><a href='https://arxiv.org/abs/2610.02610'>Seer: Maximum Likelihood Regression for Learning-Speed Curves</a></td><td>8</td><td>0</td><td>LG</td><td>1995년 박사논문을 재게시한 학습 곡선 예측 모델로 최신 연구 기여가 아님</td></tr>
<tr><td>537</td><td><a href='https://arxiv.org/abs/2610.02615'>Quantifying the Value of Constructive Induction, Knowledge, and Noise Filtering on Inductive Learning</a></td><td>8</td><td>0</td><td>LG</td><td>1991년 ICML 논문을 재게시한 effective dimension 측정 지표 연구로 최신 기여가 아님</td></tr>
<tr><td>538</td><td><a href='https://arxiv.org/abs/2610.03082'>Smart Sensing for Safer Bridges: From Sensor Signals to AI-Driven Anomaly Detection</a></td><td>8</td><td>0</td><td>LG</td><td>교량 센서 데이터의 이상탐지를 신호처리와 Isolation Forest로 비교한 응용 연구임</td></tr>
<tr><td>539</td><td><a href='https://arxiv.org/abs/2610.03256'>Cross-cohort TB classification using clinical data gathered in Uganda and South Africa</a></td><td>8</td><td>0</td><td>LG</td><td>국가 간 결핵 선별을 위한 임상 데이터 분류 모델 비교 연구임</td></tr>
<tr><td>540</td><td><a href='https://arxiv.org/abs/2610.03259'>PaMIR: Open Benchmark of Public Credit-Default Datasets</a></td><td>8</td><td>0</td><td>LG</td><td>신용 부도 예측을 위한 공개 데이터셋 19개를 모은 벤치마크 릴리스임</td></tr>
<tr><td>541</td><td><a href='https://arxiv.org/abs/2610.03402'>16-bit Precision of Convolutional Neural Networks on Microcontroller Units for 8-bit Costs</a></td><td>8</td><td>0</td><td>LG</td><td>마이크로컨트롤러에서 16비트 CNN을 8비트 비용으로 돌리는 양자화 기법으로 경량화 연구임</td></tr>
<tr><td>542</td><td><a href='https://arxiv.org/abs/2610.03505'>An Automated and Reproducible Workflow for Crack Identification and Damage Assessment of Fusion Materials</a></td><td>8</td><td>0</td><td>CV</td><td>핵융합 재료의 SEM 균열 탐지를 자동화한 재현 가능 워크플로임</td></tr>
</tbody></table>

</details>
