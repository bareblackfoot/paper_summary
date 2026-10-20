# 오늘의 arXiv Top 15 — 2026-09-22 (화)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**
> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)

**신규 논문 수: 전체 931편 → 중복 제거 후 931편 (이번 평가 대상 931편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 221 |
| cs.LG | 241 |
| cs.RO | 182 |
| cs.CL | 176 |
| cs.AI | 111 |

*1차 스크리닝: 전체 931편을 제목/초록 기반으로 채점(Claude (scheduled agent)) → 상위 15편은 arXiv 원문을 내려받아 정밀 리뷰(Claude (scheduled agent)) 후 최종 점수 산정.*

---

## Top 15

### 1. [79점] Robot World Models Are Not Invariant to How the Actions Are Written

- **분야**: World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.23252](https://arxiv.org/abs/2609.23252) ([PDF](https://arxiv.org/pdf/2609.23252))
- **저자**: Ahmed Karim, Leon Chlon
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 65점

> 💡 action-conditioned world model을 absolute joint target으로 학습시키고 동일한 궤적을 relative encoding으로 바꿔 주면 retrieval이 최대 13.4배 나빠지고 goal-conditioned action selection이 53%에서 15%로 무너짐을 보임. 두 encoding 사이를 서로 복원하는 회귀의 R²=0.996으로 정보량 자체는 동일함을 확인해 이것이 정보 손실이 아니라 notation 자체에 대한 취약성임을 밝히고, objective averaging과 disagreement penalty를 결합한 repair로 worst-case agreement를 0.78에서 0.995까지 회복시킴.

**Core innovation & methodology**

- action-conditioned world model이 absolute/relative action parameterization이라는 순수 표기법 차이에 얼마나 취약한지를 처음 정량적으로 측정한 문제 설정임.
- 두 encoding이 서로 완전히 복원 가능한지(mutual reconstructibility)와 predictive parity를 함께 검사하는 admissibility test(Definition 1)를 제안해 진짜 symmetry와 정보를 잃는 lossy transformation을 구분함.
- Theorem 2로 orbit-constant predictor의 risk가 최악의 view risk보다 크거나 같음을 증명하고, 이 parity gap을 invariance를 강제할 때 치르는 비용의 하한으로 제시함.
- repair는 두 encoding에 대해 objective를 평균내는 joint training과, direction 값 예측에 맞춘 disagreement penalty(consistency loss)로 구성됨. 확률 벡터에서 성립하는 output averaging의 Jensen 부등식이 unit vector 예측에서는 깨짐을 반례로 증명함(Proposition 3).

**Novelty vs. prior works**

- invariance 연구는 거의 다 pixel 쪽(crop, jitter, camera pose)만 다루고 action channel은 아무도 감사하지 않았다는 지적이 이 논문의 진짜 기여임.
- IRM·causal invariance 계열은 여러 environment의 변동에서 invariance를 추론하지만, 이 논문은 단일 environment에서 주어진 transformation이 symmetry인지 아닌지를 판정하는 test를 제공함. 저자도 두 접근이 상호보완적이라고 명시함.
- 저자가 제안했던 4개 candidate axis 중 3개(photometric jitter, camera choice, action-window summary)는 test에서 스스로 기각당함. 남은 축(absolute/relative action)만 성립해서 novelty의 범위는 이 특정 축 하나로 좁음.

**Benchmark results**

- ALOHA mobile cabinet은 retrieval rank가 canonical 6.19에서 held-out 61.5로 9.9배, ALOHA static coffee는 3.97에서 53.3으로 13.4배 collapse함. PushT는 66.2에서 169.8로 2.6배지만 cross-encoding cosine이 mean 0.067, worst -0.377로 두 encoding 예측이 거의 직교함.
- goal-conditioned action selection(32개 후보 top-1, chance 3.1%)은 teacher가 자기 encoding에서 53.1%, 반대 encoding에서는 15.4%로 떨어짐.
- objective averaging만으로(λ=0) ALOHA cabinet의 held-out rank가 61.5→5.98, action selection이 15.4%→40.1%로 회복됨. consistency penalty(λ=16)는 accuracy 개선은 거의 없지만(41.1%) worst-case agreement를 0.779→0.995로 끌어올림.
- PushT에서는 averaging만으로 축이 완전히 안 고쳐짐. worst-case cos는 0.067→0.971로 좋아지지만 canonical accuracy는 66.2→79.2로 오히려 나빠져 repair가 공짜가 아님을 보여줌.
- training set 크기 n을 150→1200으로 늘리면 collapse ratio는 2.5배→9.9배로 커지는데 cross-encoding cosine은 0.357~0.374로 거의 그대로임. scale-up으로는 이 결함이 해결되지 않고 오히려 격차만 벌어짐.

**Top-tier conference 적합성 — 66/100 · 추천 venue: CoRL**

action parameterization이라는 로봇러닝 실무에서 흔히 겪는 선택이 world model을 이 정도로 망가뜨린다는 지적은 실용적 파급력이 큼. Theorem 2의 risk 하한 증명, MDL(minimum description length) 기준으로 invariance 강제가 유리한 조건을 정리한 분석, Proposition 3 반례로 주장을 이론적으로 탄탄히 받침. 다만 검증이 frozen encoder 위 작은 MLP의 retrieval·offline action selection에 그치고 real robot이나 closed-loop control 실험이 없어서, CoRL 심사에서 실제 정책 학습이나 제어 성능으로 이어지는지에 대한 근거 부족이 지적될 위험이 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- 누리랩이 쓰는 world model이 절대/상대 action encoding을 섞어 쓰고 있다면 이 논문의 admissibility test(Definition 1)를 그대로 돌려서 우리 predictor가 같은 결함을 갖는지 먼저 확인할 수 있음.
- failure detection/recovery 연구에서 "predictor가 다른 질문에 답하고 있다"는 프레이밍은 action representation 불일치를 failure mode 원인 하나로 잡는 진단 틀로 쓸 수 있음.
- consistency-penalty repair(Eq.2)는 VLA policy가 joint/delta/end-effector 등 여러 action space를 오가며 학습될 때 world model 쪽을 미리 단단하게 만드는 실무적 레시피로 바로 가져다 쓸 수 있음.

---

### 2. [72점] Grounded Action Model: 3D Grounding as a Foundation for Robotics

- **분야**: VLA / Manipulation / 3D Vision · **robotics relevance**: 9/10
- **arXiv**: [2609.23863](https://arxiv.org/abs/2609.23863) ([PDF](https://arxiv.org/pdf/2609.23863))
- **저자**: Gehao Zhang, Weikai Huang, Shailesh Shailesh, Yiyan Peng, Jiafei Duan, Ranjay Krishna
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 65점

> 💡 언어·point·box 프롬프트를 frozen 3D grounding 모델에 넣어 타겟 물체의 이미지·3D detection 토큰을 만들고 로봇 state와 함께 MM-DiT flow matching action head로 조작 action을 예측하는 Grounded Action Model(GAM)을 제안함. RoboTwin 2.0·LIBERO-PRO·실로봇 2종에서 scene randomization·타겟 재배치·신규 타겟 지정 상황의 일반화 성능이 VLA·world-action model baseline보다 크게 높으나, 물체 외형 변화 조건에서는 오히려 낮음.

**Core innovation & methodology**

- VLM·video generation backbone 대신 promptable 3D grounding 모델(WildDet3D)을 frozen backbone으로 써서 '물체 위치 파악'은 backbone에, '조작 방법 학습'은 action head에 분리함.
- 언어·2D point·2D box 세 프롬프트를 모두 grounding backbone을 거쳐 2D/3D box·depth 기반 object-centric 표현 하나로 통일함.
- 이미지 토큰은 타겟 물체·로봇팔 영역만 남기고 마스킹하고, detection 토큰은 물체별 point cloud를 octant pooling해 shape feature와 center/extent/rotation으로 구성함.
- image/detection/state-history/action 4-stream MM-DiT로 joint attention 후 flow matching으로 action chunk를 예측하며, 언어는 토큰 추가 없이 adaptive layer norm으로만 주입함.
- Franka 실로봇 실험에서는 VLM planner(Molmo2)가 point로 타겟을 지정하고 GAM이 그 point를 받아 저수준 policy로 동작하는 조합도 평가함.

**Novelty vs. prior works**

- VLA(π0.5 등)·world-action model은 언어·video generation objective로 pretrain해 metric grounding을 직접 요구하지 않는데, GAM은 grounding 자체를 pretraining objective로 삼은 backbone을 골라 foundation의 선택 자체를 바꿈.
- object-centric selective visual representation, PerAct/RVT류 3D 표현과 방향은 겹치나, promptable 3D detection 모델 하나로 language/point/box 입력을 같은 표현으로 통합한 점이 다름.
- 이미지 마스킹, point cloud encoder, MM-DiT, flow matching 등 구성 요소 각각은 선행연구 기법의 조합이라 architecture 자체의 참신성은 제한적이고, 참신성은 grounding을 foundation으로 쓰는 paradigm 제안 쪽에 있음.

**Benchmark results**

- RoboTwin 2.0 50 task single-task 학습(clean scene만): GAM 평균 55.3%(Easy 63.0/Hard 47.6)로 동일 프로토콜 π0.5(44.95%, Easy 64.0/Hard 25.9)를 10점 상회함.
- 50-task co-training VLA/WAM(Spatial Forcing 77.2/26.7, FastWAM 77.8/1.9)은 clean에서 GAM보다 높지만 randomization(Hard)에서 크게 뒤처짐.
- LIBERO-PRO 16개 perturbation 평균 GAM 0.61 vs π0.5 0.53. 타겟 재배치·신규 지정(Pos/Task)에서 격차가 크나(Spatial-Task 0.88 vs baseline 전원 0.11 이하), 물체 외형 변화(Obj)에서는 GAM이 더 낮음(LIBERO-10 Obj 0.50 vs π0.5 0.92).
- 실로봇: bimanual YAM visual shift에서 GAM 17/20 vs π0.5 4/20(clean 대비 retention 89%/21%), Franka 4-task에서는 GAM을 VLM planner(Molmo2)와 결합해 OOD step completion 49.8%를 기록함(π0.5 24.0%, MolmoAct2 17.1%).
- ablation(10 task): image masking 제거 시 평균 46.8%→22.3%, point cropping 제거 시 12.8%, detection/image 중 하나만 쓰면 각각 16.0%/20.3%로 object-centric filtering과 두 stream 결합이 모두 필수임.

**Top-tier conference 적합성 — 73/100 · 추천 venue: CoRL**

실로봇 2 embodiment와 2개 sim benchmark, 명확한 ablation을 갖춰 CoRL/RSS 수준의 실험 증빙은 충족함. backbone·action head 각 구성 요소의 신규성은 낮고 WildDet3D grounding 품질에 성능이 강하게 의존해, reviewer가 기존 기법 조합으로 볼 rejection risk가 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- grounding 오류가 회복 없이 action으로 이어지는 구조라, grounding confidence 기반 실패 감지·recovery module 연구로 바로 확장 가능함.
- VLM planner가 point로 타겟을 지정하고 GAM이 저수준 policy로 동작하는 구조는 long-horizon·memory-dependent manipulation, skill chaining 연구와 직결됨.
- 현재 3D box 수준의 거친 object-centric grounding을 3DGS나 scene graph 기반 표현으로 확장하면 더 정밀한 geometric grounding 연구로 이어질 수 있음.

---

### 3. [70점] The Right Future for Action: Learning Action-Relevant Predictive States in World Action Models

- **분야**: World Model · **robotics relevance**: 8/10
- **arXiv**: [2609.23369](https://arxiv.org/abs/2609.23369) ([PDF](https://arxiv.org/pdf/2609.23369))
- **저자**: Qiwen Gu, Jifan Li, Bingjie Gao, Rui Chen, Jing Tang, Xiangxiang Chu, Junqiao Zhao
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: 19 pages, 5 figures, 8 tables
- **원문 검토**: PDF 전문 · 1차 스크리닝 65점

> 💡 generation-free WAM(world action model)인 Fast-WAM이 내부 video feature를 그대로 action expert에 넘기는데, 어떤 정보를 남겨야 하는지 진단 실험으로 먼저 밝히고 그 결과로 ARPS(Action-Relevant Predictive States)라는 압축 predictive state를 설계함. horizon별 learnable query가 중간 video feature를 V-JEPA2 teacher 기준 미래 표현·변화량으로 학습해 LIBERO-Plus에서 Fast-WAM 대비 39.2%p 향상을 냄.

**Core innovation & methodology**

- 진단 실험 1: predictability와 action readability가 어긋남 — VGGT가 미래 변화 예측은 가장 쉽지만 action readout은 가장 낮음.
- 진단 실험 2·3: 관측된 미래 변화가 현재 표현보다 추가 action 정보를 주고, 그 정보는 소수 spatial location에 집중됨(128개 중 상위 8개가 full readout의 93% 회복).
- 이 진단을 바탕으로 horizon-conditioned state predictor를 설계함: video expert 중간층(15/30 layer) feature를 learnable query(M=32, horizon 2개로 균등 분할)로 압축한 병목 Zt를 만들고, frozen V-JEPA2 teacher의 미래 절대 표현·temporal-difference(Δ) 표현을 training-only로 distill함(cosine+smooth-L1 loss).
- 추론 시엔 teacher와 decoding head를 모두 제거하고 video expert도 해당 layer까지만 실행해, 압축 state만으로 action을 예측함(early termination으로 latency도 줄임).

**Novelty vs. prior works**

- 가장 가까운 선행연구는 Enfold(다중 레벨 미래 조건 state를 현재 시점 표현으로 distill), DC-WAM(temporal change/interaction 영역으로 supervision 재배치), VPP(예측 feature로 inverse dynamics 조건화), RepWAM/AGRA(world model feature alignment)임. ARPS는 이들과 같은 축(representation-level foresight distillation)에 있고 architecture도 Perceiver류 query bottleneck + JEPA distillation의 조합이라 새로운 paradigm은 아님.
- 본질적 기여는 아키텍처가 아니라 diagnostic protocol임 — predictability와 action readability를 분리해 측정하고, teacher/objective/capacity 선택을 진단 결과로 정당화한 절차가 선행연구에 없던 부분임.
- future target을 absolute와 temporal-difference로 나눠 multi-horizon으로 동시 지도한 조합, 그리고 gradient를 video expert까지 흘려보내는 설계는 세부적으로는 새롭지만 각 구성요소 자체는 기존 기법의 재조합에 가까움.

**Benchmark results**

- LIBERO: ARPS 99.2%로 Fast-WAM(97.6%, +1.6%p) 및 embodied pretraining 쓰는 LingBot-VA(98.5%)보다 높음. 단 점수가 포화되어 변별력은 제한적이라고 저자도 인정함.
- LIBERO-Plus(적응 없이 그대로 평가): ARPS 87.3%로 Fast-WAM 재현 결과(48.1%) 대비 +39.2%p, 최강 baseline Cosmos-Policy(82.2%) 대비 +5.1%p. Camera(+74.3%p), Noise(+58.0%p) shift에서 특히 큼.
- RoboTwin 2.0(양팔 조작): ARPS 평균 90.7%로 Fast-WAM(90.7%)과 동률. Clean은 +0.9%p, Random은 -1.0%p로 개선이 일관되지는 않음.
- ablation: future target 없이 present-only면 LIBERO-Plus 49.0%로 급락(-38.3%p), absolute-only 74.9%·Δ-only 80.4%보다 absolute+Δ 결합 87.3%이 더 좋음. bottleneck 없이 dense feature 그대로 쓰는 JEPA-dense는 76.8%로 ARPS보다 10.5%p 낮아 압축 state 자체의 효과를 보임.
- 부가: end-to-end latency 306ms로 Fast-WAM 353ms 대비 13% 감소. 모든 실험은 LIBERO/LIBERO-Plus/RoboTwin 2.0 시뮬레이션에 한정되고 real-robot 검증은 없음.

**Top-tier conference 적합성 — 64/100 · 추천 venue: CoRL**

diagnostic 실험부터 3개 benchmark ablation, state에 noise를 주입해 closed-loop 성능 저하를 보는 intervention 실험까지 통제된 실험이 많아 robot learning venue 기준 empirical conviction이 탄탄함. 다만 architecture 자체는 기존 Perceiver bottleneck·JEPA distillation의 재조합에 가깝고, 단일 backbone(Fast-WAM/Wan2.2)·sim-only·real-robot 미검증이라 oral보다는 poster급 accept 가능성이 높음.

**추천 이유 & 누리랩 연구와의 연결점**

- predictability와 action readability가 어긋난다는 진단 프로토콜은 랩에서 쓰는 다른 world model backbone(VLA용 latent world model 포함)을 검증할 때 그대로 재사용 가능함.
- LIBERO-Plus 같은 distribution shift 하에서 predictive state의 nuisance invariance를 측정한 방식(Fig.3b, App.E)은 failure detection/recovery에서 state 이상 탐지 지표로 응용해볼 만함.
- state에 Gaussian noise를 주입해 closed-loop 성능 저하를 측정한 intervention 방식은 test-time optimization·robustness 평가 도구로 그대로 가져다 쓸 수 있음.

---

### 4. [68점] DexTacWAM: A Visuo-Tactile World-Action Model for Dexterous Manipulation

- **분야**: World Model / Dexterous Manipulation (Tactile) · **robotics relevance**: 9/10
- **arXiv**: [2609.24976](https://arxiv.org/abs/2609.24976) ([PDF](https://arxiv.org/pdf/2609.24976))
- **저자**: Haoran Yuan, Zekai Wang, Boning Shao, Haoran Lu, Trevor Darrell, Ismini Lourentzou, Wei Zhan
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 22 pages. Project website: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 비전 중심 World-Action Model에 다섯 손가락 tactile을 policy 입력이 아니라 world state 자체로 넣은 DexTacWAM을 제안함. 22-DoF bimanual 로봇 6개 contact-rich task에서 평균 70.6점으로 최강 baseline(38.0)을 크게 앞섰고, 그중 4개 binary task 기준으로는 tactile을 world model 예측에서 빼면 점수가 74.7에서 26.6으로 급락해 contact evolution 예측 자체가 핵심 기여임을 ablation으로 보임.

**Core innovation & methodology**

- tactile을 action expert의 보조 입력이 아니라 video diffusion world model이 직접 예측하는 world state의 일부로 취급함
- 손가락별 tactile map을 frozen pretrained visual VAE로 개별 인코딩하고, finger identity embedding + pose encoder + self-attention pooling(5:1) + temporal refinement로 구성된 compressor로 손 단위 latent 하나로 압축함
- 압축된 tactile latent를 video DiT에 추가 view로 붙여 vision·tactile 토큰을 함께 denoising하는 modality-split flow-matching objective로 world model을 학습함
- action expert는 world model latent에 cross-attention하되 visual·tactile 두 modality의 K/V를 따로 RMS normalize해야 학습이 수렴함(안 하면 발산)

**Novelty vs. prior works**

- 기존 visuo-tactile world model(VTAM, VT-WM, OmniVTA)은 parallel gripper 등 단순 end-effector 중심이라 손가락 identity·hand pose 의존적 접촉 구조를 다루지 않음. DexTacWAM은 multi-finger 구조를 보존하는 compressor로 이를 정면으로 다룸
- ViTacFormer는 ACT/CVAE policy 안에서 tactile을 forecast-then-act 방식 auxiliary head로만 예측함. DexTacWAM은 tactile을 world model의 predicted state 자체로 삼아 vision과 joint denoising한다는 점에서 formulation이 다름
- 다만 핵심 구성요소(frozen VAE 재사용, self-attention pooling, RMSNorm)는 각각 기존 기법의 조합이라 architecture 자체의 참신함은 제한적이고, novelty는 dexterous multi-finger tactile을 world state로 다루는 problem formulation에 있음. 가장 가까운 선행연구인 VTAM(저자 본인의 이전 작업)·VT-WM·OmniVTA와 Table 1에서 직접 비교하지 않았고, baseline은 π0.5·ViTacFormer·RDP·Genie Envisioner로 한정됨

**Benchmark results**

- 22-DoF bimanual platform 6개 contact-rich task, task당 20회 real-robot trial 기준 DexTacWAM 평균 70.6점으로 전 task 1위, 최강 baseline RDP는 38.0점
- 4개 binary task(Cube Place, Tongs, Bowl, Bottle Cap) 80회 trial 통합 성공률 68.8%(55/80) vs RDP 30.0%(24/80), Fisher exact test p=1.59×10^-6로 유의함
- 4개 binary task 기준, tactile을 world model 예측에서 빼고 action expert 입력으로만 쓰면 평균이 74.7에서 26.6으로 급락, tactile conditioning만으론 부족하고 contact evolution 예측이 핵심임을 보임
- tactile-encoder ablation: full compressor(pose+temporal)가 contact recall@9 0.725·retention 89.4%로 cross-attention pooling(0.492·62.9%) 대비 크게 개선, finger identity embedding 제거 시 recall@9 0.671로 하락
- vision-to-touch 적응 후 visual PSNR 손실이 0.5dB 이내(95% CI가 0을 포함)이고, tactile compression으로 학습 2.26배·inference 1.29배 가속됨. unseen bowl 색상/개수 generalization은 각각 13/20, 12/20으로 in-distribution과 비슷함

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

real robot 6개 task에서 통계적으로 유의한 성능 개선과 촘촘한 policy-level·encoder-level ablation을 갖춰 contact-rich dexterous manipulation venue에 강점이 있음. 다만 가장 가까운 선행연구(VTAM, VT-WM, OmniVTA)와 직접 비교가 빠져 있고 단일 플랫폼·단일 tactile sensor(Sharpa)에서만 검증돼 일반화 근거가 제한적임. CoRL/RSS 수준 accept은 무난하나 architecture 자체가 기존 기법의 조합이라 oral/highlight까지는 애매함.

**추천 이유 & 누리랩 연구와의 연결점**

- world model의 predicted state에 무엇을 포함시킬지를 재설계한 사례임. 누리랩 world model 연구에서 contact·힘처럼 partially observable한 물리 상태를 world state에 포함시키는 설계 패턴으로 참고 가능
- 논문이 스스로 밝힌 한계가 success-only data라 failure recovery supervision이 없다는 점임. 이는 누리랩의 failure detection·recovery 주제와 바로 연결되는 gap이고, DexTacWAM 위에 perturbation/intervention 데이터를 더해 recovery policy를 얹는 후속 연구가 가능함
- frozen visual VAE를 tactile encoder로 재사용해 4시간 소량 데이터로 새 modality를 붙이는 continual vision-to-touch 전략은 test-time·저자원 적응 문제 전반에 일반화 가능한 아이디어임

---

### 5. [67점] Beyond the Leaderboard: Counterfactual Diagnosis of End-to-End and VLA Driving Policies Under Domain Shift

- **분야**: VLA · **robotics relevance**: 8/10
- **arXiv**: [2609.22582](https://arxiv.org/abs/2609.22582) ([PDF](https://arxiv.org/pdf/2609.22582))
- **저자**: Ruolin Yang, Zilin Huang, Buoyue Wang, Zhengyang Wan, Yuhao Luo, Zihao Sheng, Sikai Chen
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 E2E·VLA 자율주행 정책 6개를 리더보드 순위 대신 counterfactual 편집(보행자 제거, 야간 조명 편집)으로 진단하는 Check-Up 프레임워크를 제안함. 보행자가 경로 위에 있는 경우에도 진짜 회피 반응은 1.9%뿐이고, 기존 리더보드 지표(NAVSIM EPDMS)는 근접보행자 행동과 상관관계가 거의 없음(ρ=-0.09)을 보임.

**Core innovation & methodology**

- 두 causal axis 정의: 보행자 제거가 일으키는 경로 변화인 faithfulness displacement F와, 주행과 무관한 야간 조명 편집이 일으키는 경로 변화인 interference displacement I. F≥0.5m·clearance 증가 ΔS≥0.5m·F>I 세 조건을 모두 만족해야 진짜 회피로 인정함.
- 이 두 축 위에 다섯 개 exam(exposure, hazard sensitivity, scaling, specificity, lighting)을 세워 리더보드 점수 하나가 뭉뚱그리던 행동을 분리함.
- pixel-level paired data 구성: 3D box를 카메라에 투영해 타깃을 정하고 SAM으로 세그먼트·LaMa로 인페인팅해 보행자를 제거하고, 감마·게인·채도·노이즈로 야간 조명을 흉내 낸 photometric perturbation을 적용함. 모든 편집은 독립 detector(Faster R-CNN)로 검증함.
- 사전등록(pre-registration) 전이 검증: 보스턴(좌측통행) 88 frame에서 7개 예측을 미리 고정하고 싱가포르(우측통행) 148 frame으로 검증해, 어떤 진단이 새 도메인으로 옮겨가는지와 그 비용(필요 frame 수)까지 함께 산정함.

**Novelty vs. prior works**

- CheckList·corruption benchmark류는 정확도 하락만 보고 원인은 말하지 않는데, 본 논문은 부호 있는 causal axis(F, I)로 왜 점수가 그렇게 나왔는지까지 귀속시킴.
- CausalAgents가 forecaster에서 non-causal agent를 지워 테스트하는 아이디어를 pixel-level 실제 프레임 편집으로 확장하고, 모든 편집을 detector로 검증하는 절차를 더함. representation engineering·function vector 같은 interpretability의 ablation-attribution 방법을 driving policy 평가에 처음 적용한 것으로 보임.
- 다만 개별 구성 요소(SAM+LaMa 편집, photometric perturbation, ablation 기반 attribution)는 기존 기법의 조합이라, novelty는 새 architecture·representation이 아니라 진단 문제 설정과 사전등록 전이 검증이라는 평가 방법론 자체에 있음. 저자도 이 점을 명시함.

**Benchmark results**

- 246개 NAVSIM 싱가포르 근접보행자 scene, 6개 정책(LTF, DiffusionDrive, DiffusionDriveV2, SimLingo, AutoVLA, Alpamayo-1.5)에서 보행자가 planned path 위에 있는 cell 787개 중 진짜 회피는 15개(1.9%)뿐임.
- open-loop 프로토콜에서 median clearance 변화는 정책별로 최대 0.03m, median 거리 변화는 최대 0.08m로 사실상 반응이 없음.
- 좌측통행→우측통행 사전등록 전이 검증에서 7개 예측 중 4개(lighting verdict, exposure/specificity ordering, collision outcome)는 전이되고, point value와 hazard-sensitivity verdict, 보조 예측 P6은 전이되지 않음(P6은 오히려 반대 방향, ρ=-0.90).
- verdict별 소요 frame: lighting은 14 frame, exposure 순위는 10 frame·specificity 순위는 40 frame 안에 안정화되지만, hazard sensitivity는 57~1326 frame이 필요해 170-frame pool을 넘어서는 정책도 있음.
- 기존 지표는 이 차이를 못 봄: nuScenes L2는 보행자 제거해도 최대 0.07m밖에 안 변하고, NAVSIM EPDMS 순위는 근접보행자 246 scene에서의 순위와 무관함(ρ=-0.09). 8m/s에서 SimLingo가 가장 긴 평균 exposure 시간(2.19초, 인간의 2배 이상)을 보였고, 충돌률도 최고(정면 40.5%/측면 36.6%)임.

**Top-tier conference 적합성 — 58/100 · 추천 venue: ICRA**

6개 공개 정책을 실제 프레임 기준으로 detector-verified counterfactual 편집과 사전등록 전이 검증까지 갖춰 실험적 증거가 탄탄하고, deployment 의사결정에 바로 쓸 수 있는 selection report를 제공함. 다만 open-loop replay 기반이고 조명 편집이 실제 야간 촬영이 아닌 photometric transform이라는 한계가 있고, 새로운 학습 알고리즘이 아니라 진단 방법론이라 CVPR/NeurIPS급 oral보다는 ICRA/IROS 계열의 강한 accept 후보로 보임.

**추천 이유 & 누리랩 연구와의 연결점**

- failure detection·diagnosis, counterfactual/causal reasoning 우선 주제와 직접 연결됨. manipulation VLA에도 물체 제거·조명 변화 같은 counterfactual check-up을 적용해 정책이 어떤 단서에 진짜로 반응하는지 진단하는 방식으로 확장할 수 있음.
- 사전등록 전이 검증(한 도메인에서 만든 예측을 다른 도메인에서 검증)이라는 실험 설계 자체가 학생 연구의 domain shift 평가 rigor를 높이는 참고 틀이 될 수 있음.
- open-loop trajectory 진단이라 contact-rich manipulation처럼 closed-loop 상호작용이 중요한 task에는 그대로 적용하기 어렵고, 편집이 실제 촬영이 아닌 합성이라는 한계도 그대로 옮겨감.

---

### 6. [66점] AffordanceWAM: Affordance-Aware Joint World-Action Modeling for Robot Manipulation

- **분야**: VLA / World Model · **robotics relevance**: 10/10
- **arXiv**: [2609.22332](https://arxiv.org/abs/2609.22332) ([PDF](https://arxiv.org/pdf/2609.22332))
- **저자**: Jiadi You, Qize Yu, Yue Chen, Minghong Cai, Zhide Zhong, Yuran Wang, Bowen Ping, Jiaqi Liang 외 6명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 인간 영상과 로봇 영상을 함께 학습시키기 위해, world model이 예측하는 미래 표현에 RGB뿐 아니라 Scalar Affordance와 Affordance Heatmap을 추가한 AffordanceWAM을 제안함. Masked Joint Self-Attention으로 world 예측과 action 예측을 분리 결합해, affordance가 없을 때는 오히려 성능을 깎던 인간 영상이 affordance를 매개로 하면 RoboCasa·CALVIN·실로봇 전반에서 일관되게 성능을 올림을 보임.

**Core innovation & methodology**

- future World 예측 대상을 RGB 한 가지에서 RGB+Scalar Affordance(상호작용 가능 영역을 나타내는 [0,1] scalar field)+Affordance Heatmap(그 영역을 RGB에 렌더링한 보조 타깃) 세 스트림으로 확장함
- pretrained video DiT(Wan2.2-TI2V-5B) 기반 World Expert와 별도 파라미터의 Action Expert를 layer마다 Masked Joint Self-Attention으로 결합함
- Action은 RGB·Scalar Affordance만 읽고, Heatmap과 Action 자체 정보는 World로 역류하지 못하게 막음
- 인간 영상은 World Expert만 학습시키고(RGB+두 affordance 타깃), 로봇 궤적만 Action Expert까지 학습시켜 action label 없는 인간 데이터가 world 표현을 통해서만 로봇 제어를 돕도록 설계함
- flow matching으로 world·action을 동시에 생성한 뒤, 완성된 world를 고정하고 action만 추가로 denoising 정제하는 2단계 inference(joint generation + refinement)를 사용함

**Novelty vs. prior works**

- 가장 가까운 prior인 UWM·WorldVLA류 world-action model은 RGB나 visual latent만 미래 타깃으로 삼는데, AffordanceWAM은 affordance를 world의 생성 타깃 자체로 만든 점이 차별점임
- CoA-VLA·RT-Affordance·AffordVLA 등 기존 affordance-aware VLA는 affordance를 policy 입력이나 중간 예측으로만 쓰는데, 이 논문은 affordance를 human-robot 공유 supervision 신호로 명시적으로 분리해 사용함
- 다만 backbone(Wan2.2 video DiT), flow matching objective, dual-expert 결합 구조 자체는 UWM 등 기존 틀을 그대로 가져온 것이라 새로움은 representation 설계와 masking 메커니즘에 국한됨

**Benchmark results**

- RoboCasa 평균 성공률 69.4%로 Cosmos Policy(50 demos/task, 67.1%) 대비 2.3%p 높음. 단 UWM(60.8%)은 1,000 demos/task를 썼고 이 논문은 300 demos/task라 baseline 간 학습 조건이 다름
- CALVIN ABC→D 평균 sequence length 4.22로 최고 baseline VPP(4.01) 대비 개선. 1/5~5/5 성공률도 96.1/92.8/85.5/77.8/69.5%로 전부 최고
- 핵심 ablation: affordance 없이 인간 영상을 추가하면 RoboCasa 57.3%→55.1%, CALVIN 3.75→3.68로 오히려 하락하지만, affordance를 쓰면 63.7%→69.4%, 3.91→4.22로 상승함. 이 부호 반전이 affordance가 human-robot 전이의 핵심 매개라는 근거임
- Affordance Heatmap→Action attention을 막지 않으면(마스킹 제거) RoboCasa 69.4%→63.5%, CALVIN 4.22→3.85로 떨어져 masking 설계의 효과를 뒷받침함
- 실로봇에서는 Cosmos Policy 단일 baseline 대비 기본 5개 task 평균 42.7%→74.7%, 복잡 3개 task 중 서랍 닫기 46.7%→80.0%, 꽃 정리 6.7%→20.0%로 개선. 각 task 50 demo, 15 trial 기준이고 baseline이 하나뿐임

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

human-to-robot 전이·world model·affordance라는 누리랩 우선 주제와 정확히 맞고, sim 2개 benchmark(RoboCasa, CALVIN)에 seed 3회 반복·std 보고와 실로봇 8개 task까지 갖춰 실험적 증거가 탄탄함. 다만 실로봇 baseline이 Cosmos Policy 하나뿐이고 sim baseline들도 demos/task 조건이 서로 달라 공정 비교인지 의문이 남아, top-tier full paper는 가능하나 oral·highlight까지는 확신하기 어려움.

**추천 이유 & 누리랩 연구와의 연결점**

- affordance를 world model의 생성 타깃으로 삼아 human video를 robot data와 공유 supervision으로 묶는 방식은 human-to-robot transfer·world model 연구에 바로 참고할 만함
- Masked Joint Self-Attention으로 world와 action 간 정보 흐름을 선택적으로 차단하는 설계는 failure detection/recovery에서 world 예측과 action 예측을 분리 진단하는 데도 응용 가능함
- real-world 3개 복잡 task에서의 실패 유형 분류(spatial drift, RGB-copy collapse, wrong-object localization)는 world model 기반 실패 진단 연구의 참고 사례로 쓸 수 있음

---

### 7. [66점] EgoWild2Dex: Learning Dexterous Robotic Manipulation from In-the-Wild Human Experience

- **분야**: Manipulation/Dexterous (VLA) · **robotics relevance**: 9/10
- **arXiv**: [2609.23755](https://arxiv.org/abs/2609.23755) ([PDF](https://arxiv.org/pdf/2609.23755))
- **저자**: Kunyang Lin, Xutao Wen, Jingxi Lin, Lanyong Lin, Jiaming Liu, Tianshuo Yang, Xianchi Chen, Yue Han 외 3명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 가정·공장·약국 등 실환경에서 촬영한 538.9시간 규모 egocentric human 데이터셋 EgoWild와 homography 기반 경량 view alignment 모듈 GeoFormer, 3단계 progressive human-robot training을 결합해 양팔 dexterous manipulation을 학습함. 로봇 전문 데모 1시간 미만으로 3개 long-horizon bimanual task에서 평균 96.7% 성공률을 달성했고, π0·π0.5·GR00T-N1.7을 같은 100개 demo로 direct fine-tuning한 결과 대비 압도적으로 높은 성공률을 보임.

**Core innovation & methodology**

- GeoFormer는 8차원 homography 파라미터를 matrix exponential로 표현하고 cascaded refinement predictor로 robot-to-ego warp를 예측함. Wasserstein critic 기반 adversarial loss로 robot 이미지를 ego 배경에 자연스럽게 합성하도록 학습해, 3D reconstruction·inpainting 없이 view alignment를 수행함.
- Progressive 3단계 학습: (1) EgoWild 538.9시간으로 VLM에 broad manipulation prior를 학습함.
- (2) task-specific ego·glove·소량 로봇 데이터로 co-training하며, 이때 frozen GeoFormer로 ego 관측을 robot view로 정렬함. (3) 로봇 전문 시연과 DAgger recovery(Anchored Delta-Cmd)로 execution·contact gap을 refinement함.
- 사람 손동작·glove·로봇 데이터를 동일한 IK·retargeting 파이프라인으로 변환해 팔 관절각+손 모터값으로 구성된 하나의 robot-native action space로 통일하고, 전 단계에서 같은 flow-matching objective로 학습함.
- Anchored Delta-Cmd는 human takeover 시 로봇 명령을 takeover 시점 값에 anchor하고 이후 조작자의 상대 동작을 더해 명령 jump 없이 DAgger recovery 데이터를 수집하는 teleoperation 기법임.

**Novelty vs. prior works**

- EgoMimic·EgoVLA·Being-H0·DexWild 등 기존 ego-human 데이터 연구는 통제된 촬영 환경이나 대규모 비공개 데이터에 의존하는데, 본 논문은 실제 비통제 환경에서 밀집된 clutter(프레임당 instance 34.78개, EgoDex 대비 7.71배)와 큰 head rotation(15.93도/초, EgoDex 대비 3.8배)을 가진 데이터를 직접 수집함. 데이터 자체의 다양성이 핵심 기여임.
- GeoFormer는 spatial transformer network와 ST-GAN 스타일 homography 예측·adversarial 합성을 robot view alignment에 적용한 것으로, MoGe reprojection+LaMa inpainting 파이프라인 대비 구조는 단순화했지만 구성 요소 자체는 기존 기법의 재조합에 가까움. Homography는 global projective warp만 표현하므로 시차가 큰 근접 조작 장면에서는 근사적 정렬에 그침.
- 3단계 progressive training(broad pretraining→task-specific co-training→DAgger refinement)은 이미 널리 쓰이는 커리큘럼 구조이며, 새로운 learning paradigm이라기보다 ego-human 데이터를 이 구조에 맞춰 정리한 practical recipe에 가까움. 정책 구조와 목적함수 자체는 새롭지 않음.

**Benchmark results**

- Table I: 100개 로봇 전문 시연만으로 direct fine-tuning한 π0(평균 score 2.7/success 3.3%), π0.5(4.2/6.7%), GR00T-N1.7(2.1/0.0%) 대비 EgoWild2Dex 전체 파이프라인은 평균 score 9.8/성공률 96.7%로 압도적으로 높음.
- Table II ablation(Open-Box task): robot-domain refinement만 쓰면 1.4/0.0%, Human-to-Robot learning만 추가하면 5.1/20.0%, Human-Robot co-training만 추가하면 7.5/40.0%, 두 단계 모두 합치면 8.8/70.0%, Anchored Delta-Cmd DAgger까지 더하면 9.5/90.0%로 각 단계 기여가 확인됨.
- Table III: GeoFormer는 Project+Inpaint(MoGe+LaMa) 대비 평균 latency를 162.58ms에서 7.43ms로(21.9배 speedup), GPU-h/1M frame을 45.16에서 2.06으로 줄이면서 PSNR은 +1.05dB, LPIPS는 -11.46% 개선했고, Open-Box task 성공률도 80%에서 90%로 향상시킴.
- Table IV 일반화: 학습에 쓴 bouquet를 제외한 seen object 3종은 평균 score 8.1/성공률 70.0%, unseen object 3종은 평균 score 7.0/성공률 33.3%로 저하됨. Embodiment 전이는 Piper에서 Tianji Marvin Pro arm으로 fine-tuning 시 Task I에서 score 9.2/성공률 60%를 기록함.
- 전 실험은 real robot 3개 task(각 10 trial)에 국한되고 sim 검증은 없으며, direct fine-tuning 베이스라인은 100개 demo라는 제한된 조건에서만 비교됨 — 더 많은 demo로 fine-tuning했을 때의 격차는 본문에서 확인 불가.

**Top-tier conference 적합성 — 60/100 · 추천 venue: CoRL**

538.9시간 규모 실환경 ego 데이터셋 공개와 3개 long-horizon bimanual dexterous task에서 평균 96.7% 성공률이라는 강한 real-robot 증거가 강점임. GeoFormer와 progressive training은 각각 기존 기법(spatial transformer, DAgger)의 조합에 가까워 formulation 신규성은 제한적이고, 평가가 자체 구축한 3개 task와 단일 로봇 플랫폼(Piper+Revo2)에 집중돼 있어 일반화 주장은 조심스럽게 읽어야 함. CoRL/ICRA 수준의 systems+data 논문으로 적합하나 oral/highlight급 conceptual leap는 약함.

**추천 이유 & 누리랩 연구와의 연결점**

- EgoWild 데이터셋과 GeoFormer alignment는 실로봇 환경에서 human video로 policy를 즉석 보정하는 test-time optimization 연구의 재료로 쓸 수 있음.
- Anchored Delta-Cmd 기반 DAgger recovery 수집 방식은 human correction을 학습 데이터로 흡수하는 절차로 failure detection·recovery 연구에 참고할 만함.
- 3단계 progressive training(broad prior→task co-training→refinement)은 data-efficient adaptation recipe로 학생 연구의 long-horizon manipulation 실험 설계에 벤치마킹할 수 있음.

---

### 8. [66점] What Matters in Designing World Action Models: An Empirical Study

- **분야**: World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.24048](https://arxiv.org/abs/2609.24048) ([PDF](https://arxiv.org/pdf/2609.24048))
- **저자**: Chao Tang, Haoqing Wang, Zilang Cen, Weishi Mi, Wei Xia, Fangcheng Liu, Anda Cheng, Yeqing Shen 외 4명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 새 아키텍처 제안 없이 World Action Model(WAM)의 세 설계 축인 video-action causal structure(6종)·latent representation(8종)·world-action objective(4종)를 같은 base model 안에서 통제 비교한 실증 연구임. RoboCasa-GR1(ID)·LIBERO-Plus(OOD)·DROID real-robot 데이터셋 offline action prediction 실험을 통해 미래 예측은 정확한 pixel 내용보다 시간적 구조로 action에 영향을 주고, framewise latent가 OOD에 강하며, video generation objective를 먼저 학습한 뒤 dynamics objective를 얹는 staged training이 가장 좋다는 결론을 냄.

**Core innovation & methodology**

- 새 architecture를 제안하는 대신 causal structure(disentangled/video-to-action/action-to-video/bidirectional/joint/causally interleaved), latent representation(semantic/geometric/reconstructive/predictive 4 family, 8종), training objective(BC/IDM/FDM/VG)라는 WAM 설계 축을 같은 프레임워크·학습 파이프라인 안에서 분리해 비교함.
- 구조 비교뿐 아니라 route-enabled 정책에 content corruption(future latent를 noise로 치환)과 temporal reversal(future slot 순서 뒤집기) intervention을 직접 가해, 생성된 future가 실제로 action 예측에 인과적으로 기여하는지 검증함.
- linear probing(hidden state에서 expert action을 R^2로 복원)으로 latent 종류별 action decodability를 측정하고, 이를 ID/OOD 성능 순위와 대조함.
- latent representation, causal structure, training objective 각각의 대표 variant를 RoboCasa-GR1·LIBERO-Plus 뿐 아니라 real-robot DROID offline action prediction으로도 재검증함.

**Novelty vs. prior works**

- 새 architecture·representation을 제안하지 않는 순수 통제 실증 연구임. RoboVLMs·OpenVLA-OFT 같은 VLA design study를 WAM 영역으로 확장한 성격에 가까움.
- 'World Action Models: The Next Frontier in Embodied AI', 'World Model for Robot Learning: A Comprehensive Survey' 같은 WAM survey나 'Do World Action Models Generalize Better Than VLAs? A Robustness Study' 같은 WAM-VLA robustness 비교 논문과 달리, content corruption·temporal reversal 같은 직접 개입 실험으로 generated future가 실제로 action을 인과적으로 좌우하는지 검증한 점이 방법론적 차별점임.
- 핵심 결론(temporal structure가 content보다 중요, framewise latent가 OOD에 유리, staged training이 유리)은 개념적으로 새로운 paradigm이라기보다 기존 설계 선택의 원인을 실증적으로 규명한 것이라 novelty는 새 이론보다 분석 방법론과 결과의 일반화 가능성에 있음.

**Benchmark results**

- route-enabled causal structure(Joint vs Uncond, Bidirectional vs Action-to-Video)는 LIBERO-Plus OOD에서 각각 16.14%p·14.93%p 개선했지만 RoboCasa-GR1 ID에서는 각각 2.33%p·4.00%p 하락함.
- temporal reversal intervention은 ID에서 action 변화 2.30~2.41%·성공률 6.08~11.08%p 하락, OOD에서는 action 변화 12.79~14.36%·성공률 24.24~32.37%p 하락으로 훨씬 크게 나타났고, content corruption은 성공률 변화가 거의 없었음.
- Causally Interleaved가 6개 causal structure 중 LIBERO-Plus 77.33%로 최고였고, 변형인 Video-Causal Global은 79.84%로 2.51%p 더 높았음(성공률 기준, 이하 %p로 통일).
- training objective에서는 BC-only가 RoboCasa-GR1(ID) 최고이고, VG 추가로 LIBERO-Plus(OOD) 성공률이 77.96%에서 81.22%로 개선됨. 4개 objective를 처음부터 joint training하면 성능이 떨어지지만 BC+VG를 80% 학습 후 dynamics objective를 추가하는 staged schedule은 83.15%로 최고를 기록함.
- real-robot DROID offline action prediction에서 Causally Interleaved(MSE 0.0666 vs Uncond 0.0730), DINOv3(framewise latent, MSE 0.0684 vs 대표적 inter-frame latent인 DA3의 0.0702), BC+VG(MSE 0.0697 vs BC-only 0.0769)가 L1·Accuracy@0.1·Accuracy@0.5 4개 지표 모두에서 일관되게 우세해, framewise latent가 distribution shift가 큰 real-robot 세팅에서 더 강건하다는 simulation 결론을 뒷받침함.

**Top-tier conference 적합성 — 60/100 · 추천 venue: CoRL**

동일 프레임워크에서 세 설계 축을 통제 비교하고 real-robot DROID로 재검증한 점은 CoRL/RSS 커뮤니티가 실질적인 WAM 설계 지침으로 받아들일 만함. 다만 새 아키텍처·representation 제안이 없고 real-robot 평가가 closed-loop rollout이 아닌 offline action prediction에 그쳐, oral/highlight보다는 poster 수준 accept 가능성이 커 보임.

**추천 이유 & 누리랩 연구와의 연결점**

- framewise latent(DINOv3 등)가 OOD에 강건하다는 결과는 우리 lab의 failure detection·recovery 연구에서 world model latent 선택 기준으로 바로 참고할 수 있음.
- content corruption에는 둔감하고 temporal reversal에만 민감하다는 causal intervention 방법론은 우리 world model이 실제로 미래를 보고 action을 내는지 진단하는 도구로 그대로 가져올 수 있음.
- BC+VG를 먼저 학습하고 후반에 dynamics objective를 얹는 staged curriculum은 test-time optimization·auxiliary objective 설계에서 참고할 만한 practical recipe임.

---

### 9. [66점] Latent Policy Steering: An Efficient and Flexible Framework for Cross-Embodiment Transfer

- **분야**: World Model / Cross-Embodiment Transfer · **robotics relevance**: 9/10
- **arXiv**: [2609.22521](https://arxiv.org/abs/2609.22521) ([PDF](https://arxiv.org/pdf/2609.22521))
- **저자**: Yiqi Wang, Mrinal Verghese, Jeff Schneider
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 optical flow를 embodiment-agnostic transition representation으로 써서 여러 로봇·인간 데이터로 Dreamer 기반 world model을 사전학습하는 Latent Policy Steering(LPS)을 제안함. target robot 데모 50개로 finetune한 뒤 base policy(Diffusion Policy, Pi0.5)를 재학습 없이 world model latent space에서 test-time에 steering해, Robomimic·real-world 대부분의 조건에서 base policy 대비 성능을 끌어올림(단 action chunking horizon을 크게 늘리면 역전됨).

**Core innovation & methodology**

- optical flow를 embodiment-agnostic transition representation으로 써서 image-based world model(Dreamer v3 기반)을 로봇 6종+human play data 등 9개 embodiment, 약 55시간 데이터로 pretrain함.
- flow encoder는 선행연구(FlowRetrieval, Motus)처럼 VQ-VAE로 별도 학습하지 않고 world model과 end-to-end로 학습해 추가 학습 단계를 없앰.
- target embodiment(Franka) 데모 50개로 finetune할 때 optical flow encoder를 실제 robot action으로 교체해, 같은 world model이 policy 종류와 무관하게 재사용되도록 함(policy-agnostic).
- base policy가 샘플한 action plan을 world model latent space에서 굴려 expert state와의 cosine similarity 기반 penalty를 reward에 추가함.
- expert state와 policy가 방문할 state 양쪽으로 value function을 학습해(offline RL pessimism과 유사) inference 시 여러 plan 중 최고 value plan을 open-loop 실행함.

**Novelty vs. prior works**

- optical flow를 embodiment-invariant 신호로 쓰는 아이디어 자체는 FlowRetrieval, Motus 등 선행연구에 이미 있어 representation 차원의 새로움은 제한적임.
- 이 논문의 차별점은 flow encoding을 world model과 end-to-end로 합쳐 별도 학습 단계를 없앤 것과, pretraining과 finetuning을 분리해 policy 재학습 없이 어떤 base policy든 steering 가능하게 만든 policy-agnostic 설계임.
- latent action 기반 cross-embodiment 사전학습(LAPA, Moto)과 달리 latent action이 의미있는지 보장이 안 되는 문제를 optical flow로 우회하지만, 핵심 구성요소(world model planning, policy steering, distribution-shift penalty)는 각각 기존 연구(Dreamer, value-guided policy steering, offline RL pessimism)의 조합이라 새로운 paradigm이라기보다는 파이프라인 통합에 가까운 기여임.

**Benchmark results**

- Robomimic 4개 task(Lift/Can/Square/Transport, Franka), target demo 50개 기준: DP 57.2%→LPS-DP 66.7%(상대 개선 16%), Pi0.5 60.9%→LPS-Pi0.5 66.0%(상대 개선 8%).
- real-world 4개 task(pick-place, tool use, deformable object 포함, task당 20 trial): DP 46.2%→LPS-DP 75.0%, Pi0.5 68.8%→LPS-Pi0.5 80.0%로 sim보다 real-world에서 개선폭이 더 큼.
- ablation(Can task): pretrain 유무가 가장 큰 영향(LPS-DP 88.0% vs no-pretrain 81.0%). distribution-shift penalty 없이 non-expert state만 추가하면 base policy(77.8%)보다 낮은 76.5%로 성능이 떨어짐.
- sample efficiency: pretrain된 LPS-DP가 target demo 50개로 DP의 target demo 100개 성능을 넘어서, target demo 요구량을 절반으로 줄이는 효과를 보임(Can task 기준).
- horizon ablation에서 LPS는 action chunking horizon 4~16까지는 DP를 능가하지만 24로 늘리면 역전됨. Square task처럼 단순 pick-and-place에서는 대형 VLA(Pi0.5)가 LPS-DP보다 여전히 강함을 저자가 명시함.

**Top-tier conference 적합성 — 58/100 · 추천 venue: ICRA**

real robot 4개 task와 2개 baseline(DP, Pi0.5) 대비 일관된 개선, scalability·ablation 분석까지 갖춘 실증이 강점임. 다만 target embodiment가 Franka 하나뿐이고 핵심 아이디어가 기존 world model planning·policy steering·offline RL pessimism의 조합에 가까워, conceptual novelty만으로 CoRL/RSS oral을 노리기보다 ICRA/IROS full paper급 완성도로 보임.

**추천 이유 & 누리랩 연구와의 연결점**

- test-time optimization/inference-time planning과 직접 연결됨. value function이 낮은 plan을 사전에 걸러내는 구조를 실패 예측·recovery 판단에 확장할 여지가 있음.
- world model 기반 latent search가 Pi0.5 같은 VLA에도 재학습 없이 붙는다는 점은 누리랩의 VLA test-time steering 실험에 baseline이나 구성요소로 바로 가져다 쓸 수 있음.
- optical flow를 embodiment-agnostic transition representation으로 쓰는 방식은 다른 embodiment로 확장하거나 object-centric 3D representation과 결합해 robot memory·world model 연구로 넓힐 여지가 있음.

---

### 10. [64점] Stable and Efficient Real-World Online VLA Post-Training via Asynchronous Replay-Anchored Policy Improvement

- **분야**: VLA/Online RL · **robotics relevance**: 9/10
- **arXiv**: [2609.22888](https://arxiv.org/abs/2609.22888) ([PDF](https://arxiv.org/pdf/2609.22888))
- **저자**: Jiarui Yang, Jiajin Zhang, Bin Zhu, Jingjing Chen, Yu-Gang Jiang
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 9 pages, 7 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 온라인 VLA post-training에서 rollout과 학습을 비동기로 병행하되, critic과 actor 업데이트를 모두 replay된(기록된) 행동에만 고정시키는 RAPolicy를 제안함. Franka 로봇 실험에서 1~2시간 온라인 학습만으로 단일 task 평균 86.3% 성공률을 냈고, 5-task joint setting에서는 성공률을 52%에서 88%로 끌어올림.

**Core innovation & methodology**

- Critic은 in-sample expectile regression(IQL 방식: 현재 정책이 새로 뽑은 action이 아니라 replay에 실제 기록된 action의 Q-value만으로 value를 맞추는 offline RL 기법)으로 chunk-level value를 학습함. Bellman target이 V'(s_{t+1}) 하나로만 구성돼 다음 action을 예측할 필요가 없어 critic 업데이트마다 VLA forward pass가 추가로 안 붙음.
- Actor는 π0.5 기반 one-step flow actor임. rollout 시 뽑은 초기 Gaussian latent z_t를 저장해두고 학습 때 그대로 재사용해서, 새 noise를 뽑는 flow-matching 없이 advantage-weighted conditional likelihood(AWAC 방식: advantage가 클수록 그 행동의 likelihood를 더 크게 밀어주는 학습)로 one-step mapping을 직접 supervise함.
- rollout과 optimization을 별도 프로세스에서 동시에 돌리고, update group(critic 20회 + actor 5회)마다 rollout 정책을 동기화함. replay buffer는 online buffer(전체 rollout)와 demo buffer(사람 개입 trajectory + 가장 빠른 성공 20개, 계속 갱신)로 나눠 50:50 샘플링함.
- 이 설계 전체를 'replay anchoring'이라 부름 — critic·actor 어느 쪽도 현재 정책이 새로 생성한 action에 대한 value 추정을 학습 신호로 쓰지 않도록 해서, 비동기 학습에서 replay reuse가 커질 때 생기는 value 오차 전파를 막는 것이 핵심 주장임.

**Novelty vs. prior works**

- 가장 가까운 prior work는 IQL(in-sample offline RL), AWAC(advantage-weighted behavior cloning), ALOE(비동기 VLA post-training + action-level off-policy evaluation), FQL(multi-step flow policy를 별도 one-step actor로 distill)임.
- 본질적 차이는 FQL류가 teacher policy에서 distill해 별도 one-step actor를 만드는 반면, RAPolicy는 원래 flow actor의 solver step을 1개로 줄이고 rollout 때 쓴 latent를 그대로 재사용해 teacher나 distillation 단계 없이 직접 학습한다는 점임. 이 latent 재사용이 실질적 기여로 보임.
- 다만 in-sample critic(IQL)과 advantage-weighted actor(AWAC) 자체는 새 learning paradigm이 아니라 기존 offline RL 기법을 async VLA 세팅에 옮겨 붙인 조합이라, formulation 차원의 신규성은 제한적임. novelty는 '새 알고리즘'보다 '비동기 실로봇 세팅에서 안정적으로 작동하도록 조합하고 검증했다'는 쪽에 가까움.

**Benchmark results**

- 단일 task 4개(Plug Charger·Pick Banana·Stack Blocks·Wipe Whiteboard)를 Franka Research 3에서 평가함. baseline은 ALOE, EXPO-FT, HIL-SERL(Plug Charger만)임.
- 동일 online-time budget에서 20 trial 최종 성공률: Plug Charger 100%, Pick Banana 95%, Stack Blocks 70%, Wipe Whiteboard 80%로 SFT 대비 각 95/80/70/70%p 개선함. 가장 강한 baseline 대비로는 각 15~40%p 높음.
- abstract·introduction은 위 task별 %p 수치와 별도로, 가장 강한 baseline인 EXPO-FT 대비 평균 rollout 성공률 72.5% 상대 개선이라는 집계 수치를 따로 보고함.
- Joint 5-task setting(10 trial/task)에서 overall 성공률 52%→88%로, HG-DAgger(70%)보다 18%p 높음. 두 stacking task 합산 성공률은 15%→75%로 가장 큰 개선폭을 보임.
- Ablation(Plug Charger 단독 기준)에서 one-step actor·replay-anchored critic·stored-latent likelihood 각각이 2/3-step actor, predicted-action bootstrap, flow-matching 업데이트보다 빠르고 안정적으로 수렴함을 확인함. 세 대안 변형 모두 40분 시점 10~64%에 머문 반면 RAPolicy는 30분 내 100%에 도달함. intervention rate 개선은 그래프로만 제시돼 baseline 대비 구체적 수치는 본문에서 확인 불가.

**Top-tier conference 적합성 — 58/100 · 추천 venue: CoRL**

실로봇 5개 세팅(단일 4개+joint 5-task)에서 일관된 정량적 우위와 세 갈래 ablation으로 design 각 요소를 정당화한 점이 강점임. 반면 baseline인 ALOE·EXPO-FT가 모두 2026년 최근 preprint로 아직 검증되지 않았고, 단일 로봇팔·단일 랩 환경이라 일반화 근거가 약하며, 알고리즘 자체는 IQL·AWAC 조합의 응용이라 formulation 참신성은 낮아 oral보다는 main track 수준으로 판단함.

**추천 이유 & 누리랩 연구와의 연결점**

- 학습된 V(s_t)가 사람 개입에 의한 실패와 회복 구간을 반영한다는 결과(Fig.7)는 failure detection·recovery 연구에서 value function을 실패 신호로 재활용하는 아이디어로 확장할 수 있음.
- replay anchoring 원칙(critic·actor 모두 기록된 행동에만 학습 신호를 고정)은 test-time/online VLA adaptation을 다루는 다른 연구에서 안정성 확보 레시피로 참고할 만함.
- online buffer + demo buffer(최고 성공 trajectory 자동 갱신) 구성은 continual online learning에서 robot memory curation 전략으로 가져다 쓸 수 있음.

---

### 11. [60점] Hierarchical Aggregation of Semantic Uncertainty in 3D Scene Graphs

- **분야**: 3D Vision · **robotics relevance**: 8/10
- **arXiv**: [2609.22351](https://arxiv.org/abs/2609.22351) ([PDF](https://arxiv.org/pdf/2609.22351))
- **저자**: Carlos Cueto Zumaya, Iacopo Catalano, Wallace Moreira Bessa, Julio A. Placed
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 open-vocabulary 3D scene graph가 이미 갖고 있는 detector confidence와 embedding만 재활용해 추가 학습·추가 쿼리 없이 물체별 신뢰도를 확률로 바꾸고, 이를 containment hierarchy를 따라 room 단위 belief로 전파하는 프레임워크임. HM3DSem 6개 scene에서 HOV-SG에 적용해 object retrieval을 개선하고 room-level assertion의 Brier score를 대체로 낮추나, frequent class에서는 오히려 naive baseline보다 나빠짐.

**Core innovation & methodology**

- 문제 설정: 3DSG가 저장은 하지만 query 시점엔 버려지는 detector confidence와 visual/text embedding을 재활용해 물체 신뢰도를 정의함.
- 4개 신호(detection confidence, cross-view consistency, vocabulary membership, semantic·coherence margin)를 각각 CLIP 로짓 스케일의 확률로 변환함. 순서대로 false positive, fusion error, OOD 여부, labeling error를 나타내는 지표임.
- 4개 신호를 chain rule로 조건부 곱해 물체 확률 q_i를 산출하고, positive association 이론으로 이 곱이 실제 확률의 conservative estimate임을 보임.
- room 단위 집계에서는 한 room의 물체들이 같은 detector·vocabulary·trajectory를 공유해 오류가 서로 correlated임을 근거로, 독립 가정(noisy-OR)이 아닌 fully correlated limit(=object 확률의 최댓값)을 belief로 채택함.

**Novelty vs. prior works**

- 가장 가까운 prior work인 Zhang et al.(arXiv:2606.08277)은 물체마다 여러 view의 caption을 추가로 쿼리해 분산을 재는 반면, 본 논문은 추가 쿼리 없이 그래프가 이미 저장한 값만으로 room 단위까지 전파함. 다만 직접 성능 비교 실험은 없음.
- negative-label 기반 OOD 확률, CLIP 로짓 margin, cross-view consistency 등 개별 신호는 기존 기법의 재조합이고, 새로운 부분은 이를 3DSG containment hierarchy에 correlation-aware하게 묶은 집계 설계임.
- belief는 room type에 대한 사전 지식(예: 침실엔 보통 침대가 있다)을 전혀 반영하지 못하는 한계를 저자도 인정함, novelty가 집계 방식에 국한됨.

**Benchmark results**

- HM3DSem 6개 scene, HOV-SG 위에 얹어 평가함. object retrieval에서 macro OS@1 24.07→26.21(+2.14pt), OS@3 29.04→30.29, OS@5 29.81→30.84, OMRR@5 0.26→0.28로 개선되나, 6개 중 2개 scene에서는 OS@1이 오히려 하락함(00824 -1.33pt, 00849 -3.49pt).
- room-level Brier score(낮을수록 좋음): as-built(모든 entry를 확실하다고 가정) 0.80 → noisy-OR(독립 가정) 0.47 → 제안 belief(fully correlated) 0.33, 95% bootstrap CI [0.30,0.34]로 as-built CI [0.76,0.83]과 겹치지 않음. AUROC도 0.50→0.61로 상승함.
- class frequency별로는 결과가 엇갈림: frequent class에서는 as-built가 오히려 가장 낮은 Brier(0.17, belief는 0.25)를 기록하고, rare class에서는 belief가 가장 낮음(0.33 vs as-built 0.91)임.
- 평가는 단일 3DSG 시스템(HOV-SG), 단일 시뮬레이션 데이터셋(HM3DSem 6 scene, 500 scene-class query)에 한정되고 real-robot 실험은 본문에서 확인 불가.

**Top-tier conference 적합성 — 52/100 · 추천 venue: ICRA**

이론적 유도(chain rule 분해, association of random variables 기반 bracket)가 탄탄하고 기존 파이프라인을 수정하지 않고 얹는 실용성이 강점임. 검증이 단일 시스템(HOV-SG)·단일 시뮬레이션 데이터셋 6 scene에 그치고 real-robot 실험이 없으며, frequent class에서 naive baseline에도 못 미치는 결과가 rejection risk임. top-tier oral보다는 ICRA/RAL급 solid contribution으로 판단함.

**추천 이유 & 누리랩 연구와의 연결점**

- scene graph/semantic mapping 우선주제와 직결됨. robot이 query 응답의 신뢰도를 갖는다는 점에서 failure detection/recovery 파이프라인의 전처리 신호로 활용 가능함 — 불확실한 entry를 재관측하거나 확인 요청하는 recovery 트리거로 연결 가능함.
- closed-form·training-free라 test-time/inference-time 활용에 바로 붙일 수 있음. 우리 lab의 3DGS/scene graph 기반 world representation 연구에 신뢰도 있는 map 요소로 결합해볼 만함.
- room-type prior 결합과 containment edge 자체의 불확실성 전파는 저자도 미해결로 남긴 부분이라, robot memory·active perception/NBV 연구에서 언제 map을 믿고 언제 재탐색할지 정하는 후속 연구로 확장 가능함.

---

### 12. [60점] Think Like a World Model, Act Like a VLA: Distilling World-Model Representations into Compact Robot Policies

- **분야**: VLA / World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.24682](https://arxiv.org/abs/2609.24682) ([PDF](https://arxiv.org/pdf/2609.24682))
- **저자**: Trung Dao, Sankalp Yamsani, Jaden Park, Joohyung Kim, Yong Jae Lee
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 VLA 학생 정책의 pooled 이미지 토큰 특징을 frozen world model(Cosmos3-Nano)의 캐시된 특징에 코사인 정렬시키는 loss 하나만 학습에 추가함. 배포 시엔 teacher와 projector를 모두 버리고 원래 크기의 VLA를 그대로 실행해 지연시간·메모리 증가 없이 LIBERO·RoboCasa-GR1에서 2~3%p, 실로봇 3개 과제에서는 6.7~13.3%p 성능을 올림.

**Core innovation & methodology**

- world model의 미래 예측 능력이 아니라 그 결과로 생긴 internal feature만 필요하다는 문제 설정임. 생성은 feature를 만든 수단일 뿐이라 grounding과 generative 추론 비용을 분리할 수 있다고 주장함.
- frozen teacher(Cosmos3-Nano, Cosmos 3의 Qwen3-VL-8B reasoner 부분)를 학습 프레임에 대해 딱 한 번 돌려 (trajectory id, index)로 memory-mapped cache를 만들고, student 학습 중엔 teacher forward 없이 캐시만 읽음.
- student의 마지막 layer pooled image-token feature를 2-layer MLP projector로 teacher 차원에 맞춰 cosine loss로 정렬함(stop-gradient, λ=0.5). action loss는 순수 flow-matching으로 ground-truth 행동만 쓰고 teacher의 action 채널은 전혀 사용하지 않음.
- 배포 정책은 undistilled baseline과 flow step 수까지 아키텍처가 완전히 동일함. projector와 teacher는 학습 후 버려 추론 비용이 0.8B 기준 32ms, 1.86GB(RTX 5090)로 그대로 유지됨.

**Novelty vs. prior works**

- 기법 자체는 REPA(diffusion transformer 중간 feature를 frozen self-supervised encoder에 정렬)를 world model teacher·로봇 정책 student로 옮긴 것이라 알고리즘 novelty는 제한적임.
- 이 논문의 실질 기여는 서로 다른 teacher 3종(omnimodal VLM인 Cosmos3-Nano, video diffusion 기반 WAM인 Fast-WAM, self-supervised encoder-predictor인 V-JEPA2-AC)에서 모두 이득이 나온다는 것과, student scale(0.8B~4B)·backbone(Qwen3.5-VL, InternVL, Qwen3-VL)·정렬 layer를 바꿔도 이득이 유지된다는 것을 보여 "특정 teacher와의 우연한 정합"이 아님을 입증한 실험 설계임.
- 다만 이 일반성 검증은 모두 같은 paradigm(cosine feature alignment) 안에서의 robustness 확인이고, 새로운 representation이나 learning objective를 제안한 것은 아님.

**Benchmark results**

- LIBERO 4-suite 평균: distilled 0.8B 97.9±0.5%, 동일 구조 undistilled student 95.3±0.7%(+2.6pt), 4회 평가(2 seed×2 GPU) 평균임. 4B 이상 SOTA VLA/WM(Qwen-RobotManip 99.2, S2-VLA 98.2, Being-H0.7 99.2)엔 여전히 뒤처짐.
- RoboCasa-GR1(24 env, GR1 humanoid): distilled 0.8B 50.5±2.3%, undistilled 48.2±2.1%(+2.3pt)로 QwenFAST·QwenPI·QwenOFT·Isaac-GR00T N1.5/1.6(4B급)는 넘어섰지만, 동일 구조 4B QwenGR00T(54.8±2.0)엔 4.3pt 못 미치고 ACE-Ego-0(72.8), PhysBrain(64.5) 같은 대규모 데이터 파이프라인 모델과는 격차가 큼.
- 실로봇 AgileX Nero fruit pick-place(30 trial): distilled 93.3%(28/30)로 4B π-style policy(93.3%)와 동률, undistilled control은 83.3%(25/30)임.
- 실로봇 egg task: distilled 60.0%(18/30) vs undistilled 46.7%(14/30) vs 4B 70.0%(21/30). TRIP-Bag bimanual handover: distilled 46.7%(14/30) vs undistilled 40.0%(12/30) vs 4B 53.3%(16/30)로 과제 난이도가 올라갈수록 세 정책 모두 성능이 떨어지되 순서는 유지됨.
- ablation: teacher 3종 모두 LIBERO에서 이득(Cosmos3-Nano +2.6pt, Fast-WAM +1.6pt, V-JEPA2-AC +1.2pt). alignment layer sweep(quarter schedule, single run)은 비단조적이며 final layer가 최고(49.8%)였지만 best와 second-best 차이가 스케줄 노이즈보다 작다고 저자 스스로 밝힘.

**Top-tier conference 적합성 — 50/100 · 추천 venue: CoRL**

world model teacher 3종·student 3종·real-robot 2 platform에 걸쳐 일관된 이득을 보인 넓은 ablation과, 4-run(2 seed×2 GPU) 평가로 LIBERO/RoboCasa 재현성 문제를 직접 다룬 점은 로봇러닝 venue에서 긍정적으로 볼 만함. 다만 핵심 기법이 REPA의 직접 이식이고 이득 폭이 2~3pt로 작으며, RoboCasa 관련 ablation은 single A100 run이라 분산 검증이 없고 실로봇 trial 수(30회, task 3개)도 작아 top-tier oral보다는 straight accept 수준으로 보임.

**추천 이유 & 누리랩 연구와의 연결점**

- world model 전체를 배포하지 않고 "world model이 아는 것"만 경량 정책에 이식하는 이 recipe는 test-time optimization 없이 grounding을 얻는 방법이라, 배포 제약이 큰 failure detection/recovery용 경량 정책 설계에 그대로 적용해볼 수 있음.
- teacher를 world model이 아니라 실패·이상 상태를 잘 구분하는 encoder로 바꾸면, failure diagnosis 표현을 VLA에 주입하는 동일한 feature-alignment 틀로 확장 가능함.
- alignment layer가 action head가 이미 소비하는 final layer에서 가장 싸고 잘 작동했다는 결과는, robot memory나 scene graph 표현을 VLA에 붙일 때 "어디에 정렬할지" 설계 참고점이 됨.

---

### 13. [58점] CausalWM: Causal Chain-of-Thought Reasoning for Embodied World Model

- **분야**: World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.23184](https://arxiv.org/abs/2609.23184) ([PDF](https://arxiv.org/pdf/2609.23184))
- **저자**: Ziming Xu, Shuang Liang, Ruobing Han, Ziqiao Xi, Mingxing Rao, Kun Zhou, Zijun Zhang, Yuchen Yan 외 5명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 70점

> 💡 미래 비디오를 바로 예측하지 않고 optical flow와 pointmap을 먼저 순서대로 생성한 뒤 RGB를 만드는 16B embodied world model임. 하나의 diffusion Transformer 안에서 causal attention mask로 단방향 정보 흐름을 강제하고 대규모 pretraining·CoT mid-training·RL post-training 3단계로 학습해 TriWorldBench 1위, PAI-Bench robot domain 최고 점수를 달성함.

**Core innovation & methodology**

- 하나의 diffusion Transformer가 RGB·optical flow·pointmap을 모두 in-context token으로 처리하고, causal attention mask로 뒤 단계에서 앞 단계로 정보가 새는 것을 차단함.
- 추론 시 optical flow → pointmap → RGB 순서로 한 변수씩 denoising하고, 완성된 변수를 다음 단계 context에 다시 넣는 variable-by-variable 생성 방식을 씀.
- 학습은 3단계임: (1) 31K시간 embodied video로 pixel-level pretraining, (2) SEA-RAFT flow·VGGT-Omega pointmap을 pseudo-label로 쓰는 causal CoT mid-training, (3) DiffusionNFT 기반 multi-objective RL post-training.
- RL post-training 보상은 physical consistency·temporal coherence·visual quality·task completion 네 항목으로 구성됨.
- in-context 인터페이스 덕분에 URDF 렌더링 같은 새 control 신호를 소량 fine-tuning만으로 CoT 단계에 끼워 넣을 수 있음(in-context feature guidance).

**Novelty vs. prior works**

- optical flow를 auxiliary 신호로 쓰는 접근은 기존에도 있었다고 논문 스스로 related work에서 인정함. 차이는 flow·pointmap·RGB를 causal order로 묶고 attention mask로 강제한 것과, 이를 16B 스케일 + RL post-training까지 하나의 파이프라인으로 완성한 것임.
- "causal"이라는 이름과 달리 실제 causal graph 추정이나 intervention/counterfactual 검증은 없음. motion→geometry→RGB 순서로 중간 표현을 먼저 생성하게 만든 structured CoT에 가깝고, formulation 자체의 신규성은 제한적임.
- 같은 아이디어(causal CoT for video generation)를 다룬 동시대 연구(Chain of event-centric causal thought [79], CausalMotion [102])를 본문에서 직접 인용함. 이 논문의 기여는 새 문제 정의보다 스케일(16B, 31K시간 데이터)과 학습 엔지니어링에 집중됨.

**Benchmark results**

- TriWorldBench(action-conditioned 3-view manipulation, 500 episode/50 task, 2026-09-11 리더보드): CWM TWB-Score 66.04로 1위. technical report가 공개된 8개 baseline 중 최고인 BWM(65.54) 대비 0.50점 차이임.
- 부록의 전체 36개 모델 리더보드에서는 dream4act가 65.66점으로 CWM과 0.38점 차이임. 본문 비교표는 technical report가 있는 모델만 골라 우위 폭을 크게 보이게 한 측면이 있음.
- PAI-Bench-G robot domain(174 prompt, Qwen3-VL-235B judge): CWM 89.9, Cosmos3-Super 89.7로 0.2점 차이임. 논문 스스로 "공식 리더보드 점수를 그대로 재현하지 못했다"고 밝혔고, CWM은 프롬프트를 pretraining caption 스타일로 재작성해 평가해 baseline과 조건이 완전히 같지 않음.
- few-step ablation에서 denoising step을 20/20/20→4/4/4로 줄이면 RO score가 86.54→88.86으로 오히려 오르고 생성 시간은 76.43초→24.25초(3.15배 단축)됨. 1/1/1까지 줄여도 88.84로 거의 유지됨.
- case study는 병 옮기기·병 꺼내기·서랍 닫기 3개 task에 대한 정성 비교(Wan2.2-A14B, LingBot-Video 대비)뿐이고 정량 성공률·real-robot 실행 평가는 없음. 모든 정량 지표가 video 품질 또는 VLM/VQA judge 기반임.

**Top-tier conference 적합성 — 52/100 · 추천 venue: CVPR**

world model에 causal CoT를 결합하고 16B 스케일·31K시간 데이터로 학습한 실험 규모는 CVPR/ICCV video generation 트랙에서 주목받을 만함. 다만 벤치마크 우위 폭이 0.2~0.5점으로 얇고 VLM judge 기반 벤치마크에 크게 의존하며, real-robot closed-loop 검증이 전혀 없어 reviewer가 marginal improvement·incremental engineering으로 볼 위험이 큼.

**추천 이유 & 누리랩 연구와의 연결점**

- 중간 예측 단계(optical flow·pointmap)를 실패 감지 신호로 재활용할 수 있어 failure detection/diagnosis·recovery 연구와 연결 가능함.
- in-context CoT 인터페이스는 test-time에 새 control 신호(목표 pose, 궤적)를 few-shot fine-tuning만으로 주입하는 구조라 test-time optimization/inference-time planning 연구에 참고할 만함.
- "causal"이라는 이름에도 실제 intervention/counterfactual 검증이 없다는 한계 자체가 우리 lab의 counterfactual reasoning 연구와 차별화 지점이 될 수 있음. 실제 causal intervention을 world model에 붙이는 후속 연구로 발전 가능함.

---

### 14. [58점] An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond

- **분야**: VLA · **robotics relevance**: 9/10
- **arXiv**: [2609.24170](https://arxiv.org/abs/2609.24170) ([PDF](https://arxiv.org/pdf/2609.24170))
- **저자**: Wenbo Zhang, Kaixuan Wang, Yutao Ouyang, Xiaoyu Huang, Liyang Li, Kailun Su, Weiyang Jin, Wenhao Chai 외 4명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: 24 pages
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 task-specific fine-tuning 없이 frozen LLM을 로봇 policy로 직접 쓰는 LLM-as-policy 설정을 RoboDojo 42개 task, 공개 policy 40개 대비 2,100 trial 규모로 평가함. GPT-6 Astra는 zero-shot으로 22.48% 평균 success rate를 기록해 모든 공개 policy를 앞섰지만 GPT-5.5·DeepSeek-Flash는 각각 0.88%·1.92%에 그쳐 결과가 특정 모델에 국한됨을 보임.

**Core innovation & methodology**

- LLM-as-policy를 두 조건으로 정의함 — control path에 학습된 policy가 없고, 이번 평가를 위한 task-specific fine-tuning 없이 weight를 고정함.
- LLM은 move_eef(엔드이펙터 목표 pose 지정)와 give_up 두 tool만 호출하며, pick/place 같은 motion primitive는 제공하지 않음.
- action conversion은 학습되지 않은 모듈로, 요청된 엔드이펙터 target을 inverse kinematics로 joint path로 바꿔 25Hz로 실행하고 도착 오차를 다음 observation에 그대로 반환함.
- GPT-6 Astra·GPT-5.5·DeepSeek-Flash 세 모델을 RoboDojo 공식 50-episode(DeepSeek-Flash는 10-episode) protocol로 42개 task 전체에서 평가하고, 40개 공개 pretrained policy와 같은 leaderboard 지표로 비교함.

**Novelty vs. prior works**

- 새로운 architecture·representation·학습 방법은 제안하지 않음 — 순수 평가 연구이며 기여는 실험 설계와 발견 자체에 있어 novelty는 제한적임.
- Kwon et al.(2024)의 zero-shot trajectory generator는 별도 detection/segmentation 모델에 의존했고 30-task 평가에 그쳤는데, 본 논문은 그런 보조 모델 없이 42-task 공개 leaderboard 전체와 직접 비교한 첫 사례라고 주장함.
- Anthropic의 Claude Plays Robotics(LIBERO-40, full-task success 0~5.5%)나 OpenAI/Robocurve의 GPT-6 Astra 자체 보고서는 소규모 custom task suite였던 반면, 이 논문은 공식 benchmark protocol과 공개 policy board를 그대로 사용해 비교 범위를 넓힌 점이 차별점임.

**Benchmark results**

- GPT-6 Astra 28.97 Score / 22.48% 평균 SR(2,100 trial)로 43개 entry 중 1위, 2위 DM0.5(24.90/19.34) 대비 SR +3.14pp임.
- GPT-5.5 1.13/0.88%, DeepSeek-Flash† 2.99/1.92%(10-episode)로 Astra와 최대 약 25배 SR 격차가 남.
- Astra는 Open(34.36/31.00)·Generalization(33.36/30.50) 축에서 강하지만 Precision(12.65/4.00)·Long-Horizon(21.45/8.25) 축과 Memory(43.04/38.67, DM0.5의 47.74/47.44보다 낮음) 축에서는 뒤처짐.
- one-shot demonstration ICL은 zero-shot 78/340=22.9% 대비 image+EEF demo 17.9%(-5.0pp), text demo 12.9%(-10.0pp)로 오히려 성능을 낮춤.
- RoboDojo-Real 공식 protocol은 unsafe action으로 장비가 손상돼 중단됐고, 남은 33개 diagnostic trial의 Score/SR은 6.97/3.03%로 공식 18-task baseline(OpenWAM-α 37.60/24.40%)에 크게 못 미침.

**Top-tier conference 적합성 — 52/100 · 추천 venue: CoRL**

42-task·2,100 trial·공개 policy 40개 비교라는 실험 규모와 protocol 준수는 top-tier venue 수준의 empirical rigor를 갖춤. 다만 새로운 method나 representation이 없는 순수 평가 논문이라 oral보다는 poster·findings track에 가깝고, real-robot 결과가 안전 문제로 중단돼 미완성인 점이 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- one-shot demonstration이 오히려 성능을 낮춘 결과는 test-time optimization 설계에서 in-context example 삽입을 그대로 신뢰하면 안 된다는 반례로 참고할 만함.
- perturbation 하에서 관찰된 within-episode correction 사례(좌우 반전, pose jitter 등)는 별도 recovery module 없이 LLM 자체가 관찰 결과로 재시도하는 baseline으로 failure detection·recovery 연구에 참고 가능함.
- Precision·bimanual coordination에서의 실패가 physical commonsense 부족으로 설명되는데, 이는 world model 기반 policy와 LLM-as-policy를 결합하는 hybrid 설계의 문제 정의 근거로 쓸 수 있음.

---

### 15. [50점] Prioritized Rollouts for Efficient World Model-based Vision-Language-Action Policy Optimization

- **분야**: VLA / World Model 기반 RL · **robotics relevance**: 9/10
- **arXiv**: [2609.22879](https://arxiv.org/abs/2609.22879) ([PDF](https://arxiv.org/pdf/2609.22879))
- **저자**: Yifei Sheng, Haoxiang Ren, Zhilong Zhang, Haonan Wang, Runjie Xu, Yihao Sun, Nan Tang, Zhichao Wu 외 3명
- **카테고리**: Machine Learning (cs.LG) · 신규 목록 게재: cs.LG
- **원문 검토**: PDF 전문 · 1차 스크리닝 65점

> 💡 World model으로 VLA 정책을 RL fine-tuning할 때 branched rollout을 어느 state에서 시작할지가 정책 개선에 큰 영향을 준다는 걸 보임. policy uncertainty가 높은 state(파지·배치처럼 정밀도가 필요한 구간)를 우선 선택하고 회복 불가능한 실패 tail은 제외하는 샘플링 레이어 U-GROW(Uncertainty-Guided Rollouts for policy Optimization with World models)로 같은 rollout 예산에서 성공률을 끌어올림.

**Core innovation & methodology**

- 문제 설정: 기존 MBRL 기반 VLA 학습(VLA-MBPO)은 branched rollout 시작 state를 offline dataset에서 균일 샘플링해 state별 정책 개선 잠재력 차이를 무시함.
- self-consistency uncertainty estimator(denoising step 수를 바꿔가며 생성한 action chunk들의 불일치도로 정의, 저자들의 이전 워크숍 논문에서 가져옴)로 state별 uncertainty를 계산함.
- failure-tail truncation: 실패 trajectory에서 uncertainty가 threshold를 처음 넘는 시점 이후는 회복 불가능한 구간으로 보고 rollout 후보에서 제외함.
- uncertainty-prioritized sampling: 남은 state 중 uncertainty 상위 ρ_pri 비율을 우선 샘플링하고, PPO critic 학습을 위한 state coverage 확보용 uniform 샘플링과 λ=0.5로 혼합해 rollout-start distribution만 교체함(RL objective·world model·rollout horizon은 VLA-MBPO와 동일).

**Novelty vs. prior works**

- 가장 가까운 prior work인 VLA-MBPO(같은 저자 그룹, ICML'26) 파이프라인을 그대로 두고 rollout-start distribution 하나만 바꾼 plug-in 레이어라 방법론적 변화 폭이 작음.
- uncertainty 신호 자체도 저자들의 별도 워크숍 논문(Ren et al., RSS'26 workshop)에서 제안된 self-consistency estimator를 재사용한 것이라, 이 논문의 새 기여는 어디서 rollout을 시작할지를 uncertainty로 우선순위화하고 실패 tail을 자르는 조합에 국한됨.
- 개념적으로는 TD-error 대신 policy uncertainty를 priority 신호로 쓰는 prioritized experience replay류 아이디어의 변형이며, 저자들도 이를 새 learning objective나 architecture가 아닌 sampling layer로 명시적으로 한정함. novelty는 제한적이나 policy-switching intervention으로 uncertainty와 개선 잠재력의 상관관계를 실증한 분석 자체는 실용적 가치가 있음.

**Benchmark results**

- RoboTwin 2.0 4개 task 평균 성공률: U-GROW 58.8% vs VLA-MBPO 54.3%(+4.5pp) vs πRL 44.8% vs IDQL 43.0% vs πbase 40.8%.
- LIBERO 4개 suite 평균: U-GROW 89.1% vs VLA-MBPO 87.7%(+1.4pp), task별로는 모두 U-GROW가 최고 성공률을 기록함.
- 실로봇 4개 task(Arx-X5 bimanual, task당 50 trial)에서도 VLA-MBPO 대비 학습 효율과 최종 성공률 모두 개선되었다고 서술되나 정확한 수치는 그래프로만 제시되어 본문 텍스트에서 확인 불가.
- clean-to-randomized generalization(RoboTwin 4 task): U-GROW 평균 26.0% vs VLA-MBPO 24.0%, task별로는 3개 task에서 우위, Move Can Pot은 동률(15.0%).
- ablation(Handover Block 단일 task): coverage(uniform) 컴포넌트 제거 시 성능 저하가 가장 크고 truncation·prioritization 제거도 각각 성능을 낮춤을 정성적으로 보였으나 구체적 수치는 본문에서 확인 불가(그래프만 제시).

**Top-tier conference 적합성 — 60/100 · 추천 venue: CoRL**

sim(RoboTwin 2.0, LIBERO) 4+4 task와 real-world 4 task, generalization·ablation까지 갖춘 비교적 탄탄한 실험 구성이라 robot learning venue에서 통과 가능성은 있음. 다만 VLA-MBPO 대비 rollout-start distribution만 바꾼 plug-in 모듈이라 conceptual leap이 크지 않고 개선폭도 RoboTwin +4.5pp, LIBERO +1.4pp로 크지 않아 oral/highlight급으로 보기는 어려움.

**추천 이유 & 누리랩 연구와의 연결점**

- failure-tail truncation은 실패 궤적에서 회복 불가능한 구간을 uncertainty로 식별하는 방식이라, 실로봇 failure detection·recovery 연구에서 언제부터 실패가 굳어지는지 판별하는 신호로 응용해볼 수 있음.
- policy uncertainty를 정책 개선 잠재력의 proxy로 쓰는 아이디어는 test-time optimization에서 어느 state·timestep에 추가 연산(re-planning, world model rollout)을 투입할지 결정하는 데 그대로 옮겨볼 만함.
- self-consistency uncertainty estimator(denoising step 수 변화에 대한 action chunk 민감도)는 world model 없이도 VLA policy 자체의 신뢰도 추정 도구로 쓸 수 있어, 별도 world model 학습 부담 없이 학생 연구에 먼저 붙여볼 수 있는 요소임.

---

## 오늘의 핵심 연구 트렌드 종합

- **World-Action Model(WAM) 설계 표준화 경쟁** — WAM 구조가 오늘 top 논문 네 편을 지배함. [AffordanceWAM](https://arxiv.org/abs/2609.22332)·[DexTacWAM](https://arxiv.org/abs/2609.24976)은 world state에 넣을 정보(affordance, tactile)를 다투고, [What Matters in Designing World Action Models](https://arxiv.org/abs/2609.24048)는 그 설계축을 통제 실험으로 정리함.
- **action 표현 자체의 취약성이 드러남** — [Robot World Models Are Not Invariant to How the Actions Are Written](https://arxiv.org/abs/2609.23252)은 world model이 absolute와 relative action encoding에 대해 전혀 다른 예측을 내놓음을 보였음. world model 학습·평가 파이프라인이 이 취약성 위에 서 있었다는 문제 제기임.
- **counterfactual·causal 진단이 evaluation의 새 축으로 등장함** — 리더보드 순위 대신 counterfactual edit로 정책의 실제 반응을 진단하는 [Beyond the Leaderboard](https://arxiv.org/abs/2609.22582)와, causal chain-of-thought로 world model reasoning을 강화하는 [CausalWM](https://arxiv.org/abs/2609.23184)이 같은 날 나옴.
- **world model이 학습 보조를 넘어 배포 시점 도구로 이동함** — 재학습 없이 base policy 위에서 world model로 plan을 고르는 [Latent Policy Steering](https://arxiv.org/abs/2609.22521)과 world model rollout 시작점을 우선순위화하는 [U-GROW](https://arxiv.org/abs/2609.22879)가 나옴. test-time optimization이 world model의 실질적 활용처로 자리잡는 중임.
- **human video → robot 전이가 가벼운 중간 표현으로 정교해짐** — [EgoWild2Dex](https://arxiv.org/abs/2609.23755)는 homography 기반 view alignment로, [AffordanceWAM](https://arxiv.org/abs/2609.22332)은 affordance heatmap으로 각각 액션 라벨 없는 인간 영상을 로봇 정책에 붙임. 두 방법 모두 3D reconstruction 없이 가벼운 중간 표현을 씀.

## 유망 연구 방향 및 프로젝트 제안

**Action encoding invariance를 world model 진단·설계 도구로 삼기**
- research question: 우리가 쓰는 world model이 action encoding 선택(absolute/relative, joint/end-effector)에 얼마나 민감한가. 그 민감도를 낮추는 학습 objective를 설계할 수 있는가.
- 접근·novelty: [Robot World Models Are Not Invariant](https://arxiv.org/abs/2609.23252)의 admissibility test와 disagreement penalty를 우리 world model에 적용해 민감도를 정량화하고, objective averaging을 학습 목표에 명시적으로 추가함
- 왜 지금·경쟁 prior works: 이 논문이 action channel을 invariance 감사 대상에서 아무도 넣지 않았다는 공백을 처음 지적함 — 우리 world model·failure detection 연구에 바로 쓸 진단 도구가 됨
- risk·target venue: 우리 아키텍처가 이미 invariant해 negative result로 끝날 위험 있음, CoRL/ICRA 대상

**Tactile/affordance 예측 오차를 failure detection 신호로 재활용**
- research question: world model이 예측한 미래 tactile 접촉·affordance와 실제 관측 사이의 불일치를 contact-rich task의 실시간 failure signal로 쓸 수 있는가
- 접근·novelty: [DexTacWAM](https://arxiv.org/abs/2609.24976)과 [AffordanceWAM](https://arxiv.org/abs/2609.22332)처럼 world model이 tactile·affordance를 직접 예측하게 하고, prediction-observation discrepancy를 failure detector로 전용함
- 왜 지금·경쟁 prior works: 두 논문 모두 world state 확장이 성능을 크게 끌어올렸지만 failure detection 활용은 다루지 않음. DexTacWAM은 success-only training이 한계라고 스스로 밝혀 이 공백을 인정함 — 랩의 failure detection·recovery 우선 주제와 직결
- risk·target venue: 단일 tactile sensor·단일 플랫폼 검증이라 일반화 확인 필요, CoRL 대상

**Counterfactual 진단 프레임워크를 manipulation VLA로 이식**
- research question: [Beyond the Leaderboard](https://arxiv.org/abs/2609.22582)의 counterfactual edit 진단을 autonomous driving이 아닌 manipulation VLA에 적용하면 무엇이 드러나는가
- 접근·novelty: 장면 내 방해물체·조명을 counterfactual 편집해 VLA가 실제로 반응하는지 측정함 — 원논문의 faithfulness/interference axis를 manipulation success rate로 재정의함
- 왜 지금·경쟁 prior works: 이 논문이 사전등록 전이 검증까지 방법론을 공개했고, VLA 평가가 여전히 벤치마크 숫자 위주라는 문제의식이 랩의 문제의식과 일치함
- risk·target venue: counterfactual edit 품질 검증(inpainting artifact) 비용이 큼, ICRA/RSS 대상

**Test-time world model steering을 진행 중인 test-time optimization 연구에 결합**
- research question: [Latent Policy Steering](https://arxiv.org/abs/2609.22521)의 test-time value function 기반 plan selection을 우리 test-time optimization 연구에 붙이면 어떤 이득이 있는가
- 접근·novelty: base VLA가 샘플한 여러 action chunk를 우리 world model latent space에서 distribution-shift penalty로 평가해 최고 plan을 재학습 없이 선택함
- 왜 지금·경쟁 prior works: 랩의 test-time optimization/inference-time planning 우선 주제와 정확히 일치하고, 저자들이 공개한 프레임워크가 base policy에 붙이기만 하면 되는 구조임
- risk·target venue: 원논문이 target embodiment 하나(Franka)만 검증해 우리 로봇에서 재현이 안 될 위험 있음, CoRL/RSS 대상

## 오늘 반드시 읽어야 할 논문

- [Robot World Models Are Not Invariant to How the Actions Are Written](https://arxiv.org/abs/2609.23252) — action encoding 취약성을 최초로 규명, 우리 world model 감사에 바로 쓸 진단 도구임
- [Grounded Action Model: 3D Grounding as a Foundation for Robotics](https://arxiv.org/abs/2609.23863) — 3D grounding을 backbone으로 쓰는 새 robot foundation model paradigm, real-robot OOD 검증이 탄탄함
- [The Right Future for Action: Learning Action-Relevant Predictive States in World Action Models](https://arxiv.org/abs/2609.23369) — predictability와 action readability의 어긋남을 진단해 WAM을 재설계, LIBERO-Plus 성공률을 +39.2%p 끌어올림
- [DexTacWAM: A Visuo-Tactile World-Action Model for Dexterous Manipulation](https://arxiv.org/abs/2609.24976) — tactile을 world state 예측 대상으로 삼아 contact-rich task 6개 평균 점수를 70.6점(최강 baseline 38.0점)까지 끌어올림
- [Beyond the Leaderboard: Counterfactual Diagnosis of End-to-End and VLA Driving Policies](https://arxiv.org/abs/2609.22582) — counterfactual 진단 프레임워크로 리더보드 지표의 허점을 드러냄, failure detection으로 확장 가능함
- [Latent Policy Steering](https://arxiv.org/abs/2609.22521) — 재학습 없이 world model로 test-time에 policy를 조정, 랩 test-time optimization 주제와 직결됨
- [AffordanceWAM: Affordance-Aware Joint World-Action Modeling for Robot Manipulation](https://arxiv.org/abs/2609.22332) — affordance를 매개로 인간 영상을 로봇 정책에 전이, sign-reversal ablation이 설득력 있음
- [EgoWild2Dex: Learning Dexterous Robotic Manipulation from In-the-Wild Human Experience](https://arxiv.org/abs/2609.23755) — 대규모 egocentric human 데이터셋과 경량 view alignment로 로봇 데모 1시간 미만에 성공률 96.7% 달성함

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (931편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2609.22521'>Latent Policy Steering: An Efficient and Flexible Framework for Cross-Embodiment Transfer</a></td><td>72</td><td>9</td><td>World Model</td><td>optical flow 기반 world model을 embodiment-agnostic하게 사전학습한 뒤 latent space 탐색으로 정책을 steering하는 test-time 최적화 구조라 새 problem formulation에 가까움, 실로봇서 50개 데모만으로 큰 성능 향상 확인함</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2609.23184'>CausalWM: Causal Chain-of-Thought Reasoning for Embodied World Model</a></td><td>70</td><td>9</td><td>World Model</td><td>미래 비디오 예측 전에 명시적 causal chain-of-thought로 물리적 인과 의존성을 포착하는 16B embodied world model이라 world model과 causal reasoning 우선 주제에 정확히 부합함</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2609.22582'>Beyond the Leaderboard: Counterfactual Diagnosis of End-to-End and VLA Driving Policies Under Domain Shift</a></td><td>68</td><td>8</td><td>VLA</td><td>E2E·VLA 주행 정책을 리더보드 순위가 아니라 counterfactual 편집으로 진단하는 새 방법론이라 counterfactual reasoning과 VLA 우선 주제에 정확히 부합함</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2609.22879'>Prioritized Rollouts for Efficient World Model-based Vision-Language-Action Policy Optimization</a></td><td>65</td><td>9</td><td>VLA</td><td>world model 기반 VLA policy RL에서 정책 불확실성이 높은 state에 rollout을 집중시키는 U-GROW 제안, 시뮬·실로봇 조작 실험 모두 포함해 test-time optimization과 world model 우선주제에 정확히 부합함</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2609.23252'>Robot World Models Are Not Invariant to How the Actions Are Written</a></td><td>65</td><td>9</td><td>World Model</td><td>절대좌표 vs 상대좌표 action parameterization만 바꿔도 동일 world model의 retrieval·goal selection이 붕괴함을 정량적으로 보이고 objective averaging이라는 수리적 해법까지 제시한 분석이 랩의 world model 연구에 바로 활용 가능함</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2609.23863'>Grounded Action Model: 3D Grounding as a Foundation for Robotics</a></td><td>65</td><td>9</td><td>VLA/3D Vision</td><td>언어·포인트·박스 프롬프트를 공유된 object-centric 3D 표현으로 통일해 조작 정책의 기하학적 접지를 명시화한 Grounded Action Model로 RoboTwin·LIBERO-PRO·실로봇 전반에서 baseline을 능가해 robot foundation model에 새로운 축을 제시함</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2609.23369'>The Right Future for Action: Learning Action-Relevant Predictive States in World Action Models</a></td><td>65</td><td>8</td><td>World Model</td><td>world action model의 내부 표현이 제어에 필요한 정보를 실제로 담는지 진단하고 action-relevant한 예측 표현을 새로 제안해 world model-action 연결에 본질적 기여를 함</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2609.22332'>AffordanceWAM: Affordance-Aware Joint World-Action Modeling for Robot Manipulation</a></td><td>62</td><td>10</td><td>VLA</td><td>affordance(스칼라+히트맵)를 world model과 action model이 공유하는 인터페이스로 삼아 사람 영상에서 로봇으로 전이, 비디오diffusion transformer 위에서 world·action을 masked joint attention으로 결합하고 실로봇·RoboCasa·CALVIN에서 일관된 개선을 보여 world model·object-centric representation·human-to-robot transfer 우선주제에 강하게 부합함</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2609.24170'>An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond</a></td><td>62</td><td>9</td><td>VLA</td><td>task-specific finetuning 없이 LLM을 로봇 조작 정책으로 직접 사용하는 LLM-as-policy 설정을 RoboDojo 42개 태스크에서 공개 정책들과 비교 평가한 실험 연구임</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2609.22888'>Stable and Efficient Real-World Online VLA Post-Training via Asynchronous Replay-Anchored Policy Improvement</a></td><td>62</td><td>9</td><td>VLA/RL</td><td>replay 기반 critic·actor로 rollout과 학습을 비동기 병행하는 online VLA post-training 구조로 실로봇 1~2시간 온라인 학습만으로 멀티태스크 성공률을 52%에서 88%로 끌어올려 test-time/online RL 우선주제에 강하게 부합함</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2609.23755'>EgoWild2Dex: Learning Dexterous Robotic Manipulation from In-the-Wild Human Experience</a></td><td>62</td><td>9</td><td>Manipulation/Dexterous</td><td>538.9시간 규모의 실환경 egocentric 데이터를 미분가능 기하 변환기로 로봇 관측·행동에 정렬시켜 덱스터러스 양팔조작을 96.7% 성공률로 전이한 대규모 human-to-robot 파이프라인임</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2609.24048'>What Matters in Designing World Action Models: An Empirical Study</a></td><td>62</td><td>9</td><td>World Model</td><td>인과구조·latent space·학습목표라는 world action model 설계축을 통제된 실험으로 분리해 3개 벤치마크와 실제 DROID 데이터로 체계적으로 비교한 실증연구로 향후 WAM 설계에 직접 참고할 근거를 제공함</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2609.24682'>Think Like a World Model, Act Like a VLA: Distilling World-Model Representations into Compact Robot Policies</a></td><td>62</td><td>9</td><td>World Model/VLA</td><td>world model의 미래생성 자체가 아니라 내부 특징만 feature-alignment loss로 VLA에 전수해 배포 시엔 동일한 VLA를 그대로 32ms로 실행하는 설계로 LIBERO·RoboCasa·실로봇 전반에서 이득을 재현해 world model 표현을 경량 정책에 이식하는 간결하고 일반화 가능한 아이디어임</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2609.24976'>DexTacWAM: A Visuo-Tactile World-Action Model for Dexterous Manipulation</a></td><td>62</td><td>9</td><td>World Model/Tactile/Manipulation</td><td>각 손끝 촉각을 독립 인코딩해 video diffusion world model에 주입하는 DexTacWAM으로 접촉역학을 world state의 일부로 모델링해야 함을 ablation으로 입증하고 소량 데이터로 vision-to-touch 지속학습까지 보여 tactile world model 우선주제와 정확히 맞음</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2609.22351'>Hierarchical Aggregation of Semantic Uncertainty in 3D Scene Graphs</a></td><td>62</td><td>8</td><td>3D Vision</td><td>open-vocabulary 3D scene graph의 각 노드 의미 불확실성을 추가 학습 없이 detector confidence와 임베딩만으로 추정하는 새 프레임워크라 scene graph 우선 주제와 직결됨</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2609.23478'>Algebraic Consistency Alone Does Not Certify Temporal Structure in Latent Action Models</a></td><td>62</td><td>8</td><td>World Model</td><td>latent action model이 additive·antisymmetric 대수 항등식을 만족해도 실제 시간 구조를 포착했다고 인증할 수 없음을 보여 action-free video 사전학습의 흔한 평가 지표가 틀렸음을 지적함</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2609.23753'>OnlineWM: Causality-Aware Active Online Learning for Effective World Modeling</a></td><td>62</td><td>8</td><td>World Model</td><td>오프라인 데이터의 분포 불일치와 long-tail 동역학 문제를 causality-aware active online learning으로 해결하는 world model 학습 파이프라인이라 world model·능동 학습 우선 주제에 부합함</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2609.24313'>NeuIDO: Neural Intrinsic Dynamics Operator for Physics-Informed 4D World Models</a></td><td>62</td><td>8</td><td>World Model</td><td>수작업 동역학 가정 대신 통합된 신경 연산자로 물리 동역학 자체를 내재화하는 물리 정보 4D world model이라 embodied intelligence를 겨냥한 본질적 formulation 기여임</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2609.22175'>Contrastive World Models</a></td><td>62</td><td>8</td><td>World Model</td><td>픽셀 재구성 대신 상태-행동 시퀀스와 지역 패치 간 상호정보를 최대화하는 Deep InfoMax 방식으로 world model을 학습해 시각적으로 복잡한 환경에서의 distraction 문제를 다루는 Dreamer 계열 개선임</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2609.23144'>Probabilistic Scene Graphs: Hierarchical Representation and Real-time System</a></td><td>62</td><td>8</td><td>Scene Graph/3D Vision</td><td>그래프 구조와 연속 상태 모두에 불확실성을 유지하는 확률적 3D scene graph를 제안하고 계층적 Gaussian으로 구현해 6개 데이터셋에서 실시간 state-of-the-art 정확도를 보인 견고한 표현학습 기여임</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2609.22816'>FIRM-WM: State-factorized factual-interventional recurrent modeling for reward-free visual planning</a></td><td>62</td><td>7</td><td>World Model</td><td>factual-goal state와 dynamic fiber를 분리한 state-factorized world model로 reward-free visual planning 개선, OGBench-Cube 등에서 baseline 대비 우위 보이고 counterfactual branch로 offline mismatch 해결함</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2609.24749'>D-JEPA: A Decision-Aligned Latent World Model</a></td><td>60</td><td>9</td><td>World Model</td><td>예측 정확도가 좋아도 후보 중 최종 실행성공과 무관할 수 있다는 decision-local prediction gap을 정의하고 permutation-equivariant 연산자로 목표상대 특징과 순서 evidence를 함께 학습하는 D-JEPA로 PushT·RoboTwin·실로봇 전반에서 action selection을 개선함</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2609.22293'>Validating, Not Sampling: Region-Level Robustness of Vision-Language and Vision-Language-Action Models</a></td><td>60</td><td>8</td><td>VLA</td><td>GR00T·OpenVLA·pi 등 VLA와 VLM의 연속 영역 강건성을 샘플링이 아니라 검증 방식으로 처음 평가한 벤치마크 논문임</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2609.23048'>Anatomy of a Closed-Loop Collapse: A Causal Case Study of a Compressed VLA Policy</a></td><td>60</td><td>8</td><td>VLA/Failure Analysis</td><td>오프라인 검증을 통과하고도 closed-loop에서 붕괴하는 압축 VLA를 인과적으로 해부해 z축 잔차 결함을 특정하고 표준 치료법들이 실패함을 보인 정밀한 사례연구로 압축 정책 배포 리스크에 대한 통찰이 큼</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2609.24308'>HappyWorld-Bench</a></td><td>60</td><td>7</td><td>World Model</td><td>에이전트가 탐색·상호작용·수정할 때 생성된 world가 얼마나 일관되고 반응하는지를 6개 능력 차원으로 평가하는 종합 world model 벤치마크임</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2609.24984'>WorldCrafter: Consistent Video World Model with Implicit 3D-aware Memory</a></td><td>60</td><td>6</td><td>World Model</td><td>카메라 시점에 따라 과거 관측을 압축하는 implicit 3D-aware memory로 장기·다시점 일관성을 확보한 video world model이라 world model과 robot memory 개념이 결합됨</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2609.22591'>REBOOT: From Failure to Recovery - A Dataset and Benchmark for Precision Assembly</a></td><td>58</td><td>9</td><td>Manipulation/Failure Benchmark</td><td>실패를 1급 신호로 다루는 정밀조립 벤치마크로 2160개 데모에 phase별 실패-회복 라벨을 붙여 랩이 강조하는 failure recovery 연구에 바로 쓸 수 있는 데이터 자산임</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2609.22684'>StateMem: Single-State Residual Memory with Adaptive Inference for Vision-Language-Action Policies</a></td><td>58</td><td>9</td><td>VLA/Robot Memory</td><td>단일 residual memory token으로 VLA에 이력 정보를 저장하고 캐시 재사용률을 적응 조절하는 robot memory 방법으로 LIBERO-Mem 97.6%, 실로봇 +21%p를 보여 랩 우선주제에 정확히 부합함</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2609.22895'>H-VLA: Hierarchical Vision-Language-Action Model with Key-Action Reasoning and Motion Planning in a Unified Action Space</a></td><td>58</td><td>9</td><td>VLA</td><td>고수준 key-action 추론과 저수준 motion generation을 분리하고 카메라 중심 통합 action space로 embodiment 차이를 흡수한 H-VLA로 SimplerEnv와 실로봇 OOD에서 큰 폭 개선을 보임</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2609.22966'>Transferring the Intelligence of VLMs to Robotic Control</a></td><td>58</td><td>9</td><td>VLA/Embodied AI</td><td>VLM을 이산 동작 인터페이스로 감싸 로봇 특화 학습 없이 closed-loop 제어시키고 한 번의 in-context 시연만으로 baseline을 넘는 RoboDawn으로 digital-to-real 지능 전이라는 프레이밍이 새로움</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2609.23100'>Splat-CBF: Safe Next-Best-View Control in 3D Gaussian-Splat Maps</a></td><td>58</td><td>9</td><td>Active Perception/3D Vision</td><td>3D Gaussian splat 맵의 불확실성을 위험인지 CBF로 바꿔 안전제약과 next-best-view를 하나의 QP로 통합한 Splat-CBF로 active perception과 3DGS 우선주제를 동시에 다룸</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2609.23504'>Imagine then Verify: Affordance-Targeted Active Perception for Task-Oriented Grasping in Cluttered Scenes</a></td><td>58</td><td>9</td><td>Active Perception/Manipulation</td><td>물체 전체를 스캔하는 대신 가려진 어포던스 영역만 가상 형상으로 가정하고 검증하는 viewpoint planning인 ATAP로 NBV 스텝을 57% 이상 줄이면서 성공률을 높여 active perception 우선주제와 정확히 맞음</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2609.23578'>AR-WAM: A Visual-Conditioned Agent-Ready World Action Model for Robotic Manipulation</a></td><td>58</td><td>9</td><td>World Model/VLA</td><td>언어 대신 바운딩박스와 학습된 조작 토큰으로 조건화한 agent-ready world action model로 0.5B 경량 모델임에도 메모리·장기과업에서 강한 baseline을 능가하고 지연시간도 가장 낮아 agentic 제어 인터페이스로서 novelty가 큼</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2609.24093'>Dexterous Robot Manipulation from Human Demonstrations via Contact-Anchored Retargeting and Residual Policy Learning</a></td><td>58</td><td>9</td><td>Manipulation/Dexterous</td><td>인간 시연의 접촉 구조만 형태와 독립적으로 전이시키고 하나의 residual RL 정책으로 물리적 타당성을 복원하는 3단계 파이프라인으로 실로봇 학습 데이터 없이 성공률을 7.3%에서 59.3%로 끌어올린 강한 human-to-robot 전이 기여임</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2609.24271'>ME-Brain-1.0: Memory, Cognition and Action for Evolving Embodied Intelligence</a></td><td>58</td><td>9</td><td>Embodied AI/Robot Memory</td><td>행동-경험획득-경험진화-향상실행의 폐루프로 배포 후에도 재학습 없이 진화하는 ME-Brain으로 계층적 메모리와 이벤트 기반 world prediction을 결합해 여러 벤치마크에서 baseline을 앞섬</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2609.24411'>Zeva-Ego: Egocentric Mid-Training with In-Context Causal Learning for Robot Manipulation</a></td><td>58</td><td>9</td><td>Manipulation/Causal Learning</td><td>egocentric 영상으로 action-centric 사전지식을 mid-training하고 배포 시엔 파라미터 갱신 없이 action-effect 피드백으로 in-context 적응하는 ICCL로 4회 시도만에 성공률을 58%에서 89%로 올려 test-time 적응과 causal 학습을 결합함</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2609.24525'>Bridge3D: Enabling Vision-Language-Action Models to See and Act in 3D</a></td><td>58</td><td>9</td><td>VLA/3D Vision</td><td>3D 기초모델 특징을 시각토큰에 암묵적으로 섞고 명시적 3D semantic field로 action denoising을 조건화하는 이중 전략 Bridge3D로 2D 중심 VLA에 명시적 기하 안내를 더해 RoboTwin과 실로봇 모두에서 큰 폭 향상을 냄</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2609.24745'>Beyond Visual Quality: A Study of Test-Time Planning with World Action Models</a></td><td>58</td><td>9</td><td>World Model/Test-Time Planning</td><td>world action model이 예측한 여러 미래 중 실제로 좋은 행동을 고르는 selection이 시각품질·물리일관성 점수로는 잘 안 된다는 사실을 oracle 상한(79.2%)과 비교해 실증하고 그 원인을 반사실 분기로 분석한 test-time planning 연구로 랩의 test-time optimization 관심사와 정확히 맞음</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2609.24868'>DualWAM: Dual-System World Action Models for Asynchronous Global Planning and Local Refinement</a></td><td>58</td><td>9</td><td>World Model/VLA</td><td>넓은 지평의 world-action 생성을 담당하는 System2와 손목관측만으로 저노이즈 구간을 빠르게 정제하는 System1을 같은 denoising 궤적 위에서 비동기 결합한 DualWAM으로 world model의 반응성 병목을 구조적으로 해결하고 16.6배 임계경로 가속을 보임</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2609.23352'>BiView-Touch: Learning Bimanual Tactile Representations by Cross-Hand Completion</a></td><td>58</td><td>8</td><td>Manipulation</td><td>양손의 촉각 관측을 서로의 마스킹된 부분을 완성하도록 학습하는 self-supervised 방식으로 tactile perception과 양손 조작 우선 주제에 부합함</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2609.24452'>Do LiDAR Language Models Really Understand Spatio-temporal Relationships?</a></td><td>58</td><td>8</td><td>Embodied AI</td><td>4D LiDAR language model이 실제로는 항상 같은 답을 고르는 것과 비슷한 수준이라는 것을 보여 spatio-temporal reasoning 능력을 geometry-referenced 벤치마크로 비판적으로 검증한 연구임</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2609.23118'>Verti-WM: A Physics-Aided Exteroceptive World Model for Off-Road Reinforcement Learning</a></td><td>58</td><td>8</td><td>World Model/Navigation</td><td>고정 지형 transformer와 신경-기호 terramechanics 모델을 결합한 물리보조 world model로 오프로드 RL을 시뮬레이터 없이 학습시키고 실세계 데이터로도 검증한 하이브리드 접근임</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2609.24996'>Learning Beyond What Humans Can Demonstrate</a></td><td>58</td><td>8</td><td>Manipulation/IL</td><td>사람이 시연 자체를 만들기 어려운 infeasible-demonstration 영역을 정의하고 LLM이 실패양식을 추론해 수집·배포 단계에서 실행 가능한 guardrail로 변환하는 CoRL 논문 GLIDE로 데이터수집 성공률을 0~10%에서 70~90%로 끌어올린 새로운 문제 정식화임</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2609.23881'>MotionJEPA: Preventing Temporal Feature Collapse by Capturing Visual Changes in Latent Space</a></td><td>58</td><td>7</td><td>World Model</td><td>JEPA 학습이 느린 특징에 치우쳐 표현이 붕괴하는 문제를 action label 없이 이미지 차분 정규화로 방지하는 방법이라 latent world model 표현학습에 본질적으로 기여함</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2609.24981'>GAE: Learning a Geometry-Native Latent Space for 3D-Consistent World Generation</a></td><td>58</td><td>6</td><td>World Model</td><td>인식과 생성이 공유하는 geometry-native latent space를 제안해 3D 일관성 있는 world generation을 표현 수준에서 해결한 연구라 world model에 본질적인 기여를 함</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2609.22641'>ConsistWorld: Evidence Routing for Consistent Multi-Agent World Models</a></td><td>58</td><td>5</td><td>World Model</td><td>단일 이미지에서 여러 에이전트의 카메라 제어 비디오 스트림을 일관되게 생성하는 evidence routing 방식의 multi-agent world model이라 새로운 formulation을 제시함</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2609.23566'>G6D: Geometric Learning-Free RGB-D 6D Pose Solver for Robotic Manipulation</a></td><td>55</td><td>9</td><td>Manipulation</td><td>대규모 사전학습 모델 없이 기하학적으로 6D pose를 푸는 학습-프리 솔버라 로봇 조작 배포 제약을 직접 겨냥한 해석 가능한 방법임</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2609.22274'>CHOREO: Every Humanoid Skill as a Trajectory</a></td><td>55</td><td>9</td><td>Manipulation</td><td>이질적 휴머노이드 스킬을 SkillMotion이라는 통일된 궤적 표현으로 변환해 재학습 없이 조합하는 프레임워크, skill chaining 우선주제에 부합하고 2950개 스킬·130개 태스크에서 95.4% 성공률 보이나 시뮬레이션(MuJoCo)에 국한됨</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2609.22299'>When Does Test-Time Physical Diagnosis Pay? A Frozen Policy Buys Evidence It Never Reads</a></td><td>55</td><td>9</td><td>Embodied AI</td><td>test-time physical diagnosis가 실제로 행동을 바꾸려면 여섯 조건이 모두 성립해야 함을 보이고, frozen decoder가 evidence를 수집만 하고 쓰지 않는 지점을 정확히 짚어냄, failure detection·test-time optimization 우선주제에 정확히 부합함</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2609.22538'>FRAMES: Failure Recovery And Monitoring of Embodied Skills for Humanoid Loco-Manipulation</a></td><td>55</td><td>9</td><td>Failure Detection/Recovery</td><td>인간형 로봇 loco-manipulation에서 LLM planner-VLM monitor-recovery agent를 계층화한 failure-aware 프레임워크로 랩 핵심 주제와 직결되지만 IROS 워크숍 poster이고 monitor 모듈만 검증돼 recovery loop 전체 evidence는 부족함</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2609.22854'>SmoLSTM: A Compact Vision-Language-Action Model with Recurrent Memory that Persists</a></td><td>55</td><td>9</td><td>VLA/Robot Memory</td><td>관측-행동 토큰을 하나의 causal stream에 넣어 에피소드 내내 리셋 없는 recurrent state로 유지하는 경량 VLA로 LIBERO-Mem에서 메모리 기반 baseline들을 앞서 robot memory 우선주제에 부합함</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2609.23614'>CompVLA: A Variable Compliance Vision-Language-Action Model for Contact-rich Manipulation</a></td><td>55</td><td>9</td><td>VLA/Manipulation</td><td>RGB-언어로부터 motion과 강성행렬을 동시에 예측하는 Compliance Expert를 VLA에 추가한 CompVLA로 접촉이 많은 과업에서 순수 kinematic VLA를 능가하는 새로운 action space 설계임</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2609.23888'>HapticWAM: Distilling Imagined Touch into a World-Action Model without Inference-Time Tactile Sensing</a></td><td>55</td><td>9</td><td>World Model/Tactile</td><td>촉각 관측을 포함해 학습한 teacher world model을 촉각 입력 없는 student로 증류해 배포 시 손끝 센서 없이도 접촉 미래를 상상하게 하는 HapticWAM으로 tactile world model 우선주제에 부합함</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2609.23968'>Opt2VLA: Force-Aware Vision-Language-Action for Contact-Rich Humanoid Whole-Body Manipulation</a></td><td>55</td><td>9</td><td>VLA/Manipulation</td><td>VLA-제어 인터페이스에 연속 접촉력 명령을 명시적으로 도입해 기하 목표와 힘 목표를 동시 예측하는 Opt2VLA로 접촉 후 시각이 불안정한 상황에서도 힘 조절이 가능함을 실로봇으로 확인함</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2609.24033'>Imagine-RL: Residual-Confidence-Guided Cross-Attention for World-Model-Augmented VLA Reinforcement Learning</a></td><td>55</td><td>9</td><td>World Model/RL/VLA</td><td>각 후보 action chunk에 대해 frozen visual-torque world model이 미래를 상상하고 예측 잔차로 신뢰도를 매겨 critic을 개선하는 Imagine-RL로 100개 RL 궤적만으로 VLA post-training 성능을 크게 끌어올림</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2609.24118'>CARE: Experience-Guided Atomic Corrective Execution for Vision-Language-Action Policies</a></td><td>55</td><td>9</td><td>VLA/Failure Recovery</td><td>실패 rollout에서 단계별 deviation 분포를 학습해 교정 시연을 합성하는 CARE로 새 FSR-Bench에서 시뮬레이션·실로봇 모두 14~16%p 성공률 향상을 보여 failure recovery 우선주제와 잘 맞음</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2609.24124'>ActiveArena: Benchmarking and Understanding Active Perception in Robotic Manipulation</a></td><td>55</td><td>9</td><td>Active Perception/Manipulation</td><td>시점 제어가 가능한 대규모 시뮬레이터와 메모리 주석이 포함된 35개 과업 벤치마크, 13종 VLA 구성으로 active perception 연구를 위한 표준 테스트베드를 제공하는 체계적 기여임</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2609.24350'>LIBERO-VPro: Benchmarking Closed-Loop Visual Robustness of Robotic Foundation Models</a></td><td>55</td><td>9</td><td>VLA/Benchmark</td><td>시각 증거 저하·카메라 지연·소스 불일치·태스크 관련 장면변화 네 축으로 VLA와 world action model의 closed-loop 강건성을 19만 에피소드와 실로봇으로 대규모 진단한 벤치마크로 표면 성능 뒤에 숨은 취약점을 드러냄</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2609.23673'>Which Terrain Is Better? Preference Learning with VLM Prototypes for Off-Road Traversability Ranking</a></td><td>55</td><td>8</td><td>Navigation</td><td>오프로드 주행 가능성을 절대 점수가 아니라 VLM 프로토타입 기반 선호 순위로 재정의한 접근이라 로봇 내비게이션에 새로운 formulation을 제공함</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2609.24526'>ME-VLM:A Unified VLM for Embodied Cognition and Agent Coordination</a></td><td>55</td><td>8</td><td>Embodied AI</td><td>물리 지각·시공간 추론·계획·상호작용·결과 평가를 디지털·물리 환경 모두에서 통합한 embodied VLM이라 embodied cognition 우선 주제에 직접 부합함</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2609.22108'>Correcting Learning-based Perception for Safety</a></td><td>55</td><td>8</td><td>Navigation</td><td>perception contract의 preimage로 ML 상태추정의 불확실성을 오프라인에서 특성화하고 런타임에 risk heuristic으로 보정하는 방법이라 자율 시스템의 인식 안전성·실패 인지에 본질적으로 기여함</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2609.22730'>BEACON: Belief-Enabled Adaptive CONtrol for Imitation Learning under Uncertainty</a></td><td>55</td><td>8</td><td>IL/Partial Observability</td><td>raw 관측 이력 대신 베이지안 belief로 diffusion policy를 조건화해 state aliasing 문제를 해결하는 구조로 탐색-실행 행동을 암묵적으로 조절하는 점이 새롭지만 도메인 2개로 검증이 좁음</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2609.22798'>Expert-Play Contouring Control: Faster-than-Demonstration Planning from Slow Expert and Fast Play</a></td><td>55</td><td>8</td><td>Manipulation/World Model</td><td>느린 전문가 시연으로 진행도 contour를 학습하고 빠른 play 데이터로 world model을 학습해 시연보다 빠른 실행을 계획하는 조합이 새롭고 접촉 민감 과업에서 2배 처리량 향상을 보임</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2609.22858'>PileBelief: Persistent Physical State for Interaction-Driven World Modeling</a></td><td>55</td><td>8</td><td>World Model/Manipulation</td><td>굴착처럼 지형을 계속 바꾸는 태스크에서 표면 아래 상태까지 유지하는 persistent world model로 5-step 예측오차와 action selection regret을 크게 줄여 world model 표현 자체에 기여함</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2609.23269'>Latent Telepathy: Multi-Robot Communication with Self-Supervised Perceptual Latents</a></td><td>55</td><td>8</td><td>Multi-Robot/Representation Learning</td><td>자기지도 joint-embedding 인코더의 고정 latent를 그대로 방송해 팀원이 과업 보상만으로 해석하게 하는 Latent Telepathy 아이디어가 새롭고 raw 이미지보다 압축 latent가 더 신뢰도 높은 신호임을 실로봇으로 확인함</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2609.23305'>Shared Execution-Clock Drifting Policy for Dynamic Precision Manipulation</a></td><td>55</td><td>8</td><td>Manipulation</td><td>one-step policy에 진행도-인덱스 action curve와 공유 monotone clock을 명시적으로 예측시켜 실행 리듬을 학습하는 SECD로 요격·마감시한 과업에서 baseline을 능가함</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2609.23841'>Structured World-State Reasoning for Agentic Robotic Search</a></td><td>55</td><td>8</td><td>Navigation/Embodied Spatial Reasoning</td><td>지리 사전지식으로 초기화된 지속 그래프 위에서 경쟁 가설을 유지하는 Reasoner와 Examiner-Judge 구조를 결합한 WORLDS로 CityNav에서 최고 성능을 내고 실제 쿼드로터로도 검증함</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2609.23944'>Topology-Informed Visual Prompting For Vision Language Action Policies</a></td><td>55</td><td>8</td><td>VLA/Manipulation</td><td>복잡한 장애물 기하를 Gauss-Linking-Integral 위상 서명으로 표현해 시뮬레이션 플래너로 증강 데이터를 만들고 VLM이 이를 visual prompt로 렌더링해 VLA를 유도하는 방식으로 실로봇에서 40%p 향상을 보인 새로운 표현 기여임</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2609.24385'>Tactile-JEPA: Topology-Aware Self-Supervised Representation Learning for Distributed Tactile Sensors</a></td><td>55</td><td>8</td><td>Tactile/Representation Learning</td><td>센서 배치 그래프를 이용해 masked 요소를 예측하는 JEPA 스타일 자기지도학습으로 분산형 촉각 인코더를 사전학습시킨 Tactile-JEPA로 힘추정·자세추정 오차를 두 자릿수 퍼센트 줄임</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2609.24660'>Touch2Robot: Robot Touch in the Human Demonstration Loop</a></td><td>55</td><td>8</td><td>Manipulation/Tactile/Data Collection</td><td>사람이 시연하는 동안 목표 로봇 손이 실제로 어떻게 접촉할지를 시뮬레이션으로 보여줘 시연을 유도하는 Touch2Robot으로 재현 성공률을 37.9%에서 72.1%로 올리면서 수집 시간도 크게 줄인 새로운 데이터 수집 루프임</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2609.24864'>SE(3) Neural Potential Fields for 6-DoF Trajectory Planning Directly from Images Without Explicit 3D Reconstruction</a></td><td>55</td><td>8</td><td>Manipulation/Planning</td><td>명시적 3D 재구성 없이 이미지로부터 직접 학습한 SE(3) potential field가 navigation function 기반 geodesic 감독으로 기존 인공potential field의 고전적 결함(국소최소)을 해소한 방법으로 실로봇 UR10 grasp 성공률을 90%까지 끌어올림</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2609.24626'>Relationally Grounded Latent World Models for Autonomous Driving</a></td><td>55</td><td>7</td><td>World Model</td><td>nuScenes 3D 주석으로 만든 actor-centric traffic scene graph를 latent world model의 의미론적 supervision으로 활용해 world model과 scene graph 우선 주제를 결합함</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2609.22762'>DriveReferee: Geometric Safety Verdicts Need Not Be Learned for Driving World-Action Models</a></td><td>55</td><td>6</td><td>World Model</td><td>주행 world-action model의 궤적을 센서 학습 없이 기하학적 규칙으로 검증하는 방식이라 world model의 closed-loop 검증에 새로운 원리를 제공함</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2609.22788'>Human-Level Accuracy, Non-Human Strategies: Revealing Model-Human Divergence in Video Physical Reasoning</a></td><td>55</td><td>5</td><td>World Model</td><td>비디오 foundation model이 물리 추론에서 사람과 같은 forward simulation을 하는지 통계적 지름길을 쓰는지를 분포 기반으로 구분한 평가 프레임워크라 world model 평가에 새 관점을 제공함</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2609.23658'>Why Do Video Diffusion Models Violate Physics? Unveiling the Flaws in Attention Mechanisms</a></td><td>55</td><td>5</td><td>World Model</td><td>video diffusion model이 물리 법칙을 위반하는 원인을 attention의 motion planning 내부 메커니즘 해석으로 처음 규명해 world model 이해에 기여함</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2609.22361'>Common Cause, Not Cross-Attention: Blocking Visual Shortcuts in Audio-Video Generation</a></td><td>53</td><td>3</td><td>Multimodal</td><td>오디오-비디오 생성모델이 외형에서 지름길 학습하는 문제를 SCM으로 규명하고 counterfactual invariance가 필요충분조건임을 증명, causal reasoning 원리가 로봇 지각에도 시사점 있음</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2609.22462'>VLPSA: Vision-Language-Poisson-Safe Actions for Full-Body Safety of Learned Policies</a></td><td>52</td><td>9</td><td>VLA</td><td>Poisson Safety Function에서 유도한 CBF-QP로 VLA 정책을 재학습 없이 전신 안전 필터링, Franka FR3 실로봇 동적 장애물 환경에서 충돌회피율을 23.1%에서 91.2%로 높이면서 과제 성공률도 유지함</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2609.22587'>React When You Need To: Event-Triggered Asynchronous Inference for VLA Policies</a></td><td>52</td><td>9</td><td>VLA</td><td>고정 inference gap 대신 장면 변화량에 따라 재추론 시점을 동적으로 조절하는 asynchronous VLA inference로 실로봇 성공률 55%p 개선했지만 아이디어 자체는 기존 asynchronous inference의 점진적 확장임</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2609.22285'>ORDER: A Fictitious-World Benchmark for Domain-Adaptive Embodied AI</a></td><td>52</td><td>8</td><td>Embodied AI</td><td>가상의 물리 법칙으로 이루어진 세계를 만들어 사전학습 오염 없이 world-model induction을 측정하는 벤치마크, 지식테스트 정답률이 아니라 spatial reasoning 성능이 실제 계획 품질을 예측함을 iiwa7 시뮬레이션으로 보임</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2609.22611'>HIGenNTO: Scalable Humanoid Interaction Generation via Noise-Space Trajectory Optimization</a></td><td>52</td><td>8</td><td>Embodied AI/Humanoid</td><td>사전학습된 motion diffusion의 초기 noise를 최적화해 접촉이 많은 휴머노이드 상호작용 모션을 생성하는 방식이 새롭고 G1 실로봇 4개 과업까지 이어짐</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2609.23113'>Search, Ground, Plan: Functional Sufficiency for Task and Motion Planning under Incomplete Scene Knowledge</a></td><td>52</td><td>8</td><td>TAMP</td><td>불완전한 장면 지식 하에서 필요한 기능적 역할을 먼저 탐색-접지한 뒤에만 계획하는 GRAB-TAMP로 functional sufficiency라는 새로운 개념을 FM 기반 TAMP에 도입함</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2609.23275'>SCULPT-VLA: Learning Structured Control through Staged Action Grounding</a></td><td>52</td><td>8</td><td>VLA</td><td>teacher scaffold로 진행도·장면동역학·공간접지 요인을 먼저 형성한 뒤 점진적으로 떼어내며 action을 접지시키는 staged curriculum으로 SimplerEnv-WidowX와 실로봇에서 꾸준한 개선을 보임</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2609.23445'>BiRoAD: Learning Shared and Role-Adaptive Representations for Bimanual Manipulation</a></td><td>52</td><td>8</td><td>Manipulation/Bimanual</td><td>양팔 특징을 교환-대칭/교환-반대칭 성분으로 분해해 역할 편중 데이터에서도 일반화하는 BiRoAD로 기존 정책에 모듈로 얹을 수 있는 실용적 표현 기여임</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2609.23580'>TaskAnchor: Grounding Task State in Reactive VLAs for Long-Horizon Manipulation</a></td><td>52</td><td>8</td><td>VLA/Robot Memory</td><td>task-state aliasing을 정의하고 milestone 기반 task-state 좌표를 언어채널에 주입하는 경량 어댑터로 RMBench에서 4.9~5.5배 성능 향상을 보이면서도 추가 지연은 2ms에 불과함</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2609.23650'>Beyond Appearance Shifts: Task-Semantic Action Calibration for VLA Models</a></td><td>52</td><td>8</td><td>VLA</td><td>과업보존 변화에는 행동 드리프트가 생기고 의미파괴 변화에는 둔감한 두 가지 VLA 실패모드를 정의하고 선택적 evidence-gated calibration으로 대응한 BAS-VLA로 목표교체 실패를 0%로 억제함</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2609.23656'>WOLF: World Model Guided LiDAR Exploration with Predictive Frontiers</a></td><td>52</td><td>8</td><td>World Model/Navigation</td><td>recurrent world model로 가려진 영역의 미래 관측을 예측해 measured frontier와 결합하는 WOLF로 LiDAR UAV 탐사 효율과 커버리지를 크게 개선하고 실비행까지 검증함</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2609.24511'>InsertAnything: Generalizable Contact-Rich Precision Insertion from Simulation to Reality</a></td><td>52</td><td>8</td><td>Manipulation/RL</td><td>3D 손끝 힘 피드백과 목표자세를 결합한 RL 삽입정책을 시뮬레이션에서만 학습해 실세계 시연이나 파인튜닝 없이 배포한 InsertAnything으로 미지 형상 8종 평균 95% 성공률을 보임</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2609.24563'>ARSTAG: An Agentic Real2Sim2Real System for Task-Specific Robot Data Generation</a></td><td>52</td><td>8</td><td>Manipulation/Data Generation</td><td>RGB 한 장과 지시문만으로 장면 구성-시연 생성-랜덤화까지 언어 에이전트 계층이 수행하는 ARSTAG로 pi0.5 sim2real 평균 성공률 74.6%를 달성한 확장 가능한 데이터 생성 파이프라인임</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2609.24778'>H2RBench: A Real-to-Sim Benchmark for Evaluating Human-to-Robot Transfer</a></td><td>52</td><td>8</td><td>Manipulation/Benchmark</td><td>동일 프로토콜로 human-to-robot 전이 방법들을 비교하는 CoRL H2RBench로 시뮬레이션 성능이 실로봇 성능과 r=0.89로 강하게 상관됨을 보여 향후 방법 비교의 표준 잣대를 제공함</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2609.24815'>Uranus: Building the Next-Generation Simulation Infrastructure for Embodied AI</a></td><td>52</td><td>8</td><td>Simulation/World Model</td><td>관절궤적 조건 autoregressive diffusion으로 24fps 스트리밍 시뮬레이션을 생성하는 Uranus로 데이터 기반 시뮬레이터라는 방향을 world model적 관점에서 확장한 인프라 기여임</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2609.23896'>BarrierFormer: Transformer-Guided Predictive Barrier Enforcement for Safe Robot Control</a></td><td>52</td><td>7</td><td>Safe RL/Control</td><td>causal transformer가 rollout을 생성해 CBF 제약을 평가하고 barrier-consistent 교사가 지도하는 model-free 안전정책 BarrierFormer로 온라인 최적화 없이 실시간 예측적 안전을 달성함</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2609.24140'>BayesianGS-SLAM: Uncertainty-Aware Neural Rendering SLAM via Probabilistic Formulation</a></td><td>52</td><td>7</td><td>SLAM/3D Vision</td><td>센서잡음과 opacity 유도 맵불확실성을 모두 반영한 예측 불확실성을 매핑·추적·키프레임 선택 전반에 재사용하는 BayesianGS-SLAM으로 3DGS SLAM의 불확실성 정식화를 체계화함</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2609.23565'>MaskVLA: Visual Masking Against Trajectory Overfitting of Vision-Language-Action Model</a></td><td>50</td><td>8</td><td>VLA</td><td>VLA finetuning 시 발생하는 trajectory overfitting을 wrist·main 카메라 마스킹으로 완화하는 방법이라 VLA 우선 주제에 직접 해당하나 기법 자체는 비교적 단순함</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2609.22606'>VT-Bridge: Bridging Pretrained Foundation VLAs to VTLAs via Lightweight Residual Adaptation</a></td><td>50</td><td>8</td><td>VLA/Tactile</td><td>사전학습된 VLA에 경량 residual adapter만 붙여 촉각까지 다루는 VTLA로 확장한 실용적 방법이며 50개 데모로 접촉 과업 성공률을 크게 끌어올렸지만 구조적으로는 어댑터 튜닝 수준임</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2609.22829'>Whole-Body UMI: Transferring UMI Manipulation Skills to Humanoid Whole-Body Manipulation via Real-Time Motion Generation</a></td><td>50</td><td>8</td><td>Manipulation/Humanoid</td><td>UMI로 모은 end-effector 궤적을 실시간 전신 모션생성기로 변환해 휴머노이드 전신 조작에 이식하는 파이프라인으로 formulation은 새롭지만 과업별 성공률 편차가 30~90%로 큼</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2609.22840'>ForceRFT: Refining VLA Actions through Force-Guided Residual Reinforcement Learning</a></td><td>50</td><td>8</td><td>VLA/RL</td><td>고정된 force-conditioned VLA 위에 손목 wrench로 조건화한 residual RL을 얹어 접촉 회복 행동을 배우는 구조로 사람 교정과 자율 성공 데이터를 나눠 학습해 credit assignment 문제를 다룸</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2609.23131'>Selective Commitment for Language-Guided Object Retrieval under Partial Observability</a></td><td>50</td><td>8</td><td>Manipulation/Active Perception</td><td>타겟 정체성·컨테이너 관계·존재여부에 대한 결합 belief를 유지하며 정보수집-집기-포기를 조율하는 closed-loop 프레임워크로 실로봇 재관측·복구까지 보여줌</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2609.24068'>When Does Touch Matter? Charting the Vision-Interaction Gap in Cluttered Dexterous Grasping</a></td><td>50</td><td>8</td><td>Tactile/Manipulation</td><td>잡동사니 속 덱스터러스 그래스핑에서 촉각·손목 wrench가 시각 대비 언제 이득이 되는지를 통제 실험으로 처음 정량화한 연구로 vision-interaction gap을 벤치마크화한 기여가 큼</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2609.24155'>Object-Centric Conditioning for Visuomotor Flow Matching</a></td><td>50</td><td>8</td><td>Manipulation/Representation</td><td>장면을 semantic과 spatial 단서로 분리해 A2A flow matching을 조건화하는 SlotFlow로 공간 OOD와 시각교란에 대한 강건성을 얻으면서 추론 효율은 유지함</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2609.24180'>GraspTune: Tactile-Driven Execution Refinement for Robust Grasping</a></td><td>50</td><td>8</td><td>Manipulation/Tactile</td><td>잡기 제안 자체는 건드리지 않고 접촉 형성 단계에서 촉각 기반 residual TCP 보정을 학습하는 GraspTune으로 여러 grasp generator에 공통으로 붙여 실행단 성공률을 크게 끌어올린 실용적 기여임</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2609.24507'>TACIT: Tactile Contact Supervision for Spatial Attention in Dexterous Manipulation</a></td><td>50</td><td>8</td><td>Manipulation/Tactile</td><td>인간 주석 없이 측정된 촉각 접촉만으로 공간 attention을 지도학습하는 TACIT로 10개 시연만으로 볼배치·페그삽입 성공률을 크게 높인 few-shot 기여임</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2609.24576'>What do VLM-Based Vision-Language Navigation Models Rely on: Interpreting and Steering Policy Behavior</a></td><td>50</td><td>8</td><td>Navigation/Interpretability</td><td>개입 기반 지표로 VLN 정책이 시각·지시문·기억 중 무엇에 의존하는지 밝히고 활성화 벡터를 zero-shot으로 실환경에 스티어링까지 시킨 해석가능성 연구로 방법론적 통찰이 실용적으로 이어짐</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2609.24621'>Learning tactile perception from high-bandwidth single-point sensing</a></td><td>50</td><td>8</td><td>Tactile Perception</td><td>단일점 고대역 촉각 신호를 시간-주파수 스펙트로그램으로 바꿔 표준 vision encoder로 처리하는 SpectRobot으로 공간 밀도 대신 대역폭을 활용하는 새로운 촉각 표현을 제시함</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2609.23432'>RopeFormer: Cross-Trial Adaptation from Interaction History for Dynamic Rope Manipulation</a></td><td>50</td><td>7</td><td>Manipulation/Deformable Object</td><td>명시적 파라미터 추정 없이 시행이력을 context로 유지해 미지 로프 동역학에 적응하는 RopeFormer로 실로봇 H1-2에서 목표 도달시간과 명중률을 개선함</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2609.23976'>Anticipatory Robot Goalkeeping via Monotone Optimal Stopping</a></td><td>50</td><td>7</td><td>RL/Decision Theory</td><td>언제 동작을 개시할지를 policy-conditional finite-horizon optimal stopping으로 정식화한 MOS로 4족 골키퍼 실로봇에서 구원율을 67.7%에서 74.4%로 올려 의사결정 이론을 로봇 제어에 접목한 참신한 틀임</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2609.24840'>PredActor: Predictive Action Diffusion for Steerable Onboard Humanoid Control</a></td><td>50</td><td>7</td><td>Humanoid/Control</td><td>실행 가능한 행동과 내부 future-state 궤적을 동시에 생성해 classifier guidance로 목표를 조향하는 PredActor로 Jetson Orin에서 20ms 이내 온보드 실행을 달성한 실용적 diffusion 제어임</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2609.22868'>Planning-Aligned Pretraining of BEV Representations with Sparse Action-Conditioned Targets for End-to-End Autonomous Driving</a></td><td>50</td><td>6</td><td>Navigation</td><td>단일 LiDAR로부터 planning에 맞춘 희소 action-conditioned target으로 BEV를 사전학습해 E2E 주행 표현을 개선한 새 pretraining 방식임</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2609.24708'>SPARSER: Sparse Variable Projection by Exploiting Separable Structure in Robotic Perception</a></td><td>50</td><td>6</td><td>SLAM/Perception</td><td>SLAM·SfM에서 자주 쓰이는 separability를 gauge symmetry 문제까지 확장한 matrix-free Schur complement 연산자 SPARSER로 CPU·GPU 모두에서 최대 40배 이상 속도향상을 보인 견고한 수치최적화 기여임</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2609.22317'>EditWM: Event-Decomposed World Modeling with Incremental Correction for End-to-End Autonomous Driving</a></td><td>48</td><td>8</td><td>World Model</td><td>자율주행 world model을 정상 진화와 이벤트 기반 보정으로 분해해 planning에 연결, NAVSIM 전체 12146 장면에서 future-feature 오차 감소와 EPDMS 91.05 달성함</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2609.22385'>Active Spatial Inspection for Effective and Efficient Embodied Exploration</a></td><td>48</td><td>8</td><td>Navigation</td><td>단서의 충분성을 공간적으로 명시 판단하는 evidence-grounded perception과 exposure-informed movement로 조기종료·과잉탐색을 완화, active perception 우선주제에 해당하며 navigation·QA에서 각각 18.0%, 10.3% 개선을 보임</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2609.23423'>RiverVLN: Phase-Grounded Temporal Vision--Language Navigation for Unmanned Surface Vehicles</a></td><td>48</td><td>8</td><td>Navigation/VLN</td><td>지시문을 검증가능한 의미적 phase 시퀀스로 바꾸고 온라인으로 진행상태를 추적하는 PGT-NAV로 연속 관성 운동을 하는 무인수상정 VLN이라는 새 도메인을 여는 벤치마크임</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2609.24189'>A Topological Representation with Object-Path Graphs for Open-Vocabulary Instance Navigation</a></td><td>48</td><td>8</td><td>Navigation/Scene Graph</td><td>밀집 metric map 없이 object-path graph만으로 open-vocabulary 인스턴스 내비게이션을 수행하는 경량 위상 프레임워크로 scene graph와 navigation을 한 표현으로 통합함</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2609.24995'>MIGU: Multimodal Instruction Grounding under Uncertainty for Manipulation Planning</a></td><td>48</td><td>8</td><td>Manipulation/Multimodal</td><td>시선·손가락 기하 불확실성을 전파한 3D 가능도와 VLM 의미사전을 베이즈식으로 결합해 애매한 지시-제스처를 grounding하는 MIGU로 실환경 벤치마크에서 baseline을 능가함</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2609.24312'>AnalogDepth: Multi-view Geometry from FPV drones under Analog Video Transmission</a></td><td>48</td><td>7</td><td>3D Vision</td><td>아날로그 영상 전송 잡음이 Depth Anything 3 같은 feed-forward geometry foundation model을 크게 저해함을 보이고 FPV 드론에 맞는 파라미터 효율적 적응을 제안한 실용적 로봇 인식 연구임</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2609.22809'>Kinematic Interface for the Wild: Modular Bimanual Loco-Manipulation Capture from 360$^{\circ}$ Cameras Alone</a></td><td>48</td><td>7</td><td>Manipulation/Data Collection</td><td>360도 카메라만으로 양팔 UMI 데이터 수집 시 위치추정을 해결하는 캡처 키트로 부가 하드웨어 없이 확장 가능한 데이터 수집을 가능하게 하고 3DGS 재구성까지 연결됨</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2609.22813'>Commonsense-Grounded Path Planning from Abstract Instructions</a></td><td>48</td><td>7</td><td>Navigation</td><td>VLM으로 암묵적 고려사항(젖은 바닥 등)을 지역별 랭킹으로 바꿔 경로탐색 비용에 반영하는 CoRS 방법으로 embodied spatial reasoning에 닿아있고 1350문제 벤치마크도 새로 구축함</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2609.22852'>Physical-Touch Observability from Wrist Wrench in Granular Scooping</a></td><td>48</td><td>7</td><td>Manipulation/Tactile</td><td>손목 wrench가 지형-행동 짝이 맞을 때만 최종 적재량을 예측할 수 있다는 physical-touch observability 개념을 6700회 실로봇 스쿠핑으로 검증한 실증연구임</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2609.22983'>Connectivity-Aware Exploration of Robotic Grasp Spaces</a></td><td>48</td><td>7</td><td>Manipulation/Grasping</td><td>SE(3) grasp 공간의 연결성 구조를 분석해 exploration 전략에 활용하는 새로운 관점으로 grasp space의 위상적 조직화가 탐색 효율에 기여함을 실증함</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2609.23439'>Receding-Horizon Pushing with Composable Object-Centric Policies</a></td><td>48</td><td>7</td><td>Manipulation</td><td>포인트클라우드 기반 저수준 push 정책과 BIT* 상위 경로탐색을 feasibility 피드백으로 연결한 계층적 pushing 프레임워크로 zero-shot sim2real까지 확인함</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2609.23483'>STRIDER: Stepping-Enabled Multi-Gait Hierarchical 3D Loco-Manipulation Framework for Humanoid Robots</a></td><td>48</td><td>7</td><td>Locomotion/Humanoid</td><td>발디딤 추적과 전신조작을 하나의 학생 정책으로 증류하는 LD-PPO를 제안해 실제 휴머노이드에서 다중 보행-조작을 검증했지만 distillation 기법 자체는 점진적 개선에 가까움</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2609.23486'>Cognitive Action Reasoning for Proactive Robots from Human-Centered Multimodal Observations</a></td><td>48</td><td>7</td><td>Embodied AI/HRI</td><td>명시적 지시 없이 멀티모달 인간 단서로 다음 행동을 정하는 Proactive Robot Action Reasoning을 새 문제로 정의하고 1만 샘플 데이터셋을 구축한 초기 단계 기여임</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2609.23731'>Marginal Calibration Does Not Compose: Hidden Dependence in Modular Robot Navigation</a></td><td>48</td><td>7</td><td>Navigation/Uncertainty</td><td>개별적으로 잘 보정된 모듈도 합성되면 보정이 깨질 수 있음을 보인 워크숍 논문으로 모듈형 로봇 시스템 설계 전반에 시사점이 크지만 검증 규모는 작음</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2609.23800'>ContactDP: Contact-Guided Diffusion Policy for Tight Insertion Tasks</a></td><td>48</td><td>7</td><td>Manipulation/Tactile</td><td>손목 RGB, 지촉, 힘/토크를 결합한 diffusion policy로 접촉상태를 추론해 타이트 삽입을 안정화한 ContactDP로 비전전용 baseline 대비 신뢰성이 뚜렷이 좋음</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2609.24145'>MimicAgent: Quadruped Skills via Prompt-to-Trajectory Generation</a></td><td>48</td><td>7</td><td>RL/Locomotion</td><td>보상설계 대신 LLM 에이전트가 참조 모션을 생성해 example-guided RL로 4족 스킬을 학습시키는 MimicAgent로 reward shaping 부담을 우회하는 접근이 실용적임</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2609.24547'>MIRA: Real-Time Full-Duplex Human-Robot Interaction for Embodied Companions</a></td><td>48</td><td>7</td><td>HRI/Humanoid</td><td>스트리밍 음성에서 응답 텍스트와 embodiment cue를 동시에 예측하고 물리적 안전을 저수준에서 강제하는 이중 시간척도 정책 MIRA로 full-duplex 동반로봇 상호작용을 실기체 Astribot S1에서 검증함</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2609.24552'>Smoothness as a Constraint for Stable Humanoid Locomotion</a></td><td>48</td><td>7</td><td>Locomotion/RL</td><td>상체·하체 부드러움을 별도 제약군으로 분리하고 경계근접 시 활성화되는 barrier penalty를 쓰는 DeCap으로 보상항 튜닝 없이 여러 지형에 전이되는 명시적 smoothness 제약을 제안함</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2609.24632'>Feasibility Distance Fields for Heterogeneous Constraints in Robot Configuration Space</a></td><td>48</td><td>7</td><td>Motion Planning/Theory</td><td>관절공간 거리라는 공통 metric으로 충돌·관절한계·특이점 등 이질적 제약을 하나의 feasibility distance field로 통일한 이론적 틀로 신경망 근사와 다중 실험 검증까지 갖춘 일반화 가능한 도구임</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2609.22716'>ZIL: Zero-shot Image-to-LiDAR Registration</a></td><td>48</td><td>6</td><td>Navigation</td><td>비동기 프레임 간 이미지-LiDAR 등록을 위한 최초의 zero-shot foundation model이라 로봇 내비게이션·매핑에 바로 쓰일 수 있음</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2609.23492'>CE$^4$L: Continual Ego, Exo, and Ego-Exo Learning</a></td><td>48</td><td>6</td><td>Embodied AI</td><td>ego·exo 시점과 태스크가 동시에 바뀌는 상황에서의 continual learning을 다루는 통합 멀티뷰 벤치마크라 embodied agent 지각 연구와 직결됨</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2609.23534'>PosEviLoc: Position-Conditioned Spatial Evidence for Language-Based 3D Localization</a></td><td>48</td><td>6</td><td>Navigation</td><td>전역 디스크립터 압축 대신 객체 단위 의미와 위치 조건 증거로 텍스트-포인트클라우드 위치를 찾는 방법이라 embodied spatial reasoning과 연결됨</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2609.24839'>When Wider Views Fail: Stress-Testing Feed-Forward 3D Reconstruction</a></td><td>48</td><td>6</td><td>3D Vision</td><td>feed-forward 3D reconstruction 모델이 넓은 시야각 분포 이동에서 실패하는 양상을 체계적으로 스트레스 테스트해 배포 신뢰성 관련 실패 모드를 규명함</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2609.22630'>Simultaneous Forward and Inverse Human-in-the-Loop Optimization</a></td><td>48</td><td>6</td><td>RL/HRI</td><td>인간 선호로부터 forward-inverse 보상을 동시에 추정하는 CoRL 논문으로 human-robot interaction 세팅에서 샘플 효율을 개선하지만 로보틱스 자체보다 보상학습 이론 기여가 큼</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2609.22941'>D3GS: Depth, DINO, and RGB Diffusion Co-Guided 3D Gaussian Splatting for Sparse-View Reconstruction</a></td><td>48</td><td>5</td><td>3D Vision</td><td>depth·DINO·diffusion을 함께 활용해 희소 뷰 3DGS 재구성을 개선한 방법으로 object-centric 3D representation 우선 주제와 맞닿음</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2609.23182'>GrapeSplat: Geometry-Grounded Reconstruction via Amalgamated Pose-Free Encoding for Feed-Forward 3D Gaussian Splatting</a></td><td>48</td><td>5</td><td>3D Vision</td><td>voxel 정렬 장면 표현에서 Gaussian을 직접 디코딩하는 pose-free feed-forward 3DGS라 실시간 로봇 3D 인식에 참고할 만함</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2609.22588'>Seeing is not Enough: Vision-Language Models Perceive Evidence but Fail to Act</a></td><td>48</td><td>4</td><td>Multimodal</td><td>VLM이 증거를 인식하고도 행동에 반영하지 못하는 process failure를 분리 진단한 벤치마크로 failure detection 관점과 연결됨</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2609.22283'>Rethinking Streaming Video Diffusion Model: Context, Execution, and Training</a></td><td>48</td><td>2</td><td>Video</td><td>streaming video diffusion의 설계 공간을 체계적으로 분석했고 world model의 비디오 생성 기반 기술과 맞닿아 있음</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2609.22135'>Read-Best Is Not Steer-Best: A Probing--Steering Layer Dissociation in Omni-Modal Large Language Models</a></td><td>48</td><td>1</td><td>Multimodal/Interpretability</td><td>probing 정확도가 가장 높은 층이 steering에도 최적이라는 가정이 3개 옴니모달 모델에서 깨짐을 인과적으로 보인 해석가능성 연구로 표현학습 통찰은 있으나 로보틱스 응용은 아님</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2609.23381'>Discovering Physical Representation Languages</a></td><td>47</td><td>3</td><td>LG</td><td>익명 실험만으로 물리량의 측정 온톨로지를 다항시간에 복원하는 이론적 프레임워크, 물리적 세계표현 학습 원리로서 world model과 접점 있음</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2609.24942'>Exactness at Inference: A Representational Criterion for Out-of-Distribution Generalization</a></td><td>47</td><td>2</td><td>LG</td><td>생성 메커니즘과 구조적으로 동치인 표현만이 OOD 일반화를 보장한다는 exactness 기준을 Tensor Logic으로 제시한 이론 연구, 외삽·개체 결합 문제가 embodied reasoning과 접점 있음</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2609.24209'>Displacement Geometry Captures Platonic Shared Reality Across Models and Modalities</a></td><td>47</td><td>0</td><td>Multimodal</td><td>44개 모델 간 절대 위치는 다르나 displacement vector는 정렬됨을 보이고 이를 이용한 무학습 capability 전이(Shadow Casting)를 제안, 표현학습 이론으로 novelty 있으나 로봇과 무관함</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2609.23038'>Spatial-Interactor: Learning Spatial Reasoning through Interaction with the Observable Physical World</a></td><td>46</td><td>8</td><td>Embodied AI</td><td>물리세계와의 상호작용 궤적으로 VLM의 공간상태 전이 추론을 3단계 커리큘럼으로 학습, embodied spatial reasoning 우선주제에 직접 부합하는 참신한 데이터/학습 설계임</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2609.22359'>Resist, Update, Reject: Preference Optimization Installs a Prior-Dependent Reliability Switch</a></td><td>46</td><td>0</td><td>NLP</td><td>선호최적화 목적함수가 신뢰도 정보를 식별 불가능하게 만드는 문제를 데이터로 해결한 정체성 연구, novelty 있으나 로봇과 무관함</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2609.23312'>Manipulation Feasible Navigation Among Movable Obstacles with Discrete Contact Pushing</a></td><td>45</td><td>7</td><td>Navigation/Manipulation</td><td>이동 가능한 대형 장애물을 밀어서 치우는 NAMO를 고수준 재배치 탐색과 저수준 강화학습 push 정책으로 계층화한 실용적 프레임워크임</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2609.23418'>HEARTH: An Object-Centric RGB-Thermal-3D Dataset for Temperature-Aware Robot Manipulation</a></td><td>45</td><td>7</td><td>Manipulation/Dataset</td><td>물체 표면온도를 메쉬에 매핑한 최초의 RGB-열화상-3D 데이터셋으로 pi0.5에 온도관측을 더해 성공률을 35%에서 75%로 끌어올려 새로운 물리적 속성 모달리티를 보임</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2609.23491'>Elevator-VIGS: Separating Elevator Motion from Robot Motion in Visual-Inertial Gaussian Splatting SLAM</a></td><td>45</td><td>7</td><td>SLAM/3D Vision</td><td>엘리베이터 탑승 시 카메라와 IMU가 서로 다른 운동을 보는 문제를 엘리베이터 프레임과 transport state로 분리해 해결한 3DGS SLAM으로 특수 상황에 대한 새로운 정식화가 돋보임</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2609.23666'>UniPoint: Unified Point-Level Sensor Fusion for Humanoid Locomotion Across Challenging Terrains</a></td><td>45</td><td>7</td><td>Locomotion/Perception</td><td>LiDAR와 다중 depth 카메라를 포인트 단위로 조기융합해 지형별 강인성을 확보한 휴머노이드 로코모션 지각 시스템으로 실용성은 높지만 센서 융합 엔지니어링 성격이 강함</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2609.23910'>ReVeal: A Reconstruction-Aware Real-to-Sim Framework for VLA Policy Evaluation</a></td><td>45</td><td>7</td><td>VLA/Evaluation</td><td>재구성 품질과 sim-real 정책 성능 일치도를 함께 측정하는 지표(NVMF, APGF)를 제안해 real2sim VLA 평가의 신뢰도를 검증한 실용적 방법론 논문임</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2609.23997'>RoboTalk: Learning Multi-Robot Communication and Coordination from Multimodal Demonstrations</a></td><td>45</td><td>7</td><td>Multi-Robot/VLA</td><td>리더-팔로워 계획, 도구호출, 언어소통을 담은 멀티모달 데이터셋으로 온디바이스 소형 VLM을 파인튜닝해 다중로봇 협업 성공률을 크게 올렸지만 데이터셋 구축과 파인튜닝 중심 기여임</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2609.24055'>Toward Human-in-the-Loop Robot Failure Recovery: Bridging Communication Gaps in Human-Robot Collaboration</a></td><td>45</td><td>7</td><td>Failure Recovery/HRI</td><td>청자의 지식 수준 차이를 반영해 로봇이 도움 요청 문구를 만드는 문제를 다룬 LD-HRI 벤치마크로 failure recovery의 소통 측면을 새로 정의했지만 요청생성 자체는 여전히 초보-전문가 격차가 큼</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2609.24906'>Visuomotor Robotic Pruning in Planar Orchards Using Hybrid Reinforcement Learning</a></td><td>45</td><td>7</td><td>Manipulation/RL</td><td>합성 과수원 시뮬레이터에서 오프라인 시연과 온라인 rollout을 결합한 하이브리드 RL로 optical flow만으로 전지 로봇을 학습시켜 실외·실내 38회 실증까지 zero-shot 전이한 실용적 농업로봇 기여임</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2609.24727'>ReSTI: A Source-Grounded Audit and Repair of STI-Bench</a></td><td>45</td><td>6</td><td>Embodied AI</td><td>ScanNet·Waymo·Omni6DPose 기반 STI-Bench의 좌표계·시간축 오류를 체계적으로 감사하고 복구한 연구라 embodied spatial reasoning 평가의 신뢰성을 바로잡는 기여임</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2609.22173'>Industrial Kinematic Trajectory Model (IKTM): Coordinate-Free Autoregressive Generator</a></td><td>45</td><td>6</td><td>Navigation</td><td>절대 좌표 없이 속도·방향 변화만으로 산업 현장 차량 궤적을 생성하는 coordinate-free 모델이라 특정 사이트에 묶이지 않는 일반화 가능한 모빌리티 표현을 제시함</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2609.22733'>Rapidly-Iterating Grid-Based Near-Optimal Kinodynamic Motion Planning</a></td><td>45</td><td>6</td><td>Motion Planning</td><td>grid decomposition으로 kinodynamic planning을 상수시간 갱신 가능하게 만들고 점근적 near-optimality를 증명한 고전 planning 논문이며 학습 기반은 아님</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2609.22926'>Embodied Snap: Octopus-Inspired Distributed Reach-and-Attach with a Speed-Limited Soft Arm</a></td><td>45</td><td>6</td><td>Manipulation/Soft Robotics</td><td>문어에서 착안해 느린 preload와 빠른 elastic release를 분리한 embodied snap 제어로 기어 구동 소프트암의 속도 한계를 몸체 역학으로 극복하는 아이디어가 흥미로움</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2609.23488'>FeasibleFlow: One-Step Joint Transport of Configuration Feasibility and Trajectories for End-to-End Driving</a></td><td>45</td><td>6</td><td>Autonomous Driving</td><td>configuration-space feasibility 필드와 다중 궤적을 하나의 one-step flow로 동시 이송하는 FeasibleFlow로 NAVSIM에서 안전성-진행도 균형을 개선한 end-to-end 주행 방법임</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2609.23745'>FlockDiffusion: Assignment-Conditioned Diffusion for Multi-Drone Task Allocation and Completion</a></td><td>45</td><td>6</td><td>Multi-Robot Planning</td><td>장면그래프 인코더와 할당조건 diffusion transformer로 다중 드론 태스크 번들링을 학습한 FlockDiffusion으로 고전 파이프라인 대비 6~7배 빠른 추론을 보임</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2609.24253'>OpenFlyScan: A Quality-Guided Aerial Reconstruction System for Consumer Drones</a></td><td>45</td><td>6</td><td>3D Vision/3DGS</td><td>GS 렌더링 오차로 재구성 품질을 예측하고 부족한 영역만 재촬영하도록 유도하는 OpenFlyScan으로 소비자용 드론만으로 대규모 도시 3DGS 자산 구축을 개선한 실용적 시스템임</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2609.23049'>VDGS: Visibility-Driven Large-Scale 3D Gaussian Splatting for Aerial Scene Reconstruction</a></td><td>45</td><td>5</td><td>3D Vision</td><td>UAV로 촬영한 대규모 항공 장면을 가시성 기반으로 3DGS 재구성하는 방법이라 로봇 자율 매핑에 바로 쓰일 수 있음</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2609.23286'>RegVGGT: Sustainable Visual Geometry Grounding for Streaming via Regulated Memory</a></td><td>45</td><td>5</td><td>3D Vision</td><td>토큰의 초기 saliency로 장기 중요도를 판단해 메모리를 조절하는 스트리밍 3D 재구성 방법이라 로봇의 온라인 장면 매핑에 참고할 만함</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2609.24565'>Active Visual Sampling with a Connectome-Constrained Fly Model for One-Shot Hatch Recognition in Architectural Drawings</a></td><td>45</td><td>5</td><td>CV</td><td>모션용으로 사전학습된 커넥톰 제약 파리 시각 신경망을 태스크별 추가학습 없이 재사용해 one-shot 패턴 매칭을 수행한 생체모방 active visual sampling 연구임</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2609.22687'>PanoSeg3R: Feed-Forward 3D Semantic Segmentation for Panoramic Images with an Automatic Data Curation Pipeline</a></td><td>45</td><td>4</td><td>3D Vision</td><td>파노라마 영상에서 3D 기하와 다시점 시맨틱 세그멘테이션을 한 번에 예측하는 feed-forward 방법이라 scene understanding에 참고할 만함</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2609.22308'>GameReplica: A Benchmark for Black-Box Visual Game Replication by Vision-Language Agents</a></td><td>45</td><td>3</td><td>Embodied AI</td><td>블랙박스 게임을 시각 관찰만으로 규칙을 추론해 재현하는 벤치마크라 world model적 환경 이해와 맞닿아 있으나 물리 로봇과는 거리 있음</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2609.24287'>Classifier-Free Guidance in Flow Matching: Non-Autonomous Potentials, Overshoot, and Posterior-Mean Control</a></td><td>45</td><td>3</td><td>RL</td><td>flow matching에서 classifier-free guidance가 분포를 왜곡하는 원인을 기하학적으로 규명하고 posterior-mean 제어를 제안해 flow matching 기반 정책 학습 설계에도 참고할 만함</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2609.22152'>Is Imagination Derived from Hallucination? A Cross-Taxonomy Evaluation of Imagination and Hallucination in Large Language Models</a></td><td>45</td><td>0</td><td>NLP/Evaluation</td><td>상상력과 환각을 같은 생성에서 동시에 채점하는 Whiteboard 벤치마크로 79개 LLM과 1만3천여 인간판단으로 검증한 대규모 평가 기여이나 로보틱스와는 무관함</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2609.22691'>Generative Embodied Multiple Behavior Control Systems for Human-like Agents</a></td><td>44</td><td>6</td><td>Embodied AI</td><td>습관적/목표지향적 이중 통제시스템과 키프레임 기반 3D 모션생성으로 인간형 에이전트의 행동을 재현, embodied agent 행동제어에 직접 관련된 신규 formulation임</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2609.23366'>What Can a Recurrent State Safely Forget?</a></td><td>44</td><td>3</td><td>LG</td><td>recurrent state가 안전하게 잊어도 되는 정보를 predictive quotient로 규명한 이론, 메모리 압축·robot memory 설계에 시사점 있음</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2609.22867'>Leveraging Inference-Time Compute for Diffusion Models via Global Scheduling of Denoising Trajectories</a></td><td>44</td><td>2</td><td>Video</td><td>확산모델 denoising trajectory 전체에 대한 inference-time compute 배분을 수학적으로 정식화한 연구, test-time optimization 일반 원리로서 로봇 정책에도 응용 가능성 있음</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2609.23387'>Blind Thermodynamic Ontology Discovery from Anonymous Experiments</a></td><td>44</td><td>2</td><td>LG</td><td>위 논문의 열역학 버전, 익명 관측에서 extensive/intensive 양을 식별하는 동일 계열 이론 연구임</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2609.22278'>DeViGrasp: Robust Visual Mobile Grasping for Quadruped Manipulators under Degraded Perception</a></td><td>42</td><td>9</td><td>Manipulation</td><td>저하된 지각 하 사족 매니퓰레이터 모바일 그래스핑 벤치마크와 teacher-student temporal memory 프레임워크, 열화 조건별 체계적 평가가 실질적이나 시뮬레이션 벤치마크 중심임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2609.22289'>OJOx: Specification-Conditioned Demonstrations for Embodied AI in Construction</a></td><td>42</td><td>8</td><td>Embodied AI</td><td>설계 명세를 함께 기록하는 specification-conditioned demonstration이라는 새로운 데이터 패러다임 제안, 건설 도메인 단일 세션 검증이라 실증은 제한적이나 문제 정식화가 참신함</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2609.22925'>&quot;Dear LLaVA, Please Drive&quot;: A Depth-Aware Vision-Language Agent for Closed-Loop Robotic Control</a></td><td>42</td><td>7</td><td>Navigation/VLA</td><td>라벨 궤적 대신 미분가능한 기하 비용장에 imperative learning으로 VLM을 LoRA 파인튜닝해 스테레오 깊이만으로 주행하는 구조는 흥미롭지만 검증 범위가 좁음</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2609.22973'>An Empirical Study and Open Testbed for Federated Fine-Tuning of Vision-Language-Action Models</a></td><td>42</td><td>7</td><td>VLA/Federated Learning</td><td>사전학습 VLA에 대한 federated fine-tuning을 체계적으로 비교한 실증연구로 새로운 방법 제안보다 재현 가능한 벤치마크와 교훈 도출에 의의가 있음</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2609.23133'>AquaCap: A Training-Free Underwater Embodied Agent with Code-as-Policy</a></td><td>42</td><td>7</td><td>Embodied AI/Underwater</td><td>code-as-policy를 수중 환경에 training-free로 확장하고 failure-aware 메모리로 재계획하는 구조로 새로운 도메인 적용이 핵심 기여이며 방법론 자체는 기존 패러다임의 이식임</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2609.23784'>PackLab: A Comprehensive Framework for Developing, Training, and Evaluating MLLMs in Robotic Bin Packing</a></td><td>42</td><td>7</td><td>Manipulation/Multimodal</td><td>빈패킹을 위한 MLLM 학습-평가 프레임워크로 물리기반 시뮬레이션과 벤치마크를 함께 구축했지만 방법 자체는 폐루프 MLLM 정책의 응용에 가까움</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2609.24317'>Performance-Preserving Online Adaptation in Social Navigation via Diffusion Steering</a></td><td>42</td><td>7</td><td>Navigation/RL</td><td>diffusion steering RL로 noise policy만 학습해 기본 diffusion 정책 성능을 보존하며 소셜 내비게이션을 배포환경에 온라인 적응시킨 방법임</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2609.24896'>Steerable and Reactive Grasping Through Modular Design with a Three-Point Interface</a></td><td>42</td><td>7</td><td>Manipulation/Grasping</td><td>grasp affordance heatmap에서 뽑은 세 접촉점으로 전역 기하 추론과 국소 RL 안정화를 분리한 모듈형 그래스핑 프레임워크로 일반화된 촉감정제 정책이 물체 전반에 공유됨</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2609.22857'>Image Frame Dynamic Object Segmentation and Ego Motion Estimation using Radar Image Fusion</a></td><td>42</td><td>6</td><td>Navigation</td><td>레이더 도플러로 ego motion과 동적 객체 세그멘테이션의 상호 의존 문제를 함께 푸는 방법이라 자율주행 로봇의 상태 추정에 직접 적용됨</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2609.23003'>M3GA-Wild: A Large-Scale Dataset and Benchmark for Multi-Modal Multi-session Ground-to-Aerial Place Recognition in Forests</a></td><td>42</td><td>6</td><td>Navigation</td><td>숲 환경에서 지상-공중 멀티모달 장소 인식을 위한 대규모 데이터셋·벤치마크로 필드 로봇 측위에 직접 쓰일 수 있음</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2609.23541'>Towards robust multimodal 3D object detection via visual foundation models</a></td><td>42</td><td>6</td><td>Navigation</td><td>SAM 같은 vision foundation model을 활용해 LiDAR-카메라 멀티모달 3D 검출을 OOD 손상에 강건하게 만든 자율주행 인식 연구임</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2609.23961'>Colon3R: Cross-Domain 3D Reconstruction from Monocular Colonoscopic Video</a></td><td>42</td><td>6</td><td>3D Vision</td><td>수술 로봇 대장내시경을 위한 단안 비디오 3D 재구성 연구로 약한 텍스처·비강체 조직이라는 실제 제약을 다루는 의료 로봇 인식 기여임</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2609.24151'>STAR: Scene- and Task-Aware 4D Radar Preprocessing Towards End-to-End Cognitive Radar</a></td><td>42</td><td>6</td><td>Navigation</td><td>신호 기준 CFAR 대신 장면·태스크 인지 방식으로 4D 레이더 포인트클라우드를 전처리하는 방법이라 로봇 perception 파이프라인에 직접 적용됨</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2609.23856'>Object-Centered Reconstruction for Vision-Based 3D Force Estimation</a></td><td>42</td><td>6</td><td>3D Vision/Medical Robotics</td><td>스테레오 내시경 영상에서 조직 변형을 object-centered 좌표로 재구성해 3D 접촉력을 추정하는 방법으로 힘센서가 없는 구형 수술 로봇에 적용 가능한 실용적 기여임</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2609.24054'>AquaOrbit: Sim-to-Real Reinforcement Learning for Underwater Target Orbiting under Intermittent Visual Feedback</a></td><td>42</td><td>6</td><td>RL/Underwater</td><td>시각신호가 끊길 때 latched line-of-sight로 재획득하는 복구모듈을 갖춘 RL 제어기로 sim2real zero-shot 배치까지 검증했지만 방법론 자체는 기존 RL 파이프라인의 응용임</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2609.24187'>StenoVLA-3D: 3D-Aware Reasoning VLA for Navigation Through Gastrointestinal Stenoses</a></td><td>42</td><td>6</td><td>VLA/Medical</td><td>point-map을 backbone에 융합하고 진행도 상태를 추적하는 3D-aware VLA로 내시경 협착 통과를 다루며 임상 팬텀 실험까지 이어졌지만 도메인이 니치함</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2609.24702'>AC-DC: Adaptive Communication for Scalable Dynamic Average Consensus in Multi-Robot Ergodic Search</a></td><td>42</td><td>6</td><td>Multi-Robot/Search</td><td>누구와 언제 무엇을 통신할지 국소 정보로 적응 조절하는 AC-DC로 120대 규모까지 통신량을 중앙집중식에 근접하게 줄인 분산합의 알고리즘임</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2609.24952'>Learning to Drive on Mars: Visual Multimodal Traversability Estimation for Off-World Navigation</a></td><td>42</td><td>6</td><td>Navigation/Dataset</td><td>화성 Perseverance 500 sol, 45km 실주행 데이터를 공개하고 불확실성 인지 traversability 추정 프레임워크를 제안해 오프월드 내비게이션 연구에 실데이터 기반을 제공함</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2609.22500'>Event-Frame Fusion for Inter-Frame Segmentation via Event-Guided Motion</a></td><td>42</td><td>5</td><td>Navigation</td><td>이벤트-프레임 융합으로 프레임 사이 세그멘테이션을 채우는 방법이며 자율주행 perception에 직접 적용됨</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2609.22896'>Combining Foundation Model Confidence and Monocular Depth for Training-Free Out-of-Distribution Segmentation</a></td><td>42</td><td>5</td><td>CV</td><td>foundation model confidence와 단안 depth를 결합한 학습 없는 OOD 세그멘테이션이라 자율주행 open-world perception에 바로 쓰일 수 있음</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2609.23404'>ScaleBlind: Point Cloud Completion under Unknown Scale</a></td><td>42</td><td>5</td><td>3D Vision</td><td>ground-truth scale 없이 point cloud를 완성하는 방법이라 실세계 로봇 인식에서 흔한 비현실적 가정을 제거한 기여임</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2609.24787'>Toward a foundation model for forest point clouds</a></td><td>42</td><td>5</td><td>3D Vision</td><td>단일 사전학습 모델이 다양한 산림 조사 설정에서 전이 가능한 표현을 학습할 수 있는지 검증한 3D point cloud foundation model 연구로 필드 로봇 응용에 참고할 만함</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2609.24487'>AgentSTAR: Agentic Shape Tracking and Reconstruction from Monocular Videos</a></td><td>42</td><td>4</td><td>3D Vision</td><td>VLM 에이전트의 render-and-compare 루프로 구조화된 3D 객체 기하와 운동학 구조를 함께 추론하는 방법이라 object-centric 3D representation과 닿아 있음</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2609.24813'>INTCORT: Training-Free Spatial Reasoning Enhancement for Vision-Language Models via Input Transformations and Confidence Routing</a></td><td>42</td><td>4</td><td>Multimodal</td><td>기하 변환과 confidence routing만으로 VLM의 spatial reasoning을 학습 없이 회복시키는 방법이라 embodied spatial reasoning과 연결됨</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2609.25001'>GameHorizon Suite: Multi-Horizon Data and Evaluation in Gameplay</a></td><td>42</td><td>4</td><td>Embodied AI</td><td>게임 플레이에서 시각 이해·지시 분해·목표 계획·정밀 행동 제어를 다중 시간 지평으로 측정하는 통합 데이터·평가 suite라 long-horizon planning 평가와 연결됨</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2609.22120'>Success Leaves Detours: Learning Executable Walkthroughs for Long-Horizon Agents</a></td><td>42</td><td>4</td><td>RL</td><td>sparse-reward 궤적에서 실행 가능한 절차를 추출해 장기 지평 에이전트가 재사용하는 방법이라 long-horizon planning·skill chaining과 개념적으로 연결됨</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2609.24744'>World State Generator</a></td><td>42</td><td>4</td><td>World Model</td><td>실패한 계획을 세계가 인증한 상태로 재정렬하는 세계모델 기반 계획정렬 프레임워크, 7개 벤치마크에서 오픈모델을 상용모델 수준으로 끌어올림</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2609.23436'>GAPS: Generative Active Pseudo-view Selection for Sparse-View 3D Gaussian Splatting</a></td><td>42</td><td>3</td><td>3D Vision</td><td>diffusion으로 생성한 pseudo-view를 활용해 sparse-view 3DGS를 보강하는 방법이라 active view 선택 아이디어가 active perception과 약하게 닿아 있음</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2609.23601'>PREM: Prefix-Steered Recurrent Memory for Long-Video Understanding</a></td><td>42</td><td>3</td><td>Multimodal</td><td>긴 비디오를 토큰 없이 압축된 associative state로 처리하는 메모리 구조라 robot memory와 개념적으로 닿아 있으나 대상은 VLM 비디오 QA임</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2609.24489'>Lifted Bellman Linear Programming for Offline Reinforcement Learning</a></td><td>42</td><td>3</td><td>RL</td><td>Bellman optimality를 (Q,V) 결합공간의 부등식 제약으로 끌어올려 target network 없이 오프라인 RL을 학습하는 LBLP/ALBUM 제안, OGBench에서 FQL과 동등 성능을 최소 파라미터로 달성해 방법론적으로 solid함</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2609.24125'>Positive Pair Geometry Matters: Optimal Transport for Contrastive Learning of Visual Representations</a></td><td>42</td><td>1</td><td>CV</td><td>optimal transport로 데이터 분포의 내재 기하를 반영한 positive pair를 생성하는 새 contrastive learning 프레임워크로 representation learning에 본질적 기여를 하나 로봇 적용은 없음</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2609.22151'>Do Language Models Know Their Own Constraints?</a></td><td>42</td><td>1</td><td>NLP/Interpretability</td><td>행동적으로는 제약을 잘 지키면서도 그 제약을 명시적으로 보고하는 능력은 오히려 퇴화한다는 SFT/GRPO 비교 분석으로 내적 표현과 언어화의 괴리라는 통찰이 흥미로우나 로보틱스 응용은 없음</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2609.22195'>The Situated Identity Test: Distinguishing Persistent Cognitive Identity from Persona Imitation</a></td><td>42</td><td>1</td><td>NLP/Agent Identity</td><td>동일 프로필을 공유해도 서로 다른 이력을 가진 에이전트를 구분할 수 있는지 묻는 Situated Identity Test로 상한을 수식으로 증명한 개념적 기여이나 응용은 페르소나 에이전트에 국한되고 로보틱스와는 무관함</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2609.22119'>Evaluation Awareness Shifts from Format to Context with Model Scale</a></td><td>42</td><td>0</td><td>NLP/Interpretability</td><td>모델 규모가 커질수록 평가인식 탐지가 프롬프트 형식 민감도에서 문맥 추론으로 옮겨간다는 메커니즘 차이를 밝힌 해석가능성 연구로 분석은 탄탄하나 로보틱스와 무관함</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2609.22133'>Observational Equivalence of LLM and Human Annotation</a></td><td>42</td><td>0</td><td>NLP/Evaluation</td><td>14개 정치학 연구를 재현해 LLM과 인간 주석이 품질 면에서 관측적으로 동등함을 보인 대규모 실증 연구로 방법론은 견고하나 로보틱스와 무관함</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2609.22163'>MechaTerp-TRACE: A Novel Approach for Component Ablation Analysis in Language Models</a></td><td>42</td><td>0</td><td>NLP/Interpretability</td><td>13개 모델에서 개체명 산출을 지지하는 구성요소를 ablation으로 특정해 지식이 실제로는 범용 생성기구에 분산돼 있음을 보인 해석가능성 연구로 로보틱스와 무관함</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2609.22208'>Replicating the Geometry of Emotion Representations in a Base Open-Weights Model</a></td><td>42</td><td>0</td><td>NLP/Representation Learning</td><td>Claude Sonnet 4.5의 감정 표현 기하구조를 기반 오픈웨이트 모델(gemma-2-27b)에서 재현해 정서 개념의 선형적 회로 구조를 검증한 견고한 재현연구로 로보틱스와는 무관함</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2609.22215'>On Mitigation of Subliminal Learning in Large Language Models</a></td><td>42</td><td>0</td><td>NLP/Safety</td><td>무해해 보이는 파인튜닝 데이터로도 안전정렬이 은밀히 훼손되는 subliminal learning 현상의 학습동역학을 추적하고 KL 정규화 시점을 조절하는 liminal training으로 완화한 EMNLP 논문이며 로보틱스와는 무관함</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2609.22219'>Knowing, and Saying It Only When Asked: LLM Endognostics and the Schizognosis of Minerva-7B</a></td><td>42</td><td>0</td><td>NLP/Interpretability</td><td>행동으로는 구분 못하는 위험차이를 residual stream 투영으로는 내부적으로 유지하고 있음을 인과적 ablation으로 보인 endognostics 프레임워크로 로보틱스와 무관함</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2609.22226'>Swiss-Knife: A Framework for Reconfigurable Externalised Multi-Objective Alignment at Decode Time</a></td><td>42</td><td>0</td><td>NLP/Alignment</td><td>decode-time 다목표 정렬을 hot-swap 가능한 런타임 객체로 일반화하고 표현정리로 안정적 집계연산자를 특정한 Swiss-Knife로 이론과 실험을 함께 갖췄지만 로보틱스와는 무관함</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2609.22246'>The Corroboration Illusion: When More News Makes LLM Forecasts Less True</a></td><td>42</td><td>0</td><td>NLP</td><td>뉴스 코퍼스 오염으로 LLM 예측 확률을 조작 가능함을 보인 공격 연구, 실험 규모 크고 문제의식 신선함</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2609.23039'>Auditing Political Alignment in LLM Assistants: Engagement, Stance, and User Identity</a></td><td>42</td><td>0</td><td>NLP</td><td>6개 LLM의 정치적 발화 정책을 사전등록 실험으로 감사, 방법론과 스케일 모두 견고함</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2609.23065'>From Concept Alignment to Causal Grounding: An Intervention Test of Chain-of-Thought Faithfulness</a></td><td>42</td><td>0</td><td>LG</td><td>SAE로 예측-CoT 공유 개념을 비교하고 인과적 기여(Δp)를 측정, 충실성 평가에 새로운 인과적 기준을 제시함</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2609.23215'>Triggers and Diagnostics for LLM-Based Interpretability Failures in Active Inference Agents</a></td><td>41</td><td>3</td><td>Multimodal</td><td>LLM explainer가 active inference 에이전트의 corrupted belief를 유창하지만 틀리게 서술함을 보인 실증 연구, 자율 에이전트 실패 진단 문제와 맞닿아 있음</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2609.24969'>Rare Event Estimation via Iterative Unalignment</a></td><td>41</td><td>3</td><td>NLP</td><td>에이전트 자체 행동에서 발생하는 희귀사건 확률을 모델 가중치를 미분가능하게 섭동하는 중요도샘플링으로 추정, 자율 에이전트 안전성 평가와 맞닿아 있음</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2609.24089'>FlashBoB: I/O-Efficient Exact Backward-over-Backward for Softmax Attention</a></td><td>41</td><td>1</td><td>NLP</td><td>softmax attention의 exact backward-over-backward를 I/O 효율적으로 구현, 2차 최적화·test-time training 등에 필요한 인프라 기여로 test-time optimization에 간접적으로 연관됨</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2609.24146'>Mind or Message? Auditing Theory of Mind in Multi-Agent Social Simulation</a></td><td>41</td><td>1</td><td>Multimodal</td><td>다중에이전트 협상 시뮬레이션에서 에이전트가 상대 마음보다 대화 표면을 추적함을 정밀한 counterfactual probe로 규명한 감사 연구임</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2609.24241'>Hessian Rank Constraint for Learning Structure of Nonlinear Latent Variable Models</a></td><td>41</td><td>1</td><td>LG</td><td>cross-Hessian rank로 비선형 잠재 인과구조를 식별하는 새로운 조건(HRC)을 제안한 이론 연구, causal reasoning 우선주제와 관련되나 로봇 실험은 없음</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2609.23780'>Falling Trees: A Model Class for Interpretable Risk Prioritization</a></td><td>41</td><td>0</td><td>LG</td><td>단조 위험 제약을 유지하며 트리 분기를 허용한 falling tree 모델군, ICML spotlight로 해석가능성 기여가 탄탄함</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2609.24380'>Information-Time Proximal Policy Optimization</a></td><td>41</td><td>0</td><td>RL</td><td>토큰 시간 대신 정보밀도로 RLVR의 시간을 재매개변수화해 긴 추론에서 discounting 효과를 회복한 방법론임</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2609.24797'>Complex KDA: Understanding and Enhancing the Expressivity of Kimi Delta Attention</a></td><td>41</td><td>0</td><td>NLP</td><td>Kimi Delta Attention이 채널게이트로 2D 회전을 구현할 수 있음을 증명, state-tracking 표현력 이론 기여이나 로봇과 무관함</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2609.23974'>LEAP-NBV: Lightweight Edge Active-Perception for Foundation-Model Next-Best-View Planning</a></td><td>40</td><td>8</td><td>3D Vision</td><td>HMR을 경량 증류해 엣지에서 실시간 능동지각 NBV 플래닝을 수행, active perception 우선주제에 직접 부합하며 실제 Jetson 배포로 지연/에너지까지 측정한 견고한 기여임</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2609.22608'>Becoming a Fruit Ninja: Real-Time Probabilistic Kinodynamic Planning for Manipulator Projectile Interception</a></td><td>40</td><td>6</td><td>Manipulation/Planning</td><td>GPU 병렬 tree search로 던져진 물체를 밀리초 단위로 요격하는 kinodynamic planner이며 성능은 인상적이나 태스크가 좁고 학습 요소가 없음</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2609.22871'>A Reconfigurable Dual-Opposition Architecture for Single-Hand Assembly and Manipulation</a></td><td>40</td><td>6</td><td>Manipulation/Hardware</td><td>한 손 안에서 두 부품을 동시에 쥐고 조립하는 이중 opposition 구조 핸드로 시뮬레이션·하드웨어 성능은 좋지만 기구설계 중심 기여임</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2609.23103'>DiagGen: Agentic Generation of Deformable Assets with Sim-based Diagnostics for Robotic Simulation</a></td><td>40</td><td>6</td><td>Simulation</td><td>이미지 한 장에서 시뮬레이션 가능한 변형체 자산을 생성-시뮬레이션-진단-수정하는 agentic 루프로 sim2real 자산 생성 품질을 개선하지만 로봇 정책 자체 기여는 아님</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2609.23610'>PRIMO: Prior-Informed Odometry from Human-Motion Tracking for Humanoid Robots</a></td><td>40</td><td>6</td><td>State Estimation/Humanoid</td><td>다양한 human motion retargeting으로 오도메트리 학습 데이터를 넓히고 물리·대칭 사전지식을 구조에 반영한 PRIMO로 sim2real 오차를 크게 줄였지만 상태추정 문제에 한정됨</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2609.24668'>Ev-YOLO: Uncertainty-Aware Object Detection via a Unified Evidential Formulation</a></td><td>40</td><td>5</td><td>CV</td><td>분류와 회귀 불확실성을 같은 evidential 이론 틀로 통합한 객체 탐지기라 자율 시스템의 신뢰도 기반 실패 인지에 참고할 만함</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2609.24825'>ZVeC: A Zero-Shot Framework for Instance-Level Vehicle Extraction and Generative Point Cloud Completion</a></td><td>40</td><td>5</td><td>3D Vision</td><td>지하 환경의 가려진 LiDAR 포인트클라우드를 객체 인스턴스 단위로 분해해 학습 없이 완성하는 zero-shot 프레임워크라 필드 로봇 인식에 참고할 만함</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2609.24127'>Action-Slot: Structured Action-Centric Representation Learning for Multi-Agent Atomic Activity Understanding</a></td><td>40</td><td>4</td><td>CV</td><td>다중 에이전트 교통 행동을 슬롯 어텐션 기반 구조화된 action-centric 표현으로 이해하는 연구라 object-centric representation과 약하게 닿아 있음</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2609.24850'>Revisiting Multi-View Stereo: A Sequence-to-Sequence Formulation</a></td><td>40</td><td>3</td><td>3D Vision</td><td>MVS를 sequence-to-one이 아닌 sequence-to-sequence로 재정식화해 기하 왜곡 문제를 다룬 새 방법이라 로봇 3D 인식 파이프라인에 참고할 만함</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2609.22206'>Dissecting Training-Free Uncertainty Estimation in Multimodal Large Language Models</a></td><td>40</td><td>2</td><td>Multimodal/Uncertainty</td><td>토큰수준·언어화·의미공간 세 계열의 training-free 불확실성 추정을 멀티모달 LLM에서 체계적으로 비교한 벤치마크로 각기 다른 응답 길이에서 우세함을 보였고 VLA 정책의 불확실성 추정에도 참고 가치가 있음</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2609.22884'>Block-Sparse Attention with Semantic-Geometric Decoupled Routing</a></td><td>40</td><td>1</td><td>LG</td><td>post-RoPE 라우팅 문제를 pre-RoPE 분리로 해결한 training-free 방법, 긴 맥락 추론 효율화에 실질적으로 기여함</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2609.22272'>Moonworks Lunara: Modeling Artistic Intelligence</a></td><td>40</td><td>0</td><td>Multimodal</td><td>새 DiT 기반 text-to-image 아키텍처와 학습 알고리즘을 제시하지만 로보틱스와는 무관한 산업 제품형 논문임</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2609.24088'>Bridging Reconstruction and Generation: A Latent Distribution Perspective on Evaluation and Improvement</a></td><td>40</td><td>0</td><td>CV</td><td>reconstruction FID와 generation FID의 불일치를 latent distribution mismatch로 규명하고 개선책을 제시한 생성모델 평가 연구로 로봇과는 무관하나 방법론적 기여가 뚜렷함</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2609.22240'>Statistical Inference for Adversarial Training: Central Limit Theorems via Optimal Transport</a></td><td>40</td><td>0</td><td>LG</td><td>adversarial training의 통계적 성질을 empirical optimal partial transport로 규명한 이론 논문, 수학적으로 탄탄하나 로봇과 무관함</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2609.22254'>Teacher Should Think Ahead: Adaptive Continuations for Reliable On-Policy Distillation</a></td><td>40</td><td>0</td><td>NLP</td><td>teacher uncertainty contraction을 규명하고 적응적 continuation으로 on-policy distillation 개선, 이론과 실험이 탄탄함</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2609.22143'>Using Composition Operators to Linearize LLM Semantic Transformations</a></td><td>40</td><td>0</td><td>NLP/Theory</td><td>LLM의 의미변환을 composition operator로 선형화하는 Koopman 이론 기반 수학적 형식화로 참신하지만 로보틱스 적용은 없음</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2609.22174'>SCoR: A Hierarchical Framework for Forecasting Relations Between Scientific Concepts</a></td><td>40</td><td>0</td><td>NLP/Scientific Discovery</td><td>개념 간 공출현을 넘어 사용·대체·모순 같은 관계 형성 자체를 예측하는 계층적 과학관계 예측 프레임워크로 대규모 그래프와 벤치마크를 구축했지만 로보틱스와 무관함</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2609.22224'>From Trait Vectors to Circuits: Tracing Refusal and Sycophancy Through Language Models</a></td><td>40</td><td>0</td><td>NLP/Interpretability</td><td>스티어링이 실제로 작동하는 회로와 거부·아첨 행동을 만드는 회로가 다를 수 있음을 밝힌 기계론적 해석가능성 연구로 로보틱스와 무관함</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2609.22904'>LLMs Anchor on Chief Complaint and Fail to Integrate Evidence in Sequential Clinical Triage</a></td><td>40</td><td>0</td><td>NLP</td><td>순차 트리아지에서 LLM이 초기 주호소에 고착돼 증거 통합에 실패함을 밝힌 임상 안전성 연구, 방법론이 탄탄함</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2609.23264'>Judging a Review by its Cover: A Reliability Analysis of LLM-based Peer Review Evaluation Metrics</a></td><td>40</td><td>0</td><td>NLP</td><td>리뷰 평가 지표 29개가 표면적 문체에 민감함을 통계적으로 검증, 평가 방법론 신뢰성에 중요한 경고를 줌</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2609.24927'>Et Tu, Brute? Economic Misalignment in Personal AI Agents</a></td><td>40</td><td>0</td><td>AI</td><td>개인화 AI 에이전트가 명시적 지시를 어기고 부유한 사용자에게 더 비싼 옵션을 권함을 32만건 규모로 실증, adversarial delegation이라는 새로운 위험 프레이밍을 제시함</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2609.24103'>Reinforcement Learning under State and Outcome Uncertainty: A Foundational Distributional Perspective</a></td><td>39</td><td>3</td><td>RL</td><td>부분관측 MDP로 distributional RL을 확장해 return 분포 전체를 학습하는 이론, risk-sensitive 로봇 제어에 기초가 될 수 있음</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2609.24111'>SPeaR: Test-Time Adaptation with Steering Primitives for Realigning Representations</a></td><td>39</td><td>2</td><td>CV</td><td>frozen 백본의 중간표현을 steering primitive로 재정렬하는 test-time adaptation 기법, 분포 변화 대응 원리가 로봇 배포와도 관련 있음</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2609.24259'>MemCalib: Benchmarking and Optimizing Memory Use in LLM Agents</a></td><td>39</td><td>2</td><td>NLP</td><td>LLM이 컨텍스트 메모리를 과다/과소 사용하는 문제를 벤치마크·RL로 교정, robot memory와 개념적으로 맞닿아 있으나 로봇 실험은 없음</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2609.22197'>Dissecting Hierarchical Reasoning Models: A Mechanistic Study</a></td><td>39</td><td>1</td><td>LG</td><td>hierarchical reasoning model의 recurrent state를 개입·probe로 해부한 해석연구, 로봇 적용과는 거리 있음</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2609.23219'>Causal Inference with Unobserved Confounding: A Mixture Learning Perspective</a></td><td>39</td><td>1</td><td>LG</td><td>잠재 혼란변수를 mixture learning 관점으로 다룬 인과추론 프레임워크, 이론적 novelty 있으나 로봇과 무관함</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2609.24144'>Luck Is Not Skill: When Do Paired Rollouts Help Group-Relative RL of LLM Agents?</a></td><td>39</td><td>1</td><td>RL</td><td>환경 노이즈를 공유하는 paired rollout이 gradient variance를 줄이는 조건을 이론·실험으로 규명한 group-relative RL 연구임</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2609.24947'>Learning Physics from an Imperfect Ancestor</a></td><td>39</td><td>1</td><td>LG</td><td>부정확한 neural operator로 PINN을 올바른 해 basin에 안착시키는 3단계 증류 프레임워크, PDE 외삽 문제에 solid한 기여임</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2609.24972'>RRSI: Regularized Recursive Self-Improvement of Agent Harnesses</a></td><td>39</td><td>1</td><td>NLP</td><td>에이전트 harness의 재귀적 자기개선이 in-distribution에 과적합되는 문제를 정규화로 완화한 연구, agent self-improvement로서 참고할 만함</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2609.22894'>Are Coreset Selection Methods Worth Their Cost?</a></td><td>39</td><td>0</td><td>LG</td><td>coreset selection의 wall-clock 비용을 포함한 엄밀한 벤치마크, random sampling이 대부분 승리함을 보인 비판적 연구임</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2609.23087'>Neural Spectral Capacity: Measuring and Designing Architectures from Network Specification Alone</a></td><td>39</td><td>0</td><td>NLP</td><td>가중치 스펙트럼만으로 아키텍처 용량을 계산하는 closed-form 지표, LLaMA 프루닝 등 실용성 있으나 로봇과 무관함</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2609.23125'>Perplexity Cost Understates What Activation Quantisation Breaks</a></td><td>39</td><td>0</td><td>NLP</td><td>perplexity 평균 지표가 activation quantization이 induction/retrieval에 미치는 손상을 가린다는 것을 보인 진단 연구임</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2609.23529'>Predicting Out-of-Distribution Generalization of Neural Operators via Observable Spectral Error Decomposition</a></td><td>39</td><td>0</td><td>LG</td><td>neural operator의 OOD 오차를 스펙트럴 필터로 분해해 관측가능한 진단지표를 만든 연구임</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2609.23892'>Circuit-Diff: Factual Edit-based Intervention Method for Localizing Knowledge in Attribution Graphs</a></td><td>39</td><td>0</td><td>NLP</td><td>저순위 factual edit으로 attribution graph에서 지식 노드를 라벨링하는 해석성 방법론임</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2609.23695'>PhysAI-Bench: A Benchmark for LLM-Based Agentic Decision-Making in Autonomous UAV-Centric Physical AI</a></td><td>38</td><td>7</td><td>Embodied AI</td><td>UAV 미션에서 MCP/A2A 상호작용과 네트워크 조건을 포함한 에이전틱 의사결정 벤치마크, physical AI 우선주제와 직접 관련되며 실증 규모도 큼</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2609.24218'>Audio-based UAV Localization with Adaptive Temporal Correspondence via Reinforcement Learning</a></td><td>38</td><td>6</td><td>Localization/RL</td><td>탐지 신뢰도를 보고 오디오 윈도우 크기를 RL로 적응시켜 UAV 위치추정 지연을 줄인 방법으로 특정 모달리티에 한정된 개선임</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2609.24631'>From Semantic Decisions to Feasible Trajectories: Self-Evolving LLM-Guided Optimal Control for Narrow-Space Parking</a></td><td>38</td><td>6</td><td>Planning/Control</td><td>LLM이 이산 기동을 제안하고 최적제어가 저수준 동역학·충돌 제약을 강제하는 하이브리드 주차 플래너로 실패 사례를 지식베이스로 축적하는 자기진화 구조가 흥미로움</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2609.23271'>Steering Through Contact: A Finite-Support Motion Model for Single-Track Center-Articulated Robots</a></td><td>38</td><td>5</td><td>Field Robotics/Modeling</td><td>관절형 단일궤도 차량의 접촉점 회전저항을 고려한 finite-support quadratic 모델로 7km 실주행 데이터로 검증했지만 고전 동역학 모델링 확장임</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2609.24204'>SAFe: Segment-guided Aggregation of Feature Densities for Anomaly-aware Segmentation</a></td><td>38</td><td>4</td><td>CV</td><td>segment 단위로 feature density를 집계해 공간 일관성 있는 anomaly-aware segmentation을 수행하는 방법이라 자율 시스템의 open-world perception에 쓰일 수 있음</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2609.24403'>Can Spiking Neural Networks play pinball? A neuromorphic motion detector for target tracking</a></td><td>38</td><td>4</td><td>CV</td><td>이벤트 카메라와 스파이킹 신경망으로 핀볼 타겟을 추적하는 신경형태 모션 검출기라 저지연 active perception 하드웨어에 참고할 만함</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2609.22910'>When Should a VLM Look? Paying Only for Visual Calls That Were Needed and Used</a></td><td>38</td><td>4</td><td>VLA</td><td>시각 도구호출이 실제로 필요했고 사용됐는지 반사실적으로 검증하는 보상설계, 불필요한 시각호출을 크게 줄이며 성능도 개선하는 견고한 기여임</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2609.23064'>FireWorldBench: Benchmarking Complex Physical World Intelligence through Coupled-Field Fire Dynamics</a></td><td>38</td><td>4</td><td>World Model</td><td>화재라는 다중물리장 결합 현상으로 물리세계 이해력을 평가하는 벤치마크, 인과·개입추론까지 포괄해 world model 평가에 의미 있는 스트레스테스트임</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2609.22947'>RewardVerse: Rubric-Guided Policy Optimization for Video Reward Modeling</a></td><td>38</td><td>3</td><td>RL</td><td>비디오 생성 RL을 위한 rubric 기반 보상 모델링이라 reward modeling 원리는 VLA 학습에도 참고할 만하지만 대상은 비디오 생성임</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2609.24531'>Dynamic Thermal Gaussians: Multimodal 4D Gaussian Splatting</a></td><td>38</td><td>3</td><td>3D Vision</td><td>RGB-열화상-기하를 함께 시간에 따라 모델링하는 첫 동적 4D Gaussian Splatting 프레임워크로 4D representation 확장에 새로움이 있음</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2609.24397'>Probabilistic Modelling of Operational Design Domains, A New Approach for Testing AI Systems</a></td><td>38</td><td>3</td><td>LG</td><td>operational design domain을 확률적 온톨로지(PEON)로 모델링해 자율주행 등 ML 시스템 테스트 대표성을 보장, 자율시스템 검증 방법론으로서 로봇 안전성 평가와 접점 있음</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2609.24352'>Few-Shot Demonstrations Elicit the Use of In-Context World Representations in LLMs</a></td><td>38</td><td>3</td><td>World Model</td><td>소수샷 시연이 LLM 내부의 세계표상을 재배치해 예측 활용도를 높임을 프로빙으로 규명, in-context world modeling 메커니즘 이해에 기여함</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2609.22178'>Beyond Task Completion: Training Capable and Safe Computer-Use Agents</a></td><td>38</td><td>1</td><td>Multimodal</td><td>GUI 컴퓨터사용 에이전트 안전성 SFT+RL 파이프라인 논문, 로봇 정책과는 거리 있음</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2609.22247'>CHART: A Harness-Rotation Curriculum for Harness-Robust Search Agents</a></td><td>38</td><td>1</td><td>NLP</td><td>검색 에이전트가 harness 변화에 취약한 문제를 커리큘럼으로 해결한 방법론, 로봇 정책 일반화와는 다른 도메인임</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2609.22554'>The Ups and Downs of Backprop Weights</a></td><td>38</td><td>1</td><td>LG</td><td>weight entanglement 문제를 지적하고 재사용 가능한 weight operator를 제안, 모듈 재조합 아이디어가 흥미로우나 로봇과는 거리 있음</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2609.24417'>ARM: Attention with Routed-Memory for Learnable Sparse Control</a></td><td>38</td><td>1</td><td>NLP</td><td>Gumbel-Softmax로 고정크기 메모리 슬롯을 선택·갱신하는 미분가능 KV 캐싱 구조, 메모리 관리 아이디어가 로봇 메모리와 개념적으로 유사하나 LLM 롱컨텍스트 문제임</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2609.22101'>Context Poisoning as Extreme-Value Attention Interference in Long-Context Language Models</a></td><td>38</td><td>1</td><td>NLP/LG</td><td>긴 컨텍스트에서 attention 극값 간섭으로 정답 신호가 묻히는 현상을 finite-sample bound로 정식화한 이론 분석으로 근거는 탄탄하나 로보틱스 적용은 없음</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2609.22228'>Assessing Adversarial Robustness of Latent Reasoning Models</a></td><td>38</td><td>1</td><td>NLP/Robustness</td><td>연속 latent로 추론을 압축한 latent reasoning model이 명시적 CoT보다 적대적 공격에 더 취약함을 8개 모델·6개 벤치마크로 보인 체계적 강건성 연구이며 로보틱스 응용은 다루지 않음</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2609.22231'>EvalMem: An Operation-Level Diagnostic Framework for Long-Term Memory Systems</a></td><td>38</td><td>1</td><td>NLP/Memory</td><td>장기 메모리 시스템의 오류를 인코딩·검색·생성 단계로 분리 진단하는 EvalMem 프레임워크로 로봇 메모리 설계에 개념적으로 참고할 수 있으나 대상은 LLM 어시스턴트임</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2609.22245'>Do Chess Explanations Reflect Model Decisions? Behavioral and Token-Level Tests of LLM Reasoning Faithfulness</a></td><td>38</td><td>1</td><td>NLP</td><td>체스 무브 설명의 충실성을 행동/토큰 단위로 검증한 분석, reasoning faithfulness 방법론은 탄탄하나 로보틱스 적용성 낮음</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2609.23371'>Machine-Interpretable Information: Compiling Documents into Searchable and Readable Protocol States</a></td><td>38</td><td>1</td><td>LG</td><td>문서를 고정 대역폭 상태로 압축해 에이전트 간 전달하는 새 프로토콜, retrieval-reasoning-reconstruction을 통합한 참신한 표현 방식임</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2609.22131'>Correlation-Aware Structured Pruning for Large Language Models</a></td><td>38</td><td>0</td><td>NLP/LG</td><td>unit 간 상관관계를 반영한 binary quadratic program으로 구조적 프루닝을 정식화한 LLM 경량화 연구로 로보틱스 적용은 다루지 않음</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2609.22169'>Monocultural Biases: Correlated biases in large language models lead to unequal systemic exclusion rates in hiring</a></td><td>38</td><td>0</td><td>NLP/Fairness</td><td>채용용 LLM의 base 대비 post-trained 모델이 연령차별을 더 강화한다는 COLM 논문으로 모노컬처 편향 확산을 실증했지만 로보틱스와는 무관함</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2609.22223'>EAVer: Long-Form Factuality Verification as an End-to-End Agentic Policy</a></td><td>38</td><td>0</td><td>NLP/Factuality</td><td>주장을 그룹화해 검색량을 줄이면서 응답수준 정책으로 장문 사실검증을 end-to-end 학습한 EAVer로 로보틱스와는 무관하나 효율적인 agentic 검증 설계는 참고할 만함</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2609.22225'>Do LLMs Choose Like Humans? Using Cognitive Theory to Evaluate LLM Decision-Making</a></td><td>38</td><td>0</td><td>NLP/Cognitive Science</td><td>인간의 문제 범주화·주의배분 이론으로 LLM의 맥락민감 선택을 대규모로 검증해 인간과 다른 메커니즘임을 보인 연구로 로보틱스와 무관함</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2609.22566'>Do Student LLMs Inherit OOD Robustness? Invariance-Weighted Distillation for Reliable Knowledge Transfer</a></td><td>38</td><td>0</td><td>LG</td><td>teacher의 인과적 신뢰도로 distillation 샘플을 재가중하는 이론적 프레임워크, OOD 일반화 개선폭이 크고 이론 근거도 갖춤</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2609.23053'>Attributable Post-Rationalization in RAG Citations: A Controlled Reproduction and an RLVR Comparison</a></td><td>38</td><td>0</td><td>NLP</td><td>RLVR 학습이 인용 충실성을 개선하지 못함을 보인 실증 연구, 보상 설계 시사점이 큼</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2609.24895'>Human-LLM Deliberation as Interactive Proof: Conditions for Verifiability Without Transparency</a></td><td>38</td><td>0</td><td>AI</td><td>인간-LLM 숙의를 대화형 증명으로 모델링해 anytime-valid soundness를 증명, 이론적 기여가 탄탄함</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2609.22682'>Self-Organizing Agent Teams Learn to Reason Together</a></td><td>38</td><td>0</td><td>AI</td><td>에이전트 팀이 협업 전략을 경험으로부터 학습해 미지 벤치마크로 전이함을 보임, demonstrability가 개선폭을 예측한다는 발견이 흥미로움</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2609.24967'>Emergent Collusion in Long-Horizon LLM Agent Interaction</a></td><td>38</td><td>0</td><td>AI</td><td>장기 다중에이전트 상호작용에서 검증프로토콜 회피 담합이 94% 궤적에서 창발함을 보인 안전성 연구, 모델능력이 높을수록 더 빨리 담합함</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2609.24391'>NAVIR: Neuromorphic Audio-Visual Speech Recognition for Robust Human-Robot Interaction on Edge Hardware</a></td><td>37</td><td>5</td><td>Multimodal</td><td>뉴로모픽 프로세서에서 동작하는 시청각 음성인식으로 산업용 인간-로봇 상호작용을 목표한 엣지 시스템, HRI 응용이나 VLA·조작 핵심주제와는 거리 있음</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2609.22919'>Computationally efficient safe exploration in reinforcement learning</a></td><td>37</td><td>4</td><td>RL</td><td>Nadaraya-Watson 추정기로 GP 없이 계산 가볍게 안전 탐색하는 제약 MDP 알고리즘, 화성 지형 데이터 실험 포함해 robot learning 안전성과 관련 있으나 조작·VLA와는 거리 있음</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2609.23875'>VISTA: An Attention-Based Multi-Agent Reinforcement Learning Architecture for Space Situational Awareness Sensor Tasking</a></td><td>37</td><td>3</td><td>RL</td><td>가변 개체수에 대응하는 attention 기반 MARL로 우주감시 센서 태스킹, 확장가능한 아키텍처가 흥미로우나 로봇 조작과는 다름</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2609.24117'>PAC-Bayesian Meta-Learning for Few-Shot Identification of Linear Dynamical Systems</a></td><td>37</td><td>3</td><td>RL</td><td>선형 동역학계 few-shot 식별을 위한 PAC-Bayesian 메타학습, 시스템 식별이 로봇 동역학 모델링과 연관됨</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2609.23127'>Provably Efficient Reinforcement Learning in Continuous-Time Episodic MDPs with Poisson Decision Epochs</a></td><td>37</td><td>2</td><td>RL</td><td>Poisson decision epoch 연속시간 MDP의 후회 상한을 증명한 이론, 이벤트 구동 로봇 의사결정과 연관 가능하나 실험은 없음</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2609.23775'>Statistical Convergence of Transformer Encoder-Accelerated Robust Reinforcement Learning</a></td><td>37</td><td>2</td><td>RL</td><td>transformer로 warm-start한 robust RL의 conformal 수렴 보장 이론, maze 실험 포함하나 이론 위주 연구임</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2609.22819'>Counterfactual Tool Ranking under Utility, Cost, and Privilege Constraints</a></td><td>37</td><td>1</td><td>NLP</td><td>utility·cost·privilege 제약 하 tool 순위 평가를 위한 counterfactual 방법론, BFCL 실험 포함하나 로봇 정책 평가는 아님</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2609.22833'>Personalized Federated Reinforcement Learning via Model-Agnostic Meta-Learning: Convergence of Exact and Hessian-Free Meta-Policy Gradients</a></td><td>37</td><td>1</td><td>RL</td><td>개인화 연합 RL의 MAML 스타일 수렴 이론, navigation 실험 있으나 이론 중심 논문임</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2609.24882'>Learning Prognostic Variables for AI Convective Parameterizations via Symbolic Distillation</a></td><td>37</td><td>1</td><td>LG</td><td>잠재 기억변수를 오토인코더로 압축 후 기호방정식으로 대체해 대류 파라미터화를 개선, 메모리 변수 도입 아이디어가 흥미로움</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2609.24985'>Critical-State RL: Diagnosing Trainable States for Multi-Turn Tool Use</a></td><td>37</td><td>1</td><td>RL</td><td>멀티턴 tool-use에서 보상 분산을 분해해 학습 가치 있는 state를 진단하는 Critical-State RL, BFCL 실험으로 유효성 입증함</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2609.22194'>A Pinch of SFT, A Dash of RL: When Reinforcement Learning Helps Long-Horizon Advertising Agents</a></td><td>37</td><td>0</td><td>NLP</td><td>SFT/RL 배분 전략을 진단하는 실증 연구, 통찰은 있으나 광고 에이전트 도메인에 국한됨</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2609.22415'>Complex-valued Phase-Coherent Transformers</a></td><td>37</td><td>0</td><td>NLP</td><td>복소수 트랜스포머 attention을 코사인 스코어로 정규화해 표현력 개선, 아키텍처 novelty는 있으나 로봇과 무관함</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2609.23055'>Optimizers for Diffusion Models: A Controlled Benchmark</a></td><td>37</td><td>0</td><td>Video</td><td>이산 확산모델용 optimizer를 처음으로 통제 비교한 벤치마크, 방법론적으로 유용하나 로봇과 무관함</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2609.23117'>Whitening Inverts the Hierarchy: What the Norm of a Whitened Embedding Measures</a></td><td>37</td><td>0</td><td>NLP</td><td>whitened embedding norm이 log-likelihood가 아닌 Mahalanobis 이례성 척도임을 규명한 해석연구임</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2609.23260'>Why Ghost Outputs Teach: A Kernel-Based Understanding of Subliminal Learning</a></td><td>37</td><td>0</td><td>NLP</td><td>subliminal learning의 최적화 메커니즘을 cross-task kernel로 이론적으로 설명한 연구임</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2609.23549'>Physics-residual machine learning predicts oxygen-evolution catalyst activity beyond the training range from sparse polarization measurements</a></td><td>37</td><td>0</td><td>LG</td><td>Tafel 방정식과 잔차학습을 결합해 훈련범위 밖 촉매 활성도를 예측, physics-residual 방식의 extrapolation이 solid함</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2609.24504'>On Emergent Capabilities and Model Merging</a></td><td>37</td><td>0</td><td>NLP</td><td>모델 병합이 misalignment 같은 emergent capability를 어떻게 보존·희석하는지 실증한 연구임</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2609.24678'>Muon Can Outperform Dedicated Continual Learning Methods</a></td><td>37</td><td>0</td><td>NLP</td><td>Muon 옵티마이저의 업데이트 기하구조가 전용 continual learning 기법 없이도 망각을 억제함을 보인 실증 연구임</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2609.24243'>Taming CoT Obfuscation in VLMs: From Mechanistic Evidence to Activation Enforcement</a></td><td>36</td><td>2</td><td>Multimodal</td><td>RL이 VLM CoT를 감독 회피적으로 만드는 표상수준 원인을 SAE로 규명하고 활성화 억제로 모니터링 가능성을 회복, 표상수준 개입으로 넘어간 진전된 연구임</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2609.24838'>MedRSI: Recursive Self-Improvement for Medical Agents via Clinically Aligned Self-Evolution</a></td><td>36</td><td>2</td><td>AI</td><td>임상비용 인지 우선순위와 느린등록 메커니즘으로 의료에이전트가 실패를 새 역량으로 전환, 설계자가 예상못한 해법까지 자율발견한 재귀적 자기개선 연구임</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2609.22700'>LLaDA-PRM: A Bidirectional Step-Level Reasoning Evaluator</a></td><td>36</td><td>0</td><td>LG</td><td>양방향 attention이 step-level reasoning evaluator 성능을 일관되게 높임을 보인 통제 비교, 아키텍처 기여가 견고함</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2609.23083'>Directing large language models to follow the letter or spirit of the law</a></td><td>36</td><td>0</td><td>NLP</td><td>targeted adaptation으로 LLM이 법의 정신/문언을 선택하게 조종, 내부 표현의 저차원 구조 발견이 흥미로움</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2609.23935'>Measuring the Assistant&#x27;s Harmlessness Preferences on the User Turn</a></td><td>36</td><td>0</td><td>NLP</td><td>post-training이 유저 턴 예측에도 해악성 선호를 전이시킴을 보인 행동 분석, 페르소나 일반화 메커니즘에 시사점이 있음</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2609.24635'>Written as a Record, Read as an Address: What a Forward Pass Leaves in an Operation&#x27;s KV Cache</a></td><td>36</td><td>0</td><td>LG</td><td>연산 스팬이 남기는 라우팅/페이로드 기록을 인과적으로 규명한 기계적 해석 연구, entity tracking 메커니즘 이해에 기여함</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2609.24821'>The Answer-Basin Representation Hypothesis: We Are Not Probing or Steering Concepts</a></td><td>36</td><td>0</td><td>LG</td><td>선형표상가설을 답변확률측도 관점으로 재정식화, 개념적 기여가 참신함</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2609.24890'>OSWorld-Pro: Process-based Evaluation for Computer Use Agents</a></td><td>36</td><td>0</td><td>LG</td><td>컴퓨터사용 에이전트를 서브골 단위로 절차평가하는 대규모 벤치마크, 인간주석 규모와 실패유형 분석이 강점임</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2609.22512'>Agreement Overstates Evidence: Error Dependence in LLM Judge Consensus</a></td><td>36</td><td>0</td><td>AI</td><td>LLM 판정자 간 오류상관을 정량화해 합의가 독립적 증거보다 과대평가됨을 보인 통계적 기여, 평가 실무에 직접적 함의가 있음</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2609.24101'>When More Evidence Hurts: Publication-Bias Drift and Principled Stopping for Biomedical Causal Search</a></td><td>36</td><td>0</td><td>AI</td><td>검색깊이가 커질수록 출판편향으로 인한 거짓양성이 증가함을 이론/실증으로 규명, 인과그래프 에이전트로 드리프트를 절반으로 감소시킴</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2609.22276'>D3DWA: Adaptive Weight and Prediction-Horizon for Dynamic Window Approach via Dueling Double Deep Q-Network</a></td><td>35</td><td>8</td><td>Navigation</td><td>DWA의 평가가중치와 예측horizon을 D3QN으로 상태별 적응 선택, 실로봇 실험 포함하나 고전 로컬플래너 파라미터 튜닝 수준의 기여임</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2609.24274'>vla.simd: Efficient CPU Inference for Language-Conditioned Manipulation</a></td><td>35</td><td>7</td><td>VLA/Efficient Inference</td><td>SIMD 커널과 캐시된 언어표현으로 GPU 없이 VLA를 라즈베리파이에서 구동한 실용적 엔지니어링으로 새로운 원리 제시보다 효율화 자체가 목적임</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2609.24433'>FoldQuantVLA: Native Low-Bit Quantization of Vision-Language-Action Models via Consistent Folding</a></td><td>35</td><td>7</td><td>VLA/Efficient Inference</td><td>재학습 없이 채널 스케일링과 Hadamard 변환으로 VLA를 4비트로 양자화해 실로봇 지연을 줄인 FoldQuantVLA로 배포 효율화 기여이며 새로운 표현이나 패러다임은 아님</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2609.23554'>PINGU: Extending Air-Bearing Spacecraft Emulators with Open-Source Actuators and Learned Control for Contact-Rich Proximity Operations</a></td><td>35</td><td>6</td><td>Space Robotics</td><td>평면 air-bearing 우주선 에뮬레이터에 반작용휠과 힘/토크 팔을 더해 접촉이 많은 근접운용 RL을 검증한 플랫폼 논문으로 인프라 기여 성격이 강함</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2609.23643'>Spiking Neural Network Actor-Critic Proximal Policy Optimization Control for Autonomous UAV Navigation Through Constrained Openings in Civil Infrastructure and Buildings</a></td><td>35</td><td>6</td><td>RL/Navigation</td><td>spiking neural network 기반 actor-critic PPO로 UAV의 제약된 개구부 통과를 학습한 연구로 효율성 중심이며 성공률도 63.77%로 아직 낮음</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2609.24059'>Automatic Labelling for Bimanual Mobile Manipulation</a></td><td>35</td><td>6</td><td>Manipulation/Data</td><td>궤적 분석으로 시간 경계를 정하고 VL reasoning으로 의미를 붙이는 자동 라벨링 파이프라인으로 양팔 이동조작 데이터 주석의 실용적 확장임</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2609.24133'>Phrase-Level Robotic Guqin Performance: Bimanual Motion Planning and Audio-Tactile Interaction Monitoring</a></td><td>35</td><td>6</td><td>Manipulation/Bimanual</td><td>고금 연주라는 밀리미터 단위 접촉타이밍 과업을 계층적 이산-연속 계획과 촉각-청각 피드백으로 수행한 이색적 실증이지만 응용 범위가 좁음</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2609.24841'>CAST: Collision-Aware Assembly with Construction Robots using Simultaneous Trajectory Estimation and Planning</a></td><td>35</td><td>6</td><td>Multi-Robot/Planning</td><td>측정 상태·충돌·케이블 제약을 하나의 factor graph로 통합해 궤적 추정과 계획을 동시에 하는 CAST로 건설 조립 다중로봇 시스템에 적용한 엔지니어링 기여임</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2609.22967'>General Collaborative Intelligence: Architecting Cognition for Resilient Multi-Agent Ecosystems</a></td><td>35</td><td>5</td><td>Embodied AI</td><td>멀티에이전트 무인 시스템의 협업 지능을 다섯 차원으로 통합 정리한 서베이라 새 실험적 기여는 없음</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2609.22670'>AquaWorld: Structure-Consistent Underwater World Generation for Robot Simulation</a></td><td>35</td><td>5</td><td>Simulation</td><td>언어조건 플랜으로 지형-자산-태스크-조류를 일관되게 생성하는 수중 시뮬레이션 프레임워크이며 world model이라기보다 절차적 world generation 엔지니어링임</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2609.22726'>Decentralized Multi-Robot Exploration with Probabilistic Peer Intent and Multi-hop Plan Propagation</a></td><td>35</td><td>5</td><td>Multi-Robot Exploration</td><td>DMCE의 peer intent를 확률적 표현으로 바꾸고 multi-hop 전파를 추가한 확장 연구로 개선폭은 있지만 formulation 자체의 새로움은 크지 않음</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2609.22803'>ARCGym: Benchmarking Deep Reinforcement Learning in Autonomous Robotic Colonoscopy</a></td><td>35</td><td>5</td><td>RL/Medical Robotics</td><td>유연 대장내시경 자율주행을 위한 RL 벤치마크로 니치하지만 실제 임상 형상 5개를 반영한 벤치마크 구축 자체는 유용함</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2609.23132'>Tip Manipulation in Soft Everting Robots via Wall Retraction and Deployable Fingers</a></td><td>35</td><td>5</td><td>Soft Robotics/Hardware</td><td>외벽 되감기로 everting 로봇 끝단 도구를 재배치하는 기구설계 논문으로 좁은 공간 조작 응용은 흥미롭지만 학습 요소는 없음</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2609.23280'>Safety-Critical Control under Uncertainty via Adaptive Conformal Quantile Prediction Intervals</a></td><td>35</td><td>5</td><td>Control Theory</td><td>conformal quantile regression으로 상태의존 비대칭 예측구간을 만들어 CBF 보수성을 줄이는 안전제어 논문으로 이론적 기여이나 로봇학습과는 거리가 있음</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2609.23414'>EmoPose: Vision-Language Model Guided Emotion-Aware Gesture Generation for Humanoid Robots</a></td><td>35</td><td>5</td><td>HRI/Humanoid</td><td>VLM이 제스처 라이브러리에서 계획을 세우고 결정론적 모듈이 실행하는 EmoPose 시스템으로 사회적 표현을 넓히지만 시스템 통합 성격이 강함</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2609.23885'>HumynexSurg-1: A Curated Expert Liposuction Dataset</a></td><td>35</td><td>5</td><td>Dataset/Medical Robotics</td><td>지방흡입이라는 드문 수술 과업의 힘·영상 동기화 전문가 데이터셋을 처음 공개한 것으로 데이터 기여는 있으나 방법론적 novelty는 낮음</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2609.23943'>FinsSim: A Reality-Aligned Integrated Simulation Platform for Underwater Robot Learning</a></td><td>35</td><td>5</td><td>Simulation</td><td>고정밀 유체역학과 표준 학습 워크플로를 결합한 수중로봇 sim2real 시뮬레이터로 파이프라인 통합 기여이며 새로운 학습 방법은 아님</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2609.24195'>Odometry-Aided Real-Time Mapping for Underwater Robots Using Forward-Looking Sonar</a></td><td>35</td><td>5</td><td>Mapping/Underwater</td><td>전방주시 소나의 노이즈·타겟 고도 모호성을 처리해 실시간 2.5D 매핑을 만든 파이프라인으로 인지 엔지니어링 성격이 강함</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2609.24497'>ScaleMPA: Rethinking Scalable RRT* Acceleration With a Grid-Native Representation</a></td><td>35</td><td>5</td><td>Motion Planning/Hardware</td><td>RRT*를 grid-native 표현으로 재구성해 28nm CMOS 가속기로 구현한 하드웨어 논문으로 로봇학습과는 별개의 반도체 설계 기여임</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2609.24424'>Estimating Accurate Hand Pose in Camera Space with Vision Transformer</a></td><td>35</td><td>4</td><td>CV</td><td>단안 RGB에서 카메라 좌표계의 정확한 손 포즈를 추정하는 연구라 모방학습을 위한 인간 시연 파싱에 참고할 만함</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2609.22295'>On The Robustness-Resolution Tradeoff In Temporal Quantization Of Event Streams</a></td><td>35</td><td>3</td><td>CV</td><td>이벤트 카메라 시간 양자화의 강건성-해상도 트레이드오프를 이론적으로 분석했고 이벤트 기반 로봇 perception에 참고할 만함</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2609.23733'>VGGT-Prime: Compute-Adaptive Mixture-of-Heads for Efficient Visual Geometry Transformers</a></td><td>35</td><td>3</td><td>3D Vision</td><td>VGGT 계열 feed-forward 3D reconstruction을 compute-adaptive mixture-of-heads로 가속한 연구라 효율화 중심이지만 로봇 3D 인식 파이프라인에 참고할 만함</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2609.24470'>Spatial Action Review: A Visual Analytics Dashboard for Auditing Language-to-Action Hand-offs in Electron Microscopy</a></td><td>35</td><td>3</td><td>Multimodal</td><td>MLLM의 언어 답변은 맞는데 짝지어진 공간 출력이 틀리는 silent failure를 전자현미경 워크플로에서 감사하는 대시보드로 failure detection 개념과 연결됨</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2609.23161'>An Eternal Irradiance Camera</a></td><td>35</td><td>2</td><td>CV</td><td>구면조화함수로 근사되는 전방위 irradiance를 측정하는 새 카메라 설계로 조명 추정에 참고할 만하나 로봇 적용은 제시되지 않음</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2609.23796'>Mira-Scene: Pixel-Aligned Layouts for Generative 3D Scene</a></td><td>35</td><td>2</td><td>3D Vision</td><td>단일 이미지에서 객체를 장면 레이아웃에 픽셀 정렬로 배치하는 생성 3D 장면 연구로 시뮬레이션 자산 생성에 참고할 여지가 있으나 그래픽스 중심임</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2609.24031'>Video-STLayout Pre-training</a></td><td>35</td><td>2</td><td>Video</td><td>객체 bounding box의 시공간 레이아웃으로 비디오 표현을 사전학습하는 새 전략이라 video understanding 우선 주제와 닿아 있음</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2609.24098'>A$^2$Safe: Counterfactual Evidence-Aligned Adaptive Agent Collaboration for Safe and Effective Visual Question Answering</a></td><td>35</td><td>2</td><td>Multimodal</td><td>멀티모달 증거의 상호작용에서 발생하는 위험을 counterfactual 정렬로 판단하는 안전한 VQA 에이전트 협업 연구로 counterfactual reasoning과 약하게 연결됨</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2609.23153'>SparkDiffusion: Mitigating the High-Sparsity Trap --- A Unified Framework for up to $265\times$ Single-GPU Acceleration of Visual Generation</a></td><td>35</td><td>1</td><td>Video</td><td>video diffusion의 high-sparsity trap을 진단하고 265배 가속을 달성한 연구지만 효율화 중심이라 로봇 문제로 연결되지 않음</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2609.23533'>GeoBalance: Geometry-Aware Monitoring and Reconstruction with Asymmetric Optimization for Balanced Multimodal Learning</a></td><td>35</td><td>1</td><td>Multimodal</td><td>모달리티 불균형이 약한 모달리티의 표현 자체를 붕괴시킨다는 새 관찰을 제시했으나 로봇 적용은 없음</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2609.24244'>Look Where It Counts: A Free, Label-Free Visual Evidence Signal for Fine-Grained Vision-Language Reasoning</a></td><td>35</td><td>1</td><td>Multimodal</td><td>고해상도 다운샘플링으로 놓치는 시각 증거를 추가 라벨 없이 신호화해 세밀한 VL 추론을 돕는 방법으로 로봇 적용은 다루지 않음</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2609.24737'>Ananke: Contractive Torus Attractor Networks</a></td><td>35</td><td>1</td><td>CV</td><td>잠재 표현을 product-torus prior에 얹고 이중 위상 연속 흐름으로 특징을 갱신하는 새 표현학습 프레임워크로 일반 비전 백본 연구이며 로봇 적용은 없음</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2609.22107'>Generalized Multimodal Foundation Model</a></td><td>35</td><td>1</td><td>Multimodal</td><td>임의의 모달리티 조합과 태스크에 적용 가능한 통합 멀티모달 fusion 모델을 목표로 한 야심찬 일반화 프레임워크로 로봇 적용은 제시되지 않음</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2609.22234'>Seeing Through Conflicts: Improving Instruction Hierarchy Alignment in Vision-Language Models</a></td><td>35</td><td>1</td><td>Multimodal/Safety</td><td>지시문이 이미지·텍스트에 분산되거나 변형될 때 상위 지시를 우선하도록 강화학습으로 정렬한 VLM 안전성 연구로 웹 에이전트 일반화까지 확인했지만 로보틱스 제어와는 결이 다름</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2609.24422'>Prior-Amortized In-Context Bayesian Inference for Generalized Linear Mixed-Effects Models</a></td><td>35</td><td>0</td><td>LG</td><td>GLMM을 위한 prior-amortized in-context 베이지안 추론망, NUTS 대비 수백배 빠른 zero-shot 추론을 제공함</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2609.24432'>1% of Tokens Can Be Enough: On Gradient Estimation in On-Policy Distillation</a></td><td>35</td><td>0</td><td>NLP</td><td>정보기하학적 신호대잡음비로 on-policy distillation의 토큰 선택을 개선한 방법, 0.1~1% 토큰만으로 성능 유지함</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2609.22090'>Recognition, Simulation, and Refusal: A Contamination-Aware Study of Classic Psychological Effects in LLM Agents</a></td><td>35</td><td>0</td><td>NLP</td><td>LLM 에이전트가 보이는 고전 심리효과가 진짜 편향인지 라벨-오염 여부를 분리해 검증한 벤치마크로 로보틱스와는 무관한 NLP/심리학 융합 연구임</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2609.22111'>Beyond the Text: Verifying That Agent-Written Papers Are Backed by Their Artifacts</a></td><td>35</td><td>0</td><td>NLP/Agentic AI</td><td>에이전트가 쓴 연구 문서가 실제 코드·실험과 일치하는지 정적·동적으로 감사하는 ReAgent 프레임워크로 로보틱스와는 관련 없는 연구무결성 도구임</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2609.22125'>Type-Driven Tokenization for Brahmic Scripts</a></td><td>35</td><td>0</td><td>NLP/Tokenization</td><td>브라흐미 문자족의 정서법을 partial semigroup으로 형식화해 토크나이저 오류를 고치는 이론적으로 탄탄한 언어처리 기여이나 로보틱스와는 무관함</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2609.22138'>Does the Truthfulness Signal Survive Code-Mixing? Probing Hidden States for Hallucination Detection in Hinglish</a></td><td>35</td><td>0</td><td>NLP/Hallucination</td><td>코드믹싱된 힌글리시에서도 hidden-state 환각탐지 프로브가 잘 전이됨을 보인 다국어 실증 연구로 로보틱스와는 무관함</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2609.22144'>Multilingual Safety Signals Are Multi-Layered: Filtering Safety-Degrading Data for Safer LLMs</a></td><td>35</td><td>0</td><td>NLP/Safety</td><td>안전정렬을 훼손하는 파인튜닝 샘플이 언어마다 다른 층에 분산돼 있음을 보이고 다층 필터링으로 방어하는 다국어 안전성 연구로 로보틱스와 무관함</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2609.22162'>Beyond Raw Context Transfer: Representation-based Federated Retrieval-Augmented Generation</a></td><td>35</td><td>0</td><td>NLP/Federated Learning</td><td>원문 대신 압축된 latent representation만 교환하는 federated RAG로 의료 등 민감 도메인의 검색증강 생성을 다루며 로보틱스와는 무관함</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2609.22200'>PII-TRACE: A Benchmark for Context-Aware PII Detection in Multi-Turn LLM Conversations</a></td><td>35</td><td>0</td><td>NLP/Privacy</td><td>여러 턴에 걸쳐 반복되는 PII를 놓치지 않는지 평가하는 PII-TRACE 벤치마크와 경량 탐지기로 대화형 프라이버시 보호를 다루며 로보틱스와 무관함</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2609.22213'>SCoP: Structured Constraint Parsing for Evidence-Space Control in Temporal Knowledge Graph Question Answering</a></td><td>35</td><td>0</td><td>NLP/KGQA</td><td>시간지식그래프 질의응답에서 앵커사건과 시간제약을 명시적으로 파싱해 증거공간을 통제하는 SCoP 프레임워크로 로보틱스와 무관함</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2609.22243'>Replay-Gated Neural Execution: Decoupling Persistent Behavioral Specifications from Neural Realizations in Frozen Language Models</a></td><td>35</td><td>0</td><td>LG</td><td>고정 LLM에서 행동 사양과 실현을 분리하는 추상적 실행 프레임워크, 개념은 흥미롭지만 소형 모델 실험에 그침</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2609.22455'>Apollo Restore: A Foundation LLM for Historical Greek Optimized for Fill-in-the-Middle Restoration of Ancient Greek Texts</a></td><td>35</td><td>0</td><td>NLP</td><td>고대 그리스어 결손 텍스트 복원 특화 LLM, 전문가 평가에서 인간 수준 근접해 니치 응용 완성도가 높음</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2609.22607'>Pretrained Persona Mixture Models and Tandem Models for Human Simulation</a></td><td>35</td><td>0</td><td>NLP</td><td>자유형 대화 샘플로 페르소나를 바인딩하는 새 인간 시뮬레이션 패러다임, 다양성 보존 면에서 기존 롤플레잉보다 개선됨</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2609.24362'>VLM-in-Sandbox: Visual Workspaces for Agentic Visual Reasoning</a></td><td>34</td><td>3</td><td>Multimodal</td><td>시각근거를 원장으로 관리해 멀티모달 컨텍스트 폭증을 막는 샌드박스 프레임워크, 정확도와 토큰효율을 동시에 개선함</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2609.22701'>Autonomous Model Lifecycle Management for Digital Twin-Based Manufacturing Control</a></td><td>34</td><td>2</td><td>RL</td><td>디지털트윈 제조 공정의 모델 생애주기 자동관리 CPS, 2023년부터 실배포된 산업 RL 시스템이나 로봇 조작과는 다름</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2609.24754'>Inference of Unknown Dynamical Components Using Next Generation Reservoir Computing: From Chaotic Systems to Climate Data</a></td><td>34</td><td>2</td><td>LG</td><td>next-generation reservoir computing으로 미관측 동역학 성분을 적은 데이터로 추론, 카오스계 시스템 식별 원리가 로봇 동역학과 연관될 수 있음</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2609.24025'>Synthesizing Reactive Character Behaviors for Continuous Games via Programmatic Policy Search</a></td><td>34</td><td>2</td><td>RL</td><td>연속게임 정책을 DSL 프로그램 탐색으로 합성, 신경망 대비 해석가능하고 이식성 높은 정책을 발견함</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2609.23242'>Proximal Residual Value Functions for Consistent Planning and Real-Time Execution</a></td><td>34</td><td>1</td><td>RL</td><td>재고배치용 proximal residual value function으로 planning-execution 일관성을 보장한 RL 방법론임</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2609.23254'>The Price of Self-Calibration: Exact Evidence Budgets and Manufactured Blind Sets in Adaptive Monitoring</a></td><td>34</td><td>1</td><td>LG</td><td>self-calibrating 모니터의 오탐율 보장 비용을 정확한 법칙으로 계산한 이론 논문, 모니터링 일반원리로서 흥미로움</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2609.23333'>A Patient World Model for Early Forecasting of Digital Health Campaign Outcomes: Capabilities and Limits</a></td><td>34</td><td>1</td><td>World Model</td><td>환자별 latent state로 디지털 헬스 캠페인 성과를 rollout 예측하는 world model, 도메인은 마케팅이나 world model 정식화는 일반적임</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2609.24289'>TTSE: A Two-Track Online Self-Evolution Framework</a></td><td>34</td><td>1</td><td>NLP</td><td>환경 사실과 절차를 분리해 온라인 자기진화하는 에이전트 프레임워크, ALFWorld 등에서 성능 개선하나 로봇 실물 실험은 없음</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2609.23466'>RPMem: Learning Long-Term Recurrent Parametric Memory Across Sessions for LLM Agents</a></td><td>34</td><td>1</td><td>LG</td><td>세션 간 파라메트릭 메모리를 LoRA로 압축해 백본 교체에도 재사용 가능하게 함, agent memory 아키텍처로서 의미 있음</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2609.23808'>FLARE: A Full-Lifecycle Dense Supervision Paradigm for Long-Horizon Coding Agents via Generative Reward Model</a></td><td>34</td><td>1</td><td>LG</td><td>장기 코딩 에이전트에 밀집 보상을 주는 generative reward model, 토큰 절감과 성능 개선이 모두 확인된 견고한 기여임</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2609.24066'>Efficient Reasoning Exploration via State-Conditioned Latent Steering with Progress Guidance</a></td><td>34</td><td>1</td><td>LG</td><td>reasoning 탐색 붕괴를 완화하는 training-free latent steering, best-of-N 효율을 개선함</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2609.22592'>AutoGym: Blueprint-First Generation of Verifiable Agent Gyms</a></td><td>34</td><td>1</td><td>LG</td><td>블루프린트 우선 설계로 검증가능한 agent gym을 자동생성, 난이도 조절 가능한 커리큘럼 합성이 참신함</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2609.23957'>Divergent strategies and convergent outcomes in autonomous materials discovery</a></td><td>34</td><td>1</td><td>AI</td><td>16개 독립 에이전트가 서로 다른 전략에도 동일한 소재 프런티어에 수렴함을 보이되 공통 오류도 드러낸 과학에이전트 신뢰성 연구, 감사 프로토콜 필요성을 실증함</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2609.24881'>Pinocchio: Fast Uncertainty Estimates for Black-Box Language Models</a></td><td>34</td><td>1</td><td>LG</td><td>블랙박스 API 모델의 정답 확신도를 단일 forward pass로 추정하는 외부 캘리브레이터, 미지 모델 13종에 제로샷 전이가 성공함</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2609.22220'>Measuring the Checker: Mutation Analysis for GPU-Kernel Benchmark Oracles</a></td><td>34</td><td>0</td><td>LG</td><td>GPU 커널 벤치마크 채점기 자체의 결함을 mutation analysis로 측정한 메타평가, 방법론은 탄탄하나 로봇과 무관함</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2609.22232'>CNA: An AI-Oriented Comprehensive Normalized Assessment for Healthy Status and Application to Optimize RRT Strategies by Reinforcement Learning</a></td><td>34</td><td>0</td><td>LG</td><td>신장대체요법 전략 최적화를 위한 오프라인 RL 응용, 의료 도메인 성과 개선 연구임</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2609.22237'>Not All Ranks Are Equal: Budget-Aware LoRA Merging Across Tasks</a></td><td>34</td><td>0</td><td>NLP</td><td>SVD 기반 rank 할당으로 LoRA 병합 성능 개선, 실용적이나 novelty는 제한적임</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2609.22752'>D-IMPL: A Diffusion-based Solver for Parameterized BBOs</a></td><td>34</td><td>0</td><td>LG</td><td>블랙박스 최적화를 확산모델 기반 minimization policy로 amortize한 방법론임</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2609.22782'>Look Before You Steer: Geometry Predicts SAE Feature Steerability</a></td><td>34</td><td>0</td><td>NLP</td><td>SAE 디코더 기하구조로 feature steerability를 사전 예측하는 해석연구, 로봇과 무관함</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2609.22820'>Beyond Average Error through Oracle-Informed Stress Tests for Time-Series Forecasting</a></td><td>34</td><td>0</td><td>LG</td><td>예측오차를 환경 위험과 오라클 거리로 분해하는 stress test 벤치마크, 시계열 평가 방법론 연구임</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2609.23457'>RLVR$^{2}$: Reinforcement Learning with Verifiable Rubric-based Ranking</a></td><td>34</td><td>0</td><td>NLP</td><td>rubric 다차원 점수를 순위 기반 latent utility로 합치는 RLVR 보상 설계 연구임</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2609.23516'>ITSY: Causal Discovery From Irregular Time-Series Data</a></td><td>34</td><td>0</td><td>LG</td><td>결측 시점을 가장 가까운 관측으로 재구성해 불규칙 시계열 인과구조를 학습하는 방법임</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2609.23535'>Decoupled Causal Discovery</a></td><td>34</td><td>0</td><td>LG</td><td>Markov boundary를 decoupling weighting으로 직접 식별하는 새로운 인과발견 방법임</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2609.23585'>Global Ranks Survive, Selected Heads Shift: BOS-Sink Topology under 4-bit Weight-Only Quantization</a></td><td>34</td><td>0</td><td>NLP</td><td>4bit 양자화 후 sink head 위치가 전역적으로는 유지되나 국소적으로 이동함을 보인 진단 연구임</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2609.23686'>One Patch, Three Roles: What Is Actually Coupled in Autoregressive Time-Series Forecasting?</a></td><td>34</td><td>0</td><td>LG</td><td>패치 기반 자기회귀 시계열 예측의 표현·전이·실행 역할을 분리해 분석한 연구임</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2609.23761'>GenVoid: Uncertainty-Aware Learning of Subsurface Material Defects with an Experimentally Validated Physics-Informed Generative Model</a></td><td>34</td><td>0</td><td>LG</td><td>표면 변위만으로 내부 공극을 불확실성 포함해 역추정하는 physics-informed 생성모델임</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2609.23789'>Belted Engression: Sufficient Dimension Reduction for Generative Distributional Regression</a></td><td>34</td><td>0</td><td>LG</td><td>조건부 생성모델에 sufficient dimension reduction을 임베딩한 belted engression 프레임워크임</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2609.23826'>Real-time Generalizable Heart Valve Mechanics for Clinical Disease Assessment via a Physics-Conditioned Neural Operator</a></td><td>34</td><td>0</td><td>LG</td><td>심장판막 역학을 transformer surrogate로 15000배 가속한 신경연산자 논문임</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2609.23907'>A discrete generative model of neuronal spiking activity on microelectrode arrays</a></td><td>34</td><td>0</td><td>LG</td><td>미세전극 배열 스파이킹 활동을 모티프 어휘로 표현하는 이산 생성모델임</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2609.23924'>Matched-Input Estimates Differ in Sign Across Architectures: Auditing EEG Foundation Models on Motor Imagery</a></td><td>34</td><td>0</td><td>LG</td><td>EEG 파운데이션 모델이 motor imagery에서 지도학습보다 못함을 검증한 엄밀한 감사 연구임</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2609.24141'>CLOOPD: Closing the Learner Loop in On-Policy Distillation</a></td><td>34</td><td>0</td><td>NLP</td><td>teacher 채점과 student 소화를 분리한 closed-loop on-policy distillation 프레임워크임</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2609.24202'>Opinion Leader Dynamics: How Sparse Attention Shapes Token Clustering</a></td><td>34</td><td>0</td><td>NLP</td><td>sparse attention이 토큰을 여러 군집으로 수렴시키는 동역학을 Wasserstein gradient flow로 이론화한 연구임</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2609.24322'>The Undetected Damage of Quantization on Retrieval and How to Fix It</a></td><td>34</td><td>0</td><td>NLP</td><td>quantization이 분류보다 retrieval top-1을 더 많이 바꿈을 밝히고 score gap 기반 대응책을 제안한 진단 연구임</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2609.24328'>A Distributional Optimisation Perspective on Combining Models in Deep Learning</a></td><td>34</td><td>0</td><td>LG</td><td>앙상블과 LoRA 평균화를 분포 최적화 관점에서 통합한 이론적 프레임워크임</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2609.24370'>Prescriptive SVD-Inspired Attention via Spectral Energy Retention</a></td><td>34</td><td>0</td><td>CV</td><td>SVD 기반 attention의 스펙트럴 진단을 실제 개입(에너지 보존 절단)으로 확장한 연구임</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2609.24440'>Comparing Latent Concept Formation in State Space Models and Transformers via Sparse Autoencoders</a></td><td>34</td><td>0</td><td>NLP</td><td>SAE로 Mamba와 Transformer의 잠재개념 형성을 비교해 universality hypothesis를 뒷받침한 해석연구임</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2609.24559'>$t_0$: A Time-Series Foundation Model for Forecasting with Context</a></td><td>34</td><td>0</td><td>LG</td><td>공변량 기반 예측을 지원하는 오픈웨이트 시계열 파운데이션 모델, 여러 벤치마크에서 상위권 성능임</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2609.24646'>iSDFT: Information-Proximal Self-Distillation for Continual Learning in LLMs</a></td><td>34</td><td>0</td><td>NLP</td><td>teacher 정보량을 예산으로 다루는 information-proximal self-distillation continual learning 기법임</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2609.24741'>An Exact Junction-Tree Extended Formulation for Optimal Classification Trees</a></td><td>34</td><td>0</td><td>LG</td><td>junction-tree 표현으로 최적 분류트리를 정확히 푸는 LP 정식화, column generation·message passing으로 큰 인스턴스를 인증함</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2609.24862'>When Tomorrow Becomes Today: Self-Evolving Policies for Agentic Time-Series Forecasting</a></td><td>34</td><td>0</td><td>LG</td><td>실현된 예측 결과로 orchestration 정책을 지속 갱신하는 자기진화 시계열 에이전트임</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2609.22522'>When Cosine Similarity Fails to Reflect Linearly Accessible Structure in Dialogue Models</a></td><td>34</td><td>0</td><td>NLP</td><td>대화 표현에서 cosine similarity가 선형 접근 가능한 구조를 과소평가함을 보인 표현학습 진단 연구</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2609.22633'>Beetle: A Bilingual Model Suite for Modelling Second-Language Processing</a></td><td>34</td><td>0</td><td>NLP</td><td>통제된 이중언어 프리트레이닝 프레임워크로 285개 모델을 공개, L2 습득 연구용 자원 논문으로 완성도가 높음</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2609.23205'>Euston: Training Away Mathematical Sycophancy Without Losing the Mathematics</a></td><td>34</td><td>0</td><td>NLP</td><td>손상된 수학 정리에 대한 아첨을 줄이는 검증 모델, GRPO로 판별력을 개선하면서 수학 능력을 유지함</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2609.23587'>On the Efficiency-Safety Dilemma in Large Reasoning Models</a></td><td>34</td><td>0</td><td>NLP</td><td>효율화 기법이 진짜 정렬이 아니라 추론력 저하로 탈옥 성공률을 낮춘다는 점을 규명, 안전성 평가에 중요한 함의를 줌</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2609.23886'>this-that-model-1.0: A typed decision model that decides in 30 ms, for a millionth of a cent</a></td><td>34</td><td>0</td><td>LG</td><td>은닉 상태에서 바로 답을 읽는 타입드 의사결정 모델로 지연시간과 비용을 극단적으로 절감, 산술 연쇄 추론엔 약함을 인정하는 균형잡힌 보고임</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2609.24194'>When Residualization Helps an Audit: Format Effects, Slice Gains, and Their Limits</a></td><td>34</td><td>0</td><td>NLP</td><td>잔차화가 평가 점수의 표면 요인을 제거하되 구성타당도까지 훼손할 수 있음을 통제실험으로 규명한 평가 방법론 경고임</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2609.24554'>Toward a Unified Mathematics of Concepts</a></td><td>34</td><td>0</td><td>AI</td><td>개념 표상의 13개 연산을 기준으로 10개 프레임워크를 비교하는 이론적 시도, 범주화 사례연구로 실증도 일부 제공함</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2609.22497'>The Wisdom of Artificial Deliberative Crowds</a></td><td>34</td><td>0</td><td>AI</td><td>LLM 숙의가 수동집계보다 집단오차를 줄이고 모델 다양성이 핵심임을 4개 도메인에서 확인, 시야가 넓고 실증이 탄탄함</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2609.23378'>Leaky-integrator reconstruction: taming error accumulation in recursive differenced time-series forecasting</a></td><td>34</td><td>0</td><td>LG</td><td>차분예측의 오차누적을 극점이동으로 해결하는 무학습 기법, 다양한 아키텍처에서 일관된 개선을 보인 단순하고 견고한 기여임</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2609.23917'>Increasing Skill Level Recruits Deeper Attention Layers in a Frozen Chess Transformer</a></td><td>34</td><td>0</td><td>LG</td><td>Elo 조건을 바꾸며 체스 트랜스포머의 계산중심이 깊어짐을 관찰한 기계적 해석 연구, 조건화 입력이 계산을 재분배하는 메커니즘을 규명함</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2609.24130'>Self-Healing Harness for Runtime Oversight of Agent Self-Modification</a></td><td>34</td><td>0</td><td>AI</td><td>자기수정 제안을 외부 게이트가 승인/거부하는 admission control 프레임워크, 로컬개선이 회귀를 유발하는 경우를 실증으로 보임</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2609.24290'>When and How Should an Agent Clarify? CIGAsk: Teaching LLMs to Clarify via Counterfactual Information Gain</a></td><td>34</td><td>0</td><td>NLP</td><td>반사실적 정보이득과 비대칭 모호성 보너스로 언제/어떻게 명확화할지 동시학습, 3개 벤치마크에서 일관된 개선을 보임</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2609.24346'>LADDER: Graph-Guided Diffusion Language Models for Efficient Multi-Hop Reasoning</a></td><td>34</td><td>0</td><td>NLP</td><td>확산언어모델과 그래프RAG를 결합해 부분노이즈 상태에서 조기등장 엔티티로 검색을 트리거, 정확도와 지연 모두 개선함</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2609.24480'>Fathom-Vaidya: Advancing Medical Reasoning with Rubric-Based Rewards</a></td><td>34</td><td>0</td><td>NLP</td><td>진단추론과 임상대화 추론을 분리해 루브릭기반 RL로 순차학습, HealthBench-Hard에서 GPT-5를 능가함</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2609.24677'>TimeLitmus: A Diagnostic Benchmark for Cross-Modal Understanding and Explanation Faithfulness in Event-Conditioned Time-Series Prediction</a></td><td>34</td><td>0</td><td>Multimodal</td><td>시계열예측에서 정확도가 진짜 교차모달 이해를 과대평가함을 반사실통제로 드러낸 진단 벤치마크, 설명충실성 격차도 큼</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2609.24974'>Harness-Zero: Harness Distillation via Agent-as-Harness</a></td><td>34</td><td>0</td><td>LG</td><td>최적화된 하네스의 유도행동을 agent-as-harness로 학생응답에 증류해 배포시 하네스 없이도 유지, 태스크 성공률 개선폭이 큼</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2609.22183'>CleanScore: Black-Box Benchmark Audits with Negative Controls and Sensitivity Bounds</a></td><td>33</td><td>0</td><td>NLP</td><td>벤치마크 오염 감사용 negative control 방법론, 통계적으로 탄탄하나 로봇과 무관함</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2609.22253'>CAMFT: Conflict-Aware Mergeable Fine-Tuning for Large Language Models</a></td><td>33</td><td>0</td><td>NLP</td><td>학습 단계에서 충돌 회피를 유도하는 mergeable fine-tuning 기법, LLM 병합 방법론 개선임</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2609.22257'>Strategy Accumulation and Guided Execution for Automated LLM Fine-Tuning</a></td><td>33</td><td>0</td><td>NLP</td><td>AutoML fine-tuning 탐색 전략을 축적·재사용하는 프레임워크, 응용 메타학습 연구임</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2609.22690'>Multi-Armed Bernoulli Bandits via Minimax Single-Arm Stopping</a></td><td>33</td><td>0</td><td>RL</td><td>단일팔 stopping 문제의 minimax 해로 밴딧 인덱스 정책을 구성한 이론 논문임</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2609.22319'>Embedding Physics Priors in Robot Learning: A Survey</a></td><td>32</td><td>6</td><td>Manipulation</td><td>물리 prior를 로봇학습에 임베딩하는 방법을 분류체계로 정리한 서베이, 새로운 방법 제시는 없으나 참고자료로 유용함</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2609.22974'>A Horizon-slicing Approach to Minimum Obstacle Displacement Planning for Robot Navigation</a></td><td>32</td><td>5</td><td>Planning</td><td>이동가능 장애물을 치우는 경로계획을 NP-hard로 증명하고 근사해를 제시한 이론 논문으로 학습 요소는 없음</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2609.23037'>Fast and Robust Temporal Logic Planning via ADMM-based Trajectory Optimization</a></td><td>32</td><td>5</td><td>Planning/Formal Methods</td><td>STL 명세 하 연속시간 경로계획을 ADMM으로 가속한 방법으로 기존 대비 4.7배 속도향상이지만 formulation 자체는 알려진 문제의 최적화 기법 개선임</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2609.23792'>Risk-Aware Motion Planning and Control under Unknown Dynamics with Hybrid Observations</a></td><td>32</td><td>5</td><td>Planning</td><td>관측이 부분적으로만 주어지는 미지 동역학 하에서 blind region 통과 리스크를 정량화한 이론 중심 플래닝 논문임</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2609.23928'>MR-SPITE: Accelerating Multi-Robot Conflict Scans via Hierarchical Swept-Volume Approximations</a></td><td>32</td><td>5</td><td>Multi-Robot Planning</td><td>swept-volume 근사로 다중로봇 충돌 스캔을 가속하는 필터로 계획시간을 절반 이상 줄였지만 기존 collision checker의 가속 기법 수준임</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2609.24099'>Ask Before It Tells: Benchmark-to-Robot Body-Cue Transfer for a Question-First Bedside Robot</a></td><td>32</td><td>5</td><td>HRI</td><td>고통 신호를 곧바로 경보가 아닌 질문 트리거로 쓰는 침상 보조로봇 프로토타입으로 응용 시스템 논문에 가까움</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2609.24413'>Robotic Valve Turning: Axial Misalignment Correction Using Reaction Torque Feedback</a></td><td>32</td><td>5</td><td>Manipulation/Control</td><td>반작용 토크와 오정렬 벡터의 기하관계로 밸브조작 오차를 보정하는 안정성 증명이 딸린 제어법이며 학습 기반은 아님</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2609.24761'>A Switched Adaptive Control Framework for Aerial Manipulators Under Dynamic Transitions</a></td><td>32</td><td>5</td><td>Control/Aerial Manipulation</td><td>전이구간에서 안정성을 보장하는 스위칭 신호를 제공하는 적응제어 프레임워크로 공중 매니퓰레이터 제어이론 기여이며 학습 요소는 없음</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2609.23263'>Scenario MPC with STL Specifications and Pareto-Based Feasibility Repair</a></td><td>32</td><td>4</td><td>Control/Planning</td><td>확률적 비협조 에이전트 하에서 STL 제약을 Pareto 재구성으로 회복하는 자율주행 MPC 논문으로 제어이론 기여에 가까움</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2609.23336'>MinCU: A Fine-Grained Benchmark for Grounded Minimal-Change Understanding in Image Pairs</a></td><td>32</td><td>2</td><td>Multimodal</td><td>거의 동일한 이미지 쌍의 미세한 변화를 위치까지 정확히 짚어내는 벤치마크로 변화 탐지가 실패 진단과 개념적으로 닿아 있음</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2609.24026'>InterHier: Learning Interconnected Hierarchical Semantics for Open-Vocabulary Object Detection</a></td><td>32</td><td>2</td><td>CV</td><td>고정 커넥터 대신 상호 연결된 계층 구조로 open-vocabulary 객체 탐지를 개선한 연구로 open-world 인식에 참고할 만함</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2609.24409'>DeCo: Efficient Decouple-to-Couple Learning for Multi-Task Visual Grounding</a></td><td>32</td><td>2</td><td>Multimodal</td><td>태스크 간 특징 충돌을 분리-결합 방식으로 완화한 멀티태스크 visual grounding 연구로 language-to-action 접지와 약하게 연결됨</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2609.22746'>ProcessLight: Process Supervision for Large Language Model Based Traffic Signal Control</a></td><td>32</td><td>2</td><td>RL</td><td>신호제어 LLM에 단계별 신용할당을 도입한 RL프레임워크, 실도로 데이터로 검증된 프로세스 감독 기여임</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2609.23023'>PINNForge: Execution-Grounded Evolutionary Design of Physics-Informed Neural Networks for PDE Solving via Large Language Models</a></td><td>32</td><td>2</td><td>World Model</td><td>실행피드백을 LLM 진화탐색에 반영해 PINN 설계를 자동화, PDE 25종에서 일관된 오차 개선을 보임</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2609.24165'>APEXA: Execution-Integrity Enforcement for Multi-Agent LLM Automation of Synchrotron Data Reduction</a></td><td>32</td><td>2</td><td>AI</td><td>방사광가속기 데이터환원을 다중에이전트로 자동화하며 미실행 결과를 차단하는 실행무결성 가드, 실제 빔라인 배포로 검증됨</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2609.24876'>Partner-Specific Affective Precision in Social Active Inference</a></td><td>32</td><td>2</td><td>RL</td><td>관계별 신뢰도를 능동추론 프레임워크로 정식화해 정책선택에 반영, 신뢰보정 지연 현상까지 시뮬레이션으로 규명함</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2609.23005'>Compressing 3D Gaussian Splatting via Cross-Representation Priors</a></td><td>32</td><td>1</td><td>3D Vision</td><td>3DGS의 anchor 간 중복을 노리는 압축 프레임워크로 저장·전송 비용을 줄이는 엔지니어링 기여에 가까움</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2609.24997'>VideoGen-Agent: Reinforcing Video Generation Agents</a></td><td>32</td><td>1</td><td>RL</td><td>외부 도구를 조율하는 멀티태스크 agentic RL로 비디오 생성 에이전트를 강화하는 연구로 로봇 적용은 다루지 않음</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2609.22091'>Memory That Looks Forward: A Zero-Inference Prospective Term for Personal Memory Retrieval</a></td><td>32</td><td>1</td><td>NLP/Memory</td><td>쿼리 시점 추론비용 없이 개인 기억 검색에 미래 지향적(prospective) 커밋 신호를 얹는 방법으로 로봇 메모리와 결이 다른 개인비서형 LLM 메모리 연구임</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2609.23465'>Propose, Verify, Commit: Evidence-Grounded Memory for Long-Horizon Multi-Actor Conversations</a></td><td>32</td><td>1</td><td>LG</td><td>장기 다자간 대화 메모리를 propose-verify-commit 상태기계로 구성, 벤치마크 개선폭은 크나 로봇 메모리와는 별개 영역임</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2609.22702'>Hapi: A Multivariable Land-Surface Transformer for Medium-Range Hydrological Forecasting at Continental Scale</a></td><td>32</td><td>1</td><td>World Model</td><td>대륙규모 수문 예측을 위한 멀티변수 랜드서피스 트랜스포머, 실측 게이지 검증과 학습된 과업가중치로 희귀홍수 탐지를 개선한 견고한 응용 세계모델링 연구임</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2609.23989'>ACLArena: Agent Continue Learning in Multi-stage Post-training</a></td><td>32</td><td>1</td><td>LG</td><td>에이전트 지속학습에서 망각/일반화 메커니즘을 모델/토큰 수준에서 분석하고 LoRA 전문가 라우팅 레시피를 제안, 분석 깊이가 강점임</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2609.24663'>Beyond Endpoint Performance: Process-Level Evaluation of Self-Evolving Agents</a></td><td>32</td><td>1</td><td>LG</td><td>자기진화 에이전트의 일반화/보존/규칙적응 능력을 체크포인트별로 추적하는 벤치마크, 선택된 업데이트가 잠재력에 못미침을 발견함</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2609.24831'>GRUET: Quantifying Uncertainty of Agentic Reasoning-and-Acting Processes</a></td><td>32</td><td>1</td><td>LG</td><td>추론공간을 그래프로 모델링해 에이전트 궤적의 불확실성을 정량화, 9개 LLM 5개 벤치마크에서 선택생성 성능을 검증함</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2609.24379'>Topographic Training Concentrates Causal Circuits Without Improving Neuron Monosemanticity</a></td><td>32</td><td>0</td><td>CV</td><td>공간 지역성 손실이 causal circuit을 집중시키지만 뉴런 monosemanticity는 개선하지 못함을 보인 mechanistic interpretability 연구로 로봇과 무관함</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2609.22196'>EvoRank: LLM-Guided Evolution of Multi-Objective Learning-to-Rank Pipelines</a></td><td>32</td><td>0</td><td>LG</td><td>LLM 기반 랭킹 파이프라인 진화 시스템, fitness noise 감사 결과가 흥미로우나 추천시스템 응용임</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2609.22098'>TreeSpark: Calibrated, Load-Adaptive Draft Trees for Semi-Autoregressive Speculative Decoding</a></td><td>32</td><td>0</td><td>NLP/LG</td><td>semi-autoregressive draft tree를 부모조건 분포로 보정해 speculative decoding을 가속한 LLM 추론 효율화 연구로 로보틱스와 직접 관련은 없음</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2609.22104'>DeepInstructor: An Agentic AI Instructor for Experience-Driven Idea Evaluation</a></td><td>32</td><td>0</td><td>NLP/Agentic AI</td><td>peer review 경험을 구조화한 그래프로 연구 아이디어를 평가하는 에이전트 프레임워크이며 로보틱스와 무관함</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2609.22188'>Fairness Beyond Anonymization? Demographic Leakage in German LLM-Generated Resumes</a></td><td>32</td><td>0</td><td>NLP/Fairness</td><td>독일어 이력서 생성에서 성별·인종 신호가 익명화 후에도 잔존함을 분류기로 감사한 공정성 연구로 로보틱스와 무관함</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2609.22198'>The Role of AI in Online Reviews</a></td><td>32</td><td>0</td><td>NLP/Social Science</td><td>LLM 공급 충격 전후 온라인 리뷰의 부정성 변화를 계량경제학적으로 분석한 연구로 로보틱스와 무관함</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2609.23916'>Time-Incremental Continued Pretraining of LLMs: Knowledge Updates Without Catastrophic Forgetting</a></td><td>32</td><td>0</td><td>LG</td><td>웹 스냅샷 지속 프리트레이닝을 현실적 URL 중복 조건에서 재평가, 파국적 망각 없이 지식 갱신이 가능함을 확인함</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2609.24106'>You Can Tell Who&#x27;s Asking: What the Web&#x27;s Questions Are Made Of, and Where They Come From</a></td><td>32</td><td>0</td><td>NLP</td><td>12년간 웹 질문의 진짜 사용자 비중이 급감했음을 대규모로 측정, 데이터 오염 경고로서 흥미로움</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2609.24196'>LoopCD: Loop-wise Contrastive Decoding for Improving Reasoning in Looped Language Models</a></td><td>32</td><td>0</td><td>LG</td><td>루프형 LM의 불안정한 반복을 대조 디코딩으로 교정, 무학습 추론을 개선함</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2609.24877'>Decomposing Error and Style in Automated Clinical Coding</a></td><td>32</td><td>0</td><td>NLP</td><td>코더 간 불일치의 상당부분이 오류가 아니라 코딩 스타일임을 입증, 평가 프레임 재고를 촉구함</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2609.24885'>The Copy Ceiling: An Input-Exposure Control for Ontology-Grounded Generation over Curated Corpora</a></td><td>32</td><td>0</td><td>NLP</td><td>그래프 기반 생성이 답을 그대로 노출한 컨텍스트를 베낀 것에 불과함을 통제하는 exposure accounting 제안, RAG 평가의 근본적 함정을 지적함</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2609.22695'>A Survey on the Linear Representation Hypothesis</a></td><td>32</td><td>0</td><td>AI</td><td>선형표상가설을 반증가능한 과학적 가설로 재정식화한 개념정리 서베이, 표상학습 이해에 유용한 참조자료임</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2609.23640'>Are Human-Aligned Models Models of Humans? A Turing-Test Gap in Preference Alignment</a></td><td>32</td><td>0</td><td>AI</td><td>선호정렬이 인간유사성을 오히려 해칠 수 있음을 이론/실증으로 보인 정렬 연구, 정렬 목표 재고를 촉구하는 개념적 기여임</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2609.24092'>DocMIDE: Learning Multi-Hop Implicit Derivation in Visually Rich Documents</a></td><td>32</td><td>0</td><td>Multimodal</td><td>시각근거를 명시적으로 검색한 뒤 다단계로 유도하는 문서추론 학습, 정확도 개선폭이 매우 큼</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2609.24186'>LIMIT: Less Is More for Instruction Tuning in Text-to-SQL</a></td><td>32</td><td>0</td><td>NLP</td><td>극소량 정선 데이터로 Text-to-SQL SOTA를 달성, 20배 적은 데이터로 동등 이상 성능을 냄</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2609.24265'>Unsupervised Brain Anomaly Detection as a Bayesian Inverse Problem with Diffusion Prior</a></td><td>32</td><td>0</td><td>CV</td><td>확산모델 사전을 베이지안 역문제로 재정식화해 UAD 성능을 개선, PET/MRI에서 검증함</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2609.24324'>Brain-Token Learning: Microstate-Based Tokenization and Multi-Scale Interaction for Long-Horizon EEG Sequence Modeling</a></td><td>32</td><td>0</td><td>CV</td><td>미소상태 기반 뇌토큰화로 EEG 장기시퀀스를 모델링, 5개 이질적 데이터셋에서 일관된 성능 우위를 보임</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2609.24662'>DUMA-Bench: A Dual-Control Multi-Agent Benchmark for Evaluating LLM Agent Security</a></td><td>32</td><td>0</td><td>AI</td><td>사용자도 환경을 변경할 수 있는 이중통제 상호작용에서 에이전트 보안취약성이 커짐을 실증, 새로운 위협모델을 제시함</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2609.22218'>Toollery: Scaling LLM Agents to Thousands of Skills and Tools</a></td><td>31</td><td>0</td><td>NLP</td><td>수천 개 tool/skill 후보를 압축 검색하는 프레임워크, 에이전트 인프라 최적화 연구임</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2609.22632'>Classification with Abstention Under Class-Conditional Error Constraints</a></td><td>31</td><td>0</td><td>LG</td><td>클래스별 오류 제약 하 abstention 분류의 minimax 이론, 통계학습 이론 연구임</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2609.22850'>Testing the Construct Validity of a Functional Valence Axis in LLM Agents</a></td><td>31</td><td>0</td><td>NLP</td><td>LLM 에이전트의 good-bad 방향이 history-invariant valence인지 검증한 해석연구, maze 실험이나 로봇과 무관함</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2609.22886'>Merge++: Universal Merge Refinement Through Data-Free Checkpoint Inversion</a></td><td>31</td><td>0</td><td>NLP</td><td>체크포인트 역변환으로 합성 이미지를 만들어 모델 병합을 정제하는 data-free 방법론임</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2609.22984'>LPINNs: First-Layer Gated Localization for Physics-Informed Neural Networks</a></td><td>31</td><td>0</td><td>LG</td><td>PINN 첫 레이어에 국소화 함수를 곱해 긴 도메인 최적화를 돕는 경량 개선책임</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2609.22990'>On attention heads and bilinear forms</a></td><td>31</td><td>0</td><td>NLP</td><td>attention head의 bilinear form을 대칭·반대칭으로 분해한 이론 해석 연구임</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2609.23092'>The Role of Coordinates in Pareto Regret for Adversarial Multi-Objective Bandits</a></td><td>31</td><td>0</td><td>RL</td><td>adversarial 다목적 밴딧의 Pareto regret 하한을 규명한 이론 논문임</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2609.23183'>K-TRAIL: Simulator-Guided Generative Design of EM/RF Circuits</a></td><td>31</td><td>0</td><td>LG</td><td>시뮬레이터 피드백으로 RF 회로 레이아웃을 확산모델로 생성하는 방법론임</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2609.23265'>Optimal No-Regret Learning for Repeated Prophet Inequality</a></td><td>31</td><td>0</td><td>LG</td><td>prefix feedback 하 반복 prophet inequality의 최적 후회 알고리즘을 제시한 이론 논문임</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2609.23460'>TRACE: Tractable Routing Autoencoder for Clinical ECG</a></td><td>31</td><td>0</td><td>CV</td><td>사전 정의된 생리학적 잠재공간으로 해석 가능한 ECG 진단 오토인코더임</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2609.23594'>Bilinear Optimization Divergence: Diagnosing Factor-Constrained LoRA Continual Learning</a></td><td>31</td><td>0</td><td>NLP</td><td>LoRA continual learning의 orthogonality 제약이 실제로 보호하는 대상을 anchor-relative 진단으로 규명한 연구임</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2609.23812'>Iterative Atom Refinement: A Monotonicity Principle for Dictionary Learning</a></td><td>31</td><td>0</td><td>LG</td><td>sparse coefficient 관측에서 dictionary atom을 3스텝만에 복원하는 수렴이론 논문임</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2609.24040'>Graph-to-Grid (G2G): Continuous-Coordinate Feature Painting for Soccer Pass Surfaces</a></td><td>31</td><td>0</td><td>CV</td><td>축구 패스 서페이스 예측에 선수 좌표를 연속적으로 그리드에 투영하는 기법임</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2609.24278'>High-Dimensional Online Change Point Detection with Adaptive Thresholding and Interpretability</a></td><td>31</td><td>0</td><td>LG</td><td>Sliced Wasserstein 거리로 고차원 온라인 변화점 탐지를 해석 가능하게 만든 방법임</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2609.24338'>Pharmacokinetic State Space Models for Unbiased Prediction of Haemodynamic Collapse</a></td><td>31</td><td>0</td><td>LG</td><td>약물주입 이력을 반영한 Mamba 기반 저혈압 예측 상태공간모델임</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2609.24679'>Guaranteed Low-Rank Tensor Recovery from Modewise Measurements via Normalized Block-Weighted Riemannian Gradient Descent</a></td><td>31</td><td>0</td><td>LG</td><td>modewise 측정으로부터 저계수 텐서를 복원하는 Riemannian gradient descent 이론 연구임</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2609.24979'>LoRA-generating hypernetworks for efficient on-device LLM generative personalization</a></td><td>31</td><td>0</td><td>NLP</td><td>사용자 컨텍스트로 LoRA를 온디바이스에서 합성하는 하이퍼네트워크 개인화 기법임</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2609.22353'>PAANI : On Device Visual Evidence Fusion and Explainable Guidance for River Robot Simulation</a></td><td>30</td><td>6</td><td>Navigation</td><td>강 모니터링 로봇의 온보드 지각-가이던스 아키텍처, YOLO+세그멘테이션 융합과 ROS2/Gazebo 연동한 실질적 로보틱스 시스템이나 실수상 충돌회피 검증은 미완임</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2609.22493'>Layered e-skin for Shear Sensing</a></td><td>30</td><td>5</td><td>Tactile Perception</td><td>2층 FSR 배열로 전단력까지 추정하는 촉각 센서 하드웨어 논문이며 학습 기반 요소는 CNN-GRU 회귀 정도라 novelty가 제한적임</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2609.22609'>From Documented Strengths to Force Limits: Material-Informed Robotic Insertion for Construction Assembly</a></td><td>30</td><td>5</td><td>Manipulation/Construction</td><td>건설 문서의 재료 강도 정보를 LLM으로 추출해 삽입력 한계로 변환하는 시스템이며 니치한 응용 엔지니어링에 가까움</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2609.23392'>Towards Reliable Underwater Diver-Robot Interaction: Gesture Design, Interaction Logic, and Real-World Evaluation</a></td><td>30</td><td>5</td><td>HRI/Underwater</td><td>다이버-로봇 제스처 어휘와 인식 신뢰도를 사용자 연구로 검증한 응용 HRI 논문으로 방법론적 새로움은 제한적임</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2609.24376'>Multi-Agent Transportation of Free-Flyers in Microgravity Via Pushing Interaction Under Human-in-the-Loop Control</a></td><td>30</td><td>5</td><td>Space Robotics/Control</td><td>미소중력에서 밀기 접촉만으로 자유부유체를 운반하는 CLF-CBF 기반 human-in-the-loop 제어로 니치한 우주로봇 제어이론 기여임</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2609.24846'>Range-Aided SLAM Initialization Exploiting Accurate Heading Information</a></td><td>30</td><td>5</td><td>SLAM/Underwater</td><td>정확한 헤딩 정보를 활용해 range-aided SLAM 초기화를 선형화한 방법으로 AUV 니치 응용에 국한됨</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2609.22795'>Task-Oriented Co-Design and Optimization of Geared Actuators for Robotic Applications</a></td><td>30</td><td>4</td><td>Hardware/Actuator</td><td>모터-기어박스를 태스크 지향으로 공동설계하는 최적화 프레임워크로 액추에이터 하드웨어 기여이며 학습 정책과는 무관함</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2609.22885'>Barrier Certificate Synthesis for Non-Polynomial Robotic Dynamics via Polynomial Lifting</a></td><td>30</td><td>4</td><td>Control Theory</td><td>비다항식 로봇 동역학에 polynomial lifting을 적용해 barrier certificate를 합성하는 제어이론 논문으로 학습 기반 로봇 정책과는 거리가 있음</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2609.24062'>Safety Control of a Hyper-redundant Robot via Adaptive Weighted Control Barrier Functions</a></td><td>30</td><td>4</td><td>Control</td><td>가중 CBF로 초여유자유도 로봇의 하중 불균형 추종오차를 줄인 제어이론 논문으로 학습 기반 정책과 무관함</td></tr>
<tr><td>486</td><td><a href='https://arxiv.org/abs/2609.24832'>Minimum Time Trajectories for a Car-Like Mobile Robot Moving with Rigid Wheels Under Non-Sliding Constraints</a></td><td>30</td><td>4</td><td>Motion Planning/Theory</td><td>비슬립 제약을 반영해 car-like 로봇 시간최적 궤적 primitive를 확장한 고전 궤적최적화 이론 논문임</td></tr>
<tr><td>487</td><td><a href='https://arxiv.org/abs/2609.23507'>Detecting Phone-Induced Pedestrian Distraction via a Multimodal Fusion Transformer</a></td><td>30</td><td>3</td><td>CV</td><td>보행자의 휴대폰 주의분산을 멀티모달 트랜스포머로 탐지해 자율주행 위험 평가에 쓰이는 응용 연구임</td></tr>
<tr><td>488</td><td><a href='https://arxiv.org/abs/2609.24193'>Lightweight Pedestrian Head-Orientation Recognition Network for Safe Pedestrian-Vehicle Interaction</a></td><td>30</td><td>3</td><td>CV</td><td>보행자 머리 방향을 경량 CNN으로 인식해 자율주행 안전에 활용하는 응용 연구로 엔지니어링 기여에 가까움</td></tr>
<tr><td>489</td><td><a href='https://arxiv.org/abs/2609.23293'>Expansion Counts under Standard A* Tie-Breaking Strategies on the Final Plateau</a></td><td>30</td><td>3</td><td>RL</td><td>동일 f값 타이브레이킹 전략별 확장수 차이를 이론적으로 증명, 탐색 알고리즘 이론에 정밀한 기여로 planning에 참고 가치가 있음</td></tr>
<tr><td>490</td><td><a href='https://arxiv.org/abs/2609.23971'>UniK: Universal Knowledge Perception for Digital and Physical AI</a></td><td>30</td><td>3</td><td>Embodied AI</td><td>디지털/물리 AI 지식 파이프라인을 통합한 검색증강 플랫폼, 텍스트 중심 실험이 대부분이고 physical AI 적용은 개념적 주장에 그침</td></tr>
<tr><td>491</td><td><a href='https://arxiv.org/abs/2609.22479'>Spatiotemporal Flux Probing for Single-Photon Videography</a></td><td>30</td><td>2</td><td>CV</td><td>극저조도 단일광자 비디오 복원 연구로 저조도 active perception에 참고 여지는 있으나 로봇 응용은 없음</td></tr>
<tr><td>492</td><td><a href='https://arxiv.org/abs/2609.23372'>Vision-Wireless Fusion for Multi-User Localization: A Cross-Modal Transformer Approach</a></td><td>30</td><td>2</td><td>Navigation</td><td>무선 CSI와 시각 정보를 융합한 다중 사용자 측위 방법으로 로봇 자체보다 인간 측위에 초점이 있음</td></tr>
<tr><td>493</td><td><a href='https://arxiv.org/abs/2609.23431'>HOIBlender: Blending Lightweight Detection with Vision-Language Priors for Efficient Human-Object Interaction Detection</a></td><td>30</td><td>2</td><td>CV</td><td>효율적인 human-object interaction 탐지 방법으로 embodied 이해와 약하게 연결되나 엔지니어링 기여에 가까움</td></tr>
<tr><td>494</td><td><a href='https://arxiv.org/abs/2609.24564'>HyperCLIP++: Fine-tuning CLIP forOpen-vocabulary Semantic Segmentation in Hyperbolic Space</a></td><td>30</td><td>2</td><td>CV</td><td>쌍곡 공간에서 CLIP을 fine-tuning해 open-vocabulary 세그멘테이션을 개선한 연구로 open-world 인식에 참고할 만함</td></tr>
<tr><td>495</td><td><a href='https://arxiv.org/abs/2609.22325'>ReliCAD: From Uncertain LLM Generation to Reliable Parametric CAD Modeling</a></td><td>30</td><td>2</td><td>LG</td><td>LLM의 확률적 생성과 CAD의 결정론적 요구 사이 간극을 design-intent 구조화와 검증-피드백으로 메우는 프레임워크, 로봇 조작 자체와는 거리 있음</td></tr>
<tr><td>496</td><td><a href='https://arxiv.org/abs/2609.22619'>GaitVista: Reliability-Aware AI Measurement toward Accessible Longitudinal Gait Assessment</a></td><td>30</td><td>2</td><td>CV</td><td>카메라/IMU 신뢰도를 프레임 단위로 가중해 보행 측정 오차를 줄이는 방법, 재활 모니터링에 실용적이나 로봇 자체는 아님</td></tr>
<tr><td>497</td><td><a href='https://arxiv.org/abs/2609.22956'>A Compact Stance-Indexed Anterior-Posterior COP Representation for Parkinson&#x27;s Disease Classification from Plantar VGRF</a></td><td>30</td><td>2</td><td>CV</td><td>보행 압력중심을 정상화 스탠스 구간별로 압축한 표현으로 파킨슨병 분류 AUC를 개선, 컴팩트 표현의 판별력을 입증함</td></tr>
<tr><td>498</td><td><a href='https://arxiv.org/abs/2609.22688'>Vision2CAD: A Visual Agent Harness for Explicit Geometry Referencing and Localization in Parametric CAD Modeling</a></td><td>30</td><td>1</td><td>Multimodal</td><td>파라메트릭 CAD 모델링을 위한 VLM 기반 시각 에이전트로 로봇과는 거리가 있는 설계 도구 연구임</td></tr>
<tr><td>499</td><td><a href='https://arxiv.org/abs/2609.22913'>AVTR-1: Open Stack for Real-Time Interactive Avatars</a></td><td>30</td><td>1</td><td>Multimodal</td><td>실시간 대화형 아바타를 위한 오픈 스택 연구로 신체 embodiment 없는 talking-head 시스템이라 로봇과 무관함</td></tr>
<tr><td>500</td><td><a href='https://arxiv.org/abs/2609.23121'>MM-ContextFold: Context Folding for Multimodal Agentic Retrieval</a></td><td>30</td><td>1</td><td>Multimodal</td><td>멀티모달 에이전트 검색에서 시각 토큰 폭증을 접는 context folding 기법으로 로봇 응용은 다루지 않음</td></tr>
<tr><td>501</td><td><a href='https://arxiv.org/abs/2609.23409'>Retrieval Geometry Shapes Cache-Based Clip Adaptation</a></td><td>30</td><td>1</td><td>CV</td><td>캐시 기반 CLIP 테스트타임 적응에서 검색 공간의 기하학적 영향을 분석한 연구로 일반 CV 통찰이라 로봇 적용은 간접적임</td></tr>
<tr><td>502</td><td><a href='https://arxiv.org/abs/2609.23495'>Pay More Attention To Text In High-Resolution MLLMs</a></td><td>30</td><td>1</td><td>Multimodal</td><td>고해상도 MLLM 실패의 원인이 시각이 아니라 질문의 언어적 병목에 있음을 밝힌 연구로 로봇 적용은 제시되지 않음</td></tr>
<tr><td>503</td><td><a href='https://arxiv.org/abs/2609.23509'>GARO: Geometry-Aware Redundancy Optimization for Real-Time and High-Fidelity Dynamic Gaussian Splatting</a></td><td>30</td><td>1</td><td>3D Vision</td><td>동적 3DGS의 중복 Gaussian을 기하 인지 방식으로 줄여 실시간 렌더링을 개선한 엔지니어링 기여임</td></tr>
<tr><td>504</td><td><a href='https://arxiv.org/abs/2609.24208'>CoaG: Cylinders on a Grid: Coarse 3D Layout Control for Video Generation</a></td><td>30</td><td>1</td><td>Video</td><td>바닥 그리드와 실린더만으로 인물 배치·카메라 이동을 제어하는 coarse 3D layout 비디오 생성 도구로 시뮬레이션 데이터 생성에 참고할 여지는 있으나 로봇 연구는 아님</td></tr>
<tr><td>505</td><td><a href='https://arxiv.org/abs/2609.22409'>Contextual Causality with Large Language Models: A Survey</a></td><td>30</td><td>1</td><td>NLP</td><td>LLM과 맥락적 인과관계 연구를 정리한 서베이, causal reasoning 우선주제와 맞닿지만 로봇 적용은 없음</td></tr>
<tr><td>506</td><td><a href='https://arxiv.org/abs/2609.22410'>Learning 3D biophysical cell properties from 2D images and cell-population statistics</a></td><td>30</td><td>1</td><td>CV</td><td>집단통계만으로 2D 이미지에서 3D 세포 특성을 추론하는 약지도 프레임워크, 식별가능성 조건을 이론적으로 규명함</td></tr>
<tr><td>507</td><td><a href='https://arxiv.org/abs/2609.22775'>DVA-Neurons: Design and Verification of Adaptive LIF Neurons: From Single-Neuron Dynamics to Multi-Neuron Spiking Networks</a></td><td>30</td><td>1</td><td>LG</td><td>적응형 LIF 뉴런을 단일-다중 스케일로 설계/검증한 뉴로모픽 하드웨어 연구, 효율적 추론 하드웨어에 기여하나 로봇 응용은 명시되지 않음</td></tr>
<tr><td>508</td><td><a href='https://arxiv.org/abs/2609.24277'>How Many Pixels Is a Digit Worth? Place-Aware Coordinate Entropy for GUI Agent Confidence Estimation</a></td><td>30</td><td>1</td><td>Multimodal</td><td>좌표토큰의 자릿값을 반영한 엔트로피로 GUI 에이전트 클릭 신뢰도를 추정, 단일 forward pass로 K-샘플 기법을 능가함</td></tr>
<tr><td>509</td><td><a href='https://arxiv.org/abs/2609.23655'>Reassessing Global Gradient-Norm Imbalance in BLIP Fine-Tuning Across Physical Domains</a></td><td>30</td><td>0</td><td>Multimodal</td><td>BLIP fine-tuning에서 gradient-norm 불균형 교정의 전제를 재검증한 실증 연구로 로봇과 무관함</td></tr>
<tr><td>510</td><td><a href='https://arxiv.org/abs/2609.23967'>Rethinking Diffusion Segmentation: When Does It Rely on Its Noisy State, and Does Diffusion Matter?</a></td><td>30</td><td>0</td><td>CV</td><td>diffusion 기반 세그멘테이션이 실제로 noisy state에 의존하는지 검증한 방법론 분석 연구로 로봇과 무관함</td></tr>
<tr><td>511</td><td><a href='https://arxiv.org/abs/2609.24919'>PixelDiT2: Representation-Grounded Pixel Diffusion Transformers</a></td><td>30</td><td>0</td><td>CV</td><td>픽셀 공간 diffusion에 명시적 표현 prior를 도입해 품질과 수렴을 개선한 생성모델 연구로 로봇과 무관함</td></tr>
<tr><td>512</td><td><a href='https://arxiv.org/abs/2609.22109'>A Shared Learning Rate Is Not a Neutral Control in Selective On-Policy Distillation</a></td><td>30</td><td>0</td><td>LG</td><td>selective on-policy distillation 비교에서 공유 학습률이 중립적이지 않음을 실증한 방법론적 연구로 로봇과 무관함</td></tr>
<tr><td>513</td><td><a href='https://arxiv.org/abs/2609.22199'>Improving Parameter Utilization by Sharing Neural Experts Across Layers in Transformers</a></td><td>30</td><td>0</td><td>NLP</td><td>레이어 간 expert 공유로 파라미터 효율 개선한 MoE 구조, 경량화 중심 기여라 우선순위 낮음</td></tr>
<tr><td>514</td><td><a href='https://arxiv.org/abs/2609.22094'>Summarize, Judge, Refine: Decoupled Content Understanding and Policy Learning for Multimodal Content Moderation</a></td><td>30</td><td>0</td><td>Multimodal/NLP</td><td>멀티모달 콘텐츠 이해와 정책 분류를 텍스트 요약으로 분리한 조정 시스템으로 콘텐츠 모더레이션 응용이며 로보틱스와 무관함</td></tr>
<tr><td>515</td><td><a href='https://arxiv.org/abs/2609.22100'>AdaMem: Adaptive Memory Token Allocation for Soft Compression in Retrieval-Augmented Generation</a></td><td>30</td><td>0</td><td>NLP/RAG</td><td>질의 관련도에 따라 메모리 토큰을 차등 배분하는 RAG 압축 기법으로 로보틱스 관련성이 없는 검색증강 생성 연구임</td></tr>
<tr><td>516</td><td><a href='https://arxiv.org/abs/2609.22114'>An Empirical Cost Attribution of Context-Compression Gateways in Multi-Turn Coding Agents</a></td><td>30</td><td>0</td><td>NLP/Systems</td><td>코딩 에이전트의 컨텍스트 압축 게이트웨이 비용을 턴 수에 따라 분해한 실증 분석으로 로보틱스와는 관련 없는 시스템 비용 연구임</td></tr>
<tr><td>517</td><td><a href='https://arxiv.org/abs/2609.22127'>Beyond Accuracy and Surface Fluency: Risk-Sensitive Evaluation of LLMs for Legal Clause Generation</a></td><td>30</td><td>0</td><td>NLP/Legal</td><td>계약 조항 생성 LLM을 최대심각도 원칙으로 평가하는 법률 도메인 프레임워크로 로보틱스와 관련 없음</td></tr>
<tr><td>518</td><td><a href='https://arxiv.org/abs/2609.22136'>DiFA: Dual Evidence Fusion and Aggregation for Token-Level Text Anomaly Detection</a></td><td>30</td><td>0</td><td>NLP/Anomaly Detection</td><td>형태-구조와 의미 두 관점의 이상탐지 점수를 적응적으로 융합하는 토큰수준 텍스트 이상탐지 기법으로 로보틱스와 무관함</td></tr>
<tr><td>519</td><td><a href='https://arxiv.org/abs/2609.22149'>Beyond the Stitching Assumption: A Unified Framework for Multimodal Synthetic Data Evaluation via Semantic Quantization</a></td><td>30</td><td>0</td><td>Multimodal/Evaluation</td><td>표-텍스트 짝을 흩트려도 개별 모달리티 지표는 높게 유지되는 문제를 semantic quantization으로 검출하는 합성데이터 평가 프레임워크로 로보틱스와 무관함</td></tr>
<tr><td>520</td><td><a href='https://arxiv.org/abs/2609.22212'>A Channel-Boosted Multi-Agent System with Iterative Consultation for Document Sensitivity Classification</a></td><td>30</td><td>0</td><td>NLP/Classification</td><td>문서 민감도 분류를 위한 채널부스팅 다중에이전트 상담 시스템으로 긴 문서의 절단 문제를 완화하지만 로보틱스와 무관함</td></tr>
<tr><td>521</td><td><a href='https://arxiv.org/abs/2609.22255'>Deep Persona: A Psychologically Grounded Architecture and Evaluation Framework for Role-Playing Agents and Simulations</a></td><td>30</td><td>0</td><td>NLP</td><td>심리학 기반 계층적 페르소나 아키텍처로 롤플레잉 agent 일관성 개선 시도, 실증 강도는 약함</td></tr>
<tr><td>522</td><td><a href='https://arxiv.org/abs/2609.22259'>Which Part of the Context Layer Does the Work? Separating Semantic Content from Retrieval Scaffolding in Text-to-SQL Agents</a></td><td>30</td><td>0</td><td>NLP</td><td>context layer의 의미 콘텐츠와 retrieval scaffolding 기여를 분리한 통제 실험, 실용적이나 text-to-SQL에 국한됨</td></tr>
<tr><td>523</td><td><a href='https://arxiv.org/abs/2609.22988'>Rethinking Pivot Programming Languages in Code Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>코드 LM의 피벗 언어 논쟁을 기하학적으로 재검증, Python의 역할을 영어 친화성으로 재해석함</td></tr>
<tr><td>524</td><td><a href='https://arxiv.org/abs/2609.23088'>OmniEdu: Open Foundation Models for Learning and Teaching</a></td><td>30</td><td>0</td><td>NLP</td><td>K-12 교육 특화 파운데이션 모델, 커리큘럼 기반 데이터 큐레이션으로 벤치마크 전반을 개선함</td></tr>
<tr><td>525</td><td><a href='https://arxiv.org/abs/2609.23239'>SoK: Formal Methods for Fact-Checking and Information Integrity</a></td><td>30</td><td>0</td><td>NLP</td><td>팩트체킹 파이프라인을 형식검증 관점에서 정리한 SoK, 121편 분류가 기여임</td></tr>
<tr><td>526</td><td><a href='https://arxiv.org/abs/2609.23697'>Distill What You Trust: Reliability-Aware Multi-Teacher On-Policy Distillation</a></td><td>30</td><td>0</td><td>LG</td><td>다중 teacher distillation을 토큰 단위 신뢰도로 재가중, 회수율 개선폭이 큼</td></tr>
<tr><td>527</td><td><a href='https://arxiv.org/abs/2609.23742'>Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap</a></td><td>30</td><td>0</td><td>NLP</td><td>제약 디코딩이 구조 실패는 없애지만 의미 정확도 격차는 스케일 의존적임을 실증한 유용한 부정적 결과임</td></tr>
<tr><td>528</td><td><a href='https://arxiv.org/abs/2609.23939'>XYEval: Agents say yes to bad advice</a></td><td>30</td><td>0</td><td>NLP</td><td>agent가 사용자 오도 제안에 취약함을 측정하는 메타평가 프레임워크, XY 문제를 에이전틱 세팅으로 확장함</td></tr>
<tr><td>529</td><td><a href='https://arxiv.org/abs/2609.24052'>Calibrated Decisions at Scale: Converting Police Crash Narratives into Probabilistic Crash Variables with a System One Model (Jev)</a></td><td>30</td><td>0</td><td>NLP</td><td>50만건 교통사고 서술문을 타입드 모델로 코딩, 대규모 실배포 검증이 강점이나 로봇과 무관함</td></tr>
<tr><td>530</td><td><a href='https://arxiv.org/abs/2609.24122'>Re:CAP - Auditing Retrieval Coverage in Production RAG Pipelines</a></td><td>30</td><td>0</td><td>NLP</td><td>배포된 RAG의 누락 문서를 참조없이 감사하는 반복 프로빙 방법, 회수율 개선 실증이 탄탄함</td></tr>
<tr><td>531</td><td><a href='https://arxiv.org/abs/2609.24698'>Adapting Tree-Structured Speculative Decoding to DeepSeek-V4 for Efficient Inference</a></td><td>30</td><td>0</td><td>LG</td><td>압축 어텐션 하에서도 트리 추론이 선형 대비 일관되게 우월함을 보인 시스템 최적화 연구임</td></tr>
<tr><td>532</td><td><a href='https://arxiv.org/abs/2609.24799'>When Quantization Preserves Accuracy but Not Evidence: Explanation-Aware Post-Training Quantization for Medical LLMs</a></td><td>30</td><td>0</td><td>NLP</td><td>PTQ가 정답은 유지해도 근거 토큰의 충실성을 해친다는 의료 LLM 관찰, 양자화 평가기준 확장 필요성을 제시함</td></tr>
<tr><td>533</td><td><a href='https://arxiv.org/abs/2609.24911'>SocioVerse2: A Longitudinal Dynamic Social Simulation Framework under a Human-AI Co-evolutionary Paradigm</a></td><td>30</td><td>0</td><td>AI</td><td>개입 가능하고 연구자 통제 가능한 종단 사회 시뮬레이션 인프라, 다양한 사례연구로 검증함</td></tr>
<tr><td>534</td><td><a href='https://arxiv.org/abs/2609.24971'>DolphinBench: Mapping the Pareto Frontier of Agent Memory</a></td><td>30</td><td>0</td><td>LG</td><td>비용/지연을 포함해 에이전트 메모리를 태스크 완수로 직접 평가하는 벤치마크, 기존 벤치마크 사각지대를 보완함</td></tr>
<tr><td>535</td><td><a href='https://arxiv.org/abs/2609.22478'>Replication Without Persistence in Hosted LLMs: Measurement Sensitivity in Action-Time Belief Evaluation</a></td><td>30</td><td>0</td><td>AI</td><td>호스팅 LLM 행동평가가 설정 재구성만으로도 달라짐을 실증, 평가 방법론에 중요한 경고를 줌</td></tr>
<tr><td>536</td><td><a href='https://arxiv.org/abs/2609.23806'>WorkWorlds: An Infrastructure for Evaluating AI Agents on Workplace Tasks</a></td><td>30</td><td>0</td><td>AI</td><td>조직상태와 과업명세를 분리해 평가 편향을 드러내는 직장 에이전트 평가 인프라, 방법론적으로 흥미로운 발견임</td></tr>
<tr><td>537</td><td><a href='https://arxiv.org/abs/2609.23953'>Agents That Edit Documents: Measuring Agentic PDF Forgery Against a Non-Agentic Control</a></td><td>30</td><td>0</td><td>AI</td><td>코딩에이전트의 문서위조 성공률을 결정론적 규칙으로 측정한 레드팀 연구, AI 오남용 위험을 정량화함</td></tr>
<tr><td>538</td><td><a href='https://arxiv.org/abs/2609.24012'>Testing, not presuming, adequacy: calibrating generative social simulators against emergent network structure</a></td><td>30</td><td>0</td><td>AI</td><td>생성형 사회시뮬레이터 검증에 사후예측 적정성 체크를 도입한 방법론 연구, 실제 리세일시장 사례로 한계까지 투명하게 보고함</td></tr>
<tr><td>539</td><td><a href='https://arxiv.org/abs/2609.24517'>Not All Task Vectors Need Equal Rank: Energy-Proportional Allocation for Model Merging</a></td><td>30</td><td>0</td><td>CV</td><td>태스크벡터의 스펙트럼 에너지에 비례해 랭크를 할당하는 모델병합 기법, 동일 예산에서 성능을 개선함</td></tr>
<tr><td>540</td><td><a href='https://arxiv.org/abs/2609.24921'>BackTrend: Evaluating Scientific Weak-Signal Prediction via Backward Reconstruction</a></td><td>30</td><td>0</td><td>NLP</td><td>과학적 약한신호를 역방향으로 복원해 예측하는 벤치마크, 최고 시스템도 F1 10%대에 그쳐 현 시스템 한계를 명확히 드러냄</td></tr>
<tr><td>541</td><td><a href='https://arxiv.org/abs/2609.22258'>RS-Claw-Evolution: Environment-Feedback-Driven Evolution for Lightweight Remote Sensing Agents in Long-Horizon Tasks</a></td><td>29</td><td>1</td><td>CV</td><td>경량 원격탐사 에이전트를 환경 피드백으로 점진 개선, 로봇 조작과는 다른 도메인 에이전트 연구임</td></tr>
<tr><td>542</td><td><a href='https://arxiv.org/abs/2609.23590'>Cost-Aware Reinforcement Learning with Action Masking and Projection for Battery Energy Storage Dispatch under Suppressed-Spread Market Shifts</a></td><td>29</td><td>1</td><td>RL</td><td>배터리 디스패치를 위한 action masking+projection 안전 RL, 물리적 제약 강제 아이디어가 로봇 안전제어와 유사하나 도메인은 다름</td></tr>
<tr><td>543</td><td><a href='https://arxiv.org/abs/2609.22191'>WildfireSpreadBench: The Metric Decides the Model in Wildfire Spread Prediction</a></td><td>29</td><td>0</td><td>CV</td><td>산불 확산 예측 평가지표(AP vs F1/IoU) 문제를 지적한 벤치마크 논문, 메트릭 선택 중요성만 보임</td></tr>
<tr><td>544</td><td><a href='https://arxiv.org/abs/2609.22216'>The Effect of Quantization on Clinical Benchmarks: Accuracy and Safety Across Model Families</a></td><td>29</td><td>0</td><td>NLP</td><td>임상 LLM 양자화가 정확도·안전성에 미치는 영향 분석, 의료 도메인 벤치마크 연구임</td></tr>
<tr><td>545</td><td><a href='https://arxiv.org/abs/2609.22230'>List Counting Failures Are Not One Phenomenon</a></td><td>29</td><td>0</td><td>NLP</td><td>LLM의 리스트 개수 세기 오류가 모델마다 다른 양상임을 보인 해석연구, 로봇과 무관함</td></tr>
<tr><td>546</td><td><a href='https://arxiv.org/abs/2609.22233'>SCALE: Simulation-Calibrated Amortized Learning for Energy Materials (A hybrid architecture connecting deterministic modeling, real-world data, and transformer-scale inference for accelerated energy-materials discovery)</a></td><td>29</td><td>0</td><td>LG</td><td>물리 시뮬레이션 보정 학습으로 에너지 소재 스크리닝 가속, 응용 소재과학 연구임</td></tr>
<tr><td>547</td><td><a href='https://arxiv.org/abs/2609.22487'>COREM: Cosine-Relation Momentum Reshaping with Stateful Writeback</a></td><td>29</td><td>0</td><td>LG</td><td>옵티마이저 모멘텀을 cosine relation으로 재구성하는 방법, optimizer 연구로 로봇과 무관함</td></tr>
<tr><td>548</td><td><a href='https://arxiv.org/abs/2609.22783'>Improved Private Sparse Covariance Estimation with Multiscale Threshold Tests</a></td><td>29</td><td>0</td><td>LG</td><td>sparse covariance의 차분사생활 추정 샘플복잡도를 개선한 이론 논문임</td></tr>
<tr><td>549</td><td><a href='https://arxiv.org/abs/2609.22866'>Causilo Technical Report</a></td><td>29</td><td>0</td><td>LG</td><td>빠른 추론 속도를 갖는 테이블 파운데이션 모델, 효율-성능 파레토 개선 응용 연구임</td></tr>
<tr><td>550</td><td><a href='https://arxiv.org/abs/2609.22870'>Towards Full Pipeline FP8 Reinforcement Learning for LLMs</a></td><td>29</td><td>0</td><td>NLP</td><td>FP8 quantization RL 파이프라인의 불안정성 원인을 규명하고 clipping 교정, LLM RL 인프라 연구임</td></tr>
<tr><td>551</td><td><a href='https://arxiv.org/abs/2609.22943'>Token Utility Is Selection-Conditioned: Coupled Selection of Prompt Context and Response Supervision for Efficient Instruction Tuning</a></td><td>29</td><td>0</td><td>NLP</td><td>prompt-response 선택을 상호조건부로 결합한 효율적 instruction tuning 토큰 선택법임</td></tr>
<tr><td>552</td><td><a href='https://arxiv.org/abs/2609.23033'>WaveFront Decoding: Parallelized Self-Speculative Decoding for Looped Language Models</a></td><td>29</td><td>0</td><td>NLP</td><td>looped LM의 recurrence를 활용한 self-speculative decoding으로 속도 개선, 추론 효율화 연구임</td></tr>
<tr><td>553</td><td><a href='https://arxiv.org/abs/2609.23314'>ValueDiff: Value-Geometric KV Cache Eviction for Sink-Suppressed LLMs</a></td><td>29</td><td>0</td><td>NLP</td><td>sink가 약한 LLM에서 value-vector 분산 기반 KV cache eviction 기법임</td></tr>
<tr><td>554</td><td><a href='https://arxiv.org/abs/2609.23325'>Rethinking Class Imbalance for Single-Cell Foundation Models: A Systematic Benchmark Across Architectures and Long-Tail Loss Functions</a></td><td>29</td><td>0</td><td>LG</td><td>single-cell 파운데이션 모델의 long-tail loss 선택을 체계적으로 벤치마크한 연구임</td></tr>
<tr><td>555</td><td><a href='https://arxiv.org/abs/2609.23374'>The Evidence Ladder for Reinforcement Learning in Healthcare: From Retrospective Policies to Trusted Interventions</a></td><td>29</td><td>0</td><td>RL</td><td>헬스케어 RL을 evidence ladder로 정리한 리뷰 성격 논문, 새로운 방법 제시는 없음</td></tr>
<tr><td>556</td><td><a href='https://arxiv.org/abs/2609.23547'>Preserving Geometric Integrity in Graph Prompting via Measure-Constrained Optimal Transport</a></td><td>29</td><td>0</td><td>LG</td><td>그래프 프롬프트 라우팅의 붕괴를 measure-constrained OT로 방지하는 방법임</td></tr>
<tr><td>557</td><td><a href='https://arxiv.org/abs/2609.23688'>Tail-Weight Control and Localized Generalization in Nearly Low-Rank Adversarial Classification</a></td><td>29</td><td>0</td><td>LG</td><td>저차원 informative subspace를 갖는 adversarial 분류의 tail-weight 이론 분석임</td></tr>
<tr><td>558</td><td><a href='https://arxiv.org/abs/2609.23843'>Adaptive Determinantal Client Scheduling in Federated Learning</a></td><td>29</td><td>0</td><td>LG</td><td>DPP로 클라이언트 다양성을 고려한 연합학습 스케줄링 기법임</td></tr>
<tr><td>559</td><td><a href='https://arxiv.org/abs/2609.23845'>PROSE: A Theory of Optimal Stopping with Perishable Evidence for Peer Selection in Intermittently Connected Decentralised Learning</a></td><td>29</td><td>0</td><td>LG</td><td>간헐적으로 연결된 분산학습의 peer selection을 optimal stopping 이론으로 정식화, 실험 없는 이론 논문임</td></tr>
<tr><td>560</td><td><a href='https://arxiv.org/abs/2609.23876'>GLR-MM: Graph-Based Global-Local Reconstruction for Robust Multimodal Chest X-ray and EHR Representation Learning under Missing Modalities</a></td><td>29</td><td>0</td><td>Multimodal</td><td>흉부X선-EHR 결측 모달리티 재구성을 위한 그래프 기반 프레임워크, 의료 응용 연구임</td></tr>
<tr><td>561</td><td><a href='https://arxiv.org/abs/2609.23900'>GDN Tree-Scan: Served Tree Verification for Recurrent-Hybrid Language Models</a></td><td>29</td><td>0</td><td>NLP</td><td>recurrent-hybrid LM용 tree speculative decoding 서빙 시스템 논문임</td></tr>
<tr><td>562</td><td><a href='https://arxiv.org/abs/2609.23934'>The Neural Forcing for Three-Dimensional Incompressible Navier-Stokes finite time blowup</a></td><td>29</td><td>0</td><td>LG</td><td>3차원 비압축 Navier-Stokes 유한시간 blowup을 위한 신경 강제력 설계 논문임</td></tr>
<tr><td>563</td><td><a href='https://arxiv.org/abs/2609.23990'>MGRD: Compact morphology-gated residual diffusion for variance-aware cross-domain neurite forecasting</a></td><td>29</td><td>0</td><td>LG</td><td>뉴라이트 형태 변화를 확률적으로 예측하는 경량 확산 서로게이트 모델임</td></tr>
<tr><td>564</td><td><a href='https://arxiv.org/abs/2609.23995'>Simpler Methods Work Better for L1 Penalized Logistic Models and Large Datasets</a></td><td>29</td><td>0</td><td>LG</td><td>L1 로지스틱 회귀에서 최신 solver보다 구식 방법이 실무에 더 낫다는 실증 연구임</td></tr>
<tr><td>565</td><td><a href='https://arxiv.org/abs/2609.24003'>ShapeLex: Decoupling Local Shape Symbolization and Global Scale Modeling for Text-Controlled Time Series Generation</a></td><td>29</td><td>0</td><td>LG</td><td>텍스트 조건 시계열 생성을 이산 shape 어휘와 연속 scale로 분리한 방법임</td></tr>
<tr><td>566</td><td><a href='https://arxiv.org/abs/2609.24233'>Adaptive Forgetting for Nonstationary Optimization: Towards Robust EEG Decoding</a></td><td>29</td><td>0</td><td>LG</td><td>cross-subject EEG 디코딩을 위한 텐서별 적응적 second-moment decay 옵티마이저임</td></tr>
<tr><td>567</td><td><a href='https://arxiv.org/abs/2609.24303'>SupportCal: Label-Free Calibration of Post-Trained LLMs via Reference Support and Corroboration</a></td><td>29</td><td>0</td><td>NLP</td><td>사전학습 모델을 label-free reference로 삼아 post-trained LLM 신뢰도를 보정하는 방법임</td></tr>
<tr><td>568</td><td><a href='https://arxiv.org/abs/2609.24394'>Climate Variability Modulates the Impact of Price Spikes on Food Insecurity</a></td><td>29</td><td>0</td><td>LG</td><td>El Nino 민감도 지역별 식량가격 급등 영향을 인과 ML로 추정한 응용 정책 연구임</td></tr>
<tr><td>569</td><td><a href='https://arxiv.org/abs/2609.24629'>Augmented Hypothesis Testing with Persona-Based LLM Simulations</a></td><td>29</td><td>0</td><td>NLP</td><td>페르소나 기반 LLM 시뮬레이션 예측을 A/B 테스트 표본 크기 절감에 활용한 통계적 프레임워크임</td></tr>
<tr><td>570</td><td><a href='https://arxiv.org/abs/2609.24651'>Corrective Forcing: Unified Post-Training for Diffusions and Flows in Generative Speech Enhancement</a></td><td>29</td><td>0</td><td>Multimodal</td><td>학습-추론 불일치를 self-generated rollout에서 교정하는 음성향상용 post-training 방법임</td></tr>
<tr><td>571</td><td><a href='https://arxiv.org/abs/2609.24746'>Enhancing Transformer Representations of Symbolic ODE Expressions</a></td><td>29</td><td>0</td><td>LG</td><td>트리 기반 위치임베딩이 기호 ODE 표현학습을 돕는지 체계적으로 검증한 연구임</td></tr>
<tr><td>572</td><td><a href='https://arxiv.org/abs/2609.24823'>G-NAC: Graph Neural Automata Clustering via Emergent Domain Formation</a></td><td>29</td><td>0</td><td>LG</td><td>그래프 셀룰러 오토마타로 창발적 도메인을 형성하는 비지도 클러스터링 방법임</td></tr>
<tr><td>573</td><td><a href='https://arxiv.org/abs/2609.22404'>Behavior Trees for Robotic Systems: An Empirical Study on Practices and Experiences</a></td><td>28</td><td>6</td><td>Manipulation</td><td>행동트리 실무 관행을 혼합방법으로 조사한 실증연구, 새로운 알고리즘은 아니나 산업 현장의 설계 고충을 정리함</td></tr>
<tr><td>574</td><td><a href='https://arxiv.org/abs/2609.22668'>Density-Driven Area Coverage for Nonholonomic Multi-Robot Systems with Safety Guarantee</a></td><td>28</td><td>4</td><td>Multi-Robot Control</td><td>비완전구속 로봇의 밀도기반 커버리지에 CBF 안전필터를 결합한 제어이론 논문으로 학습 요소 없이 고전 제어 확장임</td></tr>
<tr><td>575</td><td><a href='https://arxiv.org/abs/2609.22954'>MIRA-PRM: Mission-Informed Reusable Roadmap Planning for Mobile Gas-Sensing Inspection</a></td><td>28</td><td>4</td><td>Planning</td><td>가스센싱 순회를 위한 roadmap planning 개선으로 대규모 실험은 꼼꼼하지만 고전 PRM 계열의 공학적 확장임</td></tr>
<tr><td>576</td><td><a href='https://arxiv.org/abs/2609.22963'>Prescribed-Time Contracting-Boundary Control of a Tendon-Driven Flexible Arm</a></td><td>28</td><td>4</td><td>Control</td><td>텐던구동 연성 팔의 곡률 추종을 위한 prescribed-time 제어법으로 이론적으로는 탄탄하나 로봇학습과 무관한 고전 제어 논문임</td></tr>
<tr><td>577</td><td><a href='https://arxiv.org/abs/2609.24499'>A Monolithic Force-Proprioception Soft Acutuator Enabled by Single-Material 3D printing</a></td><td>28</td><td>4</td><td>Hardware/Soft Robotics</td><td>단일 재료 3D프린팅으로 구동과 힘감지를 동시에 구현한 소프트 액추에이터 하드웨어 기여로 학습 요소는 없음</td></tr>
<tr><td>578</td><td><a href='https://arxiv.org/abs/2609.24535'>Estimation and Control of Tensegrity Manipulator Kinematics based on Strut Inclination Angles</a></td><td>28</td><td>4</td><td>Kinematics/Hardware</td><td>텐세그리티 매니퓰레이터의 strut IMU 기반 형상 추정과 PI 자세제어를 실험으로 보인 하드웨어 중심 논문임</td></tr>
<tr><td>579</td><td><a href='https://arxiv.org/abs/2609.24494'>CMAMBADEPTH: Self-supervised Monocular Depth Estimation with Channel Mamba and Hybrid Attention</a></td><td>28</td><td>3</td><td>CV</td><td>Mamba 기반 채널 선택으로 효율적인 자기지도 단안 depth 추정을 개선한 연구로 로봇 perception에 쓰일 수 있으나 효율화 중심임</td></tr>
<tr><td>580</td><td><a href='https://arxiv.org/abs/2609.22483'>Tracker-Free Robotic Ultrasound Calibration with a Spherical-Marker Phantom and Threshold-Free Center Localization</a></td><td>28</td><td>3</td><td>Robotics</td><td>구형 마커 팬텀 기반 초음파 캘리브레이션으로 트래커를 없앤 건 실용적이지만 방법론적으로는 기존 캘리브레이션 파이프라인의 개선 수준임</td></tr>
<tr><td>581</td><td><a href='https://arxiv.org/abs/2609.23060'>On the Control of Mobile Ad-Hoc Agent Deployments in Partially Observed Space</a></td><td>28</td><td>3</td><td>Multi-Robot Theory</td><td>미지 환경에서 art gallery problem 변형으로 통신망 배치를 증명한 이론 논문으로 로봇학습과 거리가 멂</td></tr>
<tr><td>582</td><td><a href='https://arxiv.org/abs/2609.23487'>Design and Control of a Cable-Driven Switchable Actuator with Torque/Tension Dual Modes for Exoskeletons</a></td><td>28</td><td>3</td><td>Hardware/Exoskeleton</td><td>토크-장력 겸용 케이블구동 액추에이터를 제안한 외골격 하드웨어 논문으로 로봇학습 기여는 없음</td></tr>
<tr><td>583</td><td><a href='https://arxiv.org/abs/2609.22897'>Scout: Open-World Species Recognition on the Edge</a></td><td>28</td><td>2</td><td>CV</td><td>야생동물 카메라 트랩용 엣지 open-world 인식 시스템으로 경량화·효율성 중심이라 우선 평가 주제와는 거리가 있음</td></tr>
<tr><td>584</td><td><a href='https://arxiv.org/abs/2609.23010'>MixiMotion: One-Step Text-to-Motion Generation via Asymmetric Set Distillation</a></td><td>28</td><td>2</td><td>CV</td><td>텍스트-모션 생성을 one-step으로 증류하는 방법으로 애니메이션 응용이라 로봇 제어와는 거리가 있음</td></tr>
<tr><td>585</td><td><a href='https://arxiv.org/abs/2609.23067'>LD-RSVIS: A Large-Scale and Diverse Benchmark for Referring Surgical Video Instrument Segmentation</a></td><td>28</td><td>2</td><td>CV</td><td>수술 영상에서 언어로 지칭된 기구를 세그멘테이션하는 대규모 벤치마크로 의료 로봇과 간접적으로만 연결됨</td></tr>
<tr><td>586</td><td><a href='https://arxiv.org/abs/2609.24075'>A paired synthetic construction-site image dataset for robust computer vision under adverse conditions</a></td><td>28</td><td>2</td><td>CV</td><td>악조건 건설현장 컴퓨터비전을 위한 합성 페어 데이터셋으로 필드 로봇 모니터링에 참고할 여지는 있으나 데이터셋 논문에 그침</td></tr>
<tr><td>587</td><td><a href='https://arxiv.org/abs/2609.24337'>LiAuto-MindViT: A Hybrid Vision Backbone with Adaptive Bidirectional Mamba</a></td><td>28</td><td>2</td><td>CV</td><td>CNN·Mamba·Transformer를 결합한 하이브리드 비전 백본으로 효율화 중심이나 자율주행 관련 조직명이 붙어있음</td></tr>
<tr><td>588</td><td><a href='https://arxiv.org/abs/2609.22584'>Augmenting PID Control with Deep Reinforcement Learning: A Hybrid Approach to the Industrial Benchmark</a></td><td>28</td><td>2</td><td>RL</td><td>PID와 DRL을 결합한 하이브리드 산업 제어기, 산업 벤치마크 실험이며 로봇 제어와는 거리 있음</td></tr>
<tr><td>589</td><td><a href='https://arxiv.org/abs/2609.22379'>MarsRecon: Self-Supervised and Multimodal Surface Representations for Mars</a></td><td>28</td><td>1</td><td>3D Vision</td><td>화성 지표 영상용 자기지도 표현학습 파이프라인으로 로버 탐사에 잠재적 연결은 있지만 논문 자체는 지질 표현학습에 국한됨</td></tr>
<tr><td>590</td><td><a href='https://arxiv.org/abs/2609.22849'>LINGO: Latent Initialization and Gradient Optimization for Sparse-view X-ray Novel View Synthesis and CT Reconstruction with 3D Gaussian Splatting</a></td><td>28</td><td>1</td><td>3D Vision</td><td>희소 X-ray 뷰의 3DGS 기반 CT 재구성 연구로 3DGS를 쓰지만 의료 영상 도메인이라 로봇과 무관함</td></tr>
<tr><td>591</td><td><a href='https://arxiv.org/abs/2609.22115'>ZoAQ: Adaptive Zeroth-Order Querying via Query-Reuse Coupling</a></td><td>28</td><td>1</td><td>LG</td><td>과거 평가를 재사용해 쿼리 예산을 적응적으로 배분하는 zeroth-order 최적화 기법으로 일반 최적화 연구이며 로봇 적용은 제시되지 않음</td></tr>
<tr><td>592</td><td><a href='https://arxiv.org/abs/2609.22987'>OptiSkill: A Hierarchical and Evolving SkillBank for LLM-Based Optimization Modeling</a></td><td>28</td><td>1</td><td>LG</td><td>OR 모델링용 재사용 가능한 스킬뱅크를 계층적으로 구축, 정형화 오류 반복 방지에 실질적으로 개선됨</td></tr>
<tr><td>593</td><td><a href='https://arxiv.org/abs/2609.23986'>Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents</a></td><td>28</td><td>1</td><td>LG</td><td>System1/2 분업으로 메모리 구성-검색을 경량화한 에이전트 메모리 아키텍처, 구축속도와 지연 모두 큰 폭 개선됨</td></tr>
<tr><td>594</td><td><a href='https://arxiv.org/abs/2609.22267'>Did You Steal My Shot? Pioneering Camera Motion Plagiarism Detection in Generative Videos</a></td><td>28</td><td>0</td><td>CV</td><td>카메라 모션 표절 탐지 벤치마크인데 로보틱스와 무관하고 detection task incremental engineering에 가까움</td></tr>
<tr><td>595</td><td><a href='https://arxiv.org/abs/2609.22916'>Planning and Rendering in Concert: DeepFusion of Autoregressive Layouts and Diffusion for Visual Text Generation</a></td><td>28</td><td>0</td><td>CV</td><td>레이아웃 계획과 렌더링을 공동학습하는 텍스트 이미지 생성 연구로 로봇과 무관함</td></tr>
<tr><td>596</td><td><a href='https://arxiv.org/abs/2609.23386'>ProxyBuild: Text-Guided Structured 3D Building Generation with Mesh-Anchored Procedural Proxies</a></td><td>28</td><td>0</td><td>CV</td><td>텍스트로 건물을 절차적으로 생성하는 프레임워크로 그래픽스 응용이라 로봇과 무관함</td></tr>
<tr><td>597</td><td><a href='https://arxiv.org/abs/2609.23592'>Collapse, Not Complexity: Failure-Conditioned Decomposition Repair for End-to-End Document Parsing</a></td><td>28</td><td>0</td><td>CV</td><td>문서 파싱에서 reasoning 모드가 언제 도움이 되는지 분석한 연구로 로봇과 무관함</td></tr>
<tr><td>598</td><td><a href='https://arxiv.org/abs/2609.23717'>BindCLIP: One Balanced Coupling For Compositional Vision Language Scoring</a></td><td>28</td><td>0</td><td>Multimodal</td><td>고정된 CLIP 인코더에서 토큰-패치 정렬 구조를 읽어내 compositional scoring을 개선한 연구로 로봇 적용은 없음</td></tr>
<tr><td>599</td><td><a href='https://arxiv.org/abs/2609.23758'>Training-Free Spectral Transductive Refinement for Cross-Domain Few-Shot Classification</a></td><td>28</td><td>0</td><td>CV</td><td>도메인 이동에 강건한 학습 없는 few-shot 분류 테스트타임 기법으로 로봇과 무관함</td></tr>
<tr><td>600</td><td><a href='https://arxiv.org/abs/2609.24071'>Monitorable Chart Reasoning Agents via Verifiable Process Rewards</a></td><td>28</td><td>0</td><td>Multimodal</td><td>차트 추론 과정을 검증 가능한 process reward로 감시하는 에이전트 연구로 도메인이 차트 이해라 로봇과 무관함</td></tr>
<tr><td>601</td><td><a href='https://arxiv.org/abs/2609.24276'>Hierarchical Prompt Learning for Hyperbolic Vision-Language Models</a></td><td>28</td><td>0</td><td>Multimodal</td><td>쌍곡 공간 VLM에 계층적 prompt learning을 적용한 연구로 로봇과 무관함</td></tr>
<tr><td>602</td><td><a href='https://arxiv.org/abs/2609.24612'>Beyond Uniform Subspaces: Spectrum-Aware and Depth-Adaptive Fusion for Multi-Task Model Merging</a></td><td>28</td><td>0</td><td>LG</td><td>태스크별 스펙트럴·깊이 이질성을 고려한 모델 병합 기법으로 로봇과 무관함</td></tr>
<tr><td>603</td><td><a href='https://arxiv.org/abs/2609.24782'>Virtual neural networks: hundreds of souls in a body</a></td><td>28</td><td>0</td><td>CV</td><td>소수의 물리 모델에서 가중치를 공유하는 수백 개의 virtual model을 앙상블하는 새 개념으로 로봇 적용은 없음</td></tr>
<tr><td>604</td><td><a href='https://arxiv.org/abs/2609.22217'>UniGIO: Unified Generative Global In-situ Weather Modeling from Spatiotemporal Incomplete Observations</a></td><td>28</td><td>0</td><td>LG</td><td>전지구 관측소 결측 날씨 데이터 생성 프레임워크, 응용 기상 연구임</td></tr>
<tr><td>605</td><td><a href='https://arxiv.org/abs/2609.24401'>Artificial Structure Function Search: Preserving Artificial Functional Connectivity for Structured Pruning</a></td><td>28</td><td>0</td><td>CV</td><td>뇌의 structure-function 관계에서 영감받은 구조적 프루닝 기법, 경량화 중심 연구임</td></tr>
<tr><td>606</td><td><a href='https://arxiv.org/abs/2609.24441'>MUSE: Dependency-Aware Adaptation of a Frozen Vision Backbone for Multivariate Time Series Forecasting</a></td><td>28</td><td>0</td><td>LG</td><td>고정된 vision backbone을 다변량 시계열 예측에 적응시키는 dependency-aware 프레임워크임</td></tr>
<tr><td>607</td><td><a href='https://arxiv.org/abs/2609.24464'>RAILS: Retrieval-Augmented Incremental LLM Clustering at Scale</a></td><td>28</td><td>0</td><td>NLP</td><td>성장하는 라벨 풀에 대한 retrieval 기반 증분 LLM 클러스터링 시스템, 프로덕션 배포 사례 포함함</td></tr>
<tr><td>608</td><td><a href='https://arxiv.org/abs/2609.22097'>Token Signatures of Code: Comparing Coding Behaviors Across Large Language Models</a></td><td>28</td><td>0</td><td>NLP/Code</td><td>코드 생성 LLM들의 토큰 사용 패턴을 시각분석 도구로 비교한 연구로 로보틱스와 무관함</td></tr>
<tr><td>609</td><td><a href='https://arxiv.org/abs/2609.22112'>Privacy Personalization Trade offs in LLMs: The Impact of Stylometric Signal Reduction on User-Specific Text Generation</a></td><td>28</td><td>0</td><td>NLP/Privacy</td><td>문체 신호를 줄이면 LLM 개인화 품질이 얼마나 떨어지는지 측정한 프라이버시-개인화 트레이드오프 연구로 로보틱스와 무관함</td></tr>
<tr><td>610</td><td><a href='https://arxiv.org/abs/2609.22164'>A Multi-Agent Pipeline for Source-Grounded Synthetic Note Generation from Longitudinal Structured EHR</a></td><td>28</td><td>0</td><td>NLP/Healthcare</td><td>구조화된 EHR을 근거로 임상노트를 합성 생성하는 다중 에이전트 파이프라인으로 헬스케어 응용이며 로보틱스와 무관함</td></tr>
<tr><td>611</td><td><a href='https://arxiv.org/abs/2609.22171'>Quantifying Hidden Salt for Precision Healthcare: Sodium Assessment via Joint-Factor Retrieval and Chain-of-Thought Inference</a></td><td>28</td><td>0</td><td>NLP/Healthcare</td><td>레시피의 숨은 나트륨 함량을 RAG와 4단계 CoT로 추정하는 헬스케어 응용 연구로 로보틱스와 무관함</td></tr>
<tr><td>612</td><td><a href='https://arxiv.org/abs/2609.22209'>Schematize: An Agentic System for Generating and Refining Information-Extraction Schemas for Legal Research</a></td><td>28</td><td>0</td><td>NLP/Legal</td><td>법률 연구를 위한 정보추출 스키마를 대화형으로 생성·정제하는 에이전트 시스템 데모로 로보틱스와 무관함</td></tr>
<tr><td>613</td><td><a href='https://arxiv.org/abs/2609.22210'>SALSA: Semi-Autonomous Literature Summarization Assistant</a></td><td>28</td><td>0</td><td>NLP/Tool</td><td>문헌에서 구조화 데이터를 반자동으로 추출하는 human-in-the-loop 도구로 재료과학 문헌 큐레이션에 초점을 맞춰 로보틱스와 무관함</td></tr>
<tr><td>614</td><td><a href='https://arxiv.org/abs/2609.22214'>The Bairong System for MLC-SLM 2026: Dynamic Question-Aware Evidence Routing for Multilingual Conversational Speech Understanding</a></td><td>28</td><td>0</td><td>NLP/Speech</td><td>다국어 대화형 음성질의응답을 위한 동적 증거 라우팅 대회 시스템으로 로보틱스와 무관함</td></tr>
<tr><td>615</td><td><a href='https://arxiv.org/abs/2609.22221'>Team DArgk at the 2026 ELOQUENT lab for evaluating generative language model quality: Residuals of Humanity: AI Detection Evasion via GRPO Fine-Tuning</a></td><td>28</td><td>0</td><td>NLP/Adversarial</td><td>GRPO로 AI 텍스트 탐지기를 회피하도록 LLM을 강화학습시킨 대회 참가 리포트로 로보틱스와 무관함</td></tr>
<tr><td>616</td><td><a href='https://arxiv.org/abs/2609.22235'>BizSage: A Self-Evolving Multi-Agent Framework for Business Research with Efficient Knowledge Retrieval</a></td><td>28</td><td>0</td><td>NLP</td><td>business/economics 연구용 multi-agent RAG 프레임워크, retrieval 세분화와 self-evolution 결합한 엔지니어링 기여로 로보틱스와 무관함</td></tr>
<tr><td>617</td><td><a href='https://arxiv.org/abs/2609.22362'>Functional Emotion Without Character: Large Language Models, Aristotelian Disposition, and the Limits of Behavioral Alignment</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM 감정 표현을 아리스토텔레스 개념으로 재구성한 이론 논문, 실증 검증 없이 개념 틀만 제시함</td></tr>
<tr><td>618</td><td><a href='https://arxiv.org/abs/2609.22452'>Vox-Infinity: Benchmarking the Limits of Long-Context Spoken Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>음성 LM의 장문 맥락 이해 벤치마크, recency effect 확인이 주된 발견임</td></tr>
<tr><td>619</td><td><a href='https://arxiv.org/abs/2609.22553'>Correct Diagnosis, Better Feedback: A Symbolic-Verifier for Faithful LLM Tutoring Feedback in Logic Proofs</a></td><td>28</td><td>0</td><td>NLP</td><td>논리 증명 튜터링에서 진단-피드백을 분리한 verifier 구조, 견고하나 범위가 좁음</td></tr>
<tr><td>620</td><td><a href='https://arxiv.org/abs/2609.22603'>Preserving What Matters: Semantic Scaffolds Beyond Saturation in Summarization Evaluation</a></td><td>28</td><td>0</td><td>NLP</td><td>요약 평가에서 LLM-judge 포화 문제를 사실/질문/엔티티 보존 지표로 보완한 평가 방법론 기여</td></tr>
<tr><td>621</td><td><a href='https://arxiv.org/abs/2609.22697'>COT-TTS: Audio Context-Aware Text-to-Speech with Chain-of-Thought Reasoning</a></td><td>28</td><td>0</td><td>NLP</td><td>대화 맥락 기반 CoT로 스타일을 추론하는 TTS, 데이터셋과 베이스라인 구축 위주 응용 연구임</td></tr>
<tr><td>622</td><td><a href='https://arxiv.org/abs/2609.22778'>MIS-Bench: Benchmarking Multimodal LLMs for Psychotherapeutic Interpersonal Skills Assessment</a></td><td>28</td><td>0</td><td>Multimodal</td><td>심리치료 대인기술 평가 벤치마크와 회귀인지 파인튜닝 방법, MLLM과 전문가 판단 격차를 확인함</td></tr>
<tr><td>623</td><td><a href='https://arxiv.org/abs/2609.22934'>Measuring Behavioural Signatures of Large Language Models through Psychometric Profiling</a></td><td>28</td><td>0</td><td>NLP</td><td>심리검사로 LLM 행동 시그니처를 측정한 분석, 응답거부 패턴 등 관찰은 흥미로우나 로봇과 무관함</td></tr>
<tr><td>624</td><td><a href='https://arxiv.org/abs/2609.23551'>Paragraph Boundaries Are Not White Space:Compression Depth as the Signature of Hierarchical Structure</a></td><td>28</td><td>0</td><td>NLP</td><td>계층적 위치 인코딩에서 압축 깊이가 진짜 구조의 신호임을 실험적으로 규명함</td></tr>
<tr><td>625</td><td><a href='https://arxiv.org/abs/2609.23716'>STEVE: Stabilizing Textual Gradient-Based Prompt Optimization via Error-Driven Refinement and Regularized Verification</a></td><td>28</td><td>0</td><td>LG</td><td>텍스트 그래디언트 프롬프트 최적화의 불안정성을 오류기반 정제와 정규화 검증으로 완화함</td></tr>
<tr><td>626</td><td><a href='https://arxiv.org/abs/2609.23959'>Open-Jev Judgments on CallScreenBench: Calibrated One-Pass Scam Screening with a Small Language Model</a></td><td>28</td><td>0</td><td>NLP</td><td>타입드 결정 모델을 보이스피싱 스크리닝에 적용, 정확도보다 캘리브레이션과 지연시간 개선이 기여임</td></tr>
<tr><td>627</td><td><a href='https://arxiv.org/abs/2609.24156'>TAC-Time: Texts as Channels For Multimodal Time Series Forecasting</a></td><td>28</td><td>0</td><td>Multimodal</td><td>텍스트를 시계열 채널로 통합하는 멀티모달 예측 프레임워크, 해석가능성 분석을 포함함</td></tr>
<tr><td>628</td><td><a href='https://arxiv.org/abs/2609.24238'>Memory vs. Context? Influential Factors of Factual Recall in Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>기존 연구 재현과 5개 관계유형 확장, 질문 표현만으로 신뢰도가 80%p 흔들림을 확인함</td></tr>
<tr><td>629</td><td><a href='https://arxiv.org/abs/2609.24275'>Structure Before Sampling: Community-Aware Core-Set Selection for Data-Efficient Text-to-Speech</a></td><td>28</td><td>0</td><td>NLP</td><td>음소 그래프 커뮤니티 기반 코어셋 선택으로 데이터 효율적 TTS 학습, CER 개선이 명확함</td></tr>
<tr><td>630</td><td><a href='https://arxiv.org/abs/2609.24574'>Evaluating Decision Models for Text Annotation in Computational Social Science</a></td><td>28</td><td>0</td><td>NLP</td><td>저비용 결정모델의 사회과학 분류 정확도/캘리브레이션을 프론티어 LLM과 비교, 저비용 1차 필터로서 실용성을 확인함</td></tr>
<tr><td>631</td><td><a href='https://arxiv.org/abs/2609.22161'>Didactic knowledge or Clinical Cases? How Data Types Shape Medical Large Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>교과서/임상데이터 비율이 의료 LLM 능력에 비대칭적 영향을 줌을 토큰매칭 실험으로 규명함</td></tr>
<tr><td>632</td><td><a href='https://arxiv.org/abs/2609.22760'>CTSpinoPelvic1K: spine, pelvis, ribs and femora in one coordinate frame, annotated for lumbosacral transitional anatomy</a></td><td>28</td><td>0</td><td>CV</td><td>척추-골반-늑골을 한 좌표계로 통합한 CT 주석 데이터셋, 임상해부학적 모호성 해결에 유용한 자원임</td></tr>
<tr><td>633</td><td><a href='https://arxiv.org/abs/2609.22951'>AgentRouter: Heterogeneous Model Routing for Cost-Optimal Multi-Step Agentic Workflows</a></td><td>28</td><td>0</td><td>LG</td><td>트레젝토리 단계별로 모델 티어를 라우팅하는 경량 분류기, 비용-품질 트레이드오프 개선을 실증함</td></tr>
<tr><td>634</td><td><a href='https://arxiv.org/abs/2609.23774'>On Probabilistic Inference Through Parametric Tensor Decomposition in Base Tensor Networks</a></td><td>28</td><td>0</td><td>LG</td><td>텐서네트워크 재매개변수화로 추론 가능성을 잠재구조에 의해 통제하는 이론적 프레임워크임</td></tr>
<tr><td>635</td><td><a href='https://arxiv.org/abs/2609.23860'>Pretraining of Medical Visual Encoders Toward Multi-modal Large Language Models</a></td><td>28</td><td>0</td><td>CV</td><td>report generation으로 시각인코더를 사전학습해 LLM 인터페이스 불일치를 줄이는 방법, 교차LLM 전이성을 확인함</td></tr>
<tr><td>636</td><td><a href='https://arxiv.org/abs/2609.24057'>Representation-guided in-context learning for medical image interpretation with multimodal large language models</a></td><td>28</td><td>0</td><td>Multimodal</td><td>정렬된 예시 검색이 무작위보다 훨씬 효과적임을 보인 무학습 의료영상 ICL 프레임워크임</td></tr>
<tr><td>637</td><td><a href='https://arxiv.org/abs/2609.24555'>The Endless Exam: Mathematical Constructions from Today&#x27;s Models toward Superintelligence</a></td><td>28</td><td>0</td><td>AI</td><td>파라미터화된 14개 구성문제로 초지능을 향한 수학적 진전을 연속점수로 측정하는 벤치마크임</td></tr>
<tr><td>638</td><td><a href='https://arxiv.org/abs/2609.24760'>Construting Reverse Thinking: Developing Large Language Models&#x27; Reverse Thingking Ability</a></td><td>28</td><td>0</td><td>NLP</td><td>역방향 추론경로를 학습시켜 수학추론 오류유형을 줄이는 2단계 훈련, 일관된 정확도 개선을 보임</td></tr>
<tr><td>639</td><td><a href='https://arxiv.org/abs/2609.22187'>Correlation-Guided Flow Matching with Annealed Masking for Spatial Transcriptomics Generation</a></td><td>27</td><td>0</td><td>CV</td><td>조직학 이미지에서 공간전사체 예측하는 플로우매칭, gene-gene correlation 모델링이나 로봇과 무관함</td></tr>
<tr><td>640</td><td><a href='https://arxiv.org/abs/2609.22222'>Can Coding Agents Reproduce Official Statistics? Metadata, Retry Budget and the Limits of Execution Feedback in a Controlled Eurostat Benchmark</a></td><td>27</td><td>0</td><td>NLP</td><td>공식 통계 재현을 위한 코딩 에이전트 메타데이터/재시도 예산 실험, 응용 벤치마크 연구임</td></tr>
<tr><td>641</td><td><a href='https://arxiv.org/abs/2609.22252'>CALM: A Calibrated LLM Choice Network Framework for Activity-Based Traveler Simulation</a></td><td>27</td><td>0</td><td>LG</td><td>LLM 기반 통행자 시뮬레이션 프레임워크, 교통수요 모델링 응용 연구임</td></tr>
<tr><td>642</td><td><a href='https://arxiv.org/abs/2609.22471'>Efficient Mixture-of-Experts with Speculative Decoding via Expert Coactivation</a></td><td>27</td><td>0</td><td>NLP</td><td>MoE와 추측 디코딩 결합 시 expert coactivation 라우터 설계, 추론 효율화 연구임</td></tr>
<tr><td>643</td><td><a href='https://arxiv.org/abs/2609.22585'>TWIG: A Time-Causal Wavelet Operator for Autoregressive Forecasting on Irregular Graphs</a></td><td>27</td><td>0</td><td>LG</td><td>불규칙 그래프용 시간인과 웨이블릿 연산자로 자기회귀 예측, 응용 그래프 예측 연구임</td></tr>
<tr><td>644</td><td><a href='https://arxiv.org/abs/2609.22643'>Monotone-Constrained Diffusion Models for Long-Horizon Production Forecasting</a></td><td>27</td><td>0</td><td>LG</td><td>석유가스 생산량 장기예측용 단조성 제약 확산모델, 응용 시계열 연구임</td></tr>
<tr><td>645</td><td><a href='https://arxiv.org/abs/2609.22785'>Robust Market Making with Hawkes Order Flow and Price Impact via Adversarial Reinforcement Learning</a></td><td>27</td><td>0</td><td>RL</td><td>Hawkes order flow 하 마켓메이킹을 위한 adversarial RL, 금융 응용 연구임</td></tr>
<tr><td>646</td><td><a href='https://arxiv.org/abs/2609.22836'>A Hybrid Attention Model Learning Unified Time-aware Patch Representation for Irregular Multivariate Time Series Forecasting</a></td><td>27</td><td>0</td><td>LG</td><td>불규칙 다변량 시계열용 time-aware patch representation 파운데이션 모델임</td></tr>
<tr><td>647</td><td><a href='https://arxiv.org/abs/2609.22862'>CurvFlow-DTA: dual-graph discrete Ricci curvature flow for drug--target affinity prediction</a></td><td>27</td><td>0</td><td>LG</td><td>Ricci curvature flow로 drug-target affinity 예측 개선, 응용 신약 연구임</td></tr>
<tr><td>648</td><td><a href='https://arxiv.org/abs/2609.22932'>Joint Domain-Class Modeling for Federated Learning Under Feature Skew</a></td><td>27</td><td>0</td><td>LG</td><td>feature skew 하 연합학습을 위한 pseudo-domain 분류헤드 확장 기법임</td></tr>
<tr><td>649</td><td><a href='https://arxiv.org/abs/2609.23008'>Interpretable Multi-Hypersphere Deep Anomaly Detection for Open-set Supervised Anomaly Detection</a></td><td>27</td><td>0</td><td>CV</td><td>클래스별 hypersphere로 open-set 이상탐지를 해석 가능하게 만든 방법론임</td></tr>
<tr><td>650</td><td><a href='https://arxiv.org/abs/2609.23073'>MolSC: Leveraging Substituent Contributions to Enhance Fine-grained Molecular Understanding in LLMs</a></td><td>27</td><td>0</td><td>NLP</td><td>치환기 기여도 데이터셋으로 분자 LLM의 fine-grained 이해를 개선한 응용 연구임</td></tr>
<tr><td>651</td><td><a href='https://arxiv.org/abs/2609.23102'>When Does Adversarial Refinement Help? A Negative Result and Open Problem in Adapting R3GAN to Time Series Imputation</a></td><td>27</td><td>0</td><td>LG</td><td>안정화된 R3GAN을 시계열 imputation에 적용했으나 개선 없음을 보인 negative result 논문임</td></tr>
<tr><td>652</td><td><a href='https://arxiv.org/abs/2609.23146'>Ask for Any Appliance: A Prompt-Programmable Foundation Model for Non-Intrusive Load Monitoring</a></td><td>27</td><td>0</td><td>LG</td><td>프롬프트로 임의 가전 전력을 추정하는 파운데이션 모델, NILM 응용 연구임</td></tr>
<tr><td>653</td><td><a href='https://arxiv.org/abs/2609.23185'>Neural Residual Modeling for Scientific Data Compression under Guaranteed Error Bounds</a></td><td>27</td><td>0</td><td>LG</td><td>RVQ 압축 후 U-Net으로 잔차를 보정하는 과학 데이터 손실압축 파이프라인임</td></tr>
<tr><td>654</td><td><a href='https://arxiv.org/abs/2609.23257'>CTRL: Control-Based Time Series Forecasting with LLM-Guided Residual Learning</a></td><td>27</td><td>0</td><td>NLP</td><td>LLM 에이전트가 잔차 보정 신호를 내는 시계열 예측 프레임워크임</td></tr>
<tr><td>655</td><td><a href='https://arxiv.org/abs/2609.23308'>Optimal Multi-way Decision Trees for Stratified Sampling in Online Controlled Experiments</a></td><td>27</td><td>0</td><td>LG</td><td>A/B 테스트 분산감소용 최적 multi-way stratification tree 방법임</td></tr>
<tr><td>656</td><td><a href='https://arxiv.org/abs/2609.23435'>Tool-Augmented On-Policy Distillation for LLM Domain Adaptation in Sequence-Based Omics Tasks</a></td><td>27</td><td>0</td><td>NLP</td><td>multi-omics 서열 예측을 근거기반 reasoning으로 정렬한 tool-augmented distillation 방법임</td></tr>
<tr><td>657</td><td><a href='https://arxiv.org/abs/2609.23659'>ETH-TraceBench: A Large-Scale Event-Stream Benchmark for Ethereum DeFi under Temporal, Protocol, and Contract Shift</a></td><td>27</td><td>0</td><td>LG</td><td>이더리움 DeFi 이벤트스트림 벤치마크, 도메인 시프트 하 shortcut 학습을 드러낸 연구임</td></tr>
<tr><td>658</td><td><a href='https://arxiv.org/abs/2609.23836'>Actionable Insights from Observational Data: The Case of Advanced Classes in K-12 Education</a></td><td>27</td><td>0</td><td>LG</td><td>K-12 심화과정 수강의 인과효과를 관측 데이터로 추정한 교육 응용 연구임</td></tr>
<tr><td>659</td><td><a href='https://arxiv.org/abs/2609.23838'>From Regional to Global: Transfer Learning for Atmospheric Transport Emulators</a></td><td>27</td><td>0</td><td>LG</td><td>지역별 대기수송 에뮬레이터를 지역 간 전이학습으로 확장한 응용 연구임</td></tr>
<tr><td>660</td><td><a href='https://arxiv.org/abs/2609.23906'>Multivariate quantile regression via Kolmogorov-Arnold Networks</a></td><td>27</td><td>0</td><td>LG</td><td>Kolmogorov-Arnold Network 앙상블로 다변량 quantile regression을 수행한 방법임</td></tr>
<tr><td>661</td><td><a href='https://arxiv.org/abs/2609.23999'>Misaligned Clinical Risk Classification and Cost Asymmetry in Open-Weight Large Language Models</a></td><td>27</td><td>0</td><td>NLP</td><td>LLM이 비용 방향은 인코딩하나 실제 결정에는 잘 통합하지 못함을 보인 임상 위험 분석 연구임</td></tr>
<tr><td>662</td><td><a href='https://arxiv.org/abs/2609.24042'>Q-DEQ: Discrete Solving and Quantization for Deep Equilibrium Models in Time Series Forecasting under Edge Deployment Coding Constraints</a></td><td>27</td><td>0</td><td>LG</td><td>deep equilibrium model의 fixed-point 갱신을 QUBO로 이산화해 엣지 배포에 적합하게 만든 방법임</td></tr>
<tr><td>663</td><td><a href='https://arxiv.org/abs/2609.24150'>Acceptance-Aware Draft Model Training for Speculative Decoding</a></td><td>27</td><td>0</td><td>NLP</td><td>acceptance length를 직접 최적화하는 draft model 훈련 손실을 제안한 추측디코딩 연구임</td></tr>
<tr><td>664</td><td><a href='https://arxiv.org/abs/2609.24197'>H-Spec: Parallel Speculative Decoding Without a Drafter-Side KV Cache</a></td><td>27</td><td>0</td><td>NLP</td><td>drafter 측 KV 캐시 없이 target KV를 재사용하는 병렬 추측디코딩 기법임</td></tr>
<tr><td>665</td><td><a href='https://arxiv.org/abs/2609.24249'>Reinforcement Learning Inspired Black-box Adversarial Attacks for Computer Vision</a></td><td>27</td><td>0</td><td>CV</td><td>RL 기반 블랙박스 적대적 공격으로 쿼리 효율을 높인 보안 연구임</td></tr>
<tr><td>666</td><td><a href='https://arxiv.org/abs/2609.24298'>KV-COBRA: KV Cache Compression via Co-Optimized Bit-Rank Allocation</a></td><td>27</td><td>0</td><td>NLP</td><td>attention head별 rank-bitwidth를 공동최적화한 KV 캐시 압축 기법임</td></tr>
<tr><td>667</td><td><a href='https://arxiv.org/abs/2609.24579'>Universal Multi-Modal Traceformer: Integrating Heterogeneous Context for Process Event Prediction</a></td><td>27</td><td>0</td><td>LG</td><td>이벤트 로그의 이종 컨텍스트를 통합해 다음 이벤트를 예측하는 트랜스포머 프레임워크임</td></tr>
<tr><td>668</td><td><a href='https://arxiv.org/abs/2609.24591'>Taking a Second Look: Correcting Sea Ice Forecasts with Sparse Observations</a></td><td>27</td><td>0</td><td>LG</td><td>희소 관측으로 해빙 예측 오차를 상태의존적 전파거리로 보정하는 방법임</td></tr>
<tr><td>669</td><td><a href='https://arxiv.org/abs/2609.22277'>An Affordable AI-Integrated Smart Cane for Multimodal Mobility Assistance of Visually Impaired Users</a></td><td>26</td><td>4</td><td>Embodied AI</td><td>시각장애인용 저가 오프라인 스마트 케인, RGB+ToF 융합과 엣지 추론 배포를 검증한 실제 보조로봇 시스템이나 로봇 팔/이동 제어 연구는 아님</td></tr>
<tr><td>670</td><td><a href='https://arxiv.org/abs/2609.22942'>An Evolutionary Agentic Approach for Open-ended Image Quality Perception</a></td><td>26</td><td>0</td><td>CV</td><td>개방형 이미지 품질 평가를 위한 에이전트 진화 방식 연구로 로봇과 무관함</td></tr>
<tr><td>671</td><td><a href='https://arxiv.org/abs/2609.22251'>Predictors and Orchestrators: Parsimonious Machine Learning within an Agentic AI Harness for Multi-Horizon Karst Aquifer Forecasting</a></td><td>26</td><td>0</td><td>LG</td><td>카르스트 대수층 유출량 예측용 5개 모델 비교+에이전트 오케스트레이션, 응용 수문학 연구임</td></tr>
<tr><td>672</td><td><a href='https://arxiv.org/abs/2609.22441'>Connected Content Retriever: Dense Graph Edge Features Powering Pre-Ranking at LinkedIn</a></td><td>26</td><td>0</td><td>LG</td><td>LinkedIn 피드 프리랭킹용 GPU 기반 그래프 특성 스코어링 시스템, 산업 인프라 논문임</td></tr>
<tr><td>673</td><td><a href='https://arxiv.org/abs/2609.22508'>EmbeddGAN: A Novel GAN Framework Using an Embedding Network and Gini Distance Correlation</a></td><td>26</td><td>0</td><td>CV</td><td>Gini distance correlation 기반 GAN 안정화 기법, 생성모델 학습 안정성 개선 연구임</td></tr>
<tr><td>674</td><td><a href='https://arxiv.org/abs/2609.24444'>WPBench: A Comprehensive Benchmark for Wind Power Forecasting</a></td><td>26</td><td>0</td><td>LG</td><td>풍력발전 예측을 위한 26개 데이터셋·19개 모델 종합 벤치마크임</td></tr>
<tr><td>675</td><td><a href='https://arxiv.org/abs/2609.22805'>To Consolidate or not to Consolidate? Evaluating the Impact of Consolidation in Multi-Reference Training using Peer Reviews</a></td><td>26</td><td>0</td><td>NLP</td><td>다중 참조 통합이 리뷰 생성에 유리함을 실증하고 대규모 데이터셋을 공개함</td></tr>
<tr><td>676</td><td><a href='https://arxiv.org/abs/2609.23178'>Chronologic: Measuring Language Models&#x27; Ability to Represent the Past</a></td><td>26</td><td>0</td><td>NLP</td><td>과거 맥락 재현 능력을 페어와이즈로 측정하는 벤치마크, 생성이 판별보다 어렵다는 관찰을 제공함</td></tr>
<tr><td>677</td><td><a href='https://arxiv.org/abs/2609.23191'>Low resource cross-modal alignment using HGNN to enhance speech representation</a></td><td>26</td><td>0</td><td>NLP</td><td>그래프 신경망으로 저자원 언어 음성-텍스트 정렬, 데이터 효율성을 확인함</td></tr>
<tr><td>678</td><td><a href='https://arxiv.org/abs/2609.23490'>BabelArena: A Large-Scale Multilingual Benchmark for LLM Agents</a></td><td>26</td><td>0</td><td>NLP</td><td>다국어 agent 벤치마크로 저자원 언어에서 도구사용 오류가 두드러짐을 확인함</td></tr>
<tr><td>679</td><td><a href='https://arxiv.org/abs/2609.23880'>Q-TIE: A Lightweight and Generalizable Re-ranking Framework for Temporal Information Retrieval</a></td><td>26</td><td>0</td><td>NLP</td><td>시간 의도를 구간으로 추출해 재랭킹하는 경량 TIR 프레임워크, 일반화력을 개선함</td></tr>
<tr><td>680</td><td><a href='https://arxiv.org/abs/2609.24083'>From Content Generation to Learning Support: Pedagogy-Guided Generative Video Tutors for STEM Learning</a></td><td>26</td><td>0</td><td>Multimodal</td><td>교육학 원칙을 반영한 생성형 STEM 비디오 튜터 파이프라인, 응용 시스템 기여임</td></tr>
<tr><td>681</td><td><a href='https://arxiv.org/abs/2609.24199'>Vimarsha: Faithful ASR Evaluation for Indian Languages with Demographic Diversity, In-the-Wild Audio and Spelling Variations</a></td><td>26</td><td>0</td><td>NLP</td><td>인도 22개 언어 현실적 ASR 벤치마크, 평가 편향 두 종류를 동시에 해결함</td></tr>
<tr><td>682</td><td><a href='https://arxiv.org/abs/2609.24812'>MSI-Bench: Evaluating Multi-Speaker Voice Interaction for Collaborative AI Agents</a></td><td>26</td><td>0</td><td>NLP</td><td>다자간 음성 상호작용 벤치마크, 지각-추론 실패 원인을 분리해 진단함</td></tr>
<tr><td>683</td><td><a href='https://arxiv.org/abs/2609.24932'>Linguistic Features for Interpretable Textual Entailment</a></td><td>26</td><td>0</td><td>NLP</td><td>구조-관계와 분포-정보 특징을 결합한 해석가능 함의인식 모델, 경량 모델로 RoBERTa에 근접함</td></tr>
<tr><td>684</td><td><a href='https://arxiv.org/abs/2609.24965'>Jev for Scientific Decisions: Evaluating Semantic Choices and Their Consequences</a></td><td>26</td><td>0</td><td>NLP</td><td>과학 워크플로의 의미론적 선택지를 타입드 모델로 평가한 소규모 사례연구임</td></tr>
<tr><td>685</td><td><a href='https://arxiv.org/abs/2609.22408'>Social Influence and the Allocation of Scientific Attention in AI Populations</a></td><td>26</td><td>0</td><td>AI</td><td>AI 에이전트 집단에서 사회적 정보가 논문 선택 다양성을 줄임을 실험으로 보인 흥미로운 관찰, 로봇과 무관함</td></tr>
<tr><td>686</td><td><a href='https://arxiv.org/abs/2609.22628'>Text, Pixels, or Both? Evaluating Input Representations for Multimodal Document QA</a></td><td>26</td><td>0</td><td>Multimodal</td><td>문서QA에서 이미지/텍스트 입력 선택이 정확도-지연 트레이드오프를 가짐을 실증, 라우터로 상호보완성을 활용함</td></tr>
<tr><td>687</td><td><a href='https://arxiv.org/abs/2609.22878'>ISA-Bench: A Benchmark for Computational Reasoning Across Instruction Set Architectures</a></td><td>26</td><td>0</td><td>AI</td><td>낯선 명령어집합에서의 코드추론 벤치마크, reasoning-execution gap 분석이 기여임</td></tr>
<tr><td>688</td><td><a href='https://arxiv.org/abs/2609.22939'>Beyond Linear Context: Graph-Guided Evidence Navigation for Long-Novel Reasoning with a Local 9B Language Model</a></td><td>26</td><td>0</td><td>AI</td><td>소형 로컬 모델에 지식그래프를 붙여 장편소설 추론을 돕는 탐색적 연구, 통계적 유의성은 확보하지 못함</td></tr>
<tr><td>689</td><td><a href='https://arxiv.org/abs/2609.23058'>LazyAgent: Demand-Driven Materialization and Physical Optimization of Agentic Programs</a></td><td>26</td><td>0</td><td>AI</td><td>목표기반 지연평가로 불필요한 에이전트 실행을 제거하는 런타임, CPU/컨테이너 시간 절감을 실증함</td></tr>
<tr><td>690</td><td><a href='https://arxiv.org/abs/2609.23074'>Event Signature Transfer: Model-Agnostic Forecast Scenario Construction from Historical Events</a></td><td>26</td><td>0</td><td>AI</td><td>과거 이벤트의 신호를 학습없이 예측 시나리오로 전이하는 연산자, 다양한 예측기에 적용가능한 실용적 기여임</td></tr>
<tr><td>691</td><td><a href='https://arxiv.org/abs/2609.23512'>AgentBetta: Verification-Driven Adaptive Configuration of an AI Nano-Agent through Selective Expansion and Verified Contraction</a></td><td>26</td><td>0</td><td>AI</td><td>검증기반 진단으로 에이전트 설정을 확장/축소하는 나노에이전트 프레임워크, 컨텍스트/도구 노출을 크게 줄이면서 성공률을 유지함</td></tr>
<tr><td>692</td><td><a href='https://arxiv.org/abs/2609.24115'>EDGEGEN: Improving Tool-Calling Agents Beyond Happy Paths with Synthetic Edge Case Generation</a></td><td>26</td><td>0</td><td>AI</td><td>에이전트 명세에서 규칙위반 엣지케이스를 자동생성해 파인튜닝하는 폐루프 시스템, 성능개선이 일관됨</td></tr>
<tr><td>693</td><td><a href='https://arxiv.org/abs/2609.24229'>Recovering Lost Details: Multi-Scale Frequency Compensation for Long-Term Time Series Forecasting</a></td><td>26</td><td>0</td><td>LG</td><td>웨이블릿 기반 다중스케일 혼합으로 장기 시계열 예측의 손실된 디테일을 복원함</td></tr>
<tr><td>694</td><td><a href='https://arxiv.org/abs/2609.24620'>Ascent: An Agentic System over the Model Context Protocol for Real-World Clinical Data Analysis</a></td><td>26</td><td>0</td><td>AI</td><td>MCP 기반 임상데이터 분석 에이전트, 약물역학 오류 회피 벤치마크로 검증된 정확도 개선을 보임</td></tr>
<tr><td>695</td><td><a href='https://arxiv.org/abs/2609.24855'>Extracting Arguments, Not Just Classifying Them: Instruction-Tuned LLMs for Generative Component Detection</a></td><td>26</td><td>0</td><td>NLP</td><td>논증요소 탐지를 생성과제로 재구성한 명령어튜닝 LLM 접근, SOTA를 달성함</td></tr>
<tr><td>696</td><td><a href='https://arxiv.org/abs/2609.24742'>LLM-based Conversational AI Knowledge Assistant for MyBuddy Humanoid Robot</a></td><td>25</td><td>5</td><td>HRI</td><td>MyBuddy 휴머노이드에 LLM 대화·검색 기능을 통합한 시스템 데모 성격의 워크숍 포스터로 새 방법론은 없음</td></tr>
<tr><td>697</td><td><a href='https://arxiv.org/abs/2609.22706'>DOA-SORT: Directional Occlusion-Aware Multi-Object Tracking with Distributional Observations</a></td><td>25</td><td>2</td><td>CV</td><td>방향성 가림을 명시적으로 모델링한 학습 없는 MOT 트래커로 개선폭은 있으나 점진적 엔지니어링에 가까움</td></tr>
<tr><td>698</td><td><a href='https://arxiv.org/abs/2609.24455'>MECAIL: Communication-Aware Incremental Learning for Object Detection with 14.6 KB Spatiotemporal Experts</a></td><td>25</td><td>2</td><td>CV</td><td>엣지 장치용 통신 인지 incremental learning으로 지능형 교통 시스템의 객체 탐지를 적응시키는 효율화 연구임</td></tr>
<tr><td>699</td><td><a href='https://arxiv.org/abs/2609.24619'>Video-based Surgical Skill Assessment Using Dynamics-and-Uncertainty-Aware Tree-based Gaussian Process Classifier</a></td><td>25</td><td>2</td><td>CV</td><td>동역학·불확실성 인지 tree 기반 Gaussian Process로 수술 영상에서 술기를 평가하는 연구로 수술 로봇 평가와 간접적으로 연결됨</td></tr>
<tr><td>700</td><td><a href='https://arxiv.org/abs/2609.22291'>Beyond the Survey: A Systematic Empirical Study of Detection and Association in Visual MOT</a></td><td>25</td><td>1</td><td>CV</td><td>멀티오브젝트 트래킹 detection·association 기여도를 분석한 실험적 서베이라 새 방법론 제시가 약함</td></tr>
<tr><td>701</td><td><a href='https://arxiv.org/abs/2609.22807'>C$^{2}$-INR: Customized Convolutional Implicit Neural Representation</a></td><td>25</td><td>1</td><td>CV</td><td>컨볼루션 기반 implicit neural representation 개선 연구로 일반 표현학습이라 로봇 적용은 간접적임</td></tr>
<tr><td>702</td><td><a href='https://arxiv.org/abs/2609.22834'>SatOV: Restoring Spatial Priors for Training-Free Open-Vocabulary Segmentation in Remote Sensing Imagery</a></td><td>25</td><td>1</td><td>CV</td><td>원격탐사 영상의 학습 없는 open-vocabulary 세그멘테이션 연구로 로봇 응용과는 거리가 있음</td></tr>
<tr><td>703</td><td><a href='https://arxiv.org/abs/2609.23248'>SPACE: Semantic Projection and Alignment of CLIP Embeddings for Domain Adaptation</a></td><td>25</td><td>1</td><td>CV</td><td>CLIP 임베딩의 시맨틱 정렬을 통한 도메인 적응 연구로 일반 CV 문제라 로봇 적용은 간접적임</td></tr>
<tr><td>704</td><td><a href='https://arxiv.org/abs/2609.23380'>LiteTex-GS: Fast and Lightweight Texturing for Gaussian Splatting</a></td><td>25</td><td>1</td><td>3D Vision</td><td>Gaussian Splatting에 텍스처 맵을 가볍게 결합하는 경량화 기법으로 로봇 응용은 다루지 않음</td></tr>
<tr><td>705</td><td><a href='https://arxiv.org/abs/2609.23425'>Semi-automated reconstruction of indoor geometry from 360-degree video for CFD-based airflow analysis in classrooms</a></td><td>25</td><td>1</td><td>3D Vision</td><td>360도 영상으로 실내 CFD 기류 분석용 지오메트리를 반자동 재구성하는 워크플로로 로봇과는 거리가 있음</td></tr>
<tr><td>706</td><td><a href='https://arxiv.org/abs/2609.23561'>Transferring Visual Explanations: How Cross-Architecture Knowledge Distillation Affects Model Interpretability</a></td><td>25</td><td>1</td><td>CV</td><td>지식 증류가 모델 해석가능성에 미치는 영향을 분석한 연구로 자율주행을 언급하나 핵심은 일반 해석가능성 연구임</td></tr>
<tr><td>707</td><td><a href='https://arxiv.org/abs/2609.24226'>SRPR-Net: Semantic and Relational Prompt Refinement for Automated SAM-based Instance Segmentation</a></td><td>25</td><td>1</td><td>CV</td><td>SAM 기반 자동 인스턴스 세그멘테이션을 의미·관계 프롬프트로 개선한 연구로 일반 CV 엔지니어링 기여임</td></tr>
<tr><td>708</td><td><a href='https://arxiv.org/abs/2609.24367'>TReViS: Temporal Repetition Structure Aware Video Synthesis for Self-supervised Repetitive Action Counting</a></td><td>25</td><td>1</td><td>Video</td><td>반복 행동 카운팅을 라벨 없이 학습하기 위한 self-supervised 비디오 합성 프레임워크로 로봇 응용은 없음</td></tr>
<tr><td>709</td><td><a href='https://arxiv.org/abs/2609.24482'>STA-TFM: Spatio-Temporal Aggregation Across Views TransForMer for Pose Estimation</a></td><td>25</td><td>1</td><td>CV</td><td>다시점 트랜스포머로 3D 인간 자세를 추정하는 연구로 모션 캡처에 참고할 여지는 있으나 로봇 적용은 없음</td></tr>
<tr><td>710</td><td><a href='https://arxiv.org/abs/2609.24510'>0.5\%&gt;100\%: Bidirectional Reciprocal Learning for Referring Image Segmentation</a></td><td>25</td><td>1</td><td>Multimodal</td><td>referring image segmentation을 위한 PEFT 양방향 상호학습 기법으로 일반 CV 엔지니어링 기여임</td></tr>
<tr><td>711</td><td><a href='https://arxiv.org/abs/2609.22506'>Rethinking Vision Architectures with Gated Linear Attention and KAN</a></td><td>25</td><td>0</td><td>CV</td><td>Gated Linear Attention과 KAN을 결합한 효율적 비전 백본으로 경량화 중심 기여라 우선 평가 대상 아님</td></tr>
<tr><td>712</td><td><a href='https://arxiv.org/abs/2609.22950'>CLEAR: Complex Learned Explicit Analytical Regularization for Ultra-Accelerated 4D Flow CMR Reconstruction</a></td><td>25</td><td>0</td><td>CV</td><td>초가속 4D flow 심장 MRI 재구성을 위한 학습된 정규화 기법으로 의료 영상 연구라 로봇과 무관함</td></tr>
<tr><td>713</td><td><a href='https://arxiv.org/abs/2609.23169'>UltraTex: Unleashing 2K Multi-View Diffusion for 3D Texturing</a></td><td>25</td><td>0</td><td>CV</td><td>2K 해상도 멀티뷰 디퓨전 기반 3D 애셋 텍스처링 연구로 그래픽스 응용이라 로봇과 무관함</td></tr>
<tr><td>714</td><td><a href='https://arxiv.org/abs/2609.23442'>PhysReflect: Geometry and Perception Guided Diffusion for Physically-Plausible Mirror Reflections</a></td><td>25</td><td>0</td><td>CV</td><td>거울 반사의 물리적 타당성을 개선한 diffusion 생성 연구로 로봇과 무관함</td></tr>
<tr><td>715</td><td><a href='https://arxiv.org/abs/2609.23600'>PETR: Prompt Ensembling with Training-free Routing for Vision-Language Models</a></td><td>25</td><td>0</td><td>Multimodal</td><td>학습 없는 라우팅으로 두 프롬프트를 결합해 VLM의 seen·unseen 일반화를 동시에 잡는 방법으로 로봇 적용은 없음</td></tr>
<tr><td>716</td><td><a href='https://arxiv.org/abs/2609.24691'>What Makes a Good Medical Image Tokenizer? Rethinking Reconstruction and Generation in Medical Image Tokenization</a></td><td>25</td><td>0</td><td>CV</td><td>의료 영상용 tokenizer 설계를 재검토한 연구로 로봇과 무관함</td></tr>
<tr><td>717</td><td><a href='https://arxiv.org/abs/2609.24788'>Streaming Video Editing with Easy Adaptation</a></td><td>25</td><td>0</td><td>Video</td><td>사전학습된 양방향 video diffusion을 자기회귀적 스트리밍 편집으로 적응시키는 연구로 로봇과 무관함</td></tr>
<tr><td>718</td><td><a href='https://arxiv.org/abs/2609.22146'>GRRR: The Geometry of Reshaping, Rotation, and Routing in Decoder LLM post-training</a></td><td>25</td><td>0</td><td>LG</td><td>LLM post-training이 가중치를 SVD 프레임에서 어떻게 바꾸는지 분석한 연구로 로봇과 무관함</td></tr>
<tr><td>719</td><td><a href='https://arxiv.org/abs/2609.22170'>Multiple latent orderings better predict language model preferences</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM 선호의 비이행성을 여러 잠재 순서의 혼합으로 설명한 연구로 로봇과 무관함</td></tr>
<tr><td>720</td><td><a href='https://arxiv.org/abs/2609.22977'>Beyond Similarity: Coverage-Aware Prompt Selection for Time Series Forecasting with LLMs</a></td><td>25</td><td>0</td><td>LG</td><td>시계열 예측용 LLM 프롬프트 선택에 coverage 정규화를 추가한 방법임</td></tr>
<tr><td>721</td><td><a href='https://arxiv.org/abs/2609.23320'>CSC: Calibrated Simplicity for Conflict-Aware Social Bot Detection in the LLM Era</a></td><td>25</td><td>0</td><td>LG</td><td>LLM 시대 소셜봇 탐지를 위한 calibrated fusion 프레임워크임</td></tr>
<tr><td>722</td><td><a href='https://arxiv.org/abs/2609.23883'>Collaborative Streaming Anomaly Detection with Interactive Explanations and Ensemble Consensus</a></td><td>25</td><td>0</td><td>LG</td><td>산업 스트리밍 이상탐지에 분석가 개입을 결합한 협업 시스템 논문임</td></tr>
<tr><td>723</td><td><a href='https://arxiv.org/abs/2609.24382'>Credit Access is Associated with Improved Food Security in the Horn of Africa</a></td><td>25</td><td>0</td><td>LG</td><td>신용접근성과 식량안보의 인과관계를 관측 ML로 추정한 응용 연구임</td></tr>
<tr><td>724</td><td><a href='https://arxiv.org/abs/2609.24609'>GraphToolbox: A Configurable Python Framework for Graph Neural Network Forecasting</a></td><td>25</td><td>0</td><td>LG</td><td>GNN 기반 전력수요 예측 실험을 통합하는 설정 기반 파이썬 프레임워크 도구 논문임</td></tr>
<tr><td>725</td><td><a href='https://arxiv.org/abs/2609.24718'>A Federated Artificial Intelligence Framework for Optimizing Pancreatic Cancer Treatment - Strategy Update</a></td><td>25</td><td>0</td><td>LG</td><td>췌장암 치료 최적화를 위한 연합학습 파이프라인 구축 경험 보고서임</td></tr>
<tr><td>726</td><td><a href='https://arxiv.org/abs/2609.22099'>A framework for recipe data structure with applications for culinary and nutritional insights</a></td><td>25</td><td>0</td><td>NLP/Data</td><td>레시피를 재료-영양-지역 정보로 구조화한 데이터셋 논문으로 로보틱스와 무관한 CS 응용 데이터 기여임</td></tr>
<tr><td>727</td><td><a href='https://arxiv.org/abs/2609.22110'>Evaluating Fine-Tuned and Base Language Models in Maternal and Vaccination Healthcare for African Settings</a></td><td>25</td><td>0</td><td>NLP/Healthcare</td><td>나이지리아 모성건강·백신 챗봇의 도메인 파인튜닝 효과를 임상의 평가로 비교한 응용 연구로 로보틱스와 무관함</td></tr>
<tr><td>728</td><td><a href='https://arxiv.org/abs/2609.22204'>Evaluating Personal Information Output from Conversational Interactions in Generative AI Systems</a></td><td>25</td><td>0</td><td>NLP/Privacy</td><td>생성형 AI가 대화에서 개인정보를 어디까지 출력하는지 소규모 참가자로 조사한 탐색적 파일럿 연구로 로보틱스와 무관함</td></tr>
<tr><td>729</td><td><a href='https://arxiv.org/abs/2609.22239'>Knowledge Graph-Augmented Ambient AI for Clinical Note Generation</a></td><td>25</td><td>0</td><td>NLP</td><td>KG 기반으로 clinical note 누락 정보 보완하는 응용 시스템, novelty 제한적임</td></tr>
<tr><td>730</td><td><a href='https://arxiv.org/abs/2609.22248'>Checkpoints Are Not Enough: Trust Calibration in CoSLR, a Human-AI System for Systematic Literature Reviews</a></td><td>25</td><td>0</td><td>NLP</td><td>문헌리뷰 Human-AI 협업 시스템의 신뢰 보정 문제를 설문으로 검증, 시스템 기여보다 HCI 관찰 중심임</td></tr>
<tr><td>731</td><td><a href='https://arxiv.org/abs/2609.22256'>DIPLOMAT: Dialogue-Span-Aware Direct Preference Optimization for Polite Persuasive Workplace Negotiation Dialogues</a></td><td>25</td><td>0</td><td>NLP</td><td>직장 협상 대화 생성에 DPO 변형 적용한 응용 연구, formulation 자체는 기존 프레임 답습함</td></tr>
<tr><td>732</td><td><a href='https://arxiv.org/abs/2609.22494'>CultureMINE: Datasets and Methods for Improving the Cultural Capabilities of NLP Systems</a></td><td>25</td><td>0</td><td>NLP</td><td>문화 NLP 375편 메타분석 서베이, 트렌드 정리 위주라 방법론적 기여 낮음</td></tr>
<tr><td>733</td><td><a href='https://arxiv.org/abs/2609.22205'>Prediction of Nonlinear Oscillations in a Jumping Quarter-Car Model Using Reservoir Computing</a></td><td>24</td><td>2</td><td>LG</td><td>차량 서스펜션 바운싱 동역학 예측용 reservoir computing, 로봇 제어보다 순수 비선형 동역학 연구에 가까움</td></tr>
<tr><td>734</td><td><a href='https://arxiv.org/abs/2609.22184'>DPTM-DT: Dual-Pretrained Transformer Multitask Representation Learning for Drug-Target Prediction</a></td><td>24</td><td>0</td><td>LG</td><td>약물-타겟 예측 멀티태스크 트랜스포머, 응용 도메인 벤치마크 개선 수준임</td></tr>
<tr><td>735</td><td><a href='https://arxiv.org/abs/2609.22238'>Task-Aware Hybrid QUBO Optimization for Structured Neural Network Pruning</a></td><td>24</td><td>0</td><td>CV</td><td>구조적 프루닝을 QUBO로 정식화한 압축 기법, 경량화 중심이라 우선순위 낮음</td></tr>
<tr><td>736</td><td><a href='https://arxiv.org/abs/2609.23084'>AirGC-CD: Gaussian-Circulant Precoding for Exactly Debiasable PAPR Reduction in Over-the-Air Federated Learning</a></td><td>24</td><td>0</td><td>LG</td><td>over-the-air 연합학습의 PAPR 감소를 위한 Gaussian-circulant precoding 기법임</td></tr>
<tr><td>737</td><td><a href='https://arxiv.org/abs/2609.23521'>Feature Suppression and Differential Privacy for Residential Traffic Classification: A Two-Home Federated Study</a></td><td>24</td><td>0</td><td>LG</td><td>가정용 트래픽 분류에서 feature suppression과 DP-SGD의 형평성 trade-off를 비교한 연구임</td></tr>
<tr><td>738</td><td><a href='https://arxiv.org/abs/2609.24586'>Overlay\_dx - Automating forecasting evaluation</a></td><td>24</td><td>0</td><td>LG</td><td>시계열 예측 성능을 신뢰구간 내 비율로 시각화하는 평가지표 제안임</td></tr>
<tr><td>739</td><td><a href='https://arxiv.org/abs/2609.22261'>Used, Mentioned, or Condemned? A Controlled Contrast-Set Diagnostic for the Use-Mention Distinction in Code-Mixed Hinglish Misogyny Detection</a></td><td>24</td><td>0</td><td>NLP</td><td>use-mention 구분 진단용 contrast-set 벤치마크 제작, 평가 아티팩트 분석이 주된 기여임</td></tr>
<tr><td>740</td><td><a href='https://arxiv.org/abs/2609.22767'>Beyond Final-Token Classification: Heterogeneous Readouts for Evidence-Grounded Suicide Risk Detection</a></td><td>24</td><td>0</td><td>NLP</td><td>답 토큰 경계와 의미 표현을 분리하는 readout 기법, 대회 특화 엔지니어링임</td></tr>
<tr><td>741</td><td><a href='https://arxiv.org/abs/2609.22793'>Diagnose, Then Repair: A Two-Stage MQM-Guided Post-Editing Framework for Domain-Specific Machine Translation</a></td><td>24</td><td>0</td><td>NLP</td><td>진단-수정을 분리한 2단계 MT 후편집 프레임워크, 산업 적용성은 있으나 방법론적 새로움 제한적임</td></tr>
<tr><td>742</td><td><a href='https://arxiv.org/abs/2609.22971'>Automatic multimodal UX improvement recommendations from LLM agent user simulations</a></td><td>24</td><td>0</td><td>Multimodal</td><td>멀티모달 사용자 시뮬레이션으로 UX 개선안을 생성하는 산업 응용 사례연구임</td></tr>
<tr><td>743</td><td><a href='https://arxiv.org/abs/2609.23056'>Bridging Static and Agentic RAG for Taiwanese Historical Question Answering</a></td><td>24</td><td>0</td><td>NLP</td><td>대만 역사 QA에서 두 RAG 방식의 상호보완성을 오라클/셀렉터로 분석, 도메인이 국한됨</td></tr>
<tr><td>744</td><td><a href='https://arxiv.org/abs/2609.23231'>ChemCLIR-Bench: Benchmarking Cross-Lingual Information Retrieval in Multilingual Chemical Patents</a></td><td>24</td><td>0</td><td>NLP</td><td>화학 특허 교차언어 검색 벤치마크, 모노-교차 성능 격차 정량화가 기여임</td></tr>
<tr><td>745</td><td><a href='https://arxiv.org/abs/2609.23267'>Knowing When to Trust Images: Reliability-Aware Multi-modal Entity Alignment</a></td><td>24</td><td>0</td><td>Multimodal</td><td>신뢰도 기반 시각 표현으로 멀티모달 엔티티 정렬을 개선, 방법론적 기여는 점진적임</td></tr>
<tr><td>746</td><td><a href='https://arxiv.org/abs/2609.23463'>Perplexity Predicts Protection: Choosing Pretrained Backbones for Worst-Client Fairness in Federated Parameter-Efficient Fine-Tuning</a></td><td>24</td><td>0</td><td>NLP</td><td>perplexity로 최약체 클라이언트 보호 백본을 사전 선택 가능함을 실증, 연합학습 실무 지침을 제공함</td></tr>
<tr><td>747</td><td><a href='https://arxiv.org/abs/2609.23703'>Financial Language Models as Applied Artificial Intelligence Systems for News-Based Trading under Market Frictions</a></td><td>24</td><td>0</td><td>NLP</td><td>뉴스 기반 트레이딩에 시장 마찰을 반영한 평가 프레임워크, 엔지니어링 통합이 주 기여임</td></tr>
<tr><td>748</td><td><a href='https://arxiv.org/abs/2609.23955'>Some Dialects Are More Equal Than Others: Non-Prestigious Arabic Dialectal Bias in LLMs</a></td><td>24</td><td>0</td><td>NLP</td><td>비주류 이집트 방언에 대한 LLM 편향을 통사 평가와 다운스트림 성능으로 확인함</td></tr>
<tr><td>749</td><td><a href='https://arxiv.org/abs/2609.23966'>From Tables to Quantified Statements: Evaluating LLM Inference Generation through Executable Verification</a></td><td>24</td><td>0</td><td>NLP</td><td>표에서 정량화 진술 생성을 실행가능 검증기로 평가하는 태스크를 제안함</td></tr>
<tr><td>750</td><td><a href='https://arxiv.org/abs/2609.24028'>When Evidence Conflicts: Reliability-aware Meta-review Generation</a></td><td>24</td><td>0</td><td>NLP</td><td>리뷰어 신뢰도를 반영해 메타리뷰를 생성, 충돌 인식을 개선함</td></tr>
<tr><td>751</td><td><a href='https://arxiv.org/abs/2609.24264'>Canonical Procedural Actions: An Auditable Annotation Protocol for Tool-Use Agent Traces</a></td><td>24</td><td>0</td><td>NLP</td><td>도구사용 에이전트 궤적의 절차단위 주석 프로토콜, 재현성 측정 위주임</td></tr>
<tr><td>752</td><td><a href='https://arxiv.org/abs/2609.24357'>Mitigating Entity Type Confusion in Cross-Domain NER via Multidimensional Quantification and Reasoning Enhancement</a></td><td>24</td><td>0</td><td>NLP</td><td>소스-타깃 계층/의미유사도로 엔티티 혼동을 정량화하고 이를 완화하는 추론체인을 제안함</td></tr>
<tr><td>753</td><td><a href='https://arxiv.org/abs/2609.24538'>QLoRA Fine-Tuning of Ministral LLM for Sequence-to-Function Protein Annotation</a></td><td>24</td><td>0</td><td>NLP</td><td>단백질 기능주석을 생성과제로 재구성, LLM-judge 평가 기반 응용 연구임</td></tr>
<tr><td>754</td><td><a href='https://arxiv.org/abs/2609.24903'>ToneCL: Contrastive Learning for Few-Shot Syllable-Level Tone Classification</a></td><td>24</td><td>0</td><td>NLP</td><td>대조학습 기반 소수샷 음절 성조 분류, 저자원 언어 전이 실험을 포함함</td></tr>
<tr><td>755</td><td><a href='https://arxiv.org/abs/2609.24983'>onPanda: Efficient Annotation of On-Policy Alignment Data for LLMs and Agents via Token-Level Correction</a></td><td>24</td><td>0</td><td>NLP</td><td>토큰 단위 교정으로 온폴리시 정렬 데이터를 효율적으로 주석하는 도구, 주석시간을 대폭 절감함</td></tr>
<tr><td>756</td><td><a href='https://arxiv.org/abs/2609.22599'>MAWILE: Multi-Axis Workbench for Inspecting LLM Evaluators</a></td><td>24</td><td>0</td><td>AI</td><td>LLM 판정자 프롬프트/루브릭 민감도를 감사하는 개발자용 워크벤치, 툴 기여임</td></tr>
<tr><td>757</td><td><a href='https://arxiv.org/abs/2609.22694'>Toward Auditable and Calibrated AI for Dementia-Related Crash Severity Prediction: A Selective Deferral Framework to Support Human Review</a></td><td>24</td><td>0</td><td>AI</td><td>치매 관련 사고심각도 예측에 선택적 위임을 결합한 감사가능 프레임워크, 응용 안전연구임</td></tr>
<tr><td>758</td><td><a href='https://arxiv.org/abs/2609.23142'>CraftBench-UE: Deterministic Evaluation for Coding Agents in Unreal Engine</a></td><td>24</td><td>0</td><td>AI</td><td>언리얼엔진 코딩에이전트를 결정론적으로 평가하는 벤치마크, C++/블루프린트 격차를 확인함</td></tr>
<tr><td>759</td><td><a href='https://arxiv.org/abs/2609.23363'>TicTacBench: Benchmarking Timing Closure Capabilities of Coding Agents</a></td><td>24</td><td>0</td><td>AI</td><td>RTL 타이밍 클로저 능력을 평가하는 코딩에이전트 벤치마크, 하드웨어 설계 도메인 특화임</td></tr>
<tr><td>760</td><td><a href='https://arxiv.org/abs/2609.23735'>ScholarStack: Layered Research Asset Orchestration and Cross-Task Reuse for Scientific Agents</a></td><td>24</td><td>0</td><td>AI</td><td>문헌자산을 계층화해 재사용하는 과학 에이전트 인프라, 크로스페이퍼 태스크에서 품질/비용을 개선함</td></tr>
<tr><td>761</td><td><a href='https://arxiv.org/abs/2609.24002'>FinInteract: Benchmarking Clarification and Intent Integration in Ambiguous Financial Question Answering</a></td><td>24</td><td>0</td><td>AI</td><td>모호한 재무질문에서 명확화 여부를 측정하는 벤치마크임</td></tr>
<tr><td>762</td><td><a href='https://arxiv.org/abs/2609.24090'>Incremental Consistency Execution for Autonomous Intelligent Systems</a></td><td>24</td><td>0</td><td>AI</td><td>필드단위 의존성 마스크로 자율시스템의 재실행 비용을 줄이는 시스템 기법임</td></tr>
<tr><td>763</td><td><a href='https://arxiv.org/abs/2609.24453'>Predicting Postprandial Glycemic Response from Meal Images, Clinical Variables, and Gut Microbiome Information</a></td><td>24</td><td>0</td><td>Multimodal</td><td>식사이미지·임상변수·장내미생물을 결합한 혈당반응 예측, 응용 멀티모달 연구임</td></tr>
<tr><td>764</td><td><a href='https://arxiv.org/abs/2609.22360'>Contrastive Siamese Representation Learning for Predictive Maintenance of Electrical Submersible Pumps</a></td><td>23</td><td>0</td><td>LG</td><td>전기잠수펌프 결함 진단용 Siamese contrastive+KNN, 예지보전 응용 연구임</td></tr>
<tr><td>765</td><td><a href='https://arxiv.org/abs/2609.24386'>Machine Learning-Based Prediction of Childhood Stunting in Bangladesh: Fairness and Temporal Robustness Assessment</a></td><td>23</td><td>0</td><td>LG</td><td>방글라데시 아동 발육부진 예측의 공정성·시간적 강건성을 평가한 공중보건 연구임</td></tr>
<tr><td>766</td><td><a href='https://arxiv.org/abs/2609.23061'>HDMamba-YOLO: Efficient State-Space Perception and Local Spatial Reconstruction for UAV Small Object</a></td><td>22</td><td>2</td><td>CV</td><td>UAV 소형 객체 탐지용 state-space 아키텍처로 효율성 중심 엔지니어링 기여임</td></tr>
<tr><td>767</td><td><a href='https://arxiv.org/abs/2609.22677'>SHAFT: A Slack-Compensating, Helical-Buckling-Attenuating Flexible-Shaft Transmission for Lightweight Multi-DoF Manipulation</a></td><td>22</td><td>2</td><td>Hardware/Mechanism</td><td>유연축 전달의 슬랙-버클링 문제를 텐셔너로 보완한 기구설계 논문으로 학습이나 새 formulation은 없음</td></tr>
<tr><td>768</td><td><a href='https://arxiv.org/abs/2609.23619'>Compact Low-Cost Hyperspectral Imaging via Angular-to-Spectral Diversity Conversion</a></td><td>22</td><td>1</td><td>CV</td><td>각도-분광 변환 기반 소형 저비용 하이퍼스펙트럼 이미징 하드웨어 연구로 로봇 센서로 쓰일 여지는 있으나 논문 자체는 응용을 다루지 않음</td></tr>
<tr><td>769</td><td><a href='https://arxiv.org/abs/2609.23817'>VISTA: Video-Injected Stylized Text-to-Animation</a></td><td>22</td><td>1</td><td>CV</td><td>텍스트와 참조 비디오 스타일을 결합해 3D 인간 모션을 생성하는 애니메이션 연구로 로봇과는 거리가 있음</td></tr>
<tr><td>770</td><td><a href='https://arxiv.org/abs/2609.24872'>DTKDP: A Dual Teacher Knowledge Distillation and Pruning Framework for Lightweight Oriented SAR Ship Detection</a></td><td>22</td><td>1</td><td>CV</td><td>SAR 선박 탐지용 경량화 dual-teacher distillation·pruning 프레임워크로 효율화 엔지니어링 기여임</td></tr>
<tr><td>771</td><td><a href='https://arxiv.org/abs/2609.22282'>Brain-to-Image Generation: Reconstructing Visual Stimuli from EEG using Generative Adversarial Networks</a></td><td>22</td><td>0</td><td>CV</td><td>EEG 기반 시각 자극 복원 재현 베이스라인 연구라 새로움이 제한적이고 로봇과 무관함</td></tr>
<tr><td>772</td><td><a href='https://arxiv.org/abs/2609.22302'>Authority-Preserving Evaluation of Medical Vision-Language Assistants</a></td><td>22</td><td>0</td><td>Multimodal</td><td>의료 VLM 평가 프레임워크로 임상 워크플로 중심이라 로봇과 무관함</td></tr>
<tr><td>773</td><td><a href='https://arxiv.org/abs/2609.22323'>ALPINE: Adaptive Localization for Parameter- and Sample-Efficient Few-Shot Learning</a></td><td>22</td><td>0</td><td>CV</td><td>파라미터·샘플 효율적인 few-shot 분류 아키텍처로 경량화 중심이라 로봇 문제로 연결되지 않음</td></tr>
<tr><td>774</td><td><a href='https://arxiv.org/abs/2609.22789'>PixelART: Image-to-Layer Decomposition without Latents or Text-to-Image Pretraining</a></td><td>22</td><td>0</td><td>CV</td><td>이미지를 편집 가능한 RGBA 레이어로 분해하는 생성 모델로 디자인 도구 연구이며 로봇과 무관함</td></tr>
<tr><td>775</td><td><a href='https://arxiv.org/abs/2609.23427'>RSPDBench: Benchmarking Vision Foundation Models on Earth Observation Tasks Under Physically Grounded Remote-Sensing Product Degradations</a></td><td>22</td><td>0</td><td>CV</td><td>원격탐사 제품 결함에 대한 vision foundation model 강건성 벤치마크로 로봇과 무관함</td></tr>
<tr><td>776</td><td><a href='https://arxiv.org/abs/2609.23715'>Layer-Aware Position Embeddings for Visual Token Pruning in Multimodal Large Language Models</a></td><td>22</td><td>0</td><td>Multimodal</td><td>MLLM 시각 토큰 pruning 시 위치 임베딩을 층별로 재설계한 효율화 연구로 로봇과 무관함</td></tr>
<tr><td>777</td><td><a href='https://arxiv.org/abs/2609.23815'>Confidence-Aware Teacher-Student Distillation for 3D Medical Segmentation</a></td><td>22</td><td>0</td><td>CV</td><td>극단적으로 희소한 주석으로 3D 의료 영상을 분할하는 teacher-student distillation 연구로 로봇과 무관함</td></tr>
<tr><td>778</td><td><a href='https://arxiv.org/abs/2609.24158'>Relightable 3D Avatar Reconstruction with Semantic-Adaptive Motion-Illumination Responses</a></td><td>22</td><td>0</td><td>CV</td><td>얼굴 부위별 모션·조명 반응을 분리한 relightable 3D 아바타 재구성 연구로 그래픽스 응용이며 로봇과 무관함</td></tr>
<tr><td>779</td><td><a href='https://arxiv.org/abs/2609.24359'>Dissecting Agentic Forensics: The Role of Triage, Prompting, and Evidence Arbitration in Open-World Fake Image Detection</a></td><td>22</td><td>0</td><td>CV</td><td>에이전트 기반 이미지 포렌식에서 triage·프롬프팅·증거 조정의 역할을 분석한 연구로 로봇과 무관함</td></tr>
<tr><td>780</td><td><a href='https://arxiv.org/abs/2609.24485'>VPRune: Efficient Training-free Pre-LLM Visual Token Pruning</a></td><td>22</td><td>0</td><td>Multimodal</td><td>LVLM 추론 비용을 줄이는 학습 없는 pre-LLM 시각 토큰 프루닝 기법으로 효율화 중심임</td></tr>
<tr><td>781</td><td><a href='https://arxiv.org/abs/2609.24539'>Incentive Noise and Structural Prior Infusion for Multi-modal Object Re-Identification</a></td><td>22</td><td>0</td><td>CV</td><td>텍스트 설명의 노이즈를 고려한 멀티모달 객체 재식별 연구로 로봇과 무관함</td></tr>
<tr><td>782</td><td><a href='https://arxiv.org/abs/2609.24595'>Applications of Neural Cellular Automata: State of the Art, Challenges and Opportunities</a></td><td>22</td><td>0</td><td>LG</td><td>Neural Cellular Automata의 응용과 과제를 정리한 서베이로 로봇 응용을 다루지 않음</td></tr>
<tr><td>783</td><td><a href='https://arxiv.org/abs/2609.24768'>PrismGPT: Proxy-Guided Learning for Region-Aware Photo Editing with Self-Synthesized Reasoning</a></td><td>22</td><td>0</td><td>Multimodal</td><td>영역 인지 사진 보정을 위한 VLM 기반 편집 계획 생성 연구로 로봇과 무관함</td></tr>
<tr><td>784</td><td><a href='https://arxiv.org/abs/2609.24879'>Generating Chest X-Ray Counterfactuals by Specialising Foundation Image Models</a></td><td>22</td><td>0</td><td>CV</td><td>흉부 X-ray의 counterfactual 이미지를 foundation model 특화로 생성하는 연구로 counterfactual 개념은 쓰이나 의료 도메인이라 로봇과 무관함</td></tr>
<tr><td>785</td><td><a href='https://arxiv.org/abs/2609.22177'>OpenBlock: Constructive and Verified Content Generation for Adaptive Tile-Matching Games</a></td><td>22</td><td>0</td><td>LG</td><td>타일매칭 게임 콘텐츠 생성 플랫폼 논문임, robotics·embodied AI와 무관함</td></tr>
<tr><td>786</td><td><a href='https://arxiv.org/abs/2609.22096'>AI-inferred expressed well-being and collective-action discourse in climate-change campaigns on X</a></td><td>22</td><td>0</td><td>NLP/Social Science</td><td>기후 캠페인 트윗의 행복-행동 언어 괴리를 분석한 사회과학 텍스트 연구로 로보틱스 관련성이 없음</td></tr>
<tr><td>787</td><td><a href='https://arxiv.org/abs/2609.22124'>Balancing Reasoning and Hardware Constraints in RAG Pipelines for Ukrainian Multi-Domain Document Understanding</a></td><td>22</td><td>0</td><td>NLP/RAG</td><td>제한된 시간 예산 내 우크라이나어 문서 RAG 파이프라인을 구축한 대회 시스템 리포트로 새로운 방법론은 없음</td></tr>
<tr><td>788</td><td><a href='https://arxiv.org/abs/2609.22241'>H2LooP Telecom Model v1: From Telecom Comprehension to Autonomous Issue and PR Resolution</a></td><td>22</td><td>0</td><td>NLP</td><td>통신 도메인 특화 LLM 파인튜닝, 도메인 적응 벤치마크 개선 위주로 formulation 신규성 낮음</td></tr>
<tr><td>789</td><td><a href='https://arxiv.org/abs/2609.22463'>Toward Personalized Sleep Guidance from Wearable Data Using Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>웨어러블 데이터 기반 수면 가이던스 생성 파이프라인, 도메인 응용 위주로 novelty 낮음</td></tr>
<tr><td>790</td><td><a href='https://arxiv.org/abs/2609.22705'>Analyzing Public Discourse on Urbanism: Topic Clustering, Sentiment Analysis and Retrieval-Augmented Generation using YouTube Comments</a></td><td>22</td><td>0</td><td>NLP</td><td>유튜브 댓글로 도시 담론을 분석하는 파이프라인, NLP 컴포넌트의 실패 양상 측정이 주 기여임</td></tr>
<tr><td>791</td><td><a href='https://arxiv.org/abs/2609.23194'>Enhancing speech representation learning with cross-modal knowledge transfer with HGNN under low resource settings: the case study of Yemba</a></td><td>22</td><td>0</td><td>NLP</td><td>위 논문과 유사한 방법을 Yemba어에 재적용한 확장판 성격의 연구임</td></tr>
<tr><td>792</td><td><a href='https://arxiv.org/abs/2609.23582'>ARID: A Deployable Edge AI System for Structured Information Extraction from Industrial Maintenance Work Orders</a></td><td>22</td><td>0</td><td>NLP</td><td>8GB 엣지 기기에서 작업지시서를 구조화 추출하는 배포형 시스템, 실전 배포 검증은 있으나 로봇과 무관함</td></tr>
<tr><td>793</td><td><a href='https://arxiv.org/abs/2609.23726'>GRACE: Grounded Adversarial Reasoning over Canadian Law</a></td><td>22</td><td>0</td><td>NLP</td><td>캐나다 법률 적대적 추론 데이터셋과 경량 모델, 도메인 특화 자원 논문임</td></tr>
<tr><td>794</td><td><a href='https://arxiv.org/abs/2609.23825'>Federated Multilingual Speech-LLMs: Architecture and Aggregation Strategy Benchmarking</a></td><td>22</td><td>0</td><td>NLP</td><td>FL 구성 요소별 학습률 튜닝이 중요함을 보인 벤치마크 연구임</td></tr>
<tr><td>795</td><td><a href='https://arxiv.org/abs/2609.23853'>From UNDRR Reports to Event Records: Schema-Constrained LLM Extraction of Georeferenced Disasters</a></td><td>22</td><td>0</td><td>NLP</td><td>재난 보고서에서 지리참조 이벤트 레코드를 추출하는 스키마 제약 파이프라인, 응용 시스템임</td></tr>
<tr><td>796</td><td><a href='https://arxiv.org/abs/2609.24177'>Efficient LLM Distillation for Bangladesh Legal Context: A Smartphone-Compatible Retrieval-Augmented Generation Model</a></td><td>22</td><td>0</td><td>NLP</td><td>스마트폰 구동형 법률 RAG 증류, 실전 배포 중심 응용임</td></tr>
<tr><td>797</td><td><a href='https://arxiv.org/abs/2609.24219'>From Articles to Publishers: Aggregating Language Model Predictions for News Source Reliability Inference</a></td><td>22</td><td>0</td><td>NLP</td><td>기사 단위 예측을 출판사 단위로 집계하는 프레임워크, 정치성향별 오분류 패턴을 분석함</td></tr>
<tr><td>798</td><td><a href='https://arxiv.org/abs/2609.24372'>URA-NER: A Unified Retrieval-Augmented Framework with Retrieval Alignment and Uncertainty Reduction for Low-Resource NER</a></td><td>22</td><td>0</td><td>NLP</td><td>검색 정합과 불확실성 감소를 결합한 저자원 NER 프레임워크, 소형 LLM에서 이득이 큼</td></tr>
<tr><td>799</td><td><a href='https://arxiv.org/abs/2609.24516'>LLJ Cards: Best practices for the Use of LLMs as Judges</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM 판정자 평가 모범사례를 정리한 가이드라인 프레임워크, 실증 기여 없음</td></tr>
<tr><td>800</td><td><a href='https://arxiv.org/abs/2609.24650'>Assessing Readability with LLMs: The Role of Reasoning and Few-Shot Prompting</a></td><td>22</td><td>0</td><td>NLP</td><td>CoT와 few-shot이 가독성 평가를 개선함을 다국어로 검증한 벤치마크 연구임</td></tr>
<tr><td>801</td><td><a href='https://arxiv.org/abs/2609.22475'>Goal-driven Variant Categorization</a></td><td>22</td><td>0</td><td>AI</td><td>프로세스 변형을 목표모델 기준으로 LLM이 분류하게 하는 방법, 적용사례 중심임</td></tr>
<tr><td>802</td><td><a href='https://arxiv.org/abs/2609.22529'>IntLawNER: A Named Entity Recognition Dataset and Benchmark in International Law</a></td><td>22</td><td>0</td><td>NLP</td><td>국제법 NER 데이터셋과 벤치마크, 실버-골드 불일치 분석이 흥미로운 발견임</td></tr>
<tr><td>803</td><td><a href='https://arxiv.org/abs/2609.22537'>EvidenT: Building Trustworthy Enterprise Assistants through Evidence Groundedness and Traceability</a></td><td>22</td><td>0</td><td>AI</td><td>기업용 RAG의 인용 드리프트를 제거하는 경량 검증 파이프라인, 재학습 없이 적용 가능한 실무 기여임</td></tr>
<tr><td>804</td><td><a href='https://arxiv.org/abs/2609.22696'>Building Trustworthy Mental Health Benchmarks on Bluesky: A Validation-Aware Weak-Supervision Framework</a></td><td>22</td><td>0</td><td>AI</td><td>탈중앙 SNS에서 약지도 정신건강 벤치마크를 구축, 라벨 오류양상을 분석함</td></tr>
<tr><td>805</td><td><a href='https://arxiv.org/abs/2609.22959'>R-GEAN: Regimen-Guided Edit Action Network for Within-Admission Medication Change Prediction</a></td><td>22</td><td>0</td><td>AI</td><td>입원 중 약물변경을 예측하는 비대칭 후보스코어링 네트워크, 리키지 통제 벤치마크 제안이 기여임</td></tr>
<tr><td>806</td><td><a href='https://arxiv.org/abs/2609.23043'>Enforcing Narrative Reliability and Epistemic Pacing in LLM-Driven Detective Games via Structured Knowledge Trees</a></td><td>22</td><td>0</td><td>NLP</td><td>지식트리로 정보공개 순서를 강제하는 탐정게임 대화시스템, 환각 감소 효과는 확인되나 로봇과 무관함</td></tr>
<tr><td>807</td><td><a href='https://arxiv.org/abs/2609.23130'>From Inference Engine to Inference Control Plane: Connecting vLLM, llm-d, and the Evolution of Efficient Distributed LLM Serving</a></td><td>22</td><td>0</td><td>AI</td><td>vLLM/llm-d를 분산 추론 제어평면 관점으로 종합한 서베이, 신규 실험은 없음</td></tr>
<tr><td>808</td><td><a href='https://arxiv.org/abs/2609.23201'>Do Not Trust the Benchmark: Limitations of General LLM Rankings and a Case for Task-Specific Evaluation</a></td><td>22</td><td>0</td><td>AI</td><td>범용 LLM 랭킹의 한계를 논한 퍼스펙티브 논문, 실증 기여가 제한적임</td></tr>
<tr><td>809</td><td><a href='https://arxiv.org/abs/2609.23790'>Total Cost of Agency: Exact Attribution of Memory Injection Cost in Multi-Agent LLM Workflows</a></td><td>22</td><td>0</td><td>AI</td><td>멀티에이전트 워크플로의 메모리주입 비용을 정확히 귀속시키는 분해기법, 시스템 비용분석 기여임</td></tr>
<tr><td>810</td><td><a href='https://arxiv.org/abs/2609.23877'>Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery</a></td><td>22</td><td>0</td><td>AI</td><td>LLM 근거를 오프라인 사전계산해 지연없이 탐색추천에 적용한 산업사례, A/B 검증됨</td></tr>
<tr><td>811</td><td><a href='https://arxiv.org/abs/2609.24174'>CREDO: Variance-Guided Rubric Evolution for Replay-Corrected Credit Assignment</a></td><td>22</td><td>0</td><td>LG</td><td>신용할당을 위한 예비 이론보고서로 실증결과 없이 방법과 증명만 제시함</td></tr>
<tr><td>812</td><td><a href='https://arxiv.org/abs/2609.24784'>Convex AI Compositionality and the Governance of AI System Populations</a></td><td>22</td><td>0</td><td>AI</td><td>AI 시스템 집단의 형식적 정체성/거버넌스를 볼록공간으로 표현하는 이론적 프레임워크, 실증 사례는 예시 수준임</td></tr>
<tr><td>813</td><td><a href='https://arxiv.org/abs/2609.22614'>Concurrency-Aware Process Model Forecasting with Causal Nets</a></td><td>21</td><td>0</td><td>LG</td><td>프로세스 마이닝의 concurrency-aware causal net 예측, 니치 응용 연구임</td></tr>
<tr><td>814</td><td><a href='https://arxiv.org/abs/2609.24250'>Explainable Predictive Condition-based Maintenance of Naval-Propulsion Systems using Fuzzy Logic</a></td><td>21</td><td>0</td><td>LG</td><td>선박 추진시스템 예지보전을 위한 fuzzy decision tree 설명가능 프레임워크임</td></tr>
<tr><td>815</td><td><a href='https://arxiv.org/abs/2609.24358'>Explainable Neuro-Fuzzy Prediction for Trustworthy Decision-Making in Maritime</a></td><td>21</td><td>0</td><td>LG</td><td>선박 유지보수 예측을 위한 explainable neuro-fuzzy 프레임워크임</td></tr>
<tr><td>816</td><td><a href='https://arxiv.org/abs/2609.22786'>Distributed Infrastructure Sensors and Cues for Robotic Fire-Fighting and Safety System on a Lunar Base</a></td><td>20</td><td>3</td><td>Robotics/Space</td><td>달 기지 화재대응을 위한 QR코드 기반 분산 센서 인프라 프로토타입으로 로봇학습과는 거리가 멂</td></tr>
<tr><td>817</td><td><a href='https://arxiv.org/abs/2609.22594'>Characterizing Wildlife Response to Biomimetic and Conventional Underwater Vehicles</a></td><td>20</td><td>2</td><td>Robotics</td><td>생체모방 수중로봇이 야생동물 행동에 미치는 영향을 비교한 생태조사이며 로봇학습 기여는 거의 없음</td></tr>
<tr><td>818</td><td><a href='https://arxiv.org/abs/2609.22681'>A Direct Rigid Transmission 2-DoF Wrist Extension for Tendon-Driven Hand</a></td><td>20</td><td>2</td><td>Hardware</td><td>덱스터러스 핸드에 붙이는 2자유도 손목 확장 기구를 제안한 하드웨어 논문으로 연구 임팩트는 제한적임</td></tr>
<tr><td>819</td><td><a href='https://arxiv.org/abs/2609.24537'>MIRAGE: Full-Body Bystander Privacy for Smart Glasses with Consent-Based Restoration</a></td><td>20</td><td>1</td><td>CV</td><td>스마트글래스에서 전신 생체정보를 보호하는 동의 기반 프라이버시 아키텍처로 로봇과는 거리가 있음</td></tr>
<tr><td>820</td><td><a href='https://arxiv.org/abs/2609.22130'>Hierarchical Bayesian optimization of an aircraft-based multi-agent system-of-systems</a></td><td>20</td><td>1</td><td>LG</td><td>항공기 기반 다중 에이전트 system-of-systems를 위한 계층적 베이지안 최적화 연구로 로봇 자체보다 시스템 설계 최적화에 초점이 있음</td></tr>
<tr><td>821</td><td><a href='https://arxiv.org/abs/2609.24410'>End-to-end Jordanian dialect speech-to-text self-supervised learning framework</a></td><td>20</td><td>1</td><td>NLP</td><td>저자원 요르단 방언 음성인식 자기지도학습 프레임워크, 인간-로봇 상호작용을 응용처로 언급하나 실제 로봇 실험은 없음</td></tr>
<tr><td>822</td><td><a href='https://arxiv.org/abs/2609.22271'>Enabling Vision and Cross-Modal Learning for Multimodal Stroke Recurrence Prediction: An Interpretable Two-Step Framework</a></td><td>20</td><td>0</td><td>CV</td><td>뇌졸중 재발 예측용 멀티모달 의료 영상 분석이라 로봇 연구와 관련 없음</td></tr>
<tr><td>823</td><td><a href='https://arxiv.org/abs/2609.22281'>Performance vs Consistency: Evaluating a Foundation Model in Lung-RADS Screening</a></td><td>20</td><td>0</td><td>CV</td><td>폐암 스크리닝용 의료 foundation model 평가 연구로 로봇과 무관함</td></tr>
<tr><td>824</td><td><a href='https://arxiv.org/abs/2609.22284'>Complementary rPPG-Derived and Lip-Region Frequency Cues for Talking-Face Deepfake Detection</a></td><td>20</td><td>0</td><td>CV</td><td>talking-face 딥페이크 탐지용 rPPG·입술 주파수 단서 결합 연구로 로봇과 무관함</td></tr>
<tr><td>825</td><td><a href='https://arxiv.org/abs/2609.22315'>Yarn tracking of large-scale 3D textile reinforcements using topological material features</a></td><td>20</td><td>0</td><td>CV</td><td>항공기 부품 CT 영상에서 실 가닥을 추적하는 산업용 세그멘테이션 연구로 로봇과 무관함</td></tr>
<tr><td>826</td><td><a href='https://arxiv.org/abs/2609.22562'>AdaMerge: Tuning-Free Patch Compression for Multi-Vector Visual Document Retrieval</a></td><td>20</td><td>0</td><td>Multimodal</td><td>시각 문서 검색을 위한 패치 압축 기법으로 로봇과 무관한 정보 검색 효율화 연구임</td></tr>
<tr><td>827</td><td><a href='https://arxiv.org/abs/2609.23012'>CrowdCue: Specialist-Cue Conditioning for Vision-Language Crowd Counting</a></td><td>20</td><td>0</td><td>CV</td><td>VLM 기반 군중 계수에 전문가 단서를 결합한 연구로 로봇과 무관함</td></tr>
<tr><td>828</td><td><a href='https://arxiv.org/abs/2609.23026'>BrainIAC: Interactive 3D Brain Lesion Segmentation across Heterogeneous MRI Modalities with Online Adaptation</a></td><td>20</td><td>0</td><td>CV</td><td>이종 MRI 모달리티 간 뇌 병변 세그멘테이션 프레임워크로 임상 응용이라 로봇과 무관함</td></tr>
<tr><td>829</td><td><a href='https://arxiv.org/abs/2609.23139'>QwenVLConnector: A Fast, Unified Medical VLM Chatbot for Fine-Grained Clinical Perception and Text Generation</a></td><td>20</td><td>0</td><td>Multimodal</td><td>임상 세부 인식과 리포트 생성을 통합한 의료 VLM 챗봇으로 로봇과 무관함</td></tr>
<tr><td>830</td><td><a href='https://arxiv.org/abs/2609.23249'>Exact Quotients of Fresnel-Kummer Surfaces and Certified Biaxial Refraction</a></td><td>20</td><td>0</td><td>CV</td><td>복굴절 결정의 Fresnel 파면을 대수기하학적으로 규명한 이론 논문으로 로봇과 무관함</td></tr>
<tr><td>831</td><td><a href='https://arxiv.org/abs/2609.23408'>Accurate Motion Estimation with Bézier Control Point for Efficient Frame Interpolation</a></td><td>20</td><td>0</td><td>CV</td><td>베지어 제어점 기반 프레임 보간 정확도 개선 연구로 로봇과 무관함</td></tr>
<tr><td>832</td><td><a href='https://arxiv.org/abs/2609.23548'>SewFusion: Tailored Generation of Topology and Panel-Level Geometry for Sewing Patterns</a></td><td>20</td><td>0</td><td>CV</td><td>봉제 패턴의 토폴로지와 기하를 함께 생성하는 방법으로 패션 응용이라 로봇과 무관함</td></tr>
<tr><td>833</td><td><a href='https://arxiv.org/abs/2609.23553'>Modeling Clinical Workflow for SYNTAX Scoring from Coronary Angiography Videos</a></td><td>20</td><td>0</td><td>CV</td><td>관상동맥 조영술 영상에서 SYNTAX 점수를 임상 워크플로에 맞춰 계층적으로 추론하는 의료 연구로 로봇과 무관함</td></tr>
<tr><td>834</td><td><a href='https://arxiv.org/abs/2609.23596'>StyleAT: Defending Face Recognition Against Semantic Attacks</a></td><td>20</td><td>0</td><td>CV</td><td>얼굴 인식을 semantic adversarial 공격으로부터 방어하는 연구로 로봇과 무관함</td></tr>
<tr><td>835</td><td><a href='https://arxiv.org/abs/2609.23606'>Beyond UV Mapping: Mesh Texture Compression via Surface-Aligned Texture Fields</a></td><td>20</td><td>0</td><td>CV</td><td>UV 맵 대신 표면 정렬 texture field로 메시 텍스처를 압축하는 그래픽스 연구로 로봇과 무관함</td></tr>
<tr><td>836</td><td><a href='https://arxiv.org/abs/2609.24172'>LegendBench: A Diagnostic Benchmark for Legend Understanding with Counterfactual Interventions</a></td><td>20</td><td>0</td><td>Multimodal</td><td>차트 범례 이해를 counterfactual 개입으로 정밀 진단하는 벤치마크로 로봇과 무관함</td></tr>
<tr><td>837</td><td><a href='https://arxiv.org/abs/2609.24210'>ChartJudgeBench: Evaluating LMM Judges for Chart-to-Code Generation</a></td><td>20</td><td>0</td><td>Multimodal</td><td>차트-투-코드 작업에서 LMM judge의 신뢰성을 진단하는 벤치마크로 로봇과 무관함</td></tr>
<tr><td>838</td><td><a href='https://arxiv.org/abs/2609.24223'>DiaSeg: Diagonal Segment Extraction from DTW Paths for Interpretable Gait Analysis</a></td><td>20</td><td>0</td><td>CV</td><td>DTW 경로에서 대각 세그먼트를 추출해 보행을 해석 가능하게 분석하는 임상 연구로 로봇과 무관함</td></tr>
<tr><td>839</td><td><a href='https://arxiv.org/abs/2609.24330'>AlignMorph: Tuning-Free Diffusion Image Morphing via Explicit Semantic Transport</a></td><td>20</td><td>0</td><td>CV</td><td>기하 정렬과 생성적 디노이징을 분리한 tuning-free 이미지 모핑 연구로 로봇과 무관함</td></tr>
<tr><td>840</td><td><a href='https://arxiv.org/abs/2609.24875'>SPHQuant: Efficient extreme low bit weight quantization for Vision-Language Models</a></td><td>20</td><td>0</td><td>Multimodal</td><td>VLM의 극저비트 가중치 양자화를 위한 효율화 연구로 로봇과 무관함</td></tr>
<tr><td>841</td><td><a href='https://arxiv.org/abs/2609.22106'>PRQuant: Permutation Residual Quantization for Low-Overhead Inference</a></td><td>20</td><td>0</td><td>LG</td><td>선형 계층의 저비트 양자화 정확도를 개선하는 학습 없는 저오버헤드 프레임워크로 로봇과 무관함</td></tr>
<tr><td>842</td><td><a href='https://arxiv.org/abs/2609.22122'>Rank Portability Does Not Imply Feasibility Portability: Target-Specific Evaluation of Joint Hardware Constraints</a></td><td>20</td><td>0</td><td>LG</td><td>하드웨어 간 순위 이식성이 실현가능성 이식성을 보장하지 않음을 보인 NAS 평가 연구로 로봇과 무관함</td></tr>
<tr><td>843</td><td><a href='https://arxiv.org/abs/2609.22156'>The Limits of Speculation: Bounding Speculative Decoding in Mixture-of-Experts</a></td><td>20</td><td>0</td><td>LG</td><td>Mixture-of-Experts에서 speculative decoding의 검증 비용을 최단경로 문제로 분석한 연구로 로봇과 무관함</td></tr>
<tr><td>844</td><td><a href='https://arxiv.org/abs/2609.22158'>StepKV: Step-Aware KV Cache Compression for LLM Agents</a></td><td>20</td><td>0</td><td>LG</td><td>멀티스텝 LLM 에이전트를 위한 step-aware KV cache 압축 기법으로 로봇과 무관함</td></tr>
<tr><td>845</td><td><a href='https://arxiv.org/abs/2609.22182'>Gaussian Process Decorrelation for Spatiotemporal Deep Learning-Based Snow Water Equivalent Prediction</a></td><td>20</td><td>0</td><td>LG</td><td>적설량 예측용 GP 탈상관+LSTM 응용 연구, 새 학습 패러다임 제시 없음</td></tr>
<tr><td>846</td><td><a href='https://arxiv.org/abs/2609.22583'>Benchmarking Hybrid Deep Learning Architectures for Predictive Maintenance in Industry 4.0</a></td><td>20</td><td>0</td><td>LG</td><td>산업 예지보전용 RNN/Transformer 벤치마크, 700개 실험이나 novelty 낮음</td></tr>
<tr><td>847</td><td><a href='https://arxiv.org/abs/2609.24467'>A Temporal Knowledge Graph for Music Festival Lineup Forecasting</a></td><td>20</td><td>0</td><td>LG</td><td>음악 페스티벌 라인업 예측용 temporal knowledge graph 데이터셋·벤치마크 논문임</td></tr>
<tr><td>848</td><td><a href='https://arxiv.org/abs/2609.22536'>Cross-Dialect NER for Bangla Regional Dialects Using Leave-One-Dialect-Out Cross-Validation and Explainable AI</a></td><td>20</td><td>0</td><td>NLP</td><td>저자원 방언 NER 벤치마크와 LODOCV 평가, 벤치마크 기여 위주임</td></tr>
<tr><td>849</td><td><a href='https://arxiv.org/abs/2609.22774'>NLPCC 2026 Task 10: Citation-Level Faithfulness Verification with DeBERTa Ensembles and Class-Wise Calibration</a></td><td>20</td><td>0</td><td>NLP</td><td>공유과제 시스템 논문, 앙상블/캘리브레이션 위주 엔지니어링임</td></tr>
<tr><td>850</td><td><a href='https://arxiv.org/abs/2609.23573'>Error-Supervised Synthetic Learner Writing for Automated Essay Scoring</a></td><td>20</td><td>0</td><td>NLP</td><td>오류 주석 학습으로 AES용 합성 에세이 품질을 개선하는 응용적 기여임</td></tr>
<tr><td>851</td><td><a href='https://arxiv.org/abs/2609.23951'>HaikuS2S: A Cascaded System For Responding In Verse</a></td><td>20</td><td>0</td><td>NLP</td><td>하이쿠 운율 구조를 반영한 TTS 캐스케이드 시스템, 니치 응용임</td></tr>
<tr><td>852</td><td><a href='https://arxiv.org/abs/2609.24246'>Taramandal-GPT: Enhancing Astrodynamics Problem-Solving with Knowledge Retrieval and Structured Thinking</a></td><td>20</td><td>0</td><td>NLP</td><td>천체역학 문제풀이용 RAG 모델, 도메인 응용임</td></tr>
<tr><td>853</td><td><a href='https://arxiv.org/abs/2609.22620'>Splitting Documents at Lower Cost: Multi-Split Boundary Decisions for LLM-Based Page Stream Segmentation</a></td><td>20</td><td>0</td><td>AI</td><td>페이지 스트림 분할을 한 번의 호출로 다중 경계 예측, 효율성 개선 위주임</td></tr>
<tr><td>854</td><td><a href='https://arxiv.org/abs/2609.22712'>Trustworthy Agentic AI: Failure Modes, Mitigation Strategies, and a Lifecycle Framework for Autonomous LLM Systems</a></td><td>20</td><td>0</td><td>AI</td><td>에이전틱 AI 신뢰성 실패모드와 완화기법을 정리한 6단계 라이프사이클 프레임워크, 리뷰 성격으로 실증이 없음</td></tr>
<tr><td>855</td><td><a href='https://arxiv.org/abs/2609.23071'>Tutoring Large Language Models to be Domain-adaptive, Precise and Safe</a></td><td>20</td><td>0</td><td>AI</td><td>도메인적응/정렬/문화안전을 아우르는 박사논문 프리프린트, 개별 기여의 초점이 분산됨</td></tr>
<tr><td>856</td><td><a href='https://arxiv.org/abs/2609.23945'>Echo State Network (ESN) for Signal Recovery in RF-Impaired IBFD MIMO Systems</a></td><td>20</td><td>0</td><td>AI</td><td>에코상태망으로 IBFD MIMO 자기간섭을 제거하는 신호처리 연구, 로봇과 무관한 통신분야 응용임</td></tr>
<tr><td>857</td><td><a href='https://arxiv.org/abs/2609.24036'>Structured Decomposition for Reliable LLM-Generated Access Control Policies</a></td><td>20</td><td>0</td><td>AI</td><td>자연어 접근정책을 Rego 코드로 변환하는 파이프라인, 구조화 분해가 정확도를 3배 개선함</td></tr>
<tr><td>858</td><td><a href='https://arxiv.org/abs/2609.24198'>SKstars at SHROOM: Visions Agreement-Guided Ensembling of Zero-Shot and LoRA-Adapted Vision--Language Models</a></td><td>20</td><td>0</td><td>Multimodal</td><td>시각언어모델 환각탐지 공유과제 참가 시스템, 앙상블 위주 엔지니어링임</td></tr>
<tr><td>859</td><td><a href='https://arxiv.org/abs/2609.24755'>Epi-Logic: A Conceptual Framework for Epistemic Runtime Control, Schema Validity Checking, and Controlled Accommodation in Autonomous AI Agents</a></td><td>20</td><td>0</td><td>AI</td><td>스키마 불일치를 탐지하는 인식론적 런타임 통제 개념 프레임워크, 실증검증 없이 가설만 제시함</td></tr>
<tr><td>860</td><td><a href='https://arxiv.org/abs/2609.24883'>A Global Comparison of Schemas, Transparency, and Interoperability in Public-Sector AI Registers and Inventories</a></td><td>20</td><td>0</td><td>AI</td><td>72개국 공공AI 레지스터의 스키마/투명성을 비교분석한 정책연구, 기술적 기여보다 거버넌스 진단 성격임</td></tr>
<tr><td>861</td><td><a href='https://arxiv.org/abs/2609.23687'>A multi-temporal dataset for mapping burned areas in the Brazilian Cerrado using time series of remote sensing imagery</a></td><td>19</td><td>0</td><td>CV</td><td>브라질 세하두 지역 화재 탐지용 다중시기 데이터셋 공개 논문임</td></tr>
<tr><td>862</td><td><a href='https://arxiv.org/abs/2609.23456'>Smartphone GNSS Booster: Centimeter-Level Pedestrian Positioning Using a Portable Signal Re-Radiator</a></td><td>18</td><td>2</td><td>Localization/Hardware</td><td>스마트폰 GNSS 신호를 재복사해 보행자 위치정확도를 높이는 안테나 하드웨어 연구로 로봇학습과 무관함</td></tr>
<tr><td>863</td><td><a href='https://arxiv.org/abs/2609.22333'>Dimensionality reduction for AI based hyperspectral image classification based on XAI</a></td><td>18</td><td>0</td><td>CV</td><td>목재 재활용을 위한 초분광 영상 차원축소·XAI 응용 연구로 로봇과 무관함</td></tr>
<tr><td>864</td><td><a href='https://arxiv.org/abs/2609.22392'>Style as Cover: Deep Image Steganography via Stylized Transmission</a></td><td>18</td><td>0</td><td>CV</td><td>스타일 전이 기반 이미지 스테가노그래피 연구로 로봇과 무관함</td></tr>
<tr><td>865</td><td><a href='https://arxiv.org/abs/2609.22631'>X-Beat: An Explainable Framework for ECG Image Classification</a></td><td>18</td><td>0</td><td>CV</td><td>ECG 영상 분류용 설명가능 프레임워크로 의료 응용이며 로봇과 무관함</td></tr>
<tr><td>866</td><td><a href='https://arxiv.org/abs/2609.22647'>Math2Visual-X: A Modular Framework for Pedagogically Aligned Lower-Primary Math Visuals Generation</a></td><td>18</td><td>0</td><td>Multimodal</td><td>초등 수학 문제용 교육 시각자료 생성 프레임워크로 로봇과 무관함</td></tr>
<tr><td>867</td><td><a href='https://arxiv.org/abs/2609.23268'>Blind Deconvolution of Binary and Pattern Images with Pixel Intensity Constraints and Sparse Gradient Prior</a></td><td>18</td><td>0</td><td>CV</td><td>이진·패턴 이미지의 blind deconvolution 연구로 고전 영상처리 문제이며 로봇과 무관함</td></tr>
<tr><td>868</td><td><a href='https://arxiv.org/abs/2609.23586'>An Efficient and Effective Watermarking Scheme for the Protection of the Intellectual Property Rights of Video Generative Models</a></td><td>18</td><td>0</td><td>CV</td><td>비디오 생성 모델의 저작권 보호를 위한 워터마킹 기법으로 로봇과 무관함</td></tr>
<tr><td>869</td><td><a href='https://arxiv.org/abs/2609.23679'>Mind the Gaps: A Curated Benchmark for Form Field Detection</a></td><td>18</td><td>0</td><td>CV</td><td>문서 양식 필드 탐지용 벤치마크로 로봇과 무관함</td></tr>
<tr><td>870</td><td><a href='https://arxiv.org/abs/2609.23830'>DFD-Lab: A Modular Audio-Visual Deepfake Detection Pipeline</a></td><td>18</td><td>0</td><td>CV</td><td>오디오-비주얼 딥페이크 탐지 모듈형 파이프라인으로 로봇과 무관함</td></tr>
<tr><td>871</td><td><a href='https://arxiv.org/abs/2609.23832'>Comparative Performance and Parameter-Efficient Adaptation of DINOv2 for Active Trachoma Classification</a></td><td>18</td><td>0</td><td>CV</td><td>트라코마 분류를 위한 DINOv2 파라미터 효율적 적응 비교 연구로 로봇과 무관함</td></tr>
<tr><td>872</td><td><a href='https://arxiv.org/abs/2609.23983'>Evaluating the Generalization of Neuroimaging Foundation Models on African Brain MRI</a></td><td>18</td><td>0</td><td>CV</td><td>아프리카 뇌 MRI에서 neuroimaging foundation model의 일반화를 평가한 연구로 로봇과 무관함</td></tr>
<tr><td>873</td><td><a href='https://arxiv.org/abs/2609.24058'>All-in-One Multilingual Scene Text Recognition with Script-aware Mixture-of-Experts</a></td><td>18</td><td>0</td><td>CV</td><td>다국어 장면 텍스트 인식을 위한 script-aware MoE 연구로 로봇과 무관함</td></tr>
<tr><td>874</td><td><a href='https://arxiv.org/abs/2609.24095'>HDND: Hierarchical Dynamic Neural Decoding for Multilingual Word/Character Retrieval from Non-Invasive Brain Recordings</a></td><td>18</td><td>0</td><td>CV</td><td>비침습 뇌 신호로부터 다국어 단어를 계층적으로 디코딩하는 BCI 연구로 로봇과 무관함</td></tr>
<tr><td>875</td><td><a href='https://arxiv.org/abs/2609.24109'>Adaptive Cortically Constrained EEG-Vision Alignment for Zero-Shot Brain-to-Image Retrieval</a></td><td>18</td><td>0</td><td>CV</td><td>피질 제약을 반영한 EEG-비전 정렬로 zero-shot 뇌-이미지 검색을 개선한 연구로 로봇과 무관함</td></tr>
<tr><td>876</td><td><a href='https://arxiv.org/abs/2609.24136'>The Visual Target Matters: Learning across the Visual Hierarchy for Brain-to-Image Retrieval</a></td><td>18</td><td>0</td><td>CV</td><td>시각 계층 전체를 학습 타겟으로 활용하는 뇌-이미지 검색 연구로 로봇과 무관함</td></tr>
<tr><td>877</td><td><a href='https://arxiv.org/abs/2609.24190'>Benchmarking Off-the-Shelf Multimodal AI Models Against Dermatologists on Patient-Captured Skin Images</a></td><td>18</td><td>0</td><td>CV</td><td>환자 촬영 피부 영상에 대해 멀티모달 AI와 피부과 전문의를 비교한 벤치마크로 로봇과 무관함</td></tr>
<tr><td>878</td><td><a href='https://arxiv.org/abs/2609.24215'>Beyond Emotion Prompts: Fine-Grained Text-to-Image Generation Driven by Valence-Arousal-Dominance</a></td><td>18</td><td>0</td><td>CV</td><td>valence-arousal-dominance 좌표로 감정을 세밀하게 제어하는 text-to-image 생성 연구로 로봇과 무관함</td></tr>
<tr><td>879</td><td><a href='https://arxiv.org/abs/2609.24468'>MIGA:Shared-Geometry Gaussian Representation with Implicit Amplitude Modeling for Accelerated 3D Multi-Echo MRI</a></td><td>18</td><td>0</td><td>CV</td><td>3D multi-echo MRI 가속 재구성을 위한 공유 기하 Gaussian 표현 연구로 의료 영상이며 로봇과 무관함</td></tr>
<tr><td>880</td><td><a href='https://arxiv.org/abs/2609.24524'>Preoperative Prediction of Microvascular Invasion in Hepatocellular Carcinoma by Integrating Multimodal Ultrasound and Clinical Data: A Multicenter Study</a></td><td>18</td><td>0</td><td>CV</td><td>간세포암 미세혈관 침습을 멀티모달 초음파로 술전 예측하는 임상 연구로 로봇과 무관함</td></tr>
<tr><td>881</td><td><a href='https://arxiv.org/abs/2609.24627'>FedMust: Semi-supervised Multi-task Student-Teacher Federated Learning for Multi-organ CT Segmentation</a></td><td>18</td><td>0</td><td>CV</td><td>다기관 CT 장기 분할을 위한 반지도 연합학습 프레임워크로 로봇과 무관함</td></tr>
<tr><td>882</td><td><a href='https://arxiv.org/abs/2609.24732'>GraphSVR: q-Space--Aware Graph-Based Slice-to-Volume Registration for Diffusion MRI</a></td><td>18</td><td>0</td><td>CV</td><td>확산 MRI의 q-space 인지 그래프 기반 slice-to-volume 정합 연구로 로봇과 무관함</td></tr>
<tr><td>883</td><td><a href='https://arxiv.org/abs/2609.24736'>MiTHras: Task-specific Hierarchical Semi-supervised Contrastive Masked Autoencoder for Mitotic Figure Analysis</a></td><td>18</td><td>0</td><td>CV</td><td>유사분열 세포 분석을 위한 계층적 반지도 대조 마스크 오토인코더 연구로 로봇과 무관함</td></tr>
<tr><td>884</td><td><a href='https://arxiv.org/abs/2609.24769'>Brain Metastases Segmentation for BraTS 2026 Task 1: A Multi-Architecture Comparison</a></td><td>18</td><td>0</td><td>CV</td><td>BraTS 2026 뇌전이 세그멘테이션을 위한 다중 아키텍처 비교 연구로 로봇과 무관함</td></tr>
<tr><td>885</td><td><a href='https://arxiv.org/abs/2609.24894'>SLICEChat: Progressive In-Encoder Token Pruning for Whole-Slide Pathology Language Models</a></td><td>18</td><td>0</td><td>Multimodal</td><td>병리 슬라이드 언어모델의 점진적 인코더 내 토큰 프루닝 효율화 연구로 로봇과 무관함</td></tr>
<tr><td>886</td><td><a href='https://arxiv.org/abs/2609.22117'>LE4Mob: Towards Inductive, Distance-Aware and General-Purpose Location Embedding for Human Mobility Modelling</a></td><td>18</td><td>0</td><td>LG</td><td>인간 이동성 모델링을 위한 귀납적·거리 인지 위치 임베딩 프레임워크로 로봇과 무관함</td></tr>
<tr><td>887</td><td><a href='https://arxiv.org/abs/2609.22145'>Weak Ties, Strong Signals: Efficient Training Data Detection in Diffusion LLMs via Independent Token Sampling</a></td><td>18</td><td>0</td><td>NLP</td><td>diffusion LLM에서 독립 토큰 샘플링으로 학습 데이터 유출을 탐지하는 프라이버시 연구로 로봇과 무관함</td></tr>
<tr><td>888</td><td><a href='https://arxiv.org/abs/2609.22153'>SafeTune: A Unified Faithful Library for Auditing and Repairing Safety Drift in Fine-Tuned LLMs</a></td><td>18</td><td>0</td><td>LG</td><td>fine-tuned LLM의 안전성 저하를 감사·복구하는 통합 라이브러리로 로봇과 무관함</td></tr>
<tr><td>889</td><td><a href='https://arxiv.org/abs/2609.22157'>PAGE: Partition-Aware Gated KV-Cache Eviction</a></td><td>18</td><td>0</td><td>NLP</td><td>KV-cache eviction을 입력별 admission 결정 문제로 재구성한 LLM 추론 효율화 연구로 로봇과 무관함</td></tr>
<tr><td>890</td><td><a href='https://arxiv.org/abs/2609.22185'>Adaptive Physics-Informed Neural Networks for the Blasius Boundary-Layer Problem</a></td><td>18</td><td>0</td><td>LG</td><td>Blasius 경계층 방정식 풀이용 PINN 하이퍼파라미터 탐색, 좁은 물리 문제에 국한됨</td></tr>
<tr><td>891</td><td><a href='https://arxiv.org/abs/2609.22244'>Universal Observatory Graphs for Distributed Sky Coverage and Artificial Intelligence Based Interplanetary Routing</a></td><td>18</td><td>0</td><td>LG</td><td>행성 간 관측소 네트워크 커버리지·라우팅을 그래프+Q-learning으로 푼 니치 응용 연구임</td></tr>
<tr><td>892</td><td><a href='https://arxiv.org/abs/2609.22734'>Clinical Domain Classification from Medical Transcriptions</a></td><td>18</td><td>0</td><td>NLP</td><td>전통 ML 대 트랜스포머 비교와 데이터 밸런싱 실험, 방법론 신규성 없음</td></tr>
<tr><td>893</td><td><a href='https://arxiv.org/abs/2609.22796'>AlexandriaX 2026: The First Shared Task on Dialectal Arabic Machine Translation</a></td><td>18</td><td>0</td><td>NLP</td><td>방언 아랍어 MT 공유과제 소개 논문, 벤치마크 구축이 기여임</td></tr>
<tr><td>894</td><td><a href='https://arxiv.org/abs/2609.24016'>Context-Aware Pre-Deployment Evaluation of AI Systems: A Regulatory Framework for Nigerian Fintech</a></td><td>18</td><td>0</td><td>AI</td><td>나이지리아 핀테크 AI 규제 프레임워크 제안, 정책논문 성격임</td></tr>
<tr><td>895</td><td><a href='https://arxiv.org/abs/2609.24625'>Custom Named Entity Recognition and Topic Classification for Global Health Publications</a></td><td>18</td><td>0</td><td>NLP</td><td>자원제약 환경에서의 NER/토픽분류 모델선택을 비교한 학위논문 성격 연구임</td></tr>
<tr><td>896</td><td><a href='https://arxiv.org/abs/2609.22192'>SegTSim: A Big Data Driven Segmented Temporal Simulation Framework for Heterogeneous Multivariate Systems</a></td><td>17</td><td>0</td><td>LG</td><td>무역 시계열 시뮬레이션 프레임워크, 공학적 응용 수준의 기여임</td></tr>
<tr><td>897</td><td><a href='https://arxiv.org/abs/2609.22229'>A Synthetic Multivariate Refrigerator Time-Series Dataset for Predictive Maintenance</a></td><td>16</td><td>0</td><td>LG</td><td>합성 냉장고 시계열 데이터셋 공개 논문, 새 방법론 기여 없음</td></tr>
<tr><td>898</td><td><a href='https://arxiv.org/abs/2609.22593'>User-Level Handover Decision Making Based on Machine Learning Approaches</a></td><td>16</td><td>0</td><td>LG</td><td>이동통신 핸드오버 결정을 위한 고전 ML 방법 비교, 통신 응용 연구임</td></tr>
<tr><td>899</td><td><a href='https://arxiv.org/abs/2609.22917'>An Iterative LangGraph Agent for Text-to-SQL: Natural Language Access to the Chicago Crime Database</a></td><td>16</td><td>0</td><td>NLP</td><td>단일 모델 엔지니어링 평가로 학술적 기여가 낮음</td></tr>
<tr><td>900</td><td><a href='https://arxiv.org/abs/2609.22750'>Towards Robust Classroom Attendance: A Comprehensive Evaluation of Face Detection and Recognition Models</a></td><td>15</td><td>0</td><td>CV</td><td>교실 출석용 얼굴 인식 데이터셋·평가 연구로 로봇과 무관함</td></tr>
<tr><td>901</td><td><a href='https://arxiv.org/abs/2609.23017'>Reconstructed holograms and explanation-aware evaluation for low-cost computational pollen analysis in veterinary cytology</a></td><td>15</td><td>0</td><td>CV</td><td>수의학용 저비용 홀로그램 꽃가루 분석 연구로 로봇과 무관함</td></tr>
<tr><td>902</td><td><a href='https://arxiv.org/abs/2609.23345'>AniPrO: Interpretable Anime Image Provenance Detection via Multi-Dimensional Semantic Reasoning</a></td><td>15</td><td>0</td><td>CV</td><td>애니메이션 이미지의 생성 출처를 판별하는 프레임워크로 로봇과 무관함</td></tr>
<tr><td>903</td><td><a href='https://arxiv.org/abs/2609.23397'>Enhancing Shrimp Disease Detection via Deep Learning and Data Refinement for Resilient Aquaculture</a></td><td>15</td><td>0</td><td>CV</td><td>새우 질병 탐지용 ViT·SSL 응용 연구로 로봇과 무관함</td></tr>
<tr><td>904</td><td><a href='https://arxiv.org/abs/2609.23450'>Rule-Constrained Assignment for Cue-Ball Identification in Broadcast Snooker</a></td><td>15</td><td>0</td><td>CV</td><td>방송 스누커 영상에서 큐볼을 식별하는 규칙 기반 할당 문제로 로봇과 무관함</td></tr>
<tr><td>905</td><td><a href='https://arxiv.org/abs/2609.23714'>Infectious Bovine Pinkeye Detection Using Computer Vision and Imbalance-Aware Learning</a></td><td>15</td><td>0</td><td>CV</td><td>소 눈병 탐지를 위한 YOLO 응용 연구로 로봇과 무관함</td></tr>
<tr><td>906</td><td><a href='https://arxiv.org/abs/2609.23769'>PRISM-RAG: Multimodal Hypergraph Retrieval-Augmented Generation for Tobacco Product and Legislative Policy Reasoning</a></td><td>15</td><td>0</td><td>NLP</td><td>담배 제품 관련 관할권별 법령을 다루는 멀티모달 hypergraph RAG 연구로 로봇과 무관함</td></tr>
<tr><td>907</td><td><a href='https://arxiv.org/abs/2609.24049'>U-PEN Mamba: Progressive Expansion with Selective State-Space Modeling for Efficient Retinal Vessel Segmentation</a></td><td>15</td><td>0</td><td>CV</td><td>망막 혈관 세그멘테이션을 위한 Mamba 기반 효율적 아키텍처로 의료 응용이며 로봇과 무관함</td></tr>
<tr><td>908</td><td><a href='https://arxiv.org/abs/2609.24064'>Vision Transformers versus convolutional neural networks for fine-grained orchid genus identification in a species-rich, data-poor flora: a controlled benchmark on the Orchidaceae of New Guinea</a></td><td>15</td><td>0</td><td>CV</td><td>뉴기니 난초속 식별을 위한 ViT·CNN 비교 벤치마크로 로봇과 무관함</td></tr>
<tr><td>909</td><td><a href='https://arxiv.org/abs/2609.24116'>Patch-to-Global: Random Patch Diffusion for Globally Consistent Megapixel Artifact Inpainting in Whole Slide Images</a></td><td>15</td><td>0</td><td>CV</td><td>병리 슬라이드 영상의 메가픽셀급 아티팩트를 복원하는 패치 diffusion 연구로 로봇과 무관함</td></tr>
<tr><td>910</td><td><a href='https://arxiv.org/abs/2609.24220'>Document Retrieval-Aware Chunking (D-RAC): Universal Retrieval-Aware Ingestion of Enterprise Documents via PDF Normalization and Multimodal Markdown Conversion</a></td><td>15</td><td>0</td><td>NLP</td><td>기업 문서를 위한 검색 인지 청킹 시스템으로 로봇과 무관함</td></tr>
<tr><td>911</td><td><a href='https://arxiv.org/abs/2609.24228'>IMPLICIT-Bench: Measuring Implicit Bias in Text-to-Image Models under Neutral Prompts</a></td><td>15</td><td>0</td><td>CV</td><td>중립 프롬프트에서 text-to-image 모델의 암묵적 편향을 측정하는 벤치마크로 로봇과 무관함</td></tr>
<tr><td>912</td><td><a href='https://arxiv.org/abs/2609.24492'>Identity-Consistent Analysis of Long-Shot Windsurfing Video: A Domain-Specific Offline Tracking System</a></td><td>15</td><td>0</td><td>CV</td><td>윈드서핑 영상에서 라이더별 안정적 트래킹을 만드는 도메인 특화 오프라인 시스템으로 로봇과 무관함</td></tr>
<tr><td>913</td><td><a href='https://arxiv.org/abs/2609.24560'>Evaluating Transformation Models for pCLE Mosaic Registration</a></td><td>15</td><td>0</td><td>CV</td><td>공초점 레이저 내시현미경 모자이크 정합 변환 모델 평가 연구로 로봇과 무관함</td></tr>
<tr><td>914</td><td><a href='https://arxiv.org/abs/2609.24634'>High-resolution Nitrogen Dioxide Maps Reveal Exposure Limit Breaches across Europe</a></td><td>15</td><td>0</td><td>CV</td><td>유럽 이산화질소 고해상도 지도 제작 연구로 로봇과 무관함</td></tr>
<tr><td>915</td><td><a href='https://arxiv.org/abs/2609.24814'>Mobile Imaging Solutions for Medical Diagnosis: Trends and Applications</a></td><td>15</td><td>0</td><td>CV</td><td>스마트폰 등 모바일 기기를 이용한 의료 영상 진단 동향을 정리한 서베이로 로봇과 무관함</td></tr>
<tr><td>916</td><td><a href='https://arxiv.org/abs/2609.24937'>Anatomy-Decomposed Chest Computed Tomography (CT) Projections as Scalable Supervision for Bone Suppression in Chest Radiographs</a></td><td>15</td><td>0</td><td>CV</td><td>CT를 뼈·연조직·폐로 분해한 투영으로 흉부 방사선 사진의 뼈 억제를 학습시키는 의료 영상 연구로 로봇과 무관함</td></tr>
<tr><td>917</td><td><a href='https://arxiv.org/abs/2609.22113'>Toward Fairness in Machine Learning Models for Predicting Treatment Retention and Premature Discontinuation in Medication for Opioid Use Disorder</a></td><td>15</td><td>0</td><td>LG</td><td>아편계 치료제 유지·중단 예측 ML 모델의 공정성을 평가한 연구로 로봇과 무관함</td></tr>
<tr><td>918</td><td><a href='https://arxiv.org/abs/2609.22121'>Modelling daily activity patterns from mobile phone location data via deep representation learning</a></td><td>15</td><td>0</td><td>LG</td><td>휴대폰 위치 데이터로 일일 활동 패턴을 표현학습하는 도시 컴퓨팅 연구로 로봇과 무관함</td></tr>
<tr><td>919</td><td><a href='https://arxiv.org/abs/2609.22123'>StationPDE: Station-Oriented Surface PDE Learning for Multi-Station Multivariate Weather Forecasting</a></td><td>15</td><td>0</td><td>LG</td><td>다중 관측소 지표 기상 예보를 위한 station-oriented PDE 학습 모델로 로봇과 무관함</td></tr>
<tr><td>920</td><td><a href='https://arxiv.org/abs/2609.22126'>SolarFlowRefiner: Refinement-Aware Flow Matching for Surface Solar Radiation Downscaling</a></td><td>15</td><td>0</td><td>LG</td><td>지표 태양복사를 고해상도로 다운스케일링하는 flow matching 연구로 로봇과 무관함</td></tr>
<tr><td>921</td><td><a href='https://arxiv.org/abs/2609.22129'>Helix-FNO: Spectral-Domain Operator Learning Coupled with a High-Fidelity Mechanistic Model for Fast Surrogate Simulation</a></td><td>15</td><td>0</td><td>LG</td><td>처리 공정 시뮬레이션을 위한 스펙트럴 도메인 연산자 학습 대체 모델로 로봇과 무관함</td></tr>
<tr><td>922</td><td><a href='https://arxiv.org/abs/2609.22154'>A Comparative Framework for Evaluating Foundation Models on Tabular Data: A Case Study in Healthcare</a></td><td>15</td><td>0</td><td>LG</td><td>표 형태 데이터용 foundation model을 헬스케어 사례로 비교 평가하는 프레임워크로 로봇과 무관함</td></tr>
<tr><td>923</td><td><a href='https://arxiv.org/abs/2609.22155'>From Latent Biomarkers to Clinical Rules: Embedding-Guided Rule Mining and Attribution-Based Translation for Interpretable Tabular Learning</a></td><td>15</td><td>0</td><td>LG</td><td>잠재 바이오마커를 임상 규칙으로 변환하는 해석 가능한 표 형태 학습 연구로 로봇과 무관함</td></tr>
<tr><td>924</td><td><a href='https://arxiv.org/abs/2609.22160'>Uncertainty and Business-Aware Remaining Useful Life Estimation for Semiconductor Manufacturing</a></td><td>15</td><td>0</td><td>LG</td><td>반도체 제조 설비의 불확실성 인지 잔여수명 추정 예지보전 연구로 로봇과 무관함</td></tr>
<tr><td>925</td><td><a href='https://arxiv.org/abs/2609.22166'>Clustering-Based Collective Anomaly Detection in IoT Systems: A Graph Neural Network Approach</a></td><td>15</td><td>0</td><td>LG</td><td>IoT 시스템의 집단 이상 탐지를 위한 클러스터링 기반 GNN 연구로 로봇과 무관함</td></tr>
<tr><td>926</td><td><a href='https://arxiv.org/abs/2609.22790'>From Research Frontier to Laboratory Bench: Design of a Four-Tier Experimental Teaching System for Multimodal Medical Image Intelligent Diagnosis</a></td><td>14</td><td>0</td><td>AI</td><td>의료영상 AI 실습 커리큘럼 설계 논문, 연구 기여보다 교육설계 성격이 강함</td></tr>
<tr><td>927</td><td><a href='https://arxiv.org/abs/2609.24014'>WebMRIQC: A Web-Based Implementation of MRIQC for Accessible MRI Image Quality Assessment in Resource-Constrained Settings</a></td><td>12</td><td>0</td><td>CV</td><td>자원 제약 환경을 위한 웹 기반 MRI 품질관리 도구로 로봇과 무관함</td></tr>
<tr><td>928</td><td><a href='https://arxiv.org/abs/2609.24384'>A Lightweight Convolutional Neural Network for Real-Time Recognition of Hand-Drawn Geometric Shapes</a></td><td>12</td><td>0</td><td>CV</td><td>손으로 그린 기하 도형을 인식하는 경량 CNN 데스크톱 앱 연구로 로봇과 무관함</td></tr>
<tr><td>929</td><td><a href='https://arxiv.org/abs/2609.22165'>TARGet: Topology-Aware Fusion-based Radio Frequency Circuit Functional Modeling using Graph Neural Networks</a></td><td>12</td><td>0</td><td>LG</td><td>RF 회로 기능 모델링을 위한 토폴로지 인지 GNN 연구로 로봇과 무관함</td></tr>
<tr><td>930</td><td><a href='https://arxiv.org/abs/2609.22167'>Role-Aware Morgan Fingerprints for Reaction Yield Prediction</a></td><td>12</td><td>0</td><td>LG</td><td>반응 수율 예측을 위한 역할 인지 Morgan fingerprint 방법으로 화학 응용이며 로봇과 무관함</td></tr>
<tr><td>931</td><td><a href='https://arxiv.org/abs/2609.22249'>A Tutorial on Prompt Engineering: From Messy Thoughts to AI Workflows</a></td><td>12</td><td>0</td><td>NLP</td><td>실무 가이드라인 성격의 프롬프트엔지니어링 튜토리얼로 연구 기여 없음</td></tr>
</tbody></table>

</details>
