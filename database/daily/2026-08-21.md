# 오늘의 arXiv Top 15 — 2026-08-21 (금)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**
> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)

**신규 논문 수: 전체 269편 → 중복 제거 후 269편 (이번 평가 대상 269편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 66 |
| cs.LG | 65 |
| cs.RO | 27 |
| cs.CL | 49 |
| cs.AI | 62 |

*1차 스크리닝: 전체 269편을 제목/초록 기반으로 채점(Claude (scheduled agent)) → 상위 15편은 arXiv 원문을 내려받아 정밀 리뷰(Claude (scheduled agent)) 후 최종 점수 산정.*

---

## Top 15

### 1. [70점] RoMAN-Flow: Taming Autoregressive Normalizing Flows for Offline Reinforcement Learning in Robotic Manipulation

- **분야**: Manipulation · **robotics relevance**: 10/10
- **arXiv**: [2608.20208](https://arxiv.org/abs/2608.20208) ([PDF](https://arxiv.org/pdf/2608.20208))
- **저자**: Shaoxuan Wang, Guangting Zheng, Rui Huang, Zhipeng Tang, Sha Zhang, Jiajun Deng, Yanyong Zhang
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 RoMAN-Flow는 autoregressive normalizing flow(AR-NF, SimFlow backbone)를 로봇 정책으로 사용하고, IQL 기반의 sampling-free advantage-weighted likelihood objective(NF-IQL)로 offline dataset action에 대해서만 policy improvement를 수행해 학습 중 순차적 샘플링을 회피한다. 이후 one-step distillation으로 배포 시 autoregressive inverse까지 제거해 LIBERO-Long 기준 8.55배 추론 가속을 달성하면서 MetaWorld-MT50, LIBERO, RoboMimic, real-robot 4개 벤치마크에서 IL 대비 대체로 성능을 유지하거나 개선했다.

**Core innovation & methodology**

- AR-NF(SimFlow backbone)를 조건부 정책으로 채택해 continuous action chunk를 Gaussian latent로 매핑하고, prefix-causal attention 기반 flow block의 forward pass만으로 exact conditional log-likelihood를 병렬 계산한다.
- NF-IQL: IQL의 advantage-weighted maximum-likelihood를 AR-NF에 적용하되, actor 업데이트를 offline dataset action에만 수행해 현재 policy에서의 action sampling(순차적 autoregressive inverse)을 완전히 배제한다.
- Chunk-level critic ensemble(M개)과 expectile regression 기반 state-value baseline으로 advantage A=Q̄-V를 계산하고, weight w=exp(βA)로 likelihood를 가중해 고가치 action의 likelihood를 높인다.
- One-step policy distillation: 고정된 NF-IQL teacher의 intermediate flow state와 최종 action chunk를 bidirectional Transformer student가 한 번의 forward pass로 근사하도록 data-induced distillation과 prior-sampled distillation을 결합해 학습한다.

**Novelty vs. prior works**

- Diffusion-QL, EDP, IDQL 등 기존 diffusion 기반 offline RL은 denoising surrogate·value guidance·sampling 기반 extraction으로 exact likelihood 계산을 우회하는 반면, RoMAN-Flow는 AR-NF가 제공하는 tractable exact likelihood를 IQL objective에 직접 대입한다는 점이 차별점이다.
- 가장 근접한 선행 연구인 SERNF(RealNVP+TD3+BC)와 비교하면, backbone을 표현력이 더 큰 SimFlow 기반 AR-NF로 교체하고 actor update를 TD3+BC 방식의 policy-sampling에서 sampling-free advantage-weighted likelihood(NF-IQL)로 대체한 것이 핵심 기여이며, RoboMimic MH에서 SERNF 대비 우위를 실증한다.
- One-step distillation 기법 자체는 FARMER, BiFlow의 image-domain 기법을 로봇 action-chunk 도메인으로 이전 적용한 것으로, 새로운 representation이나 objective라기보다는 IQL + AR-NF + one-step distillation의 기존 요소 조합을 로봇 policy에 처음 결합·검증한 응용적 novelty에 가깝다.

**Benchmark results**

- MetaWorld-MT50(50 tasks, 4 난이도 그룹 평균): IL 72.8% -> NF-IQL 81.1% -> One-Step 78.5%. NF-IQL은 online interaction을 사용하는 π0+Flow-SDE(78.1%)보다 3.0%p 높지만, RoMAN-Flow는 offline data만 사용한다는 차이가 있다.
- LIBERO(4 suites 평균): IL 93.5% -> NF-IQL 95.3%(LIBERO-Long에서 +6.6%p 기여) -> One-Step 93.7%. NF-IQL은 π0(94.2%), UniVLA-Full(~7.5B params, 95.2%) 등 비교군 중 최고 평균 성공률을 기록했다.
- RoboMimic MH: NF-IQL이 Lift 100%, Can 96%, Square 85%(SERNF TD3+BC는 91%/96%/68%)로 특히 Square에서 +17%p 우위를 보였다.
- Real-robot(Franka+XHand, 4 tasks): IL 57.3% -> NF-IQL 81.5%(+24.2%p), π0.5(71.8%) 대비 +9.7%p. 다만 One-Step 증류 모델은 69.5%로 NF-IQL teacher 대비 -12%p(약 85% 유지) 하락해, 시뮬레이션에서 저자가 강조한 'teacher 성능의 약 97% 유지'와는 대조적이며 본문에서 이 격차는 별도로 논의되지 않는다.
- Ablation(RoboMimic Square-MH): AR-NF actor capacity를 33.8M(S)에서 466.2M(L)까지 늘려도 성공률이 77~78%로 정체되고, 685.5M(XL)에서만 85%로 상승해 중소형 규모에서는 capacity scaling 효과가 제한적임을 보였다.
- Distillation 효율: LIBERO-Long(action horizon H=16)에서 action-chunk 생성 latency가 약 697ms에서 81.5ms로 감소해 8.55배 속도 향상을 얻었다.

**Top-tier conference 적합성 — 60/100 · 추천 venue: CoRL**

AR-NF를 로봇 정책으로 도입해 exact-likelihood offline RL(NF-IQL)과 one-step distillation을 결합한 완결성 있는 시스템형 논문으로, 4개 sim/real 벤치마크와 capacity ablation을 포함해 실험적 증거가 비교적 탄탄하다. 다만 핵심 구성요소가 각각 기존 방법(IQL, FARMER/BiFlow)의 직접적 적용에 가까워 conceptual leap은 제한적이고, real-world one-step distillation의 큰 성능 하락(81.5%→69.5%)이 명확히 분석되지 않은 점은 rejection risk로 작용할 수 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- NF-IQL의 sampling-free advantage-weighted likelihood objective는 diffusion/flow-matching 기반 VLA post-training에서 어려웠던 exact-likelihood offline RL을 가능케 하는 practical recipe로, 누리랩의 RL/IL 및 test-time optimization 연구에 참고할 수 있다.
- FARMER/BiFlow 방식의 intermediate-state alignment 기반 one-step distillation은 diffusion policy의 multi-step denoising 지연 문제에도 유사하게 적용 가능해, failure detection 이후 실시간 재계획(replanning)이 필요한 manipulation task의 inference 가속 아이디어로 활용할 수 있다.
- Real-world 평가에서 spatial out-of-distribution 조건을 명시적으로 포함한 프로토콜은 누리랩의 embodied spatial reasoning 및 generalization 관련 real-robot 평가 설계 시 참고할 만하다.

---

### 2. [66점] EXIMO: VLM Guided Exploration of VLA Policies

- **분야**: VLA · **robotics relevance**: 9/10
- **arXiv**: [2608.19891](https://arxiv.org/abs/2608.19891) ([PDF](https://arxiv.org/pdf/2608.19891))
- **저자**: Bhavya Sukhija, Oliver Groth, Mohit Shridhar, Tim Hertweck, Michael Bloesch, Markus Wulfmeier, Abbas Abdolmaleki, Martin Riedmiller
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 Eximo는 사전학습된 VLA(Gemini Robotics On-Device, GROD)를 VLM(Gemini)이 자연어로 orchestration하며 새로운 장기·조합·추론 task 데이터를 teleoperation 없이 수집하고, 이를 SFT로 distill한 뒤 residual off-policy RL(MPO)로 다시 다듬는 3단계(Explore-Imitate-Optimize) finetuning 파이프라인이다. ALOHA 시뮬레이션 22개 manipulation task에서 VLM orchestration, SFT, RL 각 단계가 순차적으로 성능과 sample-efficiency를 끌어올림을 ablation으로 보였다.

**Core innovation & methodology**

- Explore 단계: 3B GROD VLA(PaliGemma backbone + diffusion policy head)에 Gemini VLM을 planner로 결합해, 상태 이력과 목표를 보고 VLA가 수행 가능한 짧은 sub-goal을 closed-loop로 지속 생성한다(π_VLM(g_t | s≤t, g)).
- 수집된 rollout 중 ground-truth success detector로 성공한 episode만 필터링해 buffer에 저장하고, VLM이 준 중간 goal이 아닌 원래 task goal(g)로 conditioning해 VLA를 behaviour-cloning objective로 SFT(Imitate 단계) — VLM의 지식을 VLA 하나로 distill해 평가 시 VLM 호출을 없앤다.
- Optimize 단계: VLA 출력에 residual action Δa를 더하는 residual policy(a = a_VLA + Δa)를 MPO 기반 off-policy RL로 학습해 sparse reward(성공 여부 indicator) 환경에서 추가 성능을 확보한다. Ankile et al.(2025a)의 residual off-policy RL 방식을 채택했다.
- GROD가 자연어를 직접 이해하는 instructable VLA이기 때문에 별도의 API grounding이나 masked-LLM grounding 없이 VLM이 자유형식 지시를 바로 내릴 수 있다는 점을 구조적 장점으로 강조한다.

**Novelty vs. prior works**

- 방법론 조각들(LLM/VLM 기반 task decomposition, VLM guided exploration, residual RL을 통한 VLA finetuning) 각각은 Dalal et al.(2024, Plan-Seq-Learn), Ankile et al.(2025a) 등 선행 연구에 이미 존재하며, Eximo는 이를 하나의 3단계 파이프라인으로 결합한 시스템 논문에 가깝다.
- Plan-Seq-Learn과의 핵심 차이는 vision policy를 처음부터 RL로 학습하는 대신, 이미 자연어로 직접 지시 가능한 SOTA VLA(GROD)를 VLM이 바로 명령해 grounding 문제를 우회하고, 그 orchestration 데이터를 SFT로 VLA 자체에 distill한다는 점이다.
- Hi Robot(Shi et al., 2025)처럼 VLM+VLA를 처음부터 공동학습하지 않고, 기성 VLA와 기성 VLM을 별도 모듈로 조합한 뒤 distillation으로 단일 정책으로 합친다는 점에서 실용적이지만, VLM orchestration → SFT → residual RL이라는 조합 자체의 개념적 새로움은 제한적이다.

**Benchmark results**

- ALOHA 로봇 시뮬레이션에서 22개 manipulation task(T2~T23, T1은 전체 평균)로 평가했으며, 접시/그릇 배치, semantic reasoning(예: '원숭이가 먹는 과일'), 좌우 compartment 공간 이해, 다중 tool 순차 배치 등 4개 범주를 포함한다.
- Fig. 3에서 GROD 단독 대비 GROD+VLM-Orchestration이 success rate를 유의미하게 높였고(특히 PlateBowlOnRack 같은 장기 task와 reasoning task에서 두드러짐), episode length도 더 짧아 데이터 수집 효율이 높다고 보고했다. 다만 구체적 success rate 수치(%)는 그래프로만 제시되어 본문에서 확인 불가.
- GROD+SFT(VLM orchestrated data로 파인튜닝)는 GROD+VLM-Orchestration보다도 성능이 높다고 서술되며, 저자들은 이를 filtered 고품질 supervision과 multi-step 행동의 단일 정책 distillation 효과로 설명한다(정확한 수치는 확인 불가).
- Fig. 4: GROD+SFT+RL은 base GROD+RL보다 학습 시작점과 수렴 성능이 모두 높으며, base GROD는 explore 단계의 추가 데이터 수집을 보상하기 위해 더 많은 environment step으로 RL을 돌렸음에도 GROD+SFT를 따라잡지 못했다고 claim한다(환경 step 수 x축은 2.5e7까지 제시, 정확한 최종 success rate 값은 확인 불가). 본문에 'twenty tasks 평균'이라는 서술과 '22개 task'라는 서술이 혼재해 task 수 표기에 다소 불일치가 있다.
- Ablation(부록): (1) VLM의 자유형식 지시와 pick&place로 제한한 지시는 5개 task에서 비슷한 성능을 보여 GROD가 별도 grounding 없이도 자유형식 명령을 잘 따른다는 것을 확인. (2) VLM orchestration을 VLA가 아니라 residual policy에 AWBC로 distill하는 대안은 offline 단계에서는 개선되지만 online RL 전환 시 distribution shift로 인해 순수 online RL baseline보다 느리게 학습해 실패했다고 보고한다. (3) rollout 중 VLM을 확률 p로만 사용하는 online RL 변형에서도 VLM을 전혀 쓰지 않는 baseline이 평가 시 가장 우수해, orchestration 이점이 residual policy로는 잘 전이되지 않음을 보였다 — 이는 저자 스스로 인정한 negative result다.

**Top-tier conference 적합성 — 62/100 · 추천 venue: CoRL**

VLM planner + BC distillation + residual RL을 하나의 파이프라인으로 통합하고 각 단계의 기여를 ablation으로 분해해 보였다는 점, Google DeepMind의 최신 GROD/Gemini를 실사용했다는 점에서 CoRL/RSS 워크숍이나 poster급 완성도는 갖췄다. 다만 전 실험이 ALOHA 시뮬레이션에 한정되어 real-robot 검증이 본문에서 확인되지 않고, 구체적 수치가 표로 제시되지 않아 재현성·정량적 비교가 약하며, 방법론적 새로움보다 기존 요소의 조합에 가까워 oral/highlight보다는 poster 수준의 accept 가능성이 높다.

**추천 이유 & 누리랩 연구와의 연결점**

- VLM을 planner로 써서 장기·조합 task를 sub-goal로 분해하고 성공 데이터만 필터링해 distill하는 Explore→Imitate 구조는, 누리랩의 skill chaining/long-horizon planning 및 language feedback 기반 learning 연구에 데이터 수집 파이프라인으로 직접 참고할 수 있다.
- Future Work에서 언급된 'VLM을 success detector로도 활용'하는 방향은 누리랩의 failure detection/diagnosis/recovery 주제와 맞닿아 있어, ground-truth detector 의존을 줄이는 확장 실험으로 이어갈 수 있다.
- residual policy로의 VLM orchestration distillation이 distribution shift로 실패했다는 negative result는, counterfactual/causal reasoning이나 test-time optimization 관점에서 residual RL과 VLM guidance를 결합하는 더 나은 distillation 방식(on-policy distillation 등, 논문도 future work로 제안)을 연구할 여지를 시사한다.

---

### 3. [65점] SafeBranch: Branch-Pair Safety Alignment for Embodied Agents

- **분야**: Embodied AI / Safety Alignment · **robotics relevance**: 8/10
- **arXiv**: [2608.19729](https://arxiv.org/abs/2608.19729) ([PDF](https://arxiv.org/pdf/2608.19729))
- **저자**: Hyunse Lee, Jiwoo Jeong, Haneul Lee, Kyochul Jang, Youngjae Yu, Woojin Lee
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **Comments**: 25 pages, 12 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 64점

> 💡 VLM 기반 embodied agent의 안전 위반이 trajectory 전체가 아니라 소수의 safety-critical step에서 결정된다는 점에 착안해, actor 자신의 unsafe rollout을 위반 시점으로 rollback한 뒤 critic feedback으로 안전한 대안을 이끌어내고 이를 동일 context에 대한 preference pair(branch pair)로 재구성하는 SafeBranch를 제안한다. BranchPO라는 DPO 변형으로 이 pair를 학습하면 배포 시 critic 없이도 IS-Bench SSR이 0.031에서 0.281로, unseen-object 변형에서는 0.048에서 0.469로 개선되어 task 성공률을 크게 해치지 않으면서 안전 성공을 늘렸다.

**Core innovation & methodology**

- safety-critical step(h_safe)이라는 개념을 formal하게 정의해, 안전 여부가 trajectory 전체가 아니라 actor의 선택이 갈리는 소수 분기점에서 결정된다는 step-level objective(Eq.1)를 제시한다.
- branch pair (h_k, y+, y-)라는 데이터 형태를 제안한다. actor의 unsafe rollout을 safety critic이 지목한 위반 시점 h_k로 environment rollback한 뒤, critic feedback f_k를 조건으로 actor 자신이 안전한 대안 y+_k를 샘플링하게 한다.
- critic feedback은 학습 입력에서 제거하는 hindsight relabeling을 적용해(Eq.3-4), 배포 시 cue 없이도 h_k만으로 안전 행동을 하도록 학습시킨다. prospective(행동 전 위반 예측)와 retrospective(잔여 위험 탐지) 두 trigger로 critic을 호출해 서로 다른 유형의 위반을 모두 다룬다.
- BranchPO는 DPO 형태의 objective로 branch pair에 대해 log pi(y+|h)-log pi(y-|h) margin을 극대화한다(Eq.5). judge filter와 cross-temperature pruning으로 pair 품질을 걸러 최종 학습 데이터를 만든다.

**Novelty vs. prior works**

- 기존 interactive safety 연구(HomeGuard, Safety Guardrails for LLM-Enabled Robots, C-MCTS, RoboMonkey 등)는 배포 시 매 스텝 외부 critic/guardrail을 돌리는 방식인 반면, SafeBranch는 critic 비용을 학습 단계 1회로 옮겨 actor 자체를 안전하게 만든 최초의 방법이라고 저자들은 주장한다. 이 claim은 논문 내 baseline 비교로만 뒷받침되며 외부 검증은 없다.
- 기존 embodied preference learning(D2PO는 trajectory-level, TCPO는 step-level이지만 동일 anchor 보장 없음, GRAPE는 trajectory-level safety 목표 포함)과 달리, SafeBranch는 두 branch가 반드시 동일 anchor state를 공유하도록 강제한다. 이 차이는 Table 4의 pair-구성 비교와 Trajectory DPO ablation으로 직접 검증되어 novelty가 실험적으로 뒷받침된다.
- DPO objective 자체(Rafailov et al. 2023)는 기존 것을 그대로 차용하므로, 방법론적 novelty는 loss가 아니라 rollback 기반 데이터 구성과 hindsight relabeling에 집중되어 있다. 즉 새로운 learning paradigm이라기보다 새로운 data-construction recipe에 가깝다.

**Benchmark results**

- IS-Bench(ID, Qwen3-VL-32B backbone)에서 SSR 0.031→0.281, SRec 0.273→0.467로 개선했다(baseline은 untrained actor).
- OOD-TaskShift(target object를 unseen category로 대체, 저자들이 abstract에서 'unseen-object variant'로 지칭)에서 SSR 0.048→0.469로 약 9.8배 상승해 abstract의 '약 10배' claim과 수치가 일치한다.
- OOD-ObjectShift(distractor object 주입)에서 SSR 0.051→0.355, SRec은 +34.6%p 개선됐다.
- cross-simulator 전이 실험(SafetyALFRED)에서 hazard accuracy 0.274→0.438; Property Damage +39.4%p, Appliance Misuse +15.4%p 개선했지만 Fall/Trip Hazard는 학습 pair가 아예 생성되지 않아 사실상 변화가 없었다(0.079→0.079, 본문 명시).
- ablation: 동일 DPO objective라도 branch pair 없이 trajectory-level DPO를 쓰면 IS-Bench SSR이 0.000까지 떨어져, 개선이 objective가 아니라 pair 구성 방식(same-state 여부)에서 온다는 것을 보였다. critic feedback을 학습 프롬프트에 남겨두는 +FB ablation도 배포 시 cue 부재로 SFT-only SSR이 0.000으로 붕괴해, hindsight relabeling이 핵심 설계 요소임을 확인했다.
- 데이터 생성 효율은 동일 GPU-시간당 natural best-of-N DFS 대비 5.2배(3.0→15.7 pairs/GPU-hour) 많은 usable branch pair를 만들었고, human reviewer 검증에서 filtering 단계를 거칠수록 usable pair 비율이 상승했다(raw 753→judge-kept 675→final 475 pairs).
- 배포 시에도 critic을 계속 쓰는 full-critic(GPT-4o, step마다 호출) baseline과 비교하면 ID split SRec은 full-critic이 더 높지만(0.680 vs SafeBranch 0.467), OOD split SR은 SafeBranch가 더 높다(ObjectShift 0.819 vs 0.762). 저자들은 이를 cluttered/unfamiliar 장면에서 full-critic의 over-flagging(과잉 중단)으로 설명하며, SafeBranch는 배포 시 추가 GPT-4o 호출이 0회다(full-critic은 최대 9,510회).
- 절대 성능은 여전히 낮다. 최고 조건에서도 SSR은 0.28~0.47, SRec은 0.44~0.8 수준이다. 실패 사례 분석(App G)에서 46개 안전 실패 중 34개(74%)가 critic의 retrospective feedback을 actor가 재계획에 반영하지 못하는 'reflection without repair' 패턴이었다.

**Top-tier conference 적합성 — 60/100 · 추천 venue: EMNLP**

IS-Bench/SafetyALFRED 등 최신 벤치마크에서 일관된 개선, 다수의 ablation, human verification까지 갖춰 empirical conviction이 상당히 높고, 유사 계열 연구(TCPO EMNLP 2025, SafetyALFRED ACL Findings 2026)를 볼 때 EMNLP/ACL/NAACL 계열에 적합하다. 다만 rollback 가능한 시뮬레이터에 의존하고 실제 로봇 검증이 없으며, 단일 seed 실험(seed 42)에 32-task 소규모 dev split이라 rejection risk가 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- rollback 기반으로 actor 자신의 실패(unsafe) rollout에서 대안 행동을 이끌어내는 구조는 누리랩의 failure detection/recovery 연구에서 recovery action을 self-collect하는 데이터 구성법으로 참고할 수 있다.
- critic feedback을 학습 시에만 조건으로 주고 hindsight relabeling으로 제거하는 방식은, language feedback을 policy에 internalize시키는 일반적 레시피로서 manipulation VLA policy의 test-time correction 내재화에도 응용 가능하다.
- critic 비용을 배포에서 학습 단계로 옮긴 설계는 test-time optimization/inference-time planning 연구에서 '매 스텝 비용 vs 학습 시 1회 비용' trade-off를 다루는 비교 사례로 활용할 수 있다.
- 다만 environment rollback에 의존하는 구조는 실제 manipulation robot에는 그대로 적용하기 어려워, world model 기반 approximate rollback으로 확장하는 것이 이어질 연구 아이디어가 될 수 있다.

---

### 4. [64점] DECOWAM: Decoupled Whole-Body World-Action Model for Legged Mobile Manipulation

- **분야**: World Model (Legged Mobile Manipulation) · **robotics relevance**: 10/10
- **arXiv**: [2608.20114](https://arxiv.org/abs/2608.20114) ([PDF](https://arxiv.org/pdf/2608.20114))
- **저자**: Siyuan Ma, Boshi Zhang, Yutian Zhang, Qinglian Wu, Jiaqi Zhai, Dong Wei, Qiaojun Yu
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **Comments**: 8 pages, 5 figures. Introduces DECOWAM, a decoupled whole-body world-action model for legged mobile manipulation, and the ARMDOG real-robot dataset
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 DECOWAM은 FastWAM(Wan-2.2 기반 video-action backbone)을 얼리고 residual adapter, action-equivalent future bottleneck, base/arm adversarial 분리, ego-motion conditioning 4개 모듈만 25.95M 파라미터로 추가 학습해 legged mobile manipulation용 whole-body world-action model을 만들었다. 새로 구축한 real-robot 데이터셋 ARMDOG에서 replay 실험으로 action MSE를 21.7% 줄였고, 79회 closed-loop 실험에서 whole-body coordination과 base-displacement robustness가 가장 우수했다.

**Core innovation & methodology**

- 문제 설정: legged mobile manipulator는 카메라가 base에 실려 이동해 ego-motion·scene dynamics·arm motion이 이미지에서 섞이고, action이 고주파 arm(~15-30Hz)과 저주파 base velocity(~3-5Hz)로 이질적이라는 점을 지적하며, 이를 explicit factor로 분리하는 decoupled whole-body world-action modeling을 제안한다.
- Backbone: Wan-2.2 기반 video diffusion + ActionDiT 액션 헤드로 구성된 FastWAM(6725.44M total, 6020.75M trainable)을 Stage1에서 50k step 전체 fine-tuning한 뒤, Stage2에서 backbone을 얼리고 4개 모듈만 25.95M 파라미터로 학습하는 staged parameter-efficient adaptation을 쓴다.
- Action-equivalent future bottleneck: teacher는 현재+미래 WAN-VAE latent 요약(mean/std)을 보고 student는 현재 상태만 보는 causal 구조로 두고, reconstruction + teacher-student distillation + geometry-preserving loss(batch 내 정규화 action 거리와 latent 거리 정합)로 미래 정보를 causal policy에 distill한다.
- Base/arm 분리: pooled action context를 16-D base/arm latent 두 개로 나누고, 각 latent에 직접 head는 자기 factor를 복원하고 gradient-reversal layer(GRL)를 통한 cross head는 반대 factor 정보를 억제하도록 학습하는 adversarial disentanglement를 적용한다.
- Ego-motion conditioning: 정규화된 현재 base velocity(vx, vy, ωz) 토큰을 모든 video token에 동일하게 더해, 카메라 ego-motion을 video expert에 명시적으로 노출한다(픽셀만으로 추론시키지 않음).

**Novelty vs. prior works**

- 가장 가까운 prior work는 backbone인 FastWAM, 그리고 UVA·X-WAM·Motus 같은 video-action WAM 계열, π0.5·X-VLA 같은 VLA 계열이다. 이 논문은 새로운 backbone이나 generative 구조를 제안하지 않고, LoRA류 residual adapter, teacher-student distillation, domain-adversarial GRL, disentangled representation 같은 기존에 알려진 기법들을 legged mobile manipulation embodiment에 맞춰 조합한 구조에 가깝다.
- novelty는 새로운 알고리즘보다 문제 설정과 조합에 있다. base motion·arm manipulation·camera ego-motion을 explicit interface로 분리한다는 problem formulation 자체는 이 legged-mobile-manipulation 도메인에서 시도가 드물며, 저자들도 legged base에서 unified whole-body world-action modeling을 수행한 선행 연구를 인지하지 못한다고 명시한다.
- ARMDOG 데이터셋(4족 로봇+6-DoF arm, video·state/action·language 동기화)은 Open-X, DROID, RoboTwin 등 기존 데이터셋에 없는 legged-base ego-motion 스트림을 포함한다는 점에서 기여이나, quality-filtered 기준 1487 episode(모델 학습에는 이보다 작은 214개 subset 사용)로 규모는 크지 않다.

**Benchmark results**

- Table I(23-episode ARMDOG replay slice): DECOWAM(50k)이 FastWAM(50k) 대비 frame MSE 15.03%, action MSE 21.71% 감소했고 PSNR은 31.441→31.663(+0.222dB)로 개선됐다.
- Table II ablation(별도 학습된 suite, adapter-only 대비): full frozen decoupled 모델이 frame MSE 4.6%, action MSE 15.7%, action MAE 16.1% 감소했다. future bottleneck 또는 base-velocity conditioning 중 하나만 제거해도 video·action 두 branch 성능이 모두 나빠져, 각 모듈의 기여가 확인된다.
- Table III VLA 비교(같은 23-episode slice, action만 비교): X-VLA가 A-MSE 2.11e-5로 전체 중 최저이며 DECOWAM(5.38e-5)보다 낮다. DECOWAM은 π0.5 대비 A-MSE 69.9%, A-L2 21.1% 개선했지만 X-VLA에는 못 미친다(저자도 X-VLA가 action-only 최고 성능임을 인정).
- Table IV WAM 비교에서는 DECOWAM이 F-MSE, PSNR, SSIM, LPIPS, A-MSE, A-MAE, A-L2 전부 1위다. Motus 대비 frame/action MSE 83.1%/89.3% 감소, X-WAM(4프레임·160px로 더 낮은 사양) 대비 66.6%/91.5% 감소했다.
- 79회 real-robot closed-loop trial(Table V)에서 DECOWAM의 task success rate는 58.2%(FastWAM 57.0%, π0.5 49.4%, X-WAM 15.2%, GR00T 8.9%)로 가장 높고 mean completion time도 49s로 가장 빠르다. whole-body coordination success rate(WBCM-SR) 44.3%(FastWAM 대비 +10.1pt), base-displacement robustness(BDP-SR) 30.4%(FastWAM 대비 +17.7pt)로 격차가 가장 크다. 다만 최종 task success rate 자체는 FastWAM과 큰 차이가 아니다(58.2% vs 57.0%, 저자도 'comparable'로 표현).
- Table VI: Stage2 학습 파라미터를 6020.75M→25.95M로 약 232배 줄이면서 evaluator latency는 1196.6ms→1333.2ms로 11.4% 증가에 그쳤다.

**Top-tier conference 적합성 — 60/100 · 추천 venue: ICRA**

실제 legged-arm 로봇에서 79회 closed-loop trial과 새 데이터셋(ARMDOG), 명확한 module ablation(Table II)을 갖춰 systems 논문으로서 완성도가 있다. 다만 핵심 기법(residual adapter, teacher-student distillation, GRL disentanglement, velocity conditioning)이 각각 기존 기법의 재사용 조합이라 conceptual novelty는 제한적이고, action-only 최강 baseline인 X-VLA에는 action 정확도에서 열세이며 단일 로봇·소수 task family(box 조작 위주)로 generalization 근거가 약해 top-tier oral보다는 강한 poster/ICRA-IROS급 accept가 현실적이다.

**추천 이유 & 누리랩 연구와의 연결점**

- Pretrained video-action backbone을 얼리고 embodiment-specific adapter(25.95M, 총 파라미터의 0.4% 수준)만 학습하는 staged parameter-efficient adaptation 레시피는 우리 lab이 다양한 embodiment(양팔/사족/휠형)로 world model을 확장할 때 재사용 가능한 실무적 방법론이다.
- action-equivalent future bottleneck(teacher는 미래 latent를 보고 causal student로 distill)은 test-time optimization·failure detection 연구에서 '미래 rollout latent를 현재 정책에 causal하게 주입'하는 아이디어로 확장할 수 있다. 예를 들어 여러 미래 rollout 후보 중 실패로 이어질 latent를 조기 판별하는 diagnosis 모듈에 응용 가능하다.
- base/arm GRL disentanglement는 whole-body mobile manipulation에서 navigation-scale 결정과 manipulation-scale 보정을 분리 표현하는 방식으로, 우리 lab의 skill chaining·long-horizon TAMP 과제에서 base와 arm 정책을 모듈화할 때 참고할 수 있다.

---

### 5. [64점] Fine-Tuning VLAs with Self-Demonstrated Generative Control for Multi-Task Manipulation

- **분야**: VLA · **robotics relevance**: 9/10
- **arXiv**: [2608.19490](https://arxiv.org/abs/2608.19490) ([PDF](https://arxiv.org/pdf/2608.19490))
- **저자**: Prachi Garg, Steve Xing, Prahit Yaugand, Saurabh Gupta, Derek Hoiem
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Project Page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 58점

> 💡 π0.5 VLA를 새 embodiment(ALOHA 로봇)에 fine-tuning할 때, frozen zero-shot 정책을 target robot 위에서 직접 rollout시켜 얻은 self-demonstration을 expert demo와 함께 학습시키는 self-supervised generative replay 기법을 제안한다. Real ALOHA와 RoboTwin 시뮬레이션 실험에서 expert-only fine-tuning 대비 instruction following과 pretrained behavior(예: place skill) 유지, 새로운 contact-rich task의 sample efficiency를 모두 개선했다.

**Core innovation & methodology**

- 문제 설정: pretrained VLA(π0.5)를 새 embodiment에 fine-tuning하면 expert task 성능은 좋아지지만, zero-shot에서 보이던 instruction following과 pretrained behavioral prior(예: pick 후 place 동작)를 잃는 catastrophic forgetting이 발생한다.
- 핵심 아이디어: frozen base policy π0.5_base를 target robot 위에서 self-supervised task prompt p_SS로 직접 online rollout시켜 관측-행동 쌍 (o_t, â_t)을 수집하고 이를 self-demonstration(D_SS)으로 사용한다. 원본 pretraining data나 task list에 접근할 필요가 없고, rollout이 target hardware/scene/prompt에서 직접 수집되므로 embodiment/domain gap이 없다.
- objective: π0.5의 FAST cross-entropy + conditional flow matching per-sample loss(Eq.1)를 expert dataset D_ES와 self-demo dataset D_SS 각각에 적용해 L = L_ES + λL_SS 로 joint fine-tuning한다. 1:1 mixing ratio, uniform task sampling이 최적이며(Table 9 ablation), task-weighted sampling이나 SS 데이터 buffer 축소는 TSS retention을 크게 낮춘다.
- Real ALOHA-1(pick/place, contact-rich caterpillar gear insertion)과 RoboTwin 2.0 simulation(ALOHA-Agilex) 두 benchmark, 그리고 TES/TSS/TNO/TNC 4종 test set을 새로 구성해 expert task·self-supervised task·novel object·novel composition으로의 generalization을 체계적으로 평가했다.

**Novelty vs. prior works**

- continual learning의 generative replay(예: DreamBooth류 diffusion prior-preservation)와 유사하지만, 기존 방법은 pretraining prior를 offline sampling하거나 같은 class를 재현하는 반면, 본 논문은 pretrained VLA를 target robot에서 online rollout시켜 expert task와 disparate한 pretraining task들을 self-distillation한다는 점이 다르다고 저자는 주장한다.
- Liu et al.(ICML 2026, [29])의 parameter-efficient fine-tuning + replay 연구는 LIBERO에서 저장된 mid-training data 접근을 전제하는 반면, 본 논문은 pretraining data/task list에 전혀 접근하지 않고 policy 자신의 rollout만으로 rehearsal한다는 실용적 제약을 명시적으로 다루며, RoboTwin에서 이 방법과 직접 비교한다.
- 다만 방법론 자체는 '자기 자신의 예측을 pseudo-label로 쓰는 self-training/self-distillation + experience replay'의 결합이며, VLA post-training이라는 응용 영역에서의 novelty이지 학습 패러다임 자체의 새로움은 제한적이다. 저자들도 왜 self-supervision이 도움이 되는지(traversed state 때문인지 distillation target 자체 때문인지)에 대한 명확한 이론적 설명 없이 실험적 관찰에 의존한다고 Future Work에서 인정한다.

**Benchmark results**

- Real ALOHA Benchmark 1(pick/place, Table 2): expert-only Multi-Task ES는 place 동작을 완전히 잊어 TSS pick-and-place SR이 0%였으나, 제안 방법(ES+SS)은 expert place demo 없이 SR 55%까지 회복(post-grasp IF 90%)했다. Expert task TES(cube pick) SR도 65%→90%로, novel object TNO SR도 50%→55%로 개선됐다(20 trial 기준).
- Instruction following(저자 주장, 본문 수치와 일치): novel object picking IF 50%→55%, pick-and-place IF 75%→90%로 개선되어 6개 test set 중 5개에서 zero-shot π0.5보다 높은 IF를 기록했다.
- Held-out skill 'push'(Table 7, 어느 fine-tuning data에도 없는 task): push 성공률(SR)이 제안 방법 60% 대 all-expert oracle(MT ES+ES) 5%, zero-shot 30%. Full expert supervision은 35%의 경우 학습된 pick 동작을 그대로 밀어붙이는 경향을 보인 반면, 제안 방법은 관련 없는 prior를 온전히 보존했다.
- Contact-rich caterpillar gear insertion(Table 3, base policy pretraining 범위 밖 task): SR이 expert-only 30%→90%(학습된 gear color), novel gear color TNO에서는 0%→30%로 개선됐다.
- RoboTwin(Table 4·5): naive Multi-Task ES는 TSS(mid-training task) 성능을 90.8%→16.6%로 붕괴시키지만, 제안 방법은 70.6%까지 회복(54% 회복)하면서 TES도 93%→98%로 오히려 향상됐다. Overall average는 56.8%로, 원본 mid-training data에 접근하는 rehearsal oracle(57.0~60.8%)에 0.2%p 차이로 근접했고 Multi-Task ES 대비 13.5%p 높았다.
- ablation(Table 6): expert supervision을 전량 확보한 upper-bound oracle(MT ES+ES) 대비 TES SR 95% vs 90%, TSS pick-place SR 65% vs 55%로 소폭 낮았고, self-demo 품질이 노이즈가 많은 laundry task에서는 격차가 컸다(90% vs 40% partial SR).

**Top-tier conference 적합성 — 60/100 · 추천 venue: CoRL**

Real ALOHA 로봇과 RoboTwin 시뮬레이션 두 환경에서 다수의 baseline·oracle 비교와 세밀한 ablation(mixing ratio, freezing scheme, FAST+Flow objective)을 갖춰 실험적 conviction이 상당히 높고, VLA를 새 embodiment에 배포할 때의 실용적 문제를 다룬다는 점에서 CoRL/RSS 성격의 robot learning venue에 적합하다. 다만 방법 자체가 self-training과 experience replay의 조합이라는 비교적 단순한 아이디어이고 real robot trial 수가 10~20회로 적으며, 이론적 설명이나 다른 continual learning SOTA와의 직접 비교가 제한적이어서 NeurIPS/ICML급 top-tier에서는 novelty 부족으로 rejection risk가 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- self-supervised generative replay는 누리랩의 test-time optimization/inference-time planning 및 robot memory 연구와 연결지어, 새 로봇 배치 시 '자기 자신의 rollout을 rehearsal buffer로 활용'하는 continual adaptation 모듈로 확장할 수 있다.
- 논문이 밝힌 실패 모드(성공적 place 이후 반복적으로 pick-place를 되풀이하는 현상, 안전하지 않은 self-demo 행동)는 failure detection·diagnosis·recovery 연구와 접목해 self-demo를 자동 필터링하는 project로 이어질 수 있다.
- π0.5의 catastrophic forgetting과 embodiment gap 문제는 generalist robot policy 연구에 직접 관련되며, self-demo 기반 rehearsal을 world model이나 counterfactual reasoning 기반 rollout selection과 결합해 self-demo data quality를 자동 판별하는 방향도 고려할 수 있다.

---

### 6. [64점] Video2DoorTraversal: Push Door Traversal via Simulated Door Twins

- **분야**: Manipulation (Loco-manipulation, Real-to-Sim-to-Real) · **robotics relevance**: 9/10
- **arXiv**: [2608.20251](https://arxiv.org/abs/2608.20251) ([PDF](https://arxiv.org/pdf/2608.20251))
- **저자**: Xincheng Tang, Yiji Chen, Youhan Xie, Wanyu Li, Zhengjie Shu, Lai Jiang, Wenkang Hu, Yitong Li 외 3명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 8 pages, 6 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 Video2DoorTraversal은 문 하나를 찍은 단일 RGB 비디오로부터 articulated door twin(DoorTwin)을 복원하고, simulation-in-the-loop agent로 teleoperation 없이 expert demonstration을 생성해 dual-depth policy ArticuACT를 학습시키는 real-to-sim-to-real 파이프라인이다. 그 결과 실제 5개 문에서 평균 96.57%, 구조가 유사한 unseen door에서 80.95%의 zero-shot 성공률을 onboard 추론만으로 달성해 wheel-legged mobile manipulator의 door opening-traversal을 안정적으로 수행한다.

**Core innovation & methodology**

- Video2DoorTraversal은 문을 촬영한 단일 RGB 비디오만으로 real-to-sim-to-real 파이프라인 전체를 구성해 wheel-legged mobile manipulator(Unitree A2-W + Z1 arm)의 door opening과 traversal을 가능하게 한다.
- DoorTwin은 Articraft 기반 articulated asset generation에 DAGE(+LingBot-Depth) 기반 video geometry grounding, SAM3 segmentation, reference-view rendering-critique loop, GPT 기반 delighting과 Tripo3D texture transfer를 결합해 metric scale과 instance-level appearance를 동시에 관측 대상 문에 맞춘다.
- Simulation-in-the-loop agent가 복원된 articulation을 BaseMoveTo, EE_Approach, Rotate_Handle, Push_Door, Pass 등 parameterized skill program으로 변환하고, Isaac Gym rollout(50Hz) 실패를 진단해 파라미터를 bounded 범위 내에서 반복 수정하는 generate-execute-diagnose-refine loop로 human teleoperation 없이 expert demonstration을 생성한다.
- ArticuACT는 ACT를 base로 front/wrist dual-depth 관측에 robot-centric Plücker ray map conditioning(Jiang et al., 2025의 camera conditioning 기법을 응용)과 contact·handle-rotation-progress·door-opening-progress를 예측하는 interaction-state auxiliary supervision을 추가해, base velocity/yaw·6개 arm joint·gripper로 구성된 action chunk(H=100)를 예측한다.

**Novelty vs. prior works**

- 핵심 구성요소인 Articraft(articulated asset generation), DAGE(video geometry estimation), SAM3(segmentation), Plücker ray conditioning(Jiang et al., 2025)은 모두 기존에 독립적으로 존재하던 기법이며, 본 논문의 기여는 이들을 door 특화 real-to-sim-to-real 파이프라인으로 결합·확장하는 systems integration에 가깝다. 완전히 새로운 representation이나 learning paradigm을 제안하지는 않는다.
- 저자는 Table I에서 Human2Sim2Robot, X-SIM, SIMPACT(real-to-sim), UniDoorManip/DoorGym/ArticuBot(articulated manipulation), teacher-student 방식 legged door traversal과 비교해 "single RGB video 입력 + mobile robot + articulated manipulation + agentic expert + sim-to-real + door traversal"을 모두 만족하는 유일한 방법이라 주장한다. 이 조합 자체가 novelty의 핵심이며 개별 요소의 발명이 아니다.
- Simulation-in-the-loop agentic expert generation의 diagnose-refine loop(실패 원인 진단 → bounded parameter 수정 → simulator 재검증)는 rule-based baseline(74.38%) 및 no-rollout variant(48.13%) 대비 유의미한 성능 개선(85.63%)을 보여 방법론적 기여가 실험적으로 뒷받침된다.

**Benchmark results**

- Asset generation 품질(실제 문 20개, GPT-5.5로 공정 비교): DoorTwin이 Scale Score 94.95, mIoU 0.972, PSNR 18.53, VLM Score 56.74로 Articraft(89.03/0.880/16.64/28.75), Articulate-Anything(86.62/0.831/16.03/11.59), PhysX-Omni(65.75/0.635/17.51/11.54) 대비 대부분 지표에서 우세하다. 다만 SSIM은 0.692로 PhysX-Omni(0.726)·Articraft(0.702)보다 낮아 appearance fidelity가 모든 지표에서 일관되게 최고는 아니다.
- Simulation 실험(문 20개, 256 trial): door opening/traversal success에서 Ours 98.44%/97.27%로 UniDoorManip(74.22%/50.78%), Vanilla ACT(67.58%/64.84%), Diffusion Policy(64.45%/64.45%), DP3(68.36%/66.41%), DoorGym(12.50%/12.50%), OA Replay(53.13%/53.13%), Replay(14.06%/14.06%)를 모두 상회한다.
- Real-world 실험(실제 문 5개, 각 35 trial): Ours 평균 96.57%(35/35, 32/35, 35/35, 33/35, 34/35)로 Vanilla ACT 65.71%, OA Replay 36.58%, Replay 18.29%를 크게 앞선다. 전체 approach-opening-traversal sequence를 평균 약 13초에 완료한다.
- Zero-shot cross-door generalization: 학습에 쓰인 door twin과 "구조적으로 유사한(structurally similar)" unseen door 3개(각 35 trial)에서 25/35, 31/35, 29/35로 평균 80.95% 성공률을 보인다. 다만 대상이 구조가 유사한 문으로 한정돼 있어 완전히 다른 door type에 대한 일반화는 본문에서 확인 불가.
- Ablation: vanilla ACT 대비 Plücker conditioning과 interaction-state prediction을 모두 추가한 ArticuACT full model이 joint-command 기준 traversal success를 71.09%→97.27%(+26.18%p), EE-command 기준 64.84%→82.42%(+17.58%p)로 개선하며, 가장 강한 단일 모듈(interaction, joint-command 94.92%) 대비로도 +2.35%p 개선한다. Data scaling에서는 demonstration 50개 59.38%→200개 97.27%로 첫 100개 구간에서 개선폭이 가장 크다.

**Top-tier conference 적합성 — 58/100 · 추천 venue: CoRL**

Video2DoorTraversal은 real-world 5개 문 96.57%, 20개 문 시뮬레이션 97.27% traversal 성공률과 policy component·agentic trajectory generation·data scaling까지 아우르는 세밀한 ablation을 갖춘 systems paper로, CoRL/ICRA 수준 리뷰를 통과할 만한 실험적 증거를 확보했다. 다만 핵심 구성요소(Articraft, DAGE, SAM3, Plücker conditioning)가 대부분 기존 기법의 결합·응용이라 conceptual novelty는 제한적이고, 평가 대상 door가 5개(+unseen 3개)로 적어 door diversity에 대한 rejection risk가 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- DoorTwin의 "single video → simulation-ready articulated digital twin" 파이프라인은 object-centric 3D/4D representation 및 scene graph 연구에 참고할 만한 템플릿을 제공한다. drawer, cabinet 등 다른 articulated object로 확장해볼 수 있다.
- Simulation-in-the-loop agent의 실패 진단(diagnose) → bounded parameter 수정 → simulator 재검증 loop는 failure detection/diagnosis/recovery 및 test-time optimization 연구와 직접 연결된다. 이 구조를 real robot rollout에서의 online failure recovery로 확장하는 방향을 검토할 수 있다.
- ArticuACT의 robot-centric Plücker ray conditioning과 interaction-state auxiliary prediction은 VLA/generalist policy에서 camera geometry grounding과 contact-aware supervision을 결합하는 사례로, 다른 mobile manipulation·dexterous manipulation policy 설계에도 적용 가능하다.

---

### 7. [64점] The Missing Touch: Spatially Distributed Tactile Feedback Brings Teleoperation Closer to Human Dexterity

- **분야**: Manipulation / Tactile Perception (Teleoperation) · **robotics relevance**: 8/10
- **arXiv**: [2608.19372](https://arxiv.org/abs/2608.19372) ([PDF](https://arxiv.org/pdf/2608.19372))
- **저자**: Rohan Kota, Gregory Reardon, J. Edward Colgate
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 이 논문은 2-DoF bilateral force-feedback telemanipulator에 32-DoF cutaneous shape display(Fluid Reality, electro-osmotic actuation)를 결합해, GelSight Mini로 측정한 robot fingertip의 국소 접촉 변형을 조작자의 손가락에 공간적으로 그대로 재현하는 teleoperation 시스템을 제시한다. Off/1D/2D/Full 네 단계로 촉각 해상도를 조절한 button discrimination·peg-rolling 실험에서, 완전 국소화된(Full) 피드백이 직접 조작(direct manipulation) 궤적과의 DTW distance를 29-79% 줄이고 조작 간 variability와 mental demand도 함께 낮춤을 보였다.

**Core innovation & methodology**

- 문제 설정: teleoperation이 자율 로봇 정책 학습용 demonstration 수집 수단으로 널리 쓰이는데도, 조작자가 느끼는 촉각 정보가 force feedback 또는 저차원 vibrotactile/skin-stretch/uniform tilting cue로 collapse되어 있다는 점을 gap으로 지목한다.
- 방법: vision-based tactile sensor(GelSight Mini)가 robot finger의 접촉 이미지를 차분·이진화(Otsu's method)해 32-pixel inflation pattern으로 변환하고, 이를 32-DoF cutaneous shape display에 그대로 매핑해 human fingertip에 렌더링한다.
- 실험 설계: 공간 해상도를 4단계(Off, 1D-전체 동시 팽창, 2D-상하 2분할, Full-완전 국소화)로 조작하는 within-subject 실험을 button discrimination task(12명)와 peg-rolling task(10명)에서 각각 48 trial(조건당 12 trial)로 수행했다.
- 평가 지표: teleoperated trajectory와 (시각 차단 상태의) direct manipulation baseline trajectory 간 dynamic time warping(DTW) distance를 'naturalness' 지표로 새로 도입해, 기존의 속도·정확도 중심 평가와 구분했다.

**Novelty vs. prior works**

- 가장 가까운 선행연구(vibrotactile/electrotactile stimulation, skin-stretch display, uniform tilting platform 기반 force-to-cutaneous rendering, refs 22-30)는 접촉 정보를 저차원 신호로 압축해 렌더링하는 반면, 본 논문은 (저자들 주장상) robot fingertip의 국소 변형 분포를 human fingertip에 공간적으로 보존해 전달하는 첫 teleoperation 시스템이라고 밝힌다.
- naturalness를 직접 조작 대비 DTW distance로 정량화하는 평가 프레임을 제시한 점이 개념적 기여이며, 기존 연구들이 속도/정확도 개선만 보고한 것과 달리 움직임의 질적 자연스러움과 state-space compactness를 별도 축으로 분리해 측정했다.
- 다만 방법론적 새로움은 제한적이다: DTW, LME, Wilcoxon/Mann-Whitney 등 기존 통계 도구를 그대로 사용했고, tactile sensing-to-display mapping도 단순 thresholding/binarization 알고리즘이다. 시스템 통합(hardware integration)과 human-subjects 실험 설계의 엄밀함이 핵심 novelty이고, 새로운 representation이나 learning paradigm은 제시하지 않는다.

**Benchmark results**

- Button discrimination task(12명, 조건당 12 trial): Full 조건이 Off·1D·2D 대비 overshoot(p<0.001)과 switchback 횟수(p≤0.007)를 유의하게 감소시켰다. DTW distance는 모든 feedback 조건이 Off 대비 유의하게 감소했고(p<0.001), Full은 1D보다도 유의하게 낮았다(F(1,572)=8.125, p_adj=0.014)이나 2D와는 유의차 없음(p=0.244).
- Peg-rolling task(10명, 조건당 12 trial): Full 조건이 roll-off 횟수(p≤0.039), stroke length(p≤0.004), stroke 수(p≤0.014) 모두에서 다른 세 조건 대비 유의하게 개선됐다. DTW distance는 Full이 2D(p=0.003), 1D(p<0.001), Off(p<0.001) 대비 유의하게 낮았으나, 1D는 kinesthetic cue와의 redundancy로 Off와 유의차가 없었다(p=0.059).
- Naturalness(DTW distance) 개선폭은 abstract 기준 29-79%로 보고되나, 이 범위가 어느 조건 조합·어느 task에 해당하는지 구체적 산출 근거는 본문에서 확인 불가.
- state-space compactness: Full 조건에서 within-participant inter-trial DTW distance(button p_adj<0.001, peg p_adj=0.003)와 다중 조작자 aggregated dataset의 inter-trial DTW distance(양 task 모두 p<0.001)가 다른 모든 조건보다 유의하게 낮아, 궤적 분포가 더 compact해짐을 보였다.
- NASA-TLX 기반 mental demand(Q2)가 해상도 증가에 따라 점진적으로 감소하는 경향을 보였다(구체적 p-value 표는 본문에서 확인 불가). 단, 이 논문은 실제 imitation learning 정책을 학습·평가하지 않았고, demonstration 품질 개선이 정책 학습에 도움된다는 주장은 선행연구(refs 41, 42) 인용에 근거한 추론이며 저자 자신의 실험 결과는 아니다.

**Top-tier conference 적합성 — 58/100 · 추천 venue: RSS (또는 Science Robotics)**

Northwestern 그룹의 정교한 hardware 통합(32-DoF electro-osmotic cutaneous display)과 엄격한 통계 처리(LME, Holm-Bonferroni correction)를 갖춘 human-subjects 연구로, teleoperation 논문 형식보다는 Science/Science Robotics 스타일 short paper에 가깝다. 로봇학습 커뮤니티 관점에서는 참신한 문제의식(촉각 demonstration quality)과 견고한 실증이 강점이지만, 2-DoF 단일 손가락 시스템·10-12명의 소규모 참가자·단순 button/peg task로 실제 dexterous manipulation이나 정책 학습 결과 없이 extrapolation에 그친 점이 top-tier ML/robotics 학회에서는 rejection risk로 작용할 수 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- teleoperation demonstration의 tactile 해상도가 학습 데이터 품질(state-space compactness, inter-operator consistency)에 영향을 준다는 결과는, VLA/manipulation policy 학습 시 demonstration collection pipeline 설계에 참고할 수 있는 실증 근거를 제공한다.
- tactile perception을 저차원 force cue가 아니라 공간 분포로 다루는 접근은, object-centric contact representation이나 tactile-conditioned world model 연구에 입력 modality 설계 아이디어로 확장 가능하다.
- naturalness(DTW-to-direct-manipulation) 지표는 누리랩의 demonstration quality 평가나 failure detection 연구에서, teleoperated trajectory의 '자연스러움'을 정량화하는 auxiliary metric으로 응용해볼 수 있다.

---

### 8. [62점] Stream4D: 4D-Consistency for Streaming Autoregressive Diffusion Video Models

- **분야**: World Model / Video Generation (RL for streaming AR video diffusion) · **robotics relevance**: 7/10
- **arXiv**: [2608.19556](https://arxiv.org/abs/2608.19556) ([PDF](https://arxiv.org/pdf/2608.19556))
- **저자**: Yuanhao Ban, Jiaqi Feng, Hengguang Zhou, Xiaohuan Pei, Justin Cui, Cho-Jui Hsieh
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 Streaming autoregressive video diffusion 모델을 RL로 파인튜닝할 때 static 3D Gaussian-Splatting reward가 실제 움직임을 reconstruction error로 오인해 화면을 정지시키는 reward hacking 문제를 지적한다. Stream4D는 이를 feed-forward 4D-GS reconstructor(MoVieS) 기반 reward와 gated motion prior, perceptual anchor로 대체해 Self-Forcing/Causal-Forcing/LongLive 세 backbone 모두에서 4D-PSNR과 motion 유지율을 동시에 개선했다.

**Core innovation & methodology**

- 문제 설정: streaming AR diffusion video model(Self-Forcing, Causal-Forcing, LongLive)을 RL로 파인튜닝할 때, World-R1·VideoGPA가 쓰는 static 3D-GS reconstruction reward는 rigid한 단일 3D 장면만 표현 가능해 실제 object motion을 reconstruction error로 벌점 처리하고, 그 결과 영상을 정지시키는 것이 reward를 최대화하는 shortcut이 된다는 점을 지적한다.
- 해결책: MoVieS(feed-forward 4D Gaussian-Splatting, per-frame deformation·scene-flow 포함)로 rollout을 재구성해 LPIPS 기반 R_recon을 계산하고, 이는 동적 장면도 잘 설명하므로 motion을 구조적으로 벌하지 않는다.
- 추가로 motion 품질을 유도하는 R_mot = g(m)·smooth·rigid를 설계한다. g(m)은 자연스러운 motion magnitude(median of base rollout, m_nat=0.020)를 중심으로 하는 Gaussian gate이고, smooth/rigid는 jitter와 공간적으로 비정합적인 flow(찢어짐/젤리화 아티팩트)를 벌점 처리하는 항이다.
- R_recon, R_mot에 HPSv2 기반 perceptual anchor R_hpsv2를 더해 axis별 z-normalization 후 가중합(Eq. 8)하고, Astrolabe 프레임워크(rolling-KV-cache + DiffusionNFT forward-process loss)의 advantage로 사용해 LoRA adapter를 학습한다. RL 알고리즘 자체는 기존 Astrolabe를 그대로 사용하고, 기여는 reward 설계에 집중된다.

**Novelty vs. prior works**

- 가장 가까운 prior work인 World-R1(ICML 2026 제출), VideoGPA(ICML 2026 제출)는 static 3D-GS reconstruction을 reward로 쓰는 bidirectional T2V RL 방법이다. Stream4D는 reconstructor를 rigid 3D-GS에서 4D-GS(MoVieS)로 교체해 '3D-consistency reward'를 '4D-consistency reward'로 재정의한 것이 핵심 차별점이며, streaming AR 세팅(제한된 temporal context로 인해 static collapse가 더 쉬운 shortcut이 되는 상황)에 처음 적용했다는 점을 강조한다.
- 다만 RL 최적화 알고리즘(DiffusionNFT, Astrolabe의 rolling-KV-cache), reward 백본(MoVieS, StreamVGGT, HPSv2)은 모두 기존 공개 모델을 그대로 재사용한다. 즉 새로운 representation이나 learning paradigm이라기보다는, 기존 구성요소들을 조합한 reward 설계·엔지니어링에 가까운 기여다.
- motion gate(Gaussian, m_nat)의 형태와 smooth/rigid 항은 저자들이 직접 설계했고 ablation으로 각 항의 필요성을 뒷받침하지만(Table 3, 4), 방법론적 참신성보다는 실험적으로 잘 검증된 practical fix의 성격이 강하다.

**Benchmark results**

- 500-prompt motion-prominent VidProM subset 기준, Stream4D는 세 backbone 모두에서 base 대비 4D-PSNR(MoVieS 기준)을 크게 개선했다: Self-Forcing 16.88→20.34dB(+3.46dB), Causal-Forcing 15.44→20.97dB(+5.53dB), LongLive 17.44→24.20dB(+6.76dB). reconstructor가 다른 4DGT 기준으로도 World-R1 대비 +0.7/+1.1/+2.5dB 우위를 보여 MoVieS 특이적 효과가 아님을 교차 검증했다(단 두 reconstructor 모두 카메라 추정에는 동일한 StreamVGGT를 사용).
- Gemini-3.5-Flash judge(reward-blind)의 Consistency win%는 82.2/73.9/74.2%로 World-R1의 75.9/69.1/54.0%를 상회했고, motion 보존 점수도 세 backbone 모두 최고였다(0.833/0.765/0.706).
- VideoReward(Qwen2-VL-7B) Overall win-rate는 66.2/76.0/84.4%로 World-R1(61.8/74.8/78.2%)을 앞섰고, motion-quality head에서 격차가 가장 컸다(+12.2/+6.4/+11.4pp).
- Human study(LongLive, 50 high-motion prompt, 5 rater, 150 2AFC 비교)에서 Stream4D는 World-R1 대비 Overall 76%, VideoGPA 대비 80% 승률을 보였다(base 대비는 Overall 60%, raw Motion 43%로 base보다 낮게 나온 점은 저자도 명시). 단 human study는 LongLive 한 backbone에만 적용됐다.
- Ablation(Table 3): motion term 제거 시 세 backbone 모두 motion 붕괴(예: Self-Forcing Consist. 82.2→31.1%), reconstruction term 제거 시 motion score는 최고(0.98 수준)로 오르지만 coherence가 붕괴(Consist. 24.2%까지 하락). perceptual anchor 제거는 LongLive에서 4D-PSNR 3.6dB, VideoReward-Overall 15pp 손실을 유발. 즉 세 reward axis 모두 적어도 하나의 backbone에서는 필수적임을 보였다.
- World-R1/VideoGPA는 distilled AR 세팅용 공식 checkpoint가 없어 저자들이 동일 base·trainer·prompt로 직접 재구현한 결과이며, 이는 비교의 공정성에 영향을 줄 수 있는 한계점이다(본문에서 명시).

**Top-tier conference 적합성 — 58/100 · 추천 venue: CVPR**

세 개의 서로 다른 streaming AR backbone에 걸친 일관된 개선, reconstructor-independent(4DGT) 교차검증, reward-blind LLM judge와 human study까지 포함한 다각도 실험 설계는 top-tier 리뷰를 통과할 만한 empirical rigor를 보여준다. 다만 방법론 자체는 기존 RL 프레임워크(Astrolabe)와 기존 4D reconstructor(MoVieS)를 조합한 reward 재설계 수준의 기여이고, World-R1/VideoGPA가 저자 자체 재구현이라는 점, human study가 LongLive 한 backbone에만 국한된 점이 rejection risk로 작용할 수 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- world model reward 설계에서 '정지가 곧 낮은 오차'가 되는 shortcut은 누리랩의 world model 기반 policy learning·simulation에서도 동일하게 발생할 수 있는 실패 모드로, reward/critic 설계 시 참고할 만한 사례다.
- MoVieS 같은 feed-forward 4D-GS reconstruction을 rollout consistency reward로 쓰는 아이디어는 robot manipulation의 world model rollout 평가(예: 생성된 미래 예측 영상이 물리적으로 타당한지 판별)나 failure detection에 4D consistency score를 활용하는 방향으로 확장 가능하다.
- 저자들이 future work로 언급한 'grading rollouts against explicit action or camera inputs for embodied control'은 VLA/embodied world model 방향과 직접 연결되며, action-conditioned rollout에 4D-consistency reward를 적용하는 후속 연구 아이디어로 발전시킬 수 있다.

---

### 9. [60점] What Matters for Latent Actions in Robot Learning

- **분야**: VLA · **robotics relevance**: 8/10
- **arXiv**: [2608.19613](https://arxiv.org/abs/2608.19613) ([PDF](https://arxiv.org/pdf/2608.19613))
- **저자**: Xizhou Bu, Qingda Hu, Lei Zhou, Lingfeng Zhang, Yingbo Tang, Zihao Liu, Xinyi Tao, Zhiqiang Ma 외 8명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Project page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 58점

> 💡 이 논문은 latent action model(LAM) 연구에서 파편적으로 제안돼온 41가지 design choice(latent action modeling 패러다임, 학습 objective/regularization, latent action integration 전략)를 하나의 autoencoding framework로 통합해 LIBERO, LIBERO-Plus, RoboTwin2.0 세 benchmark와 Franka Panda 실로봇에서 통제된 비교 실험을 수행한다. LAPO가 여전히 가장 강한 baseline임을 보이는 동시에, latent action으로 VLM backbone을 fine-tuning하는 것이 downstream policy 학습에 더 나은 초기화를 제공하며 이 효과가 pretraining 규모 확대에 따라 커진다는 것을 실험으로 뒷받침한다.

**Core innovation & methodology**

- LAM 연구의 파편화 문제를 해결하기 위해 implicit IDM-FDM 계열(LAPO, LAOF, CoMo)과 explicit CFD-AE 계열(ΔRGB, ΔDINO, optical flow 기반)을 동일한 latent dimension과 동일한 autoencoding pipeline으로 재구현해 공정 비교가 가능한 단일 framework로 통합한다.
- Stage I(video만으로 하는 LAM pre-training) → Stage II(latent action으로 VLM backbone fine-tuning, mid-training) → Stage III(robot action data로 downstream policy 학습, post-training)의 3단계 pipeline을 정의하고, 각 단계의 design 선택이 최종 manipulation 성능에 미치는 영향을 분리해서 측정한다.
- 학습 objective/regularization으로 AE, VQ-VAE, VAE, Sparsity, SIGReg 5가지를 다양한 regularization 강도(λ_reg)에서 비교하고, latent action integration 전략으로 DAP(VLM만 fine-tuning 후 폐기), LAP(latent action을 물리 action의 중간 표현으로 사용), JAP(latent action과 물리 action을 공동 예측) 및 그 변형인 JAP-DAP, JAP-LAP까지 5가지를 정의한다.
- latent action 품질을 downstream 실험 없이 빠르게 평가하기 위한 4가지 proxy metric(Linear probe, MLP probe, SSIM Gain, MSE Gain)을 제안하고, 이들이 실제 robotic manipulation 성능과 얼마나 상관되는지 Pearson/Spearman 상관분석으로 검증한다.

**Novelty vs. prior works**

- 개별 LAM 구성요소(LAPO[28], LAOF[33], CoMo[34], StaMo[29]의 ΔDINO, Motus[10]류의 optical flow, VQ-VAE/VAE/SIGReg/Sparsity regularization)는 모두 선행 연구에서 이미 제안된 것이며, 이 논문의 기여는 새로운 architecture나 objective 제안이 아니라 이들을 동일 조건에서 대규모로 통제 비교한 empirical study라는 점에 있다.
- 새로운 representation이나 learning/inference paradigm을 제시하지는 않으므로, novelty는 '새로운 방법'보다는 '체계적 비교와 실용적 guideline 도출'에 있다. 이는 criteria 상 감점 요인인 incremental engineering에 가깝다는 시각과, 가점 요인인 '일반화 가능한 도구(proxy metric 검증, 통합 framework)'라는 시각이 공존한다.
- proxy metric의 신뢰성을 실측 downstream 성능과 대조 검증한 점(Fig. 5, correlation 분석)은 커뮤니티에 실용적 가치가 있으나, 상관계수(r, ρ)의 구체적 수치는 그림에만 제시되고 본문 서술이 발췌 텍스트에서 확인 불가하다.

**Benchmark results**

- Design I(latent action modeling paradigm) 비교에서, latent dim=64, λ_reg=1e-6 조건으로 5가지 integration 전략(DAP/LAP/JAP/JAP-DAP/JAP-LAP) 평균을 3개 benchmark에 걸쳐 낸 순위는 LAPO(0.7327) > ΔDINO(0.7280) > CoMo(0.7167) > ΔRGB(0.6973) > LAOF(0.6907) > SEA-RAFT(0.6433) > RAFT(0.6427)로, LAPO가 별도 전처리 없이 raw data만으로 학습됨에도 최고 성능을 보였다고 저자들은 밝힌다.
- optical flow 기반 방법(RAFT, SEA-RAFT)은 raw data에서 직접 계산한 flow를 그대로 사용했을 때 세 benchmark 모두에서 가장 낮은 성능을 보였고, 단순 pixel 차이인 ΔRGB보다도 낮았다. LAPO에 optical flow 제약을 추가한 LAOF도 LAPO 단독보다 성능이 떨어져(0.888 vs 0.910, LIBERO 평균 기준), optical flow가 latent action 학습에 항상 유리한 inductive bias는 아님을 시사한다.
- Design II(regularization) 비교에서 LIBERO-Plus(zero-shot robustness) 평균은 VQ-VAE(β=1)가 0.517로 다른 방법(VAE 0.433, Sparsity 0.468, SIGReg 0.467, AE 0.445)보다 높았고, RoboTwin2.0 평균은 VAE(λ=1e-7)가 0.859로 가장 높아, benchmark별로 최적 regularization이 달라진다는 점이 raw table에서 확인된다.
- action head architecture 비교(Fig. 4, 3개 benchmark 평균)에서 optical flow 기반 방법은 DAP 사용 시 가장 낮았으나(RAFT 0.590) JAP-LAP 사용 시 개선되고(RAFT 0.669), VQ-VAE(β=1)는 JAP-LAP에서 0.758로 12개 방법 중 최고값을 기록해 latent action integration 전략 선택이 특히 약한 latent action 표현의 성능을 크게 좌우함을 보여준다.
- 저자들은 latent action dimensionality=32가 7-DoF 단일팔과 14-DoF 양팔 platform 모두에서 최고 성능을, FDM reconstruction 기반 proxy metric이 probe 기반 proxy metric보다 신뢰성이 높다는 것을, 그리고 VLM backbone을 latent action으로 fine-tuning하면 real-world Franka Panda 실험과 pretraining scale 확대 모두에서 downstream 성능이 개선된다는 것을 주장하나, 해당 실험의 구체적 수치·표·그래프는 제공된 발췌 텍스트 중 결과 서술 구간이 상당 부분 누락되어 본문에서 확인 불가하다.

**Top-tier conference 적합성 — 58/100 · 추천 venue: CoRL**

41개 design choice를 3개 benchmark와 real-world robot까지 아우르는 대규모 통제 실험으로 검증한 점은 robot learning 커뮤니티에 실질적인 practical guideline을 제공하며, empirical rigor를 중시하는 CoRL/RSS 성격에 부합한다. 다만 새로운 architecture·objective·problem formulation 제안 없이 기존 방법들의 재현·비교에 집중한 empirical study 성격이 강하고, 특정 VLM backbone(Qwen3-VL-4B)과 OpenVLA-OFT 기반 pipeline에 결과가 종속돼 일반화 가능성이 완전히 검증되지 않았다는 점이 top-tier oral 선정에는 감점 요인이 될 수 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- Stage II에서 대량의 unlabeled robot/human video로 VLM backbone을 latent action으로 미리 fine-tuning하는 mid-training 전략은, 별도 action label 없이 시작 가능하다는 점에서 누리랩의 generalist VLA pretraining data 확보 비용을 낮추는 방향으로 참고할 수 있다.
- 저자들이 제안한 4가지 proxy metric(Linear/MLP probe, SSIM Gain, MSE Gain)은 새로운 LAM 변형을 개발할 때 전체 3단계 pipeline을 돌리지 않고 빠르게 1차 선별하는 도구로 활용할 수 있으나, 저자들 스스로도 fine-grained ranking에는 부적합하다고 밝힌 만큼 최종 모델 선택은 실제 policy 평가로 재검증해야 한다.
- latent action과 물리 action을 함께 VLM fine-tuning에 사용하는 JAP/JAP-DAP/JAP-LAP integration 전략은, 누리랩의 failure detection·recovery나 test-time adaptation 연구에서 latent action을 실패 예측·상태 표현용 auxiliary supervision으로 확장하는 아이디어로 이어질 수 있다.

---

### 10. [60점] HiTac-WAM: A Hierarchical Tactile World Action Model for Contact-Rich Robot Manipulation

- **분야**: Manipulation (Tactile World Model) · **robotics relevance**: 9/10
- **arXiv**: [2608.19574](https://arxiv.org/abs/2608.19574) ([PDF](https://arxiv.org/pdf/2608.19574))
- **저자**: Chao Xue, Chaofan Zhang, Wenxuan Ma, Guocai Yao, Shaowei Cui, Shuo Wang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 8 pages, 7 figures, and 3 tables
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 HiTac-WAM은 사전학습된 world action model 위에 tactile branch를 추가해, 각 candidate action chunk의 미래 촉각 상태를 contact → 3D deformation → slip risk 순서의 directed hierarchy로 예측한다. 이 계층적 forecast로 후보 action을 ranking하고, 선택된 forecast를 실행 중 reference로 유지해 편차가 지속되면 replanning을 트리거함으로써 실로봇 contact-rich task 성공률을 31.1%에서 72.2%까지 끌어올렸다고 보고한다.

**Core innovation & methodology**

- contact state, contact-conditioned 3D deformation field, slip risk를 별도 stream이 아니라 물리적 의존관계를 반영한 directed hierarchy로 factorize한다. 각 downstream head는 upstream head의 stop-gradient 신호(contact→deformation, contact+deformation→slip)에 조건화된다.
- directed attention mask를 도입해 tactile query는 video-action context(예측된 시각적 미래 포함)를 attend할 수 있지만, video·action query는 tactile token을 attend하지 못하도록 제한한다. 이를 통해 tactile branch가 기존 pretrained world action model([1], DreamZero)의 video/action 예측 품질을 크게 훼손하지 않으면서 결합된다.
- forecast-guided candidate selection: K개 candidate action chunk에 대해 batched로 tactile forecast를 생성하고, task-progress score와 contact/deformation/slip cost를 가중합한 J(k) = -w_prog·ρ_task + w_C·J_C + w_D·J_D + w_R·J_R 를 최소화하는 후보를 선택한다.
- online forecast verification: 선택된 tactile forecast를 실행 중 reference로 유지하고, 실제 관측과의 편차를 task별로 fitting한 KDE 기반 anomaly score로 모니터링해 지속적 편차 시 안전 후퇴 후 재계획(replanning)을 트리거한다.

**Novelty vs. prior works**

- 가장 가까운 동시대 연구로 Dream-Tac(vision·touch·action 동시 예측), UniTacVLA(tactile latent 예측+online correction), ViTacFormer(future tactile prediction으로 cross-modal representation 학습), VT-WAM, OmniVTA, ViTacWorld 등이 인용되어 있으며, 이들 모두 2026년 arXiv에 올라온 tactile world (action) model 계열로 문제 설정 자체는 이미 여러 그룹이 동시에 다루고 있다.
- 저자가 명시하는 본질적 차이는 새로운 problem formulation이라기보다, contact-deformation-slip을 '하나의 stream에 얽어 넣거나 독립 target으로 다루던' 기존 방식 대비 stop-gradient 기반 directed hierarchy로 명시적 인과 순서를 부여한 architecture적 설계, 그리고 forecast를 candidate ranking과 execution-time verification까지 하나의 파이프라인으로 묶은 점이다.
- 이 hierarchy 설계 자체는 ablation(Table III, Fig. 5)으로 비교적 잘 뒷받침되지만, 근본적으로 새로운 representation이나 learning paradigm이라기보다 기존 pretrained world action model(DreamZero, [1])에 tactile head를 추가하는 architecture-level engineering에 가까워 novelty는 제한적이다.

**Benchmark results**

- Tactile prediction (Table II, 3개 task 평균): contact F1 0.921(범위 0.908-0.931), onset/release MAE 2.1/2.3 frame(30Hz, 약 60-87ms), 3D displacement L2 0.058mm, Top-20 Z MAE 0.076mm, slip AUPRC 0.247(chance level 0.0139).
- Hierarchy ablation(Table III, matched training budget): directed hierarchy가 F1 0.921/3D L2 0.056mm/Top-20 Z 0.072mm/norm ratio 0.97로 전 지표 최고. deformation-only predictor(0.068mm) 대비 3D L2 17.6% 감소, slip-only predictor(AUPRC 0.154) 대비 slip AUPRC 60.4% 상대 개선(0.247). independent heads는 F1(0.896)에서 contact-only(0.903)보다 오히려 낮아, 단순 공유 표현만으로는 부족함을 보여준다.
- Contact intervention 실험(Fig. 5a): deformation head에 주입하는 contact 신호를 GT→predicted→shuffled→zero로 저하시키면 3D L2가 0.053→0.056→0.071→0.078mm로 단조 증가, conditioning이 실제로 사용되고 있음을 확인.
- Real-robot 360-trial 비교(Table I, task당 30 trial): DreamZero(tactile 없는 원본 WAM) 31.1%, Reactive Tactile(current touch만 사용) 40.0%, HiTac-WAM Selection(ranking만) 61.1%, Full HiTac-WAM(ranking+online verification) 72.2%. Fixed K=4 budget에서 tactile-forecast ranking 61.1% vs task-progress ranking 35.6%로 95% Wilson CI가 겹치지 않음([50.8,70.5] vs [26.4,45.8]).
- Online verification: Full 구성 90 trial 중 18건에서 replanning 트리거, 그중 16건이 실제 실행 anomaly와 일치했고 12건은 이후 성공으로 이어짐(2건은 false trigger). tactile branch 추가로 인한 부작용으로 video LPIPS +1.4%, action MAE +0.9%(원 world action model 대비)가 보고된다.

**Top-tier conference 적합성 — 55/100 · 추천 venue: CoRL**

controlled ablation(hierarchy vs independent/contact-conditioned heads, contact intervention)과 신뢰구간을 갖춘 real-robot 비교(360+90 trial)로 empirical conviction은 준수하다. 다만 단일 로봇 플랫폼(IMETA-Y1)·3개 task라는 좁은 검증 범위, DreamZero라는 매우 최근의 미검증 base model에 대한 부가 module 성격의 기여, 그리고 Dream-Tac/UniTacVLA/VT-WAM/OmniVTA/ViTacWorld 등 거의 동시기 유사 연구들과의 직접 비교 부재가 rejection risk로 지적될 수 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- online forecast verification(KDE 기반 anomaly score + persistent deviation trigger replanning)은 누리랩의 failure detection·diagnosis·recovery 및 test-time optimization 주제와 바로 연결되며, tactile 외 다른 modality(force, vision uncertainty)의 execution-time verification으로 일반화할 수 있다.
- contact→deformation→slip의 stop-gradient 기반 directed hierarchy는 world model에서 여러 물리량을 동시에 예측할 때 인과 순서를 부여하는 일반적 설계 패턴으로, VLA나 다른 world model의 auxiliary prediction head 설계에 참고할 수 있다.
- forecast-guided candidate selection(J(k) ranking)은 diffusion/flow 기반 policy의 inference-time planning에 그대로 적용 가능한 구조이므로, 누리랩의 test-time optimization/inference-time planning 연구에서 baseline 혹은 확장 지점으로 활용할 수 있다.

---

### 11. [60점] Learning Highly Dynamic Skills Transition for Quadruped Jumping Through Constrained Space

- **분야**: Legged Locomotion / Hierarchical RL · **robotics relevance**: 7/10
- **arXiv**: [2608.19977](https://arxiv.org/abs/2608.19977) ([PDF](https://arxiv.org/pdf/2608.19977))
- **저자**: Zeren Luo, Jiahui Zhang, Yimin Han, Ji Ma, Minghao Lu, Ioannis Havoutis, Peng Lu
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 15 pages, 12 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 60점

> 💡 AMP 스타일 imitation learning으로 pacing부터 running jump까지 다양한 skill을 하나의 velocity-conditioned low-level policy로 통합하고, RGB-D 기반 gate detection 정보를 받는 high-level policy가 이 skill들을 velocity command로 조합해 실제 Unitree Aliengo 로봇이 몸체 크기와 비슷한 좁은 gate를 공중에서 통과하도록 만들었다. 4족 보행 로봇의 자율적인 aerial narrow-gate traversal을 실제 하드웨어에서 시연한 초기 사례 중 하나라고 주장한다.

**Core innovation & methodology**

- 2단계 hierarchical RL: low-level locomotion policy는 GAN 기반 adversarial imitation learning(AMP 계열)으로 pace/cantering/jumping/steering 등 동물 mocap 데이터를 모방하며, jump 데이터에는 6배 높은 sampling weight를 부여해 고속 점프 학습을 강화한다.
- high-level policy(10Hz)는 low-level(50Hz)을 고정한 상태에서 학습되며, 관측에 gate 중심 방향 벡터, yaw error, gate 내외곽 크기(l_in, l_out)를 포함해 RGB-D 기반 vision detection 결과를 직접 활용한다.
- high-level action은 discrete skill selection이 아니라 연속적인 velocity command(전진속도 v_cmd_x, yaw 각속도 ω_cmd_z) 2차원으로, 이를 통해 low-level skill을 continuous state로 다루어 discrete skill switching에서 생기는 불연속성을 피한다고 주장한다.
- gate detection은 저자들의 기존 연구를 이진화-Canny edge-Douglas-Peucker/Quickhull convex hull 추출 방식으로 gate의 4개 vertex를 찾고 depth 정보와 결합해 3D gate 위치·크기를 추정하는 고전적 CV 파이프라인이다(별도 학습 기반 perception 모델은 아님).

**Novelty vs. prior works**

- 가장 가까운 선행연구는 discrete low-level skill을 학습한 뒤 high-level이 weight(HierGate) 또는 one-hot selection(HierDisc)으로 skill을 전환하는 hierarchical RL 계열이다. 본 논문은 skill을 velocity command라는 연속 space로 암묵적으로 표현해 discrete switching의 불연속성을 없앤 점이 차별점이라고 서술한다.
- 다만 AMP 스타일 imitation learning, hierarchical RL 구조, RGB-D 기반 gate/frame 검출은 모두 저자들 자신 또는 타 그룹의 기존 기법을 재사용한 것으로, 알고리즘 자체의 근본적 novelty는 제한적이다. 핵심 기여는 '좁은 gate를 공중에서 통과'하는 새로운 task formulation과 이를 real hardware에서 통합·검증한 시스템 수준 기여로 보인다.
- narrow gap 통과 자체는 UAV 분야에서는 오래 연구된 문제이고, 4족 로봇의 crouching/squeezing 통과는 선행연구가 있으나(저자도 관련 연구로 인용), aerial phase를 포함하는 dynamic narrow-gate traversal을 실제 legged robot에서 자율적으로 수행한 사례가 드물다는 점이 논문이 내세우는 novelty의 핵심이며, 이는 알고리즘적이라기보다 응용/시스템적 novelty에 가깝다.

**Benchmark results**

- 정량적 baseline 비교는 시뮬레이션에서 E2EBase, E2EStyle, Parkour([6], scandots 기반 E2E), HierGate([17]), HierDisc([18]) 대비 학습 곡선(task reward)과 collision 횟수, calf joint oscillation을 그래프(Fig.8, Fig.9)로 제시하지만, 정확한 수치(성공률, 충돌 횟수 등)는 본문 텍스트에서 확인 불가하며 '유의미하게 더 많은 충돌', 'jerky joint command' 같은 정성적 서술 위주다.
- real robot 실험: 실제 Aliengo(22kg, 최대 torque 약 45Nm)에서 최고 속도 약 2.5 m/s, airborne time 약 0.44초, rear calf joint 140도 이상 굴곡으로 gate edge를 회피했다고 보고한다.
- gate 위치 적응성 테스트에서 y좌표를 1.4m부터 -1.4m까지 0.4m 간격으로 8개 위치에 대해 각 2회씩(총 16회 추정) 반복했고, '모든 trial에서 실패 없이 과제를 완수했다'고 서술한다(정확한 총 시행 횟수는 명시되지 않아 계산값이며, 통계적 유의성 검증은 없음).
- 동적으로 이동하는 gate에 대한 실시간 추종에서 평균 선속도 tracking error 0.0258 m/s, 각속도 tracking error 0.0857 rad/s를 보고한다.
- 일반화 실험(계단, 연속 gap, 경사면 통과 및 hurdle/gap/vertical fence 등 새로운 task로의 확장)은 정성적 시연(Fig.10, 11, 12)으로만 제시되며 성공률 등 정량 지표는 본문에서 확인 불가하다.
- baseline 방법들(E2EBase, Parkour 등)은 시뮬레이션에서만 비교되고 실제 하드웨어에서 직접 비교되지 않아, real-world에서의 성능 우위는 저자의 주장이지 실험적으로 직접 검증된 것은 아니다.

**Top-tier conference 적합성 — 55/100 · 추천 venue: ICRA / IROS**

실제 4족 로봇 하드웨어에서 aerial narrow-gate traversal을 자율적으로 시연한 시스템 논문으로, real-robot demonstration과 hierarchical 구조의 설계 근거(연속 skill representation vs discrete switching)가 실용적 설득력을 가진다. 그러나 알고리즘적 novelty가 기존 AMP/hierarchical RL 기법의 재조합 수준에 머물고, baseline 비교가 시뮬레이션 정성적 그래프 위주이며 실제 실험 환경이 6m×3m MoCap 공간 하나로 제한적이라 CoRL/RSS 급 oral보다는 ICRA/IROS 수준의 system paper에 더 적합해 보인다. Wiley 저널(Supporting Information 문구로 추정) 투고 형식인 점도 conference 적합성 평가와는 별개로 고려할 점이다.

**추천 이유 & 누리랩 연구와의 연결점**

- velocity-conditioned continuous skill abstraction 아이디어는 누리랩의 skill chaining/long-horizon planning 연구에서 discrete skill switching의 불연속성 문제를 다룰 때 참고할 수 있다.
- vision 기반 high-level controller가 low-level skill의 capability를 인지하고 obstacle 정보와 결합해 실시간 의사결정을 내리는 구조는 active perception 및 collision-free trajectory 생성 문제에 적용 가능한 패턴이다.
- AMP 스타일 imitation learning으로 다양한 동물 동작을 하나의 policy에 통합하는 방식은 manipulation이나 다른 embodiment의 diverse skill을 구성할 때 참고할 수 있는 reward engineering(style/task/regularization ratio 설계) 사례로 활용 가치가 있다.

---

### 12. [60점] Causal Reasoning with Bipartite Graphical Causal Models

- **분야**: Causal Inference (Theory) · **robotics relevance**: 3/10
- **arXiv**: [2608.19831](https://arxiv.org/abs/2608.19831) ([PDF](https://arxiv.org/pdf/2608.19831))
- **저자**: Joris M. Mooij
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **Comments**: Figure 2 was added w.r.t. to the published version at Uncertainty in Artificial Intelligence (UAI) 2026
- **원문 검토**: PDF 전문 · 1차 스크리닝 60점

> 💡 순환(feedback) 인과 시스템에서 do(X=x) 개입 표기가 모호해지는 문제를, 변수 노드와 방정식 노드로 이루어진 bipartite graph(BGCM)로 표현해 해결한다. 어떤 방정식이 교체되는지까지 명시하는 do(f_j:X_v=ξ_v)와 새 분리 기준 B-separation을 정의해, 기존 CBN/SCM보다 강한 Markov property와 do-calculus 확장을 도출한다.

**Core innovation & methodology**

- 연립방정식 시스템의 구조를 변수 노드(V)와 방정식 노드(F)로 이루어진 undirected bipartite graph로 표현하는 BGCM(bipartite graphical causal models)을 정의한다.
- Simon의 causal ordering algorithm(perfect matching 기반)을 확장해 bipartite graph에 partial orientation(directed edge와 cluster 내부의 == edge)을 부여하고, cluster 구조로 cyclic causal dependency를 표현한다.
- hard intervention을 do(f_j: X_v=ξ_v) 형태로 정의해 '어떤 방정식이 교체되는지'까지 명시함으로써, 같은 변수를 같은 값으로 고정해도 개입 방식에 따라 결과가 달라지는 do(X=x)의 모호성을 해소한다.
- functional determinism(endogenous cluster가 parent의 결정론적 함수라는 성질)을 이용하는 새 분리 기준 B-separation을 정의하고, 이를 기반으로 global/extended Markov property와 Pearl의 do-calculus 3법칙을 넘어서는 domain invariance 추론 절차를 제시한다.

**Novelty vs. prior works**

- 가장 가까운 선행연구는 Blom et al.(2021)의 causal constraint models로, do(f_j:X_v=ξ_v) 개입 표기 자체는 이미 그 논문에서 제안됐다. 본 논문은 이를 정당화하는 bathtub 시스템의 완전한 case study를 통해 '물리적으로 자연스러운 표현'임을 입증한다.
- Blom et al.이 causal ordering graph와 Markov ordering graph라는 두 개의 별도 그래프를 사용한 것과 달리, 본 논문은 하나의 partially oriented bipartite graph에 causal 구조(cluster·edge 방향)와 conditional independence 구조(B-separation)를 통합해 표현한다.
- 저자는 B-separation이 Blom et al.의 d-separation 기반 Markov property보다 strictly 강하다고 주장하지만, footnote 7에서 이 결과가 Markov ordering graph에 대한 D-separation(Geiger et al. 1990)을 적용한 것과 동치임을 스스로 인정한다. 즉 도출되는 conditional independence 집합 자체의 새로움보다는 '단일 그래프로의 통합 표현'이 핵심 novelty다.
- non-random input을 다루는 extended Markov property(Forré의 transitional conditional independence 활용)와 이를 이용한 do-calculus 확장(도메인 불변성 추론, Examples 21-24)은 Blom et al.(2021)에 없는 부분으로, 본 논문 고유의 기여로 판단된다.

**Benchmark results**

- 이 논문은 실험/벤치마크가 없는 순수 이론 논문이다. 검증은 bathtub 평형계(endogenous 변수 X_O, X_P, X_D 3개, exogenous 변수 X_I, X_K, X_g 3개) 하나에 대한 완전한 해석적 case study로 이루어진다.
- Table 1에서 가능한 9가지 hard intervention 조합(f_1/f_2/f_3 × X_O/X_P/X_D) 중 실제로 uniquely solvable한 조합을 판별했고, Table 2에서 각 intervention의 solution function을 닫힌 형태로 유도했다.
- do(f_1:X_D=ξ_D), do(f_2:X_D=ξ_D), do(f_3:X_D=ξ_D) 세 가지가 모두 X_D=ξ_D를 만족하지만 X_O, X_P 값이 서로 다름을 수식으로 명시적으로 보여, 표준 do(X=x) 표기의 모호성을 구체적으로 입증했다(Example 20).
- domain invariance 응용에서 observational 분포와 do(X_g=ξ_g), do(f_3:X_D=ξ_D) 등 4개 사례(Examples 21-24) 중 3개는 새 Markov property로 invariance를 도출했고, 1개(Example 23, do(f_1:X_D=ξ_D))는 전체 시스템이 하나의 cluster로 묶여 invariance를 도출할 수 없음을 보였다.
- 경제 시장(supply-demand), 전자회로, 생화학 반응망 등 다른 응용 도메인은 가능성만 언급되며, 실제 적용 사례나 정량적 결과는 본문에서 확인 불가(Appendix H 언급은 있으나 발췌 범위 내 세부 내용 확인 불가).

**Top-tier conference 적합성 — 55/100 · 추천 venue: UAI**

graphical causal inference 이론 커뮤니티(UAI, JMLR)의 관심사에 정확히 부합하며, 실제로 UAI 2026에 이미 accept됐다고 comments에 명시돼 있다(criteria에 따라 이 사실과 독립적으로 평가함). 다만 novelty의 상당 부분이 Blom et al.(2021) 프레임워크의 재구성·통합에 해당하고 검증이 toy example 하나에 그쳐, NeurIPS/ICML 등 더 넓은 top-tier venue에서는 impact 대비 다소 좁은 스코프로 평가될 위험이 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- BGCM의 do(f_j:X_v=ξ_v) 개입 표기는 로봇이 물리적 actuation을 수행할 때 '어떤 메커니즘을 통해 목표 상태에 도달했는가'를 구분하므로, failure diagnosis나 counterfactual policy 평가에서 개입 모호성을 정리하는 이론적 참고 틀이 될 수 있다.
- cyclic causal dependency(feedback loop)를 다루는 프레임워크라는 점에서, contact-rich manipulation이나 force control처럼 실시간 피드백이 지배적인 로봇-환경 상호작용의 인과 모델링에 이론적 기반을 제공할 수 있다.
- B-separation과 do-calculus 확장은 world model 학습에서 sim-to-real이나 task shift 같은 도메인 간 invariance를 그래프 기반으로 식별하는 데 응용 아이디어를 줄 수 있으나, 현재는 저차원 결정론적 방정식계에 한정돼 고차원 학습 기반 world model에 직접 적용하려면 추가 연구가 필요하다.

---

### 13. [60점] Evidence-Gated Task and Motion Planning with Vision-Language Models

- **분야**: TAMP / Embodied AI (VLM-guided Task and Motion Planning) · **robotics relevance**: 9/10
- **arXiv**: [2608.20084](https://arxiv.org/abs/2608.20084) ([PDF](https://arxiv.org/pdf/2608.20084))
- **저자**: Tsunehiko Tanaka, Matthew Stephenson, Alistair Macvicar, Edgar Simo-Serra
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 VLM이 먼저 문을 열거나 가림물체를 치우는 등의 exploratory subgoal로 시각적 evidence를 모으고, feasibility gate가 이 evidence를 보고 planning 진행·추가 탐색·halt 중 하나를 결정하는 EAFG를 제안한다. Cooking 시뮬레이션에서 underspecified goal의 recipe completion을 크게 높이고 missing-object goal에서는 불필요한 조작 시도를 줄이며 적절히 halt하는 것을 보였다.

**Core innovation & methodology**

- Task planning 이전에 별도의 evidence-acquisition 단계를 두어, VLM이 문/서랍 열기 등 reversible한 exploratory subgoal 시퀀스 G^EA_t를 생성하고 TAMP(PDDLStream)로 실행해 관찰 이미지를 수집한다.
- 실행 후 관찰들을 시간순 image collage로 합쳐 VLM에 제공하고, VLM이 evidence state E_t=(H_t, O_t, F_t)(실행 이력, 관찰 요약, 유지되는 findings)를 매 iteration마다 append가 아니라 재생성(outdated/모순 정보 제거)하는 방식으로 갱신한다.
- Feasibility Gating 모듈이 목표 G_eng와 E_t, collage I_t를 보고 ready_to_plan / need_more_evidence / halt 세 상태 중 하나를 출력한다. need_more_evidence면 같은 inference step에서 다음 탐색 subgoal을 바로 생성해 루프를 돈다(최대 5회).
- ready_to_plan이 나오면 최종 evidence state E_T를 자연어 텍스트 context로 VLM-TAMP의 subgoal generation 모듈 Π에 그대로 append하여 evidence-conditioned planning을 수행한다(Π는 기존 VLM-TAMP를 그대로 재사용).

**Novelty vs. prior works**

- 가장 가까운 prior work인 VLM-TAMP[3]와 Kumar et al.[4]은 완전 관측 가능한 object-oriented state를 가정하고 현재 표현된 scene에서 바로 subgoal을 생성한다. 이 논문은 그 이전 단계에 '언제 planning을 시작해도 되는지'를 능동적으로 판단하는 gate를 추가한 것이 핵심 차이다.
- POMDP/belief-space TAMP 계열(Garrett et al. 2020, Phiquepal & Toussaint 2019)도 partial observability를 다루지만 확률적 belief 표현과 최적화 기반 접근인 반면, 본 논문은 VLM의 자연어 추론만으로 evidence 충분성을 판단하는 prompting 기반 방식이라 이론적 보장은 없고 순수히 경험적 검증에 의존한다.
- VerifyLLM[21]은 사후(post-hoc) plan 검증인 반면 이 논문은 사전(pre-planning) 능동 정보 수집이라는 점에서 다르지만, 메커니즘 자체는 새로운 학습 패러다임이라기보다 기존 VLM-TAMP 파이프라인 앞에 iterative VLM prompting 기반 evidence loop를 얹은 조합적 설계에 가깝다. Problem formulation은 새롭지만 architecture적으로는 기존 요소(VLM subgoal 생성, TAMP, VLM 상태 업데이트)의 재조합 성격이 강하다.

**Benchmark results**

- 단일 시뮬레이션 kitchen 환경(치킨 수프 요리, VLM-TAMP[3]에서 쓰인 벤치마크)에서 GPT-5.5와 Gemini-3.5-Flash 두 VLM에 대해 EAFG 유무를 비교했으며, 각 조건당 20회 실행.
- S2(underspecified goal, 'make chicken soup'): Recipe CR이 GPT-5.5는 0.05→0.40, Gemini-3.5-Flash는 0.00→0.20으로 상승. salt/pepper step CR도 GPT-5.5 0.10→1.00, 0.30→1.00, Gemini 0.05→0.95, 0.05→0.85로 크게 개선.
- S3(explicit-but-missing, carrot 부재): Halt SR이 GPT-5.5 0.45→0.90, Gemini 0.40→1.00으로 상승했고, Missing-object Attempt Count는 GPT-5.5 4.00→0.55, Gemini 2.40→0.00으로 감소.
- S1(explicit-and-present, 목표 물체가 명시되고 실제 존재): GPT-5.5는 Recipe CR 0.20→0.45로 개선되었지만 Gemini-3.5-Flash는 오히려 0.15→0.10으로 소폭 악화되었고, GPT-5.5의 water step CR도 0.80→0.55로 하락하는 등 EAFG가 항상 이득이 아님을 저자도 명시.
- Real-robot 실험은 본문에서 확인 불가(시뮬레이션 kitchen 환경만 사용). Baseline은 VLM-TAMP[3] 단일 비교뿐이며, feasibility gate 자체의 구성요소(예: evidence state 재생성 vs append, collage 유무)를 분리한 ablation은 본문에서 확인 불가.

**Top-tier conference 적합성 — 45/100 · 추천 venue: CoRL**

TAMP와 VLM 결합에서 pre-planning evidence gating이라는 명확하고 실용적인 문제 설정을 제시하고 halt 판단·attempt count 감소라는 정량적 개선을 보여준 점은 CoRL/ICRA 워크숍 또는 짧은 페이퍼 수준으로는 설득력이 있다. 다만 단일 시뮬레이션 kitchen 시나리오, 단일 baseline(VLM-TAMP) 비교, real-robot 검증 부재, S1에서 Gemini 성능 악화 등 실험 범위와 견고성이 top-tier main track(리뷰어가 요구하는 다양한 환경·multi-baseline·ablation) 기준에는 미치지 못해 desk-reject 또는 major revision 위험이 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- Evidence-acquisition subgoal 생성과 feasibility gate 아이디어는 누리랩의 failure detection/recovery, test-time inference-time planning 주제와 직결된다. 특히 'need_more_evidence' 루프는 test-time에 추가 탐색을 할지 즉시 실행할지 결정하는 general한 inference-time optimization 패턴으로 확장 가능하다.
- 문을 열거나 가림물체를 치우는 exploratory subgoal은 active perception/NBV(next-best-view) 문제와 본질적으로 유사하다. Image collage 대신 object-centric 3D/4D representation이나 scene graph를 evidence state에 결합하면 더 정교한 spatial reasoning이 가능할 것으로 보인다.
- Evidence state E_t=(H_t,O_t,F_t)의 재생성 방식은 robot memory 설계에 참고할 만하다. 단기 evidence를 넘어 여러 task episode에 걸친 장기 memory로 확장하고, halt 이후의 human-in-the-loop 또는 대체 계획 생성으로 이어지는 counterfactual reasoning 결합을 검토할 수 있다.

---

### 14. [58점] Learning Hierarchical Skill Policies with Offline Quality-Diversity Reinforcement Learning

- **분야**: RL (Offline-to-Online Hierarchical Skill Learning) · **robotics relevance**: 8/10
- **arXiv**: [2608.19684](https://arxiv.org/abs/2608.19684) ([PDF](https://arxiv.org/pdf/2608.19684))
- **저자**: Tanachai Anakewat, Takayuki Osa, Tatsuya Harada
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **Comments**: IROS 2026
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 QDOS는 IQL로 학습한 value function에서 얻은 trajectory segment의 advantage로 skill extraction과 diversity 목적함수에 가중치를 주는 Advantage-Weighted Quality-Diversity VAE를 제안해, 노이즈·실패 사례가 섞인 offline dataset에서 고품질·다양한 low-level skill을 뽑아낸다. 이 skill을 SUPE의 dual dataset reuse(pseudo-labeling) 전략과 결합해 offline-to-online RL을 수행하며, antmaze/antsoccer/kitchen/humanoidmaze/scene 등 sparse-reward benchmark에서 SUPE 대비 normalized return과 첫 목표 도달 속도를 개선했다고 보고한다.

**Core innovation & methodology**

- 문제 설정: 기존 offline skill extraction(OPAL, SPiRL, SUPE의 trajectory VAE)은 dataset 내 optimal trajectory와 noise·실패 시도를 구분하지 않고 균등하게 reconstruct해, 유용한 skill과 무의미한 skill이 뒤섞인 'cluttered skill space'가 생긴다는 점을 문제로 지목한다.
- Advantage 추정: 고정 길이 H=20 segment마다 IQL(expectile regression, τ=0.9)로 학습한 Vψ(s)와 target critic Qψ̂로 advantage A(τ)를 추정하고, weight w(τ) ∝ exp(A/λ)를 계산해 high-advantage segment에 높은 가중치를 부여한다.
- Weighted VAE objective(L_AW_VAE): encoder fθ(z|τ), state-conditioned prior pθ(z|s0), decoder(저수준 policy) πθ(a|s,z)로 구성된 VAE의 reconstruction term을 advantage weight로 스케일링하고 KL(β=0.1~0.2) 정규화를 결합한다.
- Mutual information 항(Linfo)도 동일한 advantage weight를 곱해, mode collapse를 막는 diversity 유도가 고품질 behavior 안에서만 이뤄지도록 제한한다. 이후 SUPE와 동일하게 pretrained encoder로 offline segment의 skill을 pseudo-label하고 RND 기반 UCB로 optimistic reward를 추정해 high-level replay buffer(offline+online 50/50 sampling)에 채우고, SAC/RLPD 계열 off-policy 알고리즘으로 high-level policy πψ(z|s)를 학습한다.

**Novelty vs. prior works**

- 가장 가까운 선행연구는 DiveOff(Osa & Harada, ICML 2024, quality-diversity offline RL)와 SUPE(Wilcoxson et al., 2024/2025, offline-to-online dual dataset reuse)이며, 저자도 본문에서 'Our work builds upon DiveOff'라고 명시한다. QDOS의 핵심 기여는 DiveOff의 QD variational objective에 IQL 기반 advantage weighting을 추가한 것이고, Phase 2(pseudo-labeling, RND optimistic reward, offline/online 50/50 replay)는 SUPE의 파이프라인을 그대로 채택했다.
- 즉 QDOS는 'IQL advantage weighting + DiveOff QD-VAE + SUPE dual reuse'의 결합이며, 완전히 새로운 architecture·representation·learning paradigm을 제시하기보다는 advantage-weighted regression(AWR) 계열 아이디어를 skill discovery 단계에 적용한 확장에 가깝다. 개념적 참신성보다는 solid한 engineering 결합으로 보인다.
- component-level ablation(advantage weighting만 제거, diversity term만 제거 등)은 본문에 제시되지 않고, mutual information weight α_loss에 대한 민감도 분석만 있어 각 구성 요소의 개별 기여는 검증되지 않는다.

**Benchmark results**

- Table I(정규화 return, SUPE·QDOS는 3 seed 평균 — 단 IV-C절 Implementation Notes는 'averaged over 5 random seeds'라 기재해 seed 수에 내부 불일치가 있다): antmaze-large SUPE 83.0±21.0 → QDOS(α=0.3) 96.0±6.0, antsoccer-arena SUPE 27.0±31.0 → QDOS(α=0.3) 80.0±10.0(개선폭 최대이자 variance도 크게 감소), humanoidmaze-medium SUPE 97.0±6.0 → QDOS(α=0.3) 100.0±0.0.
- kitchen-mixed는 SUPE 85±13.25 대비 QDOS(α=0.2) 100.00±0.00로 완전 해결을 보였으나, QDOS(α=0.3)는 83.25±28.75로 오히려 SUPE와 비슷하거나 variance가 더 커, 동일 방법이라도 diversity weight 설정에 성능이 크게 좌우된다. kitchen-partial, scene-task1은 SUPE와 QDOS 성능 차이가 크지 않거나(둘 다 100.0±0.0으로 ceiling effect) overlap 구간이 넓다.
- Table II(첫 목표 도달까지 step 수): antmaze-large SUPE 13334±5774 → QDOS 11668±9465, humanoidmaze SUPE 23334±6292 → QDOS 19168±8036, scene SUPE 5834±1443 → QDOS 5001±0. 평균은 QDOS가 일관되게 빠르지만 표준편차가 평균과 비슷하거나 더 커서 통계적 유의성 검정 결과는 본문에서 확인 불가.
- Hyperparameter 민감도: antsoccer처럼 solution space가 넓은 task는 높은 α_loss(0.3)가, kitchen처럼 optimal behavior가 제한적인 task는 중간 α_loss(0.2)가 낫다는 task-dependent trade-off를 보고한다.
- Failure case: cube-single/cube-double 같은 고품질·구조화된 dataset에서는 α_loss를 낮출수록 QDOS 성능이 SUPE baseline에 수렴한다고 서술하나(Fig. 5, 정성적 서술), 구체적 수치·표는 본문에서 확인 불가.

**Top-tier conference 적합성 — 52/100 · 추천 venue: IROS / ICRA (또는 CoRL)**

6개 sparse-reward domain(antmaze, antsoccer, humanoidmaze, kitchen-mixed/partial, scene)에서 다수 baseline(SUPE, ExPLORe, trajectory skills, IQL, BC, Diffusion BC+JSRL)과 비교하고 hyperparameter 민감도 분석·latent space 시각화(t-SNE)까지 갖춘 점은 강점이다. 다만 novelty가 DiveOff와 SUPE의 결합에 가깝고, seed 수 기재 불일치(3 vs 5), 일부 결과의 큰 표준편차와 ceiling effect, real-robot 검증 부재, component-level ablation 미비가 rejection risk로 작용해 top-tier(NeurIPS/ICML/CoRL) oral보다는 IROS/ICRA 수준의 solid contribution에 가깝다.

**추천 이유 & 누리랩 연구와의 연결점**

- Advantage-weighted skill extraction은 누리랩의 offline-to-online RL, skill chaining/long-horizon manipulation 연구에서 mixed-quality demonstration dataset을 다룰 때 저품질·실패 궤적을 자동으로 down-weight하는 pretraining 기법으로 바로 참고할 수 있다.
- IQL advantage 기반 weighting을 failure detection·diagnosis에 응용해, teleoperation이나 autonomous collection으로 모은 대규모 demonstration에서 실패 segment를 자동 식별·필터링하는 전처리 단계로 확장하는 아이디어를 검토할 수 있다.
- pseudo-labeling + RND 기반 optimistic reward 조합은 world model 기반 test-time planning/exploration에서 offline data를 온라인 replay buffer로 재활용하는 설계 참고 사례가 된다.

---

### 15. [42점] Towards Surgical World-Action Modeling: A Preliminary Joint Visual-Trajectory Forecasting for Surgical Motion Planning

- **분야**: World Model · **robotics relevance**: 8/10
- **arXiv**: [2608.20284](https://arxiv.org/abs/2608.20284) ([PDF](https://arxiv.org/pdf/2608.20284))
- **저자**: Weiliang Huang, Huanrong Liu, Bob Zhang, Qi Dou, Zhen Chen, Yun Gu, Guy Rosman, Qingbiao Li
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 58점

> 💡 수술 영상의 미래 시각 상태와 2D 기구 궤적을 하나의 모델로 동시에 예측하는 preliminary surgical world-action model을 제안한다. 15-step을 한 번에 예측하는 대신 3-step chunk를 5번 반복하는 autoregressive rollout을 적용해, 첫 segment 기준 PSNR을 18.86에서 23.11dB로, ADE를 45.77에서 22.22 pixel로 개선했다.

**Core innovation & methodology**

- 수술 planning에서 흔히 분리돼 다뤄지던 'future scene generation'과 'instrument trajectory prediction'을 하나의 joint world-action model로 묶는 problem formulation을 제시한다.
- Frozen SurgMotion ViT-L encoder에서 mid-layer(국소 외형)와 final-layer(고수준 semantic/motion) visual token을 동시에 추출하고, 2D 기구 좌표를 MLP로 임베딩한 뒤 spatial broadcast로 융합해 shared visual-motion representation을 구성한다.
- Temporal-spatial encoder로 5-step history를 인코딩한 뒤, 두 개의 head로 분기한다: visual head는 마지막 관측 상태 대비 residual ΔZ를 예측하고, trajectory head는 constant-velocity prior(직전 두 점의 속도로 외삽) 위에 residual correction을 더해 최종 좌표를 낸다.
- 15-step 전체를 한 번에 예측하는 대신, 3-step chunk를 5회 반복하는 chunked autoregressive rollout을 쓰고, scheduled sampling(epoch 8부터 시작, epoch 45에 predicted-state 확률 0.75 도달)으로 train-inference 간 exposure bias를 줄인다.

**Novelty vs. prior works**

- 가장 가까운 prior work는 SurgWMBench를 만든 동일 그룹의 벤치마크 논문과 surgical video generation 계열(HieraSurg, SurgSora, SurGen), trajectory-only 계열(Shi et al. IROS'22, ImitateCholec)이다. 이 논문의 차별점은 두 task를 한 backbone에서 동시에 예측해 trajectory-level로 직접 평가 가능하게 만든 점이다.
- 다만 개별 구성요소는 새롭지 않다: constant-velocity prior + residual correction은 trajectory forecasting에서(e.g., Social-GAN 계열) 널리 쓰이는 기법이고, scheduled sampling도 Bengio et al. 2015의 기존 기법을 그대로 가져온 것이다. Visual encoder(SurgMotion)도 frozen 상태로 재사용한다.
- 저자 스스로 'preliminary'라고 명시하듯, 새로운 architecture/objective/inference paradigm 제안이라기보다는 기존 구성요소들을 surgical world-action modeling 문제에 처음 결합해 본 초기 feasibility study에 가깝다.

**Benchmark results**

- SurgWMBench(SAR-RARP50 기반, RARP 수술 영상, suturing motion, 1,637 segment / 32,740 frame) 단일 벤치마크에서만 평가했다. 5-frame history로 15-step 미래를 예측하는 protocol을 사용한다.
- 비교 대상은 저자 자신의 두 설정(direct one-shot vs chunked rollout)뿐이며, 외부 baseline(다른 surgical world model이나 trajectory predictor)과의 정량 비교는 본문에서 확인 불가하다.
- 첫 segment(t+1:3) 기준: PSNR 18.859→23.105dB, SSIM 0.4713→0.7971, LPIPS 0.6045→0.1783(70.5% 감소), ADE 45.77→22.22px, FDE 49.47→31.64px로 chunked rollout이 direct 대비 크게 개선됐다.
- 마지막 segment(t+13:15) 기준: PSNR 16.872→17.982dB, SSIM 0.4264→0.6343, LPIPS 0.6244→0.3047, ADE 195.27→158.52px(약 18.8% 감소), FDE 208.04→172.12px(약 17.3% 감소)로 개선폭은 유지되나 절대 성능은 크게 저하됐다.
- Chunked rollout 내에서도 segment가 진행될수록 PSNR이 23.105→17.982dB로, ADE가 22.22→158.52px로 뚜렷하게 악화되는 것을 저자들이 직접 확인했다. Long-horizon에서의 visual degradation과 trajectory error 누적은 저자가 명시한 한계이며, 이를 해소하는 추가 기법(uncertainty modeling 등)은 아직 적용되지 않았다.

**Top-tier conference 적합성 — 22/100 · 추천 venue: MICCAI Workshop**

본문에 포함된 anonymized 코드 저장소 이름(MICCAI2026_Workshop_EndoLINA)에서 드러나듯 MICCAI 워크숍 제출을 겨냥한 preliminary study로 보인다. 단일 데이터셋, 자체 ablation(direct vs chunked) 외 외부 baseline 비교 부재, 저자 스스로 'preliminary'라 명시한 점 때문에 CVPR/ICCV/NeurIPS/CoRL/RSS급 main track에는 적합하지 않다. Real-robot 실험이나 3D/전신 기구 pose가 아닌 2D anchor point 궤적만 다루는 점도 rejection risk로 작용할 수 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- Joint world-action(visual+trajectory) formulation과 chunked autoregressive rollout + scheduled sampling 조합은 누리랩의 world model / long-horizon planning 연구에서 짧은 horizon chunk 단위로 rollout해 error accumulation을 줄이는 아이디어로 참고할 수 있다.
- Constant-velocity prior 위에 residual을 학습하는 trajectory head 설계는 action decoder에 explicit physical prior를 주입하는 test-time/inference-time 기법으로, VLA의 action head 설계에 응용 가능하다.
- Long-horizon에서 시각 degradation과 궤적 오차가 함께 누적되는 현상은 failure detection/recovery 연구와 연결지어, chunk 경계에서 예측 불확실성을 감지해 재계획(replanning)하는 후속 연구 아이디어로 확장할 수 있다.

---

## 오늘의 핵심 연구 트렌드 종합

- **Tactile-aware world/action model의 부상** — [HiTac-WAM](https://arxiv.org/abs/2608.19574)은 contact→deformation→slip을 directed hierarchy로 예측해 candidate action ranking과 execution-time replanning에 쓰고, [DECOWAM](https://arxiv.org/abs/2608.20114)은 pretrained video-action backbone을 얼린 채 legged mobile manipulation에 특화된 whole-body world-action model을 소규모 adapter로 구축한다. [The Missing Touch](https://arxiv.org/abs/2608.19372)는 반대편에서 human teleoperator에게 국소 접촉 변형을 그대로 렌더링해 demonstration 품질 자체를 높인다. 세 논문 모두 touch modality를 world model/policy 파이프라인에 명시적으로 결합하는 방향으로 수렴한다.
- **Frozen VLA/world-action backbone + 소규모 module 추가라는 공통 레시피** — DECOWAM(25.95M adapter), HiTac-WAM(tactile head), [EXIMO](https://arxiv.org/abs/2608.19891)(residual RL on top of GROD), [Fine-Tuning VLAs with Self-Demonstrated Generative Control](https://arxiv.org/abs/2608.19490) 모두 대형 pretrained backbone을 그대로 두고 그 위에 lightweight 모듈이나 self-collected data로 embodiment/task를 확장하는 parameter-efficient adaptation 전략을 택한다.
- **Teleoperation·인간 개입 없는 self-supervised data 수집 파이프라인** — EXIMO(VLM orchestration으로 rollout 생성 후 SFT distill), Fine-Tuning VLAs(frozen base policy의 self-rollout을 generative replay로 사용), [Video2DoorTraversal](https://arxiv.org/abs/2608.20251)(simulation-in-the-loop agent가 diagnose-refine loop로 expert demo를 자동 생성)까지, teleoperation 의존을 줄이려는 시도가 오늘 top 논문의 절반 가까이를 차지한다.
- **Advantage/value 기반 가중치로 offline data 품질을 자동 정제** — [RoMAN-Flow](https://arxiv.org/abs/2608.20208)의 NF-IQL과 [QDOS](https://arxiv.org/abs/2608.19684)의 advantage-weighted QD-VAE 모두 IQL 계열 value function으로 noisy offline dataset에서 고가치 segment/behavior만 골라 학습한다는 점에서 같은 원리를 서로 다른 policy class(flow, skill-VAE)에 적용한 사례다.
- **VLM을 능동적 정보 수집·안전 게이트로 쓰는 embodied reasoning** — [Evidence-Gated TAMP](https://arxiv.org/abs/2608.20084)는 planning 전에 VLM이 스스로 탐색 subgoal을 만들어 evidence를 모으고, [SafeBranch](https://arxiv.org/abs/2608.19729)는 actor의 unsafe rollout을 rollback해 critic feedback으로 안전 대안을 만든 뒤 이를 학습에만 쓰고 배포 시에는 critic 없이 동작하게 한다. 둘 다 '판단 비용을 언제 지불할 것인가'(inference-time 탐색 vs 학습 시 1회)라는 공통 질문을 다룬다.
- **개별 novelty는 제한적이나 systems-level integration으로 승부하는 논문이 다수** — Video2DoorTraversal, DECOWAM, HiTac-WAM, EXIMO 등 top-score 논문 다수가 기존 구성요소(articulated asset generation, adversarial disentanglement, residual RL, VLM orchestration)의 재조합이며, 완전히 새로운 representation·paradigm보다 문제 설정과 실전 검증(real-robot 실험)의 완성도로 점수를 얻었다.

## 유망 연구 방향 및 프로젝트 제안

**Tactile forecast 기반 online failure detection 모듈**
- research question: contact-rich manipulation 중 촉각 forecast와 실제 관측의 편차를 실시간으로 감지해 replanning을 언제 트리거할지 일반화할 수 있는가?
- 접근·novelty: HiTac-WAM의 KDE 기반 anomaly score를 force/vision uncertainty 등 다른 modality로 확장하고, 여러 modality의 anomaly score를 결합한 multi-modal failure diagnosis 모듈을 설계한다.
- 왜 지금·경쟁 prior works: Dream-Tac, UniTacVLA, ViTacFormer 등 2026년 동시다발적으로 tactile world model이 제안되고 있어 differentiation이 필요한 시점이다. HiTac-WAM의 forecast-guided candidate selection을 baseline으로 확장 가능.
- risk·target venue: 여러 modality의 anomaly score를 어떻게 결합할지에 대한 이론적 근거가 약할 위험이 있다. CoRL/ICRA 타깃.

**VLM 기반 evidence-gating을 3D/scene graph로 확장**
- research question: image collage 대신 object-centric 3D/4D representation이나 scene graph를 evidence state로 쓰면 evidence-gated TAMP의 spatial reasoning 정확도가 개선되는가?
- 접근·novelty: Evidence-Gated TAMP(EAFG)의 evidence state E_t=(H_t,O_t,F_t)를 scene graph 기반으로 재구성하고, need_more_evidence 루프를 active perception/NBV 문제로 재정식화한다.
- 왜 지금·경쟁 prior works: EAFG는 순수 prompting 기반이라 이론적 보장이 없다는 한계가 있어, 구조화된 표현을 결합하면 실험적으로도 강한 차별화가 가능하다.
- risk·target venue: 3D representation 구축 비용이 evidence loop의 반응 속도를 저해할 위험. CoRL/RSS.

**Rollback 기반 safety alignment의 world-model 근사화**
- research question: SafeBranch의 environment rollback을 실제 로봇에서 재현 불가능한 문제를, world model 기반 approximate rollback으로 대체할 수 있는가?
- 접근·novelty: world model rollout으로 counterfactual한 safe/unsafe branch pair를 생성해 BranchPO 스타일 학습을 offline world model 위에서 수행한다.
- 왜 지금·경쟁 prior works: SafeBranch는 시뮬레이션 rollback을 전제하므로 real-robot deployment로 직접 확장이 어렵다는 명시적 한계가 있다.
- risk·target venue: world model의 rollout 정확도가 낮으면 safety pair 품질이 오염될 위험이 큼. EMNLP/CoRL.

**Advantage-weighted skill/action 정제 기법을 VLA post-training에 통합**
- research question: RoMAN-Flow의 NF-IQL(sampling-free advantage-weighted likelihood)과 QDOS의 advantage-weighted skill extraction을 VLA flow-matching post-training에 결합하면 noisy demonstration에서 sample efficiency를 더 높일 수 있는가?
- 접근·novelty: diffusion/flow 기반 VLA의 action head에 advantage-weighted likelihood objective를 적용하고, one-step distillation으로 배포 latency를 줄인다.
- 왜 지금·경쟁 prior works: 두 논문 모두 exact-likelihood 또는 skill-level advantage weighting이 offline RL/IL에서 실증됐으나 VLA 규모로는 아직 검증되지 않았다.
- risk·target venue: 대규모 VLA에서 exact likelihood 계산 비용이 커질 위험. CoRL/ICML.

**Single-video real-to-sim 파이프라인을 articulated object 일반으로 확장**
- research question: Video2DoorTraversal의 DoorTwin(single RGB video → simulation-ready articulated digital twin)을 drawer, cabinet 등 다른 articulated object class로 일반화할 수 있는가?
- 접근·novelty: object class에 무관한 articulation reconstruction과 simulation-in-the-loop diagnose-refine loop를 결합해 teleoperation-free expert demonstration 생성을 확장한다.
- 왜 지금·경쟁 prior works: 저자들이 door에 특화된 파이프라인만 검증했고, UniDoorManip/ArticuBot 등은 개별 요소만 다뤄 통합된 일반화 사례가 없다.
- risk·target venue: articulation type마다 reconstruction 실패 모드가 달라 범용성 확보가 관건. CoRL/ICRA.

## 오늘 반드시 읽어야 할 논문

- [RoMAN-Flow: Taming Autoregressive Normalizing Flows for Offline Reinforcement Learning in Robotic Manipulation](https://arxiv.org/abs/2608.20208) — exact-likelihood AR normalizing flow로 offline RL을 sampling-free하게 만들고 one-step distillation으로 8.55배 가속까지 real-robot에서 검증했다.
- [EXIMO: VLM Guided Exploration of VLA Policies](https://arxiv.org/abs/2608.19891) — teleoperation 없이 VLM이 VLA를 orchestration해 장기·조합 task 데이터를 스스로 모으고 distill하는 3단계 파이프라인이 ablation으로 각 단계 기여를 명확히 보여준다.
- [DECOWAM: Decoupled Whole-Body World-Action Model for Legged Mobile Manipulation](https://arxiv.org/abs/2608.20114) — legged mobile manipulation 전용 world-action model이 드문 가운데, base/arm/ego-motion을 explicit factor로 분리한 problem formulation과 새 real-robot 데이터셋 ARMDOG를 함께 제시한다.
- [Video2DoorTraversal: Push Door Traversal via Simulated Door Twins](https://arxiv.org/abs/2608.20251) — 단일 RGB 비디오만으로 articulated digital twin을 만들어 teleoperation-free demonstration을 생성하고 real-robot door traversal에서 96.57% 성공률을 보였다.
- [Stream4D: 4D-Consistency for Streaming Autoregressive Diffusion Video Models](https://arxiv.org/abs/2608.19556) — static 3D-GS reward가 streaming video RL에서 motion을 정지시키는 reward hacking을 명확히 진단하고 4D-GS 기반 reward로 해결한 사례 분석이 세 backbone 모두에서 일관되게 재현된다.
- [SafeBranch: Branch-Pair Safety Alignment for Embodied Agents](https://arxiv.org/abs/2608.19729) — actor 자신의 unsafe rollout을 rollback해 안전 대안을 self-collect하고 배포 시 critic 없이 동작하게 만드는 데이터 구성법이 IS-Bench에서 SSR을 9배 가까이 개선했다.
- [HiTac-WAM: A Hierarchical Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2608.19574) — contact-deformation-slip을 인과 순서대로 예측하는 tactile world model이 online forecast verification으로 real-robot 성공률을 31.1%에서 72.2%까지 끌어올렸다.
- [Evidence-Gated Task and Motion Planning with Vision-Language Models](https://arxiv.org/abs/2608.20084) — planning 전에 VLM이 스스로 탐색해 evidence를 모으고 언제 시작할지 결정하는 feasibility gate는 test-time inference-time planning 연구에 바로 응용 가능하다.
- [What Matters for Latent Actions in Robot Learning](https://arxiv.org/abs/2608.19613) — 41가지 latent action model design choice를 통제 비교한 대규모 empirical study로, VLM backbone을 latent action으로 mid-training하는 전략의 효과를 실험적으로 뒷받침한다.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (269편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2608.20208'>RoMAN-Flow: Taming Autoregressive Normalizing Flows for Offline Reinforcement Learning in Robotic Manipulation</a></td><td>72</td><td>10</td><td>Manipulation</td><td>autoregressive normalizing flow의 exact likelihood를 이용해 sampling-free advantage-weighted objective로 offline RL을 수행하고 one-step distillation으로 배포하며 real-world manipulation에서 낮은 지연시간과 경쟁력 있는 성능을 실증한다.</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2608.20084'>Evidence-Gated Task and Motion Planning with Vision-Language Models</a></td><td>72</td><td>9</td><td>Embodied AI</td><td>VLM이 생성한 exploratory subgoal로 시각적 evidence를 수집하고 feasibility gate로 planning 지속·추가 탐색·중단을 결정하는 Evidence Acquisition and Feasibility Gating(EAFG)을 제안한다. VLM의 prior knowledge에만 의존한 TAMP subgoal의 실행 실패를 줄이는 새로운 problem formulation으로 cooking task에서 recipe completion 개선과 부재 물체에 대한 적절한 halt 결정을 보였다.</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2608.19891'>EXIMO: VLM Guided Exploration of VLA Policies</a></td><td>72</td><td>9</td><td>VLA</td><td>VLM planner로 장기 과제를 분해하고 탐색·모방·residual off-policy RL 3단계로 VLA를 파인튜닝하는 EXIMO로 기존 방법 대비 표본 효율과 최종 성능을 크게 높였다.</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2608.20114'>DECOWAM: Decoupled Whole-Body World-Action Model for Legged Mobile Manipulation</a></td><td>68</td><td>10</td><td>World Model</td><td>카메라 ego-motion과 base·arm 동작을 분리한 whole-body world-action model DECOWAM으로 real robot ARMDOG 데이터셋에서 action MSE를 21.7% 줄이고 79회 closed-loop 실험에서 whole-body coordination 우위를 보였다.</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2608.20251'>Video2DoorTraversal: Push Door Traversal via Simulated Door Twins</a></td><td>68</td><td>9</td><td>Manipulation</td><td>단일 RGB 영상으로 articulated door twin을 복원하는 real-to-sim-to-real 파이프라인과 dual-depth policy ArticuACT를 결합한다. 실제 5개 문에서 평균 96.57%, unseen door에서 80.95% zero-shot 성공률을 온보드 추론만으로 달성해 object-centric articulated representation과 loco-manipulation policy 학습을 강하게 뒷받침한다.</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2608.19556'>Stream4D: 4D-Consistency for Streaming Autoregressive Diffusion Video Models</a></td><td>68</td><td>7</td><td>World Model</td><td>streaming autoregressive video 생성에서 정적 3DGS critic이 움직임을 정지 상태로 유도하는 문제를 4D reconstruction reward로 해결해 world model의 motion 일관성을 개선한다.</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2608.19729'>SafeBranch: Branch-Pair Safety Alignment for Embodied Agents</a></td><td>64</td><td>8</td><td>Embodied AI</td><td>unsafe rollout을 안전-critical step으로 rollback해 동일 지점에서만 다른 안전/불안전 action 쌍(branch pair)을 구성해 embodied agent를 학습하는 SafeBranch를 제안한다. IS-Bench, SafetyALFRED 및 out-of-distribution 변형에서 critic 없이도 unseen-object 환경에서 안전 성공을 약 10배 높이며 task success를 희생하지 않는다.</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2608.19574'>HiTac-WAM: A Hierarchical Tactile World Action Model for Contact-Rich Robot Manipulation</a></td><td>62</td><td>9</td><td>Manipulation</td><td>contact state·3D deformation·slip risk를 계층적으로 예측하는 tactile world action model(HiTac-WAM)을 제안해 hierarchical forecast 기반 후보 action 선택으로 실로봇 contact-rich task 성공률을 31.1%에서 72.2%까지 끌어올린다.</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2608.19372'>The Missing Touch: Spatially Distributed Tactile Feedback Brings Teleoperation Closer to Human Dexterity</a></td><td>62</td><td>8</td><td>Manipulation</td><td>32-DoF tactile fingertip display로 원격조작 시 국소 접촉 변형을 재현하면 teleoperation 궤적이 자연스러운 인간 동작에 29-79% 가까워짐을 보여 로봇 정책 학습용 demonstration 품질 향상에 직접적으로 기여한다.</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2608.19684'>Learning Hierarchical Skill Policies with Offline Quality-Diversity Reinforcement Learning</a></td><td>62</td><td>8</td><td>RL</td><td>trajectory segment의 advantage로 skill extraction과 diversity objective에 가중치를 부여하는 Advantage-Weighted Quality-Diversity offline pretraining QDOS를 제안한다. offline-to-online dual dataset reuse와 결합해 구조화된 manipulation과 sparse-reward locomotion에서 강한 baseline들을 능가하며 IROS 2026에 채택됐다.</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2608.19977'>Learning Highly Dynamic Skills Transition for Quadruped Jumping Through Constrained Space</a></td><td>60</td><td>7</td><td>RL</td><td>imitation learning으로 학습한 low-level skill과 vision 기반 high-level controller를 결합한 hierarchical RL로 좁은 gate를 통과하는 고난도 quadruped locomotion을 구현한다. 실제 로봇에서 최초 수준의 자율 aerial gate traversal급 민첩성을 보였다고 주장하나 정량적 성공률은 본문에서 확인 불가하다.</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2608.19831'>Causal Reasoning with Bipartite Graphical Causal Models</a></td><td>60</td><td>3</td><td>Causal Reasoning</td><td>순환 인과 구조를 다루는 bipartite graphical causal model과 새로운 do-calculus를 제안해 CBN/SCM의 근본적 한계를 해결하는 이론적 기여이며 counterfactual/causal reasoning 우선 주제와 부합한다.</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2608.19490'>Fine-Tuning VLAs with Self-Demonstrated Generative Control for Multi-Task Manipulation</a></td><td>58</td><td>9</td><td>VLA</td><td>π0.5 VLA를 새 embodiment에 fine-tuning할 때 zero-shot VLA로부터 생성한 online rollout을 함께 학습시켜 기존 instruction-following 능력을 유지하면서 새 task를 sample-efficient하게 습득하는 self-supervised 기법을 real ALOHA와 RoboTwin에서 검증한다.</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2608.20284'>Towards Surgical World-Action Modeling: A Preliminary Joint Visual-Trajectory Forecasting for Surgical Motion Planning</a></td><td>58</td><td>8</td><td>World Model</td><td>수술 도구 궤적과 시각 상태를 함께 예측하는 world-action model을 제안하고 chunked autoregressive rollout이 PSNR 18.86에서 23.11로, ADE를 45.77에서 22.22로 개선하나 장기 예측에서는 오차가 누적된다고 명시한다.</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2608.19613'>What Matters for Latent Actions in Robot Learning</a></td><td>58</td><td>8</td><td>VLA</td><td>Latent Action Model의 41가지 design choice를 공통 autoencoding 프레임워크로 통합해 체계적으로 비교한 최초의 종합 실증 연구로, VLM backbone을 latent action으로 fine-tuning하는 것이 downstream manipulation 성능에 가장 중요함을 real robot까지 검증한다.</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2608.20308'>DreamHand: Repurposing Video Diffusion Models for Occlusion-Robust Egocentric 3D Hand Motion Recovery</a></td><td>58</td><td>7</td><td>Manipulation</td><td>video diffusion model을 deterministic geometry encoder로 재활용해 가려진 손의 3D 궤적을 복원하고 ARCTIC에서 MPJPE를 30%, HOT3D에서 40% 줄이며 사람 영상을 robot manipulation 데이터로 전환할 잠재력을 제시한다.</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2608.19955'>MILD: Tractable Terrain Modeling for Learning Improved Bipedal Locomotion on Deformable Surfaces</a></td><td>58</td><td>7</td><td>Embodied AI</td><td>discrete-element contact solver로 변형 지형을 모사하고 latent modulation 기반 RL controller를 학습한다. 실제 로봇 실험으로 다양한 강성의 표면에서 온라인 지형 식별과 적응을 보이나 bipedal deformable terrain이라는 특정 문제에 집중된 기여다.</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2608.19536'>CVSD-Reg: Cross-Modal Visual Semantic Prior Distillation for Robust LiDAR Registration</a></td><td>58</td><td>6</td><td>3D Vision</td><td>DINOv2 시각 prior를 LiDAR 등록에 distillation해 KITTI·nuScenes·HeLiPR에서 SR@0.5m/1도 97~99%를 달성하고 카메라 없이 cross-sensor 일반화를 보인다.</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2608.20065'>Orthogonal JEPA: Factorized Predictive States for Latent World Models</a></td><td>58</td><td>6</td><td>World Model</td><td>JEPA의 단일 target embedding을 orthogonal basis로 분해해 여러 predictive branch가 서로 다른 latent 성분을 예측하도록 하는 새로운 world model representation을 제안하고 vision부터 continuous control까지 폭넓게 검증한다.</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2608.20087'>Towards Professional Tennis Styles for Humanoid Robots with Adaptive Motion Planning and Tracking</a></td><td>55</td><td>7</td><td>Embodied AI</td><td>broadcast 영상에서 학습한 스타일과 sim-to-real 격차를 줄이는 randomized execution speed tracking 및 motion-speed adapter를 결합한 AdaPT를 제안한다. Unitree G1과 1.7m Dobot Atom 휴머노이드에서 실외 tennis serving을 시연했으나 정량적 baseline 비교는 본문에서 확인 불가하다.</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2608.19491'>DeltaMomentum: A Key-Value based Anisotropic Momentum Update via Delta Rule</a></td><td>55</td><td>1</td><td>LG</td><td>delta rule 기반의 새로운 momentum update(DeltaMomentum)를 제안하고 이론적 증명과 1B 규모 pretraining까지 검증한 견고한 optimization 연구다.</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2608.19375'>Learning the Right Abstraction: Neural Reduced Dynamics for Complex Robot Control</a></td><td>52</td><td>7</td><td>World Model</td><td>high-fidelity simulator 대비 4자리수 빠른 neural reduced dynamics(NRD)로 terrain-aware 정책을 학습하고 다시 high-fidelity simulator에서 검증하는 abstraction 기반 sim-to-real 브릿지를 제안한다.</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2608.19443'>Hybrid Feedback Sampling for Sample-Efficient Model Predictive Control</a></td><td>52</td><td>7</td><td>Manipulation</td><td>optimal sampling proposal을 학습된 feedback policy로 실현하는 Feedback Sampling MPC(FS-MPC)를 제안해 humanoid loco-manipulation 등 불안정한 contact-rich task에서 표준 MPPI 대비 sample efficiency를 개선하고 실로봇으로 검증한다.</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2608.19669'>Scaffolding Minds: Optimizing Latent Visual Target Representations for Multimodal Reasoning</a></td><td>52</td><td>4</td><td>Multimodal</td><td>latent visual reasoning의 SFT/RL 두 단계 한계를 지적하고 scaffolding encoder와 확률적 RL sampler를 도입해 FrozenLake 공간 계획에서 최대 19%p 개선한다.</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2608.19842'>SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning</a></td><td>52</td><td>4</td><td>RL</td><td>정책과 가치 함수가 단일 autoregressive backbone을 공유하는 SAPO로 ALFWorld·WebShop에서 PPO 대비 +15.1%p, GRPO 대비 +12.1%p 향상시키고 메모리·연산 효율을 높였다.</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2608.19710'>Robust Cross-Modal Foundation Model Perception for Underwater Robots under Degraded Visual Conditions</a></td><td>50</td><td>8</td><td>Embodied AI</td><td>DINOv2와 sonar를 degradation-aware gating으로 융합해 극한 혼탁 조건에서 balanced accuracy를 0.461에서 0.615로 높이는 underwater robot 인지 기법이다.</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2608.19589'>OrthoSkillVLA: Continual Skill Learning via Gradient-Informed Skill Subspace Adaptation</a></td><td>50</td><td>8</td><td>VLA</td><td>VLM과 ActionHead의 서로 다른 forgetting 취약성을 분석해 각각 다른 subspace constraint를 부여하고 output layer는 feature-aware MoE로 처리하는 OrthoSkillVLA로 replay 없이 continual skill learning을 개선한다.</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2608.19759'>GOAG: Generative and Object-Agnostic Grasp Planner for Dexterous Robotic Manipulation</a></td><td>50</td><td>8</td><td>Manipulation</td><td>gripper와 물체가 접촉점에서 동일한 표면 geometry를 공유한다는 관찰에 기반해 object-specific 학습 없이 gripper contact surface 분포만 학습하는 GOAG를 제안, MultiDex에서 86.93% 성공률로 SOTA를 달성한다.</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2608.19776'>CoToGrasp: Contact-Topology-Conditioned Dexterous Grasp Synthesis via Canonical Workspace Learning</a></td><td>50</td><td>8</td><td>Manipulation</td><td>물체 기하와 gripper의 기능적 접촉 topology를 canonical workspace로 분리해 object-agnostic하게 학습하는 CoToGrasp를 제안, DexGraspNet에서 SOTA를 달성하고 실로봇으로 검증한다.</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2608.19453'>When Automata Meet Streams: Temporal Logic Compilation for Stream-Based Robotics Task and Motion Planning</a></td><td>50</td><td>7</td><td>Manipulation</td><td>stream 기반 TAMP에서 LTL_f temporal constraint를 automaton으로 컴파일해 action schema에 내장하는 SAM-TD를 제안, stream 객체 생성과 temporal constraint 준수를 최초로 동시에 지원한다.</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2608.19739'>Question-Guided Evidence Acquisition for Multimodal Visual Question Answering</a></td><td>50</td><td>4</td><td>Multimodal</td><td>document VQA에서 inference-time에 필요한 evidence를 능동적으로 탐색하는 agent로 DocVQA2026에서 65% vs 40%의 큰 개선을 보이며 복잡한 planner보다 perception budget이 핵심임을 보인다.</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2608.19303'>Outcome Monitors: Recovery Affordances for Silent Tool Failures</a></td><td>50</td><td>4</td><td>Embodied AI</td><td>task-disjoint trace나 public schema에서 outcome contract를 채굴해 silent tool failure를 감지하고 recovery tool을 안내하는 Outcome Monitor를 제안한다. ToolMaze 완료율을 10.9%에서 28.1%로, tau-bench retail에서 12-14점 높이며 recovery-tool 리스트 제거 시 효과가 사라짐을 통제 실험으로 확인해 failure detection·recovery 연구에 참고할 만하다.</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2608.20256'>Learning When to Think: Adaptive Reasoning for Test-Time Compute Allocation</a></td><td>50</td><td>3</td><td>RL</td><td>GRPO 내부에서 NoThink/Short/Long 추론 모드를 스스로 선택하도록 학습해 MATH500 정확도를 유지하며 응답 길이를 41% 줄이고 GSM8K에도 zero-shot 전이했으며 test-time inference 배분이라는 우선 주제와 연결된다.</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2608.19866'>A 360-Degree Vision Dataset for Learning Yaw Control on GPS-Denied Micro-UAVs in Disaster-Response-Relevant Environments</a></td><td>48</td><td>8</td><td>Navigation</td><td>GPS 차단 환경에서 360도 카메라로 yaw를 예측해 micro-UAV가 개활지로 자율 복귀하는 재난대응용 데이터셋과 CNN 컨트롤러를 제안하고 실환경 테스트에서 반사·눈부심 실패 모드를 규명한다.</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2608.19693'>RIPE++: Reinforced Keypoint Learning from Positive Pairs Only</a></td><td>48</td><td>6</td><td>3D Vision</td><td>단일 positive pair만으로 keypoint detector/descriptor를 학습하는 RL reward를 제안해 MegaDepth1500 AUC@5를 56.58에서 59.65로 높이고 SfM이 어려운 저텍스처 의료 영상에도 적용된다.</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2608.20056'>Gravity-aware partially calibrated absolute pose estimation from affine- or rotation-covariant features</a></td><td>48</td><td>6</td><td>3D Vision</td><td>IMU gravity와 affine/orientation-covariant feature를 결합한 UP1PfAC·UP2PfORI solver로 기존 4점 기반 방법보다 적은 대응점으로 빠르고 정확한 absolute pose 및 초점거리 추정을 제공한다.</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2608.19964'>G-MARK: Grounded Multi-Agent Reasoning for Cooperative Driving via Knowledge Graphs</a></td><td>48</td><td>6</td><td>Embodied AI</td><td>협력 주행에서 latent feature 대신 provenance-aware knowledge graph로 occlusion reasoning을 명시적으로 표현하는 G-MARK를 제안해 occlusion 정확도 42.2% 개선과 25.6배 작은 통신량을 달성한다.</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2608.19567'>Block3D: Efficient Text-to-3D Generation via Block-Wise Diffusion</a></td><td>48</td><td>3</td><td>3D Vision</td><td>shape token을 block 단위로 diffusion 생성해 autoregressive baseline 대비 5.15배 속도 향상을 달성하는 효율적 3D 생성 기법이다.</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2608.19760'>Credit Without Ground Truth: Auditing Step-Level Credit Assignment in LLM Agents Against Executed Replay</a></td><td>48</td><td>3</td><td>RL</td><td>LLM agent의 step-level credit assignment 신호(judge score, logprob ratio 등)가 실제 causal contribution과 상관관계가 없음을 ALFWorld executed-replay로 감사한 rigor 있는 연구다.</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2608.19726'>Projector Is All You Train</a></td><td>48</td><td>3</td><td>Multimodal</td><td>3D MLLM에서 backbone은 고정하고 projector만 학습해도 joint training과 대등하거나 더 나은 성능을 보이며 언어 능력 drift를 방지하고 학습 처리량을 2배로 높인다는 반직관적 결과를 제시한다. 여러 backbone에서 검증된 실용적이고 일반화 가능한 발견이나 새로운 representation이나 problem formulation은 아니다.</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2608.19504'>A Plug-in Interpretation of Conditioning in Score-Based Diffusion Models</a></td><td>48</td><td>2</td><td>CV</td><td>joint diffusion 기반 plug-in conditioning term으로 조건부 reverse-SDE/ODE를 유도하는 이론적 기여가 있으나 robotics 적용은 다루지 않는다.</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2608.19425'>SCAPE: Scenario-Conditioned Simulation-Augmented Policy Evaluation</a></td><td>47</td><td>6</td><td>Embodied AI</td><td>제한된 sim-real paired sample로 시나리오별 정책 성능을 예측하는 SCAPE를 제안하며 sim-to-real bias 보정과 conformal prediction으로 quadruped·주행 정책을 real-world까지 검증한다.</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2608.20009'>ExPhy: A Benchmark for Explicit Physical Property Learning in Multi-Object Trajectory Forecasting</a></td><td>47</td><td>4</td><td>World Model</td><td>질량·마찰·반발계수를 명시적으로 라벨링한 ExPhy 벤치마크와 물리 기반 PhyODE 모델로 OOD 조건에서 ADE·FDE를 각각 33.1%, 31.0% 줄였으며 물리 추론이 필요한 조작·예측 문제와 연관된다.</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2608.20237'>Rule-Compliant Visual Spatial Planning for Multimodal Large Language Models</a></td><td>46</td><td>5</td><td>Embodied AI</td><td>MLLM이 자연어 규칙을 지키며 미로를 탐색하는 RuleMaze 벤치마크와 perception·execution·rule verification을 분리한 DMP를 제안해 unseen rule에 대한 일반화를 높였으며 embodied spatial reasoning과 관련된다.</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2608.19583'>VGI-BENCH: Probing Visual Intelligence in Video Generation Models</a></td><td>46</td><td>3</td><td>Video</td><td>비디오 생성 모델의 시각적 추론 능력을 27개 task로 평가하는 벤치마크이며 최상위 모델도 51%에 그쳐 world model의 self-correction 한계를 드러낸다.</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2608.20000'>Point-Based 3D Reconstruction from Sparse Views under Known Illumination</a></td><td>46</td><td>3</td><td>3D Vision</td><td>opacity를 가진 beta surfel과 adjoint light transport로 sparse-view 3D 재구성을 수행해 267개 primitive만으로 기존 point 기반 baseline보다 낮은 Chamfer distance를 얻는다.</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2608.19338'>Mechanistic Tomography: Designed Measurement for Control-Oriented Interpretability</a></td><td>46</td><td>2</td><td>LG</td><td>patching·gradient·HVP 등 해석가능성 측정법을 y=Ax+w 형태의 통합된 tomography 문제로 정식화하고 GPT-2·Qwen에서 검증하는 일반화 가능한 이론적 틀을 제시한다.</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2608.20290'>Phantom Gains: Auditing Self-Improvement Against a Measured Null</a></td><td>46</td><td>0</td><td>LG</td><td>self-training의 능력 향상 주장을 frozen control과 대조해 감사하고 7가지 측정 오류를 규명해 여러 self-improvement 주장을 뒤집었으나 로보틱스와는 무관한 LLM 학습 방법론 평가 논문이다.</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2608.19661'>World-Model-Grounded LLM Planning for AUV and ASV Navigation Near Offshore Wind Farms</a></td><td>45</td><td>7</td><td>Navigation</td><td>LLM이 무엇을 할지 결정하고 physics-grounded neural world model이 얼마나 오래 실행할지 결정하는 구조로 AUV·ASV 항법을 grounding해 GazeboSim 목표거리 오차를 70-93% 줄인다.</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2608.19894'>Unified and Efficient Point-Line Local Features</a></td><td>45</td><td>6</td><td>3D Vision</td><td>point와 line feature를 단일 경량 네트워크로 동시 추출해 ALIKED+DeepLSD 대비 4배 빠르고 메모리 10분의 1인 SLAM용 local feature 추출기다.</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2608.19492'>Beyond Multimodal Alignment: Certifying Physical Language through Response Substitution and Ordered Execution</a></td><td>45</td><td>6</td><td>World Model</td><td>multimodal representation이 새로운 action composition에서도 동일한 executable meaning을 갖는지 검증하는 새로운 certificate(DBOSC)를 제안하나 toy-scale haptic/elastoplastic 실험에 그친다.</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2608.19522'>LF-GICP: Parameter-Free Degeneracy-Aware LiDAR Odometry via a Voxel-Normal Localizability Field</a></td><td>45</td><td>6</td><td>Navigation</td><td>GICP의 GN Hessian이 translational degeneracy를 가린다는 원인을 규명하고 regularization-free voxel-normal localizability field로 parameter-free degeneracy 검출을 구현해 KITTI·tunnel·다중 센서에서 일반화됨을 보인다.</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2608.19803'>MileGPO: Milestone Inference with Local Evidence for Graph-Based Policy Optimization of Long-Horizon LLM Agents</a></td><td>45</td><td>5</td><td>RL</td><td>ALFWorld·WebShop에서 milestone과 trap을 자동 발견해 reliability-calibrated shaping을 적용하는 MileGPO를 제안하며 long-horizon agent RL의 credit assignment를 개선한다.</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2608.20111'>Planning-Oriented End-to-End Autonomous Driving: Architectures, Evaluation, and Emerging Paradigms</a></td><td>45</td><td>5</td><td>Embodied AI</td><td>camera-to-control부터 world-model 기반 planner, VLA까지 planning-oriented end-to-end autonomous driving을 input representation·output·supervision·evaluation 4축으로 정리한 survey다. 새로운 방법론 제안 없이 open-loop 지표의 한계와 closed-loop 평가 필요성을 논증하는 데 그친다.</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2608.19553'>Where Grounding Accuracy Lives on the IoU Curve: Label-Free Inference-Time Boundary Refinement</a></td><td>45</td><td>4</td><td>Multimodal</td><td>label 없이 inference-time에 grounding box를 재조정하는 방법으로 여러 벤치마크에서 mAcc를 일관되게 개선하지만 test-time 개선 폭은 크지 않다.</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2608.19807'>Answer-Level Trust Selection for Physical Vision-Language Reasoning</a></td><td>45</td><td>4</td><td>Multimodal</td><td>fine-tuning 없이 VLM의 물리량 추정(duration, speed 등) 예측을 개별적으로 신뢰할지 판단하는 Answer-Level Trust Selection을 20개 VLM에서 검증한 연구다.</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2608.20104'>Structured Affinity for Unsupervised Visual Class-Incremental Memory in Deep Artificial Immune Networks</a></td><td>45</td><td>3</td><td>LG</td><td>backprop과 replay 없이 구조화된 면역 affinity로 class-incremental 시각 기억을 형성하는 대안적 학습 패러다임을 제시하고 여러 데이터셋에서 replay-free 성능을 검증한다.</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2608.19202'>Active Inference as Context Acquisition for AI Agents</a></td><td>45</td><td>3</td><td>RL</td><td>context 획득을 잠재 task state에 대한 belief update와 expected free energy 최소화로 정식화하는 active inference framework를 제안한다. Optimal Question Asking으로 exact posterior와 DP oracle을 갖춘 벤치마크를 구성해 여러 LLM을 평가하는 model-agnostic 설계 원리로, active perception 연구와 이론적으로 맞닿아 있다.</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2608.19804'>ADAPT: Physics-Aware Diffusion-based World Models for Adaptive Predictive Transferable HVAC Control</a></td><td>45</td><td>2</td><td>World Model</td><td>물리 제약을 반영한 diffusion 기반 world model로 HVAC 제어에서 에너지 7.3%, 불쾌감 30.2% 개선을 보였으나 적용 도메인이 건물 제어로 로보틱스와는 거리가 있다.</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2608.19540'>Continuous Adversarial MeanFlow Transfer</a></td><td>45</td><td>1</td><td>Video</td><td>이질적인 pretrained diffusion/flow model을 공유 velocity representation으로 통합해 domain adaptation과 few-step acceleration을 동시에 해결하는 MeanFlow-Transfer와 CAMF를 제안한다.</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2608.19973'>Open-Vocabulary 3D Object Detection with Co-Distillation Discovery and Dual Guidance Robust Training</a></td><td>44</td><td>5</td><td>3D Vision</td><td>co-distillation으로 novel object discovery 신뢰도를 높이고 LLM 기반 계층적 정렬로 classification head를 보강해 SUN RGB-D·ScanNetV2에서 open-vocab 3D detection 성능을 높인다.</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2608.20157'>G3Ego: Gaze-Guided Graphs for Egocentric Action Understanding</a></td><td>44</td><td>5</td><td>Embodied AI</td><td>시선을 scene graph 구성에 직접 활용해 관련 entity만 남기는 gaze-guided graph로 EGTEA/MECCANO에서 video pretraining 없이 경쟁력 있는 egocentric action 인식을 보인다.</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2608.19783'>Coupled Optimal Transport with Landmark Constraints</a></td><td>44</td><td>2</td><td>CV</td><td>소수의 landmark로 변형장과 optimal transport plan을 상호 일관성 제약으로 결합한 이론적 프레임워크이며 shape matching에서 검증된다.</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2608.20093'>HandMvNet: Real-Time 3D Hand Pose Estimation Using Multi-View Cross-Attention Fusion</a></td><td>42</td><td>5</td><td>3D Vision</td><td>카메라 파라미터 없이 multi-view cross-attention으로 실시간 3D 손 자세를 추정해 monocular 방식의 depth-scale 모호성을 해소하며 imitation learning용 hand tracking에 활용 가능하다.</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2608.19380'>CAViAR: A Causal Video Dataset for Fine-Grained Accident Reasoning in Real-World Scenarios</a></td><td>42</td><td>4</td><td>Video</td><td>2,249개 사고 영상에 책임 소재까지 라벨링한 새 벤치마크로 VLM의 perception-reasoning gap을 드러내지만 workshop 논문으로 규모가 제한적이다.</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2608.19639'>S$^2$GS: Structured Sparse Gaussian Streaming for Efficient Free-Viewpoint Video Reconstruction on Edge-IoT Devices</a></td><td>42</td><td>4</td><td>3D Vision</td><td>octree 기반 sparse gaussian streaming으로 QUEEN 대비 저장비용 85% 절감을 보이는 edge-IoT용 4D reconstruction 최적화 기법이다.</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2608.19766'>Far from the Crowd: Scalable Self-Supervised Learning via Geographic Isolation</a></td><td>42</td><td>2</td><td>LG</td><td>geolocation만으로 계산되는 label-free curriculum으로 MAE 학습 예산을 20%까지 줄이면서 BigEarthNet mAP를 최대 5점 높이는 효율적 SSL 전략이다.</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2608.20319'>Inducing Task Models from Computer-Use Traces</a></td><td>42</td><td>2</td><td>LG</td><td>동시다발적 목표가 얽힌 computer-use trace에서 잠재 task를 분리하고 계층적 목표-절차 모델을 함께 유도하는 Task Model Induction(TMI)을 제안한다. ground-truth 대비 0.974의 grouping 일치도와 74.9% 실행 단계 재구성을 보이며, 유도된 skill이 held-out task 정확도를 최강 baseline 대비 30.0%p 높여 skill chaining 관점에서 참고할 만한 새로운 problem formulation이다.</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2608.19953'>Learning Early-to-Final Solution Consistency for MILP Acceleration</a></td><td>42</td><td>1</td><td>LG</td><td>초기 탐색 해와 최종 해의 consistency를 예측하는 새로운 학습 목표로 Gurobi 기반 primal gap을 평균 56.9% 줄이고 SCIP로 zero-shot 전이했으나 로보틱스 관련성은 낮다.</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2608.20011'>Manifold Drift in Flow Preference Optimization: A Root Cause of Reward Hacking</a></td><td>42</td><td>0</td><td>Video</td><td>flow matching 기반 preference optimization의 실패 원인을 manifold drift로 규명하고 ThermoDPO를 제안해 FlowDPO 대비 StrictScore를 0.629에서 0.899로 높였으나 로보틱스와는 무관한 생성모델 논문이다.</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2608.19968'>PVRA: A Pointwise Key-point Voting Framework for Robotic Assembly</a></td><td>40</td><td>6</td><td>Manipulation</td><td>3D keypoint 기반 modular framework로 조립 의존성을 학습해 assembly manipulation의 actionable output을 예측한다. ECoR 2026 발표작으로 자체 pose estimation dataset에서만 평가되어 일반화 근거가 제한적이다.</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2608.19376'>Does Marginal Coverage Guarantee Class-Conditional Safety for Zero-Shot VLMs Under Shift?</a></td><td>40</td><td>3</td><td>Multimodal</td><td>CLIP/SigLIP 등 zero-shot VLM의 conformal coverage가 class-tail에서 붕괴함을 실증한 audit 논문으로 방법론적 기여보다 분석적 기여가 크다.</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2608.19652'>Can Agent Memory Systems Track Evolving State?</a></td><td>40</td><td>3</td><td>NLP</td><td>사실·제약·결정이 갱신되는 상황에서 최신 상태를 추적하는 state tracking을 정의하고 234개 시나리오의 StateMemBench를 구축한다. 상태 우선 memory 기법 StateMem이 최강 baseline 대비 최대 1.8배 정확도를 보이며 기존 memory 시스템에 lightweight wrapper로 적용해도 32-67점 개선되어 robot memory 설계에 참고할 만하다.</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2608.19598'>PEA-DPO: Perception-Enhanced Alignment Direct Preference Optimization for MLLMs Alignment</a></td><td>40</td><td>2</td><td>Multimodal</td><td>MLLM의 visual insensitivity를 이론적으로 분석하고 DPO에 시각 선호 신호를 추가해 hallucination을 줄이지만 alignment 기법의 확장 성격이 강하다.</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2608.19987'>STEP: Score-Based Temporal Energy for Human Pose Video Anomaly Detection</a></td><td>40</td><td>2</td><td>Video</td><td>PCA whitening으로 pose noise를 물리적으로 타당하게 만들어 EBM 기반 skeleton anomaly detection의 UBnormal AUROC를 12.2%p 높인 경량 기법이다.</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2608.20107'>BeyondMasks: Evaluating Causal and Physical Consistency in Video Object Removal</a></td><td>40</td><td>2</td><td>Video</td><td>물체 제거를 그림자·반사 등 물리적 파급효과까지 포함한 causal intervention으로 재정의하고 CORE 평가 프로토콜로 기존 방법들의 causal consistency 실패를 드러낸다.</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2608.20127'>ID-VTG: Image-Disambiguated Video Temporal Grounding</a></td><td>40</td><td>2</td><td>Video</td><td>참조 이미지와 텍스트를 결합해 유사 인스턴스를 구별하는 새로운 video temporal grounding task를 정의하고 fast-slow dual-branch 구조로 SOTA를 달성한다.</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2608.20335'>4DAnyone: Create Anyone in 4D from a Casual Monocular Video</a></td><td>40</td><td>2</td><td>3D Vision</td><td>reference/target context의 attention 병목을 RCP·TCR로 해결해 monocular 영상으로부터 multiview-consistent 4D human을 재구성한다.</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2608.19587'>Unregularized Convergence of Single-Loop, Entropy-Regularized Natural Actor-Critic</a></td><td>40</td><td>2</td><td>RL</td><td>single-loop entropy-regularized Natural Actor-Critic의 unregularized 수렴률을 개선한 이론 연구이나 robot learning에 대한 직접적 적용은 제시되지 않는다.</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2608.19993'>Optimal Skill Selection for LLM Agents with Provable Bicriteria Guarantees</a></td><td>40</td><td>2</td><td>LG</td><td>skill 선택을 submodular 최적화로 정식화하고 (1-1/e,1) bicriteria 근사 보장을 갖는 BPS 알고리즘을 제시해 task success 0.73을 달성했으나 LLM 코드 에이전트 대상이라 로보틱스 관련성은 낮다.</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2608.19662'>ReCache: Efficient KV Cache Reuse and Compression for Tool-Augmented LLM Agents</a></td><td>40</td><td>1</td><td>LG</td><td>tool schema를 resource 단위로 독립 caching하는 resource-wise attention으로 KV cache 재사용을 가능하게 하는 ReCache를 제안한다. dense 대비 82.3% vs 82.4% Inv-F1을 유지하며 TTFT 3.655배 가속과 KV 메모리 92.43% 절감을 달성했으나 tool-agent serving에 특화된 효율화 기여다.</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2608.20061'>Let&#x27;s Scale Step by Step: Compute-Efficient Hyperparameter Transfer for Large-Scale Mixture-of-Experts</a></td><td>40</td><td>0</td><td>LG</td><td>MoE에 MLA와 Muon을 결합한 μP 확장과 token-budget scaling law로 155B MoE 모델의 learning rate를 소규모 proxy만으로 예측해 실용적인 대규모 사전학습 기여를 한다.</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2608.19743'>Gallileo-4D: Frozen Backbone Ensemble for Dynamic 4D Reconstruction</a></td><td>38</td><td>4</td><td>World Model</td><td>13가지 fine-tuning 시도 중 12개가 challenge 성능을 오히려 악화시켰음을 밝히고 frozen backbone ensemble만으로 3위를 달성해 benchmark overfitting에 대한 경고를 제공한다.</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2608.20275'>DART-S: Reachability-Audited Active-Suspension Preconditioning for Off-Road Vehicle Jumps</a></td><td>38</td><td>4</td><td>Robotics</td><td>reachability 기반 interval screen과 local calibration map으로 오프로드 차량 점프 전 active suspension을 조정하는 DART-S를 제안한다. BeamNG 시뮬레이션 600회 실험에서 통계적으로 유의한 성공률 개선을 보이나 학습 기반 요소가 없어 우선 주제와의 관련성은 낮다.</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2608.19285'>Clustering and Token Denoising for Faster and More Robust VLMs</a></td><td>38</td><td>3</td><td>Multimodal</td><td>training-free token pruning으로 LLaVA 추론을 가속하지만 clustering+denoising 조합의 engineering 개선에 가깝고 robotics 연관성은 낮다.</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2608.19723'>StreamSoccer: Event-Driven Memory for Streaming Soccer Commentary</a></td><td>38</td><td>2</td><td>Video</td><td>event lifecycle을 명시적으로 모델링하는 memory 구조로 실시간 축구 중계를 생성하며 robot memory 설계에 참고할 아이디어를 제공하나 응용 도메인은 스포츠 중계다.</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2608.19323'>Improved Confidence Estimates for Black-Box Large Language Models</a></td><td>38</td><td>2</td><td>NLP</td><td>유사 질의의 정답 여부를 특징으로 활용해 LLM 응답의 정확도를 예측하는 경량 분류기로 zero-shot UQ 점수보다 일관되게 우수하다.</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2608.19880'>EnvHarness: Awakening Static Worlds for Agent Learning</a></td><td>38</td><td>2</td><td>RL</td><td>정적 RL 환경을 정책의 약점에 맞춰 재구성하는 plug-in layer로 최대 9.0점 개선을 보였으나 로보틱스 특정성은 낮고 LLM agent 벤치마크 중심이다.</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2608.19860'>AutoLumNet: Monotone Optimal Transport for Single-Shot Exposure Correction</a></td><td>38</td><td>1</td><td>CV</td><td>단조 tone curve를 OT 최적해로 학습하는 이론적으로 보장된 exposure correction 기법으로 11.2ms의 빠른 처리 속도를 보인다.</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2608.20134'>Feature Evolution and Migration during Vision Transformer Training</a></td><td>38</td><td>1</td><td>CV</td><td>Sparse Autoencoder로 ViT의 layer-epoch 간 feature migration을 시각화하는 해석 도구로 학습 초기에 이동이 집중됨을 밝힌다.</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2608.19529'>When Machines Speak: A Unified Generative Framework for Integrating Machine-Native Symbols into Pretrained Large Language Models</a></td><td>38</td><td>1</td><td>LG</td><td>LLM의 vocabulary와 embedding space를 machine-native symbol까지 확장해 텍스트와 기호를 하나의 autoregressive objective로 공동 생성하는 UniLang을 제안한다. 추천 시스템과 법률 판례 예측 두 과제에서 baseline을 능가하나 로봇 도메인과는 거리가 있다.</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2608.19893'>Interrupting the Loop: Periodic Subject Changes Raise Judged Surprise and Connection in Base Language Models</a></td><td>38</td><td>0</td><td>NLP</td><td>base LM의 생성 루프에 주기적 subject 전환을 주입하는 것이 judged surprise·connection 상승의 핵심 요인임을 24개 조건 실험으로 규명한다. judge의 착시(주입 문장을 모델 것으로 착각)까지 통제한 엄밀한 평가 프로토콜이 돋보이나 로봇과는 무관하다.</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2608.20316'>Pandora&#x27;s AI Model Routing Box: Efficient Allocation with Costly Value Estimation</a></td><td>38</td><td>0</td><td>LG</td><td>모델 라우팅을 Pandora&#x27;s Box 문제로 정식화해 closed-form value-of-information 정책을 제시했으나 로보틱스와 무관한 LLM 라우팅 연구다.</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2608.20161'>DARS: Dual-Level Credit Assignment RL with Structured Reasoning for Instruction-Based Image Editing</a></td><td>37</td><td>1</td><td>RL</td><td>planner-renderer 구조의 image editing에 dual-level credit assignment RL을 적용한 DARS로 Joint RL baseline 대비 성능을 높였으나 로보틱스와는 무관한 이미지 편집 태스크다.</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2608.20274'>Break It Down, Pass It On: Cross-Task Skill Transfer in LLM Agents</a></td><td>37</td><td>1</td><td>NLP</td><td>subtask 단위·text 형식의 skill이 더 잘 전이됨을 규명하고 specificity와 abstractness를 결합한 skill utility score를 제안했으나 물리적 skill chaining이 아닌 LLM 에이전트 텍스트 skill 메모리에 국한된다.</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2608.19208'>When Irrelevant Text Matters: Affine Margin Shifts in Multimodal Large Language Models</a></td><td>36</td><td>1</td><td>Multimodal</td><td>irrelevant text가 MLLM의 binary 판단 margin을 context-free 대비 affine 변환 형태로 왜곡시킴을 발견한다. 여러 벤치마크에서 일관된 geometric regularity를 보여 noisy-context 진단에 유용한 분석적 기여다.</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2608.20054'>What You Can&#x27;t See Is What You Learn: Restricted Evidence Visibility Favors Compositional Generalization in Shared-Genome Language-Model Societies</a></td><td>36</td><td>1</td><td>NLP</td><td>정보 접근을 제한한 multi-agent LM society가 compositional generalization을 오히려 촉진함을 보인 통제 실험이나 최종 벤치마크 기준을 통과하지 못했다고 스스로 밝힌다.</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2608.19758'>FlashPrefill V2: Block-Sparse Prefill Attention for Long-Context LLM Serving</a></td><td>36</td><td>0</td><td>LG</td><td>mean correction term과 FlashAttention-3/4 정합 커널로 block-sparse prefill attention을 production 수준으로 발전시킨 FlashPrefill V2를 제안한다. H20 GPU에서 FA2 대비 최대 47.26배 가속을 보이는 강한 engineering 기여지만 새로운 학습 패러다임은 아니다.</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2608.19537'>Multimodal Trajectory Planning for Surface Vehicles using Turning Circle-based Control Barrier Functions</a></td><td>35</td><td>5</td><td>Navigation</td><td>turning circle 기반 CBF로 surface vehicle의 좌우 회피 모드를 명시적으로 구분해 global guide path 없이 multimodal trajectory를 생성하는 MPC 프레임워크다.</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2608.19836'>Adaptive Probabilistic Shielding by Learning MDPs for Safe Reinforcement Learning</a></td><td>35</td><td>3</td><td>RL</td><td>MDP transition probability를 online으로 추정하며 shield를 점진적으로 개선하는 adaptive probabilistic shielding을 제안해 safe RL에 기여하나 검증이 formal method 위주다.</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2608.19751'>GenMatch: An End-to-End Generative Matching Framework for Micro-View Order-Dispatching in Ride-Hailing</a></td><td>35</td><td>0</td><td>LG</td><td>라이드헤일링 order-dispatching을 generative matching으로 정식화한 산업 배포 사례이나 로보틱스와 무관하고 특정 도메인 엔지니어링에 가깝다.</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2608.19644'>When Guidance Goes Off-Scale: Recalibrating Diffusion Transformers under Analog Compute-in-Memory Nonidealities</a></td><td>34</td><td>2</td><td>CV</td><td>analog compute-in-memory 잡음 하에서 CFG scale을 재보정해 PixArt/DiT의 FID를 크게 낮추는 하드웨어 특화 보정 기법이다.</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2608.20312'>Inter-X++: A Comprehensive Benchmark for Multimodal Human-Human Interaction Analysis</a></td><td>34</td><td>2</td><td>CV</td><td>손가락 움직임까지 포함한 대규모 human-human interaction 벤치마크와 통합 표현/모델 OpenHHI를 제안하며 생성·인지 과제 모두에서 SOTA를 달성한다.</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2608.19564'>Remember, Verify, or Ask? Cross-Family Evaluation of Memory Commitment in LLM Agents</a></td><td>34</td><td>2</td><td>NLP</td><td>LLM agent가 정보를 영구 저장·재검증·사용자 확인 중 무엇을 선택해야 하는지 평가하는 Memory Commitment Benchmark(MCB)를 제안한다. Claude와 Qwen 모두 사실 변화는 잘 검증하지만 ambiguity에 대한 clarification recall은 0.333에 그쳐 robot memory 설계에 참고할 실패 양상을 보여준다.</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2608.19737'>TempJail: Temporal Jailbreak Attack against Large Vision-Language Models via Subtitle Scheduling</a></td><td>34</td><td>1</td><td>Multimodal</td><td>자막의 시간적 배치를 최적화해 LVLM을 jailbreak하는 새로운 공격 벡터를 제시하고 GPT-5 등에서 높은 성공률을 보이는 안전성 연구다.</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2608.20122'>ArmorOCR: Grounded Adversarial Visual Perception via Observation-Transferred Self-Distillation</a></td><td>34</td><td>1</td><td>Multimodal</td><td>self-distillation과 GRPO로 adversarial 텍스트에 대한 grounded OCR 강건성을 높이는 2단계 학습 프레임워크다.</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2608.20263'>Ultra-High-Definition Restoration Transformers with Correlation Matching Transformation</a></td><td>34</td><td>1</td><td>CV</td><td>4개 해상도 공간을 오가는 UHD restoration transformer로 파라미터를 86% 줄이면서 5개 복원 task에서 성능을 유지한다.</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2608.19203'>Asymmetric Attention Heads: Structured Head-Wise Context Allocation for Transformer Attention</a></td><td>34</td><td>1</td><td>LG</td><td>head마다 다른 causal context 길이를 할당하는 Asymmetric Attention Heads(AAH)를 제안한다. 4096 토큰 실험에서 일부 variant가 full attention보다 낮은 validation loss를 보이나 seed 하나의 소규모 실험으로 증거가 제한적이다.</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2608.20116'>When Text and Numbers Disagree: Evidence Arbitration in Large Language Models</a></td><td>34</td><td>1</td><td>LG</td><td>텍스트와 수치 evidence가 상충할 때 LLM의 arbitration 행태를 조작 가능한 synthetic benchmark로 분석한다. 모델이 신뢰도보다 시간적 최신성에 더 의존하는 체계적 heuristic 편향을 드러내 tool-augmented 의사결정의 실패 모드를 규명한다.</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2608.19211'>Represented but Ignored: A Causal Account of Prosodic Underuse in Audio-Language Models</a></td><td>34</td><td>0</td><td>NLP</td><td>stage-specific probe와 hidden-state intervention으로 audio-LLM이 prosody 정보를 내부적으로 갖고 있지만 응답에 활용하지 못함을 인과적으로 규명한다. 4개 모델에서 일관된 실험 증거를 제시하나 로봇 응용과는 거리가 있다.</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2608.19611'>Forking Fast: Efficiently Estimating Uncertainty Dynamics in Text Generation</a></td><td>34</td><td>0</td><td>LG</td><td>reasoning chain resampling 분석의 비용을 줄이기 위해 uncertainty dynamics가 안정적 패턴으로 수렴함을 보이고 저비용 rollout을 고비용 수준으로 보정하는 통계 모델을 제안한다. LLM 해석가능성 도구로서 유용하나 로봇 응용과는 무관하다.</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2608.19670'>The Asymmetric Harms of LLM Compression</a></td><td>34</td><td>0</td><td>LG</td><td>3개 LLM, 11개 압축 기법에서 compression이 head knowledge를 tail보다 더 크게 손상시키고 압축 모델이 틀린 답에도 높은 confidence를 유지함을 보인다. aggregate bias score 뒤에 그룹별 상반된 편향 변화가 숨어있음을 드러내는 세밀한 empirical 분석이다.</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2608.19920'>Learning how to Forget: Fine-tuning for Long-Context Sparse Attention</a></td><td>34</td><td>0</td><td>LG</td><td>임의의 KV cache 정책에 대해 모델이 sparse attention과 co-adapt하도록 fine-tuning하는 방법과 H2O 전용 커널 라이브러리 KeysAndValues를 공개한다. 단일 A100에서 동작하며 exact attention 대비 우수한 성능을 보이는 효율화 기여다.</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2608.19579'>Enforcing LLM Safety through DMD-based Classification of Prompt-Response Embedding Dynamics</a></td><td>34</td><td>0</td><td>LG</td><td>prompt-response embedding 궤적에 safe/unsafe Koopman operator를 각각 적합시켜 잔차 기반으로 안전성을 분류하는 DMD 방법을 제안한다. dynamical system을 AI 분석 도구로 쓰는 방향 전환이 흥미로우나 로봇 응용과는 무관하다.</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2608.19514'>In Two Minds about Lifelong Learning: Exploring Hemispheric Redundancy and Specialisation in Neural Models</a></td><td>33</td><td>2</td><td>LG</td><td>뇌의 hemisphere 비대칭과 sleep consolidation에서 영감받은 4MAS continual learning architecture를 제안하나 Split-CIFAR-100 정확도가 29.29%로 낮아 실증력이 약하다.</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2608.20172'>Ask Self, Ask Others: Relation Is All You Need</a></td><td>33</td><td>1</td><td>LG</td><td>attention 대신 Self/Exchange relation을 먼저 구성한 뒤 information flow를 유도하는 새로운 token-mixing primitive(Relation)를 제안하나 100M 이하 소규모에서만 검증되었다.</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2608.19790'>LLMs as Acquisition Policies for Finite-Pool Materials Optimization: A Controlled Study</a></td><td>33</td><td>0</td><td>LG</td><td>LLM을 재료 탐색의 acquisition policy로 쓰는 controlled study이나 Gaussian-process 대비 우위가 불명확하고 로보틱스와 무관하다.</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2608.19281'>APPROVE: Visual End-User-in-the-Loop Robot Programming with LLMs</a></td><td>32</td><td>6</td><td>Embodied AI</td><td>LLM으로 생성한 로봇 프로그램을 Blockly 블록으로 시각화해 사용자가 확인·수정·재사용하도록 하는 human-in-the-loop 프로그래밍 프레임워크(APPROVE)로 엔지니어링 성격이 강하다.</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2608.19671'>SAGE: Ergodic Control for Autonomous and Adaptive Inspection of Subsea Infrastructure</a></td><td>32</td><td>5</td><td>Navigation</td><td>실시간 위험 분포에 비례해 방문 빈도를 배분하는 ergodic control(SAGE)로 subsea valve 점검을 적응적으로 수행하나 5개 밸브 규모의 simulation 검증에 그친다.</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2608.19817'>Core-KAN: Continuous Vision Kernels with Kolmogorov-Arnold Networks</a></td><td>32</td><td>1</td><td>CV</td><td>KAN 기반 continuous kernel로 scale 적응과 content 필터링을 분리하는 dynamic convolution 모듈이며 기존 vision backbone 대비 소폭 개선이다.</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2608.19871'>DIFFCZSL: Compositional Zero-Shot Learning Regularized by Diffusion Representations</a></td><td>32</td><td>1</td><td>CV</td><td>diffusion intermediate representation을 CLIP 임베딩에 정렬시켜 compositional zero-shot 인식을 보조하는 기법으로 CLIP 기반 baseline 대비 점진적 개선이다.</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2608.19885'>Separating Covariate Shift from Mechanism Change with Two Discriminators: CJSD, a Conditional Discrepancy with an Exact Covariate-Concept Decomposition</a></td><td>32</td><td>1</td><td>LG</td><td>covariate shift와 mechanism change를 두 discriminator로 분리하는 conditional discrepancy(CJSD)를 제안하며 lifelong expert pool 관리에 anytime validity를 보장한다.</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2608.19875'>A knowledge-guided agentic framework for mitigating patient-context ambiguity in health queries</a></td><td>32</td><td>1</td><td>NLP</td><td>환자 질의의 맥락 모호성을 knowledge graph 기반 가설 생성과 targeted follow-up question으로 해소하는 agentic framework를 제안한다. 진단 검색에서 Top-1 정확도를 57.1%p 이상 높였으나 헬스케어 도메인에 특화된 clarification 기여다.</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2608.19857'>Inadvertent Context Leakage in Language Models</a></td><td>32</td><td>0</td><td>NLP</td><td>LLM context 내 민감정보가 정상적인 출력에도 hidden correlation으로 leakage됨을 보이는 보안 연구로 robotics와는 무관하다.</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2608.19799'>SWE-bench Science: Can Coding Agents Resolve Engineering Tasks in Science?</a></td><td>32</td><td>0</td><td>NLP</td><td>20개 과학 도메인, 98개 저장소에서 119개 과제로 구성된 과학 소프트웨어 수리 벤치마크 SWE-bench Science를 제안한다. 최고 모델(Claude Code+Opus-5)도 pass@1 50% 미만으로 과학 지식 활용의 한계를 드러내는 벤치마크·분석 논문이다.</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2608.20047'>Auditing Cross-Lingual Fairness in Language Model Watermarking</a></td><td>32</td><td>0</td><td>NLP</td><td>6개 watermarking 기법, 11개 언어에 대해 detection threshold와 quality를 분리 측정하는 평가 프레임워크를 제안한다. cross-lingual fairness gap이 개별 언어보다 typological family 구조에 기인함을 보이는 체계적 auditing 기여다.</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2608.20338'>ConceptGuard: Benchmarking Context-Sensitive Unlearning in Large Language Models</a></td><td>32</td><td>0</td><td>NLP</td><td>harmful/benign 맥락에서 모두 쓰이는 dual-use concept 개념으로 unlearning을 forget-retain의 개념 수준에서 평가하는 ConceptGuard 벤치마크를 제안한다. 기존 unlearning 기법들이 contextual separation에서 취약함을 드러내는 새로운 평가 관점의 벤치마크다.</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2608.20318'>AI4AI-Bench: Benchmarking LLM Agents in Algorithmic Design for Recursive Self-Improvement</a></td><td>32</td><td>0</td><td>LG</td><td>학습 알고리즘 자체를 재작성하는 재귀적 자기개선 능력을 평가하는 벤치마크로 최고 시스템도 0.250점에 그쳐 한계를 드러냈으나 로보틱스와는 무관하다.</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2608.19701'>Beyond Memory Majority: Latent-Source Reasoning for Multi-Agent Memory Arbitration</a></td><td>30</td><td>2</td><td>NLP</td><td>여러 agent가 쓴 memory가 상위 source를 공유해 false majority를 만드는 memory correlation bias를 정의하고 이를 보정하는 CAMA를 제안한다. 독립적 evidence 수를 추정하고 부족하면 추가 검색하는 구조로 multi-agent memory arbitration에서 baseline을 능가한다.</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2608.20202'>MemTrapBench: Benchmarking Cognitive Traps in LLM Memory Use</a></td><td>30</td><td>2</td><td>NLP</td><td>LLM 메모리가 오히려 추론을 왜곡시키는 cognitive trap을 MemTrapBench로 정량화하고 AdaptiveMem으로 완화했으나 로봇 메모리가 아닌 대화형 LLM 메모리에 국한된다.</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2608.20141'>DPC-Net: Dual-Prior Collaborative Network for All-in-One Image Restoration</a></td><td>30</td><td>1</td><td>CV</td><td>VLM 감독 기반 degradation-semantic prior와 low-level prior를 결합한 all-in-one image restoration 네트워크로 모듈 추가형 개선이다.</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2608.19351'>Uncovering the Limits of Proof Sharing for Neural Networks</a></td><td>30</td><td>1</td><td>LG</td><td>신경망 검증에서 template 기반 proof sharing의 한계를 jointly stable neuron 지표로 설명하고 layer별 자동 분배 기법 FastCert로 평균 1.13배 속도 향상을 얻는다.</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2608.19888'>Evidence Before Expansion: Reuse, Spawn, or Defer in Lifelong Expert Pools</a></td><td>30</td><td>1</td><td>LG</td><td>expert pool에서 reuse·spawn·defer를 sequential hypothesis testing으로 통계적으로 정당화하는 프레임워크로 위 논문과 거의 동일한 방법론을 다룬다.</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2608.20186'>Decoding silent reading from non-invasive EEG</a></td><td>30</td><td>1</td><td>CV</td><td>묵독 시 EEG로부터 open-vocabulary 단어 정보를 CLIP-style contrastive decoding으로 복원 가능함을 보인 BCI 연구로 robotics와는 직접적 관련이 없다.</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2608.19741'>One Success Isn&#x27;t Reliability: Thinkingbox, a Sandbox and Benchmark for Agents in Stateful Business Workflows</a></td><td>30</td><td>1</td><td>NLP</td><td>MCP 호환 tool 세션과 상태 기반 backend를 갖춘 stateful business workflow용 agent 샌드박스 Thinkingbox를 구축한다. 최고 모델도 pass@1 65.36%, pass^20 25.25%에 그쳐 long-horizon 신뢰성의 어려움을 드러내나 도메인은 로봇과 무관하다.</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2608.19535'>From Retrieved Context to Runtime Control: Adaptive Compression for Edge-based RAG</a></td><td>30</td><td>1</td><td>LG</td><td>Jetson AGX Thor에서 압축기 자체의 연산 비용까지 고려한 telemetry 기반 adaptive context compression을 제안한다. 중간 수준 압축으로 GPU 에너지 53.2%, SoC 에너지 48.2% 절감을 보여 edge 컴퓨팅 관점에서 로봇 온보드 추론에 참고할 만하다.</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2608.19861'>PolicyGuide: From Guarding One Action to Guiding the Whole Workflow for Policy-Compliant LLM Agents</a></td><td>30</td><td>1</td><td>NLP</td><td>고객 서비스 LLM 에이전트의 정책 준수를 위한 workflow graph 기반 verifier로 Pass^4를 0.42에서 0.62로 높였으나 로보틱스와는 무관한 도메인 특화 엔지니어링이다.</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2608.19900'>AvatarDynamizer: From Static to Dynamic Human Avatars via Generative Dynamic Textures</a></td><td>30</td><td>0</td><td>CV</td><td>static avatar를 texture-space dynamic embedding으로 4D 아바타화하는 생성 기법으로 human graphics 응용에 한정된다.</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2608.19488'>When to Retrain: An Empirical Study of Retraining Policies for Streaming ML Under Concept Drift, Budget, and Latency Constraints</a></td><td>30</td><td>0</td><td>LG</td><td>concept drift 하에서 retraining policy를 비교한 대규모 실증 연구이나 robotics와 관련이 없고 새로운 방법론 제시는 아니다.</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2608.19653'>DeltaML-Bench: Evaluating Machine Learning Agents on Real-World Research Repositories</a></td><td>30</td><td>0</td><td>LG</td><td>ML agent가 실제 연구 repository의 baseline을 개선하도록 평가하는 DeltaML-Bench를 제안하며 specification gaming 문제를 드러낸다.</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2608.19748'>Truncate Bad, Upweight Good: BoN-Style Distillation via Rank-Based Classification</a></td><td>30</td><td>0</td><td>NLP</td><td>Best-of-N distillation에서 하위 rank를 완전히 truncate하는 TUP 기법을 제안하고 이를 이론적으로 정당화하나 robotics와는 무관하다.</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2608.19762'>Finite-Horizon Input-Output Dynamics of Minibatch Perturbations in AdamW</a></td><td>30</td><td>0</td><td>LG</td><td>AdamW의 minibatch perturbation이 optimizer state를 통해 미래 loss에 미치는 지연 효과를 input-state-output 시스템으로 분석한 이론 도구다.</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2608.19914'>Multi-Source Wasserstein Distributionally Robust Graph Learning</a></td><td>30</td><td>0</td><td>LG</td><td>이질적 source domain의 그래프를 Wasserstein barycenter로 융합하는 distributionally robust graph learning(MS-WDRO)으로 이론적 guarantee를 갖추었으나 robotics와는 무관하다.</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2608.19369'>Linguistic Holonomy and Statistical Watermarks: Inner Geometry of Meaning-Preserving Transformations</a></td><td>30</td><td>0</td><td>NLP</td><td>의미보존 변환의 불변량을 endpoint와 holonomy로 분해하고 watermark 잔존 신호가 ρ^(h+1) decay law를 따름을 이론적으로 증명한다. Wilson loop 유비를 정리로 formalize한 흥미로운 이론이나 로봇 연구와는 무관하다.</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2608.20153'>FormalTCS: Benchmarking End-to-End Frontier Formal Theoretical Computer Science Research of Large Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>STOC/FOCS/SODA/COLT 2025-2026 논문 175개로 구성된 이론전산 연구 벤치마크를 Lean 정형화와 함께 구축한다. 최고 모델도 autoformalization 정확도 11.5%에 그쳐 자율 연구의 병목을 명확히 드러낸다.</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2608.19889'>Write Once, Run Everywhere: The Axon DSL for Shape-Safe and Framework-Agnostic LLM Architectures</a></td><td>30</td><td>0</td><td>LG</td><td>프레임워크에 종속되지 않는 LLM 아키텍처 DSL로 vLLM 배포 시 Transformers 대비 58% 속도 향상을 보였으나 로보틱스와는 무관한 인프라 도구다.</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2608.19635'>Magnetically Self-Sealed MR Haptic Actuator With PWM-Based Excitation and High-Fidelity Torque Control</a></td><td>28</td><td>4</td><td>Manipulation</td><td>자가 밀봉 구조와 PWM 여기, sliding-mode 보정을 결합한 MR haptic actuator로 토크 렌더링 오차를 PID 대비 최대 77% 줄이는 하드웨어 중심 연구다.</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2608.19794'>Towards general embodied intelligence: integrating large language models, knowledge bases, and reasoning capabilities to build the next generation of AI agents</a></td><td>28</td><td>4</td><td>Embodied AI</td><td>LLM·지식베이스·추론을 결합한 general embodied intelligence 개념 프레임워크를 제시하는 survey/position paper로 구현된 방법론이나 실험 증거가 없다.</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2608.19907'>Spike-based Belief Propagation in Nonlinear Dynamical Systems</a></td><td>28</td><td>3</td><td>RL</td><td>spiking neural network와 Bayesian inference를 결합한 brain-like controller를 mountain car 문제로 검증한 초기 단계 연구로 워크숍 논문 수준이다.</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2608.19298'>SceneGTMM: A Conformal Mapping-based Scene-Aware Transferable GNN-Transformer Dual-Graph Interaction Framework for Map Matching</a></td><td>28</td><td>2</td><td>CV</td><td>GNN-Transformer 기반 map matching 프레임워크로 자율주행 응용을 언급하나 도로망 매칭 문제에 국한되어 embodied AI와의 접점이 약하다.</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2608.20053'>On the Applicability of Safety Nets: A Safety-By-Design Solution for Certifying Neural Networks</a></td><td>28</td><td>2</td><td>RL</td><td>신경망과 lookup table을 결합한 Safety Net의 크기-성능 trade-off를 체계적으로 분석해 시스템 크기를 3자릿수 줄였으나 항공 인증 도메인 특화 연구로 로보틱스 일반화는 제한적이다.</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2608.20154'>Artificial Intelligence for Workflow Analysis in Colorectal Surgery: A Multicentric, Cross-Procedural Development and Generalization Study</a></td><td>28</td><td>1</td><td>CV</td><td>DINOv3와 계층적 TCN으로 대장 수술 워크플로우 단계를 인식하는 multicentric 모델로 수술 로봇과는 다소 거리가 있는 임상 검증 연구다.</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2608.19515'>Hear2Act: Benchmarking When Prosody Should Change What an Assistant Does</a></td><td>28</td><td>1</td><td>NLP</td><td>prosody가 어휘 정보로 명시되지 않을 때만 downstream 행동 선택에 실질적으로 기여함을 보이는 Hear2Act 벤치마크다. concern 상태를 명시적 텍스트로 표현할 때만 optimal-solution rate가 14.6%에서 39.6%로 상승해 audio-LLM의 암묵적 활용 한계를 드러낸다.</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2608.19408'>Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress</a></td><td>28</td><td>1</td><td>LG</td><td>teacher-derived reward와 독립적으로 추정한 reasoning progress 간의 ranking 불일치를 이용해 distillation reward를 선택적으로 억제하는 R2-OPD를 제안한다. on-policy distillation 대비 일관된 개선을 보이는 LLM reasoning 특화 기여다.</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2608.19719'>Scale-Separated Conditioning for Style-Encoder-Free Diffusion Stylization</a></td><td>28</td><td>0</td><td>CV</td><td>encoder 없이 crop 기반 style token만으로 diffusion stylization을 수행하는 기법으로 이미지 편집 응용에 한정된다.</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2608.19825'>Towards Clinically Faithful Medical Image Captioning via Enhanced Vision-Language Alignment</a></td><td>28</td><td>0</td><td>NLP</td><td>BioMedCLIP/SigLIP2 기반 의료 영상 captioning에서 training-time·inference-time alignment를 분리해 clinical fidelity를 높이는 도메인 특화 기법이다.</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2608.19965'>Flow Matching Meets 3D Curvilinear Structure Segmentation in Medical Imaging</a></td><td>28</td><td>0</td><td>CV</td><td>flow matching으로 3D 혈관 등 curvilinear 구조를 분할하는 의료 영상 기법이며 diffusion 대비 추론 효율을 높였다.</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2608.20229'>Prompt-Conditioned Channel Attention for Hierarchical Feature Modulation toward Anatomy-Agnostic Segmentation</a></td><td>28</td><td>0</td><td>CV</td><td>prompt 기반 channel attention을 encoder-decoder 전 층에 깊게 통합한 의료 영상 분할 모듈로 여러 벤치마크에서 IoU를 개선한다.</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2608.20334'>Swift-Image: Exploring the Performance Frontier of Compact Unified Image Generation Models</a></td><td>28</td><td>0</td><td>CV</td><td>6B 파라미터로 생성·편집을 통합한 compact diffusion 모델을 체계적 training engineering으로 구축한 엔지니어링 중심 연구다.</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2608.19436'>Longitudinal Bayesian Learning of Continuous Disease Position across the Alzheimer&#x27;s Disease Continuum</a></td><td>28</td><td>0</td><td>LG</td><td>longitudinal DTI로 알츠하이머 진행도를 연속적 latent 변수로 추정하는 Bayesian 프레임워크로 ADNI 코호트에서 검증된다.</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2608.19463'>LLM as Detector: An In-context Learning Approach for Tabular Anomaly Detection</a></td><td>28</td><td>0</td><td>LG</td><td>tabular anomaly detection에 LLM in-context learning을 적용한 연구로 robotics와 무관하며 방법론적 novelty도 제한적이다.</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2608.20183'>Exact Algebraic Computation of Learning Coefficients for Two-Dimensional Singular Models</a></td><td>28</td><td>0</td><td>LG</td><td>2차원 singular model의 learning coefficient(RLCT)를 최초로 정확히 계산하는 결정론적 알고리즘을 제시하는 이론 연구다.</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2608.19802'>Stopping and Routing LLM Judge Panels</a></td><td>28</td><td>0</td><td>LG</td><td>judge 후보를 copy, complement, specialist 역할로 분류해 비용 대비 최적 judge panel을 구성하는 정책을 제안한다. 여러 평가 도메인에서 실용적인 call plan을 제공하는 방법론적 기여다.</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2608.20169'>Task-CoEvolve: Efficient Harness Optimization via Adaptive Validation Task Selection</a></td><td>28</td><td>0</td><td>LG</td><td>harness와 validation task를 함께 진화시키며 variance-weighted sampling으로 informative task만 선별 평가하는 Task-CoEvolve를 제안한다. Terminal-Bench 2.1에서 전체 평가 대비 80% 평가 횟수를 줄이면서 동일 성능을 유지하는 효율화 기여다.</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2608.20331'>G-CARL: Grounded Checklist-Aligned Reward Learning for Patient-Oriented Medical Report Interpretation</a></td><td>28</td><td>0</td><td>Multimodal</td><td>atomic claim 검증과 checklist 기반 coverage를 결합한 grounded RL 프레임워크 G-CARL로 환자 대상 의료 리포트 해석을 최적화한다. 의료 도메인 특화 RL fine-tuning 기여로 로봇 학습과는 무관하다.</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2608.19689'>Rethinking the Evaluation and Optimization of LLM-Based Social Simulation</a></td><td>28</td><td>0</td><td>NLP</td><td>주관성이 큰 사회 시뮬레이션 과제에서 hard-label accuracy 평가의 한계를 subjectivity coefficient로 정량화하고 soft-label training SALT를 제안한다. 19,300개 문항의 SUBJSIM 벤치마크로 검증했으나 로봇과는 무관한 사회과학 응용이다.</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2608.19966'>Rethinking Patch Based Multivariate Time Series Forecasting with Semantic Structured Partitioning</a></td><td>28</td><td>0</td><td>LG</td><td>의미 단위 기반 patch partitioning으로 다변량 시계열 예측을 개선한 방법이나 로보틱스와 무관한 예측 태스크다.</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2608.19882'>TESTNAV: Pareto-Guided Search for Compositional Robustness Testing</a></td><td>27</td><td>0</td><td>CV</td><td>Pareto 기반 compositional robustness testing 프레임워크로 탐색 효율을 최대 2.15배 높였으나 로보틱스와 무관한 평가 방법론 논문이다.</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2608.19447'>Quantifying Event Impacts on Time Series via Multiscale Contrastive Learning</a></td><td>26</td><td>1</td><td>LG</td><td>사이버보안 사고 공시가 주가에 미치는 단기 영향을 multiscale contrastive learning으로 예측하는 금융 시계열 기법이다.</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2608.19621'>Mitigating Identity Essentialism in LLM Agents with Longitudinal Life Trajectories</a></td><td>26</td><td>1</td><td>NLP</td><td>구조화된 life-event retrieval과 parametric memory를 결합한 LifeMem으로 social simulation agent의 identity essentialism을 완화한다. Add Health와 Understanding Society 데이터에서 인간 응답 분포와의 정합성을 개선했으나 로봇 memory와는 응용 영역이 다르다.</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2608.20069'>V-REX: Efficient Specialist VLM Training for Veterinary X-Rays</a></td><td>26</td><td>0</td><td>Multimodal</td><td>수의학 X-ray 특화 VLM을 소규모로 처음부터 학습해 대형 범용 모델을 능가하는 도메인 특화 시스템이다.</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2608.20144'>PelviNeXt: A Modality-Agnostic Hybrid Network for Pelvic Imaging in Women&#x27;s Health</a></td><td>26</td><td>0</td><td>CV</td><td>초음파와 X-ray에 공통 적용되는 modality-agnostic 골반 영상 네트워크로 여성 건강 데이터 부족 문제를 다루는 의료 특화 연구다.</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2608.20212'>Unwarping the Lens: A Physics-Grounded Approach to Video Glasses Removal</a></td><td>26</td><td>0</td><td>CV</td><td>렌즈 광학을 물리 시뮬레이션한 데이터로 안경을 제거하는 얼굴 편집 기법으로 identity drift 완화에 초점을 둔다.</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2608.20305'>CalcSeg: Confidence-aware 3D Latent Context Curriculum Learning For Myocardial Scar Segmentation From Single-Stack LGE-CMRs</a></td><td>26</td><td>0</td><td>CV</td><td>confidence-aware curriculum learning으로 single-stack LGE-CMR에서 심근 반흔을 분할하는 의료 영상 기법이다.</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2608.20336'>WithEveryone: Unified Planning and Identity Grounding for Group Image Generation</a></td><td>26</td><td>0</td><td>CV</td><td>최대 10명까지 identity를 layout에 정합시키는 group image generation 프레임워크로 face similarity와 중복률을 개선한다.</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2608.19207'>Compliance, Capability, and Conflict: Benchmarking Multimodal LLMs under System Messages</a></td><td>26</td><td>0</td><td>Multimodal</td><td>MMVet-v2 기반으로 system message 준수와 vision-language 성능을 동시에 측정하는 VSysBench를 제안한다. 16개 MLLM에서 system message가 정확도를 저해하고 open-weight 모델의 compliance가 충돌 시 붕괴함을 보였으나 벤치마크 구축 위주 기여다.</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2608.20314'>MidTool: Mid-training Data Synthesis for Agentic Tool Use</a></td><td>26</td><td>0</td><td>NLP</td><td>tool-use 능력을 위한 mid-training 코퍼스 구축 파이프라인으로 BFCL·tau2-Bench에서 성능을 높였으나 로보틱스와 무관한 데이터 구축 연구다.</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2608.19593'>The Verification Gap in Networked Physical AI: A Post-Semantic Communication Framework</a></td><td>25</td><td>3</td><td>Embodied AI</td><td>networked physical AI에서 task-effective proposal과 physically justified action 사이의 verification gap을 정의하고 evidence 기반 통신 프레임워크를 제안하는 시스템 설계 연구다.</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2608.19632'>Complementary, Not Cumulative: Interaction Effects in Physics-Informed Neural Networks for Navier-Stokes Vortex Shedding</a></td><td>25</td><td>1</td><td>LG</td><td>PINN 기법들이 단독으로는 효과가 없고 SIREN activation과 causal weighting을 결합할 때만 Navier-Stokes vortex shedding을 잘 재현함을 보인 실증 연구다.</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2608.19643'>Time-Uniform Self-Normalized Concentration for Discounted Least Squares: Limits and Corrections</a></td><td>25</td><td>1</td><td>RL</td><td>discounted least-squares의 기존 self-normalized concentration bound가 실제로는 성립하지 않음을 반례로 보이고 수정된 bound를 제시하는 이론 교정 논문이다.</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2608.19666'>MUST-PET: MUltimodal Self-supervised learning across Tracers for whole-body PET/CT-based lesion segmentation</a></td><td>25</td><td>0</td><td>CV</td><td>PET-CT 병변 분할을 위한 multi-tracer self-supervised 프레임워크로 의료 영상 도메인에 국한된다.</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2608.19808'>FAR-DPO: Feasibility-Aware and Robust Direct Preference Optimization for Cyclic Peptide Design</a></td><td>25</td><td>0</td><td>LG</td><td>cyclic peptide 설계를 위한 feasibility-aware DPO(FAR-DPO)로 신약 개발 응용이며 robotics와 무관하다.</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2608.19890'>Reliable Neural Collapse Approximation for Open-World Test-Time Adaptation</a></td><td>25</td><td>0</td><td>CV</td><td>neural collapse를 구조적 prior로 활용해 open-world test-time adaptation에서 OOD 샘플을 걸러내는 ReNC를 제안하는 점진적 개선 연구다.</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2608.20005'>Scale-Aware Pretraining of Time Series Foundation Models via Multi-Patch Token Alignment and Hybrid Masking</a></td><td>25</td><td>0</td><td>LG</td><td>다양한 sampling frequency를 다루기 위한 scale-aware token alignment로 time series foundation model을 사전학습하는 SATS를 제안한다.</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2608.20295'>Physical-Support Confidence Sets for Highly Coherent Dictionaries</a></td><td>25</td><td>0</td><td>LG</td><td>highly coherent dictionary에서 물리적 해석의 신뢰구간을 dictionary·representation 불확실성을 함께 고려해 도출하는 이론적 신호처리 연구다.</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2608.19206'>Hallucination as a Feature, not a Defect: Evaluating a multi-agent architecture to transform speculative language-model outputs into testable scientific hypotheses</a></td><td>25</td><td>0</td><td>NLP</td><td>고엔트로피 생성 agent와 web-grounded 평가 agent를 결합해 hallucination을 speculative hypothesis로 전환하는 multi-agent 구조를 제안한다. ablation 결과 self-reflection 대비 일관된 우위를 보이지 못해 novelty가 제한적이다.</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2608.19407'>HiRA-CAM: Preserving Fine-Grained Spatial Relevance in Gradient-Based Visual Explanations</a></td><td>24</td><td>1</td><td>CV</td><td>LayerCAM을 개선한 gradient 기반 saliency map 기법으로 다층 activation을 활용하지만 기존 CAM 계열의 소폭 개선에 그친다.</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2608.20026'>From Street View Imagery to Street Quality Indicators: Vision Language Inference for the Suburban 15-minute City</a></td><td>24</td><td>1</td><td>Multimodal</td><td>Street View 이미지에 VLM을 적용해 보행 친화성을 평가하는 도시계획 응용 워크플로우다.</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2608.19222'>Interaction valence reveals contrasting social networks in dairy cattle</a></td><td>24</td><td>1</td><td>CV</td><td>pose 기반 CV pipeline으로 젖소 상호작용을 affiliative/agonistic valence로 구분해 사회연결망을 구성한다. 자동·수동 라벨 일치율 82.8%, macro-F1 0.872를 보이는 응용 CV 연구로 로봇 학습과는 거리가 있다.</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2608.19637'>TextRefine: Improving Textual Fidelity, Spatial Placement, and Glyph Rendering for Text Editing in Product Posters</a></td><td>24</td><td>0</td><td>CV</td><td>제품 포스터의 텍스트 편집 품질을 개선하는 post-training 기법으로 특정 상업 응용에 특화되어 있다.</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2608.19297'>Holtercare-Bench: A Multimodal Benchmark for Evaluating Long-Term Dynamic ECG Analysis</a></td><td>24</td><td>0</td><td>Multimodal</td><td>장기 Holter ECG에 대한 signal-video-text tri-modal 벤치마크로 기존 MLLM의 장시간 병리 시퀀스 처리 한계를 드러낸다.</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2608.20044'>End-to-end Early Classification of Time Series in Non-Stationary Environments</a></td><td>24</td><td>0</td><td>RL</td><td>non-stationary 환경에서 표현학습·분류·triggering을 RL로 end-to-end 학습하는 DQeND를 제안해 시계열 조기분류의 separable 설계 가정에 도전한다.</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2608.19437'>Are LLMs becoming similarly creative? Evidence from three years of models</a></td><td>24</td><td>0</td><td>NLP</td><td>3년간 모델 출시에 걸친 sentence-embedding 유사도 분석으로 LLM 창작 출력의 다양성이 통계적으로 유의하게 감소함을 보인다. 예비 분석 수준으로 causal mechanism은 다루지 않는다.</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2608.19981'>HealMed: Multilingual Evaluation of Large Language Models in Medicine</a></td><td>24</td><td>0</td><td>NLP</td><td>9개 언어, 9개 데이터셋으로 구성된 의료 LLM 다국어 벤치마크 HealMed를 23명의 의료 전문가와 구축한다. 저자원 언어에서 성능 저하가 크고 의료 특화 모델도 다국어 강건성이 보장되지 않음을 보이는 벤치마크 논문이다.</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2608.20281'>Inject, Align, Recover: Staged Post-Training for Retrieval-Free Document Knowledge Internalization</a></td><td>24</td><td>0</td><td>NLP</td><td>문서 지식을 continuation·rewrite·instruction 재구성 목적함수로 주입하고 QA alignment 후 일반 능력을 복원하는 3단계 post-training IAR을 제안한다. domain QA 정확도 3.6%p, 일반 성능 12.1%p 개선을 보이는 post-training 기법 수준의 기여다.</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2608.19902'>Bringing analytic rigor to agentic AI for science: The Brain Researcher platform for neuroimaging data analysis</a></td><td>24</td><td>0</td><td>NLP</td><td>신경영상 분석용 agentic research harness로 tool-selection 정확도를 23.3%에서 93.6%로 높였으나 로보틱스와 무관한 과학 연구 도메인이다.</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2608.20019'>Contrastive Mixed Prompt Learning for Incomplete Multimodal Sentiment Analysis with Unseen Modality Combination</a></td><td>24</td><td>0</td><td>Multimodal</td><td>unseen modality combination에 대응하는 prompt 기반 멀티모달 감성 분석 방법으로 로보틱스와 무관하고 특정 태스크 성능 개선에 그친다.</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2608.19480'>VideoRun2D Demo: Markerless Body Tracking for Biomechanical Analysis of Running</a></td><td>22</td><td>1</td><td>CV</td><td>스프린트 biomechanics 분석을 위한 markerless pose tracking demo로 스포츠 응용에 초점이 맞춰져 있다.</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2608.19580'>Mix&amp;Fix-Net: A Dual-Stage Trajectory Prediction Model for AIS and Vision-Derived Vessel Data</a></td><td>22</td><td>1</td><td>CV</td><td>AIS/vision 기반 선박 궤적 예측 모델로 해상 안전 도메인에 특화되어 있다.</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2608.19218'>Time-Series Retrieval for Grounding Multimodal Language Models in Remaining Useful Life</a></td><td>22</td><td>1</td><td>Multimodal</td><td>유사 degradation segment를 검색해 시각적 비교 artifact로 변환한 뒤 MLLM에 입력하는 retrieval 기반 remaining useful life 추정 프레임워크다. C-MAPSS FD001에서 검색이 예측 오차를 줄였으나 모델 용량에 성능이 의존하는 제한적 개선이다.</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2608.19646'>PL-NBA: A Possession-level Universal Basketball Video Dataset Supporting Multiple Visual Understanding Tasks</a></td><td>22</td><td>0</td><td>Video</td><td>possession 단위 NBA 비디오 데이터셋으로 스포츠 비디오 이해에 특화되어 있다.</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2608.19738'>Learning to Beat: Phenotype-Guided Latent Flow with Regional Motion Priors for Biventricular Motion Synthesis</a></td><td>22</td><td>0</td><td>CV</td><td>단일 ED mesh로부터 심실 전체 주기 모션을 합성하는 phenotype 조건부 flow 모델로 심장 영상 도메인에 특화되어 있다.</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2608.19304'>Quantum Kernel Estimation for the Discovery of Early Lung Cancer Detection</a></td><td>22</td><td>0</td><td>LG</td><td>cfDNA fragmentomics/methylation에 quantum kernel SVM을 적용한 폐암 조기진단 탐색 연구로 일부 조건에서만 classical SVM을 능가한다.</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2608.19735'>RecPFN: Prior-Fitted Networks for In-Context-Based Recommendations</a></td><td>22</td><td>0</td><td>LG</td><td>synthetic causal prior로 사전학습한 in-context recommendation 모델로 robotics와 무관한 추천시스템 연구다.</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2608.19858'>Online Test-Time Adaptation for Generalizable Dynamic Graph Anomaly Detection</a></td><td>22</td><td>0</td><td>LG</td><td>동적 그래프 이상탐지를 위한 online test-time adaptation 기법으로 robotics와 무관하다.</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2608.19906'>PETA:Parameter-Efficient Test-Time Adaptation for Virtual Screening</a></td><td>22</td><td>0</td><td>LG</td><td>virtual screening 모델을 pocket별로 LayerNorm만 업데이트해 test-time adaptation하는 PETA로 신약 스크리닝 응용이다.</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2608.20025'>CLaST: Context-aware Contrastive VAE for Probabilistic Time Series Forecasting</a></td><td>22</td><td>0</td><td>LG</td><td>contrastive loss로 문맥 유사성을 보존하는 VAE 기반 확률적 시계열 예측 CLaST를 제안한다.</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2608.20052'>DecoVAE: a Lightweight Interpretable Trend-Seasonal VAE Framework for Efficient Probabilistic Time Series Forecasting</a></td><td>22</td><td>0</td><td>LG</td><td>trend와 seasonal 성분을 분리해 해석 가능하게 모델링하는 경량 VAE(DecoVAE)로 시계열 예측 응용 연구다.</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2608.20285'>Dynamic Structural Causal Modeling for Sleep</a></td><td>22</td><td>0</td><td>LG</td><td>PCMCI+로 수면무호흡 causal graph를 성별·연령별로 학습한 의료 응용 causal discovery 연구다.</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2608.19800'>LoRA-GA$^2$: Low Rank Adaptation with Multi-step Gradient Adaptive Alignment</a></td><td>22</td><td>0</td><td>LG</td><td>multi-step gradient probe로 rank 할당과 초기화를 개선하는 LoRA-GA2를 제안한다. GLUE에서 평균 0.66점, GSM8K에서 1.03점 개선에 그쳐 기존 LoRA variant 대비 incremental한 개선이다.</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2608.20083'>SABET-QA: Temporal Knowledge Graph Question Answering</a></td><td>22</td><td>0</td><td>NLP</td><td>bidirectional entity-temporal scoring과 differentiable working memory로 multi-hop temporal KGQA를 반복적으로 정제하는 SABET-QA를 제안한다. CronQuestions 등에서 개선을 보이나 기존 embedding 기반 방법의 확장 수준이다.</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2608.20106'>OenoBench: A Wine-Domain Benchmark for Knowledge-Grounded Evaluation of Large Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>38,104개 출처 검증 사실로 구성한 와인 도메인 지식 벤치마크 OenoBench를 구축한다. o3가 83.6%로 최고 성능을 보이며 Anthropic 모델의 자기선호 편향(+9pp) 등을 드러내는 벤치마크 분석이다.</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2608.19299'>Air Traffic Control Using Large Language Models: Prompt Engineering, Architecture, and Evaluation</a></td><td>22</td><td>0</td><td>NLP</td><td>실제 비행 교신을 ground truth로 LLM 기반 항공관제(ATC) 발화 생성을 prompt 구조별로 평가한다. 가장 가벼운 prompt가 최고 성능을 보이고 과도한 제약은 오류가 누적되어 붕괴함을 보이는 응용 실험이다.</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2608.19625'>Scientific Data Skills: Enabling Agent-Ready Scientific Data Services at Scale</a></td><td>22</td><td>0</td><td>LG</td><td>과학 데이터셋을 agent가 발견·해석·호출할 수 있도록 reusable skill로 패키징하는 Scientific Data Skill(SciDSK)을 제안한다. 6개 분야에 걸친 인프라 구축 논문으로 새로운 학습 패러다임 기여는 아니다.</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2608.19680'>Frequency-Aware Continual Learning for Smart Contract Vulnerability Detection with Large Language Models</a></td><td>22</td><td>0</td><td>LG</td><td>Fourier domain LoRA와 forgetting-risk 기반 replay, anchor-protected merging을 결합한 3단계 continual learning 파이프라인으로 스마트컨트랙트 취약점 탐지를 다룬다. 블록체인 보안 도메인에 특화된 조합형 기여다.</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2608.19789'>TT-net: Quantum Inspired Tensor Network Denoising in Conditional GANs</a></td><td>22</td><td>0</td><td>CV</td><td>cGAN denoising의 SVD 블록을 tensor-train으로 교체한 module 수준 개선으로 novelty가 제한적이며 로보틱스 관련성은 없다.</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2608.20320'>An Agentic Approach for Active Data Collection, Travel Behavior Modeling, and Weather-Sensitive Demand Prediction</a></td><td>22</td><td>0</td><td>NLP</td><td>대화형 설문과 LLM 예측을 결합한 travel behavior 모델링 연구로 로보틱스와 무관한 교통 수요 예측 응용이다.</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2608.19740'>Keeping the Franka Emika Panda alive: a ROS 2 stack with a reliable position interface</a></td><td>20</td><td>4</td><td>Manipulation</td><td>Franka Emika Panda의 external position control 불안정성 원인을 규명하고 비동기 hardware interface로 해결한 ROS 2 오픈소스 스택으로 연구 기여보다는 엔지니어링 인프라 성격이 강하다.</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2608.19210'>Towards On-Board Implementation of ML-Based Helicopter Weight Estimator</a></td><td>20</td><td>1</td><td>LG</td><td>항공기 이륙 중량을 예측하는 LSTM 모델을 인증 규정에 맞춰 온보드 구현한 산업 응용 연구로 embodied AI와는 거리가 멀다.</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2608.19385'>Beyond Recognition: Compact Multi-Domain Arabic Manuscript HTR with Candidate-Selection Analysis and Evidence-Preserving Review</a></td><td>20</td><td>0</td><td>NLP</td><td>아랍어 고문서 인식 파이프라인으로 CER을 크게 낮췄으나 robotics/embodied AI와 무관한 도메인 특화 시스템이다.</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2608.19234'>Triangular Fuzzy Rescaling Distance</a></td><td>20</td><td>0</td><td>LG</td><td>선형 재척도를 거리 계산에 직접 통합한 triangular fuzzy number metric으로 metric 성질을 수학적으로 증명하는 이론 연구다.</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2608.19497'>Empirical Characterization of Learning Geometry in Hybrid Quantum Forecasting Models</a></td><td>20</td><td>0</td><td>LG</td><td>hybrid quantum forecasting model의 NTK 학습 geometry를 분석한 소규모 실증 연구로 robotics와 무관하다.</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2608.19659'>FleetSieve: Decision-Critical Profiling for SLO-Aware LLM Fleet Configuration</a></td><td>20</td><td>0</td><td>LG</td><td>LLM serving fleet의 tensor-parallel 설정을 위한 decision-critical profiling 기법으로 시스템 최적화 연구이며 robotics와 무관하다.</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2608.19727'>A Locally Tokenized Generative Model for Robust Time-Series Watermarking</a></td><td>20</td><td>0</td><td>LG</td><td>multivariate time-series generative model에 대한 watermarking 기법으로 robotics와 무관하다.</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2608.20117'>SAE-Xplainers: Rule-Based Feature Interpretation for Extreme Earth Events</a></td><td>20</td><td>0</td><td>CV</td><td>극한 기상 이벤트 해석을 위한 지리적 modulation과 rule-based Sparse Autoencoder 설명기(SAE-Xplainers)로 climate 응용 연구다.</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2608.20315'>Explainable Transformer Models for Clinical Prediction Tasks on Structured Electronic Health Records</a></td><td>20</td><td>0</td><td>NLP</td><td>구조화된 EHR을 위한 BERT 기반 해석 가능 임상 예측 모델(BERT-LER)로 헬스케어 응용이다.</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2608.19199'>A Virtual Member of a Community of Practice for the Society of Petroleum Engineers: From Prototype to Deployment</a></td><td>20</td><td>0</td><td>NLP</td><td>석유공학 커뮤니티를 위한 RAG 기반 virtual assistant ATHENA의 배포 사례를 다룬다. multi-document retrieval과 answer validation을 개선했으나 로봇 학습과의 관련성은 없는 응용 시스템 논문이다.</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2608.19558'>Reliable Financial Named Entity Recognition under Domain Shift</a></td><td>20</td><td>0</td><td>NLP</td><td>SEC filing, 뉴스, 소셜미디어 3단계 domain shift 환경에서 금융 NER의 confidence 기반 selective prediction을 평가한다. self-consistency가 domain shift에 강건함을 보이나 극단적 shift에서는 abstention도 효과가 없어 실무적 한계를 확인한 벤치마크 연구다.</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2608.19746'>PersonalBench: Measuring the Authorship Gap in LLM Personalization</a></td><td>20</td><td>0</td><td>NLP</td><td>authorship verification 모델 LUAR로 개인화 생성 텍스트가 실제 저자 스타일에 도달하지 못함을(AUC 0.484-0.508 vs human floor 0.626) 정량화한 벤치마크다. 방법 간 차이가 거의 없어(spread 0.024) 진단적 가치가 큰 측정 도구 논문이다.</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2608.19216'>Bounded Sovereignty and the Control Tax: Pricing AI Oversight When the Deployer Does Not Own the Model</a></td><td>20</td><td>0</td><td>LG</td><td>deployer가 모델 소유권이 없는 상황에서 AI control protocol의 실행 가능성을 4계층 접근 typology로 분석한다. 135만 건 synthetic 시뮬레이션으로 뒷받침하나 실제 payment 시스템 증거는 아니라고 스스로 명시한 개념 검증 수준 연구다.</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2608.19511'>Symposium: Trust via Auditable Records for Communities of AI Scientist Agents</a></td><td>20</td><td>0</td><td>LG</td><td>AI scientist agent 커뮤니티의 분석·가설·증거를 불변 기록으로 남기는 auditable record 프레임워크 Symposium을 제안한다. 구조화된 과학적 논증 기록을 위한 인프라 논문으로 새로운 학습 방법론은 아니다.</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2608.19974'>ReguSim: Evaluating LLM Agent Rule Grounding in Financial Compliance</a></td><td>20</td><td>0</td><td>NLP</td><td>금융 컴플라이언스 환경에서 LLM agent의 rule grounding을 평가하는 벤치마크로 로보틱스와 무관하다.</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2608.20240'>QUASAR: A Quantum-Classical Neural Network for SAR Satellite Physical-Layer Authentication</a></td><td>20</td><td>0</td><td>CV</td><td>SAR 위성 물리계층 인증을 위한 quantum-classical hybrid 분류기로 데이터 효율을 높였으나 로보틱스와 무관한 보안 도메인이다.</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2608.20322'>A comparison between ceiling-mounted FMCW, IR-UWB and Wi-Fi radar for in-bedroom human activity monitoring and sleep interruption detection</a></td><td>18</td><td>1</td><td>CV</td><td>천장형 FMCW·IR-UWB·Wi-Fi radar를 동일 조건에서 비교한 수면 모니터링 센싱 연구로 robotics 센서 perception과는 거리가 있다.</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2608.19584'>Kähler landscapes for complex neural network descents and guarantees including a search and destroy of the Calabi-Yau manifold</a></td><td>18</td><td>0</td><td>LG</td><td>복소 파라미터 신경망의 loss landscape를 Kähler geometry로 분석한 이론 연구로 실용적 함의와 실증적 검증이 부족하다.</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2608.19658'>Rationally Enriched Chebyshev Trunk Bases for DeepONet Surrogates of High Péclet Entrance Transport</a></td><td>18</td><td>0</td><td>LG</td><td>high-Péclet 물질전달 문제를 위한 DeepONet trunk basis 개선 연구로 robotics와 무관한 수치해석 응용이다.</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2608.19672'>SAGE-XGBoost: Spatially Augmented Graph Embeddings--Machine Learning Framework for Natural Hazards Susceptibility Mapping under Data Scarcity</a></td><td>18</td><td>0</td><td>LG</td><td>산사태·산불 susceptibility mapping을 위한 graph embedding 기반 XGBoost 프레임워크로 robotics와 무관한 지리공간 응용이다.</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2608.19801'>Unsupervised Anomaly Detection Using Flow Matching on Tabular Data</a></td><td>18</td><td>0</td><td>LG</td><td>오염된 학습 데이터 하에서 flow matching 기반 tabular anomaly detection의 scoring function을 비교한 응용 연구다.</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2608.20181'>A Standardized Framework for Machine Learning in Power System Protection</a></td><td>18</td><td>0</td><td>LG</td><td>전력계통 보호 ML 연구의 평가 설계를 표준화하는 프레임워크로 도메인 특화 응용이며 robotics와 무관하다.</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2608.20258'>DICS: Data-Informed Centroid Splitting for Decision Tree Classifiers</a></td><td>18</td><td>0</td><td>LG</td><td>clustering 기반 후보 split을 구성해 decision tree 학습을 가속하는 DICS로 효율성 개선에 그치는 incremental 기여다.</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2608.19212'>NepOOC-M: Bilingual Nepali-English Benchmark and Comparative Analysis of Multimodal Architectures for OOC Detection</a></td><td>18</td><td>0</td><td>Multimodal</td><td>네팔어 out-of-context 오정보 탐지를 위한 최초의 벤치마크 NepOOC를 구축한다. text-only mBERT가 최고 multimodal 모델과 통계적으로 동등한 94.65% Macro-F1을 보여 데이터셋 규모 확장이 아키텍처 개선보다 중요함을 시사하는 벤치마크 논문이다.</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2608.19472'>SynFlow: A Multidimensional Diachronic Semantic Analysis Toolkit</a></td><td>18</td><td>0</td><td>NLP</td><td>통사·형태·구문 패턴을 통합적으로 다루는 diachronic semantic change 분석 툴킷 SynFlow를 공개한다. 독일어 형용사 viral 사례 연구 중심으로 새로운 학습 패러다임 기여는 아니다.</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2608.19549'>Generating Diverse Personas for User Simulators to Test Interview Dialogue Systems</a></td><td>18</td><td>0</td><td>NLP</td><td>LLM으로 다양한 persona를 자동 생성해 interview dialogue system 테스트용 user simulator를 만드는 방법을 제안한다. SIGDIAL 2025 발표작으로 발화 다양성 증가를 보이는 응용 수준 기여다.</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2608.19942'>Dynamic Gated Cross-Modal Fusion with Sarcastic-aware Contrastive Regularization for Multimodal Sarcasm Detection</a></td><td>18</td><td>0</td><td>Multimodal</td><td>instance-level modality gating과 sarcasm-aware contrastive regularization을 결합한 fusion 모듈을 제안한다. MMSD, MMSD2.0에서 baseline을 능가하나 SEKE 2026 발표의 소규모 module 추가 수준 기여다.</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2608.19957'>Natural Language Code Retrieval for 1C:Enterprise: An Open Benchmark and Efficient Bi-Encoder</a></td><td>18</td><td>0</td><td>NLP</td><td>1C:Enterprise 코드 검색을 위한 최초의 러시아어 도메인 벤치마크와 bi-encoder를 공개한다. 78만 개 synthetic triplet으로 학습해 baseline 대비 개선을 보이나 특정 플랫폼에 국한된 기여다.</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2608.19971'>Robust Incomplete Multimodal Sentiment Analysis via Iterative Proxy Correction</a></td><td>18</td><td>0</td><td>Multimodal</td><td>언어 정보가 결손된 상황에서 non-language modality로부터 proxy를 반복적으로 정제하는 iterative correction 프레임워크를 제안한다. MOSI, MOSEI, SIMS에서 baseline을 능가하나 SEKE 2026급 module 개선 수준이다.</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2608.19215'>How to Navigate Uncertainty About AI Consciousness</a></td><td>18</td><td>0</td><td>NLP</td><td>AI 의식에 대한 불확실성을 valence(경험의 유쾌·불쾌 상태) 평가로 대체해 다루기 쉬운 질문으로 전환할 것을 제안하는 철학 논문이다. 실험적 방법론이 없는 개념적 논증이다.</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2608.19932'>A Strong Linear Baseline for Whole-Heart Cardiac Shape Completion on CT, with an Open Eleven-Structure Statistical Shape Model</a></td><td>18</td><td>0</td><td>CV</td><td>심장 CT의 11-구조 statistical shape model과 closed-form completion 방법을 제안한 의료 영상 논문으로 로보틱스와 무관하다.</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2608.20218'>Electronic Navigational Chart Change Classification</a></td><td>18</td><td>0</td><td>LG</td><td>전자 해도 변경의 위험도를 gradient-boosted tree로 분류하는 응용 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2608.19568'>DraftFM: A FoundationModel for Day-Zero Drafting in Magic: The Gathering</a></td><td>15</td><td>0</td><td>LG</td><td>Magic: The Gathering draft를 위한 day-zero foundation model로 robotics와 무관한 게임 도메인 연구다.</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2608.19578'>A Two-Stage Time-Aware Transformer for Short-Horizon AECOPD Risk Prediction</a></td><td>15</td><td>0</td><td>LG</td><td>가정용 인공호흡기 파형으로 AECOPD 악화를 예측하는 임상 응용 연구로 robotics와 무관하다.</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2608.20024'>Systematic Evaluation of TabPFN-TS for Zero-Shot Probabilistic Heat Load Forecasting in District Heating Networks</a></td><td>15</td><td>0</td><td>LG</td><td>지역난방 열부하 예측에 TabPFN-TS 등 zero-shot 시계열 foundation model을 체계적으로 평가한 응용 연구다.</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2608.20038'>An Inclusive and Lightweight Approach to Federated Continual Learning for Cultural Heritage</a></td><td>15</td><td>0</td><td>LG</td><td>문화유산 이미지 분류를 위한 경량 federated continual learning(FedCurv-DR)으로 응용 도메인이 좁다.</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2608.19201'>Automatic bioinformatic software named entity recognition from literature</a></td><td>15</td><td>0</td><td>NLP</td><td>생물정보학 소프트웨어·데이터베이스 명칭을 인식하는 hybrid NER 모델 SNAIL을 제안한다. bioNerDS2 및 ChatGPT 등 LLM 대비 우수한 성능을 보이나 도메인 특화 engineering 기여로 로봇 연구와 무관하다.</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2608.19220'>Can Conversational AI loosen Us-Versus-Them Boundaries? The Effects of Common, Dual, and Separate Identity Framings on Pro-Immigrant Intergroup Helping</a></td><td>15</td><td>0</td><td>NLP</td><td>GPT-4o와의 5회 대화가 백인 참가자의 이민자 categorization을 common/dual identity 방향으로 완화시킴을 보인 preregistered 실험이다. 행동 변화는 유의하지 않아 인지적 재범주화와 실제 행동 간 격차를 드러낸다.</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2608.19361'>A Speech Corpus for Mizo Automatic Speech Recognition: Whisper and SraVaani 1.0 Fine-Tuning with Morphology-Aware Evaluation</a></td><td>15</td><td>0</td><td>NLP</td><td>저자원 언어 Mizo용 음성 17.62시간을 구축하고 Whisper와 SraVaani 1.0을 fine-tuning한다. morphology-aware 평가에서 Whisper-large-v3가 WER 7.22%를 보이나 특정 언어 자원 구축 위주의 기여다.</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2608.20204'>ContractScrub: A benchmark for final review of legal contracts</a></td><td>15</td><td>0</td><td>NLP</td><td>법률 계약서 최종 검토 능력을 평가하는 벤치마크로 로보틱스와 무관한 법률 도메인 논문이다.</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2608.20220'>InsufficiencyBench: Evaluating LLM legal advice on underspecified user queries</a></td><td>15</td><td>0</td><td>NLP</td><td>불완전한 질의에 대한 법률 자문 벤치마크로 로보틱스와 무관하다.</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2608.20271'>Catching the Rug: Early Prediction of Fraudulent Memecoins on Solana via Machine Learning</a></td><td>15</td><td>0</td><td>LG</td><td>Solana 밈코인 rug pull을 5분 데이터로 조기 탐지하는 응용 ML 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2608.19214'>Robust Metaheuristics under Uncertainty for Berth Allocation and Quay Crane Assignment: A Review</a></td><td>14</td><td>0</td><td>LG</td><td>불확실성 하 berth allocation·quay crane assignment를 위한 robust population-based metaheuristic을 정리한 첫 리뷰다. 항만 물류 도메인 서베이로 로봇 학습과는 무관하다.</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2608.19812'>When Saying No Makes Better Videos: Designing Dual Gatekeeping for Pedagogically Grounded AI Content Creation</a></td><td>14</td><td>0</td><td>NLP</td><td>교육용 AI 영상 생성에서 이중 거부 메커니즘을 설계한 워크숍 논문으로 로보틱스와 무관하고 기술적 기여가 작다.</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2608.20041'>A three-dimensional typology of agency for advanced AI systems</a></td><td>14</td><td>0</td><td>NLP</td><td>AI 시스템의 agency를 도덕·법·개인/집단 축으로 분류한 철학적 typology 논문으로 기술적 방법론이나 실험이 없다.</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2608.20201'>The Third Restructuring of Software Form: From the Three-Tier Architecture to Storage, Models, and Agents</a></td><td>14</td><td>0</td><td>LG</td><td>소프트웨어 아키텍처가 storage·model·agent로 수렴한다는 위상 논문으로 기술적 실험 증거가 부족하다.</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2608.19922'>Auditing Recorded Predictive Lead Service-Line Classifications Against Physical Verification: A Statewide Study of New York</a></td><td>12</td><td>0</td><td>LG</td><td>뉴욕주 상수도관 lead 예측 모델의 기록을 실제 검증과 감사한 정책 분석 연구로 ML 방법론적 기여가 없다.</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2608.19526'>Automated Summarization of Financial News Using Large Language Models and Retrieval-Augmented Generation: An Early Empirical Study (Fall 2023)</a></td><td>12</td><td>0</td><td>NLP</td><td>2023년 수행된 초기 실증 연구로 LLM과 RAG 기반 금융 뉴스 요약 파이프라인을 구축한다. Falcon-7B가 가장 우수했고 RAG는 반복·환각 문제를 보였으나 2026년 기준으로는 시의성이 낮은 오래된 실험이다.</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2608.19838'>Specification-delta-driven data governance: an empirical study of the «spec-delta» as the unit of change in lakehouse data platforms</a></td><td>12</td><td>0</td><td>LG</td><td>데이터 플랫폼 변경 관리를 위한 spec-delta 개념을 제안한 실증 연구 설계 논문으로 실제 실험 결과 없이 향후 시연을 예고하는 수준이다.</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2608.19994'>Green BOA: Determining the environmental break-even point for ML-based data compression</a></td><td>10</td><td>0</td><td>LG</td><td>ML 기반 데이터 압축의 탄소배출 손익분기점을 다룬 lightning-talk 수준의 짧은 워크숍 논문이다.</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2608.20149'>Evaluating Neural Cartographic Relief Shading for Urban Environments: A Downtown Calgary Study Using High-Resolution DEM and DSM Data</a></td><td>10</td><td>0</td><td>CV</td><td>도심 환경에서 neural relief shading 기법(Eduard)의 적용 가능성을 탐색한 지도제작 응용 연구로 ML 방법론적 기여가 거의 없다.</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2608.19200'>Transformer Models for Text Summarization: A Comparative Study of BART, BERT, and RoBERTa</a></td><td>10</td><td>0</td><td>NLP</td><td>BART, BERT, RoBERTa의 요약 성능을 비교하는 서술적 리뷰다. 새로운 방법이나 실험 없이 기존 아키텍처를 정리하는 수준에 그친다.</td></tr>
</tbody></table>

</details>
