# 오늘의 arXiv Top 15 — 2026-08-28 (금)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**
> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)

**신규 논문 수: 전체 419편 → 중복 제거 후 419편 (이번 평가 대상 419편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 93 |
| cs.LG | 77 |
| cs.RO | 35 |
| cs.CL | 118 |
| cs.AI | 96 |

*1차 스크리닝: 전체 419편을 제목/초록 기반으로 채점(Claude (scheduled agent)) → 상위 15편은 arXiv 원문을 내려받아 정밀 리뷰(Claude (scheduled agent)) 후 최종 점수 산정.*

---

## Top 15

### 1. [78점] Predicting Consequences and Reinforcing Navigation Policies with Latent World Models

- **분야**: World Model / Robot Navigation · **robotics relevance**: 9/10
- **arXiv**: [2608.26190](https://arxiv.org/abs/2608.26190) ([PDF](https://arxiv.org/pdf/2608.26190))
- **저자**: Zengmao Wang, Wei Gao, Shuhan Shen
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **원문 검토**: PDF 전문 · 1차 스크리닝 78점

> 💡 future observation을 재구성하는 대신 action-conditioned latent feature의 compatibility만 예측하는 world model인 LWM을 제안함. 다른 trajectory의 action sequence를 가져와 counterfactual 학습에 쓰고, 이 world model로 unlabeled video에서 policy를 학습·강화해서 real-world navigation에서 기존 world model·imitation learning 대비 큰 성능 향상을 보임.

**Core innovation & methodology**

- world model의 목표를 pixel/feature reconstruction에서 action-conditioned latent compatibility prediction으로 바꿈. 공간적으로 가까우면 latent feature도 유사하다는 가정을 이용해 goal image와의 compatibility score만 예측
- counterfactual imagination: 같은 offline dataset 내 다른 trajectory에서 action sequence를 가져와 현재 observation에 대한 negative/hard negative로 사용, cross-trajectory InfoNCE 및 log-distance 기반 MSE loss로 학습
- world model을 이용해 unlabeled video에 pseudo action label을 부여(compatibility 최고인 action sequence 선택)해서 policy를 supervised로 학습시키고, 이후 world model을 reward model 삼아 GRPO 스타일 RL로 policy를 world model 내부에서만 추가 강화(실제 환경 상호작용 없음)
- goal image를 observation encoding 단계에서 미리 주는 LWM-B-P variant가 가장 좋은 성능을 보임 (goal-conditioned encoding)

**Novelty vs. prior works**

- 가장 가까운 prior work인 NWM(pixel-level video generation 기반 world model)과 Dino-WM(frozen DINOv2 feature reconstruction) 대비, reconstruction objective 자체를 없애고 compatibility discrimination으로 대체한 것이 formulation 수준의 차이임
- counterfactual action sequence를 다른 trajectory에서 가져와 학습에 쓰는 방식은 offline data augmentation에 가까운 아이디어지만, world model 학습에 명시적으로 counterfactual reasoning을 주입한 점은 novelty 있음
- 다만 spatial proximity가 visual similarity와 상관관계가 있다는 inductive bias는 저자도 인정하듯 occlusion이 심한 cluttered environment에서는 깨질 수 있어, navigation이라는 특정 도메인에 강하게 의존하는 가정임

**Benchmark results**

- RECON/SCAND/자체 수집 LWM-Dataset(6시간, 60만 m² 실외) 세 데이터셋에서 world model prediction 평가: LWM-B-P가 PE(Position Error)/OE(Orientation Error, 본문 확인 필요) 최저(RECON 1.264/0.425, SCAND 0.651/0.122, LWM-Dataset 1.122/0.125), ACC5 절대값 기준 NWM(26~27%)·Dino-WM(24~74%) 대비 최고 83.8% 달성
- policy learning 평가(Table 2)에서도 world model이 만든 pseudo label로 학습한 policy가 NWM/Dino-WM supervision 대비 PE/OE 최저
- real-world 6개 navigation 시나리오에서 LWM-B-P가 success rate 66.7% (NoMaD, BC는 각 33.3%), LPIPS도 최저(0.396) — 다만 6개 시나리오라는 적은 표본 규모
- ablation: counterfactual action sequence 수 M을 1→16으로 늘릴수록 ACC5가 23.83%→58.54%로 개선(SCAND), M=1(counterfactual 없음)이 성능을 크게 저해함을 확인
- loss ablation에서 제안한 log-distance 기반 MSE가 순수 contrastive loss·ranking loss 대비 ACC3 90.6% vs 36~86%로 우수
- 실물 로봇 배포는 이루어졌으나 6개 시나리오, indoor generalization은 정성적(성공 사례) 시연 수준이라 통계적 일반화 근거는 제한적임

**Top-tier conference 적합성 — 72/100 · 추천 venue: CoRL**

world model formulation의 새로운 관점(compatibility prediction)과 real-world navigation deployment, RL-in-imagination까지 포함한 완결된 파이프라인이 CoRL/RSS 수준의 강점임. 다만 navigation이라는 좁은 action space(x, y, θ)에 한정되고, spatial proximity=visual similarity 가정이 강한 도메인 특화 inductive bias라서 일반 manipulation이나 highly dynamic/occluded 환경으로의 확장성은 검증되지 않아 top-tier oral보다는 poster/spotlight 수준으로 판단됨.

**추천 이유 & 누리랩 연구와의 연결점**

- world model을 reconstruction 없이 discriminative compatibility로 학습하는 방식은 누리랩의 test-time optimization/inference-time planning 주제와 직접 연결됨 — manipulation에서도 pixel reconstruction 없이 latent compatibility만으로 action selection이 가능한지 검토할 가치 있음
- counterfactual action sequence를 offline data에서 cross-trajectory로 가져오는 기법은 counterfactual/causal reasoning 주제에 활용 가능. failure detection/recovery 맥락에서 '실패로 이어질 counterfactual action'을 이 방식으로 라벨링하는 확장 고려 가능
- world model을 reward model 삼아 imagination 내에서만 GRPO로 policy 강화하는 구조는 실 로봇 상호작용 없이 policy를 개선한다는 점에서 test-time optimization 연구와 결합 가능성 있음

---

### 2. [77점] Riemann-1.0: An Embodied World Action Model for Physical AI

- **분야**: World Model / VLA (Embodied Foundation Model) · **robotics relevance**: 10/10
- **arXiv**: [2608.27033](https://arxiv.org/abs/2608.27033) ([PDF](https://arxiv.org/pdf/2608.27033))
- **저자**: Haofeng Sun, Jiangbo Pei, Fei Kang, Zexiang Liu, Yaokun Li, Boyi Jiang, Hua Xue, Cindy Zhou 외 8명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 로봇 policy 실행과 action-conditioned world simulation을 하나의 causal autoregressive 모델(action 예측 후 그 action을 조건으로 visual latent 예측)로 통합한 Riemann-1.0을 제안함. 인간 1인칭 영상, UMI/외골격 시연, 이종 로봇 궤적 200K+시간을 3단계 progressive pretraining(pseudo action→실제 action→로봇 전용)으로 통합해 시뮬레이션·실로봇 벤치마크 다수에서 SOTA를 달성함.

**Core innovation & methodology**

- action과 visual latent를 하나의 causal 시퀀스로 묶어, 매 스텝마다 이전 관측·상태·action 이력으로 다음 action을 예측하고 그 action을 조건으로 다음 visual latent를 예측하는 fully causal factorization을 사용함(joint denoising도, video-first도 아님).
- 배포 시 predicted visual latent를 실제 환경 관측으로 치환하면 policy로, 그대로 재입력하면 world simulator로 동작해 동일 모델이 두 역할을 겸함.
- Stage 1(frozen Latent Action Model이 라벨 없는 인간 영상에서 pseudo action 추출, λ=0.1) → Stage 2(UMI/로봇/3D hand-pose 인간 데이터로 실제 action에 정렬, λ=0.5) → Stage 3(고품질 로봇 데이터로 정책 특화, λ=0.9)의 3단계 커리큘럼으로 이종 데이터를 단계적으로 통합함.
- embodiment별 canonical action/state 표현과 category-specific projection head를 둬 하나의 backbone을 공유하면서도 로봇마다 다른 action 차원·좌표계를 처리함.

**Novelty vs. prior works**

- DreamZero(joint generation), LingBot-VA(video-first prediction), FastWAM(decoupled action-video DiT) 등 최근 WAM들과 비교해, action이 먼저 예측되고 이를 조건으로 visual latent가 생성되는 순서를 강제하는 fully causal 구조가 차별점이며 이 순서가 실제 로봇의 action→관측 인과 흐름과 일치한다고 주장함.
- 그러나 이 차별점은 기존 3가지 패러다임(joint/video-first/decoupled) 대비 '액션 우선 순서'라는 architecture 선택의 변형에 가깝고, GigaWorld-Policy 등 동시기 유사 연구가 다수 존재해 근본적으로 새로운 problem formulation이라기보다 engineering적 정제로 판단됨.
- 데이터 통합(200K+시간, LAM 기반 pseudo action bootstrapping) 자체는 규모 면에서 인상적이나, human video→robot action 정렬이라는 방향성은 최근 cross-embodiment 학습 흐름(Being-H0.5 등 인용 문헌)의 연장선임.

**Benchmark results**

- RoboTwin2.0 94.3%, LIBERO 99.0%, RoboCasa-365 62.6%로 세 벤치마크 모두 SOTA 주장, RoboCasa-365에서 이전 최고(ABot-M0.5 54.2%) 대비 +8.4%p — 다만 이 수치들이 sim 벤치마크임은 명시해야 함.
- 실로봇(Tianji Marvin dual-arm) 4개 task(순서대로 쌓기, 옷개기, 책상정리, 주방정리) 평균 SR(Success Rate) 85.0%, PSR(Partial Success Rate, 원문 확인 필요) 94.4%로, 가장 강한 오픈소스 baseline G0.5(SR 70.0%, PSR 80.18%) 대비 SR +15.0%p.
- task별 편차 큼: kitchen organization은 90.0% SR(G0.5는 35.0%)로 격차가 매우 크지만, ordered cube stacking은 85.0% vs G0.5 80.0%로 격차가 작음 — 개선폭이 task에 따라 불균일함.
- 각 실로봇 task는 15개 teleoperation 시연으로 post-training(pretraining 후 fine-tuning)했다고 명시돼 있어, 순수 zero-shot pretraining 성능이 아니라 task별 소량 fine-tuning이 포함된 수치임에 유의해야 함.
- 본문 발췌본에서 세부 ablation(3-stage curriculum 각 단계의 개별 기여도, action loss weight λ 스케줄의 정량적 효과)은 확인 불가 — 텍스트 중간 생략 구간에 있을 가능성이 있으나 제공된 발췌에서는 근거를 찾지 못함.

**Top-tier conference 적합성 — 72/100 · 추천 venue: CoRL**

대규모 실로봇 검증과 다수 벤치마크 SOTA는 강점이나, 핵심 architecture 기여가 동시기 WAM들과의 차이가 'causal ordering' 정도로 제한적이고 기업 기술보고서 성격이 강해(학회 제출 여부 불명, 소속이 스타트업) ablation 깊이가 부족해 보임 — 이 부분이 review에서 지적될 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- action-conditioned world simulation과 policy 실행을 한 모델로 통합한 구조는 world model 기반 test-time planning(가상 rollout으로 실패 가능성 사전 평가) 연구에 바로 활용 가능함.
- 인간 영상→UMI→로봇 순으로 감독 신호 신뢰도를 높여가는 progressive pretraining curriculum은 로봇 시연 데이터가 부족한 새 task/embodiment로 확장할 때 참고할 수 있는 데이터 전략임.
- 동일 모델이 policy와 world simulator를 겸하는 특성은 failure prediction(action 실행 전 결과를 시뮬레이션해 위험 감지)이나 counterfactual reasoning(다른 action을 가정한 반사실 rollout) 연구로 직접 연결됨.

---

### 3. [76점] FLARE: A Failure-Aware Framework for Autonomous Correction and Recovery in Visual-Language Robotic Manipulation

- **분야**: VLA / Failure Detection & Recovery · **robotics relevance**: 9/10
- **arXiv**: [2608.26645](https://arxiv.org/abs/2608.26645) ([PDF](https://arxiv.org/pdf/2608.26645))
- **저자**: Ganlong Zhao, Zijia Tang, Xingping Chen, Zhanghui Kuang, Ye Tian, Guanbin Li
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Accepted to CVPR 2026
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 VLA가 실패 없는 시연 데이터로만 학습돼 오류를 복구하지 못하는 문제를 ID(pose만 낯선 상태)/OOD(환경 자체가 망가진 상태) 두 종류로 나눠 각각 다른 방법으로 해결함. Retry는 perturbation-bridging 증강으로 pose와 task 진행을 분리해서 학습시키고, Reset은 MLLM이 실패 영상을 분석해 object-centric 복구 skill을 자동으로 만들어 냄.

**Core innovation & methodology**

- ID Error(환경은 정상, robot pose만 낯선 상태)와 OOD Error(환경 자체가 task 불가능 상태)를 구분하는 taxonomy를 제시함.
- Retry: 시연 segment 사이에 random perturbation 후 bridging 궤적을 삽입해, robot pose와 환경 상태의 spurious correlation을 깨는 방식으로 재시도 능력을 내재화함.
- Reset: 실행 영상을 Gemini-2.5-Pro가 오프라인 분석해 OOD 실패 유형·대상 object·실패 시점을 자동 라벨링하고, 이를 바탕으로 소수(10~20개)의 human demo를 모아 object-centric reset skill을 학습함.
- 배포 시 online MLLM monitor가 task 수행과 reset skill 사이를 전환하고, LoRA adapter로 task/skill별 policy를 모듈화해 관리함.

**Novelty vs. prior works**

- MimicGen류 segment stitching과 달리 perturbation-bridging은 pose-state 상관관계 자체를 깨는 데 초점을 둬서, 궤적이 한 방향으로만 진행되고 낯선 pose에서 되돌아오는 법을 배우지 못하는 trajectory-monotonic 문제를 정면으로 다룸.
- Phoenix(motion-based self-reflection)와 비교하면 fixed skill library 의존을 넘어 MLLM이 reset skill 수집 대상을 스스로 지정한다는 점에서 데이터 확보 파이프라인이 다름.
- 다만 ID/OOD 구분과 MLLM 기반 실패 분석 자체는 REFLECT, FailSafe 등 기존 self-correction 계열의 연장선이라 완전히 새로운 problem formulation은 아니고, 새로움은 두 메커니즘을 통합한 시스템 설계에 있음.

**Benchmark results**

- RoboMimic 9개 contact-rich task 평균 성공률 84.0%로 Phoenix(57.8%), π0.5 backbone 단독(72.2%) 대비 각각 +26.2%p, +11.8%p 개선. 인간이 직접 보정하는 상한선 Phoenix-Human(78.9%)도 상회함.
- 실로봇 검증: Piper arm 2개 task, 각 40 trial. Stack Three Blocks 62.5%→75.0%, Insert U-shaped Block 45.0%→55.0%로 소규모지만 real-world 개선 확인됨.
- Reset skill 제거 ablation: 평균 -3.5%p, human-oracle 대체 시 +7%p 개선(Coffee/ThreePieceAssembly 4개 조건 평균) — reset 학습의 기여도는 제한적임을 시사.
- Reset skill 성공률은 대상 object에 따라 편차가 큼(coffee machine lid 84% vs coffee pod 24%) — 손 안에서 자세를 바로잡아야 하는 조작은 여전히 취약함.
- MLLM 실패 분류 정확도 88~96%(retry/reset), reset object 식별 78~88%로 파이프라인의 병목이 될 수 있음을 저자도 인정.

**Top-tier conference 적합성 — 82/100 · 추천 venue: CVPR**

CVPR 2026 accept 논문으로, real-robot 검증과 강한 baseline 대비 수치 개선이 뒷받침돼 있어 accept 수준의 완성도는 확인됨. 다만 real-world 실험이 2개 task·40 trial로 규모가 작고 reset skill의 object별 성공률 편차가 커 oral/highlight급 임팩트로 보기는 어려움.

**추천 이유 & 누리랩 연구와의 연결점**

- ID/OOD error taxonomy와 perturbation-bridging은 누리랩의 failure detection·recovery 연구에 바로 적용 가능한 데이터 증강 기법으로 참고할 만함.
- MLLM 기반 오프라인 실패 분석 → skill 수집 → LoRA adapter 학습 파이프라인은 test-time monitoring과 robot memory(실패 사례 축적) 연구를 연결하는 구조로 확장 가능함.
- reset skill의 object별 성공률 편차 문제는 counterfactual reasoning이나 in-hand pose refinement 연구로 이어질 여지가 있음.

---

### 4. [76점] Memory Anchors for Continual Robot Learning

- **분야**: Continual Learning / Robot Manipulation · **robotics relevance**: 9/10
- **arXiv**: [2608.26545](https://arxiv.org/abs/2608.26545) ([PDF](https://arxiv.org/pdf/2608.26545))
- **저자**: Maximilian Du, Zhanyi Sun, Chen Xu, Paarth Shah, Masha Itkina, Shuran Song
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 22 pages, 15 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 continual robot learning에서 experience replay(ER) buffer 안의 일부 데이터만이 과거 task 성능 유지에 크게 기여한다는 사실을 발견하고, 이를 Memory Anchor(새 task와 관측이 겹치지만 요구되는 action이 다른 old task 데이터)로 정의함. latent 유사도와 action disagreement로 Memory Anchor를 찾아 buffer에 보강하는 ANCHORER를 제안해 LIBERO에서 forgetting을 63% 줄이고 real robot에서 성공률을 1.7배 높임.

**Core innovation & methodology**

- ER buffer 내 데이터 중요도가 균일하지 않다는 것을 실험으로 보임: FixedER 대비 transition 단위로 매 task마다 resample하는 RandER가 forgetting variance를 36% 낮추지만, 같은 RandER도 buffer sample에 따라 forgetting이 최대 20%p까지 달라짐
- Memory Anchor를 3단계로 추출: (1) 새 task 데이터를 old policy의 latent space에 투영해 old task와 겹치는 영역(state overlap) 찾기, (2) 그 중 old policy가 예측한 action과 실제 action label이 크게 다른(action disagreement) 지점 선별(gaussian noise 후 denoise로 multimodality false positive 방지), (3) 그 conflict 지점과 latent 상 가장 유사한 old task 데이터를 Memory Anchor로 추출
- ANCHORER: 추출한 Memory Anchor로 ER buffer의 n%를 채우는 buffer curation 알고리즘. diffusion policy와 π0.5 VLA 양쪽에서 검증
- '관측은 유사하지만 action이 상충하는(homogeneous) task'가 forgetting의 주범이라는 task-relationship 기반 진단을 제시하고, 이를 real robot(OpenJar, SweaterFold) task suite 설계에 직접 반영

**Novelty vs. prior works**

- 기존 ER 계열(MIR, GSS 등)은 gradient diversity나 새 task와의 loss 변화만으로 buffer를 다루는데, ANCHORER는 policy의 latent overlap과 action disagreement를 결합해 buffer curation 자체(단순 sampling이 아니라)에 반영한다는 점이 본질적 차이임.
- ablation(Table 2)에서 ANCHORER가 MIR(NBT 0.14)·GSS(0.17)·action disagreement 제거 버전(0.13) 대비 최저 NBT(0.11)를 보여 두 요소(state overlap+action disagreement) 모두 필요함을 실증함.
- HAL(class-conditioned anchor synthesis) 등 continual learning 일반 이론에서의 anchor 개념을 연속적(continuous) visuomotor policy에 맞게 적응시킨 것으로, 완전히 새로운 이론이라기보다는 로봇 imitation learning 도메인에 맞춘 실증적 재정의에 가까움
- '관측이 겹치지만 action이 반대인' task 쌍이 forgetting의 대부분을 차지한다는 정량적 발견(LIBERO-Goal에서 상위 2개 task가 전체 negative backward transfer의 50% 이상 차지) 자체는 새로운 problem framing으로서 가치가 있으나, continual learning의 catastrophic forgetting 원인 규명이라는 문제 자체는 잘 알려진 영역이라 완전히 새로운 setting은 아님

**Benchmark results**

- LIBERO 4개 suite(Long/Goal/Object/Spatial, diffusion policy)에서 상위 10% Memory Anchor를 buffer sampling에서 제외하면 forgetting이 4.5배 이상 증가, 1%만 제외해도 일부 경우 forgetting 증가 관찰
- ANCHORER(buffer의 1%를 Memory Anchor로 채움)로 가장 상충하는 6개 task pair의 forgetting을 63% 감소(Fig. 6), LIBERO-Goal 전체 평균 NBT는 37% 감소
- π0.5 VLA(LIBERO-Goal)에서도 동일 경향 확인: RandER baseline NBT 0.12에서 Memory Anchor 10%를 제거하면 0.35로 2.9배 증가하고, ANCHORER 미적용 baseline NBT 0.45에서 Memory Anchor 20%를 추가하면 0.35로 22% 감소함 — VLA도 buffer가 상대적으로 작을 때는 forgetting에 취약함을 확인(대형 buffer에서는 거의 forgetting 없다는 선행연구와 다른 조건)
- real robot 2개 suite(OpenJar 3-task, SweaterFold 3-task bimanual folding, UMI+ARX arm)에서 ANCHORER가 RandER 대비 최종 성공률 1.7배 향상, 두 번째 task의 plasticity(학습 능력) 손실도 완화함
- baseline 비교(Table 2, LIBERO-Goal): ANCHORER NBT 0.11±0.01 vs MIR 0.14±0.01, GSS 0.17±0.03, action-disagreement 제거판 0.13±0.01, RandER 0.18±0.02 — Memory Anchor concentration과 NBT가 양의 상관관계임을 확인
- 한계: task sequence 길이가 3~10개로 짧고, 저자도 실제 장기 배포 상황을 대표하지 못할 수 있음을 명시. Memory Anchor 추출에 policy의 latent space와 과거 학습 데이터 전체 접근이 필요해 proprietary model에는 적용 어려움

**Top-tier conference 적합성 — 78/100 · 추천 venue: CoRL**

명확한 실증적 발견(소수 데이터가 forgetting을 좌우)에서 출발해 방법론(ANCHORER)과 real robot 검증(2개 bimanual task suite)까지 갖춘 완결된 연구로, diffusion policy와 VLA 양쪽에서 일관된 결과를 보여 empirical conviction이 강함. 다만 continual learning 자체는 CoRL/RSS 커뮤니티에서 상대적으로 틈새 주제이고 방법론이 기존 anchor/replay 아이디어의 확장이라 완전히 새로운 패러다임은 아니어서 oral보다는 강한 poster/spotlight급으로 판단됨.

**추천 이유 & 누리랩 연구와의 연결점**

- robot memory 및 continual learning 주제와 직접 연결: '관측 유사·action 상충' 조합을 latent overlap + action disagreement로 자동 탐지하는 방법은 failure detection/recovery에서도 '비슷해 보이지만 다른 대응이 필요한 상황'을 식별하는 데 응용 가능
- action disagreement 측정에 gaussian noise 후 policy denoise를 쓰는 기법은 diffusion/flow 기반 정책의 uncertainty 추정 아이디어로, test-time에서 policy가 헷갈리는 conflict state를 탐지하는 용도로 전용 가능
- homogeneous task(같은 환경·물체, 다른 전략)를 명시적으로 설계한 OpenJar/SweaterFold 벤치마크 구성 방식은 VLA의 test-time adaptation이나 world model 평가에서 hard negative task suite를 만들 때 참고할 만함

---

### 5. [76점] CLAP: Cross-Embodiment Video World Models are Zero-Shot Physical Simulators

- **분야**: World Model (Cross-Embodiment Video World Model, VLA) · **robotics relevance**: 9/10
- **arXiv**: [2608.27406](https://arxiv.org/abs/2608.27406) ([PDF](https://arxiv.org/pdf/2608.27406))
- **저자**: Kechen Liu, Ola Shorinwa
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 서로 다른 embodiment(로봇 여러 종과 인간)의 비디오를 함께 학습하기 위해 end-effector·language·latent action을 통일하고 latent action으로 무라벨 데이터에서 물리 prior를 먼저 학습한 뒤 EE action으로 정제하는 curriculum(CLAP)을 제안함. DROID 환경에서 SOTA 단일-embodiment 모델과 동등한 성능을 내면서, 실제 로봇에서 inference-time cross-policy planning으로 π0.5·MolmoAct-2의 성공률을 높이고 새로운 embodiment(bimanual, humanoid)로도 few-shot 적응이 가능함을 보였음.

**Core innovation & methodology**

- human+robot cross-embodiment video로 action-conditioned video world model을 학습하기 위해 end-effector pose, natural language instruction, learned latent action(VAE 기반 pseudo-action) 세 가지 action 표현을 통일된 형태로 사용함
- latent action은 라벨 없는 human video 활용을 가능케 하지만 실배치에 부적합하고 EE action은 실배치엔 적합하지만 라벨 데이터만 쓸 수 있는 trade-off를, curriculum(CLAP-CURR)으로 해결함: latent action으로 무라벨 video에서 물리 prior를 먼저 학습한 뒤 action head를 EE action용으로 교체해 fine-tuning함
- absolute EE action space를 로봇별 정규화 계수로 [-1,1]에 맞춰 cross-embodiment 학습을 단순화하는 반면, language action은 relative action으로 변환해 tokenization 정밀도 문제를 완화함. 이 둘은 서로 반대되는 최적 선택이며, 이를 실증적으로 규명함
- SVD 기반 video diffusion + history conditioning(과거 프레임·pose에 대한 causal cross-attention) + multi-view latent concat으로 architecture를 구성하고, inference-time cross-policy planning(여러 정책의 action proposal을 CLAP로 rollout 후 VLM reward로 선택)과 world-model 기반 RL fine-tuning까지 활용함

**Novelty vs. prior works**

- 기존 action-conditioned video world model(Ctrl-World, WorldGym 등)은 단일 embodiment에 국한되어 internet-scale human video를 활용하지 못했는데, CLAP는 cross-embodiment+cross-actor(human 포함) 학습을 action 표현 통일 문제로 정식화하고 curriculum으로 해결한 점이 본질적 차이임
- latent action 기반 cross-embodiment 학습(Genie, LAPA류) 자체는 선행 연구가 있으나 downstream alignment가 필요해 배포 성능이 떨어지는데, CLAP-CURR는 latent→EE curriculum으로 이 gap을 없애 무라벨 데이터 스케일링과 zero-shot 실배치를 동시에 달성한 점이 새로움
- 다만 video backbone은 2023년 SVD를 그대로 사용하고 새로운 diffusion architecture를 제안하지 않음(저자도 부록 FAQ에서 인정), architecture 측면의 novelty는 낮고 기여의 핵심은 cross-embodiment action harmonization recipe라는 학습 전략 차원임

**Benchmark results**

- DROID(가장 어려운 환경)에서 CLAP-LAM/CLAP-EE가 SOTA 단일-embodiment baseline Ctrl-World와 동등 수준 성능을 달성했다고 보고되나, 본문에서 그림(Fig.3)으로만 제시되고 구체적 수치표는 확인 불가함(본문에서 확인 불가)
- absolute vs relative action 비교: EE-action-conditioned 모델은 absolute action이 relative 대비 DROID LPIPS 기준 약 14.6% 우수(반직관적 결과)한 반면, language-action-conditioned 모델은 반대로 relative가 더 우수함
- zero-shot inference-time cross-policy planning(단일팔 Franka, DROID, 5개 pick-and-place/fold task, task당 20 trial): CLAP가 π0.5·MolmoAct-2의 base success rate를 모든 태스크에서 유지하거나 개선함(예: Fish 태스크는 MolmoAct-2·π0.5 각 50%→CLAP 75%, Red Lobster 태스크는 MolmoAct-2 20%/π0.5 90%→CLAP 95%)
- bimanual YAM(학습 범위 밖의 새 embodiment)에서도 zero-shot planning으로 MolmoAct-2 base 대비 성공률이 개선됨(Pick Carrot&Apple 90%→95%), 다만 task당 10 trial로 표본 크기가 작음
- few-shot adaptation은 pretrained embodiment(DROID·Bridge)에서 대부분 지표에서 SOTA baseline을 능가했고 novel embodiment(14-DoF bimanual YAM, 26-DoF G1 humanoid)에도 성공적으로 적응함
- RL 기반 policy fine-tuning 데모는 2개 task(Put Carrot in Bowl 80%→88%, Fold Towel 100%→100%)뿐으로 제한적이며, 저자 스스로 real-time(10Hz) 미달(추론 1.49~3.24초, GPU별)과 hallucination을 한계로 인정함. 학습 규모도 100K step·8GPU·2~3일로 internet-scale은 아직 아님

**Top-tier conference 적합성 — 78/100 · 추천 venue: CoRL / RSS**

cross-embodiment human+robot video world model이라는 새로운 문제 설정, curriculum 기반 action harmonization, real-robot(단일팔·bimanual) zero-shot planning과 RL fine-tuning까지 이어지는 실증적 증거가 강해 CoRL/RSS의 강력한 후보임. 다만 video backbone이 구형(SVD)이고 real-time이 아니며 real-robot trial 수(task당 10~20회)가 제한적이라 최신 backbone 대비 우위 여부와 통계적 신뢰도가 rejection risk로 지적될 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- world model로 여러 정책의 action proposal을 rollout해 VLM reward로 선택하는 inference-time cross-policy planning은 test-time optimization/failure detection 연구에 바로 적용 가능한 패턴이며, 정책이 실패할 후보를 world model이 사전에 걸러내는 방식임
- cross-embodiment latent action→EE action curriculum은 여러 embodiment(로봇팔, 휴머노이드) 간 robot memory·policy 전이 연구에 재사용 가능한 학습 레시피임
- video-world-model 기반 RL policy fine-tuning(실제 하드웨어 없이 imagination에서 정책 개선) 실험은 test-time training/counterfactual reasoning 연구 방향과 직접 연결되며, 실패 사례에 대한 counterfactual rollout 생성으로 확장할 수 있음

---

### 6. [74점] WALL-SS: Scaling Long-horizon World Models via Next-Scale Autoregression

- **분야**: World Model / Robot Manipulation · **robotics relevance**: 9/10
- **arXiv**: [2608.26239](https://arxiv.org/abs/2608.26239) ([PDF](https://arxiv.org/pdf/2608.26239))
- **저자**: Maeve Zhang, Rain Sun, Xiang Wang, Cyril Zhang, Shalfun Li, Meng Cao, Howard Lu, Ethan Chen 외 17명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 관측·action·task를 하나의 causal sequence로 묶어 coarse-to-fine next-scale autoregression으로 미래 영상을 생성하는 robot world model인 WALL-SS를 제안함. action-conditioned next-scale prediction, scale 단위로 압축되는 long-horizon memory, on-policy visual alignment(RL)를 결합해 action following과 분 단위 streaming rollout, sim-real policy 평가 일치도를 개선했다고 주장함.

**Core innovation & methodology**

- observation·action·task instruction을 시간순으로 interleave된 하나의 causal sequence로 표현하고, 각 미래 관측을 VAR(Visual AutoRegressive)류의 coarse-to-fine next-scale prediction으로 생성하는 formulation 제안(InfinityStar 초기화)
- action-conditioned next-scale prediction: scale마다 정렬된 action representation을 causal attention에 주입해 action-future coupling을 강화하고, 성공뿐 아니라 실패·suboptimal behavior도 충실히 시뮬레이션하도록 설계
- scale-compressed long-horizon memory: 최근 history는 fine scale로, 먼 history는 coarse scale로 압축해 bounded memory에서 streaming rollout을 지원하며, scale-wise dream forcing(corrupted/self-generated context로 학습)으로 rollout 시 오차 누적(exposure bias)을 완화
- on-policy alignment: next-scale visual token 생성을 확률적 policy로 보고, action-following reward와 long-term consistency reward로 GRPO 스타일 정책 최적화를 수행하되 KL regularization과 실제 trajectory replay로 pretrained visual prior를 보존
- 성공/실패 데이터 외에 policy-intervention·rollback-and-replay 데이터를 별도 구성해 물체 접촉 부근의 counterfactual 대조(같은 맥락에서 다른 action이 다른 물리적 결과로 이어짐)를 학습에 명시적으로 포함

**Novelty vs. prior works**

- 기존 action-conditioned world model(IRASim, UniSim 등)은 대부분 clip 단위 diffusion 생성인데, WALL-SS는 next-scale autoregression을 로봇 world model에 처음 적용했다고 주장하며 이는 VAR/Infinity/InfinityStar 계열 image/video 생성 기법을 robot world model로 확장한 것에 해당함 — 아키텍처 자체의 원류는 기존 연구이나 robot action-grounding과 결합한 조합은 새로움
- scale 축과 시간(cycle) 축을 함께 쓰는 memory 압축 설계는 기존 long-video streaming 기법(FramePack, LongLive, Echo-Forcing 등)의 아이디어를 next-scale hierarchy에 재사용한 것으로 원리적으로는 확장·재조합에 가까움
- 실패·intervention·rollback 데이터를 world model 학습에 명시적으로 포함시켜 '의도한 action ≠ 물리적 효과'를 학습시키는 데이터 설계는 실용적으로 중요하지만, counterfactual reasoning의 이론적 새 formulation이라기보다는 데이터 큐레이션 기여에 가까움

**Benchmark results**

- 본문 추출 텍스트에 실험 섹션(6장) 표와 구체 수치가 분량 제한으로 누락되어 있어 action following 개선폭, streaming rollout 길이(수치), sim-real 정책 순위 일치도 등 핵심 정량 결과는 본문에서 확인 불가
- abstract·conclusion에서 주장하는 내용(저자 주장이며 표/수치로 뒷받침되는지는 본문에서 확인 불가): action following·trajectory accuracy 개선
- 수 분 단위 streaming rollout을 bounded memory에서 지원, on-policy alignment가 action drift와 long-horizon inconsistency를 일관되게 감소시킴
- 외부 로봇 policy를 WALL-SS와 실제 로봇에 동일하게 배포했을 때 task outcome이 calibrate되고 policy-checkpoint 순위가 일치함
- 학습 데이터는 AgiBotWorld-Beta(1,003,672 trajectories, 987,508 captioned clips) 전체 + 자체 X2-Robot bimanual 데이터 + UMI(non-embodiment) 데이터 + intervention/failure-recovery 데이터로 대규모이며 real-robot(X2-Robot) 배포 평가를 포함한다고 서술됨
- 코드·프로젝트 페이지 공개(github.com/X-Square-Robot/wall-ss)

**Top-tier conference 적합성 — 65/100 · 추천 venue: CoRL**

action-grounded next-scale autoregression과 scale-compressed memory, on-policy visual alignment를 하나의 통일된 프레임워크로 묶은 시스템 기여는 CoRL/RSS 수준의 완결성이 있으나, 본문에서 확인 가능한 범위 내에서는 핵심 벤치마크 수치가 부재해 empirical conviction을 독립적으로 판단하기 어려움. 대규모 산업 로봇팀(X Square Robot)의 시스템 논문 성격이 강해 신규 problem formulation보다는 engineering integration 쪽에 가까워 oral보다는 poster 수준으로 평가함.

**추천 이유 & 누리랩 연구와의 연결점**

- scale-compressed long-horizon memory(최근은 fine, 과거는 coarse로 압축)는 robot memory 주제와 직접 연결되며, world model 기반 장기 실행에서 memory budget을 관리하는 설계로 참고할 만함
- intervention/rollback-and-replay 데이터로 '동일 맥락, 다른 action → 다른 물리적 결과'를 world model에 학습시키는 방식은 counterfactual reasoning 및 failure detection/recovery 연구에 바로 활용 가능한 데이터 구성 전략임
- on-policy alignment로 world model의 visual dynamics를 reward 기반으로 정렬하는 접근은 test-time optimization/inference-time planning 연구, 특히 world model을 정책 평가기로 쓰는 실험(sim-real calibration)에 참고할 가치가 있음

---

### 7. [73점] Arrive and Survive: Scaling Safe Goal-Conditioned Policy Learning from One-Bit Failure Signals

- **분야**: Reinforcement Learning / Safe Goal-Conditioned Control · **robotics relevance**: 7/10
- **arXiv**: [2608.26571](https://arxiv.org/abs/2608.26571) ([PDF](https://arxiv.org/pdf/2608.26571))
- **저자**: Guopeng Li, Yiyang Duan, Yiru Jiao, Chengcheng Xu
- **카테고리**: Machine Learning (cs.LG) · 신규 목록 게재: cs.LG
- **Comments**: 21 pages, 14 figures, 5 tables, Code: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 54점

> 💡 failure로 episode가 종료되는 상황에서 기존 contrastive RL(CRL)이 실패 이전 future goal만 정규화해서 쓰다 보니 짧게 살아남은 trajectory에 과도한 가중치가 실려 goal-reaching value를 체계적으로 과대추정한다는 것을 이론적으로 증명함. 이를 mass-weighted InfoNCE와 log-survival-mass correction 두 가지로 고쳐서 Safe-CRL을 제안하고, 12개 실패 취약 navigation/locomotion task에서 Scaling-CRL baseline 대비 생존시간과 goal-reaching 성능을 일관되게 크게 개선함.

**Core innovation & methodology**

- failure-terminated MDP에서 goal-reaching Q-function이 실제로는 failure-aware discounted future-goal occupancy(µ_f)와 같다는 것을 증명(Proposition 1)했고, 이 occupancy는 총 확률질량(survival mass Z(x))이 1보다 작은 sub-probability measure임을 규명함
- 기존 CRL은 trajectory마다 남은 pre-failure future occupancy를 단위 질량으로 재정규화한 뒤 평균을 내는데, 이 정규화가 짧은 trajectory(거의 바로 죽는 경우)에 과도한 가중치를 줘서 goal-reaching value에 non-negative overestimation bias를 만든다는 것을 수식으로 증명(Eq. 12)
- critic 쪽 보정: 각 trajectory row를 실현된 survival mass Ẑ_i로 가중하는 mass-weighted InfoNCE(MW-InfoNCE)로 trajectory-wise 정규화 왜곡을 상쇄(Proposition 2)
- actor 쪽 보정: 4-layer 경량 Z-encoder로 예측한 log-survival-mass 항을 contrastive score에 더해(f_corrected = f_θ + logZ_ψ) actor 최적화 시 누락된 survival mass를 복원(Corollary 1). 오직 failure termination의 1비트 신호(성공/실패)만 사용하고 별도 cost/annotation 불필요

**Novelty vs. prior works**

- 가장 가까운 prior work인 Scaling-CRL(Eysenbach et al. 계열 CRL의 depth-scaling 버전)이 failure termination 자체를 다루지 않았다는 점에서, failure-terminated MDP에 대한 CRL 이론을 완성했다는 것이 이 논문의 핵심 기여이며, 저자들이 명시적으로 밝히듯 이 overestimation bias는 선행연구에서 규명된 바 없음
- DDC, USHER 등 기존 CRL 개선 연구는 horizon dependence나 stochastic dynamics 하 hindsight bias를 다뤘고, SVL/SRL은 survival analysis로 time-to-goal을 명시적으로 모델링하는 다른 formulation인데, 본 논문은 CRL의 occupancy formulation을 그대로 유지하면서 정규화로 인한 survival mass 손실만 정확히 짚어낸다는 점에서 접근이 구분됨. 다만 아이디어의 본질은 'CRL의 정규화가 정보를 버린다'는 비교적 단순한 통찰이며, 수정 자체(가중치 곱하기, log 항 추가)는 minimal correction으로 구현이 단순함
- Constrained MDP 기반 safe RL(CPO, Lagrangian 등)과는 달리 명시적 cost signal 없이 termination의 1비트만으로 안전성을 학습한다는 setting 자체는 실용적이나, '1비트 신호로 안전 학습'이라는 문제의식 자체가 근본적으로 새로운 formulation은 아니고 CRL이라는 기존 프레임워크 내 이론적 공백을 메우는 성격이 강함

**Benchmark results**

- Brax(MJX backend) 기반 12개 실패 취약 navigation(Point/Car Goal, Safety-Gymnasium 기반)·locomotion(Ant/Humanoid, 마찰 감소·actuator gear 축소로 실패 유발) task에서 Safe-CRL이 time at goal을 12개 task 전부에서 Scaling-CRL 이상으로 개선, 9개에서 뚜렷한 향상: 예를 들어 Ant Goal 276.8→684.0 steps, Humanoid Goal 22.2→266.4 steps, Humanoid Big Pitfall 8.2→474.1 steps (5 random seed 평균)
- survival time도 12개 task 전부에서 개선. goal coverage는 7개 task에서 증가, 5개에서는 감소했으나 해당 task에서도 time at goal은 크게 증가해 '더 안전하게 오래 머무는' 방향으로 학습됨을 시사
- depth scaling 실험: 8-layer Safe-CRL이 64-layer Scaling-CRL을 모든 평가 task에서 능가, Humanoid U-Maze는 256-layer까지 성능 향상이 이어져 Scaling-CRL의 depth scalability를 그대로 보존
- ablation(Table 1, Brax 기준, 3 random seed 평균 — 본문 결과의 5 random seed와 조건이 달라 Scaling-CRL baseline 수치도 다름): logZ correction이 지배적 기여를 함. Humanoid Goal에서 Scaling-CRL baseline은 time at goal 13.8, logZ-only 적용 시 288.7로 개선. MW-InfoNCE 단독은 상대적으로 작은 개선(13.8→28.3)이며 둘을 합친 Safe-CRL이 최고(297.0)
- Z-encoder는 파라미터 4.2%, wall-clock 학습 시간 2.8% 증가로 오버헤드가 작음(64-layer 기준)
- 전부 시뮬레이션(Brax/MuJoCo) 환경이며 real-robot 검증은 없음. SAC-HER baseline도 부록에서 비교했으나 Safe-CRL이 크게 앞섬(구체 수치는 본문에서 확인 불가)

**Top-tier conference 적합성 — 75/100 · 추천 venue: ICLR**

failure-terminated MDP 하에서 CRL의 overestimation bias를 엄밀히 증명하고, 이론에서 직접 유도된 minimal correction(가중치·log항)으로 12개 task에서 depth scalability를 유지하며 일관된 개선을 보인 것은 technical/empirical conviction이 강함. 다만 시뮬레이션(Brax)에만 한정되어 real-robot 검증이 없고, safe RL 자체는 이미 성숙한 분야라 potential impact는 CRL 커뮤니티에 국한될 가능성이 있어 RSS/CoRL보다는 이론 중심의 ICLR/NeurIPS가 더 적합함.

**추천 이유 & 누리랩 연구와의 연결점**

- '실패는 1비트 신호만으로도 정보 손실 없이 correction 가능하다'는 이론적 틀은 failure detection/recovery 연구에서 실패 신호를 dense reward로 바꾸는 대신 정확히 처리하는 방법론으로 참고할 만함
- log-survival-mass를 policy score에 더해 위험을 회피하는 행동을 유도하는 방식은 VLA의 test-time optimization에서 '성공은 했지만 곧 실패할' unsustainable behavior(논문에서 제시한 overshoot·collision 사례)를 억제하는 reward shaping 아이디어로 응용 가능
- goal-conditioned contrastive RL 자체가 world model 없이 self-supervised로 policy를 스케일링하는 대안적 패러다임이라, 누리랩의 test-time optimization/RL 연구에서 world model 기반 imagination RL(예: 2608.26190 LWM)과 대비되는 baseline 혹은 결합 대상으로 검토 가치 있음

---

### 8. [71점] Generative Semantic Scene Completion

- **분야**: 3D Vision / Semantic Scene Completion · **robotics relevance**: 6/10
- **arXiv**: [2608.26737](https://arxiv.org/abs/2608.26737) ([PDF](https://arxiv.org/pdf/2608.26737))
- **저자**: Shi Chen, Weifeng Ge
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: 18 pages, 12 figures, 4 tables. Supplementary material (29 pages) is included as an ancillary file. Project page: this https URL - Code, models and the PS$^3$ dataset: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 56점

> 💡 outdoor LiDAR semantic scene completion을 discrete diffusion 하나로 데이터 생성(PS3)·scene completion(SGSC)·기존 예측 보정(S2D2) 세 역할을 다 수행하도록 재정의함. 특히 S2D2는 임의의 frozen SSC 모델의 예측을 재학습 없이 한 번의 Euler step으로 보정해 SemanticKITTI hidden test에서 causal single-sweep 최고 성능(38.8% mIoU)을 달성함.

**Core innovation & methodology**

- PS3: pyramid discrete diffusion으로 dense scene을 생성하고, rare-class object bank로 희귀 클래스를 이식한 뒤 HDL-64E ray-casting(HALO)으로 대응하는 sparse scan을 만들어 sparse-dense pair를 대량 합성함.
- SGSC: uniform noise에서 시작하는 multinomial discrete diffusion으로, BEV semantic map과 sparse 3D feature stream을 조건으로 scene을 처음부터 생성함.
- S2D2: diffusion의 noise source를 uniform prior 대신 frozen base 모델의 argmax 예측(structured source)으로 바꿔, source와 target을 잇는 straight interpolant를 학습해 배포 시 단 1 step만으로 보정을 완료함.
- 세 역할이 동일한 discrete-diffusion 틀(product simplex 위의 multinomial diffusion) 안에서 작동하며, S2D2는 별도 재학습이나 test-time adaptation 없이 어떤 frozen SSC base에도 적용 가능함.

**Novelty vs. prior works**

- SCPNet(supervision 강화), TALoS(test-time adaptation), PaSCo(instance supervision) 등 기존 SSC 개선 계열은 모두 base network 가중치 자체를 바꾸는데, S2D2는 base를 건드리지 않고 label space에서 후처리로 보정한다는 점이 본질적으로 다름.
- CarlaSC나 unconditional 3D diffusion 생성기와 달리 PS3는 SemanticKITTI 분포에 맞춰 희귀 클래스를 원천에서 증폭하고 대응 sparse scan까지 함께 만들어 long-tail 문제를 데이터 단계에서 해결함.
- SemCity(triplane 기반 continuous refinement), Octree Diffusion(하나의 latent로 생성·완성 다목적 수행) 등 인접 연구가 이미 존재해 '여러 역할을 하나의 생성 모델로' 자체는 완전한 최초는 아니며, 저자도 이를 명시함.

**Benchmark results**

- SemanticKITTI hidden test에서 SCPNet+S2D2(N=1, no TTA)가 38.8% mIoU로 SCPNet 발표치 36.7% 대비 +2.1pp, 이는 저자 주장상 causal·single-sweep·single-sample 조건에서 최고 기록(4-sweep 사용 SCPNet 47.5%나 TTA 사용 TALoS 37.9%는 별도 조건이라 직접 비교 대상 아님).
- 4-step + 8-view test-time augmentation 앙상블 시 39.2%까지 상승하나 이는 저자가 정의한 '제한 조건' 밖의 결과로 명시됨.
- SGSC 단독(from noise, T=100)은 val 30.5% mIoU로 PaSCo(30.1%, panoptic-mode evaluator라 직접 비교 어려움)와 비슷한 수준이며, S2D2 추가 시 32.8%로 개선됨.
- val split에서 SCPNet 자체 포팅 버전 36.17%가 S2D2로 38.54%까지 개선(+2.37pp), 재학습 없이 얻은 향상임.
- zero-shot cross-domain(SSCBench-KITTI360, SemanticPOSS) 결과와 thin-structure 개선 정도는 본문 발췌에서 구체 수치 확인 불가; 저자 스스로 thin structure는 거의 개선되지 않고 occlusion을 분리 검증한 실험이 없다고 한계를 명시함.

**Top-tier conference 적합성 — 74/100 · 추천 venue: CVPR**

이론적 근거(telescoping error bound, exact ELBO)와 강한 실증(SemanticKITTI hidden test SOTA)을 갖춰 top-tier 3D vision venue에 적합한 완성도임. 다만 outdoor driving 도메인에 특화돼 있고 논문 자체가 아직 review 중(preprint) 상태이며, thin structure·occlusion 등 핵심 실패 모드 개선이 제한적이라는 저자 자평이 rejection risk로 작용할 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- S2D2의 '어떤 frozen 모델이든 재학습 없이 1-step 보정' 아이디어는 로봇의 scene representation(occupancy, semantic map)을 test-time에 빠르게 보정하는 test-time optimization 연구에 응용 가능함.
- PS3의 sparse-dense pair 합성과 rare-class object bank는 로봇 환경에서 희귀하지만 안전에 중요한 물체(장애물, 사람) 인식 데이터를 늘리는 데 참고할 만함.
- object-centric 3DGS나 scene graph 연구에서 sparse 관측으로부터 dense semantic occupancy를 추정하는 이 논문의 conditioning 설계(BEV map + sparse feature stream)를 구조적으로 차용할 수 있음.

---

### 9. [69점] Decoupling Planning and Control for Instructable Agents

- **분야**: VLA / Hierarchical Embodied Agent · **robotics relevance**: 9/10
- **arXiv**: [2608.26788](https://arxiv.org/abs/2608.26788) ([PDF](https://arxiv.org/pdf/2608.26788))
- **저자**: Zineng Tang, Kelsey R. Allen, Sjoerd van Steenkiste, Ishita Dasgupta, Alane Suhr
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **Comments**: Published as a conference paper at COLM 2026. Project page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 75점

> 💡 VLM planner가 만든 sparse한 고수준 언어 지시를 world-model 기반 controller가 고빈도로 실행하도록 planning과 control을 완전히 분리한 Instruct-to-Act를 제안함. controller rollout을 VLM으로 사후 라벨링해 behavior cloning과 Dreamer식 world-model objective를 함께 학습시켜, 7개 embodied 환경(멀티에이전트 3개 포함)에서 controller-only 및 VLM 직접 action 생성 대비 일관되게 우수한 성능을 보임.

**Core innovation & methodology**

- planner(πp)는 관측→언어 지시, controller(πc)는 언어 지시+관측→저수준 action으로 역할을 분리하고, 두 프로세스를 비동기로 병렬 실행해 VLM의 느린 추론과 controller의 빠른 제어를 동시에 활용함.
- controller는 언어 조건부 DreamerV3 스타일 RSSM으로, replay segment를 VLM(GPT-4o)이 사후에 instruction으로 요약·라벨링한 뒤 behavior cloning loss를 world-model/reward objective에 추가해 학습함(전문가 시연 불필요).
- 멀티에이전트 환경에서는 동일한 controller 파라미터를 공유하되 각 agent가 독립된 latent state를 유지하고, planner끼리는 공유 chatroom을 통해 언어로만 협상·조율함(중앙 critic 없음).
- instruction-completion을 예측하는 별도 head를 둬 controller가 스스로 다음 지시가 필요한 시점을 판단하게 함.

**Novelty vs. prior works**

- HiRT 등 기존 slow/fast 분리 구조와 달리 planner-controller 인터페이스를 latent나 waypoint가 아닌 자연어로 둬서, controller 재학습 없이 서로 다른 VLM planner를 교체(plug-and-play) 가능하게 만든 점이 핵심 차별점임.
- RT-1/RT-2/OpenVLA 같은 단일 end-to-end VLA와 달리 저수준 action 공간에 맞춘 VLM fine-tuning이 필요 없고, 환경별로는 경량 controller(23 GPU-hour)만 학습하면 됨.
- 다만 slow/fast 분리 자체는 새로운 패러다임이 아니라고 저자도 명시하며, 평가가 Atari·Minecraft·Overcooked 등 game/simulation 환경에 국한돼 실제 로봇 조작 domain에서의 검증은 없음.

**Benchmark results**

- 7개 환경(Atari, Minecraft Diamond, Crafter, DMLab, Overcooked, Pico Park, MindCraft) 중 6개에서 강한 VLA/MARL baseline과 경쟁력 있는 성능을 보임.
- controller-only 및 GPT-4o 직접 action 생성 대비 7개 전체 task에서 개선(예: Atari 게임 점수 기준 Instruct-to-Act 891 vs controller-only 809 vs GPT-4o w/o controller 670).
- instruction-following accuracy 평균 92.8%(환경·planner별 172/200~194/200, 86~97%).
- annotation quality ablation: environment-derived symbolic label 11.4 vs VLM-generated 11.1 vs template 9.9 vs random string 8.3 vs no-instruction 8.2 (Minecraft Diamond) — 의미 있는 언어 신호 자체가 성능에 기여함을 보임.
- cross-planner transfer(Table 3)는 9.2~10.2로 안정적이나, 통합 controller를 여러 환경에 걸쳐 학습하면 Minecraft Diamond에서 약 10% 성능 하락(1.12점) — 환경 범용 controller는 아직 미해결.
- real-robot 실험은 없음(전부 game/simulation 환경), manipulation task로의 일반화는 본문에서 확인 불가.

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

COLM 2026(언어모델 중심 학회)에 게재됐으나 로봇 커뮤니티 관점에서는 CoRL/RSS가 더 적합함. planner-controller 분리와 멀티에이전트 언어 협업 실험은 설득력 있으나, 실로봇 검증 부재와 game-환경 중심 평가가 top-tier 로보틱스 학회에서는 약점으로 지적될 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- VLM planner + world-model controller의 언어 인터페이스 분리 구조는 VLA의 test-time inference 효율화(고빈도 제어 유지하며 저빈도 reasoning 삽입)에 응용 가능함.
- controller rollout을 VLM으로 사후 라벨링해 학습 신호를 만드는 방식은 로봇 실패 데이터에 사후적으로 language feedback을 주는 robot memory·failure recovery 파이프라인에 참고할 수 있음.
- 멀티에이전트 언어 협상 구조는 여러 로봇이 공유 world model을 두고 협업하는 시나리오로 확장할 여지가 있음.

---

### 10. [68점] Rapid On-Robot Learning for Dynamic Manipulation Skills: Robot Juggling

- **분야**: Manipulation / Rapid On-Robot Learning · **robotics relevance**: 9/10
- **arXiv**: [2608.26800](https://arxiv.org/abs/2608.26800) ([PDF](https://arxiv.org/pdf/2608.26800))
- **저자**: Taeyoon Lee, Chunpeng Wang, Christopher G. Atkeson, Alfred A. Rizzi, Nicolas Rojas
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 58점

> 💡 부정확한 sim2real prior 모델을 버리지 않고 국소 경험 기반 모델과 결합하는 regularized memory-based learning으로, 양팔 다지 로봇이 5분 이내 실제 하드웨어 학습만으로 저글링 패턴 5종(cascade, tennis, half-shower, shower, box)을 익힘. cascade·tennis·half-shower는 5사이클 연속 성공까지 안정적으로 도달했지만 shower·box는 부분적으로만 습득함. 연속 동작 사이 안전한 상태 전이만 허용하는 mutually reachable set을 함께 도입해, 관절·구동기 한계를 위반하지 않으면서 고성능 동적 동작을 반복 연습할 수 있게 함.

**Core innovation & methodology**

- 정확도가 낮아 단독으로는 저글링 한 사이클도 완수하지 못하는 prior 모델을 완전히 대체하지 않고, 경험이 풍부한 영역은 국소 선형회귀 모델로, 경험이 희소한 영역은 prior의 1차 미분 정보로 외삽하는 regularized memory-based learner를 사용함.
- throw/catch를 재사용 가능한 skill 단위로 분해하고, 각 skill의 명령을 직전 동작에서 관측된 상태에 조건화해 서로 다른 패턴 간에도 경험을 재사용함(open-loop 시퀀스가 아닌 closed-loop stateful policy).
- 연속된 throw-catch 전이가 관절·구동기 한계를 위반하지 않도록 사전 계산한 mutually reachable set(MRS)을 task-level planner의 hard constraint로 부과함.
- regularization 계수 γ로 prior 의존도와 실측 경험 반영 속도 사이 trade-off를 조절함(γ=0.001 사용).

**Novelty vs. prior works**

- 가장 근접한 선행연구인 Ploeger and Peters(2023)와 학습 원리(local model + prior의 1차 정보로 정규화)는 유사하나, 그쪽은 open-loop throw 시퀀스에 개별 보정을 episodic하게 적용하는 반면 본 논문은 상태 조건부 closed-loop skill로 실시간 학습을 진행하고 패턴 간 경험 재사용을 가능케 한다는 점이 차이임.
- Schaal and Atkeson(1994)의 memory-based 저글링 학습을 다지 손·양팔·여러 패턴으로 확장했지만, 학습 알고리즘 자체(국소 선형회귀 + prior 정규화)의 이론적 새로움은 제한적이며 novelty는 시스템 통합(skill 재사용 + MRS 안전 제약)에 있음.
- MRS는 juggling 도메인에 특화된 안전 제약 설계로, 일반적인 로봇 안전 이론(reachability 등)의 새로운 확장이라기보다 해당 task에 맞춘 구체적 구현임.

**Benchmark results**

- cascade 패턴은 7회 재시도(리셋), 총 약 53초의 물리적 상호작용만으로 5사이클 연속 성공에 최초 도달했고(수동 리셋 시간 제외), 5회 독립 시행 모두 8번째 시도 이내 재현에 성공함. 5개 패턴 전체로는 7~10회 재시도가 필요했다고 요약됨(논문 Table 1).
- tennis→half-shower→cascade 연속 전환은 평균 75초, 이전에 학습한 skill 재사용으로 cascade 습득이 단독 학습보다 빨라짐(2~3회 추가 시행으로 충분).
- shower·box 패턴은 각각 약 30초·60초 후 성능이 정체(plateau)되며 5사이클 목표를 모든 시행에서 안정적으로 달성하지는 못함 — 저자도 open-loop catch의 한계로 명시.
- MRS 없이 소급 검증(전체 7,578개 planner query) 시 99.1%가 MRS 밖에 위치하고 그중 89.0%가 실제로 unsafe(도달 불가 또는 다음 동작 실행 불가)로 확인돼, MRS 제약이 실질적으로 활성화되는 구간이 큼을 실증함.
- real-robot(AthenaZero) 단일 플랫폼에서만 검증됐고 sim 벤치마크나 다른 로봇으로의 일반화는 본문에서 확인 불가; box 패턴에서는 좌우 팔 간 학습 속도 비대칭(손가락 재접촉으로 인한 비선형성)이 관찰돼 저수준 전략 설계의 한계도 노출됨.

**Top-tier conference 적합성 — 66/100 · 추천 venue: RSS**

5분 이내 실로봇 학습이라는 인상적인 실증과 안전 제약(MRS)의 정량적 검증이 강점이나, 학습 알고리즘 자체의 이론적 기여는 Ploeger and Peters 대비 제한적이고 juggling이라는 특정 task에 최적화된 시스템 논문 성격이 강해 top-tier에서는 highlight보다 regular accept 수준으로 평가될 가능성이 높음.

**추천 이유 & 누리랩 연구와의 연결점**

- prior 모델이 부정확해도 국소 경험으로 보정하며 즉시 학습을 시작하는 방식은 test-time optimization 및 rapid adaptation 연구(예: sim2real gap이 큰 VLA의 real-time fine-tuning)에 바로 적용 가능한 아이디어임.
- skill을 상태 조건부로 분해해 여러 task 간 경험을 재사용하는 구조는 로봇 memory·skill chaining 연구와 접점이 있음.
- MRS처럼 task-specific 안전 제약을 사전 계산해 학습 중 hard constraint로 부과하는 설계는 dexterous manipulation의 test-time exploration을 안전하게 만드는 데 참고할 수 있음.

---

### 11. [68점] GameWAM: A World Action Model for Video Games

- **분야**: World-Action Model / Embodied AI (Video Games) · **robotics relevance**: 5/10
- **arXiv**: [2608.26200](https://arxiv.org/abs/2608.26200) ([PDF](https://arxiv.org/pdf/2608.26200))
- **저자**: Yuncheng Guo, Zhanqiu Zhang, Yiwen Guo, Weijia Li
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **Comments**: 44 pages, 23 figures, 7 tables
- **원문 검토**: PDF 전문 · 1차 스크리닝 55점

> 💡 미래 시각 관측과 실행 가능한 keyboard-mouse action을 동시에 생성하는 World-Action Model인 GameWAM을 Minecraft/ViZDoom native gameplay와 GUI control에 처음 적용함. block-cycle control(길게 예측하고 짧게 실행)과 계층적 memory로 fewer action으로 경쟁력 있는 task success를 달성함. 부수적으로 low-frequency action source가 카메라 동작을 편향시키는 LASI(Low-Frequency Action Source Imprinting)라는 실패 모드도 발견함.

**Core innovation & methodology**

- World Model(미래 예측)과 policy(action 생성)를 분리하지 않고 parallel Video-DiT/Action-DiT + block-causal attention + joint flow matching으로 동시에 생성하는 구조 제안, 첫 native closed-loop game WAM이라 주장
- gameplay(연속 카메라·이산 키)와 GUI(커서·클릭)가 물리적으로 같은 keyboard-mouse 좌표를 공유하지만 분포가 다르다는 문제를 timestep-wise router로 해결(모드별 예측·정규화 분리)
- block-cycle control: P step을 예측하되 E(<P) step만 실행하고 새 관측으로 replan하는 predict-long/execute-short 구조로 촘촘한 시각 샘플링과 긴 look-ahead를 동시에 확보
- cycle-local KV cache(within-cycle 세밀한 문맥) + 압축된 recent/long-term hierarchical visual history(cycle 간 지속 문맥)를 결합해 bounded memory 하에서 장기 상호작용 지원

**Novelty vs. prior works**

- 가장 가까운 prior work인 DreamZero(Ye et al., 2026)·Fast-WAM 등은 로봇 tabletop/실내 조작 위주였는데, 이를 rapid ego-motion·이질적 native control(gameplay+GUI)이 있는 game domain으로 처음 확장했다는 점이 novelty임. 다만 world-action model 자체의 formulation(parallel DiT + flow matching)은 Fast-WAM의 modality-decoupled mask를 그대로 채용한 것으로, 완전히 새로운 아키텍처라기보다 도메인 확장·엔지니어링 조합에 가까움
- block-cycle control(predict-long/execute-short)과 계층적 memory는 기존 long-video streaming 기법(FramePack, LongLive 등)의 아이디어를 WAM에 적용한 것으로 원리적 신규성은 제한적이나 실제 게임 환경에서의 효과는 실증됨
- LASI(Low-Frequency Action Source Imprinting) 발견은 이 논문에서 가장 독창적인 기여로, 생성형 action policy에서 sampled noise source의 저주파 성분이 반복 replanning을 통해 누적되어 카메라 방향 편향을 유발한다는 새로운 실패 모드를 통제 실험(DCT 분해, donor swap, zeroing)으로 인과적으로 규명함

**Benchmark results**

- MCU(800+ tasks) 벤치마크에서 GameWAM이 ASR Mini 50.7%, ASR All 46.6%로 비교 agent 중 최고(2위 OpenHA는 36.8%/31.5%, game-pretrained Game-TARS는 ASR All 42.5%), 특히 GUI task에서 step 수가 155로 다른 agent(291~406) 대비 크게 적어 interaction 효율이 높음
- ViZDoom 4개 map에서 Game-TARS 대비 일관되게 개선, o4-mini/GPT-5/Gemini-2.5-Pro/Claude-4-Sonnet 등 범용 멀티모달 에이전트와 경쟁적이거나 우위(구체 수치는 그래프로만 제시, 본문 텍스트에서 정확한 값 확인 불가)
- ablation(Table 2, MCU Mini): future-video supervision 제거 시 Avg 50.7→35.7로 가장 크게 저하, coarser temporal sampling도 36.7로 저하, unified action distribution(모드 미분리) 38.3, P=E(long-horizon 예측 제거) 41.3으로 각 설계 요소의 기여를 확인
- LASI 정량 증거: 고정 조건에서 yaw DCT0 저주파 성분의 Pearson r=0.890, donor swap 시 94.8% 추종률, zeroing 시 variance 99.25% 제거 — 인과관계를 뒷받침하는 통제 실험이지만 시뮬레이션 게임 환경에 국한됨
- 전부 시뮬레이션(Minecraft, ViZDoom) 환경 실험이며 real-robot 검증 없음. 코드·데이터·가중치 공개 예정이라고 명시

**Top-tier conference 적합성 — 60/100 · 추천 venue: ICLR**

게임 환경에서 첫 native closed-loop World-Action Model이라는 프레이밍과 LASI라는 흥미로운 실패 모드 발견이 강점이나, 핵심 아키텍처(Fast-WAM 스타일 마스킹, next-scale/block-cycle 유사 기법)는 기존 요소의 재조합이라 conceptual leap은 제한적임. 로봇 실환경 검증이 전혀 없어 CoRL/RSS보다는 게임/생성모델 중심의 ICLR·NeurIPS 계열이 더 적합하고, oral보다는 poster급으로 판단됨.

**추천 이유 & 누리랩 연구와의 연결점**

- LASI는 world model 기반 policy가 imagination 내에서 반복 rollout할 때 생기는 systematic bias 사례로, world model을 test-time planning이나 imagination-driven RL에 쓸 때(예: 2608.26190의 LWM) 반드시 점검해야 할 실패 모드로 참고할 만함
- gameplay/GUI처럼 이질적 action space를 모드별로 분리해 예측하는 per-step router 아이디어는 manipulation에서 서로 다른 action modality(예: navigation vs. grasping)를 하나의 VLA에서 다루는 문제에 적용 가능
- block-cycle(predict-long/execute-short) + hierarchical memory 구조는 robot memory·long-horizon planning 주제, 특히 world model 기반 test-time replanning에서 bounded memory로 장시간 rollout을 안정화하는 설계로 참고 가치 있음

---

### 12. [67점] Making Latent Evolution Explicit: Operator-Structured Transitions for World Action Models

- **분야**: World Model (World Action Model, Latent Dynamics) · **robotics relevance**: 8/10
- **arXiv**: [2608.27259](https://arxiv.org/abs/2608.27259) ([PDF](https://arxiv.org/pdf/2608.27259))
- **저자**: Xiaoxiao Lu, Yunlong Dong, Jiahao Shi, Ye Yuan
- **카테고리**: Machine Learning (cs.LG) · 신규 목록 게재: cs.LG
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 World Action Model(WAM)에서 latent transition을 Transformer로 암묵적으로 학습하는 대신 controlled Koopman generator 이론에 기반한 context-modulated operator로 명시적으로 구조화한 LEON을 제안함. VLA-JEPA에 적용 시 LIBERO success rate를 97.2%에서 99.05%로 높였으나, 정책 추론에 직접 개입하는 LaWAM에 적용했을 때는 개선이 아니라 기존 성능과 거의 동일한 수준(84.13% vs 84.50%)에 그쳤음.

**Core innovation & methodology**

- WAM에서 latent transition을 어떻게 구현할지('transition realization')를 predictive representation, prediction-policy coupling과 구별되는 별개의 설계 축으로 규정함
- LEON: 현재 latent를 learned observable space로 매핑(H=φ(X))하고 action/semantic context로 transition context ξ를 만든 뒤, low-rank shared operator basis(D+Σα_k(ξ)B_k)를 context로 modulate해 evolution을 표현하며 여기에 context-dependent additive forcing term b(ξ)를 병렬로 둠
- control-affine 시스템의 controlled Koopman generator가 L0+Σu_jLj로 분해되는 이론에 근거해 구조를 설계했고, Transformer 기반 predictor(암묵적 transition)와 달리 evolution law를 파라미터화 안에 명시적으로 표현함
- representation-mediated coupling(VLA-JEPA)과 policy-facing coupling(LaWAM) 두 종류의 WAM에서 기존 Transformer 기반 transition을 LEON으로 전면 교체해 검증함

**Novelty vs. prior works**

- transition realization을 predictive representation·prediction-policy coupling과 별개의 축으로 명시적으로 분리한 문제 설정 자체가 새로운 관점이며, 기존 WAM들은 이 구분 없이 Transformer를 기본값으로 사용해옴
- Koopman generator를 물리적 control 입력 대신 학습된 semantic/action context에 적용한 확장은 locally linear latent model·Deep Koopman 계열 연구의 자연스러운 연장으로, 완전히 새로운 이론이라기보다 기존 controlled Koopman 틀을 WAM 문맥에 이식한 것임
- 실험적으로는 두 WAM(VLA-JEPA, LaWAM 모두 2026년 arXiv 프리프린트로 아직 독립 검증이 부족한 매우 최신 baseline)의 transition 모듈만 교체하는 ablation적 성격이 강해, 새로운 WAM 제안이라기보다 기존 WAM에 꽂아 넣는 모듈 성격이 큼

**Benchmark results**

- VLA-JEPA + LEON: LIBERO 평균 success rate 97.2%→99.05%(+1.85pp), LIBERO-Plus aggregate 79.5%→80.6%(+1.1pp)이며 개선은 camera·lighting·background·noise·layout perturbation에 집중되고 robot·language perturbation에서는 이득이 뚜렷하지 않음
- LaWAM(policy-facing)+LEON: 4-task RoboTwin subset matched 비교에서 clean 85.00% vs baseline 84.50%, randomized 83.25% vs 84.50%로 aggregate 84.13% vs 84.50%로 사실상 동등하거나 미세하게 낮음, 저자도 '개선'이 아니라 'near-baseline 유지'로 표현함
- controlled dynamical system(damped spring, nonlinear pendulum, driven oscillator)에서 Koopman-구조 predictor가 Transformer 대비 학습 범위 밖(OOD) 진폭 외삽에서 크게 낮은 오차를 보였고, operator 경로 제거 시 OOD RMSE가 10.95배, forcing 경로 제거 시 3.03배 증가해 operator propagation이 지배적 기여임을 확인함
- 모든 실험이 시뮬레이션(LIBERO/LIBERO-Plus/RoboTwin) 기준이며 real-robot 실험은 없음, VLA-JEPA·LaWAM은 저자가 직접 학습한 모델이 아니라 기존 최근 공개 모델 위에 transition만 교체한 것이라 재현성·일반화 여부는 원본 모델 공개 상태에 의존함

**Top-tier conference 적합성 — 63/100 · 추천 venue: ICLR / NeurIPS**

transition realization을 독립적 설계 축으로 규정하고 controlled dynamical system 검증까지 곁들인 점은 이론적 정합성이 있어 ICLR/NeurIPS 관련 트랙에 적합함. 다만 policy-facing coupling(LaWAM)에서는 개선이 아니라 동등 수준에 그쳤고, 두 baseline이 모두 2026년 매우 최근 preprint라 독립적 재현 검증이 부족한 점이 rejection risk로 작용할 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- WAM의 latent transition을 Koopman operator로 구조화하는 아이디어는 world model·test-time optimization 연구에서 물리적으로 그럴듯한 latent dynamics를 강제하는 inductive bias로 바로 활용 가능함
- operator propagation과 additive forcing을 분리해 개입(intervention)하는 분석 방식은 world model 예측 오류가 어느 경로에서 오는지 진단하는 failure diagnosis 방법론으로 응용할 수 있음
- representation-mediated vs policy-facing coupling 구분은 world model prediction을 policy에 training-time signal로 결합할지 inference-time conditioning으로 결합할지 설계할 때 참고할 분류 체계임

---

### 13. [60점] SpatialCrafter: Single Image World Modeling with Generative 3D Proxies

- **분야**: World Model / 3D Scene Generation (Single-Image-to-Video) · **robotics relevance**: 6/10
- **arXiv**: [2608.27073](https://arxiv.org/abs/2608.27073) ([PDF](https://arxiv.org/pdf/2608.27073))
- **저자**: Chuan Fang, Lingteng Qiu, Yixun Liang, Rui Chen, Kunming Luo, Zhaohua Zheng, Tongyuan Bai, Feipeng Tian 외 3명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: 12 pages
- **원문 검토**: PDF 전문 · 1차 스크리닝 55점

> 💡 단일 이미지에서 3D-consistent한 explorable 비디오를 생성하기 위해 point cloud 등 불완전한 reconstructive proxy 대신 완전한 global 3D proxy를 한 번에 생성한 뒤 video diffusion으로 photorealistic하게 정제하는 SpatialCrafter를 제안함. SpatialGen-Video·RE10K·DL3DV 세 벤치마크에서 FVD·PSNR·RPE 기준 기존 SOTA(Voyager, GEN3C, ViewCrafter 등) 대비 우수한 성능을 보였고 115K 규모의 새 데이터셋도 함께 구축함(공개 예정, 본문 시점 미공개).

**Core innovation & methodology**

- 생성 과정을 global 3D proxy 생성과 appearance refinement 두 단계로 분리함, TRELLIS 기반 3D generator로 proxy를 만들고 video diffusion model(Wan2.1)을 'Generative Deferred Refiner'로 재해석함
- Point-anchored Sparse Structure(PaSS) Flow: 입력 뷰에서 얻은 sparse point cloud를 명시적 anchor로 조건화해 생성된 3D proxy가 입력 이미지와 spatial misalignment 없이 정렬되도록 함
- Parallel Geometry Injection: coarse RGB/depth 렌더링을 VAE로 각각 인코딩해 나란히 tile한 뒤 noisy latent와 채널 결합하고 LoRA만 학습해 pretrained VDM manifold를 훼손하지 않고 geometry를 주입함
- Proxy-Aware Corruption: 학습 시 coarse RGB-D 조건에 blur·block noise·depth erasure를 랜덤 적용해 proxy artifact에 대한 refiner의 overfitting을 방지함
- SpatialGen(합성 22K)·RealEstate10K·DL3DV(실측 65K+10K)를 결합해 115K scene 규모의 image-to-scene generation 전용 데이터셋을 최초로 구축함

**Novelty vs. prior works**

- 기존 reconstructive 3D proxy 방법(ViewCrafter, GEN3C, Voyager)은 입력 뷰에서만 point cloud를 재구성해 미관측 영역이 항상 비어있는 반면, SpatialCrafter는 비디오 생성 전에 완전한 global proxy를 one-shot으로 생성해 이 불완전성 문제를 구조적으로 없앰
- incremental proxy 갱신 방식(Voyager)은 proxy의 완전성이 VDM 자체의 공간 인식 능력에 의존하는 순환 구조를 갖는데, one-shot generative proxy는 이 의존성을 피함
- 다만 novelty는 TRELLIS(3D latent diffusion)와 Wan2.1(video diffusion)이라는 기존 강력한 사전학습 모델을 LoRA로 결합하는 엔지니어링적 성격이 강하고, 근본적으로 새로운 representation이나 학습 패러다임을 제시하는 것은 아님

**Benchmark results**

- SpatialGen-Video(합성 104 scene)에서 FVD 193.54, RPE 0.093으로 DFoT·GeometryForcing·GEN3C·Voyager·ViewCrafter 전부보다 우수함
- RealEstate10K(실측 100 scene)에서 FVD 148.71, PSNR 17.185로 전 지표 최고 성능을 기록함
- DL3DV(실측)에서도 FVD·PSNR·SSIM·LPIPS는 최고였으나 RPE(0.149)는 ViewCrafter(0.147)에 근소하게 뒤짐(2위)
- ablation: PaSS-Flow 제거 시 FVD가 193.54에서 472.07로 급격히 악화되어 spatial alignment 문제가 성능의 핵심 병목임을 확인함
- Voyager를 SpatialCrafter의 새 데이터셋으로 재학습한 Voyager†는 FVD/PSNR은 개선되지만 RPE·RVE(기하 일관성)는 여전히 크게 뒤처져, 성능 향상이 데이터셋이 아니라 one-shot generative proxy 구조 자체에서 온다는 것을 보여줌
- 모든 실험은 시뮬레이션/실측 비디오 데이터셋 기반이며 real-robot 실험은 없음, 코드·모델·데이터셋은 공개 예정('will be publicly released')이나 본문 시점에는 미공개

**Top-tier conference 적합성 — 66/100 · 추천 venue: SIGGRAPH Asia / CVPR**

6개 baseline과 3개 벤치마크에 걸친 견고한 정량 비교, 그리고 새 데이터셋 기여가 강점이며 그래픽스·비전 톱티어에 적합함. 다만 architecture는 TRELLIS·Wan2.1 조합의 엔지니어링 성격이 강해 근본적 새로움은 제한적이고, robot navigation이나 embodied AI로의 직접적인 실증(real-robot 실험)은 없음.

**추천 이유 & 누리랩 연구와의 연결점**

- reconstructive proxy와 generative proxy의 구분은 로봇이 탐색하며 3D memory를 구성하는 문제(robot memory, active perception/NBV)에도 적용 가능한 프레임임
- reconstructive proxy의 hallucination·drift 문제는 로봇 SLAM 스타일 incremental map 구축의 실패 모드와 유사해 failure detection/recovery 연구의 'proxy 완전성 신뢰도' 개념으로 확장할 수 있음
- PaSS의 point-anchored conditioning(입력 뷰와 생성 proxy의 정합)은 world model 기반 test-time policy evaluation이나 novel view synthesis 기반 planning에 재사용 가능함

---

### 14. [57점] Tensegrity Continuum Robots Enable Task-Adaptive Morphologies for Cooperative Behaviors

- **분야**: Robotics (Modular/Tensegrity Continuum Robot Hardware) · **robotics relevance**: 7/10
- **arXiv**: [2608.27221](https://arxiv.org/abs/2608.27221) ([PDF](https://arxiv.org/pdf/2608.27221))
- **저자**: Mahmud Hasan Saikot, Sydney Spiegel, Sudheera Akalanka Kariyawasam, Andrew Stefka, Josh Chrisler, Jianguo Zhao
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 22 pages, 6 figures, Accepted to Nature Machine Intelligence
- **원문 검토**: PDF 전문 · 1차 스크리닝 55점

> 💡 rigid modular robot의 재구성 가능성과 continuum robot의 신체 순응성(compliance)을 하나로 합친 tensegrity 기반 모듈 로봇 TeCoBot을 제안함. 여러 대의 TeCoBot이 claw 기반 도킹으로 chain·loop·branch 등 형태를 재구성해 협동 조작·이동·loco-manipulation을 실제 하드웨어로 시연했으나, 재구성은 대부분 사람의 teleoperation으로 이뤄지고 자동 도킹은 일부 사례로만 검증됨.

**Core innovation & methodology**

- icosahedral tensegrity module 여러 개를 수직으로 쌓아 만든 compliant continuum body와 양 끝단의 claw(파지+도킹 겸용)를 결합한 TeCoBot 설계, 3개 longitudinal cable로 omnidirectional bending과 axial collapse/extension을 cable-driven으로 제어함
- 각 모듈은 6개 rigid carbon fiber rod와 연속 TPU tendon으로 구성되며, 여러 모듈을 스택해도 peak actuation force는 거의 일정하게 유지되면서 변형량만 선형으로 증가함
- 다수 로봇이 claw-to-claw / claw-to-body docking으로 chain·loop·H자·branch 등 morphology를 self-reconfigure해 협동 조작(cooperative manipulation)과 협동 이동(cooperative locomotion)을 수행함(대부분 teleoperation 기반이며, 자동 도킹은 부록 수준의 일부 사례로만 검증됨)
- constant-curvature 기반 kinematic model로 cable displacement에서 backbone 변형을 예측하고 실측 대비 tip position error 0.8~3.0% 수준으로 검증함

**Novelty vs. prior works**

- 기존 rigid MRR은 global reconfiguration은 가능하나 body compliance가 없어 접촉이 많은 조작·지형 적응에 제한적이고, 기존 continuum robot은 compliance는 있으나 개별 로봇 간 도킹·재구성 기능이 없는데, TeCoBot은 두 특성을 동시에 갖춘 플랫폼으로 제시됨
- 기존 tensegrity robot은 대개 단일 tensegrity unit을 locomotion 목적으로만 구동했던 것과 달리, 여러 module을 스택해 연속체 body로 만들고 다중 로봇 협동까지 확장함
- mechanical/hardware 설계 기여가 중심이며 perception·policy learning 등 학습 기반 요소는 거의 없음, self-reconfiguration은 대부분 사람이 teleoperation하며 자율성은 부록 수준의 open/closed-loop docking 데모(fiducial marker 기반)로만 제한적으로 검증됨

**Benchmark results**

- 단일 모듈 axial collapse: tendon 2×2mm 기준 peak force 27.4±0.8N, 모듈 4개 스택 시 axial displacement 60mm→260mm로 선형 증가하나 peak collapsing force는 23~28N로 거의 일정함(모듈 수 증가에도 actuation force 불변)
- 야외 지형 8종에서 locomotion 속도 측정: rolling 모드가 smooth wood에서 최대 30mm/s, cost of transport 7.4로 대표적 modular robot 대비 낮은(효율적인) 값을 보임
- docking force: claw-to-claw symmetric 기준 latex sleeve 42.9±4.5N, silicone 38.9±2.6N
- kinematic model 검증: 4개 대표 cable actuation pattern에서 tip position error 1.9~6.4mm(backbone 길이의 0.8~3.0%)로 model과 실측이 일치함
- 모두 실제 하드웨어(real-world) 데모이며 시뮬레이션이 아니지만, baseline 로봇과의 직접적 정량 비교표는 제한적이고 대부분 정성적 태스크 데모(책상 정리, 캐비닛 정리 등)임, self-reconfiguration은 소수의 open/closed-loop docking 사례만 자동화되고 나머지는 teleoperation에 의존함

**Top-tier conference 적합성 — 52/100 · 추천 venue: Nature Machine Intelligence급 저널 / ICRA-IROS 하드웨어 트랙**

하드웨어 설계·특성화가 매우 꼼꼼하고(force curve, docking force, kinematic model validation) 실제 다중 로봇 협동 시연이 풍부해 로보틱스 하드웨어 저널/컨퍼런스에서 높은 평가를 받을 만함. 다만 학습·자율성 요소가 거의 없고 재구성이 대부분 teleoperation에 의존해 CS 로봇러닝 컨퍼런스(CoRL/RSS) 기준으로는 relevance가 낮음.

**추천 이유 & 누리랩 연구와의 연결점**

- self-reconfigurable claw docking 메커니즘은 로봇이 스스로 형태를 바꿔 대안 전략을 시도하는 test-time morphology adaptation 아이디어에 참고할 수 있음
- compliant tensegrity body가 sensing/control 부담을 신체 구조로 offload한다는 embodied intelligence 개념은 world model이나 policy가 명시적으로 처리하지 않아도 되는 정보를 체화 구조로 흡수한다는 점에서 representation 설계에 참고할 프레임임
- 학습 기반 perception/policy가 없어 VLA·world model·failure detection 연구에 직접 이식할 기술 요소는 제한적이며, 하드웨어 플랫폼 자체보다는 'compliance + reconfigurability' 설계 철학만 참고하는 정도로 활용 가능함

---

### 15. [46점] Diffusion Policies for Short-Horizon Planning in Robot Crowd Navigation

- **분야**: Navigation (Robot Crowd Navigation, RL) · **robotics relevance**: 7/10
- **arXiv**: [2608.27158](https://arxiv.org/abs/2608.27158) ([PDF](https://arxiv.org/pdf/2608.27158))
- **저자**: Wendong Li, Jochen Garcke
- **카테고리**: Machine Learning (cs.LG) · 신규 목록 게재: cs.LG
- **원문 검토**: PDF 전문 · 1차 스크리닝 55점

> 💡 crowd navigation에서 기존 RL 정책들이 매 스텝 단일 Gaussian action만 출력하는 한계를 diffusion policy 기반 5-step action chunk로 해결한 PDPO를 제안함. ORCA demonstration으로 behavioral cloning pretrain 후 PPO로 online fine-tuning함. 경계 제약이 없는 기존 CrowdNav++ 벤치마크의 평가 허점을 지적하며 Bounded CrowdNav를 새로 제안해 그 위에서 success rate를 74.5%에서 84.7%로 개선함.

**Core innovation & methodology**

- crowd observation을 latent로 encoding한 뒤 diffusion policy로 5-step short-horizon action chunk를 생성하고 receding-horizon 방식으로 첫 action만 실행함
- offline-to-online 학습: ORCA demonstration으로 BC pretrain 후, denoising process를 augmented MDP로 취급해 PPO로 online fine-tuning하는 DPPO(Ren et al. 2025) 프레임워크를 crowd navigation 도메인에 적용함
- CrowdNav++ 벤치마크에 명시적 경계 제약이 없어 로봇이 workspace 밖으로 나가 밀집 군중을 우회하는 evaluation artifact를 발견하고, 경계 이탈을 collision으로 처리하는 Bounded CrowdNav를 제안함
- observation encoder는 CrowdNav++/ASTG의 masked self-attention + attention pooling 구조를 그대로 채택함, 새로운 아키텍처는 아님

**Novelty vs. prior works**

- 방법론 핵심(diffusion policy + denoising-as-MDP PPO fine-tuning)은 Ren et al. 2025의 Diffusion Policy Policy Optimization을 crowd navigation이라는 새 도메인에 적용한 것으로, 알고리즘 자체의 novelty는 제한적임
- 가장 실질적인 기여는 evaluation artifact 발견과 Bounded CrowdNav benchmark 제안이며, 이는 방법론 novelty가 아니라 벤치마크 설계 기여임
- action chunking 아이디어 자체는 manipulation 분야(Diffusion Policy, Chi et al.)에서 이미 검증된 것을 dense multi-agent crowd 세팅으로 옮긴 것으로, crowd-specific한 구조적 변형은 관찰되지 않음

**Benchmark results**

- original CrowdNav++ benchmark: PDPO success rate 90.6% vs CrowdNav++ 87.0%(+3.6pp), action chunk 없는 ablation은 86.2%로 CrowdNav++와 비슷한 수준에 그침
- Bounded CrowdNav(제안 benchmark, 3 seed 평균): PDPO 84.7±1.4% vs CrowdNav++ 74.5±2.1%, action chunk 없는 ablation 73.7±0.7%.
- 본문은 CrowdNav++ 대비 개선폭을 +11.7pp로 서술하나 표의 두 수치(84.7-74.5)로 재계산하면 +10.2pp임 — 원문 표기 오류로 추정됨.
- ablation 대비 개선폭은 본문 서술 +11.0pp가 표 수치(84.7-73.7)와 정확히 일치함. action chunk 자체의 기여가 diffusion policy 도입 효과보다 크다는 저자 주장은 이 수치로 뒷받침됨
- boundary artifact 정량화: original benchmark 성공 궤적 중 out-of-bounds 비율이 CrowdNav++ 16.1%, ORCA 31.8%, PDPO(w/o chunk) 18.7%, PDPO 19.8%로 확인되어 평가 신뢰도 문제를 실증함
- 전부 CrowdNav++ 시뮬레이터(12×12m 워크스페이스, human 20명, human이 로봇에 반응하지 않는 단순화된 세팅) 내 실험이며 real-robot 실험은 없음
- PDPO는 1.049M trainable parameter로 CrowdNav++(2.503M)보다 적음에도 더 높은 성능을 보이나, iterative denoising으로 인한 inference overhead가 있고 저자도 실시간성 한계를 인정함

**Top-tier conference 적합성 — 44/100 · 추천 venue: RSS / ICRA**

crowd navigation이라는 확립된 RL 문제에 diffusion policy를 적용한 견실한 응용 논문으로 3개 지표·ablation·다중 seed 실험이 갖춰져 있으나 방법론적 참신성이 낮고 CrowdNav++ 단일 시뮬레이터에 한정됨. real-robot 검증 부재가 주요 rejection risk이며 CoRL/RSS oral보다는 ICRA/RSS 일반 세션 수준에 적합함.

**추천 이유 & 누리랩 연구와의 연결점**

- denoising step을 augmented MDP로 보고 PPO로 online fine-tuning하는 패턴은 test-time optimization/inference-time planning 연구에 재사용 가능한 프레임임
- action chunk 기반 receding-horizon 실행은 manipulation의 failure recovery에서 replanning 시점을 결정하는 문제에도 응용해볼 수 있음
- 경계 없는 시뮬레이션 환경에서 shortcut behavior가 발생한다는 발견은 누리랩이 다루는 시뮬레이션 벤치마크 신뢰성 점검(real-robot 검증 가능성 평가)에 참고할 사례임

---

## 오늘의 핵심 연구 트렌드 종합

- **World Action Model(WAM)로의 수렴** — policy 실행과 world simulation을 하나의 모델로 합치는 시도가 여러 편에서 동시에 나옴. [Riemann-1.0](https://arxiv.org/abs/2608.27033)은 action 예측 후 그 action을 조건으로 visual latent를 예측하는 causal 구조로 두 역할을 한 모델에 담았고, [WALL-SS](https://arxiv.org/abs/2608.26239)는 next-scale autoregression으로, [GameWAM](https://arxiv.org/abs/2608.26200)은 게임 도메인으로 같은 구조를 확장함.
- **Reconstruction 없는 latent dynamics 구조화** — 미래 관측을 pixel/feature 단위로 복원하는 대신 latent 공간의 관계 자체를 학습 목표로 삼는 흐름임. [LWM](https://arxiv.org/abs/2608.26190)은 reconstruction을 action-conditioned compatibility 예측으로 바꿨고, [LEON](https://arxiv.org/abs/2608.27259)은 latent transition을 Koopman operator(선형 연산자로 상태 전이를 표현하는 이론) 기반으로 명시적으로 구조화함.
- **실패·counterfactual을 학습 데이터에 명시적으로 주입** — 성공 시연만으로는 복구 능력이 안 생긴다는 문제의식이 공통으로 나타남. [FLARE](https://arxiv.org/abs/2608.26645)는 ID/OOD 실패를 나눠 각각 perturbation-bridging과 MLLM 기반 reset skill로 대응함. [WALL-SS](https://arxiv.org/abs/2608.26239)는 rollback-and-replay 데이터로, [LWM](https://arxiv.org/abs/2608.26190)은 다른 trajectory의 action을 negative로 가져와 같은 목적을 이룸.
- **Robot memory를 균일하지 않은 자원으로 재정의** — buffer나 history를 통째로 쓰는 대신 무엇을 남길지 선별하는 연구가 나옴. [Memory Anchors](https://arxiv.org/abs/2608.26545)는 replay buffer 중 forgetting 방지에 실제로 기여하는 데이터만 골라내고, [WALL-SS](https://arxiv.org/abs/2608.26239)와 [GameWAM](https://arxiv.org/abs/2608.26200)은 최근 history는 세밀하게, 과거는 압축해서 bounded memory로 장기 rollout을 지원함.
- **Human video를 로봇 action 학습에 정렬하는 curriculum** — internet-scale human video와 로봇 action 데이터 사이 격차를 단계적 학습으로 메움. [Riemann-1.0](https://arxiv.org/abs/2608.27033)은 인간 영상→UMI→로봇 순 3단계 pretraining을, [CLAP](https://arxiv.org/abs/2608.27406)은 latent action으로 무라벨 human video에서 물리 prior를 먼저 학습한 뒤 end-effector action으로 정제하는 curriculum을 씀.
- **평가 관행 자체에 대한 비판** — 벤치마크·정책의 숨은 실패 모드를 찾아내는 논문이 눈에 띔. diffusion policy 기반 crowd navigation 논문 [PDPO](https://arxiv.org/abs/2608.27158)는 CrowdNav++ 벤치마크에 경계 제약이 없어 로봇이 workspace 밖으로 나가 우회하는 evaluation artifact를 지적함. [GameWAM](https://arxiv.org/abs/2608.26200)은 world model이 imagination 내에서 반복 rollout할 때 저주파 noise가 누적돼 카메라 방향이 편향되는 LASI(Low-Frequency Action Source Imprinting) 실패 모드를 새로 규명함.

## 유망 연구 방향 및 프로젝트 제안

**Manipulation을 위한 reconstruction-free counterfactual world model**
- research question: pixel/feature reconstruction 없이 action-conditioned latent compatibility만으로 manipulation policy의 action selection이 가능한가.
- 접근·novelty: [LWM](https://arxiv.org/abs/2608.26190)의 compatibility discrimination과 [WALL-SS](https://arxiv.org/abs/2608.26239)의 intervention/rollback 데이터 구성을 결합해, contact 근처의 counterfactual 대조를 manipulation world model 학습에 명시적으로 넣는 formulation을 제안한다.
- 왜 지금·경쟁 prior works: 두 논문 모두 navigation·통제된 rollout 도메인에 머물러 있고 접촉이 많은 manipulation에서는 검증되지 않음. spatial proximity가 visual similarity와 상관관계 있다는 LWM의 가정이 occlusion 많은 manipulation에서 깨질 수 있어 이 gap이 research question이 됨.
- risk·target venue: contact-rich task에서 compatibility score의 신뢰도가 낮아질 위험 있음. CoRL/RSS 타겟.

**실패 신호 하나로 policy를 보정하는 test-time correction**
- research question: dense reward나 별도 cost 없이 성공/실패 1비트 신호만으로 policy의 위험 행동을 test time에 억제할 수 있는가.
- 접근·novelty: Arrive and Survive 논문이 제안한 Safe-CRL의 log-survival-mass correction을 VLA의 action score에 적용해, '성공은 했지만 곧 실패할' 행동을 test-time에 걸러내는 reward shaping으로 확장한다.
- 왜 지금·경쟁 prior works: Safe-CRL은 navigation/locomotion 12개 task에서만 검증됐고 VLA 결합은 시도되지 않음. Constrained MDP 계열(CPO 등)은 명시적 cost signal이 필요해 실패 라벨링 비용이 큼.
- risk·target venue: contrastive RL formulation이 discrete manipulation action space로 잘 옮겨지지 않을 위험 있음. ICRA/CoRL 타겟.

**Latent overlap 기반 실시간 실패 탐지**
- research question: '관측은 비슷한데 요구되는 action이 다른' 상황을 online에서 탐지해 즉시 개입할 수 있는가.
- 접근·novelty: [Memory Anchors](https://arxiv.org/abs/2608.26545)의 latent overlap + action disagreement 탐지를 continual learning의 buffer curation이 아니라 [FLARE](https://arxiv.org/abs/2608.26645)의 online monitor 자리에 넣어, 실패 직전 conflict state를 실시간으로 잡아내는 monitoring 모듈로 재구성한다.
- 왜 지금·경쟁 prior works: Memory Anchors는 offline buffer 구성에만 쓰였고, FLARE의 MLLM monitor는 별도 vision-language 모델에 의존해 무거움. policy 자체의 latent로 감지하면 추가 모델 없이 저비용 모니터링 가능.
- risk·target venue: action disagreement 임계값이 task마다 달라 일반화가 어려울 위험 있음. CoRL/ICRA 타겟.

**Cross-embodiment world model을 이용한 정책 후보 선별**
- research question: 여러 정책이 제안한 action 후보를 world model로 미리 굴려보고 실패할 후보를 사전에 걸러낼 수 있는가.
- 접근·novelty: [CLAP](https://arxiv.org/abs/2608.27406)의 inference-time cross-policy planning(world model rollout + VLM reward 선택)을 실 로봇의 failure detection 파이프라인 앞단에 배치해, 실행 전 counterfactual rollout으로 위험 action을 걸러내는 구조를 제안한다.
- 왜 지금·경쟁 prior works: CLAP는 이 구조를 π0.5·MolmoAct-2 두 정책에만 적용해 성능 향상을 보였지만 failure detection 목적으로 프레이밍하지 않음. video backbone이 2023년 SVD 그대로라 architecture 최신화 여지도 있음.
- risk·target venue: video world model rollout의 latency가 실시간 제어 주기를 넘어설 위험 있음. RSS/CoRL 타겟.

**희소 관측에서 dense semantic occupancy로: object-centric scene 표현**
- research question: sparse LiDAR/RGB-D 관측만으로 로봇이 온라인에서 dense semantic occupancy를 재학습 없이 빠르게 보정할 수 있는가.
- 접근·novelty: discrete diffusion 기반 1-step 보정 모델인 [S2D2](https://arxiv.org/abs/2608.26737)의 '어떤 frozen 모델이든 재학습 없이 1-step 보정' 아이디어를 object-centric 3DGS나 scene graph의 test-time 보정 단계로 가져와, 관측이 바뀔 때마다 재학습 없이 scene representation을 갱신한다.
- 왜 지금·경쟁 prior works: S2D2는 outdoor LiDAR SSC 도메인에 한정돼 있고 3DGS·scene graph로의 이전은 시도되지 않음. 기존 test-time adaptation(TALoS 등)은 gradient update가 필요해 느림.
- risk·target venue: outdoor LiDAR와 indoor manipulation scene의 도메인 차이가 커서 S2D2의 discrete diffusion 틀이 그대로 옮겨지지 않을 위험 있음. CVPR/ICRA 타겟.

## 오늘 반드시 읽어야 할 논문

- [Predicting Consequences and Reinforcing Navigation Policies with Latent World Models](https://arxiv.org/abs/2608.26190) — reconstruction 없이 counterfactual compatibility만으로 world model을 학습하는 formulation 자체가 test-time optimization 연구에 바로 참고할 만함.
- [Riemann-1.0: An Embodied World Action Model for Physical AI](https://arxiv.org/abs/2608.27033) — policy와 world simulator를 한 모델로 통합하고 200K+시간 이종 데이터를 progressive curriculum으로 붙인 규모가 오늘 Top 15 중 가장 큼.
- [FLARE: A Failure-Aware Framework for Autonomous Correction and Recovery](https://arxiv.org/abs/2608.26645) — ID/OOD 실패를 구분해 서로 다른 복구 전략을 쓰는 taxonomy가 failure detection/recovery 연구와 직접 맞닿음.
- [Memory Anchors for Continual Robot Learning](https://arxiv.org/abs/2608.26545) — replay buffer 데이터의 중요도가 균일하지 않다는 발견과 정량적 근거(forgetting의 절반이 상위 2개 task 쌍에서 발생)가 robot memory 연구에 바로 쓸 만함.
- [CLAP: Cross-Embodiment Video World Models are Zero-Shot Physical Simulators](https://arxiv.org/abs/2608.27406) — human video까지 포함한 cross-embodiment 학습과 inference-time cross-policy planning이 실 로봇에서 검증됨.
- [WALL-SS: Scaling Long-horizon World Models via Next-Scale Autoregression](https://arxiv.org/abs/2608.26239) — intervention/rollback 데이터로 counterfactual을 world model에 명시적으로 주입하는 데이터 설계가 참고할 가치 있음.
- [Arrive and Survive: Scaling Safe Goal-Conditioned Policy Learning from One-Bit Failure Signals](https://arxiv.org/abs/2608.26571) — 이 논문이 제안하는 방법인 Safe-CRL은 실패 termination만으로 goal-reaching value의 overestimation을 이론적으로 증명하고 고친 점이 탄탄함.
- [Decoupling Planning and Control for Instructable Agents](https://arxiv.org/abs/2608.26788) — VLM planner와 world-model controller를 자연어로만 인터페이스해 controller 재학습 없이 planner를 교체 가능하게 만든 구조가 VLA 효율화에 참고할 만함.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (419편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2608.26190'>Predicting Consequences and Reinforcing Navigation Policies with Latent World Models</a></td><td>78</td><td>9</td><td>World Model</td><td>로봇 navigation을 위한 latent world model로 observation 복원 대신 action-conditioned latent feature 호환성을 예측해 counterfactual 궤적으로 학습하고, unlabeled video로 policy를 supervise한 뒤 world model 내부에서 RL까지 수행한다. 여러 real-world navigation dataset에서 기존 world model·imitation learning baseline 대비 예측 정확도·정책 성능·실환경 navigation 모두에서 크게 앞섰다.</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2608.26788'>Decoupling Planning and Control for Instructable Agents</a></td><td>75</td><td>9</td><td>VLA</td><td>VLM planner가 생성한 sparse 고수준 언어 지시를 world-model controller가 고빈도로 실행하도록 분리한 Instruct-to-Act 구조로, controller rollout에 synthetic instruction을 relabel해 behavior cloning과 world-modeling objective를 함께 학습한다. 7개 embodied 환경(멀티에이전트 3개 포함)에서 controller-only 및 직접 VLM action-generation 대비 일관되게 우수했고 VLA·multi-agent RL baseline과도 경쟁력 있는 성능을 보였다.</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2608.27033'>Riemann-1.0: An Embodied World Action Model for Physical AI</a></td><td>72</td><td>10</td><td>World Model</td><td>로봇 정책 실행과 action-conditioned world simulation을 하나의 causal autoregressive 모델로 통합한 Riemann-1.0을 제안하고, 인간 영상부터 이종 로봇 시연까지 200K+ 시간을 progressive pretraining으로 통합해 RoboTwin2.0 94.3%, LIBERO 99.0%, 실로봇 장기과제 SR 85.0%로 기존 오픈소스 대비 15%p 앞서는 강력한 결과를 보인다.</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2608.26239'>WALL-SS: Scaling Long-horizon World Models via Next-Scale Autoregression</a></td><td>70</td><td>9</td><td>World Model</td><td>action-conditioned observation을 causal sequence로 표현해 scale-wise autoregression으로 장기 예측하는 WALL-SS를 제안하며, 액션 추종성과 분 단위 streaming rollout, on-policy alignment까지 다뤄 world model 우선주제에 정확히 부합한다.</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2608.26545'>Memory Anchors for Continual Robot Learning</a></td><td>62</td><td>9</td><td>Manipulation</td><td>replay buffer 내 소수의 Memory Anchor가 continual robot learning의 catastrophic forgetting 방지에 핵심적임을 밝히고, LIBERO와 real robot에서 forgetting을 63% 감소시켜 robot memory 우선주제에 부합하는 강한 실험적 증거를 제시한다.</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2608.26645'>FLARE: A Failure-Aware Framework for Autonomous Correction and Recovery in Visual-Language Robotic Manipulation</a></td><td>62</td><td>9</td><td>VLA</td><td>실패 없는 시연 데이터의 한계를 지적하고 Retry(교란 주입)와 Reset(MLLM 기반 OOD 탐지 후 skill 복구)을 결합해 VLA에 실패 복구 능력을 부여한 CVPR 2026 논문으로 failure detection·recovery 우선주제에 정확히 부합한다.</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2608.27406'>CLAP: Cross-Embodiment Video World Models are Zero-Shot Physical Simulators</a></td><td>62</td><td>9</td><td>World Model</td><td>end-effector pose·언어·latent action으로 이종 action space를 통일해 인간 및 로봇 영상 전반에서 action-conditioned video world model을 학습하는 CLAP를 제안하고, DROID 등에서 단일 embodiment 모델에 필적하거나 능가해 cross-embodiment world model 우선주제에 크게 부합한다.</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2608.27259'>Making Latent Evolution Explicit: Operator-Structured Transitions for World Action Models</a></td><td>62</td><td>8</td><td>World Model</td><td>Koopman generator 관점에서 world action model의 latent transition을 연산자 구조로 명시화한 LEON을 제안하며, transition 설계가 정책 성능에 미치는 영향을 두 WAM 프레임워크에서 검증해 world model 우선주제와 밀접하다.</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2608.26800'>Rapid On-Robot Learning for Dynamic Manipulation Skills: Robot Juggling</a></td><td>58</td><td>9</td><td>Manipulation</td><td>양팔 로봇이 5분 내 real robot 위에서 저글링 패턴 5종을 학습하도록, 국소 모델을 전역 사전모델과 결합한 regularized memory-based online learning과 안전한 상호 도달 집합을 제안해 dexterous manipulation·rapid on-robot learning 우선주제에 부합하는 인상적인 실증이다.</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2608.26737'>Generative Semantic Scene Completion</a></td><td>56</td><td>6</td><td>3D Vision</td><td>LiDAR semantic scene completion을 discrete diffusion 생성 문제로 재정의(GSSC)하고 SemanticKITTI에서 causal single-sweep 최고 성능(38.8% mIoU, +2.1pp)을 보여 새 problem formulation과 강한 실증을 겸비했다.</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2608.27158'>Diffusion Policies for Short-Horizon Planning in Robot Crowd Navigation</a></td><td>55</td><td>7</td><td>Navigation</td><td>군중 내비게이션에서 diffusion policy로 단기 action chunk를 생성하고 PPO로 온라인 미세조정하는 offline-to-online RL 프레임워크로 navigation 및 RL 우선주제와 관련이 크다.</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2608.27221'>Tensegrity Continuum Robots Enable Task-Adaptive Morphologies for Cooperative Behaviors</a></td><td>55</td><td>7</td><td>Robotics</td><td>tensegrity 유연 몸체와 claw 연결 메커니즘을 결합해 개별 로봇이 체인·루프·branch 형태로 자가 재구성하며 협력 조작·이동을 수행하는 modular reconfigurable robot으로, Nature Machine Intelligence 게재의 형태적 새로움을 갖췄다.</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2608.27073'>SpatialCrafter: Single Image World Modeling with Generative 3D Proxies</a></td><td>55</td><td>6</td><td>World Model</td><td>단일 이미지에서 global 3D proxy를 먼저 생성하고 VDM으로 외형을 정제하는 2단계 world modeling으로 장기 drift를 줄였으며 gaming·robotics·VR용 explorable scene 생성을 명시한다.</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2608.26200'>GameWAM: A World Action Model for Video Games</a></td><td>55</td><td>5</td><td>World Model</td><td>비디오 게임에서 미래 시각 관측과 keyboard-mouse 행동 궤적을 block-causal conditioning과 flow matching으로 동시 생성하는 World-Action Model(GameWAM)로, world model과 policy를 통합하는 패러다임은 로봇 world model 연구와 개념적으로 맞닿아 있으나 도메인은 게임 GUI 제어다.</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2608.26571'>Arrive and Survive: Scaling Safe Goal-Conditioned Policy Learning from One-Bit Failure Signals</a></td><td>54</td><td>7</td><td>RL</td><td>failure-terminated MDP에서 contrastive RL의 goal-reaching value 과대추정 편향을 이론적으로 규명하고 mass-weighted InfoNCE로 교정한 Safe-CRL로, 12개 실패빈발 로봇 navigation·locomotion task에서 생존율과 목표도달 성능을 모두 개선했다.</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2608.26821'>TemporalFlow-VLA: Learning Physically Grounded Execution History for Long-Horizon Robot Manipulation</a></td><td>52</td><td>8</td><td>VLA</td><td>로봇-표면 접촉의 물리적 temporal flow를 학습 전용 supervision으로 사용해 실행 이력을 압축 인코딩하는 TemporalFlow-VLA를 제안하고 LIBERO Long 96.6%, RoboTwin 최대 85.5%의 강한 long-horizon 성능을 보인다.</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2608.26314'>Dispersive Forward Tree Search for Optimal Control: Coverage, Complexity, and Computation</a></td><td>52</td><td>6</td><td>RL</td><td>미분평탄계 nonlinear 시스템에 대해 forward tree search의 유한 샘플 근사 최적성을 이론적으로 보장하는 DFT*를 제안하고 unicycle·trailer·quadrotor에서 실시간 kinodynamic planning으로 검증해 TAMP·long-horizon planning 우선주제와 관련이 크다.</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2608.26673'>PredVLA: A Sub-Million-Parameter Predictive-Coding Policy for Robot Manipulation</a></td><td>50</td><td>8</td><td>VLA</td><td>0.68M 파라미터의 predictive-coding 정책이 관측을 예측오차 기반 latent 추론으로만 반영하는 구조를 제안해 동일 파라미터 규모의 Transformer·LSTM 대비 3.7-7.4배 높은 LIBERO 성공률을 보여, VLA에 대한 근본적으로 다른 제어 구조 대안을 제시한다.</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2608.27371'>Embodied Scene Rearrangement Planning</a></td><td>50</td><td>8</td><td>Embodied AI</td><td>전역 상태 접근 없이 egocentric 관측과 top-down target layout만으로 가구를 재배치하는 새로운 task ESRP를 정의하고 5,400 scene pair 규모의 ESRP-Bench와 TAMP·VLM·IL·RL 네 baseline을 제시해 long-horizon planning·embodied spatial reasoning 우선주제에 부합한다.</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2608.27456'>UrbanGround: From Local Perception to Spatial Agency in a Real-Scale City</a></td><td>50</td><td>7</td><td>Navigation</td><td>홍콩 실제 규모 3D 도시 복제본에서 MLLM 에이전트의 1인칭 폐루프 탐색을 시험해 지역적 grounding이 장거리 목표지향 행동으로 이어지지 못함을 보인 embodied spatial reasoning/VLN 벤치마크다.</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2608.26583'>SOLO: Stable Omni-terrain Long-Horizon Perceptive Humanoid Locomotion</a></td><td>50</td><td>7</td><td>Embodied AI</td><td>Fourier 인코딩 쿼리 기반 지형 재구성과 미래 disagreement를 반영하는 TA-MSE distillation으로 장거리 perceptive locomotion의 오차 누적 문제를 다루며 1.5km 실외 zero-shot 배치로 실증했다.</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2608.26947'>4DSynth: Controllable Procedural World Synthesis for Dynamic Embodied Simulation</a></td><td>50</td><td>7</td><td>Embodied AI</td><td>자연어·블루프린트·사진으로부터 물리 상호작용 가능한 편집 가능 4D 환경을 생성하는 절차적 시스템과 이를 활용한 내비게이션 벤치마크로, VLM들이 대다수 과제에 실패함을 보여 embodied spatial reasoning 평가에 기여한다.</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2608.27395'>LeVJEPA: Efficient &amp; Scalable Video Pretraining without the Heuristics</a></td><td>50</td><td>5</td><td>World Model</td><td>asymmetry 없이 collapse-free objective로 학습하는 video JEPA로 V-JEPA2 대비 5.6~20.8배 적은 연산으로 대등하거나 우수한 성능을 보여 world model용 video representation learning에 실질적 기여를 한다.</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2608.26496'>RTNav: Towards Real-Time Zero-Shot Object Navigation</a></td><td>48</td><td>7</td><td>Navigation</td><td>실시간 실행 조건에서 zero-shot object navigation의 추론 지연을 명시적 설계 요소로 다룬 RTNav를 제안하고 HM3D 계열에서 성공률을 최대 11%p 개선해 navigation·VLN 우선주제에 부합한다.</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2608.26622'>Relaxation-Aware Multimodal Sensing of Soft Gripper Driven by Structure-Perception-Learning</a></td><td>48</td><td>7</td><td>Manipulation</td><td>점탄성 응력 이완으로 인한 grasping force 감쇠를 온도-결합 모델과 physics-informed 학습으로 보상하는 구조-지각-학습 통합 프레임워크로, 280초 파지 유지에서 오차를 기존 대비 80-95% 줄여 tactile perception 우선주제와 관련이 크다.</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2608.27079'>GRAFT: Grounded and Efficient Online Reinforcement Adaptation for Fine-Grained Robot Manipulation</a></td><td>48</td><td>7</td><td>VLA</td><td>region-level supervision으로 시점별 시각 anchor를 학습해 VLA의 온라인 강화학습 적응을 grounding하는 GRAFT를 제안하고 생체의료 조작 과제에서 동일 예산 대비 성공률을 25%p 높였다.</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2608.26868'>CGS-SLAM: Collaborative Gaussian Splatting based SLAM for Multi-Agent Reconstruction</a></td><td>48</td><td>6</td><td>3D Vision</td><td>RGB+관성만으로 다중 에이전트 3DGS SLAM을 GNSS-denied 환경에서 구현해 collaborative mapping·scene reconstruction에 직접 닿아있다.</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2608.27365'>KnockGS:interaction-Grounded Calibrationof Physical Gaussian Representations</a></td><td>48</td><td>6</td><td>World Model</td><td>관측된 힘-반응 동역학으로부터 물리 3DGS의 탄성·밀도 파라미터를 역추정하는 calibration 신호로 활용해 physics-integrated 표현과 sim-to-real 물성 추정에 새로운 방향을 제시한다.</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2608.27328'>R2M-Bench: Evaluating Revisit Memory via Relative Consistency in Interactive Video World Models</a></td><td>48</td><td>5</td><td>World Model</td><td>동일 rollout 내 상대 비교로 video world model의 revisit memory를 절대 유사도와 분리해 측정하는 새 평가 paradigm으로 robot memory 평가에 직접 참고할 만하다.</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2608.27226'>DINOcular: Self-Supervised Visuospatial Representations</a></td><td>46</td><td>6</td><td>Embodied AI</td><td>RGB-D를 활용한 self-supervised visuospatial representation 학습으로 embodied 시스템의 depth 센싱을 명시적으로 겨냥해 3D-aware 표현학습에 직접 기여한다.</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2608.27345'>PAWBench: How Far Are We from Probabilistically Aligned World Modeling?</a></td><td>46</td><td>5</td><td>World Model</td><td>video world model을 물리 동역학의 확률적 sampler로 보고 분포 수준 정합성을 측정하는 PAWBench/PAWEval을 제안해 world model 평가에 새로운 기준을 제시한다.</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2608.27367'>Successive Capacity Growth: Task-Complexity-Driven Width and Depth Expansion for Vision Transformer Encoders in JEPA World Models</a></td><td>46</td><td>5</td><td>World Model</td><td>JEPA world model의 ViT encoder를 task 복잡도에 따라 test-and-verify로 점진 확장하는 방법으로 다중물체 동역학·2D navigation task에서 fixed large model 대비 20~23% 개선을 보였다.</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2608.26238'>Procedura: Agentic 3D Modeling with Procedural Control</a></td><td>46</td><td>3</td><td>3D Vision</td><td>LLM 에이전트가 part 단위 procedural CAD 프로그램을 작성하는 새 paradigm이지만 로봇 조작과의 직접 연결은 약하다.</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2608.26766'>MeshPriorDiT: Hierarchical Modeling for Action-Conditioned Cloth Dynamics</a></td><td>45</td><td>7</td><td>Manipulation</td><td>메시 GNN이 예측한 구조적 prior에 conditional flow matching 기반 residual DiT를 결합해 옷감 동역학의 국소-광역 상호작용을 함께 포착하며, GNN-only 대비 Global MSE를 43% 줄여 deformable manipulation의 world model적 접근을 제시한다.</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2608.27384'>FlashVLA: Streaming Action Decoding for Fast and Asynchronous VLA Inference</a></td><td>45</td><td>7</td><td>VLA</td><td>chunk-wise causal attention으로 다른 노이즈 수준의 action chunk를 스트리밍 디코딩해 flow-matching VLA의 비동기 실행 불안정을 해결한 FlashVLA로, 실로봇에서 30Hz 제어 주파수를 달성했다.</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2608.26659'>Simple Actors and Deep Critics for Scalable Reinforcement Learning</a></td><td>45</td><td>4</td><td>RL</td><td>offline RL에서 critic을 deepening하는 방법을 제안하나 추론 효율 개선이 핵심이라 로봇 학습과의 직접 연결은 제한적이다.</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2608.26859'>A Geometry-Driven, Framework-Agnostic Optimization for Object Pose Estimation</a></td><td>44</td><td>6</td><td>Manipulation</td><td>principal axes 정렬로 대칭 물체의 회전 라벨 모호성을 데이터 단에서 해소하는 framework-agnostic 기법으로 조작에 핵심적인 object pose estimation 전반에 plug-and-play로 적용 가능하다.</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2608.27039'>Multi-Person Human Motion Forecasting in Complex Scenes</a></td><td>44</td><td>5</td><td>Embodied AI</td><td>object-conditioned social diffusion으로 복잡한 장면의 다인 모션·human-object 상호작용을 예측해 HiK·HOI-M3에서 경로오차를 31~33% 줄였으며 social navigation·HRI 예측에 직접 활용 가능하다.</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2608.26883'>Active Surface-Driven Reconfigurable Gripper: Robust Grasping and Sequential Manipulation of Thin Objects</a></td><td>42</td><td>7</td><td>Manipulation</td><td>능동 표면과 underactuated compliance를 결합해 얇은 물체(책 등)의 in-hand repositioning과 grasp를 복잡한 제어 없이 달성한 RSS 2026 그리퍼 설계 연구로 기구-학습 결합 성격의 실용적 기여다.</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2608.27407'>Reconstructing Humans and Objects in Interaction using Large Reconstruction Models</a></td><td>42</td><td>5</td><td>3D Vision</td><td>Large Reconstruction Model의 mesh를 human/object로 분해해 3D human-object interaction을 복원하는 방법으로 AR/VR·robotics·embodied AI 응용을 명시한다.</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2608.26872'>Self-OPD: On-Policy Distillation for Flow Matching Models without Teacher</a></td><td>42</td><td>4</td><td>RL</td><td>teacher 없이 self-exploration으로 flow matching 모델을 on-policy distillation하는 새 학습 paradigm으로, flow matching 기반 로봇 정책 학습에도 적용 가능성이 있다.</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2608.26116'>The Artificial Experimentalist: Discovery and Control of Self-Organizing Phenomena with Autotelic Reinforcement Learning</a></td><td>42</td><td>3</td><td>RL</td><td>Lenia cellular automaton에서 autotelic RL로 self-organizing soliton을 발견·제어하는 closed-loop 프레임워크(CARL)로, goal-conditioned policy의 zero-shot 일반화를 보였으나 로봇 도메인과는 거리가 있다.</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2608.26187'>When the Canonical Completion Is Wrong: Formalizing and Measuring the Jump in Large Language Models</a></td><td>42</td><td>1</td><td>NLP</td><td>Kan extension 기반으로 LLM의 abductive jump를 형식화하고 측정한 이론적 기여로 novelty는 있으나 로봇 문제와는 거리가 있다.</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2608.26273'>Constraint-Aware Physics-Informed Neural Networks for Static Shape Estimation of Co-Manipulative Continuum Robots</a></td><td>40</td><td>6</td><td>Manipulation</td><td>공동 조작 continuum robot의 정적 형상 추정에 물리 제약을 결합한 PINN으로, 폐쇄 체인 기하 제약 하에서 강한 수치 개선(구성 오차 67% 이상 감소)을 real robot에서 검증했으나 특정 하드웨어에 국한된 응용 성격이 강하다.</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2608.26578'>TrapVLA: Trapping Vision-Language-Action Models in Configured Failure Modes</a></td><td>40</td><td>6</td><td>VLA</td><td>단순 실패 유도가 아니라 지정된 실패 양상을 트리거로 유도하는 새로운 backdoor 공격 task를 VLA에 대해 정의하고 TrapVLA로 구현해 문제 설정 자체는 새로우나 보안 공격 연구로 로봇 학습 발전과는 결이 다르다.</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2608.26644'>Real-time Unsupervised Object Discovery from Asynchronous Event Streams</a></td><td>40</td><td>4</td><td>Embodied AI</td><td>이벤트 카메라 기반 training-free 실시간 물체 발견은 latency-critical active perception에 실질적으로 쓰일 수 있다.</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2608.26656'>CoGeo-GS: Concept-Driven and Geometry-Aware Multi-Object Removal in 3D Scenes</a></td><td>40</td><td>4</td><td>3D Vision</td><td>3DGS에서 concept 태그 기반 다중 물체 제거는 object-centric 3D representation·scene editing에 닿아있다.</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2608.27072'>Emotional Preferences as Goal-Priority Regulation</a></td><td>40</td><td>4</td><td>RL</td><td>고차원 목표가 하위 목표 우선순위를 상태 의존적으로 조정하는 감정적 선호 개념을 multi-objective RL로 구현한 연구로 로봇 행동 우선순위 조정에 아이디어를 제공할 수 있다.</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2608.26794'>Ring Forcing: Towards Precise Long-Term Memory for Autoregressive Video Diffusion</a></td><td>40</td><td>3</td><td>World Model</td><td>ring 구조 학습과 sparse RoPE로 자기회귀 비디오 확산의 분 단위 object permanence를 개선한 방법으로 world model의 장기 메모리 설계와 개념적으로 닿아있다.</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2608.27448'>TTPO: Test-Time Policy Optimization</a></td><td>40</td><td>3</td><td>RL</td><td>다수결 pseudo-label의 비대칭적 신뢰도를 이용해 label 없이 test-time policy optimization을 수행하는 TTPO로, test-time optimization이라는 우선 주제와 직접 맞닿아 있으나 수학 추론 도메인에 한정된다.</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2608.26701'>Accelerating Scientific Research with Gemini in the Real-World</a></td><td>40</td><td>3</td><td>Multimodal</td><td>Gemini 기반 multi-agent Co-Scientist를 실제 CVD 반응기·생물학 실험과 연결해 closed-loop로 가설 생성부터 실험 실행까지 자동화했고 재료과학에서 새로운 2D 물질 합성 경로를 제안했다. 물리적 실험 장비와의 closed-loop 자동화는 로봇 자율 실험과 유사하지만 로봇 조작 자체는 다루지 않는다.</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2608.26671'>RECAP-Forcing: Retaining Content Appearances for Long Video Generation</a></td><td>40</td><td>2</td><td>Video</td><td>novelty 기준으로 KV cache를 유지하는 training-free 장기 비디오 메모리 구조를 제안했으나 robot memory와는 응용 맥락이 다르다.</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2608.27225'>STEP: State-Aware Task Estimation and Planning with Multi-Modal LLMs for Human-Robot Collaboration</a></td><td>38</td><td>6</td><td>Embodied AI</td><td>MM-LLM이 시스템 상태와 상태 전이를 명시적으로 추정하도록 하여 hallucinated action을 줄이는 STEP을 제안하고 조립 과제에서 실행가능성을 32.8%p 개선했으나 시뮬레이션 평가에 그친다.</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2608.26481'>Shared Actors Need Not Share Critics: Effects of Value Mismatch in Parallel Reinforcement Learning</a></td><td>38</td><td>4</td><td>RL</td><td>병렬 환경에서 critic 공유가 유발하는 value mismatch를 이론적으로 규명하고 환경 index 조건화만으로 CartPole·MuJoCo·Procgen에서 성능을 개선해 domain randomization 기반 로봇 RL에 직접 적용 가능하다.</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2608.26684'>Reason in the Words You Speak: Idiolectal Paraphrasing Off-Policy Traces for Reasoning Distillation in VideoLLMs</a></td><td>38</td><td>2</td><td>RL</td><td>off-policy teacher trace를 student의 idiolect로 재작성해 GRPO의 gradient clipping 문제를 완화하는 distillation 기법으로 RL 학습 paradigm에 기여하나 대상은 video reasoning이다.</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2608.26902'>Tether the Subject, Release the Scene: Query-Aware Memory Routing for Long-Horizon Autoregressive Video Generation</a></td><td>38</td><td>2</td><td>Video</td><td>subject/scene query를 분리한 training-free memory routing으로 장기 비디오 생성의 scene under-progression 문제를 짚었으나 robot memory와는 응용이 다르다.</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2608.26142'>Position Is All You Need: A Free Lunch Token Compression Strategy for MLLM-based Referring Expression Segmentation</a></td><td>38</td><td>2</td><td>Multimodal</td><td>MLLM 기반 referring expression segmentation에서 위치 정보만으로 토큰을 압축하는 training-free 방법으로 효율화 위주 기여다.</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2608.26147'>CARE: Causally-Aligned Reasoning Exploration for Medical Large Language Models</a></td><td>38</td><td>2</td><td>RL</td><td>의료 LLM 추론에서 causal sufficiency와 proximal learnability로 experience curation을 하는 RL 프레임워크(CARE)로 outcome reward의 credit assignment 문제를 다루지만 도메인이 의료에 국한된다.</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2608.26887'>Planting a Latent Variable in Natural-Looking Text: a More Realistic Test of Belief States in LLMs and Their Link to Concept Geometry</a></td><td>38</td><td>2</td><td>NLP</td><td>인위적으로 심은 잠재변수를 소형 트랜스포머가 belief state로 추적하고 그 기하가 SAE concept geometry와 연결됨을 보인 해석가능성 연구로, world model의 내재 표현 형성 원리에 시사점이 있다.</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2608.27115'>Cross-Lingual Alignment Without Joint Training: Do Monolingual Language Models Converge on Universal Representations?</a></td><td>38</td><td>1</td><td>NLP</td><td>공동학습 없이도 단일언어 모델들이 정렬 가능한 표상 기하로 수렴하며, Procrustes 회전으로 기능적 내용까지 전이됨을 인과적으로 보인 표상학습 연구다.</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2608.26676'>FOCUS &amp; RePAIR: Mitigating Text Degeneration via Token-Level Guidance for Pruned Large Language Models</a></td><td>38</td><td>0</td><td>NLP</td><td>가지치기된 LLM의 반복 루프를 loop entry/persistence로 분해하고 FOCUS·RePAIR로 완화한 ICML spotlight급 분석이다.</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2608.26504'>NeuDonatello: Uncertainty-Aware Framework for Accurate Neural SDF Learning</a></td><td>36</td><td>3</td><td>3D Vision</td><td>SDF 불확실성을 모델링해 표면 재구성 정확도를 높인 방법으로 active perception/NBV에 응용 가능성이 있다.</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2608.26589'>DPA-I2P: Depth-Guided Projective Alignment for Image-to-Point-Cloud Registration in Autonomous Driving</a></td><td>36</td><td>3</td><td>3D Vision</td><td>depth-guided image-to-pointcloud registration으로 KITTI에서 RTE/RRE를 크게 낮췄으나 자율주행 localization에 특화된 engineering이다.</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2608.27417'>Retrieval Heads Meet Vision: Uncovering How VLMs Locate and Extract Visual Information</a></td><td>36</td><td>3</td><td>Multimodal</td><td>VLM 내부의 visual retrieval head를 인과적으로 규명한 해석가능성 연구로 VLA backbone의 visual grounding 메커니즘 이해에 참고가 된다.</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2608.26495'>Video-FLAIR: Not Whether to Reason, But How</a></td><td>36</td><td>2</td><td>Multimodal</td><td>RL로 perceptual/compositional/deliberative reasoning 모드를 적응적으로 고르는 아이디어는 test-time reasoning 제어와 맞닿아 있으나 대상이 video QA에 한정된다.</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2608.27455'>CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes</a></td><td>36</td><td>2</td><td>RL</td><td>약한 모델의 실패 패턴을 critique로 재활용해 반복 생성 없이 추론 성능을 높이는 CritICL로 inference-time weak-to-strong generalization을 다룬다.</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2608.26386'>Co-Evolving Structured Knowledge and Reasoning in Language Models</a></td><td>36</td><td>1</td><td>NLP</td><td>구조화 지식베이스 구축과 그 위에서의 추론을 QA 보상으로 공진화시키는 KBevo 프레임워크로 지식-추론 결합에 새로운 설정을 제시한다.</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2608.27088'>Active sensing to characterize the heterogeneity of plant stress</a></td><td>35</td><td>6</td><td>Robotics</td><td>3D 식물 재구성과 기하 분석으로 측정 지점을 선정하고 충돌 없는 궤적을 생성하는 능동 형광 센싱 로봇 플랫폼으로 active perception·NBV 우선주제와 관련이 있다.</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2608.26383'>Cross-Platform Benchmark of Neural 3D Reconstruction for Autonomous Laboratory Robots</a></td><td>35</td><td>5</td><td>3D Vision</td><td>실험실 로봇을 위한 NeRF·3DGS·SAM3D의 컴퓨팅 플랫폼별 지연시간·품질 벤치마크로, object-centric 3D representation 우선주제와 관련은 있으나 새 방법론 제안 없이 벤치마킹에 그친다.</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2608.26198'>Agentic AI for operating scientific instruments for nanoscale characterization</a></td><td>35</td><td>3</td><td>Embodied AI</td><td>AFM(원자간력현미경) 운용을 위한 MCP 기반 tool-augmented LLM agent 3종(Messenger/Pilot/Doctor)으로 이미지 품질 평가·파라미터 조정·아티팩트 진단을 수행하며 실기기 실험에서 전문가와 동등한 성능을 보였다. 실제 하드웨어를 다루는 active perception형 자동화라는 점이 로봇 자율 조작과 방법론적으로 맞닿아 있다.</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2608.26683'>SIGMA: Structured Noise-Effect-Aware Grouped Multi-Agent Aggregation</a></td><td>35</td><td>3</td><td>RL</td><td>노이즈가 있는 관측 하에서 협력 구조를 활용해 robust하게 학습하는 계층적 cooperative MARL 프레임워크(SIGMA)로 StarCraft II에서 검증했다. MARL 방법론은 RL 우선주제와 맞닿아 있으나 로봇 실험은 없다.</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2608.26193'>AffectOmni: RL-Verifiable People-Centric Grounded Affective Reasoning for Social and Art-Related Scenes</a></td><td>35</td><td>2</td><td>Multimodal</td><td>GRPO로 사람 중심 evidence에 집중하도록 학습한 affective reasoning MLLM(AffectOmni)으로 People Focus/Temporal Order reward와 SAM3 기반 pixel-level grounding이 특징이나 감성 인식 시나리오이며 robotics 관련성은 낮다.</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2608.27044'>Omni-Interactive Universal Embedder</a></td><td>35</td><td>2</td><td>Multimodal</td><td>텍스트·비디오·오디오를 아우르는 통합 임베딩 공간과 omni-interactive query(텍스트/시각 영역/오디오 span)를 지원하는 embedder(OmniUE)로 여러 벤치마크에서 baseline 대비 큰 개선을 보였다. representation learning 우선주제와 관련 있으나 로봇 응용은 다루지 않는다.</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2608.26292'>On Scope Classification and Current Knowledge-Editing Benchmarks: A Negative Result, with INLAY as a Gradient-Free Case Study</a></td><td>35</td><td>1</td><td>NLP</td><td>knowledge editing 벤치마크가 scope 결정 능력을 측정할 수 없다는 negative result를 gradient-free editor로 규명한 방법론적 기여다.</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2608.26720'>Parameter Efficient Continual Learning for Sparse Event-Based Transformers</a></td><td>34</td><td>4</td><td>CV</td><td>spiking vision transformer용 파라미터 효율적 continual learning으로 로봇/엣지 배포를 명시하나 효율화 중심의 incremental 기여다.</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2608.26722'>UniGeo: A Multi-modal Large Language Model for Text-Guided Cross-View Geo-Localization</a></td><td>34</td><td>3</td><td>Navigation</td><td>텍스트 기반 드론 cross-view geo-localization MLLM으로 GeoText-1652에서 R@10 13.59pt 개선했으며 navigation·spatial grounding과 일부 연결된다.</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2608.26951'>Per-View Gaussian Predictions Enable Training-Free Distractor Filtering in Feed-Forward 3DGS</a></td><td>34</td><td>3</td><td>3D Vision</td><td>feed-forward 3DGS에서 per-view 예측 구조를 활용한 training-free distractor 필터링으로 casual capture 3D 재구성 품질을 개선한다.</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2608.27214'>CODE: Cross-Modal Calibration and Dynamic Suppression for Open World Object Detection</a></td><td>34</td><td>3</td><td>CV</td><td>cross-modal calibration과 dynamic suppression으로 open-world 미지 물체 탐지 성능을 개선해 embodied 환경의 open-set 인지와 연결된다.</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2608.26469'>Active Curriculum Refinement for Reinforcement Learning</a></td><td>34</td><td>3</td><td>RL</td><td>curriculum DAG 위에서 active learning으로 학습 경로를 재배분하는 PATH는 skill chaining·long-horizon curriculum 설계에 원리적으로 적용 가능하다.</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2608.26355'>Finding the Right Evidence: Factor-Guided Coarse-to-Fine Reasoning for Long Videos</a></td><td>34</td><td>2</td><td>Video</td><td>long-video QA에서 option-discriminative evidence 회수라는 문제를 짚었지만 로봇 학습과는 거리가 있다.</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2608.26993'>Aphanta: Diagnosing Task-Aligned Image-Edited Intermediates for Multimodal Reasoning</a></td><td>34</td><td>2</td><td>Multimodal</td><td>이미지 편집을 MLLM reasoning의 시각적 작업공간으로 진단하는 프레임워크로, 시각적 중간 상태 활용이라는 아이디어가 test-time reasoning과 개념적으로 맞닿아 있으나 로봇 응용은 아니다.</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2608.26155'>VFA: Empowering Multilingual MLLMs via Vision-Free Adaptation</a></td><td>34</td><td>1</td><td>Multimodal</td><td>task vector 합성으로 다국어 능력과 vision alignment를 분리 확장하는 VFA 방법으로 데이터 효율성은 있으나 응용적 기여다.</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2608.26329'>Neuro-symbolic PRM: Enhancing Scientific Reasoning via Structured Traces and Symbolic Verification</a></td><td>34</td><td>1</td><td>RL</td><td>symbolic validity와 semantic groundedness를 분리해 PRM을 학습하는 neuro-symbolic 프레임워크로 STEM 도메인에 한정된다.</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2608.27176'>When Text Misleads: Inconsistent-Aware Reasoning for Audio-Grounded Dialogue</a></td><td>34</td><td>1</td><td>Multimodal</td><td>transcript와 음향 단서가 충돌할 때 text-only LLM은 90%에서 33-48%로 급락함을 보이고 Audio Twin으로 grounding을 개선한 벤치마크+방법이다.</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2608.27265'>SCIT: Testing Causal Cache Carriers in Latent Chain-of-Thought Models</a></td><td>34</td><td>1</td><td>NLP</td><td>latent chain-of-thought 모델에서 counterfactual computation이 value-cache suffix를 통해 전달됨을 causal interchange test로 규명한 해석가능성 연구다.</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2608.26449'>Vowel Signs Are Not Letters: A Pre-tokenization Ceiling on Multilingual Tokenizer Fertility</a></td><td>34</td><td>0</td><td>NLP</td><td>abugida 문자에서 BPE pre-tokenizer가 모음 기호마다 단어를 쪼개는 구조적 한계를 formal lower bound로 밝히고 널리 배포된 문제임을 census로 입증했다.</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2608.27309'>Difference-in-Differences on a Censored Rating Scale Can Manufacture an Effect: Evidence from a Pre-Registered LLM-Judge Audit</a></td><td>34</td><td>0</td><td>NLP</td><td>censored rating scale에서 difference-in-differences가 허구의 효과를 만들어낼 수 있음을 사전등록 감사로 입증한 방법론적 경고다.</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2608.27402'>How Language Models Organize and Structure Moral Knowledge</a></td><td>34</td><td>0</td><td>NLP</td><td>도덕 기반들이 서로 겹치지 않는 독립 차원으로 표상되며 도덕 딜레마는 그 구성요소의 조합+갈등 구조로 표현됨을 보인 표상 기하 연구다.</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2608.26932'>Contact-Aided Factor-Graph Localization for Underwater Sampling</a></td><td>32</td><td>5</td><td>Navigation</td><td>흡착 조작기 접촉 이벤트를 고신뢰 factor로 사용해 특징이 부족한 해저 환경에서 표류를 줄이는 factor-graph localization으로 embodied physical interaction을 위치추정 primitive로 활용한 점이 흥미롭다.</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2608.26752'>Glass Surface Detection Grounded in 3D Visual Geometry</a></td><td>32</td><td>3</td><td>3D Vision</td><td>3D geometry 기반 유리 표면 탐지는 navigation 안전(투명 장애물 인지)에 실질적으로 연결될 수 있다.</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2608.27233'>HALO: A Heterogeneity-Aware Language-Aligned IMU Foundation Model for Open-Set Human Activity Recognition</a></td><td>32</td><td>3</td><td>Embodied AI</td><td>IMU 기반 open-set 행동 인식 파운데이션 모델로 embodied sensing과 관련 있으나 로봇 조작·정책 학습과는 직접 연결이 약하다.</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2608.27065'>Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models</a></td><td>32</td><td>2</td><td>Video</td><td>evidence frame에 조건화된 self-teacher로 Video-LLM을 distillation하는 post-training 기법이나 로봇 응용과는 거리가 있다.</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2608.27168'>Magpie: Real-Time World Renderer for Interactive Games</a></td><td>32</td><td>2</td><td>World Model</td><td>게임플레이 로직과 시각 생성을 분리한 실시간 world renderer로 재현 가능한 상태 관리를 유지하며, 시뮬레이션 환경 구축 아이디어에 참고할 만하다.</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2608.27420'>Boosting LLM Exploration via Weak-Model Guidance in RLVR</a></td><td>32</td><td>2</td><td>RL</td><td>약한 모델이 만든 prefix로 RLVR의 entropy collapse를 완화해 탐색 범위(pass@k)를 넓히는 방법으로 RL 탐색 일반론에 기여한다.</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2608.26317'>Modality Maturity Index: A benchmark for assessing multimodal capabilities of omni models</a></td><td>32</td><td>1</td><td>Multimodal</td><td>omni 모델의 멀티모달 능력을 재는 벤치마크로 robotics 관련성이 낮다.</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2608.26563'>SPT: Skills as Pre-Training Data for Agentic Language Models</a></td><td>32</td><td>1</td><td>NLP</td><td>공개 skill 패키지를 mid-training 데이터로 삼아 tool-using 에이전트 성능을 높이는 SPT로 skill 재사용을 학습 데이터화하는 새 관점을 제시한다.</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2608.26596'>Not Just Reason, Not Just Scan: Reinforcement Learning for Proactive Scientific Error Verification over Academic Paper</a></td><td>32</td><td>1</td><td>RL</td><td>사전 지정 없이 논문의 오류를 능동 탐색·검증하는 Reason-Verify-Scan RL 프레임워크(VERA-RL)로 세밀한 보상 설계를 도입했다.</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2608.27409'>Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms</a></td><td>32</td><td>1</td><td>RL</td><td>Merge/Mix RL/MOPD 세 fusion paradigm을 공통 실험조건에서 비교해 실무 가이드라인을 도출한 체계적 연구다.</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2608.26319'>When Is Noise Response Universal? Tokenization as the Hidden Variable in Language Models</a></td><td>32</td><td>0</td><td>NLP</td><td>노이즈에 대한 모델 강건성 격차를 tokenization 재분절로 설명한 메커니즘적 발견이다.</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2608.26372'>Knowledge-Verified Emergent Deception in LLM Agents Under Conflicting Incentives</a></td><td>32</td><td>0</td><td>NLP</td><td>이해충돌 상황에서 LLM 에이전트의 emergent deception을 지식 검증 기반으로 측정한 안전성 벤치마크다.</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2608.27128'>TwinKV: A Composable Repair Pass for KV Cache Eviction via Pairwise Key Redundancy</a></td><td>32</td><td>0</td><td>NLP</td><td>attention 크기가 토큰의 인과적 기여와 무관함을 controlled leave-one-out으로 보이고, 중복 키 탐지로 KV cache eviction을 보정하는 TwinKV를 제안했다.</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2608.27397'>Making Clinical Language Models Auditable: Concept-Guided Fine-Tuning for Robust Prediction</a></td><td>32</td><td>0</td><td>NLP</td><td>SAE로 임상 텍스트 모델의 artifact latent를 검출·억제해 감사 가능한 예측을 만드는 CAST 방법이다.</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2608.26888'>Beyond Shallow-Water Photorealism: Physically and Sensor-Grounded Simulation for Deep-Sea Robotics</a></td><td>30</td><td>5</td><td>Robotics</td><td>심해 물리·센서 사실성을 강화한 Stonefish 시뮬레이터 확장으로 학습 기반 underwater autonomy를 위한 도구적 기여이며 새로운 학습 방법론은 아니다.</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2608.27085'>Pass the Bucket: Efficient, Robust, Local Load Balancing for Teams of Heterogeneous Robots</a></td><td>30</td><td>5</td><td>Robotics</td><td>이종 로봇팀의 분산 국소 load balancing을 위한 bucket brigade 안정화 메커니즘으로 이론·실증을 갖췄으나 학습 기반 요소는 없다.</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2608.26182'>Why did My Robot Just Change Personality? Prompting Guidelines for a Grounded Robot Persona in LLM-Based HRI</a></td><td>30</td><td>5</td><td>Embodied AI</td><td>LLM 기반 social robot persona 설계를 위한 8개 요소 prompting template과 가이드라인을 HRI 전문가 설문을 바탕으로 제안했으나, 기술적 기여보다는 실무 가이드에 가까워 novelty가 제한적이다.</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2608.27282'>TADP: Task-Aware Deformable Prediction for Single-Stage 3D Object Detection</a></td><td>30</td><td>4</td><td>3D Vision</td><td>단일 스테이지 3D 물체 탐지에서 task별 deformable prediction head로 KITTI car mAP 80.91%를 달성했으나 기존 backbone 위 plug-and-play 개선에 가깝다.</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2608.27181'>SSMB: Self-Supervised Local Feature Detection under Motion Blur</a></td><td>30</td><td>3</td><td>3D Vision</td><td>모션 블러에 강인한 deblur-free self-supervised keypoint detector로 visual localization·pose estimation의 안정성을 높인다.</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2608.26490'>Bayesian methods and Markov chain Monte Carlo algorithms for curve reconstruction and point cloud data analysis</a></td><td>30</td><td>3</td><td>3D Vision</td><td>point cloud 곡선 재구성에 불확실성 정량화를 도입한 베이지안 MCMC 프레임워크로 LiDAR 데이터에서 검증했으며 active perception의 불확실성 추정에 참고할 만하다.</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2608.26860'>Reinforcement Learning-Based Control of CAV Platoon Joining Maneuvers in Mixed Traffic</a></td><td>30</td><td>3</td><td>RL</td><td>자율주행 차량 플래투닝 합류 제어에 DRL을 적용한 응용 연구로 방법론적 새로움은 제한적이다.</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2608.26306'>Approved Too Late: Verdict Staleness in LLM-Guarded Self-Adaptive Systems</a></td><td>30</td><td>3</td><td>LG 등</td><td>LLM guardrail 승인이 실행 시점에 stale해지는 TOCTOU 위험을 다루며 Freshness-Bounded Shield로 approval expiry율을 최대 24.7%에서 1.8%로 낮췄다. 실시간 안전 판단의 신선도 문제는 로봇 failure detection과 유사하나 self-adaptive software 도메인이다.</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2608.26983'>GraphMemix: Query-Aware Evidence Forests for Long-Term Multimodal Agent Memory</a></td><td>30</td><td>3</td><td>Multimodal</td><td>질의에 따라 evidence forest를 구성하는 combinatorial-optimization 기반 장기 multimodal agent memory 프레임워크(GraphMemix)로 정확도-lifecycle cost의 새로운 Pareto frontier를 제시했다. robot memory 주제와 개념적으로 맞닿아 있으나 로봇 적용은 다루지 않는다.</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2608.26624'>Text-to-seed generation: Training-free open-vocabulary seeded semantic segmentation via re-purposing diffusion as text-guided seed generator</a></td><td>30</td><td>2</td><td>CV</td><td>diffusion attention을 seed point로 재활용하는 training-free open-vocab segmentation으로 semantic mapping에 부분적으로 연결된다.</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2608.26960'>Geo-LoRA: Geometry-Aware Subspace Evolution for Low-Rank Adaptation in Continual Learning</a></td><td>30</td><td>2</td><td>RL</td><td>Grassmann manifold 기반으로 LoRA subspace 전이를 기하학적으로 규제하는 continual learning 기법으로 로봇의 lifelong learning에 원리적으로 적용 가능하다.</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2608.26748'>Self-Augmented Diffusion Guidance for Physics-Informed Generation</a></td><td>30</td><td>2</td><td>Video</td><td>물리 법칙을 반영한 diffusion guidance 기법으로 world model 생성에 원리적으로 적용 가능하나 유체역학 시뮬레이션 중심이다.</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2608.27219'>BALMS: Benchmarking Agentic LLMs for Longitudinal Mental Health Sensing</a></td><td>30</td><td>2</td><td>Multimodal</td><td>웨어러블 장기 신호에 대해 LLM 에이전트가 근거를 붙여 추론하는지 재는 첫 벤치마크(BALMS)로, 장기 시계열 센서 추론이라는 점에서 embodied sensing과 맥락이 닿는다.</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2608.26263'>SKILL.state: Scalable Long-Horizon Agent Skills</a></td><td>30</td><td>2</td><td>LG 등</td><td>append-only 대화 이력 대신 명시적 mutable execution state를 사용하는 long-horizon agent runtime(SKILL.state)으로, skill chaining·long-horizon planning과 개념적으로 유사하나 소프트웨어 에이전트 도메인이다.</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2608.26530'>PILOT in the Loop: Live Self-Improvement for Long-Horizon Agents</a></td><td>30</td><td>2</td><td>LG 등</td><td>supervisor가 실행 중인 worker agent를 실시간 steering하고 경험을 skill/memory로 증류하는 long-horizon agent harness(PILOT)로 Terminal-Bench 2.0에서 최대 9.8%p 향상을 보였다. robot memory·skill chaining과 유사한 문제의식이나 소프트웨어 에이전트 대상이다.</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2608.26747'>AgentFold: Closed-Loop Agentic Search for Protein Folding Model Design</a></td><td>30</td><td>2</td><td>LG 등</td><td>단백질 폴딩 모델(ESMFold)의 코드 수준 아키텍처를 MCTS 스타일로 자동 탐색·개선하는 closed-loop multi-agent 시스템(AgentFold)으로 lDDT를 7.5% 개선했다. 과학적 자동 설계 탐색 패러다임은 흥미로우나 robotics와는 무관하다.</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2608.27351'>Understanding Evolution Strategies for LLM Reasoning: Broader Reasoning Coverage than GRPO</a></td><td>30</td><td>1</td><td>RL</td><td>LLM reasoning post-training에서 evolution strategies가 GRPO보다 넓은 reasoning coverage를 보인다는 분석으로 로봇 정책 학습과의 직접 연결은 약하다.</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2608.26120'>Recipes for Steering and Scaling LLMs via Sampling</a></td><td>30</td><td>1</td><td>NLP</td><td>SMC·Replica Exchange 기반으로 LLM 생성 분포를 steering·scaling하는 샘플링 이론 프레임워크로 test-time 방법론이나 텍스트 생성에 국한되어 로봇 적용과는 거리가 있다.</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2608.26152'>Artificial Intelligence Models Can Predict and Collaboratively Modulate Human Memory Search</a></td><td>30</td><td>1</td><td>NLP</td><td>LLM이 인간의 semantic fluency task 궤적을 예측·조절한다는 인지과학적 발견이나 robot memory와는 직접 연결이 약하다.</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2608.26295'>MemToC: Benchmarking Memory-Tool Conflict Resolution in Large Language Models</a></td><td>30</td><td>1</td><td>NLP</td><td>tool 반환값과 parametric memory가 충돌할 때 LLM의 arbitration을 재는 MemToC 벤치마크로 memory-tool 신뢰 문제를 다루나 embodied 맥락은 없다.</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2608.26374'>Survival-Guided Length Control for Efficient Diffusion Language Models</a></td><td>30</td><td>1</td><td>NLP</td><td>diffusion LM의 길이 선택을 survival 문제로 재정식화해 추론을 최대 7배 가속하는 plug-in 방법이다.</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2608.26550'>SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning</a></td><td>30</td><td>1</td><td>RL</td><td>symbolic milestone과 LCS 정렬로 신경망 PRM 없이 dense process reward를 주는 SPEAR로 distillation 효율을 높였다.</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2608.27348'>INTENT-AS-A-TOOL Makes it Easy to Track Agentic Misalignment</a></td><td>30</td><td>1</td><td>NLP</td><td>intent 전용 tool 호출 확률로 CoT 모니터링을 보완해 agentic misalignment를 조밀하게 추적하는 INTENT-AS-A-TOOL이다.</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2608.26385'>Why RAGs Hallucinate: Penalty-Aware Evaluation of Retrieval-Augmented Generation Systems with Knowledge-Gap Canaries</a></td><td>30</td><td>0</td><td>NLP</td><td>knowledge-gap canary와 비대칭 채점으로 RAG의 abstention 실패를 분리 진단하는 평가 프레임워크다.</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2608.26465'>Compositional Generalization via Structural Identification in a Category-Theoretic Framework</a></td><td>30</td><td>0</td><td>NLP</td><td>Kan extension으로 compositional generalization의 admissibility를 데이터 측에서 진단하는 범주론적 프레임워크다.</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2608.26511'>Sycophancy Suppression Can Impair Rational Updating: Anti-Sycophancy Should Preserve the Ability to Update</a></td><td>30</td><td>0</td><td>NLP</td><td>anti-sycophancy 개입이 rational updating 능력까지 손상시킨다는 메커니즘적 trade-off를 규명했다.</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2608.26587'>Surgical Alignment in Knowledge Graph Training for Clinical Diagnosis with Large Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>KG-LLM 통합 방식이 만드는 gradient 갱신의 희소성(GID/GD)을 새 지표로 진단한 방법론적 연구다.</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2608.26638'>Which Metrics Save the Most Human Annotation? Prediction-Powered Evaluation and Meta-Evaluation</a></td><td>30</td><td>0</td><td>NLP</td><td>prediction-powered inference로 사람 평가 비용을 줄이는 일반적 통계 프레임워크와 새 메타지표(PPSR)를 제안한다.</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2608.26762'>Equal Ranking Quality, Different Decisions: Training Order-Consistent LLM Scorers</a></td><td>30</td><td>0</td><td>NLP</td><td>ranking quality가 같아도 순서에 따라 실제 결정(retain/answer)이 크게 달라짐을 보이고 OC-SFT로 안정화했다.</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2608.26982'>JudgeStealer: Extracting LLM Judging Capabilities across Evaluation Protocols</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM judge의 판단 능력을 pointwise/pairwise/listwise 전방위로 추출하는 첫 query-efficient 공격(JudgeStealer)이다.</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2608.27394'>RATIO: A Benchmark for Retrieval Across Typed Ideation Operations in Scientific Literature</a></td><td>30</td><td>0</td><td>NLP</td><td>Address/Broaden/Specify라는 ideation move 단위로 과학 문헌 검색을 재정의한 RATIO 벤치마크로 아이디어 발상 지원 검색이라는 새 문제를 제시한다.</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2608.27428'>Stochastic Estimation of Transduced Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>transduced LM의 target prefix 확률을 threshold pruning 대신 unbiased resampling으로 추정하는 이론적 알고리즘 기여다.</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2608.26739'>Residual Deep Reinforcement Learning-Based Computed Torque Control for a Cable-Driven Lower-Limb Rehabilitation Robot under Disturbances and Parametric Uncertainties</a></td><td>28</td><td>5</td><td>RL</td><td>케이블 구동 재활로봇의 computed torque control에 잔차 DDPG 보정을 결합한 연구로 시뮬레이션 검증 중심의 점진적 제어 엔지니어링에 가깝다.</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2608.27186'>Task-space model-based control of pneumatic soft actuators</a></td><td>28</td><td>5</td><td>Robotics</td><td>비최소좌표 이산 탄성봉 모델 기반의 공압 소프트 액추에이터 task-space 제어 연구로 모델 기반 제어의 점진적 개선에 가깝다.</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2608.27151'>Planning a Shared Modular Fixture Layout Across Robotic Disassembly Stages</a></td><td>28</td><td>4</td><td>Manipulation</td><td>diffusion 모델로 초기 배치를 생성하고 베이지안 최적화로 정제하는 분해 단계별 공유 고정구 레이아웃 계획 연구로 특정 산업 응용에 가까운 엔지니어링이다.</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2608.26214'>Surgical Video Generation From Diffusion to World Models: A Survey</a></td><td>28</td><td>3</td><td>World Model</td><td>surgical video generation/world model 서베이로 새 방법론 제시 없이 문헌 정리에 그친다.</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2608.26780'>AI Control Scientist: LLM-driven Agentic System for Automated Control Design</a></td><td>28</td><td>3</td><td>RL</td><td>화학 공정·항공엔진 제어 설계를 Task Modeling-Controller Design-Parameter Tuning agent로 자동화하는 시스템(AICS)으로, 제어 자동화 문제의식은 로봇 제어와 접점이 있으나 산업 프로세스 제어에 초점이 맞춰져 있다.</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2608.27454'>WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution</a></td><td>28</td><td>3</td><td>Embodied AI</td><td>agent의 실행 경험을 raw trace-지식 wiki-executable skill 세 층위로 분리해 지속적으로 축적·재사용하는 skill evolution 프레임워크(WikiSkill)로, 여러 벤치마크에서 no-skill 및 기존 skill-evolution 방법 대비 우수했다. skill chaining·robot memory와 개념적으로 유사하나 로봇 실험은 없다.</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2608.26948'>KISS-GS: 3D Gaussian Splatting Compression Kept Simple</a></td><td>28</td><td>2</td><td>3D Vision</td><td>3DGS를 최대 319배 압축하는 모듈형 파이프라인으로 실용적이나 학습과 분리된 압축 engineering에 가깝다.</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2608.26846'>Evaluating Confidence-Gated Retrieval with Matched Trajectory Replay</a></td><td>28</td><td>2</td><td>NLP</td><td>confidence-to-action 매핑을 궤적 수준 결과로 비교하는 matched trajectory replay로, retrieval 여부를 결정하는 test-time 판단을 다룬다는 점에서 실패 회복적 의사결정과 맥락이 닿는다.</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2608.26833'>Rethinking Image Processing for the Age of AI: A Problem-First Framework for Scientific Progress</a></td><td>28</td><td>1</td><td>CV</td><td>model-first 벤치마크 경쟁 문화를 비판하는 position paper로 실증적 기여보다 연구방법론 제안에 가깝다.</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2608.26582'>J-Zero: Unified Challenger--Solver--Judge Co-Evolution from Zero Data</a></td><td>28</td><td>1</td><td>NLP</td><td>Challenger-Solver-Judge가 함께 진화하는 zero-data self-improvement 프레임워크로 LLM 도메인에 한정되나 curriculum·adversarial task generation 아이디어는 참고할 만하다.</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2608.26879'>Mitigating Strong-Modality Collapse in Multimodal Learning via Inverted Asymmetric Fusion</a></td><td>28</td><td>1</td><td>Multimodal</td><td>멀티모달 융합에서 강한 모달리티가 오히려 손상되는 현상을 다루는 연구로 로봇 학습과의 연결은 약하다.</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2608.27135'>Said Aloud, Read Different: Cross-Modal Instability in Multimodal Models</a></td><td>28</td><td>1</td><td>Multimodal</td><td>음성 vs 텍스트, 영어 vs 아랍어에서 멀티모달 모델의 판단이 불일치함을 보인 문화적으로 그라운딩된 벤치마크다.</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2608.26288'>Muon with Finite Newton-Schulz: The Smoothing Benefit in Nonsmooth Nonconvex Optimization</a></td><td>28</td><td>0</td><td>LG</td><td>Muon optimizer의 finite Newton-Schulz가 nonsmooth nonconvex 최적화에 이론적으로 유리함을 증명한 최적화 이론 논문으로 로봇 관련성은 없다.</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2608.26159'>Self-Generated Text Recognition: Quality Heuristics, Cross-Task Transfer, and Downstream Bias in LLM Evaluation</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM이 자기 출력을 인식해 judge로 쓰일 때 편향을 일으키는 SGTR 현상을 체계적으로 규명한 안전성 연구다.</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2608.26175'>Lost in Compression: A Controlled Cross-Lingual Audit of Extractive Prompt Compressors</a></td><td>28</td><td>0</td><td>NLP</td><td>extractive prompt compression이 영어 외 언어에서 성능을 크게 해친다는 대규모 통제 감사이나 로봇과 무관하다.</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2608.26357'>Cross-lingual Representation Learning via Centroid Intervention Fusion</a></td><td>28</td><td>0</td><td>NLP</td><td>여러 언어 intervention projection을 하나의 공유 연산자로 합치는 CIF 방법으로 저자원 언어 전이에 초점을 맞춘다.</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2608.26529'>Multi-Expert Conformal Risk Control for Pairwise LLM Judging in Open-Ended Dialogue</a></td><td>28</td><td>0</td><td>NLP</td><td>이질적 LLM judge 패널에 대해 conformal risk control로 coverage를 회복하는 MC3 방법이다.</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2608.26574'>Dependency-Aware Revocable Decoding for Efficient Diffusion Large Language Model Inference</a></td><td>28</td><td>0</td><td>NLP</td><td>diffusion LLM의 revocable decoding에서 verification context를 선택적으로 정제하는 DARD로 속도-품질 파레토를 개선한다.</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2608.26576'>Double Trouble: Bilingual Pretraining Leaves Language-Conditioned Effects in Shared-Language Representations</a></td><td>28</td><td>0</td><td>NLP</td><td>이중언어 사전학습이 공유 언어의 은닉표현에 남기는 불일치를 통제 실험으로 보인 해석가능성 연구다.</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2608.26641'>Information-Guided Frontier Decoding: Contextual Utility-Driven Commitment in dMLLMs</a></td><td>28</td><td>0</td><td>Multimodal</td><td>diffusion MLLM 디코딩에서 confidence 대신 contextual utility로 토큰 커밋 순서를 정하는 training-free 방법이다.</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2608.26735'>Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD</a></td><td>28</td><td>0</td><td>NLP</td><td>도메인 특화 시 일반 능력 저하를 막는 uncertainty-calibrated MOPD로 dual-temperature 샘플링과 CLL 필터링을 결합했다.</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2608.26779'>Instruction Quality Matters: Refining Instructions for Effective Preference Learning</a></td><td>28</td><td>0</td><td>NLP</td><td>선호학습에서 instruction 품질이 병목임을 밝히고 rubric 기반 refinement 파이프라인을 제안한다.</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2608.26925'>Mapping Written Words to Spoken Words in a Different Language Using Only Visual Grounding</a></td><td>28</td><td>0</td><td>NLP</td><td>transcription 없이 시각적 grounding만으로 언어 간 단어-음성 매핑을 정렬 기반으로 학습한 연구다.</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2608.26973'>Squeezing More from Limited Data with Recursive Transformers</a></td><td>28</td><td>0</td><td>NLP</td><td>저자원 사전학습에서 recursive transformer와 factorized embedding으로 파라미터-데이터 결합을 완화한 구조 연구다.</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2608.27165'>Prediction of Prediction (PoP): Inter-Layer Activation Fusion for Single-Pass Hallucination Detection in Large Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>레이어 간 hidden state 전이를 단일 forward pass에서 융합해 환각을 탐지하는 PoP 방법이다.</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2608.26476'>Zero-Shot Video Restoration and Enhancement with Text-to-Image Latent Diffusion Models and Multi-Modal References</a></td><td>26</td><td>1</td><td>Video</td><td>zero-shot video restoration으로 diffusion inversion 효율화를 제안하나 로봇 관련성은 낮다.</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2608.26580'>Visual Information-Guided Parallel Decoding for Diffusion Multimodal Large Language Models</a></td><td>26</td><td>1</td><td>Multimodal</td><td>diffusion MLLM의 병렬 디코딩 순서를 이미지 attention 기반으로 개선한 sampler 수준의 기여다.</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2608.26585'>GRAS: Guided Reduced-Variance Proposals and Adaptive Selection for Training-Free Reward Alignment in Discrete Diffusion</a></td><td>26</td><td>1</td><td>LG</td><td>discrete diffusion의 training-free reward alignment를 위한 분산 감소 proposal과 adaptive resampling 기법으로 DNA·단백질 설계에 적용했으며 test-time steering 원리는 일반화 가능하다.</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2608.26807'>Behavior2Trip: Towards Personalized Travel Planning via User Behavior Trajectory</a></td><td>26</td><td>1</td><td>NLP</td><td>과거 행동 궤적에서 선호를 추론해 여행 계획을 세우는 RL 에이전트(B2T-Agent)로 사용자 선호 추론이라는 새 과제를 정의했다.</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2608.27161'>STAR : Sentence Translation Alignment Rate for Document-to-Document Machine Translation</a></td><td>26</td><td>0</td><td>NLP</td><td>문서 단위 번역의 문장 정합성을 재는 STAR 지표와 이를 최적화하는 StarPO를 제안한다.</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2608.27360'>Your Voice Cloning System is Secretly a Voice Anonymizer</a></td><td>26</td><td>0</td><td>NLP</td><td>음성 클로닝 모델 XTTSv2를 재훈련 없이 화자 익명화기로 재활용한 발견적 연구다.</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2608.27370'>Puro-2B: Poor Lab&#x27;s Qwen2-1.5B Trained on RTX 5090 within $5090</a></td><td>26</td><td>0</td><td>NLP</td><td>소비자용 GPU로 저비용 LLM 사전학습을 가능케 한 Puro-2B 레시피와 비용 스케일링 법칙으로, 경량화·효율 위주 기여다.</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2608.27380'>D2C-Routing: Dimension-to-Composition Evidence Routing for Mixed-Origin AI-Generated Text Detection</a></td><td>26</td><td>0</td><td>NLP</td><td>content/expression origin을 분리해 혼합 기원 AI 텍스트를 탐지하는 D2C-Routing 방법이다.</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2608.26505'>Closing the Loop on the Poppy Humanoid: Bipedal Locomotion with Linear-Quadratic Control and Learned Cost Functions</a></td><td>25</td><td>5</td><td>Manipulation</td><td>Poppy 휴머노이드에 LQR과 학습된 비용함수로 폐루프 보행 제어기를 구현한 연구로, 특정 오픈소스 하드웨어에 대한 엔지니어링 성격이 강해 개념적 새로움은 제한적이다.</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2608.26819'>CLIPPER: Replayable Shortlisted Optimization for Repeated Spatial Coverage Planning</a></td><td>25</td><td>3</td><td>RL</td><td>도시 마이크로모빌리티 배치 계획을 위한 재계산 가능한 shortlisted 최적화 기법으로 로봇 학습보다는 도시 공간 계획 응용에 가깝다.</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2608.26755'>Safety by Design: Realized-Cost Constraints for Contextual Bandits with Continuous Actions</a></td><td>25</td><td>2</td><td>RL</td><td>연속 행동 contextual bandit의 안전 제약 이론 연구로 자율 시스템 언급은 있으나 로봇 학습과는 거리가 있다.</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2608.27152'>Ultra Low-Power, Lightweight, Probabilistic RSS-Based Path Reconstruction: A System for Landscape-Scale Bee Tracking</a></td><td>25</td><td>2</td><td>Robotics</td><td>초저전력 RSS 기반 곤충 추적 시스템으로 로보틱스에 언급되나 로봇 학습 자체와는 거리가 있다.</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2608.26189'>Invocation-Level Reliability of Tool-Using Agents</a></td><td>25</td><td>2</td><td>LG 등</td><td>tool-using agent의 invocation 단계 실패 전파를 측정해 depth 6에서 clean-context 성능의 약 70%가 손실됨을 보였으나, 소프트웨어 tool-use 도메인이며 로봇 실행과는 다르다.</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2608.26291'>Assessing mentalization in humans and large language models</a></td><td>25</td><td>2</td><td>NLP</td><td>경제 게임과 인지 계산 모델링으로 LLM의 mentalization(마음이론) 전략을 인간과 비교한 연구로 사회적 추론 평가는 흥미로우나 robotics 적용은 다루지 않는다.</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2608.26763'>Categorizer Automata for Discounted-Sum Payoffs</a></td><td>25</td><td>2</td><td>RL</td><td>discounted-sum payoff에 대한 유한 상태 automaton으로 불연속 utility function에서도 pseudo-polynomial time MDP 정책 합성을 보장하는 형식적 방법 연구로 RL 정책 합성과 관련 있으나 로봇 응용은 다루지 않는다.</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2608.26716'>Beyond Atomic Layouts: Compositional Design Understanding with Vision-Language Models</a></td><td>25</td><td>1</td><td>Multimodal</td><td>문서/UI의 compositional layout 이해를 다루며 GPT-o3 79.68%를 91.66%로 끌어올렸으나 로봇과는 거리가 멀다.</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2608.26744'>G2D: Generative-to-Discriminative Collaborative Inference for Zero-Shot Image Classification</a></td><td>25</td><td>1</td><td>CV</td><td>CLIP과 generative VLM을 결합한 training-free zero-shot 분류로 로봇 관련성은 낮다.</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2608.26812'>Hyperspectral Diffusion Equivariant Imaging (HyDiff-EI): A Self-supervised Framework for Hyperspectral Image Inpainting</a></td><td>25</td><td>1</td><td>CV</td><td>단일 취득 영상만으로 학습하는 test-time hyperspectral inpainting이나 원격탐사 응용에 한정된다.</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2608.26956'>RubricRM: Generative Reward Modeling via Dynamic Rubrics for Image Generation and Editing</a></td><td>25</td><td>1</td><td>Multimodal</td><td>이미지 생성/편집을 위한 입력별 dynamic rubric 기반 reward model로 로봇 관련성은 낮다.</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2608.26829'>SAGE: Variate-Wise Semantic Augmentation for Vision-Language Time Series Forecasting</a></td><td>25</td><td>1</td><td>Multimodal</td><td>CLIP 기반 시계열 예측에 의미 정보를 결합한 방법으로 로봇 학습과의 연결은 약하다.</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2608.26965'>ClusterAttention: A training-free speedup of bidirectional attention</a></td><td>25</td><td>1</td><td>LG</td><td>양방향 attention의 training-free 가속 기법으로 비디오 생성에도 적용되나 핵심은 추론 효율화이다.</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2608.26121'>Can a Model Catch Its Own Hallucinations for Free?: Label-Free Doubt Signals Hold Their Own Against a Labelled Dataset for Abstention</a></td><td>25</td><td>1</td><td>NLP</td><td>레이블 없이 모델 자체 confidence만으로 abstention을 학습하는 연구로 실패 인지라는 개념은 로봇 실패 탐지와 느슨히 연결되나 도메인은 QA이다.</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2608.26141'>AdaThinking-E: One-Token Entropy Regulation for Adaptive Thinking</a></td><td>25</td><td>1</td><td>Multimodal</td><td>단일 토큰 엔트로피로 사고 개입 여부를 결정하는 적응적 reasoning RL 기법으로 test-time 적응 개념은 있으나 문서 reasoning 도메인이라 로봇 적용과는 거리가 있다.</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2608.26961'>Gromov-Monge Flow Matching for Equivariant Graph Generation</a></td><td>25</td><td>0</td><td>CV</td><td>그래프 생성에서 순열 대칭을 고려한 flow matching 방법으로 분자 생성이 주 대상이며 로보틱스와 무관하다.</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2608.26962'>Packora: Systematic Design for Generative Molecular Crystal Structure Prediction</a></td><td>25</td><td>0</td><td>CV</td><td>분자 결정 구조 예측을 위한 flow 기반 생성 모델로 소재과학 응용이며 로보틱스와 무관하다.</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2608.26139'>Syntax vs. Semantics: How Transformers Learn Deep Dependencies</a></td><td>25</td><td>0</td><td>NLP</td><td>transformer가 표면 통계와 심층 의미 의존성을 학습하는 과정을 gradient starvation으로 설명하는 이론 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2608.27199'>Vision-centric generative AI models: A software-hardware perspective</a></td><td>24</td><td>2</td><td>CV</td><td>vision generative AI의 하드웨어-소프트웨어 co-design을 주장하는 perspective 논문으로 자율주행 등을 언급하나 새 방법 제안은 없다.</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2608.26827'>Evaluator-Dependent Patient-Adaptive ECG Lead-Channel Allocation</a></td><td>24</td><td>1</td><td>CV</td><td>ECG 채널 선택 정책이 평가 모델에 따라 달라짐을 보인 분석 논문으로 active sensing과 개념적으로만 유사하다.</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2608.26375'>CG4AI: A Column Generation Framework for Training AI Models Under Constraints</a></td><td>24</td><td>1</td><td>LG</td><td>column generation으로 AI 모델 출력에 선형 제약을 강제하는 프레임워크로 autonomous system을 언급하나 로봇 특화 검증은 없다.</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2608.26581'>Activation Outliers Matter: Robust Recovery for Quantized Multimodal LLMs</a></td><td>24</td><td>1</td><td>Multimodal</td><td>양자화된 멀티모달 LLM에서 activation outlier가 성능저하의 주 원인임을 밝히고 residual fallback으로 보정하는 efficiency 기법이다.</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2608.26163'>From Sound to Symptom: Real-Time Respiratory Signal Understanding for Conversational Healthcare Agents</a></td><td>24</td><td>1</td><td>Multimodal</td><td>대화 중 기침 신호를 실시간 처리하는 헬스케어 파이프라인으로 응용 엔지니어링에 가깝다.</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2608.27334'>BTS-AgentBench: A Deterministic, Replayable Pipeline from Read-Only Telemetry Logs to Agent Benchmarks</a></td><td>24</td><td>1</td><td>NLP</td><td>산업 현장 read-only telemetry를 결정론적으로 에이전트 벤치마크 episode로 변환하는 파이프라인(BTS-AgentBench)이다.</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2608.26516'>Algorithmic Principles For Multiclass Learning Are Hard To Come By: Limits of Regularization and Proper Learning</a></td><td>24</td><td>0</td><td>LG</td><td>multiclass learning에서 proper learning·regularization의 한계를 증명한 이론 논문으로 로봇 응용은 없다.</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2608.26143'>Beyond Accuracy: A Qualitative Analysis of Vision-Language Models for Hate Speech Detection in Memes</a></td><td>24</td><td>0</td><td>NLP</td><td>밈 혐오표현 탐지에서 VLM 정성 분석에 그쳐 새 방법론이 없고 로봇 연구와 무관하다.</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2608.26177'>A Multi-Framework Comparison of Outline Stages in Long-Form Generation with LLMs</a></td><td>24</td><td>0</td><td>NLP</td><td>장문 생성에서 outline 단계 자체를 평가하는 벤치마크로 도메인이 글쓰기에 한정된다.</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2608.26194'>A Reranker for Orchestrating Heterogeneous Speech and Text Retrievers</a></td><td>24</td><td>0</td><td>NLP</td><td>음성·텍스트 혼합 검색을 위한 reranker 학습으로 응용 엔지니어링이다.</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2608.26414'>Case2Flow: Bridging Patient Cases and Guideline Flowcharts through Multimodal Retrieval</a></td><td>24</td><td>0</td><td>Multimodal</td><td>환자 사례를 가이드라인 flowchart와 매칭하는 멀티모달 검색 과제(Case2Flow)로 의료 응용에 국한된다.</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2608.26674'>Do LLMs Understand Personality? Rethinking Persona Fidelity Evaluation through Structured Behavioral Inference</a></td><td>24</td><td>0</td><td>NLP</td><td>persona fidelity를 SFL 기반 구조적 추론으로 재정식화한 평가 프레임워크(PRISM)다.</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2608.26706'>Towards Expert Financial QA via Self-Improving RAG</a></td><td>24</td><td>0</td><td>NLP</td><td>금융 QA용 self-improving RAG로 judge 기반 재시도를 도입한 응용 시스템이다.</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2608.26832'>RuleWeaver: Benchmarking Rule-Centered Scenario Reasoning for Large Language Models</a></td><td>24</td><td>0</td><td>NLP</td><td>규칙 중심 시나리오 추론을 재는 RuleWeaver 벤치마크로 응용 평가에 그친다.</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2608.27036'>Reasoning about In-Context Samples for Machine-Translation</a></td><td>24</td><td>0</td><td>NLP</td><td>in-context 예시에서 병렬 fragment를 추출해 추론 흔적으로 쓰는 기계번역 방법이다.</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2608.27000'>Arbitrary-Order Hermite Interpolation of Rigid-Motion Jets via Hyper-Multidual Quaternions</a></td><td>22</td><td>4</td><td>Robotics</td><td>강체운동 jet의 임의 차수 Hermite 보간을 hyper-multidual quaternion으로 다루는 순수 수학적 screw theory 연구로 학습 기반 로보틱스와는 거리가 있다.</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2608.26806'>Multi-Image Visual Token Pruning in Large Visual Language Models</a></td><td>22</td><td>1</td><td>Multimodal</td><td>다중 이미지 LVLM용 training-free visual token pruning으로 efficiency 위주의 기여다.</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2608.26820'>LLaVAFlow: Preserving Latent Alignment Flow for Parameter-Efficient Multimodal Fine-Tuning</a></td><td>22</td><td>1</td><td>Multimodal</td><td>MLLM fine-tuning 시 정보이론적 distillation으로 catastrophic forgetting을 줄이는 PEFT 기법이다.</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2608.27206'>PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference</a></td><td>22</td><td>1</td><td>Multimodal</td><td>VLM 추론을 가속하는 training-free condense-and-extract 프레임워크로 로봇 관련성은 낮은 efficiency 기여다.</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2608.26649'>Robust Neural Stimulation Response Modeling Through Meta-Learning and Pretraining</a></td><td>22</td><td>1</td><td>RL</td><td>신경 자극 반응 예측에 meta-learning·pretraining을 적용해 세션당 캘리브레이션을 줄인 연구로 폐루프 제어의 sample-efficient 적응이라는 아이디어가 로봇 sim-to-real 적응과 개념적으로 유사하다.</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2608.27048'>Soft Active Electromyography Interface for Machine Learning-Enabled Silent Speech Recognition</a></td><td>22</td><td>1</td><td>CV</td><td>손가락 부착형 EMG 인터페이스로 무음 음성 인식을 수행하는 웨어러블 HCI 연구로 로봇 학습과의 직접 연결은 약하다.</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2608.27070'>Unifying Detection and Adaptation in Task-Free Continual Learning</a></td><td>22</td><td>1</td><td>NLP</td><td>LLM의 task-free continual learning을 위한 Fisher 기반 LoRA 프레임워크로 로봇 continual learning과는 도메인이 다르다.</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2608.26809'>Thinking on Shots: Consistent Multi-Shot Video Editing with Agentic Reasoning</a></td><td>22</td><td>0</td><td>Video</td><td>multi-shot 장편 비디오 편집을 위한 에이전틱 프레임워크로 로봇 학습과 무관하다.</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2608.26324'>Privacy Without Regret: Differentially Private Inference-Time Alignment</a></td><td>22</td><td>0</td><td>NLP</td><td>Best-of-N inference-time alignment에 차등 프라이버시를 결합한 이론적 분석으로 로봇 관련성이 없다.</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2608.26462'>Diff Mining: Logit Differences Reveal Finetuning Objectives</a></td><td>22</td><td>0</td><td>NLP</td><td>logit 차이로 finetuning 목표를 역추적하는 모델 diffing 기법으로 로봇 학습과 무관하다.</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2608.26963'>Adversarial Training Without Input Gradients via Low-Rank Householder Expansions</a></td><td>22</td><td>0</td><td>LG</td><td>입력 gradient 없이 저랭크 Householder 전개로 adversarial training을 수행하는 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2608.27032'>Disentangling Optimization Scale from Preference Scale in DPO</a></td><td>22</td><td>0</td><td>NLP</td><td>DPO의 beta 계수가 갖는 두 역할을 분리하는 이론 연구로 LLM 정렬에 국한되며 로보틱스와 무관하다.</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2608.27254'>Circuit Condensation: Post-Training that Concentrates a Behavior&#x27;s Causal Circuit</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM 행동의 인과 회로를 축소하는 mechanistic interpretability post-training 기법으로 로보틱스와 무관하다.</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2608.26161'>Mutual Debiasing via Dual-Seed Comparison for Probabilistic Sampling in Large Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM의 확률적 샘플링 편향을 dual-seed로 상쇄하는 도구적 기법으로 범위가 좁다.</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2608.26180'>PACEShop: Evaluating Personalized, Actionable, Compositional, and Evidence-grounded Shopping Assistants</a></td><td>22</td><td>0</td><td>NLP</td><td>쇼핑 어시스턴트용 PACE 평가 벤치마크로 응용 도메인 벤치마크에 그친다.</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2608.26327'>How Unlikely Is &quot;Unlikely&quot;? Assessing Verbal Probability Perception Across Large Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM의 언어적 확률 표현(예: unlikely) 해석을 인간 기준과 비교한 평가 연구다.</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2608.26434'>AfriSwitch: A Benchmark for In-the-Wild African Code-Switched Speech Recognition</a></td><td>22</td><td>0</td><td>NLP</td><td>아프리카 code-switched 음성인식 벤치마크로 자원 구축 기여다.</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2608.26592'>Benchmarking Clinical Decision Pathway Adherence in Large Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>임상 의사결정 경로 준수를 재는 MEGA-CDP 벤치마크로 응용 평가에 그친다.</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2608.26650'>Meta-Learning Where to Allocate Experts: Task-Conditioned Layer-Wise Compression for MoEs</a></td><td>22</td><td>0</td><td>NLP</td><td>MoE의 레이어별 전문가 활성화를 task-conditioned로 조절하는 경량화 기법이다.</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2608.26689'>Beyond Reflection: Affirmation as a Promising Behavioral Marker Associated with Quality in Text-Based Counseling</a></td><td>22</td><td>0</td><td>NLP</td><td>텍스트 상담에서 reflection보다 affirmation이 품질과 더 관련 있다는 행동 분석 연구다.</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2608.26697'>Scaling phoneme-based TTS augmentation for ASR: A unified pipeline and controlled study</a></td><td>22</td><td>0</td><td>NLP</td><td>TTS 증강으로 ASR을 개선하는 파이프라인 및 phoneme 빈도 기반 후보 선택 기법이다.</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2608.27038'>Cascaded Batch Prompting</a></td><td>22</td><td>0</td><td>NLP</td><td>복잡한 추론과 symbol grounding을 분리한 2단계 batch prompting으로 효율-성능 파레토를 개선했다.</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2608.27358'>RCMN: Understanding Misleadingness in Influential Public Discourse</a></td><td>22</td><td>0</td><td>NLP</td><td>공적 담론의 오해 유발 메커니즘을 5차원으로 정식화한 RCMN 프레임워크다.</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2608.26107'>EduRiskX: A Neuro-Symbolic Framework with F-Logic Reasoning for Early Academic Risk Prediction</a></td><td>22</td><td>0</td><td>NLP</td><td>F-Logic 규칙과 temporal Transformer를 결합한 학업 위험 조기예측 시스템(EduRiskX)으로 교육 응용에 국한된다.</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2608.26109'>Standalone LLM and a Pre-specified Agentic Pipeline for Explaining ICU Mortality Predictions: a Feasibility Study on the eICU Demo Dataset</a></td><td>22</td><td>0</td><td>NLP</td><td>ICU 사망률 예측 설명에서 standalone LLM과 agentic pipeline을 38건 규모로 비교한 예비 타당성 연구다.</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2608.26789'>Online Joint Calibration of Steering Offset and Planar LiDAR Extrinsics for Wheeled Mobile Robots</a></td><td>20</td><td>4</td><td>Robotics</td><td>조향 오프셋과 LiDAR 외부 파라미터를 EKF로 온라인 보정하는 캘리브레이션 연구로 창의성보다는 실용적 엔지니어링에 가깝다.</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2608.26669'>Beyond the Proving Ground: Independent Public-Road Testing of Assisted Lane Change Systems using LiDAR</a></td><td>20</td><td>3</td><td>Robotics</td><td>공공도로에서 LiDAR로 차선변경 보조 시스템의 규제 준수를 독립 검증한 실증 연구로 방법론적 새로움보다는 규제·테스트 성격이 강하다.</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2608.26991'>ASIL: Replacing Screenshot-and-Click with Structured State and Semantic Actions</a></td><td>20</td><td>2</td><td>LG 등</td><td>GUI screenshot-click 대신 구조화된 JSON 상태와 semantic action으로 소프트웨어를 조작하는 agent-native interface(ASIL)로 screenshot 기반 대비 strict success가 크게 향상됐다(예: 26.6→53.3). 구조화된 상태·행동 표현이라는 아이디어는 embodied action representation과 유사하나 GUI 소프트웨어 도메인이다.</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2608.26517'>HUG-VIS: A Multimodal Benchmark for Human-centered Understanding and Generation in Visual Intelligence</a></td><td>20</td><td>1</td><td>Multimodal</td><td>인간 중심 감정·비디오생성·음성복제 통합 벤치마크로 로봇 관련성이 낮다.</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2608.26665'>Hull First, Wake Second: Wake-Reliance Suppression for Robust Maritime Vessel Detection</a></td><td>20</td><td>1</td><td>CV</td><td>해상 선박 탐지에서 wake-reliance 문제를 다룬 detection engineering으로 로봇 관련성이 낮다.</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2608.26724'>GeoMAD: Geometry-Aware Multi-View Anomaly Detection via Deformable Fusion and Distributional Alignment</a></td><td>20</td><td>1</td><td>CV</td><td>산업 다중뷰 이상탐지 프레임워크로 로봇 학습과 관련이 낮다.</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2608.27182'>TraceBench: Controlled Evaluation of LLM Agents for Time-Series Root-Cause Attribution</a></td><td>20</td><td>1</td><td>NLP</td><td>시계열 근본원인 분석을 위한 LLM 에이전트 벤치마크로 로봇 실패 진단과 개념적으로 인접하나 도메인은 산업 시스템이다.</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2608.26442'>Don&#x27;t Overthink, Don&#x27;t Underthink: Toward Adaptive Reasoning in Agentic AI</a></td><td>20</td><td>1</td><td>LG 등</td><td>agentic workflow에서 reasoning 과다/과소 배분을 MATH-500·GAIA로 분석한 연구로 test-time reasoning 최적화와 개념적 접점이 있으나 로봇 도메인은 다루지 않는다.</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2608.27260'>What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents</a></td><td>20</td><td>1</td><td>LG 등</td><td>agentic 데이터를 (E,q,τ,v)로 정형화하고 Accuracy-Complexity-divErsity 관점에서 생성 방법론을 정리한 프레임워크(ACE)로 IL 데이터 생성과 개념적 접점이 있으나 로봇 도메인은 다루지 않는다.</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2608.26714'>LiveVVT: High-Fidelity Video Virtual Try-On in Real Time</a></td><td>20</td><td>0</td><td>Video</td><td>실시간 비디오 가상 피팅 시스템으로 로봇 학습과 무관하다.</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2608.26132'>SLM-Conditioned Hierarchical Relation Routing for Labeled Property Graph Learning</a></td><td>20</td><td>0</td><td>LG</td><td>SLM을 이용한 property graph의 관계 라우팅 학습으로 로봇 학습과 무관하다.</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2608.26926'>A Layer Importance Metric for Quantization Accounting for the Speed-Quality Trade-off in Autoregressive Models</a></td><td>20</td><td>0</td><td>LG</td><td>소형 언어모델 양자화를 위한 레이어 중요도 지표로 경량화 중심 연구이며 로보틱스와 무관하다.</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2608.26958'>Scaling Model-Generated Distillation Data Can Make Latent Teacher Traits More Recoverable</a></td><td>20</td><td>0</td><td>NLP</td><td>distillation 데이터 스케일링이 teacher 특성 노출에 미치는 영향을 다룬 LLM 안전성 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2608.27046'>Performance Foundations of Parallel &amp; Distributed Reasoning Language Models</a></td><td>20</td><td>0</td><td>LG</td><td>reasoning LLM 학습을 위한 병렬/분산 시스템 분석으로 로보틱스와 무관한 시스템 연구이다.</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2608.27286'>MM-Spectrum: Multimodal Multi-spectral Molecular Structural Elucidation with a Stable MoE Framework</a></td><td>20</td><td>0</td><td>Multimodal</td><td>다중 스펙트럼 신호로부터 분자 구조를 추론하는 MoE 프레임워크로 화학 응용이며 로보틱스와 무관하다.</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2608.27339'>Beyond Parallel Blindness: Information Floors and Model Gaps in Block Drafting</a></td><td>20</td><td>0</td><td>NLP</td><td>block drafting의 거부율을 정보 하한과 모델 격차로 분해하는 speculative decoding 분석 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2608.26112'>TreeGraft: Adaptive Multi-Drafter Grafting for Tree-Based Speculative Decoding</a></td><td>20</td><td>0</td><td>NLP</td><td>tree 기반 speculative decoding에서 여러 drafter를 결합하는 TreeGraft로 LLM 추론 가속 연구이며 로보틱스와 무관하다.</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2608.26144'>Why Current XAI Is Not Enough for Arabic NLP: A Critical Survey of the Explainability Gap</a></td><td>20</td><td>0</td><td>NLP</td><td>아랍어 XAI 문헌을 정리한 서베이로 새로운 방법 제안이 없다.</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2608.26186'>Investigating the Influence of Prompt and Response Languages on LLM Content Generation</a></td><td>20</td><td>0</td><td>NLP</td><td>프롬프트·응답 언어가 LLM 출력 길이에 미치는 영향을 측정한 경험적 연구다.</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2608.26192'>Comparing Chunking and Embedding Strategies for Turkish RAG Systems</a></td><td>20</td><td>0</td><td>NLP</td><td>터키어 RAG의 chunking·embedding 전략 비교 실험으로 특정 언어 벤치마킹에 그친다.</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2608.26389'>LowRankArena: A Standardized Evaluation Platform for SVD-Based LLM Compression</a></td><td>20</td><td>0</td><td>NLP</td><td>SVD 기반 LLM 압축을 표준화 평가하는 벤치마크 플랫폼으로 경량화 위주 기여다.</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2608.26923'>TabuLM: Morphology-Aware Tabular Pre-training for Low-Resource Languages</a></td><td>20</td><td>0</td><td>NLP</td><td>키냐르완다어 표 데이터 사전학습 자원(TabuLM) 구축 논문이다.</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2608.27031'>ITL: Interpretable Document Alignment with Structured Reference Frameworks</a></td><td>20</td><td>0</td><td>NLP</td><td>구조화 참조 프레임워크와 문서 정렬을 개념 단위로 추적 가능하게 만드는 ITL 방법론이다.</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2608.27035'>Representing and Parsing Korean Constituency Structure at Different Levels of Granularity</a></td><td>20</td><td>0</td><td>NLP</td><td>한국어 구구조 분석의 표상 단위(형태소/어절)를 비교한 파싱 연구다.</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2608.27049'>Research Design Tracking and Assessment for the Social Sciences</a></td><td>20</td><td>0</td><td>NLP</td><td>사회과학 인과 연구설계 탐지·평가 과제(ARDTrA)를 정의한 응용 연구다.</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2608.27110'>DocTalkBN: A Novel Dataset of Expert Telemedicine Conversations in Bengali</a></td><td>20</td><td>0</td><td>NLP</td><td>벵골어 원격의료 대화 데이터셋(DocTalkBN) 구축 자원 논문이다.</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2608.26178'>AI Revealed Preferences</a></td><td>20</td><td>0</td><td>NLP</td><td>20개 LLM의 revealed preference(과업 선호, sycophancy 등)를 forced-choice 실험으로 측정한 연구로 alignment 함의는 있으나 robotics와는 무관하다.</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2608.27429'>Mechanistic Reaction Prediction via Discrete Flow Matching on Graph-Structured Electron Occupation</a></td><td>20</td><td>0</td><td>LG 등</td><td>화학 반응을 전자 점유 벡터에 대한 discrete flow matching(CTMC)으로 모델링해 mechanistic reaction pathway를 예측하는 연구(MAELLE)로 generative modeling 방법론은 흥미로우나 robotics와는 무관하다.</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2608.26363'>A Unified Framework for the Mechanics of Information in Convolutional Neural Network Image Space</a></td><td>18</td><td>1</td><td>CV</td><td>CNN 필터를 상대론적 에너지-운동량에 비유한 유사수학적 프레임워크로 실증적 강도가 약하다.</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2608.26989'>Decentralized Multitask Learning over Learned Task Graphs</a></td><td>18</td><td>1</td><td>LG</td><td>미지의 task graph를 학습하는 분산 멀티태스크 학습 이론 연구로 로봇 학습과의 연결은 약하다.</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2608.26382'>VIPER: An Expert-Curated Benchmark for Vision-Language Models in Veterinary Pathology</a></td><td>18</td><td>0</td><td>CV</td><td>수의병리 VLM 벤치마크로 로봇/embodied AI와 무관하다.</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2608.26531'>FAN-LoRA: A Fourier-Adaptive Nonlinear Low-Rank Adaptor for Medical Foundation Model Domain Adaptation</a></td><td>18</td><td>0</td><td>CV</td><td>SAM의 의료영상 도메인 적응을 위한 LoRA 변형으로 특정 태스크 fine-tuning 위주의 기여다.</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2608.26632'>Who Remains, What Changes: Identity Anchored Composed Gait Retrieval</a></td><td>18</td><td>0</td><td>CV</td><td>자연어 조건부 gait retrieval 새 태스크로 로봇 학습과 무관하다.</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2608.26648'>Hierarchical Channel Stacking: A Structured Decision Framework for AI-Generated Image Detection</a></td><td>18</td><td>0</td><td>CV</td><td>AI 생성 이미지 탐지를 위한 계층적 채널 표현으로 로봇 관련성이 없다.</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2608.26658'>PailitaoGR: Latent Think-with-Images for Generative Image Retrieval</a></td><td>18</td><td>0</td><td>Multimodal</td><td>전자상거래 이미지 검색을 위한 generative retrieval로 로봇 학습과 무관하다.</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2608.26713'>AesCanvas: A Large-Scale Dataset and Benchmark for Aesthetic Critique and Contextual Suitability</a></td><td>18</td><td>0</td><td>Multimodal</td><td>이미지 심미성 평가 벤치마크로 로봇 관련성이 없다.</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2608.26856'>From Reasoning to Pixels: Grounded Medical Multimodal LLMs for VQA and Segmentation</a></td><td>18</td><td>0</td><td>Multimodal</td><td>의료 MLLM의 reasoning-to-segmentation grounding 기법으로 임상 도메인에 한정된다.</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2608.27004'>MVC-Bench: Benchmarking Calibration of Medical Vision-Language Models</a></td><td>18</td><td>0</td><td>Multimodal</td><td>의료 VLM의 calibration 벤치마크로 로봇 관련성이 없다.</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2608.27066'>Beyond Classification: Task-Dependent Learnability under Privacy-Motivated Image Transformations</a></td><td>18</td><td>0</td><td>CV</td><td>프라이버시 보호 이미지 변환의 downstream task별 학습가능성 평가 프로토콜로 로봇 관련성이 없다.</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2608.27123'>EditaLive! Unified Character Video Editing for Live Streaming</a></td><td>18</td><td>0</td><td>Video</td><td>실시간 라이브 스트리밍용 캐릭터 비디오 편집 시스템으로 로봇 관련성이 없다.</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2608.27154'>ReViCo: Unveiling the Limitations of VLMs in Visual Text Understanding via Error Correction</a></td><td>18</td><td>0</td><td>Multimodal</td><td>VLM의 이미지 내 텍스트 오류 교정 벤치마크로 로봇 학습과 무관하다.</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2608.27280'>Sidecar: Training-Free Semantic Reuse for Character-Consistent Free-form Visual Storytelling</a></td><td>18</td><td>0</td><td>Video</td><td>캐릭터 일관성을 유지하는 training-free 스토리텔링 이미지 생성 모듈로 로봇 관련성이 없다.</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2608.26222'>NeuronFuzz: Safety Neuron Guided Fuzzing for LLM Safety Evaluation</a></td><td>18</td><td>0</td><td>NLP</td><td>안전 뉴런 활성화를 이용한 LLM jailbreak fuzzing 프레임워크로 로봇 관련성이 없다.</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2608.26309'>Algebraic Multigrid Acceleration for Efficient Label Spreading</a></td><td>18</td><td>0</td><td>LG</td><td>algebraic multigrid solver로 label spreading을 가속하는 준지도학습 기법으로 로봇 학습과 무관하다.</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2608.26453'>Distributed Training using an Intelligent Network</a></td><td>18</td><td>0</td><td>LG</td><td>WAN 분산학습을 위한 네트워크-알고리즘 공동설계 시스템 논문으로 로봇 관련성이 없다.</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2608.26493'>A Unified Framework for Fair and Personalized Decentralized Learning under Communication Constraints</a></td><td>18</td><td>0</td><td>LG</td><td>통신 제약 하 분산학습의 공정성·개인화 통합 프레임워크로 로봇 학습과 무관하다.</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2608.26526'>High Probability Derivative Bounds for Random tanh Neural Networks on a Hypercube</a></td><td>18</td><td>0</td><td>LG</td><td>wide tanh 신경망의 고차 미분에 대한 고확률 bound를 증명한 이론 논문으로 로봇 관련성이 낮다.</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2608.26655'>When Privacy Hurts Mergeability: Geometry-Aware Model Merging under Differential Privacy</a></td><td>18</td><td>0</td><td>LG</td><td>차등 프라이버시 하 모델 병합의 기하학적 장애를 분석한 논문으로 로봇 학습과 무관하다.</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2608.26732'>Rethinking Message Passing as Retrieval for Text-Attributed Graph Learning</a></td><td>18</td><td>0</td><td>LG</td><td>GNN 메시지 패싱을 retrieval 관점으로 재해석한 그래프 학습 연구로 embodied AI와 관련 없다.</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2608.27153'>Inductive Correlation Clustering with Graph Neural Networks</a></td><td>18</td><td>0</td><td>LG</td><td>GNN 기반 inductive correlation clustering 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2608.26130'>Agents Don&#x27;t Paginate: First-Chunk Selection for LLM Tool Responses</a></td><td>18</td><td>0</td><td>NLP</td><td>코딩 에이전트의 tool 응답 첫 청크 선택 전략을 분석한 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2608.26136'>Reward-Informed Sparse Autoencoders and the Solution-Completeness Confound</a></td><td>18</td><td>0</td><td>NLP</td><td>보상 신호로 큐레이션한 sparse autoencoder가 실제로는 reasoning quality가 아닌 solution completeness를 포착함을 보인 해석가능성 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2608.26140'>Affix Cache for Diffusion Large Language Models</a></td><td>18</td><td>0</td><td>NLP</td><td>diffusion LLM을 위한 affix 캐시 재사용 기법으로 추론 효율화 연구이며 로보틱스와 무관하다.</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2608.26146'>Vagdhenu: A Vrutta (Meter) Aware Shloka-to-Chant (TTS) System for Sanskrit</a></td><td>18</td><td>0</td><td>NLP</td><td>산스크리트 챈트 TTS 구축 경험 보고서로 저자 스스로 새 아키텍처가 아니라고 명시한다.</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2608.26148'>Towards Interpretable Depression Detection: Linking Acoustic Features to DSM-5 Indicators</a></td><td>18</td><td>0</td><td>NLP</td><td>음향 특징과 DSM-5 우울 지표를 연결하는 예비 연구로 검증이 얕다.</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2608.26154'>Evaluating AI Generated Summaries for Cancer Patients</a></td><td>18</td><td>0</td><td>NLP</td><td>암 환자용 AI 요약을 임상 전문가와 LLM judge로 평가한 응용 연구로 방법론적 novelty가 없다.</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2608.26165'>Using Poly-Encoders for Computationally Efficient Automated Creativity Assessment</a></td><td>18</td><td>0</td><td>NLP</td><td>Poly-Encoder로 창의성 평가를 경량화하는 효율화 기여로 우선순위가 낮다.</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2608.26168'>Hallucinations in LLMs: A Lifecycle-Based Survey of Causes, Detection, Mitigation, and Prevention</a></td><td>18</td><td>0</td><td>NLP</td><td>LLM 환각의 생애주기 서베이로 새 방법론이 없다.</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2608.26344'>MoganColBERT-TR: A Late-Interaction Multi-Vector Retrieval Model for Turkish</a></td><td>18</td><td>0</td><td>NLP</td><td>터키어용 late-interaction 검색 모델 학습 보고로 특정 언어 엔지니어링이다.</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2608.26700'>PragAlign: Evidence-Sensitive Reply Assistance Across Chinese and Japanese Appropriateness Judgments</a></td><td>18</td><td>0</td><td>NLP</td><td>중국어·일본어 답장 보조 시스템을 소규모 사용자 평가로 비교한 응용 연구다.</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2608.26749'>Letters hide the truth from our eyes: English homophones have meaningfully different phonetic realizations</a></td><td>18</td><td>0</td><td>NLP</td><td>영어 동음이의어의 음성학적 실현 차이를 대규모로 분석한 언어학 연구다.</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2608.26941'>KinyaEmbed: Contrastive Sentence Embeddings for Kinyarwanda via Multi-Stage Curriculum Training</a></td><td>18</td><td>0</td><td>NLP</td><td>키냐르완다어 전용 문장 임베딩 모델(KinyaEmbed) 구축 자원 논문이다.</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2608.27296'>LLMs Can Design Near-Optimal OR Algorithms</a></td><td>18</td><td>0</td><td>LG 등</td><td>재고관리·큐잉·assortment 최적화 같은 OR 문제에서 LLM이 튜닝 없이도 기존 특화 알고리즘과 경쟁력 있는 알고리즘을 설계함을 보인 연구로 robotics와는 무관하다.</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2608.26233'>Pruning Binarized Neural Networks: A Dedicated Framework and Globally Weighted Algorithms</a></td><td>16</td><td>1</td><td>LG</td><td>이진화 신경망 전용 pruning 프레임워크로 edge 배포에 유용하나 경량화 중심의 기여다.</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2608.26607'>FU-Mamba: A Frequency-Enhanced Dynamic Scanning Framework for Oralscan Image Segmentation</a></td><td>16</td><td>0</td><td>CV</td><td>구강 스캔 영상 분할을 위한 Mamba 변형으로 mIoU 1.1% 개선에 그치는 incremental 기여다.</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2608.26848'>MedFG-VQA: Low-Frequency Memory and Graph Attention for Lightweight Medical VQA</a></td><td>16</td><td>0</td><td>Multimodal</td><td>경량 의료 VQA 프레임워크로 로봇 학습과 무관하다.</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2608.26971'>TempJail: Temporal Jailbreak Attacks against Image-to-Video Generation Models</a></td><td>16</td><td>0</td><td>CV</td><td>image-to-video 생성 모델에 대한 시간적 jailbreak 공격 연구로 로봇 학습과 무관하다.</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2608.27175'>Temporal Sensitivity Analysis of Tessera Embeddings</a></td><td>16</td><td>0</td><td>CV</td><td>지구관측 foundation model 임베딩의 시간창 민감도 분석으로 로봇 관련성이 낮다.</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2608.26423'>The Latent Diagnostic Taxonomy: A Framework for Constructing Classifiers and Diagnosing Their Decisions, Applied to Prompt Injection Detection</a></td><td>16</td><td>0</td><td>NLP</td><td>prompt injection 분류기의 판단 신뢰도를 진단하는 taxonomy로 로봇 학습과 무관하다.</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2608.26433'>FedCMAPSS: A Benchmark for Federated Learning in Remaining Useful Life Estimation</a></td><td>16</td><td>0</td><td>LG</td><td>연합학습 기반 잔여수명 예측 벤치마크로 산업 PHM 응용이며 로봇 학습과 무관하다.</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2608.26594'>SimCast-S2S: An Efficient Generative Model for Subseasonal Precipitation Forecasting via Transfer Learning from Climate Simulations</a></td><td>16</td><td>0</td><td>LG</td><td>계절 내 강수 예보를 위한 latent diffusion 생성모델로 로봇 학습과 무관하다.</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2608.27343'>Pair-Level Essay-Scale Republication and Reuse from Fragmented Historical Text Reuse: A Workflow Study on Eighteenth-Century Books and Newspapers</a></td><td>16</td><td>0</td><td>NLP</td><td>18세기 텍스트 재사용 탐지를 위한 디지털인문학 워크플로 연구다.</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2608.26896'>AI agents in Algorithmic Electricity Markets: On the Emergence of Tacit Collusion</a></td><td>15</td><td>1</td><td>RL</td><td>전력시장에서 MARL 기반 입찰 에이전트들이 명시적 지시 없이 묵시적 담합에 이를 수 있음을 보인 연구로 emergent multi-agent behavior 분석이지만 로봇 도메인과는 무관하다.</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2608.27142'>GRAIN: Bridging Name and Narrative Shifts in Real-World Graph Reasoning through Invariance-Rewarded Agentic RL</a></td><td>15</td><td>1</td><td>RL</td><td>그래프 추론에서 명칭·서술 변화에 강건하도록 Structure Invariance Reward로 학습한 단일 에이전트 RL 프레임워크(GRAIN)로 RL 기법이지만 robotics와는 무관하다.</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2608.26686'>Domain-Specific Self-Supervised Representation Learning for Retinal Fundus Classification</a></td><td>15</td><td>0</td><td>CV</td><td>망막안저 영상 자기지도학습 응용으로 로봇 학습과 무관하다.</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2608.27051'>Anatomy-Guided Foundation Model Adaptation with Within-Case Prototype Supervision for Standard Plane Detection in Fetal Ultrasound Blind Sweeps</a></td><td>15</td><td>0</td><td>Multimodal</td><td>태아 초음파 표준 단면 검출 응용 논문으로 로봇 학습과 무관하다.</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2608.27190'>Unsupervised Adaptation of 3D CT Foundation Models for 3D CBCT Segmentation</a></td><td>15</td><td>0</td><td>CV</td><td>CT foundation model을 CBCT로 도메인 적응하는 의료영상 응용으로 로봇 학습과 무관하다.</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2608.26332'>Beyond Capability Benchmarks: Learning Operational Fingerprints of LLM Cloud Services from Production Incident Metadata</a></td><td>15</td><td>0</td><td>LG</td><td>LLM 클라우드 서비스의 운영 인시던트 메타데이터 기반 fingerprinting으로 MLOps 성격의 연구이며 로봇 학습과 무관하다.</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2608.26436'>NeoTriFuse: Reliability-Aware Multimodal Fusion under Missingness Heterogeneity for Neonatal Mortality Risk Prediction</a></td><td>15</td><td>0</td><td>LG</td><td>신생아 사망 위험 예측을 위한 멀티모달 융합 논문으로 로봇 학습과 무관하다.</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2608.26437'>Subgraph Filtering for Fair Graph Neural Networks</a></td><td>15</td><td>0</td><td>LG</td><td>그래프 신경망의 공정성을 위한 subgraph filtering 기법으로 로봇 관련성이 없다.</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2608.26451'>Toward Equitable Low-Carbon Mobility: Fairness-Aware Demand Prediction for Expanding Bike-Sharing Systems</a></td><td>15</td><td>0</td><td>LG</td><td>공유자전거 수요 예측의 공정성 개선 GNN으로 로봇 학습과 무관하다.</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2608.26506'>A Single Suffix to Break Them All: Basin-Aware Jailbreaks for Merged Model Families</a></td><td>15</td><td>0</td><td>NLP</td><td>병합된 모델 계열에 전이되는 jailbreak 공격 연구로 로봇 관련성이 없다.</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2608.26544'>Chart2SVG: Editable SVG Generation from Raster Chart Images</a></td><td>15</td><td>0</td><td>LG</td><td>래스터 차트를 편집 가능한 SVG로 변환하는 MLLM 응용으로 로봇 관련성이 없다.</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2608.26729'>Neural Regression with Embeddings for Numerical Attribute Prediction in Knowledge Graphs</a></td><td>15</td><td>0</td><td>LG</td><td>지식 그래프 수치 속성 예측을 위한 회귀 모델로 로봇 학습과 무관하다.</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2608.26765'>Beyond Client Averaging: A Client-Independent Second-Order Stationary-Bias Component in Stochastic SCAFFOLD</a></td><td>15</td><td>0</td><td>LG</td><td>연합학습 SCAFFOLD의 편향 분석 이론 논문으로 로봇 학습과 무관하다.</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2608.26797'>On the Indistinguishability of Human v/s AI Generated Text</a></td><td>15</td><td>0</td><td>NLP</td><td>AI 생성 텍스트와 인간 텍스트 구분 가능성에 대한 이론 분석으로 로보틱스와 무관하다.</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2608.26877'>When Is the Sharp Covariance Envelope Tight? Feature-Only Geometry for Volume-Sampled Least Squares</a></td><td>15</td><td>0</td><td>LG</td><td>volume sampling 최소자승법의 공분산 이론 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2608.26964'>Graph-Based Pseudo-multimodal Contrastive Learning for 12-Lead ECG Representations</a></td><td>15</td><td>0</td><td>CV</td><td>12-lead ECG 표현학습을 위한 그래프 기반 contrastive learning으로 의료 응용이며 로보틱스와 무관하다.</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2608.26992'>Benchmarking_Fast_Domain_Adaptation_for_Unsupervised_Speech_Units</a></td><td>15</td><td>0</td><td>NLP</td><td>악센트별 음성 표현 학습의 빠른 도메인 적응 벤치마크로 로보틱스와 무관하다.</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2608.27122'>Cone Extended Rayleigh Quotients for Directed Graph Learning: Minimax Spectral Certificates, Sensitivity, and Adaptive Control</a></td><td>15</td><td>0</td><td>LG</td><td>방향 그래프 학습을 위한 스펙트럼 인증 이론 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2608.27124'>TRACE-CRC: Trajectory-Adaptive Conformal Risk Control for Multi-Step Channel State Information Prediction</a></td><td>15</td><td>0</td><td>LG</td><td>무선 채널 상태 정보 예측의 conformal risk control 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2608.27187'>When Interference Graphs Evolve: Doubly Robust Estimation of Dynamic Peer Effects</a></td><td>15</td><td>0</td><td>LG</td><td>변화하는 상호작용 그래프에서 동적 peer effect를 추정하는 인과추론 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2608.27203'>Common Geodesics Do Not Guarantee Fisher Consistency of the Structured SVM: Minimal Counterexamples and a Tree-Metric Classification</a></td><td>15</td><td>0</td><td>LG</td><td>structured SVM의 Fisher consistency 이론 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2608.27241'>Importance Scoring of Transformer Attention Heads in Learning Tabular Data</a></td><td>15</td><td>0</td><td>LG</td><td>tabular 데이터 학습에서 transformer attention head 중요도를 분석한 해석가능성 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2608.27302'>QuantumBoostNet: A Hybrid Classical-Quantum Architecture for Enhanced Accuracy in Cardiac Ultrasound View Identification</a></td><td>15</td><td>0</td><td>CV</td><td>심장 초음파 뷰 식별을 위한 고전-양자 하이브리드 모델로 의료영상 응용이며 로보틱스와 무관하다.</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2608.26118'>ElementCheck: Complexity-Aware Long-Form Text Factuality Evaluation via Sentence Elements</a></td><td>15</td><td>0</td><td>NLP</td><td>장문 사실성 평가를 문장 요소 단위로 수행하는 ElementCheck으로 로보틱스와 무관하다.</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2608.26119'>DeflectBench: A Benchmark for Evaluating Rhetorical Fallacy Generation in LLMs</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM의 수사적 오류 생성 능력을 평가하는 DeflectBench로 로보틱스와 무관하다.</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2608.26124'>Natural-Language Policies to Executable Decisions: An Interpretable Large Language Model Framework</a></td><td>15</td><td>0</td><td>NLP</td><td>관광 가격 정책을 실행가능한 결정으로 변환하는 산업용 LLM 시스템으로 로보틱스와 무관하다.</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2608.26126'>TelecomGPT-R1: A Unified Open-Source Reasoner for the Telecom Stack</a></td><td>15</td><td>0</td><td>NLP</td><td>통신 도메인 특화 reasoning LLM인 TelecomGPT-R1으로 로보틱스와 무관하다.</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2608.26129'>FIRSTPASS: A Multi-Domain, Multi-Round Peer Review Dataset Grounded in Real Editorial Outcomes</a></td><td>15</td><td>0</td><td>NLP</td><td>다분야 동료평가 대화를 담은 FIRSTPASS 데이터셋 논문으로 로보틱스와 무관하다.</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2608.26131'>Evaluating Language Models in Realistic Conversational Contexts</a></td><td>15</td><td>0</td><td>NLP</td><td>인간 규모 대화 평가를 위한 UPHELD 벤치마크로 로보틱스와 무관하다.</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2608.26133'>Agent Seer: Synthesizing Scenarios from Specification Understanding</a></td><td>15</td><td>0</td><td>NLP</td><td>MCP 명세로부터 평가 시나리오를 자동 생성하는 Agent Seer로 로보틱스와 무관하다.</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2608.26111'>Large Models for Battery Prognostics and Health Management: A Review and Future Roadmap</a></td><td>15</td><td>0</td><td>LG 등</td><td>배터리 건강관리(BPHM)에 대한 Large Model 적용 서베이로 robotics와 무관하다.</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2608.26113'>PICasso: An AI-Enabled Design Framework for Autonomous Optimization of Silicon Photonic Devices</a></td><td>15</td><td>0</td><td>LG 등</td><td>자연어 명세로부터 광집적회로를 설계하는 AI 프레임워크로 robot learning과 관련이 없다.</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2608.26149'>Methodological and Conceptual Framework for 5D Multi-Table Analysis: A Unified Approach for Complex Data Reuse</a></td><td>15</td><td>0</td><td>LG 등</td><td>relational database를 hypergraph로 표현해 학습하는 아키텍처(RHT)로 헬스케어 EHR 도메인이며 robotics와 무관하다.</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2608.26167'>Refusal Is Not Robustness: Auditing Confident Fabrication in Large Language Models on a Provably Uninformative Clinical Pain Speech Transcript</a></td><td>15</td><td>0</td><td>NLP</td><td>lexical pain 정보가 없는 clinical speech transcript에서 LLM의 confident fabrication을 감사한 연구로 hallucination 평가 방법론은 흥미로우나 robotics와는 무관하다.</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2608.26199'>Benchmarking AI Agents for Hardware Design Automation via MCP Tool Calling</a></td><td>15</td><td>0</td><td>LG 등</td><td>로컬 LLM 에이전트로 하드웨어 설계 tool-calling workflow를 자동화하는 벤치마크로 robotics와 무관하다.</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2608.26730'>Knowing When Not to Reuse: Conditional Experience Transfer in Autonomous LLM Post-Training</a></td><td>15</td><td>0</td><td>LG 등</td><td>자율 LLM post-training에서 과거 update 경험의 재사용 여부를 판단하는 방법(BCIT)으로 robotics와 무관하다.</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2608.27167'>Calibrated Enough to Know, Not Calibrated to Act: Fabricated Evidence Makes LLM Agents Commit to the Unknowable</a></td><td>15</td><td>0</td><td>NLP</td><td>권위 있어 보이는 market panel 형식이 답할 수 없는 질문에도 LLM agent의 confident commitment를 유발함을 보인 연구로 agent reliability 평가 방법론은 흥미로우나 robotics와는 무관하다.</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2608.26471'>Mapping Woody Vegetation from Multi-Source Imagery and Prediction Fusion for Enhanced Data Efficiency and Accuracy</a></td><td>14</td><td>0</td><td>CV</td><td>원격탐사 수목 피복 매핑 응용 논문으로 로봇 학습과 관련 없다.</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2608.26489'>Learning Woody Clearing With Loss Alignment for Zero-Shot Regrowth and Woody Segmentation</a></td><td>14</td><td>0</td><td>CV</td><td>위성영상 기반 수목 벌채/재생 탐지로 로봇 학습과 무관한 원격탐사 응용이다.</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2608.26500'>Systematic Literature Review of Machine Learning Models and Applications for Text Recognition</a></td><td>14</td><td>0</td><td>CV</td><td>OCR 분야 체계적 문헌리뷰로 새로운 방법 제안이 없다.</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2608.26647'>Tissue-Mixture Entropy-Weighted Reconstruction for Partial-Volume-Aware Brain MRI Super-Resolution</a></td><td>14</td><td>0</td><td>CV</td><td>뇌 MRI super-resolution 의료영상 논문으로 로봇 학습과 무관하다.</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2608.26771'>Cross-Architecture Knowledge Distillation from a Vision Foundation Model to a Lightweight Visual State Space Model for Tea Leaf Disease Classification</a></td><td>14</td><td>0</td><td>CV</td><td>차잎 질병 분류를 위한 경량 distillation 응용 논문으로 로봇 학습과 무관하다.</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2608.26861'>FIDA: Feature Instability-Driven Attack on Self-Supervised Facial Representation</a></td><td>14</td><td>0</td><td>CV</td><td>얼굴 SSL 표현에 대한 backdoor 공격 연구로 로봇 학습과 무관하다.</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2608.26866'>Order Matters: A Chinese Multi-Panel Meme Benchmark for Vision-Language Reasoning</a></td><td>14</td><td>0</td><td>Multimodal</td><td>중국어 다중 패널 밈 이해 벤치마크로 로봇 관련성이 없다.</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2608.27034'>Differentiable Jitter Correction using Deep Learning-based Image Quality Metric for Phase-Contrast Micro-CT</a></td><td>14</td><td>0</td><td>CV</td><td>위상대비 마이크로 CT의 jitter 보정 기법으로 로봇 학습과 무관한 의료영상 응용이다.</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2608.27095'>Automated 2D and 3D Segmentation of AMD and DME Lesions in OCT</a></td><td>14</td><td>0</td><td>CV</td><td>OCT 기반 망막 병변 분할 응용 논문으로 로봇 학습과 무관하다.</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2608.27169'>Ancient-Bench: A Comprehensive Multi-millennial, Multi-medium, and Multi-script Benchmark for Ancient Chinese Artifact Text Recognition</a></td><td>14</td><td>0</td><td>CV</td><td>고대 중국 유물 문자 인식 벤치마크로 로봇 학습과 무관하다.</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2608.27178'>Parameter-Efficient pretrained-CT-to-MRI Transfer for Rectal Cancer Segmentation: Performance-Calibration Trade-offs</a></td><td>14</td><td>0</td><td>CV</td><td>직장암 MRI 분할을 위한 CT-to-MRI 파라미터 효율적 전이 학습으로 로봇 학습과 무관하다.</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2608.27240'>UniFLM: United Segmentation and Measurement on Fetal Limb Ultrasonic Image</a></td><td>14</td><td>0</td><td>CV</td><td>태아 사지 초음파 분할·측정 응용 논문으로 로봇 학습과 무관하다.</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2608.26538'>Predicting Quantifiability from Primary Screens to Prioritize Dose-Response Profiling</a></td><td>14</td><td>0</td><td>LG</td><td>신약 스크리닝의 정량화 가능성을 예측하는 triage 모델로 로봇 학습과 무관하다.</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2608.26613'>Technical Comparative Benchmarking Study: Advanced AI Hybrid Methods for Renewable Energy Farm Optimization and Forecasting</a></td><td>14</td><td>0</td><td>LG</td><td>재생에너지 발전 최적화·예측을 위한 AI 방법 비교 벤치마크로 로봇 관련성이 없다.</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2608.26921'>AraMS-28k: The Largest Publicly Released Line-Level Dataset of Historical Arabic Manuscripts with Margin and Insertion-Anchor Annotations</a></td><td>12</td><td>0</td><td>NLP</td><td>역사적 아랍어 필사본 라인 단위 데이터셋으로 로봇 학습과 무관하다.</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2608.26998'>Virtual iEEG from Scalp EEG: Charting the Landscape of Source Imaging, Intracranial Inference and Reconstruction</a></td><td>12</td><td>0</td><td>CV</td><td>두피 EEG로부터 iEEG를 추론하는 뇌과학 리뷰 논문으로 로봇 학습과 무관하다.</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2608.27290'>Detection of Christmas tree plantations from high-resolution aerial imagery. A case study in the French Morvan</a></td><td>12</td><td>0</td><td>CV</td><td>크리스마스 트리 농장 탐지를 위한 원격탐사 응용 논문으로 로봇 학습과 무관하다.</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2608.27076'>Tabular Deep Learning for Algorithmic Trading: Cross-Regime Bayesian Optimisation for Equity Signal Generation</a></td><td>12</td><td>0</td><td>LG</td><td>주식 트레이딩을 위한 tabular 딥러닝 베이지안 최적화 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2608.27205'>Profit based evaluation of machine learning for nitrogen recommendations in winter wheat</a></td><td>12</td><td>0</td><td>LG</td><td>밀 질소 시비 추천을 위한 ML 평가 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2608.26123'>Which India Survives Translation? Narrative Homogenisation Across Indian Oral Traditions in LLMs</a></td><td>12</td><td>0</td><td>NLP</td><td>인도 지역 구전 전통이 LLM 번역에서 균질화되는 현상을 분석한 문화 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2608.26125'>Training-Time Explainability for Multilingual Hate Speech Detection: Aligning Model Reasoning with Human Rationales</a></td><td>12</td><td>0</td><td>NLP</td><td>다국어 혐오발언 탐지를 위한 학습 시점 설명가능성 프레임워크로 로보틱스와 무관하다.</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2608.26138'>Cross-Platform Generalisation Failure in Mental Health Natural Language Processing: A Five-Axis Fairness Audit of Transformer Models on Social Media</a></td><td>12</td><td>0</td><td>NLP</td><td>정신건강 NLP 모델의 플랫폼 간 일반화 실패를 감사한 공정성 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2608.26114'>CIFQA: A Deterministic Tool-Grounded Multi-Agent LLM Framework for Financial Query Answering</a></td><td>12</td><td>0</td><td>NLP</td><td>금융 계산 QA를 위한 tool-grounded multi-agent LLM 프레임워크로 robotics 관련성이 낮다.</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2608.26134'>The Accuracy-Efficiency Paradox Quantifying Net Energy Loss in on-Device Energy Forecasting</a></td><td>12</td><td>0</td><td>LG 등</td><td>on-device 에너지 예측의 정확도-효율 trade-off를 다루는 TCO 프레임워크로 robotics와 무관하다.</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2608.26157'>GROUND: Reducing Hallucinations in LLM-Based Enterprise Analytics Through Governed Semantic Definitions</a></td><td>12</td><td>0</td><td>NLP</td><td>거버넌스된 semantic layer로 기업 analytics LLM의 hallucination을 억제하는 프레임워크(GROUND)로 robotics와 무관하다.</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2608.26176'>Knowledge Cards: Structured Knowledge for AI Systems</a></td><td>12</td><td>0</td><td>LG 등</td><td>AI 시스템이 사용하는 지식을 구조화해 문서화하는 Knowledge Card 아티팩트 제안으로 robotics와 무관하다.</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2608.26188'>Is Your Neighborhood Safe? Place-based Stigma in Large Language Models&#x27; Urban Safety Judgments</a></td><td>12</td><td>0</td><td>NLP</td><td>LLM의 도시 안전 판단에서 지명이 유발하는 place-based stigma를 분석한 연구로 robotics와 무관하다.</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2608.26191'>Structured Evidence Routing for Incident Risk Prediction from Multimodal Longitudinal EHRs</a></td><td>12</td><td>0</td><td>LG 등</td><td>multimodal longitudinal EHR에서 incident risk를 예측하는 router-predictor-reviewer 워크플로우로 robotics와 무관하다.</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2608.26218'>Same Model, Different Harness: Different Coding-Agent Results</a></td><td>12</td><td>0</td><td>LG 등</td><td>동일 모델이라도 context 관리 harness에 따라 coding-agent 성능이 크게 달라짐을 보인 연구로 robotics와 무관하다.</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2608.26235'>The Reasoning Tax: Token Economics of LLM Reasoning Across Task Types and Deployment Contexts</a></td><td>12</td><td>0</td><td>LG 등</td><td>reasoning token 사용의 비용 대비 정확도 효율(TES)을 정량화한 벤치마킹 연구로 robotics와 무관하다.</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2608.26430'>Fine-Tuning of Transformer models with Frames</a></td><td>12</td><td>0</td><td>LG 등</td><td>Fusion Frame 기반 sparse coefficient로 LoRA보다 메모리 효율적인 PEFT(FrameFT)를 제안한 연구로 robotics와 무관하다.</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2608.26546'>DuMateBench: Evaluating Autonomous Agents in Complex Real-World Workflows</a></td><td>12</td><td>0</td><td>LG 등</td><td>실제 production agent 세션을 재구성한 real-world workflow 벤치마크(DuMateBench)로 robotics와 무관하다.</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2608.27147'>Thomson: Continual Learning of Frontier Models for SovereignAI</a></td><td>12</td><td>0</td><td>NLP</td><td>오픈웨이트 모델의 continual learning으로 sovereign 프론티어 모델(Thomson)을 구축하는 연구로 robotics와 무관하다.</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2608.26137'>Interpretable, Fairly Evaluated Automated L2 Speaking Assessment that Beats the Single-Human Ceiling and Why Pause Encoding Does Not Change LLM Fluency Scores</a></td><td>10</td><td>0</td><td>NLP</td><td>L2 영어 스피킹 자동 평가 시스템 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2608.26145'>LLMs for Academic Workflows: An Evaluation of Literature Reviews Generated with Short and Long Context Windows of LLMs</a></td><td>10</td><td>0</td><td>NLP</td><td>short/long context window에 따른 LLM 문헌 리뷰 품질을 평가한 연구로 robotics와 무관하다.</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2608.26150'>Leveraging Large Language Models for Systematic Literature Review of Disease Spread Models</a></td><td>10</td><td>0</td><td>NLP</td><td>LLM으로 감염병 확산 모델 문헌을 체계적으로 정리한 연구로 robotics와 무관하다.</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2608.26153'>EEG-to-Report: An Annotation and Feature-Text Framework for Training Language Models on Clinical EEG</a></td><td>10</td><td>0</td><td>Multimodal</td><td>임상 EEG 주석 및 리포트 생성용 feature-text 프레임워크로 robotics와 무관하다.</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2608.26160'>SAREF-based Ontology for Distributed AI Workflows across the Edge-Fog-Cloud Continuum</a></td><td>10</td><td>0</td><td>LG 등</td><td>edge-fog-cloud 분산 AI workflow를 위한 SAREF 기반 온톨로지로 robotics와 무관하다.</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2608.26162'>A Safety-Gated Multimodal AI Backend for Mental-Health Support: Hierarchical State Representation, Conservative Risk Fusion, and Controlled Generation in Anian</a></td><td>10</td><td>0</td><td>Multimodal</td><td>산모 정신건강 지원을 위한 safety-gated multimodal AI backend로 robotics와 무관하다.</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2608.26164'>A Task-Centric Ontology and Deterministic Domain Rules as a Verifiable Core for AI-Assisted Chemistry Problem Solving</a></td><td>10</td><td>0</td><td>LG 등</td><td>학교 수준 화학 문제풀이를 위한 task-centric 온톨로지와 결정론적 규칙 엔진으로 robotics와 무관하다.</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2608.26184'>TutorTrace: A Dataset and Taxonomy for Classifying Learner Behavioral States during AI-Assisted Programming Education</a></td><td>10</td><td>0</td><td>LG 등</td><td>AI 보조 프로그래밍 교육에서 학습자 행동 상태를 분류하는 데이터셋·분류체계로 robotics와 무관하다.</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2608.26225'>Agent Mesh: Reliability Primitives for Non-Idempotent Agent Delegation - Identity Adequacy and Evidence Adequacy</a></td><td>10</td><td>0</td><td>LG 등</td><td>production agentic 소프트웨어 배포 플랫폼의 실패 사례 분석과 reliability primitive 제안으로 robotics와 무관하다.</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2608.26226'>LLM Agents for Time-Series: A Survey</a></td><td>10</td><td>0</td><td>NLP</td><td>시계열 문제를 다루는 LLM agent에 대한 서베이로 robotics와 무관하다.</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2608.26236'>6.5% of the Neuro-Symbolic Literature Can Be Reproduced from Its Published Artifacts, a Six-Stage Audit Framework and First Instantiation</a></td><td>10</td><td>0</td><td>LG 등</td><td>neuro-symbolic AI 문헌의 재현성을 감사해 6.52%만 재현 가능함을 보인 연구로 robotics와 무관하다.</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2608.26310'>FaithSieve: Fine-Grained Evaluation of Math Proofs with Faithful Formal Evidence</a></td><td>10</td><td>0</td><td>LG 등</td><td>Lean 기반으로 자연어 수학 증명의 첫 오류 위치를 정밀 평가하는 프레임워크(FaithSieve)로 robotics와 무관하다.</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2608.26334'>ProofEvolve: Neuro-Symbolic Evolution for Formal Automated Theorem Proving</a></td><td>10</td><td>0</td><td>LG 등</td><td>신경-기호 진화로 형식 정리증명을 개선하는 프레임워크(ProofEvolve)로 robotics와 무관하다.</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2608.26535'>Multi2AV-Safety: Benchmarking Safety in Multimodal-to-Audio-Video Generation</a></td><td>10</td><td>0</td><td>Video</td><td>multimodal 조건부 오디오-비디오 생성의 compositional safety risk를 다루는 벤치마크로 robotics와 무관하다.</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2608.26623'>AgentJudgeBench: A Multi-Difficulty Benchmark for Evaluating LLM Judges on Agentic Tool-Calling</a></td><td>10</td><td>0</td><td>LG 등</td><td>agentic tool-calling에 대한 LLM judge의 신뢰성을 평가하는 벤치마크로 robotics와 무관하다.</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2608.26696'>Five Primitives for Governing Autonomous AI Agents at Runtime</a></td><td>10</td><td>0</td><td>LG 등</td><td>런타임에서 자율 AI agent를 거버넌스하기 위한 5가지 원칙을 제안한 연구로 robotics와 무관하다.</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2608.26710'>Style as a Confound: False Positives in AI Detection of Non-Native Academic Writing</a></td><td>10</td><td>0</td><td>NLP</td><td>전문 편집이 AI 텍스트 탐지기의 false positive에 미치는 영향을 대규모로 분석한 연구로 robotics와 무관하다.</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2608.26757'>DEEPCHART: How Far are LLMs from Faithful Data-Science Chart Generation?</a></td><td>10</td><td>0</td><td>Multimodal</td><td>LLM의 데이터 사이언스 차트 생성 충실도를 평가하는 벤치마크(DEEPCHART)로 robotics와 무관하다.</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2608.26836'>SymbolLKG: Towards Verifiable Logical Reasoning via Logical Knowledge Graph and Symbolic Solvers</a></td><td>10</td><td>0</td><td>NLP</td><td>logical knowledge graph와 symbolic solver로 LLM 다단계 추론을 검증하는 프레임워크(SymbolLKG)로 robotics와 무관하다.</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2608.26867'>BekchiAI: Measuring, Observing, and Controlling LLM Agents in One Click</a></td><td>10</td><td>0</td><td>LG 등</td><td>LLM agent의 agentic skill을 측정·관제하는 벤치마크 및 플랫폼(BekchiAI)으로 robotics와 무관하다.</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2608.26889'>Learning-Augmented Online Allocation under Unreliable Advice: Robustness, Exposure Fairness, and Distribution Shift</a></td><td>10</td><td>0</td><td>LG 등</td><td>신뢰할 수 없는 조언 하에서의 learning-augmented online allocation 이론 연구로 robotics와 무관하다.</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2608.26949'>A Table Is Worth 64 Tokens: Pixel-level Compression for Multi-Table Document Question Answering</a></td><td>10</td><td>0</td><td>Multimodal</td><td>표를 이미지로 압축해 처리하는 multi-table 문서 QA 방법으로 robotics와 무관하다.</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2608.26950'>From Atomic to Agentic: Towards Interpretable Evaluation of LLMs&#x27; Agentic Mathematical Capabilities</a></td><td>10</td><td>0</td><td>NLP</td><td>LLM의 agentic 수학 능력을 process-level로 평가하는 벤치마크로 robotics와 무관하다.</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2608.27010'>A Multi-Modal AI Framework for Real-Time Queue Prediction, Management and Optimisation in Intelligent Border Control Systems</a></td><td>10</td><td>0</td><td>LG 등</td><td>국경관리 대기열 예측·최적화를 위한 multimodal AI 프레임워크로 robotics와 무관하다.</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2608.27086'>A Contract-Centered Architecture for Scalable and Manageable Agentic Runtimes</a></td><td>10</td><td>0</td><td>LG 등</td><td>agentic runtime 거버넌스를 위한 계약 기반 아키텍처 제안으로, 구현·실험·데이터 없이 개념만 제시했으며 robotics와 무관하다.</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2608.27102'>LAAF: A Layered Accountability Architecture Framework for LLM Applications</a></td><td>10</td><td>0</td><td>LG 등</td><td>LLM 응용의 책임소재를 다루는 계층적 accountability 프레임워크(LAAF) 서베이로 robotics와 무관하다.</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2608.27146'>When Tool Outputs Become Commands: Separating Action Induction from Runtime Authorization in Tool-Augmented LLM Agents</a></td><td>10</td><td>0</td><td>LG 등</td><td>tool 출력이 명령으로 오용되는 것을 방지하기 위해 action induction과 실행 권한을 분리하는 방법(SARA)으로 robotics와 무관하다.</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2608.27266'>Naive Prompt Optimization: Rethinking the Need for Complex Prompt Search</a></td><td>10</td><td>0</td><td>NLP</td><td>단순한 single-lineage prompt 개정이 복잡한 prompt search(GEPA)와 견줄 만함을 보인 연구로 robotics와 무관하다.</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2608.27311'>Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification</a></td><td>10</td><td>0</td><td>LG 등</td><td>agent harness 진화를 위한 behavior-aware verification 프레임워크(HarnessLens)로 robotics와 무관하다.</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2608.27340'>Not All Eval-Awareness Is Equal: Capabilities Framing Predicts Compliance</a></td><td>10</td><td>0</td><td>NLP</td><td>LLM의 eval-awareness가 capability-framing인지 safety-framing인지에 따라 compliance가 달라짐을 보인 해석가능성 연구로 robotics와 무관하다.</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2608.26970'>TEMPLAR Wales: A georeferenced environmental and toponymic dataset of Welsh settlements</a></td><td>8</td><td>0</td><td>NLP</td><td>웨일스 지명 환경 데이터셋 구축 논문으로 로보틱스와 전혀 무관하다.</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2608.26978'>Terrain signatures in Welsh settlement names</a></td><td>8</td><td>0</td><td>NLP</td><td>웨일스 지명과 지형 간 상관관계를 분석한 언어지리학 연구로 로보틱스와 무관하다.</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2608.26135'>Data Science Approaches to Evaluating Honours Candidates</a></td><td>8</td><td>0</td><td>NLP</td><td>OSINT 기반 공인 평판 감성 분석 파이프라인으로 로보틱스와 무관하다.</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2608.26151'>Explainable Artificial Intelligence for Customer Churn Prediction in Telecommunications: A Framework for CRM Integration</a></td><td>8</td><td>0</td><td>LG 등</td><td>통신사 고객이탈 예측 XAI 및 CRM 통합 프레임워크로 robotics와 무관하다.</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2608.26156'>Selection Bias Correction in Retail Intelligence</a></td><td>8</td><td>0</td><td>LG 등</td><td>소매 물가지표의 long-tail selection bias 보정 방법을 비교한 시뮬레이션 연구로 robotics와 무관하다.</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2608.26185'>Can You Say This for Me? Speaking Up by Proxy in Co-Located Discussion</a></td><td>8</td><td>0</td><td>LG 등</td><td>co-located 토론에서 발언을 embodied proxy로 대신 전달하는 mixed-reality 시스템으로 robotics와 무관하다.</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2608.26694'>Relational Over-Regularization: Graph-Based AI-Generated Text Detection via Sentence Transition Deviation</a></td><td>8</td><td>0</td><td>NLP</td><td>문장 전이 분산 신호로 AI 생성 텍스트를 탐지하는 그래프 기반 방법(CSFG)으로 robotics와 무관하다.</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2608.26743'>Graph-Guided Selective Unlearning for Language Models: Controlling Support Routes Beyond Forget Seeds</a></td><td>8</td><td>0</td><td>NLP</td><td>forget seed를 넘어 지식 전파 경로까지 제거하는 그래프 기반 selective unlearning(GRAPHSU)으로 robotics와 무관하다.</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2608.26750'>Discovering Relationships in Data Lakes Using Large Language Models: An Industrial Case</a></td><td>8</td><td>0</td><td>NLP</td><td>데이터 레이크에서 LLM으로 컬럼 관계를 발견하는 산업 사례 연구(ColRel)로 robotics와 무관하다.</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2608.26849'>LiveSim: Simulating Environment-Shaped Users in Multi-Agent Live-Stream Ecosystems</a></td><td>8</td><td>0</td><td>LG 등</td><td>라이브 스트리밍 생태계의 사용자 행동을 LLM으로 시뮬레이션하는 프레임워크(LiveSim)로 robotics와 무관하다.</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2608.26870'>C-Unseen: Weak Signal Detection in Dynamic Temporal Knowledge Graphs via LLM Reasoning</a></td><td>8</td><td>0</td><td>NLP</td><td>동적 시간적 지식그래프에서 LLM 추론으로 weak signal을 탐지하는 프레임워크로 robotics와 무관하다.</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2608.26885'>Evaluating human and LLM screening workflows in a conceptually complex scoping review: Recall--workload trade-offs and run-to-run consistency</a></td><td>8</td><td>0</td><td>NLP</td><td>scoping review에서 인간과 LLM 스크리닝의 recall-workload trade-off를 비교한 연구로 robotics와 무관하다.</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2608.26899'>Counterfactual Bias Testing for Application Tracking System</a></td><td>8</td><td>0</td><td>LG 등</td><td>채용 매칭 시스템의 인구통계학적 편향을 counterfactual audit로 검증하는 방법론으로 robotics와 무관하다.</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2608.26990'>DSA: Evidence-Aware LLM-Agent Orchestration for Multi-Market Stock Research</a></td><td>8</td><td>0</td><td>LG 등</td><td>다중 시장 주식 리서치를 위한 evidence-aware LLM agent orchestration(DSA)으로 robotics와 무관하다.</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2608.27101'>pro-team at LLMs4OL 2026 Tasks Flagship and Reuse: Retrieval-Augmented Generation and Vocabulary-Constrained Filtering for Ontology Learning</a></td><td>8</td><td>0</td><td>NLP</td><td>온톨로지 학습 챌린지(LLMs4OL 2026)에 RAG와 vocabulary-constrained filtering으로 참가한 시스템 기술서로 robotics와 무관하다.</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2608.27127'>TransMeme: A Multi-Agent Framework for Cross-Cultural Meme Transcreation</a></td><td>8</td><td>0</td><td>Multimodal</td><td>밈의 문화 간 transcreation을 위한 multi-agent 프레임워크(TransMeme)로 robotics와 무관하다.</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2608.27144'>Feature Transformation Enhanced Jacobi Polynomial Graph Filtering for Graph Anomaly Detection</a></td><td>8</td><td>0</td><td>CV</td><td>Jacobi 다항식 기반 그래프 필터링으로 그래프 이상 탐지를 개선한 방법으로 robotics와 무관하다.</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2608.27268'>BrailleBench: Investigating Multi-Criteria Braille Comprehension in Large Language Models</a></td><td>8</td><td>0</td><td>NLP</td><td>점자 이해에 대한 LLM 성능을 평가하는 벤치마크(BrailleBench)로 robotics와 무관하다.</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2608.27391'>CorporateBench: Large-Scale Q&amp;A Benchmarking with Temporal Knowledge Bases</a></td><td>8</td><td>0</td><td>NLP</td><td>대규모 기업 문서에 대한 temporal knowledge base QA 벤치마크(CorporateBench)로 robotics와 무관하다.</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2608.27421'>Learning a Continuous Sepsis Severity Score Without Hour-by-Hour Supervision: A Two-Site Retrospective Study</a></td><td>8</td><td>0</td><td>LG 등</td><td>시간 단위 감독 없이 연속적인 패혈증 중증도 점수를 학습한 임상 연구로 robotics와 무관하다.</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2608.27149'>BPMN4CAI: A BPMN Extension for Modeling Dynamic Conversational AI</a></td><td>5</td><td>0</td><td>LG 등</td><td>동적 대화형 AI를 표현하기 위한 BPMN 확장 표기법 제안으로 robotics와 무관하다.</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2608.27364'>Sophistication in GenAI Use: Field Evidence from a Large Firm</a></td><td>5</td><td>0</td><td>LG 등</td><td>대기업 back-office 직원의 생성형 AI 사용 정교함을 현장 데이터로 분석한 경제학 연구로 robotics와 무관하다.</td></tr>
</tbody></table>

</details>
