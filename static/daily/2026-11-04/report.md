# 오늘의 arXiv Top 15: 2026-11-04 (수)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**
> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)

**신규 논문 수: 전체 489편 → 중복 제거 후 489편 (이번 평가 대상 488편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 143 |
| cs.LG | 134 |
| cs.RO | 55 |
| cs.CL | 52 |
| cs.AI | 105 |

*1차 스크리닝: 전체 488편을 제목/초록 기반으로 채점(Claude (scheduled agent)) → 상위 15편은 arXiv 원문을 내려받아 정밀 리뷰(Claude (scheduled agent)) 후 최종 점수 산정.*

---

## Top 15

### 1. Future Representation Distillation for Imagination-free World Action Models (84점)

[arXiv](https://arxiv.org/abs/2611.04527) · [PDF](https://arxiv.org/pdf/2611.04527) · [alphaXiv](https://www.alphaxiv.org/abs/2611.04527) (요약 있음) · [프로젝트 페이지](https://harryjo97.github.io/dreamfree/) · [코드](https://github.com/harryjo97/dreamfree)

- **저자**: Jaehyeong Jo, Sangwon Jang, Sihyun Yu, Seonghyeon Ye, Yekyung Nah, Hojung Jung, Kimin Lee, Sung Ju Hwang
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 68점
- **읽은 원문**: PDF 전문

> video diffusion model이 미래 프레임에서 뽑은 feature를 현재 관측만 보는 encoder에 distillation해서, 미래 video를 만들지 않고 action을 예측하는 World Action Model을 만듦. DROID(대규모 실로봇 조작 데이터셋) 설정의 실제 과제 10개 성공률이 64%로 DreamZero(56%)보다 높고, action chunk당 latency는 91ms로 DreamZero보다 17.8배 빠름.

**무슨 문제인가**

World Action Model(WAM)은 사전학습된 video diffusion model이 아는 장면 변화 지식을 robot control에 쓰는 policy임. 기존 WAM은 미래 video를 action과 함께 생성하거나, 생성한 video에서 action을 뽑음. 이 방식은 배포 때마다 video denoising을 반복해서 느림. 또 생성한 미래 장면이 틀리면 action도 틀림. Fast-WAM처럼 학습 때만 video를 함께 학습하고 추론 때는 video를 만들지 않는 방법도 있으나, 이 feature에 예측 지식이 얼마나 남는지는 불분명했음.

**어떻게 푸나**

DreamFree는 학습을 두 단계로 나눔. 첫 단계에서는 사전학습된 video DiT(Wan2.2 5B 또는 14B)를 visual encoder로 씀. attention mask를 걸어 현재 프레임 token이 현재 관측과 instruction만 보게 함. 고정된 teacher video diffusion model은 현재와 미래 프레임이 모두 든 demonstration video에서 hidden feature를 뽑음. encoder의 현재 프레임 feature를 projector로 teacher feature 형태에 맞춤. 그다음 둘의 유사도를 높이는 future representation distillation loss를 씀. 원래의 video 생성 flow matching loss도 함께 써서 생성 능력을 유지함. 이 단계는 action label이 필요 없음. 둘째 단계에서는 Perceiver식 readout이 encoder feature에서 action용 token을 뽑음. 1B action DiT가 이 token과 instruction, proprioception을 받아 32 step action chunk를 flow matching으로 생성함. 배포 때는 teacher와 projector를 버리고 encoder를 한 번만 통과시킴.

**결과**

- RoboCasa-Kitchen(시뮬레이션 주방 조작 과제 24개, 과제당 demonstration 50개)의 평균 성공률이 14B backbone에서 71.7%임. distillation loss를 빼면 47.2%, 생성 loss를 빼면 55.6%로 내림.
- 같은 benchmark에서 추론 때 video를 만들지 않는 Fast-WAM은 44.4%이고, backbone을 14B로 키워도 44.7%임. DreamFree는 5B에서 14B로 키우면 58.5%에서 71.7%로 오름. action label 없는 추가 video를 encoder 학습에 쓰면 74.4%임.
- 실제 DROID 로봇에서 사전학습 분포 안의 과제 10개를 새 물체·배치로 과제당 5회 평가함. 평균 성공률은 64%로 DreamZero 56%, π0.5 16%보다 높음. 수건 덮기, 모자 걸기, 볼트 담기에서 DreamZero는 전부 실패함.
- action label 없이 composite 과제 video만 encoder 학습에 넣으면, 시뮬레이션 composite 과제 3개의 평균 성공률이 0%에서 21.7%로 오름. distillation 없이 같은 video를 넣으면 0%임. 평가 로봇과 다른 dual-arm Franka의 video만 encoder 학습에 더 넣으면, ALOHA-AgileX(양팔 조작 로봇) 과제 평균 성공률이 6.7%에서 30%로 오름.

**한계**

실로봇 정량 평가는 DROID 과제 10개, 과제당 5회뿐이고 모두 사전학습 분포 안의 과제 종류임. 저자는 DreamZero가 수건 덮기 등에서 실패한 사례 대부분에서 부정확한 미래 video 예측을 관찰했다고 씀. 이것이 실패 원인인지 다른 차이를 통제해 확인한 실험은 없음. video만으로 배우는 과제 전이는 base policy가 필요한 동작을 이미 할 수 있을 때만 됨: cabinet을 못 여는 policy는 cabinet에 넣는 과제를 video로 배우지 못함.

**누리랩 연구와의 연결**

- 미래 장면을 생성하지 않고 world model의 예측 지식만 feature로 쓰는 설계임. world model 기반 VLA를 실시간 control에 쓸 때, 그리고 test-time에 미래 imagination이 꼭 필요한지 따질 때 직접 비교 대상임.
- action label 없는 video, 다른 embodiment video로 새 과제를 배우는 실험은 demonstration 수집 비용을 줄이는 manipulation 연구의 baseline으로 쓸 수 있음.

*대표 그림: 실제 로봇 평가 과제 6개의 장면 사진임. 정밀 조작(볼트 담기, 펜 뚜껑 열기), 변형 물체(모자 걸기, 셔츠 접기), 물체 놓기(링 끼우기, 드라이버 통에 넣기)로 묶었고, 측정 결과는 담기지 않음.*

*영상: [DROID 데이터로만 학습한 policy가 과제별 적응 없이 누운 병을 세워 놓는 실제 로봇 시연 영상임.](https://blog-media.assets.alphaxiv.org/videos/01a1a99d-4472-7195-811b-17b84f6851ac/c2441a5e-4c1e-4a4a-815d-262dbf374033) (alphaXiv 요약에서 가져옴)*

---

### 2. AIRoA-0: Long-Horizon, Precise, Cross-Embodiment Manipulation from Handheld Data (82점)

[arXiv](https://arxiv.org/abs/2611.03815) · [PDF](https://arxiv.org/pdf/2611.03815) · [alphaXiv](https://www.alphaxiv.org/abs/2611.03815) (요약 있음) · [프로젝트 페이지](https://a-0.airoa.io)

- **저자**: Yueh-Hua Wu, Kei Ota, Hanlong Li, Hayata Yuasa, Jason Wang, Kengo Ikeuchi, Kensuke Chiyoma, Makoto Sugiura 외 12명
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 82점
- **읽은 원문**: PDF 전문

> 로봇 없이 사람이 손에 든 gripper로 녹화한 16,151시간 데모만으로 양팔 VLA를 학습하고, 데이터에 없던 장소에서 긴 조작 과제를 한 문장 지시로 수행함. Franka 과제 10개 평균 성공률이 78%로, 같은 데모로 post-training한 π0.5의 27%보다 높음.

**무슨 문제인가**

로봇 teleoperation으로 데모를 모으면 데이터 양이 로봇 대수와 로봇 사용 시간에 묶임. UMI(Universal Manipulation Interface)처럼 손에 드는 gripper로 녹화하면 사람 수만큼 데이터가 늘지만, 데이터에는 로봇이 실패하거나 회복하는 장면이 없음. 정책은 손목 카메라 두 대만 보므로 작업 공간 전체를 못 봄. 손목 카메라 화면이 과제의 서로 다른 단계에서 거의 같게 보일 수 있어, 화면만으로는 지금 몇 번째 단계인지 알기 어려움. 녹화 장소와 배치 장소가 늘 달라서, 긴 양팔 과제를 처음 보는 장소에서 해내는 것이 이 방식의 실제 조건임.

**어떻게 푸나**

AIRoA-0(A-0)은 π0.5 구조(SigLIP 이미지 encoder, Gemma 2B, flow matching action expert)를 공개 가중치에서 시작함. 데이터는 손목 카메라가 달린 자체 gripper YUBI로만 녹화하고, 같은 gripper를 로봇 끝단에 달아 씀. 입력은 양 손목 영상 두 장, 지시문, gripper 상태이고 출력은 action chunk임. 각 action은 관측 시점 gripper 자세를 기준으로 한 목표 자세라서 로봇 base나 관절에 기대지 않음. pre-training에서는 visual evidence budget(지시문에 맞춰 이미지 token마다 남길 비율을 학습하는 gate)과 subtask 문장 예측 보조 loss를 더함. post-training에서는 지금 과제가 어느 stage(연속된 subtask 묶음)인지 분류하는 head를 붙이고, 예측한 stage를 문장으로 action expert에 넣음. 추론 때는 예측한 stage 확률을 EMA(지수 이동 평균)로 평활해, 한 번의 오분류로 stage가 바뀌지 않게 함. 최근 gripper 상태 10개를 token 4개로 줄인 proprioceptive memory도 더함. 추론 때는 noise 수준이 다른 chunk 2개를 buffer에 두고 새 관측마다 함께 denoise하는 streaming decoding을 씀. 새로 들어온 chunk는 noise 수준 1에서 0.1까지 크게 denoise되고, 실행 직전 chunk는 0.1에서 0까지 작은 보정만 받음(non-uniform schedule).

**결과**

- 학습 데이터를 녹화하지 않은 장소의 양팔 Franka에서 과제 10개(수건 접기, 부품 분류, 로봇청소기 패드 교체 등)를 과제당 15회 평가함. 부분 점수를 준 평균 성공률이 A-0은 78%, π0.5는 27%, XR-1은 23%, GR00T N1.7은 16%, MolmoAct2는 14%임.
- 비교 모델 4개는 action horizon, 주기, update 수를 바꿔 과제마다 최고 결과를 보고했고, A-0은 모든 과제에 recipe 하나만 씀. 과제 10개 모두에서 A-0이 가장 높음. A-0 성공률이 가장 낮은 과제는 이어폰(Earbuds) 과제로, A-0 30%, 비교 모델 최고 18%임.
- pre-training 데이터를 6.25%에서 100%로 늘린 5개 모델을 같은 16개 과제 묶음에 post-training함. held-out action loss가 데이터 양에 대해 power law를 따름(R² 0.98). 데이터가 두 배가 될 때마다 loss가 약 2.4% 내림.
- 같은 가중치를 재학습 없이 TX-G2, OpenArm, UR 팔에서 돌려 과제 2~4개를 시연함. 이 로봇들의 성공률 수치는 본문에서 확인 불가함.

**한계**

visual budget, stage head, memory, non-uniform decoding 각각의 기여를 떼어 본 성공률 ablation이 없어 78%가 어느 구성 요소에서 왔는지 알 수 없음. 장면 변화 대응과 다른 로봇 실행은 정량 평가 없이 시연 사례로만 보임. 새 과제마다 그 과제의 손 데모 3~26시간과 post-training이 필요하고, 같은 YUBI gripper와 손목 카메라를 단 로봇에만 적용됨.

**누리랩 연구와의 연결**

- stage를 분류해 문장으로 action expert에 넣고 EMA로 평활하는 구조는 long-horizon manipulation에서 진행 상태를 추적하는 robot memory 설계의 비교 대상이 됨.
- 공개될 16,151시간 손 데모와 pre-trained 가중치는 VLA pre-training 실험의 출발점으로 쓸 수 있음. 실패 장면이 없는 데이터라 failure detection/recovery 연구에는 별도 데이터가 필요함.

*대표 그림: 흰 작업대 위에서 양팔 Franka 로봇이 빨간 손끝의 gripper 두 개로 베이지색 수건 한쪽 끝을 함께 잡아 접는 장면임. 손목 카메라 마운트가 달린 gripper가 보이며, 측정 결과가 아닌 과제 수행 사진임.*

---

### 3. FloMo: 3D Scene Flow as a World Action Model Intermediate for Learning from Human Video (79점)

[arXiv](https://arxiv.org/abs/2611.05062) · [PDF](https://arxiv.org/pdf/2611.05062) · [alphaXiv](https://www.alphaxiv.org/abs/2611.05062) (요약 있음) · [프로젝트 페이지](https://flomo-wam.github.io)

- **저자**: Jeremy Collins, Namra Patel, Ayush Agarwal, Shitij Govil, Animesh Garg
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 80점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 10쪽
- **읽은 원문**: PDF 전문

> World action model이 미래 영상 대신 3D scene flow(장면 점들의 3D 이동량)와 action을 함께 예측하게 바꿔서, 사람 영상에서 배운 움직임을 로봇으로 더 잘 옮김. 처음 보는 실로봇 과제 3종의 평균 성공률이 영상을 예측하는 같은 구조의 7%에서 60%로 오름.

**무슨 문제인가**

Action label이 붙은 로봇 demonstration은 모으기 비싸고, action이 없는 사람 영상은 많음. 그래서 영상 생성 모델을 backbone으로 쓰고 미래 영상과 action을 함께 예측하는 world action model(WAM)이 쓰임. 그런데 미래 영상에는 질감, 조명, 배경처럼 action을 정하는 데 필요 없는 정보가 많음. 모델 용량이 이런 외관 예측에 쓰이고, 외관이 바뀌는 새 물체나 새 과제에서 일반화가 약해질 수 있음.

**어떻게 푸나**

FloMo는 이미지 한 장과 언어 지시를 입력으로 받아, 앞으로 16 step 동안의 3D scene flow와 action chunk를 출력함. Scene flow는 SpatialTrackerV2(기성 3D point tracker)로 첫 frame의 64×64 격자 점 4096개를 따라가서 미리 뽑아 둠. 점 좌표는 첫 frame의 카메라 좌표계로 옮기고, 첫 frame 대비 누적 3D 변위를 target으로 씀. 이 변위 (ΔX, ΔY, ΔZ)를 RGB 값으로 바꿔 영상처럼 만든 뒤, 고정된 Wan 2.2 VAE로 encoding함. 그래서 새 tokenizer 없이 영상 latent와 같은 형식의 motion token을 얻음. Wan 2.2 5B DiT에 LoRA(학습 파라미터 약 161M)를 붙여 motion token과 action token을 flow matching으로 함께 denoise함. 학습은 두 단계임. Mid-training에서는 사람 영상(EgoVerse 약 81시간 등)은 scene flow loss만, 로봇 데이터는 scene flow와 action loss를 받음. Fine-tuning에서는 사람 영상을 빼고 로봇 데이터만 씀.

**결과**

- 같은 구조와 학습 절차에서 예측 target만 바꿈: motion+action(FloMo), video+action(VA), video+motion+action(VMA). 양팔 YAM 로봇 플랫폼의 학습 분포 안 과제 3개(과제당 15회) 평균 성공률이 FloMo 91%, VMA 51%, VA 40%임. 좁은 틈으로 뚜껑을 여는 Toolbox에서는 FloMo 87%, VMA와 VA 모두 13%임.
- 로봇 데이터에 없던 동작·과제·물체 3종(Close Cabinet, Pull String, Highlighter, 과제당 10회)에서 FloMo는 30회 중 18회 성공(60%)함. 2D point track을 중간 표현으로 쓰는 AMPLIFY와 영상을 함께 예측하는 DreamZero는 각각 20%임. 영상을 예측하는 같은 구조의 VA와 VMA는 각각 30회 중 2회(7%)임. Pull String에서 FloMo는 7/10, 다른 방법은 모두 1/10 이하임.
- 사람 영상을 빼고 학습하면 같은 3종 평균 성공률이 60%에서 7%로 내림. 이 대조군은 과제당 5회(총 15회)만 평가함.
- RoboTwin(시뮬레이션 양팔 조작 benchmark) 5개 과제를 과제당 demonstration 50개로 학습하고 100회씩 평가함. 평균 성공률이 FloMo 63.6%, π0.5 44.8%, FAST-WAM(영상 기반 WAM) 41.0%, Diffusion Policy 19.2%임.

**한계**

실로봇 평가는 YAM 한 종류에서 과제 6개뿐이고 과제당 10~15회라 차이의 통계적 신뢰도가 낮음. 영상 target이 성능을 낮추는 이유가 외관에 대한 민감성이라는 설명은 가설이고 따로 분리해 검증하지 않음. Scene flow 추출은 30fps 영상 1시간당 약 72 GPU-hour가 들고, 예측한 motion과 action이 서로 맞도록 묶는 제약이 없어 둘이 어긋날 수 있음. 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- World model의 예측 target을 영상이 아닌 3D 변위장으로 바꾼 설계라서, 누리랩의 VLA·world model 연구에서 예측 target을 정할 때 바로 비교 대상이 됨. 같은 구조에서 target만 바꾼 ablation 방식도 그대로 가져다 쓸 수 있음.
- 예측한 scene flow와 실제 실행 결과의 차이를 failure detection 신호로 쓰는 방향, 그리고 motion과 action의 불일치를 test-time에 줄이는 방향으로 이어질 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 왼쪽은 텍스트·이미지 조건을 받은 Wan 2.2 5B DiT가 action과 3D scene flow token을 함께 denoise하는 구조임. 오른쪽은 반죽을 미는 사람 영상에서 3D scene flow를 뽑아 (ΔX, ΔY, ΔZ)를 RGB로 바꾸는 과정임.*

*영상: [로봇 데이터에 없던 Pull String 과제에서 "장난감에 매달린 줄을 당겨라"라는 지시로 FloMo가 성공한 실로봇 rollout 영상임.](https://blog-media.assets.alphaxiv.org/videos/01a1a96d-23e5-736c-a782-db8aa09de396/34dfd9a4-d15e-4c79-946e-3be55b44a7f3) (alphaXiv 요약에서 가져옴)*

---

### 4. PrimeSim: A Generalist World Model Simulator from Large-Scale Cross-Embodiment Demonstrations (78점)

[arXiv](https://arxiv.org/abs/2611.04870) · [PDF](https://arxiv.org/pdf/2611.04870) · [alphaXiv](https://www.alphaxiv.org/abs/2611.04870) (요약 있음) · [프로젝트 페이지](https://primebottech.github.io/PrimeSim-website)

- **저자**: Travis Davies, Wentao Ma, Lihao Guo, Tengfei Ma, Xiaowen Chang, Jiafeng Xu, Shilong Wang, Yiqi Deng 외 5명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> video generator를 22개 로봇 플랫폼의 demonstration 30,110시간으로 추가 학습해, action을 넣으면 카메라 3개 시점의 미래 영상을 이어 만드는 autoregressive world model simulator PrimeSim을 만듦. 4-step 샘플링으로 A100 한 장에서 초당 10.1 frame을 만들고 최대 105초 rollout을 유지함.

**무슨 문제인가**

world model을 policy 평가와 학습용 simulator로 쓰려면 그럴듯한 영상을 만드는 것으로는 부족함. 명령한 action대로 로봇이 움직여야 하고, 여러 카메라 시점이 같은 장면을 보여야 하고, 학습 window보다 긴 rollout에서도 장면이 유지돼야 함. 기존 video generator는 고정 길이의 실제 영상을 context로 학습하므로, 자기가 만든 영상을 다시 조건으로 쓰면 오류가 쌓임. 또 chunk마다 50 step씩 denoising하면 반복 rollout에 쓰기에 느림.

**어떻게 푸나**

PrimeSim은 Wan2.2-TI2V-5B(5B 파라미터 video generator)에서 시작해 midtraining과 posttraining 두 단계로 학습함. midtraining에서는 모든 로봇의 action을 양손 end-effector pose, 머리·허리·몸통 관절각, gripper 개폐, 바퀴 속도로 된 31차원 벡터로 바꾸고 없는 칸은 0으로 둠. action은 window 첫 frame 기준의 상대값으로 표현함. 각 action token은 attention mask로 자기 frame에만 연결되고, 별도 adapter가 같은 action을 frame feature에 직접 더함. 30개 transformer block 중 3개마다 1개만 세 시점 전체를 보고 나머지는 시점 안에서만 attention하며, 시점마다 camera token을 붙임. posttraining은 4단계임. 먼저 chunk 단위 causal 생성으로 바꾸고, 50-step 샘플링을 4-step으로 distillation함. 이어서 자기가 만든 history로 rollout하며 bidirectional 모델을 teacher로 DMD(distribution matching distillation) 학습함. 끝으로 rollout 길이를 episode 전체로 늘림. 마지막 단계의 KV cache는 첫 관측 3칸, 드문드문 뽑은 장기 history 9칸, 최근 9칸으로 된 총 21칸 memory임. 입력은 첫 관측의 3시점 영상, action 궤적, 언어 지시이고 출력은 3시점 미래 영상임.

**결과**

- WorldSimProbe(명령한 action대로 로봇이 움직이고 장면이 실제 움직임에 반응하는지 보는 진단 suite 5개)에서 공개 action-conditioned world model 5개와 비교함. 5개 suite 중 4개에서 1위임. 가장 강한 경쟁 모델보다 global trajectory coverage는 10.0%, 행동 출처별 차이 보존은 41.8%, interaction dynamics는 48.4% 높음. 원문은 이 값이 상대 비율인지 점수 차인지 밝히지 않음. 작고 큰 action 섭동에 대한 반응을 보는 local action calibration에서는 다른 모델보다 낮음.
- EWMBench(embodied world model 생성 영상 평가 benchmark) overall 점수가 6.09로 GE-Sim 두 변형의 5.82, 5.79보다 높음. 8개 항목 중 5개에서 1위임.
- LIBERO(시뮬레이션 조작 과제 모음)에서 PrimeSim 안에서 잰 policy 성공률이 물리 시뮬레이터 성공률과 r=0.99로 맞음. 저자는 PrimeSim 안에서 GRPO(group relative policy optimization, 같은 상태에서 뽑은 rollout 묶음 안의 상대 reward로 갱신하는 RL)로 policy를 개선했다고 주장함. 비교한 policy 수와 학습 전후 성공률은 제공된 본문 텍스트에서 확인 불가함.
- 학습에 없던 플랫폼에 그 플랫폼 데이터로 100~200 gradient step만 적응시켜 생성이 가능해짐. 같은 조건에서 midtraining 없는 pretrained backbone은 적응하지 못함.

**한계**

policy 평가와 개선 근거는 LIBERO 물리 시뮬레이터와의 비교이고, 실로봇 policy를 PrimeSim으로 개선한 결과는 제공된 본문에서 확인되지 않음. 새 플랫폼은 100~200 step의 추가 학습이 필요해 zero-shot 적응은 아님. dexterous hand와 다리 보행 데이터는 학습에서 제외해 이런 embodiment는 다루지 않으며, 세밀한 action 반응(local calibration)은 다른 모델보다 낮음.

**누리랩 연구와의 연결**

- 가중치와 학습·추론 코드를 공개한다고 밝혔지만 코드 저장소 주소는 본문에 없음. 공개되면 world model 기반 policy 평가나 test-time planning에서 imagined rollout으로 후보 action을 비교하는 실험의 baseline simulator로 쓸 수 있음.
- 첫 관측, 장기 history, 최근 history로 나눈 KV cache memory는 robot memory 연구와 이어짐. 같은 21칸 예산에서 memory 구성을 바꾸는 비교 실험을 우리 과제에 옮겨 볼 수 있음.

*대표 그림: 측정 결과가 아니라 데이터, 학습 구조, 기능을 요약한 개요 그림임. (a)는 humanoid 16.5K시간, dual-arm 5.5K시간, UMI 4.1K시간, single-arm 4.0K시간으로 된 약 30.1K시간 학습 데이터를 보여 줌. (b)는 언어 지시, 통합 action, 3시점 관측을 받아 KV cache memory와 4-step denoising으로 chunk를 이어 만드는 구조임. (c)는 생성 영상과 시뮬레이터 정답 비교, 새 embodiment few-shot 적응, world model 대 시뮬레이터 성공률 산점도를 담음.*

*영상: [하나의 action-conditioned rollout을 머리 카메라와 양손 카메라 3개 시점으로 동시에 보여 주는 저자 프로젝트 페이지 영상임.](https://blog-media.assets.alphaxiv.org/videos/01a1a4a6-4afb-7cb4-bfcd-307909f51093/5a40834f-9e1f-456c-b195-a4d34c1b4118) (alphaXiv 요약에서 가져옴)*

---

### 5. Say the Same, Act Differently: Diagnosing and Steering Text-Action Divergence in Reasoning VLAs (76점)

[arXiv](https://arxiv.org/abs/2611.04166) · [PDF](https://arxiv.org/pdf/2611.04166) · [alphaXiv](https://www.alphaxiv.org/abs/2611.04166) (요약 있음)

- **저자**: Zihao Feng, Qingzhao Zhang, Chunyu Xia, Bo Yu, Z. Morley Mao, Ramesh Govindan
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 68점
- **학회**: NeurIPS 2026 채택 · 근거: comments에 "Accepted to NeurIPS 2026. 23 pages, 3 figures, 8 tables"
- **읽은 원문**: PDF 전문

> reasoning VLA의 rationale은 한 글자도 바꾸지 않고 행동만 바꾸는 이미지 교란이 가능함을 보이고, 그 원인을 hidden state의 기하로 설명함. 주행 VLA Alpamayo의 장애물 주석 장면 154개 중 52.6%에서 rationale이 그대로인 채 새 충돌 경로가 만들어지고, text 보존 항만 넣은 일반 gradient 공격도 48.7%로 비슷함.

**무슨 문제인가**

reasoning VLA는 행동과 함께 자연어 rationale을 내므로, 감독자가 이 글을 읽고 위험한 행동을 미리 잡아낼 수 있다는 기대가 있음. 기존 VLA reasoning 공격(TRAP 등)은 rationale 자체를 바꾸므로 글을 읽는 monitor에 흔적이 남음. rationale monitor로 안전을 보증하려면 행동이 위험하게 바뀔 때 글도 반드시 바뀌어야 함. 이 반대 방향, 즉 글은 그대로 두고 행동만 바꿀 수 있는지는 확인된 적이 없었음.

**어떻게 푸나**

저자들은 글과 행동이 같은 hidden state를 읽는다는 점에 주목함. 글은 이산적인 readout이라 서로 다른 hidden state가 같은 문장을 낼 수 있음. TNAS(text-neutral action-subspace) 진단은 먼저 action 출력의 Jacobian으로 행동이 가장 민감한 hidden state 방향을 구함. 다음으로 clean rationale의 NLL과 logit margin 감소를 두 text loss로 정하고, 두 loss의 gradient가 이루는 2차원 공간을 구함. 행동 방향에서 이 공간 성분을 빼고 정규화한 것이 TNAS 방향이며, 1차 근사에서 두 text loss를 바꾸지 않음. 공격은 이미지에 대한 white-box PGD(projected gradient descent: 교란 크기를 제한한 gradient 공격)임. 그 목적함수에 행동 변화, text 보존 penalty, hidden state 변화와 TNAS 방향의 cosine 정렬 항을 함께 넣음. 실험 모델은 주행용 Alpamayo-1.5와 조작용 InstructVLA임.

**결과**

- hidden state에 같은 크기의 교란을 넣었을 때 Alpamayo(64개 waypoint, 6.4초 경로)의 평균 경로 변위는 TNAS 방향 0.142m, 두 text gradient 방향 0.00297m와 0.00323m임. 반대로 teacher-forced KL(clean과 교란 시 다음 token 분포의 차이)은 text gradient 방향이 269배에서 277배 큼.
- Alpamayo 전체 이미지 공격에서 rationale이 글자 그대로 유지된 비율은 TNAS 유도 시 89.5%, text 보존 PGD 83.0%임. teacher-forced KL은 text 보존 PGD의 0.326에서 TNAS 유도의 0.103으로 68.4% 내림. silent collision(새 충돌이 생기고 rationale은 동일) 비율은 52.6% 대 48.7%로 비슷한 수준임.
- 행동 변화만 노리는 PGD는 rationale을 9.5%만 유지해 silent collision이 4.55%에 그침. 전방 카메라 두 대에만, visual token의 13.1%를 덮는 patch로 공격을 제한해도 silent collision이 31.8%에서 35.1% 사이로 나옴.
- 조작 모델 InstructVLA(Bridge 분포 예시 200개)에서 응답 문장 유지율은 TNAS 유도 85.0%, text 보존 PGD 77.5%임. 이때 16단계 7-DoF action chunk의 정규화 변위는 1.73으로 text 보존 PGD의 1.97보다 약간 작음.

**한계**

모든 공격은 전처리된 이미지 tensor에 넣는 digital white-box 교란이며 실제 물리 patch는 배치하지 않음. 충돌은 기록된 주변 차량과 경로를 겹쳐 보는 open-loop 판정이고, 조작 쪽은 action 변위만 쟀으며 실로봇 실행이나 과제 실패는 보이지 않음. 방어 방법은 시험하지 않았고, 공격 코드와 교란 tensor는 공개하지 않는다고 밝힘.

**누리랩 연구와의 연결**

- VLA의 rationale을 failure detection 신호로 쓰려는 연구에 직접적인 반례임. 글 기반 monitor와 별도로 action channel을 검사하는 detector를 설계할 근거가 됨.
- TNAS처럼 text gradient를 빼낸 hidden state 방향은 reasoning과 action의 정합성을 재는 진단 도구로 쓸 수 있음. reasoning VLA의 faithfulness 평가나 counterfactual 분석에 바로 적용해 볼 수 있음.

*대표 그림: 측정 결과가 아니라 문제 상황을 그린 개념도임. 위는 clean 입력에서 rationale "Stop to keep distance to the lead vehicle"과 정지 행동이 일치하는 경우임. 아래는 교란된 입력에서 같은 rationale이 나오지만 행동이 "Keep going"으로 바뀌어, rationale만 보는 monitor가 차이를 못 보는 경우임.*

---

### 6. Should the Action Expert Train the VLM? Action-Token Supervision and Gradient Routing in Mixture-of-Transformer VLAs (74점)

[arXiv](https://arxiv.org/abs/2611.05249) · [PDF](https://arxiv.org/pdf/2611.05249) · [alphaXiv](https://www.alphaxiv.org/abs/2611.05249) (요약 있음) · [프로젝트 페이지](https://mot-vla-gradient-routing.github.io/)

- **저자**: Asher James Hancock, Boyi Li, Yuxiao Chen, Shuhan Tan, Wenhao Ding, Thomas Tian, Yan Wang, Boris Ivanovic 외 1명
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 70점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> VLM과 flow-matching action expert를 묶은 VLA에서 expert의 loss gradient를 VLM까지 흘릴지(coupling) 막을지(insulation)를, 이산 action token 감독 유무와 교차해 통제 비교함. action token 없이 함께 학습하면 coupling이 closed-loop 주행 route progress를 0.425에서 0.601로 올림.

**무슨 문제인가**

π0.5, MolmoAct2, Alpamayo-R1 같은 VLA는 action expert의 gradient가 VLM으로 들어가지 않게 막는 Knowledge Insulation을 씀. 근거는 새로 붙인 expert의 gradient가 VLM의 사전학습 능력을 해친다는 것임. 그런데 이 recipe들은 VLM에 FAST 같은 이산 action token 예측도 같이 감독함. 그래서 insulation이 잘 되는 이유가 gradient 차단 자체인지, action token이 VLM에 행동 정보를 대신 가르쳐서인지 가려지지 않았음.

**어떻게 푸나**

VLM이 이미지·언어·과거 궤적을 읽고, expert는 VLM 층별 K/V(key-value) 표현을 조건으로 연속 action을 생성하는 구조를 고정함. 주행 모델은 Qwen3-VL-2B와 같은 폭의 flow-matching expert이고, 출력은 가속도와 곡률 열을 적분한 궤적임. 두 스위치를 독립으로 바꿈: VLM이 같은 미래 궤적의 이산 action token을 cross-entropy로 예측하는지, flow loss gradient가 K/V 경로로 VLM에 가는지임. insulation은 stop-gradient로 구현해 forward 계산은 같고 backward만 다름. 평가 때 action token은 decode하지 않고 expert의 연속 출력만 씀. 2x2 조건을 동시 학습, VLM 먼저 100k step, expert 먼저 100k step의 세 schedule에서 총 300k step으로 맞춤. 조작에서는 π0.5 재구현과 MolmoAct2로 동시 학습만 반복함.

**결과**

- 주행 open-loop 평가(Physical AI AV 데이터셋 Public Golden 1,434개, OOD 273개)의 첫 샘플 ADE(예측 궤적과 실제 궤적의 평균 위치 오차)를 잼. 동시 학습에서 action token이 없으면 Public Golden ADE가 insulation 3.21m에서 coupling 2.36m로 내림. action token이 있으면 insulation 2.09m, coupling 2.21m로 insulation의 오차가 조금 더 작음.
- AlpaSim(closed-loop 주행 시뮬레이터) 827개 장면, 장면당 rollout 5회의 평균 route progress를 잼. 동시 학습에서 coupling이 token 없이 0.425에서 0.601로, token 있을 때 0.600에서 0.703으로 오름. VLM 먼저 학습한 경우 token이 있으면 0.648 대 0.646으로 차이가 없음.
- PolaRiS(시뮬레이션 조작 평가) 과제 3개에서 조건·과제당 50회 rollout의 정규화 progress(채점 항목 달성 비율, 완수율 아님)를 잼. insulation에서 coupling으로 바꾸면 π0.5 재구현은 FAST가 없을 때 10.3%에서 32.9%로, 있을 때 19.5%에서 30.7%로 오름. MolmoAct2는 각각 14.5%에서 36.5%, 22.0%에서 24.3%임.
- 안전 지표는 coupling 쪽이 항상 낫지 않음. expert 먼저 학습하고 token이 있을 때 at-fault 충돌률이 insulation 0.061, coupling 0.097임.

**한계**

조건마다 학습을 한 번만 돌려 seed 변동은 재지 않았고, 신뢰구간은 평가 clip에 대한 bootstrap뿐임. closed-loop 평가는 주행·조작 모두 시뮬레이션이고 실로봇 실험은 없음. insulation이 VLM의 일반 능력을 지키는지는 주행 rationale 판정(Lingo-Judge)으로만 봤고, 차이가 나는 기전은 밝히지 않음.

**누리랩 연구와의 연결**

- MoT(Mixture-of-Transformers, VLM과 action expert가 층별 attention 표현을 공유하는 구조) VLA를 학습할 때 stop-gradient와 FAST 감독을 따로 끄고 켜는 ablation 설계를 그대로 가져다 쓸 수 있음. open-loop 오차와 closed-loop 성능의 결론이 갈린다는 결과는 VLA 평가 지표를 고를 때 근거가 됨.
- 동시 학습 + coupling이 VLM 먼저 학습하는 기존 recipe보다 나은 경우가 있다는 결과는, 우리 VLA fine-tuning 기본 설정을 다시 점검할 이유가 됨.

*대표 그림: 측정 결과와 방법 구조를 함께 담은 개요 그림임. 왼쪽은 VLM이 이산 action token의 cross-entropy(CE) gradient를, action expert가 K/V cache를 통해 flow loss gradient(Backprop On 스위치)를 받는 구조임. 오른쪽은 학습 step별 평가 오차 곡선으로, action token이 켜지면 Knowledge Insulation과 coupled 학습의 차이가 작고 꺼지면 커지는 모습과 주행·조작 장면 예시를 보여 줌.*

---

### 7. RAFT: Reasoning-Aligned Fine-Tuning Improves Robustness of VLA Post-Training (72점)

[arXiv](https://arxiv.org/abs/2611.04368) · [PDF](https://arxiv.org/pdf/2611.04368) · [alphaXiv](https://www.alphaxiv.org/abs/2611.04368) (요약 있음) · [프로젝트 페이지](https://princeton-prism.github.io/RAFT) · [코드](https://github.com/princeton-prism/RAFT)

- **저자**: Shresth Grover, Andrey Kolobov, Dhruv Shah
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 70점
- **학회**: CoRL 양식 (추정) · 근거: 1단 구성, 초록 아래 'Keywords:' 줄
- **읽은 원문**: PDF 전문

> VLA를 적은 demonstration으로 fine-tuning하기 전에, 과제 관련 물체와 움직임을 말로 예측하는 LoRA adapter를 먼저 학습하고 고정하는 2단계 post-training을 제안함. 실제 DROID 로봇의 분포 밖 조건 성공률이 plain fine-tuning의 27.9%에서 75.0%로 오름.

**무슨 문제인가**

generalist VLA를 실제 과제에 쓰려면 보통 그 과제의 demonstration으로 post-training을 함. demonstration은 모으기 비싸서 좁은 환경 몇 곳에서 적게 모으는 경우가 많음. 이렇게 fine-tuning하면 학습 환경에서는 성공률이 오르지만, 조명·배경·물체·지시문이 바뀌면 성공률이 내려감. 기존 대응은 RETAIN처럼 pretrained 가중치와 fine-tuned 가중치를 섞거나, DeLock처럼 vision encoder 가중치 변화를 regularization으로 묶는 방식이었음.

**어떻게 푸나**

RAFT(Reasoning-Aligned Fine-Tuning)는 action 학습 전에 reasoning 학습 단계를 따로 둠. Stage I에서는 VLM annotator(Gemini 3.1 Pro)가 demonstration 관측과 지시문을 보고 reasoning 정답을 만듦. 정답은 물체 bounding box, keypoint, gripper 궤적(trace), 공간 관계 설명, VQA 답 같은 text token 열임. policy는 관측과 reasoning prompt를 입력받아 이 token 열을 cross-entropy로 예측하고, 이때 language model과 vision encoder에 붙인 LoRA만 갱신됨. Stage II에서는 이 LoRA를 고정하고 language model, action expert, projection layer를 action demonstration으로 학습함. 출력은 policy의 원래 action chunk이며 SigLIP vision 가중치는 두 단계 내내 고정됨. 그래서 action gradient가 reasoning adapter를 직접 바꾸지 못함.

**결과**

- 실제 DROID 로봇에서 단팔 pick-and-place를 평가함. MolmoBot(대규모 시뮬레이션 데이터로 학습한 조작 policy)을 demonstration 50개로 post-training함. 분포 밖 조건 68회 성공률이 RAFT 75.0%, plain fine-tuning 27.9%임. 조건별로는 새 물체 색 83% 대 33%, distractor 추가 75% 대 25%, 탁자면 변경 65% 대 25%이고, 학습 환경에서는 63% 대 60%로 비슷함.
- 실제 양팔 YAM 로봇에서 상자를 열고 물체를 넣는 2단계 과제(π0.5, demonstration 100개)의 전체 완료율이 RAFT 70.0%, 가장 강한 baseline인 DeLock 36%, plain fine-tuning 34.7%, RETAIN 29%임. 학습 환경과 4가지 변화 조건을 합친 값이고 조건당 30회임.
- MolmoSpaces 시뮬레이션 pick-and-place(5개 평가 split, split당 106회)의 평균 성공률이 RAFT 83.21%, plain fine-tuning 79.62%임. reasoning과 action을 1:1로 섞어 한 번에 학습하면 63.21%, Stage II에서 adapter를 계속 학습하면 73.96%로 plain fine-tuning보다 낮음.
- vision encoder만 고정한 plain fine-tuning도 79.62%에 머물러, vision 가중치 고정만으로는 차이가 설명되지 않음. 다만 시뮬레이션 평균 차이는 3.6퍼센트포인트로 작음.

**한계**

어떤 reasoning 형식이 좋은지는 과제마다 달라서, 본 결과도 pick-and-place는 full reasoning, open-drawer는 bounding box처럼 과제별로 고른 형식을 썼음. 실로봇은 과제 하나씩이고 DROID 조건당 20~30회, YAM 조건당 30회로 표본이 작음. attention과 linear probe 분석은 표현이 다르다는 것을 보일 뿐, 그 차이가 성공률 차이의 원인임을 보이지는 않음.

**누리랩 연구와의 연결**

- VLA post-training에서 robustness를 지키는 방법을 가중치 병합이나 regularization이 아니라 학습 순서와 parameter 고정으로 다룬 사례임. 적은 demonstration으로 manipulation VLA를 적응시킬 때 바로 비교 baseline으로 쓸 수 있음.
- Stage I 정답이 bounding box·keypoint·trace 같은 object-centric 표현이라, 어떤 grounding 표현을 adapter에 넣을지 비교하는 embodied spatial reasoning 연구와 이어짐.

*대표 그림: 왼쪽은 plain fine-tuning이 학습 배치에서는 성공하지만 상자 위치·물체 색·distractor·탁자면이 바뀐 실제 로봇 rollout에서 실패하는 예시이고, 오른쪽은 같은 조건에서 RAFT가 성공하는 예시임. 가운데는 2단계 구조 도식과 실로봇 성공률 막대그래프(YAM 34.7% 대 70.0%, DROID OOD 27.9% 대 75.0%)임.*

---

### 8. Human-to-Robot Transfer via Bridging Representation and Action Space in VLAs (72점)

[arXiv](https://arxiv.org/abs/2611.04391) · [PDF](https://arxiv.org/pdf/2611.04391) · [alphaXiv](https://www.alphaxiv.org/abs/2611.04391) (요약 있음) · [프로젝트 페이지](https://junhyeong-park.me/h2rb/)

- **저자**: Junhyeong Park, Wook Jung, Taeyoung Kim, Huiwon Jang, Jinwoo Shin
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 70점
- **학회**: CoRL 2026 채택 · 근거: comments에 "Accepted for Oral Presentation at the CoRL 2026 Workshop on Scaling H2R. Project page: https://junhyeong-park.me/h2rb/"
- **읽은 원문**: PDF 전문

> 로봇 데이터로 사전학습한 VLA에 사람 손 시연만으로 새 물체와 새 동작을 가르치기 위해, 관측 쪽은 손 기하로 맞추고 행동 쪽은 공유 latent와 분리된 decoder로 맞춤. 사람 시연으로만 보여 준 에어프라이어 Open/Close 과제의 진행 점수가 기존 co-training의 0.0에서 62.7로 오름.

**무슨 문제인가**

VLA를 새 로봇과 환경에 맞추려면 그 로봇으로 teleoperation 시연을 모아야 해서 비용이 큼. 사람 손 시연은 카메라만으로 쉽게 모이지만, 사람과 로봇은 보이는 모습과 움직이는 방식이 모두 다름. 기존 방법은 frame 변화로 추정한 latent action이나 복원한 손목·손 동작으로 행동 공간만 맞춤. 이 경우 관측의 차이는 그대로 남고, 사람과 로봇의 움직임 속도나 궤적 모양 차이도 하나의 action mapping에 억지로 묶임.

**어떻게 푸나**

H2RB(Human-To-Robot Bridge)는 짝이 맞지 않는 사람 시연과 로봇 시연을 함께 써서 사전학습 VLA(RLDX-1-IMG)를 fine-tuning함. 먼저 사람 영상에서 HaWoR(1인칭 영상에서 손 동작을 world 좌표로 복원하는 기존 방법) 기반 파이프라인으로 손목 움직임과 손가락 관절을 복원함. 이를 로봇 손에 retarget해 로봇과 같은 손목 위치·회전·손 관절 형식으로 바꿈. 다음으로 16 step action chunk를 받는 공유 encoder 하나와 사람용·로봇용 decoder 두 개로 된 VAE tokenizer를 학습함. 이때 chunk 안 같은 상대 위치의 사람 latent 평균과 로봇 latent 평균을 가깝게 당기는 regularization을 더함. 관측 쪽에서는 VLM 출력 token에 residual adapter를 붙이고, 현재 손목 자세와 손목 기준 손가락 끝 5개 위치를 맞히도록 학습함(hand geometry-anchored alignment). 각 관측이 자기 손 기하를 정답으로 가지므로 사람과 로봇 데이터의 짝이 필요 없음. policy는 고정된 tokenizer의 latent를 flow matching으로 예측함. 두 decoder는 모두 로봇이 쓸 수 있는 같은 손목·손 표현을 출력함. 배포 때는 decoder 선택 실험에서 물체 전이 점수가 더 높았던 사람용 decoder를 쓰고, 그 출력을 IK로 팔 관절 명령으로 바꿈.

**결과**

- 평가는 OpenArm 팔과 Inspire 손에서 하고, 점수는 rollout마다 도달한 단계(접근 0.3, 잡기 0.6, 들기·절반 열기 0.8, 완료 1.0)를 평균해 0~100으로 매긴 값임. 성공률이 아님.
- 사람 시연으로만 보여 준 에어프라이어 Open/Close 과제(과제당 15회) 평균 점수가 H2RB 62.7임. 사람·로봇 행동을 같은 손목·손 행동 공간으로 묶는 Ego-Pi 방식 baseline과 일반 co-training은 같은 데이터와 학습량에서 둘 다 0.0임. 완전 성공 비율은 H2RB 30.0%임.
- 사람 시연으로만 보여 준 물체 3개(Box, Ball, Towel)의 pick-and-place 점수는 일반 co-training 8.0, Ego-Pi 방식 27.2, H2RB 51.8임. 학습 때 없던 배치 위치에서도 Ego-Pi 방식 21.3 대비 45.3임.
- 구성 요소를 하나씩 더한 ablation에서 Ego-Pi 방식 행동 공간에 관측 정렬만 넣고 tokenizer가 없으면 물체·동작 전이 점수가 34.7과 0.0임. tokenizer를 넣으면 43.3과 49.7, latent regularization까지 넣으면 51.8과 62.7로 오름.

**한계**

조건마다 policy를 한 번만 학습했고 분산이나 신뢰구간이 없으며, 동작 전이는 에어프라이어 하나의 30회 평가뿐임. 진행 점수 대신 완전 성공만 보면 물체 전이 12.2%, 동작 전이 30.0%로 아직 낮음. 저자는 사람 데이터가 수집 시간을 줄인다고 쓰지만, 수집 시간 절감은 측정하지 않았음.

**누리랩 연구와의 연결**

- 사전학습 VLA에 사람 시연으로 새 manipulation 동작을 넣는 구체적 방법이고, 관측 정렬과 행동 정렬을 따로 ablation한 결과가 있어 human video 기반 VLA 적응 연구의 비교 대상으로 쓸 수 있음.
- 공유 encoder와 embodiment별 decoder로 latent action을 나누는 구조는 dexterous hand를 쓰는 cross-embodiment policy를 설계할 때 그대로 시험해 볼 만함.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 개념도임. 왼쪽의 로봇 시연(간식 옮기기)과 사람 영상(에어프라이어 열기)이 hand-geometry alignment, action expert, 공유 encoder, 사람용 decoder를 거쳐, 오른쪽에서 로봇 손이 상자를 집어 넣고 에어프라이어를 여는 장면으로 이어짐.*

*영상: [프로젝트 페이지의 영상으로, 사람이 에어프라이어를 여는 시연과 OpenArm 로봇이 같은 동작을 하는 장면을 함께 보여 줌.](https://blog-media.assets.alphaxiv.org/videos/01a1a456-adea-73aa-a748-72928bd527d3/1eb90864-6f50-413c-ae0f-575cf6ffc898) (alphaXiv 요약에서 가져옴)*

---

### 9. Compression Forcing: Hierarchical History Tokenization Enables Flexible World Models (72점)

[arXiv](https://arxiv.org/abs/2611.04028) · [PDF](https://arxiv.org/pdf/2611.04028) · [alphaXiv](https://www.alphaxiv.org/abs/2611.04028) (요약 있음)

- **저자**: Siqiao Huang, Partha Kaushik, Michael Chen, Hengkai Pan, Kaiwen Geng, Omar Chehab, Fernando Moreno-Pino, Max Simchowitz
- **분야**: World Model · robotics relevance 7/10 · 1차 스크리닝 68점
- **읽은 원문**: PDF 전문

> world model이 과거 프레임을 압축할 때 움직임 정보를 앞쪽 token에, 정적인 배경을 뒤쪽 token에 두도록 학습하고, 앞쪽 token만 골라 증폭해 다음 프레임을 예측함. RT-1 서랍 열기 과제에서 끝까지 학습한 RT-1 policy의 실제 성공률은 81.5%이고, 이 방법은 64%, 기존 tokenizer ElasticTok은 48%로 예측함.

**무슨 문제인가**

최근 world model은 video generation 모델의 tokenizer와 history conditioning을 그대로 가져다 씀. 이 방식은 프레임마다 같은 양의 token을 쓰고 보기 좋은 화질을 목표로 학습되어, 예측에 필요한 움직임과 쓸모없는 배경을 구분하지 않음. Diffusion Forcing 계열은 과거 프레임에 noise를 섞어 일부만 보게 하는데, 이는 저주파 성분만 남기는 필터에 가까움. 저자들은 world model이라면 공간 주파수가 아니라 예측에 얼마나 중요한지에 따라 과거 정보를 골라야 한다고 주장함.

**어떻게 푸나**

CF(Compression Forcing)는 세 부분으로 이루어짐. 먼저 DAT(Dynamics-Aware Tokenization)가 과거 프레임 묶음을 순서가 정해진 token 열로 압축함. 각 slot token은 앞선 slot만 보도록 causal attention을 쓰므로, 앞부분 m개만 잘라도 그 자체로 쓸 수 있는 표현이 됨. DAT의 diffusion decoder는 두 가지 과제로 학습함: prefix만으로 전체 clip을 복원하는 static reconstruction과, 첫 프레임을 함께 받아 이후 프레임을 예측하는 dynamic prediction임. prefix가 짧을수록 dynamic prediction의 가중치를 크게 주어, 앞쪽 token은 변화를, 뒤쪽 token은 정적인 외형을 담게 함. 다음으로 diffusion transformer backbone이 다음 프레임을 예측하도록 학습되며, 조건으로는 겹치는 window마다 DAT token의 앞부분(길이는 임의)과 action을 받음. 마지막으로 HG-H(Hierarchical History Guidance)는 inference 때 서로 다른 prefix 길이로 얻은 score를 classifier-free guidance처럼 조합해 앞쪽 token의 영향을 원하는 만큼 키움.

**결과**

- Kinetics-600(행동 입력 없는 자연 영상 예측, 16프레임을 보고 8프레임 생성)에서 같은 backbone과 학습량으로 tokenizer만 바꿔 비교함. 비교 tokenizer는 프레임마다 고정된 양으로 압축하는 SD-VAE와, 앞쪽 token이 복원 화질을 우선 담도록 영상을 1D token 열로 압축하는 ElasticTok임. PSNR이 DAT+HG-H 18.83, guidance를 쓴 ElasticTok 18.60, SD-VAE 18.53으로 차이는 작음. FID는 88.13 대 90.74 대 90.57임.
- RT-1(실제 로봇 조작 데이터, 8프레임을 보고 16프레임 생성)에서 FVD가 DAT+HG-H 101.5, ElasticTok+HG-H 105.4, SD-VAE 120.4임. SSIM과 PSNR은 세 방법이 거의 같음(PSNR 20.43, 20.42, 20.47). 기존 world model인 DIAMOND는 FVD 382.4, Dreamer 4는 984.1임.
- CS:GO(1인칭 게임, 4프레임을 보고 12프레임 생성)에서 FVD가 DAT+HG-H 123.0, ElasticTok+HG-H 197.1, DIAMOND-HQ 368.5임. PSNR은 DIAMOND-HQ 18.3이 DAT의 17.24보다 높고, SSIM도 SD-VAE가 가장 높음.
- policy 평가 대용(Real2Sim, 서랍 열기 1개 과제, 정책당 50회 rollout, 성공 여부는 사람이 판정)에서 policy 4개를 평가함. 4개는 RT-1 학습 초기 checkpoint(Begin), 데이터 15%로 학습한 RT-1(15%), 끝까지 학습한 RT-1(Converged), RT-1-X임. 실제 성공률 0, 70.4, 81.5, 51.9%에 대해 CF는 2, 54, 64, 40%를 예측함. ElasticTok은 6, 40, 48, 36%이고, SD-VAE는 RT-1(15%)과 수렴 policy의 순위를 뒤집음.

**한계**

같은 backbone 비교에서 화질 지표 차이는 PSNR 0.2 dB 수준이고, 반복 실행에 따른 분산은 본문에서 확인 불가임. 정적 복원과 동적 예측 가중치 schedule이 각각 얼마나 기여하는지는 본문에서 확인 불가임. 실로봇 실험은 없고, policy 평가도 기록된 RT-1 데이터 기반의 과제 1개이며 CF도 실제 성공률을 일관되게 낮게 예측함.

**누리랩 연구와의 연결**

- 조작 world model에서 과거 관측을 예측 중요도 순으로 압축하는 방법으로, robot memory를 고정 길이 frame buffer 대신 길이를 바꿀 수 있는 token 열로 두는 설계에 참고가 됨.
- world model을 policy 평가 대용으로 쓰는 실험(Real2Sim)을 포함해, world model 기반 test-time planning이나 failure 예측 연구에서 tokenizer 선택이 평가 신뢰도에 주는 영향을 보는 비교 대상이 됨.

*대표 그림: 운동선수가 움직이는 영상 8프레임과, DAT의 slot 16, 32, 128, 254가 이미지 patch에 주는 cross-attention을 겹쳐 그린 그림임. slot 16은 선수의 몸과 팔 근처에 모이고, slot 128과 254는 위쪽 조명이나 배경 띠처럼 선수 밖의 영역으로 퍼짐.*

---

### 10. CANDO: Conservative Action-Noise Directional Optimization for Residual Reinforcement Learning (66점)

[arXiv](https://arxiv.org/abs/2611.04543) · [PDF](https://arxiv.org/pdf/2611.04543) · [alphaXiv](https://www.alphaxiv.org/abs/2611.04543) (요약 있음) · [프로젝트 페이지](https://cando-rl.github.io/)

- **저자**: Zeyu Gao, Chengkai Hou, Chaoyue Li, Zhuangzhe Wu, Jiaming Liu, Yao Mu, Peng Jia, Li Zhang 외 1명
- **분야**: RL · robotics relevance 9/10 · 1차 스크리닝 70점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> 고정된 flow matching policy를 online RL로 고칠 때, 입력 noise 수정을 latent 영역 제한 대신 conservative critic과 gate로 조절하고 행동 보정을 더함. 시뮬레이션 조작 과제 5개 평균 NAUC(학습 곡선 아래 면적)가 76.1로, 가장 강한 기존 방법 DICE의 68.5보다 7.6점 높음.

**무슨 문제인가**

diffusion이나 flow matching으로 demonstration을 배운 generative policy는 online RL로 더 고치기 어려움. 생성 과정 전체를 fine-tuning하면 계산이 많고 불안정하므로, policy를 고정하고 작은 residual만 배우는 방식이 쓰임. residual은 decoding 전 입력 noise를 바꾸는 noise-space 방식(DSRL 등)과 decoding 후 행동을 직접 고치는 action-space 방식(DICE 등)으로 나뉨. noise-space 방식은 tanh 경계나 Gaussian 구면 같은 고정된 latent 영역으로 noise 수정을 제한하는데, latent 거리는 decoding된 행동의 품질과 간접적으로만 이어짐. 그 결과 noise-space 방식은 대부분 과제에서 DICE보다 sample efficiency가 낮고, 두 방식을 단순히 합쳐도 DICE보다 나아지지 않음.

**어떻게 푸나**

CNDO(Conservative Noise Directional Optimization)는 상태와 Gaussian noise를 입력받아 noise에 더할 방향을 출력하는 network를 배움. 원래 noise와 수정된 noise를 각각 고정된 policy에 넣어 두 action chunk를 만들고, critic은 decoding된 action chunk 위에서 가치를 매김. latent 영역 제한을 없애는 대신 두 장치를 둠. 첫째, critic 10개 ensemble의 최솟값을 쓰고, 고정 policy 행동과 replay 행동 어느 쪽에서도 먼 후보 행동의 가치만 낮추는 conservative 항을 더함. 둘째, target critic의 가치 비교를 증류한 이진 gate가 chunk마다 수정된 행동과 원래 행동 중 하나를 실행함. CANDO(Conservative Action-Noise Directional Optimization)는 여기에 원래 행동을 입력받는 action residual을 더해 최종 행동의 Q 값을 두 branch가 함께 최대화함. gate가 noise 수정을 거부해도 action residual은 계속 적용됨.

**결과**

- RoboMimic(Can, Square, Transport)과 ManiSkill(PegInsertionSide, StackCube)의 state 입력·sparse reward 과제 5개에서 seed 3개로 잼. 평균 NAUC(학습 step에 따른 성공률 곡선 아래 면적)는 CANDO 76.1, CNDO 69.5, DICE 68.5임. 평균 최종 성공률은 CANDO 91.4%, DICE 87.3%임. 다만 StackCube 최종 성공률은 CANDO 90.6%로 DICE 94.1%보다 낮음.
- DSRL과 DICE를 단순히 합친 방법은 평균 NAUC 68.0, 최종 성공률 82.6%로 DICE 단독보다 낮음. noise branch가 DICE와 비슷한 수준이 된 뒤에 합쳐야 이득이 생긴다는 저자 주장의 근거임.
- conservative critic을 빼면 CNDO 평균 NAUC가 69.5에서 58.2로 내리고, PegInsertionSide 최종 성공률은 83.1%에서 0.1%로 내림. gate 없이 수정을 항상 실행하면 평균 NAUC가 57.5로 내림.
- 두 팔과 로봇 손을 쓰는 실로봇에서 고정된 위치의 과제 4개를 과제당 20회 평가함. 평균 성공률은 CANDO 87.5%, CNDO 86.25%, DSRL 55.0%, DICE 42.5%, base policy 40.0%임.

**한계**

시뮬레이션은 state 입력 과제 5개와 seed 3개뿐이고, 이미지 입력 policy나 VLA 규모 policy에는 적용하지 않음. 실로봇은 물체 위치를 바꾸지 않은 과제 4개이며, CANDO의 CNDO 대비 이득은 1.25퍼센트포인트로 작음. 두 branch의 능력이 비슷할 때 결합이 유리하다는 주장은 이 실험 범위의 관찰이며, 계산 비용이나 실제 학습 시간은 보고하지 않음.

**누리랩 연구와의 연결**

- 고정된 generative policy를 noise와 행동 두 공간에서 RL로 고치는 방법이라, VLA나 diffusion policy를 실로봇에서 online으로 적응시키는 연구에서 비교 대상으로 쓸 수 있음.
- critic 가치로 수정 실행 여부를 고르는 gate는 base policy 행동으로 되돌아가는 장치라, 실행 전 행동 단위 failure 회피 연구와 이어짐.

*대표 그림: 측정 결과와 방법 구조를 함께 담은 동기 그림임. (a)는 decoding 전에 noise를 바꾸는 DSRL과 decoding 후 행동을 고치는 DICE의 구조를 비교함. (b)(c)는 Transport 학습 곡선에서 DSRL이 DICE보다 낮고, DICE+DSRL은 DICE와 비슷한 수준에 머무름을 보임.*

---

### 11. Physical Diffusion Policy via MPM-Guided 3D Gaussian Simulation (66점)

[arXiv](https://arxiv.org/abs/2611.04493) · [PDF](https://arxiv.org/pdf/2611.04493) · [alphaXiv](https://www.alphaxiv.org/abs/2611.04493) (요약 있음)

- **저자**: Can Wang, Qiyuan Qiao, Lei Liu, Ge Yuan, Xinhui Liu, Dong Xu
- **분야**: Manipulation · robotics relevance 9/10 · 1차 스크리닝 68점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 10쪽
- **읽은 원문**: PDF 전문

> 시연 영상에서 물체의 탄성·소성·점성 parameter를 미분 가능한 물리 시뮬레이션으로 추정하고, 이 값을 재질별 expert로 나뉜 diffusion policy의 조건으로 넣음. 실로봇 pick-and-place에서 탄성 물체 평균 성공률이 DP3의 30.0%에서 57.1%로 오름.

**무슨 문제인가**

Diffusion Policy와 DP3 같은 imitation policy는 물체를 겉모습과 형상으로만 보고 재질은 모름. 겉모습이 비슷해도 물렁한 빵과 단단한 블록은 잡는 방식이 달라야 함. 재질이 다른 물체의 시연을 한 policy로 배우면 서로 맞지 않는 행동이 평균되어 어느 쪽에도 맞지 않는 행동이 나올 수 있음. 기존 system identification은 설계된 상호작용이나 힘 측정이 필요해 일상 물체 여러 개로 늘리기 어려움.

**어떻게 푸나**

먼저 물체 주변을 반구 모양으로 찍은 영상에서 64 frame을 뽑아 feed-forward 3DGS로 Gaussian을 복원함. Gaussian 하나마다 MPM(Material Point Method: 입자와 배경 격자로 변형체를 계산하는 시뮬레이션) 입자를 하나씩 붙여, 시뮬레이션된 움직임이 그대로 렌더링되게 함. 추정 대상은 Young's modulus(E), Poisson's ratio(ν), yield stress(τY), viscosity(η) 4개임. VLM(Qwen3-VL)이 초기값을 주고, 재질 종류별 상하한으로 값을 매 단계 잘라 냄. 고정 시점 조작 영상과의 렌더링 차이, 물체 형상의 Chamfer distance, 그리퍼가 쥔 구간의 입자 위치 제약을 합친 loss로 parameter를 gradient descent로 맞춤. 추정된 parameter는 언어 지시, 고정 카메라·손목 카메라 영상과 함께 policy에 들어감. policy는 탄성·foam·소성·강체 4개 expert가 각각 noise를 예측하고, router가 낸 가중치로 합쳐 행동을 만듦. 네 expert는 먼저 각 재질 라벨의 시연으로 따로 학습하고, 그다음 router와 함께 전체를 fine-tuning함. 배포 때는 시뮬레이션을 돌리지 않고, DINOv2 feature로 미리 추정해 둔 parameter 저장소(physics memory bank)에서 가장 비슷한 물체의 값을 가져옴.

**결과**

- 실로봇 pick-and-place(재질마다 물체 여러 개, 물체당 30회)에서 탄성 물체 평균 성공률이 DP3 30.0%, DP 25.2%에 비해 57.1%임. 강체는 DP3의 49.2%에서 70.0%로 오름. 시뮬레이션(Isaac Lab, 과제당 120회)에서는 소성·강체가 이미 95% 이상이라 차이가 작음.
- 실로봇 ablation에서 네 재질 평균 성공률은 DP 28.9%, DP에 물리 parameter 조건만 넣은 단일 policy 49.4%, 전체 모델 62.5%임. 단일 policy 대비 차이에는 expert 사전학습과 router가 함께 들어 있어 router만의 효과는 따로 보이지 않음.
- 시뮬레이션 물체의 parameter 추정 오차(4개 parameter 평균, E·τY·η는 log-MAE)는 0.565이고, VLM 초기화를 빼면 1.257로 커짐.
- 실로봇에서 물체당 online 최적화는 798.22초, memory bank 검색은 약 415ms 걸림. 두 과제 평균 성공률은 online 최적화 60.7%, memory bank 검색(bank 크기 15) 59.2%로 비슷함.

**한계**

parameter 추정 정확도는 정답이 있는 시뮬레이션 물체로만 쟀고, 실제 물체의 추정값이 맞는지는 확인하지 않음. memory bank 검색은 같은 물체가 저장된 within-domain 조건에서만 평가되어, 처음 보는 물체에 맞는 물리값을 가져오는지는 보이지 않음. expert 사전학습에 재질 라벨이 필요하고, 과제는 pick-and-place와 stacking 두 가지이며 코드 공개 언급이 없음.

**누리랩 연구와의 연결**

- 3DGS를 MPM 입자와 묶어 시연 영상에서 물체 물성을 거꾸로 추정하는 파이프라인임. object-centric 3DGS 표현에 외형 외에 물리 속성을 붙이는 연구에서 비교 대상으로 쓸 수 있음.
- 시뮬레이션에서 parameter 하나씩 오차를 일부러 키우자 성공률이 내려간 sensitivity 실험은, 물성 추정 실패를 manipulation failure의 원인으로 진단하는 failure detection 연구의 출발점이 될 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 위쪽은 다시점 영상에서 3DGS와 MPM 속도장을 거쳐, 미분 가능한 rasterizer로 시연 영상과 비교해 E, ν, τY, η를 학습하는 과정임. 아래 왼쪽은 T5 언어 encoder와 고정·손목 카메라 입력을 router가 MoE diffusion expert에 나누는 policy이고, 아래 오른쪽은 grasp부터 release까지의 경계 조건과 Chamfer distance 형상 정렬 제약임.*

---

### 12. Trusting Imagined Futures: Auditing Imagined Rewards for VLA Post-Training (62점)

[arXiv](https://arxiv.org/abs/2611.04873) · [PDF](https://arxiv.org/pdf/2611.04873) · [alphaXiv](https://www.alphaxiv.org/abs/2611.04873) (요약 있음)

- **저자**: Zicheng Kong, Zhenbo Xu, Haoyan Zhang, Jinghan Yang, Zhenzhen Li, Yiwei Ru, Liuyu Xiang, WanTing Xu 외 2명
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> video world model이 상상한 결과에 reward model이 준 높은 점수를, 실제 실행 결과로 학습한 auditor가 한 번 더 검사해서 VLA behavior cloning에 쓸 궤적을 고름. LIBERO 4개 suite 평균 성공률이 기존 궤적으로만 학습할 때의 73.25%에서 76.25%로 오름.

**무슨 문제인가**

VLA를 imitation learning으로 post-training하면 정책은 supervision 궤적의 좋고 나쁜 점을 그대로 따라 배움. 그래서 후보 행동을 world model로 상상해 보고 reward model 점수가 높은 궤적으로 기존 supervision을 바꾸는 방식이 쓰임. 그런데 상상 영상에서는 성공한 것처럼 보여도 실제로는 물체가 미끄러지거나 충돌하는 후보가 높은 점수를 받을 수 있음. 이런 후보를 behavior cloning 목표로 받아들이면 정책이 잘못된 행동을 배우게 됨.

**어떻게 푸나**

TIF(Trusting Imagined Futures)는 고정된 후보 풀에서 supervision 궤적을 고르는 offline 방법임. 초기 상태마다 기존 궤적(Source), OpenVLA greedy 후보 1개, sampling 후보 3개를 실제로 실행하고, Cosmos-Predict2 2B로 같은 행동의 상상 영상을 만듦. reward model은 상상 영상, 지시문, 행동을 입력받아 utility 점수 하나와 5개 실행 품질 차원(진행도, 목표 정합성, 조작 품질, 안전, 안정성)의 등급을 예측함. auditor는 이 예측값, 예측 불확실성, 영상 진단값을 입력받아 과대평가 위험(risk)을 출력함. auditor의 정답은 예측 utility가 높은데 실제 실행 utility가 낮고 둘의 차이가 큰 경우로 정함. 선택 단계에서는 utility가 가장 높은 후보가 Source보다 0.15 넘게 높고 risk가 0.50 이하일 때만 교체하고, 아니면 Source를 유지함. 고른 실제 실행 궤적의 관측과 행동으로 OpenVLA의 LoRA를 behavior cloning으로 학습함.

**결과**

- LIBERO(시뮬레이션 조작 benchmark, Spatial/Object/Goal/Long 4개 suite 40개 과제) 평균 성공률이 TIF 76.25%, Source만 쓴 behavior cloning 73.25%임. 궤적 수 800개와 학습 budget은 같고, 학습 seed 3개 평균임. Goal suite에서는 TIF가 Source보다 1.00퍼센트포인트 낮음.
- reward model과 교체 기준(Source 대비 예측 utility 차이 0.15 초과)을 고정하고 audit gate만 더하면 평균 성공률이 74.78%에서 76.25%로 1.47퍼센트포인트 오름. seed 3개 모두에서 오름.
- 교체 개수를 230개로 맞춘 정책 학습 비교에서 TIF는 76.25%, 예측 advantage 순위는 75.55%, logistic regression risk는 75.65%임. offline 비교에서는 같은 후보 310개 중 111개를 고를 때 Source보다 나은 교체가 auditor 58개, 예측 advantage 47개임.
- 실제 JAKA S5 로봇 과제 3개의 후보 풀 60개에서, 녹화된 실행 영상을 채점해 하나씩 고름. 충돌이나 잘못된 물체 조작 없이 끝난 궤적 비율이 Reward-only 58.33%(35/60)에서 TIF 70.00%(42/60)로 오름.

**한계**

정책 학습 실험은 OpenVLA와 LIBERO에만 있고, 개선 폭은 평균 3퍼센트포인트 정도임. 실로봇 실험은 상상 영상이 아니라 녹화된 실제 실행 영상을 채점한 것이고, 고른 궤적으로 정책을 다시 학습하지는 않음. reward model과 auditor 학습에는 정책 학습용 후보 풀과 별도로, 초기 상태 8,000개에서 만든 실제 실행·상상 영상 32,000쌍이 필요함. video world model의 상상 rollout으로 policy를 최적화하는 WMPO나, 상상 결과의 신뢰도로 후보를 거르는 WISE와 직접 비교하지 않음. 코드 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- world model과 reward model이 실패를 성공으로 잘못 평가하는 경우를 실제 실행과 짝지어 따로 학습한 사례임. world model 기반 failure detection에서 평가 신뢰도를 다루는 비교 대상으로 쓸 수 있음.
- test-time에 VLA 후보 행동을 reward로 고르는 방식(offline RL value로 행동 순위를 다시 매기는 V-GPS, process reward로 후보를 고르는 RoVer 계열)에 risk gate를 붙이는 설계로 옮겨 볼 수 있음.

*대표 그림: LIBERO의 와인병을 선반에 올리는 과제에서 왼쪽에 world model 예측, 오른쪽에 실제 실행 장면을 둔 그림임. 기준 행동은 예측과 실행 모두 병이 선반 위에 놓임. 후보 행동은 예측에서는 선반 위에 놓이지만 실제 실행에서는 병이 미끄러져 선반 밖 바닥에 섬.*

---

### 13. DiMuRe: Diagnosis-Guided Multilevel Recovery for Robotic Task Execution (62점)

[arXiv](https://arxiv.org/abs/2611.04226) · [PDF](https://arxiv.org/pdf/2611.04226) · [alphaXiv](https://www.alphaxiv.org/abs/2611.04226) (요약 있음)

- **저자**: Renkai Yi, Yuwei Wu, Haoyu Zhang, Penghao Dai, Zhi Gao, Jin Chen, Che Sun
- **분야**: Failure Recovery · robotics relevance 8/10 · 1차 스크리닝 68점
- **학회**: IEEE 학술지 계열 양식 (추정) · 근거: IEEE 2단 양식, 15쪽
- **읽은 원문**: PDF 전문

> 작업 도중 물체가 밀리거나 grasp가 풀렸을 때, 진단 결과에 맞춰 기존 프로그램 재사용과 미리 만든 복구 skill 중 쓸 수 있는 것을 골라 실행하고 결과를 확인함. 시뮬레이션 교란 사례 801개에서 과제 성공률이 원래 프로그램의 58.68%에서 77.65%로 오름.

**무슨 문제인가**

code로 작업을 수행하는 robot-use agent는 실행 중 물체 위치나 grasp 상태가 바뀌면 다음 명령의 전제가 성립하지 않아 실패함. 이때 프로그램 대부분은 여전히 쓸 만하므로 전부 다시 짜는 것은 낭비이고, 그대로 계속 실행하면 실패함. 복구 방법마다 쓸 수 있는 조건이 다르므로, 지금 상태에서 어느 방법이 적용 가능한지 판단하고 복구가 실제로 됐는지 확인하는 절차가 필요함. 또 교란을 걸었다고 해서 그 교란이 실제로 적용되고 효과를 냈는지는 따로 기록되지 않아 평가도 어려움.

**어떻게 푸나**

DiMuRe(diagnosis-guided multilevel recovery)는 원래 작업 프로그램을 고치지 않고 실행 monitor를 붙여 motion·gripper 호출을 가로챔. 진단기는 rule 기반이며 현재 phase(grasp, transport, place, verify)에 따라 gripper 열린 폭, 물체와 end-effector의 변위 차이, 과제 관계를 RGB-D 기하로 확인함. 증거가 부족하면 결함으로 판정하지 않고 로봇을 위로 물러나게 한 뒤 다시 관측함. grasp 복구는 정해진 순서로 후보를 시도함: L1은 기록해 둔 grasp 구간의 waypoint를 물체 이동량만큼 평행이동해 재생하고, L2는 측정 형상 기반 regrasp와, 기존 grasp 전용 VLA인 GraspVLA를 쓴 grasp skill임. 후보마다 전제 조건을 먼저 확인해 맞지 않으면 건너뜀. 실행 후 grasp가 확인되면 탐색을 끝내고, 아니면 다음 후보로 넘어감. L3는 원래 프로그램이 끝난 뒤에만 들어가며, MLLM(DeepSeek V4.1 Flash)이 RGB 이미지·상태·프로그램 맥락·실행 기록을 받아 교정 code를 생성함. 모든 단계는 같은 물리 step 예산을 나눠 씀.

**결과**

- LIBERO-Disturb(LIBERO 과제 실행 도중 9종 교란을 거는 저자들의 새 benchmark)에서 평가함. Encore(평가 전에 과제 프로그램을 code로 미리 만들어 두는 기존 방법)의 프로그램 30개와 교란 사례 801개를 씀. 같은 물리 step 한도(1,000)에서 과제 성공률이 원래 프로그램 58.68%에서 Local DiMuRe(L1+L2) 77.65%로 오름.
- 단계별 ablation에서 L1만 쓰면 73.66%, L2만 쓰면 65.54%임. grasp slip 90건 성공은 L1만 72건 대 L2만 49건이고, 물체 자세 변화 81건 성공은 L1만 26건 대 L2만 47건임.
- 원래 프로그램이 성공한 470건 중 Local은 463건을 유지함. 교란 없는 90건은 원래 프로그램, Local, Full(L1~L3 모두 사용) 세 설정 모두 100% 성공함.
- 사례당 평균 물리 step은 Local 310.20, 원래 프로그램 328.90으로 Local이 적음. 평균 작업 시간은 5.47초 대 4.65초로 Local이 김. Full은 81.90%이나 step 400을 더 받음. 또 결함이 계속되면 프로그램이 끝나기 전에 L3로 넘기는 조기 handoff도 허용돼 L3만의 효과로 볼 수 없음.

**한계**

결과는 모두 시뮬레이션이며 801개 사례는 개발 중에 고른 부분집합이고 사전 등록된 held-out 평가가 아님. 801건에서 뺀 교란 유형(물체를 놓을 영역을 6cm 옮기는 교란) 90건에서는 Local이 67건 성공으로 원래 프로그램 79건보다 낮음. 801건 중 교란의 물리적 효과가 확인된 것은 105건뿐이고, DoReMi 같은 기존 복구 방법과 직접 비교하지 않았으며 코드 공개 주소는 본문에 없음.

**누리랩 연구와의 연결**

- failure detection·recovery 연구에서, 진단 증거가 부족할 때 재관측하고 복구 후보를 전제 조건과 사후 검증으로 거르는 절차를 비교 기준으로 쓸 수 있음.
- LIBERO-Disturb는 교란 적용, 물리적 효과, 과제 성공을 따로 기록하고 π0.5 같은 VLA policy에도 붙일 수 있어 VLA의 실행 중 교란 강건성 평가에 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 왼쪽은 RGB-D·로봇 상태·맥락에서 출발해 증거가 부족하면 재관측하는 layered diagnosis임. 오른쪽은 L1 프로그램 재사용, L2 복구 skill, L3 MLLM 재계획, 그리고 Template→Geometry→VLA 순서로 admit·execute·verify하는 grasp 복구 흐름임.*

---

### 14. Cycle WAM: Coupling Action and Video through Cycle Consistency (60점)

[arXiv](https://arxiv.org/abs/2611.04711) · [PDF](https://arxiv.org/pdf/2611.04711) · [alphaXiv](https://www.alphaxiv.org/abs/2611.04711) (요약 있음)

- **저자**: Qinglin Yang, Jiepeng Wang, Yuxing Huang, Haibin Huang, Kai Xu, Chi Zhang, Ruizhen Hu, Xuelong Li
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> 영상과 행동을 함께 생성하는 world action model에, 영상과 행동 사이 양방향 변환 학습과 행동으로 영상을 다시 복원하는 cycle 학습 목표를 더함. LIBERO-Pro 교란 조건 4개 평균 성공률이 DreamZero의 13.5%에서 17.8%로 오르지만, 오른 폭 대부분은 cycle이 아니라 양방향 변환 학습에서 나옴.

**무슨 문제인가**

world action model(WAM)은 사전학습된 video model 위에서 미래 영상과 로봇 행동을 함께 생성하는 모델임. DreamZero, UWM 같은 기존 WAM은 두 출력을 한 backbone에서 만들지만, 예측한 행동이 예측한 영상 변화를 실제로 만들어 내는지는 학습 목표에 들어 있지 않음. 그럴듯한 미래 영상을 만들어도 그 영상에 맞는 실행 가능한 행동이 함께 나온다는 보장이 없음. 저자들은 이 불일치 때문에 사전학습된 영상 지식이 행동 예측에 충분히 쓰이지 못한다고 봄.

**어떻게 푸나**

Cycle WAM은 DreamZero 구조의 5B WAM(Wan2.2-TI2V-5B에서 초기화)을 세 단계로 학습함. 첫 단계는 관측, 로봇 상태, 지시문을 받아 미래 영상과 7차원 행동을 함께 생성하는 co-training임. 둘째 단계 Bidirectional Conversion은 같은 모델에 영상을 주고 행동을 맞히게 하거나(inverse dynamics), 행동을 주고 영상을 맞히게 함(forward dynamics). 셋째 단계 Cycle은 원본 영상에서 한 번의 flow readout으로 행동을 추정하고, 그 행동으로 원본 영상을 다시 복원하게 함. 추정한 행동을 계산 그래프에 남겨 두므로 복원 손실의 gradient가 forward 경로를 거쳐 inverse 경로까지 흐름. 기록된 행동으로 inverse를 따로 지도하는 항도 함께 두어 행동이 실제 로봇 명령에서 벗어나지 않게 함. 배포 시에는 cycle을 돌리지 않고 joint generation으로 영상과 행동을 바로 생성함.

**결과**

- LIBERO-Pro(LIBERO 과제에 지시문 바꾸기와 물체 위치 바꾸기 교란을 건 평가)에서 고른 조건 4개, 조건당 100 episode의 평균 성공률이 17.8%임. 같은 조건에서 직접 평가한 DreamZero는 13.5%, π0.5는 15.3%임. 조건 이름의 T는 지시문 바꾸기, S는 물체 위치 바꾸기 교란임. 다만 Spatial-T에서는 DreamZero(27%)보다, Goal-S에서는 π0.5(38%)보다 낮음.
- 같은 표의 ablation에서 Cycle을 뺀 모델의 평균은 17.0%로, 오른 폭의 대부분은 Bidirectional Conversion에서 나옴. 같은 checkpoint에서 데이터와 계산량을 맞춰 이어 학습한 비교에서는 Cycle의 추가 이득이 일관되게 나타나지 않음.
- DROID(대규모 실로봇 조작 데이터셋) 기반 DreamZero-DROID 시뮬레이터 장면 3개(장면당 20 episode)에서 성공 횟수가 59/60임. Cycle을 뺀 변형은 58/60, 공개 DreamZero 가중치는 52/60임.
- 실로봇에서는 평가한 장면 5개 중 3개에서 과제를 완료했고 DreamZero는 0개임. 장면 단위 집계이며 반복 시행 성공률은 아님.

**한계**

제목의 Cycle 목표가 따로 기여한다는 증거가 약함. 저자도 학습 예산과 update 방식이 달라 각 목표의 기여를 분리하지 못했고, 전체 LIBERO-Pro 집계는 거의 변하지 않으며 교란 없는 Standard 조건 성능은 Bidirectional Conversion 뒤 내려간다고 적음. 실로봇은 장면 5개의 완료 여부만 있고, 원문에 코드 공개 주소가 없음.

**누리랩 연구와의 연결**

- world model과 VLA를 한 모델에서 forward/inverse dynamics로 함께 학습하는 설정이라, 행동과 예측 영상의 일치도를 failure detection 신호로 쓰는 연구의 출발점이 될 수 있음.
- 같은 checkpoint에서 데이터와 계산량을 맞춰 이어 학습했을 때 cycle 손실의 추가 이득이 없었다는 결과는, world model 기반 policy에 cycle consistency를 넣으려 할 때 미리 확인할 부정적 근거가 됨.

*대표 그림: LIBERO 장면 4개의 forward dynamics 예측 결과임. 왼쪽부터 정답(GT), UWM, Cycle WAM 열이고, 각 열에 카메라 시점 2개가 있음. UWM 예측은 로봇 팔과 그릇 경계가 번지고 색이 섞인 반면 Cycle WAM 예측은 윤곽과 질감이 더 또렷하지만, 물체 위치와 화면 구성은 정답과 일부 다름.*

---

### 15. Physical Experience Builds Continual Spatial World Models (50점)

[arXiv](https://arxiv.org/abs/2611.04016) · [PDF](https://arxiv.org/pdf/2611.04016) · [alphaXiv](https://www.alphaxiv.org/abs/2611.04016) (요약 있음)

- **저자**: Yuhang Sun
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 68점
- **학회**: NeurIPS 2026 채택 · 근거: 1쪽에 "40th Conference on Neural Information Processing Systems (NeurIPS 2026)"
- **읽은 원문**: PDF 전문

> 공이 굴러가는 원형 미로에서 문의 열림 여부가 바뀌는 변화 사이의 관계를 여러 에피소드에 걸쳐 배우는 memory(SCM)를 만듦. 학습에서 한 번도 안 본 위치의 문 상태를 0.898의 정확도로 맞혔고, 위치별 memory는 약 0.566에 머묾.

**무슨 문제인가**

변하는 환경을 다시 방문하는 로봇은 바뀐 곳을 보고 나서 경로를 다시 짜는 reactive 방식으로도 매번 과제에 성공할 수 있음. 하지만 이 방식은 열 번째 방문에도 첫 방문과 같은 관측과 수정이 필요해서, 경험이 쌓여도 다음 방문이 쉬워지지 않음. D* Lite(예전 탐색 정보를 남겨 경로를 다시 짤 때 쓰는 planner)나 Experience Graphs(예전에 성공한 동작으로 다음 planning을 유도하는 방법)가 있음. 이들은 예전 탐색 결과나 성공한 동작을 재사용할 뿐, 환경이 어떻게 바뀌는지를 배우지는 않음. 또 경로가 위상적으로 맞아도 관성, 마찰, 접촉, actuator 지연 때문에 행동 결과 예측은 틀릴 수 있음.

**어떻게 푸나**

실험 환경은 기울어지는 원형 미로임. 동심원 고리 사이 벽에 문이 있고, 문의 열림 여부는 에피소드마다 바뀜. 인접한 고리의 경로 관련 상태가 확률 1−ε로 같도록 변화 구조를 통제함. SCM(Spatial Change Memory)은 위쪽 고리의 관측 상태를 입력으로 아래쪽 고리 상태를 예측하는 조건부 확률을 Beta prior와 개수 세기로 추정함. 이 추정기를 모든 위치가 공유하므로 한 위치에서 모은 증거를 다른 위치에 바로 씀. 주행 중에는 SCM이 아래쪽 문이 보이기 전에 그 상태를 추론해 경로를 바꾸고, 증거가 부족하면 reactive 판단으로 돌아감. 별도로 공의 운동은 rolling 관성, 선형·2차 drag, 탄성 벽 접촉, 1차 actuator 지연을 넣은 물리 모델로 예측함. 상태·행동·다음 상태 기록이 쌓이면 이 모델의 parameter 5개를 갱신함.

**결과**

- ε=0.10에서 학습 에피소드를 0개에서 64개로 늘리면 shared SCM의 예측 정확도가 0.564에서 0.898로 오름. 이론상 최대치(Bayes 한계)는 0.900임. 에피소드당 경로 수정 횟수는 1.744에서 0.406으로 내림.
- 학습에서 완전히 뺀 위치 하나를 평가하면 shared SCM은 0.898, reactive·episodic·위치별 memory는 약 0.566임. 과거와 미래 변화가 독립인 ε=0.5 조건에서는 history를 늘려도 정확도가 약 0.50에 머묾.
- 연속 주행 시뮬레이션의 결정이 바뀌는 에피소드 15개에서, 이미 무효가 된 목표를 쫓는 시간이 reactive 방식 7.806초에서 SCM 0.0083초(한 simulation step)로 내림. 평균 완주 시간은 42.25초에서 34.69초로 줄었고, 결정이 그대로인 에피소드 15개에서는 완주 시간 차이가 0임.
- 물리 parameter 추정은 일부러 틀린 초기값에서 시작함. 2,000개 transition을 쌓은 뒤 가장 큰 parameter 오차가 4.69%로 내림.

**한계**

모든 실험이 시뮬레이션이고, 문 상태는 인식 오류 없이 관측되며 변화는 이진이고 일부러 구조화됨. 물리 모델 학습은 정답 방정식 형태를 알고 parameter만 맞추는 설정임. D* Lite 등 기존 방법과 직접 비교하지 않았고, 코드나 프로젝트 주소는 본문에 없음.

**누리랩 연구와의 연결**

- 직접 연결 약함. 다만 robot memory나 continual world model 연구에서 변화 구조가 없는 ε=0.5 대조군과 학습에서 뺀 위치 평가를 넣는 실험 설계는 참고할 만함.

*대표 그림: 측정 결과가 아니라 실험 논리를 그린 개념도임. 원형 미로와 공(a), reactive 갱신 순서(b), 과거 에피소드의 상태 쌍에서 조건부 확률을 배우는 SCM(c), 구조화된 변화와 ε=0.5 무작위 변화 대조(d)를 보여 줌.*

---

## 오늘의 흐름

- **world action model이 예측하는 대상 바꾸기**: 미래 영상 전체를 만들지 않고 action에 필요한 정보만 예측하는 world action model(WAM)이 여럿 나옴. [FloMo](https://arxiv.org/abs/2611.05062)는 미래 영상 대신 3D scene flow를 예측하고, [DreamFree](https://arxiv.org/abs/2611.04527)는 video diffusion model의 미래 feature를 현재 관측 encoder에 distillation해 영상 생성 없이 action을 냄. [Cycle WAM](https://arxiv.org/abs/2611.04711)은 영상에서 행동을, 행동에서 영상을 서로 복원하게 학습함.
- **world model을 simulator와 평가기로 쓰기**: [PrimeSim](https://arxiv.org/abs/2611.04870)은 22개 플랫폼 데이터로 다시점 action-conditioned simulator를 만듦. [Compression Forcing](https://arxiv.org/abs/2611.04028)은 과거 프레임 압축 방식을 바꿔, world model이 예측한 policy 성공률을 비교 tokenizer보다 실제 값에 가깝게 맞춤. [TIF](https://arxiv.org/abs/2611.04873)(Trusting Imagined Futures)는 상상 결과에 매긴 reward를 실제 실행으로 학습한 auditor가 다시 검사함.
- **VLA post-training의 학습 방식 따지기**: [RAFT](https://arxiv.org/abs/2611.04368)는 reasoning adapter를 먼저 학습하고 고정해, 실로봇 분포 밖 조건 성공률을 plain fine-tuning보다 높임. [Should the Action Expert Train the VLM?](https://arxiv.org/abs/2611.05249)은 action expert의 gradient를 VLM까지 흘릴지를 통제 비교함. [CANDO](https://arxiv.org/abs/2611.04543)는 고정된 flow matching policy를 noise와 행동 두 공간에서 online RL로 고침.
- **로봇 없이 모은 사람 데이터로 VLA 학습하기**: [AIRoA-0](https://arxiv.org/abs/2611.03815)는 손에 드는 gripper로 녹화한 16,151시간 데모만으로 양팔 VLA를 학습함. [H2RB](https://arxiv.org/abs/2611.04391)(Human-To-Robot Bridge)는 사람 손 시연을 관측과 행동 양쪽에서 로봇에 맞춰 사전학습 VLA에 새 동작을 가르침.
- **실패를 찾고 복구하기**: [Say the Same, Act Differently](https://arxiv.org/abs/2611.04166)는 reasoning VLA의 rationale을 그대로 둔 채 행동만 바꾸는 교란을 보여, 글만 보는 monitor로는 실패를 못 잡는 경우를 드러냄. [DiMuRe](https://arxiv.org/abs/2611.04226)는 실행 중 교란을 진단하고 복구 수단을 골라, 시뮬레이션 교란 사례 801개의 과제 성공률을 58.68%에서 77.65%로 올림.

## 해볼 만한 연구

### 예측한 scene flow와 실제 움직임의 차이로 실행 중 실패 감지하기
- 질문: world action model이 예측한 3D scene flow와 실행 뒤 관측한 실제 scene flow의 차이가, 영상 예측 오차보다 실패를 더 일찍 알려 주는지 밝힘.
- 첫 실험: LIBERO-Disturb(실행 중 교란을 넣는 시뮬레이션 조작 benchmark)에서 FloMo 방식의 flow 예측 오차와 영상 예측 모델의 픽셀 오차를 실패 예측 점수로 씀. 실패 발생 전 몇 step에서 AUROC가 얼마인지 비교함.
- 가장 가까운 연구: [FloMo](https://arxiv.org/abs/2611.05062)는 flow를 action 예측에만 쓰고 실패 판정에는 쓰지 않음. [DiMuRe](https://arxiv.org/abs/2611.04226)는 rule 기반 기하 검사로 교란을 진단하고, 학습된 예측 모델의 오차를 실패 신호로 쓰지 않음.

### rationale과 행동이 어긋나는지 action 쪽에서 검사하는 monitor
- 질문: reasoning VLA에서 rationale이 같을 때 행동이 달라지는 경우를, hidden state를 TNAS(text loss gradient 성분을 뺀, 행동이 가장 민감한 방향)에 투영한 크기만으로 실행 전에 잡을 수 있는지 밝힘.
- 첫 실험: 조작용 reasoning VLA인 InstructVLA에 이미지 교란과 자연스러운 조명·가림 변화를 각각 넣음. 이후 TNAS 투영 크기와 rationale 기반 monitor의 실패 검출률을 비교함.
- 가장 가까운 연구: [Say the Same, Act Differently](https://arxiv.org/abs/2611.04166)는 공격을 만드는 데 TNAS를 쓰고 방어나 검출은 시험하지 않음.

### 상상 결과의 reward를 믿을지 test-time에 고르기
- 질문: world model이 상상한 후보 행동 중 하나를 실행 직전에 고를 때, 실제 실행으로 학습한 auditor gate(TIF식 과대평가 위험 판정기)가 성공률을 올리는지 밝힘.
- 첫 실험: PrimeSim 같은 공개 world model simulator로 VLA 후보 action chunk 여러 개를 rollout함. 이후 reward 최대값으로 고르는 방식과 TIF식 auditor gate를 붙인 방식의 실제 성공률을 비교함.
- 가장 가까운 연구: [TIF](https://arxiv.org/abs/2611.04873)는 학습 데이터를 고르는 offline 단계에만 auditor를 쓰고, 실행 시점의 행동 선택에는 쓰지 않음.

## 꼭 읽을 논문

- [DreamFree](https://arxiv.org/abs/2611.04527): 미래 영상을 만들지 않고 world model feature를 distillation함. 실제 DROID 과제 10개 성공률이 DreamZero 56%에서 64%로 오르고, action chunk당 latency는 91ms로 17.8배 빠름.
- [AIRoA-0](https://arxiv.org/abs/2611.03815): 로봇 없이 사람이 손에 든 gripper로 녹화한 데모 16,151시간만으로 양팔 VLA를 학습하고 데이터와 가중치 공개를 밝힘.
- [FloMo](https://arxiv.org/abs/2611.05062): 같은 구조에서 예측 대상만 영상에서 3D scene flow로 바꿔 처음 보는 과제 성공률이 7%에서 60%로 오름.
- [Say the Same, Act Differently](https://arxiv.org/abs/2611.04166): rationale 기반 failure monitor가 놓치는 경우를 hidden state 기하로 설명함.
- [Should the Action Expert Train the VLM?](https://arxiv.org/abs/2611.05249): VLA 학습에서 gradient 차단과 action token 감독을 따로 끄고 켠 통제 비교라 우리 기본 설정을 점검할 근거가 됨.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (488편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2611.03815'>AIRoA-0: Long-Horizon, Precise, Cross-Embodiment Manipulation from Handheld Data</a></td><td>82</td><td>10</td><td>VLA</td><td>handheld 데이터 16,151시간으로 로봇 데이터 없이 bimanual 정책을 학습함. 규모와 cross-embodiment 주장이 강함</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2611.05062'>FloMo: 3D Scene Flow as a World Action Model Intermediate for Learning from Human Video</a></td><td>80</td><td>10</td><td>VLA</td><td>3D scene flow를 world action model 중간 표현으로 써서 사람 영상에서 로봇 policy를 학습함</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2611.04711'>Cycle WAM: Coupling Action and Video through Cycle Consistency</a></td><td>72</td><td>9</td><td>World Model</td><td>cycle consistency로 행동과 영상을 묶는 world action model로 VLA와 직접 관련됨</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2611.04870'>PrimeSim: A Generalist World Model Simulator from Large-Scale Cross-Embodiment Demonstrations</a></td><td>72</td><td>9</td><td>World Model</td><td>cross-embodiment 대규모 데이터 generalist world model simulator임. action 충실도 평가에 초점이 있음</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2611.04873'>Trusting Imagined Futures: Auditing Imagined Rewards for VLA Post-Training</a></td><td>72</td><td>9</td><td>VLA</td><td>imagined reward를 감사해 VLA post-training의 reward hacking을 줄임. world model reward 신뢰성 문제를 다룸</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2611.04368'>RAFT: Reasoning-Aligned Fine-Tuning Improves Robustness of VLA Post-Training</a></td><td>70</td><td>10</td><td>VLA</td><td>reasoning 정렬 fine-tuning으로 VLA post-training 견고성을 높임. VLA 주제에 직접 부합함</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2611.05249'>Should the Action Expert Train the VLM? Action-Token Supervision and Gradient Routing in Mixture-of-Transformer VLAs</a></td><td>70</td><td>10</td><td>VLA</td><td>action expert가 VLM을 학습시켜야 하는지 gradient routing으로 분석함. VLA 설계 질문이 구체적임</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2611.04543'>CANDO: Conservative Action-Noise Directional Optimization for Residual Reinforcement Learning</a></td><td>70</td><td>9</td><td>RL</td><td>frozen generative policy에 residual RL을 보수적 action noise 방향 최적화로 적용하는 방법으로 policy 적응 문제에 직결됨</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2611.04391'>Human-to-Robot Transfer via Bridging Representation and Action Space in VLAs</a></td><td>70</td><td>9</td><td>VLA</td><td>사람 영상에서 로봇으로 VLA를 옮길 때 표현과 action space를 잇는 방법으로 주제에 직접 맞으나 세부 실험 확인 필요함</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2611.04166'>Say the Same, Act Differently: Diagnosing and Steering Text-Action Divergence in Reasoning VLAs</a></td><td>68</td><td>9</td><td>VLA</td><td>reasoning VLA에서 텍스트 rationale과 행동이 어긋나는 현상을 진단하고 steering하며 안전 감시 관점의 새 공격면을 제시함</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2611.04493'>Physical Diffusion Policy via MPM-Guided 3D Gaussian Simulation</a></td><td>68</td><td>9</td><td>Manipulation</td><td>MPM 가이드 3D Gaussian 시뮬레이션으로 diffusion policy를 학습함. 물성 다양한 물체 대응이 흥미로움</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2611.04527'>Future Representation Distillation for Imagination-free World Action Models</a></td><td>68</td><td>9</td><td>World Model</td><td>future representation distillation으로 imagination 없는 WAM을 만듦. 추론 효율과 world action model 결합임</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2611.04016'>Physical Experience Builds Continual Spatial World Models</a></td><td>68</td><td>8</td><td>World Model</td><td>물리 경험으로 spatial world model을 continual 학습함. 주제 적합하나 규모 확인 필요함</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2611.04226'>DiMuRe: Diagnosis-Guided Multilevel Recovery for Robotic Task Execution</a></td><td>68</td><td>8</td><td>Failure Recovery</td><td>진단 기반 다단계 recovery임. failure diagnosis와 recovery 주제에 직접 부합함</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2611.04028'>Compression Forcing: Hierarchical History Tokenization Enables Flexible World Models</a></td><td>68</td><td>7</td><td>World Model</td><td>계층적 history tokenization으로 예측에 유용한 압축을 학습하는 world model임</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2611.05155'>Asynchronous Robot Policies</a></td><td>66</td><td>10</td><td>VLA</td><td>비동기 robot policy로 대형 VLA 지연을 줄임. 실용적 추론 효율 주제임</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2611.05163'>Synthesizing Dexterous Robot Demonstrations from Human Videos via Virtual Try-On</a></td><td>66</td><td>9</td><td>Manipulation</td><td>virtual try-on으로 인간 영상에서 dexterous 시연을 합성함. 데이터 확장 방법임</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2611.04492'>Hybrid Particle-Voxel Dynamics for Multimodal 3D World Simulation</a></td><td>66</td><td>8</td><td>World Model</td><td>particle-voxel 하이브리드 3D world simulation임. 로봇 행동 조건 예측 표현이 새로움</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2611.04839'>Coordinating Humanoid Loco-Manipulation through Action-Conditioned Latent Foresight</a></td><td>66</td><td>8</td><td>Humanoid</td><td>action-conditioned latent foresight로 humanoid loco-manipulation을 조율함. world model 활용이 적합함</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2611.03937'>FlowBench: Counterfactual Imagination Training for Spatial Intelligence</a></td><td>66</td><td>7</td><td>Embodied AI</td><td>가상 움직임에 따른 장면 변화를 상상하는 counterfactual spatial imagination 과제와 학습 자원을 제안함</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2611.04195'>SettleSplat: Monocular Gaussian Mapping under In-View Scene Changes</a></td><td>66</td><td>7</td><td>3D Vision</td><td>조작 중 장면 변화를 다루는 단안 Gaussian 온라인 매핑으로 로봇 조작과 연결됨</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2611.04522'>Action Intent as a Bridge: Transferring Manipulation Knowledge from Human-Centric Videos to Robots</a></td><td>65</td><td>10</td><td>VLA</td><td>action intent로 인간 중심 지식을 VLA에 이전함. 데이터 효율 주제에 부합함</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2611.05119'>DexHOT: Learning Hand-Object Configuration Transfer for Dexterous Manipulation</a></td><td>64</td><td>9</td><td>Dexterous</td><td>hand-object 구성 전이로 dexterous manipulation을 학습함. 접촉 배치 관점이 새로움</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2611.05023'>HiLo-WAM: Decoupling Long-Horizon Task Evolution and Local Dynamics in World Action Models</a></td><td>62</td><td>9</td><td>World Model</td><td>long-horizon 진화와 local dynamics를 분리한 WAM임. 구조 제안이 명확함</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2611.05080'>CRONOS: Benchmarking Non-Episodic Reinforcement Learning for Robotic Manipulation</a></td><td>62</td><td>9</td><td>RL</td><td>non-episodic RL 매니퓰레이션 벤치마크임. 실제 적응 RL 평가에 유용함</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2611.05368'>GUILD: Guided Iterative Data Collection for Imitation Learning</a></td><td>60</td><td>9</td><td>Imitation Learning</td><td>guided iterative 데이터 수집으로 IL 효율을 높임. 데이터 수집 전략 주제임</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2611.05058'>Do Agentic Policies Need to Look at Every Step? Geometric Abstraction for Reasoning and Action</a></td><td>60</td><td>8</td><td>Embodied AI</td><td>기하 abstraction으로 agentic 정책 reasoning을 줄임. 효율적 추론 관점이 좋음</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2611.05093'>LoopQ: Fair, Closed-Loop Evaluation of Quantized Vision-Language-Action Models</a></td><td>60</td><td>8</td><td>VLA</td><td>양자화 VLA 폐루프 공정 평가임. efficient inference 평가 도구로 가치 있음</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2611.04241'>AceAction-5M: Hierarchical Goals for Generalist Action Learning Across 3D Game Worlds</a></td><td>60</td><td>6</td><td>VLA</td><td>3D 게임 환경에서 계층적 목표를 단 VLA 학습용 대규모 데이터셋으로 규모는 크나 게임 도메인 한정임</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2611.05295'>GSBR: Geometric Support Behavior Regularization for Online RL</a></td><td>58</td><td>8</td><td>RL</td><td>online RL의 geometric support 행동 정규화임. 기존 정규화 개선 성격임</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2611.04228'>DualWorldBench: Can Agents Plan Deliveries across Symbolic and Grounded Worlds?</a></td><td>58</td><td>6</td><td>Embodied AI</td><td>기호 세계와 실세계 배달 계획을 함께 평가하는 benchmark로 embodied planning 관련이나 평가 위주 기여임</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2611.04080'>FEIJOA: Task-Driven Grounding and Execution for Mobile Manipulation</a></td><td>55</td><td>8</td><td>Mobile Manipulation</td><td>작업 기반 grounding과 실행 모바일 매니퓰레이션 시스템임. 통합 위주임</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2611.04485'>All-For-One: Distilling Visual Foundation Models to a Fast, Memory-Efficient Visuomotor Policy</a></td><td>55</td><td>8</td><td>Manipulation</td><td>VFM을 빠른 시각 encoder로 distillation함. efficient inference로 유용하나 증류 자체는 흔함</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2611.05113'>HLO-AMP: Hierarchical Loco-Manipulation from Object-Aware Motion Priors</a></td><td>55</td><td>8</td><td>Humanoid</td><td>object-aware motion prior로 계층적 loco-manipulation을 함. 계층 설계는 흔함</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2611.05320'>PyRUA-DataFarm: LLM Agent as a Cost-Efficient Teleoperator for Real-Ready Robot Data</a></td><td>55</td><td>8</td><td>Imitation Learning</td><td>LLM agent를 텔레오퍼레이터로 써 데이터 수집 비용을 줄임. 품질 검증 필요함</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2611.04422'>GVT3D: Gesture-Vision-Text Token Enrichment for 3D Embodied Reference Understanding</a></td><td>55</td><td>7</td><td>Embodied AI</td><td>제스처 시각 텍스트 token으로 3D embodied reference understanding을 개선함</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2611.05084'>Sparse Anchors for Visual Multi-Session Registration in Changing Environments</a></td><td>55</td><td>7</td><td>Navigation</td><td>변화 환경에서 로봇의 다중 세션 시각 정합을 위한 sparse anchor임</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2611.04424'>ReflexArc: Bottom-Up Integration of Instantaneous Tactile Reflexes into Whole-Body Humanoid Control</a></td><td>55</td><td>7</td><td>Tactile</td><td>전신 휴머노이드 촉각 반사 통합임. 접촉 반응 설계가 구체적임</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2611.04836'>HTCE: Homeomorphism-inspired Topological Cross-Scene Experience Canonicalization and Reuse for Object Navigation</a></td><td>55</td><td>7</td><td>Navigation</td><td>object-goal navigation 경험을 위상 기반으로 장면 간 표준화하는 방법으로 navigation과 memory에 맞으나 세부 검증 확인 필요함</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2611.04221'>Mamba3R: Fixed-Capacity Selective State Memory for Long-Sequence 3D Reconstruction</a></td><td>55</td><td>6</td><td>3D Vision</td><td>고정 용량 상태 메모리로 스트리밍 3D 재구성을 장시간 유지하는 방법임</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2611.04974'>LLMs as MDP Designers: A Dependency-Aware Agentic Framework for Automated Robot Policy Generation</a></td><td>55</td><td>6</td><td>RL</td><td>LLM이 MDP를 설계해 robot RL 정책을 자동 생성함. reward 설계 자동화임</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2611.04006'>Controlling Action-Head Co-Adaptation to VLM Representation Anisotropy</a></td><td>55</td><td>6</td><td>VLA</td><td>VLM 표현의 anisotropy와 action head co-adaptation을 다룬 VLA 관련 분석으로 주제는 맞으나 실험 범위는 확인 필요함</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2611.05029'>DRAP: Dynamics-Risk Adaptive Plasticity for Continual Learning in Physical AI</a></td><td>52</td><td>7</td><td>RL</td><td>physical AI의 continual learning에서 궤적 오차 누적 위험에 맞춰 plasticity를 조절하는 방법으로 문제 설정이 로봇에 맞음</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2611.04093'>VARP: A Visual Adaptive Rearrangement Planner for Non-Monotone Object Rearrangement Planning</a></td><td>52</td><td>7</td><td>Planning</td><td>non-monotone 재배치 시각 적응 플래너임. long-horizon 계획 관련임</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2611.05172'>PadLoc: Training-Free Floor-Plan Localization by Sparse Geometric Matching</a></td><td>52</td><td>6</td><td>Navigation</td><td>학습 없이 floor plan 위치 추정을 하는 sparse 기하 매칭임</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2611.04708'>CLARA: A Cognitively-Driven Clarification Framework for Grounding Ambiguous Requests</a></td><td>52</td><td>6</td><td>Embodied AI</td><td>모호한 요청 clarification 프레임워크임. 인지 기반 설계이나 평가 범위 확인 필요함</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2611.04494'>Spatial Memory for AR Glasses: Hierarchical Visual Acquisition and Source-Linked Recall</a></td><td>52</td><td>5</td><td>Embodied AI</td><td>AR 안경에서 시각 기억을 계층 획득하고 출처를 연결해 회상하는 spatial memory 시스템으로 robot memory와 닿으나 시스템 데모 성격임</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2611.04943'>Learning Where to Look: Observation Policy Optimization for Thinking with Images</a></td><td>52</td><td>4</td><td>Multimodal</td><td>관찰 위치를 RL로 학습하는 thinking with images로 active perception과 유사함</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2611.04073'>Computer-Use Agents Gain Little Benefit from a World Model When Conditioned on Tutorials</a></td><td>52</td><td>4</td><td>Agent</td><td>computer-use agent에서 world model의 이득이 tutorial 조건에서 작다는 부정적 결과로 ablation 가치는 있음</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2611.04477'>Spectrally Routed Diffusion Policy for Multi-Task Robotic Manipulation</a></td><td>50</td><td>9</td><td>Manipulation</td><td>spectral routing diffusion policy로 multi-task 학습함. 작은 module 수준임</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2611.03850'>RoboScope Kit: Unified Interfaces for Fast and Scalable Embodied-AI Evaluation</a></td><td>50</td><td>7</td><td>Embodied AI</td><td>여러 sim benchmark 평가 인터페이스 통합 도구임. 재현성에 유용하나 방법 novelty는 낮음</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2611.04972'>Caging Vision-Language Navigation for Legged Robots via Barrier-Certified Safety Architecture</a></td><td>50</td><td>7</td><td>Navigation</td><td>barrier 인증 안전으로 legged VLN을 보호함. 안전 계층 결합임</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2611.04027'>A Practical Causal Framework for Autonomous Mobile Robots: From Simulation to Real-World Human Environments</a></td><td>50</td><td>6</td><td>Causal</td><td>이동 로봇용 causal 프레임워크임. 시뮬레이션에서 실제까지 다루나 기법 novelty는 보통임</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2611.05443'>SurgTransfer: Multi-Step Latent Action Modeling for Action Transfer in Surgical World Model</a></td><td>50</td><td>4</td><td>World Model</td><td>수술 world model에서 latent action으로 행동을 전이하는 방식으로 world model 관점은 흥미로우나 도메인이 특수함</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2611.04244'>CounterSketch: Physics-Grounded Counterfactual Reasoning for Sketch-to-Video Generation</a></td><td>50</td><td>3</td><td>Video</td><td>물리 기반 counterfactual 스케치 애니메이션 생성이나 로봇 적용은 약함</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2611.05313'>MDSKILL: Learning to Internalize Skill Memory through Multi-View Distillation for Efficient Dynamic Agent Self-Evolution</a></td><td>50</td><td>2</td><td>LG</td><td>skill memory를 multi-view distillation으로 내재화하는 RL 방법으로 memory 아이디어는 있으나 LLM 에이전트 대상임</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2611.04113'>The Evolution Strategies Paradox: Better Models from Worse Perturbations</a></td><td>50</td><td>1</td><td>RL</td><td>Evolution Strategies가 LLM을 최적화하는 이유를 설명하는 분석으로 일반적 통찰은 있으나 로봇 실험은 없음</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2611.04010'>Decision Transformer with Task-Aware Representations for Offline Meta-Reinforcement Learning</a></td><td>48</td><td>6</td><td>RL</td><td>Decision Transformer에 task 표현을 넣은 offline meta-RL로 방법은 incremental임</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2611.04614'>Policy Network Diffusion</a></td><td>48</td><td>6</td><td>RL</td><td>diffusion으로 RL policy network 파라미터를 생성하는 시도로 참신하나 제한된 설정으로 보임</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2611.04912'>MiCaDe: Online LiDAR-Camera Miscalibration Change Detection for Autonomous Driving</a></td><td>48</td><td>5</td><td>3D Vision</td><td>LiDAR 카메라 miscalibration 변화를 온라인으로 검출함</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2611.04164'>What Remains in Sight? Autoregressive Video Decoding as Representation-Guided Context Rewriting</a></td><td>48</td><td>4</td><td>Video</td><td>자기회귀 영상 생성에서 context를 재작성하는 방식으로 장기 일관성을 다룸</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2611.04666'>Phase-DGS: Phase-guided Dynamic Gaussian Splatting from Unsynchronized Multi-view Video</a></td><td>48</td><td>4</td><td>3D Vision</td><td>비동기 다시점 영상에서 위상 기반 dynamic Gaussian을 복원함</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2611.05072'>Trajectory Evaluation via Rollout-Free World Model for End-to-end Autonomous Driving</a></td><td>48</td><td>3</td><td>Autonomous Driving</td><td>rollout 없는 world model 궤적 평가임. 주행 영역이라 연결은 중간임</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2611.03861'>Predictive gains, causal losses: why interventional competence cannot be learned from data alone</a></td><td>48</td><td>1</td><td>LG</td><td>개입 능력은 예측 학습만으로 얻을 수 없다는 이론 결과로 causal 추론과 닿으나 로봇 실험은 없음</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2611.04083'>MABEL: An Open Anthropomorphic Mobile Bimanual Platform for Teleoperation and Learning</a></td><td>45</td><td>7</td><td>Hardware</td><td>오픈 모바일 bimanual 텔레오퍼레이션 플랫폼임. 하드웨어 기여임</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2611.05129'>WayTrace: A Map-to-Language-to-Trace Hierarchy for Embodied Urban Navigation</a></td><td>45</td><td>6</td><td>Navigation</td><td>지도-언어-궤적 계층 도시 navigation임. 응용 범위가 특수함</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2611.03885'>Self-Consistent Neural Control: Learning Trajectories for Implicit Equilibrium</a></td><td>45</td><td>5</td><td>Robotics</td><td>implicit equilibrium 시스템 궤적 학습 제어임. 문제 설정은 흥미하나 범위 좁음</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2611.03944'>h-NESDF: An Infinitely Differentiable Signed Distance Between Two Sets with Robotic Applications</a></td><td>45</td><td>5</td><td>Robotics</td><td>미분 가능한 집합 간 signed distance임. 모션 플래닝용 도구임</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2611.04096'>Online Hamilton-Jacobi Reachability Onboard the Robot Control Loop: A Real-Time GPU Solver for Safety-Critical Autonomy</a></td><td>45</td><td>5</td><td>Control</td><td>HJ reachability 온라인 실시간 계산임. 안전 제어용 시스템 기여임</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2611.04371'>Embodied AI for Scientific Discovery: From Physical Action to Scientific Evidence</a></td><td>45</td><td>5</td><td>Embodied AI</td><td>과학 실험을 물리적으로 수행하는 embodied AI의 증거 흐름을 논한 관점 논문으로 방법론 기여는 약함</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2611.04173'>ReconDreamer#: Self-Evolving Closed-Loop Synergy of Reconstruction and Generation for Dynamic Driving Scenes</a></td><td>45</td><td>4</td><td>3D Vision</td><td>주행 장면 재구성과 생성을 닫힌 루프로 결합한 방법임</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2611.04838'>Found by Search, Broken by a Shortcut: Transfer and Tampering of Searched Intrinsic Rewards</a></td><td>45</td><td>4</td><td>RL</td><td>탐색된 intrinsic reward의 전이와 shortcut 취약성을 다루는 RL 분석임</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2611.05448'>Jev with Foresight: Safe Language-Guided Autonomous Driving via a Language World Model</a></td><td>45</td><td>4</td><td>Autonomous Driving</td><td>language world model 기반 안전 주행임. 주행 영역임</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2611.03862'>Dr. No: Feature Steering for Abstention in Vision-Language Models</a></td><td>45</td><td>3</td><td>Multimodal</td><td>VLM이 근거 부족 시 답하지 않도록 feature steering하는 방법으로 신뢰성 관점에서 embodied에 응용 가능함</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2611.03930'>What Is This Memory Useful For? Measuring Task-Conditioned Utility in Long-Term Agent Memory</a></td><td>45</td><td>2</td><td>NLP</td><td>장기 기억의 과제 조건부 유용성을 측정하는 연구로 memory 평가 관점이 있으나 대화 에이전트 대상임</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2611.04473'>Treating the Symptom, Missing the Cause: Anatomy of a Scientific Reasoning Failure</a></td><td>45</td><td>1</td><td>AI</td><td>과학 에이전트가 원인을 이해하지 못하고 개입만 찾는 실패를 분석한 연구로 causal 관점은 있으나 합성 환경 대상임</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2611.04054'>Forgetting to Improve: Principled Data Removal in Active Learning</a></td><td>44</td><td>1</td><td>LG</td><td>active learning에서 데이터 제거의 원리를 다룬 이론 연구로 일반성은 있으나 로봇과 거리가 멂</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2611.05344'>A Circuit for In-Context Learning</a></td><td>44</td><td>0</td><td>NLP</td><td>in-context learning 회로를 분석한 해석 연구로 흥미롭지만 로봇과 거리가 멂</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2611.04204'>Online iLQR-MPC with Whole-Body Control for Robust Humanoid Locomotion</a></td><td>42</td><td>5</td><td>Locomotion</td><td>iLQR-MPC 전신 제어 휴머노이드 보행임. 고전 제어 기반임</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2611.04452'>DynOSeg: Dynamic Object Segmentation via Motion-Geometry Fusion</a></td><td>42</td><td>4</td><td>CV</td><td>움직임과 기하를 융합한 동적 객체 분할임</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2611.05279'>Möbius: A Unified Motion-Language Model Bridging Understanding and Generation</a></td><td>42</td><td>3</td><td>Generative</td><td>인간 모션 이해, 생성, 편집을 통합한 모델로 휴머노이드 모션 활용 여지는 있으나 간접적임</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2611.04158'>On the Feature Evolution of Temporal Difference Learning</a></td><td>42</td><td>3</td><td>RL</td><td>TD learning의 feature 진화 이론 분석으로 RL 표현 학습과 연결됨</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2611.04031'>Language Model Augmented Decision Transformer for Multi-Task Offline Reinforcement Learning</a></td><td>42</td><td>3</td><td>RL</td><td>LM 증강 decision transformer로 multi-task offline RL함. 로봇 직접 평가는 불확실함</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2611.04764'>Pixel-space video generation with U-JiT</a></td><td>42</td><td>2</td><td>Video</td><td>latent 없이 pixel 공간에서 영상을 생성하는 U-JiT임</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2611.05266'>Stabilizing On-Policy Targeted Guidance in Agentic Reinforcement Learning</a></td><td>42</td><td>2</td><td>RL</td><td>agentic RL의 on-policy guidance 안정화임. LLM 대상이라 로봇 연결 약함</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2611.04061'>On the Primacy Bias in RLVR Training</a></td><td>42</td><td>1</td><td>RL</td><td>RLVR 학습의 primacy bias를 분석한 연구로 RL 관점은 있으나 LLM 추론 대상임</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2611.05234'>ARLoop: Fully-Open Pre-trained Looped Transformers with Attention Residuals</a></td><td>42</td><td>0</td><td>LG</td><td>looped transformer에 attention residual을 넣어 사전학습한 오픈 모델로 효율 연구이나 로봇과 거리가 멂</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2611.04279'>Bidirectional Centered Score Matching for Discrete Diffusion Distillation</a></td><td>42</td><td>0</td><td>Generative</td><td>discrete diffusion distillation의 score matching 목적 개선으로 생성 모델 방법론이나 로봇 연결은 약함</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2611.03825'>A Tutorial on Shape Servoing of Deformable Objects-Part II: Advanced Concepts</a></td><td>40</td><td>6</td><td>Manipulation</td><td>변형 물체 shape servoing 튜토리얼임. 새 방법보다 정리 성격임</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2611.03942'>Camera Radar LiDAR Fusion via Point-Cloud Projection for Multi-Task Learning</a></td><td>40</td><td>4</td><td>3D Vision</td><td>카메라 레이더 LiDAR 융합 멀티태스크 학습이나 자율주행 인식 위주임</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2611.04300'>CLOCs-R: Radar-Assisted Camera-LiDAR Fusion for Long-Range Object Detection</a></td><td>40</td><td>4</td><td>3D Vision</td><td>레이더를 더한 장거리 카메라 LiDAR 후보 수준 융합 검출임</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2611.04352'>ReSMap: Recasting Satellite Priors for Robust and Accurate Online HD Map Construction</a></td><td>40</td><td>4</td><td>3D Vision</td><td>위성 prior로 센서 고장에 강한 온라인 HD 맵을 만드는 방법임</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2611.03981'>Rapid Mean-Field Formation Transport with a Shared-Representation Neural Fokker-Planck Controller</a></td><td>40</td><td>4</td><td>Control</td><td>대규모 multi-agent 대형 이동을 Fokker-Planck controller로 빠르게 푸는 방법으로 swarm 제어에 해당함</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2611.03932'>CoReMatch: Recurrent Continuous Coordinate Refinement for Real-Time Robotic Feature Matching</a></td><td>40</td><td>4</td><td>3D Vision</td><td>실시간 feature matching 좌표 refinement임. 점진적 개선임</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2611.04491'>SPA-Q: Structure-Preserving Adaptive Post-Training Quantization for Monocular Depth Estimation</a></td><td>40</td><td>3</td><td>CV</td><td>단안 깊이 모델의 구조 보존 양자화로 효율 추론에 일부 관련됨</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2611.04710'>DenseTwins: Dense Modality Decoupling for Multimodal Self-Supervision</a></td><td>40</td><td>3</td><td>Multimodal</td><td>dense modality 분리 기반 멀티모달 self-supervision임</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2611.04309'>What Is the Influence of Task Order in Continual Learning? An Empirical Study and Order-Aware Evaluation for Motion Forecasting</a></td><td>40</td><td>3</td><td>LG</td><td>continual learning에서 task 순서 영향을 motion forecasting으로 평가하는 방법론임</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2611.04792'>Density-Aware Reward Scaling: A Reinforcement Learning Framework for Reward-Proportional Sampling</a></td><td>40</td><td>3</td><td>RL</td><td>reward 비례 샘플링을 위한 density-aware reward scaling으로 다양성 확보 RL 방법임</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2611.04216'>LiSA: Linear Stochastic Attention for Long-Range Visual Modeling</a></td><td>40</td><td>2</td><td>CV</td><td>선형 확률적 attention으로 긴 시퀀스 효율을 높이는 구조임</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2611.04472'>Beyond Token Representations: Explicit Visual Object Grounding for Video Reasoning Segmentation</a></td><td>40</td><td>2</td><td>Video</td><td>명시적 객체 grounding으로 영상 추론 분할을 개선함</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2611.04537'>BtsPruner: Role-Aware Visual Token Pruning for Large Vision-Language Models</a></td><td>40</td><td>2</td><td>Multimodal</td><td>역할 인식 visual token pruning으로 LVLM 효율을 높임</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2611.04728'>SPOD: Recovering Suppressed Temporal Evidence in Video-LLMs via Single-Pass Orthogonal Decomposition</a></td><td>40</td><td>2</td><td>Video</td><td>Video-LLM의 시간 환각을 직교 분해로 줄이는 기법임</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2611.05158'>Perturb, Repair, Verify: Self-Play Vision-Language Verifiers for Compositional Understanding</a></td><td>40</td><td>2</td><td>Multimodal</td><td>self-play로 VL verifier의 compositional 이해를 학습함</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2611.05359'>GSCV++: Lightweight 3D Gaussian Splatting Sequence Compression via Standard Video Codecs</a></td><td>40</td><td>2</td><td>3D Vision</td><td>3DGS 시퀀스를 표준 video codec으로 압축하는 공학적 기여로 로봇 직접성은 낮음</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2611.04142'>Interpretable Early Termination of Web Navigation Agents via Closed Sequential Pattern Mining</a></td><td>40</td><td>2</td><td>AI</td><td>web agent의 실패를 일찍 감지해 종료하는 방법으로 failure detection 관점이 있으나 웹 대상임</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2611.04948'>PATTS: Parallel-Aware Test-Time Scaling for Thought-Image Generation in Multimodal Discrete Diffusion LLMs</a></td><td>40</td><td>1</td><td>Generative</td><td>이산 diffusion LLM의 병렬 인식 test-time scaling임</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2611.04003'>WASP-Mem: Let Agent Organize Procedural Memory. Human Spend Effort on Diagnosis</a></td><td>40</td><td>1</td><td>NLP</td><td>enterprise 절차 기억을 에이전트가 정리하게 하는 procedural memory 시스템이나 LLM 에이전트 대상임</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2611.05345'>Adversarial Speculative Reasoning Improves Long Horizon Agents</a></td><td>40</td><td>1</td><td>AI</td><td>speculative decoding을 적대적 추론으로 바꿔 장기 에이전트를 개선하는 아이디어로 LLM 대상임</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2611.04887'>FourSight: Stable FP4 RL Post-Training via Sequence Filtering and Sparse Channel Compensation</a></td><td>40</td><td>0</td><td>RL</td><td>FP4 RL post-training 안정화로 효율 연구이나 LLM 대상임</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2611.04755'>iMED: A Multi-Endoscope Dataset for Surgical 3D Perception</a></td><td>38</td><td>5</td><td>3D Vision</td><td>로봇 수술용 다중 내시경 3D 인식 데이터셋임</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2611.04397'>Auditing Targetless Camera-LiDAR Extrinsic Correction before Recursive Use</a></td><td>38</td><td>4</td><td>3D Vision</td><td>카메라 LiDAR extrinsic 보정의 사용 전 감사 프로토콜 연구임</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2611.04583'>Multi-Path Mamba Diffusion for 3D Point Cloud Semantic Scene Completion</a></td><td>38</td><td>4</td><td>3D Vision</td><td>Mamba diffusion을 이용한 3D semantic scene completion임</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2611.04759'>Beyond Local Refinement: Wide-Area Precise Cross-View Localization</a></td><td>38</td><td>4</td><td>3D Vision</td><td>광역 cross-view 정밀 위치 추정 방법임</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2611.03952'>Do We Still Need Rotation-Invariant Architectures? A Statistical Robustness Benchmark for Point Cloud Classification</a></td><td>38</td><td>3</td><td>3D Vision</td><td>회전 불변 point cloud 구조의 필요성을 통계적으로 비교한 벤치마크임</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2611.04358'>EndoS3:Endoscopic Semantic Splatting SLAM</a></td><td>38</td><td>3</td><td>3D Vision</td><td>내시경 의미 Gaussian SLAM으로 수술 도메인 한정임</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2611.04062'>StreamLTT: Risk Certification for Policy Selection under Stream Dependence</a></td><td>38</td><td>3</td><td>LG</td><td>policy 선택의 risk 인증을 stream 의존성 하에서 다루는 conformal 계열 연구임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2611.05275'>Route Anything: A Study of Model and Policy Routing for General-Purpose AI Systems</a></td><td>38</td><td>2</td><td>Multimodal</td><td>모델과 policy를 라우팅하는 연구로 범용 시스템 관점은 있으나 로봇 직접성은 낮음</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2611.05036'>ToolSpace: Scaling Tool-Centric Environment Synthesis for Long-Horizon Agents</a></td><td>38</td><td>2</td><td>NLP</td><td>tool 환경 합성으로 long-horizon agent를 학습함. 로봇 연결 약함</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2611.04487'>Reconstruction-Based Diagnosis through Gödel-Regularized Virtual Observability</a></td><td>38</td><td>2</td><td>LG</td><td>센서 없는 부품의 고장을 복원 기반으로 진단하는 방법으로 diagnosis 관련이나 산업 시스템 대상임</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2611.04438'>Entropy-Gated Dynamic Rectification for Object Hallucination in Large Vision-Language Models</a></td><td>38</td><td>1</td><td>Multimodal</td><td>엔트로피 게이트로 LVLM 객체 환각을 줄이는 기법임</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2611.03962'>Sampling Interventional Distributions with Orthogonal MMD Flow</a></td><td>38</td><td>1</td><td>LG</td><td>interventional 분포 샘플링을 MMD flow로 수행하는 인과 추론 연구로 causal reasoning과 약하게 연결됨</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2611.05263'>JHiMA-WebRL: A Joint Hierarchical Multi-Agent Reinforcement Learning Framework for Long-Horizon Web Tasks</a></td><td>38</td><td>1</td><td>RL</td><td>멀티모달 web agent용 계층 multi-agent RL로 GUI 대상이며 로봇과 거리가 멂</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2611.05450'>Towards Robust Long-Lived Agents: Benchmarking Experience Lifecycles in Evolving Environments</a></td><td>38</td><td>1</td><td>AI</td><td>진화하는 환경에서 에이전트의 경험 수명 주기를 평가하는 benchmark로 memory 관점은 있으나 LLM 대상임</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2611.05287'>Knowingly Wrong: Training LLMs Against Their Own Beliefs can Induce Misalignment</a></td><td>38</td><td>0</td><td>NLP</td><td>자기 믿음에 반하는 학습이 misalignment를 유발하는지 보인 안전성 연구로 로봇과 무관함</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2611.04395'>Correct Labels Are Not Enough: Reliable Metadata Can Silently Control Model Behavior</a></td><td>38</td><td>0</td><td>NLP</td><td>신뢰할 수 있는 metadata가 모델 행동을 조용히 지배함을 보인 분석 연구임</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2611.04757'>When Should an LLM Steering Edit Depend on the Input?</a></td><td>38</td><td>0</td><td>NLP</td><td>activation steering 편집이 입력에 의존해야 하는 조건을 이론화한 연구임</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2611.04834'>Feeling of Knowing in Large Language Models</a></td><td>38</td><td>0</td><td>NLP</td><td>post-training 후 LLM의 답변 가능성 판단 정렬을 보는 분석임</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2611.03953'>P$^2$-MOPD: Accelerating Multi-Teacher On-Policy Distillation via Parameter Priors</a></td><td>37</td><td>0</td><td>NLP</td><td>multi-teacher on-policy distillation 가속 방법으로 LLM 대상임</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2611.04034'>Do Pretrained Backbones Transfer to Physical Sensors? A Systematic Study of Multimodal Initialization Across the Sensor Stack</a></td><td>36</td><td>3</td><td>CV</td><td>사전학습 backbone의 물리 센서 전이를 실험적으로 비교한 연구임</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2611.03849'>LaplaceDiag: Fault Diagnosis through Changes in Learned Actuator Effects</a></td><td>36</td><td>2</td><td>LG</td><td>actuator 효과 변화로 고장을 진단하는 방법으로 fault diagnosis 관련이나 플랜트 대상임</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2611.05451'>From Tokens to Trajectories: Parameter-Efficient Continuous Adaptation of Unified Multimodal Models</a></td><td>36</td><td>1</td><td>Multimodal</td><td>unified multimodal model의 연속 표현 parameter-efficient 적응으로 로봇 연결은 약함</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2611.05278'>Beyond Accuracy: What Language-Subspace Interventions Capture, Remove, and Improve</a></td><td>36</td><td>0</td><td>NLP</td><td>다국어 추론에서 language-subspace 개입의 효과를 분석한 해석 연구로 로봇과 무관함</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2611.05358'>Suppressing Misaligned Behaviors in Language Models, Durably</a></td><td>36</td><td>0</td><td>NLP</td><td>오정렬 행동을 오래 억제하는 학습 방법 연구로 로봇과 무관함</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2611.04055'>HybridSpec: Throughput-Aware Speculative Decoding for Hybrid GDN-MoE Models</a></td><td>36</td><td>0</td><td>LG</td><td>하이브리드 GDN-MoE 모델용 speculative decoding 처리량 최적화로 시스템 엔지니어링 성격임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2611.04479'>A Parametric Linear Conic Projection for Structured Sparse Attention</a></td><td>36</td><td>0</td><td>LG</td><td>sparse attention용 conic projection 측정 지표 제안으로 이론적이나 로봇과 거리가 멂</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2611.04814'>Think Less, Locally: Local Preference Learning for Reasoning Compression</a></td><td>36</td><td>0</td><td>NLP</td><td>추론 압축을 위한 local preference learning으로 incremental함</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2611.03936'>Geometric Refinement and Distributional Alignment for Sim2Real Roadside LiDAR Detection</a></td><td>35</td><td>4</td><td>3D Vision</td><td>합성 데이터만으로 도로변 LiDAR 검출을 푸는 챌린지 참가 기술 보고임</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2611.04334'>RAIPAL: A Powerful and Agile Humanoid Arm for Human Tasks</a></td><td>35</td><td>4</td><td>Hardware</td><td>휴머노이드 팔 하드웨어 설계임. 학습 기여 없음</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2611.04518'>LLM-Assisted Planning with Distributed Onboard Behaviour Tree Execution for Multi-AUV Missions</a></td><td>35</td><td>4</td><td>Multi-Robot</td><td>LLM 보조 AUV 계획과 behaviour tree임. 응용 시스템 성격임</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2611.04374'>IGSW: Multi-Weather Urban Scene Reconstruction with Intrinsic-Decoupled Gaussian Splatting</a></td><td>35</td><td>3</td><td>3D Vision</td><td>날씨 편집용 Gaussian 도시 장면 재구성임</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2611.04591'>SparseGraph-I2P: Consistency-Guided Hypothesis Selection for Efficient Image-to-Point-Cloud Registration</a></td><td>35</td><td>3</td><td>3D Vision</td><td>일관성 기반 가설 선택의 image-to-point-cloud 정합임</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2611.04072'>Finite-Sample Convergence in Networked Average Reward MARL: Decentralization Pitfalls and Entropy Remedies</a></td><td>35</td><td>3</td><td>RL</td><td>네트워크형 MARL의 유한 표본 수렴 이론임</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2611.04774'>Cooperative Multi-Agent Reinforcement Learning with Submodular Trajectory Rewards</a></td><td>35</td><td>3</td><td>RL</td><td>submodular trajectory reward를 갖는 협력 MARL 이론임</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2611.04957'>Safeguarding Multi-Agent Reinforcement Learning for Connected and Automated Vehicles with Recursively Feasible Control Barrier Functions</a></td><td>35</td><td>3</td><td>RL</td><td>CAV용 안전 MARL임. 로봇 학습 연결 약함</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2611.03916'>When Latent Dynamics Meet Data Assimilation: A Benchmark of Koopman-Type Representations</a></td><td>35</td><td>2</td><td>LG</td><td>Koopman 표현의 data assimilation benchmark로 동역학 모델링과 약하게 연결됨</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2611.05439'>Learning Implicit Solves for Dynamic Simulations</a></td><td>35</td><td>2</td><td>LG</td><td>동역학 시뮬레이션용 implicit solve 학습임. 물리 시뮬레이션 쪽 간접 관련임</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2611.04867'>One Assistant, Many Memories: Benchmarking Real-World Group Assistance When Recall Is Not Enough</a></td><td>35</td><td>2</td><td>NLP</td><td>그룹 어시스턴트 memory 활용 벤치마크임. memory 주제이나 대화 한정임</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2611.04489'>Bridging CLIP with DINO: Cross-Modal Information Maximization for Online Test-Time Adaptation</a></td><td>35</td><td>1</td><td>CV</td><td>CLIP과 DINO를 이용한 online test-time adaptation임</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2611.05066'>VIGOR: Visual Gain Ordering for Hallucination Mitigation in Multimodal Discrete Diffusion Language Models</a></td><td>35</td><td>1</td><td>Multimodal</td><td>이산 diffusion VLM의 환각을 순서 조정으로 줄임</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2611.04663'>Best-of-Depth: Learning Exploratory Dynamics in Looped Transformers</a></td><td>35</td><td>1</td><td>NLP</td><td>looped transformer가 중간 깊이에서 대안을 탐색하도록 학습함</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2611.04689'>Uncertainty-Aware Prototype Learning for Open-Set Test-Time Adaptation</a></td><td>35</td><td>1</td><td>CV</td><td>open-set test-time adaptation의 불확실성 prototype 학습으로 TTA 계열임</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2611.04787'>ReSI-Math: Exploring Recoverable Capability Frontiers for Efficient Reasoning Improvement</a></td><td>35</td><td>1</td><td>NLP</td><td>RLVR 수학 추론 효율 개선임. 로봇 연결 약함</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2611.04277'>Harness-S: Learning from Sibling Harnesses for Generalizable Agent Training</a></td><td>35</td><td>1</td><td>AI</td><td>에이전트 harness 변형들에서 배우는 학습 방식으로 LLM 에이전트 대상 incremental 연구임</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2611.04817'>The Pen is Mightier than the Pixel: Natural Textual Unlearnable Example for Large Vision Language Models</a></td><td>35</td><td>1</td><td>Multimodal</td><td>LVLM에 대한 텍스트 기반 unlearnable example 연구로 보안 성격임</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2611.04952'>Artifact-to-Capability: Diagnosing Breaks in Capability Formation of Self-Evolving Agents in a Controlled Environment</a></td><td>35</td><td>1</td><td>AI</td><td>self-evolving agent의 capability 형성 단절을 진단하는 분석임</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2611.05139'>Meta$^2$: Precomputing Reusable Knowledge for Online Harness Evolution in Long-Horizon Agents</a></td><td>35</td><td>1</td><td>AI</td><td>장기 에이전트 harness 진화를 위한 지식 사전계산으로 LLM 에이전트 대상임</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2611.05255'>Going Deeper With Memories</a></td><td>35</td><td>0</td><td>NLP</td><td>byte level LM의 memory 구조 개선임. 로보틱스 연결 없음</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2611.05304'>LoopVQ: Sub 1-bit KV Cache Quantization for Looped Transformers</a></td><td>35</td><td>0</td><td>NLP</td><td>looped transformer KV cache 양자화임. 효율화지만 로봇 연결 없음</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2611.03998'>Dory1.0-4B: A Looped Normalized-GPT</a></td><td>35</td><td>0</td><td>NLP</td><td>looped 4B 언어 모델 공개임. 로봇 연결 없음</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2611.03834'>Low-Rank Hierarchical Merging for Efficient Long-to-Short Reasoning</a></td><td>35</td><td>0</td><td>NLP</td><td>long-to-short 추론 모델 병합을 low-rank로 하는 incremental 연구임</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2611.04399'>Silent Instrument Errors Reorder Agent Leaderboards</a></td><td>35</td><td>0</td><td>AI</td><td>계측 오류가 agent 리더보드 순위를 바꾼다는 평가 방법론 지적임</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2611.04556'>Inter-Agent Influence: Evaluating Persuasion, Deception, and Coercion in Multi-Agent Systems</a></td><td>35</td><td>0</td><td>AI</td><td>multi-agent 간 설득, 기만, 강압을 평가한 안전성 benchmark임</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2611.04805'>Where Is the Truth When AI Agents Disagree? Dependence-Aware Belief Propagation for Unsupervised Truth Discovery (Extended Version)</a></td><td>35</td><td>0</td><td>AI</td><td>상관된 LLM 에이전트 답변을 의존성 고려 belief propagation으로 합치는 방법임</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2611.05108'>From AutoResearch to Continual AutoResearch: Do Agents Learn Across Tasks?</a></td><td>35</td><td>0</td><td>AI</td><td>autoresearch 에이전트가 과제 간 학습하는지 보는 평가 연구임</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2611.05272'>The Geometry of Ignorance: Detecting Suppressed Knowledge in LLMs through Activation Fragmentation</a></td><td>35</td><td>0</td><td>NLP</td><td>활성화 기하로 LLM의 억제된 지식을 검출하는 해석 연구임</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2611.04262'>Sketch-Omni: Instance-Level Sketch-Based Visual Prompting for Perception MLLMs</a></td><td>34</td><td>2</td><td>Multimodal</td><td>스케치 prompt 기반 perception MLLM임</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2611.05280'>YANAMI: A Large-Scale Multimodal Dataset and Benchmark for Multiturn Stateful Interaction</a></td><td>34</td><td>1</td><td>Multimodal</td><td>멀티턴 상태 유지 상호작용 dataset과 benchmark로 로봇 연결은 약함</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2611.05166'>When Self-Verification Hurts: Calibrated Answer Repair for Financial Question Answering</a></td><td>34</td><td>0</td><td>NLP</td><td>금융 QA에서 self-verification이 오히려 해가 되는 현상을 보정해 고치는 방식으로 로봇과 무관한 응용 연구임</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2611.04035'>Recursa: Toward Recursively Self-Improving Foundation Model Systems</a></td><td>34</td><td>0</td><td>AI</td><td>새 도메인 지식을 흡수하는 self-improving foundation model 시스템으로 개념 수준이며 로봇과 무관함</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2611.04260'>Neologism Inoculation Prompting</a></td><td>34</td><td>0</td><td>NLP</td><td>inoculation prompting 변형으로 reward hacking을 줄이려는 안전성 연구임</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2611.03940'>Coordinate Frame Recovery, Per Class NMS and Null Return Modelling for Sim2Real V2X LiDAR Detection</a></td><td>33</td><td>4</td><td>3D Vision</td><td>V2X LiDAR sim2real 챌린지용 좌표계 복원과 NMS 튜닝 위주 보고임</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2611.04305'>Weather Adaptive Autonomous Driving</a></td><td>33</td><td>3</td><td>CV</td><td>악천후 주행 검출기의 conformal 임계값 설정 연구임</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2611.05361'>Visibility-Aware Reference Generation for Benchmarking Visual 3D Reconstruction in Vegetation-Rich Environments</a></td><td>33</td><td>2</td><td>3D Vision</td><td>식생 환경 3D 재구성 평가용 reference 생성으로 benchmark 성격임</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2611.04894'>VisSearch-Bench: Evaluating Long Horizon Visual Search in Multimodal Agents</a></td><td>33</td><td>1</td><td>Multimodal</td><td>멀티모달 agent의 장기 시각 검색 벤치마크임</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2611.03876'>Embedding Semantic Entropy: NLI-Free Semantic Uncertainty Estimation with Geometry-Aware Clustering</a></td><td>33</td><td>0</td><td>NLP</td><td>LLM 불확실성 추정을 NLI 없이 embedding 기하로 수행함</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2611.04079'>AlgoPilot: Cross-Paradigm Reasoning in Language Models via Strategy Selection and Guidance</a></td><td>33</td><td>0</td><td>NLP</td><td>전략 선택으로 패러다임 간 추론을 하는 LLM 방법으로 incremental함</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2611.04181'>Clocks all the way down: does sequence-processing AI need endogenous temporal structure?</a></td><td>33</td><td>0</td><td>LG</td><td>시퀀스 모델에 내생적 시간 상태가 필요한지 논하는 입장 논문으로 실험 근거가 약함</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2611.04323'>FP4Quant: Efficient 4-Bit Communication Compression for Model-Parallel LLM Training</a></td><td>33</td><td>0</td><td>LG</td><td>모델 병렬 학습의 4-bit 통신 압축으로 시스템 최적화이며 로봇과 무관함</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2611.04782'>Reducing Logprob Without Causal Verification: Diagnosing SAE-Based PII Suppression in LLMs</a></td><td>33</td><td>0</td><td>NLP</td><td>SAE 기반 PII 억제가 인과 검증 없이 평가됨을 지적한 분석임</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2611.05097'>The Platonic Brain: Representational Convergence in EEG Foundation Models</a></td><td>33</td><td>0</td><td>LG</td><td>EEG foundation model의 표현 수렴을 보는 분석으로 로봇과 무관함</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2611.04084'>From Visual Matching to Textual Conditioning: Cross-Domain Few-Shot Segmentation via Reference Inversion</a></td><td>32</td><td>2</td><td>CV</td><td>SAM3 텍스트 조건을 이용한 cross-domain few-shot 분할 개선임</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2611.04554'>SEEK-VAU: Towards Evidence-Faithful Video Anomaly Understanding via Agentic Search</a></td><td>32</td><td>2</td><td>Video</td><td>agentic 검색으로 영상 이상 이해의 근거 충실성을 높임</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2611.05083'>Manifold Embedding of Deep Image Features for Image Matching via Neural Adjoint Maps</a></td><td>32</td><td>2</td><td>CV</td><td>manifold 임베딩으로 의미 대응을 추정함</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2611.09997'>SurvAD: How Anomalies Survive Diffusion Reconstruction</a></td><td>32</td><td>1</td><td>Generative</td><td>diffusion 복원 기반 이상 탐지에서 이상이 남는 정도를 이론적으로 분석함</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2611.04497'>SKILL2STEER: One-Pass Hypernetwork for Mapping Natural-Language Skills to Low-Rank Post-Block Activation Shifts</a></td><td>32</td><td>1</td><td>NLP</td><td>자연어 skill을 activation shift로 매핑하는 hypernetwork로 agent skill 관점은 있으나 LLM 대상임</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2611.04931'>Modulating Merging Strengths via Joint Loss Estimation for LoRA-based Continual Learning</a></td><td>32</td><td>1</td><td>LG</td><td>LoRA continual learning merge 강도 조절임</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2611.05147'>GM League Arena: An Interactive Long-Horizon Task Benchmark Based on Professional Sports League Management</a></td><td>32</td><td>1</td><td>NLP</td><td>프로 스포츠 운영 long-horizon 벤치마크임. 로봇 연결 약함</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2611.04413'>CaliSplat: Sparse Gaussian Fitting and Calibrated Rate Allocation for Image Compression</a></td><td>32</td><td>1</td><td>CV</td><td>2D Gaussian 이미지 압축의 rate 할당 개선으로 3DGS가 아닌 압축 응용임</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2611.03992'>FlagRot: Selective Rotation for Low-Bit KV Caches</a></td><td>32</td><td>0</td><td>NLP</td><td>저비트 KV cache 회전 기법임. 로봇 연결 없음</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2611.04152'>PACT: Certifying What Is Written in Parallel Decoding of Diffusion Language Models</a></td><td>32</td><td>0</td><td>NLP</td><td>diffusion LM 병렬 디코딩 인증임. 효율 주제이나 로봇 연결 없음</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2611.04958'>Shuffled OPSD: When Semantic Consistency Hurts On-Policy Self-Distillation?</a></td><td>32</td><td>0</td><td>NLP</td><td>on-policy self-distillation 분석임. 로봇 연결 없음</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2611.04315'>Drift No More: Spectral Locking for Long-Horizon Open-Weight Multi-Agent AI</a></td><td>32</td><td>0</td><td>AI</td><td>multi-agent 장기 drift를 spectral locking으로 막는 방법으로 근거가 약함</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2611.04848'>Amortized Nonlinear Variable Selection with Prior-Data Fitted Networks</a></td><td>32</td><td>0</td><td>LG</td><td>PFN 기반 비선형 변수 선택으로 로봇과 거리가 멂</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2611.04255'>ActOR: Ambient AI-Based Agentic Orchestration for Humanoid Autonomy in Operating Rooms</a></td><td>30</td><td>4</td><td>Embodied AI</td><td>수술실 휴머노이드 agentic 오케스트레이션임. 응용 시스템 성격임</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2611.04176'>Grasping and Stabilizing Tumbling Objects with Rotating-Base Multi-Arm Space Manipulators</a></td><td>30</td><td>3</td><td>Space Robotics</td><td>우주 매니퓰레이터 tumbling 물체 포획 제어임. 학습 요소 약함</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2611.05027'>Haptic Shared Control for Multi-Robot Systems</a></td><td>30</td><td>3</td><td>HRI</td><td>다중 로봇 haptic shared control임. 학습 요소 약함</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2611.04102'>Is This 3D Asset Usable? Beyond the Beauty Render for Asset Curation</a></td><td>30</td><td>2</td><td>3D Vision</td><td>3D asset 재사용 가능성 평가 벤치마크로 시뮬레이션 데이터 구축에 일부 쓰임</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2611.04414'>SphereFlow: Missing Modality Imputation via Geometric Transport on Hypersphere</a></td><td>30</td><td>2</td><td>Multimodal</td><td>초구면 transport로 결측 modality를 보간하는 방법임</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2611.05205'>TAQ-MOTR: Tracking-Aware Detection Query Formation for End-to-End Multiple Object Tracking</a></td><td>30</td><td>2</td><td>CV</td><td>tracking 인식 query를 쓰는 end-to-end 다중 객체 추적임</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2611.04458'>Large Language Model-Assisted Adaptive Heuristic Search for Agile Earth Observation Satellite Scheduling</a></td><td>30</td><td>2</td><td>AI</td><td>LLM 보조 휴리스틱으로 지구 관측 위성 임무를 스케줄링하는 최적화 응용임</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2611.04087'>ScienceVision: Can AI Observe and Reason Like a Scientist?</a></td><td>30</td><td>1</td><td>Multimodal</td><td>과학용 3D 데이터 멀티모달 추론 벤치마크로 로봇과 거리가 있음</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2611.04112'>Co-Occurrence Priors Override Visual Spatial Evidence: Understanding False Alarms in Vision-Language Models for Construction Struck-By Hazard Detection</a></td><td>30</td><td>1</td><td>Multimodal</td><td>건설 위험 검출에서 VLM의 오경보 원인을 분석한 연구임</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2611.04286'>GroundSeek-CXR: Retrospective Evaluation-Guided Active Observation Framework for Multi-Label Chest Radiography Diagnosis</a></td><td>30</td><td>1</td><td>Multimodal</td><td>흉부 X선 진단용 능동 관찰 프레임워크로 도메인이 의료임</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2611.04418'>VidUEU-Agent: A Data-Curation Agent for Multimodal Understanding, Editing, and Unified Tasks</a></td><td>30</td><td>1</td><td>Multimodal</td><td>영상에서 instruction 데이터를 만드는 data curation agent임</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2611.04903'>Heads That Write, Not Just Point: Image Retrieval Heads in Vision-Language Models</a></td><td>30</td><td>1</td><td>Multimodal</td><td>VLM의 이미지 retrieval head를 분석한 연구임</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2611.05286'>Anchored Rank-Adversarial Fine-Tuning Pretrained Visual Place Recognition Models</a></td><td>30</td><td>1</td><td>CV</td><td>visual place recognition의 adversarial 강건성 fine-tuning으로 navigation과 간접 연결됨</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2611.05449'>SO(3)-Equivariant Learning on CAD Boundary Representations</a></td><td>30</td><td>1</td><td>3D Vision</td><td>CAD B-rep의 SO(3) equivariant 학습으로 로봇 관련성은 낮음</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2611.04760'>Koopman Generative Operators for Efficient Probabilistic Time-Series Forecasting</a></td><td>30</td><td>1</td><td>LG</td><td>Koopman generative operator 확률적 시계열 예측임</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2611.04885'>DLER: Dual-Logit Experience Replay for Online Continual Learning</a></td><td>30</td><td>1</td><td>LG</td><td>online continual learning의 dual-logit replay임</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2611.04480'>ReListen: Training-Free Evidence Localization in Hour-Long Audio with Frozen Audio Language Models</a></td><td>30</td><td>1</td><td>Multimodal</td><td>시간 단위 오디오 근거 위치 추정임. 로봇 연결 약함</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2611.04313'>Coarse Semantic Blocks for Efficient Training-Free Sparse Attention</a></td><td>30</td><td>0</td><td>NLP</td><td>training-free sparse attention으로 LLM 추론 가속임</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2611.04327'>Anchor: Augmented Cross-Layer Recurrent State for Long-Context Retrieval in Test-Time Training</a></td><td>30</td><td>0</td><td>NLP</td><td>TTT 선형화 모델의 장문 검색 개선임</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2611.04632'>Self-Privileged Fine-Tuning</a></td><td>30</td><td>0</td><td>NLP</td><td>privileged 정보를 이용한 SFT 개선임</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2611.05184'>Provably Learning Mixtures of Linear Experts</a></td><td>30</td><td>0</td><td>LG</td><td>Mixture of linear experts 수렴 보장 이론임. 로보틱스와 거리 멂</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2611.03852'>Why Pay for Long Reasoning When Rewrite Do Trick? Causal Effects of Reasoning History Compaction on Future Generation and Agent Cost</a></td><td>30</td><td>0</td><td>NLP</td><td>reasoning 길이를 rewrite로 줄이는 인과 분석임. 로봇 연결 약함</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2611.04169'>Length Is Cheap, Competition Is Not: Attention Predicts Context Rot in Retrieval</a></td><td>30</td><td>0</td><td>NLP</td><td>context rot의 attention 원인 분석임. 로봇 연결 없음</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2611.04349'>Sparse Internal Control of Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>LM sparse 내부 제어임. 로봇 연결 없음</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2611.03832'>El Agente Fármaco: A Scalable AI Scientist for Drug Discovery</a></td><td>30</td><td>0</td><td>LG</td><td>약물 탐색용 AI scientist 에이전트 시스템으로 로봇과 무관한 응용임</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2611.04059'>Query-based Submodular Data Selection for Efficient Instruction Tuning</a></td><td>30</td><td>0</td><td>NLP</td><td>instruction tuning용 submodular 데이터 선택으로 incremental한 연구임</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2611.04301'>OSGR: Observation-Support Graph Reasoning for Earth Observation Question Answering</a></td><td>30</td><td>0</td><td>CV</td><td>지구 관측 질의응답용 그래프 추론으로 원격탐사 응용임</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2611.04321'>ATC: Agent Trajectory Control for Role-Contract Enforcement in Black-Box Multi-Agent Systems</a></td><td>30</td><td>0</td><td>AI</td><td>multi-agent 역할 계약 강제 제어 방법으로 LLM 시스템 엔지니어링임</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2611.04420'>Verifier strength does not buy discovery quality: a pre-registered two-domain test of LLM-based automated research, with post-hoc evidence pointing to proposer-pool composition</a></td><td>30</td><td>0</td><td>AI</td><td>검증기 강도가 발견 품질을 높이지 않는다는 사전등록 실험임</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2611.04841'>DGC-Net: Cross-Modal Dynamic Routing with Global-Guided Compensation in Multimodal Sentiment Analysis</a></td><td>30</td><td>0</td><td>Multimodal</td><td>사용자 영상 감성 분석의 cross-modal routing으로 benchmark 개선 성격임</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2611.05039'>ALBI: LLM-Guided Inductive Logic Programming via Iterative Generate-Test-Constrain Refineme</a></td><td>30</td><td>0</td><td>AI</td><td>LLM 기반 귀납 논리 프로그래밍 프레임워크로 incremental함</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2611.05167'>Learning Behaviorally Relevant Dynamics in Multimodal Neural Recordings</a></td><td>30</td><td>0</td><td>LG</td><td>신경 기록에서 행동 관련 동역학을 학습하는 신경과학 방법임</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2611.05306'>You don&#x27;t need long context</a></td><td>30</td><td>0</td><td>NLP</td><td>긴 context가 필요 없다는 주장으로 비용 분석 성격임</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2611.04822'>Radial distortion homography estimation from affine-covariant or orientation-covariant features</a></td><td>28</td><td>2</td><td>3D Vision</td><td>방사 왜곡 homography 최소 solver 제안임</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2611.04386'>StepX-OPD: Rethinking Multi-Teacher On-Policy Distillation in Diffusion Models</a></td><td>28</td><td>1</td><td>Generative</td><td>다중 teacher on-policy distillation으로 few-step 이미지 diffusion을 개선함</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2611.04916'>Behind Video Generation: Observations and Insights on Multimodal Understanding from Kling</a></td><td>28</td><td>1</td><td>Video</td><td>Kling 영상 생성 관찰 보고서임</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2611.03868'>EvoGroup: A Self-Evolving Harness for Group Agents in Shared Contexts</a></td><td>28</td><td>1</td><td>NLP</td><td>group agent 자기 진화 harness임. 로봇 연결 약함</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2611.04507'>Signals: Continuous Diagnostics of AI Agents</a></td><td>28</td><td>1</td><td>AI</td><td>AI 에이전트 지속 진단용 신호 체계로 엔지니어링 성격임</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2611.04268'>Weight-Space Programming for Improving Image-Restoration Diffusion Models: Technical Conjectures and a Recursive Improvement Loop</a></td><td>28</td><td>0</td><td>LG</td><td>LLM이 diffusion 복원 모델 가중치를 직접 수정하는 추측성 제안임</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2611.04085'>Follow the Features: SAE Feature-Guided Data-Efficient Instruction-Tuning of Large Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>SAE feature로 instruction tuning 데이터 선택함</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2611.04108'>Separating Common and Unique Directions for Model Merging</a></td><td>28</td><td>0</td><td>LG</td><td>model merging에서 공통과 고유 방향 분리함</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2611.04902'>Attending to Memory Writes Reduces Seed Variability in Recurrent Length Generalization</a></td><td>28</td><td>0</td><td>LG</td><td>recurrent memory 길이 일반화의 seed 변동 분석임</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2611.05207'>Multi-Objective Generative Optimization via Expected Hypervolume Fine-Tuning</a></td><td>28</td><td>0</td><td>LG</td><td>다목적 생성 최적화 fine-tuning임. 과학 설계용이라 로보틱스 연결 약함</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2611.04107'>Say Less, Mean Better: Training-Free Verbosity Control for Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>학습 없는 verbosity 제어임. 로봇 연결 없음</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2611.04141'>Where Do Distilled Students Store Thinking?</a></td><td>28</td><td>0</td><td>NLP</td><td>distilled student의 reasoning 저장 위치 분석임. 로봇 연결 없음</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2611.05033'>Whose Effect Is It? How Objectives Inflate Learned Subspace Interventions</a></td><td>28</td><td>0</td><td>NLP</td><td>subspace intervention 해석 편향 분석임. 로봇 연결 없음</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2611.05292'>Personas Are Not People: Identity as State, Not Attribute</a></td><td>28</td><td>0</td><td>NLP</td><td>합성 페르소나를 상태로 봐야 한다는 입장 논문으로 실험 근거가 약하고 로봇과 무관함</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2611.03980'>Measuring Model-Specific Alignment Drift in LLM-Based Opinion Dynamics</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM 의견 동역학 실험에서 모델별 drift를 재는 사회 시뮬레이션 연구임</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2611.04180'>Validation-Gated ML Pipeline Synthesis with Expert-Grounded Self-Evolving Skills</a></td><td>28</td><td>0</td><td>AI</td><td>ML 파이프라인 자동 합성 에이전트로 AutoML 응용임</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2611.04320'>Planning-Coding Separation in LLM-Based Code Generation: An Empirical Study</a></td><td>28</td><td>0</td><td>NLP</td><td>코드 생성에서 planning과 coding 분리 효과를 본 실증 연구임</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2611.04380'>Twice as Fast, Until It Isn&#x27;t: Quantized Serving of Mid-Size Open LLMs</a></td><td>28</td><td>0</td><td>LG</td><td>중형 LLM 양자화 서빙 비교 측정 연구로 로봇과 무관함</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2611.04879'>ScamWorld: An Interactive Environment for Evaluating Web Agents Against Online Fraud</a></td><td>28</td><td>0</td><td>AI</td><td>web agent 사기 취약성 평가 환경으로 로봇과 무관함</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2611.05291'>Low-Density 3D Point Cloud Classification</a></td><td>27</td><td>1</td><td>3D Vision</td><td>저밀도 point cloud 분류로 incremental한 성격임</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2611.05041'>Positional Encoding is All You Need for Scalable Equivariance Constraint Relaxation</a></td><td>27</td><td>1</td><td>LG</td><td>positional encoding으로 equivariance 제약 완화함</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2611.04043'>Denoising Is Stein: Moment Access and a Resource Hierarchy for Learning Hidden Structure in Diffusion Models</a></td><td>27</td><td>0</td><td>Generative</td><td>diffusion의 hidden 구조 학습 자원 이론임</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2611.04063'>TB-Transolver: Parallelized and Coherent Long-Horizon Rollouts via Temporal Bundling for Time-Dependent PDEs</a></td><td>27</td><td>0</td><td>LG</td><td>PDE용 Transolver의 temporal bundling임</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2611.04098'>When Strong Reasoners Join the Pool: Small Union Premiums and Costly Runaway Generations in LLM Routing</a></td><td>27</td><td>0</td><td>NLP</td><td>LLM 라우팅 평가 oracle 문제 분석임</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2611.04106'>Structure, Dimensionality, and Distribution Shape - What Makes Pretraining Data Transferable, and Why the Input Pipeline Decides Which</a></td><td>27</td><td>0</td><td>LG</td><td>pretraining 데이터 전이성 원리 연구임</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2611.04137'>LoopKV: Loop-Aware KV Cache Compression for Serving Looped Transformers</a></td><td>27</td><td>0</td><td>NLP</td><td>looped transformer KV cache 압축임</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2611.04239'>LIRA: A More Interpretable Dynamic Loss-Informed Rank Allocation for Low-Rank Adaptation</a></td><td>27</td><td>0</td><td>LG</td><td>동적 rank 할당 LoRA로 incremental함</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2611.04376'>Aligning Training and Rollout Policies for End-to-End FP4 RL on Mixture-of-Experts LLMs</a></td><td>27</td><td>0</td><td>NLP</td><td>MoE LLM의 FP4 RL 정합 문제임</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2611.04657'>Exploiting Biases in Attention for Transformers</a></td><td>27</td><td>0</td><td>CV</td><td>ViT attention 편향 활용 효율화임</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2611.04797'>Training Specialist LLMs on Your Phone: Forward-Only Optimization via Block-Spectral Coordinates</a></td><td>27</td><td>0</td><td>NLP</td><td>휴대폰에서 forward-only로 LLM 학습함</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2611.05003'>Unifying and Beyond the Theory of Pervasive Capability Degradation in LLM Post-training SFT from Feature Interference</a></td><td>27</td><td>0</td><td>NLP</td><td>SFT 능력 저하 이론임</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2611.05195'>Ensembles of Random Partition-Based Models under Covariate Shift</a></td><td>27</td><td>0</td><td>LG</td><td>covariate shift 하 ensemble 분석임. 이론 중심이고 로보틱스 연결 약함</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2611.04481'>Goal-Driven Autonomous Optical Experimentation via a Self-Recursive Hardware-Software Harness</a></td><td>26</td><td>1</td><td>AI</td><td>광학 실험을 자율 수행하는 에이전트로 응용 사례 보고 성격임</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2611.04032'>ROCm InferaSim: Cut LLM Serving Trial Costs and Deploy the Best Configuration</a></td><td>26</td><td>0</td><td>LG</td><td>LLM 서빙 설정을 시뮬레이션하는 시스템 도구로 로봇과 무관함</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2611.04100'>The Agent Board: Kanban for Machines; Durable Coordination for Agents That Outlive the Conversation</a></td><td>26</td><td>0</td><td>AI</td><td>장기 에이전트 조정용 kanban 시스템 설계로 엔지니어링 성격이며 로봇과 무관함</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2611.05074'>Nested Field-of-View Barriers for Teleoperated Multi-Robot Relay Chains</a></td><td>25</td><td>3</td><td>Multi-Robot</td><td>teleoperation 릴레이 체인 FOV barrier임. 제어 중심임</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2611.05302'>PACT: Pose-Robust Actuation Co-Design for Tendon-Driven Robotic Hands</a></td><td>25</td><td>3</td><td>Hardware</td><td>tendon 손 actuation co-design임. 하드웨어 설계임</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2611.04654'>BhopalMLS: A LiDAR Dataset for Semantic Scene Understanding in Heterogeneous Urban Environments</a></td><td>25</td><td>2</td><td>3D Vision</td><td>인도 도시 MLS LiDAR 의미 분할 데이터셋임</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2611.04012'>SurgEye: Instruction Tuning-Free Perception-Reasoning Framework for Surgical Scene Understanding</a></td><td>25</td><td>1</td><td>Multimodal</td><td>수술 장면 이해용 학습 없는 인식 추론 프레임워크로 로봇과 거리가 있음</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2611.04498'>3DGS-VBench+ and 3DGSV-Assessor: A Multi-Dimensional Subjective Benchmark and a Reference-Flexible Objective Model for 3D Gaussian Splatting Video Quality Assessment</a></td><td>25</td><td>1</td><td>3D Vision</td><td>3DGS 영상 품질 평가 벤치마크임</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2611.04939'>Robustness Verification against Patch Attacks via Group-Lasso Semidefinite Relaxation</a></td><td>25</td><td>1</td><td>LG</td><td>패치 공격에 대한 robustness 검증 방법임</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2611.04641'>Does LinUCB Need Valid Confidence Sets?</a></td><td>25</td><td>1</td><td>RL</td><td>LinUCB confidence 폭 이론임</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2611.04482'>TEMPO: Time Series Understanding via Discrete Tokenization</a></td><td>25</td><td>1</td><td>NLP</td><td>시계열 이산 토큰화 이해임. 로봇 연결 약함</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2611.04416'>Efficient and Faithful High-Resolution Image Editing with Sparse Cross-Resolution Denoising</a></td><td>25</td><td>0</td><td>Generative</td><td>고해상도 이미지 편집의 효율화 기법임</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2611.04467'>Is Forgetting Unified? Exploring Concept Unlearning in Unified Multimodal Models</a></td><td>25</td><td>0</td><td>Multimodal</td><td>통합 멀티모달 모델의 개념 unlearning 분석임</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2611.04913'>EP-LVMQA: Evidence-Preserving Coarse-to-Fine Localization for Low-Quality Long Video Moment Question Answering</a></td><td>25</td><td>0</td><td>Video</td><td>저화질 긴 영상 moment QA의 근거 보존 방법임</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2611.05004'>ScoreDial: Precise Control of Visual Attributes in Image Generation via Regressor Guidance from Limited Human Ratings</a></td><td>25</td><td>0</td><td>Generative</td><td>제한된 평가로 이미지 속성을 정밀 제어하는 regressor guidance임</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2611.05193'>Factorized MLLM Embeddings for Composed Image Retrieval</a></td><td>25</td><td>0</td><td>Multimodal</td><td>분해된 MLLM embedding의 composed image retrieval임</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2611.05231'>Diagnosis by Composition: Detecting and Localizing Unseen Diseases by Composing Learned Radiological Findings</a></td><td>25</td><td>0</td><td>CV</td><td>방사선 소견 조합으로 미지 질환을 진단하는 의료 영상 연구로 로봇과 무관함</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2611.03887'>The Information Limits of Neural Controlled Differential Equations Under Sparse Observations</a></td><td>25</td><td>0</td><td>LG</td><td>Neural CDE의 희소 관측 정보 한계에 관한 이론임</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2611.03955'>Forget What Comes Next: LLM Unlearning via Statistical Independence</a></td><td>25</td><td>0</td><td>NLP</td><td>통계적 독립성 기반 LLM unlearning임</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2611.04081'>RAPID: Increasing Efficiency of Internal Distillation via Randomized Methods</a></td><td>25</td><td>0</td><td>LG</td><td>내부 활성 distillation 효율화임</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2611.04097'>ScaleTraj: Scale-Decomposed Human Trajectory Generation</a></td><td>25</td><td>0</td><td>LG</td><td>사람 이동 궤적 생성 모델임</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2611.04192'>Where Did the Update Go? Certifying Declared Change Envelopes for Model Updates</a></td><td>25</td><td>0</td><td>NLP</td><td>모델 업데이트 변화 범위 인증 통계 연구임</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2611.04434'>Sketchpad: certified exact arithmetic with a small vision-language model</a></td><td>25</td><td>0</td><td>Multimodal</td><td>작은 VLM으로 정확한 산술 인증임</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2611.04565'>Curriculum unlearning in humans and neural networks</a></td><td>25</td><td>0</td><td>LG</td><td>사람과 신경망의 curriculum unlearning 연구임</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2611.04751'>What Does It Mean to Remove an Edge? Intervention-Aware Fidelity for Graph Neural Network Explanations</a></td><td>25</td><td>0</td><td>LG</td><td>GNN 설명의 intervention 인지 fidelity임</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2611.04987'>ZEMA: confidence-calibrated signed descent with only one state</a></td><td>25</td><td>0</td><td>LG</td><td>부호 기반 optimizer ZEMA임</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2611.05120'>Towards an Optimal Control Foundation of Early Exits - Turnpikes and ResNets</a></td><td>25</td><td>0</td><td>LG</td><td>early exit의 optimal control 이론임</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2611.05191'>Stepsize modulation for cross entropy from local quadratic optimization</a></td><td>25</td><td>0</td><td>LG</td><td>cross entropy용 stepsize 조절 기법임. 작은 최적화 기법임</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2611.05243'>Logarithmic Regret for Alternating Mirror Descent</a></td><td>25</td><td>0</td><td>LG</td><td>zero-sum game용 mirror descent regret 이론임. 로보틱스 거리 멂</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2611.05325'>CATF: A Manager-Worker Framework for Context-Aware Time-Series Forecasting</a></td><td>25</td><td>0</td><td>LG</td><td>시계열 예측 manager-worker 프레임워크임. 로보틱스 연결 약함</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2611.05436'>Constraint-Preserving Flow Matching for Spectral Graph Generation</a></td><td>25</td><td>0</td><td>LG</td><td>spectral graph 생성용 flow matching임. 로보틱스 연결 없음</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2611.03836'>A Conditional Mutual Information Analysis of Response Variety in Language Models</a></td><td>25</td><td>0</td><td>NLP</td><td>응답 다양성 조건부 상호정보 분석임. 로봇과 무관함</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2611.04264'>Reliability Stress Testing of RAG Retrieval under Query-Relevant Corpus Poisoning</a></td><td>25</td><td>0</td><td>NLP</td><td>RAG 검색 단계의 corpus poisoning 신뢰성 stress test로 로봇과 무관함</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2611.04447'>Formalizing PTX in Lean to Prove GPU Kernel Correctness</a></td><td>25</td><td>0</td><td>LG</td><td>PTX를 Lean으로 형식화한 GPU 커널 검증 연구로 로봇과 무관함</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2611.04483'>CogniLife: Continuous Cognitive Distillation for Deployed Multi-Expert Agent Marketplaces</a></td><td>25</td><td>0</td><td>AI</td><td>에이전트 마켓플레이스용 연속 distillation으로 로봇과 무관함</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2611.04566'>A research world model of power engineering learns its dynamics and reveals what-ifs</a></td><td>25</td><td>0</td><td>LG</td><td>전력 공학 연구 방향용 world model이라는 이름을 쓴 응용으로 로봇의 world model과 다름</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2611.05088'>LatentTriad: Pre-Action Risk Representations for Malicious Agent Skill Detection</a></td><td>25</td><td>0</td><td>AI</td><td>악성 agent skill 검출용 위험 표현으로 보안 응용임</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2611.05151'>Catalyzing Interactive HTML Generation Capabilities via High-Fidelity Reinforcement Learning</a></td><td>25</td><td>0</td><td>NLP</td><td>HTML 생성용 high-fidelity RL로 코드 LLM 응용임</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2611.04057'>Look Before You Launch: Learned Throughput Prediction for Hardware Selection in a Production Training Fleet</a></td><td>24</td><td>0</td><td>LG</td><td>이종 가속기 선택을 위한 throughput 예측 연구로 로봇과 무관함</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2611.04534'>A Universal Raw-IQ Radar Encoder for Cross-Sensor Human Sensing</a></td><td>22</td><td>2</td><td>Multimodal</td><td>범용 raw IQ 레이더 인코더로 사람 센싱을 다룸</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2611.05197'>Robust Reconstruction of Power Lines from Incomplete Mobile and Aerial LiDAR Data</a></td><td>22</td><td>2</td><td>3D Vision</td><td>불완전 LiDAR에서 송전선을 복원함</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2611.04092'>CHROMA-MILL: Joint Low-Light Enhancement and White Balance under Colored Illumination</a></td><td>22</td><td>1</td><td>CV</td><td>저조도 향상과 화이트 밸런스 동시 처리하는 저수준 비전 연구임</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2611.04379'>Understanding Backdoor Attacks in Scene Graph Generation via Global Context Pathway</a></td><td>22</td><td>1</td><td>CV</td><td>scene graph 생성 backdoor 공격 분석임</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2611.04007'>Physics-Informed Identification of Tensegrity Prestress across Taut-Slack Transitions</a></td><td>22</td><td>1</td><td>LG</td><td>tensegrity prestress 식별로 구조 분야 연구임</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2611.04185'>What Does 4-Bit Microscaling Cost a Wearable Activity Recognizer?</a></td><td>22</td><td>1</td><td>LG</td><td>웨어러블 활동 인식의 4-bit 양자화 비용 평가임</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2611.04835'>Anomaly Detection on Resource-Constrained Devices with Reservoir Computing</a></td><td>22</td><td>1</td><td>LG</td><td>reservoir computing 엣지 이상 탐지임</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2611.04893'>Fault-tolerant shallow recurrent decoders for sparse sensing with missing sensor measurements</a></td><td>22</td><td>1</td><td>LG</td><td>센서 결측에 강한 sparse sensing 디코더임</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2611.05206'>Diffusion Plug-in Priors for Self-Supervised Ultrasound Video Restoration</a></td><td>22</td><td>0</td><td>CV</td><td>초음파 영상 복원용 diffusion prior 활용이며 로봇 관련성 없음</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2611.05294'>Wonder 4: A Mixture-of-Experts Recipe for Image Quality Enhancement</a></td><td>22</td><td>0</td><td>CV</td><td>이미지 화질 개선 mixture-of-experts recipe로 로봇과 무관함</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2611.03928'>Sequential auditing of connected forecast errors under partial observations</a></td><td>22</td><td>0</td><td>LG</td><td>그래프 예측 오차의 순차적 감사로 로봇과 무관함</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2611.03964'>Ermakov--Based embeddings as a parameter-free layer for physics-informed neural networks</a></td><td>22</td><td>0</td><td>LG</td><td>physics-informed 신경망의 Ermakov embedding으로 로봇과 무관함</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2611.03966'>Stacking-Based Weighting for Large Language Bayes in M-Open Settings</a></td><td>22</td><td>0</td><td>LG</td><td>LLM Bayes의 stacking 가중치 연구임</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2611.04056'>Structured Priors: Towards an algebra of component priors for prior-data fitted networks</a></td><td>22</td><td>0</td><td>LG</td><td>PFN prior 합성 대수 연구로 tabular 대상임</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2611.04066'>Graph-Localized Coverage for Conformal Prediction on Inductive Graphs</a></td><td>22</td><td>0</td><td>LG</td><td>그래프 conformal prediction의 국소 coverage임</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2611.04199'>An Information Budget for Label-Noise Memorization, and What Statistical Complexity Tracks: A Study with Multilayer Perceptrons</a></td><td>22</td><td>0</td><td>LG</td><td>label noise 암기 정보량 연구임</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2611.04256'>OmniST: Topology-Invariant Spatiotemporal Forecasting with Guaranteed-Coverage Uncertainty at Unseen Sensor Locations</a></td><td>22</td><td>0</td><td>LG</td><td>센서 위치 불변 시공간 예측임</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2611.04462'>SaMA: Morpho Adaptation via Asymmetric Expansion of Kronecker Product</a></td><td>22</td><td>0</td><td>LG</td><td>Kronecker 기반 PEFT 방법임</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2611.04611'>CAPSkip: Cancellation-Aware Prefix Skipping for Selective Backpropagation</a></td><td>22</td><td>0</td><td>LG</td><td>선택적 backprop 규칙임</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2611.05157'>Macrocanonical Generator Networks: Data-Efficient Neural Surrogates for Amortized Physics Simulation</a></td><td>22</td><td>0</td><td>LG</td><td>과학 시뮬레이션 surrogate 생성망임. 로보틱스와 무관함</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2611.05202'>Empirical Bayes Flow Matching for Continuous Cryo-EM Heterogeneity</a></td><td>22</td><td>0</td><td>LG</td><td>cryo-EM용 flow matching임. 로보틱스와 무관함</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2611.05241'>Shrinkage prior for implicit generative models</a></td><td>22</td><td>0</td><td>LG</td><td>implicit generative model용 shrinkage prior임. 통계 중심임</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2611.05346'>Agnostic Learning by Imitating</a></td><td>22</td><td>0</td><td>LG</td><td>agnostic learning 이론임. 로보틱스와 무관함</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2611.04697'>When Ground Truth Is Not Ground Truth: Automatic Labeling for Hallucination Detection</a></td><td>22</td><td>0</td><td>NLP</td><td>환각 탐지용 자동 라벨링임. 로봇 연결 없음</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2611.04878'>TraceRouter++: Causal Semantic Routing Realignment via Optimal Transport</a></td><td>22</td><td>0</td><td>NLP</td><td>foundation model 안전 라우팅 OT임. 로봇 연결 없음</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2611.03882'>ProofPaths: An AI Agent Framework for Assessing Student Reasoning</a></td><td>22</td><td>0</td><td>NLP</td><td>학생 추론 평가용 에이전트 프레임워크로 교육 응용이며 로봇과 무관함</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2611.03983'>A Guideline-Grounded Multi-Agent Framework for Personalized Exercise Prescription from Clinical and Wearable Data</a></td><td>22</td><td>0</td><td>AI</td><td>운동 처방용 multi-agent 프레임워크로 의료 응용이며 로봇과 무관함</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2611.04048'>Exploit or conform? How norm utility prompting changes the way LLMs use community beliefs</a></td><td>22</td><td>0</td><td>NLP</td><td>규범 prompting이 LLM의 공동체 자원 사용에 주는 영향을 본 사회 시뮬레이션 연구임</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2611.04435'>A Systematic Point Cloud Edge Detection Framework for Automatic Aircraft Skin Milling</a></td><td>20</td><td>2</td><td>3D Vision</td><td>항공기 외피 밀링용 point cloud 에지 검출임</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2611.04959'>Lightweight graph transformers for clutter and target classification in automotive radar</a></td><td>20</td><td>2</td><td>CV</td><td>자동차 레이더 clutter 분류용 경량 graph transformer임</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2611.03975'>Self-governed access control in open robot swarms using a blockchain-based DAO</a></td><td>20</td><td>2</td><td>Robotics</td><td>swarm 접근 제어에 blockchain DAO 적용임. 학습 관련성 낮음</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2611.04748'>Mass Scaling Laws for Energy-Optimal Horizontal Multirotor Flight</a></td><td>20</td><td>2</td><td>Aerial</td><td>멀티로터 질량 스케일링 법칙 분석임. 학습 관련성 낮음</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2611.05244'>Reality and Perceptual Gaps in Expressive Swarm Robotics</a></td><td>20</td><td>2</td><td>Swarm</td><td>expressive swarm sim-to-real 간극 분석임. 학습 관련성 낮음</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2611.04242'>Improving Diffusion-Based Augmentation for Data-Scarce Image Classification via Mask-Guided Reference Attention and Repulsive Noise Optimization</a></td><td>20</td><td>1</td><td>CV</td><td>데이터 부족 분류를 위한 diffusion 증강 개선임</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2611.04111'>Generalizable AI-Generated Image Detection with Embedding-Space Explanations</a></td><td>20</td><td>0</td><td>CV</td><td>AI 생성 이미지 검출 연구로 로봇과 무관함</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2611.03844'>Probabilistic Steering of Generative Priors for Lab-in-the-Loop Antibody Optimization</a></td><td>20</td><td>0</td><td>LG</td><td>항체 최적화용 생성 prior steering으로 로봇과 무관함</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2611.03867'>ExaTune: Exhaustive Hyperparameter Landscape Exploration at Scale</a></td><td>20</td><td>0</td><td>LG</td><td>hyperparameter landscape 탐색 도구로 로봇과 무관함</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2611.03968'>One Mistake, Three Layers: Persistence Rules Under Depth Correlation</a></td><td>20</td><td>0</td><td>LG</td><td>layer probing 지속성 규칙 연구로 로봇과 무관함</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2611.04104'>ModelBlaster: Closing the Performance Gap through Learning-Augmented Agents Across Models, Kernels and Hardware Backends</a></td><td>20</td><td>0</td><td>LG</td><td>accelerator 코드 최적화 agent임</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2611.04116'>Decomposing Rank Reversals under Temporal Nonstationarity: Alignment, Aggressiveness, and Instability</a></td><td>20</td><td>0</td><td>LG</td><td>시계열 순위 역전 분해 분석임</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2611.04146'>RGDM: Robust Graph Diffusion Model</a></td><td>20</td><td>0</td><td>LG</td><td>그래프 diffusion 모델 강건성 연구임</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2611.04273'>Deep Learning Compilers: Architecture, Optimization, and Empirical Characterization</a></td><td>20</td><td>0</td><td>LG</td><td>DL compiler 개요와 실험 분석임</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2611.04295'>Reciprocity Can Erase Direction:tructural Boundaries and Controlled Utility of Magnetic Graph Networks</a></td><td>20</td><td>0</td><td>LG</td><td>magnetic graph network 구조 한계 분석임</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2611.04449'>Near-Zero Token Embeddings Silently Stall Training in Gated Sequence Models</a></td><td>20</td><td>0</td><td>NLP</td><td>토큰 embedding norm 문제 진단임</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2611.04465'>Theoretical Analysis of Muon on Transformers for Next-Token Prediction</a></td><td>20</td><td>0</td><td>LG</td><td>Muon optimizer 이론 분석임</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2611.04501'>Sample-Grained Approximate Unlearning with Provable Per-Sample Bounds</a></td><td>20</td><td>0</td><td>LG</td><td>sample 단위 근사 unlearning 이론임</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2611.04513'>Variational Learning with Lie Group Exponential Families</a></td><td>20</td><td>0</td><td>LG</td><td>Lie group 지수족 변분 학습임</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2611.04667'>FedCSGA: Evolutionary Client Selection with Joint Statistical and System Heterogeneity in Federated Learning</a></td><td>20</td><td>0</td><td>LG</td><td>federated learning client 선택임</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2611.05276'>De Rham cohomological architectures for PINNs and PDEs with topological holes</a></td><td>20</td><td>0</td><td>LG</td><td>PINN용 de Rham 구조임. 로보틱스와 무관함</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2611.03982'>SLATE: A Large-Scale Benchmark for Long-Horizon API Selection in E-commerce Tool Use</a></td><td>20</td><td>0</td><td>NLP</td><td>e-commerce API 선택 벤치마크임. 로보틱스와 무관함</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2611.04215'>Tokenizer Myths and Where To Find Them</a></td><td>20</td><td>0</td><td>NLP</td><td>tokenizer 통념 검증임. 로보틱스와 무관함</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2611.03853'>Performance, Scalability and Maintenance: An Experimental Study of RPA vs. Autonomous Agents in the Healthcare Domain</a></td><td>20</td><td>0</td><td>LG</td><td>RPA와 자율 에이전트의 의료 포털 데이터 수집 비교 실험으로 로봇 학습과 무관함</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2611.03985'>Thinking Fast, Trading Late: System One Decision Models vs the Market</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 뉴스 기반 주식 예측의 한계를 보는 금융 연구로 로봇과 무관함</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2611.04101'>Structured Clinical Memory as Context for Probabilistic Decision Models: A Synthetic Evaluation with Jev</a></td><td>20</td><td>0</td><td>AI</td><td>임상 기록 구조화 memory 합성 연구로 의료 응용임</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2611.04330'>CORA: Teacher-Guided Causal O-RAN Adaptation for Jamming Detection</a></td><td>20</td><td>0</td><td>LG</td><td>O-RAN 재밍 검출 적응 방법으로 통신 응용임</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2611.04510'>Fast, Cheap, and Fair? Evaluating Decision Models</a></td><td>20</td><td>0</td><td>AI</td><td>결정 모델의 속도, 비용, 공정성 평가로 로봇과 무관함</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2611.04772'>TactiNavi: Serving and Revising an LLM Game Coach with Explicit Strategy Conditions</a></td><td>20</td><td>0</td><td>AI</td><td>게임 코치 LLM의 전략 조건 서빙으로 응용 시스템임</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2611.04809'>RAHC: Rule-Augmented Hyper-Relational Knowledge Graph Completion for Materials Synthesis</a></td><td>20</td><td>0</td><td>AI</td><td>재료 과학 지식 그래프 완성 방법으로 응용임</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2611.04813'>AgenticFinBench: Benchmarking Financial Agents on Diverse Tasks from Real-World Requests</a></td><td>20</td><td>0</td><td>AI</td><td>금융 에이전트 benchmark로 로봇과 무관함</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2611.05135'>From Opinions to Commitments: Unstable Assignments and Silent Choices in AI-Mediated Proposals</a></td><td>20</td><td>0</td><td>NLP</td><td>시민 의견을 제안으로 바꾸는 LLM의 불안정성 분석으로 로봇과 무관함</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2611.05459'>Can Large Language Models Review the Scientific Literature? A Test Against a 102-Article Benchmark</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM의 문헌 리뷰 능력 평가로 로봇과 무관함</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2611.04317'>SteelHuman: Predicting Operator Estimates of Steel-Scrap Composition from Sparse RGB Views</a></td><td>18</td><td>1</td><td>CV</td><td>고철 조성 추정으로 로봇과 거리가 멂</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2611.04548'>Predicting Void Points in Self-Occluding Forest Volumes</a></td><td>18</td><td>1</td><td>3D Vision</td><td>숲 캐노피 합성 개구 영상의 가려짐 예측임</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2611.04616'>Gradient-Guided Orientation Learning for Weakly Supervised Oriented Object Detection</a></td><td>18</td><td>1</td><td>CV</td><td>약지도 회전 객체 검출로 방향 학습을 개선함</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2611.04389'>Spin Spherical Fourier Neural Operators: Efficient Equivariant Learning for Vector and Spin Fields on the Sphere</a></td><td>18</td><td>0</td><td>LG</td><td>구면 spin field용 등변 neural operator로 로봇과 무관함</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2611.04811'>NightIQA: A Comprehensive Dataset and Benchmark for MLLM-Based Nighttime Image Quality Assessment</a></td><td>18</td><td>0</td><td>Multimodal</td><td>야간 이미지 품질 평가 MLLM 벤치마크임</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2611.05223'>PLANTEUR: A Crop-Type Segmentation Benchmark for Tropical Regions</a></td><td>18</td><td>0</td><td>CV</td><td>열대 작물 위성 영상 분할 benchmark로 로봇과 무관함</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2611.09993'>Retrieval-Grounded Multi-View Reasoning for Clinically Reliable Radiology Report Generation</a></td><td>18</td><td>0</td><td>Multimodal</td><td>흉부 X-ray 보고서 생성으로 로봇과 무관함</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2611.04571'>Ground-Wing: A Parametric 3D Wing-in-Ground-Effect Dataset for Benchmarking Neural Surrogate Models</a></td><td>18</td><td>0</td><td>LG</td><td>지면 효과 날개 CFD dataset임</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2611.04603'>SCANO: Restoring Boundary-Condition Completeness in Sampled Meshes with a Sliced-Cross-Attention Neural Operator for 3D Thermal Fields</a></td><td>18</td><td>0</td><td>LG</td><td>3D 열장 neural operator 연구임</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2611.04670'>Sheaf-MPNN: A Library for Sheaf Neural Networks as Message Passing</a></td><td>18</td><td>0</td><td>LG</td><td>sheaf neural network 라이브러리임</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2611.05012'>Rethinking GA2Ms: performance and out-of-distribution generalisation</a></td><td>18</td><td>0</td><td>LG</td><td>GA2M 성능과 OOD 일반화임</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2611.05141'>Beyond Foundation Models: PFN Priors Improve Tabular Hyperparameter Optimization</a></td><td>18</td><td>0</td><td>LG</td><td>tabular HPO용 PFN prior임</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2611.05208'>Privacy for Free in Efficient Agnostic Halfspace Learning</a></td><td>18</td><td>0</td><td>LG</td><td>differential privacy halfspace 학습 이론임. 로보틱스와 무관함</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2611.05225'>Post-Inference Model Chaining: A Problem Statement and a Model-based Bootstrap for Training End-to-End Digital Twins</a></td><td>18</td><td>0</td><td>LG</td><td>디지털 트윈 모델 체이닝 bootstrap임. 로보틱스 연결 약함</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2611.04218'>Shared Context Candidate Scoring with Jointly Adapted Readout Networks</a></td><td>18</td><td>0</td><td>NLP</td><td>공유 문맥 후보 scoring 어댑테이션임. 로보틱스와 무관함</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2611.03946'>We Ran a Research Sprint With AI. The AI Worked. The Research Didn&#x27;t</a></td><td>18</td><td>0</td><td>AI</td><td>AI 활용 연구 스프린트 경험 보고로 기술적 기여가 없음</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2611.04126'>GlucoAgent: Personalized Glucose Forecasting from Multimodal Personal Context</a></td><td>18</td><td>0</td><td>LG</td><td>혈당 예측 멀티모달 모델로 의료 응용이며 로봇과 무관함</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2611.04203'>Toward User-Centered Agentic Recommendation: When Does Platform Competition Benefit Users?</a></td><td>18</td><td>0</td><td>AI</td><td>플랫폼 경쟁이 추천에 주는 영향을 다룬 모델 연구로 로봇과 무관함</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2611.04338'>Patching the Protocol: A Taxonomy of Pre-Registration Repairs in LLM-Proposer Experiments</a></td><td>18</td><td>0</td><td>AI</td><td>LLM 제안자 실험의 사전등록 수정 유형 분류로 메타 연구임</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2611.04342'>Beyond Fine-Tuning: Evaluating Prompt Engineering and Prompt Tuning for Roman Urdu Hate Speech Detection</a></td><td>18</td><td>0</td><td>NLP</td><td>로만 우르두 혐오 발화 검출에서 prompt 방식 비교 연구임</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2611.04369'>Benchmarking Unsupervised Jamming Detection in 5G Open RAN</a></td><td>18</td><td>0</td><td>LG</td><td>5G Open RAN 재밍 검출 benchmark로 로봇과 무관함</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2611.04637'>SAT Encoding for Set of At-Most-K Cardinality Constraints with Ladder Shape</a></td><td>18</td><td>0</td><td>AI</td><td>ladder 모양 cardinality 제약의 SAT 인코딩으로 로봇과 무관함</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2611.04819'>Reconstructing Fraudulent Strategies in Online Payments via Interpretable Inverse Reinforcement Learning</a></td><td>18</td><td>0</td><td>LG</td><td>결제 사기 전략 복원용 inverse learning으로 응용임</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2611.05148'>Creating Power Flexibility in Datacenters via Query Routing</a></td><td>18</td><td>0</td><td>LG</td><td>질의 라우팅으로 데이터센터 전력 유연성을 만드는 시스템 연구임</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2611.04871'>Physics-Based Plausibility Assessment of AI-Predicted Vehicle Parameters for Automotive Radar in Pre-Crash Scenarios</a></td><td>15</td><td>1</td><td>Autonomous Driving</td><td>레이더 차량 파라미터 타당성 평가임. 로봇 학습과 거리 멂</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2611.04529'>Learning to Falsify: Hierarchical Multiple Instance Learning for High Resolution AI-Generated Image Detection</a></td><td>15</td><td>0</td><td>CV</td><td>AI 생성 이미지 검출 연구임</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2611.04633'>ReXMo: End-to-End Video Character Replacement with Expression and Motion Preservation</a></td><td>15</td><td>0</td><td>Video</td><td>영상 캐릭터 교체 생성으로 로봇과 무관함</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2611.04754'>Bounded AUKS: A Novel Evaluation Metric for Anomaly Detection via Bounded Area Under the Kolmogorov--Smirnov Curve</a></td><td>15</td><td>0</td><td>CV</td><td>이상 검출 평가 지표 제안임</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2611.04874'>OCR in the Foundation Model Era: From Specialist Models to Unified Models</a></td><td>15</td><td>0</td><td>Multimodal</td><td>OCR foundation model 서베이임</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2611.05181'>What Does the Model See? Representation Validity in Multimodal LLM-Based Video Analysis</a></td><td>15</td><td>0</td><td>Multimodal</td><td>MLLM 영상 분석 입력 표현 타당성 연구임</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2611.05348'>OpenBrain: An Auditable Generated-Label Release for Whole-Brain MRI Parcellation</a></td><td>15</td><td>0</td><td>CV</td><td>뇌 MRI parcellation label 공개로 로봇과 무관함</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2611.09998'>Quality-Governed Deep Learning Network for Brain Tumor MRI Segmentation</a></td><td>15</td><td>0</td><td>CV</td><td>뇌종양 MRI 분할 네트워크로 로봇과 무관함</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2611.03934'>Accelerating FastDEC Clustering Algorithm with GPUs</a></td><td>15</td><td>0</td><td>LG</td><td>FastDEC 클러스터링 GPU 가속으로 로봇과 무관함</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2611.04217'>LENS: Reliability-Aware Stock Prediction via LLM-Extracted Priors and News-Driven Semantic Graphs</a></td><td>15</td><td>0</td><td>LG</td><td>뉴스 기반 주가 예측임</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2611.04344'>Proper Agnostic Learning of Affine Halfspaces under Log-Concave Marginals</a></td><td>15</td><td>0</td><td>LG</td><td>affine halfspace agnostic 학습 이론임</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2611.04660'>Leakage-free evaluation of residual graph convolutional networks for network intrusion detection</a></td><td>15</td><td>0</td><td>LG</td><td>네트워크 침입 탐지 GCN 평가 누수 점검임</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2611.04664'>Feature-Based and Deep Learning Methods for Astronomical Light Curve Classification</a></td><td>15</td><td>0</td><td>LG</td><td>천문 광도 곡선 분류 비교임</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2611.04695'>Surrogate Models for Stochastic Al-Cu Phase-Field Solidification</a></td><td>15</td><td>0</td><td>LG</td><td>Al-Cu 응고 phase-field surrogate임</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2611.04747'>TAPES: Task-Aligned Joint Predictive Pretraining for Transaction Event Sequences</a></td><td>15</td><td>0</td><td>LG</td><td>거래 이벤트 시퀀스 사전학습임</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2611.04756'>Non-Interfering Asymmetric AdamW Updates for Constrained Exploration of Equifinality in Hybrid Models</a></td><td>15</td><td>0</td><td>LG</td><td>hybrid 모델 AdamW 업데이트임</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2611.04806'>On the Complexity of Finite-Sum Nonconvex-Strongly-Concave Minimax Optimization with Exact Proximal Oracles</a></td><td>15</td><td>0</td><td>LG</td><td>minimax 최적화 복잡도 하한임</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2611.04907'>Cool Graphs: Active Property Search Towards Quantum Nano-Refrigerators</a></td><td>15</td><td>0</td><td>LG</td><td>양자 냉각 소자 능동 탐색임</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2611.04997'>Auditing Multi-Proxy Explanations of Web User Preferences: Identification Boundaries and Abstention</a></td><td>15</td><td>0</td><td>LG</td><td>웹 사용자 선호 설명 감사임</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2611.05022'>Finite Spectral Depth Controls Gaussian Entrance Rank and Avoidance of the First Gradient-Flow Saddle</a></td><td>15</td><td>0</td><td>LG</td><td>행렬 분해 gradient flow 이론임</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2611.05035'>Federated Transfer Learning for Medical Image Classification under Mixed Skew</a></td><td>15</td><td>0</td><td>CV</td><td>의료 영상 federated transfer learning임</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2611.05099'>Dual-VaDE: Efficient and Robust Prototype Learning via Variational Dual-Domain Mixture Priors</a></td><td>15</td><td>0</td><td>CV</td><td>의료 영상 prototype 학습임</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2611.05164'>Basin2Vec: Learning Basin-Centric Embeddings for Scalable Hydrological Modeling</a></td><td>15</td><td>0</td><td>LG</td><td>수문 모델링용 basin embedding임. 로보틱스와 무관함</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2611.05270'>iGC: Antibody Optimization via Reinforcement Learning over a Learned Somatic Hypermutation Prior</a></td><td>15</td><td>0</td><td>RL</td><td>항체 최적화 RL임. 로보틱스와 무관함</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2611.05296'>Universal Hardness From Masking Channels</a></td><td>15</td><td>0</td><td>LG</td><td>hardcore lemma 일반화 이론임. 로보틱스와 무관함</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2611.04090'>Swapping the Judge Changes the Ranking: A Preregistered Study of Cross-Provider Replication in LLM-Judged System Comparisons</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM judge 교체 순위 변화 연구임. 로보틱스와 무관함</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2611.04249'>COMPREHEND: Ultra-Fine-Grained Benchmark Understanding by Entailment Hierarchy</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM 벤치마크 계층 분석임. 로보틱스와 무관함</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2611.04390'>Do Multi-Turn Conversational Capabilities Carry Over from Text to Speech? A Parallel Multilingual Benchmark</a></td><td>15</td><td>0</td><td>NLP</td><td>음성 multi-turn 능력 이전 평가임. 로보틱스와 무관함</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2611.05124'>The Right Source Is Not Enough: Understanding History Interference in Speech-LLM Memory</a></td><td>15</td><td>0</td><td>NLP</td><td>speech LLM 기록 간섭 분석임. 로보틱스와 무관함</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2611.04196'>DoGNAVY-Exploit: Harnessing Parallel Open-Weight Agents for Stage-Aware Vulnerability Exploitation</a></td><td>15</td><td>0</td><td>AI</td><td>오픈 가중치 에이전트의 취약점 exploit 연구로 로봇과 무관함</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2611.04546'>Are LLM Assistants Regulatory Ready? Answers from regenold&#x27;s 2026 EU AI Act Q&amp;A Challenge</a></td><td>15</td><td>0</td><td>NLP</td><td>EU AI Act Q&amp;A에서 LLM 신뢰성을 평가한 법규 응용임</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2611.04576'>ValQID: Learning the Net Value of Semantic Query Groups for Web Device Identification</a></td><td>15</td><td>0</td><td>LG</td><td>웹 장치 식별용 질의 그룹 가치 학습으로 로봇과 무관함</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2611.04886'>Modelling lock-in of AI adoption through skill erosion</a></td><td>15</td><td>0</td><td>AI</td><td>AI 사용에 따른 기술 약화 lock-in 모델로 이론 사회과학임</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2611.05171'>AgentAM: An AI Agent for Spatter- and Defect-Aware Process Optimization in Laser Powder Bed Fusion</a></td><td>15</td><td>0</td><td>AI</td><td>레이저 적층 제조 공정 최적화 에이전트로 응용임</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2611.04254'>P-SER: Physical Consistency-Constrained Scattering Expandable Representation for Class-Incremental HRRP Target Recognition</a></td><td>12</td><td>0</td><td>CV</td><td>레이더 HRRP 클래스 증분 인식으로 로봇과 무관함</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2611.04303'>FlowTranslator: Training-Free In-Image Machine Translation with Flow-Based Editing</a></td><td>12</td><td>0</td><td>CV</td><td>이미지 내 텍스트 번역 편집으로 로봇과 무관함</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2611.04476'>KeyWise: Efficient Video-Only Piano Transcription with a Lightweight Per-Key Architecture</a></td><td>12</td><td>0</td><td>Video</td><td>영상만으로 피아노 채보하는 경량 모델임</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2611.04626'>MambaHand: Local Identity and Behavioral Sequence Learning with Mamba for Dynamic Hand Gesture Authentication</a></td><td>12</td><td>0</td><td>CV</td><td>동적 손 제스처 인증으로 생체 인식임</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2611.04980'>ProAlign: Progressive Positional and Prototype-Guided Alignment for Aerial-Ground Person Re-Identification</a></td><td>12</td><td>0</td><td>CV</td><td>항공 지상 재식별 정렬 방법임</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2611.05131'>High-fidelity training-free photovoltaic module mapping from multi-view UAV imagery</a></td><td>12</td><td>0</td><td>CV</td><td>UAV 태양광 모듈 매핑임</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2611.04532'>The Price of List Replicability: Tight Bounds for Bias Estimation</a></td><td>12</td><td>0</td><td>LG</td><td>list replicability 표본 복잡도 이론임</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2611.04818'>Sleep-Disordered Breathing Detection with Quantum Recurrent Neural Networks</a></td><td>12</td><td>0</td><td>LG</td><td>양자 RNN 수면 호흡 탐지임</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2611.04955'>Deep Neural Operator Learning for stochastic heat equations and applications</a></td><td>12</td><td>0</td><td>LG</td><td>SPDE neural operator 근사 이론임</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2611.04995'>Exact Selective Inference for Spectral Clustering via Piecewise-Constant Graph Perturbation</a></td><td>12</td><td>0</td><td>LG</td><td>spectral clustering selective inference임</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2611.05220'>Fusing Earth observation embeddings and spaceborne terrain with meteorological forcing for flood peak depth prediction from high-water marks</a></td><td>12</td><td>0</td><td>LG</td><td>홍수 깊이 예측용 융합 모델임. 로보틱스와 무관함</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2611.05222'>Fairness Metrics based on the AUC in Clinical Predictive AI</a></td><td>12</td><td>0</td><td>LG</td><td>임상 예측 공정성 지표 연구임. 로보틱스와 무관함</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2611.05260'>NovoCRF: Globally Normalized De Novo Peptide Sequencing on a Prefix-Mass Lattice</a></td><td>12</td><td>0</td><td>LG</td><td>펩타이드 시퀀싱 모델임. 로보틱스와 무관함</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2611.05309'>$Φ$asmaNet: A Staged Spectral Token-Refinement Architecture for Fast Gravitational-Wave Signal-to-Noise Ratio Prediction</a></td><td>12</td><td>0</td><td>LG</td><td>중력파 SNR 근사 모델임. 로보틱스와 무관함</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2611.03826'>Rethinking Next-Visit Diagnosis Prediction Beyond Aggregate Metrics: Retrieval--Memory Multi-Agent Adjudication</a></td><td>12</td><td>0</td><td>NLP</td><td>진단 예측 평가 연구임. 로보틱스와 무관함</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2611.03948'>Balancing Chain-of-Thought and Answer Supervision for Small Language Models on Medical Question Answering</a></td><td>12</td><td>0</td><td>NLP</td><td>의료 QA 소형 LM supervision 균형임. 로보틱스와 무관함</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2611.04230'>Exact Optimality Certification of QPLIB 2096 through Complete Set Partitioning</a></td><td>12</td><td>0</td><td>LG</td><td>QPLIB 인스턴스의 최적성 증명으로 로봇과 무관함</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2611.04515'>Learnings and Pitfalls from AI-Assisted A/B Experimentation at Scale</a></td><td>12</td><td>0</td><td>AI</td><td>AI 보조 A/B 실험 운영 경험담으로 기술 기여가 약함</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2611.04053'>Spatial and Temporal Super-Resolution and Denoising of Intracardiac 4D Flow MRI</a></td><td>10</td><td>0</td><td>CV</td><td>심장 4D flow MRI 초해상도로 로봇과 무관함</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2611.04200'>Impact of Input Resolution in Mammographic Mass Detection: A Controlled Multi-Architecture Study</a></td><td>10</td><td>0</td><td>CV</td><td>유방촬영 해상도 영향 연구로 로봇과 무관함</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2611.04219'>Reliability-Role Collaborative Learning for Semi-Supervised Cardiac Image Segmentation</a></td><td>10</td><td>0</td><td>CV</td><td>반지도 심장 분할 연구로 로봇과 무관함</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2611.04337'>Mitigating Spatial Blindness in Multiple Instance Learning for Whole-Slide Image Analysis</a></td><td>10</td><td>0</td><td>CV</td><td>병리 WSI의 공간 정보 활용 문제로 로봇과 무관함</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2611.04409'>LCM-UNet: Scale-Selective Mamba with Reparameterizable Multi-Basis Local Modeling for Lightweight Skin Lesion Segmentation</a></td><td>10</td><td>0</td><td>CV</td><td>피부 병변 경량 분할로 로봇과 무관함</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2611.04423'>SWAP-INR: Implicit Neural Representation with Switchable Attention Paths for Time-varying Multivariate Scientific Data Compression</a></td><td>10</td><td>0</td><td>LG</td><td>과학 시뮬레이션 데이터 압축용 INR로 로봇과 무관함</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2611.04490'>Polarimetric Scattering-Structure Contrastive Learning for Few-Shot HRRP Recognition</a></td><td>10</td><td>0</td><td>CV</td><td>레이더 HRRP few-shot 인식으로 로봇과 무관함</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2611.04712'>VISAGE: Vertex-based Intrinsic Surface Appearance GEneration via Dual-Stream Diffusion for Arbitrary 3D Heads</a></td><td>10</td><td>0</td><td>3D Vision</td><td>3D 머리 표면 외형 생성으로 로봇과 무관함</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2611.04932'>VISTA: Vision-Language Integrated Semantic Triage Architecture for Online Face Clustering in Long Videos</a></td><td>10</td><td>0</td><td>Video</td><td>긴 영상 온라인 얼굴 clustering임</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2611.04950'>DPAGait: Dynamic Pose-Knowledge-Aware Network for Robust Gait Recognition in the Wild</a></td><td>10</td><td>0</td><td>CV</td><td>보행 인식 생체 연구임</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2611.04960'>An Agentic Framework for Quality-Aware and Scenario-Adaptive Image Compression</a></td><td>10</td><td>0</td><td>CV</td><td>이미지 압축 agentic 프레임워크임</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2611.05008'>Learned Smartphone ISP on Mobile GPUs: Mobile AI 2026 Challenge Report</a></td><td>10</td><td>0</td><td>CV</td><td>모바일 ISP 챌린지 보고서임</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2611.05011'>Can saliency maps flag chest radiograph classifier errors at a new hospital? An external validation study</a></td><td>10</td><td>0</td><td>CV</td><td>흉부 방사선 saliency 외부 검증임</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2611.05024'>RGB Photo Enhancement with Deep Learning on Smartphone GPUs: Mobile AI 2026 Challenge Report</a></td><td>10</td><td>0</td><td>CV</td><td>모바일 사진 보정 챌린지 보고서임</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2611.05102'>Characterizing the vertical continuity of fuel strata based on TLS point clouds Gaussian decomposition and overlap metrics</a></td><td>10</td><td>0</td><td>3D Vision</td><td>TLS 점군 연료층 분석으로 산림학 응용임</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2611.05192'>From Natural Images to Medical Scans: Transferability of Diffusion Models for Medical Image Generation</a></td><td>10</td><td>0</td><td>Generative</td><td>의료 영상 생성용 diffusion 전이 연구임</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2611.05103'>Molecular Prior Networks</a></td><td>10</td><td>0</td><td>LG</td><td>약물 표적 친화도 예측임</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2611.05114'>Beyond Multi-Index Models: Learning Intersections of Degree-2 PTFs</a></td><td>10</td><td>0</td><td>LG</td><td>PTF 교집합 PAC 학습 이론임</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2611.05128'>Do Ray-Traced Cities Make a Better Channel Prior for an Unseen Site? A Pre-Registered Study in Simulation, and a Test on Measured Channels that Reverses It</a></td><td>10</td><td>0</td><td>LG</td><td>무선 채널 prior 연구임</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2611.05133'>PAC Learning with Multiple Correct Answers</a></td><td>10</td><td>0</td><td>LG</td><td>복수 정답 PAC 학습 이론임</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2611.05442'>Matched but Not Better: An Equivalence-Tested Benchmark of Quantum Machine Learning on Six Clinical Datasets and the QML-Health-READY Reporting Framework</a></td><td>10</td><td>0</td><td>LG</td><td>양자 ML 임상 벤치마크임. 로보틱스와 무관함</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2611.03993'>Whose startup does the AI back? An algorithm audit of reputation and demographic signals in LLM-assisted crowdfunding</a></td><td>10</td><td>0</td><td>NLP</td><td>LLM 창업 추천 편향 감사임. 로보틱스와 무관함</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2611.04091'>Same Rule, Different Verdicts: Rubric Language and Clause Structure in LLM Judges for Korean Support Dialogues</a></td><td>10</td><td>0</td><td>NLP</td><td>한국어 rubric LLM judge 연구임. 로보틱스와 무관함</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2611.04099'>Evaluation Contracts and Evaluation Leverage: Sliced-Gap Readings in Structured Prediction Can Move Without Model Change</a></td><td>10</td><td>0</td><td>NLP</td><td>관계 추출 평가 해석 연구임. 로보틱스와 무관함</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2611.04147'>AdSteer: Native Advertising in Large Language Model Generation</a></td><td>10</td><td>0</td><td>NLP</td><td>LLM 생성 내 광고 삽입임. 로보틱스와 무관함</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2611.04421'>Typological Feature Induction as a Benchmark for Inductive Metalinguistic Reasoning</a></td><td>10</td><td>0</td><td>NLP</td><td>유형론 feature 귀납 벤치마크임. 로보틱스와 무관함</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2611.04941'>Residual Attribute Leakage Is an Interface: Auditing Privacy Evaluation After Text De-identification</a></td><td>10</td><td>0</td><td>NLP</td><td>비식별화 프라이버시 평가임. 로보틱스와 무관함</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2611.04153'>Palimpsestic Accountability in the US Federal AI Inventories</a></td><td>10</td><td>0</td><td>AI</td><td>미국 연방 AI 인벤토리 정책 분석으로 기술 연구가 아님</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2611.04785'>Kierston &amp; KierstonBench: Simulation of Allentown, PA and Evaluation of Language Models in Crime Investigation and Surveillance Tasks</a></td><td>10</td><td>0</td><td>NLP</td><td>범죄 수사 시뮬레이션과 LLM 평가로 로봇과 무관함</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2611.04155'>Improving PI-RADS Prediction and Prostate Cancer Detection from Multiparametric MRI with Anatomical Guidance</a></td><td>8</td><td>0</td><td>CV</td><td>전립선 MRI PI-RADS 예측 개선으로 로봇과 무관함</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2611.04193'>Statistical Machine Learning for Medicinal Plant Leaves Classification</a></td><td>8</td><td>0</td><td>CV</td><td>약용 식물 잎 분류로 로봇과 무관함</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2611.04233'>LINDA: Low Resource Foot Ulcer Segmentation using Local Similarity and Iterative Neural Dynamics</a></td><td>8</td><td>0</td><td>CV</td><td>발 궤양 분할로 로봇과 무관함</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2611.04235'>TCINet: Tissue-Conditioned Adaptive Cross-Branch Interaction Network for Nuclei Instance Segmentation</a></td><td>8</td><td>0</td><td>CV</td><td>핵 인스턴스 분할로 로봇과 무관함</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2611.04257'>ProGeo-RC: Prototype-guided Semantic Reliability and Geometric Error Calibration for Semi-supervised Cardiac Image Segmentation</a></td><td>8</td><td>0</td><td>CV</td><td>반지도 심장 분할로 로봇과 무관함</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2611.04405'>DR-LiteNet: A Lightweight Explainable Hybrid CNN Framework for Imbalanced Diabetic Retinopathy Grading via Adaptive SMOTE Fusion</a></td><td>8</td><td>0</td><td>CV</td><td>당뇨망막병증 등급 분류로 로봇과 무관함</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2611.04470'>Using GeoAI and machine learning tools for consistent high-resolution land cover mapping based on time-series NAIP imagery</a></td><td>8</td><td>0</td><td>CV</td><td>항공영상 토지 피복 지도 작성으로 로봇과 무관함</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2611.04524'>E2I-Flow: EEG-to-Image Reconstruction via Wavelet-Temporal Cross-Attention and Conditional Flow Matching</a></td><td>8</td><td>0</td><td>CV</td><td>EEG 이미지 복원으로 로봇과 무관함</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2611.04624'>Polyp Matching Using Deep Learning</a></td><td>8</td><td>0</td><td>CV</td><td>캡슐 내시경 용종 매칭으로 로봇과 무관함</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2611.04709'>Learning from Unlabeled Photographs for General Oral Image Analysis</a></td><td>8</td><td>0</td><td>CV</td><td>구강 사진 자기지도 학습으로 로봇과 무관함</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2611.04734'>TEXMET: A Deep Learning Benchmark for Archaeological Textile Reconstruction</a></td><td>8</td><td>0</td><td>CV</td><td>고고학 직물 복원 벤치마크임</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2611.04940'>HTNN-MSC: Multi-view Subspace Clustering with a Hyperbolic Tangent Tensor Low-Rank Surrogate</a></td><td>8</td><td>0</td><td>LG</td><td>다중 뷰 subspace clustering 방법임</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2611.04946'>How Well Does Webcam Eye Tracking Work &quot;in the Wild&quot;? A Large-Scale Validation of Chiasm and a Comparison with WebGazer</a></td><td>8</td><td>0</td><td>CV</td><td>웹캠 시선 추적 검증 연구임</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2611.05049'>On the Learnability of Footwear Robustness: Footstep Recognition Under Unseen Conditions</a></td><td>8</td><td>0</td><td>CV</td><td>발자국 생체 인식 연구임</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2611.05145'>When Cell Crops Share a Parent: Measuring and Isolating Acquisition Leakage in Cervical Cytology Benchmarks</a></td><td>8</td><td>0</td><td>CV</td><td>자궁경부 세포 벤치마크 데이터 누수 분석임</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2611.05042'>Effects of Parton Pair Correlations on Direct-Photon Yields and Elliptic Flow in Heavy-Ion Collisions</a></td><td>8</td><td>0</td><td>LG</td><td>중이온 충돌 물리 연구임</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2611.04231'>Constructing a Regional Slang Lexicon for Electricity Demands via Soft-Label Bidirectional Anchoring and Active Learning</a></td><td>8</td><td>0</td><td>NLP</td><td>전력 지역 은어 사전 구축임. 로보틱스와 무관함</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2611.04406'>The Min-Max theory of language behavior</a></td><td>8</td><td>0</td><td>NLP</td><td>언어 행동 Min-Max 이론임. 로보틱스와 무관함</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2611.04627'>Evaluating LLMs as Judges of Counterspeech Quality Against Online Hate Speech</a></td><td>8</td><td>0</td><td>NLP</td><td>혐오 대응 발화 LLM judge 평가임. 로보틱스와 무관함</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2611.04685'>MIMIC-Note-Extract: A Large-Scale Structured Dataset Extracted from MIMIC-IV-Note Discharge Summaries</a></td><td>8</td><td>0</td><td>NLP</td><td>MIMIC 노트 추출 데이터셋임. 로보틱스와 무관함</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2611.04687'>CardioVascBench:Prioritized Diagnosis Generation from Real-World Chinese Cardiovascular Records</a></td><td>8</td><td>0</td><td>NLP</td><td>심혈관 진단 생성 벤치마크임. 로보틱스와 무관함</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2611.04921'>PROSE: Preservation-Constrained Selective Editing for Guilty Bias in Legal Judgment Prediction</a></td><td>8</td><td>0</td><td>NLP</td><td>법률 판결 편향 편집임. 로보틱스와 무관함</td></tr>
<tr><td>486</td><td><a href='https://arxiv.org/abs/2611.04949'>HERIT: Enabling Global Access to Hanja-to-English Historical Translation by Mitigating Temporal Bias</a></td><td>8</td><td>0</td><td>NLP</td><td>한자 영어 역사 번역임. 로보틱스와 무관함</td></tr>
<tr><td>487</td><td><a href='https://arxiv.org/abs/2611.04968'>Who is the Pronoun Pro? Comparing LLMs and Humans at Number-Disambiguation of &#x27;they&#x27;</a></td><td>8</td><td>0</td><td>NLP</td><td>대명사 수 판별 LLM 비교임. 로보틱스와 무관함</td></tr>
<tr><td>488</td><td><a href='https://arxiv.org/abs/2611.04645'>Therapy-FIS: A Dataset for Assessing Facilitative Interpersonal Skills in Psychotherapeutic Setting</a></td><td>5</td><td>0</td><td>NLP</td><td>심리치료 대화 기술 평가 데이터셋으로 로봇과 무관함</td></tr>
</tbody></table>

</details>
