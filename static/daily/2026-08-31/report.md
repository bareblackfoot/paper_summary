# 오늘의 arXiv Top 15: 2026-08-31 (월)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**

**신규 논문 수: 전체 308편 → 중복 제거 후 308편 (이번 평가 대상 293편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 77 |
| cs.LG | 67 |
| cs.RO | 28 |
| cs.CL | 51 |
| cs.AI | 85 |

---

## Top 15

### 1. Deciding If, When, and Where to Replan for Robust Manipulation (72점)

[arXiv](https://arxiv.org/abs/2608.28075) · [PDF](https://arxiv.org/pdf/2608.28075) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28075) · [프로젝트 페이지](https://narendhiranv04.github.io/ROBUST-TAMP/)

- **저자**: Narendhiran Vijayakumar, Puru Ojha, Nav Singhal, Girish Varma, Antony Thomas
- **분야**: TAMP · robotics relevance 10/10 · 1차 스크리닝 76점
- **읽은 원문**: PDF 전문

> 조작 도중 숨어 있던 물체가 새로 보일 때, 재계획이 필요한지와 수정 동작을 남은 계획의 어디에 넣을지를 따로 정하는 foundation model(FM) 기반 TAMP(task and motion planning) 틀을 만듦. MuJoCo 14개 변형에서 성공률 92.1%로, 가장 강한 baseline인 Inner Monologue의 45.0%보다 높음.

**무슨 문제인가**

foundation model(FM) 기반 TAMP(task and motion planning)는 계획 전에 장면 전체를 안다고 가정함. 그러나 긴 조작 과제에서는 뚜껑을 열거나 물체를 옮긴 뒤에야 과제와 관련된 물체가 보이는 일이 흔함. 이때는 실패한 동작이 없어도 남은 계획이 새 물체를 다루지 못할 수 있음. Inner Monologue처럼 실행 피드백으로 계획을 고치는 방법은 새 물체가 수정을 요구하는지, 수정 동작을 어디에 넣을지를 정해 주지 않음.

**어떻게 푸나**

Robust-TAMP는 실행 중 새 물체가 보이면 IF, WHEN, WHERE 세 가지를 차례로 정함. 입력은 언어 목표, 현재 보이는 물체와 영역, 지나간 관측을 담은 memory, 완료한 동작 기록, 남은 계획이고, 출력은 수정된 남은 계획임. IF 단계는 규칙으로 판정함: 남은 계획이 이미 다루는 물체는 넘기고, 목표를 아직 못 채운 관련 물체나 놓을 자리를 막는 무관한 물체만 FM 호출을 일으킴. WHEN 단계에서는 FM이 수정안을 만드는 동안 수정과 겹치지 않는 물체·영역의 동작만 계속 실행함. WHERE 단계에서 FM은 수정 동작 묶음마다 urgent 또는 deferred 표시와 넣을 위치를 내놓음. urgent 묶음은 남은 계획 맨 앞에, deferred 묶음은 지정한 동작 뒤나 끝에 들어가고, 기존 동작 순서는 그대로 유지됨. 수정안은 형식과 대상 물체를 검사해 통과하지 못하면 피드백과 함께 FM에 다시 물음.

**결과**

- MuJoCo 14개 변형(부엌: 식료품을 찬장에, 머그를 뚜껑 달린 상자에 넣기 / 그릴: 생고기를 구워 접시에 담기), 변형당 10회에서 Qwen3-VL-8B-Thinking planner 기준 성공률이 92.1%임. 같은 FM과 실행기를 쓴 Inner Monologue는 45.0%, EPoG는 28.6%, VLM-TAMP는 18.6%, OWL-TAMP는 14.3%임.
- in-context example 없이 비교해도 성공률이 68.6% 대 43.6%(Inner Monologue)임. in-context example을 준 조건에서 trial당 FM 호출은 Inner Monologue 15.0회에서 3.8회로, 전체 시간은 1,240초에서 449초로 줄어듦.
- ablation에서 수정 동작을 늘 계획 끝에 붙이면 부엌 성공률이 95.0%에서 52.5%로 내림. 그릴에서는 맨 앞 고정, 끝 고정 모두 86.7%에서 30.0%로 내림. memory를 빼면 그릴 성공률이 60.0%로 내림.
- IF를 빼고 새 물체마다 재계획하면 부엌 성공률은 95.0%로 같고 FM 호출이 4.2회에서 5.5회로 늚. WHEN을 쓰면 부엌 대기 시간이 127초에서 118초로 줄어 효과가 작음.

**한계**

정량 결과는 시뮬레이션뿐이고, 실로봇(UFACTORY xArm 7) 5개 설정은 시연 영상만 있고 성공률은 본문에서 확인 불가함. FM이 첫 시도에 urgency를 맞힌 비율은 58.8%이고, 실패를 겪은 trial 96개 중 85개는 검증과 재질의로 회복해 성공함. 동작이 pick·place·open·close 네 가지이고 물체·영역 이름이 미리 주어진 symbolic 장면을 가정함.

**누리랩 연구와의 연결**

- 동작 실패가 아니라 새 관측 때문에 계획이 틀어지는 경우를 다루므로 failure detection/recovery 연구에서 실패 정의를 넓히는 비교 대상이 됨.
- 지나간 관측을 memory에 남겨 수정 여부를 정하는 구조는 robot memory와 active perception을 TAMP와 묶는 실험의 출발점으로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 시뮬레이션 그릴 장면과 여러 시점의 물체·영역 지도가 구조화된 입력으로 FM planner에 들어가고, planner의 동작 순서가 검증기와 motion planning 실행을 거쳐 closed loop로 다시 관측되는 흐름을 보여 줌.*

---

### 2. ChainSplat: A Physics-Inspired Screw-Theoretic Model for Learning Deformable Linear Object Dynamics from Multi-View RGB Videos (68점)

[arXiv](https://arxiv.org/abs/2608.28570) · [PDF](https://arxiv.org/pdf/2608.28570) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28570) (요약 있음) · [프로젝트 페이지](https://chainsplat.github.io)

- **저자**: Seungyeon Kim, Noémie Jaquier
- **분야**: Manipulation · robotics relevance 8/10 · 1차 스크리닝 66점
- **학회**: IEEE 학술지 계열 양식 (추정) · 근거: IEEE 2단 양식, 18쪽
- **읽은 원문**: PDF 전문

> 케이블·로프 같은 변형 선형 물체를 revolute joint로 이은 강체 사슬로 보고, 다중 시점 RGB 영상만으로 형상·외형·운동학·동역학을 함께 학습함. 상태가 joint 각도 벡터 하나로 줄어 상태·힘 추정과 gradient 기반 궤적 최적화를 실로봇에서 보임.

**무슨 문제인가**

로봇이 케이블이나 로프를 다루려면 물체가 어떻게 움직일지 예측하는 dynamics model이 필요함. 신경망 dynamics model은 물리 법칙을 강제하지 않아 학습 때 보지 못한 로봇 동작에 약함. PhysTwin, PGND, EMPM 같은 물리 기반 digital twin은 2D point tracking, depth로 3D particle 만들기, Gaussian 구성을 차례로 거치는 다단계 pipeline임. depth가 빠른 움직임에서 noise가 커 오차가 쌓이고, 수많은 particle로 상태를 나타내므로 model-based control이 비쌈.

**어떻게 푸나**

ChainSplat은 DLO(deformable linear object: 케이블·로프·호스처럼 가늘고 긴 변형 물체)를 강체 link가 revolute joint로 이어진 open chain으로 나타냄. link 자세는 screw theory의 product-of-exponentials 공식으로 joint 각도에서 바로 계산되고, 상태는 joint 각도 벡터뿐임. 각 joint에는 spring·damper를, 각 link에는 질량·관성·바닥 마찰을 두고 recursive Newton-Euler 식으로 closed-form dynamics 식을 만듦. 로봇이 한쪽 끝을 계속 잡고 있다고 보고, chain의 base는 end-effector 궤적을 따라 움직임. 형상과 외형은 3D Gaussian이 맡고, Gaussian마다 어느 link에 붙는지 확률을 둠. 학습 1단계는 SAM으로 물체만 남긴 다중 시점 RGB 영상과 렌더링 영상의 차이를 줄여 Gaussian과 시점별 joint 각도를 함께 구함. 2단계는 이 joint 궤적을 simulation 궤적과 맞춰 질량·damping·마찰 같은 동역학 parameter를 구함.

**결과**

- 실험 절의 수치를 본문에서 확인할 수 없어 baseline 대비 결과는 본문에서 확인 불가함.
- 저자는 실제 DLO 실험에서 dynamics 예측, 3D 형상 복원, RGB 렌더링 모두 기존 방법보다 낫다고 주장함.
- 학습한 모델로 RGB 영상에서 joint 각도와 외력을 실시간으로 추정하고, 로봇 손 궤적을 gradient로 최적화해 로프 끝으로 목표 지점을 치는 실로봇 과제를 수행했다고 보고함. 성공률과 오차 값은 본문에서 확인 불가함.

**한계**

screw axis를 모두 같은 방향으로 고정하고 일정 간격으로 놓으므로, 변형이 거의 한 평면 안에서 일어나는 경우만 다룸. 로봇이 한쪽 끝을 계속 잡고 있어야 하고, 보정된 카메라 여러 대와 end-effector 자세가 필요함. 형상 단계와 동역학 단계를 따로 풀며, 길이가 다른 물체나 다른 상호작용으로 한 모델을 일반화하는 것은 저자도 향후 과제로 남김.

**누리랩 연구와의 연결**

- 3DGS를 link 단위로 묶어 물리 상태(joint 각도)에서 바로 렌더링하는 object-centric 표현임. 렌더링 차이로 상태를 추정하는 방식은 manipulation 중 world model 기반 상태 추적과 test-time 궤적 최적화에 바로 쓸 수 있음.
- 모델이 예측하지 못한 움직임에서 외력을 역산하는 기능은 접촉이나 외란을 찾는 failure detection 신호로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법의 기초가 되는 screw theory를 그린 개념도임. 왼쪽은 screw axis S를 중심으로 각도 θ만큼 돌 때 물체 자세 T가 exp([S]θ)·T로 바뀌는 모습이고, 오른쪽은 joint 세 개가 이어진 chain에서 끝 link 자세가 지수 함수의 곱으로 정해지는 과정임.*

---

### 3. DeicticVLA: Unifying Instruction Modes Based on Language and Deictic Gestures in a Single VLA (66점)

[arXiv](https://arxiv.org/abs/2608.28108) · [PDF](https://arxiv.org/pdf/2608.28108) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28108) (요약 있음)

- **저자**: Kango Yanagida, Tatsuya Aoki, Yuichiro Yoshikawa, Takato Horii
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 66점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 12쪽
- **읽은 원문**: PDF 전문

> 말만 쓰는 지시, 말과 클릭을 함께 쓰는 지시, 클릭만 쓰는 지시를 같은 text prompt와 mask 형식으로 바꿔 π0 하나가 세 방식을 모두 따르게 함. 실로봇에서 학습 때 없던 범주의 인형을 옮기는 과제는 클릭을 쓰면 12회 모두 성공했고, 말만 쓰면 2회 성공함.

**무슨 문제인가**

VLA는 자연어로 과제를 받지만, 같은 범주이거나 생김새가 비슷한 물체가 여럿 있으면 대상을 하나로 집어 내는 긴 표현이 필요함. 게다가 VLA는 공간 관계나 서수 표현을 제대로 쓰지 못하고 학습 데이터의 시각적 편향을 따라 대상을 고르는 경우가 보고됨. 손가락으로 가리키는 지시를 쓰는 기존 연구는 말과 가리키기를 함께 쓰는 방식이나 가리키기만 쓰는 방식 중 하나만 다룸. 또한 가리킨 영역을 VLA에 어떻게 넣을지는 연구마다 backbone과 데이터가 달라 공정하게 비교된 적이 없음.

**어떻게 푸나**

DeicticVLA는 사용자 입력을 세 방식으로 받음: 말만 쓰는 LI(Language Instruction), 말과 클릭을 함께 쓰는 VLI(Vision-Language Instruction), 클릭만 쓰는 VI(Visual Instruction). 사용자가 로봇 카메라 화면에서 물체를 클릭하면 SAM 2가 그 물체의 mask를 만들고 조작 중에도 따라가며 갱신함(deictic mask). mask는 옮길 물체, 놓을 곳, 공간 표현의 기준 물체라는 세 역할로 나뉨. 세 방식은 모두 text prompt와 mask 묶음으로 바뀌며, VI의 text prompt는 과제 내용이 없는 고정 문구 "follow visual instruction"이고 LI의 mask는 전부 0임. mask를 π0에 넣는 방법으로 네 가지를 비교함: RGB 영상에 빨간 상자를 그리는 VP-BBox, mask 밖을 회색으로 흐리게 하는 VP-Fade, mask embedding을 visual encoder 앞에 더하는 MP-Early, 뒤에 더하는 MP-Late. 학습은 두 단계로 함: 먼저 LI 데이터로 과제를 익히고, 이어서 LI·VLI·VI 데이터를 함께 학습함.

**결과**

- LIBERO(시뮬레이션 조작 과제 모음)에서 물체 배치를 섞은 평가 suite Object-ZS로 mask를 켰을 때와 껐을 때 성공률 차이를 잼. 총 60k step을 맞춘 조건에서 VP-BBox의 차이는 두 단계 학습에서 VLI 29.2, VI 27.8퍼센트포인트였고 한 단계 학습에서 0.9, 1.0퍼센트포인트로 내려감.
- 두 번째 단계에서 LI 데이터를 빼면 VLI·VI 성공률은 95.4~97.0%로 유지되지만 LI 성공률은 63.6~72.1%로 내림. LI 데이터를 넣은 두 단계 학습의 LI 성공률은 91.5~94.0%임.
- 실제 UR5e에서 MP-Late로 과제 3개를 학습함(총 360 episode). 학습 때 없던 표현으로 블록을 고르는 PickBlock TL3(학습에 없던 색·공간·서수 표현을 쓰는 조건)에서 성공률은 VI 93.8%, VLI 68.8%, LI 18.8%임(각 16회).
- 학습 때 없던 범주의 인형을 바구니에 넣는 조건에서 VLI와 VI는 12회 모두 성공함. 함께 학습한 LI는 16.7%, LI만 학습한 baseline은 33.3%임.

**한계**

시뮬레이션에서는 정답 segmentation mask를 썼고, 실로봇에서 SAM 2의 분할·추적 오류가 성능에 주는 영향은 따로 재지 않음. 실로봇에서는 MP-Late만 평가해 prompting 방법 간 비교가 없음. 실로봇에서 함께 학습한 LI 성능은 LI만 학습한 baseline보다 낮았음(학습 때 쓴 표현으로 지시하는 PickBlock TL1에서 70.8%에서 29.2%로 내림). 사용자의 설명 부담이 실제로 줄어드는지는 사용자 실험으로 확인하지 않음.

**누리랩 연구와의 연결**

- VLA에 클릭 기반 mask를 조건으로 넣는 방법 네 가지를 같은 backbone과 같은 step 수로 비교한 결과임. object-centric 조건이나 scene graph에서 고른 물체를 VLA에 넘기는 연구에서 입력 방식을 고를 때 참고가 됨.
- 대상 지정 실패와 동작 실패를 나눌 수 있는 구조여서, failure recovery에서 사람이 클릭으로 대상을 고쳐 주는 multi-turn 교정 실험의 출발점으로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 위쪽은 LI·VLI·VI 입력이 SAM 2를 거쳐 text prompt와 deictic mask로 바뀌어 DeicticVLA에 들어가는 흐름이고, 아래쪽은 VP-BBox, VP-Fade, MP-Early, MP-Late 네 입력 방식을 보여 줌.*

---

### 4. STEGNav: Spatio-Temporal Event Graph Reasoning for Multimodal Lifelong Object Navigation (66점)

[arXiv](https://arxiv.org/abs/2608.28279) · [PDF](https://arxiv.org/pdf/2608.28279) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28279)

- **저자**: Yang Chen, Zhenyu Huang, Wenbo Fu, Danyang Peng, Shi-Yu Tian, Kun-Yang Yu, Lan-Zhe Guo
- **분야**: Navigation · robotics relevance 9/10 · 1차 스크리닝 68점
- **읽은 원문**: PDF 전문

> 여러 목표를 차례로 찾는 실내 navigation에서 scene graph에 질의별 instance 구분, 탐색 frontier, 최근 궤적과 예전 성공 기록을 함께 담아 VLM이 다음 목표를 고르게 함. 학습 없이 GOAT-Bench(여러 목표를 한 episode에서 차례로 찾는 benchmark) 성공률 66.3%로 비교 방법 중 가장 높음.

**무슨 문제인가**

multimodal lifelong navigation은 한 episode 안에서 물체 이름, 언어 설명, 참조 이미지로 주어지는 목표를 차례로 찾아가는 과제임. 기존 zero-shot 방법은 관측한 물체를 scene graph에 쌓고 목표와 같은 category의 node만 골라 VLM에 넘김. 이 방식은 같은 category의 여러 물체 중 설명이나 이미지에 맞는 하나를 가려내지 못함. 또 frontier(탐색된 공간과 미탐색 공간의 경계)가 graph와 따로 주어지고, 지나온 경로와 앞 subtask에서 찾은 물체를 기억하지 않아 같은 곳을 다시 탐색함.

**어떻게 푸나**

STEGNav(Spatio-Temporal Event Graph Navigation)는 학습 없이 RGB-D 관측과 pose로 scene graph와 occupancy map을 만들고, 이를 두 방향으로 확장한 graph를 VLM에 넣음. 공간 쪽에서는 VLM이 후보 물체마다 질의와의 관련도 점수와 짧은 설명을 매기고, 언어·이미지 질의면 상위 5개만 남김. 같은 graph에 frontier node를 넣고, 각 node에 도달 가능 여부, geodesic 경로 비용, 탐색 이득(주변 미탐색 면적)을 붙여 물체와 frontier를 한 표현에서 비교하게 함. 시간 쪽에서는 짧은 창이 현재 subtask에서 내린 최근 20개 결정과 실행 궤적을 기록함. 긴 창은 VLM 검증과 거리 조건을 통과한 예전 subtask 성공을 최대 8개 남기고, 지금 graph의 node와 CLIP 외형 유사도로 다시 연결함. VLM(gpt-5.4-mini)은 이 graph를 글로 펼친 입력을 보고 다음 목표로 물체 node나 frontier node 하나를 출력함.

**결과**

- GOAT-Bench(물체·언어·이미지 목표를 한 episode에서 5~10개 차례로 찾는 Habitat 과제) Val-Unseen 전체에서 성공률(SR)이 66.3%임. 가장 강한 학습 없는 방법 MSGNav의 62.4%보다 3.9퍼센트포인트 높음.
- 같은 조건에서 SR과 경로 효율(SPL)을 모두 보고한 EvoMemNav와 비교하면 SR은 59.6%에서 66.3%로, SPL은 38.9에서 39.7로 오름.
- 36개 episode 부분집합의 누적 ablation에서 기본 3D scene graph의 SR 55.8%가 instance grounding 추가 후 59.4%, frontier grounding 추가 후 66.9%, 두 창 memory 추가 후 70.9%로 오름.
- HM3D ObjectNav(물체 category 6종 찾기)에서 데이터셋 버전 v1, v2의 SR은 각각 64.0%, 69.4%로 가장 높음. SPL은 v1 29.8, v2 28.2로 EvoMemNav의 33.6, 39.4보다 낮음.

**한계**

모든 실험은 Habitat 시뮬레이션이며 실로봇 결과와 코드 주소는 본문에 없음. ablation과 실패 분석은 각 scene의 첫 episode 36개로만 했고, temperature 0.95로 한 번씩 돌린 결과라 반복 실행 편차는 보고하지 않음. 실패 분석에서 실행·정지 실패는 기본 3D scene graph의 18건에서 14건으로만 줄어 저수준 제어 문제는 남아 있음.

**누리랩 연구와의 연결**

- 예전 subtask의 검증된 성공만 골라 저장하고 지금 graph에 다시 연결하는 긴 창은 robot memory와 scene graph 연구에서 비교 대상으로 쓸 수 있음.
- 물체 node와 frontier node를 같은 graph에서 경로 비용·탐색 이득으로 고르게 한 구성은 active perception에서 다음 관측 위치를 고르는 문제와 이어짐.

*대표 그림: 측정 결과가 아니라 기존 state-centric scene graph의 문제를 그린 개념도임. 집 평면도 위에 같은 곳을 맴도는 반복 탐색, 이미 찾은 물체를 잊는 문제, 같은 category 의자 둘을 구분 못하는 문제, 물체 graph와 frontier(F1, F2)가 따로 노는 문제를 공간축·시간축에 나눠 표시함.*

---

### 5. Contact-Guided Exploration for Non-Prehensile Locomanipulation with Multi-Critic RL (66점)

[arXiv](https://arxiv.org/abs/2608.28140) · [PDF](https://arxiv.org/pdf/2608.28140) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28140) (요약 있음) · [프로젝트 페이지](https://tolomeis.github.io/contact-guided-exp/)

- **저자**: Simone Tolomei, Mayank Mittal, Franco Angelini, Manolo Garabini, Paolo Salaris, Marco Hutter
- **분야**: RL · robotics relevance 9/10 · 1차 스크리닝 64점
- **학회**: RA-L 채택 · 근거: comments에 "project website: https://tolomeis.github.io/contact-guided-exp Accepted in IEEE Robotics and Automation Letter (RA-L) 8 pages, 9 figures"
- **읽은 원문**: PDF 전문

> 사족 보행 로봇에 달린 팔이 의자를 잡지 않고 밀거나 걸어 당겨 목표 위치로 옮기는 policy를 RL로 학습함. 접촉 지점 쪽으로 끌어 주는 탐색 reward를 별도 critic에 맡기고 그 가중치를 학습 중에 줄여, 시뮬레이션 의자 운반 성공률 94.1%를 얻음.

**무슨 문제인가**

의자나 상자처럼 무겁고 큰 물체는 집어 들기 어려워 밀기·당기기 같은 non-prehensile manipulation이 필요함. 이 접촉은 한쪽으로만 힘이 걸리고 마찰에 기대므로 dynamics가 불연속이고, MPC 같은 model-based 방법은 단순화한 모델과 정확한 mesh가 필요함. model-free RL은 로봇이 물체에 제대로 닿아 힘을 줘야만 task reward를 받으므로 reward가 희소함. 보행 로봇은 자유도가 많아 이 문제가 더 커지고, 에너지 penalty만 받는 쪽으로 물체를 아예 건드리지 않는 local minimum에 빠지기 쉬움.

**어떻게 푸나**

상위 policy는 팔 관절 목표값, 몸통 SE(2) 속도, 몸통 높이를 내고, 미리 학습한 보행 policy가 이를 다리 관절 목표로 바꿈. actor는 proprioception과 물체의 위치·자세·목표 오차를 입력으로 받음. 물체 mesh에 기존 grasping 알고리즘을 돌려 접촉 후보점 25개를 뽑고, episode마다 하나를 골라 end-effector가 그 점에 가까워질수록 탐색 reward를 줌. reward는 task, 탐색, regularization 세 묶음으로 나누고 PPO critic이 묶음마다 value head를 따로 둠(multi-critic). policy 갱신에는 세 head의 advantage를 가중합해 쓰며, 학습 5k에서 10k step 사이에 탐색 가중치를 0.1에서 0.01로 줄이고 regularization 가중치를 0.15에서 0.24로 올림. 그래서 초반에는 접촉을 찾는 데 집중하고, 후반에는 탐색 목표 대신 물체를 넘어뜨리지 않고 옮기는 쪽에 집중함.

**결과**

- 시뮬레이션 의자 운반(IKEA 의자 15개와 절차 생성 의자 100개로 학습)에서 제안 방법의 성공률은 94.1%, 물체 넘어짐 비율은 4.4%임. 5개 seed 평균이고, 성공은 물체가 목표 0.2m 안에 들어온 경우임.
- 단일 critic PPO는 물체에 닿지 못한 비율이 9.1%이고, 같은 가중치 schedule을 reward 항에 직접 건 PPO + WS는 4.0%임. 탐색 reward를 아예 빼면 성공률이 0%임. baseline별 성공률 수치는 그래프로만 제시돼 본문에서 확인 불가함.
- 실제 ALMA 사족 로봇에서 학습에 없던 IKEA 가구 4종으로 58회 시도해 40회 성공함(69.0%). 주력 의자 ADDE는 72.9%, SANDSBERG는 57.1%이며, 물체 자세는 외부 motion capture로 받음.
- 식기세척기 문 열기 과제에서는 손잡이를 당긴 뒤 문짝을 미는 쪽으로 접촉을 바꾸는 행동이 나옴. 팔 관절이 한계의 10% 안에 머문 시간 비율이 단순 PPO보다 59% 줄었음.

**한계**

실로봇 실험은 의자 운반 한 과제이고, 물체 자세를 외부 motion capture에 기대므로 현장 배치는 보이지 않음. 시뮬레이션 94.1%에서 실로봇 57~73%로 성공률이 낮아지며, 저자는 옆으로 접근할 때의 급한 회전이 state estimation 오차를 키우는 것을 주원인으로 꼽음. 가중치 schedule은 의자 과제에서 손으로 맞춘 값이고, 접촉 후보점을 만들려면 물체 mesh가 있어야 함.

**누리랩 연구와의 연결**

- grasping 알고리즘이 낸 object-centric 접촉 후보를 RL 탐색 prior로 쓰는 방식은, manipulation policy 학습에서 희소 reward를 다루는 단순한 기준선으로 쓸 수 있음.
- 접촉이 빗나가면 몸통을 다시 놓고 팔을 더 크게 휘두르는 회복 행동이 학습으로 나왔다고 보고함. failure recovery를 따로 설계하지 않은 policy의 사례로 참고할 만하지만 정량 분석은 없음.

*대표 그림: 사족 로봇에 달린 팔이 의자 다리에 고리를 걸어 빨간 원판 목표로 끄는 실제 장면임. 왼쪽 큰 그림에는 의자 다리의 접촉 후보점 몇 개와 end-effector가 각 점으로 가는 점선 경로가 겹쳐 그려져 있고, 오른쪽에는 접이식 의자와 다리 세 개짜리 탁자를 끄는 장면이 있음.*

---

### 6. RoboPhys-3D: A Comprehensive Embodied World Model Evaluation via 3D Reconstruction (64점)

[arXiv](https://arxiv.org/abs/2608.28718) · [PDF](https://arxiv.org/pdf/2608.28718) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28718)

- **저자**: Tianyi Wang, Jiazhou Chen, Yiming Xu, Xiangyu Li, Tianyi Zeng, Chih-Hsien Chou, Ning Lu, Liang Peng 외 2명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 66점
- **읽은 원문**: PDF 전문

> 로봇 조작용 video world model이 만든 영상을 정답 영상과 같은 3D 복원 과정에 넣고, inverse dynamics model로 행동을 뽑아 시뮬레이터에서 실행해 보는 평가 benchmark RoboPhys-3D를 만듦. 과제 성공과 상관이 높은 지표 8개의 평균인 RoboPhyscore는 사람 평가와 Pearson 상관 0.9761을 보임.

**무슨 문제인가**

Video world model은 로봇 학습에서 데이터 생성기, 행동 계획기, 시뮬레이터로 쓰이지만, 생성된 영상이 실제 장면의 3D 상태를 지키는지는 보장되지 않음. 기존 영상 생성 benchmark는 화질과 그럴듯함을 생성 프레임만 보고 재므로, 정답 3D 상태와 맞는지나 영상 속 동작을 로봇이 실행할 수 있는지는 재지 않음. 3D 일관성을 재는 WBench도 생성 영상 내부의 자기 일관성만 보고 기준 장면과 비교하지 않음. 또 3D 복원 자체의 오차와 생성 모델의 오차가 섞여 있어, 3D 지표가 낮을 때 어느 쪽 탓인지 가를 수 없었음.

**어떻게 푸나**

RoboTwin 2.0(양팔 로봇 조작 시뮬레이터)의 50개 과제를 한 팔/두 팔, 목표 위치 있음/없음의 네 갈래로 나누고, 과제당 100 episode를 카메라 5대로 녹화함. Qwen3-VL이 정답 영상을 보고 집게 방향과 궤적을 적은 시점별 설명문을 만들고, 사람이 잘못된 설명을 걸러냄. 평가할 world model은 첫 프레임과 설명문을 받아 이후 프레임을 생성함. 생성 영상과 정답 영상을 똑같이 네 가지 3D 복원 방법(VGGT, VGGT-Ω, 4DGS, 4C4D)에 넣어, 정답 영상의 복원 오차로 복원 자체의 오차를 따로 잼. 이어서 IDM(inverse dynamics model, 영상에서 로봇 행동을 추정하는 모델)인 DreamGen이 생성 영상을 행동 열로 바꾸고, 이 행동을 시뮬레이터에서 실행해 과제 성공을 확인함. 생성 영상을 합성 데이터로 써서 π0.5 policy를 학습시킨 성공률도 과제 성공 측정에 넣음. 지표는 픽셀 품질, 3D 기하 일관성, 물체 위치와 궤적 같은 상태 일치, 과제 완수의 4단계로 나뉘고, 18개 하위 항목에 걸쳐 모두 50개임. AFS(Average Full Score)는 50개 지표를 단계별로 균등 평균한 값이고, RoboPhyscore는 세 가지 과제 성공 측정과 모두 Pearson 상관 0.70을 넘는 지표 8개의 평균임.

**결과**

- RoboPhyscore(1점 만점)에서 Cosmos 3가 0.6330으로 가장 높고, 같은 과정을 거친 정답 영상 0.6829의 92.7%임. Wan 2.2는 0.5359, RoboDreamer는 0.3492, CogVideoX 1.5는 0.3363임.
- 겉보기 판정과 실행 결과가 어긋남. Wan은 VLM이 과제 완수로 판정한 점수가 평균 0.9185인데, 추정 행동을 시뮬레이터에서 실행한 성공률 지표는 0.4010임. CogVideoX는 충돌 안전 점수가 0.9650으로 정답 영상 0.9385보다 높지만 과제 성공 점수는 정답 영상의 16.5%임.
- 복원 방법만 바꿔도 점수가 바뀜. 정답 영상 기준 대비 RoboPhyscore 유지율이 VGGT-Ω는 96.1%, 4DGS는 78.2%임. Cosmos의 과제 성공 점수(3점 만점)는 복원 없이 2.3275, 4DGS 복원 뒤 1.7000으로 27.0% 내림.
- 평가자 70명이 10점 척도로 매긴 점수와 RoboPhyscore의 상관은 Pearson 0.9761, Spearman 0.8962임. 실험은 모두 시뮬레이션이며 실로봇 실험은 없음.

**한계**

시뮬레이터 하나(RoboTwin 2.0)와 로봇 형태 하나에서만 만든 benchmark이고, 평가한 world model도 4개뿐임. RoboPhyscore의 지표 8개는 같은 4개 모델의 결과에서 과제 성공과의 상관으로 골랐으므로, 새 모델에도 같은 상관이 유지되는지는 보이지 않음. 사람 평가에 쓴 영상 표본 수와 코드·데이터 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- world model을 planner나 데이터 생성기로 쓸 때, 화질이나 VLM 판정 대신 IDM으로 행동을 뽑아 실행해 보는 평가 방식을 world model 연구의 검증 절차로 가져올 수 있음.
- VLM 판정은 높은데 물체 위치와 궤적이 틀리는 사례가 정리돼 있어, world model rollout의 failure detection 지표를 고를 때 근거로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 benchmark 전체 구성을 그린 개요도임. 위쪽은 RoboTwin 2.0 과제 네 갈래, Qwen3-VL 설명문 생성, 3D 복원 네 가지, world model 네 개를 보여 주고, 아래쪽은 DreamGen과 π0.5로 행동을 실행하는 과정과 4단계 18개 하위 항목 50개 지표를 보여 줌.*

---

### 7. PHR-VLA: Planning Horizon Reasoning for Vision-Language-Action Models (62점)

[arXiv](https://arxiv.org/abs/2608.27609) · [PDF](https://arxiv.org/pdf/2608.27609) · [alphaXiv](https://www.alphaxiv.org/abs/2608.27609) (요약 있음) · [프로젝트 페이지](https://davoodsz.github.io/PHR-VLA.github.io/)

- **저자**: Davood Soleymanzadeh, Kaidi Zhang, Zhiyuan Zhang, Bihao Zhang, Xiao Liang, Yu She, Minghui Zheng
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 68점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 8쪽
- **읽은 원문**: PDF 전문

> VLA를 fine-tuning할 때 앞으로 H step 동안 장면 feature가 어떻게 바뀌는지 맞히는 보조 head를 붙여 학습시키고, 배포 때는 그 head를 뺌. 실제 분해 과제 4개의 평균 성공률이 SmolVLA의 63.3%에서 82.5%로 오름.

**무슨 문제인가**

대부분의 VLA는 현재 관측만 보고 action chunk를 내므로, 장면이 앞으로 어떻게 바뀔지를 따로 표현하지 않음. 이 점은 접촉이 많고 미세한 조정이 필요한 조작에서 약점이 됨. 관측 history를 길게 넣는 memory 방식은 입력이 길어져 추론 지연이 늘어남. 미래 이미지나 subgoal을 먼저 만들어 쓰는 forecasting·world model 방식은 추론 때 생성 단계가 추가되어 실시간 제어에 부담이 됨.

**어떻게 푸나**

PHR-VLA(Planning Horizon Reasoning VLA)는 SmolVLA(0.45B)를 base로 하고, 학습 때만 쓰는 future head를 하나 붙임. demonstration에는 현재 시점 이후 H개 frame이 있으므로, 이를 고정된 vision encoder(SigLIP 또는 V-JEPA 2)에 넣어 frame별 latent를 얻음. 연속한 두 frame latent의 차이를 latent dynamics로 정의하고 이를 학습 target으로 씀. future head는 VLM backbone이 내는 action-token representation을 입력으로 받아 이 latent dynamics를 예측함. 전체 loss는 원래 VLA loss에 예측 latent dynamics와 target 사이의 MSE를 가중치 λ로 더한 것임. 추론 때는 future head와 encoder를 버리므로 입력과 출력, 계산량은 SmolVLA와 같음.

**결과**

- LIBERO(언어 지시 탁상 조작 benchmark, suite 4개)에서 wrist camera의 patch 단위 latent dynamics로 감독했을 때 평균 성공률이 SmolVLA의 84.1%에서 88.4%로 오름. 오름폭은 긴 과제 묶음인 LIBERO-Long에서 66.0%에서 74.4%로 가장 큼.
- 같은 설정에서 target을 바꾼 ablation 결과, latent 차이 대신 미래 latent 자체를 맞히면 86.7%, patch 대신 평균 pooling한 latent를 맞히면 86.2%임. target을 뽑는 camera를 wrist, third-person, 둘 다로 바꾼 세 설정 모두 patch 단위가 평균 pooling보다 높음.
- Meta-World(다양한 단일 조작 과제 모음, third-person camera만 있음)에서는 평균 성공률이 56.7%에서 57.8%로 1.1퍼센트포인트 오르는 데 그침. Very Hard 등급은 46.7%에서 45.3%로 내림.
- 실제 Franka 로봇의 분해 과제 4개(과제당 demonstration 100개, 평가 30회)에서 성공 횟수가 SmolVLA 76/120에서 99/120으로 오름. 비틀어 빼는 Task IV에서 6/30에서 23/30으로 차이가 가장 큼.

**한계**

base model은 SmolVLA 하나뿐이고, 비교 대상에 미래 예측을 보조 loss로 쓰는 다른 VLA 방법은 없음. LIBERO 표의 일부 baseline 수치는 다른 논문에서 가져온 것이라 학습 조건이 다름. 실험은 한 번씩 돌린 결과로 보이며 분산은 본문에서 확인 불가함. 저자도 학습 때 표현만 바꿀 뿐 추론 때 plan을 고치거나 실패를 바로잡지는 않는다고 밝힘. 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- world model을 추론 때 돌리지 않고 학습 때 VLA 표현에 미래 정보를 넣는 쪽을 택한 사례임. test-time planning이나 world model 기반 VLA 연구에서 추가 추론 비용이 없는 비교 기준으로 쓸 수 있음.
- wrist camera의 patch 단위 장면 변화가 가장 효과적이었다는 결과는, 접촉 중심 manipulation에서 failure detection용 예측 target을 고를 때 참고가 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 왼쪽 학습 단계에서는 t부터 t+H까지의 frame을 고정 vision encoder에 넣고 차이를 구해 future head의 target으로 쓰고, action head는 따로 L_VLA로 학습됨. 오른쪽 추론 단계에는 VLM backbone과 action head만 남고, 아래에 LIBERO 과제 수행 frame이 이어져 있음.*

---

### 8. CEDAR: Automata as Verifiable Interfaces for Language-Guided Embodied Action (60점)

[arXiv](https://arxiv.org/abs/2608.27797) · [PDF](https://arxiv.org/pdf/2608.27797) · [alphaXiv](https://www.alphaxiv.org/abs/2608.27797)

- **저자**: Lekai Chen, Alvaro Velasquez, Ashutosh Trivedi
- **분야**: Embodied AI · robotics relevance 7/10 · 1차 스크리닝 58점
- **학회**: ACL 계열 양식 (추정) · 근거: A4 용지, 2단 구성
- **읽은 원문**: PDF 전문

> 자연어 지시의 skill과 지속 제약을 모두 DFA(결정적 유한 오토마타)로 배우고, 둘을 교집합으로 합쳐 제약을 실행 내내 지키게 함. Minecraft의 "밤에는 자면서 다이아몬드 모으기" 과제에서 목표와 제약을 함께 달성한 시행이 5회 중 5회였고, code 생성 baseline 4종은 모두 0회였음.

**무슨 문제인가**

사용자 지시에는 목표뿐 아니라 실행 내내 지켜야 할 제약이 섞여 있음. "다이아몬드를 모으되 밤에는 자라", "이 biome 안에서만 탐험하라" 같은 것임. VOYAGER처럼 LLM이 code를 생성하는 agent는 이런 제약을 한 번 처리할 subgoal로 다루기 쉬움. 그 결과 오래 도는 skill이 밤이 된 뒤에도 계속 실행됨. 또 skill이 자유 형식 program이라 새 제약과 형식적으로 합칠 수 없고, 실패 궤적을 근거로 고치기도 어려움.

**어떻게 푸나**

CEDAR는 지시를 환경 event 궤적 위의 regular language로 바꾸고, skill과 제약을 각각 DFA로 학습함. 먼저 simulator API에 구현된 기호 1,429개(행동 16개, event predicate 9개, 물체 1,404개)에서 embedding 검색과 LLM 가지치기로 과제용 alphabet을 고름. 다음으로 active DFA learning 알고리즘 CAPAL이 "이 궤적이 지시에 맞는가"라는 membership query를 LLM에게 묻고 DFA 가설을 만듦. 가설 DFA는 accepting state까지의 최단 경로를 따라 실행되고, 결과가 의도와 어긋나면 그 궤적을 counterexample로 돌려 DFA를 다시 학습함. 제약 DFA는 사람이 준 counterexample도 씀. 배운 skill DFA와 제약 DFA를 product intersection으로 합치면 두 언어를 모두 만족하는 궤적만 받는 controller가 됨. 동사가 같고 물체만 다른 새 과제는 저장된 DFA의 물체 기호를 바꿔 재사용함.

**결과**

- "다이아몬드 곡괭이를 만들고 다이아몬드를 계속 모으되 밤에는 자라" 과제(시행 5회)에서 목표와 제약을 함께 달성한 시행이 CEDAR는 5회임. VOYAGER와 CodeAct(LLM이 Python code를 행동으로 내는 agent)는 runtime assertion을 붙인 경우까지 4종 모두 0회임. 평균 체력도 CEDAR 18.4, 가장 높은 baseline(assertion 붙인 CodeAct) 12.0임.
- "광물은 밤에만 캐라" 과제에서 24,000 tick 동안 모은 물체 수가 VOYAGER 229개에서 CEDAR 387개로 늘어남. 다만 핵심 지표인 낮 시간 채굴 비율의 수치는 본문 표에서 확인 불가하고 그림으로만 제시됨.
- "다이아몬드 찾기" 단계 순서에서 마지막 단계까지의 누적 LLM query 수가 VOYAGER 75회, CEDAR 37회임. 첫 단계(통나무)에서는 CEDAR가 18회로 VOYAGER의 4회보다 많이 쓰지만, 이후 skill 재사용으로 역전함.
- skill library를 쓴 다이아몬드 곡괭이 과제 성공은 25회 중 CEDAR 23회, VOYAGER 17회임. 실로봇 실험은 없고, iTHOR(가정 환경 시뮬레이터) 5개 과제는 비교 없이 파이프라인이 돈다는 것만 보임.

**한계**

비교 실험은 모두 Minecraft이고 시행 수가 5회 수준이라 저자도 통계 검정 없는 서술적 비교로만 해석함. 제약 DFA 학습에는 저자 1명이 준 human counterexample(4~8개)이 쓰였고, 필요한 predicate가 API에 없거나 alphabet에서 빠지면 지시 일부가 조용히 무시될 수 있음. raw 영상 입력이나 연속 제어에서는 시험하지 않았음.

**누리랩 연구와의 연결**

- 실행 궤적의 counterexample로 DFA를 다시 배우는 고리는 failure detection·recovery를 형식 언어 수준에서 다루는 사례임. VLA 위에 언어 제약 monitor를 얹는 연구에서 비교 대상으로 쓸 수 있음.
- 학습된 skill을 DFA로 저장해 재사용하고 제약과 합성하는 구조는 robot memory와 long-horizon skill chaining 연구와 이어짐. 다만 기호화된 simulator 상태를 전제로 해 실로봇 지각과의 연결은 직접 보이지 않음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 자연어 지시가 DFA Learner로 들어가 alphabet 선택과 LLM membership query로 DFA를 만들고, Skill Library와 Specification Library의 DFA가 교집합으로 합쳐져 제약된 DFA가 되는 흐름을 보임. Minecraft 환경의 실행 궤적이 counterexample로 학습기에 되돌아가는 경로도 그려져 있음.*

---

### 9. Video Generative Models as Geometry Learner (60점)

[arXiv](https://arxiv.org/abs/2608.28549) · [PDF](https://arxiv.org/pdf/2608.28549) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28549) (요약 있음) · [프로젝트 페이지](https://happy-hsy.github.io/projects/GeoNeXt/)

- **저자**: Haosen Yang, Jifei Song, Zhensong Zhang, Xiatian Zhu, Jiankang Deng
- **분야**: 3D Vision · robotics relevance 6/10 · 1차 스크리닝 62점
- **읽은 원문**: PDF 전문

> 사전학습된 video 생성 모델에 depth map과 surface normal map을 입력 사진 다음 frame으로 생성하게 가르쳐, 모델 하나로 두 geometry를 함께 추정함. 59K 합성 데이터로 학습해 KITTI depth AbsRel을 208K로 학습한 GeoWizard의 14.4에서 8.2로 낮춤.

**무슨 문제인가**

사진 한 장에서 depth와 surface normal을 추정할 때, 최근에는 Stable Diffusion 같은 image diffusion 모델을 fine-tuning해 geometry를 생성하는 방식이 적은 label로도 잘 됨. 그런데 Marigold처럼 depth와 normal을 따로 학습하면 모델이 두 개 필요하고 두 geometry 사이의 관계를 쓰지 못함. GeoWizard처럼 한 모델이 둘을 같이 내게 하려면 attention 구조를 바꿔야 하고, 사전학습과 멀어진 만큼 학습 데이터가 더 많이 듦.

**어떻게 푸나**

GeoNeXt는 image-to-video 생성 모델인 Stable Video Diffusion(SVD)을 그대로 가져와 geometry 추정에 씀. 입력 RGB 사진, depth map, normal map 세 장을 짧은 video의 frame 세 개로 보고, 사진 뒤에 오는 frame으로 depth와 normal을 생성하게 함. 세 장은 고정된 Stable Diffusion VAE로 latent로 바뀌고, 사진 latent를 복제해 각 frame의 noise latent 옆에 붙여 조건으로 줌. U-Net은 geometry만이 아니라 입력 사진도 함께 다시 생성하도록 세 latent 모두에 diffusion loss를 받음. 학습은 U-Net만 하고, 사진 크기를 바꿔야 하는 CLIP cross-attention 조건은 geometry를 왜곡한다는 이유로 끔. 추론 때는 noise에서 세 frame을 함께 denoising한 뒤 사진 latent는 버리고 depth와 normal만 decoding함.

**결과**

- 학습에 쓰지 않은 실제 데이터셋 KITTI(실외 주행 장면)의 affine-invariant depth 오차(AbsRel, 낮을수록 좋음)가 GeoNeXt 8.2, GeoWizard 14.4임. 학습 데이터는 59K 대 208K이고 GeoWizard는 저자가 다시 돌린 값임.
- 같은 59K 규모로 depth와 normal을 각각 따로 학습한 Lotus-G(image diffusion 기반 geometry 추정 모델)와 비교하면 KITTI AbsRel 8.5 대 8.2, NYUv2(실내 장면 benchmark) 5.4 대 5.3으로 차이가 작음. normal 오차는 NYUv2에서 Lotus-G 16.6, GeoNeXt 16.7로 GeoNeXt가 모든 benchmark에서 이기지는 않음.
- 입력 사진을 다시 생성하는 부분을 빼면 NYUv2 depth AbsRel이 5.3에서 6.5로, iBims-1(실내 고해상도 장면 benchmark) normal 평균 각도 오차가 16.4에서 18.5로 나빠짐. depth만 또는 normal만 학습한 별도 모델도 같은 지표에서 함께 학습한 모델보다 나쁨.
- 62.6M장으로 학습한 Depth Anything V2와 비교하면 ETH3D(실내외 고해상도 장면 benchmark) AbsRel은 GeoNeXt 5.6 대 13.1로 GeoNeXt가 낮음. 반면 NYUv2는 5.3 대 4.5, KITTI는 8.2 대 7.4로 Depth Anything V2가 낮음.

**한계**

평가는 depth와 normal 지표뿐이고 metric scale depth는 다루지 않음. video prior와 temporal attention이 성능의 원인이라는 주장은 SVD를 image diffusion 모델로 바꾼 비교가 없어 실험으로 따로 확인되지 않음. 기본 설정은 5 step에 5회 ensemble이라 NVIDIA A5000 GPU에서 depth와 normal을 함께 내는 데 10.0초가 걸리고, 1 step 단일 추론은 1.0초임.

**누리랩 연구와의 연결**

- 사진 한 장에서 depth와 normal을 함께 내는 모델이라 manipulation용 장면 기하 입력이나 object-centric 3DGS 초기화에 쓸 수 있음. 다만 로봇 실험은 없고 추론 시간이 길어 실시간 제어에는 바로 쓰기 어려움.
- video 생성 모델의 frame 축을 다른 modality 출력 칸으로 쓰는 방식은, video 기반 world model이 미래 관측과 함께 geometry를 내게 하는 설계에 참고가 됨.

*대표 그림: 측정 결과가 아니라 GeoNeXt 학습 구조를 그린 그림임. 사진, depth, normal을 고정된 VAE로 latent로 바꾸고 noise를 더해 사진 latent와 이어 붙인 뒤, 학습되는 U-Net이 세 latent를 모두 복원하도록 세 항을 더한 loss로 학습하는 흐름을 보임.*

---

### 10. Post-Training VLMs for Video Mistake Detection (60점)

[arXiv](https://arxiv.org/abs/2608.28406) · [PDF](https://arxiv.org/pdf/2608.28406) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28406) · [코드](https://github.com/FedeSpu/mstk)

- **저자**: Federico Spurio, Olga Zatsarynna, Lars Doorenbos, Emad Bahrami, Gianpiero Francesca, Juergen Gall
- **분야**: Video · robotics relevance 5/10 · 1차 스크리닝 58점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> 요리 영상의 한 단계가 지시문대로 수행됐는지 VLM이 YES/NO로 답하게 하고, 같은 단계의 정상·실수 영상에 다른 답을 내면 reward를 더 주는 방식으로 post-training함. 학습에 없던 요리에 대해 EP-VQA(1인칭 요리 실수 영상 benchmark)의 실수 검출 F1이 일반 GRPO의 43.0에서 48.0으로 오름.

**무슨 문제인가**

기존 영상 실수 검출 방법은 대부분 closed-set임. 학습과 테스트에서 같은 동작 단계를 가정하므로, 과제가 바뀌면 데이터를 새로 모으고 다시 학습해야 함. open-set을 다룬 유일한 선행 연구(CaptainCook4D)는 20분이 넘는 긴 영상에서 단계 위치 찾기와 실수 판별을 zero-shot VLM에 한꺼번에 맡겨 성능이 낮았음. 저자는 특정 단계를 외우는 대신 지시문과 실제 수행이 어긋나는지를 보는 일반적인 실수 개념을 배워야 한다고 봄.

**어떻게 푸나**

먼저 MD-VQA(Mistake Detection VQA) 프로토콜을 만듦. 입력은 한 단계에 해당하는 짧은 영상 clip과 그 단계의 지시문이고, 출력은 실수가 있으면 YES, 없으면 NO임. 모델은 답 앞에 chain-of-thought로 근거를 먼저 씀. CaptainCook4D와 EgoPER(1인칭 요리 실수 데이터셋)를 이 형식으로 고쳐 CC-VQA와 EP-VQA를 만들고, 학습에 없던 요리를 unseen test로 따로 뗌. 모델은 Qwen2.5-VL-7B이고, SFT 단계 없이 GRPO로 바로 post-training함. reward는 형식 reward, 정답 reward, 새로 제안한 opposite reward의 합임. opposite reward는 같은 지시문의 반대 영상(정상이면 실수 영상, 실수면 정상 영상)을 하나 뽑아 두 답이 다르면 줌. 단, 원래 질문의 답이 맞았을 때만 주며 가중치는 0.2임.

**결과**

- 학습에 없던 요리로 이뤄진 EP-VQA unseen split에서 실수 검출 F1이 48.0임. opposite reward 없는 GRPO는 43.0, reasoning prompt를 준 GPT-4o-mini는 29.0, SFT는 4.7임.
- CC-VQA unseen split에서는 F1 35.5로 SFT 34.5, GRPO 32.6보다 높음. 학습에 나온 요리의 seen split에서는 GRPO(30.9)보다 낮은 29.7임.
- opposite reward에서 정답 조건을 빼면 EP-VQA F1이 seen 53.8에서 50.3, unseen 48.0에서 43.6으로 내림. chain-of-thought 없이 opposite reward만 쓰면 거의 모든 clip을 실수로 답해 recall 100%, precision 8~10%가 됨.
- 부록에서 Qwen3-VL-8B로 바꿔도 EP-VQA unseen F1이 GRPO 45.5에서 52.4로 오름. 실험은 요리 영상 두 데이터셋에서만 했고, 코드와 benchmark는 공개됨.

**한계**

가장 좋은 결과도 precision이 40% 안팎이라 실수로 판정한 clip의 절반 이상이 오탐임. unseen split도 학습 데이터와 같은 데이터셋·같은 요리 도메인에서 나온 것이어서, 다른 작업이나 촬영 조건으로 일반화되는지는 보이지 않음. clip 하나만 보므로 순서 바뀜이나 단계 누락처럼 앞뒤 단계에 걸친 실수는 다루지 않음.

**누리랩 연구와의 연결**

- 지시문과 실행 영상이 어긋나는지를 VLM으로 판정하는 구조는 VLA 실행 중 단계별 failure detection 모듈에 그대로 옮겨 볼 수 있음. 정상·실패 쌍에 다른 답을 요구하는 opposite reward는 로봇 성공·실패 rollout 쌍으로 detector를 학습할 때 비교 대상이 됨.
- 다만 사람 요리 영상만 다루고 실로봇 실험은 없어서, 로봇 조작 실패에 적용하려면 데이터를 새로 구성해야 함.

*대표 그림: 같은 질문 형식으로, 학습에 나온 요리(오트밀 4큰술 계량)와 학습에 없던 요리(토르티야에 Nutella 바르기)의 영상 프레임을 보여 주는 예시 그림임. 두 경우 모두 Zero-Shot, SFT, GRPO는 NO로 답하고 제안 방법만 YES로 실수를 찾음.*

---

### 11. AcrossVAM1.0: Particle World Modeling for Text-Assisted Robot Video Prediction (58점)

[arXiv](https://arxiv.org/abs/2608.28491) · [PDF](https://arxiv.org/pdf/2608.28491) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28491) (요약 있음)

- **저자**: Yafei Zhang, Nan Wu
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 72점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> 로봇 영상 예측을 로봇·팔·그리퍼 3개 particle의 움직임 예측과 마지막 프레임 기반 외형 복원으로 나눔. 0.28M parameter dynamics 모델이 마지막 프레임 복사 대비 궤적 오차를 21.0% 줄였지만, 영상 화질 향상 폭은 작고 언어 지시의 영향도 약함.

**무슨 문제인가**

실제 로봇 영상은 대부분의 픽셀이 멈춰 있고, 동작은 팔과 그리퍼 같은 작은 부분에서만 일어남. 그래서 마지막 관측 프레임을 그대로 복사하는 baseline(persistence)도 영상 전체의 PSNR·SSIM에서 높은 점수를 받음. 프레임 전체를 dense latent로 압축하는 world model은 움직임과 질감을 한 latent에 섞어 배우므로, 움직임을 실제로 배웠는지 확인하기 어려움. 언어 조건을 넣어도 예측 궤적이 지시문에 따라 달라지는지는 따로 검증해야 함.

**어떻게 푸나**

AcrossVAM1.0은 과거 4프레임과 지시문을 받아 다음 5프레임을 128×128 해상도로 예측함. 먼저 고정된 SAM3-DLP codec(분할 mask를 써서 프레임을 particle로 바꾸는 사전학습 encoder)이 RGB와 부위 마스크를 받아 프레임마다 로봇 전체·팔·그리퍼에 해당하는 particle 3개와 배경 latent를 뽑음. particle 하나는 위치, 크기, 깊이, 존재 여부, 외형 code로 이루어짐. 2층짜리 spatio-temporal Transformer가 particle의 위치·크기·깊이·존재 여부를 한 step씩 자기회귀로 예측함. 지시문은 고정된 OpenCLIP text encoder로 embedding한 뒤 FiLM(feature 단위 scale·shift 조절)으로 이 Transformer에만 넣음. 예측된 particle은 고정된 renderer가 대략적인 RGB와 alpha map으로 그리고, 마지막 관측 프레임에서 뽑은 외형 feature와 residual refiner가 세부 질감을 채움. 마지막으로 학습된 mask가 픽셀마다 생성 결과와 마지막 프레임 복사 중 어느 쪽을 쓸지 섞음.

**결과**

- VRS(DROID 계열 실로봇 영상에 로봇·팔·그리퍼 마스크와 지시문을 붙인 benchmark) 368개 test window에서 particle dynamics의 궤적 오차가 persistence보다 21.0% 낮음. seed 3개 범위는 20.6~21.4%임.
- 92개 clip, 460 frame의 미래 영상 예측에서 PSNR이 persistence 19.97에서 20.573으로, SSIM이 0.796에서 0.8004로 오름. LPIPS는 0.1304로 persistence의 0.122보다 나쁨. seed 3개는 mask 학습만 바꾼 것이고 앞단 모델은 공유함.
- 움직이는 영역만 잰 PSNR은 persistence 11.89에서 mask 없이 생성한 결과 13.23으로 오름. mask를 쓰면 12.870으로 내려감. 픽셀마다 정답 쪽을 고르는 oracle은 전체 프레임 PSNR이 22.12로 최종 모델(20.573)보다 1.55dB 높음.
- 올바른 지시문 대신 다른 clip의 지시문을 넣으면 궤적 오차가 2.8~3.1%만 늘어남. 저자가 세운 10% 목표에 못 미쳐서 저자 스스로 instruction-controlled가 아니라 text-assisted라고 부름.

**한계**

FitVid, SlotFormer, TextOCVP 같은 공개 baseline은 같은 조건으로 재학습하지 않아 직접 비교 수치가 없고, 재현 진행 상황만 표로 정리함. 로봇별 궤적 오차는 persistence 대비 Franka에서 21.1% 줄었지만 Mobile ALOHA에서 16.1%, Google Robot에서 5.2% 늘어남. 5프레임·128×128 예측만 했고, 부위 마스크가 필요하며, policy나 planning에 써서 실제 제어를 평가하지는 않음.

**누리랩 연구와의 연결**

- 로봇 부위를 particle로 둔 world model이라 예측 실패가 팔인지 그리퍼인지 부위 단위로 볼 수 있음. world model 기반 failure detection에서 부위별 예측 오차를 신호로 쓰는 실험의 출발점이 됨.
- 마지막 프레임 복사 baseline, 지시문 섞기 control, oracle을 함께 보고하는 평가 방식은 우리 world model·VLA 영상 예측 실험의 평가 설계에 그대로 가져다 쓸 수 있음.

*대표 그림: 실제 로봇이 빨간 그릇 옆 물체로 팔을 뻗는 장면의 미래 5 step을 위에서부터 정답, 제안 방법, mask 없는 생성, 마지막 프레임 복사, 학습된 mask 순서로 배치한 그림임. 제안 방법과 mask 없는 생성 결과 모두 팔 부분이 흐릿하게 번지고, mask는 팔이 있는 영역만 노랗게 표시함.*

---

### 12. A Probabilistic Interpretation of KV Cache Eviction (56점)

[arXiv](https://arxiv.org/abs/2608.28293) · [PDF](https://arxiv.org/pdf/2608.28293) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28293) (요약 있음)

- **저자**: Renato Geh, Alex Chen, Daniel Israel, Aditya Grover, Guy Van den Broeck
- **분야**: Efficient LLM · robotics relevance 2/10 · 1차 스크리닝 56점
- **학회**: NeurIPS 양식 (추정) · 근거: 1단 구성, 1쪽 꼬리말 'Preprint.'
- **읽은 원문**: PDF 전문

> KV cache eviction을 attention 기대값 추정 문제로 다시 정의하고, 남길 항목을 sampling으로 고른 뒤 decode 때 importance sampling으로 보정함. Llama3.2-3B와 Qwen3-4B에서 기존 top-k 방법과 비슷한 점수를 내면서 과제별 순위가 더 고르게 유지됨.

**무슨 문제인가**

KV cache eviction은 prompt의 key·value 항목 일부를 지워 메모리와 계산을 줄이는 방법임. 기존 방법(H2O, SnapKV, StreamingLLM 등)은 attention 점수나 위치로 점수를 매겨 상위 k개만 남기는 heuristic이고, 문제 자체는 형식적으로 정의된 적이 없음. 항목을 지운 뒤 남은 항목만으로 softmax를 다시 계산하면 정규화 상수가 바뀌어 attention 값이 왜곡됨. 이 왜곡은 다음 layer와 이후 생성 token으로 전파되지만 기존 연구는 이를 보정하지 않았음.

**어떻게 푸나**

먼저 저자는 정해진 압축률에서 attention 출력 오차를 허용치 안에 두는 항목 집합을 찾는 문제가 NP-complete임을 PARTITION 문제로부터의 환원으로 증명함. 다음으로 attention을 항목 위치에 대한 categorical 분포 아래에서 value의 기대값을 구하는 계산으로 해석함. eviction 시점에 proposal 분포 π에서 위치를 m번 복원 추출하고, 한 번 이상 뽑힌 항목만 남기며 뽑힌 횟수를 저장함. decode 시점에는 남은 옛 항목에 (뽑힌 횟수 / (m × π))를 가중치로 곱해 옛 prompt 부분의 기대값과 정규화 상수를 추정함. 이를 eviction 이후 생성된 token들의 정확한 값과 합쳐 다시 정규화함(self-normalized importance sampling). π가 모든 항목을 덮으면 m이 커질수록 참값으로 수렴하고, 유한한 m에서의 bias와 오차는 O(1/m)로 묶임. 기존 top-k 방법은 이 틀에서 분산은 0이지만 bias에 상한이 없는 추정기로 해석되고, 그 점수를 정규화하면 proposal로 바로 쓸 수 있음. 저자는 추정 분산을 최소로 하는 proposal도 유도하고, 지난 시점들을 harmonic prior로 가중한 변형을 πmin-h라 부름.

**결과**

- Llama3.2-3B에서 prompt 하나의 첫 응답 token에 대한 attention 평균 절대 오차를 압축률별로 잼. 낮은 압축률부터 중간 압축률까지는 H2O 점수를 정규화해 proposal로 쓰고 importance sampling으로 보정한 probabilistic H2O의 오차가 낮음. 압축률이 아주 높아 sample 수가 적으면 분산이 커져 보정하지 않은 쪽보다 오차가 커짐.
- Llama3.2-3B와 Qwen3-4B를 LongBench(긴 문서 QA 묶음, HotpotQA·QASPER·TriviaQA 중 3,000 token 미만 예제)와 RULER(긴 문맥 검색·추적 과제 묶음, 130개 예제)에서 평가함. 평균 점수는 기존 top-k 방법 5개와 비슷하거나 높다고 보고하지만 정확한 수치는 그래프로만 제시되어 본문에서 확인 불가임.
- 예제별 순위를 과제마다 정규화해 평균한 win score에서는 harmonic prior를 둔 최소분산 proposal(πmin-h)이 두 모델과 두 benchmark 모두에서 가장 위에 있음. 기존 방법은 과제에 따라 순위가 뒤집힘: Llama3.2-3B에서 StreamingLLM은 QuestionAnswer 과제 1위, MultiKey-NIAH(긴 문맥에서 여러 key 중 맞는 값을 찾는 과제) 꼴찌임.

**한계**

실험은 3B~4B 모델 2개와 benchmark 일부 예제로 한정됨. eviction의 원래 목적인 throughput이나 latency는 측정하지 않았고, head마다 압축률이 달라지는 구현은 효율적인 sparse tensor 구현을 전제로 함. 중요도 가중치의 온도를 높여 분산을 줄이는 실험에서는 대부분의 경우 bias 증가가 더 컸음.

**누리랩 연구와의 연결**

- 직접 연결 약함. 긴 관측 기록을 KV cache로 들고 가는 VLA나 robot memory에서 cache를 줄일 때, top-k 대신 sampling과 보정을 쓰는 방법으로 참고할 수 있음.

---

### 13. Stay Seated: Learning Omnidirectional Humanoid Locomotion on a Passive Mobile Chair with Casters (55점)

[arXiv](https://arxiv.org/abs/2608.28090) · [PDF](https://arxiv.org/pdf/2608.28090) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28090) (요약 있음)

- **저자**: Kango Yanagida, Kazuki Miyazawa, Takato Horii
- **분야**: Humanoid · robotics relevance 9/10 · 1차 스크리닝 58점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 8쪽
- **읽은 원문**: PDF 전문

> 휴머노이드가 바퀴 달린 사무용 의자에 앉은 채 발로 바닥을 밀어 전후좌우와 회전 이동을 하도록 motion reference 없이 RL로 학습함. 좌우 대칭 regularization과 command curriculum을 함께 쓴 조건의 좌우 속도 추종 RMSE가 0.1268 m/s로, 같은 명령을 서서 추종하는 policy의 0.1490 m/s보다 낮음.

**무슨 문제인가**

QDD(quasi-direct-drive) 모터를 쓰는 휴머노이드는 선 자세를 유지하는 동안에도 관절 torque를 계속 내야 해서 전류와 열이 생김. 사람은 책상 작업 때 의자에 앉아 체중을 맡기고, 바퀴 달린 의자로 자리를 옮김. 기존 휴머노이드의 롤러스케이트·스케이트보드·스키 연구는 대부분 몸과 장치의 접촉을 미리 고정하고 장치를 통해 지면과 상호작용함. 골반이 좌석에 고정되지 않은 채 발로 바닥을 직접 밀어 로봇과 의자를 함께 움직이는 문제는 RL로 다뤄진 적이 없다고 저자는 주장함.

**어떻게 푸나**

mjlab(MuJoCo 기반 로봇 RL 학습 프레임워크)의 표준 서기 속도 추종 환경에 바퀴 다섯 개와 회전 좌석을 가진 수동 의자 모델을 넣고, 골반 주변 collision mesh와 마찰 설정을 다듬음. Unitree G1(29자유도)의 actor는 관절 상태, 몸통 각속도, 중력 방향, 직전 action, 속도 명령(전후·좌우 속도와 yaw rate)만 받고 29차원 관절 목표 위치를 출력함. 의자 상태와 접촉 정보는 학습 중 critic에만 줌(asymmetric actor-critic). reward에는 속도 추종, 자세 유지, 골반이 좌석 중심 근처에서 접촉을 유지하는 항이 들어가고, 사람 동작을 따라 하는 항은 없음. 비교할 요소는 좌우 대칭 regularization(SY), 접촉 중 발 미끄러짐 penalty(FS), 처음 2,000 iteration 동안 속도 범위를 ±0.5 m/s로 좁히는 command curriculum(CC)임. 세 요소를 켜고 끄는 8개 조합을 seed 4개씩 PPO로 학습함.

**결과**

- 무작위 명령 20초 rollout 1,000회 평가에서 8개 조건 모두 99.45% 이상이 앉은 상태를 유지한 채 조기 종료 없이 20초를 채움. SY+CC의 속도 추종 RMSE는 전후 0.1512 m/s, yaw 0.1453 rad/s로, 서서 걷는 policy(0.1551 m/s, 0.1752 rad/s)보다 낮음. 다만 서기 policy는 다른 환경과 reward로 학습했다고 저자가 밝힘.
- FS만 켠 조건은 전후 추종 RMSE가 0.1964±0.0432 m/s로 아무것도 켜지 않은 조건(0.1650 m/s)보다 높음. 일부 seed가 대각선 앞 방향 명령에서 전혀 움직이지 않는 해로 수렴했고, FS에 SY나 CC를 더하면 seed 4개 모두 이 실패가 없었음.
- 1.0 m/s 명령에서 SY+CC의 cost of transport(CoT: 양의 관절 일을 체중과 이동 거리로 나눈 값, 낮을수록 효율적)는 뒤 0.209, 옆 0.273, 앞 0.543 순임. 앞으로 갈 때는 발뒤꿈치를 먼저 짚고 무릎을 굽혀 당기고, 뒤와 옆으로 갈 때는 짚은 다리를 펴서 밂.
- 실제 Unitree G1에 추가 fine-tuning 없이 옮겨 앞·뒤·옆·회전 이동을 보임.

**한계**

실로봇 결과는 정성적 시연뿐이고 속도 추종 정확도와 외란 강건성은 측정하지 않음. 앉으면 배터리 전력이 111.06 W에서 101.25 W로 준다는 결과는 자세별 60초 측정 1회라 일반적인 에너지 절감 근거로 보기 어렵다고 저자도 밝힘. 의자 하나, 바닥 조건 하나, 명령 범위 하나에서만 실험했고 앉은 채 물건을 다루는 과제는 아직 하지 않음.

**누리랩 연구와의 연결**

- 직접 연결 약함. 고정되지 않은 접촉을 유지하며 수동 물체(의자)와 함께 움직이는 whole-body policy를 proprioception만으로 학습한 사례임.

*대표 그림: 실제 Unitree G1이 바퀴 달린 사무용 의자에 앉아 두 발로 바닥을 짚으며 이동하는 장면을 네 시점으로 겹쳐 보인 사진임. 측정 결과 그래프가 아니라 실로봇 시연 사진임.*

---

### 14. CoCoBench: A Cooperative Coordination Benchmark for Embodied Multi-Agent Task Planning (55점)

[arXiv](https://arxiv.org/abs/2608.28266) · [PDF](https://arxiv.org/pdf/2608.28266) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28266) (요약 있음) · [코드](https://github.com/AgibotGeneral/CoCoBench)

- **저자**: Yang Chen, Ye-Xin Xie, Lirong Che, Danyang Peng, Yuzhe Yang, Peiwen Lin, Xu Cao, Chuang Wang 외 3명
- **분야**: Embodied AI · robotics relevance 8/10 · 1차 스크리닝 55점
- **읽은 원문**: PDF 전문

> 여러 agent가 가사 과제를 함께 할 때 최종 성공률만으로는 보이지 않는 협업 실패를, 협업 유형 4가지별 궤적 점수로 따로 재는 benchmark CoCoBench를 만듦. 전체 성공률 1위인 GPT-5.6-sol(84.8%)도 작업 분담 점수는 0.63에 그침.

**무슨 문제인가**

MLLM을 planner로 쓰는 embodied agent가 여럿이 한 공간에서 일하는 상황이 늘고 있음. 기존 multi-agent embodied benchmark는 대부분 최종 과제 성공률이나 효율 하나로 팀을 평가함. 이 방식에서는 같은 일을 두 agent가 겹쳐 하거나, 서랍을 너무 일찍 닫거나, 칼 하나를 두고 다투거나, 넘겨받을 물건을 기다리며 노는 실패가 드러나지 않음. 성공한 episode 안에 규칙을 어긴 지름길이 섞여 있어도 구분하지 못함.

**어떻게 푸나**

저자는 한 agent의 행동이 다른 agent 행동의 가능 여부나 효율을 바꾸는 경우를 coordination coupling으로 정의함. 이 coupling을 네 가지 construct로 나눔. D1은 작업 분담(task allocation), D2는 순서 지키기(sequential ordering)임. D3는 공용 도구 충돌 피하기(mutual exclusion), D4는 중간 버퍼를 통한 물건 넘기기(handoff)임. AI2-THOR(가정 실내 시뮬레이터)에서 각 construct를 노리는 과제 897개를 만들고, agent는 2~4명임. policy 입력은 각 agent의 관측(이미지 또는 텍스트)과 이력이고, 출력은 이동·집기·놓기·열기·닫기·자르기·대기 같은 high-level skill 조합임. 고정된 executor가 skill을 실행하고 궤적을 기록함. 이 궤적에서 성공률(SR)과 construct 점수(CS, 0~1)를 따로 계산함. CS는 construct마다 다르게 계산함. D1은 기준 makespan(모든 작업을 마칠 때까지 걸린 총 시간) 대비 실제 makespan, D2는 순서 위반 비율, D3는 도구 충돌 비율과 길이, D4는 버퍼 넘침과 빈 버퍼 대기 횟수로 계산함. 과제는 배치 가능성, oracle policy의 해결 가능성, oracle 궤적이 목표 CS에서 거의 만점인지를 차례로 통과한 것만 남김.

**결과**

- 897개 전체에서 중앙 계획·이미지 관측 조건으로 MLLM 11개를 평가함. GPT-5.6-sol이 전체 SR 84.8%, CS 0.90으로 가장 높지만 D1 CS는 0.63, D3 CS는 1.00임. D1 SR·CS 1위는 전체 SR 24.6%인 Qwen3-VL-8B임.
- 240개 균형 subset에서 모델 4개 평균을 비교함. 중앙 계획(한 모델이 모든 agent의 행동을 정함)은 SR 48.0%, CS 0.69이고, 분산 계획(agent마다 따로 정함)에 broadcast 통신을 주면 39.6%와 0.65, 통신이 없으면 36.7%와 0.63임.
- 같은 subset에서 계획 구조 3가지 평균으로, 이미지를 빼고 텍스트만 주면 SR이 40.6%에서 42.3%로 오히려 오름. 저자는 병목이 시각 인식이 아니라 기호 수준의 팀 계획이라고 해석함.
- 성공률과 규칙을 지킨 계획 비율이 어긋남. Claude Haiku 4.5는 SR 63.1%이지만 규칙을 지킨 계획은 47.2%이고, Qwen3.6-Plus는 69.1% 대 56.7%임.

**한계**

모든 실험이 AI2-THOR 시뮬레이션이고 low-level 실행은 고정된 executor가 맡으므로 실로봇 조작 오류나 물리적 충돌은 다루지 않음. 이미지를 빼도 성능이 유지된다는 결과는 거꾸로 이 benchmark가 시각 정보를 거의 요구하지 않는다는 뜻이기도 함. 구조 비교와 관측 비교는 모델 4개, 과제 240개에서만 했고, 과제를 학습으로 개선하는 방법은 제안하지 않음.

**누리랩 연구와의 연결**

- 성공 여부와 별도로 궤적에서 순서 위반·자원 충돌·대기 같은 사건을 세어 실패 원인을 나누는 방식은 multi-agent 상황의 failure detection·diagnosis 평가 지표 설계에 참고할 수 있음.
- 그 밖의 누리랩 주제(VLA, manipulation, world model)와는 직접 연결 약함.

*대표 그림: 측정 결과가 아니라 benchmark의 동기를 그린 개념도임. 위쪽은 여러 로봇이 집 안 평면도에서 움직이는 장면이고, 아래 상자는 최종 성공률이 가리는 네 가지 협업 실패와 CoCoBench의 궤적 단위 construct 점수를 나열함.*

---

### 15. GeoFF3D: Coordinate-Anchored Feed-Forward Reconstruction for Large-Scale UAV Mapping (55점)

[arXiv](https://arxiv.org/abs/2608.28288) · [PDF](https://arxiv.org/pdf/2608.28288) · [alphaXiv](https://www.alphaxiv.org/abs/2608.28288) · [코드](https://github.com/yanxian-ll/GeoFF3D)

- **저자**: Xiang Yang, Yongli Wang, Yunsheng Zhang, Jun Li, Hao Chen, Haifeng Li
- **분야**: 3D Vision · robotics relevance 6/10 · 1차 스크리닝 56점
- **읽은 원문**: PDF 전문

> 드론 사진 수천 장을 feed-forward 모델로 복원할 때, GNSS 카메라 위치를 입력으로 넣어 처음부터 중력 기준 좌표계에서 예측하게 함. 긴 드론 비행 경로 benchmark UAVScenes의 경로 8개에서 5m 기준 F-score가 Pi3X 기반 분할 복원의 0.687에서 0.848로 오름.

**무슨 문제인가**

DUSt3R, VGGT, Pi3 같은 feed-forward 3D 복원 모델은 한 번에 수십 장만 처리하고, 결과를 기준 카메라 좌표계나 내부 정규화 좌표계로 냄. 드론 측량은 수백에서 수천 장을 찍고 결과를 위경도 기준의 중력 정렬 metric 좌표계로 받아야 함. 그래서 보통 이미지를 여러 묶음(chunk)으로 나눠 복원한 뒤 GNSS 위치에 맞춰 Sim(3) 변환(회전·이동·크기)으로 정렬함. 카메라가 거의 일직선으로 늘어선 비행 경로에서는 이 정렬의 roll과 pitch가 잘 정해지지 않아 복원 결과가 기울어짐. 묶음마다 따로 복원하므로 이웃 묶음끼리 같은 이미지의 depth가 달라 이음매와 높이 어긋남도 생김.

**어떻게 푸나**

GeoFF3D는 좌표 고정(coordinate-anchored) 예측 모델과 SLRF(spatial large-scale reconstruction framework, 공간 기반 대규모 복원 틀)로 이뤄짐. 예측 모델은 Pi3X에서 시작해, 이미지와 함께 GNSS 카메라 위치, 선택적으로 회전·ray 방향·depth를 받음. 출력은 Z축이 중력 반대 방향인 metric 좌표계의 카메라 pose와 픽셀별 point map, confidence임. 학습에서는 world 좌표계 point·pose loss와 카메라 위쪽 방향 loss를 더하고, 입력 prior를 무작위로 빼거나 흔들어 일부만 있어도 동작하게 함. SLRF는 각 이미지가 땅에 닿는 영역(footprint)을 추정해 촬영 순서가 아니라 공간 위치로 이진 트리를 만들어 묶음을 나눔. 장면 가운데 묶음부터 바깥으로 처리하면서, 앞 묶음에서 얻은 공유 이미지의 depth를 다음 묶음의 입력 prior로 넘김. 마지막에 roll과 pitch는 건드리지 않고 크기·yaw·이동만 맞추는 변환으로 잎에서 뿌리까지 묶음을 합침.

**결과**

- 항공 측량 블록 9개(UseGeo 3개, UAVFF3D-Real 6개, 블록당 224~1,177장) 평균 5m 기준 F-score가 Pi3X + SLRF의 0.829에서 0.877로 오름. 블록별로는 NF02, XX02, YHT02에서 Pi3X + SLRF가 더 높음.
- 긴 비행 경로인 UAVScenes 8개(원본 1,317~2,589 frame을 3장 간격으로 추출)에서 5m F-score가 0.848임. Pi3X + SLRF는 0.687, 평가한 SLAM·streaming 방법 중 가장 높은 LingBot-Map은 0.451임.
- 같은 조건 1m F-score는 0.181에서 0.319로 오름. 다만 Valley01·Valley02 두 경로에서는 1m F-score와 accuracy가 Pi3X + SLRF보다 낮음.
- 회전 prior 없이 위치 prior만 주면 세 장면 평균 ATE(카메라 위치 오차)가 5.52m에서 10.67m로 늘어남. 2,000장 복원에 약 5분, GPU 메모리 약 16GiB가 듦.

**한계**

입력 pose prior는 실제 GNSS·IMU 값이 아니라 정답 pose에 noise를 더해 만든 값이라, 실제 센서 오차에서의 성능은 보이지 않음. 회전 prior가 없으면 오차가 크게 늘어 IMU 자세 정보에 기대는 정도가 큼. 실험은 모두 하늘에서 내려다본 드론 영상이고, 전역 최적화나 온라인 복원은 다루지 않음.

**누리랩 연구와의 연결**

- 직접 연결 약함. 위치·자세 센서 값을 feed-forward 복원 모델의 좌표계를 정하는 입력으로 쓰는 설계는, 로봇 semantic mapping에서 odometry를 같은 방식으로 넣는 실험의 비교 대상이 될 수 있음.

*대표 그림: 카메라 배치에 따라 묶음별 복원을 합친 결과를 비교한 그림임. 카메라가 넓게 퍼진 경우는 Sim(3) 정렬과 GeoFF3D 모두 맞게 합쳐짐. 카메라가 거의 일직선인 경우는 Sim(3) 정렬 결과가 어긋나고 GeoFF3D 결과는 고르게 이어짐.*

---

## 오늘의 흐름

- **실행 중 어긋남을 잡아 계획을 고치는 구조**: 새 관측이나 실행 결과가 계획과 어긋날 때 재계획 여부와 위치를 정하거나, 제약을 어긴 실행 궤적을 반례로 삼아 과제 제약을 나타내는 automaton을 다시 배움. [Deciding If, When, and Where to Replan](https://arxiv.org/abs/2608.28075), [CEDAR](https://arxiv.org/abs/2608.27797)
- **world model을 실행 결과로 평가하고 쪼개 보는 시도**: 생성 영상을 화질로 평가하지 않고, 영상에서 3D 복원과 inverse dynamics로 뽑은 행동을 실제로 실행해 봄. 또는 로봇 부위별 particle로 예측을 나눠 어디서 틀렸는지 보게 함. [RoboPhys-3D](https://arxiv.org/abs/2608.28718), [AcrossVAM1.0](https://arxiv.org/abs/2608.28491)
- **VLA 입력과 학습 신호를 넓히는 방법**: 클릭 mask를 언어 지시와 같은 형식으로 넣거나, 학습 때만 미래 장면 변화를 맞히는 보조 head를 붙여 추론 비용을 늘리지 않고 성공률을 올림. [DeicticVLA](https://arxiv.org/abs/2608.28108), [PHR-VLA](https://arxiv.org/abs/2608.27609)
- **최종 성공률로는 안 보이는 실패를 따로 재는 평가**: 영상 단계별 실수 검출이나 multi-agent 협업 유형별 점수처럼, 실패를 종류별로 나눠 측정함. [Post-Training VLMs for Video Mistake Detection](https://arxiv.org/abs/2608.28406), [CoCoBench](https://arxiv.org/abs/2608.28266)
- **구조를 넣은 장면 표현**: 케이블을 joint로 이은 3DGS 사슬로 표현하거나, scene graph에 frontier와 예전 성공 기록을 함께 담아 다음 목표를 고름. [ChainSplat](https://arxiv.org/abs/2608.28570), [STEGNav](https://arxiv.org/abs/2608.28279)

## 해볼 만한 연구

### world model 예측 오차를 VLA failure detector로 쓰기
- 질문: world model 예측과 실제 관측의 차이 중 어떤 지표가 VLA 실행 실패를 가장 먼저 알려 주는지 밝힘.
- 첫 실험: LIBERO(시뮬레이션 조작 과제 모음)의 성공·실패 rollout에서 픽셀 오차, 3D 궤적 오차, 부위별 particle 오차를 실패 예측 AUROC로 비교함.
- 가장 가까운 연구: [RoboPhys-3D](https://arxiv.org/abs/2608.28718)는 world model 자체를 평가하는 데 그치고, 실행 중 실패를 예측하는 데는 쓰지 않음.

### 새 관측에 따른 재계획을 VLA 수준으로 옮기기
- 질문: 숨어 있던 물체가 드러날 때 VLA가 재계획 여부와 새 동작을 기존 계획의 어느 단계에 넣을지를 정하면 긴 조작 과제의 성공률이 오르는지 밝힘.
- 첫 실험: 가려진 물체가 있는 조작 과제에서 매 step 재계획, 재계획 없음, 관측 변화 판정 후 재계획 세 조건의 성공률과 계획 호출 수를 비교함.
- 가장 가까운 연구: [Deciding If, When, and Where to Replan](https://arxiv.org/abs/2608.28075)은 foundation model 기반 TAMP(task and motion planning)에서만 다루고, 학습된 VLA policy와는 묶지 않음.

### 성공·실패 쌍 reward로 로봇 실패 판정 VLM 학습하기
- 질문: 같은 단계의 성공·실패 rollout에 다른 답을 내도록 주는 reward가 로봇 실패 판정 정확도를 올리는지 밝힘.
- 첫 실험: 실로봇 rollout 쌍으로 VLM을 일반 GRPO(group relative policy optimization)와, 성공·실패 쌍에 다른 답을 낼 때 reward를 더 주는 GRPO로 각각 학습해 처음 보는 과제의 실패 검출 F1을 비교함.
- 가장 가까운 연구: [Post-Training VLMs for Video Mistake Detection](https://arxiv.org/abs/2608.28406)은 사람 요리 영상만 다루고 로봇 실행 영상은 쓰지 않음.

## 꼭 읽을 논문

- [Deciding If, When, and Where to Replan for Robust Manipulation](https://arxiv.org/abs/2608.28075): 새 관측 때문에 계획이 틀어지는 경우를 재계획 여부와 위치로 나눠 다룸. MuJoCo 시뮬레이션 14개 변형에서 가장 강한 baseline보다 성공률이 47.1퍼센트포인트 높음.
- [ChainSplat](https://arxiv.org/abs/2608.28570): 케이블 같은 변형 선형 물체를 joint 사슬과 3DGS로 묶어 상태 추정과 궤적 최적화를 같은 표현에서 함.
- [RoboPhys-3D](https://arxiv.org/abs/2608.28718): world model 생성 영상을 행동으로 바꿔 실행해 보는 평가 절차를 제시함.
- [DeicticVLA](https://arxiv.org/abs/2608.28108): 클릭 mask를 VLA 조건으로 넣는 방식 네 가지를 같은 조건에서 비교함.
- [STEGNav](https://arxiv.org/abs/2608.28279): 학습 없이 scene graph memory만으로, 목표 물체 여러 개를 차례로 찾는 GOAT-Bench에서 비교 방법 중 가장 높은 성공률을 냄.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (293편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2608.28075'>Deciding If, When, and Where to Replan for Robust Manipulation</a></td><td>76</td><td>10</td><td>TAMP</td><td>가려진 물체가 나중에 보이는 long-horizon 조작에서 재계획 여부와 시점 및 위치를 정하는 FM 기반 TAMP임. failure recovery와 직결됨</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2608.28491'>AcrossVAM1.0: Particle World Modeling for Text-Assisted Robot Video Prediction</a></td><td>72</td><td>8</td><td>World Model</td><td>particle 기반 world model로 텍스트 보조 로봇 비디오 예측을 하며 모션과 외형을 분리하는 설계가 world model 우선 주제에 부합함.</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2608.27609'>PHR-VLA: Planning Horizon Reasoning for Vision-Language-Action Models</a></td><td>68</td><td>10</td><td>VLA</td><td>VLA에 planning horizon reasoning을 명시적으로 넣어 현재 관측 의존을 줄이려는 시도임. 주제 적합도 높음</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2608.28279'>STEGNav: Spatio-Temporal Event Graph Reasoning for Multimodal Lifelong Object Navigation</a></td><td>68</td><td>9</td><td>Navigation</td><td>training-free로 spatial/temporal event graph와 dual-window memory를 쓰고 GOAT-Bench SR 66.3%를 보임. 탐색 frontier와 경험 재사용이 설득력 있음</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2608.28108'>DeicticVLA: Unifying Instruction Modes Based on Language and Deictic Gestures in a Single VLA</a></td><td>66</td><td>10</td><td>VLA</td><td>언어와 deictic 제스처를 하나의 VLA로 통합해 지시 모호성을 해소함. 문제 설정이 실용적임</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2608.28718'>RoboPhys-3D: A Comprehensive Embodied World Model Evaluation via 3D Reconstruction</a></td><td>66</td><td>9</td><td>World Model</td><td>RoboTwin 2.0 기반 50개 과제, 50개 지표의 3D 복원 평가로 world model의 상태·실행 실패를 드러내고 인간 평가와 상관 0.98을 보임. world model 평가 도구로 가치 큼</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2608.28570'>ChainSplat: A Physics-Inspired Screw-Theoretic Model for Learning Deformable Linear Object Dynamics from Multi-View RGB Videos</a></td><td>66</td><td>8</td><td>Manipulation</td><td>screw 이론 open-chain 모델과 Gaussian splatting을 결합해 RGB만으로 DLO dynamics를 학습함. 실로봇 실험과 모델 기반 궤적 최적화까지 보이고 코드 공개됨</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2608.28140'>Contact-Guided Exploration for Non-Prehensile Locomanipulation with Multi-Critic RL</a></td><td>64</td><td>9</td><td>RL</td><td>접촉 유도 탐색과 multi-critic RL로 비파지 locomanipulation을 학습함. 희소 보상 문제를 구체적으로 다룸</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2608.28549'>Video Generative Models as Geometry Learner</a></td><td>62</td><td>6</td><td>3D Vision</td><td>video 생성 모델을 next-frames 예측으로 geometry 추정에 전용해 100배 적은 데이터로 discriminative SOTA에 근접함. 새 formulation이며 로봇 3D 이해에 유용함</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2608.28090'>Stay Seated: Learning Omnidirectional Humanoid Locomotion on a Passive Mobile Chair with Casters</a></td><td>58</td><td>9</td><td>Humanoid</td><td>수동 캐스터 의자에 앉은 휴머노이드의 전방향 이동을 RL로 학습함. 새 문제 설정이나 loco-manipulation 첫 단계임</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2608.27797'>CEDAR: Automata as Verifiable Interfaces for Language-Guided Embodied Action</a></td><td>58</td><td>7</td><td>Embodied AI</td><td>오토마타 교집합으로 지속 제약을 구성적으로 강제하고 반례로 skill을 수리함. 실험이 Minecraft에 한정됨</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2608.28406'>Post-Training VLMs for Video Mistake Detection</a></td><td>58</td><td>5</td><td>Video</td><td>open-set mistake detection용 MD-VQA benchmark와 VLM post-training reward를 제안함. 미관측 절차에서 개선되어 failure detection과 연결됨</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2608.28288'>GeoFF3D: Coordinate-Anchored Feed-Forward Reconstruction for Large-Scale UAV Mapping</a></td><td>56</td><td>6</td><td>3D Vision</td><td>좌표 고정 feed-forward 재구성과 계층 집계로 2000장 UAV 매핑을 5분에 처리함. 강한 SLAM baseline 대비 F-score가 크게 높아 근거가 탄탄함</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2608.28293'>A Probabilistic Interpretation of KV Cache Eviction</a></td><td>56</td><td>2</td><td>Efficient LLM</td><td>KV eviction을 형식화해 NP-hard를 증명하고 기대값 추정으로 decode 시점 보정을 가능케 함. 이론적 정리가 강점임</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2608.28266'>CoCoBench: A Cooperative Coordination Benchmark for Embodied Multi-Agent Task Planning</a></td><td>55</td><td>8</td><td>Embodied AI</td><td>MLLM 다중 에이전트 협업 계획을 세분 진단하는 CoCoBench임. benchmark 기여임</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2608.28518'>When Robots Mishear Us: Mapping the Safety Risks of Voice-Controlled Embodied AI</a></td><td>55</td><td>7</td><td>Embodied AI</td><td>ASR 오류가 embodied AI 안전 위험으로 이어지는 점을 체계적으로 분석해 음성 제어 로봇 안전에 직접 관련됨.</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2608.28578'>Aero Hand Open: A Simulation-Ready Tendon-Driven Hand for Dexterous Manipulation Learning</a></td><td>54</td><td>8</td><td>Manipulation</td><td>cable 전달을 재현한 시뮬레이션과 actuation map, RL 패키지로 sim-only 학습 정책을 fine-tuning 없이 실제 손에 올림. 하드웨어와 환경 전체 공개가 강점이나 방법 novelty는 제한적임</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2608.28386'>GraspHOI: Full-Body 3D Human-Object Reconstruction with Finger-Level Grasps from a Single In-the-Wild Image</a></td><td>54</td><td>6</td><td>3D Vision</td><td>단일 이미지에서 물체 사전 mesh 없이 손가락 contact까지 최적화해 전신 HOI를 복원함. 네 benchmark 여섯 baseline 대비 개선되어 dexterous 데이터 추출에 연결됨</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2608.28733'>Generation of High-Level Concepts in 3D Scene Graphs via Autoregressive Diffusion</a></td><td>54</td><td>6</td><td>Scene Graph</td><td>구조와 특징을 함께 학습하는 자기회귀 diffusion으로 임의 깊이 3DSG를 생성하고 로봇 센서 데이터까지 평가함. Gromov-Wasserstein 평가도 제안함</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2608.28216'>WALDO: One-Shot Exemplar-Conditioned Object Detection in Cluttered Scenes with World-Model Features</a></td><td>52</td><td>6</td><td>Embodied AI</td><td>one-shot 인스턴스 검출에서 DINOv3와 V-JEPA 2.1 world model 특징이 상호 보완적임을 보임. 융합 이득은 modest하나 로봇 객체 탐색에 유용함</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2608.27685'>Distributed Model-Based Diffusion: Finite Horizon Contraction under Bounded Delay</a></td><td>52</td><td>6</td><td>Planning</td><td>분산 model-based diffusion의 지연 하 수렴을 분석한 다중 에이전트 궤적 최적화임</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2608.27562'>VidParse: Online Parsing of Egocentric Procedures Like a Pro</a></td><td>52</td><td>5</td><td>Video</td><td>training-free로 task graph 제약 beam search를 써서 egocentric 조작 절차를 온라인 파싱함. 로봇 절차 이해와 연결됨</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2608.27881'>StreamEMS: Streaming Video Understanding with Self-Evolving Memory Scheme for Vision-Language Models</a></td><td>52</td><td>5</td><td>Video</td><td>streaming video용 self-evolving memory로 VLM 기억을 관리함. robot memory와 연결 가능함</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2608.27678'>SegBench-GC: Testing Segmentation Invariance in Multi-Step Offline Goal-Conditioned Reinforcement Learning</a></td><td>52</td><td>4</td><td>RL</td><td>offline GCRL에서 궤적 분할 불변성을 점검하는 benchmark로 RL 진단 가치는 있으나 벤치 중심임</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2608.28128'>VICT: Verifier-Instrumented Credit Tracing for Long-Horizon LLM Agent Reinforcement Learning</a></td><td>52</td><td>3</td><td>RL</td><td>검증기 기반 credit tracing으로 long-horizon LLM agent RL의 credit assignment를 다룸</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2608.27628'>One year in a forest: Analyzing the challenges of autonomous navigation in subarctic environments</a></td><td>50</td><td>8</td><td>Navigation</td><td>아북극 숲에서 1년간 자율 주행 과제를 분석한 실환경 연구임. 알고리즘 novelty는 낮으나 실로봇 근거가 가치 있음</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2608.28270'>Spatial-Semantic Reasoning using Large Language Models for Efficient UAV Search Operations</a></td><td>50</td><td>8</td><td>Navigation</td><td>LLM 공간-의미 추론으로 UAV ObjectNav 탐색 시간을 줄임. 방법은 평이한 LLM 활용임</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2608.28460'>LayerRecall: A State-Conditioned Memory Router for Long-Horizon Consistency in Video Generation</a></td><td>50</td><td>4</td><td>Video</td><td>상태 조건 memory router로 long video 생성 일관성 유지함. memory 개념이 world model과 연결됨</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2608.27735'>ABCD: Alpha-Composited Block Coordinate Descent: Constant-VRAM Training for Large Radiance Fields</a></td><td>50</td><td>3</td><td>3D Vision</td><td>block coordinate descent로 대형 3DGS를 일정 VRAM에서 학습함. 실용적이나 로봇 직접성 낮음</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2608.28008'>Visual Token Coding for Video Multimodal Large Language Models</a></td><td>50</td><td>2</td><td>Multimodal</td><td>video coding에서 착안한 visual token 압축임. 효율적 inference에 관련되나 로봇 직접성 낮음</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2608.28444'>Sliding-window beats linear attention</a></td><td>50</td><td>2</td><td>Efficient LLM</td><td>sliding window와 sink가 retrofit linear attention보다 낫다는 비교를 보임. 단순하나 실용적 결과임</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2608.27793'>CAVE-NAV: VLM-Based Autonomous 3D Navigation in Underwater Cave Environments</a></td><td>48</td><td>8</td><td>Navigation</td><td>VLM으로 수중 동굴 3D 내비게이션을 수행하는 응용 시스템임. 도메인 새로우나 방법은 평이함</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2608.28175'>Picking Bins Empty: A Hierarchical Hybrid Approach with Online Self-Learning of Grasp Points for Reliable Industrial Bin-Picking</a></td><td>48</td><td>8</td><td>Manipulation</td><td>산업용 bin-picking에서 grasp point를 온라인 self-learning하는 하이브리드 접근임. 실용적이나 증분적임</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2608.28404'>How Far Can 5,500 Hours of Driving Take You? A Scaling Law Analysis of Video Diffusion Models</a></td><td>48</td><td>4</td><td>World Model</td><td>1M~9B 주행 video diffusion의 power-law scaling 분석임. 학습 노출이 모델 크기보다 효율적이라는 결과이며 world model 학습 예산에 참고됨</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2608.28192'>Locate Anything in Videos: Rethinking Efficient Generative Spatio-Temporal Video Grounding</a></td><td>48</td><td>3</td><td>Video</td><td>생성형 spatio-temporal video grounding을 효율화함. 일반 video 이해임</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2608.28316'>Conditional Visual Evidence Utility: State-Dependent Rank Reversals in Frozen Vision-Language Encoders</a></td><td>48</td><td>3</td><td>Multimodal</td><td>관측 상태에 따라 시각 증거 순위가 뒤바뀜을 800 장면 통제 실험으로 보임. 다만 상태 정보 예측기는 이득을 확립하지 못함. active perception과 개념적으로 연결됨</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2608.28476'>ContextPilot: Teaching Agents for Proactive Context Management via Fine-grained RL</a></td><td>48</td><td>2</td><td>NLP</td><td>fine-grained RL로 에이전트 컨텍스트 관리를 학습함. 장기 memory 관리 관점은 있음</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2608.27808'>CURA: Certified Runtime Alarms for Computer-Use Agents</a></td><td>48</td><td>2</td><td>AI</td><td>CUSUM 기반 인증 경보로 실패의 42.3%를 사전 탐지하고 false alarm을 통제함. 한계도 솔직히 보고하나 GUI 에이전트 한정임</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2608.27953'>The Illusion of $\textit{What If}$: Evaluating the Breakdown of Counterfactual Reasoning in LLMs</a></td><td>48</td><td>2</td><td>NLP</td><td>LLM의 counterfactual reasoning 붕괴를 평가하는 benchmark로 주제는 맞으나 LLM 텍스트 한정임.</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2608.27726'>Coordinated Motion Planning for Multi-Arm Systems via Iterative LQ Games</a></td><td>46</td><td>7</td><td>Manipulation</td><td>iterative LQ game으로 다중 팔 협응 모션 플래닝을 함. 고전 제어 기반으로 증분적임</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2608.28305'>PanelShield: Verifiable Closed-Loop Safe Planning for Robotic Industrial Panel Operation</a></td><td>46</td><td>6</td><td>Embodied AI</td><td>LTL과 Safety FSM 이중 검증, counterexample 기반 수리로 위반율 2.7%를 달성하고 실로봇 실험도 함. failure repair 관점은 있으나 패널 도메인 특화임</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2608.28435'>Linear Temporal Logic Translation via Human-Inspired Self-Constrained Reasoning for Robot Task Specification</a></td><td>46</td><td>6</td><td>Embodied AI</td><td>구조 제약을 추론 내부에 넣는 SCR로 LTL 변환의 제약 만족과 일반화를 높임. 수치가 초록에 없어 증분적으로 판단됨</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2608.27871'>Temporal Tree of Thought: Reasoning-Guided Visual Cue Search for Long-Video Understanding</a></td><td>46</td><td>3</td><td>Video</td><td>tree search로 long-video 단서를 찾는 reasoning 방식임. 일반 video 이해 개선임</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2608.27727'>Probing Perceptual Priors of MLLMs via Gibbs Sampling with Interpretable Generative Controls</a></td><td>46</td><td>2</td><td>Multimodal</td><td>Gibbs sampling으로 MLLM의 지각 prior를 탐침함. 참신한 해석 방법임</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2608.28213'>PAMoR: Parameterized Affective Motion Generation in Real Time for Humanoid Robots</a></td><td>45</td><td>6</td><td>Humanoid</td><td>휴머노이드의 감정 표현 모션을 파라미터로 실시간 생성함. 사회적 로봇 응용임</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2608.27860'>From Perspective to Fisheye Depth Estimation and Open-Vocabulary Segmentation</a></td><td>45</td><td>4</td><td>3D Vision</td><td>perspective에서 fisheye로 depth와 segmentation을 확장함. 로봇 카메라에 유용하나 incremental함</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2608.27922'>DensityKV: Density-Guided KV Cache Compression for Long Video Generation</a></td><td>45</td><td>3</td><td>Video</td><td>long video generation의 KV cache 압축임. 효율화 기법으로 world model에 간접 관련됨</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2608.28069'>VersaGauss: A Versatile Framework for Generating Multiphase Dynamics with 3D Gaussians</a></td><td>45</td><td>3</td><td>3D Vision</td><td>3D Gaussian으로 다상 유체 동역학을 생성함. 물리 시뮬레이션 관련되나 로봇 거리 있음</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2608.28174'>Manifold4D: Denoising on Point Cloud Rendered Manifolds for Video Re-shooting</a></td><td>45</td><td>2</td><td>Video</td><td>point cloud manifold 렌더링 기반 video re-shooting 디노이징임. 생성 위주임</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2608.27885'>There and Back Again: Bidirectional Diffusion Bridges for Multimodality Translation</a></td><td>45</td><td>1</td><td>Generative</td><td>양방향 diffusion bridge로 modality 번역을 하는 생성 모델 연구로 로봇 연결 약함</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2608.28246'>Training-free Suction Grasp Detection for Deformed Aseptic Cartons Using Vision-Language Models and Geometric Surface Scoring</a></td><td>44</td><td>7</td><td>Manipulation</td><td>VLM과 기하 점수로 찌그러진 카튼의 suction grasp를 training-free로 검출함. 응용 시스템이며 증분적임</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2608.27929'>Training-Free Temporal Abstraction for General Video Understanding</a></td><td>44</td><td>3</td><td>Video</td><td>training-free temporal abstraction으로 video 이해를 효율화함. 일반 video 방법임</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2608.28113'>H-Scale: Hessian-Guided Scale Refinement for NVFP4 Sub-Byte LLM Inference</a></td><td>44</td><td>2</td><td>Efficient LLM</td><td>Hessian 대각 근사로 NVFP4 그룹 scale을 정제하며 추론 오버헤드가 없음. 증분적임</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2608.28214'>Probabilistic Multi-Robot Gas Source Localization with Uncalibrated Sensors: A Distributed Estimation Approach</a></td><td>42</td><td>6</td><td>Multi-Robot</td><td>비보정 센서를 쓰는 다중 로봇 가스원 위치 추정의 분산 추정법임. 도메인 특화임</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2608.28096'>Ex-Sim(3)-Reg: 2D-3D Correspondence Pruning via Extended Sim(3) Registration</a></td><td>42</td><td>5</td><td>3D Vision</td><td>2D-3D 대응 pruning용 Sim(3) 정합임. localization에 관련되나 incremental함</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2608.27584'>Quanta Perception as Probabilistic Events</a></td><td>42</td><td>4</td><td>CV</td><td>photon 이벤트 확률 모델 기반 quanta 센싱 인식임. 고속 로봇 센싱에 관련되나 incremental함</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2608.27866'>Iron: Intent-Aligned and Retrospective Dual Learning Framework for Enhancing Generalist Virtual Agents</a></td><td>42</td><td>4</td><td>Agent</td><td>가상 agent의 intent 정렬과 회고 학습 프레임워크임. GUI 에이전트 중심이라 로봇 거리 있음</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2608.28240'>WilLaGS: Latent-Conditional 3D Appearance Fields for Robust Gaussian Splatting In-the-Wild</a></td><td>42</td><td>3</td><td>3D Vision</td><td>in-the-wild 3DGS용 latent 조건 appearance field임. 로봇 직접성 낮음</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2608.28707'>ReVA: A Region-Aware Visual Assistant for Visually Grounded Question Answering</a></td><td>42</td><td>3</td><td>Multimodal</td><td>영역 인식 시각 보조로 MLLM의 공간 환각을 줄임. 증분적이나 공간 추론과 관련됨</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2608.27750'>The Calls are Coming from Inside the Model: Investigating Probe-based Detection of Tool-Calling Errors in LLMs</a></td><td>42</td><td>2</td><td>NLP</td><td>LLM hidden state probe로 tool-calling 오류를 검출함. failure detection과 약하게 연결됨</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2608.28010'>When Can Conditional Flow Matching Replace Pointwise Negative Log-Likelihood?</a></td><td>42</td><td>2</td><td>Generative</td><td>conditional flow matching 손실을 NLL로 대체 가능한 조건을 규명함. flow policy 정렬에 시사점 있음</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2608.28158'>HARTS: A Prefix-Sharing Training System for Agentic RL with Hybrid-Attention Models</a></td><td>42</td><td>2</td><td>RL</td><td>agentic RL 학습의 prefix 공유 시스템으로 효율성 기여가 있으나 시스템 엔지니어링임</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2608.28264'>Finding Where the Buck Stops: An Automated Failure Attribution-Based Reflection Framework for Multi-Agent Collaboration</a></td><td>42</td><td>2</td><td>LLM Agent</td><td>multi-agent 실패 귀인 기반 reflection으로 failure diagnosis 주제와 닿으나 LLM agent 한정임.</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2608.28383'>Semantic Head Specialization Guides Hybrid ViT Attention for Multimodal LLMs</a></td><td>42</td><td>1</td><td>Multimodal</td><td>MLLM ViT 하이브리드 attention 설계 분석임. 로봇 직접성 낮음</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2608.27763'>Fast Weight Attention for Continual Learning</a></td><td>42</td><td>1</td><td>LG</td><td>fast weight attention을 continual learning 관점에서 분석함. 이론적이나 로봇 연결 약함</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2608.27795'>uScenes: A Multimodal RGB and 3D Sonar Dataset for Underwater Robot Perception</a></td><td>40</td><td>6</td><td>Robot Perception</td><td>수중 로봇용 RGB와 3D sonar 데이터셋임. 데이터셋 기여 위주임</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2608.28033'>ZipMVS: Multi-View Stereo with Compressed Cost Volumes</a></td><td>40</td><td>3</td><td>3D Vision</td><td>cost volume 압축한 MVS임. 메모리 효율 개선이며 incremental함</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2608.28080'>Cyc3D: Evaluating Cyclic Structural Stability and Asset Usability in Image-to-3D Generation</a></td><td>40</td><td>3</td><td>3D Vision</td><td>image-to-3D 생성의 순환 안정성 평가 benchmark임. 평가 기여임</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2608.28541'>An Enclosed Mode Is a Gauge Choice: Topology Relative to Reach in Certified Code World Models</a></td><td>40</td><td>3</td><td>World Model</td><td>certified code world model이 접근 가능 영역 밖에서 틀릴 수 있음을 이론화함. world model 신뢰성과 연결됨</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2608.27996'>Should I Use This Synthetic Dataset for Training? How to Test with Minimal Real Data</a></td><td>40</td><td>3</td><td>LG</td><td>digital twin/world model 합성 데이터를 최소 실데이터로 검증하는 통계 검정이라 sim-to-real 데이터 신뢰와 연결됨.</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2608.28726'>Pro-Router: Token-Aware Progressive Model Routing with Adaptive Edge-Cloud Collaboration for Efficient Multimodal LLM Inference</a></td><td>40</td><td>3</td><td>Multimodal</td><td>edge-cloud 협업 MLLM 라우팅으로 온디바이스 효율 추론과 연결됨.</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2608.28138'>Token-Budget Distillation: Transferring Full-Token Semantics to Compressed Video Vision-Language Models</a></td><td>40</td><td>2</td><td>Video</td><td>token budget 증류로 압축 video VLM 성능 유지함. 효율화 기법임</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2608.28706'>Variable-Granularity Tokenization for High-Resolution Object Detection</a></td><td>40</td><td>2</td><td>CV</td><td>가변 granularity tokenization으로 고해상도 검출함. 효율화 incremental함</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2608.27757'>Beyond Search-Imitation: Prior-Directed Exploration for Searchless Chess</a></td><td>40</td><td>2</td><td>RL</td><td>searchless chess에서 prior 기반 탐색으로 search imitation 한계를 넘으려 함. 체스에 한정됨</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2608.27985'>Is Monte Carlo Tree Search Just Every-Visit Monte Carlo Control?</a></td><td>40</td><td>2</td><td>RL</td><td>MCTS가 every-visit MC control과 같다는 개념 연결 분석으로 RL 이론적 통찰이 있음</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2608.27785'>Compositional Failure in Audio-Visual LLMs: Late-Layer Prior Dominance Under Cross-modal Conflict</a></td><td>40</td><td>2</td><td>Multimodal</td><td>AV-LLM의 교차 모달 충돌 시 late-layer prior 지배를 분석함. 진단 연구로 의미 있음</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2608.27768'>Why Didn&#x27;t It Check? Unsupported Final Claims and Their Repair in Two Tool-Equipped Language Models</a></td><td>40</td><td>2</td><td>AI</td><td>도구 사용 LM이 근거 없이 결론을 내는 실패와 수리를 분석함. failure 관점이 있음</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2608.27906'>Design the Feedback, Not Just the Reward: Environments for Open-Ended Reinforcement Learning</a></td><td>40</td><td>2</td><td>RL</td><td>open-ended 과제용 RL 환경의 feedback 설계 논의로 language feedback 학습과 일부 연결됨.</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2608.28306'>VISTA: Verifier-Informed Student-to-Teacher Adaptation for On-Policy Self-Distillation</a></td><td>40</td><td>1</td><td>NLP</td><td>검증기 정보로 on-policy self-distillation의 teacher를 적응시킴. LLM 추론 학습 개선임</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2608.28560'>A Formal Limitation on Learning Human Language From Textual Corpora</a></td><td>40</td><td>0</td><td>NLP</td><td>텍스트만으로 의미 복원이 불가능한 정보이론적 한계를 유도함. 이론적 기여가 있음</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2608.28300'>MaCoPlanner: LLM-Assisted Manual-Compiled Task Planning with Proactive Safety Verification for Robotic Industrial Panel Operation</a></td><td>38</td><td>6</td><td>Embodied AI</td><td>매뉴얼 기반 LLM task planning과 안전 검증을 산업용 패널 조작에 적용함. 응용 중심이고 novelty 제한적임</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2608.28409'>Cooperative Risk-Aware Exploration in Heterogeneous Multi-Robot Systems Using Algorithmic Altruism</a></td><td>38</td><td>6</td><td>Multi-Robot</td><td>Hamilton 법칙 기반 altruism으로 Social Nash Equilibrium 계획을 구성하고 하드웨어 실험도 함. 고전 기법 중심임</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2608.27867'>CoRe-MoE: Compact Reusable MoE for Continual Multimodal Instruction Tuning</a></td><td>38</td><td>2</td><td>Multimodal</td><td>continual multimodal instruction tuning용 MoE 압축으로 continual 주제와 약하게 닿음.</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2608.28206'>NumBench: Diagnosing Counting Failures in Text-to-Image Models</a></td><td>38</td><td>1</td><td>Generative</td><td>T2I 개수 오류 진단 benchmark임. 평가 기여임</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2608.27728'>Diffusion Distillation for Efficient Weather Ensembles</a></td><td>38</td><td>1</td><td>LG</td><td>diffusion 앙상블을 단일 단계로 증류하는 효율화 기법이나 날씨 도메인에 한정됨</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2608.28276'>Parser Transitions Already Reveal Structural Responsibility: KV Persistence for Structured Generation</a></td><td>38</td><td>1</td><td>NLP</td><td>parser 전이를 이용한 구조화 생성의 KV 유지 기법으로 LLM 추론 효율화임</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2608.27661'>Knowing Before Answering: Decoding Language Models for Reliable RAG</a></td><td>38</td><td>1</td><td>NLP</td><td>모델 내부 신호로 RAG 근거의 충분성과 충돌을 3분류함. 증분적 연구임</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2608.28018'>Twin Worlds: Equivariance-Based Abstention for Evidence-Grounded Reasoning</a></td><td>38</td><td>1</td><td>NLP</td><td>equivariance 기반 abstention으로 근거 부족 시 답변을 보류함. 아이디어는 참신하나 NLP 한정임</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2608.27960'>When Teacher Guidance Misleads: Reward-Aligned On-Policy Distillation</a></td><td>38</td><td>1</td><td>RL</td><td>teacher 지침이 오도하는 문제를 reward 정렬로 푸는 OPD 개선임.</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2608.27964'>AERA: Adaptive Evidence Residual Allocation for Efficient Test-Time Reasoning</a></td><td>38</td><td>1</td><td>LLM Reasoning</td><td>test-time 연산 예산 적응 할당 기법으로 LLM 한정임.</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2608.28099'>Speculative Probing: LLM Monitoring at Speculative-Decoding Cost</a></td><td>38</td><td>1</td><td>Efficient Inference</td><td>speculative decoding 비용으로 LLM 모니터링하는 효율 기법이나 로봇 직접성은 약함.</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2608.28382'>When Linguistic and Internal Confidence Diverge in Large Language Models</a></td><td>38</td><td>0</td><td>NLP</td><td>언어적 확신과 내부 확신의 불일치를 30개 모델로 분석함. 규모 있는 분석임</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2608.28020'>3D-USE: From Image-Level to Scene-Level Underwater Enhancement</a></td><td>36</td><td>3</td><td>3D Vision</td><td>수중 3D 장면 enhancement임. 도메인 특화임</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2608.27796'>ReToolSQL: Agentic Reinforcement Learning for Robust Text-to-SQL</a></td><td>36</td><td>1</td><td>RL</td><td>agentic RL로 text-to-SQL 오류 복구를 학습함. 증분적이고 로봇 무관함</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2608.27963'>SABER: Stability-Aware Early Exit for LLM Reasoning via Adversarial Branch Probing</a></td><td>36</td><td>1</td><td>LLM Reasoning</td><td>reasoning 조기 종료 기법으로 효율 추론이나 incremental함.</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2608.28082'>Attribute Token Arithmetic: Disentangled and Continuous Semantic Control for Visual Autoregressive Models</a></td><td>36</td><td>0</td><td>Generative</td><td>visual autoregressive 모델의 속성 token 산술 제어임. 로봇 무관함</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2608.28496'>Ladders in Chaos: When, How, (and Perhaps Why) Does Test-Time Scaling Improve LLM Machine Translation</a></td><td>36</td><td>0</td><td>NLP</td><td>번역에서 test-time scaling 효과를 분석함. 분석 위주이고 로봇 무관함</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2608.28421'>Program Learning with Verifiable Rewards: Symbolic Backpropagation for Post-Training LLMs</a></td><td>36</td><td>0</td><td>LLM</td><td>symbolic backpropagation으로 프로그램 학습을 하는 post-training 새 시도이나 로봇과 무관함.</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2608.27997'>A-PAIR: A Benchmark and Identity-Consistent Grounding Framework for Air-Ground Cross-View Referring Person Detection</a></td><td>35</td><td>4</td><td>Embodied AI</td><td>공중-지상 cross-view 지시 기반 사람 검출 benchmark임. 협업 embodied에 관련되나 좁음</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2608.28429'>Lossy Event Compression: From Event Stream Distortion to Task Performance</a></td><td>35</td><td>3</td><td>Event Camera</td><td>event stream 손실 압축을 task 성능과 연결함. 센싱 효율 개선임</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2608.27911'>TACIT-Switch: Cost-Aware Model Escalation for LLM Agents from Censored Supervision</a></td><td>35</td><td>2</td><td>NLP</td><td>LLM agent의 비용 인지 모델 승격 라우팅으로 실패 모드 감지와 일부 닿음</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2608.28534'>InstructMesh: Selective Refinement of Generative 3D Models for Fabrication</a></td><td>35</td><td>2</td><td>3D Vision</td><td>생성 3D 모델의 제작용 선택적 정제로 3D 생성 응용임.</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2608.28058'>Dynamic Alignment Compensation for Hallucination Mitigation in Large Vision-Language Models</a></td><td>35</td><td>1</td><td>Multimodal</td><td>LVLM hallucination 완화용 alignment 보정임. incremental함</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2608.28272'>Non-Uniform Quantisation for 3DGS Compression</a></td><td>35</td><td>1</td><td>3D Vision</td><td>3DGS 압축용 비균일 양자화임. incremental함</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2608.27875'>HyQuant: Hybrid-Precision Quantization for LLM Attention</a></td><td>35</td><td>1</td><td>Efficient Inference</td><td>attention 하이브리드 정밀도 양자화로 효율 추론 기법이나 로봇 직접성은 약함.</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2608.28312'>AIM: Anchor Identity Features, Then Match for Multimodal Large Language Model Unlearning</a></td><td>35</td><td>0</td><td>Multimodal</td><td>MLLM 신원 정보 unlearning 방법임. 로봇 무관함</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2608.27651'>More Data Cannot Break a Symmetry: Identifiability by Design</a></td><td>35</td><td>0</td><td>LG</td><td>표현 정렬의 식별 가능성을 대칭군으로 분석한 이론 성격 연구로 로봇 연결 약함</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2608.28150'>Intrinsic Interaction Geometry Controls the Low-Rank Complexity of Softmax Attention</a></td><td>35</td><td>0</td><td>LG</td><td>softmax attention의 low-rank 복잡도를 기하로 분석한 이론 연구임</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2608.28262'>SinkSLOT: Sinkhorn via Sparse Lifted Optimal Transport</a></td><td>35</td><td>0</td><td>LG</td><td>sparse lifted OT로 Sinkhorn을 가속하는 수치 기법임</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2608.28425'>Euclidean Fourier Neural Operators</a></td><td>35</td><td>0</td><td>LG</td><td>FNO를 비주기 유클리드 도메인으로 확장한 과학 ML 연구임</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2608.27925'>Entity-Memory Graph Retrieval Improves Evidence Coverage in Long-Conversation Question Answering</a></td><td>34</td><td>2</td><td>NLP</td><td>entity-memory 그래프 검색으로 긴 대화 QA 근거 범위를 넓힘. memory 구조는 로봇 memory와 약하게 연결됨</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2608.27790'>Credo: Reusable Declarative Primitives for Agentic Workflows</a></td><td>34</td><td>1</td><td>AI</td><td>에이전트 workflow용 선언적 primitive를 제안함. 시스템 중심임</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2608.27982'>Learning from Hard Prompts: Difficulty-aware Advantage Amplification in Dynamic Sampling</a></td><td>34</td><td>1</td><td>RL</td><td>DAPO dynamic sampling에서 어려운 prompt advantage 증폭하는 작은 개선임.</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2608.28363'>EvoUndo: Recoverability-Constrained Self-Evolution for LLM Agent Harnesses</a></td><td>34</td><td>1</td><td>LLM Agent</td><td>agent 자기진화 시 복구 가능성을 제약하는 개념이 recovery와 닿으나 LLM 하네스 한정임.</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2608.27882'>SOMTab: Set-Order Mamba for Efficient Tabular In-Context Learning</a></td><td>34</td><td>0</td><td>LG</td><td>Mamba 기반 tabular in-context learning 효율화로 증분적임</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2608.27760'>Informational Antilocality and the Locality Bias in LLMs</a></td><td>34</td><td>0</td><td>NLP</td><td>antilocal 언어로 LLM의 locality bias를 분석함. 이론적 호기심 위주임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2608.27899'>OpenStamp: A Watermark for Open-Source Language Models</a></td><td>34</td><td>0</td><td>NLP</td><td>오픈소스 LLM용 워터마크를 제안함. 문제 설정은 의미 있으나 로봇 무관함</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2608.27580'>LongGuard: Mechanistic Analysis and Training-Free Mitigation of Long-Context Failure in Safety Guardrails</a></td><td>34</td><td>0</td><td>NLP</td><td>긴 문맥에서 안전 guardrail 실패를 분석하고 학습 없이 완화함. 로봇 무관함</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2608.28078'>Task-State Adaptation with Prototype Memory for Multi-Task Dense Prediction</a></td><td>33</td><td>1</td><td>CV</td><td>prototype memory 기반 multi-task dense prediction임. incremental함</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2608.28241'>Beyond Task-Only Matching: Personalized Skill Routing with Counterfactual Evaluation</a></td><td>33</td><td>1</td><td>LLM Agent</td><td>사용자별 skill 라우팅과 counterfactual 평가로 agent skill 선택 문제임.</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2608.28724'>MANTLE: A Framework for Adaptive In-Situ Planetary Perception Using a Modular Uplink Principle</a></td><td>32</td><td>6</td><td>Robot Perception</td><td>DINOv2 고정 backbone에 task head를 uplink하는 화성 지형 분류와 boulder 분할임. 설계 개념은 있으나 기법 novelty 낮음</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2608.27924'>What Makes Agent Memory Useful for Reliable Unanswerable Question Handling?</a></td><td>32</td><td>2</td><td>NLP</td><td>agent memory가 답변 불가 질문 처리에 주는 효과를 체계적으로 연구함. 분석 위주임</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2608.28205'>Cut-ViT: Task-Specific Model Pruning via Gram Anchoring Subspace Consistency</a></td><td>32</td><td>1</td><td>Efficient</td><td>Gram anchoring 기반 ViT pruning임. 효율화 incremental함</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2608.28378'>PersonaForge: Realistic Multi-Turn User Simulation for Agentic Systems</a></td><td>32</td><td>1</td><td>NLP</td><td>실제 세션 분석 기반 다중 턴 사용자 시뮬레이션임. 로봇 관련성 낮음</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2608.28062'>WeAgent-MMSearch: Native Text-Vision Interaction for Multimodal Search Agents</a></td><td>32</td><td>1</td><td>Multimodal</td><td>멀티모달 검색 agent의 텍스트-비전 상호작용 환경으로 웹 검색 중심임.</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2608.27668'>Report Supervision</a></td><td>32</td><td>0</td><td>Medical</td><td>보고서를 supervision으로 쓰는 의료 segmentation 연구임. 로봇 무관함</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2608.27821'>How do features act in an individual prediction? Separating standalone and interaction effects with a case-based taxonomy</a></td><td>32</td><td>0</td><td>LG</td><td>개별 예측에서 특징 효과를 분류하는 XAI taxonomy로 로봇과 무관함</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2608.27948'>Temporal Memory-Aware Online Test-Time Adaptation on Dynamic Graphs</a></td><td>32</td><td>0</td><td>LG</td><td>동적 그래프 test-time adaptation에 temporal memory를 넣은 증분적 기법임</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2608.28308'>Deriving Scaling Laws for OpenEuroLLM Models: Learning Rate, Batch Size and Loss</a></td><td>32</td><td>0</td><td>NLP</td><td>OpenEuroLLM scaling law 도출로 실무적이나 로봇과 무관함</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2608.28442'>Curvature-Conditioned Multiscale Momentum with Sphere Constraints for LLM Pretraining</a></td><td>32</td><td>0</td><td>LG</td><td>곡률 조건 multiscale momentum optimizer로 LLM pretraining 개선임</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2608.28547'>DARTS: Decoder-Aware Representation Tuning via Surgery for Model Merging</a></td><td>32</td><td>0</td><td>NLP</td><td>모델 병합의 representation bias를 decoder 인지로 보정하는 증분 기법임</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2608.27756'>Load-Bearing Context: The Question Damage Score for Evaluating Context Reliance in Linguistic Reasoning</a></td><td>32</td><td>0</td><td>NLP</td><td>언어 올림피아드 퍼즐로 문맥 의존도를 측정하는 점수를 제안함. 흥미로우나 로봇 무관함</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2608.28229'>Stay Within Your Bounds: Distance-Guided Decoding for Guaranteed Context-Free Grammar Compliance</a></td><td>32</td><td>0</td><td>NLP</td><td>CFG 준수 보장 distance-guided decoding으로 구조화 출력 기법임.</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2608.28154'>From Small Talk to Rapport: Exploring Robot Self-Disclosure in Collaborative Tasks</a></td><td>30</td><td>5</td><td>HRI</td><td>협업 과제에서 로봇 self-disclosure의 라포 효과를 보는 HRI 사용자 연구임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2608.27971'>GAAT: Geometry-Aware Alignment Transformer for Multimodal UAV Perception</a></td><td>30</td><td>3</td><td>Multimodal</td><td>UAV 다중 센서 geometry-aware 정렬 transformer임. incremental함</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2608.28723'>Vehicle Drift Emergence: Continuous Evolution from Grip Driving to the Handling Limit via Boundary Exploration Learning Model Predictive Control</a></td><td>30</td><td>3</td><td>Control</td><td>학습 MPC로 grip 주행에서 drift로의 연속 전이를 다룸. 차량 제어 특화라 로봇 학습과 거리 있음</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2608.27988'>Predicting Turn-Taking Outcomes in Multi-Party Conversation: Interpretable Modelling of Speech and Gaze Dynamics with Interpersonal Closeness</a></td><td>30</td><td>3</td><td>HRI</td><td>음성과 시선으로 다자 대화 turn-taking을 예측함. HRI와 약하게 연결됨</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2608.27843'>Synthetic Linguistic Agency: How an Embodied Mortal Agent Learns Linguistic Affordances through Consequential Social Experience</a></td><td>30</td><td>2</td><td>Embodied AI</td><td>죽을 수 있는 embodied 에이전트의 언어 affordance 학습을 개념적으로 다룸. 실증 약함</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2608.28384'>MAP: A Benchmark on Multimodal Accessibility Planning for Real World Places</a></td><td>30</td><td>2</td><td>Multimodal</td><td>접근성 요구 장소 방문 계획 멀티모달 benchmark로 평가 중심임.</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2608.27610'>ShiftSplit-AD: Separating Domain Shift from Defects in Foundation-Feature Visual Anomaly Detection</a></td><td>30</td><td>1</td><td>CV</td><td>domain shift와 결함을 분리하는 anomaly detection 개선임. 로봇 관련성 낮음</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2608.28219'>RASA: Disentangled Spatial-Motional Priors for Cross-Identity Character Animation</a></td><td>30</td><td>1</td><td>Video</td><td>공간과 모션 prior 분리 캐릭터 애니메이션임. 생성 incremental함</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2608.27662'>Unsupervised Continual Learning with Growing Self-Organizing Maps and Synthetic Replay</a></td><td>30</td><td>1</td><td>LG</td><td>growing SOM과 합성 replay로 exemplar-free continual learning을 하나 증분적임</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2608.27646'>If Agents Were Angels, No Governance Would Be Necessary: Out-of-Band Policy Enforcement at a Trusted Tool Boundary</a></td><td>30</td><td>1</td><td>AI Safety</td><td>도구 경계에서 정책을 대역 외로 강제하는 에이전트 거버넌스 방식임. 시스템 설계 위주임</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2608.27818'>AcCoRD: Evaluating User-Agent Collaboration Under Realistic User Preference Dynamics</a></td><td>30</td><td>1</td><td>AI</td><td>변하는 사용자 선호 하에서 협업을 평가하는 benchmark임. 로봇 관련성 낮음</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2608.28011'>Coverage, Not Credit: Failure-Credit Routing of Zeroth-Order Perturbation Budgets Does Not Improve On-Pool Sample Efficiency for LLM Agents</a></td><td>30</td><td>1</td><td>LLM Agent</td><td>실패 credit 라우팅이 sample efficiency를 높이지 못한다는 부정적 결과 위주임.</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2608.28145'>Dual-Stream Semantic Guidance with Prototype Anchor Calibration for Source-Fully-Free Adaptation of Vision-Language Models</a></td><td>30</td><td>0</td><td>Multimodal</td><td>source-free VLM domain adaptation임. 로봇 무관함</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2608.28567'>GeBDA: Building Damage Assessment as Text-Based Sequence Prediction</a></td><td>30</td><td>0</td><td>Remote Sensing</td><td>VLM으로 건물 피해 평가를 text 예측으로 풀이함. 응용임</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2608.27715'>Beyond Non-IID: Learner--Client Distribution Mismatch in Federated Learning</a></td><td>30</td><td>0</td><td>LG</td><td>federated learning에서 learner-client 분포 불일치를 정식화함. 로봇 연결 없음</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2608.27883'>Beyond Pairwise Graphs in Science: Hypergraph Adaptive Wavelet Operators for Parametric PDEs</a></td><td>30</td><td>0</td><td>LG</td><td>hypergraph wavelet operator로 PDE를 푸는 과학 ML 연구로 로봇과 무관함</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2608.27658'>When Tokenizers Fail: Byte-Level Chunking for Zero-Shot Transfer to Low-Resource Languages</a></td><td>30</td><td>0</td><td>NLP</td><td>byte-level chunking으로 저자원 언어 zero-shot 전이를 다룸. 로봇 관련성 없음</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2608.27729'>Below the Noise Floor: Bimodal Seed Collapse and Distinct Failure Modes in Small-Model Knowledge Distillation</a></td><td>30</td><td>0</td><td>NLP</td><td>소형 모델 지식 증류의 seed 분산 분석임. 특정 과제 한정이고 로봇 무관함</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2608.28478'>Blind Men and the Elephant: Probing the Epistemic Myopia of LLMs under Long-Tail Divergent Knowledge</a></td><td>30</td><td>0</td><td>NLP</td><td>장꼬리 사실의 상이한 설명을 탐지하는 benchmark임. 로봇 무관함</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2608.27839'>KLOD: Locality-Preserving Knowledge Editing via Non-Target Distribution Preservation</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM knowledge editing의 locality 보존용 loss 개선으로 incremental하며 로봇과 무관함.</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2608.27857'>SpikeOPD: Stable On-Policy Distillation for Autoregressive Spiking Language Models</a></td><td>30</td><td>0</td><td>LLM</td><td>spiking LM 대상 on-policy distillation 안정화로 로봇 관련성 낮음.</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2608.27869'>See, Hypothesize, Validate: Multimodal Agentic Framework for Discovering Governing PDEs</a></td><td>30</td><td>0</td><td>LG</td><td>PDE 발견용 멀티모달 agent 프레임워크로 과학 응용임.</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2608.27984'>When Evidence Shapes Collaboration: Knowledge-Conditioned Topology Generation for Multi-Agent Systems</a></td><td>30</td><td>0</td><td>LLM Agent</td><td>multi-agent topology 생성에 지식 조건을 넣은 방법임.</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2608.28256'>Physics-Guided Flow Matching for CT Image Reconstruction</a></td><td>30</td><td>0</td><td>CV</td><td>CT 재구성에 physics-guided flow matching을 쓴 의료 영상 생성 모델 응용임.</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2608.28361'>GRACE:Gradient-guided Coreset Selection for LLM Unlearning</a></td><td>30</td><td>0</td><td>LLM</td><td>gradient 기반 coreset으로 LLM unlearning 데이터 선택함.</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2608.28447'>Learning to Use Tools: Reinforcement Learning for Tool-Integrated Mathematical Reasoning</a></td><td>30</td><td>0</td><td>RL</td><td>계산기 도구 통합 수학 추론 RL 적용임.</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2608.28725'>Beyond the Answer Key: Robustness Evaluation of Large Language Models for Step-Level Mathematical Verification</a></td><td>30</td><td>0</td><td>LLM</td><td>수학 단계 검증 LLM 강건성 평가임.</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2608.28343'>Denoising-Aware Temporal Point Cloud Completion for 3D Crop Architecture Recovery and Phenotypic Trait Extraction</a></td><td>28</td><td>3</td><td>3D Vision</td><td>작물 point cloud 시간 completion임. 농업 응용임</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2608.28218'>Focus Where It Counts: A Salience-Driven Vision-Language Model for Low Vision Assistance</a></td><td>28</td><td>1</td><td>Multimodal</td><td>저시력 보조용 salience VLM임. 응용임</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2608.27847'>Beyond Uncertainty Reduction: Calibrated Planning for Interactive Diagnosis</a></td><td>28</td><td>1</td><td>LLM Agent</td><td>대화형 진단 질문 계획에 calibration을 넣은 도메인 응용임.</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2608.27886'>Resource Constraints and Performance in Agentic AI Systems</a></td><td>28</td><td>1</td><td>LLM Agent</td><td>agentic system의 자원 제약과 성능 관계 분석으로 실증 위주임.</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2608.27969'>openJiuwen: Beyond Static Harnesses for Long-Horizon Coding Agents</a></td><td>28</td><td>1</td><td>LLM Agent</td><td>장기 coding agent 하네스 설계로 엔지니어링 성격이 강함.</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2608.28271'>RECAST: Recent &amp; Context-Aware Sampling for Test-Time Adaptation in Streaming Biosignals</a></td><td>28</td><td>1</td><td>LG</td><td>생체신호 test-time adaptation 샘플링 개선으로 도메인 한정임.</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2608.27877'>Relational Knowledge Distillation Brings DNN Representations Close Enough to Humans to Be Aligned Without Supervision</a></td><td>28</td><td>0</td><td>Representation</td><td>relational distillation으로 DNN 표현을 인간과 정렬함. 로봇 무관함</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2608.28517'>Learning the Target Priors Before Image Translation: A Decoupled Training Paradigm for Cross-Modal Image Translation in Remote Sensing</a></td><td>28</td><td>0</td><td>Remote Sensing</td><td>target prior 선학습 후 cross-modal 변환함. 로봇 무관함</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2608.28184'>Biologically Inspired Mechanisms for Facilitating Grokking in Multilayer Perceptrons</a></td><td>28</td><td>0</td><td>LG</td><td>grokking을 돕는 생물학적 메커니즘 탐색으로 소규모 MLP 실험임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2608.28198'>Performative Privacy: When Differential Privacy Maximizes Utility</a></td><td>28</td><td>0</td><td>LG</td><td>performative learning 관점에서 차등 프라이버시 효용을 이론화함</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2608.27816'>PersonaEdit: Representative Sample Selection for Personalized Model Editing</a></td><td>28</td><td>0</td><td>NLP</td><td>개인화 모델 편집을 위한 대표 샘플 선택법임. 증분적이고 로봇 무관함</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2608.28432'>Are These Modules Worth Their Cost? A Paradigm-Level Accuracy-Cost Analysis of In-context Learning Text-to-SQL</a></td><td>28</td><td>0</td><td>NLP</td><td>ICL text-to-SQL 모듈별 정확도-비용 분석임. 로봇 무관함</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2608.27831'>RealSWE: A Compositional Evaluation of Coding Agents under Realistic User Requests</a></td><td>28</td><td>0</td><td>AI</td><td>현실적 사용자 요청 하의 코딩 에이전트 평가임. 로봇 무관함</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2608.28233'>REINS: Refusal-Enhanced Inhibitory Steering with Sparse Autoencoder Features</a></td><td>28</td><td>0</td><td>LLM Safety</td><td>SAE 특징 기반 refusal steering으로 LLM 안전 기법임.</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2608.28281'>LoopArena: Benchmarking Models as Runtime Controllers for Loop Engineering</a></td><td>28</td><td>0</td><td>LLM Agent</td><td>coding agent runtime controller 벤치마크임.</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2608.28511'>Training Communication-Efficient Mixture-of-Experts Language Models with Layer Re-Configuration</a></td><td>28</td><td>0</td><td>Efficient Training</td><td>MoE 학습 통신 효율용 layer 재구성 시스템 최적화임.</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2609.00032'>EULER: Exploring Underused Links with Evidence-Checked Return for Multi-Agent Mathematical Discovery</a></td><td>28</td><td>0</td><td>LLM Agent</td><td>수학 발견 multi-agent 시스템임.</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2608.28439'>Fidelity Is Not Enough: Dispatch-Level Instrumentation for Agentic Datasheet Extraction</a></td><td>26</td><td>1</td><td>NLP</td><td>데이터시트 추출의 도구 호출 trace 기반 계측을 주장함. 로봇 무관함</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2608.28458'>Acquire, Repair, Preserve: A Diagnosis-Guided Post-Training Recipe for Small-Model Dialogue Game Agents</a></td><td>26</td><td>1</td><td>NLP</td><td>진단 기반 후처리로 소형 대화 게임 에이전트를 개선함. 일반성 낮음</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2608.28165'>CrabOS: An Operating System for Human-AI Co-inhabitation</a></td><td>26</td><td>1</td><td>LLM Agent</td><td>인간-AI 공존 OS 개념 제안으로 시스템 비전 위주임.</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2608.27844'>EvoHarmBench: Breaking Content Moderation with Iterative Human-Like Evasion</a></td><td>26</td><td>0</td><td>NLP</td><td>반복 회피 방식의 콘텐츠 검열 우회 benchmark임. 로봇 무관함</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2608.27974'>QUORUM: QUality-Optimized Routing Using Multiple annotators</a></td><td>26</td><td>0</td><td>NLP</td><td>다중 annotator 비용 대비 품질 라우팅 방법임. 로봇 무관함</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2608.28151'>Nested Byte-Level Vocabularies Are Cheap to Deploy and Expensive to Share: A Pre-Registered Negative Result</a></td><td>26</td><td>0</td><td>NLP</td><td>nested byte-level 어휘의 사전 등록 부정 결과임. 정직하나 영향 작음</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2608.28467'>Stranger, Fan, or Peer? A Systematic Study on the Role of Interlocutor in Persona-Based Dialogue Generation</a></td><td>26</td><td>0</td><td>NLP</td><td>페르소나 대화에서 상대방 역할을 체계적으로 연구함. 로봇 무관함</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2608.28247'>A comprehensive and trustworthy benchmark of AI methods for change detection in Earth observation</a></td><td>25</td><td>1</td><td>Remote Sensing</td><td>change detection benchmark임. 로봇 무관함</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2608.28142'>Conditional Diffusion Models for Energy-Efficient Driving</a></td><td>25</td><td>1</td><td>LG</td><td>에너지 효율 주행 예측에 conditional diffusion을 적용한 응용임</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2608.28065'>Learning to Allocate Incentives for Incentivized Advertising via Offline Model-Based Reinforcement Learning</a></td><td>25</td><td>1</td><td>RL</td><td>광고 보상 배분용 offline model-based RL 응용임.</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2608.28295'>Memristive-Friendly Hadamard Reservoir Computing: Structured, Multiplier-Free Recurrences at Scale</a></td><td>25</td><td>1</td><td>LG</td><td>memristive 하드웨어용 Hadamard reservoir computing임.</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2608.27753'>What Can Low Resource Languages Learn From Each Other?</a></td><td>25</td><td>0</td><td>Multimodal</td><td>저자원 언어 간 VLM 전이 분석임. 로봇 무관함</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2608.27893'>CommerceVibe: Learning to Design E-Commerce Creatives as Executable Visual Code via Dual-Feedback Reinforcement Learning</a></td><td>25</td><td>0</td><td>Generative</td><td>이커머스 creative를 코드로 생성하는 RL임. 로봇 무관함</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2608.28191'>EXPOSE: Explainable and Domain-Robust Embeddings from Pathology Vision Foundation Models using Sparse Autoencoders</a></td><td>25</td><td>0</td><td>Medical</td><td>병리 VFM 임베딩에 sparse autoencoder를 적용함. 로봇 무관함</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2608.28302'>FUSED: Forensic-Semantic Mixture-of-Experts for AI Inpainting Detection and Localization</a></td><td>25</td><td>0</td><td>CV</td><td>AI inpainting 검출용 mixture-of-experts임. 로봇 무관함</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2608.27574'>Self-Explainable Multi-Label Graph Neural Network for Correlated Evidence Attribution</a></td><td>25</td><td>0</td><td>LG</td><td>다중 label 그래프 신경망 증거 귀속임. 로봇 무관함</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2608.27634'>Curvature-Aware Radius Shrinkage for Adaptive Nearest Neighbor Classification</a></td><td>25</td><td>0</td><td>LG</td><td>k-NN 반경을 곡률에 맞춰 조절하는 고전적 분류 기법으로 로봇과 무관하고 증분적임</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2608.28007'>Exact Risk Ratios for Weighted Data Selection in Linear Regression</a></td><td>25</td><td>0</td><td>LG</td><td>선형 회귀 데이터 선택의 정확한 위험비를 구하는 순수 이론임</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2608.28052'>Explainable Uncertainty Estimation for Reliable Medical AI</a></td><td>25</td><td>0</td><td>LG</td><td>의료 AI용 설명 가능 불확실성 추정으로 증분적임</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2608.28482'>How Proper Scoring Rules Shape LLM Forecasting</a></td><td>25</td><td>0</td><td>NLP</td><td>proper scoring rule별 LLM 예측 성능 비교 평가임</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2608.28557'>Blog: Survey of Optimizers</a></td><td>25</td><td>0</td><td>LG</td><td>optimizer 설문 블로그 글로 신규 기여는 없음</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2608.27945'>Cross-Session Decomposition Attacks: Scaling Risk and Intent-Aligned Retrieval Defense</a></td><td>25</td><td>0</td><td>LLM Safety</td><td>cross-session 분해 공격과 방어로 안전 주제이나 로봇과 무관함.</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2608.28067'>SEPO: Evidence-Grounded Prompt Optimization via Structural Editing</a></td><td>25</td><td>0</td><td>NLP</td><td>구조적 편집 기반 prompt 최적화로 incremental함.</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2608.28475'>COVER: Identifiable Evaluation of Coalition Routing</a></td><td>25</td><td>0</td><td>LLM Agent</td><td>multi-agent 팀 라우팅 효과의 식별 가능 평가 방법임.</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2608.27794'>Node-wise Feature Encoding for Neural Performance Prediction</a></td><td>24</td><td>0</td><td>LG</td><td>NAS용 지연 시간 예측기의 노드 단위 인코딩으로 증분적임</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2608.27813'>Representation of syntax in LLMs through the lens of linear distance and similarity-aware entropy</a></td><td>24</td><td>0</td><td>NLP</td><td>structural probe를 라벨별로 분해해 통사 표현을 분석함. 로봇 무관함</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2608.28009'>Beyond Global Scalars: Synergizing Token-Level Statistics and Deep Semantics for Adversarial AIGC Text Detection</a></td><td>24</td><td>0</td><td>NLP</td><td>토큰 통계와 의미를 결합한 AIGC 텍스트 탐지임. 증분적이고 로봇 무관함</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2608.28481'>NL2AGBench: Benchmarking LLM Auto-Formalization for AlphaGeometry</a></td><td>24</td><td>0</td><td>NLP</td><td>AlphaGeometry용 자동 형식화 benchmark임. 로봇 무관함</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2608.28334'>Real-Valued Hyperdimensional Sequence Representations with Hadamard Product Binding and Shift Equivariance</a></td><td>24</td><td>0</td><td>LG</td><td>hyperdimensional 시퀀스 표현에 Hadamard binding을 쓴 이론적 소품임.</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2608.28341'>Cross-Spectral Dense Correspondence for Multimodal Spectral Medical Imaging</a></td><td>22</td><td>1</td><td>Medical</td><td>다중 스펙트럼 의료 영상 dense 대응임. 도메인 특화임</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2608.27672'>First Make It Playable, Then Make It Good: Staged Interaction Learning for Small Dialogue-Game Agents</a></td><td>22</td><td>1</td><td>NLP</td><td>2B 모델의 단계적 SFT로 대화 게임 점수를 올린 챌린지 기술 보고임. 일반성 낮음</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2608.27942'>CASTANET: Causality-Aware Spatio-Temporal Adversarial Network Using Traffic Incident Effects</a></td><td>22</td><td>1</td><td>LG</td><td>교통 사고 혼잡 예측에 인과 인식 네트워크를 쓴 응용임.</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2608.27879'>What Do Interaction Representations Actually Measure? Pre-Event Separability in Weakly-Supervised Violence Detection</a></td><td>22</td><td>0</td><td>CV</td><td>폭력 검출에서 interaction 표현 분석임. 로봇 무관함</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2608.28063'>A Controlled Audit of Architectural Complexity in Uncertainty-Aware Multi-Organ Ultrasound Classification</a></td><td>22</td><td>0</td><td>Medical</td><td>초음파 분류 구조 복잡도 audit임. 로봇 무관함</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2608.27704'>RiskBlend: A Multi-Signal Framework for Test Input Prioritization in Machine Learning Regression Testing</a></td><td>22</td><td>0</td><td>LG</td><td>재학습 분류기의 회귀 결함 테스트 입력 우선순위화로 로봇과 무관함</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2608.28003'>A Method for Layer Bit-Width Allocation in LLM Quantization via Performance Maximization Under a Quality-Degradation Constraint</a></td><td>22</td><td>0</td><td>NLP</td><td>Gemma-3-1B 레이어별 bit-width 할당의 소규모 양자화 기법임</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2608.28134'>Learning to Difference: Adaptive Reversible Differencing (AdaRDiff) for Time Series Forecasting</a></td><td>22</td><td>0</td><td>LG</td><td>시계열 예측용 적응형 차분 모듈로 증분적임</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2608.28209'>Generalized Context in Cross Attention for Transfer Learning of Disjoint Tabular Data</a></td><td>22</td><td>0</td><td>LG</td><td>서로 다른 tabular 데이터 간 cross attention 전이로 증분적임</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2608.28267'>Residual-Guided Randomized Neural Networks</a></td><td>22</td><td>0</td><td>LG</td><td>잔차 유도 randomized neural network로 증분적임</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2608.28273'>Learning to Transfer Across Modes: Towards Unified Urban Mobility Forecasting</a></td><td>22</td><td>0</td><td>LG</td><td>다중 교통 수단 수요 예측 전이 학습으로 응용임</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2608.28408'>SymboLLM-FE: LLM-Accelerated Symbolic Regression for Automated Feature Engineering on Tabular Data</a></td><td>22</td><td>0</td><td>LG</td><td>LLM 기반 symbolic regression 특징 공학으로 tabular 응용임</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2608.27855'>AI Writers Have a Consistent Stylometric Footprint, but AI Editors Do Not</a></td><td>22</td><td>0</td><td>NLP</td><td>AI 작성과 편집의 문체 흔적을 비교함. 로봇 무관함</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2608.28155'>FinExam-10K: When Retrieval Helps Financial Reasoning?</a></td><td>22</td><td>0</td><td>NLP</td><td>CFA, FRM 금융 시험 benchmark임. 로봇 무관함</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2608.28283'>Embedding Models for Stance-Aware Argument Retrieval</a></td><td>22</td><td>0</td><td>NLP</td><td>입장 인식 논증 검색용 embedding 모델임. 로봇 무관함</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2608.28405'>CultureConverse: A Multilingual Multi-turn Simulation Harness for Culturally Grounded Assistance in East and Southeast Asia</a></td><td>22</td><td>0</td><td>NLP</td><td>동아시아 문화 대화 시뮬레이션 benchmark임. 로봇 무관함</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2608.27992'>GOD: Govern, Observe, and Direct - A Real-Time Control Room for Agent Societies</a></td><td>22</td><td>0</td><td>LLM Agent</td><td>agent 사회 모니터링 제어실 도구로 시스템 데모 성격임.</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2608.27713'>DART-FL: Burst-Aware Multitask Federated Learning under Dynamic Inference Demand at the Edge</a></td><td>20</td><td>1</td><td>LG</td><td>엣지 federated learning의 추론 수요 대응 스케줄링으로 증분적임</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2608.27888'>Thread-Efficient Decoding for Neural Texture Compression</a></td><td>20</td><td>0</td><td>Graphics</td><td>neural texture 압축 디코딩 효율화임. 로봇 무관함</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2608.28455'>ARC-CT: Anatomy-Routed Contrastive Vision-Language Learning for 3D Chest CT</a></td><td>20</td><td>0</td><td>Medical</td><td>흉부 CT 대조 학습임. 로봇 무관함</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2608.27791'>Initialization Is Critical: Advancing Federated Short-Term Load Forecasting under Load Heterogeneity via Model Initialization</a></td><td>20</td><td>0</td><td>LG</td><td>federated 전력 부하 예측의 모델 초기화 기법으로 응용 중심임</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2608.27856'>FedEHR-Agents: Federated Agentic Optimization for Automated EHR Modeling</a></td><td>20</td><td>0</td><td>NLP</td><td>federated agent로 EHR 모델링을 자동화하는 의료 응용임</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2608.28116'>Generalized Gibbs Ensemble Weighting for Forecast Combination</a></td><td>20</td><td>0</td><td>LG</td><td>예측 앙상블 결합 가중치 기법으로 증분적임</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2608.28188'>Beyond Flat Netlist: Hierarchical Graph Representation Learning for Scalable Analysis of Sequential Circuits</a></td><td>20</td><td>0</td><td>LG</td><td>순차 회로 netlist 계층 그래프 표현 학습으로 EDA 응용임</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2608.28236'>D-TAIA: Domain-Aware LLM Adaptation for Multi-Task Predictive Process Monitoring</a></td><td>20</td><td>0</td><td>NLP</td><td>업무 프로세스 모니터링용 도메인 인지 LLM 적응으로 응용임</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2608.28237'>Efficient Online Continual Foundation Model Fine-Tuning for Predictive Process Monitoring</a></td><td>20</td><td>0</td><td>NLP</td><td>프로세스 모니터링용 온라인 continual fine-tuning으로 응용임</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2608.27902'>LandingAgent: A Reference-Annotated Dataset and Agentic Generation Framework for Landing Pages</a></td><td>20</td><td>0</td><td>NLP</td><td>랜딩 페이지 데이터셋과 에이전트 생성 프레임워크임. 응용 위주이고 로봇 무관함</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2608.28040'>A Shaky Voice Is Not Always a Dodge: Benchmarking Textual and Vocal Evasion Detection in Earnings Calls</a></td><td>20</td><td>0</td><td>NLP</td><td>실적 발표의 텍스트와 음성 회피 탐지 benchmark임. 로봇 무관함</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2608.28053'>CNeo-Bench: Diagnosing Large Language Models on Chinese Neologisms</a></td><td>20</td><td>0</td><td>NLP</td><td>중국어 신조어 이해 benchmark임. 로봇 무관함</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2608.28407'>A Unified Framework to Elicit Structured Feedback for Interpretable Multi-Trait Essay Scoring</a></td><td>20</td><td>0</td><td>NLP</td><td>다중 특성 에세이 채점 프레임워크임. 로봇 무관함</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2608.28508'>Phoneme- and Word-Level Metrics Using Self-Supervised Speech Representations for Forced Alignment Evaluation</a></td><td>20</td><td>0</td><td>Speech</td><td>SSL 음성 표현 기반 forced alignment 평가 지표임. 로봇 무관함</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2608.27910'>AI Alignment through a Game-theoretic Lens: A Survey</a></td><td>20</td><td>0</td><td>LLM</td><td>게임이론 관점 alignment 서베이로 로봇과 무관함.</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2608.28027'>String: An Agentic OS Where Every App Is a Markdown File</a></td><td>20</td><td>0</td><td>LLM Agent</td><td>markdown 기반 agent OS 시스템 제안으로 로봇과 무관함.</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2608.28553'>Four conditions for composing plugin-based agents without a host agents</a></td><td>20</td><td>0</td><td>LLM Agent</td><td>plugin 기반 agent 합성 조건 논의로 시스템 설계임.</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2609.05498'>Observability Analysis of Joint Steering and Extrinsic Calibration</a></td><td>18</td><td>3</td><td>State Estimation</td><td>차량 조향과 LiDAR 외부 보정의 observability 분석 기술 보고서임. 학습 요소 없고 novelty 낮음</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2608.27633'>Depth-Aware Pothole Detection Using YOLO and RT-DETR at the Edge</a></td><td>18</td><td>2</td><td>CV</td><td>YOLO/RT-DETR 포트홀 검출 응용 연구임. 단순 엔지니어링임</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2608.27989'>GAN-Based Semantic Communication for Image Transmission in IoV</a></td><td>18</td><td>1</td><td>Communication</td><td>GAN 기반 semantic communication임. 로봇 관련성 낮음</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2608.28371'>Real-Time Musculoskeletal Surrogates for Pediatric Cerebral Palsy: a Credibility Pilot</a></td><td>18</td><td>1</td><td>Medical</td><td>뇌성마비 근골격 surrogate 파일럿임. 도메인 특화임</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2608.27840'>An Empirical Evaluation of Cross-City POI Recommendation on a Large-Scale Benchmark</a></td><td>18</td><td>1</td><td>LG</td><td>POI 추천 벤치마크 재평가 실증 연구로 로봇과 거리 멂.</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2608.27923'>PCBnet: A Dataset and Automatic Construction of SPICE Netlists from Schematic Images</a></td><td>18</td><td>0</td><td>Dataset</td><td>PCB 회로도의 netlist 데이터셋임. 로봇 무관함</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2608.28248'>Synth-JDoc: Synthesizing a Japanese Document Image Dataset for OCR with Diverse Layouts and Embedded Images</a></td><td>18</td><td>0</td><td>OCR</td><td>일본어 문서 OCR 합성 데이터셋임. 로봇 무관함</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2608.28568'>SignRR: Retrieve and Refine Real Motion for Sign Language Production</a></td><td>18</td><td>0</td><td>Generation</td><td>수어 모션 retrieve-refine 생성임. 로봇 무관함</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2608.27719'>Leveraging a Foundation Model for the EEG-Based Diagnosis of Alzheimer&#x27;s Disease</a></td><td>18</td><td>0</td><td>LG</td><td>EEG 파운데이션 모델을 알츠하이머 진단에 적용한 응용 연구임</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2608.27931'>TI$^2$PS: A Topology-Informed Inverse Design Framework for Stochastic Multicellular Pattern Formation</a></td><td>18</td><td>0</td><td>LG</td><td>다세포 패턴 inverse design 프레임워크로 도메인 특화 응용임</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2608.28042'>SimpCue: Cue-Based Prompting for Multilingual Text Simplification</a></td><td>18</td><td>0</td><td>NLP</td><td>언어학적 cue 프롬프팅으로 다국어 문장 단순화를 시도함. 증분적임</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2608.28170'>Text Restoration of Ancient Documents with Language Models</a></td><td>18</td><td>0</td><td>NLP</td><td>언어 모델로 고문서 결손 텍스트를 복원함. 로봇 무관함</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2609.00329'>The Curse of Multilinguality in Lexical Normalization</a></td><td>18</td><td>0</td><td>NLP</td><td>어휘 정규화에서 다국어 학습의 저주를 분석함. 로봇 무관함</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2608.27716'>PCFBench: A Diagnostic Benchmark for Product Carbon Footprint Estimation</a></td><td>18</td><td>0</td><td>AI</td><td>제품 탄소발자국 추정 진단 benchmark임. 로봇 무관함</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2608.27919'>From Documents to Reasoning: A Validated Synthetic Data Pipeline and Semantic-Aware Fine-Tuning for Financial Numerical Reasoning</a></td><td>18</td><td>0</td><td>NLP</td><td>금융 수치 추론용 합성 데이터와 fine-tuning으로 dataset 중심 기여임.</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2609.00330'>Topic Matching in the Wild: Benchmark and Lessons from Real-World ASR Transcripts</a></td><td>16</td><td>0</td><td>NLP</td><td>콜센터 ASR 전사 주제 매칭 benchmark임. 로봇 무관함</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2608.28070'>CF-YOLO: Context-Aware Feature Refinement for Camouflaged Industrial Micro-Defect Detection</a></td><td>15</td><td>1</td><td>CV</td><td>산업 미세 결함 검출 YOLO 변형임. 단순 엔지니어링임</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2608.28339'>Abstract4D: A Large-Scale Dataset and Framework for Understanding the Visual Language of Abstract Art</a></td><td>15</td><td>0</td><td>CV</td><td>추상 미술 이해 데이터셋임. 로봇 무관함</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2608.27978'>PhyMamba: Physics-Modulated Mamba for Robust Battery Health Prognostics</a></td><td>15</td><td>0</td><td>LG</td><td>배터리 수명 예측용 physics-modulated Mamba로 응용 연구임</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2608.28084'>Comparing Classical and Quantum Machine Learning for Regression in High Energy Physics Collision Data</a></td><td>15</td><td>0</td><td>LG</td><td>고에너지 물리에서 고전/양자 ML 회귀 비교로 로봇과 무관함</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2608.28499'>REPLICANT: Learning Policies for Evading and Hardening Malware Detectors</a></td><td>15</td><td>0</td><td>LG</td><td>멀웨어 탐지기 회피 및 강화 정책 학습으로 로봇과 무관함</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2608.28552'>Advancing Interaction-Sensitive Feature Selection: Novel Relief-Based Algorithms, Expanded Comparisons, and Recommendations for Biomedical Data Mining</a></td><td>15</td><td>0</td><td>LG</td><td>생의학 데이터 Relief 기반 feature selection으로 로봇과 무관함</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2608.28144'>The Shape of Power: A Multilingual Framework for Social Power Reasoning in Dialogues</a></td><td>15</td><td>0</td><td>NLP</td><td>다국어 사회적 권력 추론 데이터와 프레임워크임.</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2608.28178'>Expert Knowledge &amp; Machine Understanding: Bridging Reactome&#x27;s Ontology with LLM Semantic Embeddings</a></td><td>15</td><td>0</td><td>NLP</td><td>Reactome 온톨로지와 LLM 임베딩 결합 생물 응용임.</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2608.28315'>MAIL: Memory-driven, Adaptive, Incremental, and Literature-grounded Framework for Hypothesis Generation in Chemistry</a></td><td>15</td><td>0</td><td>LLM Agent</td><td>화학 가설 생성용 메모리 기반 프레임워크 응용임.</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2608.28433'>Prove2Me: An Open Collaborative Platform for Scaling Math Formalization</a></td><td>15</td><td>0</td><td>LLM</td><td>Lean 형식화 협업 플랫폼 시스템임.</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2608.28329'>BanglaMed-QA: A Question Answering System for Healthcare Support in Bangla</a></td><td>14</td><td>0</td><td>NLP</td><td>벵골어 의료 QA 시스템임. 로봇 무관함</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2608.27671'>A Framework for Object-Centric Predictive Monitoring of Collaborative Processes</a></td><td>14</td><td>0</td><td>AI</td><td>협업 프로세스 예측 모니터링용 object-centric 프레임워크임. 로봇 무관함</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2608.27824'>Evidential-Based Higher-Order Set Argumentation Framework</a></td><td>14</td><td>0</td><td>AI</td><td>증거 기반 고차 논증 프레임워크의 형식 이론임. 로봇 무관함</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2608.28360'>Propagating construction-time knowledge quality into medical question answering: A framework grounded in clinical guidelines</a></td><td>14</td><td>0</td><td>NLP</td><td>임상 지침 KG 품질을 의료 QA에 전파하는 도메인 응용임.</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2608.28399'>RetailAgent: Structured Adverse Timing in Self-Conditioned Multimodal LLM Trading Agents</a></td><td>14</td><td>0</td><td>LLM Agent</td><td>LLM 트레이딩 agent 불리한 타이밍 분석 금융 응용임.</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2608.28402'>VERA-8B: Evidence-Grounded Audit Risk Reasoning from SEC Filings</a></td><td>14</td><td>0</td><td>NLP</td><td>SEC 공시 기반 감사 위험 추론 8B 모델 도메인 응용임.</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2608.27688'>SafeStep: An Interactive Demonstration of Semantic Communication for Pedestrian Safety Monitoring</a></td><td>12</td><td>1</td><td>CV</td><td>보행자 안전 semantic communication 데모로 연구 기여가 작음</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2608.28195'>UniLipi: A Unified Multi-Script OCR for Historical Indic Manuscripts</a></td><td>12</td><td>0</td><td>OCR</td><td>인도 문자 필사본 OCR임. 로봇 무관함</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2608.28207'>Explainable Diabetic Retinopathy Classification Using Vision Foundation Models</a></td><td>12</td><td>0</td><td>Medical</td><td>당뇨망막병증 설명 가능 분류 응용임</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2608.28242'>Spectral Features Dominate BCG Respiratory-Event Detection: A Large-Scale Patient-Independent Comparison of Feature Groups in Sleep Apnea Patients</a></td><td>12</td><td>0</td><td>LG</td><td>BCG 수면무호흡 이벤트 특징군 비교로 의료 신호 응용임</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2608.27966'>Lexically conditioned realization ambiguity in Korean predicate morphology</a></td><td>12</td><td>0</td><td>NLP</td><td>한국어 용언 형태론의 표면형 모호성 연구임. 로봇 무관함</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2608.27940'>A Deep Learning-Based Stacking Ensemble Framework for Turbofan Engine Remaining Useful Life Prediction</a></td><td>12</td><td>0</td><td>LG</td><td>터보팬 엔진 RUL 예측 stacking ensemble로 단순 응용임.</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2608.27999'>PhenoIntel: A Lifecycle-Aligned Multi-Agent Web Application for Verified, Accessible Plant Phenotype Analysis</a></td><td>12</td><td>0</td><td>LLM Agent</td><td>식물 표현형 분석 웹 앱으로 응용 시스템임.</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2608.28152'>Under-Mattress Temporal Sensing for Next-Day Agitation Risk Scoring in Dementia Wards</a></td><td>12</td><td>0</td><td>LG</td><td>매트리스 하부 센서 기반 치매 병동 초조 위험 예측 의료 응용임.</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2608.28228'>Generative AI Alignment with Hinduism&#x27;s Theological Plurality and Sacred Representation</a></td><td>12</td><td>0</td><td>LLM</td><td>힌두교 관점의 생성 AI alignment 논의임.</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2608.28252'>Regime-Aware Portfolio Management via Retrieval-Augmented LLM-Guided Expert Switching</a></td><td>12</td><td>0</td><td>LG</td><td>검색 증강 LLM 포트폴리오 전문가 전환 금융 응용임.</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2608.28161'>Empowering Local Agriculture: A Deep Learning-Powered Web System for Identifying Bangladeshi Mango Varieties</a></td><td>10</td><td>0</td><td>CV</td><td>망고 품종 분류 웹 시스템임. 응용임</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2608.28453'>Prompt-Guided Interactive Segmentation of Interstitial Lung Disease in Thoracic CT</a></td><td>10</td><td>0</td><td>Medical</td><td>폐질환 CT prompt 분할임. 로봇 무관함</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2608.28461'>Anatomy-Aware Promptable Segmentation with Online Interactive Training for AUTOPET V</a></td><td>10</td><td>0</td><td>Medical</td><td>PET/CT 병변 분할 챌린지 방법임. 로봇 무관함</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2608.28524'>Texture Image Classification Using DWT AlexNet Feature Fusion and Deep Neural Networks</a></td><td>10</td><td>0</td><td>CV</td><td>DWT AlexNet 텍스처 분류임. 단순 엔지니어링임</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2608.28274'>An algebraic proof of Colombo&#x27;s difference-power determinant conjecture</a></td><td>10</td><td>0</td><td>Math</td><td>Colombo 행렬식 추측의 대수적 증명으로 ML과 무관함</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2608.27638'>Generative AI Expands the Intellectual Reach of Course Based Undergraduate Research Experiences (CUREs)</a></td><td>10</td><td>0</td><td>AI</td><td>GenAI를 학부 연구 수업에 쓴 교육 연구임. 로봇 무관함</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2608.27998'>Automated Analysis Framework for Multilingual Climate-Health Literature Based on Multi-Agent Large Language Model</a></td><td>10</td><td>0</td><td>NLP</td><td>기후-건강 문헌 분석 multi-agent 응용임.</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2608.28345'>AGENT-O: A Semantic Agent Card Framework for Interoperable and Governed Healthcare AI Agents</a></td><td>10</td><td>0</td><td>LLM Agent</td><td>의료 AI agent 카드 온톨로지 프레임워크임.</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2608.28393'>Timing-Aware Repurchase Prediction for Web-Scale E-Commerce: Survival Models for Multi-Surface Grocery Recommendation</a></td><td>10</td><td>0</td><td>LG</td><td>식료품 재구매 생존 모델 추천 응용임.</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2608.28728'>PermitGPT: A Unified Generative-AI Pipeline for Construction Hazard Forecasting, Permit Prediction, and Community Impact</a></td><td>10</td><td>0</td><td>LLM</td><td>건설 허가·위험 예측 생성형 AI 응용임.</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2608.27675'>Agents for Everyone: A Workshop Framework for Building Agentic AI Capabilities in a Distributed Curation Community</a></td><td>8</td><td>0</td><td>AI</td><td>큐레이션 커뮤니티용 에이전트 워크숍 틀임. 연구 기여 없음</td></tr>
</tbody></table>

</details>
