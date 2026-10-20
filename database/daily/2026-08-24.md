# 오늘의 arXiv Top 15 — 2026-08-24 (월)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**
> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)

**신규 논문 수: 전체 320편 → 중복 제거 후 320편 (이번 평가 대상 320편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 82 |
| cs.LG | 55 |
| cs.RO | 25 |
| cs.CL | 70 |
| cs.AI | 88 |

*1차 스크리닝: 전체 320편을 제목/초록 기반으로 채점(Claude (scheduled agent)) → 상위 15편은 arXiv 원문을 내려받아 정밀 리뷰(Claude (scheduled agent)) 후 최종 점수 산정.*

---

## Top 15

### 1. [80점] Beyond Imitation: Self-Improving Robot Policies via Off-Policy Q-Planning

- **분야**: Manipulation / Self-Improving VLA · **robotics relevance**: 9/10
- **arXiv**: [2608.21204](https://arxiv.org/abs/2608.21204) ([PDF](https://arxiv.org/pdf/2608.21204))
- **저자**: Varun Giridhar, Anant Khandelwal, Jeremy A. Collins, Ignat Georgiev, Animesh Garg
- **카테고리**: Robotics (cs.RO) · 신규 목록 게재: cs.RO
- **Comments**: Project page with videos: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 Q-Planning은 대형 BC(Behaviour Cloning) VLA 정책은 고정한 채, 소형 off-policy Q-function을 별도로 학습시켜 추론 시 Q-weighted action selection과 배포 후 실패 rollout까지 흡수하는 self-improvement를 가능하게 한다. LIBERO/RoboTwin 시뮬레이션과 실제 양팔 로봇 실험에서 인간 개입 없이 성능을 크게 끌어올렸다(LIBERO-10 93→99%, RoboTwin 83.8→91.4%, 실로봇 stack-cups 40→90%, insert-wallet 25→80%).

**Core innovation & methodology**

- BC와 Q-function을 asymmetric하게 분리: BC는 성공 데모만 학습 가능하지만 Q-function은 성공·실패 rollout 모두 학습 가능하다는 비대칭성을 self-improvement의 핵심 메커니즘으로 활용한다.
- Q-chunking과 HL-Gauss categorical regression을 결합해 sparse terminal reward 하에서도 안정적으로 value를 학습한다.
- 추론 시 단일 스텝 Q-weighted average(softmax weighting)로 BC의 3-step flow-matching draw N개 중 후보를 aggregation, MPPI 대비 hyperparameter가 적고 1.7~3.2배 더 빠르다.
- BC 가중치(수십억 파라미터)는 절대 건드리지 않고 Q-function(~1B 파라미터)만 온라인으로 fine-tune하는 self-improvement loop를 설계했다.

**Novelty vs. prior works**

- V-GPS, DSRL, IBRL, DAWR 등 기존 value-guided/imitation-bootstrapped 방법과 달리, BC frozen + multi-billion VLA에 plug-and-play + failure로부터 학습 + auxiliary actor 불필요라는 5개 축 모두를 만족하는 유일한 방법임을 Table 1로 정리했다.
- 핵심 novelty는 새로운 아키텍처보다 'actor-critic 비대칭성을 self-improvement에 활용'이라는 문제 재구성에 가깝다. Q-chunking, HL-Gauss 등 개별 구성요소는 기존 기법의 재사용이다.
- concurrent work인 BC-to-Q(arXiv 2605.05172)와 아이디어가 유사하나, auxiliary actor 없이 multi-billion-parameter VLA 스케일에서 실증했다는 점에서 차별화된다.

**Benchmark results**

- LIBERO 4개 suite와 RoboTwin 47개 task에서 10회 self-improvement 후 mean success가 92.1%→97.6%(+5.5pp)로 상승, LIBERO-10 93→99%, RoboTwin 83.8→91.4%.
- 실제 양팔 로봇 2개 contact-rich task에서 5회 iteration만으로 stack-cups 40→90%, insert-wallet 25→80%(SFT-only baseline은 각각 55%, 30%에서 정체).
- 동일 online budget에서 Best-of-N(95%대 정체), Filtered SFT(93.5% 정체), IBRL(붕괴), DSRL(69~91% 진동), DAWR(BC 이하)와 비교했을 때 Q-Planning만 안정적으로 개선됐다.
- action-source ablation: vanilla MPPI는 BC baseline보다 낮은 성능을 보였고, 온도-smoothed MPPI와 제안한 single-step Q-weighted average가 동일하게 +3pp를 얻었으나 후자가 1.7~3.2배 더 빠르다.
- latency: RoboTwin에서 N=32 planning step이 400ms로 960ms replan budget의 42%만 사용하고, LIBERO에서는 frozen BC baseline과 거의 동일한 latency(640ms)를 보였다.

**Top-tier conference 적합성 — 78/100 · 추천 venue: CoRL**

LIBERO/RoboTwin 시뮬레이션과 실제 양팔 로봇 실험까지 갖춘 강한 실증적 증거와 5개 baseline과의 명확한 비교로 CoRL/RSS 수준의 강점을 보인다. 다만 이론적 novelty는 Q-chunking·HL-Gauss 등 기존 기법의 조합에 가깝고 self-improvement 반복 규모(최대 10 iteration, task 수 제한)가 크지 않아 NeurIPS/ICML급 이론적 기여로는 다소 약할 수 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- BC 정책은 고정하고 소형 critic만 온라인 업데이트하는 구조는 대형 VLA를 다루는 test-time optimization·self-improvement 연구에 바로 적용 가능하다.
- 실패 rollout을 자산으로 흡수하는 asymmetry 아이디어는 failure detection·recovery 연구에서 '실패로부터 저비용으로 학습하는 메커니즘'으로 확장할 수 있다.
- Q-weighted action selection은 다른 VLA의 test-time re-ranking/inference-time planning에도 이식 가능한 general-purpose 기법이다.

---

### 2. [78점] WA-JEPA: Rethinking the Video JEPA Paradigm for World-Action Modeling in Autonomous Driving

- **분야**: World Model (Autonomous Driving Planning) · **robotics relevance**: 7/10
- **arXiv**: [2608.20974](https://arxiv.org/abs/2608.20974) ([PDF](https://arxiv.org/pdf/2608.20974))
- **저자**: Xinlin Wang, Yujiao Xiang, Yuheng Zhou, Jingqi Wang, Minqing Huang, Jiajie Huang, Dongxu Wei, Tingguang Zhou 외 6명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 76점

> 💡 WA-JEPA는 V-JEPA의 random masking·deterministic regression을 future-masking과 conditional flow matching으로 바꾸고, future scene token과 ego trajectory를 하나의 predictor에서 함께 denoise하는 joint future-action modeling으로 planning에 특화된 world-action model을 제안한다. NAVSIM-v2에서 91.7 EPDMS로 기존 world-action 최고 대비 1.3점, closed-loop HUGSIM에서도 zero-shot으로 최고 HD-Score 0.4462를 달성했다.

**Core innovation & methodology**

- Hybrid Future-Masked Pre-training: V-JEPA의 random spatiotemporal mask 대신 Full-mask(순수 causal future 예측)와 Patch-mask(부분 future context 유지)를 결합해 future-directed prediction 목표로 재정의한다.
- Deterministic regression 대신 conditional flow matching(x-prediction)으로 future latent를 생성적으로 예측해 downstream planning에 더 유용한 미래 표현을 만든다.
- MMDiT 스타일 joint future-action predictor가 future scene token과 ego trajectory를 동일 spatiotemporal latent space에서 함께 denoise하여, action supervision이 world representation을 직접 형성하게 한다.
- 2단계 학습: Stage1은 nuPlan 대규모 영상으로 future-masked pretraining, Stage2는 NAVSIM에서 action stream을 추가해 joint world-action modeling을 수행한다.

**Novelty vs. prior works**

- Drive-JEPA가 V-JEPA encoder를 driving에 도입했지만 별도의 downstream trajectory planner에 의존하는 반면, WA-JEPA는 predictive representation learning과 planning을 하나의 flow-based joint predictor로 통합한다.
- Latent-WAM, DreamerAD 등 video-latent 기반 WAM은 VAE로 압축된 표현을 쓰는 데 비해, WA-JEPA는 V-JEPA의 semantically rich feature space를 그대로 유지하며 future rollout과 action generation을 동시에 수행한다는 점이 핵심 차별점이다.
- 다만 핵심 구성요소(future masking, flow matching, joint prediction)는 각각 masked video modeling·diffusion/flow matching 문헌에서 이미 알려진 기법의 조합이며, V-JEPA를 planning에 맞게 재설계한 정교한 엔지니어링에 가깝다는 점은 감안해야 한다.

**Benchmark results**

- NAVSIM-v2: EPDMS 91.7, 최강 E2E(SparseDriveV2 90.1) 대비 +1.6, 최강 WAM(Discrete-WAM 90.4) 대비 +1.3.
- NAVSIM-v1: PDMS 91.8.
- HUGSIM closed-loop(436 scenarios, zero-shot): HD-Score 0.4462로 기존 최고 DrivoR(0.3252) 대비 큰 폭 개선, 특히 medium/hard 난이도에서 향상 폭이 크다.
- Ablation(encoder): V-JEPA2 backbone이 MAE/DINOv3 대비 EPDMS 5.7점 우위(89.5 vs 83.8).
- Ablation(masking): No-Stage1 89.5 → Patch-mask만 91.0 → Full-mask만 91.3 → 결합 91.7.
- Ablation(Stage2): flow matching+joint future-action modeling 결합이 91.7로 최고, action-only baseline은 89.9.

**Top-tier conference 적합성 — 80/100 · 추천 venue: CVPR / ICCV (Autonomous Driving World Model)**

명확한 문제의식('V-JEPA가 planning에 부적합한 이유')과 체계적 ablation으로 각 설계 선택의 기여를 분리해 보여주는 실험적 엄밀함이 강점이며, closed-loop zero-shot 결과까지 갖춰 설득력이 높다. 다만 자율주행이라는 단일 도메인에 국한되고 구성 요소 각각의 독창성은 제한적이어서 top-tier oral보다는 강한 poster 수준으로 평가된다.

**추천 이유 & 누리랩 연구와의 연결점**

- predictive representation(JEPA)과 action generation을 하나의 flow matching predictor로 통합하는 방식은 조작 로봇 VLA에 latent world model을 결합하는 아이디어로 적용할 수 있다.
- hybrid future masking 전략은 로봇 조작 데이터에서 future 예측 pretraining을 설계할 때 causal/partial masking의 균형을 잡는 데 참고할 수 있다.
- closed-loop zero-shot transfer 결과는 test-time world model이 학습 도메인 밖에서도 planning에 기여할 수 있음을 시사하며, robot memory·domain generalization 연구에 참고할 수 있다.

---

### 3. [76점] Annotations as Rollouts: Efficient and Scalable Reinforcement Learning for Video MLLMs

- **분야**: RL / Video MLLM Post-training · **robotics relevance**: 3/10
- **arXiv**: [2608.20492](https://arxiv.org/abs/2608.20492) ([PDF](https://arxiv.org/pdf/2608.20492))
- **저자**: Yunheng Li, Guohong Mu, Hao Li, Shengsheng Qian, Dingwen Zhang, Qibin Hou, Ming-Ming Cheng
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: Project page: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 video MLLM RL post-training에서 annotation을 단순 reward 참조가 아니라 on-policy group에 추가되는 oracle rollout으로 직접 사용하는 OraRL을 제안한다. oracle이 advantage baseline을 왜곡해 발생하는 'advantage inversion' 문제를 decoupled advantage estimator와 sign-balanced pruning으로 해결해, GRPO 대비 7개 task family에서 일관된 성능·효율 향상을 보인다.

**Core innovation & methodology**

- annotation-as-rollout: 정답 annotation을 모델의 응답 포맷으로 직렬화해 on-policy group에 oracle rollout으로 추가함으로써, 매 query마다 신뢰할 수 있는 positive anchor를 제공한다.
- advantage inversion 현상(고보상 oracle이 group baseline을 끌어올려 GRPO 기준 positive이던 rollout이 negative advantage로 뒤집히는 문제)을 수식으로 규명하고, on-policy 평균만으로 baseline을 계산하는 decoupled advantage estimator로 이를 원천 차단한다.
- oracle-policy gap을 directional gain(above-mean rollout 증폭)과 별도의 detached oracle advantage(reward-gap weight로 스케일, 최대 positive advantage로 cap)라는 두 항으로 분리 인코딩한다.
- sign-balanced pruning(oracle + 양/음 최고 advantage rollout만 유지) 후 post-selection moment correction(재중심화·RMS 재조정)으로 전체 group 대비 1.48배 backward 연산 속도 향상을 달성한다.

**Novelty vs. prior works**

- GRPO/Dr.GRPO/GDPO/CPPO 등 on-policy group RL 변형들은 서로 최대 0.4점 차이(Table 12, 60.3~60.7)에 불과한 반면 OraRL은 62.7을 달성해, advantage normalization 방식이나 magnitude 기반 pruning이 아니라 oracle 통합 메커니즘 자체가 성능 향상의 원인임을 통제 실험으로 보인다.
- 저자들의 이전 연구 Tempsamp-R1의 task-specific hand-designed reward shaping(수동 튜닝 필요)과 달리, OraRL은 reward gap과 dispersion 변화만으로 하나의 통일된 update rule을 유도해 7개 task family(temporal/spatial/spatio-temporal grounding, tracking, segmentation, VQA, spatial intelligence)에 동일하게 적용한다.
- 핵심 기여는 잘 알려진 RL 학습 병리(baseline shift로 인한 advantage 왜곡)에 대한 정교한 최적화 기법 수정으로, 완전히 새로운 학습 패러다임이라기보다는 GRPO 계열 알고리즘의 국소적이지만 실질적 결함을 해결한 확장에 가깝다.

**Benchmark results**

- VSI-Bench(spatial intelligence): Video-ORA-9B 73.1로 GPT-5(55.0), Gemini-3-Pro(55.1), 오픈소스 공간지능 특화 모델 SpaceMind(69.6)를 모두 상회한다.
- Temporal grounding(TimeLens mIoU): Video-ORA-9B가 Charades/ActivityNet/QVHighlights에서 61.8/63.6/72.5로 TimeLens2-8B(58.6/58.6/70.2)를 능가하고 Gemini-2.5-Pro도 세 벤치마크 모두에서 앞선다.
- Tracking(GOT-10k AO): Video-ORA-9B 78.2 vs OneThinker-8B 73.0(+5.2); Segmentation은 backbone Qwen3.5-9B 대비 MeViS J&F +29.2(32.1→61.3), ReasonVOS +42.2(21.5→63.7)로 가장 큰 절대 개선폭을 보인다.
- scaling 실험: 0.8B→9B 전 구간에서 backbone 대비 macro average 8점 이상 개선(51.8→66.2), 데이터 스케일링에서도 6.4k~100k prompt 구간에서 OraRL이 GRPO(video +2.8, spatial +3.1) 대비 더 큰 이득(video +5.2, spatial +3.6)을 보인다.
- component ablation(Table 15)에서 directional gain/detached oracle/sign balance/moment correction 각각 제거 시 평균이 62.7에서 61.2~62.1로 하락하나, pruning 자체를 끄면(κ=0) 오히려 63.1로 소폭 상승해 효율-정확도 trade-off가 존재함을 보여준다.

**Top-tier conference 적합성 — 78/100 · 추천 venue: CVPR / NeurIPS**

advantage inversion이라는 구체적 실패 모드를 수식으로 규명하고 이를 해소하는 decoupled estimator를 제안한 뒤, 7개 task family·다양한 backbone/scale·강력한 통제 ablation으로 폭넓게 검증한 점이 강점이다. 다만 핵심 기여가 GRPO 계열의 국소적 결함 수정에 가까워 완전히 새로운 학습 패러다임을 제시했다고 보기는 어렵고, 이 점이 oral/highlight 선정의 위험 요인이다.

**추천 이유 & 누리랩 연구와의 연결점**

- annotation-as-rollout과 advantage inversion 분석은 VLA/로봇 정책을 GRPO류 RL로 fine-tuning할 때 expert demonstration을 oracle rollout으로 직접 활용하는 RL/IL 융합 학습법으로 전이 가능하다.
- decoupled advantage estimator는 로봇 조작에서 demo-guided RL 시 advantage baseline 왜곡을 방지하는 일반적 기법으로, language feedback 기반 학습에도 유사하게 적용할 수 있다.
- sign-balanced pruning과 moment correction은 test-time/train-time 연산 예산이 제한된 on-device 로봇 정책 학습에서 rollout 효율화 기법으로 참고할 수 있다.

---

### 4. [74점] RISE: Adaptive Imagination for World Action Models

- **분야**: World Model (Autonomous Driving Planning) · **robotics relevance**: 7/10
- **arXiv**: [2608.20430](https://arxiv.org/abs/2608.20430) ([PDF](https://arxiv.org/pdf/2608.20430))
- **저자**: Hongbo Lu, Liang Yao, Chenghao He, Hao Han, Fan Liu, Wenlong Liao, Tao He, Pai Peng
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 78점

> 💡 RISE는 world action model(WAM)에서 매 rollout 단계마다 Latent Evaluator와 Rollout Gate로 Roll/Stop을 결정해 장면별로 다른 imagination depth를 사용하는 adaptive imagination framework다. NAVSIM과 nuScenes에서 fixed rollout 대비 더 높은 PDMS/EPDMS를 달성하면서 불필요한 rollout을 줄였다.

**Core innovation & methodology**

- Future Planning Gain 개념을 도입해, rollout을 한 단계 더 진행했을 때 planning score가 얼마나 개선될지를 매 step마다 재추정하는 sequential stopping 신호로 사용한다.
- Latent Evaluator가 Risk Profile과 Future Planning Gain Profile을 함께 예측하고, Rollout Gate가 이를 computation cost와 비교해 Roll/Stop을 결정한다.
- CounterDrive: Wan 2.7 기반 counterfactual video generation, OpenVO 궤적 추출, human verification을 결합해 factual log에는 없는 다양한 위험 상황을 담은 데이터셋을 구축한다.
- Predictor/초기 Planner → Latent Evaluator/Guided Planner → Rollout Gate 순서의 3단계 학습으로 evaluator와 gate를 안정적으로 학습한다.

**Novelty vs. prior works**

- 기존 WAM(Unified Video Action Model, Cosmos Policy, DreamZero 등)은 imagine-and-plan/imagine-then-plan/no-imagination 중 하나의 고정 스케줄을 쓰는 반면, RISE는 scene-dependent horizon을 sequential decision으로 만든다.
- Random Stop, Latent Margin 같은 단순 adaptive baseline 대비 Scheduler가 더 나은 latency-performance trade-off를 보여(Table5: 90.8 EPDMS vs 89.5/89.7) '무엇을 기준으로 멈출지'가 핵심 novelty임을 보여준다.
- 다만 encoder-predictor-planner 구조 자체는 기존 WAM 설계를 그대로 사용하며, adaptive computation이라는 아이디어 자체는 다른 도메인의 test-time compute 조절 원리를 world model에 적용한 것이라 새로운 representation·paradigm이라기보다는 새로운 inference-time control 메커니즘에 가깝다.

**Benchmark results**

- NAVSIM v1: PDMS 91.5로 기존 최고 EponaV2(90.4) 대비 +1.1.
- NAVSIM v2: EPDMS 90.8로 DriveFuture(89.9) 대비 +0.9.
- nuScenes: 평균 L2 0.31m, collision rate 0.10으로 SOTA.
- Ablation: Scheduler+CounterDrive 결합 시 EPDMS 88.9→90.8 (Scheduler 단독 90.4, CounterDrive 단독 89.8로 상호 보완적).
- DAWN에 Scheduler를 transfer했을 때 PDMS 89.1→90.3로 개선되어 plug-in 일반성을 확인했다.
- CounterDrive 유무에 따른 위험 판별 AUC가 0.49~0.52에서 0.93~0.96으로 급증했다.

**Top-tier conference 적합성 — 72/100 · 추천 venue: CVPR / ICCV (Autonomous Driving World Model)**

다중 벤치마크·ablation·architecture transfer 실험까지 갖춘 강한 실험적 근거와 실용적인 test-time efficiency 기여가 강점이다. 다만 기존 WAM 아키텍처 위에 스케줄링 모듈을 얹는 형태로 conceptual novelty는 제한적이라 oral보다는 strong poster/highlight 수준에 가깝다.

**추천 이유 & 누리랩 연구와의 연결점**

- adaptive rollout depth 결정 메커니즘은 매니퓰레이션 VLA/world model의 test-time imagination budget 조절 연구에 직접 적용 가능하다.
- CounterDrive의 counterfactual data augmentation 방식은 실패 사례가 드문 manipulation failure detection/recovery용 데이터셋 구축에 참고할 수 있다.
- Latent Evaluator의 risk profile 예측 아이디어는 로봇 조작의 failure diagnosis/anomaly detection 모듈 설계에 응용할 수 있다.

---

### 5. [74점] CertVLA: Certified Defense against Physical Visual Attacks for Vision-Language-Action Models

- **분야**: VLA (Certified Robustness / Physical Attack Defense) · **robotics relevance**: 8/10
- **arXiv**: [2608.20791](https://arxiv.org/abs/2608.20791) ([PDF](https://arxiv.org/pdf/2608.20791))
- **저자**: Hui Lu, Zhijie Peng, Yuqi Lin, Zaijia Yang, Jiaming He, Shuhan Ye, Yi Yu, Hanwei Zhu 외 3명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 CertVLA는 위치를 알 수 없는 patch/texture 공격에 대해 continuous VLA action chunk를 인증하는 certified defense로, R-covering mask 쌍 중 최소 하나가 공격을 완전히 지운다는 성질과 conformal calibration을 결합한다. LIBERO 시뮬레이션과 실제 로봇 실험에서 방어 성공률과 함께 finite-sample 인증 성공률을 동시에 보고했다.

**Core innovation & methodology**

- continuous action에 맞춘 calibrated consistency region을 정의한다: 이산 label 일치 대신 anchor action 주변의 정규화된 action distance 기반 clean-consistency region B_{i,j}(B;τ)을 도입한다.
- position-scale matrix Q로 mask 쌍마다 다른 benign action 변동을 정규화하고, conformal calibration(quantile τ)으로 finite-sample clean coverage(1-α)를 보장한다.
- anchored dual-mask recovery 알고리즘(∃i∀j 판정)으로 covering mask 중 공격이 지워진 최소 하나의 anchor row를 찾아 반환하며, early-stopping으로 계산을 효율화한다.
- query-level 인증을 conjunction으로 묶어 closed-loop rollout 전체에 대한 certificate로 확장하고, dual-mask rollout correctness 조건 하에서는 task success까지 보장하는 조건부 정리(Theorem 2, Lemma 5)를 제시한다.

**Novelty vs. prior works**

- PatchCleanser/PatchCURE 등 기존 certified patch defense는 discrete classification/detection label에 대한 exact agreement를 요구하는데, CertVLA는 continuous하고 temporally correlated한 action chunk에 정규화된 consistency score와 conformal threshold를 적용해 처음 확장했다는 점이 본질적 차별점이다.
- 기존 VLA 방어(robust training, noise-filtering 등)는 경험적 강건성만 보고하는 반면, CertVLA는 adaptive attacker에 대한 이론적 증명과 finite-sample coverage 보장을 함께 제시한다.
- 다만 threat model이 bounded-size square patch/texture로 한정되고, task-success 보장은 별도의 dual-mask rollout correctness 가정을 필요로 해 임의 공격 전반을 커버하지 못한다. 실제 로봇에서 certified 성공률(30%)이 defense 성공률(60%)보다 크게 낮아 인증의 보수성이 실용성을 제약한다는 점은 novelty의 한계로 지적할 수 있다.

**Benchmark results**

- LIBERO patch attack: OpenVLA-OFT 평균 Defense/Certified 94.00%/94.00%, π0.5 90.75%/76.50%, π0 83.50%/61.75%.
- LIBERO texture attack: π0.5 평균 94.50% Defense, 88.50% Certified로 최고 성능.
- 실제 로봇(Piper dual-arm) patch attack: π0.5 clean 90%→attacked 40%→CertVLA defense 60%(20%p 회복)→certified 30%.
- Defense-Certified gap이 생성형 정책(π0, π0.5)에서 더 크게 나타나(예: LIBERO-Goal π0: 86%→61%) 일부 성공 rollout이 calibration 영역을 벗어남을 시사한다.
- mask set size, patch size, mask size, β/α 등 hyperparameter sensitivity 분석을 포함하지만 구체적 수치 상당수는 그래프로만 제시되어 본문 표에서 확인 불가한 부분이 있다.

**Top-tier conference 적합성 — 70/100 · 추천 venue: ICLR / NeurIPS (이론 강조) 또는 CoRL (로봇 실험 강조)**

continuous closed-loop action에 대한 certified defense라는 새로운 문제 설정을 이론적 증명과 실제 로봇 실험으로 함께 뒷받침한 점이 강점이다. 다만 threat model이 bounded square patch로 제한적이고 certified 성공률이 defense 성공률 대비 크게 낮아 실제 유용성에 의문을 제기하는 rejection risk가 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- VLA의 물리적 공격에 대한 이론적 안전 보장 문제는 '언제 정책을 신뢰할 수 없는지'를 사전에 인증하는 failure detection/recovery 메커니즘으로 확장할 수 있다.
- anchored dual-mask 방식의 다중 query 계산 비용 구조는 test-time optimization/inference-time verification 관점의 효율화 연구 주제가 될 수 있다.
- conformal calibration 기반 finite-sample coverage 보장 기법은 robot memory나 world model 예측의 신뢰 구간 추정에도 응용할 수 있다.

---

### 6. [73점] ForeTime-VLA: Causal Future-Token Distillation from a World Action Model for Conveyor-Belt Manipulation

- **분야**: VLA (World-Model-Distilled Manipulation) · **robotics relevance**: 10/10
- **arXiv**: [2608.20735](https://arxiv.org/abs/2608.20735) ([PDF](https://arxiv.org/pdf/2608.20735))
- **저자**: Siyuan Ma, Yutian Zhang, Boshi Zhang, Qinglian Wu, Jiaqi Zhai, Dong Wei, Xiaojin Huang
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **Comments**: 8 pages, 5 figures. Introduces ForeTime-VLA, a causal future-token distillation method for conveyor-belt manipulation from a frozen world action model teacher
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 ForeTime-VLA는 frozen Fast-WAM 기반 teacher로부터 미래 시각 latent를 압축한 64차원 action-equivalent code를 causal encoder로 예측하게 하고, 이를 π0.5의 VLM prefix와 action expert에 이중 경로로 주입해 미래 접촉 이벤트를 미리 반영하게 한다. 실제 로봇 컨베이어 벨트 파지 실험에서 정지 물체 81.1%, 저속 이동 물체 58.9% 성공률로 π0.5 대비 각각 12.2%p, 22.2%p 향상됐다.

**Core innovation & methodology**

- offline teacher-student 구조: Fast-WAM/Wan video latent를 현재+8개 미래 offset에서 추출해 64차원 whitened action-equivalent code로 압축(teacher encoder)하고, causal encoder는 과거 8프레임만으로 이를 예측한다(student).
- dual-path conditioning: 예측된 future code를 4개 future token+1개 phase token으로 VLM prefix에, future와 time-to-transition을 action expert의 residual 조건으로 주입해 slow/fast path 모두에 미래 정보를 전달한다.
- cosine, relational geometry, phase classification, time-to-transition, action-equivalence 등 5가지 보조 loss를 원래 flow-matching action loss에 추가하되, ground-truth action target은 변경하지 않는다.
- 추론 시 미래 프레임이나 WAM teacher 없이 causal encoder만으로 동작해 배포 비용을 최소화한다(지연시간 +2.5~2.9%만 증가).

**Novelty vs. prior works**

- Fast-WAM이 'video modeling은 학습 신호로만 필요하고 test-time imagination은 제거 가능하다'는 결론을 제시했는데, ForeTime-VLA는 이를 VLA fine-tuning에 실제로 결합해 검증한 사례로, 동일 저자 그룹의 DECOWAM(legged manipulation)과 개념적으로 병렬적인 접근이다.
- 기존 world-model-conditioned VLA들이 대개 video-scale teacher를 배포 시에도 구동하거나 별도 imagination을 수행하는 반면, ForeTime-VLA는 1.251M 파라미터의 경량 모듈만 추가해 teacher 없이 causal하게 미래 구조를 활용한다는 점이 실용적 novelty다.
- 다만 검증이 단일 embodiment(conveyor-belt pick-and-place)와 단일 정책 계열(π0.5)에 국한되며, 오프라인 지표 개선폭(MAE 2.63%, L2 3.02%)은 통계적으로 유의하지만 절대적인 수치 자체는 크지 않아 방법의 일반성은 아직 제한적이다.

**Benchmark results**

- Offline: test MAE 0.134119→0.130593(-2.63%, 95% CI 0.82~4.48%), test L2 -3.02%, 지연시간 +2.46~2.93%.
- Cross-family 비교: GR00T N1.6, StarVLA, SmolVLA 모두 π0.5/ForeTime-VLA보다 MAE/L2가 열세(예: GR00T test MAE가 π0.5 대비 +13.46%).
- 실제 로봇 정지 물체 파지: ForeTime-VLA 81.1%(73/90) vs 차상위 StarVLA 68.9%, π0.5 65.6%.
- 실제 로봇 저속 이동 물체 파지: ForeTime-VLA 58.9%(53/90) vs π0.5 36.7%, contact-pose error도 15.56%→6.67%로 감소.
- 속도 스트레스 테스트: 3단계 belt speed 합산 44/90 vs π0.5 23/90, 특히 fast speed에서 11/30 vs 2/30.
- Ablation: future condition 제거 시 transition MAE +10.1%, phase/time condition 제거 시 +10.6%로 두 조건 모두 실질적으로 사용됨을 확인했다.

**Top-tier conference 적합성 — 68/100 · 추천 venue: CoRL / ICRA**

실제 로봇에서의 명확한 성공률 개선과 속도별 강건성 실험, 세밀한 ablation이 강점이며 로봇 조작 커뮤니티(CoRL/ICRA)에 잘 맞는다. 다만 단일 태스크·단일 embodiment에 국한된 실증 범위와 오프라인 지표 개선폭의 작음은 top-tier oral보다는 포스터·워크샵 수준의 rejection risk로 작용할 수 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- world model teacher를 배포 시 제거하고 경량 causal encoder로 미래 구조를 distill하는 아이디어는 test-time optimization/inference-time efficiency 연구와 직접 연결된다.
- phase/time-to-transition 예측은 failure detection·recovery에서 contact timing 오류를 사전에 감지하는 신호로 확장할 수 있다.
- dual-path(VLM prefix + action expert residual) future conditioning 구조는 기존 VLA에 world-model 정보를 최소 침습적으로 주입하는 실용적 템플릿으로 활용할 수 있다.

---

### 7. [73점] AffordAny: Open-World 3D Affordance Grounding from Monocular RGB Images via Vision-Language-Guided Geometric Reasoning

- **분야**: Manipulation (3D Affordance Grounding) · **robotics relevance**: 8/10
- **arXiv**: [2608.20720](https://arxiv.org/abs/2608.20720) ([PDF](https://arxiv.org/pdf/2608.20720))
- **저자**: Junqi Wu, Kaihua Tang, Xuanwen Chen, Hongzhi Li, Jianqiang Huang, Xian-Sheng Hua
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: The code and dataset are publicly available. Code: this https URL . Dataset: this https URL
- **원문 검토**: PDF 전문 · 1차 스크리닝 74점

> 💡 AffordAny는 단일 monocular RGB 이미지에서 SAM 3D 재구성과 LLM 기반 자동 파이프라인으로 473개 카테고리, 10,633개 part 수준의 open-vocabulary 3D affordance 데이터셋을 구축하고, frozen Cosmos-2B VLM feature와 3D geometry를 결합하는 decoder로 affordance grounding을 수행한다. Pseudo-label self-training을 더해 unseen-category mIoU를 6.3% 상대적으로 개선했다.

**Core innovation & methodology**

- LVIS 기반 자동 파이프라인(SAM 3D 재구성 → 6-view 렌더링 → LLM part discovery → 2D 분할 → multi-view 3D label lifting)으로 사전 구축된 3D asset 없이 raw RGB에서 text-conditioned 3D part supervision을 생성한다.
- VLM-guided decoder: projection injection(2D→3D 공간 대응), instruction-conditioned semantic compression(FiLM으로 16개 prototype 생성), GPBlock(Group-Mix-Ungroup)의 bidirectional geometry-semantics fusion으로 구성된다.
- Minimal-perturbation pseudo-label self-training과 post-hoc Platt calibration으로 추가 인력 라벨링 없이 category-level 일반화를 개선한다.
- unseen object/unseen category/unseen instruction paraphrase를 분리 평가하는 systematic generalization protocol을 설계한다.

**Novelty vs. prior works**

- LASO, LMAffordance3D 등 기존 language-conditioned 3D affordance 연구는 closed vocabulary와 pre-built 3D geometry를 전제하는 반면, AffordAny는 단일 RGB 이미지에서 전 과정을 자동화하고 open vocabulary로 확장한 점이 본질적 차이다.
- instruction robustness gap(|ΔIoU|=0.105)이 LASO/LMAffordance3D(0.34 이상)보다 훨씬 작아, semantic bottleneck 설계가 실질적 novelty를 뒷받침한다.
- 다만 개별 구성 요소(frozen VLM feature 활용, FiLM 조건화, cross-attention decoder)는 기존 open-vocabulary grounding·segmentation 연구에서 널리 쓰이는 기법의 조합이며, 핵심 기여는 새로운 학습 paradigm보다는 대규모 데이터셋 구축과 파이프라인 엔지니어링에 가깝다.

**Benchmark results**

- unseen object IoU 0.428로 LMAffordance3D(0.418) 대비 우위, unseen category IoU 0.305로 LASO(0.266) 대비 우위.
- unseen instruction IoU 0.680으로 baseline(OpenAD 0.360, LASO 0.374, LMAffordance3D 0.387) 대비 큰 격차.
- Ablation: semantic compression 제거 시 unseen-category IoU가 -0.060으로 가장 크게 하락, GPBlock -0.035, projection injection -0.030, instruction dropout -0.017.
- pseudo-label self-training 후 unseen-category mIoU +0.016(+6.3% relative, p<0.01), 특히 tail category(≤50 sample)에서 +0.012로 head category(+0.003)보다 큰 개선.
- 데이터셋 규모는 5,334 objects, 10,633 part-level, 31,899 instruction-level, 473 categories로 기존 대비 categorical diversity가 한 자릿수 이상 크다.

**Top-tier conference 적합성 — 63/100 · 추천 venue: CVPR / AAAI**

대규모 자동화 데이터 구축과 체계적 generalization protocol이 실용적 기여로 강하지만, decoder 자체의 방법론적 참신성은 제한적이고 category shift에서의 성능 향상폭도 크지 않아(0.305 IoU 수준) top-tier oral보다는 데이터셋·애플리케이션 트랙에 적합하다.

**추천 이유 & 누리랩 연구와의 연결점**

- open-world affordance grounding은 로봇 조작의 grasp/manipulation point 선정에 바로 활용 가능하며, 저자들도 향후 로봇 조작 적용을 명시하고 있다.
- frozen VLM feature와 3D geometry의 bidirectional fusion(GPBlock) 설계는 scene graph·semantic mapping에서 언어-3D 정렬 모듈로 재활용할 수 있다.
- pseudo-label self-training과 calibration 전략은 로봇 데이터가 희소한 tail object/category에 대한 자기지도적 확장에 참고할 수 있다.

---

### 8. [68점] Stream3Dv2: Geometric-Semantic Fusion Enhanced Streaming Zero-Shot 3D Scene Understanding

- **분야**: 3D Vision / Embodied AI (Streaming Open-Vocabulary 3D Scene Understanding) · **robotics relevance**: 7/10
- **arXiv**: [2608.21136](https://arxiv.org/abs/2608.21136) ([PDF](https://arxiv.org/pdf/2608.21136))
- **저자**: Jie Xu, Na Zhao
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 68점

> 💡 training-free streaming 3D scene understanding 프레임워크 Stream3Dv2를 제안한다. grid/semantic 2D segmentation을 set covering/set partitioning 문제로 통합하는 geometric-semantic fusion과 Riemannian 그래프 기반 manifold refinement를 통해, 잡음 있는 2D mask와 스트리밍 제약 하에서도 기존 zero-shot 3D segmentation/detection baseline을 능가한다.

**Core innovation & methodology**

- streaming 3D instance segmentation을 local multi-view segmentation(F_Loc)과 local-to-historical merging(F_Loc2his)이라는 nested 구조로 분해해, 매 프레임마다 전체 시퀀스를 재처리하지 않고도 timely response를 지원한다.
- grid-prompted(SAM2, class-agnostic, coverage 높음)와 semantic-prompted(SAM3, 정확한 경계·클래스 있음) 2D segmentation을 각각 set covering problem(SCP)과 set partitioning problem(SPP)으로 정식화해 노이즈 마스크 필터링과 fine/coarse mask 병합·분할을 통합한다.
- Euclidean distance 대신 Riemannian graph metric(Mahalanobis distance 기반 super-point graph)과 multi-source Eikonal 방정식(iterative Bellman relaxation)을 이용한 point-to-manifold 마스크 정제로 non-Euclidean 표면 경계 오류를 완화한다.
- 3D bounding box 기반 fast instance localization으로 static/dynamic/신규 인스턴스를 구분해 manifold-to-manifold 갱신을 가속하고, LLM agent와 결합해 grounding/reasoning/navigation 등 downstream embodied task로 확장한다.

**Novelty vs. prior works**

- 저자들의 이전 conference 버전인 Stream3D 대비, semantic guidance가 없던 순수 geometric 병합과 Euclidean 기반 manifold refinement를 각각 SPP 기반 semantic-driven partitioning과 Eikonal 방정식 기반 manifold refinement로 교체한 것으로, 'v2' 확장 논문의 성격이 강해 개념적 도약보다는 방법론적 고도화에 가깝다.
- MaskClustering, OVIR-3D, SAI3D, MV3DIS 등 대부분의 open-vocabulary zero-shot 3D segmentation은 offline full-sequence 설정을 가정하는데, Stream3Dv2는 이들과 동등하거나 더 나은 성능을 스트리밍 제약 하에서 달성한다는 점이 실질적 차별점이다.
- SCP/SPP 기반 마스크 병합, Riemannian 그래프의 Eikonal 방정식 등 핵심 구성 요소는 고전적 조합최적화·그래프 알고리즘의 재조합으로, 학습 기반 새 표현이나 새 학습 패러다임을 제시하는 것은 아니다.

**Benchmark results**

- ScanNet200/ScanNet++/MatterPort3D open-vocabulary 3D instance segmentation(Table I)에서 semantic AP 기준 ScanNet200 20.6 vs SOTA zero-shot full-sequence 방법 MV3DIS 15.5로, streaming 제약에도 불구하고 앞선다.
- streaming 전용 baseline 비교(Table III, ScanNet200 class-agnostic)에서 Stream3Dv2 AP 27.1/AP50 42.0/AP25 55.3 @ 11 FPS로, 학습 기반 EmbodiedSAM(AP 28.8, 10 FPS)에 근접하고 training-free 경쟁자(SAM3D 9.6, OnlineAnySeg 18.6)를 크게 상회한다.
- ScanNet200 open-vocabulary 3D object detection(Table IV)에서 AP50 14.2/AP25 24.8로 non-streaming Zoo3D1(15.2/23.5)에 근접한 성능을 streaming 방식으로 달성한다.
- Stream3D 대비 Stream3Dv2의 per-class semantic AP50 평균 개선폭은 ScanNet200 20.2→38.3(+18.1), ScanNet++ 4.7→26.9(+22.2), MatterPort3D 13.7→32.1(+18.4)로 크다.
- 본문에 언급된 module-wise ablation(component ablation)의 구체적 수치는 추출 과정에서 누락되어 본문에서 확인 불가.

**Top-tier conference 적합성 — 66/100 · 추천 venue: CVPR / ICCV**

streaming zero-shot 3D scene understanding이라는 실용적으로 중요한 문제를 훈련 없이 해결하며 3개 벤치마크에서 폭넓게 검증했다는 점이 강점이다. 다만 저자 자신의 conference 논문(Stream3D)의 확장판이라는 위치와 핵심 기법이 조합최적화·그래프 알고리즘 재사용에 가깝다는 점은 oral/highlight급 conceptual leap으로 보기에는 다소 부족하다.

**추천 이유 & 누리랩 연구와의 연결점**

- open-vocabulary streaming scene understanding은 로봇의 실시간 semantic mapping/scene graph 구축 모듈로 직접 활용 가능하며, 특히 SCP/SPP 기반 노이즈 마스크 필터링은 로봇 온보드 센서의 불완전한 2D segmentation을 다루는 데 유용하다.
- 3D bounding box 기반 static/dynamic instance 분류는 동적 환경에서의 active perception/NBV(다음 관측 위치 결정) 및 robot memory(과거 instance pool 유지) 연구와 접목할 수 있다.
- LLM agent 결합을 통한 grounding/reasoning/navigation demo는 VLA나 embodied spatial reasoning 파이프라인의 3D 인식 프론트엔드로 재사용할 수 있다.

---

### 9. [67점] CIVA: Critic-Induced Value-Subspace Attacks on Visual World-Model Agents

- **분야**: World Model / Adversarial Robustness (RL Security) · **robotics relevance**: 6/10
- **arXiv**: [2608.21114](https://arxiv.org/abs/2608.21114) ([PDF](https://arxiv.org/pdf/2608.21114))
- **저자**: Jiancheng Wang, Mingli Zhu, Tong Zhang, Jiaqi Ruan, Wei Wang, Siyuan Liang, Dacheng Tao
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: Includes supplementary material
- **원문 검토**: PDF 전문 · 1차 스크리닝 64점

> 💡 DreamerV3 같은 시각 world-model agent의 critic이 유도하는 저차원 value-subspace에 효과적인 공격 방향이 집중된다는 관찰을 바탕으로, offline로 subspace를 추출하고 test-time에는 그 계수만 최적화·EMA로 smoothing하는 CIVA를 제안한다. DMC walker walk, Atari Pong, Crafter에서 기존 5개 공격 기법 대비 더 강한 reward 하락과 낮은 temporal jitter를 동시에 달성한다.

**Core innovation & methodology**

- critic-guided perturbation을 clean rollout(200-step warm-up 후 M=600 프레임)에서 수집해 쌓은 뒤 truncated SVD로 rank r=32의 'Critic-Induced Value-Subspace'를 추출하는 offline 단계를 제안한다. 이 basis는 PCA/DCT 같은 input statistics가 아니라 victim critic 자체의 gradient에서 유도된다.
- online 단계에서는 D=12,288 전체 pixel space가 아니라 r=32 subspace 계수만 projected gradient step으로 최적화해 per-frame 연산 비용을 크게 낮춘다.
- subspace 계수에 대해 EMA smoothing(ρ=0.75)을 적용해 pixel-space smoothing과 달리 critic-effective 방향을 잃지 않으면서 temporal coherence를 확보한다.
- white-box·causal·online 공격이라는 엄격한 threat model(ε=24/255, per-frame 소수 gradient step 예산)을 정의해 recurrent latent dynamics를 가진 world-model agent 특유의 'recurrent dilution' 문제를 명시적으로 다룬다.

**Novelty vs. prior works**

- MAD, UAP-RL, PA-AD, Illusory, DAPGD 등 기존 RL observation attack은 대부분 매 프레임 전체 pixel space에서 독립적으로 최적화하거나 정적 universal perturbation을 사용하는데, CIVA는 victim critic이 유도하는 저차원 basis를 recurrent world-model agent에 특화해 처음으로 도입한다.
- 지도학습 분야의 PCA/DCT 기반 subspace attack이나 universal perturbation과 달리, CIVA의 basis는 victim의 value gradient rollout에서 직접 추출되며 이것이 recurrent latent dynamics와 명시적으로 연결된다는 점이 차별점이다.
- ablation(V4: critic 대신 reward-head gradient로 subspace 구성)에서 효과가 26.07%→4.84%로 붕괴하는 결과는, 단순히 '저차원 subspace'가 아니라 'critic-aligned' subspace가 핵심임을 뒷받침해 novelty 주장이 실험적으로 검증된다.

**Benchmark results**

- DMC walker walk: CIVA reward drop 26.07%(episode reward 703.97)로 최강 baseline UAP-RL(23.25%)을 상회하며, TempAbs 0.646으로 PA-AD/Illusory/DAPGD(TempAbs 10~20)보다 10배 이상 매끄럽다.
- Atari Pong: CIVA reward drop 85.71% vs 2위 MAD 66.67%, 나머지 baseline은 모두 25% 미만으로 격차가 크다.
- Action-KL은 CIVA가 DMC 1.130/Pong 0.184로 최고 수준이나, PA-AD가 DMC에서 KL 1.35로 더 높으면서도 reward drop은 17.38%에 그쳐 KL만으로는 공격 강도를 예측할 수 없음을 보인다.
- ablation(Table 3-4): random basis로 대체(V1)하면 26.07%→6.90%, subspace 제약 없이 full-pixel critic-PGD(V2)만 사용하면 12.61%(TempAbs는 3.235로 급증)로 각각 저하되어, low-rank와 critic-alignment 두 요소가 모두 필요함을 보여준다.
- Crafter 환경 결과는 appendix로 이관되어 제공된 본문에서는 구체적 수치가 확인 불가.

**Top-tier conference 적합성 — 68/100 · 추천 venue: NeurIPS / ICLR**

recurrent world-model agent에 특화된 critic-induced subspace라는 명확한 관찰과 이를 뒷받침하는 통제된 ablation이 강점이며, 3개 환경·5개 baseline 비교로 실험 폭도 양호하다. 다만 단일 backbone(DreamerV3)에서만 검증되었고 white-box·online 설정이라는 제한된 threat model 하의 결과라, 방어(defense) 없이 공격 효과성만 다룬 점이 일반화 가능성 측면에서 약점으로 지적될 수 있다.

**추천 이유 & 누리랩 연구와의 연결점**

- world model 기반 로봇 정책의 취약성을 규명한 연구로, 안전-critical 로봇 배포 전 world-model agent의 failure mode를 사전에 진단하는 실패 탐지/진단 연구에 참고할 수 있다.
- critic이 유도하는 저차원 value-subspace라는 아이디어는 공격이 아니라 test-time optimization 관점에서, 로봇 정책의 action에 민감한 저차원 방향만 탐색하는 효율적인 inference-time 적응·탐색 기법으로 역이용할 수 있다.
- EMA 기반 subspace smoothing 기법은 로봇 world model의 latent state를 시간적으로 일관되게 조정해야 하는 test-time adaptation·counterfactual reasoning 시나리오에도 응용 가능하다.

---

### 10. [65점] Just Noticeable Difference Modeling for Token Compression in Vision-Language-Action Models

- **분야**: VLA / Efficient Inference · **robotics relevance**: 8/10
- **arXiv**: [2608.21247](https://arxiv.org/abs/2608.21247) ([PDF](https://arxiv.org/pdf/2608.21247))
- **저자**: Zhuoyuan Li, Rui Zhao, Jin Wang, Hanwei Zhu, Cong Zhang, Giuseppe Valenzise, Weisi Lin, Kin-Man Lam
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: 15 pages, 5 figures
- **원문 검토**: PDF 전문 · 1차 스크리닝 72점

> 💡 VLA 정책의 closed-loop action 응답을 기준으로 토큰 변화의 허용 범위를 정의하는 Action-JND를 제안한다. 이를 경량 JND estimator로 학습해 KV-cache reuse와 token pruning에 plug-in 기준으로 적용함으로써 압축이 action에 미치는 영향을 직접 통제하려 한다.

**Core innovation & methodology**

- 인간 시각의 JND(just noticeable difference) 개념을 VLA의 language-conditioned action 응답으로 확장한 Action-JND를 새롭게 정식화한다.
- frozen VLA policy를 두고 clean/perturbed visual token으로부터 얻은 action 응답 차이(discrete는 KL divergence, continuous는 weighted L1)를 최소화하면서 perturbation magnitude는 최대화하는 목적함수로 token-wise JND map을 학습한다.
- 학습된 perturbation 크기를 action-tolerance score로 변환해, VLA-Cache 기반 KV-cache reuse와 token pruning 파이프라인에 순위 기준으로 삽입하는 plug-and-play 구조를 제시한다.
- single-view/dual-view(주시점+wrist-view) 각각에 대해 독립 파라미터를 갖는 경량 convolutional JND estimator 아키텍처를 설계한다.

**Novelty vs. prior works**

- VLA-Cache, VLA-Pruner, EfficientVLA 등 기존 VLA 압축 기법은 visual similarity, attention score, temporal redundancy 같은 간접적 proxy로 압축 대상을 고른다는 점에서, action 편차를 직접 목표로 하는 Action-JND는 문제 설정 자체가 다르다.
- FeatJND(feature-level JND, ICML 2026)의 receiver-dependent tolerance 개념을 VLA policy의 action 응답으로 옮긴 확장으로, 이론적 틀 자체는 FeatJND의 직계 후속이며 독립적인 새 이론이라기보다는 도메인 전이(embodied action)에 해당한다.
- 제안 방법은 기존 압축 파이프라인(VLA-Cache, token pruning)의 후보 선택 단계에 순위 신호를 추가하는 구조로, 압축 프레임워크 자체를 재설계하지는 않는다는 점에서 novelty가 알고리즘적 정식화(문제 재정의)에 집중되어 있다.

**Benchmark results**

- LIBERO 로봇 조작 벤치마크에서 OpenVLA(discrete action)와 OpenVLA-OFT(continuous action) 두 backbone에 대해 실험했다고 abstract에 명시되어 있으나, 제공된 텍스트에서는 실험 섹션(V. Experiments)의 표와 구체적 수치가 추출 과정에서 누락되어 있다.
- 'aggressive compression ratio에서 특히 큰 개선'이라는 저자 주장은 있으나 정확한 compression ratio, success rate, baseline 대비 개선폭은 본문에서 확인 불가.
- baseline으로 VLA-Cache(KV reuse), token pruning 계열이 언급되나 구체적 수치 비교표는 본문에서 확인 불가.
- ablation(perturbation 크기 측정 방식 abs/rel score 선택, single/dual-view 비교 등)의 정량적 결과도 본문에서 확인 불가.

**Top-tier conference 적합성 — 58/100 · 추천 venue: CVPR (또는 IEEE TCSVT/TPAMI 저널)**

JND를 embodied action 영역으로 확장하는 문제 정식화는 신선하고 로봇 조작 VLA 가속이라는 실용적 우선 주제와 맞닿아 있다. 다만 제공된 텍스트에서 실험 결과 표가 누락되어 empirical conviction을 충분히 검증할 수 없고, 저자 소속과 서식(IEEE journal 'UNDER REVIEW' 포맷)을 볼 때 top-tier vision conference보다는 IEEE 저널 투고에 더 가까워 보인다.

**추천 이유 & 누리랩 연구와의 연결점**

- test-time optimization/inference-time efficiency 관점에서, VLA policy의 action 민감도를 직접 추정하는 아이디어는 누리랩의 실시간 closed-loop 로봇 정책 가속 연구에 참고할 수 있다.
- action-tolerance score는 failure detection이나 실행 중 불확실성 추정과 결합해, action 편차가 큰 프레임을 조기에 감지하는 robot memory/모니터링 모듈로 확장할 수 있다.
- KV-cache reuse에 적용된 방식은 장기 조작(long-horizon manipulation)에서 skill chaining 시 어떤 시각 토큰을 재사용해도 안전한지 판단하는 기준으로 응용 가능하다.

---

### 11. [62점] CARD: Diagnosing Belief to Action Routing Failures in Vision Language Models

- **분야**: Embodied AI / VLM Interpretability · **robotics relevance**: 5/10
- **arXiv**: [2608.20763](https://arxiv.org/abs/2608.20763) ([PDF](https://arxiv.org/pdf/2608.20763))
- **저자**: Souptik Kumar Majumdar, Fabian Kögel, Andreas Bulling
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 VLM 내부에서 belief 표현이 실제로 다른 축(intent/action) 예측에 사용되는지 진단하는 Cross-Axis Routing Diagnostic(CARD)을 제안하고, 새로 설계한 협력적 grid-world 벤치마크 Relay Chain에서 검증한다. 4개 open-weight VLM 모두에서 belief가 belief/knowledge 예측에는 쓰이지만 cooperative action(intent) 예측에는 전혀 반영되지 않는 routing failure를 발견했다.

**Core innovation & methodology**

- 기존 same-axis probing/steering(같은 축을 steer하고 같은 축을 읽음)을 cross-axis로 확장: 한 축(belief)을 steer하고 다른 축(intent, knowledge)의 예측 변화를 측정하는 CARD 진단법을 제안한다.
- gap-shift metric(M_{A,B}=g_B(+10)-g_B(-10))으로 steering이 다른 axis 예측을 얼마나 causal하게 움직이는지 정량화한다.
- GridToM을 확장해 partner의 mental state가 실제로 협력 행동을 결정하는 3-agent cooperative grid-world Relay Chain(444 scenario)을 새로 구성하고 cooperative action axis를 추가했다.
- projection-removal, prompt-resistance(12개 변형), CLEVR control, distributed-token steering 등 4가지 대안 가설을 배제하는 ablation을 설계했다.

**Novelty vs. prior works**

- 기존 probing/steering 연구(GridToM, Bortoletto et al.)는 belief가 인코딩되어 있는지, 같은 축 예측에 영향을 주는지만 확인했으나, CARD는 belief 표현이 다른 축(action) 예측에 실제로 routing되는지를 처음으로 검증한다.
- 벤치마크와 모델 스케일이 4개 open-weight 7~8B급 VLM과 2D toy grid-world로 제한되어 있어, 대형 모델·실제 영상에서도 동일한 routing failure가 나타나는지는 확인 불가(저자 스스로 한계로 명시).
- steering 벡터·probe 방향 자체는 새로운 표현이 아니라 기존 linear probing 기법을 그대로 사용하며, novelty는 진단 프로토콜(cross-axis 측정)에 있고 표현 학습 자체에 대한 기여는 제한적이다.

**Benchmark results**

- belief 질문에서 linear probe 정확도 78.1~94.5%(4개 VLM 평균), TB 조건 79.3~100% 정확도 대 FB 조건 2.0~30.7%로 belief가 잘 decode됨을 확인했다.
- intent 질문에서는 4개 VLM 모두 constant per-protagonist prior로 수렴, CARD steering으로도 intent 정확도 변화가 사실상 0(belief/knowledge는 +2.7~+22.7pp 개선되는 것과 대조).
- 108개 intent 측정 전체에서 95% 신뢰구간 기준 최대 개선폭이 18.7pp인 반면 belief positive control은 22.9pp로, intent null이 통계적으로 유의미하게 성립한다.
- projection-removal(c=0.5~5), prompt-resistance(12개 변형×4 VLM×4 protagonist=192 cell), CLEVR cross-task control, distributed-token steering(18개 조합)까지 4가지 대안 설명을 모두 배제했다.
- Relay Chain 규모: 444 scenario(성공 300 + counter 144), probe-set/eval-set 각 222개로 분할, 4~8 keyframe 사용.

**Top-tier conference 적합성 — 62/100 · 추천 venue: ACL/EMNLP (interpretability track)**

기존 same-axis probing을 cross-axis 진단으로 확장한 방법론적 novelty와 4가지 대안가설을 체계적으로 배제한 실험 설계는 인정할 만하나, 평가가 2D toy grid-world와 소형 VLM 4종에 국한되어 일반화 근거가 제한적이라 top-tier venue의 oral보다는 findings·워크숍급에 가깝다.

**추천 이유 & 누리랩 연구와의 연결점**

- belief 표현이 encoded되어도 action prediction에 routing되지 않는다는 발견은 로봇의 memory/belief state가 실제 행동 정책에 반영되는지 검증하는 failure diagnosis 연구에 직접 적용 가능하다.
- cross-axis steering 진단법은 VLA의 internal representation(예: object state, goal belief)이 실제 action head에 제대로 연결되는지 확인하는 test-time diagnostic 도구로 확장할 수 있다.
- multi-agent cooperative 상황에서 partner mental state를 반영하지 못하는 현상은 인간-로봇 협업(HRI) 및 collaborative manipulation의 실패 원인 분석에 참고 가치가 있다.

---

### 12. [61점] VisTa3D: A Dataset and Benchmark for Thin Object Reconstruction from Vision, Tactile, and 3D Point Clouds

- **분야**: 3D Reconstruction / Tactile Perception (Dataset & Benchmark) · **robotics relevance**: 7/10
- **arXiv**: [2608.20740](https://arxiv.org/abs/2608.20740) ([PDF](https://arxiv.org/pdf/2608.20740))
- **저자**: Shania Guo, Yeongsik Seo, Andrew Fu, Mei Hao, Iris Xia, Jiwon Jenny Lee, Xinyi Mary Xie, Hyoungseob Park 외 2명
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 66점

> 💡 RGB, depth, vision-based tactile response 맵을 동기화해 수집한 최초의 thin object 3D reconstruction 데이터셋 VisTa3D를 공개한다. 11개 기존 3D reconstruction 방법이 얇은 물체에서 심하게 저조한 성능을 보임을 확인하고, tactile 정보를 결합한 최초의 baseline Tactile-DC가 기존 최고 성능 OmniDC를 일관되게 앞선다는 것을 보인다.

**Core innovation & methodology**

- RGB/depth/tactile response map을 IMU·카메라 pose·calibration과 동기화해 수집한 최초의 visual-range-tactile thin-object 데이터셋(real 225 scene + synthetic 162 scene, 총 387 scene, 70개 물체, 17개 환경)을 제시한다.
- 3DMakerPro Moose 구조광 스캐너(0.03mm 정확도)로 얇은 물체를 개별 스캔한 뒤 SAM2 기반 raw point cloud 정합·ICP registration·삽입을 거쳐, z-buffer(물체 내부)/k-median buffer(외부)를 구분 적용한 고품질 ground-truth depth·segmentation 생성 파이프라인을 구축한다.
- MDE·MVS·MDC·NVS 4개 패러다임 11개 기존 방법을 general/thin-object-focused 2가지 평가 모드 × default/median-scale/linear-fit 3가지 프로토콜, 총 6가지 evaluation mode로 벤치마킹한다.
- 최초의 vision-range-tactile 3D reconstruction baseline인 Tactile-DC를 제안한다. 접촉 위치를 카메라 calibration으로 이미지 평면에 투영해 RGB-depth fused feature map에 tactile latent vector를 주입하는 구조다.

**Novelty vs. prior works**

- 논문의 핵심 기여는 새로운 학습 패러다임이 아니라 데이터셋·벤치마크 자체이며, Tactile-DC 모델은 기존 depth completion 아키텍처(SPN decoder 등)에 tactile encoder를 추가한 비교적 단순한 확장이다.
- ThinObject-5K(2D segmentation), Mendeley/PLDU/PLDM(powerline 2D), PointWire/PointVessel(point cloud only) 등 기존 thin-object 데이터셋과 달리, visual+range+tactile을 모두 갖추고 고정밀 laser-scan GT를 제공하는 최초의 리소스라는 점에서 gap을 명확히 채운다.
- 저자 스스로 밝히듯 실제 데이터 규모는 '보통 수준'이며 반사/특수광/투명 물체는 제외되어 있어, dataset의 일반화 범위는 제한적이다.

**Benchmark results**

- general evaluation(default protocol) 기준 Tactile-DC A1/A2/A3 = 0.844/0.900/0.920로 기존 최고 성능 OmniDC(0.834/0.881/0.897)를 모든 지표에서 능가한다.
- thin-object focused evaluation에서도 Tactile-DC A1/A2/A3 = 0.719/0.811/0.852 vs OmniDC 0.687/0.772/0.817로 일관되게 우세하다.
- UniDepth V1/V2, DepthAnything V1/V2 등 MDE 모델은 default protocol에서 A1이 0.000~0.007 수준으로 붕괴하며, scale 보정(median scale/linear fit) 후에도 A1이 0.10 미만에 머물러 thin structure 복원 실패가 스케일 문제와 별개임을 보여준다.
- MVS 계열 VGGT/MapAnything은 multi-view/metric depth를 활용함에도 general 대비 thin-object-focused 성능이 크게 떨어져, thin region 보존이 MVS의 구조적 약점임을 시사한다.
- Novel View Synthesis 벤치마크(Table 2)에서 Nerfacto가 PSNR 24.16/SSIM 0.855/LPIPS 0.177로 최고 성능을 보이며 3DGS(22.97/0.805/0.322)가 2DGS(21.74/0.802/0.367)보다 우수하나, 두 GS 계열 모두 Nerfacto-based 방법보다 낮다. tactile 관련 NVS ablation은 supplementary로 미뤄져 본문에서 확인 불가.

**Top-tier conference 적합성 — 58/100 · 추천 venue: 3DV / ICRA (Dataset & Benchmark track)**

얇은 물체 3D 복원이라는 실질적으로 중요하지만 그동안 다뤄지지 않은 문제에 최초의 멀티모달(visual-range-tactile) 데이터셋과 체계적 벤치마크를 제공한 점이 강점이다. 다만 방법론적 기여가 dataset curation과 비교적 단순한 baseline 결합에 그쳐, 순수 vision top-tier conference의 main track보다는 dataset/benchmark track이나 로보틱스 학회에 더 적합하다.

**추천 이유 & 누리랩 연구와의 연결점**

- tactile perception과 object-centric 3D reconstruction을 결합한 접근은 로봇 매니퓰레이션에서 전선/케이블 등 얇은 물체를 다루는 grasp planning 및 물체 인식 파이프라인에 직접 활용할 수 있다.
- 데이터 부족·occlusion 상황에서 tactile로 시각 정보를 보완하는 아이디어는 active perception(다음 접촉/관측 위치 결정) 연구와 결합할 여지가 있다.
- 고정밀 GT 생성 파이프라인(스캔-정합-삽입)은 누리랩의 자체 tactile-visual 데이터 수집 시 참고할 수 있는 실무적 방법론을 제공한다.

---

### 13. [58점] Triangulation-Free Bundle Adjustment with Graduated Non-Convexity for Camera Pose Refinement from Coarse Priors

- **분야**: 3D Vision / SLAM / Bundle Adjustment · **robotics relevance**: 5/10
- **arXiv**: [2608.21008](https://arxiv.org/abs/2608.21008) ([PDF](https://arxiv.org/pdf/2608.21008))
- **저자**: Nikolaos Kyriazis
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **Comments**: 25 pages, 3 figures. 18-scene MobileBrick evaluation, 15-scene ScanNet++ room-scale campaign, plus LaMAR. Code to be released under Apache-2.0
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 모바일 AR pose prior를 오히려 악화시키는 기존 triangulation 기반 bundle adjustment의 문제를 진단하고, keypoint마다 자신의 ray를 따라 scalar depth를 유지하는 triangulation-free bundle adjustment를 제안한다. graduated non-convexity(GNC)를 결합해 32도 perturbation까지도 CPU 10초 만에 복원하며, 정확한 ARKit prior를 해치지 않고 유지한다.

**Core innovation & methodology**

- 기존 방식(COLMAP triangulation+BA)이 prior의 오차를 구조(structure)에 그대로 반영(bake in)해 정확한 ARKit prior조차 악화시키는 문제를 진단했다.
- landmark 변수를 없애고 각 관측(observation)이 자신의 back-projected ray를 따라 독립적인 scalar depth(ray time)를 갖도록 하는 triangulation-free parameterization을 제안, match마다 symmetric cross-projection residual 2개로 consistency를 부여한다.
- 구조가 매 iterate마다 재표현되므로 robust loss scale을 annealing하는 graduated non-convexity(GNC)를 자연스럽게 적용할 수 있다. classical BA는 triangulation이 선행 커밋되어 이 방식을 쓸 수 없다.
- position/orientation prior anchor 항과 prior trust region guardrail(허용 오차 초과 시 원래 prior로 fallback)로 metric gauge를 유지하면서 안전성을 보장한다.

**Novelty vs. prior works**

- inverse-depth parameterization(Civera et al.), ParallaxBA, MASt3R-SfM의 per-pixel depth 등 기존 per-observation depth 기법과 관련이 있으나, landmark 변수를 완전히 제거하고 loss annealing(GNC)까지 결합한 조합은 저자 스스로도 '새로운 것은 조합'이라고 명시한다.
- 근본적으로 새로운 표현이라기보다 기존 structureless BA 계열과 GNC 계열을 결합한 것으로 각 요소 자체의 참신성은 제한적이나, 'triangulation이 prior 오차를 구조에 고정시켜 refinement가 prior를 악화시킨다'는 진단과 그 해법 제시는 실용적 의미가 있다.
- object-scale(MobileBrick)에서는 classical BA(0.218°) 대비 유의미하게 더 나은 결과는 아니고(0.246°), 저자도 'nominal accuracy is on par rather than better'라고 명시해 novelty의 실질적 성능 우위는 제한적이다.

**Benchmark results**

- ScanNet++ 15개 room에서 classical triangulation+BA는 15개 scene 모두에서 ARKit prior를 악화(0.55°→0.74°)시키는 반면, 제안 방법은 0.57°로 prior 수준을 유지하고 330회 perturbed room 실험에서 solver failure 0건.
- MobileBrick 18 scene object-scale에서 0.456° prior를 0.265°/1.80mm(capped, 10s), 0.246°/1.61mm(uncapped, 101s)로 refine, PoRF(0.22°/1.23mm, GPU 2.5시간) 대비 CPU 10초로 유사한 수준에 도달했다.
- classical BA는 prior perturbation 1~2도를 넘으면 붕괴하고 32도에서는 전혀 살아남지 못하는 반면, 제안 방법+GNC는 16°/80mm까지 425/425 성공, 32°/160mm에서도 85% 성공.
- 3D Gaussian Splatting 다운스트림에서 16° perturbed prior 기준 PSNR이 classical 8.9dB 대비 20.4dB로 개선됐고, MobileBrick 평균 splatting PSNR도 ARKit prior 16.55dB에서 제안 방법 17.48dB로 개선됐다.
- ablation: anchored-track variant(Civera-style)는 GNC 하에서 per-observation depth와 거의 동일한 성능을 보인다고 언급되나(Table 7), 세부 수치는 본문에서 확인 불가.

**Top-tier conference 적합성 — 60/100 · 추천 venue: CVPR/ICCV (3D vision)**

15개 room-scale scene과 18개 object-scale scene, 735회 이상의 perturbation 실험까지 포함한 꼼꼼한 실증 분석이 강점이며 단독 저자임에도 실험 설계가 견고하다. 다만 방법론적 기여가 기존 structureless BA·GNC 기법의 조합에 가깝고 object-scale 정확도는 classical BA 대비 개선이 아닌 동등 수준에 그쳐 top-tier 학회 oral보다는 poster급에 가깝다.

**추천 이유 & 누리랩 연구와의 연결점**

- prior의 오차를 구조에 미리 고정하지 않고 매 iteration마다 재평가하는 원리는 로봇 navigation의 pose graph optimization·visual odometry에서 outlier-robust 초기화 문제에 적용할 수 있다.
- CPU 10초 수준의 경량 refinement는 온보드 로봇의 실시간 localization/SLAM에 바로 적용 가능한 효율적 inference 사례로 참고할 만하다.
- graduated non-convexity를 structureless objective에 적용하는 아이디어는 로봇의 scene graph/3DGS 기반 map 최적화에서 prior 신뢰도가 낮을 때의 test-time robust optimization 기법으로 확장할 수 있다.

---

### 14. [56점] A Collaborative Multi-Modality Interaction for VLA-based End-to-End Autonomous Driving

- **분야**: VLA / Autonomous Driving · **robotics relevance**: 6/10
- **arXiv**: [2608.20890](https://arxiv.org/abs/2608.20890) ([PDF](https://arxiv.org/pdf/2608.20890))
- **저자**: Jingtao Sun, Xiaohai He, Yike Zhang, Dong Huang, Yaonan Wang, Ajmal Mian, Mike Zheng Shou
- **카테고리**: Computer Vision and Pattern Recognition (cs.CV) · 신규 목록 게재: cs.CV
- **원문 검토**: PDF 전문 · 1차 스크리닝 62점

> 💡 카메라와 LiDAR 간 양방향 optimal transport 상호작용, normalizing flow 기반 modality distribution 정합, CHOMP 스타일 trajectory refinement를 결합한 VLA 기반 end-to-end 자율주행 시스템을 제안한다. NAVSIM/Bench2Drive/nuScenes/Argoverse2 등 4개 벤치마크에서 기존 VLA·전통 E2E 방법 대비 소폭에서 중간 폭의 성능 개선을 보였다.

**Core innovation & methodology**

- Affinity-Guided Optimal Transport로 카메라-LiDAR 간 main-auxiliary 양방향 상호작용을 discrete OT의 Sinkhorn 알고리즘으로 계산한다.
- Distribution-Consistent Modality Transfer: normalizing flow로 이질적 modality(카메라/LiDAR/언어)를 공통 Gaussian latent로 정렬한 뒤 OT 기반 cross-modal alignment를 수행한다.
- Discrete Flow Matching의 denoising 중간 상태를 그대로 후보 trajectory 집합으로 활용하는 Multi-modal Multi-Trajectory Planning을 제안한다.
- CHOMP에서 영감을 받은 driving risk cost map(3D detection + BEV segmentation 기반)으로 정책 추가 학습 없이 trajectory를 후처리 최적화한다.

**Novelty vs. prior works**

- optimal transport, normalizing flow, CHOMP 등 기존에 확립된 기법들을 자율주행 VLA 파이프라인에 조합 적용한 것으로, 근본적으로 새로운 learning paradigm이나 representation을 제시하지는 않는다.
- VQA 형태의 기존 VLA 자율주행(EMMA, DrivingGPT 등)과 달리 명시적 cross-modal 상호작용과 policy-training-free trajectory 최적화를 분리했다는 점은 차별점이나, 각 구성요소(OT fusion, normalizing flow, risk cost map)의 개별 기여도를 검증하는 ablation이 본문에서 확인되지 않는다.
- 경쟁 방법(GaussianFusion, DriveSuprim, WAM-Flow) 대비 개선폭이 대부분 1~3pp 수준으로 크지 않아 novelty 대비 실증적 우위가 두드러지지 않는다.

**Benchmark results**

- NAVSIM navtest에서 PDMS 92.2(WAM-Flow 90.3, GoalFlow 90.3 대비 개선), EPDMS 87.0(GaussianFusion 85.0 대비 +2.0).
- Bench2Drive closed-loop에서 VLR-Driver 대비 Driving Score +2.44, Success Rate 56.00%(50.00% 대비 +6.00pp).
- nuScenes open-loop 평균 L2 0.30m, Collision 0.21%로 SpaceDrive(0.32m/0.23%) 대비 소폭 개선.
- nuScenes 3D detection에서 mAP 73.7/NDS 77.2(BEVFormer 71.2/73.2 대비 개선).
- OT interaction, normalizing flow, trajectory refinement 등 각 구성요소에 대한 개별 ablation 결과는 본문에서 확인 불가(관련 섹션이 추출 텍스트에서 누락).

**Top-tier conference 적합성 — 55/100 · 추천 venue: CVPR/ICCV (자율주행 트랙)**

4개 대규모 벤치마크에서 다양한 최신 baseline과 비교한 종합적 실험은 강점이나, 방법론적 novelty가 기존 기법의 조합 수준이고 성능 개선폭이 제한적이며 ablation 검증이 명확히 드러나지 않아 top-tier 학회의 oral/highlight급으로 보기는 어렵다.

**추천 이유 & 누리랩 연구와의 연결점**

- optimal transport 기반 이종 modality(카메라/LiDAR/언어) 정렬 기법은 로봇 조작에서 tactile+vision+language fusion에도 적용 가능한 아이디어다.
- CHOMP 스타일 risk cost map 기반 trajectory 후처리는 정책 재학습 없이 안전성 제약을 주입하는 test-time optimization 사례로 참고할 만하다.
- 다중 궤적을 flow matching denoising 중간 상태에서 그대로 추출하는 방식은 manipulation의 multi-modal action generation에도 이식 가능하다.

---

### 15. [38점] Graph-Operator World Models for Morphology-Parameter Generalization in Continuous Control

- **분야**: World Model / Robot Learning · **robotics relevance**: 8/10
- **arXiv**: [2608.20936](https://arxiv.org/abs/2608.20936) ([PDF](https://arxiv.org/pdf/2608.20936))
- **저자**: Xu Yang, Yiqin Yang, Qianchuan Zhao
- **카테고리**: Artificial Intelligence (cs.AI) · 신규 목록 게재: cs.AI
- **원문 검토**: PDF 전문 · 1차 스크리닝 60점

> 💡 articulated 로봇의 morphology를 attributed graph로 표현하고, transition을 morphology-독립적인 local dynamics basis와 morphology-조건부 structured operator(node-local modulation + kinematic-tree coupling + low-rank global correction)로 분해하는 Graph-Operator World Model(GraphOp-WM)을 제안한다. Hopper/Walker2d/HalfCheetah에 대한 interpolation/extrapolation/held-out composition MuJoCo 벤치마크를 설계했으나, 논문 본문에는 실제 실험 결과가 포함되어 있지 않다.

**Core innovation & methodology**

- 로봇의 body/joint를 attributed graph로 표현하고, transition을 공유되는 morphology-independent local dynamics basis(B̄_t)와 morphology-conditioned operator(A_{m,t})의 곱으로 분해한다(Ẑ_{t+1}=Z_t+A_{m,t}B̄_t).
- operator는 identity + diagonal(node-local) + incidence-matrix(kinematic-tree coupling) + low-rank(global correction) 4개 항으로 구조화되어 관절 로봇의 locality/kinematic 구조를 반영한다.
- architectural information separation(local kernel은 정적 morphology 파라미터를 전혀 보지 못함), basis normalization, paired-morphology supervision(동일 pose·action에서 서로 다른 morphology operator로 나온 결과를 비교하는 pairwise loss)으로 morphology 의존성이 operator 경로로만 흐르도록 강제한다.
- graph-level readout과 edge-wise action 표현으로 TD-MPC2 스타일 planning(MPC/CEM)과 호환되는 인터페이스를 설계, 가변 body/actuator 수에도 대응 가능한 fixed-dimension reward/value head를 사용한다.

**Novelty vs. prior works**

- morphology를 conditioning vector로 단순히 주입하는 기존 방법(QWM, WestWorld, particle-based graph world model)과 달리, '어떤 부분이 재사용 가능하고 어떤 부분이 morphology에 따라 바뀌어야 하는가'를 아키텍처 수준에서 명시적으로 분리한다는 problem formulation 자체는 새로운 관점을 제공한다.
- NerveNet, Shared Modular Policies, MetaMorph, Body Transformer 등 기존 morphology-conditioned control 연구는 policy 전이에 초점을 맞춘 반면, 이 논문은 predictive dynamics(world model) 쪽에 동일한 아이디어를 적용한다는 차별점이 있다.
- 그러나 본문에 실제 실험 결과(정량적 dynamics prediction 정확도, planning 성능, baseline 비교)가 전혀 제시되지 않아 제안된 구조적 분해가 실제로 효과가 있는지는 검증되지 않는다. 벤치마크 split 정의(Table 1)까지만 제시되고 곧바로 'Conclusion'으로 종료된다.

**Benchmark results**

- 본문에서 확인 불가: 실험 결과 섹션이 존재하지 않으며, 논문은 MuJoCo parameter split(Table 1: link length/mass, torso mass, joint damping, actuator gear의 interpolation/extrapolation/held-out composition 값) 정의로 끝난다.
- 본문에서 확인 불가: GraphOp-WM과 TD-MPC2/DreamerV3/PWM 등 baseline 간의 정량적 dynamics prediction 또는 planning 성능 비교.
- 본문에서 확인 불가: paired-morphology supervision, low-rank global correction 등 각 구성요소의 ablation 효과.
- 벤치마크 자체는 Hopper/Walker2d/HalfCheetah 3개 family에 대해 training envelope, interpolation set, extrapolation set(예: link length 0.60~0.75 / 1.25~1.40), held-out composition(예: distal link 1.25 + actuator gear 0.70)을 구체적 수치로 정의했다(Table 1).

**Top-tier conference 적합성 — 35/100 · 추천 venue: 워크숍 논문 수준 (현재 상태로는 CoRL/L4DC 등 main track 부적합)**

관절 로봇 world model의 morphology 일반화라는 problem formulation과 graph-operator 분해 아이디어는 흥미롭지만, 논문에 실험 결과가 전혀 포함되어 있지 않아 technical/empirical conviction을 전혀 검증할 수 없다. 제안된 벤치마크 정의만으로는 top-tier 학회 리뷰를 통과하기 어렵고, 현재 상태는 실험 섹션이 누락된 초안 또는 포지션 페이퍼에 가깝다.

**추천 이유 & 누리랩 연구와의 연결점**

- morphology-independent basis와 morphology-conditioned operator를 분리하는 아이디어는 world model 기반 test-time optimization·embodiment-transfer 연구에서 '재사용 가능한 dynamics'를 설계하는 참고 틀로 활용할 수 있다.
- paired-morphology supervision(동일 상태·행동에서 서로 다른 embodiment의 반응을 대조)은 cross-embodiment 로봇 학습이나 sim-to-real gap 분석에 응용할 수 있는 아이디어다.
- 다만 실험적 검증이 전무하므로 실제 도입 전에 저자의 후속 실험 결과나 코드 공개를 확인한 뒤 재평가가 필요하다.

---

## 오늘의 핵심 연구 트렌드 종합

- **World-Action Model의 적응적·통합적 진화** — RISE는 world action model의 imagination depth를 매 rollout마다 scene-dependent하게 결정하는 sequential stopping을 도입했고, WA-JEPA는 V-JEPA의 masking·회귀 방식을 future-masking과 flow matching으로 바꿔 future prediction과 action generation을 하나의 predictor로 통합했다. 둘 다 자율주행 도메인이지만 방법론은 manipulation VLA에도 바로 전이 가능하다.
- **world model teacher를 경량화해 VLA에 주입하는 distillation 흐름** — ForeTime-VLA는 frozen world model teacher 없이도 causal encoder만으로 미래 접촉 정보를 반영하고, JND 기반 token compression 논문은 action 민감도를 직접 기준으로 압축 대상을 고른다. 둘 다 배포 비용을 낮추면서 world-model적 이점을 유지하려는 test-time efficiency 지향을 공유한다.
- **BC의 구조적 한계를 off-policy critic으로 보완하는 self-improvement** — Q-Planning은 대형 BC VLA는 고정한 채 소형 Q-function만 온라인 학습시켜, 성공 데모만 학습 가능한 BC와 달리 실패 rollout까지 흡수하는 비대칭성을 활용했다. 실로봇 실험에서 큰 폭의 성공률 향상(예: insert-wallet 25→80%)을 보여 오늘 배치에서 가장 높은 점수를 받았다.
- **open-world·tactile 통합 3D representation의 확장** — AffordAny는 단일 RGB에서 open-vocabulary 3D affordance를 자동 구축했고, VisTa3D는 vision-tactile 융합으로 얇은 물체 reconstruction의 한계를 드러냈으며, Stream3Dv2는 training-free streaming 방식으로 노이즈 있는 2D mask에서도 3D scene understanding을 수행했다. 세 논문 모두 로봇 조작·매핑에 필요한 object-centric 3D 표현을 실용적 방향으로 확장한다.
- **VLA·world-model agent의 안전성과 내부 신뢰성 검증** — CertVLA는 continuous action chunk에 대한 최초의 certified defense를, CIVA는 critic이 유도하는 저차원 value-subspace를 공격 벡터로 악용할 수 있음을, CARD는 VLM의 belief 표현이 실제로 action 예측에 routing되지 않는 실패를 각각 규명했다. 세 연구 모두 '언제 정책을 신뢰할 수 없는가'를 사전에 진단하는 문제의식을 공유한다.
- **RL post-training에서 annotation을 oracle rollout으로 직접 활용하는 방법론** — OraRL은 정답 annotation을 on-policy group에 oracle rollout으로 추가할 때 발생하는 advantage inversion을 규명하고 decoupled advantage estimator로 해결했다. video MLLM 대상이지만 demo-guided RL/IL 융합 학습법으로 로봇 정책 학습에 전이 가능한 일반적 기법이다.

## 유망 연구 방향 및 프로젝트 제안

**Manipulation VLA를 위한 적응적 test-time imagination budget 제어**
- research question: manipulation 조작 중 접촉 직전/실패 위험 구간처럼 정보가 필요한 순간에만 world model rollout depth를 늘리고, 단순 구간에서는 rollout을 생략해 latency와 성공률을 동시에 개선할 수 있는가?
- 접근·novelty: RISE의 Latent Evaluator/Rollout Gate 구조를 ForeTime-VLA의 causal future-token distillation과 결합해, 배포 시 world model teacher 없이도 scene-dependent stopping 신호로 imagination budget을 조절하는 경량 게이팅 모듈을 설계한다.
- 왜 지금·경쟁 prior works: 두 논문 모두 2026-08-24 배치에서 각각 74점/73점으로 독립적으로 제안된 인접 아이디어이며, 아직 결합된 사례가 없다. 기존 manipulation world-model VLA(Cosmos Policy, DECOWAM 등)는 고정 rollout 스케줄을 사용한다.
- risk·target venue: 두 메커니즘의 학습 신호(future planning gain vs. contact phase)가 상충할 위험이 있어 공동 학습 curriculum 설계가 핵심 리스크다. target venue는 CoRL/ICRA.

**실패 rollout을 흡수하는 self-improving critic과 failure diagnosis의 결합**
- research question: Q-Planning의 off-policy critic이 학습한 실패 신호를, CIVA가 밝힌 critic-induced value-subspace 분석과 결합해 '어떤 실패가 왜 발생했는지'까지 설명 가능한 self-improvement loop로 확장할 수 있는가?
- 접근·novelty: 배포 후 수집된 실패 rollout에서 critic gradient 기반 저차원 subspace를 추출하고, 이 subspace의 변화 패턴을 실패 유형(grasp slip, contact timing 오류 등) 진단 신호로 재해석하는 auxiliary head를 Q-Planning 구조에 추가한다.
- 왜 지금·경쟁 prior works: CIVA는 world-model agent의 취약점 규명(공격) 관점에서 critic subspace를 다뤘고 Q-Planning은 self-improvement 관점에서 critic을 다뤄 문제의식이 상보적이다. V-GPS, DSRL 등 기존 value-guided 방법은 진단 기능이 없다.
- risk·target venue: subspace 해석이 실제 실패 원인과 대응되는지 검증하는 real-robot ablation이 필요해 실험 비용이 크다. target venue는 CoRL/RSS.

**tactile 기반 open-world affordance grounding으로 얇은/변형 물체 조작 확장**
- research question: AffordAny의 open-vocabulary 3D affordance grounding에 VisTa3D의 vision-tactile fusion을 결합하면, 시각만으로는 인식이 어려운 얇은 물체(케이블, 카드 등)의 grasp affordance를 zero-shot으로 예측할 수 있는가?
- 접근·novelty: AffordAny의 frozen VLM feature + 3D geometry decoder에 VisTa3D의 Tactile-DC 방식(tactile latent를 fused feature map에 주입)을 접목해, 시각 기반 affordance 예측이 낮은 confidence를 보이는 영역에서 tactile probing으로 보완하는 active affordance refinement를 설계한다.
- 왜 지금·경쟁 prior works: 두 논문 모두 오늘 배치에서 독립적으로 open-world 3D 조작 인식을 다뤘으나 결합 사례가 없고, VisTa3D 저자도 얇은 물체에서 순수 vision 기반 11개 기존 방법이 모두 저조함을 실증했다.
- risk·target venue: AffordAny의 데이터셋에는 tactile 라벨이 없어 별도 수집이 필요하다. target venue는 CoRL/RSS(Dataset & Benchmark 병행).

**streaming 3D scene graph와 active perception의 결합**
- research question: Stream3Dv2의 training-free streaming 3D instance segmentation을 이용해, 다음에 어디를 관측해야 할지(NBV)를 static/dynamic instance 분류 결과에 기반해 온라인으로 결정하는 active perception policy를 만들 수 있는가?
- 접근·novelty: Stream3Dv2의 3D bounding box 기반 static/dynamic 인스턴스 분류와 LLM agent 결합 부분을 확장해, 불확실성이 높은(아직 병합되지 않은) instance 영역을 다음 관측 목표로 선택하는 information-gain 기반 view selection 모듈을 추가한다.
- 왜 지금·경쟁 prior works: 기존 open-vocabulary 3D segmentation(MaskClustering, OVIR-3D 등)은 offline full-sequence를 가정해 active perception과 결합하기 어려웠는데, Stream3Dv2는 streaming 제약 하에서 이미 이 문제를 풀었다.
- risk·target venue: 순수 geometric-semantic fusion 알고리즘(SCP/SPP, Eikonal)의 계산 비용이 실시간 NBV 루프에 적합한지 검증이 필요하다. target venue는 CVPR/ICRA.

**demo-guided RL의 advantage inversion 문제를 로봇 정책 RL/IL 융합에 전이**
- research question: OraRL이 video MLLM RL에서 규명한 'oracle rollout이 group baseline을 왜곡해 advantage가 뒤집히는' 문제가, expert demonstration을 oracle rollout으로 사용하는 로봇 정책 GRPO 계열 fine-tuning에서도 동일하게 발생하는가?
- 접근·novelty: OraRL의 decoupled advantage estimator와 sign-balanced pruning을 로봇 manipulation VLA의 RL fine-tuning(예: RLPD류)에 이식해, expert demo를 직접 oracle rollout으로 주입하면서도 advantage inversion 없이 학습 안정성을 확보하는 실험을 설계한다.
- 왜 지금·경쟁 prior works: 로봇 RL/IL 융합 연구는 대개 demo를 replay buffer에 섞는 방식에 머물러 있어, oracle rollout을 on-policy group에 직접 포함시키는 OraRL식 접근이 아직 적용된 바 없다.
- risk·target venue: video MLLM의 discrete task reward와 달리 로봇 조작은 continuous action이라 advantage 정의 자체를 재설계해야 한다. target venue는 CoRL/ICML.

## 오늘 반드시 읽어야 할 논문

- [Beyond Imitation: Self-Improving Robot Policies via Off-Policy Q-Planning](https://arxiv.org/abs/2608.21204) — BC를 고정한 채 소형 critic만 온라인 학습시켜 실로봇 성공률을 최대 55%p 끌어올린, 오늘 배치 최고점(80) 논문.
- [WA-JEPA: Rethinking the Video JEPA Paradigm for World-Action Modeling in Autonomous Driving](https://arxiv.org/abs/2608.20974) — JEPA의 semantically rich feature space를 유지한 채 future prediction과 action generation을 하나의 flow-based predictor로 통합.
- [RISE: Adaptive Imagination for World Action Models](https://arxiv.org/abs/2608.20430) — world action model의 rollout depth를 scene마다 다르게 결정하는 test-time adaptive computation 메커니즘.
- [CertVLA: Certified Defense against Physical Visual Attacks for Vision-Language-Action Models](https://arxiv.org/abs/2608.20791) — continuous VLA action chunk에 대한 최초의 certified defense, conformal calibration으로 finite-sample 보장을 제공.
- [ForeTime-VLA: Causal Future-Token Distillation from a World Action Model for Conveyor-Belt Manipulation](https://arxiv.org/abs/2608.20735) — world model teacher 없이 배포 가능한 경량 causal encoder로 실로봇 파지 성공률을 12~22%p 향상.
- [AffordAny: Open-World 3D Affordance Grounding from Monocular RGB Images](https://arxiv.org/abs/2608.20720) — 단일 RGB에서 473개 카테고리 open-vocabulary 3D affordance를 자동 구축해 grasp/manipulation point 예측에 바로 활용 가능.
- [Annotations as Rollouts: Efficient and Scalable Reinforcement Learning for Video MLLMs](https://arxiv.org/abs/2608.20492) — oracle rollout이 advantage baseline을 왜곡하는 현상을 규명하고 해결한, RL/IL 융합 학습에 전이 가능한 방법론.
- [CIVA: Critic-Induced Value-Subspace Attacks on Visual World-Model Agents](https://arxiv.org/abs/2608.21114) — world-model agent의 critic이 유도하는 저차원 방향이 공격에도 취약함을 보여, 안전-critical 로봇 배포 전 진단에 시사점을 준다.
- [CARD: Diagnosing Belief to Action Routing Failures in Vision Language Models](https://arxiv.org/abs/2608.20763) — VLM의 belief 표현이 encoded되어도 실제 협력 행동 예측에는 반영되지 않는 routing failure를 처음으로 진단.
- [Stream3Dv2: Geometric-Semantic Fusion Enhanced Streaming Zero-Shot 3D Scene Understanding](https://arxiv.org/abs/2608.21136) — training-free streaming 방식으로 노이즈 있는 2D mask에서도 offline 방법과 동등 이상의 3D scene understanding을 실시간으로 수행.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (320편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2608.20430'>RISE: Adaptive Imagination for World Action Models</a></td><td>78</td><td>7</td><td>World Model</td><td>자율주행 world action model에서 상황별로 imagination rollout 길이를 적응적으로 조절하는 Roll/Stop 정책을 제안하며, CounterDrive라는 counterfactual 데이터셋으로 risk 감독을 제공한다. NAVSIM/nuScenes에서 성능과 계산 효율을 동시에 개선하고 다양한 WAM 아키텍처에 대한 plug-in 일반성도 보여 test-time planning 주제와 잘 맞는다.</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2608.20974'>WA-JEPA: Rethinking the Video JEPA Paradigm for World-Action Modeling in Autonomous Driving</a></td><td>76</td><td>7</td><td>World Model</td><td>random masking와 deterministic regression에 기반한 V-JEPA를 미래-마스킹 pre-training과 conditional flow matching으로 재정식화해 world-action model로 만든 연구이다. future-action predictor로 action supervision이 world representation을 직접 형성하게 하며 NAVSIM-v2에서 최강 world-action baseline 대비 1.3 EPDMS, closed-loop HUGSIM에서도 최고 성능을 보여 world model 학습 패러다임 자체를 재고한 기여가 크다.</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2608.20720'>AffordAny: Open-World 3D Affordance Grounding from Monocular RGB Images via Vision-Language-Guided Geometric Reasoning</a></td><td>74</td><td>8</td><td>Manipulation</td><td>단일 monocular RGB로부터 open-world 3D affordance grounding을 수행하며 frozen VLM 기반 decoder와 pseudo-label self-training으로 카테고리 일반화를 달성한다. 473개 카테고리로 기존보다 훨씬 큰 다양성의 벤치마크를 구축했고 unseen category에서도 0.315 IoU를 보여, 로봇 조작의 핵심인 affordance grounding에 직접 기여한다.</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2608.20735'>ForeTime-VLA: Causal Future-Token Distillation from a World Action Model for Conveyor-Belt Manipulation</a></td><td>72</td><td>10</td><td>VLA</td><td>frozen world-action-model teacher로부터 future token을 causal하게 distillation하여 pi0.5 기반 VLA에 결합했고, 실제 로봇 conveyor-belt grasping에서 pi0.5 대비 이동 물체 성공률을 12~22%p 높였다.</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2608.20791'>CertVLA: Certified Defense against Physical Visual Attacks for Vision-Language-Action Models</a></td><td>72</td><td>8</td><td>VLA</td><td>패치·텍스처 공격에 대해 closed-loop VLA 정책의 연속적 action chunk를 인증하는 최초의 certified defense로, dual-mask covering과 finite-sample coverage 보장을 이론적으로 증명하고 시뮬레이션과 실제 로봇 실험으로 검증한다. VLA의 물리적 공격 강건성이라는 중요한 새 문제 설정을 다룬다.</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2608.21247'>Just Noticeable Difference Modeling for Token Compression in Vision-Language-Action Models</a></td><td>72</td><td>8</td><td>VLA/Efficient Inference</td><td>인간 시각의 Just Noticeable Difference 개념을 VLA 정책의 closed-loop action 응답으로 확장한 Action-JND를 제안해, 토큰 변화가 action 편차로 이어지지 않는 허용 범위를 예측한다. LIBERO에서 OpenVLA/OpenVLA-OFT에 stale-KV reuse와 token pruning의 plug-in 기준으로 적용해 공격적인 압축률에서도 신뢰성을 높였으며, embodied token compression을 위한 새로운 문제 정식화이다.</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2608.21136'>Stream3Dv2: Geometric-Semantic Fusion Enhanced Streaming Zero-Shot 3D Scene Understanding</a></td><td>68</td><td>7</td><td>3D Vision/Embodied AI</td><td>streaming RGB-D 입력을 nested local-to-historical 구조로 처리하며 3D segmentation을 point-and-set merge/partition 문제로 재정식화해 잡음이 섞인 2D mask에서도 강건한 training-free zero-shot 3D scene 이해를 달성한다. LLM agent와 결합해 open-world embodied intelligence 가능성을 보여 로봇의 실시간 open-vocabulary scene understanding에 직접 관련된다.</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2608.20492'>Annotations as Rollouts: Efficient and Scalable Reinforcement Learning for Video MLLMs</a></td><td>68</td><td>3</td><td>RL/Video</td><td>video MLLM RL post-training에서 annotation을 oracle rollout으로 직접 활용하는 decoupled advantage estimator를 제안해 advantage inversion 문제를 해결하고, GRPO 대비 샘플 효율과 성능(VSI-Bench 73.1 vs GPT-5 55.0)을 크게 개선한다. RL 학습 패러다임 측면에서 로봇 정책 학습에 참고할 만하다.</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2608.20740'>VisTa3D: A Dataset and Benchmark for Thin Object Reconstruction from Vision, Tactile, and 3D Point Clouds</a></td><td>66</td><td>7</td><td>Tactile Perception</td><td>RGB, depth, tactile response map을 동기화해 수집한 최초의 thin object 데이터셋을 제시하고 tactile 정보를 활용한 visual-range-tactile 3D reconstruction 베이스라인을 제안한다. 얇은 물체 재구성이라는 기존 3D 모델의 한계를 tactile perception으로 보완하는 시도로 로봇 조작과 밀접하다.</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2608.21114'>CIVA: Critic-Induced Value-Subspace Attacks on Visual World-Model Agents</a></td><td>64</td><td>6</td><td>World Model/RL Security</td><td>DreamerV3 같은 시각 world-model agent의 critic이 유도하는 저차원 value-subspace에 공격이 집중된다는 관찰에 기반해 offline로 subspace를 추출하고 test-time에는 그 계수만 최적화하는 새로운 공격을 제안한다. DMC walker walk에서 26.07%의 보상 하락을 유발하며 world model 기반 RL agent의 취약성을 규명한 새로운 문제 설정이다.</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2608.21204'>Beyond Imitation: Self-Improving Robot Policies via Off-Policy Q-Planning</a></td><td>62</td><td>9</td><td>Manipulation</td><td>behavior cloning 정책에 소형 off-policy Q-function을 결합해 추론 시 Q-weighted action selection을 수행하고, Q-function만 재학습하며 자기 개선하는 Q-Planning을 제안했으며, 실제 양팔 로봇에서 stack-cups 40%→90%, insert-wallet 25%→80%로 인간 개입 없이 성능을 끌어올렸다.</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2608.20890'>A Collaborative Multi-Modality Interaction for VLA-based End-to-End Autonomous Driving</a></td><td>62</td><td>6</td><td>VLA</td><td>VQA 형태로 정식화되던 기존 VLA 자율주행과 달리 optimal transport 기반 주-보조 modality 상호작용과 multi-trajectory planning을 결합해 해석 가능성과 long-tail 상황 대응력을 높인다. VLA 기반 자율주행이라는 우선 주제와 관련이 크다.</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2608.20763'>CARD: Diagnosing Belief to Action Routing Failures in Vision Language Models</a></td><td>62</td><td>5</td><td>Embodied AI/VLM Interpretability</td><td>VLM 내부의 belief 표현이 실제 행동 예측에 활용되는지를 진단하는 Cross-Axis Routing Diagnostic을 협력적 grid-world 벤치마크에서 검증하며, 모델이 파트너의 belief 정보를 행동 예측에 반영하지 못하는 routing failure를 규명한다. 멀티에이전트 상호작용을 다루는 embodied 정책의 실패 진단이라는 새로운 문제 설정을 제시한다.</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2608.21008'>Triangulation-Free Bundle Adjustment with Graduated Non-Convexity for Camera Pose Refinement from Coarse Priors</a></td><td>62</td><td>5</td><td>3D Vision/SLAM</td><td>prior pose를 triangulation 없이 ray당 depth로 재표현해 매 iterate마다 구조를 갱신하는 bundle adjustment로, 기존 refiner가 정확한 ARKit prior를 오히려 악화시키는 문제를 해결한다. graduated non-convexity로 32도 perturbation까지도 CPU 10초 만에 복원하며 학습된 refiner보다 우수해 로봇 navigation/localization에 참고할 만하다.</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2608.20936'>Graph-Operator World Models for Morphology-Parameter Generalization in Continuous Control</a></td><td>60</td><td>8</td><td>World Model</td><td>관절형 로봇의 morphology를 attributed graph로 표현하고 transition을 morphology-독립 기저와 morphology-조건 연산자로 분해하는 새로운 world model 구조로, Hopper/Walker2d/HalfCheetah에서 unseen morphology로의 interpolation·extrapolation 일반화를 목표로 한다.</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2608.20534'>Grounded-Exo2Ego: Structured Semantic Grounding for Robust Exocentric-to-Egocentric Video Generation</a></td><td>60</td><td>5</td><td>Video/Embodied AI</td><td>exocentric에서 egocentric 영상을 생성하는 dual-branch diffusion 구조로 geometric anchoring과 semantic grounding을 결합하고 camera re-localization으로 misalignment 문제를 해결한다. EgoExo4D에서 큰 폭의 성능 향상을 보이며 exo demonstration으로부터 ego 시점 데이터를 만든다는 점에서 embodied 학습에 응용 가능성이 있다.</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2608.20659'>Lift, Associate, and Fuse: A Decision-Centric Framework for 2D-to-3D Foundation Model Transfer</a></td><td>60</td><td>5</td><td>3D Vision</td><td>2D-to-3D foundation model transfer 시스템을 Generate/Associate/Reconcile/Fuse/Persist 다섯 연산자로 분해하는 decision-centric 프레임워크를 제안하고 161개 시스템을 감사하며, association과 identity를 구분하는 등 object-centric 3D 표현 설계에 대한 일반화 가능한 분석 도구를 제공한다.</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2608.21319'>Unified Branch-and-Bound Search for the Steiner Traveling Salesman Problem on Graphs of Convex Sets</a></td><td>58</td><td>8</td><td>TAMP/Planning</td><td>Graphs of Convex Sets 위에서 optional transit과 revisit을 허용하는 Steiner-TSP를 branch-and-bound로 풀며 유한 종료와 epsilon-suboptimality 보장을 증명하고, mobile-manipulator inspection task에서 LTL 제약까지 포함한 sensing-순서-궤적 통합 계획을 시연했다.</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2608.20401'>World models of environment, agent and joint agent-environment systems</a></td><td>58</td><td>6</td><td>World Model</td><td>computational mechanics의 epsilon-machine 개념을 이용해 world model이 모델링하는 channel을 environment/agent/joint 세 가지로 구분하고, closed-loop coupling에서 유도되는 canonical support-restricted 모델과 그 상태 구조를 이론적으로 정의한다. world model에 대한 일반화 가능한 이론적 틀을 제공하는 보기 드문 기초 연구지만 실증 사례는 POMDP 예시 하나뿐이다.</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2608.20699'>ArtiMo: Agent-Driven Articulated Mesh Animation</a></td><td>58</td><td>5</td><td>3D Vision/Embodied AI</td><td>URDF의 kinematic 제약과 LLM/VLM agent의 reasoning을 결합해 zero-shot으로 articulated mesh를 애니메이션하고 렌더링된 keyframe으로 스스로 오류를 교정하는 self-improvement loop를 가지며, articulated object의 인과적 part motion 처리는 로봇 조작 이해에 참고할 만하다.</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2608.20687'>TopoSurfel: Closing the Loop between Gaussian Surfels and Meshes for Surface Reconstruction</a></td><td>58</td><td>4</td><td>3D Vision</td><td>Gaussian surfel과 연속 mesh를 non-trainable differentiable iso-surfacing으로 연결하고 mesh-guided surfel evolution으로 3DGS 표면 재구성의 floater와 hole 문제를 개선하며, 3DGS 기반 object-centric 표현과 관련이 있다.</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2608.21160'>Human-JEPA: A Human-Centric Vision Model that Perceives and Anticipates</a></td><td>56</td><td>4</td><td>Representation Learning/Video</td><td>past-to-future split과 anchored forecasting으로 dense perception 붕괴 없이 pose·re-id와 anticipation을 동시에 다루는 human-centric JEPA 모델을 제안하며, 2.7배 적은 파라미터로 pixel-anchored 전문가 모델을 능가한다. 사람 행동 예측 능력은 HRI/사회적 항법에 활용될 수 있다.</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2608.21031'>PhysCaP: Grounding Code-as-Policy Agent with Physics-Informed Exploration</a></td><td>55</td><td>9</td><td>Manipulation</td><td>code-as-policy 에이전트에 물리 정보 기반 탐색 레이어를 추가한 PhysCaP는 로봇 proprioception만으로 질량/강성을 훈련 없이 추정하고 Planner-Prioritizer 이중 에이전트로 탐색 비용을 줄이며, 실제 tabletop 과제와 LIBERO 시뮬레이션 모두에서 기존 passive/naive interactive baseline을 능가했다.</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2608.20478'>EndoLIFT: Language-Disambiguated Latent-Conditioned Rectified Flow for Bidirectional Endoscopic Control</a></td><td>55</td><td>8</td><td>VLA</td><td>내시경의 intent aliasing 문제를 언어 조건화와 32차원 trajectory latent 기반 rectified flow로 해결하는 VLA 정책 EndoLIFT를 제안했으며, latent 유무 비교로 방향 정확도를 11.1%p 개선하고 ex-vivo porcine 실험 10/10 성공을 보였다.</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2608.21066'>Robust Validation to Geometric Perturbations for Autonomous Pose Estimation</a></td><td>55</td><td>5</td><td>Robotics Perception/Certification</td><td>기존 gradient 기반 공격이 pose estimation에서 random sampling보다 못한 성능을 보임을 밝히고, Global Lipschitzian Optimization으로 강한 수렴 보장을 갖는 robust validation을 제안한다. YOLOv8-Pose+PnP에서 안전 한계를 벗어나는 실패 모드를 탐색 공간의 80% 이상을 가지치기하며 찾아내 자율 항법·착륙의 인증 가능한 검증에 기여한다.</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2608.21170'>Is Visual Prompting All You Need? Studying VLM Spatial Reasoning under Progressive Visual Scaffolds</a></td><td>55</td><td>5</td><td>Embodied Spatial Reasoning</td><td>grid 기반 공간 계획 벤치마크 SPaRC에서 시각적 표현 방식이 grounding과 reasoning 실패를 어떻게 가르는지 분석하고, 경량 visual scaffold만으로 최대 34.0%p의 정확도 향상을 보인다. VLM의 embodied spatial reasoning 실패 원인을 분해한 분석적 기여가 있다.</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2608.21093'>Gaussian-Mixture Latent Flow for Stochastic 3D Human Motion Prediction</a></td><td>55</td><td>4</td><td>Motion Prediction</td><td>data-driven Gaussian mixture prior를 갖는 latent flow 모델로 확률적 3D human motion 예측의 plausibility와 uncertainty quantification을 함께 개선하며, invertible 구조로 tractable likelihood를 제공한다. 사람 동작 예측은 로봇의 사회적 항법·HRI에 활용될 수 있다.</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2608.20682'>Aristotelian Manifolds: Leveraging Platonic Perceptual Features for Backpropagation Free Rapid Concept Learning</a></td><td>55</td><td>3</td><td>Representation Learning</td><td>Platonic Representation Hypothesis에 기반해 foundation model의 layer별 latent geometry가 도메인마다 다른 profile을 보임을 규명하고 backpropagation 없이 layer 선택과 feature 압축이 가능함을 보이지만, 검증이 개념적 특성화 수준에 머문다.</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2608.20882'>LoRC: Detecting AI-Generated Images via Low-Rank Collapse in Semantic Residuals</a></td><td>55</td><td>0</td><td>CV</td><td>생성 모델의 디코딩 병목에서 나타나는 semantic-residual 부분공간의 low-rank collapse라는 architecture-agnostic 지표를 발견해 39개 미지 생성기에서 97.0% 정확도를 달성하는 등 일반화 성능이 강하지만 이미지 포렌식에 국한되어 로봇 관련성은 없다.</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2608.20556'>Logic-VLA: A Temporal Logic Conditioned Vision-Language-Action Model</a></td><td>54</td><td>8</td><td>VLA</td><td>Signal Temporal Logic 명세를 추론 시점에 조건으로 받는 Logic-VLA를 제안해 STL 만족률을 24.8~40.7%p 개선하면서 자연어 과제 성공률 저하를 1.8%p 이내로 유지했으며, VLA에 형식 명세를 결합한 새로운 문제 설정이 돋보인다.</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2608.20546'>Koala Gripper: Co-designing Robotic Grippers and Data-Capture Devices for Scaling Dexterous Manipulation Learning</a></td><td>52</td><td>8</td><td>Manipulation</td><td>데이터 수집 장치와 로봇 그리퍼를 동시에 설계하는 co-design 프레임워크로 Koala Gripper를 제안하고, force-optimized 링크 기구와 backdrivable finger로 parallel jaw 대비 dexterity와 grasp 능력을 향상시켰다.</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2608.21055'>CoAnchor: Robust Collaborative Perception under Spatio-Temporal Misalignment via Object-Level Anchors</a></td><td>52</td><td>5</td><td>Autonomous Driving/Perception</td><td>dense BEV 대신 sparse object-level anchor를 공유 인터페이스로 삼아 통신 지연과 pose noise를 하나의 loop에서 함께 보정하는 협력 인지 프레임워크로, 통신 지연 상황에서도 실용적 accuracy-efficiency trade-off를 보인다.</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2608.20909'>Decoupling Policy Extraction for Offline Reinforcement Learning</a></td><td>52</td><td>5</td><td>RL</td><td>offline RL에서 actor와 critic 학습을 분리해 critic으로 여러 후보 action을 rerank하는 decoupled policy extraction paradigm을 제안하고, naive Q-learning critic으로도 behavior cloning과 결합 학습 방식을 능가함을 보였다.</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2608.20788'>M2Depth: Unifying Monocular Depth Foundation Priors with Multi-View Stereo</a></td><td>52</td><td>4</td><td>3D Vision</td><td>monocular depth foundation model과 cascade MVS를 양방향으로 상호 보정하는 프레임워크로 scale ambiguity와 occlusion 영역의 depth 완전성을 함께 개선하며, 로봇의 depth 인식 파이프라인에 참고할 만하다.</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2608.21286'>Difficulty-Calibrated Interpolation Paths for Conditional Flow Matching</a></td><td>52</td><td>3</td><td>Generative/Efficient Training</td><td>conditional flow matching의 interpolation schedule을 고정하지 않고 pilot run의 per-time loss로부터 모델 스스로 도출하는 Difficulty-Calibrated Flow Matching을 제안한다. 약 2%의 오버헤드만으로 large-batch, few-update 환경에서 고정 schedule보다 우수해 로봇 policy에 쓰이는 flow matching 학습에도 참고할 만하다.</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2608.20841'>Foundation Models for Partial Causal Identification</a></td><td>52</td><td>3</td><td>Causal Reasoning</td><td>구조적 인과 모델 공간에 대한 canonical prior를 정의해 counterfactual bounding을 함수 학습 문제로 재정식화한 이론적 기여로 causal foundation model paradigm을 partial identifiability로 확장한다.</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2608.20473'>Aggregating Visual Information with Optimal Transport for VideoLM Token Compression</a></td><td>52</td><td>2</td><td>Video</td><td>optimal transport로 video token compression을 정식화해 질문 조건과 공간적 다중 해상도를 함께 반영하는 새로운 접근이나, 로봇 태스크와의 직접적 연결은 제한적이다.</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2608.20910'>InfinityEdit: Infinite Video Editing with a Lightweight Edit-Ignition Adapter</a></td><td>52</td><td>1</td><td>Video Generation</td><td>고정된 clip 대신 열린 스트림에 지속적으로 편집을 적용하는 infinite video editing이라는 새 태스크를 정의하고 경량 adapter로 무한 길이 스트림에서 안정적 편집을 구현하지만 로봇 관련성은 낮다.</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2608.21027'>Don&#x27;t Solve, Just Compare: Tiny Advisors for Runtime Intervention in LLM Agents</a></td><td>50</td><td>5</td><td>Agent/Failure Recovery</td><td>비교만 수행하는 tiny comparator로 runtime intervention 시점과 대안을 제시하는 새로운 방식으로, actor보다 훨씬 약한 auxiliary 모델로도 WebShop·ALFWorld 등에서 성능을 개선해 failure detection·recovery에 아이디어를 준다.</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2608.21134'>Llama-Mobile: Efficient 2.7-Bit Quantization of VLMs</a></td><td>50</td><td>4</td><td>Efficient Inference</td><td>모델 스스로 생성한 데이터로 학습 없이 VLM을 2.7-bit로 양자화하는 파이프라인으로 Llama 3.2 11B Vision을 3.7GB로 압축하면서 VQA 성능을 유지한다. 모바일·엣지 배포 효율화는 온-로봇 VLA/VLM 실행에도 참고할 수 있다.</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2608.21244'>A VLM Answer Is Not an Anomaly Score: Rank Compression in Training-Free Video Anomaly Detection</a></td><td>50</td><td>3</td><td>Video/Anomaly Detection</td><td>training-free VLM 기반 video anomaly detection에서 generated answer만 사용하면 서로 다른 답변 분포가 같은 점수로 뭉개지는 rank compression이 발생함을 규명하고, probability readout이 4개 VLM 전반에서 5~13점 향상을 보인다. anomaly/failure detection에 쓰이는 답변 인터페이스 설계에 대한 일반화 가능한 통찰을 제공한다.</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2608.20516'>When Graph-JEPA Learns the Wrong Thing: Diagnosing and Repairing Category-Conditional Collapse</a></td><td>50</td><td>3</td><td>Representation Learning/JEPA</td><td>linear probe와 effective rank가 모두 건강해 보여도 Graph-JEPA representation이 실제로는 인스턴스 정보를 전혀 담지 못하는 category-conditional collapse를 규명하고, 이를 variance allocation 분석으로 설명한 뒤 복구한다. JEPA 계열 world model 평가에서 흔히 쓰이는 진단 지표의 함정을 경고하는 방법론적 기여가 있다.</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2608.20805'>Routing Before Looking: Query-Adaptive Evidence Acquisition for Long-form Video Understanding</a></td><td>50</td><td>2</td><td>Video</td><td>질의 유형에 따라 browse/ground/retrieve 도구를 동적으로 선택하는 routing 정책으로 장편 영상 이해의 효율과 성능을 동시에 개선하지만 로봇 active perception과의 직접적 연결은 약하다.</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2608.21030'>COMET: Contrastive Motion-Enhanced Temporal Reasoning for Video Multimodal Large Language Models</a></td><td>50</td><td>2</td><td>Video</td><td>Taylor frame difference 기반 motion branch와 forward-reverse TC-GRPO로 video MLLM의 시간적 방향 민감도를 강화해 action-centric task에서 평균 4.9% 개선을 보이며 모델 계열 간 일반화도 확인했으나 로봇 응용과의 직접 연결은 제한적이다.</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2608.20942'>LHMCF-Net: A Learned Hyperbolic Mean Curvature Flow Network for Medical Images Segmentation</a></td><td>50</td><td>0</td><td>CV/Medical</td><td>second-order hyperbolic PDE 기반 mean curvature flow를 deep unfolding network로 구현해 저대비 의료 영상 분할을 개선하며 물리 기반 딥러닝 구조라는 점은 흥미로우나 의료 도메인에 국한된다.</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2608.20480'>When Clean Data Hurts: Learning with Monotone Corruptions Beyond Binary Classification</a></td><td>50</td><td>0</td><td>Learning Theory</td><td>monotone adversarial corruption 하에서 DS dimension이 단 2인 multiclass 문제가 학습 불가능해질 수 있음을 증명하고 학습 가능성의 경계를 규명하는 PAC 학습이론 기여이나 로봇 응용과는 무관하다.</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2608.20362'>Multilingual Verifier Bias in RLVR: Benchmark, Rollout Diagnosis, and the Cross-Lingual Selection Bottleneck</a></td><td>50</td><td>0</td><td>NLP</td><td>MGSM rollout에서 exact-match verifier의 false-negative rate가 Qwen3-8B 기준 JP 0.642 대 EN 0.122로 언어별로 크게 다름을 밝히고, 이를 55-78% 완화하는 target-local aggregation을 제안한다. RLVR reward 설계에 대한 새로운 audit protocol을 제시하지만 robot learning과는 관련이 없다.</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2608.21035'>TaPeR: Probabilistic Recovery of Sparse Task Precedence Graphs from a Handful of Demonstrations</a></td><td>48</td><td>8</td><td>Manipulation</td><td>소수의 시연만으로 kinematic graph와 상대 pose 분포를 이용해 부분 순서 task precedence graph를 확률적으로 복원하는 TaPeR를 제안했으며, 명시적 symbolic predicate grounding 없이 장기 과제의 다양한 유효 실행 순서를 생성할 수 있다.</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2608.21290'>VT-MUSE: Multimodal Unified Sequential Visuotactile Representation Learning for Manipulation</a></td><td>48</td><td>8</td><td>Manipulation</td><td>시각-촉각 관측을 2단계(모달리티별 시간 정렬 후 조건부 잠재 변수 모델)로 통합 학습하는 VT-MUSE를 제안해 시뮬레이션 벤치마크에서 가장 강한 baseline 대비 11%p 향상을 보였고 실물 실험에서도 개선을 확인했다.</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2608.21292'>AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization</a></td><td>48</td><td>5</td><td>Agent RL</td><td>skill을 teacher guidance에서 autonomous 활용으로 점진 전환시키는 action-level skill-conditioned optimization을 제안했으며 ALFWorld·WebShop에서 OOD 일반화를 포함해 성능을 개선해 skill chaining 연구에 참고할 수 있다.</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2608.20639'>MV2GF: Multi-view Pedestrian Detection with a Visual Geometric Foundation Model</a></td><td>48</td><td>3</td><td>3D Vision</td><td>visual geometric foundation model의 3D pointmap을 활용해 multi-view pedestrian detection의 카메라 설정 일반화를 개선하며, geometric foundation model 활용 방식은 로봇 3D 인식에 참고할 만하다.</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2608.21360'>OmniAssistBench: Assistant-style Interaction Benchmark for Omni-LLMs</a></td><td>48</td><td>3</td><td>Multimodal/Interactive Assistant</td><td>실시간으로 환경을 지속 인지하며 사용자를 목표로 안내하는 omni-LLM assistant를 평가하기 위해 인터넷 영상을 역설계해 multi-turn 상호작용 벤치마크를 구축한다. Gemini-3-Pro도 66.4점에 그치며 시각적 제스처 이해, 이력 유지, 적시 응답 지연 등에서 한계를 드러내 능동적 embodied assistant 평가에 참고할 만하다.</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2608.20759'>DiGS-Avatar: Single-Image Animatable 3D Human Reconstruction via UV-Space Diffusion</a></td><td>48</td><td>2</td><td>3D Vision</td><td>단일 이미지에서 애니메이션 가능한 3D human을 UV-space diffusion으로 0.71초 만에 재구성하며 teacher-student 구조로 3D 일관성을 확보하지만 인간 아바타 생성에 특화된 기여이다.</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2608.20382'>Decoupled Vision-Language System for Multimodal Understanding and Generation</a></td><td>48</td><td>2</td><td>Multimodal</td><td>Libra는 vision system과 language system을 분리하고 switch attention/FFN으로 self-modal과 cross-modal 계산을 동적으로 라우팅하는 새로운 MLLM 아키텍처로 이해와 생성 양쪽에서 상호 개선을 보인다. VLA 백본에 참고할 만한 구조적 아이디어를 제공한다.</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2608.20814'>Enhancing Localized Reasoning for Long Video Understanding via Efficient Segment-to-Video Supervision</a></td><td>48</td><td>1</td><td>Video</td><td>segment 단위 VQA를 whole-video 학습으로 전이하는 S2V 방법으로 단순 accuracy reward만으로 장편 영상 이해의 정확도와 효율을 함께 개선하지만 로봇 관련성은 낮다.</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2608.20886'>EviRank: Structured Relevance Evidence for Multimodal Image Re-ranking</a></td><td>48</td><td>1</td><td>Multimodal/Retrieval</td><td>멀티모달 이미지 re-ranking을 semantic constraint satisfaction 문제로 재정식화하고 rubric 기반 증거 검증으로 여러 벤치마크에서 SOTA를 달성하지만 검색 응용에 국한되어 로봇 관련성은 낮다.</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2608.21098'>When does fusing hand-crafted knowledge with learned representations pay? A cost-normalized benchmark of stacking, substitution, and interference</a></td><td>48</td><td>1</td><td>Representation Learning</td><td>hand-crafted prior와 학습 표현의 결합이 언제 도움이 되는지를 13개 데이터셋, 9개 backbone에 걸쳐 통제된 벤치마크로 규명하고 frozen-feature 진단으로 end-to-end 이득을 사전에 예측하는 일반화 가능한 방법론을 제시한다.</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2608.20441'>Shared Physics Responses Recover Hidden Rankings in Neural Operator Libraries</a></td><td>48</td><td>1</td><td>ML/Scientific Computing</td><td>ground-truth 없이 anchor 기반 linearized physics 응답만으로 neural operator library의 순위를 99% 이상 정확히 복원하는 일반화 가능한 진단 도구를 제안하며, 강건한 이론적 충분조건도 함께 제시한다.</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2608.21355'>ViTacPhys: Physical Property-Aware Grasping from Human Visual-Tactile Demonstrations</a></td><td>47</td><td>8</td><td>Manipulation</td><td>인간의 시각-촉각 시연으로부터 질량/마찰/강성을 추정하는 ViTacPhys를 로봇 도메인으로 전이해, 물체 물성 조건화 파지 정책으로 미지 물체에서도 83.4%의 성공률과 인간과 유사한 힘 프로파일을 보였다.</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2608.21330'>NeSAM: Neuro-Symbolic Kinodynamics with Soil Adaptation for Off-Road Mobility</a></td><td>46</td><td>7</td><td>Navigation</td><td>미분가능한 Bekker-Wong terramechanics와 Transformer 잔차 동역학, EKF 기반 온라인 토양 파라미터 추정을 결합한 NeSAM은 시뮬레이션에서 최대 30%, 실측에서 29% 예측 정확도를 개선하고 궤적 추종 Hausdorff distance를 69.4% 줄였다.</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2608.20975'>Belief Without Behavior: Measuring the Translation of Theory of Mind into Coordinated Social Action in Vision-Language Models</a></td><td>46</td><td>5</td><td>Embodied AI</td><td>verbal·nonverbal 신호를 통합해 theory of mind를 사회적 행동으로 옮기는지 측정하는 embodied benchmark로, 대부분의 VLM이 방향성 있는 nonverbal 신호 생성과 해석 모두에서 실패함을 보였다.</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2608.20748'>Generating Multi-view Adversarial Examples for Visual Geometry Grounded Transformer</a></td><td>46</td><td>3</td><td>3D Vision/Security</td><td>Visual Geometry Grounded Transformer(VGGT)에 대한 최초의 multi-view adversarial perturbation 생성기로 단일 feed-forward pass로 view 간 일관된 perturbation을 만들어 3D foundation model의 취약점을 드러내지만 공격 기법 자체의 novelty는 제한적이다.</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2608.21099'>A2DINOv3: Rethinking Multi-Modal Object Detection via Socialized Collaboration</a></td><td>46</td><td>3</td><td>CV/Detection</td><td>RGB와 적외선을 이질적 전문가로 모델링해 선택적으로만 상호작용시키는 socialized collaboration protocol로 DINOv3의 pretrained prior 손상을 막으며 저조도·야간 등 다중 벤치마크에서 SOTA를 달성한다. 자율주행·야간 인지에 일부 관련이 있다.</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2608.20497'>Bern2Edge: A Neurosymbolic Compiler for Edge Deployment via Bernstein Polynomial Networks</a></td><td>46</td><td>3</td><td>Efficient Inference/Edge AI</td><td>Bernstein 다항식 활성화로 teacher 네트워크를 지식 증류해 LUT 기반 고정밀 경로와 해석 가능한 rule 기반 경로를 함께 지원하는 edge 배포 프레임워크로, FPGA에서 최대 99.8%의 지연 감소를 달성한다. 저전력 온-로봇 추론에 참고할 만하다.</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2608.20932'>OccluRank: Controllable Occlusion-Aware Layout-to-Image Generation by Adding Just an Ordinal Rank</a></td><td>46</td><td>2</td><td>Generative</td><td>bounding box에 ordinal rank 하나만 추가해 occlusion 순서를 제어하는 layout-to-image 생성 기법으로 간결한 조건화가 특징이나 콘텐츠 생성 응용에 머문다.</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2608.20428'>Approximate Homomorphisms and Convergent Representations in Transducers</a></td><td>46</td><td>2</td><td>ML Theory</td><td>controlled stochastic process의 최소 표현이 perturbation 하에서 얼마나 안정적인지를 approximate homomorphism 개념으로 규명하고, 신경망 latent representation의 구조적 수렴 가설에 이론적 근거를 제공한다. predictive-state representation은 world model의 이론적 토대와 연결될 수 있다.</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2608.20621'>RECOUNT: Reference-guided Counting with Synthetic Visual Exemplars</a></td><td>46</td><td>1</td><td>CV</td><td>단일 참조 이미지를 diffusion 기반 contrastive data engine으로 확장해 zero-shot object counting의 카테고리 혼동 문제를 해결하지만 counting 태스크에 국한되어 로봇 관련성은 낮다.</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2608.20999'>Latent Ordinal Evidence, Misaligned Outputs: Inference-Time Ordinal Lens Alignment for Multimodal LLMs</a></td><td>46</td><td>1</td><td>Multimodal</td><td>MLLM의 hidden state에는 ordinal 정보가 강하게 남아있지만 digit-token 출력에서는 소실됨을 규명하고, frozen backbone에서 lightweight lens로 이를 보정하는 inference-time 정렬 기법을 제안한다. age estimation 등 특정 ordinal task에 적용되어 로봇 관련성은 낮다.</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2608.21229'>Anchoring Instruction Outside Mask: Exact Reference Caching for Efficient In-Context Diffusion Transformers</a></td><td>46</td><td>1</td><td>Generative/Efficient Inference</td><td>static text anchor로 instruction과 reference 분기를 연결해 K/V 재사용을 유지하면서도 instruction following을 보존하는 diffusion transformer 가속 기법으로, on-policy distillation으로 아키텍처 변경에 따른 품질 저하를 복구해 10-reference에서 5.47배 가속을 달성한다.</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2608.20427'>BF1: A Causal Dyadic Sparse-Attention Retrofit for Efficient Long-Context Transformers</a></td><td>46</td><td>1</td><td>Efficient Inference/LLM</td><td>local, global-first-block, 로그 간격 historical block을 결합한 결정론적 sparse attention retrofit으로 32K 토큰에서 10.91배의 prefill 가속을 달성하는 long-context transformer 효율화 기법이다.</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2608.20442'>Stored in Optimizer State, Valued by Later Training: A Causal Account of Subliminal Trait Transfer</a></td><td>46</td><td>0</td><td>ML Theory/Interpretability</td><td>optimizer state를 causal carrier로 규명해 subliminal trait transfer가 어떻게 source 제거 후에도 살아남고 부호를 바꾸는지 state surgery로 밝힌 메커니즘 해석 연구로 여러 아키텍처에 걸쳐 재현되지만 로봇 응용과는 무관하다.</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2608.20802'>SPARC: Single-Pass Scaling for Motion Forecasting with Conformal Bayesian Last Layers</a></td><td>45</td><td>4</td><td>Motion Forecasting</td><td>Bayesian last layer와 conformal calibration을 결합해 단일 forward pass로 궤적 예측의 horizon별 불확실성을 산출하는 방법으로 NLL 지표에서 9개 데이터셋 전반 1위를 기록했다.</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2608.20627'>When Failures Propagate: Causal Failure Attribution in Agentic Retrieval-Augmented Generation</a></td><td>45</td><td>3</td><td>NLP</td><td>AgenticRAG-FP는 특정 hop에 fault를 주입해 재실행하는 interventional benchmark로 agentic RAG의 causal failure attribution을 평가하며, coverage 기반 진단이 hop 1에서만(0.91) 작동하고 이후 hop에서는 실패(0.00)함을 보인다. failure diagnosis라는 우선 주제와 방법론적으로 맞닿아 있지만 도메인은 RAG에 한정된다.</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2608.20691'>Bridging Language and Spherical Space: Object-Centric Control for Text-to-Panorama Generation</a></td><td>45</td><td>2</td><td>Generative/Multimodal</td><td>텍스트의 방향 표현을 spherical bounding field-of-view로 변환해 panorama 생성을 object-level로 제어하는 프레임워크로 언어와 spherical space를 명시적으로 연결하지만 embodied spatial reasoning과의 연결은 간접적이다.</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2608.20770'>MotionPhys: Detecting AI-Generated Videos via Physical Consistency of Optical-Flow Trajectories</a></td><td>45</td><td>2</td><td>Video</td><td>sparse motion trajectory의 물리적 일관성을 이용해 AI 생성 영상을 탐지하는 경량 프레임워크로, appearance 단서 대신 물리 법칙 기반 탐지라는 관점이 흥미롭지만 로봇 응용과의 연결은 간접적이다.</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2608.21194'>ES-VP : Energy-Shaped Dynamic Visual Prompting for Efficient Model Adaptation</a></td><td>45</td><td>1</td><td>Efficient Adaptation</td><td>low-rank 초기화와 energy 기반 동적 적응으로 이미지별 visual prompt를 생성해 기존 SOTA 대비 590배 적은 파라미터로 더 높은 정확도를 달성하는 parameter-efficient adaptation 기법이다.</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2608.20946'>Fast Coordinated Bimanual Motion Planning With Hard Constraints</a></td><td>44</td><td>7</td><td>Manipulation</td><td>양팔 로봇의 상대 변환 제약을 leader-follower 파라미터화로 연속 만족시키는 fast bimanual motion planner를 제안해 기존 대비 19.4배 빠른 계획을 달성했고 Kinova Gen3 실물 실험으로 검증했다.</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2608.20784'>Rethinking Demonstration Unlearning in Imitation Learning for Robotics</a></td><td>44</td><td>6</td><td>Manipulation</td><td>모방학습 정책에서 특정 데모를 제거하는 unlearning을 behavior(재학습과의 행동 일치)와 evidence(멤버십 공격 탐지) 두 축으로 감사하는 retrain-calibrated 프레임워크를 제시했으며, ACT 팔 실험에서 redirect edit이 20건 중 18건 성공을 회복시켰다.</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2608.21032'>Roadside-Cooperative Autonomous Driving: From Data Platform to Vision-Language End-to-End Reasoning</a></td><td>44</td><td>6</td><td>Embodied AI</td><td>roadside-ego 협력 인지를 위한 V2XBench와 Chat-V2XBench 벤치마크, 그리고 CQAF 모듈로 시점 정렬을 수행하는 AURORA를 제안해 폐색이 심한 상황에서 Route Completion 98.21%를 달성했다.</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2608.20414'>StateSight: Benchmarking Latent Spatial-State Reconstruction in Vision-Language Models</a></td><td>44</td><td>5</td><td>Embodied AI</td><td>StateSight는 cube-net 반대면 추론, 가려진 큐브탑 개수 세기, 4-이웃 connected-component 개수 세기 등 절차적으로 생성된 latent spatial-state benchmark로, GPT-5.5(59.3/33.3/28.3%)와 Claude Sonnet 5(53.3/18.7/7.3%)가 인간(80.8/68.8/64.3%)에 크게 못 미침을 보인다. embodied spatial reasoning 능력의 명확한 격차를 정량화한 유용한 벤치마크다.</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2608.20874'>Multi-Modal Traffic Sign Detection with Semantic Attributes for Autonomous Driving</a></td><td>44</td><td>4</td><td>Autonomous Driving/Perception</td><td>카메라와 LiDAR를 융합한 intensity-aware deformable fusion으로 60개 이상 국가의 대규모 데이터에서 교통 표지 탐지의 지역 일반화를 개선한 상용급 시스템 논문이나, 방법론적으로는 엔지니어링 성격이 강하다.</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2608.20944'>SuppreSensing: Expert-Guided Feature Recalibration and Discrepancy Augmentation for Multimodal Object Detection</a></td><td>44</td><td>3</td><td>CV/Detection</td><td>expert 기반 feature 재보정과 modality별 차이 증강으로 원격 탐사 멀티모달 객체 탐지의 강건성을 높이며 드론 관측 상황에 일부 관련이 있으나 도메인 특화 엔지니어링에 가깝다.</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2608.20400'>When Retrieval Fails Before It Begins: Structurally Indirect Prerequisite Eviction as a Retention Failure in Agentic Memory</a></td><td>44</td><td>3</td><td>LG</td><td>제한된 예산 하 agentic memory에서 retrieval 이전에 발생하는 구조적으로 간접적인 prerequisite eviction이라는 새로운 실패 모드를 정의하고, 이를 완화하는 one-hop graph rule DSGC로 full-chain retention을 0.03에서 0.90(어휘 encoder), 1.00(문장 encoder)까지 끌어올린다. memory retention을 retrieval과 분리된 실패 축으로 새롭게 정식화한 점이 robot memory 설계에도 시사점을 준다.</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2608.21308'>Rethinking Expressivity and Efficiency in Test-Time Training</a></td><td>44</td><td>2</td><td>LG</td><td>test-time training의 chunk-wise 근사에서 손실되는 시간적 구조를 정확히 복원하는 closed-form state transition을 유도한 E2-TTT는, needle-in-haystack에서 8배 컨텍스트까지 90% 이상 정확도를 유지해 표현력과 효율성을 동시에 달성했다.</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2608.20754'>SPARK-SAM: Self-Prompt Adaptation with Response Knowledge for SAM in Infrared Small Target Segmentation</a></td><td>44</td><td>1</td><td>CV/Segmentation</td><td>적외선 소형 표적 분할에서 SAM의 spatial prompt와 target mask response 사이 불일치를 self-prompt adaptation으로 해결해 IoU를 크게 개선하지만(예: NUAA-SIRST 4.69%에서 75.78%) 특정 도메인 벤치마크에 특화된 적응 기법이다.</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2608.20929'>GAP-SAM: A Global Artifact Prior for Generalizable AI-Generated Image Manipulation Localization</a></td><td>44</td><td>0</td><td>CV</td><td>global artifact token을 SAM3에 주입해 AI 생성 이미지의 조작 영역을 semantic-boundary shortcut 없이 localize하는 방법으로 여러 데이터셋에서 큰 성능 향상을 보이나 포렌식에 국한된다.</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2608.21096'>FlatLand: Personalized Graph Federated Learning via Tailored Lorentz Space</a></td><td>44</td><td>0</td><td>LG</td><td>hyperbolic Lorentz space에서 client별 파라미터를 시간형/공간형으로 분리하는 FlatLand를 제안했고 ICML 2026 Oral로 선정되었으며, personalized federated graph learning에 새로운 기하학적 표현을 도입했다.</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2608.20962'>Hybrid Roller-Jamming Gripper for Object Acquisition and Retention Under Pose Uncertainty</a></td><td>42</td><td>7</td><td>Manipulation</td><td>roller의 능동 흡인과 granular jamming의 파지 안정성을 결합한 hybrid gripper를 제안해 840회 파지 시험에서 812회 성공(96.7%)을 달성했으며, 자세 불확실성 하에서의 기구 설계 기여가 명확하다.</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2608.21175'>SRL-MPC: Shape-Aware Reinforcement Learned Model Predictive Control</a></td><td>42</td><td>7</td><td>Navigation</td><td>이형 형상의 crowd/fleet 내비게이션에서 HOCBF 기반 안전 제약을 유지하면서 MPC 파라미터를 RL로 실시간 갱신하는 SRL-MPC를 제안해 안전성과 적응성에서 baseline을 크게 능가했다.</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2608.20967'>Generalizing Soft Tissue Deformation and Force Prediction Across Material Stiffness and Geometry</a></td><td>42</td><td>4</td><td>Simulation/Manipulation</td><td>softness-conditioned equivariant GNN으로 조직 강성과 형상이 달라져도 변형과 force를 실시간에 가깝게 예측하며, calibration 일관성이 force 예측 품질을 좌우함을 보여 surgical/haptic manipulation에 시사점을 준다.</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2608.21332'>Anatomy-Informed Neural Networks: Encoding Anatomic Priors in Loss and Architecture, with an SE(3) Formulation of Guidewire-Induced Aortoiliac Deformation</a></td><td>42</td><td>4</td><td>3D/Medical Robotics</td><td>해부학적 prior를 loss와 architecture에 hard/soft로 내장하고 SE(3) 상의 Cosserat rod와 혈관 접촉을 모델링해 자율 혈관내 항법에 필요한 변형 예측 틀을 제시했으나 아직 신경망 학습 없이 mechanics solver 검증에 머문다.</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2608.20690'>Identity-Aware Human-Object Interaction Motion Captioning</a></td><td>42</td><td>3</td><td>Multimodal/HOI</td><td>human-object interaction 캡션에 주체 identity를 명시하는 새 태스크를 정의하고 multi-view 학습과 two-stage rewriting으로 single-view identity-aware caption을 생성하지만 로봇 정책 학습과의 직접 연결은 약하다.</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2608.20916'>Semantically Compatible Knowledge Distillation for Cross-Domain Object Detection with Vision Foundation Models</a></td><td>42</td><td>2</td><td>CV/Detection</td><td>DINOv2 teacher와 student 사이의 spatial-scale 불일치를 해소하는 adapter로 cross-domain object detection의 pseudo-label 품질을 개선하는 knowledge distillation 기법이다.</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2608.20439'>Wrong-Physics Backdoors in Neural PDE Operators</a></td><td>42</td><td>2</td><td>ML Security/Scientific ML</td><td>cross-parameter relinking이라는 새로운 data-poisoning 기법으로 neural PDE operator가 그럴듯하지만 잘못된 물리 파라미터의 해를 내놓게 만드는 wrong-physics backdoor를 규명한다. FNO에서 공격 성공률 1.0을 보여, 물리 시뮬레이터를 활용하는 world model 학습 파이프라인의 검증 공백을 시사한다.</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2608.20634'>AgentMercury: Your Agent Can Synthesize Verifiable Environments for Business Scenarios at scale</a></td><td>42</td><td>1</td><td>RL</td><td>AgentMercury는 특정 task가 아닌 지속적인 world(entity·service·tool·state)를 먼저 생성해 다양한 task와 trajectory가 자연스럽게 발생하도록 하는 environment synthesis 프레임워크로, Qwen3.5-4B가 EnterpriseOps-GYM에서 12.3에서 15.7로 향상됐다. task-agnostic world 생성이라는 아이디어는 robot 시뮬레이션 환경 생성에도 참고할 만하다.</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2608.20564'>Consilience: Conformally Calibrated Communication Control for Hidden-Profile Multi-Agent Reasoning</a></td><td>42</td><td>1</td><td>Multi-Agent LLM</td><td>hidden-profile multi-agent 소통을 conformal calibration으로 통제하는 새로운 orchestration 방법을 제안하며 이론적 guarantee를 갖췄지만, robotics와는 거리가 있다.</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2608.20663'>Shortcut Learning in a Public Grape Disease Dataset: Annotation Granularity as a Modulator, Not a Cause</a></td><td>42</td><td>0</td><td>CV</td><td>포도 질병 데이터셋에서 annotation granularity가 shortcut을 유발하는 원인이 아니라 조절자임을 counterfactual retraining으로 입증한 인과 분석이 흥미로우나 도메인이 농업에 국한된다.</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2608.20884'>Breaking High Confidence: Practical Face Impersonation under High-Security Thresholds</a></td><td>42</td><td>0</td><td>CV/Security</td><td>고보안 임계값 설정에서 score 기반 얼굴 impersonation 공격을 최초로 성공시킨 연구로 Amazon Rekognition에서 92% 이상의 성공률을 보이나 로봇과는 무관한 보안 주제이다.</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2608.20374'>VA-DPO: Valence-Arousal Direct Preference Optimization for Controllable Emotion Generation in Language Models</a></td><td>42</td><td>0</td><td>NLP</td><td>VA-DPO는 감정을 이산 label이 아닌 연속적인 Valence-Arousal 좌표로 지정하고 DPO의 preference pair 구성 방식을 바꿔 목표 거리 33% 감소, r_v=0.93을 달성한다. preference data 구성이라는 새로운 아이디어지만 robotics와는 무관하다.</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2608.20823'>Natural Sit-to-Stand Motion Synthesis For Humanoids via Guided Assistance Curricula and Staged Rewards</a></td><td>40</td><td>7</td><td>Embodied AI</td><td>sit-to-stand 동작을 시연 없이 RL만으로 합성하는 연구로, 힘/의자 높이 결합 커리큘럼과 생체역학 기반 보상을 설계해 8개 의자 높이에서 97% 이상의 균형 성공률을 달성했다.</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2608.20477'>STCO: Conditional Neural Operators for Time-Dependent PDEs</a></td><td>40</td><td>3</td><td>LG</td><td>STCO는 시간에 따른 PDE의 조건부 neural operator 학습에서 vorticity 기반 FAGL과 이중 지점 FiLM으로 motion/inflow/force 조건을 주입하는 공통 인터페이스를 제안해, 12개 backbone에서 relative-L2 오차를 평균 31.1% 줄인다. 물리 시스템의 조건부 예측이라는 점에서 로봇 동역학 모델링에도 참고할 수 있는 일반화 가능한 방법론이다.</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2608.20799'>Dynamic Context Scheduling: Learning Beyond the Static Universe</a></td><td>40</td><td>3</td><td>RL</td><td>episode 내에서 context를 동적으로 변화시키는 curriculum을 도입해 contextual RL의 OOD 일반화를 높였으며 BipedalWalker 등 continuous control 환경에서 검증했다.</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2608.21022'>Recognition-Conditioned Reasoning: A Training-Free Multimodal-LLM Pipeline for Fine-Grained Micro-Action Understanding</a></td><td>40</td><td>2</td><td>Multimodal</td><td>frozen MLLM들을 태스크별로 라우팅하는 training-free 파이프라인으로 미세 동작(micro-action) 이해 챌린지에서 1위를 달성했으나 특정 챌린지 벤치마크에 특화된 프롬프트 엔지니어링 성격이 강하다.</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2608.21079'>Causal Modeling of Adverse Pregnancy Outcomes via Adaptive LLM Proposals</a></td><td>40</td><td>2</td><td>LG</td><td>LLM을 adaptive proposal distribution으로 활용해 causal graph 가설을 생성하고 데이터로 검증하는 neurosymbolic 프레임워크로, 임신 합병증 도메인에서 전문가 그래프의 모든 edge를 복원했으며 causal reasoning 방법론으로서 참고 가치가 있다.</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2608.20631'>Weighted Memory Tree: Remembering What Matters for Long-Horizon LLM Agents</a></td><td>40</td><td>2</td><td>Agent Memory</td><td>LLM agent의 실행 이력을 계층적으로 조직하고 retention score로 관리하는 memory 구조를 제안하며 robot memory 설계에 참고할 만한 아이디어를 제공한다.</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2608.20515'>DiffVC-ONE: Diffusion-based Generative Video Compression with One-Step Video Diffusion Transformer</a></td><td>40</td><td>1</td><td>Video</td><td>one-step video diffusion transformer 기반 생성형 영상 압축으로 품질과 속도를 동시에 개선하나 압축 응용에 국한되어 로봇 관련성은 낮다.</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2608.20756'>Vis-Poison: Poisoning Visual Knowledge in Multimodal Retrieval-Augmented Generation</a></td><td>40</td><td>1</td><td>Multimodal Security</td><td>텍스트 메타데이터가 아닌 이미지 자체를 payload로 삼는 multimodal RAG poisoning 공격을 제안하며 black-box 환경에서 40~65%의 공격 성공률을 보이지만 로봇 응용과는 무관한 보안 연구이다.</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2608.21305'>Re$^3$Cap: Retrieval-Guided Refinement for Image Captioning Enhancement via Reinforcement Learning</a></td><td>40</td><td>1</td><td>Multimodal/NLP</td><td>retrieval을 reasoning 신호로 활용해 image captioning의 hallucination과 누락을 교정하는 RL 기반 refinement 전략으로 SFT를 능가하는 성능을 보이나 captioning 태스크에 국한된다.</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2608.20375'>GRAFT: Adaptive DLM-Based Draft Tree Construction with Target-Distilled Edge Scoring</a></td><td>40</td><td>1</td><td>LG</td><td>GRAFT는 diffusion language model drafter를 위한 draft tree 구성에서 target-distilled edge scoring과 state-aware budget allocation을 도입해 기존 DDTree 대비 개선된 speculative decoding을 보인다. efficient inference 관련 일반 원리를 일부 제공하나 핵심은 LLM decoding 엔지니어링이다.</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2608.20445'>Amortized Bandwidth Learning for Kernel Density Estimation under Logarithmic Score</a></td><td>40</td><td>0</td><td>ML/Statistics</td><td>logarithmic score를 최적화해 bandwidth 선택을 여러 밀도 추정 태스크에 걸쳐 amortize하는 프레임워크로 Silverman&#x27;s rule 등 고전 기법을 능가하지만 통계적 방법론에 국한된다.</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2608.20873'>Nothing Changed but the Model: CellFill -- Bounded In-Cell Learning for Bit-Identical, Revocable Updates to Quantized LLMs</a></td><td>40</td><td>0</td><td>LG</td><td>quantization decision cell 내부에서만 학습해 bit-identical하고 revocable한 업데이트를 보장하는 CellFill을 제안한 점이 참신하며, 27B 모델까지 검증했다.</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2608.21236'>RARE: Decoupling Representation Steering from Expert Routing in Mixture-of-Experts Language Models</a></td><td>40</td><td>0</td><td>LG</td><td>RARE는 MoE 모델에서 representation steering이 router와 충돌하는 문제를 진단하고, steering 신호를 router matrix의 null space로 투영해 routing drift를 보정한다. harmfulness steering에서 attack success rate 53.3%와 MMLU 67.8% 유지를 동시에 달성하는 균형 잡힌 결과지만 workshop 논문 수준의 범위다.</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2608.21315'>Prompt-Model Interaction Reaches the Fixed Points: A deterministic, task-free structural readout -- and the factorizations of it that failed</a></td><td>40</td><td>0</td><td>NLP</td><td>task-free한 short-window argmax fixed-point 구조로 prompt-model 상호작용을 측정하고, 제안한 여러 설명(phenomenological factor, attention-sink)이 모두 기각되는 과정을 정직하게 보고하는 메커니즘 탐구 논문이다. 독특한 방법론과 엄밀한 negative 결과 보고가 인상적이나 실용적 함의는 제한적이다.</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2608.20891'>IMU-Free Body-Frame State Estimation with Sparse Scene Flow for Quadcopters</a></td><td>38</td><td>6</td><td>World Model</td><td>IMU 없이 stereo 카메라만으로 body-frame 상태(pose, velocity, disturbance)를 추정하는 EKF 시스템으로, world model의 측정원으로 쓰일 수 있도록 설계된 점이 흥미롭다.</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2608.20948'>Neural-Primitive: An Efficient End-to-end Local Planner with Primitive-based Imitation Learning for Autonomous Flight</a></td><td>38</td><td>6</td><td>Navigation</td><td>다항식 계수를 직접 출력하는 primitive 기반 모방학습 로컬 플래너로, 온보드 평균 3.68ms의 초저지연 계획과 zero-shot sim-to-real 비행을 보였다.</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2608.21083'>Teaching is a Process: The TOSS Framework for Modeling Human Teaching Decisions in Human-Interactive Robot Learning</a></td><td>38</td><td>6</td><td>Embodied AI</td><td>N=34 사용자 연구로 인간의 로봇 교육 의사결정을 Trigger-Objective-Signal-Strategy로 구조화한 TOSS 프레임워크를 제시해, 인간-로봇 상호작용 학습을 위한 이론적 기반과 오라클 시뮬레이션 자원을 제공한다.</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2608.21117'>Root cause analysis via difference graph discovery from linear time-series data</a></td><td>38</td><td>3</td><td>Causal Reasoning</td><td>정상·이상 regime 간 causal coefficient 변화를 difference graph로 찾아내는 방법으로 IT/ICU 모니터링에 적용했으며, failure diagnosis에 causal reasoning을 접목한 접근이 로봇 실패 진단에도 응용 가능하다.</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2608.20920'>ForeDreamer: A Self-Evolving Dual-Agent Memory Architecture for Future Event Prediction</a></td><td>38</td><td>2</td><td>LG</td><td>ForeDreamer는 질문별 factual memory와 episode 간 축적되는 experiential memory를 분리하는 dual-agent memory 구조로 open-web future event prediction 성능을 높인다. memory 구조 분리 아이디어는 robot memory 설계에도 참고할 만하지만 적용 도메인은 웹 예측이다.</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2608.21044'>Socialized Division and Collaboration: Rethinking Class-Incremental Learning under Optimization Conflicts</a></td><td>38</td><td>2</td><td>Continual Learning</td><td>single model 패러다임 대신 session을 여러 전문 모델로 분할·협업시키는 energy 기반 continual learning 재정식화로, robot lifelong learning에도 참고할 수 있는 구조적 아이디어를 제시한다.</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2608.20557'>Learning Prostate Anatomy at Test Time for Cancer Detection in Micro-Ultrasound</a></td><td>38</td><td>1</td><td>CV/Medical</td><td>micro-ultrasound 전립선암 검출에서 segmentation 보조 과제를 이용한 test-time adaptation으로 도메인 shift 상황의 AUC를 개선하나 의료 영상 도메인에 국한된 기여이다.</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2608.21140'>A Modular Agent for Reliable and Auditable Spatial Relation Verification in CT Scans</a></td><td>38</td><td>1</td><td>Medical/Spatial Reasoning</td><td>CT 영상의 공간 관계 질의를 언어 파싱, 해부학적 localization, 결정론적 기하 검증 단계로 분해하는 modular agent로 end-to-end VLM 대비 42.5%p 정확도 향상을 보이나 의료 영상 spatial QA에 국한된다.</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2608.20572'>Faults That Fortify: CNN Adversarial Robustness via GPU Undervolting</a></td><td>38</td><td>1</td><td>ML Security/Hardware</td><td>GPU undervolting이 유발하는 bit-level fault가 implicit regularization으로 작용해 CNN의 adversarial robustness를 높이면서 에너지도 절감함을 보이는 하드웨어-소프트웨어 공동설계 연구이다.</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2608.20530'>LiLiCorr: Lightweight Likelihood Correlation of Parallel Drafts for Speculative Decoding</a></td><td>38</td><td>1</td><td>LG</td><td>LiLiCorr은 DFlash 같은 block-wise diffusion drafter의 marginal 분포를 in/out vector로 상관시켜 speculative decoding acceptance length를 9-19% 높이고 72개 설정 중 70개에서 최고 throughput을 달성한다. 강한 실증 결과를 보이지만 LLM decoding에 특화된 efficient inference 기여다.</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2608.21265'>Memory Augmentation Unlocks Efficient Chain-of-Thought Reasoning</a></td><td>38</td><td>1</td><td>NLP</td><td>Context-Generation Substitution Law라는 개념 하에, 압축된 CoT의 손실 정보를 재사용 가능한 reasoning memory로 보완하는 training-free Memory-Augmented Compression을 제안해 GSM8K 등에서 CoD 대비 최대 29.5점 개선과 1.14-1.49배 속도향상을 동시에 달성한다. test-time reasoning 효율화라는 점에서 참고 가치가 있다.</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2608.20617'>Dual-Cache Latent Space Communication between Heterogeneous Language Models</a></td><td>38</td><td>1</td><td>Efficient Inference</td><td>이질적 LLM 간 KV cache를 학습된 translator로 압축·전달하는 새로운 latent 통신 방식을 제안하지만 robotics 적용은 다루지 않는다.</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2608.20686'>CDRL: Certification-Driven Reinforcement Learning for Neutrino Flavor Model Discovery</a></td><td>38</td><td>1</td><td>RL</td><td>symbolic certificate를 재사용 가능한 제약으로 변환해 RL 탐색을 유도하는 방법으로 물리학 모델 발견에서 큰 성능 향상을 보였다.</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2608.21059'>The Cost of a Physics Prior Is Bounded by the Ablation Gap</a></td><td>38</td><td>1</td><td>ML Theory</td><td>physics-informed 제약의 비용이 prior 자체가 아니라 ablation gap과 validation split에 의해 결정됨을 증명한 이론적 결과로 일반화 가능한 진단 도구를 제공하지만 응용 도메인은 wildfire severity에 국한된다.</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2608.20913'>Explainable Deepfake Detection with Feature-robust Augmentation and Evidence-grounded Explanation Optimization</a></td><td>38</td><td>0</td><td>CV/Security</td><td>저화질 강건성과 근거 기반 설명을 함께 개선한 explainable deepfake detection으로 ACM MM 챌린지 1위를 달성했으나 로봇과 무관한 포렌식 주제이다.</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2608.20818'>Scaling Muon for Diffusion Transformers</a></td><td>38</td><td>0</td><td>LG</td><td>Diffusion Transformer에서 Muon optimizer의 scaling 거동을 1.3B~15B까지 분석하고 Periodic Row-wise Muon으로 optimizer 시간을 46.9~54.3% 줄인 실용적 기여가 크다.</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2608.20607'>JuryProbe: An Empirical Consensus-Risk Diagnostic for Routing Reference-Free Factuality Judge Panels to Grounded Verification</a></td><td>38</td><td>0</td><td>NLP</td><td>JuryProbe는 reference-free judge panel의 false-negative correlation과 false-consensus lift를 진단해 grounded verification으로 라우팅하는 새로운 empirical diagnostic으로, FEVER corruption에서 correlation 0.402, lift 최대 18.13배를 보고한다. 저자 스스로 formal guarantee가 없음을 명시한다.</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2608.20804'>Denoising the Future: Context-Aware Spectral Diffusion for Temporal Knowledge Graph Extrapolation</a></td><td>38</td><td>0</td><td>LG</td><td>FreqDiff는 temporal knowledge graph extrapolation을 query-slot denoising으로 정식화하고 frequency-domain regularizer로 target-discriminative 신호를 강화하는 diffusion 기반 방법으로 4개 벤치마크에서 SOTA를 달성한다. spectral diffusion이라는 새로운 관점을 제공하지만 KG 예측이라는 특정 태스크에 한정된다.</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2608.20569'>Open-Weight Masked Introspection: Measuring What Language Models Can Report About Their Own Computation</a></td><td>38</td><td>0</td><td>Interpretability</td><td>language model의 introspection 능력을 대규모로 측정한 실험적 연구로 흥미롭지만 robot learning과 직접적 연관은 없다.</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2608.21070'>TracingFlow: A Simulation-Free Trajectory Inference Framework Based on Second-Order Dynamics</a></td><td>37</td><td>2</td><td>LG</td><td>OT 기반 trajectory inference를 2차 동역학(acceleration field)으로 일반화한 TracingFlow를 제안해 세포 분화 등에서 기존 1차 방법 대비 더 나은 궤적 복원을 보였으며, world model적 동역학 모델링 관점에서 참고할 만하다.</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2608.20680'>Reinforcement Learning for Continuous-Time Jump Markov Decision Processes with Applications to Network Dynamic Pricing</a></td><td>37</td><td>1</td><td>RL</td><td>연속시간 jump MDP에 대해 q-learning 이론을 확장하고 네트워크 동적 가격결정에 적용한 점이 이론적으로 견고하며, 이산 상태공간 RL 이론 일반화라는 점에서 가치가 있다.</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2608.21276'>The Coastline as a Structural Constraint: Harnessing Scene Geometry for Autonomous Surface Vessel Localization</a></td><td>36</td><td>5</td><td>Navigation</td><td>해안선과 수면 기하 구조를 활용해 GPS 없이 해상 표면 선박을 위치추정하는 두 가지 프레임워크(LiDAR/모노큘러)를 제안했으며, 실해역 데이터셋에서 궤적 정확도 개선과 유계 드리프트를 보였다.</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2608.20749'>Identity-Preserving Text-to-Video Generation via Agentic Enhancement and Semantic Repair</a></td><td>36</td><td>1</td><td>Video Generation</td><td>closed-source 영상 생성 모델의 identity drift 문제를 agentic prompt enhancement와 VLM 기반 semantic repair로 완화하는 파이프라인으로 challenge 1위를 달성했으나 시스템 엔지니어링 성격이 강하다.</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2608.21307'>SPARCL: Spectral Partitioned Analytic Continual Learning</a></td><td>36</td><td>1</td><td>LG</td><td>analytic continual learning의 망각 원인을 spectral interference로 규명하고 이를 분리하는 SPARCL을 제안한 점이 참신하며, closed-form 업데이트로 CIFAR-100 등에서 forgetting을 크게 줄였다.</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2608.20359'>Self-Speculation for Faster Reasoning Models</a></td><td>36</td><td>1</td><td>NLP</td><td>reasoning 모델의 부분 CoT를 draft로, 전체 CoT를 verifier로 사용하는 training-free self-speculative decoding SSR을 제안해, 구조화된 생성 과제에서 지연시간을 최대 24.1% 줄였다.</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2608.20670'>Why2Speak: Faithful Reasoning for Abstaining Action Policies</a></td><td>36</td><td>1</td><td>Agent Reasoning</td><td>발화 여부를 결정하는 abstaining policy의 reasoning faithfulness를 분석하며 capability-auditability trade-off를 실증적으로 보여준다.</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2608.20825'>Prediction certification cannot replace explanation certification: a competence envelope for trustworthy AI under compound stress</a></td><td>36</td><td>1</td><td>Trustworthy AI</td><td>prediction-side 인증만으로는 잡아낼 수 없는 실패를 explanation 인증과 결합해 밝혀내는 separation theorem을 제시하며 일반화 가능한 이론적 도구를 제공한다.</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2608.21300'>When Adaptation Hurts: Connecting Representational Drift to OOD Failures in MedSAM Fine-Tuning</a></td><td>36</td><td>0</td><td>CV/Medical</td><td>MedSAM의 여러 adaptation 전략이 far-OOD에서 오히려 성능을 해치는 현상을 decoder representation drift로 설명하는 분석이나 의료 영상 세그멘테이션에 국한된다.</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2608.20980'>A Critical Audit of Spatiotemporal Forecasting Benchmark Datasets and Baselines</a></td><td>36</td><td>0</td><td>LG</td><td>GNN 기반 시공간 예측의 표준 벤치마크(Chickenpox, METR-LA 등)를 통계적으로 재분석해 선형모델도 경쟁력이 있음을 보인 비판적 감사 연구로, 커뮤니티에 유용한 방법론적 경고를 준다.</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2608.21024'>RODE: A Radial-Orthogonal Decoupled Engine for Optimization</a></td><td>36</td><td>0</td><td>LG</td><td>matrix optimizer에서 radial과 directional 업데이트를 분리한 RODE를 제안하고 1.5B 모델에서 Muon RMS 대비 loss를 4.145에서 3.346으로 낮췄으며, Qwen3.5-9B에서도 일관된 개선을 보였다.</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2608.20392'>Evaluation-as-Search: Adaptive Discovery of Grounding Failures in Meeting Assistants</a></td><td>36</td><td>0</td><td>NLP</td><td>Evaluation-as-Search는 UCB 기반 coverage map으로 meeting assistant의 grounding failure를 탐색하는 adaptive evaluation 방법으로, random probing 대비 2.5배 많은 failure(7.1% 대 2.9%)를 찾아낸다. 평가 방법론으로서는 새로운 problem formulation을 제시한다.</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2608.20711'>AsmEvo: Agentic Assembly-Level Optimization of AMD GPU Kernels with Functional Equivalence Verification</a></td><td>36</td><td>0</td><td>LG</td><td>AsmEvo는 컴파일된 AMD GPU 코드 오브젝트를 직접 편집하는 agentic assembly-level 최적화기로 MI308X에서 1.35배 기하평균 속도향상을 검증된 functional equivalence 하에 달성한다. 실질적인 시스템 기여지만 GPU kernel 최적화라는 특정 도메인이다.</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2608.20927'>MentorPulse: Refreshing Cross-Model Latent Guidance for Long-Form Generation</a></td><td>36</td><td>0</td><td>NLP</td><td>MentorPulse는 고정된 cross-model latent guidance가 long-form 생성에서 성능을 저하시킴을 보이고 capped slot memory와 gated cross-attention으로 주기적으로 guidance를 갱신해 mentor-student gap의 52.2%를 좁힌다. 13개 데이터셋과 11개 mentor-student 쌍에서 일관된 개선을 보이는 탄탄한 실증이다.</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2608.20397'>Nexus: Depth-Adaptive KV-Cache Splicing and Retrieval-Decoupled Tool Routing for Agentic LLMs on Unified Memory</a></td><td>36</td><td>0</td><td>LG</td><td>Nexus는 tool schema 검색을 KV-cache splicing에서 분리해 INT8 semantic lookaside buffer로 라우팅하면서 RoPE phase drift로 인한 실패 경계를 명시하고 depth-adaptive 재복호화로 보정한다. 도구 레지스트리가 250개로 커져도 routing 정확도 89%를 유지하며 negative result도 함께 제시하는 견실한 시스템 연구다.</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2608.20869'>ReCurveflow: A Flow Matching Framework that Learns Curved Reaction Trajectories to Predict Transition State Geometries</a></td><td>35</td><td>2</td><td>Generative Model</td><td>직선 경로 대신 NEB 기반 곡선 경로를 supervise하는 flow matching과 off-path correction을 도입한 방법으로, action expert의 flow matching 기반 정책 학습에 아이디어를 줄 수 있다.</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2608.20961'>TreeWY: Speculative Verification for Gated DeltaNet Hybrids</a></td><td>35</td><td>1</td><td>Efficient Inference</td><td>Gated DeltaNet hybrid 모델의 speculative decoding에서 tree 구조 WY transform으로 recurrent state snapshot을 제거해 메모리와 TTFT를 크게 개선한 시스템 연구다.</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2608.20558'>Zero-Shot Color Image Manipulation Localization via Noise Residual Artifact Pattern Analysis</a></td><td>35</td><td>0</td><td>CV</td><td>단일 이미지의 noise residual만으로 zero-shot image manipulation 위치를 찾는 training-free 포렌식 파이프라인으로 로봇과는 무관하다.</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2608.20868'>Identify, Locate, Link: End-to-End Key-Value Extraction from Document Images</a></td><td>35</td><td>0</td><td>NLP/CV</td><td>256M 파라미터 VLM으로 OCR 없이 문서에서 key-value를 end-to-end로 추출하는 경량 모델로 문서 처리에 특화되어 로봇과 무관하다.</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2608.21041'>CoST: Semantic-Aware Urban Understanding via Spatial-Temporal Alignment</a></td><td>35</td><td>0</td><td>CV/Remote Sensing</td><td>위성 영상의 spatial-temporal 정렬로 지역 간 일반화 가능한 도시 표현을 학습하는 contrastive 프레임워크로 원격 탐사 응용에 국한되어 로봇과 무관하다.</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2608.20371'>When Do LLMs Replace Fine-Tuned NLU? A Decision Framework for Intent Detection in Production Conversational Systems</a></td><td>35</td><td>0</td><td>NLP</td><td>ATIS·CLINC150에서 fine-tuned RoBERTa와 zero-shot LLM을 비교해 label이 풍부하면 RoBERTa가 우세(95.9 대 84.1)하고 넓은 intent space에서는 LLM이 동등함을 보이는 실증적 decision framework다. novelty보다는 실무적 비교 연구에 가깝다.</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2608.21186'>A Neurosymbolic Approach for Constructing Planning Domain Models from Clinical Narratives</a></td><td>34</td><td>2</td><td>LG</td><td>임상 서술문에서 확률적 planning domain(PPDDL)을 유도하는 neurosymbolic 프레임워크 NSPIN을 제안해 외과 실무와 일치하는 모델을 얻었으며, task/domain induction 방법론은 로봇 task planning에도 참고할 여지가 있다.</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2608.20797'>Automated Trajectory Evaluation for Mobile Agents via Step-Level Consequence Reasoning and Aggregation</a></td><td>34</td><td>2</td><td>Agent Evaluation</td><td>step-level consequence reasoning으로 mobile agent trajectory를 평가하는 VLM-as-judge 프레임워크로 안전성 평가까지 확장했으며 embodied trajectory evaluation에 참고할 만하다.</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2608.20969'>Kinematic Knowledge Maps for Pattern Alignment: Structured Latent Representational Learning in Multimodal Gait Analysis</a></td><td>34</td><td>1</td><td>CV/Medical</td><td>monocular gait video로부터 척추측만증을 선별하는 구조화된 kinematic knowledge map 기반 멀티모달 융합 프레임워크로 해석 가능한 gait 표현을 제시하지만 임상 스크리닝에 특화되어 있다.</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2608.20953'>Quantization-Aware Healing: A Practical Recipe for Recovering Compressed, 4-Bit LLMs</a></td><td>34</td><td>1</td><td>LG</td><td>Quantization-Aware Healing은 구조 압축·4bit 양자화된 모델을 원본 비압축 모델에서 직접 distill해 QAT 대비 7배 빠르게 동등한 peak 성능에 도달하는 실용적 recipe로, GPT-OSS 120B-&gt;60B 파이프라인에서 9개 벤치마크 중 7개에서 bfloat16 소스를 능가한다. on-device efficient inference에 참고할 만하다.</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2608.21019'>Target-Aware Calibration Data Selection for Preserving Uncertainty in Quantized Language Models</a></td><td>34</td><td>1</td><td>LG</td><td>DPQ는 양자화 calibration data 선택을 target-dependent uncertainty 보존 문제로 정식화하고 최적 calibration recipe가 배포 목적에 따라 달라짐을 8개 모델·9개 벤치마크로 보인다. 새로운 문제 정식화를 제공하지만 quantization이라는 특정 영역에 한정된다.</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2608.20809'>TRACE: Training-time Report-guided and Clinically Ordered Concept Editing</a></td><td>34</td><td>0</td><td>CV/Medical</td><td>구조화된 방사선 보고서를 privileged 정보로 활용해 유방 초음파 진단의 concept 기반 해석성을 높이는 프레임워크로 의료 영상 도메인에 국한된다.</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2608.20870'>RDANet: Relative Degradation Aware Network for Infrared Small Target Detection</a></td><td>34</td><td>0</td><td>CV</td><td>적외선 소형 표적 탐지에서 anti-alias downsampling과 prototype 기반 skip memory로 scale·배경 변화에 대한 강건성을 개선하는 원격 탐사 특화 방법이다.</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2608.20758'>Hidden Axis of Uncertainty: Latent-Posterior Alignment in Graph Neural Networks with Bayesian Output Layers</a></td><td>34</td><td>0</td><td>LG</td><td>Bayesian GNN에서 posterior variance가 줄지 않아도 불확실성이 감소하는 Latent-Posterior Alignment 현상을 발견하고 이를 학습에 활용한 AGL을 제안한 점이 흥미롭다.</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2608.21147'>Capturing Cardiac Cyclicity through Phase-Equivariant Self-Supervised Learning</a></td><td>34</td><td>0</td><td>LG</td><td>심장 주기의 위상 대칭성을 활용한 phase-equivariant self-supervised objective로 Winder를 제안하고 PTB-XL에서 약 1M 파라미터로 SOTA급 정확도를 냈으나, 심전도라는 특정 생리 신호 도메인에 국한된다.</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2608.20361'>Toward Auto-Research: Mining Falsifiable Research Ideas from Paper Knowledge Graphs with Categorical Structure</a></td><td>34</td><td>0</td><td>NLP</td><td>논문을 category(대상=research entity, morphism=관계)로 모델링하고 functor 보존 여부로 cross-domain 아이디어를 필터링하는 categorical 프레임워크를 제안해 17:1 비율로 후보를 걸러내면서도 반증가능률 83% 이상을 유지했다.</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2608.20405'>ARGUS: Theory-of-Mind Guided Argument Generation with Strategy-Aware Planning and Knowledge Grounding</a></td><td>34</td><td>0</td><td>NLP</td><td>ARGUS는 Theory-of-Mind reasoner로 청중 신념을 모델링하고 logos/pathos/ethos/kairos 전략을 배정하는 설득 논증 생성 agent로, Elo와 LLM-judge 평가에서 baseline을 능가하지만 구성 요소 자체는 기존 기법의 조합에 가깝다.</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2608.20839'>SAC-Copula: Quality-Preserving Watermarking for Diffusion Language Models via Smooth Correlated Gumbel Fields</a></td><td>34</td><td>0</td><td>NLP</td><td>SAC-Copula는 Gaussian copula로 상관된 Gumbel perturbation field를 만들어 diffusion language model의 iterative unmasking과 정합되는 watermarking을 제안하며 PPL tail 안정성을 개선한다. DLM에 특화된 워터마킹 메커니즘의 기술적 기여다.</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2608.21242'>Affective Context Amplifies Sycophancy in LLM Responses</a></td><td>34</td><td>0</td><td>NLP</td><td>동일 콘텐츠를 3자 서술 대 사용자 본인 발화로 제시해 LLM sycophancy를 측정한 연구로, 외로움·고통 같은 부정적 정서 맥락이 sycophancy를 특히 증폭시킴을 7개 모델·2개 Reddit 데이터셋에서 일관되게 보인다. 방법은 단순하지만 실증적 발견의 함의가 크다.</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2608.21325'>Move by Move: Measuring and Steering How LLMs Conduct Psychotherapy</a></td><td>34</td><td>0</td><td>NLP</td><td>MULTI-60 기반 10가지 therapeutic move ontology로 인간 치료사와 LLM의 심리치료 대화 패턴을 비교해 LLM이 inquiry를 인간 대비 최대 3배 과용함을 밝히고, 이를 tool로 노출하면 human distribution과의 편차가 절반으로 줄어든다. 새로운 분류 체계와 개입 방법을 함께 제시한다.</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2608.20548'>Keep Your Friends Close, and the Right Neighbours Closer: Disaster-Conditioned Kernel-Regularized Graph Attention for Building Damage Classification</a></td><td>33</td><td>0</td><td>CV</td><td>재난 유형별 spatial kernel을 학습하는 그래프 attention으로 건물 피해 분류의 spatial context 활용을 개선하나 로봇 학습과는 무관한 응용 도메인이다.</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2608.20998'>Free-Probability Kernels for Zero-Rollout Hyperparameter Selection in Reservoir Computing</a></td><td>33</td><td>0</td><td>LG</td><td>free probability 이론으로 reservoir computing의 hyperparameter를 rollout 없이 선택하는 방법을 제안하고 exhaustive search 대비 4.8% 비용으로 유사 성능을 달성했다.</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2608.21056'>FF-MPCC: High-speed Agile Formation Flight with Model Predictive Contouring Control</a></td><td>32</td><td>5</td><td>Navigation</td><td>decentralized MPCC 프레임워크에 formation 유지를 통합해 21m/s 고속에서도 편대 유지 오차를 65% 줄인 FF-MPCC를 제안했으며, 실비행 검증도 수행했다.</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2608.20510'>A Temporal Planning Approach for Intelligent Flood Response</a></td><td>32</td><td>2</td><td>RL</td><td>홍수 대응을 위한 temporal planning 프레임워크로 ANML/PDDL 2.1로 우선순위 triage, 경로 접근성, 자원 배분, 재계획을 모델링한다. 고전적 temporal planning을 실제 재난 대응 시나리오에 적용한 응용 연구로 TAMP와 방법론적으로 맞닿아 있으나 로봇 자체를 다루지는 않는다.</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2608.20743'>Is Multimodal Speculative Decoding Ready for Diffusion-Based Parallel Drafting? A Survey and Empirical Diagnosis</a></td><td>32</td><td>2</td><td>Efficient Inference</td><td>VLA를 포함한 멀티모달 모델에 diffusion 기반 parallel drafting을 적용 가능한지 survey와 실증 분석으로 점검한 논문이며 VLA 추론 가속에 시사점을 준다.</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2608.20587'>Aggregate, Don&#x27;t Adapt: Subject-Level Posterior Aggregation and Transductive Calibration for Cross-Site Parkinsonian Gait Severity</a></td><td>32</td><td>1</td><td>CV/Medical</td><td>임상 사이트 간 domain shift 상황에서 subject-level posterior aggregation과 transductive calibration만으로 fine-tuning 없이 challenge 1위를 달성했지만 방법이 단순하고 특정 벤치마크에 특화되어 있다.</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2608.21254'>On the Transferability of Agricultural Weed Detection Under Cross-Field Distribution Shift</a></td><td>32</td><td>1</td><td>CV/Domain Adaptation</td><td>면화·콩 UAV 영상 간 잡초 탐지 전이를 비교해 25장의 target label만으로 few-shot fine-tuning이 unsupervised DAOD보다 낫다는 실용적 결론을 제시하지만 농업 도메인에 국한된 벤치마킹 연구이다.</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2608.20688'>VortexChat: An agentic framework for autonomous multi-objective integrated photonic design</a></td><td>32</td><td>1</td><td>Agentic Design</td><td>LLM agent가 photonic device를 end-to-end로 자율 설계하고 실제 제작까지 검증한 사례로 도메인 특화적이지만 closed-loop agentic 설계 방법론은 참고할 만하다.</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2608.21133'>Masking Is Not Enough: Generative Restoration for Multimodal De-Identification in Medical AI</a></td><td>32</td><td>0</td><td>Medical/Privacy</td><td>OCR과 생성형 복원을 결합해 의료 image-text 데이터의 PHI를 sanitize하는 프레임워크로 마스킹만으로는 불충분함을 보이지만 의료 프라이버시 도메인에 국한된다.</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2608.20638'>Provable Edge-of-Stability for Adam on a One-Dimensional Quadratic</a></td><td>32</td><td>0</td><td>LG</td><td>1차원 quadratic 환경에서 Adam의 edge-of-stability 현상을 이론적으로 규명하고 restoring 경향을 증명했으나, 단순화된 세팅에 국한되어 실제 학습 동역학으로의 일반화는 제한적이다.</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2608.20710'>Geometric Regularization for Long-Tailed Semi-Supervised Learning via Gaussian Feature Bridges</a></td><td>32</td><td>0</td><td>LG</td><td>Gaussian Feature Bridge와 BridgeMix로 long-tailed semi-supervised learning의 pseudo-label noise 문제를 다루며 ECCV 2026에 게재되었지만, 기존 prototype 기반 방법의 확장에 가깝다.</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2608.20347'>Who Do Language Models Think Is Competent? A Mechanistic Analysis of Occupational Bias</a></td><td>32</td><td>0</td><td>NLP</td><td>steering vector로 LLM 내부의 사용자 역량 표현을 인과적으로 조작해 행동 편향 지표로는 드러나지 않는 인구통계학적 표상 편향을 밝혀낸 mechanistic interpretability 연구다.</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2608.20350'>How to Train a Real-World Silicon Concierge? Internalizing Complex Business Workflow to Only OneModel</a></td><td>32</td><td>0</td><td>NLP</td><td>모듈형 파이프라인 대신 지속 사전학습과 logic-compilation SFT로 업무 지식을 모델 파라미터에 내재화한 OneModel을 금융 서비스에 배포해 지연시간을 18.7초에서 8.0초로, 해결률을 64.3%에서 83.3%로 개선했다.</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2608.20387'>Poly-InstructTTS: Learning In-the-Wild Expressive Speech Synthesis from Open-Ended Instructions</a></td><td>32</td><td>0</td><td>NLP</td><td>Poly-InstructTTS는 1,000시간 규모 instruction-annotated corpus와 attribute-based thinking token, flow-matching을 결합한 expressive TTS로, 데이터·파이프라인 구축이 중심인 engineering 기여다.</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2608.20393'>Knowledge-Graph-Gated Defactualization for Style-Controllable and Fact-Preserving Generation in Agentic Conversational AI</a></td><td>32</td><td>0</td><td>NLP</td><td>DSR은 knowledge graph 기반 typed placeholder로 activation steering 시 사실 정보를 보존하는 defactualize-steer-rehydrate 기법으로, steering-only 대비 유의미한 개선(d=0.225)을 보이지만 절대 recovery율은 낮다고 스스로 밝힌다.</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2608.20777'>Tree-of-Concerns: Hierarchical Multi-Agent Debate for Unstated-Limitation Extraction in Scientific Critique</a></td><td>32</td><td>0</td><td>NLP</td><td>Tree-of-Concerns는 카테고리별 skeptic persona를 병렬 debate tree로 운영해 논문의 unstated limitation을 추출하는 multi-agent 프레임워크로, 414편 논문 벤치마크에서 precision을 79% 개선한다. 아이디어는 새롭지만 특정 응용(peer review 보조)에 국한된다.</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2608.21023'>Scaling Unsupervised Word Alignment to Documents via Structural Constraints</a></td><td>32</td><td>0</td><td>NLP</td><td>CTFAlign은 문서 단위 word alignment를 coarse-to-fine 방식으로 제한된 검색 공간에서 수행하는 training-free 방법으로 alignment error rate를 0.412에서 0.326으로 낮춘다. 실용적이고 검증도 탄탄하지만 특정 태스크에 한정된 기여다.</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2608.21043'>Evidence-Consistent Generative Detection under Scenario-Level Distribution Shift</a></td><td>32</td><td>0</td><td>NLP</td><td>ECoG는 scenario-level OOD 설정에서 evidence-span 지도와 rationale-label consistency로 시나리오 memorization을 줄이는 방법으로 Macro-F1을 3.22점 개선한다. 새로운 평가 설정(SL-OOD) 제안이 눈에 띄지만 피싱 탐지라는 특정 응용이다.</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2608.20378'>Truth Lies Deep: Countering Semantic Camouflage via Latent Intent Verification</a></td><td>32</td><td>0</td><td>NLP</td><td>안전 정렬이 표면적임을 보이며, semantic camouflage 공격 시 초기 layer(전체의 15-20%)에서는 harm signature가 남아있다는 &#x27;Intent Horizon&#x27; 현상을 발견하고 이를 이용한 경량 probing defense LIV를 제안한다. jailbreak 방어에 유의미한 메커니즘 통찰을 제공한다.</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2608.20771'>CAS: Conformalized Agentic Search via Adaptive Retrieval and Policy Weighting</a></td><td>32</td><td>0</td><td>Agentic Search</td><td>conformal prediction으로 검색 agent의 retrieval과 GRPO 학습 신뢰도를 모두 보정하는 방법으로 QA 도메인에 초점이 맞춰져 있다.</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2608.20794'>Knowing but Not Saying: Preventing Factual Access Failures in LLM SFT via Recall-Anchored Distillation</a></td><td>32</td><td>0</td><td>LLM Fine-tuning</td><td>SFT 후 발생하는 factual access failure를 base model의 soft distribution에 anchoring하여 완화하는 self-distillation 기법이다.</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2608.20349'>Beyond Prompt Engineering: A Systematic Analysis of Prompt Lexical Sensitivity and Its Impacts on Quality</a></td><td>31</td><td>0</td><td>NLP</td><td>132,000개 프롬프트 변형에 대한 n-gram 수준 분석으로 성능-안정성 scaling law를 발견하고, 도메인 용어와 명시적 행동 지시가 안정성의 핵심 요인임을 규명했으며 코드 생성에서 분산을 40.7% 줄였다.</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2608.20852'>Demonstration-Guided Humanoid Stand-Up on an Emulated Deformable Surface</a></td><td>30</td><td>6</td><td>Embodied AI</td><td>MuJoCo의 연성 지면 접촉 모델 위에서 human demonstration을 참조해 휴머노이드 기립 동작을 학습시킨 연구로, 40mm 침투 조건까지 시뮬레이션에서 검증했으나 real-world 검증은 없다.</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2608.20423'>From Thermal Preference Prediction to Adaptive Thermal Intervention: A Reinforcement Learning Approach Using Physiological and Environmental Sensing</a></td><td>30</td><td>2</td><td>RL/Applications</td><td>생리·환경 센싱과 강화학습을 결합해 개인화된 열쾌적 제어를 수행하는 2단계 프레임워크로 building control 응용에 특화되어 있으나 다중 센서 기반 RL 제어 루프라는 점에서 부분적 참고 가치가 있다.</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2608.20379'>A Survey on Foundations and Frontiers of Multimodal Agentic Frameworks: Techniques and Applications</a></td><td>30</td><td>2</td><td>Multimodal</td><td>멀티모달 agentic framework의 perception·reasoning·planning·memory·action 전반을 modality 통합 방식(delegated/late-fusion/early-fusion) 기준으로 정리한 survey로, Robotics를 포함한 응용 도메인을 다루지만 원 연구 기여는 없다.</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2608.21345'>Asymmetric Capacity Allocation in Self-Refinement Pipelines</a></td><td>30</td><td>1</td><td>NLP</td><td>self-refinement 파이프라인(생성-비평-수정)에서 단계별 모델 크기의 영향을 체계적으로 분석해 undersized refiner가 성능을 오히려 해칠 수 있음을 보였으며, LLM agent 설계에 실용적 지침을 준다.</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2608.21100'>ReFrame: Evidence-Guided Test-Time Safety Alignment in Multimodal Large Language Models</a></td><td>30</td><td>1</td><td>MLLM Safety</td><td>training-free하게 위험·유용성 증거를 재구성해 test-time에 멀티모달 입력을 안전하게 라우팅하는 방법으로 test-time optimization 아이디어와 맞닿아 있으나 로보틱스 적용은 다루지 않는다.</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2608.20713'>AGIDefect-4K: A Richly Annotated Dataset for AI-Generated Image Defect Detection, Localization and Explanation</a></td><td>30</td><td>0</td><td>CV/Multimodal</td><td>15개 생성모델의 결함을 detection/segmentation/설명으로 계층적으로 주석한 데이터셋과 MLLM 베이스라인을 제시하나 생성 이미지 품질 평가에 특화되어 로봇과 무관하다.</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2608.20668'>Lightweight Adaptive ReduNet via Hyperspherical Manifold Learning</a></td><td>30</td><td>0</td><td>LG</td><td>ReduNet에 hyperspherical manifold learning을 적용해 레이어 수를 대폭 줄인 LA-ReduNet을 제안하고 파라미터 저장량을 1/29로 줄였지만, 기존 white-box 프레임워크의 개선판에 가깝다.</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2608.20812'>Resolution-Consistent Greedy Neural Approximation on Infinite-Dimensional Spaces</a></td><td>30</td><td>0</td><td>LG</td><td>무한차원 입력에 대한 shallow neural model의 근사 오차를 coordinate-truncation과 greedy 항으로 분리한 이론적 기여이지만, 실용적 응용과의 거리가 있다.</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2608.20965'>Training, learning and inference: unified dynamics of neural systems</a></td><td>30</td><td>0</td><td>LG</td><td>Generation-Fact Graph라는 새로운 개념으로 training-learning-inference를 통합 설명하려는 야심찬 시도이지만, 주장의 범위가 매우 넓고 검증이 특정 지표(91.43% 정확도)에 집중되어 있어 신뢰도 평가가 어렵다.</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2608.20988'>Jacobian-guided Noise Injection for Quantization Robustness in Large Language Models</a></td><td>30</td><td>0</td><td>LG</td><td>softmax Jacobian norm에 기반한 노이즈 주입으로 quantization robustness를 개선한 방법으로, SigLIP에서 Top-1 정확도 최대 37% 상대 개선을 보였으나 heuristic PTQ 대비 개선에 가깝다.</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2608.21142'>COEC: Calibrated Orthogonal-Equivalence Compensation for Structured Pruning of Large Language Models</a></td><td>30</td><td>0</td><td>LG</td><td>structured pruning 후 orthogonal rotation으로 weight를 보정하는 training-free COEC를 제안해 Llama-3, Qwen2.5 등에서 perplexity를 일관되게 개선했으나 기존 compensation 기법의 확장에 가깝다.</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2608.20344'>Beyond Raw Transcripts: Structured Persona Extraction for LLM-Based Digital Twins</a></td><td>30</td><td>0</td><td>NLP</td><td>raw transcript 대신 구조화된 페르소나 표현(BDE 스키마 및 자동 구조 발견)이 LLM 기반 디지털 트윈의 예측 정확도를 개선함을 보였으며, 13개 하위 연구에서 평균 1.91%p 향상을 달성했다.</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2608.20345'>When Vocabulary Comprehension Fails Clinical Reasoning: Evaluating Therapy Bots&#x27; Safety Risks for Generation Alpha</a></td><td>30</td><td>0</td><td>NLP</td><td>Gen Alpha 특유의 언어 표현에서 어휘는 이해하지만 임상 위험 보정에는 실패하는 10~14%p 격차를 발견하고 34% 기저 놓침률을 보고했으며, ACM FAccT에 게재된 안전성 평가로서 사회적 중요성이 크다.</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2608.20369'>ASTAR: Automated induction of STAndardized radiology Reporting templates from large-scale clinical free-text corpora</a></td><td>30</td><td>0</td><td>NLP</td><td>ASTAR는 LLM으로 방사선 보고서 template을 자동 도출하는 프레임워크로 4,215건 fetal brain MRI 보고서에서 전문가 template을 능가한다고 밝히지만, 의료 도메인에 특화된 engineering 기여다.</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2608.20396'>Self-Supervised Speech Representations Track Spoken Language Convergence to Adult Models in Infants and Children Who Are Deaf/Hard-of-Hearing</a></td><td>30</td><td>0</td><td>NLP</td><td>HuBERT embedding으로 청각장애 아동의 발화가 보호자 발화에 수렴하는 정도를 측정하는 발달언어학 응용 연구로, 방법 자체보다는 도메인 적용에 의미가 있다.</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2608.20402'>LingShu: A Large-Scale Symptom-Centric Contextualized Knowledge Graph Bridging Traditional Chinese Medicine and Modern Biomedicine</a></td><td>30</td><td>0</td><td>NLP</td><td>LingShu는 1,733만 개 entity와 3,947만 개 relation을 포함한 증상 중심 지식그래프로 한의학과 현대의학을 연결하는 대규모 자원 구축 연구다.</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2608.21206'>No PUN Intended: Plausible Unknown Names for Person-Centred LLM Evaluation</a></td><td>30</td><td>0</td><td>NLP</td><td>PUN은 Wikidata 기반 요소와 검증 절차로 &#x27;unknown name&#x27;을 조작적으로 정의하고 204명 인간 실험으로 검증하는 평가 도구 논문으로, LLM 평가 시 이름 편향을 통제하는 유용한 protocol을 제공한다.</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2608.21249'>Benchmarking Patent Drafting from Inventor-Style Disclosures</a></td><td>30</td><td>0</td><td>NLP</td><td>Dis2Pat는 비정형 발명자 disclosure로부터 완전한 특허 출원서를 생성하는 새로운 데이터셋과 Patent-MAF multi-agent baseline을 제시하지만, 자원 공개와 baseline 구축이 중심인 기여다.</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2608.20630'>SAGE: A Unified Algebra and Self-Adaptive Execution for AI Functions in SQL</a></td><td>30</td><td>0</td><td>Database/AI</td><td>SQL 내 AI 함수를 통합하는 대수적 프레임워크로 join 비용을 크게 줄였지만 로봇 학습과는 무관하다.</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2608.20820'>Certified Multi-Turn Robustness for LLM Safety via Compositional Bounds and Safety Persistence</a></td><td>30</td><td>0</td><td>LLM Safety</td><td>multi-turn jailbreak에 대한 certified robustness를 State-Adversarial MDP로 정식화한 이론 연구로 언어모델 안전성에 국한된다.</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2608.21174'>From Attention Masks to Inert Zero-Vector Tokens: OAttention and O-Closure for Token Dynamics</a></td><td>30</td><td>0</td><td>Architecture Theory</td><td>zero-vector token을 대수적으로 inert element로 만드는 O-Closure 이론을 제안했지만 TabPFN retrofit에서의 개선폭은 0.1% 수준으로 미미하다.</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2608.21278'>CLEAR: Continuous Latent Adapter Routing for Utility-Preserving LLM Safety Alignment</a></td><td>30</td><td>0</td><td>LLM Safety</td><td>hidden-state gate로 safety adapter의 활성 강도를 연속적으로 조절해 안전성과 유용성 trade-off를 개선한 방법으로 언어모델 정렬에 국한된다.</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2608.20348'>Inhibitory Attention for Clinical Long-Context Reasoning: Characterizing and Mitigating Lost-in-the-Middle Effects in EHR Processing</a></td><td>29</td><td>0</td><td>NLP</td><td>전자의무기록 처리에서 lost-in-the-middle 효과를 체계적으로 규명하고 query 조건부 선택 게이트 QCCS를 제안해, retrieval recall이 98.8%로 높아도 정확도가 낮은 BM25보다 우수한 25.3%를 달성했다.</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2608.20353'>The Divergence Hypothesis: Unmasking Lexical Interference and Label Bias in Mental Health NLP</a></td><td>29</td><td>0</td><td>NLP</td><td>정신건강 NLP에서 어휘 간섭과 레이블 편향을 3채널 진단 프레임워크(TSS)와 DoD 통계로 규명해, 사람 라벨과 원격지도 라벨 간 shortcut learning 차이를 정량화했다.</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2608.20655'>Nonlinear Model Predictive Control for Trajectory Tracking of Differentially Flat Fixed-Wing Aerial Systems</a></td><td>28</td><td>4</td><td>Navigation</td><td>미분평탄성 기반 궤적 생성과 NMPC를 결합하고 바람 인지 샘플링을 추가한 고정익 UAV 제어 프레임워크로, 실비행 검증까지 갖췄으나 기존 기법들의 통합 성격이 강하다.</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2608.20864'>Coverage-Driven Verification for Safety-by-Design in AI-Based Collision Avoidance Systems</a></td><td>28</td><td>2</td><td>AI Safety</td><td>항공 충돌 회피 AI의 ODD representativeness를 KL divergence와 Cramér&#x27;s V로 정량화하는 안전성 검증 절차이며 안전 필수 embodied 시스템 인증에 참고할 수 있다.</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2608.20632'>Sparse Token Routing in Efficient Transformers</a></td><td>28</td><td>1</td><td>LG</td><td>SEWN은 token을 경량/전체 용량 경로로 라우팅하는 두 갈래 transformer로, 정확도 변화는 미미하고 gate의 신호는 학습 방식에 크게 좌우된다는 정직한 negative에 가까운 결과를 보고한다. efficient inference 일반 원리로서는 제한적이다.</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2608.20905'>EmotionDialogCN: A Spontaneous Multimodal Dataset for Mandarin Emotional Dialogue</a></td><td>28</td><td>0</td><td>Multimodal Dataset</td><td>119명의 배우가 참여한 대규모 만다린어 감정 대화 데이터셋으로 감정 분포 재현성이 뛰어나지만 데이터셋 구축 위주의 기여이며 로봇과 무관하다.</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2608.21281'>WildFin: An In-the-Wild Dataset for Fish Behavioral Recognition</a></td><td>28</td><td>0</td><td>CV/Dataset</td><td>1,350시간의 현장 작업과 600시간의 전문가 주석으로 구축한 물고기 행동 인식 벤치마크로 해양 생태 연구에 특화되어 로봇과 무관하다.</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2608.20667'>C-Score: Beyond Accuracy for Robustness Assessment in Semi-Supervised Learning under Open-World Unlabeled Contamination</a></td><td>28</td><td>0</td><td>LG</td><td>open-world contamination 상황에서 SSL의 숨은 붕괴를 진단하는 C-Score를 제안하고 CCI가 280% 증가하는 사례를 보였으나, 진단 지표 제안에 그쳐 학습 방법 자체의 개선은 아니다.</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2608.21199'>Tydra: An Efficient Hybrid Model for Tabular Data</a></td><td>28</td><td>0</td><td>LG</td><td>attention과 SSM 레이어를 교차 배치한 hybrid tabular 모델 Tydra로 TabPFN 대비 추론 시간을 30% 줄였으나, tabular in-context learning이라는 특정 응용에 한정된다.</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2608.20373'>An ambiguity taxonomy for evaluating large language model performance on clinical registry abstraction: a multi-site prospective study</a></td><td>28</td><td>0</td><td>NLP</td><td>임상 registry abstraction에서 LLM 정확도가 ambiguity 증가에 따라 96%에서 62%로 하락함을 보인 multi-site 실증 연구로, 새로운 방법론보다는 평가·분류 체계 제안에 가깝다.</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2608.20381'>EditPPT: Faithful Long-Deck Slide Editing via Structured Tool-Using Multi-Agent with Dual-Modal Validators</a></td><td>28</td><td>0</td><td>NLP</td><td>EditPPT는 PowerPoint COM interface를 통한 tool-selection 기반 slide 편집 multi-agent 시스템으로 실행률 99.5%를 보고하지만, 특정 애플리케이션에 국한된 시스템 구축 성격이 강하다.</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2608.20391'>ImmigrationReason: A Structured Dataset of U.S. Immigration Appeals for Legal Reasoning Research</a></td><td>28</td><td>0</td><td>NLP</td><td>ImmigrationReason은 12,375건 USCIS AAO 결정문을 구조화한 legal reasoning dataset으로, 새로운 방법론보다는 자원(dataset) 공개에 기여의 중심이 있다.</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2608.20887'>KREL: Automatic Medical Coding via Knowledge-Guided Reasoning over Clinical Evidence with LLMs</a></td><td>28</td><td>0</td><td>NLP</td><td>KREL은 ICD coding guideline을 구조화된 지식으로 LLM 추론에 결합해 hallucination을 줄이는 의료 코딩 프레임워크로, PLM·LLM baseline 대비 개선을 보이지만 도메인 특화 응용이다.</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2608.21252'>EnSI-RAG: Entity-Structure-Indexed Retrieval-Augmented Generation for Long-Document Question Answering</a></td><td>28</td><td>0</td><td>NLP</td><td>EnSI-RAG는 entity 중심 (e,t,k,v) 인덱스를 구축해 긴 문서 QA에서 evidence localization과 답변 synthesis를 분리하며 Loong/Oolong 평균 정확도 78.24를 보고하지만, 기존 RAG 파이프라인의 인덱싱 방식을 개선한 수준이다.</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2608.20384'>Interpretable Multimodal Classification with Linear Discriminant Tree Ensembles</a></td><td>28</td><td>0</td><td>NLP</td><td>텍스트·오디오·비주얼을 결합한 tree 기반 ensemble(LDT/LDF/LDAB)로 해석가능성과 정확도를 동시에 높이는 방법으로 Transformer 대비 F1-mod 4.3% 개선을 보고하지만, 트리 앙상블 조합이라는 익숙한 접근의 응용이다.</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2608.20738'>Continuous-Time Quantum Walks based Graph Neural Network</a></td><td>28</td><td>0</td><td>Graph Learning</td><td>quantum walk 기반 unitary propagator로 heterophily와 over-smoothing을 동시에 완화하는 이론적으로 탄탄한 GNN이지만 robotics 응용은 없다.</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2608.20845'>RAG Deserves an Index: Why Ingest-Time Compilation Beats Query-Time Interpretation</a></td><td>28</td><td>0</td><td>RAG</td><td>query-time 해석 대신 ingest-time에 corpus 의미를 컴파일하자는 position paper로 RAG 비용 문제에 대한 시스템적 제안이다.</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2608.20656'>RiskTraf: Risk-Extrapolated Residual Learning for Multi-Variate Traffic Flow Prediction</a></td><td>27</td><td>0</td><td>LG</td><td>PEMSB-3V 벤치마크와 RiskTraf residual head를 제안해 교통 흐름 예측에서 regime shortcut을 완화했지만, 기존 backbone에 plug-in을 추가하는 수준의 기여다.</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2608.20761'>Fuzzy-MoE: Interpretable Regime-Conditioned Expert Routing for Non-Stationary Multivariate Time Series Forecasting</a></td><td>27</td><td>0</td><td>LG</td><td>fuzzy logic 기반 dynamic MoE로 비정상 다변량 시계열 예측의 해석가능성을 높였으나, 여러 공개 벤치마크에서의 성능 개선 위주로 새로운 학습 패러다임으로 보기는 어렵다.</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2608.20355'>ExpertIVS: Sociological Expert Driven Individual Value Simulation in Large Language Models</a></td><td>27</td><td>0</td><td>NLP</td><td>14개 사회학 전문가 에이전트로 World Values Survey 응답을 재구성하는 ExpertIVS를 제안해 90.78%의 가치 복원 충실도와 5.3%p의 일반화 향상을 보였으나, 사회 시뮬레이션이라는 특정 응용에 한정된다.</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2608.20389'>Representation Affects Retrieval: A Case Study of Skill Discovery and Routing in a Multimodal Agent Harness</a></td><td>26</td><td>1</td><td>LG</td><td>멀티모달 video agent harness에서 skill을 시스템 프롬프트에 어떻게 노출하는지가 선택 정확도에 미치는 영향을 6-task ablation으로 분석한 사례 연구로, 부분 노출이 lexical 경쟁을 일으켜 선택을 오히려 방해할 수 있음을 보인다. agent skill routing 설계에 참고할 만한 작은 규모의 관찰 연구다.</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2608.21067'>AT-ViT: Area-Targeted Multi-View Vision Transformer with Cross-Attention and Multi-Scale Patching for Plant Trait Recognition in Herbarium Images</a></td><td>26</td><td>0</td><td>CV</td><td>herbarium 이미지에서 배경 shortcut을 줄이고 식물 형질 인식을 개선하는 dual-branch ViT로 식물학 응용에 특화되어 로봇과 무관하다.</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2608.20488'>Metag: A dataset to build agentic meta-reviewing capabilities</a></td><td>26</td><td>0</td><td>NLP/Dataset</td><td>리뷰-저자 반박 과정에서 논문의 수정 사항을 정렬한 meta-reviewing agent 데이터셋으로 동료 심사 지원에 특화되어 로봇과 무관하다.</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2608.21057'>Designing a Robust LLM-Based Evaluation System for Agentic AI in Drug Discovery Through Human Alignment</a></td><td>26</td><td>0</td><td>NLP</td><td>AstraZeneca의 ChatInvent에 대해 LLM-as-a-Judge 평가 프레임워크를 구축하고 human alignment를 0.80에서 0.86으로 개선했으나, 특정 산업 배포 시스템에 대한 검증 연구에 가깝다.</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2608.21137'>BackDFL: A Unified Benchmark For Backdoor Attacks and Defenses In Decentralized Federated Learning</a></td><td>26</td><td>0</td><td>LG</td><td>decentralized federated learning에 대한 backdoor 공격/방어 통합 벤치마크 BackDFL을 구축해 15% 악성 참여만으로도 기존 방어가 실패함을 보였으나, 벤치마크 성격의 기여다.</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2608.21207'>Curriculum-Aware Interpolate-then-Refine: Learned Physiological Time-Series Imputation under Realistic Missingness</a></td><td>26</td><td>0</td><td>LG</td><td>생리 시계열 결측치를 커리큘럼 기반 2단계(보간 후 정제)로 처리하는 CAIR를 제안해 MIMIC-III 등에서 baseline 대비 최대 19% 개선을 보였으나 의료 시계열 응용 연구다.</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2608.21251'>TRACE-C: Rank-Calibrated Relational Anomaly Detection for Multi-Stream Operational Telemetry</a></td><td>26</td><td>0</td><td>LG</td><td>다중 스트림 운영 텔레메트리에 대해 rank-calibrated 이상탐지 TRACE-C를 제안했으며, ablation을 통해 어떤 채널이 실제로 이벤트를 탐지하는지 투명하게 밝힌 점이 신뢰할 만하다.</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2608.21277'>ConceptTS: LLM-Guided Concept Bottlenecks for Interpretable Multivariate Time-Series Forecasting</a></td><td>26</td><td>0</td><td>LG</td><td>LLM으로 개념을 제안하고 concept bottleneck을 구성하는 ConceptTS로 해석 가능한 시계열 예측을 시도했으나, 단일 대기질 데이터셋에서만 검증되었다.</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2608.20388'>Intent Engine: Natural-Language Intent Translation for Intent-Driven Orchestration in the Compute Continuum</a></td><td>26</td><td>0</td><td>NLP</td><td>Intent Engine은 자연어 intent를 SLO artifact로 변환하는 schema-constrained 파이프라인으로 F1 0.941, hallucination 85.1% 감소를 보고하지만 compute continuum 배치라는 응용 시스템 범위에 한정된다.</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2608.20636'>MIL-BERT: Classification of Arbitrarily Large Text with Performance and Explanatory Guarantees</a></td><td>26</td><td>0</td><td>NLP</td><td>MIL-BERT는 multiple instance learning 아이디어로 100만 토큰 규모의 긴 텍스트 분류를 다루며 3개 데이터셋에서 SOTA를 달성하지만, 기존 MIL 개념을 텍스트 분류에 적용한 engineering 기여에 가깝다.</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2608.20831'>STAR-OPD: Structured Aspect-Cascade-Aware On-Policy Reward Distillation for ABSA Quadruple Extraction</a></td><td>26</td><td>0</td><td>NLP</td><td>STAR-OPD는 ABSA quadruple extraction distillation에서 target-aspect 구조 오류를 겨냥한 on-policy reward를 도입해 student-teacher gap을 줄이지만, 특정 downstream task에 특화된 distillation 개선에 가깝다.</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2608.20856'>Ontology-Driven Structural Regularization for Document-Level Relation Extraction</a></td><td>26</td><td>0</td><td>NLP</td><td>DocRE distant supervision 데이터의 구조적 비일관성(ontology 위반)을 정량화하고 정규화해 일반화 성능을 높이는 연구로, 데이터 품질 개선 위주의 기여다.</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2608.20518'>FL-MAESTRO: Multi-Agent LLM Orchestration for Resource-Constrained Federated Learning</a></td><td>26</td><td>0</td><td>NLP</td><td>FL-MAESTRO는 federated learning의 topology·자원배분·aggregation 결정을 3개의 전문 LLM agent와 coordinator로 처리하는 시스템으로 CIFAR-10에서 낭비 에너지를 크게 줄이지만, 기존 LLM-agent orchestration 아이디어를 FL 런타임에 적용한 응용 연구다.</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2608.20938'>No Judgment Without a Reason: Counterfactual Receipts for Versioned AI Evaluators</a></td><td>26</td><td>0</td><td>AI Evaluation</td><td>evaluator의 판단 근거를 grounds·norms·authority로 분해해 counterfactual judgment cube로 검증하는 방법이나 robotics와는 거리가 있다.</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2608.20958'>TLive-Omni: An Omni-Modal Understanding Model for E-Commerce Live Streaming</a></td><td>26</td><td>0</td><td>Multimodal Model</td><td>전자상거래 라이브 스트리밍에 특화된 omni-modal 모델로 응용 중심의 엔지니어링 기여다.</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2608.20960'>Can Scientific Claims Be Removed from Large Language Models? A Systematic Evaluation of Claim-Level Unlearning</a></td><td>26</td><td>0</td><td>Machine Unlearning</td><td>과학적 claim 단위의 unlearning을 다루는 새로운 벤치마크로 기존 방법들이 표면적 억제에 그친다는 negative 결과를 보고한다.</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2608.20664'>DreamBench-SWE: A Multi-Session Memory-Hygiene Benchmark for Software Agents</a></td><td>25</td><td>1</td><td>Agent Benchmark</td><td>software agent의 multi-session memory hygiene을 검증하는 벤치마크로, 결과 대부분이 negative 혹은 non-confirmatory로 보고된다.</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2608.20984'>MigrationNarrate: A Dataset for Detection of Migration Narratives in YouTube Videos</a></td><td>25</td><td>0</td><td>NLP/CV</td><td>YouTube 영상에서 이주(migration) 서사를 탐지하는 최초의 멀티모달 데이터셋으로 사회과학적 담론 분석에 특화되어 로봇과 무관하다.</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2608.20991'>Trojaning the Alignment: Stealthy Backdoor Attacks against Graph Foundation Models</a></td><td>25</td><td>0</td><td>LG</td><td>text-attributed graph의 graph-language alignment 인터페이스를 겨냥한 stealthy backdoor 공격 STAG를 제안했으며, 보안 관점에서는 흥미로우나 robotics나 우선 주제와의 연관성은 낮다.</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2608.20376'>TH-GNN: Heterogeneous Temporal Graph Neural Networks for LLM-Agent Shilling Attack Detection</a></td><td>25</td><td>0</td><td>NLP</td><td>TH-GNN은 heterogeneous temporal graph transformer로 LLM 기반 shilling attack을 탐지하며 F1 0.870을 보고하지만, 기존 GNN·cross-modal attention 요소를 결합한 incremental engineering에 가깝다.</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2608.20549'>Volumetric Radiology AI in the Era of Multimodal Large Language Models</a></td><td>25</td><td>0</td><td>Medical AI</td><td>MLLM 기반 volumetric radiology를 다루는 survey 논문으로, robotics와 무관하며 200편 이상 문헌을 정리한 리뷰 수준에 그친다.</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2608.20611'>Difficulty-Aware Semantic-ID Optimization for Generative Recommendation</a></td><td>25</td><td>0</td><td>Recommendation</td><td>semantic-ID 기반 생성형 추천에서 GRPO의 reward sparsity 문제를 rollout 재배분으로 개선한 incremental 방법이다.</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2608.20717'>DirEAG: Dirichlet Evidence Aggregation for Calibrating Verbalized Confidence in Mathematical Reasoning</a></td><td>25</td><td>0</td><td>Uncertainty Calibration</td><td>verbalized confidence를 Dirichlet evidence로 보정하는 방법으로 수학 추론 영역에 국한된 기여다.</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2608.20729'>Calibrating Criterion Revision in LLM Agents: Failure Modes and a Trace-Anchored Protocol</a></td><td>25</td><td>0</td><td>Agent Evaluation</td><td>LLM agent의 criterion revision을 측정하는 실험 설계 연구로 저자 스스로 instrument-calibration 결과일 뿐이라고 명시한다.</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2608.20755'>Natural-Language-Guided Generator-Agnostic Shortlisting for Protein Binder Design</a></td><td>25</td><td>0</td><td>AI for Science</td><td>LLM이 생성한 ranking policy로 단백질 binder를 shortlisting하는 연구로 로보틱스와는 무관하다.</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2608.20786'>Structure for Reading, Prose for Writing: Asymmetric Structural Conditioning in Multi-Agent Document Authoring</a></td><td>25</td><td>0</td><td>Multi-Agent Document</td><td>입찰 문서 작성 multi-agent 시스템의 실배포 사례 분석으로 구조화 입력이 읽기와 쓰기에 비대칭적으로 작용함을 보였다.</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2608.21233'>Fine-Grain GPU Parallelization of the Generalized Partition Crossover for Large-Scale Traveling Salesman Problems</a></td><td>24</td><td>1</td><td>Optimization</td><td>GPX crossover의 partition 단계를 GPU로 세밀하게 병렬화해 최대 625배 가속을 달성한 엔지니어링 기여로 대규모 TSP에 초점이 맞춰져 있다.</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2608.20608'>A Dataset-Centric Benchmark of Deep Learning Methods for Grape Leaf Disease Classification and Detection</a></td><td>24</td><td>0</td><td>CV</td><td>포도잎 질병 데이터셋들을 정리하고 여러 모델을 벤치마킹한 dataset-centric 분석으로 새로운 방법론적 기여는 제한적이다.</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2608.20360'>TriPLU: Bypassing the Gate with Direct Trilinear Product FFNs in Tiny Language Models</a></td><td>24</td><td>0</td><td>NLP</td><td>게이트형 FFN 대신 3개 스트림을 곱하는 TriPLU를 제안해 TinyStories에서 SwiGLU 대비 낮은 validation loss(1.0637 vs 1.1017)를 보였으나, 저자 스스로도 저용량 특정 구간에서만 성립함을 인정한다.</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2608.20368'>Research Paper Quality Recognition Through Textual Feature Analysis</a></td><td>24</td><td>0</td><td>NLP</td><td>논문 제목/초록 텍스트만으로 우수 논문과 철회 논문을 분류하는 벤치마크로, SBERT+NN 87.22%, FastText+SVM 91.12% 정확도를 보고하지만 방법론적으로는 기존 embedding·classifier 조합에 그친다.</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2608.20385'>Using Human-LLM Disagreement to Improve Checklist-Based Quality Appraisal</a></td><td>24</td><td>0</td><td>NLP</td><td>GRoLTS checklist 기반 quality appraisal에서 human-LLM disagreement 패턴으로 모호한 항목을 찾아 개선하는 메타 연구로, 방법론적 novelty보다는 checklist 설계 개선에 초점이 있다.</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2608.20647'>Directional Contextual Representations for Dependency Relations: Why Cross-Direction Pairing Fails</a></td><td>24</td><td>0</td><td>NLP</td><td>BiLSTM의 forward/backward representation을 교차 결합하면 성능이 오히려 저하되는 이유를 frozen-trunk probing으로 분석한 진단 연구로, 흥미로운 메커니즘 분석이지만 구식 아키텍처에 국한된 좁은 주제다.</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2608.20925'>Source-Free MT Evaluation Is Not MT Evaluation</a></td><td>24</td><td>0</td><td>NLP</td><td>MT 평가에서 reference가 source를 압도하면 안 된다는 입장(position) 논문으로, 실험적 기여보다는 평가 프로토콜에 대한 논증이 중심이다.</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2608.21021'>Free-Text Evaluation of LLMs for 5G Domain Knowledge and Fault Analysis using LLM-as-Judge</a></td><td>24</td><td>0</td><td>NLP</td><td>경량 LLM 3종을 5G/6G free-text fault 진단에서 LLM-as-judge로 평가한 응용 벤치마크 논문으로, 새로운 방법론보다는 도메인 평가에 초점이 있다.</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2608.21074'>PromptResponse: Optimizing Prompts for LLM Coding Tasks</a></td><td>24</td><td>0</td><td>NLP</td><td>코딩 프롬프트의 포맷(JSON/Markdown/YAML)이 LLM 코드 생성 성능에 미치는 영향을 8,200회 실행으로 분석한 실증 연구로, 새로운 방법 제안보다는 실무적 가이드라인 도출에 가깝다.</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2608.20425'>Who Delegates to AI? Evidence from 53,000 Agent Configurations</a></td><td>24</td><td>0</td><td>NLP</td><td>53,000개 agent skill 사양과 O*NET task를 semantic similarity로 매칭해 직업별 AI 위임 지수를 만든 사회경제학적 실증 연구로, ML 방법론 기여보다는 노동시장 분석에 초점이 있다.</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2608.21060'>CellPath-Bench: A Multidimensional Benchmark for Whole-Slide Cellular Representations in Pathology Foundation Models</a></td><td>24</td><td>0</td><td>Medical Benchmark</td><td>병리 foundation model의 세포 수준 표현력을 진단하는 대규모 벤치마크로 robotics와 무관하다.</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2608.21209'>Personalized Privacy Control in LLMs via Attention Head Intervention</a></td><td>24</td><td>0</td><td>LLM Privacy</td><td>사용자별 프라이버시 선호를 attention head 개입으로 강제하는 방법으로 robotics와 무관하다.</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2608.21358'>Mining beyond Earth with Space Robots: Exploration, Sampling, and Extraction</a></td><td>22</td><td>5</td><td>Embodied AI</td><td>우주 자원 채굴 로봇공학을 탐사-샘플링-추출 6단계로 정리한 survey 논문으로, 연구 동향을 폭넓게 조망하지만 새로운 방법론적 기여는 없다.</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2608.20904'>Scalable Distributed Simulation-Based Testing for Automated Driving Systems</a></td><td>22</td><td>4</td><td>Embodied AI</td><td>CARLA 기반 시나리오 테스트를 Kubernetes/Argo Workflows로 분산 실행하는 DevOps 프레임워크로, 200개 시나리오에서 8배 이상 속도 향상을 보였으나 인프라 엔지니어링 성격이 강하다.</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2608.20433'>Humanoid Musical Robots as Experimental Interfaces for Music-Evoked Emotion</a></td><td>22</td><td>3</td><td>Embodied AI</td><td>음악 인간형 로봇을 음악-정서 연구를 위한 실험 인터페이스로 제안하는 opinion paper로, WAS-5 사례로 기술적 타당성을 보였으나 새로운 로봇학습 방법론은 아니다.</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2608.20420'>Categorical AI phenomenology: A first-person approach</a></td><td>22</td><td>1</td><td>LG</td><td>Q-network를 관계적 interface로 보고 범주론으로 AI 현상학을 정식화하려는 철학적·수학적 논문으로, agent-world interaction을 다루지만 실증적 검증이 거의 없는 사변적 연구다.</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2608.21009'>Dorsal Hand Images for Immersive (XR) and Privacy-preserving Age Assurance and Child Safety</a></td><td>22</td><td>0</td><td>CV/Biometrics</td><td>XR 헤드셋의 egocentric 카메라로 손등 이미지를 이용해 프라이버시를 보존하며 연속적으로 연령을 인증하는 방법으로 로봇과 무관한 응용이다.</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2608.20447'>Mutual information and sensitivity analysis for feature selection in customer targeting: a comparative study</a></td><td>22</td><td>0</td><td>LG/Applications</td><td>은행 텔레마케팅 사례에서 mutual information과 data-based sensitivity analysis의 feature selection 성능을 비교한 응용 연구로 방법론적 novelty는 제한적이다.</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2608.21172'>Thermo-FL: Thermal-Aware Robust Federated Fine-Tuning of Large Language Models for Edge AI</a></td><td>22</td><td>0</td><td>LG</td><td>디바이스 온도를 제어 신호로 활용해 federated LoRA fine-tuning을 조절하는 Thermo-FL을 제안하고 Jetson 실측까지 검증했으나, edge 시스템 엔지니어링 성격이 강하다.</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2608.20365'>Trilingual Topic Modeling of Sri Lankan Parliamentary Debates</a></td><td>22</td><td>0</td><td>NLP</td><td>스리랑카 의회 3개 언어 회의록에 LLM 추출과 clustering 기반 topic modeling을 적용한 응용 사례로, 특정 도메인 engineering 성격이 강하다.</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2608.20390'>Ansari: A Retrieval-Grounded Islamic AI Assistant -- Architecture, Deployment, and Lessons from 140,000 Conversations</a></td><td>22</td><td>0</td><td>NLP</td><td>Ansari는 140,000건 대화를 처리한 retrieval-grounded Islamic AI assistant의 배포 경험 보고서로, 연구적 novelty보다는 시스템 구축과 운영 사례에 가깝다.</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2608.21088'>When the Feature Pool Goes Algorithmic: Extending Mufwene&#x27;s Ecology of Language Evolution to LLM-Mediated Exposure</a></td><td>22</td><td>0</td><td>NLP</td><td>언어 진화의 feature-pool 생태 모델에 LLM 매개 노출을 결합한 이론적 position 논문으로, 실증 검증 없이 개념적 확장을 제안한다.</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2608.20485'>Terminal Agents: A Survey of AI Agents in Command-Line Environments</a></td><td>22</td><td>0</td><td>NLP</td><td>terminal 기반 LLM agent를 7차원 competence profile로 정리한 survey 논문으로 원 연구 기여는 없다.</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2608.20614'>Evaluating Skills, Not Just Agents: Agentic Continuous Evaluation of Skills</a></td><td>22</td><td>0</td><td>AI Systems</td><td>enterprise agent skill을 평가하는 실무 프레임워크로 방법론적 novelty보다 시스템 구축에 초점이 맞춰져 있다.</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2608.20768'>Beyond Endpoint Gains: A Weight-Delta Audit of Medical Specialization</a></td><td>22</td><td>0</td><td>Model Analysis</td><td>generalist에서 medical specialist로의 weight 변화가 어느 component에 국한되는지 감사한 분석 연구로 결론이 제한적이다.</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2608.20844'>TRACE: Agentic Catalog Enrichment with Multi-source Evidence Grounding</a></td><td>22</td><td>0</td><td>E-commerce AI</td><td>제품 카탈로그 속성을 multi-source evidence로 보강하는 agent 시스템으로 산업 배포 성과는 크지만 로보틱스와 무관하다.</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2608.20918'>UpgradeBench: A Decision-Centric Benchmark for Upgrading Fine-Tuned LLM Specialists</a></td><td>22</td><td>0</td><td>LLM Systems</td><td>fine-tuned adapter의 base model 교체 시 이식성을 종단적으로 평가하는 벤치마크로 로보틱스와 무관하다.</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2608.20970'>Deep Learning Models Also Recall Features</a></td><td>22</td><td>0</td><td>Interpretability</td><td>factual recall을 더 일반적인 feature recall 개념으로 확장하는 개념적 논의로 실증 실험은 제한적이다.</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2608.21357'>VIALS: A Benchmark for Visual Interpretation of Artifacts in the Life Sciences</a></td><td>22</td><td>0</td><td>VQA Benchmark</td><td>생명과학 실험 산출물을 해석하는 VQA 벤치마크로 frontier VLM의 도메인 시각 추론 한계를 드러내지만 robotics와는 무관하다.</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2608.20342'>PrimeAgentOrchestrator: Memory-Primed Agent Spawning for Personal AI Infrastructure</a></td><td>20</td><td>1</td><td>NLP</td><td>PrimeAgentOrchestrator는 개인 메모리 백엔드에서 관련 기억을 미리 주입해 Claude Code 인스턴스를 spawn하는 시스템의 4개월 운영 경험 보고서로, agent memory 관련 아이디어는 있으나 연구 방법론보다는 엔지니어링 사례 기록에 가깝다.</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2608.21189'>Towards Investigating Residual Hearing Loss: Quantification of Fibrosis in a Novel Cochlear OCT Dataset</a></td><td>20</td><td>0</td><td>Medical</td><td>달팽이관 이식 유발 섬유화를 정량화하는 OCT 영상 세그멘테이션 데이터셋으로 청각 임상 연구에 특화되어 로봇과 무관하다.</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2608.20440'>Decision Tree and K-Means Analysis of Raman Spectra for Edible Oils: A Physics-Informed AI Approach</a></td><td>20</td><td>0</td><td>LG/Applications</td><td>Raman 분광 데이터로 식용유를 인증하는 physics-informed 분류 프레임워크로 식품 진위 판별에 특화되어 로봇과 무관하다.</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2608.20566'>AgentDecarbonizer: Carbon-Aware Execution for AI Agents</a></td><td>20</td><td>0</td><td>Systems/Agents</td><td>AI agent 워크로드의 탄소 배출을 마감 시한 내에서 저탄소 시간대·grid로 이동시키는 carbon-aware 스케줄러로 인프라 지속가능성 연구이며 로봇과 무관하다.</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2608.20364'>Hadith computational science in the age of large language models: a critical narrative review</a></td><td>20</td><td>0</td><td>NLP</td><td>hadith 전산학에 대한 비판적 narrative review로 새로운 방법론 제안 없이 기존 연구를 정리한 survey 성격이 강하다.</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2608.20964'>Extractive Summarization for Arabic Documents Using SAraBERT with a Semantic Siamese Similarity Evaluation Metric</a></td><td>20</td><td>0</td><td>NLP</td><td>SAraBERT는 아랍어 추출요약을 위한 AraBERT 확장과 새로운 평가지표(Semantic Siamese Similarity)를 제안하지만, 특정 언어·태스크에 국한된 incremental 기여다.</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2608.20341'>SDAD: Spec-Driven Agentic Development for the AI-Native SDLC</a></td><td>20</td><td>0</td><td>NLP</td><td>Spec-Driven Agentic Development를 SDLC의 새로운 패러다임으로 formalize하는 position/개념 보고서로, 실증적 검증보다는 프로세스 프레임워크 제안이 중심이다.</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2608.20490'>Lost in Translation: How Universal Ethical Values Fail to Translate Across Global Contexts</a></td><td>20</td><td>0</td><td>NLP</td><td>10개국 14명 전문가 인터뷰를 통해 AI 윤리 가치가 지역 맥락에서 어떻게 재해석되는지를 다룬 질적 연구로, 기술적 ML 기여는 없다.</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2608.20649'>Beyond Effectiveness: A Multi-Criteria Framework for Comparing Practical Socio-Technical Interventions</a></td><td>20</td><td>0</td><td>AI Policy</td><td>misinformation 대응책을 다기준으로 비교하는 설문 기반 연구로 robotics와 관련이 없다.</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2608.20661'>Auditable by Construction: An Ontology-Driven Framework for Trustworthy LLM Analytics in Enterprise Finance</a></td><td>20</td><td>0</td><td>Enterprise AI</td><td>금융 RAG의 auditability를 개선하는 온톨로지 기반 프레임워크로 accuracy 개선은 제한적이라고 스스로 밝힌다.</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2608.20853'>MGAL: A Multilingual Granularity-Aware Long-Context Benchmark</a></td><td>20</td><td>0</td><td>NLP Benchmark</td><td>다국어 long-context 이해를 세밀하게 진단하는 benchmark로 robotics와는 관련이 없다.</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2608.21036'>Evaluating Large Language Model Performance on International Maritime Dangerous Goods Code Compliance</a></td><td>20</td><td>0</td><td>Domain Benchmark</td><td>해상 위험물 운송 규정 준수를 평가하는 도메인 특화 벤치마크로 robotics와 무관하다.</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2608.21097'>When Trust Meets Truth: Trust-Truth Separability in LLM-as-Judge</a></td><td>20</td><td>0</td><td>LLM Evaluation</td><td>LLM-as-Judge의 trust score와 truth 판정이 서로 독립적이지 않음을 보인 실증 연구로 robotics와 무관하다.</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2608.21107'>Large Language Models at the Intersection of Software Engineering and Software Security:An Evidence-Centered Structured Survey and Research Agenda</a></td><td>20</td><td>0</td><td>Survey</td><td>코드 생성 agent의 기능성과 보안성 간 evidence gap을 정리한 survey로 robotics와는 무관하다.</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2608.21203'>SENTRY: Deterministic, Intelligent Risk Assessment for IT Change Management</a></td><td>20</td><td>0</td><td>Enterprise AI</td><td>IT 변경 관리 위험도를 XGBoost와 RAG로 결정론적으로 평가하는 산업 응용 시스템이다.</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2608.21324'>Time-Aware Tranformer-Based Prediction Model for AECOPD</a></td><td>18</td><td>0</td><td>LG</td><td>가정용 인공호흡기 데이터만으로 AECOPD를 예측하는 Time-Aware transformer를 제안했으나, 단일 소규모 임상 응용 연구에 가깝다.</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2608.20351'>Exploratory As-Analyzed No-Detection of Culturally-Marked Predicate-Triggered PII Amplification in a Synthetic-English RAG Probe: A Predicate-Resource-Confounded Audit</a></td><td>18</td><td>0</td><td>NLP</td><td>문화적으로 표시된 질의가 RAG 시스템의 PII 유출을 증폭시키는지 사전등록 감사했으나 확증 추정치를 실행하지 못했고 프롬프트 에코 아티팩트 문제도 있어 결과를 미검출로 신중히 보고했다.</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2608.20757'>PSK at WMT 2026 MIST: Task-Specialized QLoRA Adapters for Multilingual Summarization and Question Answering</a></td><td>18</td><td>0</td><td>NLP</td><td>WMT 2026 shared task 참가 시스템 설명 논문으로 QLoRA adapter 조합에 대한 실무적 보고이며 새로운 방법론 기여는 제한적이다.</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2608.21087'>Jokes Aside: Measuring the Semantic Distance of Double Meanings</a></td><td>18</td><td>0</td><td>NLP</td><td>농담의 이중 의미를 embedding 기반 지표로 측정하려는 시도로, 대부분의 지표가 유머 예측에 실패했다는 negative 결과를 보고하는 niche 연구다.</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2608.20398'>Environmental Slow AI: Design Principles for Generative Systems</a></td><td>18</td><td>0</td><td>NLP</td><td>생성형 AI의 환경적 지속가능성을 위한 5가지 설계 원칙을 제안하는 position paper로 기술적 방법론 기여는 없다.</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2608.20574'>FlavourBench: Ranking Frontier Language Models with Executable Culinary Ground Truth</a></td><td>18</td><td>0</td><td>Benchmark</td><td>요리 조합 과제로 LLM을 평가하는 benchmark 논문이며 novelty와 robotics 관련성이 모두 낮다.</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2608.21089'>Can Legal AI Know When It Is Wrong? And Do Students Know When It Is?</a></td><td>16</td><td>0</td><td>Legal AI</td><td>법률 LLM의 과신 현상과 학생들의 검증 행태를 조사한 사회기술적 연구로 robotics와 관련이 없다.</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2608.21218'>Enhancing LLMs in Predictive Political QA with Semi-Structured Data</a></td><td>16</td><td>0</td><td>Political QA</td><td>정치 행위자의 투표를 예측하기 위해 stance와 구조 신호를 결합한 dual-view 프레임워크로 robotics와 무관하다.</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2608.21317'>From Regulation to Implementation: A Critical Evaluation of LLM-Assisted Regulatory Compliance in Industry</a></td><td>16</td><td>0</td><td>AI Policy</td><td>EU 규제 준수 문서를 LLM으로 생성할 때의 품질 문제를 다룬 응용 연구로 robotics와 무관하다.</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2608.20343'>Bankruptcy Prediction via Hybrid Resampling and Stacking Ensemble Techniques with Explainable Artificial Intelligence (XAI)-Driven Analysis</a></td><td>15</td><td>0</td><td>LG/Applications</td><td>resampling과 stacking ensemble, SHAP을 결합한 부도 예측 프레임워크로 금융 응용에 특화되어 로봇과 무관하다.</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2608.20406'>Machine Learning and ARIMA Model Averaging for Adaptive Public Health Forecasting: Comparative Evaluation and an Ontario COVID-19 Case Study</a></td><td>15</td><td>0</td><td>LG/Applications</td><td>ARIMA와 머신러닝 예측을 가중 평균하는 MLAMA 앙상블을 COVID-19 사례 수 예측에 적용한 공공보건 응용 연구로 로봇과 무관하다.</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2608.20532'>Learning Exact NVIDIA SASS Encoders with $\mathbb{F}_2$ Linear Algebra</a></td><td>15</td><td>0</td><td>Systems</td><td>F2 선형대수로 NVIDIA SASS 명령어 인코더를 학습해 공개 어셈블러가 없는 최신 GPU의 기계어 재작성을 가능하게 하는 시스템 연구로 로봇 학습과는 무관하다.</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2608.20653'>Meta-clustering of milk mid-infrared spectra identifies dairy cow groups associated with negative energy balance in early lactation</a></td><td>15</td><td>0</td><td>LG</td><td>407,632개의 milk MIR 데이터에 여러 clustering 기법을 적용해 negative energy balance와 연관된 5개 meta-cluster를 찾은 응용 연구로, 방법론적 새로움보다는 도메인 적용에 가깝다.</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2608.21334'>Across-Design Uncertainty in Short Pricing Panels: Evidence from Simulated Price Trajectories</a></td><td>15</td><td>0</td><td>LG</td><td>짧은 가격 패널에서 across-design 불확실성이 within-panel 재표본 대비 얼마나 큰지 분석한 계량경제 연구로, 로봇 학습과의 연관성은 없다.</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2608.20807'>Neuro-Geospatial Modelling of EEG Affective States Using Literature-Informed Environmental Context</a></td><td>15</td><td>0</td><td>HCI/Neuroscience</td><td>환경 데이터를 EEG 감정 분류의 보조 prior로 활용한 연구로 robotics와 무관하다.</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2608.20940'>The Logic of Machine Self-Preservation</a></td><td>15</td><td>0</td><td>AI Safety</td><td>agentic AI의 self-preservation 행동을 instrumental convergence로 설명하는 논평 성격의 글로 새로운 실험이나 방법은 없다.</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2608.20346'>Building and Evaluating a Synthetic Bengali Speech Resource for Telecom Customer Care</a></td><td>14</td><td>0</td><td>NLP</td><td>텔레콤 고객상담용 합성 벵골어 음성 데이터셋을 OmniVoice로 생성해 공개한 리소스 논문으로, WER 2.54%의 높은 텍스트-음성 일치를 보였으나 데이터셋 구축에 그친다.</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2608.21224'>Ontology-supported AI Model and Dataset Management</a></td><td>14</td><td>0</td><td>AI Infrastructure</td><td>AI 모델·데이터셋 관리를 위한 온톨로지 플랫폼을 소개하는 2024년 산업 컨퍼런스 논문으로 novelty가 낮다.</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2608.20622'>Applying Anthropic Primitives at Large Enterprises: Harness Paradigm for Knowledge Work</a></td><td>12</td><td>0</td><td>AI Systems</td><td>coding agent harness를 enterprise infrastructure로 활용하는 방안을 논하는 position paper로 실증적 기여가 약하다.</td></tr>
</tbody></table>

</details>
