# 오늘의 arXiv Top 15 — 2026-09-01 (화)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**
> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)

**신규 논문 수: 전체 927편 → 중복 제거 후 927편 (이번 평가 대상 927편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 260 |
| cs.LG | 185 |
| cs.RO | 68 |
| cs.CL | 233 |
| cs.AI | 181 |

*1차 스크리닝: 전체 927편을 제목/초록 기반으로 채점(Claude (scheduled agent)) → 상위 15편은 arXiv 원문을 내려받아 정밀 리뷰(Claude (scheduled agent)) 후 최종 점수 산정.*

---

## Top 15

### 1. [80점] Can Video World Models Track Unobserved World States?

- **분야**: World Model / 영상 생성 아키텍처 표현력 분석 · **robotics relevance**: 8/10
- **arXiv**: [2608.30692](https://arxiv.org/abs/2608.30692) ([PDF](https://arxiv.org/pdf/2608.30692))
- **저자**: Joonghyuk Shin, Yicong Hong, Jaesik Park, Xun Huang
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: Project webpage: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 숨겨진 카드 아래 공 위치를 추적하는 action-conditioned 셸 게임을 만들어 video world model이 눈에 안 보이는 world state를 실제로 추적하는지 검증함. 표준 Transformer·Mamba2·nonnegative-eigenvalue linear attention은 학습 길이에서는 완벽하지만 길이가 늘면 chance 수준으로 무너지는 반면, negative eigenvalue linear attention과 test-time training(TTT) 기반 nonlinear fast weight(LaCT)만 길이 일반화에 성공함.

**Core innovation & methodology**

- action-conditioned video Shell Game 벤치마크 제안: S5 순열군 word problem을 시각화해 렌더링 품질과 hidden state(공 위치) 추적 능력을 분리해서 측정함
- 표준 backbone(bidirectional/causal Transformer, Mamba2, nonnegative-eigenvalue GDN/KDA)은 학습 길이(N=5 swap)에서 100% accuracy지만 N=30에서는 chance(0.2)로 떨어지는 반면 PSNR 등 시각 품질은 그대로 유지됨을 보여 렌더링 그럴듯함과 state tracking이 별개 능력임을 입증함
- 실패 원인을 readout probing으로 분석: causal Transformer의 KV cache는 append-only라 매 청크마다 전체 히스토리에서 배치를 재유도해야 하고, pixel diffusion loss가 숨겨진 상태를 직접 지도하지 않아 state가 토큰이 아니라 아키텍처 내부에 있어야 한다는 논지를 세움
- 해결 메커니즘 두 가지 확인: (1) DeltaNet 계열 선형 attention의 transition eigenvalue 범위를 [0,1]에서 [-1,1]로 넓히면 swap에 해당하는 reflection 연산을 표현 가능해짐 (2) LaCT(TTT, nonlinear SwiGLU fast weight)는 online으로 feature map(W0,W2)을 갱신해 커널 자체가 history-dependent해짐. 두 메커니즘 모두 '청크 간 이어지는 state + 이를 in-place로 revise하는 표현력 있는 transition'이라는 하나의 원리로 통합됨

**Novelty vs. prior works**

- 가장 가까운 선행연구는 언어모델 state tracking 이론(Merrill et al.의 TC0/NC1 분석, Grazzi et al.의 negative eigenvalue DeltaNet)과 video world model controllability 연구(Self Forcing, LaCT)임. 이 이론을 action-conditioned video generation 도메인에 처음 실증 적용한 것이 핵심 기여임
- 새 아키텍처를 제안한 것이 아니라 기존 GDN-neg, LaCT를 가져다 쓴 진단 실험이라 방법 자체의 novelty는 제한적임. 새로움은 Shell Game이라는 진단 벤치마크 설계와 KV cache가 압축된 state가 아니라 시각적 히스토리일 뿐이라는 것을 readout probing으로 보인 분석에 있음
- 실제 배포되는 대규모 video world model(Cosmos, Genie 계열)에 대한 직접 검증은 없고 약 200M 규모 자체 학습 모델로만 확인해 스케일 일반화는 미확인 상태임

**Benchmark results**

- Shell Game(N=5 학습, N=30까지 평가): 표준 backbone은 학습 길이에서 100% accuracy지만 N=30에서 chance(0.2) 수준으로 저하됨
- GDN-neg(음수 eigenvalue 허용)는 N=30에서 accuracy 0.95로 사실상 문제를 해결함
- LaCT(8 fast-weight head)는 N=20에서 0.98, N=30에서 0.69 유지. head 1~2개는 학습 길이를 넘어서면 실패함
- LaCT ablation: SwiGLU를 1-layer linear MLP로 교체하면 N=10 accuracy가 1.00에서 0.23으로 붕괴, feature map(W0,W2)을 고정하고 readout W1만 갱신해도 붕괴해 feature map의 online update가 핵심임을 확인함
- denoising step을 4에서 50으로 늘려도 state accuracy는 불변함(PSNR만 소폭 개선). 모든 실험은 synthetic Shell Game/Memory Maze/Block World에 국한되며 real video나 real robot 실험은 없고, 코드·모델 공개 여부는 본문에서 확인 불가

**Top-tier conference 적합성 — 78/100 · 추천 venue: ICLR**

formal state-tracking 이론과 video world model 아키텍처를 잇는 명확하고 재현 가능한 실증 실험, KV cache·fast weight 메커니즘 분석의 정밀함이 강점임. 다만 synthetic toy task와 200M 규모 자체 학습 모델에 국한돼 실제 배포되는 video world model에 대한 함의는 제한적이라는 게 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- hidden state tracking 실패는 occlusion이 있는 manipulation(가려진 물체, 카메라 이탈)에서 world model 신뢰성 문제로 직결됨. RoboPhys-3D류 평가에 '가려진 상태 추적' 축을 추가할 근거로 쓸 수 있음
- negative-eigenvalue linear attention과 LaCT 같은 nonlinear fast weight 메커니즘은 test-time optimization과 robot memory 설계에서 stateful world model 아키텍처 후보로 바로 검토 가능함
- Shell Game 벤치마크 설계 방법론을 occlusion-heavy manipulation task의 world model 평가 프로토콜로 변형해 counterfactual reasoning·active perception 연구와 연결할 수 있음

---

### 2. [77점] Temporal Forcing: 4D Representation Alignment for Vision-Language-Action Models

- **분야**: VLA (Representation Alignment) · **robotics relevance**: 9/10
- **arXiv**: [2608.30643](https://arxiv.org/abs/2608.30643) ([PDF](https://arxiv.org/pdf/2608.30643))
- **저자**: Xingyu Ding, Yuzhong Zhao, Chunhai Zhao, Yinghuan Shi, Chaoyang Zhao, Yifan Zhang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 VLA의 3D geometry alignment가 현재 프레임만 봐서 발생하는 observation aliasing 문제를 history pathway와 4D foundation model(StreamVGGT) alignment로 해결한 Temporal Forcing을 제안함. LIBERO 98.8%(+2.2pt), 실물 hidden-placement task에서 20.0%→43.3%로 향상함.

**Core innovation & methodology**

- history pathway가 과거 K=7개 프레임을 DINOv2+Q-Former로 압축한 gist token을 causal transformer로 요약해 16개 history token을 만들고 zero-init gated cross-attention으로 VLA backbone에 주입함.
- 이 history 표현을 pretrained 4D foundation model(StreamVGGT)의 causal geometric feature에 정렬하는 temporal alignment(state+change+read-out 세 항 조합)를 도입함.
- current-frame alignment로 현재 프레임 image token을 dense geometric feature에 정렬해 backbone feature 자체도 별도로 구조화함.
- 추론 시엔 4D foundation model과 alignment head를 모두 제거하고 history pathway만 남겨 배포 비용을 억제함(action chunk 45ms→58ms, 10Hz 제어 예산 이내).

**Novelty vs. prior works**

- 가장 가까운 prior work인 Spatial Forcing 대비 정렬 대상을 현재 프레임 3D geometry에서 시간에 따라 진화하는 4D geometry로 확장한 점이 핵심 차이임.
- HAMLET, MemoryVLA 등 history-augmented VLA는 입력에 history를 추가할 뿐 latent representation이 실제로 시간 정보를 담도록 직접 감독하지 않는데, Temporal Forcing은 이를 4D geometric alignment로 직접 supervise함.
- history만 추가하거나 4D target만 추가하는 조합으로는 개선이 없고 temporal alignment가 있어야 history가 유효해짐을 통제 실험(compute-constrained protocol)으로 입증해 novelty 주장이 실험적으로 뒷받침됨.

**Benchmark results**

- LIBERO 4개 suite 평균 98.8%로 동일 base model(StarVLA-OFT, Qwen3-VL-4B) 96.6% 대비 +2.2pt, Long suite에서 93.8%→97.2%로 가장 큰 개선임.
- RoboTwin 2.0 bimanual 12 task 평균 53.5%→62.8%(9/12 task 개선), handover block 0→44%, handover mic 39→79%로 occlusion이 큰 task에서 개선폭이 가장 큼(sim benchmark).
- 실물 UR3 hidden-placement multi-stage task에서 isolated stage 성능은 base와 비슷(78/90 vs 75/90)하지만 sequential full-task success가 20.0%→43.3%로 두 배 이상 개선됨(trial 30회로 규모는 제한적).
- compute-constrained ablation(10k step)에서 history만 추가 시 88.2%, temporal alignment 없는 조합(row4) 83.7%로 오히려 base(90.7%)보다 낮고, temporal alignment 추가 시 93.6%로 상승해 4D alignment가 history를 유용하게 만드는 핵심 요인임을 확인함.
- LIBERO-Plus zero-shot robustness에서 pooled 성능 75.0%→77.8%, sensor noise 항목에서 73.1%→81.3%로 가장 크게 개선됨. 코드는 논문에 공개 예정이라고만 명시되어 있고 텍스트 기준 아직 공개 여부는 확인 불가.

**Top-tier conference 적합성 — 79/100 · 추천 venue: CoRL**

representation alignment paradigm을 프레임 단위 3D에서 4D로 자연스럽게 확장했고 controlled ablation이 매우 체계적이라 설득력이 높음. 다만 alignment target(StreamVGGT)이 기존 pretrained 모델의 재사용이라 conceptual leap은 크지 않고, 실물 실험이 task 1개·trial 30회에 그쳐 일반화 근거가 약한 점이 리스크임.

**추천 이유 & 누리랩 연구와의 연결점**

- world model/failure detection 연구와 직접 연결됨: 4D geometric alignment는 로봇의 task progress를 latent에 남기는 방법으로, '무엇이 끝났고 무엇이 안 끝났는지' 추적하는 failure diagnosis에 응용 가능함.
- test-time optimization 관점에서, 4D foundation model을 inference-time에 재부착해 uncertainty를 재점검하는 test-time verification 모듈로 확장할 수 있음.
- robot memory 연구(HAMLET, MemoryVLA) 대비 direct supervision 방식의 벤치마킹 기준으로 유용함.

---

### 3. [76점] Zeva: In-Context Causal Learning for Generalizable Embodied Manipulation

- **분야**: VLA / Robot Memory / Test-time Adaptation · **robotics relevance**: 10/10
- **arXiv**: [2608.30880](https://arxiv.org/abs/2608.30880) ([PDF](https://arxiv.org/pdf/2608.30880))
- **저자**: Fu Chen, Xin Ding, Bingjia Huang, Xiangyu Li, Mingju Wang, Jiawei He, Kun Li, Wei Sun 외 3명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 78점

> 💡 Zeva는 policy 파라미터를 얼린 채로 로봇이 실제로 겪은 action과 state change를 causal interaction signal로 인코딩해 dual-timescale memory에 저장하고, 다음 action 생성 시 이 신호를 in-context prompt로 주입하는 방법임. RoboCasa365-Atomic5 시뮬레이션에서 76.8%(최고 baseline 대비 +4.4%p)를 냈고, gradient update 없이 반복 시도만으로 시뮬레이션 누적 성공률이 26%에서 73%까지 오르며, 실제 ChemLab-Evo 화학실험 로봇에서도 task별로 유사한 상승 추세(예: Pick Up Test Tube 65%→100%)를 보이는 self-evolution을 보임.

**Core innovation & methodology**

- In-Context Causal Learning(ICCL)이라는 문제 설정을 새로 제시함 — frozen policy가 자기 action과 state change의 인과관계를 gradient update(∇θπ=0) 없이 in-context로 학습하도록 목표 함수를 정의함.
- Causal Transition Encoder(CTE)가 GRU로 visual latent·action encoding·observed effect를 causal interaction state로 압축하고, 여기서 task phase token과 causal interaction signal을 뽑아냄.
- Dual-timescale memory 구조를 제안함 — attempt 내 최근 신호만 담는 Brief Interaction Trace(BIT, sliding window)와, attempt 간 유사도 기반으로 merge되는 Persistent Interaction Memory(PIM) 두 층으로 나눔.
- 검색된 causal signal을 causal prompt로 구성해 frozen diffusion policy의 full-attention block에 주입함 — policy 파라미터는 전혀 갱신하지 않고 memory만 온라인으로 갱신함.

**Novelty vs. prior works**

- test-time training 계열(RoboTTT, WAM-TTT)은 deployment history를 gradient update로 fast weight에 반영하는데, Zeva는 gradient 없이 memory retrieval만으로 적응함 — 적응 속도는 빠르지만 in-context learning과 test-time adaptation을 결합한 방향 자체는 최근 연구 흐름과 궤를 같이함.
- GEN-1.5·Skild S1 같은 in-context robot learner는 새로운 task를 few-shot demo로 파악하는 것이 목적인데, Zeva는 같은 task 안에서 반복 시도의 causal structure를 학습하는 것이 목적이라는 차이를 내세움 — 다만 이 구분이 근본적으로 다른 문제인지 적용 범위 차이인지는 논문만으로는 확실치 않음.
- action-state change를 causal unit으로 명시적으로 저장하는 점을 MemoryVLA·DIM-WAM 같은 perception-level memory와 차별화하지만, 결국 memory-augmented policy와 test-time adaptation 계열을 결합한 형태라 완전히 새로운 paradigm이라기보다 기존 요소의 재조합에 가까움.

**Benchmark results**

- RoboCasa365-Atomic5(5개 task, 각 50 episode)에서 평균 성공률 76.8%로 최고 — Fast-WAM 72.4%, Cosmos3-Nano 64.8%, LingBot-VA 55.2% 대비 우위지만 task별 편차가 커서 CoffeeSetupMug는 44%에 그침.
- 실제 로봇 ChemLab-Evo(ARX manipulator, 7개 task 3단계 난이도, 각 20 episode)에서 전 난이도 최고 성공률 — atomic 83.3%, short-sequence 70.0%, complex 7.5%로 최고 baseline 대비 각각 +6.6, +5.0, +5.0%p지만 complex task 자체의 절대 성공률은 5~10%로 낮음.
- post-deployment scaling 실험(별도 구성한 fixed episode subset)에서 cumulative success rate가 RoboCasa365는 1회 시도 26%에서 4회 누적 시도 73%까지, ChemLab-Evo 3개 atomic task도 유사하게 상승 — 매 시도 전 환경을 초기 상태로 되돌리는 fixed episode 조건에서 측정한 결과임.
- ablation(5개 real-world task, 각 20 episode)에서 BIT 제거 시 15~30%p, PIM 제거 시 10~20%p 하락, 둘 다 제거하면 가장 낮은 성능 — 두 memory 층이 상호보완적임을 시사함.
- one-shot human teleoperation demo로 memory warm-up 시 최대 20%p(Place Beaker) 개선, cross-task retrieval도 nearest 신호로 대체하면 성능 유지되지만 random 신호로 대체하면 35~40%p 하락함.

**Top-tier conference 적합성 — 76/100 · 추천 venue: CoRL**

실로봇·시뮬레이션 양쪽에서 반복 시도에 따른 성공률 상승을 명시적으로 측정한 실험 설계가 강점이고 ICCL이라는 문제 정의도 명료함. 다만 비교 baseline이 전부 저자가 직접 재현한 것이고 방법 자체가 memory-augmented policy와 test-time adaptation의 재조합에 가까워 top-tier full paper의 conceptual leap 기준에는 다소 못 미침.

**추천 이유 & 누리랩 연구와의 연결점**

- causal memory 구조(BIT+PIM)는 누리랩의 robot memory·failure recovery 연구에 바로 참고할 아키텍처임 — PIM의 유사도 기반 merge 방식을 실패 사례 축적에 응용할 수 있음.
- gradient 없이 memory retrieval만으로 적응한다는 설계는 test-time optimization 연구에서 gradient 기반 test-time training과의 latency·성능 비교 실험 축으로 쓸 수 있음.
- cross-task causal signal transfer 실험(Fig.7,8)은 서로 다른 task에서 같은 물리적 효과를 인식하는 실험이라 counterfactual reasoning·object-centric representation 연구에 방법론적으로 참고할 만함.

---

### 4. [76점] SUN: Persistent Programs For Language-Grounded Control-to-Learning-to-Real Policies

- **분야**: Manipulation · **robotics relevance**: 8/10
- **arXiv**: [2608.31167](https://arxiv.org/abs/2608.31167) ([PDF](https://arxiv.org/pdf/2608.31167))
- **저자**: Weiqi Wang, Zhi Li, Yudong Lei, David Martinez, Xiaofeng Gao, Yuxin Jiang, Chenfanfu Jiang, Yingnian Wu 외 2명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 64점

> 💡 LLM이 언어와 scene semantics로부터 기하·접촉 관계를 한 번만 정의하는 SUN Program을 합성하고, 이를 MPC cost·RL reward·stage transition·진단 predicate로 동시에 컴파일해 control-to-learning 전 과정에서 task semantics가 유지되게 함. 9개 manipulation task에서 macro-success 82.03%로 sparse-reward baseline(35.67%)과 Stage-BC(24.75%)를 크게 앞서고, 물리 Franka·Kinova 로봇 zero-shot 전이에서 34.7% 성공률을 보임.

**Core innovation & methodology**

- SUN Program: 기하/접촉 relation을 한 번 정의하면 MPC cost, stage 완료 predicate, RL reward, transition guard, diagnostics로 동시 컴파일되는 typed executable을 제안함(Semantic Unification)
- Kuafu 시스템: LLM이 등록된 scene frame과 typed operator library에서 SUN Program을 합성하고, MPC로 10개 초기조건에서 feasibility screening 및 최대 5회 repair를 거쳐 program을 승인함
- 승인된 program의 MPC 성공 trajectory로 stage-conditioned behavior cloning(Stage-BC)을 학습하고, 그 위에 program-derived reward로 학습하는 bounded residual RL(PPO)을 추가해 whole-task policy를 구성함(π = clip(π_θ + α_ρ·π_ψ))
- 정책 학습 이후에도 SUN Program이 data production 단계에서 stage 진행·완료 판정·false-completion 필터링을 계속 제공하며, 최종 vision policy(DP3 등)는 program 없이 관측-행동 쌍만으로 학습됨

**Novelty vs. prior works**

- 가장 가까운 선행연구인 ReKep(keypoint cost 최적화)과 OmniManip(object-centric constraint+VLM checking)은 control 단계에 머물고 학습된 policy로 넘어가면서 semantics를 잃는데, 이 논문은 하나의 typed relation을 control·monitoring·learning 세 인터페이스로 동시 컴파일하는 것이 본질적 차별점임
- Eureka류 LLM reward 자동생성과 달리 LLM이 새 코드를 생성하지 않고 검증된 typed operator를 선택·binding만 하도록 제한해, 반복 학습 cycle 없이 MPC로 즉시 feasibility를 screening함(LLM 상호작용 비용이 rollout당이 아니라 task당으로 전환됨)
- 다만 typed operator library와 registered scene frame이 사전 정의되어야 하므로 완전한 open-vocabulary 일반화는 아니며, deformable object나 fluid는 다루지 못한다고 저자가 스스로 명시함

**Benchmark results**

- 9개 task 평균 macro-success: Kuafu 82.03%(3-run robustness aggregate 79.43%) vs sparse-reward residual RL 35.67%, Stage-BC 24.75%, Eureka 12.85%(final eval), VoxPoser 10.00%
- long-horizon 견고성: stacking 8단계->15단계(T1 95.78%->T6 87.25%, -8.53pp), drawer 6단계->14단계(T2 98.01%->T7 95.21%, -2.80pp)로 저하폭이 sparse-reward baseline(65.14%->22.21%)보다 훨씬 작음
- 컴퓨팅 비용: end-to-end GPU-hour Kuafu 122.67 vs Eureka 479.60(약 3.91배 효율), task당 LLM 토큰도 110.5k vs Eureka 234.4k
- data generation: task당 500개 성공 trajectory 기준 DP3 학습 성공률 Kuafu 46.02% vs 최강 baseline SkillMimic 22.44%(2.05배), 궤적 효율·smoothness 지표인 Q95 yield(완료 시간·경로 길이·action 매끄러움이 모두 MPC 성공 궤적의 95th percentile 이내인 rollout 비율) 57.3% vs MimicGen 20.4%; 시간당 성공 trajectory 산출량은 인간 teleoperation 대비 10.57배(246.79 vs 23.34 min/GPU-hr)
- 물리 로봇 zero-shot 전이: Franka FR3·Kinova Gen3에서 6개 task(T1,T2,T4,T5,T7,T8)·106회 시행 중 36회 성공(task-macro 34.7%, pooled 33.96%), task별 편차가 있음(T1 15.0%~T2 55.0%); program synthesis에는 GPT-5.5를 사용했고 held-out instruction·operator·scene에 대한 일반화는 검증하지 않았다고 명시함

**Top-tier conference 적합성 — 72/100 · 추천 venue: CoRL**

language-grounded task program을 control·RL·data generation·real-robot deployment까지 일관되게 연결한 시스템 설계와 강한 ablation(구성요소별 handoff 비교), 실물 로봇 검증까지 갖춘 완성도 높은 논문임. 다만 typed operator library와 scene registration에 의존해 open-world 일반화 주장은 제한적이고, 실물 검증이 6개 task·106회 시행으로 표본이 작아 task당 신뢰구간이 넓고(가장 표본이 작은 task는 6회 중 2회 성공, Wilson 신뢰구간 9.7%~70.0%) 이 점이 rejection risk로 작용할 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- SUN Program처럼 관계를 한 번 정의해 control·monitoring·learning에 동시 컴파일하는 아이디어는 failure detection에도 적용 가능함: 동일 predicate를 실행 중 실시간 diagnostics로 재사용해 어느 stage에서 실패했는지 판별하는 용도로 확장할 수 있음
- stage-conditioned BC + bounded residual RL 구조와 false-completion 검출 메커니즘은 VLA policy에 stage-aware skill chaining과 자기 진단(self-diagnosis)을 결합하는 test-time 구조로 참고할 만함
- registered scene frame과 typed operator library에 의존하는 한계는 scene graph·semantic mapping과 결합해 operator grounding 자체를 자동화하는 후속 연구로 이어질 수 있음

---

### 5. [74점] RoboPhys-3D: A Comprehensive Embodied World Model Evaluation via 3D Reconstruction

- **분야**: Embodied World Model 평가 벤치마크 (3D reconstruction 기반) · **robotics relevance**: 9/10
- **arXiv**: [2608.28718](https://arxiv.org/abs/2608.28718) ([PDF](https://arxiv.org/pdf/2608.28718))
- **저자**: Tianyi Wang, Jiazhou Chen, Yiming Xu, Xiangyu Li, Tianyi Zeng, Chih-Hsien Chou, Ning Lu, Liang Peng 외 2명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 66 pages, 12 figures, 55 tables
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 생성된 video와 ground-truth video를 동일한 3D reconstruction 파이프라인에 통과시켜 재구성 자체의 오류와 world model 생성 오류를 분리하는 RoboPhys-3D 벤치마크를 제안함. RoboTwin 2.0 기반 50개 매니퓰레이션 task, 25000개 ground-truth 영상, 50개 metric으로 4개 video world model을 평가해 시각적으로 그럴듯한 rollout도 물체 위치·경로 추적과 실제 task 성공에서는 크게 뒤처진다는 것을 보임.

**Core innovation & methodology**

- generated video와 ground-truth video를 동일한 3D reconstruction 파이프라인(VGGT, VGGT-Ω, 4DGS, 4C4D)에 통과시켜서 재구성 오류(reconstruction-induced)와 world model 생성 오류(generation-induced)를 분리하는 평가 프로토콜을 제안함
- RoboTwin 2.0 기반 50개 매니퓰레이션 task(단/양팔 x target 유무 4 regime), 5000 episode, 5-view 25000개 ground-truth video로 벤치마크를 구축함
- pixel-level fidelity, 3D geometry consistency, state-level understanding, task-level completeness 4단계 x 18 sub-dimension x 50 metric의 계층적 taxonomy를 설계하고, 전체 평균 Average Full Score(AFS)와 task success와 상관 높은 8개 metric만 평균한 RoboPhyscore 두 지표를 제안함
- 생성된 rollout을 IDM(DreamGen)으로 실행 가능한 action으로 디코딩해 시뮬레이터에서 replay하고, action planner·data engine·VLM 판정 3가지 task-success 지표로 종합 평가함

**Novelty vs. prior works**

- 가장 가까운 선행연구는 WBench(생성 영상의 3D self-consistency만 측정, ground truth와의 정합성은 안 봄)와 ESI-Bench(reconstruction을 downstream reasoner 입력으로만 사용)임. generated와 ground-truth를 '같은' reconstruction pipeline으로 통과시켜 직접 비교하는 최초의 프로토콜이라는 것이 핵심 차이임
- 새로운 world model이나 학습 방법은 제안하지 않는 벤치마크/평가지표 논문이라 method novelty는 없음. 다만 metric 개수(50개)와 taxonomy 통합 범위가 기존 벤치마크(6~22개 metric) 대비 넓다는 점에서 실질적 기여가 있음
- RoboTwin 2.0이라는 단일 시뮬레이션 플랫폼, 단일 embodiment에 한정되어 cross-embodiment나 sim-to-real 일반화는 저자 스스로 future work로 남김

**Benchmark results**

- Cosmos 3가 4개 모델 중 RoboPhyscore 최고(0.6330, ground truth 대비 92.7%), 이어서 Wan(0.5359), RoboDreamer(0.3492), CogVideoX(0.3363) 순임
- reconstruction 방법 자체의 오차: VGGT/VGGT-Ω는 ground truth 대비 94.7%/96.1%를 유지하지만 4DGS/4C4D는 78.2%/85.4%만 유지해 reconstruction 선택이 RoboPhyscore를 최대 21.8%p까지 흔듦
- state-level understanding에서 Cosmos도 object localization·trajectory accuracy는 ground truth의 61.2%/73.2%에 불과(Wan은 33.2%/63.3%)한 반면, VLM 판정 기반 interaction·physical law adherence는 ground truth와 비슷하거나 상회해 시각적 그럴듯함과 실제 상태 정확도가 분리됨을 보임
- task-level에서 CogVideoX는 collision safety 0.9650(ground truth보다 높음)이면서 task success는 ground truth의 16.5%에 불과함, 보수적 행동이 안전해 보이지만 과제를 못 끝낸다는 사례임
- RoboPhyscore와 사람 평가(70명 rater) 간 Pearson r=0.9761, Spearman ρ=0.8962로 강한 정합성 확인. inverse dynamics model(IDM, 생성된 영상을 실행 가능한 action으로 디코딩하는 모델) 선택 ablation에서 DreamGen이 baseline IDM인 MIDM 대비 MAE 59.0% 감소, action planner/data engine success를 각각 9.2%/23.7%p 개선함
- 모든 실험은 RoboTwin 2.0 시뮬레이터 기반이며 real robot 실험은 없음(저자도 future work로 명시). 4개 오픈소스 video world model(Wan, CogVideoX, Cosmos 3, RoboDreamer)만 평가했고 코드·데이터셋 공개 여부는 본문에서 확인 불가

**Top-tier conference 적합성 — 76/100 · 추천 venue: CoRL**

50개 task, 25000개 ground-truth 영상, human alignment 검증까지 갖춘 포괄적 벤치마크이며 reconstruction-induced와 generation-induced 오류를 분리한 프로토콜이 명확한 기여임. 다만 단일 시뮬레이터·단일 embodiment에 한정되고 real robot 검증이 없어 sim-to-real 격차에 대한 근거가 없다는 게 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- object localization·trajectory accuracy가 VLM 기반 판정보다 훨씬 낮게 나온다는 결과는 world model 평가에서 시각적 그럴듯함만으로는 실패를 못 잡는다는 근거이며, 누리랩 failure detection 연구에서 state-level metric을 반드시 병행해야 한다는 논거로 쓸 수 있음
- reconstruction-matched 비교 프로토콜은 object-centric 3DGS·scene graph 연구에서 생성된 rollout의 3D consistency를 검증하는 방법론으로 그대로 이식 가능함
- Cosmos가 3D geometry consistency는 ground truth 수준이지만 object localization 등 state-level에서 크게 뒤처진다는 분리 결과는 world model을 manipulation policy 학습용 data engine으로 쓸 때 추가로 검증해야 할 축을 구체적으로 제시함

---

### 6. [74점] Hydra: A Navigation World Action Model with Discrete Latent Planning and Continuous Flow-Matching Execution

- **분야**: Navigation / World Action Model · **robotics relevance**: 9/10
- **arXiv**: [2608.28995](https://arxiv.org/abs/2608.28995) ([PDF](https://arxiv.org/pdf/2608.28995))
- **저자**: Mohammad Nazeri, Alexandyr Card, Samira Huber, Anuj Pokhrel, Yujun Wang, Ruben Hammele, Daeun Song, Sören Pirk 외 1명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 29 pages, 12 figures. this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 Hydra는 visual state·pose·action을 하나의 latent manifold로 early-fusion한 뒤 modality별 VQ codebook으로 이산화해, planner(sampler+evaluator)를 world model 내부의 discrete latent 공간에서 그대로 돌리는 Discrete Latent Planning(DLP)을 제안함. Jackal·Spot 두 실로봇에서 baseline인 NWM 대비 500배 이상 빠른 계획 시간(0.9초 vs 500초 이상)을 보였고, 장애물이 있는 상황에서 NWM·VertiFormer 모두 0/10에 그친 반면 Hydra는 8/10 성공함.

**Core innovation & methodology**

- vision(frozen VAE latent)·pose·action을 early-fusion으로 하나의 unified token stream에 합친 뒤 Transformer encoder-decoder로 압축하고, modality별 VQ codebook(visual 2048, pose·action 각 64)으로 이산화해 kinodynamic intent 어휘를 학습함.
- 이산 codebook 후보를 continuous flow matching decoder로 매핑해 실행하는 이원 구조를 제안함 — planning은 discrete manifold 안에서, 실행은 continuous 공간에서 수행함.
- Kinematic-Perceptual Cost(KPC)는 geometric goal distance, visual goal distance, unbiased expert prior의 negative log-likelihood, visual token entropy, VQ quantization error 다섯 항으로 후보를 평가함 — quantization error와 predictive entropy를 pixel decode 없는 충돌 감지 신호로 사용함.
- Gumbel-max 기반 iterative latent search(coarse-to-fine annealing)로 후보를 반복 정제하고, 최종 elite 후보만 flow matching으로 한 번 디코딩해 실행함.

**Novelty vs. prior works**

- 가장 가까운 baseline인 NWM은 continuous latent를 pixel로 decode해 LPIPS로 candidate를 평가하는데, Hydra는 평가 자체를 decode 없이 discrete latent 공간(quantization error, entropy)에서 수행한다는 점이 핵심 차이고 real-time 제약이 있는 navigation에 실질적인 이득을 줌.
- discrete latent world model 자체는 DreamerV3·IRIS에 이미 있다고 저자도 인정하며, 이를 cost function과 결합해 실제 real-time 로봇 planner로 만든 것이 저자가 내세우는 기여인데 개념적으로는 discrete world model과 MPC의 조합에 가까워 도약폭이 크지는 않음.
- WorldPlanner(MCTS+play data)와 달리 tree 구조가 아니라 representation 자체를 discretize한다는 차이를 강조하지만, VQ-VAE 기반 world model 자체는 이미 널리 쓰이는 기법이라 navigation 도메인에 처음 적용한 응용적 기여로 보는 편이 정확함.

**Benchmark results**

- planning 성능(Jackal·Spot, 각 10 trial)에서 Hydra(143M 파라미터)는 계획 시간 약 0.9초, NWM/B(200M)는 500초 이상 — VertiFormer(continuous MPPI)는 0.7초로 빠르지만 NWM/B와 마찬가지로 장애물 있는 환경 두 시나리오 모두 0/10 성공으로 충돌을 회피하지 못함.
- Hydra는 unobstructed 10/10, obstructed 8/10, corner turn 8/10 성공 — 단 8m 내외의 close-range navigation task에 한정된 평가임.
- video synthesis 품질(FVD, teacher-forcing 100 clip)에서 Hydra 19.16 vs NWM/B 22.11, VertiFormer 81.03으로, discrete bottleneck에도 불구하고 장기 temporal consistency가 오히려 더 좋게 나옴.
- local path following(Spot, 각 10 trial, 3개 시나리오)에서 Hydra의 sparse waypoint 기반 variant가 dense goal-image 기반 reactive baseline(GNM·ViNT·NoMaD)과 동등하거나 나은 성공률을 보였으나, Long Distance 시나리오에서 CFG variant의 traversal time(138±7.7초)은 오히려 reactive baseline보다 느림.
- KPC 개별 항목(Cprior, Cent, Cvq)이 obstacle avoidance에 기여한다는 ablation table은 본문 추출 과정에서 표가 누락돼 구체 수치는 본문에서 확인 불가하고, 정성적 사례(Fig.4)로만 quantization error·entropy가 장애물 접근 시 함께 상승·하강함을 확인함.

**Top-tier conference 적합성 — 74/100 · 추천 venue: CoRL**

실로봇 두 플랫폼에서 500배 속도 개선과 명확한 baseline 대비 성공률 이득을 보여 실용적 기여가 뚜렷하고 코드·가중치도 공개함. 다만 discrete VQ world model 자체는 기존 기법의 재조합이고 8m 내외 close-range navigation에 한정된 평가라 long-horizon 일반화 근거가 약한 것이 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- decode 없이 latent 안에서 quantization error·entropy로 OOD·충돌을 감지하는 아이디어는 우리 lab의 failure detection 연구에 그대로 적용 가능함 — manipulation domain에서도 codebook distance를 failure signal로 쓸 수 있음.
- discrete latent 탐색과 continuous flow matching 실행을 나누는 이원 구조는 test-time planning 속도를 높이는 general한 패턴이라 우리 world model 연구의 real-time inference 최적화에 참고할 수 있음.
- early-fusion vs in-context alignment 비교(VertiFormer 대비)는 VLA의 multimodal token 설계 논쟁과 직결돼 manipulation VLA 연구에서 modality fusion 방식을 정할 때 참고할 실측 근거임.

---

### 7. [74점] AnyWorld: Factorized Egocentric World Models for Cross-Embodiment Generalization

- **분야**: World Model / Cross-Embodiment Manipulation · **robotics relevance**: 9/10
- **arXiv**: [2608.29242](https://arxiv.org/abs/2608.29242) ([PDF](https://arxiv.org/pdf/2608.29242))
- **저자**: Cheng Chen, Jerry Bai, Jiacheng Wei, Boyu Chen, Xiaoji Zheng, Fan Wu, Minghao Yang, Tianrun Chen 외 6명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Project page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 사람 1인칭 영상 하나를 action·camera·embodiment 세 요소로 분해해 다양한 로봇 시점·바디의 rollout으로 재구성하는 world model AnyWorld를 제안함. RoboCasa GR1 시뮬레이션과 실제 IRON 휴머노이드에서 VLA 정책 성능을 개선함.

**Core innovation & methodology**

- 상호작용을 action(스켈레톤 control video), camera(Plücker ray embedding), embodiment(첫 프레임+텍스트 태그)로 분해해 사람 영상 하나로 여러 로봇 rollout을 zero-shot 생성함.
- WAN Fun-Control 14B 기반 latent diffusion video model에서 action은 채널 concat, camera는 patch embedding에 additive, embodiment는 cross-attention으로 각기 다른 방식으로 주입함.
- EgoDex 대규모 human video pretraining 후 unpaired human-robot mixed fine-tuning(2:1 비율)으로 학습해 human-robot paired demo 없이 재구성이 가능함.
- 생성된 관찰과 human wrist trajectory를 로봇 end-effector action으로 재보정한 action calibration을 결합해 VLA 적응용 video-action pair를 만듦.

**Novelty vs. prior works**

- 가장 가까운 prior work인 DreamDojo(human video 기반 generalist world model)와 달리, action/camera/embodiment를 독립적으로 재구성 가능한 축으로 명시적으로 분해해 embodiment·viewpoint·scene을 따로 통제하는 점이 본질적 차이임.
- Xskill, EgoMimic류 human-to-robot transfer 연구는 latent representation·retargeting 학습에 그치고 완전한 robot-native 비디오를 렌더링하지 않는데, AnyWorld는 완결된 영상-액션 쌍을 생성함.
- factorized conditioning 자체는 world model 문헌에서 이미 흔한 기법이라 조합과 zero-shot cross-embodiment 적용이 novelty의 중심이고, representation·objective 자체의 신규성은 제한적임.

**Benchmark results**

- controllability 평균(ActionAlign/CameraAlign/EmbodAcc)에서 AnyWorld 0.778로 WAN Fun-Control 0.609, Cosmos-Predict2.5 0.417 대비 우세함.
- RoboCasa GR1 18개 pick-and-place task에서 UniT 베이스라인 49.8%→54.6%(+4.8pt)로 개선함(시뮬레이션).
- 실제 IRON 로봇 20회 banana-grasping trial에서 20.0%→55.0%(+35.0pt)로 개선함, 다만 단일 task·소규모 trial(20회)이라 통계적 안정성은 제한적임.
- human:robot 비율 ablation(60개 held-out case로 통제된 별도 평가 subset, 메인 벤치마크 0.778과는 다른 subset)에서 2:1이 controllability 평균 0.740으로 최적이며 4:1(0.706)·1:1(0.723)보다 우수해 최종 모델의 2:1 비율 선택을 뒷받침함.
- 저자가 명시한 한계: tactile/contact force는 반영 못 하고, 평가는 EgoDex/RoboCasa GR1/IRON 3개 embodiment에 국한되며 action-camera 추출은 occlusion·빠른 motion에 취약함. 코드/모델 공개 여부는 본문에서 확인 불가.

**Top-tier conference 적합성 — 74/100 · 추천 venue: CoRL**

human video를 조건부 재구성해 로봇 데이터 스케일링 문제를 정면으로 다루고 실제 휴머노이드 검증까지 갖춰 CoRL 강점이 큼. 다만 핵심 ablation 다수가 정성적 사례 연구 수준이고 IRON 실험 규모가 작아 실험적 conviction 면에서 rejection risk가 남음.

**추천 이유 & 누리랩 연구와의 연결점**

- world model/test-time optimization 관점에서, factorized 조건으로 human video를 재구성하는 방식은 로봇 실패 상태(partial completion 등)를 표적 합성하는 데이터 엔진으로 응용 가능함.
- failure detection/recovery 연구에 붙이면 counterfactual visual-action pair 생성 도구로 활용해 policy gap을 겨냥한 학습 데이터를 만들 수 있음.
- object-centric 3DGS/scene graph 파이프라인과 결합해 scene recomposition 축을 3D representation 기반으로 확장하는 방향을 검토할 만함.

---

### 8. [73점] Lucida: Parse, Generate, and Place for Composable Real-to-Sim Scene Modeling

- **분야**: 3D Vision / Real-to-Sim Scene Modeling · **robotics relevance**: 8/10
- **arXiv**: [2608.30821](https://arxiv.org/abs/2608.30821) ([PDF](https://arxiv.org/pdf/2608.30821))
- **저자**: Minghan Qin, Yuang Wang, Xiuyu Yang, Yushi Long, Yujian Zhang, Ruihuan Wang, Kai Ye, Yangang Zhang 외 1명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: Project Page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 real-to-sim scene modeling을 parse-generate-place 순서는 유지하되 각 단계가 요구하는 입력 정밀도를 낮추고 마지막 배치 단계에서 정밀도를 확보하도록 재설계한 Lucida를 제안함. 3D 편집기에서 물체를 이동·회전·스케일하는 조작 위젯인 gizmo를 다루는 VLM 기반 closed-loop 정책 GizmoAct로 R2S-Scene mAP를 Boxer 대비 69% 개선하고 scene F-Score를 0.794(SAM 3D)에서 0.924로 올림.

**Core innovation & methodology**

- scene parsing을 covisibility 기반 keyframe 선택 → VLM object discovery → full-sequence evidence consolidation → relation-aware scene refinement로 구성해 객체별 multi-view evidence bundle을 담은 scene graph를 만듦.
- amodal object asset generation에서 가려진 부분을 point cloud completion 대신 multi-view 기반 image editing으로 완성한 뒤 image-to-3D 모델로 자산화함.
- GizmoAct는 3D grounding을 3D 에디터의 gizmo 조작 GUI multi-turn interaction으로 재정의해 회전/이동/스케일을 gizmo 로컬 프레임 기준 상대값으로 예측하고 스스로 stop을 판단함.
- GizmoAct는 synthetic expert trajectory SFT(DART 스타일 error injection 포함) 후 GRPO 기반 RL(quantized IoU/rotation reward)로 학습되어 mismatched asset·coarse initialization에서도 재학습 없이 동작함.

**Novelty vs. prior works**

- SAM 3D, RecGen 같은 기존 파이프라인은 shape와 pose를 동시에 예측하거나 정밀한 instance geometry를 앞단에서 요구하는데, Lucida는 요구조건을 파이프라인 끝(GizmoAct)으로 미루는 problem reformulation이 핵심 차별점임.
- 3D grounding·pose estimation을 render-and-compare가 아니라 스스로 정지 시점을 판단하는 GUI 조작형 VLM 정책으로 formulate한 점은 기존 6/9-DoF pose estimation 문헌과 본질적으로 다른 틀임.
- 개별 구성요소(scene graph 구축, image-to-3D lifting, GRPO 기반 refinement policy)는 각각 선행 기법(DART, DAPO, FoundationPose 등)의 재조합에 가까워 전체 시스템 통합이 novelty의 중심이고 완전히 새로운 representation은 아님.

**Benchmark results**

- R2S-Scene(자체 구축 벤치마크) 3D object detection에서 mAP가 all-protocol 0.351(Boxer)→0.592, filter-protocol 0.355→0.597로 개선됨(외부에서 재현 검증은 아직 불가한 자체 벤치마크).
- CA-1M object pose estimation에서 ADD-SB@0.05가 57.8%(RecGen)→83.4%, 3D IoU 0.434→0.607로 개선됨.
- R2S-Object에서 ADD-SB@0.05 79.2%→92.0%, 3D IoU 0.500→0.719로 개선됨. 초기화 방식(Boxer/Any6D/SAM 3D)이 달라도 재학습 없이 동작함을 확인함.
- scene reconstruction 종합 평가에서 scene F-Score 0.794(SAM 3D)→0.924, object F-Score 0.704→0.736로 개선됨.
- 저자가 예고한 3.4절 scene-parsing/GizmoAct 학습전략 ablation과 conclusion/limitations 절 본문은 PDF 텍스트 추출 과정에서 누락되어(레퍼런스 구간으로 바로 이어짐) 본문에서 확인 불가하며, 실물 로봇 조작 실험은 보고되지 않음(전부 3D reconstruction 지표).

**Top-tier conference 적합성 — 77/100 · 추천 venue: CVPR**

real-to-sim 파이프라인 재설계와 GizmoAct의 GUI형 pose refinement가 CVPR급 vision 문제로서 설득력 있고 benchmark 개선폭이 크다. 다만 R2S 벤치마크가 자체 구축이라 재현성 검증이 어렵고 ablation·limitation 절이 텍스트에서 확인되지 않아 실패 사례와 robustness 한계를 판단하기 어려운 점이 리스크임.

**추천 이유 & 누리랩 연구와의 연결점**

- object-centric 3DGS/scene graph 연구와 직결됨: evidence bundle 기반 scene graph 구조는 누리랩 semantic mapping 파이프라인에 real-to-sim 자산 생성 모듈로 바로 결합 가능함.
- GizmoAct의 closed-loop, self-stopping 정책 설계는 test-time optimization/active perception(다음 뷰 선택, 언제 충분한지 스스로 판단) 연구에 참고할 만한 패턴임.
- 생성된 simulation-ready 자산은 manipulation policy의 real-to-sim-to-real 학습 데이터로 바로 활용 가능함.

---

### 9. [71점] Scaffolding Foundation Models into Physical-World Agents Pushes the Frontier of Long-Horizon Navigation

- **분야**: Navigation / Embodied Question Answering · **robotics relevance**: 9/10
- **arXiv**: [2608.30396](https://arxiv.org/abs/2608.30396) ([PDF](https://arxiv.org/pdf/2608.30396))
- **저자**: Zixing Lei, Gengze Zhou, Xiong-Hui Chen, Jiazhao Zhang, Yiyang Huang, Hang Yin, Haoqi Yuan, Qi Wu 외 2명
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **Comments**: 22 pages, 6 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 66점

> 💡 장기 탐색을 위해 VLM 추론 에이전트가 navigation foundation model(NFM)을 intent·observation·memory 세 채널로 감싸는 NavMCP를 제안함. HM-EQA·MT-HM3D·EXPRESS-Bench에서 SOTA를 달성했고 실물 Unitree Go2에서 78.3% 성공률, horizon이 길어질수록 baseline 대비 격차가 10→45pt로 벌어짐.

**Core innovation & methodology**

- episodic tool interface의 세 한계(instruction-intent mismatch, intermediate observation loss, cross-call accumulation 부재)를 각각 해소하는 intent/observation/memory 세 채널을 설계함.
- intent channel은 evidence need를 mode+sub-goal+budget+constraint로 구조화된 navigation call로 변환해 VLM이 low-level control 없이 탐색 의도만 지정하게 함.
- observation channel은 rollout 전체에서 keyframe(4-step stride, 최대 16장)을 샘플링해 VLM summarizer로 source-grounded journey artifact를 만들어 종료 시점 정보 손실을 막음.
- memory channel은 EQA context state(H_t, E_t, U_t: history, evidence ledger, unresolved goal)를 유지해 여러 navigation call에 걸쳐 탐색 이력을 누적함.

**Novelty vs. prior works**

- 가장 가까운 비교 대상은 FAST-EQA/ToolEQA 등 tool-augmented EQA 시스템인데, 이들은 navigation을 terminal outcome으로만 소비하는 episodic interface를 쓰는 반면 NavMCP는 rollout 중간 관찰과 negative evidence까지 구조화해 재사용함.
- VLM+NFM을 재학습 없이 결합하는 구조(reasoning agent가 low-level executor를 호출) 자체는 이미 많은 tool-use/embodied agent 연구의 패턴이라, novelty는 새로운 architecture보다 NFM을 위한 3채널 protocol 설계에 있음.
- episodic interface로 되돌리는 ablation(74.0%→59.1%, -14.9pt)으로 protocol 설계의 기여를 직접 분리해 측정한 점은 실험적 근거가 강함.

**Benchmark results**

- cross-benchmark 비교에서 HM-EQA 76.7%(FAST-EQA 69.2% 대비 +7.5pt), MT-HM3D 54.4%(+3.9pt), EXPRESS-Bench LLM Score 79.27(+10.57pt)/E_path 33.96(+4.71pt)로 개선됨(sim 벤치마크, 결과는 저자 보고치와 혼재해 cross-paper 비교임을 저자도 명시함).
- 동일 agent(Qwen3.5-397B-A17B) 기준 matched 비교에서도 NavMCP 74.0%로 FAST-EQA reproduction 63.5% 대비 +10.5pt 우세함.
- ablation에서 agent capability를 없애면(No Agent) 38.2%로 급락하고 executor를 Random Walk로 바꾸면 60.9%로 하락해 VLM agent와 NFM executor가 상호보완적임을 확인함.
- protocol ablation에서 전체를 episodic interface로 바꾸면 -14.9pt, observation을 terminal-only로 바꾸면 -5.9pt, memory state 제거 시 -4.6pt로 memory·observation 채널의 기여가 가장 큼.
- 실물 Unitree Go2 실험(low/medium/high horizon 각 20 episode)에서 NavMCP 78.3% 대 frontier exploration 48.3%, reactive 38.3%로 horizon이 길어질수록 격차가 10→25→45pt로 커짐(6개 task 유형, episode당 10~20회로 규모는 크지 않음). 저자가 명시한 한계는 큰 VLM 의존으로 인한 느린 추론과 cross-view duplication으로 인한 counting 오류(HM-EQA Count 카테고리 65.0%로 최저)임.

**Top-tier conference 적합성 — 73/100 · 추천 venue: CoRL**

세 벤치마크 SOTA와 통제된 ablation, 실물 로봇 실험까지 갖춰 실험적 근거가 탄탄함. 다만 두 개의 기성 foundation model(VLM+NFM)을 재학습 없이 프로토콜로 엮은 시스템 논문이라 새로운 학습 패러다임이나 representation을 제안하지는 않아 top-tier oral 경쟁에서는 엔지니어링 기여로 평가받을 가능성이 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- robot memory/failure detection 연구와 직접 연결됨: EQA context state(evidence ledger+unresolved goal)는 로봇 실패 상황에서 '무엇을 확인했고 무엇이 안 됐는지'를 추적하는 memory 구조로 manipulation failure diagnosis에 응용 가능함.
- long-horizon skill chaining/TAMP 연구에서 reasoning VLM과 low-level executor를 분리하는 3채널 protocol 패턴은 현재 navigation 전용이지만 manipulation VLA에도 적용해 볼 수 있음.
- negative evidence 누적 및 스스로 멈출지 판단하는 구조는 active perception/NBV 연구와 비교·확장할 가치가 있음.

---

### 10. [70점] Does Latent Planning Survive Point Clouds? Action-Conditioned JEPA World Models for Geometric Observations

- **분야**: World Model / 3D Representation · **robotics relevance**: 9/10
- **arXiv**: [2608.29434](https://arxiv.org/abs/2608.29434) ([PDF](https://arxiv.org/pdf/2608.29434))
- **저자**: Fabio F. Oberweger, Michael Schwingshackl
- **카테고리**: Machine Learning (cs.LG) · 신규 목록 게재: cs.LG
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 이 논문은 이미지에서만 검증되던 JEPA world model 세 가지 설계(frozen-encoder, distribution-prior, action-sensitive)를 point cloud 관측으로 그대로 옮기고, stable-worldmodel benchmark를 point cloud로 재-sensing해 이미지 baseline과 통제 비교함. distribution-prior 모델(Point-LeWM)은 4개 벤치마크 중 3개에서 이미지 버전과 통계적으로 동등했고(Push-T에서만 유의한 차이), action-sensitive 모델(Point-Delta-JEPA)은 씬에서 가장 많은 점이 움직이는 조건에서 이미지 버전보다도 높은 성공률을 보임.

**Core innovation & methodology**

- JEPA 세 가지 canonical 설계 — frozen-encoder(Utonia-WM), distribution-prior(Point-LeWM), action-sensitive(Point-Delta-JEPA) — 를 point cloud 인코더로 재구현해 각 설계의 anti-collapse 메커니즘이 point cloud에서도 유지되는지 검증함.
- stable-worldmodel의 4개 image 환경을 raycast range sensor로 재-sensing함 — episode·action·goal은 동일하게 두고 관측만 point cloud로 교체해 modality를 통제 변수로 격리함.
- 3D target(예: cube의 xyz 위치)만으로 goal latent를 만드는 target-to-latent module을 제안함 — 현재 latent를 함께 조건으로 넣어, 방문한 적 없는 goal observation 없이도 planning이 가능하게 함.
- linear·MLP probing으로 latent가 object position을 거의 완벽히 디코딩 가능함(R²≥0.95)을 보이고, attention이 소수의 움직이는 point에 집중함을 확인해 collapse가 일어나지 않는 이유를 설명함.

**Novelty vs. prior works**

- 기존 point cloud world model(PointWorld, 3D Point World Models)은 explicit geometry로 decode해 planning cost를 계산하는데, 이 논문은 decode 없이 action-conditioned latent 공간에서 곧바로 planning한다는 점이 핵심 차이임.
- AD-L-JEPA는 point cloud에서 latent JEPA를 학습하지만 action-free이고 fine-tuning으로만 평가되는 반면, 이 논문은 action-conditioned 학습과 실제 planning(CEM)까지 닫아 point cloud에서 action-conditioned latent world model을 planner와 결합한 최초 사례라는 저자 주장이 관련 연구 검토 범위 내에서는 타당해 보임.
- 다만 세 JEPA design 자체는 이미지 도메인에서 이미 확립된 것을 point cloud 인코더로 옮긴 것이라, 새로운 objective나 learning paradigm을 제안하지는 않고 modality 전이가 되는지를 검증하는 실증 논문에 가까움.

**Benchmark results**

- Point-LeWM(distribution-prior)이 이미지 LeWM과 4개 벤치마크 중 3개(Two-Room, Reacher, OGB-Cube)에서 통계적으로 동등, Push-T에서만 2.8점 유의한 차이(83.6 vs 86.4) — CEM 1회 solve 시간도 0.53초 vs 0.48초로 거의 동일함.
- Point-Delta-JEPA(action-sensitive)가 OGB-Cube(움직이는 점 비율 최다, 약 15%)에서 83.4±3.8로, protocol이 다른 비통제 비교이긴 하나 이미지 버전 보고치(79.3±1.8)보다도 높았고 Two-Room에서는 100.0±0.0으로 saturate함.
- Utonia-WM(frozen encoder)은 Two-Room 94.0으로 최고지만 manipulation 성격의 Push-T에서 46.6으로 가장 약함 — 학습을 전혀 하지 않는 대조군 Vox-WM 대비로는 전 벤치마크에서 +7.8~16.8점 우위임.
- perturbation ablation에서 학습 시 본 적 없는 25~50% dropout에는 강건(Point-LeWM Two-Room에서 clean 대비 99% 유지)하지만, range noise(scan extent의 0.25~0.5%)는 얇은 구조가 지배적인 Push-T에서 두 모델 모두 성공률을 clean 대비 5% 이하로 붕괴시킴.
- target-to-latent module은 4개 환경 모두에서 goal cloud reference와 seed noise 범위 내로 일치했으나, 이 결과는 4개의 simulated tabletop 환경과 노이즈 없는 idealized sensor에서만 검증된 것임.

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

통제된 재-sensing benchmark와 엄밀한 통계 검정(2.8점 차이도 유의성 검증)으로 실험 신뢰도가 높음. 다만 4개 tabletop toy 환경과 idealized noise-free sensor에 한정되고 새로운 objective 제안 없이 기존 세 JEPA design을 modality만 바꿔 검증한 논문이라 top-tier full paper의 conceptual leap 기준에는 다소 못 미침.

**추천 이유 & 누리랩 연구와의 연결점**

- point cloud에서 곧바로 action-conditioned latent planning이 가능하다는 결과는 우리 lab의 object-centric 3DGS·scene graph 연구에 world model 백엔드로 재사용할 근거가 됨.
- target-to-latent module(3D 좌표만으로 goal latent 생성)은 goal observation 없이 목표를 지정하는 인터페이스라 goal-conditioned manipulation 실험에 바로 적용 가능함.
- attention이 소수 moving point에 집중한다는 probing 결과는 active perception·NBV 연구에서 어디를 관측할지를 latent attention으로 유도하는 아이디어와 연결됨.

---

### 11. [68점] Motus2: A Self-Evolving General World Model for Dexterous Manipulation

- **분야**: World Model / Dexterous Manipulation · **robotics relevance**: 10/10
- **arXiv**: [2608.30237](https://arxiv.org/abs/2608.30237) ([PDF](https://arxiv.org/pdf/2608.30237))
- **저자**: Hongzhe Bi, Zihao Zhou, Yihang Tang, Jingrui Pang, Shuhe Huang, Haitian Liu, Runqing Wang, Shuai Huang 외 11명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 Motus2는 하나의 shared-weight 모델에서 policy·simulator·evaluator 세 인터페이스를 노출하는 dexterous manipulation general world model임. candidate action 생성→미래 관측 예측→가치 평가로 이어지는 closed decision-and-learning loop를 구성함. 약 130K시간 규모 egocentric(단안→스테레오) human data로 pretrain한 뒤 로봇 데이터로 mid-training해 5개 실로봇 task 평균 성공률을 WAN-SFT 0%에서 84%로 끌어올렸고, MBRL(DiffusionNFT)과 test-time planning을 결합해 별도 2개 task에서 65%를 75%까지 추가로 개선함.

**Core innovation & methodology**

- 하나의 shared-parameter 모델에서 action-first factorization(policy→simulator→evaluator 순서)으로 세 인터페이스를 분리함 — action 예측이 미래 observation과 value 신호를 보지 못하게 mask를 설계함.
- trajectory-dependent supervision routing을 제안함 — 성공한 시연만 action imitation target으로 쓰고, 실패·suboptimal trajectory는 clean conditioning으로만 남겨 simulator·evaluator 학습에 재활용함.
- VLAC 스타일 relative-progress reward(rt=Δt/(T-t))로 evaluator를 학습하고, 이 value 추정을 DiffusionNFT 기반 model-based RL 업데이트와 Best-of-N test-time planning 양쪽에 모두 사용함.
- long-horizon partial observability 대응으로 global autoregression과 MemoryWAM 스타일 hybrid memory 두 방식을 비교하고, T-Rex 스타일 tactile expert로 backbone K/V cache를 재사용해 contact-aware action refinement를 추가함.

**Novelty vs. prior works**

- 선행 연구 Motus가 이미 UniDiffuser 스타일로 policy와 simulator를 한 모델에 결합했는데, Motus2의 핵심 기여는 evaluator(value model)를 세 번째 인터페이스로 추가해 model-based RL closed loop를 완성한 것임 — 방향은 명확하나 policy·simulator·evaluator를 한 backbone에 통합한다는 아이디어 자체는 world model 문헌의 자연스러운 확장이라 개념적 도약폭은 크지 않음.
- egocentric data scaling을 단안에서 스테레오로 확장한 scaling law 검증은 실증적으로 유의미하나, monocular egocentric scaling 자체는 이미 보고된 바 있어(H-RDT, EgoVLA 등) 점증적인 확장에 가까움.
- tactile expert는 T-Rex의 기존 방법을 그대로 재사용했다고 저자가 명시하고 있어 이 부분의 novelty는 낮음.

**Benchmark results**

- 5개 real-robot task(각 20 rollout)에서 π0.5·WAN-SFT는 0%인데 egocentric pretrain만 거친 Pretrain-SFT는 51%, robot-domain mid-training까지 마친 Motus2는 84% — π0.5·WAN-SFT는 egocentric pretrain 없이 target-task 데이터만 쓴 극단적 baseline이라는 점에 주의.
- MBRL·planning factorial 실험(Put Phone, Multi-Finger 각 20 rollout)에서 planning만 65.0%→67.5%(+2.5%p), MBRL만 65.0%→72.5%(+7.5%p), 둘 다 적용 시 75.0% — task가 2개뿐이라 일반화 근거로는 제한적임.
- long-horizon context 비교(Find Square·Press Button, 시뮬레이션 25 rollout, 실로봇 20 rollout)에서 global autoregression이 hybrid memory보다 시뮬레이션 78% vs 52%, 실로봇 57.5% vs 25.0%로 크게 앞섬 — memory를 압축하는 방식이 오히려 크게 불리했다는 결과임.
- tactile expert ablation(Pull Out Paper Cup, Tear Paper 각 20 rollout)에서 60.0%→72.5%(+12.5%p) 개선됐으나 task가 2개뿐임.
- stereo egocentric data scaling law는 2k~20k시간 구간에서 L*_val(D)≈0.101-0.005lnD로 로그선형 감소를 확인했는데, 저자도 이 hour 단위가 필터링 전 raw hour라 실제 학습량은 더 작다고 명시함.

**Top-tier conference 적합성 — 65/100 · 추천 venue: CoRL**

biomimetic dual-arm dual-hand tactile 플랫폼에 실제로 구현하고 model scaling·data scaling 양쪽을 다룬 시스템 논문으로서의 완성도는 높음. 다만 핵심 ablation 대부분이 task 2개에 대해서만 이뤄져 통계적 근거가 약하고, evaluator 추가 외의 아이디어는 대체로 기존 요소의 결합이라 top-tier oral 기준의 conceptual leap은 부족함.

**추천 이유 & 누리랩 연구와의 연결점**

- policy·simulator·evaluator를 action-first mask로 한 backbone에서 분리하는 설계는 우리 world model·test-time optimization 연구에 바로 적용할 아키텍처 패턴임.
- 실패·suboptimal trajectory를 imitation target이 아니라 dynamics·value 학습에만 라우팅하는 방식은 failure detection·recovery 연구에서 실패 데이터를 버리지 않고 활용하는 방법으로 참고할 만함.
- global autoregression이 압축형 hybrid memory보다 크게 앞선 실측 결과는 우리 robot memory 연구에서 압축 방식을 고를 때 주의할 반례로 인용할 수 있음.

---

### 12. [68점] Blind Dexterity: Whole-Body Humanoid Manipulation via Pure Proprioception

- **분야**: Manipulation · **robotics relevance**: 9/10
- **arXiv**: [2608.29487](https://arxiv.org/abs/2608.29487) ([PDF](https://arxiv.org/pdf/2608.29487))
- **저자**: Aditya Bhatt, Oleg Kaidanov, Puze Liu, Jan Peters
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 9 pages, 6 figures. Project page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 65점

> 💡 카메라·촉각·force-torque 센서 없이 관절 인코더 신호만으로 Unitree G1 휴머노이드가 축구공 트래핑, 여행가방 들기, 스케이트보드 탑승 같은 접촉 기반 whole-body 조작을 학습함. compliant PD control 하에서 명령-측정 관절각 차이가 접촉 정보를 담는다는 점을 이용해 순수 proprioception만으로 active exploration과 물체 pose 추정이 가능함을 실증함.

**Core innovation & methodology**

- encoder-as-tactile 가설: position-PD control에서 명령된 관절 목표와 실제 관절각의 잔차(residual)가 토크에 비례하므로, 순응 접촉 시 관절 인코더 신호 자체가 전신 촉각 채널로 기능한다는 관점을 제시함
- 정책 관측에 이전 명령 action(a_t-1)을 포함해야 이 신호를 활용할 수 있음을 IMU/이전 action 제거 실험으로 확인함
- 정책과 완전히 분리된 task-specific state estimator(MLP)를 학습해, 접촉 이후 물체 pose 추정 오차가 급격히 줄어드는지 진단 도구로만 사용함(정책 gradient에 영향 없음)
- Isaac Sim + PPO(RSL-RL), asymmetric actor-critic, domain randomization으로 4개 과제를 학습 후 실물 G1에 정성적으로 배치함

**Novelty vs. prior works**

- proprioception만으로 legged locomotion이 가능하다는 결과 자체는 이미 알려져 있으나(RMA 계열), 이를 whole-body manipulation(물체 조작)까지 확장한 문제 설정의 novelty가 큼
- 가장 가까운 선행연구(Miller et al., NeurIPS 2025)는 시뮬레이션에서 proprioception+단순 tactile로 reach/manipulate를 학습했지만 real-world 전이가 없음; 이 논문은 real robot 정성 검증까지 포함해 차별화됨
- 방법론 자체는 새 architecture나 learning paradigm 제안 없이 표준 PPO+MLP+asymmetric actor-critic을 그대로 사용하므로, 기여는 알고리즘이 아니라 관측 신호의 재해석과 실증에 있음

**Benchmark results**

- 축구공 트래핑(4096 episode, 5 seed 평균): privileged 99.8%, distilled(DAgger) 31.2%, blind-SE 92.9%, blind+SE 86.5%
- 스케이트보드 탑승: privileged 28.1%(seed 민감성 큼), distilled 8.2%, blind-SE(state estimator 미결합) 88.2%, blind+SE(state estimator 결합) 89.7%(pose error 0.098, 단위 본문에서 확인 불가)
- 여행가방 들기: privileged 95.5%, distilled 34.6%, blind 조건 중 최고는 blind+VS-SE 88.3%(tipping 18.8%); variable stiffness가 tipping을 약 4~5pp 낮춤
- IMU-free 보행: +IMU+PE(이전 action 관측 포함, PE=previous-action) 생존율 96.1% vs -IMU+PE 90.4% vs -IMU-PE(이전 action 관측 제거) 89.1%; a_t-1 제거 시 속도 추적과 관성 추정 오차가 크게 악화됨
- 정량 평가는 전부 시뮬레이션(4096 병렬 환경)이며, 실물 로봇 결과는 고정 프로토콜 하의 성공률이 아니라 정성적 데모 영상 수준임; 코드·모델 공개 여부는 본문에서 확인 불가(프로젝트 페이지만 언급됨)

**Top-tier conference 적합성 — 64/100 · 추천 venue: RSS**

카메라 없이 whole-body humanoid manipulation을 실물까지 정성 검증한 시스템 논문으로 실용적 임팩트가 강점이며 실물 데모로 적용 가능성을 보임. 다만 알고리즘 기여가 표준 PPO 조합에 그치고 실물 성공률이 고정 프로토콜로 보고되지 않아, top-tier에서는 oral보다 poster/시스템 트랙에 가까운 채택 가능성이 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- interactive perception과 active perception(NBV) 연구에 직접 참고할 사례임: 접촉을 능동적으로 만들어 상태 추정 불확실성을 줄이는 방식은 실패 복구 시 로봇이 스스로 재탐색하는 정책 설계에 응용 가능함
- vision 기반 VLA가 occlusion·조명 저하로 실패할 때 proprioceptive contact 신호를 보조 modality로 fusion하는 fallback 전략의 아이디어로 연결됨
- 정책과 분리된 diagnostic state estimator 구조는 world model이나 robot memory 연구에서 "물체 상태를 별도 head로 추정해 관측 가능성을 평가"하는 패턴으로 재사용 가능함

---

### 13. [68점] PRACTICE: From Experience to Expertise in Self-Evolving Embodied Agents

- **분야**: Embodied Agent 스킬 학습 (MLLM 기반 task planning, experience-augmented agent) · **robotics relevance**: 8/10
- **arXiv**: [2608.30760](https://arxiv.org/abs/2608.30760) ([PDF](https://arxiv.org/pdf/2608.30760))
- **저자**: Ziyi Bai, Siqi Li, Tinglei Huang, Börje F. Karlsson
- **카테고리**: Machine Learning (cs.LG) · 신규 목록 게재: cs.LG
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 고정된 prompt-engineered 규칙 대신 학습 가능한 skill learner가 과거 trajectory에서 ADD/REVISE/MERGE/REMOVE 형태의 구조화된 skill 편집을 생성하도록 curriculum SFT와 on-policy distillation으로 학습함. executor는 얼려둔 채 skill 라이브러리만 계속 진화시켜 EB-ALFRED와 EB-Habitat에서 기존 experience 기반 방법들을 앞섬.

**Core innovation & methodology**

- 스킬 라이브러리 관리를 고정된 prompt-engineered workflow가 아니라 학습 가능한 정책(skill learner)으로 대체함. skill learner가 trajectory와 현재 라이브러리를 보고 구조화된 batch-edit(ADD/REVISE/MERGE/REMOVE)을 생성하고 task executor는 frozen 상태로 유지함
- 2단계 curriculum SFT 구조: Stage0은 성공한 oracle trajectory로 기본 skill 생성·편집·통합을 학습하고, Stage1은 같은 task에 대한 8개 이종 executor의 성공·실패 trajectory를 대조해 invalid condition과 failure recovery 전략을 학습함
- Skill OPD(on-policy distillation) 단계: skill learner 자신이 생성한 rollout에서 방문한 context에 대해 더 큰 teacher(Qwen3-VL-32B)의 top-K forward KL을 맞춰 train-inference 분포 불일치를 줄임. task reward나 policy gradient는 쓰지 않음
- skill card는 action pattern sequence와 usage specification(적용 조건, 실패 시 recovery 전략)으로 구조화돼 실행 중 실패가 발생하면 저장된 invalid condition과 매칭해 recovery action을 호출함

**Novelty vs. prior works**

- 가장 가까운 선행연구는 AutoSkill, Trace2Skill, MemCompiler 같은 prompt 기반 skill·memory maintenance 방법들임. 본질적 차이는 유지보수 정책 자체를 학습 가능하게 만든 것과, 실패 trajectory를 성공 trajectory와 명시적으로 대조해 recovery 전략을 학습 신호로 넣은 점임
- skill learner의 아키텍처 자체는 표준 MLLM(Qwen3-VL-8B) SFT와 distillation이라 새로운 representation이나 learning paradigm은 아니고, 학습 신호 조합(성공/실패 대조, teacher distillation)에서의 novelty에 가까움
- executor를 계속 frozen으로 두는 설계는 스킬 학습과 정책 학습을 분리해 깔끔하지만, executor 자체의 능력 향상은 다루지 않아 ELITE 같은 executor post-training 방법과는 대체재가 아니라 상호보완 관계임

**Benchmark results**

- EB-ALFRED에서 평균 success rate 49.7%(Qwen3-VL-32B executor)로 최강 experience-augmented baseline인 MemCompiler(40.0%) 대비 9.7%p 개선. EB-Habitat에서는 58.3% vs MemCompiler 55.7%로 2.6%p 개선
- ablation(EB-ALFRED): No Skill 24.3% → Initial skill(BPE(byte pair encoding)로 초기화한 skill library) 40.7% → Stage0 SFT 42.3% → Stage1 failure-aware SFT 45.3% → Stage2 Skill OPD 49.7%로, 학습 단계(Stage0→1→2) 중에서는 OPD의 증분(+4.4%p)이 가장 큼
- failure-aware 학습의 순수 효과: 성공 trajectory만 추가한 조건(42.3%→42.7%, +0.4%p)과 비교해 실패 trajectory를 대조 학습에 포함하면 45.3%(+2.6%p)로 개선되고, Long-horizon split에서 6%→14%로 가장 크게 개선됨
- cross-executor 일반화: GPT-5.2, Gemini-3-Flash, Qwen3-VL-32B에서 각각 +30.3%p, +15.3%p, +25.4%p 개선. 이미 강한 executor인 GPT-5.4에는 +2.4%p로 상대적으로 작은 개선폭을 보임
- 모든 실험은 EmbodiedBench의 EB-ALFRED/EB-Habitat 시뮬레이션(각 6개 split)에 한정되며 real robot 실험은 없음. 프로젝트 페이지(baai-agents.github.io/PRACTICE)로 코드·리소스가 공개된 것으로 명시됨

**Top-tier conference 적합성 — 62/100 · 추천 venue: AAAI**

학습 가능한 skill maintenance 정책이라는 formulation이 명확하고 여러 executor에서 일관된 개선을 보인 것이 강점임. 다만 evaluation이 텍스트·시뮬레이션 기반 EmbodiedBench에 한정되고 실로봇 검증이 없어 manipulation 난이도가 낮다는 게 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- 실패 trajectory를 성공과 대조해 recovery 전략을 구조화된 skill card에 저장하는 방식은 누리랩의 failure detection/recovery 연구에 바로 응용 가능하며, real robot manipulation의 실패 유형별 recovery skill 라이브러리로 확장할 수 있음
- executor를 frozen으로 두고 skill layer만 학습하는 구조는 VLA policy 자체를 재학습하지 않고 test-time에 procedural knowledge를 주입하는 test-time optimization 아이디어와 연결됨
- skill learner를 teacher distillation으로 훈련하는 Skill OPD 방식은 robot memory 시스템에서 학생 정책이 자기 rollout 분포 위에서 학습하도록 만드는 on-policy 학습 참고 사례로 쓸 수 있음

---

### 14. [63점] The Intervention Gap in Latent World Models

- **분야**: World Model 평가·감사 방법론 (RL / latent world model) · **robotics relevance**: 9/10
- **arXiv**: [2608.29998](https://arxiv.org/abs/2608.29998) ([PDF](https://arxiv.org/pdf/2608.29998))
- **저자**: Donna Vakalis
- **카테고리**: Machine Learning (cs.LG) · 신규 목록 게재: cs.LG
- **Comments**: 21 pages, 10 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 학습된 world model이 reward는 잘 맞히면서도 실제 개입(intervention)이 task 변수를 움직이는 방식은 전혀 다르게 예측할 수 있다는 것을 capture-gated 감사 프로토콜로 보임. TD-MPC2·LeWorldModel·PreJEPA·DreamerV3에 이 프로토콜을 적용해 reward fit이나 task-anchored 학습만으로는 이 결함이 드러나지도 방지되지도 않음을 확인함.

**Core innovation & methodology**

- 'planning-time intervention fidelity' 개념 제안: 학습된 world model의 open-loop rollout이 실제 환경 개입(do-operator)과 같은 방향으로 task 변수를 움직이는지를 측정하며, reward fit이나 task-anchored 학습으로는 보장되지 않는다는 것이 핵심 주장임
- capture-gated matched-intervention audit 설계: Gate1(현재 상태에서 task query가 readout으로 capture되는지), Gate2(matched intervention의 real effect가 frozen readout으로 resolve되는지), Gate3(모델 자신의 imagined rollout이 실제 효과와 얼마나 일치하는지)의 3단 게이트로 실패 원인을 분리함
- released TD-MPC2 체크포인트 사이즈 스윕에서 episode return과 operator error의 순위상관 -0.90, 같은 구간에서 reward-prediction error는 [0.03, 0.09]로 거의 flat함을 보여 reward fit이 operator 오류를 못 잡아낸다는 것을 입증함
- Cheetah에서 LeWorldModel 3개 체크포인트가 현재 query는 capture하지만 5-step 상상된 효과는 predicted R2 -6.33~-3.36으로 zero-effect 예측보다도, environment-endpoint oracle보다도 나쁨. task 방향 성분이 거의 직교(cosine 0.85~0.89인 전체 feature 변화와 대조)로 뒤틀리고 1.7~2.6배 과다 증폭되는 'task-direction rotation with excess gain'으로 특징지음

**Novelty vs. prior works**

- 가장 가까운 선행연구는 value-equivalent model learning(Farahmand, Grimm)과 discrete automaton에서 implicit transition을 평가한 Vafa et al.(2024)임. 이 논문은 continuous control에서 실제 환경 intervention과 매칭된 연속형 진단을 제안한 것이 차별점임
- 새로운 학습 방법이나 representation은 제안하지 않음. gate 순서(capture→real-effect resolvability→propagation)로 실패 원인을 분리하는 평가 방법론이 기여의 전부이고, 새 representation·objective 제안 없이 진단 프로토콜만 제시한다는 한계가 있음
- 결과가 conditional함을 스스로 강조함: LeWorldModel의 심각한 실패 패턴이 PreJEPA에서는 재현되지 않고, 아키텍처 전체에 대한 일반화 주장이 아니라 candidate·task·seed별로 다르다는 점이 스코프의 한계이자 동시에 저자가 명시한 신중함임

**Benchmark results**

- TD-MPC2 체크포인트 5개(1M~317M) 사이즈 스윕: operator error 상승과 episode return 하락의 순위상관 -0.90(95% CI [-0.90, -0.70]), 317M 모델은 reward fit이 스윕 내 최상위인데 operator error는 최악이고 return이 붕괴함
- self-supervised LeWorldModel(3 seed)이 task-anchored TD-MPC2보다 operator error가 약 0.457배로 낮음(같은 Cheetah task). 다만 model family가 2개, anchored seed 1개뿐이라 저자도 architecture ranking으로 확대 해석하지 않음
- Cheetah/LeWorldModel 3개 체크포인트 모두 predicted-effect R2가 -6.33~-3.36으로 severe 조건(3/3) 충족. Cheetah/PreJEPA 5개 seed는 predicted R2 -0.005~0.064로 severe 조건은 0/5지만 oracle 대비 deficit은 5/5에서 유지됨
- DreamerV3에서 current query를 capture하는 유일한 native surface는 posterior logits(centered)뿐이며 샘플링된 categorical state·mode·deterministic recurrent state는 4개 체크포인트 전부에서 실패함
- ensemble disagreement는 task-policy support 근처에서만 에러와 상관(ρ=0.678)이 있고 environment-random support에서는 무상관(ρ=0.027). frozen support-aware score는 양방향 held-out transfer 모두에서 native disagreement 단독보다 성능이 나빠짐(paired ranking gain 모두 음수). 모든 실험은 DeepMind Control Suite(Cheetah, Finger Spin) 2개 sim task 한정이며 real robot 실험 없음, 코드·모델 공개 여부는 본문에서 확인 불가

**Top-tier conference 적합성 — 60/100 · 추천 venue: NeurIPS**

통계적으로 매우 엄격한 매칭-개입 감사 프로토콜을 제안하고 capture와 propagation을 분리해 실용적으로 유용한 결과를 냄. 다만 새 방법론이나 representation 제안 없이 DeepMind Control Suite locomotion 2개 task로 스코프가 좁아 로보틱스 커뮤니티 임팩트는 제한적이라는 rejection risk가 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- world model을 실로봇에 적용하기 전 'planning-time intervention fidelity' 감사 개념을 manipulation world model 신뢰성 검증·failure detection 연구에 프로토콜로 이식할 수 있음
- posterior distribution(logits)이 sample보다 query 정보를 더 잘 담는다는 결과는 robot memory·state representation 설계에서 discrete latent를 어떤 형태로 읽어야 하는지에 대한 실용적 지침이 됨
- ensemble disagreement가 training support 근처에서만 유효하다는 결과는 test-time optimization에서 OOD 상황의 uncertainty 신호 설계에 경고로 쓸 수 있고, do-operator 기반 개입 매칭 프레임은 counterfactual reasoning 연구에 그대로 연결됨

---

### 15. [55점] Flow-JEPA: Flow Matching for Robust Latent Dynamics in JEPA World Models

- **분야**: World Model · **robotics relevance**: 8/10
- **arXiv**: [2608.29029](https://arxiv.org/abs/2608.29029) ([PDF](https://arxiv.org/pdf/2608.29029))
- **저자**: Yanchen Huo, Ziying Song, Yadan Luo
- **카테고리**: Machine Learning (cs.LG) · 신규 목록 게재: cs.LG
- **원문 검토**: PDF 전문 · 1차 스크리닝 66점

> 💡 LeWorldModel(LeWM)의 결정적 one-step autoregressive latent predictor를 conditional flow matching으로 바꿔 미래 latent trajectory 전체를 한번에 생성하는 F-JEPA를 제안함. Two-Room·Reacher·Push-T·OGBench-Cube 4개 시뮬레이션 환경에서 clean 조건 평균 성공률을 86%에서 92%로, 배경 국소 노이즈를 준 noisy 조건에서는 67%에서 86%로 올림.

**Core innovation & methodology**

- LeWM의 두 한계인 one-step rollout의 오차 누적과 deterministic point-wise regression을 지적하고, 이를 conditional flow matching 하나로 함께 해결함
- action-conditioned 미래 latent trajectory 전체를 단일 joint variable로 취급해 Gaussian source에서 clean trajectory로 이동하는 velocity field를 학습함(recursive dependency 제거)
- encoder의 representation collapse를 막는 SIGReg(LeWM이 쓰는 representation-collapse 방지 정규화)는 그대로 유지하고, predictor만 AdaLN 기반 Transformer flow matching model로 교체함
- inference 시 8 step Euler ODE integration으로 미래 latent를 생성하고 CEM 기반 MPC로 planning에 사용함

**Novelty vs. prior works**

- 핵심 기여는 새 representation·objective 발명이 아니라 이미 확립된 flow matching(Lipman et al. 2022)을 LeWM이라는 특정 JEPA world model의 predictor에 적용한 것임
- world model에 flow matching을 쓰는 접근 자체는 동시기 연구(Porcher et al. 2026, feature-space flow matching)와 개념적으로 겹쳐 novelty가 제한적임
- 대신 task-irrelevant visual perturbation에 대한 JEPA world model의 취약성을 실증적으로 부각시키고 이를 정량 개선한 점은 실용적 기여로 볼 수 있음

**Benchmark results**

- clean 조건 평균 성공률: LeWM 86% -> F-JEPA 92% (Two-Room 87->100, Reacher 86->90, Push-T 96->96 동률, OGBench-Cube 74->82)
- noisy 조건(국소 Gaussian 패치 노이즈) 평균 성공률: LeWM 67% -> F-JEPA 86%, clean 대비 저하폭이 19pp에서 6pp로 축소됨
- perturbation 강도(patch radius, noise std)를 바꾼 ablation 전 구간에서 F-JEPA가 대체로 우위를 유지해 특정 세팅에 국한된 개선이 아님을 보임
- 4개 환경 모두 시뮬레이션(DeepMind Control Reacher, Push-T, OGBench-Cube, 자체 Two-Room)이고 real-robot 검증은 없으며, 환경당 평가 rollout은 50회로 규모가 작음
- F-JEPA는 LeWM 대비 planning 1 cycle당 약 3.8배 느리지만 재계획 횟수가 줄어 전체 rollout 기준으로는 약 1.6배 격차로 완화됨; 코드는 공개됨(GitHub)

**Top-tier conference 적합성 — 42/100 · 추천 venue: ICLR**

실험 설계와 ablation(perturbation 강도, flow step, CEM 반복 수)이 꼼꼼하고 재현성 문서화도 잘 되어 있어 workshop이나 poster 수준 채택은 가능함. 다만 방법이 기존 flow matching을 기존 architecture에 적용한 module 교체 수준이고 sim 4개·소규모 rollout·real-robot 부재라 top-tier oral 채택 가능성은 낮음. 저자 스스로도 ICLR 2027 work-in-progress로 표기함.

**추천 이유 & 누리랩 연구와의 연결점**

- world model의 시각적 perturbation 강건성 문제는 failure detection·recovery와 직결되며, sim-to-real에서 조명·배경 변화에 강한 latent dynamics가 필요할 때 이 predictor 구조를 참고할 만함
- 미래 trajectory 전체를 flow matching으로 joint 생성하는 방식은 test-time에 여러 rollout을 stochastic하게 샘플링해 실패 가능성이 낮은 것을 고르는 test-time optimization에 응용 가능함
- 검증이 저해상도 sim 4개, real robot 미검증 수준이라 manipulation VLA에 바로 이식하기 전 실물 검증이 선행되어야 함

---

## 오늘의 핵심 연구 트렌드 종합

- **world model 신뢰성 진단** — [Can Video World Models Track Unobserved World States?](https://arxiv.org/abs/2608.30692), [The Intervention Gap in Latent World Models](https://arxiv.org/abs/2608.29998), [RoboPhys-3D](https://arxiv.org/abs/2608.28718) 세 편이 독립적으로 같은 결론에 도달함. 시각적으로 그럴듯한 rollout도 가려진 상태 추적·실제 개입(intervention) 효과·object localization에서는 크게 무너짐. reward fit이나 visual fidelity만으로는 world model의 실제 신뢰성을 보장하지 못함을 정량적으로 보임.
- **policy-simulator-evaluator 통합형 world model** — [Motus2](https://arxiv.org/abs/2608.30237)와 [Hydra](https://arxiv.org/abs/2608.28995)가 world model을 real-time planning·evaluation에 직접 결합함. Hydra는 discrete latent 공간에서 decode 없이 후보를 평가함. NWM 대비 500배 빠른 계획을 실로봇에서 검증함.
- **world model의 modality·robustness 확장** — [JEPA point clouds](https://arxiv.org/abs/2608.29434), [Flow-JEPA](https://arxiv.org/abs/2608.29029), [AnyWorld](https://arxiv.org/abs/2608.29242)는 새 objective 없이 기존 JEPA/world model을 point cloud 관측, 시각 perturbation, cross-embodiment human video로 옮기는 실증형 확장 연구임.
- **gradient 없는 test-time 적응·기억** — [Zeva](https://arxiv.org/abs/2608.30880)는 memory retrieval만으로, [PRACTICE](https://arxiv.org/abs/2608.30760)는 학습 가능한 skill 편집만으로 policy weight를 건드리지 않고 반복 시도·경험에서 성능을 끌어올림.
- **semantics를 실행 가능한 구조로 컴파일해 control-learning 파이프라인 전체에 공급** — [SUN](https://arxiv.org/abs/2608.31167)·[Temporal Forcing](https://arxiv.org/abs/2608.30643)·[NavMCP](https://arxiv.org/abs/2608.30396)는 각각 관계·시간 정보·탐색 의도를 구조화된 표현으로 한 번 정의해 이후 단계(제어·학습·평가)에 재사용하는 동일 원리를 공유함.
- **vision 없이 접촉만으로 조작** — [Blind Dexterity](https://arxiv.org/abs/2608.29487)는 카메라·촉각 센서 없이 관절 인코더 잔차만으로 whole-body contact-rich manipulation이 가능함을 실물 휴머노이드로 보임.

## 유망 연구 방향 및 프로젝트 제안

**hidden-state tracking 실패를 실시간 failure signal로 전환**
- research question: manipulation world model이 가려진 물체 상태를 추적하지 못하는 지점이 실제 policy 실패와 상관관계를 갖는가, 그리고 이를 실행 중 감지할 수 있는가.
- 접근·novelty: Shell Game류 진단 벤치마크([Can Video World Models Track](https://arxiv.org/abs/2608.30692))를 occlusion-heavy manipulation task로 이식하고, RoboPhys-3D의 3D reconstruction 기반 state-level metric과 결합해 hidden-state tracking 오류를 failure detector의 입력 신호로 재정의함.
- 왜 지금·경쟁 prior works: 오늘 세 편이 독립적으로 world model 신뢰성 결함을 보였지만 아직 이를 실시간 failure signal로 활용한 연구는 없음. Hydra의 quantization error/entropy를 failure trigger로 쓰는 아이디어와 조합 가능.
- risk·target venue: Shell Game류 진단 벤치마크 이식과 RoboPhys-3D metric 결합의 재현 난이도가 높고 sim 검증에 그칠 위험이 큼. CoRL/RSS 타겟.

**실패 전용 causal memory로 test-time recovery 확장**
- research question: Zeva의 dual-timescale causal memory(BIT+PIM)를 성공 경험이 아니라 실패 trajectory 축적에 특화하면 recovery 성공률이 오르는가.
- 접근·novelty: PIM의 유사도 기반 merge를 실패 사례 클러스터링으로 재설계하고, retrieval 결과를 다음 action이 아니라 recovery action 후보 생성에 사용함.
- 왜 지금·경쟁 prior works: Zeva·PRACTICE 모두 gradient 없는 test-time 적응을 보였지만 실패 복구에 특화된 메커니즘은 아님.
- risk·target venue: real robot 반복 시행 비용이 크고 in-context window 크기에 제약받음. CoRL.

**semantic program predicate를 실행 중 진단 신호로 재사용**
- research question: SUN Program처럼 관계를 한 번 정의해 컴파일하는 방식을 이용해 학습된 vision policy 실행 중 "어느 stage에서 왜 실패했는지"를 실시간 판별할 수 있는가.
- 접근·novelty: SUN의 typed predicate를 policy rollout에 attach해 stage mismatch·false-completion 감지로 확장하고, 감지 결과를 recovery skill 호출 조건으로 연결함(SUN 저자도 관련 확장을 future work로 언급).
- 왜 지금·경쟁 prior works: ReKep·OmniManip(keypoint·constraint 기반 manipulation 선행연구)은 control 단계에 머물고 policy로 넘어가면 semantics를 잃는다는 한계를 SUN이 지적했으나, failure diagnosis로의 응용은 아직 검증되지 않음.
- risk·target venue: registered scene frame·typed operator library를 사전 정의해야 해 open-vocabulary 일반화가 제한됨. CoRL/RSS.

**discrete latent world model의 quantization error를 manipulation replanning trigger로 이식**
- research question: Hydra가 navigation에서 보인 decode-free discrete latent evaluation(quantization error, entropy)을 manipulation domain에 옮기면 real-time failure-aware replanning이 가능한가.
- 접근·novelty: Motus2의 policy-simulator-evaluator shared backbone에 Hydra의 discrete latent quantization cost를 결합해, 후보 action의 codebook distance를 replanning 트리거로 사용함.
- 왜 지금·경쟁 prior works: 두 논문 모두 오늘 발표됐고 discrete latent planning을 manipulation에 적용한 사례가 아직 없음.
- risk·target venue: manipulation의 접촉 다양성이 navigation보다 커 codebook 설계가 어려울 수 있음. CoRL.

**4D temporal alignment 기반 자기 진단 VLA**
- research question: Temporal Forcing의 4D geometric alignment로 얻은 history latent가 task progress를 명시적으로 담고 있다면, 별도 head 없이 policy가 스스로 실패·미완료를 감지하고 멈출 수 있는가.
- 접근·novelty: history pathway alignment는 유지한 채 stage completion/실패 감지 head를 추가해, inference 시 4D foundation model을 제거한 경량 구성에서도 자기 진단이 가능한지 검증함.
- 왜 지금·경쟁 prior works: 저자들은 이 alignment를 성능 개선에만 썼고 자기 진단 활용은 다루지 않음. HAMLET·MemoryVLA(기존 메모리 기반 VLA 선행연구) 대비 direct supervision 방식의 새로운 활용처가 됨.
- risk·target venue: 4D foundation model 학습·정렬 비용이 크고 real robot 검증 규모가 작음(hidden-placement task 1종). CoRL/ICRA.

## 오늘 반드시 읽어야 할 논문

- [Zeva: In-Context Causal Learning for Generalizable Embodied Manipulation](https://arxiv.org/abs/2608.30880) — gradient 없이 memory retrieval만으로 실로봇 성공률을 26%→73%까지 올린 test-time adaptation 사례임.
- [Can Video World Models Track Unobserved World States?](https://arxiv.org/abs/2608.30692) — 시각 품질과 hidden state tracking이 별개 능력임을 명확한 진단 벤치마크로 입증함.
- [Temporal Forcing: 4D Representation Alignment for Vision-Language-Action Models](https://arxiv.org/abs/2608.30643) — 4D geometry alignment로 history가 실제로 유효해진다는 것을 통제 실험으로 보인 VLA 논문임.
- [SUN: Persistent Programs For Language-Grounded Control-to-Learning-to-Real Policies](https://arxiv.org/abs/2608.31167) — 관계를 한 번 정의해 MPC·RL·BC·진단에 동시 컴파일하는 구조로 실물 로봇까지 zero-shot 전이함.
- [Hydra: A Navigation World Action Model with Discrete Latent Planning and Continuous Flow-Matching Execution](https://arxiv.org/abs/2608.28995) — decode 없는 discrete latent 평가로 real-time navigation planning을 실로봇 2종에서 검증함.
- [RoboPhys-3D: A Comprehensive Embodied World Model Evaluation via 3D Reconstruction](https://arxiv.org/abs/2608.28718) — 생성·ground-truth 영상을 동일 파이프라인에 통과시켜 world model의 시각적 그럴듯함과 실제 state 정확도를 분리한 벤치마크임.
- [AnyWorld: Factorized Egocentric World Models for Cross-Embodiment Generalization](https://arxiv.org/abs/2608.29242) — human video를 action/camera/embodiment로 분해해 로봇 rollout으로 재구성하는 world model임.
- [Motus2: A Self-Evolving General World Model for Dexterous Manipulation](https://arxiv.org/abs/2608.30237) — policy·simulator·evaluator를 한 backbone에서 분리해 model-based RL closed loop를 완성함.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (927편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2608.30880'>Zeva: In-Context Causal Learning for Generalizable Embodied Manipulation</a></td><td>78</td><td>10</td><td>Manipulation</td><td>정책을 freeze한 채 실제 물리 상호작용에서 causal interaction signal을 뽑아 dual-timescale memory에 저장하고 배포 중 gradient 없이 self-evolve하는 in-context causal learning임 - test-time adaptation과 robot memory를 동시에 다루는 새 formulation으로 우선 주제와 정확히 맞음</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2608.30237'>Motus2: A Self-Evolving General World Model for Dexterous Manipulation</a></td><td>72</td><td>10</td><td>World Model</td><td>정책·시뮬레이터·평가자를 하나의 가중치 공유 모델로 노출해 폐루프 의사결정-학습을 구성한 world model임. egocentric에서 로봇 도메인으로 데이터 스케일링하고 촉각까지 결합한 바이오미메틱 플랫폼에서 검증해 world model·조작·test-time 우선주제 전반에 강하게 부합함.</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2608.29434'>Does Latent Planning Survive Point Clouds? Action-Conditioned JEPA World Models for Geometric Observations</a></td><td>72</td><td>9</td><td>World Model</td><td>포인트클라우드에 세 가지 JEPA world model을 이식해 collapse 없이 계획이 되는지 검증하고 3D 목표를 latent로 직접 구성한 연구라 world model·3D 표현·planning을 잇는 핵심 관심사와 정확히 맞음</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2608.28995'>Hydra: A Navigation World Action Model with Discrete Latent Planning and Continuous Flow-Matching Execution</a></td><td>72</td><td>9</td><td>World Model</td><td>시각·자세·행동을 하나의 discrete latent manifold로 압축해 픽셀 디코딩 없이 계획·평가하는 구조를 제안함. discrete latent planning과 flow matching 실행을 결합해 실제 로봇 두 종에서 검증한 점이 world model 활용한 test-time planning의 새로운 접근임.</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2608.30692'>Can Video World Models Track Unobserved World States?</a></td><td>72</td><td>8</td><td>World Model</td><td>video world model이 숨은 상태를 토큰이 아니라 아키텍처 내부에 유지해야 함을 shell game으로 보인 분석이라 world model 설계에 핵심적인 시사점을 줌</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2608.29998'>The Intervention Gap in Latent World Models</a></td><td>70</td><td>9</td><td>World Model</td><td>TD-MPC2, DreamerV3 등 latent world model이 실제 개입과 일치하는 반사실적 예측을 하는지 검증해 task-direction rotation이라는 실패모드를 찾은 연구라 world model 평가·counterfactual reasoning 관심사와 정확히 일치함</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2608.30760'>PRACTICE: From Experience to Expertise in Self-Evolving Embodied Agents</a></td><td>70</td><td>8</td><td>Embodied AI</td><td>과거 궤적에서 skill을 add/refine/merge하는 skill learner를 학습해 실행기는 고정한 채 지속 개선하는 구조를 제안함. 성공·실패 궤적 대비를 통한 회복 전략 학습이 실패 탐지·회복과 스킬 체이닝 우선 주제에 직접 부합하고 EB-ALFRED/EB-Habitat에서 검증함.</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2608.28718'>RoboPhys-3D: A Comprehensive Embodied World Model Evaluation via 3D Reconstruction</a></td><td>68</td><td>9</td><td>World Model</td><td>3D 재구성 파이프라인을 공유해 생성 오류와 재구성 오류를 분리하는 EWM 평가 프로토콜을 제안함. RoboTwin 2.0 기반 50개 조작 태스크로 검증하고 사람 평가와 높은 상관을 보여 world model 평가 인프라로서 기여가 큼.</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2608.29242'>AnyWorld: Factorized Egocentric World Models for Cross-Embodiment Generalization</a></td><td>68</td><td>9</td><td>World Model</td><td>상호작용을 action·camera·embodiment로 분해해 인간 영상 하나를 다양한 로봇 조작 rollout으로 확장하는 world model 프레임워크임. RoboCasa와 실제 IRON 휴머노이드에서 정책 개선을 확인해 cross-embodiment 데이터 스케일링 문제에 대한 강한 실험적 근거를 제공함.</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2608.30643'>Temporal Forcing: 4D Representation Alignment for Vision-Language-Action Models</a></td><td>68</td><td>9</td><td>VLA</td><td>history를 4D foundation model 기하 표현에 정렬시켜 observation aliasing 문제를 해결한 4D representation alignment임 - LIBERO 98.8%, 실물 hidden-placement task 20→43.3%로 개선폭 뚜렷함</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2608.30821'>Lucida: Parse, Generate, and Place for Composable Real-to-Sim Scene Modeling</a></td><td>68</td><td>8</td><td>Embodied AI</td><td>비디오에서 장면을 파싱-자산생성-배치까지 잇는 real-to-sim 파이프라인이고 VLM 정책으로 배치를 GUI 상호작용처럼 처리해 embodied AI 시뮬레이션 자산 구축에 직접 유용함</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2608.30396'>Scaffolding Foundation Models into Physical-World Agents Pushes the Frontier of Long-Horizon Navigation</a></td><td>66</td><td>9</td><td>Navigation</td><td>VLM 추론 에이전트와 navigation foundation model 실행기를 결합해 장기 탐색을 지속적 memory로 이어감, Unitree Go2 실로봇에서 horizon이 길어질수록 baseline 대비 격차가 10점에서 45점까지 벌어짐을 보임</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2608.29029'>Flow-JEPA: Flow Matching for Robust Latent Dynamics in JEPA World Models</a></td><td>66</td><td>8</td><td>World Model</td><td>JEPA world model의 결정적 autoregressive 예측을 flow matching으로 바꿔 노이즈 상황에서 조작 성공률을 67%에서 86%로 올린 결과라 world model 강건성에 직접 관련됨</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2608.29487'>Blind Dexterity: Whole-Body Humanoid Manipulation via Pure Proprioception</a></td><td>65</td><td>9</td><td>Manipulation</td><td>카메라·촉각 센서 없이 관절 인코더만으로 축구공 트래핑·가방 들기 등 접촉 풍부한 전신 조작을 수행함. 순응 접촉이 고유수용감각을 촉각 채널로 만든다는 새로운 통찰을 실제 휴머노이드에서 검증함.</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2608.31167'>SUN: Persistent Programs For Language-Grounded Control-to-Learning-to-Real Policies</a></td><td>64</td><td>8</td><td>Manipulation</td><td>기하·접촉 관계를 한 번 정의해 MPC cost·RL reward·전이 조건까지 동시에 컴파일하는 SUN Program으로 symbolic planning과 data-driven policy를 통합함 - 9개 태스크에서 sparse reward 대비 82% vs 36%로 격차 크고 실물 Franka/Kinova 검증도 있음</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2608.30897'>CAER: Causal Action Effect Reweighting for World Model Training</a></td><td>64</td><td>8</td><td>World Model</td><td>action-conditioned world model 학습에서 action이 실제로 바꾸는 토큰에만 supervision을 재배분하는 CAER를 제안함, action 유무 예측 차이로 causally affected 영역을 온라인 특정하는 방식이 새로운 학습 paradigm에 해당하고 물리적 일관성·제어성이 일관되게 개선됨</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2608.29967'>Training-Free Action Correction for VLA Model Failures via Language Feedback</a></td><td>62</td><td>9</td><td>VLA</td><td>정책 재학습 없이 태스크 수준 언어 교정을 행동 크기 보정으로 변환하는 방법임. 실패 유형을 execution misalignment와 semantic 실패로 나눠 교정 가능 경계를 명시하고 실로봇에서 검증해 failure recovery·language feedback 우선주제에 정확히 부합함.</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2608.29078'>DREAM: Deployment-Time Demonstration Generation via Real-to-Sim for Scalable Policy Adaptation</a></td><td>62</td><td>8</td><td>VLA</td><td>사람 시연 없이 워크스페이스 재구성과 TAMP로 VLA fine-tuning 데이터를 자동 생성하는 배포시점 적응 방법임. 실로봇 실험으로 human teleoperation 대비 비용 이점을 검증해 VLA 데이터 확보 문제에 실질적 해법을 제시함.</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2608.29601'>$\mathcal{N}_0$-Foundation: Towards the Age of Tactile Intelligence</a></td><td>62</td><td>8</td><td>Manipulation</td><td>6개 embodiment 450개 태스크에 걸친 3만 시간 규모 시각-촉각 데이터셋과 센서 간 전이 가능한 촉각 표현모델을 구축함. tactile 우선주제의 인프라 스케일이 커서 후속 연구 파급력이 큼.</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2608.30935'>LightNav-0: Eliciting VLM Spatial Intelligence for Generalist Embodied Navigation</a></td><td>62</td><td>8</td><td>Navigation</td><td>VLM의 spatial intelligence를 pointing·action tokenizer로 그대로 끌어와 임베디먼트 무관 generalist navigation을 만든 연구임 - 10개 시뮬레이션 벤치마크 SOTA에 실물 zero-shot 검증까지 포함해 근거가 탄탄함</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2608.30640'>Three Steps at a Time: Learning Representations from Action Sequences in Contrastive RL</a></td><td>62</td><td>6</td><td>RL</td><td>contrastive RL을 action chunk 단위로 확장해 offline/online 벤치마크에서 큰 폭 성능 향상을 보임. action chunk가 critic 표현에 미치는 영향을 분석한 점이 VLA의 action chunking과 직결됨.</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2608.29768'>SmoothRL: Online Reinforcement Learning During Asynchronous Execution</a></td><td>60</td><td>8</td><td>RL</td><td>비동기 action chunk 실행 구조를 학습 과정에 명시적으로 반영해 committed/execution/discarded 구간별로 gradient를 분리 전파하는 value-gradient RL 방법임. 실로봇 배포에서 실시간성과 온라인 적응을 동시에 다뤄 실용적 novelty가 있음.</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2608.29769'>Learning Agile Perceptive Traversal of Sparse 3D Structures for Humanoids</a></td><td>60</td><td>8</td><td>Embodied AI</td><td>헤드마운트 lidar와 attention encoder로 얇은 구조물을 인지하며 점프-브라키에이션-착지를 실제 휴머노이드에서 15회 중 14회 성공시킴. active perception과 agile whole-body control을 결합한 강한 실증 결과임.</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2608.30773'>Learning to infer and manipulate through distributed whole-arm interaction in a soft robot</a></td><td>60</td><td>8</td><td>Manipulation</td><td>soft robot의 분산 IMU만으로 blind grasping을 수행하는 physical intelligence 프레임워크로, POMDP 상황을 memory 기반 recurrent policy로 풀고 탐색·인식·파지를 end-to-end 학습함 - tactile 없이 순수 proprioception만 쓴다는 점이 흥미로움</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2608.30344'>Proximity3D: Shape from Capacitive Proximity on Sensing Manifold</a></td><td>60</td><td>7</td><td>Manipulation</td><td>곡면 정전용량 텍스타일 센서로 근접 형상을 복원하는 새 감지 원리라 로봇 근접·촉각 인지에 직접 연결됨</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2608.29937'>AcrossWAM1.0:A Modular Latent World-Action Stack for Compact Robot Policies</a></td><td>58</td><td>9</td><td>World Model</td><td>latent world-action stack(LaWAM)을 모듈화하고 소형 backbone으로 압축해 LIBERO에서 성능 유지를 확인함, 알고리즘 자체는 기존 formulation을 재현·정리한 수준이라 novelty는 제한적이나 compact VLA policy 배포 관점에서 실용적임</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2608.29003'>RoSe-SLAM: Robust Semantic-Aware Gaussian Splatting SLAM from Dynamic Monocular Videos</a></td><td>58</td><td>8</td><td>3D Vision</td><td>동적 단안 비디오에서 semantic feature를 distill한 Gaussian SLAM으로 dynamic distractor를 걸러내며 정확한 tracking·매핑을 함. IROS 2026 게재로 SLAM·scene understanding에 직접 기여함</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2608.28677'>Cognitively-Grounded On-Device Runtime Learning for Ground Robots in Unknown Physical Environments</a></td><td>58</td><td>8</td><td>Robot Learning</td><td>지도·사전지식 없이 edge 기기에서 actor-critic RL과 instance-based learning을 안전하게 블렌딩하는 온라인 학습 구조를 제안함. 사족보행 로봇과 오프로드 차량 실환경에서 검증해 test-time adaptation 우선주제에 부합함.</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2608.29537'>AGM: Achievement-Grounded Memory for Closed-Loop Agents with Frozen VLA Policies</a></td><td>58</td><td>8</td><td>VLA</td><td>물리적 증거로 검증된 후에만 진행 포인터를 갱신하는 폐루프 메모리로 frozen VLA의 open-loop 실행 문제를 해결함. 실로봇 검증까지 포함해 failure detection·회복 우선주제에 부합함.</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2608.30289'>CometVLA: Co-Training on an Embodied Data Pyramid towards Physical Understanding</a></td><td>58</td><td>8</td><td>VLA</td><td>로봇 action 도메인과 정렬된 physical VQA corpus/benchmark를 구축하고 GAP 토큰으로 VLM의 물리 이해를 action head에 전달함. VLM 물리 이해도와 VLA 성공률의 상관관계를 직접 검증한 점이 중요한 open question에 답함.</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2608.30955'>Learning Action Models with Conditional and Quantified Effects via Uncertainty-Guided Exploration</a></td><td>58</td><td>8</td><td>Manipulation</td><td>조건부·수량화 효과를 갖는 action model을 불확실성 기반 능동 탐색으로 온라인 학습하는 OHCAM을 제안하고 Kinova Gen3 실로봇 두 과제에서 검증함, TAMP에 필요한 action model 학습이라는 문제 설정이 명확하고 실로봇 검증도 있음</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2608.28733'>Generation of High-Level Concepts in 3D Scene Graphs via Autoregressive Diffusion</a></td><td>58</td><td>7</td><td>3D Vision</td><td>구조와 노드 특징을 함께 학습하는 autoregressive diffusion으로 3D scene graph를 bottom-up 생성함. 합성·실제 건축도면·로봇 센서 데이터 전반에서 기존 방법을 능가해 semantic mapping 우선주제에 부합함.</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2608.29516'>Task-Relevant Feature-Dynamics Fidelity Enables Zero-Shot Sim-to-Real Transfer for Robotic Ultrasound Scanning</a></td><td>58</td><td>7</td><td>Manipulation</td><td>프로브 동작에 따른 task-relevant feature dynamics fidelity라는 새 개념을 정의하고 contraction 이론으로 근거를 제시함. 400회 중 390회 zero-shot 성공이라는 강한 실험 결과로 뒷받침함.</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2608.29772'>Self-Aware Active Learning Enables Continual Improvement in Autonomous Driving</a></td><td>58</td><td>7</td><td>World Model</td><td>world model 기반 fear·curiosity 내재 신호로 개입 시점을 스스로 판단해 takeover 궤적으로 선택적 모방학습을 수행함. Waymo·CARLA·실제 모바일로봇까지 폭넓게 검증해 test-time 지속 개선이라는 우선주제에 부합함.</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2608.31025'>Analytic Dynamics: Learning Physics-Grounded Representation for Fast Intrinsic Dynamics Inference from Monocular Videos</a></td><td>58</td><td>6</td><td>World Model</td><td>물리 상태를 중간 표현으로 둬 monocular 비디오에서 feed-forward로 dynamics를 추론하는 physics-grounded 방법이라 조작 대상 물성 추론에 직접 연결됨</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2608.30067'>How do World Models and Policies Compose in LLM Agents? A Joint Spectral and Behavioral Account</a></td><td>58</td><td>3</td><td>World Model</td><td>LLM agent 안에서 world model과 policy 업데이트의 기하학적 관계를 분석함. embodied 로봇 실험 없이 텍스트 기반 controlled setting이라 로봇 적용성은 제한적임.</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2608.29881'>OptiGeo: Efficient Monocular Geometry for Embodied Perception in Optically Challenging Scenes</a></td><td>55</td><td>8</td><td>Manipulation</td><td>투명·반사·거울 등 로봇 배포 시 실패하는 단안 depth 추정을 clean-geometry teacher로 교정한 프레임워크임. embodied perception 실패 모드를 직접 다루고 30M 파라미터로 대형 모델을 능가하며 실제 내비게이션 검증도 함</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2608.30122'>Aligning Multi-Trajectory Supervision with Policy Optimization for VLA Driving</a></td><td>55</td><td>8</td><td>VLA</td><td>VLA 자율주행에서 다중 궤적 지도학습과 GRPO 정책최적화를 정렬시켜 advantage 오정합 문제를 해결함. Pareto 최적성 기반 궤적 필터링으로 NAVSIM에서 실패 사례를 유의미하게 회복해 VLA 정책학습에 직접 기여함</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2608.29432'>SMILE: Smooth Motion for Improved Long-Horizon VLA Execution</a></td><td>55</td><td>8</td><td>VLA</td><td>action chunk를 B-spline 계수로 표현해 여러 VLA 백본에 architecture 변경 없이 적용, LIBERO·CALVIN·실로봇에서 정확도와 속도를 동시에 개선함. 대표적 VLA 백본 다수에 검증한 범용성이 강점임.</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2608.29749'>DriftingVLA: Native One-Step Vision-Language-Action Generation via Per-Dimension Temporal Drifting</a></td><td>55</td><td>8</td><td>VLA</td><td>action 차원별로 별도 drifting unit을 두어 noise-to-action-chunk 직접 매핑을 학습, 반복 정제 없이 LIBERO 98.32% 등 강한 성능과 3.36배 속도 향상을 동시에 달성함.</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2608.30378'>PAVE: Predictive Alignment and Value-Guided Evolution for World-Action Policies</a></td><td>55</td><td>8</td><td>VLA</td><td>다중 시간축 JEPA 예측 목표와 분포형 value critic으로 배포 궤적의 좋고 나쁨을 구분해 flow-matching actor를 조건화함. 표현학습과 정책개선을 분리한 구조가 흥미로우나 시뮬레이션 벤치마크만 제시되고 일부 서술이 자리표시자로 남아있어 완성도가 떨어짐.</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2608.30983'>Autonomously Acquiring Robot Manipulation Skills with Language-Driven Quality-Diversity</a></td><td>55</td><td>8</td><td>Manipulation</td><td>자연어 설명만으로 LLM이 fitness·diversity 함수를 낮은 차원에서 자동 탐색해 QD 알고리즘을 구동하는 방법임 - 전문가 설계 없이 다양한 motion primitive 라이브러리를 얻는다는 formulation이 새로움</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2608.29910'>Matrix-Game 3.5: Enhancing Real-Time Streaming Interactive World Models with Patch Memory</a></td><td>55</td><td>6</td><td>World Model</td><td>geometry-aware patch memory와 정적·동적 분리 표현으로 실시간 인터랙티브 world model을 개선함. 로봇·embodied agent 응용을 명시하며 장기 일관성·카메라 제어를 다뤄 world model 연구 우선순위와 직접 맞음</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2608.30054'>When 3D Gaussian Splatting Recovers Real Surfaces</a></td><td>55</td><td>6</td><td>3D Vision</td><td>3DGS가 실제 표면을 복원하는 조건을 각도 용량과 parallax로 규명한 이론 프레임워크라 조작·플래닝에 필요한 정확한 3DGS 기하 신뢰성 판단에 참고됨</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2608.30406'>Locally-Guided Actor-Critic: Training a Goal-conditioned Actor with a Subgoal-aware Critic</a></td><td>55</td><td>5</td><td>RL</td><td>subgoal 기반 value 함수를 명시적으로 분해해 RIS/PBRS의 실패 사례를 해결한 goal-conditioned RL 방법임. long-horizon skill chaining과 맞닿아 있으나 실제 로봇 실험은 없음.</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2608.30423'>ObjectSplat: Improving Mesh Fidelity and Interactivity for 3D Scenes via Object-Level Mesh Splatting</a></td><td>54</td><td>6</td><td>3D Vision</td><td>장면을 인스턴스별로 분해 후 복원하는 object-level mesh splatting이라 조작 대상 자산의 object-centric 3D 표현에 직접 쓸 만함</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2608.29061'>PathBridger: Subgoal Bridges for Offline Goal-Conditioned Reinforcement Learning</a></td><td>54</td><td>6</td><td>Manipulation</td><td>subgoal 사이 state 경로를 명시적으로 잇는 offline goal-conditioned RL이고 multi-object cube manipulation에서 큰 개선을 보여 skill chaining에 직접 참고됨</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2608.30536'>Behavior-Skill: A Fine-Grained Benchmark for Evaluating Vision-Language-Action Policies in Long-Horizon Tasks</a></td><td>52</td><td>7</td><td>VLA</td><td>긴 호라이즌 mobile manipulation을 스킬 단위로 쪼갠 대규모 벤치마크(23만 인스턴스)로 pi0.5·GR00T 등 실패 지점을 스킬별로 드러냄 - VLA 실패 진단에 유용하나 새 방법론 제안은 아님</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2608.29904'>Off-Manifold Refinement: Guiding Video Generators with a Frozen World Model</a></td><td>52</td><td>6</td><td>World Model</td><td>frozen V-JEPA world model의 surprise 신호로 비디오 생성 궤적을 물리적으로 그럴듯한 쪽으로 교정하는 inference-time 기법임. world model을 이용한 test-time 안내라는 점에서 로봇 world model·정책 교정에 직접 참고할 만함</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2608.30451'>SeqAlign3DVG: A Sequence-Aligned Benchmark and Voxel Reasoning Framework for 3D Visual Grounding</a></td><td>52</td><td>6</td><td>Embodied AI</td><td>순서 정렬된 이미지 기반 3D visual grounding 벤치마크와 voxel memory 방법이라 embodied spatial reasoning에 바로 연결됨</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2608.29114'>CGFM-Nav: Cognitive Graph-Field Memory for Semantic-Guided Lifelong Multimodal Embodied Navigation</a></td><td>52</td><td>6</td><td>Navigation</td><td>명시적 관계 메모리와 semantic-frontier field를 결합해 GOAT-Bench 성공률을 53.2%에서 63.0%로 끌어올림. VLN에서의 robot memory 활용이라는 점에서 우선주제에 부합하나 preliminary 실험 규모임.</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2608.30883'>SleepWalking: Privileged Representation Shaping for End-to-End Blind Locomotion in Legged Robots</a></td><td>50</td><td>7</td><td>RL</td><td>partial observability를 아키텍처 분해가 아니라 정보 보존 문제로 재해석해 privileged reconstruction으로 recurrent representation을 shaping하는 legged locomotion 연구임 - 이론적 gap 분석까지 곁들였으나 도메인이 blind locomotion으로 좁음</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2608.28967'>Brain-Language-Action (BLA) Models: Language-Conditioned EEG for Robotics Control</a></td><td>50</td><td>6</td><td>Embodied AI</td><td>언어로 신경 상태와 행동 매핑을 동적으로 재정의해 적은 수의 EEG 클래스로 넓은 행동 공간을 커버하는 새로운 formulation임. 드론 제어 proof-of-concept 수준으로 검증 규모는 작음.</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2608.30220'>Contrast-Free Autonomous Navigation of Untethered Endovascular Microrobots Using Single-Plane Fluoroscopy</a></td><td>50</td><td>6</td><td>Navigation</td><td>단일면 형광투시만으로 3D digital twin 위 milestone 매칭을 통해 조영제 없이 마이크로로봇을 항법하는 방법임. 실제 쥐 체내 실험까지 포함한 강한 임상 검증이나 도메인이 매우 특화됨.</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2608.30870'>VCAR: Training-Free 3DGS Segmentation via View Completeness and Axis-Aware Boundary Refinement</a></td><td>50</td><td>5</td><td>3D Vision</td><td>학습 없이 뷰 완전성과 axis-aware 경계 보정으로 3DGS를 분할하는 방법이라 3DGS 기반 장면 이해에 바로 참고됨</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2608.31023'>SMG: Semantic Motion Graph for Monocular Dynamic Gaussian Splatting</a></td><td>50</td><td>5</td><td>3D Vision</td><td>semantic coherence 기반 저랭크 motion graph로 monocular dynamic 3DGS를 정규화한 방법이라 동적 장면의 object-centric 4D 표현에 참고할 만함</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2608.28724'>MANTLE: A Framework for Adaptive In-Situ Planetary Perception Using a Modular Uplink Principle</a></td><td>48</td><td>7</td><td>Embodied AI</td><td>화성 로버의 지형 분류·암석 분할을 위한 modular uplink 원칙임. 실제 행성탐사 로봇 배포 사례라 현장 로보틱스 관련성 높으나 방법 자체는 백본+헤드 조합 수준임</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2608.29177'>Dynamic-Robust Photometric-Semantic Reconstruction for Open-Vocabulary 3D Scene Understanding</a></td><td>48</td><td>6</td><td>3D Vision</td><td>동적 장면에서 novel view synthesis와 open-vocab segmentation을 함께 하는 feed-forward 모델임. semantic mapping·scene understanding에 직접 관련되고 ECCV 게재로 실험적 근거도 탄탄함</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2608.30690'>Failure or Drift? Evaluating Monocular SLAM under Synthetic and Real-World Corruptions</a></td><td>48</td><td>6</td><td>Navigation</td><td>합성·실제 corruption에서 monocular SLAM의 실패와 drift를 구분해 평가한 연구라 navigation failure detection에 직접 참고됨</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2608.29208'>AdaVLA: Adaptive Step Flow Matching for Training-free Acceleration of Vision-Language-Action Models</a></td><td>48</td><td>6</td><td>VLA</td><td>flow matching 궤적 곡률로 행동 생성 confidence를 정의해 학습 없이 추론 스텝과 MLP pruning을 동적으로 줄이는 방법임. VLA 가속이라는 점에서 효율화 방향이나 새로운 confidence 지표를 제안한 점은 단순 벤치마크 개선 이상임.</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2608.29379'>Bridging Semantics and Physics with Constrained LLMs for Safe and Trustworthy Robotic Manipulation</a></td><td>48</td><td>6</td><td>Manipulation</td><td>LLM 계획을 schema 기반 도구 호출로 제한하고 MoveIt으로 kinematic·collision 검증해 실행하는 구조임. 실제 로봇에서 pouring·grasp 태스크 성공률을 검증해 language-action gap과 안전 문제에 실질적으로 접근함.</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2608.30307'>ScenePilot: Grow-and-Repair Policy for Text-Driven 3D Indoor Scene Generation</a></td><td>48</td><td>5</td><td>Embodied AI</td><td>retrieval-augmented grow-and-repair로 3D indoor scene을 생성하는 정책이라 embodied AI 시뮬레이션 환경 구축에 쓸 수 있으나 로봇 실제 검증은 없음</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2608.31029'>Driving on Memory</a></td><td>48</td><td>5</td><td>Navigation</td><td>현재 장면 대신 과거 기억만으로도 NAVSIM 점수가 거의 유지된다는 걸 보여 자율주행 벤치마크의 타당성 자체에 의문을 제기한 비판적 분석임</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2608.30804'>Geometric Attractor Monitoring: A Robust and Frugal Framework for Multi-modal Industrial Robotic Cycles</a></td><td>48</td><td>5</td><td>Robotics</td><td>phase space reconstruction으로 산업 로봇 함대의 이상 징후를 조기에 잡아내는 방법임. 21대 실제 로봇 3년 데이터로 검증해 failure detection 주제에 부합하나 방법은 비학습 기반 고전적 접근임.</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2608.29228'>Localizing Emergent Failures in Agentic AI: Recovering Minimal Repair Families via Counterfactual Replay</a></td><td>48</td><td>3</td><td>NLP</td><td>multi-agent LLM 실패를 counterfactual replay로 최소 복구 집합까지 정확히 복원하는 방법을 제시함, failure diagnosis 방법론 자체는 로봇 멀티에이전트 시스템에도 전이 가능함</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2608.30428'>Lies We Can See: Joint Verbal and Non-Verbal Deception by VLM Agents in Embodied Social Interactions</a></td><td>47</td><td>5</td><td>Embodied AI</td><td>3D embodied 사회적 기만 게임에서 언어·비언어 채널을 함께 다루는 벤치마크임, VLM agent alignment에 새로운 문제 formulation 제시함</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2608.29207'>Hyper-Fold: Exploring the Expressive Limit of Sequence-Geometry Learning for Proteins via Hypergraph Modeling</a></td><td>47</td><td>0</td><td>LG</td><td>단백질 구조 예측에서 sequence-geometry 상호작용의 표현 한계를 이론으로 규명하고 이에 근접하는 경량 backbone을 제시함, 이론과 효율 양쪽에서 기여가 탄탄하나 도메인이 단백질에 한정됨</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2608.29562'>Asynchronous Cooperative Online Learning for Multi-Robot Control under Computational Delays</a></td><td>46</td><td>6</td><td>RL</td><td>계산지연이 있는 다중로봇 제어에서 GP 기반 협력학습을 비동기로 확장한 방법이고 USV 시뮬레이션으로 검증해 multi-robot learning에 직접 관련됨</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2608.29685'>Last Step Matters: Early Uncertainty Cannot Predict Failure in Long-Horizon Agents</a></td><td>46</td><td>5</td><td>Embodied AI</td><td>장기 에이전트에서 초기 불확실성이 실패를 예측 못하고 path switching 때문에 마지막 단계 confidence만 유효하다는 결과라 로봇 장기 태스크의 실패탐지 타이밍 설계에 시사점을 줌</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2608.28853'>Equivariant Sheaf Neural Networks: Learning Geometric Transport on Graphs</a></td><td>46</td><td>4</td><td>World Model</td><td>그래프 엣지의 방향성 전송을 학습하는 equivariant sheaf network로 입자 동역학·메시 시뮬레이션에서 성능을 높여 물리 시뮬레이션 표현학습에 참고될 만함</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2608.29028'>Facts Without Rules: Boundary Metadata Collapse in Multi-Agent LLM Handoffs</a></td><td>46</td><td>0</td><td>NLP</td><td>multi-agent LLM handoff에서 privacy 경계 정보가 사실 정보보다 먼저 유실되는 현상을 정의하고 측정함, 문제 정의는 참신하나 로보틱스와 무관함</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2608.29183'>Foundational feature fusion for conditional flow matching in 6D pose estimation</a></td><td>45</td><td>7</td><td>Manipulation</td><td>foundation model feature를 활용한 flow matching 기반 6D pose estimation임. task-specific encoder 학습 없이 BOP 벤치마크에서 SOTA 달성해 그래스핑에 바로 쓰일 수 있음</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2608.29315'>SGE: Semantically-Guided Exploration for Unstructured Environments via Image-Space Waypoint Sampling</a></td><td>45</td><td>6</td><td>Navigation</td><td>픽셀 수준 semantic segmentation을 waypoint 샘플링에 통합한 exploration 프레임워크로 광산 등 다양한 실환경에서 검증함. active perception 우선주제에 부합하나 방법 자체는 기존 모듈의 조합에 가까움.</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2608.29770'>Sampling-based Certified Planning with Graphs of Convex Sets</a></td><td>45</td><td>6</td><td>Manipulation</td><td>GCS 플래너의 확률적 collision-free 보장이 실제로는 큰 오답률을 낳는다는 것을 정량화하고, 클리어런스 인증 구를 이용한 무해상도 검증 플래너를 제안함. 기존 방법의 숨은 결함을 드러내고 해결한 점이 실질적 기여임.</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2608.28913'>mmIR: Frequency-Space Inverse Rendering for 3D Millimeter-Wave Radar ADC Synthesis</a></td><td>45</td><td>5</td><td>3D Vision</td><td>LiDAR 메시를 스캐폴드로 mmWave 레이더 ADC 신호를 물리 기반 미분가능 렌더링으로 합성함. 센서 시뮬레이션(world model)에 새로운 원리 제공하나 로봇 정책 적용은 아직 없음</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2608.29346'>GSPotential: Camera Potential Field for Sparse-View 3D Gaussian Splatting</a></td><td>45</td><td>5</td><td>3D Vision</td><td>카메라 포텐셜 필드로 sparse-view 3DGS의 저감시 영역을 찾아 가상 카메라를 배치하는 기법임. 정보 부족 뷰포인트 식별이 active perception/NBV와 개념적으로 맞닿음</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2608.30417'>No Equivariant Architecture Covers All Equivariant Attention</a></td><td>45</td><td>3</td><td>Representation Learning</td><td>고정된 equivariant MHSA 아키텍처가 전체 equivariant map class를 커버할 수 없음을 대수기하로 증명함. SE(3) equivariant 로봇 정책 설계에 이론적 함의가 있으나 응용 실험은 없음.</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2608.29322'>Test-Time Scaling for Video Diffusion Models via Diagnosis-Guided Candidate Recycling</a></td><td>45</td><td>2</td><td>Video</td><td>diagnosis-guided candidate recycling으로 비디오 생성 test-time scaling을 하는 프레임워크임. 진단 후 편집 루프가 실패 감지·복구 패러다임과 개념적으로 유사해 참고할 만하나 응용은 비디오 생성임</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2608.30124'>TPR-Attention for Combinatorial Generalization</a></td><td>45</td><td>2</td><td>Representation Learning</td><td>tensor product representation 기반 attention으로 combinatorial generalization을 개선함. compositional structure 표현이라는 점에서 object-centric 표현과 맥이 닿지만 로봇 실험은 없음.</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2608.30618'>AQ3D: Adaptive Query Transformer for 3D Instance Segmentation</a></td><td>44</td><td>4</td><td>3D Vision</td><td>장면 크기에 맞춰 query 수를 조정하는 3D instance segmentation 디코더라 로봇 장면 이해 파이프라인에 활용 가능함</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2608.30342'>CapFrame: Text-Instructed Viewpoint Grounding in 3D Gaussian Scenes via Geometric Pseudo Labels</a></td><td>44</td><td>3</td><td>3D Vision</td><td>3DGS에서 언어로 카메라 뷰포인트를 지정하는 새 태스크(TIVG)라 active viewpoint 개념과 닿아있으나 로봇 지각 자체를 다루지는 않음</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2608.30283'>BCPPO: Bachelier-Inspired Constrained Proximal Policy Optimization for Tail-Risk-Aware Safe Reinforcement Learning</a></td><td>44</td><td>3</td><td>RL</td><td>critic disagreement 기반 tail-risk safe RL로 Push1 같은 로봇 조작형 safety-gym task에서 검증함. 다만 도메인이 넓은 safe RL 벤치마크 중심이라 embodied 특화는 아님.</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2608.29118'>Emergent Misalignment Is Not Magical</a></td><td>44</td><td>0</td><td>NLP</td><td>emergent misalignment을 representation distance로 예측 가능함을 보여 신비화를 해소한 분석 연구임, 안전성 관점에서 impact는 있으나 로보틱스 무관함</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2608.30242'>CanonNav: Disentangling Navigation Behavior from Camera Geometry in Cross-Platform Visual Navigation</a></td><td>42</td><td>6</td><td>Navigation</td><td>카메라 기하와 주행 행동을 분리하는 canonicalization으로 cross-platform 시연 데이터 활용도를 높인 방법임. RGB만으로 RGB-D 기반 방법을 능가하는 결과가 인상적이나 네비게이션 도메인에 국한됨.</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2608.30368'>SpectraTac: A Compact Camera-Free Optical Tactile Sensor with Distributed Color Sensing</a></td><td>42</td><td>6</td><td>Manipulation</td><td>카메라 없이 분산 색 센서로 촉각 힘·접촉영역을 추정하는 소형 저가 센서 하드웨어임. 촉각 인식 우선주제에 부합하나 하드웨어 기여 중심으로 학습 알고리즘 novelty는 제한적임.</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2608.28693'>RoboGesture: Real-Time Semantic-aligned Co-Speech Gestures Generation for Humanoid Interaction</a></td><td>42</td><td>5</td><td>Embodied AI</td><td>오디오에서 직접 의미론적 제스처를 생성하는 diffusion transformer를 실제 휴머노이드에 적용함. HRI/제스처 생성 중심이라 조작·VLA 핵심 주제와는 다소 거리가 있음.</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2608.29080'>GHOST in the Robots: Real-Time Exocentric Dual-Robot VR Teleoperation from Onboard Cameras</a></td><td>42</td><td>5</td><td>Robotics</td><td>온보드 센서만으로 두 대 로봇을 한 명이 조작하는 exocentric VR 인터페이스임. teleoperation 데이터 수집 인프라로서 유용하나 학습 알고리즘 기여는 아님.</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2608.28982'>FractureFields: Contact-Aware Binary Multi-Field Transfer for Fractured 3D Gaussian Simulation</a></td><td>42</td><td>4</td><td>World Model</td><td>파쇄된 3D Gaussian 물체의 fragment별 momentum field 분리로 물리 시뮬레이션 안정성을 개선함. contact-aware 시뮬레이션이라 world model·매니퓰레이션 물리 이해에 참고할 만함</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2608.30388'>PRISM: Predictive Recomposition via Semantic Latent Decomposition for View-invariant Video Representation Learning</a></td><td>42</td><td>4</td><td>Video</td><td>ego-exo 비디오에서 view-invariant/variant를 언어 지도로 분리하는 표현학습이라 로봇의 인간 시연 학습 표현에 참고할 만함</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2608.30617'>RealCAD: Towards Real-World Image-to-CAD Reconstruction under Domain Shift and Parameter Bias</a></td><td>42</td><td>4</td><td>3D Vision</td><td>실제 이미지-CAD 재구성에서 parameter bias를 밝히고 domain gap을 줄인 연구라 조작 대상 CAD 자산 획득에 참고할 만함</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2608.29193'>HalluPrism: When Multimodal Uncertainty Should Diagnose, Not Decide</a></td><td>42</td><td>4</td><td>Multimodal</td><td>멀티모달 불확실성을 perturbation 기반 진단 신호로 분해해 실패 유형을 구분한 방법이라 VLA perception failure 진단에 참고할 만함</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2608.28675'>Multi-Agent Self-Improving Reinforcement Learning for Video Reasoning</a></td><td>42</td><td>3</td><td>RL</td><td>frozen verifier로 GRPO 학습 신호를 주는 video grounding RL 프레임워크임. verifier 기반 학습 신호 아이디어는 실패 감지/보상 설계에 참고할 만하나 로봇 적용은 아님</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2608.28895'>ReconSplat: Generalizable 3D Scene Reconstruction Beyond Observed Views</a></td><td>42</td><td>3</td><td>3D Vision</td><td>3DGS와 multi-view latent diffusion을 결합해 미관측 영역까지 기하 일관되게 복원하는 feed-forward 방법임. object-centric 3D representation에 기여하나 로봇 적용 검증은 없음</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2608.30294'>Dynamic Hub-and-Spoke Memory for Streaming Video Understanding</a></td><td>42</td><td>3</td><td>Video</td><td>training-free hub-and-spoke 메모리로 streaming video 장기 기억을 다루는 구조는 robot memory 설계에 참고할 만하나 실제 embodied task 검증은 없음</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2608.30959'>LOCI: A Locator-Critic with Refinement Loop</a></td><td>42</td><td>3</td><td>Multimodal</td><td>탐색과 검증을 분리한 training-free visual search 루프라 VLM 기반 시각 근거 확인에 참고될 만함</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2608.30395'>When LLM Meets Tree Search: A Systematic View of Inference as Search in Large Language Models</a></td><td>42</td><td>3</td><td>RL</td><td>test-time scaling을 tree search로 통합 정리한 서베이임, inference-time planning 우선 주제와 직접 연관되나 새 방법 제안은 아님</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2608.28704'>ORDDAR: Observation-Driven Reasoning for Distortion-Resilient Decision, Action, and Cognitive Recovery</a></td><td>41</td><td>4</td><td>RL</td><td>추론 궤적을 상태 전이로 모델링해 국소적 왜곡만 탐지·복구하는 프레임워크임, failure detection·recovery 문제의식과 formulation이 로봇 실패 복구 연구에 직접 참고할 만함</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2608.29896'>EMERGE-Policy: A Robot Mind Emerges Beyond a Single Policy</a></td><td>40</td><td>7</td><td>Embodied AI</td><td>인지·실행·검증·메모리를 역할별 sub-agent로 나눠 협업시키는 fine-tuning 없는 agentic 프레임워크임. failure 진단·회복·메모리 통합이라는 방향은 우선주제에 맞으나 서술이 다소 과장되어 있고 정량적 비교가 약함.</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2608.29475'>Seeing Through Extreme Visual Sparsity: Surface Understanding from a Single Random Visual Patch</a></td><td>40</td><td>6</td><td>Manipulation</td><td>10%만 보이는 sparse patch로 표면 재질을 인식하는 프레임워크임. 로봇 인식·촉각 관련 벤치마크(Touch-and-Go)로 실질적 관련이 있으나 기존 백본 4종 비교 수준임</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2608.28664'>The Potential of Haptic Foundation Models</a></td><td>40</td><td>6</td><td>Tactile Perception</td><td>촉각 파운데이션 모델로 가는 패러다임 전환을 제시한 비전/포지션 논문임. 방향 제시에 그치고 magazine 기고문이라 실증적 근거는 약함.</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2608.30858'>GAFT: Geo-Anchored Fine-Tuning for Hazard Identification from Rare Failures</a></td><td>40</td><td>6</td><td>Navigation</td><td>off-road 지형 위험 인식에 기하학적 prior로 LoRA를 가이드하는 방법임 - rare failure 데이터 문제를 다루지만 특정 도메인(forest hazard)에 국한된 PEFT 기법 수준임</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2608.29232'>Background-Free Objectness Learning for Class-Agnostic Detection</a></td><td>40</td><td>5</td><td>Manipulation</td><td>배경 라벨 없이 objectness를 학습하는 class-agnostic 탐지 프레임워크임. cs.RO 태그가 있고 open-world 물체 탐지가 매니퓰레이션에 실질적으로 필요한 능력임</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2608.29483'>GeoAgent: Evaluating VLM Geolocalization Through Embodied Navigation</a></td><td>40</td><td>5</td><td>Navigation</td><td>VLM 지오로컬라이제이션을 정적 이미지가 아닌 embodied navigation으로 재구성한 벤치마크임. VLN 주제와 맞닿으나 매니퓰레이션과는 거리 있음</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2608.29388'>Fully Distributed GNE Algorithms for Multi-Robot Placement without Consensus on Multipliers</a></td><td>40</td><td>5</td><td>RL</td><td>승수 교환 없이 GNE에 도달하는 완전분산 알고리즘을 multi-robot placement에서 검증한 논문이라 다중로봇 협조에 직접 관련됨</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2608.29720'>VeloBins: Learning Velocity and Its Uncertainty via Bins and Error-Conditioned Gaussian Labels for Aerial Inertial Odometry</a></td><td>40</td><td>5</td><td>Navigation</td><td>속도 회귀를 bin 분류로 재구성해 불확실성까지 함께 얻는 방법으로 네 개 항공 데이터셋에서 오차를 3-27% 줄임. representation 재구성이라는 점에서 아이디어는 있으나 항법 도메인 특화임.</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2608.29705'>A Calibration Audit of Confidence in Feed-Forward 3D Reconstruction</a></td><td>40</td><td>4</td><td>3D Vision</td><td>feed-forward 3D 복원 모델의 신뢰도 점수가 실제로는 과신됨을 감사한 연구임. 인식 신뢰도 캘리브레이션은 실패 감지의 기반이 되는 문제라 참고 가치 있음</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2608.30819'>What Emerges and What Breaks in Self-Play Driving</a></td><td>40</td><td>4</td><td>Navigation</td><td>대규모 self-play 주행 정책 학습에서 reward hacking 등 실패 유형을 실도시 지도로 분석함. 정책 학습 실패 분석이 흥미로우나 새 방법 제안보다는 진단성 연구에 가까움.</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2608.28697'>Multi-Group Pipe Routing under Permanent Geometric Occupancy: Problem, Benchmark, and Classical Baselines</a></td><td>40</td><td>4</td><td>Robotics</td><td>영구 점유 제약 하 다중 그룹 파이프 라우팅이라는 새 문제를 정식화하고 CBS/PBS 등 고전 baseline으로 벤치마크함. 새로운 problem formulation은 가점 요소이나 학습 기반 기여는 없음.</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2608.28778'>Adversarial Calibration Attack on Autonomous Vehicles</a></td><td>40</td><td>4</td><td>Robotics</td><td>카메라-LiDAR 온라인 캘리브레이션을 새로운 공격면으로 제시하고 실물 포스터로 실제 로봇·시뮬레이터에서 충돌까지 유발함. 새로운 공격 표면 발굴이라는 novelty는 있으나 학습·조작 알고리즘 기여는 아님.</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2608.29005'>A Degradation-Tolerance Benchmark for Camera-Only End-to-End Driving</a></td><td>40</td><td>4</td><td>Navigation</td><td>카메라 열화에 대한 E2E 주행 정책의 tolerance를 체계적으로 측정한 벤치마크임. 새 방법 제안보다는 진단성 벤치마크 기여임.</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2608.28791'>Efficient Geothermal Well-Control Optimization via Diffusion-Surrogate Reinforcement Learning</a></td><td>40</td><td>4</td><td>World Model</td><td>diffusion 모델을 물리 시스템의 학습된 surrogate world model로 써서 RL 정책을 학습함, world model 기반 제어 formulation이 로봇 매니퓰레이션 RL에 바로 참고할 만하나 지열 시스템 도메인임</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2608.29426'>Polis: 3D Self-Supervision at City Scale</a></td><td>40</td><td>3</td><td>3D Vision</td><td>도시 스케일 점군에 SIGReg 목적함수를 적용한 자기지도 3D 표현학습임. 대규모 semantic mapping에 참고할 만하나 자율주행 로봇 직접 적용은 없음</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2608.29519'>FuncRoom-Agent: Sequential Feed-Forward 3D Functional Indoor Scene Generation</a></td><td>40</td><td>3</td><td>Embodied AI</td><td>기능성 목표를 만족하는 실내 3D 장면을 DSL 기반 순차 생성으로 만드는 프레임워크임. 로봇 학습용 시뮬레이션 환경 생성에 참고할 만함</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2608.29920'>Continual Test-Time Adaptation via Entropy Sensitivity-Guidance in Strict Online Setting</a></td><td>40</td><td>3</td><td>CV</td><td>구조화된 지우기로 엔트로피 민감도를 측정해 배치크기 1 온라인 continual TTA를 안정화함. test-time optimization 주제와 부합하나 로봇 적용은 없음</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2608.30584'>Learning Compositional Spatio-Temporal Video Grounding with Synthetic Curriculum</a></td><td>40</td><td>3</td><td>Video</td><td>복합 속성·관계를 요구하는 spatio-temporal grounding 난이도별 벤치마크와 curriculum RL이라 embodied grounding 평가에 참고할 만함</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2608.31113'>BLARM: Animating 3D Objects from Video via Blending Latent Rigid Motion Primitives</a></td><td>40</td><td>3</td><td>3D Vision</td><td>비디오만으로 3D 메시를 저차원 rigid motion primitive로 애니메이션하는 feed-forward 방법이라 관절·변형 물체 모션 표현에 참고할 만함</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2608.28723'>Vehicle Drift Emergence: Continuous Evolution from Grip Driving to the Handling Limit via Boundary Exploration Learning Model Predictive Control</a></td><td>40</td><td>3</td><td>Robotics</td><td>명시적 drift reference 없이 랩타임 최소화만으로 grip에서 drift로의 연속적 전이가 나타남을 보인 MPC 연구임. 차량 동역학 제어 중심이라 조작·VLA 핵심 주제와는 거리가 있음.</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2608.29395'>GATE: Reliability-Gated Gaussian Evidence Fusion for Training-Free Test-Time Adaptation of Vision-Language Models</a></td><td>40</td><td>2</td><td>Multimodal</td><td>가우시안 증거 융합으로 VLM을 학습 없이 test-time adaptation하는 기법임. test-time optimization 주제와 맞으나 로봇 적용은 없음</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2608.30328'>Learning PDE Time-Stepping with Neural Cellular Automata</a></td><td>40</td><td>1</td><td>World Model</td><td>local update rule 기반 neural cellular automata로 PDE 장기 예측을 개선함. 물리 동역학 표현이라는 점에서 world model과 맥락이 있으나 로봇 실험은 없음.</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2608.29102'>Clustering as Approximation by Constrained Projectors: Theory and Guarantees</a></td><td>40</td><td>0</td><td>LG</td><td>k-means부터 spectral clustering까지를 constrained projector로 통합하는 이론 틀을 제시함, 이론적으로 깔끔하나 로보틱스와 직접 연결점은 없음</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2608.30376'>Kathleen Remembers: Length-Invariant One-Shot Recall Without Attention</a></td><td>39</td><td>3</td><td>LG</td><td>홀로그래픽 연상 메모리로 길이 불변 one-shot recall 구현, 선택적 unlearning·귀속 가능한 구조라 robot memory에 아이디어로 참고 가능하나 텍스트 바이트 실험만 있음</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2608.30144'>Rethinking Language&#x27;s Role in Efficient VLA for Autonomous Vehicles: Toward Smarter, Trustworthy Driving</a></td><td>38</td><td>6</td><td>VLA</td><td>추론 시점 언어 사용 방식을 4단계로 분류해 자율주행 VLA의 지연-성능 trade-off를 정리한 서베이임. 원저작 방법 제안은 없고 기존 문헌 정리에 가까움.</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2608.28665'>Understanding Temporal Semantic Stability in Open-Vocabulary UAV Perception through Metric 3D Fusion</a></td><td>38</td><td>5</td><td>Embodied AI</td><td>UAV 오픈보캡 segmentation의 시간적 안정성 분석임. semantic mapping과 관련은 있으나 새 방법론 없이 평가 프레임워크 제안 수준임</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2608.30034'>Input-Adaptive Gating of a Dehazing Front-End for On-Device Perception in Smoke-Obscured Environments</a></td><td>38</td><td>5</td><td>Embodied AI</td><td>연기 자욱한 환경에서 dehazing을 조건부로 게이팅해 온디바이스 엣지 검출을 하는 소방로봇 지원 시스템임. 실제 임베디드 배포와 적응적 계산 게이팅이 실용적이나 방법론은 임계값 기반 단순 조합임</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2608.29576'>Event-triggered Control and Online Learning for Networked Systems under Computational Delays</a></td><td>38</td><td>5</td><td>RL</td><td>계산지연이 있는 네트워크 시스템에 이벤트 트리거 제어와 온라인학습을 결합한 이론이라 실시간 로봇 제어 인프라에 참고될 만함</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2608.29396'>Toward Trustworthy Robot-Assisted Sliding Palpation for Shallow Vessel Localisation with a Calibrated Digital Twin</a></td><td>38</td><td>5</td><td>Manipulation</td><td>캘리브레이션된 digital twin으로 촉각 시퀀스를 생성해 실사용 데이터 의존을 줄이는 연구임. tactile 우선주제에 부합하나 도메인이 의료 특화이고 sim-to-real gap이 남아있음.</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2608.29767'>LARC: Lazy Adaptive Reachability Certification of Robot Manipulator Trajectories</a></td><td>38</td><td>5</td><td>Manipulation</td><td>clearance가 불확실한 구간만 선택적으로 bisect하는 lazy adaptive 인증 방법으로 실제 궤적에서 baseline 대비 계산량을 크게 줄임. 안전성 검증 효율화라는 점에서 실용적 기여이나 conceptual novelty는 제한적임.</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2608.28672'>FrameScope: Temporal Data Valuation for Stream Active Learning in Autonomous Vehicle Systems</a></td><td>38</td><td>4</td><td>RL</td><td>자율주행 스트림 데이터에 NTK 이론을 확장한 온라인 active learning 프레임워크임. 이론적 일반화는 있으나 robot manipulation과는 거리가 있음</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2608.28933'>NBS: No Bias Stereo</a></td><td>38</td><td>4</td><td>3D Vision</td><td>구조적 inductive bias 없이 순수 ViT로 스테레오 매칭 SOTA를 달성해 스케일링 법칙을 주장함. 스테레오 depth는 로봇 인식에 쓰이나 논문 자체는 순수 CV 스케일업 주장임</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2608.29113'>GramLoop: Training-Free Gram-Gated Replay for Robust Dense Prediction</a></td><td>38</td><td>3</td><td>CV</td><td>가중치 변경 없이 추론 시 transformer 블록을 반복 적용해 dense prediction 강건성을 높임. inference-time 계산 활용이라는 점에서 test-time optimization과 결이 맞음</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2608.30279'>Motion-Saliency Complementary Masked Modeling for Point Cloud Video Understanding</a></td><td>38</td><td>3</td><td>3D Vision</td><td>포인트클라우드 비디오 self-supervised masked modeling으로 motion-saliency 분리는 있으나 action recognition 벤치마크 위주라 로보틱스 적용은 간접적임</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2608.28599'>CDPR: Counterfactual Advantage-based Credit Assignment for Cost-Aware Sequential Medical Diagnosis</a></td><td>38</td><td>3</td><td>RL</td><td>비용 인지 순차 진단에서 counterfactual advantage로 credit assignment 문제를 해결함, 전문가 라벨·학습된 critic 없이 하는 방식이 sparse reward RL 일반에 참고할 만함</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2608.29374'>Think, Look, and Revise: Inconsistency-Aware Visual Self-Correction in MLLMs</a></td><td>38</td><td>2</td><td>Multimodal</td><td>도구 증강 MLLM 추론에서 도구 출력 검증·자기수정을 학습시키는 프레임워크임. 실패 감지·복구 컨셉과 유사하나 시각 도구 사용 맥락이라 로봇 정책은 아님</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2608.30530'>WebWorld: The Browser as a World Model for Self-Improving Web Code</a></td><td>38</td><td>2</td><td>World Model</td><td>브라우저를 world model로 써서 VLM 자기개선 루프를 검증하는 아이디어임, 시뮬레이터 기반 self-improvement 방법론은 로봇에도 참고 가능하나 웹 코드 도메인 한정임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2608.29356'>Plant-Inspired AI: Plants as Inspiration for Novel Problem Formulations, and Two Case Studies</a></td><td>38</td><td>2</td><td>RL</td><td>식물의 잎 의태·뿌리-줄기 자원배분 행동에서 기존 AI 프레임워크가 다루지 못한 새 문제 formulation을 끌어냄, 아이디어 단계라 실증은 약하지만 문제 정의 자체는 참신함</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2608.29074'>Nested Convex-Body Chasing for Online Optimization with Evolving Feasible Sets</a></td><td>38</td><td>1</td><td>LG</td><td>nested convex-body chasing으로 온라인 최적화 regret-movement 경계를 개선한 이론 연구임, 이론적 기여는 탄탄하나 로보틱스 적용은 간접적임</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2608.29030'>Learning to Follow In-Context Watermark Instructions via Self-Distillation</a></td><td>38</td><td>0</td><td>NLP</td><td>in-context watermark 지시 준수율을 self-distillation+RL로 크게 끌어올림, 벤치마크 개선 위주라 novelty는 제한적임</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2608.29128'>APIFlow-Bench: Measuring Whether Agents Survive Long, Dependent API Workflows</a></td><td>37</td><td>1</td><td>NLP</td><td>장기 API workflow에서 agent가 어디서 실패하는지 세분화해 측정하는 벤치마크임, 실패 진단 문제 설정은 failure detection 주제와 방법론적으로 닿아있음</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2608.30673'>CIG-RL: Curiosity-Driven Information-Guided Reinforcement Learning for Source Term Estimation in Uncertain Environments</a></td><td>36</td><td>5</td><td>RL</td><td>가스 소스 탐지 위한 curiosity 기반 DRL로 novelty exploration을 도입함 - 문제 자체가 협의의 소스 탐지 태스크라 일반 로봇학습 임팩트는 제한적임</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2608.30480'>VisER: Visual Evidence and Reliance for Object Hallucination Detection in LVLMs</a></td><td>36</td><td>3</td><td>Multimodal</td><td>LVLM object hallucination을 evidence와 reliance로 나눠 진단하는 training-free 지표라 VLA perception failure 진단에 참고할 만함</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2608.29057'>Sparse Koopman Autoencoders Identify Local Dynamical Regimes in Multibasin Systems</a></td><td>36</td><td>3</td><td>World Model</td><td>sparse latent로 다중 basin을 라벨 없이 구분하는 Koopman autoencoder라 동역학 표현학습에 참고되나 로봇 응용 실험은 없음</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2608.29507'>Denoising as Projection: Constrained Optimization with Gradient-Guided Diffusion</a></td><td>36</td><td>3</td><td>Generative Models</td><td>denoising을 데이터 기하로의 투영으로 보고 목적함수 gradient를 결합한 제약 최적화 이론이라 diffusion policy의 제약 준수 생성에 간접 참고될 수 있음</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2608.29188'>Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space</a></td><td>36</td><td>2</td><td>RL</td><td>RLVR이 해 공간을 어디서 좁히는지 entrance 지점으로 국소화한 분석이라 RL 학습 다양성 이해에 흥미로우나 로보틱스 응용은 아님</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2608.29092'>EviAnchor: Mitigating Hallucinations in Large Vision-Language Models via Regional Visual Evidence Compensation</a></td><td>36</td><td>2</td><td>Multimodal</td><td>LVLM의 시각 근거가 후반 레이어에서 약화되는 현상을 찾아 training-free로 재활성화함, VLA의 시각 grounding 개선에 참고할 만함</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2608.29459'>Toward Latent Language Model Skills Steering and Optimization: An Empirical Study</a></td><td>36</td><td>1</td><td>LG</td><td>LLM의 절차적 skill이 활성화 공간의 방향으로 표현되고 조작 가능함을 실증함, skill chaining 논의에 참고할 만한 표현학습 관찰임</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2608.29433'>Calibration and Comparative Analysis of Forward-Looking Sonar and 3D Sonar for Enhanced Underwater Object Recognition</a></td><td>35</td><td>6</td><td>Navigation</td><td>수중 2D·3D 소나를 자동 캘리브레이션·필터링해 물체 인식을 개선하는 연구임. cs.RO 태그의 실제 수중로봇 인식 문제나 기여는 캘리브레이션 수준임</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2608.30506'>Anomaly Detection on Small Industrial Components via Vision-Based Tactile Sensing</a></td><td>35</td><td>6</td><td>Manipulation</td><td>GelSight 기반 tactile AD 벤치마킹 연구임 - 방법론 새로움보다 기존 unsupervised AD 기법 비교·가이드라인 제공에 그침</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2608.28830'>BlobBoards: Robust Markers for Accurate Pose</a></td><td>35</td><td>5</td><td>CV</td><td>AprilTag 대비 위치오차와 폐색 강건성을 크게 개선한 fiducial marker 시스템임. 로봇 캘리브레이션에 실용적이나 새 패러다임은 아님</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2608.29609'>nnMNet: Baseline for Martian Terrain Semantic Segmentation</a></td><td>35</td><td>5</td><td>Embodied AI</td><td>화성 지형 semantic segmentation 베이스라인·벤치마크임. 행성탐사 로버 내비게이션에 관련 있으나 방법 자체는 경량화된 조합 수준임</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2608.28656'>RedLight-VLA: Models for traffic-rule grounding and behavioral emphasis in driving policies</a></td><td>35</td><td>5</td><td>VLA</td><td>신호등·정지선 상태를 보조 head로 명시 감독하는 VLA 학습 목적함수임. 개선폭이 수 % 수준으로 크지 않고 auxiliary head 추가에 가까운 incremental 기여임.</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2608.29514'>A Sliding Window Filter on the Galilean Group for Consistent Aided Inertial Navigation with Unknown Measurement Delays</a></td><td>35</td><td>5</td><td>Navigation</td><td>지연이 있는 관성항법을 Galilean group 위에서 formulation해 지연-상태 대칭에 의한 정보 누출 문제를 규명하고 sliding window로 해결함. 시뮬레이션 검증만 있고 실로봇 적용은 없음.</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2608.30433'>A Hybrid PEM-GP Framework for Uncertainty-Aware System Identification of Quadcopters</a></td><td>35</td><td>5</td><td>Robotics</td><td>물리 모델과 GP 잔차를 결합해 해석가능성과 불확실성 추정을 동시에 얻는 시스템 식별 방법임. LSTM과 동등한 정확도를 내며 불확실성까지 제공하나 방법론적으로는 기존 하이브리드 접근의 조합임.</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2608.29819'>PhasorNet: Learning Structure from Frequency for Real-Time Stereo Matching</a></td><td>35</td><td>4</td><td>3D Vision</td><td>주파수 위상 정보를 활용한 경량 실시간 스테레오 매칭임. 반사·투명 물체 처리가 로봇 인식에 참고할 만함</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2608.29927'>Everybody Tracking Every Body</a></td><td>35</td><td>4</td><td>3D Vision</td><td>에고센트릭 카메라·IMU와 타인의 외부시점 관측을 확산모델로 융합해 다인 3D 포즈를 추정함. 웨어러블 embodied 인식과 관련 있으나 HRI 검증은 없음</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2608.30765'>T3S: Improving Multi-Task Reinforcement Learning with Task-Specific Feature Selector and Scheduler</a></td><td>35</td><td>4</td><td>RL</td><td>task별 feature selector와 scheduler로 MTRL의 태스크 간 간섭을 줄인 연구로 로봇 조작 태스크에서 검증했으나 2023년 IJCNN 게재분의 재게시로 새로움은 제한적임.</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2608.28762'>Inter-3D VQA: A Roadside Multimodal Benchmark for 3D Spatiotemporally Grounded Visual Question Answering</a></td><td>35</td><td>3</td><td>3D Vision</td><td>노변 센서 기반 3D 시공간 VQA 벤치마크임. 자율주행 인프라 관점이라 embodied spatial reasoning과는 결이 다름</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2608.29081'>AdapToPASS: Ambiguity-aware Adaptive Spherical Transformer for Panoramic Semantic Segmentation</a></td><td>35</td><td>3</td><td>CV</td><td>카메라 움직임에 따른 모호성을 인식하는 파노라마 segmentation transformer임. 능동 인식과 관련은 있으나 벤치마크 개선 위주임</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2608.29567'>MotionSync: Non-Causal Refinement of Causal Tracker for Label-Efficient 3D Perception</a></td><td>35</td><td>3</td><td>3D Vision</td><td>자율주행 3D 트래킹에서 causal/non-causal 처리를 분리한 오토라벨링 시스템임. 데이터 엔진 효율화로서 유의미하나 새 패러다임은 아님</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2608.29917'>FoundYou: A Unified Model for Personalized Segmentation and Retrieval</a></td><td>35</td><td>3</td><td>CV</td><td>SAM2의 인스턴스 정체성 보존 특성을 활용해 개인화 분할·검색을 통합한 프레임워크임. 물체 재식별에 참고할 만하나 로봇 검증은 없음</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2608.29923'>Towards Continual Test-Time Adaptation of Vision-Language Models in Open-Vocabulary Semantic Segmentation</a></td><td>35</td><td>3</td><td>Embodied AI</td><td>오픈보캡 segmentation VLM의 continual TTA 붕괴를 앵커·필터링으로 방지함. 자율주행·수중 도메인 포함해 embodied 인식 강건성과 관련 있음</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2608.30247'>OPUS: A Simple yet Effective Unified Framework for Open-Vocabulary Detection</a></td><td>35</td><td>3</td><td>CV</td><td>텍스트·시각 프롬프트를 하나로 단순화한 오픈보캡 탐지 프레임워크임. 비정형 환경 물체 탐지에 참고할 만하나 로봇 검증은 없음</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2608.30899'>Uncertainty-Aware Trajectory Forecasting from Imperfect Tracking</a></td><td>35</td><td>3</td><td>Navigation</td><td>불완전한 트래커 출력을 불확실성으로 인코딩해 궤적예측을 개선한 방법이라 다중객체 추적 기반 내비게이션에 참고될 수 있음</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2608.28702'>Stochastic Liquid Deformation Fields: An SDE Generalisation of Closed-Form Continuous-Time Cells for Dynamic 3D Gaussian Splatting</a></td><td>35</td><td>2</td><td>3D Vision</td><td>Liquid Neural Network 셀에 SDE 항을 되살려 dynamic 3DGS 변형 필드를 개선함. 4D representation 관련 있으나 아키텍처 미세 개선 수준임</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2608.29285'>3D-MRL: Nested Multimodal 3D Representations via Matryoshka Representation Learning</a></td><td>35</td><td>2</td><td>3D Vision</td><td>Matryoshka 표현학습을 점군-이미지-텍스트 정렬에 적용해 가변 차원 임베딩을 학습함. object-centric 3D representation과 관련 있으나 미세조정 성격의 기여임</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2608.29924'>Hallucination Mitigation for Large Vision-Language Models via Implicit Feature Stabilization</a></td><td>35</td><td>2</td><td>Multimodal</td><td>특징 불안정성과 환각의 상관관계를 밝히고 미세조정으로 암묵적 안정화하는 기법임. VLA 백본 신뢰성에 참고할 만하나 로봇 적용은 없음</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2608.30695'>Liquid Gated Attention</a></td><td>35</td><td>2</td><td>Representation Learning</td><td>불규칙 샘플링 시계열을 위한 solver-free 연속시간 attention 연산자를 제안함. 센서 융합에 적용 가능하나 로봇 실험은 없음.</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2608.28692'>Growing a Stand, Not a Tree: Joint Canopy Generation Reproduces Crown Shyness</a></td><td>35</td><td>1</td><td>3D Vision</td><td>나무 개체 간에만 존재하는 구조(crown shyness)를 flow matching으로 집합 생성하는 문제임. set generation formulation 자체는 새롭지만 로봇 적용은 아님</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2608.29160'>Training-Free Hidden-State Refinement for Flow-Matching Image Generators</a></td><td>35</td><td>1</td><td>CV</td><td>학습 없이 denoiser 내부에서 토큰을 반복 갱신해 flow-matching 이미지 생성 품질을 높이는 test-time 기법임. 일반화 가능한 inference-time 계산 활용 아이디어지만 로봇 적용은 없음</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2608.29621'>CineForge: Self-Improving Agents for Long-Horizon Video Generation</a></td><td>35</td><td>1</td><td>Multimodal</td><td>장기 스토리 비디오 생성 에이전트가 케이스를 정책으로 진화시키는 자기개선 프레임워크임. 자기개선 에이전트 패러다임은 참고할 만하나 응용은 비디오 제작임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2608.30194'>NoisEasier: Test-Time Noise Optimization for Text-to-Video Generation</a></td><td>35</td><td>1</td><td>Video</td><td>보상 유도 노이즈 최적화로 전체 확산 궤적을 test-time에 최적화하는 text-to-video 기법임. test-time scaling 패러다임은 참고할 만하나 응용은 비디오 생성임</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2608.30320'>On the Design of Qwen3.8-Next Architecture: Evaluation, Efficiency, and Training Stability</a></td><td>35</td><td>1</td><td>LG</td><td>Qwen 아키텍처 기술 리포트, 학습 안정성·효율 설계는 실용적이나 formulation 새로움은 제한적임</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2608.30896'>Rad-R: A Raw-ADC Radar Dataset and Capture-Invariant SSM for Hardware-Fault Diagnosis</a></td><td>34</td><td>3</td><td>CV</td><td>raw ADC 레이더 데이터로 하드웨어 결함을 진단하는 데이터셋·SSM 모델이라 센서 고장 진단이라는 점에서 로봇 실패탐지와 일부 닿아있음</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2608.31005'>From Intent to Evidence: Policy-Steered Multi-Strategy Retrieval for Long-Video Agents</a></td><td>34</td><td>3</td><td>Video</td><td>질문 의도에 따라 검색 전략을 바꾸는 training-free long-video agent라 장기 비디오 이해에는 도움되나 embodied 적용은 아님</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2608.29860'>Uncertainty-Driven Replay Memory for Reinforcement Learning</a></td><td>34</td><td>3</td><td>RL</td><td>불확실성 기반으로 replay buffer를 구성하는 방법이라 로봇 RL 학습 효율화에 일반적으로 참고될 수 있으나 로보틱스 실험은 없음</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2608.30716'>SocialReasonBench: A Video-QA Benchmark for Social Reasoning with Counterfactual Narrative Videos</a></td><td>34</td><td>3</td><td>Video</td><td>반사실적 서사 분기 비디오로 사회적·인과적 추론을 평가하는 벤치마크, counterfactual reasoning 우선 주제와 직접 연관되나 방법 제안은 아님</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2608.30603'>DiffSAC: Diffusion-guided Sampling for Consensus-based Robust Estimation</a></td><td>34</td><td>2</td><td>CV</td><td>diffusion으로 좋은 minimal set을 학습해 RANSAC 샘플링 효율을 높이는 방법이라 포즈추정 등 로봇 지각 파이프라인에 간접 도움됨</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2608.30653'>Fine-Grained Multi Image Object Hallucination Benchmark</a></td><td>34</td><td>2</td><td>Multimodal</td><td>멀티이미지 상황에서 object hallucination을 세분화해 진단하는 벤치마크라 VLM 신뢰성 평가에 참고할 만함</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2608.30705'>VisLens: Single-Pass Interpretable Visual Search for Multimodal LLMs</a></td><td>34</td><td>2</td><td>Multimodal</td><td>logit lens로 한 번의 forward pass에서 visual search를 수행하는 해석가능한 방법이라 active perception 효율화에 참고될 수 있음</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2608.29197'>PokaiTrainer: Scaling Belief-State Search to Competitive Pokémon VGC</a></td><td>34</td><td>2</td><td>RL</td><td>동시행동·은닉정보를 가진 포켓몬 대전에 belief-state 탐색을 스케일링한 사례라 대규모 불완전정보 탐색 기법으로 참고 가치 있으나 로보틱스 응용은 아님</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2608.28660'>Test-Time Scaling for Scientific Equation Discovery</a></td><td>34</td><td>2</td><td>LG</td><td>LLM 기반 수식 발견에서 test-time compute 배분(width가 핵심)을 분석한 연구임 - test-time scaling 원리는 참고할 만하나 로봇 태스크 적용은 없음</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2608.29605'>Hindsight Memory-PRM: Supervising Memory Management with Auditable Hindsight Credit</a></td><td>34</td><td>2</td><td>LG</td><td>메모리 연산의 가치를 회고적 근거(검색·인용)로 학습하는 memory-utility critic임 - robot memory에 아이디어로 참고 가능하나 텍스트 에이전트 장기기억 QA 벤치마크에 한정됨</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2608.28603'>C3-UniMM: Causal Cycle-Consistent Unified Multimodal Modeling via Super Alignment and Shared Decoding Space</a></td><td>34</td><td>2</td><td>Multimodal</td><td>구조화된 latent causal graph로 통합 멀티모달 이해·생성을 인과적으로 일관되게 만드는 프레임워크, 새로운 표현 formulation이지만 로봇 적용은 미검증임</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2608.30369'>Augmenting Human Performance with an XR Agent Learning from Online Behavior and BCI Evidence</a></td><td>34</td><td>2</td><td>Multimodal</td><td>XR 환경에서 행동 신호와 EEG를 온라인 융합해 실시간 보조를 제공하는 프레임워크임, 온라인 신뢰도 추정과 재수렴 속도 개선이 test-time adaptation 관점에서 참고할 만함</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2608.30751'>Autoregressive Mosaics: Probing 2D Spatial Reasoning in Text-Only Language Models</a></td><td>34</td><td>2</td><td>NLP</td><td>텍스트 전용 LLM의 2D 공간 추론을 번역과 layout 과제로 분리해 probing함, embodied spatial reasoning 논의에 참고할 만하나 실제 embodiment는 없음</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2608.30442'>Confounding Masquerading as Improvement: A Systematic Evaluation of Offline Reinforcement Learning for Stroke Antithrombotic Treatment in a 129,000-Patient Registry</a></td><td>34</td><td>1</td><td>RL</td><td>대규모 임상 registry에서 offline RL 정책 개선 신호가 reward-embedded confounding임을 규명한 방법론 논문임. offline RL 평가 방법론적 교훈은 로봇 RL에도 참고할 만하나 도메인은 의료임.</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2608.30457'>Learning Where Outcomes Change:Credit-Addressable Reasoning for Multimodal Geometry</a></td><td>34</td><td>1</td><td>Multimodal</td><td>VLM의 다단계 기하 추론에 이벤트 단위 credit assignment를 도입한 방법임. VLA의 action-level advantage 설계에 아이디어 차용 가능성은 있으나 로봇 도메인은 아님.</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2608.29252'>Dynamic Important Example Mining for Reinforcement Finetuning</a></td><td>34</td><td>0</td><td>RL</td><td>RFT에서 샘플 가치가 훈련 중 변한다는 점에 착안해 gradient-alignment 기반 동적 샘플 선택을 제안함, 데이터 선택 기법 개선 위주임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2608.29460'>Can escalation channels redirect reward hacking toward defect disclosure?</a></td><td>34</td><td>0</td><td>NLP</td><td>결함을 보고하는 escalation channel을 주면 coding agent의 reward hacking이 크게 줄어듦을 실험적으로 보임, 실용적 안전 개입 연구임</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2608.29696'>Ideation Arena: Evaluating LLM Generated Research Ideas with Battle-style Human Expert Assessment</a></td><td>34</td><td>0</td><td>NLP</td><td>LLM이 생성한 연구 아이디어를 전문가 페어와이즈 평가로 비교하는 Elo 리더보드를 구축함, 연구 아이디어 평가 인프라로서 의미 있음</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2608.30051'>Mitigating Over-Optimization in PRM-Guided Search in Mathematical Reasoning by Optimizing the Guide</a></td><td>34</td><td>0</td><td>RL</td><td>PRM 유도 탐색의 over-optimization을 극단값 이론으로 설명하고 robust maximin 탐색으로 완화함, 이론적 근거가 탄탄함</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2608.29608'>Wide Learning: Learning to Reach Evidence</a></td><td>33</td><td>3</td><td>LG</td><td>학습자 상태가 접근 가능한 증거 실험 범위 자체를 바꾼다는 effective epistemic reach 개념을 형식화한 이론으로 active perception과 개념적으로 닿아있으나 실험은 매우 추상적임</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2608.29596'>Towards a Systems Foundation for Agentic Skills: Architecture, Lifecycle, and Security</a></td><td>33</td><td>2</td><td>NLP</td><td>agentic skill의 아키텍처·수명주기·보안을 체계화한 서베이성 연구임, embodied robotics를 응용 사례 중 하나로만 언급함</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2608.29286'>MMPCBench: Benchmarking Multimodal Large Language Models on Proactive Critique of Flawed Inputs</a></td><td>33</td><td>1</td><td>Multimodal</td><td>MLLM이 결함 있는 입력을 스스로 지적하는 proactive critique 능력을 벤치마킹함, 내부 추론과 최종 출력 간 consistency gap 발견이 흥미로움</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2608.29264'>EpaCache: Error-Propagation-Aware Caching for Accelerating Diffusion-Based Visual Generation</a></td><td>33</td><td>0</td><td>Video</td><td>diffusion 생성 캐싱을 trajectory-level 오차 전파까지 고려해 latency-fidelity를 개선함, inference 가속 기법으로 로보틱스와는 거리 있음</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2608.29376'>Evaluating Tiny Recursive Models Across Training for Code Generation</a></td><td>33</td><td>0</td><td>LG</td><td>tiny recursive model의 코드생성 성능을 teacher-forced fit과 free-running generation 양쪽에서 훈련 전 구간 추적한 분석 연구임</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2608.30035'>Beyond Uncertainty: Multi-Solver Disagreement Rewards for Self-Evolving Reasoning Curricula</a></td><td>33</td><td>0</td><td>RL</td><td>단일 solver 불확실성 대신 여러 solver 간 불일치를 curriculum 보상으로 쓰는 self-play 방법임, reward collapse 문제를 잘 짚음</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2608.31075'>Scaling Large Reasoning Models beyond Human Supervision: A Path toward Superintelligence</a></td><td>33</td><td>0</td><td>NLP</td><td>인간 감독이 줄어드는 상황에서 reasoning model을 어떻게 계속 개선할지 다룬 서베이성 비전 논문임</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2608.29237'>AGRICAM: A Track-Mounted Crop Pollination Monitoring Robot</a></td><td>32</td><td>6</td><td>CV</td><td>트랙 이동형 농업 화분매개곤충 모니터링 로봇 실배치 사례임. cs.RO 태그의 실제 로봇 시스템이나 ML 방법론적 novelty는 낮음</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2608.29347'>A Cognitive Architecture for Shared Autonomy in AUV Operations</a></td><td>32</td><td>4</td><td>Robotics</td><td>온톨로지와 다중 LLM으로 AUV 임무 계획·실행을 지원하는 구조로 시뮬레이션에서만 검증해 실증 근거가 약함.</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2608.29547'>Module Number Adaptive Visual Shape Control for Serial Modular Soft Robots</a></td><td>32</td><td>4</td><td>Manipulation</td><td>단일 모듈 데이터만으로 학습한 controller를 패치 분해를 통해 모듈 수가 다른 로봇에 재사용하는 방법임. 특정 소프트로봇 형태에 국한된 엔지니어링 기여임.</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2608.28666'>Improving Spatial-Temporal Reasoning in Video-Language Models with Structured Video Prompting</a></td><td>32</td><td>3</td><td>Video</td><td>video-language model 추론 시 구조화된 프롬프팅으로 시공간 추론 개선함. training-free지만 벤치마크 개선 위주의 기여임</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2608.30129'>Efficient and High-Quality Depth Estimation via Pixel-Space Diffusion with Linear Attention</a></td><td>32</td><td>3</td><td>3D Vision</td><td>선형 어텐션과 1스텝 확산으로 depth 추정을 고속화한 연구임. 로봇 인식 파이프라인에 유용하나 효율화 위주 기여임</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2608.30521'>MEOM: Multi-View Expected-OKS Maximization for Human Pose Triangulation</a></td><td>32</td><td>2</td><td>CV</td><td>멀티뷰 히트맵 전체를 활용한 3D 사람 포즈 삼각측량 개선으로 로보틱스보다 순수 CV 과제에 가까움</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2608.28609'>Parametric Multimodal User Memory: Storing What Captions Cannot Carry</a></td><td>32</td><td>2</td><td>Multimodal</td><td>캡션이 못 담는 지각 정보(목소리·얼굴)를 별도 encoder로 저장하는 personalization memory 구조임 - text/perceptual memory 분리 아이디어는 robot memory에 참고할 만하나 사람 대화 에이전트 대상 연구임</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2608.30567'>TuringLLM: Efficiently Scaling Foundation Models Toward Physical AI</a></td><td>32</td><td>2</td><td>LG</td><td>latency에 민감한 physical AI 응용을 겨냥한 20B MoE 언어모델 기술보고서임, 정작 embodied 평가는 없고 일반 LLM 효율화 기여가 중심임</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2608.30184'>ATGS: Anchored Temporal Gaussian Splatting for Long Volumetric Video Representation</a></td><td>32</td><td>1</td><td>3D Vision</td><td>시간축 앵커로 장시간 복잡 모션의 volumetric video를 안정화하는 4D Gaussian 표현임. object-centric 4D representation과 관련 있으나 로봇 응용은 없음</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2608.30978'>Sparse Competition during Training For the Emergence of Specialized Modules</a></td><td>32</td><td>1</td><td>Representation Learning</td><td>뉴런 그룹 간 경쟁으로 모듈 특화가 자발적으로 나타남을 보인 연구임. object-centric 표현과 개념적으로 유사하나 로봇 도메인 검증은 없음.</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2608.29530'>The Emergent Symbolic Structure of Artificial Neural Networks</a></td><td>32</td><td>1</td><td>LG</td><td>신경망 내부표현을 닫힌형 기호구조로 근사할 수 있음을 보인 해석가능성 연구임 - 표현학습 이론적 통찰이나 로봇 응용 실험은 없음</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2608.29646'>Detect Before You Attribute: Cascade Failure Attribution for Multi-Agent Systems</a></td><td>32</td><td>1</td><td>NLP</td><td>multi-agent 실패를 detect-before-attribute 방식으로 먼저 이상탐지 후 원인귀속하는 필터를 제안함, failure attribution 방법론이 로봇 멀티에이전트에도 참고될 만함</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2608.30230'>Rethinking the Test-Time Prompt Tuning Objective from the Perspective of Calibration</a></td><td>32</td><td>1</td><td>CV</td><td>test-time prompt tuning의 entropy minimization이 calibration을 해친다는 문제를 지적하고 target distribution 정렬로 개선함, test-time 적응이라는 주제 자체는 참고할 만함</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2608.30081'>Tracing Generated Samples to Training-Data Clusters in Flow-Matching Models</a></td><td>32</td><td>0</td><td>Generative Models</td><td>flow matching 생성 결과의 training sample attribution을 분석함. 새로운 해석 방법론이나 로봇 문제와 직접 연결점 없음.</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2608.30315'>Context Staircase: Signature-Aligned Dynamics of Token Embeddings under Small Initialization</a></td><td>32</td><td>0</td><td>NLP</td><td>토큰 임베딩이 학습 중 저차 통계에서 고차 통계로 이행하는 현상을 분석한 해석가능성 연구로 로봇과 무관함.</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2608.29988'>AutoCRAT: Within-trajectory Joint Control of Stochasticity and Compute for LLM Reasoning</a></td><td>32</td><td>0</td><td>RL</td><td>추론 중 sampling 확률성과 compute 예산을 궤적 내에서 함께 조절하는 controller임, test-time 제어 아이디어는 있으나 대상이 LLM 추론에 국한됨</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2608.30025'>Interpreting and Steering for Safe and Correct Code Generation</a></td><td>32</td><td>0</td><td>NLP</td><td>코드 취약점 관련 내부 표현을 찾아 steering으로 안전한 코드 생성을 유도함, 메커니즘 해석과 개입을 함께 보인 점이 좋음</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2608.30047'>Can LLM Agents Discover? Evaluating Creativity on ML Engineering Tasks</a></td><td>32</td><td>0</td><td>NLP</td><td>LLM 리서치 에이전트의 창의성을 novelty와 usefulness로 분리 평가함, 새로운 해를 찾아도 성능으로 못 이어진다는 진단이 흥미로움</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2608.30650'>Geometry of Divergence: Tracking Hidden-State Trajectories for Adaptive Multi-Turn Reasoning</a></td><td>32</td><td>0</td><td>NLP</td><td>멀티턴 추론의 hidden-state 궤적 곡률로 정답 여부를 완료 전에 구분해 토큰 비용을 줄임</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2608.30841'>HSRM: Hidden-State Reward Models for Test-Time Verification</a></td><td>32</td><td>0</td><td>NLP</td><td>생성기의 hidden state를 직접 읽어 후보 해를 검증하는 경량 reward model임, 재처리 없이 text verifier급 성능을 보임</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2608.31077'>Reconciling Process Supervision with Outcome-Based Credit in Agentic Policy Optimization</a></td><td>32</td><td>0</td><td>RL</td><td>outcome 기반 강화학습에 privileged information을 action 단위로 재분배하는 credit assignment 방법을 제안함</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2608.30478'>Agents in the Large: Perception-Centered Architecture for Persistent Agents</a></td><td>31</td><td>2</td><td>NLP</td><td>지속적 서비스를 위한 perception 중심 persistent agent 아키텍처, 장기 적응 개념은 lifelong robot agent와 유사하나 서비스 도메인 한정임</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2608.31100'>S3Gym: Can LLMs Turn Self-Testing and Self-Judging into Self-Improvement?</a></td><td>31</td><td>2</td><td>RL</td><td>self-testing·self-judging·self-improvement 세 능력을 텍스트 게임에서 평가하는 벤치마크, 경험 기반 자기개선 파이프라인 개념이 test-time learning에 참고됨</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2608.30319'>Beyond Token-Level Guidance: Inference-Time Alignment of Specialized LLMs via Cross-Family Representation Steering</a></td><td>31</td><td>1</td><td>NLP</td><td>특화 모델의 inference-time steering 기법, hidden representation 조작 아이디어는 test-time 개입 연구에 참고 가능</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2608.31002'>DARP: A Calibrated Dual-Arm RGB-D-IR Dataset for Multi-View Robotic Perception</a></td><td>30</td><td>5</td><td>3D Vision</td><td>듀얼암 RGB-D-IR 캘리브레이션 데이터셋 논문임 - 멀티뷰 퓨전 파이프라인은 학습 없는 deterministic 방식이라 알고리즘 기여는 크지 않음</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2608.30471'>HorizonNet for visual terrain navigation</a></td><td>30</td><td>4</td><td>Navigation</td><td>수평선 검출 기반 USV 위치추정으로 navigation 관련은 있으나 2018-2020년 구작을 재게시한 수준이라 새로움이 낮음</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2608.28891'>Pixel-wise Geo-registration of Drone and Satellite Images</a></td><td>30</td><td>3</td><td>Navigation</td><td>드론-위성 영상의 픽셀 단위 지오등록 벤치마크임. UAV 내비게이션과 관련 있으나 벤치마크·베이스라인 위주임</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2608.29187'>OPUS-V2: Bridging the Gap between Sparse Points and Dense Voxels</a></td><td>30</td><td>3</td><td>3D Vision</td><td>자율주행용 점군-복셀 occupancy 예측을 잇는 경량 변환 모듈임. AV 인식 파이프라인 개선이지만 새 패러다임은 아님</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2608.29235'>Uncertainty-Aware Multimodal Anti-UAV Detection via Evidential Fusion and Conflict-Discounted Belief Aggregation</a></td><td>30</td><td>3</td><td>CV</td><td>RGB-열화상 융합에 evidential deep learning으로 불확실성을 다루는 안티드론 탐지임. 실패 시 신뢰도 표현은 유의미하나 null result가 많음</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2608.30657'>InfraOcc: An Infrastructure Occupancy Benchmark with Static-to-Dynamic Reasoning</a></td><td>30</td><td>3</td><td>3D Vision</td><td>고정 시점 인프라 occupancy에서 정적-동적 비대칭을 활용한 벤치마크·방법이라 scene understanding에 일부 참고될 수 있으나 로봇 시점과는 다름</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2608.30820'>RealOOB: A Definition-Consistent Real-World Oriented Occlusion Boundary Benchmark</a></td><td>30</td><td>3</td><td>3D Vision</td><td>occlusion boundary 정의를 통일한 대규모 벤치마크라 depth ordering 기반 scene understanding에 참고될 수 있음</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2608.30512'>Trajectory-Initialized Neural Double Q-Routing for Large-Scale Overhead Hoist Transport Systems</a></td><td>30</td><td>3</td><td>RL</td><td>반도체 팹 천장 이송 로봇 함대의 라우팅을 shared value network로 대체한 응용 연구임. 실제 산업 로봇 함대 문제이나 방법 자체는 기존 Q-routing의 증분적 확장임.</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2608.31045'>Rotational Equivariance in Machine Learning: A Comprehensive Tutorial</a></td><td>30</td><td>3</td><td>Representation Learning</td><td>회전 equivariance 이론과 아키텍처를 정리한 튜토리얼로 3D 비전·로봇 정책 설계에 배경지식으로 유용하나 원저작 기여는 없음.</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2608.29023'>Teaching Robot Policies to Humans Using Erroneous Examples</a></td><td>30</td><td>3</td><td>Embodied AI</td><td>오류 예제를 통한 로봇 정책 교육이 인간의 정책 이해도를 높인다는 사용자 연구임. 로봇 학습 자체보다 인간 교육 방법론에 가까움.</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2608.28706'>Variable-Granularity Tokenization for High-Resolution Object Detection</a></td><td>30</td><td>2</td><td>CV</td><td>학습 없이 지역별 패치 크기를 다르게 주는 training-free tokenizer로 항공 소형 객체 탐지를 개선함. 효율화가 크지만 로봇 적용은 없음</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2608.30233'>Semantic-Spatial Discriminability Enhancement for Generalized Visual Grounding</a></td><td>30</td><td>2</td><td>Multimodal</td><td>다중·비대상 시나리오까지 다루는 일반화된 시각 그라운딩 프레임워크임. 지시 기반 물체 찾기가 매니퓰레이션에 참고될 수 있으나 벤치마크 개선 위주임</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2608.30621'>Cost-efficient Active Learning for Referring Image Segmentation and Grounding</a></td><td>30</td><td>2</td><td>Multimodal</td><td>raw 이미지만으로 visual grounding용 active learning 샘플을 고르는 방법으로 데이터 구축 효율화에 가까움</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2608.28771'>ERR+: Sequential Entropy Resolution for Efficient and Decisive LLM Reasoning</a></td><td>30</td><td>2</td><td>NLP</td><td>사고과정 중 엔트로피 감소를 보상해 추론 효율을 높인 RLVR 방법으로 test-time reasoning 최적화와 일부 닿아있으나 로보틱스 응용은 아님</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2608.28960'>Continuity-Free Near-Minimax Leading-Order Regret for CVaR-UCBVI</a></td><td>30</td><td>2</td><td>RL</td><td>CVaR 강화학습의 minimax 최적 후회 상한을 연속성 가정 없이 증명한 이론 논문으로 로보틱스 적용 사례는 없음</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2608.29107'>PathGuide: Dynamic Classifier-Free Guidance via On-Policy Transport Alignment</a></td><td>30</td><td>2</td><td>Generative Models</td><td>flow 모델에서 classifier-free guidance 스케일을 transport 문제로 재정식화한 방법이라 diffusion policy의 inference-time 제어에 간접 참고될 수 있음</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2608.29528'>MedCache: Efficient and Temporally Valid Memory for Longitudinal Clinical Agents</a></td><td>30</td><td>2</td><td>Multimodal</td><td>다중방문 임상 에이전트의 시간유효 메모리 설계를 다룬 연구라 장기 에이전트 메모리 구조 설계에 개념적으로 참고될 수 있으나 의료 도메인이라 직접 관련은 낮음</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2608.29647'>Reward-guided Fine-Tuning of One-Step Generative Models via Wasserstein Gradient Flow</a></td><td>30</td><td>2</td><td>Generative Models</td><td>one-step 생성모델을 Wasserstein gradient flow로 reward fine-tuning하는 방법이라 diffusion policy RL fine-tuning에 원리적으로 참고될 수 있음</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2608.28886'>Moving the Mean Toward the Known Good, Not Beyond It: What Inference-Time Interventions and Weight Consolidation Buy in Open-Ended Generation</a></td><td>30</td><td>2</td><td>RL</td><td>generate-verify-select-consolidate 루프에서 LoRA 통합이 평균은 올리지만 best solution은 못 넘는다는 실증 연구임 - test-time self-improvement 한계를 보여줘 참고할 만하나 태스크가 온라인 빈패킹임</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2608.29305'>Learning Simple Test-Time Environments for LLM Web Agents</a></td><td>30</td><td>2</td><td>LG</td><td>복잡한 웹 환경 관찰을 서브모듈로 분해해 테스트타임에 라벨없이 학습하는 방법임 - test-time adaptation 원리는 참고할 만하나 웹 에이전트 한정임</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2608.29606'>Agent Zero Memory: Provenance-Aware Long-Term Memory for LLM Agents</a></td><td>30</td><td>2</td><td>LG</td><td>출처 추적 가능한 3중 병렬 장기기억 구조(episodic·knowledge graph·hierarchical)로 LongMemEval SOTA를 달성함 - memory 설계 아이디어는 참고할 만하나 텍스트 대화 에이전트 대상임</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2608.29073'>Revolutionizing Turn-by-Turn Navigation with Cloud-Edge Deep Learning</a></td><td>30</td><td>2</td><td>Navigation</td><td>차량 내비게이션 음성 안내 생성을 transformer+MoE로 개선한 실차 적용 사례임, 로봇 navigation과는 결이 다름</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2608.31022'>MNIST-PRO: MNIST is Back as a Partially Observable World for AI Agents</a></td><td>30</td><td>2</td><td>Embodied AI</td><td>MNIST를 부분관측 glimpse 탐색 과제로 바꿔 능동 인지와 작업기억을 분리 평가함, active perception 논의에 닿아있으나 실제 embodiment나 물리적 제어는 없음</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2608.29996'>Partition-Aware Unlearning for Removing Spurious Correlations in Large Vision-Language Models</a></td><td>30</td><td>1</td><td>Multimodal</td><td>LVLM의 객체-배경 허위상관을 파티션 인식 unlearning으로 제거하는 프레임워크임. 시각 기반 신뢰성 개선이나 로봇 적용은 없음</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2608.30218'>Amortized Anchor Refinement for Deployable Continuous-Time 4D Gaussian Reconstruction</a></td><td>30</td><td>1</td><td>3D Vision</td><td>XR 헤드셋 배포용 4D Gaussian의 앵커 정제·위상학적 가지치기 기법임. 4D representation 효율화지만 로봇 적용은 없음</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2608.30502'>When the Martingale Never Stops Firing: Anytime-Valid Gating on Real Forecast Streams</a></td><td>30</td><td>1</td><td>LG</td><td>실제 스트림에서 conformal martingale의 교환성 가정이 깨지는 현상을 실측한 모니터링 연구로 온라인 적응 시스템 진단에 참고할 만하나 로봇 특화는 아님.</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2608.30724'>BAITBENCH: Measuring Agent Reward Hacking with Optional Shortcuts Planted in ML Tasks</a></td><td>30</td><td>1</td><td>LG</td><td>ML 에이전트의 shortcut 기반 reward hacking을 측정하는 벤치마크임. 에이전트 신뢰성 문제는 failure detection과 결이 닿지만 embodied 도메인은 아님.</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2608.30256'>Beyond Surface Forms: Symbolic Edits as a Test for Logical Reasoning with LLMs</a></td><td>30</td><td>1</td><td>NLP</td><td>논리 연산자 편집으로 LLM 추론 견고성 테스트, formulation은 새롭지만 로봇 적용성 낮음</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2608.28592'>A collective capability boundary in frontier large language models on guideline-conformant and case-specific oncology decision-making</a></td><td>30</td><td>1</td><td>AI</td><td>종양학 의사결정에서 프론티어 LLM들이 공통으로 실패하는 blind spot을 규명, 모델 역량 경계를 감지해 사람에게 라우팅하는 문제의식이 failure detection 논의와 닿음</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2608.29088'>HANIA: Planner-Guided Multimodal Graph Evidence Selection for Grounded Question Answering</a></td><td>30</td><td>1</td><td>Multimodal</td><td>planner 기반 멀티모달 그래프 근거 선택으로 QA grounding을 개선함, fine-tuning 없이 동작하는 점은 좋으나 대상 태스크가 QA에 국한됨</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2608.29880'>Perceive to Hypothesize, Verify to Ground: An Agentic Reasoning Framework for Open-World Geo-Localization</a></td><td>30</td><td>1</td><td>Multimodal</td><td>지리위치 추정을 perceive-then-verify 구조로 재정식화해 환각을 줄임, 증거 기반 검증 절차는 active perception 논의와 결이 비슷함</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2608.30550'>GarmentWeaver: Schema-Aware Structured Synthesis for Multimodal Sewing Patterns</a></td><td>30</td><td>1</td><td>3D Vision</td><td>스케치·텍스트에서 실행 가능한 재봉 패턴을 schema-aware하게 생성함, 시뮬레이션 호환 표현이라는 점에서 변형체 조작 표현에 참고할 만함</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2608.30162'>Reinforcement Learning for Symbolic Equation Solving</a></td><td>30</td><td>0</td><td>RL</td><td>기호 방정식 풀이에 RL을 적용한 연구로 로봇 문제와 무관함.</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2608.30366'>Mode Connectivity Beyond Classifiers: Evidence from Generative and Contrastive Models</a></td><td>30</td><td>0</td><td>Generative Models</td><td>classifier 넘어 생성/대조 모델까지 mode connectivity를 확장 검증한 해석가능성 연구로 로봇과 무관함.</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2608.30487'>Measuring Memory and Generalization as Separable Geometric Channels: The Topo^2 Framework</a></td><td>30</td><td>0</td><td>Representation Learning</td><td>persistent homology로 memorization과 generalization 채널을 분리한 해석가능성 연구로 로봇과 무관함.</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2608.31067'>Universal Transformers for Circuit Computations: Perfect Length Generalization in Tiny Transformers</a></td><td>30</td><td>0</td><td>Representation Learning</td><td>회로 계산을 임베딩한 transformer로 완벽한 길이 일반화를 증명한 이론 연구로 로보틱스와 무관함.</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2608.29168'>JudgePanel: A Compact Judge with Panel Deliberation via Adaptive Multi-Reward Reinforcement Learning</a></td><td>30</td><td>0</td><td>NLP</td><td>소형 judge 모델에 panel deliberation을 증류해 저비용으로 큰 judge를 능가하게 만듦, LLM 평가 인프라 개선 연구임</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2608.29210'>Imag-Eval: a language-grounded framework for interpretable Text-to-Image instruction following evaluation</a></td><td>30</td><td>0</td><td>Multimodal</td><td>T2I instruction following 평가에서 prompt 길이와 compositional difficulty를 분리한 벤치마크임, 진단적 가치는 있으나 로보틱스와 무관함</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2608.29357'>LiteSearch-VL: Small Multimodal Search Agents via Trajectory Distillation and Synthetic Step-DPO</a></td><td>30</td><td>0</td><td>Multimodal</td><td>대형 멀티모달 검색 에이전트를 소형 모델로 증류하며 무엇이 전이되는지 분석함, 검색 깊이보다 답변 검증이 병목이라는 진단이 흥미로움</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2608.29372'>FORESIGHT-9: Prospective and Process-Aware Evaluation of Adaptive Trading Agents</a></td><td>30</td><td>0</td><td>RL</td><td>금융 트레이딩 에이전트를 반사실적 stress worldline으로 prospective 평가하는 벤치마크임, 실행 상태와 보고 상태의 불일치를 드러낸 진단이 유용함</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2608.30044'>Balance of Benchmarks: Semantic Density Reweighting for Benchmark Multiplicity and Task-Conditioned Evaluation</a></td><td>30</td><td>0</td><td>LG</td><td>벤치마크 밀도 편향을 semantic weight로 보정해 모델 랭킹을 재조정하는 평가 방법론 연구임</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2608.30181'>A.X K2 Technical Report</a></td><td>30</td><td>0</td><td>NLP</td><td>688B MoE 언어모델 기술보고서임, sparse attention과 학습 안정화 기법은 견고하나 scale-up 위주 기여임</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2608.30345'>Answer Probing-Guided Search for Diverse Solution Exploration of LLMs</a></td><td>30</td><td>0</td><td>NLP</td><td>의미 임베딩 대신 probed answer의 hidden state로 해 경로 다양성을 구분하는 tree search 방법임</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2608.30352'>Co-Annotator: Expert-Distilled ViT and VLM for Visual and Documentation Guidance in Age-Related Macular Degeneration</a></td><td>30</td><td>0</td><td>Multimodal</td><td>안과 진단에서 전문가 시선과 구술을 증류해 ViT와 VLM 가이드를 결합한 임상 도구임, 실제 배치 평가까지 수행한 점이 탄탄함</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2608.30362'>Will the User Ever Know? Covert Indirect Prompt Injection on Tool-Using LLM Agents</a></td><td>30</td><td>0</td><td>NLP</td><td>tool-using agent에 대한 간접 프롬프트 주입이 사용자 모르게 성공하는 covert 공격을 정의하고 유도함, agent 보안 연구임</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2608.30676'>MedAgent-R1: Faithfulness-Aware Reinforcement Learning for Evidence-Grounded Medical Reasoning</a></td><td>30</td><td>0</td><td>NLP</td><td>근거 기반 보상 게이트로 의료 추론 에이전트의 인용 조작(confident hallucination)을 크게 줄임</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2608.31068'>Wrong Prediction, Right Answer: Recovering Evidence from Collapsed LLM Sequence Scores</a></td><td>30</td><td>0</td><td>NLP</td><td>sequence score가 무너져도 hidden state probe로는 정답이 살아있음을 보여 실패를 표현 실패와 능력 부재로 구분함</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2608.28978'>Selective Forgetting: A Graph-Based Memory Framework for Long-Term LLM Agents</a></td><td>29</td><td>3</td><td>NLP</td><td>그래프 기반 장기 메모리가 flat retrieval보다 못하다는 부정적 실증 결과, robot memory 설계에서 구조화 메모리의 한계를 시사함</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2608.30508'>UTILMEM: Benchmarking Evidence Utilization in Long-Term Conversational Memory</a></td><td>29</td><td>2</td><td>NLP</td><td>장기 대화 메모리의 증거 통합 능력을 진단하는 벤치마크, robot memory의 evidence integration 문제와 개념적으로 유사함</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2608.31111'>Aspire: Can Models Self-Evolve from Vague Goals?</a></td><td>29</td><td>2</td><td>AI</td><td>모호한 목표에서 스스로 학습 방법을 정하는 self-evolution 벤치마크, 목표 해석부터 검증까지 다루는 formulation이 신선하나 가중치 개선은 불안정함</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2608.30391'>Using Grounded Theory for Agent Behavior Analysis at Scale</a></td><td>29</td><td>1</td><td>NLP</td><td>grounded theory로 에이전트 궤적 대량 분석하는 파이프라인, agent behavior 분석 방법론이 로봇 실패 분석에 약하게 전이 가능함</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2608.30397'>Co-Evolving Actor-Conditioned Critics for Non-Verifiable Generation</a></td><td>29</td><td>1</td><td>NLP</td><td>actor-conditioned critic 공진화 학습, critique-refinement 루프는 failure recovery 연구에 참고할 여지 있음</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2608.30980'>Evaluating and Improving LLM Self-Modeling</a></td><td>29</td><td>1</td><td>NLP</td><td>LLM의 자기 행동 예측 능력(self-modeling) 평가와 RL 개선, introspection 개념이 실패 예측 연구에 약하게 참고됨</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2608.29279'>Understanding Deep Learning via Entropy Space Theory</a></td><td>29</td><td>0</td><td>LG</td><td>딥러닝을 위한 entropy space 이론을 새로 제안함, 수학적 틀은 흥미로우나 실증 검증이 빈약함</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2608.29291'>Accelerating Unified Multimodal Models with Core-Expansion Routing and Unified Computation Scheduling</a></td><td>29</td><td>0</td><td>Multimodal</td><td>통합 멀티모달 모델의 이해·생성 계산 중복을 라우팅과 스케줄링으로 줄인 효율화 연구임</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2608.29588'>Call Neighbours Yourself: Graph Walks with Destination-Conditioned On-Policy Self-Distillation</a></td><td>29</td><td>0</td><td>NLP</td><td>텍스트 그래프 추론에서 이웃 선택 자체를 추론 과정에 포함시켜 능동적으로 증거를 탐색하게 함</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2608.29814'>FRAMEWORKERS: A Dynamic Multi-Agent Framework for AI-Generated Video Production</a></td><td>29</td><td>0</td><td>Video</td><td>영상 제작 전 과정을 동적 태스크 스택으로 오케스트레이션하는 멀티에이전트 시스템임, 생성형 비디오 워크플로 엔지니어링에 가까움</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2608.30517'>ScienceArena: Benchmarking LLMs on Latest Scientific Olympiad Competitions</a></td><td>29</td><td>0</td><td>NLP</td><td>최신 과학 올림피아드 문제로 LLM 추론을 평가하는 벤치마크임, LLM judge 신뢰도 검증까지 포함함</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2608.28691'>Defending Wearable VLMs Against Private Attribute Inference</a></td><td>28</td><td>3</td><td>Multimodal</td><td>웨어러블 VLM에서 시각 토큰의 프라이버시 유출을 막는 방어 기법임. 에고센트릭 인식과 관련은 있으나 로봇 매니퓰레이션과는 거리 있음</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2608.29935'>System Identification of Admittance Models for Large Real-World Objects</a></td><td>28</td><td>3</td><td>Robotics</td><td>문·손수레 같은 실제 대형 물체의 admittance 모델을 물리적 일관성 보장하며 식별한 연구로 haptic 시뮬레이션 인프라 기여이나 학습 요소는 없음.</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2608.30301'>Data-Centric Neuromotor Interfaces for Portable Human-Machine Interaction</a></td><td>28</td><td>3</td><td>Robotics</td><td>초경량 파라미터 모델로 34개 제스처를 엣지에서 인식하는 sEMG 인터페이스임. 로봇 조작보다는 human-machine interface에 초점이 맞춰져 있음.</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2608.29126'>Efficient Language-to-Vision Feature Injection for Referring Single-Object Tracking</a></td><td>28</td><td>2</td><td>CV</td><td>언어 기반 단일 객체 추적에서 semantic drift를 완화하는 gated feature injector임. 지시 기반 추적이 embodied task와 맥이 닿으나 트래킹 벤치마크 개선 수준임</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2608.29611'>See the Change, Keep the Flow: Unsupervised Action Segmentation via Spectral-Temporal Representation Learning</a></td><td>28</td><td>2</td><td>RL</td><td>spectral-temporal 표현으로 비지도 행동 분할의 optimal transport 의사라벨을 개선함. long-horizon 행동 구조 학습과 관련 있으나 사람 행동 데이터 위주임</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2608.30839'>Physical Adversarial Examples for Person Detectors in Thermal Images Based on 3D Modeling</a></td><td>28</td><td>2</td><td>CV</td><td>3D 모델링 기반 열화상 사람탐지 회피 의류로 사람탐지 강건성과 관련되나 로봇 응용은 아님</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2608.28981'>V2TATC: A Joint Voice-Trajectory Embedding Framework and Dataset for Air Traffic Controller Situational Awareness</a></td><td>28</td><td>2</td><td>Multimodal</td><td>음성지시와 항공기 궤적을 공유 잠재공간에 정렬한 관제 응용으로 언어-궤적 정렬이라는 점에서 VLA와 개념적으로 유사하나 도메인이 다름</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2608.29448'>SS-ESOAP: Self-Scaled Adaptive Preconditioning for Physics-Informed Learning</a></td><td>28</td><td>2</td><td>LG</td><td>물리정보신경망용 SOAP 스타일 전처리 최적화 기법으로 시뮬레이션 학습 인프라에 참고되나 로보틱스 응용 실험은 없음</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2608.28977'>The Role of Network Topology and Opponent Information in Shaping Cooperation in Multi-Agent Reinforcement Learning Systems</a></td><td>28</td><td>2</td><td>RL</td><td>그래프 위상과 상대 정보가 다중 에이전트 협력 형성에 미치는 영향을 분석함, 다중 로봇 협력 설계에 참고할 만함</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2608.29106'>Elastic Triangle Splatting</a></td><td>28</td><td>1</td><td>3D Vision</td><td>triangle splatting 커널 함수를 분석하고 elastic kernel을 제안한 그래픽스 연구임. 3D representation 일반 연구지만 로봇 적용은 없음</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2608.29793'>GridFlow: Structured Latent Flow for Seamless City-Scale 3D Point Cloud Generation</a></td><td>28</td><td>1</td><td>3D Vision</td><td>위성영상 조건으로 도시 스케일 점군을 seamless하게 생성하는 프레임워크임. 시뮬레이션 환경 생성에 참고 가능하나 도시계획 응용 위주임</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2608.29800'>Source-Dependent Deference in Medical Imaging Agents Under Falsified Findings: A Pilot Audit</a></td><td>28</td><td>1</td><td>Multimodal</td><td>도구가 거짓 소견을 반환할 때 에이전트가 정답을 뒤집는지 감사한 파일럿 연구임. 에이전트 신뢰도 문제로서 참고 가치 있으나 소규모 의료 파일럿임</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2608.28840'>Unsupervised Latent Space Alignment with Hyperspherical Geodesic Matching</a></td><td>28</td><td>1</td><td>LG</td><td>쌍 데이터 없이 잠재공간을 기하학적으로 정렬하는 방법으로 모델 결합에 쓸 수 있으나 로보틱스 응용은 아님</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2608.28859'>The Halt Vector: Internalizing a Causal Steering Intervention for Efficient Reasoning</a></td><td>28</td><td>1</td><td>NLP</td><td>추론 길이를 줄이는 halt vector를 가중치에 내재화한 해석가능성 연구로 로보틱스 응용은 아님</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2608.30152'>Converse and Collision-Based Achievability for Node Localization with Hybrid Distance-Spectral Graph Positional Encodings</a></td><td>28</td><td>1</td><td>LG</td><td>그래프 positional encoding의 node 식별 가능성을 이론적으로 분석함. scene graph/SLAM과 표면적 연결은 있으나 로봇 응용은 다루지 않음.</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2608.30730'>E-Commerce Bench: Evaluating LLM Agents on Long-Horizon Autonomous Business Operation</a></td><td>28</td><td>1</td><td>NLP</td><td>연 단위 자율 비즈니스 운영을 평가하는 LLM 에이전트 벤치마크로 long-horizon 개념은 겹치나 로봇 도메인이 아님.</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2608.30750'>Do VLMs Share Safety Neurons Across Modalities?</a></td><td>28</td><td>1</td><td>Multimodal</td><td>VLM의 시각/텍스트 safety 뉴런을 causal하게 분리 분석한 연구로 VLM 내부 기전 분석 방법론은 참고할 만하나 로봇 도메인 아님.</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2608.30778'>Reciprocity Separates Gradient Flow from Rotation in Conservative Physical Learning</a></td><td>28</td><td>1</td><td>LG</td><td>물리적 학습 시스템에서 gradient flow와 rotation을 분리하는 이론 연구로 로봇 대상 물리 학습과 개념적으로만 연결됨.</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2608.31009'>Language-Informed Flow Matching for Trend-Guided Structure-Based 3D Molecular Generation</a></td><td>28</td><td>1</td><td>Generative Models</td><td>언어 유도 화학 prior를 flow matching 3D 분자 생성에 결합한 연구로 flow matching+언어조건 결합 방식은 VLA와 유사하나 도메인은 신약임.</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2608.31036'>Normalized Low-Rank Adaptation</a></td><td>28</td><td>1</td><td>LG</td><td>LoRA down-projection 정규화로 학습 안정성을 개선한 기법으로 VLA fine-tuning에 범용 적용 가능하나 로봇 특화 검증은 없음.</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2608.30241'>PaperBanana-Interact: Scientific Diagram Refinement with Multi-Turn Human Feedback</a></td><td>28</td><td>1</td><td>Multimodal</td><td>다이어그램 다중 턴 수정 벤치마크임, 시각 생성 피드백 루프 아이디어는 약하게 참고 가능</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2608.28787'>Beyond Representation Learning: A Systematic Study of Joint-Embedding Predictive Generation for 3D Brain MRI</a></td><td>28</td><td>0</td><td>CV</td><td>JEPA를 3D 뇌 MRI 생성에 적용한 연구임. JEPA 확장이라는 점은 흥미로우나 의료영상 도메인이라 로봇 관련성 낮음</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2608.31069'>A Model with No Head and Many Thoughts</a></td><td>28</td><td>0</td><td>NLP</td><td>LM head를 경량 projector로 대체해 연속 임베딩 공간에서 추론하는 기법으로 로보틱스와 무관함.</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2608.29035'>EmoLASP: Emotion Recognition with Language Models and Answer Set Programming</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM에 ASP 추론을 결합해 감정인식 안정성을 높인 파이프라인 조합 연구임, 단일 데이터셋 위주라 일반성 낮음</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2608.29352'>Cross-Relational Preference Learning for Better LLM Instruction Following</a></td><td>28</td><td>0</td><td>NLP</td><td>instruction 간 관계를 반영한 preference 데이터 구성법으로 instruction following을 개선함</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2608.29363'>TRACER: Per-Tool Context Retention for LLM Agents via Consequence-Attributed Reinforcement Learning</a></td><td>28</td><td>0</td><td>NLP</td><td>tool 출력 압축이 재호출을 유발하는 비용을 고려한 강화학습 압축 정책임, 엔터프라이즈 효율화 연구임</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2608.29589'>Not Safe for All: Auditing the Dialect Penalty in Text-to-Image Safety Pipelines</a></td><td>28</td><td>0</td><td>Multimodal</td><td>T2I 안전 필터가 비표준 방언 표현을 과도하게 걸러내는 편향을 감사한 연구임, 공정성 이슈 발굴이 기여임</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2608.29953'>SearchWiki: Learning to Build and Navigate Knowledge Wikis for Active Information Seeking</a></td><td>28</td><td>0</td><td>NLP</td><td>코퍼스를 계층적 위키로 재구성해 RAG 탐색을 학습시킨 프레임워크임</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2608.30214'>SPARK: Skeleton-Guided Reasoning Synthesis from Large-Scale Scientific Literature</a></td><td>28</td><td>0</td><td>NLP</td><td>논문의 주장-증거 구조를 뼈대로 과학 추론 데이터를 합성하는 프레임워크임, 데이터 구축 기여가 중심임</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2608.30413'>DERELAB: Probing Defeasible Reasoning and Confirmation Bias in LLMs with a Generative Benchmark</a></td><td>28</td><td>0</td><td>NLP</td><td>defeasible reasoning에서 확증편향을 측정하는 생성형 벤치마크임, 대부분 모델이 반대 증거에도 결론을 안 바꾼다는 점을 보임</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2608.30532'>DiffPDE: Masked Diffusion Language Models as PDE Solver</a></td><td>28</td><td>0</td><td>LG</td><td>PDE 솔버 코드 오류를 masked diffusion으로 국소 재생성해 고치는 방법임, 코드 수리 효율화 연구임</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2608.30581'>Automated Testing of LLM-Based Post Hoc Explainers Using Model Checking as an Oracle</a></td><td>28</td><td>0</td><td>NLP</td><td>정책 설명을 생성하는 LLM의 사실성을 model checking으로 자동 검증하는 테스트 프레임워크임</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2608.30685'>ATLAS: Dual-Horizon Diagnostic Evaluation for Industrial Tool-Use Agents</a></td><td>28</td><td>0</td><td>NLP</td><td>산업용 tool-use 에이전트를 요청 단위와 상호작용 단위로 나눠 진단하는 이중 horizon 평가 프레임워크임</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2608.30922'>CARVE: Verified Expansion for Variable-Length Generation in Diffusion Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>masked diffusion LM의 답변 길이를 반사실적 안정성 검증으로 동적으로 늘리는 training-free 방법임</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2608.30997'>Multi-View Reflective Surface Inspection via Semantic-Saliency Cross-Verification</a></td><td>27</td><td>2</td><td>CV</td><td>반사면 결함 검사에서 멀티뷰 semantic-saliency 교차검증한 산업 응용 논문임</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2608.31159'>BRF-GS: Hyperspectral Bidirectional Reflectance Factor Modeling and Image Generation Based on 3D Gaussian Splatting</a></td><td>27</td><td>2</td><td>3D Vision</td><td>3DGS로 하이퍼스펙트럴 BRDF를 모델링한 원격탐사 응용으로 로봇 장면 표현과는 도메인이 다름</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2608.30270'>Read the Room, Read the Image: Understanding Indirect Speech Acts in Multimodal Visual Contexts</a></td><td>27</td><td>1</td><td>Multimodal</td><td>시각 맥락 기반 간접 화행 이해 벤치마크, pragmatic reasoning은 HRI에 약하게 닿음</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2608.30462'>Enhancing Low-Resource Language Reasoning via High-Resource Language Feature Transfer</a></td><td>27</td><td>1</td><td>NLP</td><td>sparse autoencoder feature steering으로 저자원 언어 추론 전이, 메커니즘 개입 방법론은 일반화 가능하나 로봇과 무관함</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2608.30646'>BiG-SURE - Bipartite Graph for Semantic Uncertainty and Reliability Estimation of LLMs</a></td><td>27</td><td>1</td><td>NLP</td><td>black-box LLM의 semantic uncertainty 추정 기법, uncertainty 개념은 failure detection과 약하게 연결됨</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2608.30661'>SwarmBench: Can Large Language Models Act as Agent Swarm Orchestrators?</a></td><td>27</td><td>1</td><td>AI</td><td>LLM의 agent swarm 오케스트레이션 능력 평가 벤치마크, 다중 로봇 조율에 약하게 전이 가능함</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2608.30712'>GUIDE: Guiding Internal Evidence with Language Instructions</a></td><td>27</td><td>1</td><td>Multimodal</td><td>언어 지시로 멀티모달 증거 의존 경로를 제어하는 프레임워크, 근거 사용 제어 개념이 참고할 만함</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2608.30204'>When Models Hear What They Expect: Diagnosing Prosodic Heuristics in Multimodal Sarcasm Detection</a></td><td>27</td><td>0</td><td>NLP</td><td>MLLM 음성 조롱 탐지 진단 연구임, 로보틱스 연관성 없음</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2608.30303'>Lazy Grounding: Attacking Search Agents with Factual Evidence</a></td><td>27</td><td>0</td><td>NLP</td><td>검색 에이전트가 인접 질문의 사실 증거에 오도되는 lazy grounding 현상 규명, 흥미롭지만 로봇과 무관함</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2608.30373'>Beyond Consensus: Downward Bias and Role Asymmetry in Multi-Agent LLM Judges for Subjective Evaluation</a></td><td>27</td><td>0</td><td>NLP</td><td>multi-agent judge의 하향 편향 규명, LLM 평가 방법론 연구임</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2608.29054'>Let Prompts Bridge Defense Knowledge: Transferable Graph Purification via Vulnerability-Aware GPL</a></td><td>27</td><td>0</td><td>LG</td><td>그래프 정화 방어를 prompt learning으로 도메인 전이시킨 module 추가 수준 연구임</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2608.29098'>SafeAtlas-VL: Beyond Binary Multimodal Safety with Large-Scale Data and Guard Models</a></td><td>27</td><td>0</td><td>Multimodal</td><td>멀티모달 안전성 판정을 5단계로 세분화한 대규모 데이터셋·guard 모델 연구임, 데이터 스케일 위주라 novelty는 낮음</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2608.29198'>How Identity and Opinion Shape Political Sycophancy in LLMs</a></td><td>27</td><td>0</td><td>NLP</td><td>정치적 아첨을 의견 편향과 정체성 편향으로 분리해 측정한 벤치마크 연구임</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2608.29263'>RACER: Reinforced Agent Collaboration for Explainable Reasoning on Knowledge Graphs</a></td><td>27</td><td>0</td><td>NLP</td><td>지식그래프 기반 LLM 추론에 강화학습 경로 탐색과 멀티에이전트 협업을 결합함, 구성 요소 조합형 개선임</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2608.29355'>APPSolver: Adaptive Patch Partitioning for Point-Wise Ship Flow Prediction on Unstructured Meshes</a></td><td>27</td><td>0</td><td>LG</td><td>선박 CFD 유동 예측에 적응형 patch partitioning을 적용해 계산 비용을 줄임, persistence baseline보다 정확도가 낮다는 한계를 스스로 밝힘</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2608.29612'>LLMs Interpret, Embeddings Organize, Graphs Emerge: Agent-Driven Compilation of Scientific Knowledge</a></td><td>27</td><td>0</td><td>NLP</td><td>LLM으로 논문을 위키·그래프 뷰로 컴파일해 연구 지식을 누적하는 시스템임, 응용 도구 성격이 강함</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2608.29753'>PAGE-RAG: Provenance-Aware Graph Evidence Promotion for Fixed-Budget Multi-hop Retrieval-Augmented Generation</a></td><td>27</td><td>0</td><td>NLP</td><td>multi-hop RAG에서 연결성과 실제 지지 여부의 격차를 그래프 기반으로 선별하는 방법임</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2608.29951'>Spatial Matryoshka Training for Multi-Granularity Visual Document Retrieval</a></td><td>27</td><td>0</td><td>Multimodal</td><td>시각 문서 검색에서 patch 임베딩을 다단계로 압축하는 학습법을 제안함, 저장 비용 절감 위주 연구임</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2608.30226'>LaMoC: Loss-Aware Modular Compression for LLMs</a></td><td>27</td><td>0</td><td>LG</td><td>모듈 압축에 loss-sensitivity 정보를 결합한 LLM 압축 기법임, 기존 activation 기반 압축 대비 점진적 개선임</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2608.30277'>SimCRAFT: Distilling Remote Sensing Agents via Synthetic Trajectories and Contextual Retrieval-Augmented Fine-Tuning</a></td><td>27</td><td>0</td><td>Multimodal</td><td>원격탐사 에이전트를 7B 모델로 증류한 경량화 연구임</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2608.30466'>CHASE: How Content Ecosystems Are Reshaped When Ranking Is the Only Target</a></td><td>27</td><td>0</td><td>NLP</td><td>LLM 랭킹 신호만을 목표로 콘텐츠를 반복 최적화하면 생태계가 동질화된다는 시뮬레이션 연구임</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2608.30672'>HiRS-Agent: A Hierarchical Multi-Agent System for Reliable Long-Horizon Remote Sensing Task Solving</a></td><td>27</td><td>0</td><td>Multimodal</td><td>원격탐사 장기 태스크를 관리자-전문가 계층 멀티에이전트로 안정화한 시스템임</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2608.31082'>Token-Efficient Data Reasoning Agents via Adaptive Structuring of Unstructured Data</a></td><td>27</td><td>0</td><td>NLP</td><td>비정형 문서를 질의에 따라 적응적으로 구조화해 재사용하는 agentic data cracking 개념을 제안함</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2608.31105'>BLOOM-WILT: Logit Tilting for Behaviour Elicitation in Automated LLM Auditing</a></td><td>27</td><td>0</td><td>NLP</td><td>logit tilting으로 배포된 LLM의 희귀 행동을 표본 효율적으로 유도해내는 자동 감사 파이프라인임</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2608.28826'>Dual Park-Ravani Interpolation of Rigid Motions: Acceleration-Field Continuity and Holonomic Hermite Repair</a></td><td>26</td><td>3</td><td>Robotics</td><td>강체 운동 보간의 가속도장 연속성을 증명한 순수 기구학 이론 연구로 학습 기반 로봇 지능과는 거리가 있음.</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2608.30400'>Real-Time Scene-Adaptive Tone Mapping for High-Dynamic Range Object Detection</a></td><td>26</td><td>2</td><td>CV</td><td>자율주행용 HDR 톤매핑 실시간 파이프라인으로 detection 성능 개선 위주의 engineering 기여임</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2608.30872'>SurgSkill-Bench: A Benchmark for Multimodal Surgical Skill Assessment</a></td><td>26</td><td>2</td><td>CV</td><td>수술 영상-점수-코멘트를 함께 쓰는 외과술기 평가 벤치마크로 로봇수술과는 거리 있는 평가 태스크임</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2608.31065'>Multimodal Shared Latent Representation of Narration, Microscope and iOCT Images for Phase Recognition in Vitreoretinal Surgery</a></td><td>26</td><td>2</td><td>Multimodal</td><td>안과수술 내레이션-현미경-iOCT를 공유 잠재공간에 정렬한 논문이라 수술로봇과는 결이 다르나 멀티모달 정렬 기법은 참고 가능함</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2608.29296'>When Do Larger Batches Help Scale LLM Reinforcement Learning?</a></td><td>26</td><td>2</td><td>RL</td><td>LLM RL 학습에서 배치 크기와 처리량의 trade-off를 분석한 시스템 연구로 로보틱스 RL 학습 인프라에 일부 참고될 수 있음</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2608.29349'>Information-Based Calibration of Uncertainty Quantification in Product-of-Experts Gaussian Process Models</a></td><td>26</td><td>2</td><td>LG</td><td>product-of-experts GP의 분산 과대추정을 보정한 방법으로 불확실성 정량화 일반기법이나 로보틱스 응용 실험은 없음</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2608.29598'>On the Resilience of Text-to-Video Diffusion Models to Hardware Faults</a></td><td>26</td><td>2</td><td>Video</td><td>text-to-video 생성모델의 하드웨어 결함 강건성을 처음 체계적으로 분석한 신뢰성 연구로 생성 모델 failure 이해에 참고되나 로보틱스 응용은 아님</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2608.30263'>Centering before Pruning: Lightweight Geometry Correction for Diversity-Based Visual Token Pruning in LVLMs</a></td><td>26</td><td>1</td><td>Multimodal</td><td>LVLM 토큰 프루닝에서 centering으로 diversity와 distinctiveness 분리하는 분석이나 로보틱스와 무관한 incremental efficiency 기여임</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2608.29494'>Learning Human Health and Diseases from 24-hour Wrist Movement</a></td><td>26</td><td>1</td><td>Multimodal</td><td>손목 가속도계 24시간 신호로 질병을 예측하는 self-supervised foundation model로 건강 응용이라 로보틱스와 거리 있음</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2608.30323'>Generative multi-domain transfer learning for fault detection in data-scarce wind turbines</a></td><td>26</td><td>1</td><td>LG</td><td>풍력터빈 이상탐지를 위한 domain mapping 기법으로 failure detection 주제와 개념적으로만 닿아있고 로봇 도메인 아님.</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2608.30952'>One Policy Is Enough: Single-Agent Reinforcement Learning Outperforms Tree Search for Chemistry Tool Learning</a></td><td>26</td><td>1</td><td>RL</td><td>화학 도구 사용에서 tree search를 단일 정책 RL로 대체해 성능과 비용을 모두 개선함. search 대체라는 아이디어는 test-time 추론과 결이 있으나 도메인은 화학임.</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2608.30902'>Low-Resource Preference Adaptation of LLMs via Activation-Based Label Propagation</a></td><td>26</td><td>1</td><td>NLP</td><td>activation 기반 선형 프로브로 저자원 선호 라벨 전파, 소량 라벨 활용법이 RLHF에 일반화 가능함</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2608.28620'>Preference Elicitation for Policy Optimization and Application to Aligning Heart Transplantation with Human Values</a></td><td>26</td><td>1</td><td>AI</td><td>선호 elicitation으로 utility function을 학습해 정책 최적화, cutting-plane 알고리즘은 reward learning 일반에 참고할 만함</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2608.28639'>Reward-Oracle MCTS for Formal Theorem Proving: Sample-Efficient Search and the Need for Kernel-Level Proof Auditing</a></td><td>26</td><td>1</td><td>RL</td><td>컴파일러를 순수 reward oracle로 쓰는 MCTS 정리증명 프레임워크, tree search 방법론이 로봇 planning에 참고할 만함</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2608.30520'>Learning-Assisted Congestion-Aware Route Scheduling for Semiconductor Fab Material Control Systems</a></td><td>26</td><td>1</td><td>LG</td><td>반도체 팹 자재이송 로봇의 혼잡 인지 경로 스케줄링을 학습 기반으로 개선함, multi-robot 스케줄링과 맥이 닿지만 로봇 지능 자체를 다루진 않음</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2608.31057'>Measure Before You Manage: Evaluating Agent Working Memory in Coding Agents</a></td><td>26</td><td>1</td><td>NLP</td><td>코딩 에이전트의 working memory를 객체 종류별로 다르게 관리해야 함을 실증한 연구임, robot memory 설계에도 참고할 만한 관찰이지만 대상은 코딩 에이전트임</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2608.30103'>Graph4BiLO: Graph Neural Network Approximation for Bilevel Mixed-Integer Linear Optimization</a></td><td>26</td><td>0</td><td>LG</td><td>bilevel MILP를 GNN으로 근사하는 방법으로 조합 최적화 분야 기여이나 로보틱스 연관성 없음.</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2608.30382'>Convergence rates for the RMSprop optimizer with full control of the hyperparameters</a></td><td>26</td><td>0</td><td>LG</td><td>RMSprop의 하이퍼파라미터 전반에 걸친 균일 오차 상계를 증명한 최적화 이론 논문으로 로봇과 무관함.</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2608.30585'>The Safety Relay in Roleplay Jailbreaks: A Component-Resolved Causal Analysis of Harm Recognition and Refusal</a></td><td>26</td><td>0</td><td>NLP</td><td>LLM 롤플레이 jailbreak의 뉴런 수준 기전을 분석한 해석가능성 연구로 로보틱스와 무관함.</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2608.30720'>Tracing distinguishability through transformer processing with stochastic LayerNorm</a></td><td>26</td><td>0</td><td>Representation Learning</td><td>표현 간 statistical distinguishability를 정보이론적으로 추적한 해석가능성 연구로 로보틱스와 무관함.</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2608.31046'>Does On-Policy Distillation Really Distill? From Noisy Teacher to Self-Improvement</a></td><td>26</td><td>0</td><td>NLP</td><td>on-policy distillation이 실제로는 저확률 토큰 억제로 작동함을 규명하고 teacher-free 대안을 제안함. LLM 학습 분석으로 로보틱스와 무관함.</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2608.29251'>GuardianAgent: Policy-Conditioned Risk-Adaptive Anonymization with Verified Adversarial Escalation</a></td><td>26</td><td>0</td><td>NLP</td><td>정책 조건부 위험 적응형 익명화 프레임워크임, 프라이버시 보호 엔지니어링 성격이 강함</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2608.29345'>BIRD-History: A Benchmark for History-Driven Text-to-SQL with Fine-Grained Knowledge Annotations</a></td><td>26</td><td>0</td><td>NLP</td><td>과거 SQL 로그를 활용한 history 기반 text-to-SQL 벤치마크와 retriever를 제안함</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2608.29348'>Extending TotalSegmentator: Predicting Patient and Acquisition Characteristics from CT and MR Images</a></td><td>26</td><td>0</td><td>CV</td><td>CT/MR 영상에서 환자·촬영 메타데이터를 예측하는 멀티태스크 모델임, 임상 인프라용 실용 연구임</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2608.29387'>EvoGenUI-Bench: Evaluating LLMs as Multi-Turn Generative UI Assistants</a></td><td>26</td><td>0</td><td>NLP</td><td>멀티턴 생성형 UI 유지보수 능력을 평가하는 벤치마크임, 턴 간 상태 동기화 실패 유형 분석이 기여임</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2608.30429'>EvoSkill Injection: Red-Teaming Autonomous Skill Generation and Evolution in Self-Evolving Agents</a></td><td>26</td><td>0</td><td>NLP</td><td>self-evolving agent의 skill 생성·진화 과정에 대한 red-teaming 위협 모델을 정의함</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2608.29194'>RLG-TPV: Radar- and LiDAR-Guided Tri-Perspective View Fusion for Camera-Radar 3D Object Detection</a></td><td>25</td><td>3</td><td>3D Vision</td><td>레이더·LiDAR로 카메라-레이더 3D 탐지의 TPV 표현을 보강하는 멀티모달 융합임. 자율주행 센서 융합 엔지니어링 수준임</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2608.29000'>Coding What Matters: A Semantic-Aware Memory Interface for Energy-Efficient Perception in Autonomous Vehicles</a></td><td>25</td><td>3</td><td>Robotics</td><td>의미 중요도 기반 메모리 인코딩으로 AV 인지 파이프라인 에너지를 절감한 연구로 경량화 방향이라 랩 우선순위와는 맞지 않음.</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2608.29100'>Agri-Sim: Agricultural Simulation Platform for Embodied Intelligence Evaluation in Greenhouse Robotics</a></td><td>25</td><td>3</td><td>Robotics</td><td>온실 농업 로봇을 위한 Unity-ROS2 시뮬레이션 플랫폼 구축 논문으로 알고리즘적 기여보다 인프라 엔지니어링에 가까움.</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2608.29108'>From Multi-Modal Paths to Executable Trajectories: A Trajectory Planning Framework for 4WIS Robots</a></td><td>25</td><td>3</td><td>Robotics</td><td>4륜 독립조향 로봇의 모드 인지 경로탐색·궤적 최적화를 결합한 엔지니어링 연구로 특정 로봇 형태에 국한된 incremental 기여임.</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2608.29211'>Ground-to-Satellite Localization in Unconstrained Image Collections for 3D Scene Reconstruction</a></td><td>25</td><td>2</td><td>3D Vision</td><td>SfM 제약을 이용한 지상-위성 교차뷰 위치추정으로 3D 복원을 지오등록하는 연구임. 대규모 매핑에 참고할 만하나 로봇 직접 적용은 없음</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2608.29759'>SynCrash: A Multi-Stage Pipeline for Zero-Shot Accident Detection and Localization in Traffic Surveillance Video</a></td><td>25</td><td>2</td><td>CV</td><td>CCTV 영상에서 제로샷 사고 탐지·위치추정을 하는 다단계 파이프라인임. 자율주행 안전 워크숍용 엔지니어링 파이프라인임</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2608.29891'>MASQ: Mask-Aware Spatiotemporal Quantization for Unsupervised Skeleton Action Segmentation</a></td><td>25</td><td>2</td><td>RL</td><td>골격 기반 비지도 행동 분할에서 마스킹·양자화 충돌을 해소하는 프레임워크임. skill segmentation과 관련 있으나 사람 행동 데이터 위주임</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2608.29980'>FIS-OT: Feature-Induced Optimal Transport for Unsupervised Action Segmentation</a></td><td>25</td><td>2</td><td>RL</td><td>지역 정보로 optimal transport 의사라벨의 확증편향을 줄이는 비지도 행동 분할 프레임워크임. skill segmentation 관련 있으나 사람 행동 데이터 위주임</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2608.29137'>Chat-Edit-3D++: Interactive 3D and 4D Scene Editing via Large Language Models</a></td><td>25</td><td>1</td><td>3D Vision</td><td>LLM으로 3D/4D 장면 편집을 오케스트레이션하는 대화형 도구임. 콘텐츠 편집 응용이라 로봇과 거리 있음</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2608.29233'>Generalization over Memorization: Generalization-Aware Diffusion Adaptation for Single-Image Multi-View Synthesis</a></td><td>25</td><td>1</td><td>3D Vision</td><td>단일 이미지 멀티뷰 합성 챌린지 우승 솔루션임. 검증 설계 통찰은 있으나 대회용 엔지니어링 위주임</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2608.29243'>DARD: Zero-Shot Degradation-Aware Retinex-Guided Diffusion for Low-Light Image Enhancement</a></td><td>25</td><td>1</td><td>CV</td><td>Retinex 기반 zero-shot 저조도 향상 확산 프레임워크임. downstream segmentation 개선 확인했으나 일반 이미지 향상 연구임</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2608.29269'>LightFuse: Relightable Interactive Gaussian Scene Reconstruction via Multi-Scan Fusion and 2D Gaussian Ray Tracing</a></td><td>25</td><td>1</td><td>3D Vision</td><td>2D Gaussian 기반 재조명 가능 인터랙티브 장면 재구성임. 물리 기반 렌더링 연구지만 로봇 응용은 없음</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2608.29733'>XDG: Accelerated Visual Disambiguation</a></td><td>25</td><td>1</td><td>3D Vision</td><td>3D foundation model 백본을 재활용해 SfM의 도플갱어 문제를 3배 빠르게 해결하는 기법임. 매핑 파이프라인 효율화 수준임</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2608.29974'>SpanCalib-VLM: Calibrated Hallucination Span Detection in Vision-Language Models</a></td><td>25</td><td>1</td><td>Multimodal</td><td>생성형·판별형 시스템을 결합해 VLM 환각 span을 캘리브레이션된 신뢰도로 탐지하는 공유 태스크 논문임. VLM 신뢰도 문제로 참고 가치 있으나 로봇 적용은 없음</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2608.30916'>Selection-Aware Stress Testing for Interactive Agents</a></td><td>25</td><td>1</td><td>LG</td><td>에이전트 평가에서 selection bias를 통계적으로 통제하는 프로토콜 연구로 방법론적 참고는 가능하나 로봇 도메인 아님.</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2608.28623'>Looking Again: Measuring Sycophancy in the Reasoning Chains of Multimodal Models Under Pressure</a></td><td>25</td><td>1</td><td>Multimodal</td><td>멀티모달 추론모델의 sycophancy를 reasoning chain 단위로 측정한 벤치마크임 - failure mode 분석이라는 점은 흥미로우나 임베디드 로봇 실패탐지와는 결이 다름</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2608.30632'>GMTS: Gradient Magnitude-based Token Selection Improves RLVR Training for LLM Reasoning</a></td><td>25</td><td>1</td><td>RL</td><td>gradient magnitude 기반 토큰 선택으로 RLVR 학습 개선, RL 학습 기법으로 일반화 가능성 있음</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2608.30719'>Mind the Gap: Theory-of-Mind-Grounded Friction for Epistemic Alignment</a></td><td>25</td><td>1</td><td>NLP</td><td>Theory-of-Mind 기반 belief divergence를 friction 신호로 활용, HRI의 belief modeling에 약하게 참고 가능함</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2608.28638'>Self-Evolving Skills via Surrogate-Guided Solve-and-Reproduce</a></td><td>25</td><td>1</td><td>AI</td><td>재현 가능성을 검증하는 solve-and-reproduce 프로토콜로 스킬을 자기진화시킴, 스킬 체이닝 학습 방법론과 개념적으로 닿음</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2608.28694'>SNF-Bench: Separating Static Drift from Natural Flow in Long-Horizon Fixed-Camera Video Generation</a></td><td>25</td><td>0</td><td>Video</td><td>고정 카메라 장기 비디오 생성에서 정적 드리프트와 동적 흐름을 분리 평가하는 벤치마크임. 로봇과 무관함</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2608.29313'>Hyper3-CLIP: Hierarchy-Conditioned Hyperbolic Vision-Language Training</a></td><td>25</td><td>0</td><td>Multimodal</td><td>계층 구조를 인코딩하는 hyperbolic VLM 학습법임. representation learning 관점에서 흥미로우나 로봇 적용은 없음</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2608.29335'>GenFirst: Generation Before Reconstruction for Stable End-to-End Latent Generative Modeling</a></td><td>25</td><td>0</td><td>Generative</td><td>latent collapse 방지를 위한 generation-before-reconstruction 학습 전략임. 표현학습 통찰은 일반적이나 로봇 적용은 없음</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2608.29783'>InspectorGPT: A Comparative Reasoning Enhanced VLM for Comprehensive Industrial Anomaly Detection</a></td><td>25</td><td>0</td><td>Multimodal</td><td>정상 참조 이미지와 비교 추론하는 산업 이상탐지 VLM임. CoT+GRPO 학습이 흥미로우나 로봇과 무관함</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2608.30070'>Selection, Representation, and Execution in Sparse Fourier Neural Operators</a></td><td>25</td><td>0</td><td>LG</td><td>FNO sparsity와 실제 속도 향상 사이 괴리를 실증적으로 분석한 efficiency 연구임. 로보틱스와 무관하고 benchmark성 분석에 가까움.</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2608.30252'>Strong Drafts Need Compact Memories: Long-Context Speculative Decoding with Compressed KV Cache</a></td><td>25</td><td>0</td><td>NLP</td><td>long-context LLM 디코딩 가속 기법으로 로보틱스와 무관한 순수 efficient inference 연구임.</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2608.30254'>Exact Recovery Thresholds for Weighted Data Selection in Vector-Valued Linear Regression</a></td><td>25</td><td>0</td><td>LG</td><td>weighted data selection의 이론적 threshold를 규명한 통계학습 이론 논문으로 로봇 응용과 무관함.</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2608.30390'>Uncertainty of Vision Medical Foundation Models</a></td><td>25</td><td>0</td><td>CV</td><td>의료 비전 파운데이션 모델의 conformal prediction 보정 연구로 로보틱스와 무관함.</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2608.30229'>Quantifying and Mitigating Korean Jamo-Level Typographical Vulnerabilities in Large Language Models</a></td><td>25</td><td>0</td><td>NLP</td><td>한국어 자모 단위 오타 취약성 분석과 선택적 CoT 적용, 견고성 연구지만 로봇과 무관함</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2608.30437'>Graph Evidence Is Not Enough: Diagnosing Native Decoder Use in Graph-Augmented LLMs</a></td><td>25</td><td>0</td><td>NLP</td><td>그래프 증거가 디코더에 실제로 쓰이는지 진단하는 벤치마크, 텍스트 그래프 추론 연구임</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2608.29139'>More Perspectives, Stronger Signals: Multi-Perspective Enhancement and Progressive Fusion for Multimodal Entity Representation Learning</a></td><td>25</td><td>0</td><td>Multimodal</td><td>멀티모달 엔티티 표현학습에 multi-perspective와 progressive fusion을 더한 module 추가형 연구임</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2608.29971'>EDGE: Engine for Deterministic Graph Evaluation through Conversation Simulation from Graph Structured DSL Configuration</a></td><td>25</td><td>0</td><td>NLP</td><td>멀티에이전트 대화 결정론성을 그래프 DSL 기반으로 측정하는 평가 프레임워크임</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2608.30022'>Automatic Conversion of NICE Guidelines to an Executable Computational Model Using Large Language Models</a></td><td>25</td><td>0</td><td>NLP</td><td>임상 가이드라인을 LLM으로 실행 가능한 규칙 모델로 변환하는 응용 연구임</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2608.30050'>Spec2Twin-Chain: Orchestrating Bi-Level Optimization with LLMs for Blockchain Digital Twin Construction</a></td><td>25</td><td>0</td><td>LG</td><td>블록체인 디지털 트윈 구축을 LLM 상위-시뮬레이션 하위 이중 최적화로 자동화함, 도메인이 좁음</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2608.30322'>Ignorance or Incompetence? Constructing Knowledge-Gated, Verifiable Tasks for LLM Agents</a></td><td>25</td><td>0</td><td>NLP</td><td>에이전트가 지식 부재인지 능력 부족인지 구분하는 knowledge-gated 태스크 구성법을 제안함</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2608.28884'>MineCEraft: Evaluating Language Models as Construction Engineers in the World of Minecraft</a></td><td>24</td><td>2</td><td>Embodied AI</td><td>마인크래프트 건설 공학 지시 수행 벤치마크, 공간 추론 과제라 embodied spatial reasoning에 약하게 참고 가능하나 텍스트 지시 기반임</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2608.30975'>MR-JEPA: A General Purpose Video Foundation Model for Cardiac MRI</a></td><td>24</td><td>1</td><td>Multimodal</td><td>JEPA를 심장 MRI 비디오에 적용한 foundation model로 아키텍처는 JEPA 계열이나 의료 도메인이라 로보틱스와 무관함</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2608.31106'>DreamX-Creator: Democratizing Native Audio-Video Generation at 2K Resolution</a></td><td>24</td><td>1</td><td>Multimodal</td><td>7B 규모 native 오디오-비디오 동시생성 시스템으로 생성모델 기여이나 로보틱스 응용은 아님</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2608.28896'>Conservative Hybrid Graph Networks for Process Systems with Learned Routing</a></td><td>24</td><td>1</td><td>LG</td><td>공정 네트워크의 라우팅을 학습하며 질량보존을 강제하는 하이브리드 그래프망으로 로보틱스와 거리 있음</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2608.28948'>From the Loss Landscape to Diverse Feature Learning in Neural Networks</a></td><td>24</td><td>1</td><td>LG</td><td>손실 지형과 mode connectivity를 다룬 박사논문으로 일반 이론 기여이나 로보틱스 응용은 아님</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2608.29458'>Reference-Grafting Matches Fine-Tuning at Eliciting Sandbagged Capabilities</a></td><td>24</td><td>1</td><td>NLP</td><td>sandbagging 모델의 숨은 능력을 activation grafting으로 끌어내는 AI safety 연구로 로보틱스와 무관함</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2608.29461'>A Causal Model for Locating and Unlocking Sandbagging in Model Organisms</a></td><td>24</td><td>1</td><td>NLP</td><td>sandbagging의 인과 메커니즘을 residual stream에서 찾아낸 해석가능성 연구로 로보틱스와 무관함</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2608.29472'>Knowledge Distillation under Teacher Misspecification: An Order-Parameter Analysis of the Gap between Teacher Mimicry and Task Performance</a></td><td>24</td><td>1</td><td>LG</td><td>teacher misspecification 하에서 distillation과 실제 task 성능의 괴리를 이론적으로 분석한 논문으로 로보틱스 응용은 아님</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2608.30923'>Towards Stream Learning on Embedded Systems: Benchmarking the Memory Consumption of Stream Learning Methods</a></td><td>24</td><td>1</td><td>LG</td><td>임베디드 환경에서 스트림 학습기의 메모리 사용을 벤치마킹한 연구로 온디바이스 로봇 학습에 참고 가능하나 경량화 중심이라 우선순위 낮음.</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2608.29034'>A Unifying Perspective on Language Model Representations: From Filler-Role Structure to Mechanistic Interpretability</a></td><td>24</td><td>1</td><td>LG</td><td>필러-역할 결합으로 여러 해석가능성 기법을 통합 설명하는 이론적 연구임 - 통찰력 있으나 로봇 응용은 없음</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2608.29109'>Recognition-Refusal Misalignment in LLMs: Why Models Answer Structurally Unanswerable Questions</a></td><td>24</td><td>1</td><td>LG</td><td>구조적으로 답할 수 없는 질문에 답하는 실패가 인식 문제가 아니라 라우팅 문제임을 보인 해석가능성 연구임 - 실패탐지 관점에서 흥미로우나 수학/코드 텍스트 한정임</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2608.30702'>An Agentic Retrobiosynthesis Framework with Learned Frontier Selection</a></td><td>24</td><td>1</td><td>AI</td><td>생합성 역합성 탐색에서 frontier 선택 정책을 학습, 탐색 정책 학습 방법론은 일반화 가능성 있음</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2608.31119'>PaperGym: Rubric-Centered Evolution for Research-Plan Generation</a></td><td>24</td><td>1</td><td>AI</td><td>논문 구조에서 rubric을 추출해 연구계획 생성 RL 환경으로 쓰는 프레임워크임</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2608.30295'>CateKV: On Sequential Consistency for Long-Context LLM Inference Acceleration</a></td><td>24</td><td>0</td><td>NLP</td><td>long-context KV cache head 특성 기반 압축 기법으로 이미 ICML 2025 게재됐고 로보틱스와 무관함.</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2608.30310'>Tail-Replay: Escaping the Curse of Linear Attention in Prefix Caching for Hybrid LLMs</a></td><td>24</td><td>0</td><td>NLP</td><td>hybrid linear attention 모델의 prefix reuse 효율화 기법으로 로봇 응용 없음.</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2608.30386'>DASC: Decay-Aware State Compression for Hybrid Linear-Attention Serving</a></td><td>24</td><td>0</td><td>NLP</td><td>linear attention 모델의 recurrent state 압축 서빙 기법으로 로봇과 무관한 LLM 인프라 연구임.</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2608.30528'>PAC: Progress-Augmented Advantage Curriculum for Multi-Task Reinforcement Learning of LLMs</a></td><td>24</td><td>0</td><td>RL</td><td>LLM 추론 강화학습의 태스크 커리큘럼을 진행도 기반으로 조정한 방법으로 로보틱스와 무관함.</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2608.30960'>Singular Curvature in ReLU Training:Differentiation and the Gradient-Flow Limit Need Not Commute</a></td><td>24</td><td>0</td><td>LG</td><td>hard-ReLU GD의 이산 미분과 gradient flow 극한이 교환되지 않음을 증명한 이론 논문으로 로보틱스와 무관함.</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2608.31157'>Sharp Approximation Rates for Neural Networks with Affine Latent Parameterizations</a></td><td>24</td><td>0</td><td>LG</td><td>hypernetwork류의 latent-parameter 근사 오차의 sharp rate를 증명한 이론 연구로 로보틱스와 무관함.</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2608.30258'>Stratified Consistency Distillation for Natural Language Formalization</a></td><td>24</td><td>0</td><td>NLP</td><td>자연어-논리식 변환 정확도 향상 위한 distillation 기법임</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2608.30372'>Auditing MCQA Benchmarks through Probability Landscapes</a></td><td>24</td><td>0</td><td>NLP</td><td>MCQA 벤치마크 품질 감사용 확률 분포 분석 도구임</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2608.30427'>Ceiling-Clipped Acceptance Histograms Indicate Stranded Speed-up in Block-Diffusion Speculative Decoding</a></td><td>24</td><td>0</td><td>LG</td><td>block-diffusion speculative decoding의 stranded speed-up 진단과 재학습 기법, LLM 추론 효율화 연구임</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2608.30461'>From Final Artifacts to Trajectories: Retrospective Process Supervision for Evidence-Grounded Long-Form Generation</a></td><td>24</td><td>0</td><td>NLP</td><td>완성물 역산으로 궤적 데이터를 생성하는 self-improving 프레임워크, 장문 생성 특화임</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2608.30468'>Hi-Q: Hierarchical Evidence-guided Query Refinement for Multi-Hop Question Answering</a></td><td>24</td><td>0</td><td>NLP</td><td>증거 기반 계층적 쿼리 정제로 multi-hop QA 개선, IR 특화 연구임</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2608.30619'>Hidden Threat in Synthetic Data: Covert Targeted Bias Injection through Benign Text</a></td><td>24</td><td>0</td><td>NLP</td><td>무해해 보이는 synthetic data로 편향을 은닉 주입하는 보안 위협 연구임</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2608.29063'>Agent2UCB: Agentic System for Generative Engine Optimization</a></td><td>24</td><td>0</td><td>NLP</td><td>LLM 검색엔진 대상 콘텐츠 최적화를 bandit으로 자동화한 응용 시스템임, 연구적 기여보다 엔지니어링 성격이 강함</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2608.29127'>Beyond Correctness: Validity-Oriented Evaluation of Biomedical LLM Judges</a></td><td>24</td><td>0</td><td>NLP</td><td>biomedical LLM judge 평가를 정확도 외 견고성·형식 준수까지 확장한 평가 프로토콜 연구임</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2608.29301'>Predicting Future Organ Dysfunction in ICU Patients Using Temporal Convolutional Networks on MIMIC-IV Data</a></td><td>24</td><td>0</td><td>LG</td><td>ICU 환자의 미래 장기기능 저하를 TCN으로 예측한 임상 응용 연구임, 모델이 최근 관측치에만 의존한다는 한계도 스스로 지적함</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2608.29965'>Review Before Trust: Source-Grounded Integrity Gates for AI-Assisted Personal Health Records</a></td><td>24</td><td>0</td><td>NLP</td><td>의료기록에서 LLM 생성 데이터를 원문 대조로 검증하는 게이트를 도입한 응용 시스템임</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2608.30056'>Game-Agnostic Value Functions through Automatic JSON Feature Extraction</a></td><td>24</td><td>0</td><td>RL</td><td>게임에 무관한 JSON 기반 value function을 만든 소규모 연구임</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2608.30192'>FaVOR: LLM-Based Agentic Framework for Factor Mining via Empirical Validation</a></td><td>24</td><td>0</td><td>NLP</td><td>금융 팩터 마이닝에서 수익률만 최적화할 때 경제적 의미가 깨지는 문제를 가설-검증 루프로 보완함</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2608.30250'>Generating Workflow DAGs from Natural Language with Non-Reasoning LLMs</a></td><td>24</td><td>0</td><td>NLP</td><td>자연어 라우팅 규칙을 워크플로 DAG로 변환하는 산업 응용 연구임, 결정론적 컴파일러로 신뢰성을 높인 점이 실용적임</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2608.30405'>Dense Clinical Contrasts Enhance Medical Knowledge Updating in Large Language Models</a></td><td>24</td><td>0</td><td>NLP</td><td>의료지식 갱신에서 supervision 포맷이 결과에 미치는 영향을 비교한 벤치마크 연구임</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2608.30498'>CM2: Multimodal Cultural Reasoning via an Integrated Multi-Agent Framework</a></td><td>24</td><td>0</td><td>Multimodal</td><td>멀티모달 문화 추론을 위한 멀티에이전트 프레임워크임, 조합형 개선 연구임</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2608.30556'>AdaPath: Query-Adaptive Path-Finding via Path-Bank for Multi-Hop Implicit Biomedical KGQA</a></td><td>24</td><td>0</td><td>NLP</td><td>생의학 KGQA에서 query-adaptive meta-path를 검색해 multi-hop 추론을 돕는 연구임</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2608.30785'>SkillZip Pro: Execution-Aware Dynamic Compression of Progressively Loaded Skills for Self-Evolving Agents</a></td><td>24</td><td>0</td><td>NLP</td><td>progressive loading되는 agent skill 번들을 파일 간 압축하는 엔지니어링 기법임</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2608.28627'>Machine Learning-Enhanced Tabu Search for Tactical Wireless Network Design</a></td><td>23</td><td>1</td><td>AI</td><td>GNN이 Tabu Search의 이동 선택을 학습해 조합최적화 효율을 높임, 탐색 안내 방법론이 모션 플래닝에 전이 가능함</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2608.29206'>Benevolent Bias in Multi-Turn Human-Agent Dialogue</a></td><td>23</td><td>0</td><td>NLP</td><td>온화한 어조 뒤에 숨은 편향을 탐지 대상으로 정의하고 코퍼스를 구축함, 탐지기 성능 격차 분석이 주 기여임</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2608.30832'>A Dual-Cam Parallel Elastic Actuator with Shared Gas-Spring Compensation for Humanoid Ankles</a></td><td>22</td><td>3</td><td>Manipulation</td><td>휴머노이드 발목용 병렬 탄성 액추에이터 기계 설계 논문임 - FEA·기구학 시뮬레이션 중심이라 학습 기반 연구와 관련성 낮음</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2608.29510'>ARMOR: Manifold-Oriented Training for Adversarially Robust Aerial Object Detection under Data Scarcity</a></td><td>22</td><td>2</td><td>CV</td><td>데이터 희소 환경에서 항공 물체탐지의 적대적 패치 방어 기법임. 드론 응용이나 방어 엔지니어링 수준임</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2608.28669'>MIRAGE-CAD: Construction-Mediated Multimodal Generation of Executable CAD Programs</a></td><td>22</td><td>1</td><td>CV</td><td>자연어·이미지·점군에서 CAD 프로그램 복원하는 멀티모달 생성임. 로봇과 무관하고 CAD 응용 중심임</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2608.29928'>Biomechanical 3D Body: Self-Supervised Distillation of Biomechanical Pose from a 3D Body Foundation Model</a></td><td>22</td><td>1</td><td>3D Vision</td><td>단안 이미지에서 생체역학적 관절각을 distill하는 기법임. 임상 응용이라 로봇과 거리 있음</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2608.30305'>Learning to Restore More: Continual Capability Expansion for Pretrained Image Restoration Models</a></td><td>22</td><td>1</td><td>CV</td><td>image restoration continual capability expansion으로 로보틱스와 무관한 응용 논문임</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2608.30355'>Seeing the Unseen: Camouflaged Object Detection Beyond the Visible Spectrum</a></td><td>22</td><td>1</td><td>CV</td><td>멀티스펙트럴 위장 객체 탐지로 로보틱스와 무관한 응용 논문임</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2608.30817'>A Composition-Aware Pretraining Framework for Geospatial Foundation Models</a></td><td>22</td><td>1</td><td>CV</td><td>위성영상 foundation model에 fractional land-cover 구성비를 예측 목표로 추가한 사전학습으로 로보틱스와 거리 있음</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2608.30964'>Vision Models Predict Urban Scene Appraisal with Limited Neural Alignment</a></td><td>22</td><td>1</td><td>CV</td><td>도심 경관 평가에서 비전 임베딩과 뇌 반응 정렬을 분석한 신경과학 연구로 로보틱스와 거리 있음</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2608.28911'>SemKV: Semantic Mixed-Precision KV Cache Quantization Guided by the Quality Cliff for Long-Context LLM Inference</a></td><td>22</td><td>1</td><td>NLP</td><td>long-context LLM의 KV cache 양자화에서 quality cliff를 찾아 정밀도를 배분한 방법으로 로보틱스 응용은 아님</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2608.29070'>Selective Disclosure of Hidden Directives in Reasoning Models: Behavioral Asymmetry and Steering</a></td><td>22</td><td>1</td><td>NLP</td><td>추론모델이 hidden system prompt를 CoT에 비대칭적으로 노출하는 현상 분석으로 로보틱스와 무관한 AI safety 연구임</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2608.29411'>Where Induction Runs Out: Description-Length Difficulty and the Memorisation Gap in Integer-Sequence Benchmarks</a></td><td>22</td><td>1</td><td>NLP</td><td>OEIS 정수열 벤치마크가 사실상 암기를 측정한다는 걸 MDL로 보인 분석으로 로보틱스와 무관함</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2608.29513'>On the Plasticity Collapse in Continual Machine Unlearning</a></td><td>22</td><td>1</td><td>LG</td><td>연속적 machine unlearning에서 plasticity가 붕괴하는 현상을 분석한 논문으로 로보틱스와 무관함</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2608.29563'>HoopMind: A Real-Time Neural Game-Tree System for Opponent-Aware Possession Planning</a></td><td>22</td><td>1</td><td>RL</td><td>농구 possession을 게임트리로 풀어 실시간 전술을 제안한 응용으로 로보틱스와 무관함</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2608.29715'>Higher-Dimensional Rotary Position Embedding</a></td><td>22</td><td>1</td><td>NLP</td><td>RoPE를 고차원 회전으로 확장한 위치 임베딩 개선으로 로보틱스와 무관함</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2608.29765'>PruneShift: A Framework for Evaluating Decision Reliability in Structured Pruning</a></td><td>22</td><td>1</td><td>LG</td><td>구조적 프루닝에서 surrogate가 고른 결정 자체의 신뢰성을 검증하는 프레임워크로 efficient inference 평가방법론이나 로보틱스 응용은 아님</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2608.29867'>Partially Linear Autoencoders for Manifold Learning and Dimensionality Reduction</a></td><td>22</td><td>1</td><td>LG</td><td>오토인코더에서 인코더만 선형으로 제약해도 성능이 유지되는지 분석한 표현학습 연구로 로보틱스와 거리 있음</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2608.29869'>Towards an Expressivity-Normalized Energy-Demand Comparison of ANNs and SNNs</a></td><td>22</td><td>1</td><td>LG</td><td>ANN과 SNN의 표현력 대비 에너지효율을 이론적으로 비교한 논문으로 경량화 지향이라 로보틱스 우선순위와 맞지 않음</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2608.30317'>Online Estimation of Dynamic Origin-Destination Matrices Using Reinforcement Learning with Link-Flow Propagation Guidance</a></td><td>22</td><td>1</td><td>RL</td><td>교통 OD 수요 추정에 RL을 적용한 응용 연구로 navigation과는 결이 다르고 로봇 embodiment 없음.</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2608.30392'>Foundation Models Meet Agriculture: Challenges Beyond Pretraining</a></td><td>22</td><td>1</td><td>CV</td><td>지구관측 파운데이션 모델의 농업 적용 한계를 분석한 벤치마킹 연구로 embodied 로봇과는 거리가 있음.</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2608.28625'>Asymmetric Within-Document Predictive Learning for Scientific Document Representation</a></td><td>22</td><td>1</td><td>NLP</td><td>논문의 discourse 구조로 예측적 프리트레이닝하는 과학문헌 표현학습임 - JEPA식 예측 아이디어는 흥미로우나 텍스트 도메인 한정임</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2608.28707'>ReVA: A Region-Aware Visual Assistant for Visually Grounded Question Answering</a></td><td>22</td><td>1</td><td>Multimodal</td><td>region-aware VQA로 CLIP+LLM에 region bridge를 추가해 hallucination을 줄인 연구임 - 로봇 시각접지에 참고 가능하나 순수 VQA 벤치마크 중심임</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2608.28930'>The Hallucination Signal Is a Mean Shift: Why Simple Probes Suffice</a></td><td>22</td><td>1</td><td>LG</td><td>hallucination 프로브 신호가 단일 mean-shift 성분에 지배된다는 분석임 - 해석가능성 연구로 실패탐지에 참고 가치는 있으나 텍스트 LLM 한정임</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2608.29278'>Modality Fault Lines: Structural Corruptions Reveal Fragile Omni-Modal Reasoning</a></td><td>22</td><td>1</td><td>Multimodal</td><td>옴니모달 모델이 구조적으로 손상된 입력에서 얼마나 취약한지 진단한 벤치마크임 - 멀티모달 강건성 통찰이나 로봇 센서융합과는 별개 도메인임</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2608.29397'>AlgoWorlds: Benchmarking Tool Use for Global Optimization in Algorithmic Worlds</a></td><td>22</td><td>1</td><td>LG</td><td>도구사용 에이전트가 전역 최적해까지 도달하는지 평가하는 조합최적화 벤치마크임 - 의사결정 최적화 통찰은 있으나 로봇 도메인 아님</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2608.29464'>Chain-of-Thought Faithfulness of Reasoning Models Varies with Where and How Preference Cues Are Delivered</a></td><td>22</td><td>1</td><td>LG</td><td>선호 신호가 도구반환으로 오면 CoT에 덜 드러난다는 충실성 평가 벤치마크임 - reasoning 모니터링 통찰은 있으나 텍스트 에이전트 한정임</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2608.30147'>CAST: Critique-Aware Supervision for Training Reliable Long-Horizon Tool-Calling Agents</a></td><td>22</td><td>1</td><td>LG</td><td>장기 도구호출 에이전트의 행동 타당성을 비평 기반으로 학습시킨 연구임 - 실패 사전차단 관점은 로봇 실패탐지와 결이 비슷하나 리테일/헬스 텍스트 에이전트 도메인임</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2608.31035'>When Does Predictor-Based RL Align with Human Perception? A Study of Subjective Rewards in Codec-Based Speech Language Models</a></td><td>22</td><td>1</td><td>RL</td><td>주관적 reward가 인간 지각과 정렬되는 조건을 분석한 GRPO 연구, reward 설계 진단 방법론이 일반 RL에 참고할 만함</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2608.28695'>Weaving Visual Narratives: Agentic Image Bundle Composition Beyond Atomic Visual Matching</a></td><td>22</td><td>0</td><td>Multimodal</td><td>개별 이미지 매칭을 넘어 이미지 번들을 구성하는 검색 패러다임임. 개인 사진 정리 응용이라 로봇과 무관함</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2608.30205'>Diffusion-Based Refinement for Kilometer-Scale Probabilistic Precipitation Nowcasting</a></td><td>22</td><td>0</td><td>Video</td><td>강수량 nowcasting을 위한 diffusion 기반 ensemble 보정으로 로봇 응용 없음.</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2608.30674'>CoMPASS: Collaborative Molecular Property Prediction via Adaptive Small-Large Model Synergy</a></td><td>22</td><td>0</td><td>LG</td><td>GNN과 LLM을 결합한 분자 특성 예측 프레임워크로 로보틱스와 무관함.</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2608.29706'>The Depth Flow of Token Representations Is Nonlinear and Does Not Descend Its Own Density</a></td><td>22</td><td>0</td><td>LG</td><td>레이어를 관통하는 토큰 표현 흐름을 랑주뱅 모델로 적합시킨 해석가능성 연구임 - 이론적 흥미는 있으나 로봇 응용 없음</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2608.30224'>The Differential Reasoning Router: Operationalizing Cost-Aware LLM Annotation in E-commerce</a></td><td>22</td><td>0</td><td>NLP</td><td>e-commerce 어노테이션 비용 절감용 라우터, 산업 적용 논문임</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2608.30260'>Using Prosody to Predict Syntactic Structure</a></td><td>22</td><td>0</td><td>NLP</td><td>운율이 통사구조를 예측한다는 정보이론적 분석, 언어학 연구임</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2608.31076'>Learning to Evaluate Before Improving: Automatic Rubric Induction for Automatic Research Agents</a></td><td>22</td><td>0</td><td>AI</td><td>연구 에이전트를 위한 실행 전 rubric 자동 생성 프레임워크임</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2608.28600'>SHAPE of Chain-of-Thought in Math Reasoning</a></td><td>22</td><td>0</td><td>NLP</td><td>CoT를 수학교육 개념(semantic space·heuristic)으로 분석한 진단 프레임워크임</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2608.28648'>How Language Models Choose Sides: Internal Representations of Instruction Hierarchy</a></td><td>22</td><td>0</td><td>NLP</td><td>system-user 지시 충돌 시 내부 표현에서 결정 신호를 읽어내는 해석 가능성 연구임</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2608.28725'>Beyond the Answer Key: Robustness Evaluation of Large Language Models for Step-Level Mathematical Verification</a></td><td>22</td><td>0</td><td>AI</td><td>step-level 수학 검증에서 LLM의 견고성 격차를 분석한 벤치마크임</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2608.28945'>Automated Researchers Can Reliably Mitigate Alignment Failures</a></td><td>22</td><td>0</td><td>AI</td><td>자동화된 alignment 연구자가 인간 연구자보다 안전 벤치마크 개선에 낫다는 실증 연구임</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2608.29012'>Frequency Selective Neural Networks as a Foundation Architecture for Time Series Learning</a></td><td>22</td><td>0</td><td>LG</td><td>미분 가능 필터뱅크로 물리적으로 해석 가능한 시계열 파운데이션 아키텍처를 제안함</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2608.29223'>Computational Depth Measurement in Thermographic Video: Overcoming Spatial Overfitting via Spatio-Temporal Decoupling</a></td><td>22</td><td>0</td><td>CV</td><td>열화상 영상에서 결함 깊이 추정 시 공간적 overfitting을 줄이는 응용 엔지니어링 연구임</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2608.30091'>VERA: Authority-Preserving Edge Revocation for Federated AI-Agent Workflows</a></td><td>22</td><td>0</td><td>NLP</td><td>agent 위임 그래프의 권한 철회를 정확히 계산하는 프로토콜 연구임, 시스템 보안 성격이 강함</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2608.30234'>CoLa-ICD: A Knowledge-Enhanced Framework for Long-Tail Automated Medical Coding</a></td><td>22</td><td>0</td><td>NLP</td><td>long-tail ICD 코드에 외부 용어를 결합한 지식증강 의료코딩 연구임</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2608.30235'>LLM-Based Knowledge Graph Completion Combining Discrete Structural Coding with Similar Entity Information</a></td><td>22</td><td>0</td><td>NLP</td><td>지식그래프 완성에 구조 코딩과 유사 엔티티 정보를 결합한 조합형 개선 연구임</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2608.30419'>From Metaheuristics to Exact Methods: A CP-SAT Approach for Multi-Objective Healthcare Workforce Scheduling</a></td><td>22</td><td>0</td><td>LG</td><td>병원 인력 스케줄링을 CP-SAT로 정확히 푸는 제약 프로그래밍 연구임, 산업 응용 성격이 강함</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2608.30726'>Multimodal Adaptive Expert Selection with Text Routing and Ordinal Prototype Optimization for Sentiment Analysis</a></td><td>22</td><td>0</td><td>Multimodal</td><td>텍스트 라우팅 기반 MoE와 순서 인지 대조학습을 결합한 멀티모달 감성분석 연구임</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2608.30846'>VFR-Audit: Verdict-Level Reliability for Fairness Audits in Hospital Length-of-Stay Prediction</a></td><td>22</td><td>0</td><td>LG</td><td>병원 재원기간 예측의 공정성 감사 verdict가 재표본마다 뒤집히는 정도를 측정하는 지표임</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2608.31118'>When Does Bigger Help? A Controlled Study of LLM Scale for Ontology Learning</a></td><td>22</td><td>0</td><td>NLP</td><td>온톨로지 학습에서 LLM 스케일 효과를 통제 실험으로 분석함, 스케일보다 아키텍처·계열이 중요하다는 결론이나 로보틱스 무관함</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2608.30647'>What It Costs to Compose, Rebuild, and Correct Precomputed Memory</a></td><td>21</td><td>1</td><td>LG</td><td>precomputed memory의 조립·갱신·정정 비용을 실측한 시스템 연구, 메모리 관리 트레이드오프 분석임</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2608.30325'>Sequential Trajectories and Simultaneous Blending: Multi-Emotion Modeling for Instruction-Following TTS</a></td><td>21</td><td>0</td><td>NLP</td><td>다중 감정 TTS를 위한 hybrid reward RL, 음성 합성 특화 연구임</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2608.30398'>Beyond Polarization: The Generative Constraint of Chain-of-Thought in Pointwise Reranking</a></td><td>21</td><td>0</td><td>NLP</td><td>pointwise reranking에서 CoT의 구조적 한계 분석, IR 특화 연구임</td></tr>
<tr><td>486</td><td><a href='https://arxiv.org/abs/2608.30463'>More Capable, Less Faithful: A Multilingual Analysis of Mathematical (Un)Solvability Detection in LLMs</a></td><td>21</td><td>0</td><td>NLP</td><td>다국어 수학 unsolvability 탐지의 faithfulness 분석임</td></tr>
<tr><td>487</td><td><a href='https://arxiv.org/abs/2608.30627'>REER-PT: Reverse-Engineered Reasoning for Perplexity-Guided Pre-training Data Augmentation</a></td><td>21</td><td>0</td><td>NLP</td><td>perplexity 기반 사전학습 데이터 증강 기법, incremental 개선임</td></tr>
<tr><td>488</td><td><a href='https://arxiv.org/abs/2608.30679'>LCoT-GV: Graph Attention Networks for Verifying Long Reasoning Chains in Large Language Models</a></td><td>21</td><td>0</td><td>NLP</td><td>그래프 어텐션으로 long CoT 정합성을 검증하는 기법, 규모가 작은 실험임</td></tr>
<tr><td>489</td><td><a href='https://arxiv.org/abs/2608.30725'>Where Do Multilingual Vision-Language Encoders Fail on Low-Resource Languages?</a></td><td>21</td><td>0</td><td>Multimodal</td><td>다국어 vision-language 인코더의 저자원 언어 성능 저하 원인을 진단한 분석 연구임</td></tr>
<tr><td>490</td><td><a href='https://arxiv.org/abs/2608.30968'>CogEvol: Towards Efficient and Reliable Learning Environment Generation</a></td><td>21</td><td>0</td><td>AI</td><td>슬라이드·HTML 학습 콘텐츠 생성 모델, RL reward hacking 사례는 흥미로우나 교육 도메인 특화임</td></tr>
<tr><td>491</td><td><a href='https://arxiv.org/abs/2608.30987'>Stick to What You Know: A Study of Knowledge-Aligned Supervised Fine-Tuning</a></td><td>21</td><td>0</td><td>NLP</td><td>SFT 타겟을 base model 지식에 정렬시켜 hallucination 줄이는 기법임</td></tr>
<tr><td>492</td><td><a href='https://arxiv.org/abs/2608.28647'>Self-Specialized Teachers for Domain Post-Training</a></td><td>21</td><td>0</td><td>AI</td><td>도메인 특화 post-training이 일반 능력을 해치지 않도록 하는 self-teacher distillation 기법임</td></tr>
<tr><td>493</td><td><a href='https://arxiv.org/abs/2608.28806'>Enhancing SAE-based Steering via Neighbor Integrated Feature Selection</a></td><td>21</td><td>0</td><td>NLP</td><td>SAE steering에서 이웃 특징을 통합해 feature selection을 개선한 기법임</td></tr>
<tr><td>494</td><td><a href='https://arxiv.org/abs/2608.28997'>Verification abundance, adjudication scarcity: what happens to mathematical knowledge when proof checking becomes free</a></td><td>21</td><td>0</td><td>AI</td><td>커널 검증 수학 증명이 늘어도 의미론적 검증은 여전히 부족하다는 구조적 분석임</td></tr>
<tr><td>495</td><td><a href='https://arxiv.org/abs/2608.29175'>An Explainable Coherence Score for Detecting Temporal Inconsistencies in Political News</a></td><td>21</td><td>0</td><td>NLP</td><td>정치 뉴스의 시간적 모순을 탐지하는 해석 가능한 metric을 제안함, 응용 범위가 좁은 도메인 특화 연구임</td></tr>
<tr><td>496</td><td><a href='https://arxiv.org/abs/2608.29146'>Systematic Lightweight Method for Robotics Based on Strain Energy Distribution Optimization</a></td><td>20</td><td>3</td><td>Robotics</td><td>변형에너지 분포 균일화를 통한 로봇 경량 설계 방법으로 명시적으로 경량화 방향이라 랩 우선순위와 맞지 않음.</td></tr>
<tr><td>497</td><td><a href='https://arxiv.org/abs/2608.30222'>Optimized Modular Design and Development of a Tilt-Rotor Bicopter Drone</a></td><td>20</td><td>3</td><td>Robotics</td><td>틸트로터 바이콥터의 구조·공력 최적 설계 엔지니어링 연구로 학습 기반 지능과 무관함.</td></tr>
<tr><td>498</td><td><a href='https://arxiv.org/abs/2608.28673'>AdaptAV: Continuous Adaption of Vision Models for Autonomous Vehicles Using Cloud-based Oracle</a></td><td>20</td><td>2</td><td>CV</td><td>클라우드 오라클로 차량 비전 모델을 지속 재학습하는 시스템 엔지니어링임. 새로운 학습 패러다임은 아님</td></tr>
<tr><td>499</td><td><a href='https://arxiv.org/abs/2608.30055'>MiBOT: A head-worn robot that modulates cardiovascular responses through human-like soft massage</a></td><td>20</td><td>2</td><td>Robotics</td><td>두부 마사지 로봇의 생리적 효과를 검증한 응용 연구로 2024년 ICRA 게재분이며 학습 기반 로봇 지능과 무관함.</td></tr>
<tr><td>500</td><td><a href='https://arxiv.org/abs/2608.28678'>Evaluating Constrained Iterative Refinement for Scalable Vector Graphics Generation with Off-the-Shelf VLMs</a></td><td>20</td><td>1</td><td>Multimodal</td><td>VLM으로 SVG 생성하는 inference-time refinement 평가임. self-correction 한계 지적이 흥미로우나 로봇과 무관함</td></tr>
<tr><td>501</td><td><a href='https://arxiv.org/abs/2608.29043'>Di$^2$CycleSB: Towards High-Quality Unsupervised Nighttime Visibility Enhancement via Schrödinger Bridge Transformer</a></td><td>20</td><td>1</td><td>CV</td><td>야간 조도 개선을 Schrodinger bridge로 비지도 학습하는 연구임. 야간 인식에 도움될 수 있으나 일반 이미지 향상 위주임</td></tr>
<tr><td>502</td><td><a href='https://arxiv.org/abs/2608.29112'>NFAD: Nuisance-Filtered Anomaly Detection Under Distribution Shift</a></td><td>20</td><td>1</td><td>CV</td><td>산업 이상탐지에서 촬영조건 변화(nuisance)를 필터링하는 기법임. 분포 변화 강건성은 유의미하나 로봇 특화는 아님</td></tr>
<tr><td>503</td><td><a href='https://arxiv.org/abs/2608.29121'>Acoustically Grounded Cost Learning for Open-Vocabulary Audio-Visual Semantic Segmentation</a></td><td>20</td><td>1</td><td>Multimodal</td><td>오디오-비주얼 오픈보캡 segmentation을 위한 acoustic 기반 cost learning임. 로봇과 거리 있음</td></tr>
<tr><td>504</td><td><a href='https://arxiv.org/abs/2608.29220'>SGPDFuse: Semantically-Guided Physics-Disentanglement General Multi-Modal Image Fusion</a></td><td>20</td><td>1</td><td>CV</td><td>물리 원리를 분리한 멀티모달 이미지 융합 기법임. 로봇 인식에 쓸 수 있으나 일반 이미지 처리 연구임</td></tr>
<tr><td>505</td><td><a href='https://arxiv.org/abs/2608.29230'>Compact Snapshot Spectral Imaging with Calibration-Free Aperture Diffraction</a></td><td>20</td><td>1</td><td>CV</td><td>캘리브레이션 없는 스냅샷 분광 이미징 하드웨어·알고리즘 제안임. 센서 혁신이나 로봇 응용 검증은 없음</td></tr>
<tr><td>506</td><td><a href='https://arxiv.org/abs/2608.29852'>MariSat: A Maritime Dataset for Instance Segmentation of Objects in Satellite and Aerial Images</a></td><td>20</td><td>1</td><td>CV</td><td>위성·항공영상 해상 선박 인스턴스 분할 데이터셋임. 자율운항 응용 가능하나 데이터셋 논문 수준임</td></tr>
<tr><td>507</td><td><a href='https://arxiv.org/abs/2608.30281'>SELECT: SELEctive Context Transfer for Class-Incremental Semantic Segmentation</a></td><td>20</td><td>1</td><td>CV</td><td>class-incremental segmentation의 context transfer attention 개선으로 로보틱스와 관련 없는 incremental engineering임</td></tr>
<tr><td>508</td><td><a href='https://arxiv.org/abs/2608.30316'>Knowing Beyond the Known: Reinforced Knowledge Specification for Multi-Label Class-Incremental Learning</a></td><td>20</td><td>1</td><td>CV</td><td>multi-label class-incremental learning의 known/unknown 경계 문제 다루는 논문으로 로보틱스와 거리 있음</td></tr>
<tr><td>509</td><td><a href='https://arxiv.org/abs/2608.30563'>Modality Disentangled Learning for Incomplete Multimodal Emotion Recognition: A Primitive Memory Distillation Perspective</a></td><td>20</td><td>1</td><td>Multimodal</td><td>결측 모달리티 감정인식에서 모달리티별 memory distillation 다루는 논문으로 로보틱스 응용은 아님</td></tr>
<tr><td>510</td><td><a href='https://arxiv.org/abs/2608.30704'>TUE-Detector: A Tool-Using Expert MLLM-Based Detector for AI-Generated Videos</a></td><td>20</td><td>1</td><td>CV</td><td>AI 생성 비디오 탐지를 위한 tool-using MLLM 탐지기로 로보틱스와 무관함</td></tr>
<tr><td>511</td><td><a href='https://arxiv.org/abs/2608.30709'>RailSyn: Diagnosis-Guided Image Generation for Traceable Data Completion in Railway Foreign Object Detection</a></td><td>20</td><td>1</td><td>CV</td><td>철도 이물질 탐지용 진단 기반 합성 데이터 생성 논문으로 로보틱스와 거리 있음</td></tr>
<tr><td>512</td><td><a href='https://arxiv.org/abs/2608.30727'>RailGen: Improving Railway Intrusion Detection via Agent-Guided Small-Scale Foreign Object Generation</a></td><td>20</td><td>1</td><td>CV</td><td>철도 이물질 생성증강 및 탐지 프레임워크로 로보틱스와 거리 있음</td></tr>
<tr><td>513</td><td><a href='https://arxiv.org/abs/2608.30782'>PixelIR: Fidelity-Perception Decoupling via Pixel-Space Image-Residual Flow Matching for Efficient One-Step Real-World Super-Resolution</a></td><td>20</td><td>1</td><td>CV</td><td>one-step super-resolution의 fidelity-perception 분리 논문으로 로보틱스와 무관함</td></tr>
<tr><td>514</td><td><a href='https://arxiv.org/abs/2608.31074'>Real-Time Video Anomaly Detection Using YOLO Pose Estimation and CLIP-Based Semantic Scoring</a></td><td>20</td><td>1</td><td>CV</td><td>YOLO pose와 CLIP 유사도로 실시간 이상행동 탐지하는 경량 파이프라인으로 로보틱스 응용은 아님</td></tr>
<tr><td>515</td><td><a href='https://arxiv.org/abs/2608.31096'>One Adapter, Many Tasks: Task-Conditioned Feature Transformations for Continual Learning</a></td><td>20</td><td>1</td><td>CV</td><td>class-incremental learning용 단일 어댑터 feature transformation 방법으로 로보틱스와 거리 있음</td></tr>
<tr><td>516</td><td><a href='https://arxiv.org/abs/2608.29420'>One Capability or Many? Testing the Economic Validity of Frontier AI Evaluation</a></td><td>20</td><td>1</td><td>LG</td><td>프론티어 AI 경제 벤치마크가 별도 능력을 측정하는지 검증한 방법론 연구로 로보틱스와 무관함</td></tr>
<tr><td>517</td><td><a href='https://arxiv.org/abs/2608.29553'>BEACON: Behavioral and Semantic Enrichment of AlphaEarth Embeddings through Tri-Modal Contrastive Learning</a></td><td>20</td><td>1</td><td>Multimodal</td><td>지리공간 foundation model 임베딩에 행동·의미 신호를 대조학습으로 결합한 도시분석 논문으로 로보틱스와 무관함</td></tr>
<tr><td>518</td><td><a href='https://arxiv.org/abs/2608.29579'>Predicting the Unpredictable: LLM-powered Long-term Chaotic Time Series Forecasting under Short-term Observations</a></td><td>20</td><td>1</td><td>LG</td><td>짧은 관측만으로 카오스 시계열을 예측하는 LLM 프레임워크로 로보틱스와 무관함</td></tr>
<tr><td>519</td><td><a href='https://arxiv.org/abs/2608.29640'>LLMODE: Aligning ODEs with LLMs via Gated Token Injection for Irregular Spatio-Temporal Forecasting</a></td><td>20</td><td>1</td><td>LG</td><td>불규칙 시공간 예측에 ODE 인코더와 frozen LLM을 결합한 도시 예측 논문으로 로보틱스와 무관함</td></tr>
<tr><td>520</td><td><a href='https://arxiv.org/abs/2608.29817'>Structure Aware Neural Architecture Search for Mixture of Experts</a></td><td>20</td><td>1</td><td>LG</td><td>MoE 아키텍처 탐색에 클러스터-전문가 정렬을 명시적으로 최적화한 NAS 방법으로 로보틱스와 무관함</td></tr>
<tr><td>521</td><td><a href='https://arxiv.org/abs/2608.29888'>Sensitivity-Constrained Neural Operators for Data-Efficient Forward and Inverse Modeling of Partial Differential Equation Systems</a></td><td>20</td><td>1</td><td>LG</td><td>PDE 신경연산자에 solver의 sensitivity를 추가 지도로 준 방법으로 시뮬레이션 학습에 참고되나 로보틱스 응용 실험은 없음</td></tr>
<tr><td>522</td><td><a href='https://arxiv.org/abs/2608.28980'>The Illusion of Replacement: Rethinking Specialized Machine Learning Models in the Foundation Model Era</a></td><td>20</td><td>1</td><td>LG</td><td>구조 데이터에 특화 아키텍처가 언어모델로 대체 가능한지 159편을 리뷰한 서베이임 - 통찰은 있으나 신규 실험 기여는 아님</td></tr>
<tr><td>523</td><td><a href='https://arxiv.org/abs/2608.29058'>RouteSparse: Input-Conditional Pattern Routing for Budgeted Long-Context Prefilling</a></td><td>20</td><td>1</td><td>LG</td><td>긴 컨텍스트 prefill용 입력조건부 sparse attention 라우팅 기법임 - 효율화 연구로 로봇 문제 적용은 없음</td></tr>
<tr><td>524</td><td><a href='https://arxiv.org/abs/2608.29571'>Which one is banana man? Evaluating vision-language models in multi-turn pragmatic interpretation</a></td><td>20</td><td>1</td><td>Multimodal</td><td>반복 참조게임에서 VLM의 다중턴 화용론적 해석 능력을 평가한 연구임 - 대화맥락 활용 실패를 보여주나 텍스트/이미지 게임 도메인임</td></tr>
<tr><td>525</td><td><a href='https://arxiv.org/abs/2608.29897'>When History Is Multimodal: Rethinking Context Management for Long-Horizon Agents</a></td><td>20</td><td>1</td><td>Multimodal</td><td>장기 에이전트의 히스토리 압축에 시각 렌더링을 컨텍스트 매니저로 쓰는 연구임 - 멀티모달 히스토리 관리 아이디어이나 로봇 관측 상황은 아님</td></tr>
<tr><td>526</td><td><a href='https://arxiv.org/abs/2608.30924'>TRIPPULSE: Multi-Agent Travel Planning with Review-Grounded Reasoning</a></td><td>20</td><td>1</td><td>AI</td><td>리뷰 근거 기반 여행 일정 생성 multi-agent 프레임워크, 전문화 에이전트 조율 구조가 약하게 참고할 만함</td></tr>
<tr><td>527</td><td><a href='https://arxiv.org/abs/2608.28632'>AutoScientist-Quant: Self-Evolving Coding Agents for Automatic Research in Quantitative Investment</a></td><td>20</td><td>1</td><td>AI</td><td>예산 제약 하 알파 탐색을 자기진화 컨트롤러로 통합한 퀀트 투자 연구, 탐색 제어 구조가 약하게 참고할 만함</td></tr>
<tr><td>528</td><td><a href='https://arxiv.org/abs/2608.28642'>From Extraction to Governed Memory: Multi-Agent Knowledge Graph Construction with Domain-Expert Review</a></td><td>20</td><td>1</td><td>AI</td><td>출처·소유권을 명시한 governed 지식그래프 구축 프레임워크, scene graph 구축 방법론과 형식적으로 유사하나 문서 도메인 한정임</td></tr>
<tr><td>529</td><td><a href='https://arxiv.org/abs/2608.29026'>Disentangling Representation using Attributes-based Gaussian Estimation for Medical Sound Diagnosis</a></td><td>20</td><td>1</td><td>AI</td><td>속성 기반 가우시안 추정으로 의료 음향 진단의 disentangled representation을 학습함, 표현학습 우선주제와 약하게 닿음</td></tr>
<tr><td>530</td><td><a href='https://arxiv.org/abs/2608.29913'>On the Instance Hardness as a Decision Criterion in TinyML Systems</a></td><td>20</td><td>1</td><td>LG</td><td>TinyML에서 instance hardness로 pruning 임계값을 조절해 에너지-정확도 균형을 맞추는 초기 단계 연구임</td></tr>
<tr><td>531</td><td><a href='https://arxiv.org/abs/2608.28685'>Data Diversity, Not Frequency Invariance: A Controlled and Self-Audited Study of Compression-Robust Deepfake Detection</a></td><td>20</td><td>0</td><td>CV</td><td>압축 강건 딥페이크 탐지에서 frequency invariance 가설을 재검증한 negative result 연구임. 방법론적으로는 꼼꼼하나 로봇과 무관함</td></tr>
<tr><td>532</td><td><a href='https://arxiv.org/abs/2608.28696'>Instruction Distillation: Text Instructions as Visual Examples</a></td><td>20</td><td>0</td><td>Multimodal</td><td>이미지 예시 대신 텍스트 지시문으로 ICL 토큰 비용을 줄이는 기법임. fine-grained 분류 효율화 위주임</td></tr>
<tr><td>533</td><td><a href='https://arxiv.org/abs/2608.28698'>State-Conditioned Visual Evidence Retrieval for Fine-Grained Perception in Document Vision-Language Models</a></td><td>20</td><td>0</td><td>Multimodal</td><td>문서 파싱에서 상태 조건부로 고해상도 영역을 검색하는 효율화 기법임. 로봇과 무관함</td></tr>
<tr><td>534</td><td><a href='https://arxiv.org/abs/2608.28701'>TopoAgent: A Structure-Aware Perception-to-Reasoning Framework for Diagram-to-Graph Topology Extraction with Large Vision-Language Models</a></td><td>20</td><td>0</td><td>Multimodal</td><td>다이어그램에서 그래프 위상을 추출하는 VLM 에이전트 프레임워크임. 로봇과 무관함</td></tr>
<tr><td>535</td><td><a href='https://arxiv.org/abs/2608.29048'>DReSG: Diffusion Residuals for Stylized Gaussian Splatting</a></td><td>20</td><td>0</td><td>3D Vision</td><td>diffusion residual로 3DGS 스타일화하는 콘텐츠 제작 기법임. 로봇과 무관함</td></tr>
<tr><td>536</td><td><a href='https://arxiv.org/abs/2608.29186'>Multi-Scale Temporal Domain Alignment for Federated Video Domain Adaptation</a></td><td>20</td><td>0</td><td>Video</td><td>연합학습 환경에서 비디오 도메인 적응을 위한 시간 정렬 기법임. 로봇과 무관함</td></tr>
<tr><td>537</td><td><a href='https://arxiv.org/abs/2608.29281'>Elastic Token Compression for Pixel-Space Diffusion Transformers</a></td><td>20</td><td>0</td><td>CV</td><td>픽셀 공간 diffusion transformer의 토큰 압축 효율화임. 로봇 문제에 적용된 바 없는 일반 생성모델 가속 연구임</td></tr>
<tr><td>538</td><td><a href='https://arxiv.org/abs/2608.29958'>RIDGE: Region-Informed Derivative-Guided Evidence Selection for Long Video Understanding</a></td><td>20</td><td>0</td><td>Video</td><td>장기 비디오 이해를 위한 프레임-쿼리 유사도 곡선 기반 프레임 선택 기법임. 로봇과 무관함</td></tr>
<tr><td>539</td><td><a href='https://arxiv.org/abs/2608.29997'>Discrete Diffusion Bridges for Spatiotemporally Aligned Image Translation and Generation</a></td><td>20</td><td>0</td><td>CV</td><td>이산 확산모델의 시공간 정렬 불일치를 해소하는 이미지 변환 프레임워크임. 로봇과 무관함</td></tr>
<tr><td>540</td><td><a href='https://arxiv.org/abs/2608.30209'>DICS: Exploring Data Intrinsic Consistency for Visual Instruction Selection</a></td><td>20</td><td>0</td><td>Multimodal</td><td>시각 지시 데이터의 샘플 내적 일관성 기반 선택 기법임. 로봇과 무관함</td></tr>
<tr><td>541</td><td><a href='https://arxiv.org/abs/2608.30113'>Supraglacial Lake Fate Is Knowable Long Before the Season Ends</a></td><td>20</td><td>0</td><td>LG</td><td>빙하 호수 운명 조기 예측 문제로 로봇/embodied AI와 무관한 응용 분석임.</td></tr>
<tr><td>542</td><td><a href='https://arxiv.org/abs/2608.30367'>Beat-Synchronous Tokenization for ECG Transformers</a></td><td>20</td><td>0</td><td>CV</td><td>심전도 transformer의 tokenization 방식 개선으로 로보틱스와 무관함.</td></tr>
<tr><td>543</td><td><a href='https://arxiv.org/abs/2608.30384'>RSLM: Training-Free Vector Quantization for Approximate Nearest Neighbor Search</a></td><td>20</td><td>0</td><td>LG</td><td>임베딩 압축 기반 근사 최근접 이웃 검색 기법으로 로보틱스와 무관함.</td></tr>
<tr><td>544</td><td><a href='https://arxiv.org/abs/2608.30505'>Tensor Methods for Language Models: From Token Representation to Training, Adaptation, Inference, Compression, and Interpretability</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 텐서 분해 기법 전반을 정리한 서베이로 원저작성 기여가 낮고 로보틱스와 무관함.</td></tr>
<tr><td>545</td><td><a href='https://arxiv.org/abs/2608.30568'>Collapsibility of Performance Metrics in Clinical Predictive AI</a></td><td>20</td><td>0</td><td>LG</td><td>임상 예측 AI에서 성능 지표의 collapsibility 특성을 분석한 통계 이론 연구로 로보틱스와 무관함.</td></tr>
<tr><td>546</td><td><a href='https://arxiv.org/abs/2608.30597'>PLC-DPO: Posterior Label Correction in Noisy and Ambiguous Preference Optimization</a></td><td>20</td><td>0</td><td>NLP</td><td>노이즈 있는 선호 데이터를 온라인으로 교정하는 DPO 변형으로 로보틱스와 무관함.</td></tr>
<tr><td>547</td><td><a href='https://arxiv.org/abs/2608.30699'>Learning Dynamics of Logits Debiasing for Long-Tailed Semi-Supervised Learning</a></td><td>20</td><td>0</td><td>CV</td><td>long-tailed semi-supervised learning의 logit debiasing 기전을 이론적으로 규명한 연구로 로보틱스와 무관함.</td></tr>
<tr><td>548</td><td><a href='https://arxiv.org/abs/2608.30710'>Kolmogorov--Arnold against bounded translations</a></td><td>20</td><td>0</td><td>LG</td><td>Kolmogorov-Arnold 표현의 adversarial translation 강건성을 분석한 이론 논문으로 로보틱스와 무관함.</td></tr>
<tr><td>549</td><td><a href='https://arxiv.org/abs/2608.30877'>Deploying DeepSeek 175B Locally on a Single Consumer-Grade RTX 4060 Laptop with 32GB RAM for 200k-Scale Protein-Ligand Virtual Screening</a></td><td>20</td><td>0</td><td>LG</td><td>소비자용 GPU에서 대형 LLM 가상 스크리닝을 돌린 엔지니어링 실현 가능성 연구로 로보틱스와 무관함.</td></tr>
<tr><td>550</td><td><a href='https://arxiv.org/abs/2608.30910'>S3C-LLM: Skill-Code Guided Agentic Language Models for Spectrum-to-Structure Elucidation</a></td><td>20</td><td>0</td><td>NLP</td><td>스펙트럼 기반 분자 구조 규명을 위한 skill-code 에이전트 LLM으로 로보틱스와 무관함.</td></tr>
<tr><td>551</td><td><a href='https://arxiv.org/abs/2608.30946'>Reproducible macroscopic dynamics in a closed-loop human-AI learning system</a></td><td>20</td><td>0</td><td>LG</td><td>대규모 학습자-AI 상호작용의 거시 동역학을 분석한 연구로 로보틱스와 무관함.</td></tr>
<tr><td>552</td><td><a href='https://arxiv.org/abs/2608.30976'>A Human-in-the-Loop Autonomous Agent for Industry Time Series Forecasting</a></td><td>20</td><td>0</td><td>LG</td><td>전력가격 예측을 위한 human-in-the-loop 에이전트 시스템으로 로보틱스와 무관함.</td></tr>
<tr><td>553</td><td><a href='https://arxiv.org/abs/2608.30986'>Controlling Refusal Behavior of LLMs via Stiefel-Constrained Rotation Steering</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 거부 행동을 Riemannian 회전으로 제어하는 steering 기법으로 로보틱스와 무관함.</td></tr>
<tr><td>554</td><td><a href='https://arxiv.org/abs/2608.31013'>TSPFN: A Temporal Tabular Foundation Model for Physiological Time Series Classification</a></td><td>20</td><td>0</td><td>LG</td><td>TabPFN을 시계열 생리 신호용으로 재설계한 파운데이션 모델로 로보틱스와 무관함.</td></tr>
<tr><td>555</td><td><a href='https://arxiv.org/abs/2608.31079'>Sycophantic Agreement Transfers with Neutral Data via Contrastive Preference Optimization</a></td><td>20</td><td>0</td><td>NLP</td><td>preference optimization이 의도치 않게 아첨 행동을 전이시키는 현상을 분석한 연구로 로보틱스와 무관함.</td></tr>
<tr><td>556</td><td><a href='https://arxiv.org/abs/2608.31108'>Stress-Testing Efficient Responsible-AI Evaluation: When Compute Savings Change Benchmark Conclusions</a></td><td>20</td><td>0</td><td>LG</td><td>효율적 평가 방식이 책임 AI 벤치마크 결론을 바꾸는지 스트레스 테스트한 연구로 로보틱스와 무관함.</td></tr>
<tr><td>557</td><td><a href='https://arxiv.org/abs/2608.31166'>Constant Individual Regret in General Games</a></td><td>20</td><td>0</td><td>RL</td><td>다인 게임에서 개별 후회를 상수로 제한하는 uncoupled 알고리즘 연구로 로보틱스와 무관함.</td></tr>
<tr><td>558</td><td><a href='https://arxiv.org/abs/2608.28643'>Redesigning and Auditing Deep Research Writing for Faithful Reports</a></td><td>20</td><td>0</td><td>NLP</td><td>deep research 보고서의 claim 단위 hallucination 감사·완화 기법임 - 텍스트 생성 신뢰도 문제로 로보틱스와 무관함</td></tr>
<tr><td>559</td><td><a href='https://arxiv.org/abs/2608.29144'>Quantifying Error Tolerance in Synthetic Data: An Atomic-level Operand vs. Operator Perturbation Study</a></td><td>20</td><td>0</td><td>LG</td><td>합성데이터 필터링에서 operand·operator 오류를 구분하는 프레임워크임 - 데이터 큐레이션 연구로 로보틱스와 무관함</td></tr>
<tr><td>560</td><td><a href='https://arxiv.org/abs/2608.29314'>All You Need Is Non-Commutative Words</a></td><td>20</td><td>0</td><td>NLP</td><td>단어를 유니터리 행렬로 표현해 어순을 인코딩하는 대안적 언어모델 아키텍처임 - 참신하나 텍스트분류 벤치마크 수준 검증에 그침</td></tr>
<tr><td>561</td><td><a href='https://arxiv.org/abs/2608.29327'>When to Adapt: Conditional Memory Adapters for Retention-Preserving Domain Specialization</a></td><td>20</td><td>0</td><td>LG</td><td>도메인 특화 시 선택적으로만 활성화되는 조건부 메모리 어댑터임 - 파라미터효율 파인튜닝 연구로 로보틱스와 무관함</td></tr>
<tr><td>562</td><td><a href='https://arxiv.org/abs/2608.29431'>Evaluating the Semantic Specificity of Representation Steering in Language Models</a></td><td>20</td><td>0</td><td>LG</td><td>표현 스티어링이 실제 추론 회로 수정인지 표면적 라벨 편향인지 감사한 진단 프레임워크임 - 해석가능성 방법론 연구로 로보틱스와 무관함</td></tr>
<tr><td>563</td><td><a href='https://arxiv.org/abs/2608.29702'>A Hub of Short Rows Inflates Intrinsic Dimension Estimation of Token Embeddings</a></td><td>20</td><td>0</td><td>LG</td><td>토큰 임베딩의 허브가 내재차원 추정을 왜곡한다는 분석 연구임 - 표현학습 진단이나 로봇 응용 없음</td></tr>
<tr><td>564</td><td><a href='https://arxiv.org/abs/2608.29841'>SkillForge: Compositional Skill Synthesis with Verification-in-the-Loop for Generating Formally Verified Dafny Programs</a></td><td>20</td><td>0</td><td>NLP</td><td>형식검증 프로그램 합성을 atomic skill 라이브러리로 분해한 프레임워크임 - &#x27;스킬&#x27; 용어만 유사할 뿐 로봇 스킬체이닝과는 무관한 정형검증 도메인임</td></tr>
<tr><td>565</td><td><a href='https://arxiv.org/abs/2608.29956'>Detecting Hidden Chain-of-Thought in Large Language Models with Linguistic, Behavioral, and Mechanistic Indicators</a></td><td>20</td><td>0</td><td>LG</td><td>명시적 CoT 없이도 잠재적 추론이 있는지 언어·행동·메커니즘 지표로 탐지한 연구임 - 해석가능성 연구로 로봇 응용 없음</td></tr>
<tr><td>566</td><td><a href='https://arxiv.org/abs/2608.30216'>Label Semantic Expansion via Label Guided Neural Topic Modeling</a></td><td>20</td><td>0</td><td>NLP</td><td>라벨 유도 토픽 모델링, 텍스트 분석 도구 개선 수준임</td></tr>
<tr><td>567</td><td><a href='https://arxiv.org/abs/2608.30426'>Learning to Reason and Use Tools through Unsupervised Fine-Tuning in Task-Oriented Dialog Systems</a></td><td>20</td><td>0</td><td>NLP</td><td>ReAct 기반 task-oriented dialog의 비지도 fine-tuning 파이프라인임</td></tr>
<tr><td>568</td><td><a href='https://arxiv.org/abs/2608.31066'>Every Token Leaves a Ripple in the Stream of Thought: Eliciting Model-Internal Token Saliency for Chain-of-Thought Compression</a></td><td>20</td><td>0</td><td>NLP</td><td>모델 내부 saliency로 CoT를 압축하는 기법, 토큰 선택 개선 연구임</td></tr>
<tr><td>569</td><td><a href='https://arxiv.org/abs/2608.28662'>FRAC-MAS: A Safe and Explainable Multi-Agent System for Fracture Diagnosis</a></td><td>20</td><td>0</td><td>AI</td><td>골절 진단용 conformal prediction 기반 multi-agent 시스템, 의료 영상 특화 연구임</td></tr>
<tr><td>570</td><td><a href='https://arxiv.org/abs/2608.28833'>Evaluating the Hidden Costs of Personalization in Large Language Models</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 개인화가 초래하는 sycophancy 등 부작용을 측정한 평가 프레임워크임</td></tr>
<tr><td>571</td><td><a href='https://arxiv.org/abs/2608.28990'>Agentic AI uncovers conserved cross-tissue protein co-abundance programs inaccessible to single-dataset analysis</a></td><td>20</td><td>0</td><td>AI</td><td>LLM 에이전트로 조직 간 단백질 공존재 네트워크를 발견한 생물학 응용 연구임</td></tr>
<tr><td>572</td><td><a href='https://arxiv.org/abs/2608.29311'>Formal Concept Analysis with Three Types of Negation</a></td><td>20</td><td>0</td><td>LG</td><td>형식개념분석에 세 가지 부정 개념을 도입한 논리학 이론 연구임, 응용 사례가 제한적임</td></tr>
<tr><td>573</td><td><a href='https://arxiv.org/abs/2608.30543'>Designing an Auditable LLM-Supported Workflow for Qualitative Thematic Analysis</a></td><td>20</td><td>0</td><td>NLP</td><td>질적 주제분석을 LLM으로 감사 가능하게 수행하는 워크플로 설계 연구임</td></tr>
<tr><td>574</td><td><a href='https://arxiv.org/abs/2608.31097'>Cross-Regional Grapevine Cold Hardiness Prediction via Learned Multimodal Latent Representations</a></td><td>20</td><td>0</td><td>LG</td><td>포도나무 내한성 예측을 지역 간 전이 가능한 잠재표현으로 개선한 농업 응용 연구임</td></tr>
<tr><td>575</td><td><a href='https://arxiv.org/abs/2608.31137'>OntoAligner-Ensemble: Voting-Based Fusion across Heterogeneous Ontology Alignment Techniques</a></td><td>20</td><td>0</td><td>NLP</td><td>이질적 온톨로지 정렬 기법들을 투표 기반으로 앙상블하는 프레임워크임, 조합형 엔지니어링 연구임</td></tr>
<tr><td>576</td><td><a href='https://arxiv.org/abs/2608.30297'>AIA$^{2}$: Attribute-Agnostic Imbalance Augmentation for Subgroup Robustness</a></td><td>19</td><td>0</td><td>NLP</td><td>속성 불균형 대응 augmentation 프레임워크, incremental engineering 성격임</td></tr>
<tr><td>577</td><td><a href='https://arxiv.org/abs/2608.30393'>Quantitative Evidence Mining for Plausibility-Aware Biomedical AI</a></td><td>19</td><td>0</td><td>NLP</td><td>생의학 정량 증거 마이닝을 위한 perspective 논문, 실험적 증거 약함</td></tr>
<tr><td>578</td><td><a href='https://arxiv.org/abs/2608.30399'>SemPOI-RL: Aligning LLM Semantic Reasoning for Interpretable Out-of-Town POI Sequential Generation</a></td><td>19</td><td>0</td><td>RL</td><td>관광지 추천 시퀀스 생성용 RL 정렬 기법, 추천시스템 특화임</td></tr>
<tr><td>579</td><td><a href='https://arxiv.org/abs/2608.30649'>Where Identity Lives: Localized, Retain-Free Identity Unlearning in Multimodal Large Language Models</a></td><td>19</td><td>0</td><td>Multimodal</td><td>MLLM에서 retain set 없이 개인 정체성 정보만 국소적으로 지우는 unlearning 기법임</td></tr>
<tr><td>580</td><td><a href='https://arxiv.org/abs/2608.30678'>OCR-MetaReasoning Benchmark: Evaluating the Meta-Reasoning Ability of MLLMs in Text-Rich Image Understanding</a></td><td>19</td><td>0</td><td>Multimodal</td><td>OCR 텍스트 이해에서 연역·귀납·귀추 추론을 구분 평가하는 벤치마크임</td></tr>
<tr><td>581</td><td><a href='https://arxiv.org/abs/2608.30738'>Not All Fallbacks Are Failures: Understanding and Recovering from Fallbacks in Mobile Voice Assistants</a></td><td>19</td><td>0</td><td>NLP</td><td>음성 비서 fallback 상황 분류 및 복구 사례 연구, 서비스 배포 데이터 기반 연구임</td></tr>
<tr><td>582</td><td><a href='https://arxiv.org/abs/2608.30811'>TopoCompress: Long Context Compression via Graph-Wired Semantic Trajectories</a></td><td>19</td><td>0</td><td>NLP</td><td>그래프 기반 long-context 압축 기법, 학습 없이 동작하는 실용적 개선임</td></tr>
<tr><td>583</td><td><a href='https://arxiv.org/abs/2608.31084'>The First Token Is a Clue: Verbalizing Multi-Token Concepts from the J-lens</a></td><td>19</td><td>0</td><td>NLP</td><td>J-lens로 multi-token 개념을 복원하는 interpretability 기법임</td></tr>
<tr><td>584</td><td><a href='https://arxiv.org/abs/2608.28590'>DS-Lighting: Making Agent Harnesses Explicit for Data-Science Automation</a></td><td>19</td><td>0</td><td>AI</td><td>데이터사이언스 자동화 에이전트의 harness를 명시적으로 계층화한 툴킷임</td></tr>
<tr><td>585</td><td><a href='https://arxiv.org/abs/2608.28594'>From Question-First to Analyst-First: Domain-Expert Skills and Verified Knowledge Compilation for Proactive Enterprise Analytics</a></td><td>19</td><td>0</td><td>AI</td><td>질문 우선에서 분석가 우선으로 전환하는 기업 분석 스킬 시스템, 아키텍처 제안 위주 논문임</td></tr>
<tr><td>586</td><td><a href='https://arxiv.org/abs/2608.28612'>InternReviewer &amp; InternAdvocate: Objective Reward and Evaluation for Agentic Reinforcement Learning in Peer Review and Rebuttal</a></td><td>19</td><td>0</td><td>AI</td><td>논문 심사·반박 생성 전용 에이전트의 RL 학습 프레임워크임</td></tr>
<tr><td>587</td><td><a href='https://arxiv.org/abs/2608.28726'>Pro-Router: Token-Aware Progressive Model Routing with Adaptive Edge-Cloud Collaboration for Efficient Multimodal LLM Inference</a></td><td>19</td><td>0</td><td>AI</td><td>토큰 단위 신뢰도로 edge-cloud 모델 라우팅을 결정하는 효율화 기법임</td></tr>
<tr><td>588</td><td><a href='https://arxiv.org/abs/2608.29249'>Validating FKG.in: Soundness Assessment in LLM-Augmented Indian Food Knowledge</a></td><td>19</td><td>0</td><td>NLP</td><td>인도 음식 지식그래프의 LLM 생성 데이터를 검증하는 파이프라인임, 도메인이 매우 좁음</td></tr>
<tr><td>589</td><td><a href='https://arxiv.org/abs/2608.28958'>CoVA-SFT: A Large-Scale Dataset for Chain of Visual Abstractions</a></td><td>18</td><td>1</td><td>Multimodal</td><td>텍스트 추론에 시각적 중간표현을 끼워넣는 CoT 데이터셋임 - 멀티모달 추론 보조 자원으로 로봇과는 거리 있음</td></tr>
<tr><td>590</td><td><a href='https://arxiv.org/abs/2608.28670'>Memory-Efficient Training-Free Acceleration of Diffusion Transformers with BaryCache</a></td><td>18</td><td>0</td><td>CV</td><td>diffusion transformer 샘플링 가속을 위한 barycentric extrapolation 캐시 기법임. 로봇과 무관한 효율화 연구임</td></tr>
<tr><td>591</td><td><a href='https://arxiv.org/abs/2608.28699'>Beyond Visual Boundaries: Rethinking Scene Segmentation for Movie RAG</a></td><td>18</td><td>0</td><td>Video</td><td>영화 이해용 RAG를 위한 서사 중심 장면 분할 데이터셋임. 로봇과 무관함</td></tr>
<tr><td>592</td><td><a href='https://arxiv.org/abs/2608.30410'>SePArate: Segmenting Patterns from Defects in Wafer Manufacturing Using Weak Supervision</a></td><td>18</td><td>0</td><td>CV</td><td>웨이퍼 결함 약지도 분할로 로보틱스와 무관한 산업 응용임</td></tr>
<tr><td>593</td><td><a href='https://arxiv.org/abs/2608.30420'>Whole-Slide Image Analysis under Realistic Few-Shot Annotation Protocols</a></td><td>18</td><td>0</td><td>CV</td><td>병리 슬라이드 few-shot transduction 분석으로 로보틱스와 무관함</td></tr>
<tr><td>594</td><td><a href='https://arxiv.org/abs/2608.30450'>FlowVVTON: Flow-Guided Mask-Free Video Virtual Try-On</a></td><td>18</td><td>0</td><td>CV</td><td>비디오 가상 착의 생성 논문으로 로보틱스와 무관함</td></tr>
<tr><td>595</td><td><a href='https://arxiv.org/abs/2608.30510'>Lot Machine: Multimodal Lot Extraction from Auction Catalogs</a></td><td>18</td><td>0</td><td>Multimodal</td><td>경매 카탈로그에서 VLM으로 메타데이터 추출하는 디지털 인문학 응용으로 로보틱스와 무관함</td></tr>
<tr><td>596</td><td><a href='https://arxiv.org/abs/2608.30633'>Quantum-Grassmann-Plucker Token Mixing for Deep Learning-Based Post-Disaster Damage Assessment</a></td><td>18</td><td>0</td><td>CV</td><td>위성영상 재해 피해평가에 quantum-inspired token mixing 적용한 논문으로 로보틱스와 무관함</td></tr>
<tr><td>597</td><td><a href='https://arxiv.org/abs/2608.30656'>APT: Anchor-aligned Perturbations for Tamper Localization in Fully Regenerated Images</a></td><td>18</td><td>0</td><td>CV</td><td>이미지 위변조 국소화 포렌식 논문으로 로보틱스와 무관함</td></tr>
<tr><td>598</td><td><a href='https://arxiv.org/abs/2608.30689'>CANVAS: Consistency-Aware Navigation via Visual Adaptive Sampling for Long-Context Text-to-SVG Generation</a></td><td>18</td><td>0</td><td>CV</td><td>텍스트-SVG 생성 일관성 개선 논문으로 로보틱스와 무관함</td></tr>
<tr><td>599</td><td><a href='https://arxiv.org/abs/2608.30714'>SegWave: Wavelet-Driven Segmentation of Tampered Regions</a></td><td>18</td><td>0</td><td>CV</td><td>웨이블릿 기반 위변조 영역 분할 논문으로 로보틱스와 무관함</td></tr>
<tr><td>600</td><td><a href='https://arxiv.org/abs/2608.30762'>ChessQueries: Toward Better Chess Board Recognition</a></td><td>18</td><td>0</td><td>CV</td><td>체스판 인식 정확도를 크게 높인 논문이나 로보틱스와 무관함</td></tr>
<tr><td>601</td><td><a href='https://arxiv.org/abs/2608.30835'>Reliable Benchmarking of Artifact Detection in Computational Pathology: A Reproducibility and Uncertainty Analysis</a></td><td>18</td><td>0</td><td>CV</td><td>병리 아티팩트 탐지 벤치마크 재현성 검증 논문으로 로보틱스와 무관함</td></tr>
<tr><td>602</td><td><a href='https://arxiv.org/abs/2608.30844'>Pretrained, Curriculum-Tuned, and Ensembled: A Tracer-Aware Interactive Segmentation Pipeline for AutoPET V</a></td><td>18</td><td>0</td><td>CV</td><td>PET/CT 병변 interactive segmentation 파이프라인으로 로보틱스와 무관함</td></tr>
<tr><td>603</td><td><a href='https://arxiv.org/abs/2608.31033'>FaceSnap: Real-Time Personalized Lightstage Facial Performance Capture</a></td><td>18</td><td>0</td><td>CV</td><td>단일 카메라 실시간 lightstage 얼굴 캡처 논문으로 로보틱스와 무관함</td></tr>
<tr><td>604</td><td><a href='https://arxiv.org/abs/2608.31107'>VeriCam: A Verification Baseline for the Classification of Unknown Data</a></td><td>18</td><td>0</td><td>CV</td><td>번호판 인식 verification 기반 미지 클래스 분류 파이프라인으로 로보틱스와 무관함</td></tr>
<tr><td>605</td><td><a href='https://arxiv.org/abs/2608.28843'>Curvature Cryptanalysis of Smooth Transformer Feed-Forward Networks</a></td><td>18</td><td>0</td><td>LG</td><td>transformer FFN의 곡률을 이용한 모델 추출 공격 분석으로 로보틱스와 무관함</td></tr>
<tr><td>606</td><td><a href='https://arxiv.org/abs/2608.28910'>Learning-Theoretic Foundation for General Coded Computing: The Straggler Setting</a></td><td>18</td><td>0</td><td>LG</td><td>straggler 상황의 coded computing을 학습이론으로 재정식화한 논문으로 로보틱스와 무관함</td></tr>
<tr><td>607</td><td><a href='https://arxiv.org/abs/2608.28934'>Revisiting the Provable-Auditable Privacy Gap of DP-SGD</a></td><td>18</td><td>0</td><td>LG</td><td>DP-SGD의 이론-실증 프라이버시 격차를 줄이는 경량 방어 프레임워크로 로보틱스와 무관함</td></tr>
<tr><td>608</td><td><a href='https://arxiv.org/abs/2608.29096'>Development of an Autonomous AI Coding Agent using Monte Carlo Tree Search (MCTS) and Gemini LLM Frameworks</a></td><td>18</td><td>0</td><td>LG</td><td>MCTS와 Gemini로 코드 생성을 탐색문제화한 에이전트로 로보틱스와 무관함</td></tr>
<tr><td>609</td><td><a href='https://arxiv.org/abs/2608.29099'>Temperature-Adaptive Transformed Teacher Matching</a></td><td>18</td><td>0</td><td>CV</td><td>distillation temperature를 샘플별로 조정하는 지식증류 개선으로 로보틱스와 무관함</td></tr>
<tr><td>610</td><td><a href='https://arxiv.org/abs/2608.29247'>RL-FAT: Reinforcement Learning for Fair Adversarial Training</a></td><td>18</td><td>0</td><td>CV</td><td>클래스별 강건성 불균형을 줄이는 공정 적대적학습으로 로보틱스와 무관함</td></tr>
<tr><td>611</td><td><a href='https://arxiv.org/abs/2608.29503'>Adversarial Online Classification with a Preview</a></td><td>18</td><td>0</td><td>LG</td><td>온라인 분류에 preview 모델을 도입한 학습이론으로 로보틱스와 무관함</td></tr>
<tr><td>612</td><td><a href='https://arxiv.org/abs/2608.29560'>Which LLM for Which Work? Budgeted Model Allocation under Uncertain Evaluation</a></td><td>18</td><td>0</td><td>LG</td><td>예산 제약 하 LLM-작업 배정을 평가 불확실성과 함께 다룬 의사결정 이론으로 로보틱스와 무관함</td></tr>
<tr><td>613</td><td><a href='https://arxiv.org/abs/2608.29600'>Adaptive Doubly Robust Off-Policy Evaluation for Ranking Policies under Diverse User Behavior</a></td><td>18</td><td>0</td><td>LG</td><td>순위 정책 off-policy evaluation에 doubly robust 보정을 결합한 추천시스템 방법으로 로보틱스와 무관함</td></tr>
<tr><td>614</td><td><a href='https://arxiv.org/abs/2608.29667'>A Target-Centric Survey of Quantization-Aware Training</a></td><td>18</td><td>0</td><td>NLP</td><td>Quantization-Aware Training을 target별로 정리한 서베이로 로보틱스와 무관함</td></tr>
<tr><td>615</td><td><a href='https://arxiv.org/abs/2608.29886'>Structural Hierarchy and Geometry in Molecular Representation Learning</a></td><td>18</td><td>0</td><td>LG</td><td>분자의 scaffold 구조를 지도로 준 표현학습 분석으로 로보틱스와 무관함</td></tr>
<tr><td>616</td><td><a href='https://arxiv.org/abs/2608.29892'>Joint Spatiotemporal Spectral Neural Operators for Learning PDEs on Irregular Domains</a></td><td>18</td><td>0</td><td>LG</td><td>그래프 스펙트럴과 시간 푸리에를 결합한 비정형 도메인 PDE 신경연산자로 로보틱스와 무관함</td></tr>
<tr><td>617</td><td><a href='https://arxiv.org/abs/2608.29907'>Diffusion-Based Inverse Design of Dielectric Resonator Metasurfaces for Shaping Smart Electromagnetic Environments</a></td><td>18</td><td>0</td><td>LG</td><td>메타표면 역설계용 조건부 확산모델로 로보틱스와 무관함</td></tr>
<tr><td>618</td><td><a href='https://arxiv.org/abs/2608.29943'>On the Recoverability of Private Information Unlearning in Large Language Models</a></td><td>18</td><td>0</td><td>NLP</td><td>LLM machine unlearning이 실제로는 정보를 숨기기만 한다는 걸 inverse greedy decoding으로 보인 감사 연구로 로보틱스와 무관함</td></tr>
<tr><td>619</td><td><a href='https://arxiv.org/abs/2608.30028'>Multiclass Linear Perceptrons with Multiplicative Margins</a></td><td>18</td><td>0</td><td>LG</td><td>곱셈적 마진을 쓰는 다중클래스 퍼셉트론 이론으로 로보틱스와 무관함</td></tr>
<tr><td>620</td><td><a href='https://arxiv.org/abs/2608.30046'>Forget or Fine-tune? A Comparative Study of Machine Unlearning Strategies for Noisy Label Correction</a></td><td>18</td><td>0</td><td>LG</td><td>노이즈 라벨 교정에 machine unlearning과 fine-tuning을 비교한 실험연구로 로보틱스와 무관함</td></tr>
<tr><td>621</td><td><a href='https://arxiv.org/abs/2608.30564'>Q-Strata: Hierarchical Bit Allocation for Mixed-Precision Quantization of Mixture-of-Experts LLMs</a></td><td>18</td><td>0</td><td>LG</td><td>MoE LLM의 mixed-precision 양자화 할당 최적화로 로보틱스와 무관함.</td></tr>
<tr><td>622</td><td><a href='https://arxiv.org/abs/2608.30741'>Functional Degeneracy in Neural Networks: Measurement and Pruning</a></td><td>18</td><td>0</td><td>LG</td><td>behavioral Hessian 기반 압축 가능성 측정 연구로 경량화 방향이라 랩 기준상 낮게 평가함.</td></tr>
<tr><td>623</td><td><a href='https://arxiv.org/abs/2608.30908'>Fine-Tuning Low-Bit Models with Gradient in Quantized Code Space</a></td><td>18</td><td>0</td><td>LG</td><td>저비트 모델 fine-tuning을 위한 gradient surrogate 기법으로 로보틱스와 무관함.</td></tr>
<tr><td>624</td><td><a href='https://arxiv.org/abs/2608.30963'>A Universal Context-Reuse Layer for Cross-Model KV Sharing</a></td><td>18</td><td>0</td><td>NLP</td><td>서로 다른 LLM 간 KV 캐시를 공유하는 시스템 연구로 로보틱스와 무관함.</td></tr>
<tr><td>625</td><td><a href='https://arxiv.org/abs/2608.31120'>On the Complexity of the Compatibility Problem for Succinctly Encoded Conditional Distributions</a></td><td>18</td><td>0</td><td>LG</td><td>succinct 조건부 분포의 compatibility 문제 복잡도를 규명한 이론 연구로 로보틱스와 무관함.</td></tr>
<tr><td>626</td><td><a href='https://arxiv.org/abs/2608.28846'>A rigor-matched audit of periodic-step layer skipping for efficient llm inference: conflayers versus swift, with a supplemental analysis of trained routing alternatives</a></td><td>18</td><td>0</td><td>LG</td><td>주기적 레이어 스킵 추론 가속 기법들의 엄밀 재감사임 - 효율화 방법론이나 로봇 문제에 새 원리 제공은 없음</td></tr>
<tr><td>627</td><td><a href='https://arxiv.org/abs/2608.29215'>Attribute-Based Activation Steering of LLMs for Group-Specific Explanation Generation</a></td><td>18</td><td>0</td><td>LG</td><td>그룹별 맞춤 설명 생성을 위한 속성기반 활성화 스티어링임 - 로보틱스와 무관함</td></tr>
<tr><td>628</td><td><a href='https://arxiv.org/abs/2608.29270'>SHADOWBENCH: Toward Reliable Automatic Evaluation of Semantic Alignment in Autoformalization</a></td><td>18</td><td>0</td><td>LG</td><td>Lean 형식화 진술의 의미정합성 평가 지표(SA-Pass)임 - 수학 증명 도메인으로 로보틱스와 무관함</td></tr>
<tr><td>629</td><td><a href='https://arxiv.org/abs/2608.29455'>Item-Mean Surrogates: Why Richer Persona Data Fail to Improve LLMs as Human Surrogates</a></td><td>18</td><td>0</td><td>NLP</td><td>LLM이 개인별 응답 편차를 대체 못하고 항목평균만 근사한다는 실증 연구임 - 서베이 응용으로 로보틱스와 무관함</td></tr>
<tr><td>630</td><td><a href='https://arxiv.org/abs/2608.29539'>LoGo: Token-Level Dynamic Local-Global Attention</a></td><td>18</td><td>0</td><td>LG</td><td>토큰별 동적 local-global attention으로 긴 컨텍스트 효율을 높인 아키텍처임 - 순수 언어모델 효율화로 로보틱스와 무관함</td></tr>
<tr><td>631</td><td><a href='https://arxiv.org/abs/2608.29610'>Beyond Surface Alignment: Grounding the Dynamics of Situational Understanding and Generative Control in LLMs</a></td><td>18</td><td>0</td><td>NLP</td><td>상황적 그라운딩과 생성적 제어를 다루는 박사논문 요약임 - 여러 서브연구 나열이라 로보틱스 연관성 낮음</td></tr>
<tr><td>632</td><td><a href='https://arxiv.org/abs/2608.29934'>Compression-Aware Abstention: Teaching LLMs to Refuse When KV-Compression Masks Remove Answer Evidence</a></td><td>18</td><td>0</td><td>LG</td><td>KV캐시 압축으로 증거가 사라지면 답변을 거부하도록 학습시킨 어댑터임 - 실패인지 관점은 흥미로우나 텍스트 QA 한정임</td></tr>
<tr><td>633</td><td><a href='https://arxiv.org/abs/2608.30109'>COGTRL: Training LLMs for Scientific Discovery Assistance using Cognitive Traces via Reinforcement Learning</a></td><td>18</td><td>0</td><td>LG</td><td>과학적 발견 보조를 위해 인지적 흔적을 강화학습으로 학습시킨 연구임 - AI 과학보조 응용으로 로보틱스와 무관함</td></tr>
<tr><td>634</td><td><a href='https://arxiv.org/abs/2608.30198'>When Errors Become Memories: Causal Pathway Tracing in Multi-Turn Memory-Augmented LLMs</a></td><td>18</td><td>0</td><td>LG</td><td>메모리 증강 LLM에서 오류가 인과적으로 전파되는 경로를 SCM으로 분석한 연구임 - robot memory 실패전파와 개념적으로 유사하나 텍스트 대화 시스템 한정임</td></tr>
<tr><td>635</td><td><a href='https://arxiv.org/abs/2608.30614'>TaxCE : A Framework for Automated Taxonomy Construction and Evaluation at Scale</a></td><td>18</td><td>0</td><td>NLP</td><td>대규모 피드백 텍스트의 자동 분류체계 구축 프레임워크, 산업 응용 연구임</td></tr>
<tr><td>636</td><td><a href='https://arxiv.org/abs/2608.30662'>MURANO: Design, Run, and Reproduce Mechanistic Interpretability Experiments as Composable Pipelines</a></td><td>18</td><td>0</td><td>NLP</td><td>mechanistic interpretability 실험을 위한 조합 가능한 파이프라인 툴킷임</td></tr>
<tr><td>637</td><td><a href='https://arxiv.org/abs/2608.31016'>LLM Judges Verify Presence, Not Absence: Omission Blindness in AI Clinical Notes and What Recovers It</a></td><td>18</td><td>0</td><td>NLP</td><td>AI 임상노트에서 LLM judge의 누락 오류 탐지 실패를 규명한 연구임</td></tr>
<tr><td>638</td><td><a href='https://arxiv.org/abs/2608.31058'>Improving Information Extraction with Learned Queries</a></td><td>18</td><td>0</td><td>NLP</td><td>질의 설계 자체를 학습 대상으로 삼아 정보 추출 성능을 높인 연구임</td></tr>
<tr><td>639</td><td><a href='https://arxiv.org/abs/2608.28593'>Statutory AI: Aligning Large Language Models With Legal Norms</a></td><td>18</td><td>0</td><td>NLP</td><td>법률 텍스트를 헌법처럼 사용하는 LLM alignment 기법임</td></tr>
<tr><td>640</td><td><a href='https://arxiv.org/abs/2608.28631'>CrossAudit: A Git-Native, Cross-Vendor Audit Loop for Agentic Science</a></td><td>18</td><td>0</td><td>AI</td><td>다른 벤더 모델이 서로 감사하는 git 기반 agentic science 감독 프로토콜임</td></tr>
<tr><td>641</td><td><a href='https://arxiv.org/abs/2608.29973'>An Open-Source, Event-Driven Pipeline for Cryptocurrency Market Data: Ingestion, Forecasting, and On-Chain Fraud Detection</a></td><td>18</td><td>0</td><td>LG</td><td>오픈소스 이벤트 기반 암호화폐 데이터 파이프라인 구축과 기본 예측 모델 비교임, 연구 novelty는 낮음</td></tr>
<tr><td>642</td><td><a href='https://arxiv.org/abs/2608.30652'>PyKEEN-NSX: A Modular Framework for Static, Dynamic and Schema-Aware Negative Sampling in PyKEEN</a></td><td>18</td><td>0</td><td>LG</td><td>지식그래프 임베딩용 negative sampling을 모듈화한 라이브러리 확장 연구임</td></tr>
<tr><td>643</td><td><a href='https://arxiv.org/abs/2608.30757'>Which Rules Matter Now? Policy-Centroid Routing Before an Intelligent System Acts</a></td><td>18</td><td>0</td><td>NLP</td><td>행동 전 적용 규칙을 선별하는 policy-centroid routing 개념을 제안한 이론 논문임, 실증 결과가 없음</td></tr>
<tr><td>644</td><td><a href='https://arxiv.org/abs/2608.28652'>A Generalized Optimization Engine (GOE) for Edge AI Inference Acceleration</a></td><td>17</td><td>1</td><td>AI</td><td>엣지 배포용 범용 모델 압축 최적화 엔진, 경량화 위주라 우선순위 낮음</td></tr>
<tr><td>645</td><td><a href='https://arxiv.org/abs/2608.30327'>Do Small Models Use the Law You Give Them? Measuring Context Use on a Bilingual Bangladesh Legal Benchmark</a></td><td>17</td><td>0</td><td>NLP</td><td>방글라데시 법률 QA에서 context 활용도 측정, 도메인 특화 벤치마크임</td></tr>
<tr><td>646</td><td><a href='https://arxiv.org/abs/2608.30475'>ImageEval 2026: Culturally Grounded Arabic Multimodal Evaluation</a></td><td>17</td><td>0</td><td>Multimodal</td><td>아랍어 문화 기반 멀티모달 평가 shared task 리포트임</td></tr>
<tr><td>647</td><td><a href='https://arxiv.org/abs/2608.30541'>Seeing the Unseen: Visual Similarity for Pixel Language Model Adaptation</a></td><td>17</td><td>0</td><td>NLP</td><td>픽셀 기반 언어모델의 티베트어 적응 사례 연구임</td></tr>
<tr><td>648</td><td><a href='https://arxiv.org/abs/2608.30683'>WildSEEK: Evaluating Language Models for Information-Seeking</a></td><td>17</td><td>0</td><td>NLP</td><td>실사용 정보탐색 질의에서 LLM 응답의 위험성을 분석한 벤치마크임</td></tr>
<tr><td>649</td><td><a href='https://arxiv.org/abs/2608.30893'>ECGQuest: Benchmarking and Fine-Tuning Language Models for Electrocardiography</a></td><td>17</td><td>0</td><td>NLP</td><td>심전도 해석 전용 벤치마크와 fine-tuning 연구임</td></tr>
<tr><td>650</td><td><a href='https://arxiv.org/abs/2608.31014'>Evidence-Bounded Mental Health Reasoning from Heterogeneous Speech Protocols</a></td><td>17</td><td>0</td><td>NLP</td><td>이질적 음성 프로토콜에서 근거 경계를 지키는 정신건강 스크리닝 연구임</td></tr>
<tr><td>651</td><td><a href='https://arxiv.org/abs/2608.31017'>One note in three: a verified census of three deployed AI scribes, and the instrument that counted it</a></td><td>17</td><td>0</td><td>NLP</td><td>상용 AI 스크라이브 3종의 오류율을 검증한 인구조사식 감사 연구임</td></tr>
<tr><td>652</td><td><a href='https://arxiv.org/abs/2608.31128'>DIASENTINEL: An Auditable Multi-Agent System for Guideline-Grounded Diabetes Risk Screening</a></td><td>17</td><td>0</td><td>NLP</td><td>당뇨 위험 스크리닝을 위한 가이드라인 근거 multi-agent 시스템임</td></tr>
<tr><td>653</td><td><a href='https://arxiv.org/abs/2608.28596'>Paper Pilot: A Human-in-the-Loop Expert System for Evidence-Traceable Scientific Manuscript Generation in Applied Sciences</a></td><td>17</td><td>0</td><td>AI</td><td>근거 추적 가능한 논문 초안 생성을 위한 human-in-the-loop 승인 게이트 시스템임</td></tr>
<tr><td>654</td><td><a href='https://arxiv.org/abs/2608.28597'>The Race between Agentic AI Capabilities and Data Quality Control in Online Surveys</a></td><td>17</td><td>0</td><td>AI</td><td>에이전틱 AI가 설문 주의 확인 문항을 통과하는 취약점과 방어책 연구임</td></tr>
<tr><td>655</td><td><a href='https://arxiv.org/abs/2608.28605'>MedTVL: Harnessing Vision and Language for Medical Time Series Classification</a></td><td>17</td><td>0</td><td>Multimodal</td><td>의료 시계열 분류를 위한 시각-언어 dual-pathway 아키텍처임</td></tr>
<tr><td>656</td><td><a href='https://arxiv.org/abs/2608.28610'>TPvG: A Moral Decision Framework for Large Language Models from One-Shot to Sequential Feedback</a></td><td>17</td><td>0</td><td>AI</td><td>결과 피드백이 있는 순차적 도덕 딜레마에서 LLM 행동을 평가한 프레임워크임</td></tr>
<tr><td>657</td><td><a href='https://arxiv.org/abs/2608.28809'>Capability-Stratified Degradation in Ternary Language Models</a></td><td>17</td><td>0</td><td>LG</td><td>삼진법 양자화 언어모델의 능력별 성능 저하를 분석한 연구, 경량화 방향이라 우선순위 낮음</td></tr>
<tr><td>658</td><td><a href='https://arxiv.org/abs/2608.30371'>MCSeg: Pre-training and Fine-tuning Volumetric Pyramid Transformer for Multi-modal Cardiac Image Segmentation</a></td><td>16</td><td>0</td><td>CV</td><td>심장 영상 분할 의료 논문으로 로보틱스 관련성 없음</td></tr>
<tr><td>659</td><td><a href='https://arxiv.org/abs/2608.30537'>Minerals in the Wild: A Hyperspectral-XRF Dataset for Elemental Composition Estimation</a></td><td>16</td><td>0</td><td>CV</td><td>암석 하이퍼스펙트럴-XRF 원소분석 데이터셋 공개로 로보틱스와 무관함</td></tr>
<tr><td>660</td><td><a href='https://arxiv.org/abs/2608.30789'>Camera trap classification with deep learning under ground truth uncertainty</a></td><td>16</td><td>0</td><td>CV</td><td>카메라트랩 종 분류에서 라벨 불확실성 학습 효과 분석한 생태 응용 논문으로 로보틱스와 무관함</td></tr>
<tr><td>661</td><td><a href='https://arxiv.org/abs/2608.30895'>A Controlled Evaluation of Model Rankings and Input Reliance in Surface Water Segmentation</a></td><td>16</td><td>0</td><td>CV</td><td>지표수 분할 모델 순위의 안정성과 입력 의존성을 점검한 방법론 논문으로 로보틱스와 무관함</td></tr>
<tr><td>662</td><td><a href='https://arxiv.org/abs/2608.31053'>Identity-Conditioned Latent Consistency Distillation for Face Synthesis</a></td><td>16</td><td>0</td><td>CV</td><td>얼굴인식용 합성 얼굴 생성 속도를 distillation으로 높인 논문으로 로보틱스와 무관함</td></tr>
<tr><td>663</td><td><a href='https://arxiv.org/abs/2608.31073'>LISynSeg: Data-Centric Label-to-Image Synthesis for Cross-Modality Whole-Heart Segmentation</a></td><td>16</td><td>0</td><td>CV</td><td>심장 전체 분할용 label-to-image 합성 데이터 증강 논문으로 로보틱스와 무관함</td></tr>
<tr><td>664</td><td><a href='https://arxiv.org/abs/2608.28922'>RankShift: In-Database Detection and Explanation of Categorical Shifts</a></td><td>16</td><td>0</td><td>LG</td><td>DB 내부에서 카테고리 분포 변화를 탐지하는 방법으로 로보틱스와 무관함</td></tr>
<tr><td>665</td><td><a href='https://arxiv.org/abs/2608.29001'>Effective Graph and Rank-based Contextual Embeddings for Textual and Multimedia Data</a></td><td>16</td><td>0</td><td>LG</td><td>텍스트·멀티미디어용 rank 기반 해석가능 그래프 임베딩으로 로보틱스와 무관함</td></tr>
<tr><td>666</td><td><a href='https://arxiv.org/abs/2608.29004'>Context-Aware Interpretable Representations for Retrieval and Graph Convolutional Network Classification</a></td><td>16</td><td>0</td><td>LG</td><td>manifold 분석 기반 해석가능 그래프 임베딩으로 검색·분류에 쓰나 로보틱스와 무관함</td></tr>
<tr><td>667</td><td><a href='https://arxiv.org/abs/2608.29428'>Behavioral Latency as Weak Event-Time Supervision for EEG Reaction-Time Decoding</a></td><td>16</td><td>0</td><td>LG</td><td>EEG 반응시간 예측을 event-time posterior로 재정식화한 방법으로 로보틱스와 무관함</td></tr>
<tr><td>668</td><td><a href='https://arxiv.org/abs/2608.29635'>Unsupervised Multi-Scale Gromov-Wasserstein Hypergraph Alignment</a></td><td>16</td><td>0</td><td>LG</td><td>필터레이션 기반 다중스케일 optimal transport로 hypergraph를 정렬하는 방법으로 로보틱스와 무관함</td></tr>
<tr><td>669</td><td><a href='https://arxiv.org/abs/2608.29674'>Creation begins with understanding: LLMs as strategy designers for privacy-preserving tabular data synthesis</a></td><td>16</td><td>0</td><td>LG</td><td>LLM이 tabular 합성 전략을 설계하게 하는 프라이버시 보호 방법으로 로보틱스와 무관함</td></tr>
<tr><td>670</td><td><a href='https://arxiv.org/abs/2608.29901'>INTERVenE: Temporal-Abstraction-Interval Based Transformers for Short-Horizon Medical Event Prediction</a></td><td>16</td><td>0</td><td>LG</td><td>중환자실 사건예측용 시간추상화 트랜스포머로 로보틱스와 무관함</td></tr>
<tr><td>671</td><td><a href='https://arxiv.org/abs/2608.30021'>Error Detection for PET/CT Radiology Reports: Domain-Specific vs Large Language Models</a></td><td>16</td><td>0</td><td>LG</td><td>PET/CT 리포트 오류탐지에서 도메인특화 모델과 LLM을 비교한 의료 논문으로 로보틱스와 무관함</td></tr>
<tr><td>672</td><td><a href='https://arxiv.org/abs/2608.30394'>TopGQ: Fast GNN Post-Training Quantization Leveraging Topology Information</a></td><td>16</td><td>0</td><td>LG</td><td>GNN post-training quantization 가속 기법으로 로보틱스와 무관함.</td></tr>
<tr><td>673</td><td><a href='https://arxiv.org/abs/2608.30636'>MolLedger: An Additive Graph Neural Network with Chemically Grounded ADME Attributions</a></td><td>16</td><td>0</td><td>LG</td><td>원자 단위 additive attribution을 갖는 GNN으로 신약 특성 해석을 개선한 연구로 로보틱스와 무관함.</td></tr>
<tr><td>674</td><td><a href='https://arxiv.org/abs/2608.30682'>Learning Materials Properties from Scarce Labels and Unlabeled Crystals</a></td><td>16</td><td>0</td><td>LG</td><td>반지도 소재 물성 예측 벤치마크로 로보틱스와 무관함.</td></tr>
<tr><td>675</td><td><a href='https://arxiv.org/abs/2608.28924'>Causal Interventions Reveal Typologically Organized Syntactic Mechanisms in Multilingual Language Models</a></td><td>16</td><td>0</td><td>NLP</td><td>다국어 LM의 통사 메커니즘 전이를 mechanistic interpretability로 분석한 연구임 - 언어학적 관심사로 로보틱스와 무관함</td></tr>
<tr><td>676</td><td><a href='https://arxiv.org/abs/2608.29307'>Detecting and Repairing Hallucinations in Retrieval-Augmented Generation</a></td><td>16</td><td>0</td><td>NLP</td><td>RAG hallucination을 탐지 후 삭제·교체·재작성으로 복구하는 전략 비교임 - 로보틱스와 무관함</td></tr>
<tr><td>677</td><td><a href='https://arxiv.org/abs/2608.29846'>Influence-Directed Distillation: Solving the Diversity Bottleneck in Sampled-Token On-Policy Distillation</a></td><td>16</td><td>0</td><td>LG</td><td>온폴리시 증류에서 다양성 붕괴를 엔트로피 영향력으로 진단·완화한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>678</td><td><a href='https://arxiv.org/abs/2608.30948'>Detecting AI Impostors: How Do Middle Schoolers Identify LLM Agents in a Live Collaborative Setting?</a></td><td>16</td><td>0</td><td>NLP</td><td>중학생 대상 AI 사칭 탐지 게임 사용자 연구임</td></tr>
<tr><td>679</td><td><a href='https://arxiv.org/abs/2608.30996'>Faithfulness Is Not Free: Auditing Offline KV-Cache Quantization in Retrieval-Augmented Generation</a></td><td>16</td><td>0</td><td>NLP</td><td>RAG의 KV-cache 양자화가 faithfulness에 미치는 영향을 감사한 연구임</td></tr>
<tr><td>680</td><td><a href='https://arxiv.org/abs/2608.28591'>Expert-validated STEM QA</a></td><td>16</td><td>0</td><td>NLP</td><td>전문가 검증 STEM QA 데이터셋 구축과 post-training 검증 연구임</td></tr>
<tr><td>681</td><td><a href='https://arxiv.org/abs/2608.30912'>Responsible Integration of AI in Cancer Genomics: Barriers, Risks, and Pathways to Trustworthy Clinical Translation</a></td><td>16</td><td>0</td><td>NLP</td><td>암유전체학에 AI 도입 시 신뢰성 장벽을 정리한 리뷰 논문임</td></tr>
<tr><td>682</td><td><a href='https://arxiv.org/abs/2608.28684'>Distributed Semantic Segmentation With Improved Rate-Distortion Trade-Off</a></td><td>15</td><td>1</td><td>CV</td><td>엣지-클라우드 분산 semantic segmentation의 rate-distortion 개선임. 통신 효율화 위주라 로봇 임팩트 낮음</td></tr>
<tr><td>683</td><td><a href='https://arxiv.org/abs/2608.28689'>Projection-Aware End-to-End Learned Video Compression for 360-Degree Video</a></td><td>15</td><td>1</td><td>CV</td><td>360도 비디오 투영 방식이 신경 압축 효율에 미치는 영향 분석임. 자율주행 언급은 있으나 핵심은 압축임</td></tr>
<tr><td>684</td><td><a href='https://arxiv.org/abs/2608.28823'>Text-Driven Artistic Staging: Pose, Lighting, and Camera References from Paintings</a></td><td>15</td><td>1</td><td>3D Vision</td><td>회화에서 포즈·조명·카메라를 추출해 3D 스테이징 생성하는 연구임. 감성적 3D 생성이라 로봇과 거리 있음</td></tr>
<tr><td>685</td><td><a href='https://arxiv.org/abs/2608.29336'>FISICA: A Deployed Service for Plantar-Pressure and Posture Assessment with Ontology-Grounded Recommendation</a></td><td>15</td><td>1</td><td>CV</td><td>족압·자세 평가 배포 서비스와 아바타 피팅 방법임. 헬스케어 응용이라 로봇과 거리 있음</td></tr>
<tr><td>686</td><td><a href='https://arxiv.org/abs/2608.29408'>A Visual Question Answering Model to Automate Nondestructive Evaluation Image Analysis</a></td><td>15</td><td>1</td><td>Multimodal</td><td>비파괴검사 이미지용 VQA 모델임. 산업검사 응용이라 로봇 관련성 낮음</td></tr>
<tr><td>687</td><td><a href='https://arxiv.org/abs/2608.30149'>CedarCypress3D: an annotated UAV-LiDAR dataset of individual trees in planted cedar and cypress forests</a></td><td>15</td><td>1</td><td>3D Vision</td><td>UAV-LiDAR 개별 나무 주석 데이터셋임. 항공로봇 센싱 데이터이나 임업 응용 위주임</td></tr>
<tr><td>688</td><td><a href='https://arxiv.org/abs/2608.30088'>A Lightweight Phenology-Aware YOLOv5 Framework for Tomato Growth Stage Detection in Resource-Constrained Bhutanese Greenhouse Environments</a></td><td>15</td><td>1</td><td>CV</td><td>특정 dataset에 대한 lightweight detection backbone 개선으로 incremental engineering임. 경량화 방향이라 랩 기준상 가점 요소 아님.</td></tr>
<tr><td>689</td><td><a href='https://arxiv.org/abs/2608.28681'>CARD: Calibration via Agreement in Reverse Diffusion for Out-of-Domain MRI Segmentation</a></td><td>15</td><td>0</td><td>CV</td><td>MRI 도메인 시프트 하 확산모델 기반 calibration 기법임. 의료영상 특화라 로봇 관련성 낮음</td></tr>
<tr><td>690</td><td><a href='https://arxiv.org/abs/2608.28687'>FLM: Frequency-Aware Language Models for Generative Image Compression</a></td><td>15</td><td>0</td><td>CV</td><td>주파수 인식 언어모델 기반 이미지 압축임. 로봇과 무관한 압축 효율화 연구임</td></tr>
<tr><td>691</td><td><a href='https://arxiv.org/abs/2608.28784'>ClearText-Video: A Large-Scale Text-Centric Video Dataset Bridging Video Restoration and Scene-Text Enhancement</a></td><td>15</td><td>0</td><td>Video</td><td>장면 텍스트 인식용 비디오 복원 벤치마크임. 로봇과 무관함</td></tr>
<tr><td>692</td><td><a href='https://arxiv.org/abs/2608.28814'>FigMirror: Ground It, Code It, Plot It</a></td><td>15</td><td>0</td><td>Multimodal</td><td>과학 그림을 코드로 변환해 스타일 유지하며 재플로팅하는 에이전트임. 로봇과 무관함</td></tr>
<tr><td>693</td><td><a href='https://arxiv.org/abs/2608.28909'>Coarse to Fine: Iterative Adversarial Neural Cellular Automata for Medical Image Synthesis</a></td><td>15</td><td>0</td><td>CV</td><td>경량 Neural Cellular Automata 기반 의료영상 생성 GAN임. 로봇과 무관함</td></tr>
<tr><td>694</td><td><a href='https://arxiv.org/abs/2608.28923'>ActiveAugment: Online Active Learning for Augmentation Selection in Deep Learning</a></td><td>15</td><td>0</td><td>LG</td><td>온라인 active learning 기반 데이터 증강 선택 프레임워크임. 로봇과 무관한 일반 학습 기법임</td></tr>
<tr><td>695</td><td><a href='https://arxiv.org/abs/2608.29037'>DocIntent: Answerability-Guided Agentic Restoration for Real-World Document Visual Question Answering</a></td><td>15</td><td>0</td><td>Multimodal</td><td>문서 열화 복원을 답변 가능성 기준으로 선택 실행하는 agentic 프레임워크임. 로봇과 무관함</td></tr>
<tr><td>696</td><td><a href='https://arxiv.org/abs/2608.29123'>Dancing Stick Figures: An Introductory Dataset for Training Video Generation Models</a></td><td>15</td><td>0</td><td>Video</td><td>비디오 생성 모델 학습용 소규모 stick figure 합성 데이터셋임. 로봇과 무관함</td></tr>
<tr><td>697</td><td><a href='https://arxiv.org/abs/2608.29167'>Feature-Spectral Fragility in Segmentation: Dataset Dependence, Architecture-Specific Localization, and Spectral Correlates</a></td><td>15</td><td>0</td><td>CV</td><td>segmentation 모델의 feature-domain 주파수 취약성 분석임. 일반적 강건성 분석이나 로봇 특화는 아님</td></tr>
<tr><td>698</td><td><a href='https://arxiv.org/abs/2608.29268'>Learning to Ground Before Reading: Unified PCB Engineering Drawing Parsing with Compact Vision-Language Models</a></td><td>15</td><td>0</td><td>Multimodal</td><td>PCB 도면을 읽는 경량 VLM 파싱 연구임. 로봇과 무관함</td></tr>
<tr><td>699</td><td><a href='https://arxiv.org/abs/2608.29280'>RAGDiffusion++: From Macro-Retrieval to Micro-Fidelity Alignment for Garment Generation</a></td><td>15</td><td>0</td><td>Generative</td><td>의류 자산 생성의 고주파 텍스처 재현 RL 기법임. 로봇과 무관한 패션 응용임</td></tr>
<tr><td>700</td><td><a href='https://arxiv.org/abs/2608.29287'>PERSIST: Persistent-State Discrimination for Shot Boundary Detection</a></td><td>15</td><td>0</td><td>Video</td><td>샷 경계 검출에서 지속성 기반 판별 기법임. 로봇과 무관함</td></tr>
<tr><td>701</td><td><a href='https://arxiv.org/abs/2608.29456'>Text-Guided Diffusion-Based Adversarial Attacks on Chest X-Ray Images</a></td><td>15</td><td>0</td><td>CV</td><td>흉부 X-ray 분류기에 텍스트 유도 확산 적대공격을 가하는 연구임. 의료 AI 안전성 연구로 로봇과 무관함</td></tr>
<tr><td>702</td><td><a href='https://arxiv.org/abs/2608.29467'>Co-Evolutionary Prompt Optimization with Cross-Category Transfer for Zero-Shot Anomaly Detection</a></td><td>15</td><td>0</td><td>CV</td><td>제로샷 이상탐지용 진화 알고리즘 기반 프롬프트 최적화임. 산업검사 응용이라 로봇과 거리 있음</td></tr>
<tr><td>703</td><td><a href='https://arxiv.org/abs/2608.29577'>TRINITY: A Multi-Perspective Benchmark for Personal-Style Video Highlight Detection</a></td><td>15</td><td>0</td><td>Video</td><td>개인 취향별 비디오 하이라이트 탐지 벤치마크임. 로봇과 무관함</td></tr>
<tr><td>704</td><td><a href='https://arxiv.org/abs/2608.29607'>SnapBench: Benchmarking Snap-and-Ask Multimodal Retrieval for Mobile Interactions</a></td><td>15</td><td>0</td><td>Multimodal</td><td>모바일 스냅-질문 검색의 강건성 벤치마크임. 로봇과 무관함</td></tr>
<tr><td>705</td><td><a href='https://arxiv.org/abs/2608.29626'>SPLG-Mamba: Structure-Preserving Local-Global Mamba Network for Salient Object Detection in Optical Remote Sensing Images</a></td><td>15</td><td>0</td><td>CV</td><td>원격탐사 영상 salient object detection용 Mamba 네트워크임. 로봇과 무관함</td></tr>
<tr><td>706</td><td><a href='https://arxiv.org/abs/2608.29680'>GeoRay: Gauge-Aware Feed-Forward Satellite 3D Reconstruction in the Geodetic Frame</a></td><td>15</td><td>0</td><td>3D Vision</td><td>위성 사진측량의 지오데틱 프레임 3D 복원 기법임. 로봇과 무관한 원격탐사 연구임</td></tr>
<tr><td>707</td><td><a href='https://arxiv.org/abs/2608.29809'>RegionCache: Semantic-Aware Region Reuse for Efficient Multi-Turn Image Generation</a></td><td>15</td><td>0</td><td>Generative</td><td>다중턴 이미지 편집에서 안 바뀐 영역을 재사용해 가속하는 캐시 기법임. 로봇과 무관함</td></tr>
<tr><td>708</td><td><a href='https://arxiv.org/abs/2608.29905'>OrnaStyler: Ornament-Aware Latent Editing for Content-Preserving 3D Stylization</a></td><td>15</td><td>0</td><td>3D Vision</td><td>텍스트 유도로 3D 자산에 장식적 스타일을 입히는 콘텐츠 제작 기법임. 로봇과 무관함</td></tr>
<tr><td>709</td><td><a href='https://arxiv.org/abs/2608.29929'>Evaluating 2D and 3D-Aware Vision Foundation Models for Vehicle Attribute Recognition</a></td><td>15</td><td>0</td><td>CV</td><td>차량 속성 인식용 2D/3D foundation model 벤치마크임. 로봇과 무관함</td></tr>
<tr><td>710</td><td><a href='https://arxiv.org/abs/2608.29992'>SVI2LoD3: Agent-Driven Reconstruction of LoD3 Facade Openings in Semantic 3D City Models from Volunteered Street View Imagery using Large Language and Visual Models</a></td><td>15</td><td>0</td><td>3D Vision</td><td>거리뷰 영상으로 LoD3 건물 파사드를 복원하는 LLM·VLM 에이전트 파이프라인임. 도시 모델링 응용이라 로봇과 무관함</td></tr>
<tr><td>711</td><td><a href='https://arxiv.org/abs/2608.30003'>OPAL: Orthonormal Prototype Alignment Learning for Interpretable Image Classification</a></td><td>15</td><td>0</td><td>CV</td><td>직교 프로토타입 정렬 기반 설명가능 이미지 분류 기법임. 로봇과 무관함</td></tr>
<tr><td>712</td><td><a href='https://arxiv.org/abs/2608.30068'>TAKE 85: Testing Audiovisual filmmaKer&#x27;s intEnt across 85 Hours of Film</a></td><td>15</td><td>0</td><td>Multimodal</td><td>영화 연출 의도 이해 벤치마크임. 로봇과 무관함</td></tr>
<tr><td>713</td><td><a href='https://arxiv.org/abs/2608.30094'>A Hybrid State-Space Approach for Census-Tract Population Estimation</a></td><td>15</td><td>0</td><td>CV</td><td>행정구역 단위 인구 추정용 시퀀스 모델(Mamba)임. 로봇과 무관함</td></tr>
<tr><td>714</td><td><a href='https://arxiv.org/abs/2608.30404'>ImageCAS-X: a dataset and benchmark for coronary artery segmentation and centerline extraction in coronary CT angiography</a></td><td>15</td><td>0</td><td>CV</td><td>관상동맥 분할 의료 데이터셋으로 로보틱스와 무관함</td></tr>
<tr><td>715</td><td><a href='https://arxiv.org/abs/2608.30458'>Federated Multi-Task Learning for Bladder Tumor Segmentation and MIBC Classification Using a Hybrid CNN-Transformer Architecture</a></td><td>15</td><td>0</td><td>CV</td><td>방광 종양 federated segmentation 의료 논문으로 로보틱스와 무관함</td></tr>
<tr><td>716</td><td><a href='https://arxiv.org/abs/2608.30467'>Beyond Accuracy: Quantifying Pulmonary Attribution in Anatomy-Guided Chest X-Ray Classification Under Domain Shift</a></td><td>15</td><td>0</td><td>CV</td><td>흉부 X-ray 해부학 기반 분류 신뢰성 연구로 로보틱스와 무관함</td></tr>
<tr><td>717</td><td><a href='https://arxiv.org/abs/2608.30616'>OCR-Based Field Extraction for Archaeological Pottery Metadata: The CENTURIA Dataset</a></td><td>15</td><td>0</td><td>CV</td><td>고고학 도자기 손글씨 메타데이터 OCR 논문으로 로보틱스와 무관함</td></tr>
<tr><td>718</td><td><a href='https://arxiv.org/abs/2608.30688'>UFPR-PEs: A Brazilian Face Recognition Benchmark with Self-Declared Race/Color Labels</a></td><td>15</td><td>0</td><td>CV</td><td>브라질 정치인 얼굴인식 인종 편향 벤치마크로 로보틱스와 무관함</td></tr>
<tr><td>719</td><td><a href='https://arxiv.org/abs/2608.30758'>CheXGround: Anatomical Region Tokens for Grounded Longitudinal Chest X-ray Interpretation</a></td><td>15</td><td>0</td><td>CV</td><td>흉부 X-ray 종단 해부영역 언어모델 논문으로 로보틱스와 무관함</td></tr>
<tr><td>720</td><td><a href='https://arxiv.org/abs/2608.30768'>CORAL: A Benchmark for Structure-aware and Brain-wide Neuron Reconstruction in Light Microscopy</a></td><td>15</td><td>0</td><td>CV</td><td>뉴런 재구성 벤치마크로 로보틱스와 무관한 신경과학 응용임</td></tr>
<tr><td>721</td><td><a href='https://arxiv.org/abs/2608.30824'>Whole-Body MRI Classification via Prompt-Based Clinical Conditioning</a></td><td>15</td><td>0</td><td>CV</td><td>전신 MRI와 임상변수 결합 진단 논문으로 로보틱스와 무관함</td></tr>
<tr><td>722</td><td><a href='https://arxiv.org/abs/2608.30857'>TAMI: Temporally Aligned, Missingness-Aware, and Interpretable Multimodal Fusion for Mental Health Assessment in Older Adults with Mild Cognitive Impairment</a></td><td>15</td><td>0</td><td>CV</td><td>노인 인지장애 우울·불안 스크리닝용 멀티모달 융합 논문으로 로보틱스와 무관함</td></tr>
<tr><td>723</td><td><a href='https://arxiv.org/abs/2608.30951'>Audio-Driven Adversarial Defense for 3D Talking Face Generation with totally Visual Fidelity Preservation</a></td><td>15</td><td>0</td><td>CV</td><td>3D 토킹페이스 생성 방지를 위한 오디오 영역 방어 논문으로 로보틱스와 무관함</td></tr>
<tr><td>724</td><td><a href='https://arxiv.org/abs/2608.31052'>Segmentation of Bovid Dentition Under Imperfect Annotations: A Comparative Study of Convolutional and Attention Models</a></td><td>15</td><td>0</td><td>CV</td><td>소·화석 치아 분할에서 라벨 불완전성 비교연구로 로보틱스와 무관함</td></tr>
<tr><td>725</td><td><a href='https://arxiv.org/abs/2608.31094'>Robust retinal biometrics for patient identity verification and retrieval across age and imaging devices</a></td><td>15</td><td>0</td><td>CV</td><td>망막 생체인식 환자식별 시스템으로 로보틱스와 무관함</td></tr>
<tr><td>726</td><td><a href='https://arxiv.org/abs/2608.28905'>Off-Policy Evaluation for Semantic ID Recommenders: Does the Model&#x27;s Own Code Hierarchy Help?</a></td><td>15</td><td>0</td><td>LG</td><td>semantic ID 추천시스템의 off-policy evaluation 방법으로 로보틱스와 무관함</td></tr>
<tr><td>727</td><td><a href='https://arxiv.org/abs/2608.29024'>Hybrid Semantic Context-Enhanced Ensemble Learning for Wind Power Ramp-Event Forecasting and Uncertainty-Aware Evaluation</a></td><td>15</td><td>0</td><td>LG</td><td>풍력 급변 예측에 텍스트 임베딩을 결합한 앙상블로 로보틱스와 무관함</td></tr>
<tr><td>728</td><td><a href='https://arxiv.org/abs/2608.29045'>NVE: A Separability and Coverage-Aware Internal Validation Metric for Biclustering</a></td><td>15</td><td>0</td><td>LG</td><td>biclustering 내부 검증지표 제안 논문으로 로보틱스와 무관함</td></tr>
<tr><td>729</td><td><a href='https://arxiv.org/abs/2608.29093'>Titans-QFWP: A Regime-Aware Hybrid Quantum Fast Weight Programmer for Portfolio Optimization</a></td><td>15</td><td>0</td><td>LG</td><td>포트폴리오 최적화용 양자 fast weight programmer로 로보틱스와 무관함</td></tr>
<tr><td>730</td><td><a href='https://arxiv.org/abs/2608.29755'>GraM-Diff: A Unified Graph-Mamba Diffusion Framework for EEG-Based Alzheimer&#x27;s Disease Data Generation and Diagnosis</a></td><td>15</td><td>0</td><td>LG</td><td>EEG 알츠하이머 진단용 그래프-맘바 확산 생성모델로 로보틱스와 무관함</td></tr>
<tr><td>731</td><td><a href='https://arxiv.org/abs/2608.30102'>SMOTE-VAR: An Uncertainty-Aware Oversampling Method for Predicting Depression Remission in University Students</a></td><td>15</td><td>0</td><td>LG</td><td>임상 데이터 oversampling 방법론으로 로봇 지능과 무관함.</td></tr>
<tr><td>732</td><td><a href='https://arxiv.org/abs/2608.30175'>Benchmarking Peptide-Protein Affinity Prediction Across Peptide and Target Shifts</a></td><td>15</td><td>0</td><td>LG</td><td>신약 관련 벤치마크 연구로 로보틱스와 무관함.</td></tr>
<tr><td>733</td><td><a href='https://arxiv.org/abs/2608.30201'>Certified Safety Radii in Forecast-Error Space for Wasserstein Distributionally Robust Small Signal Stability-Constrained AC Optimal Power Flow via Lifted Spectrahedral Containment</a></td><td>15</td><td>0</td><td>LG</td><td>전력망 안정성 최적화 이론으로 로봇 지능과 무관함.</td></tr>
<tr><td>734</td><td><a href='https://arxiv.org/abs/2608.30262'>Multivariate Scientific Data Compression with Learned Cross-Variable Latent Decorrelation and Autoregressive Entropy Modeling</a></td><td>15</td><td>0</td><td>LG</td><td>과학 시뮬레이션 데이터 압축 방법으로 로보틱스와 무관함.</td></tr>
<tr><td>735</td><td><a href='https://arxiv.org/abs/2608.30337'>Coarse composition suffices: tabular in-context learning for multi-activity antimicrobial peptide profiling</a></td><td>15</td><td>0</td><td>LG</td><td>항균 펩타이드 다중 활성 예측 연구로 로보틱스와 무관함.</td></tr>
<tr><td>736</td><td><a href='https://arxiv.org/abs/2608.30364'>Beyond Churn: Predicting Financial Fragmentation in Retail Banking with Temporal Machine Learning</a></td><td>15</td><td>0</td><td>LG</td><td>은행 고객 이탈 예측 시스템으로 로보틱스와 완전히 무관함.</td></tr>
<tr><td>737</td><td><a href='https://arxiv.org/abs/2608.30449'>PRIME: Mitigating Subgroup Optimization Competition in Shared CTR Top Networks with Plug-in Residual Input-Conditioned Mixture of Expert</a></td><td>15</td><td>0</td><td>LG</td><td>CTR 모델 top network의 subgroup 경쟁을 완화하는 residual MoE 기법으로 로보틱스와 무관함.</td></tr>
<tr><td>738</td><td><a href='https://arxiv.org/abs/2608.30456'>Self-Supervised Pretext Tasks for Infant Cry Analysis: A Controlled Comparison and a Cautionary Result on Donateacry</a></td><td>15</td><td>0</td><td>CV</td><td>아기 울음 분석용 self-supervised pretext task 비교 연구로 로보틱스와 무관함.</td></tr>
<tr><td>739</td><td><a href='https://arxiv.org/abs/2608.30472'>ToxLens: A Reproducible Graph-Learning Framework for Leakage-Aware, Uncertainty-Calibrated Molecular Toxicity Prediction</a></td><td>15</td><td>0</td><td>LG</td><td>분자 독성 예측을 위한 leakage-aware GNN 프레임워크로 로보틱스와 무관함.</td></tr>
<tr><td>740</td><td><a href='https://arxiv.org/abs/2608.30593'>State of Health Estimation using Convolutional and Bidirectional LSTM Neural Networks tuned by Bayesian Optimization</a></td><td>15</td><td>0</td><td>LG</td><td>배터리 건강 상태 추정을 위한 하이브리드 딥러닝+베이지안 튜닝 연구로 로보틱스와 무관함.</td></tr>
<tr><td>741</td><td><a href='https://arxiv.org/abs/2608.30654'>Season-Aware Hybrid Convolutional-Transformer for Antarctic Sea Ice Concentration Forecasting</a></td><td>15</td><td>0</td><td>Video</td><td>계절성 prior를 결합한 hybrid conv-transformer 해빙 예측 연구로 로보틱스와 무관함.</td></tr>
<tr><td>742</td><td><a href='https://arxiv.org/abs/2608.30745'>TDDM-Melatt: A Decoupled Memory and Diffusion Framework for Generalizable Encrypted Traffic Classification</a></td><td>15</td><td>0</td><td>LG</td><td>암호화 트래픽 분류를 위한 memory-decoupled diffusion 프레임워크로 로보틱스와 무관함.</td></tr>
<tr><td>743</td><td><a href='https://arxiv.org/abs/2608.30769'>TrainSDC: Characterizing and Mitigating Silent Data Corruption in Large Language Model Training</a></td><td>15</td><td>0</td><td>LG</td><td>LLM 학습 중 silent data corruption을 특성화하고 완화하는 시스템 연구로 로보틱스와 무관함.</td></tr>
<tr><td>744</td><td><a href='https://arxiv.org/abs/2608.30944'>Nonparametric Contextual Pricing and Inventory Learning under Censored Demand</a></td><td>15</td><td>0</td><td>LG</td><td>온라인 소매 가격·재고 학습 알고리즘으로 로보틱스와 무관함.</td></tr>
<tr><td>745</td><td><a href='https://arxiv.org/abs/2608.28614'>STAGEET: Stage-wise Typed Edit Tagging for Grammatical Error Correction with Arabic as a Case Study</a></td><td>15</td><td>0</td><td>NLP</td><td>문법 오류 교정을 단계별 타입드 edit tagging으로 재구성한 논문임 - 아랍어 GEC 특화 기여로 로보틱스와 무관함</td></tr>
<tr><td>746</td><td><a href='https://arxiv.org/abs/2608.28619'>From GenAI Virtual Patient Dialogue Logs to Teacher-Interpretable Process Evidence: A Learning Analytics Study in Higher Education</a></td><td>15</td><td>0</td><td>NLP</td><td>의대생 가상환자 대화 로그를 교사가 해석 가능한 형태로 분석한 학습분석 연구임 - 임상교육 응용이라 로보틱스와 무관함</td></tr>
<tr><td>747</td><td><a href='https://arxiv.org/abs/2608.28624'>MA-RAG: Multi-Agent Retrieval-Augmented Generation for Query-Driven Summarization of Longitudinal Parkinson&#x27;s Disease Assessments</a></td><td>15</td><td>0</td><td>NLP</td><td>파킨슨병 종단 임상기록 요약용 멀티에이전트 RAG 논문임 - 의료 도메인 특화로 로보틱스와 무관함</td></tr>
<tr><td>748</td><td><a href='https://arxiv.org/abs/2608.28626'>Do large language models scrutinise what they review? A multimodal audit of scoring calibration, error detection, and author-identity effects</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM이 논문 심사에서 얼마나 엄밀히 검증하는지 감사한 연구임 - 메타 연구 성격으로 로보틱스와 무관함</td></tr>
<tr><td>749</td><td><a href='https://arxiv.org/abs/2608.28629'>Intelligent Identification and Repair of Design Defects in BIM via Domain-Specific Large Language Models</a></td><td>15</td><td>0</td><td>NLP</td><td>건축 BIM 설계결함 탐지·수정에 도메인 특화 LLM 적용한 응용 논문임 - 로보틱스 연관성 낮음</td></tr>
<tr><td>750</td><td><a href='https://arxiv.org/abs/2608.28641'>Terminal-Bench-LILT: Multilingual Agentic Coding Benchmark Grounded in Language, Region, and Culture</a></td><td>15</td><td>0</td><td>NLP</td><td>다국어 코딩 에이전트 벤치마크임 - 문화·언어 특화 코딩 태스크로 로보틱스와 무관함</td></tr>
<tr><td>751</td><td><a href='https://arxiv.org/abs/2608.28860'>Latent-Space Intervention for Cross-Lingual Factual Consistency: Consistency Improvements without Accuracy Drops</a></td><td>15</td><td>0</td><td>NLP</td><td>다국어 factual QA 일관성 개선용 latent space intervention임 - 로보틱스와 무관함</td></tr>
<tr><td>752</td><td><a href='https://arxiv.org/abs/2608.29120'>HEAR Who Said What: Unlocking Speaker-Attributed Reasoning via Counterfactual Voice Grounding</a></td><td>15</td><td>0</td><td>NLP</td><td>다화자 음성모델의 화자 귀속 추론 벤치마크·모델임 - 로보틱스와 무관함</td></tr>
<tr><td>753</td><td><a href='https://arxiv.org/abs/2608.29241'>When Patients Cut In: Extending Clinical Conversational AI Safety to Interruptions</a></td><td>15</td><td>0</td><td>NLP</td><td>임상 음성 에이전트의 환자 인터럽션 대응 안전성 평가임 - 로보틱스와 무관함</td></tr>
<tr><td>754</td><td><a href='https://arxiv.org/abs/2608.29517'>LLM Judges as Raters: A Pre-Registered Audit of Severity, Halo, Reliability, and Version Instability in LLM Essay Scoring on Public Corpora</a></td><td>15</td><td>0</td><td>NLP</td><td>에세이 채점 LLM 심사관의 심각도·halo·버전불안정성 감사 연구임 - 교육측정학 응용으로 로보틱스와 무관함</td></tr>
<tr><td>755</td><td><a href='https://arxiv.org/abs/2608.29529'>Argument-Aware Semantic Alignment of Normative Texts: A Toulmin-Based Neuro-Symbolic Approach</a></td><td>15</td><td>0</td><td>NLP</td><td>논증구조(Toulmin) 기반 규범문서 정합 뉴로심볼릭 파이프라인임 - 사이버보안 표준 매핑 도메인이라 로보틱스와 무관함</td></tr>
<tr><td>756</td><td><a href='https://arxiv.org/abs/2608.29591'>How You Ask Shapes What You Get: A Theory-Seeded Measurement of Articulation in Advice-Seeking LLM Conversations</a></td><td>15</td><td>0</td><td>NLP</td><td>조언요청 프롬프트의 표현양식이 응답에 미치는 영향을 측정한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>757</td><td><a href='https://arxiv.org/abs/2608.29617'>Memory-First Fact-Checking: A Knowledge-Graph-Grounded Multi-Agent System for Misinformation Detection</a></td><td>15</td><td>0</td><td>NLP</td><td>지식그래프 기반 허위정보 탐지 멀티에이전트 시스템임 - 로보틱스와 무관함</td></tr>
<tr><td>758</td><td><a href='https://arxiv.org/abs/2608.29623'>MI-Distillation: Selecting from Model-Interpolated Instruct-Reasoning Data Spectrum for Chain-of-Thought Distillation</a></td><td>15</td><td>0</td><td>LG</td><td>Long CoT distillation에서 gradient 관점 데이터 스펙트럼 선택 기법임 - 로보틱스와 무관함</td></tr>
<tr><td>759</td><td><a href='https://arxiv.org/abs/2608.29748'>ReTrace: Rejected-Trajectory Conditioning for Speculative Decoding</a></td><td>15</td><td>0</td><td>LG</td><td>추측 디코딩에서 거부된 suffix를 다음 블록에 재사용하는 기법임 - 추론 가속화 연구로 로보틱스와 무관함</td></tr>
<tr><td>760</td><td><a href='https://arxiv.org/abs/2608.29834'>You Know What I Mean: A Benchmark for Agentic Conversational Reference Grounding</a></td><td>15</td><td>0</td><td>NLP</td><td>대화 중 간접 참조를 외부 워크스페이스 도구로 해소하는 벤치마크임 - 개발자 채팅 도메인으로 로보틱스와 무관함</td></tr>
<tr><td>761</td><td><a href='https://arxiv.org/abs/2608.29936'>When Safety Speaks a Language: A Mechanistic Analysis of Safety-Language Identity Entanglement in LLMs</a></td><td>15</td><td>0</td><td>LG</td><td>다국어 안전정렬 특징이 언어정체성과 얽혀있다는 SAE 기반 분석임 - 로보틱스와 무관함</td></tr>
<tr><td>762</td><td><a href='https://arxiv.org/abs/2608.29978'>Evolutionary Soups: Evolving Mixture-of-Experts for Multi-Objective LLM Alignment</a></td><td>15</td><td>0</td><td>LG</td><td>다목적 정렬을 위해 MoE 게이팅을 진화알고리즘으로 훈련한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>763</td><td><a href='https://arxiv.org/abs/2608.30005'>Small Language Models as Judges for Rubric-Based Reinforcement Learning</a></td><td>15</td><td>0</td><td>LG</td><td>루브릭 기반 RL 보상함수로 소형 LM 심사관을 쓰는 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>764</td><td><a href='https://arxiv.org/abs/2608.30076'>Budget-Aware Compression Pipeline for Single-GPU LLM Inference: Methods, Trade-offs, and Coupling Effects</a></td><td>15</td><td>0</td><td>LG</td><td>70B 모델을 단일 GPU에 압축배치하는 pruning·quantization·KV압축 결합 연구임 - 효율화 엔지니어링으로 로보틱스와 무관함</td></tr>
<tr><td>765</td><td><a href='https://arxiv.org/abs/2608.30135'>Verification-Aware Training for Speculative Decoding</a></td><td>15</td><td>0</td><td>LG</td><td>추측 디코딩 드래프트 모델을 검증패턴으로 학습시키는 기법임 - 추론 가속화 연구로 로보틱스와 무관함</td></tr>
<tr><td>766</td><td><a href='https://arxiv.org/abs/2608.30158'>CPR for LLMs: Critical-Point Routing against Catastrophic Forgetting in Domain Adaptation</a></td><td>15</td><td>0</td><td>LG</td><td>토큰단위 라우팅으로 도메인적응 시 catastrophic forgetting을 줄인 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>767</td><td><a href='https://arxiv.org/abs/2608.30197'>ALTSTEER: Selective Safety Steering for Moving Beyond Hard Refusals to Constructive Alternatives</a></td><td>15</td><td>0</td><td>NLP</td><td>안전 거부를 건설적 대안으로 바꾸는 선택적 스티어링 기법임 - 로보틱스와 무관함</td></tr>
<tr><td>768</td><td><a href='https://arxiv.org/abs/2608.30583'>Language Proficiency Assessment from Eye Movements in Naturalistic Passage Reading</a></td><td>15</td><td>0</td><td>NLP</td><td>안구운동으로 언어 숙련도 측정, 인지과학 응용 연구임</td></tr>
<tr><td>769</td><td><a href='https://arxiv.org/abs/2608.30731'>Calibrating Small Language Models for Claim Check-Worthiness Detection</a></td><td>15</td><td>0</td><td>NLP</td><td>소형 LM의 fact-checking 신뢰도 검증 가능성 보정 기법임</td></tr>
<tr><td>770</td><td><a href='https://arxiv.org/abs/2608.30856'>You Shouldn&#x27;t Have Asked: A Pragmatics-Inspired Taxonomy for Evaluating LLM Refusals</a></td><td>15</td><td>0</td><td>NLP</td><td>화용론 기반 LLM 거절 분류체계 제안 연구임</td></tr>
<tr><td>771</td><td><a href='https://arxiv.org/abs/2608.31139'>Configurable Semantic Chunking for Biomedical Information Extraction in Retrieval-Augmented Generation</a></td><td>15</td><td>0</td><td>NLP</td><td>생의학 RAG용 configurable semantic chunking 기법임</td></tr>
<tr><td>772</td><td><a href='https://arxiv.org/abs/2608.28595'>The Signal in the Noise: An Auditable Reliability Layer for Biomedical Text Classification</a></td><td>15</td><td>0</td><td>NLP</td><td>생의학 텍스트 분류를 위한 보수적 철자교정 신뢰성 레이어임</td></tr>
<tr><td>773</td><td><a href='https://arxiv.org/abs/2608.28602'>Integrating Triaxial IMU Sensors and Ensemble Learning for Effective Parkinson Disease Severity Classification</a></td><td>15</td><td>0</td><td>AI</td><td>IMU 센서 기반 파킨슨병 중증도 분류 앙상블 비교 연구임</td></tr>
<tr><td>774</td><td><a href='https://arxiv.org/abs/2608.28944'>Oculi: A Conversational Agentic Platform for Automated Credit Risk Analysis</a></td><td>15</td><td>0</td><td>AI</td><td>신용 위험 분석 자동화용 대화형 multi-agent 플랫폼, 금융 도메인 산업 응용 연구임</td></tr>
<tr><td>775</td><td><a href='https://arxiv.org/abs/2608.28974'>From Analytics to Tumor Boards: An Evidence-Linked Multi-Agent Workflow for Oncology Feature Extraction</a></td><td>15</td><td>0</td><td>AI</td><td>종양학 문서에서 구조화 필드를 추출하는 증거 연결 multi-agent 워크플로우임</td></tr>
<tr><td>776</td><td><a href='https://arxiv.org/abs/2608.29368'>Reviving our data foundations is the most disruptive step to data maturity</a></td><td>15</td><td>0</td><td>NLP</td><td>기업 지식그래프 인프라 재정비를 주장하는 비전 성격 글임, 실증 연구가 아님</td></tr>
<tr><td>777</td><td><a href='https://arxiv.org/abs/2608.30865'>Predicting Residential Rents in Dakar Using Machine Learning</a></td><td>15</td><td>0</td><td>LG</td><td>다카르 임대료를 웹스크래핑 데이터로 예측한 지역 특화 머신러닝 사례임</td></tr>
<tr><td>778</td><td><a href='https://arxiv.org/abs/2608.29110'>Explainable Machine Learning for Broadband Adoption Disparities: Tract-Level Prediction and SHAP-Based Factor Profiling</a></td><td>14</td><td>0</td><td>LG</td><td>광대역 인터넷 격차 예측 SHAP 분석으로 로보틱스와 무관함</td></tr>
<tr><td>779</td><td><a href='https://arxiv.org/abs/2608.29262'>Adaptive Multi-Branching for Shallow Decision Tree Induction</a></td><td>14</td><td>0</td><td>LG</td><td>얕은 결정트리에 multi-way split을 도입한 표형 데이터 방법으로 로보틱스와 무관함</td></tr>
<tr><td>780</td><td><a href='https://arxiv.org/abs/2608.29302'>A Spectral Identifiability Threshold for Dissipative Rate Recovery from Truncated Liouvillian Spectra</a></td><td>14</td><td>0</td><td>LG</td><td>소산율 복원을 위한 스펙트럼 식별가능성 이론으로 로보틱스와 무관함</td></tr>
<tr><td>781</td><td><a href='https://arxiv.org/abs/2608.29304'>MEL: Coordinate-Preserving EEG Tokenization for fMRI Translation</a></td><td>14</td><td>0</td><td>LG</td><td>EEG를 fMRI로 변환하는 토큰화 방법으로 로보틱스와 무관함</td></tr>
<tr><td>782</td><td><a href='https://arxiv.org/abs/2608.29360'>Spatial Entropy based Partitioning for Spatiotemporal Graph Unlearning</a></td><td>14</td><td>0</td><td>LG</td><td>공간엔트로피 기반 그래프 분할로 spatiotemporal graph unlearning을 다룬 논문으로 로보틱스와 무관함</td></tr>
<tr><td>783</td><td><a href='https://arxiv.org/abs/2608.29369'>Unlearning on Spatio-Temporal Graphs through Subgraph Virtual Edge Reconstruction</a></td><td>14</td><td>0</td><td>LG</td><td>뇌량 구조에서 착안한 가상엣지로 spatio-temporal graph unlearning하는 논문으로 로보틱스와 무관함</td></tr>
<tr><td>784</td><td><a href='https://arxiv.org/abs/2608.29419'>Scalable Clinical Data Infrastructure and Comparative ML Evaluation for Hospitalisation Risk Prediction in Elderly Patients with Multiple Long-Term Conditions using CPRD</a></td><td>14</td><td>0</td><td>LG</td><td>노인 다중질환 입원위험 예측 파이프라인 벤치마크로 로보틱스와 무관함</td></tr>
<tr><td>785</td><td><a href='https://arxiv.org/abs/2608.29496'>Target-Aware State-Adaptive $p$-Dirichlet Graph Neural Regression for Non-Invasive Body-Composition Estimation</a></td><td>14</td><td>0</td><td>LG</td><td>체성분 추정용 그래프 신경망 회귀로 로보틱스와 무관함</td></tr>
<tr><td>786</td><td><a href='https://arxiv.org/abs/2608.29763'>ECA-BLS: An Efficient Complex-Augmented Broad Learning System</a></td><td>14</td><td>0</td><td>LG</td><td>복소수 확장 broad learning system 효율화 논문으로 로보틱스와 무관함</td></tr>
<tr><td>787</td><td><a href='https://arxiv.org/abs/2608.29850'>Designing for the Next Click: Bandits for Real-Time Page Layout</a></td><td>14</td><td>0</td><td>LG</td><td>실시간 페이지 레이아웃을 밴딧으로 최적화하는 이커머스 응용으로 로보틱스와 무관함</td></tr>
<tr><td>788</td><td><a href='https://arxiv.org/abs/2608.29983'>Robust Broad Learning System with Wave Loss for Classification under Data Uncertainty</a></td><td>14</td><td>0</td><td>LG</td><td>wave loss 기반 강건 broad learning system으로 로보틱스와 무관함</td></tr>
<tr><td>789</td><td><a href='https://arxiv.org/abs/2608.28630'>Enabling Proactive Spoken Turns via a Generalized Style-Aware Full-Duplex Framework</a></td><td>14</td><td>0</td><td>NLP</td><td>능동적 발화 타이밍을 다루는 full-duplex 음성대화 프레임워크임 - 로봇 상호작용과 직접 관련 없음</td></tr>
<tr><td>790</td><td><a href='https://arxiv.org/abs/2608.28635'>Do MLLMs Really Understand Low-Resource Khmer Documents? A Pilot Study on Khmer Document VQA</a></td><td>14</td><td>0</td><td>NLP</td><td>크메르어 문서 VQA에 대한 MLLM 진단 평가임 - 저자원 언어 문서이해 파일럿 연구로 로보틱스와 무관함</td></tr>
<tr><td>791</td><td><a href='https://arxiv.org/abs/2608.29257'>Large Language Models Systematically Favor Popular Options: Evidence and Mitigation Across MCQs</a></td><td>14</td><td>0</td><td>NLP</td><td>LLM이 인기있는 오답을 선호하는 편향과 완화기법 연구임 - 평가방법론으로 로보틱스와 무관함</td></tr>
<tr><td>792</td><td><a href='https://arxiv.org/abs/2608.29453'>AI Can Be Easily Persuaded in Clinical Decision Making</a></td><td>14</td><td>0</td><td>NLP</td><td>임상 의사결정에서 AI가 권위·설득에 쉽게 흔들리는지 실험한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>793</td><td><a href='https://arxiv.org/abs/2608.29887'>Check The Scoreboard: An Analysis of Scoring Schemes on Multiple-Choice Evaluation</a></td><td>14</td><td>0</td><td>NLP</td><td>객관식 평가에서 채점방식 대안을 분석한 메타 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>794</td><td><a href='https://arxiv.org/abs/2608.29966'>DataFoundry: Evolving Data Preparators via Recursive Self-Improvement</a></td><td>14</td><td>0</td><td>NLP</td><td>재귀적 자기개선으로 데이터 전처리기를 진화시키는 프레임워크임 - 도메인적응 데이터 파이프라인 연구로 로보틱스와 무관함</td></tr>
<tr><td>795</td><td><a href='https://arxiv.org/abs/2608.30425'>Generative Models Enhanced by Sequence Labelling and Aspect-Code Switching Improve Cross-lingual Aspect-Based Sentiment Analysis</a></td><td>14</td><td>0</td><td>NLP</td><td>cross-lingual aspect-based 감성분석 성능 개선, incremental 기여임</td></tr>
<tr><td>796</td><td><a href='https://arxiv.org/abs/2608.30485'>Two Centuries of Sexism in British Parliament: A Computational Analysis of Women&#x27;s Representation in the Hansard Corpus</a></td><td>14</td><td>0</td><td>NLP</td><td>200년치 영국 의회 발언의 성차별 계산사회과학 분석임</td></tr>
<tr><td>797</td><td><a href='https://arxiv.org/abs/2608.30609'>Reading the News: Adapting Large Language Models to Swedish Journalism Through Continued Pre-Training</a></td><td>14</td><td>0</td><td>NLP</td><td>스웨덴어 저널리즘 도메인 continued pretraining 사례임</td></tr>
<tr><td>798</td><td><a href='https://arxiv.org/abs/2608.30754'>CLIN: an Objective Framework for Evaluating Creativity in Short Persian Literary Text</a></td><td>14</td><td>0</td><td>NLP</td><td>페르시아어 짧은 문학텍스트 창의성 평가 프레임워크임</td></tr>
<tr><td>799</td><td><a href='https://arxiv.org/abs/2608.30827'>Error-Type-Aware Loss Reweighting for Robust Named Entity Recognition with Noisy LLM Labels</a></td><td>14</td><td>0</td><td>NLP</td><td>NER에서 오류 유형별 loss reweighting 기법, 증분적 개선임</td></tr>
<tr><td>800</td><td><a href='https://arxiv.org/abs/2608.30842'>Thesis Proposal: Toward a Human-Centered and Perspective-Aware Framework for Reproducible ML Evaluation and AI Alignment</a></td><td>14</td><td>0</td><td>NLP</td><td>재현 가능한 ML 평가를 위한 인간 중심 프레임워크 제안하는 학위논문 제안서임</td></tr>
<tr><td>801</td><td><a href='https://arxiv.org/abs/2608.30853'>Linguistic Distance Segregates Latent Representations in Automatic Speech Recognition Systems</a></td><td>14</td><td>0</td><td>NLP</td><td>화자 모국어 거리와 ASR 오류율의 상관관계를 분석한 연구임</td></tr>
<tr><td>802</td><td><a href='https://arxiv.org/abs/2608.30873'>Personas Differ from Native-Language Generation: Language Pathways Shape LLM Interpersonal Advice</a></td><td>14</td><td>0</td><td>NLP</td><td>페르소나 프롬프팅과 원어 생성의 차이를 분석한 방법론 연구임</td></tr>
<tr><td>803</td><td><a href='https://arxiv.org/abs/2608.30884'>Evaluating and Mitigating Anti-LGBTQ Biases in German and Multilingual Language Models</a></td><td>14</td><td>0</td><td>NLP</td><td>독일어권 anti-LGBTQ 편향 벤치마크와 완화 실험임</td></tr>
<tr><td>804</td><td><a href='https://arxiv.org/abs/2608.30903'>MMDS-Bench: Benchmarking Multimodal Large Language Models on Dynamic Stance in Social Media Interactions</a></td><td>14</td><td>0</td><td>Multimodal</td><td>소셜미디어 부모-답글 관계의 동적 stance 분류 벤치마크임</td></tr>
<tr><td>805</td><td><a href='https://arxiv.org/abs/2608.30929'>Annotated Surrogate Retrieval for Polish Statutory Law</a></td><td>14</td><td>0</td><td>NLP</td><td>폴란드 법령 검색을 위한 surrogate annotation 기법 비교 연구임</td></tr>
<tr><td>806</td><td><a href='https://arxiv.org/abs/2608.31037'>Language-Statistical Analysis of Neural Audio Codec Tokens Across Architectures, Corpora, and Noise Conditions</a></td><td>14</td><td>0</td><td>NLP</td><td>신경 오디오 코덱 토큰의 언어통계적 특성 분석 연구임</td></tr>
<tr><td>807</td><td><a href='https://arxiv.org/abs/2608.31038'>Type-Balanced Contextual Learning for Incremental Named Entity Recognition</a></td><td>14</td><td>0</td><td>NLP</td><td>증분 NER에서 biased context 문제 해결하는 학습 기법임</td></tr>
<tr><td>808</td><td><a href='https://arxiv.org/abs/2608.31170'>Context-Aware Interleaved Batching for WhisperX</a></td><td>14</td><td>0</td><td>NLP</td><td>WhisperX의 배치 간 문맥 유지를 위한 interleaved batching 기법임</td></tr>
<tr><td>809</td><td><a href='https://arxiv.org/abs/2608.28607'>RegDivergence-101: An LLM Benchmark for Cross-Jurisdiction Regulatory Contradiction Detection in Life Sciences</a></td><td>14</td><td>0</td><td>NLP</td><td>제약 규제 문서 간 모순 탐지 벤치마크 및 baseline 비교임</td></tr>
<tr><td>810</td><td><a href='https://arxiv.org/abs/2608.28628'>CDEP Agent: Connecting Meteorologically Detected Temporal Compound Events to Real-World Documentary Evidence</a></td><td>14</td><td>0</td><td>AI</td><td>복합 가뭄-폭우 이벤트의 실측 문서화 여부를 검증하는 에이전트 연구임</td></tr>
<tr><td>811</td><td><a href='https://arxiv.org/abs/2608.28637'>AI Scientist Mission Control (AIMC): Visual Analytics for Human Oversight of Autonomous Scientific Discovery</a></td><td>14</td><td>0</td><td>AI</td><td>자율 과학 발견 시스템 산출물을 감시하는 visual analytics 도구임</td></tr>
<tr><td>812</td><td><a href='https://arxiv.org/abs/2608.28820'>Explainable Artificial Intelligence (XAI) in Computational Pathology: Definitions, Taxonomy, and Recommendations</a></td><td>14</td><td>0</td><td>CV</td><td>computational pathology용 XAI 분류체계와 권고안 리뷰 논문임</td></tr>
<tr><td>813</td><td><a href='https://arxiv.org/abs/2608.28968'>Efficient GPU Retrieval for Semantic Search</a></td><td>14</td><td>0</td><td>AI</td><td>대규모 시맨틱 검색을 위한 GPU 2단계 검색 아키텍처 산업 연구임</td></tr>
<tr><td>814</td><td><a href='https://arxiv.org/abs/2608.28640'>PromptKWS: A Novel Prompt-Guided Open-Vocabulary Keyword Spotting Framework</a></td><td>13</td><td>0</td><td>NLP</td><td>프롬프트 기반 오픈보캡 키워드 스포팅 프레임워크임 - 음성인식 응용으로 로보틱스와 무관함</td></tr>
<tr><td>815</td><td><a href='https://arxiv.org/abs/2608.28649'>Can Large Language Models Identify Meaningful Touchpoints in Conversion Attribution?</a></td><td>13</td><td>0</td><td>NLP</td><td>전환 기여도 분석에 LLM 활용 가능성 검토한 이커머스 응용 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>816</td><td><a href='https://arxiv.org/abs/2608.28667'>GreenBench: Benchmarking Energy Efficiency and Carbon Footprint of Open-Source LLM Inference on Apple Silicon</a></td><td>13</td><td>0</td><td>LG</td><td>Apple Silicon에서 LLM 추론 에너지효율 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>817</td><td><a href='https://arxiv.org/abs/2608.28916'>VoiceCodeBench: Evaluating Exact Structured-Token Recovery in Automatic Speech Recognition</a></td><td>13</td><td>0</td><td>NLP</td><td>ASR의 구조화 토큰(식별자·수치) 정확 복원 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>818</td><td><a href='https://arxiv.org/abs/2608.28646'>BiasMix-Finance: Post-Generation KYC Guardrails for LLM Portfolio Advice</a></td><td>13</td><td>0</td><td>AI</td><td>LLM 포트폴리오 추천의 KYC 위반을 사후 보정하는 가드레일 파이프라인임</td></tr>
<tr><td>819</td><td><a href='https://arxiv.org/abs/2608.28728'>PermitGPT: A Unified Generative-AI Pipeline for Construction Hazard Forecasting, Permit Prediction, and Community Impact</a></td><td>13</td><td>0</td><td>AI</td><td>건설 허가 데이터를 구조화해 위험·규제 예측하는 생성형 파이프라인임</td></tr>
<tr><td>820</td><td><a href='https://arxiv.org/abs/2608.28824'>Discovering Machine Correlates of Consciousness</a></td><td>13</td><td>0</td><td>AI</td><td>LLM의 하드웨어 이상 신호로 machine correlates of consciousness를 탐색한 사변적 연구임</td></tr>
<tr><td>821</td><td><a href='https://arxiv.org/abs/2608.28663'>Open-Set Cattle Muzzle Identification: A Leakage-Controlled Benchmark and Evaluation Protocol</a></td><td>12</td><td>0</td><td>CV</td><td>가축 개체 식별 벤치마크임. 로봇 지능과 무관함</td></tr>
<tr><td>822</td><td><a href='https://arxiv.org/abs/2608.28608'>NLP-Driven Knowledge Extraction and Thematic Classification of Translated Ancient Indian Medical Texts</a></td><td>12</td><td>0</td><td>NLP</td><td>고대 인도 의학 문헌에 NER·토픽모델링·지식그래프 적용한 응용 논문임 - 로보틱스와 무관하고 방법론도 기존 도구 조합 수준임</td></tr>
<tr><td>823</td><td><a href='https://arxiv.org/abs/2608.28611'>Gurukul AI: An Interactive AI-Driven Educational Platform for Indian Education System</a></td><td>12</td><td>0</td><td>NLP</td><td>인도 교육과정에 맞춘 RAG 챗봇 배포 논문임 - 순수 교육 응용으로 로보틱스 연관성 없음</td></tr>
<tr><td>824</td><td><a href='https://arxiv.org/abs/2608.28633'>PAUSE: Editable Strategy Artifacts for Long-Form Cultural Story Adaptation</a></td><td>12</td><td>0</td><td>NLP</td><td>장편 소설의 문화적 각색 전략을 편집 가능하게 만든 연구임 - 로보틱스와 전혀 무관함</td></tr>
<tr><td>825</td><td><a href='https://arxiv.org/abs/2608.28645'>Cross Lingual Transfer in Tulu Legal Comprehension: Script-Dependent Improvement and RAG-Induced Knowledge Conflict</a></td><td>12</td><td>0</td><td>NLP</td><td>저자원 Dravidian 언어 법률 이해 cross-lingual transfer 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>826</td><td><a href='https://arxiv.org/abs/2608.28926'>Leveraging Turn-taking Dynamics for Intent Recognition in Multi-party Conversations</a></td><td>12</td><td>0</td><td>NLP</td><td>멀티파티 대화에서 턴테이킹 다이내믹스로 의도인식 보조한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>827</td><td><a href='https://arxiv.org/abs/2608.28932'>VocalAffectBench: Evaluating Vocal Emotion Recognition in AI Audio Models</a></td><td>12</td><td>0</td><td>NLP</td><td>음성 감정인식 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>828</td><td><a href='https://arxiv.org/abs/2608.29066'>Not All or None: Dynamic Construction of Target-aware Memory Graph for Conversational Stance Detection</a></td><td>12</td><td>0</td><td>NLP</td><td>대화형 스탠스 탐지에 타겟 인지 메모리 그래프 도입한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>829</td><td><a href='https://arxiv.org/abs/2608.29133'>AI Historian: Helping historians organize and verify person-centred temporal clues from dispersed historical narratives</a></td><td>12</td><td>0</td><td>NLP</td><td>역사 문헌의 인물-시간 단서를 정리하는 에이전트 시스템임 - 로보틱스와 무관함</td></tr>
<tr><td>830</td><td><a href='https://arxiv.org/abs/2608.29209'>Toward Cultural Alignment: Human-Centered Evaluation of Multimodal AI Stories Across Five African Communities</a></td><td>12</td><td>0</td><td>NLP</td><td>아프리카 5개 커뮤니티 대상 AI 생성 스토리 문화정합성 평가임 - 로보틱스와 무관함</td></tr>
<tr><td>831</td><td><a href='https://arxiv.org/abs/2608.29239'>Anchoring Speech with Semantics: A Multimodal Adapter Mechanism for Automatic Speech Recognition in Low-Resource Languages</a></td><td>12</td><td>0</td><td>NLP</td><td>저자원 언어 ASR에 번역기반 semantic anchor를 추가한 어댑터임 - 로보틱스와 무관함</td></tr>
<tr><td>832</td><td><a href='https://arxiv.org/abs/2608.29284'>Cloud and On-Premises Deployment of Uzbek Legal RAG via Targeted Retriever Fine-Tuning</a></td><td>12</td><td>0</td><td>NLP</td><td>우즈베크어 법률 RAG 클라우드/온프레미스 배포 사례 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>833</td><td><a href='https://arxiv.org/abs/2608.29477'>MUDDLE: Measuring Understanding of Documents under Distractor and Length Effects</a></td><td>12</td><td>0</td><td>NLP</td><td>문서QA에서 distractor와 길이효과를 분리한 통제 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>834</td><td><a href='https://arxiv.org/abs/2608.29564'>TACS: Trajectory-Aware Candidate Selection for LLM Jailbreak Suffix Optimization</a></td><td>12</td><td>0</td><td>NLP</td><td>탈옥 접미사 최적화에서 후보선택 단계의 근시안적 선택을 개선한 연구임 - 보안 연구로 로보틱스와 무관함</td></tr>
<tr><td>835</td><td><a href='https://arxiv.org/abs/2608.29582'>SUP-MIMIC: A Multi-Task Clinical Diagnosis Benchmark for Evaluating LLMs&#x27; Robustness to Contradictory Evidence</a></td><td>12</td><td>0</td><td>NLP</td><td>임상진단 모순증거 강건성 평가 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>836</td><td><a href='https://arxiv.org/abs/2608.29613'>Cross-lingual Functional Vectors for Emotion Detection in Large Language Models</a></td><td>12</td><td>0</td><td>NLP</td><td>감정인식 태스크의 함수벡터 교차언어 전이 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>837</td><td><a href='https://arxiv.org/abs/2608.29662'>ACTD: Anchor-Based Cross-Tokenizer Distillation with Residual Regularization</a></td><td>12</td><td>0</td><td>LG</td><td>토크나이저가 다른 모델간 지식증류 앵커기법임 - 로보틱스와 무관함</td></tr>
<tr><td>838</td><td><a href='https://arxiv.org/abs/2608.29738'>Evaluating the Capabilities of LLMs for Persuasive Dialogue</a></td><td>12</td><td>0</td><td>NLP</td><td>LLM의 논증적 설득력을 정식 논증이론으로 평가한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>839</td><td><a href='https://arxiv.org/abs/2608.29790'>HiVe: Beyond Static Prompts for Multitask Learning via Hierarchy-based Vertical Mixture-of-Experts</a></td><td>12</td><td>0</td><td>LG</td><td>계층적 프롬프트 튜닝에 vertical MoE를 결합한 멀티태스크 학습법임 - 로보틱스와 무관함</td></tr>
<tr><td>840</td><td><a href='https://arxiv.org/abs/2608.29831'>A^2Agent: Action-Aware Reinforcement Learning for Repository-Level Code Localization Agents</a></td><td>12</td><td>0</td><td>NLP</td><td>레포지토리 레벨 코드 위치추정 액션인지 RL 에이전트임 - 소프트웨어공학 응용으로 로보틱스와 무관함</td></tr>
<tr><td>841</td><td><a href='https://arxiv.org/abs/2608.29835'>EVAR: Evidence-Validated Hypothesis Admission for Budget-Aware Narrative Reasoning</a></td><td>12</td><td>0</td><td>NLP</td><td>장문 서사 추론에서 근거검증된 가설만 채택하는 프레임워크임 - 로보틱스와 무관함</td></tr>
<tr><td>842</td><td><a href='https://arxiv.org/abs/2608.29856'>GenRubric: Self-Evolving Rubric Generation for Scalable LLM Evaluation</a></td><td>12</td><td>0</td><td>NLP</td><td>LLM 평가용 루브릭 자기진화 생성 프레임워크임 - 로보틱스와 무관함</td></tr>
<tr><td>843</td><td><a href='https://arxiv.org/abs/2608.29899'>REIGN: Refurbished Embeddings with Integrated Guidance Networks for Efficient Context-Length Scaling</a></td><td>12</td><td>0</td><td>NLP</td><td>청크 임베딩 기반 저비용 장문서 검색 인코더임 - 로보틱스와 무관함</td></tr>
<tr><td>844</td><td><a href='https://arxiv.org/abs/2608.29921'>Sleight of Word Benchmark: Can Language Models Notice If Their Own Output Was Tampered With?</a></td><td>12</td><td>0</td><td>NLP</td><td>생성 중 단어치환에 대한 모델 자기인식을 측정한 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>845</td><td><a href='https://arxiv.org/abs/2608.29948'>XQDT: eXplainable and Quantitative Data-Text Alignment Metric with Feedback Signals</a></td><td>12</td><td>0</td><td>NLP</td><td>데이터-텍스트 정합성 설명가능 평가지표임 - 로보틱스와 무관함</td></tr>
<tr><td>846</td><td><a href='https://arxiv.org/abs/2608.30086'>When Does a Classifier Help an LLM? Classifier-Guided Prompting and Hybrid Classifier-LLM Models for Credit-Default Prediction</a></td><td>12</td><td>0</td><td>LG</td><td>신용평가에서 분류기와 LLM 결합 방식을 비교한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>847</td><td><a href='https://arxiv.org/abs/2608.30107'>AtlasNLP: A Country-Aware Atlas of Dataset Representation in NLP</a></td><td>12</td><td>0</td><td>NLP</td><td>NLP 데이터셋의 국가별 대표성을 지도화한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>848</td><td><a href='https://arxiv.org/abs/2608.30156'>Reactivating Test-Time Scaling for Plane Geometry Problem Solving</a></td><td>12</td><td>0</td><td>Multimodal</td><td>평면기하 문제풀이에 test-time scaling을 재활성화한 연구임 - 수학 도메인 한정으로 로보틱스와 무관함</td></tr>
<tr><td>849</td><td><a href='https://arxiv.org/abs/2608.30188'>GPAgentBench-2K: Benchmarking Large Language Model Agents in Complex Clinical Action Space</a></td><td>12</td><td>0</td><td>NLP</td><td>1차진료 임상 에이전트의 제약된 의사결정 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>850</td><td><a href='https://arxiv.org/abs/2608.30828'>Opinionated, Hesitant and Stressed: Three Studies of How Politicians Speak in Four Slavic Parliaments</a></td><td>12</td><td>0</td><td>NLP</td><td>슬라브어권 의회 발언의 음향·정치수사 대규모 연구임</td></tr>
<tr><td>851</td><td><a href='https://arxiv.org/abs/2608.30866'>Beyond Good Intentions: When Does the Framing of Multilingual and Low-Resource NLP Research Become a Caricature?</a></td><td>12</td><td>0</td><td>NLP</td><td>저자원 언어 NLP 연구의 서사적 프레이밍을 비평하는 메타 연구임</td></tr>
<tr><td>852</td><td><a href='https://arxiv.org/abs/2608.28601'>Leveraging Generative AI to Design Accessible Interactive Visualizations for Undergraduate Mathematics: A Six-Phase Workflow</a></td><td>12</td><td>0</td><td>AI</td><td>GenAI로 대학 수학 접근성 시각화 도구를 만드는 워크플로우 사례임</td></tr>
<tr><td>853</td><td><a href='https://arxiv.org/abs/2608.28965'>From Location Phrases to Geographic Entities: Task-Adapted Retrieval for People Search</a></td><td>12</td><td>0</td><td>AI</td><td>인물 검색용 지명구를 지리 엔티티로 매핑하는 검색 시스템임</td></tr>
<tr><td>854</td><td><a href='https://arxiv.org/abs/2608.28676'>Automated pipeline for herbarium label digitization</a></td><td>10</td><td>0</td><td>NLP</td><td>표본 라벨 디지털화 파이프라인임. 로봇 지능과 무관함</td></tr>
<tr><td>855</td><td><a href='https://arxiv.org/abs/2608.28680'>Multi-Sensor Mapping of Vulnerable Urban Settlements Using SAR, Multispectral, and Hyperspectral Imagery: A Case Study in Córdoba, Argentina</a></td><td>10</td><td>0</td><td>CV</td><td>위성 다중센서로 빈민가 매핑하는 원격탐사 응용임. 로봇과 무관함</td></tr>
<tr><td>856</td><td><a href='https://arxiv.org/abs/2608.28777'>FairReL: Deepfake Detection using Fairness-Aware Representation Learning</a></td><td>10</td><td>0</td><td>CV</td><td>딥페이크 탐지의 인구통계 편향 완화 기법임. 로봇과 무관함</td></tr>
<tr><td>857</td><td><a href='https://arxiv.org/abs/2608.28798'>Blind Stereoscopic Omnidirectional Image Quality Assessment Using Predictive Coding Hierarchy</a></td><td>10</td><td>0</td><td>CV</td><td>스테레오 파노라마 이미지 품질 평가 지표임. 로봇과 무관함</td></tr>
<tr><td>858</td><td><a href='https://arxiv.org/abs/2608.28802'>A Large-scale Evaluation of Text-guided Models for Facial Editing</a></td><td>10</td><td>0</td><td>CV</td><td>텍스트 기반 얼굴 편집 모델 대규모 평가임. 로봇과 무관함</td></tr>
<tr><td>859</td><td><a href='https://arxiv.org/abs/2608.28874'>MWIR-4-Plastic: The Identification of Complex End-of-Life Industrial Plastic using Mid-wave Infrared Hyperspectral Imaging and Machine Learning</a></td><td>10</td><td>0</td><td>CV</td><td>폐플라스틱 분류용 초분광 이미징 데이터셋임. 로봇과 무관함</td></tr>
<tr><td>860</td><td><a href='https://arxiv.org/abs/2608.29016'>Towards Fully Automated Medical Imaging Code Generation via Validation-based Context Engineering</a></td><td>10</td><td>0</td><td>CV</td><td>의료영상 처리 코드를 자동 생성하는 멀티에이전트 프레임워크임. 로봇과 무관함</td></tr>
<tr><td>861</td><td><a href='https://arxiv.org/abs/2608.29038'>sRGB Real Noise Modeling via Noise-Aware Sampling with Normalizing Flows</a></td><td>10</td><td>0</td><td>CV</td><td>sRGB 노이즈를 normalizing flow로 모델링하는 denoising 연구임. 로봇과 무관함</td></tr>
<tr><td>862</td><td><a href='https://arxiv.org/abs/2608.29153'>SGRNet: Spatially Guided Radiology Network for Structured Radiological Reporting of Head and Neck Cancer</a></td><td>10</td><td>0</td><td>CV</td><td>두경부암 CT 구조화 판독 보고서 생성임. 의료영상 특화라 로봇과 무관함</td></tr>
<tr><td>863</td><td><a href='https://arxiv.org/abs/2608.29162'>Subtraction-Based Tumor Segmentation and Lesion-Centered pCR Prediction for the MAMA-MIA Challenge</a></td><td>10</td><td>0</td><td>CV</td><td>유방암 MRI 종양 분할·pCR 예측 챌린지 제출 논문임. 로봇과 무관함</td></tr>
<tr><td>864</td><td><a href='https://arxiv.org/abs/2608.29172'>A Tensor Variational Formulation of Gradient Energy Total Variation</a></td><td>10</td><td>0</td><td>CV</td><td>gradient energy tensor 기반 total variation 변분 공식 제안임. 고전적 디노이징 이론 연구임</td></tr>
<tr><td>865</td><td><a href='https://arxiv.org/abs/2608.29196'>Bayesian-Optimized Superpixel-GrabCut for Traceable Optic Disc Segmentation</a></td><td>10</td><td>0</td><td>CV</td><td>시신경 유두 분할용 베이지안 최적화 GrabCut 파이프라인임. 로봇과 무관함</td></tr>
<tr><td>866</td><td><a href='https://arxiv.org/abs/2608.29227'>Using Channel Representations in Regularization Terms: A Case Study on Image Diffusion</a></td><td>10</td><td>0</td><td>CV</td><td>채널 표현 기반 비선형 diffusion 필터링 이론임. 로봇과 무관함</td></tr>
<tr><td>867</td><td><a href='https://arxiv.org/abs/2608.29253'>QCell: Recombining and Aligning Cell Queries for Overlapping Instance Segmentation</a></td><td>10</td><td>0</td><td>CV</td><td>현미경 겹친 세포 인스턴스 분할 기법임. 로봇과 무관함</td></tr>
<tr><td>868</td><td><a href='https://arxiv.org/abs/2608.29289'>AOI-Net: Structural Face AOI-Guided Eye-Gaze Track Representation Learning for Autism Spectrum Disorder Detection</a></td><td>10</td><td>0</td><td>CV</td><td>자폐 스펙트럼 선별용 시선추적 표현학습 연구임. 로봇과 무관함</td></tr>
<tr><td>869</td><td><a href='https://arxiv.org/abs/2608.29331'>Neural video codecs quality assessment dataset and benchmark</a></td><td>10</td><td>0</td><td>Video</td><td>신경 비디오 코덱 품질평가 데이터셋임. 로봇과 무관함</td></tr>
<tr><td>870</td><td><a href='https://arxiv.org/abs/2608.29364'>Sketch2Inspire: Structure-Sensitive Evaluation for Product Retrieval</a></td><td>10</td><td>0</td><td>Multimodal</td><td>제품 디자인용 스케치-텍스트 검색 평가 자원임. 로봇과 무관함</td></tr>
<tr><td>871</td><td><a href='https://arxiv.org/abs/2608.29384'>FiLM-GPNet: Geometry-Aware Pseudo-Supervised Phase Restoration with Zero-Shot Generalization for Large Temporal InSAR Stacks</a></td><td>10</td><td>0</td><td>CV</td><td>InSAR 위상 복원용 기하 조건부 네트워크임. 원격탐사 응용이라 로봇과 무관함</td></tr>
<tr><td>872</td><td><a href='https://arxiv.org/abs/2608.29540'>NepScript Genesis: Neural Architecture Search for Handwritten Devanagari Digit Synthesis</a></td><td>10</td><td>0</td><td>Generative</td><td>네와리 문자 손글씨 숫자 생성용 NAS 프레임워크임. 로봇과 무관함</td></tr>
<tr><td>873</td><td><a href='https://arxiv.org/abs/2608.29590'>Guardrail-Agnostic Societal Bias Evaluation in Large Vision-Language Models</a></td><td>10</td><td>0</td><td>Multimodal</td><td>가드레일이 있는 LVLM의 사회적 편향 평가 기법임. 로봇과 무관함</td></tr>
<tr><td>874</td><td><a href='https://arxiv.org/abs/2608.29644'>Conducting Stylistic Analysis of Paintings through an Art-History Agent</a></td><td>10</td><td>0</td><td>Multimodal</td><td>회화 양식 분석을 자동화하는 미술사 에이전트임. 로봇과 무관함</td></tr>
<tr><td>875</td><td><a href='https://arxiv.org/abs/2608.29663'>PhysVR: Vision-Language Model Guided Interference-aware Temporal Feature Refinement for Remote Physiological Measurement</a></td><td>10</td><td>0</td><td>CV</td><td>VLM 유도 원격 생체신호(rPPG) 측정 잡음 제거 기법임. 로봇과 무관함</td></tr>
<tr><td>876</td><td><a href='https://arxiv.org/abs/2608.29677'>MedSegBenchmarker: A Raw-Count-First Framework for Controlled 2D Medical Image Segmentation Benchmarks</a></td><td>10</td><td>0</td><td>CV</td><td>2D 의료영상 분할 벤치마킹 프레임워크임. 로봇과 무관함</td></tr>
<tr><td>877</td><td><a href='https://arxiv.org/abs/2608.29739'>Drift Calibration in Geometric Eye Tracking Systems</a></td><td>10</td><td>0</td><td>CV</td><td>기하학적 시선추적기의 드리프트 캘리브레이션 데이터셋임. 로봇과 무관함</td></tr>
<tr><td>878</td><td><a href='https://arxiv.org/abs/2608.29802'>Foundation and Multimodal Large Language Models for Face Presentation and Morph Attack Detection</a></td><td>10</td><td>0</td><td>CV</td><td>얼굴 위변조·모핑 공격 탐지에 foundation model을 적용한 연구임. 로봇과 무관함</td></tr>
<tr><td>879</td><td><a href='https://arxiv.org/abs/2608.29804'>Beyond Global Realism: Virtual Try-On Evaluation and Optimization with Dimension-wise Garment Fidelity Assessment</a></td><td>10</td><td>0</td><td>Generative</td><td>가상 피팅의 의류 충실도 다차원 평가 프레임워크임. 로봇과 무관함</td></tr>
<tr><td>880</td><td><a href='https://arxiv.org/abs/2608.29820'>Null-Space Diffusion Restoration with Adaptive Uncertainty-Guided Fusion for Ultrasound Speckle Reduction</a></td><td>10</td><td>0</td><td>CV</td><td>초음파 스펙클 노이즈 제거용 null-space diffusion 기법임. 의료영상 특화라 로봇과 무관함</td></tr>
<tr><td>881</td><td><a href='https://arxiv.org/abs/2608.29847'>ContextBias: Controlled Evaluation of Bias Persistence Under Context Shift in Text-to-Image Models</a></td><td>10</td><td>0</td><td>Multimodal</td><td>text-to-image 모델의 맥락 이동에 따른 직업 편향 지속성 평가임. 로봇과 무관함</td></tr>
<tr><td>882</td><td><a href='https://arxiv.org/abs/2608.29925'>Dior: Drawing the Light of Image via Material-Decoupled Illumination Representation</a></td><td>10</td><td>0</td><td>Generative</td><td>손그림 스크리블로 이미지 재조명하는 편집 도구임. 로봇과 무관함</td></tr>
<tr><td>883</td><td><a href='https://arxiv.org/abs/2608.29944'>On the Role of MRI Sequences in Cross-Dataset Generalization for Brain Tumor Segmentation</a></td><td>10</td><td>0</td><td>CV</td><td>MRI 시퀀스별 뇌종양 분할 교차 데이터셋 일반화 분석임. 로봇과 무관함</td></tr>
<tr><td>884</td><td><a href='https://arxiv.org/abs/2608.29970'>Confidence-Aware Ensemble and Long-Word Refinement for Artistic Text Recognition</a></td><td>10</td><td>0</td><td>CV</td><td>예술적 텍스트 인식 앙상블·긴 단어 보정 기법임. 로봇과 무관함</td></tr>
<tr><td>885</td><td><a href='https://arxiv.org/abs/2608.30087'>The Nearest Target Is the Wrong One: Target Separation in Arc2Face Identity Unlearning</a></td><td>10</td><td>0</td><td>Generative</td><td>얼굴 조건부 생성모델의 정체성 unlearning 타겟 분리 연구임. 로봇과 무관함</td></tr>
<tr><td>886</td><td><a href='https://arxiv.org/abs/2608.30143'>Repeatability Characterisation and Error Budget of a Consumer Structured-Light Scanner for 3-D Wound Geometry:A Rigid-Phantom Study</a></td><td>10</td><td>0</td><td>CV</td><td>상처 3D 형상 측정용 구조광 스캐너 반복성 분석임. 로봇과 무관함</td></tr>
<tr><td>887</td><td><a href='https://arxiv.org/abs/2608.30161'>AI-enabled Low-Cost 3D Maize Ear Morphometry Platform at Breeding Scale</a></td><td>10</td><td>0</td><td>CV</td><td>저비용 옥수수 이삭 3D 형태측정 파이프라인임. 로봇과 무관함</td></tr>
<tr><td>888</td><td><a href='https://arxiv.org/abs/2608.30213'>Towards a Joint Khmer Text Recognition and Word Segmentation</a></td><td>10</td><td>0</td><td>NLP</td><td>크메르어 텍스트 인식·단어 분할 통합 모델임. 로봇과 무관함</td></tr>
<tr><td>889</td><td><a href='https://arxiv.org/abs/2608.28776'>Evaluating Multilingual Sentence Embeddings for Translation Error Detection:An English--Greek Contrastive Study</a></td><td>10</td><td>0</td><td>NLP</td><td>영어-그리스어 번역 오류 탐지에 다국어 임베딩 민감도 평가한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>890</td><td><a href='https://arxiv.org/abs/2608.28875'>No Detectable Change in Side-Level WER from Prompt-Level Context: A Preregistered Ablation on a Production Oral-History Corpus</a></td><td>10</td><td>0</td><td>NLP</td><td>프롬프트 컨텍스트가 ASR WER에 미치는 효과를 사전등록 연구로 검증한 논문임 - 로보틱스와 무관함</td></tr>
<tr><td>891</td><td><a href='https://arxiv.org/abs/2608.28986'>Detecting and Guiding LLM-Generated Korean Poetry with Interpretable Form-level Features</a></td><td>10</td><td>0</td><td>NLP</td><td>한국어 시 LLM 생성여부 탐지·가이드 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>892</td><td><a href='https://arxiv.org/abs/2608.29170'>Toward a Cross-Lingual Romanization Ecosystem for Sinitic Languages: A Paired Mandarin-Cantonese Case Study</a></td><td>10</td><td>0</td><td>NLP</td><td>시닉어족 로마자 표기 생태계 설계 논문임 - 로보틱스와 무관함</td></tr>
<tr><td>893</td><td><a href='https://arxiv.org/abs/2608.29324'>Padārtha: Ontology-Grounded Fine-Grained NER Benchmark for Classical Sanskrit</a></td><td>10</td><td>0</td><td>NLP</td><td>산스크리트 고전문헌 온톨로지 기반 NER 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>894</td><td><a href='https://arxiv.org/abs/2608.29326'>StageWell: A Process-Aligned Chinese Corpus for Positive-Psychology Support Dialogue</a></td><td>10</td><td>0</td><td>NLP</td><td>중국어 긍정심리 지지대화 코퍼스·프로토콜임 - 로보틱스와 무관함</td></tr>
<tr><td>895</td><td><a href='https://arxiv.org/abs/2608.29378'>Arabic Safety Alignment as Selective Refusal: An Empirical Study of SFT, DPO, and Guard Calibration</a></td><td>10</td><td>0</td><td>NLP</td><td>아랍어 안전정렬의 SFT/DPO/가드 캘리브레이션 실증 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>896</td><td><a href='https://arxiv.org/abs/2608.29446'>Whose Assessment of Distress? Community Perspectives and LLM Alignment on Well-Being Posts</a></td><td>10</td><td>0</td><td>NLP</td><td>커뮤니티별 심리적 고통 판단 기준과 LLM 정렬 차이를 조사한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>897</td><td><a href='https://arxiv.org/abs/2608.29481'>SIC-Agents: Benchmarking and Building an Adaptive Simulator for Pediatric Serious Illness Communication Training</a></td><td>10</td><td>0</td><td>NLP</td><td>소아 중증질환 커뮤니케이션 훈련용 시뮬레이터·벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>898</td><td><a href='https://arxiv.org/abs/2608.29492'>CoCoA: Context-Conditional Cultural Alignment for Large Language Models</a></td><td>10</td><td>0</td><td>NLP</td><td>문맥조건부 문화편향 완화 학습 프레임워크임 - 로보틱스와 무관함</td></tr>
<tr><td>899</td><td><a href='https://arxiv.org/abs/2608.29526'>Ontology-Guided Multi-Agent Extraction of Evaluation Objects from Academic Review Texts: Evidence from Chinese Library and Information Science</a></td><td>10</td><td>0</td><td>NLP</td><td>중국 도서정보학 학술리뷰에서 평가대상 추출하는 온톨로지 기반 멀티에이전트임 - 로보틱스와 무관함</td></tr>
<tr><td>900</td><td><a href='https://arxiv.org/abs/2608.29543'>Evaluating LLMs on Conversational Text-to-SQL under Chain Ambiguity and Intent Drift</a></td><td>10</td><td>0</td><td>NLP</td><td>대화형 text-to-SQL의 체인모호성·의도전환 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>901</td><td><a href='https://arxiv.org/abs/2608.29575'>SemTrace: Source-Grounded Semantic Signatures for Tracing LLM Exposure to Protected Documents</a></td><td>10</td><td>0</td><td>NLP</td><td>보호문서 노출 추적용 의미 워터마크 기법임 - 로보틱스와 무관함</td></tr>
<tr><td>902</td><td><a href='https://arxiv.org/abs/2608.29616'>JPO: Juris Policy Optimization for Structured Legal Reasoning in Criminal Judgment Prediction</a></td><td>10</td><td>0</td><td>NLP</td><td>중국 형사판결 예측용 구조화 법률추론 강화학습임 - 로보틱스와 무관함</td></tr>
<tr><td>903</td><td><a href='https://arxiv.org/abs/2608.29624'>PrivBench: A Holistic and Modular Benchmarking Platform for Evaluating Text-to-Text Privatization</a></td><td>10</td><td>0</td><td>NLP</td><td>텍스트 프라이버시화 평가 플랫폼임 - 로보틱스와 무관함</td></tr>
<tr><td>904</td><td><a href='https://arxiv.org/abs/2608.29711'>DVBench: Benchmarking MLLMs for Understanding Dynamic Charts and Narratives in Data Videos</a></td><td>10</td><td>0</td><td>NLP</td><td>동적 차트·내러티브 이해 MLLM 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>905</td><td><a href='https://arxiv.org/abs/2608.29798'>R$^2$A: Learning Persona Policies Through Persona Representation Learning and Runtime Alignment</a></td><td>10</td><td>0</td><td>NLP</td><td>페르소나 행동을 선택/실현으로 나눠 학습하는 프레임워크임 - 로보틱스와 무관함</td></tr>
<tr><td>906</td><td><a href='https://arxiv.org/abs/2608.29865'>ManGo: Manga Active Narrative Grounding Optimization</a></td><td>10</td><td>0</td><td>NLP</td><td>만화 패널 단위 능동적 근거탐색 VQA 프레임워크임 - 로보틱스와 무관함</td></tr>
<tr><td>907</td><td><a href='https://arxiv.org/abs/2608.29884'>Improving Argument Saliency Coverage in Small LLMs for Long Legal Opinion Summarization via Sequence-Level Distillation</a></td><td>10</td><td>0</td><td>NLP</td><td>장문 법률 의견 요약의 논지 커버리지를 증류로 개선한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>908</td><td><a href='https://arxiv.org/abs/2608.29889'>VibeJam: A User Study Platform for Web Development with Agents</a></td><td>10</td><td>0</td><td>NLP</td><td>AI 에이전트와 협업하는 웹개발 사용자연구 플랫폼임 - 로보틱스와 무관함</td></tr>
<tr><td>909</td><td><a href='https://arxiv.org/abs/2608.29890'>En-ViMedNER: An English-Vietnamese Parallel Biomedical Corpus with UMLS Semantic Type Annotations</a></td><td>10</td><td>0</td><td>NLP</td><td>영어-베트남어 병렬 생의학 NER 코퍼스임 - 로보틱스와 무관함</td></tr>
<tr><td>910</td><td><a href='https://arxiv.org/abs/2608.29903'>When Less is More: Understanding When Token Filtering Helps and Fails in AI-generated Text Detection</a></td><td>10</td><td>0</td><td>NLP</td><td>AI 생성 텍스트 탐지에서 토큰 필터링 효과를 분석한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>911</td><td><a href='https://arxiv.org/abs/2608.29919'>IndicDetect: Evaluating Cross-Lingual LLM-Generated Text Detection for Hindi, Telugu, and Tamil</a></td><td>10</td><td>0</td><td>NLP</td><td>인도 3개 언어 AI 생성 텍스트 탐지 강건성 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>912</td><td><a href='https://arxiv.org/abs/2608.29930'>Token Counts Are Not Model Lineage: A Frozen-Threshold Holdout Study of Black-Box LLM API Fingerprinting</a></td><td>10</td><td>0</td><td>NLP</td><td>토큰수 기반 API 모델 계열 지문인식의 유효성을 홀드아웃 검증한 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>913</td><td><a href='https://arxiv.org/abs/2608.29959'>Generative vs. Encoder Models for Multilingual NER: A Comprehensive Empirical Study on Naamapadam</a></td><td>10</td><td>0</td><td>NLP</td><td>인도 11개 언어 NER에서 인코더가 생성모델을 능가함을 보인 실증 비교임 - 로보틱스와 무관함</td></tr>
<tr><td>914</td><td><a href='https://arxiv.org/abs/2608.29995'>Generating Clinical Vignettes that Preserve Cognitive Formulations</a></td><td>10</td><td>0</td><td>NLP</td><td>인지모델을 보존하는 임상 사례 생성 프레임워크임 - 로보틱스와 무관함</td></tr>
<tr><td>915</td><td><a href='https://arxiv.org/abs/2608.30033'>&quot;Act Like a 5th Grader&quot; is Not Enough: Bounding Knowledge in LLM-Based User Simulators</a></td><td>10</td><td>0</td><td>NLP</td><td>초등학생 독해력 시뮬레이션에 인지적 제약을 건 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>916</td><td><a href='https://arxiv.org/abs/2608.30092'>Arkios: An Open Bilingual English-Nepali Language Model Trained From Scratch, with a Devanagari-Aware Tokenizer</a></td><td>10</td><td>0</td><td>NLP</td><td>영어-네팔어 이중언어 소형 LM을 처음부터 학습시킨 논문임 - 로보틱스와 무관함</td></tr>
<tr><td>917</td><td><a href='https://arxiv.org/abs/2608.30110'>Can LLMs Take the Pulse of the Economy? A Real-Time Evaluation of LLM Nowcasts on Macroeconomic Indicators</a></td><td>10</td><td>0</td><td>NLP</td><td>LLM 에이전트의 실시간 거시경제 지표 예측 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>918</td><td><a href='https://arxiv.org/abs/2608.29008'>Multi-Step Forecasting of Grape Berry Temperature based on LSTM Model with Feed-Forward Attention</a></td><td>10</td><td>0</td><td>AI</td><td>포도알 온도 다단계 예측용 attention-LSTM 모델임</td></tr>
<tr><td>919</td><td><a href='https://arxiv.org/abs/2608.28671'>Measuring Similarity between Artistic and AI Generated Images using Siamese Neural Networks</a></td><td>8</td><td>0</td><td>CV</td><td>AI 생성 이미지와 원작 유사도 측정하는 Siamese network임. 로봇 지능과 완전히 무관함</td></tr>
<tr><td>920</td><td><a href='https://arxiv.org/abs/2608.28674'>Multi-exposure HDR Imaging: A Review of Pixel-level and Feature-level Reconstruction Methods</a></td><td>8</td><td>0</td><td>CV</td><td>HDR 이미징 서베이 논문임. 로봇 지능과 무관함</td></tr>
<tr><td>921</td><td><a href='https://arxiv.org/abs/2608.29164'>Mapping-Based Image Diffusion</a></td><td>8</td><td>0</td><td>CV</td><td>텐서 기반 변분 이미지 향상·디노이징 함수 제안임. 고전적 이미지처리 연구라 로봇과 무관함</td></tr>
<tr><td>922</td><td><a href='https://arxiv.org/abs/2608.29952'>How Prolific Sellers Self-Present: Dissecting the Communication Patterns of 1.6 Million Reverb Listings</a></td><td>8</td><td>0</td><td>NLP</td><td>온라인 악기 마켓플레이스 판매자 자기표현 언어패턴 분석임 - 로보틱스와 완전 무관함</td></tr>
<tr><td>923</td><td><a href='https://arxiv.org/abs/2608.29990'>Beyond Fluency: A Rubric-Based Benchmark for Evaluating Saudi Dialect and Cultural Competence in Large Language Models</a></td><td>8</td><td>0</td><td>NLP</td><td>사우디 방언·문화역량 루브릭 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>924</td><td><a href='https://arxiv.org/abs/2608.30065'>Pak3H: Evaluating the Cost of Cultural Mismatch in LLM Alignment with a Human-Contextualized Urdu Benchmark</a></td><td>8</td><td>0</td><td>NLP</td><td>우르두어 3H(도움/무해/정직) 정렬 벤치마크임 - 로보틱스와 무관함</td></tr>
<tr><td>925</td><td><a href='https://arxiv.org/abs/2608.30114'>Manacá-1B: An Open, Reproducible Brazilian-Portuguese Language Model and a Tokenizer-Aware, Paired Evaluation</a></td><td>8</td><td>0</td><td>NLP</td><td>브라질 포르투갈어 소형 언어모델 재현성 연구임 - 로보틱스와 무관함</td></tr>
<tr><td>926</td><td><a href='https://arxiv.org/abs/2608.29027'>Explainable Multi-Loss Distillation Framework for Efficient and Interpretable Shrimp Disease Text Classification</a></td><td>5</td><td>0</td><td>NLP</td><td>새우 질병 텍스트 분류 설명가능성 프레임워크임. 로봇과 완전히 무관함</td></tr>
<tr><td>927</td><td><a href='https://arxiv.org/abs/2608.29145'>STARLINC: Satellite Trail Artifact Removal using Inter-Frame Correlation</a></td><td>5</td><td>0</td><td>CV</td><td>천문 관측 위성 궤적 아티팩트 제거 기법임. 로봇과 무관함</td></tr>
</tbody></table>

</details>
