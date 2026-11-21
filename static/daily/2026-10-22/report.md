# 오늘의 arXiv Top 15: 2026-10-22 (목)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**

**신규 논문 수: 전체 485편 → 중복 제거 후 485편 (이번 평가 대상 470편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 131 |
| cs.LG | 138 |
| cs.RO | 67 |
| cs.CL | 88 |
| cs.AI | 61 |

---

## Top 15

### 1. Reconstruction-Augmented Visuomotor Pre-Training of 3D-Grounded Bimanual Dexterity from RGB-Only Human Videos (77점)

[arXiv](https://arxiv.org/abs/2610.29716) · [PDF](https://arxiv.org/pdf/2610.29716) · [alphaXiv](https://www.alphaxiv.org/abs/2610.29716) (요약 있음) · [프로젝트 페이지](https://spatial-dex.github.io/)

- **저자**: Xingyi He, Zhiwen Qiu, Adhitya Polavaram, Yunhao Cao, Cory Fan, Julius Samwer, Saleh Kalantari, Kuan Fang
- **분야**: Manipulation · robotics relevance 10/10 · 1차 스크리닝 76점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> RGB만 있는 사람 영상 100만 클립에서 장면 3D 형상과 손 동작을 같은 scale로 맞춰 복원하고, 이 형상을 policy 입력과 예측 목표로 함께 써서 양손 dexterous policy를 사전학습함. 실로봇 양손 과제 6개의 성공률이 가장 강한 baseline π0.5의 43.3%에서 81.7%로 오름.

**무슨 문제인가**

양손 dexterous 조작은 손과 물체의 3D 위치 관계를 알아야 하지만, teleoperation으로 모은 로봇 demonstration은 비싸서 과제와 장면이 좁음. 인터넷의 사람 영상은 양이 많지만 RGB만 있어 장면 형상과 로봇이 쓸 수 있는 행동 label이 없음. 기존 사람 영상 사전학습 VLA는 주로 손목·손가락 동작만 supervision으로 쓰고, 주변 장면은 일부 점이나 keypoint로만 다룸. 단안 복원으로 형상을 얻어도 scale이 정해지지 않아 손 궤적과 장면 거리가 서로 어긋나는 문제가 있음.

**어떻게 푸나**

SpatialDex는 먼저 영상마다 손 추정기 HaWoR로 MANO 손 mesh와 손목 궤적을 얻고, VGGT-Omega로 장면 depth와 camera pose를 복원함. MANO 손 mesh가 실제 손 크기에 가까우므로, 복원 depth의 손 영역 점을 이 mesh에 맞춰 영상 전체에 하나의 scale과 frame별 rigid 변환을 함께 풂. policy는 PaliGemma VLM에서 시작해 RGB-D 영상, 손목·손가락 상태, 언어 지시를 받고, depth는 patch별 3D 점으로 바꿔 Sonata 점 encoder로 인코딩함. 형상 특징은 VLM 이미지 patch 격자에 맞춰 pooling한 뒤 두 sigmoid gate를 거쳐 RGB 특징에 residual로 더하고, 이 residual 가중치는 학습 초기에 0에서 1로 서서히 올림. 학습 때만 쓰는 형상 예측기가 16 step 뒤 patch별 3D 점을 예측해 Chamfer distance로 손실을 줌(forward dynamics 예측). 출력은 wrist expert가 양 손목 궤적을, finger expert가 그 궤적을 조건으로 손가락 동작을 만드는 두 diffusion transformer이고, 로봇에는 과제당 소수 demonstration과 센서 depth로 fine-tuning함.

**결과**

- 같은 영상·같은 학습량에서 형상 입력과 미래 형상 목표만 뺀 motion-only 사전학습과 비교함. DexJoCo(MuJoCo 기반 dexterous 조작 benchmark)의 Allegro 손 과제 6개 평균 성공률이 58.9%에서 73.1%로 14.2퍼센트포인트 오름. 사람 영상 사전학습이 없으면 45.6%임.
- 시뮬레이션 9개 과제(DexJoCo 과제 6개와 저자가 만든 Wuji 손 양손 과제 3개)에서 평균 성공률이 π0.5의 59.8%보다 높은 76.3%임. 과제당 demonstration 100개, seed 3개 평균이며, Pick Bucket은 π0.5가 84.0% 대 79.3%로 더 높음.
- 실제 Wuji 손과 Tianji 팔 양손 로봇에서 꽃 건네기, 물 붓기, 가방 지퍼 열기 등 6개 과제를 과제당 demonstration 50개로 학습함. 과제당 10회 시도 합계로 49/60(81.7%)을 성공했고, π0.5는 26/60(43.3%)임.
- 영상 전체 공통 scale 대신 frame별 scale 맞춤을 쓰면 6개 과제 평균이 73.1%에서 63.8%로 내림. forward dynamics 손실만 빼면 65.1%로 내림.

**한계**

사전학습 supervision의 품질은 손 추정과 단안 복원 정확도에 기대고, 공통 scale 맞춤으로 손 크기·자세·camera 움직임 오차를 다 고칠 수는 없음. 핵심 비교인 motion-only 대조는 형상 입력과 미래 형상 목표를 함께 빼므로 사전학습 단계에서 둘의 몫은 따로 보이지 않음. 배치 때 depth 센서와 새 로봇마다 demonstration이 필요하고, 실로봇 평가는 과제당 10회이며 코드 공개 여부는 원문에서 확인 불가함.

**누리랩 연구와의 연결**

- 사람 영상에서 3D 장면과 손 동작을 같은 좌표·scale로 맞추는 pipeline은 manipulation용 VLA 사전학습 데이터를 만들 때 바로 쓸 수 있는 방식임. 미래 장면 형상을 보조 목표로 예측하는 부분은 world model을 policy 표현 학습에 넣는 사례로 비교 대상이 됨.
- patch 격자에 3D 점 특징을 gate로 섞는 구조는 object-centric 3D 표현이나 active perception 결과를 기존 VLM 기반 policy에 넣을 때 참고할 수 있음.

*대표 그림: 측정 결과가 아니라 전체 흐름을 그린 개요 그림으로, 위쪽은 RGB 사람 영상에서 장면 형상과 손 동작(빨간 손 mesh)을 복원한 예이고 가운데는 RGB와 depth 격자를 맞춰 양손 행동을 내는 과정임. 아래쪽은 실로봇 평가 과제 6개(꽃 건네기, 식물에 분무, 쓰레기 쓸기, 물 붓기, 가방 지퍼 열기, 여행 가방 싸기)의 시작 장면임.*

*영상: [저자가 올린 양손 로봇의 꽃 건네기 과제 영상으로, 꽃병에서 꽃을 뽑아 다른 손에 넘기고 바구니에 넣는 장면임.](https://blog-media.assets.alphaxiv.org/videos/01a16222-5e53-7ac0-89e2-46a2c8b7485d/50827e66-1994-42d7-89dd-85dd02cdaecd) (alphaXiv 요약에서 가져옴)*

---

### 2. Real2Sem2Real: 3D Semantic Augmentations for Robot Learning from a Single Human RGB Demonstration (76점)

[arXiv](https://arxiv.org/abs/2610.28880) · [PDF](https://arxiv.org/pdf/2610.28880) · [alphaXiv](https://www.alphaxiv.org/abs/2610.28880) (요약 있음) · [프로젝트 페이지](https://real2sem2real.github.io/)

- **저자**: Matthew Strong, Ankush K. Dhawan, Julien Poffet, Giuse Pham, Jinho So, Monroe Kennedy
- **분야**: Manipulation · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> 사람이 머그를 커피 머신에 올리는 RGB 영상 1개로, 처음 보는 머그와 머신 조합까지 담은 로봇 demonstration 2,000개를 시뮬레이션에서 만듦. xArm7 머그 올리기 성공률이 같은 영상에서 같은 물체만 쓴 데이터의 36%에서 90%로 오름.

**무슨 문제인가**

사람 영상은 로봇 없이 쉽게 모을 수 있지만, 기존 방법은 depth 센서가 필요하거나 2D 영상 위에 로봇을 덧그려서 물체를 옮길 수 없음. RGB 영상 1개로 VLA를 학습시킨 Real2Render2Real(R2R2R)도 시연에 나온 그 물체의 위치만 바꿔서 데이터를 늘림. 그래서 다른 머그나 다른 커피 머신을 다루려면 조합마다 스캔과 시연을 새로 해야 함. 비슷한 물체로 바꿔 끼우는 digital cousin 방식도 있지만, 전체 모양이 비슷하다는 것만으로는 새 머신의 어디에 머그를 놓아야 하는지 정해지지 않음.

**어떻게 푸나**

R2Sem2R(Real2Sem2Real)의 입력은 사람 시연 RGB 영상 1개, 시연 물체의 휴대폰 스캔, 대체 물체(cousin)의 사진 몇 장이고 출력은 로봇 demonstration 수천 개임. 먼저 스캔을 DINOv3 feature가 입혀진 Gaussian splat으로 만들고, 영상의 각 frame에서 RGB·feature·silhouette·monocular depth 순위 loss를 줄이도록 물체의 SE(3) pose를 최적화함. 사람 손은 HaMeR(RGB 영상에서 손의 3D 자세를 복원하는 모델)로 복원해 엄지와 검지 끝을 기준으로 parallel-jaw gripper 파지로 옮기고, 충돌이 없는 파지를 고름. cousin은 사진에서 SAM3D 계열 모델로 생성한 뒤, DINOv3 feature가 같은 부위끼리만 짝을 짓는 ICP로 시연 물체에 맞춤. 이어서 머신의 트레이나 머그 테두리처럼 과제에 중요한 부위의 점에 20배 가중치를 주고 다시 맞춰서, 시연의 물체 간 관계가 cousin 조합에서도 유지되게 함. 정렬된 궤적과 파지로 inverse kinematics를 풀고 IsaacSim이나 MuJoCo에서 episode를 렌더링함.

**결과**

- xArm7 머그 올리기(머그 7개·머신 7개로 평가하고, 그중 각 3개는 teleoperation 데이터에 없는 물체임)에서 50회 중 45회 성공해 90%임. 같은 영상과 같은 pipeline으로 시연 물체만 쓴 2,000 episode(R2R2R+)는 36%, 여러 물체에서 모은 teleoperation 150개는 62%임.
- 과제 4개(올리기, 붓기, 걸기, 드릴 세우기)와 로봇 2대(xArm7, Franka Panda) 모두에서 R2R2R+보다 26~54퍼센트포인트 높음. teleoperation과는 같거나 높고, 드릴 세우기는 두 로봇 모두 teleoperation과 같은 값(xArm7 85%, Franka Panda 65%)임.
- 같은 2,000 episode를 IsaacSim 대신 MuJoCo로 만들면 xArm7 올리기 성공률이 90%에서 62%로 내려감. RGB만 보는 policy에는 접촉 물리보다 화면 사실감이 더 중요했다고 저자는 해석함.
- 물체 tracking은 7개 물체 평균 mask IoU가 0.913임. 추정 depth를 영상마다 보정해 준 FoundationPose는 0.823, WARPED는 0.681임.

**한계**

영상 1개만 쓰는 것은 아님: 시연 물체의 스캔과 실제 크기, cousin의 사진과 높이가 필요함. 단단한 물체만 다루고, IsaacSim 재생은 손가락과 물체의 접촉을 계산하지 않아서 접촉이 많은 과제에는 맞지 않음. 실로봇 평가는 과제 4개에 과제당 50회(드릴 40회)이고, 본문에 코드 공개 주소는 없음.

**누리랩 연구와의 연결**

- 사람 영상 1개에서 object-centric 3DGS로 pose를 추적하고 DINOv3 feature로 부위를 맞추는 구조라서, VLA manipulation 데이터 생성과 object-centric 3DGS 연구에 그대로 가져다 쓸 수 있음.
- 과제에 중요한 부위만 가중해서 맞추는 정렬은, 물체가 바뀌었을 때 어느 부위 관계가 어긋나 실패했는지 따지는 failure diagnosis의 기준으로도 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 위에서부터 사람 RGB 영상과 물체 스캔을 cousin에 semantic alignment로 맞추는 단계, 과제 4개와 로봇 2대로 합성 데이터를 만드는 단계, fine-tuning한 VLA가 실제 xArm7과 Panda에서 과제를 수행한 장면을 보여 줌.*

*영상: [시뮬레이션의 xArm7이 cousin 머그를 cousin 커피 머신에 올리는 장면을, 원래 사람 시연과 함께 작은 창으로 보여 주는 저자 영상임.](https://blog-media.assets.alphaxiv.org/videos/01a16137-4b65-7b12-a0bb-aeca5b6cc970/00c40294-e8e9-458a-b9dd-e9a68a1ed89b) (alphaXiv 요약에서 가져옴)*

---

### 3. T-WLA: Bridging Slow Vision and Fast Touch with a World-Language-Action Model (74점)

[arXiv](https://arxiv.org/abs/2610.28814) · [PDF](https://arxiv.org/pdf/2610.28814) · [alphaXiv](https://www.alphaxiv.org/abs/2610.28814) · [프로젝트 페이지](https://t-wla.github.io/)

- **저자**: Kaichen Zhou, Yuzhen Chen, Hannah Yao, Chonghe Jiang, Rao Fu, Xihang Yu, Wei Dai, Bashar Kabbarah 외 12명
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 78점
- **읽은 원문**: PDF 전문

> 느린 시각 policy가 만든 action chunk를, 시각 branch를 다시 돌리지 않고 촉각 입력으로 실행 도중에 고치는 구조를 제안함. 실제 dexterous hand 과제 4개의 평균 성공률이 시각과 촉각을 서로 다른 주기로 처리하는 기존 policy T-Rex의 23.0%에서 51.0%로 오름.

**무슨 문제인가**

물체를 잡거나 끌어당기는 조작에서는 접촉 상태가 시각 policy의 다음 갱신보다 빨리 바뀜. 대부분의 VLA는 시각과 언어만 입력으로 받으므로, 이미지로 잘 안 보이는 미끄러짐이나 힘 변화에 늦게 반응함. 접촉이 바뀔 때마다 시각 policy를 다시 돌리면 지연이 생김. 반대로 촉각 신호만으로는 과제 맥락을 모르므로 진행 중인 동작을 어떻게 고칠지 정하기 어려움.

**어떻게 푸나**

T-WLA(Tactile World-Language-Action)는 느린 시각 branch와 빠른 촉각 editor를 하나의 visual memory로 잇는 구조임. 시각 branch는 현재 RGB 이미지, 언어 지시, 손 상태와, 지난 8번의 시각 갱신에서 저장한 visual memory를 학습된 query로 요약한 값을 vision-language model에 넣어 새 visual memory를 만듦. action expert는 이 visual memory를 조건으로 flow matching으로 8단계 base action chunk를 만들고, 이 둘은 다음 시각 갱신까지 고정함. 그 사이 촉각이 들어올 때마다 작은 Transformer가 visual memory, base chunk, 경과 시간으로 action feature를 만들고, 촉각 feature가 FiLM(곱하고 더할 값을 촉각에서 계산하는 조절)으로 이를 조절함. 출력은 아직 보내지 않은 action에 더할 residual 보정값이며, 보정은 이전 보정 위가 아니라 원래 base chunk에 더함. 먼저 사람 손 데이터로 미래 손 자세를 예측하도록 학습하고(미래 이미지·압력 보조 head는 학습 때만 붙임), 로봇에는 과제당 teleoperation 30개로 맞춤.

**결과**

- EgoTouch(egocentric 영상과 손 촉각을 함께 기록한 데이터셋, 5개 환경)에서 100ms 뒤 손 자세를 예측함. 손목 기준 손가락 관절 오차(MPJPE)가 가장 강한 baseline의 0.50cm에서 0.35cm로 내림. Tachin(촉각 장갑 데이터셋)에서는 가장 강한 baseline(VITRA + tactile)의 0.63cm에서 0.46cm로 내림.
- 같은 H100 GPU에서 계산만 잰 촉각 보정 빈도는 T-WLA가 119.1Hz, 가장 빠른 baseline(SmolVLA + tactile)이 69.0Hz임.
- 양팔 Linker A7 로봇과 Linker Hand L6 손으로 과제 4개(달걀 옮기기, 종이 한 장 집기, 종이컵 포개기, 종이봉투 끌기)를 과제당 시연 30개로 학습함. 평균 성공률은 T-WLA 51.0%, T-Rex 23.0%, SmolVLA + tactile 17.0%임. 과제당 시도 횟수는 본문에서 확인 불가함.
- 같은 구조에서 촉각만 뺀 T-WLA는 평균 44.25%임. 촉각 editor가 더한 몫은 6.75퍼센트포인트이고, 촉각 없이도 T-Rex보다 21.25퍼센트포인트 높음.

**한계**

실로봇 성공률 향상의 대부분은 촉각보다 시각 branch와 memory에서 나오므로, 촉각 보정 효과는 과제별 4~9퍼센트포인트 수준임. 미래 이미지·압력 예측을 빼도 손 자세 예측 오차가 평균 1.0%만 오르므로 world model 성격의 보조 학습이 하는 일은 작음. 실제 하드웨어 지연 측정은 팔을 움직이지 않는 조건이었고, 실제 하드웨어의 보정 출력은 14.5Hz였으며 매 보정마다 새 촉각이 들어오는지는 확인되지 않음.

**누리랩 연구와의 연결**

- 실행 중인 action chunk를 다시 계획하지 않고 빠른 센서로 고치는 residual editor 구조는, VLA 실행 중 failure detection과 즉시 recovery를 붙이는 설계의 비교 대상이 됨.
- 지난 visual memory를 query로 꺼내 쓰는 방식이 촉각 없이도 성공률을 크게 올린 결과는 robot memory 연구의 근거로 쓸 수 있음.

*대표 그림: 세 칸으로 된 개요 그림으로, 왼쪽 위는 촉각 유무로 나눈 사람 손 시연 데이터, 왼쪽 아래는 시간에 따라 색이 바뀌는 미래 손 자세 예측임. 오른쪽은 촉각이 있으면 달걀을 잡아 들고 없으면 접촉만 하거나 미끄러지는 로봇 장면과, 한 visual memory 아래에서 촉각 6번으로 action a1~a6를 고치는 구조도임.*

---

### 4. Plan First, Act Later: Streaming Reasoning for Executable Memory in Robot Control (74점)

[arXiv](https://arxiv.org/abs/2610.29329) · [PDF](https://arxiv.org/pdf/2610.29329) · [alphaXiv](https://www.alphaxiv.org/abs/2610.29329) (요약 있음) · [프로젝트 페이지](https://qinghangliu.github.io/pal-webpage/)

- **저자**: Qinghang Liu, Conglin Wang, Zongsheng Li, Boyong He, Han Gao, Pengcheng Wang, Tao Sun, Lige Liu 외 1명
- **분야**: Robot Memory · robotics relevance 10/10 · 1차 스크리닝 74점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> 고수준 VLM이 영상 증거가 보이는 순간 나중에 할 subtask를 미리 목록에 적어 두고, 실행할 때는 그 목록에서 꺼내 VLA에 넘기게 함. 기억이 필요한 조작 과제 모음 RoboMME의 평균 성공률을 가장 강한 baseline의 44.51%에서 56.05%로 올림.

**무슨 문제인가**

VLA는 대개 현재 관측이나 최근 몇 frame만 보고 행동을 정하므로, 앞서 잠깐 보였다 사라진 정보가 필요한 과제에서 실패함. 이를 보완하려고 과거 관측을 memory bank에 쌓아 두는 방법(MemER 등)이 나왔음. 그러나 이 방법들은 실행 시점마다 고수준 모델이 큰 memory bank를 뒤져 다음 subtask를 추론해야 함. bank에는 겹치는 정보가 많아 필요한 정보를 찾기 어렵고, 저장된 이력이 길어질수록 계산도 늘어남.

**어떻게 푸나**

PAL(Plan first, Act Later)은 최근 RGB frame을 담는 visual buffer, 사건을 문장으로 적는 semantic-event memory, 실행할 subtask 문장을 차례로 담는 subtask list를 둠. 매 query마다 고수준 VLM(Qwen3-VL-4B)은 지난 memory, 새 image chunk, 과제 지시문을 받아 새 event, 목록에 덧붙일 새 subtask, 지금 실행할 subtask를 하나씩 내며, 증거가 부족하면 앞의 두 칸은 비워 둠. memory가 갱신되면 visual buffer를 비우고, subtask가 추가되면 event memory도 비워서 문맥이 길어지지 않게 함. 선택된 subtask 문장은 저수준 VLA(MemER와 같은 사전학습 VLA)가 받아 행동으로 바꿈. 학습은 두 단계로, Stage 1은 한 시점에만 달린 갱신 label을 앞뒤 query로 늘려 증거가 부족한 앞쪽에는 '갱신 없음', 뒤쪽에는 정답 갱신을 붙임. Stage 2는 Stage 1 모델을 학습 데이터에서 직접 돌려, 틀리거나 되풀이한 갱신을 지우고 필요한 갱신을 제때 다 한 rollout만 남겨 다시 fine-tuning함(self-labeling).

**결과**

- RoboMME(기억이 필요한 시뮬레이션 조작 과제 16개 모음)의 평균 성공률이 PAL 56.05%, FrameSamp-Modul 44.51%, MemER 42.38%, GPT-6-astra를 고수준 모델로 쓴 경우 39.75%임. FrameSamp-Modul은 과거 frame의 시각 feature로 action expert를 조절하는 방법임. 16개 과제 중 PAL이 가장 높은 과제는 4개뿐임.
- 긴 조건 영상을 보고 목록을 만드는 Long-video 묶음에서 성공률이 FrameSamp-Modul의 46.00%에서 81.60%로 오름. 처음부터 정보가 다 주어지는 Episode-start 묶음에서는 같은 VLA를 쓰는 MemER의 65.11%보다 12.22퍼센트포인트 높은 77.33%임.
- 학습 단계 ablation에서 평균 성공률은 Stage 1만 쓰면 37.35%, 한 시점 label만 쓰면 43.39%, 두 단계를 다 쓰면 56.05%임. 과제 4개에서 Stage 1만 쓴 모델은 정답보다 34~44% 더 자주 목록을 고치고, 최종 목록 정확도는 18~30%임. PAL은 갱신 빈도가 정답과 6.4% 이내로 맞고 최종 목록 정확도는 54~84%임.
- 실제 Franka Research 3 로봇 과제 4개에서 과제당 30회 평가한 전체 성공률이 PAL 60.83%, MemER 45.00%, FrameSamp-Modul 28.33%임. 박스를 정해진 횟수만큼 집는 PickXtimes에서 MemER는 0%, PAL은 53.33%임.

**한계**

subtask list가 순서만 있는 목록이라 실행 중 관측에 따라 갈라지는 조건 분기를 담지 못함. RoboMME의 MemER, FrameSamp-Modul 수치는 RoboMME 논문 보고값을 그대로 가져온 것이라 PAL과 평가 횟수가 같지 않음. 학습에 사건·subtask 정답 label이 필요하고, 저자는 문맥이 줄어든다고 주장하지만 지연 시간이나 계산량은 재지 않음.

**누리랩 연구와의 연결**

- 관측을 사건 문장과 실행할 subtask 목록으로 바꿔 두는 robot memory 구조로, VLA의 long-horizon 기억 연구에서 비교 대상으로 쓸 수 있음.
- 모델 자신의 rollout에서 정답과 맞는 갱신만 남겨 다시 학습하는 Stage 2 방식은, 고수준 VLM의 failure detection이나 진행 상태 판단을 학습할 때 데이터 분포를 맞추는 방법으로 참고할 만함.

*대표 그림: 왼쪽은 방법 구조, 오른쪽은 성공률 막대그래프인 개요 그림으로, 왼쪽은 증거가 보인 t1에 'pick up the blue cube'를 subtask list에 미리 적어 t2에 VLA로 넘기는 과정임. 오른쪽 막대그래프는 시뮬레이션과 실로봇에서 PAL이 가장 강한 baseline보다 각각 11.5, 15.8퍼센트포인트 높은 성공률을 보임.*

*영상: [저자가 올린 VideoUnmask 시뮬레이션 성공 장면으로, 용기가 초록 큐브를 가린 뒤에도 위치를 기억해 그 용기를 들어 올리는 영상임.](https://blog-media.assets.alphaxiv.org/videos/01a16137-9570-7ecc-883c-bc0715b4756f/1a4d5c07-ddf2-47e2-91b1-9974fba06826) (alphaXiv 요약에서 가져옴)*

---

### 5. GeoMem-VLA: Internalizing 3D Scene Understanding into Temporal Memory for Vision-Language-Action Models (72점)

[arXiv](https://arxiv.org/abs/2610.29866) · [PDF](https://arxiv.org/pdf/2610.29866) · [alphaXiv](https://www.alphaxiv.org/abs/2610.29866) (요약 있음)

- **저자**: Qinfan Zhang, Yifan Luo, Haoyuan Shi, Guanlin Liu, Han Dong, Haozhe Shan, Yong Dai, Xiangcong Ren 외 1명
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 88점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> VLA에 3D 기하를 학습한 별도 token을 두고, 그 token을 episode 안의 memory로 저장해 꺼내 쓰게 함. RoboTwin 2.0 양팔 과제 50개에서 기하 branch를 뺀 같은 모델보다 평균 성공률이 89.71%에서 91.17%로 오름.

**무슨 문제인가**

대부분의 VLA는 현재 프레임의 2D 관측만 보고 행동을 정함. 3D를 쓰는 VLA도 매 시점 관측에서 기하를 따로 추정하고 다음 시점에는 버림. 그래서 수건으로 사과를 덮은 뒤 다시 찾는 과제처럼 지금 화면에 안 보이는 공간 정보가 필요한 경우를 다루기 어려움. 저자들은 행동 생성에 필요한 것은 매 시점의 완전한 3D 복원이 아니라, 시간에 따라 갱신되는 작은 기하 요약이라고 주장함.

**어떻게 푸나**

GeoMem-VLA는 Qwen3-VL-4B를 backbone으로 쓰고 GR00T 방식의 flow-matching action expert로 행동 chunk를 출력함. 입력은 여러 시점 RGB 영상, 로봇 상태, 언어 지시이고, 여기에 학습 가능한 GeoPlan token(기하 정보를 담도록 학습하는 추가 token) K개를 덧붙임. 학습 때는 보조 head가 GeoPlan token을 조건으로, 고정된 VGGT(RGB에서 3D point map을 추정하는 모델)의 현재 point map과 미래 end-effector 궤적을 예측함. GeoPlan token과 관측 token은 시점별로 별도 memory bank에 저장되고, 매 step 현재 token이 같은 episode의 과거 항목을 attention으로 검색해 gate로 관측 token에 섞음. bank 용량이 차면 이웃한 항목 쌍 가운데 가장 비슷한 쌍을 평균으로 합쳐, 장면이 바뀐 시점의 항목이 남도록 함. 추론 때는 VGGT와 복원 head를 떼어 내므로 3D 복원 없이 행동을 냄.

**결과**

- RoboTwin 2.0(양팔 조작 과제 50개, Clean과 장면을 무작위로 바꾼 Randomized 두 설정)에서 과제당 100회 평가함. 두 설정 평균 성공률이 전체 모델 91.17%, 기하 branch 제거 89.71%, memory 제거 90.18%, 바탕 모델인 StarVLA-GR00T 88.25%임.
- LIBERO(시뮬레이션 조작 과제 10개씩 묶은 suite 4개)에서 4개 suite 평균 성공률이 98.9%임. 표에 실린 최고 기존 방법인 3DThinkVLA 98.7%, Spatial Forcing 98.5%와 차이가 작음. 긴 과제 묶음(Long)에서는 memory를 빼면 96.6%에서 94.2%로 내림.
- 실로봇 양팔 플랫폼 2종(Astribot S1, AgileX)에서 과제 5개를 과제당 60개 demonstration으로 학습하고 10회씩 평가함. 평균 성공률은 78.0%이고, 수건에 가려진 사과 찾기 80%, 정해진 횟수만큼 큐브 옮기기 50%임. 비교한 π0.5, LingBot-VLA 2.0, OpenVLA-OFT의 과제별 수치는 본문 텍스트에서 정확히 확인 불가함.

**한계**

LIBERO와 RoboTwin의 기존 방법 비교는 각 논문이 보고한 값을 옮긴 것이라 학습 데이터와 평가 조건이 다름. 통제된 비교인 ablation에서 차이는 1~1.5퍼센트포인트 수준이고, 기하 branch 제거는 supervision·token·memory bank·gate를 한꺼번에 빼므로 어느 요소가 효과를 내는지 가를 수 없음. 실로봇 평가는 과제당 10회뿐이며, 추론 시간이나 memory 비용은 측정하지 않았고 코드는 출판 후 공개 예정임.

**누리랩 연구와의 연결**

- 3D 기하를 latent token으로 요약해 episode memory에 저장하는 설계는 robot memory 연구에서 MemoryVLA(과거 관측을 memory bank에 쌓아 검색하는 VLA), Spatial Forcing과 함께 비교 대상이 됨.
- 가림이 생기는 과제(수건 아래 사과)와 횟수 세기 과제는 memory가 필요한 실패 사례를 만들 때 참고할 수 있음. 다만 failure detection이나 recovery를 직접 다루지는 않음.

*대표 그림: 방법 구조와 성능 요약을 한데 그린 개요 그림으로, 위쪽은 수건에 가려진 사과 위치를 기억해 집는 예시이고 가운데는 GeoPlan token 학습(학습 때만 사용)과 memory 검색·gate 융합으로 행동을 내는 부분임. 아래쪽 막대그래프는 LIBERO, RoboTwin, 실로봇에서 기존 VLA와 성공률을 비교함.*

---

### 6. CW-WAM: A Structured Contact-Wrench World Action Model for Force-Sensitive Manipulation (72점)

[arXiv](https://arxiv.org/abs/2610.30117) · [PDF](https://arxiv.org/pdf/2610.30117) · [alphaXiv](https://www.alphaxiv.org/abs/2610.30117) (요약 있음) · [프로젝트 페이지](https://cw-wam-project.github.io/)

- **저자**: Houzhu Ding, Xinda Qi, Luqi Wang, Ming Yang
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 74점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 8쪽
- **읽은 원문**: PDF 전문

> video와 action을 함께 예측하는 world action model에 손목 힘·토크 센서 값을 입력과 출력으로 넣어, 동작과 그때 받을 접촉력을 짝지어 예측하게 함. 면당 틈이 1mm인 사각 peg 끼우기 성공률이 힘 정보 없는 모델의 25%에서 70%로 오름.

**무슨 문제인가**

WAM(world action model)은 앞으로의 영상과 action을 함께 예측해 조작 동작을 만드는 모델임. 하지만 영상에는 접촉력이 보이지 않음. 구멍에 걸린 peg가 다 들어간 것처럼 보이거나, 겉모습이 같은 상자의 무게가 크게 다를 수 있음. 손목 F/T(force-torque) 센서가 이 정보를 주지만, 기존 WAM은 wrench(3축 힘과 3축 토크를 묶은 값)를 다루지 않음.

**어떻게 푸나**

CW-WAM은 DreamZero(영상과 action을 함께 생성하는 기존 WAM) 계열 video-action backbone(Wan2.2 5B DiT)에 상호작용 모듈을 붙임. 입력은 카메라 3대의 RGB, 언어 지시, 로봇 상태, 과거 이력임. 과거 이력은 최근 1.6초 동안의 동작 명령과 같은 구간에서 잰 wrench를 짝지은 token과, 10초 길이의 wrench 전용 기억(LTM, long-term wrench memory)으로 이루어짐. 출력은 앞으로 1.6초 동안의 동작 24개와 각 동작 시점의 예상 wrench 24개이며, 둘은 token·prediction head·loss를 따로 씀. pair-causal attention은 미래의 각 wrench가 짝이 되는 동작과 앞선 짝들만 보게 하고, 동작은 같은 짝의 wrench를 보지 못하게 함. 실행할 때는 예측 wrench를 기준값으로 측정 wrench와의 차이로 자세를 고치는 admittance 제어를 20Hz로 돌려, 0.5~0.6초 걸리는 모델 추론 사이에도 힘 feedback이 이어짐.

**결과**

- 실제 Franka 로봇에서 과제마다 20회 시도함. 사각 peg 끼우기(38mm peg를 40mm 구멍에 약 50mm 깊이로 넣기) 성공이 힘 정보 없는 WAM의 5회에서 CW-WAM의 14회로 늘어남. 전원 어댑터 끼우기는 8회에서 19회로 늘어남.
- wrench 이력을 한 덩어리로 넣고 action과 wrench를 이어 붙여 예측한 WAM + Wrench와 비교함. peg 끼우기는 8회 대 14회, 어댑터 끼우기는 9회 대 19회임. LTM을 빼면 peg 성공이 14회에서 7회로 내려감.
- 겉모습이 같은 30g·830g 상자를 용수철 저울로 들어 옮기는 과제에서 CW-WAM의 최고 높이 중앙값은 가벼운 상자 423.6mm, 무거운 상자 481.8mm임. 시연 중앙값은 420.9mm와 492.7mm임. WAM은 464.4mm와 447.3mm로 무거운 상자를 더 높이 들지 않음.
- 예측 wrench로 admittance 제어를 더하면 기준 힘과 측정 힘의 RMSE가 peg 끼우기에서 4.8N에서 2.7N으로, 칠판 닦기에서 2.0N에서 1.3N으로 내려감. 성공률은 그대로임.

**한계**

실험은 과제 4개이고 물체는 시연 때와 비슷한 위치에만 놓았으며, admittance 이득과 힘을 받아들일 방향은 과제마다 손으로 정함. 어댑터 끼우기에서는 성공률이 오른 대신 기준 힘 RMSE가 WAM + Wrench의 2.53N보다 큰 8.37N이었음. 힘을 예측하는 다른 WAM인 FAWAM과 직접 비교하지 않았고, 코드 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- world model이 영상과 action 외에 접촉력까지 예측하게 한 사례임. 예측 wrench와 측정 wrench의 차이는 끼임 같은 접촉 실패를 실행 중에 감지하는 failure detection 신호로 바로 쓸 수 있음.
- 느린 VLA·WAM 추론 사이를 빠른 힘 feedback으로 메우는 구조는 contact-rich manipulation에서 test-time 보정을 설계할 때 참고할 만함.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림으로, 영상·언어·로봇 상태와 action-wrench 이력, 긴 wrench 기억이 Causal DiT로 들어가 video·action·wrench를 함께 denoising함. 오른쪽은 예측된 action chunk와 wrench chunk가 slow-fast 동작·힘 제어로 로봇 실행에 쓰이는 흐름임.*

*영상: [저자 프로젝트 페이지에 올라온 사각 peg 끼우기 과제의 실제 로봇 영상임.](https://blog-media.assets.alphaxiv.org/videos/01a16172-efd1-7a6b-b3fa-bd6fdac78f19/b8a3ee74-b72e-4301-8dfa-fe356cdb30cf) (alphaXiv 요약에서 가져옴)*

---

### 7. Training in Deployment: Human-in-the-loop Online Post-Training for Robot Manipulation (72점)

[arXiv](https://arxiv.org/abs/2610.29264) · [PDF](https://arxiv.org/pdf/2610.29264) · [alphaXiv](https://www.alphaxiv.org/abs/2610.29264) (요약 있음) · [프로젝트 페이지](https://logosintelligencelab.github.io/TIDE/)

- **저자**: Chun Gu, Xiaofei Wei, Yiming Chen, Bozhou Zhang, Juntong Zhang, Xiatian Zhu, Li Zhang
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 72점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> 실로봇 배포 중에 사람이 개입한 action과 policy가 직접 실행한 action을 출처 label로 구분해 그 자리에서 policy를 계속 학습시키는 시스템 TIDE를 만듦. critic이나 reward model 없이 양팔 조작 과제 4개의 완주 횟수가 20회 중 4~6회에서 13~17회로 오름.

**무슨 문제인가**

사전학습된 robot foundation model을 offline teleoperation demonstration으로 목표 과제에 맞추면, 배포 중 policy가 스스로 만든 접촉·복구·정밀 상태를 demonstration이 덮지 못함. human-in-the-loop 방법은 사람이 개입한 구간만 demonstration으로 쓰고 policy가 실행한 구간은 버리는 경우가 많음. 또 수집 후 다시 offline으로 학습하는 주기를 따르므로 배포 경험이 바로 반영되지 않음. online RL은 policy 실행 데이터도 쓰지만 성공·실패 같은 희소한 결과로 value function을 학습해야 해서 긴 action chunk를 안정적으로 평가하기 어려움.

**어떻게 푸나**

TIDE(Training In DEployment)는 로봇 client, 추론·기록 server, online learner를 한 배포 세션 안에서 비동기로 묶음. policy는 video generation backbone과 flow-matching action expert로 된 30억 parameter world-action 모델로, 관측과 지시를 받아 50 step 양팔 action chunk와 미래 영상을 함께 예측함. 로봇이 policy action을 실행하다 필요할 때 사람이 VR로 개입하고, 시스템은 각 step의 action이 사람과 policy 중 누구에게서 나왔는지(provenance)를 기록함. 50 step 전체가 한 출처인 chunk만 사람 또는 policy label을 받고, 두 출처가 섞인 chunk는 학습에서 뺌. 각 label을 학습 가능한 embedding으로 바꿔 backbone과 action expert에 조건으로 넣고, offline 데이터와 함께 flow-matching loss로 text encoder와 video VAE를 뺀 모든 모듈을 갱신함. 새 checkpoint는 5개 episode마다 나오며 episode 경계에서만 교체되고, 평가 때는 사람 출처 조건으로 고정해 실행함.

**결과**

- 양팔 UR5e 과제 4개(나사 비트 꽂기, 수건 접기, 수건 걸기, 쇠사슬 상자에 담기)에서 사람 개입 없이 과제당 20회 평가함. 단계별 완료 비율로 잰 task progress가 warm-start(offline demonstration으로만 맞춘 시작 policy)와 추가 offline demonstration 기준선은 21.7~55%였고 TIDE는 78.3~88.3%였음. 완주 횟수는 두 기준선이 20회 중 4~6회임.
- 같은 시간 동안 policy를 고정한 채 데이터를 모은 뒤 같은 예산으로 학습한 Fixed Policy와는 최종 성능이 비슷함. 완주 횟수는 TIDE가 16, 13, 17, 16회, Fixed Policy가 16, 12, 16, 14회임. 차이는 TIDE의 checkpoint가 배포 세션 도중에 갱신된다는 점이며, 과제당 배포 시작부터 마지막 checkpoint까지 1시간 미만이 걸림.
- 나사 비트 꽂기에서 task progress가 TIDE 80.0%, 출처 조건을 뺀 경우 65.0%, 사람 개입 chunk만 쓴 경우 67.5%임. 이 ablation은 과제 1개에서만 했음.

**한계**

사람 감독자가 늘 있어야 하고, 사람이 성공으로 확인한 episode만 학습에 넣어 선택 편향이 생길 수 있음. 실험은 로봇 플랫폼 1개, 과제 4개, backbone 1개뿐이며 반복 세션 간 편차나 통계 검정은 없음. 배포가 진행될수록 사람 개입 비율이 줄었다는 관찰도 나사 비트 꽂기 한 세션의 결과이고 학습 효과와 시간 요인을 분리하지 않았음.

**누리랩 연구와의 연결**

- 배포 중 실패 상황에서 사람이 개입한 데이터를 바로 policy 개선에 쓰는 구조라서, failure detection과 recovery 연구에서 사람 개입 대신 자동 실패 감지기를 넣는 확장의 출발점이 됨.
- value function 없이 action 출처만 조건으로 주는 방식은 VLA를 실로봇에서 online으로 post-training할 때 RL 대신 비교할 baseline으로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 TIDE 시스템 구조를 그린 그림임. 양팔 UR5e와 다중 카메라 환경, 사람 개입과 policy 실행이 오가는 client, 언어와 provenance를 받아 video model과 action expert를 학습하고 다시 배포하는 server/learner의 순환을 보여 줌.*

*영상: [양팔 UR5e가 사람 개입 없이 TIDE policy로 수건을 펴고 두 번 접는 장면을 찍은 영상임.](https://blog-media.assets.alphaxiv.org/videos/01a176cb-fcd7-7516-9ce8-57688b6463a8/7087f929-7f2e-4276-a735-ba3f32c57bb3) (alphaXiv 요약에서 가져옴)*

---

### 8. Doob-Based Generative Policy Optimization (72점)

[arXiv](https://arxiv.org/abs/2610.28990) · [PDF](https://arxiv.org/pdf/2610.28990) · [alphaXiv](https://www.alphaxiv.org/abs/2610.28990) (요약 있음) · [프로젝트 페이지](https://maojiangsu.github.io/DoobPO/)

- **저자**: Maojiang Su, Qijie Zhu, Yu Xiao, Shuyang Yu, Minshuo Chen, Zhaoran Wang, Han Liu
- **분야**: RL · robotics relevance 8/10 · 1차 스크리닝 74점
- **학회**: NeurIPS 2026 채택 · 근거: comments에 "38 pages, 4 figures. Accepted at NeurIPS 2026"
- **읽은 원문**: PDF 전문

> diffusion·flow policy의 action likelihood를 계산하지 않고도 PPO·GRPO 갱신 규칙으로 RL 학습을 할 수 있게 함. MuJoCo HalfCheetah의 flow policy 평균 return을 기존 방법 ReinFlow의 1,344에서 6,368로 올림.

**무슨 문제인가**

diffusion·flow policy는 여러 갈래로 나뉘는 행동 분포를 표현할 수 있어 로봇 policy로 많이 쓰임. 행동 하나가 denoising이나 velocity 적분 전체를 거쳐 나오므로, 그 행동의 확률(likelihood)을 정확히 계산하기 어려움. PPO·GRPO(GRPO: 표본 묶음 안에서 보상을 정규화하는 PPO 변형)는 새 policy와 이전 policy의 확률 비(probability ratio)로 갱신 폭을 조절하므로 이 policy에 그대로 쓸 수 없음. 기존 우회 방법들은 추정 편향, 큰 계산량, 특정 policy 종류나 갱신 규칙에만 맞는다는 제약이 있다고 저자는 정리함.

**어떻게 푸나**

DoobPO(Doob Policy Optimization)는 policy를 어느 쪽으로 바꿀지 정하는 단계와 생성 모델을 그쪽으로 학습시키는 단계를 나눔. 첫 단계에서 작은 MLP인 ratio model이 상태와 행동을 받아, 그 행동의 확률을 이전 policy보다 몇 배로 할지 양수로 출력함. ratio model은 이전 policy로 모은 데이터에서 PPO나 GRPO 목적식의 확률 비 자리에 들어가 학습되고, 이전 policy 아래 기댓값이 1이 되도록 정규화됨. 두 번째 단계의 목표는 이전 policy를 이 ratio로 다시 가중한 분포이고, Doob h-transform(끝점 분포를 바꿀 때 확률 과정의 drift를 어떻게 고칠지 주는 정리)으로 필요한 drift 보정을 정의함. 이 보정은 직접 계산할 수 없으므로, 이전 policy 샘플에 ratio를 가중치로 곱한 denoising 회귀 loss(conditional drift matching)로 score network를 학습함. flow policy도 ratio를 곱한 velocity 회귀로 같은 방식으로 학습하며, 출력은 갱신된 score 또는 velocity network임.

**결과**

- MuJoCo 10개 과제(시뮬레이션 보행·조작·균형 제어)에서 flow policy를 처음부터 5M step 학습함. seed 3개 평균 return이 HalfCheetah에서 가장 강한 baseline ReinFlow의 1,344에서 DoobGRPO의 6,368로 오르고, Walker2d에서 503에서 4,215로 오름. 10개 중 9개 과제(동점 포함)에서 평균이 가장 높음.
- 같은 10개 과제에서 diffusion policy를 4M step 학습하면 diffusion RL 방법 중 8개 과제(동점 포함)에서 평균이 가장 높음. HalfCheetah는 DoobPPO 14,921 대 SDAC 14,731로 차이가 작고, Ant·Hopper는 DACER가 앞섬(7,137 대 6,738, 3,774 대 3,681).
- Robomimic(로봇 팔 조작 시뮬레이션 benchmark)의 Can·Square 과제를 성공 여부만 reward로 주고 같은 behavior cloning policy에서 fine-tuning함. 성공률은 DoobPPO와 DPPO(diffusion policy를 PPO로 fine-tuning하는 기존 방법)가 거의 같음: Can 99.46% 대 99.23%, Square 99.78% 대 99.59%.

**한계**

실험은 모두 저차원 상태 입력 시뮬레이션이고 이미지 입력이나 실로봇 실험은 없음. Gaussian policy인 SAC가 Walker2d에서 6,882로 diffusion policy DoobPPO의 5,642보다 높아, MuJoCo에서는 생성 policy를 쓰는 이득 자체가 분명하지 않음. 이론 보장은 diffusion policy이고 ratio model이 정확히 학습된다는 가정에서만 성립함. flow 쪽 loss는 근사이며, ratio 추정 오차의 영향은 저자도 미해결로 남김.

**누리랩 연구와의 연결**

- π0 같은 flow 기반 VLA를 likelihood 계산 없이 PPO·GRPO로 RL fine-tuning하는 경로임. VLA를 rollout 결과로 고치는 연구에서 ReinFlow·DPPO와 함께 비교 대상이 됨.
- 바꿀 방향을 별도의 ratio model로 표현하므로, failure detection 결과로 실패 행동의 ratio를 낮춰 policy를 고치는 recovery 실험에 그대로 붙일 수 있음.

*대표 그림: 측정 결과 그림으로, diffusion policy 방법들의 MuJoCo 10개 과제 학습 곡선(4M step, seed 3개 평균, 음영은 표준편차)을 보여 줌. DoobPPO(파랑)는 HalfCheetah·Humanoid·Ant에서 상위권이지만 두 Inverted Pendulum 과제에서 중간에 return이 크게 내려가는 구간이 있고, DoobGRPO(빨강)는 HalfCheetah·Ant·Hopper에서 낮게 머무름.*

---

### 9. ALPS: Visual State Encoders for World Models (72점)

[arXiv](https://arxiv.org/abs/2610.30120) · [PDF](https://arxiv.org/pdf/2610.30120) · [alphaXiv](https://www.alphaxiv.org/abs/2610.30120) (요약 있음) · [프로젝트 페이지](https://ucsc-vlaa.github.io/ALPS/) · [코드](https://github.com/UCSC-VLAA/ALPS)

- **저자**: Yanqing Liu, Letian Zhang, Chengzhi Liu, Zijun Wang, Jieru Mei, Hongliang Fei, Yuyin Zhou, Cihang Xie
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 73점
- **읽은 원문**: PDF 전문

> world model과 robot policy가 공유할 frozen 시각 encoder ALPS를 정지 이미지와 텍스트만으로 학습함. 한 벌의 patch token이 물체 상태, 언어 정렬, 픽셀 복원을 함께 지원하고, LIBERO 물체 상태 probe의 상대 오차(Stage 1 = 1.000)는 ViT-B 중 가장 낮은 0.829로, 3.5배 큰 V-JEPA 2-L과 같음.

**무슨 문제인가**

많은 world model은 frozen 시각 encoder의 token 위에서 미래를 예측하고 계획함. 그래서 token에 물체 위치와 상태가 담겨 있어야 적은 상호작용 데이터로 dynamics를 배울 수 있음. 지시문을 장면과 연결하려면 언어 정렬이, 상상한 미래를 사람이 확인하려면 픽셀 복원이 필요함. 기존 encoder는 DINO 계열처럼 공간 정보, CLIP 계열처럼 언어 정렬, MAE처럼 복원 중 한두 가지에만 강하고, 이미지-텍스트 encoder의 상태 정보를 보강하면 언어 정렬 성능이 낮아지는 문제가 있음.

**어떻게 푸나**

ALPS(A Language-aligned, Pixel-renderable State encoder)는 ViT-B/16을 두 단계로 처음부터 학습함. 입력은 이미지 한 장이고 출력은 196개의 patch token이며, 언어 쪽은 token을 평균 pooling한 뒤 선형 투영해 함께 학습한 text encoder와 맞춤. Stage 1은 DataComp-1B 이미지-캡션 쌍으로 학습하며, 같은 patch token에 contrastive 정렬, 캡션 생성, 픽셀 복원, patch 대응(dense correspondence)을 함께 적용함. Stage 2는 Stage 1 encoder를 고정 teacher와 학습할 student로 복사함. student는 변형된 crop을 보고, predictor가 crop 위치와 상대 scale을 담은 geometry query를 받아 깨끗한 crop의 teacher token을 MSE로 맞힘. 손실은 student crop 안에 중심이 있는 teacher patch에만 걸고, 학습 뒤 predictor는 버리고 student를 Stage 1 text tower와 그대로 짝지음.

**결과**

- LIBERO-Object·LIBERO-Spatial(시뮬레이션 조작 시연 모음)에서 frozen token으로 물체 위치를 읽거나 1초·3초 뒤를 예측하는 probe의 상대 오차(Stage 1을 1.000으로 둠)가 0.829임. ViT-B 다음 순위는 C-RADIOv3 0.864, DINOv3 0.870이고, V-JEPA 2-L도 0.829이나 3초 예측은 ALPS가 0.813 대 0.904로 낮음.
- 같은 Stage 2 refinement를 세 encoder에 적용하면 state 오차는 모두 내려감. Flickr30k(이미지-캡션 검색 benchmark) 이미지→텍스트 Recall@1은 ALPS가 93.4%에서 93.2%로 유지됨. SigLIP 2는 7.5퍼센트포인트, CLIP은 10.9퍼센트포인트 내려감. SigLIP 2의 learning rate를 낮춰 state 개선 폭을 17%로 맞춰도 하락은 2.3퍼센트포인트로 ALPS의 0.2퍼센트포인트보다 큼.
- LIBERO 4개 suite에서 frozen token 위에 behavior cloning policy를 학습함. 각 encoder의 text tower로 지시문을 넣었을 때 평균 성공률이 ALPS 85.5%, SigLIP 2 84.8%, C-RADIOv3 81.8%임.
- DINO-WM 방식(frozen encoder token 위에서 미래를 예측해 행동을 계획하는 world model)으로 계획 성능을 잼. PushT 성공률 90%(C-RADIOv3와 같음), Wall 92%(DINOv2와 같음), Granular Chamfer 거리 0.176으로 가장 낮음. Rope은 C-RADIOv3(0.558 대 0.750), Reacher는 DINOv3(86.0% 대 78.7%)가 앞섬.

**한계**

모든 실험이 시뮬레이션이고 실로봇 검증이 없으며, backbone은 ViT-B/16 하나만 다룸. 상태·언어·픽셀 복원 세 가지를 한 계획기 안에서 함께 쓰는 실험은 없고, 각각 따로 측정함. 픽셀 복원 ℓ1 오차는 0.120으로 MAE·VC-1·OpenVision 3(0.104~0.109)보다 높고, refinement가 언어를 보존하는 이유(평균 pooling 구조)는 저자의 해석에 그침.

**누리랩 연구와의 연결**

- world model과 VLA의 시각 backbone을 고를 때 상태 probe, 언어 정렬, 복원을 함께 재는 평가 틀로 쓸 수 있음. 픽셀 복원이 되는 token은 world model rollout을 사람이 보고 failure를 진단하는 용도와 이어짐.
- 언어 정렬을 잃지 않고 공간 정보를 보강하는 Stage 2 방식은 VLA encoder를 manipulation 데이터에 맞출 때 language 성능 하락을 줄이는 비교 기준이 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림으로, 위쪽은 이미지-캡션 쌍에 네 목적함수(contrastive, captioning, reconstruction, correspondence)를 쓰는 Stage 1임. 아래쪽은 변형 crop을 본 student가 predictor와 geometry query로 고정 teacher의 깨끗한 crop token을 맞히는 Stage 2임.*

---

### 10. AtomicRL: Atomic Reinforcement Learning for Long-Horizon Robotic Manipulation (70점)

[arXiv](https://arxiv.org/abs/2610.30097) · [PDF](https://arxiv.org/pdf/2610.30097) · [alphaXiv](https://www.alphaxiv.org/abs/2610.30097) (요약 있음)

- **저자**: Likui Zhang, Zhe Zhu, Zhihao Zhan, Yibo Bai, Hanlin Wang, Dongwei Li, Bin Wang, Tianle Zhang 외 2명
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 74점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> VLA를 RL로 추가 학습할 때 뒤쪽 하위 과제의 실패 신호가 앞서 성공한 하위 과제의 학습 신호까지 낮추는 문제를, 하위 과제 경계에서 신호 전파를 줄이는 방식으로 막음. CALVIN ABC-D에서 하위 과제 5개를 모두 이어서 끝낸 비율이 PPO의 70.6%에서 80.1%로 오름.

**무슨 문제인가**

긴 조작 과제를 RL로 학습할 때 보통 마지막 성공 여부만 reward로 줌. 이때 PPO가 쓰는 GAE(generalized advantage estimation: 한 스텝 가치 오차인 TD residual을 시간 역순으로 누적해 advantage를 구하는 방식)는 끝부분 실패의 오차를 궤적 처음까지 거꾸로 전달함. 그래서 앞의 하위 과제 k개를 잘 해내고 k+1번째에서 실패한 궤적이면, 잘한 행동의 advantage도 같이 낮아짐. 중간 reward를 촘촘히 주는 기존 방법은 이 전파를 그대로 두고, 학습 후반 실패가 일부 하위 과제에 몰려도 과제를 고르게 뽑아 이미 익힌 하위 과제에 상호작용을 낭비함.

**어떻게 푸나**

AtomicRL은 SFT로 학습한 VLA를 PPO 기반으로 추가 학습하는 RL post-training 방법이고, 긴 지시를 차례가 정해진 하위 과제(atomic subtask)로 나눠 다룸. 먼저 PCC(Progress-Completion Critic)가 최근 L스텝의 관측·행동과 현재 하위 과제를 받아 진행도와 완료 여부를 내며, VLM과 사람이 단 demonstration 주석으로 오프라인 학습한 뒤 RL 중에는 고정함. SAPO(Semantic-Aware Policy Optimization)는 PCC가 찾은 하위 과제 경계에서 GAE 누적에 계수 κ를 곱해, 다음 하위 과제가 실패했으면 κ를 1보다 작게 해 앞쪽 성공 구간으로 넘어가는 실패 신호를 약하게 만듦(성공이면 κ=1). BATE(Bottleneck-Adaptive Target Exploration)는 하위 과제별 완료율 이동 평균이 낮은 하위 과제를 포함한 과제를 더 자주 뽑고, 그 구간에서 entropy 정규화를 키움. 실로봇용으로는 실제 demonstration 1개와 물체 다시점 사진으로 MuJoCo 시뮬레이션 환경을 자동 재구성하는 Real2Sim2Real pipeline을 만들고, 시뮬레이션에서 학습한 policy를 실로봇에 그대로 배치함.

**결과**

- LIBERO-LONG(시뮬레이션 장기 조작 과제 10개) 요소 분석에서 일부러 약한 SFT policy로 시작함. 성공/실패 0/1 reward만 쓸 때 성공률이 PPO 78.2%에서 SAPO 87.8%로 오름. 하위 과제 reward나 진행도 reward를 줘도 PPO는 80.2%와 81.8%, SAPO는 89.4%와 89.0%임. 여기에 진행도 reward 가중치를 학습 중 선형으로 줄이는 설정과 BATE를 더하면 91.2%가 됨.
- CALVIN ABC-D(환경 A, B, C에서 학습하고 처음 보는 환경 D에서 하위 과제 5개를 연달아 수행)에서 π0.5로 1,000회 평가함. 5개를 모두 끝낸 비율이 PPO 70.6%에서 80.1%로 오름. 평균 연속 완료 개수는 4.36에서 4.56으로 오름.
- LIBERO-LONG 본 실험에서 성공률이 base VLA가 π0.5일 때 PPO 95.4%에서 AtomicRL 99.0%로, OpenVLA-OFT일 때 94.8%에서 98.8%로 오름. PPO가 이미 높아 차이는 4퍼센트포인트 안팎임.
- AgiBot G1 실로봇의 탁상 과제 3개(하위 과제 4~6개)를 과제·방법마다 25회 평가함. 평균 성공률이 SFT 48.0%, PPO 61.3%, AtomicRL 69.3%임. 9개 조합의 시뮬레이션 성공률과 실로봇 성공률의 Pearson 상관계수는 0.909임.

**한계**

하위 과제를 나눠 쓴 STARE-VLA, IG-RFT 같은 방법과 직접 비교한 실험이 없고, baseline은 PPO뿐임. SAPO 기여를 보인 요소 분석은 약한 초기 policy를 쓴 LIBERO-LONG 한 설정에서만 했고, BATE의 과제 샘플링과 entropy 조절 효과는 따로 나누지 않음. PCC를 위해 과제마다 주석 달린 궤적이 필요하고(LIBERO 150개, 실로봇 과제당 50개), 실로봇 실험은 탁상 과제 3개이며 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- 하위 과제 경계와 성공·실패를 판정하는 PCC는 하위 과제 단위 failure detection 모듈로 볼 수 있음. 실패 판정을 탐지에서 끝내지 않고 RL의 credit 전파를 조절하는 데 쓴 사례로, failure detection을 VLA 학습에 연결하는 연구의 비교 대상임.
- skill chaining과 long-horizon 조작에서 앞 단계 성공을 보존하며 병목 단계에 탐색을 모으는 방식이라, 하위 과제 구조를 쓰는 VLA RL fine-tuning 실험의 baseline으로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 휴지와 장난감 차를 통에 넣는 과제를 하위 과제 4개로 나누고, 3개 성공 뒤 마지막 과제가 실패할 때 경계에서 κ로 신호 전달을 줄이는 SAPO와 PCC, 탐색 조절, 실제 장면을 병렬 시뮬레이션으로 옮기는 Real2Sim2Real 흐름을 함께 보여 줌.*

---

### 11. From VLM Planners to Robotic Agents: Self-Evolving Harnesses for History-Dependent Manipulation (70점)

[arXiv](https://arxiv.org/abs/2610.29560) · [PDF](https://arxiv.org/pdf/2610.29560) · [alphaXiv](https://www.alphaxiv.org/abs/2610.29560) (요약 있음)

- **저자**: Tingwen Du, Haoyu Guo, Hanxue Zhang, Xuanxu Wang, Junting Dong, Chao Gao, Mingfei Han, Tao Lu 외 4명
- **분야**: Embodied AI · robotics relevance 10/10 · 1차 스크리닝 72점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> VLM planner를 고정 VLA 위에 두고, 과제 진행 상황을 기록하는 편집 가능한 harness와 rollout 실패에서 그 harness를 스스로 고치는 절차를 붙임. RoboMME 16개 과제 평균 성공률이 self-evolution 없이 44.38%, 있을 때 51.38%임.

**무슨 문제인가**

버튼을 세 번 누르는 과제처럼, 같은 장면이라도 지금까지 몇 번 성공했는지에 따라 맞는 행동이 달라지는 경우가 있음. 현재 관측만 보는 VLA는 이런 과제를 풀 수 없고, 기억을 붙인 VLA나 VLM planner를 둔 계층 구조도 명령을 내린 뒤 실제로 성공했는지를 따로 확인하지 않음. 또 planner가 같은 실수를 반복할 때 이를 고치려면 보통 demonstration을 더 모아 VLM을 fine-tuning해야 함.

**어떻게 푸나**

SERA(Self-Evolving Robotic Agent)는 상위 VLM(gpt-5.6-sol)을 harness(입력 구성, 과제 상태 기록, 명령 검사, 실패 시 제어 규칙을 묶은 바깥 틀)로 감싸고, 하위 VLA는 고정한 채 실행만 맡김. 매 round마다 VLM은 지시문에서 뽑은 고정 guidance, 최근 front·wrist 영상, 텍스트 task context, 직전 명령, 실행 가능한 명령 후보를 받음. VLM은 직전 명령이 성공했는지 판단해 task context를 고쳐 쓰고 다음 하위 명령을 한 번에 냄. task context는 진행 단계, 완료한 일, 잡은 물체 등을 1,600자 이내로 요약한 것이라 영상이 창에서 빠진 뒤에도 과거 정보를 남김. 개발 단계에서는 분석 agent가 실패 rollout에서 처음 어긋난 지점을 찾고, 수정 agent가 planning guidance·판정 기준·제어 규칙 수정안을 냄. verifier가 같은 episode에서 기존 harness와 수정안을 다시 돌려 비교하고, 고른 harness는 test 전에 고정함.

**결과**

- RoboMME(과거 관측을 기억해야 풀리는 시뮬레이션 조작 과제 16개, 과제당 50 episode)에서 16개 과제 평균 성공률이 self-evolution 없는 harness의 44.38%에서 51.38%로 오름. 오름폭은 Counting suite(34%에서 49%)와 Imitation suite(18.5%에서 30%)에 몰려 있고, Reference suite는 69%에서 69.5%로 거의 같음.
- 공개 leaderboard 수치와 비교하면 평균 성공률이 MemER(VLM이 과거 keyframe을 골라 subtask를 내는 계층 구조) 42.38%, FrameSamp+Modul 44.51%보다 높음. FrameSamp+Modul은 과거 frame의 시각 feature로 action expert를 조절하는 방법임. Reference suite는 69.5%로 MemER 38.00%보다 높지만, Counting(49.00% 대 65.22%)과 Imitation(30.00% 대 51.39%)은 FrameSamp+Modul보다 낮음.
- 저자가 직접 재현한 MemER와 과제별로 비교하면 전체 성공 episode는 MemER 363/800, SERA 411/800임. MemER에서 SERA로 가며 VideoPlaceOrder는 18에서 46으로 오르지만 ButtonUnmask는 41에서 20, ButtonUnmaskSwap은 12에서 0으로 내림.
- PatternLock 개발용 6개 episode에서 초기 harness는 2개 성공함. 방향 해석을 고친 뒤 3개, 빠진 방향 명령을 추가해 후보를 5개에서 8개로 늘린 뒤 5개 성공함. 이 값은 test 전 개발 단계 결과임.

**한계**

실험은 RoboMME 시뮬레이션뿐이고 실로봇 실험은 없으며, 본문에 코드 공개 주소가 없음. leaderboard baseline과의 비교는 같은 조건에서 돌린 대조 실험이 아니고, 어떤 수정이 오름폭을 만들었는지 가르는 ablation도 없음. 상위 planner가 비공개 대형 VLM이고 매 round 호출하므로 지연이 클 수 있지만, 본문은 이 지연을 재지 않았음.

**누리랩 연구와의 연결**

- 실행 직후 영상으로 명령 성공 여부를 판정하고 task context를 고치는 구조라, VLA 위에서 failure detection과 recovery를 돌리는 설계의 비교 대상이 됨.
- 가중치 대신 planner의 prompt·판정 기준·제어 규칙을 rollout 실패로 고치는 방식은 language feedback 기반 learning과 텍스트 형태 robot memory 연구에 바로 이어짐.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림으로, 위쪽은 버튼을 세 번 누를 때 같은 장면이라도 1/3 완료면 누르고 3/3 완료면 멈춰야 함을 보임. 아래쪽은 왼쪽부터 기억 붙인 VLA, VLM planner 계층 구조, SERA(context를 고치는 harness와, rollout 결과로 harness 수정안을 골라 반복하는 절차) 순서로 그림.*

---

### 12. Think-Capture: Active 3D Geometry Acquisition for Spatial Reasoning in Vision-Language Models (70점)

[arXiv](https://arxiv.org/abs/2610.29232) · [PDF](https://arxiv.org/pdf/2610.29232) · [alphaXiv](https://www.alphaxiv.org/abs/2610.29232) (요약 있음) · [코드](https://github.com/819346675/Think-Capture)

- **저자**: Junjie Wang, Zhihao Yuan, Yunhan Tang, Sheng Xu, Jiaqi Mao, Xiaoyu Ye, Yueru Luo, Xu Yan 외 2명
- **분야**: Embodied AI · robotics relevance 7/10 · 1차 스크리닝 74점
- **학회**: WACV 2027 채택 · 근거: comments에 "Accepted at WACV 2027"
- **읽은 원문**: PDF 전문

> VLM이 질문에 필요한 물체만 골라 그 3D 위치와 카메라 자세를 도구로 재고, 그 결과를 짧은 텍스트로 받아 답하게 함. 4B 모델의 MindCube-Tiny 정확도가 32.9%에서 54.4%로 오름.

**무슨 문제인가**

VLM은 2D 인식은 잘하지만 여러 시점의 사진 사이에서 물체의 3D 관계를 일관되게 유지하지 못함. 가려짐이나 시점 변화가 있으면 사진 속 배경을 관찰자 뒤쪽으로 착각하는 식으로 틀림. 기존 방법은 장면 전체의 dense geometry를 모든 질문에 미리 섞어 넣으므로 계산과 context가 늘어남. 3D 도구를 부르는 agent 방식도 도구 출력이 틀리면 그 오류가 답으로 그대로 이어짐.

**어떻게 푸나**

Think-Capture는 두 단계로 답함. Stage 1에서 VLM은 질문과 사진 최대 4장을 보고 3D 측정이 필요한 물체 이름만 출력함. 도구 묶음은 SAM3로 그 물체의 mask를 따고, Pi3X(여러 사진에서 point map과 카메라 자세를 추정하는 3D 복원 모델)로 사진마다 point map과 카메라 자세를 추정해 첫 사진 기준 좌표계로 옮김. Symbolic 3D State Abstraction(정해진 문장 틀)이 이를 물체의 위치·크기·쌍별 방향과 거리, 카메라의 위치와 회전을 적은 평균 100 token 텍스트로 바꿈. Stage 2에서 VLM은 원래 사진과 이 텍스트를 함께 보고 답함. Qwen3-VL-4B를 GRPO(정답 보상을 표본 묶음 안에서 정규화하는 RL)로 학습하며, 도구가 오답을 바로잡은 학습 표본 1,927개에는 정답 보상 1, 도구 때문에 오답이 된 표본 1,105개에는 정답 보상 2를 줌.

**결과**

- MindCube-Tiny(여러 시점 사진을 보고 회전·주변 배치·관점 전환을 묻는 문제 1,050개)에서 정확도가 Qwen3-VL-4B의 32.9%에서 54.4%로 오름. 같은 크기의 3D 도구 사용 방법 Think3D-4B는 38.2%임.
- 같은 물체 선택과 mask를 쓰고 Stage 2 입력만 2D box로 바꾸면 MindCube 36.9%, 전체 MMSI-Bench(서로 다른 사진에 나온 물체 사이 관계를 묻는 benchmark) 31.8%임. 3D 텍스트는 각각 54.4%, 38.9%임.
- Pi3X 좌표에 0.4m Gaussian noise를 넣으면 MindCube-Tiny 정확도가 학습 없이 도구만 쓴 경우 26.7%, 보상 차등 없이 학습한 경우 40.3%, 전체 방법 46.2%임.
- 학습에 쓰지 않은 ViewSpatial-Bench(자기 시점과 타인 시점 전환 문제)에서 37.6%에서 42.8%로 오름. 실로봇은 Agibot G1에서 약 상자를 집는 시연만 보였고 성공률 수치는 본문에서 확인 불가임.

**한계**

물체가 모든 시점에서 가려지거나 깊이·자세 추정이 한쪽으로 치우치면 텍스트 관계 자체가 틀리며, 학습으로도 이를 복구하지 못함. 학습 데이터는 MindCube 한 곳에서만 뽑았고, 방향을 몇 개 언어 구간으로 나누므로 세밀한 조작에 필요한 접촉·형상 정보는 담지 않음. 한 번 추론에 21.8초가 걸려 로봇에서는 시작 시점에 waypoint 하나를 주는 용도로만 썼음.

**누리랩 연구와의 연결**

- 질문에 따라 필요한 물체만 골라 3D를 재는 구조는 active perception과 object-centric 표현을 VLA 상위 planner에 붙이는 방식의 사례임. 측정 대상 선택을 다음 시점 선택(NBV)으로 넓히는 비교 실험에 쓸 수 있음.
- 도구가 답을 망친 표본에 더 큰 보상을 주는 학습은, 부정확한 world model이나 perception 출력을 언제 믿을지 판단하는 failure detection 연구에 그대로 가져올 수 있음.

*대표 그림: 측정 결과가 아니라 두 방식을 비교한 개념도임. 왼쪽은 질문과 무관하게 2D·3D token을 섞어 거울이 뒤에 있다고 틀리는 기존 방식이고, 오른쪽은 Stage 1에서 거울과 사진 2의 위치를 요청한 뒤 3D 정보를 받아 앞 왼쪽이라고 맞히는 Think-Capture임.*

---

### 13. SimPT: An Automated Simulation Framework for Intervention-Based VLA Post-Training (68점)

[arXiv](https://arxiv.org/abs/2610.29161) · [PDF](https://arxiv.org/pdf/2610.29161) · [alphaXiv](https://www.alphaxiv.org/abs/2610.29161) (요약 있음)

- **저자**: Caicheng Wang, Zipeng Ye, Zhexuan Zhou, Zilong Huang, Xi Zhang, Yuchen Xie
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> VLA post-training에서 사람이 하던 개입(실패한 실행을 넘겨받아 고치는 일)을 시뮬레이션에서 자동으로 하는 프레임워크 SimPT를 만듦. 과제 단계를 추적하는 그래프로 복구 시도 횟수를 75.0% 줄였고, 이 틀에서 다듬은 RECAP 변형은 실로봇 랜선 꽂기 성공률을 72%에서 96%로 올림.

**무슨 문제인가**

사람이 개입해 고친 데이터로 VLA를 post-training하는 HIL(human-in-the-loop) 방식은 알고리즘 하나를 시험할 때마다 사람의 교정과 실로봇 평가를 반복해야 함. 실제 환경은 매번 조금씩 달라서 방법끼리 같은 조건으로 비교하기도 어려움. 시뮬레이션에서 교정 데이터를 자동으로 만들려면 실패한 rollout의 어느 상태로 돌아가 전문가가 이어받을지 정해야 함. 기존 IntervenGen은 이 결정을 사람에게 맡겼고, VLM으로 진행 상황을 감시하면 질의마다 추론 비용이 듦.

**어떻게 푸나**

SimPT는 policy rollout, 교정 데이터 수집, policy 학습, 단독 평가를 시뮬레이터 안에서 자동으로 이어 돌림. 핵심 도구인 Progress Graph는 과제를 접근, 파지, 들기 같은 단계로 나누고, 시뮬레이터만 아는 상태(물체 pose, gripper 상태, 접촉)로 단계 완료와 후퇴를 판정하는 그래프임. Codex agent(GPT-5.6-Sol 기반)가 RoboTwin 과제 코드를 읽고 이 그래프를 만들며, 판정 임계값은 시뮬레이션 전문가 궤적으로 보정함. VLA 실행 중에는 agent를 다시 부르지 않고 그래프 검사만으로 단계마다 가장 최근 snapshot을 남김. rollout이 실패하면 cuRobo(GPU 병렬 motion planner) 기반 전문가가 가장 많이 진행된 단계의 snapshot부터 복원해 과제를 끝내 보고, 실패하면 그 이전 단계로 물러남. 모은 궤적은 RECAP(value function으로 구한 advantage를 policy 조건으로 줌), HG-DAgger(교정 구간으로 재학습), DPO+SFT, FlowPRO(flow VLA용 DPO 변형)가 나눠 씀.

**결과**

- RoboTwin(양팔 로봇 시뮬레이션 조작 benchmark) 7개 과제에서 snapshot을 50 step마다 저장하는 고정 간격 baseline과 Progress Graph 방식을 비교함. 전체 복구 시도 횟수가 3,781회에서 945회로 75.0% 줄고, 복구 성공률은 93.4%에서 98.9%로 오름.
- 수집 방식이 학습에 주는 영향을 π0.5 기반 policy로 잼(과제당 held-out 200 seed). RECAP의 7개 과제 평균 성공률은 고정 간격 데이터 66.64%에서 Progress Graph 데이터 76.50%로 오름. HG-DAgger는 1.93퍼센트포인트 올랐지만 FlowPRO는 76.07%에서 71.86%로 내려감. Progress Graph 데이터에서는 HG-DAgger가 82.14%로 가장 높았고, SFT만 한 policy는 67.29%임.
- RECAP-CF-LPF는 RECAP의 value 예측을 5-fold cross-fitting(다른 fold로 학습한 모델로 예측)과 1 Hz Butterworth low-pass filter로 다듬은 변형임. held-out 1,400회 평균 성공률이 RECAP의 76.50%에서 79.36%로 오름. 향상폭의 95% 신뢰구간은 0.36~5.36퍼센트포인트이고, 7개 중 2개 과제는 내려감.
- 실로봇은 AgileX PiPER 양팔로 랜선을 집어 다른 팔에 넘기고 컴퓨터 포트에 꽂는 과제임. 사람 개입을 포함한 같은 1,672개 궤적으로 학습했을 때 25개 장면 성공률이 RECAP 72%(18/25)에서 RECAP-CF-LPF 96%(24/25)로 오름.

**한계**

실로봇에서는 SimPT의 자동 수집을 쓰지 않았고, 시뮬레이션에서 고른 RECAP 수정만 사람이 모은 데이터에 적용함. Progress Graph는 시뮬레이터 특권 상태와 cuRobo 전문가에 기대므로 실제 환경 데이터 수집에는 바로 쓸 수 없음. 실로봇 검증은 과제 1개 25개 장면뿐이고, cross-fitting과 low-pass filter 각각의 성공률 기여는 따로 보이지 않았으며 코드 주소도 본문에 없음.

**누리랩 연구와의 연결**

- 실패 rollout에서 어느 단계의 snapshot으로 돌아가 복구할지 고르는 Progress Graph는 failure detection·recovery 연구에서 시뮬레이션 교정 데이터를 자동으로 만드는 도구로 쓸 수 있음.
- 같은 seed와 데이터로 VLA post-training 방법 4개를 비교한 결과(HG-DAgger가 가장 높고, 수집 방식에 따라 FlowPRO 성능이 내려감)는 VLA RL fine-tuning 실험의 baseline을 고를 때 근거가 됨.

*대표 그림: 측정 결과가 아니라 SimPT의 전체 흐름을 그린 개념도로, Progress Graph 생성과 보정(A), 실패 시 snapshot 복원과 cuRobo 복구로 만드는 데이터 수집(B), 알고리즘 개발 반복(C, 곡선은 개략도)을 차례로 보임. D칸에는 RECAP 대비 RECAP-CF-LPF의 성공률(시뮬레이션 76.50%에서 79.36%, 실로봇 72%에서 96%)을 적음.*

---

### 14. How Representational Priors Shape Generalization in World Action Models (68점)

[arXiv](https://arxiv.org/abs/2610.29168) · [PDF](https://arxiv.org/pdf/2610.29168) · [alphaXiv](https://www.alphaxiv.org/abs/2610.29168) (요약 있음)

- **저자**: Junha Chun, Youngjoon Jeong, Taesup Kim
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 74점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> world action model의 backbone이 policy 학습 전부터 겉모습 변화를 깨끗한 장면들의 feature 공간 바깥으로 보내는지를 재는 지표(nuisance orthogonality)를 만듦. backbone 9개에서 이 값과 LIBERO-Plus 4개 시각 변화 평균 성공률의 결정계수 R²가 0.835임.

**무슨 문제인가**

WAM(world action model)은 영상·이미지 생성 모델을 backbone으로 삼아 미래 장면 예측과 행동 생성을 함께 학습하는 robot policy임. 같은 학습 설정이라도 어떤 생성 backbone을 쓰느냐에 따라 조명·배경·카메라가 바뀐 장면에서의 성공률이 크게 달라짐. 기존 연구는 이미지 편집 모델이 영상 예측 모델보다 낫다고 보고했지만, 무엇이 차이를 만드는지는 설명하지 못함. policy 학습 한 번에 GPU 수십 시간이 들기 때문에, 학습 전에 backbone의 쓸모를 미리 가늠할 방법이 필요함.

**어떻게 푸나**

먼저 LIBERO-Plus에서 시뮬레이터 상태는 같고 겉모습만 다른 관측 쌍을 모아 진단용 데이터를 만듦. 깨끗한 관측 40장을 backbone에 넣어 층별 중간 feature를 얻고, SVD로 이 feature들이 차지하는 부분공간(in-distribution 부분공간)을 구함. 이어서 겉모습을 바꾼 관측 1,200장의 feature가 원래 feature에서 얼마나 옮겨 갔는지 변위 벡터를 계산함. nuisance orthogonality는 이 변위 중 부분공간 바깥으로 향하는 비율을 층과 샘플에 대해 평균한 값임. 값이 높으면 행동과 무관한 변화가 깨끗한 장면끼리 구분하는 방향과 섞이지 않는다는 뜻임. policy 학습 뒤에는 nuisance suppression을 잼: 깨끗한 feature의 분산으로 정규화한 변위가 학습 전 world model 대비 얼마나 줄었는지를 부분공간 안쪽과 바깥쪽으로 나눠 비율로 나타냄.

**결과**

- LIBERO-Plus(LIBERO 조작 과제에 조명·배경·센서 노이즈·카메라 시점 변화를 넣은 robustness 평가 모음)의 4개 변화 평균에서, FLUX.2 backbone은 orthogonality 0.799에 성공률 89.0%임. Wan2.2 backbone은 0.594에 46.5%임. backbone 9개, 평가 궤적 총 5,418개 기준임.
- 같은 구조를 무작위 초기화한 FLUX.2는 orthogonality 0.724, 성공률 63.9%로 두 모델 사이에 놓임. 영상 모델 MAGI-1(0.750, 76.2%)과 SANA-Video(0.742, 75.4%)도 높은 값을 보임. 저자는 이를 근거로 사전학습 목표가 이미지 편집인지 영상 생성인지보다 표현 기하가 더 관련 있다고 주장함.
- FLUX.2를 backbone으로 쓴 ImageWAM을 학습하면 깨끗한 feature의 총분산이 13.4배 커지는 동안 변위의 부분공간 안쪽 성분은 2.73배, 바깥쪽 성분은 2.48배만 커져 상대적으로 억제됨. Wan2.2를 backbone으로 쓴 FastWAM을 학습하면 총분산은 4.42배, 안쪽·바깥쪽 변위 성분은 5.63배와 3.18배로 억제가 약함. FastWAM의 카메라 변화 성공률은 16.4%임.

**한계**

모든 실험이 LIBERO 시뮬레이션 조작과 LIBERO-Plus의 시각 변화에 한정되고, 실로봇 실험과 언어·과제 조합 일반화는 다루지 않음. 결과는 모델 간 상관관계이며, 저자도 orthogonality가 robustness의 원인임을 따로 떼어 보이지 않았다고 밝힘. Kiwi-Edit(0.786, 77.1%)처럼 추세에서 벗어난 점이 있고, suppression 분석은 두 쌍의 단일 층에서만 보였으며 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- world model이나 VLA backbone을 고를 때 policy 학습 전에 깨끗한 장면 40장과 변형 장면만으로 robustness를 가늠하는 진단 도구로 쓸 수 있음.
- 같은 변위 분해를 실패 장면에 적용하면, 실패가 겉모습 변화에서 왔는지 장면 자체의 차이에서 왔는지 가르는 failure diagnosis 지표로 확장할 여지가 있음.

*대표 그림: 네 열은 원본 LIBERO 장면, FLUX.2 편집 결과, OmniGen2 편집 결과, LIBERO-Plus의 실제 변형 장면이고, 세 행은 배경·조명·센서 blur 변화임. 이미지 편집 backbone이 이런 시각 변화를 zero-shot으로 이미 만들 수 있다는 동기를 보이는 예시이며, policy 성능 측정 결과는 아님.*

---

### 15. AOV-GS: Active Open-Vocabulary Semantic Mapping with 3D Gaussian Splatting (62점)

[arXiv](https://arxiv.org/abs/2610.29374) · [PDF](https://arxiv.org/pdf/2610.29374) · [alphaXiv](https://www.alphaxiv.org/abs/2610.29374) · [코드](https://github.com/OptimusFaber/AOV-GS)

- **저자**: Rodion Shkokov, Tatiana Zemskova, Dmitry Yudin
- **분야**: 3D Vision · robotics relevance 9/10 · 1차 스크리닝 78점
- **학회**: CoRL 양식 (추정) · 근거: 1단 구성, 초록 아래 'Keywords:' 줄
- **읽은 원문**: PDF 전문

> 로봇이 처음 보는 실내를 탐색하며 3DGS 지도를 만들 때, 다음 시점을 고르는 기준에 SAM·CLIP으로 잰 의미적 새로움을 더함. Replica 8개 장면에서 텍스트 질의 분할 평균 mIoU가 기하만 보는 탐색의 33.3%에서 34.6%로 오름.

**무슨 문제인가**

ActiveGS 같은 기존 active mapping은 아직 안 본 영역을 많이 덮는 시점만 고름. 그래서 지도에 어떤 물체 정보가 담길지는 지나간 경로에 따라 우연히 정해짐. 의미 정보로 탐색을 이끄는 ActiveSGM은 장면마다 OneFormer 분할기를 정해진 label 집합으로 fine-tuning해야 함. 이 경우 label 집합 밖의 단어로 지도를 질의하는 open-vocabulary 사용이 막힘.

**어떻게 푸나**

AOV-GS(Active Open-Vocabulary Gaussian Splatting)는 SplaTAM(RGB-D SLAM 방법)으로 3DGS 지도를 만들고 ActiveGS의 planner로 다음 시점(NBV, next-best-view)을 고름. 탐색 초반(stage 0)에는 후보 시점마다 아직 안 본 픽셀 수와 이동 거리로 기하 점수를 매겨 상위 8개를 남기고, 남은 후보마다 현재 지도에서 RGB 영상을 렌더링하고, SAM으로 물체 mask를 따고 CLIP으로 mask마다 512차원 embedding을 뽑음. 이 embedding이 지금까지 지나온 keyframe의 embedding bank와 얼마나 다른지를 cosine 유사도로 재어 의미적 새로움 점수로 씀. 최종 점수는 기하 점수와 새로움 점수의 곱이고, 후반(stage 1 이후)에는 기하 점수만 씀. 탐색이 끝나면 keyframe의 CLIP embedding으로 LangSplatV2(Gaussian마다 언어 feature를 붙이는 방법) language field를 학습하며, 이 field는 텍스트 질의를 받아 새 시점 분할 mask를 냄.

**결과**

- Replica(실내 장면 사진 수준 재현 데이터, 8개 장면)에서 같은 SAM·CLIP 파이프라인을 쓴 기하 전용 탐색 대비 평균 mIoU가 33.3%에서 34.6%로 오름. 장면별로는 office0에서 7.1퍼센트포인트 오르고 4개 장면에서는 내림. 8개 장면을 seed 5개로 반복한 평균 PSNR은 기하 전용 31.62dB, AOV-GS 31.53dB로 비슷함.
- office0을 seed 5개로 반복하면 mIoU가 기하 전용 28.8±1.4%, AOV-GS 33.6±1.1%임.
- Matterport3D(더 넓은 실내 장면 데이터, 5개 장면)에서는 평균 mIoU가 21.3%에서 23.1%로 오름. 두 방법 모두 CorrCLIP 방식 후처리(mask 병합과 클래스 간 억제)를 쓰면 21.8% 대 24.0%임.
- ActiveSGM이 OneFormer용으로 고른 경로를 그대로 재생해 같은 language field를 학습하면 Replica 평균 mIoU가 28.2%에 그침. 저자는 탐색 기준이 지도의 의미 표현과 맞아야 한다는 근거로 이 결과를 듦.

**한계**

모든 실험이 Habitat 시뮬레이터에서 정답 카메라 pose를 받아 진행되었고 실로봇이나 SLAM 오차 조건은 없음. 평균 향상폭이 1~2퍼센트포인트이고 Replica 8개 중 4개 장면에서는 오히려 내리며, seed 반복은 office0 한 장면의 mIoU만 보고함. 후보 하나를 의미 점수로 매기는 데 약 8초가 걸려 office0 한 번 탐색에 약 61분이 듦.

**누리랩 연구와의 연결**

- active perception/NBV와 open-vocabulary semantic mapping을 3DGS 위에서 묶은 사례임. 기하 점수 위에 foundation model 점수를 곱해 시점을 다시 고르는 구조는 과제 조건이 붙은 NBV 연구의 비교 대상으로 쓸 수 있음.
- OneFormer용 경로가 CLIP language field에는 도움이 안 된다는 결과는, object-centric 3DGS 지도를 만들 때 탐색 기준을 하위 표현에 맞춰 설계해야 한다는 근거가 됨.

*대표 그림: 측정 결과가 아니라 시스템 구조를 그린 그림으로, 위쪽 online 단계에서는 Habitat RGB-D, SplaTAM 지도, planner, SAM·CLIP embedding bank, RRT 이동이 반복됨. 아래쪽 offline 단계에서는 language field를 학습하고 "chair" 같은 텍스트로 새 시점 분할을 질의함.*

---

## 오늘의 흐름

- **VLA 실행 중 기억을 따로 두기**: 지나간 관측을 VLA 안에 그대로 쌓지 않고, 3D 기하 token이나 문장 목록처럼 꺼내 쓰기 쉬운 형태로 바꿔 저장하는 논문이 셋 나옴. 셋 모두 기억 장치를 뺀 비교 조건보다 평균 성공률이 오름. [GeoMem-VLA](https://arxiv.org/abs/2610.29866), [Plan First, Act Later](https://arxiv.org/abs/2610.29329), [Self-Evolving Harnesses](https://arxiv.org/abs/2610.29560)
- **실패와 사람 개입을 post-training에 쓰기**: 배포나 시뮬레이션에서 나온 실패를 VLA post-training에 쓰는 방법이 여럿 나옴. 사람 개입 데이터를 그대로 쓰는 쪽, 시뮬레이터가 개입을 대신하는 쪽, 하위 과제 경계에서 실패 신호의 전파를 줄이는 쪽으로 나뉨. [Training in Deployment](https://arxiv.org/abs/2610.29264), [SimPT](https://arxiv.org/abs/2610.29161), [AtomicRL](https://arxiv.org/abs/2610.30097)
- **world model의 접촉 예측과 시각 표현 평가**: world action model(영상과 action을 함께 예측하는 world model)이 접촉력까지 예측하게 한 연구가 나옴. 시각 encoder가 일반화에 유리한지 policy 학습 전에 재는 연구와, world model과 policy가 함께 쓸 encoder를 따로 학습하는 연구도 나옴. [CW-WAM](https://arxiv.org/abs/2610.30117), [Representational Priors](https://arxiv.org/abs/2610.29168), [ALPS](https://arxiv.org/abs/2610.30120)
- **느린 시각 판단과 빠른 센서 보정 나누기**: 느린 시각 모델 추론 사이를 촉각이나 힘 feedback으로 메우는 구조가 두 편 나옴. T-WLA는 action chunk를 촉각으로 실행 도중에 고쳐 실제 dexterous hand 과제 4개 평균 성공률을 23.0%에서 51.0%로 올림. [T-WLA](https://arxiv.org/abs/2610.28814), [CW-WAM](https://arxiv.org/abs/2610.30117)
- **사람 영상과 3D 측정으로 공간 정보 보강**: RGB 사람 영상에서 3D 형상을 복원해 policy를 사전학습하거나 시뮬레이션 demonstration을 늘리는 방식이 나옴. VLM이나 탐색 로봇이 필요한 물체와 시점만 골라 3D를 재는 방식도 나옴. [SpatialDex](https://arxiv.org/abs/2610.29716), [Real2Sem2Real](https://arxiv.org/abs/2610.28880), [Think-Capture](https://arxiv.org/abs/2610.29232), [AOV-GS](https://arxiv.org/abs/2610.29374)

## 해볼 만한 연구

### 예측 접촉력과 측정 접촉력의 차이로 실패 감지하기
- 질문: world action model이 예측한 wrench(힘과 토크를 묶은 값)와 실제로 잰 wrench의 차이가 끼임·미끄러짐 같은 접촉 실패를 시각 신호보다 먼저 알려 주는지 밝힘.
- 첫 실험: peg 끼우기와 서랍 열기에서 wrench 예측 오차 기반 감지기와 VLM 영상 판정 기반 감지기의 감지 시점과 정확도를 비교함.
- 가장 가까운 연구: [CW-WAM](https://arxiv.org/abs/2610.30117)은 예측 wrench를 action 생성과 힘 제어에만 쓰고, 실패 감지 신호로는 평가하지 않음.

### 자동 실패 감지기로 사람 개입 대체하기
- 질문: 배포 중 online post-training에서 사람 개입을 자동 실패 감지와 자동 복구 동작으로 바꿔도 성능 향상이 유지되는지 밝힘.
- 첫 실험: 같은 양팔 과제에서 세 조건을 같은 학습 횟수로 비교함: 사람 VR 개입, 과제 단계를 추적하는 그래프로 실패를 판정한 뒤 자동 복구, 개입 없음.
- 가장 가까운 연구: [Training in Deployment](https://arxiv.org/abs/2610.29264)는 사람 개입에 기댐. [SimPT](https://arxiv.org/abs/2610.29161)는 시뮬레이터만 아는 물체 pose·접촉 상태가 있어야 단계를 판정함.

### 문장 memory와 3D token memory 비교
- 질문: 기억이 필요한 조작 과제에서 사건을 문장으로 적는 memory와 3D 기하를 token으로 저장하는 memory가 각각 어떤 과제에서 유리한지 밝힘.
- 첫 실험: RoboMME(기억이 필요한 조작 과제 모음)에서 같은 VLA에 문장 memory, 3D token memory, 둘을 함께 쓰는 경우를 붙여 과제 유형별 성공률을 비교함.
- 가장 가까운 연구: [Plan First, Act Later](https://arxiv.org/abs/2610.29329)와 [Self-Evolving Harnesses](https://arxiv.org/abs/2610.29560)는 텍스트 기록만, [GeoMem-VLA](https://arxiv.org/abs/2610.29866)는 3D token memory만 다룸.

## 꼭 읽을 논문

- [SpatialDex](https://arxiv.org/abs/2610.29716): RGB 사람 영상에서 3D 형상을 복원해 양손 policy를 사전학습함. 실로봇 양손 과제 6개 성공률이 π0.5의 43.3%에서 81.7%로 오름.
- [T-WLA](https://arxiv.org/abs/2610.28814): 시각 action chunk를 촉각으로 실행 도중 고치는 구조로, 실행 중 보정 설계의 비교 대상이 됨.
- [Plan First, Act Later](https://arxiv.org/abs/2610.29329): 할 일을 미리 목록에 적어 두는 robot memory 구조로, 기억이 필요한 조작 과제 성공률을 올림.
- [CW-WAM](https://arxiv.org/abs/2610.30117): world model이 접촉력까지 예측하게 한 사례로, 예측 접촉력을 실패 감지 신호로 시험해 볼 출발점이 됨.
- [SimPT](https://arxiv.org/abs/2610.29161): VLA post-training의 개입과 복구를 시뮬레이션에서 자동화하고, post-training 방법 4개를 같은 조건에서 비교함.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (470편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2610.29866'>GeoMem-VLA: Internalizing 3D Scene Understanding into Temporal Memory for Vision-Language-Action Models</a></td><td>88</td><td>10</td><td>VLA</td><td>VLA에 3D 기하를 temporal memory로 내재화하는 접근, 조작과 robot memory에 직결됨</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2610.28814'>T-WLA: Bridging Slow Vision and Fast Touch with a World-Language-Action Model</a></td><td>78</td><td>10</td><td>VLA</td><td>촉각과 world-language-action을 결합해 contact-rich 조작의 지연 문제를 다룸</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2610.29374'>AOV-GS: Active Open-Vocabulary Semantic Mapping with 3D Gaussian Splatting</a></td><td>78</td><td>9</td><td>3D Vision</td><td>로봇용 active open-vocabulary semantic mapping을 3DGS로 수행, NBV와 semantic map에 해당함</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2610.29716'>Reconstruction-Augmented Visuomotor Pre-Training of 3D-Grounded Bimanual Dexterity from RGB-Only Human Videos</a></td><td>76</td><td>10</td><td>Manipulation</td><td>RGB 인간 영상에서 3D 재구성으로 양손 dexterity를 사전학습함</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2610.29329'>Plan First, Act Later: Streaming Reasoning for Executable Memory in Robot Control</a></td><td>74</td><td>10</td><td>Robot Memory</td><td>계획 먼저 하는 streaming reasoning으로 실행 가능한 memory를 구성함</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2610.30097'>AtomicRL: Atomic Reinforcement Learning for Long-Horizon Robotic Manipulation</a></td><td>74</td><td>10</td><td>VLA</td><td>원자 단위 RL로 장기 조작 VLA를 IL 한계 너머로 학습시킴</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2610.30117'>CW-WAM: A Structured Contact-Wrench World Action Model for Force-Sensitive Manipulation</a></td><td>74</td><td>10</td><td>World Model</td><td>contact-wrench 구조 world action model로 힘 민감 조작을 다룸</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2610.29168'>How Representational Priors Shape Generalization in World Action Models</a></td><td>74</td><td>9</td><td>World Model</td><td>world action model의 표현 기하가 일반화에 미치는 영향을 분석함</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2610.28990'>Doob-Based Generative Policy Optimization</a></td><td>74</td><td>8</td><td>RL</td><td>Doob h-transform으로 diffusion/flow policy를 likelihood 없이 PPO/GRPO 최적화, 로봇 policy RL에 직접 연결됨</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2610.29232'>Think-Capture: Active 3D Geometry Acquisition for Spatial Reasoning in Vision-Language Models</a></td><td>74</td><td>7</td><td>Embodied AI</td><td>VLM이 능동적으로 3D 기하를 획득해 spatial reasoning을 하는 active perception 접근임</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2610.30120'>ALPS: Visual State Encoders for World Models</a></td><td>73</td><td>8</td><td>World Model</td><td>world model용 visual state encoder 설계, 물리 상태·언어 정렬·복원을 통합한 representation임</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2610.29161'>SimPT: An Automated Simulation Framework for Intervention-Based VLA Post-Training</a></td><td>72</td><td>10</td><td>VLA</td><td>VLA의 intervention 기반 post-training을 시뮬레이션으로 자동화하는 프레임워크임</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2610.29264'>Training in Deployment: Human-in-the-loop Online Post-Training for Robot Manipulation</a></td><td>72</td><td>10</td><td>VLA</td><td>배포 중 human-in-the-loop 온라인 post-training으로 recovery 상태를 보완함</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2610.29560'>From VLM Planners to Robotic Agents: Self-Evolving Harnesses for History-Dependent Manipulation</a></td><td>72</td><td>10</td><td>VLA</td><td>VLM planner에서 자기 진화 harness로 history 의존 조작을 다룸</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2610.28880'>Real2Sem2Real: 3D Semantic Augmentations for Robot Learning from a Single Human RGB Demonstration</a></td><td>72</td><td>9</td><td>Manipulation</td><td>단일 RGB 인간 영상에서 3D 시맨틱 증강으로 로봇 데이터를 대량 생성함</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2610.29702'>CausGround: Causal Interaction Grounding for Adaptive Embodied Planning</a></td><td>72</td><td>9</td><td>Embodied AI</td><td>인과 상호작용 grounding으로 precondition과 effect를 학습하는 계획임</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2610.30061'>Test-Time Motion Steering for Perceptive Humanoid Fall Recovery</a></td><td>72</td><td>8</td><td>Humanoid</td><td>test-time motion steering으로 지각 기반 넘어짐 복구를 수행함</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2610.30089'>ProactEgoMem: Benchmarking Proactive Memory in Streaming Egocentric Video</a></td><td>72</td><td>7</td><td>Embodied AI</td><td>streaming egocentric video의 proactive memory benchmark, robot memory와 연결됨</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2610.30129'>Rethinking Video Autoencoders for Interactive World Models</a></td><td>72</td><td>7</td><td>World Model</td><td>interactive world model용 video autoencoder 재설계, 시뮬레이터/planning 기반 연구임</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2610.28882'>inr2action: Encoding Robot Episodes as Neural Implicit Representations for Recall and Action</a></td><td>70</td><td>9</td><td>Robot Memory</td><td>에피소드를 neural implicit 표현으로 저장하는 parameter-space memory가 참신함</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2610.29282'>Relational Geometry Forcing for World Action Models</a></td><td>70</td><td>9</td><td>World Model</td><td>world action model에 관계적 3D 기하 제약을 넣어 조작 정밀도를 높임</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2610.29730'>Post-hoc Epistemic Uncertainty for Vision-Language-Action Policies</a></td><td>70</td><td>9</td><td>VLA</td><td>VLA 정책의 post-hoc epistemic uncertainty로 failure 감지에 직결됨</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2610.29768'>UniRAP: Towards Unified Part-level Physical Affordance Reasoning and Actionable Perception</a></td><td>70</td><td>8</td><td>Manipulation</td><td>part-level affordance reasoning과 actionable perception 통합, 조작 grounding에 관련됨</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2610.30125'>PhysiCalWorld: In-Context Physics Calibration for World Models</a></td><td>70</td><td>8</td><td>World Model</td><td>in-context 물리 보정으로 world model이 물성을 추론하게 함</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2610.28779'>Second Thoughts: Exploring and Planning through Comparative Imagination in World Models</a></td><td>70</td><td>7</td><td>World Model</td><td>world model 상상 rollout 비교로 탐색과 plan 대체 시점을 정하는 방법, planning 연관 높음</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2610.29408'>LiveAct: Towards Real-Time Multi-Agent World Models with Heterogeneous Action Interfaces</a></td><td>70</td><td>6</td><td>World Model</td><td>이종 action interface를 갖는 multi-agent 실시간 video world model임</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2610.29435'>Events, Not Pixels: Where World Models Get the Return Wrong</a></td><td>70</td><td>6</td><td>World Model</td><td>world model이 return을 틀리는 지점이 event transition임을 진단 실험으로 보임, Atari 중심이나 planning 평가 관점이 참신함</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2610.28948'>COWBOY: A Scalable Sim-to-Real Framework for Learning Contextual Whole-Body Manipulation</a></td><td>68</td><td>9</td><td>Manipulation</td><td>모바일 whole-body 조작을 위한 확장형 sim-to-real 프레임워크로 실로봇 검증함</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2610.29829'>Robot Generalization Beyond Volume: The Diversity Path via Zero-Shot Capabilities</a></td><td>68</td><td>9</td><td>Embodied AI</td><td>볼륨보다 다양성과 zero-shot 능력을 강조하는 robot 일반화 입장 논문임</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2610.29997'>DONIC: Generalist Dexterous Bimanual Tracking Control from Human Demonstrations</a></td><td>68</td><td>9</td><td>Dexterous</td><td>범용 양손 dexterous tracking 제어를 인간 시연에서 학습함</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2610.29936'>DewHand: Direct Metric World-Space Hand Motion Reconstruction from Egocentric Videos</a></td><td>68</td><td>7</td><td>3D Vision</td><td>egocentric video에서 metric 월드 좌표 손 동작 복원, 로봇 모방학습 데이터로 활용 가능함</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2610.28788'>ArcFlow: Training Flow Policies for Multiple Solver Budgets</a></td><td>68</td><td>7</td><td>RL</td><td>flow policy를 여러 solver 예산에서 RL 학습, 로봇 policy inference 효율과 직결됨</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2610.29075'>Value-Rectified Distillation for Flow-based Offline Reinforcement Learning</a></td><td>68</td><td>7</td><td>RL</td><td>flow 기반 offline RL 증류의 OOD mode averaging 해결, 다중모달 policy와 연관 높음</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2610.29139'>Steering Black-Box Large Language Model Agents with Pitfall Anticipation World Model</a></td><td>67</td><td>5</td><td>World Model</td><td>실패 직전 pitfall만 예측해 black-box agent를 유도하는 world model로 failure anticipation 주제와 맞으나 LLM agent 환경 한정임</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2610.29692'>FlowVLA: Learning Flow-Aware Physical Completion for Quantitative Robotic Pouring</a></td><td>66</td><td>9</td><td>VLA</td><td>pouring에서 물리적 완료 추정을 분리한 VLA로 모호성 문제를 다룸</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2610.28962'>RoPT: Robust 6DoF Object Pose Tracking in Video</a></td><td>66</td><td>8</td><td>3D Vision</td><td>로봇 상호작용용 6DoF 물체 pose tracking의 강건성 개선, 인식 모듈 수준임</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2610.33074'>AGQ: Action-Guided Ultra-Low-Bit Quantization for Vision-Language-Action Models</a></td><td>66</td><td>8</td><td>VLA</td><td>VLA 초저비트 양자화를 action 기준으로 유도, 온보드 배포용 efficient inference로 실용적임</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2610.29203'>NavBind: Diagnosing Instruction-Action Binding at Route Forks in Navigation VLAs</a></td><td>66</td><td>8</td><td>Navigation</td><td>navigation VLA의 지시-행동 결합 진단으로 분석 관점이 좋음</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2610.29677'>Toward Recursive Self-Improvement in Physical AI</a></td><td>66</td><td>8</td><td>Embodied AI</td><td>physical AI의 recursive self-improvement를 논하는 새 문제 설정임</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2610.29964'>Object- and Task-Aware Active Perception for Safe Navigation of Mobile Manipulators in Semi-Static Environments</a></td><td>66</td><td>8</td><td>Active Perception</td><td>객체와 과제 인지 active perception으로 준정적 환경 내비게이션을 안전화함</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2610.29088'>Causal world models under physical parameter shifts</a></td><td>66</td><td>7</td><td>World Model</td><td>물리 파라미터 변화 하 causal world model 분석, 합성 벤치마크 위주라 규모 작음</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2610.28945'>Self-Improving Agents with World Model Predictive Paths</a></td><td>66</td><td>5</td><td>World Model</td><td>world model로 후보 행동 결과를 상상하는 MPPI식 test-time planning과 경험 메모리 결합, ALFWorld 한정이나 주제 적합함</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2610.29246'>DepState-JEPA: Learning Depth-Grounded State Representation for Visual Perception and Manipulation</a></td><td>64</td><td>9</td><td>Representation</td><td>깊이 기반 JEPA 상태 표현을 조작에 연결하는 representation learning임</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2610.29915'>CausalAlign: Causal Alignment of Video Generation Models for Consistent Ego-Motion</a></td><td>64</td><td>5</td><td>Video</td><td>video generation의 camera ego-motion 일관성을 causal alignment로 개선, world model 간접 연관임</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2610.28801'>JUICE: Unified Multimodal Modeling in Pretrained Representation Spaces</a></td><td>64</td><td>2</td><td>Multimodal</td><td>사전학습 표현 공간에서 이미지·텍스트를 하나의 과정으로 생성하는 통합 모델임</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2610.30044'>SP-HLM: Sparse-Pose-Driven Motion Generation and Whole-Body Control for Humanoid Loco-Manipulation</a></td><td>62</td><td>9</td><td>Humanoid</td><td>sparse pose 인터페이스로 humanoid loco-manipulation 전신 제어를 연결함</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2610.28893'>Flexible Language-Guided Representation Editing for Adaptive Robot Behavior</a></td><td>62</td><td>8</td><td>Robot Learning</td><td>언어로 표현 공간을 편집해 시연 의도를 정렬하는 language feedback 학습임</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2610.29724'>Sufficient and Necessary Causal Explanations for the Analysis of Autonomous Systems</a></td><td>62</td><td>6</td><td>Failure Analysis</td><td>자율 시스템 실패에 대한 충분 필요 인과 설명으로 failure diagnosis와 연결됨</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2610.30105'>Asymmetric On-Policy Distillation Learns In-Context Exploration</a></td><td>62</td><td>6</td><td>RL</td><td>비대칭 on-policy distillation으로 부분관측 탐색 행동을 학습함</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2610.29317'>SpatialBrain: Spatial Intelligence Growing from Experience</a></td><td>62</td><td>6</td><td>Embodied AI</td><td>3D 공간 기억과 skill library, 경험 축적으로 공간 추론을 개선, 벤치마크 향상폭 근거 부족하나 주제 적합함</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2610.29107'>PhyMo: Learning Physical Dynamics with Accurate and Continuous Motion from Multi-View Videos</a></td><td>62</td><td>5</td><td>3D Vision</td><td>multi-view video에서 물리 동역학 복원, 4D 표현과 물리 파라미터 추정에 관련됨</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2610.29989'>Looking Ahead: Modeling Future Evolution in Autoregressive Video Generation</a></td><td>62</td><td>5</td><td>Video</td><td>autoregressive video 생성이 장면 진화를 모델링하도록 하는 학습, world model 간접 연관임</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2610.30127'>VoxProg: 3D Spatial Reasoning through Voxel Programming</a></td><td>62</td><td>5</td><td>Embodied AI</td><td>voxel programming으로 3D spatial reasoning 수행, embodied spatial reasoning 관련임</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2610.29229'>Cache Locally, Recompute Selectively for Streaming Video Understanding</a></td><td>62</td><td>4</td><td>Video</td><td>streaming video LLM의 KV cache 선택적 재계산, efficient inference 개선임</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2610.28925'>One Policy, Many Styles: Where to Aggregate Preferences for Steerable Humanoid Control?</a></td><td>60</td><td>8</td><td>RL</td><td>선호 조건 humanoid 정책에서 선호 집계 위치를 분석한 steerable control 연구임</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2610.29646'>From Association to Decision Value: Testing Paired Instruction Dependence for VLA Corpus Selection</a></td><td>60</td><td>7</td><td>VLA</td><td>로봇 demonstration corpus 선택에 paired instruction dependence 진단을 시험, 주요 이득 불확실함을 정직하게 보고하나 quadruped navigation 한정임</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2610.29676'>DriveMLP: When Training Strategy Outperforms Model Complexity in Autonomous Driving</a></td><td>60</td><td>6</td><td>RL</td><td>자율주행 closed-loop IL에서 학습 전략이 모델 복잡도보다 중요함을 보임, IL 관점 연관 높음</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2610.28827'>WorldStream: Streaming Interactive 3D Worlds with Hierarchical Planning and Persistent State</a></td><td>60</td><td>5</td><td>World Model</td><td>언어로 조작되는 스트리밍 3D world model이나 게임/생성 성격이 강함</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2610.29327'>OACap: Caption-Guided Active Observation for Detailed Video Captioning</a></td><td>60</td><td>4</td><td>Video</td><td>caption 유도 능동 관찰로 상세 video captioning, active perception 아이디어임</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2610.29454'>BlazeVGGT: 13x Faster VGGT at 2,000 Frames via Camera Token without Training</a></td><td>60</td><td>4</td><td>3D Vision</td><td>VGGT를 학습 없이 13배 가속, efficient inference로 유용하나 engineering 성격임</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2610.29241'>Encoded but Unused: Bounding the Sources of VLM Errors</a></td><td>60</td><td>3</td><td>Multimodal</td><td>VLM 오류를 표현 실패와 활용 실패로 분해, 진단 관점이 유용함</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2610.29117'>Learning to Absorb Corrections: Critic-Weighted Residual Flow for Vision-Based Insertion</a></td><td>58</td><td>8</td><td>Manipulation</td><td>critic 가중 residual flow로 삽입 과제 교정을 흡수하는 온라인 학습임</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2610.29903'>HuMiT: Low-Latency Whole-Body Humanoid Teleoperation via Compact Reference Tracking</a></td><td>58</td><td>8</td><td>Humanoid</td><td>압축 reference tracking으로 저지연 전신 텔레오퍼레이션을 구현함</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2610.30043'>TARSphere: A Robot-Oriented Full-Stack Framework for Long-Horizon Embodied Agents in Evolving Physical and Social Environments</a></td><td>58</td><td>8</td><td>Embodied AI</td><td>장기 embodied agent 풀스택 프레임워크로 시스템 통합 성격임</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2610.29612'>Watch Your Step: Anticipated Perception for Humanoid Locomotion</a></td><td>58</td><td>7</td><td>Locomotion</td><td>예측 지각으로 발 디딤 지형 정보만 쓰는 humanoid 보행 정책임</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2610.30108'>Multimodal Embodied Agents: A Unified Capability-centric Perspective from Computer-Use to Robot-Use</a></td><td>58</td><td>7</td><td>Embodied AI</td><td>computer-use에서 robot-use까지 능력 중심 관점의 서베이임</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2610.30013'>ClunoGS: Compact Language 3D Gaussian Splatting via Unified Optimization</a></td><td>58</td><td>5</td><td>3D Vision</td><td>language 3DGS의 compact 압축, semantic 3D 표현 관련이나 효율 개선 위주임</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2610.29061'>OccJEPA: Occlusion as Masking for Amodal Video Segmentation</a></td><td>58</td><td>3</td><td>Video</td><td>occlusion을 masking으로 보는 amodal video segmentation, JEPA world model 활용함</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2610.29409'>LLMSeg: Training-Free Text-Prompted Image Segmentation with B-Splines</a></td><td>58</td><td>3</td><td>Multimodal</td><td>MLLM이 학습 없이 detect, B-spline 윤곽 추적, refine 3단계로 마스크를 직접 그려 ReasonSeg val 71.5 cIoU로 SAM 3에 필적하게 한 설계가 흥미로우나 상용 backend 의존이고 로봇 연결은 약함</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2610.29995'>Remembering Through Change: Provenance-Preserving Hypergraph Memory for Multimodal Agents</a></td><td>58</td><td>3</td><td>Multimodal</td><td>멀티모달 agent용 hypergraph 메모리로 entity 상태 변화와 시각 근거를 추적, robot memory와 약하게 연결됨</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2610.29671'>Uni-Mem: Learning a Long-Horizon Agentic Memory Manager with Unified Online Policy Optimization</a></td><td>58</td><td>2</td><td>NLP</td><td>agent 메모리 구성·검색을 단일 policy로 online RL 학습, Stage-Decoupled GRPO가 참신하고 memory 주제와 약하게 연결됨</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2610.29854'>How Do DiTs Denoise? An Aggregator-Predictor View of Attention and MLPs</a></td><td>58</td><td>1</td><td>Generative</td><td>DiT denoising을 aggregator-predictor로 해석하는 이론적 분석임</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2610.29605'>Improved Training of Strong Stochastic Flow Maps</a></td><td>58</td><td>1</td><td>Generative</td><td>stochastic flow map 학습 개선, 생성 모델 방법론이나 로봇 연결 약함</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2610.30051'>From Reasoning to Action: Benchmarking Frontier AI Models on LIBERO-10 Robot Manipulation Tasks</a></td><td>55</td><td>9</td><td>Benchmark</td><td>frontier 모델을 LIBERO-10에서 평가하는 벤치마크 성격임</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2610.28955'>SLoSa: Small, Low-Power, and Safe Foundation Models for Robotic Task Planning</a></td><td>55</td><td>8</td><td>Task Planning</td><td>소형 저전력 foundation model로 안전 task planning을 시도함</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2610.29169'>SMR: Learning streaming motion retargeting for humanoids from human semantic</a></td><td>55</td><td>7</td><td>Humanoid</td><td>의미 보존 streaming 모션 리타게팅으로 humanoid 응용이나 incremental임</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2610.29377'>Integrating Flow Matching and Model Predictive Control for Safe Robot Navigation</a></td><td>55</td><td>7</td><td>Navigation</td><td>flow matching 경로 계획과 MPC 결합으로 안전성을 보강하나 방식은 직관적임</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2610.29452'>Distance Field Driven Reinforcement Learning for Reactive and Robust Collision Avoidance</a></td><td>55</td><td>7</td><td>RL</td><td>distance field를 RL에 직접 넣어 반응형 충돌 회피를 구현함</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2610.29761'>OMAR: Open-World Multi-Attribute Reasoning for Scene-Conditioned Shelf Organization</a></td><td>55</td><td>7</td><td>Embodied AI</td><td>다속성 추론으로 개방형 선반 정리를 수행하는 응용임</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2610.29845'>RangeNav: Task-Aligned LiDAR Range-Image Pretraining for Robot Navigation</a></td><td>55</td><td>7</td><td>Navigation</td><td>LiDAR range image 과제 정렬 사전학습으로 내비게이션 표현을 개선함</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2610.28821'>Register Anything Model for Generalizable and Robust Point Cloud Registration</a></td><td>55</td><td>4</td><td>3D Vision</td><td>범용 point cloud registration 모델, 일반화는 좋으나 로봇 직접 연관 약함</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2610.29517'>AutoPhyX: Automatic Text-Condition Physics Property Generation</a></td><td>55</td><td>4</td><td>3D Vision</td><td>텍스트 조건 물리 파라미터 생성으로 4D 시뮬레이션에 쓰이나 응용 범위 제한적임</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2610.28835'>Conditional Imaging for Privacy-Preserving Visual Sensing</a></td><td>55</td><td>3</td><td>CV</td><td>정적 광학계로는 privacy와 복원 가능성이 양립 못 함을 정보이론으로 보이고 프레임마다 광학 상태를 바꾸는 카메라 시제품까지 만든 점이 새로우나 얼굴 데이터셋 평가에 그침</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2610.28771'>Motion Equivariant Convolutional LSTM: When Motion Becomes a Gauge Symmetry</a></td><td>55</td><td>2</td><td>Video</td><td>motion equivariant ConvLSTM, 대칭성 기반 표현 아이디어는 흥미로우나 로봇 연결 약함</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2610.28914'>D-Skill: Distilling Teacher Knowledge through Agent Skills</a></td><td>54</td><td>3</td><td>LG</td><td>teacher 행동 차이를 skill 문서로 증류하며 ALFWorld 평가, 로봇 skill 학습과 약하게 연결됨</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2610.29934'>ToM2Vec: Continuous Theory-of-Mind Tokens for Multi-Agent Coordination</a></td><td>54</td><td>3</td><td>RL</td><td>연속 latent ToM 토큰으로 multi-agent 협력 개선, Overcooked 포함 여러 환경에서 검증하나 로봇 직접 연결은 약함</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2610.29102'>Diffusion Posterior Sampling with Uncertain Forward Models</a></td><td>54</td><td>1</td><td>Generative</td><td>불확실한 forward model에서 diffusion posterior sampling, 이론적 기여 있음</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2610.29699'>AirPlayground: Benchmarking Aerial Navigation across Diverse Reconstructed Environments</a></td><td>52</td><td>7</td><td>Navigation</td><td>복원 환경 기반 항공 내비게이션 벤치마크로 데이터셋 기여임</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2610.29474'>Extending Affordance Segmentation for Wearable Robots to Multi-Object Images</a></td><td>52</td><td>6</td><td>Manipulation</td><td>보철/웨어러블 로봇용 graspable part affordance를 다중 물체로 확장, 작은 개선임</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2610.28950'>HyperDrone: Simulation-to-Reality Transfer at Millions of Frames per Second</a></td><td>52</td><td>6</td><td>Simulation</td><td>쿼드로터 배치 렌더링 시뮬레이터 속도 개선으로 도구 기여 중심임</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2610.29432'>PRISM: Learning Realistic Depth via Physics-Grounded Noise Disentanglement with Semantic-Geometric Collaboration</a></td><td>52</td><td>6</td><td>Sim2Real</td><td>물리 기반 depth noise 분리로 sim-to-real 간극을 줄이는 센서 모델링임</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2610.29568'>Mixture of Flow Matching and Particle Filter for Proprioception-Based Online Contact Estimation</a></td><td>52</td><td>6</td><td>State Estimation</td><td>flow matching과 particle filter로 고유수용 접촉 추정함</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2610.28803'>Towards Realistic Models of Change: A Causal Perspective on Decision-Making and Dynamical Systems</a></td><td>52</td><td>4</td><td>LG</td><td>인과 관점의 decision-making과 dynamical system 개관, 위치 논문성임</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2610.28776'>Complexity-Aware Surgical Video Reasoning Segmentation with Digital Twin and Context Memory</a></td><td>52</td><td>3</td><td>Video</td><td>수술 video reasoning segmentation에 digital twin과 memory 사용함</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2610.28954'>Pair-Free Coarse-to-Real Video Generation via Real-to-Coarse Image Supervision</a></td><td>52</td><td>3</td><td>Video</td><td>pair 없이 coarse-to-real 영상 변환, sim-to-real 관련성 있음</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2610.28915'>A Model-Free Continuous-Time RL Algorithm from Discrete-Time Off-Policy Data with End-to-End Guarantees</a></td><td>52</td><td>3</td><td>RL</td><td>이산 off-policy 데이터로 continuous-time RL 보장 제시, 이론 중심임</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2610.29237'>MA-UITD: Offline Multi-Agent Reward Inference for Characterizing Continuous Social Behavior</a></td><td>52</td><td>3</td><td>RL</td><td>multi-agent offline inverse RL로 사회 행동 보상 추론, IL과 약하게 연결됨</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2610.29357'>Memory-Centric Continual Learning for AI Agents</a></td><td>52</td><td>3</td><td>Agent Memory</td><td>에이전트 지속 학습을 memory 중심으로 구성하는 관점이 robot memory와 닿음</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2610.29272'>Certified Abstention for Provably-Unidentifiable Index-Phase Recovery in Image Registration</a></td><td>52</td><td>2</td><td>CV</td><td>위치 충실도와 위상 충실도가 독립임을 보이고 식별 불가능 영역에서는 구조를 지어내지 않고 abstain하는 인증 프레임워크를 이론과 실제 스캐닝 장비로 확인한 점이 신선하나 로봇 직접 연결은 약함</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2610.29552'>Generalized CycleGRPO for Fine-Grained Multimodal Understanding and Grounding</a></td><td>52</td><td>2</td><td>Multimodal</td><td>CycleGRPO로 region 이해와 grounding을 함께 학습함</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2610.30036'>Attn-Forcing: Learning Full-Context Attention Proxies for Streaming Video Generation</a></td><td>52</td><td>2</td><td>Video</td><td>streaming video 생성의 full-context attention proxy 학습, 효율 개선임</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2610.28858'>DualHeads: Reward-tilted few-step diffusion made simple</a></td><td>52</td><td>1</td><td>Generative</td><td>few-step diffusion을 reward로 정렬하는 간단한 방법임</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2610.29380'>AdvFidelity: Unifying Preference Alignment and Few-Step Image Generation within Reinforcement Learning</a></td><td>52</td><td>1</td><td>Generative</td><td>RL 선호 정렬과 few-step 생성을 통합함</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2610.29581'>Unlocking Spatial Grounding in Flow-Matching Models via SNR Tuning</a></td><td>52</td><td>1</td><td>Generative</td><td>flow-matching의 SNR tuning으로 공간 grounding 확보, 간단한 아이디어임</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2610.29784'>Evolving with Open Worlds: Towards Recursive Self-Improvement for Future Forecasting</a></td><td>52</td><td>1</td><td>NLP</td><td>미래 예측 환경에서 agent 자기개선을 다루며 FutureX 1위를 주장하나 로봇 관련성 낮음</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2610.29244'>Failure Modes of Vision-Language Models for Human Activity Understanding in Thermal HRI</a></td><td>50</td><td>6</td><td>Embodied AI</td><td>thermal HRI에서 VLM 실패 양상 분석, 로봇 관련 있으나 평가 위주임</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2610.29586'>End-to-End Reinforcement Learning for Quadrupedal Jumping in Lunar Gravity</a></td><td>50</td><td>6</td><td>Locomotion</td><td>달 중력 사족 점프 RL로 응용 사례 성격임</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2610.29839'>Spacetime Splines for Adaptive Robot Motions</a></td><td>50</td><td>6</td><td>Motion Primitives</td><td>시공간 spline 이동 프리미티브로 표현 제안이나 규모는 작음</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2610.29024'>Dissimilarity-Based Markov Decision Processes for Stabilizing State Distributions</a></td><td>50</td><td>4</td><td>RL</td><td>상태 분포 안정화를 위한 MDP 이론 틀, 제어 관점에서 일부 연결됨</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2610.29200'>NeuralSRender: G-Buffer Guided Video Diffusion for Sim-to-Real Rendering</a></td><td>50</td><td>3</td><td>Video</td><td>자율주행용 sim-to-real 영상 변환, 데이터 생성 응용임</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2610.28883'>RL-IF: Tracking Non-local Training Data Influence for Online Reinforcement Learning</a></td><td>50</td><td>3</td><td>RL</td><td>online RL 학습 데이터 영향 추적, 로봇 직접 연결 약함</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2610.29621'>Reliability-Aware Probabilistic Fusion for Multimodal Learning with Incomplete Evidence</a></td><td>50</td><td>3</td><td>Multimodal</td><td>결측 모달리티 reliability-aware 융합, 센서 강건성에 일부 연결됨</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2610.28806'>SAIL: A Learnable Generalisation of Spatial Autocorrelation over Graph-Structured Data</a></td><td>50</td><td>2</td><td>CV</td><td>Moran I·Geary C를 학습 가능한 연산자로 일반화하고 고전 통계를 정확히 복원함을 보인 점은 탄탄하나 실험이 합성·생의학 그래프에 한정되고 로봇 연결은 약함</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2610.29106'>DriftNeRF: Cross-Ray Density Drifting for Sparse-View Neural Radiance Fields</a></td><td>50</td><td>2</td><td>3D Vision</td><td>sparse-view NeRF에 cross-ray density 정규화 제안, 명확한 결함 진단임</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2610.28811'>A Mechanistic Study of Automated Failure Attribution in LLM-based Agentic Systems</a></td><td>50</td><td>2</td><td>NLP</td><td>LLM multi-agent failure attribution 분석, failure diagnosis와 약하게 연결됨</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2610.29172'>Conditional Flow Models Convert Epistemic Uncertainty into Apparent Aleatoric Variance</a></td><td>50</td><td>2</td><td>Generative</td><td>conditional flow의 epistemic을 aleatoric으로 오인하는 문제 분석, 불확실성 관련임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2610.29823'>MemoryTax: The Bitter Lesson of Agent Memory</a></td><td>50</td><td>2</td><td>NLP</td><td>agent memory 설계가 강한 모델에서 불필요함을 보이나 대화 하나·1회 실행뿐인 소규모 실험임</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2610.29308'>LLM-Based Exogenous World Modeling for Dynamic Scheduling</a></td><td>50</td><td>2</td><td>World Model</td><td>LLM을 exogenous world model로 쓴 동적 스케줄링 planning, 로봇과는 간접 연결임</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2610.29003'>T-DIG: Text-Conditioned Diversity for Image Generation</a></td><td>50</td><td>1</td><td>Generative</td><td>frozen 생성기 앞에 GRPO로 학습한 LLM policy를 두어 사용자 지정 축으로 이미지 다양성을 높이는 설계와 데이터셋이 쓸 만하나 로봇 연결은 없음</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2610.28905'>Hidden Messages Between Diffusion Language Model Agents: Causal Evidence for Latent Communication</a></td><td>50</td><td>1</td><td>LG</td><td>diffusion LM agent 간 latent 통신의 인과 증거를 보여 실험 설계는 좋으나 로봇 무관</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2610.28953'>GGraph: A GPU-Accelerated Library for Graph-Based Robot Deployment and Learning</a></td><td>48</td><td>6</td><td>Navigation</td><td>GPU 가속 그래프 라이브러리로 scene graph 계열 도구이나 엔지니어링 중심임</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2610.30080'>Do Earth-Trained Humanoid Controllers Walk on the Moon? Gravity, Terrain, and Soil Transfer</a></td><td>48</td><td>6</td><td>Locomotion</td><td>지구 학습 humanoid의 달 전이 비교 연구로 경험적 분석임</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2610.28901'>Learning Dynamic Games for Cooperative Iterative Tasks</a></td><td>48</td><td>5</td><td>Multi-agent Control</td><td>동적 게임 학습 프레임워크로 이론은 있으나 로봇 학습 핵심과는 거리 있음</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2610.28829'>HorizonComposer: Spatiotemporally Consistent Driving Video Editing with Enriched Traffic Semantics</a></td><td>48</td><td>3</td><td>Video</td><td>주행 영상 편집의 시공간 일관성과 교통 의미 보존임</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2610.29174'>LocalAgent: Collaborative Agentic Verification for Fine-Grained Instance-Level Consistency</a></td><td>48</td><td>3</td><td>Multimodal</td><td>agentic 검증으로 인스턴스 일관성 판단, 응용적임</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2610.29618'>FogTTA: Online Test-Time Adaptation for Robust Transformer-based Object Detection in Foggy Weather</a></td><td>48</td><td>3</td><td>CV</td><td>자율주행 안개 환경 detection의 online test-time adaptation임</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2610.29788'>Open-Vocabulary Models and Label Propagation for Uncertainty-aware Pseudo-Labeling of Object Detection Datasets</a></td><td>48</td><td>2</td><td>CV</td><td>open-vocabulary 검출기 표현으로 object 유사도 그래프를 만들어 soft label을 전파하고 COCO에서 라벨 1%로 40.5 AP(전체 라벨 40.9)를 달성했으나 로봇과는 간접 연결임</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2610.33072'>VLMProbe: An Open-source Library for VLM Probing and Interpretation</a></td><td>48</td><td>2</td><td>Multimodal</td><td>VLM probing 오픈소스 라이브러리, 도구 성격임</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2610.29014'>GenXR-Bench: Benchmarking Coding Agents for Interactive XR Development</a></td><td>48</td><td>2</td><td>Embodied AI</td><td>XR 개발용 coding agent benchmark로 physical grounding 실패를 분석하나 로봇은 아님</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2610.29816'>COMET: A coordinated multi-layer runtime monitoring framework for human-supervised AI-enabled safety systems</a></td><td>48</td><td>2</td><td>LG</td><td>다층 runtime monitor로 fault mode를 진단, failure detection 관점이나 압축공기 누출 데이터 한정임</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2610.28843'>Beyond Correct Answers: How Compositional Cues Shape Visual Judgments</a></td><td>48</td><td>1</td><td>Multimodal</td><td>VQA의 compositional cue 영향 분석임</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2610.28889'>Policy-Mask: Budget-Aware Adaptation of Diffusion Features to Discriminative Tasks</a></td><td>48</td><td>1</td><td>CV</td><td>diffusion feature 선택을 budget-aware로 학습함</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2610.29248'>ER-Chord: Spatially Consistent One-Step Image Editing via Equal-Energy Reliability Redistribution</a></td><td>48</td><td>1</td><td>Generative</td><td>neighboring noise level 간 일치도를 신뢰 신호로 삼아 editing 강도를 equal-energy 최적화로 재분배하는 training-free 해법이 깔끔하나 편집 benchmark 개선에 한정되고 로봇과 무관함</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2610.29441'>Sparsity Should Be ALLOTted by Output: Training-Free Allocation of Block-Sparse Attention for Video Diffusion Transformers</a></td><td>48</td><td>1</td><td>Video</td><td>video DiT block-sparse attention 할당, 효율 개선임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2610.29780'>JointLight: Human-Centric Video Relighting with Asynchronous RGB-Irradiance Joint Modeling</a></td><td>48</td><td>1</td><td>Video</td><td>noise가 고주파 artifact만 지우고 저주파 광 전달을 남긴다는 관찰로 RGB와 irradiance를 서로 다른 timestep으로 함께 denoise하는 설계가 참신하나 인물 relighting 한정이고 로봇 연결은 약함</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2610.30023'>RealMe: Immersive Volumetric Video from Minimal Captures</a></td><td>48</td><td>1</td><td>3D Vision</td><td>sparse 촬영으로 volumetric video 생성, 응용 중심임</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2610.30035'>Plausible but Unimplantable: A Trustworthiness Audit of Shape Completion Foundation Models for Cranial Defect Reconstruction</a></td><td>48</td><td>1</td><td>Medical</td><td>사전학습 shape completion 모델 3종이 두개골 결함 239건에서 아무것도 안 하는 것보다 낫지 않고 이식 가능한 출력이 없음을 보인 감사가 명확하나 새 방법은 없고 의료 한정임</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2610.33071'>DuoPIC: Uncertainty-Aware Voxel-Level Digital Twins of Cerebral Perfusion with Transport PDEs in Acute Stroke</a></td><td>48</td><td>1</td><td>Medical</td><td>Windkessel 유량 모델과 tracer 수송 PDE에 neural closure를 얹어 불확실성까지 낸 물리 기반 digital twin으로 ISLES 병변 검출 AUC 최고를 냈으나 뇌 관류 한정이고 로봇 연결은 약함</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2610.29427'>One Act, Many Masks: Effect-Marginal Policy Optimization for Long-Horizon Agents</a></td><td>48</td><td>1</td><td>RL</td><td>long-horizon LLM agent의 effect 단위 policy optimization임</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2610.29249'>MOSAIC: An Omni-Modal Benchmark for Long-Term Memory and Cross-Modal Reasoning in Conversational Agents</a></td><td>48</td><td>1</td><td>Multimodal</td><td>omni-modal 장기 memory 벤치마크로 memory 관점 약한 연결 있음</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2610.29518'>Mitigating Query Shortcuts in Chain-of-Thought with Context-Aware Decoding</a></td><td>48</td><td>1</td><td>NLP</td><td>CoT에서 rationale 유무 분포를 대조하는 training-free 디코딩이며 CAD 응용 수준이라 novelty 제한적임</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2610.28763'>Automating ML for Science: Can Frontier Agents Climb Scientific Hills in the Wild?</a></td><td>48</td><td>1</td><td>NLP</td><td>과학 ML에서 coding agent 한계를 측정한 testbed, 로봇 무관</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2610.29271'>ARCANA: A Benchmark for Abstraction and Analogical Reasoning</a></td><td>48</td><td>1</td><td>NLP</td><td>유추 추론 benchmark와 ConceptSIR 제안, 로봇 관련성 낮음</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2610.28770'>ReAPO: Retry-Aware Policy Optimization for Efficient Exploration in LLM Reasoning</a></td><td>48</td><td>0</td><td>RL</td><td>LLM reasoning RLVR 탐색 개선, incremental임</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2610.29352'>Don&#x27;t Stop Long-Context Continual Pre-Training Too Early: An Empirical Scaling Law</a></td><td>48</td><td>0</td><td>NLP</td><td>장문 컨텍스트 사전학습 토큰 스케일링 법칙 실증임</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2610.29410'>ECHO: Emergent Common-Mode Hidden Offsets Drive Vocabulary Collapse in Preference Optimization</a></td><td>48</td><td>0</td><td>LG</td><td>선호 최적화 vocabulary collapse 원인을 공통 오프셋으로 설명함</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2610.29832'>S-EDL: Eliciting Self-Evidence from Sequence Likelihoods for Semantic Calibration of LLMs</a></td><td>48</td><td>0</td><td>NLP</td><td>evidential 방식의 LLM semantic calibration, 방법은 정돈됐으나 로봇 무관</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2610.28815'>Forging More Tasks into Better Harnesses: Agentic Harness Evolution via Successive Scale Racing</a></td><td>47</td><td>1</td><td>NLP</td><td>agent harness 진화에서 증거 선택을 racing으로 최적화, 로봇 관련성 낮음</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2610.29727'>Accept or Repair: Preserving Passage-Supported Answers in Contrastive Decoding</a></td><td>47</td><td>0</td><td>NLP</td><td>passage 지지 여부를 확인해 contrastive decoding 부작용을 줄이는 training-free 방법, 로봇 무관</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2610.29933'>Graph Topology Meets Energy-Driven Pathfinding: Preserving Contextual Consistency in Retrieval-Augmented Generation</a></td><td>47</td><td>0</td><td>NLP</td><td>KG 기반 RAG에서 의미 토폴로지와 energy pathfinding 사용, 일반 RAG 개선임</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2610.29158'>SICAF: Time-Varying Focus Bottleneck for Self-Supervised Event-Based Optical Flow with Spiking Neural Network</a></td><td>46</td><td>3</td><td>CV</td><td>event 기반 optical flow를 SNN으로 self-supervised 학습함</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2610.29177'>ROCOCO: Robust Outline Completion of Occluded Curvilinear Objects</a></td><td>46</td><td>3</td><td>CV</td><td>가림 곡선 물체 윤곽 완성, flow matching 사용함</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2610.29388'>FM-Occ: Feature-Diverse Upsampling and Memory-Aware Decoding for 3D Occupancy Prediction</a></td><td>46</td><td>3</td><td>3D Vision</td><td>3D occupancy upsampling과 decoding 개선, incremental임</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2610.29196'>A Unified Evaluation Framework of Physical Adversarial Robustness in the Edge VLM Era</a></td><td>46</td><td>2</td><td>Multimodal</td><td>edge VLM의 physical adversarial robustness 평가 프레임워크임</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2610.29607'>No Frames, Just Frequencies: Bandwidth-Efficient Deployment-Time Adaptation for Smart Glasses</a></td><td>46</td><td>2</td><td>CV</td><td>스마트 글래스용 대역폭 효율 deployment-time adaptation임</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2610.29811'>Compositionality with Primitives: A Unified View from Euclidean to Hyperbolic Vision-Language Models</a></td><td>46</td><td>1</td><td>Multimodal</td><td>compositional zero-shot을 유클리드에서 쌍곡 공간으로 통합 시각화함</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2610.29875'>Stochastic Nonlinearities Improve Uncertainty Estimation</a></td><td>46</td><td>1</td><td>LG</td><td>확률적 비선형성으로 uncertainty 추정 개선함</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2610.33075'>Diagnosing and Mitigating Evidence Misgrounding in Multimodal Knowledge Editing</a></td><td>46</td><td>1</td><td>Multimodal</td><td>multimodal knowledge editing의 evidence misgrounding 진단과 완화임</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2610.29527'>RCSD: Reinforcement and Continual Learning for Domain-Specific Speculative Decoding</a></td><td>46</td><td>1</td><td>NLP</td><td>speculative decoding draft 학습을 accept/reject 선호쌍으로 바꾼 효율화 기법이나 로봇 관련성 낮음</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2610.28934'>Back Up Before You Regret: Measuring Backup Awareness and Automating Backup in Coding Agents</a></td><td>46</td><td>1</td><td>NLP</td><td>coding agent의 backup awareness benchmark와 plug-in 층, 되돌림 주제와 약한 연결임</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2610.29013'>Target Regeneration Shrinks the Gains of Draft-Training Objectives in Speculative Decoding</a></td><td>46</td><td>0</td><td>Efficient Inference</td><td>speculative decoding 이득 재평가로 분석 가치 있음</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2610.29136'>GRAFT: Restoring the Missing Sampling Interface in Continuous Diffusion Language Models</a></td><td>46</td><td>0</td><td>Generative</td><td>연속 diffusion 언어모델에 샘플링 인터페이스를 복원함</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2610.29378'>Right On Q: Recovering Reasoning under Quantization via Self-Generated Trajectories</a></td><td>46</td><td>0</td><td>Efficient Inference</td><td>self-generated trajectory로 양자화 추론 능력을 회복함</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2610.29792'>MAPS: Macro-Adaptive Parallel Reasoning for Regulating Search Momentum in Retrieval-Augmented Generation</a></td><td>46</td><td>0</td><td>NLP</td><td>RAG 반복 검색의 query drift를 병렬 reasoning으로 완화, 일반적인 RAG 개선임</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2610.29110'>GRAM: Group-wise Rank-Aware Model Merging via Subspace Alignment</a></td><td>46</td><td>0</td><td>LG</td><td>principal angle 기반 그룹별 model merging, 이론 근거는 있으나 로봇 무관</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2610.29134'>NormTune: Norm-Guided Parameter-Efficient Fine-Tuning for Reasoning-Intensive Tasks</a></td><td>46</td><td>0</td><td>NLP</td><td>update norm 기반 PEFT 보정으로 단순하고 효과 크나 로봇 무관</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2610.29167'>TeachBack: Learning to Teach via Bidirectional Preference Optimization for On-Policy Self-Distillation</a></td><td>46</td><td>0</td><td>NLP</td><td>on-policy self-distillation에서 teacher 행동까지 학습, 수학·논리 과제 한정임</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2610.29501'>Parallel Thinking for Large Language Model with Path Diversity</a></td><td>46</td><td>0</td><td>NLP</td><td>parallel thinking RL에서 경로 다양성 보상, 로봇 무관</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2610.29030'>PHD-Hand: A Printable Humanoid Dexterous Hand with Linkage-Driven 3-DOA Digits</a></td><td>45</td><td>7</td><td>Hardware</td><td>프린트 가능한 링크 구동 humanoid 손 설계로 하드웨어 기여임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2610.29142'>State-Dependent Objective Coordination for End-to-End Balance and Navigation</a></td><td>45</td><td>7</td><td>RL</td><td>불안정 플랫폼 균형과 내비게이션을 위한 목적 조율 RL로 incremental임</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2610.29467'>PreCoMem: Predictive Cognitive Memory for Self-Evolving Long-Term Dialogue Agents</a></td><td>45</td><td>2</td><td>NLP</td><td>예측 부호화식 대화 agent 메모리 갱신 규칙, robot memory와는 거리 있음</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2610.28766'>Different Defects, Different Effects: A Controlled Audit of Face Recognition Training Data</a></td><td>45</td><td>1</td><td>CV</td><td>MS1MV3의 중복·분할 ID 등 결함 5종을 통제 실험으로 따져 정리 효과를 보인 데이터 감사 연구라 방법론 novelty는 작고 로봇과 무관함</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2610.29025'>Single-Image Food Mass Estimators Do Not Transfer Their Gram Scale Across Datasets</a></td><td>45</td><td>1</td><td>CV</td><td>음식 질량 추정기가 데이터셋을 넘으면 gram 스케일이 어긋나고 Nutrition5k 무작위 분할이 정확도를 부풀림을 보인 진단 연구는 꼼꼼하나 새 방법은 없고 로봇 연결은 약함</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2610.29415'>CCG Diffusion: Combinatory Categorial Grammar-Driven Compositional and Syntactically Disambiguated Text-to-Image Generation</a></td><td>45</td><td>1</td><td>Generative</td><td>CCG 파싱 범주로 수식 관계를 읽어 prompt 재작성과 attention 유도에 쓰는 training-free 방법으로 PP 모호성 해소 이점이 있으나 T2I 벤치마크 한정이고 로봇 연결은 약함</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2610.29590'>CineEvolve: An Agentic Self-Evolution Framework for Cinematic Multi-Shot Video Generation</a></td><td>45</td><td>1</td><td>Video</td><td>다중 shot 영상 생성 agentic 자기 진화 프레임워크임</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2610.33078'>Evaluating Visual Language Models on Visual Grounding for Visually Impaired People</a></td><td>45</td><td>1</td><td>Multimodal</td><td>VLM의 visual grounding 평가와 VG-SHAP 제안, 평가 위주라 novelty 제한적임</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2610.28849'>When Do Gaussian Priors Fail? A Latent Geometry Investigation of RL Fine-Tuning</a></td><td>45</td><td>1</td><td>Generative</td><td>latent diffusion Gaussian prior의 RL fine-tuning 한계 분석임</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2610.29129'>Mitigating Reward Hacking in Realistic Scenarios Through Representation Engineering</a></td><td>45</td><td>1</td><td>NLP</td><td>representation engineering으로 reward hacking 완화, LLM 중심임</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2610.29475'>Density-Level Backward Error for Low-NFE Generative Flows</a></td><td>45</td><td>1</td><td>Generative</td><td>low-NFE flow 샘플링 backward error 이론, 효율 추론 연관 약함</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2610.29965'>CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents</a></td><td>45</td><td>1</td><td>RL</td><td>RL과 self-distillation gradient 충돌 완화, LLM agent 중심임</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2610.30014'>Agent Behavior Maps: Locating Agents by What They Would Do, Without Running Them</a></td><td>45</td><td>1</td><td>NLP</td><td>agent behavior map으로 rollout 없이 agent 위치화임</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2610.30107'>Velocity Ambiguity Profiles: Time-Resolved Bayes-Risk Diagnostics for Flow Matching</a></td><td>45</td><td>1</td><td>Generative</td><td>flow matching 시간별 Bayes-risk 진단 도구는 흥미로우나 로봇 연결 약함</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2610.29545'>PACE: Periodic and Channel-Aligned Encoding of Four-Bit Recurrent States</a></td><td>45</td><td>1</td><td>LG</td><td>linear attention 상태 4bit 양자화 개선이며 공학적 기여 중심이고 로봇과 거리 있음</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2610.30116'>Environment Duels: A Microcosm of LLM Co-Evolution</a></td><td>45</td><td>1</td><td>NLP</td><td>LLM 환경 작성·풀이 co-evolution benchmark, 로봇 관련성 낮음</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2610.29152'>From Augmentation to Synthetic Evidence: Evaluating Generated Chest Radiographs at Dataset Intake</a></td><td>45</td><td>0</td><td>Medical</td><td>합성 흉부 X선이 화질 검사와 출처 분류기를 동시에 통과하는 비율을 따져 출처 기록 검증 필요성을 주장한 분석은 흥미로우나 방법 기여가 약하고 로봇과 무관함</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2610.29881'>Expandable Modality Experts for Medical Vision-Language Learning</a></td><td>45</td><td>0</td><td>Medical</td><td>의료 영상 7개 modality에 확장 가능한 expert bank를 두고 기존 경로를 고정한 채 fundus·OCT expert를 추가하는 구조로 25개 설정 중 24개 최고를 냈으나 의료 한정이고 로봇과 무관함</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2610.29734'>Monitorability Is Trainable: Post-Training for Chain-of-Thought Monitorability</a></td><td>45</td><td>0</td><td>NLP</td><td>CoT monitorability post-training, LLM 안전 주제임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2610.29932'>FrontierCS 2: A Benchmark for Computer Science R&amp;D</a></td><td>45</td><td>0</td><td>NLP</td><td>LLM agent CS R&amp;D 벤치마크 FrontierCS 2임</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2610.28767'>SkillEval: Learning Interpretable Ability Profiles of LLMs via Cognitive Diagnosis Models</a></td><td>45</td><td>0</td><td>NLP</td><td>인지 진단 모델로 LLM 능력 프로필을 만드는 평가 연구임</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2610.28819'>LIFT: Scoped Constraints for Evaluating and Training Instruction Following</a></td><td>45</td><td>0</td><td>NLP</td><td>범위 제약 기반 지시 따르기 평가와 학습 제안임</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2610.28838'>How to Use Parallel Data for Multilingual Pretraining</a></td><td>45</td><td>0</td><td>NLP</td><td>다국어 사전학습에서 병렬 데이터 활용법을 체계적으로 비교함</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2610.28887'>Building AI Research Teams for Autonomous Discovery of Linear Attention Architectures</a></td><td>45</td><td>0</td><td>LG</td><td>AI 연구팀의 linear attention 자율 탐색 시도임</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2610.29498'>A Strong MoE Is All You Need for Process Supervision</a></td><td>45</td><td>0</td><td>NLP</td><td>MoE로 process supervision을 제공하는 방법임</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2610.29722'>Retrieval Augmented Generation Compositionality</a></td><td>45</td><td>0</td><td>NLP</td><td>RAG 구성요소 조합 효과를 450개 설정으로 통제 평가한 분석, 로봇 무관</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2610.30006'>Building Auditable AI Text Detectors with Sparse Autoencoders</a></td><td>45</td><td>0</td><td>NLP</td><td>SAE feature로 해석 가능한 AI 텍스트 탐지기를 만든 방법, 로봇 무관</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2610.30066'>Looped Uniform Diffusion Language Models</a></td><td>45</td><td>0</td><td>NLP</td><td>uniform diffusion LM에 looping을 적용해 학습 효율을 높인 효율화 연구임</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2610.29688'>Rethinking Post-hoc Debiasing of Large Pretrained Models</a></td><td>44</td><td>1</td><td>CV</td><td>pretrained 모델 post-hoc debiasing 재검토임</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2610.29443'>DynaWeave: Learning to Adapt through Dynamic Scenario Synthesis</a></td><td>44</td><td>1</td><td>Agent</td><td>동적 시나리오 합성으로 도구 사용 에이전트를 적응시킴</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2610.29751'>Bridging Foundational and Agentic Capabilities of LLMs</a></td><td>44</td><td>1</td><td>NLP</td><td>LLM 기초 능력과 agentic 실행 간 격차를 operation 단위로 진단하는 프레임워크, 로봇과 거리 있음</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2610.28982'>Behavior Beyond Text: Evaluating Refusal Transfer Failure in LLM Agents</a></td><td>44</td><td>1</td><td>NLP</td><td>텍스트 거부가 tool 사용으로 이어지지 않는 현상을 분석한 안전성 연구임</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2610.28989'>AgentPolicyForge: From Executable Environments to Policy Benchmarks and Adaptive Guards</a></td><td>44</td><td>1</td><td>NLP</td><td>실행 가능한 환경으로 policy benchmark와 guard를 만드는 agent 안전 연구임</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2610.29245'>CrashGym: Measuring the Decision Value of Experimentation for LLM Agents in Counterfactual Market Crashes</a></td><td>44</td><td>1</td><td>NLP</td><td>시장 폭락 시뮬레이터에서 실험의 의사결정 가치를 측정, counterfactual 요소 있으나 로봇 무관</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2610.30041'>Robust Soft Skill Adaptation via Behavioral Localization in Tool-Using Agents</a></td><td>44</td><td>1</td><td>NLP</td><td>soft prompt skill을 행동 국소화로 학습, SpreadsheetBench 한정임</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2610.29550'>Hyperspherical Simplex Representations for Backward-Compatible Retrieval</a></td><td>44</td><td>0</td><td>CV</td><td>backward-compatible retrieval용 hyperspherical simplex 표현임</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2610.29210'>Understanding Target Probability Reuse in Speculative Decoding</a></td><td>44</td><td>0</td><td>Efficient Inference</td><td>speculative decoding의 target 확률 재사용을 이론 분석함</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2610.29255'>Hierarchical Masked Diffusion Language Models</a></td><td>44</td><td>0</td><td>Generative</td><td>계층적 masked diffusion 언어모델 제안임</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2610.29331'>From Prompts to Posteriors: Can LLM Agents Perform Bayesian Inference in Context?</a></td><td>44</td><td>0</td><td>NLP</td><td>LLM의 in-context 베이즈 추론 평가로 로봇 무관</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2610.28909'>DiffResearch: Accelerating Deep Research with Diffusion Language Models</a></td><td>43</td><td>0</td><td>NLP</td><td>diffusion LM을 deep research에 적용해 속도를 높인 시스템, 로봇 무관</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2610.28761'>Human-Robot Interaction via Meta-Learning Based Mode Recognition and Adaptive Control</a></td><td>42</td><td>5</td><td>HRI</td><td>meta-learning 모드 인식과 적응 제어는 pHRI 응용이나 novelty 보통임</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2610.29647'>Reading the Room: Scale-ambiguous Semantic Registration of Sparse VSLAM Maps to Floor Plans in Partially Built Environments</a></td><td>42</td><td>5</td><td>Mapping</td><td>VSLAM 지도와 평면도 시맨틱 정합이나 건설 응용 중심임</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2610.29302'>Compressing Onboard Language Models for Space Robots under a Behavioral-Fidelity Requirement</a></td><td>42</td><td>4</td><td>Efficient LM</td><td>우주 로봇용 언어모델 저비트 압축은 응용 특수적임</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2610.29913'>Asking a Multimodal LLM Whether Someone Fell: Zero-Shot Screening of Low-Resolution Thermal Video in a Laboratory and an Occupied Home</a></td><td>42</td><td>3</td><td>Multimodal</td><td>MLLM으로 낙상 zero-shot 선별, 평가 위주임</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2610.28856'>Depth-guided Geometric Adaptation for Few-shot Image Classification</a></td><td>42</td><td>2</td><td>CV</td><td>few-shot 분류에 단안 depth 기반 geometry 보정과 patch 매칭을 얹은 module 조합이라 incremental하고 로봇 연결은 depth 활용 정도임</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2610.29231'>DisasterRoute: Evidence-Guided Dual-System Routing for Visual Disaster Question Answering</a></td><td>42</td><td>2</td><td>Multimodal</td><td>UAV 재난 VQA 이중 시스템 라우팅임</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2610.29257'>CRAB: Cuboid-based Representation for As-built BIM from Point Clouds</a></td><td>42</td><td>2</td><td>3D Vision</td><td>point cloud에서 BIM 복원, 건축 응용임</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2610.29959'>Training-free Acceleration for Blind Compressed Image Restoration via Activation-Calibrated Singular Value Decomposition</a></td><td>42</td><td>2</td><td>CV</td><td>압축 영상 복원 Transformer에 channel activation 가중 SVD를 쓰는 training-free 경량화로 파라미터 59% 감소는 실용적이나 복원 모델 한정이고 로봇 연결은 약함</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2610.28941'>MINER: Modeling Inter- and Intra-Person Variance for Reidentification</a></td><td>42</td><td>1</td><td>CV</td><td>옷 갈아입은 person re-ID에서 hard example 대조와 intra/inter 분산 균형을 쓴 단순 프레임워크로 benchmark 개선 위주이고 로봇 연결은 약함</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2610.29090'>ReSeg: Retraining-free segmentation of abdominal organs via generalizable semantic representation learning</a></td><td>42</td><td>1</td><td>Medical</td><td>합성 데이터만으로 사전학습해 복부 장기를 재학습 없이 분할하는 2단계 구조는 domain randomization 계열의 응용이며 의료 한정이라 로봇 연결은 약함</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2610.29098'>UNIVERS: Learning UNIversal Voxel-wise Embedding via Randomized Synthesis for generalizable one-shot landmark localization</a></td><td>42</td><td>1</td><td>Medical</td><td>장기 형태 템플릿으로 합성한 데이터와 voxel 대조학습으로 one-shot 랜드마크 위치를 찾는 방법이나 부신 3개 데이터셋 평가로 범위가 좁고 로봇 연결은 약함</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2610.29361'>Seeing through Denoising: Frequency-guided One-step Denoising for Infrared Small Target Detection</a></td><td>42</td><td>1</td><td>CV</td><td>적외선 소형 표적 검출을 diffusion 배경 복원 문제로 바꾸고 one-step denoising을 쓴 점은 관점이 있으나 세 benchmark 개선 위주이고 로봇 연결은 약함</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2610.29519'>Supervision-Adaptive Curriculum and Guarded Anti-Curriculum Learning for Dense Prediction</a></td><td>42</td><td>1</td><td>CV</td><td>dense prediction용 신뢰도 기반 curriculum과 spectral 후학습을 결합해 정확도를 올린 학습 기법으로 기존 학회 방법의 확장이고 로봇 연결은 약함</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2610.29537'>Melange: A Synthetic Visual Bias Benchmark for Multi-modal Large Language Models</a></td><td>42</td><td>1</td><td>Multimodal</td><td>MLLM 시각 편향 합성 benchmark임</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2610.29691'>Efficient Generative Image Compression with Quantized Latents Refinement</a></td><td>42</td><td>1</td><td>CV</td><td>양자화 latent 정제와 residual VQ 재구성으로 생성 압축 속도를 OneDC 대비 27배 이상 올린 효율 개선이며 Jetson 평가가 있으나 로봇 연결은 약함</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2610.29830'>Revealing Hidden Failure Modes in Chest X-ray Classification via Spectral Domain Analysis</a></td><td>42</td><td>1</td><td>CV</td><td>흉부 X-ray 실패 모드를 스펙트럼 분석으로 찾음</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2610.28892'>Combating Catastrophic Forgetting in Continual Domain Adaptation via Knowledge Recasting</a></td><td>42</td><td>1</td><td>NLP</td><td>LLM continual domain adaptation forgetting 완화임</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2610.29262'>Estimating Performance for Safe Deployment of Machine Learning Models</a></td><td>42</td><td>1</td><td>LG</td><td>라벨 없는 모델 성능 추정으로 안전 배포, 분포 변화 대응임</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2610.29473'>Asymmetry Tunneling Beyond Adaptive Equivariance Relaxation</a></td><td>42</td><td>1</td><td>LG</td><td>equivariant 네트워크의 대칭 깨짐 대응, 로봇 연결 약함</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2610.29526'>Geometric state space, memory representation and architectures</a></td><td>42</td><td>1</td><td>LG</td><td>attention 구조를 기하학 틀로 유도, 이론이나 로봇 연결 약함</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2610.29992'>SCDM: Scalable Causal Discovery in Nonlinear Temporal Systems with Meta-Learning</a></td><td>42</td><td>1</td><td>LG</td><td>비선형 시계열 causal discovery meta-learning, 인과 연관 약함</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2610.29318'>Asking What a Director Sees Can Change What Vision-Language Models Choose</a></td><td>42</td><td>1</td><td>Multimodal</td><td>VLM 관점 취하기 theory of mind 프롬프트 효과 분석임</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2610.28891'>Fig: Automated Multiagent Behavior Elicitor</a></td><td>42</td><td>1</td><td>NLP</td><td>게임 환경 개입으로 multiagent 행동을 유도하는 평가 시스템임</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2610.28987'>PerMIT: Securing Persistent Memory for LLM Agents via Machine-Checked Integrity Theorems and Scalable Community Trust</a></td><td>42</td><td>1</td><td>NLP</td><td>agent 영속 메모리 무결성 정리와 Lean 검증, 보안 중심이라 로봇 무관</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2610.29010'>An Evidence-Driven Multi-Agent Compound AI System for Head and Neck Proton Radiotherapy Planning</a></td><td>42</td><td>1</td><td>RL</td><td>양성자 치료 계획에 PPO와 LLM agent를 결합한 응용, 21명 환자라 규모 작음</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2610.30042'>HGM-Dual: Lineage-Aware Guided Agent Harness Optimization for Long-Horizon Planning</a></td><td>42</td><td>1</td><td>NLP</td><td>planning agent harness 진화를 lineage 문맥으로 개선, 로봇 무관</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2610.29322'>OpenMAP-HIE: Pathology Informed Score-based Diffusion Model for Unsupervised Neonatal Hypoxic-Ischemic Encephalopathy Lesion Segmentation</a></td><td>42</td><td>0</td><td>Medical</td><td>건강한 ADC 분포를 학습한 diffusion의 조건·무조건 noise 예측 차이로 신생아 HIE 병변을 찾는 아이디어는 쓸 만하나 Dice 0.283으로 성능이 낮고 의료 한정임</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2610.29431'>Look Beyond the Question: Preserve-Focus-Fuse for Whole-Slide Image Question Answering</a></td><td>42</td><td>0</td><td>Medical</td><td>전체 슬라이드 병리 영상 질의응답에서 morphology bank와 질문 기반 retrieval을 융합한 구조이며 WSI-Bench 개선 위주고 의료 한정이라 로봇과 무관함</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2610.29442'>Beyond Shortcut Learning: Hierarchical Spatial Prototype Regularization for Face Forgery Detection</a></td><td>42</td><td>0</td><td>CV</td><td>deepfake 탐지기에 prototype 직교성 regularization을 넣어 cross-dataset AUC를 5.6% 올린 plug-in module 수준이며 로봇과 무관함</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2610.29651'>Spatially Gated Demographic Steering for Debiasing Multi-Person Text-to-Image Generation</a></td><td>42</td><td>0</td><td>Generative</td><td>DiT attention map에서 인물별 마스크를 뽑아 인물마다 다른 인구통계 벡터로 steering하는 training-free 방식은 설계가 분명하나 편향 완화 한정이고 로봇과 무관함</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2610.29665'>Learning to Reason Like a Cytopathologist:Clinically Grounded Multiscale Evidential Learning for Cervical Cytology</a></td><td>42</td><td>0</td><td>Medical</td><td>자궁경부 세포 진단을 ordinal 연속체와 Dempster-Shafer 증거 융합으로 다뤄 불확실성 triage를 낸 구성은 설계가 있으나 의료 한정이고 로봇과 무관함</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2610.28937'>Auditing Conformal Prediction for Language Models Under Inference-Time Model Shift</a></td><td>42</td><td>0</td><td>NLP</td><td>LLM conformal prediction의 inference 설정 변화 감사임</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2610.29281'>Flat-RLVR: Sharpness-Aware Reinforcement Learning with Verifiable Rewards for Reasoning Capacity in LLMs</a></td><td>42</td><td>0</td><td>RL</td><td>sharpness-aware RLVR, LLM reasoning incremental임</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2610.29303'>ExpEvolve: Structuring and Reusing Experience for Open-Ended Discovery</a></td><td>42</td><td>0</td><td>NLP</td><td>진화형 코딩 agent 경험 재사용, 로봇 무관함</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2610.29346'>Benchmarking and Error Analysis of Deep Search and Deep Research LLM Agents</a></td><td>42</td><td>0</td><td>NLP</td><td>deep research agent 벤치마크와 오류 분석임</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2610.29385'>Parallelizable Probabilistic Latent Reasoning for Diverse Reasoning Trajectories</a></td><td>42</td><td>0</td><td>NLP</td><td>병렬 probabilistic latent reasoning 제안임</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2610.29458'>Harness Scaling for Generalizable Agentic Reinforcement Learning</a></td><td>42</td><td>0</td><td>RL</td><td>agent harness scaling RL, LLM agent 중심임</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2610.29999'>EPIC: Rethinking Trust Regions for Autoregressive LLM Policies via Exact-KL Prefix Importance-Ratio Clipping</a></td><td>42</td><td>0</td><td>RL</td><td>LLM policy exact-KL prefix clipping, LLM RL incremental임</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2610.30068'>Loopholing All the Way: Language Modeling with pure Self-Conditioning</a></td><td>42</td><td>0</td><td>Generative</td><td>diffusion LM pure self-conditioning임</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2610.30076'>Circuits of LLM Classifiers</a></td><td>42</td><td>0</td><td>LG</td><td>LLM 분류기 조합 회로의 최적성 이론은 깔끔하나 로봇과 무관함</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2610.28787'>Is Anyone Enforcing the Cartel? What Reinforcement Learning Teaches LLM Agents in Markets</a></td><td>42</td><td>0</td><td>NLP</td><td>시장 LLM 에이전트 담합 분석이며 로봇과 무관함</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2610.28886'>SANE: Automated Scorer-Specific Metamorphic Testing for LLM Judges</a></td><td>42</td><td>0</td><td>NLP</td><td>LLM judge 메타모픽 테스트 자동화로 평가 도구임</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2610.28895'>CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer</a></td><td>42</td><td>0</td><td>NLP</td><td>교차 tokenizer logit distillation 방법 개선임</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2610.29250'>Let Agents Design How They Search: Automatic Interface Optimization for Agentic Search</a></td><td>42</td><td>0</td><td>NLP</td><td>agentic search 인터페이스 자동 최적화임</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2610.29681'>Scaling Multilingual Pretraining of Pixel Language Models</a></td><td>42</td><td>0</td><td>NLP</td><td>pixel language model 다국어 scaling 분석으로 scale-up 성격이 강하고 로봇 무관</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2610.29922'>Unintended Side Effects of Value Training in LLMs</a></td><td>42</td><td>0</td><td>NLP</td><td>value 학습이 다른 가치·행동에 주는 부작용 분석, 로봇 무관</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2610.30103'>Did the Problem Actually Get Harder? Testing LLMs on Paired P and NP-Complete Problems Hardened by Adversarial Multi-Agent Rewriting</a></td><td>42</td><td>0</td><td>NLP</td><td>P/NP 쌍 문제 benchmark와 adversarial rewriting, 로봇 무관</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2610.29135'>LaVGuard: Selective Decoding for Contextual Value Drift</a></td><td>42</td><td>0</td><td>NLP</td><td>task 상대적 value drift를 디코딩으로 제어, 이론 보장은 있으나 로봇 무관</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2610.29414'>Solving Go under Positional Superko: Sound Proof Transfer and New Board Values</a></td><td>42</td><td>0</td><td>AI</td><td>superko 하 Go 풀이 solver로 기술적으로 탄탄하나 로봇 무관</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2610.29491'>RubricOpt: Self-Revision of Semantic Rubrics for Preference Optimization</a></td><td>42</td><td>0</td><td>NLP</td><td>rubric 자기 수정으로 DPO를 보조, 이득이 모델별로 엇갈림</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2610.30072'>Charts as Epistemic Actions for Experience-Driven Agentic Data Analysis</a></td><td>42</td><td>0</td><td>NLP</td><td>데이터 분석 agent가 차트를 인식 행동으로 쓰게 하는 경험 증류, 로봇 무관</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2610.28769'>Learning-Enhanced Observer for Sensorless Task-Null-Space Compliant Control</a></td><td>40</td><td>5</td><td>Control</td><td>센서리스 wrench observer와 compliant 제어로 고전 제어 중심의 incremental임</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2610.28920'>Navigation Explainability for Object Avoidance with LLMs for Assistive Robots</a></td><td>40</td><td>5</td><td>Navigation</td><td>시각장애인 안내용 LLM 내비게이션 설명 프레임워크로 응용 중심임</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2610.29212'>DetM-Tracker: Deterministic and Memory-Efficient VIS for Autonomous Industrial Inspection</a></td><td>40</td><td>3</td><td>CV</td><td>산업 검사용 메모리 효율 VIS, 응용 위주임</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2610.29398'>Region-Aware Multi-View Inspection Using Deep Learning and Domain-Informed Decision Fusion</a></td><td>40</td><td>2</td><td>CV</td><td>연료 분사 바늘 검사에서 두 모델 출력을 SOP 기반 결정 층으로 합쳐 오탐률을 57.6%에서 10.9%로 낮춘 산업 응용이며 방법 novelty는 작고 로봇 연결은 약함</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2610.33079'>Rethinking Video Storage for AI Training: Breaking Cross-Frame Dependencies for Efficient Random Access</a></td><td>40</td><td>2</td><td>CV</td><td>AI 학습용 video 저장 방식 개선, 시스템 엔지니어링 성격임</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2610.29580'>Fast Bayesian Optimization Through Linear Models</a></td><td>40</td><td>2</td><td>LG</td><td>선형 모델 기반 빠른 Bayesian optimization, 일부 제어 튜닝에 쓸 수 있음</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2610.28985'>MedBOE: Optimization-Based Estimation of Complete Patient Body Models from Whole-Body Medical Imaging</a></td><td>40</td><td>1</td><td>Medical</td><td>SMPL 템플릿을 전신 PET-CT의 누락 부위 보정에 최적화로 맞춘 응용으로 아이디어는 깔끔하나 의료 도메인 한정이고 로봇 연결은 약함</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2610.29047'>Weakly Supervised Fish Segmentation through Point-Supervised Tracking and Motion-Informed Language</a></td><td>40</td><td>1</td><td>CV</td><td>점 하나 라벨로 물고기 tracker와 언어 조건 분할 모델을 이어 붙인 파이프라인이며 DeepFish mIoU 개선 위주라 incremental하고 로봇 연결은 약함</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2610.29108'>WaFIR: Wavelet-Fourier Mixture-of-Experts with Subband-Adaptive Routing for Blind All-in-One Image Restoration</a></td><td>40</td><td>1</td><td>CV</td><td>all-in-one 복원 decoder에 subband 단위 expert routing을 넣어 PSNR 0.48dB를 올린 module 추가 수준이라 incremental하고 로봇 연결은 약함</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2610.29159'>RiO-DETRv2: Geometry-Aware Uncertainty Modeling Meets Real-Time Oriented Object Detection Transformer</a></td><td>40</td><td>1</td><td>CV</td><td>회전 객체 검출 DETR에 boundary 분포와 각도 잔차 refinement를 넣어 DOTA mAP를 1.2~1.5 올린 기존 모델의 점진적 개선이며 로봇 연결은 약함</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2610.29569'>Rethinking Underwater Image Enhancement: Learning through Text-Guided Degradation Curriculum</a></td><td>40</td><td>1</td><td>CV</td><td>수중 영상 개선에 text 기반 열화 합성과 curriculum, one-step diffusion을 묶은 학습 프레임워크이며 benchmark 개선 위주고 로봇 연결은 약함</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2610.29219'>PerSPL: Personalized Semi-supervised Preference Learning</a></td><td>40</td><td>1</td><td>NLP</td><td>개인화 reward model semi-supervised preference 학습임</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2610.29396'>Progressive Permutation Alignment with Temperature-Controlled Spectral Sharpening</a></td><td>40</td><td>1</td><td>3D Vision</td><td>INR weight 공간 permutation alignment, 로봇 연결 약함</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2610.30009'>Mitigating Model Collapse through Dreaming Learning</a></td><td>40</td><td>1</td><td>Generative</td><td>model collapse를 dreaming으로 완화, 스펙트럼 분석임</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2610.30026'>What the Author Wrote, What the Agent Reads: Silent Cue Loss in Enterprise Document Ingestion</a></td><td>40</td><td>1</td><td>NLP</td><td>문서 변환 시 서식 단서 손실을 측정한 분석으로 로봇 무관</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2610.29126'>Two for One: Privileged Learning for Resource-Constrained Screening</a></td><td>40</td><td>0</td><td>Medical</td><td>양안 teacher에서 단안 student로 privileged learning을 하는 구성은 표준적이고 AUROC 소폭 개선에 그치며 의료 한정이라 로봇과 무관함</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2610.29358'>Reading the Mask: Descriptor-Grounded BI-RADS Rationale Generation for Breast MRI Segmentation</a></td><td>40</td><td>0</td><td>Medical</td><td>BI-RADS 결정 트리의 측정값만 LLM이 문장으로 옮기게 해 유방 MRI 분할의 근거 설명을 만든 응용이며 faithfulness 지표가 자명한 편이고 로봇과 무관함</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2610.29643'>SemQAM: A Unified Generative Image Codec for Joint Semantic-Channel Coding and Modulation</a></td><td>40</td><td>0</td><td>CV</td><td>VQ 인덱스를 QAM 심볼에 묶어 의미·채널 부호화를 한 모델로 합친 codec으로 OneDC 대비 비트율 절감을 보였으나 통신 도메인 한정이고 로봇과 무관함</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2610.29697'>Forward-Only Learning for Shared-Kernel Wavelet Neural Networks without Backpropagation</a></td><td>40</td><td>0</td><td>LG</td><td>backprop 없는 forward-only 학습, 영향 제한적임</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2610.29740'>APED-CXR: Adaptive Privileged Evidence Distillation for Chest X-Ray Grounding with Image-Only Inference</a></td><td>40</td><td>0</td><td>Medical</td><td>보고서를 쓰는 teacher의 지지 점수로 이미지만 쓰는 student의 흉부 X선 박스 F1을 0.302에서 0.338로 올린 distillation 개선이며 ISBI 4쪽 규모이고 로봇과 무관함</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2610.30007'>Multiclass Boundary Refinement with Neural Cellular Automata for Remote Sensing Land Cover Segmentation</a></td><td>40</td><td>0</td><td>CV</td><td>neural cellular automaton으로 원격탐사 분할 경계를 다듬어 BIoU를 2.36 올린 소폭 개선이며 로봇과 무관함</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2610.28785'>Measure First, Then Allocate: Calibrated Rollout Budgets for MCP Agents in Reinforcement Learning</a></td><td>40</td><td>0</td><td>RL</td><td>MCP agent RL rollout 예산 할당, LLM agent 중심임</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2610.28958'>Transformers as Generic Deep Neural Networks: Exact Compilation, the Cost of Removing Activation-Activation Products, and Multi-Agent Attention Clustering</a></td><td>40</td><td>0</td><td>LG</td><td>Transformer를 일반 DNN으로 정확 compile, 로봇 무관함</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2610.28975'>How Does Orthogonalization Adapt to the Neural Network Hessian Structure? A Gradient Self Outer-Product Analysis at Initialization</a></td><td>40</td><td>0</td><td>LG</td><td>Muon 직교화와 Hessian 구조 분석, 로봇 무관함</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2610.29289'>Approximate Solomonoff Induction: On the Robustness of Learned Universal Predictors</a></td><td>40</td><td>0</td><td>LG</td><td>Solomonoff induction 근사 견고성 이론임</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2610.29426'>BIRD-RL: Scaling Agentic Reinforcement Learning over Stateful Data-Centric Environments</a></td><td>40</td><td>0</td><td>RL</td><td>SQL 디버깅 agentic RL 프레임워크, LLM 중심임</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2610.29476'>Generative Modeling via Nonlinear Schrödinger Bridges and Branching Diffusions</a></td><td>40</td><td>0</td><td>Generative</td><td>Schrodinger bridge와 branching diffusion 생성 모델 이론임</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2610.29927'>Your Benchmark Is an Empirical Measure Over Difficulty</a></td><td>40</td><td>0</td><td>NLP</td><td>benchmark를 난이도 측정으로 보는 평가 관점임</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2610.30086'>Orbitol: Crystal Generation on Wyckoff Orbits</a></td><td>40</td><td>0</td><td>LG</td><td>Wyckoff orbit 기반 결정 생성은 재료 분야 응용으로 로봇과 무관함</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2610.30118'>The role of locality and weight sharing in convolutional neural networks</a></td><td>40</td><td>0</td><td>LG</td><td>CNN locality와 weight sharing 이론 분석으로 로봇과 무관함</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2610.28992'>Language Impairment as a Lens onto Large Language Models</a></td><td>40</td><td>0</td><td>NLP</td><td>실어증 관점으로 LLM 국소 교란을 분석함</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2610.29292'>Credit Where Credit Is Due: Contrastive Attribution Topology Search for Multi-Agent Systems</a></td><td>40</td><td>0</td><td>NLP</td><td>멀티 에이전트 topology 대조 귀인 탐색임</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2610.29507'>Keeping Time vs. Understanding Time: Neither Alone Explains Temporal Reasoning in LLMs</a></td><td>40</td><td>0</td><td>NLP</td><td>시간 추론 두 모드 분해 가설을 검증하는 분석임</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2610.29602'>A Diagnostic Study of Faithfulness in Diffusion Language Models for Table-to-Text Generation</a></td><td>40</td><td>0</td><td>NLP</td><td>diffusion LM의 table-to-text faithfulness 진단 연구로 범위 좁고 로봇 무관</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2610.28855'>Speedrunning Relational Foundation Model Pretraining</a></td><td>40</td><td>0</td><td>LG</td><td>relational foundation model 사전학습 speedrun 리더보드로 로봇 무관</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2610.29046'>AutoFraming: Synthesizing Dynamic Frames of C Code with LLMs</a></td><td>40</td><td>0</td><td>NLP</td><td>C 코드 ACSL frame 명세를 LLM으로 합성, 로봇 무관</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2610.29680'>TraceForge: Distilling with Your Own Thinking</a></td><td>40</td><td>0</td><td>NLP</td><td>student 계열 스타일로 reasoning trace를 생성하는 증류, 로봇 무관</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2610.29822'>UserSWE: Evaluating Coding Agents in Multi-Turn Conversations with Dynamic Users</a></td><td>40</td><td>0</td><td>NLP</td><td>다중 턴 coding agent benchmark로 로봇 무관</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2610.29985'>TIDE: Tree-Induced Fine-Grained Diagnostic Evaluation from Model Behaviors</a></td><td>40</td><td>0</td><td>NLP</td><td>결정 트리 기반 LLM 능력 진단 평가로 로봇 무관</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2610.29356'>Payload generalization on feedforward control actions for trajectory tracking in robots with rigid and elastic joints</a></td><td>38</td><td>5</td><td>Control</td><td>payload 일반화 feedforward 제어로 고전 제어 중심임</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2610.29565'>Preserving Operator Intent Under Actuation Constraints: Teleoperation of Manipulators with Coupled Transmissions</a></td><td>38</td><td>5</td><td>Teleoperation</td><td>결합 전동 매니퓰레이터 텔레오퍼레이션 제어로 incremental임</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2610.28791'>VeriCalib: Verifiable Target-Based LiDAR-Camera Calibration</a></td><td>38</td><td>3</td><td>Calibration</td><td>LiDAR-카메라 보정 검증 가능성 제안이나 로봇 학습과 거리 있음</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2610.28974'>TEMPL: A Resource-Efficient and Transparent Model-Free Framework for Pseudo-Label Generation in Material CT Scans</a></td><td>38</td><td>1</td><td>CV</td><td>소재 CT용 임계값·영역 확장 기반 pseudo-label 생성은 실용적이나 고전적 처리 조합이라 novelty가 작고 로봇과 무관함</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2610.29176'>Multi-Scale Latent Temporal Compression Attention and Video-Text Cross Attention Fusion for Video Action Detection</a></td><td>38</td><td>1</td><td>Video</td><td>video action detection에 시간 압축 attention과 video-text cross attention module을 더한 구성이라 incremental하고 로봇 연결은 약함</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2610.29642'>OpenEarth-OVS44: A Multimodal Remote Sensing Dataset for Open-Vocabulary Segmentation</a></td><td>38</td><td>1</td><td>CV</td><td>위성·SAR 44클래스 open-vocabulary 분할 데이터셋과 3개 평가 트랙 공개가 기여이며 방법론 novelty가 없고 로봇 연결은 약함</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2610.28898'>Minimax-Optimal Predictive Flow Matching under Distribution Drift</a></td><td>38</td><td>1</td><td>Generative</td><td>distribution drift 하 flow matching 이론임</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2610.28899'>Data-Driven Glyph Positioning for Handwritten Music Synthesis</a></td><td>38</td><td>0</td><td>CV</td><td>필기 악보 합성의 glyph 위치를 경험 분포와 GNN으로 개선해 OMR 검출 mAP를 올린 좁은 도메인 응용이며 로봇과 무관함</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2610.29104'>From Canon to Nikon: Camera Domain Shift and Potential Equity Implications in Retinal AI</a></td><td>38</td><td>0</td><td>Medical</td><td>망막 카메라 기종에 따른 성능 차이를 frozen 모델로 측정한 평가 연구이고 새 방법이 없으며 로봇과 무관함</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2610.29141'>DGCM-SSFA: Dual-Granularity Cross-Modulation and Sparse Strip Frequency Attention for Efficient 3T-to-7T MRI Synthesis</a></td><td>38</td><td>0</td><td>Medical</td><td>3T에서 7T MRI를 합성하는 11M 파라미터 U-Net에 attention module 두 개를 얹은 구성이라 incremental하고 로봇과 무관함</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2610.29267'>Clinical radar heart sounds with echocardiographic phenotypes of ventricular dysfunction and valvular disease</a></td><td>38</td><td>0</td><td>Medical</td><td>레이더 심장음과 심초음파를 짝지은 환자 162명 데이터셋 공개가 기여이며 방법론 novelty가 없고 로봇과 무관함</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2610.29295'>Latent space configuration for neural network finetuning, fast ranking, and embedding dimensionality reduction</a></td><td>38</td><td>0</td><td>CV</td><td>embedding 검색용 latent space 구성임</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2610.29611'>Diff-IrisPAD: Modeling Bona Fide Iris Distributions for Unsupervised Presentation Attack Detection</a></td><td>38</td><td>0</td><td>CV</td><td>건강한 홍채 분포만 Brownian Bridge diffusion으로 학습해 복원 불일치로 공격을 탐지하나 ACER 30.52로 성능이 낮고 로봇과 무관함</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2610.29616'>An interpretable deep learning method for early hepatocellular carcinoma diagnosis on multiphase CT</a></td><td>38</td><td>0</td><td>Medical</td><td>신경망 예측과 수작업 영상 측정값을 logistic regression으로 합친 간암 진단 모델이며 LI-RADS 대비 정확도 비열등성 확인에 그치고 로봇과 무관함</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2610.29649'>MS2CAST: A Video Anomaly Detection Framework via Multi-Scale Spatial Cross-Attention and Efficient Spatiotemporal Networks</a></td><td>38</td><td>0</td><td>Video</td><td>ViT와 CNN 특징을 cross-attention으로 합치고 SwinLSTM 또는 VMRNN을 붙인 감시 영상 이상 탐지 구성이라 incremental하고 로봇과 무관함</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2610.29738'>Learning to Measure and Diagnose: A Clinical-Dictionary Radiomic Bottleneck Model for Thyroid Nodule Classification</a></td><td>38</td><td>0</td><td>Medical</td><td>갑상선 결절 분류에 radiomic 측정값 bottleneck을 둔 해석 가능 모델로 성능은 경쟁 수준에 그치고 의료 한정이며 로봇과 무관함</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2610.29746'>LEAF-Mamba: Feature Adaptation and Fusion for Whole Slide Image Analysis</a></td><td>38</td><td>0</td><td>Medical</td><td>WSI 분석에 reconstruction adapter와 Mamba-conv 병렬 gate를 얹은 MIL 모듈 조합이라 incremental하고 로봇과 무관함</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2610.28988'>Attention-based Classification for Indirect Prompt Injection</a></td><td>38</td><td>0</td><td>NLP</td><td>prompt injection 탐지 attention 분류, 로봇 무관함</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2610.29029'>Better Policies, Worse Verifier Audits</a></td><td>38</td><td>0</td><td>LG</td><td>verifier audit 제어 루프 이론, 로봇 무관함</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2610.29276'>Design and Tuning of Multi-Agent Systems Using Bayesian Evolutionary Optimization</a></td><td>38</td><td>0</td><td>NLP</td><td>multi-agent 시스템 topology 진화 탐색, LLM agent 중심임</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2610.29348'>Data Schedules and Learning Rate Schedules Should Be Designed Together</a></td><td>38</td><td>0</td><td>NLP</td><td>LLM data schedule과 LR schedule 공동 설계임</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2610.29411'>The Predictive--Optimization Gap in GuanDan Self-Play</a></td><td>38</td><td>0</td><td>RL</td><td>GuanDan self-play 예측 신호 대 최적화 격차임</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2610.29538'>Stochastic Pruning of the DPO Computation Graph: 1.4x Faster Training and Lower Peak Memory</a></td><td>38</td><td>0</td><td>NLP</td><td>DPO 계산 그래프 stochastic pruning 효율화임</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2610.29662'>SPARE: Sparsity Allocation via Routing Entropy for Efficient MoEs</a></td><td>38</td><td>0</td><td>LG</td><td>MoE sparsity 할당 pruning, efficient inference이나 로봇 무관함</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2610.30099'>Differentially Private Sparse Reward Estimation with Preference Feedback</a></td><td>38</td><td>0</td><td>LG</td><td>DP 환경 sparse reward 추정 이론은 RLHF 정렬 쪽이라 로봇과 무관함</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2610.28799'>Where Do Legal Factors Live in LLMs?</a></td><td>38</td><td>0</td><td>NLP</td><td>LLM 내 법적 요인 표현 위치 분석으로 로봇과 무관함</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2610.28957'>Scan or Index? large Evidence Coverage, Answer Quality, and Cost in Long-Document RAG</a></td><td>38</td><td>0</td><td>NLP</td><td>장문 RAG에서 scan과 index 비교 실증임</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2610.29328'>Seeing the Forest for the Trees: Emergent Agreement from Individual Conversations</a></td><td>38</td><td>0</td><td>NLP</td><td>LLM 간 대화에서 합의 수렴 현상 분석임</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2610.29657'>Effects of Model Scale and Quantization on Social Bias and Abstention in Question Answering</a></td><td>38</td><td>0</td><td>NLP</td><td>모델 크기·양자화가 BBQ 편향과 abstention에 미치는 영향 분석, 로봇 무관</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2610.29767'>ALIAS: Evaluating Performance and Memorization in LLM-Written TLA+ Specifications</a></td><td>38</td><td>0</td><td>NLP</td><td>TLA+ 명세 생성에서 identifier renaming 기반 memorization 검사의 한계 분석, 로봇 무관</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2610.29968'>CulturalRiddles: A Multicultural Benchmark of Riddles</a></td><td>38</td><td>0</td><td>NLP</td><td>62개 문화 수수께끼 benchmark로 dataset 기여이며 로봇 무관</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2610.37692'>Bouba Beats Kiki, and Other Regularities in the Subjective Preferences of LLMs</a></td><td>38</td><td>0</td><td>NLP</td><td>LLM 주관적 선호 규칙성 분석으로 로봇 무관</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2610.29036'>GRAIL: From Saliency to Semantics in Time-Series Explanation</a></td><td>38</td><td>0</td><td>LG</td><td>시계열 설명에 영역 기반 Owen value 사용, 로봇 무관</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2610.29092'>Same Answer, Different Reasons: Trace-Level Divergence in Multilingual Large Language Models</a></td><td>38</td><td>0</td><td>NLP</td><td>다국어 reasoning trace 구조 유사도 평가로 로봇 무관</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2610.29430'>MERP: A Latent-Bottleneck Framework for Robust Multi-Modal Multi-Label Emotion Recognition</a></td><td>38</td><td>0</td><td>Multimodal</td><td>missing modality 감정 인식 latent 병목, 개선폭이 0.004~0.005로 작음</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2610.29057'>Does Every Instance Count Equally? Order Effects in LLM Multi-Instance Processing</a></td><td>37</td><td>0</td><td>NLP</td><td>LLM multi-instance 처리의 순서 편향 분석으로 로봇 무관</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2610.29777'>Key Findings for Small UAS for Post-Disaster Damage Assessment from the CURSE&#x27;26 Exercise</a></td><td>36</td><td>3</td><td>CV</td><td>UAV 재난 평가 훈련 결과 보고, 연구 기여 약함</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2610.29825'>GuidedSAM-Plume: An Expert-Guided Segmentation Framework for Volcanic Plumes</a></td><td>36</td><td>1</td><td>CV</td><td>SAM2의 점·박스 prompt를 화산 연기 분할에 맞춰 쓴 상호작용 도구와 재주석 데이터 공개라 novelty가 작고 로봇 연결은 약함</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2610.29828'>Early versus Late RGB-Infrared Fusion for Counter-UAV Detection: A Comparative Study</a></td><td>36</td><td>1</td><td>CV</td><td>RGB-IR 융합 비교 연구, 새로움 적음</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2610.29283'>Computer Vision and Knowledge-Grounded Language Models for Intelligent Beekeeper Assistance</a></td><td>36</td><td>0</td><td>Multimodal</td><td>벌통 프레임 사진을 검출기와 지식베이스 기반 LLM 보고서로 잇는 양봉 도메인 파이프라인이며 평가가 빈약하고 로봇과 무관함</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2610.29905'>ViBMR: A Large-Scale Multi-Sequence Brain MRI Dataset and Comprehensive Evaluation for Vietnamese Radiology Report Generation</a></td><td>36</td><td>0</td><td>Medical</td><td>베트남어 뇌 MRI 보고서 데이터셋 공개와 baseline 평가가 기여이며 방법론 novelty가 없고 로봇과 무관함</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2610.28944'>Guilt by Association: Semantic Leakage Drives Associative Gender Bias</a></td><td>36</td><td>0</td><td>NLP</td><td>시맨틱 누출이 성별 편향을 일으키는 분석임</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2610.29843'>Every Part Has Its Role: Part-of-Speech Effects in LLM Post-Training</a></td><td>36</td><td>0</td><td>NLP</td><td>concept augmentation의 품사별 효과를 재현·확장한 소규모 분석임</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2610.29896'>Investigating the Impact of Learner Errors on Social Bias in Large Language Models</a></td><td>36</td><td>0</td><td>NLP</td><td>학습자 문법 오류가 LLM 편향을 키우는지 분석, 로봇 무관</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2610.30113'>Quant-Arena: Benchmarking LLM Agents for Quantitative Trading Research</a></td><td>36</td><td>0</td><td>NLP</td><td>퀀트 트레이딩 연구 benchmark로 로봇 무관</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2610.29217'>When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models</a></td><td>36</td><td>0</td><td>NLP</td><td>decision model 확률 배분 편향 분석으로 로봇 무관</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2610.29330'>AgentMonopoly: Behavioral Patterns and Persona Control in LLM Agents</a></td><td>36</td><td>0</td><td>NLP</td><td>모노폴리 게임에서 LLM agent 행동·persona 분석, 로봇 무관</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2610.30017'>GuideEvolve: Self-Evolving Agent Framework with Expert Guidance and 3Ts Mechanisms</a></td><td>36</td><td>0</td><td>NLP</td><td>self-evolving agent 프레임워크로 SOTA와 비슷한 수준이며 로봇 무관</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2610.29438'>A2I-Calib++: A Kinematics-Driven Anti-noise Active Calibration Framework for Whole-Body Multi-IMU Systems on Legged Robots</a></td><td>35</td><td>4</td><td>Calibration</td><td>다중 IMU 보정 프레임워크로 특수 센서 보정 중심임</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2610.29674'>From Acceptance and Avoidance to Affective Viscosity: Designing Social Agents Intermediating in Human Relationships</a></td><td>35</td><td>3</td><td>HRI</td><td>사회적 에이전트의 관계 중재 설계 논의로 개념 연구임</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2610.29008'>Enhancing Cross-Grade Generalization in Banana Variety Classification via Hybrid CNN-Transformers and Knowledge Self-Distillation</a></td><td>35</td><td>0</td><td>CV</td><td>바나나 품종 분류에 Swin-ResNet 하이브리드와 self-distillation을 쓴 농업 도메인 비교 연구로 novelty가 작고 로봇과 무관함</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2610.29045'>HumanCentric-Scenes-AI: A Human-Curated Multimodal Dataset of AI-Generated Human-Centric Scenes Across Surveillance, Occupational Portraits, AI-Edited Images, and Short-Form Video</a></td><td>35</td><td>0</td><td>CV</td><td>AI 생성 인물 이미지 296개의 소규모 데이터셋 공개가 기여의 전부이고 방법론 novelty와 로봇 연결이 없음</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2610.29407'>VideoGen Model 1: Prompt Expansion Versus Formatting in Audiovisual Generation</a></td><td>35</td><td>0</td><td>Generative</td><td>프롬프트 30개의 소규모 pilot에서 prompt expansion이 점수를 올렸다고 보고한 상용 모델 평가이며 일부 구간이 0을 포함해 불확실하고 로봇과 무관함</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2610.29495'>Balancing Foundation Models and Trait-Specific Learning for Forehead-Crease Recognition</a></td><td>35</td><td>0</td><td>CV</td><td>이마 주름 생체인식에서 MLLM zero-shot과 도메인 적응 모델을 비교한 평가이며 새 방법 기여가 작고 로봇과 무관함</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2610.28773'>Building a Nested LADDER for LLM Unstructured Post-Training Pruning</a></td><td>35</td><td>0</td><td>LG</td><td>LLM pruning sparsity 할당 개선, incremental임</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2610.28798'>An Explicit Feedback Contract for Iterative ML-Agent Harnesses</a></td><td>35</td><td>0</td><td>LG</td><td>ML agent 피드백 계약, 로봇 무관함</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2610.28871'>How Much Gradient Does Truncated Backprop Lose in Looped Transformers?</a></td><td>35</td><td>0</td><td>LG</td><td>looped transformer truncated backprop 분석, 로봇 무관함</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2610.28943'>Multi-Objective Protein Optimization via Modular Diffusion Steering</a></td><td>35</td><td>0</td><td>LG</td><td>단백질 다목적 최적화 diffusion steering, 로봇 무관함</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2610.28947'>Is 2:4 Sparsity Still Worth It? Semi-Structured Sparsity versus Quantization in LLM Inference</a></td><td>35</td><td>0</td><td>LG</td><td>2:4 sparsity와 quantization 비교 실험, 로봇 무관함</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2610.28997'>Rethinking Time Series Tokenization from a Frequency Perspective</a></td><td>35</td><td>0</td><td>LG</td><td>시계열 tokenization 주파수 관점, 로봇 무관함</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2610.29054'>Dynamics of Hidden Learning Structure</a></td><td>35</td><td>0</td><td>LG</td><td>학습 구조 dynamics 이론, 로봇 무관함</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2610.29063'>Distilling Multi-Teacher Scoring Principles for Unsupervised Time Series Anomaly Detection</a></td><td>35</td><td>0</td><td>LG</td><td>시계열 이상 탐지 multi-teacher 증류, 로봇 무관함</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2610.29340'>Reader--Writer Coupling in Transformer MLPs</a></td><td>35</td><td>0</td><td>LG</td><td>Transformer MLP reader-writer 분석, 로봇 무관함</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2610.29355'>GaP-MoE : Explicit Expert Specialization in Mixture-of-Experts via Orthogonal Gradient Accumulation and Projection</a></td><td>35</td><td>0</td><td>LG</td><td>MoE expert 특화 gradient projection, incremental임</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2610.29508'>Shortcut-Resistant CAM Distillation for Long-Tailed Recognition</a></td><td>35</td><td>0</td><td>CV</td><td>long-tailed 인식 CAM 증류, incremental임</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2610.29555'>WRDO: Weighted Refusal Direction Optimization in Aligned Language Models</a></td><td>35</td><td>0</td><td>NLP</td><td>LLM refusal direction 최적화, 로봇 무관함</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2610.29925'>Privacy in Context Is Being Overlooked in the Age of General-Purpose LLMs</a></td><td>35</td><td>0</td><td>NLP</td><td>LLM 맥락적 privacy 입장 논문임</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2610.30018'>ExGrad: Beyond Suppression - Explicit Clean-Gradient Subtraction in Adversarial Training</a></td><td>35</td><td>0</td><td>LG</td><td>adversarial training gradient 재구성, incremental임</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2610.28897'>Is Refusal Direction Universal across Low-Resourced Languages?</a></td><td>35</td><td>0</td><td>NLP</td><td>저자원 언어에서 refusal direction 보편성 재검증임</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2610.29225'>Beyond Binary Labels: Diagnostic Evaluation of LLM Safety with Prompt-Level Rubrics</a></td><td>35</td><td>0</td><td>NLP</td><td>프롬프트 수준 rubric LLM 안전성 진단 벤치마크임</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2610.29645'>LLMs as survey respondents: Comparison to simple semantic baselines</a></td><td>35</td><td>0</td><td>NLP</td><td>LLM 설문 응답 예측을 임베딩 baseline과 비교한 소규모 분석으로 로봇 무관</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2610.29785'>Where Do LLMs Learn to Recommend AI?</a></td><td>35</td><td>0</td><td>NLP</td><td>LLM의 AI 추천 편향 원인을 학습 단계별로 분석한 연구로 로봇 무관</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2610.28875'>To Manipulate or Not: Opinion Dynamics in LLM Interactions</a></td><td>35</td><td>0</td><td>NLP</td><td>LLM 간 토론 의견 변화 분석, 로봇 무관</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2610.29472'>OmniSimulator: Aligning Small Language Models for Authentic Heterogeneous Behavior Modeling</a></td><td>34</td><td>0</td><td>NLP</td><td>소형 모델 사용자 시뮬레이터 정렬임</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2610.29121'>Recursive Self-Improvement on a Budget: Scoring Code Edits Before They Run</a></td><td>34</td><td>0</td><td>NLP</td><td>coding agent scaffold 편집 선택 방법, 개선폭이 작고 서술이 불명확함</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2610.29294'>Same Probabilities, Different Advice: Gain-Loss Framing Effects in High-Stakes LLM Decision Support</a></td><td>34</td><td>0</td><td>NLP</td><td>gain-loss framing이 LLM 조언을 바꾸는 현상 분석, 로봇 무관</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2610.29812'>Real PMIDs, Wrong Papers: Harness Design for Biomedical Claim-Verification Agents</a></td><td>34</td><td>0</td><td>NLP</td><td>생의학 claim 검증 agent harness ablation 소규모 연구임</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2610.29961'>Commit or Abstain? System One Decision Models, LLMs, and Missing Legal Authority</a></td><td>34</td><td>0</td><td>NLP</td><td>법률 decision model의 abstention 평가로 로봇 무관</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2610.29461'>Linear Twisting Sidewinding Gaits for Twistable Snake Robot Motion Planning on Complex Terrains</a></td><td>33</td><td>3</td><td>Locomotion</td><td>뱀 로봇 sidewinding 보행 설계로 특수 하드웨어 응용임</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2610.29478'>S-Rolling: Steerable Rolling Gaits for Twistable Snake Robots in Low-Clearance Environments</a></td><td>33</td><td>3</td><td>Locomotion</td><td>뱀 로봇 rolling 보행 조향 설계로 틈새 분야 응용임</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2610.28836'>Sketch2Sim: an end-to-end modular framework for hand-drawn circuit analysis</a></td><td>33</td><td>1</td><td>CV</td><td>손그림 회로를 netlist로 바꾸는 YOLO 파이프라인으로 엔지니어링 중심임</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2610.28872'>LEAN: Loss-Engineered Modulation of the Model Weight-Sensitivity Distribution for Efficient, Error-Tolerant Neural Networks</a></td><td>33</td><td>0</td><td>LG</td><td>bit flip 내성 가중치 민감도 조절, 로봇 무관함</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2610.30119'>Self-normalized Bernstein Inequalities for Regenerative Processes and Applications to Learning Without Independence</a></td><td>33</td><td>0</td><td>LG</td><td>regenerative process 집중 부등식 이론이며 로봇 연결 거의 없음</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2610.29162'>Why is AI-generated language so hard to understand?</a></td><td>33</td><td>0</td><td>NLP</td><td>AI 생성 텍스트 이해 난이도의 심리언어학 분석임</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2610.29907'>Benchmarking Large Language Models for Detecting Satirical Code-Mixed Sentences</a></td><td>33</td><td>0</td><td>NLP</td><td>루마니아어 code-mixed 풍자 탐지 dataset·벤치마크, 로봇 무관</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2610.30045'>Which Differences Matter? Controlled Tests of Rule Transfer, Joint Reliability, and Information Use in Decision Models</a></td><td>33</td><td>0</td><td>NLP</td><td>decision model 규칙 전이 통제 실험으로 로봇 무관</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2610.29505'>Make it Walk: Computational Design of LEGO Walkers</a></td><td>32</td><td>3</td><td>Design</td><td>LEGO 보행체 계산적 설계로 로봇 학습 핵심과 거리 있음</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2610.29673'>Characterizing Oblivious Common-Reward Multi-Player Bandits: Universal Stationarity, Coordination Traps, and Certified Global Rates</a></td><td>32</td><td>1</td><td>RL</td><td>multi-player bandit 이론 분석임</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2610.28864'>A General Topological Symmetry Index for Critical Orbits In Neural Network Loss Landscapes</a></td><td>32</td><td>0</td><td>LG</td><td>loss landscape 대칭 지수, 이론 위주로 로봇 무관함</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2610.29313'>YingLan: A Multimodal Ocean Foundation Model for Unified Representation Learning from Heterogeneous Observations</a></td><td>32</td><td>0</td><td>LG</td><td>해양 multimodal foundation model, 로봇 무관함</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2610.29320'>BrainCodes: A Lightweight EEG Foundation Model over Discrete Neural Codes</a></td><td>32</td><td>0</td><td>LG</td><td>경량 EEG foundation model, 로봇 무관함</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2610.29504'>Rethinking Agentic Model Orchestration for Time Series Forecasting</a></td><td>32</td><td>0</td><td>LG</td><td>시계열 foundation model 오케스트레이션 분석, 로봇 무관함</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2610.28772'>Scaling Therapy Supervision: Assessing Psychotherapy Fidelity Using Large Language Models</a></td><td>32</td><td>0</td><td>NLP</td><td>심리치료 충실도 평가에 LLM을 쓰는 응용 연구임</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2610.29052'>Our Own Jev: Typed Decisions in One Forward Pass, from an In-House Judge to Open LoRA Models</a></td><td>32</td><td>0</td><td>NLP</td><td>단일 forward pass 유형 결정 judge 시스템 보고임</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2610.29165'>Carving Radiology Reports at Their Evidential Joints: Anatomical Region Sets as Generation Units</a></td><td>32</td><td>0</td><td>Multimodal</td><td>방사선 보고서 영역 단위 생성으로 의료 응용임</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2610.29223'>C$^2$U in RAG: Compositional Concept Unlearning in Retrieval-Augmented Generation</a></td><td>32</td><td>0</td><td>NLP</td><td>RAG 개념 unlearning 방법으로 로봇과 무관함</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2610.29326'>Signals and Queries: Token-Efficient Agentic Context Discovery</a></td><td>32</td><td>0</td><td>NLP</td><td>에이전트 정책 관련성 경량 필터로 엔지니어링임</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2610.29424'>A KAN-based Non-linear Factorization for Embedding Layer Compression</a></td><td>32</td><td>0</td><td>LG</td><td>KAN 기반 임베딩 압축으로 incremental임</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2610.30067'>GoiBERT: Compact Vietnamese Language Models via Two-Stage Knowledge Distillation</a></td><td>32</td><td>0</td><td>NLP</td><td>베트남어 compact encoder 지식 증류, 일반적 엔지니어링 수준임</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2610.28826'>Decision language models as affordable and rapid alternatives to LLM judges of clinical generative AI</a></td><td>32</td><td>0</td><td>LG</td><td>임상 평가용 decision LM 판정기 비교로 로봇 무관</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2610.29228'>From Scores to Safe Sets: Exact Safety--Constrained Decoding for Medication Recommendation</a></td><td>32</td><td>0</td><td>LG</td><td>약물 추천 제약 디코딩을 MILP로 푼 소규모 개선으로 로봇 무관</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2610.29570'>Joint-Angle Invariance of Jacobian-Based Performance Indices for Serial Robotic Manipulators</a></td><td>30</td><td>3</td><td>Kinematics</td><td>Jacobian 지표의 관절각 불변성 분석으로 순수 기구학 이론임</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2610.33081'>SWIFT-Cell: Segmentation Without Iterative Flow Tracking</a></td><td>30</td><td>0</td><td>CV</td><td>세포 segmentation 속도 개선, 로봇과 무관한 응용임</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2610.28797'>CALLIOPE: Private Insights into AI Use, Without Embeddings</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 대화 topic 계층 발견과 DP, 로봇 무관함</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2610.28878'>Actually, All Learnable Distribution Classes Are Privately Learnable</a></td><td>30</td><td>0</td><td>LG</td><td>분포 학습의 privacy 이론 결과, 로봇 무관함</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2610.28973'>From Weather to Enhanced Weathering: Weather Foundation Models for Carbon Dioxide Removal at Operational Scale</a></td><td>30</td><td>0</td><td>LG</td><td>weather foundation model의 탄소 제거 응용, 로봇 무관함</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2610.28998'>FlashNext-RL: A System Optimization Study for Long-Horizon Agentic RL of Qwen3.8-Flash-Next</a></td><td>30</td><td>0</td><td>RL</td><td>LLM agentic RL 시스템 최적화, 엔지니어링임</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2610.29049'>ART-MPG: Autoregressive R/T Manifold Path Guiding</a></td><td>30</td><td>0</td><td>CV</td><td>specular path guiding 렌더링 샘플링, 로봇 무관함</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2610.29067'>The Price of Choice in Selective Prediction</a></td><td>30</td><td>0</td><td>LG</td><td>selective prediction 검정 이론, 로봇 무관함</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2610.29311'>Interpretable Cutting Plane Selection for Mixed-Integer Linear Programming Using Genetic Programming</a></td><td>30</td><td>0</td><td>LG</td><td>MILP cut 선택 유전 프로그래밍, 로봇 무관함</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2610.29381'>Cascading Bandits with Noisy Observations: Algorithms and Regret Bounds</a></td><td>30</td><td>0</td><td>LG</td><td>cascading bandit 이론, 로봇 무관함</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2610.29425'>Generalization Bounds via Vector-Valued $L_p$ Correlation $V_α$</a></td><td>30</td><td>0</td><td>LG</td><td>generalization bound 이론, 로봇 무관함</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2610.29528'>Are Joint-Embedding Predictive Objectives Effective for Longitudinal EHRs?</a></td><td>30</td><td>0</td><td>LG</td><td>EHR JEPA 목적 효과 검토, 로봇 무관함</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2610.29531'>Phase Transitions in Learning Driven by Extremal Data</a></td><td>30</td><td>0</td><td>LG</td><td>max pooling MIL 상전이 이론, 로봇 무관함</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2610.29571'>Implicit Feature Reweighting for Label-Free Graph Generalization</a></td><td>30</td><td>0</td><td>LG</td><td>그래프 OOD 일반화 feature reweighting, 로봇 무관함</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2610.29577'>The Reflexivity Threshold: A Phase Transition for Multi-Agent Performative Prediction</a></td><td>30</td><td>0</td><td>LG</td><td>multi-agent performative prediction 상전이, 로봇 무관함</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2610.30104'>BatchBench: Benchmarking AI Robustness to Batch Effects and Domain Shift in Biomedical Images - A JUMP Cell Painting Leaderboard</a></td><td>30</td><td>0</td><td>CV</td><td>생체 이미지 batch effect 벤치마크로 기여가 데이터셋 중심임</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2610.29073'>A Large-Scale Evaluation of Role-Enhanced Zero-Shot Chain-of-Thought Prompting</a></td><td>30</td><td>0</td><td>NLP</td><td>역할 부여 CoT 프롬프팅 대규모 평가로 novelty 낮음</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2610.29171'>TrainBridge: Agentic NPU Training Optimization Guided by GPU Compilation Evidence</a></td><td>30</td><td>0</td><td>LG</td><td>NPU 학습 최적화 에이전트로 시스템 엔지니어링임</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2610.29350'>B-CARE: Blind Classwise Assessment of Relative Evidence for Stance Error Ranking</a></td><td>30</td><td>0</td><td>NLP</td><td>stance 오류 순위화 기법임</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2610.29455'>Omnilingual-MsASR: Benchmarking Multimodal, Multilingual, Long-Form Multi-Speaker ASR of Omni Large Language Models</a></td><td>30</td><td>0</td><td>Speech</td><td>omni LLM 다화자 ASR 벤치마크임</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2610.29606'>Overview of CHIP 2026 Shared Task 1: Patient-Specific Phenotype Concept Recognition in Full-Text Biomedical Literature</a></td><td>30</td><td>0</td><td>NLP</td><td>생의학 shared task 개요 논문으로 방법론적 novelty 없음</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2610.29926'>Task-Preserving Multilingual Instruction Tuning for Open-Ended QA in WMT 2026 MIST</a></td><td>30</td><td>0</td><td>NLP</td><td>WMT shared task 제출 기술문서로 LoRA fine-tuning 중심이라 기여 작음</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2610.29943'>Towards English - Mizo Legal Machine Translation: Corpus Creation, Analysis, and Benchmarks</a></td><td>30</td><td>0</td><td>NLP</td><td>영어-미조 법률 번역 코퍼스 구축, 로봇 무관</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2610.29023'>Inheritance as an Admission Test for LLM Prompt Merge Operators</a></td><td>30</td><td>0</td><td>NLP</td><td>prompt merge 연산자 admission test, 단일 과제·단일 모델 실험임</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2610.28918'>Query Feedback and Teaching for Stable and Certifiable Language Generation</a></td><td>28</td><td>0</td><td>NLP</td><td>language generation in the limit 이론, 로봇 무관함</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2610.28949'>Online Open-World Wafer Defect Discovery using Hyperdimensional Computing</a></td><td>28</td><td>0</td><td>LG</td><td>웨이퍼 결함 open-world 탐지, 로봇 무관함</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2610.28976'>SSMCGM-Stream: A Streaming State-Space Model for Personalized Diabetes Management</a></td><td>28</td><td>0</td><td>LG</td><td>혈당 예측 streaming SSM, 로봇 무관함</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2610.29009'>Local and Sparse Kernel Operator Learning for Incompressible Flows: An Operator Lagrange Formulation</a></td><td>28</td><td>0</td><td>LG</td><td>비압축 유동 kernel operator 학습, 로봇 무관함</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2610.29034'>Gate Initialisation versus Recurrent Dropout and Zoneout in Learning Long Dependencies: A Controlled Study of LSTM and GRU Networks on Synthetic Tasks</a></td><td>28</td><td>0</td><td>LG</td><td>LSTM/GRU 초기화 대 dropout 통제 실험, 로봇 무관함</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2610.29220'>Delay-Guided Attention for Quality Prediction in Multistage Manufacturing</a></td><td>28</td><td>0</td><td>LG</td><td>제조 품질 예측 attention, 로봇 무관함</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2610.29315'>DISRL: Dual-Scale Incremental Semi-Supervised Reinforcement Learning for Dynamic Community Tracking</a></td><td>28</td><td>0</td><td>LG</td><td>동적 community 추적 RL, 로봇 무관함</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2610.29391'>Nominate-then-Adjudicate: LLM-Assisted One-Pass and Per-Instance MIP Solver Tuning</a></td><td>28</td><td>0</td><td>LG</td><td>MIP solver 튜닝 LLM, 로봇 무관함</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2610.29416'>Alternative Strategies for Active Learning with Bayesian Bradley Terry Model</a></td><td>28</td><td>0</td><td>LG</td><td>Bayesian Bradley-Terry active learning, 로봇 무관함</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2610.29439'>How Far Can Foundation Models Be Distilled for Efficient Jet Tagging?</a></td><td>28</td><td>0</td><td>LG</td><td>jet tagging foundation model 증류, 로봇 무관함</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2610.29515'>BRIDGE: An Acceptance Gate to Block False Improvements in Model Updates, with a Retrospective Clinical Evaluation</a></td><td>28</td><td>0</td><td>LG</td><td>임상 모델 업데이트 acceptance gate, 로봇 무관함</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2610.29533'>Block Diffusion for Longitudinal EHR: Accuracy, Efficiency, and Representation Trade-offs</a></td><td>28</td><td>0</td><td>LG</td><td>EHR block diffusion, 로봇 무관함</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2610.29575'>Private Online Prediction from Experts with Small Losses</a></td><td>28</td><td>0</td><td>LG</td><td>private online prediction 이론, 로봇 무관함</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2610.29604'>Local and Global Recursive Ridge Regression for Online Residual Correction of Frozen Multivariate Forecasters under Label Delay</a></td><td>28</td><td>0</td><td>LG</td><td>시계열 예측 residual online 보정, 로봇 무관함</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2610.29667'>Leveraging Time-Series Foundation Models for Financial Crime Detection</a></td><td>28</td><td>0</td><td>LG</td><td>금융 범죄 탐지 시계열 foundation model, 로봇 무관함</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2610.29798'>Asymmetric Likelihood-Free Hypothesis Testing</a></td><td>28</td><td>0</td><td>LG</td><td>likelihood-free 가설 검정 이론, 로봇 무관함</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2610.29898'>A Sharp Dynamic Haussler Lemma</a></td><td>28</td><td>0</td><td>LG</td><td>dynamic Haussler lemma 이론, 로봇 무관함</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2610.29918'>Preventing Model Extraction in Contextual Linear Optimization</a></td><td>28</td><td>0</td><td>LG</td><td>contextual linear optimization 모델 추출 방지, 로봇 무관함</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2610.30075'>From Classifier Heads to Encoder Prototypes: Personalized Federated Learning with Head-Derived Clustering</a></td><td>28</td><td>0</td><td>LG</td><td>personalized FL head 기반 clustering, 로봇 무관함</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2610.28823'>A Parallel Multi-Dialect Arabic Dependency Treebank</a></td><td>28</td><td>0</td><td>NLP</td><td>아랍어 방언 의존 구문 treebank 자원 구축임</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2610.28840'>KIRA: A Full-Stack Reading Screening System with Dual-Pathway Analysis for Children</a></td><td>28</td><td>0</td><td>NLP</td><td>아동 읽기 선별 시스템으로 응용 중심임</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2610.29097'>Multi-level Encoder with Global Topic for Task-oriented Dialogue Summarization</a></td><td>28</td><td>0</td><td>NLP</td><td>대화 요약 인코더 개선으로 incremental임</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2610.29188'>LTEM: LLM-Friendly Table-Enhanced Markdown for Table Understanding and Generation</a></td><td>28</td><td>0</td><td>NLP</td><td>표 마크다운 표현 개선으로 incremental임</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2610.29319'>OSynth: A Longitudinal, Context-Sensitive Evaluation of Meeting Understanding</a></td><td>28</td><td>0</td><td>NLP</td><td>회의 이해 종단 평가 벤치마크임</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2610.29339'>ChronoSynth: Constraint-Aware Question Synthesis over Temporal Knowledge Graphs</a></td><td>28</td><td>0</td><td>NLP</td><td>시간 지식그래프 질문 생성으로 incremental임</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2610.29413'>Beyond Small Talk: Modeling Disclosure Trajectories in Human-AI Conversation</a></td><td>28</td><td>0</td><td>NLP</td><td>인간-AI 대화 자기 노출 궤적 모델링임</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2610.29122'>StochIKM: Automated High-Fidelity Reconstruction of Individual Patient Data from Published Kaplan-Meier Curves</a></td><td>28</td><td>0</td><td>LG</td><td>Kaplan-Meier 곡선에서 환자 데이터 복원, 로봇 무관</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2610.29594'>A Transfer Learning-Driven Methodology for Efficient and Sustainable Indoor Localization Using VLC</a></td><td>25</td><td>1</td><td>LG</td><td>VLC 실내 위치 추정 transfer learning, 응용 위주임</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2610.29638'>Cross-Area Transfer Learning for VLC-based Indoor Localization with a Transfer Efficiency Score</a></td><td>25</td><td>1</td><td>LG</td><td>VLC 실내 위치 추정 지역 간 전이, 응용 위주임</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2610.28784'>Extreme Low-State Quantized Transformer for Electricity-Load Forecasting</a></td><td>25</td><td>0</td><td>LG</td><td>전력 부하 예측용 양자화 Transformer, 로봇과 무관함</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2610.28933'>The Data Differentiator Framework (DDF): Quantifying Marginal Data Value with Information-Theoretic and Game-Theoretic Measures in an Agentic Evaluation Pipeline (SDSAE)</a></td><td>25</td><td>0</td><td>LG</td><td>기업 데이터 가치 평가 프레임워크, 로봇 무관함</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2610.28968'>Unit-Aware Differentially Private Quantum Machine Learning for Clinical and Wearable Health Data</a></td><td>25</td><td>0</td><td>LG</td><td>양자 ML DP 건강 데이터, 로봇 무관함</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2610.29114'>MHeatmap: Two-Walk Laplacian Reordering and Mosaic Layout for Rectangular Matrix Visualization</a></td><td>25</td><td>0</td><td>LG</td><td>행렬 heatmap 시각화, 로봇 무관함</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2610.29195'>Truncated Out-of-Bag Probability Gain: A Noise-Robust Criterion for Random-Forest Wrapper Feature Selection</a></td><td>25</td><td>0</td><td>LG</td><td>random forest 특징 선택, 로봇 무관함</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2610.29252'>Extending FAIR Principles with Observability for Trustworthy Federated Learning</a></td><td>25</td><td>0</td><td>LG</td><td>federated learning observability, 로봇 무관함</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2610.29362'>Compositional neural networks for multimodal X-ray and neutron scattering inversion</a></td><td>25</td><td>0</td><td>LG</td><td>X-ray 중성자 산란 역문제, 로봇 무관함</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2610.29589'>Fragment-Level Graph Encoding for Interpretable Molecular Property Prediction</a></td><td>25</td><td>0</td><td>LG</td><td>분자 fragment graph 인코딩, 로봇 무관함</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2610.29654'>Probabilistic Machine Learning for Short-Term Atmospheric Seeing Forecasting</a></td><td>25</td><td>0</td><td>LG</td><td>대기 seeing 확률 예측, 로봇 무관함</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2610.29725'>Structure-Aware Message Passing on Petri Nets through Directed Walks and Incidence Diffusion</a></td><td>25</td><td>0</td><td>LG</td><td>Petri net message passing, 로봇 무관함</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2610.29207'>norregel: a preregistered benchmark of dated numeric values in Norwegian law</a></td><td>25</td><td>0</td><td>NLP</td><td>노르웨이 법 수치 벤치마크로 데이터셋 기여임</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2610.29254'>Intergroup Bias Predicts Expressions of Social Judgment and Empathy in the r/AmITheAsshole Reddit Community</a></td><td>25</td><td>0</td><td>NLP</td><td>Reddit 집단 편향 분석으로 사회과학 성격임</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2610.29091'>Context-Augmented, Session-Calibrated Blood Pressure Tracking from Photoplethysmography</a></td><td>25</td><td>0</td><td>LG</td><td>PPG 혈압 추적 평가이며 개선폭이 작고 로봇 무관</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2610.29493'>An Exact 93-Move Solution to a Nonlocal Crystal-Exchange Puzzle</a></td><td>25</td><td>0</td><td>AI</td><td>퍼즐 한 개의 최단해 증명으로 기여 범위 좁고 로봇 무관</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2610.29556'>SOAR: Social and Opinion-Aware Recommendations</a></td><td>22</td><td>0</td><td>LG</td><td>소셜 추천 시스템, 로봇 무관함</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2610.29338'>Policy Central: Detecting Conflicts, Redundancy, and Similarity in Deployed Police Policy</a></td><td>22</td><td>0</td><td>NLP</td><td>경찰 정책 문서 충돌 탐지 시스템으로 응용임</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2610.29477'>TenetBench: A Clause-Anchored Russian Corpus for Evaluating Language Models against Professional Codes of Ethics</a></td><td>22</td><td>0</td><td>NLP</td><td>러시아 윤리 규약 벤치마크 코퍼스임</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2610.28912'>Simply Logical -- The First Three Decades</a></td><td>20</td><td>0</td><td>AI</td><td>Prolog 교재 변천사 회고로 연구 기여 없음</td></tr>
</tbody></table>

</details>
