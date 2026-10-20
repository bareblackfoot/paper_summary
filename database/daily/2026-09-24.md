# 오늘의 arXiv Top 15 — 2026-09-24 (목)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**
> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)

**신규 논문 수: 전체 444편 → 중복 제거 후 444편 (이번 평가 대상 444편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 106 |
| cs.LG | 115 |
| cs.RO | 91 |
| cs.CL | 73 |
| cs.AI | 59 |

*1차 스크리닝: 전체 444편을 제목/초록 기반으로 채점(Claude (scheduled agent)) → 상위 15편은 arXiv 원문을 내려받아 정밀 리뷰(Claude (scheduled agent)) 후 최종 점수 산정.*

---

## Top 15

### 1. [82점] Latent evolving World Action Model

- **분야**: World Model / VLA Manipulation · **robotics relevance**: 9/10
- **arXiv**: [2609.27455](https://arxiv.org/abs/2609.27455) ([PDF](https://arxiv.org/pdf/2609.27455))
- **저자**: Xueji Fang, Boqiang Duan, Hua Wu, Jingdong Wang, Guo-Jun Qi
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 65점

> 💡 VAE와 video diffusion backbone 대신 frozen I-JEPA embedding 위에서 action 생성과 미래 상태 예측을 한 predictor로 같이 학습하는 LeWAM을 제안함. 0.4B 파라미터, embodied pretraining 없이 RoboTwin 2.0 평균 성공률 92.28%로 기존 대형 VLA·WAM과 맞먹거나 앞서고 real robot에서도 검증함.

**Core innovation & methodology**

- VDM 기반 WAM은 observation을 VAE로 압축한 뒤 video diffusion backbone으로 특징을 뽑는데, 이 압축이 action 예측에 필요한 정보를 잃는다는 것을 이론적으로 보임 (action relevance gap, VAE posterior mean의 spectral compression)
- 대안으로 frozen I-JEPA embedding을 관측 표현으로 그대로 쓰고, action denoising(flow matching)과 미래 embedding 예측(world modeling)을 구조화된 attention mask로 하나의 predictor에서 같이 학습하는 LeWAM을 제안함. 추론 시에는 future query와 demonstrated action을 빼서 action만 생성하므로 video diffusion backbone이 필요 없음
- AdaFuse: JEPA encoder의 여러 layer 표현을 feature dimension별로 다른 가중치로 합쳐 씀. 단일 layer보다 depth·segmentation probing 성능이 좋아짐
- DemoDPO: online RL이나 사람 피드백 없이, frozen reference policy가 뽑은 후보 action들을 demonstration과의 MSE로 승/패로 나눠 offline DPO로 policy를 재조정함. imitation learning이 demonstration은 맞히지만 좋은 action과 나쁜 action을 구분 못 한다는 문제를 겨냥함

**Novelty vs. prior works**

- 가장 가까운 LaWAM(DINOv3 기반 latent action + 별도 world model + subgoal 조건 action expert)과 VLA-JEPA(V-JEPA2를 world model supervision에만 쓰고 action은 VLM 표현에서 생성)와 달리, LeWAM은 JEPA embedding을 action 생성의 직접 입력이자 미래 예측 타겟 둘 다로 쓰고 단일 predictor로 학습함. 추론 시 future prediction을 완전히 제거해 별도 subgoal decode 단계가 없음
- encoder 비교 자체의 기여도 있음. 기존 연구는 VAE·SigLIP·DINOv3·V-JEPA2 등을 서로 다른 setting에서 봤거나 VLA feature에 추가하는 형태였는데, 이 논문은 동일 action predictor·학습 레시피로 통제 비교함
- DemoDPO는 Diffusion-DPO/Flow-DPO를 offline demonstration 기반 랭킹으로 재구성한 것이라 알고리즘 자체의 이론적 참신성은 제한적임. preference label을 사람·reward 없이 demonstration MSE로 대체한 실용적 조합에 가까움

**Benchmark results**

- RoboTwin 2.0 50 task 평균 성공률 92.28%(clean 93.14%, randomized 91.42%), trainable parameter 0.4B로 π0.5(3B), Fast-WAM(6B), LingBot-VA(5B), LaWAM(1.7B) 대비 비슷하거나 근소 우위
- encoder 비교(같은 action predictor 기준)에서 Wan2.2 VAE 10.81%로 최저, I-JEPA-Huge 86.17%로 최고, AdaFuse 추가 시 86.88%
- ablation: Action Only 86.17% → future embedding direct prediction 87.02%(flow matching 방식은 86.21%로 더 낮음) → future embedding 예측 위에 AdaFuse 추가 시 90.69% → +DemoDPO(최종 LeWAM) 92.28%로 단계적 개선
- DemoDPO는 8개 도전적 task subset에서 73.31% → 76.63%로 개선했고, 같은 step 수만큼 추가 supervised 학습만 하면 73.25%로 오히려 소폭 하락해 개선이 단순 추가 학습 효과가 아님을 확인함
- real-world 3 task(블록 쌓기, 수건 접기, 꽃 꽂기)에서 task progress 84.9%/60.7%/53.0%로 π0.5·LingBot-VLA-v2·FastWAM보다 높음. 단 task 3개, rollout 50회 규모이고 완결 success rate가 아니라 milestone 기반 progress 지표라 일반화 검증 범위는 제한적임

**Top-tier conference 적합성 — 78/100 · 추천 venue: CoRL**

정보이론 기반 action relevance gap 분석, controlled encoder comparison, LeWAM·AdaFuse 구조, DemoDPO offline 정제, real robot 검증까지 갖춰 CoRL이나 RSS에 잘 맞고 representation 분석 비중을 보면 ICLR도 후보임. real-world 실험이 task 3개·rollout 50회로 규모가 작고 DemoDPO가 기존 DPO 변형의 조합적 기여라는 지적이 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- video diffusion backbone 없이 frozen self-supervised encoder 표현 공간에서 action과 future state를 함께 예측하는 구조는, 누리랩 world model·failure detection 연구에서 무거운 video generation 없이 쓰는 저비용 dynamics 예측 module로 재사용 가능함
- DemoDPO처럼 demonstration MSE만으로 candidate action을 랭킹해 offline preference를 만드는 방식은, online RL 없이 test-time에 여러 후보 action을 sampling·재순위화하는 failure recovery/inference-time optimization 아이디어로 확장 가능함
- I-JEPA가 VAE·SigLIP보다 depth·segmentation 정보를 더 잘 노출한다는 probing 결과는, object-centric 3D representation을 쓰는 누리랩 연구에서 policy backbone 선택 근거로 활용 가능함

---

### 2. [78점] InternW0: A Foundational Physical World Model for Efficient Real-World Interactions

- **분야**: World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.27656](https://arxiv.org/abs/2609.27656) ([PDF](https://arxiv.org/pdf/2609.27656))
- **저자**: Jisong Cai, Yao Mu, Ganlin Yang, Zhe Cao, Zhangzheng Tu, Xing Gao, Kailin Li, Xinyu Zhan 외 18명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: A technical report of world models, 24 pages, 8 figures, and 7 tables
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 InternW0는 video expert(느림)와 action expert(빠름)를 비대칭 구조로 분리하고, 매 action chunk마다 관측 기반으로 cached video context만 국소 수정해 재사용함. 이 방식으로 world-action model의 추론 속도를 Fast-WAM 대비 3배 이상 높였고, LIBERO·RoboTwin 2.0 시뮬레이션은 물론 MOF(금속-유기 골격체) 합성·정량 pipetting 같은 실제 과학 실험 조작까지 검증해 로봇 조작을 넘어선 적용 범위를 보여줌.

**Core innovation & methodology**

- mixture-of-transformers 기반으로 future video prediction을 맡는 video expert(느림)와 robot control을 맡는 action expert(빠름)를 비대칭으로 분리해 flow matching으로 joint 학습함
- 매 action chunk마다 video plan을 다시 생성하지 않고, layerwise chunk K/V editor가 최신 관측으로 cached video context를 국소적으로만 수정해 재사용함(observation-conditioned context routing)
- action expert에 force/tactile 이력을 조건으로 넣고 미래 action과 6차원 wrench(힘 3축+모멘트 3축)를 함께 예측하는 contact-aware post-training으로 접촉이 중요한 조작을 지원함
- embodiment별 soft prompt와 37차원 통합 action/state 인터페이스로 real-robot 4종·simulation 2종·egocentric video 1종, 총 7개 데이터셋·25개 domain을 하나의 backbone으로 학습함


**Novelty vs. prior works**

- video context routing 메커니즘은 논문이 스스로 AHA-WAM 설계를 따른다고 밝히고, embodiment별 soft prompt도 X-VLA 설계를 차용함 → architecture 자체의 신규성은 제한적임
- 신규성은 주로 스케일과 도메인 확장에 있음: 실험실 wet-lab 조작(MOF 합성, 정량 pipetting)까지 다루는 275시간 EgoLab egocentric 데이터셋과 과학 실험 workflow 적용은 기존 WAM 논문들이 다루지 않은 영역임
- video/action expert 분리로 추론 속도를 크게 높인 점은 실용적 기여이나, 개념적으로는 기존 dual-system VLA(π0.5 계열)의 비동기 처리 아이디어를 world-action model 맥락으로 확장한 것에 가까움


**Benchmark results**

- LIBERO 전체 40 task 평균 success rate 98.6%로 LingBot-VA(98.5%), Fast-WAM(97.6%) 대비 각각 0.1%p, 1.0%p 앞섬
- RoboTwin 2.0-Full(50 task, in-domain) 평균 93.12%로 최고 성능 ABot-M0.5(94.10%)보다 0.98%p 낮고, Fast-WAM(91.83%) 대비는 1.29%p 높음
- RoboTwin 2.0-Clean2Random(clean 학습→randomized 평가로 out-of-domain generalization 측정) 평균 75.60%로 비교 대상 중 1위, 2위 GigaBrain-0.7(67.3%)을 8.3%p 앞섬
- 추론 속도 16.47Hz(60.73ms)로 Fast-WAM(5.26Hz, 190ms) 대비 3.13배, Motus(0.54Hz, 1866ms) 대비 약 30배 빠름
- 실로봇 실험(Make Sandwich, Pick Industrial Parts, Sort Tubes, MOF 15단계 합성, 정량 pipetting 5단계)에서 π0.5·Fast-WAM 대비 success rate가 대체로 높게 보고되나, 해당 수치는 표지 그래프에서 추출한 값이라 방법-수치 정확한 대응은 본문에서 확인 불가함. ablation 세부 결과와 limitation 논의도 제공된 텍스트가 중간에서 생략되어 확인 불가함


**Top-tier conference 적합성 — 66/100 · 추천 venue: CoRL**

LIBERO·RoboTwin 2.0 시뮬레이션과 실제 wet-lab 과학 실험(MOF 합성, 정량 pipetting)까지 아우르는 대규모 systems 논문이라 로봇학습 학회 적합도는 높음. 다만 핵심 메커니즘(context routing, soft prompt)을 AHA-WAM·X-VLA에서 그대로 가져왔다고 스스로 밝혀 conceptual novelty가 부족하고, 단일 기관 기술보고서 성격이 강해 리뷰에서 incremental engineering으로 지적받을 위험이 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- force/tactile 조건화와 미래 wrench 예측을 결합한 contact-aware post-training은 접촉 실패를 사전에 예측하는 신호로 failure detection·recovery 연구에 참고할 만함
- video expert는 느리게, action expert는 빠르게 돌리는 비대칭 구조와 chunk K/V editor는 world model rollout 비용을 줄이는 test-time optimization 설계 참고 사례로 쓸 수 있음
- 특정 도메인(실험실) egocentric video로 action-free video 학습을 얹는 EgoLab 방식은 데이터가 부족한 특정 산업 조작 도메인에 적용해볼 만한 데이터 전략임


---

### 3. [72점] Memory That Changes Action Is Not Memory That Guides It: Counterfactual Auditing of History-Conditioned Robot Policies

- **분야**: Robot Memory / Evaluation · **robotics relevance**: 10/10
- **arXiv**: [2609.27247](https://arxiv.org/abs/2609.27247) ([PDF](https://arxiv.org/pdf/2609.27247))
- **저자**: Jiajie Zhang, Yankai Xiang, Changhao Chen
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 58점

> 💡 action이 바뀌어도 그것이 올바른 branch 선택이라는 보장은 아님을 보이는 counterfactual 평가 프로토콜 CMA(Counterfactual Memory Audit)를 제안함. Mem-0와 BridgeVLA++를 시뮬레이션과 양팔 로봇 실험에서 감사한 결과, action은 바뀌지만 올바른 목표를 고르지 못하는 사례를 다수 확인함.

**Core innovation & methodology**

- 두 개의 task-consistent 과거가 서로 다른 memory를 만들면서도 동일한 현재 입력으로 수렴하는 상황을 구성해, perceptual aliasing 조건에서 memory가 결정에 실제로 쓰였는지를 감사하는 문제로 formulation함
- frozen policy를 memory state만 바꿔 동일 action seed로 두 번 쿼리하고, 저장된 action을 policy에 노출되지 않는 evaluator-only world 두 개에서 각각 채점하는 교차 설계를 씀
- 평가를 sensitivity(S, action 변화 여부), signed faithfulness(F, warranted branch 선택 여부), matched-world value(U1, 물리적 진행도), reliability(모든 방향·시드에서 일관되게 정답인 pair 비율) 네 단계로 분리함
- native rollout에서 history bank를 교체하거나 4096바이트 anchor만 복원하는 개입을 추가해, 구성된 audit 밖의 closed-loop 영향력도 별도로 검증함

**Novelty vs. prior works**

- 가장 가까운 선행연구 Chameleon은 stored trace를 유지·교체·제거하며 counterfactual choice accuracy까지만 봄. CMA는 완전한 lawful native history를 교체하고 current packet의 정확한 동일성을 검증한 뒤 matched-world physical value와 pair 단위 bidirectional reliability를 추가해, discrete choice가 다른 physical value를 감출 수 있다는 점과 평균 성능이 개별 pair 실패를 감출 수 있다는 점 두 가지 빈틈을 메움
- TFP는 action variation 확인에서 멈추고 TRACE는 routing path consistency만 봄. CMA는 이보다 한 단계 더 나아가 reliability 검증까지 포함함
- 다만 새로운 policy나 memory architecture를 제안하지 않고 기존 두 정책(Mem-0, BridgeVLA++)에 대한 평가 프로토콜만 제공하므로, 알고리즘적 novelty보다는 evaluation methodology 기여로 한정됨

**Benchmark results**

- Mem-0 Put Back: 64쌍 모두 action change가 일어나지만 fully reliable pair는 20/64에 불과함. correct-choice rate 0.729, signed faithfulness F=0.529, matched-world value U1=0.185이지만 absolute regret 0.442로 평균적 이득과 신뢰성이 분리됨
- later Swap: 24쌍 모두 action이 바뀌지만 F=0, pcorrect=0.5로 branch 선택은 무작위 수준이고 fully reliable pair는 0/24임
- native event에서 opposite-target history로 교체하면 official success가 BridgeVLA++·Mem-0 모두 0/48로 떨어지지만, 48/48 continuation이 donor target으로 이동해 closed-loop redirection이 확인됨
- 4096바이트 anchor만 복원해도 injected bank fault 이후 success가 6/36에서 20/36으로 회복함(+38.9 point, [27.8, 50.0]). full rebuild(20/36)와 동일한 회복 수준임
- 양팔 로봇(PiPER) 실험: Put Back 32회 실행 중 target correct 6/32, full success 4/32, memory-consistent direction 16/32에 그쳐 시뮬레이션과 같은 분리 현상이 재현됨. 이 수치는 조작자 라벨 기반이고 독립 blind annotation은 아님

**Top-tier conference 적합성 — 62/100 · 추천 venue: CoRL**

preregistration, pair-cluster bootstrap, 물리 로봇 재현 등 통계적 엄밀성이 높고 memory 평가의 실질적 빈틈(성공률과 action 변화가 memory 사용의 증거가 아니라는 점)을 명확히 지적함. 다만 새로운 알고리즘 기여가 없고 감사 대상이 Mem-0, BridgeVLA++ 두 정책과 소수 task(Put Back, Swap, Repick)에 국한돼 일반화 근거가 제한적이라 rejection risk로 작용할 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- robot memory·failure detection 연구에 바로 적용 가능한 진단 도구임. memory-augmented VLA나 recovery policy를 낼 때 CMA 방식으로 memory가 실제로 결정을 바꿨는지 사전 검증에 쓸 수 있음
- counterfactual/causal reasoning 축과 직접 연결됨. 두 개의 lawful history를 교차시켜 동일 현재에서 평가하는 설계는 우리 lab의 counterfactual reasoning 문제 정의에 참고할 실험 설계 패턴임
- memory bank 결함 발생 시 protected anchor만 복원해 성능을 회복하는 아이디어는 test-time failure recovery 연구에서 policy가 아니라 memory 저장 구조 설계 원칙으로 가져올 수 있음

---

### 4. [70점] Watch, Recall, Act: Always-On Robots in Concurrent Embodied Streams

- **분야**: VLA · **robotics relevance**: 9/10
- **arXiv**: [2609.28429](https://arxiv.org/abs/2609.28429) ([PDF](https://arxiv.org/pdf/2609.28429))
- **저자**: Ding Yi, Peiwen Sun, Chenchu Rong, Jianan Wang, Xili Dai, Xiangyu Yue, Xi Lin
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 11 pages, 3 figures. Accepted to the 10th Conference on Robot Learning (CoRL 2026)
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 항상 켜져 있는 dual-arm 로봇이 먼 미래 신호를 지켜보고(watch) 자기 과거 행동을 기억하고(recall) 실행하는(act) 문제를 하나의 π0.5 backbone에 perception trigger gate, embodied-state head, 압축 self-history memory 세 모듈을 얹어 푼 논문임. 직접 구축한 dual-arm 스트리밍 벤치마크에서 combined-task 성공률(EAS) 45%로 최강 baseline인 SwitchVLA의 28%를 앞섬.

**Core innovation & methodology**

- watch(먼 미래 standing guard 감지)·recall(자기 과거 행동 참조)·act(dual-arm 동시 실행)를 하나의 문제로 묶어 always-on dual-arm streaming을 새로 formulation함.
- 새 네트워크나 planner를 만들지 않고 pretrained π0.5 backbone 하나에 경량 module 세 개(perception trigger gate, embodied-state head, 압축 self-action memory)를 붙여 각각을 context token으로 주입하는 구조임.
- 핵심은 agent-causal self-history임: 어느 arm이 무엇을, 언제 했는지 기록해 두 팔의 동시 기록이 섞이지 않게 하고 "왼팔이 넣은 것" 같은 self-referential recall을 가능하게 함.
- 세 module이 asynchronous하게 context를 갱신해 perception·memory 갱신이 action 실행을 막지 않음(Dispider의 non-blocking skeleton을 계승), 이 설계가 dual-arm concurrency를 가능하게 하는 핵심임.

**Novelty vs. prior works**

- MemoryVLA(perceptual-cognitive memory)·SwitchVLA(mid-task switching)·RoboStream(causal spatio-temporal graph memory)는 각각 always-on·proactive·retrospective·interruptible·concurrent 다섯 축 중 일부만 만족함(Table 1). ARMS는 다섯 축을 모두 만족한다고 주장하나 개별 메커니즘(trigger gate는 Dispider, memory 압축은 MemoryVLA)은 기존 것을 그대로 가져온 것임.
- 새로운 학습 알고리즘이나 architecture가 아니라 기존 module들의 통합과 agent-causal 라벨(어느 arm, 언제)이라는 새 supervision 신호가 novelty의 핵심이며, 저자 스스로도 "integration, not a new network or planner"라고 명시함.
- 즉 novelty는 problem formulation(다섯 축 동시 충족)과 dataset construction(구축 스크립트가 곧 오라클이 되어 추가 annotation 없이 라벨 생성)에 있고, module 각각의 기술적 기여는 제한적임.

**Benchmark results**

- ARMS Dataset Online protocol에서 combined-task 성공률(EAS) 45% vs 최강 baseline SwitchVLA 28%(+17%p)임. Oracle/human 85%에는 아직 40%p가량 못 미침.
- Probe(인식)-Online(실행) 비교에서 recognition은 80% 넘게 유지되는데 action success는 급락함. 병목이 perception이 아니라 execution(동시성·collision 처리)에 있음을 확인함.
- ablation에서 memory module 제거 시 EAS 45→32(recall 72→31), embodied-state head 제거 시 45→34(foreground-continuation 76→58, non-interference 78→68), async concurrency를 hard interrupt로 바꾸면 45→30(foreground-continuation 76→41)으로 가장 크게 떨어져 세 module 모두 필요함을 보임.
- 같은 memory 용량을 유지한 채 agent-causal tag만 제거(world-state memory로 대체)하면 recall 72→50, history consistency 82→55로 하락함. 이득이 memory 크기가 아니라 provenance labeling에서 옴을 보임.
- 실제 Cobot Magic dual-arm robot(N=60/segment)에서도 watch+concurrency 성공률 65% vs baseline 20%, recall 60% vs 13%, self-perturbation relocation 62% vs 18%, 10분 이상 long stream retention 67% vs 30%로 real-robot에서도 큰 격차를 보임. 단 이 데모는 서로 다른 두 물체(banana/carrot)만 써서 외형만으로도 구분 가능하다는 한계를 저자가 명시함, same-class 구분은 ARMS Dataset 실험에서만 정량 검증됨.

**Top-tier conference 적합성 — 74/100 · 추천 venue: CoRL**

real dual-arm robot에서 자체 구축한 benchmark로 다섯 가지 능력(always-on/proactive/retrospective/interruptible/concurrent)을 동시에 검증하고 module별 ablation으로 필요성을 명확히 보여 CoRL 수준의 실험적 conviction은 충분함. 다만 핵심 mechanism(trigger gate, memory 압축)이 대부분 기존 연구(Dispider, MemoryVLA)를 그대로 가져온 것이고 baseline 4개가 모두 저자 자신의 재구현이라 비교의 공정성은 불확실함. real-robot trial 수(~200 stream, N=60/segment)가 작아 large-scale overload 상황 검증은 제한적임.

**추천 이유 & 누리랩 연구와의 연결점**

- agent-causal self-history(어느 arm이 언제 무엇을 했는지 기록)는 failure detection·recovery 연구에 바로 붙일 수 있음, 실패 시점을 "무엇을 했는데 왜 실패했는가"로 되짚는 diagnosis에 활용 가능함.
- embodied-state head가 collision check를 한 문장으로 처리하는 방식은 별도 world model 없이 test-time에서 즉석 상태 추론을 하는 사례라 test-time optimization/inference-time planning 연구와 비교할 만함.
- ARMS Dataset의 "구축 스크립트가 곧 오라클" 방식(추가 annotation 없이 supervision 생성)은 robot memory·counterfactual reasoning 데이터 구축 비용을 줄이는 방법론으로 다른 project에도 이식 가능함.

---

### 5. [68점] LiMA: Bridging Long-term Imagination to Real-time Dexterous Manipulation via Asynchronous Diffusion

- **분야**: Dexterous Manipulation / World Action Model · **robotics relevance**: 8/10
- **arXiv**: [2609.28431](https://arxiv.org/abs/2609.28431) ([PDF](https://arxiv.org/pdf/2609.28431))
- **저자**: Ning Chen, Yankai Fu, Junkai Zhao, Qianpu Sun, Guocai Yao, Pengwei Wang, Zhongyuan Wang, Shanghang Zhang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 장기 상상을 맡는 느린 world model과 고빈도 동작 보정을 맡는 빠른 diffusion 모델을 비동기로 분리한 dual-system 프레임워크 LiMA를 제안함. 두 시스템은 Schrödinger bridge로 latent 단에서 직접 연결되며, 6개 양팔 dexterous manipulation 실물 task에서 Cosmos-Policy 대비 추론 지연 45.8% 줄이면서 평균 성공률 70.8%, 평균 subtask 진행률 78.9%를 달성함.

**Core innovation & methodology**

- LiMA는 느린 Future Dreamer(장기 spatiotemporal intent 생성, Cosmos-Predict2-2B로 초기화)와 빠른 Motion Refiner(1B 파라미터, from scratch 학습)로 이루어진 dual-DiT 구조로 world model 기반 장기 상상과 고빈도 반응 실행을 비동기로 분리함
- 두 시스템을 잇는 방식으로 Latent Schrödinger Bridge Coupling(I2SB)을 도입함. Dreamer의 intent latent를 bridge 한쪽 경계(X1), 정답 execution latent를 다른쪽 경계(X0)로 두고, Refiner가 unconditional Gaussian이 아니라 이 경계쌍 사이의 entropy-regularized transport 경로에서 직접 clean latent를 복원하도록 학습함
- Spatiotemporal Adaptive Modulation으로 Dreamer가 상상한 미래 시각 latent를 카메라 뷰별 affine(감마, 베타) 변조를 통해 실시간 관측 토큰에 주입해, 장기 의도와 최신 관측을 정합시킴
- Dreamer는 일정 step마다 한 번만 갱신하고 Refiner는 매 step 동작하는 asynchronous 실행 스케줄과, 학습 시 intent latent에 소량 노이즈를 섞는 Boundary Noise Injection으로 두 시스템 인터페이스의 강건성을 높임

**Novelty vs. prior works**

- 가장 가까운 비교군은 IDM류(VPP)와 통합형 WAM(Cosmos-Policy), 기존 dual-system VLA(Fast-in-Slow, HiRT 등)임. 저자는 IDM은 상상과 행동 예측이 느슨하게 연결되고, 통합 WAM은 이미지·행동을 함께 denoising해 latency가 크며, 기존 비동기 dual-system은 System2 출력을 단순 조건(concat/cross-attention)으로만 쓴다는 한계를 지적함
- 본질적 차이는 System2에서 System1로의 연결을 cross-attention 조건부여가 아니라 diffusion bridge의 경계 조건으로 재정의한 점임. I2SB 자체는 기존 기법(Liu et al. 2023)이라 새로운 생성 모델은 아니고, 이를 dual-system 로봇 정책의 latent 인터페이스로 재배치한 응용적 novelty에 가까움
- ablation(Table 2)에서 동일 조건의 Gaussian 초기화+cross-attention 대비 bridge 방식이 우세함을 보여 이 설계 선택 자체는 실험적으로 뒷받침됨. 다만 world model이나 diffusion bridge 자체에 대한 새로운 이론 기여는 없고, 기존 요소의 조합·재배치 성격이 강함

**Benchmark results**

- 6개 실물 양팔 dexterous task(Stack Cup, Roll T-shirt, Cook Rice, Make Sandwich, Make Coffee, Assemble Package, task당 20 trial)에서 LiMA는 평균 성공률(SR) 70.8%, 평균 subtask 진행률(PSR) 78.9%를 기록함
- 장기·contact-intensive task인 Cook Rice(SR 80.0%/PSR 82.0%), Make Sandwich(SR 70.0%/PSR 80.0%)에서 최고 VLA baseline인 InternVLA-A1(Cook Rice SR 70.0%/PSR 78.0%, Make Sandwich SR 65.0%/PSR 77.5%)과 WAM baseline인 Cosmos-Policy(둘 다 SR 60.0%)를 모두 상회함
- 추론 지연은 H100 기준 325ms로, 통합 WAM인 Cosmos-Policy 600ms 대비 45.8% 감소함. 다만 InternVLA-A1(360ms), GR00T N1.6(270ms), VPP(225ms) 같은 경량 baseline보다는 여전히 느리거나 비슷한 수준임
- Bridge 설계 ablation(Table 2, 별도 3-seed 실험, seed당 real-world 20 trial)에서 future visual intent를 제거하면 LiMA full model 기준 Cook Rice SR이 78.3%에서 61.7%로 가장 크게 떨어지고, I2SB를 Flow Matching으로 대체해도 78.3%에서 73.3%로 하락해 bridge coupling의 기여를 확인함. 이 78.3%는 Table 1 주 실험의 Cook Rice SR(80.0%)과는 별도 실험 회차의 수치임
- component ablation(Table 3a, task 평균 기준)에서 asynchronous 구조를 제거해도 SR은 80%로 유지되지만 latency가 325ms에서 450ms로 늘어, 비동기 설계는 정확도보다 주로 효율 개선에 기여함이 드러남. denoising step은 15 step에서 SR 85%로 채택한 10 step(80%)보다 오히려 높게 나와, 10 step은 성능-효율 절충 선택임

**Top-tier conference 적합성 — 65/100 · 추천 venue: CoRL**

실물 양팔 dexterous 로봇에서 6개 task, 4개 baseline(VLA 2종·WAM 2종)과 비교한 실험 규모와 latency-성능 trade-off 분석이 탄탄해 CoRL 실험 기준에는 부합함. 다만 핵심 기법인 I2SB bridge는 기존 방법의 재활용이고 dual-system 구조 자체도 선행연구가 다수 존재해 novelty는 top-tier oral보다는 poster급 contribution에 가까움. main 결과표(Table 1)에 표준편차나 다중 seed 표기가 없어 통계적 유의성 검증이 ablation(Table 2)만큼 엄격하지 않은 점이 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- world model 기반 장기 imagination과 실시간 반응 실행을 latent bridge로 잇는 구조는 test-time optimization/inference-time planning 연구에 참고할 만함. Dreamer 갱신 주기를 상황 인식형으로 바꾸면 failure detection 이후 재계획(recovery)에도 응용 가능함
- Spatiotemporal Adaptive Modulation은 object-centric 3D/4D representation이나 scene graph 기반 semantic mapping과 결합해, 상상된 미래 시각 latent 대신 3D/4D 표현을 주입하는 방식으로 확장할 수 있음
- 논문이 밝힌 한계(시각 가림에 취약, tactile 미포함)는 실험실의 tactile perception·failure recovery 연구와 직접 연결되는 지점이라 공동 비교 실험 대상으로 삼을 만함

---

### 6. [66점] BEE: Intervention-Adaptive Real-World Reinforcement Learning with Vision-Language-Action Models

- **분야**: VLA · **robotics relevance**: 9/10
- **arXiv**: [2609.27450](https://arxiv.org/abs/2609.27450) ([PDF](https://arxiv.org/pdf/2609.27450))
- **저자**: Weihui Zhao, Xiaohan Yan, Zunian Wan, Xuan Du, Zhaozhan Chi, Jianbo Mao, Ruipu Wu, Rushuai Yang 외 9명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 고정된 VLA 위에 residual policy를 얹고 online RL로 학습하되, 사람의 개입을 그대로 따라하는 대신 correction model로 액션 차원별 신뢰도를 예측해 Mahalanobis 제약으로 바꿔 씀. 일관되게 고쳐지는 차원은 사람 쪽으로 강하게 묶고 들쭉날쭉한 차원은 자유도를 풀어줌. 3개 실로봇 task와 LIBERO-Pro 1개 task에서 평균 91.2% 성공률로 RLT(57.5%)와 DSRL(42.1%)을 크게 앞섬.

**Core innovation & methodology**

- 사람의 correction을 imitation target이 아니라 constraint에 대한 evidence로 재정식화함. VLA proposal과 사람 correction의 차이인 residual을 Correction Model qφ로 학습해 차원별 평균과 분산을 예측함.
- 예측된 분산의 역수로 각 차원을 가중한 정규화 Mahalanobis 거리 ρφ를 policy 제약으로 씀. 일관되게 고쳐지는 차원은 좁게 묶고, 변동 큰 차원은 제약을 풀어줌.
- state별 Lagrange multiplier λω(st)를 dual ascent로 학습해 제약 강도를 상태마다 다르게 조절함. VLA는 완전히 얼리고 residual policy πθ만 online RL로 학습해 배포 시 추가 추론 비용이 없음.
- 전체 학습 구조는 RLT의 frozen VLA·latent token·chunk-level actor-critic 인터페이스를 그대로 가져오고, correction을 다루는 방식만 새로 설계함.

**Novelty vs. prior works**

- 가장 가까운 prior work는 RLT와 SiLRI임. RLT는 사람이 개입하면 그 transition의 VLA proposal을 correction으로 통째로 대체해 actor를 학습시키는데, BEE는 proposal을 그대로 두고 correction을 residual로만 다뤄 구분함.
- SiLRI는 state-wise scalar Lagrange multiplier로 사람 개입의 신뢰도를 다루지만 모든 action 차원을 동일하게 취급함. BEE는 heteroscedastic uncertainty 추정으로 이를 차원별로 확장한 것이 핵심 차별점임.
- 다만 이는 완전히 새로운 패러다임이라기보다 SiLRI의 correction-as-constraint 틀을 차원 단위로 정교화한 확장에 가까워서 formulation 자체의 novelty는 제한적임.

**Benchmark results**

- 실로봇 3개 task(phone charging, snack hanging, cloth aligning)와 LIBERO-Pro bowl placing 1개에서 평균 SR 91.2%로 RLT 57.5%, DSRL 42.1%, Base Policy(π0.5 SFT) 38.8%를 앞섬.
- task별 SR은 phone charging 100.0±0.0(Base 90.0±5.0, RLT 58.3±2.9, DSRL 93.3±2.9), snack hanging 85.0±0.0(Base 0.0, RLT 21.7±5.8, DSRL 13.3±2.9)임. cloth aligning 90.0±10.0(Base 36.7±7.6, RLT 73.3±7.6, DSRL 31.7±2.9), bowl placing 90.0±13.2(Base 28.3±7.6, RLT 76.7±17.6, DSRL 30.0±5.0)임.
- human intervention rate은 BEE 평균 30.5%로 RLT 49.0%보다 낮음. RLT는 phone charging에서 동일 예산으로는 58.3%에 그치고 3배 더 많은 online data를 써야 96.7±5.8%에 도달한다고 명시됨.
- ablation에서 correction model을 제거하고 raw correction을 직접 모방하면 가장 성능이 나쁘고, correction model에서 VLA proposal 조건을 빼면 snack hanging에서 더 나빠짐. Mahalanobis 제약을 state-wise scalar 제약으로 바꾸면 saturated된 phone charging에서는 비슷하지만 snack hanging 성능이 크게 떨어짐.
- DAgger는 phone charging에서 63.3±5.8%로 Base Policy(90.0%)보다 낮고, SiLRI·HIL-SERL은 동일 예산에서 SR 0%(개입률 90% 이상)로 사실상 학습이 안 됨. 모든 수치는 real robot 단일 플랫폼, task 4개, 코드·모델 비공개 조건에서 나온 것임.

**Top-tier conference 적합성 — 65/100 · 추천 venue: CoRL**

실로봇 dual-arm manipulation에서 human-in-the-loop RL의 여러 baseline을 강하게 앞선 실험 증거와 calibration·ablation 분석이 탄탄해서 CoRL 수준 발표는 가능해 보임. 다만 formulation이 SiLRI의 state-wise Lagrangian 제약을 dimension-wise로 확장한 수준이라 conceptual leap은 크지 않고, task 4개·단일 플랫폼·단일 operator 조건이라 oral·highlight급 impact로 보기는 어려움.

**추천 이유 & 누리랩 연구와의 연결점**

- correction을 imitation target이 아니라 차원별 신뢰도가 있는 constraint evidence로 다루는 관점은 failure detection·recovery 연구에 바로 적용 가능함. 실패 직전 개입 데이터를 그대로 모방하는 대신 어느 신호가 일관되고 어느 것이 노이즈인지 분리하는 데 쓸 수 있음.
- frozen VLA에 residual policy를 얹어 배포 시 추가 추론 비용 없이 학습하는 구조는 test-time optimization 관점에서 실시간 correction 반영 pipeline 설계에 참고할 만함.
- Correction Model이 학습하는 per-dimension heteroscedastic uncertainty는 robot memory나 counterfactual reasoning 연구에서 재사용 가능한 개입 신호를 걸러내는 필터로 확장해볼 수 있음.

---

### 7. [66점] Generalizable Robotic Insertion with World Models

- **분야**: World Model / Manipulation · **robotics relevance**: 8/10
- **arXiv**: [2609.28258](https://arxiv.org/abs/2609.28258) ([PDF](https://arxiv.org/pdf/2609.28258))
- **저자**: Nicklas Hansen, Iretiayo Akinola, Yijie Guo, Jie Xu, Bingjie Tang, Hao Su, Xiaolong Wang, Abhishek Gupta 외 2명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: IROS 2026
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 AutoMate처럼 물체마다 specialist policy를 따로 학습하던 로봇 조립(insertion) 문제를, wrist 장착 depth 카메라와 proprioception을 입력으로 받는 단일 TD-MPC2 world model로 최대 90개 과제를 동시에 학습시킴. CAD 없이 raw visual 정보만으로 미지 물체 10개에 56% zero-shot 성공률을 냈고, 같은 조건에서 model-free baseline인 AutoMate는 7%에 그침. 학습 물체 수가 늘수록 zero-shot 성능도 같이 커지는 scaling을 확인함.

**Core innovation & methodology**

- 핵심 주장은 새 알고리즘 제안이 아니라, model-free RL(PPO 기반 AutoMate) 대신 model-based RL(TD-MPC2)을 쓰면 raw visual 입력만으로 다중 삽입 과제를 학습하는 generalist policy가 훨씬 잘 확장된다는 실증임.
- world model 인코더는 wrist 장착 depth 카메라(96x96)를 shallow ConvNet으로, proprioception(관절각 7차원+노이즈 섞인 end-effector pose 7차원+socket pose 7차원(각각 3D 위치+4D quaternion)+목표 위치 3차원, 총 24차원)을 2-layer MLP로 각각 처리한 뒤 fuse해 하나의 latent state로 합침.
- 학습은 TD-MPC2 방식을 그대로 유지함: latent dynamics·reward·Q·policy prior를 joint-embedding prediction과 reward/TD loss로 end-to-end 학습하고 원 관측을 픽셀로 복원(decode)하지 않는 implicit world model이며, 실행 시 MPPI 기반 planning으로 행동을 정함(inference-time planning).
- object ID나 CAD 같은 privileged 정보 없이 순수 시각 정보만으로 물체를 구분하게 만들어, 배포 시 미지 물체에도 zero-shot 적용 가능한 구조로 설계함.

**Novelty vs. prior works**

- 알고리즘 자체(TD-MPC2)는 기존 것을 그대로 가져다 쓴 것이라 방법론적 신규성은 낮음. 저자도 새 알고리즘 제안이 목적이 아니라고 명시함.
- 가장 가까운 prior work인 AutoMate 대비 본질적 차이는 문제 설정에 있음. AutoMate의 generalist는 CAD 기반 point cloud embedding에 배포 시에도 의존하지만, 이 논문은 raw depth만으로 학습·배포를 모두 처리해 완전히 data-driven한 미지 물체 조립을 시도한 첫 사례라고 주장함.
- reward 함수(r_penetration, r_dist, r_imitation, r_success)는 IndustReal/AutoMate에서 그대로 가져와 수정 없이 사용함. 즉 novelty는 새 방법론이 아니라 model-based RL을 assembly generalist에 처음 적용해 scaling 이득을 실증했다는 응용 차원에 있음.

**Benchmark results**

- specialist 비교: 100개 assembly 전체 평균 성공률이 InsertionWM 79.78% vs AutoMate 70.31%임(5 seed 평균, object당 100 trial).
- generalist in-domain(seen) 비교: 90개 학습 물체 기준 InsertionWM 55.0% vs AutoMate는 80개 물체 기준 15.6%로, 학습 물체 수가 늘어날수록 AutoMate보다 훨씬 잘 scale함(단 두 방법의 정확한 train/test split이 공개되지 않아 완전한 직접 비교는 아님).
- zero-shot(unseen, 10개 held-out) 성공률은 학습 물체 5/15/45/75/90개에서 각각 27%/40%/50%/53%/56%로 물체 수에 비례해 증가했고, 90개 학습 시 AutoMate의 7%를 크게 앞섬.
- ablation 결과 vision이 핵심임: generalist에서 proprio-only 39.6% vs depth 추가(기본안) 54.5%, specialist에서 proprio-only 55.2% vs depth 추가 79.8%로 차이가 큼. curriculum 효과는 상대적으로 작음(generalist 52.1%→54.5%, specialist 76.2%→79.8%).
- 물체당 expert rollout 100개를 추가로 준 privileged 버전은 성능이 소폭만 향상됐고(정확한 수치는 본문에서 확인 불가) 학습된 expert policy가 필요해 확장성이 낮아 채택하지 않음. 또한 학습 물체 수가 늘수록 in-domain 성능이 소폭 떨어지는 경향도 관찰됨.

**Top-tier conference 적합성 — 60/100 · 추천 venue: IROS**

5-seed 재현, specialist·generalist·finetuning·다양한 ablation까지 실험 설계가 탄탄하고 model-based RL의 scaling 이점을 명확한 수치로 보여줌. 다만 알고리즘은 기존 TD-MPC2 재사용이고 전 실험이 시뮬레이션(Isaac)에 국한돼 real robot 검증이 없어, RSS/CoRL급 oral보다는 IROS/ICRA 수준의 응용 시스템 논문에 적합함(실제로 IROS 2026 게재로 확인됨).

**추천 이유 & 누리랩 연구와의 연결점**

- world model 기반 multi-task policy가 raw visual 입력만으로 unseen object에 zero-shot 일반화된다는 결과는, 누리랩의 VLA/generalist policy 연구에서 world model이 정책 일반화에 기여하는 정도를 보여주는 직접적 근거 사례로 활용 가능함.
- MPPI 기반 decision-time planning으로 정밀 삽입을 수행하는 구조는 test-time optimization/inference-time planning 주제와 바로 연결됨. occlusion으로 인한 실패 케이스에 재탐색·재계획을 붙이는 failure detection·recovery 확장 아이디어로 이어질 수 있음.
- 큰 socket에서 시각적 occlusion 때문에 성능이 떨어진다는 한계는, 논문이 언급한 Fabrica처럼 촬영 위치를 능동적으로 바꿔 기하학적 불확실성을 줄이는 active perception(NBV) 연구로 바로 이어지는 gap이며 누리랩 주제와 맞닿아 있음.

---

### 8. [64점] The Gaussian Is Enough: Flow-Matching Priors Do Not Help When Fine-Tuning Large Behavior Models

- **분야**: VLA/Imitation Learning · **robotics relevance**: 10/10
- **arXiv**: [2609.27070](https://arxiv.org/abs/2609.27070) ([PDF](https://arxiv.org/pdf/2609.27070))
- **저자**: Chen Xu, Rishi Shah, Hadas Kress-Gazit, Haruki Nishimura, Masha Itkina
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 60점

> 💡 flow-matching·diffusion 기반 LBM(Large Behavior Model; LBM 1.0, pi0.5, GR00T N1.5)을 파인튜닝할 때 target에 가까운 non-Gaussian action prior로 바꿔도 대부분 Gaussian과 성능이 통계적으로 구분 안 됨을 10만 건 이상의 시뮬레이션과 1250회 실기체 실험으로 보임. 진단 분석에서는 prior와 무관하게 파인튜닝된 action 예측이 비슷하게 수렴하고, 인코더 학습률을 낮추면 성능이 훨씬 크게 떨어져 인코더 학습이 prior 선택보다 지배적 요인임을 확인함.

**Core innovation & methodology**

- 새 방법 제안이 아니라 문제 설정 자체가 기여임. from-scratch 학습에서는 검증된 "target에 가까운 non-Gaussian prior가 유리하다"는 통념이 pretrained LBM 파인튜닝에도 적용되는지를 최초로 대규모 검증함.
- prior 7종(Gaussian Z, 자체 제안한 A_pre·A_pre+노이즈·E_pre+노이즈, 외부 baseline Cocos·BRIDGER·Retrieval)을 flow-matching objective 하나로 통일해 비교함. task·data·architecture·optimizer·step 수를 전부 고정하고 prior만 바꾸는 통제 실험을 설계함.
- Setting A에서는 이미 절반 파인튜닝된 체크포인트로 target에 3배 가까운 prior(A_pre)를 인위적으로 만들어 "prior 품질이 낮아서 효과가 없다"는 반론을 원천 차단함.
- STEP(논문이 제안한 통계 검정 프레임워크), Welch t-test, Bonferroni 보정, compact letter display(CLD)를 써서 평균 성공률이 아니라 통계적 유의성 기준으로 결론을 냄.

**Novelty vs. prior works**

- BRIDGER, Cocos, action-to-action flow matching 등 기존 non-Gaussian prior 연구는 전부 from-scratch 학습에서만 검증됐고 pretrained LBM 파인튜닝 전이 여부는 다루지 않았음. 이 논문은 그 공백을 정면으로 채운 최초 대규모 연구임.
- 방법론적 novelty는 제한적임. 새 prior나 architecture를 제안하지 않고 기존 7개 prior를 재현·비교한 것이 전부임. novelty는 negative result와 그 원인 규명에 있음.
- LogME와 embedding-space divergence 분석으로 "왜 prior가 파인튜닝에 안 통하는지"까지 설명한 점은 단순 벤치마크 비교 논문과 차별화됨.

**Benchmark results**

- Setting A(LBM 1.0, kitchen 5 task, prior당 1000 rollout): from-scratch에서는 A_pre 성공률 약 28%로 Gaussian 18%보다 유의하게 우세했으나, 파인튜닝 후에는 Gaussian 35%(350/1000)가 A_pre 29%(290/1000)를 오히려 앞섬.
- Setting B_sim(LBM 1.0, 8 task, 5개 data fraction, 총 56000 rollout): 데이터 25~100% 구간에서는 7개 prior가 Gaussian과 통계적으로 구분 안 됨. 5% 데이터에서만 E_pre+노이즈 prior가 25.9% vs Gaussian 18.9%로 유일하게 유의한 우세를 보임.
- Setting B_real(LBM 1.0, FR3 양팔 5 task, 1250 rollout): partial task progress 71~77%에서 Z·E_pre+노이즈·Cocos·Retrieval 4개가 통계적으로 동일 그룹임. BRIDGER는 학습 중 NaN loss가 발생해 약 56%로 유일하게 열세임.
- Setting C(pi0.5·GR00T N1.5, RoboCasa 34 task, 각 27200 rollout): Z와 A_pre+노이즈가 최상위이고, A_pre는 target에 3배 가까운데도 최하위권으로 밀림. real-world 중심으로 pretrain된 pi0.5·GR00T에서는 frozen self-copy 기반 prior(A_pre, Retrieval)가 domain gap에 취약하다고 분석함.
- 인코더 학습률을 1/10로 낮춘 ablation: 시뮬레이션 성공률이 56~59%에서 41~43%로, 실기체는 37%에서 28%로 하락함(모든 prior에서 유사한 폭). prior 선택보다 인코더 학습 자체가 성능을 지배함을 보임.

**Top-tier conference 적합성 — 55/100 · 추천 venue: CoRL**

10만 건 이상 시뮬레이션과 1250회 실기체, 3개 LBM 아키텍처를 아우르는 규모와 엄격한 통계 검정은 CoRL·RSS 수준의 empirical rigor를 갖춤. 다만 negative result이고 새 method·representation 제안이 없어 oral·highlight보다는 poster급 accept에 가깝다고 판단함. 제공된 본문 텍스트에는 Limitations 섹션(Section VIII) 본문이 누락돼 있어 저자가 직접 밝힌 한계는 본문에서 확인 불가함.

**추천 이유 & 누리랩 연구와의 연결점**

- test-time optimization 관점에서, 이 논문이 scope 밖으로 제외한 inference-time warm-starting·frozen-policy noise steering(DSRL, Golden Ticket 등)은 training-time이 아니라 inference-time에 prior·noise를 조정하는 접근이라 누리랩의 test-time optimization 주제와 바로 연결됨.
- 인코더 학습이 파인튜닝 성능을 지배한다는 결과는 failure detection/recovery 연구에서 "정책 실패 원인이 action head가 아니라 encoder representation일 수 있다"는 가설로 이어질 수 있음. embedding divergence를 실패 진단 지표로 재사용할 여지가 있음.
- LogME 기반 training-free introspection 방법론은 world model·representation 연구에서 파인튜닝 품질을 미리 가늠하는 proxy로 가져다 쓸 수 있음.

---

### 9. [63점] PointCast: One World Model for Rigid, Articulated, and Deformable Object Manipulation

- **분야**: World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.28393](https://arxiv.org/abs/2609.28393) ([PDF](https://arxiv.org/pdf/2609.28393))
- **저자**: Hantao Ye, Ross Worobel, Zhuoli Xie, Mingen Li, Houjian Yu, Youngjin Hong, Changhyun Choi
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 8 pages, 8 figures, 5 tables. Project page: this https URL . This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 POINTCAST는 물체와 엔드이펙터 위 3D point set을 상태로 삼아 rigid·articulated·deformable object를 하나의 diffusion transformer와 학습 레시피로 다루는 point-set world model임. 점마다 identity를 유지한 채 자기 궤적으로 지도하고 distance-preservation prior를 더함. sim 4개 regime 중 3개와 real-world 6개 카테고리 중 4개에서 가장 낮은 오차를 냈고, frozen 상태로 sampling-based MPC에 넣어 4개 task를 계획함.

**Core innovation & methodology**

- 상태를 mesh나 material label 없이 물체·엔드이펙터 위의 3D point set만으로 표현함. object point 128개, actor point 16개로 rigid·articulated(cabinet)·deformable(cloth, rope)을 한 아키텍처와 학습 레시피로 다룸(단, regime별로 checkpoint는 따로 학습함).
- 각 point가 identity를 유지한 채 자기 궤적으로 지도됨. 점 대응 없이 shape만 맞추는 ParticleFormer의 Chamfer/Hausdorff loss와 달리 어느 점이 어디로 가는지까지 학습함.
- DiT 백본이 미래 5프레임 윈도우 전체를 한 번에 denoise함. self-attention은 kNN 기반 local(k=16)과 global을 블록마다 번갈아 쓰고 8개 register token을 둠.
- cross-attention으로 엔드이펙터 point의 위치·움직임 정보를 모든 object point에 전달함. 손실은 flow matching 항에 velocity 정합 항과, 이웃 6점과의 초기 거리를 유지시키는 distance-preservation prior를 더한 것임.

**Novelty vs. prior works**

- 가장 가까운 선행연구 ParticleFormer 대비 본질적 차이는 point correspondence 기반 per-point supervision과 distance prior임. 손실을 ParticleFormer식 shape-matching loss로 바꾸는 ablation에서 cabinet 관절 오차가 79% 악화돼, 이 선택이 실제로 무엇을 학습하는지를 가른다는 근거가 있음.
- material label(ParticleFormer)이나 frozen encoder의 appearance feature(PointWorld) 없이 geometry만으로 4개 regime을 커버하는 점은 강점임. 다만 DiT, flow matching, 3D RoPE, register token, local/global alternating attention은 모두 기존 연구에서 가져온 조합이라 아키텍처 자체의 신규성은 제한적임.
- 제목의 '하나의 world model' 주장과 달리 실제로는 regime마다 별도 checkpoint를 학습함. 4배 budget으로 단일 joint checkpoint를 학습한 ablation은 rope에서 15%, cabinet 관절에서 3.8배 나빠져 진짜 통합 모델로의 일반화는 아직 못 보여줌.

**Benchmark results**

- Sim benchmark(mean rollout error, mm) 기준 cloth 31.90(ParticleFormer 대비 16.6% 개선)과 rope 14.67(32.6% 개선), cabinet 관절 6.84(PTv3 10.34)에서 1위임. rigid는 24.40으로 ParticleFormer 20.88에 16.9% 뒤져 유일하게 진 regime임.
- Real-world PGND benchmark(3초 시점 mean displacement error, mm, 6개 카테고리)에서 rope 15.83, bread 18.65, bag 11.64, sloth 37.83으로 4개 카테고리 1위, cloth·box는 2위임. PGND 자체 모델 대비로는 6개 카테고리 모두 개선함.
- Zero-shot transfer 4개 capture 중 Push-T(15.35)와 Franka YCB push(52.86)에서 1위임. rope·cloth는 ParticleFormer가 앞서 2위에 그침.
- MPC 플래닝(one network eval per window)에서 SE(2) pose push per-point error 1.39cm으로 5개 방법 중 최저(ParticleFormer 1.57cm)이고, sequential articulation 첫 관절 오차도 0.42cm로 최저임. cloth·rope drag는 ParticleFormer·PGND와 차이가 run-to-run spread 안이라고 저자가 명시함.
- 추론 1 Euler step 기준 윈도우당 RTX 4090에서 16.2ms로 25-step 대비 23.8배 빠름. ablation에서 25-step으로 늘려도 cloth 개선은 1% 미만이고 cabinet 관절은 오히려 16% 악화됨.

**Top-tier conference 적합성 — 60/100 · 추천 venue: ICRA**

4개 sim regime, 6개 real-world 카테고리, 4개 zero-shot capture, MPC 플래닝까지 검증한 실험 강도는 top-tier robotics venue 수준임. 다만 아키텍처 요소가 기존 연구의 조합이고 rigid에서 ParticleFormer에 뒤지며 '하나의 world model'이 실제로는 regime별 checkpoint라는 점이 rejection risk임. RSS/ICRA/IROS급 정규 논문에는 적합하나 개념적 도약은 크지 않아 oral·highlight까지는 어려워 보임.

**추천 이유 & 누리랩 연구와의 연결점**

- frozen world model로 sampling-based MPC를 돌려 4개 task를 계획하는 파이프라인은 test-time optimization/replanning 연구에 그대로 재사용 가능함. PGND가 관절 하나에서 드리프트했다가 재계획으로 회복하는 사례(Fig. 8)는 failure detection·recovery 연구에 참고할 만함.
- point identity를 유지한 per-point trajectory 지도 방식은 object-centric 3D representation·scene graph 연구와 연결 가능함. object point에 semantic 정보를 얹어 world model 상태를 확장하는 방향을 검토할 만함.
- deformable·articulated object까지 한 레시피로 다루는 시도는 manipulation generalist policy나 VLA의 action-conditioned world model 서브모듈로 흡수될 여지가 있음. 다만 regime별 checkpoint가 따로 필요하다는 한계는 그대로 옮겨감.

---

### 10. [62점] Beyond Future Prediction: Denoising as Generative Adaptation for Robot Control

- **분야**: VLA (generative policy / world-action model) · **robotics relevance**: 8/10
- **arXiv**: [2609.28339](https://arxiv.org/abs/2609.28339) ([PDF](https://arxiv.org/pdf/2609.28339))
- **저자**: Zanyi Wang, Yuheng Lei, Dengyang Jiang, Ping Luo, Mengdi Wang, Zhixuan Liang, Shilong Liu
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Project page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 58점

> 💡 미래 시각 예측을 별도 타깃으로 쓰는 기존 world-action model co-training과 달리 현재 관측을 denoising하면서 바로 action을 예측하는 NowWAM을 제안함. LIBERO-Plus에서 future-target baseline 대비 6.1점 개선(87.7%)과 함께 학습 visual token을 절반으로 줄이고 step time을 1.8배 단축함.

**Core innovation & methodology**

- 미래 예측이 generative co-training 이득의 원인인지 되짚는 통제 비교에서 past/future target 성능이 82.89~83.80%로 서로 비슷해 forward temporal semantics가 핵심이 아님을 확인함.
- NowWAM은 별도 미래·과거 target 스트림 없이 pretrained DiT의 denoising trajectory를 현재 관측 latent z_t에 직접 적용하고 같은 stream에서 action을 예측함. noise level σ는 저노이즈 쪽으로 치우친 분포에서 샘플링함.
- 학습은 velocity prediction loss(denoising)와 action MSE loss를 λ_vis=0.5, λ_act=1.0으로 결합하고, DiT-MoT 구조(action expert가 DiT의 layer-wise visual-language context를 masked mixed attention으로 소비)를 그대로 사용함.
- 추론 시에는 σ=0(clean endpoint)에서 한 번의 forward pass만 수행해 별도 denoising rollout이나 auxiliary visual stream이 필요 없고, 순수 text-to-image DiT(Z-Image)에도 그대로 적용됨.

**Novelty vs. prior works**

- 가장 가까운 prior인 Fast-WAM/ImageWAM은 여전히 미래(또는 미래 조건부 단일 이미지) target을 유지한 채 추론에서만 제거한 것인데, NowWAM은 그 target 자체를 없애고 현재 프레임의 denoising trajectory를 학습 신호로 재활용한다는 점에서 한 단계 더 나아간 formulation임.
- Table 3b에서 과거/미래 target 성능 차이가 거의 없고, 오히려 같은 시점(t)의 별도 auxiliary target(79.10%)이 NowWAM류 single-stream(83%대)보다 낮게 나와 '무엇을 예측하는가'보다 'denoising trajectory를 action 표현과 얼마나 결합하는가'가 핵심임을 시사함.
- 다만 아키텍처 자체(DiT+action expert, masked mixed attention)는 기존 world-action model 계열과 동일해 구조적 novelty보다는 학습 신호 설계 차원의 novelty에 가까움.

**Benchmark results**

- LIBERO-Plus(perturbation 7종, 10,030 episode)에서 NowWAM(FLUX2-Klein)이 87.7%로 future-target baseline ImageWAM 81.6% 대비 6.1점 개선했고, Z-Image backbone도 87.8%로 유사함.
- 개선폭은 camera(88.6% vs 77.7%), robot(70.5% vs 48.3%) 등 시각·환경 perturbation에서 크고, language 항목은 87.5% vs 89.9%로 비슷하거나 소폭 낮아 개선이 현재 visual representation의 강건성에 집중됨을 보여줌.
- 표준 LIBERO에서는 NowWAM 98.4%로 ImageWAM(98.4%)과 동일해 saturation 구간이라 변별력은 낮음.
- RoboCasa GR1(100-shot, 24 task, 1,200 episode)에서 NowWAM 64.9%로 같은 100-shot 조건의 DIAL(58.3%), Fast-WAM(56.0%)보다 높음.
- Ablation에서 denoising trajectory 없이 clean frame만 학습하면 77.48%로 8점가량 낮아지고, pretrained init 없이 학습하면 50~58%대로 더 크게 낮아져(Table 3a) generative pretraining 자체가 강건성의 주된 원천임을 확인함.
- Table 4 학습 효율 비교에서 future target 스트림을 제거하면 학습 visual token이 784개에서 392개로 절반 줄고 step time이 2.85초에서 1.63초로 1.8배 단축됨.

**Top-tier conference 적합성 — 60/100 · 추천 venue: CoRL**

통제된 ablation으로 world-action model 계열의 핵심 가정(미래 예측 필요성)을 반박하는 명확한 실험 설계가 강점이고, 학습 효율(token 50% 감소, 1.8배 가속)까지 함께 제시해 실용성도 있음. 다만 LIBERO·LIBERO-Plus·RoboCasa 모두 시뮬레이션이고 real-robot 검증은 본문에서 확인 불가하며, 구조 자체는 기존 DiT-MoT 계열과 동일해 novelty가 architecture가 아닌 training-signal 차원에 국한된다는 지적이 나올 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- world model/VLA 연구에서 '미래 예측이 필수인가'라는 가정 자체를 재검토하는 근거로 쓸 수 있음. pretrained generative prior의 기여와 temporal target의 기여를 분리하는 통제 실험 설계를 참고할 만함.
- LIBERO-Plus의 perturbation별 breakdown(camera/robot/background)은 real-robot 실험 없이도 강건성 원인을 분해하는 evaluation protocol이라 failure detection·diagnosis 연구의 평가 설계에 참고 가능함.
- 이 논문 자체는 새 world model이나 recovery 메커니즘을 제안하지 않으므로, 직접 확장보다는 generative backbone을 co-training에 붙이는 방식을 설계할 때 참고 문헌으로 쓰는 게 적절함.

---

### 11. [61점] MemBodied: Recurrent Associative Memory for Vision-Language-Action Models

- **분야**: VLA · **robotics relevance**: 8/10
- **arXiv**: [2609.28256](https://arxiv.org/abs/2609.28256) ([PDF](https://arxiv.org/pdf/2609.28256))
- **저자**: Tej Deep Pala, Navonil Majumder, Bryce Goh, Raphael Yee, Jianfei Yang, Liming Chen, Soujanya Poria
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 VLA policy가 현재 관측만 보고 과거 정보를 못 쓰는 문제를, gated delta rule 기반 고정크기 associative memory와 초기 장면을 압축 저장하는 episode anchor 두 갈래로 해결함. RMBench 5개 태스크에서 stateless 대비 7.81배, 실로봇 3개 태스크에서 8.0배 성공률 향상을 보임. NativeMEM 대비 추론 latency도 91.9% 줄임.

**Core innovation & methodology**

- history-dependent manipulation을 과거 관측을 context에 계속 쌓지 않고, 레이어별 associative matrix(rank r=128)를 gated delta rule로 갱신하는 고정크기 메모리로 푸는 문제 설정임.
- write-value는 실행한 action chunk와 그 결과로 관측된 다음 프레임(post-execution visual consequence)을 합쳐 만들고, delayed-write causal schedule로 미래 관측이 그 액션 생성에 새어 들어가지 않게 막음.
- associative state가 반복 갱신되며 초기 장면 디테일을 지우는 문제를 막기 위해, 첫 관측을 4x4로 압축한 episode anchor를 별도 경로로 두고 cross-attention으로 조회함.
- 검색한 메모리 벡터를 action network의 self-attention suffix에 memory token으로 주입하는 방식이, attention-steering·LSTM류 hierarchical variant보다 우수함을 확인했고 memory parameter는 별도 손실 없이 action loss만으로 sequence 단위 학습함.

**Novelty vs. prior works**

- 가장 가까운 prior work인 NativeMEM(압축 history 토큰 추가), μVLA/ReMem-VLA(recurrent latent state) 대비 associative matrix와 anchor를 분리한 조합은 새롭지만, 핵심 update rule인 gated delta rule 자체는 Gated DeltaNet과 언어모델용 δ-mem에서 그대로 가져온 것이라 이 부분의 신규성은 제한적임(본문도 이를 명시함).
- ablation에서 anchor pathway 제거 시 50.0%에서 37.6%로 떨어져 두 메모리 경로의 역할 분리가 실제 기여를 함을 보였고, 이 조합 자체가 논문의 실질적 novelty 포인트로 보임.
- 문제 설정 새로 정의라기보다 기존 memory-augmented VLA 설계 공간(압축 history/recurrent latent/memory bank) 안에서 vision+action 결합 방식과 주입 인터페이스를 재조합한 수준이라 conceptual leap은 크지 않음.

**Benchmark results**

- RMBench 5개 태스크 평균 성공률 50.0%로 π0-Stateless 6.4% 대비 7.81배, π0-Vanilla Recurrent Memory 16.8% 대비 2.98배, NativeMEM 38.4% 대비 1.3배(11.6%p) 우수함.
- 추론 효율에서 NativeMEM 대비 latency 91.9% 감소(1594ms→129ms), peak GPU memory 9.5% 감소, 추가 파라미터는 40M(π0의 1.26%)으로 NativeMEM 415M(12.81%)의 약 10분의 1임.
- π0.5 backbone에서도 stateless 12.4%에서 48.0%로 3.87배 개선됐고, 실로봇 3개 태스크 평균은 3.33%에서 26.67%로 8.0배 향상됐으나 태스크당 20회 rollout 규모의 소규모 검증임.
- LIBERO 4개 suite 평균은 95.1%로 π0의 94.2%와 comparable하고, long-horizon suite에서만 85.2%에서 90.6%로 5.4%p 개선됐으며 Spatial·Object는 각각 0.6%p, 1.0%p 소폭 하락함.
- memory rank를 32→64→128로 올릴수록 두 태스크 평균이 27.0%→42.0%→55.0%로 단조 증가했고, NativeMEM과 결합하면 오히려 50.0%에서 45.2%로 떨어져 두 메모리 방식이 서로 방해할 수 있음을 보임.

**Top-tier conference 적합성 — 58/100 · 추천 venue: CoRL**

RMBench·LIBERO·real robot까지 폭넓게 검증하고 baseline 비교와 ablation이 촘촘해 empirical conviction은 높음. 다만 핵심 update rule인 gated delta rule이 기존 Gated DeltaNet/δ-mem에서 가져온 것이라 방법론적 새로움은 제한적이고, 실로봇 검증도 3태스크·20회 rollout 규모라 규모 면에서 약함. robot manipulation과 memory 문제 설정에 초점을 맞춘 CoRL/ICRA 계열에는 적합하지만 conceptual novelty를 중시하는 NeurIPS/ICLR full track에서는 reject risk가 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- robot memory 우선주제와 직접 연결됨. associative memory에 과거 action chunk와 그 결과를 함께 기록해 다음 시도를 바꾸는 구조는 우리 lab의 failure detection·recovery 연구에서 실패 이력 기반 재시도 전략 모듈로 응용 가능함.
- episode anchor처럼 초기 장면을 압축해 별도 경로로 참조하는 설계는 object-centric 3D representation·scene graph와 결합해 test-time에 목표 상태를 되짚는 용도로 확장할 수 있음.
- cross-episode로 associative state를 이어가면 50.0%에서 36.8%로 오히려 성능이 떨어진 결과는, 언제 메모리를 리셋해야 하는지에 대한 판단 문제로 lifelong/world model 메모리 연구에 참고할 만함.

---

### 12. [60점] TANDEM: Task and Motion Planning with As-Needed Demonstrations for Efficient Vision-Language-Action Model Fine-tuning

- **분야**: VLA / TAMP 기반 데이터 수집 · **robotics relevance**: 8/10
- **arXiv**: [2609.28314](https://arxiv.org/abs/2609.28314) ([PDF](https://arxiv.org/pdf/2609.28314))
- **저자**: Samrat Sahoo, Liang Ji, Tom Silver, Yixuan Huang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Under review. Project page: this https URL . The first two authors contributed equally
- **원문 검토**: PDF 전문 · 1차 스크리닝 58점

> 💡 TAMP가 못 푸는 구간만 사람이 원격조작으로 메우도록 VLM이 predicate와 human-executed magic operator를 자동으로 만들어 계획에 끼워 넣는 데이터 수집 시스템임. 5개 long-horizon manipulation task에서 pi0.5-DROID를 task당 20개 demonstration으로 fine-tuning해 평균 성공률을 0%에서 60%로 올림.

**Core innovation & methodology**

- 핵심 아이디어는 사람의 개입을 TAMP 도메인 위의 on-demand planning capability로 표현하는 것임. TAMP가 못 다루는 능력을 magic operator라는 symbolic operator로 만들어 계획에 끼워 넣음.
- VLM이 언어 지시와 초기 관측을 보고 기존 TAMP domain(predicate/operator)으로 부족한 부분을 찾아 새 predicate와 human 실행 magic operator를 동시에 생성함(예: IsOpen(box) predicate와 LiftOpen(box) operator).
- task planner 역할의 VLM이 robot phase와 human phase가 섞인 순서 있는 phase sequence를 생성하고, 각 phase 종료 후 재관측해서 VLM predicate classifier로 효과가 확인된 뒤에만 다음 phase로 넘어감.
- 수집한 완전한 demonstration(로봇 자율 구간+사람 teleoperation 구간)을 그대로 VLA(pi0.5-DROID) fine-tuning에 사용하고, 자율 구간만 DATAFARM으로 사람 teleoperation 분포에 맞춰 정렬함.

**Novelty vs. prior works**

- 가장 가까운 선행연구는 HITL-TAMP임. HITL-TAMP는 사람이 맡을 teleoperated action schema를 task마다 미리 정의해야 하고 배포 시에도 TAMP와 local diffusion policy를 함께 유지하는데, TANDEM은 VLM이 predicate/operator를 자동 발명해 task-specific engineering이 필요 없고 배포 시 TAMP 없이 VLA 단독 15Hz 추론만으로 동작함.
- predicate invention 자체는 VisualPredicator, Pixels to Predicates의 연장선임. 두 선행연구는 주어진 low-level skill을 조합하는 모델을 학습하는 데 초점이 있는 반면, TANDEM은 로봇이 아예 실행 불가능한 구간을 사람에게 위임하고 그 결과를 VLM으로 검증하는 데 씀.
- 시스템 구성요소(TiPToP의 TAMP, DATAFARM의 정렬, VLM predicate invention)가 대부분 기존 것을 가져다 쓴 조합이라 새로운 representation·objective·inference paradigm이라기보다는 human-in-the-loop 데이터 수집 파이프라인의 새로운 조합에 가까움.

**Benchmark results**

- demonstration 수집 성공률: Raw TAMP는 5개 task 전부 0%(0/100)인 반면 TANDEM은 전체 76.9%(100/130), task별로는 64.5~90.9%임.
- 실패 원인 분석(130회 시도 중 실패 30건 기준): 93.3%(28/30)가 기존 TAMP execution 실패이고 6.7%(2/30)만 predicate/operator invention 문제임. TAMP planning과 human teleoperation으로 인한 실패는 0%임.
- 사람 시간 매칭 실험(Cover Bread Rolls task): 524초 예산에서 TANDEM 40개 vs oracle teleop 14개, 785초 예산에서 60개 vs 21개로 약 2.9배 더 많은 demonstration을 수집함.
- downstream fine-tuning: pi0.5-DROID pretrained는 5개 task 전부 성공률 0%(task progress 30~41%)였는데, task당 TANDEM demonstration 20개로 fine-tuning하면 평균 성공률 60.0%, task progress 65~93%로 오름.
- HITL-TAMP와 비교(task당 20 trial): TANDEM 평균 성공률 60.0% vs HITL-TAMP 17.0%, 평균 task progress 77.6% vs 55.8%로 5개 task 전부에서 TANDEM이 성공률 우위임. 단 HITL-TAMP는 배포 시 TAMP+diffusion policy를 유지하고 TANDEM은 VLA 단독 15Hz 추론임.

**Top-tier conference 적합성 — 58/100 · 추천 venue: CoRL**

실로봇 5개 long-horizon task에서 demonstration 수집부터 VLA fine-tuning까지 전체 파이프라인을 검증했고 HITL-TAMP 대비 성공률 우위(60% vs 17%)를 명확한 수치로 보여줘서 CoRL 계열 robot learning venue에 적합함. 다만 핵심 구성요소(TiPToP, DATAFARM, VLM predicate invention)가 대부분 기존 방법의 조합이라 conceptual novelty는 크지 않고, task당 demonstration 20개·embodiment 1개(DROID)·VLA 1개(pi0.5)만 검증돼 일반화 근거가 제한적이라 oral보다는 poster급으로 판단됨.

**추천 이유 & 누리랩 연구와의 연결점**

- TANDEM의 magic operator 검증(재관측 후 VLM predicate classifier로 확인)은 사람 개입 지점을 자동 탐지하는 구조와 비슷해서, 이를 배포 후 실패 감지·복구 트리거로 재활용하는 아이디어로 확장할 수 있음.
- VLA data collection 효율화 관점에서 test-time optimization 연구와 결합 가능함. TAMP가 커버 못 하는 구간을 magic operator로 표시하는 방식을, inference 중 policy가 막힌 구간을 스스로 탐지해 인간 또는 추가 데이터 수집으로 전환하는 test-time recovery 파이프라인 설계에 참고할 수 있음.
- predicate invention을 scene graph·semantic mapping과 연결하면 TAMP domain 확장을 object-centric 3D representation 위에서 수행하는 후속 연구로 이어질 수 있음. 단 이 논문 자체는 2D 이미지 기반 VLM 검증만 쓰고 3D representation은 다루지 않음.

---

### 13. [55점] Talk2Escape: Conversational Grounding for Vision-and-Language Navigation

- **분야**: Navigation · **robotics relevance**: 8/10
- **arXiv**: [2609.28296](https://arxiv.org/abs/2609.28296) ([PDF](https://arxiv.org/pdf/2609.28296))
- **저자**: Zerui Li, Sihao Lin, Yanyan Shao, Jiwen Zhang, Xiangyu Shi, Shijie Li, Qi Wu
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: IROS 2026
- **원문 검토**: PDF 전문 · 1차 스크리닝 58점

> 💡 제로샷 MLLM 기반 VLN agent에 kinematic trigger(반복 방문·목표 거리 발산)로 실패 징후를 감지해 대화로 도움을 요청하는 폐루프 개입 프레임워크 Talk2Escape를 제안함. 트리거가 뜨면 오라클이 방향·거리 힌트를 대화로 제공함. R2R-CE에서 GTA에 붙여 SR을 48.8%에서 72.0%로 올려 supervised SOTA(64.2%)도 넘었고, Unitree Go2 실로봇에서도 SR을 40%에서 62%로 끌어올림.

**Core innovation & methodology**

- 기존 VLN을 단일턴 open-loop 실행으로 규정하고, kinematic 상태를 계속 관측하다 실패 징후가 뜨면 agent가 스스로 멈추고 도움을 요청하는 closed-loop 대화 개입으로 문제를 재정의함
- 자동 트리거 두 종류를 수식으로 정의함: 반경 0.5m 지역을 3회 이상 재방문하면 발동하는 Repeat trigger와, 2-step 이동평균 목표 거리가 직전보다 늘어나면 발동하는 Deviation trigger임
- 트리거 발동 시 MLLM 기반 vision-language translator가 RGB-D 관측을 관측 가능한 랜드마크·상대 방향 중심의 짧은 질의로 바꾸고, 알고리즘 오라클 또는 사람이 상대 방위각·거리 기반 규칙으로 방향 힌트를 만들어 프롬프트의 Navigation Assistance 블록에 주입함
- 전체 파이프라인은 파인튜닝 없이 frozen MLLM(Gemini 3.1 Pro) 하나로 동작하며 NavGPT·MapGPT·GTA 등 서로 다른 base agent에 모델-무관하게 얹을 수 있게 설계함

**Novelty vs. prior works**

- 기존 dialogue-driven VLN(DialFRED, HANNA, DialNav, HA-VLN 등)은 시뮬레이터 안에서 지도학습·RL·PEFT로 대화 정책을 학습하고 통신이 즉시·완벽하다고 가정하는데, 본 논문은 프롬프트만으로 zero-shot MLLM을 대화 정책으로 쓰고 실로봇 배치까지 검증함
- 기존 zero-shot VLN(Open-Nav, GTA, SmartWay 등)은 여전히 단일턴 open-loop이라 실패 복구 수단이 없는데, dialogue를 평가 지표가 아니라 실패 복구용 안전망으로 재정의한 점이 핵심 차별점임
- 다만 트리거는 거리 임계값 기반 규칙(반경·이동평균)이고 오라클 힌트도 상대 방위각 계산에 기반한 결정론적 규칙이라, 새 representation이나 learning paradigm이 아니라 기존 zero-shot MLLM VLN 위에 조건부 프롬프트 개입을 얹은 시스템적 기여에 가까움. novelty는 problem framing에 집중되고 방법 자체의 새로움은 제한적임

**Benchmark results**

- R2R-CE 100 episode 부분집합에서 Talk2Escape+GTA는 SR 72.0%(NE 4.80, SPL 49.4, nDTW 51.4)로 zero-shot 기존 최고인 GTA 단독(SR 48.8%)보다 23.2%p 높고 supervised 최고인 Efficient-VLN(SR 64.2%)도 넘어섬
- RxR-CE 260 episode 부분집합에서는 SR이 46.2%에서 62.9%로 오르지만 SPL은 39.3에서 34.2로, nDTW는 57.4에서 49.9로 떨어져 성공률 증가가 경로 효율 저하를 동반함
- VLNVerse에서 NavGPT 단독 SR 19.30%가 CoT 추가만으로 28.70%인데 Talk2Escape 결합 시 84.60%(SPL 8.13에서 35.20)까지 뛰어 대화 개입이 CoT보다 훨씬 큰 효과임을 보임
- trigger ablation(R2R-CE 100 episode)에서 Deviation trigger 단독이 SR 66.0%/SPL 49.4로 가장 효율적인 자동 트리거였고, Repeat과 합친 Hybrid는 개입 빈도가 23.1%로 너무 잦아 SR 54.0%로 오히려 떨어지는 intervention fatigue를 보임
- 실로봇 Unitree Go2 배치에서 Talk2Escape+GTA는 SR 62.0%(NE 3.31m)로 GTA 단독 SR 40.0%(NE 3.66m), zero-shot SmartWay SR 32.0%, supervised RDP SR 20.0%를 모두 앞섬. 다만 정확한 실로봇 시행 횟수는 본문에서 확인 불가

**Top-tier conference 적합성 — 58/100 · 추천 venue: IROS / ICRA**

실로봇 quadruped 배치와 model-agnostic 검증까지 갖춘 실용적 VLN 시스템 논문이라 ICRA/IROS 응용 트랙에 잘 맞음. 트리거와 오라클 힌트가 결정론적 규칙 기반이고 학습되는 새 구성요소가 없어 학습 이론 중심 venue의 oral 기준에는 못 미침. rejection risk는 알고리즘 기여가 얇고, 시뮬레이션 오라클이 ground-truth pose를 쓰는 privileged 정보에 의존한다는 점임.

**추천 이유 & 누리랩 연구와의 연결점**

- failure detection·recovery 연구에 바로 참고할 만함. kinematic 기반 실패 트리거(반복 방문·거리 발산)를 manipulation의 test-time 실패 감지 신호로 변형해 볼 수 있음
- 논문이 스스로 지적한 asymmetric context 한계(오라클이 순간 프레임만 보고 힌트를 줘서 부정확해짐)는 robot memory 연구와 바로 연결됨. spatio-temporal buffer를 오라클·피드백 모듈에 결합하는 후속 연구로 확장 가능함
- 규칙 기반 오라클을 학습된 world model이나 실패 원인 진단 모듈로 대체하면 language feedback 기반 learning과 failure recovery를 결합한 manipulation VLA 버전으로 확장할 여지가 있음

---

### 14. [52점] AWM-VLA: AlignedWorld Modeling for Efficient and Explainable Vision-Language-Action Policies

- **분야**: VLA / World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.27753](https://arxiv.org/abs/2609.27753) ([PDF](https://arxiv.org/pdf/2609.27753))
- **저자**: An Lanji, Dawei Liu, Jin Li, Haoran Xu, Mei Chen, Yu Tian
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: 11pages,7 figures, submitted to ICML 2026
- **원문 검토**: PDF 전문 · 1차 스크리닝 65점

> 💡 FLARE의 global future latent alignment를 object 단위로 쪼개고 MGDA로 action/global/object loss 가중치를 자동 조절하는 VLA world model을 제안함. RoboCasa·휴머노이드 시뮬레이션에서 FLARE 대비 성공률 5~8%p대 개선, object 단위 예측 rationale을 사람 평가자 83.1%가 선호함.

**Core innovation & methodology**

- FLARE(미래 관측 latent를 예측하는 future token alignment)를 확장해, future token 활성값을 object별 embedding으로 디코딩하고 이를 미래 관측의 object 단위 embedding과 정렬하는 object-centric alignment loss를 추가함.
- action flow-matching loss, global alignment loss, object-centric alignment loss 세 개를 MGDA(Sener & Koltun, 2018) 방식으로 gradient 균형을 맞춰 학습하고, 1차 근사에서 어떤 loss도 악화시키지 않는다는 no-degradation을 증명함(Theorem 3.1).
- object별 미래 예측을 '컵이 접시 위로 이동함' 같은 문장으로 디코딩해 policy의 rationale로 그대로 사용함 — 별도 설명 모듈 없이 예측 objective 자체가 설명 역할을 함.
- 학습 가능한 future token M개와 경량 2-layer MLP 디코더만 추가하는 구조라 어떤 diffusion/flow-matching policy에도 꽂을 수 있고 파라미터 오버헤드가 2% 미만임.

**Novelty vs. prior works**

- 가장 가까운 prior work는 FLARE(global latent만 정렬)와 저자들 자신의 InstrucRobo(object-centric decoupling이지만 예측적 world model은 없음)이며, 본 논문은 이 둘을 결합한 조합형 기여임.
- MGDA 기반 multi-objective balancing도 Sener & Koltun(2018)의 기존 기법을 그대로 적용한 것이라, 새로운 representation·architecture·learning paradigm이라기보다 기존 요소 3개를 이어붙인 구성에 가까움.
- 관련 연구 절에서 인용하는 후속 확장 방향(object relation, 3D scene understanding, tokenization)이 대부분 동일 저자 계열의 2026년 미발표성 논문(Yang et al. 2026a-d)이라 독립적 검증이 약하다는 점도 novelty 판단에서 감안해야 함.

**Benchmark results**

- RoboCasa 성공률은 Policy-Only 43.8% → FLARE 53.2% → AWM-VLA(full) 58.9%로, FLARE 대비 +5.7%p, Policy-Only 대비 +15.1%p 개선됨.
- 휴머노이드 tabletop에서도 AWM-VLA 52.6% vs FLARE 47.5%, novel object 48.3% vs FLARE 40.6%, novel instruction 46.1% vs FLARE 37.9%로 5~8%p대 일관된 개선을 보임.
- 초록의 '최대 21% 개선' 주장은 Table 1 수치로 정확히 재현되지 않음 — 본문에서 확인되는 가장 큰 격차는 Diffusion Policy 대비 RoboCasa +29.7%p, UWM(pixel world model) 대비 novel instruction +26.9%p임.
- ablation에서 object-centric alignment를 제거하면 RoboCasa는 58.9→56.4로, rater 선호도는 83.1%→71.5%로 크게 떨어져 해석가능성 개선이 주로 object 정렬에서 나옴을 보임(rater 평가는 사람 5명, N=5 기준이라 표본이 작음).
- MGDA 대신 고정 가중치(λ=0.2)를 쓰면 RoboCasa 58.9→57.2, novel object 48.3→46.8로 하락함.

**Top-tier conference 적합성 — 42/100 · 추천 venue: CoRL**

VLA에 object-centric predictive world model을 결합해 성능과 해석가능성을 동시에 개선한 점은 강점임. 다만 FLARE·object-centric decoupling·MGDA라는 기존 요소 세 개를 조합한 구성이라 conceptual leap이 크지 않고, RoboCasa·휴머노이드 시뮬레이션 두 벤치마크에만 국한되며 real-robot 검증이 본문에서 확인되지 않아 ICML/NeurIPS 계열 oral보다는 CoRL·ICRA 같은 robot learning venue에 더 적합함. 초록의 '최대 21%' 개선 주장이 Table 1 수치와 정확히 맞지 않는 점도 rejection risk로 작용함.

**추천 이유 & 누리랩 연구와의 연결점**

- object-centric future prediction을 rationale로 바로 쓰는 방식은 failure detection/recovery 연구에 붙일 수 있음 — 예상한 object 변화가 실제로 일어나지 않는 것을 실패 신호로 쓰는 test-time monitoring으로 확장 가능함.
- MGDA 기반 multi-objective balancing은 우리 VLA world model 프로젝트에서 auxiliary loss 가중치를 수동 튜닝하는 대신 쓸 수 있는 일반적 도구로 참고할 만함.
- 다만 이 논문은 RoboCasa·휴머노이드 시뮬레이션에 한정되고 real-robot 검증이 본문에서 확인되지 않으므로, 우리 연구에서 실로봇 검증을 먼저 채우면 차별점이 됨.

---

### 15. [50점] InfiNoVA: Infinite Novel View Augmentation for Viewpoint Invariant Robot Policies

- **분야**: VLA · **robotics relevance**: 8/10
- **arXiv**: [2609.27734](https://arxiv.org/abs/2609.27734) ([PDF](https://arxiv.org/pdf/2609.27734))
- **저자**: Sai Puneeth Reddy Gottam, Elmar Rueckert, Vedant Dave
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 동기화된 5대 카메라 데모를 timestep마다 3D Gaussian Splatting으로 재구성해 새 카메라 시점 이미지를 렌더링하고 원래 상태-액션 라벨을 그대로 붙여 VLA 학습 데이터를 늘리는 방법임. 4개 실물 매니퓰레이션 task에서 미학습 시점 성공률을 VISTA 대비 5.4배, 5대 카메라 전체 학습 대비 1.7배 높였음.

**Core innovation & methodology**

- InfiNoVA는 5대 동기화 카메라로 찍은 매니퓰레이션 데모를 매 timestep마다 InstantSplat++로 3D Gaussian Splatting 재구성해 time-varying 장면 표현을 만듦.
- 재구성한 장면에서 방위각 [-π/2, π/2], 반경 0.6~1.2m, 고도 0~π/2 범위로 가상 카메라를 샘플링해 timestep당 최대 15개 새 시점을 렌더링함.
- 렌더링된 관측은 원본 데모와 같은 물리적 상태이므로 언어 지시와 액션 라벨을 그대로 재사용해 relabeling 없이 D_train = D ∪ D_nv를 구성함.
- SmolVLA 정책에서 wrist 카메라는 그대로 두고 2개의 third-person 카메라만 합성 시점으로 교체해 학습하며, 데모당 최대 100개 가상 episode를 만들어 task당 7,000 episode로 확장함.

**Novelty vs. prior works**

- 가장 가까운 baseline인 VISTA는 단일 이미지 diffusion 기반 NVS로 시점을 늘리지만 미관측 영역을 데이터셋 수준 prior로 채워 task 간 콘텐츠가 섞이는 hallucination이 생김 (Pick-and-Place에 Stack task 스펀지가 등장하는 사례 등).
- InfiNoVA는 다중 시점에서 재구성한 명시적 3D Gaussian 표현에서 렌더링해 이런 task-critical hallucination을 줄이는 것이 핵심 차별점이지만, InstantSplat++ 재구성과 feed-forward Gaussian Splatting 자체는 기존 기법을 그대로 가져온 것이라 표현이나 학습 패러다임 차원의 새로움은 아님.
- Yang et al.(RSS 2025)도 Gaussian Splatting으로 시점·외형 증강을 했지만 장면 분해와 정렬이 필요했던 반면, InfiNoVA는 장면 전체를 통째로 재구성해 별도 편집 단계를 없앤 것이 차이점임. 다만 이 역시 응용 단의 개선이지 새로운 problem formulation은 아님.

**Benchmark results**

- novel-view 렌더링 품질(4 task 400 샘플)에서 PSNR 16.65, SSIM 0.841, LPIPS 0.388로 Hunyuan3D/DepthSplat/GLD/VISTA 대비 전 지표 최고이며, 상위 3개 baseline 대비 PSNR 4.3~25.5%, SSIM 2.6~11.7% 개선, LPIPS 15.5~25.0% 감소함.
- 렌더링 시간은 episode당 평균 437초로 VISTA(1575초) 대비 3.6배, GLD(36204초) 대비 82.8배 빠름.
- temporal consistency에서 FeaCD 0.915, ReStraV-Δθ 3.49도로 VISTA 대비 각각 7.0%, 51.3% 개선됨.
- 정책 평가(4 task, 100 rollout)에서 미학습 랜덤 시점 평균 성공률이 Baseline(Random) 7.5%, VISTA-Aug 7.5%인 반면 InfiNoVA는 40.5%로 5.4배 높음. 원 시점 고정 학습인 Baseline(Reference) 65.3% 대비로는 손실의 약 57%를 회복함.
- ablation(Pick-and-Place, 100 rollout)에서 단일 시점 학습은 랜덤 시점 6%, 5대 카메라 전체 학습은 24%인데 InfiNoVA는 40%로, 물리적 카메라를 늘리는 것보다 밀도 높은 가상 시점 증강이 1.7배 더 효과적임을 보임.

**Top-tier conference 적합성 — 38/100 · 추천 venue: ICRA**

실물 로봇 4개 task, 5개 baseline과 비교하고 rendering quality·시간·temporal consistency·policy 성공률까지 다각도 정량 지표를 갖춰 ICRA/IROS급 regular paper로는 적합함. 다만 InstantSplat++ 재구성과 3DGS 렌더링 자체는 기존 기법 조합이라 conceptual leap이 작고, 정책 구조는 SmolVLA 하나, 로봇 플랫폼도 SO-101 하나뿐이며 InfiNoVA의 절대 성공률도 40.5%로 낮아 CoRL·NeurIPS급 oral 후보로 보기는 어려움.

**추천 이유 & 누리랩 연구와의 연결점**

- object-centric 3DGS로 로봇 데모를 time-varying 장면으로 재구성하는 파이프라인은 실패 진단·recovery 연구에서 재현(replay) 기반 counterfactual 시점 생성에 그대로 응용 가능함.
- viewpoint 증강이 VLA의 spurious camera correlation을 줄인다는 결과는 test-time에 여러 가상 시점 관측을 앙상블해 policy 신뢰도를 추정하는 failure detection 아이디어로 연결됨.
- InstantSplat++ 기반 pose-free 재구성은 카메라 calibration 없이 동작하므로, tabletop rig에서 demo 수가 부족한 manipulation 프로젝트에 바로 이식 가능함.

---

## 오늘의 핵심 연구 트렌드 종합

- **World-action model의 비대칭·경량 실행** — [InternW0](https://arxiv.org/abs/2609.27656), [LiMA](https://arxiv.org/abs/2609.28431), [NowWAM(Beyond Future Prediction)](https://arxiv.org/abs/2609.28339) 세 편 모두 느린 미래 예측과 빠른 동작 실행을 분리하거나, 미래 예측 자체가 필요한지 되물음. video diffusion backbone을 걷어내고 real-time 제약 안에서 world model을 돌리는 방향으로 수렴함.
- **video diffusion backbone 없는 world model** — [LeWAM](https://arxiv.org/abs/2609.27455)는 frozen I-JEPA embedding으로, [PointCast](https://arxiv.org/abs/2609.28393)는 point-set 상태로, [Generalizable Robotic Insertion](https://arxiv.org/abs/2609.28258)은 TD-MPC2 implicit world model로 각각 무거운 video generation 없이 world model을 구성함.
- **robot memory가 만드는 연구와 감사(audit)하는 연구가 같은 날 등장** — [MemBodied](https://arxiv.org/abs/2609.28256)는 고정크기 associative memory 구조를, [Watch, Recall, Act](https://arxiv.org/abs/2609.28429)는 agent-causal self-history를, [CMA](https://arxiv.org/abs/2609.27247)는 memory가 실제로 결정을 바꿨는지 감사하는 프로토콜을 제안함. memory를 만드는 쪽과 검증하는 쪽이 분리된 채 같이 성숙하고 있음.
- **개입(intervention)을 constraint·trigger로 재정식화** — [BEE](https://arxiv.org/abs/2609.27450)는 사람 correction을 차원별 신뢰도 있는 constraint로, [TANDEM](https://arxiv.org/abs/2609.28314)은 TAMP 실패 구간을 사람이 임시로 채워 넣는 placeholder 동작(magic operator)으로, [Talk2Escape](https://arxiv.org/abs/2609.28296)는 kinematic 실패 신호를 대화 트리거로 바꿈. "언제 개입할지"와 "개입을 어떻게 반영할지"를 분리해서 다루는 것이 공통 패턴임.
- **통념을 대규모 통제 실험으로 반증하는 논문** — [The Gaussian Is Enough](https://arxiv.org/abs/2609.27070)은 flow-matching prior가 LBM 파인튜닝에 효과 없음을, [NowWAM(Beyond Future Prediction)](https://arxiv.org/abs/2609.28339)은 미래 예측이 world-action model 성능의 핵심 요인이 아님을 통계적으로 보임. 둘 다 새 방법이 아니라 가정 자체를 겨냥함.
- **3D reconstruction을 데이터 증강으로 쓰는 흐름 지속** — [InfiNoVA](https://arxiv.org/abs/2609.27734)는 timestep마다 3DGS로 재구성해 새 시점을 렌더링하고, relabeling 없이 학습 데이터를 늘림.

## 유망 연구 방향 및 프로젝트 제안

**Memory read 신뢰도를 test-time에 실시간 추정하는 monitor**
- research question: history-conditioned policy가 배포 중 memory를 실제로 의사결정에 썼는지, 그 판단이 맞는 branch를 골랐는지를 rollout 중간에 감지할 수 있는가.
- 접근·novelty: CMA가 제안한 offline counterfactual audit(두 개의 lawful 과거를 교차시켜 사후 채점)을 배포 중 매 스텝 계산 가능한 lightweight proxy로 압축함. 두 과거를 실제로 재현하지 않고 memory read의 attention 분포나 associative state 변화량만으로 신뢰도를 근사하는 방식을 목표로 함.
- 왜 지금·경쟁 prior work: [CMA](https://arxiv.org/abs/2609.27247)는 offline 사후분석만 제안하고, [MemBodied](https://arxiv.org/abs/2609.28256)는 memory 구조 개선에만 집중함. memory reliability를 실시간 실패 신호로 쓰는 연구는 없음.
- risk·target venue: proxy 지표와 실제 action 실패 간 상관이 task마다 다를 위험이 큼. 실로봇 검증 없이는 신뢰도 논문으로만 읽힐 수 있어 real-robot failure case를 먼저 확보해야 함. CoRL/RSS.

**Encoder representation divergence를 실패 조기 경보로 쓰는 diagnosis**
- research question: fine-tuning 성능을 prior보다 encoder 학습이 지배한다는 결과를 거꾸로 이용해, 배포 중 encoder embedding이 학습 분포에서 벗어나는 정도로 정책 실패를 미리 예측할 수 있는가.
- 접근·novelty: [The Gaussian Is Enough](https://arxiv.org/abs/2609.27070)이 학습 단계 진단용으로만 쓴 LogME(사전학습 특징의 전이 적합도를 라벨 없이 추정하는 지표) 기반 training-free introspection을 test-time monitoring으로 옮김. action head가 아니라 encoder representation을 실패 원인으로 분리해서 보는 관점이 기존 failure detection 연구와 다름.
- 왜 지금·경쟁 prior work: 해당 논문은 이 결과를 파인튜닝 품질 진단에만 씀. 배포 단계 실패 예측으로 확장한 사례는 확인되지 않음.
- risk·target venue: embedding divergence가 distribution shift와 실제 task 실패를 항상 같이 예측하지 못할 위험이 있음. 여러 실패 유형(occlusion, 목표 오인식 등)별로 구분되는지 먼저 확인해야 함. CoRL.

**Sampling-based MPC 기반 world model에 active perception 결합**
- research question: [Generalizable Robotic Insertion](https://arxiv.org/abs/2609.28258)이 남긴 한계인 큰 socket에서의 시각적 occlusion 문제를, 카메라 시점을 능동적으로 바꿔 기하학적 불확실성을 줄이는 방식으로 풀 수 있는가.
- 접근·novelty: implicit world model(TD-MPC2)의 latent uncertainty를 NBV(next-best-view) 목적함수로 바로 쓰는 방식. object CAD 없이 raw visual 정보만으로 동작한다는 원 논문의 장점을 유지한 채 active perception을 얹음.
- 왜 지금·경쟁 prior work: 논문이 스스로 Fabrica류 촬영 위치 조정을 참고문헌으로만 언급하고 직접 다루지 않음. world model uncertainty와 NBV를 명시적으로 연결한 삽입 조작 연구는 확인되지 않음.
- risk·target venue: 추가 시점 이동이 조작 속도를 늦출 위험, 실시간성과의 trade-off를 실험으로 보여야 함. ICRA/IROS.

**Object-centric future prediction을 failure trigger로 쓰는 통합 프레임워크**
- research question: [AWM-VLA](https://arxiv.org/abs/2609.27753)의 object 단위 미래 예측과 [Talk2Escape](https://arxiv.org/abs/2609.28296)의 kinematic trigger를 결합해, "예상한 object 변화가 실제로 일어나지 않음"을 manipulation의 실패 신호로 formalize할 수 있는가.
- 접근·novelty: 두 논문 모두 서로 다른 도메인(manipulation vs. navigation)에서 독립적으로 trigger 설계를 했음. object-centric 예측 오차를 trigger 조건으로 통일하면 도메인 무관한 failure detection 신호를 만들 수 있음.
- 왜 지금·경쟁 prior work: AWM-VLA는 rationale 생성에, Talk2Escape는 kinematic 신호에만 머무름. object 예측 오차 자체를 trigger로 쓰는 논문은 확인되지 않음.
- risk·target venue: object segmentation·tracking 오차가 trigger의 false positive를 늘릴 위험. real-robot 검증이 두 원 논문 모두 제한적이라 이 부분을 채우는 것이 차별점임. CoRL.

## 오늘 반드시 읽어야 할 논문

- [Latent evolving World Action Model](https://arxiv.org/abs/2609.27455) — video diffusion backbone 없이 frozen I-JEPA 위에서 action과 미래를 함께 학습해 대형 VLA와 맞먹는 성공률을 냄.
- [InternW0](https://arxiv.org/abs/2609.27656) — video/action expert 비대칭 분리로 world-action model 추론 속도를 3배 이상 높이고 로봇 조작을 넘어 과학 실험까지 검증함.
- [Memory That Changes Action Is Not Memory That Guides It (CMA)](https://arxiv.org/abs/2609.27247) — memory가 action을 바꿔도 옳은 선택인지는 별개라는 것을 보이는 counterfactual 감사 프로토콜임.
- [Watch, Recall, Act](https://arxiv.org/abs/2609.28429) — always-on dual-arm 로봇에 self-history memory를 붙여 watch·recall·act를 하나의 문제로 formulation함.
- [LiMA](https://arxiv.org/abs/2609.28431) — 느린 world model과 빠른 diffusion 보정기를 Schrödinger bridge로 연결해 지연을 줄이면서 dexterous manipulation 성공률을 높임.
- [BEE](https://arxiv.org/abs/2609.27450) — 사람의 correction을 imitation target이 아니라 차원별 신뢰도 있는 constraint로 재정식화한 online RL임.
- [The Gaussian Is Enough](https://arxiv.org/abs/2609.27070) — flow-matching prior가 LBM 파인튜닝에 통계적으로 무의미하고 encoder 학습이 지배 요인임을 대규모로 실증함.
- [Generalizable Robotic Insertion with World Models](https://arxiv.org/abs/2609.28258) — model-based RL 하나로 최대 90개 조립 과제를 학습해 미지 물체에 zero-shot 일반화됨을 보임.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (444편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2609.27450'>BEE: Intervention-Adaptive Real-World Reinforcement Learning with Vision-Language-Action Models</a></td><td>72</td><td>9</td><td>VLA</td><td>VLA 실로봇 online RL에서 human correction을 차원별 제약으로 모델링하는 새 formulation 제시하고 91.2% 대 57.5%로 실증까지 강함, 우선주제 정확히 부합함</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2609.27656'>InternW0: A Foundational Physical World Model for Efficient Real-World Interactions</a></td><td>68</td><td>9</td><td>World Model</td><td>7200시간 규모 데이터로 학습한 asynchronous video-action world model이고 접촉 인지 post-training과 실제 과학실험 태스크까지 검증해 world model 우선주제에 크게 부합함</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2609.27455'>Latent evolving World Action Model</a></td><td>65</td><td>9</td><td>World Model</td><td>video diffusion 대신 JEPA 임베딩으로 world action model을 구성하고 DemoDPO로 offline preference 정제한 방법, RoboTwin 2.0에서 SOTA급 92.28% 성공률과 real-robot 검증까지 있어 world model·VLA 우선 주제에 정확히 부합함</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2609.27753'>AWM-VLA: AlignedWorld Modeling for Efficient and Explainable Vision-Language-Action Policies</a></td><td>65</td><td>9</td><td>VLA</td><td>FLARE 원리를 확장해 미래 latent를 object-centric하게 분리 예측하는 world model을 diffusion VLA에 내장한 방법, RoboCasa·휴머노이드 조작에서 최대 21%p 성공률 개선과 해석가능한 rationale까지 제공해 VLA+world model 우선 주제에 강하게 부합함</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2609.28393'>PointCast: One World Model for Rigid, Articulated, and Deformable Object Manipulation</a></td><td>62</td><td>9</td><td>World Model</td><td>rigid·articulated·deformable을 하나의 point-set world model로 통합해 다루는 방법, mesh-free 표현과 sim/real 양쪽 검증까지 포함해 world model 우선주제에 크게 부합함</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2609.28429'>Watch, Recall, Act: Always-On Robots in Concurrent Embodied Streams</a></td><td>62</td><td>9</td><td>VLA</td><td>끊임없는 스트림에서 먼 과거를 회상하고 먼 미래 신호를 감지하는 always-on 정책 문제를 새로 정의, CoRL 게재에 dual-arm 동시성까지 검증한 novelty 있는 연구임</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2609.27734'>InfiNoVA: Infinite Novel View Augmentation for Viewpoint Invariant Robot Policies</a></td><td>62</td><td>8</td><td>VLA</td><td>시간가변 3DGS로 매니퓰레이션 데모를 새 시점에서 렌더링해 VLA의 viewpoint invariance를 크게 개선, 5.4배 성공률 향상 등 실증 강하고 object-centric 3D 표현 우선주제에 부합함</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2609.28256'>MemBodied: Recurrent Associative Memory for Vision-Language-Action Models</a></td><td>62</td><td>8</td><td>VLA</td><td>고정크기 associative memory로 VLA의 history-dependent 매니퓰레이션을 개선, LIBERO-Long 90.6%와 파라미터 효율성까지 보여 robot memory 우선주제에 부합함</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2609.28258'>Generalizable Robotic Insertion with World Models</a></td><td>62</td><td>8</td><td>World Model</td><td>wrist camera와 proprioception 결합한 world model로 90개 삽입 과제를 학습해 미지 물체에도 56% 성공, world model+매니퓰레이션 일반화 우선주제에 정확히 부합함</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2609.28431'>LiMA: Bridging Long-term Imagination to Real-time Dexterous Manipulation via Asynchronous Diffusion</a></td><td>62</td><td>8</td><td>Manipulation</td><td>느린 장기 상상과 빠른 반응 실행을 비동기 diffusion으로 분리하고 Schrödinger bridge로 정합시키는 dexterous manipulation 방법, latency 45.8% 감소와 70.8% 성공률로 실증 탄탄함</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2609.27070'>The Gaussian Is Enough: Flow-Matching Priors Do Not Help When Fine-Tuning Large Behavior Models</a></td><td>60</td><td>10</td><td>VLA/Imitation Learning</td><td>LBM 1.0·pi0.5·GR00T N1.5 세 모델과 40개 이상 과제, 시뮬 10만+회·실기체 1250회 규모로 flow-matching prior 선택이 fine-tuning에 도움 안 됨을 반증한 논문임. VLA 파인튜닝에 대한 통념을 큰 스케일로 뒤집은 강한 실증 연구임.</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2609.27247'>Memory That Changes Action Is Not Memory That Guides It: Counterfactual Auditing of History-Conditioned Robot Policies</a></td><td>58</td><td>10</td><td>Robot Memory/Counterfactual Evaluation</td><td>동일한 현재 입력으로 수렴하는 두 과거를 교차 검증하는 Counterfactual Memory Audit으로 memory-conditioned policy가 실제로 과거를 활용하는지 감사함. 실제 양팔 로봇에서 memory가 행동을 바꿔도 틀린 목표를 고르는 사례를 밝혀 robot memory 평가에 근본적 문제를 제기함.</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2609.28296'>Talk2Escape: Conversational Grounding for Vision-and-Language Navigation</a></td><td>58</td><td>8</td><td>Navigation</td><td>궤적 이상 감지 시 대화로 개입해 VLN 폐루프 오류복구를 수행, R2R-CE 66% SOTA와 실로봇 전이까지 검증해 recovery/language feedback 우선주제에 부합함</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2609.28314'>TANDEM: Task and Motion Planning with As-Needed Demonstrations for Efficient Vision-Language-Action Model Fine-tuning</a></td><td>58</td><td>8</td><td>VLA</td><td>TAMP가 다루지 못하는 구간만 인간이 시연하도록 VLM으로 planning domain을 확장하는 방법, pi0.5 finetuning에서 0%에서 60%로 성공률 상승시켜 데이터효율 기여가 실질적임</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2609.28339'>Beyond Future Prediction: Denoising as Generative Adaptation for Robot Control</a></td><td>58</td><td>8</td><td>VLA</td><td>사전학습 생성 DiT가 제어에 기여하는 요소를 현재관측 denoising으로 재해석해 미래예측이 필수가 아님을 보임, LIBERO-Plus에서 속도·성능 모두 개선한 흥미로운 formulation임</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2609.27467'>Kairos: Grounded Forecasting of Presence and Directional Flow in 4D Scene Graphs</a></td><td>58</td><td>7</td><td>Embodied AI</td><td>3D scene graph를 4D로 확장해 사람 이동을 예측하는 표현 제안, 11개월 실환경 배포와 downstream planning 검증까지 있어 novelty와 증거 모두 괜찮음</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2609.27526'>NavProbe: Evidence-Grounded Reasoning with Active Memory Retrieval for Zero-Shot Navigation</a></td><td>58</td><td>7</td><td>Navigation</td><td>능동적 memory retrieval로 zero-shot VLN 성능 개선, R2R/RxR SOTA급 수치와 실로봇 데모까지 갖춰 navigation/memory 우선주제에 부합함</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2609.28064'>SlackDrive: Reclaiming Runtime Slack for Adaptive Driving Inference</a></td><td>58</td><td>6</td><td>Autonomous Driving/World Model</td><td>실시간 latency slack을 이용해 driving world-action model의 추론 예산을 매 스텝 선택하는 SlackDrive로 NAVSIM v2에서 21.7% 개선을 보인 test-time compute 할당 연구임</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2609.27068'>HiRE: Hindsight Reward Editing for Policy Finetuning</a></td><td>56</td><td>8</td><td>RL/Reward Design</td><td>성공·실패 궤적을 hindsight로 대조해 foundation representation의 trap state를 찾아내 보상을 training-free로 교정하는 HiRE를 제안함. CoRL 2026 논문이고 기존 정책 대비 3배 이상 성능이라는 강한 실험 증거가 있음.</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2609.28236'>EmbodiedMemory-Bench: Benchmarking Embodied Memory for Long-Horizon Embodied Tasks</a></td><td>55</td><td>9</td><td>Embodied AI</td><td>장기 embodied 상호작용에서 fine-grained 시각기억·동적 상태추적·상호작용 결과 기록·경험 일반화 4가지 결함을 규명하고 공간·이벤트·장면 메모리로 구성된 EMem·EMem-8B를 제안, robot memory 우선 주제에 정확히 부합하며 방법과 벤치마크를 함께 제공함</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2609.27468'>CereVLA: Cerebellum-Inspired Consequence-Aware Residual Governance for Efficient Vision-Language-Action Execution</a></td><td>55</td><td>8</td><td>VLA</td><td>action chunk 실행 중 예측되는 결과가 불리하면 residual correction을 억제하는 소뇌 영감 governance를 frozen VLA에 붙인 방법, SO-101 실로봇에서 57.5%에서 90.0%로 성공률 개선을 보여 실증력이 있음</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2609.27449'>X2Real: an eXtensive simulation benchmark for real-world generalist policies</a></td><td>55</td><td>8</td><td>Manipulation</td><td>generalist manipulation policy 평가용 대규모 sim benchmark로 sim-to-real correlation 0.84 등 인프라 기여 크나 새 방법론 제안은 아님</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2609.27513'>Behavior-Aligned Action Tokenization for Robot Policy Learning</a></td><td>55</td><td>7</td><td>Manipulation</td><td>soft-DTW로 행동 대응관계를 학습해 action tokenizer를 정렬하는 방법, VLA policy learning에 실질적으로 기여하고 실로봇 검증 포함함</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2609.27780'>Task-Prototype Guided Flow Matching for Few-Shot Generalization in Vision-Language Robot Manipulation</a></td><td>55</td><td>7</td><td>VLA</td><td>few-shot 데모를 task-prototype 토큰으로 변환해 flow matching을 guide하는 방법, 실로봇 검증과 수치적 개선 폭이 준수함</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2609.28131'>DEAL-Grasp: Decoupled Alignment Representation for Geometry-Aware Dexterous Grasp Generation</a></td><td>55</td><td>7</td><td>Manipulation</td><td>rigid transform과 관절을 분리한 alignment 표현으로 dexterous grasp를 flow matching 생성, 접촉 물리성과 다양성 모두 준수한 수치로 보임</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2609.27105'>Provably Complete Generalized Planning with LLMs</a></td><td>55</td><td>5</td><td>Planning/Formal Methods</td><td>LLM이 생성한 generalized plan을 Lean으로 완전성 증명까지 자동 생성해 13개 중 12개 도메인에서 검증된 완전한 계획을 얻어 skill chaining·long-horizon planning에 강한 형식적 보증을 더함</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2609.26911'>TwinCheck: Evidence-Grounded Negative-Twin Verification for Stateful Tool Agents</a></td><td>55</td><td>3</td><td>Agent/Counterfactual Verification</td><td>의심되는 tool call에 대해 trace-grounded counterfactual negative twin을 만들어 검증하는 방법으로 counterfactual reasoning 활용이 참신하고 성공률을 45.3%에서 58.5%로 크게 올렸음</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2609.28290'>Computation Over Geometry: Meaning Identity Is Computed, Not Shipped in the Embeddings</a></td><td>55</td><td>1</td><td>Representation Learning/NLP</td><td>문장 의미 동일성 판단이 독립 임베딩 기하가 아니라 joint forward pass에서 계산됨을 다양한 모델·구조로 폭넓게 입증한 흥미로운 발견임</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2609.27381'>CoPRE: Improving Sensitivity in Proprioceptive Contact Detection for Low-Cost Robot Arms</a></td><td>52</td><td>7</td><td>Manipulation</td><td>저가 로봇팔의 접촉 감지 민감도 개선 방법이고 실로봇 검증(ARX, G1)과 belief-space planning 연계까지 보여줌, failure detection 쪽에 걸림</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2609.28175'>DAVIS: A Depth-Only End-to-End Active-Vision Framework for Humanoid Soccer Skills</a></td><td>52</td><td>7</td><td>Embodied AI</td><td>depth 영상만으로 휴머노이드 축구 접촉 스킬을 학습하는 active-vision 프레임워크, 실로봇(Noetix E1) 검증 포함해 active perception 우선주제에 부합함</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2609.28312'>VGM-VS: Rethinking Visual Geometry Model for High-Precision Visual Servoing</a></td><td>52</td><td>7</td><td>Manipulation</td><td>사전학습 visual geometry model에 scene-specific metric adaptation을 더한 visual servoing, USB-C·케이블 삽입 등 실제 정밀조립에서 서브밀리미터 정확도를 보임</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2609.27334'>Just-in-Time Memory: Learning to Curate Task-Adaptive Memory for LLM Agents</a></td><td>52</td><td>4</td><td>Agent Memory/Embodied</td><td>메모리 큐레이션을 write 시점이 아닌 read 시점으로 미루는 JitMem을 제안해 ALFWorld 등 embodied 벤치마크에서 큰 성공률 개선(+16.2점)을 보였음</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2609.28414'>Frozen Flows Forget: Diagnosing and Restoring Lost Motion in a Latent-flow World Model</a></td><td>50</td><td>8</td><td>World Model</td><td>frozen latent space 위 flow로 만든 world model이 물체 조작 시 motion을 잃어버리는 현상을 진단하고 decode 경로 supervision(DART)으로 복구한 연구, world model의 실패 원인을 규명하고 고친다는 점에서 문제설정이 참신하고 robotics와 직결됨</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2609.27695'>GLoTouch: Global-to-Local Haptic Perception Using a Parallel Gripper for Object Search, Recognition, and Grasping Without External Vision</a></td><td>50</td><td>7</td><td>Manipulation</td><td>시각 없이 촉각만으로 물체 탐색·인식·파지하는 global-to-local 프레임워크, tactile perception 우선주제에 부합하고 sim/real 모두 검증함</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2609.27035'>Reinforcement Learning with Decomposed Subtasks</a></td><td>50</td><td>4</td><td>RL/Agent</td><td>GRPO의 scalar trajectory reward를 subtask 단위로 분해하는 RLDS를 제안해 ScienceWorld 같은 embodied 환경에서 큰 개선(+11.5점)을 보였음</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2609.27745'>Categorical Internalisation of Environmental Groupoids for Generalisable POMDP Solving</a></td><td>50</td><td>4</td><td>RL/Theory</td><td>환경 상태의 대칭을 groupoid로 묶어 symmetry-reduced state space에서 POMDP를 학습하는 범주론적 프레임워크로 로봇 조작의 대칭적 상태 표현에도 적용 가능한 일반화 도구를 제시함</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2609.28274'>Shutdown Sabotage Propensities in Multi-Agent Systems</a></td><td>50</td><td>1</td><td>AI Safety</td><td>목표 없이도 multi-agent 시스템이 shutdown을 방해하도록 서로 조율하는 현상을 17개 모델에서 실증한 중요한 안전성 발견임</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2609.27787'>Ask Which, Not How Good: Sizing Benchmarks Scored by an LLM</a></td><td>50</td><td>0</td><td>Evaluation Methodology</td><td>generalizability theory로 LLM judge 벤치마크의 해상도 한계를 구조적으로 규명하고 pairwise 설계가 이를 해결함을 보인 방법론적으로 탄탄한 연구지만 로봇과 무관함</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2609.27308'>EmbodiedSWE: Coding Agents for Long Horizon Dexterous Robotics</a></td><td>49</td><td>9</td><td>VLA/Data Generation via Agents</td><td>코딩 agent가 장기 dexterous 과제를 풀고 그 해를 대규모 VLA 학습 데이터로 확장하는 EmbodiedSWE를 제안함. 실기체 장기과제 성공까지 보여 VLA 데이터 생성 파이프라인으로서 설득력 있음.</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2609.27314'>CoRe-WAM: Correspondence-Aligned Temporal Residuals for World Action Models</a></td><td>49</td><td>9</td><td>World Model/Manipulation</td><td>frozen tracking으로 과거 시각 특징을 현재 위치로 정합한 뒤 차이를 구해 world action model에 넣는 CoRe-WAM을 제안함. 파라미터 159만 개만 학습해 RoboTwin 2.0에서 유의한 성능 향상을 보인 효율적이고 관련성 높은 기여임.</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2609.26857'>FLINT: Fast Lightweight Inference for Traversability</a></td><td>48</td><td>8</td><td>Navigation/Traversability</td><td>RGB만으로 21.6M 파라미터 경량 모델을 학습해 foundation model보다 정확한 costmap을 내고 실제 야지 주행에서 99% 자율성을 달성함. 자기지도 학습 신호 비교와 실기체 폐루프 검증이 탄탄하나 경량화가 핵심 메시지임.</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2609.28161'>Dissecting Advantage-Guided Post-Training for Vision-Language-Action Policies</a></td><td>48</td><td>7</td><td>VLA</td><td>advantage 기반 VLA post-training의 설계선택들을 통제된 분석으로 분해한 연구, 실로봇 4개 bimanual task로 검증했으나 새 formulation보다는 레시피 정리에 가까움</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2609.28281'>BrickCraft-Duo: Efficient Dual-Arm Skill Learning and Refinement for Compositional Long-Horizon Assembly</a></td><td>48</td><td>7</td><td>Manipulation</td><td>대칭성 활용한 스킬 공유로 듀얼암 브릭 조립을 구성하는 long-horizon 프레임워크, 실환경 9단계 조립까지 검증한 수치가 준수함</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2609.28299'>Contact-Implicit Stein Projected ADMM for Discovery of Diverse Contact-Rich Manipulation Strategies</a></td><td>48</td><td>7</td><td>Manipulation</td><td>Stein variational inference를 ADMM에 결합해 contact-rich 매니퓰레이션의 다양한 접촉모드를 발견하는 방법, 알고리즘적으로 흥미로우나 실로봇 검증은 부족함</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2609.27338'>DUGM-R: Uncertainty-Aware Dynamic Grid Mapping and Risk-Triggered Recovery for Learned Local Navigation</a></td><td>48</td><td>6</td><td>Navigation</td><td>risk-triggered recovery로 failure detection/recovery 주제와 연결되나 sim 위주 검증이고 방법 자체는 기존 요소 조합에 가까움</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2609.27720'>CoRelNav: Collaborative Relational Navigation for Multi-Robot Spatially Constrained Semantic Navigation</a></td><td>48</td><td>6</td><td>Navigation</td><td>관계 기반 목표를 다중로봇이 협력 탐색·검증하는 프레임워크, 실로봇 2대 검증 포함하나 novelty는 기존 요소 결합 수준임</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2609.27747'>Less Language, More Latents: Annotation-Efficient VLAs for Driving</a></td><td>48</td><td>6</td><td>VLA</td><td>latent action codebook으로 언어 주석 5% 미만만 써서 driving VLA 학습, annotation efficiency 관점에서 실용적이나 domain이 driving이라 매니퓰레이션 우선주제와는 다소 거리 있음</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2609.28247'>Controlling Collectives of AI Agents in Reasoning Space with Spatial Transformers</a></td><td>48</td><td>6</td><td>Embodied AI</td><td>spatial transformer 기반 reasoning feedback으로 최대 1024대 로봇 집단을 언어명령으로 제어, 스케일과 novel feedback 메커니즘이 흥미로움</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2609.28378'>ForgetMimic: Motion Unlearning for Reinforcement Learning Humanoid Control</a></td><td>48</td><td>6</td><td>RL</td><td>휴머노이드 RL 정책에서 특정 동작만 선택적으로 잊게 하는 최초의 motion unlearning 방법, 새로운 문제설정이고 G1·H2 실기 검증까지 포함함</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2609.28416'>Agent-Editing World Model: Rethinking World Modeling for LLM Agents</a></td><td>48</td><td>3</td><td>LLM Agent/World Model</td><td>관측을 재구성하는 대신 행동이 task progress를 어떻게 바꾸는지 모델링하는 AEWM을 제안해 world model 문제 설정을 새롭게 정의했지만 embodied 환경이 아닌 소프트웨어 에이전트 대상임</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2609.27286'>Memory Control Signals Emerge Before Action in Long Horizon Agents</a></td><td>48</td><td>3</td><td>Agent Memory/Interpretability</td><td>행동 이전에 이미 hidden state에 압축·회상 필요 신호가 존재함을 밝혀 이를 활용한 PaMER로 컨텍스트 소모를 줄인 메커니즘 발견이 robot memory 설계에도 시사점 있음</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2609.27321'>Verifiable Hidden Dynamics Play: Generating Agentic RL Environments from Solved Mechanisms</a></td><td>48</td><td>3</td><td>RL/Agent Environments</td><td>환경을 만들기 전에 수학적 모델을 먼저 풀어 dynamics와 verifier를 동시에 얻는 VHD-Play로 3300개 저비용 agentic RL 환경을 생성해 폭넓은 벤치마크 개선을 보였음</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2609.27273'>CAVEAT: Towards Robust Computer-Use Agents in Incentive-Misaligned Environments</a></td><td>48</td><td>2</td><td>Agent Safety/Computer-Use</td><td>마켓플레이스 환경이 computer-use agent를 조종하는 8가지 steering mechanism을 새로 정의하고 CAVEAT-Harness로 성공률을 55%p 개선했음</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2609.26891'>Harness as a Language: A Minimalist Agent Framework With Maximal Expressivity</a></td><td>48</td><td>1</td><td>LLM Agent Framework</td><td>agent loop 자체를 코드 실행 primitive invoke 하나로 축소한 최소주의 프레임워크로 Letta·ACE 대비 성능·비용 우위를 보였지만 로봇 적용은 없음</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2609.27038'>Are Stated Reasoning Steps Causally Load-Bearing?</a></td><td>48</td><td>0</td><td>Interpretability</td><td>CoT의 표면적 faithfulness가 activation 수준 인과성을 과대평가함을 보인 정교한 causal patching 연구지만 로봇 적용점은 없음</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2609.27167'>Median Temporal Ensembling: Training-Free Robust Aggregation for Action-Chunked Visuomotor Policies</a></td><td>47</td><td>9</td><td>VLA/Robust Policy Execution</td><td>action-chunked visuomotor policy의 temporal ensembling을 median으로 바꿔 adversarial corruption에 대한 breakdown point를 개선한 training-free 방법임. 적대적 스트레스 테스트와 카메라 실패 상황까지 검증한 실증이 탄탄함.</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2609.27095'>Intelligence Across Embodiments</a></td><td>47</td><td>8</td><td>Cross-Embodiment Learning</td><td>embodiment 간 대응관계를 설계하는 기존 접근의 한계를 지적하고 embodiment diversity를 scaling 축으로 삼자는 포지션 페이퍼임. 새 실험은 없지만 generalist robot policy 방향성 논의로 ISRR에 채택됨.</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2609.27269'>Banana Kick: Response-Informed Skill Evolution for Humanoid Soccer</a></td><td>47</td><td>8</td><td>Humanoid Skill Learning/RL</td><td>reward가 국소적으로 평평해 학습이 멈추는 first-order learning starvation을 정의하고 RISE로 일반 킥을 커브볼 킥으로 진화시킴. sim-to-real 하드웨어 검증까지 갖춘 참신한 문제 정의임.</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2609.27001'>Humanoid Locomotion with a Fly-Inspired Recurrent Controller</a></td><td>46</td><td>7</td><td>Legged Locomotion/Bio-inspired Control</td><td>파리 신경회로에서 영감받은 recurrent controller로 휴머노이드 보행을 구현하고 어떤 경로가 행동을 지탱하는지 개입 실험으로 규명함. 시뮬레이션 한정이지만 embodied recurrent 제어의 메커니즘 분석이 참신함.</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2609.27240'>A Quasi-Direct-Drive Underactuated Asymmetric Hand for Dexterous and Efficient Grasping and Manipulation</a></td><td>45</td><td>8</td><td>Dexterous Manipulation/Hardware</td><td>QDD 액추에이터와 생체모사 비대칭 설계로 손가락별 dexterity와 힘을 분담시킨 Berkeley QUAD Hand를 공개함. Feix taxonomy 33개 중 29개 파지와 큰 발열 감소를 실증한 견고한 하드웨어 기여임.</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2609.27675'>Track2Art: Motion-Centric Articulated Object Model Recovery from 2D Point Trackers</a></td><td>45</td><td>7</td><td>Manipulation</td><td>2D point tracking만으로 관절체의 rigid part와 kinematic 관계를 복원하는 motion-centric 프레임워크, 로봇 상호작용에 필요한 articulated object 이해에 test-time optimization 없이 접근한 점이 새로움</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2609.28099'>Visual Tripwires: Anticipating Failure in Deep Vision Systems</a></td><td>45</td><td>6</td><td>CV</td><td>representation drift·prediction 진동·attention entropy 같은 시간적 불안정성 신호로 모델 실패를 사전에 예측하는 프레임워크, failure detection·diagnosis 우선 주제에 부합하고 조기 경보라는 문제설정이 참신함</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2609.27408'>What Looks Like a Capability Limit in Vision-Language Models Is a Readout Limit</a></td><td>45</td><td>5</td><td>Multimodal</td><td>VLM의 spatial reasoning 실패가 능력 한계가 아니라 answer readout convention(좌표 vs 텍스트) 문제임을 밝힌 분석 논문, embodied grounding에서 좌표 출력을 쓰는 설계에 직접적 시사점이 있음</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2609.27702'>DAVIO: Dense Monocular-Inertial SLAM with Feed-Forward Initialization and Pose-Conditioned Mapping</a></td><td>45</td><td>5</td><td>3D Vision</td><td>Depth Anything 3 기반 feed-forward 초기화로 monocular-inertial SLAM 시작 지연을 줄인 기술 기여, 매니퓰레이션/VLA 우선주제와는 다소 거리 있음</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2609.27264'>GaussPDE: Graph-Based Partial Differential Equation-Driven Rendering for 3D Gaussian Splatting</a></td><td>45</td><td>3</td><td>3D Vision</td><td>사전학습된 3DGS 위에 그래프 기반 PDE 동역학을 얹어 mesh화 없이 물리적 렌더링을 만드는 새로운 표현임, robot 응용은 제시 안 됐지만 3DGS를 동적 시뮬레이션 도메인으로 확장한 점이 novel함</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2609.27374'>Planned Test-Time Scaling with Coordinated Reasoning Paths</a></td><td>45</td><td>3</td><td>LG</td><td>test-time scaling에서 독립 샘플링 대신 planner가 branch들을 조율하게 해 pass@k를 최대 13.4포인트 개선, 로봇학습 우선주제인 test-time optimization과 원리적으로 연결되나 domain은 LLM 추론임</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2609.27277'>TimeEvo: Failure-Driven Self-Evolution of a Time Series Agent</a></td><td>45</td><td>3</td><td>Agent/Failure-Driven Learning</td><td>진단된 실패를 capability gap으로 클러스터링해 evidence-only tool을 합성하는 TimeEvo로 failure-driven self-evolution이라는 failure detection·recovery 주제와 맞닿아 있음</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2609.27869'>Learning What to Activate: Combinatorial Capability Allocation for Long-Horizon Multimodal Agents</a></td><td>45</td><td>3</td><td>Multimodal Agent</td><td>단계별로 필요한 능력 조합을 선택하는 combinatorial capability allocation 문제를 정의하고 CoCA로 비용·성능을 함께 최적화했으며 inference-time planning과 맞닿아 있음</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2609.28250'>Complementary Roles of Activation and Parametric Memory in Few-Shot Learning</a></td><td>45</td><td>2</td><td>LLM Memory/Interpretability</td><td>activation memory와 parametric memory의 역할 분리와 뉴런 수준 상호작용을 밝힌 메커니즘 분석이지만 robot memory가 아닌 few-shot 학습 문제임</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2609.27855'>Reachable Global Optimization in AI Systems: How Global Is Global?</a></td><td>45</td><td>2</td><td>Optimization Theory</td><td>AI 시스템의 최적화 주장이 실제 도달 가능한 영역을 명시하지 않으면 무의미함을 보이는 RIO 프레임워크로 test-time optimization 주장 검증에 시사점이 있음</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2609.27490'>WhatWorkedBench: Benchmarking Experimental Understanding in AI Agents</a></td><td>45</td><td>1</td><td>Agent/Benchmark</td><td>실험 결과를 예측하는 response surface 과제로 AI 리서치 에이전트의 실험적 이해력을 측정하는 새로운 벤치마크 형식을 제시했음</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2609.28041'>How Much Were You Told? Measuring External Information in Peer Reviews</a></td><td>45</td><td>0</td><td>NLP/Meta-science</td><td>리뷰에 담긴 외부 정보량을 정보이론적으로 측정하는 self-conditioning 추정기 제안으로 AUC 1.0까지 보이는 등 방법이 참신하지만 로봇과는 무관함</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2609.27041'>Math Reasoning in LLMs is Organized by Approach, Not Topic</a></td><td>45</td><td>0</td><td>Interpretability/Reasoning</td><td>수학 추론 LLM의 내부 표현이 토픽이 아닌 reasoning approach 단위로 조직됨을 8개 모델에서 보인 흥미로운 발견임</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2609.26872'>MSK-Bench: Benchmarking Full-Body Musculoskeletal Motor Control Across Tasks, Control Paradigms, and Physiological Metrics</a></td><td>44</td><td>6</td><td>Embodied AI/Motor Control Benchmark</td><td>22개 과제로 근골격 휴머노이드의 5가지 제어 패러다임을 표준화해 비교한 MSK-Bench를 제시함. task success와 생리학적 지표가 따로 논다는 점을 밝혀 평가체계로서 기여가 있음.</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2609.26919'>Bend the Clock: Predicting Ahead to Beat Latency in Event-Based Object Detection</a></td><td>44</td><td>6</td><td>Perception/Event Cameras</td><td>예측 지연을 감안해 결과가 나올 시점의 상태를 예측하는 ChronoFuse로 이벤트 카메라 지연 문제를 해결함. 초고속 로봇 인식에서 latency로 인한 성능 손실을 크게 회복시킨 실증이 강함.</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2609.27244'>Full-Covariance Smoothing of Bayesian Neural Networks for Online Adaptation</a></td><td>44</td><td>5</td><td>Bayesian Learning/VLA</td><td>레이어를 state-space로 보고 full-covariance smoothing으로 온라인 적응하는 방법이며 VLA 모델 policy adaptation에도 적용해봄. test-time adaptation 방향에서 관련성 있음.</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2609.28184'>VLMs Can Describe, But Not Measure: Object-Centric Scene Understanding for Robotic Manipulation</a></td><td>42</td><td>7</td><td>Manipulation</td><td>VLM으로 물체 segmentation·주석하고 depth로 grounding하는 모듈형 파이프라인, object-centric 표현 우선주제에 걸리나 구성요소 조합 성격이 강함</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2609.28427'>Context-Continuous Preference Learning for Exoskeleton Personalization</a></td><td>42</td><td>6</td><td>Wearable Robotics/HRI</td><td>Gaussian process로 조건 간 선호를 공유하는 CCPL로 exoskeleton assistance를 소수 피드백만으로 개인화함. 실제 사람 대상 ankle/elbow 실험으로 웨어러블 로봇 개인화에 직접 관련 있음.</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2609.27905'>Anchor-Free Hidden-Target Seeking via Certified Self-Calibration under Correlated Odometry</a></td><td>42</td><td>5</td><td>Navigation</td><td>anchor 없는 hidden-target seeking에서 SE(2) gauge 불확정성을 분석하고 폐형 보정 추정기를 제시, 이론과 실증(200회 트라이얼, ROS/Gazebo) 모두 탄탄하나 우선주제와는 다소 거리 있음</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2609.28225'>Large-Scale Geometric Map-Based Localization of UAVs in GNSS-Denied Urban Environments</a></td><td>42</td><td>5</td><td>Navigation</td><td>건물 배치 기하 디스크립터로 GNSS 없는 도시에서 UAV를 대규모로 localization, 100% recall 등 수치는 강하나 매니퓰레이션/VLA 우선주제와는 거리 있음</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2609.28364'>LEAP-CBF: A Safety Filter for Uncertain Systems with Least-Effort Adversarial Potentials</a></td><td>42</td><td>5</td><td>RL</td><td>불확실성 하 CBF를 adversarial potential로 재정의한 안전필터, 쿼드러페드·쿼드로터 실기 검증까지 갖췄으나 로봇학습 핵심주제와는 다소 거리 있음</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2609.27033'>WTF?! Simulation-Free Reinforcement Learning with Wasserstein-Tilted Flow Maps</a></td><td>42</td><td>3</td><td>RL</td><td>KL reward tilting 대신 optimal transport로 flow map을 직접 fine-tuning하는 simulation-free RL 프레임워크, deterministic optimal control과의 동치를 보이고 280배 적은 학습 연산으로 reward-aligned 성능을 얻어 policy 최적화 일반 원리로 확장 가능성이 있음</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2609.26836'>Silent Failures in Agent-Tool Interaction: An Audit of ToolUniverse</a></td><td>42</td><td>3</td><td>Agent/Failure Detection</td><td>도구 호출이 성공한 것처럼 보이지만 정보가 누락되는 silent failure를 감사한 연구로 failure detection·diagnosis 주제와 맞닿지만 생물학 도구 대상 소프트웨어 에이전트에 국한됨</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2609.28187'>Two Global Crops Suffice: Locating Semantic Emergence in DINO-Style Self-Supervised Learning</a></td><td>42</td><td>2</td><td>Representation Learning</td><td>DINO류 SSL에서 semantic representation이 global view 간 instance consistency에서 주로 발생함을 통제 실험으로 규명한 분석 논문, iBOT의 patch masking objective 역할을 재해석하는 기여가 있어 표현학습 원리 이해에 novel함</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2609.28150'>Exact Feedback Is Not Control: Evaluating Text-based Closed-Loop Revision in LLMs</a></td><td>42</td><td>2</td><td>NLP/Agent</td><td>정확한 피드백이 주어져도 revision이 신뢰할 수 없음을 보인 연구로 language feedback 기반 learning과 맞닿지만 텍스트 편집 태스크에 국한됨</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2609.27664'>Evolutionary Stability Does Not Guarantee Learning Accessibility: A Multi-Agent Reinforcement Learning Perspective on Cooperation Emergence</a></td><td>42</td><td>2</td><td>MARL/Game Theory</td><td>진화적으로 안정한 협력 균형이 유한 샘플 학습 에이전트에는 도달 불가능할 수 있음을 3-agent 게임에서 보인 이론·실증 결합 연구임</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2609.27158'>The Linear Representation Hypothesis Needs a Group Action</a></td><td>42</td><td>1</td><td>Representation Learning</td><td>Linear Representation Hypothesis를 group action으로 재정식화한 개념적 논문임. representation 이론에 기여하지만 embodied AI 실험은 없음.</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2609.27925'>Learning When Not to Listen: Selective Anti-Interference Pretraining for Language Models</a></td><td>42</td><td>1</td><td>LM Pretraining</td><td>먼 prefix 간섭을 선택적으로 억제하는 pretraining objective(SPAR)로 여러 모델에서 RULER 개선을 보였지만 로봇과는 무관함</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2609.27615'>BiCFlow-MER: Orchestrating Discriminative and Generative Multimodal Emotion Recognition via Conditional Transport</a></td><td>42</td><td>1</td><td>Multimodal/Affective Computing</td><td>감정 인식을 구조화된 emotion space로의 generative evidence transport로 재정의한 BiCFlow-MER로 판별·생성 방식을 새롭게 결합했음</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2609.27218'>NaviScale: Generating Large-Scale Semantic Map Datasets for Object Navigation</a></td><td>41</td><td>8</td><td>Navigation/Semantic Mapping</td><td>실내 평면도를 합성해 대규모 semantic map 데이터셋을 생성하고 이를 학습한 predictor로 ObjectNav 성능을 높인 NaviScale을 제안함. HM3D/MP3D 수치와 실기체 배포까지 갖춘 데이터 생성 기여임.</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2609.27275'>BranchDrive: A Branch-Structured Dataset for Action-Conditioned Driving Prediction</a></td><td>41</td><td>7</td><td>Autonomous Driving/Counterfactual Prediction</td><td>동일한 과거에서 12가지 개입 미래를 실제로 물리 시뮬레이션한 branch-structured 데이터셋 BranchDrive를 구축함. counterfactual 주행 예측 평가에 기여하나 closed-loop 안전성까지는 입증하지 못함.</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2609.27532'>ProCredit: From Outcome Rewards to Progress Credit in Agentic Reinforcement Learning</a></td><td>41</td><td>4</td><td>RL/Agentic</td><td>verified progress를 turn 단위 credit으로 바꿔 outcome reward의 sparse 문제를 해결한 agentic RL 방법임. long-horizon credit assignment 아이디어는 skill chaining 문제에 참고할 만함.</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2609.28360'>Privacy-Preserving Semantic Segmentation from High-Resolution Depth and Ultra-Low-Resolution RGB</a></td><td>40</td><td>7</td><td>Navigation</td><td>고해상도 depth와 초저해상도 RGB만으로 semantic segmentation과 3D scene 이해를 수행해 프라이버시를 보존하면서 실로봇 object-goal navigation까지 검증한 방법, 비대칭 센싱이라는 문제설정이 새롭고 real-robot 실험이 있어 실증력이 있음</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2609.26868'>Backdoors in Learning-Based Industrial Robotic Arm Manipulation: An Empirical Security Study</a></td><td>40</td><td>7</td><td>Manipulation/Security</td><td>실제 산업용 로봇팔 두 종에 백도어 공격을 걸고 온라인 방어 파이프라인을 검증한 예비 보안 연구임. 학습 기반 매니퓰레이션 배포의 취약점을 실증했지만 워크숍 논문 수준의 초기 연구임.</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2609.26989'>Spiderbot: An Open-Source Energy-Efficient Hexapod with Passive Gravity Compensation</a></td><td>40</td><td>7</td><td>Legged Robotics/Hardware</td><td>4절 링크와 수동 스프링으로 몸무게를 지지해 정지자세 전력을 90% 이상 줄인 오픈소스 헥사포드 Spiderbot을 공개함. RL sim-to-real까지 검증했으나 학습 알고리즘 자체의 새로움은 크지 않음.</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2609.27005'>MultiPush: Learning to Rearrange with Teams of Car-Like Pushers</a></td><td>40</td><td>7</td><td>Multi-Robot Manipulation/TAMP</td><td>car-like 로봇 팀의 push 재배치를 Dubins curve 할당 문제로 완화해 RL로 스케줄과 배정을 함께 학습하는 MultiPush를 제안함. 실로봇 검증도 있으나 문제를 특정 kinematics 구조에 크게 의존해 푼 점이 제약임.</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2609.27312'>Turning Safety into Competence: Minimally Exploitable Robot Policies via Safety-Filtered Reinforcement Learning</a></td><td>40</td><td>7</td><td>Safe RL/Robot Competition</td><td>안전 필터 학습과 경쟁 과제 학습을 분리해 exploitability를 낮춘 S2C를 제안하고 사람 상대 하드웨어 스트레스 테스트까지 수행함. Markov game 설정에서 이론적 non-exploitability 보장을 붙인 점이 강점임.</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2609.27076'>Pro-Bench: Prompt-Robust Open-Vocabulary Visual Grounding Across Real-World Heterogeneous Environments</a></td><td>40</td><td>6</td><td>Embodied AI</td><td>로봇 배치 환경에서 open-vocab visual grounding의 prompt-robustness를 측정하는 벤치마크임, 방법 제안 없이 16개 모델 평가라 기여가 벤치마크에 국한됨</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2609.27509'>Know-Your-Scene (KYS)-SLAM: Hierarchical Semantic-Motion Priors for Feature Matching in Stereo Visual SLAM</a></td><td>40</td><td>6</td><td>Navigation</td><td>semantic·panoptic·motion prior를 binary 배제 대신 연속적 correspondence cost로 반영한 stereo SLAM 확장, KITTI/EuRoC/VKITTI2 3개 도메인에서 일관된 ATE 개선을 보여 실증력이 탄탄함</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2609.27816'>Safe Multi-Robot Coordination via VLM-LLM Reasoning and Reachability Analysis</a></td><td>40</td><td>6</td><td>Embodied AI</td><td>VLM-LLM 추론과 zonotope reachability를 결합한 안전 코디네이션, 기존 검증기법 조합 위주라 formulation 새로움은 제한적임</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2609.28044'>AeRSoM: An Aerial Rigid-Soft Integrated Manipulator for Contact-Rich Manipulation</a></td><td>40</td><td>6</td><td>Manipulation</td><td>강성가변 rigid-soft 매니퓰레이터로 공중 접촉작업의 안정성을 개선한 하드웨어 논문, 학습 요소 없이 기구설계·제어 위주임</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2609.28222'>From Alignment to Fusion in 3D Vision-Language</a></td><td>40</td><td>5</td><td>3D Vision-Language</td><td>포인트클라우드·복셀·멀티뷰 표현을 pairwise cosine 정렬 후 orthogonal 재매개변수화로 왜곡 없이 융합하는 3D VLM 프레임워크, ScanNet200·ScanRefer 등 8개 데이터셋에서 일관된 개선을 보여 scene understanding에 실증력 있음</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2609.26918'>On Preference Coverage Collapse from Hindsight Relabeling in Multi-Objective Reinforcement Learning</a></td><td>40</td><td>5</td><td>RL</td><td>hindsight relabeling을 preference-conditioned MORL에 적용하면 critic이 방문한 좁은 선호 영역으로 coverage가 붕괴함을 실증하고 her_mix로 해결한 연구, RL 우선 주제에서 실패 원인 규명과 수정이 명확한 좋은 실증 사례임</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2609.27462'>Hybrid Gaussians for Robust Open-Vocabulary 3D Segmentation with Multi-View Object Association and Boundary Refinement</a></td><td>40</td><td>4</td><td>3D Vision</td><td>multi-view object association과 경계 정제로 open-vocab 3D segmentation을 개선한 3DGS 방법, LERF에서 13.4% 상대 개선이나 기존 파이프라인 모듈 보강 수준임</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2609.27850'>GaussianDS: Depth-supervised Semantic Gaussian Splatting for Scene Understanding</a></td><td>40</td><td>4</td><td>3D Vision</td><td>깊이 감독으로 semantic 3DGS의 view 불일치와 경계 누출을 줄인 방법, LERF·3D-OVS에서 SOTA 달성했으나 SAM2 mask propagation과 depth 정렬이라는 기존 요소 조합임</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2609.27186'>Data-driven discrete-time deep recurrent neural network-based modeling for dissipative systems</a></td><td>40</td><td>4</td><td>Dynamics Model/Control</td><td>이산시간 RNN에 dissipativity를 구조적으로 강제해 안정성 보장을 얻은 world model류 방법임. 로봇 실험은 없지만 학습된 dynamics model의 안정성 보장은 robot control에 직결됨.</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2609.27915'>UVU: Improving Multimodal Understanding via Vision-Language Unified Autoregressive Paradigm</a></td><td>40</td><td>2</td><td>Multimodal</td><td>pixel-level visual codebook을 구축해 vision-language를 하나의 autoregressive 어휘로 통합한 pretraining 방법, 사전학습 단계에서 시각 supervision을 도입한다는 설정은 참신하나 robotics 응용은 없음</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2609.27948'>VIVAS: Vitalizing Visual Perception in VLM Pre-training via Vision-language Unified Autoregressive Supervision</a></td><td>40</td><td>2</td><td>Multimodal</td><td>dense-structural-semantic vision tokenizer로 unified vocab을 확장해 fine-grained 시각 지각을 강화한 VLM 사전학습법, 12.4T 토큰 규모와 39개 벤치마크 SOTA가 실증력 있으나 robotics 무관함</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2609.27988'>Task-Induced Riemannian Metrics for Vision Transformer Feature Spaces</a></td><td>40</td><td>2</td><td>CV</td><td>ViT feature space의 task별 pullback metric을 low-rank로 근사 가능한지 진단하는 방법과 token importance head 제안, DPT depth token pruning에서 오차 25% 감소를 보였고 일반적 표현학습 통찰로서 novel함</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2609.27353'>Guides That Cause Actions: An Offline Study of Guide-Action Mutual Reinforcement in Multimodal Web Agents</a></td><td>40</td><td>2</td><td>LG</td><td>웹 에이전트에서 가이드 문장이 행동선택을 인과적으로 유도함을 재현가능 오프라인 벤치마크로 검증, GPT-5.5 등을 능가하나 로봇학습과는 다소 거리 있음</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2609.27717'>SkillGym: Internalizing Human Skills into LLMs for Real-World Problem Solving</a></td><td>40</td><td>2</td><td>LLM Agent</td><td>human skill을 학습 가능한 환경으로 바꿔 SFT+RL로 내재화하는 파이프라인인데 로봇 skill과는 다른 소프트웨어 에이전트 대상임</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2609.26986'>Same evidence, different judgments: Evidence noncommutative in vision/speech-text conflicts</a></td><td>40</td><td>2</td><td>Multimodal</td><td>vision/speech와 text가 충돌할 때 증거 순서만 바꿔도 판단이 달라짐을 보인 evidence noncommutativity 발견으로 embodied spatial reasoning에도 시사점 있지만 로봇 실험은 없음</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2609.27276'>DRSR: Learning Set-Level Deletion Risk for Efficient Long-Horizon Agents</a></td><td>40</td><td>2</td><td>Agent Memory</td><td>history block을 개별이 아닌 집합 단위로 삭제 위험을 학습하는 DRSR을 제안해 토큰을 20%대로 줄이면서 reward를 유지했지만 소프트웨어 에이전트 컨텍스트 압축 문제에 국한됨</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2609.27621'>SHRAV: State-Hypothesis-Reason-Action-Verify Framework for Physical Modeling and Inverse Design</a></td><td>40</td><td>2</td><td>Physics/World Model</td><td>state-continuation core로 순방향 예측과 inverse design을 통합한 SHRAV 프레임워크로 전자기·리소그래피에 적용했으며 world model적 상태 연속성 개념이 로봇에도 참고될 만함</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2609.27252'>What Converges in the Platonic Representation Hypothesis? Structure over Geometry</a></td><td>40</td><td>1</td><td>Representation Learning</td><td>Platonic Representation Hypothesis에서 relational structure와 metric geometry를 분리해 재검증한 분석 논문임. representation learning 우선주제와 닿아있으나 embodied 실험 없음.</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2609.27288'>PotARCin: Multi-Dimensional Evaluation of Skill Acquisition in Abstract Reasoning Tasks</a></td><td>40</td><td>1</td><td>Reasoning/Benchmark</td><td>ARC의 단일 출력 평가를 5개 차원으로 확장해 모델이 스스로 formalize한 규칙과도 모순됨을 보인 견고한 벤치마크 연구임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2609.28197'>PASTABench: Proactive Assessment of Sequential Trajectories for Agent Safety</a></td><td>40</td><td>1</td><td>Agent Safety/Benchmark</td><td>언제 개입해야 하는지를 Optimal Intervention Window로 정량화한 PASTABench로 최고 모델도 40.74%에 그치는 문제를 잘 드러냈음</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2609.28048'>TEMPS: Temporal Sentence Embeddings for Temporal Information Retrieval</a></td><td>40</td><td>0</td><td>IR/NLP</td><td>시간 정렬을 위한 temporal embedding을 semantic retriever에 결합해 R@1을 19.92에서 25.39로 올린 IR 방법론임</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2609.28470'>StudentBench: AI and human tutoring yield equivalent GRE learning gains</a></td><td>40</td><td>0</td><td>Education/HCI</td><td>AI 튜터링이 인간 튜터링과 GRE 학습 향상에서 통계적으로 동등함을 2383명 규모로 보인 대규모 실증 연구지만 로봇과 무관함</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2609.27145'>Planning Trajectories that Bounce: Reflection Classes for Collision-Tolerant Robots</a></td><td>39</td><td>7</td><td>Motion Planning</td><td>벽 반사를 의도적으로 활용하는 reflection class 기반 경로계획으로 충돌회피 대신 접촉을 활용하는 새로운 planning 문제를 정의함. 충돌 tolerant 로봇이라는 설정이 참신하나 시뮬레이션 검증뿐임.</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2609.27188'>Learning Dissipative Dynamics with Dissipativity-by-Construction Discrete-Time Neural Networks</a></td><td>39</td><td>7</td><td>Learned Dynamics Model/Control</td><td>이산시간 MLP에 incremental dissipativity를 구조적으로 보장시켜 로봇 dynamics 학습에 안정성 증명을 붙인 방법임. world model적 안정성 보장이 robot control loop에 바로 쓰일 수 있음.</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2609.28366'>AnchorReasoning: A Visual Grounding and Causal Reasoning Dataset in Long-Tail Autonomous Driving Scenarios</a></td><td>38</td><td>6</td><td>Autonomous Driving</td><td>long-tail 자율주행에서 결정적 시각 증거를 위치·속성·이유·궤적까지 잇는 VG-CoT로 라벨링한 대규모 데이터셋과 커리큘럼 학습법, 8개 백본에서 궤적 오차와 grounding을 동시에 개선해 embodied spatial reasoning에 실증적으로 기여함</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2609.28467'>Where Should I Join? Robot Group Joining via Language-Guided Goal Prediction</a></td><td>38</td><td>5</td><td>Navigation</td><td>언어로 지정된 그룹에 합류할 위치를 예측하는 소셜 네비게이션 연구, 실로봇 검증 있으나 로봇학습 핵심주제와는 거리 있음</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2609.27342'>BladeMaster: Real-Time Robotic Cutting Simulation with Online-Generated Persistent Discontinuities</a></td><td>38</td><td>4</td><td>Manipulation</td><td>GPU cutting simulation은 기술적으로 탄탄하나 로봇 학습/policy와 무관한 시뮬레이터 인프라 논문임</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2609.27469'>Collocated Shape Regulation for Soft Robots</a></td><td>38</td><td>4</td><td>Robotics</td><td>soft robot의 collocated shape control 최초 일반 프레임워크로 안정성 증명 탄탄하나 학습 기반 아니고 로봇학습 우선주제와 거리 있음</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2609.27833'>From Reasoning Strings to Partial Orders: Verifier-Certified Rule Transport through Quotient Policy Optimization</a></td><td>38</td><td>2</td><td>RL/Reasoning</td><td>연산 순서가 바뀌어도 같은 결과면 인정하는 commutation certificate로 RL credit을 재분배하는 VCRT를 제안함. 새로운 문제 formulation이나 도메인은 ProofWriter/CLRS/Lean 추론임.</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2609.27307'>Learn How to Act from Your Own Interactions: On-Policy Self-Distillation for GUI Agents</a></td><td>38</td><td>2</td><td>GUI Agent/Imitation Learning</td><td>privilege-conditioned self-teacher로 GUI grounding을 넘어 멀티턴 상호작용까지 on-policy self-distillation을 확장한 GUI-SD-v2 연구임</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2609.27156'>Giving Credit Where It&#x27;s Due: Redundancy-Aware Learning for Efficient Reasoning</a></td><td>38</td><td>1</td><td>LG</td><td>추론 단계별 기여도를 구조적 책임과 답 방향성으로 나눠 GRPO에 반영한 효율적 추론 방법, 정확도 유지하며 토큰 8-31% 절감하나 로봇학습과는 무관함</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2609.27173'>Realize What Matters: Principled Context Representation for Large-Scale Reasoning</a></td><td>38</td><td>1</td><td>LG</td><td>relevance realization 이론에 기반해 대규모 context 표현 설계원칙을 제시하고 작은 모델로 큰 모델을 능가시킨 성과가 흥미로우나 로봇학습과는 무관함</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2609.27900'>Delegated Misalignment: How Multi-Agent Structures Amplify LLM Safety Risks</a></td><td>38</td><td>1</td><td>LLM Safety</td><td>delegation 구조가 개별 모델의 safety alignment를 무력화시킨다는 실증인데 multi-agent 소프트웨어 안전 문제에 국한됨</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2609.27349'>MolDesignBench: Evaluating LLM-based Agent for Scenario-grounded Molecular Design</a></td><td>38</td><td>1</td><td>Agent/Science</td><td>암묵적 제약과 실행 불가능성 탐지까지 요구하는 분자 설계 벤치마크로 최고 성공률이 43%에 그친다는 점을 잘 드러낸 벤치마크 연구임</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2609.27176'>Beyond Overlap: Estimating the Causal Effect of Benchmark Exposure</a></td><td>38</td><td>0</td><td>NLP</td><td>벤치마크 오염이 실제로 성능에 미친 인과효과를 개입실험으로 분리 측정하는 방법론, 대규모 실험(26만+ 생성)으로 근거는 탄탄하나 로봇학습과 무관함</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2609.27373'>Attention Routing Stabilizes Early: Working-Set Inference for Recurrent Language Models</a></td><td>38</td><td>0</td><td>LG</td><td>recurrent LM에서 attention routing이 조기에 안정화됨을 발견해 sparse reuse로 최대 1.76배 가속, 로봇학습과 무관한 효율화 논문임</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2609.27297'>Large Knowledge Model: From Papers to a Scientific Reasoning Landscape</a></td><td>38</td><td>0</td><td>Knowledge/IR</td><td>논문을 근거 기반 reasoning graph로 표현해 과학 지식 접근을 통합하는 Large Knowledge Model으로 야심찬 시스템이지만 로봇 연구와는 거리가 있음</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2609.27863'>A hierarchy of faithfulness criteria for knowledge base completion</a></td><td>38</td><td>0</td><td>Knowledge Graph/Neurosymbolic</td><td>지식베이스 완성 모델의 논리적 faithfulness를 4단계 위계로 정의하고 현재 임베딩 모델 전부가 이를 만족 못함을 보인 이론·실증 연구임</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2609.27741'>Limiting-Kernel Q($λ$): Bridging Short and Long Horizons</a></td><td>37</td><td>4</td><td>RL</td><td>n-step truncation과 limiting kernel을 결합해 단기·장기 horizon을 잇는 off-policy value estimator LKQL을 제안함. MuJoCo continuous control에서 검증되어 robot RL에 활용 가능함.</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2609.28003'>Learning from Failures: Heterogeneous Graph Memory for Small Language Model Tool-Using Agents</a></td><td>37</td><td>3</td><td>LLM Agent Memory</td><td>실패 경험을 이종 그래프로 구조화해 tool-using agent가 재사용하는 FRESH를 제안함. robot memory·failure recovery 문제의식과 닿아있으나 도메인은 소형 LLM tool agent임.</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2609.28086'>LAYERSCOPE: A Layerwise Characterization of Video and Multimodal Learned Representations</a></td><td>37</td><td>3</td><td>Representation Learning/Video</td><td>video/multimodal 모델의 레이어별 표현 구조를 라벨 없이 비교하는 LAYERSCOPE 프레임워크임. 중간층이 최종층보다 나을 수 있음을 보였고 video understanding 우선주제와 관련 있음.</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2609.28145'>RL Starts before RL: On Policy Distillation for Better Reinforcement Learning</a></td><td>37</td><td>3</td><td>RL/LLM Reasoning</td><td>on-policy distillation을 RL 이전 준비단계로 보고 teacher 정렬이 이후 RL 성능을 좌우함을 실증함. RL 앞단 초기화 통찰은 robot RL/IL 파이프라인에도 참고할 만함.</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2609.27883'>False-science induction in autonomous scientific discovery</a></td><td>37</td><td>2</td><td>AI4Science/Autonomous Discovery</td><td>closed-loop 자율 실험에서 레코드 오귀속이 실험 예산을 잘못된 방향으로 유도하는 false-science induction 현상을 규명함. 자율 실험 무결성이라는 새 문제를 제시했으나 도메인은 단백질·재료 실험임.</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2609.27370'>Geometry-Conditioned Visual Place Recognition in Natural Environments</a></td><td>35</td><td>6</td><td>Navigation</td><td>자연환경 VPR에서 깊이 기반 geometric conditioning으로 외형 변화에 강건한 표현을 학습, WildCross에서 Recall 개선 확인되나 방법은 기존 distillation 틀 안에서의 적용임</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2609.28107'>Distillation for Efficient Multitask Manipulation Policies via Conditional Flow Matching</a></td><td>35</td><td>6</td><td>Manipulation</td><td>단일과제 CFM 전문가들을 멀티태스크 정책으로 지식증류하는 방법, sim(RLBench)만 검증했고 efficiency 지향이라 novelty는 제한적임</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2609.27671'>SGDet3D++: Geometry-Grounded Semantics for 4D Radar and Camera 3D Object Detection</a></td><td>35</td><td>5</td><td>Autonomous Driving</td><td>4D radar-camera 검출에서 증거가 진화하는 3D 가설을 실제로 뒷받침하는지 조건화하는 hypothesis-conditioned evidence grounding 개념 제안, OmniHD-Scenes 등에서 개선폭 있으나 자율주행 검출 태스크에 국한됨</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2609.28328'>BronchoTop: Bronchoscopy Navigation via RGB-Only Topological Localization</a></td><td>35</td><td>5</td><td>Navigation</td><td>환자별 CT 없이 RGB만으로 기관지경 위치를 토폴로지적으로 추정하는 실시간 프레임워크, 실 데이터에서 20%p 이상 개선하고 코드·데이터를 공개해 의료 로봇 내비게이션에 실증적 기여가 있음</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2609.27612'>RegenHarness: A Robot Agent Harness with Evidence-Gated Recursive Self-Improvement</a></td><td>35</td><td>5</td><td>Embodied AI</td><td>task planning과 verification을 분리한 evidence-gated 에이전트 하네스인데 정량적 벤치마크 없이 정성적 사례 위주라 근거가 약함</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2609.28396'>Tractable Reinforcement Learning for Full Class of Signal Temporal Logic Specifications Using Spatiotemporal Tube Reward</a></td><td>35</td><td>5</td><td>RL</td><td>STL 명세를 spatiotemporal tube reward로 매핑한 RL 프레임워크, 형식검증 지향이라 로봇학습 우선주제와는 거리 있음</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2609.27123'>PEARL: A Lightweight Prompt-based Feature Interpreter Framework for Real-Time, Anonymous, and Heterogeneous Collaborative Perception</a></td><td>35</td><td>4</td><td>Multimodal</td><td>협업 인지에서 미지 에이전트에 실시간으로 interpreter를 선택하는 prompt 기반 프레임워크, V2X 도메인 한정이나 heterogeneous multi-agent 적응이라는 문제설정은 참신함</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2609.28159'>Depth-Guided Contrastive Learning for 2D Representations with 3D Spatial Awareness</a></td><td>35</td><td>4</td><td>Representation Learning</td><td>3D 공간에서 가까운 픽셀일수록 표현을 유사하게 만드는 depth 기반 contrastive 보조 objective, scene understanding에 유용한 3D 인지 표현학습이라는 점에서 embodied spatial reasoning과 연결되나 단순한 auxiliary loss 추가 수준임</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2609.27358'>Omnidirectional Amphibious Locomotion via Internal Mass Actuation</a></td><td>35</td><td>4</td><td>Robotics</td><td>내부 질량 이동 기반 양서류 로봇 하드웨어 설계 논문, 학습 요소 없고 mechanism 기여 위주임</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2609.27463'>Safety-Filtered Distributed Koopman-MPC</a></td><td>35</td><td>4</td><td>RL</td><td>분산 Koopman-MPC에 safety filter QP를 분리한 제어이론 논문, 로봇학습 우선주제와 거리 있음</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2609.27778'>Visibility-Guided Structured Measure Flow for Class-Conditioned 3D Gaussian Generation</a></td><td>35</td><td>3</td><td>3D Vision</td><td>3DGS를 opacity·covariance·visibility로 가중된 measure로 formulate해 클래스 조건 생성한 방법, VISTA-Obj30에서 큰 개선폭이나 자체 벤치마크라 일반화는 미확인이고 robot 응용은 없음</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2609.27779'>Fusion-Aware Direct 3D Gaussian Generation with Structured Patch Latent Flows</a></td><td>35</td><td>3</td><td>3D Vision</td><td>비정형 Gaussian을 계층적 patch token으로 인코딩해 rectified flow로 직접 생성하는 방법, 위 VISTA-GS와 유사한 문제를 다루며 sampling 효율은 좋으나 robot task 검증 없음</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2609.27346'>Reflection-Aware Reasoning for Non-Line-of-Sight Pedestrian Localization</a></td><td>35</td><td>3</td><td>CV</td><td>NLOS 보행자 위치추정은 자율주행 perception 문제라 로봇학습 우선주제와 거리 있음</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2609.28087'>Discovery of fully efficient fault indicators along a data-based diagnosis process</a></td><td>35</td><td>3</td><td>Fault Diagnosis/Symbolic Regression</td><td>symbolic regression 기반 fault indicator를 개선한 DT4X+로 failure detection·diagnosis 주제와 관련 있지만 산업 시스템 대상의 incremental 개선임</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2609.27423'>Overlapping Visual Grouping Without Semantic Priors</a></td><td>35</td><td>2</td><td>CV</td><td>의미 카테고리 없이 센서 측정 관계만으로 지각적 grouping을 형성하는 새 문제설정(DPG), active perception 이전 단계의 표현이라는 점에서 개념적으로 흥미로우나 robot task 검증은 없음</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2609.27917'>Spread and Scale: What Determines Whether Test-Time Budget Allocation Pays</a></td><td>35</td><td>2</td><td>Test-Time Compute/Combinatorial Optimization</td><td>테스트타임 예산 재배분이 언제 이득인지 사전등록 실험으로 규명한 논문임. test-time optimization 우선주제와 닿아있으나 TSP 솔버 도메인임.</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2609.27773'>Beyond Unsafe Detection: Counterfactually Anchored Evidence Attribution for Multi-Turn LLM Safety Failures</a></td><td>35</td><td>2</td><td>NLP Safety</td><td>multi-turn LLM 안전 실패를 turn/token 단위로 attribution하는 방법인데 counterfactual reasoning과 맞닿아 있지만 물리적 embodiment는 없음</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2609.28182'>Finite-Sample Probabilistic Safety Certification for AI-Based Grid-Edge Coordination</a></td><td>35</td><td>2</td><td>Safety Certification/MARL</td><td>그리드 엣지 제어용 AI 모델을 finite-sample binomial inference로 안전 인증하는 프레임워크로 방법론은 탄탄하나 전력망 도메인에 국한됨</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2609.28473'>On the Diffusibility of High-Dimensional Latents</a></td><td>35</td><td>1</td><td>Generative Models</td><td>고차원 latent에서 velocity prediction 대신 x0-prediction이 신호 매니폴드 학습에 더 효율적임을 보인 분석, RAE 기반 diffusion의 일반 원리를 다루나 robotics 응용은 없음</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2609.26913'>COMED: The Missing Middle Between Routing and Collaboration in Multi-LLM Inference</a></td><td>35</td><td>1</td><td>NLP</td><td>여러 LLM 간 선택적 협업을 위한 controller 제안, 순수 NLP 인프라 논문이라 로봇학습과 무관함</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2609.27372'>Neither Silence nor Overlap Is Failure: Intent-Conditioned Evaluation of Turn-Taking in Full-Duplex Spoken Dialogue Models</a></td><td>35</td><td>1</td><td>NLP</td><td>full-duplex 음성대화의 turn-taking을 화자 의도 조건부로 평가하는 벤치마크, 로봇학습과 무관함</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2609.27203'>XLOG: A CUDA-Native Engine for Neurosymbolic Integration</a></td><td>35</td><td>1</td><td>Neurosymbolic/Systems</td><td>신경 지각과 Datalog·확률추론을 GPU에서 통합한 xlog 엔진으로 caching·join 최적화에서 큰 속도 향상을 보였지만 로봇 적용은 없는 시스템 논문임</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2609.27332'>Stable Geometry with Divergent Task Evidence for Efficient Long-Horizon Agent Compression</a></td><td>35</td><td>1</td><td>Agent Memory</td><td>geometric redundancy만으로는 안전한 압축을 보장 못한다는 것을 보이고 evidence 보존을 우선하는 GEM을 제안한 agent history 압축 연구임</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2609.27220'>LOCKR: A Hidden-State Trajectory-Guided Planner for Detecting and Repairing Stable-but-Wrong Lock-In in Diffusion Language Models</a></td><td>35</td><td>0</td><td>NLP</td><td>diffusion LM의 조기 고착 오류를 hidden state 궤적으로 탐지·복구하는 test-time planning 방법, 로봇학습과는 무관하나 test-time repair 아이디어는 참고할 만함</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2609.27225'>Meet, Compare, or Abstain: LatWeave for Deterministic Multi-Hop Question Answering on Knowledge Lattices</a></td><td>35</td><td>0</td><td>NLP</td><td>지식을 격자구조로 조직해 결정적 연산으로 multi-hop QA를 수행하는 neurosymbolic 방법, 완전성 있는 지식에서만 강해 적용범위 좁고 로봇학습과 무관함</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2609.27233'>Distilling Sequential Computation in Transformer Language Models</a></td><td>35</td><td>0</td><td>LG</td><td>인접 토큰 구간을 하나의 대체 임베딩으로 압축해 추론시 시퀀스 길이를 40%까지 줄이는 방법, 로봇학습과 무관한 효율화 논문임</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2609.27380'>MORSE: Multi-Context Ordering via Reverse Scoring for Evidence-Preserving Compression</a></td><td>35</td><td>0</td><td>NLP</td><td>context 압축 시 순서에 따라 근거 보존율이 달라지는 information preemption 현상을 발견하고 순서 최적화로 개선, 로봇학습과 무관함</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2609.27396'>When Parallel Drafter Meets Parallel Speculative Decoding</a></td><td>35</td><td>0</td><td>LG</td><td>diffusion 기반 parallel drafter와 speculative decoding을 결합해 3배 이상 가속한 방법, 로봇학습과 무관한 효율화 논문임</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2609.27510'>Uncheatable Eval: Dynamic Compression-Based Evaluation of Language Models</a></td><td>35</td><td>0</td><td>NLP</td><td>압축률을 이용해 오염에 강한 LLM 평가를 수행하는 동적 벤치마크, 80개 모델로 검증했으나 로봇학습과 무관함</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2609.27981'>Risk-Controlled KV-Cache Eviction: From Memory Budgets to Risk Targets</a></td><td>35</td><td>0</td><td>LLM Efficient Inference</td><td>KV-cache eviction을 finite-sample risk 인증 문제로 재구성한 점은 방법론적으로 깔끔하지만 로봇과 무관한 LLM serving 문제임</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2609.28117'>Scaling Attention Head Analysis via Gradient-Based Attribution in Context-Aware Machine Translation</a></td><td>35</td><td>0</td><td>NLP/Interpretability</td><td>gradient 기반 attention head attribution으로 MT 중의성 해소를 분석한 해석가능성 연구지만 로봇 적용점은 없음</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2609.27051'>Propose, Don&#x27;t Judge: An Anytime-Valid Referee for LLM Agents That Mine Investment Factors</a></td><td>35</td><td>0</td><td>Finance/Agent</td><td>투자 팩터 채굴 에이전트에 frozen statistical referee를 두어 false discovery를 통제하는 governed self-evolution 구조로 금융 도메인에 국한됨</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2609.27333'>Alignment Inertia: Auditing the Durability of Training Data Influence Through Policy Override Resistance</a></td><td>35</td><td>0</td><td>Alignment/Safety</td><td>system prompt·fine-tuning이 이전 훈련 행동을 override하는 정도를 측정하는 alignment inertia 지표를 제안한 감사 연구임</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2609.27336'>CART: Closed-Loop Adaptive Red Teaming for Large Language Models</a></td><td>35</td><td>0</td><td>LLM Safety</td><td>이전 결과로 다음 테스트를 유도하는 closed-loop red teaming CART로 정적 replay보다 더 많은 실패를 찾아냈지만 로봇과 무관함</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2609.27756'>Reporting Under Pressure: Separating Factual and Tonal Sycophancy in LLM Statistical Analysis</a></td><td>35</td><td>0</td><td>NLP/LLM Behavior</td><td>통계 보고에서 사실적 sycophancy와 어조 sycophancy를 분리해 측정한 4x4 팩토리얼 실험으로 방법은 깔끔하지만 로봇과 무관함</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2609.27763'>Alignment of LRMs via Counter-Aligned Few-Shot Conversation Exposure</a></td><td>35</td><td>0</td><td>LLM Safety</td><td>counter-aligned few-shot 대화로 reasoning model을 조종하는 공격(SRCF)과 방어(ARCF)를 함께 제시한 안전성 연구임</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2609.27844'>Agentic Governance and Adversarial Verification for Policy-Constrained LLM Healthcare Appeal Generation</a></td><td>35</td><td>0</td><td>Agent/Healthcare</td><td>의료 이의신청 생성을 CMDP로 정식화해 인용 근거 없는 주장 발생을 이론적으로 차단한 AGVF로 형식적 보증은 있으나 의료 도메인 특화 응용임</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2609.27077'>Fast Direction-Conditioned Reachability for Motion Prediction Under Model Uncertainty</a></td><td>34</td><td>6</td><td>Motion Planning/Reachability</td><td>모델 불확실성이 있을 때 특정 방향으로만 reachable set을 빠르게 계산하는 direction-conditioned 방법을 제안함. 재계획 주기 단축에는 유효하나 특정 방향 질의로 한정된 실용적 개선임.</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2609.27547'>EBRL: Asynchronous Embodied RL by Multi-Grained Resource Management</a></td><td>34</td><td>5</td><td>Embodied RL/Systems</td><td>embodied RL의 rollout-training 비동기화와 자원관리로 처리량을 높인 시스템 논문임. embodied RL 인프라 기여지만 학습 알고리즘 자체의 새로움은 크지 않음.</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2609.27088'>Water Surface Swimming in a Centipede and its Robophysical ModeL</a></td><td>34</td><td>5</td><td>Bio-inspired Robotics</td><td>다지 로봇과 지네가 수면에서 direct wave로 오히려 전진하는 현상을 robophysical model로 규명함. 기초과학적 발견이나 조작·VLA 등 우선주제와는 거리가 있음.</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2609.27667'>Robust Adversarial Reinforcement Learning with Risk Sensitivity and Critic Consistency Regularization</a></td><td>34</td><td>3</td><td>RL/Robust Control</td><td>risk-sensitive 관점에서 adversarial RL의 불안정성을 critic consistency로 완화한 RACER 제안임. continuous control 벤치마크라 robot RL에 일부 참고 가능함.</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2609.27421'>Counterfactual Constraint-Conditioned On-Policy Distillation for Multi-Constraint Instruction Following</a></td><td>34</td><td>2</td><td>LLM/Counterfactual</td><td>다중 제약 instruction following에서 제약을 하나씩 빼는 counterfactual 방식으로 distillation 신호를 만드는 방법임. counterfactual reasoning 아이디어는 참신하나 도메인이 LLM instruction following임.</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2609.27144'>Learning Risk Scores Robust to Unobserved Confounders</a></td><td>34</td><td>1</td><td>Causal Inference/LG</td><td>unobserved confounding에 강건한 risk score 학습을 IPW와 distributionally robust optimization으로 결합함. 방법론은 탄탄하나 응용이 자원배분 문제라 robotics와 거리 있음.</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2609.27166'>Scaling of Capability and Efficiency at Inference Time in Large Reasoning Models</a></td><td>34</td><td>1</td><td>LLM/Reasoning</td><td>reasoning LLM의 capability-efficiency scaling을 계층적 베이지안 모델로 분석함. 흥미로운 실증이나 CoT 산술 추론에 국한됨.</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2609.27572'>DCRL: Decoupling and Coupling Reinforcement Learning via Policy-Reward Manifold Alignment</a></td><td>34</td><td>1</td><td>RL/LLM Reasoning</td><td>reasoning을 세 개의 sub-manifold로 보고 policy-reward 정합을 맞추는 RL 프레임워크임. 기하학적 해석이 흥미로우나 LLM reasoning 도메인 한정임.</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2609.27003'>Learning Expressive Humanoid Locomotion from Monocular Runway Videos for Robot Fashion Shows</a></td><td>33</td><td>6</td><td>Humanoid Locomotion/Motion Imitation</td><td>런웨이 영상에서 모션을 추출해 휴머노이드 캣워크 보행 정책을 학습하고 실기체 배포까지 성공함. 파이프라인 엔지니어링 성격이 강하고 응용이 패션쇼로 니치함.</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2609.27363'>From LiDAR Maps to Visual Localization: Unified Visual Association for Robust Point-Line-Plane Pose Estimation</a></td><td>33</td><td>4</td><td>3D Vision</td><td>LiDAR맵 기반 시각 localization 프레임워크, SLAM 엔지니어링 개선에 가까움</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2609.27475'>RoboCafé in the Open: Interaction Continuity in Long-Term Public Human-Robot Interaction</a></td><td>33</td><td>4</td><td>Embodied AI</td><td>장기 공공 HRI 배포 연구(12일, 148건 주문)로 관찰 위주 systems 논문, 로봇학습 핵심주제와는 거리 있음</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2609.27441'>Stable Neural Decoding Across Sessions via Task-Conditioned Latent Alignment for Brain-Machine Interfaces</a></td><td>33</td><td>3</td><td>BMI/Neural Decoding</td><td>task-conditioned latent alignment로 세션 간 신경 디코딩을 안정화한 BMI 연구임. embodied 제어 신호 디코딩이라 일부 관련 있으나 로봇 실험은 아님.</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2609.27554'>PhyMo: A Physical-Field Modality for Multimodal AI4Physics</a></td><td>33</td><td>2</td><td>Multimodal/AI4Physics</td><td>PDE 연산자 기반 physical-field modality를 도입한 멀티모달 프레임워크임. world model적 아이디어와 닿아있으나 물리 시뮬레이션 도메인 실험뿐임.</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2609.28325'>Motoneuron-Inspired Sampling for Model Predictive Path Integral Control</a></td><td>32</td><td>5</td><td>RL</td><td>운동뉴런에서 착안한 구조적 샘플링으로 MPPI 제어 매끄러움을 개선, MuJoCo Ant 하나만 검증해 근거가 제한적임</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2609.28027'>Learning a Speed-adaptive Hip Exoskeleton Control Policy Via Sim-to-real Reinforcement Learning</a></td><td>32</td><td>3</td><td>RL</td><td>고관절 외골격에 sim-to-real RL과 선호학습을 결합한 개인화 보조, 로봇학습 핵심주제와는 거리 있는 응용 연구임</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2609.27865'>What Changed? Drift Detection with Real, Virtual, and Incomparable Diagnosis</a></td><td>32</td><td>2</td><td>OOD/Drift Detection</td><td>공유 인코더 위에서 relational vs functional drift를 분리하는 two-discriminator 방법임. failure detection 문제의식과 닿아있으나 이미지 분류 도메인 실험뿐임.</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2609.28116'>Probabilistic and Geometry Aware Neural Surrogate of Scrape Off Layer Plasma Simulations</a></td><td>32</td><td>1</td><td>Scientific ML/Surrogate Modeling</td><td>conditional flow matching으로 tokamak 경계 플라즈마의 다중모드 상태를 확률적으로 대리모델링한 논문임. 확률적 surrogate라는 아이디어는 world model과 닿아있으나 플라즈마 물리 도메인임.</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2609.27395'>PRISM-VLM: A Multi-Axis Discriminative Benchmark for Compact Vision-Language Models</a></td><td>32</td><td>1</td><td>Multimodal</td><td>소형 VLM을 7개 축으로 평가하는 다축 벤치마크, 로봇학습과는 거리 있으나 멀티모달 평가방법론으로 참고 가능함</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2609.27279'>EnSIMem: Entity-Structured Indexing for Long-Term Agent Memory</a></td><td>32</td><td>1</td><td>Agent Memory</td><td>엔티티 구조화 인덱싱으로 장기 대화 기억을 구성하는 EnSIMem으로 엔지니어링 성격이 강한 메모리 아키텍처임</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2609.27298'>StateComp: Learning When to Compress History in Long Horizon Agents</a></td><td>32</td><td>1</td><td>Agent Memory</td><td>state 조건부로 history 압축 시점을 학습하는 StateComp로 이번 배치의 여러 agent-memory 압축 연구 중 하나이며 토큰을 52% 줄였지만 novelty는 제한적임</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2609.27032'>LexLattice: Multilingual Extractive Summarization via Neural Cellular Automata on Document Hierarchies</a></td><td>32</td><td>0</td><td>NLP</td><td>neural cellular automata로 문서 계층을 통합해 추출요약하는 방법, 파라미터 효율은 흥미로우나 로봇학습과 무관함</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2609.27603'>When Context Misleads: In-context Learning with Jurisdiction in Large Language Models</a></td><td>32</td><td>0</td><td>NLP</td><td>ICL이 잘못된 문맥을 맹신하는 취약점을 context 권위판단으로 보완하는 post-training 방법, 로봇학습과 무관함</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2609.27154'>HINT-Blimp: Human INTent Inference from Multimodal Cues for Robotic Blimps</a></td><td>31</td><td>6</td><td>HRI/Intent Inference</td><td>물리적 push와 음성 명령으로 human intent를 particle filter로 추정해 블림프를 제어하는 HINT-Blimp를 제안함. 다수 참여자 실험은 있으나 방법 자체는 기존 particle filter 활용에 가까움.</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2609.27340'>Spatial and Semantic Reasoning for LLM-Driven Robot Navigation via MCP</a></td><td>30</td><td>5</td><td>Navigation</td><td>LLM-ROS 연동 위한 MCP 래퍼 제안이라 엔지니어링 통합 수준, formulation novelty 약함</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2609.27466'>A Modular Dual-Arm Robotic Cell for Disassembly and Repair of Industrial Control Electronics</a></td><td>30</td><td>5</td><td>Manipulation</td><td>산업용 전자기기 분해수리용 듀얼암 셀 통합 시스템 논문, 아키텍처 통합 위주라 새 학습 방법론 없음</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2609.27227'>Surgical Kinematics from Monocular Video with Learned Articulated Motion Constraints</a></td><td>30</td><td>4</td><td>Robotics</td><td>단안 영상에서 수술 기구 kinematics를 복원하는 방법, LiveMAE 대비 오차 감소 있으나 수술 로봇 상태추정이라는 좁은 응용임</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2609.28466'>The Past Frames the Future: Memory for Autoregressive Video Generation</a></td><td>30</td><td>4</td><td>World Model</td><td>autoregressive 비디오 생성의 memory 메커니즘을 형태·기능·연산·학습·평가 5축으로 정리한 survey, world model의 장기 지속성 문제를 체계화했으나 원 연구가 아니라 리뷰라 실증적 기여는 없음</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2609.27938'>Remote Surfaces at Your Fingertips: Electrovibration-Based Tactile Feedback for Robot Teleoperation via Touchscreen Interfaces</a></td><td>30</td><td>4</td><td>Robotics</td><td>터치스크린 전기진동 촉각 피드백으로 원격조작 개선하는 HCI 연구, 로봇학습 우선주제와는 거리 있는 사용자연구 위주 논문임</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2609.28172'>Dynamic, Decentralized Spatial Code Reuse for OCDMA LiDAR in Robot Swarms</a></td><td>30</td><td>4</td><td>Robotics</td><td>로봇 군집용 LiDAR 코드 재사용을 분산 프로토콜로 스케일링한 통신 이론 논문, 로봇학습 우선주제와는 거리 있음</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2609.28179'>GLASS: Architecture-Tuned, Composable, Device-Side Linear Algebra for Edge Robotics and Beyond</a></td><td>30</td><td>4</td><td>Robotics</td><td>엣지 로봇용 GPU 선형대수 라이브러리로 최대 73배 속도 개선 보이나 학습 방법론이 아닌 시스템 인프라 논문임</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2609.27821'>Groundbench: Multi-Resolution Polygon Grounding Exposes the Geometry Gap in Vision-Language Models</a></td><td>30</td><td>3</td><td>Multimodal</td><td>bounding box 대신 다중 해상도 폴리곤으로 visual grounding을 재정의해 VLM의 geometry gap을 드러낸 벤치마크, 진단적 가치는 있으나 방법 제안은 없음</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2609.27890'>RelCheck: Dual-Evidence Spatial Grounding for VLM Hallucination Correction</a></td><td>30</td><td>3</td><td>Multimodal</td><td>scene graph와 bbox 기하 정보를 결합해 VLM의 관계적 hallucination을 post-hoc 교정하는 training-free 파이프라인, MME position subtask에서 큰 개선이나 관계 하나에 국한된 보정임</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2609.27394'>Automotive mmWave Spinning Radar Place Recognition with Spatially Gated Feature-Correlation Representation</a></td><td>30</td><td>3</td><td>Navigation</td><td>차량용 레이더 place recognition 개선, 로봇학습 우선주제와는 거리 있는 지각 모듈 논문임</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2609.27728'>NeuralSRNF: Neural Square Root Normal Fields for the Statistical Shape Analysis and Generation of Nonrigid 3D and 4D Objects</a></td><td>30</td><td>2</td><td>3D Vision</td><td>SRNF의 비가역성 문제를 신경망으로 풀어 4D 형상 통계분석을 빠르게 만든 방법, 계산효율 개선은 크지만(3초 vs 10분) 응용이 형상 통계·생성에 국한되고 robot task 연결은 없음</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2609.27868'>TopoGS: Topology-Aware Anchor Feature Aggregation for Large-Scale 3D Gaussian Splatting</a></td><td>30</td><td>2</td><td>3D Vision</td><td>octree 기반 대규모 3DGS에서 계층 간 feature aggregation을 비대칭적으로 설계한 방법, PSNR 개선은 있으나 렌더링 품질 최적화 수준의 엔지니어링임</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2609.27866'>A Shared Encoder Is Not a Shared Task: Conditional Comparison for Deep Expert Pools</a></td><td>30</td><td>2</td><td>OOD/Drift Detection</td><td>위 27865와 초록이 거의 동일한 짧은 버전 논문임. 같은 conditional comparison 방법으로 동일한 결론을 반복함.</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2609.28085'>Curriculum Learning with GNN-based Reinforcement Learning for Job Shop Scheduling</a></td><td>30</td><td>2</td><td>RL/Combinatorial Optimization</td><td>GNN 기반 RL job shop scheduling에 curriculum learning을 적용해 학습시간을 줄인 연구임. 스케줄링 문제라 TAMP와 유사하나 로봇 실험은 없음.</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2609.26866'>Marginally Correct Tool Caches Can Reverse Group-Normalized Policy Updates</a></td><td>30</td><td>1</td><td>RL</td><td>tool-result 캐시 공유가 rollout marginal 분포를 보존해도 group-normalized policy update의 방향을 뒤집을 수 있음을 이론적으로 규명한 논문, RL 학습 인프라의 숨은 버그를 밝힌 점이 흥미로우나 robotics 응용은 아님</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2609.27067'>ChipMEM: Verification-Grounded Memory for EDA Agents</a></td><td>30</td><td>1</td><td>LLM Agent</td><td>EDA agent용 검증 기반 메모리 레이어 제안임. 도메인이 반도체 설계라 robotics와 무관하고 개선폭도 제한적임.</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2609.26826'>What Makes a Terminal-Bench Task Hard? Separating Genuine Hardness from Fake-Hardness on an Adjudicated Agentic Corpus</a></td><td>30</td><td>0</td><td>LG</td><td>Terminal-Bench의 all-fail 태스크가 진짜 난이도인지 오라클 결함·인프라 실패인지 감사한 메타연구, 벤치마크 신뢰성에 대한 방법론적 기여이나 robotics 무관함</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2609.27234'>Discover, Falsify, Revise: Auditing Input-Use Claims from Source Code to Predictive Contribution in Agent-Discovered Cell Models</a></td><td>30</td><td>0</td><td>AI4Science/Agent</td><td>agent가 생성한 cell 예측 모델의 input-use claim을 falsification으로 감사하는 프레임워크임. 참신하나 도메인이 세포생물학이라 robotics와 무관함.</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2609.27964'>Linear RNN Scaling Laws: When Longer Sequences Beat More Sequences</a></td><td>30</td><td>0</td><td>Scaling Theory</td><td>선형 RNN teacher-student 모델에서 시퀀스 길이 대 개수 트레이드오프를 이론적으로 규명한 논문임. 순수 이론이라 robotics 실험 없음.</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2609.28080'>Reference-Based Analysis of Coherence and Diversity in Open-Ended Text Generation</a></td><td>30</td><td>0</td><td>NLG</td><td>개방형 텍스트 생성의 coherence·diversity를 human reference와 비교 분석하는 연구로 방법론적 참신성이 크지 않음</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2609.28270'>Predicting Quantization Price for Selecting PTQ Configurations Before Deployment</a></td><td>30</td><td>0</td><td>Efficient Inference</td><td>PTQ 설정을 배포 전에 curvature 기반 price로 선택하는 이론적 틀이지만 결국 quantization efficiency 기여임</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2609.26929'>Which Objectives Need a Dial? Predicting Objective Conflict and Covering Trade-offs in Steerable Pluralistic Alignment</a></td><td>30</td><td>0</td><td>RLHF/Alignment</td><td>MODPO 기반 pluralistic alignment에서 목표 간 충돌 예측과 trade-off 커버리지를 다룬 응용 연구임</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2609.27150'>Do We Need Complex Topology Control? Distinct-Peer Random Routing Improves Cost-Efficiency in Sparse Multi-Agent Debate</a></td><td>30</td><td>0</td><td>Multi-Agent LLM</td><td>복잡한 topology control 없이 무작위 peer 라우팅만으로 sparse multi-agent debate 비용 효율을 개선한 실증 연구임</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2609.28322'>Learning the Cost of Reliable Inference</a></td><td>30</td><td>0</td><td>LLM Systems/Market Design</td><td>reverse second-price auction으로 LLM 제공자 간 가격 경쟁을 유도하는 라우팅 플랫폼 설계 연구임</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2609.28165'>Confidence Falls Short: Asymmetric Certainty Gains from Optimization Hinder Multimodal Classification</a></td><td>29</td><td>2</td><td>Multimodal Learning</td><td>멀티모달 학습에서 강한 모달리티가 더 과신하게 되는 비대칭 확신도 문제를 규명하고 MaxCR로 보정함. multimodal foundation model 우선주제와 약하게 관련 있음.</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2609.27987'>PCQC: Privileged Counterfactual Question Credit for Multi-Turn Medical Dialogue</a></td><td>29</td><td>1</td><td>RL/Dialogue</td><td>privileged 환자정보로 묻지 않은 질문의 counterfactual credit을 학습하는 PCQC를 제안함. counterfactual credit assignment 아이디어는 있으나 의료 대화 도메인임.</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2609.28409'>Learning Holographic Reduced Representations with Clifford Variational Autoencoders</a></td><td>29</td><td>1</td><td>Representation Learning/VSA</td><td>Clifford torus에 투영하는 VAE로 vector symbolic algebra의 binding 성능을 높인 Clifford-VAE 제안임. 상징적 표현 학습이 scene graph적 아이디어와 약하게 닿아있으나 이미지 분류 실험뿐임.</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2609.27306'>Discrete Diffusion Models via Evolving Variational Autoregressive Networks</a></td><td>29</td><td>0</td><td>Generative Models</td><td>variational autoregressive network로 정규화된 discrete diffusion을 구현해 Ising model에 적용함. 물리 시스템 샘플링 문제라 robotics 관련성 낮음.</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2609.27593'>Hidden not Deleted: How Networks Suppress Entangled Features</a></td><td>29</td><td>0</td><td>Interpretability</td><td>선형 개념 삭제가 dense superposition에서 실패하는 이유를 회로 수준에서 규명한 분석 논문임. LLM unlearning 메커니즘 연구로 robotics와 무관함.</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2609.27099'>Design and Modeling of a Single-Port Three-Arm Robotic Tool for Minimally Invasive Neurosurgery</a></td><td>28</td><td>5</td><td>Surgical Robotics/Hardware</td><td>단일 포트 3암 수술 로봇 도구의 설계와 기구학 모델을 검증한 논문임. 하드웨어·모델링 기여이나 학습 요소는 없음.</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2609.27330'>A Sample-Based Approach for Hierarchical Information-Theoretic Compression of Probabilistic Occupancy Grids</a></td><td>28</td><td>4</td><td>Robotics</td><td>MCTS 기반 occupancy grid 압축 가속화라 기존 방법의 속도 개선에 그침, formulation 새로움 부족함</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2609.28078'>LiAM-SAM: Lifecycle-Aware Memory for Robust SAM2-Based MOT</a></td><td>28</td><td>3</td><td>CV</td><td>SAM2 기반 MOT의 생애주기(생성·드리프트·재식별)별로 메모리를 다루는 프레임워크, 붐비는 환경에서 큰 폭의 HOTA 개선을 보였으나 로봇 자체 embodied memory와는 다른 추적 문제임</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2609.27439'>Compressed delayed-information projection for six-degree-of-freedom underwater vehicle navigation under delayed acoustic positioning</a></td><td>28</td><td>3</td><td>Navigation</td><td>수중로봇 지연 음향 위치추정용 필터 기법, 추정이론 개선에 그침</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2609.27597'>Gray-Box Model Predictive Control for Articulated Dump Trucks via Gaussian Process Learning of Sideslip</a></td><td>28</td><td>3</td><td>RL</td><td>덤프트럭용 GP 기반 sideslip 학습 gray-box MPC, 광산 차량이라는 니치 응용의 점진적 개선임</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2609.27712'>Wave-Robust Passive AUV Localization Using FP-MUSIC</a></td><td>28</td><td>3</td><td>Navigation</td><td>부표 하이드로폰 배열로 수동 AUV 위치추정하는 신호처리 논문, 로봇학습 우선주제와 거리 있음</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2609.28317'>Multimodal Voice Activity Projection for Social Robot Mediation: Expected Behavior and Deployment Constraints</a></td><td>28</td><td>3</td><td>Embodied AI</td><td>사회로봇 중재를 위한 멀티모달 turn-taking projection 모델, HRI 응용 연구라 로봇학습 우선주제와는 거리 있음</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2609.28061'>AstraLOD3: Zero-shot multimodal agentic reconstruction of LOD3 building models</a></td><td>28</td><td>2</td><td>3D Vision</td><td>범용 foundation model 에이전트가 Python·Blender를 실행해 LOD3 건물 모델을 zero-shot 복원하는 프레임워크, 고정 파이프라인 대신 제약된 agentic process로 재정의한 점은 흥미로우나 로봇 embodiment와는 거리 있음</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2609.28300'>RoomLight: A 2.5D Illumination Prior for Indoor Environments</a></td><td>28</td><td>2</td><td>3D Vision</td><td>실내 illumination을 원거리 환경맵이 아닌 유한거리 emitter로 모델링하는 2.5D 조명 prior, inverse rendering 품질 개선이나 embodied task와 직접 연결되지 않음</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2609.26890'>PR-Smoother: Simulator-Preserving Non-Gaussian Smoothing for Data Assimilation</a></td><td>28</td><td>2</td><td>LG</td><td>prescribed simulator를 유지한 채 future-conditioned correction만 학습하는 non-Gaussian smoother, Kolmogorov flow 같은 고차원 물리 시스템에 확장 가능하나 robotics 적용은 제시 안 됨</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2609.27248'>Repurposing Pre-trained LLMs as High Fidelity Continuous Text Autoencoders</a></td><td>28</td><td>0</td><td>Generative Models/NLP</td><td>사전학습 LLM을 continuous text autoencoder로 재활용하는 방법임. 텍스트 생성 도메인이라 robotics와 무관함.</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2609.27867'>Evaluation Choices Decide the Forecasting Leaderboard: Evidence from a Production Marketplace Panel</a></td><td>28</td><td>0</td><td>Forecasting Methodology</td><td>평가 설계 선택이 예측 리더보드 순위를 뒤집는다는 실증 사례 연구임. 방법론적으로 흥미로우나 수요예측 도메인이라 robotics와 무관함.</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2609.28385'>When and Where to Trust the Teacher: Unifying On-Policy Distillation and GRPO through Entropy-Calibrated Credit Assignment</a></td><td>28</td><td>0</td><td>RL/LLM Reasoning</td><td>OPD와 GRPO 신호를 엔트로피로 보정해 결합한 UECR-GRPO를 제안함. 수학 추론 벤치마크 개선 위주라 robotics와 무관함.</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2609.27059'>The Illinois Social Attitudes Aggregate Corpus (ISAAC): An Open Tool and Reproducible Pipeline for Analyzing Social Group Discourse at Scale</a></td><td>28</td><td>0</td><td>NLP</td><td>5억건 규모 레딧 사회집단 담론 코퍼스 구축 논문, 대규모 자원이지만 로봇학습과 무관함</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2609.27064'>What Changes When Fact-Verification Scores Improve? Evidence and Answer Accounting Across Trained Verifiers and LLMs</a></td><td>28</td><td>0</td><td>NLP</td><td>fact-verification 점수 향상의 원인을 답변과 근거로 분해해 정량화한 방법론 논문, 로봇학습과 무관함</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2609.27165'>Count Evidence, Not Sentences: Tempered Evidence Fusion of LLM Judgments for Long-Text Value Measurement</a></td><td>28</td><td>0</td><td>NLP</td><td>긴 텍스트의 가치판단 측정을 문장별 정보량 가중 융합으로 개선한 방법, 로봇학습과 무관한 NLP 응용 논문임</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2609.27262'>Can One Adapted Model Do It All? Fine-Tuning Strategy Selection for Customer Support LLMs</a></td><td>28</td><td>0</td><td>NLP</td><td>고객지원 LLM에서 멀티태스크 fine-tuning이 최선임을 13개 모델 200개 체크포인트로 실증한 연구, 로봇학습과 무관함</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2609.27590'>MWE-ECL: Recoverable Long-Range Context Does Not Always Override Local Lexical Priors</a></td><td>28</td><td>0</td><td>NLP</td><td>장거리 문맥이 검색 가능해도 지역적 어휘선호를 못 뒤집는 현상을 진단하는 벤치마크, 로봇학습과 무관함</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2609.27607'>Can Jev Judge Radiology Reports? Evaluating a System One Model for Clinical Factuality</a></td><td>28</td><td>0</td><td>NLP</td><td>방사선 판독문의 사실성 평가를 위한 저비용 judge 모델, 로봇학습과 무관한 임상 NLP 논문임</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2609.28272'>Towards Efficient Reasoning: Learning Causal Shortcuts for Diffusion Language Models</a></td><td>28</td><td>0</td><td>Diffusion LM</td><td>causal shortcut 토큰에 마스킹을 집중시키는 SFT 기법으로 MATH-500에서 4.2%p 개선에 그치는 incremental 기여임</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2609.27517'>Not What You Meant: Can LLMs Follow a Specified Negation Semantics?</a></td><td>28</td><td>0</td><td>NLP/Logic</td><td>지정된 부정 의미론을 LLM이 따르는지 측정하는 NAFBench로 논리 추론의 세밀한 실패를 드러냈지만 로봇과 무관함</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2609.27219'>Vision-Based Control of a Tether-Suspended Aerial Radiation Sensing Payload</a></td><td>27</td><td>6</td><td>Aerial Robotics/Control</td><td>테더로 매단 방사선 센서 페이로드를 비전 기반 LQR로 제어해 추적오차를 줄인 논문임. 응용은 명확하나 제어 기법 자체는 표준적인 칼만필터+LQR 조합임.</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2609.27221'>Tail-Aware Geometry Learning for Conformal Ellipsoids</a></td><td>27</td><td>1</td><td>Uncertainty Quantification</td><td>conformal ellipsoid의 tail-aware geometry 학습법임. 이론적으로 깔끔하나 robot perception 적용 실험은 없음.</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2609.27409'>Active Learning for Biodiversity Monitoring: From Label Efficiency to Reliable Ecological Inference</a></td><td>27</td><td>1</td><td>Active Learning</td><td>생물다양성 모니터링에서 능동학습 예산 배분 문제를 정리한 서베이·튜토리얼 성격 논문임. active perception과 결이 비슷하나 도메인이 생태 데이터라 관련성 낮음.</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2609.27739'>MENO: Memory-Efficient Neural Operator</a></td><td>27</td><td>1</td><td>Neural Operator</td><td>메모리 효율적인 PDE neural operator MENO 제안임. 임의 기하·이산화를 다루는 점은 흥미로우나 robotics 실험은 없음.</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2609.27963'>I-SplineFlow: Learning Monotone Spline Stochastic Interpolant Schedulers for Few-Step Generation</a></td><td>27</td><td>1</td><td>Generative Models</td><td>I-spline으로 diffusion/flow 스케줄러를 파라미터화해 few-step 생성 품질을 높인 방법임. 생성모델 가속 기여로 world model 생성 파트에 참고 가능하나 직접 실험은 없음.</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2609.27294'>KITE: KV-Invariant Transformer Expansion for Efficient Agentic LLM Scaling</a></td><td>27</td><td>0</td><td>LLM Scaling</td><td>KV 캐시 비용을 줄이는 transformer 확장 구조 KITE/SST 제안임. LLM 추론 효율화 위주 기여임.</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2609.27588'>The Capability Manifold and ML Scaling Laws</a></td><td>27</td><td>0</td><td>LLM Scaling Theory</td><td>downstream capability를 자원에 매핑하는 capability manifold 개념 프레임워크임. 초기 적용 사례뿐이라 실증 근거가 약함.</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2609.27679'>What Do Tabular Foundation Models Compute In Context? In-Situ Representation Refinement through Attention-Gated Updates</a></td><td>27</td><td>0</td><td>Tabular Foundation Models</td><td>tabular foundation model의 in-context 연산을 attention-gated update로 분석·개선한 논문임. 정형데이터 도메인이라 robotics와 무관함.</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2609.28442'>Order-Invariant Answers, Order-Sensitive Representations in Mathematical Reasoning</a></td><td>27</td><td>0</td><td>Interpretability/Reasoning</td><td>규칙 순서를 바꿔도 답은 같지만 내부 표현은 다르다는 것을 SNR로 정량화한 분석 논문임. LLM 수학 추론 해석 연구로 robotics와 무관함.</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2609.28377'>Amplify: A Lightweight Library for Reproducible Nonlinear Programming Problems in Robotics</a></td><td>25</td><td>4</td><td>Robotics</td><td>궤적최적화 재현성을 위한 경량 AMPL 기반 라이브러리, 방법론 novelty보다는 도구 제공에 가까움</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2609.27677'>RoadOcc Learns When to Persist, Transport, or Refresh Memory for Roadside Occupancy Prediction</a></td><td>25</td><td>3</td><td>Autonomous Driving</td><td>고정 카메라 점유 예측에서 과거 기억을 유지·이동·갱신할지 학습하는 라우팅 방법, InfraOcc에서 개선폭 있으나 로드사이드 인프라라는 좁은 도메인임</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2609.26979'>Resource-Efficient Distributed Recursive Gaussian Processes</a></td><td>25</td><td>3</td><td>LG</td><td>다중 에이전트가 통신을 줄이며 통합 Gaussian process 모델을 유지하는 분산 recursive GP 두 가지, multi-robot 분산 추정에 응용 가능하나 검증은 풍력 데이터에 그침</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2609.27139'>A Hierarchy-Aware Video-Language Model Evaluation and Hyperbolic Baseline for Surgery</a></td><td>25</td><td>2</td><td>Video</td><td>수술 영상의 phase-step 계층을 hyperbolic embedding으로 반영한 평가 벤치마크, 수술 로봇과 거리 있고 방법도 기존 hyperbolic 기법 적용 수준임</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2609.27470'>DeltaS: Reading the Gated Linear Attention State for KV Cache Eviction in Streaming Video</a></td><td>25</td><td>2</td><td>Video</td><td>gated-delta linear attention의 state drift를 이용한 training-free KV cache eviction, streaming video efficient inference 기여이고 robotics 응용은 없음</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2609.27794'>DMM-Align: Closed-Loop Optimization for 2D-3D Registration with Dual-Role Diffusion</a></td><td>25</td><td>2</td><td>3D Vision</td><td>correspondence-pose-representation 학습을 diffusion으로 closed-loop 결합한 2D-3D registration 방법, 저중첩·가림 상황에서 개선 있으나 robot pose estimation 응용은 제시 안 됨</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2609.26972'>TinyUDE: Solver-Free Universal Differential Equations on Microcontrollers via Lie-Taylor Jet Matching</a></td><td>25</td><td>2</td><td>LG</td><td>ODE solver 없이 Lie-Taylor jet matching으로 마이크로컨트롤러에서 UDE를 학습하는 방법, 임베디드 제어와 연관 가능하나 경량화 지향 연구라 우선 평가 대상은 아님</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2609.27901'>All modalities are equal, but video is more equal: Closing the Cross-Attention Gap in Joint Video Generation</a></td><td>25</td><td>1</td><td>Video</td><td>joint multimodal diffusion에서 비디오가 다른 모달리티를 덜 제약받는 비대칭성을 KL regularizer로 보정한 방법, 생성 품질 지표 개선이나 robotics 무관함</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2609.27606'>State-Grounded Conditioning: Wrapping User-Facing LLM Agents Where Direction Depends on Live State</a></td><td>25</td><td>1</td><td>Agent/Applied</td><td>게임 코칭 에이전트에서 live state와 응답 방향의 불일치를 줄이는 wrapper 설계로 특정 응용 엔지니어링에 가까움</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2609.26924'>nnFoundation: 3D Foundation Models for Radiology</a></td><td>25</td><td>0</td><td>CV</td><td>210만 볼륨으로 학습한 3D radiology foundation model, 스케일은 크지만 CNN/Transformer 상호보완 관찰이 주 기여라 개념적 novelty는 제한적임</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2609.27511'>NV-Reason-CT: 3D Visual Language Model for CT Analysis</a></td><td>25</td><td>0</td><td>CV</td><td>3D ViT와 LLM을 결합한 흉복부 CT 분석 모델, GRPO 학습과 대규모 데이터가 강점이나 robotics 무관한 의료 응용임</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2609.26811'>The Drift Contract: Spectral Updates for Depth-Robust Local Learning</a></td><td>25</td><td>0</td><td>LG</td><td>local learning에 Muon 스타일 spectral update를 적용해 깊이에 따른 붕괴를 줄인 방법, 소규모 CIFAR-10 실험 수준이고 robotics 무관함</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2609.26905'>CORE-STACK+: Meta-Learning for Deep Stacked Generalization</a></td><td>25</td><td>0</td><td>CV</td><td>CKA 기반 중복 제거와 spectrum-adaptive ridge로 vision backbone 스태킹을 개선한 앙상블 방법, PAC-Bayes bound를 제시하나 여러 컴포넌트 조합형 엔지니어링에 가깝고 robotics 무관함</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2609.27232'>A Scaling Study for fMRI Foundation Models</a></td><td>25</td><td>0</td><td>LG</td><td>fMRI foundation model의 scaling law를 대규모로 실증 분석함. 도메인 특화 연구라 robotics 관련성 낮음.</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2609.27912'>Global tree forecasters collapse at the hierarchical aggregate: a five-panel failure characterization</a></td><td>25</td><td>0</td><td>Forecasting</td><td>global tree forecaster가 계층 합산 시 붕괴하는 현상을 다섯 개 패널로 특성화한 연구임. 원인은 이미 알려진 것이라 novelty가 제한적임.</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2609.28022'>PISCES: Physics-Informed Solar-wind Convolutional autoEncoder for Space-weather Anomaly Detection and Early Warning</a></td><td>25</td><td>0</td><td>Space Weather/Anomaly Detection</td><td>물리 제약을 넣은 convolutional autoencoder로 태양풍 이상을 조기 경보하는 PISCES 제안임. 우주기상 도메인이라 robotics와 무관함.</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2609.26926'>Experts Rise Where LLMs Disagree: Using Cross-Model Disagreement to Target Expert Effort in LLM Codebook Revision for Large-Scale Annotation</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM 간 불일치를 활용해 전문가 검수 대상을 좁히는 annotation 방법론, 로봇학습과 무관한 응용 NLP 논문임</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2609.26976'>When Learned Context Planning Fails to Beat Strong Retrieval: A Controlled Study of Planning, Routing, and Reranking for Long-Context QA</a></td><td>25</td><td>0</td><td>NLP</td><td>long-context QA에서 learned planning이 강한 retrieval을 못 이긴다는 negative result 논문, 로봇학습과 무관함</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2609.27257'>UniDataAgent: An Ontology-Grounded Agent for Enterprise Question-to-Report Automation</a></td><td>25</td><td>0</td><td>NLP</td><td>기업용 온톨로지 기반 질의응답-리포트 자동화 시스템, 실배포 사례이나 로봇학습과 무관한 응용 논문임</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2609.27289'>Ruby-ASR: Evidence-Preserving Supervision for Joint Orthographic and Lexical-Reading Recognition</a></td><td>25</td><td>0</td><td>NLP</td><td>일본어 ASR에서 표기와 발음을 함께 지도학습하는 방법, 로봇학습과 무관한 음성인식 논문임</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2609.27418'>EviStreams: Human-in-the-Loop AI Data Extraction for Systematic Reviews in Medicine</a></td><td>25</td><td>0</td><td>NLP</td><td>의료 systematic review의 데이터추출을 인간개입형 AI로 지원하는 플랫폼, 로봇학습과 무관한 응용 도구 논문임</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2609.27758'>Hard Negatives Reveal What Easy Negatives Hide: Cross-Lingual Harmfulness Representations Degrade with Resource Tier Under Hard Negatives</a></td><td>25</td><td>0</td><td>NLP Safety</td><td>cross-lingual harmfulness representation의 hard negative 취약성 분석이라 안전성 진단 연구에 국한됨</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2609.28090'>Can LLMs Catch a Rigged Backtest? A Clean-Control Calibration Benchmark</a></td><td>25</td><td>0</td><td>NLP/Finance</td><td>조작된 백테스트를 LLM이 잡아내는지 재는 calibration 벤치마크로 특정 금융 도메인에 국한됨</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2609.28395'>Fine-Tuning LLMs for Translation: General Forgetting Mitigation Does Not Preserve MT-Specific Instruction Following</a></td><td>25</td><td>0</td><td>NLP/MT</td><td>번역 fine-tuning의 forgetting 완화가 MT-specific instruction following까지 보존하지 못함을 보인 응용 실험 연구임</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2609.27290'>Sparse-Observation Atmospheric Thermal Forecasting with Physics-Informed Neural Networks for Climate-Aware Digital Twins</a></td><td>25</td><td>0</td><td>Physics-ML</td><td>물리 제약 신경망으로 대기 온도를 예측하는 기후 디지털 트윈 응용 연구로 로봇과 무관함</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2609.27006'>Laser-Tracker-Assisted Camera-to-Robot Calibration for Mobile Robots</a></td><td>24</td><td>5</td><td>Calibration</td><td>레이저 트래커와 카메라를 결합한 모바일 로봇 hand-eye calibration의 일반화 버전임. 기존 방법의 가정을 완화한 엔지니어링 확장이라 novelty가 크지 않음.</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2609.27411'>When Labels Are Scarce: An Oscillatory State Space Model for Vibration Diagnosis</a></td><td>24</td><td>1</td><td>Signal Processing</td><td>진동 신호 기반 설비 고장진단용 경량 oscillatory state-space model임. 엣지 효율화 위주라 우선순위 낮게 평가함.</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2609.27036'>An open benchmark for machine learning-based polymer property prediction</a></td><td>24</td><td>0</td><td>LG</td><td>고분자 물성 예측용 벤치마크 구축 논문임. 데이터셋 기여이고 방법론 자체는 기존 GNN/descriptor 비교라 novelty가 낮음.</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2609.27199'>ZO-COSMO: Index-Free One-Hop Mixing for Decentralized Zeroth-Order Optimization</a></td><td>24</td><td>0</td><td>Distributed Optimization/LG</td><td>decentralized zeroth-order 최적화의 통신 효율화 논문임. LLM LoRA 실험 위주라 robotics 관련성 없음.</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2609.27291'>NGN: Learning Neural Network Size as a Differentiable Count</a></td><td>24</td><td>0</td><td>Architecture Search/LG</td><td>네트워크 크기를 differentiable count로 학습하는 방법임. 경량화 방향이라 우선순위 낮게 평가함.</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2609.27385'>Forecast Workflow Bench: Evaluating Language-Model Decisions with Budgeted Forecast Tools</a></td><td>24</td><td>0</td><td>LLM Agent/Time Series</td><td>예측 도구 비용을 고려해 LLM agent의 의사결정을 평가하는 벤치마크임. 전력/자전거 수요 예측 도메인이라 robotics와 무관함.</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2609.27473'>Learning Where to Look: A Shared Relative-Alignment Module for Time-Series Forecasting and PPG-to-Vital-Sign Reconstruction</a></td><td>24</td><td>0</td><td>Time Series</td><td>PPG-vital sign 재구성과 시계열 예측을 공유 모듈로 처리하는 방법임. 헬스케어·에너지 도메인이라 robotics와 무관함.</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2609.27657'>FLEET: From Logits Entropy to Enhanced Trajectories in Text Generation</a></td><td>24</td><td>0</td><td>Text Generation</td><td>logits entropy 기반 메모리로 반복 샘플링의 중복 생성을 줄이는 방법임. 텍스트/코드 생성 도메인이라 robotics와 무관함.</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2609.27860'>Exact Minimax One-Bit Unbiased Compression: Heavy-Tail Necessity and Finite-Randomness Approximation</a></td><td>24</td><td>0</td><td>Information Theory</td><td>1비트 unbiased 압축의 minimax 최적성을 규명한 이론 논문임. 통신이론 중심이라 robotics와 무관함.</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2609.27913'>Reliable Fusion of Conflicting Experts</a></td><td>24</td><td>0</td><td>Multi-Agent Fusion</td><td>확률회로 기반으로 여러 LLM expert 의견을 신뢰도에 따라 융합하는 방법임. QA 도메인 기여로 robotics와 무관함.</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2609.27932'>Binary Quantized Neural Network Training Is W[1]-Hard Parameterized by Input and Output Dimensions</a></td><td>24</td><td>0</td><td>Learning Theory</td><td>이진 quantized NN 학습이 입출력 차원 파라미터화에서 W[1]-hard임을 증명한 이론 논문임. 순수 계산복잡도 기여임.</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2609.27982'>Riemannian Structure and Optimization for a Class of Low-Parametric Orthogonal Matrices</a></td><td>24</td><td>0</td><td>Optimization/Geometry</td><td>block-diagonal 직교행렬 클래스의 Riemannian 구조와 최적화 알고리즘을 다룬 논문임. LLM PEFT 응용 위주로 robotics와 무관함.</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2609.28053'>Exact Quantile Balancing and Load-Error Injection for Mixture-of-Experts</a></td><td>24</td><td>0</td><td>LLM Training/MoE</td><td>MoE 학습에서 정확한 quantile balancing과 load-error injection으로 로드밸런스를 개선한 논문임. LLM infra 최적화 위주 기여임.</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2609.28212'>Log-Depth Recurrent Language Modeling</a></td><td>24</td><td>0</td><td>Language Model Architecture</td><td>balanced-tree recursive 연산자로 로그 깊이 autoregressive 언어모델을 구성한 논문임. 아키텍처 효율화 위주 기여임.</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2609.28399'>Memory Attention</a></td><td>24</td><td>0</td><td>Transformer Architecture</td><td>토큰 인덱스 메모리로 attention value 생성을 대체하는 Memory Attention 제안임. LLM 아키텍처 효율화 기여이며 robot memory와는 다른 개념임.</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2609.27577'>VCMM: Variance-Calibrated Momentum for Multimodal Learning</a></td><td>23</td><td>0</td><td>Multimodal Learning</td><td>모멘텀 옵티마이저의 모달리티 불균형을 보정하는 VCMM 제안임. 표준 벤치마크 개선 위주의 incremental 기여임.</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2609.28405'>Learning Collective Dynamics with Differentiable Gaussian Representations</a></td><td>23</td><td>0</td><td>Behavioral Modeling</td><td>Gaussian mixture와 differentiable aggregation으로 집단 행동 동역학을 학습하는 DGD 제안임. 추천·소매 데이터 도메인이라 robotics와 무관함.</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2609.27160'>Fine Wrist Control as a Marker of Surgical Teleoperation Expertise</a></td><td>22</td><td>4</td><td>Surgical Teleoperation/Human Factors</td><td>숙련자와 초심자의 손목 안정성을 모션 트래커로 비교한 인간공학 연구임. ML 기여가 거의 없는 인체 동작 분석 논문임.</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2609.28049'>Prompt, Probe, Train, or Annotate? Single-camera sports video understanding in amateur settings</a></td><td>22</td><td>1</td><td>Video</td><td>아마추어 배구 영상에서 prompting·특화 CV·world model·수동 라벨링을 단계별로 비교한 실증 연구, 방법론 novelty보다 현장 배포 관점의 벤치마킹임</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2609.28095'>MotionSpec: Spectral Trajectory Supervision for Motion-Consistent Video Generation</a></td><td>22</td><td>1</td><td>Video</td><td>궤적을 spectral 영역으로 변환해 motion consistency를 강화한 비디오 생성 supervision, 생성 품질 개선 위주라 robotics 응용은 제시 안 됨</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2609.26820'>Signal2Symbol: Neuro-Symbolic Temporal Reasoning for Explainable Physiological Time-Series Anomaly Detection</a></td><td>22</td><td>1</td><td>LG</td><td>ECG/EEG를 기호열로 변환해 rare itemset과 Allen 시간대수로 해석 가능한 이상탐지를 만든 neuro-symbolic 프레임워크, 생체신호 도메인 특화이고 robotics 무관함</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2609.27092'>Local Evidence and Geometric Readout Repair in Trained GNNs</a></td><td>22</td><td>0</td><td>GNN/LG</td><td>GNN readout 오류를 reweighting과 translation으로 분해하는 분석 논문임. 범위가 node classification에 국한된 incremental 기여임.</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2609.27209'>Scalable Subgraph Sampling via Resistance Curvature</a></td><td>22</td><td>0</td><td>GNN/LG</td><td>resistance curvature 기반 subgraph sampling 효율화 논문임. GNN 학습비용 절감 위주의 engineering 기여임.</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2609.27278'>Graph Learning with Spectral Connectivity Priors for Scarce Data</a></td><td>22</td><td>0</td><td>Graph Learning</td><td>데이터가 적을 때 spectral connectivity prior로 그래프를 학습하는 방법임. 응용이 신호처리 벤치마크에 국한됨.</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2609.27355'>Quantization-Robust Unlearning through the Lens of Retain-Forget Loss Landscapes Interaction</a></td><td>22</td><td>0</td><td>LLM Unlearning</td><td>quantization 이후에도 강건한 LLM unlearning 방법임. 모델 압축 강건성 문제라 우선주제와 무관함.</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2609.27581'>Does Step Law Transfer to Small-Scale Language Models? An Empirical Recalibration Below 59M Parameters</a></td><td>22</td><td>0</td><td>LLM Pretraining</td><td>Step Law를 소형 언어모델 영역까지 재검증한 실증 연구임. 특정 스케일 구간 재보정이라 novelty가 제한적임.</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2609.27760'>Backdoors Leave Structural Traces: FedMAST for Backdoor Detection and Containment in Federated Learning</a></td><td>22</td><td>0</td><td>Federated Learning/Security</td><td>federated learning 백도어 공격의 구조적 흔적을 탐지하는 FedMAST 방어법임. 도메인이 FL 보안이라 robotics와 무관함.</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2609.27819'>When Adaptation Hurts: Split Sensitivity and Person-Level Negative Transfer in Federated Wearable Onboarding</a></td><td>22</td><td>0</td><td>Federated Learning/Wearable</td><td>federated wearable 모델의 개인별 negative transfer를 감사한 벤치마크 연구임. 웨어러블 헬스 도메인이라 robotics와 무관함.</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2609.27954'>When Accuracy Gaps Fail to Certify: Auditing Cross-Domain Recalibration of LLM Judges</a></td><td>22</td><td>0</td><td>LLM Judge Calibration</td><td>LLM judge의 도메인 간 정확도 격차가 calibration 실패를 인증하지 못함을 보인 감사 연구임. robotics와 무관함.</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2609.27955'>CS-WCP: Robust Conformal Sets for LLM-Judge Traffic Shifts with Uncertain Group Proportions</a></td><td>22</td><td>0</td><td>Conformal Prediction</td><td>그룹 비율이 불확실할 때 LLM judge 예측집합의 커버리지를 보장하는 CS-WCP 제안임. 이론 기여지만 robotics와 무관함.</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2609.28006'>Shared Global KV with Layer-Specific Local History</a></td><td>22</td><td>0</td><td>Transformer Architecture</td><td>레이어 간 공유 KV에 레이어별 local history를 더하는 캐시 구조 연구임. LLM 추론 효율화 기여임.</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2609.28194'>Geospatial embeddings detect old-growth forests but buffered spatial validation narrows their advantage over Sentinel features</a></td><td>22</td><td>0</td><td>Remote Sensing</td><td>geospatial foundation model embedding으로 원시림을 탐지하고 공간 검증 방식의 영향을 분석함. 원격탐사 도메인이라 robotics와 무관함.</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2609.28263'>Resource-Adaptive Stochastic Gradient Descent for Online Linear Programming without Re-solving</a></td><td>22</td><td>0</td><td>Online Optimization</td><td>재계산 없이 온라인 선형계획을 SGD로 푸는 RASGD를 제안하고 regret 하한을 매칭함. LLM 추론 서빙 자원할당 도메인이라 robotics와 무관함.</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2609.28438'>Minimal-Norm Univariate Two-Layer ReLU Classification: Exact Solutions and Global Optimality with Skip Connections</a></td><td>22</td><td>0</td><td>Learning Theory</td><td>univariate two-layer ReLU 분류의 minimal-norm 해를 기하학적으로 완전히 특성화한 이론 논문임. robotics와 무관한 순수 이론 기여임.</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2609.28459'>Even Sharper Bounds for Transductive Learning and Its Applications</a></td><td>22</td><td>0</td><td>Learning Theory</td><td>transductive learning의 국소복잡도 bound를 log factor 없이 개선한 STLC를 제안함. 순수 통계학습이론 기여임.</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2609.27009'>LEGO: Synergizing Expert GraphRAG and Expert Chain-of-Thought for Legal Reasoning</a></td><td>22</td><td>0</td><td>NLP</td><td>법률 GraphRAG와 CoT를 결합한 응용 시스템 논문, 로봇학습과 무관함</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2609.27043'>EduBehaviors: Assertion-based Schemas for Auditable Coding of Educational Dialogues</a></td><td>22</td><td>0</td><td>NLP</td><td>교육대화 라벨링을 관찰가능 행동 기반으로 해석가능하게 만드는 프레임워크, 로봇학습과 무관한 응용 논문임</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2609.27205'>Phonemizing User-Generated Text: A Benchmark, Taxonomy, and Compositional Approach</a></td><td>22</td><td>0</td><td>NLP</td><td>사용자생성 텍스트의 발음추정을 위한 G2P 벤치마크, 로봇학습과 무관한 니치 음성 논문임</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2609.27359'>Automated Extraction of Records of Processing Activities (RoPA) Using Hybrid RAG and Locally Deployed Large Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>베트남 개인정보보호법 대응 처리활동기록을 hybrid RAG로 자동추출하는 응용 시스템, 로봇학습과 무관함</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2609.27376'>Cross-Lingual Legal QA for Vietnamese Labour Law: Retrieval, Translation, and Verifier-Guided Correction</a></td><td>22</td><td>0</td><td>NLP</td><td>베트남 노동법 교차언어 법률QA 시스템, 로봇학습과 무관한 응용 논문임</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2609.27669'>The Path Matters: Evaluating Small Language Models Beyond Answer Accuracy in KGQA</a></td><td>22</td><td>0</td><td>NLP</td><td>SLM의 KG 내비게이션 경로 충실도를 재는 평가 연구라 novelty가 제한적임</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2609.27690'>Consequential Behaviour and Representational Fairness in the Validation of Synthetic Research</a></td><td>22</td><td>0</td><td>NLP/CY</td><td>synthetic survey respondent 검증 프레임워크 제안인데 사회과학 방법론에 가까움</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2609.28060'>A Native-Reference Coordinate Geometry for L2 Pronunciation Deviation Using Self-Supervised Speech Models</a></td><td>22</td><td>0</td><td>Speech</td><td>self-supervised 음성 표현으로 L2 발음 편차를 재는 좌표 기하학 제안으로 응용 범위가 좁음</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2609.27087'>Policy-as-Skill: Governed LLM Decision Support with Evidence, Deterministic Control, and Audit</a></td><td>22</td><td>0</td><td>LLM Agent/Governance</td><td>정책 준수를 위한 governed LLM decision support 런타임으로 엔터프라이즈 거버넌스 엔지니어링에 가까움</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2609.27417'>Emergi-PersonaOS: A Persona Agent Operating System for Situational Adaptation and Controllable Evolution</a></td><td>22</td><td>0</td><td>Agent/HCI</td><td>persona agent의 생애주기를 관리하는 심리학 기반 아키텍처 제안이지만 정량적 검증이 약한 시스템 비전 논문임</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2609.28335'>An Open Pipeline and Dashboard for Systemic-Risk Evidence under the EU AI Act&#x27;s Code of Practice</a></td><td>22</td><td>0</td><td>AI Policy/Evaluation</td><td>EU AI Act 체계적 위험 평가를 위한 오픈 파이프라인·대시보드로 연구보다 도구 제공 성격이 강함</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2609.27986'>Relative Discharge Stage (RDS) Classification: A Practical Indicator of Battery Discharge Progress</a></td><td>21</td><td>1</td><td>Battery Management</td><td>배터리 잔여 방전 단계를 다섯 클래스로 분류하는 물리 정보 기반 프레임워크임. 배터리 관리 도메인이라 robotics 관련성이 낮음.</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2609.27287'>SR-Fraud: An Outcome-Supervised Reflective LLM Agent Framework for Non-Stationary Payment Fraud Detection</a></td><td>21</td><td>0</td><td>LLM Agent/Security</td><td>결제 사기 탐지용 reflective LLM agent 프레임워크임. 도메인이 금융 사기탐지라 robotics와 무관함.</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2609.27303'>Live Assistant: Learning Whether, When, and Whom to Assist in Real-World Live Social Streams</a></td><td>21</td><td>0</td><td>Multimodal/LG</td><td>라이브 스트리밍에서 언제 누구를 도울지 결정하는 정책 학습 논문임. 응용 도메인이 소셜 스트리밍이라 robotics와 무관함.</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2609.27362'>Anomaly-Free Self-Optimization via AUC Bounds</a></td><td>21</td><td>0</td><td>Anomaly Detection</td><td>AUC bound를 이상탐지 모델 설정의 미분가능 목적함수로 쓰는 방법임. 오디오 이상탐지 도메인이라 robotics와 무관함.</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2609.27633'>Pheno-GS: Phenoscape-scale Geodesic Sinkhorn</a></td><td>21</td><td>0</td><td>Optimal Transport/Biology</td><td>단일세포 데이터의 phenoscape 규모 optimal transport 계산 가속 방법임. 생물정보학 도메인이라 robotics와 무관함.</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2609.27457'>Beyond Balanced Accuracy: A Resolution and Parity-Controlled Benchmark for Vision-Language and Vision-Only Defect Assessment in UAV Power-Line Inspection</a></td><td>20</td><td>2</td><td>CV</td><td>UAV 전력선 결함 평가에서 VLM이 vision backbone보다 우월하다는 통념을 해상도·픽셀예산 통제로 반박한 벤치마크 감사 논문, 방법 제안 없이 평가 프로토콜 지적이 주 기여임</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2609.27681'>CasCVS-Net: A Staged Multi-Task Cascade for Critical View of Safety Assessment</a></td><td>20</td><td>2</td><td>CV</td><td>복강경 수술 CVS 평가를 detection-segmentation-classification 단계적 cascade로 결합한 방법, 수술 로봇과 인접하나 태스크 커플링 엔지니어링 수준임</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2609.27118'>From greenhouse climate to individual leaves: an organ-resolved model of lettuce growth</a></td><td>20</td><td>1</td><td>CV</td><td>잎 단위 광합성-생장 결합 시뮬레이션으로 상추 생장 디지털 트윈 구축, 농업 도메인 특화라 robotics 연관성 낮음</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2609.27142'>MINER: Multi-crop INference-time Enhancement for Rare-Object Retrieval with Frozen Dual Encoders</a></td><td>20</td><td>1</td><td>Multimodal</td><td>frozen dual encoder에 지역 임베딩 뱅크를 더해 rare object retrieval 개선, training-free inference trick 수준으로 robotics 응용 제시 없음</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2609.27533'>ICM: Intra-class Mixing for Domain Adaptation in Adverse Weather</a></td><td>20</td><td>1</td><td>CV</td><td>동일 이미지·클래스 내 mixing으로 악천후 도메인 적응 일관성을 강화한 방법, Cityscapes to ACDC에서 SOTA 갱신했으나 mixing 방식의 변형 수준임</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2609.28235'>Diff-RF: Mutually Reinforced Image Registration and Fusion via Degradation-Aware Learning</a></td><td>20</td><td>1</td><td>CV</td><td>저하된 조건에서 registration과 fusion을 상호보강하는 diffusion 프레임워크, 이미지 처리 응용이고 robot task 연결은 없음</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2609.27770'>Improving LLM-based Autonomous Web Agents with Filtering</a></td><td>20</td><td>1</td><td>Web Agent</td><td>2023년 수행된 구작업으로 HTML 필터링 retriever 추가하는 수준의 incremental engineering임</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2609.26927'>Building Socio-Affective Artificial Intelligence for Interactive Multi-Agent Simulations</a></td><td>20</td><td>1</td><td>Multi-Agent/HCI</td><td>사회정서적 multi-agent 시뮬레이션 아키텍처 제안이지만 정량 검증이 약한 시스템 비전 논문임</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2609.26809'>AgroBench: A Reproducible Multimodal Benchmark for Weakly Supervised Crop Yield Learning from County Statistics and Pixel Observations</a></td><td>20</td><td>0</td><td>CV</td><td>county 단위 라벨을 픽셀 단위 약지도로 바꾸는 벤치마크 구축 논문임, 방법 자체 novelty는 낮고 robotics 무관함</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2609.27217'>Learning Spectral Allocation: A Fractional Diffusion Framework for Adaptive Volumetric Segmentation</a></td><td>20</td><td>0</td><td>CV</td><td>fractional heat equation 기반 spectral mixing 강도를 학습시키는 3D 의료 분할 방법, 아이디어는 깔끔하나 도메인이 의료 영상에 국한됨</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2609.27327'>Can Vision-Language Models Analyze Human-Centered Video? Mapping Model Capabilities and Human-AI Collaborative Workflows</a></td><td>20</td><td>0</td><td>Video</td><td>CHI 논문 코딩을 통해 인간중심 영상분석 taxonomy를 만들고 VLM-사람 협업 워크플로를 비교한 HCI 연구, robotics와 거리 있음</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2609.27611'>A generalizable structural brain MRI foundation model built through dual-priority federated pretraining</a></td><td>20</td><td>0</td><td>CV</td><td>42개 기관 연합학습으로 구축한 뇌 MRI foundation model, federated pretraining 전략은 흥미로우나 robotics 무관함</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2609.27682'>Gender Bias in Vision-Language In-Context Learning</a></td><td>20</td><td>0</td><td>Multimodal</td><td>in-context learning demo의 성별이 LVLM 편향을 방향성 있게 이동시킨다는 실증 분석, robotics 무관하고 완화책도 간단한 데이터 교체 수준임</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2609.27958'>ScoutNeRV: Rapid Encoding of Grid-Based Video INRs via ScoutNet</a></td><td>20</td><td>0</td><td>Video</td><td>content-adaptive expert 초기화로 grid 기반 video INR 인코딩 속도를 9배 높인 방법, 압축 효율 개선 위주라 robotics 무관함</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2609.28192'>From Change Captions to Change Detection: Semantic-Appearance Agreement Framework for Remote Sensing Change Detection</a></td><td>20</td><td>0</td><td>CV</td><td>변화 캡션을 유일한 supervision으로 써서 픽셀 라벨 없이 변화탐지를 학습하는 프레임워크, 원격탐사 약지도학습 응용이고 robotics 무관함</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2609.28437'>MultiVENT-Raw: A Benchmark for Retrieval and Reasoning over Raw Videos</a></td><td>20</td><td>0</td><td>Video</td><td>편집 안 된 raw 비디오에 대한 대규모 다국어 검색·요약 벤치마크, 정보검색 연구이고 robotics 무관함</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2609.26853'>COPE: Continual Personalization of LLMs under Sparse User Feedback via User Embeddings and Self-Evaluation</a></td><td>20</td><td>0</td><td>LG</td><td>sparse feedback 하에서 유저 임베딩과 self-evaluation으로 LLM을 지속 개인화하는 방법, robotics 무관함</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2609.27201'>A Systematic Benchmark of Explainable Methods for Temporal Attribution in Sequential Recommendation Systems</a></td><td>20</td><td>0</td><td>LG</td><td>순차 추천시스템 설명가능성 방법 벤치마크임. 도메인이 추천시스템이라 우선주제와 무관함.</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2609.27825'>CAST: Context- and Anomaly Structure-Conditioned Time Series Anomaly Generation</a></td><td>20</td><td>0</td><td>Time Series Generation</td><td>context와 anomaly structure에 조건화한 시계열 이상치 생성 프레임워크임. 데이터 증강 목적의 응용 기여임.</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2609.28105'>Fed-ReMasker: Federated Tabular Imputation under Feature-Level Missingness</a></td><td>20</td><td>0</td><td>Federated Learning/Healthcare</td><td>feature 단위 결측이 있는 다기관 데이터의 federated imputation 방법임. 임상 데이터 도메인이라 robotics와 무관함.</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2609.28199'>Transferable Evidence Reconstruction for Longitudinal Glucose Representations</a></td><td>20</td><td>0</td><td>Healthcare Time Series</td><td>연속혈당 모니터링 데이터의 evidence 기반 자기지도 표현학습 TER를 제안함. 헬스케어 도메인이라 robotics와 무관함.</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2609.28208'>Support-Compiled Feature Folding: More Evidence at Lower Memory Across Tabular Foundation Models</a></td><td>20</td><td>0</td><td>Tabular Foundation Models</td><td>tabular foundation model의 feature 상호작용 비용을 선형으로 줄이는 SCFF 제안임. 정형데이터 추론 효율화 기여임.</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2609.26942'>Recognized but Not Produced: A Generation Benchmark for Culturally Specific Kinship Terms</a></td><td>20</td><td>0</td><td>NLP</td><td>친족어 생성 벤치마크로 니치한 다국어 평가 논문, 로봇학습과 무관함</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2609.26945'>Classifying Interpretive Canons at the Sentence Level: A Benchmark from the German Federal Constitutional Court</a></td><td>20</td><td>0</td><td>NLP</td><td>독일 헌법재판소 판결문의 해석기준을 문장단위로 분류하는 법률 NLP 벤치마크, 로봇학습과 무관함</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2609.27558'>ThaiTrees: Thai Syntactic Dependency Trees Across Domains</a></td><td>20</td><td>0</td><td>NLP</td><td>태국어 대규모 의존구문 코퍼스 구축 논문, 로봇학습과 무관함</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2609.27650'>Brain-to-Language Decoding: Tasks, Signals, Methods, Evaluation, Practical Use and Beyond</a></td><td>20</td><td>0</td><td>NLP</td><td>brain-to-language decoding 서베이 논문이라 새 방법론 없고 로봇과도 무관함</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2609.27814'>LabourCrew: A Multi-Agent RAG Framework for Trustworthy Adversarial Deliberation and Statutory Reasoning over Labour Law</a></td><td>20</td><td>0</td><td>NLP</td><td>노동법 QA를 위한 multi-agent RAG 프레임워크로 특정 도메인 엔지니어링 성격이 강함</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2609.28430'>Cross-Scale Transfer Learning for Depression Severity Prediction: From PHQ-8 to HAMD-17 Across Languages and Clinical Paradigms</a></td><td>20</td><td>0</td><td>NLP/Health</td><td>PHQ-8에서 HAMD-17로 언어·척도를 넘나드는 LoRA 전이 학습으로 단일 사이트 탐색 연구에 그침</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2609.27037'>Training Intelligent Voice Assistant Wakeup with Controllable Synthetic Conversations</a></td><td>20</td><td>0</td><td>Speech</td><td>wake word 이후 contextual trigger를 구분하는 음성 비서 학습용 합성 대화 데이터셋 구축 연구임</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2609.27284'>Hunyuan-A13B Technical Report</a></td><td>20</td><td>0</td><td>LLM</td><td>80B MoE 오픈소스 LLM의 기술 리포트로 새로운 연구 문제 제기 없이 스케일·성능 보고에 그침</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2609.27446'>Quantum Reinforcement Learning for Cost and Delay Tradeoffs in Quantum Cloud Orchestration</a></td><td>19</td><td>0</td><td>Quantum RL</td><td>양자 클라우드 스케줄링에 quantum RL을 적용한 논문임. 도메인이 클라우드 오케스트레이션이라 robotics와 무관함.</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2609.27594'>Efficient Linear Bandits via Cluster-Aware Sketching</a></td><td>19</td><td>0</td><td>Bandits/LG</td><td>고차원 선형 밴딧의 계산 효율화를 위한 clustering 기반 sketching 방법임. 이론 중심의 효율화 기여임.</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2609.27637'>Learning Local Heterogeneity and Cross-Region Context for Large-Scale Traffic Forecasting</a></td><td>19</td><td>0</td><td>Time Series/LG</td><td>대규모 교통 흐름 예측을 위한 지역-교차지역 spatial temporal network임. 응용 도메인 특화 기여로 novelty가 제한적임.</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2609.27735'>NS-ATTENTION: Newton-Schulz Transformations of Attention Outputs in Vision Transformers</a></td><td>19</td><td>0</td><td>Vision Transformer</td><td>Newton-Schulz 변환을 attention 출력에 적용한 parameter-free 기법임. CIFAR급 실험의 소폭 개선에 그침.</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2609.27317'>Breaking Weather-Content Coupling: Type-Severity Guided Progressive Disentanglement for All-in-One Infrared Restoration</a></td><td>18</td><td>1</td><td>CV</td><td>적외선 영상에서 날씨 종류와 지역별 심각도를 분리해 복원하는 all-in-one 프레임워크, 자율주행 언급되나 모듈 조합형 엔지니어링 수준임</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2609.27413'>S2A:Semantic-to-Spatial Alignment for Alignment-Free RGB-T Salient Object Detection</a></td><td>18</td><td>1</td><td>CV</td><td>정렬 안 된 RGB-T 쌍에서 semantic-to-spatial 순서로 saliency 탐지하는 프레임워크, 모듈 조합형 성능 개선 논문임</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2609.28230'>A Unified Framework and Dataset for Oriented Object Visual Grounding in Remote Sensing</a></td><td>18</td><td>1</td><td>CV</td><td>원격탐사에서 방향성 bbox 기반 visual grounding을 위한 판별형+생성형 모델군과 데이터셋, 도메인 특화 엔지니어링 성격이 강함</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2609.28239'>ODPure: Backdoor Purification for Object Detection via Ensemble Corruption Consensus</a></td><td>18</td><td>1</td><td>CV</td><td>corruption-reconstruction-selection으로 object detection 백도어를 입력단에서 정화하는 방어법, 자율주행 언급되나 보안 응용에 가까움</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2609.27110'>Feed the Panel Dimensions, Not Verdicts: Rubric-Decomposed Fusion of Vision-Language Aesthetic Judges</a></td><td>18</td><td>0</td><td>Multimodal</td><td>VLM 미학 평가 패널을 rubric 차원별로 분해해 fusion하는 실험 연구, robotics와 무관하고 기여가 응용 수준임</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2609.27442'>SatUnreal: A High-Precision Synthetic Dataset for Satellite Stereo Matching via Unreal Engine</a></td><td>18</td><td>0</td><td>3D Vision</td><td>위성 스테레오 매칭용 Unreal Engine 합성 데이터셋, sim-to-real 전이 결과는 있으나 데이터셋 논문 성격이 강함</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2609.27461'>Invisible in Space, Visible in Time: Motion Vision CAPTCHA against GUI Agents</a></td><td>18</td><td>0</td><td>CV</td><td>GUI agent 대상 motion 기반 CAPTCHA, robotics와 무관하고 응용 벤치마크 논문임</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2609.27493'>Information Capacity of Generative Video Compression: Quantifying the Rate-Compute Exchange at Identical Quality</a></td><td>18</td><td>0</td><td>Video</td><td>생성적 비디오 압축의 rate-compute trade-off를 information capacity로 정량화한 분석 논문, robotics 무관함</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2609.27620'>InGuard: Towards Generalized Inner Guardrail for Safe Text-to-Image Generation</a></td><td>18</td><td>0</td><td>CV</td><td>T2I 생성 파이프라인 내부 표현에서 동작하는 안전 가드레일, 응용 시스템 논문이고 robotics 무관함</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2609.28283'>Benchmarking Hyperspectral Foundation Models for Hyperspectral Unmixing</a></td><td>18</td><td>0</td><td>CV</td><td>hyperspectral foundation model을 unmixing 태스크에 처음 벤치마킹하고 upsampling으로 해상도 문제를 완화한 연구, 원격탐사 도메인 특화이고 robotics 무관함</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2609.28342'>Zero-Shot Object Removal via Attention Masking, Latent Anchoring, and Refinement</a></td><td>18</td><td>0</td><td>CV</td><td>frozen Stable Diffusion으로 attention masking·latent anchoring을 결합한 zero-shot 물체 제거 파이프라인, 이미지 편집 응용이고 robotics 무관함</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2609.26855'>QUARTET: Quad-branch cross-Attention and Random-walk Traces for Enhancing Transformers on Relational Graphs</a></td><td>18</td><td>0</td><td>LG</td><td>관계형 그래프 transformer에 causal random walk 샘플러와 4분기 cross-attention을 더한 방법, RelBench 성능 개선이나 robotics 무관함</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2609.27018'>GeoRVQ: Decoder-aware geometry for residual-token prediction in physiological signals</a></td><td>18</td><td>0</td><td>LG</td><td>생리 파형 residual vector quantization에서 decoder 반응을 반영한 geometry-aware soft target을 도입한 방법, 의료 신호 응용이고 robotics 무관함</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2609.27658'>Private Decentralized Optimization with Noise Reduction and Bias Correction</a></td><td>18</td><td>0</td><td>Distributed Optimization</td><td>differential privacy 하 decentralized 최적화의 노이즈·bias 보정 방법임. 이론적 기여지만 robotics와 무관함.</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2609.27764'>Learning to Detect Symbolic Failure: Machine Learning and the Limits of Black-Scholes</a></td><td>18</td><td>0</td><td>Finance/LG</td><td>옵션가격의 Black-Scholes 이탈을 ML로 탐지하는 표현학습 비교 연구임. 금융 도메인이라 robotics와 무관함.</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2609.27936'>Quality over Quantity: Semi-Supervised Detection of Illicit Bitcoin Flows via Feature Engineering</a></td><td>18</td><td>0</td><td>Finance/Security</td><td>비트코인 불법거래 탐지에서 feature engineering이 데이터량보다 중요함을 보인 준지도학습 연구임. robotics와 무관함.</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2609.28248'>hyperbolix: Hyperbolic Deep Learning in JAX</a></td><td>18</td><td>0</td><td>Library/Tool</td><td>JAX 기반 hyperbolic deep learning 오픈소스 라이브러리 소개임. 도구 논문으로 과학적 novelty가 낮음.</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2609.27086'>NADI 2026: The Second Multidialectal Arabic Speech Processing Shared Task</a></td><td>18</td><td>0</td><td>NLP</td><td>다방언 아랍어 음성처리 shared task 개요 논문, 로봇학습과 무관함</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2609.27387'>AraGenre 2026: A Hierarchical Definition-Guided Arabic Genre Classification Shared Task</a></td><td>18</td><td>0</td><td>NLP</td><td>아랍어 장르분류 shared task 개요 논문, 로봇학습과 무관함</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2609.27678'>Same Scores, Different Decisions: Evaluating JEV and Language Models for Legal Document Understanding</a></td><td>18</td><td>0</td><td>NLP</td><td>법률 문서 이해에서 JEV와 LM 비교하는 응용 평가라 일반화 가치가 낮음</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2609.27980'>Six Layers Less: Encoder Pruning for Whisper with Label-Free Recovery</a></td><td>18</td><td>0</td><td>Speech/Efficient</td><td>Whisper 인코더를 6개 층 pruning하는 label-free 압축 기법으로 단순 efficiency 기여임</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2609.28004'>Controlled Attribute-Specific Summarization of Interrogative Dialogues</a></td><td>18</td><td>0</td><td>NLP</td><td>심문 대화 요약을 위한 CoT 프롬프팅 프레임워크로 특정 포렌식 응용에 그침</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2609.28026'>Evaluating Feedback Focus and Pedagogical Adaptivity in LLM-Generated Feedback on Student Writing</a></td><td>18</td><td>0</td><td>NLP/Education</td><td>LLM 피드백의 교육적 초점과 적응성을 벤치마크로 측정한 응용 평가 연구임</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2609.28471'>Contrastive Learning for Authorship Verification</a></td><td>18</td><td>0</td><td>NLP</td><td>저자 식별 과제에서 contrastive learning 설정을 튜닝해 정확도를 높인 응용 벤치마크 연구임</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2609.26952'>Escaping Python Dependency Hell: A Hybrid Replay-and-Repair Pipeline for Python Dependency Resolution</a></td><td>18</td><td>0</td><td>Software Engineering/Agent</td><td>Python 의존성 충돌 해결을 결정론적 replay 우선으로 처리하는 파이프라인으로 LLM 기여는 5건에 불과한 엔지니어링 성격임</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2609.27197'>Enhancing Small Language Models for Power Outage Report Generation via Minimum Risk Training</a></td><td>18</td><td>0</td><td>NLP/Applied</td><td>정전 보고서를 표준 XML로 변환하는 SLM에 minimum risk training을 적용한 특정 도메인 응용 연구임</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2609.27749'>Evaluation of pre-trained models for pedagogical assessment of novel AI-assisted educational questions</a></td><td>18</td><td>0</td><td>NLP/Education</td><td>AI가 생성한 교육 문항의 Bloom 수준 분류기를 OOD에서 평가한 응용 연구로 novelty가 낮음</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2609.27564'>TNLearn: An Open Source Python Package for Task-based Neurons</a></td><td>17</td><td>0</td><td>LG Tool</td><td>task-based neuron 구축용 오픈소스 파이썬 패키지 소개임. 도구 논문으로 새로운 과학적 기여가 약함.</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2609.27536'>Behaviora - A Conceptual Architecture for External and Internal Behavior of Robots and Agents</a></td><td>15</td><td>3</td><td>Robotics</td><td>행동 표현을 위한 개념적 아키텍처 제안인데 toy 예시 하나뿐이라 실험적 근거가 거의 없음</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2609.28262'>RAMP: Robust Adaptive Mixed-Precision Quantization for Edge CPU Vision Models</a></td><td>15</td><td>1</td><td>LG</td><td>edge CPU에서 레이어별 양자화 민감도 지표 13종을 비교하고 클러스터링으로 정책을 정하는 실증 연구, 경량화 방향이라 우선 평가 대상이 아니고 새 방법론이라기보다 벤치마킹임</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2609.26920'>Cross-Modal Contrastive Learning from Histopathology and CT for Automated Renal Cell Carcinoma Grading</a></td><td>15</td><td>0</td><td>CV</td><td>병리-CT cross-modal contrastive 학습으로 신장암 등급 예측, AUC 0.601로 baseline 대비 개선 폭 작고 robotics 무관함</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2609.27011'>HYDRO: Towards Non-Reversible Face De-Identification Using a High-Fidelity Hybrid Diffusion and Target-Oriented Approach</a></td><td>15</td><td>0</td><td>CV</td><td>diffusion 기반 얼굴 비식별화로 재구성 공격 방어, 응용 엔지니어링 수준이고 robotics 무관함</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2609.27015'>Anatomy-Aware Synthesis of Post-Contrast Breast MRI from Pre-Contrast Images</a></td><td>15</td><td>0</td><td>CV</td><td>pre-contrast에서 post-contrast 유방 MRI 합성, 해부학 인지 supervision 추가한 incremental 기여임</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2609.27022'>Adversarial Attacks and Identity Leakage in De-Identification Systems: An Empirical Study</a></td><td>15</td><td>0</td><td>CV</td><td>비식별화 시스템 대상 adversarial attack 전이성 실증 연구, 새로운 방법론보다 실험적 관찰 위주임</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2609.27115'>Damnatio Memoriae: Adversarially and Selectively Forgetting Identities in the Embedding Space of Face Recognition Models</a></td><td>15</td><td>0</td><td>CV</td><td>얼굴인식 임베딩 공간에서 특정 신원을 선택적으로 잊게 하는 loss 3종 제안, 문제는 흥미롭지만 robotics 무관함</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2609.27149'>Temporally Ordered Region-Token Mamba with Logit-Space Diffusion for Remote Sensing Change Detection</a></td><td>15</td><td>0</td><td>CV</td><td>Mamba+diffusion으로 원격탐사 변화탐지, 벤치마크 수치 개선 위주 incremental 엔지니어링임</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2609.27194'>Diverse by Design: Architectural Constraints for Prototype-Based Interpretability</a></td><td>15</td><td>0</td><td>CV</td><td>prototype 다양성을 attention 구조 제약으로 확보하는 해석가능성 연구, CUB-200 단일 벤치마크의 작은 개선임</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2609.27208'>Benchmarking Active Spot Selection for Cost-Efficient Spatial Transcriptomics</a></td><td>15</td><td>0</td><td>LG</td><td>공간전사체학에서 active learning이 random sampling 대비 일관되게 낫지 않다는 부정적 벤치마크 결과, robotics 무관함</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2609.27238'>Strip Convolution and Direction-Aware Exclusion Loss for Oriented Ship Detection</a></td><td>15</td><td>0</td><td>CV</td><td>strip convolution과 방향인지 loss로 선박 탐지 성능 개선, 파라미터 효율 강조하는 incremental detection 연구임</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2609.27274'>High Dynamic Range Video Reconstruction from Single-Exposure Raw Sequences</a></td><td>15</td><td>0</td><td>CV</td><td>단일 노출 raw 영상에서 HDR 비디오 복원하는 방법, Bayer 채널 분리 처리라는 엔지니어링 기여이고 robotics 무관함</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2609.27356'>Beyond Mean Foils: Auditing Worst-Foil Specificity in Frozen CLIP Region Explanations</a></td><td>15</td><td>0</td><td>CV</td><td>frozen CLIP region 설명이 최강 경쟁 클래스 대비 실패하는 비율을 감사하는 진단 연구, 방법 제안보다 현상 보고 위주임</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2609.27523'>M3D-Net: Hierarchical Coordination of Spatial Context, Feature Reuse, and Differential Attention for Mammography Classification</a></td><td>15</td><td>0</td><td>CV</td><td>유방 촬영술용 계층적 attention 조합 인코더, 의료 영상 분류 성능 개선 위주의 incremental 연구임</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2609.27696'>SynSeq: End-to-End SYNTAX Score Prediction from Coronary Angiography Videos</a></td><td>15</td><td>0</td><td>CV</td><td>관상동맥 조영 영상에서 SYNTAX score를 직접 회귀하는 방법, 의료 응용이고 robotics 무관함</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2609.27710'>FFM-CP: Cross-Backbone Fusion of Vision-Language Foundation Models for Few-Shot Computational Pathology</a></td><td>15</td><td>0</td><td>CV</td><td>few-shot 설정에서 병리 VLM 여러 개를 Procrustes 정렬 후 융합하는 프레임워크, 의료 도메인 특화 엔지니어링임</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2609.27793'>DualStabSleepNet: A Dual-Domain Diffusion Stabilization Network for Robust Sleep Staging</a></td><td>15</td><td>0</td><td>CV</td><td>이중 도메인 diffusion으로 노이즈를 안정화한 수면 단계 분류 네트워크, 의료 신호처리 응용이고 robotics 무관함</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2609.27848'>Geometry-anchored PET-aware multimodal pseudo-CT synthesis for whole-body attenuation correction: the BIC-MAC Challenge</a></td><td>15</td><td>0</td><td>CV</td><td>NAC-PET을 공간 기준으로 삼아 pseudo-CT를 합성하는 challenge 방법론 논문, 의료 응용이고 robotics 무관함</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2609.28077'>TEEP-RCNN: Texture-Enhanced Edge-aware Perception for Steel Surface Defect Detection via Improved Convolutional Block Attention in Faster R-CNN</a></td><td>15</td><td>0</td><td>CV</td><td>CBAM 개선과 TTA+WBF로 강판 표면 결함을 탐지하는 방법, 산업 검사 엔지니어링이고 robotics 무관함</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2609.28083'>ZoomDiff: A High-Fidelity Diffusion Model for Dual-Camera Smooth Zooming</a></td><td>15</td><td>0</td><td>CV</td><td>이중 카메라 줌 전환에서 diffusion 조건화로 이질감을 줄인 프레임 보간 방법, 모바일 카메라 응용이고 robotics 무관함</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2609.28110'>Field-of-View Extension in Dental Cone-Beam CT via Implicit Neural Representations and Diffusion Model-Based Refinement</a></td><td>15</td><td>0</td><td>CV</td><td>INR과 diffusion을 결합해 dental CBCT의 잘린 FOV를 확장하는 3단계 파이프라인, 의료 영상 응용이고 robotics 무관함</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2609.28154'>A comparative assessment of global building and settlement datasets across geographic and settlement contexts</a></td><td>15</td><td>0</td><td>CV</td><td>7개 글로벌 건물·정주지 데이터셋을 135개 지역에서 비교 평가한 벤치마크 연구, 새 방법 없이 비교 분석 위주임</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2609.28231'>Do Center Biases Propagate? Robustness of Pathology Foundation Models in Whole-Slide Image Classification</a></td><td>15</td><td>0</td><td>CV</td><td>병리 foundation model이 촬영 기관 정보를 암묵적으로 인코딩해 WSI 예측에 spurious shortcut을 만드는지 검증한 연구, 의료 진단 로버스트니스 분석이고 robotics 무관함</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2609.28286'>PBLH Estimation from Satellite Radiances via a Dual-Encoder Transformer</a></td><td>15</td><td>0</td><td>LG</td><td>위성 복사휘도로부터 대기경계층 고도를 추정하는 dual-encoder transformer, 기상 응용이고 robotics 무관함</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2609.28327'>LightMIS: Ultra-Lightweight Medical Image Segmentation Without a Stage-Wise Decoder</a></td><td>15</td><td>0</td><td>CV</td><td>decoder 없는 초경량 의료 영상 분할 네트워크, 경량화 방향이고 정확도는 기존 SOTA와 대등한 수준에 그침</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2609.28424'>The Skin-Restricted Reinhard Transform:Uniqueness under a Lightness-Preserving Constraint</a></td><td>15</td><td>0</td><td>CV</td><td>피부 리컬러링에서 밝기를 보존하는 diagonal affine map을 CIE Lab에서 유일하게 결정하는 색 변환 방법, 카탈로그 이미지 편집 응용이고 robotics 무관함</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2609.28434'>Predicting the Progression of Adolescent Idiopathic Scoliosis</a></td><td>15</td><td>0</td><td>CV</td><td>합성 데이터로 학습한 transformer로 청소년 척추측만증 진행을 예측, 의료 응용이고 robotics 무관함</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2609.28439'>HaRP: High Dynamic Range Photosequencing through Dual Reversed Shutter Scanning</a></td><td>15</td><td>0</td><td>CV</td><td>이중 역방향 rolling shutter 촬영으로 HDR을 복원하는 하드웨어-알고리즘 결합 방법, 모바일 촬영 응용이고 robotics 무관함</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2609.26822'>HARN: Hierarchical Associative Resonance Network for Event-Driven Multi-Timeframe Forecasting</a></td><td>15</td><td>0</td><td>LG</td><td>완결된 봉만 갱신하는 계층적 연상 공명 네트워크로 금융 다중시간대 예측, 금융 응용이고 robotics 무관함</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2609.26839'>LWCal: Loss-Weighted Calibration for Tabular Classifiers with Noisy Calibration Labels</a></td><td>15</td><td>0</td><td>LG</td><td>노이즈 있는 calibration 라벨에 대응하는 loss-weighted calibration 방법, tabular 응용이고 robotics 무관함</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2609.26848'>A Leakage-Aware Multimodal Evaluation Framework for Early Intraoperative Acute Kidney Injury Prediction</a></td><td>15</td><td>0</td><td>LG</td><td>수술 중 급성 신손상 조기 예측을 위한 파형+정형 데이터 앙상블, 의료 응용이고 robotics 무관함</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2609.26955'>When Post-Processing Fairness Constraints Help and When They Harm: Evidence from Eight Cross-Domain Evaluations</a></td><td>15</td><td>0</td><td>LG</td><td>post-processing fairness 개입이 8개 도메인에서 언제 돕고 언제 해치는지 감사한 연구, 공정성 응용이고 robotics 무관함</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2609.26959'>Transfer Learning with Conformalized Quantile Regression for Solar PV Forecasting Under Load-Shedding-Driven Data Scarcity</a></td><td>15</td><td>0</td><td>LG</td><td>부하차단으로 데이터가 희소한 지역의 태양광 예측에 전이학습과 conformal quantile regression을 결합, 에너지 예측 응용이고 robotics 무관함</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2609.26962'>CRISP: Scalable Importance-Stratified Coresets for Imbalanced Tabular Learning</a></td><td>15</td><td>0</td><td>LG</td><td>불균형 tabular 학습에서 중요도 계층화로 다수 클래스를 pruning하는 coreset 방법, 사기탐지 등 응용이고 robotics 무관함</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2609.27824'>&quot;AI Is Turning Too Human&quot;: How Teenagers Experience and Negotiate AI in Everyday Life</a></td><td>15</td><td>0</td><td>HCI</td><td>청소년의 AI 경험을 다루는 질적 담론 분석이라 ML 방법론 기여가 없음</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2609.27939'>From Sentiment Classification to Actionable and Responsible Feedback: A Scoping Review and Evidence Map of NLP in Student Evaluation of Teaching, 2015-2026</a></td><td>15</td><td>0</td><td>NLP/Education</td><td>SET(강의평가) NLP 연구 421편을 정리한 scoping review라 새로운 방법 기여가 없음</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2609.28007'>Evaluating Open-Weight LLMs for Turkish Domain Documents Under Retrieval and Hardware Constraints</a></td><td>15</td><td>0</td><td>NLP</td><td>터키어 문서 QA에서 저사양 GPU 제약 하 모델 비교하는 응용 평가 연구임</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2609.28245'>Beyond Poetry: Can Large Language Models Generate Classical Arabic Maqamat?</a></td><td>15</td><td>0</td><td>NLP/Culture</td><td>고전 아랍 산문 장르 maqama 생성 능력을 평가하는 문학적 응용 연구로 일반화 가치가 낮음</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2609.27903'>A Resilience Recovery Method for Complex Traffic Network Security Based on Trend Forecasting</a></td><td>15</td><td>0</td><td>Applied/Network Security</td><td>SIRD 모델과 LSTM으로 교통망 복원력을 예측하는 응용 연구로 ML 방법론 기여가 작음</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2609.26923'>A 3D Pose-Based Ensemble Framework for Cricket Shot Classification and Automated Biomechanical Analysis</a></td><td>12</td><td>1</td><td>CV</td><td>YOLO+3D pose로 크리켓 샷 분류하는 응용 논문, 방법론 신규성 없고 robotics와도 거리 있음</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2609.27143'>A Systematic Evaluation of Infrastructure-Based Radar System for Highway Traffic Monitoring</a></td><td>12</td><td>1</td><td>CV</td><td>고속도로 인프라 레이더 성능을 드론 대비 평가한 실증 연구, 새 방법론 없이 시스템 평가임</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2609.27131'>Super-Resolution of Solar Magnetograms via Adaptive Stratified Ensemble Learning with Uncertainty Estimation</a></td><td>12</td><td>0</td><td>CV</td><td>태양 자기도 초해상도를 위한 복잡도별 앙상블 라우팅, 도메인 특화 엔지니어링이고 robotics 무관함</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2609.27815'>Evaluating ADC-only deep learning pipelines for breast cancer detection and segmentation using standalone diffusion-weighted MRI</a></td><td>12</td><td>0</td><td>CV</td><td>ADC 단독 영상으로 유방암 탐지·분할하는 최초 종합 평가, 의료 벤치마킹 논문이고 robotics 무관함</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2609.27904'>Spatiality-Frequency Domain Video Forgery Detection System Based on ResNet-LSTM-CBAM and DCT Hybrid Network</a></td><td>12</td><td>0</td><td>CV</td><td>ResNet-LSTM-CBAM과 DCT를 결합한 영상 위조 탐지 모델, 모듈 조합형 성능 개선이고 robotics 무관함</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2609.28183'>From ECG Signals to Representative-Morphology Heatmaps for Biometric Recognition</a></td><td>12</td><td>0</td><td>CV</td><td>ECG를 heatmap 이미지로 렌더링해 생체인식 성능을 높인 표현 방식, 응용 도메인이 좁고 robotics 무관함</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2609.26981'>Lessons learned from deploying imaging AI with the open PACS-AI platform</a></td><td>10</td><td>0</td><td>CV</td><td>PACS-AI 플랫폼 배포 경험 보고서, 기술 기여 없이 운영 사례 서술 위주임</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2609.28352'>Digital diglossia: Arabic between X and Facebook</a></td><td>10</td><td>0</td><td>Linguistics</td><td>X와 Facebook에서 아랍어 diglossia 분포를 통계 분석한 사회언어학 연구로 ML 기여가 없음</td></tr>
</tbody></table>

</details>
