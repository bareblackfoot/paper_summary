# 오늘의 arXiv Top 15 — 2026-09-04 (금)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**
> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)

**신규 논문 수: 전체 367편 → 중복 제거 후 367편 (이번 평가 대상 367편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 102 |
| cs.LG | 85 |
| cs.RO | 36 |
| cs.CL | 75 |
| cs.AI | 69 |

*1차 스크리닝: 전체 367편을 제목/초록 기반으로 채점(Claude (scheduled agent)) → 상위 15편은 arXiv 원문을 내려받아 정밀 리뷰(Claude (scheduled agent)) 후 최종 점수 산정.*

---

## Top 15

### 1. [76점] Puffin-World: Scaling a Unified Multimodal Model with Native 3D World States

- **분야**: World Model / Unified Multimodal 3D Perception · **robotics relevance**: 7/10
- **arXiv**: [2609.04196](https://arxiv.org/abs/2609.04196) ([PDF](https://arxiv.org/pdf/2609.04196))
- **저자**: Kang Liao, Yihang Luo, Xiao-Ming Wu, Linyi Jin, Size Wu, Chunyu Lin, Yao Zhao, Fei Wang 외 2명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: Project Page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 Puffin-World는 물리(중력·위도)·기하(depth)·외형(RGB)을 native world state로 명시해 하나의 멀티모달 프레임워크에서 카메라 이해·생성·재구성을 동시에 수행하는 world model임. 참조 프레임의 절대 중력 방향을 미래 프레임까지 전파하는 physics propagation으로 방향 drift를 줄이는 것을 목표로 하며, 생성 품질의 정량 결과는 본문에서 확인 불가함.

**Core innovation & methodology**

- physics(중력장·위도)·geometry(depth)·appearance(RGB)를 native 3D world state로 분리해 하나의 프레임워크에서 perception·generation·reconstruction을 통합함.
- Omni-Camera representation: gravity-anchored absolute field(up-vector, latitude)와 relative ray field를 9채널로 결합해 single-view·cross-view 조건을 하나로 통일함.
- physics propagation: reference view에서 추정한 절대 중력 방향을 relative rotation으로 미래 프레임에 전파해 trajectory 전체가 하나의 절대 좌표계를 공유하게 함.
- depth를 3D Hilbert curve 기반 invertible color mapping으로 RGB화해 동일 frozen VAE로 appearance와 함께 flow-matching으로 동시 생성함(asymmetric attention과 zero-init geometry embedding으로 appearance 성능 보존).

**Novelty vs. prior works**

- 가장 가까운 prior work인 Puffin 대비 본질적 차이는 persistent world frame의 유무임. Puffin은 isolated single-view 카메라 이해·생성만 다루지만 Puffin-World는 physics propagation으로 trajectory 전체에 절대 좌표계를 부여하고 reconstruction까지 통합함.
- camera representation 자체(절대+상대 결합)는 Perspective Field와 Plücker ray 계열 표현을 조합한 것이라 표현 방식의 novelty는 제한적임. 새로움은 이를 diffusion latent에 pixel-aligned additive injection으로 넣고 trajectory에 전파한 시스템 설계에 있음.
- depth를 Hilbert curve 매핑으로 RGB화해 별도 encoder 없이 기존 VAE로 처리하는 방식은 기존 아이디어(Vision Banana)를 world model 맥락에 적용한 것이라 응용 novelty에 가까움.

**Benchmark results**

- camera-to-world understanding에서 Stanford2D3D 기준 roll error 0.29도, pitch error 0.53도로 GeoCalib(0.40도/0.93도)·UVP(0.52도/0.95도) 대비 개선되고 AUC@5도가 roll 97.4%, pitch 88.8%로 비교 방법 중 최고임.
- 비교 baseline은 DeepCalib, CTRL-C, ParamNet, GeoCalib, AnyCalib 등 카메라 calibration 전용 모델임. 본문에서 확인 가능한 정량 수치는 Stanford2D3D 결과뿐이고 MegaDepth·TartanAir·LaMAR 결과는 표 후반부가 텍스트 추출 과정에서 생략되어 확인 불가.
- 학습 데이터 Puffin-16M은 vision-language-camera triplet 1500만 개와 challenging-motion trajectory 100만 개로 구성되며 기존 Puffin-4M(400만) 대비 규모가 크고, 공개 데이터셋 28개(약 4450만 이미지)에 절대 카메라 파라미터 주석을 추가로 공개함.
- physics propagation의 효과를 보여주는 ablation(Fig. 12)이 존재하나 정량 수치는 본문에서 확인 불가하고 정성적 예시만 제시됨.
- free-viewpoint 생성 품질, 3D world modeling의 reconstruction 정확도, multi-task synergy(mimic·self-calibrated exploration) 관련 정량 결과와 limitation 절은 텍스트 추출이 5.2 후반부터 결론까지 생략되어 본문에서 확인 불가. real-robot 실험은 없음(실내·파노라마 이미지 기반 world model).

**Top-tier conference 적합성 — 75/100 · 추천 venue: CVPR**

native 3D world state 통합, physics propagation, 1500만 규모 신규 데이터셋과 44.5M 이미지 카메라 주석 공개, camera-to-world understanding SOTA까지 스케일과 재현성 면에서 CVPR 강점을 가짐. 다만 핵심 카메라 표현은 기존 기법의 조합이고, 확인된 정량 벤치마크가 이해 태스크 일부에 국한돼 생성·재구성 품질에 대한 강한 실험적 증거가 본문 기준으로는 부족해 oral보다는 highlight~poster 수준의 rejection risk가 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- self-calibrated world exploration(중력 오정렬을 예측 action과 imagined observation으로 자동 감지·보정)은 failure detection·recovery 우선주제와 맥락이 닿음. VLA policy의 test-time self-correction 설계에 참고할 만함.
- physics propagation의 절대 좌표계 anchoring 아이디어는 robot manipulation에서 world model 기반 test-time planning 시 long-horizon 상태 drift를 줄이는 데 응용 가능함.
- appearance-geometry joint latent 생성은 object-centric 3DGS/scene reconstruction 파이프라인의 pretraining 신호로 쓸 수 있으나, real-robot 검증이 없고 실내·파노라마 이미지 도메인 중심이라 manipulation task로의 전이는 별도 검증이 필요함.

---

### 2. [76점] RoboTok: An Internet-Scale Data Engine for Human Demonstration Retrieval and Dexterous Manipulation Learning

- **분야**: Manipulation / Robot Data Retrieval · **robotics relevance**: 9/10
- **arXiv**: [2609.03199](https://arxiv.org/abs/2609.03199) ([PDF](https://arxiv.org/pdf/2609.03199))
- **저자**: Howard Qian, Yiting Chen, Yunfei Xie, Kejia Ren, Podshara Chanrungmaneekul, Gaotian Wang, Bowen Wen, Chen Wei 외 1명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 인터넷 동영상 속 사람의 손 움직임을 actor 중심 3D trajectory로 변환해, query 시연과 비슷한 조작 동작을 검색하는 RoboTok을 제안함. 이 검색 결과로 dexterous manipulation policy를 학습시키면 STRAP·HAND 등 기존 retrieval 방법보다 시뮬레이션 성공률이 크게 올라감.

**Core innovation & methodology**

- internet-scale retrieval 프레임워크 RoboTok을 제안, human manipulation video를 query로 웹 비디오에서 유사 조작 시연을 non-parametric하게 검색함
- 핵심 표현은 actor-centered 3D hand trajectory임. camera 좌표계의 hand pose를 hand wrist frame만으로 추정한 torso frame 기준으로 정규화해 viewpoint 변화·occlusion에 무관하게 만듦
- 정규화된 trajectory 쌍의 DTW(dynamic time warping) alignment cost를 pseudo-GT 유사도로 삼아 lightweight encoder를 학습함. set loss(top-K 이웃 판별)와 rank loss(순서 보존)를 결합
- offline으로 100K clip을 한 번씩 인코딩해 inner-product index를 구축하고, query 시 cosine similarity로 top-K를 검색해 전체 corpus와 DTW를 다시 계산하지 않고도 확장 가능하게 설계함

**Novelty vs. prior works**

- 가장 가까운 prior work은 STRAP(ICLR 2025, visual foundation feature+DTW로 고정 robot corpus 내부 검색), HAND(ICRA 2026, 2D hand-robot path 매칭, self-collected robot play 대상), FlowRetrieval(optical flow 기반)임. 이들은 fixed robot corpus 혹은 2D/이미지 공간 motion에 한정됨
- RoboTok의 본질적 차이는 query와 검색 대상이 모두 internet human video라는 점, 그리고 3D actor-relative hand trajectory라는 명시적 motion representation을 쓴다는 점임. camera coordinate가 아니라 추정된 torso frame 기준이라 occlusion과 viewpoint 변화에 강함
- 다만 구성 요소(WiLoR hand pose 추정, MoGe-2 metric depth, HaWoR infill, torso frame estimator, DTW 기반 metric learning)는 대부분 기존 방법의 조합임. novelty는 architecture가 아니라 representation·retrieval formulation에 있고, 이 formulation 자체는 STRAP·HAND의 자연스러운 확장으로 볼 여지도 있음

**Benchmark results**

- RoboTok evaluation corpus(Action100M 기반 N=100K, 10K held-out query)에서 mAP@20=0.353, Recall@20=0.996, Kendall τ=0.487로, 최강 baseline STRAP(mAP@20=0.007, Recall@20=0.12)을 크게 앞섬
- 외부 corpus AssemblyHands(N=831, cross-dataset domain shift)에서도 mAP@5=0.261 vs STRAP 0.133으로 우위가 유지돼 순위가 바뀌지 않음
- VTDexManip sim benchmark(6 task, PPO reward guidance만 사용, robot action label 미사용)의 원 formulation에서 6개 중 5개 task에서 최고 pretrained baseline(VT-JointPretrain)을 능가, 평균 seen +7.45%p / unseen +5.83%p
- 저자가 dense reward를 제거하고 3D hand control을 복원한 harder formulation(3 task)에서 BottleCap Turning 77.3%(HAND 대비 +17.8%p), Faucet Screwing 44.8%(+38.0%p), Lever Sliding 79.3%(+59.8%p)로 격차가 더 커짐. 다만 이 harder task는 논문이 자체 정의한 변형이라 외부 검증이 없음
- 모든 downstream 실험이 simulation이며 real-robot 실험은 없음. policy 학습도 imitation이 아니라 retrieved clip을 reward shaping(potential-based)으로만 사용하는 PPO 방식임

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL**

internet-scale demonstration retrieval이라는 새로운 데이터 엔진 formulation과, 여러 baseline·cross-dataset 대비 일관되게 큰 retrieval·policy 성능 격차가 강점임. 다만 downstream 검증이 simulation 6-task, PPO reward-shaping에 그치고 real-robot deployment가 전무하며, 평가 지표(DTW)가 학습 오라클과 동일해 성능 우위가 부분적으로 순환적일 수 있어 rejection risk가 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- test-time에 유사 조작 시연을 검색해 policy guidance로 쓰는 방식은 failure recovery 시 참조 시연을 검색해 복구 전략을 세우는 test-time retrieval/adaptation 아이디어로 확장 가능함
- actor-centric 대신 object-centric 3D reference frame(3DGS·scene graph 연구와 결합)으로 retrieval하면 object-relative manipulation motion을 더 정확히 잡을 수 있어 우리 연구와 연결 여지가 있음
- VLA post-training용 dexterous manipulation 데이터 확보 파이프라인 참고용으로 유용함. real robot에 이식 시 reward-shaping이 아니라 imitation 학습으로 바꿨을 때도 효과가 유지되는지 검증할 필요가 있음

---

### 3. [68점] WISE: World-model-guided Imagination Scheduling for Efficient Post-training of Vision-Language-Action Models

- **분야**: VLA / World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.03681](https://arxiv.org/abs/2609.03681) ([PDF](https://arxiv.org/pdf/2609.03681))
- **저자**: Chenhao Zhang, Hanyu Zhao, Hang Cheng, Tengfei Pan, Long Zeng
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 78점

> 💡 VLA post-training에서 world model 상상(imagination)을 아무 상태에나 쓰지 않고 interaction-relevant 상태에서만 선택적으로 짧게 굴려 GRPO 스타일로 policy를 업데이트하는 WISE를 제안함. π0/π0.5에서 MimicGen 5개 task 평균 성공률을 각각 9.8/7.9%p 올리면서 world model 연산은 full imagination 대비 약 77% 줄였고 real robot에서도 개선을 확인함.

**Core innovation & methodology**

- DINOv2 기반 lightweight scheduler로 현재 시점이 imagination이 필요한 interaction-relevant 상태인지 판단해 world model 호출을 선택적으로 트리거함
- 선택된 상태에서만 action-conditioned multi-view world model(Open-Sora 기반)로 L-chunk bounded rollout을 굴려 긴 horizon에서 누적되는 예측 오류를 제한함
- 별도 학습된 reward model이 progress/confidence/completion 신호를 결합해 imagined trajectory를 평가하고, imagined state-action을 직접 supervision으로 쓰지 않고 후보 간 상대적 advantage로만 GRPO 업데이트에 반영함
- reliability filter(ranking consistency, reward uncertainty, reward separation 기준)로 신뢰도 낮은 imagination 그룹을 걸러내고 real interaction context에서 나온 첫 action chunk만 실제로 학습에 씀

**Novelty vs. prior works**

- world model로 VLA를 post-training하는 흐름 자체는 WMPO, World4RL, VLA-RFT, AtomVLA, RISE 등 이미 여러 편 있고 이 논문도 그 계열에 속함. 본질적 차이는 imagination을 '언제·어디서' 쓸지 스케줄링하는 것을 명시적 학습 대상으로 만든 점임
- bounded rollout + 상대적 advantage(GRPO 스타일)로 imagined trajectory를 direct supervision이 아닌 counterfactual 평가로만 쓰는 설계는 world model prediction error 누적 문제에 대한 실용적 해법으로 타당함
- 다만 본문 baseline은 GRPO/DSRL/DPO(비-world model 계열)뿐이고, 가장 가까운 prior work인 WMPO·World4RL·VLA-RFT·AtomVLA·RISE와 직접 성능 비교가 없어 '스케줄링이 기존 world-model 기반 post-training보다 낫다'는 핵심 주장의 실험적 근거는 약함

**Benchmark results**

- MimicGen 5개 task 시뮬레이션: π0 49.7%→59.5%(+9.8%p), π0.5 52.3%→60.2%(+7.9%p), 가장 강한 baseline인 π0+DPO(53.8%) 대비 +5.7%p
- imagination scheduling ablation(Stack/Threading/Mug Cleanup 평균): full imagination 60.4%(138 states, 11.45 GPU h) 대비 WISE 68.3%(28 states, 2.61 GPU h)로 성공률은 높이고 GPU 시간은 약 77% 절감함. uniform(61.1%)·random(59.1%) scheduling보다도 우수함
- reward model ablation: progress-only/completion-only 각각 57.3%로 full reward(68.3%) 대비 낮아 progress+completion+confidence+backward penalty 조합이 유효함을 보임
- real robot(Galaxea R1 Lite, 4 task, standard/generalization 각 20 trial): π0 기준 표준 60.0%→77.5%(+17.5%p), generalization 42.5%→68.8%(+26.3%p); π0.5 기준 표준 61.3%→77.5%, generalization 50.0%→71.3%로 distribution shift 상황에서 개선폭이 더 큼
- reward model 최종 discrimination은 AUROC 0.938~1.000(5개 task)로 sim 데이터 기준 수치이며 real-world reward model 정확도는 별도 보고 없음

**Top-tier conference 적합성 — 62/100 · 추천 venue: CoRL**

real robot 4-task 평가와 GPU 연산 절감이라는 실용적 강점, π0/π0.5 두 backbone에 걸친 일관된 개선은 CoRL/RSS 계열 review에서 설득력 있음. 다만 가장 가까운 world-model 기반 post-training 경쟁작(WMPO, World4RL, VLA-RFT 등)과 직접 비교가 없고 real robot이 단일 플랫폼·task당 20 trial로 통계적 검증력이 약해 reviewer가 novelty와 baseline 비교 부족을 지적할 위험이 있음. 코드는 논문 시점 미공개(anonymous repo, publication 후 공개 예정)임.

**추천 이유 & 누리랩 연구와의 연결점**

- imagination scheduling(언제 world model을 불러올지 판단하는 lightweight visual classifier) 아이디어는 test-time optimization/inference-time planning에서 연산 예산을 실패 위험이 높은 지점에 집중시키는 방식으로 failure detection 연구에 바로 연결 가능함
- bounded rollout + reliability filter(ranking consistency, reward uncertainty)는 world model 예측이 신뢰 가능한 horizon을 정량적으로 판정하는 방법론이라 counterfactual reasoning 기반 실패 예측/recovery 연구에 참고할 틀임
- reward model이 progress/confidence/completion을 분리해 학습하는 구조는 robot memory나 object-centric representation과 결합해 장기 task의 stage-aware 평가로 확장할 여지가 있음

---

### 4. [67점] Sensing Which Modality Matters: Evidence-Gated Regularization for Robust VLA Policies

- **분야**: VLA / Multimodal Robustness · **robotics relevance**: 10/10
- **arXiv**: [2609.03142](https://arxiv.org/abs/2609.03142) ([PDF](https://arxiv.org/pdf/2609.03142))
- **저자**: Yue Yang, Diego Romeres, Chiori Hori, Gedas Bertasius, Daniel Szafir, Siddarth Jain
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 여러 센서를 쓰는 VLA 정책이 적은 로봇 시연 데이터 때문에 센서 간 가짜 상관관계를 학습하는 문제를 modality entanglement로 정의함. 프레임·센서별 evidence score로 무관한 센서엔 invariance를, 유효한 센서엔 single-sensor sufficiency를 강제하는 EGR을 제안해 시뮬레이션과 실로봇 두 플랫폼에서 성공률을 개선함.

**Core innovation & methodology**

- modality entanglement를 nuisance sensitivity(무관한 센서 왜곡에도 행동이 변함)와 single-modality insufficiency(유효 센서 하나만 남아도 실패함) 두 실패 모드로 formalize함
- task 구조(focal/interaction object의 픽셀 면적, tactile contact 여부)로부터 프레임·센서별 evidence score E_{t,m}을 계산함. end-to-end 학습이 아니라 heuristic으로 부여함
- evidence를 hinge weight로 게이팅해 낮은 evidence 센서엔 invariance loss, 높은 evidence 센서엔 single-sensor sufficiency loss를 적용하고 base policy(π0.5) 구조는 그대로 둠
- 2|M|번 필요한 추가 forward pass를 importance sampling으로 스텝당 2회로 줄이고 unbiased 추정임을 증명함

**Novelty vs. prior works**

- 가장 가까운 prior work인 modality dropout(Liu et al. 2017)과 adversarial multi-sensor consistency(Guo et al. 2025)는 센서·시점을 균일하게 다뤄 state-dependent 선택을 못하는데, EGR은 task-grounded evidence로 프레임마다 다르게 게이팅한다는 점이 차별점임
- TacVLA의 contact gate는 tactile·binary contact에 특화된 반면, EGR은 동일 프레임워크를 vision·tactile에 공통 적용 가능하게 일반화함
- evidence score 자체는 instance segmentation, focal/interaction object 라벨, tactile reference pattern 같은 사전 정의된 task 구조에 의존함 - 저자도 in-hand reorientation처럼 evidence를 미리 정의할 수 없는 경우엔 적용 불가능하다고 명시해 novelty가 학습 목적함수 설계에 국한됨

**Benchmark results**

- BEHAVIOR-1K 기반 47개 skill(NAV 11 + MAN 36) 시뮬레이션에서 π0.5 대비 SR을 Full 12.5%→16.4%(+31%), NoUseless 9.4%→16.5%(+75%), UsefulOnly 2.8%→6.1%(+118%)로 개선함
- 절대 성공률은 최고 16.5%로 낮음 - BEHAVIOR-1K challenge task 자체의 baseline 성능이 낮은 상태에서의 상대 개선폭임
- 실로봇 bi-manual(Kinova 2팔 + RGB 3대) 4개 task에서 RealDistractor SR 30%→85%(+183%, Fisher's exact p<0.001, N=40)로 가장 큰 개선을 보임
- 실로봇 vision-tactile(MELFA ASSISTA + GelSight 2개) 2개 task에서 SingleUseful SR 40%→90%(+125%, p=0.0022)는 유의하지만 RealDistractor 55%→70%는 유의하지 않음(p=0.51, N=20)
- ModDrop baseline과 비교해 Suite1 action-deviation ratio·Suite2 SR 대부분에서 EGR이 우세하나, Suite2 NAV Full(p=0.875)과 MAN Full(vanilla 대비 p=0.065)은 통계적으로 유의하지 않음

**Top-tier conference 적합성 — 62/100 · 추천 venue: CoRL**

서로 다른 두 embodiment(양팔 RGB, 단일팔+촉각) real-robot 검증과 Wilcoxon·Fisher's exact 유의성 검정을 꼼꼼히 보고한 점이 CoRL/RSS 수준의 실험적 conviction을 보여줌. 다만 시뮬레이션 절대 성공률이 여전히 낮고(최고 16.5%) clean 조건과 tactile RealDistractor에서 통계적 유의성이 없어 rejection risk로 지적될 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- evidence-gated invariance/sufficiency 개념은 누리랩 failure detection/recovery 연구에서 실패 감지 후 어떤 센서를 신뢰해 fallback할지 판단하는 test-time 모듈로 확장 가능함
- vision evidence 계산에 쓰는 instance segmentation·focal/interaction object 라벨을 object-centric 3DGS나 scene graph로 대체하면 evidence score를 3D 표현에서 직접 얻어 사전 라벨링 의존을 줄일 수 있음
- evidence가 사전 정의된 task 구조에만 의존하는 한계는 world model 기반 counterfactual reasoning(센서를 가상으로 perturb했을 때 예측 변화 측정)으로 evidence를 학습하는 방향으로 이어질 수 있음

---

### 5. [66점] FailBench: How Reliable are VLMs at Judging Robot Task Success?

- **분야**: Manipulation / Failure Detection · **robotics relevance**: 8/10
- **arXiv**: [2609.03611](https://arxiv.org/abs/2609.03611) ([PDF](https://arxiv.org/pdf/2609.03611))
- **저자**: Zaruhi Navasardyan, Tatul Danielyan, Hrant Davtyan
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 64점

> 💡 FailBench는 14개 공개 소스에서 모은 2,197개 로봇 매니퓰레이션 시도로 VLM 기반 실패 판정기 13종을 하나의 프로토콜에서 교차 평가함. 최고 모델(Gemini 3 Flash)도 balanced accuracy 0.77에 그치고, 접촉 여부로 성공을 판단해야 하는 assembly task에서는 0.60 이하로 chance에 가까운 수준까지 떨어짐.

**Core innovation & methodology**

- 12개 real-world·2개 simulated 소스를 하나의 스키마(instruction, 영상, binary label)로 묶어 단일 프로토콜 cross-source failure detection 벤치마크 FailBench를 구성함
- 샘플의 75%는 자연발생 실패이고 6개 소스는 애초에 failure detection용으로 만들어지지 않은 데이터라, detector가 인위적 실패 생성 절차의 흔적을 학습해 점수를 얻는 것을 차단함
- general-purpose VLM 6종, embodied VLM 2종, failure detection 특화 모델 5종 총 13개 detector를 balanced accuracy로 동일 프롬프트·디코딩 설정 하에 평가함
- 실패 판정에 필요한 시각적 근거(물체 이동 vs 물리적 접촉)에 따라 성능이 갈린다는 걸 진단하고, outcome-relevant 영역을 먼저 찾아 crop하는 evidence-localization pipeline을 추가 학습 없이 적용해 최고 모델을 2.3~2.4pt 개선함

**Novelty vs. prior works**

- 기존 실패탐지 벤치마크(Guardian/RLBench-Fail·BridgeDataV2-Fail·UR5-Fail, RoboFAC, ViFailback, AHA, I-FailSense)는 모두 단일 수집 캠페인에서 나와 로봇·카메라·라벨링 절차가 고정돼 있고 실패를 인위적으로 구성함. FailBench는 이를 14개 독립 소스로 확장해 정량적으로 문제를 드러낸 최초 사례라는 점이 핵심 기여임
- 방법론적 기여는 새 아키텍처나 representation이 아니라 벤치마크 구성과 crop 기반 test-time intervention 하나뿐이라 novelty는 benchmark/empirical finding에 국한됨
- specialist detector 5종 전부가 자신의 base VLM보다 낮은 성능을 보인다는 결과는 강한 실험적 증거지만, 원인 분석은 정성적 사례 관찰 수준(reasoning trace 일부 검토)에 머무르고 통계적으로 검증되지는 않음

**Benchmark results**

- 13개 detector 중 최고 성능은 Gemini 3 Flash로 macro balanced accuracy 0.77(micro 0.74), 2위 Gemma-4-31B-it 0.75
- contact-rich assembly(NIST task board 기반 reassemble)에서는 전 모델이 0.60 이하, 최고 모델도 0.60에 그쳐 chance에 가까움
- failure detection 특화 모델 5종(Guardian, RoboReward-8B, ViFailback-8B, RoboFAC-7B, FailSense-Calvin-3B) 전부가 fine-tuning 전 base VLM 대비 성능 하락(예: ViFailback-8B 0.587 vs base Qwen3-VL-8B-Instruct 0.675)
- evidence-localization crop(Gemini 3 Flash를 localizer+detector로 사용)으로 macro balanced accuracy가 0.773→0.797(+2.3pt)로 오름(223개 샘플 개선·160개 악화, McNemar p=0.0015)
- 상위 3개 모델의 majority vote ensemble은 +2pt 개선에 그치고 평가 비용이 3배로 늘어 실용성이 낮음
- real 환경(var≈0.0135)이 simulation(var≈0.0089)보다 모델 간 성능 분산이 커서, sim에서 고른 judge가 real 배포에서 그대로 통하지 않을 수 있음을 시사함. 다만 real-robot policy 자체를 새로 학습·검증한 실험은 없고 기존 공개 데이터의 재평가에 한정됨

**Top-tier conference 적합성 — 55/100 · 추천 venue: NeurIPS Datasets & Benchmarks Track 또는 CoRL**

2,197개 샘플·14개 독립 소스·13개 detector를 아우르는 규모와 McNemar test, error-set IoU, published-score 재현 검증까지 갖춘 진단이 뒷받침돼 empirical conviction은 강함. 다만 새로운 모델·representation·학습 방법 제안 없이 벤치마크와 간단한 test-time crop 개선에 그쳐 top-tier 메인트랙 oral보다는 benchmark/dataset 트랙이나 workshop에 적합함. rejection risk는 방법론적 기여 부족과 진단 분석 상당수가 단일 모델(Gemma-4-31B-it) 사례 관찰에 의존한다는 점임.

**추천 이유 & 누리랩 연구와의 연결점**

- VLM judge를 reward·평가 라벨·retry trigger로 쓰는 누리랩 failure detection/recovery 연구에 직접 활용 가능. FailBench 수치(상한 0.77, contact-rich에서 chance)를 파이프라인 설계 시 신뢰도 상한선 근거로 인용할 만함
- 접촉 여부 판정이 시각 정보만으로는 어렵다는 결과는 tactile perception이나 force-torque 신호를 world model·failure detector에 결합하는 연구 방향의 근거가 됨(논문도 future work로 명시)
- evidence-localization(수 프레임으로 outcome-relevant region을 먼저 찾고 crop하는 2단계 pipeline)은 test-time optimization·active perception 관점에서 실패 판정뿐 아니라 recovery 여부 판단에도 응용해볼 만한 단순한 test-time intervention 사례임

---

### 6. [64점] GIFT: Guided Intermediate Feature Training via Action-Oriented Structural Supervision for Robotic Manipulation

- **분야**: VLA / World-Action Model (표현학습, robotic manipulation) · **robotics relevance**: 9/10
- **arXiv**: [2609.04193](https://arxiv.org/abs/2609.04193) ([PDF](https://arxiv.org/pdf/2609.04193))
- **저자**: Yupeng Zheng, Xiang Li, Songen Gu, Yuhang Zheng, Shuai Tian, Weize Li, Linbo Wang, Chaoyue Li 외 6명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 74점

> 💡 GIFT는 VLA와 world-action model(WAM)의 중간 시각 feature에 geometry·affordance·goal 세 구조적 감독을 학습 시점 제약으로만 부여하는 프레임워크임. LIBERO-Plus zero-shot transfer에서 baseline 대비 4.6~12.6%p, RoboCasa에서 8.4~12.6%p 성능을 올림.

**Core innovation & methodology**

- action-sufficiency gap을 정의함: action-only 또는 pixel reconstruction 목적함수만으로는 geometry·affordance·instruction 관련 구조가 중간 feature에 보존되지 않는다는 문제를 지적함.
- geometry alignment: frozen VGGT teacher feature를 방향(cosine)과 크기(log-scale)로 분해해 얕은 층 student feature에 정렬시킴.
- affordance prediction: instruction 관련 객체와 end-effector를 anchor 상대좌표계의 20차원 pose+closure state로 표현해 object-centric 상호작용 구조를 예측하게 함.
- goal-region reconstruction: instruction-conditioned binary mask를 BCE+Dice로 예측해 조작 대상 영역을 국소화함.

**Novelty vs. prior works**

- 개별 signal(geometry alignment, affordance prediction, goal mask)은 SpatialVLA·GeoVLA·Spatial Forcing, CoA-VLA·RoboPoint, ReconVLA 등 기존 연구가 이미 다룬 방식이라 요소 자체의 novelty는 제한적임.
- 본질적 차이는 세 signal을 하나의 objective로 묶어 VLA·direct-action WAM·inverse-dynamics WAM이라는 서로 다른 action 생성 구조에 동일하게 적용한 점임. 기본형(no-injection)에서는 세 objective 모두 auxiliary loss로만 작용하고 action head에 직접 주입되지 않으며, 이 구조가 오히려 injection보다 낫다는 것을 실험으로 보임.
- 저자도 concurrent affordance-centric 연구(AffordanceVLA, AffordVLA)와의 중복을 인정하며 기여를 architecture-specific interface가 아닌 architecture-flexible principle로 규정함. 조합·검증 중심 기여로 봐야 함.

**Benchmark results**

- LIBERO(in-distribution)에서 GIFT 세 variant 모두 baseline 대비 0.1~1.3%p 개선에 그침. baseline이 이미 96~98%대로 saturated돼 차이가 작음.
- LIBERO-Plus(7종 perturbation, zero-shot transfer)에서 GIFT-VLA 79.6%(StarVLA-OFT 75.0% 대비 +4.6%p), GIFT-WAM-Fast 72.6%(Fast-WAM 60.0% 대비 +12.6%p), GIFT-WAM-IDM 87.8%(Fast-WAM-IDM 82.6% 대비 +5.2%p, 전체 비교 방법 중 1위)임.
- RoboCasa(GR1 humanoid, 24 task, LIBERO와 다른 embodiment)에서 GIFT-WAM-Fast 83.6%(+9.0%p), GIFT-WAM-IDM 82.3%(+8.4%p), GIFT-VLA 61.4%(+12.6%p)로 개선. articulated-object task에서는 WAM variant가 +21.3~24.6%p로 가장 크게 개선됨.
- single-guidance ablation에서 geometry·affordance·goal 각각 단독으로도 baseline 대비 개선되며 셋을 합칠 때 최고 성능을 보여 상호 보완적임을 시사함. 단 GIFT-VLA는 개별 gain의 합(2.1+4.0+4.1)이 결합 gain(4.6)보다 커 signal 간 중복 효과가 있어 보임.
- injection보다 no-injection이 낫다는 결과와 real-robot(xArm7, 듀얼암 ARX X5) 평가가 본문에 언급되나, PDF 추출 과정에서 본문 중간(ablation 상세·real-robot 수치·limitation)이 생략돼 구체적 수치는 본문에서 확인 불가.

**Top-tier conference 적합성 — 62/100 · 추천 venue: CoRL / RSS**

VLA·direct-action WAM·inverse-dynamics WAM 세 action formulation에 동일 원리를 적용하고 zero-shot transfer·다른 embodiment(RoboCasa)·real-robot까지 검증한 실험 규모는 top-tier venue 수준으로 보임. 다만 geometry·affordance·goal 개별 signal 자체는 기존 연구의 재조합에 가깝고 비교 baseline 다수가 2026년 arXiv preprint(미검증 학회)라 novelty와 비교 공정성 측면에서 rejection risk가 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- test-time optimization/world model 연구에서 구조적 signal(geometry·affordance·goal)을 training-time constraint로만 쓰고 inference에는 teacher를 배제하는 no-injection 설계는 우리 lab의 representation shaping 논의에 참고할 만함.
- affordance target을 anchor-relative 20-D pose+closure state로 정의한 방식은 failure detection·recovery에서 object-centric interaction 상태를 명시적으로 추적하는 representation으로 확장 가능함.
- future-conditioned inverse-dynamics WAM에 동일한 구조적 감독을 얹어 최고 성능(87.8%)을 얻은 결과는 world model 기반 test-time planning과 구조적 representation을 결합하는 실험의 참고 사례가 됨.

---

### 7. [62점] GraFT: A Training-Free Framework for Spatial Reasoning in Multimodal Large Language Models via 3D Scene Graphs

- **분야**: Embodied AI (3D Scene Graph 기반 공간추론) · **robotics relevance**: 7/10
- **arXiv**: [2609.03892](https://arxiv.org/abs/2609.03892) ([PDF](https://arxiv.org/pdf/2609.03892))
- **저자**: Junqing Du, Fernando Ropero, Erkin Turkoz, Yanfeng Zhang, Lu Liu
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 65점

> 💡 GraFT는 3D scene graph(3DSG) 하나에서 기하 도구·BEV 렌더링·egocentric frame 선택 세 모듈을 파생시켜 frozen MLLM에 학습 없이 공간추론 능력을 부여하는 프레임워크임. VSI-Bench에서 frozen backbone 대비 최대 18.8점(3B 기준) 성능 향상을 보이고, fine-tuned spatial model 여러 개도 능가함.

**Core innovation & methodology**

- 하나의 3DSG를 symbolic 기하 도구(count/size/distance/proximity/room), task-conditioned BEV 렌더링, geometry 기반 egocentric frame retrieval 세 모듈이 공유하는 구조를 제안함.
- 질문 유형에 따라 세 모듈 중 하나로 routing하는 tool-selection 방식이라 backbone은 학습 없이 그대로 사용함.
- BEV 모듈은 질의와 관련된 object만 정확한 비율의 box footprint로 렌더링하고 나머지 scene은 생략해 clutter를 제거함.
- egocentric 모듈은 visibility gate(코너 수·거리·시야각)를 통과한 프레임에 proximity×centrality×coverage 점수를 매겨 top-k만 backbone에 전달함.

**Novelty vs. prior works**

- 3DSG 기반 tool 호출(TIGeR, SpaceTools)과 BEV 렌더링(Struct2D, GPT4Scene)은 각각 이미 있던 아이디어이고, GraFT는 이를 한 그래프 위에서 라우팅하는 방식으로 묶은 조합형 기여에 가까움. 새로운 representation이나 learning paradigm은 아님.
- 가장 가까운 prior work인 Struct2D 대비 차이는 BEV를 질의 관련 object만 선택적으로 렌더링한다는 점과, perception(3DSG 구축)을 한 번만 수행해 질문마다 재실행하지 않는다는 점(perception amortization)임.
- egocentric frame selection의 점수 함수는 거리·중심성·커버리지를 곱한 직관적 기하 휴리스틱이라, 학습된 view selector 대비 novelty는 제한적임.

**Benchmark results**

- ScanQA egocentric 모듈: 동일 Qwen2.5-VL-7B backbone에서 uniform sampling 대비 CIDEr 58.0→73.6(+27%), BLEU-1 22.2→34.2로 상승했고, fine-tuned Chat-3D(CIDEr 53.2)도 능가함.
- VSI-Bench 전체(8개 subtask 평균): GraFT(InternVL2-8B)가 51.4로 1위이며, 최고 proprietary 모델 Gemini-1.5 Pro(45.4)와 최고 open-source general 모델(40.9)을 넘고 VG LLM-8B(50.7) 등 fine-tuned spatial model 다수도 상회함.
- backbone별 향상폭은 Qwen2.5-VL-3B +18.8, Qwen2.5-VL-7B +17.0, InternVL2-8B +13.9이며, GraFT 3B(47.5)가 72B general-purpose baseline(40.9)을 앞섬.
- ground-truth perception과 realistic perception(Mask3D/UniDet3D 재구성) 간 격차가 큼 — 예: GPT-o3 symbolic tool 정확도가 95.2에서 58.0으로 떨어져, 실제 성능이 upstream perception 품질에 크게 좌우됨.
- ablation: 단일 모듈만 쓰면(Tools 45.9/BEV 29.4/Ego 35.4) 질문별 routing을 쓰는 전체 시스템(50.0)보다 낮음. 실험은 indoor 정적 scene(ScanNet/ScanNet++/ARKitScenes) 기반이며 real-robot 검증은 없음.

**Top-tier conference 적합성 — 58/100 · 추천 venue: AAAI**

3DSG 기반 training-free 라우팅으로 fine-tuned spatial model을 능가하는 결과가 강점이고, ground-truth·realistic perception 양쪽에서 체계적으로 검증함. 다만 핵심 구성요소(BEV 렌더링, tool 호출, scene graph)가 각각 prior work의 재조합에 가까워 conceptual novelty가 크지 않고, indoor 정적 scene에 한정되며 real-robot 실험이 없어 top-tier oral보다는 AAAI/CVPR poster급으로 rejection risk가 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- 3DSG를 symbolic tool·BEV·egocentric evidence로 라우팅하는 구조는 누리랩의 scene graph/semantic mapping과 object-centric 3D representation 연구에 evaluation·reasoning layer로 바로 붙일 수 있음.
- GT 대비 realistic perception에서 성능이 크게 떨어지는 결과는 failure detection/recovery, robot memory 연구에서 3DSG 신뢰도 추정 문제로 연결 가능함.
- 단일 tool call만 지원하고 chaining이 없다는 한계는 test-time optimization 기반 multi-step tool reasoning으로 확장할 여지가 있어 VLA의 inference-time planning 연구와 접목 가능함.

---

### 8. [60점] SV-WAM: An Efficient Surround-View World-Action Model for End-to-End Autonomous Driving

- **분야**: World Model / Autonomous Driving · **robotics relevance**: 7/10
- **arXiv**: [2609.03602](https://arxiv.org/abs/2609.03602) ([PDF](https://arxiv.org/pdf/2609.03602))
- **저자**: Jinyang Wang, Shiwei Li, Junjian Wang, Zhiqiang Deng, Jianbin Gao, Yihang Zhao, Liu Liu, Yongjia Zhao 외 7명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: 23 pages, 16 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 65점

> 💡 SV-WAM은 6-view surround-view 관측을 유지하면서 future-video 예측을 학습 시점 supervision으로만 쓰고 추론 시엔 action만 생성하는 world-action model임. action-centered causal mask로 action token이 future-video token을 보지 못하게 막아 video branch를 배포 단계에서 제거함. NAVSIMv2에서 91.0 EPDMS로 SOTA를 달성하면서 341ms의 낮은 지연시간을 보임.

**Core innovation & methodology**

- action-centered causal mask로 action token이 future-video token에 attention하지 못하게 막아 p(A,Z|Ω)=p(A|Ω)p(Z|Ω,A)로 인수분해함. 학습 때만 video denoising이 shared parameter를 통해 supervision을 주고, 추론 시엔 video branch를 통째로 제거함.
- 단일 Wan2.2-5B DiT backbone에서 6-view future action과 6-view future-video latent를 flow matching으로 공동 denoising함. 별도 video/action expert 없이 하나의 shared 모델로 학습함.
- differentiable drivable-area compliance regularizer를 제안함. NAVSIM 공식 LQR tracker와 kinematic bicycle model을 PyTorch로 재구현해 gradient를 살리고, ego 4-corner footprint의 signed distance에 soft margin+log-mean-exp aggregation을 적용해 non-drivable 영역 침범을 벌점화함.
- 추론 시 observation prefix의 key/value를 캐싱해 재사용하고 action denoising을 2 step으로 줄여, 6-view 입력에서도 341.6ms의 낮은 latency를 달성함.

**Novelty vs. prior works**

- future-video를 학습 supervision으로만 쓰고 추론에서 action-only로 도는 패러다임 자체는 Fast-WAM, GigaWorld-Policy가 이미 embodied/general robot 영역에서 제시함. SV-WAM은 이 원리를 surround-view 자율주행 도메인에 옮긴 domain adaptation 성격이 강해 novelty가 제한적임.
- Fast-WAM이 video DiT와 action expert DiT를 별도 Mixture-of-Transformers로 두는 것과 달리, SV-WAM은 attention mask 하나로 단일 모델 안에서 같은 효과를 냄. 아키텍처를 단순화했다는 점이 차별점이지만 개념적 도약은 크지 않음.
- drivable-area regularizer는 NAVSIM 평가 지표(DAC)를 미분 가능한 학습 objective로 옮긴 것으로, 평가 지표를 학습 신호로 재구현한다는 아이디어 자체는 새롭지 않고 도메인 내 engineering 기여에 가까움.

**Benchmark results**

- NAVSIMv2 navtest 기준 EPDMS 91.0으로 C×6 조건 SOTA임. 동일 프레임워크의 C×1은 89.3, C×3은 90.5로 view 수 증가가 일관되게 성능을 올림.
- DriveVLA-W0(86.7), PWM(88.2), DriveLaW(88.9), EponaV2(88.9) 등 world-model 기반 baseline 대비 2~4점 EPDMS 우위이나, 이들 baseline은 대부분 C×1(front-view only) 조건이라 입력 조건이 다름.
- ablation(Table 3)에서 video co-training이 EPDMS 83.1→87.7, DAC regularizer 추가가 87.7→90.1(DAC 95.6→98.6), 최종 fine-tuning이 91.0까지 올려 세 구성요소 모두 기여가 확인됨.
- causal mask 유무 비교(Table 4)에서 mask 없이는 10 step이 필요(EPDMS 88.2, 2 step은 87.3)한 반면, mask 있으면 2 step만으로 91.0을 얻고 latency도 848.0ms→341.6ms로 절반 이하로 줄임.
- nuScenes zero-shot transfer는 평균 L2 0.89m, collision rate 0.16%로 zero-shot baseline(PWM, DriveVLA-W0) 대비 우수하나, 저자 스스로 이 metric이 ego-status shortcut에 민감하다고 명시해 sanity check 수준으로 취급함. 더 어려운 navhard split에서는 36.1 EPDMS로 RAP(39.6)에 뒤짐. real-robot 검증은 없고 시뮬레이션·pseudo-simulation 벤치마크에 한정됨.

**Top-tier conference 적합성 — 62/100 · 추천 venue: CVPR**

NAVSIMv2 전 항목에서 SOTA를 달성하고 causal mask·DAC regularizer·view 수에 대한 ablation을 꼼꼼히 검증해 실험적 설득력이 강함. 다만 핵심 아이디어(video supervision-only training, action-only inference)가 Fast-WAM·GigaWorld-Policy에서 이미 제시된 원리를 driving 도메인에 옮긴 것이라 conceptual novelty는 제한적이고, 더 어려운 navhard split에서 RAP에 뒤지는 점이 rejection risk로 작용할 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- world model을 학습 시에만 쓰고 추론에서는 action-only로 도는 구조는 누리랩의 test-time optimization/efficient inference 연구에 참고할 수 있음. failure detection·recovery에서도 future prediction은 학습 신호로만 쓰고 실행 경로는 가볍게 두는 전략을 검토할 만함.
- action-centered causal mask는 world model branch를 co-train하되 배포 시 잘라내는 general한 recipe로 볼 수 있어, manipulation VLA에 이식해볼 수 있음.
- 미분 가능한 evaluation-metric regularizer(drivable-area penalty를 gradient가 흐르는 PyTorch rollout으로 재구현)라는 접근은 manipulation의 workspace-boundary·collision-avoidance regularizer로 변형해 적용할 여지가 있음.

---

### 9. [60점] Latent Energy Action Planning with World Models

- **분야**: World Model / Test-Time Planning · **robotics relevance**: 8/10
- **arXiv**: [2609.03294](https://arxiv.org/abs/2609.03294) ([PDF](https://arxiv.org/pdf/2609.03294))
- **저자**: Phu Pham, Aniket Bera
- **카테고리**: Machine Learning (cs.LG) · 신규 목록 게재: cs.LG
- **Comments**: 9 pages, 5 figures, 8 tables
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 LEAP는 frozen LeWorldModel(LeWM) 위에서 action horizon 전체를 미분 가능한 변수로 두고 L-BFGS로 직접 최적화하는 test-time planner임. latent goal cost에 decoder가 예측한 terminal state 오차를 더해 latent 목적함수만 최적화할 때 생기는 objective mismatch를 억제해 4개 도메인 평균 성공률을 CEM 대비 77.5%에서 94.8%로 올림.

**Core innovation & methodology**

- action horizon을 통째로 미분 가능한 변수로 취급해 frozen LeWM의 autoregressive rollout을 통해 L-BFGS로 직접 backprop하는 gradient 기반 planner를 제안함. CEM 같은 sampling 기반 black-box 최적화를 대체함.
- terminal latent cost(LeWM 고유 목적함수)에 frozen decoder D_psi가 예측한 terminal descriptor와 goal descriptor 간 오차인 terminal-window energy(L=2, lambda_s=10)를 더한 결합 energy를 씀. latent상 goal과 가까워 보이지만 decode한 state는 goal과 다른 action sequence를 걸러냄.
- frozen goal-conditioned proposal MLP로 탐색 시작점을 잡고, L-BFGS 최적화 후 post-optimization projection으로 action을 admissible range에 clamp함. world model 표현·predictor는 재학습하지 않음.
- Push-T 2D action slice 시각화로 latent-only cost가 decoder 기준으로는 틀린 off-center basin을 만든다는 것을 보이고, terminal energy가 이 basin을 없애 정답 방향으로 descent를 바꾼다는 것을 정성적으로 확인함.

**Novelty vs. prior works**

- gradient 기반 trajectory optimization 자체는 Differentiable MPC(Amos et al.)나 learned model을 통한 planning에서 이미 쓰이던 방식이라 sampling에서 gradient로 planner를 바꾼 것 자체의 novelty는 제한적임.
- 본질적 기여는 latent 목적함수 단독 최적화가 offline data 분포 밖 action을 선호할 수 있다는 문제를 decoder 기반 보조 energy로 보정한 것임. test-time에서 latent objective hacking을 막는 정규화 기법에 가까움.
- 가장 가까운 prior work인 LeWM+CEM·DINO-WM 대비 world model·표현은 그대로 두고 planner만 바꿨다는 점은 실용적이지만, decoder가 시뮬레이터 state descriptor로 학습돼 있어 실제로는 privileged information에 의존하는 구조임(논문도 한계로 인정).

**Benchmark results**

- 100-trial 프로토콜에서 LEAP 평균 성공률 94.8%, LeWM+CEM 77.5% (Push-T 90.0 vs 88.0, OGBench-Cube 100.0 vs 62.0, Reacher 89.0 vs 75.0, TwoRooms 100.0 vs 85.0), 17.3%p 개선.
- planning time은 trial당 1.28s로 CEM(1.20s) 대비 0.08s만 증가하고, 성공까지 걸리는 평균 step 수는 21.06으로 CEM의 26.41보다 적음.
- energy ablation(50-trial)에서 latent-only 91.0%, terminal-state-only 52.0%, 결합 시 96.5%로 두 항이 상보적임을 보임. terminal-state 단독으로는 성능이 크게 떨어져 latent goal 항이 필수임.
- damping energy(terminal descriptor 변화 억제)를 terminal-state 항과 결합하면 96.5%에서 94.0%로 오히려 떨어져 두 보조 항이 비가산적임을 확인함.
- PLDM, DINO-WM, Random 결과는 LeWM 원 논문에서 재인용한 값으로 저자가 직접 재현하지 않았고, 4개 도메인 모두 simulation 환경이며 real-robot 검증은 없음.

**Top-tier conference 적합성 — 58/100 · 추천 venue: ICRA**

LeWM checkpoint를 고정한 채 controlled한 4-domain 비교와 energy·damping·optimizer 등 다수 ablation으로 test-time latent objective mismatch 문제를 명확히 짚고 일관된 개선을 보임. 하지만 gradient 기반 trajectory optimization과 auxiliary energy 결합 자체는 기존 기법의 조합에 가깝고, 4개 도메인 모두 sim이며 decoder가 privileged state descriptor에 의존해 real-robot 적용에는 추가 작업이 필요함. 저자 2인·9쪽 분량의 짧은 기고로 top-tier 학회 highlight급 임팩트보다는 ICRA/IROS 수준의 견고한 systems 논문에 가까움.

**추천 이유 & 누리랩 연구와의 연결점**

- terminal energy로 latent objective만으로는 못 잡는 실패(목표 미도달인데 latent cost는 낮은 경우)를 planning 단계에서 걸러내는 아이디어는 누리랩의 failure detection/recovery, test-time optimization 주제와 직접 연결됨.
- decoder 기반 terminal descriptor 대신 object-centric 3DGS나 scene graph 기반 geometry-aware descriptor를 goal 표현으로 쓰면(논문이 스스로 future work로 제안) privileged state 의존을 줄이면서 real-robot에 적용 가능한 확장이 될 수 있음.
- world model은 그대로 두고 test-time에서 planner objective만 바꿔 성능을 크게 올린 사례라, 우리 VLA·world model 파이프라인에서도 frozen policy 위에 test-time energy를 추가하는 방식을 재현성 있게 시도해볼 만함.

---

### 10. [60점] VeriPhy: Agentic Physical Reasoning for World Model Evaluation and Refinement

- **분야**: World Model Evaluation / Video Generation Physical Verification · **robotics relevance**: 6/10
- **arXiv**: [2609.03153](https://arxiv.org/abs/2609.03153) ([PDF](https://arxiv.org/pdf/2609.03153))
- **저자**: Wenzhuo Xu, Yuchen Zhu, Chongjian Ge, Xuan Shen, Jing Shi, Jason Kuen, Yongxin Chen, Molei Tao 외 3명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 65점

> 💡 VeriPhy는 생성 비디오의 물리적 타당성을 프롬프트에서 뽑은 typed physical obligation을 SAM 3·TAPNext++·depth·OCR·오디오 검출 같은 specialist tool로 검증하는 프레임워크임. 149-clip 코어에서 304개 flaw 중 228개를 찾아내 question-decomposition baseline(164개)보다는 낫지만, 동일 backbone에 단순히 monolithic하게 물어본 baseline(222개)과는 recall이 거의 같아 저자도 recall만으로는 시스템 구조의 이득을 입증하지 못한다고 명시함.

**Core innovation & methodology**

- 텍스트만 보고 프롬프트를 검증 가능한 claim과 typed 실행 계획으로 컴파일하는 단계를 프레임 관찰 이전에 분리함. 계획은 Parse/Refs/Typed/Acyclic 조건으로 정적 검증됨
- 실행 단계에서 관찰은 이미 선언된 노드를 활성화·스킵·구간 지정(gate/scope)할 뿐, 새 tool 호출을 즉흥적으로 만들지 않음
- SAM 3 tracking 위에서 변위·접촉·형태변화·경로모양 등 11개 typed physical measurement를 정의하고, 각 evidence record를 measured/abstained/errored 세 상태로 분리해 track 실패와 진짜 음성 측정을 구분함
- 고정된 deterministic composition rule로 claim별 supported/contradicted/unknown 상태를 clip 단위 plausible/implausible/abstain로 롤업하며, contradicted claim은 근거 evidence와 시공간 위치를 담은 별도 packet으로 남김
- 별도로 MuJoCo 시뮬레이션에서 검증된 궤적을 depth control로 렌더링해 frozen Wan 2.2-VACE를 조건화하는 physics-guided generation testbed도 제시함(critic과는 분리 평가)

**Novelty vs. prior works**

- 가장 가까운 prior work인 AV-Phys Agent는 reasoning-action loop와 결정적 오디오 tool을 쓰지만 prompt별 사람이 작성한 rubric과 binary VLM 판정에 의존함. VeriPhy는 rubric 없이 오픈 프롬프트에서 typed obligation을 자동 컴파일하고 evidence record에 provenance를 남긴다는 점이 구조적 차이임
- plan-before-act(ReWOO)와 code-as-plan(ViperGPT) 계열 아이디어를 물리 검증 도메인에 조합한 통합 시스템 논문에 가깝고, 개별 구성요소(정적 계획 검증, 증거 기반 composition, tool harness) 자체는 기존 agent 문헌에서 이미 제시된 것들임
- 저자 스스로 recall만으로는 agentic 구조의 가치를 입증하지 못한다고 밝힘(228 vs 동일 backbone monolithic prompting 222). novelty의 실질 증거는 auditability·provenance이지 성능 향상이 아님

**Benchmark results**

- 1,500개 생성 clip에 사람이 작성한 flaw record 2,582개를 모은 벤치마크를 구축했고, 이 중 clip/flaw selection을 거쳐 150-clip 코어(306 flaw)를 층화추출함
- 실측 대상은 149 clip·304 flaw(1개 clip은 측정 실패로 제외): VeriPhy 228개, published question-decomposition evaluator 164개, 동일 backbone monolithic prompting 222개를 recall함
- 코어는 development/optimization set이라고 저자가 명시함. single-annotator이고 held-out이 아니어서 이 수치는 일반화가 아니라 시스템 특성만 보여줌
- physics-guided generation testbed(MuJoCo depth control + Wan 2.2-VACE)의 정량 결과, self-evolution(context-training) ablation, closed-loop refinement 실험은 본문 텍스트가 중간에서 잘려 확인 불가
- closed-loop refinement(critic verdict를 생성으로 되먹임)는 이번 리포트에서 실제로 돌리지 않았다고 명시함. 인터페이스만 정의했을 뿐 어떤 clip도 실제로 개선시켰다는 주장은 하지 않음

**Top-tier conference 적합성 — 55/100 · 추천 venue: CVPR (또는 NeurIPS Datasets & Benchmarks Track)**

1,500 clip·2,582 flaw 규모의 human-annotated 물리 실패 벤치마크와 provenance를 남기는 evidence 체계는 엔지니어링 완성도가 높고 벤치마크·시스템 논문으로서 설득력이 있음. 다만 핵심 recall이 단순 monolithic prompting과 거의 차이가 없고(228 vs 222), 평가가 single-annotator·비held-out dev set에 국한되며, 제목이 내세우는 'refinement'는 실제로 실행되지 않은 인터페이스 제안에 그쳐 rejection risk로 지적될 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- evidence record를 measured/abstained/errored로 분리하고 provenance를 남기는 구조는 누리랩의 failure detection/diagnosis 연구에서 로봇 실패 원인을 tool 단위로 추적하는 로그 설계에 참고할 만함
- 이 논문이 미실행으로 남긴 closed-loop refinement(critic verdict를 world model 재생성에 되먹이는 것)는 누리랩의 test-time optimization 주제와 정확히 맞닿는 research gap이며, VLA policy나 world model rollout에 VeriPhy식 typed evidence를 실제로 되먹여 개선하는 실험으로 확장 가능함
- claim-bound evidence record를 관찰된 증거(measured)와 추론된 상태(learned base state)로 분리하는 설계는 robot memory에서 관측 evidence와 파생 belief를 분리 저장하는 구조와 원리가 같아 학생 연구에 바로 적용 가능함

---

### 11. [60점] Continuous Actions from Discrete Minds: Latent-Aligned Planning for End-to-End Autonomous Driving

- **분야**: VLA (Autonomous Driving) · **robotics relevance**: 7/10
- **arXiv**: [2609.04070](https://arxiv.org/abs/2609.04070) ([PDF](https://arxiv.org/pdf/2609.04070))
- **저자**: Ruoyu Yao, Yusen Xie, Qingzhao Liu, Pei Liu, Zewei Yang, Yipeng Zhu, Xiaolong Wang, Jun Ma
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: 8 pages, 5 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 LaPla는 자율주행 VLA에서 discrete action token 대신 사전학습해 frozen시킨 residual VQ-VAE decoder에 continuous latent를 직접 투영해 궤적을 생성하는 프레임워크임. nuScenes open-loop에서 장기 구간 L2를 최대 15.52% 낮추고 AlpaSim closed-loop 성공률을 33.34%p 높이면서 추론 속도도 약 3배 개선함.

**Core innovation & methodology**

- Residual VQ-VAE(4-layer, codebook 64/64/128/128)를 궤적 데이터로 먼저 학습해 decoder를 frozen하고, kinematic prior로 재사용함으로써 action 표현 학습과 policy 학습을 분리함
- VLA(Emu3-8B + LoRA)는 discrete codebook lookup 대신 action query의 hidden state를 frozen decoder의 continuous latent 공간에 직접 projection함(quantization error 제거)
- 과거 action은 discrete residual quantization으로 압축하고 미래 action은 continuous latent로 예측하는 비대칭 표현을 사용함 — 과거는 semantic context 요약, 미래는 고정밀 실행에 최적화함
- 학습된 basis vector로 latent를 perturb해 N=20개의 다양한 trajectory candidate를 만들고 Best-of-N smooth L1 loss로 학습함(inference시엔 perturbation 없이 deterministic 실행)

**Novelty vs. prior works**

- 가장 가까운 latent-space planning 계열(LAP, Last-VLA, DriveWorldVLA)은 latent space를 VLA와 co-learning하는데, LaPla는 latent prior를 먼저 고정 학습한 뒤 policy만 학습한다는 점이 본질적 차이임
- action tokenization 계열(AutoVLA, OpenDriveVLA)의 discrete lookup을 continuous projection으로 바꾼 것은 quantization error 감소로 이어지는 명확한 개선이지만, pretrained decoder를 frozen한 채 continuous embedding을 회귀하는 구조 자체는 새로운 representation이라기보다 기존 codec 설계 패턴의 재조합에 가까움
- 자율주행 domain 특화 실험만 존재해 다른 embodiment로의 일반화는 검증되지 않았고, novelty는 architecture 조합 수준으로 제한적임

**Benchmark results**

- nuScenes open-loop, UniAD 기준 평균 L2 0.60m로 OpenDriveVLA-7B(0.66m), AutoVLA w/CoT(0.70m) 대비 개선되나 1초 구간 L2(0.35m)는 OpenDriveVLA(0.19~0.20m)보다 나빠 장기 구간(3s: 0.98m vs AutoVLA 1.16m)에서만 우위를 보임
- ST-P3 collision rate 평균 0.30%로 VAD(0.14%)·OpenDriveVLA(0.10%)보다 높아 L2 개선이 안전성 지표 개선으로 이어지지 않음
- AlpaSim closed-loop(60개 시나리오)에서 success rate 61.67%로 AutoVLA action-only(28.33%)·w/CoT(15.00%) 대비 크게 개선되고 route completion도 71.67%로 우수함
- 다만 fault collision은 11.67%로 AutoVLA(1.67~5.00%)보다 높은데, 저자는 더 적극적인 주행 때문이라 설명하나 별도 검증은 없음. inference 속도는 1.582 FPS로 AutoVLA(0.532 FPS) 대비 약 3배 빠르나 real vehicle 검증은 없음
- ablation(M1→M3)에서 latent action과 frozen decoder를 순차 추가할 때 UniAD 평균 L2가 1.81m→1.13m→0.60m로 감소해 두 요소 모두 기여함을 확인했고, VQA 제거시(M3') L2가 0.60m→0.63m로 소폭 악화됨

**Top-tier conference 적합성 — 52/100 · 추천 venue: ICRA / IEEE RA-L**

문제의식이 명확하고 open-loop·closed-loop 양쪽 검증과 ablation이 탄탄해 domain venue 수준의 완성도는 갖춤. 다만 novelty가 기존 요소(residual VQ-VAE, frozen decoder, BoN sampling)의 재조합에 가깝고 closed-loop 평가가 시나리오 60개·충돌률 악화 트레이드오프를 안고 있어 CVPR/NeurIPS급 top-tier oral보다는 ICRA/RA-L 수준이 적합함.

**추천 이유 & 누리랩 연구와의 연결점**

- frozen decoder로 continuous latent를 예측해 policy를 학습하는 구조는 manipulation VLA의 action tokenizer 설계(FAST 등)에도 참고할 수 있음 — quantization error 완화 아이디어를 action representation 연구에 이식할 여지가 있음
- collision rate가 L2 개선과 반대로 움직인 결과는 failure detection/recovery 연구에서 정확도 지표와 안전성 지표가 괴리될 수 있음을 보여주는 사례로 참고할 만함
- 과거는 discrete, 미래는 continuous로 나눈 비대칭 표현은 robot memory(과거 압축)와 test-time execution(고정밀 실행)을 분리하는 아이디어로 manipulation policy에도 이식해볼 만함

---

### 12. [60점] GPU-Accelerated Astrodynamics World Models for Spacecraft Rendezvous and Proximity Operations

- **분야**: World Model / Space Robotics · **robotics relevance**: 8/10
- **arXiv**: [2609.03067](https://arxiv.org/abs/2609.03067) ([PDF](https://arxiv.org/pdf/2609.03067))
- **저자**: Duncan Eddy, Isaac R. Ward, Grace Ra Kim, Mykel J. Kochenderfer
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 20 pages, 12 figures, 5 tables, Presented at Advanced Maui Optical and Space Surveillance Technologies Conference 2026
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 우주선 랑데부·도킹 문제에 world model을 처음 적용한 논문임. transformer 기반 world model(OWM)이 카메라 영상과 상태 측정치를 공유 latent로 인코딩하고 flow matching으로 다음 상태를 예측하며, 이를 MPPI 플래닝에 결합해 ISS 도킹 성공률을 RL baseline 대비 29%에서 53%로 끌어올림.

**Core innovation & methodology**

- 상태(kinematic vector)와 카메라 영상을 공유 latent에 인코딩하고 space-time factorized transformer로 결합해 one-step flow matching(rectified flow)으로 다음 latent 분포를 예측하는 Out-of-this-World-Model(OWM) 아키텍처를 제안함.
- reward를 전혀 쓰지 않는 순수 world model 학습이며, MPPI로 latent 공간에서 128개 candidate를 배치 롤아웃해 계획하는 test-time planning 구조임.
- JAX 기반 GPU-parallel 우주역학 시뮬레이터 AstroJAX와 ISS 도킹 환경을 함께 오픈소스로 공개, 8개 포트·3개 행동 정책(random/orbit/dock)으로 50만 transition 학습 데이터를 생성함.
- world model의 예측 불확실성(in-distribution score)을 도킹 접근 중 학습되지 않은 이상 물체 탐지에 그대로 활용함.

**Novelty vs. prior works**

- 가장 가까운 prior work는 같은 저자 그룹의 Ward et al.(ICRA 2026, bimanual manipulation failure detection)로, world model 불확실성을 이상 탐지에 쓰는 아이디어를 그대로 재사용하고 도메인만 우주로 옮긴 것에 가까움.
- 아키텍처도 Dreamer 계열 posterior-correction 구조와 flow matching/JEPA 계열 요소를 조합한 수준이라 새로운 representation이나 learning paradigm 제시는 아님.
- 우주 RPO 도메인에 world model을 처음 적용했다는 점과 GPU-parallel 우주역학 시뮬레이터 오픈소스화는 실용적 기여이나, 방법론적 novelty는 제한적임.

**Benchmark results**

- ISS 도킹 8개 포트 종합 성공률에서 world model+MPPI 53% vs PPO baseline 29%(상대 84% 개선), 전량 JAX 시뮬레이션 환경에서 측정된 결과로 real-robot 검증은 없음.
- 훈련에서 제외된 held-out 3개 포트 일반화 성능은 40% vs 17%로 격차가 더 벌어졌고, world model은 baseline이 아예 도달하지 못하는 포트에도 도킹함.
- 이상 탐지는 이상 물체 포함 20회 + 정상 25회, 총 45개 approach만으로 98% 분류 정확도를 산출해 표본 수가 작음.
- PPO baseline은 원래 20Hz 환경에서 학습이 되지 않아 control step을 1Hz로 낮추고 keep-out 제약을 soft로 완화하는 등 큰 폭의 조정을 거친 뒤에야 비교 가능한 수준에 도달했음. 저자가 직접 재구성한 baseline이라는 한계가 있음.
- state/image reconstruction의 MSE·PSNR 등 예측 품질 세부 수치는 본문 결과 섹션 중간이 텍스트 추출에서 누락되어 확인 불가.

**Top-tier conference 적합성 — 45/100 · 추천 venue: ICRA**

GPU-parallel 우주역학 시뮬레이터와 world model 기반 도킹 파이프라인을 오픈소스로 공개한 시스템 기여는 강점이고 실험 설계와 서술이 깔끔함. 다만 아키텍처는 기존 world model 구성요소의 조합이라 novelty가 제한적이고, sim-only 검증에 저자가 직접 튜닝·완화한 PPO baseline과의 비교라는 점에서 rejection risk 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- world model 예측 불확실성을 이상 탐지·실패 판정에 쓰는 파이프라인은 failure detection/recovery 연구와 직접 연결됨, 같은 저자의 bimanual manipulation 논문(Ward et al., ICRA 2026)과 비교해 manipulation task에 이식 가능한지 검토할 만함.
- flow matching 기반 one-step latent dynamics와 MPPI를 결합한 test-time planning 구조는 inference-time optimization 트랙에 참고할 만한 경량 설계임.
- 상태 벡터와 이미지를 공유 latent로 fusion하는 space-time factorized transformer 설계는 object-centric 3DGS·scene graph 표현과 결합한 manipulation world model 설계에 참고 가능함.

---

### 13. [58점] FWBC-VLA: Force-Aware Whole-Body Compensation for Contact-Rich Loco-Manipulation

- **분야**: VLA / Loco-manipulation (Force-aware control) · **robotics relevance**: 8/10
- **arXiv**: [2609.03889](https://arxiv.org/abs/2609.03889) ([PDF](https://arxiv.org/pdf/2609.03889))
- **저자**: Yutian Zhang, Siyuan Ma, Liwen Yang, Yang Li, Ce Hao, Haozhen Chi, Dong We, Qiaojun Yu 외 1명
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 9 pages, 6 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 66점

> 💡 휠드-레그드 사족 로봇의 접촉이 많은 loco-manipulation을 위해 F/T 센서 없이 관절 잔차 토크로 접촉력을 추정하고, 이를 VLA action expert와 whole-body 보정기에 동시에 주입하는 FWBC-VLA를 제안함. 화이트보드 닦기·도어 오프닝 실로봇 실험에서 force 사용 baseline인 ForceVLA 대비 최대 40%p 높은 성공률을 보임.

**Core innovation & methodology**

- HSR-Force: history expert(과거 토크·모션 이력)와 state expert(현재 팔·다리·베이스·IMU 상태) 두 LSTM 기반 추정기를 고정 게이트로 결합해 자유운동 토크를 예측하고, 측정 토크와의 잔차로 외력을 추정함(F/T 센서 불필요).
- 잔차 토크를 접촉 강도와 변화율 2채널 descriptor로 요약하고 GRU로 인코딩해 force token을 생성, π0.5 action expert 내부에서 cross-attention으로 action hidden state에 late fusion함.
- 같은 잔차를 Jacobian으로 EE·body frame wrench로 변환하고 IMU 자세 편차·nominal base action과 함께 MLP에 넣어 bounded base velocity/yaw rate 보정을 생성, WBC로 전달하는 이중 피드백 경로를 구성함.
- 5,000 episode 규모의 WL&Arm teleoperation 데이터셋(Pico 기반 position-force 하이브리드 조작)을 구축함. force-intent는 메타데이터로만 기록하고 추정기·정책 입력에는 쓰지 않아 command-intent leakage를 막음.

**Novelty vs. prior works**

- 가장 가까운 prior work인 ForceVLA·ACP·TA-VLA는 F/T 센서 기반이고 팔 중심으로 force를 반영할 뿐 body-level 영향은 다루지 않음. 센서리스 추정과 VLA 조건화, WBC 보정을 하나의 파이프라인으로 묶은 점이 이 논문의 차별점임.
- 센서리스 외력 추정 자체(NEXT, GMO-SI 등)는 기존 arm 로봇 연구에서 이미 다뤄진 문제이고, HSR-Force는 dual-LSTM과 고정 게이트를 결합한 아키텍처 엔지니어링에 가까움. 새로운 학습 패러다임이나 이론적 기여는 없음.
- whole-body compensation generator도 residual velocity를 L1 회귀로 예측하는 표준적 MLP 설계라 novelty가 제한적임. 핵심 기여는 새 embodiment(휠드-레그드 사족+암)에 이 조합을 처음 적용하고 대규모 teleoperation 데이터셋을 구축한 것에 가까움.

**Benchmark results**

- 화이트보드 닦기 최종 성공률(S5, 25 trial)은 FWBC-VLA 64%, force 미사용 최고 baseline OpenPI 0.5는 12%, force 사용 baseline 중 최고 ForceVLA는 24%로 +40%p 차이임.
- 도어 오프닝 최종 성공률(S5)은 FWBC-VLA 52%, ForceVLA 12%로 +40%p임. 실제 F/T 센서를 쓰는 FWBC-GT(60%, 48%)와 비교해도 근접하거나 오히려 앞섬.
- 힘 추정 정확도(Table 1)에서 HSR-Force force MAE는 0.15N으로 NEXT(0.28N)·GMO-SI(0.43N)·DF-MLP(0.21N)보다 낮고 Touch AUC도 0.97로 가장 높음.
- component ablation(Table 3)에서 force-aware interface(FI) 추가만으로 평균 성공률이 12.0%에서 35.0%로 오르고, whole-body compensation(BC) 추가로 표 기준 65%까지 상승함. 단, 본문 텍스트는 BC 추가 후 평균을 59.5%로 서술해 표 수치(65%)와 불일치함.
- 실험은 DeepRobotics M20S 단일 플랫폼, task 2종(wiping·door)에 task당 25 trial로 real-robot 검증이지만 규모가 작고, baseline 전부를 저자 팀 데이터셋으로 재학습시켰다는 점에서 공정성 검증이 제한적임.

**Top-tier conference 적합성 — 52/100 · 추천 venue: CoRL 또는 ICRA**

실로봇 검증과 센서리스 force 추정이라는 실용적 강점이 있어 CoRL 또는 ICRA 수준은 시도해볼 만함. 다만 아키텍처 대부분이 기존 기법(LSTM 잔차 추정, cross-attention fusion, residual MLP 보정)의 조합이라 conceptual novelty가 약하고, task 2종·단일 플랫폼이라는 작은 실험 규모와 본문-표 수치 불일치가 rejection risk로 작용할 수 있음.

**추천 이유 & 누리랩 연구와의 연결점**

- 센서리스 접촉 추정을 VLA에 조건화하는 방식은 failure detection·recovery 연구에서 이상 접촉력 패턴을 감지해 정책 개입을 트리거하는 아이디어로 재사용 가능함.
- HSR-Force의 history/state dual-expert 구조는 robot memory 관점에서 최근 상호작용 이력을 압축해 정책에 주입하는 설계 참고 사례가 됨.
- task policy와 whole-body 보정 policy를 분리한 이중 경로 설계는 manipulation·active perception 과제에서 test-time optimization 기반 안정화 보정 아이디어에 참고할 만함.

---

### 14. [57점] MINERVA: How Small Can a Manipulation Policy Be and Still Solve LIBERO?

- **분야**: Manipulation (VLA capacity/efficiency analysis) · **robotics relevance**: 8/10
- **arXiv**: [2609.03715](https://arxiv.org/abs/2609.03715) ([PDF](https://arxiv.org/pdf/2609.03715))
- **저자**: Kohei Sendai, Tatsuya Matsushima, Yusuke Iwasawa
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 LIBERO manipulation benchmark를 language encoder 없이 40-way task-ID embedding만으로 풀 수 있는 최소 파라미터 수(capacity floor)를 측정한 논문임. 0.54M 파라미터 policy가 4.1B 파라미터 π0.5 대비 2.4점 낮은 95.1% 성공률을 내면서, 표준 LIBERO 평가가 사실상 task memorization을 측정한다는 것을 정량적으로 보임.

**Core innovation & methodology**

- 언어 pathway를 40개 task-ID embedding으로 교체하고 from-scratch CNN과 flow-matching(또는 L1) action head만 남긴 MINERVA policy family로 LIBERO의 empirical capacity floor를 측정함
- 9.7M부터 0.09M까지 파라미터를 줄이며 architecture·objective·inference 전 영역을 sweep, 0.54M에서 성능이 정점 근처이고 0.25M 이하서 급격히 붕괴함을 확인함
- 핵심 ablation 5개를 3-seed로 재학습해 4-suite 평균에 ±1점의 training-seed 변동 폭이 있음을 정량화하고, 이 폭을 넘는 요인은 action-chunk length와 vision allocation뿐임을 보임
- task-ID mapping만 재배열하는 permutation probe로 conditioning의 인과적 역할을 검증함(성공률 96.75%에서 6.5%로 붕괴)

**Novelty vs. prior works**

- TinyVLA·MiniVLA·SmolVLA·TurboVLA 등 기존 efficient VLA는 language pathway와 pretrained backbone을 유지한 채 크기만 줄였으나, 이 논문은 language encoder 자체를 제거하고 벤치마크가 요구하는 최소 capacity를 측정하는 것이 목적이라 문제의식이 다름
- architecture 자체는 ACT의 chunking·temporal ensembling, Diffusion Policy의 generative head, DiT/MLP-Mixer 조합으로 구성되어 새 representation은 없음
- LIBERO-PRO가 지적한 memorization 문제를 재확인·정량화한 audit 성격이 강해 novelty는 제한적이고, 기여는 새 방법론보다 측정 결과 자체에 있음

**Benchmark results**

- 표준 LIBERO 4-suite(2,000 rollout)에서 0.54M 파라미터가 95.05%(L1 head 사용 시 95.75%)를 기록, LeRobot π0.5(4.1B, 참고용 10 episode/task 결과) 대비 2.4점 낮으면서 약 7,600배 작음
- 1M 근처서 성능이 saturate하고 0.25M 이하서 붕괴함(0.24M 88.6%, 0.09M 68.3%), 붕괴는 long-horizon suite에서 먼저 발생함
- 3-seed ablation에서 ±1점 seed band를 넘는 요인은 action-chunk length(16→8: -3.16점, 16→32: -2.20점)와 vision allocation(-1.41점)뿐이고, flow matching과 L1 regression 차이는 +0.34점으로 band 안에 있으며 regression이 GPU서 최대 3.8배 빠름
- LIBERO-90(89 task, 0.995M, single seed)에서 94.6% 유지하지만, LIBERO-Plus perturbation에서는 46.7%(0.54M)/55.7%(4.89M)로 급락하고 photometric shift에는 스케일과 무관하게 거의 0%에 수렴함
- 0.54M 모델은 laptop CPU서 chunk당 5-9ms로 SmolVLA 대비 113배, π0.5 대비 1,400배 빠르지만 real-robot 검증은 없고 sim 단일 evaluation seed에 의존함

**Top-tier conference 적합성 — 62/100 · 추천 venue: RSS**

2,000 rollout 평가, 3-seed 재현성 검증, permutation probe, LIBERO-Plus audit까지 갖춰 실험적 엄밀함은 RSS·CoRL 수준임. 다만 새로운 method나 representation 없이 기존 벤치마크의 memorization 특성을 계량화한 analysis 논문이라 oral·highlight보다는 accept 또는 poster급 가능성이 높고, 단일 시뮬레이터·단일 renderer seed 의존이 rejection risk임.

**추천 이유 & 누리랩 연구와의 연결점**

- LIBERO 같은 benchmark의 memorization 특성을 밝힌 permutation probe 방법론은 실로봇 policy의 failure detection에서 policy가 실제로 무엇에 conditioning되어 성공하는지 진단하는 도구로 참고 가능함
- capacity floor 측정 프레임은 test-time optimization·distillation 연구에서 배포용 policy 크기를 정량적으로 정하는 기준으로 활용 가능함
- photometric robustness가 scale과 무관하게 0%에 수렴한다는 결과는 world model 기반 augmentation이나 counterfactual reasoning으로 보완할 연구 gap을 시사함

---

### 15. [40점] Toward Physically Grounded JEPA World Models for Goal-Conditioned Robotic Planning

- **분야**: World Model · **robotics relevance**: 9/10
- **arXiv**: [2609.03565](https://arxiv.org/abs/2609.03565) ([PDF](https://arxiv.org/pdf/2609.03565))
- **저자**: Muyuan Liu, Yue Huang, Zheng Liang, Xiang Gao
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: 5 pages, 4 figures, 2 tables. Accepted to the IROS 2026 Workshop on Physical World Models for Scaling Embodied AI (PWMS 2026)
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 action-conditioned JEPA world model에 inverse dynamics(IDM)와 물리적 state-alignment(SA) 보조 손실을 함께 붙여 latent representation이 로봇 제어에 필요한 정보를 유지하도록 학습함. TwoRoom·PushT·OGBench-Cube 3개 벤치마크에서 baseline LeWorldModel 대비 planning 성공률을 높였고 Reacher에서는 baseline과 비슷한 수준을 보였으며, straightening이 높아도 transition 차원이 낮으면 오히려 성능이 떨어질 수 있다는 분석을 제시함.

**Core innovation & methodology**

- end-to-end JEPA world model에 inverse-dynamics 헤드 H와 state-alignment 헤드 G를 동시에 붙여 latent collapse를 막고 물리적 state 정보를 남기게 함
- SA 헤드는 연속된 두 latent 표현 z_{t-1}, z_t를 이어붙여 측정된 physical state s_t(위치·속도 등)를 회귀하는 방식으로 학습 시에만 supervision을 제공함
- 배포 시에는 encoder E와 predictor F만으로 CEM 기반 latent-space model-predictive planning을 수행하고 SA·IDM 헤드는 사용하지 않음
- straightening score와 SVD 기반 transition-subspace 분석(r95)을 함께 써서 LeWorldModel의 높은 straightening이 낮은 effective transition dimension과 짝을 이룸을 보임

**Novelty vs. prior works**

- 가장 가까운 baseline인 LeWorldModel은 SIGReg로 latent 분포의 collapse만 막는 반면, 이 논문은 물리적 state 회귀 항을 추가해 무엇을 latent에 남길지 명시적으로 지정함
- PLDM도 IDM을 포함한 복합 정규화를 쓰고 SMWM·Delta-JEPA도 action-recovery 계열이라, SA 항 하나를 얹은 수준이라 formulation 자체의 새로움은 제한적임
- SA가 ground-truth physical state를 학습에 요구한다는 점에서 완전한 label-free self-supervised world model은 아니며, 이 의존성이 실험 한계로 명시되지 않음

**Benchmark results**

- TwoRoom 100%, PushT 98%, OGBench-Cube 87%로 DINO-WM·PLDM·LeWorldModel 대비 최고 성공률을 기록했고, Reacher는 85%로 LeWorldModel 86%와 비슷함
- IDM-only ablation 대비 SA 추가가 4개 태스크 전부에서 성공률을 높임 (Reacher 63→85%, TwoRoom 94→100%, PushT 83→98%, OGBench-Cube 85→87%)
- OGBench-Cube에서 LeWorldModel의 straightening score(0.69)가 SA+IDM(0.55)보다 높지만, transition-subspace r95는 LeWorldModel 17.0 대 SA+IDM 32.8로 SA+IDM이 더 넓은 유효 차원을 씀
- 평가는 시뮬레이션 4개 태스크(50개 고정 start-goal, 3 seed 평균)에 한정되며 real-robot 검증은 없음
- 벤치마크·평가 프로토콜을 LeWorldModel 논문에서 그대로 가져왔고 ViT-Tiny 백본을 쓰는 소규모 세팅임

**Top-tier conference 적합성 — 28/100 · 추천 venue: CoRL**

IDM 단독 대비 SA 추가 효과를 4개 태스크에서 일관되게 보인 ablation과, straightening 대 transition-subspace 분석으로 기존 지표의 한계를 짚은 점은 흥미로움. 다만 5페이지 workshop 논문(IROS 2026 PWMS 게재본)이고 4개의 소규모 시뮬레이션 태스크에 그쳐 real-robot 검증과 스케일이 부족해 main-track rejection risk가 높음.

**추천 이유 & 누리랩 연구와의 연결점**

- world model의 latent representation이 무엇을 보존해야 하는가라는 문제는 failure detection·recovery용 world model 설계에서 실패로 이어지는 물리적 변화를 latent에 남기는 방향으로 참고 가능함
- SVD 기반 transition-subspace 분석(r95)은 test-time optimization에서 latent world model의 표현력을 진단하는 도구로 재사용할 수 있음
- SA가 ground-truth state에 의존하는 한계는 실로봇에서 state 라벨 대신 object-centric 3DGS 표현이나 다른 self-supervised proxy로 대체하는 후속 연구 방향으로 이어질 수 있음

---

## 오늘의 핵심 연구 트렌드 종합

- **World model이 VLA의 학습·추론 양쪽에 표준 부품으로 들어옴** — [WISE](https://arxiv.org/abs/2609.03681)는 world model imagination을 post-training reward로, [Latent Energy Action Planning](https://arxiv.org/abs/2609.03294)은 frozen world model 위 test-time planner로 씀. [SV-WAM](https://arxiv.org/abs/2609.03602)은 world model을 학습 신호로만 쓰고 추론에선 제거함. world model 하나를 어디에 꽂느냐만 다를 뿐 목적은 전부 policy 개선으로 수렴함.
- **Frozen 대형 모델 위에서 test-time에만 최적화하는 패턴이 반복됨** — [LEAP](https://arxiv.org/abs/2609.03294)는 frozen world model 위 L-BFGS trajectory 최적화, [LaPla](https://arxiv.org/abs/2609.04070)는 frozen VQ-VAE decoder에 continuous latent를 투영함. 둘 다 backbone은 그대로 두고 inference 단계 목적함수·표현만 바꿔 성능을 올림.
- **VLM/world model 평가 자체를 벤치마크 대상으로 삼는 논문이 늘어남** — [FailBench](https://arxiv.org/abs/2609.03611)는 VLM 실패 판정 신뢰도 상한이 0.77에 그침을, [MINERVA](https://arxiv.org/abs/2609.03715)는 LIBERO가 사실상 task memorization을 측정한다는 것을 보임. [VeriPhy](https://arxiv.org/abs/2609.03153)는 생성 비디오 물리적 타당성 검증의 recall 한계를 정량적으로 보임. 방법 제안보다 기존 평가 체계의 허점을 드러내는 방향임.
- **센서·모달리티 신뢰도를 명시적으로 다루는 VLA 연구가 등장함** — [Sensing Which Modality Matters](https://arxiv.org/abs/2609.03142)는 evidence-gated invariance/sufficiency로 modality entanglement를 억제하고, [FWBC-VLA](https://arxiv.org/abs/2609.03889)는 F/T 센서 없이 관절 잔차 토크로 접촉력을 추정해 policy에 조건화함. 저비용 센서·데이터로 견고성을 확보하려는 흐름임.
- **3D representation을 검색·추론의 매개체로 쓰는 연구가 이어짐** — [RoboTok](https://arxiv.org/abs/2609.03199)은 사람이 등장하는 인터넷 동영상을 actor-centric 3D trajectory로 바꿔 유사 시연을 검색하고, [GraFT](https://arxiv.org/abs/2609.03892)는 3D scene graph에서 도구·BEV·egocentric frame을 파생시켜 frozen MLLM에 공간추론을 부여함. 둘 다 학습 없이 표현 변환만으로 성능을 올림.
- **자율주행·우주로봇 등 로봇학습 방법론의 인접 도메인 전이가 활발함** — [SV-WAM](https://arxiv.org/abs/2609.03602), [LaPla](https://arxiv.org/abs/2609.04070)는 world-action model을 자율주행에, [GPU-Accelerated Astrodynamics World Models](https://arxiv.org/abs/2609.03067)는 world model을 우주선 도킹에 처음 적용함. manipulation에서 검증된 아이디어가 다른 embodiment로 빠르게 옮겨감.

## 유망 연구 방향 및 프로젝트 제안

**World model 신뢰도 기반 test-time imagination 예산 배분**
- research question: world model rollout이 언제부터 신뢰할 수 없는지를 실시간으로 판정해, 신뢰 가능한 horizon에만 연산을 쓰는 test-time planner를 만들 수 있는가
- 접근·novelty: [WISE](https://arxiv.org/abs/2609.03681)의 bounded rollout + reliability filter와 [Latent Energy Action Planning](https://arxiv.org/abs/2609.03294)의 decoder 기반 terminal energy, [GPU-Accelerated Astrodynamics World Models](https://arxiv.org/abs/2609.03067)의 예측 불확실성 기반 이상 탐지를 하나의 판정 모듈로 통합
- 왜 지금·경쟁 prior works: 세 논문 모두 world model 신뢰도를 각자 다른 방식(ranking consistency, terminal state 오차, uncertainty)으로 다루면서도 서로 비교하지 않음. 이를 통일된 test-time controller로 formulation하면 세 baseline과 직접 비교 가능
- risk·target venue: world model 자체를 새로 학습해야 해 비용이 큼. CoRL/ICRA 겨냥, real-robot 검증 필수

**힘·접촉 정보를 결합한 multimodal failure detector**
- research question: 시각만으로 접촉 여부를 판단하기 어려운 assembly-class task에서, 힘·촉각 신호를 추가하면 실패 판정 정확도가 얼마나 개선되는가
- 접근·novelty: [FailBench](https://arxiv.org/abs/2609.03611)가 밝힌, 접촉 task를 chance-level로만 판정하는 한계에 [FWBC-VLA](https://arxiv.org/abs/2609.03889)의 센서리스 접촉력 추정을 결합해 VLM judge의 입력을 확장. FailBench 자체는 시각 전용 벤치마크라 이 조합은 아직 없음
- 왜 지금·경쟁 prior works: FailBench가 vision-only judge의 한계를 정량화해 놓아 개선폭을 바로 측정 가능. tactile perception을 failure detection에 붙인 선행연구는 있으나 FailBench 프로토콜로 평가한 사례는 없음
- risk·target venue: 힘 센서·촉각 데이터가 있는 real-robot task로 한정됨. CoRL/RSS, D&B track도 고려 가능

**Object-centric 3D 검색 기반 test-time failure recovery**
- research question: 실패 직후 유사한 성공 시연을 3D 표현으로 검색해 recovery 궤적을 즉시 생성할 수 있는가
- 접근·novelty: [RoboTok](https://arxiv.org/abs/2609.03199)의 actor-centric 3D trajectory retrieval을 object-centric 좌표계로 바꾸고, [GraFT](https://arxiv.org/abs/2609.03892)의 3D scene graph를 검색 인덱스로 결합. RoboTok은 학습 데이터 확보용으로만 검색을 쓰고 test-time recovery에는 쓰지 않음
- 왜 지금·경쟁 prior works: retrieval augmented policy는 있으나 실패 발생 이후 실시간 recovery로 쓴 사례는 아직 드묾. RoboTok의 검색 정확도(mAP@20 0.353)가 이미 실증됨
- risk·target venue: 검색 latency가 실시간 recovery에 맞는지가 관건. CoRL 겨냥, 실로봇 실패 시나리오 데이터셋 구축이 선행되어야 함

**Evidence-gated 센서 신뢰도를 counterfactual로 학습**
- research question: 사전 정의된 task 구조 없이, 센서를 가상으로 perturb했을 때 예측이 얼마나 바뀌는지로 evidence 신뢰도를 학습할 수 있는가
- 접근·novelty: [Sensing Which Modality Matters](https://arxiv.org/abs/2609.03142)의 evidence-gated invariance/sufficiency가 현재는 사전 정의된 라벨에 의존하는 한계를, [VeriPhy](https://arxiv.org/abs/2609.03153)의 typed evidence record(measured/abstained/errored) 구조로 보완하고, 여기에 world model 기반 counterfactual perturbation을 새로 추가해 대체
- 왜 지금·경쟁 prior works: 두 논문 모두 evidence 개념을 다루지만 각각 라벨 의존과 미실행 closed-loop라는 한계를 스스로 명시함. 둘을 잇는 후속 연구가 명시적 gap으로 열려 있음
- risk·target venue: counterfactual perturbation을 실로봇에서 안전하게 수행하는 절차가 필요. CoRL/RSS

**과거-압축·미래-정밀 비대칭 표현을 manipulation에 이식**
- research question: 자율주행에서 검증된 "과거는 discrete로 압축, 미래는 continuous로 정밀 생성"하는 비대칭 표현이 manipulation VLA의 action tokenizer에도 유효한가
- 접근·novelty: [LaPla](https://arxiv.org/abs/2609.04070)의 frozen residual VQ-VAE decoder + continuous latent projection 구조를 FAST 등 기존 manipulation action tokenizer와 비교 실험
- 왜 지금·경쟁 prior works: LaPla는 자율주행 궤적에서만 검증됨. manipulation은 접촉·힘 등 자율주행에 없는 불연속성이 있어 같은 설계가 통할지가 열린 질문
- risk·target venue: 자율주행과 manipulation의 action space 성격이 달라 이식이 실패할 위험이 있음. ICRA/CoRL, quantization error 완화 폭을 baseline과 비교해 검증 필요

## 오늘 반드시 읽어야 할 논문

- [RoboTok](https://arxiv.org/abs/2609.03199) — 사람이 등장하는 인터넷 동영상을 actor-centric 3D 검색 인덱스로 바꿔 STRAP 대비 mAP@20을 0.007→0.353으로 압도적으로 올린 데이터 확보 파이프라인임
- [Puffin-World](https://arxiv.org/abs/2609.04196) — 중력·기하·외형을 하나의 world state로 통합해 long-horizon 3D world 생성에서 방향 drift를 없앤 native world model임
- [WISE](https://arxiv.org/abs/2609.03681) — world model imagination을 언제 쓸지 스케줄링해 GPU 연산 77% 절감하면서 real robot 성능까지 올린 VLA post-training 프레임워크임
- [Sensing Which Modality Matters](https://arxiv.org/abs/2609.03142) — modality entanglement를 evidence-gated invariance/sufficiency로 정식화하고 두 embodiment 실로봇 실험까지 검증한 VLA robustness 연구임
- [FailBench](https://arxiv.org/abs/2609.03611) — VLM 기반 실패 판정기 13종을 교차 평가해 최고 모델도 balanced accuracy 0.77에 그친다는 상한을 정량적으로 제시함
- [GIFT](https://arxiv.org/abs/2609.04193) — geometry·affordance·goal 구조적 감독을 학습 시점 제약으로만 부여해 VLA와 world-action model 양쪽에서 성능을 올린 no-injection 설계임
- [GraFT](https://arxiv.org/abs/2609.03892) — 3D scene graph 하나에서 도구·BEV·egocentric frame을 파생시켜 학습 없이 frozen MLLM의 공간추론을 VSI-Bench 1위로 올린 프레임워크임
- [VeriPhy](https://arxiv.org/abs/2609.03153) — 생성 비디오의 물리적 타당성을 typed evidence로 검증하되, closed-loop refinement는 미실행으로 남겨 후속 연구 gap을 명확히 제시함

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (367편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2609.03681'>WISE: World-model-guided Imagination Scheduling for Efficient Post-training of Vision-Language-Action Models</a></td><td>78</td><td>9</td><td>VLA</td><td>world model 상상을 언제 어디서 쓸지 스케줄링해 VLA post-training 연산을 80% 절감하고 real-world robustness도 개선함</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2609.04193'>GIFT: Guided Intermediate Feature Training via Action-Oriented Structural Supervision for Robotic Manipulation</a></td><td>74</td><td>9</td><td>VLA</td><td>geometry·affordance·goal 구조를 중간 feature 학습 제약으로 명시해 action-sufficiency gap을 정의하고 VLA와 WAM 모두에서 LIBERO-Plus·RoboCasa 성능을 크게 높임</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2609.03199'>RoboTok: An Internet-Scale Data Engine for Human Demonstration Retrieval and Dexterous Manipulation Learning</a></td><td>72</td><td>9</td><td>Manipulation</td><td>웹 동영상에서 hand-trajectory 기반 latent motion space로 dexterous manipulation demonstration을 retrieval하는 데이터 엔진임. VLA·manipulation 학습 데이터 확보의 새로운 formulation으로 우선순위가 매우 높음.</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2609.03565'>Toward Physically Grounded JEPA World Models for Goal-Conditioned Robotic Planning</a></td><td>72</td><td>9</td><td>World Model</td><td>IDM와 state alignment를 결합한 JEPA world model로 로봇 planning 성공률을 높였으나 4개 소규모 벤치마크에 그침</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2609.03294'>Latent Energy Action Planning with World Models</a></td><td>72</td><td>8</td><td>World Model</td><td>frozen world model 위에서 action horizon 전체를 미분 가능하게 최적화하는 latent energy planning으로 CEM 대비 성공률을 77.5%에서 94.8%로 크게 높인 test-time planning 기여</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2609.04196'>Puffin-World: Scaling a Unified Multimodal Model with Native 3D World States</a></td><td>72</td><td>7</td><td>World Model</td><td>물리·기하·외형을 native world state로 통합 모델링하고 카메라 조건부로 생성과 재구성을 동시에 수행하는 unified world model임. world model 우선 주제의 핵심에 해당하며 formulation과 스케일 모두 새로움.</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2609.03142'>Sensing Which Modality Matters: Evidence-Gated Regularization for Robust VLA Policies</a></td><td>68</td><td>10</td><td>VLA</td><td>modality entanglement라는 새로운 실패 모드를 정의하고 evidence 기반 정규화로 해결, 양팔·촉각 로봇 실기 실험에서 최대 183% 성공률 개선을 보인 강한 VLA 논문</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2609.03715'>MINERVA: How Small Can a Manipulation Policy Be and Still Solve LIBERO?</a></td><td>68</td><td>8</td><td>Manipulation</td><td>0.54M 파라미터로 LIBERO를 95% 이상 푸는 capacity floor를 밝히고 instruction conditioning이 사실상 task 암기임을 보인 분석이 흥미로움</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2609.03889'>FWBC-VLA: Force-Aware Whole-Body Compensation for Contact-Rich Loco-Manipulation</a></td><td>66</td><td>8</td><td>VLA</td><td>센서 없는 잔차 토크 추정을 VLA 토큰으로 주입해 접촉이 많은 loco-manipulation을 안정화한 실로봇 검증이 있음</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2609.03602'>SV-WAM: An Efficient Surround-View World-Action Model for End-to-End Autonomous Driving</a></td><td>65</td><td>7</td><td>World Model</td><td>surround-view world-action model로 action-video를 함께 학습하되 배포 시 video branch를 제거해 효율적 planning을 수행함. world model과 action을 통합하는 causal mask 설계가 새롭고 우선 주제와 직접 연결됨.</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2609.03892'>GraFT: A Training-Free Framework for Spatial Reasoning in Multimodal Large Language Models via 3D Scene Graphs</a></td><td>65</td><td>7</td><td>Embodied AI</td><td>3D scene graph로부터 기하 도구·BEV·egocentric grounding을 제공하는 training-free 공간추론 프레임워크임. scene graph와 embodied spatial reasoning 우선 주제 모두와 직접 연결되고 성능 향상 폭도 큼.</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2609.03153'>VeriPhy: Agentic Physical Reasoning for World Model Evaluation and Refinement</a></td><td>65</td><td>6</td><td>World Model</td><td>비디오 생성물의 물리적 타당성을 typed obligation과 근거 기록으로 검증하는 agentic 평가 시스템임. world model 검증이라는 우선 주제와 직접 연결되고 새로운 evaluation paradigm을 제시함.</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2609.03611'>FailBench: How Reliable are VLMs at Judging Robot Task Success?</a></td><td>64</td><td>8</td><td>Manipulation</td><td>로봇 실패 탐지에 특화된 대규모 벤치마크로 VLM 기반 판정기의 한계를 정량화했으나 새 방법 제안은 없음</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2609.03067'>GPU-Accelerated Astrodynamics World Models for Spacecraft Rendezvous and Proximity Operations</a></td><td>62</td><td>8</td><td>World Model</td><td>위성 랑데부·근접운항에 world model을 최초로 적용, flow matching 기반 잠재상태 예측으로 RL 대비 도킹 성공률 53% vs 29%, OOD 일반화도 우수</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2609.04070'>Continuous Actions from Discrete Minds: Latent-Aligned Planning for End-to-End Autonomous Driving</a></td><td>62</td><td>7</td><td>VLA</td><td>VQ-VAE 기반 action tokenizer의 continuous latent를 재사용해 discrete VLM reasoning과 continuous 주행 action을 직접 연결하는 VLA 프레임워크임. 행동 표현 우선 주제와 직결되고 latent-aligned planning이 새로운 formulation임.</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2609.03572'>Drive-HWM: Hierarchical World Models for Dynamic-Latent Guided Autonomous Driving</a></td><td>62</td><td>6</td><td>World Model</td><td>자율주행을 위한 slow-fast hierarchical world model로 예측과 행동 생성을 서로 다른 시간 스케일에서 결합함. world model과 action generation을 연결하는 우선 주제와 직접 맞닿아 있고 architecture formulation이 새로움.</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2609.03673'>Do Video Generators Track the World Across Segments? A Benchmark and Method for World-State Reasoning in Video Continuation</a></td><td>62</td><td>6</td><td>World Model</td><td>비디오 연속 생성에서 world-state를 명시적 엔티티 표현으로 추적·갱신하는 벤치마크와 방법임. world model의 상태 일관성 유지라는 우선 주제와 직접 연결됨.</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2609.03952'>WorldReward: Reward Modeling for Camera-Conditioned World Models</a></td><td>62</td><td>6</td><td>World Model</td><td>camera-conditioned world model을 위한 VLM 기반 action-consistency·visual-quality 통합 reward model임. world model 평가와 RL post-training에 직접 연결되는 새로운 기여임.</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2609.03591'>Scaling Bimanual Household Manipulation from 1,500 hours of Demonstrations to On-Policy Corrections</a></td><td>60</td><td>8</td><td>VLA</td><td>1500시간 규모 bimanual 데모와 DAgger correction으로 VLA 스케일링 트렌드를 검증했으나 새로운 방법론 기여는 제한적임</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2609.03906'>Revisiting Topological Graphs for Macro Action based Closed-loop Reinforcement Learning of Vision Language Navigation in Continuous Environment</a></td><td>60</td><td>7</td><td>Navigation</td><td>토폴로지 그래프로 VLN-CE를 계층적 MDP로 재구성해 closed-loop RL을 가능하게 했고 R2R-CE에서 SOTA를 달성함</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2609.04096'>Adaptive Vision-Language Grasping via Composable Foundation Priors and Generalizable Grasp Synthesis</a></td><td>60</td><td>7</td><td>Manipulation</td><td>grasp synthesis와 foundation model 이해를 분리해 재학습 없이 grasp를 일반화하는 구조를 제안했으나 각 모듈은 기존 기법 조합임</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2609.03657'>Rethinking 3D Noise: Learning 3D-Aware Video Priors via Optimization-Free Morphological Perturbations</a></td><td>58</td><td>7</td><td>3D Vision</td><td>3DGS를 픽셀처럼 다뤄 scale·rotation·pruning 섭동을 가하는 optimization-free 정규화로 sparse-view artifact를 줄임. 다운스트림 로봇 조작 정책 성공률까지 검증해 3D representation과 manipulation을 직접 연결함.</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2609.03225'>Long-Horizon Consistent and Interaction-Aware World Models for Multi-Style End-to-End Driving</a></td><td>58</td><td>7</td><td>World Model</td><td>시간적 일관성 정규화와 상호작용 상태 분리, GRPO 기반 다중 스타일 최적화를 결합한 world model 주행 정책으로 Bench2Drive에서 +17.08점 개선, 실차 sim-to-real 시연</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2609.03729'>Unfold The World: Factorize 4D Properties in Reinforcing Spatial Reasoning</a></td><td>58</td><td>6</td><td>Embodied AI</td><td>VLM의 4D 공간추론을 평면대응·깊이일관성·시간가역성으로 분해해 강화학습으로 최적화함. embodied spatial reasoning 우선 주제와 직접 연결되고 문제 분해 방식이 새로움.</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2609.03919'>OctWorld: Long-Range World-Consistent Video Generation with Octree-Based 3D Mapping</a></td><td>58</td><td>5</td><td>World Model</td><td>octree 기반 persistent 3D memory로 재방문 영역까지 공간 일관성을 유지하는 long-range 비디오 생성 프레임워크임. world model의 장기 공간 일관성이라는 우선 주제와 직접 연결되고 표현 방식이 새로움.</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2609.04200'>Principia: Relational Physics Tests for Video Models</a></td><td>58</td><td>5</td><td>World Model</td><td>물체 간 상대적 물리 법칙 일관성으로 비디오 생성모델의 뉴턴역학 이해를 평가하는 calibration-independent 벤치마크임. world model의 물리적 타당성 검증이라는 우선 주제와 직접 연결되고 기존 벤치마크(VBench)와의 괴리를 강하게 드러냄.</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2609.03984'>MulDP: Multimodal Diffusion Policy for Autonomous Quadruped Parkour Navigation across Complex Terrains</a></td><td>56</td><td>7</td><td>Navigation</td><td>멀티모달 diffusion policy로 쿼드루페드 parkour 내비게이션을 학습했고 실로봇 실험도 포함하나 방법 자체는 diffusion policy의 응용에 가까움</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2609.03774'>Rethinking World Models for Safety-Critical Embodied Systems</a></td><td>55</td><td>9</td><td>World Model</td><td>world model이 우도·시각적 충실도만으로는 안전한 의사결정을 보장하지 못한다는 구조적 문제를 지적하고 counterfactual reasoning과 episodic safety memory를 통합한 Risk-Informed World Model을 제안해 누리랩 우선주제와 정확히 겹치나 perspective 논문이라 실증은 없음</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2609.03483'>Air-Ground Collaborative Vision-and-Language Navigation via Shared Bird&#x27;s-Eye Maps</a></td><td>55</td><td>8</td><td>Navigation</td><td>UAV의 전역 시야와 UGV의 지역 시야를 공유 bird&#x27;s-eye map으로 결합한 최초의 training-free air-ground 협업 VLN 베이스라인, CARLA-Air에서 개별 에이전트 대비 성공률 27%p 향상</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2609.03497'>BRIDGE: An Open-Source Humanoid Platform via Morphology-Control Co-Design for Physical AI</a></td><td>55</td><td>8</td><td>Embodied AI</td><td>인간 동작 재현도를 정량화하는 새 지표로 모습-제어를 공동 설계한 오픈소스 88cm 휴머노이드 플랫폼, 기존 로봇 대비 SOTA 동작 충실도</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2609.04066'>Subspace Inference Enables Efficient Active Reward Learning from Preferences</a></td><td>55</td><td>6</td><td>RL</td><td>extended Kalman filter로 저차원 부분공간에서 보상모델 불확실성을 순차 추적해 능동적 선호학습을 확장 가능하게 한 기법, D4RL·V-D4RL에서 검증된 로봇 강화학습 인접 연구</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2609.03927'>Toward Unified Robot Learning: Bridging Representation, Vision-Language-Action, and World Models</a></td><td>52</td><td>8</td><td>Embodied AI</td><td>representation·VLA·world model을 통합하는 로봇 학습 서베이로 방향 제시는 유용하나 새로운 실험적 기여는 없음</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2609.03276'>R2S-Eval: Robot Evaluation with Real-to-Sim Calibration via Vision-Language Models</a></td><td>52</td><td>7</td><td>VLA</td><td>real-to-sim 보정과 VLM 선호 평가를 결합해 반복 실기 실험 없이 로봇 정책을 통계적으로 안정되게 평가하는 새로운 평가 파이프라인</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2609.03055'>Seeing Less Is Not Seeing Safely: Privacy Leakage from Task-Scoped Robot Perception Exports</a></td><td>52</td><td>6</td><td>Embodied AI</td><td>가정용 로봇의 task-scoped perception export가 raw 센서를 남기지 않아도 의미·기하 정보로 프라이버시를 노출함을 AI2-THOR로 실증한 새로운 문제설정</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2609.04088'>Efficient Semantic Understanding from Digital Foveation</a></td><td>52</td><td>5</td><td>Embodied AI</td><td>생물학적 중심와 지각에서 착안한 saliency 기반 active vision으로 dense segmentation 대비 계산량을 크게 줄이면서 의미 이해를 유지함. active perception 우선 주제와 개념적으로 직접 연결됨.</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2609.03842'>Multi-step Proximal Policy Improvement in Offline Reinforcement Learning</a></td><td>52</td><td>5</td><td>RL</td><td>정책을 확률 매니폴드 위의 gradient flow로 보고 다단계 proximal step으로 개선하는 offline RL 기법, D4RL에서 TD3+BC 등 baseline 대비 향상</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2609.03383'>TIGPO: Temporal Instance-Graph Policy Optimization for Long-Horizon LLM Agents</a></td><td>52</td><td>4</td><td>RL</td><td>정책 업데이트를 넘나드는 지속적 transition graph로 credit assignment를 확장한 long-horizon agent RL, ALFWorld 등 embodied-style 벤치마크에서 검증</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2609.03003'>Causal Foundation Models</a></td><td>52</td><td>3</td><td>LG</td><td>in-context causal effect 추정을 위한 foundation model 패러다임 소개로 causal reasoning 연구에 참고할 만하나 아직 개론 수준</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2609.03175'>Real-Time Shape Control of Multi-Segment Soft Robotic Arms Using Koopman Operators with Global and Local Observables</a></td><td>50</td><td>7</td><td>Manipulation</td><td>전역·국소 observable을 결합한 Koopman MPC로 10분절 소프트암의 실시간 형상제어를 실기로 검증한 로봇 제어 연구</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2609.03557'>Building Pretraining Data for World Models: An Unreal Engine-Based Pipeline for Action-Conditioned Video Generation</a></td><td>50</td><td>6</td><td>World Model</td><td>Unreal Engine 기반 action-conditioned video 대규모 synthetic 데이터 생산 파이프라인임. world model 학습 데이터 확보라는 우선 주제와 직접 연결되나 기여 자체는 엔지니어링 인프라 구축에 가까움.</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2609.03222'>Following a Unique Path: A Fast Certifier Applied to Outlier-Robust Pose Registration</a></td><td>50</td><td>6</td><td>3D Vision</td><td>SDP 완화의 degeneracy를 central path를 따라 우회해 인증하는 certifier로 pose registration을 기존 대비 최대 1000배 빠르게 인증, 실데이터 파이프라인 검증</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2609.03931'>Sparse auto-regressive modeling for scene generation from multi-view images</a></td><td>50</td><td>4</td><td>3D Vision</td><td>sparse voxel-aligned 3D latent generative model로 3DGS supervision만으로 미관측 영역을 completion함. object-centric 3D representation 우선 주제와 연관됨.</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2609.02991'>TRACE: Spatiotemporal Contact Memory Graph Network Simulator for Granular Dynamics</a></td><td>50</td><td>4</td><td>World Model</td><td>contact edge에 상호작용 이력을 저장하는 graph simulator로 granular manipulation에 쓰일 수 있는 물리 시뮬레이터이나 로봇 태스크 검증은 없음</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2609.02987'>Tail-Likelihood Reinforcement Learning</a></td><td>50</td><td>3</td><td>RL</td><td>reward tail coverage를 직접 최적화하는 새로운 RL objective로 maze navigation 등에 적용했으나 로봇 실증은 없음</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2609.03117'>Kernel Reboot: Breaking the Boundaries of Neural Tangent Kernels for Neural Fields</a></td><td>50</td><td>2</td><td>3D Vision</td><td>NTK 기반 neural field를 meta-learning과 결합해 sparse-view 복원을 개선, 3D representation 연구에 참고 가능하나 로봇 검증 없음</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2609.02986'>Modern Transformers Are Implicit Hybrids: From Functional Differentiation to Principled Hybrid Architecture Design</a></td><td>50</td><td>1</td><td>LG</td><td>RoPE head 기능 분석으로 하이브리드 attention 설계 원칙을 제시하나 로봇 문제와 무관한 LLM 아키텍처 연구</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2609.03561'>TRaIL-Odom: Tightly Coupled Continuous Time Radar-IMU-LiDAR Odometry with Adaptive Doppler Weighting</a></td><td>48</td><td>6</td><td>Navigation</td><td>LiDAR 기하학적 degeneracy 방향에 맞춰 레이더 도플러 가중치를 적응적으로 조정하는 tightly-coupled odometry, degenerate 구간에서 ATE·RTE 86%/78.5% 개선</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2609.04201'>Scal3R: Learning Efficient Multi-Relative Pose Query for Scalable Online 3D Reconstruction</a></td><td>48</td><td>5</td><td>3D Vision</td><td>고정 앵커 대신 multi-reference relative pose query로 온라인 3D 재구성의 장기 드리프트를 억제함. 로봇 내비게이션·매핑에 유용한 online SLAM 성능 개선 기여임.</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2609.04203'>Temporal Self-Distillation: Learning Visual State Tracking in Videos Without Supervision</a></td><td>48</td><td>3</td><td>Video</td><td>self-distillation으로 라벨 없이 video state tracking을 학습하는 아이디어는 흥미로우나 로봇 인식 파이프라인과 직접 연결은 약함</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2609.03358'>Time Without Timesteps: Simulating Coupled Dynamical Systems via Self-Consistency</a></td><td>48</td><td>3</td><td>LG</td><td>시간축 순차 롤아웃 대신 궤적 전체의 self-consistency 고정점으로 결합 동역학계를 시뮬레이션하는 새로운 정식화, world model의 시뮬레이션 백엔드에 참고 가능</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2609.03442'>Guide, Not Bind: Why Defeasible Priors Fail in Augmented Lagrangian Causal Discovery</a></td><td>48</td><td>2</td><td>LG</td><td>causal discovery에서 전문가 prior를 forbidden-edge로 넣는 augmented Lagrangian 완화 기법이 실패하는 이유를 이론적으로 규명</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2609.03241'>FlowBalance: Verifier-Grounded Self-Improvement from On-Policy Reasoning Experience</a></td><td>48</td><td>1</td><td>RL</td><td>verifier 신호로 자기 안내 점수를 보정하는 self-improvement RL 기법으로 수학 추론에서 안정성을 개선했으나 로봇 응용 없음</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2609.04010'>Unlocking Lossless Speedups in LLMs via Discrete Diffusion</a></td><td>48</td><td>0</td><td>LG</td><td>AR 가중치와 경량 diffusion 가중치를 분리해 무손실 병렬 디코딩을 구현한 LLM 추론 가속 기법, 강력한 실증이나 로봇과 무관</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2609.03604'>On the Interaction Between Model Compression and Test-Time Adaptation</a></td><td>47</td><td>3</td><td>LG</td><td>모델 압축이 test-time adaptation 성능을 저해하는 현상을 체계적으로 분석, test-time optimization 연구에 참고 가능하나 분류 도메인에 국한</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2609.03667'>Out-of-Distribution Generalisation with Sequence Models in Offline Multi-Agent Reinforcement Learning</a></td><td>47</td><td>3</td><td>RL</td><td>offline multi-agent RL의 zero-shot 일반화가 데이터셋 크기보다 태스크 다양성에 좌우됨을 보인 대규모 실증 연구</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2609.02959'>The Geometry of Ignorance: LLMs Know When to Temper Bayesian Priors</a></td><td>47</td><td>1</td><td>NLP</td><td>unembedding 기하학으로 LLM의 prior 의존도를 해석하는 mechanistic 분석이나 로봇 연구와 관련성 낮음</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2609.03443'>Beyond Straightness: Non-Crossing Flow Matching via Quantile AlignTree Coupling</a></td><td>47</td><td>1</td><td>LG</td><td>quantile-aligned tree coupling으로 flow matching의 경로 교차를 줄이는 효율적 구조화 커플링 기법</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2609.03533'>Coupled Scaling: A Representational Accessibility Framework for Neural Scaling Laws</a></td><td>46</td><td>1</td><td>LG</td><td>아키텍처가 도달 가능한 표현 기하와 태스크 구조의 관계로 scaling law를 설명하는 이론적 프레임워크</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2609.04147'>A Low-Cost, Open Platform for End-to-End Autonomous Driving on a Miniature Ackermann Vehicle</a></td><td>45</td><td>6</td><td>Embodied AI</td><td>소형 애커먼 차량으로 sim-to-real end-to-end 자율주행을 검증하는 오픈 플랫폼, command-conditioned behavior cloning 베이스라인 위주로 방법론적 새로움은 제한적</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2609.04202'>TokenMatch: 3D Mesh Correspondence Transformer with Curvature-Guided Tokenisation</a></td><td>45</td><td>2</td><td>3D Vision</td><td>곡률 기반 토큰화로 partial shape matching 성능을 개선했으나 로봇 응용과는 거리가 있고 기존 correspondence 프레임워크의 확장에 가까움</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2609.03686'>Resolution-Aware Experimental Design under Partial Identifiability</a></td><td>45</td><td>2</td><td>LG</td><td>partial identifiability 하에서 구조적 후보집합 크기를 기준으로 실험을 선택하는 정식화, active perception과 개념적으로 유사하나 지구과학 벤치마크</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2609.04134'>Prospective Coding Improves Learning in Deep Continuous-Time Recurrent Networks</a></td><td>45</td><td>2</td><td>LG</td><td>bottom-up 입력을 prospective하게 만드는 파라미터 없는 보정으로 깊은 연속시간 RNN의 gradient attenuation을 완화, 로봇 제어용 continuous-time 모델에 참고 가능</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2609.03026'>ObserverBench: Testing Mechanistic Estimates for Intervention and Control</a></td><td>45</td><td>1</td><td>LG</td><td>해석가능성 추정치가 실제 개입 성능으로 이어지는지 검증하는 벤치마크, mechanistic interpretability 분야 기여이나 로봇과 무관</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2609.03900'>Beyond Endpoint Scores: Time- and Capacity-Conditioned Evaluation of Continual Knowledge Updating</a></td><td>45</td><td>1</td><td>LG</td><td>continual knowledge editing 방법 비교가 평가 시점과 replay 용량에 따라 뒤집힘을 보인 평가 방법론 비판 논문, lifelong learning 평가에 참고 가능</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2609.03858'>High-Dimensional Learning Dynamics of Attention-Indexed Models</a></td><td>45</td><td>0</td><td>LG</td><td>attention 파라미터화의 학습 동역학을 고차원 극한에서 분석해 tied/untied attention의 회복 샘플복잡도를 규명한 이론 논문</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2609.03422'>Inferred Generative-Process Diversity Predicts Correlated Failure Across Language Models</a></td><td>44</td><td>1</td><td>LG</td><td>압축거리 기반으로 LLM 집단의 생성과정 다양성이 상관된 실패를 예측함을 보인 분석, 멀티에이전트 안전성에 참고 가능</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2609.03621'>A computable representation of the physical laboratory enables verifiable workflows</a></td><td>42</td><td>6</td><td>Embodied AI</td><td>물리 실험실을 타입 지정 연구객체·역량기반 연산·조합 워크플로 대수로 계산 가능하게 표현해 로봇 실험실에서 실행 전 사전조건을 검증하는 프레임워크로 TAMP적 formulation에 가까움</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2609.03824'>VI3: Grounding Pretrained 3D Foundation Models with Inertial Cues</a></td><td>42</td><td>5</td><td>3D Vision</td><td>IMU 관성 신호로 3D foundation model의 metric scale을 복원하는 model-agnostic 프레임워크임. 로봇 상태추정·내비게이션에 유용한 센서 융합 기여이나 항공 도메인 중심으로 검증됨.</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2609.03229'>Language-encoded network topology enables large language models to reason about complex networks</a></td><td>42</td><td>1</td><td>NLP</td><td>네트워크 구조를 언어화해 LLM의 구조 추론을 돕는 새로운 표현법이나 로봇 scene graph와는 다른 도메인</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2609.03379'>RecurTrace: Adaptive Latent Reasoning with Loop-Time Memory</a></td><td>42</td><td>1</td><td>LG</td><td>루프 시간축에 대한 attention과 halting head로 latent recurrence 추론 깊이를 적응적으로 조절하는 기법</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2609.02998'>Verify Before You Distill: Prompt-Level Teacher Gating for On-Policy Distillation</a></td><td>42</td><td>0</td><td>NLP</td><td>teacher 신뢰도를 prompt 단위로 검증해 on-policy distillation을 게이팅하는 LLM post-training 기법</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2609.03342'>Gradients Know What Outcomes Don&#x27;t: Unlocking Reinforcement Learning for LLM Reasoning with Gradient-Aligned Rewards</a></td><td>42</td><td>0</td><td>RL</td><td>정책의 gradient 공간에서 expert anchor와의 코사인 유사도로 dense reward를 만드는 RLVR 기법</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2609.03436'>It&#x27;s the Problem, Not the Path: Budget and Difficulty Confounds in LLM Reasoning Trajectories</a></td><td>42</td><td>0</td><td>NLP</td><td>LLM 추론 궤적의 breakthrough 해석에 restart-controlled·난이도 통제 실험으로 반박한 방법론적 비판 논문</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2609.03807'>Free Pause Tokens</a></td><td>42</td><td>0</td><td>LG</td><td>병렬 예측 스트림으로 추가 문맥 길이 없이 사고 토큰 효과를 내는 효율적 추론 기법</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2609.03949'>VestigeKV: The NoPE-MLA KV Cache Carries Its Own Eviction Signal in a Vestigial Branch</a></td><td>42</td><td>0</td><td>NLP</td><td>NoPE-MLA의 decoupled 분기를 재활용해 query 없이 KV cache를 압축하는 기법, 특정 아키텍처 한정 발견</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2609.03362'>ARTiS: An Adaptive Robotic Gripper for Enhanced Tool Manipulation in Disassembly Applications</a></td><td>40</td><td>6</td><td>Manipulation</td><td>소프트 팜과 7자유도 손가락을 결합해 해체작업용 공구를 안정적으로 파지하는 적응형 그리퍼 하드웨어 설계</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2609.04174'>Zero-Shot Novel Depth Synthesis Using 3D Foundation Models Scene Representations</a></td><td>40</td><td>4</td><td>3D Vision</td><td>3D foundation model 내부 표현에서 latent diffusion으로 미관측 시점의 depth를 합성하는 방법임. novel view 지각 개선으로 active perception에 활용 가능함.</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2609.03660'>Local Updates, Global Learning (LUGL): Playing Games with non-incremental Learners</a></td><td>40</td><td>2</td><td>RL</td><td>데이터 수집과 모델 학습을 분리해 gradient-boosted tree를 self-play RL에 쓸 수 있게 한 프레임워크, 보드게임 도메인 한정</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2609.04189'>Robust PAC Learning of Concurrent Stochastic Games</a></td><td>40</td><td>2</td><td>RL</td><td>전이 불확실성이 있는 concurrent stochastic game에 대한 최초의 PAC 학습 프레임워크, 멀티로봇 게임이론에 이론적으로 연관</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2609.02982'>Equation Recast for Canonical Operator Learning Across Parametric PDEs</a></td><td>40</td><td>1</td><td>LG</td><td>PDE parametric operator learning을 canonical form으로 재구성한 물리 시뮬레이션 논문으로 로봇 적용 가능성 낮음</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2609.02993'>No-Regret Bayesian Optimization with Finite-Library Input-Warped Kernels</a></td><td>40</td><td>1</td><td>RL</td><td>유한 warp library로 GP-UCB의 후회 보장을 유지하며 커널 기하를 적응시키는 베이지안 최적화 기법, 로봇 응용은 제시 안 됨</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2609.03069'>Learnable composition for neural operators</a></td><td>40</td><td>1</td><td>LG</td><td>국소 사전학습과 조합 모듈로 neural operator의 도메인 전이를 개선한 물리 시뮬레이션 연구</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2609.03306'>Geometry-Aware Graph Construction via Adaptive Spectral Bandwidth Control</a></td><td>40</td><td>1</td><td>CV</td><td>커널 스펙트럼 복잡도를 매니폴드 고유차원에 맞추는 그래프 구성법, SSL 임베딩에서 성능 개선</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2609.03324'>DE-Venus: A Data-Efficient RLVR Framework for Large Language Models</a></td><td>40</td><td>0</td><td>RL</td><td>RLVR 파이프라인의 데이터 선별·약지도·정제를 통합한 프레임워크로 라벨 효율을 높였으나 LLM 추론 도메인 한정</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2609.03377'>SimpleDesign: A Joint Model for Protein Sequence and Structure Codesign</a></td><td>40</td><td>0</td><td>LG</td><td>단일 단계 end-to-end objective로 단백질 서열·구조를 공동 생성하는 모델, 로봇과 무관한 생물학 응용</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2609.03582'>WeatherNext 3: Increasing resolution and performance of global weather models with raw observations</a></td><td>40</td><td>0</td><td>LG</td><td>관측 데이터를 직접 동화해 해상도와 성능을 높인 대규모 기상예보 파운데이션 모델, 로봇과 무관</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2609.03826'>Witnesses Explain Anomalies</a></td><td>40</td><td>0</td><td>LG</td><td>구면 방향 투영으로 스코어와 설명을 동시에 제공하는 설명가능 이상탐지 기법, 표형 데이터 벤치마크</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2609.03941'>Headroom-Drift Replay: A Primitive for Principled Replay Control in GRPO</a></td><td>40</td><td>0</td><td>RL</td><td>GRPO의 replay를 headroom과 drift 두 기준으로 선별하는 경량 기법, agentic search에서 비용 절감</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2609.04105'>Hardware-Aware FP4 FlashAttention-4</a></td><td>40</td><td>0</td><td>LG</td><td>Blackwell FP4 텐서코어에 맞춘 attention 커널 최적화로 순전파 2배 이상 가속, 하드웨어 엔지니어링 기여</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2609.03891'>A hybrid pipeline for dynamic ontology-based semantic mapping</a></td><td>38</td><td>5</td><td>Embodied AI</td><td>온톨로지 기반 동적 semantic mapping 파이프라인으로 딥러닝적 novelty보다는 시스템 통합에 가까움</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2609.03102'>WireSeg-32K: A Physics-Grounded Synthetic Dataset for Wire Instance Segmentation</a></td><td>38</td><td>4</td><td>3D Vision</td><td>Cosserat-rod 물리 시뮬레이션 기반 wire instance segmentation synthetic dataset임. deformable linear object 인식은 로봇 조작과 연결되나 인식 벤치마크 성격이 강함.</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2609.04131'>Beyond Retrieval: Progressive Latent Memory Evolution for Streaming Video Understanding</a></td><td>38</td><td>4</td><td>Video</td><td>streaming video 이해를 위해 외부 메모리 검색 대신 progressive latent working memory로 내재화하는 프레임워크임. robot memory 우선 주제와 개념적으로 연관되나 일반 비디오 QA 도메인에 한정됨.</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2609.03341'>PointGT: Simultaneous Geometry and Texture Editing for Point-Based Representations</a></td><td>38</td><td>3</td><td>3D Vision</td><td>point-based representation에서 geometry와 texture를 동시 편집하는 방법임. object-centric 3D representation과 연관되나 응용은 그래픽스 편집 중심임.</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2609.03349'>P-CORE: Self-Supervised Surface Consistency for Point-Based Neural Editing</a></td><td>38</td><td>3</td><td>3D Vision</td><td>self-supervised surface consistency로 large deformation에 강인한 point-based 편집 방법임. 3D representation 우선 주제와 연관되나 그래픽스 편집 응용에 국한됨.</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2609.04005'>The Dually Flat Geometry of Planning as Inference</a></td><td>38</td><td>3</td><td>RL</td><td>planning-as-inference를 방문측도의 dually flat 정보기하로 재정식화해 선형 보상을 넘어선 일반 함수형으로 확장한 이론 연구로 RL 우선주제에 부합하는 일반화 가능한 프레임워크임</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2609.03495'>Spectral characteristics of autoencoder parameters as a vector representation of data</a></td><td>38</td><td>1</td><td>LG</td><td>오토인코더 파라미터의 특이값을 데이터 벡터 표현으로 쓸 수 있음을 이론·실험으로 보인 연구</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2609.03705'>Federated Causal Discovery via Regression-Directed Cumulants</a></td><td>38</td><td>1</td><td>LG</td><td>고차 cumulant를 이용한 federated LiNGAM causal discovery 알고리즘군과 그 한계 분석</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2609.04090'>Conditioning Degenerate Diffusion Models</a></td><td>38</td><td>1</td><td>LG</td><td>causal optimal transport로 특이 diffusion coefficient 하의 조건부 생성을 정식화한 이론 논문</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2609.03090'>The Gradient Does Not See Rank: Rank-Indifference in Matrix-CODI on ProsQA</a></td><td>38</td><td>0</td><td>LG</td><td>latent reasoning matrix의 rank가 정확도와 무관함을 보인 부정적 결과 논문, 로봇과 무관</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2609.03150'>Routing Is Not Enough: Diagnosing Intra-Adapter Subspace Contention in MoE+LoRA Fine-Tuning</a></td><td>38</td><td>0</td><td>NLP</td><td>MoE+LoRA 멀티도메인 파인튜닝의 negative transfer를 진단하고 완화하는 기법</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2609.03878'>Differentiable Interval Bottlenecks for Interpretable Anomaly Detection in Numerical Data</a></td><td>38</td><td>0</td><td>LG</td><td>구간 멤버십으로 구조화된 latent bottleneck을 갖는 설명가능 이상탐지 오토인코더</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2609.03079'>LeanStream: A Speculate-and-Refine Streaming Framework for Efficient on-Device LLM Inference</a></td><td>36</td><td>1</td><td>LG</td><td>on-device LLM 추론을 위한 speculate-and-refine 스트리밍 시스템으로 경량화 위주의 엔지니어링 기여</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2609.03427'>TraveL: Transformer-based Multi-view Path Distributional Representation Learning</a></td><td>36</td><td>1</td><td>LG</td><td>도로망 경로의 분포적 표현학습으로 여행 행태를 모델링, 로봇 내비게이션과는 다른 인간 교통 응용</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2609.03528'>LeanGRPO: Eliminating Redundant Recomputation in Diffusion RL</a></td><td>36</td><td>1</td><td>LG</td><td>diffusion RL 롤아웃과 업데이트의 중복 재계산을 제거하는 시스템 최적화, 이미지·비디오 생성 모델 학습 효율화 위주</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2609.04026'>Stable and Scalable Bundle Adjustment of Holistic 3D Structures</a></td><td>35</td><td>4</td><td>3D Vision</td><td>점·선을 넘어 평면성·평행성 등 고차 기하 제약을 통합한 bundle adjustment 프레임워크임. 로봇 SLAM·매핑에 유용한 기초 기하 알고리즘 개선이나 응용은 일반 3D vision임.</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2609.03334'>Laplacian Frequency Hierarchies for Efficient 3D Gaussian Splatting Training</a></td><td>35</td><td>3</td><td>3D Vision</td><td>Laplacian frequency 분해로 3DGS 학습 속도를 높이는 coarse-to-fine 기법임. 3DGS 우선 주제와 연관되나 plug-and-play 가속에 그치는 incremental engineering임.</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2609.03429'>When Do Frozen VLMs Respond to Image-Free Object-Token Edits? An Answer-Key-Free Protocol and What It Reveals</a></td><td>35</td><td>3</td><td>Multimodal</td><td>object-level token을 편집해 frozen VLM의 what-if 반응을 측정하는 counterfactual probing 프로토콜임. causal/counterfactual reasoning 우선 주제와 개념적으로 연관되나 원격탐사 VQA 도메인에 국한됨.</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2609.02988'>Mesh-Native Physics-Informed Graph Surrogates for TCAD-in-the-Loop Design Space Exploration</a></td><td>35</td><td>0</td><td>LG</td><td>반도체 소자 시뮬레이션용 physics-informed GNN surrogate로 로봇과 무관</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2609.03308'>Risk and Anomaly Identification for Distribution Network Optimal Operation Based on Reinforcement Learning and Uncertainty Quantification</a></td><td>34</td><td>1</td><td>RL</td><td>배전망 운영을 위한 불확실성 인지 강화학습 프레임워크, 로봇과 무관한 전력망 응용</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2609.03763'>From Nowcasting to Forecasting: Adapting a Reanalysis-Trained</a></td><td>34</td><td>0</td><td>LG</td><td>conditional flow matching으로 관측 기반 구름 예보를 12시간까지 확장한 기상 모델</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2609.03937'>RATL: Learning from Retrieved Residuals for Robust Multivariate Time-Series Forecasting</a></td><td>34</td><td>0</td><td>LG</td><td>과거 잔차를 retrieval-augmented로 활용하는 다변량 시계열 예측 플러그인 기법</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2609.04007'>RobustSeiz: An Open-Source Framework for Benchmarking the Robustness of EEG Seizure Detection Models</a></td><td>34</td><td>0</td><td>LG</td><td>EEG 발작 탐지기의 분포 변화 강건성을 표준화 평가하는 오픈소스 벤치마크</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2609.03392'>Programming and execution of skill-based human-robot-crane collaborative tasks</a></td><td>33</td><td>5</td><td>Manipulation</td><td>CAD 기반 스킬 프로그래밍과 behavior tree로 사람-로봇-크레인 협동 조립 작업을 실행하는 산업 응용 시스템</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2609.03177'>Frontier LLMs are effective batch optimizers: Assessing reasoning models in continuous and discrete settings</a></td><td>33</td><td>1</td><td>LG</td><td>frontier LLM을 batch optimizer로 평가한 실증 연구, 새로운 방법론이라기보다 분석 논문</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2609.04018'>A location-invariant estimator of extremal quantile treatment effects for heavy-tailed distributions</a></td><td>33</td><td>1</td><td>LG</td><td>heavy-tailed 분포에서 위치 불변 극단 quantile treatment effect 추정량을 제안한 인과추론 이론 논문</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2609.03100'>Distilling deep optical flow stereo methods to retrieve dense three-dimensional wind fields</a></td><td>33</td><td>0</td><td>CV</td><td>위성 바람장 추정을 위한 stereo optical flow distillation, 원격탐사 응용</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2609.03265'>Selective Hypergraph Refinement for Frozen Graph Clustering</a></td><td>33</td><td>0</td><td>LG</td><td>학습이 끝난 그래프 클러스터링 결과를 hypergraph로 후처리 개선하는 기법, 개선폭이 작음</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2609.03504'>Restricted Eigenvalues Beyond Gaussian Width: Threshold Occupancy under Heavy Tails</a></td><td>33</td><td>0</td><td>LG</td><td>heavy-tailed 설계에서 restricted eigenvalue 이론의 open problem에 반례를 제시한 순수 통계 이론 논문</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2609.03662'>Extracting Forgotten Prompts from Targeted Unlearned Models</a></td><td>33</td><td>0</td><td>NLP</td><td>unlearning된 모델에서 잊혀진 프롬프트 자체를 복원하는 새로운 공격 기법</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2609.03762'>Projected Riemannian Gradient Descent for the Bures-Wasserstein Barycenter: Dimension-Independent Linear Convergence at Unit Step Size</a></td><td>33</td><td>0</td><td>LG</td><td>Bures-Wasserstein barycenter 계산을 위한 unit-step 리만 경사하강법의 차원독립 수렴 이론, 순수 최적화 이론</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2609.03851'>Pushing the (Decision) Boundaries: Dynamically Calibrating Differentially Private Noise to Explainability in Federated Learning</a></td><td>33</td><td>0</td><td>LG</td><td>federated learning에서 설명가능성 신호로 DP 노이즈를 동적 조정하는 의료영상 응용 연구</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2609.04113'>Constant regret in general games via higher-order optimism</a></td><td>33</td><td>0</td><td>LG</td><td>N인 일반게임에서 상수 후회를 보장하는 uncoupled 학습 알고리즘, 순수 게임이론</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2609.03680'>DropClick: Semi-Automated One-Click Segmentation for Agricultural Robotic Data</a></td><td>32</td><td>4</td><td>Manipulation</td><td>농업 로봇 데이터용 one-click segmentation 라벨링 도구임. robotics 응용이지만 어노테이션 도구 수준의 incremental 기여임.</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2609.03720'>RoughSense: Lightweight Terrain-Induced Rover Vibration Prediction Using Point Clouds and IMU Feedback</a></td><td>32</td><td>4</td><td>Navigation</td><td>포인트클라우드와 IMU로 지형 진동을 예측하는 경량 traversability 기법으로 새로운 학습 패러다임은 아님</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2609.03818'>CauseCollab: Causal Unified and Modality-Agnostic Network for Heterogeneous Collaborative Perception</a></td><td>32</td><td>4</td><td>3D Vision</td><td>이종 센서 모달리티 간 협업 인지를 인과적 표현학습으로 정렬한 V2X 협업인지 연구로 모달리티 격차가 큰 시나리오에서 성능 향상을 보였고 embodied perception과 맞닿음</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2609.03255'>Establishing a Dynamic Multimodal HRI Dataset for Engagement Analysis with a Humanoid Robot</a></td><td>30</td><td>4</td><td>Embodied AI</td><td>생리신호를 포함한 인간-로봇 상호작용 참여도 분석용 데이터 수집 프로토콜 제안, 아직 방법론 없이 실험설계 단계</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2609.03761'>Robot Aware Computational Design of Object Specific Passive Grippers for Additive Manufacturing</a></td><td>30</td><td>4</td><td>Manipulation</td><td>객체별 수동 그리퍼를 자동 생성하는 제조 파이프라인으로 학습 기반 방법이 아님</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2609.03912'>Lose the Order, Keep the Hierarchy: Deordering HTN Plans</a></td><td>30</td><td>4</td><td>RL</td><td>HTN 계획에서 불필요한 순서 제약을 제거하는 deordering 기법으로 TAMP의 계층적 계획 후처리에 해당하나 클래식 플래닝 벤치마크에 그침</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2609.03447'>STARS-GS: Structure-Aware Regularized Gaussian Splatting for Large-Scale Aerial Surface Reconstruction</a></td><td>30</td><td>3</td><td>3D Vision</td><td>대규모 항공 표면 재구성을 위한 구조 인지 3DGS 정규화임. 3D representation 우선 주제와 연관되나 지도 제작 도메인의 incremental engineering 기여임.</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2609.03534'>TruncGradGS: Improved 3D Gaussian Splatting via Truncated Gradient Updates</a></td><td>30</td><td>3</td><td>3D Vision</td><td>3DGS의 gradient vanishing 문제를 truncated gradient로 해결하는 최적화 기법임. 3DGS 우선 주제와 연관되나 최적화 개선에 그치는 incremental 기여임.</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2609.03694'>Observation-Conditioned Latent Energy Priors for Sparse Implicit Neural Shape Completion</a></td><td>30</td><td>3</td><td>3D Vision</td><td>sparse 관측에서 implicit shape completion을 개선하는 observation-conditioned energy prior임. object-centric 3D representation과 연관되나 의료 도메인에 국한됨.</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2609.03623'>QLAUN: A Research-Oriented, Robust, Agile, Modular, and Affordable Torque-Controlled Quadruped Robot</a></td><td>30</td><td>3</td><td>Robotics</td><td>3D 프린팅 쿼드루페드 하드웨어 플랫폼 소개로 학습 알고리즘 기여는 없음</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2609.02889'>Where Does Harness-Optimization Value Live? Localized Gains and the Budget-Splitting Trap in Self-Evolving LLM Agents</a></td><td>30</td><td>3</td><td>RL</td><td>ALFWorld에서 harness 슬롯별 최적화 기여도를 분석했지만 텍스트 기반 agent 연구로 실로봇과는 거리가 있음</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2609.03158'>Who Speaks for the Pruned? Visual Token Pruning as Coverage Optimization</a></td><td>30</td><td>2</td><td>Multimodal</td><td>VLM visual token pruning을 coverage 최대화 문제로 재정의한 효율화 기법임. robotics 응용은 간접적임.</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2609.03206'>Learning to Zoom Efficiently with a Contrastive Curriculum</a></td><td>30</td><td>2</td><td>Multimodal</td><td>MLLM tool-use(zoom-in) 학습을 위한 contrastive intrinsic reward임. agent 효율화 기여이나 robotics와의 직접 연결은 약함.</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2609.03201'>MemoryLACE: Memory Lifecycle-Aware Consolidation and Evidence Retrieval</a></td><td>30</td><td>2</td><td>NLP</td><td>텍스트 증거의 병합·대체·모순 관계를 명시적으로 모델링하는 장기 메모리 프레임워크로 robot memory에 원리적으로 참고할 만하나 텍스트 대화 도메인에 한정됨</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2609.04177'>A Computationally Feasible Framework for Causal Probabilistic Explanation</a></td><td>30</td><td>2</td><td>AI</td><td>actual causality와 Pearl의 확률적 인과이론을 결합해 계산 가능한 인과적 설명 프레임워크를 제시한 연구로 counterfactual reasoning 일반 이론으로서 가치 있으나 로봇 응용은 없음</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2609.03350'>From Zero to Hero: An Open LLM Ecosystem for Armenian</a></td><td>30</td><td>0</td><td>NLP</td><td>저자원 아르메니아어 LLM 생태계 구축 논문, 언어자원 기여 위주</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2609.03464'>Mind the Gap: Robustness Risks in PII Detection Systems</a></td><td>30</td><td>0</td><td>NLP</td><td>PII 탐지 시스템의 분포 변화 강건성을 스트레스 테스트한 벤치마크 논문</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2609.03505'>An Adversarial Zero-Shot Learning Approach for Anomaly Detection in Multivariate IoT Traffic Data</a></td><td>30</td><td>0</td><td>CV</td><td>적대적 학습 기반 zero-shot 도메인 적응 IoT 이상탐지, 로봇과 무관</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2609.03809'>A Peer-Relative Representation Learning Framework for Energy Inefficiency Identification in Mobile Network Sites</a></td><td>30</td><td>0</td><td>LG</td><td>통신기지국 에너지 비효율을 비지도 peer-relative 임베딩으로 탐지하는 응용 연구</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2609.03972'>OSR: Output Space Redistribution for Adaptive Label Removal in Classification Models</a></td><td>30</td><td>0</td><td>LG</td><td>출력공간 재분배로 재학습 없이 라벨 제거를 근사하는 분류 모델 유지보수 기법</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2609.03675'>CoFiE: Coarse-to-Fine Evidence Selection for Efficient Streaming Video Understanding</a></td><td>28</td><td>3</td><td>Video</td><td>streaming video 이해를 위한 coarse-to-fine evidence selection 효율화 방법임. 지연시간 감소가 robot 스트리밍 지각과 간접 연관됨.</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2609.03677'>Understanding Autonomous Driving Datasets by Describing Differences between Image Subsets in Natural Language</a></td><td>28</td><td>3</td><td>Embodied AI</td><td>자율주행 데이터셋 subset 간 차이를 자연어로 기술하는 데이터 분석 도구임. robotics 태그가 있으나 핵심 기여는 데이터 introspection에 그침.</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2609.03995'>Catalogue Photography as a Cold Start: Toward Deployable Carbide Burr Recognition</a></td><td>28</td><td>3</td><td>CV</td><td>카탈로그 사진만으로 산업 부품 인식 콜드스타트를 분석한 연구임. robotics 태그가 있으나 핵심은 분류·검색 도메인 전이 분석에 그침.</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2609.03630'>Local Path Planning and Obstacle Avoidance for an Omnicopter Platform</a></td><td>28</td><td>3</td><td>Navigation</td><td>6D DWA 확장을 통한 UAV 지역 경로계획으로 고전적 제어 기법의 engineering 개선에 가까움</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2609.03563'>FlashRender: Few-Step Generative Rendering via Camera-Controlled Video MeanFlow</a></td><td>28</td><td>2</td><td>3D Vision</td><td>few-step camera-controlled generative rendering 방법임. novel view synthesis 효율화로 robotics와 간접적으로만 연관됨.</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2609.03915'>RuleMem: Active Rule Memory for Long-Term Conversational Agents</a></td><td>28</td><td>2</td><td>NLP</td><td>대화 이력에서 재사용 가능한 규칙을 귀납해 검색·추론을 능동적으로 이끄는 메모리 프레임워크로 robot memory 설계 원리로 일부 참고 가능하나 텍스트 QA 도메인에 국한됨</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2609.04141'>Efficient Test-Time Adaptation through Human-AI Interaction</a></td><td>28</td><td>2</td><td>AI</td><td>사용자와의 반복 상호작용으로 개인화 기준을 학습하는 test-time adaptation 프레임워크로 우선주제인 test-time optimization과 맥락은 닿지만 글쓰기·시각창작 도메인이라 로봇 응용은 아님</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2609.02996'>Evaluating Graph Neural Networks for Change-Criticality Classification in Maritime Navigation Charts</a></td><td>28</td><td>1</td><td>CV</td><td>해도 변경의 항행 위험도 분류를 위한 GNN 적용 연구로 벤치마크 성격이 강하고 로봇 내비게이션과는 다른 문제</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2609.03231'>The 2026 PNPL Competition: Word Classification and Efficient Cross-Subject Generalisation in LibriBrain100</a></td><td>28</td><td>1</td><td>NLP</td><td>비침습 speech decoding BCI 경진대회 소개 논문으로 새로운 방법론 기여는 제한적</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2609.02902'>RL-ADA: A World-Feedback Framework for Adversarially Robust Enterprise Dialogue Agents</a></td><td>28</td><td>1</td><td>RL</td><td>고객 상담 에이전트를 world feedback 보상으로 공진화시키는 adversarial RL 프레임워크로 로봇 응용과는 거리가 있음</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2609.04108'>Sequential Beats Joint: On the Interplay between On-Policy Distillation and RLVR</a></td><td>28</td><td>1</td><td>RL</td><td>on-policy distillation 후 RL을 순차 적용하는 것이 결합 최적화보다 우수함을 밝힌 LLM post-training 연구로 VLA post-training 설계에 참고할 원리적 시사점이 있음</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2609.02984'>From Euclidean to Graph-Structured Data: A Survey of Collaborative Learning</a></td><td>28</td><td>0</td><td>LG</td><td>federated·decentralized graph learning survey로 새로운 실험 기여 없음</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2609.03180'>Portable Causal Fairness Across Synthetic Data Generator Families</a></td><td>28</td><td>0</td><td>LG</td><td>synthetic data generator 계열 간 causal fairness 이식성을 검증한 응용 연구</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2609.03507'>LongCounsel-8: A Benchmark Suite for Longitudinal Depression Tracking from Multi-Session Counseling Dialogues</a></td><td>28</td><td>0</td><td>NLP</td><td>다세션 상담 대화 기반 우울증 추적 벤치마크 데이터셋 구축 논문</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2609.03938'>Towards Numerical TOHTN Planning with SMT-based HTN-SAT Encoding</a></td><td>26</td><td>3</td><td>RL</td><td>수치 fluent를 다루는 HTN 계획을 SMT 기반으로 확장한 연구로 TAMP 관련 formulation이지만 벤치마크 수준의 초기 결과에 그침</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2609.04014'>InSituMeasure: Probing Situated Measurement Grounding in Industrial Scenes with Multimodal Large Language Models</a></td><td>26</td><td>3</td><td>Embodied AI</td><td>산업 현장 계기판 판독이라는 situated measurement grounding을 MLLM으로 평가한 벤치마크로 embodied spatial reasoning과 맞닿지만 순수 벤치마크 논문임</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2609.03438'>Do GUI Agents Know When Not to Act? Enabling Conflict-Aware Termination for Multimodal GUI Agents</a></td><td>26</td><td>2</td><td>Embodied AI</td><td>GUI agent가 모순된 지시에서 행동을 멈추는 능력을 다뤄 failure-aware termination과 맥락은 닿지만 화면 조작 도메인이라 로봇 실체화와는 거리 있음</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2609.03973'>Common-Witness Certificates and Sharp Feature Bounds for Counterfactual Image Auditing</a></td><td>26</td><td>2</td><td>AI</td><td>이미지 편집기의 국소적 타당성이 전역적 일관성을 보장하지 않는 문제를 common witness 이론으로 정식화한 counterfactual auditing 연구로 일반화 가능한 이론이지만 로봇 응용은 없음</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2609.03366'>Accountable AI with Grounded, Faithful, Consistent, Actionable Rationales: A Case Study in Clinical Trial Matching with VERDICT</a></td><td>26</td><td>1</td><td>NLP</td><td>LLM 결정을 SMT 솔버로 변환해 정책 일관성과 신뢰 가능한 rationale을 확보한 neurosymbolic 접근으로 임상 도메인에 국한됨</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2609.03699'>Predictive Zonotope Reduction: Precise Runtime Monitoring under Uncertainty</a></td><td>25</td><td>4</td><td>RL</td><td>불확실성 인지 zonotope 축소를 MPC로 최적화한 런타임 안전 모니터링 기법으로 로봇 학습과는 거리가 있음</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2609.03378'>When Depth Hurts: Reliability-Aware Geometry Distillation for Depth-Free RGB-D Salient Object Detection</a></td><td>25</td><td>2</td><td>CV</td><td>depth distillation 기반 depth-free RGB-D salient object detection임. 로봇 지각과 간접적으로만 연관됨.</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2609.03406'>Neural-Collapse-guided Task-Free Continual Anomaly Detection</a></td><td>25</td><td>2</td><td>CV</td><td>neural-collapse 기반 task-free continual anomaly detection임. 산업 검사 도메인으로 robotics와 간접적으로만 연관됨.</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2609.03516'>Residual Optimal Transport-Based Experts Collaboration Towards Modality-Aware Infrared-Visible Object Detection</a></td><td>25</td><td>2</td><td>CV</td><td>결측 모달리티에 대응하는 적외선-가시광 객체탐지 fusion 방법임. 로봇 지각과 간접 연관되나 embodied 맥락은 없음.</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2609.03639'>Stabilizing Camera-Controlled Novel View Synthesis at Inference Time</a></td><td>25</td><td>2</td><td>3D Vision</td><td>카메라 제어 novel view synthesis를 inference 시점에서 안정화하는 방법임. 3D/view synthesis와 연관되나 robotics 직접 연결은 약함.</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2609.03756'>ENEAS: Embedding-guided Neural Ensemble for Adaptive Segmentation</a></td><td>25</td><td>2</td><td>CV</td><td>text-promptable instance tracking·segmentation 방법으로 3D reconstruction 활용을 염두에 둠. robotics와의 직접 연결은 약함.</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2609.03820'>Select, Compress, Reinvest: A Controlled Study of Visual-Token Allocation in Long-Video MLLMs</a></td><td>25</td><td>2</td><td>Video</td><td>long-video MLLM의 frame selection·압축·재투자를 통제 비교한 연구임. 효율화 벤치마킹으로 robotics와 간접 연관됨.</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2609.04110'>The Shape of Time: Video-Token Contrast for Temporal Understanding in VideoLMs</a></td><td>25</td><td>2</td><td>Video</td><td>VideoLM의 시간 표현 학습을 위한 representation-level counterfactual contrastive objective임. 일반 video understanding 기여로 robotics 직접 연관은 약함.</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2609.03221'>Counterfactual Fairness Audits of Multi-Step Clinical LLM Agents Require a Measured Per-Action Instability Floor</a></td><td>25</td><td>1</td><td>NLP</td><td>임상 에이전트의 counterfactual flip rate가 재현 불안정성 바닥값 없이는 해석 불가함을 보인 방법론 연구로 counterfactual reasoning과는 결이 다름</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2609.03077'>Position: Unlabeled IS NOT Equal to No Human Supervision in Visual Learning</a></td><td>25</td><td>0</td><td>CV</td><td>unsupervised 용어의 개념적 모호성을 지적하는 position paper임. 실험적 기여 없고 robotics 관련성도 낮음.</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2609.03384'>FoRIS: Progressive Foreground Refinement for Training-Free In-Context Segmentation</a></td><td>25</td><td>0</td><td>CV</td><td>training-free in-context segmentation의 coarse-to-fine refinement 방법임. robotics와 무관한 일반 세그멘테이션 기여임.</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2609.03603'>Neural-Network Maxent: a general extension with learned nonlinearity, applied to time-series for Desert Locust distribution modelling</a></td><td>25</td><td>0</td><td>LG</td><td>GRU 기반 비선형 Maxent로 사막메뚜기 서식지 분포를 예측한 생태 응용 논문</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2609.03493'>Making Every Tool Call Count: Necessary Tool-Evidence Path Rewards for Agentic Vision-Language Models</a></td><td>24</td><td>2</td><td>Multimodal</td><td>agentic VLM의 tool call을 필요한 증거 경로로 보상 설계한 연구로 VLA와는 다른 tool-use 최적화에 그침</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2609.04094'>DRACO: Fine-Grained Credit Assignment with Dynamic Rubrics for Long-Horizon Agent Training</a></td><td>24</td><td>2</td><td>RL</td><td>검증기 없는 장기 호라이즌 에이전트 학습에서 rubric 점수를 스텝별로 재분배하는 credit assignment 기법으로 skill chaining 학습과 개념은 닿으나 코딩 에이전트 도메인에 한정됨</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2609.02893'>Probe Generalization as Subspace Selection for OOD Deception Detection</a></td><td>24</td><td>1</td><td>NLP</td><td>주성분 부분공간 선택으로 기만 탐지 probe의 OOD 전이를 개선한 해석가능성 연구임</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2609.03426'>Lngram v2: Latent N-Gram Memory with Interpretable Discrete Representations</a></td><td>24</td><td>1</td><td>Multimodal</td><td>이산 latent n-gram 메모리를 백본 폭과 분리해 스케일링한 VLM용 조회 메커니즘으로 robot memory에 원리적 참고 가능성은 있으나 실증은 VLM 언어모델링에 국한됨</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2609.03340'>Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory</a></td><td>24</td><td>1</td><td>AI</td><td>분산 LLM-agent의 plan staleness 검증 프로토콜로 robot memory와는 별개인 소프트웨어 시스템 문제임</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2609.03546'>Dalek: A Constructive Agent Machine</a></td><td>24</td><td>1</td><td>AI</td><td>von Neumann 자기복제 자동자를 확장해 LLM 기반 에이전트의 자기진화·자기재생산 구조를 설계한 개념적 연구로 흥미롭지만 실증이 약하고 로봇 적용은 없음</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2609.03586'>The Attention Triangle in Audio-Video Models</a></td><td>24</td><td>1</td><td>Video</td><td>오디오-비디오 확산모델의 cross-modal attention이 의미 누출을 일으키는 경로를 분석한 연구로 멀티모달 표현 이해에 기여하나 robotics 응용은 없음</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2609.03337'>A Large Open Multi-Energy Corpus of Soil Compaction Tests, with Machine-Learning Baselines</a></td><td>24</td><td>0</td><td>LG</td><td>대규모 토질 압축시험 데이터셋 공개와 ML 베이스라인, 토목공학 응용</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2609.02899'>Contamination Inflates Scores but Rarely Reorders Large Language Model Leaderboards</a></td><td>24</td><td>0</td><td>NLP</td><td>벤치마크 오염이 LLM 리더보드 순위를 거의 바꾸지 않음을 정량화한 방법론 연구로 로봇과 무관함</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2609.03895'>Concept of a Sensor Test Environment for Dusty Agricultural Conditions</a></td><td>22</td><td>3</td><td>Embodied AI</td><td>먼지 환경 농업 로봇 센서 테스트베드 구축 개념 제안임. robotics 응용이지만 기술적 기여 없는 초기 concept paper임.</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2609.03758'>A Multi-Vine Soft Robot Enabling Accessible Working Channel and Steering</a></td><td>22</td><td>2</td><td>Robotics</td><td>의료용 vine robot의 다중 채널 스티어링 하드웨어 설계로 학습 요소가 없음</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2609.03753'>SimSkill: A Lifelong Learning AI Agent for Autonomous Mastery of Traffic Simulation</a></td><td>22</td><td>2</td><td>RL</td><td>교통 시뮬레이션 숙달을 위해 episodic·procedural·semantic memory를 축적하는 자기진화 에이전트로 robot memory 설계와 개념은 유사하나 응용 도메인이 로봇이 아님</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2609.03148'>Large Language Models in Resolving Contextual Knowledge Conflicts</a></td><td>22</td><td>1</td><td>NLP</td><td>문맥 내 지식 충돌 6유형 분류와 해결을 위한 steering 기법으로 causal reasoning과는 다른 텍스트 층위 연구임</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2609.03467'>When Users Don&#x27;t Ask: Benchmarking Context-Driven Memory Retrieval in Conversational Agents</a></td><td>22</td><td>1</td><td>NLP</td><td>암묵적 질의에서 대화형 메모리 검색의 격차를 드러낸 벤치마크로 robot memory 설계에 참고할 통찰은 제한적임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2609.04063'>Spurious Advantage Hidden in GRPO</a></td><td>22</td><td>1</td><td>RL</td><td>GRPO의 advantage 추정이 정답을 추측만 해도 높은 보상을 주는 spurious advantage 문제를 지적하고 부호 기반 재조정을 제안한 RL 알고리즘 개선 연구임</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2609.03106'>Scaling Laws, Tabular Data and Actuarial Ratemaking Models</a></td><td>22</td><td>0</td><td>LG</td><td>보험 정산 모델의 scaling law 실증 연구로 로봇과 무관</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2609.03457'>A Two-Stage Forecasting System for CPU Workload Prediction in Private Clouds</a></td><td>22</td><td>0</td><td>LG</td><td>클라우드 CPU 사용량 2단계 예측 시스템, 로봇과 무관한 인프라 응용</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2609.03970'>Automated Weld Seam Recognition and 3D Mapping for Robotic Post Processing Using Photogrammetry and Semantic Segmentation</a></td><td>20</td><td>3</td><td>CV</td><td>용접선 위치 추정을 위한 사진측량·semantic segmentation 파이프라인으로 산업 응용에 국한됨</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2609.04030'>IRWOZ 2.0: A Large Language Model-driven Dialogue Dataset for Industrial Robot Conversations</a></td><td>20</td><td>3</td><td>Embodied AI</td><td>산업용 로봇 대화 데이터셋을 LLM으로 정제·확장한 연구로 HRI 대화 품질 개선에 그치는 incremental 기여임</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2609.03585'>Text2Thermal: Physics-Aware Thermal Image Synthesis from Textual Priors</a></td><td>20</td><td>2</td><td>CV</td><td>텍스트 조건 물리 기반 열화상 이미지 합성임. 악조건 지각과 간접 연관되나 응용 중심 기여임.</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2609.03727'>Proactive Service Agents: A Unified Decision Framework, Methods, and Evaluation</a></td><td>20</td><td>2</td><td>Embodied AI</td><td>선제적 서비스 에이전트를 부분관측 순차의사결정으로 정식화한 서베이로 개입 시점 판단이라는 틀은 embodied decision-making과 닿지만 로봇 실증은 없음</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2609.03475'>SafeRestore: Detector-Relative Risk Certificates for Selective Industrial Image Restoration</a></td><td>20</td><td>1</td><td>CV</td><td>산업 이미지 복원의 detector-relative 위험 인증 프레임워크임. 산업 검사 맥락으로 간접 연관되나 통계적 방법론 중심 기여임.</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2609.03773'>RealCADBench: Benchmarking Parametric CAD Modeling from Industrial Design Intents</a></td><td>20</td><td>1</td><td>CV</td><td>산업 설계 의도 기반 parametric CAD 모델링 벤치마크임. robotics와 무관한 CAD 생성 평가 기여임.</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2609.02892'>Counterexamples as Feedback for Agent Self-Correction</a></td><td>20</td><td>1</td><td>NLP</td><td>정규식 합성에서 반례 피드백으로 multi-turn self-correction을 개선한 연구로 로봇 응용과는 무관함</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2609.03254'>What Else Needs Fixing? Exploring Cost-Effective Test-Time Compute for Revision Propagation in Artifacts Generated Through Conversation</a></td><td>20</td><td>1</td><td>NLP</td><td>대화로 생성된 산출물의 국소 수정 전파를 위한 비용 효율적 test-time compute 탐색 연구로 로봇 test-time optimization과는 도메인이 다름</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2609.03331'>FPCO-Dialog: A Multi-Turn False-Premise Benchmark for Correction and Cooperation in Vision-Language Models</a></td><td>20</td><td>1</td><td>Multimodal</td><td>반복되는 false premise에 대한 VLM의 교정·협력 행동을 평가하는 멀티턴 벤치마크로 시각-언어 상호작용 평가 관점에서만 소폭 참고 가능함</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2609.03487'>Pattern Over-Generalization of Knowledge Graph Embedding</a></td><td>20</td><td>1</td><td>LG</td><td>관계 표현의 dense linear transformation으로 패턴 과도일반화를 완화한 지식그래프 임베딩 기법으로 3D/scene representation과는 거리가 있음</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2609.03236'>Speculative Macro Commit for Faster Tool-Using Agents</a></td><td>20</td><td>1</td><td>NLP</td><td>tool-using LLM agent의 추측 실행 기반 지연시간 단축 기법으로 robotics와 무관한 시스템 엔지니어링 기여임</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2609.03834'>Semantic Bayesian World Models</a></td><td>20</td><td>1</td><td>World Model</td><td>지식그래프를 베이지안 신념 구조로 재해석한 비전 논문으로 world model이라는 이름과 달리 실증 없는 로드맵 수준이며 embodied 응용도 아님</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2609.03052'>IDSPACE: A Novel Document Generator for Reliable Evaluation of Digital Identity Verification Systems [Extended Technical Report]</a></td><td>20</td><td>0</td><td>CV</td><td>신원 확인 문서용 synthetic data 생성기임. robotics와 무관한 도메인 특화 엔지니어링 기여임.</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2609.03080'>Exemplar: Classical Priors Complement Frozen Features for Few-Shot Microscopy Segmentation at Native Resolution</a></td><td>20</td><td>0</td><td>CV</td><td>few-shot microscopy segmentation 방법임. robotics와 무관한 의료영상 도메인 기여임.</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2609.03139'>Beyond Small Patches: Black-Box Detection and Purification of Diverse Backdoor Triggers</a></td><td>20</td><td>0</td><td>CV</td><td>블랙박스 backdoor trigger 탐지·제거 방어 기법임. security 도메인으로 robotics 무관함.</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2609.03216'>ProgResViT: Progressive Resolution and Width for Adaptive Vision Transformers</a></td><td>20</td><td>0</td><td>CV</td><td>입력 적응형 ViT의 해상도·너비 조절 효율화 기법임. 순수 incremental engineering으로 robotics 무관함.</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2609.03261'>MedQA-MM: Shortcuts Behind Medical Visual Reasoning</a></td><td>20</td><td>0</td><td>Multimodal</td><td>의료 VQA의 shortcut·reasoning inflation을 분석한 벤치마크임. robotics 무관함.</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2609.03391'>Exploring the Potential of Contrastive Language-Image Pre-training for Multi-Source Remote Sensing Data</a></td><td>20</td><td>0</td><td>Multimodal</td><td>SAR·MSI·HSI를 포괄하는 원격탐사 CLIP 확장임. robotics 무관함.</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2609.03544'>SafeRI: Recognition and Intervention for Token-Level Safety Intervention in Large Vision Language Models</a></td><td>20</td><td>0</td><td>Multimodal</td><td>VLM의 토큰 단위 on-demand 안전성 개입 방법임. robotics 무관함.</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2609.03554'>WIDE: Wildcard Inference with Dynamic Expansion for Cross-Modal Generative Retrieval</a></td><td>20</td><td>0</td><td>Multimodal</td><td>cross-modal generative retrieval의 decoding hallucination 억제 기법임. robotics 무관함.</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2609.03629'>EraseSAE: Surgical Concept Erasure in Text-to-Video Diffusion Models via Sparse Autoencoders</a></td><td>20</td><td>0</td><td>Video</td><td>sparse autoencoder로 text-to-video diffusion에서 개념을 정밀 제거하는 방법임. robotics 무관함.</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2609.03655'>PL-SCEA: Reconfiguring Pretrained Attention for Few-Shot Industrial Anomaly Detection</a></td><td>20</td><td>0</td><td>CV</td><td>frozen VFM attention 재구성 기반 few-shot 산업 이상탐지임. robotics 무관함.</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2609.03796'>LLaDA-Image: Building Strong Image Generators with Fully Open Training Recipes</a></td><td>20</td><td>0</td><td>CV</td><td>완전 공개 학습 레시피 기반 이미지 생성기임. robotics 무관함.</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2609.04083'>CORE: Improving Compositional Reasoning in MLLM Embedding via Reranker Distillation</a></td><td>20</td><td>0</td><td>Multimodal</td><td>MLLM 임베딩의 compositional reasoning 개선을 위한 reranker distillation임. robotics 무관함.</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2609.03239'>B2B Customer Conversion Prediction: A Document Representation, Graph Theory, and CatBoost Driven Methodology</a></td><td>20</td><td>0</td><td>LG</td><td>B2B 고객 전환 예측을 위한 CatBoost 기반 실무 프레임워크, 연구적 기여 낮음</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2609.03790'>Landmark-Based Discrimination of Injury-Associated Athlete-Sessions from Minute-Resolution Multimodal Football Monitoring Data</a></td><td>20</td><td>0</td><td>LG</td><td>분단위 다중모달 축구 모니터링 데이터로 부상 세션을 판별하는 스포츠 분석 연구</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2609.02897'>Margins, Not Windows: Training-Free Per-Step Lossy Speculative Decoding</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 추론 가속을 위한 학습-불필요 적응형 speculative decoding 기법으로 로봇 응용과 무관함</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2609.02942'>Judging LLM-as-a-Judge: Concerning Rubric Artifacts in LLM-based Automated Text Generation Evaluation</a></td><td>20</td><td>0</td><td>NLP</td><td>rubric 텍스트만으로도 판정 결과가 예측되는 LLM judge의 취약점을 드러낸 분석 연구임</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2609.03788'>A Reverse Sign Language Dictionary: Open-Vocabulary Sign Recognition from Continuous Signing via Video Captioning and Description Retrieval</a></td><td>18</td><td>2</td><td>Multimodal</td><td>연속 수어에서 캡셔닝·검색으로 open-vocabulary 수어 인식을 수행함. RO-MAN 워크숍 발표이나 핵심 기여는 robotics와 무관함.</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2609.03704'>Toward an~Integrated Cognitive--Ergonomic Architecture for~Human--Machine Interaction: Combining Cognitive Models with~Human Factors Ergonomics</a></td><td>18</td><td>2</td><td>Embodied AI</td><td>기존 인지 아키텍처를 종합한 HMI 프레임워크 제안으로 실험적 검증이나 새로운 학습 방법은 없음</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2609.03794'>A comparative study on the accuracy &amp; repeatability of mobile robotic platforms for the delivery of precision NDE measurement</a></td><td>18</td><td>2</td><td>Robotics</td><td>5개 상용 모바일 플랫폼의 위치 정확도를 비교한 벤치마킹 연구로 학습적 기여가 없음</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2609.03883'>Inferring Affective Consciousness in an Artificial Agent: A Case Study</a></td><td>18</td><td>2</td><td>AI</td><td>쾌락적 장소선호 행동을 보이는 결정론적 인공 에이전트로 정동적 의식 문제를 논한 철학적 사례연구로 embodied agent의 내재적 욕구 표현과 개념은 닿으나 실증 로봇 연구는 아님</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2609.04021'>FLY-EVAL++: An Evidence-Driven Evaluation Protocol for Safety-Constrained Flight Prediction with Large Language Models</a></td><td>18</td><td>2</td><td>AI</td><td>비행 궤적·자세 예측 LLM의 안전 제약 위반을 측정하는 평가 프로토콜로 physics-grounded safety 평가는 참고할 만하나 로봇 응용은 아님</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2609.03707'>Counterfactual Routing Using Integer Programming with Constraint Generation</a></td><td>18</td><td>1</td><td>AI</td><td>경로 계획의 counterfactual 설명을 정수계획법으로 푸는 대회 제출 논문으로 counterfactual reasoning과 맞닿지만 로봇이 아닌 도로망 라우팅에 국한됨</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2609.03797'>Transfiver: Human-AI Co-Inference through a Shared Editable State</a></td><td>18</td><td>1</td><td>AI</td><td>인간-AI가 공유 편집 상태를 통해 추론을 조율하는 아키텍처로 로봇 대상 memory·correction 설계에 참고는 되나 직접 응용은 없음</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2609.04166'>From Deceptive Outputs to Deceptive Mechanisms: A Causal Framework for Language-Model Deception Research</a></td><td>18</td><td>1</td><td>NLP</td><td>언어모델의 기만적 출력과 기만 메커니즘을 구분하는 인과적 분류체계로 counterfactual reasoning 도구로는 흥미로우나 로봇 응용은 없음</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2609.03085'>Solving the Needle-in-a-Haystack Problem in Mammography Vision-Language Model with Differentiable Subset Sampling</a></td><td>18</td><td>0</td><td>Multimodal</td><td>mammography 특화 CLIP 스타일 VLM임. robotics 무관, 의료 fine-tuning 위주 기여임.</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2609.03445'>OCR-EDR: Rendering-Aware Diagnosis and Repair for Closed-Loop OCR Improvement</a></td><td>18</td><td>0</td><td>CV</td><td>rendering 기반 OCR 오류 진단·복구 프레임워크임. robotics와 무관함.</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2609.03453'>Preprocessing Failure and Adversarial Detection in Depthwise-Separable Edge Vision Systems</a></td><td>18</td><td>0</td><td>CV</td><td>edge vision 아키텍처별 adversarial 전처리 방어 평가임. security 도메인으로 robotics 무관함.</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2609.03688'>ToPO: Token-Conditioned Preference Routing for Attention-Based Latent Diffusion Models</a></td><td>18</td><td>0</td><td>CV</td><td>attention 기반 latent diffusion의 token-conditioned preference routing 기법임. robotics 무관함.</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2609.03740'>Fill My Mirror: Geometry-Constrained Mirror Inpainting</a></td><td>18</td><td>0</td><td>CV</td><td>장면 기하 제약을 활용한 거울 인페인팅 방법임. robotics 무관함.</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2609.03811'>VisCAD: A Foundation Model Suite with Multimodal Industrial CAD Intelligence</a></td><td>18</td><td>0</td><td>CV</td><td>산업 CAD 지능을 위한 foundation model suite임. robotics 무관함.</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2609.04031'>DSAQuant: Denoising-Stage-Aligned Quantization-Aware Training for Video Generation</a></td><td>18</td><td>0</td><td>Video</td><td>비디오 diffusion의 denoising 단계별 quantization-aware training 방법임. robotics 무관함.</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2609.03213'>LLMs Learn Better In-Context from Rules than from Examples</a></td><td>18</td><td>0</td><td>NLP</td><td>LLM이 예시보다 규칙 설명에서 더 잘 학습한다는 in-context learning 비교 연구로 로봇과 무관함</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2609.03503'>PPO-STGNN: A Proximal Policy Optimization Approach with Spatio-Temporal Graph Neural Networks for DAG Task Scheduling in Cloud-Edge-End Computing</a></td><td>16</td><td>1</td><td>RL</td><td>cloud-edge DAG 스케줄링에 PPO와 spatio-temporal GNN을 결합한 응용 RL 연구로 robot learning과는 별개 도메인임</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2609.03322'>How Perturbations Propagate: A Multi-Level Analysis of Robustness in Large Language Models</a></td><td>16</td><td>0</td><td>NLP</td><td>GPT-2·Qwen에서 perturbation이 표현 기하와 attention head에 미치는 영향을 다층적으로 분석한 연구로 로봇과 무관함</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2609.03478'>AutoGraphForge: Towards Automated Graph Theory Discovery</a></td><td>16</td><td>0</td><td>AI</td><td>그래프 이론 추측을 자동 생성·증명하는 파이프라인으로 robotics 관련성 없음</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2609.04103'>Corner Cases: Headland Coverage Path Planning for Autonomous Driving in Arable Farming</a></td><td>15</td><td>2</td><td>Navigation</td><td>농경지 코너부 커버리지 경로계획 개선으로 학습 요소 없는 전통적 경로계획 연구임</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2609.03109'>SLIDEFORGE: An LLM Agent for Controllable Editing of Slides as Structured Artifacts</a></td><td>15</td><td>0</td><td>NLP</td><td>슬라이드 편집 LLM agent임. robotics와 무관함.</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2609.03233'>Counting Animals in Camera-Traps Image Sequences without Count Labels: Winning Solution to the iWildCam 2021 Challenge</a></td><td>15</td><td>0</td><td>CV</td><td>camera-trap 동물 개체수 세기 대회 우승 솔루션임. robotics 무관함.</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2609.03258'>An Ensemble-Based Self-Taught Learning Approach for Parking Space Classification Under Limited Data</a></td><td>15</td><td>0</td><td>CV</td><td>주차 공간 분류를 위한 ensemble self-taught learning임. robotics 무관함.</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2609.03415'>Mudragen: Geometrically Supervised Generation of Interacting Two-Hand Mudras for Preserving Indian Classical Dance Heritage</a></td><td>15</td><td>0</td><td>CV</td><td>인도 고전무용 손동작 생성 diffusion 모델임. robotics와 무관한 문화유산 도메인 기여임.</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2609.03446'>Preserving Knowledge across Space and Time for Continual Video Deepfake Detection</a></td><td>15</td><td>0</td><td>CV</td><td>spatiotemporal 주파수 분리 기반 continual video deepfake 탐지임. robotics와 무관함.</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2609.03463'>BMCTrack-d: Pig re-identification and tracking via back marks in challenging camera settings</a></td><td>15</td><td>0</td><td>CV</td><td>back mark 기반 돼지 재식별 추적 방법임. robotics와 무관함.</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2609.03520'>Neural Video Compression Based on Deformable Temporal Alignment and Difference-aware Fusion</a></td><td>15</td><td>0</td><td>Video</td><td>deformable temporal alignment 기반 neural video compression임. robotics 무관함.</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2609.03569'>Occlusion-Robust Multimodal Emotion Recognition in VR via Fusion of Facial Images and EMG</a></td><td>15</td><td>0</td><td>Multimodal</td><td>VR 환경에서 얼굴 영상과 EMG를 결합한 감정 인식임. robotics와 무관한 HCI 도메인 기여임.</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2609.03615'>Auditing Patient Privacy in Medical Generative Models: Scalable Memorization Detection with DeepSSIM++</a></td><td>15</td><td>0</td><td>CV</td><td>의료 생성모델의 환자 데이터 기억 여부를 감사하는 유사도 지표임. robotics 무관함.</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2609.03641'>Tree-Structured Vector Quantization For Efficient And Progressive Image Compression</a></td><td>15</td><td>0</td><td>CV</td><td>tree-structured vector quantization 기반 progressive 이미지 압축임. robotics 무관함.</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2609.03663'>Cross-Dataset Transfer and Reliability of Explainable Artificial Intelligence for RhythmFormer Remote Photoplethysmography</a></td><td>15</td><td>0</td><td>CV</td><td>원격 광용적맥파(rPPG) 모델의 설명가능성 신뢰도를 데이터셋 간 비교한 연구임. robotics 무관함.</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2609.03668'>ARCOS: Zero-shot Boundary Localization for Corneal Layer Segmentation Across Optical Coherence Tomography Devices</a></td><td>15</td><td>0</td><td>CV</td><td>각막 OCT 경계 분할을 위한 zero-shot 패치 기반 방법임. robotics와 무관한 의료영상 기여임.</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2609.03695'>SignSeek: Learning Transferable Representations for Sign Dictionary Retrieval</a></td><td>15</td><td>0</td><td>Multimodal</td><td>수어사전 검색을 위한 articulator masking 기반 표현학습임. robotics 무관함.</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2609.03813'>SPARK: Input-Conditioned Sparse Activation Modulation for Frozen DiT-based Super-Resolution</a></td><td>15</td><td>0</td><td>CV</td><td>frozen DiT super-resolution의 dominant channel 기반 경량 적응 방법임. robotics 무관함.</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2609.03829'>The impact of phase information for few-shot fine-grained image classification</a></td><td>15</td><td>0</td><td>CV</td><td>few-shot fine-grained 이미지 분류에서 위상 정보의 역할을 분석한 연구임. robotics 무관함.</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2609.03956'>RARF: Region-Aware Rectified Flows for 3D Brain MRI Inpainting</a></td><td>15</td><td>0</td><td>CV</td><td>3D 뇌 MRI 인페인팅을 위한 region-aware rectified flow임. robotics와 무관한 의료영상 기여임.</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2609.03985'>IchthyoNoma: Nomenclature and Context Sensitivity of Zero-Shot Biological Vision--Language Models for Bangladeshi Freshwater Fish Recognition</a></td><td>15</td><td>0</td><td>Multimodal</td><td>방글라데시 담수어 인식에서 zero-shot 생물학 VLM의 명명법·언어 민감도를 감사한 연구임. robotics 무관함.</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2609.04009'>The Blind Spot in 2D Infants&#x27; Pose Estimation:Robust Learning from Noisy Annotations</a></td><td>15</td><td>0</td><td>CV</td><td>신생아 자세추정에서 노이즈 라벨에 강인한 keypoint 선택 방법임. robotics 무관함.</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2609.04071'>TAP-Path: Task-Adaptive Structural and Token Pruning for Efficient and Trustworthy Pathology Foundation Models</a></td><td>15</td><td>0</td><td>CV</td><td>병리 foundation model의 task-adaptive 구조·토큰 pruning 압축 방법임. robotics 무관함.</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2609.04151'>Persistent Identity Preservation in Generative Image Models: A Benchmark and Evaluation System</a></td><td>15</td><td>0</td><td>CV</td><td>생성 이미지 모델의 정체성 보존을 다루는 벤치마크 및 평가 시스템임. robotics 무관함.</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2609.04183'>Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning</a></td><td>15</td><td>0</td><td>Multimodal</td><td>VLM 기반 transition event 발견을 통한 약지도 dense video captioning임. robotics 무관함.</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2609.04190'>One Editor, Many Edits: A Unified Training-Free Framework for Diverse Video Editing</a></td><td>15</td><td>0</td><td>Video</td><td>다양한 편집 패러다임을 통합한 training-free 비디오 편집 프레임워크임. robotics 무관함.</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2609.03770'>OBER+: Continuity-Aware Reporting and Traceable Continuous Improvement in Outcome-Based Education</a></td><td>15</td><td>0</td><td>LG</td><td>성과기반교육 이수 보고 체계의 연속성 규칙을 제안한 교육행정 논문</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2609.03801'>From Ordered Bernoulli Levels to Critical-Line Geometry: Integer Quantization, Bernoulli Residual Phase, and Prime-Power Spectra</a></td><td>15</td><td>0</td><td>LG</td><td>리만 제타함수 임계선과 정수 양자화를 연결한 수론적 탐구, ML 방법론 기여 없음</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2609.03005'>Unifying Conformal Language Tasks with In-Context Ensembles</a></td><td>15</td><td>0</td><td>NLP</td><td>conformal prediction 점수 함수를 in-context ensembling으로 자동화한 요약·추출 기법으로 로봇과 무관함</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2609.03160'>No country for old linguists: LLM-brain alignment underdetermines neural computation</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM-뇌 정합성이 메커니즘을 규명하지 못한다는 논평 논문으로 실험적 기여가 없음</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2609.03619'>Remember and Reweight: Enhancing Multi-Agent Debate with Experience Memory and Confidence Estimation</a></td><td>15</td><td>0</td><td>NLP</td><td>과거 토론 경험 메모리와 신뢰도 가중치로 multi-agent debate의 공유 오류를 완화한 연구로 로봇과 무관함</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2609.03633'>&lt;/think&gt; Doesn&#x27;t Stop Reasoning: Analysis of Spurious CoT Termination</a></td><td>15</td><td>0</td><td>NLP</td><td>reasoning-to-answering 전환을 위한 EoT 토큰 삽입이 실제로는 추론을 멈추지 못하는 현상을 분석한 연구로 로봇과 무관함</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2609.03687'>A Circuit for Plural Reference: How LLMs Represent and Retrieve Singular and Plural Entities</a></td><td>15</td><td>0</td><td>NLP</td><td>복수 지시 대명사 예측을 담당하는 attention head 회로를 규명한 해석가능성 연구로 로봇과 무관함</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2609.03955'>Two-Stage Reinforcement Learning for Sound and Adversarial Test Generation in Code LLMs</a></td><td>15</td><td>0</td><td>RL</td><td>코드 LLM의 반례 테스트 생성을 adversarial RL로 학습한 2단계 프레임워크로 도메인이 코드에 한정되어 로봇과는 거리가 있음</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2609.04022'>Representational alignment yields generalizable safety in language models</a></td><td>15</td><td>0</td><td>NLP</td><td>도덕 개념의 prototype 구조를 잠재표현에 정렬시켜 적대적 안전성을 높인 연구로 representation learning 관점에서만 소폭 참고 가능하나 로봇과는 무관함</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2609.03787'>DNative-Twin: Decision Graphs and Digital Twins for Reconstructable Agentic Decisions</a></td><td>15</td><td>0</td><td>AI</td><td>에이전트 의사결정을 그래프로 기록하고 재실행하는 디지털트윈 프레임워크로 엔터프라이즈 프로세스 대상이라 robotics와 무관함</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2609.03966'>Interface-Induced Trajectory Censoring</a></td><td>15</td><td>0</td><td>AI</td><td>에이전트 평가에서 서빙 인터페이스가 tool call을 침묵 실패시키는 현상을 밝힌 진단 연구로 방법론적으로 흥미로우나 robotics와 무관함</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2609.04170'>A Case Study on Emergent Cheating and Whistleblowing in Autonomous Research Swarms</a></td><td>15</td><td>0</td><td>AI</td><td>100개 자율 LLM 에이전트 집단에서 자연발생한 부정행위와 내부고발을 관찰한 사례연구로 robotics와 무관함</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2609.03760'>Virtual Testing of Automated Driving Systems through Credible Simulations</a></td><td>14</td><td>1</td><td>Robotics</td><td>자율주행 시뮬레이션 신뢰성 평가 프레임워크로 로봇 학습과 무관한 인증 방법론임</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2609.02894'>R$^{2}$Adapter: A Routing and Rewriting Adapter for Efficient Hybrid RAG</a></td><td>14</td><td>0</td><td>NLP</td><td>질의 난이도에 따라 vanilla·graph RAG를 라우팅하는 경량 어댑터로 로봇 관련성 없음</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2609.03407'>Caught in the Story: Narrative Captivity in Multi-turn LLMs Conversation</a></td><td>14</td><td>0</td><td>NLP</td><td>다중턴 대화에서 모델이 한쪽 서사에 편향되는 실패 모드를 측정한 벤치마크로 robotics와 무관함</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2609.03588'>KC-Bench: A Dynamic Interactive Benchmark for Evaluating Knowledge Conflicts in LLM Agents</a></td><td>14</td><td>0</td><td>NLP</td><td>LLM agent가 지식·도구·환경 정보 충돌을 처리하는 능력을 측정한 벤치마크로 robotics와 무관함</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2609.04128'>Environment Evolution for Terminal Agents</a></td><td>14</td><td>0</td><td>RL</td><td>터미널 코딩 에이전트 학습용 환경을 오프폴리시로 점진 진화시키는 기법으로 robotics와 무관함</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2609.03302'>Tensor-based Brain Surface Modeling and Analysis</a></td><td>12</td><td>0</td><td>CV</td><td>tensor 기반 뇌 표면 형태 분석 방법임. robotics와 무관한 오래된 스타일의 의료영상 기여임.</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2609.03480'>Tree species mapping in Denmark: A comparison of spectral-temporal features with geospatial foundation model embeddings</a></td><td>12</td><td>0</td><td>CV</td><td>덴마크 국가 규모 수종 지도 제작을 위한 EO foundation model 비교임. robotics 무관함.</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2609.03689'>Semantic-Aware Subgraph State Space Model for WSI Classification in Histopathology</a></td><td>12</td><td>0</td><td>CV</td><td>병리 WSI 분류를 위한 semantic subgraph state space model임. robotics 무관함.</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2609.03690'>MetaStructAtlas: A Grounded 3D Vision-Language Dataset and Benchmark for Functional and Structural Reasoning in Whole-Body PET/CT</a></td><td>12</td><td>0</td><td>Multimodal</td><td>전신 PET/CT 3D VLM 데이터셋 및 벤치마크임. robotics 무관함.</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2609.03742'>KnowVis: Knowledge-Centric Visual Summarization for Video Lectures</a></td><td>12</td><td>0</td><td>Multimodal</td><td>지식 중심 강의 비디오 시각 요약 프레임워크임. robotics 무관함.</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2609.03804'>Urban Boundaries, Social Barriers: A Benchmark and Vision-Centric Framework for Mapping Gated Communities and Equity Implications</a></td><td>12</td><td>0</td><td>CV</td><td>게이티드 커뮤니티 매핑을 위한 도시 규모 멀티모달 벤치마크임. robotics 무관함.</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2609.03981'>Sharpening the Ensemble: An SSIM-Aligned Residual Refiner for Brain-MRI Inpainting Post-Processing</a></td><td>12</td><td>0</td><td>CV</td><td>뇌 MRI 인페인팅 앙상블 결과를 SSIM 정렬 residual refiner로 후처리하는 방법임. robotics 무관함.</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2609.04034'>Editable Visual Design</a></td><td>12</td><td>0</td><td>Multimodal</td><td>코딩 에이전트 기반 편집 가능한 비주얼 디자인 생성 파이프라인임. robotics 무관함.</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2609.02890'>Bounded Personas Match Retrieval on Classification but Not Regression for a Frozen Agent</a></td><td>12</td><td>0</td><td>NLP</td><td>개인화 언어 에이전트의 persona 압축 기법으로 로봇 연구와 무관함</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2609.02896'>PiPMRE: A Pipeline Based on Language Model for Medical Relation Extraction</a></td><td>12</td><td>0</td><td>NLP</td><td>의료 텍스트 관계 추출용 생성-필터 파이프라인으로 로봇 연구와 무관함</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2609.02940'>Listen to the Latents: Self-Correcting Speech Recognition in Large Audio Language Models Through Hidden-State Interactions</a></td><td>12</td><td>0</td><td>NLP</td><td>LLM 기반 ASR의 hidden state 상호작용으로 자기교정을 수행하는 연구로 로봇과 무관함</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2609.03181'>Jina-OCR-v1: Efficient Document Parsing with Speculative Decoding and Dense Verifiable Rewards</a></td><td>12</td><td>0</td><td>CV</td><td>저비용 GPU에서 동작하는 문서 OCR 모델로 speculative decoding을 결합했으나 로봇과 무관함</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2609.03235'>SGD-KV: Summarization Guided KV Cache Compression</a></td><td>12</td><td>0</td><td>NLP</td><td>요약 특화 attention head를 식별해 KV 캐시를 압축하는 효율화 기법으로 로봇과 무관함</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2609.03293'>PACE: Towards Surfacing Hidden Conflicts in User Requests</a></td><td>12</td><td>0</td><td>NLP</td><td>개인화 어시스턴트가 암묵적 지식 충돌을 탐지하도록 하는 벤치마크·멀티에이전트 프레임워크로 로봇과 무관함</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2609.03430'>Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning</a></td><td>12</td><td>0</td><td>NLP</td><td>KV 캐시를 무작위로 제거해도 top-score 선택법과 성능이 비슷함을 보인 분석으로 추론 효율화 연구이며 로봇과 무관함</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2609.03511'>Lost in Reordering: Structural Sensitivity of Multilingual LLMs under Semantics-Preserving Perturbations</a></td><td>12</td><td>0</td><td>NLP</td><td>어순 변화에 대한 다국어 LLM의 구조적 민감도를 힌디어·말라얄람어로 측정한 연구로 로봇과 무관함</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2609.03887'>Beyond Shallow Alignment: How Post-Training Methods Determine Refusal Circuits And Steering Robustness</a></td><td>12</td><td>0</td><td>NLP</td><td>post-training 방식이 거부 회로 내부 구조를 어떻게 바꾸는지 분석한 안전성 연구로 로봇과 무관함</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2609.04180'>Knowledge Acquisition During Pre-training? Large Language Models Learn Better With Auxiliary Views</a></td><td>12</td><td>0</td><td>NLP</td><td>사전학습에서 반복 대신 보조 관점 재구성이 지식 습득에 도움이 됨을 통제 실험으로 보인 연구로 로봇과 무관함</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2609.04194'>Legibility is Not Interpretability: Comparing Judged and Actual Importance in Chain-Of-Thought Reasoning</a></td><td>12</td><td>0</td><td>NLP</td><td>CoT 텍스트가 실제 단계 중요도를 온전히 담지 못함을 밝힌 해석가능성 연구로 로봇과 무관함</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2609.03416'>Dude: A Dual-Detection Multi-Agent System for Paper-Code Discrepancy Detection</a></td><td>12</td><td>0</td><td>NLP</td><td>논문-코드 불일치 탐지용 다중 에이전트 시스템으로 robotics와 무관한 응용임</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2609.03423'>DuplexSpeechBench-IFEval: Evaluating Implicit Instruction Following in Full-Duplex Voice Agents</a></td><td>12</td><td>0</td><td>NLP</td><td>풀듀플렉스 음성 에이전트의 암묵적 지시 따르기 벤치마크로 robotics 관련성 없음</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2609.03526'>CulturalMenuBench: Probing the Knowledge-Application Gap in Multimodal Culinary Reasoning</a></td><td>12</td><td>0</td><td>Multimodal</td><td>음식 문화 이해 벤치마크로 시각 인식과 문화 지식 적용 사이의 괴리를 보였으나 robotics와 무관함</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2609.03702'>Synthetic Semantic Supervision for Contrastive Code Representation Learning in Small Transformers: An Empirical Study</a></td><td>12</td><td>0</td><td>NLP</td><td>코드 임베딩용 합성 의미 supervision을 실험적으로 검증한 연구로 robotics와 무관함</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2609.03716'>Artificial Intelligence for Energy Optimization in Data Centers</a></td><td>12</td><td>0</td><td>LG</td><td>데이터센터 AI 에너지 최적화 문헌을 코딩 분석하고 평가 프레임워크를 제안한 서베이로 robotics와 무관함</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2609.04148'>Terminal-Universe: Turning Agent Trajectories into Scalable Terminal Environments</a></td><td>12</td><td>0</td><td>NLP</td><td>에이전트 궤적으로부터 재사용 가능한 터미널 환경을 복원하는 프레임워크로 robotics와 무관함</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2609.04198'>Clean Engineering, Unstable Measurement: A Preregistered Reliability Failure of Black-Box LLM Observers on Shared Endpoints</a></td><td>12</td><td>0</td><td>LG</td><td>공유 서빙 인프라 위 LLM judge의 재현성이 사전등록 기준을 통과하지 못했음을 보인 신뢰성 감사 연구로 robotics와 무관함</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2609.04120'>BooM-VVT: Boosting Mask-Free Video Virtual Try-On with Image-Level Pseudo Data</a></td><td>10</td><td>0</td><td>Video</td><td>mask-free 비디오 가상 시착 프레임워크임. robotics와 무관함.</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2609.02898'>Distilled Rapid Embedding Transfer (DRET): Parameter-Efficient Biomedical Domain Adaptation via Priority-Based Embedding Transfer</a></td><td>10</td><td>0</td><td>NLP</td><td>소형 모델에 대형 biomedical 모델 임베딩을 전이하는 파라미터 효율 기법으로 로봇과 무관함</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2609.02901'>Dual-Form ASR: Semantics-Aware Inverse Text Normalization for Chinese Speech Recognition</a></td><td>10</td><td>0</td><td>NLP</td><td>중국어 음성인식의 spoken·written form을 통합한 ITN 프레임워크로 로봇과 무관함</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2609.03047'>SHELF: A Synthetic Harness for Multi-Task Bibliographic Benchmarking</a></td><td>10</td><td>0</td><td>NLP</td><td>도서관 서지 작업을 위한 합성 벤치마크 생성 시스템으로 로봇과 무관함</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2609.03218'>The Analyst in the Prompt: Role, Retrieval, and Memory Biases in LLM Financial Analysis</a></td><td>10</td><td>0</td><td>NLP</td><td>역할·검색·메모리에 따른 LLM 금융 분석 편향을 측정한 연구로 로봇과 무관함</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2609.03321'>Decoupling Turn-Taking from Semantics: A Decoupled Data Approach for Finite-State-Machine-Based Full-Duplex Dialogue</a></td><td>10</td><td>0</td><td>NLP</td><td>실제 인간 대화에서 turn-taking을 학습해 FSM 기반 full-duplex 대화를 개선한 연구로 로봇과 무관함</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2609.03597'>KhatianDoc: A Human-Verified Benchmark Diagnosing Multimodal LLM Failure on Bengali Legal Land Records</a></td><td>10</td><td>0</td><td>Multimodal</td><td>방글라데시 토지대장의 16진 분수 표기를 다루는 멀티모달 LLM 실패 진단 벤치마크로 로봇과 무관함</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2609.03734'>Beyond BLEU: A Case for Redefining Sign Language Translation Benchmarks</a></td><td>10</td><td>0</td><td>NLP</td><td>수어 번역 평가에서 BLEU 대신 LLM QA 기반 내용 보존 지표를 제안한 연구로 로봇과 무관함</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2609.03894'>CROCODIL: Cross-Model Code Editing with LLMs</a></td><td>10</td><td>0</td><td>NLP</td><td>타 모델이 생성한 코드를 편집할 때 과도한 수정이 발생하는 문제를 보상 기반으로 완화한 연구로 로봇과 무관함</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2609.04197'>ESPO: Error-Structured Prompt Optimization via Diagnose, Diversify, and Stabilize</a></td><td>10</td><td>0</td><td>NLP</td><td>오류를 진단·다양화·안정화하는 3단계로 나눠 프롬프트 비대화를 억제한 최적화 기법으로 로봇과 무관함</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2609.04199'>Compile by Training: Turning Natural-Language Specifications into Local Neural Functions</a></td><td>10</td><td>0</td><td>NLP</td><td>자연어 명세를 소형 신경망 함수로 컴파일하는 시스템으로 로봇과 무관함</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2609.03494'>GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving</a></td><td>10</td><td>0</td><td>LG</td><td>LLM 서빙의 KV cache 동적 예산 관리 기법으로 robotics와 무관한 인프라 최적화임</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2609.03515'>What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation</a></td><td>10</td><td>0</td><td>LG</td><td>디코딩 시점 KV eviction의 시간적 집계 방식을 분석한 효율화 연구로 robotics 관련성 없음</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2609.03535'>Feature Reconfiguration With Visual Prior for Medical Lesion Segmentation</a></td><td>10</td><td>0</td><td>CV</td><td>SAM 기반 사전 정보로 의료 병변 분할 성능을 높인 연구로 robotics 관련성 없음</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2609.03553'>GPS-Bench: A Governance Policy Benchmark for Automating Policy Analysis</a></td><td>10</td><td>0</td><td>NLP</td><td>정책 시뮬레이션 검증용 거버넌스 벤치마크로 robotics와 무관함</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2609.03806'>SVG-Score: Human-Aligned Evaluation of Text-to-SVG Generation</a></td><td>10</td><td>0</td><td>CV</td><td>text-to-SVG 생성 평가지표 연구로 robotics와 무관함</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2609.03860'>Adapting to Evolving Requirements: Agentic AI for Retail Supply Chain Operations</a></td><td>10</td><td>0</td><td>AI</td><td>소매 공급망 최적화 파이프라인을 재구성하는 에이전트 프레임워크로 robotics와 무관함</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2609.03871'>Bioinfoysis Technical Report</a></td><td>10</td><td>0</td><td>AI</td><td>생물정보학 장기 분석용 다중 에이전트 하네스로 robotics와 무관함</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2609.03874'>STAIR (STructure Aware Information Retriever): A novel dataset and LLM based retriever for document structure augmentation</a></td><td>10</td><td>0</td><td>NLP</td><td>목차 구조를 활용한 RAG 검색기 개선 연구로 robotics와 무관함</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2609.03920'>Value-Preserving Architectures for Agentic AI Systems</a></td><td>10</td><td>0</td><td>AI</td><td>다중 에이전트 시스템의 아키텍처 설계가 프라이버시·공정성 등 가치 보존에 미치는 영향을 논한 연구로 robotics와 무관함</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2609.03943'>More Criticism Does Not Make a Better Review: EquiReview-R</a></td><td>10</td><td>0</td><td>NLP</td><td>AI 논문 리뷰에서 과잉비판과 누락을 구분해 개선하는 프레임워크로 robotics와 무관함</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2609.04024'>Instruction Duplication as an Inference-Time Control Primitive</a></td><td>10</td><td>0</td><td>NLP</td><td>지시문을 반복 삽입하는 추론시점 제어 기법으로 robotics와 무관함</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2609.04127'>Epistemic Warrant for LLM Recommendations: Characterizing the Basis for Reliance When Ground Truth Is Unavailable</a></td><td>10</td><td>0</td><td>NLP</td><td>정답이 없는 상황에서 LLM 추천의 신뢰 근거를 정식화한 인식론적 프레임워크로 robotics와 무관함</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2609.04172'>Rethinking On-Policy Distillation of Large Language Models II: One Training Example</a></td><td>10</td><td>0</td><td>NLP</td><td>단일 학습 예시만으로 on-policy distillation 효과 대부분을 재현한 분석 연구로 robotics와 무관함</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2609.02895'>BharatGather: A Culturally-Informed Benchmark Dataset for Misinformation and Fake News Detection in Indian Public Events</a></td><td>8</td><td>0</td><td>NLP</td><td>인도 대중 행사 관련 가짜뉴스 탐지 벤치마크로 로봇 연구와 무관함</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2609.02954'>LexIssue: Benchmarking Legal Issue Identification in Chinese Civil Litigation</a></td><td>8</td><td>0</td><td>NLP</td><td>중국 민사소송 쟁점 식별 벤치마크로 로봇과 무관함</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2609.03273'>Contextual Tamil Spelling and Grammar Correction Using Progressively Fine-Tuned Sequence-to-Sequence Transformers</a></td><td>8</td><td>0</td><td>NLP</td><td>Tamil 맞춤법·문법 교정을 위한 단계적 파인튜닝 seq2seq 연구로 로봇과 무관함</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2609.03330'>Less Is Moral: A CHARMing Framework for Moral Foundations Detection in Endorsement Behaviour</a></td><td>8</td><td>0</td><td>NLP</td><td>혐오발화 인지 rationale을 결합한 경량 도덕 기반 탐지 프레임워크로 로봇과 무관함</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2609.03370'>FrameBench:A Language Understanding Benchmark Based on Frame Semantics</a></td><td>8</td><td>0</td><td>NLP</td><td>동사가 문맥에 따라 다른 semantic frame을 환기하는지 평가하는 벤치마크로 로봇과 무관함</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2609.03394'>Chiaroscuro for Emotions: A Contrastive Emotion Benchmark Grounded in Appraisal Theory</a></td><td>8</td><td>0</td><td>NLP</td><td>동일 사건에서 상반된 감정을 유발하는 대조적 감정 추론 벤치마크로 로봇과 무관함</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2609.03395'>TabScope: Question-Adaptive Scope Selection for Table Question Answering</a></td><td>8</td><td>0</td><td>NLP</td><td>질문 유형에 따라 부분·전체 테이블 추론을 적응적으로 선택하는 테이블 QA 프레임워크로 로봇과 무관함</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2609.03432'>Decoupled Analysis-Judging: An Automated Creativity Evaluator Using LLMs in Complex Multi-step Creativity Tasks</a></td><td>8</td><td>0</td><td>NLP</td><td>분석과 판정을 분리한 LLM 창의성 평가기로 로봇과 무관함</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2609.03454'>When Retrieval Helps: Selective Retrieval for Single-Turn Mental-Health QA</a></td><td>8</td><td>0</td><td>NLP</td><td>정신건강 단일턴 QA에서 선택적 검색이 무조건적 검색보다 안전함을 보인 연구로 로봇과 무관함</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2609.03595'>How Far Can Synthetic Data Take Thai OCR?</a></td><td>8</td><td>0</td><td>CV</td><td>합성 데이터 요소를 분리해 태국어 OCR 전이 성능을 분석한 연구로 로봇과 무관함</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2609.03654'>Enhancing Financial Question Answering: A Novel Benchmark Dataset of Banks&#x27; financial statements</a></td><td>8</td><td>0</td><td>NLP</td><td>유럽·미국 은행 재무제표에 대한 교차기관 금융 QA 벤치마크로 RAG 파이프라인 요소별 기여를 분석했으나 로봇과 무관함</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2609.03781'>IndicSafeEval: Safety Robustness of Large Language Models under Multilingual Persuasive Jailbreak Attacks</a></td><td>8</td><td>0</td><td>NLP</td><td>인도 4개 언어에서 설득 기반 탈옥 공격에 대한 LLM 안전성 벤치마크로 로봇과 무관함</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2609.03953'>Beyond Majority Vote: Multi-Perspective Adjudication for Medical Hallucination Detection</a></td><td>8</td><td>0</td><td>NLP</td><td>의료 챗봇 응답의 사실 오류 탐지에서 다중 관점 조정이 단일 패스 주석보다 우수함을 보인 연구로 로봇과 무관함</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2609.03209'>MasterControl Seventeen Every Time</a></td><td>8</td><td>0</td><td>NLP</td><td>LLM 해석과 정책 실행을 분리해 재현 가능한 기업 분석을 수행하는 거버넌스 프레임워크로 로봇과 무관함</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2609.03402'>A Prompt-Engineering Approach to Develop Scalable, Flexible, and Real-Time Hybrid Micro-Level Personalization in a General Purpose AI Teaching Assistant</a></td><td>8</td><td>0</td><td>NLP</td><td>AI 튜터 개인화를 위한 prompt engineering 사례연구로 robotics 관련성 없음</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2609.03460'>Beyond &quot;Made with AI&quot;: Visualizing Provenance Density to Mitigate the Transparency Penalty</a></td><td>8</td><td>0</td><td>NLP</td><td>AI 생성물 신뢰 표시 UI 연구로 robotics와 무관함</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2609.03527'>NeoRed: A Knowledge-Logic-Alignment Multimodal Large Language Model for Neonatal Respiratory Disease Diagnosis</a></td><td>8</td><td>0</td><td>Multimodal</td><td>신생아 호흡기 질환 진단용 의료 MLLM으로 robotics와 무관함</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2609.03580'>HalluPeer: A Taxonomy-driven Benchmark for Detecting Hallucinations in Scientific Peer Reviews</a></td><td>8</td><td>0</td><td>NLP</td><td>AI 동료평가의 hallucination 탐지 벤치마크로 robotics와 무관함</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2609.03635'>Analysis of Prompt Engineering for Drug Toxicity Prediction</a></td><td>8</td><td>0</td><td>NLP</td><td>약물 독성 예측을 위한 prompt engineering 민감도 분석으로 robotics와 무관함</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2609.03800'>Govern the Model, Not Only the Data: Storage, Circulation, and Learning in Creative AI</a></td><td>8</td><td>0</td><td>NLP</td><td>창작 AI의 federated learning 거버넌스 정책 논의로 robotics와 무관함</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2609.03880'>Xiaomi-TabLDM: A Tabular Foundation Model Technical Report</a></td><td>8</td><td>0</td><td>LG</td><td>합성 데이터로 사전학습한 표형 데이터 파운데이션 모델 기술보고서로 robotics와 무관함</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2609.03923'>Speak for Me: Giving LLMs the Situational Awareness to Participate in a Meeting</a></td><td>8</td><td>0</td><td>NLP</td><td>화상회의에서 LLM 대리인이 말할 시점을 판단하는 아키텍처로 robotics와 무관함</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2609.03960'>FiMI Banking: A Sovereign Model for Indian Retail Banking</a></td><td>8</td><td>0</td><td>NLP</td><td>인도 소매은행 특화 대화 에이전트 연구로 robotics와 무관함</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2609.04013'>LLM4CKD: Large Language Models for Early Stage Chronic Kidney Disease Screening</a></td><td>8</td><td>0</td><td>NLP</td><td>만성 신장질환 조기선별을 위한 LLM zero-shot/few-shot 평가로 robotics와 무관함</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2609.04098'>Why Gated DeltaNet Survives 4-Bit Quantization: NVFP4 W4A4 for the Recurrent Half of a Hybrid 27B LLM</a></td><td>8</td><td>0</td><td>LG</td><td>하이브리드 LLM의 recurrent 레이어 4bit 양자화 메커니즘 분석으로 robotics와 무관한 효율화 연구임</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2609.04135'>The Natural Language Interaction Protocol and Standard for AI Agents</a></td><td>8</td><td>0</td><td>AI</td><td>에이전트 간 상호운용을 위한 자연어 상호작용 프로토콜 표준화 논문으로 robotics와 무관함</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2609.03215'>SWIM: Student Writing Simulation via Proficiency-Conditioned Generation</a></td><td>6</td><td>0</td><td>NLP</td><td>숙련도 조건부 학생 작문 시뮬레이션 태스크로 로봇과 무관함</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2609.03410'>To What Extent Do Large Language Models Understand Bangla Idioms?</a></td><td>6</td><td>0</td><td>NLP</td><td>방글라 관용구에 대한 LLM 이해도를 평가한 벤치마크 연구로 로봇과 무관함</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2609.03502'>Building and Evaluating Fixed-Voice Thai TTS from Synthetic Speech</a></td><td>6</td><td>0</td><td>NLP</td><td>짧은 음성 참조로 고정 화자 태국어 TTS 학생 모델을 학습한 온디바이스 음성합성 연구로 로봇과 무관함</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2609.03577'>Language, Language Models, and What We&#x27;re Talking About</a></td><td>6</td><td>0</td><td>NLP</td><td>이탈리아어 LLM을 사례로 언어모델이 실제 언어를 대표하는지 논하는 의견 논문으로 실험적 기여가 없음</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2609.03652'>The Impact of Synthetic Data Augmentation on Discourse-Pragmatic Function Classification</a></td><td>6</td><td>0</td><td>NLP</td><td>합성 데이터의 임베딩 공간 내 위치가 담화-화용 기능 분류 성능에 미치는 영향을 분석한 연구로 로봇과 무관함</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2609.03814'>Evaluating Criterion-Conditioned Behaviour of Large Language Models in Content Moderation</a></td><td>6</td><td>0</td><td>NLP</td><td>콘텐츠 조정 기준별 LLM 판단 일관성을 평가한 벤치마크로 로봇과 무관함</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2609.03992'>Alignment-Free Text-Audiobox for Voice Dubbing and Full-Duplex Dialogue Synthesis</a></td><td>6</td><td>0</td><td>NLP</td><td>정렬 없는 latent diffusion 기반 더빙·풀듀플렉스 음성합성 시스템으로 로봇과 무관함</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2609.04048'>Translation as a Decision Space: A Multi-Agent Perspective on Low-Resource Dialect Generation</a></td><td>6</td><td>0</td><td>NLP</td><td>저자원 방언 번역을 멀티에이전트 결정 공간으로 재구성한 연구로 로봇과 무관함</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2609.03775'>Typological Feature Prediction with Large Language Models: An In-Context Learning Approach</a></td><td>5</td><td>0</td><td>NLP</td><td>유형론적 언어 특징을 계통·지리적 이웃 정보로 예측하는 in-context learning 연구로 로봇과 무관함</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2609.03967'>Investigating the Ability of Large Language Models to Analyze Recipes for Diabetes</a></td><td>5</td><td>0</td><td>NLP</td><td>당뇨병 적합성 판단을 위한 레시피 분석 LLM 벤치마크로 로봇과 무관함</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2609.04173'>Last Translation Benchmark</a></td><td>5</td><td>0</td><td>NLP</td><td>최신 번역 모델을 무력화하는 검증 규칙 기반 살아있는 번역 벤치마크로 로봇과 무관함</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2609.02981'>Structure and Implementation of New Practical English Textbooks Driven by Artificial Intelligence</a></td><td>5</td><td>0</td><td>NLP</td><td>AI 기반 실용 영어 교재 구조를 제안하고 소규모 교육 실험으로 검증한 응용 연구로 로봇과 무관함</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2609.03719'>Opening mind by opening architecture: analysis strategies</a></td><td>3</td><td>0</td><td>NLP</td><td>전자음향 작곡에서 폐쇄형 신호처리 구조를 분석하는 인문학적 연구로 로봇과 완전히 무관함</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2609.03930'>Fixed Suffix Dependency Ratio: Quantifying the Dual-Track Mechanism of Gender Assignment in Latvian Loanwords</a></td><td>3</td><td>0</td><td>NLP</td><td>라트비아어 외래어의 성 배정 패턴을 정량화한 언어학 연구로 로봇과 무관함</td></tr>
</tbody></table>

</details>
