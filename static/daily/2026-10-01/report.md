# 오늘의 arXiv Top 15 — 2026-10-01 (목)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**
> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)

**신규 논문 수: 전체 818편 → 중복 제거 후 818편 (이번 평가 대상 818편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 187 |
| cs.LG | 256 |
| cs.RO | 127 |
| cs.CL | 115 |
| cs.AI | 133 |

*1차 스크리닝: 전체 818편을 제목/초록 기반으로 채점(Claude (scheduled agent)) → 상위 15편은 arXiv 원문을 내려받아 정밀 리뷰(Claude (scheduled agent)) 후 최종 점수 산정.*

---

## Top 15

### 1. [86점] When Instructions Retrieve Trajectories: Diagnosing and Mitigating Generalization Failures in VLA Models

- **분야**: VLA · **robotics relevance**: 10/10
- **arXiv**: [2609.39971](https://arxiv.org/abs/2609.39971) ([PDF](https://arxiv.org/pdf/2609.39971))
- **저자**: Hung-Jen Chen, Yu-Hsun Hou, Yan-Hong Chen, Yan-Fu Chen, Binghua Cai, Min Sun, Chun-Yi Lee
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 66점

> 💡 π0.5·GR00T-N1.7 같은 VLA가 language와 vision 둘 다에 반응하면서도 이를 결합해 올바른 행동을 선택하지 못하는 instruction-action binding 실패를, 행동 분석과 internal state 개입으로 규명함. 같은 instruction이 scene에 따라 다른 action을 요구하는 counterfactual demonstration과 paired loss로 학습하는 Equivariant Counterfactual Training(ECT)을 제안해 LIBERO-PRO position-swap 성공률을 36%에서 59%로, 실로봇 unseen-position 성공률을 8%에서 88%로 올림.

**Core innovation & methodology**

- VLA 실패를 nuisance(행동 불변 perturbation)와 counterfactual(행동 요구 변경 perturbation)로 구분하고, 둘 다에 강건해 보이는 aggregate robustness score가 instruction-action binding 실패를 가릴 수 있음을 지적함
- 381개 targeted probe에서 실패 rollout의 69%가 source task나 다른 demonstrated task를 그대로 재현하는 retrieval-like 행동임을 human labeling(inter-annotator κ=0.78)으로 확인함
- flow matching objective를 분석해, demonstration의 narrow conditional action support 하에서는 instruction-keyed lookup 해와 grounded 해가 수학적으로 구분되지 않음을 보임
- ECT를 제안함: 같은 instruction·다른 scene·다른 요구 action의 five-tuple 쌍을 구성하는 ECT data와, 두 counterpart의 imitation loss를 한 업데이트에서 같이 최적화하는 ECT loss로 구성됨
- internal state 개입(prefix-KV readout으로 모델 내부 KV cache에서 현재 실행 중인 task 표현을 교체)으로 행동이 바뀌는지 확인해, VLA가 실행 task를 internal state에 인코딩함을 mechanistic하게 보임

**Novelty vs. prior works**

- 가장 가까운 prior work인 CAG(Fang et al., 2026)는 inference 시점에 language conditioning을 강화하는데, ECT는 학습 데이터의 supervision 구조(conditional action support 부족) 자체를 고친다는 점에서 본질적으로 다름
- RoCoDA·MimicGen과 scene 변환 mechanism은 유사하지만, instruction-action binding 진단에서 역으로 필요한 counterfactual 쌍을 설계했다는 problem formulation의 novelty가 있음
- prefix-KV readout과 closed-loop intervention으로 실행 task가 internal state에 인코딩되어 교체 시 행동이 바뀐다는 mechanistic 증거를 제시한 점은 기존 counterfactual augmentation 연구에 없던 기여임

**Benchmark results**

- LIBERO-PRO 4개 suite 모두에서 official π0.5·GR00T-N1.7 checkpoint가 nuisance cell 대비 counterfactual cell(Swap, Task)에서 최소 42pt 낮은 성공률을 보임
- Frozen-LM 조건(3 seed 평균)에서 ECT data+loss가 π0.5 mean Swap 성공률을 36%에서 59%로, mean Task를 21%에서 28%로 올림
- CALVIN ABC→D에서 추가 demonstration 없이 ECT loss만으로 5-task 연속 완료율(LH-5)이 58%에서 76%로 상승함
- 실로봇 UR5e에서 400 demonstration 고정 예산 하에 unseen-position 성공이 Standard 3/40에서 ECT data 30/40, ECT data+loss 35/40으로 증가함(task 종류는 본문에서 확인 불가)
- demonstration을 25%에서 100%로 늘려도 Swap·Task는 ID 대비 항상 34pt 이상 낮게 유지되어, 단순 demonstration 수 증가로는 해결되지 않음을 보임

**Top-tier conference 적합성 — 82/100 · 추천 venue: CoRL**

mechanistic diagnosis(readout·intervention)와 counterfactual training을 LIBERO·CALVIN·실로봇까지 일관되게 검증한 실험 강도가 높고, 서로 다른 두 VLA 아키텍처에서 같은 패턴이 재현되어 oral 후보로 볼 만함. 다만 저자 스스로 밝히듯 ECT는 training data에 없는 distinction은 만들지 못하고(bowl 고정 instruction 등), fine-tuning 이후 세팅에서만 검증되어 generalist 적용 범위가 제한적임.

**추천 이유 & 누리랩 연구와의 연결점**

- instruction-action binding 진단 틀은 누리랩의 VLA failure detection/diagnosis 연구에 바로 적용 가능함 — rollout이 familiar하지만 틀린 trajectory를 재현하는지 readout으로 검출하는 모듈 설계에 참고할 수 있음
- prefix-KV 교체로 action을 교정하는 test-time intervention 결과는 실패 감지 후 internal state를 고쳐 복구하는 test-time recovery 메커니즘의 proof-of-concept으로 쓸 수 있음
- ECT data 구성 방식(같은 instruction·다른 scene, replay controller로 action-valid 확보)은 robot memory·counterfactual augmentation 파이프라인에 바로 이식 가능함

---

### 2. [79점] BIND: Binding 3D Robot Actions to 2D Image Features

- **분야**: Manipulation · **robotics relevance**: 9/10
- **arXiv**: [2609.38443](https://arxiv.org/abs/2609.38443) ([PDF](https://arxiv.org/pdf/2609.38443))
- **저자**: Cameron Smith, Arsh Tangri, Vitor Guizilini, Yue Wang, Zubair Irshad, Sergey Zakharov
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 BIND는 3D action 후보를 camera geometry로 2D image feature에 투영해 결합하는 action head를 제안해, global feature pooling 기반 정책보다 data efficiency와 out-of-distribution robustness를 크게 높임. 실로봇에서 단 5개 demo로 near-perfect 성공을 달성하고, camera viewpoint·object position이 크게 바뀌어도 global-regression baseline이 완전히 실패하는 조건에서 성능을 유지함.

**Core innovation & methodology**

- 기존 global-regression 정책(ACT, Diffusion Policy, π0)은 CLS token 등 하나의 global feature vector에서 MLP로 action을 직접 regression해, action-feature 간 projective relationship을 데모만으로 학습해야 하는 구조임
- BIND는 end effector 후보 위치들을 3D volume으로 discretize하고, 각 후보를 camera pose·intrinsics로 매 camera view의 image feature map에 투영해 feature를 bilinear sampling함
- 후보 position과 투영된 image feature를 concat해 작은 MLP로 classification score를 매기고 cross-entropy로 학습하며, inference는 argmax로 위치를 선택함
- rotation·gripper는 선택된 위치의 feature를 teacher forcing(학습)/argmax(추론)로 인덱싱해 별도 MLP로 전체 chunk를 예측하고, image encoder(DINOv3)는 freeze하지 않고 head와 end-to-end fine-tuning함

**Novelty vs. prior works**

- PerAct·C2F-ARM·GNFactor 같은 voxel-categorical head와 유사하게 action을 3D 위치 classification으로 보지만, 이들은 voxel화된 RGB-D fusion에 의존해 free-space voxel에는 feature가 없고 sparse keyframe만 예측하는 반면, BIND는 free-space 후보도 projection으로 feature를 받아 dense-in-time chunk를 예측함
- RVT·RVT-2는 point cloud를 가상 view로 재렌더링해 2D heatmap을 예측한 뒤 멀티뷰 triangulation으로 3D를 복원하는데, BIND는 방향을 반대로 해 3D candidate를 2D로 내려 투영하므로 depth sensor, 재렌더링, triangulation이 모두 불필요함
- 핵심 아이디어는 action-feature 관계를 camera geometry라는 closed-form 식으로 explicit하게 제공한다는 것으로, 새로운 representation learning이 아니라 기존 2D encoder에 기하학적 inductive bias를 주입한 조합이라 architecture 자체의 참신성은 제한적이나 실용적 효과가 큼

**Benchmark results**

- 실로봇 cup pick-and-place에서 5개 demo만으로 BIND는 progress 100(10/10 성공)을 달성한 반면, ACT는 모든 data 규모에서 36% 이하, Motion Tracks는 31% 이하에 머묾
- OOD object position(학습은 테이블 왼쪽 절반, 평가는 오른쪽 절반)에서 BIND는 progress 63점(63/100)을 유지하는데 ACT와 Motion Tracks는 0으로 완전히 붕괴함
- OOD camera viewpoint(3개 미학습 시점 평균)에서 BIND는 79점, ACT는 1점, Motion Tracks는 4점에 그침
- LIBERO Spatial/Object suite에서 BIND는 92.0%/94.0%(평균 93.0%)로 OpenVLA(86.6%), SpatialVLA(89.1%)보다 높고 π0(97.8%), GR00T N1.7(97.6%) 등 대형 pretrained 모델에는 못 미침
- RoboTwin 5개 task 평균 성공률 77.8%로 point cloud 기반 ManiFlow-3D(61.9%)보다 높음. teapot·cup stacking·spill cleanup·fold towel 등 long-horizon dexterous task는 30~40개 demo 기준 단일 실험이고, 코드·모델 공개 여부는 본문에서 확인 불가

**Top-tier conference 적합성 — 80/100 · 추천 venue: CoRL**

실로봇 data efficiency·OOD robustness를 여러 baseline과 backbone으로 체계적으로 검증하고 LIBERO·RoboTwin 같은 표준 벤치마크까지 포함해 실험적 설득력이 매우 강함. 다만 방법 자체는 기존 2D/3D action head 계열 아이디어의 조합이라 conceptual novelty는 보통 수준이고, long-horizon dexterous task는 소수 demo(30~40개) 단일 실험이라 통계적 근거가 약한 점이 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- action head 설계에서 camera geometry를 explicit prior로 주는 아이디어는 누리랩 manipulation·VLA 정책을 실로봇에 이식할 때 OOD robustness를 높이는 가벼운 대안으로 바로 시도해볼 만함
- object-centric 3DGS나 scene graph 연구와 결합해, 3D candidate volume을 scene representation에서 직접 뽑아 action head에 연결하는 방식으로 확장 가능함
- failure detection/recovery 관점에서 image-bound feature 점수를 action 품질의 uncertainty signal로 재활용해 test-time verifier를 만드는 아이디어로 이어질 수 있음

---

### 3. [77점] PRICE the Action Chunks: Physical Relational Credit Assignment for Embodied Reinforcement Learning

- **분야**: RL · **robotics relevance**: 9/10
- **arXiv**: [2609.38890](https://arxiv.org/abs/2609.38890) ([PDF](https://arxiv.org/pdf/2609.38890))
- **저자**: Yangang Zou, Jiajun Lu, Weitao Zhou, Haibao Yu, Bozhou Zhang, Jiawei Wang, Honglong Tian, Minglei Li 외 1명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 64점

> 💡 Outcome 기반 RL로 VLA를 post-training할 때 trajectory 전체에 같은 advantage를 주는 문제를, 같은 물리적 상황에 도달한 다른 rollout들의 성공 여부를 서로의 참조로 삼아 action chunk 단위 credit으로 바꾸는 PRICE를 제안함. 추가 evaluator 없이 cross-trajectory physical relational graph와 confidence gating만으로 LIBERO·RoboTwin 2.0·실로봇에서 outcome-based baseline 대비 성공률과 학습 속도를 모두 개선함.

**Core innovation & methodology**

- 긴 horizon manipulation에서 outcome-based GRPO가 모든 action chunk에 같은 trajectory-level advantage를 주는 문제를 지적하고, 같은 물리적 situation에 도달한 rollout들의 terminal outcome을 서로의 참조로 쓴다는 insight를 제안함.
- visual·proprioceptive descriptor로 chunk 경계를 node로 clustering한 physical relational graph를 만들어 현재 round와 과거 round의 outcome을 pooling해 node별 success potential을 추정함.
- 두 endpoint의 potential 차이를 Hoeffding 부등식 기반 confidence interval로 gating해, 불확실한 credit은 버리고 신뢰할 수 있는 credit만 GRPO advantage에 더함.
- oracle potential 변화가 terminal-success objective의 gradient와 일치함을 이론적으로 보이고(Theorem 1), finite-sample 상황에서 credit 방향이 틀릴 확률의 bound를 제시함.

**Novelty vs. prior works**

- 가장 가까운 evaluator 기반 접근(VLA-RL, TGRPO, SRPO, world-model 기반 Feat2Go 등)은 학습된 reward·value model이나 world model, task-specific progress label이 필요한데, PRICE는 추가 evaluator 없이 rollout들 간의 물리적 대응만으로 credit을 뽑는다는 점이 본질적 차이임.
- agentic RL의 cross-trajectory credit assignment(RUDDER, graph 기반 agentic credit 등)를 embodied 영역으로 옮기면서, 연속적 visual·proprioceptive 관측에서 같은 물리적 상황을 정의하는 node matching 설계가 추가 기여임.
- 다만 node matching이 cosine similarity threshold 기반 clustering이라 viewpoint·appearance 변화에 취약할 수 있고, 저자도 이를 한계로 명시함. 이 부분은 새로운 representation이라기보다 기존 clustering 기법을 그대로 적용한 수준에 가까움.

**Benchmark results**

- LIBERO 4개 suite 평균에서 one-shot SFT initialization 48.9%에서 PRICE 적용 시 99.0%로 50.1pp 개선되어, evaluator 기반 SOTA인 SRPO(99.2%)와 거의 동등함.
- RoboTwin 2.0 6개 task 평균에서 SFT 31.9%에서 90.0%로 58.1pp 개선되어, world-model 기반 Feat2Go(88.8%)·RLinf-VLA(84.5%)·SimpleVLA-RL(71.3%)보다 각각 1.2, 5.5, 18.7pp 높음.
- 실로봇(HiFi-UMI) 2개 task에서 offline adaptation 방식인 PRICE-AWR(advantage-weighted regression 기반)이 macro-average 61.25%로 GRPO-AWR(같은 방식에 GRPO credit을 적용)보다 13.75pp 높음, 다만 rollout 60개만 쓴 소규모 실험임.
- ablation에서 historical evidence를 빼면 평균 성공률이 98.3%에서 94.0%로 거의 GRPO 수준(93.9%)까지 떨어지고, confidence gate를 빼면 96.9%로 낮아져 두 구성요소 모두 필요함이 확인됨.
- 독립적 Monte Carlo continuation test에서 gating 후 retained credit의 방향 정확도가 97.5%(gating 전 77.2%)로 높아져 credit이 실제 local progress와 일치함을 보임.

**Top-tier conference 적합성 — 76/100 · 추천 venue: CoRL**

이론적 분석(oracle alignment, finite-sample bound)과 LIBERO·RoboTwin·실로봇까지 이어지는 폭넓은 실험, 독립적 MC 검증으로 신뢰도가 높아 top-tier 수준의 empirical conviction을 갖춤. 다만 node matching이 단순 threshold clustering이라 복잡한 장면이나 더 긴 horizon으로의 확장성이 불확실하고, 실로봇 실험 규모가 작다는 점이 약점임.

**추천 이유 & 누리랩 연구와의 연결점**

- failure detection/recovery, credit assignment 주제와 직접 연결됨. 같은 물리적 상황에 도달한 rollout을 서로의 참조로 삼는다는 아이디어는 실패 원인 진단, 즉 어느 chunk가 실패를 유발했는지 찾는 데도 그대로 적용 가능함.
- test-time optimization·RL 주제에서 outcome-only label로 fine-grained credit을 뽑는 틀은 evaluator 학습 비용 없이 다른 embodied RL 세팅에도 이식 가능함.
- robot memory 관점에서, round를 넘어 누적되는 node summary(historical evidence)는 과거 경험을 재사용하는 memory 구조로 볼 수 있어 관련 연구와 연결 지어볼 만함.

---

### 4. [76점] Beyond the Remembered World: Predictive 4D Belief for Persistent Navigation in Evolving Worlds

- **분야**: Navigation · **robotics relevance**: 9/10
- **arXiv**: [2609.39166](https://arxiv.org/abs/2609.39166) ([PDF](https://arxiv.org/pdf/2609.39166))
- **저자**: Mingjian Gao, Zhaocheng Li, Haoyang Huang, Wenqiao Zhang, Yingjie Niu, Hao Zhou, Chao Li, Juncheng Li 외 2명
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 EvolvingNav는 과거 관측 이후에도 계속 변화하는 환경에서 target 위치를 추론하기 위해 persistence-relocation belief와 event-driven predict-observe-replan filter를 결합한 navigation agent를 제안함. 54개 scene·803,680개 task로 구성된 새 벤치마크 EvoWorld-Bench와 실로봇 LYNX M20 실험에서 기존 structured memory·predictive baseline 대비 탐색 성공률과 효율을 크게 올림.

**Core innovation & methodology**

- Evolving-World Navigation이라는 새 문제를 정의함: target이 query 이전뿐 아니라 navigation 도중에도 보이지 않는 사이 이동할 수 있는 상황에서 agent가 도착 시점의 상태를 예측하고 belief를 갱신해야 함
- P4D-Nav는 timestamped 3D object history를 Transformer로 인코딩해, target이 마지막 관측 위치에 머무는 persistence와 다른 후보로 옮기는 relocation을 분리해 확률을 배정하고, 알려지지 않은 위치(unknown)에도 확률 질량을 남겨둠
- event-driven filter가 belief를 현재 시점으로 propagate하고, 각 후보의 도착 예정 시간(ETA)에 맞춰 occupancy를 forecast한 뒤 RGB-D evidence로 belief를 갱신함
- negative observation은 calibrated visibility-conditioned detection probability로 soft하게 반영하고 동일 evidence 재사용을 방지함
- frozen zero-shot vision-language controller(GPT-5.6-Luna)가 memory·prediction·inspection·exploration·navigation tool을 호출해 belief 기반으로 행동을 선택하고 replan함

**Novelty vs. prior works**

- PredictiveGraphs가 future object-receptacle state를 예측하고 top-k navigation을 하는 가장 가까운 선행연구이나, EvolvingNav는 candidate별 도착 시간을 고려한 arrival-time filtering과 time-valid evidence round, candidate reopening을 추가해 navigation 도중의 hidden evolution까지 다룬다는 점이 다름
- Transit-Aware Planning은 이동 가능한 target을 다루지만 irregular observation history와 visibility 조건부 evidence를 결합하지 않음. EvolvingNav는 이 세 요소(irregular history, arrival-time별 후보 occupancy, visibility 조건부 negative evidence)를 하나의 loop로 묶은 것이 formulation 측면의 기여임
- belief 구조(persistence-relocation factorization) 자체는 상태를 last-seen·다른 후보·unknown 세 갈래로 나누는 필터링 설계로, 완전히 새로운 패러다임이라기보다 기존 predictive memory 연구의 구성요소를 navigation loop에 통합한 것에 가까움

**Benchmark results**

- EvoWorld-Bench(54개 scene, 803,680개 task)에서 First-Inspection SR이 DynaMem 45.33%에서 EvolvingNav 61.32%로, Search SR이 71.94%에서 86.18%로 상승함
- FindingDory에서 HL-SR(고수준 목표 성공률) 53.22%로 비교 대상 중 최고치를 기록했으나 HL-SPL(고수준 목표 경로 효율)은 38.83%로 FindingDory Agent(40.92%)에는 못 미침
- N4(실행 중 target이 이동하는 online-dynamic) 설정에서 PredictiveGraphs 대비 Dynamic SR +18.4점, Online Recovery SR +22.0점, excess distance -4.8m, revisit 성공 +13.7점 개선됨
- paired world 비교에서 routine world는 Last Seen 대비 SR +22.36점이지만 random world에서는 +6.93점에 그쳐, 학습 가능한 시간 패턴이 있을 때 이득이 가장 큼
- ablation에서 predictive belief를 제거하면 First-Inspection SR이 62.17%에서 12.51%로 급락하고 evidence update를 제거하면 Search SR이 42.02점 하락함. 실로봇은 LYNX M20 64회 매칭 trial에서 First-Inspection SR 17.2%→34.4%, Search SR 26.6%→48.4%로 개선됨(X30·Lite3는 32-trial transfer subset)

**Top-tier conference 적합성 — 74/100 · 추천 venue: CoRL**

새 문제 설정(Evolving-World Navigation)과 대규모 벤치마크, 여러 실로봇 플랫폼(LYNX M20·X30·Lite3) 검증까지 갖춰 실험 범위가 넓음. 다만 belief 설계 자체는 기존 predictive memory·filtering 아이디어의 조합이고 frozen VLM controller에 의존해 memory와 policy가 end-to-end로 학습되지 않는다는 점이 conceptual novelty를 제한함.

**추천 이유 & 누리랩 연구와의 연결점**

- 시간에 따라 변하는 world에서 belief를 유지·갱신하는 구조는 누리랩의 robot memory·failure detection 연구에서 기억이 틀렸을 가능성을 명시적으로 모델링하는 참고 사례로 쓸 수 있음
- persistence-relocation factorization과 visibility 조건부 negative evidence 처리는 object-centric 3DGS·scene graph에 시간 축을 추가해 scene graph가 낡아지는 문제를 다루는 연구로 확장 가능함
- 후보별 도착 시간에 맞춰 belief를 forecast해 행동을 고르는 방식은 long-horizon manipulation의 test-time replanning이나 counterfactual reasoning(현재 안 보이는 물체 위치 추론) 연구와 직접 연결됨

---

### 5. [75점] EWAM: Emergent Depth-Wise Specialization in a Unified Embodied Model -- From Semantic Understanding through Visual Foresight to Action

- **분야**: VLA · **robotics relevance**: 9/10
- **arXiv**: [2609.39973](https://arxiv.org/abs/2609.39973) ([PDF](https://arxiv.org/pdf/2609.39973))
- **저자**: Hao Wang, Jiajun Wen, Jingzhi Liu, Shuoshuo Xue, Zhiliang Chen, Min Lin, Yicheng Chang, Xiaoyu Guo 외 16명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 64점

> 💡 VLA(semantic)와 world-action model(미래 예측)을 하나의 transformer에 action-centric asymmetric attention으로 통합해, action query만 semantic·현재영상·예측미래·action 토큰을 모두 읽게 설계한 EWAM을 제안함. layer-wise 지도 없이도 얕은 층은 semantic, 중간층은 미래 예측, 깊은 층은 action에 집중하는 emergent depth-wise specialization이 학습 과정에서 자연 발생하고, 이를 활용한 정책이 RoboTwin·LIBERO·실로봇에서 기존 VLA·WAM·hybrid baseline을 능가함.

**Core innovation & methodology**

- VL expert(Qwen3-VL-2B 초기화), video expert(Wan2.2-TI2V-5B 초기화), action expert를 30-layer unified transformer에 두되, attention mask로 action query만 VL/video/action key를 모두 읽고 VL·video query는 자기 스트림만 읽게 제한함(action-centric asymmetric attention).
- 미래 영상과 action을 동시에 flow matching으로 denoise하는 joint objective를 써서, 별도로 생성한 미래 프레임을 프롬프트로 주는 pipeline 방식(π0.7, Cortex 2.0)과 달리 진화 중인 future-video feature가 action 계산에 직접 참여함.
- long-horizon demonstration을 subtask phase로 나눠 subtask 텍스트 예측과 phase index 회귀를 post-training에 추가해 long-horizon completion을 개선함.
- emergent depth-wise specialization을 attention allocation 측정, training checkpoint tracking, layer-targeted causal intervention, counterfactual future-feature injection(5개 task) 네 가지 방식으로 교차 검증함.

**Novelty vs. prior works**

- π0.5(VLA)·Fast-WAM(WAM)·Motus(multi-expert이지만 frozen VLM 외부 부착)는 action attention이 한 소스에 쏠리는데, EWAM은 같은 통합 구조에서 분업이 layer 깊이에 따라 자연적으로(emergent) 형성됨을 보여 차별화됨.
- 아키텍처 자체(asymmetric attention mask)는 비교적 단순한 설계이고, 핵심 기여는 발견한 현상(emergent depth-wise specialization)에 대한 인과적 검증(중간층 future masking 시 성공률 92.80%→3.55%로 붕괴)에 있음.
- 다만 emergent specialization 분석은 하나의 32-GPU 학습 run의 checkpoint tracking에 기반해, 다른 아키텍처·스케일에서도 재현되는 현상인지는 본문에서 확인 불가함.

**Benchmark results**

- RoboTwin2.0 clean-to-random에서 본문 서술은 72.1%, 인포그래픽 요약은 77.2%(baseline π0.5 58.35%, 4D-WAM 61.6%, GigaBrain-0.7 67.3%)로 두 수치가 다르게 제시되어 있어 정확한 비교 수치는 본문에서 확인 불가.
- RoboTwin2.0 in-domain 평균 92.9%, LIBERO 98.8%로 baseline(LingBot-VA 92.2%/98.5%, WLA-0 91.5%/98.6%, π0.5 -/96.9%, RoboTwin 수치는 본문에서 확인 불가) 대비 근소 우위.
- causal intervention(고정 체크포인트)에서 중간층 future-frame masking 시 성공률 92.80%→3.55%로 붕괴, 얕은층 VL masking 시 76.53%로 하락해 depth별 의존성을 정량적으로 입증함.
- counterfactual future-feature injection 실험에서 5개 task 25/25 성공이 주입 후 4/25로 급락해, action 생성이 예측된 미래 표현의 구체적 내용에 의존함을 인과적으로 보임.
- human egocentric 사전학습으로 held-out embodiment 성공률 40.1%→66.9%, egocentric co-training으로 장면 변화 조건 real-robot 성공률 10%→60%(최대 1,000개 ego demo 추가 조건); 다만 실로봇 세부 task별 성공률 표는 본문 추출 과정에서 생략되어 확인 불가.

**Top-tier conference 적합성 — 77/100 · 추천 venue: CoRL**

depth-wise specialization을 관찰-학습 과정 추적-인과적 개입-counterfactual injection까지 네 겹으로 검증한 분석은 보기 드문 rigor이며 VLA·WAM 통합 설계에 해석가능성을 더한 기여로 평가됨. 다만 핵심 실험 section 7의 수치가 텍스트 추출 과정에서 상당 부분 누락됐고 인포그래픽과 본문 서술 수치(72.1% vs 77.2%)가 불일치하는 점은 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- attention allocation 측정과 causal intervention 방법론은 누리랩의 world model-VLA 통합 연구에서 모델이 실제로 미래 예측을 쓰는지 검증하는 진단 도구로 그대로 쓸 수 있음.
- counterfactual future-feature injection 기법은 failure detection/recovery 연구에서 어느 내부 표현이 실패를 유발했는지 인과적으로 밝히는 방법으로 응용 가능함.
- camera-relative wrist action 표현 기반 human egocentric pretraining·co-training 파이프라인은 로봇 데이터가 부족한 cross-embodiment 연구에 참고할 만함.

---

### 6. [75점] ChronoGraph: Functional 4D Scene Graphs with Vision-Language Models for Interaction Understanding and Grounded Planning

- **분야**: Embodied AI · **robotics relevance**: 9/10
- **arXiv**: [2609.39665](https://arxiv.org/abs/2609.39665) ([PDF](https://arxiv.org/pdf/2609.39665))
- **저자**: Chenyangguang Zhang, Malgorzata Gwiazda, Guanlong Jiao, Yuanchen Ju, Federico Tombari, Koushil Sreenath, Marc Pollefeys, Sunghwan Hong
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **원문 검토**: PDF 전문 · 1차 스크리닝 65점

> 💡 과거 행동이 장면을 어떻게 바꿨는지 설명하는 4D interaction understanding과 다음에 어디를 어떻게 조작할지 정하는 spatially grounded planning을 같은 표현으로 묶는 functional 4D scene graph ChronoGraph를 제안함. graph-as-chain-of-thought SFT와 joint 4D graph RL로 학습한 ChronoGraphVLM이 자체 구축한 ChronoGraphBench에서 baseline 대비 overall 24pp 안팎 개선을 보이고, VLM4D zero-shot transfer와 실제 Spot 로봇 mobile manipulation 시연까지 이어짐.

**Core innovation & methodology**

- affordance part 단위 node와 action-conditioned state transition edge로 구성된 functional 4D scene graph를 정의해, 관찰된 변화와 예측될 변화를 같은 표현으로 서술함.
- HD-EPIC·HOI! 사람 영상과 RoboCasa 로봇 trajectory를 SAM3 segmentation·SAM-3D reconstruction·GPT-5.5 graph 생성으로 자동 annotate해 ChronoGraphBench(1,669개 interaction, 15,094개 QA)를 구축함.
- 1단계 Graph-as-Chain-of-Thought SFT로 graph-evidence-answer 순서의 구조적 reasoning을 학습시키고, 2단계 GRPO 기반 joint 4D graph RL로 graph 속성(soft F1, 3D center reward 등)과 답 정확도를 동시에 보상함.
- history-conditioned planning과 static-conditioned planning 두 세팅 모두 같은 graph 표현으로 처리하며, 2D/3D grounding을 answer reward에 포함시킴.

**Novelty vs. prior works**

- 가장 가까운 선행연구인 MomaGraph는 static scene을 text 형태 functional scene graph로 표현하는 데 그치는데, ChronoGraph는 affordance 단위 action-conditioned transition을 시간축으로 이어 이해와 계획을 같은 graph trace로 연결한 점이 본질적 차이임.
- 기존 4D VLM benchmark(VLM4D, MLLM-4D 등)는 object-level 동역학만 다루고 planning benchmark는 grounding을 거의 안 다루는데, 이 논문은 두 축을 하나의 representation으로 합쳐 interleave로 평가하는 benchmark를 제시함.
- 다만 핵심 novelty는 representation과 benchmark 설계에 있고, 학습 방식(CoT SFT 후 GRPO) 자체는 최근 reasoning VLM/LLM 연구에서 널리 쓰이는 패턴이라 학습 알고리즘 차원의 신규성은 제한적임.

**Benchmark results**

- ChronoGraphBench overall average에서 9B 모델이 baseline 51.2에서 75.2로 24.0pp, 4B 모델이 48.9에서 73.0으로 24.1pp 개선함.
- 상용 모델 중 가장 높은 GPT-6 Astra(overall 79.4)보다는 낮지만, 이 모델이 static-conditioned planning에서 state-change 96.6 대 spatial 69.2로 공간 추론만 약해 spatial grounding이 공통 약점임을 확인함.
- VLM4D zero-shot transfer에서 9B 67.1%, 4B 61.0%로 pretrained 대비 각각 6.6%p, 7.3%p 개선해 benchmark 특정 overfitting이 아님을 시사함.
- ablation에서 answer-only SFT는 ChronoGraphBench를 67.0까지 올리지만 VLM4D는 60.5%에서 49.4%로 떨어뜨리고, Graph-as-CoT SFT를 쓰면 69.9/64.2%로 둘 다 개선되어 graph 중간 supervision의 역할이 확인됨.
- 실로봇 검증은 Boston Dynamics Spot으로 3개 task(스위치 켜기, 캐비닛 열고 장난감 꺼내기, 서랍 열고 주전자 옮기기)의 정성적 시연에 그치고 정량 성공률은 본문에서 확인 불가함.

**Top-tier conference 적합성 — 74/100 · 추천 venue: ICLR**

representation·benchmark·학습 파이프라인을 한 번에 제시하고 zero-shot transfer까지 확인해 완성도가 높고, VLM 추론 능력을 다루는 venue와 잘 맞음. 다만 실로봇 결과가 정성적 시연 수준이고 static-conditioned planning의 spatial grounding 격차는 여전히 커 공간 추론의 핵심 약점이 완전히 해소되지 않았다는 점이 약점임.

**추천 이유 & 누리랩 연구와의 연결점**

- object-centric 4D representation·scene graph 우선주제와 직접 맞닿음. affordance part 단위로 action-conditioned transition을 쌓는 방식은 3DGS 기반 object-centric scene 표현에 시간축을 더하는 형태로 적용해볼 수 있음.
- world model·test-time planning 연구와 연결됨. graph trace로 미래 state를 먼저 예측하고 답을 내는 구조는 robot memory나 counterfactual reasoning에 쓸 예측-검증 틀로 재사용 가능함.
- failure detection 관점에서, 예측된 graph transition과 실제 관찰된 transition의 불일치를 action 실패 신호로 쓰는 방향을 추가 연구로 제안할 수 있음.

---

### 7. [74점] The Planning Limits of Latent World Models

- **분야**: World Model · **robotics relevance**: 10/10
- **arXiv**: [2609.39235](https://arxiv.org/abs/2609.39235) ([PDF](https://arxiv.org/pdf/2609.39235))
- **저자**: Ali Alrasheed, Basim Azam, Naveed Akhtar
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 latent world model이 planning에 쓸모 있는 범위가 학습된 rollout 길이 근처로 매우 짧다는 것을 다섯 개 frozen encoder와 Meta-World sim, BridgeData V2 offline 분석으로 체계적으로 입증함. rollout을 target까지 늘리면 범위가 확장되고, world model을 VLA policy와 결합하면 성공률을 65%에서 77%로 올릴 수 있음을 보임.

**Core innovation & methodology**

- plannable range라는 지표를 정의함: world model이 imagine한 trajectory가 expert action을 random action보다 높게 ranking하는 최대 target distance를 측정함
- V-JEPA 2, V-JEPA 2.1, VideoMAEv2, VideoPrism, DINOv2 다섯 개 frozen self-supervised encoder 위에 동일한 action-conditioned predictor를 올려 비교함
- predictor capacity(81배 확대), recursive training horizon, planning 시 rollout length K, encoder 네 요인을 하나씩 바꿔가며 원인을 분리함
- 실제 시뮬레이터를 perfect predictor로 대체해 prediction error와 target 위치 자체의 효과를 분리함

**Novelty vs. prior works**

- DINO-WM, TD-MPC2, V-JEPA 2 등 기존 latent world model 연구는 모델이 할 수 있는 것을 보여주는 데 집중했고, 이 논문은 실패 조건을 정량적으로 규명한 diagnostic 연구라는 점에서 기여가 있음
- 새로운 architecture나 representation을 제안하지 않고, 기존 frozen encoder와 predictor 조합에 대한 평가 프로토콜(plannable range)을 설계한 분석 논문임
- objective mismatch in model-based RL 연구(Lambert et al.)와 문제의식은 비슷하나, robot manipulation의 latent world model에 특화해 rollout length와 target distance의 관계를 정량화한 점이 차별점임. novelty는 새 방법이 아니라 새 평가 축 제시에 있음

**Benchmark results**

- 5-step rollout 기준 V-JEPA 2.1의 plannable range는 5~10 step인데, Meta-World 16개 task의 expert demonstration은 16~53 step(평균 약 33 step) 소요됨
- 완벽한 시뮬레이터를 predictor로 써도 target이 5 step에서 20 step으로 멀어지면 성공률이 92%에서 41%로 떨어져, 한계가 prediction error가 아니라 target 위치 자체에서 옴을 보임
- predictor 크기를 81배 키워도 plannable range는 늘지 않으나, rollout length를 20 step으로 늘리면 range가 최소 20 step까지 확장됨
- pure imagination은 23% 성공에 그치고, MPC feedback 추가 시 30%, target까지 imagine하면 47%, expert subgoal(5 step 앞)을 주면 76%까지 오름
- fine-tuned π0가 제안한 8개 action 후보를 V-JEPA 2.1로 재점수화하면 16개 task 성공률이 65%에서 77%로 오름(held-out near variant는 25%→49%, 새 물체·동작 task는 둘 다 10% 이하). 전부 Meta-World sim 기반이며, 실로봇 데이터는 BridgeData V2의 offline 분석(실제 control 아님)만 포함함

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

world model planning의 근본적 한계를 다섯 encoder와 perfect-simulator 대조실험으로 꼼꼼히 규명해 실험적 설득력이 강함. 다만 새로운 method나 architecture 제안이 없고 전부 Meta-World sim과 BridgeData V2 offline 분석이라 real-robot closed-loop 검증이 빠진 점이 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- 월드모델 test-time planning의 한계를 수치로 규명한 결과라, 누리랩의 test-time optimization·world model 연구에서 baseline 가정을 재점검할 근거로 쓸 수 있음
- subgoal 제공이 성공률을 가장 크게 올린다는 결과는 failure detection/recovery나 long-horizon manipulation에서 world model을 쓸 때 subgoal generation 모듈을 먼저 설계해야 함을 시사함
- VLA proposal을 world model로 재점수화하는 VLA-WM 조합은 누리랩의 VLA+world model 결합 연구에 바로 적용 가능한 inference-time verifier 구조임

---

### 8. [73점] RoboCoach: World Models as Active Coaches for Compositional Robot Skills

- **분야**: World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.39685](https://arxiv.org/abs/2609.39685) ([PDF](https://arxiv.org/pdf/2609.39685))
- **저자**: Jiajun Liu, Yifan Chen, Yichao Liu, Jiayi Zhang, Ruoqu Chen, Shaoxuan Xie, Guocai Yao, Mengdi Xu 외 2명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 64점

> 💡 world model(CoachWorld) 안에서 로봇 정책 실행을 상상해 어느 subtask가 반복적으로 실패하는지 찾아내고, 그 subtask를 담당하는 skill expert(LoRA adapter)에만 추가 demonstration을 배정해 업데이트하는 RoboCoach를 제안함. 150개의 추가 subtask demonstration만으로 Franka 성공률이 13.3%에서 75.0%로, AgileX가 40.0%에서 83.8%로 올라감.

**Core innovation & methodology**

- Route-Imagine-Diagnose-Improve(RIDI) loop: router가 다음 미완료 subtask를 고름. 해당 skill expert를 CoachWorld 안에서 closed-loop 실행하고 progress judge(RoboMeter)가 처음 실패하는 subtask를 기록함.
- CoachWorld는 Ctrl-World 기반 action-conditioned world model로, 2-slot end-effector 궤적과 camera calibration(PRoPE)을 조건으로 여러 embodiment의 multi-view 미래 영상을 flow matching으로 예측함.
- subtask-expert pair를 데이터 수집과 adaptation의 공통 단위로 삼아, task-balanced first-timeout mass(task별로 처음 실패가 발생하는 빈도를 균형 있게 반영한 지표)로 상위 M=2개 pair를 뽑아 demonstration을 요청하고 해당 LoRA adapter만 업데이트함(backbone·다른 adapter는 고정).
- 공유 VLA backbone(π0.5/MolmoAct2) 위에 skill별 LoRA expert를 두는 modular 구조라, 무엇을 가르칠지와 어느 컴포넌트를 업데이트할지를 하나의 결정으로 묶음.

**Novelty vs. prior works**

- world model을 policy 평가·최적화 도구로 쓰는 선행연구(WorldEval, WMPO류)와 달리, RoboCoach는 world model을 어느 subtask-expert 조합에 데이터를 투입할지 결정하는 active coaching 역할로 사용함.
- active/corrective imitation learning(HG-DAgger류)과 달리 실로봇 rollout이 아니라 world model 상상 rollout으로 bottleneck을 찾고, 이를 modular skill expert 구조와 결합함.
- 다만 world model(Ctrl-World 확장), progress judge(RoboMeter 재사용), LoRA expert 구조는 각각 기존 요소이고 contribution은 이들을 잇는 시스템 설계(RIDI loop)에 있어, 단일 알고리즘적 breakthrough보다 시스템 통합 novelty에 가까움.

**Benchmark results**

- 22개 task-policy pair에서 imagined-deployed 성공률 상관 Spearman ρ=0.840, Pearson r=0.820으로 world model 신뢰성을 뒷받침함.
- 실로봇 150개 추가 demonstration 투입 후 Franka 13.3%→75.0%, AgileX 40.0%→83.8%, 동일 budget의 Single VLA + Uniform baseline은 각 30.0%, 47.5%에 그침(Budget AUC 53.1 vs 18.9, 72.7 vs 46.3).
- 시뮬레이션(LIBERO-Long 10개, RoboTwin2.0 5개 task)에서 RoboCoach가 각 71.2%, 68.0%로 비교된 4개 조건 중 최고 성능.
- ablation상 동일 targeted demonstration이라도 shared adapter 대신 해당 expert를 업데이트하면 LIBERO +3.4%p, RoboTwin +13.2%p 개선되고, world-model targeting이 random targeting보다 +2.8%p, +12.8%p 우위.
- held-out composition 4종(real robot, route당 20 trial) 평균 성공률 35.0% vs baseline 0%, 다만 case별 편차가 커서 cross-task composition(Franka)은 15%(3/20)에 불과함.

**Top-tier conference 적합성 — 76/100 · 추천 venue: CoRL**

world model-deployed 상관 분석, acquisition·update 축을 분리한 controlled ablation, 두 실로봇 플랫폼 검증까지 갖춰 empirical conviction이 강함. 다만 핵심 구성요소(world model, progress judge, LoRA expert)가 각각 기존 기법의 재사용이라 알고리즘적 novelty는 제한적이고, held-out composition 성공률 편차(최저 15%, 평균 35.0%)가 일반화 한계로 지적될 만함.

**추천 이유 & 누리랩 연구와의 연결점**

- progress judge가 첫 실패 subtask를 식별하는 방식은 누리랩의 failure detection·diagnosis 연구에 그대로 참고할 수 있음.
- world model을 데이터 수집 우선순위 결정에 쓰는 아이디어는 test-time optimization과 robot memory(반복 실패 subtask 기록) 연구에 접목 가능함.
- held-out composition 평가 프로토콜은 누리랩의 skill chaining·long-horizon generalization 연구에서 평가 설계 참고 자료로 쓸 만함.

---

### 9. [73점] Text-to-3D Policy: Fine-Grained Language-Behavior Alignment for Unseen Specification Generalization

- **분야**: VLA · **robotics relevance**: 9/10
- **arXiv**: [2609.39599](https://arxiv.org/abs/2609.39599) ([PDF](https://arxiv.org/pdf/2609.39599))
- **저자**: Xinhao Yang, Wenhao Wu, Ning Lv, Yanshen Ding, Zhenhong Sun, Daoyi Dong, Chunlin Chen, Zhi Wang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 24 pages, 8 figures, 8 table
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 같은 task 안에서도 목표 위치·변위 같은 세부 언어 사양이 학습 때 못 본 값이면 3D policy가 구분 못하는 문제를 unseen specification generalization으로 정의하고, instruction token과 behavior segment를 양방향으로 대응시키는 fine-grained alignment로 해결함. Meta-World·ManiSkill에서 global alignment 대비 13.5~14.2%p, real robot에서는 47.5%에서 65.0%로 성공률을 높임.

**Core innovation & methodology**

- 같은 task family 안에서 언어가 지정하는 세부 행동 사양(목표 위치, 변위, articulation 상태)이 학습 데이터에 없을 때의 일반화를 unseen specification generalization으로 새로 정의함
- 예비 실험으로 generic language representation과 global language-behavior alignment가 coarse task semantics만 포착하고 비슷한 사양을 구분하지 못함을 확인함
- demonstration을 reward-prediction objective로 학습한 behavior encoder에서 specification-dependent 표현을 얻고, instruction token과 state-action hidden state 사이 양방향 token-level contrastive alignment로 text encoder를 LoRA fine-tune함
- aligned text encoder의 pooled embedding을 조건으로 point-cloud 기반 3D diffusion policy(DP3 구조)를 학습해, 정책 구조 변경 없이 specification-sensitive 조건만 교체함

**Novelty vs. prior works**

- 가장 가까운 prior work T2DA는 trajectory 전체를 하나의 global embedding으로 압축해 비슷한 사양을 뭉개버리는 반면, T3DP는 token-to-segment 양방향 대응으로 이를 직접 해결함
- token-level fine-grained alignment 자체는 FILIP·FG-CLIP 같은 vision-language 문헌의 기법을 robot behavior 도메인에 옮긴 조합형 기여로, alignment objective 자체가 새로운 것은 아님
- unseen specification generalization이라는 문제 정의는 ARNOLD의 continuous goal state 일반화와 개념적으로 겹치는 부분이 있어, spatial displacement·target까지 범위를 넓힌 확장으로 보는 것이 정확함

**Benchmark results**

- Meta-World 5개 task family 평균 50.3%로 global alignment 방식 T2DA(36.1%) 대비 14.2%p, DP3(16.2%) 대비 34.1%p 높음
- ManiSkill 5개 task family 평균 54.2%로 T2DA(40.7%) 대비 13.5%p 높고, Pick Cube에서 77.7% vs 3DDA 8.3%, 3D-LOTUS 0.0%로 격차가 큼
- real robot(PiperX arm, 2개 task family, 각 20개 사양) 평균 성공률이 47.5%에서 65.0%로 17.5%p 상승함
- 계층적 ablation에서 language 조건만 추가 시 16.2%→19.1%, global alignment 추가 시 36.1%, fine-grained alignment 추가 시 50.3%로 단계별 기여가 뚜렷함
- 학습 사양 수를 10→40개로 늘려도 T3DP가 T2DA 대비 우위를 유지함(10개: 32.4% vs 23.9%, 40개: 76.4% vs 69.2%)

**Top-tier conference 적합성 — 72/100 · 추천 venue: CoRL**

unseen specification generalization이라는 명확한 문제 정의와 3개 simulation benchmark·real robot 전반의 일관된 성능 향상이 강점임. 다만 fine-grained alignment 메커니즘 자체는 vision-language 분야의 token-level contrastive 기법을 robot behavior에 옮긴 조합형 기여라, reject 위험은 novelty보다 기존 CLIP류 alignment 대비 증분성 비판에서 올 가능성이 큼.

**추천 이유 & 누리랩 연구와의 연결점**

- VLA의 language-behavior alignment 문제와 직결되며, token-level grounding을 scene graph나 object-centric representation과 결합해 '어떤 물체의 어떤 부분을 어떻게'까지 세분화하는 연구로 확장 가능함
- reward-predictive behavior encoder는 test-time verifier나 energy function으로 재사용할 수 있어, 같은 배치의 TeV 논문(temporal verification)과 결합하는 아이디어가 가능함
- held-out specification 평가 프로토콜을 '다른 사양이었다면 성공했을지'를 묻는 counterfactual reasoning 평가로 확장해 실패 진단 연구에 쓸 수 있음

---

### 10. [72점] Correcting WHERE, Preserving HOW: Compositional Generalization for Vision-Language-Action Models via Referential Guidance

- **분야**: VLA · **robotics relevance**: 9/10
- **arXiv**: [2609.38616](https://arxiv.org/abs/2609.38616) ([PDF](https://arxiv.org/pdf/2609.38616))
- **저자**: Yanyan Zhang, Disheng Liu, Xinpeng Li, Chaoda Song, Mohsen Hariri, Debargha Ganguly, Wang Yang, Kai Ye 외 3명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 66점

> 💡 VLA가 훈련 때 못 본 object·destination 조합을 만나면 global grounding만 틀리고 local manipulation 능력은 남아 있다는 관찰에서 출발함. ReGuide라는 training-free wrapper로 instructed referent를 다시 찾아 end-effector를 demonstration 기반 영역으로 옮긴 뒤 frozen policy를 재개시켜 LIBERO에서 최대 56.8%p, 실로봇 xArm6에서 75.0%p 성공률을 높임.

**Core innovation & methodology**

- VLA가 재조합 상황에서 보이는 실패는 referent를 통째로 잘못 묶는 global grounding 오류이고, 일단 올바른 위치에 도달하면 local manipulation 능력(how)은 그대로 쓸 수 있다는 관찰에서 출발함.
- semantic rebinding은 grounding module이 준 object pose로 policy가 향하는 referent(남은 action chunk의 예측 끝점)를 추정해 instructed referent와 어긋나는지를 외부 scorer 없이 판정함.
- geometric rebinding은 demonstration에서 뽑은 quantile 기반 pre-contact set(목표 pose, 접근 허용범위)으로 end-effector를 bounded flow로 옮기고, 이 영역에 들어오면 frozen policy를 그대로 재개함.
- 전체가 policy를 재학습하지 않는 wrapper라 π0.5, OpenVLA-OFT, GR00T N1.7 등 여러 backbone에 그대로 씌울 수 있음.

**Novelty vs. prior works**

- 기존 연구는 data recombination(재조합 데이터 수집), architecture 수정(target cue 주입 후 재학습), inference-time steering(action distribution 재가중 또는 외부 oracle·scorer)으로 나뉘는데 셋 다 재학습이 필요하거나 policy가 이미 제안한 것만 재가중함.
- ReGuide는 policy를 전혀 건드리지 않고 end-effector를 policy가 고려하지 않은 referent 위치로 직접 옮긴다는 점에서 reweighting이 아니라 rebinding이라는 차별점이 있음.
- 다만 방법 자체는 quantile 기반 threshold·canonical frame·다단계 gating으로 구성된 수작업 파이프라인이라, novelty는 문제 재정의와 test-time rebinding이라는 틀에 있지 representation·learning paradigm 자체의 새로움은 제한적임.

**Benchmark results**

- LIBERO 16개 조합 셀에서 π0.5 기준 Comp. Avg.를 39.0%에서 94.5%로(55.5pp) 올리고, Orig.(원래 과제) 성능은 94.0%에서 94.2%로 거의 유지함. 다른 두 backbone(X-VLA, CAG)까지 포함하면 최대 56.8pp 개선임
- CAG(π0.5 기반 baseline)는 Comp. Avg.를 39.0에서 41.4로만 올리고 Orig.를 94.0에서 81.4로 떨어뜨려, 개선폭과 원래 과제 보존 둘 다 ReGuide에 크게 밀림.
- 실로봇 xArm6에서 bare π0.5의 Comp. 성공률 15.0%를 90.0%로 올리고 Orig.도 86.0%에서 92.0%로 개선함, 다만 전체 150 paired trial로 규모는 크지 않음.
- ablation에서 pre-contact set을 빼면 800건 중 들고 있는 물체 유지가 789건에서 708건으로, competing referent 비교를 빼면 destination 도달이 785건에서 737건으로 줄어 두 구성요소가 서로 다른 실패를 막음이 확인됨.
- grounding을 oracle이 아닌 실제 perception 기반으로 바꾸면 π0.5 기준 87.5%로 오라클 대비 7.0pp 낮아져, 실제 배포 시 grounding 오차가 성능에 그대로 반영됨.

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

실로봇 검증과 여러 backbone에 대한 일관된 대폭 개선, 꼼꼼한 component ablation으로 empirical conviction이 강함. 다만 방법이 quantile 기반 수작업 파이프라인이라 학습 기반 일반 원리를 제시하는 논문보다 엔지니어링 기여로 읽힐 위험이 있고, grounding module 품질에 성능이 크게 의존하는 점이 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- failure detection/recovery 주제와 바로 연결됨. semantic rebinding의 referent mismatch 탐지 로직은 action chunk 예측만으로 VLA가 틀린 target으로 가는 것을 잡아내는 가벼운 진단 신호로 재사용 가능함.
- test-time optimization 주제와 연결됨. 재학습 없이 frozen policy를 외부 신호로 교정하는 방식은 다른 실패 모드(잘못된 grasp pose, 장애물 회피 등)에도 같은 틀로 확장해볼 만함.
- object-centric 3D representation·scene graph 연구에 grounding module 대체재로 결합할 수 있으나, demonstration 기반 quantile 통계 의존성을 줄이는 쪽이 더 일반화된 기여가 될 것으로 보임.

---

### 11. [72점] Asking the World: Generalist Physical Reasoning through Agentic World Modeling and Probing

- **분야**: World Model · **robotics relevance**: 7/10
- **arXiv**: [2609.39135](https://arxiv.org/abs/2609.39135) ([PDF](https://arxiv.org/pdf/2609.39135))
- **저자**: Shenxiang Zeng, Chen Yang, Peiyao Chen, Guohui Zhang, Jiansheng Fan, Chen Wang
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: 21 pages, 9 figures, 6 tables
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 비디오에서 질문에 필요한 만큼만 executable world를 구성하고, 그 world에 질의·시뮬레이션·개입을 가해 증거를 얻는 agentic 구조인 Asking the World(ATW)를 제안함. Warp 기반 멀티피직스 엔진 PolyWorld와 CEM system identification을 결합해 CLEVRER·ContPhy·real-world 3개 시나리오에서 기존 VLM과 training-free baseline을 큰 폭으로 앞섬.

**Core innovation & methodology**

- World Modeling(세계 구성)과 World Probing(질문 지향 실험)의 2단계 agentic 구조로 물리 추론을 formulation함. 둘 다 operation을 미리 정하지 않고 scene·question에 따라 agent가 결정함
- PolyWorld Engine(Warp 기반)이 rigid body·soft body·cloth·rope·fluid와 그 coupled interaction을 하나의 executable scene에서 다룸
- World Modeling에서 CEM으로 trajectory discrepancy를 최소화해 동역학 파라미터를 추정하고, 불일치 시 representation·object binding 자체를 수정함
- 커밋된 world는 probing 단계에서 destructively 수정되지 않고 branch로 분기되어, 여러 질문이 같은 calibrated world를 공유하면서 counterfactual 개입이 가능함

**Novelty vs. prior works**

- PhysGaussian·PAC-NeRF 등 기존 video-to-simulation 방법은 고정된 representation·material family를 가정하는데, ATW는 어떤 physical model을 쓸지 question-conditioned로 agent가 결정함
- 가장 가까운 prior work인 PhysMind(동일 저자 그룹 선행연구)는 executable world를 미리 정해진 downstream tool로 쓰는데, ATW는 world를 probing 단계에서 branch·intervene 가능한 지속 workspace로 바꾼 점이 핵심 차별점임
- agent+simulator 결합이라는 틀 자체(LLMPhy, ViperGPT 계열)는 선행연구의 연장선이라, formulation의 참신성은 2단계 분리와 멀티피직스 통합에 집중되어 있고 완전히 새로운 패러다임은 아님

**Benchmark results**

- CLEVRER validation 1,000 videos에서 overall per-question accuracy 80.82%로 Gemini-3-Flash 대비 +46.50%p, GPT-5.5 대비 +13.58%p, 가장 강한 training-free baseline PhysMind 대비 +8.27%p
- ContPhy 600 videos/1,950 questions에서 overall 70.56%로 Gemini-3-Flash 대비 +28.10%p, GPT-5.5 대비 +3.53%p. 단 counterfactual 항목은 GPT-5.5보다 6.46%p 낮음
- real-world 3개 시나리오(billiards counterfactual, bouncing-ball·toy-car prediction) 총 60개 video/question에서 overall 71.67%로 GPT-5.5(43.33%)를 크게 앞섬. 다만 시나리오가 3개뿐이고 실제 로봇 조작이 아닌 video QA에 한정됨
- ablation(CLEVRER 100-scene subset 기준, 전체 validation 수치 80.82%와는 표본이 다름)에서 Video-only VLM→Perception-only→Single-pass World Model→Full ATW 순으로 35.40%→42.07%→75.40%→82.30%로 상승해, world 실행과 feedback-guided revision의 기여가 perception 추가보다 훨씬 큼
- system identification/backend ablation(별도 CLEVRER subset 기준)에서 CEM이 Random Search 대비 median trajectory RMSE를 낮추고 per-question accuracy를 43.45%→82.76%로 올렸으며, Warp 백엔드가 MuJoCo·PhysMind 물리모델보다 낮은 오차와 높은 accuracy를 보임

**Top-tier conference 적합성 — 68/100 · 추천 venue: ICLR**

통일된 멀티피직스 엔진과 agentic formulation을 2개 벤치마크와 3개 real-world 시나리오에서 폭넓게 검증한 실험적 설득력이 강함. 다만 Gemini-3-Flash·GPT-5.5 등 비공개 모델에 의존하고 PolyWorld·코드 공개 여부가 본문에서 확인 불가하며, 실제 로봇 조작이 아닌 video QA에 머물러 embodied 검증 부족이 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- PolyWorld Engine과 CEM system identification 구조는 누리랩의 world model·test-time optimization 연구에서, manipulation policy의 inference-time에 agentic probing을 이식하는 아이디어로 연결됨
- World Modeling의 mismatch 발견 시 representation을 revise하는 루프는 실로봇 failure detection·diagnosis 파이프라인에 적용 가능한 패턴임
- counterfactual branch 개입과 object-centric 물리 표현의 결합은 scene graph·3DGS 연구와 묶어 manipulation 중 what-if 질의로 확장할 여지가 있음

---

### 12. [70점] GroundingPI: A Grounding Foundation Model towards Physical Intelligence with Visual Primitives

- **분야**: VLA · **robotics relevance**: 8/10
- **arXiv**: [2609.39601](https://arxiv.org/abs/2609.39601) ([PDF](https://arxiv.org/pdf/2609.39601))
- **저자**: Qize Yu, Lianrui Fan, Boyu Chen, Jiaqi Liang, Xini Ding, Yue Chen, Zetian Song, Yuran Wang 외 18명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: 64 pages, including supplementary material. Project page: this https URL Code: this https URL Model: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 VLA와 world-action model이 범용 vision-language 또는 video generation backbone을 써서 정밀한 grounding에 약하다는 문제를, point/box를 quantized coordinate token으로 생성하는 4B 크기 전용 foundation model GroundingPI로 해결함. 34개 grounding benchmark에서 44개 baseline(GPT-6 Astra 포함)을 평균 73.68%로 앞서고, 이를 동일한 Action DiT에 꽂아 RoboTwin2.0·RoboCasa-GR1 manipulation과 nuScenes 자율주행 전이 실험에서도 다른 backbone보다 나은 성능을 보임.

**Core innovation & methodology**

- VLA/world-action model이 general-purpose vision-language 또는 video generation backbone에서 perception을 가져와 dense clutter·tiny object 같은 정밀 grounding 상황에서 약하다는 bottleneck을 지적함
- point와 box를 quantized coordinate token으로 표현하는 공유 vocabulary로 grounding·referring·pointing·OCR·GUI·layout grounding을 하나의 autoregressive 생성 문제로 통일한 4B 모델 GroundingPI를 제안함
- multimodal·spatial pretraining, supervised fine-tuning, GRPO 기반 강화학습(coverage reward와 localization reward 결합)의 3단계 학습 recipe를 적용함
- 동일한 Action DiT에 VLM·video generation·grounding·embodied foundation 4개 계열 backbone을 번갈아 꽂는 controlled comparison으로 grounding 성능이 action learning에 전이되는지 체계적으로 검증함

**Novelty vs. prior works**

- quantized coordinate vocabulary, GRPO 기반 RL, VLA backbone 비교 같은 개별 요소는 Rex-Omni·LocateAnything·π0.5 등 기존 연구에서 이미 쓰인 기법이라 방법론 자체의 신규성은 제한적임
- 본질적 기여는 'perception을 먼저 scale-up하고 action은 나중에'라는 설계 철학을 44개 baseline·34개 benchmark·4개 backbone 계열에 걸친 대규모 통제 실험으로 체계적으로 검증한 실증 연구에 가까움
- OCR이 perceptual learning의 촉매가 될 수 있다는 data recipe 분석은 흥미로운 관찰이지만, 해당 ablation의 구체 수치는 제공된 본문 구간에서 확인 불가함

**Benchmark results**

- 34개 grounding benchmark 평균 73.68%로 44개 baseline 중 최고이며 GPT-6 Astra(71.54%)보다 높음, Dense200에서는 74.53으로 Astra(65.04)·Qwen3-VL-4B(14.02) 대비 크게 앞섬
- object pointing(F1@Point) 7개 column 중 6개에서 1위, HumanRef 88.79 vs Astra 83.83
- RoboTwin2.0 4개 OOD 세팅 전부 1위이며 최강 baseline 대비 최대 24.8% 상대 개선(Clean2Random 17.60% vs Rex-Omni 14.10%), Full 세팅은 66.20%
- RoboCasa-GR1은 Type OOD에서 1위(28.94%)이지만 Full 세팅에서는 RynnBrain(39.00%)에 이어 2위(37.75%)로 전 세팅 1위는 아님
- nuScenes open-loop L2 오차 평균 0.296m로 Qwen3-VL-4B(0.301m)보다 근소히 우수하나 closed-loop 성능은 미검증임
- abstract에서 주장한 50% demonstration으로 75% 학습 baseline을 능가한다는 결과의 구체 수치는 본문에서 확인 불가함

**Top-tier conference 적합성 — 68/100 · 추천 venue: CVPR**

34개 benchmark·44개 baseline에 걸친 광범위한 실증과 driving·manipulation 전이까지 보여준 실험 규모가 강점임. 다만 핵심 기법 요소가 기존 grounding·RL 기법의 조합이고 action 전이 검증이 open-loop 위주라, conceptual novelty와 closed-loop 실증 부족이 rejection 위험임.

**추천 이유 & 누리랩 연구와의 연결점**

- dense grounding과 tiny object 탐지 능력이 강해, scene graph 구축이나 object-centric 3DGS의 perception frontend로 재사용할 수 있음
- VLA perception bottleneck 해결 사례로서, 우리 랩의 failure detection 연구에서 실패가 perception 오류인지 policy 오류인지 구분하는 진단 도구로 활용 가능함
- Action DiT를 고정하고 backbone만 교체하는 controlled comparison 프로토콜은 우리 랩이 자체 perception·world model 모듈을 검증할 때 그대로 차용할 수 있는 실험 설계임

---

### 13. [68점] Looking Back to Move Forward: Temporal Verification for Generative Robot Policies

- **분야**: VLA · **robotics relevance**: 9/10
- **arXiv**: [2609.39038](https://arxiv.org/abs/2609.39038) ([PDF](https://arxiv.org/pdf/2609.39038))
- **저자**: Haoxuan Wang, Wayne Wu, Yan Yan, Bolei Zhou
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Project page at this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 flow-matching 기반 VLA의 action verification이 현재 관측만 보고 평가해 trajectory 연속성을 놓치는 문제를 temporal token과 energy-based verifier로 해결함. 최근 observation-action history를 조건으로 candidate action chunk를 순위 매기고 flow sampling 과정 자체도 energy gradient로 유도해서, LIBERO-Plus와 RoboTwin2.0에서 각각 최강 baseline 대비 3.8%p, 6.4%p 성공률을 높이고 real-world 과제에서도 더 매끄러운 trajectory를 만듦.

**Core innovation & methodology**

- flow-matching VLA의 action verification이 현재 관측에만 의존해 trajectory 연속성을 반영하지 못하는 문제를 지적함
- 최근 observation-action history를 causal transformer로 압축한 temporal token을 학습하고, future-action prediction objective로 이 token이 실행 맥락을 보존하도록 regularize함
- temporal token에 조건화한 lightweight energy-based verifier를 expert chunk(positive)와 temporal-mismatch·coarse-integration negative로 contrastive하게 학습함
- 학습된 energy function의 gradient로 flow matching 중간 샘플을 직접 steering해서, post-hoc ranking뿐 아니라 generation 과정 자체를 개선함

**Novelty vs. prior works**

- 가장 가까운 prior work인 TACO는 pseudo-count 기반으로 static한 현재 관측만 평가하는 반면, TeV는 temporal token으로 trajectory 연속성을 명시적으로 모델링함
- BID·Temporal Ensembling 같은 기존 temporal consistency 방법은 단순 averaging이나 유사도 기반 smoothing에 그치지만, TeV는 학습된 energy function으로 품질과 시간적 일관성을 함께 평가함
- 다만 핵심 아이디어인 energy-based guidance와 contrastive verifier 학습은 diffusion guidance·policy steering 문헌의 조합에 가까워 완전히 새로운 패러다임은 아니며, 조합의 실효성을 입증한 것이 기여의 핵심임

**Benchmark results**

- LIBERO-Plus 중 가장 어려운 LIBERO10 suite(2,519개 task instance), π0.5 backbone, M=4 candidate 기준 TeV 평균 79.8%로 TACO(76.0%), BID(72.2%), base(73.2%) 대비 최강 baseline보다 3.8%p 높음
- RoboTwin2.0 7개 task(50 demo/task, 100 trial) 평균 81.3%로 BID(74.9%)보다 6.4%p 높고, TACO는 오히려 70.0%로 base보다 낮음
- real robot 3개 task(30 trial)에서 전 task 개선, Water Filling은 40.5%에서 68.0%로 27.5%p 상승함
- negative 조합 ablation에서 coarse-integration만 78.1%, temporal-mismatch만 77.4%, 둘 다 사용 시 81.3%로 상호 보완적임을 확인함
- candidate 수 M을 늘려도 성능이 단조 증가하지 않고 M=16에서 오히려 하락해, verifier 품질이 병목임을 시사함

**Top-tier conference 적합성 — 65/100 · 추천 venue: CoRL**

sim과 real robot 양쪽에서 일관된 성능 개선과 0.15% 미만의 파라미터 증가라는 가벼운 overhead가 강점임. 다만 핵심 메커니즘이 기존 test-time verification과 diffusion guidance 기법의 조합이라 conceptual novelty가 제한적이고, real-world 검증이 3개 task에 그쳐 rejection 위험이 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- energy function이 action quality를 암묵적으로 점수화하므로, energy 급상승을 failure 조짐으로 보는 failure detection trigger로 확장 가능함
- temporal token이 사실상 short-horizon robot memory 역할을 하므로, 장기 memory 모듈(MEM 등)과 결합해 더 긴 horizon의 failure recovery 연구로 확장할 수 있음
- test-time optimization/inference-time planning 주제에 바로 결합 가능한 가벼운 add-on이라, 우리 랩의 test-time 연구에서 baseline이나 구성 요소로 활용할 수 있음

---

### 14. [63점] PneuTac: Tactile Manipulation with Soft Pneumatic Robots via Unified MPM-Gaussian Splatting Simulation

- **분야**: Manipulation · **robotics relevance**: 9/10
- **arXiv**: [2609.38418](https://arxiv.org/abs/2609.38418) ([PDF](https://arxiv.org/pdf/2609.38418))
- **저자**: Shaohong Zhong, Marco Pontin, Joe Watson, Perla Maiolino, Ingmar Posner
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 66점

> 💡 소프트 공압 로봇과 vision-based tactile sensor(Digit)를 material point method(MPM)로 동역학을, 3D Gaussian Splatting(3DGS)으로 렌더링을 결합해 하나의 시뮬레이터(PneuTac)로 동시에 모델링함. 단일 이미지만으로 real-to-sim calibration을 수행하고 이 시뮬레이터로 증강한 demonstration으로 학습한 policy가 동일한 양의 real data만 쓴 baseline보다 3개의 contact-rich manipulation task에서 높은 성공률을 보임.

**Core innovation & methodology**

- soft pneumatic robot과 vision-based tactile sensor(gel)를 모두 MPM particle로 표현하고 3DGS 렌더링을 결합한 단일 시뮬레이터를 제안함. 기존 연구는 둘을 분리 모델링함
- CAD mesh에서 particle을 샘플링하고 로봇은 crop 이미지 1장, tactile gel은 indentation 이미지 1장만으로 vision-based real-to-sim calibration을 수행함
- 전체 MPM 연산 대신 residual torque MLP(action network)와 indentation 매핑 UNet(perception network)이라는 surrogate 모델로 각각 5배, 3000배 속도를 높임
- real demonstration을 웜스타트로 쓰는 CEM 기반 MPC가 tactile 접촉 영역 신호를 guidance로 사용해 시뮬레이션에서 demonstration을 증강함

**Novelty vs. prior works**

- 가장 가까운 prior work인 PhysGaussian·PhysTwin은 천·로프 같은 passive deformable object에 MPM-3DGS를 적용했는데, PneuTac은 이를 actuated soft robot과 접촉 tactile sensing에 처음 결합함
- DiffTactile·Tacchi·DOT-Sim 등 tactile simulator는 rigid robot과의 결합만 다뤄 soft robot에 부착된 센서는 다루지 못하는데, PneuTac은 두 compliant 장치를 동시에 다룸
- 다만 MPM-3DGS 결합, CEM system identification, surrogate network는 모두 기존 기법의 조합이라 formulation 차원의 새로움은 제한적이고, 기여는 두 compliant 장치의 joint simulation이라는 engineering integration에 가까움

**Benchmark results**

- held-out pressure 지점에서 soft finger tip tracking error 4.2±0.4mm(손가락 길이 대비 4% 미만), soft arm 4.9±1.0mm(4.2%)로 marker ground-truth와 비교함
- tactile rendering에서 RMSE 10.18, PSNR 28.11dB, NCC 0.982로 Tacchi·DOT-Sim·Taxim 대비 전 지표에서 우위를 보이나, Tacchi와의 RMSE 격차는 10.18 대 10.86으로 크지 않음
- 다른 Digit sensor로 cross-device 평가 시 RMSE 8.12로 원 센서와 유사하나, 원래 calibration을 그대로 재사용하면 RMSE 22.96으로 device 간 차이가 큼을 보임
- 3개 실로봇 contact-rich task(switch flipping, egg carton opening, card pulling)에서 Sim+Real이 Real-only 대비 성공률을 switch 60.0%→83.3%, egg 26.7%→90.0%, card 33.3%→66.7%로 올림. 단 seed 3개, task당 trial 10개로 표본이 작고 soft finger 플랫폼 1종에 국한됨
- naive augmentation(N-Aug)도 Real 대비 개선되지만 Sim+Real에는 못 미치고, tactile 제거(No-Tac) 비교에서 switch·egg에서는 tactile 기여가 크나 card pulling에서는 차이가 작아 task 의존적임

**Top-tier conference 적합성 — 58/100 · 추천 venue: ICRA**

단일 이미지 기반 real-to-sim calibration의 실용성과 cross-device 검증이 강점이나, 소프트 손가락 플랫폼 1종·3개 task·task당 평가 trial 10개 규모의 소규모 실험이라 일반화 주장이 제한적임. 다른 시뮬레이터와의 policy 성능 직접 비교가 없다는 점도 저자 스스로 인정한 약점이라 RSS·CoRL보다는 ICRA/IROS급 contribution으로 보임.

**추천 이유 & 누리랩 연구와의 연결점**

- MPM-3DGS로 soft body와 tactile sensor를 동시에 시뮬레이션하는 구조는 누리랩의 tactile perception·manipulation 연구에서 시뮬레이션 기반 policy 학습에 참고할 수 있음
- CEM 기반 tactile-guided demonstration augmentation 파이프라인은 적은 real demonstration으로 시뮬레이션을 증강하는 방식이라 test-time optimization·data-efficient imitation learning 연구에 적용 가능함
- object-centric 3DGS 연구와 연결해 compliant contact를 포함하는 scene representation으로 확장하면 tactile feedback 기반 world model 연구로 이어질 수 있음

---

### 15. [62점] Function beyond Form: Functional Correspondence for Cross-Embodiment Dexterous Grasp Generation

- **분야**: Manipulation · **robotics relevance**: 9/10
- **arXiv**: [2609.39006](https://arxiv.org/abs/2609.39006) ([PDF](https://arxiv.org/pdf/2609.39006))
- **저자**: Bolin Zou, Wenlong Dong, Mu Ai, Chao Tang, Aoxiang Gu, Lipeng Chen, Hong Zhang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 64점

> 💡 손마다 다른 손가락 부위를 grasping 역할 기준으로 공통 기능 부위(wrist·metacarpal·proximal·middle·distal·tip)에 매핑하고 canonical local frame으로 정렬한 뒤, 그 위에서 diffusion model로 grasp를 생성하는 FunCo-Grasp를 제안함. 추가 데이터나 fine-tuning 없이 미지의 손 4종에서 시뮬레이션 평균 74.02%, 실로봇 미지의 손 2종에서 76.00% 성공률을 보임.

**Core innovation & methodology**

- Functional Part Alignment(FPA)로 서로 다른 손의 물리적 link를 grasping 역할에 따라 공유된 기능 부위(wrist/metacarpal/proximal/middle/distal/tip)로 매핑함.
- Canonical Frame Alignment(CFA)로 각 기능 부위를 forward·closing·lateral 축을 가진 canonical local frame으로 표현해 손 간 좌표계를 통일함.
- MAF graph encoder가 이 정렬된 hand graph에서 node/edge feature를 만들고, diffusion model이 object patch feature를 조건으로 기능 부위들의 목표 배치를 생성한 뒤 inverse kinematics로 실행 가능한 joint configuration으로 변환함.
- 미지의 손 적용에는 URDF·기구학 모델과 1회성 functional annotation만 필요하며 target-hand grasp data, fine-tuning, learned retargeting이 불필요함.

**Novelty vs. prior works**

- 가장 가까운 interaction-centric 선행연구(D(R,O)Grasp, T(R,O)Grasp)는 hand-specific link나 local frame으로 interaction을 정의해 구조가 다른 손 사이 대응이 모호했는데, FunCo-Grasp는 기능적 역할 기준의 명시적 대응을 도입함.
- morphology-alignment 계열인 UniMorphGrasp은 joint slot을 canonical하게 매핑하는 수준인 반면, FunCo-Grasp는 part 단위로 inter-part·hand-object interaction 전체를 정렬함.
- 다만 이는 기존 hand-centric/object-centric/interaction-centric 분류 안에서 interaction-centric 표현을 정교화한 확장이라, 완전히 새로운 problem formulation이라기보다 점진적 novelty에 가까움.

**Benchmark results**

- Seen hands(Shadow/Allegro/Barrett) 평균 성공률 92.40%로 baseline T(R,O)Grasp 91.07%, D(R,O)Grasp 85.33%보다 높음(시뮬레이션, CMapDataset 48 train/10 held-out objects).
- Unseen hands(ApexHand/XHand/LeapHand/Robotiq-3F) 평균 74.02%로 CEDex 66.50%, D(R,O)Grasp 38.13%, T(R,O)Grasp 11.95% 대비 크게 앞섬.
- 실로봇(ApexHand·Revo2, 둘 다 unseen, UR5 플랫폼, 물체 10종×10회)에서 전체 76.00%(84/100, 68/100) 성공.
- Ablation에서 FPA 제거 시 unseen 성공률 74.02%→33.90%, CFA 제거 시 19.40%, 둘 다 제거 시 0.95%로 급락해 두 alignment의 기여가 뚜렷함.
- Grasp 생성 효율은 0.16초/grasp로 T(R,O)Grasp(0.21초)·D(R,O)Grasp(0.75초)보다 빠르나, 생성 diversity는 0.293rad로 baseline(0.401~0.535rad)보다 낮다는 한계를 저자도 명시함.

**Top-tier conference 적합성 — 60/100 · 추천 venue: ICRA**

체계적인 ablation과 손 7종(seen 3·unseen 4)에 걸친 비교, 실로봇 unseen 손 2종 검증까지 갖춰 technical conviction이 높음. 다만 problem formulation 자체는 기존 interaction-centric·morphology-alignment 계열의 연장이라 CoRL/RSS oral급 conceptual leap으로 보기는 어렵고, grasp diversity 저하가 rejection risk로 지적될 만함.

**추천 이유 & 누리랩 연구와의 연결점**

- functional correspondence 개념은 손뿐 아니라 object affordance나 scene graph에서 서로 다른 object instance 간 기능적 대응을 정의하는 데에도 적용할 여지가 있음.
- canonical frame 기반 표현은 failure detection에서 어느 기능 부위에서 실패가 발생했는지를 진단하는 단위로 재사용할 수 있음.
- diffusion 기반 grasp 생성에 test-time optimization을 결합해 미지의 손 적응을 샘플링 단계에서 더 정교화하는 후속 연구로 확장 가능함.

---

## 오늘의 핵심 연구 트렌드 종합

- **VLA의 instruction-action binding 실패 진단** — [Equivariant Counterfactual Training](https://arxiv.org/abs/2609.39971)과 [ReGuide](https://arxiv.org/abs/2609.38616)가 VLA가 language·vision에는 반응하면서도 둘을 결합해 올바른 action을 못 고르는 binding 실패를 서로 다른 각도(counterfactual training vs. training-free rebinding)에서 공략함. 둘 다 LIBERO position-swap을 testbed로 쓰고 실로봇에서 큰 폭(각각 8%→88%, 최대 75.0%p)의 개선을 보임.
- **world model의 planning 유효 범위를 직접 측정하는 흐름** — [The Planning Limits of Latent World Models](https://arxiv.org/abs/2609.39235)가 plannable range가 5~10 step에 불과함을 수치로 입증했고, [RoboCoach](https://arxiv.org/abs/2609.39685)는 그 한계를 world model 상상 rollout으로 실패 subtask를 진단해 우회하고, [EWAM](https://arxiv.org/abs/2609.39973)은 world model과 VLA를 한 transformer로 통합해 다른 방식으로 접근함.
- **action representation에 geometry·structure prior를 명시적으로 주는 흐름** — [BIND](https://arxiv.org/abs/2609.38443)는 3D action 후보를 camera geometry로 2D feature에 투영해 OOD robustness를 얻고, [FunCo-Grasp](https://arxiv.org/abs/2609.39006)는 손 구조를 canonical frame으로 정렬해 cross-embodiment 일반화를 얻음. 둘 다 추가 학습 없이 structural prior로 문제를 해결함.
- **4D·시간 축을 더한 scene representation** — [ChronoGraph](https://arxiv.org/abs/2609.39665)와 [EvolvingNav](https://arxiv.org/abs/2609.39166)는 각각 affordance 기반 action-conditioned scene graph와 persistence-relocation belief로, 관측 사이 변하는 환경의 과거·미래 상태를 명시적으로 추적함.
- **outcome-only label에서 fine-grained credit·verification을 뽑는 흐름** — [PRICE](https://arxiv.org/abs/2609.38890)는 action chunk 단위 credit을, [Looking Back to Move Forward](https://arxiv.org/abs/2609.39038)는 temporal energy-based verifier를 추가 evaluator 없이 뽑아냄.
- **정밀 language grounding 전용 모델·표현** — [GroundingPI](https://arxiv.org/abs/2609.39601)와 [Text-to-3D Policy](https://arxiv.org/abs/2609.39599)는 범용 VLM·video backbone의 grounding 약점을 지적하고 각각 전용 grounding foundation model, fine-grained token-level alignment로 해결함.

## 유망 연구 방향 및 프로젝트 제안

**VLA 내부 상태 기반 실시간 실패 진단·복구 모듈**
- research question: VLA가 familiar-but-wrong trajectory를 재현하는 순간을 rollout 중 internal state만으로 검출하고 test-time에 교정할 수 있는가
- 접근·novelty: ECT의 counterfactual probe·prefix-KV intervention, Looking Back to Move Forward(TeV)의 energy-based temporal verifier, BIND의 image-bound feature uncertainty를 하나의 online monitor로 결합. 기존 연구는 진단(ECT)과 교정(TeV·BIND)을 따로 다룸
- 왜 지금·경쟁 prior works: 세 논문 모두 이번 주 공개, 서로 다른 신호(counterfactual readout, energy, projected feature)를 쓰므로 결합 여지가 큼
- risk·target venue: online 개입이 정책 안정성을 해칠 risk 있고 신호 간 상충 가능. target CoRL/RSS

**world model의 plannable range 안에서만 동작하는 subgoal 생성기**
- research question: plannable range(5~10 step) 밖의 장거리 target을 world model이 다루게 하려면 subgoal을 어떻게 자동 생성해야 하는가
- 접근·novelty: Planning Limits가 수치로 입증한 한계를 RoboCoach의 world-model-in-the-loop 진단, ChronoGraph의 affordance transition 예측과 묶어 subgoal sequence를 world model 스스로 뽑게 함
- 왜 지금·경쟁 prior works: Planning Limits가 처음으로 한계를 정량화했고 이를 메우는 후속 연구가 아직 없음
- risk·target venue: subgoal 품질이 전체 성능을 좌우하고 평가 설계가 어려움. target NeurIPS/CoRL

**functional correspondence를 object affordance·scene graph로 확장**
- research question: FunCo-Grasp의 손 간 canonical frame 정렬을 물체 instance 간 기능적 대응(손잡이, 버튼 등)에 적용하면 cross-category manipulation이 가능한가
- 접근·novelty: canonical frame + diffusion grasp generation을 ChronoGraph의 affordance part node와 결합해, 새 object category에 fine-tuning 없이 전이함
- 왜 지금·경쟁 prior works: 두 논문 모두 이번 주 공개, canonical frame과 affordance node가 구조적으로 유사해 바로 결합 가능
- risk·target venue: object는 손보다 기구학적으로 다양해 canonical frame 정의 자체가 어려움. target CoRL/ICRA

**outcome-only RL credit을 failure localization에 재활용**
- research question: PRICE의 cross-trajectory physical relational graph를 성공 여부가 아니라 "어느 chunk가 실패를 유발했는가" 라벨링에 쓸 수 있는가
- 접근·novelty: PRICE의 potential 차이를 failure chunk 식별 신호로 재정의하고 RoboCoach의 progress judge와 결합해 반복 실패 subtask를 자동 태깅함
- 왜 지금·경쟁 prior works: PRICE 자체가 "같은 상황에 도달한 rollout의 상호 참조"라는 재사용 가능한 틀을 이미 제공함
- risk·target venue: PRICE의 credit 방향 오류가 2.5% 존재해 실패 원인과 결과 chunk를 혼동할 risk 있음. target CoRL

**시간에 따라 변하는 환경에서 scene graph를 belief로 유지**
- research question: EvolvingNav의 persistence-relocation belief를 object-centric 3DGS·scene graph에 통합해 로봇이 안 보는 사이 바뀐 물체 상태를 추론할 수 있는가
- 접근·novelty: belief filter를 scene graph node의 confidence·위치 분포로 표현하고 ChronoGraph의 action-conditioned transition과 결합함
- 왜 지금·경쟁 prior works: 두 논문 모두 "안 보이는 동안의 변화"를 다루지만 navigation과 manipulation으로 분리돼 있어 결합 여지가 큼
- risk·target venue: belief update 연산 비용이 real-time 제약과 부딪힐 risk 있음. target RSS/CoRL

## 오늘 반드시 읽어야 할 논문

- [Equivariant Counterfactual Training (When Instructions Retrieve Trajectories)](https://arxiv.org/abs/2609.39971) — VLA의 instruction-action binding 실패를 mechanistic하게 규명하고 실로봇 success rate를 8%→88%로 올린, 오늘 전체에서 가장 강한 리뷰(86점)
- [BIND: Binding 3D Robot Actions to 2D Image Features](https://arxiv.org/abs/2609.38443) — camera geometry를 action head에 명시적 prior로 넣어 5 demo로 near-perfect 성공과 OOD robustness를 동시에 얻음
- [PRICE the Action Chunks](https://arxiv.org/abs/2609.38890) — 추가 evaluator 없이 outcome label만으로 action chunk 단위 credit을 뽑고 이론적 bound까지 제시함
- [Beyond the Remembered World (EvolvingNav)](https://arxiv.org/abs/2609.39166) — 계속 변하는 환경에서 target 위치를 belief로 추론하는 새 navigation 문제 정의와 실로봇 검증
- [EWAM](https://arxiv.org/abs/2609.39973) — VLA와 world-action model을 한 transformer로 통합했을 때 layer-wise specialization이 자연 발생함을 causal intervention으로 입증
- [ChronoGraph](https://arxiv.org/abs/2609.39665) — 4D interaction understanding과 spatially grounded planning을 같은 affordance scene graph로 묶은 표현
- [The Planning Limits of Latent World Models](https://arxiv.org/abs/2609.39235) — world model 기반 planning의 유효 거리가 5~10 step에 불과함을 처음 정량화
- [RoboCoach](https://arxiv.org/abs/2609.39685) — world model 안에서 반복 실패 subtask를 찾아 해당 skill expert만 선택적으로 업데이트, 150개 demo로 성공률을 13.3%→75.0%까지 올림
- [Text-to-3D Policy](https://arxiv.org/abs/2609.39599) — unseen specification generalization을 새 문제로 정의하고 instruction-behavior token alignment로 해결
- [ReGuide](https://arxiv.org/abs/2609.38616) — VLA 재학습 없이 global grounding만 교정하는 training-free wrapper, 실로봇에서 75.0%p 개선

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (818편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2609.39235'>The Planning Limits of Latent World Models</a></td><td>70</td><td>10</td><td>World Model</td><td>latent world model이 planning에 쓸모 있는 범위는 학습된 rollout 길이 근처뿐이라는 한계를 체계적으로 규명함. 완벽한 시뮬레이터로도 20스텝 이상 목표에서 성공률이 92%에서 41%로 떨어짐을 보여 world model 연구에 중요한 시사점을 줌.</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2609.38443'>BIND: Binding 3D Robot Actions to 2D Image Features</a></td><td>68</td><td>9</td><td>VLA</td><td>3D action 후보를 카메라 기하로 2D 이미지 feature에 직접 결합하는 새로운 action representation을 제안함. 5개 demo만으로 OOD 카메라·물체 위치에 강건한 실로봇 결과를 보임.</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2609.39166'>Beyond the Remembered World: Predictive 4D Belief for Persistent Navigation in Evolving Worlds</a></td><td>68</td><td>9</td><td>Navigation</td><td>타겟이 관측 동안에도 이동할 수 있는 상황에서 시간 인덱스 belief로 위치를 추적·갱신하는 navigation 프레임워크임. VLN 우선주제에 직접 부합하고 시뮬레이션뿐 아니라 실로봇 실험까지 수행함</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2609.39135'>Asking the World: Generalist Physical Reasoning through Agentic World Modeling and Probing</a></td><td>68</td><td>7</td><td>World Model</td><td>비디오로부터 실행 가능한 physics world를 구성하고 질문에 맞춰 시뮬레이션과 개입으로 증거를 얻는 Asking the World 제안임. PolyWorld Engine으로 rigid/soft body와 유체까지 범용 시뮬레이션하며 CEM 기반 system identification으로 동역학을 역추정하는 설계가 test-time 추론 계획과 world model을 결합한 새로운 formulation이고 baseline 대비 개선폭도 크게 보고됨</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2609.39971'>When Instructions Retrieve Trajectories: Diagnosing and Mitigating Generalization Failures in VLA Models</a></td><td>66</td><td>10</td><td>VLA</td><td>VLA가 언어와 비전을 각각은 반응하지만 결합해 행동을 바꾸지 못하는 instruction-action binding 실패를 규명함. 같은 지시가 장면에 따라 다른 행동을 요구하는 counterfactual 학습으로 실로봇 unseen 성공률을 8%에서 88%로 끌어올림.</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2609.38418'>PneuTac: Tactile Manipulation with Soft Pneumatic Robots via Unified MPM-Gaussian Splatting Simulation</a></td><td>66</td><td>9</td><td>Manipulation</td><td>MPM과 3D Gaussian Splatting을 결합해 soft pneumatic robot과 tactile membrane을 동시 시뮬레이션함. real-to-sim 보정 후 실제 tactile manipulation에서 baseline을 능가함.</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2609.38616'>Correcting WHERE, Preserving HOW: Compositional Generalization for Vision-Language-Action Models via Referential Guidance</a></td><td>66</td><td>9</td><td>VLA</td><td>grounding 결과로 global/local re-binding을 결합해 training-free하게 VLA의 compositional generalization을 개선함. 실로봇에서 최대 75pp 성공률 향상을 보임.</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2609.39665'>ChronoGraph: Functional 4D Scene Graphs with Vision-Language Models for Interaction Understanding and Grounded Planning</a></td><td>65</td><td>9</td><td>Embodied AI</td><td>행동이 만든 상태변화를 설명하는 4D scene graph로 이해와 계획을 같은 표현으로 연결함. object-centric 4D representation·scene graph 우선주제에 직접 해당하고 실로봇 모바일 매니퓰레이션까지 시연함</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2609.38890'>PRICE the Action Chunks: Physical Relational Credit Assignment for Embodied Reinforcement Learning</a></td><td>64</td><td>9</td><td>RL</td><td>같은 물리적 상황에 도달한 rollout들을 서로의 참조로 삼아 보조 평가자 없이 action-chunk credit을 추정함. LIBERO·RoboTwin·실로봇에서 성공률과 학습 속도를 모두 개선함.</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2609.39006'>Function beyond Form: Functional Correspondence for Cross-Embodiment Dexterous Grasp Generation</a></td><td>64</td><td>9</td><td>Manipulation</td><td>구조가 다른 손들 사이에 기능적으로 대응하는 부위를 정렬하는 functional correspondence 표현을 제안함. 미지의 손에 추가 데이터 없이 76% 실로봇 성공률을 보임.</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2609.39685'>RoboCoach: World Models as Active Coaches for Compositional Robot Skills</a></td><td>64</td><td>9</td><td>World Model</td><td>world model이 상상한 실패 지점을 바탕으로 어떤 demonstration을 어디서 모을지 결정하는 coaching loop임. 상상 성공률과 실제 성공률의 상관이 높고 두 실로봇 플랫폼에서 큰 개선을 보임.</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2609.39973'>EWAM: Emergent Depth-Wise Specialization in a Unified Embodied Model -- From Semantic Understanding through Visual Foresight to Action</a></td><td>64</td><td>9</td><td>VLA</td><td>VLA와 world-action model을 하나로 묶었을 때 층별로 semantic·미래예측·action에 순차적으로 집중하는 현상을 발견함. 사람 자아중심 영상 사전학습이 cross-embodiment 전이와 실로봇 강건성을 모두 높임.</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2609.39038'>Looking Back to Move Forward: Temporal Verification for Generative Robot Policies</a></td><td>62</td><td>9</td><td>VLA</td><td>현재 관측만 보던 action verification을 과거 이력을 요약한 temporal token 조건으로 확장함. energy-based verifier로 flow sample 자체를 유도해 test-time scaling 성능을 높임.</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2609.39599'>Text-to-3D Policy: Fine-Grained Language-Behavior Alignment for Unseen Specification Generalization</a></td><td>62</td><td>9</td><td>VLA</td><td>지시문과 행동을 토큰 단위로 양방향 대응시켜 미세한 언어-행동 구분을 보존함. Meta-World·ManiSkill·RoboTwin과 실로봇 전반에서 unseen specification 성공률을 크게 높임.</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2609.39601'>GroundingPI: A Grounding Foundation Model towards Physical Intelligence with Visual Primitives</a></td><td>62</td><td>8</td><td>VLA</td><td>VLA·world-action model의 perception 병목을 겨냥한 grounding foundation model GroundingPI 제안임. RoboTwin 2.0과 RoboCasa-GR1에서 OOD manipulation 성능을 크게 올리고 nuScenes 자율주행까지 검증해 perceptual pretraining이 physical intelligence의 기반이 된다는 주장을 실증적으로 뒷받침함</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2609.38494'>What to Attend, What to Keep: Skill-Conditioned Visuotactile Representation with Progress-Guided Event Memory</a></td><td>62</td><td>8</td><td>Manipulation</td><td>skill별로 vision-touch 기여도가 달라진다는 관찰에서 progress-guided event memory를 제안함. slip-detection 지연을 87% 줄여 robot memory 주제와 직결됨.</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2609.38746'>Matisse: Evidence-Space Reasoning for Active 3D Reconstruction</a></td><td>62</td><td>7</td><td>3D Vision</td><td>pretrained 3D 생성모델의 cross-attention evidence로 evidential uncertainty를 추정해 active view 선택과 keyframe 선택을 통합하는 Matisse 제안임. 미관측 구조에 대한 불확실성까지 추론한다는 점이 기존 active reconstruction 대비 본질적 차이이고 active perception/NBV 우선 주제와 정확히 맞음</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2609.38927'>World-as-Graph: Relational World Modeling Through Latent Space Graphs</a></td><td>62</td><td>7</td><td>World Model</td><td>object-centric world model에 relational latent graph를 결합한 WAG 제안, JEPA 스타일 예측학습에 관계 귀납편향 추가하고 로봇 조작 태스크에서 성능 확인함</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2609.39101'>Beyond Prediction: Steering VLM Agents with Retrospective World Modeling</a></td><td>62</td><td>7</td><td>World Model</td><td>순방향 예측만 하던 기존 world model과 달리 상태전이로부터 행동을 역추론하는 retrospective world modeling을 제안함. self-consistency reward로 VLM agent의 물리적 일관성을 높이고 NeurIPS 2026에 accept됨</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2609.38537'>Systematically Exploring the Capabilities of GPT-6 Astra as Embodied Policies</a></td><td>60</td><td>9</td><td>VLA</td><td>GPT-6 Astra를 조작·보행·내비게이션 등 6개 영역에서 범용 embodied policy로 체계 평가함. 결정 능력과 물리 제어 신뢰성 사이 간극을 드러낸 실증 연구임.</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2609.38855'>Online Evolution Strategy for Flow-Matching VLA Policies via Self-Supervised Trajectory Distribution Optimization</a></td><td>60</td><td>9</td><td>VLA</td><td>latent noise가 아닌 action trajectory 공간에서 evolution strategy로 flow-matching VLA를 온라인 적응시킴. 가치모델 없이 RL fine-tuning에 준하는 개선을 보임.</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2609.38886'>Benchmarking and Enhancing Skill-Level Memory for Partially Observable Robotic Manipulation</a></td><td>60</td><td>9</td><td>Manipulation</td><td>부분관측 조작에서 반복·이력 회상·진행추적을 요구하는 HIDE 벤치마크와 SEEK 메모리 프레임워크를 제시함. robot memory 주제를 직접 다루며 실로봇 검증도 포함함.</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2609.39017'>OccluDex: Hierarchical 3D Visuo-Tactile Representation Learning for Egocentric Dexterous Manipulation under Self-Occlusion</a></td><td>60</td><td>9</td><td>Manipulation</td><td>자기가림이 심한 상황에서 전역 기하와 국소 tactile 접촉을 계층적으로 결합한 표현학습임. Shadow Hand로 zero-shot sim-to-real 일반화를 보임.</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2609.39375'>Beyond the Current Scene: Event-Referential Grasping with Active View Selection</a></td><td>60</td><td>9</td><td>Manipulation</td><td>과거 사건에서의 역할로 대상이 지칭되고 현재는 가려져 있는 상황의 zero-shot grasping을 다룸. event prior로 시점을 능동 선택해 occluded 상황 성공률을 55%에서 77%로 높임.</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2609.39403'>IronMind: Scaling Humanoid Dexterous Manipulation via Camera-Space Ego-Centric Pretraining</a></td><td>60</td><td>9</td><td>VLA</td><td>카메라 공간 action representation으로 사람-로봇 retargeting 없이 1만 시간 자아중심 영상을 사전학습에 사용함. OOD 실로봇 과제 성공률을 5%에서 55%로 크게 높이는 스케일링 결과를 보임.</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2609.39870'>Magic-W0: A Structured World-Action Foundation Model for Physical Intelligence</a></td><td>60</td><td>9</td><td>World Model</td><td>현재 3D 기하·3D motion transition·미래 semantics로 구조화된 world transition을 action과 layer별로 상호작용시킴. 대규모 사전학습 후 여러 실로봇 과제에서 빠른 적응을 보임.</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2609.40153'>Dream4ACT: A Shared Visual Action Interface for Multi-Embodiment Video-Action Modeling</a></td><td>60</td><td>9</td><td>World Model</td><td>URDF 기반 forward kinematics로 action을 가상 카메라 이미지로 렌더링해 embodiment마다 다른 action space를 통일함. RoboTwin2.0에서 89% 성공률로 학습된 디코더 없이 action을 복원함.</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2609.40306'>DynaHarness: A Dynamic Physical Harness for Self-Evolving Robot Agents</a></td><td>60</td><td>9</td><td>VLA</td><td>느린 의미 추론과 빠른 물리 실행을 분리하고 실패 증거로 재사용 가능한 능력을 갱신하는 dynamic harness를 제안함. LIBERO-Pro에서 고정 정책 17.5%를 75.2%까지 끌어올림.</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2609.40137'>Game-Guided Skill Discovery through Self-Play for Playable Agent Control</a></td><td>60</td><td>8</td><td>RL</td><td>게임 self-play로 사람이 직접 조작 가능한 discrete skill을 발견하는 GGSD, Ant·Franka-arm·Unitree G1 환경에서 검증하고 미학습 과제로 조합 전이까지 보임</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2609.38202'>Optimize, Learn, Refine: Whole-Body Grasping and Pick-and-Throw with a Spiral Soft Robot</a></td><td>60</td><td>8</td><td>Manipulation</td><td>soft continuum robot의 whole-body grasping·pick-and-throw를 CMA-ES와 학습된 warm start로 최적화함. 실제 하드웨어에서 100% 성공률 달성함.</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2609.38640'>Yggdrasil: a Layer-First 3D Scene Graph for Real-Time Querying</a></td><td>60</td><td>8</td><td>3D Vision</td><td>generation과 consumption 모두를 고려한 layer-first 3D scene graph 구조임. 기존 DSG 대비 최대 121배 빠른 질의 응답으로 3개 실제 파이프라인에 통합됨.</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2609.38905'>EmbodiRSI: Recursive Self-Improvement for Data-Efficient Robot Adaptation</a></td><td>60</td><td>8</td><td>Manipulation</td><td>real-to-sim-to-real 환경에서 실행 피드백으로 보정 궤적과 적응 데이터 수집을 동시에 닫는 recursive self-improvement 시스템임. 실로봇 10분 상호작용만으로 83% 성공률을 달성함.</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2609.38982'>SimEX: Simulation-Integrated Robotics AutoResearch</a></td><td>60</td><td>8</td><td>Embodied AI</td><td>coding agent가 시뮬레이션에서 먼저 robot toolbox를 만들고 소수 실물 trial로 시뮬레이터를 교정하는 2단계 autoresearch 구조임. 실로봇 작업을 시연 없이 10분 상호작용으로 익힘.</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2609.39322'>A Biophysically Detailed C. elegans Circuit as a Task-Agnostic Dynamical Core for Visually Robust Robot Manipulation</a></td><td>60</td><td>8</td><td>Manipulation</td><td>136개 뉴런의 생물물리학적 C. elegans 회로를 고정된 dynamical core로 써서 visuomotor policy의 시각 교란 강건성을 얻음. 일반 신경망으로 교체하면 강건성이 사라짐을 실로봇으로 확인함.</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2609.40165'>PrefPI: Preference-Guided Steering into Out-of-Distribution Behaviors</a></td><td>60</td><td>8</td><td>RL</td><td>선호 궤적을 조건부 생성모델로 보고 classifier-free guidance로 증폭해 초기 정책 분포 밖의 행동으로 steering함. 150개 선호 라벨만으로 실제 하드웨어에서 큰 행동 변화를 만듦.</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2609.39182'>MEND: Label-Free Detection, Localisation, and Correction of Latent Hallucination in World Models</a></td><td>60</td><td>7</td><td>World Model</td><td>라벨 없이 world model의 latent hallucination을 denoising score로 탐지·국소화·보정하는 MEND 제안임. 자기 지도 world model의 조용한 오차 누적 문제를 정면으로 다루고 하나의 score field로 세 기능을 수행하는 설계가 failure detection·recovery 연구와 바로 연결됨</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2609.38285'>GaugeVLM: Structuring Spatial Supervision with Measured Geometric Interventions</a></td><td>60</td><td>4</td><td>VLA</td><td>3D scene에서 측정 가능한 기하 개입으로 preference margin을 만드는 GaugeDPO 제안임. spatial VQA에서 큰 개선폭 보이고 embodied reasoning/자율주행까지 일반화 주장함. VLM spatial supervision에 새로운 formulation을 제시한 점이 눈에 띔</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2609.39198'>DSDyn-VLA: A Dual-Stream Dynamic Manipulation Framework with Motion Perception, Future Awareness, and Realtime Correction</a></td><td>58</td><td>9</td><td>VLA</td><td>perception·latency·control gap을 각각 optical flow 예측과 고주파 RL 보정으로 해결하는 dual-stream 구조임. 동적 물체 조작에서 PI0.5 대비 5~6배 성공률을 보임.</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2609.40341'>Ego4WAM: What Matters When Scaling Egocentric Human Data for Robot Learning?</a></td><td>58</td><td>9</td><td>VLA</td><td>사람-로봇 정합성·데이터 다양성·지도 방식·사용 전략을 분리해 자아중심 데이터 스케일링에서 무엇이 중요한지 체계적으로 규명함. 실로봇과 RoboDojo closed-loop 평가로 검증함.</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2609.38401'>Memorize, Adapt, Ignore: Diagnosing Robot Learning Mechanisms under Training Data Variation</a></td><td>58</td><td>8</td><td>VLA</td><td>NTK를 진단 도구로 써서 domain randomization이 memorize에서 adapt로 전환되는 메커니즘을 규명함. VLA fine-tuning과 실로봇 ACT까지 검증한 분석 논문임.</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2609.38989'>Cue the Flow: Steering Flow-Matching Policies for Open-World Delivery Manipulation</a></td><td>58</td><td>8</td><td>VLA</td><td>grounding 결과를 spatial cue로 삼아 사전학습된 flow-matching VLA를 가벼운 adapter로 steering함. open-world delivery 조작에서 성공률을 거의 2배 높임.</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2609.39207'>ASENA: Self-evolving Agents for Embodied Navigation</a></td><td>58</td><td>8</td><td>Navigation</td><td>coding agent에 지속적 경험과 실행 중 복구를 결합해 navigation policy를 보조 도구로 통합함. R2R 성공률을 반복 수행만으로 72%에서 98%까지 끌어올림.</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2609.39579'>AVERT-VLN: Abstention-aware Visual Error Recovery and Training for Vision-and-Language Navigation</a></td><td>58</td><td>8</td><td>Navigation</td><td>VLN에서 경로 이탈을 감지하고 사람 교정을 요청·재사용하는 closed-loop recovery 프레임워크임. VLN·failure detection/recovery 두 우선주제에 직접 부합하며 R2R-CE·RxR-CE에서 검증함</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2609.38620'>HIGS: Hierarchical Implicit Grids for Joint Geometric and Semantic Scene Understanding</a></td><td>58</td><td>7</td><td>World Model</td><td>multiresolution submap으로 기하와 semantic을 함께 임베딩하는 hierarchical implicit field HIGS 제안임. large-scale 실시간 매핑과 open-vocabulary grounding을 동시에 지원해 로봇 공간 인지에 바로 쓸 수 있음</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2609.39794'>Inline Memory Meets Reusable Skills: Memory-centric Framework for Vision-Language-Action Model</a></td><td>58</td><td>7</td><td>VLA</td><td>VLA의 prefix stream에 memory token을 삽입해 query-skill memory bank로 skill을 재사용하는 Optimus-R 제안임. 파라미터 튜닝 없이 도메인 적응과 lifelong learning에서 catastrophic forgetting을 완화한다는 점이 robot memory 연구 방향과 정확히 맞음</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2609.38483'>CADeT: Causal-Aware Deformation Transmission for Indirect Robotic Manipulation of Soft Tissue</a></td><td>58</td><td>7</td><td>Manipulation</td><td>structural causal model과 active sensing으로 간접 조직 변형 전달 모드를 추론함. dVRK와 ex vivo 돼지 조직 검증까지 포함한 수술로봇 연구임.</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2609.39000'>NEXUS: Perceptive Whole-Body Control for Terrain-Adaptive Teleoperation</a></td><td>58</td><td>7</td><td>RL</td><td>지형이 다른 평지-비평지 간 모션 쌍을 대량 생성해 지형 적응형 whole-body teleoperation을 학습함. zero-shot 실로봇 다양한 지형 원격조작까지 검증함.</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2609.38615'>Exo2EgoHOI: Hand-Object-Interaction Aware Exocentric-to-Egocentric Video Generation</a></td><td>58</td><td>6</td><td>Manipulation</td><td>4D hand-object interaction prior로 exo 영상을 ego 시점으로 변환해 로봇 학습용 데이터를 확장하는 Exo2EgoHOI 제안임. object consistency와 HOI 보존 개선폭이 크고 manipulation 데이터 스케일링이라는 실질적 문제를 다룸</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2609.39145'>Blackout vs. Freeze: Analyzing Physical Failure Modes of VLAs under Camera Faults</a></td><td>56</td><td>9</td><td>VLA</td><td>blackout과 freeze라는 카메라 고장이 서로 다른 물리적 실패 양상을 일으킴을 실로봇에서 분석함. failure detection·recovery 설계에 직접 연결되는 실증 연구임.</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2609.38216'>Fiatlux: A Long-Horizon Benchmark for Humanoid Ladder Climbing and Light-Bulb Replacement</a></td><td>56</td><td>8</td><td>Embodied AI</td><td>사다리 등반과 전구 교체를 한 에피소드로 묶은 long-horizon humanoid benchmark임. VLA 베이스라인 포함해 평가 체계를 제공함.</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2609.38857'>Plan-Conditioned Imitation for Robust Object Retrieval under Self-Occlusion in Dense Clutter</a></td><td>56</td><td>8</td><td>Manipulation</td><td>digital twin의 고정 teacher rollout을 따라가는 plan-conditioned imitation으로 self-occlusion 하 물체 검색을 해결함. UR5e에서 실행시간을 192초에서 67초로 줄임.</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2609.39018'>Make Code as Policy Great Again: Frontier Agents Write, Call, and Evolve Robot Tools</a></td><td>56</td><td>8</td><td>Manipulation</td><td>code-as-policy를 다시 가져오되 프로그래밍 agent와 실행 agent의 역할을 나눠 재사용 가능한 로봇 tool을 만들고 revise함. 실제 양팔로봇 7과제에서 검증함.</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2609.39388'>UniWAM Technical Report: Unified Mobile Manipulation via Mixed-Stream World-Action Modeling and Manipulation Anchor Pose Supervision</a></td><td>56</td><td>8</td><td>World Model</td><td>내비게이션과 조작을 공유 backbone에 분리된 action head로 통합하고 조작 준비 자세를 이미지 평면 보조 지도로 학습함. 150만 에피소드 데이터와 24개 실로봇 과제로 검증함.</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2609.39751'>Beyond Policy Alignment: Closing the Planning-Learning Loop for Robot Control with Learned World Models</a></td><td>56</td><td>8</td><td>World Model</td><td>TD-MPC의 critic·terminal value 추정을 다단계 target과 불확실성 인지로 보강함. HumanoidBench에서 큰 개선을 보이고 KUKA 실로봇 zero-shot 전이까지 검증함.</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2609.39820'>Learning from Runtime Feedback through Failure-Bank Self-Evolution for Vision-Language-Action Models</a></td><td>56</td><td>8</td><td>VLA</td><td>CBF 기반 teacher의 반사실적 보정을 LoRA 업데이트로 흡수해 runtime shield를 정책 자체 개선으로 바꿈. failure-driven 지속 개선이라는 점에서 failure recovery 주제와 직결됨.</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2609.39873'>SplineWAM: Adaptive Action Horizons for World Action Models via B-Spline Representations</a></td><td>56</td><td>8</td><td>World Model</td><td>고정 action chunk 대신 B-spline으로 동작 복잡도에 맞춰 action horizon을 가변적으로 압축함. LIBERO-Plus와 양팔 실로봇에서 호출 횟수를 줄이며 성능을 높임.</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2609.40007'>Multi-Link Safety Filtering for VLA Policies Around Moving Hazards</a></td><td>56</td><td>8</td><td>VLA</td><td>end-effector뿐 아니라 팔 전체를 ellipsoid로 감싸고 optical flow로 위험물을 추적하는 training-free safety shield임. edge GPU에서 2.2ms로 동작하며 실로봇 충돌을 3분의 1로 줄임.</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2609.40134'>Tactile Curiosity Drives Robot Interaction</a></td><td>56</td><td>8</td><td>RL</td><td>모델 불확실성을 촉각 채널로 좁혀 접촉이 없는 자유공간 탐색을 줄이는 curiosity 방법임. task reward 없이 조작을 학습하고 VLA post-training에도 샘플 효율적으로 기여함.</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2609.40177'>Social-WM: Safety-Aware Latent World Models for Robot Social Navigation</a></td><td>56</td><td>8</td><td>World Model</td><td>명목 action과 실제 실현된 action의 차이를 latent world model로 학습해 실행 전 안전 신호를 얻음. 사람 충돌률을 21.67%로 줄이며 zero-shot으로 다른 환경에도 전이함.</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2609.38383'>Learning to Plan from Random Exploration</a></td><td>56</td><td>7</td><td>RL</td><td>action·reward 라벨 없이 random exploration만으로 horizon별 시간적 관계를 학습해 장거리 계획을 하는 방법 제안임. 조건부 energy-based model로 geodesic 기하와 연결성을 분리해 학습하고 manipulation 계획까지 suboptimal 데이터로 검증해 policy 개선 학습 없는 planning이라는 formulation이 새로움</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2609.38641'>Vision-Language-Action Autonomous Driving Agent with Language-based Memory</a></td><td>55</td><td>6</td><td>VLA</td><td>언어 기반 메모리를 CoT 확장으로 출력해 VLA 자율주행 에이전트의 장기 기억 문제를 다루는 AD-Memo 제안임. latent memory 대비 해석 가능하고 이식 가능한 memory 구조라는 점이 VLA의 memory 연구와 바로 연결됨</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2609.39116'>GRC-Pose: Generation-Reconstruction Correspondence for Prior-Free 6D Object Pose Tracking</a></td><td>55</td><td>6</td><td>Manipulation</td><td>CAD 없이 generation-reconstruction correspondence로 6D object pose를 추적하는 GRC-Pose 제안임. object-scene correspondence와 posterior gating으로 occlusion에 강건하고 HOT3D에서 motion retention을 크게 개선해 manipulation의 핵심 perception 문제에 바로 쓰일 수 있음</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2609.39195'>Uruqi: Learning Spatial Cognition from Visual Experience</a></td><td>55</td><td>6</td><td>Embodied AI</td><td>연속적인 시각 경험으로 self-motion tracking과 지속적 mapping을 학습시키는 Uruqi 제안임. 1만 건 이상의 모티프 기반 카메라 궤적으로 atomic spatial capability를 학습시킨다는 formulation이 embodied spatial reasoning 우선 주제에 정확히 부합하고 개선폭도 큼</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2609.39600'>GroundAnything: Reconciling Parallel Decoding with Precise Visual Grounding at Flash Speed</a></td><td>55</td><td>6</td><td>VLA</td><td>bidirectional diffusion으로 grounding을 병렬 디코딩하는 GroundAnything 제안임. autoregressive grounding의 순차적 지연을 없애면서 정확도도 유지해 latency-sensitive 로봇 인식 파이프라인에 바로 쓸 수 있음</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2609.39915'>NavHarness: Adaptive Goals for Agentic Vision-Language Navigation</a></td><td>55</td><td>6</td><td>Navigation</td><td>Goal·Verify·Memory·Visuomotor agent로 역할을 분리한 agentic VLN 프레임워크임. 실제 환경 8개 경로에서 83.3% 성공률을 보여 VLN의 장기 일관성과 추론 비용 문제를 함께 다룬 점이 우선 주제와 직접 맞음</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2609.40222'>LOCI: Spatial Linear Memory for Streaming World Models</a></td><td>55</td><td>6</td><td>World Model</td><td>key-value cache와 카메라 기하 조건부 recurrent linear memory를 함께 쓰는 hybrid 구조 LOCI 제안임. 재방문 장면을 재현하는 능력과 메모리 효율을 동시에 개선해 streaming world model의 robot memory 문제에 실질적으로 기여함</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2609.38955'>Loop-Free Inverse Reinforcement Learning via Sequential Value Recovery with Q-Score Matching</a></td><td>55</td><td>6</td><td>Manipulation</td><td>diffusion policy의 action-gradient 구조로 bi-level 최적화 없이 IRL 수행하는 LFIRL 제안, Franka Kitchen·Adroit Hand Pen·Push-T 등 실제 조작 벤치마크에서 검증함</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2609.39888'>Markovian Dynamics Enforcer: Feasibility Preserving Correction on Learned Dynamics Manifolds</a></td><td>55</td><td>6</td><td>World Model</td><td>학습된 동역학 매니폴드에 궤적을 투영해 물리적 타당성을 사후 보정하는 MaDE 제안, 로보틱스·제어 분야 NeurIPS 논문이고 차량 궤적에서 베이스라인 대비 큰 잔차 개선을 보임</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2609.38716'>SpatialCORE: Confidence-Aware Grounded Spatial Reasoning in Large Vision--Language Models</a></td><td>55</td><td>5</td><td>Embodied AI</td><td>grounding confidence를 보상에 반영해 spatial reasoning을 강화학습으로 개선하는 SpatialCORE 제안임. confidently localized object에서 reasoning하도록 유도하는 설계가 embodied spatial reasoning 우선 주제와 직접 연결됨</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2609.39238'>4MT-VLM: How Coarse Is a VLMs Cognitive Map?</a></td><td>55</td><td>5</td><td>Embodied AI</td><td>VLM의 cognitive map 해상도를 시점 변화로 테스트하는 벤치마크임. embodied spatial reasoning 우선주제와 맞닿아 있고 frontier 모델의 급격한 성능 붕괴를 수치로 보여줌</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2609.39604'>Why Do Conventional World Models Fail to Learn Cellular Automata?</a></td><td>55</td><td>5</td><td>World Model</td><td>transformer·diffusion 기반 world model이 cellular automata의 정확한 동역학을 못 배우는 이유를 공간·시간 locality와 안정성 결여로 규명함. 구조 수정만으로 거의 완벽한 rollout을 달성한 깔끔한 분석</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2609.38562'>LongTake: Learning to Sustain Dynamics in Long-Horizon Video Generation</a></td><td>55</td><td>3</td><td>World Model</td><td>긴 teacher forcing으로 autoregressive video diffusion의 장기 동역학 붕괴를 완화하는 LongTake 제안임. world model의 long-horizon rollout 안정성 문제를 직접 다뤄 관련성 있고 실험적 증거도 구체적임</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2609.38984'>Sparse-WAM: Accelerating World Action Models via Action-Guided Sparse Imagination</a></td><td>54</td><td>8</td><td>World Model</td><td>action-to-future attention의 중첩을 이용해 world-action model의 denoising에서 관련 토큰만 선택적으로 처리함. training-free로 2배 가속하며 성능을 거의 유지함.</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2609.39178'>Exploiting Vulnerabilities: Universal Adversarial Attacks on Vision-Language-Action Models in Robotics</a></td><td>54</td><td>8</td><td>VLA</td><td>표면 텍스처를 최적화한 구를 놓는 것만으로 VLA의 trajectory·action을 동시에 교란하는 universal adversarial object를 제시함. 실로봇·시뮬 모두에서 성공률을 큰 폭으로 떨어뜨림.</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2609.39179'>LocoWM: High-Precision Locomotion through World-Model-Guided Residual Adaptation</a></td><td>54</td><td>8</td><td>World Model</td><td>action-conditioned world model이 예측한 미래 상태로 residual을 선제적으로 보정하는 locomotion 프레임워크임. 지형·가속·푸시 회복 전반에서 reactive residual 대비 우위를 보임.</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2609.39324'>MotionWeave: Learning Motion-Centered Future Dynamics for Vision-Language-Action Policies</a></td><td>54</td><td>8</td><td>VLA</td><td>미래 영상 전체 대신 action이 유발하는 국소 상호작용 영역만 motion cue로 추출해 action-chunk를 보강함. MetaWorld에서 π0 대비 8.6%p 성공률 향상을 보임.</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2609.39526'>Discrete Forcing: Infusing Discrete Guidance into Continuous Denoising for Few-Step Action Experts</a></td><td>54</td><td>8</td><td>VLA</td><td>discrete action token으로 거친 구조를 먼저 잡고 continuous token으로 세부를 정제하는 coarse-to-fine action expert임. 실로봇 고정밀·동적 조작에서 개선을 보임.</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2609.39754'>ChunkTrust: Adapting Execution Horizons for Robot Policies with Action-Expert Evidence</a></td><td>54</td><td>8</td><td>VLA</td><td>action chunk 실행 길이를 고정 hyperparameter가 아닌 action-expert evidence로 추론하는 방식임. 여러 backbone과 실제 가정 환경 과제에서 일관된 성능 개선을 보임.</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2609.39822'>Toward Real-Time VLAs: Stage-Aware Two-Step Flow Denoising and System-Level Evaluation</a></td><td>54</td><td>8</td><td>VLA</td><td>속도장이 초반엔 안정적이고 후반에 방향 보정이 커진다는 관찰로 2단계 비균등 denoising을 제안함. 실제 의류 접기 장기 과제에서 시스템 수준 평가까지 수행함.</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2609.40219'>Learning Skills from Historical Action Trajectories: Action Experience Dictionary for World Action Models</a></td><td>54</td><td>7</td><td>Manipulation</td><td>과거 행동 궤적을 공유 embedding으로 인코딩해 World Action Model의 skill 재사용을 가능하게 하는 Action Experience Dictionary 제안임. cross-task와 cross-embodiment 실로봇 실험까지 검증해 skill chaining·재사용이라는 우선 주제에 바로 닿아 있음</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2609.38225'>SynIL: Leveraging Synergy for Offline Imitation Learning from Imperfect Demonstration Datasets</a></td><td>54</td><td>7</td><td>RL</td><td>motor synergy 기반 label-free demonstration 품질 평가로 offline IL을 개선함. D4RL·Robomimic에서 BC 대비 우위를 보임.</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2609.38617'>Dense Temporal Motion Retargeting for Legged Robots</a></td><td>54</td><td>7</td><td>RL</td><td>timing과 control을 동시 최적화하는 dense temporal motion retargeting을 제안함. GPU 병렬 sampling MPC로 기존 대비 19배 빠르면서 더 정밀함.</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2609.38852'>Locomotion-Grounded Humanoid Soccer: Task-Gated Reinforcement Learning of a Multi-Directional Kicking Library</a></td><td>54</td><td>7</td><td>RL</td><td>범용 locomotion을 먼저 학습하고 킥 스킬을 task-gated layer로 얹는 역발상 구조임. 29-DoF G1 실로봇에서 7가지 킥을 검증함.</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2609.38948'>DrivingBench: Can Vision-Language Models Drive a Toyota Corolla?</a></td><td>54</td><td>7</td><td>Embodied AI</td><td>실제 자동차를 VLM이 직접 조향·속도 명령으로 운전하게 한 최초의 벤치마크임. GPT-6 Astra만 완주해 모델 간 큰 격차를 드러냄.</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2609.39797'>Tool-Policy Co-Design for Powder Weighing in Laboratory Automation</a></td><td>54</td><td>7</td><td>Manipulation</td><td>분말 계량 도구 형상과 제어 정책을 bi-level 최적화로 함께 설계하는 새로운 패러다임임. 7개 재료에서 기존 도구 대비 오차를 45% 줄임.</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2609.40353'>AssemblyWorld: Rethinking 3D Assembly with General-Purpose Agents</a></td><td>54</td><td>6</td><td>Manipulation</td><td>범용 agent가 fine-tuning 없이 시각적 상호작용만으로 3D 조립을 수행할 수 있는지 평가하는 AssemblyWorldBench 제안임. part accuracy와 complete-assembly success의 큰 격차를 드러내 manipulation 계획·실행 간 간극을 정량화함</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2609.38966'>Video2SwimFish: An Automated Pipeline for Reconstructing Controllable Fish Models and Biological Locomotion from Real Fish Videos</a></td><td>54</td><td>6</td><td>3D Vision</td><td>실제 물고기 영상에서 VLM actor-critic으로 articulation을 생성해 controllable fish asset을 만듦. task 성공과 개체별 운동 충실도가 함께 가지 않는다는 점을 지적함.</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2609.39507'>LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation</a></td><td>52</td><td>8</td><td>Embodied AI</td><td>범용 agent가 스스로 관측을 고르고 도구를 써서 직접 조작하게 하는 agent-native 벤치마크임. 짧은 과제는 잘하지만 장기 과제에서 신뢰도가 급격히 떨어짐을 보임.</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2609.38709'>CEER2: Directional and Tunable End-Effector and Root Compliance for Humanoid Loco-Manipulation</a></td><td>52</td><td>7</td><td>RL</td><td>방향별 조절 가능한 end-effector·root compliance를 계층적 RL로 구현한 humanoid loco-manipulation 프레임워크임. 실로봇에서 협력 운반까지 시연함.</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2609.38864'>AdaOcc: Adaptive 3D Occupancy Prediction for Embodied Tasks</a></td><td>52</td><td>6</td><td>Embodied AI</td><td>다양한 센서 입력과 연산 예산에 적응하는 point 기반 3D occupancy 예측 AdaOcc 제안임. embodied 배포 요구사항(센서 구성, 연산 예산 가변성)을 정면으로 다루고 실제 임베디드 시스템 적용 가능성을 보임</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2609.40244'>StreamRig: Exploiting Intra-Rig Geometry for Streaming Multi-Camera Odometry</a></td><td>52</td><td>6</td><td>Navigation</td><td>frozen multi-view 3D foundation model 위에 rig 기하를 압축하는 causal streaming odometry StreamRig 제안임. 시뮬레이션만으로 학습해 휴머노이드 로봇 데이터셋에서도 zero-shot으로 드리프트를 줄여 모바일 로봇 실시간 odometry에 실질적으로 유용함</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2609.39901'>Do Better Goal Representations Improve Goal-Conditioned Reinforcement Learning?</a></td><td>52</td><td>6</td><td>RL</td><td>offline goal-conditioned RL에서 goal representation보다 state representation이 성능의 진짜 병목임을 OGBench 내비게이션에서 실증함</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2609.38717'>Soft Spatial Reasoning</a></td><td>52</td><td>5</td><td>Embodied AI</td><td>spatial reasoning CoT에서 토큰을 하드하게 고정하지 않고 soft state로 유지하는 AdaptSoft 제안임. 조기 discretization 문제를 다루는 설계는 새롭지만 spatial 태스크 한정 검증임</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2609.39227'>Emergent Multi-View Geometry Through Self-Distillation</a></td><td>52</td><td>4</td><td>3D Vision</td><td>RGB 재구성 없이 self-distillation만으로 multi-view geometry를 학습하는 Poincar3 제안임. correspondence·pose·3D reconstruction에서 DINOv3 등 기존 self-supervised 표현을 능가해 로봇 시각 foundation 표현으로 쓸 여지가 있음</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2609.39970'>PhasePlan: Ordered Future-Phase Planning for Robot Brain Models</a></td><td>50</td><td>8</td><td>VLA</td><td>고정 길이 action chunk가 task phase 경계를 가린다는 문제를 미래 phase 예측으로 해결함. conveyor-belt 조작에서 π0.5 대비 offline joint-action 오차를 22.5% 줄임.</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2609.38873'>DODGER: Safety-Guided Reinforcement Learning for Robot Navigation Among Dynamic Obstacles</a></td><td>50</td><td>7</td><td>RL</td><td>CBF 필터를 직접 실행하지 않고 reference로만 써서 policy의 탐색 제약을 줄인 안전 RL임. 실제 humanoid LiDAR 내비게이션까지 검증함.</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2609.39056'>SteerQuant: Steering Quantization Error with Action-Guided Scaling in World-Action Models</a></td><td>50</td><td>7</td><td>World Model</td><td>stream마다 quantization 오차가 action에 미치는 영향을 매핑해 4-bit 양자화를 조정함. 실제 양팔로봇에서 BF16 대비 1.35배 가속하며 성능 유지함.</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2609.39153'>Concurrent Semantic Search and Mission Execution for LTL Missions in Unknown Environments</a></td><td>50</td><td>7</td><td>Navigation</td><td>VLM 기반 scene graph와 LTL mission automaton을 결합해 탐색과 임무 수행을 동시에 진행함. photorealistic 환경에서 더 짧은 경로로 더 많은 미션을 완수함.</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2609.39670'>From Local Whole-Body VLA Behaviors to Scene-Scale Aerial Manipulation</a></td><td>50</td><td>7</td><td>VLA</td><td>물리 플랫폼 시연 없이 합성 궤적으로 aerial manipulator VLA를 학습하고 latency를 보정해 실행함. 실제 articulated UAM에서 다중 사이트 임무를 검증함.</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2609.39755'>Experience-Driven Continual Learning of Terrain Traversability for Quadruped Robots</a></td><td>50</td><td>7</td><td>RL</td><td>접촉 전 이미지로 접촉 후 결과를 예측하는 evidential regressor를 지속학습으로 갱신함. Unitree Go2 실제 시퀀스에서 gated replay의 효과를 검증함.</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2609.39763'>DiffWAM: A Fast and Efficient Navigation World Action Model</a></td><td>50</td><td>7</td><td>World Model</td><td>frozen video model의 예측 feature에서 직접 3D 카메라 궤적을 복원해 future-video decoding을 생략함. Jetson에서 1초 수준 지연으로 실시간 UAV 내비게이션을 구현함.</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2609.39854'>RL-Guided PAC-NMPC for Probabilistically-Safe Perception-Based Navigation in Unknown Environments</a></td><td>50</td><td>7</td><td>RL</td><td>RL로 학습한 확률 모델을 PAC-NMPC의 hard constraint로 써서 통계적 충돌 확률 보장을 유지함. 고정익 UAV 실제 비전 기반 내비게이션으로 검증함.</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2609.40245'>STARS: From Spatiotemporal Dynamics to Social Representations in Human-Robot Interaction</a></td><td>50</td><td>7</td><td>Navigation</td><td>사회적 내비게이션에 필요한 시공간·사회적 추론을 VQA로 평가하는 벤치마크임. 최고 성능 VLM도 규칙 기반 baseline보다 낮아 현재 VLM의 한계를 드러냄.</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2609.40297'>GPU-Accelerated Path-Dependent Marginal Information Gain for Autonomous Exploration</a></td><td>50</td><td>7</td><td>Navigation</td><td>depth buffer로 경로 상 시야 중첩을 GPU에서 병렬 계산해 marginal information gain을 근사함. 최대 118배 가속하며 실제 탐사 시간을 30% 줄임.</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2609.39995'>Learning to Explain While Planning: Rule-Aligned Diffusion Planning for Autonomous Driving</a></td><td>50</td><td>6</td><td>Navigation</td><td>자율주행 diffusion planner에 미분가능 주행 규칙을 내재화하고 규칙별 기여도를 attribution으로 설명하는 RADP 제안, nuPlan closed-loop에서 안전 시나리오 개선 확인함</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2609.38588'>Drone Soccer: Learning to Manipulate with Multicopter Downwash</a></td><td>50</td><td>6</td><td>Manipulation</td><td>downwash를 방해물이 아닌 조작 도구로 적극 활용하는 드론 축구 과제를 제안함. 단순화된 동역학 모델로 RL 학습 후 실세계 전이까지 검증함.</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2609.38653'>TERRA: Terrain-Aware Reconstruction, Retargeting and Control for Musculoskeletal Locomotion</a></td><td>50</td><td>6</td><td>RL</td><td>지형 정보 없는 모션 데이터에서 terrain-aware retargeting으로 근골격 locomotion을 학습함. 9.4시간 데이터로 단일 정책을 비평탄 지형에 일반화함.</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2609.39105'>Occlusion-Aware, Quasi-Static, Stability-Oriented Trajectory Planning on Uneven Terrain</a></td><td>50</td><td>6</td><td>Navigation</td><td>지형 가림을 coverage 기반 epistemic uncertainty로 모델링해 off-road 경로계획에 반영함. 6개 야외 환경 실제 로봇 실험으로 실패율을 절반 이하로 줄임.</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2609.39378'>EgoTools: Towards Tool-Centric Reasoning in Real-World Egocentric Videos</a></td><td>50</td><td>5</td><td>Embodied AI</td><td>도구 사용 중심의 egocentric 추론을 다루는 EgoTools 데이터·벤치마크 제안임. affordance, hand-tool-object geometry, 절차적 진행을 포괄해 manipulation과 직결되는 reasoning을 측정하며 현재 모델의 한계도 구체적으로 드러냄</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2609.39588'>KilometerVision: A New Frontier for Large-Scale Spatial Intelligence in VLMs</a></td><td>50</td><td>5</td><td>Embodied AI</td><td>1km 규모 실제 비디오에서 지리적 레이아웃 이해를 평가하는 KilometerVision 벤치마크 제안임. VLM이 path integration 대신 2D 인식과 텍스트 매칭에 의존한다는 발견이 embodied spatial reasoning의 근본적 한계를 드러냄</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2609.38839'>FrameMorrow: Future-guided Frame Selection with Prospective Tokens for Long-Horizon Video Generation</a></td><td>50</td><td>4</td><td>World Model</td><td>현재가 아니라 미래 정보 필요성에 따라 과거 프레임을 선택하는 FrameMorrow 제안임. action-conditioned world model을 포함해 11개 생성 모델에 plug-and-play로 붙는 범용성이 있고 장기 일관성 개선폭도 구체적임</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2609.40358'>Physis-Lang: Self-Evolving Language as a Physical Representation for Video World Model</a></td><td>50</td><td>4</td><td>World Model</td><td>물리 과정을 설명하는 언어를 데이터 큐레이션·학습·생성 전반의 공유 표현으로 쓰는 Physis-Lang 제안임. assertion 단위 평가로 캡션을 자기진화시켜 물리적 타당성을 개선한다는 점이 world model의 물리 일관성 문제에 새로운 접근을 제시함</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2609.40035'>OPTS-TTPO: Enhancing Finite-Sample Policy-Gradient Learning with Tree Search</a></td><td>50</td><td>4</td><td>RL</td><td>on-policy tree search로 policy gradient의 희귀 고보상 경로 커버리지를 높이고 bias를 이론적으로 제어함. MuJoCo·Atari에서 PPO 대비 개선 확인됨</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2609.38377'>PhyProbe: Rethinking Physical Consistency Evaluation in Generated Videos</a></td><td>50</td><td>3</td><td>Video</td><td>생성 비디오의 물리적 일관성을 ranking과 regression을 결합해 평가하는 PhyProbe 제안임. world model 평가 지표로 쓸 수 있어 관련성 있으나 평가 방법론 자체의 novelty는 중간 수준임</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2609.38485'>Beyond Layers: Position-Resolved Gradient Conflict and Position-Aware Modulation for Unified Multimodal Models</a></td><td>50</td><td>0</td><td>Multimodal</td><td>unified multimodal model에서 이해-생성 gradient 충돌을 position 축으로 분해한 분석임. layer 기준 분석을 넘어선 축을 제시한 점이 새롭지만 로보틱스와는 거리가 있음</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2609.39304'>Scale and Selection: What Makes Automatic Harness Evolution Work for Visual-Interface Robot Agents</a></td><td>48</td><td>7</td><td>Embodied AI</td><td>로봇 harness를 다른 coding agent가 자동 개선하게 하고 rollout 수와 champion-challenger 선택이 핵심임을 밝힘. visual-interface 로봇 agent에서 held-out 성공률을 51%에서 67%로 높임.</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2609.39323'>HiWE: Hierarchical World Knowledge Model with Visual Keypoint Enhancement for Zero-Shot 3D Path Planning</a></td><td>48</td><td>7</td><td>VLA</td><td>point 기반 인터페이스로 visual grounding과 language planner를 연결해 zero-shot 3D path planning을 수행함. 14개 시뮬 과제와 4개 실로봇 과제로 검증함.</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2609.39594'>Neuro-Symbolic Predicate Learning for Semantic Safe Robot Control</a></td><td>48</td><td>7</td><td>RL</td><td>사람이 명시한 안전 규칙을 미분 가능한 reasoner로 학습해 해석 가능한 safety feature를 뽑아냄. 새 실로봇 안전 벤치마크 REASON을 함께 공개함.</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2609.38421'>A Reachability-based Safety Certificate for Dynamical System Motion Policies</a></td><td>48</td><td>6</td><td>Manipulation</td><td>backward reachability 기반 value function으로 DS motion policy의 안전성을 증명함. Franka 매니퓰레이터 검증으로 modulation·CBF의 saddle point 문제를 회피함.</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2609.39245'>ReWAM: Reciprocal World Action Models for Interactive Autonomous Driving</a></td><td>48</td><td>6</td><td>World Model</td><td>다른 agent를 world model의 단순 구성요소가 아닌 상호 반응하는 의사결정자로 모델링한 게임이론적 world-action model임. 상호작용이 밀집한 NAVSIM 시나리오에서 큰 개선을 보임.</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2609.39652'>Making Waves: A Membrane-Coupled Delta Array for Manipulating Objects Below the Actuator Spacing</a></td><td>48</td><td>6</td><td>Manipulation</td><td>delta robot array의 end-effector를 신축 막으로 연결해 actuator 간격보다 작은 물체도 조작 가능하게 함. 하드웨어 전이 성공률 76%로 검증함.</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2609.38536'>Does This Action Still Explain the Task? Reverse Scoring for Diffusion Language Model Agents</a></td><td>48</td><td>5</td><td>Embodied AI</td><td>diffusion LLM agent가 실패한 행동을 반복 재시도하는 현상을 masked decoding의 편향으로 설명하고 reverse conditional 평가로 교정하는 Reflect Reverse 제안임. 실패를 메커니즘 수준에서 규명하고 training-free로 고친다는 점이 failure detection·recovery 우선 주제와 직접 맞닿음</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2609.38733'>Code to Control: Synthesizing Parameterized Reactive Controllers</a></td><td>48</td><td>5</td><td>RL</td><td>LLM이 제어기 구조를 코드로 합성하고 derivative-free 탐색으로 파라미터를 맞춰 실시간 제어를 실현함. Atari·Flappy Bird·MuJoCo에서 PPO와 경쟁력 있고 환경 변화에도 전이됨</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2609.40129'>VR-JEPA: Learning Contrastive-State Latent Guidance for Generation-based Video Reasoning</a></td><td>48</td><td>4</td><td>World Model</td><td>V-JEPA predictor를 task-specific reasoning logic에 맞춰 contrastive-state로 정렬하는 VR-JEPA 제안임. latent 예측 기반 world model을 reasoning 신뢰도 향상에 연결한 시도가 흥미롭고 물리적 일관성 개선폭도 보고함</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2609.38755'>Agentic Relative Camera Pose Estimation via Learned Ranking and Verification</a></td><td>48</td><td>3</td><td>3D Vision</td><td>ranking agent와 verification agent로 여러 pose estimator를 동적으로 조합하는 PoseAgent 제안임. 서로 다른 estimator의 상보적 강점을 학습 기반으로 조율하는 설계가 실용적이고 SLAM류 로봇 인식에 참고 가치 있음</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2609.38810'>CRAFT: Causal Responsibility and Failure Tracing in Medical Vision Language Models</a></td><td>48</td><td>3</td><td>Multimodal</td><td>의료 VLM의 두 안전 실패(arbitration failure, brake failure)를 분리된 attention head 집합으로 국소화하고 인과적으로 검증하는 CRAFT 제안임. failure 메커니즘을 head 단위로 특정하고 개입까지 성공시킨 점이 failure detection/diagnosis 주제와 연결되지만 의료 도메인에 국한됨</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2609.39748'>FAST: Flow Any Scene Transformer</a></td><td>48</td><td>3</td><td>3D Vision</td><td>단일 뷰 foundation model의 query-key projection을 재사용해 cross-view correspondence를 확장하는 FAST 제안임. 전용 pair-centric pretraining 없이 scaling 이점을 그대로 가져온다는 점이 좋고 SLAM류 매칭에 활용 가능함</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2609.39785'>Seeing as Humans Do: Learning from Motion to Segment Anything Without Supervision</a></td><td>48</td><td>3</td><td>CV</td><td>비디오의 motion만으로 objectness prior를 학습해 SAM 수준 성능을 무라벨로 달성하는 MoSA 제안임. annotation 없이 scalable한 segment-anything 대안이라는 점에서 로봇 시각 전처리에 참고할 가치가 있음</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2609.40333'>I Have a Stream: Making Self-Supervised Learning Work on Continuous Video</a></td><td>48</td><td>3</td><td>CV</td><td>셔플 없이 연속 비디오 스트림에서 SSL을 성립시키는 StreamMAE 제안임. 95시간 보행 영상에서 intra-batch 유사성 문제를 밝히고 해결한 점이 embodied agent의 지속적 시각 경험 학습과 직접 연결됨</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2609.39154'>DAGent: Evaluate-then-Grow Planning for Deep Research Agents</a></td><td>48</td><td>2</td><td>NLP</td><td>DAG 기반 deep research agent에 evaluate-then-grow incremental planning 도입, NeurIPS 2026 accept. agent 설계는 흥미로우나 robotics 적용성 낮음</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2609.38426'>LoopVL: Recurrent Visual Intelligence</a></td><td>48</td><td>1</td><td>Multimodal</td><td>Loop Transformer를 VLM에 적용해 반복 연산으로 멀티모달 상태를 갱신하는 LoopVL 제안임. 처음부터 학습한 recurrent VLM이라는 점에서 구조적 novelty 있음</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2609.39151'>Linear Recurrent Memory Suffices to Distil a World-Model Policy for Robot Air Hockey</a></td><td>46</td><td>7</td><td>World Model</td><td>DreamerV3 teacher를 distill해 air hockey defence에 비선형 순환이 꼭 필요하지 않음을 보임. 메모리 필요 과제에서 최소 구조로도 충분함을 증명한 분석 연구임.</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2609.39305'>FORTE: Forecasting Occupancy for Spatiotemporal Risk-Aware Planning in Dynamic Environments</a></td><td>46</td><td>6</td><td>Navigation</td><td>점유지도 예측의 시공간 중첩·방향성을 활용해 명시적 물체추적 없이 경로를 선택함. latent diffusion 예측기로 기존 대비 큰 IoU·속도 개선을 보임.</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2609.39384'>RoboAssist: Interactive Human-Humanoid Planning for Long-Horizon Surgical Assistance</a></td><td>46</td><td>6</td><td>Embodied AI</td><td>사람 작업 상태와 로봇 작업열을 분리한 비대칭 표현으로 수술 보조 장기 계획을 갱신함. 안전장치 다층 구조는 있으나 대부분 시뮬레이션 시연 수준임.</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2609.39129'>Drape-Compatible Tool-Tip Localization for Hand-Held Laparoscopic Instruments via UWB Carrier-Phase Ranging and Trocar-Constrained Geometry</a></td><td>46</td><td>5</td><td>Manipulation</td><td>trocar 기하 제약으로 UWB carrier-phase 거리만으로 복강경 도구 끝단을 위치추정함. 실제 토끼 수술까지 검증한 참신한 센싱 방법임.</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2609.39183'>Aligning Thoughts with Answers: Probability Rewards to Tame Thinking Drift</a></td><td>46</td><td>4</td><td>Embodied AI</td><td>IoU 기반 RL에서 정답 박스를 맞혀도 추론 근거가 틀린 thinking drift를 확률 기반 보상으로 교정하는 Rita 제안임. visual intention grounding이라는 embodied 과제에서 reasoning-answer 일관성을 다룬 점이 눈에 띔</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2609.40195'>MemLife: Curating and Reasoning over Long-Term Egocentric Video Memories</a></td><td>46</td><td>4</td><td>Embodied AI</td><td>entity 기반 1인칭 텍스트 episode를 만들고 시간 인덱스 기반으로 검색하는 장기 egocentric memory 시스템 MemLife 제안임. RL로 memory writer를 직접 최적화하는 MemOpt까지 더해 robot memory 설계에 참고할 요소가 많음</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2609.39089'>UGOD: Uncertainty-Guided Opacity and Dropout for Sparse-View 3D Gaussian Splatting</a></td><td>46</td><td>3</td><td>3D Vision</td><td>Gaussian별 view-dependent uncertainty를 추정해 opacity를 조절하는 sparse-view 3DGS UGOD 제안임. 불확실성 기반 렌더링 제어라는 아이디어가 object-centric 3DGS 연구에 참고할 만함</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2609.38469'>The Backdrop Exposes What the World Around an Agent Costs It</a></td><td>46</td><td>3</td><td>NLP</td><td>다른 사람이 끼어들어 지시를 바꾸는 상황에서 디지털 agent의 안전성이 급락함을 보이는 벤치마크임. embodied agent의 권한·주입 공격 평가에 참고할 개념이나 물리 로봇은 아님.</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2609.38851'>Where MLLMs Fail and Why: Causal Task Decomposition for Capability Failure Diagnosis</a></td><td>46</td><td>3</td><td>Multimodal</td><td>전제조건 개입으로 MLLM 실패가 고유 결함인지 상위 단계 오류 전파인지 구분하는 인과적 분해 틀임. counterfactual 분석 방법론은 참고할 만하나 로봇 실험은 없음.</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2609.38444'>Audible World Models: Spatially Aware Sound Generation for 3D Worlds</a></td><td>46</td><td>2</td><td>World Model</td><td>텍스트로 생성한 3D 월드에 공간 음향을 붙이는 training-free 프레임워크임. semantic-geometry-sound를 명시적으로 연결하는 아이디어는 새롭지만 world model 본연의 동역학과는 거리가 있음</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2609.38592'>StereoGaussians: Feed-Forward 3D Gaussian Splatting from Stereo Images</a></td><td>46</td><td>2</td><td>3D Vision</td><td>stereo pair 한 장에서 metric 3DGS를 feed-forward로 예측하는 StereoGaussians 제안임. 로봇 스테레오 카메라 인식에 쓸 수 있으나 본 논문은 뷰 합성 품질에 초점임</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2609.39363'>Rethinking Multi-Image Re-Representation in Multi-Image Understanding</a></td><td>46</td><td>2</td><td>Multimodal</td><td>텍스트/비주얼 재표현을 비교하고 RL로 visual tool 조합을 학습하는 Mosaic·MosaicAgent 제안임. 정밀 시각 증거가 필요한 과제에서 visual re-representation이 더 유리하다는 결과가 분명하고 도구 사용을 RL로 유도한 점이 흥미로움</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2609.38329'>ExploreNet: Learning Where to Explore in Diffusion GRPO</a></td><td>46</td><td>1</td><td>RL</td><td>diffusion GRPO에서 탐색 노이즈 분포를 학습하는 ExploreNet 제안임. exploration이 학습 가능하다는 분석은 흥미롭지만 이미지 생성 한정이고 로봇 RL로의 전이는 불명확함</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2609.38777'>Distill the Visual Evidence, Not Just the Answer: Cross-World On-Policy Distillation for Vision-Language Models</a></td><td>46</td><td>1</td><td>VLM</td><td>두 시각적 세계를 대비시켜 teacher의 belief transition을 distill하는 CW-OPD 제안임. 학생이 실제 시각 근거에 반응하게 만드는 목표가 명확하고 CWBench로 검증함</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2609.39514'>Spike-driven Vision-Language-Action Model</a></td><td>45</td><td>7</td><td>VLA</td><td>최초의 spike-driven VLA로 LIBERO·Meta-World에서 경쟁력 있는 성능을 저전력으로 달성함. manipulation 적용이지만 경량화·효율 중심 기여라 novelty 가치는 제한적</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2609.40003'>DashVMC: Real-Time Discrete World Model Control in Geometry Dash</a></td><td>45</td><td>4</td><td>World Model</td><td>Geometry Dash 게임플레이로 action-conditioned world model을 학습하고 frozen rollout 안에서 BC+PPO로 제어기를 정제, 실시간 60Hz 제어 루프 구현이 흥미로우나 게임 환경 한정임</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2609.38578'>Retargeting Motions to Diverse Skeletons via Learnable Flattening</a></td><td>45</td><td>2</td><td>3D Vision</td><td>topology-invariant latent space를 학습해 임의 스켈레톤 간 motion retargeting을 하는 Transformer autoencoder임. zero-shot 오차 감소폭 크지만 humanoid 로봇 적용은 직접 다루지 않음</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2609.39490'>OmniReasoning: Pushing the Limits of Audio-Visual Joint Reasoning</a></td><td>45</td><td>2</td><td>Multimodal</td><td>오디오와 비주얼 증거가 둘 다 필요한 질문으로 구성된 OmniReasoningBench와 modality-factored self-distillation MFSD 제안임. omni-modal joint reasoning을 직접 끌어올린 점이 좋으나 로봇 응용은 제시하지 않음</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2609.38672'>Provable Test-Time Scaling for Beam Search in LLM Reasoning</a></td><td>45</td><td>2</td><td>LG</td><td>beam search의 test-time scaling 이론적 하한/상한 증명, NeurIPS급이나 LLM 추론 문제에 한정됨</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2609.38814'>Learning Chaos Without Seeing Chaos: Extrapolation of Global Dynamics in Autoregressive Transformers</a></td><td>45</td><td>2</td><td>LG</td><td>autoregressive transformer가 국소 관측만으로 카오스 동역학 전역 구조 외삽, 동역학 학습 일반화라는 점에서 world model과 개념적으로 연결되나 물리 시스템 식별 데모 수준</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2609.38487'>Multidimensional Observer Model and Perceptual Dimensions of Human Image Quality Assessment</a></td><td>45</td><td>0</td><td>CV</td><td>인간 이미지 품질 판단을 다차원 관찰자 모델로 설명하는 NeurIPS 논문임. 지각 공간이 task별로 저차원이라는 발견은 흥미롭지만 로보틱스 응용과는 무관함</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2609.40295'>How Much Is an AI Token Worth? Scaling Laws for Wild AI-Generated Web Text</a></td><td>45</td><td>0</td><td>LG</td><td>800개 모델을 학습시켜 AI 생성 웹텍스트가 pretraining에 미치는 효과를 새 scaling law로 모델링함. 데이터 규모와 분석이 탄탄하나 robotics와 무관</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2609.38371'>TALK-Dem: Benchmarking Embodied Task Planning under Dementia-Associated Communication Patterns</a></td><td>44</td><td>6</td><td>Embodied AI</td><td>치매 환자 발화 패턴 하에서 LLM 로봇 planner의 안전성 저하를 벤치마크함. CARE 방법으로 일부 개선하나 novelty는 제한적임.</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2609.38570'>Data-Efficient Adaptation of a Driving VLA to Class 8 Trucks</a></td><td>44</td><td>6</td><td>VLA</td><td>승용차용 VLA를 Class 8 트럭에 adapt-then-steer 전략으로 데이터 효율적으로 전이함. flow velocity steering으로 ADE/FDE를 추가 개선함.</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2609.38928'>Local-Minimum Escaper: Programmatic Subgoal Generation for Robust Navigation in Unknown Environments</a></td><td>44</td><td>6</td><td>Navigation</td><td>local observation만으로 해석 가능한 기준으로 subgoal을 생성해 local minima를 탈출함. 추가 학습 없이 두 종류 실로봇에서 검증함.</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2609.39558'>General Performance Guarantee for Human Torque Estimation-Based Task-Agnostic Assistive Exoskeleton Control</a></td><td>44</td><td>6</td><td>RL</td><td>human torque 추정 오차가 있어도 matched assistance 확률 하한을 보장하는 이론을 제시함. 실제 상지 exoskeleton으로 검증함.</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2609.39575'>ECHO-G: Embodied Co-speech Humanoid mOtion Generation</a></td><td>44</td><td>6</td><td>Embodied AI</td><td>음성과 타임드 transcript를 함께 조건화한 diffusion transformer로 humanoid co-speech motion을 생성함. 실제 humanoid 배포와 비디오 평가까지 포함함.</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2609.39898'>Active Mapping of Underwater Litter Using Camera-Sonar Fusion</a></td><td>44</td><td>6</td><td>Navigation</td><td>카메라-소나 융합 점유지도에서 entropy와 발견 가능성을 함께 고려한 next-best-view를 계산함. 시뮬레이터 검증만 있고 실해역 데이터는 없음.</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2609.40230'>EviRover: Reinforcing Agentic Perception Beyond a Glance</a></td><td>44</td><td>3</td><td>Multimodal</td><td>한 번의 glance로 부족한 지각을 상호작용으로 보완하는 agentic perception EviRover 제안임. perception under insufficient evidence를 명시적으로 정식화하고 RL로 학습시킨 설계가 active perception 연구와 통한다고 볼 수 있음</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2609.38334'>EVOKE: Eliciting World Knowledge in Agents for Transferable Decision-Making</a></td><td>44</td><td>3</td><td>World Model</td><td>같은 상태에서 다른 목표로 action 선호를 바꾸도록 강제해 LLM이 사전학습으로 내재화한 world knowledge를 끌어냄. 디지털 에이전트 대상이라 물리 world model과는 다르나 개념적으로 참고할 만함.</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2609.38519'>GazeFlow: From Human Gaze Behavior to Generative Egocentric Gaze Prediction</a></td><td>44</td><td>2</td><td>Embodied AI</td><td>flow matching으로 egocentric gaze를 top-down/bottom-up 조건부 생성하는 GazeFlow 제안임. active perception과 연결 가능하지만 직접적 로봇 적용은 없음</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2609.38900'>MEMO: Multi-Level Entity-Aware Memory for Streaming Video Understanding</a></td><td>44</td><td>2</td><td>Video</td><td>entity 단위 구조화 메모리로 스트리밍 비디오를 이해하는 training-free MEMO 제안임. 장기 기억 구조라는 점에서 robot memory 연구에 참고할 설계지만 직접 로봇 적용은 없음</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2609.39590'>SPOON: Towards Coherent Compositional 3D Scene Generation from Uncalibrated Multi-view Images</a></td><td>44</td><td>2</td><td>3D Vision</td><td>다중 view 기하를 이용해 물체 pose 가설을 장면 수준으로 조율하는 SPOON 제안임. Guide-Route-Reconcile로 object-camera soup 문제를 해소해 compositional 3D scene 생성 품질을 높임</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2609.40048'>CoEvoWhen: Policy-Tool Coevolution for Ultra-Long Video Temporal Grounding</a></td><td>44</td><td>2</td><td>Video</td><td>VLM 추론 궤적에서 policy와 tool을 함께 진화시키는 CoEvoWhen 제안임. 파라미터 업데이트 없이 재사용 가능한 skill을 만든다는 아이디어가 초장편 video temporal grounding에서 효과적임</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2609.40320'>Atomizer-IO: Beyond Pixels, Patches and Grids</a></td><td>44</td><td>2</td><td>CV</td><td>격자 가정을 없애고 관측을 물리적 관계로부터 구조화하는 Atomizer-IO 제안임. 원격탐사 입력부터 3D point cloud까지 구조 재설계 없이 확장되는 범용성이 눈에 띄지만 로봇 적용 실험은 없음</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2609.38332'>Hermes: Learning Contextual Reasoning Unlocks Test-Time Scaling</a></td><td>44</td><td>2</td><td>LG</td><td>context 할당과 재사용을 모델이 직접 결정하게 하는 Hermes·Hermes-Learn 제안임. test-time scaling 전략을 모델에 내재화한다는 점이 test-time optimization 우선 주제와 통하지만 로봇 추론이 아닌 LLM reasoning 벤치마크에서만 검증함</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2609.38368'>Composition, Not Conversation: VLMs Lose the Scene, Not the Thread</a></td><td>44</td><td>1</td><td>Multimodal</td><td>장면을 layer로 쪼갰을 때 VLM 성능이 급락한다는 진단 벤치마크임. evidence composition의 중요성을 잘 드러내지만 새 방법 제안은 없음</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2609.38413'>VidHarness: Evolving Agent Harnesses for Cost-Efficient Long Video Understanding</a></td><td>44</td><td>1</td><td>Video</td><td>MCTS로 video agent harness를 자동 설계하는 VidHarness 제안임. 프레임 예산 대비 성능 개선 폭 크지만 long video QA 한정 응용임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2609.40362'>Multimodal Flow: Unified Flow Modeling of Language and Vision in Embedding Spaces</a></td><td>44</td><td>1</td><td>Multimodal</td><td>언어와 비전을 모두 연속 embedding으로 다루는 통합 flow 모델 Multimodal Flow 제안임. quantization bottleneck을 피하는 아키텍처 선택이 흥미롭지만 로보틱스 응용은 제시되지 않음</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2609.40359'>Removing Timing Shortcuts Improves Non-Invasive Brain-to-Text</a></td><td>44</td><td>1</td><td>NLP</td><td>brain-to-text 디코딩에서 timing shortcut을 찾아내고 제거해 성능을 개선함. 방법론적 엄밀성은 높으나 BCI 연구라 로보틱스 연관 낮음.</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2609.38597'>PixelUMM: Encoder-Free Unified Image and Video Understanding and Generation</a></td><td>44</td><td>0</td><td>Multimodal</td><td>encoder 없이 pixel 단위로 이미지/비디오 이해와 생성을 통합하는 PixelUMM 제안임. 구조적 시도는 흥미롭지만 로보틱스와는 무관함</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2609.38465'>Does Gradient Conflict Predict the Understanding--Generation Trade-off? A Controlled Audit of Conflict-Metric Validity in Unified Multimodal Models</a></td><td>44</td><td>0</td><td>Multimodal</td><td>gradient conflict 완화가 실제로 understanding-generation trade-off를 개선하는지 통제 실험으로 검증한 연구임. conflict 지표가 상관관계를 보이지 않는다는 부정적 결과를 명확히 제시해 UMM 설계 가정에 경종을 울리지만 로보틱스와는 무관함</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2609.38405'>Draft: A Parametric Tool for Robot Design Exploration</a></td><td>42</td><td>6</td><td>RL</td><td>실제 액추에이터·로봇 데이터로 파라메트릭 설계를 구속해 CAD 없이 MJCF 모델을 생성함. 2단계 RL로 쿼드러페드 co-design trade-off를 보임.</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2609.40158'>Rethinking Legibility in Social Robot Hallway Navigation: Impact of Intent Representation and Human Distraction</a></td><td>42</td><td>6</td><td>Navigation</td><td>정적 관찰자용 legibility를 동적 보행자 복도 내비게이션으로 확장해 두 번의 사용자 연구를 진행함. passing-side 기반 적응적 legibility가 더 부드러운 사람 동작을 이끈다는 결과임.</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2609.38407'>Disagreement-Regularized Imitation Learning for Image-Based Continuous Control with Gaussian and Beta Policies</a></td><td>42</td><td>5</td><td>RL</td><td>disagreement를 보상으로 바꾸는 DRIL을 이미지 기반 연속 제어에 적용해 behavior cloning의 분포 밖 오차를 줄이는 연구임. imitation learning의 few-demonstration 상황에서 큰 개선폭을 보였으나 CarRacing 시뮬레이션에 한정된 검증임</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2609.38467'>L1-MPPI: L1 Adaptive Model Predictive Path Integral for Agile UAV Control</a></td><td>42</td><td>5</td><td>RL</td><td>L1 adaptive control을 MPPI에 cascade해 UAV 고속 추종 성능을 개선함. 하중 35% 증가 상황에서 RMSE를 크게 낮춤.</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2609.39098'>DiFF: Doppler-informed Flow Matching for Human Motion Flow</a></td><td>42</td><td>5</td><td>3D Vision</td><td>mmWave radar의 Doppler 속도 단서를 flow matching 사전으로 삼아 희소 포인트클라우드에서 비강체 motion flow를 추정함. HRI 인지 용도로 benchmark SOTA를 달성함.</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2609.39611'>Towards Agile Vision-Based Multi-UAV Flight: Revisiting State Estimation</a></td><td>42</td><td>5</td><td>Navigation</td><td>위치만 보던 상태추정에 tilt 정보를 더해 UAV 가속도 추정 지연을 없앰. closed-loop 실험에서 position-only 대비 큰 오차 감소를 보임.</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2609.39950'>Magnetic based In-situ Self 3D Pose Estimation for a Modular Soft Tendon-Driven Continuum Robot via IMU-Fusion</a></td><td>42</td><td>5</td><td>Manipulation</td><td>IMU와 능동 자기장을 융합해 외부 카메라 없이 soft continuum robot 형상을 추정함. 실제 closed-loop 제어로 16.7Hz 갱신을 검증함.</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2609.40102'>Passive Stiffness Shaping in Cable-Suspended Aerial Manipulation via Movable Compliant Anchors</a></td><td>42</td><td>5</td><td>Manipulation</td><td>cable-suspended aerial manipulation의 수동 강성을 anchor 재배치로 형상화하는 이론임. 해석적 모델만 제시하고 실비행 검증은 범위 밖임.</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2609.39969'>TACTIC: Temporal and Context-Aware LLM Tactical Planning for Roadside LiDAR Attacks</a></td><td>42</td><td>4</td><td>Navigation</td><td>MLLM이 교통 상황을 읽고 roadside LiDAR 공격 수단을 선택하는 시나리오 인지형 공격 프레임워크임. CARLA 280회 시험에서 100% 충돌률을 보여 AV 인지 취약점을 드러냄.</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2609.40285'>PivotOPD: Learning to Recover from Pivotal Mistakes in Multi-Turn Agents</a></td><td>42</td><td>4</td><td>Embodied AI</td><td>multi-turn agent의 pivotal mistake를 예방·복구하는 on-policy distillation임. failure detection/recovery 우선주제와 연결되고 ALFWorld 등 embodied-ish 환경에서 검증함</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2609.39096'>DeCoPrune: Efficient KV-Cache Pruning for Autoregressive Video Diffusion via Denoising Consistency</a></td><td>42</td><td>3</td><td>World Model</td><td>denoising 일관성 신호로 KV cache 토큰을 선별 pruning하는 DeCoPrune 제안임. autoregressive world model 추론 속도를 크게 올리지만 핵심은 효율화 기여임</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2609.39553'>EffGS: Efficient and High-Fidelity Gaussian Splatting</a></td><td>42</td><td>3</td><td>3D Vision</td><td>frequency-aware guidance와 localized densification으로 대규모 장면에서도 품질 저하 없이 3DGS를 가속하는 EffGS 제안임. object-centric 3DGS 연구의 우선 주제와 맞닿지만 기여 자체는 가속화 engineering 위주임</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2609.39841'>DyRAD: Radar Novel View Synthesis for Dynamic Driving Scenes</a></td><td>42</td><td>3</td><td>3D Vision</td><td>정적 배경과 추적된 동적 reflector로 range-azimuth-Doppler 텐서를 렌더링하는 DyRAD 제안임. analytic point-spread function으로 센서 확산을 분리해 자율주행 closed-loop 평가용 레이더 novel view synthesis를 크게 개선함</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2609.38673'>In-Distribution Imagination for Model-Based Offline Reinforcement Learning</a></td><td>42</td><td>3</td><td>RL</td><td>model-based offline RL에서 trajectory support로 rollout truncation, world model 활용 방법론이나 로봇 환경 실험 없음</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2609.38889'>VERA: Verifiable Feasibility Representations with Counterfactual Credit for Constrained Multi-Agent Control</a></td><td>42</td><td>3</td><td>RL</td><td>제약 multi-agent control에서 feasibility representation과 counterfactual credit 분리, SAGIN 네트워크 실험이고 counterfactual reasoning 우선주제와 연결됨</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2609.39473'>Beyond the Shadows of Plato&#x27;s Cave: Evaluating False Memory in Autonomous Agents via Counterfactual Reasoning</a></td><td>42</td><td>3</td><td>Embodied AI</td><td>counterfactual reasoning으로 agent의 false memory를 hidden state만으로 탐지하는 training-free 프레임워크임. robot memory·counterfactual reasoning 우선주제와 맞닿아 있으나 평가는 수학·코드·QA에 국한</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2609.38466'>PAMI: Part Anchored Motion for Text to Human-Object Interaction Generation</a></td><td>42</td><td>2</td><td>3D Vision</td><td>신체 부위별 투표로 human-object interaction을 생성하는 PAMI 제안임. contact recall 개선폭 크지만 manipulation 실제 적용보다는 애니메이션 생성 목적임</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2609.39147'>MindWorldBench: Evaluating Mental-State-to-Behavior Reasoning in Image-to-Video Generation</a></td><td>42</td><td>2</td><td>Video</td><td>믿음·욕구 같은 mental state에서 행동을 생성하는지 평가하는 MindWorldBench 제안임. 모델이 주관적 믿음 대신 객관적 세계 상태에 의존하는 Omniscient Bias를 밝힌 점이 흥미롭고 embodied 사회적 추론과 맞닿아 있으나 본 논문은 비디오 생성 평가에 그침</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2609.39566'>From Given to Gathered Evidence: Agentic Learning for Longitudinal Medical Reasoning</a></td><td>42</td><td>2</td><td>Multimodal</td><td>의료 기록과 영상에서 증거를 능동적으로 탐색하도록 훈련한 CASE 에이전트 제안임. evidence-seeking을 명시적으로 학습시키는 agentic RL 설계는 참고할 만하나 도메인은 종단적 의료 추론에 국한됨</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2609.39591'>Structural Limits of the Information-Theoretic Uncertainty Decomposition</a></td><td>42</td><td>2</td><td>LG</td><td>aleatoric/epistemic uncertainty 분해의 feasible 영역이 ensemble 크기에 따라 제한된다는 구조적 한계를 규명한 이론 연구임. epistemic collapse 현상을 설명하는 근거를 제공해 불확실성 추정 기반 failure detection 연구에 참고할 만함</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2609.38356'>Continual Learning of Dynamical Systems in Recurrent Neural Networks through Recyclable Unit Gating</a></td><td>42</td><td>2</td><td>LG</td><td>미사용 unit을 재활용하는 gating으로 RNN의 continual dynamical systems reconstruction을 하는 CRUG 제안임. forgetting 없이 이질적 동역학을 순차 학습한다는 결과가 로봇 동역학 모델의 continual learning에 참고할 가치 있음</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2609.38278'>Masked Swingers: Harnessing Data Augmentation to Advance Autoencoders for Self-Supervised Learning</a></td><td>42</td><td>1</td><td>CV</td><td>MAE에 dual augmentation과 CLS token 교환을 추가한 SSL 개선임. fine-grained transfer에서 큰 폭 개선 보이지만 world modeling 연결은 언급 수준에 그침</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2609.38347'>TrackFish3D: Self-Supervised 3D Tracking of Schooling Fish from Multi-view Videos</a></td><td>42</td><td>1</td><td>3D Vision</td><td>multi-view geometry를 pseudo-label로 쓰는 self-supervised 3D fish tracking임. geometry 기반 self-supervision 아이디어는 쓸만하지만 응용이 생태 모니터링에 국한됨</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2609.38819'>Future Video Generation Better Aligns with the Human Visual Cortex than Observed Video</a></td><td>42</td><td>1</td><td>CV</td><td>미래 프레임 생성 표현이 관찰 비디오 재구성 표현보다 시각피질과 더 잘 정렬된다는 fMRI 비교 연구임. 흥미로운 신경과학적 발견이나 로보틱스 응용은 제시하지 않음</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2609.39660'>BAM! Bayesian Anything Model: a foundation model for generative computational imaging</a></td><td>42</td><td>1</td><td>CV</td><td>operator-conditioned flow map으로 물리 인식 posterior sampling을 하는 경량 foundation model BAM 제안임. 몇 step만에 다양한 역문제에 일반화하는 설계가 참신하지만 응용 도메인은 영상 복원에 머무름</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2609.38348'>Function-Space Transformer with Adaptive Anchors</a></td><td>42</td><td>1</td><td>LG</td><td>입력에 따라 anchor 위치를 예측하는 적응적 연속 latent 표현 Function-Space Transformer 제안임. PDE와 이미지 분류 모두에서 성능을 보여 범용성 있는 기여지만 로봇 적용은 다루지 않음</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2609.40305'>Looped Diffusion Transformer</a></td><td>42</td><td>0</td><td>CV</td><td>denoising step 안에서 Transformer block을 반복 실행해 연산 깊이를 늘리는 Looped-DiT 제안임. 파라미터 대비 큰 성능 이득을 보이지만 이미지 생성에 국한된 기여임</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2609.38806'>Blackboard Intelligence Can Surpass Autoregressive on Globally Constrained Problems</a></td><td>42</td><td>0</td><td>NLP</td><td>diffusion LM의 confidence로 global constraint 문제 search 유도, 흥미로운 inference 패러다임이나 로보틱스 무관</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2609.38400'>GestAdapt: Workspace-Conditioned Co-Speech Gesture Generation for Humanoid Robots</a></td><td>40</td><td>5</td><td>Embodied AI</td><td>작업공간 제약을 반영한 humanoid co-speech gesture 생성 프레임워크임. 실로봇(Reachy2) 평가는 있으나 novelty는 중간 수준임.</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2609.38527'>Behavioral Persistence and Incomplete Functional Transfer of Co-evolved Communication in Evolutionary Robotics</a></td><td>40</td><td>5</td><td>Embodied AI</td><td>공진화된 통신 프로토콜을 2D 시뮬에서 실제 e-puck으로 직접 전이해 부분적 실패를 보고함. sim-to-real 전이 한계를 보여주는 부정적 결과 연구임.</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2609.38824'>PhaseSync-Exo: Human Clock Anchored Reference Adaptation for Dynamic Gait Tracking</a></td><td>40</td><td>5</td><td>RL</td><td>사람의 보행 리듬에 맞춰 exoskeleton reference를 적응시키는 human-clock anchor를 제안함. 시뮬레이션 420회 모두 낙상 없이 완료함.</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2609.39596'>MVP-SLAM: Multi-Camera Visual-Inertial Floorplan-Prior SLAM</a></td><td>40</td><td>5</td><td>Navigation</td><td>평면도 사전 정보를 온라인으로 벽 매칭해 드리프트를 보정하는 visual-inertial SLAM임. 건설현장 SLAM 챌린지에서 상위권 성적을 보임.</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2609.40012'>Identifiable Decomposition of Submovements in Human Hand Trajectories</a></td><td>40</td><td>5</td><td>RL</td><td>primitive 간 상관관계를 기준으로 submovement 식별 가능성을 판정하는 정규화 회귀 방법임. 모호할 때 이를 명시적으로 알린다는 점이 novelty이며 imitation learning 분석에 활용 가능함.</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2609.38903'>DAMPER: Return-Prioritized Gradient Control for Smooth Policies</a></td><td>40</td><td>4</td><td>RL</td><td>actor-critic의 action 진동 억제를 gradient projection으로 해결, continuous control 배포 시 실질적 문제이나 표준 RL 벤치마크에 한정</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2609.39960'>Reconstructing the Dynamic World: A Representation-Centric View of 4D Scene Reconstruction</a></td><td>40</td><td>3</td><td>3D Vision</td><td>4D scene reconstruction 방법들을 표현·시간 모델링·파이프라인 관점에서 정리한 서베이임. object-centric 4D representation 연구 동향을 잘 정리했지만 새 방법 제안은 없음</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2609.38877'>On Parameters of Nonlinear Scalar Dynamics from Video: Invariants, Calibration, and Identifiability</a></td><td>40</td><td>3</td><td>CV</td><td>영상에서 비선형 스칼라 동역학 파라미터 식별가능성 이론, pendulum/free-fall 실험으로 물리 추론과 연결되나 로봇 조작 맥락은 아님</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2609.39547'>Learning Reliable GUI Agents under Imperfect Priors</a></td><td>40</td><td>3</td><td>Embodied AI</td><td>불완전한 사전지식 하에서도 신뢰도를 평가하며 동작하는 GUI agent 학습 프레임워크, 디지털 환경 embodied agent로 물리 로봇은 아니지만 exploration·noise-robust 학습 아이디어가 관련됨</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2609.40149'>Role-Adaptive Policy Optimization for Offline Reinforcement Learning</a></td><td>40</td><td>3</td><td>RL</td><td>TD3+BC/IQL의 역할 분리로 offline RL 개선함. D4RL 벤치마크 수준의 incremental 개선임.</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2609.38362'>Inductive Visual Logic for Few-Shot Out-Of-Distribution Adaptation in VLMs</a></td><td>40</td><td>1</td><td>VLM</td><td>VLM의 묘사 능력을 이용해 distant OOD에서 training-free few-shot 분류를 하는 IVL 제안임. ECCV accept. 아이디어는 명확하나 적용 범위가 분류 태스크로 제한적임</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2609.38349'>MILO: Automated Harness Discovery via Orchestrated Multi-Agent Evolution</a></td><td>40</td><td>1</td><td>LG</td><td>agent harness와 그 탐색 전략을 함께 진화시키는 MILO 제안임. 코딩·터미널 벤치마크에서 기존 탐색법을 크게 능가해 agentic 시스템 설계에 일반적으로 참고할 만함</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2609.38446'>What Pretraining and Midtraining Make Learnable from Rewards?</a></td><td>40</td><td>1</td><td>LG</td><td>pretraining·midtraining이 보상 학습에 필요한 연산을 어떻게 공급하는지 분석한 연구임. source observation이 모호성을 해소한다는 메커니즘 규명이 흥미롭지만 로보틱스 응용 실험은 없음</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2609.39441'>CAST: Causal Advantage-Structured Training with Spatially Grounded Compositional Rewards for Diffusion Models</a></td><td>40</td><td>0</td><td>CV</td><td>SDE 윈도우를 denoising trajectory에서 결정하고 장면 그래프 atom 단위로 보상을 주는 CAST 제안임. diffusion RL fine-tuning 설계가 정교하지만 이미지 생성 품질 개선에 국한됨</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2609.38374'>Doc2LoRA Provides Decodable Representations of Scientific Ideas</a></td><td>40</td><td>0</td><td>NLP</td><td>논문을 LoRA adapter로 표현해 벡터 혼합으로 새 아이디어를 질의 가능한 LLM으로 바꿈. 창의적이나 과학 문헌 검색·생성 도구로 robotics와는 무관함.</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2609.38972'>Making LLMs Say What They Think: Measuring and Improving CoT-Interpretability Alignment</a></td><td>40</td><td>0</td><td>NLP</td><td>CoT가 내부 계산을 실제로 반영하는 정도를 측정하고 보상으로 개선함. LLM 해석가능성·신뢰성 연구임.</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2609.38707'>Residual Wrench Certification and Margin-Aware Control Synthesis for Aerial Physical Interaction</a></td><td>38</td><td>5</td><td>Manipulation</td><td>다중로터 접촉 작업시 잔여 wrench 여유를 convex geometry로 인증함. 제어 이론 중심이라 학습 기반 기여는 없음.</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2609.40269'>Belief-Aware Multi-Agent Path Finding under Map Uncertainty</a></td><td>38</td><td>5</td><td>Navigation</td><td>공간 상관된 장애물 불확실성을 Gaussian belief propagation으로 추론해 MAPF 재계획 비용을 줄인 방법임. 800 에이전트 규모까지 검증한 멀티로봇 경로계획 기여</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2609.38472'>Diffusion-2BC: Hybrid Diffusion and Regression Training for Offline Behavior Cloning in Autonomous Driving</a></td><td>38</td><td>4</td><td>RL</td><td>diffusion denoising과 BC 보조 손실을 결합한 자율주행 behavior cloning임. CARLA 평가에서 multimodal 행동을 유지하며 안정성 개선함.</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2609.38862'>Efficient Multi-Modal Planning with Reward-Guided Preference Optimization for Autonomous Driving</a></td><td>38</td><td>4</td><td>Navigation</td><td>sparse anchor와 reward-guided fine-tuning으로 자율주행 경로 계획 효율을 높임. NAVSIM에서 정확도-효율 균형을 보이는 incremental 개선임.</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2609.39125'>LBDU-VIO: Learned Bias Dynamics and Uncertainty for Visual-Inertial Odometry with Unreliable Vision</a></td><td>38</td><td>4</td><td>Navigation</td><td>neural ODE로 연속시간 IMU bias 동역학을 학습해 MSCKF를 보강함. 실제 benchmark에서 오차를 줄이나 odometry 보정 수준의 기여임.</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2609.39637'>Prediction is Better than Detection: Traffic Congestion Control using Drones</a></td><td>38</td><td>4</td><td>RL</td><td>fleet 크기보다 예측 정확도가 교통정체 완화에 더 크게 기여함을 드론 시뮬레이션으로 보임. multi-robot persistent monitoring의 일반 원칙 제시이나 embodied 조작과는 거리 있음.</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2609.40085'>BatSLAM 2.0: Sequence-Verified Sonar Place Recognition in a Robust Pose Graph</a></td><td>38</td><td>4</td><td>Navigation</td><td>echolocation 기반 SLAM에 sequence verifier를 추가해 loop closure 오판으로 인한 지도 붕괴를 막음. 니치한 음향 센서 SLAM 연구임.</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2609.40325'>WorldAuditBench: Interactive 3D World Auditing with Multimodal Agents</a></td><td>38</td><td>4</td><td>Embodied AI</td><td>3D 환경에서 이상을 찾기 위해 행동(탐색)과 시각추론을 결합하는 멀티모달 agent 벤치마크임. active perception과 맥락이 닿으나 현재 성능은 사람보다 크게 낮음</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2609.38805'>Explicit Trajectory Diversity for RL-Based Post-Training of LLM Agents</a></td><td>38</td><td>3</td><td>RL</td><td>LLM agent RL post-training에서 explicit trajectory diversity 유도, Sokoban/ALFWorld embodied 벤치마크 사용함</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2609.38932'>EFormer: Temporally Aligned Local Correction for Continuous sEMG-Based Hand Pose Tracking</a></td><td>38</td><td>3</td><td>CV</td><td>sEMG로 연속 손 자세 추적하는 residual correction network, 웨어러블 HCI 응용이고 로봇 손 제어에 참고 가능하나 직접 로봇 실험은 아님</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2609.39082'>Shared Phase and Retention Control for Efficient Adaptive Spectral Recurrence</a></td><td>38</td><td>3</td><td>RL</td><td>공유 스칼라 신호 두 개로 spectral memory의 retention/phase를 제어하는 SPARC, POPGym·continuous control에서 성능 개선 확인함</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2609.39306'>ReSAIL: Mitigating Collapse in Iterative Agent Self-Distillation</a></td><td>38</td><td>3</td><td>Embodied AI</td><td>반복적 agent self-distillation의 성능 붕괴를 informative step 선별로 완화, ALFWorld·TextCraft embodied 텍스트 에이전트 벤치마크 사용함</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2609.38637'>Template-Search Domain Adaptation via Multi-Stage Feature Alignment for Cross-Modal Object Tracking</a></td><td>38</td><td>2</td><td>CV</td><td>template과 search frame의 modality가 다른 cross-modal tracking에 domain adaptation을 적용한 TSDA-Track 제안임. UAV tracking까지 검증했으나 novelty는 feature alignment 조합 수준임</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2609.39127'>How to Reduce Localization Ambiguity? Geometry-Semantic Constrained BEV Representation Learning for Satellite-Ground Localization</a></td><td>38</td><td>2</td><td>Navigation</td><td>radial depth와 height supervision으로 BEV 위치 모호성을 줄이는 GeoSem-BEV 제안임. 위성-지상 localization 오차를 크게 줄였고 navigation 관련성 있으나 자율주행 중심 벤치마크임</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2609.40037'>Enhancing Autoregressive Video Generation via Representation Adversarial Distillation</a></td><td>38</td><td>2</td><td>World Model</td><td>frozen visual foundation model 특징 공간에서 적대적 학습으로 autoregressive video generation을 distill하는 Radian 제안임. 장기 rollout에서의 품질 저하 문제를 다루지만 핵심은 생성 품질 개선에 머무름</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2609.38598'>Reinforcement Learning with Complex (valued) Memories</a></td><td>38</td><td>2</td><td>RL</td><td>복소수 recurrence로 POMDP RL 메모리 개선, continuous control 성능 향상 보이나 rocksample/Craftax 등 toy 환경 중심임</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2609.38893'>Learning Continuous Neural Representation of Stochastic Hybrid Systems</a></td><td>38</td><td>2</td><td>LG</td><td>stochastic hybrid system을 고차원 잠재 SDE로 근사하는 이론, contact 동역학 같은 hybrid system 모델링에 참고될 수 있음</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2609.39247'>Trust the Critic More</a></td><td>38</td><td>2</td><td>RL</td><td>action chunk 단위로 critic 기반 credit assignment해 terminal rollout 필요성 제거, LLM RL 효율화이나 credit assignment 아이디어는 로봇 RL에도 적용 가능</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2609.39111'>Bongard: Training Machine Intuition</a></td><td>38</td><td>2</td><td>Multimodal</td><td>System One 직관 모델 학습 프레임워크임. decision benchmark 성능은 괜찮지만 robotics·embodied와 직접 연결 약함</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2609.39406'>Inferring Causal Relations between Two Sequences of Events with Language Models</a></td><td>38</td><td>2</td><td>NLP</td><td>단일 관측만으로 두 이벤트 시퀀스 간 인과관계를 LLM으로 추론하는 방법임. causal reasoning 우선주제와 연결되나 로봇 적용은 아직 없음</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2609.38979'>Mitigating Object Hallucination in Large Vision-Language Models via False Discovery Controlled Visual Data Splitting</a></td><td>38</td><td>1</td><td>Multimodal</td><td>mirror statistics로 false discovery rate를 제어해 LVLM object hallucination을 줄이는 CORAL 제안임. 통계적 근거를 갖춘 training-free 방법이라는 점은 좋으나 로보틱스 응용은 제시되지 않음</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2609.38985'>MeshOctave generates meshes via cascading resolution transitions</a></td><td>38</td><td>1</td><td>3D Vision</td><td>dyadic 공간 해상도로 scale을 정의해 병렬 생성 가능한 메시 생성 MeshOctave 제안임. 시뮬레이션 asset 생성에 쓸 수 있으나 직접적 로봇 응용은 없음</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2609.39120'>Is Better Teacher Supervision Enough? Unlocking Student-side Learning in Multimodal On-Policy Distillation</a></td><td>38</td><td>1</td><td>Multimodal</td><td>학생의 지각 능력 부족을 on-policy distillation의 병목으로 지목하고 teacher-calibrated contrast로 보완하는 S-OPD 제안임. 멀티모달 distillation 개선으로 로보틱스 연관성은 낮음</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2609.39142'>When Can Text Replace Vision? Structural Bottlenecks in Diagram Reasoning</a></td><td>38</td><td>1</td><td>Multimodal</td><td>텍스트화된 구조가 다이어그램 추론에 충분한지 진단하는 프로토콜 제안임. 구조 추출 오차와 solver 활용 능력을 분리한 분석이 깔끔하지만 로보틱스 응용은 제시하지 않음</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2609.38195'>A Data-Free Physics-Informed Neural Operator for Level-Set Interface Advection</a></td><td>38</td><td>1</td><td>LG</td><td>라벨 없이 물리 잔차만으로 level-set 계면 이류를 학습하는 data-free neural operator 제안임. eikonal 제약이 성립하는 영역에서 물리 기반 학습의 이점을 분석한 점이 흥미롭지만 응용이 유체 계면에 국한됨</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2609.39243'>Right Answer, Wrong Mechanism: Detecting Pernicious Divergence in Causal Interventions</a></td><td>38</td><td>1</td><td>NLP</td><td>causal intervention이 숨겨진 경로를 통해 잘못된 메커니즘으로 정답을 내는 현상 탐지, mechanistic interpretability 연구이고 counterfactual reasoning과 연관되나 LLM 한정임</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2609.39632'>Towards Better Exploration in Sequential Test-Time Scaling</a></td><td>38</td><td>1</td><td>NLP</td><td>sequential test-time scaling이 attractor에 갇히는 현상 분석 및 model-mixing 해법 제시, test-time optimization 우선주제와 개념적으로 연결되나 LLM reasoning 한정</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2609.38718'>MetaSteer: Context-Conditioned, nonlinear Steering via Attention-Projection Adaptation</a></td><td>38</td><td>1</td><td>NLP</td><td>attention projection에 context 의존적 비선형 steering을 적용해 선형 개념 가정을 벗어남. VLA policy steering과 개념적으로 유사하나 텍스트 생성 한정임.</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2609.38809'>StateTree: Enhancing Long-Term Dialogue Reasoning via Reinforcement Learning</a></td><td>38</td><td>1</td><td>NLP</td><td>세션에 흩어진 key-value를 트리 구조로 추적하게 하는 RL 보조과제로 장기 대화 추론을 개선함. memory 설계 개념이나 대화 한정임.</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2609.38997'>Settle: Learning When to Stop Reasoning</a></td><td>38</td><td>1</td><td>NLP</td><td>답이 안정된 시점을 학습해 추론을 조기 종료하는 방법임. test-time 효율화 개념이나 LLM reasoning 한정임.</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2609.39069'>CORE: Conflict-Oriented Reasoning Elimination for Verifiable Language-Model Search</a></td><td>38</td><td>1</td><td>NLP</td><td>검증기가 찾은 conflict core로 최신 결정 지점까지만 backjump하는 탐색 제어기임. 탐색 알고리즘 효율화로 로봇 planning 일반론에 참고 가능함.</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2609.39102'>False Frontiers: Diagnosing and Mitigating Co-Cheating in Self-Evolving Search Agents</a></td><td>38</td><td>1</td><td>NLP</td><td>proposer와 solver가 같은 오류에 합의해 내부 보상만 오르는 co-cheating을 진단하고 cross-fitted 검증으로 완화함. self-evolving loop의 실패 진단이라는 점이 로봇 self-improvement 연구와 유사한 구조임.</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2609.38541'>ThinkV2V: Unleashing the Reasoning Capability of MLLMs for Instruction-Guided Video Editing</a></td><td>38</td><td>0</td><td>Video</td><td>MLLM reasoning을 video editing에 결합한 ThinkV2V 제안임. editing 품질 개선 위주라 로보틱스와 무관함</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2609.38691'>No Corners Cut: State-Grounded Transitions for Mid-Stream Prompt Switches in Video Generation</a></td><td>38</td><td>0</td><td>Video</td><td>스트리밍 비디오 생성에서 프롬프트 전환 시 중간 상태를 명시적으로 거치게 하는 SEGUE 제안임. 비디오 생성 품질 개선이 목적이고 로보틱스와는 거리가 있음</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2609.39573'>Steering Fields: Adaptive Vector Fields for Safe Image Generation and Beyond</a></td><td>38</td><td>0</td><td>Generative Models</td><td>매 denoising step마다 조향 방향을 재추정하는 Steering Fields 제안임. 안전한 이미지 생성과 구조 보존 편집이 목적이라 로보틱스와 무관함</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2609.39635'>SAGE: Salient Factor Discovery and Generation with Visual Foundation Representations</a></td><td>38</td><td>0</td><td>CV</td><td>frozen representation autoencoder의 latent에서 salient/common factor를 분리해 subtype을 발견하는 SAGE 제안임. contrastive analysis 응용이 참신하지만 로보틱스와는 무관함</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2609.38360'>On the Off-Policy Teacher in On-Policy Distillation</a></td><td>38</td><td>0</td><td>LG</td><td>학생이 생성한 prefix에 teacher가 잘 이어지도록 RL로 재적응시키는 SCOUT 제안임. on-policy distillation의 비대칭 문제를 지적하고 개선하지만 LLM reasoning 영역에 국한됨</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2609.38393'>Which Tasks Survive Self-Supervised Learning?</a></td><td>38</td><td>0</td><td>LG</td><td>same-instance SSL이 어떤 downstream task를 보존하는지 spectral 관점에서 규명한 이론 연구임. 일반적 통찰이지만 로보틱스 응용은 다루지 않음</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2609.38526'>Revisiting scaling laws for reward optimization</a></td><td>38</td><td>0</td><td>LG</td><td>proxy reward 데이터량과 KL budget에 따른 reward optimization scaling law를 정밀화한 연구임. RLHF 이론 기여로 로보틱스와는 거리가 있음</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2609.38764'>Lasting Effects of Abstract Pretraining Beyond Perplexity</a></td><td>38</td><td>0</td><td>LG</td><td>abstract stack 과제로 LLM pretraining warmup하면 multi-hop QA 개선, 흥미로운 발견이나 로보틱스 무관</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2609.39078'>Parameter symmetries determine representational geometry in overparameterized nonlinear networks</a></td><td>38</td><td>0</td><td>LG</td><td>과매개변수 네트워크의 parameter symmetry가 representational geometry를 결정한다는 이론, NeurIPS급 기초 연구이나 로보틱스 적용 없음</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2609.38832'>Scaling Parameter and Context in Attention: Native Sparse Attention from Mixture-of-Head</a></td><td>38</td><td>0</td><td>LG</td><td>head마다 토큰을 나눠 할당해 attention 파라미터 확장이 곧 context 확장으로 이어지게 하는 구조임. LLM 아키텍처 효율화 연구임.</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2609.38829'>Diversity Combining for Multi-Path LLM Reasoning</a></td><td>38</td><td>0</td><td>NLP</td><td>multi-path reasoning을 무선통신 diversity combining 문제로 재정식화해 self-consistency 포화를 설명함. NeurIPS 2026 accept, 이론적 틀이 참신함</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2609.38437'>Embodiment-aware control by inference over the operator: a simulation study</a></td><td>36</td><td>5</td><td>Embodied AI</td><td>gaze·pupil 신호로 operator의 embodiment를 추론하는 active inference 컨트롤러임. 시뮬레이션 300명 대상 연구로 실제 사람 검증은 없음.</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2609.38463'>TrafficSignBench: Rule-Centric Closed-Loop Evaluation of Traffic-Sign Compliance in Autonomous Driving</a></td><td>36</td><td>3</td><td>Navigation</td><td>표지판 규칙 준수를 평가하는 자율주행 closed-loop 벤치마크임. 29000개 장면으로 규모는 크나 로봇 학습 자체의 기여는 아님.</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2609.39021'>Frame Differential On-Policy Self-Distillation for Video Reasoning</a></td><td>36</td><td>1</td><td>Video</td><td>dense frame 관측 정보를 sparse frame policy로 self-distill하는 FD-OPSD 제안임. video reasoning RL 학습 효율화 기여임</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2609.39504'>PartiCam: Camera Controlled Video Generation with Reward Guidance</a></td><td>36</td><td>1</td><td>Video</td><td>particle filtering으로 카메라 궤적 준수를 안정화하는 training-free PartiCam 제안임. 카메라 제어 영상 생성이 목적이라 로보틱스 직접 응용은 아님</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2609.39563'>RESUME: Recurrent State Updates from Motion and Residual Signals for Efficient Video Language Modeling</a></td><td>36</td><td>1</td><td>Video</td><td>코덱의 motion vector와 residual을 상태로 누적해 VideoLM 토큰을 만드는 RESUME 제안임. 긴 비디오 효율 처리에 유용하나 로보틱스 직접 응용은 없음</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2609.39709'>BTC3D: Blended Tile Conditioning for Detail-Enhancing Image-to-3D Generation</a></td><td>36</td><td>1</td><td>3D Vision</td><td>타일 단위 지역 조건화로 image-to-3D의 detail attenuation을 완화하는 training-free BTC3D 제안임. 3D 에셋 품질 개선 기여로 로보틱스 직접 응용은 제한적임</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2609.40079'>LongEmo: Towards Emotion Understanding and Reasoning in Long Videos</a></td><td>36</td><td>1</td><td>Video</td><td>사건 그래프 기반 memory로 장시간 비디오의 감정을 추론하는 LongEmo 제안임. 장기 memory 설계는 참고할 만하나 응용이 감정 이해에 국한됨</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2609.40253'>ComputerSD: Online Self-Distillation from Real-Time Feedback for Computer-Use Agents</a></td><td>36</td><td>1</td><td>Multimodal</td><td>GUI 전환 피드백을 토큰 단위 self-distillation 신호로 바꾸는 ComputerSD 제안임. computer-use agent 온라인 학습 기여로 로보틱스 직접 적용은 아니지만 agentic RL 설계는 참고할 만함</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2609.40347'>Image Classifiers are Efficient Self-Supervised Video Representation Learners</a></td><td>36</td><td>1</td><td>Video</td><td>비디오를 super image로 표현해 이미지 ViT를 비디오 SSL에 재사용하는 VideoMSN 제안임. 사전학습 효율이 크게 개선되지만 로보틱스 직접 응용은 없음</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2609.38506'>Autoregressive Frontier Expansion: Growing Trees with Graph Machine Learning</a></td><td>36</td><td>1</td><td>LG</td><td>SO(2) equivariant GNN과 flow matching으로 나무형 구조를 반복 확장 생성하는 방법 제안임. 생물학적 성장 과정을 모사하는 생성 설계가 참신하지만 신경·식물 형태 생성에 국한됨</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2609.38593'>Prompt2Skill: Unsupervised Skill Optimization From Natural Language Instructions</a></td><td>36</td><td>1</td><td>NLP</td><td>자연어 설명만으로 데이터셋을 찾거나 합성해 skill을 closed-loop로 다듬는 프레임워크임. 로봇 skill library와는 다른 LLM agent skill 연구임.</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2609.38604'>Beyond Oracle Communication: Benchmarking Interactive Intent Alignment Under Miscommunication and Evolving User Intent</a></td><td>36</td><td>1</td><td>NLP</td><td>의사소통 오류와 목표 변화가 있는 상황에서 사용자 의도 추적을 평가하는 벤치마크임. HRI 지시 추종에 개념적으로 참고 가능함.</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2609.38812'>Can Terminal Agents Trust Their Own Verification? Diagnosing and Improving Self-Verification</a></td><td>36</td><td>1</td><td>NLP</td><td>terminal agent가 정답 후보를 만든 뒤 검증·수정에 실패하는 지점을 진단하고 distillation으로 보완함. self-verification 개념은 로봇 failure recovery와 유사하나 코딩 에이전트 한정임.</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2609.38607'>After a Decade: Bringing Shadow Removal into the Real World with Agentic Training Data</a></td><td>36</td><td>0</td><td>CV</td><td>agentic workflow로 그림자 제거용 paired 데이터를 자동 생성하는 AgenticShadow 제안임. 데이터 구축 방법론은 실용적이나 로보틱스와 무관함</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2609.39222'>DC-SAE: Deep Compression Semantic Autoencoder for Faster Diffusion Convergence</a></td><td>36</td><td>0</td><td>CV</td><td>semantic encoder와 pixel encoder를 분리해 고압축 diffusion autoencoder의 수렴을 빠르게 하는 DC-SAE 제안임. 이미지 생성 효율화 기여로 로보틱스와 무관함</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2609.39625'>D-Scope: Decomposing and Steering Diffusion Transformers with Sparse Autoencoders</a></td><td>36</td><td>0</td><td>CV</td><td>SAE feature를 시각적 증거와 연결해 diffusion transformer를 해석·조향하는 D-Scope 제안임. 생성모델 해석가능성 연구로 로보틱스와 무관함</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2609.39920'>MCD: Causal Distillation of Multimodal In-Context Learning in Large Vision-Language Models</a></td><td>36</td><td>0</td><td>Multimodal</td><td>토큰 개입으로 인과적 증거를 식별해 ICL을 distill하는 MCD 제안임. distillation 방법론 개선으로 로보틱스와는 거리가 있음</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2609.38342'>Activation-Conditioned Self-Distillation</a></td><td>36</td><td>0</td><td>LG</td><td>정답에 도달한 궤적과 그렇지 않은 궤적의 activation 대비로 steering vector를 뽑는 ACSD 제안임. LLM reasoning self-distillation 개선 기여로 로보틱스와는 거리가 있음</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2609.38205'>The System Prompt Illusion: How Instruction Preambles Modify Computation in Language Models</a></td><td>36</td><td>0</td><td>NLP</td><td>system prompt가 layer별로 어떻게 표현을 바꾸는지 CKA로 분석함. safety instruction은 깊이 작동하지 않는다는 흥미로운 해석가능성 결과이나 robotics와 무관함.</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2609.38760'>HALO: Heterogeneous Allocation Via Localized Observations for the Vehicle Routing Problem</a></td><td>35</td><td>4</td><td>RL</td><td>부분 관측 환경에서 heterogeneous GNN으로 VRP 할당과 라우팅을 분리함. 분산 fleet 제어 문제로 manipulation·VLA와는 거리 있음.</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2609.40208'>Centralized Multi-UAV Exploration and 3D Reconstruction Using Single-UAV Planners</a></td><td>35</td><td>4</td><td>Navigation</td><td>단일 UAV 탐사 planner를 공유 TSDF 맵으로 다중 UAV에 확장하는 시스템 통합 연구임. 알고리즘 자체의 novelty보다는 엔지니어링 기여임.</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2609.38737'>AIfred: Augmented Learning through Functional Robotic Embodiment at the Desk</a></td><td>35</td><td>3</td><td>Embodied AI</td><td>로봇팔 끝에 프로젝터를 달아 손글씨 작업 옆에 AI 가이드를 투사함. 사용자 연구는 있으나 학습 알고리즘 기여는 적음.</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2609.38891'>Consistent Plan-Act for Long-Horizon Agentic Tasks</a></td><td>35</td><td>3</td><td>RL</td><td>planner-actor 간 상태 불일치를 탐지·교정해 long-horizon agent 성능을 높임. TAMP류 planner-actor 조율 문제와 맥락이 닿아 있음</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2609.39382'>SkillFM: Generating Skills for LLM Agents via Latent Flow Matching</a></td><td>35</td><td>3</td><td>Embodied AI</td><td>텍스트 skill을 latent flow matching으로 바로 생성해 retrieval 없이 agent에 제공함. ALFWorld 등 embodied task에서 검증함</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2609.38476'>Curating Synthetic Data for Task-Specific Visual Perception</a></td><td>35</td><td>2</td><td>CV</td><td>synthetic data curation 접근을 정리한 position paper임. 새 방법 제안 없이 기존 패러다임을 분류하는 수준이라 임팩트 제한적임</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2609.39093'>Learning Infinite-Horizon Average-Reward CMDPs via State Augmentation</a></td><td>35</td><td>2</td><td>RL</td><td>무한수평 평균보상 제약 MDP에서 state augmentation으로 최초의 효율적 sqrt(T) regret 알고리즘 제시, 제약 RL 이론으로 safety RL에 참고 가능</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2609.39436'>From Imitation to Reward Discovery: On-Policy Warmup for Agentic RL</a></td><td>35</td><td>2</td><td>RL</td><td>on-policy distillation을 agentic RLVR의 warmup으로 쓰는 On-Policy Warmup 제안, IL에서 RL로의 전이라는 점에서 로봇 학습 파이프라인과 개념적으로 연결되나 텍스트 에이전트 한정</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2609.39634'>Free Everywhere, Exact on Trees: PPO&#x27;s Dropped Correction Buys Sample Efficiency Under Aggressive Reuse</a></td><td>35</td><td>2</td><td>RL</td><td>PPO의 생략된 state-visitation 보정을 history-injective 구조에서 정확히 복원하는 이론, 정책최적화 일반 기여이나 스케줄링 태스크 실험임</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2609.39140'>Schema: Discovering Unknown Environments via Agentic Program Induction</a></td><td>35</td><td>2</td><td>NLP</td><td>미지 환경 규칙을 실행 가능한 프로그램으로 귀납해 ARC-AGI-3 등에서 큰 성능 향상을 보임. 환경 이해를 프로그램화하는 아이디어가 world model과 맥락이 닿음</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2609.40027'>Who Verifies the Graph? Misspecification Attacks on Causal Action Verification for Language Agents</a></td><td>35</td><td>2</td><td>NLP</td><td>causal action verifier를 그래프 오류로 red-team해 방어 메커니즘의 비용-안전 trade-off를 수치로 보임. causal reasoning 우선주제와 연결됨</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2609.38298'>It Takes Little to Rewrite Perception: Targeted Semantic Substitution in Vision-Language Models at $ε\leq 4/255$</a></td><td>35</td><td>1</td><td>Multimodal</td><td>VLM에 대한 저강도 적대적 semantic substitution 공격임. 보안 분석 위주라 로보틱스 연관성 낮음</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2609.38683'>Unveiling the Value of Motion for Cinematic Camera Trajectories</a></td><td>35</td><td>1</td><td>Video</td><td>카메라 궤적을 pose 대신 방향·속도로 분해해 영화적 카메라 생성을 개선하는 CineGEN 제안임. 카메라 제어 표현 아이디어는 active perception에 참고 가능하나 본 논문 자체는 영상 제작 목적임</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2609.38924'>From Image Interpretation to Clinical Reasoning: Upstream Physician-Context-Aware Multimodal Learning with Causal Reinforcement Learning</a></td><td>35</td><td>1</td><td>Multimodal</td><td>흉부 X-ray와 임상 기록을 결합해 심혈관 사건을 예측하는 causal RL 프레임워크임. causal reasoning 요소가 있으나 의료 예후 예측에 국한된 응용임</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2609.39523'>CIDER-FM: Foundation Models for Causal Inference from Diverse Experimental Regimes</a></td><td>35</td><td>1</td><td>LG</td><td>관측·개입 데이터를 결합하는 causal foundation model CIDER-FM 제안, causal reasoning 우선주제와 연관되나 로보틱스 적용은 없음</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2609.39773'>Riemannian Flow Models with Reinforcement Learning for Molecular Crystal Structure Prediction</a></td><td>35</td><td>1</td><td>LG</td><td>분자결정 구조 예측에 Riemannian flow와 RL 결합, 소재과학 응용으로 로보틱스 무관하나 RL fine-tuning 아이디어는 참고될 수 있음</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2609.39837'>Fast Regularized Policy Mirror Descent with One-Step TD Updates</a></td><td>35</td><td>1</td><td>RL</td><td>one-step TD 업데이트만으로 policy mirror descent의 global linear convergence 증명, RL 이론 기여이나 로봇 실험 없음</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2609.39967'>What Limits Recursive Reasoning Models: Optimization, Architecture and Test-Time Scaling</a></td><td>35</td><td>1</td><td>LG</td><td>HRM/TRM/URM 등 recursive reasoning model의 최적화·아키텍처 요인을 통일 분석해 안정적 학습 레시피 도출, 알고리즘 추론 모델 연구로 TAMP 같은 구조적 추론에 참고 가능</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2609.40221'>PhantomEnvironments: Training LLM Agents in Fictional Worlds</a></td><td>35</td><td>1</td><td>RL</td><td>규칙 기반 가상 환경으로 LLM 검색 에이전트 RL 학습함. 환경 생성 아이디어는 흥미로우나 embodied와 무관함.</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2609.40360'>Semifactual Credit-Augmented Policy Optimization</a></td><td>35</td><td>1</td><td>RL</td><td>GRPO의 token-level credit assignment를 semifactual 안정성으로 보완함. LLM 수학 추론용이라 robotics 직접 연관 낮음.</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2609.39118'>Diagnosing On-Policy Self-Distillation for Reasoning Language Models</a></td><td>35</td><td>1</td><td>NLP</td><td>on-policy self-distillation의 실패 모드를 진단한 분석 논문임. 새 방법론 제안 없이 현상 분석에 그침</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2609.39533'>CATCH: A Controllable Analysis Testbed for Reward Hacking in Coding RL</a></td><td>35</td><td>1</td><td>NLP</td><td>coding RL에서 reward hacking을 재현·탐지하는 controllable testbed임. CoT monitor가 결국 우회당한다는 발견이 흥미로움</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2609.39740'>LatentHarness: Learning Latent Actions for Memory and Reasoning via Counterfactual Policy Distillation</a></td><td>35</td><td>1</td><td>NLP</td><td>THINK/RECALL/EXIT 잠재 행동으로 memory와 reasoning을 통합한 방법임. counterfactual distillation 아이디어는 흥미로우나 여기서 action은 로봇 행동이 아니라 내부 추론 단계임</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2609.38288'>AREX-2: Advancing Self-Improving Agents through Long-Horizon Reflective Tasks</a></td><td>35</td><td>1</td><td>NLP</td><td>장기 reflective trajectory로 self-improving agent를 학습시켜 여러 벤치마크에서 강한 전이를 보임. agentic reasoning 측면에서 참고할 만함</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2609.38372'>Self-Evolving Harness on Multiple Tasks with the Agent as Its Own Optimizer</a></td><td>35</td><td>1</td><td>NLP</td><td>동일 모델이 solver와 proposer 역할을 모두 수행하며 자기 harness를 재귀적으로 개선하는 프레임워크임. self-improvement 설계가 흥미로움</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2609.38645'>Alignment via Training Against Probes Without Losing Monitorability</a></td><td>35</td><td>0</td><td>LG</td><td>probe 기반 LLM alignment 기법, internal activation 타겟 학습은 흥미로우나 로보틱스 무관</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2609.38847'>Scoring Higher, Answering Worse: Mitigating Reward Hacking in Rubric-Based RL via Protocol-Level Rubrics</a></td><td>35</td><td>0</td><td>LG</td><td>rubric 기반 RL의 reward hacking을 protocol-level aggregation으로 완화, LLM alignment 기법임</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2609.38879'>Does Learning Protein Folding Generalize to Broader Reasoning?</a></td><td>35</td><td>0</td><td>NLP</td><td>단백질 폴딩 학습이 일반 추론 능력으로 전이되는지 검증, 생물학 데이터 활용한 LLM post-training임</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2609.38909'>Unlearning Deceptive Behaviors in LLMs with Contrastive Forget Sets</a></td><td>35</td><td>0</td><td>NLP</td><td>맥락에 따라 발현되는 LLM 기만 행동을 contrastive forget set으로 unlearning, 안전성 연구임</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2609.38931'>Adaptive Self-Consistency: From Black-Box Sampling to Distribution-Valued Feedback</a></td><td>35</td><td>0</td><td>NLP</td><td>self-consistency를 grey-box 분포 관측으로 재정식화해 trajectory 수 절감, LLM 추론 효율화 기법임</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2609.38998'>Not all solutions are created equal: An analytical dissociation of functional and representational similarity in deep linear neural networks</a></td><td>35</td><td>0</td><td>LG</td><td>선형 네트워크에서 기능적 유사성과 표현적 유사성의 분리 증명, representation 이론 기여이나 로보틱스 적용 없음</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2609.39114'>The Row Normalization Puzzle in Muon</a></td><td>35</td><td>0</td><td>LG</td><td>Muon optimizer의 row normalization이 실제로 도움되는 이유를 이론-실험 간극으로 분석, 최적화 이론 기여임</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2609.39408'>Awakening of the Buddha: Subspace Learning During Population-Loss Plateaus</a></td><td>35</td><td>0</td><td>LG</td><td>population loss plateau 동안 subspace 학습이 일어남을 이론적으로 증명, 매우 수학적인 학습 동역학 연구임</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2609.39229'>RAIM: Robust Aggregation of Inexpensive Models for Hallucination Detection</a></td><td>35</td><td>0</td><td>NLP</td><td>저비용 judge 앙상블로 frontier judge 대체 가능성 검증. 실용적이나 novelty는 제한적</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2609.39661'>The Evolution of Attention in Large Language Models: Mechanisms, Trade-offs, and Emerging Trends</a></td><td>35</td><td>0</td><td>NLP</td><td>attention·메모리 메커니즘을 5차원으로 정리한 서베이임. 유용하지만 novelty는 리뷰 성격</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2609.38296'>AI Agents are Vulnerable to Radicalization</a></td><td>35</td><td>0</td><td>NLP</td><td>LLM agent가 다른 agent를 설득·공명을 통해 극단화시킬 수 있음을 보인 안전성 연구임</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2609.38340'>CARAT: Do Materials LLMs Reason or Recite?</a></td><td>35</td><td>0</td><td>NLP</td><td>materials LLM이 구조를 추론하는지 암기하는지를 정교한 controlled benchmark로 파헤친 연구임. 벤치마크 설계의 엄밀함이 돋보임</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2609.38925'>Prototype-guided Bilateral Alignment Multimodal Federated Learning</a></td><td>35</td><td>0</td><td>LG</td><td>모델·모달리티 이질성이 있는 연합학습에서 feature·decision 양쪽을 정렬하는 방법임. ICML 2026 Spotlight</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2609.39341'>Understanding as No-Arbitrage: Bounded Dutch Books as a Definition and Training Objective for Language Models</a></td><td>35</td><td>0</td><td>NLP</td><td>no-arbitrage 관점에서 언어모델의 understanding을 정의하고 Dutch book 공격으로 측정·훈련하는 이론적 프레임워크임. 흥미로운 정식화이나 응용 범위는 reasoning consistency에 국한</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2609.40324'>Cogentic: Multi-Agent Orchestration for Automated Proof Discovery</a></td><td>35</td><td>0</td><td>NLP</td><td>다중 prover와 적대적 검증으로 실제 미해결 수학 문제를 증명한 멀티에이전트 harness임. 결과가 전문가 검증을 받았다는 점이 특이함</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2609.39416'>Communication-Free Distributed Multi-Robot Task Allocation under Partial Observations Using Labeled Multi-Bernoulli Filtering</a></td><td>34</td><td>5</td><td>RL</td><td>통신 없이 LMB 필터로 이웃 위치를 추정해 task allocation을 분산 수행함. 시뮬레이션 몬테카를로 검증에 그치는 이론적 기여임.</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2609.38511'>Onboard Vision and MPC Navigation for Underwater Robots: An Open BlueROV2 Platform for Multi-Robot Experiments &amp; Docking</a></td><td>34</td><td>4</td><td>Navigation</td><td>BlueROV2 기반 오픈소스 수중로봇 비전+NMPC 플랫폼임. 재현성 있는 시스템 구축이 주 기여라 알고리즘적 novelty는 낮음.</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2609.38715'>Path-Following Control and Terramechanics Analysis for Planetary Rovers Under Wheel-to-Wheel Traction Asymmetry</a></td><td>34</td><td>4</td><td>Navigation</td><td>감속만으로 경로 추종하는 model-free skid-steering rover 제어임. 실제 힘 센서로 terramechanics를 검증한 응용 연구임.</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2609.39570'>Sparse Planner: A Hybrid Planner for Efficient Sampling via a Conditional Variational Autoencoder</a></td><td>34</td><td>4</td><td>Navigation</td><td>CVAE로 고품질 샘플링 분포를 학습해 자율주행 trajectory sampling 밀도를 8분의 1로 줄임. 효율화 수준의 기여임.</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2609.38594'>FAST-Sync: Fast Group Synchronization for any Matrix Lie Group</a></td><td>34</td><td>3</td><td>3D Vision</td><td>임의의 matrix Lie group에 대한 group synchronization 선형 근사법임. SLAM 백엔드 초기화 도구로 로봇 학습과는 거리 있음.</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2609.38846'>Coral Grow-out Robotic Assessment System (CGRAS): Scaling Coral Recruit Monitoring Through Robotics and Computer Vision</a></td><td>34</td><td>3</td><td>CV</td><td>산호 유생 모니터링을 로봇 촬영과 CV로 자동화함. 노동력을 9.6배 줄이는 응용 시스템 연구임.</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2609.40287'>PMosFM: Preconditioned Manifold Matching for One-Step Physics-Constrained Generation</a></td><td>34</td><td>2</td><td>Video</td><td>물리 제약 one-step flow matching 생성 모델임. world model 관련성은 있으나 로봇 적용 사례 없음.</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2609.39527'>Lens Flare Removal and Reconstruction</a></td><td>34</td><td>1</td><td>3D Vision</td><td>렌즈 플레어를 제거하고 3DGS와 공동 최적화해 flare를 분해·재렌더링하는 방법임. 3D 재구성 품질을 저해하는 센서 아티팩트를 다룬다는 점은 참고 가치 있음</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2609.40055'>Less Data, Better Timing: Student-Curriculum Coupling for VLM On-Policy Distillation in Temporal Video Grounding</a></td><td>34</td><td>1</td><td>Video</td><td>teacher 신뢰도와 student 역량을 분리해 curriculum을 동적으로 조절하는 SCC 제안임. temporal video grounding 학습 효율화 기여임</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2609.38274'>Which Models Work Well Together? Measuring Heterogeneity for LLM Team Selection</a></td><td>34</td><td>1</td><td>NLP</td><td>오류 비상관성과 예측 다양성으로 LLM 팀 조합을 고르는 heterogeneity 지표를 제안함. multi-agent 일반론이나 embodied 적용은 없음.</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2609.39045'>RSIGame: Autonomous Agentic Game Development with Recursive Self-improvement</a></td><td>34</td><td>1</td><td>NLP</td><td>local·global 루프로 게임을 탐색·진단·개선하는 recursive self-improvement 프레임워크임. self-improvement 개념은 로봇 RSI와 유사하나 게임 개발 적용임.</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2609.38930'>On the Relaxation of Conditional Independence Assumption for Image Segmentation</a></td><td>34</td><td>0</td><td>CV</td><td>RankSEG의 조건부 독립 가정을 완화해 segmentation 성능을 높이는 이론적 개선임. low-contrast 상황에서 효과 있으나 로보틱스와는 무관함</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2609.39836'>Spherical Interpolation for Backward-Compatible Multimodal Representations</a></td><td>34</td><td>0</td><td>Multimodal</td><td>모델 교체 시 gallery 재인덱싱 없이 spherical interpolation으로 검색 호환성을 복구하는 방법임. 검색 시스템 엔지니어링 기여로 로보틱스와 무관함</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2609.39924'>CoVisco: Codec-Native Vision Encoder with Native Token Compression for Unified Image-Video Understanding</a></td><td>34</td><td>0</td><td>Multimodal</td><td>코덱 입력과 segmented attention으로 긴 비디오를 압축 인코딩하는 CoVisco 제안임. 효율적 비전 인코더 설계로 로보틱스와는 거리가 있음</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2609.38194'>A Moving-Horizon Approximate Branch-and-Reduce Method for Deep Classification Trees</a></td><td>34</td><td>0</td><td>LG</td><td>대규모 연속형 데이터에 대해 깊은 분류 트리를 근사 최적화하는 moving-horizon 방법임. 해석가능 ML 최적화 기여로 로보틱스와 무관함</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2609.38424'>Graph Anomaly Detection as Finite-Horizon Control: Training-Free Scoring via Empirical Bayes</a></td><td>34</td><td>0</td><td>LG</td><td>그래프 이상 탐지를 finite-horizon control 에너지로 재정식화하는 training-free EB-GAD 제안임. 그래프 이상 탐지 응용으로 로보틱스와 무관함</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2609.38453'>Grokking through the Lens of Minimum-Norm Interpolation</a></td><td>34</td><td>0</td><td>LG</td><td>grokking을 minimum-norm interpolation 관점에서 설명하는 통계 이론 연구임. 일반화 이론 기여로 로보틱스와는 거리가 있음</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2609.38261'>NinaXander: Feasibility and Limits of Composing Frozen Language Models Across Architecture Families via a Shared Latent Space</a></td><td>34</td><td>0</td><td>NLP</td><td>서로 다른 아키텍처의 frozen LLM을 공유 latent adapter로 이어붙이는 시도임. 중간층 연결 시 성능이 부모 모델에 못 미치는 한계를 보고함.</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2609.38357'>Evaluating Language Model Safety Across Long Adversarial Conversations</a></td><td>34</td><td>0</td><td>NLP</td><td>긴 적대적 대화에서 안전 응답률이 턴이 길어질수록 급락함을 보임. LLM 안전성 평가 연구임.</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2609.38530'>Shifting Mechanisms: How Positional Encoding Choice Shapes In-Context Retrieval</a></td><td>34</td><td>0</td><td>NLP</td><td>positional encoding 선택이 in-context retrieval 메커니즘을 positional에서 semantic으로 바꾼다는 분석임. 해석가능성 연구임.</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2609.38802'>Uncovering Uncontrolled Repetition through Residual Stream Dynamics</a></td><td>34</td><td>0</td><td>NLP</td><td>반복 생성이 얕은 층에서부터 residual stream에 나타남을 추적해 억제함. 자원소모 공격 완화 연구임.</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2609.38976'>Fairness Beyond a Single Run: Training-Seed Variability in Speech LLM Adaptation</a></td><td>34</td><td>0</td><td>NLP</td><td>음성 LLM의 인구통계적 공정성 격차가 압축보다 학습 시드에 더 좌우됨을 보임. ASR 공정성 평가 연구임.</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2609.40190'>Cheap to Draw, Expensive to Trust: Certifying Test-Time Scaling Curves</a></td><td>33</td><td>1</td><td>LG</td><td>test-time scaling curve 통계적 인증 방법론임. LLM 평가 통계 문제로 로보틱스 연관 낮음.</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2609.38603'>Aperture: Training-Free Multiscale Concept Bottlenecks for Remote Sensing</a></td><td>33</td><td>0</td><td>CV</td><td>원격탐사용 training-free multiscale concept bottleneck 제안임. 해석가능성 개선 위주로 응용 도메인이 좁음</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2609.38881'>STRATA: Self-Learning Through Role-Aligned Tiered Agents for Real-Time Strategy Games</a></td><td>32</td><td>2</td><td>RL</td><td>RTS 게임에서 역할별 계층 agent와 경기 간 자기학습 experience card로 승률을 크게 높임. long-horizon 전략학습 아이디어가 흥미로우나 게임 도메인에 한정</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2609.39727'>OverForge: Reasoning Through Strategies and Tactics Helps Cooperative Lifelong Adaptation</a></td><td>32</td><td>2</td><td>RL</td><td>협력 멀티에이전트에서 전략·전술 추론을 분리한 training-free 계층 구조임. Overcooked에서 검증, long-horizon 협업이라는 맥락은 겹치나 로봇은 아님</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2609.40111'>Agent Error Dataset: Scaling 50,000 Error--Diagnosis Pairs for Failure Analysis and Error-Aware Post-Training</a></td><td>32</td><td>2</td><td>NLP</td><td>5만 개 error-diagnosis 쌍으로 agent 실패 진단·복구 학습 데이터셋을 구축함. failure diagnosis 개념이 로봇에도 전이 가능함</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2609.38758'>Event-Driven Refresh and Recurrence Memory to Reduce Stale Grounding in Referring Video Object Segmentation</a></td><td>32</td><td>1</td><td>Video</td><td>referring video segmentation에서 stale grounding을 이벤트 기반으로 재호출하는 EDRRM 제안임. 효율-정확도 트레이드오프 개선 수준의 engineering 기여임</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2609.38856'>Decoupling Spherical Reasoning from Dense Prediction for 360 Depth Estimation</a></td><td>32</td><td>1</td><td>3D Vision</td><td>ERP 왜곡 문제를 구면 그래프에서 분리해 360도 depth 추정을 개선하는 방법임. 적용 범위가 파노라마 depth로 좁음</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2609.39150'>OP-CAD: On-Policy Clean-Audio Distillation for Robust Audio-Visual Reasoning</a></td><td>32</td><td>1</td><td>Multimodal</td><td>환경 소음 속에서 오디오-비주얼 추론의 강건성을 커리큘럼 self-distillation으로 높이는 OP-CAD 제안임. 응용은 음성 질의응답 강건성에 국한됨</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2609.38632'>Proper Scoring Rule-based Diffusion for Probabilistic Weather Forecasting</a></td><td>32</td><td>1</td><td>LG</td><td>CRPS 기반 확률적 날씨 예측에 auxiliary denoising task 추가, world model과 개념적으로 유사하나 도메인이 날씨임</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2609.39456'>Mutual Equilibrium: Multimodal Representation Learning through Reciprocal Feedback</a></td><td>32</td><td>1</td><td>CV</td><td>상호 피드백으로 멀티모달 임베딩을 정제하는 MEQ, visual grounding 실험 포함하나 embodied 맥락은 아님</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2609.39738'>CNCGEN: A Dataset and Framework for Machining Process Planning and Toolpath Generation from B-rep Models</a></td><td>32</td><td>1</td><td>LG</td><td>B-rep CAD에서 가공 공정계획과 toolpath를 생성하는 CNCGEN 데이터셋·프레임워크, 제조 자동화 문제로 로봇 가공과 느슨하게 연관됨</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2609.39749'>Validity-Preserving Hierarchical RL for Joint Routing and Switch Placement in EDA</a></td><td>32</td><td>1</td><td>RL</td><td>칩설계 라우팅·스위치 배치를 validity-preserving hierarchical RL로 해결, 조합최적화 응용이나 로봇은 아님</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2609.39911'>Patient-Centered Treatment Planning for Chronic Multimorbidity: A Hierarchical Reinforcement Learning Framework for Preference Modeling</a></td><td>32</td><td>1</td><td>RL</td><td>환자 선호를 반영한 hierarchical option-critic 치료계획 프레임워크, 의료 응용이나 skill chaining 구조는 로봇 HRL과 유사함</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2609.38612'>StreamDecisionBench: Evaluating Decisions in Force on Evolving Language Streams</a></td><td>32</td><td>1</td><td>NLP</td><td>실시간으로 바뀌는 상태에서 지금 유효한 결정을 평가하는 StreamDecisionBench임. 실시간 판단 개념은 로봇 제어와 유사하나 언어 스트림 한정임.</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2609.39168'>Reinforcing Multimodal Reasoning via Token-Level Perception-Grounded Advantage Estimation</a></td><td>32</td><td>1</td><td>Multimodal</td><td>멀티모달 RLVR에서 토큰별 시각 의존도와 엔트로피로 세밀한 advantage를 추정하는 방법임. ACM MM 2026</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2609.39402'>Advancing Entropy-Level Credit Assignment in RLVR via Proximal Entropy Policy Optimization</a></td><td>32</td><td>1</td><td>RL</td><td>토큰 중요도를 이웃 맥락 기준 상대값(proximal entropy)으로 측정해 GRPO 대비 수학 reasoning을 개선함. NeurIPS 2026</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2609.38689'>EPIC: Epipolar-Consistent 360° Immersive Stereo Video Generation</a></td><td>32</td><td>0</td><td>Video</td><td>zero-shot으로 360도 스테레오 비디오를 생성하는 EPIC 제안임. 몰입형 디스플레이 콘텐츠 제작이 목적이라 로보틱스와 무관함</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2609.38978'>PARK: Accurate Block Retrieval for Sparse Attention in Video Diffusion Transformers</a></td><td>32</td><td>0</td><td>Video</td><td>비디오 diffusion transformer의 sparse attention block 검색 오차를 바로잡는 PARK 제안임. 추론 효율화 기여로 우선 평가 대상이 아님</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2609.39033'>TED:Text-Axis Evidence Decomposition for Prompted Anomaly Localization</a></td><td>32</td><td>0</td><td>CV</td><td>CLIP 기반 anomaly 탐지에서 defect 증거와 hard-normal 증거를 분리하는 TED 제안임. 산업 결함 검사 한정 응용임</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2609.39115'>Beyond Local Linearity: Scale-Resolved Geometry of Learned Image Encoders</a></td><td>32</td><td>0</td><td>CV</td><td>유한 크기 섭동에 대한 인코더 반응을 측정하는 scale-resolved 통계 기법 제안임. workshop extended abstract 수준의 분석 연구임</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2609.39132'>Uncertainty-Aware Consistency Distillation for Few-Step Video Generation</a></td><td>32</td><td>0</td><td>Video</td><td>지역별 불확실성으로 few-step video generation의 consistency distillation을 재가중하는 UACD 제안임. 효율화 기여 위주임</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2609.39315'>Rethinking Generative Image Compression at Extremely Low Bitrates</a></td><td>32</td><td>0</td><td>CV</td><td>극저 bitrate에서 semantic collapse를 완화하는 RAE 기반 compression-oriented diffusion RAE-CoD 제안임. 압축 효율화 기여로 로보틱스와 무관함</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2609.39657'>Diffusable Latents from Structure-Agnostic Distillation</a></td><td>32</td><td>0</td><td>CV</td><td>position-wise distillation 없이 이미지 수준 pooled descriptor만으로도 latent diffusability가 유지됨을 보인 분석임. 생성모델 학습 효율화 기여임</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2609.39704'>When Masking Helps or Hurts Robustness in Compressed CLIP: A Pre-Deployment Diagnostic</a></td><td>32</td><td>0</td><td>Multimodal</td><td>masking 기반 토큰 pruning이 worst-group robustness에 미치는 영향을 배포 전 진단하는 SIM 지표 제안임. CLIP 압축 안전성 점검 기여로 로보틱스와는 거리가 있음</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2609.39883'>Grounding with Confidence: Controllable Generative Video Temporal Grounding</a></td><td>32</td><td>0</td><td>Video</td><td>구간별 confidence head로 후보 생성과 채택을 분리하는 video temporal grounding 제안임. 비디오 검색 응용으로 로보틱스와 무관함</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2609.38193'>EHR2Trace: Auditable EHR Data Infrastructure for Patient World Models and Clinical Agents</a></td><td>32</td><td>0</td><td>LG</td><td>EHR을 patient world model 학습용으로 추적 가능하게 변환하는 EHR2Trace 제안임. 데이터 인프라 기여로 로보틱스와는 무관함</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2609.38363'>Simulator-Refined Diffusion for Radio-Frequency Inverse Design</a></td><td>32</td><td>0</td><td>LG</td><td>저해상도 surrogate의 gradient로 방향을 잡고 고해상도 시뮬레이터로 탐색하는 PCB 역설계 SRD 제안임. 전자회로 설계 응용으로 로보틱스와 무관함</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2609.38547'>Towards Universal Wasserstein Barycenters through Flow Matching</a></td><td>32</td><td>0</td><td>LG</td><td>flow matching으로 Wasserstein barycenter 전체 집합을 근사하는 BaryFM 제안임. 이론적 생성 모델링 기여로 로보틱스와는 거리가 있음</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2609.38853'>Visualizing Distribution Coverage in Generative Diffusion Models</a></td><td>32</td><td>0</td><td>LG</td><td>diffusion distillation이 distribution coverage를 잃는 현상을 pass@k로 규명, 생성모델 평가 기여임</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2609.38860'>Optimal Design for Active Preference Learning with Biased LLM Judges</a></td><td>32</td><td>0</td><td>LG</td><td>편향된 LLM judge 하의 active preference learning 최적 설계, alignment 이론 기여임</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2609.38920'>Learning Where to Steer: Noise-Space Geometry for Efficient Offline Multi-Objective Optimization with Generative Models</a></td><td>32</td><td>0</td><td>LG</td><td>offline multi-objective optimization에서 noise space 조향으로 diffusion sampling 유도, 설계 최적화 문제임</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2609.38938'>Robust Risk-Sensitive Reinforcement Learning from Corrupted Human Feedback</a></td><td>32</td><td>0</td><td>LG</td><td>오염된 human feedback 하의 risk-sensitive RLHF 후회 경계 증명, LLM alignment 이론임</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2609.38991'>Anchoring Adversarial Trajectories to Data Manifolds: A Bilevel Transfer Optimization Framework</a></td><td>32</td><td>0</td><td>CV</td><td>adversarial transfer를 data manifold에 anchoring하는 bilevel 프레임워크, NeurIPS spotlight이나 적대적 공격 연구로 로보틱스 무관</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2609.39034'>Switching Linear Attention</a></td><td>32</td><td>0</td><td>LG</td><td>online EM 기반 linear attention 확장으로 softmax attention 격차 축소, 시퀀스 모델 아키텍처 기여임</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2609.39109'>T-Router: Learning Thalamic Routing for Reasoning with Parameter-Efficient Reinforcement Learning</a></td><td>32</td><td>0</td><td>LG</td><td>파라미터 효율적 RL에 thalamic routing 아이디어 적용, LLM reasoning 효율화 기법임</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2609.39164'>QuanVI: Score-based Variational Inference via Quantum Maximally Mixed States</a></td><td>32</td><td>0</td><td>LG</td><td>양자 텐서 네트워크로 score-based VI를 확장한 QuanVI, 변분추론 방법론 기여임</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2609.39188'>Attention Function as an Intrinsic Inductive Bias: How Models&#x27; Behavior Diverges in Novel Contexts</a></td><td>32</td><td>0</td><td>LG</td><td>attention activation 함수가 intrinsic inductive bias로 작동함을 발달심리학 관점에서 탐구, 아키텍처 분석임</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2609.39190'>Dynamics to decision: A mathematical theory of Lyapunov spectra and decision boundaries in deep classifiers</a></td><td>32</td><td>0</td><td>LG</td><td>classifier의 레이어 전개를 동역학계로 보고 Lyapunov exponent로 decision boundary 분석, 이론적 해석가능성 연구임</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2609.39242'>A differentiability framework for zigzag persistent homology via linear interpolation</a></td><td>32</td><td>0</td><td>LG</td><td>zigzag persistent homology의 미분가능성 프레임워크 구축, 위상학적 ML 이론 기여임</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2609.39271'>RW-Flow: One-Step Generation on Compact Manifolds via Wasserstein Gradient Flows</a></td><td>32</td><td>0</td><td>LG</td><td>compact manifold 위 1-step 생성모델의 식별가능성 조건 증명, ICLR급 이론 기여이나 로보틱스 무관</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2609.39277'>A Tilted Bowl Is Not a Slippery Slope: Compressing Looped Models</a></td><td>32</td><td>0</td><td>NLP</td><td>looped model 압축 실패를 loop 수렴 여부로 설명하고 적응형 8bit 컨트롤러 제안, 효율적 추론 기법임</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2609.39595'>Convergence of Practical Muon with Finite Newton-Schulz Iterations and Nesterov Momentum</a></td><td>32</td><td>0</td><td>LG</td><td>유한 Newton-Schulz 반복 Muon optimizer의 수렴 증명, 최적화 이론 기여임</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2609.39648'>From Modes to Memories: Characterizing the Scale-Space Dynamics of Diffusion Models</a></td><td>32</td><td>0</td><td>CV</td><td>diffusion model을 noise-scale별 결정론적 동역학계로 보고 memorization을 critical scale로 정량화, 생성모델 해석 연구임</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2609.39767'>How Does Local Landscape Geometry Evolve in Language Model Pre-Training?</a></td><td>32</td><td>0</td><td>LG</td><td>language model pretraining의 local landscape geometry 변화 분석 및 동적 batch size 스케줄러 제안, 학습 역학 연구임</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2609.39800'>Finite-Horizon Fisher Memory in Two-Sided Power-Bounded Recurrent Systems</a></td><td>32</td><td>0</td><td>LG</td><td>power-bounded recurrent system의 유한수평 Fisher memory 이론 분석, 매우 수학적인 메모리 이론임</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2609.39813'>Backward-State Policy Is Part of the Learning Algorithm</a></td><td>32</td><td>0</td><td>LG</td><td>저정밀도 학습에서 backward 재사용 값이 학습 알고리즘의 일부임을 증명, 수치 정밀도 이론 기여임</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2609.39866'>Preemptive LLM Unlearning against Forbidden Capability Acquisition via Gradient Sealing</a></td><td>32</td><td>0</td><td>LG</td><td>사전 배포 단계에서 금지 능력 습득을 막는 gradient sealing 기법, LLM 안전성 연구임</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2609.39929'>RoPE at the End of Its Rope? Theory, Diagnosis, and Mitigation of Long-Context Failures</a></td><td>32</td><td>0</td><td>NLP</td><td>RoPE의 semantic-positional 상충을 이론화하고 long-context 실패를 진단·완화, LLM 아키텍처 분석임</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2609.40030'>Fenchel Tilting: Weighted Correction for Efficient Finetuning of Generative Models</a></td><td>32</td><td>0</td><td>LG</td><td>Fenchel 쌍대성으로 utility 최적화와 생성모델 fitting을 분리하는 FTFC, 생성모델 효율적 파인튜닝 기법임</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2609.38260'>ContextAdapt: Evaluating Contextual Adaptation and Value Alignment in LLMs</a></td><td>32</td><td>0</td><td>NLP</td><td>직업 맥락별 가치 적용의 일관성을 평가하는 ContextAdapt 벤치마크임. AI alignment 평가 연구임.</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2609.38792'>Training LLM Judges from Language Feedback via Position-Selective Self-Distillation</a></td><td>32</td><td>0</td><td>NLP</td><td>자연어 피드백을 entropy shift로 선별해 self-distillation으로 LLM judge를 학습함. 주관적 평가 과제용 보상학습 연구임.</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2609.38795'>Recovering Off-Policy Supervision for Speculative Decoding</a></td><td>32</td><td>0</td><td>NLP</td><td>off-policy 토큰으로 무효화된 speculative decoding 지도신호를 target rollout으로 복원함. LLM 추론 가속 연구임.</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2609.38816'>You&#x27;re Hired: Strategic Model Selection for LLM Collaboration</a></td><td>32</td><td>0</td><td>NLP</td><td>LLM 협업 팀을 고르는 9가지 선택 알고리즘을 체계적으로 비교함. multi-LLM 시스템 구성 연구임.</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2609.38923'>GraphForge: Training Working Agents with Graph-Anchored Workspace Synthesis</a></td><td>32</td><td>0</td><td>NLP</td><td>실제 파일 기반 evidence graph로 작업 agent 학습 데이터를 합성함. 디지털 업무 agent 학습 연구임.</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2609.38995'>When Clipping Reverses Correction: Failure Dynamics of Pointwise Forward-KL On-Policy Self-Distillation</a></td><td>32</td><td>0</td><td>NLP</td><td>forward-KL pointwise clipping이 오히려 teacher로부터 멀어지게 만드는 실패를 증명함. self-distillation 학습역학 분석임.</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2609.39027'>A Missing Piece for Trustworthy AI Reviewers: From Benchmarking Rhetorical Robustness to SciCore Review</a></td><td>32</td><td>0</td><td>NLP</td><td>같은 내용을 다르게 쓴 원고에 AI 리뷰어 점수가 흔들리는 rhetorical robustness를 벤치마크함. AI 동료평가 신뢰성 연구임.</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2609.38445'>AIM: Agentic Idea Management for Automated Research</a></td><td>32</td><td>0</td><td>NLP</td><td>베이지안 최적화에서 착안해 자동 연구 아이디어를 관리·선택하는 프레임워크임</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2609.38639'>Component-Aware Feedback for Self-Evolving Programs</a></td><td>32</td><td>0</td><td>NLP</td><td>자기진화 프로그램 탐색에서 컴포넌트별 변화-성능 귀속을 기록하는 attribution memory를 제안함</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2609.38661'>EvoSteer: Online Self-Evolving Graph Orchestration via Reference-Anchored Credit Assignment</a></td><td>32</td><td>0</td><td>NLP</td><td>실행 중 팀을 수정하는 online self-evolving graph orchestration과 flow-matching 기반 credit assignment를 제안함</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2609.38721'>UniEvo-VL: An On-policy Self-Distillation Training Recipe for Multimodal Model Self-improvement</a></td><td>32</td><td>0</td><td>CV</td><td>멀티모달 모델이 자기비판을 teacher로 삼아 이미지 생성을 self-improve하는 on-policy self-distillation임</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2609.38866'>When Context Changes: Understanding Update Failures in LLMs</a></td><td>32</td><td>0</td><td>NLP</td><td>context 갱신 시 모델이 오래된 값을 계속 쓰는 stale binding을 attention drift로 설명하고 개입으로 교정함</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2609.38958'>Targeted Retrieval, Compact Representations: How CoT Reasoning Improves Long-Context Counting</a></td><td>32</td><td>0</td><td>NLP</td><td>CoT가 long-context counting을 돕는 메커니즘을 targeted retrieval과 내부 counter로 설명한 해석가능성 연구임</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2609.38962'>Alleviating Hallucination in Reasoning Tasks with Training-Free Uncertainty-Guided Steering</a></td><td>32</td><td>0</td><td>NLP</td><td>확신도 gradient로 활성화를 조정해 추론 중 hallucination을 줄이는 training-free steering 방법임. NeurIPS 2026</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2609.39076'>Multi-LLM Collaborative Alignment via Stackelberg Games</a></td><td>32</td><td>0</td><td>NLP</td><td>EXP3 bandit을 leader로 둔 Stackelberg 게임으로 multi-LLM instruction curriculum을 적응시킴</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2609.39838'>Learning Steganography Is Easy, Learning Steganographic Reasoning Is Hard</a></td><td>32</td><td>0</td><td>NLP</td><td>steganographic messaging은 쉽게 배우지만 steganographic reasoning은 SFT로만 겨우 학습됨을 보인 AI 감시 안전성 연구임. NeurIPS 2026 workshop oral</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2609.40303'>How Much of a Harness Does a Strong Agent Need for Autonomous ML Engineering?</a></td><td>32</td><td>0</td><td>NLP</td><td>복잡한 harness가 강한 backbone 모델 대비 이득이 없음을 보인 negative result임. ML 엔지니어링 agent 설계에 시사점이 큼</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2609.39559'>Divide and Collapse: MAPF-Collapse via Exact Decomposition into Independent Sub-Instances</a></td><td>30</td><td>4</td><td>Navigation</td><td>MAPF 계획을 독립 부분문제로 정확히 분해해 post-optimization을 크게 가속화한 알고리즘 기여임. 학습적 novelty보다 엔지니어링 최적화 성격</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2609.38462'>Observability Analysis and Online Calibration of Visual-Inertial-Wheel Odometry for 4WIS4WID Mobile Robots</a></td><td>30</td><td>3</td><td>Navigation</td><td>4WIS4WID 모바일로봇용 visual-inertial-wheel odometry observability 분석임. 센서 융합 보정 연구로 학습 요소는 없음.</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2609.39618'>TO-mdiSPAs: Topology Optimization of multi-directional Soft Pneumatic Actuators</a></td><td>30</td><td>3</td><td>Manipulation</td><td>다방향 soft pneumatic actuator를 topology optimization으로 설계함. 기구 설계 최적화 연구로 학습 요소는 없음.</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2609.39047'>BadAction: Backdoor Attacks on Interactive Video Generation via Action-Guided Triggers</a></td><td>30</td><td>2</td><td>Video</td><td>action-guided trigger로 interactive video generation에 backdoor를 심는 첫 체계적 공격 연구임. world action model의 interactivity를 공격 표면으로 다룬 점은 새롭지만 공격 연구 자체의 상한 novelty는 중간임</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2609.38730'>Bounded Channel-Adaptive Spectral Learning for Forward-Consistent Inverse Flapping-Wing Aerodynamics</a></td><td>30</td><td>2</td><td>RL</td><td>flapping-wing 역운동학 예측에 제한된 spectral correction을 결합한 GRU 구조임. 니치한 비행체 응용이라 embodied AI 연관성 낮음.</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2609.39265'>Universal Cross-Prompt Adversarial Attacks on Promptable Concept Segmentation</a></td><td>30</td><td>1</td><td>CV</td><td>SAM3 concept segmentation에 대한 범용 cross-prompt 적대적 공격 AdvPCS 제안임. foundation segmentation 모델의 취약점을 드러내지만 보안 분석에 그침</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2609.39567'>Invariant Shape Analysis of Surfaces with Spherical Topology</a></td><td>30</td><td>1</td><td>3D Vision</td><td>구면 조화 기술자를 parameterization·pose·거울상에 불변하게 만드는 수학적 방법 제안임. 해부학적 형태 분석 응용으로 로보틱스 직접 적용은 제한적임</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2609.38863'>GeoNest: Learning to Select Failure-Aware Neighborhoods for the Irregular Knapsack Problem in a Circular Container</a></td><td>30</td><td>1</td><td>LG</td><td>원형 용기 비정형 knapsack 문제에 failure-aware neighborhood search, 제조업 packing 최적화로 로봇 그리핑과는 거리가 있음</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2609.38911'>Generalized Residual Closure: General Learning Dynamics for Stability-Plasticity Compatibility</a></td><td>30</td><td>1</td><td>LG</td><td>stability-plasticity 호환성을 일반 학습 동역학으로 공식화한 추상 이론, continual learning 연결되나 매우 수학적임</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2609.39387'>Beyond Simulation: Retain-and-Repair Neural Operators for Real-World Adaptation</a></td><td>30</td><td>1</td><td>LG</td><td>시뮬레이션 사전학습 neural operator를 실세계 데이터에 보존적으로 적응시키는 R2NO, sim-to-real 적응 개념과 유사하나 PDE 도메인임</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2609.40284'>cua-speedrun: Standardized Benchmarking of the Speed of Computer-Use Agents</a></td><td>30</td><td>1</td><td>Embodied AI</td><td>computer-use agent 속도 표준 벤치마크임. 물리 로봇이 아닌 디지털 환경 평가라 연관성 낮음.</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2609.40292'>Disentangling Computation in Multi-Task Neural Networks with the Green&#x27;s Operator</a></td><td>30</td><td>1</td><td>LG</td><td>multitask RNN의 perturbation routing을 Green&#x27;s operator로 분석함. 해석가능성 이론 연구임.</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2609.38490'>Personalized State-Transition-Aware Memory for Clinical Agents</a></td><td>30</td><td>1</td><td>NLP</td><td>임상 기록의 상태 전이를 Active/History로 구분해 기억하는 메모리 프레임워크임. memory 설계 개념은 있으나 의료 대화 한정임.</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2609.39578'>Thinking Outside the Box: Can Language Models Rely on External Guidance Selectively?</a></td><td>30</td><td>1</td><td>NLP</td><td>불확실한 workflow guidance를 선택적으로 신뢰하는 능력을 측정·학습시킴. agent reliability 관점에서 의미 있으나 robotics 적용은 간접적</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2609.39938'>LEAP: Learned Block-wise Evidence Retrieval for Long Audio-Video Perception</a></td><td>30</td><td>1</td><td>Video</td><td>시간당 오디오-비디오 QA에서 블록 단위 evidence retrieval로 context 비례 문제를 해결함</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2609.39982'>Mid-Harness: Scaling Actions Between Model and Harness for Terminal Agents</a></td><td>30</td><td>1</td><td>NLP</td><td>model-harness 경계에서 action sampling·verification으로 terminal agent 신뢰도를 높인 연구임</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2609.38712'>Staying on Task: Testing the Foundations of Long-Horizon Agent Reliability</a></td><td>30</td><td>1</td><td>NLP</td><td>긴 생성 중 상태를 추적·갱신하는 능력을 축별로 분리 측정하는 진단 벤치마크임. context 길이에 따른 급격한 성능 저하를 보임</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2609.38778'>Action Conditioned Bisimulation For GUI Agent Memory</a></td><td>30</td><td>1</td><td>NLP</td><td>GUI agent 메모리에서 관측 유사도 대신 action-conditioned bisimulation으로 상태를 병합하는 방법임. 상태 추상화 아이디어는 robot memory에도 참고할 만함</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2609.38343'>Learning Semantic Inpainting for Animatable Gaussian Head Avatars</a></td><td>30</td><td>0</td><td>3D Vision</td><td>단일 이미지에서 Gaussian head avatar의 미관측 영역을 UV space에서 inpainting하는 작업임. 아바타 렌더링 품질 개선 위주로 로보틱스와 무관함</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2609.38479'>Caption-Mediated Perceived-Safety Estimation for Pedestrian Routing</a></td><td>30</td><td>0</td><td>CV</td><td>거리 영상 캡션 기반 보행자 안전 경로 산정 응용 논문임. 대규모 현장 검증은 있지만 로보틱스 연관성 없음</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2609.38591'>Restoring without Forgetting: Filter-Level Continual Image Restoration via Parameter-Space Integrated Gradients</a></td><td>30</td><td>0</td><td>CV</td><td>filter 단위로 task-specific 지식을 분리해 continual image restoration을 하는 RwF 제안임. 복원 태스크 한정이라 로보틱스와 무관함</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2609.38680'>ReGain: Restoring Subject Fidelity in Personalization on Synthetic Images</a></td><td>30</td><td>0</td><td>CV</td><td>synthetic 이미지로 DreamBooth 학습 시 생기는 피사체 충실도 저하를 CFG 주파수 보정으로 완화하는 ReGain 제안임. 개인화 생성 응용이라 로보틱스와 무관함</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2609.38748'>Here the World in Stereo: Learning Dynamic Spatial Correspondence for Immersive Joint Video-Audio Generation</a></td><td>30</td><td>0</td><td>Multimodal</td><td>motion track으로 비주얼 소스 움직임과 스테레오 오디오를 결합하는 StereoBind 제안임. AR/VR 콘텐츠 목적이라 로보틱스와 무관함</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2609.38968'>Beyond Spatial-Domain Supervision: A Relation Constrained Space for Multi-Modal Image Fusion</a></td><td>30</td><td>0</td><td>CV</td><td>frozen DINO/CLIP 특징으로 relation space supervision을 구성하는 멀티모달 이미지 융합 방법임. niche한 fusion 태스크임</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2609.39004'>When Integral Meets Decomposition: A Signal-Level Self-Supervised Feature Decompose Paradigm for Multi-Modal Image Fusion</a></td><td>30</td><td>0</td><td>CV</td><td>feature decomposition을 1D 신호 적분 문제로 재정식화하는 self-supervised 이미지 융합 방법임. niche fusion 태스크로 로보틱스와 무관함</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2609.39066'>Agentic Tool-Augmented Reasoning for Explainable Image Forgery Detection</a></td><td>30</td><td>0</td><td>CV</td><td>22개 forensic tool을 에이전트가 multi-turn으로 활용해 이미지 위조를 탐지하는 ATAR 제안임. forensics 도메인 특화 응용임</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2609.39157'>TripleFlow: Training-Free Video Object Removal by Bridging Residual Editing and Native Generation</a></td><td>30</td><td>0</td><td>Video</td><td>erasure와 generation flow를 결합한 training-free 비디오 객체 제거 TripleFlow 제안임. 비디오 편집 응용으로 로보틱스와 무관함</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2609.39451'>ResARC: Residual-Aware AutoRegressive Coding for Ultra-Low Bitrate Image Compression</a></td><td>30</td><td>0</td><td>CV</td><td>quantization residual과 generation residual을 모두 보정하는 ResARC 압축 코덱 제안임. 초저 bitrate 이미지 압축 기여로 로보틱스와 무관함</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2609.39681'>MC-PanDA++: Simpler, Stronger, and More Robust Domain-Adaptive Panoptic Segmentation</a></td><td>30</td><td>0</td><td>CV</td><td>domain-adaptive panoptic segmentation을 단일 단계 파이프라인으로 단순화한 MC-PanDA++ 제안임. 기존 방법 대비 단순화·안정화 수준의 개선임</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2609.39953'>Learning to Reason with Compressed Context: Ground-Truth-Free Adaptation of OmniLLMs via Self-Distillation</a></td><td>30</td><td>0</td><td>Multimodal</td><td>정답 없이 full-context self-teacher로 압축 context 추론을 적응시키는 CAFD 제안임. OmniLLM 배포 효율화 기여로 로보틱스와 무관함</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2609.40031'>WARP: A Unified Benchmark for Invisible Image Watermarking -- Robustness and Protection Against Attacks</a></td><td>30</td><td>0</td><td>CV</td><td>invisible watermarking의 강건성을 표준화해 평가하는 WARP 벤치마크임. 콘텐츠 인증 목적으로 로보틱스와 무관함</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2609.38484'>RetroGEF: Dynamic Graph Edit Flow for Single-Step Retrosynthesis</a></td><td>30</td><td>0</td><td>LG</td><td>그래프 크기 변화를 포함한 단일 단계 retrosynthesis를 flow 기반으로 생성하는 RetroGEF 제안임. 화학 합성 응용으로 로보틱스와 무관함</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2609.38540'>When a Flatness Proxy Is Not a Function: Robustness Certificates and Training Interventions</a></td><td>30</td><td>0</td><td>LG</td><td>flatness proxy가 robustness certificate로 쓰일 수 없는 조건을 분석한 이론 연구임. 일반 이론 기여로 로보틱스와 무관함</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2609.38585'>FlexRouter: Learning Complementary Model Sets for Flexible LLM Routing</a></td><td>30</td><td>0</td><td>LG</td><td>모델 간 상호보완성을 DPP로 모델링해 LLM 라우팅을 하는 FlexRouter 제안임. LLM 서빙 응용으로 로보틱스와 무관함</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2609.38625'>Interpretable but Fragile? Robustness of Concept Bottlenecks under Geometric-Semantic Perturbations</a></td><td>30</td><td>0</td><td>LG</td><td>concept bottleneck model의 robustness 분석, interpretability 연구로 로보틱스 연관 약함</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2609.38666'>Understanding Off- vs On-Policy Distillation: A Tale of Distinct Training Objectives</a></td><td>30</td><td>0</td><td>LG</td><td>on-policy distillation의 forward/reverse KL 특성 이론 분석, LLM 세팅 한정</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2609.38768'>Learning Under Forgetting: Statistical Support-Selective Retention in Stochastic Training Dynamics</a></td><td>30</td><td>0</td><td>LG</td><td>forgetting을 selection mechanism으로 보는 이론적 프레임워크, 추상적 분석이고 로보틱스 적용 없음</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2609.38797'>Evaluating Persistent Calibration under Evolving Model Knowledge</a></td><td>30</td><td>0</td><td>NLP</td><td>모델 지식 변화에 따른 calibration 일반화 문제 정의, LLM checkpoint 분석임</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2609.38830'>SparLeak: Privacy Leakage from Sparse Attention in LLM Inference on Shared GPUs</a></td><td>30</td><td>0</td><td>LG</td><td>sparse attention의 GPU 사이드채널 프라이버시 공격, 보안 연구로 로보틱스 무관</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2609.38833'>ReSCENE: Server-Side Replay for Structural Mitigation of Catastrophic Forgetting in Federated Continual Learning</a></td><td>30</td><td>0</td><td>LG</td><td>federated continual learning의 forgetting 완화, 연합학습 세부 개선임</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2609.38854'>Mitigating the Length-Scaling Tax with Online Distillation</a></td><td>30</td><td>0</td><td>LG</td><td>RL post-training의 응답 길이 과다 문제를 self-distillation으로 완화, LLM 효율화 기법임</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2609.38918'>Flow Matching under Noisy Latent Structure: Beyond Exact Low-Dimensional Support</a></td><td>30</td><td>0</td><td>LG</td><td>잡음 섞인 저차원 잠재 구조 하의 flow matching 수렴 이론, 생성모델 이론 기여임</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2609.38977'>Scale-Split Neural Operator for Memory- and Data-Efficient 3D Turbulence Prediction</a></td><td>30</td><td>0</td><td>LG</td><td>3D 난류 예측을 위한 scale-split neural operator, 과학계산 문제로 로보틱스 무관</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2609.38987'>Smaller Models, Better Rejects: Preference Distillation Scaling</a></td><td>30</td><td>0</td><td>NLP</td><td>preference distillation에서 작은 모델의 reject가 더 유용함을 보임, LLM post-training 분석임</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2609.39048'>Structure-aware Reinforcement Learning for Protein Directed Evolution</a></td><td>30</td><td>0</td><td>LG</td><td>구조 인지 RL로 단백질 directed evolution 최적화, 생물학 응용이라 로보틱스 무관</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2609.39137'>ID Balancing: Stable Training of Extremely Sparse MoE via PID-Based Load Control</a></td><td>30</td><td>0</td><td>LG</td><td>MoE 로드 밸런싱을 PID 제어로 재해석한 ID Balancing, LLM 스케일링 기법임</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2609.39144'>Sharp Stationary Gaussian Approximation for Constant-Stepsize SGD</a></td><td>30</td><td>0</td><td>LG</td><td>고정 스텝 SGD의 정상분포 가우시안 근사 샤프닝, 최적화 이론 기여임</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2609.39177'>Whitening Improves Robustness to Spurious Correlations in Linear Probes</a></td><td>30</td><td>0</td><td>LG</td><td>linear probe의 spurious correlation에 whitening이 도움됨을 보임, robustness 분석 연구임</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2609.39261'>Jacobian Rank Collapse in Decision-Focused Learning</a></td><td>30</td><td>0</td><td>LG</td><td>decision-focused learning의 Jacobian rank collapse 분석, 포트폴리오 최적화 응용임</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2609.39336'>How Many Samples Are Enough for Learning Across Domains?</a></td><td>30</td><td>0</td><td>LG</td><td>도메인 수와 도메인당 샘플 수의 역선형 관계를 generalization bound로 규명, 학습이론 기여임</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2609.39383'>From Search to Signal: Online Post-Training in Automatic Heuristic Design</a></td><td>30</td><td>0</td><td>LG</td><td>자동 휴리스틱 설계에서 search-coupled online post-training 신호 구성법 연구, 알고리즘 설계 자동화임</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2609.39445'>Raw-Routed Mixture of Adapters: A Causal Intervention for Routing Collapse in Time Series Foundation Models</a></td><td>30</td><td>0</td><td>LG</td><td>시계열 foundation model의 instance normalization이 유발하는 MoE routing collapse 원인 규명, 적응 기법 연구임</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2609.39497'>The Geometry of Randomized Smoothing on Feasible Sets</a></td><td>30</td><td>0</td><td>LG</td><td>feasibility filtering 하의 randomized smoothing 인증 기하학 분석, adversarial robustness 이론 기여임</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2609.39512'>Can Domain Generalization be Guaranteed in Small-Sample Learning?</a></td><td>30</td><td>0</td><td>LG</td><td>small-sample domain generalization에서 SRM의 이론적 보장 최초 제시, 학습이론 연구임</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2609.39560'>Self-Repulsive Sampling for Diffusion Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>masked diffusion LM의 peer commitment 기반 self-repulsive sampling으로 다양성 확보, 디코딩 기법임</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2609.39739'>Stable Transformers for Graph Generation</a></td><td>30</td><td>0</td><td>LG</td><td>그래프 생성용 Graph Transformer의 깊이에 따른 dissipative dynamics 분석 및 안정화, 생성모델 아키텍처 연구임</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2609.39757'>Revisiting On-policy Adversarial Black-Box Distillation: Calibrating Groupwise Reward Geometry for Effective Advantage Construction</a></td><td>30</td><td>0</td><td>CV</td><td>on-policy adversarial black-box distillation의 reward geometry 보정 GRGC, LLM distillation NeurIPS 논문임</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2609.39798'>Probabilistic Adversarial Training</a></td><td>30</td><td>0</td><td>LG</td><td>분포 간 KL 거리로 probabilistic robustness 하한 유도하는 adversarial training 해석, 적대적 견고성 이론임</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2609.39816'>Beyond Accuracy: Prefix-Invariant Realizations of Low-Precision Fast Matrix Multiplication</a></td><td>30</td><td>0</td><td>LG</td><td>고속 행렬곱의 prefix invariance 위반을 진단하고 인증 가능한 Strassen 실현법 제시, LLM 추론 정확성 연구임</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2609.39818'>Should I stay or should I show? Learning to selectively disclose information</a></td><td>30</td><td>0</td><td>LG</td><td>budget 하의 selective disclosure를 VoI threshold 정책으로 학습, human-AI decision support 연구임</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2609.39855'>Dimension-Free Rank Lifting from Random Hyperplane Arrangements</a></td><td>30</td><td>0</td><td>LG</td><td>무작위 초기화 은닉층의 rank lifting에 필요한 폭 경계 증명, 신경망 표현력 이론임</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2609.39859'>Fork-dLLM: Avoiding the Flexibility Trap in Diffusion Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>diffusion LM의 flexibility trap을 fallback step에서만 AR 샘플링하는 hybrid 방식으로 해결, 디코딩 효율화 기법임</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2609.39892'>Shared Weights, Selected Computations: How Looped Transformers Route What Each Loop Does</a></td><td>30</td><td>0</td><td>LG</td><td>looped transformer가 공유 가중치로 서로 다른 연산을 라우팅하는 메커니즘 분석, 아키텍처 해석 연구임</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2609.39912'>TRACE: Trajectory Selection for Parallel Scaling of Search Agents</a></td><td>30</td><td>0</td><td>NLP</td><td>병렬 search agent의 trajectory selection을 cross-rollout evidence로 학습, 웹 검색 에이전트 효율화 기법임</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2609.40127'>Learning Functional Subspaces for Neural Network Compression</a></td><td>30</td><td>0</td><td>NLP</td><td>end-to-end로 학습되는 orthogonal projector 기반 저랭크 압축 LSP, 고압축률에서 기존 기법 대비 우수함을 보임</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2609.40316'>Scaling Laws for Looped Mixture of Experts</a></td><td>30</td><td>0</td><td>LG</td><td>looped transformer와 MoE 결합 스케일링 법칙임. LLM 효율화 연구로 robotics 연관 없음.</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2609.38201'>TomasuLLM: Out-of-Order Speculative Execution for LLM Agents</a></td><td>30</td><td>0</td><td>NLP</td><td>코딩 에이전트 tool call을 out-of-order로 실행해 지연을 줄이는 런타임 시스템임. 로보틱스와 무관함.</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2609.38222'>Conformal Factuality Control for Multi-Hop Retrieval-Augmented Generation</a></td><td>30</td><td>0</td><td>NLP</td><td>multi-hop RAG에 claim-level conformal factuality filtering을 적용함. 검색 기반 LLM 신뢰성 연구로 robotics와 무관함.</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2609.38480'>KlinikeBench: Evaluating Language Models Beyond Diagnostic Accuracy</a></td><td>30</td><td>0</td><td>NLP</td><td>완전한 환자 기술이 아닌 대화형 진찰 과정을 평가하는 임상 벤치마크임. 의료 LLM 평가 연구임.</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2609.38510'>DEdit: Iterative Draft Editing for Speculative Decoding</a></td><td>30</td><td>0</td><td>NLP</td><td>diffusion drafter가 draft를 반복 편집해 speculative decoding 수락 길이를 늘림. LLM 추론 가속 연구임.</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2609.38543'>MedKIT: Evaluating Knowledge Integration and Generalization in Large Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>임상 지식 갱신이 실제로 사용 가능한지 평가하는 MedKIT 벤치마크임. 의료 지식 통합 평가 연구임.</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2609.38660'>Breaking Babel: A Self-Evolving Multi-Agent System for Long-Form Subtitle Translation</a></td><td>30</td><td>0</td><td>NLP</td><td>시리즈 단위 메모리와 동적 라우팅으로 장편 자막 번역 품질을 높이는 self-evolving multi-agent 시스템임. 번역 응용 연구임.</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2609.39263'>Concept Subspaces Compute Beyond the Logit Lens: A Weights-Only Test for Locating Representations Upstream of Readout</a></td><td>30</td><td>0</td><td>NLP</td><td>concept subspace와 readout 방향의 기하학적 분리를 측정하는 해석가능성 연구임. 분석 도구 성격이 강함</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2609.39346'>Offline Guidance, Online Reasoning: Reusing LLM Feedback for Small Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 피드백을 SLM hidden space에 재사용하는 방법임. 엔지니어링적 조합에 가까움</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2609.39358'>Working Around the Compute Ceiling: Byte-Exact Memory in Galahad Makes LLM Reading a One-Time Cost LLM Reading a One-Time Cost</a></td><td>30</td><td>0</td><td>LG</td><td>LLM serving의 KV state 재사용으로 반복 reading 비용을 없애는 인프라 논문임. 시스템 기여이지 모델링 novelty는 아님</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2609.39645'>SEPAL: Separated Expert Pairs with Answer-Level Fusion for Reliable LLM Collaboration</a></td><td>30</td><td>0</td><td>NLP</td><td>역할별 private Actor-Critic팀으로 multi-agent 토론의 다양성을 보존하는 방법임. 점진적 개선 수준</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2609.39687'>Better Supervision Is Nearby: Neighborhood On-Policy Self-Distillation</a></td><td>30</td><td>0</td><td>NLP</td><td>on-policy self-distillation에 이웃 파라미터 전문가 풀을 추가한 방법임. 수학 reasoning 벤치마크에 국한</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2609.39765'>MemCodex: Self-Programming Hierarchical Memory for Language Agents</a></td><td>30</td><td>0</td><td>NLP</td><td>계층적 memory를 자기진화 프로그램으로 구성하는 agent memory 시스템임</td></tr>
<tr><td>486</td><td><a href='https://arxiv.org/abs/2609.39807'>Stress-Testing LLM Lie Detectors: Role-Play Failures and Spurious Correlations</a></td><td>30</td><td>0</td><td>NLP</td><td>role-play 상황에서 기존 lie detection probe들이 persona의 믿음을 따라가며 실패함을 보임</td></tr>
<tr><td>487</td><td><a href='https://arxiv.org/abs/2609.39827'>Synthetic Pre-pretraining Survives Scale, but Not as a Grammatical Prior</a></td><td>30</td><td>0</td><td>NLP</td><td>synthetic pre-pretraining 효과가 스케일에서도 유지되지만 원인이 문법적 prior가 아니라 long-range retrieval임을 재검증함</td></tr>
<tr><td>488</td><td><a href='https://arxiv.org/abs/2609.40118'>Persistent Context Graphs for Efficient Memory Compaction in LLM Agents</a></td><td>30</td><td>0</td><td>NLP</td><td>attention 기반 importance score를 그래프로 저장해 memory compaction 비용을 줄인 시스템 기여임</td></tr>
<tr><td>489</td><td><a href='https://arxiv.org/abs/2609.40185'>Provably Tractable NFA-Constrained Language Generation via HMMs</a></td><td>30</td><td>0</td><td>NLP</td><td>#NFA 카운팅의 FPRAS를 이용해 다항시간 NFA 제약 생성 엔진을 만든 이론 기반 방법임</td></tr>
<tr><td>490</td><td><a href='https://arxiv.org/abs/2609.40340'>EvoDuet: Bilevel Co-Evolution of Web Searching and Task Solving for Scientific Discovery</a></td><td>30</td><td>0</td><td>NLP</td><td>해(solution)와 검색 쿼리를 공진화시키는 evolutionary search 방법임</td></tr>
<tr><td>491</td><td><a href='https://arxiv.org/abs/2609.38294'>MoFlow: Multi-Objective Agentic Workflow Generation</a></td><td>30</td><td>0</td><td>NLP</td><td>다목적 agentic workflow 생성을 Pareto front 탐색 문제로 푼 방법임</td></tr>
<tr><td>492</td><td><a href='https://arxiv.org/abs/2609.38359'>Beyond Mode Collapse: Generating Diverse Synthetic Expert Conversations via Generative Flow Networks</a></td><td>30</td><td>0</td><td>NLP</td><td>GFlowNet으로 합성 대화 데이터의 mode collapse를 완화한 방법임</td></tr>
<tr><td>493</td><td><a href='https://arxiv.org/abs/2609.38379'>Aligned Data Can Induce Misalignment via Context Confusion</a></td><td>30</td><td>0</td><td>NLP</td><td>한 맥락에서 정렬된 데이터가 다른 맥락에서 misalignment를 유발하는 context confusion 현상을 규명함</td></tr>
<tr><td>494</td><td><a href='https://arxiv.org/abs/2609.38385'>Fine-Tuning Diffusion Language Models with Context Selection and Target Weighting</a></td><td>30</td><td>0</td><td>NLP</td><td>diffusion LM fine-tuning에서 context 선택과 target 가중치를 submodular 목적함수로 최적화함</td></tr>
<tr><td>495</td><td><a href='https://arxiv.org/abs/2609.38411'>A Competing-Hazards Systematization of Loss of Control in Autonomous Agents</a></td><td>30</td><td>0</td><td>NLP</td><td>AI agent의 loss-of-control 사고를 경쟁 위험(competing-hazards) 모델로 체계화한 분석임</td></tr>
<tr><td>496</td><td><a href='https://arxiv.org/abs/2609.38458'>PrivMeSA: Privacy-Aware Self-Evolving Multi-Agent System for Medicine via Local-Remote LLM Collaboration</a></td><td>30</td><td>0</td><td>NLP</td><td>로컬-원격 LLM 협업에서 환자정보 노출을 RL로 제어하는 의료 멀티에이전트 시스템임</td></tr>
<tr><td>497</td><td><a href='https://arxiv.org/abs/2609.38577'>Conditional Generation of Creative Chess Puzzles with Diffusion Models</a></td><td>30</td><td>0</td><td>NLP</td><td>masked diffusion과 RL로 테마 조건부 체스 퍼즐을 생성하는 창의적 생성 연구임</td></tr>
<tr><td>498</td><td><a href='https://arxiv.org/abs/2609.38621'>When Scientific Contradictions Are Lost in Translation</a></td><td>30</td><td>0</td><td>NLP</td><td>과학적 모순 판단에서 모델이 formal 제약 대신 생물학적 기대를 따르는 편향을 발견함</td></tr>
<tr><td>499</td><td><a href='https://arxiv.org/abs/2609.38699'>Budget Boundary Effects in Test-Time Mathematical Reasoning</a></td><td>30</td><td>0</td><td>NLP</td><td>test-time 토큰 예산 경계에서 strict/advisory 중단 정책의 효과를 세밀히 분석한 연구임</td></tr>
<tr><td>500</td><td><a href='https://arxiv.org/abs/2609.38757'>Self-Evolving Algorithm-Design Agents: Escaping In-Context Evolutionary Stagnation via Population-Curated Policy Optimization</a></td><td>30</td><td>0</td><td>NLP</td><td>in-context evolutionary 정체를 파라메트릭 자기진화로 극복하는 population-curated policy optimization임</td></tr>
<tr><td>501</td><td><a href='https://arxiv.org/abs/2609.38817'>When Reasoning Goes Astray: Attention Dynamics of Uncontrolled Reasoning</a></td><td>30</td><td>0</td><td>NLP</td><td>추론 모델의 attention 동역학으로 반복 루프 발생을 실시간 감지·교정하는 방법임</td></tr>
<tr><td>502</td><td><a href='https://arxiv.org/abs/2609.38917'>How Much Can Reliability Drift Under a Fixed Confidence Distribution?</a></td><td>30</td><td>0</td><td>LG</td><td>신뢰도 분포가 고정된 상태에서 신뢰성이 공변량 이동에 따라 얼마나 흔들릴 수 있는지 이론적으로 분석함</td></tr>
<tr><td>503</td><td><a href='https://arxiv.org/abs/2609.38956'>Routing Probes Can Improve Without New Information: An Exact-Null Audit of Uncertainty Beyond Model Outputs</a></td><td>30</td><td>0</td><td>CV</td><td>routing signal이 오류 예측에 추가 정보를 주는지 exact-null로 엄밀히 재검증해 기존 주장 다수가 아티팩트임을 보임</td></tr>
<tr><td>504</td><td><a href='https://arxiv.org/abs/2609.39026'>Search Shapes Conclusions: Auditing Evidence Selection Bias in Deep Research Agents</a></td><td>30</td><td>0</td><td>NLP</td><td>deep research agent의 적응적 검색이 만드는 evidence selection bias를 인과적으로 보정하는 방법임</td></tr>
<tr><td>505</td><td><a href='https://arxiv.org/abs/2609.39148'>Do Self-Evolving Skills Generalize to Held-Out Tasks?</a></td><td>30</td><td>0</td><td>NLP</td><td>self-evolving skill이 held-out task에 일반화되는지 검증하고 task별 재작성 방법(GSO)을 제안함</td></tr>
<tr><td>506</td><td><a href='https://arxiv.org/abs/2609.39220'>Learning Process Rewards via Reasoning State Propagation</a></td><td>30</td><td>0</td><td>NLP</td><td>reasoning 상태의 valid/invalid 전이를 모델링해 process reward를 outcome label로도 학습시키는 방법임</td></tr>
<tr><td>507</td><td><a href='https://arxiv.org/abs/2609.39259'>Effective Does Not Mean Useful: Conditional Functional Substitutability for Redundancy and Scaling in Transformers</a></td><td>30</td><td>0</td><td>LG</td><td>입력조건부 함수적 대체가능성(CFS)으로 transformer의 redundancy와 scaling 관계를 분석한 연구임</td></tr>
<tr><td>508</td><td><a href='https://arxiv.org/abs/2609.39494'>Disentangling Self-Distillation: Measuring and Modeling Acquisition and Retention</a></td><td>30</td><td>0</td><td>NLP</td><td>self-distillation의 세 축(rollout source, teacher coupling, KL 방향)을 1200회 실험으로 분리 분석함</td></tr>
<tr><td>509</td><td><a href='https://arxiv.org/abs/2609.39702'>A helps B while B hurts A: directed transfer in instruction-tuning mixture</a></td><td>30</td><td>0</td><td>NLP</td><td>instruction-tuning에서 A가 B를 돕지만 B는 A를 해치는 비대칭 전이를 transfer map으로 예측한 연구임</td></tr>
<tr><td>510</td><td><a href='https://arxiv.org/abs/2609.39933'>ConflictGuide: AutoResearch Improves When Competing Behaviors Are Made Visible</a></td><td>30</td><td>0</td><td>NLP</td><td>모델 설계에서 서로 충돌하는 행동을 가시화해 autoresearch 탐색 정체를 완화하는 방법임</td></tr>
<tr><td>511</td><td><a href='https://arxiv.org/abs/2609.38719'>FlapKAD: A Simulation Dataset of Coupled Wing Kinematics and Aerodynamic Dynamics for Flapping-Wing Aerial Vehicles</a></td><td>28</td><td>3</td><td>RL</td><td>flapping-wing 비행체의 운동학-공력 결합 시뮬레이션 데이터셋임. 벤치마크 제공이 주 기여라 니치한 응용 영역임.</td></tr>
<tr><td>512</td><td><a href='https://arxiv.org/abs/2609.38714'>Hard-Region Supervision: #1 on the Waymo Open Dataset 2D Video Panoptic Segmentation Leaderboard</a></td><td>28</td><td>1</td><td>CV</td><td>Waymo panoptic segmentation 챌린지 1위 기술 보고서임. hard region 보조 head 추가와 테스트 타임 앙상블 조합으로, 방법론적 novelty는 낮은 engineering 개선임</td></tr>
<tr><td>513</td><td><a href='https://arxiv.org/abs/2609.39128'>GeoGAT: Bidirectional Temporal Sampling Meets Hierarchical Graph Attention for Global Video Geo-localization</a></td><td>28</td><td>1</td><td>Navigation</td><td>양방향 시간 샘플링과 graph attention으로 비디오 geo-localization을 하는 GeoGAT 제안임. 계층 간 예측 충돌 제거라는 기여가 있으나 응용이 영상 위치 추정으로 제한됨</td></tr>
<tr><td>514</td><td><a href='https://arxiv.org/abs/2609.39467'>DensePed-Lite: Quality-Aware Adaptive Detection for Dense Pedestrians under Occlusion</a></td><td>28</td><td>1</td><td>CV</td><td>occlusion 상황에서 품질 인지 기반으로 동작하는 경량 보행자 검출기 DensePed-Lite 제안임. 경량화에 초점이 맞춰져 있어 우선 평가 대상이 아님</td></tr>
<tr><td>515</td><td><a href='https://arxiv.org/abs/2609.39492'>Front-to-Back: Benchmarking Vision-Language Models for Asymmetric Cross-View Vehicle Re-Identification</a></td><td>28</td><td>1</td><td>CV</td><td>전방-후방 카메라 간 차량 재식별을 VLM으로 벤치마킹한 연구임. 응용이 교통 감시에 국한됨</td></tr>
<tr><td>516</td><td><a href='https://arxiv.org/abs/2609.39832'>P-SRM: Selective Recovery of Rejected Predictions in Visual Tracking</a></td><td>28</td><td>1</td><td>CV</td><td>tracking에서 기각된 후보 중 쓸만한 것을 복구하는 P-SRM 제안임. tracking 성능 개선 수준의 engineering 기여임</td></tr>
<tr><td>517</td><td><a href='https://arxiv.org/abs/2609.40014'>Can We Anticipate Violence? Multimodal Learning from Pre-Incident Behavioral Cues</a></td><td>28</td><td>1</td><td>Video</td><td>사건 발생 전 행동 단서로 폭력을 예측하는 멀티모달 분류 연구임. 감시 응용으로 로보틱스와는 거리가 있음</td></tr>
<tr><td>518</td><td><a href='https://arxiv.org/abs/2609.40317'>GLARE: Generating Listening Heads with Appropriate Reactions</a></td><td>28</td><td>1</td><td>Video</td><td>대화 상황에서 청자의 반응을 생성하는 GLARE 제안임. 사회적 반응 생성이라는 점에서 embodied 사회적 상호작용과 맞닿지만 본 논문은 아바타 생성에 그침</td></tr>
<tr><td>519</td><td><a href='https://arxiv.org/abs/2609.38618'>Differentiable Structure Learning for Cyclic Linear Gaussian Models with Latent Confounders</a></td><td>28</td><td>1</td><td>LG</td><td>순환 구조 causal discovery 이론 확장이나 로보틱스 적용 없음</td></tr>
<tr><td>520</td><td><a href='https://arxiv.org/abs/2609.40075'>Accelerated Algorithm for Sparse Regularized Partial Optimal Transport</a></td><td>28</td><td>1</td><td>LG</td><td>sparse regularized partial optimal transport 가속 알고리즘, point cloud registration 실험 포함하나 핵심은 최적화 이론임</td></tr>
<tr><td>521</td><td><a href='https://arxiv.org/abs/2609.40147'>Policy Iteration Is Not Strongly Polynomial for Deterministic Markov Decision Processes: The Price of Algorithmic Anarchy</a></td><td>28</td><td>1</td><td>RL</td><td>MDP policy iteration 하한 증명으로 이론 알고리즘 논문임. 로보틱스 적용성 낮음.</td></tr>
<tr><td>522</td><td><a href='https://arxiv.org/abs/2609.38914'>Risk-Aware Adaptive Evaluation: Finding High-Impact Failures Under Limited Budgets</a></td><td>28</td><td>1</td><td>NLP</td><td>실패가 드물고 영향이 다른 상황에서 Thompson sampling으로 평가 예산을 위험 가중 배분하는 방법임</td></tr>
<tr><td>523</td><td><a href='https://arxiv.org/abs/2609.39518'>Referential Uncertainty in Human--AI Collaboration</a></td><td>28</td><td>1</td><td>Multimodal</td><td>퍼즐 협업에서 VLM이 지칭 모호성을 내부적으로 더 잘 포착하지만 거의 표출하지 않음을 보임</td></tr>
<tr><td>524</td><td><a href='https://arxiv.org/abs/2609.38325'>Strike a Chord! Modal Kinetic Typography</a></td><td>28</td><td>0</td><td>CV</td><td>글자 모드 진동으로 kinetic typography를 생성하는 그래픽스 작업임. 로보틱스와 무관하고 응용 범위도 좁음</td></tr>
<tr><td>525</td><td><a href='https://arxiv.org/abs/2609.38622'>Eulerian Motion Reconstruction for Water Scenery</a></td><td>28</td><td>0</td><td>3D Vision</td><td>물 장면을 Eulerian motion field로 표현해 루핑 4D 재구성을 하는 그래픽스 작업임. 로보틱스와 무관함</td></tr>
<tr><td>526</td><td><a href='https://arxiv.org/abs/2609.38705'>SCALE: Synthetic Calibration via Agreement Labeling in Embedding Space</a></td><td>28</td><td>0</td><td>CV</td><td>병리 파운데이션 모델의 calibration을 pathologist agreement 기반으로 개선하는 SCALE 제안임. 의료 영상 한정 응용임</td></tr>
<tr><td>527</td><td><a href='https://arxiv.org/abs/2609.38747'>Consensus-Aware Multi-Source Fusion for Reference-Guided Camouflaged Object Detection</a></td><td>28</td><td>0</td><td>CV</td><td>reference 샘플을 이용한 camouflaged object detection 개선임. niche한 segmentation 태스크로 로보틱스와 무관함</td></tr>
<tr><td>528</td><td><a href='https://arxiv.org/abs/2609.38823'>DecoMoE: Decoupling Visual Propagation and Expert Computation for Efficient Multimodal MoE Inference</a></td><td>28</td><td>0</td><td>Multimodal</td><td>visual token propagation과 expert 연산을 분리해 MoE 추론을 압축하는 DecoMoE 제안임. 효율화 위주 기여라 우선 평가 대상이 아님</td></tr>
<tr><td>529</td><td><a href='https://arxiv.org/abs/2609.39134'>Feature-Aware Token Attack for Compression-Triggered Stealthy Failures in Large Vision-Language Models</a></td><td>28</td><td>0</td><td>Multimodal</td><td>토큰 압축 후에만 발생하는 적대적 실패를 유발하는 FATA 공격 제안임. 보안 분석으로 로보틱스와 무관함</td></tr>
<tr><td>530</td><td><a href='https://arxiv.org/abs/2609.39273'>MegaAvatar: Controllable Talking Avatar Generation</a></td><td>28</td><td>0</td><td>Video</td><td>SMPL-X 기반 3D guidance로 talking avatar의 신체·머리 동작을 제어하는 MegaAvatar 제안임. 아바타 생성 응용으로 로보틱스와 무관함</td></tr>
<tr><td>531</td><td><a href='https://arxiv.org/abs/2609.39548'>Learning Normal Diffusion Dynamics for Backdoor Defense in Text-to-Image Models</a></td><td>28</td><td>0</td><td>CV</td><td>정상 diffusion 궤적의 전이 패턴을 학습해 backdoor를 탐지하는 NDDL 제안임. T2I 보안 방어로 로보틱스와 무관함</td></tr>
<tr><td>532</td><td><a href='https://arxiv.org/abs/2609.39585'>A Generalizable and Explainable Framework for Synthetic Video Detection Using First-Digit Gradient Statistics</a></td><td>28</td><td>0</td><td>CV</td><td>Sobel gradient의 first-digit 분포로 AI 생성 비디오를 탐지하는 방법임. 포렌식 응용으로 로보틱스와 무관함</td></tr>
<tr><td>533</td><td><a href='https://arxiv.org/abs/2609.39605'>FOMO: Forget the Concept, Don&#x27;t Miss Out on the Scene in Selective Video Unlearning</a></td><td>28</td><td>0</td><td>Video</td><td>장면 보존을 우선시하는 선택적 비디오 unlearning FOMO 제안임. 안전성 콘텐츠 제거 목적으로 로보틱스와 무관함</td></tr>
<tr><td>534</td><td><a href='https://arxiv.org/abs/2609.39688'>ShieldCLIP: Selective Safety Alignment for Harmful Content Mitigation in Multimodal Foundation Models</a></td><td>28</td><td>0</td><td>Multimodal</td><td>모달리티별 안전 상태에 조건화된 CLIP 안전 정렬 ShieldCLIP 제안임. 유해 콘텐츠 완화 목적으로 로보틱스와 무관함</td></tr>
<tr><td>535</td><td><a href='https://arxiv.org/abs/2609.40322'>MatLoom: Layered Text-to-Material Generation in a Compact Program Space</a></td><td>28</td><td>0</td><td>CV</td><td>텍스트로 레이어 프로그램을 생성해 재질을 만드는 MatLoom 제안임. 그래픽스 에셋 생성 응용으로 로보틱스와 무관함</td></tr>
<tr><td>536</td><td><a href='https://arxiv.org/abs/2609.38198'>FlashDiffusion: Fused Tiled Kernel Spectral Decomposition</a></td><td>28</td><td>0</td><td>LG</td><td>GPU 타일 연산으로 고차원 diffusion map 고유값 분해를 가속하는 FlashDiffusion 제안임. 커널 방법 효율화 기여로 로보틱스와 무관함</td></tr>
<tr><td>537</td><td><a href='https://arxiv.org/abs/2609.38414'>Synthesis Without Training: An Inference-Only Pipeline for Tabular, Temporal, and Relational Synthetic Data</a></td><td>28</td><td>0</td><td>LG</td><td>학습 없이 통계 프로파일과 LLM으로 합성 데이터 생성기를 컴파일하는 GENSCRIPT 제안임. 데이터 합성 도구로 로보틱스와 무관함</td></tr>
<tr><td>538</td><td><a href='https://arxiv.org/abs/2609.38517'>Does Text Steer Neural PDE Surrogates? A Controlled Diagnostic with OperatorCLIP</a></td><td>28</td><td>0</td><td>LG</td><td>텍스트 조건이 neural PDE surrogate를 실제로 조향하는지 통제 진단한 연구임. 방법론적 경고 성격의 연구로 로보틱스와는 거리가 있음</td></tr>
<tr><td>539</td><td><a href='https://arxiv.org/abs/2609.38538'>ReLaG: A Scalable Framework Generalizing Random Splits to Data with Latent Relations</a></td><td>28</td><td>0</td><td>LG</td><td>잠재적으로 관련된 샘플을 고려해 독립적인 train-test split을 만드는 ReLaG 제안임. 평가 방법론 기여로 로보틱스와 무관함</td></tr>
<tr><td>540</td><td><a href='https://arxiv.org/abs/2609.38565'>The Advantages of Fresh Sketching for Ridge Regression</a></td><td>28</td><td>0</td><td>LG</td><td>매 step마다 새로운 sketch를 쓰는 것이 ridge regression 수렴에 이점이 있음을 보인 이론 연구임. 수치선형대수 기여로 로보틱스와 무관함</td></tr>
<tr><td>541</td><td><a href='https://arxiv.org/abs/2609.38587'>NeurDuo-EEG: A Long-Sequence EEG Foundation Model with Persistent State and Explicit Memory</a></td><td>28</td><td>0</td><td>LG</td><td>EEG foundation model 메모리 구조 개선인데 로보틱스와 무관하고 benchmark 개선 수준임</td></tr>
<tr><td>542</td><td><a href='https://arxiv.org/abs/2609.38647'>Uncertainty-Normalized Margins for Direct Preference Optimization</a></td><td>28</td><td>0</td><td>LG</td><td>DPO의 preference margin 불확실성 보정, LLM alignment 세부 개선임</td></tr>
<tr><td>543</td><td><a href='https://arxiv.org/abs/2609.38776'>Distilling Diffusion Score Discrepancy for Efficient Training Data Attribution</a></td><td>28</td><td>0</td><td>LG</td><td>diffusion model training data attribution을 score discrepancy로 distill, 생성모델 해석 도구임</td></tr>
<tr><td>544</td><td><a href='https://arxiv.org/abs/2609.38784'>Does a Shared Temperature Imply a Shared Angular Scale in Probabilistic Contrastive Learning?</a></td><td>28</td><td>0</td><td>LG</td><td>vMF 기반 probabilistic contrastive learning의 temperature-scale 이론 분석, representation learning 이론임</td></tr>
<tr><td>545</td><td><a href='https://arxiv.org/abs/2609.38789'>LEARN-TS: LLM-Enhanced Alignment and Reconstruction with Normality Guidance for Multivariate Time-Series Anomaly Detection</a></td><td>28</td><td>0</td><td>LG</td><td>LLM 의미 정보로 시계열 이상탐지 재구성 가이드, 로보틱스 무관</td></tr>
<tr><td>546</td><td><a href='https://arxiv.org/abs/2609.38840'>scTrilemma: Balancing Identity, Invariance, and Fidelity in Single-Cell Representation Learning</a></td><td>28</td><td>0</td><td>LG</td><td>단일세포 표현학습의 identity-invariance-fidelity trilemma 분석, 생물정보학 문제임</td></tr>
<tr><td>547</td><td><a href='https://arxiv.org/abs/2609.38884'>Right Answers, Costly Models: The Efficiency Gap in LLM-based Optimization Modeling</a></td><td>28</td><td>0</td><td>LG</td><td>LLM 최적화 모델링의 정확도-효율성 괴리 분석, 운영연구 문제로 로보틱스 무관</td></tr>
<tr><td>548</td><td><a href='https://arxiv.org/abs/2609.38895'>Unmerge: Efficient Machine Unlearning via Task Arithmetic</a></td><td>28</td><td>0</td><td>LG</td><td>task arithmetic 관점의 machine unlearning 기법, 모델 편집 문제로 로보틱스 무관</td></tr>
<tr><td>549</td><td><a href='https://arxiv.org/abs/2609.38901'>Certified Approximation for Interpretable Representer Landmarks</a></td><td>28</td><td>0</td><td>LG</td><td>representer explanation의 근사 오차를 top-K 랭킹까지 인증하는 프레임워크, interpretability 도구임</td></tr>
<tr><td>550</td><td><a href='https://arxiv.org/abs/2609.39019'>Synchronous Multi-view Neural Diffusion</a></td><td>28</td><td>0</td><td>Multimodal</td><td>intra/inter-view fusion을 동시에 수행하는 diffusion 기반 멀티뷰 학습, 로보틱스 무관</td></tr>
<tr><td>551</td><td><a href='https://arxiv.org/abs/2609.39055'>The Missing Coefficients: Bayesian Pairwise Merging for Model Personalization</a></td><td>28</td><td>0</td><td>LG</td><td>pairwise 선택으로 reward 가중치 베이지안 추론해 모델 병합 개인화, LLM 개인화 기법임</td></tr>
<tr><td>552</td><td><a href='https://arxiv.org/abs/2609.39099'>A Generalisation Signal Need Not Be a Model-Selection Signal</a></td><td>28</td><td>0</td><td>LG</td><td>generalisation 신호가 model selection 신호와 다를 수 있음을 생물학 태스크에서 보임, 메타과학적 분석임</td></tr>
<tr><td>553</td><td><a href='https://arxiv.org/abs/2609.39123'>Prequential E-Values for Selected-GP Near-Optimality Certificates</a></td><td>28</td><td>0</td><td>LG</td><td>GP 기반 블랙박스 최적화 정지규칙을 e-value로 감사가능하게 만드는 기법, 베이지안 최적화 통계 연구임</td></tr>
<tr><td>554</td><td><a href='https://arxiv.org/abs/2609.39124'>CDMD: A Cross-Dataset Mixed-Type Diffusion Model for Tabular Data</a></td><td>28</td><td>0</td><td>LG</td><td>이질적 스키마 간 공동학습 가능한 tabular diffusion model, 표 형식 데이터 생성 기법임</td></tr>
<tr><td>555</td><td><a href='https://arxiv.org/abs/2609.39275'>ReTaCo: Residual-Target Control for On-Policy Distillation</a></td><td>28</td><td>0</td><td>NLP</td><td>on-policy distillation의 top-k 근사 오류를 residual target으로 보정, LLM distillation 기법임</td></tr>
<tr><td>556</td><td><a href='https://arxiv.org/abs/2609.39291'>Physics-Informed Method of Group Data Handling: Adaptive Construction of Functional Representations with an Application to the Navier-Stokes Equations</a></td><td>28</td><td>0</td><td>LG</td><td>Navier-Stokes용 physics-informed 함수표현 적응적 구성법, 과학계산 문제로 로보틱스 무관</td></tr>
<tr><td>557</td><td><a href='https://arxiv.org/abs/2609.39321'>GRPO Training Dynamics for Small Language Models</a></td><td>28</td><td>0</td><td>LG</td><td>소형 언어모델의 GRPO 학습 동역학 체계적 분석, 실용적 가이드 제공 수준임</td></tr>
<tr><td>558</td><td><a href='https://arxiv.org/abs/2609.39329'>PatchKV: Weight-Space Compensation of KV Cache</a></td><td>28</td><td>0</td><td>LG</td><td>weight-space patch로 KV cache 압축 손실 보상하는 PatchKV, LLM 추론 효율화 기법임</td></tr>
<tr><td>559</td><td><a href='https://arxiv.org/abs/2609.39338'>Learning Beyond Full Imitation: Task-Preserving Knowledge Distillation</a></td><td>28</td><td>0</td><td>LG</td><td>full imitation과 conditional learning의 분리를 이론화한 task-preserving distillation, 분류 모델 distillation 기법임</td></tr>
<tr><td>560</td><td><a href='https://arxiv.org/abs/2609.39357'>Robustifying Asynchronous SGD via Soft Throttling</a></td><td>28</td><td>0</td><td>LG</td><td>비동기 SGD의 Byzantine robustness를 soft throttling으로 개선, 분산학습 연구임</td></tr>
<tr><td>561</td><td><a href='https://arxiv.org/abs/2609.39374'>Wavelet Flow Matching for Time Series</a></td><td>28</td><td>0</td><td>LG</td><td>wavelet 도메인 flow matching으로 다변량 시계열 생성, 데이터 증강 응용임</td></tr>
<tr><td>562</td><td><a href='https://arxiv.org/abs/2609.39390'>Decoupled and Distilled: Task-Adaptive LoRA-Teachers with Ensemble Knowledge Transfer for Few-Shot Class-Incremental Learning</a></td><td>28</td><td>0</td><td>LG</td><td>few-shot class-incremental learning에 task-adaptive LoRA teacher 앙상블 distillation, 지속학습 기법임</td></tr>
<tr><td>563</td><td><a href='https://arxiv.org/abs/2609.39405'>No Task Vector Is an Island: A Comprehensive Study on the Composability of Task Vectors from On-Policy Distillation</a></td><td>28</td><td>0</td><td>LG</td><td>on-policy distillation task vector의 조합가능성을 RL task vector와 비교 분석, 모델 병합 연구임</td></tr>
<tr><td>564</td><td><a href='https://arxiv.org/abs/2609.39488'>Correcting CondOT: Exact Finite-Step Sampling in Gaussian Flow Matching</a></td><td>28</td><td>0</td><td>LG</td><td>가우시안 타겟 flow matching의 finite-step sampling 오차를 CondOT 스케줄로 보정, 생성모델 이론 기여임</td></tr>
<tr><td>565</td><td><a href='https://arxiv.org/abs/2609.39561'>Candidate Retention for Abductive Learning</a></td><td>28</td><td>0</td><td>LG</td><td>abductive learning의 후보 pseudo-label 유지 전략 ACR, neurosymbolic 학습 기법임</td></tr>
<tr><td>566</td><td><a href='https://arxiv.org/abs/2609.39629'>Certification-Based Differentially Private Learning</a></td><td>28</td><td>0</td><td>LG</td><td>형식적 방법 기반 differential privacy 분석을 회귀 설정으로 일반화, 프라이버시 이론 연구임</td></tr>
<tr><td>567</td><td><a href='https://arxiv.org/abs/2609.39658'>Graph Residual Conjugate Diffusion: SNR-Equalized Heat Flow for Graph Signals</a></td><td>28</td><td>0</td><td>LG</td><td>그래프 신호의 모드별 SNR을 균등화하는 diffusion 기법, 그래프 생성모델 효율화임</td></tr>
<tr><td>568</td><td><a href='https://arxiv.org/abs/2609.39692'>GFD-OPD: Guidance-Folded On-Policy Distillation of Diffusion Models Across Scales</a></td><td>28</td><td>0</td><td>LG</td><td>큰 teacher에서 작은 student로의 diffusion on-policy distillation 실패 원인 규명 및 해법, 생성모델 압축 기법임</td></tr>
<tr><td>569</td><td><a href='https://arxiv.org/abs/2609.39737'>A library for differentiable signal processing and machine learning on the sphere</a></td><td>28</td><td>0</td><td>LG</td><td>구면 데이터용 미분가능 신호처리·ML 라이브러리, 과학계산 인프라 기여임</td></tr>
<tr><td>570</td><td><a href='https://arxiv.org/abs/2609.39777'>GraphMAS: A Systematic Benchmark of Multi-Agent Coordination for Graph Learning</a></td><td>28</td><td>0</td><td>LG</td><td>그래프 학습을 위한 LLM 멀티에이전트 협력 벤치마크, 그래프 추론 연구임</td></tr>
<tr><td>571</td><td><a href='https://arxiv.org/abs/2609.39792'>TopTimeNet: Topologically-assisted time-series classification model</a></td><td>28</td><td>0</td><td>LG</td><td>위상학적 특징으로 주기/카오스 동역학 분류를 경량화, 물리 시계열 분류 기법임</td></tr>
<tr><td>572</td><td><a href='https://arxiv.org/abs/2609.39801'>RATIO: Reasoning Analysis and Token-level Inference Optimization for Quantized Reasoning Models</a></td><td>28</td><td>0</td><td>LG</td><td>양자화된 추론모델의 overthinking token 식별 및 토큰별 penalty, LLM 추론 효율화 기법임</td></tr>
<tr><td>573</td><td><a href='https://arxiv.org/abs/2609.39848'>Predicting Multi-View Rashomon Representation: Can We Learn Where Models Disagree?</a></td><td>28</td><td>0</td><td>LG</td><td>단일 표현에서 모델 간 representation disagreement를 예측하는 신뢰도 추정 기법, foundation model 평가 연구임</td></tr>
<tr><td>574</td><td><a href='https://arxiv.org/abs/2609.39877'>Algorithmic Recourse Under Competition</a></td><td>28</td><td>0</td><td>LG</td><td>경쟁 상황에서 algorithmic recourse의 acceptance threshold 변화 문제 해결, 공정성·의사결정 연구임</td></tr>
<tr><td>575</td><td><a href='https://arxiv.org/abs/2609.39934'>Reliability-Aware Checkpoint Selection for Domain Generalization</a></td><td>28</td><td>0</td><td>CV</td><td>domain generalization에서 target 데이터 없이 reliability 기준 체크포인트 선택, 모델 선택 방법론임</td></tr>
<tr><td>576</td><td><a href='https://arxiv.org/abs/2609.40047'>Gromov-Wasserstein Distillation for Inductive Multi-View Embedding</a></td><td>28</td><td>0</td><td>LG</td><td>Gromov-Wasserstein 임베딩을 inductive하게 만드는 barycentric distillation, 표현학습 방법론임</td></tr>
<tr><td>577</td><td><a href='https://arxiv.org/abs/2609.40063'>LARC: Low-Rank Adaptive Residual Connections for Learning in Frozen Models</a></td><td>28</td><td>0</td><td>NLP</td><td>frozen model에 저랭크 residual로 빠른 피드백 학습 부여하는 LARC, 온라인 적응 기법임</td></tr>
<tr><td>578</td><td><a href='https://arxiv.org/abs/2609.40089'>Replay on Demand: An Emergent Curriculum for Balancing Adaptation and Forgetting in Continued Pretraining</a></td><td>28</td><td>0</td><td>LG</td><td>지속 사전학습의 replay 배분을 모델의 학습 동역학에서 online으로 유도, continual learning 기법임</td></tr>
<tr><td>579</td><td><a href='https://arxiv.org/abs/2609.40143'>From DNA Design to DNA Slimming: Auditable Agentic Discovery of a Deletion-Only Designer</a></td><td>28</td><td>0</td><td>LG</td><td>coding agent로 deletion-only DNA 서열 슬리밍 설계자를 탐색, 생물학 에이전틱 발견 연구임</td></tr>
<tr><td>580</td><td><a href='https://arxiv.org/abs/2609.40235'>Distribution Matching Distillation for Continuous Diffusion Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>연속 diffusion 언어모델 distillation으로 추론 단계 축소함. 텍스트 생성 효율화 연구임.</td></tr>
<tr><td>581</td><td><a href='https://arxiv.org/abs/2609.38256'>Framing the Narrative: Ideological Mimicry in Large Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>사용자 발화의 정치적 신호에 LLM 답변이 따라 바뀌는 ideological mimicry를 측정함. 사회적 영향 연구임.</td></tr>
<tr><td>582</td><td><a href='https://arxiv.org/abs/2609.38406'>Evaluating Whether LLMs Can Reliably Connect the DOTs?</a></td><td>28</td><td>0</td><td>NLP</td><td>서사 중간 문장을 채우는 narrative infilling 벤치마크임. 모델 크기가 품질을 보장하지 않는다는 결과를 보고함.</td></tr>
<tr><td>583</td><td><a href='https://arxiv.org/abs/2609.38799'>Overlap, Unique and Conflict: Can LLMs Extract What They Can Recognize?</a></td><td>28</td><td>0</td><td>NLP</td><td>두 서사 간 overlap·unique·conflict 절을 추출하는 과제를 정의함. cross-narrative 이해 벤치마크임.</td></tr>
<tr><td>584</td><td><a href='https://arxiv.org/abs/2609.38831'>Forging LLM Authorship Fingerprints with Targeted Rewriting</a></td><td>28</td><td>0</td><td>NLP</td><td>요약문을 다른 모델 글쓰기 지문처럼 보이게 다시 쓰는 fingerprint transfer 공격임. 모델 귀속 보안 연구임.</td></tr>
<tr><td>585</td><td><a href='https://arxiv.org/abs/2609.39072'>Beyond Text: LLM-Based Dimensional Emotion Evaluation in Multimodal Dialogue</a></td><td>28</td><td>0</td><td>Multimodal</td><td>음향 단서를 자연어로 서술해 LLM이 VAD 감정을 평가하게 함. 대화 감정인식 응용 연구임.</td></tr>
<tr><td>586</td><td><a href='https://arxiv.org/abs/2609.39884'>OPSRD: On-Policy Self-Role Distillation</a></td><td>28</td><td>0</td><td>NLP</td><td>역할 프롬프트를 teacher로 쓰는 on-policy self-distillation 변형임. 수학 벤치마크에 한정</td></tr>
<tr><td>587</td><td><a href='https://arxiv.org/abs/2609.38670'>Where Scientific Search Agents Fail: Decision-Checkpoint Auditing of Exposure and Inspection Attempts</a></td><td>28</td><td>0</td><td>NLP</td><td>과학 검색 agent의 실패를 노출·검토·수용 단계로 분해해 감사하는 방법론임</td></tr>
<tr><td>588</td><td><a href='https://arxiv.org/abs/2609.38684'>Concept-Grounded Attention: A Controlled Evaluation of Graph-Injected Attention, Temporal Versioning, and Epistemic Status</a></td><td>28</td><td>0</td><td>NLP</td><td>개념 그래프를 transformer attention에 주입하는 방법을 disabled-mechanism baseline으로 엄밀히 검증함. 많은 기존 주장이 통제군에서 사라짐을 보임</td></tr>
<tr><td>589</td><td><a href='https://arxiv.org/abs/2609.38743'>Learning to Route in Visual Space via Multi-Step Embedding Retrieval</a></td><td>28</td><td>0</td><td>CV</td><td>visual agentic search에서 다단계 탐색을 retriever에 넘기는 end-to-end 학습 방법임</td></tr>
<tr><td>590</td><td><a href='https://arxiv.org/abs/2609.38766'>PathAnchor: Path-Structured Evidence for Scientific Agents</a></td><td>28</td><td>0</td><td>NLP</td><td>경로 구조를 보존하는 evidence workspace로 과학 질의응답의 출처 정확도를 높인 시스템임</td></tr>
<tr><td>591</td><td><a href='https://arxiv.org/abs/2609.38798'>GraphCert: Bootstrap Agentic Graph Reasoning with Certified Evidence Rubrics</a></td><td>28</td><td>0</td><td>NLP</td><td>증거 rubric으로 그래프 reasoning agent를 레이블 없이 부트스트랩하는 GRPO 기반 방법임</td></tr>
<tr><td>592</td><td><a href='https://arxiv.org/abs/2609.38850'>OpenJev-RLCD: A Working RLCD Implementation</a></td><td>28</td><td>0</td><td>NLP</td><td>보정된 결정을 위한 RLCD를 실제로 동작하게 만든 2단계(calibrate-then-reinforce) 구현임</td></tr>
<tr><td>593</td><td><a href='https://arxiv.org/abs/2609.38912'>Composing Task-specific Agent Harnesses at Test Time with Reusable Primitives</a></td><td>28</td><td>0</td><td>NLP</td><td>재사용 가능한 harness primitive를 테스트타임에 조합해 task별 harness를 만드는 방법임</td></tr>
<tr><td>594</td><td><a href='https://arxiv.org/abs/2609.38929'>Learning What to Forget: Distributional Unlearning for LLM Representation Spaces</a></td><td>28</td><td>0</td><td>NLP</td><td>비모수적 분포 기반 unlearning으로 forget 샘플 선택을 최적화하는 방법임</td></tr>
<tr><td>595</td><td><a href='https://arxiv.org/abs/2609.39139'>BELIEFRAG: Making Adaptive RAG State-Aware under Evolving Evidence</a></td><td>28</td><td>0</td><td>NLP</td><td>다단계 RAG에서 증거 상태(충분성·신뢰성·충돌)를 명시적으로 유지하는 closed-loop controller임</td></tr>
<tr><td>596</td><td><a href='https://arxiv.org/abs/2609.39143'>RefCon: Iterative Refinement and Contrastive Memory Extraction for Context-Evolving Agent</a></td><td>28</td><td>0</td><td>NLP</td><td>gold label 없이 순차 self-refinement와 병렬 self-contrast로 agent memory 품질을 높이는 방법임</td></tr>
<tr><td>597</td><td><a href='https://arxiv.org/abs/2609.39149'>Rep2Skill: Representation-Guided Skill Self-Evolution for LLM Agents</a></td><td>28</td><td>0</td><td>NLP</td><td>텍스트 skill 진화에 agent 내부 표현 신호를 반영한 자기개선 프레임워크임</td></tr>
<tr><td>598</td><td><a href='https://arxiv.org/abs/2609.39294'>ANI: Adaptive Numerical Injection for Unifying Semantic and Arithmetic Representations in Numerical Reasoning</a></td><td>28</td><td>0</td><td>NLP</td><td>숫자 표현을 맥락에 따라 선택적으로 주입해 산술 reasoning을 개선한 방법임. EMNLP 2026</td></tr>
<tr><td>599</td><td><a href='https://arxiv.org/abs/2609.39325'>WorkGenesis: Building the Worlds That Teach Agents to Work</a></td><td>28</td><td>0</td><td>NLP</td><td>실제 아티팩트에 근거해 직업 작업 환경을 합성하는 agent 학습 데이터 프레임워크임</td></tr>
<tr><td>600</td><td><a href='https://arxiv.org/abs/2609.39343'>The Golden Path Hypothesis: Reusable Schedules in Diffusion Caching</a></td><td>28</td><td>0</td><td>CV</td><td>prompt-independent diffusion caching schedule이 prompt-specific schedule에 필적함을 보인 가설(GPH) 검증임</td></tr>
<tr><td>601</td><td><a href='https://arxiv.org/abs/2609.39351'>On the Complexity of Preference-Based Bandits</a></td><td>28</td><td>0</td><td>RL</td><td>일반 보상함수 클래스에서 preference-based bandit의 복잡도를 새 eluder dimension으로 분석한 이론 연구임</td></tr>
<tr><td>602</td><td><a href='https://arxiv.org/abs/2609.39392'>Experimental Experience Modeling for Autonomous Research</a></td><td>28</td><td>0</td><td>NLP</td><td>자율연구 agent가 실험 가치를 판단하도록 과거 실험 경험을 축적·재사용하는 프레임워크임</td></tr>
<tr><td>603</td><td><a href='https://arxiv.org/abs/2609.39394'>Can Computation from Earlier Problems Help LLMs Solve New Ones?</a></td><td>28</td><td>0</td><td>NLP</td><td>이전 문제 생성 시 계산된 KV를 재사용해 후속 문제 reasoning을 돕는 경량 학습 기법(STAIR)임</td></tr>
<tr><td>604</td><td><a href='https://arxiv.org/abs/2609.39551'>RankEvolve: A Reliable Multi-Agent Auto-Research Harness for Evolving Ranking Models</a></td><td>28</td><td>0</td><td>NLP</td><td>랭킹 모델 자동연구에서 실행 정확도를 보장하는 이기종 코딩에이전트 합성 harness임</td></tr>
<tr><td>605</td><td><a href='https://arxiv.org/abs/2609.39714'>ArchitectureIQ: On the Measure of Training Intuition</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM의 모델 훈련 직관을 사람과 비교해 네 가지 한계를 제시한 벤치마크임</td></tr>
<tr><td>606</td><td><a href='https://arxiv.org/abs/2609.39788'>Safety of Latent Communication in Multi-Agent Systems</a></td><td>28</td><td>0</td><td>NLP</td><td>잠재공간 통신 링크 학습이 안전정렬을 무너뜨릴 수 있음을 보이고 RL로 복구하는 연구임</td></tr>
<tr><td>607</td><td><a href='https://arxiv.org/abs/2609.39863'>FIGS: Evaluating Multi-Turn Sycophancy Without Penalizing Empathy</a></td><td>28</td><td>0</td><td>NLP</td><td>멀티턴 대화에서 sycophancy와 공감을 구분해 평가하는 프레임워크임</td></tr>
<tr><td>608</td><td><a href='https://arxiv.org/abs/2609.39903'>OSWorld-Science: A Benchmark of Computer Use Agents for Learning and Using Scientific Software</a></td><td>28</td><td>0</td><td>NLP</td><td>과학 소프트웨어 조작을 평가하는 computer-use agent 벤치마크임. VLM agent 한계를 정량화함</td></tr>
<tr><td>609</td><td><a href='https://arxiv.org/abs/2609.39989'>What Can Component-Replacement Evidence Establish? A Critical Scoping Review of Local Decisions in LLM Agents</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM agent의 component replacement 연구 348편을 scoping review로 재검토해 task-level 효과 귀속의 한계를 지적함</td></tr>
<tr><td>610</td><td><a href='https://arxiv.org/abs/2609.40115'>Unlearnable, or Unmeasured? On the Reliability of Difficulty Labels in RLVR</a></td><td>28</td><td>0</td><td>NLP</td><td>RLVR에서 unlearnable로 분류된 프롬프트가 사실은 측정 불안정성 때문임을 재분석함</td></tr>
<tr><td>611</td><td><a href='https://arxiv.org/abs/2609.40169'>Learning from Research: Toward Lifelong Agent Harness Evolution</a></td><td>28</td><td>0</td><td>NLP</td><td>최신 연구 논문을 바탕으로 agent harness를 능동적으로 진화시키는 프레임워크임</td></tr>
<tr><td>612</td><td><a href='https://arxiv.org/abs/2609.40330'>Turbo Harness: Instance-Adaptive Harness Optimization</a></td><td>28</td><td>0</td><td>NLP</td><td>전역 최적화된 harness를 인스턴스별로 패치하는 instance-adaptive harness 최적화 방법임</td></tr>
<tr><td>613</td><td><a href='https://arxiv.org/abs/2609.39203'>Benchmarking EMlog Calibration for Autonomous Surface Vehicles</a></td><td>26</td><td>2</td><td>Navigation</td><td>DVL 없는 상황의 EMLog 속도계 보정 기법 비교 연구임. 센서 캘리브레이션 수준의 응용 기여임.</td></tr>
<tr><td>614</td><td><a href='https://arxiv.org/abs/2609.38811'>DCM-SAM: Defect-Conditioned Mixture of LoRA Experts for NPU-Deployed AM Defect Segmentation</a></td><td>26</td><td>0</td><td>CV</td><td>SAM 백본에 defect별 LoRA expert를 붙여 NPU에 배포하는 DCM-SAM 제안임. 산업 검사용 경량화 배포 작업으로 novelty가 engineering에 머무름</td></tr>
<tr><td>615</td><td><a href='https://arxiv.org/abs/2609.39112'>CamAgent: An LLM-Agent Framework for Multi-Species Camera-Trap Workflows</a></td><td>26</td><td>0</td><td>CV</td><td>카메라 트랩 생태 분석 워크플로를 자동화하는 LLM 에이전트 프레임워크임. 야생동물 모니터링 응용으로 로보틱스와 무관함</td></tr>
<tr><td>616</td><td><a href='https://arxiv.org/abs/2609.39366'>COBICount: Separating Object and Background Responses for Remote Sensing Object Counting Without Training on Target Data</a></td><td>26</td><td>0</td><td>CV</td><td>타깃 데이터 없이 원격탐사 객체 카운팅을 전이하는 COBICount 제안임. niche 응용으로 로보틱스와 무관함</td></tr>
<tr><td>617</td><td><a href='https://arxiv.org/abs/2609.39380'>InfoAgent: Traceable Generation and Repair of Evidence-Grounded Infographics</a></td><td>26</td><td>0</td><td>CV</td><td>근거 기반 인포그래픽 생성·수정 InfoAgent 제안임. 문서 생성 응용으로 로보틱스와 무관함</td></tr>
<tr><td>618</td><td><a href='https://arxiv.org/abs/2609.39429'>Towards Trustworthy AI for Glioma Diagnosis: A Task-Aware Evaluation of Uncertainty Quantification</a></td><td>26</td><td>0</td><td>CV</td><td>교모세포종 진단에서 불확실성 정량화 방법들을 task-aware로 비교 평가한 연구임. 의료 영상 평가로 로보틱스와 무관함</td></tr>
<tr><td>619</td><td><a href='https://arxiv.org/abs/2609.39486'>From Wrecks to Wisdom: Recovering Crash Mechanics from Real-World Multi-View Photos</a></td><td>26</td><td>0</td><td>CV</td><td>사고 후 사진만으로 충돌 역학을 추정하는 예측 모델 제안임. 보험·안전 응용으로 로보틱스와 무관함</td></tr>
<tr><td>620</td><td><a href='https://arxiv.org/abs/2609.39649'>FANVIDv2: Evaluating Video Super-Resolution by Face and Licence-Plate Recognition Under Compound Degradation</a></td><td>26</td><td>0</td><td>CV</td><td>얼굴·번호판 인식 성능으로 비디오 초해상도를 평가하는 FANVIDv2 벤치마크임. 감시 응용으로 로보틱스와 무관함</td></tr>
<tr><td>621</td><td><a href='https://arxiv.org/abs/2609.39684'>Unapologetically Distributed: A Call for Decentralized Document Analysis</a></td><td>26</td><td>0</td><td>CV</td><td>문서 분석에서 federated learning이 OOD 강건성을 높일 수 있음을 보인 연구임. 응용 도메인이 문서 분석에 국한됨</td></tr>
<tr><td>622</td><td><a href='https://arxiv.org/abs/2609.39723'>Let the Carrier Carry the Attack: Preserving the Subject in Adversarial Image Generation</a></td><td>26</td><td>0</td><td>CV</td><td>보조 영역(carrier)이 적대적 변화를 흡수하게 해 피사체를 보존하는 공격 기법임. 적대적 공격 연구로 로보틱스와 무관함</td></tr>
<tr><td>623</td><td><a href='https://arxiv.org/abs/2609.39871'>Hyperspectral Image Models: Technical Report</a></td><td>26</td><td>0</td><td>CV</td><td>55개 하이퍼스펙트럴 모델을 통합한 벤치마크 라이브러리 기술 보고서임. 표준화 기여 위주로 로보틱스와 무관함</td></tr>
<tr><td>624</td><td><a href='https://arxiv.org/abs/2609.39899'>Learning Where to Look: Anatomical Grounding and Guided Attention for Cardiac MRI Vision-Language Models</a></td><td>26</td><td>0</td><td>Multimodal</td><td>심장 MRI에서 해부학적 위치에 주의를 유도하는 VLM CARA-VL 제안임. 의료 영상 응용으로 로보틱스와 무관함</td></tr>
<tr><td>625</td><td><a href='https://arxiv.org/abs/2609.39926'>Super-Resolving Unseen Hyperspectral Sensors at Any Scale via Spatial Operators</a></td><td>26</td><td>0</td><td>CV</td><td>band-shared spatial operator를 예측해 미지의 하이퍼스펙트럴 센서를 임의 배율로 초해상도화하는 OmniHSR 제안임. 원격탐사 응용으로 로보틱스와 무관함</td></tr>
<tr><td>626</td><td><a href='https://arxiv.org/abs/2609.40356'>ViTeX-Bench: Benchmarking High-Fidelity Video Scene Text Editing</a></td><td>26</td><td>0</td><td>Video</td><td>고품질 video scene text editing을 위한 벤치마크 ViTeX-Bench 제안임. 비디오 편집 응용으로 로보틱스와 무관함</td></tr>
<tr><td>627</td><td><a href='https://arxiv.org/abs/2609.38196'>Conformal Adversarial Generative Ensemble</a></td><td>26</td><td>0</td><td>LG</td><td>생성·판별·conformal prediction을 결합한 시계열 예측 앙상블 CAGE 제안임. 예측 응용으로 로보틱스와 무관함</td></tr>
<tr><td>628</td><td><a href='https://arxiv.org/abs/2609.38384'>LeanPolish: Verified Supervision for Lean Proof Compression</a></td><td>26</td><td>0</td><td>LG</td><td>Lean 4 증명을 검증 가능한 edit로 압축하는 LeanPolish 제안임. 정리 증명 응용으로 로보틱스와 무관함</td></tr>
<tr><td>629</td><td><a href='https://arxiv.org/abs/2609.38521'>ShamAN-Q: Shampoo Augmented NanoQuant for Sub-1-bit LLM Weights</a></td><td>26</td><td>0</td><td>LG</td><td>Shampoo 곡률을 이용해 LLM을 1비트 이하로 양자화하는 ShamAN-Q 제안임. 경량화 기여로 우선 평가 대상이 아님</td></tr>
<tr><td>630</td><td><a href='https://arxiv.org/abs/2609.38623'>Geometry-physics confounding impairs PDE learning across varying domains</a></td><td>26</td><td>0</td><td>LG</td><td>PDE 학습에서 geometry-physics confounding 식별, 과학계산 문제로 로봇과 무관함</td></tr>
<tr><td>631</td><td><a href='https://arxiv.org/abs/2609.39466'>T-ARC: Topology-Aware Randomized Clustering via Distributionally Robust Stochastic Block Models</a></td><td>26</td><td>0</td><td>LG</td><td>위상학적 정보를 K-means에 결합한 클러스터링 기법, 일반 클러스터링 방법론임</td></tr>
<tr><td>632</td><td><a href='https://arxiv.org/abs/2609.38427'>Policy-Conditioned AI-Use Detection: An Evidentiary Framework for Academic Publishing</a></td><td>26</td><td>0</td><td>NLP</td><td>AI 저작 탐지를 저자성 판별이 아닌 정책 준수 감사로 재정의함. 학술출판 메타 연구임.</td></tr>
<tr><td>633</td><td><a href='https://arxiv.org/abs/2609.38227'>A Two-Echelon Covering Tour Vehicle Routing Problem with Drones for Post-Disaster Relief</a></td><td>25</td><td>3</td><td>RL</td><td>재난 구호용 2단계 drone-truck 라우팅 문제임. 조합 최적화 연구로 embodied AI와는 거리 있음.</td></tr>
<tr><td>634</td><td><a href='https://arxiv.org/abs/2609.40178'>Non-Invasive Inspection of Water Canals Using Dronar</a></td><td>25</td><td>2</td><td>Robotics</td><td>드론과 소나를 결합해 물을 빼지 않고 운하 바닥을 점검하는 응용 시스템임. 학습 요소 없는 proof-of-concept 엔지니어링임.</td></tr>
<tr><td>635</td><td><a href='https://arxiv.org/abs/2609.39437'>Network-based Spatial Context Retrieval for Open-weight LLMs: A Faithfulness Benchmark for Grounded Geographic Reasoning</a></td><td>25</td><td>1</td><td>NLP</td><td>보행 네트워크 기반 공간 맥락 검색으로 LLM의 지리적 추론 충실성 평가, embodied spatial reasoning과 느슨하게 연관되나 지도 기반 텍스트 QA임</td></tr>
<tr><td>636</td><td><a href='https://arxiv.org/abs/2609.38460'>NAQD Env: A benchmark for selective withdrawal in language agents</a></td><td>25</td><td>1</td><td>NLP</td><td>증거·권한 변화 시 선택적으로 행동을 철회하는 능력을 평가하는 합성 환경임. 현재 모델들이 거의 실패함을 보임</td></tr>
<tr><td>637</td><td><a href='https://arxiv.org/abs/2609.38867'>Talk2Agent: Benchmarking Voice Interfaces for Text Agents</a></td><td>25</td><td>1</td><td>NLP</td><td>음성 인터페이스가 computer-use agent에 전달하는 정보 손실을 측정하는 execution-free 평가임</td></tr>
<tr><td>638</td><td><a href='https://arxiv.org/abs/2609.39964'>AIMS: An Agentic AI Framework for Sim-to-Real Multi-Modal ISAC</a></td><td>25</td><td>1</td><td>NLP</td><td>무선 센싱-통신 데이터의 sim-to-real 파이프라인을 자연어 지시로 구성하는 agentic 프레임워크임</td></tr>
<tr><td>639</td><td><a href='https://arxiv.org/abs/2609.38428'>MOBA-VL: Event-Localized Multi-Turn Reinforcement Learning for Real-Time MOBA Commentary</a></td><td>25</td><td>0</td><td>Multimodal</td><td>MOBA 게임 실시간 해설 생성을 위한 event-localized RL VLM임. 응용이 특정 도메인에 한정되고 로보틱스와 무관함</td></tr>
<tr><td>640</td><td><a href='https://arxiv.org/abs/2609.38636'>STEPS: Scene Text Editing with Preserved Style Using Diffusion and Contrastive Style Encoding</a></td><td>25</td><td>0</td><td>CV</td><td>scene text editing에서 스타일 보존을 개선하는 diffusion 모델임. 응용이 이미지 편집에 국한됨</td></tr>
<tr><td>641</td><td><a href='https://arxiv.org/abs/2609.38913'>FLOW: Feature-Level Optimal Warping for Generalized Remote Physiological Measurement</a></td><td>25</td><td>0</td><td>CV</td><td>optimal transport 기반 도메인 일반화 rPPG 측정 FLOW 제안임. 의료 생체신호 응용으로 로보틱스와 무관함</td></tr>
<tr><td>642</td><td><a href='https://arxiv.org/abs/2609.39024'>Persistent Watermarking of Text-to-Image Models</a></td><td>25</td><td>0</td><td>CV</td><td>T2I 모델의 지속적 워터마킹 기법임. 저작권 보호 목적으로 로보틱스와 무관함</td></tr>
<tr><td>643</td><td><a href='https://arxiv.org/abs/2609.39083'>MRI Super-Resolution with RCDM/WaveMix and Task-Aware Segmentation</a></td><td>25</td><td>0</td><td>CV</td><td>저자기장 MRI 향상이 segmentation 모델별로 다르게 작용함을 보인 연구임. 의료 영상 평가 방법론으로 로보틱스와 무관함</td></tr>
<tr><td>644</td><td><a href='https://arxiv.org/abs/2609.39184'>Fiber-Resolved Microstructure Quantification from Multi-Shell Diffusion MRI using Detection Transformers</a></td><td>25</td><td>0</td><td>CV</td><td>DETR 구조로 확산 MRI의 섬유 방향과 미세구조를 동시 예측하는 방법임. 의료 영상 분석으로 로보틱스와 무관함</td></tr>
<tr><td>645</td><td><a href='https://arxiv.org/abs/2609.39266'>PLRS-IC: A Dual-Calibration Framework for Chest X-Ray Vision-Language Alignment</a></td><td>25</td><td>0</td><td>Multimodal</td><td>흉부 X-ray의 projection별 불일치를 해소하는 dual-calibration vision-language 정합 방법임. 의료 영상 응용으로 로보틱스와 무관함</td></tr>
<tr><td>646</td><td><a href='https://arxiv.org/abs/2609.39623'>Semantic Watermarking for Malicious Image Manipulation Detection</a></td><td>25</td><td>0</td><td>CV</td><td>복원 가능한 semantic reference로 이미지 조작을 탐지하는 워터마킹 프레임워크임. 콘텐츠 변조 탐지 목적으로 로보틱스와 무관함</td></tr>
<tr><td>647</td><td><a href='https://arxiv.org/abs/2609.38599'>JARQ: Joint Alternating Refinement for Quantization</a></td><td>25</td><td>0</td><td>LG</td><td>LLM quantization 정교화 작업으로 로보틱스 연관성 없음</td></tr>
<tr><td>648</td><td><a href='https://arxiv.org/abs/2609.38781'>ChartDensity-Bench: Benchmarking MLLMs for Numerical Data Reconstruction under Visual Density</a></td><td>25</td><td>0</td><td>Multimodal</td><td>MLLM의 밀집 차트 수치 재구성 벤치마크, 로보틱스 무관</td></tr>
<tr><td>649</td><td><a href='https://arxiv.org/abs/2609.38786'>Same Loss, Different Gradients</a></td><td>25</td><td>0</td><td>LG</td><td>forward/backward 수치 불일치 문제 분석과 보정 기법, 수치해석적 기여임</td></tr>
<tr><td>650</td><td><a href='https://arxiv.org/abs/2609.38898'>K2P: Label-Free Knowledge to Prompt Distillation</a></td><td>25</td><td>0</td><td>NLP</td><td>label 없이 teacher solution에서 prompt로 distillation하는 기법, LLM reasoning 효율화임</td></tr>
<tr><td>651</td><td><a href='https://arxiv.org/abs/2609.38902'>Amortized Data Borrowing with Exchangeability-Aware Neural Posterior Estimation</a></td><td>25</td><td>0</td><td>LG</td><td>임상시험 데이터 borrowing을 amortized neural posterior estimation으로 가속, 의료통계 응용임</td></tr>
<tr><td>652</td><td><a href='https://arxiv.org/abs/2609.38936'>Signal-Routed Temperature Scaling: Low-Capacity Risk-Conditioned Calibration for Small Validation Budgets</a></td><td>25</td><td>0</td><td>LG</td><td>소규모 validation 하의 risk-conditioned temperature scaling, calibration 세부 기법임</td></tr>
<tr><td>653</td><td><a href='https://arxiv.org/abs/2609.38980'>SCORE-LM: State-Space Radar Representations with Language Models for Fault Diagnosis</a></td><td>25</td><td>0</td><td>LG</td><td>레이더 고장진단에 state-space encoder와 LLM 결합, 산업 진단 응용임</td></tr>
<tr><td>654</td><td><a href='https://arxiv.org/abs/2609.39035'>Cycle-Aware Autoencoder with Cross-SignalConsistency for Railway Door Anomaly Detection</a></td><td>25</td><td>0</td><td>LG</td><td>철도문 이상탐지용 autoencoder, 산업 모니터링 문제로 로보틱스 무관</td></tr>
<tr><td>655</td><td><a href='https://arxiv.org/abs/2609.39037'>Hard-Gate Candidacy in a Deployed Validator Suite</a></td><td>25</td><td>0</td><td>LG</td><td>배포된 validator suite의 hard-gate 적절성 실증 분석, LLM 에이전트 평가 인프라 연구임</td></tr>
<tr><td>656</td><td><a href='https://arxiv.org/abs/2609.39068'>SparseEngine: Sparse-First Inference Engine</a></td><td>25</td><td>0</td><td>LG</td><td>sparse attention 전용 LLM inference 엔진, 시스템 최적화 기여임</td></tr>
<tr><td>657</td><td><a href='https://arxiv.org/abs/2609.39074'>HO-FL: Hybrid-Order Federated Learning for Heterogeneous Edge Devices</a></td><td>25</td><td>0</td><td>LG</td><td>edge device 메모리 제약 하의 hybrid-order federated learning, 연합학습 효율화임</td></tr>
<tr><td>658</td><td><a href='https://arxiv.org/abs/2609.39185'>Low-Discrepancy Dither for Quantized Recurrent State Caches</a></td><td>25</td><td>0</td><td>LG</td><td>Mamba류 모델의 recurrent state quantization에 결정적 dither 적용, 메모리 압축 기법임</td></tr>
<tr><td>659</td><td><a href='https://arxiv.org/abs/2609.39215'>In a Streaming World, Should You Stand Still? A Comprehensive Benchmark of Anomaly Detection in Streams</a></td><td>25</td><td>0</td><td>LG</td><td>스트리밍 이상탐지 방법들의 대규모 벤치마크, static 방법이 더 우수함을 보임</td></tr>
<tr><td>660</td><td><a href='https://arxiv.org/abs/2609.39223'>QATFactory: A Versatile, Deployment-Aligned Framework for Quantization-aware Training and Distillation of LLMs</a></td><td>25</td><td>0</td><td>LG</td><td>배포 정렬 quantization-aware training/distillation 프레임워크, LLM 양자화 엔지니어링임</td></tr>
<tr><td>661</td><td><a href='https://arxiv.org/abs/2609.39337'>WinoTS: Wavelet-based Self-Distillation for Time Series Models</a></td><td>25</td><td>0</td><td>LG</td><td>wavelet 기반 self-distillation으로 시계열 사전학습 개선, 시계열 표현학습 기법임</td></tr>
<tr><td>662</td><td><a href='https://arxiv.org/abs/2609.39361'>LampAttention: Look-Ahead Mixed-Precision FlashAttention for Dedicated Accelerators</a></td><td>25</td><td>0</td><td>LG</td><td>혼합정밀도 FlashAttention을 위한 하드웨어-알고리즘 공동설계, 가속기 연구임</td></tr>
<tr><td>663</td><td><a href='https://arxiv.org/abs/2609.39386'>When, Not How Much: Evaluating Time-Series Foundation Models on Sparse Events</a></td><td>25</td><td>0</td><td>LG</td><td>sparse event에 대한 시계열 foundation model 평가, 평가방법론 연구임</td></tr>
<tr><td>664</td><td><a href='https://arxiv.org/abs/2609.39464'>Understanding Head Geometry and Dynamics in Federated Regression through a Natural Solution Selection Rule: An Unconstrained Feature Model Analysis</a></td><td>25</td><td>0</td><td>LG</td><td>연합 회귀에서 head 기하 선택 규칙 분석, 연합학습 이론 연구임</td></tr>
<tr><td>665</td><td><a href='https://arxiv.org/abs/2609.39478'>Also Small Models Can Reasonably Self-Evaluate Their Confidence</a></td><td>25</td><td>0</td><td>NLP</td><td>소형 모델의 self-evaluation confidence 신뢰성이 스케일에 독립적임을 보임, LLM 평가 연구임</td></tr>
<tr><td>666</td><td><a href='https://arxiv.org/abs/2609.39489'>Towards Robust Time Series Learning via Capacity-Centric Modulation</a></td><td>25</td><td>0</td><td>LG</td><td>샘플별 reliability에 맞춘 적응적 dropout 변조로 시계열 학습 견고성 개선, 세부 정규화 기법임</td></tr>
<tr><td>667</td><td><a href='https://arxiv.org/abs/2609.39550'>Hyperbolic Prototype Routing for Rehearsal-Free Class-Incremental Learning</a></td><td>25</td><td>0</td><td>LG</td><td>쌍곡공간 prototype routing 기반 rehearsal-free class-incremental learning, 지속학습 기법임</td></tr>
<tr><td>668</td><td><a href='https://arxiv.org/abs/2609.39628'>MIND: Marginal-Invariant Neural Dependency Diffusion for Mixed-Type Tabular Generation</a></td><td>25</td><td>0</td><td>LG</td><td>마진-의존성 분리 diffusion으로 혼합형 표 데이터 생성, tabular 생성모델 기법임</td></tr>
<tr><td>669</td><td><a href='https://arxiv.org/abs/2609.39673'>NodeGround: A Node Classification Benchmark in the Graph Foundation Model Era</a></td><td>25</td><td>0</td><td>LG</td><td>graph foundation model과 전용 GNN을 공정 비교하는 벤치마크, 그래프 학습 평가 연구임</td></tr>
<tr><td>670</td><td><a href='https://arxiv.org/abs/2609.39784'>CORD: Learning Reusable Degradation Representations Across Heterogeneous Physical Systems</a></td><td>25</td><td>0</td><td>LG</td><td>이종 물리 시스템 간 재사용 가능한 열화 표현학습, 산업 예지보전 응용임</td></tr>
<tr><td>671</td><td><a href='https://arxiv.org/abs/2609.39833'>RainAtlas: A Multi-Continental Dataset for Precipitation Downscaling</a></td><td>25</td><td>0</td><td>LG</td><td>강수량 다운스케일링용 다대륙 데이터셋 공개, 기후 ML 벤치마크임</td></tr>
<tr><td>672</td><td><a href='https://arxiv.org/abs/2609.39839'>Dynamic LoRA-Experts and Prototype-Ensemble Matching for Class-Incremental Learning</a></td><td>25</td><td>0</td><td>LG</td><td>동적 LoRA-expert와 prototype ensemble로 class-incremental learning, 지속학습 기법임</td></tr>
<tr><td>673</td><td><a href='https://arxiv.org/abs/2609.40034'>Efficient Active Auditing of Multi-Group Fairness with Bias Probes</a></td><td>25</td><td>0</td><td>LG</td><td>블랙박스 모델의 multi-group fairness를 active probing으로 감사하는 프레임워크, 공정성 감사 연구임</td></tr>
<tr><td>674</td><td><a href='https://arxiv.org/abs/2609.40070'>Inference Auctions</a></td><td>25</td><td>0</td><td>LG</td><td>LLM 추론 요청에 경매 기반 우선순위 할당 메커니즘 설계, 시스템·경제학 연구임</td></tr>
<tr><td>675</td><td><a href='https://arxiv.org/abs/2609.40117'>Beyond Model Ranking: Regime Diagnosis for Distributional-Statistical Misspecification in Industrial Time-Series Forecasting</a></td><td>25</td><td>0</td><td>LG</td><td>산업 시계열 예측의 분포적 편향을 regime별로 진단하는 도구 RBV 제안, 수요예측 평가방법론임</td></tr>
<tr><td>676</td><td><a href='https://arxiv.org/abs/2609.40131'>Prototype-Rule Neurosymbolic Regularization for Rank-Constrained Tensor Neural Networks under Label Scarcity</a></td><td>25</td><td>0</td><td>CV</td><td>rank-constrained tensor network에 prototype-rule neurosymbolic 정규화 추가, 초분광 영상 적은 라벨 학습임</td></tr>
<tr><td>677</td><td><a href='https://arxiv.org/abs/2609.40148'>From Spectra to Joint Schedules in LLM Pre-training: 3+3(+2) Scaling-Law Regimes</a></td><td>25</td><td>0</td><td>LG</td><td>LLM pretraining 학습률/배치 스케줄 스케일링 법칙 이론 분석임. robotics와 무관함.</td></tr>
<tr><td>678</td><td><a href='https://arxiv.org/abs/2609.38181'>Large Language Models are Approximate Survival Estimators</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM으로 암 생존 시간을 zero-shot 예측하는 의료 벤치마크임. robotics와 무관함.</td></tr>
<tr><td>679</td><td><a href='https://arxiv.org/abs/2609.39365'>Ready2Blend: From Natural-Language Instructions to Composable Alignment Prompts</a></td><td>25</td><td>0</td><td>NLP</td><td>continual alignment를 위한 modular prompt bank 방법. 점진적 엔지니어링 기여임</td></tr>
<tr><td>680</td><td><a href='https://arxiv.org/abs/2609.39369'>Exploring Heterogeneous Model Merging Approach for Complex Knowledge Transfer</a></td><td>25</td><td>0</td><td>LG</td><td>기존 training-free model merging 기법을 specialist-to-general 전이에 적용한 실험 보고임</td></tr>
<tr><td>681</td><td><a href='https://arxiv.org/abs/2609.39446'>DuplexAct-Bench: Broadening Full-Duplex Speech Evaluation toward Proactive Interaction across Diverse Behavioral Requirements</a></td><td>25</td><td>0</td><td>NLP</td><td>full-duplex 음성 상호작용 벤치마크 확장임. 평가 커버리지 확대 수준</td></tr>
<tr><td>682</td><td><a href='https://arxiv.org/abs/2609.39447'>Synthetic Data Characterization via Training Dynamics</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM 합성 데이터의 learnability를 training dynamics로 특성화한 분석 연구임</td></tr>
<tr><td>683</td><td><a href='https://arxiv.org/abs/2609.39608'>Is This Evidence Decision-Critical? Learning to Verify Rule-Governed Decisions</a></td><td>25</td><td>0</td><td>NLP</td><td>규칙 기반 의사결정에서 결정-critical evidence를 식별하는 counterfactual verifier임</td></tr>
<tr><td>684</td><td><a href='https://arxiv.org/abs/2609.39710'>Drift Inspector: Exploring and Measuring Scientific Drift with Atomic Contribution Claims</a></td><td>25</td><td>0</td><td>NLP</td><td>논문 claim을 atomic 단위로 추출해 연구 트렌드를 추적하는 시스템 데모임</td></tr>
<tr><td>685</td><td><a href='https://arxiv.org/abs/2609.39786'>Explore-on-Graph: Hybrid Embedding-LLM Reasoning for Knowledge Graph Question Answering under Incompleteness</a></td><td>25</td><td>0</td><td>NLP</td><td>불완전한 KG에서 임베딩과 LLM을 결합해 누락 경로를 복구하는 KGQA 방법임</td></tr>
<tr><td>686</td><td><a href='https://arxiv.org/abs/2609.39846'>When a Kindergartener Solves Calculus: Measuring Capability Leakage in Role-Prompted Reasoning Models</a></td><td>25</td><td>0</td><td>NLP</td><td>역할 프롬프트가 역량을 역할 수준으로 낮추지 못하는 capability leakage 현상을 측정함</td></tr>
<tr><td>687</td><td><a href='https://arxiv.org/abs/2609.39882'>LLM Persona Unlearning</a></td><td>25</td><td>0</td><td>NLP</td><td>특정 persona를 가중치 수준에서 제거하는 unlearning 벤치마크 및 방법임</td></tr>
<tr><td>688</td><td><a href='https://arxiv.org/abs/2609.39913'>The Concrete-Arbitrary Gap: Kinship Reasoning in LLMs Is Not Indifferent to Presentation</a></td><td>25</td><td>0</td><td>NLP</td><td>친숙한 어휘 대 명시적 정의 predicate 간 kinship reasoning 격차를 측정함</td></tr>
<tr><td>689</td><td><a href='https://arxiv.org/abs/2609.39927'>AdaGEPA: Adaptive Feedback Allocation for Reflective Prompt Optimization</a></td><td>25</td><td>0</td><td>NLP</td><td>프롬프트 최적화에서 피드백 예제를 적응적으로 선택하는 방법임</td></tr>
<tr><td>690</td><td><a href='https://arxiv.org/abs/2609.39972'>UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding</a></td><td>25</td><td>0</td><td>LG</td><td>unigram+bigram 기반 tree drafting으로 speculative decoding 속도를 높인 시스템 기여임</td></tr>
<tr><td>691</td><td><a href='https://arxiv.org/abs/2609.40097'>AutoDataBench: A Data-centric Testbed for Accelerating Auto Research</a></td><td>25</td><td>0</td><td>NLP</td><td>데이터 개입 능력만 분리 평가하는 autoresearch 테스트베드임</td></tr>
<tr><td>692</td><td><a href='https://arxiv.org/abs/2609.40103'>JuryFlow: Disagreement-Guided Human-in-the-Loop Multi-Agent Evaluation</a></td><td>25</td><td>0</td><td>NLP</td><td>judge 간 불일치를 그래프로 구조화해 human-in-the-loop로 해결하는 평가 프레임워크임</td></tr>
<tr><td>693</td><td><a href='https://arxiv.org/abs/2609.40121'>On the (In)effectiveness of AMR Augmentation for Large Language Models</a></td><td>25</td><td>0</td><td>NLP</td><td>AMR 증강이 현대 LLM에 도움이 안 됨을 재현실험으로 보인 negative result임</td></tr>
<tr><td>694</td><td><a href='https://arxiv.org/abs/2609.40124'>Debias It Yourself: Teaching LLMs Cognitive Bias Mitigation Interventions</a></td><td>25</td><td>0</td><td>NLP</td><td>인지심리학 디바이어싱 기법을 LLM에 적용한 프레임워크임. 조합적 기여</td></tr>
<tr><td>695</td><td><a href='https://arxiv.org/abs/2609.40286'>Linguistic Loopholes in LLM Unlearning: From a 174-Language Benchmark to Coverage-Aware Unlearning</a></td><td>25</td><td>0</td><td>NLP</td><td>174개 언어에 걸친 cross-lingual unlearning loophole을 측정하고 언어 선택 방법을 제안함</td></tr>
<tr><td>696</td><td><a href='https://arxiv.org/abs/2609.38369'>Can an AI Agent Rediscover a Blaschke-Curve Invariant?</a></td><td>25</td><td>0</td><td>NLP</td><td>AI agent가 수학 불변량을 재발견할 수 있는지 단일 사례로 검증한 연구임. negative에 가까운 결과를 정직하게 보고함</td></tr>
<tr><td>697</td><td><a href='https://arxiv.org/abs/2609.38392'>MetaPersona: Task-Grounded Synthetic Populations from Empirical Social Science</a></td><td>25</td><td>0</td><td>NLP</td><td>실증 사회과학 데이터 기반으로 synthetic persona를 생성하는 프레임워크임</td></tr>
<tr><td>698</td><td><a href='https://arxiv.org/abs/2609.38397'>SimTrace: Grounded Multimodal User Trajectories Generation for Online User Modeling</a></td><td>25</td><td>0</td><td>NLP</td><td>실제 로그 기반 synthetic 사용자 클릭스트림을 생성하는 시스템임</td></tr>
<tr><td>699</td><td><a href='https://arxiv.org/abs/2609.38409'>ArgGYM: A Procedural, Engine-Verified Benchmark for Structured Defeasible Reasoning</a></td><td>25</td><td>0</td><td>NLP</td><td>defeasible reasoning을 구조화한 절차적 벤치마크 및 RLVR 환경임</td></tr>
<tr><td>700</td><td><a href='https://arxiv.org/abs/2609.38448'>Reach Into The CHOIR: Free-List Elicitation Uncovers Distinct Model Voices in LLM Ensembles</a></td><td>25</td><td>0</td><td>NLP</td><td>free-list elicitation으로 LLM 앙상블의 숨은 다양성을 측정하는 진단 방법임</td></tr>
<tr><td>701</td><td><a href='https://arxiv.org/abs/2609.38555'>Demographic Pluralism: Inference-Time Modeling of Pluralistic Human Preference Distributions</a></td><td>25</td><td>0</td><td>NLP</td><td>inference-time에 집단 내 다양성을 반영하는 pluralistic opinion 모델링 방법임</td></tr>
<tr><td>702</td><td><a href='https://arxiv.org/abs/2609.38652'>AgBench: Agentic AI Benchmarks for Personal AI Devices</a></td><td>25</td><td>0</td><td>NLP</td><td>개인 AI 디바이스에서 local/hybrid/cloud agent 실행의 trade-off를 측정한 벤치마크임</td></tr>
<tr><td>703</td><td><a href='https://arxiv.org/abs/2609.38690'>GATE-ST: Gene-Aware Text-image Encoder for Spatial Transcriptomics</a></td><td>25</td><td>0</td><td>CV</td><td>유전자 요약 텍스트를 이미지 임베딩과 cross-attention으로 결합한 공간전사체 예측 방법임</td></tr>
<tr><td>704</td><td><a href='https://arxiv.org/abs/2609.38964'>When Order Matters: First-Speaker Bias and Mitigation through Personality in Sequential Multi-Agent Debate</a></td><td>25</td><td>0</td><td>NLP</td><td>순차 multi-agent debate의 first-speaker 편향을 성격 프롬프팅으로 완화한 연구임</td></tr>
<tr><td>705</td><td><a href='https://arxiv.org/abs/2609.39005'>C-STRIDE: An Observation-Driven AI Digital Twin for Predicting Basin-Wide Flood Fields from Sparse Stream-Gauge Histories</a></td><td>25</td><td>0</td><td>LG</td><td>희소 하천 게이지 데이터로 홍수 범람을 예측하는 observation-driven AI digital twin임. 응용 성격이 강함</td></tr>
<tr><td>706</td><td><a href='https://arxiv.org/abs/2609.39106'>Reserve-Aware Contrast Certificates for Conservative Bandits with Uncertain Baselines</a></td><td>25</td><td>0</td><td>RL</td><td>불확실한 baseline을 가진 conservative bandit에서 contrast 기반 confidence set을 구성한 이론 연구임</td></tr>
<tr><td>707</td><td><a href='https://arxiv.org/abs/2609.39146'>MADBench: Benchmarking the Security of Multi-Agent Debate</a></td><td>25</td><td>0</td><td>NLP</td><td>multi-agent debate의 공격 내성을 체계적으로 평가한 보안 벤치마크임</td></tr>
<tr><td>708</td><td><a href='https://arxiv.org/abs/2609.39228'>Fyan: A Human--AI Harness with Semantic Auditing for Document-Level Formalization</a></td><td>25</td><td>0</td><td>NLP</td><td>문서 단위 수학 formalization을 위한 human-AI harness와 semantic audit 메커니즘임</td></tr>
<tr><td>709</td><td><a href='https://arxiv.org/abs/2609.39297'>MiniRep: Robust Reputation-Based Aggregation for Multi-Agent Debate</a></td><td>25</td><td>0</td><td>NLP</td><td>악의적 agent가 있는 multi-agent debate에서 reputation 기반 집계로 공격에 강건한 방법임</td></tr>
<tr><td>710</td><td><a href='https://arxiv.org/abs/2609.39360'>Autoresearch in Mixed-Integer Linear and Nonlinear Programming</a></td><td>25</td><td>0</td><td>NLP</td><td>혼합정수계획법 연구를 위한 아이디어 풀링·알고리즘 트리서치 autoresearch 프레임워크임</td></tr>
<tr><td>711</td><td><a href='https://arxiv.org/abs/2609.39544'>Growing an Agent/Prover Interface: Evolutionary Tool Design for Cost-Efficient Theorem Proving in Rocq and Lean</a></td><td>25</td><td>0</td><td>NLP</td><td>정리증명 agent용 MCP 인터페이스를 진화적으로 설계한 연구임</td></tr>
<tr><td>712</td><td><a href='https://arxiv.org/abs/2609.39564'>A2Z GameSpec-Bench: How Faithfully Can Coding Agents Generate Games from Game Design Specifications?</a></td><td>25</td><td>0</td><td>NLP</td><td>장문 게임 설계 문서를 충실히 구현하는 coding agent 벤치마크임</td></tr>
<tr><td>713</td><td><a href='https://arxiv.org/abs/2609.39701'>Values as Style: Disentangling Values from Semantics with One-Way Mixing for Low-Damage LLM Steering</a></td><td>25</td><td>0</td><td>NLP</td><td>의미와 가치를 분리해 LLM을 낮은 손상으로 조종하는 활성화 편집 방법임</td></tr>
<tr><td>714</td><td><a href='https://arxiv.org/abs/2609.39717'>Trust Is Not a Score: Runtime Assurance Contracts for High-Risk AI Agents</a></td><td>25</td><td>0</td><td>NLP</td><td>고위험 AI agent의 권한을 증거 상태에 따라 전환시키는 runtime assurance contract 스키마임</td></tr>
<tr><td>715</td><td><a href='https://arxiv.org/abs/2609.39869'>GrammarRL: Effective Grammar-Constrained Decoding via Reinforcement Learning</a></td><td>25</td><td>0</td><td>NLP</td><td>grammar-constrained decoding에서 self-supervised reward로 label 없이 RL 적용한 방법임</td></tr>
<tr><td>716</td><td><a href='https://arxiv.org/abs/2609.39955'>Coverage Before Control: Route-Instruction Grounding and Steering for Controllable Retrosynthesis</a></td><td>25</td><td>0</td><td>NLP</td><td>역합성 생성에서 선호 지시를 반영하도록 coverage와 control을 함께 다루는 2단계 프레임워크임</td></tr>
<tr><td>717</td><td><a href='https://arxiv.org/abs/2609.40090'>PTNO: Training Neural Operators with Noisy Monte Carlo Estimates for Particle Transport Problems</a></td><td>25</td><td>0</td><td>LG</td><td>잡음 많은 몬테카를로 라벨로 입자수송 neural operator를 학습시키는 물리 시뮬레이션 연구임</td></tr>
<tr><td>718</td><td><a href='https://arxiv.org/abs/2609.39051'>TSMD: Temporal-Stream Modality Dropout for Robust Video Highlight Detection</a></td><td>24</td><td>0</td><td>Video</td><td>모달리티 결손에 강건한 video highlight 탐지 TSMD 제안임. 적용 범위가 하이라이트 탐지로 좁음</td></tr>
<tr><td>719</td><td><a href='https://arxiv.org/abs/2609.39335'>TexTailor: Texture-Preserving Video Virtual Try-On via Adaptive Garment Conditioning</a></td><td>24</td><td>0</td><td>Video</td><td>고해상도 비디오 가상 피팅을 위한 timestep-adaptive 의상 조건화 TexTailor 제안임. 패션 응용으로 로보틱스와 무관함</td></tr>
<tr><td>720</td><td><a href='https://arxiv.org/abs/2609.39427'>PCB-MC: Missing Component Analysis in Printed Circuit Boards</a></td><td>24</td><td>0</td><td>CV</td><td>PCB 부품 누락 탐지 데이터셋과 벤치마크임. 산업 검사 응용으로 로보틱스와 무관함</td></tr>
<tr><td>721</td><td><a href='https://arxiv.org/abs/2609.39624'>ExpandDiff: Dynamic Range Expanding Diffusion for Single-Image HDR Reconstruction</a></td><td>24</td><td>0</td><td>CV</td><td>단일 LDR 이미지에서 clipping 정도를 다양화해 학습하는 HDR 복원 diffusion 제안임. 영상 품질 개선 응용으로 로보틱스와 무관함</td></tr>
<tr><td>722</td><td><a href='https://arxiv.org/abs/2609.39662'>Typographic Attack Against VLM-based AI-generated Image Detection</a></td><td>24</td><td>0</td><td>Multimodal</td><td>VLM 기반 AI 생성 이미지 탐지에 대한 typographic 공격을 체계적으로 평가한 연구임. 보안 분석으로 로보틱스와 무관함</td></tr>
<tr><td>723</td><td><a href='https://arxiv.org/abs/2609.39756'>Determining Vertical Displacement of Agricultural Areas Using UAV-Photogrammetry and a Heteroscedastic Deep Learning Model</a></td><td>24</td><td>0</td><td>CV</td><td>UAV 사진측량으로 농경지 수직 변위를 추정하는 U-Net 기반 방법임. 원격탐사 응용으로 로보틱스와 무관함</td></tr>
<tr><td>724</td><td><a href='https://arxiv.org/abs/2609.40091'>GateSPINE: Gated Cross-View Fusion for Lumbar Spine MRI Report Generation</a></td><td>24</td><td>0</td><td>Multimodal</td><td>시상·축상 MRI를 gated cross-view fusion으로 결합해 요추 보고서를 생성하는 GateSPINE 제안임. 의료 영상 응용으로 로보틱스와 무관함</td></tr>
<tr><td>725</td><td><a href='https://arxiv.org/abs/2609.38197'>DualCast: A Dual-Path Language Model for Bimodal Financial Time-Series Forecasting</a></td><td>24</td><td>0</td><td>LG</td><td>뉴스와 가격을 함께 쓰는 금융 시계열 예측 DualCast 제안임. 금융 응용으로 로보틱스와 무관함</td></tr>
<tr><td>726</td><td><a href='https://arxiv.org/abs/2609.38276'>Kinematic signatures of impairment: Detecting alcohol intoxication in e-scooter riders using sensor data and machine learning</a></td><td>24</td><td>0</td><td>LG</td><td>IMU 신호의 엔트로피로 전동 킥보드 운전자의 음주 상태를 탐지하는 연구임. 안전 응용으로 로보틱스와 무관함</td></tr>
<tr><td>727</td><td><a href='https://arxiv.org/abs/2609.38447'>An Input-Frugal Deep Learning Framework for Weather-Driven National Crop-Yield Forecasting: A Case Study of Brazilian Soybean</a></td><td>24</td><td>0</td><td>LG</td><td>날씨 데이터만으로 브라질 대두 수확량을 예측하는 경량 모델 제안임. 농업 응용으로 로보틱스와 무관함</td></tr>
<tr><td>728</td><td><a href='https://arxiv.org/abs/2609.38523'>MM-FinEval: A Multi-Task Multimodal Benchmark for Real-World Financial Forecasting</a></td><td>24</td><td>0</td><td>LG</td><td>실적 발표 콜 데이터로 멀티모달 금융 예측을 평가하는 MM-FinEval 벤치마크임. 금융 응용으로 로보틱스와 무관함</td></tr>
<tr><td>729</td><td><a href='https://arxiv.org/abs/2609.40193'>Near-Linear Accuracy Bounds for Moreau--Yosida Unadjusted Langevin Sampling</a></td><td>24</td><td>0</td><td>LG</td><td>Langevin sampling 수렴 이론 분석임. 순수 수학적 기여라 로보틱스와 거리 있음.</td></tr>
<tr><td>730</td><td><a href='https://arxiv.org/abs/2609.40265'>OpenTSLM TeeMoE: A Unified Time-Series Language Model for Forecasting, Contextual Prediction, and Reasoning</a></td><td>24</td><td>0</td><td>LG</td><td>시계열 예측·추론 통합 언어모델임. MoE 컨트롤러로 여러 benchmark 상위권이나 robotics 무관함.</td></tr>
<tr><td>731</td><td><a href='https://arxiv.org/abs/2609.40361'>Ranking-Aware Prompt Optimization for Multimodal Clinical Diagnosis</a></td><td>24</td><td>0</td><td>Multimodal</td><td>MLLM 임상 진단 프롬프트 최적화를 AUROC 기준으로 개선함. 의료 분야 연구임.</td></tr>
<tr><td>732</td><td><a href='https://arxiv.org/abs/2609.38355'>Halluscoring 2026: The first shared task on llms hallucination detection and answer verification</a></td><td>24</td><td>0</td><td>NLP</td><td>아랍어 질의응답 환각 탐지 shared task 결과 보고임. 벤치마크 대회 리포트임.</td></tr>
<tr><td>733</td><td><a href='https://arxiv.org/abs/2609.38630'>Strong Multilingual Privacy Tagging at Encoder Speed</a></td><td>24</td><td>0</td><td>NLP</td><td>35개 언어 개인정보 태깅을 encoder 속도로 수행하는 NER 시스템임. 프라이버시 레이블링 연구임.</td></tr>
<tr><td>734</td><td><a href='https://arxiv.org/abs/2609.38861'>TRACE: Target-Aware Retrieval, Attributed Evidence, and Contract-Constrained Extraction for LitTraceQA</a></td><td>24</td><td>0</td><td>NLP</td><td>논문에서 검증 가능한 근거와 표를 추출하는 LitTraceQA 시스템임. 문헌 QA 응용 연구임.</td></tr>
<tr><td>735</td><td><a href='https://arxiv.org/abs/2609.39071'>LexReward: A Taxonomy-Driven Reward Framework for Legal Language Models</a></td><td>24</td><td>0</td><td>NLP</td><td>법률 응답 품질을 스타일·요소·추론 사슬로 나눈 taxonomy 기반 보상 모델임. 법률 도메인 보상학습 연구임.</td></tr>
<tr><td>736</td><td><a href='https://arxiv.org/abs/2609.39542'>Comparative study of adapting pre-trained models for driving behavior video captioning</a></td><td>22</td><td>1</td><td>CV</td><td>운전 행동 비디오 캡셔닝에 여러 fine-tuning 기법을 비교한 소규모 연구임. 방법론적 novelty가 낮음</td></tr>
<tr><td>737</td><td><a href='https://arxiv.org/abs/2609.39868'>Completion-Aware Cross-Fidelity Offline-to-Online Reinforcement Learning for Multi-Line Bus Holding</a></td><td>22</td><td>1</td><td>RL</td><td>버스 홀딩 제어를 위한 offline-to-online 교차 fidelity RL 연구임. 응용 범위가 교통 운영에 국한됨</td></tr>
<tr><td>738</td><td><a href='https://arxiv.org/abs/2609.38560'>Detail in Context: A Dual-Scale Machine Learning Framework for Mycosis Fungoides Detection</a></td><td>22</td><td>0</td><td>CV</td><td>dual-magnification CNN과 random forest를 결합한 피부 림프종 진단 프레임워크임. 의료 응용으로 로보틱스와 무관함</td></tr>
<tr><td>739</td><td><a href='https://arxiv.org/abs/2609.39130'>Perceptual Color Difference Modeling Using Machine Learning and Human Similarity Judgments</a></td><td>22</td><td>0</td><td>CV</td><td>인간 유사도 판단 데이터를 모아 색차 지표를 학습한 연구임. 로보틱스와 무관한 색채 평가 응용임</td></tr>
<tr><td>740</td><td><a href='https://arxiv.org/abs/2609.39300'>BMASH: Ball-Motion-Aware Soccer Header Spotting</a></td><td>22</td><td>0</td><td>Video</td><td>축구 헤더 이벤트를 공 움직임 특징과 결합해 탐지하는 BMASH 제안임. 스포츠 분석 응용으로 로보틱스와 무관함</td></tr>
<tr><td>741</td><td><a href='https://arxiv.org/abs/2609.39894'>Spatial-Temporal Multi-scale Network for Screen Content Video Quality Enhancement</a></td><td>22</td><td>0</td><td>Video</td><td>화면 콘텐츠 비디오에 특화된 품질 향상 네트워크 STM-Net 제안임. 응용이 스크린 콘텐츠 복원에 국한됨</td></tr>
<tr><td>742</td><td><a href='https://arxiv.org/abs/2609.40212'>Recognition of Urbanized Areas in UAV-Derived Very-High-Resolution Visible-Light Imagery</a></td><td>22</td><td>0</td><td>CV</td><td>UAV RGB 영상으로 도시화 지역을 분류하는 비교 연구임. 원격탐사 응용으로 로보틱스와 무관함</td></tr>
<tr><td>743</td><td><a href='https://arxiv.org/abs/2609.38491'>Role-guided Speaker Deletion Verification in Clinical Psychiatry Speech Recordings with Audio Language Models</a></td><td>22</td><td>0</td><td>LG</td><td>정신과 임상 녹음에서 특정 화자 삭제 여부를 오디오 언어모델로 검증하는 연구임. 의료 프라이버시 응용으로 로보틱스와 무관함</td></tr>
<tr><td>744</td><td><a href='https://arxiv.org/abs/2609.38744'>Molecular Property Prediction under Structural Shift with Tabular Foundation Models</a></td><td>22</td><td>0</td><td>LG</td><td>분자 물성 예측 in-context learning 개선, 신약개발 문제로 로보틱스 무관</td></tr>
<tr><td>745</td><td><a href='https://arxiv.org/abs/2609.38767'>dattri-LLM: A Unified and Efficient Library for Training Data Attribution at LLM Scale</a></td><td>22</td><td>0</td><td>LG</td><td>LLM 스케일 training data attribution 라이브러리, 엔지니어링 기여임</td></tr>
<tr><td>746</td><td><a href='https://arxiv.org/abs/2609.38785'>How Accurate Is Accurate Enough?</a></td><td>22</td><td>0</td><td>LG</td><td>수치 근사 오차가 학습에 미치는 영향 이론화, 로보틱스와 거리 있음</td></tr>
<tr><td>747</td><td><a href='https://arxiv.org/abs/2609.39025'>A Rank Graduation metric for Algorithmic fairness</a></td><td>22</td><td>0</td><td>LG</td><td>알고리즘 공정성 평가를 위한 rank 기반 지표 제안, 신용평가 응용으로 로보틱스 무관</td></tr>
<tr><td>748</td><td><a href='https://arxiv.org/abs/2609.39131'>Characterizing High Bandwidth Flash for LLM Serving</a></td><td>22</td><td>0</td><td>LG</td><td>LLM 서빙용 고대역폭 플래시 메모리 특성 분석, 시스템 인프라 연구임</td></tr>
<tr><td>749</td><td><a href='https://arxiv.org/abs/2609.39194'>Importance-Aware Feature Sparsification for Wireless Split Learning</a></td><td>22</td><td>0</td><td>LG</td><td>무선 split learning의 feature sparsification 기법, 통신 효율화 연구임</td></tr>
<tr><td>750</td><td><a href='https://arxiv.org/abs/2609.39268'>A Time-Aware Bag-of-Receptive-Fields for Interpretable Irregular Time Series Classification</a></td><td>22</td><td>0</td><td>LG</td><td>불규칙 시계열 분류용 해석가능 bag-of-receptive-fields 확장, 의료/모빌리티 응용임</td></tr>
<tr><td>751</td><td><a href='https://arxiv.org/abs/2609.39296'>Semantic-Aware Joint Source-Channel Optimization for Encoder-Agnostic Digital Video Communication</a></td><td>22</td><td>0</td><td>LG</td><td>인코더 독립적 비디오 semantic communication 최적화, 통신 시스템 연구임</td></tr>
<tr><td>752</td><td><a href='https://arxiv.org/abs/2609.39340'>ElectrolyteFM: Unifying Electrolyte Property Prediction through Cross-Property Knowledge Learning</a></td><td>22</td><td>0</td><td>LG</td><td>전해질 다중 물성 예측 통합 모델, 배터리 소재 응용으로 로보틱스 무관</td></tr>
<tr><td>753</td><td><a href='https://arxiv.org/abs/2609.39496'>When the Right Answer Is Missing: An Arithmetic-Dependent Rejection Bottleneck in Jev</a></td><td>22</td><td>0</td><td>NLP</td><td>typed decision model의 산술 문제 거부 실패 현상 보고 및 threshold 보정, 모델 행동 분석 리포트임</td></tr>
<tr><td>754</td><td><a href='https://arxiv.org/abs/2609.39613'>Hybrid Methods for Robust Tabular Data Imputation</a></td><td>22</td><td>0</td><td>LG</td><td>저랭크 초기화와 random forest를 결합한 하이브리드 결측치 대체 기법, 통계적 방법론임</td></tr>
<tr><td>755</td><td><a href='https://arxiv.org/abs/2609.39626'>Parameterization method of reservoir properties for ensemble-based data assimilation using intermediate latent space of StyleGAN</a></td><td>22</td><td>0</td><td>LG</td><td>StyleGAN2 잠재공간으로 저류층 특성 파라미터화, 석유공학 응용으로 로보틱스 무관</td></tr>
<tr><td>756</td><td><a href='https://arxiv.org/abs/2609.39630'>PEG-Tab: Sampling-Time Record Repair and Release Control for Tabular Synthesis</a></td><td>22</td><td>0</td><td>LG</td><td>표 데이터 합성 샘플링 시점 record repair로 프라이버시 위험 저감, 프라이버시 공학 기법임</td></tr>
<tr><td>757</td><td><a href='https://arxiv.org/abs/2609.39646'>Beyond Uniform Compression: Budgeted Transmission Allocation for Extreme Federated Learning</a></td><td>22</td><td>0</td><td>LG</td><td>극단적 업링크 예산 하의 레이어별 적응 압축 할당, 연합학습 통신 효율화임</td></tr>
<tr><td>758</td><td><a href='https://arxiv.org/abs/2609.39789'>Pseudo-Label-Triggered Retraining from Forecast Errors for Online Time Series Forecasting</a></td><td>22</td><td>0</td><td>LG</td><td>예측오차 기반 online retraining 시점 학습 트리거, 시계열 배포 운영 기법임</td></tr>
<tr><td>759</td><td><a href='https://arxiv.org/abs/2609.39810'>A Comprehensive Benchmark of Source-Free Universal Domain Adaptation on Time Series Representations</a></td><td>22</td><td>0</td><td>LG</td><td>source-free universal domain adaptation을 시계열에 처음 벤치마크화, 평가방법론 연구임</td></tr>
<tr><td>760</td><td><a href='https://arxiv.org/abs/2609.40120'>Scalable Cox Regression via Grouped Risk Sets and Sharper LogSumExp Rates</a></td><td>22</td><td>0</td><td>LG</td><td>대규모 Cox 회귀의 LogSumExp 확률적 최적화 수렴률 개선, 생존분석 통계 연구임</td></tr>
<tr><td>761</td><td><a href='https://arxiv.org/abs/2609.38820'>BARRAC: Adaptation of an English Aspect-based Sentiment Analysis Approach for Classification Tasks in Arabic Dialects</a></td><td>22</td><td>0</td><td>NLP</td><td>영어 ABSA 프레임워크를 아랍 방언 분류 과제에 맞게 수정함. 저자원 언어 NLP 적응 연구임.</td></tr>
<tr><td>762</td><td><a href='https://arxiv.org/abs/2609.39001'>The Invisible Language Tax: Token Premiums of French and Regional Languages in 2026 LLM Tokenizers, and a French-Optimized Prototype</a></td><td>22</td><td>0</td><td>NLP</td><td>프랑스어가 영어보다 토큰을 더 많이 쓰는 비용 불균형을 측정하고 tokenizer를 개선함. 다국어 비용 효율 연구임.</td></tr>
<tr><td>763</td><td><a href='https://arxiv.org/abs/2609.39049'>Structure vs. Chain-of-Thought: Evaluating LLM Criteria Extraction for Depression Severity</a></td><td>22</td><td>0</td><td>NLP</td><td>우울증 중증도 판정에 criteria extraction과 CoT를 비교함. 정신건강 NLP 평가 연구임.</td></tr>
<tr><td>764</td><td><a href='https://arxiv.org/abs/2609.38282'>Improving OCR Faithfulness via Gated and Attenuated On-Policy Distillation</a></td><td>22</td><td>0</td><td>CV</td><td>VLM의 OCR 충실도를 teacher distillation 강도 조절로 개선한 방법임</td></tr>
<tr><td>765</td><td><a href='https://arxiv.org/abs/2609.38600'>Sense and Sensitivity: Benchmarking LLM Clinical Triage Recommendations with Physician Experts</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM과 의사의 임상 trage 권고를 텍스트 변형에 대한 민감도로 비교한 연구임</td></tr>
<tr><td>766</td><td><a href='https://arxiv.org/abs/2609.38642'>ChartRevise: A Dataset and Evaluation Protocol for Exact Chart Editing via Code</a></td><td>22</td><td>0</td><td>CV</td><td>코드 기반 차트 편집을 정확히 평가하는 데이터셋·프로토콜임</td></tr>
<tr><td>767</td><td><a href='https://arxiv.org/abs/2609.38827'>More Choices, Fewer Decisions: Ordinal-Scale Bias in JEV-like Direct-Decision Models</a></td><td>22</td><td>0</td><td>NLP</td><td>direct-decision 모델이 ordinal scale을 충분히 활용하지 못하는 편향을 정의·측정함</td></tr>
<tr><td>768</td><td><a href='https://arxiv.org/abs/2609.38974'>RealWorldShop: Benchmarking and Improving Conversational Shopping Agents in Real-World E-commerce</a></td><td>22</td><td>0</td><td>NLP</td><td>실제 전자상거래 대화형 쇼핑 agent 벤치마크 및 상태관리 프레임워크임</td></tr>
<tr><td>769</td><td><a href='https://arxiv.org/abs/2609.39371'>EHR-RobustGym: Benchmarking and Training Agents for Robust Clinical Reasoning</a></td><td>22</td><td>0</td><td>NLP</td><td>잡음 있는 EHR에서 임상 agent의 강건성을 평가·훈련하는 벤치마크임</td></tr>
<tr><td>770</td><td><a href='https://arxiv.org/abs/2609.39054'>CLIPPER Beyond Shortlisting: Auditable Decision Support for Changing Municipal Micromobility Policies</a></td><td>20</td><td>1</td><td>LG</td><td>도시 공유 모빌리티 주차정책 재최적화를 위한 감사 가능 greedy 최적화기임. 로보틱스·embodied AI와 무관한 정책 도구임.</td></tr>
<tr><td>771</td><td><a href='https://arxiv.org/abs/2609.38271'>Evaluating Multi-Task Morphological Concept Learning for Pulmonary Nodule Malignancy Assessment in 3D CT</a></td><td>20</td><td>0</td><td>CV</td><td>LIDC 데이터로 multi-task 학습이 malignancy 분류를 개선 못했다는 부정적 결과 보고임. novelty 낮고 로보틱스와 무관함</td></tr>
<tr><td>772</td><td><a href='https://arxiv.org/abs/2609.38190'>Travel Time Prediction in Supply Chain Management Using Machine Learning</a></td><td>20</td><td>0</td><td>LG</td><td>공급망 물류의 이동 시간을 예측하는 ML 응용 연구임. 방법론적 novelty가 낮고 로보틱스와 무관함</td></tr>
<tr><td>773</td><td><a href='https://arxiv.org/abs/2609.38608'>Learning-Enabled Estimation: Tight Characterizations under Sample Selection Biases</a></td><td>20</td><td>0</td><td>LG</td><td>sample selection bias 하의 회귀 식별 이론, 계량경제학 문제라 로보틱스 무관</td></tr>
<tr><td>774</td><td><a href='https://arxiv.org/abs/2609.39067'>Argus: A Real-EKS Study of When Predicting Spot Interruptions Beats Simple Checkpointing</a></td><td>20</td><td>0</td><td>LG</td><td>spot instance 중단 예측 체크포인팅 시스템, 분산학습 인프라 연구임</td></tr>
<tr><td>775</td><td><a href='https://arxiv.org/abs/2609.39250'>Client and Training Data Selection for Computationally Efficient Synchronized Federated Learning</a></td><td>20</td><td>0</td><td>LG</td><td>연합학습의 client·데이터 선택으로 수렴 가속, 연합학습 시스템 연구임</td></tr>
<tr><td>776</td><td><a href='https://arxiv.org/abs/2609.39581'>Robust Transfer Learning for Paper ECG Recognition</a></td><td>20</td><td>0</td><td>CV</td><td>종이 ECG 이미지 인식을 위한 rank-aware contrastive learning, 의료영상 응용임</td></tr>
<tr><td>777</td><td><a href='https://arxiv.org/abs/2609.39644'>RiboUnmix: Learning Shared Translational Dynamics from Biased and Noisy Ribo-seq Measurements</a></td><td>20</td><td>0</td><td>LG</td><td>Ribo-seq 측정의 실험별 편향을 분리하는 확률모델, 생물학 응용으로 로보틱스 무관</td></tr>
<tr><td>778</td><td><a href='https://arxiv.org/abs/2609.39741'>The Nixtlaverse: An Open-Source Ecosystem for Forecasting</a></td><td>20</td><td>0</td><td>LG</td><td>통계·ML·신경망 예측을 통합하는 오픈소스 예측 생태계 소개, 소프트웨어 인프라 논문임</td></tr>
<tr><td>779</td><td><a href='https://arxiv.org/abs/2609.40170'>MANET-GNN: Learned Decentralized Optimization of Power Allocation in Multi-Channel MANETs</a></td><td>20</td><td>0</td><td>LG</td><td>MANET 무선망 전력 분배 GNN 최적화임. 로봇 학습과 무관함.</td></tr>
<tr><td>780</td><td><a href='https://arxiv.org/abs/2609.40312'>Compression Footprints as Security Signals for Model-Poisoning Defense in Federated Learning</a></td><td>20</td><td>0</td><td>LG</td><td>federated learning 압축 흔적 기반 poisoning 방어임. 로보틱스와 무관함.</td></tr>
<tr><td>781</td><td><a href='https://arxiv.org/abs/2609.40335'>Is Weight Tying Still Beneficial for Decoder-Only LLMs in Private Settings Under DP-SGD?</a></td><td>20</td><td>0</td><td>NLP</td><td>DP-SGD 환경에서 weight tying 영향을 분석함. 프라이버시 학습 연구로 robotics 무관함.</td></tr>
<tr><td>782</td><td><a href='https://arxiv.org/abs/2609.38203'>Automatic estimation of verbal fluency index in people with Motor Neuron Disease using ASR alignment and pause modelling</a></td><td>20</td><td>0</td><td>NLP</td><td>ASR 정렬로 운동신경질환 환자의 언어유창성 지수를 자동 추정함. 의료 음성 연구임.</td></tr>
<tr><td>783</td><td><a href='https://arxiv.org/abs/2609.39225'>Argument Structure Prediction in Online Conversations: A Comparative Study of Modeling Paradigms and Task Architectures</a></td><td>20</td><td>0</td><td>NLP</td><td>논증 구조 예측 아키텍처 비교 연구임. incremental benchmark 성격</td></tr>
<tr><td>784</td><td><a href='https://arxiv.org/abs/2609.39368'>Making Grid Beam Search Less Greedy</a></td><td>20</td><td>0</td><td>NLP</td><td>grid beam search의 constraint 순서 편향을 고치는 디코딩 기법임. 범위가 좁음</td></tr>
<tr><td>785</td><td><a href='https://arxiv.org/abs/2609.39420'>QuantCode Model: Specializing Language Models for Executable Algorithmic Trading Code</a></td><td>20</td><td>0</td><td>NLP</td><td>알고리즘 트레이딩 코드 생성에 특화한 LLM fine-tuning 연구임</td></tr>
<tr><td>786</td><td><a href='https://arxiv.org/abs/2609.39572'>Compact Language, Complex Model Shifts: How and Where Ambiguity and Underspecification Affect LLMs</a></td><td>20</td><td>0</td><td>NLP</td><td>인공 동음이의어·상위어로 언어모델의 모호성 처리를 분석한 연구임</td></tr>
<tr><td>787</td><td><a href='https://arxiv.org/abs/2609.39639'>Marginal Response Surface Elicitation for Zero-Label Tabular Learning</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM prior로 레이블 없는 tabular classifier를 만드는 방법임</td></tr>
<tr><td>788</td><td><a href='https://arxiv.org/abs/2609.39640'>Zero-Compute Cross-Lingual Transferability Estimation Using Typological Feature Proxies</a></td><td>20</td><td>0</td><td>NLP</td><td>typology feature만으로 cross-lingual transfer를 예측하는 zero-compute 방법임</td></tr>
<tr><td>789</td><td><a href='https://arxiv.org/abs/2609.39853'>Cognitive Enhancement: Rethinking the Necessity of Role-Playing for Large Language Models</a></td><td>20</td><td>0</td><td>NLP</td><td>role-play 프롬프팅 효과가 모델·도메인·언어에 따라 달라짐을 보인 실증 연구임</td></tr>
<tr><td>790</td><td><a href='https://arxiv.org/abs/2609.40181'>Index-Translate: A Multilingual Translation Model Family -- Text, Speech, Controlled Dubbing, and Long-Document Translation</a></td><td>20</td><td>0</td><td>NLP</td><td>다국어 번역·더빙 모델 패밀리를 구축한 산업 논문임</td></tr>
<tr><td>791</td><td><a href='https://arxiv.org/abs/2609.40198'>SCB: SpeechConversationBench for Evaluating Multi-Turn Reasoning in Speech-to-Speech Models</a></td><td>20</td><td>0</td><td>NLP</td><td>음성 대화에서 multi-turn 수학 reasoning을 평가하는 벤치마크임</td></tr>
<tr><td>792</td><td><a href='https://arxiv.org/abs/2609.40236'>Comparison of techniques for fine-tuning open-weight models for entity extraction from radiology reports</a></td><td>20</td><td>0</td><td>NLP</td><td>방사선 보고서 엔티티 추출에서 fine-tuning 전략을 비교한 응용 연구임</td></tr>
<tr><td>793</td><td><a href='https://arxiv.org/abs/2609.38346'>Examining Variation in How Guided AI Tutors Resolve Student Impasses</a></td><td>20</td><td>0</td><td>NLP</td><td>AI 튜터가 학생 impasse를 다루는 방식을 분석한 교육 응용 연구임</td></tr>
<tr><td>794</td><td><a href='https://arxiv.org/abs/2609.38386'>Decode-Latency Feedback Prefill: A Model-Free Controller and Its Generalization Limits</a></td><td>20</td><td>0</td><td>LG</td><td>LLM serving의 prefill 청크 크기를 피드백으로 조절하는 model-free controller임. 일반화 한계를 스스로 보고함</td></tr>
<tr><td>795</td><td><a href='https://arxiv.org/abs/2609.38512'>VAmoS Part Deux: Harder, More Realistic Voice-Agent Simulation</a></td><td>20</td><td>0</td><td>NLP</td><td>배경 소음이 있는 복잡한 음성 agent 시나리오 벤치마크임</td></tr>
<tr><td>796</td><td><a href='https://arxiv.org/abs/2609.38574'>Towards Model as a Library: Offline, Community-Sourced AI for Low-Resource African Languages</a></td><td>20</td><td>0</td><td>NLP</td><td>저자원 아프리카 언어를 위한 오프라인 음성모델 아키텍처 포지션 논문임</td></tr>
<tr><td>797</td><td><a href='https://arxiv.org/abs/2609.38782'>Persona and Persuasive Framing in AI Voice Agents: A $2\times2$ Field Experiment with Children</a></td><td>20</td><td>0</td><td>NLP</td><td>아동 대상 음성 AI의 persona·설득 프레이밍 효과를 실제 필드 실험으로 측정함</td></tr>
<tr><td>798</td><td><a href='https://arxiv.org/abs/2609.38869'>Reasoning Externalization for Faithful Large Language Model Narratives of Stock Return Predictions</a></td><td>20</td><td>0</td><td>NLP</td><td>SHAP 증거를 외재화해 주가예측 LLM 설명의 충실도를 높인 금융 응용 연구임</td></tr>
<tr><td>799</td><td><a href='https://arxiv.org/abs/2609.39107'>MASCRDM: Multi-Agent System for Compliance Risk Detection and Mitigation in Training Process of Large Language Models</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 학습 과정에서 컴플라이언스 위험을 실시간 감지하는 멀티에이전트 시스템임</td></tr>
<tr><td>800</td><td><a href='https://arxiv.org/abs/2609.39483'>Who Owns That? Evaluating Ownership Intuitions in Large Language Models</a></td><td>20</td><td>0</td><td>NLP</td><td>경쟁하는 소유권 주장에 대한 LLM 판단을 인간과 비교한 사회인지 연구임</td></tr>
<tr><td>801</td><td><a href='https://arxiv.org/abs/2609.39958'>Better Deck or Different Judge? Evaluating Agentic Harness Gains in Corporate and Investment Banking</a></td><td>20</td><td>0</td><td>NLP</td><td>투자은행 문서 생성 agent의 LLM judge 점수가 실제 품질 개선인지 judge 변동인지 회의적으로 검증한 연구임</td></tr>
<tr><td>802</td><td><a href='https://arxiv.org/abs/2609.38391'>Team MSU GenText-Forensics Challenge 2026 Technical Report</a></td><td>18</td><td>0</td><td>CV</td><td>ACM MM 챌린지 3위 기술 보고서임. 기존 VLM을 LoRA로 조합한 파이프라인 수준이라 novelty 낮음</td></tr>
<tr><td>803</td><td><a href='https://arxiv.org/abs/2609.39232'>What Streaming Anomaly Detection Finds (and Misses) in Industrial Time Series</a></td><td>18</td><td>0</td><td>LG</td><td>원전 산업 데이터 스트리밍 이상탐지 비교 연구, 산업 응용 리포트임</td></tr>
<tr><td>804</td><td><a href='https://arxiv.org/abs/2609.39257'>From Benchmarks to Production: Transferring Time Series Anomaly Detection Methods for Electricity Production Monitoring</a></td><td>18</td><td>0</td><td>LG</td><td>전력 생산 예측 이상탐지 산업 시스템, 응용 리포트 수준임</td></tr>
<tr><td>805</td><td><a href='https://arxiv.org/abs/2609.39013'>Evidence First, Arithmetic Second: A System Report and Failure Analysis for DocSem</a></td><td>18</td><td>0</td><td>NLP</td><td>DocSem shared task 시스템 보고서로 OCR 병합 오류를 사후 분석함. 대회 결과 리포트 수준임.</td></tr>
<tr><td>806</td><td><a href='https://arxiv.org/abs/2609.38219'>TutlAit v1: a crowdsourced Moroccan Tamazight speech dataset with Arabic transcriptions and regional accent labels</a></td><td>16</td><td>0</td><td>NLP</td><td>모로코 타마지트어 crowdsourced 음성 데이터셋 구축임. 저자원 언어 자원 구축 연구임.</td></tr>
<tr><td>807</td><td><a href='https://arxiv.org/abs/2609.39189'>ViLegalExpert: A Large-Scale Benchmark for Vietnamese Legal Retrieval and Question Answering from Real-World Consultations</a></td><td>15</td><td>0</td><td>NLP</td><td>베트남어 법률 QA 벤치마크 구축 논문임. 우선순위 주제와 무관함</td></tr>
<tr><td>808</td><td><a href='https://arxiv.org/abs/2609.39385'>TTLab at Daleel 2026: STAR-Ar, Sequence Tagging for Argument Recognition in Arabic</a></td><td>15</td><td>0</td><td>NLP</td><td>아랍어 argument mining shared task 시스템 논문임</td></tr>
<tr><td>809</td><td><a href='https://arxiv.org/abs/2609.39975'>Overview of BioASQ 2026: The fourteenth BioASQ Challenge on Large-Scale Biomedical Semantic Indexing and Question Answering</a></td><td>15</td><td>0</td><td>NLP</td><td>BioASQ 2026 챌린지 개요 논문임. 참가팀 결과 요약</td></tr>
<tr><td>810</td><td><a href='https://arxiv.org/abs/2609.40041'>MGhana-ST: A Low-Resource Speech Translation Dataset for Ghanaian Languages and an Analysis of Multilingual Training Trade-offs</a></td><td>15</td><td>0</td><td>NLP</td><td>가나 저자원 언어 음성번역 데이터셋 구축 및 multilingual training trade-off 분석임</td></tr>
<tr><td>811</td><td><a href='https://arxiv.org/abs/2609.40108'>OverdoseMoE: A Multi-Expert Framework for Opioid Overdose Risk Prediction</a></td><td>15</td><td>0</td><td>NLP</td><td>아편계 과다복용 위험 예측을 위한 multi-expert 임상 모델임. 분야 무관</td></tr>
<tr><td>812</td><td><a href='https://arxiv.org/abs/2609.38559'>Defining and Categorising Human-AI Interactions in Clinical Trials: A Multidimensional Human-AI Classification Approach</a></td><td>15</td><td>0</td><td>NLP</td><td>임상시험의 human-AI 상호작용을 분류하는 프레임워크 논문임</td></tr>
<tr><td>813</td><td><a href='https://arxiv.org/abs/2609.38818'>Whose Voice Survives the Summary? A Voice-Retention Audit of LLM Employee Listening</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM 요약이 직원 피드백의 목소리를 편향되게 걸러냄을 측정하는 audit 지표임</td></tr>
<tr><td>814</td><td><a href='https://arxiv.org/abs/2609.38627'>Marking Contour Tones in Yorùbá</a></td><td>14</td><td>0</td><td>NLP</td><td>요루바어 contour tone 표기를 위한 caron·circumflex 부호 제안임. 언어학 표기법 연구임.</td></tr>
<tr><td>815</td><td><a href='https://arxiv.org/abs/2609.39627'>Introduction to Computer Vision</a></td><td>10</td><td>0</td><td>CV</td><td>컴퓨터 비전 입문 교재임. 연구 기여가 아니라 교육 자료라 평가 대상에서 제외됨</td></tr>
<tr><td>816</td><td><a href='https://arxiv.org/abs/2609.39460'>Right-Wing Rock or Just Rock? A Computational Linguistic Analysis of Frei.Wild</a></td><td>10</td><td>0</td><td>NLP</td><td>독일 극우 록밴드의 정치 성향을 분석한 사회언어학 연구임. 분야 무관</td></tr>
<tr><td>817</td><td><a href='https://arxiv.org/abs/2609.40064'>From Tweets to Trades: Analyzing the Influence of Public Mood over Stock Market Performance in Turkiye</a></td><td>10</td><td>0</td><td>NLP</td><td>튀르키예 주식시장과 소셜미디어 여론의 상관관계를 분석한 행동재무 연구임</td></tr>
<tr><td>818</td><td><a href='https://arxiv.org/abs/2609.38788'>Positive Ratings, Hidden Concerns: Employee Voice Disclosure in AI-Mediated Organizational Listening</a></td><td>10</td><td>0</td><td>NLP</td><td>AI 음성 인터뷰에서 직원들이 우려를 숨기는 패턴을 분석한 조직행동 연구임</td></tr>
</tbody></table>

</details>
