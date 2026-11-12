# 오늘의 arXiv Top 15: 2026-11-10 (화)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**

**신규 논문 수: 전체 966편 → 중복 제거 후 966편 (이번 평가 대상 949편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 250 |
| cs.LG | 295 |
| cs.RO | 128 |
| cs.CL | 127 |
| cs.AI | 166 |

---

## Top 15

### 1. World In-Context Learning for Agentic Robot Manipulation (82점)

[arXiv](https://arxiv.org/abs/2611.12885) · [PDF](https://arxiv.org/pdf/2611.12885) · [alphaXiv](https://www.alphaxiv.org/abs/2611.12885) (요약 있음) · [프로젝트 페이지](https://ArcheOne-AI.github.io/RoboScript) · [코드](https://github.com/ArcheOne-AI/RoboScript)

- **저자**: Heng Fang, Zehui Guo, Yuehan Zhang, Mingyang Du, Dingkang Liang, Xiang Bai
- **분야**: Manipulation · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: ByteDance 자체 양식 · 근거: 글꼴 ByteSans, 학회 양식 아님
- **읽은 원문**: PDF 전문

> 가중치를 고정한 foundation model이 시연 1개로 시작해 simulator에서 과제를 연습하고, 배운 내용을 텍스트 메모리에 적어 조작을 배움. RoboTwin 2.0 50개 과제의 평균 성공률이 83.4%로, 시연 50개로 학습한 가장 강한 action policy(61.7%)보다 높음.

**무슨 문제인가**

VLA나 world action model 같은 학습형 action policy는 조작 기술을 가중치에 저장함. 그래서 학습한 분포를 벗어나면 성능이 크게 내림. 예를 들어 FastWAM은 RoboTwin 2.0 clean 장면에서 77.8%이지만 domain randomization 장면에서는 1.9%임. 시연을 context에 넣는 in-context learning은 재학습이 필요 없지만, 다른 장면에서 녹화된 시연은 지금 눈앞의 장면에서 무슨 일이 일어날지 알려 주지 못함. 그래서 in-context 방식은 지금까지 학습형 policy만큼의 성공률을 내지 못했음.

**어떻게 푸나**

WICL(World In-Context Learning)은 in-context learning에 world의 feedback을 더한 학습 방식임. 저자들은 context에 남는 지식이 겉모습이 아니라 물체 역할과 과제 단계 같은 의미 정보라고 봄. 그래서 이 지식은 의미가 같은 다른 world로 옮겨 갈 수 있다고 주장함. 구현체 RoboScript는 먼저 coding agent가 시연을 동작 단위로 나누고 기존 API로 설명되지 않는 부분의 skill 코드를 작성함. 이어서 frozen model이 시연 1개를 읽고 Task Memory를 씀. Task Memory는 물체 역할, 단계별 workflow, 물체 부위 기준의 grasp·place 규칙, 실패 교훈을 담은 Markdown 문서임. 그다음 새 simulator 장면들에서 연습하고, 실패하면 reviewer가 메모리를 고친 뒤 그 장면이 성공할 때만 수정을 반영함. 좌표나 정답 정보는 linter가 거부하고, 행동하는 agent는 RGB-D 영상과 proprioception만 받음. 배포 때는 고정된 메모리로 처음 보는 장면에서 팔 선택, 실패 후 재시도, 완료 확인을 하며 world feedback은 받지 않음.

**결과**

- RoboTwin 2.0(양팔 조작 과제 50개, clean 장면과 질감·조명·책상 높이·방해물을 바꾼 randomized 장면)에서 과제당 시연 1개, gradient update 없이 평가함. GPT-6.1-Sol 기반 RoboScript의 평균 성공률은 83.4%(clean 83.6%, randomized 83.2%)임. 시연 50개로 학습한 4D-WAM은 61.7%(clean 81.5%, randomized 41.8%)임.
- randomized 장면은 연습에 한 번도 쓰지 않았음. randomized 성공률을 clean 성공률로 나눈 유지율이 GPT-6.1-Sol을 포함한 세 foundation model 모두 95.2%에서 100.8%이고, 학습형 policy는 최대 65.1%(π0.5)임.
- 10개 과제 ablation에서 world 없이 시연만으로 메모리를 쓰면 69.0%, 같은 시연 뒤에 simulator 연습을 더하면 78.5%임(p = 0.003). 시연 없이 지시문만으로 연습하면 56.5%로 내림.
- simulated ALOHA에서 만든 메모리를 실제 양팔 PiPER 로봇에 adapter로 옮기고 재연습 없이 과제 4개를 실행함. 과제별 10회 중 10, 7, 7, 6회 성공함.

**한계**

RoboScript는 과제·setting당 10 episode로 평가함. baseline 숫자는 100 episode로 평가한 leaderboard와 발표된 보고에서 가져와 같은 조건의 직접 비교가 아님. 학습과 1,000 episode 평가 비용이 GPT-6.1-Sol 기준 1,911 USD이고, episode당 평균 54.7회의 model 호출이 필요함. 실로봇 실험은 과제 4개이고 행동 순서를 offline으로 미리 계획해 실행했으므로 실제 장면에서의 재시도는 보이지 않음.

**누리랩 연구와의 연결**

- 배포 중 실패 후 다시 관측하고 이어서 수행하는 recovery와, reflection agent가 성공 여부만 보고 실패 원인을 진단해 guidance를 쓰는 loop가 있음. failure detection·recovery와 robot memory 연구의 비교 대상으로 쓸 수 있음.
- simulator를 policy 학습이 아니라 test-time에 context를 고치는 연습장으로 쓴 사례임. simulator 대신 world model을 연습장으로 쓰면 world model 기반 test-time optimization과 바로 이어짐.

*대표 그림: 왼쪽 위는 가중치 학습, in-context learning, 이 논문의 world in-context learning을 시연 수와 일반화 범위로 비교한 개념도임. 오른쪽은 RoboTwin 2.0 측정 결과로, 시연 1개를 쓴 RoboScript가 clean 83.6%, randomized 83.2%이고 시연 50개로 학습한 policy들은 randomized에서 46.0% 이하임.*

---

### 2. Learning Heterogeneous Tactile Representation for General Dexterous Manipulation (80점)

[arXiv](https://arxiv.org/abs/2611.12806) · [PDF](https://arxiv.org/pdf/2611.12806) · [alphaXiv](https://www.alphaxiv.org/abs/2611.12806) (요약 있음) · [프로젝트 페이지](https://technology.robbyant.com/lingbot-touch) · [코드](https://github.com/robbyant/lingbot-touch)

- **저자**: Bing Han, Yichuan Peng, Haoyu Dong, Yuanmeng Hu, Yongyi Jia, Fangjing Wang, Kecheng Zheng, Yiming Zhang 외 11명
- **분야**: Manipulation · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> 압저항·자기·광학 방식 촉각 센서 데이터 5,000시간을 한 좌표계에 모아 촉각 encoder 하나를 사전학습하고, 이 encoder를 고정한 채 기존 policy에 붙임. 실제 양팔 로봇 26개 과제에서 Diffusion Policy, π0.5 등 policy 4종의 성공률이 14~26퍼센트포인트 오름.

**무슨 문제인가**

촉각 센서는 방식마다 채널 수, taxel(촉각 센서의 측정점) 배치, 해상도, 샘플링 속도가 다름. 그래서 한 센서로 학습한 모델은 다른 센서 값을 해석하지 못하고, 센서별 데이터를 하나로 모아 대규모 사전학습을 할 수도 없었음. 기존 연구는 특정 센서와 특정 과제에 묶여 있어서 촉각이 robot learning에 얼마나 도움이 되는지 같은 표현 위에서 비교하기 어려웠음. 접촉이라는 사건 자체는 센서와 무관하므로, 센서 고유의 물리를 입력에서 떼어 내면 표현을 공유할 수 있다는 것이 저자의 출발점임.

**어떻게 푸나**

LingBot-Touch는 모든 센서의 taxel 위치를 반지름 1인 기준 손가락 끝 형상 위의 좌표계(canonical fingertip space)로 옮김. 각 token은 배열 번호 대신 시간, 손가락 번호, 3D 위치로 된 5차원 주소를 받고, 이 주소는 RoPE로만 모델에 들어감. 센서 방식별 tokenizer(2층 MLP)가 한 taxel의 연속 2 frame 값을 token 하나로 만들고, 모든 센서가 공유하는 Haptic Transformer가 이를 처리함. 학습에는 latent 예측 방식인 JEPA(joint-embedding predictive architecture)를 촉각에 맞춘 Tactile-JEPA를 씀. 이 방식은 가려진 taxel의 신호를 복원하지 않고, 전체 clip을 본 target encoder의 latent feature를 예측함. 신호 대부분이 0에 가까워 복원 loss가 배경에 끌려가는 문제를 피하려는 선택임. 가림 비율은 처음 300 step 동안 40%에서 80%로 올리고, taxel 밀도와 위치를 무작위로 바꾸는 layout augmentation을 씀. 출력은 고정된 encoder의 여러 층 feature이고, 하위 policy는 이를 추가 입력으로 받음.

**결과**

- 사전학습에 없던 자기식 센서(XHand1 손)에 encoder 가중치를 바꾸지 않고 적용함. 접촉 중심 위치 오차가 0.16mm로, 여러 센서용 기존 촉각 모델 FTP-1에 센서별 adapter를 따로 학습한 경우의 5.89mm보다 작음. 촉각만으로 같은 시점 영상 frame을 찾는 top-5 recall은 47.1% 대 6.0%임.
- 실제 양팔 dexterous hand 26개 과제에서 고정 encoder(Tiny, 5.46M 파라미터)를 Diffusion Policy, π0.5, LingBot-VLA, T-Rex에 붙임. 같은 policy에 원시 촉각 신호를 넣으면 성공률이 오른 폭이 많아야 이 encoder를 붙인 경우의 절반 정도임.
- 같은 데이터와 같은 크기로 비교하면 latent 예측이 신호 복원보다 나음. 1,000시간 사전학습에서 접촉 중심 오차가 0.90mm로, 신호를 복원하는 VAE 3.03mm와 MAE(masked autoencoder) 3.07mm보다 작음. VAE는 데이터를 4,000시간으로 늘리면 5개 과제 중 4개에서 오히려 나빠짐.
- 시뮬레이션 dexterous 과제 12개에서 이 feature로 RL을 하면 성공률이 69%임. 과제별로 학습한 CNN feature는 46%, 촉각 없이는 21%임.

**한계**

FTP-1 비교는 대칭이 아님: FTP-1은 센서별 adapter를 probe와 함께 학습하고, LingBot-Touch는 probe만 학습함. 학습 예산을 1,000시간으로 고정하면 센서 하나의 데이터만 쓴 모델이 그 센서의 공간 과제에서 더 정확하므로, 여러 센서를 섞는 대가로 공간 정밀도를 일부 잃음. probing은 손 2종에서만 함. 실로봇 실험의 policy별·과제별 수치는 본문에서 확인 불가임. 공개 예정인 것은 추론 코드와 Tiny·Small checkpoint이며 사전학습 데이터는 일부 샘플만임.

**누리랩 연구와의 연결**

- 촉각 token을 VLA(π0.5, LingBot-VLA)에 고정 encoder로 붙여 dexterous manipulation 성능을 올린 사례임. 우리 VLA에 촉각 입력을 더할 때 원시 신호 대신 쓸 사전학습 표현의 기준선이 됨.
- 접촉 힘과 접촉 위치를 고정 feature에서 바로 읽을 수 있으므로, 미끄러짐이나 과도한 힘 같은 접촉 실패를 감지하는 failure detection 신호로 시험해 볼 수 있음.

*대표 그림: 연구 구성을 그린 개요 그림으로, 위쪽은 사람 장갑과 실로봇에서 모은 압저항·자기·광학 촉각 데이터가 센서 배치와 해상도가 서로 다르고 접촉 신호가 드물다는 점을 보여 줌. 아래쪽은 촉각 이해 probing, VLA·imitation learning, 손 조작 RL 과제(펜 돌리기, 조립 등)에 encoder를 쓰는 모습임.*

---

### 3. Detecting and Explaining Robot Policy Failures from Sparse Internal Features (76점)

[arXiv](https://arxiv.org/abs/2611.10400) · [PDF](https://arxiv.org/pdf/2611.10400) · [alphaXiv](https://www.alphaxiv.org/abs/2611.10400)

- **저자**: Riad Ahmed, Sujosh Nag, Moniruzzaman Akash, Momotaz Begum
- **분야**: Failure Detection · robotics relevance 9/10 · 1차 스크리닝 74점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> VLA의 중간 activation을 sparse autoencoder로 쪼개고, 쪼갠 feature마다 검증된 이름을 붙여 실패 감지와 실패 원인 설명을 같은 feature로 함. π0.5의 LIBERO 실패 감지 AUROC가 sparse autoencoder 없이 원래 activation을 쓰는 monitor의 0.988과 비슷한 0.991이면서 오경보는 6%에서 3%로 줄어듦.

**무슨 문제인가**

VLA는 카메라 시점이나 초기 상태가 조금만 바뀌어도 실패하지만, 로봇 동작만 봐서는 policy 안에서 무엇이 잘못됐는지 알 수 없음. 예를 들어 gripper가 그릇 앞에서 일찍 닫히면, policy가 그릇 위치를 잘못 봤는지 닫기 결정을 일찍 내렸는지 구분되지 않음. SAFE 같은 기존 run-time failure detector는 정보를 점수 하나로 줄이므로 실패가 났다는 것만 알려 줌. 앞선 VLA용 sparse autoencoder 연구는 대부분의 feature가 특정 장면에만 반응한다고 보고했고, 사람이 붙인 이름을 새 episode에서 확인하지도 않았음.

**어떻게 푸나**

MIND(Mechanistic Interpretability for Neural Diagnosis)는 policy를 고정한 채 중간 layer의 activation을 읽음. 이미지 patch, 단어, action 위치가 모두 같은 dictionary를 쓰는 sparse autoencoder를 학습함. 이것으로 각 activation을 소수만 켜지는 basis feature들의 합으로 나눔. 이름은 미리 정한 concept 목록(gripper 상태, 물체 잡힘·들림, 과제 단계 같은 state concept과 각 축 이동 방향, gripper 명령 같은 decision concept)에서 고름. feature가 켜질 때 concept이 참인 비율(precision)과 concept이 참일 때 feature가 켜지는 비율(recall)이 기준을 넘는 것만 이름을 받고, held-out episode에서 다시 통과해야 유지됨. decision concept은 해당 feature 값을 closed loop로 크게 고정(clamp)했을 때 로봇 행동이 이름대로 바뀌는지 확인함. 실행 중에는 이름 붙은 feature마다 켜짐 여부, 길이가 다른 창 세 개의 running mean, on/off 전환율을 모아 logistic model로 실패 점수를 냄. 점수가 선형이므로 성공 episode 평균에서 벗어난 정도를 concept별로 나눠 책임 concept을 고르고, Qwen2.5-7B-Instruct가 이를 짧은 진단문으로 씀.

**결과**

- 이름 검증: OpenVLA에서 처음 보는 초기 상태와 처음 보는 과제에서도 precision 0.9 이상으로 유지되는 이름이 decision·state 양쪽에서 나옴. 같은 규칙을 raw activation 좌표, feed-forward neuron, random direction, 학습 안 된 policy에 적용하면 concept을 하나도 이름 붙이지 못함.
- closed-loop clamp: OpenVLA의 motion concept 14개 중 12개에서 이름대로 움직인 step 비율이 0.25 이하에서 0.92 이상으로 오름. 같은 크기로 clamp한 다른 feature와 random direction은 거의 바꾸지 못함. π0.5에서는 축은 맞지만 부호가 반대로 움직임(+x feature를 clamp하면 +x 비율이 0.36에서 0.06으로 내림).
- 실패 감지: π0.5 LIBERO 4개 과제에서 AUROC가 0.991로 dense activation monitor의 0.988과 구간 안에서 같음. 실패의 99%를 잡고(dense 95%) 오경보는 3%(dense 6%)이며, 실패 시점 뒤 경보까지 중앙값이 10 step(dense 25 step)임. OpenVLA의 LIBERO-Goal에서는 fused 변형이 0.97로 dense의 0.92보다 높음. fused는 named feature로 낸 세 점수(linear, 위치별, tree) 중 가장 큰 값을 씀.
- 실로봇(Franka Panda와 Inspire hand, π0.5, 과제 2개, 과제당 attempt 수 적음): stove 과제에서 미리 정한 최선 monitor가 AUROC 0.84로 실패 11번 중 8번을 오경보 1번과 함께 잡음. 기본 monitor는 dense와 named 모두 신뢰구간이 우연 수준을 포함함.

**한계**

진단문이 실패 유형을 맞히는 비율은 낮음. OpenVLA 실패 48개 중 15개, π0.5는 3분의 1 정도이며, 같은 기록을 읽는 기계적 규칙과 비슷함. concept 목록을 사람이 미리 정해야 하고, simulator나 자동 label이 그 concept의 정답을 줘야 이름을 붙일 수 있음. 실로봇은 과제 2개에 실패 기록이 짧아 감지 결과의 신뢰구간이 넓고, clamp 검증은 시뮬레이션에서만 함. 실패 복구는 다루지 않음.

**누리랩 연구와의 연결**

- failure detection과 diagnosis를 VLA 내부 feature 수준에서 한 사례임. 감지 점수를 concept별로 나눠 설명하는 구조는 failure recovery 연구에서 복구 행동을 고를 입력으로 바로 쓸 수 있음.
- clamp로 policy가 실제로 그 feature를 통해 행동하는지 확인하는 절차는, VLA 내부 표현에 대한 counterfactual 개입 실험의 기본 도구로 가져올 수 있음.

*대표 그림: 측정 결과가 아니라 MIND의 전체 구조를 그린 그림임. 고정된 policy의 activation을 sparse autoencoder로 나눈 뒤, 위쪽은 ground truth로 이름 붙이기와 clamp 검증을 보여 줌. 아래쪽은 feature 기록에서 alarm 점수, 책임 concept, 언어 모델 진단문으로 이어지는 흐름임.*

---

### 4. SWAM: Scaling World Action Models with Cross-Modal Alignment (74점)

[arXiv](https://arxiv.org/abs/2611.12870) · [PDF](https://arxiv.org/pdf/2611.12870) · [alphaXiv](https://www.alphaxiv.org/abs/2611.12870) (요약 있음)

- **저자**: Yu Zhou, Xinyuan Xia, Xuankun Yang, Yinghao Yang, Wendi Chen, Bowen Liu, Jianhan Ma, Weicheng Duan 외 3명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 76점
- **읽은 원문**: PDF 전문

> 영상과 action을 함께 예측하는 world action model을 사전학습할 때 어떤 데이터와 언어 주석을 써야 하는지 약 47,000시간 데이터로 실험해 정리함. 이 방식으로 만든 모델은 실로봇 과제 3개의 처음 보는 조건에서 평균 성공률 40.00%를 얻어 가장 강한 baseline OpenWAM의 23.33%보다 높음.

**무슨 문제인가**

World action model(WAM)은 언어 지시를 받아 앞으로의 영상과 로봇 action을 함께 예측하는 모델임. 보통 사전학습된 영상 생성 모델에서 출발하므로, 그 모델이 이미 배운 언어와 영상의 대응을 로봇 제어에 그대로 쓸 수 있다고 가정함. 그런데 action 학습을 덧붙이면 이 언어-영상 대응이 손상될 수 있음. 기존 WAM 연구는 구조와 학습 방식에 집중했고, 이 대응을 지키려면 어떤 데이터와 supervision을 써야 하는지는 따로 다루지 않았음.

**어떻게 푸나**

저자들은 일반 영상 약 10,900시간, 1인칭 영상 약 11,000시간, 자체 수집 UMI 시연 약 15,300시간, 로봇 시연 약 9,800시간을 모았음. UMI는 스마트폰과 손으로 드는 gripper를 묶은 장치로, 사람이 조작한 궤적을 로봇 end-effector와 비슷한 형식으로 기록함. 모델은 Wan2.2-TI2V-5B에서 초기화한 video DiT와 새로 만든 action DiT를 shared masked attention으로 연결한 구조임. 입력은 과거 영상, 언어 지시, 현재 양팔 end-effector 상태이고, 출력은 다음 구간의 영상과 48 step의 16차원 action임. 언어는 video branch에만 cross-attention으로 들어가고, action branch는 video branch를 거쳐서만 언어 정보를 받음. 모든 샘플은 영상 예측 loss에 쓰이고, 유효한 action이 있는 샘플만 action loss에도 쓰임. 이 틀에서 언어 주석의 상세도, 장면 정보, subtask 단위 주석, UMI action 라벨 비율, 데이터 섞는 비율을 하나씩 바꾸며 RoboTwin 2.0(양팔 시뮬레이션 조작 과제 50개)의 성능을 비교함.

**결과**

- 언어 주석: 1인칭 영상과 UMI로 20k step 사전학습한 뒤 RoboTwin Hard(깨끗한 장면으로 학습하고 배경, 조명, 카메라 위치가 바뀐 장면에서 평가) 성공률을 잼. subtask 단위 짧은 설명은 47.20%, 상세 설명은 53.52%, 상세 설명에 장면과 조명 정보를 더하면 55.04%임.
- UMI action 라벨: UMI 영상은 모두 두고 action 라벨이 붙은 궤적 비율만 0%에서 100%로 늘림. Hard 성공률이 46.72%에서 51.28%로 오름. 사람이 손으로 조작한 action도 로봇 제어 학습에 쓸모가 있다는 근거임.
- 데이터 비율: 사전학습 20k step으로 고정하고 1인칭 영상과 UMI 비율을 바꿈. 1:1이 Hard 53.84%로 가장 높고, 1인칭 영상만 쓰면 42.56%, UMI만 쓰면 51.28%임.
- 최종 모델은 RoboTwin 50개 과제에서 Easy(학습과 같은 깨끗한 장면에서 평가) 88.10%, Hard 61.56%의 성공률을 얻음. 양팔 Flexiv Rizon 4 로봇의 과제 3개(컵 쌓기, 수건 접기, 선물 상자에 넣기)를 물체나 배경을 바꾼 조건에서 과제당 30회 평가함. 평균 성공률은 40.00%로 OpenWAM의 23.33%보다 높음.

**한계**

대부분의 비교가 RoboTwin 과제당 25회 평가 한 번씩이라, 1~2퍼센트포인트 차이는 오차 범위 안일 수 있음. 실로봇 실험은 과제 3개이고 과제마다 모델을 따로 post-training함. RoboTwin에서도 Hanging Mug(Easy 3%, Hard 1%)나 Open Microwave의 Hard(4%)처럼 거의 못 하는 과제가 남아 있음.

**누리랩 연구와의 연결**

- 영상 사전학습 기반 VLA나 world model을 직접 학습할 때 언어 주석을 얼마나 자세히 달고 사람 시연 데이터를 어떤 비율로 섞을지 정할 근거가 됨.
- action 라벨이 없는 영상도 같은 모델에서 영상 loss로만 학습시키는 구조라, 로봇 데이터가 적은 manipulation 과제에 1인칭 영상을 더하는 실험의 출발점으로 쓸 수 있음.

*대표 그림: 왼쪽은 약 47,000시간 사전학습 데이터의 구성을 출처별 시간으로 보인 도넛 그래프임(UMI 15,284.9시간이 가장 큼). 오른쪽은 측정 결과가 아니라 video DiT와 action DiT가 shared masked attention으로 이어지고 text cross-attention은 video 쪽에만 있는 구조를 그린 그림임.*

*영상: [저자가 올린 실로봇 컵 쌓기 영상으로, 학습 때 없던 여러 색 컵과 무늬 식탁보에서 성공한 장면임.](https://blog-media.assets.alphaxiv.org/videos/01a1c468-5c0d-7bbf-9c5f-f2c5cab72971/439fd190-3bee-4cbf-95f5-4692d3d29da0) (alphaXiv 요약에서 가져옴)*

---

### 5. Streaming Failure Forecasting: VLA Failure Monitors That Keep Learning After Deployment (74점)

[arXiv](https://arxiv.org/abs/2611.11688) · [PDF](https://arxiv.org/pdf/2611.11688) · [alphaXiv](https://www.alphaxiv.org/abs/2611.11688) (요약 있음) · [프로젝트 페이지](https://sff-research.org)

- **저자**: Amit Jadhav, Shaurya Beriwala, David Q. Liu, Yanfei Liu
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 75점
- **학회**: CoRL 2026 채택 · 근거: comments에 "25 pages, 13 figures, 9 tables. A short version was accepted at the Sim2Real2Field and EEAI workshops at CoRL 2026. Project page: this https URL"
- **읽은 원문**: PDF 전문

> VLA failure monitor의 마지막 linear layer만 매 episode의 성공/실패 결과로 다시 학습해, 배포 후 과제나 policy가 바뀌어도 실패를 계속 가려내게 함. 실제 SO-101 로봇 기록 434회에서 과제 전환 뒤 within-task AUROC가 frozen monitor의 0.536에서 0.656으로 오름.

**무슨 문제인가**

SAFE 같은 VLA failure monitor는 offline에서 학습하고 calibration한 뒤 고정해서 씀. 배포 뒤에는 조명, 물체, 카메라 위치가 바뀌고 policy도 새 버전이나 새 과제로 바뀌는데, monitor는 이 변화를 모름. 실제 로봇 기록에서 과제나 policy 버전이 바뀐 뒤 frozen monitor는 실패 episode를 성공 episode보다 높게 매기는 능력(같은 과제 안에서 잰 AUROC, within-task AUROC)이 거의 우연 수준인 0.5로 내려감. alarm threshold를 다시 맞추는 것으로는 이 순위가 고쳐지지 않으므로, 점수 자체를 배포 중에 고칠 방법이 필요함.

**어떻게 푸나**

SFF(Streaming Failure Forecasting)는 offline monitor의 hidden layer를 고정하고 마지막 readout만 배포 중에 학습함. 입력은 VLA 내부 activation을 128차원으로 줄인 값과 경과 시간 비율이고, 고정된 hidden layer가 이를 130차원 feature로 바꿈. readout은 policy call마다 위험 점수를 내고, episode 안의 최고 점수가 threshold를 넘으면 alarm을 냄. episode가 끝나면 그 성공/실패 결과 하나로 readout을 discounted least squares 식으로 바로 다시 계산함(130×130 선형 방정식 한 번). 이때 offline readout 쪽으로 당기는 anchor 항을 두어, 결과가 적을 때는 offline monitor와 같게 순위를 매김. 지난 episode는 저장하지 않고 합산 행렬만 들고 가므로 상태 크기가 1.0 MB로 고정되어 늘지 않음. threshold는 false alarm이 생길 수 있는 성공 episode 뒤에만 adaptive conformal inference 방식으로 움직여 장기 false alarm 비율을 목표 근처에 묶음.

**결과**

- 실제 SO-101 로봇 기록(ArmnetBench: SO-101 팔에서 과제별로 fine-tuning한 VLA 실행 기록) 434회를 과제·policy 전환이 예고 없이 오도록 재생함. 전환 뒤 within-task AUROC가 VLA 4개 모두에서 frozen monitor보다 높음. 4개 평균은 0.536에서 0.656으로 오름.
- 같은 실제 기록에서 전환 시점을 알려 주고 처음부터 다시 맞춘 full reset은 0.613임. SFF가 0.044 높으나 이 비교는 사후 분석(exploratory)으로 표시됨.
- 시뮬레이션은 SmolVLA가 LIBERO(시뮬레이션 조작 과제 모음)를 조명·물체·카메라·마모 변화 아래 수행한 기록임. 미리 고정한 test suite 5개 중 4개에서 SFF가 frozen monitor보다 높음. 주 시험인 LIBERO-10에서 0.707에서 0.736으로 올랐으나 차이의 95% 신뢰구간이 0을 포함함.
- Jetson Orin Nano CPU core 하나에서 policy call당 중앙값 2.18 ms가 듦. 시뮬레이션에서 성공 episode의 false alarm 비율은 설정에 따라 0.082~0.089로 목표 0.1 근처를 유지함. 두 변화가 겹친 조건에서는 0.19에서 0.37까지 오름.

**한계**

실제 로봇 결과는 기록을 다시 돌린 것이고 SFF를 실로봇에서 직접 돌리지는 않았음. 실제 데이터의 변화는 과제와 policy 가중치가 같이 바뀌는 전환 하나뿐이고, calibration run이 5회라 실제 false alarm 비율은 보고하지 않음. 변화가 없을 때는 학습이 손해임: 첫 과제에서 SFF의 within-task AUROC는 0.56으로 frozen monitor의 0.62보다 낮음. 매 episode 뒤 정확한 성공 label이 온다고 가정하며, 시뮬레이션 gain도 0.02에서 0.05 정도임.

**누리랩 연구와의 연결**

- failure detection을 배포 중 계속 갱신되는 문제로 다시 세운 사례임. 우리 failure detection/recovery 연구에서 offline monitor 위에 얹는 online readout 비교 대상으로 바로 쓸 수 있음.
- 성공/실패 결과 하나로 readout만 고치는 설정은 test-time optimization과 robot memory(지난 episode를 저장하지 않는 고정 크기 상태)와도 이어짐.

*대표 그림: (a)는 실제 로봇 기록에서 예고 없는 과제·policy 전환 뒤 10회 단위 within-task AUROC를 그린 그래프로, frozen monitor는 0.5 근처에 머물고 SFF는 0.53에서 약 0.7까지 오름. (b)는 전환 뒤 실패 run과 성공 run의 로봇 사진이고, (c)는 readout만 학습하는 구조를 그린 도식임.*

---

### 6. Distilling Instructions into Weights: Closed-Form Edits Fix a Robot Policy's Misreading (74점)

[arXiv](https://arxiv.org/abs/2611.11894) · [PDF](https://arxiv.org/pdf/2611.11894) · [alphaXiv](https://www.alphaxiv.org/abs/2611.11894) (요약 있음) · [프로젝트 페이지](https://ali-adeeb.com/weightsmith/) · [코드](https://github.com/adeeb10abbas/weightsmith)

- **저자**: Ali-Adeeb Abbas, Esmaeil Seraj
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 68점
- **학회**: CoRL 양식 (추정) · 근거: 1단 구성, 초록 아래 'Keywords:' 줄
- **읽은 원문**: PDF 전문

> VLA policy가 지시문을 잘못 읽어 실패할 때, 잘 되는 다른 지시문을 넣었을 때의 내부 activation 변화를 gradient 없이 closed-form으로 가중치에 써 넣어 고침. 원래 지시문 그대로 held-out 128회 성공이 27회에서 106회로 오름.

**무슨 문제인가**

generalist VLA policy는 이미 가진 기술로 할 수 있는 과제에서도 한 단계만 틀려 실패하는 일이 많음. 보통은 demonstration을 더 모아 fine-tuning하지만, 실패 원인이 한 계산에 있다면 가중치를 직접 고치는 편이 쌀 수 있음. 최근 gradient 없는 weight edit 보고가 몇 개 나왔으나 과제별로 fine-tuning된 checkpoint 위주였고 비교 조건도 제각각이었음. 그래서 학습한 적 없는 과제에서 어떤 종류의 실패를 weight edit으로 고칠 수 있는지가 정리되지 않았음.

**어떻게 푸나**

대상은 RoboLab(Isaac Sim 기반 조작 과제 모음)의 과제를 학습한 적 없는 π0.5 DROID checkpoint임. 먼저 실패한 순간의 이미지, robot state, flow-matching noise를 고정하고 지시문만 바꿔 다시 돌려 봄. "cube 다음 banana를 bowl에" 과제에서 "in the bowl"을 cube 옆으로 옮긴 표현(known-good instruction)만 cube를 일찍 놓는 행동을 없앴음. 저자는 이를 policy가 목적지를 엉뚱한 물체에 묶는 binding error로 해석함. closed-form instruction distillation은 VLM 각 층의 MLP down-projection 입력을 key로, 두 지시문 사이의 residual 변화량을 value로 둠. key는 prompt·state 위치 40개와 이미지 cell 32개이고, 실패 장면 6개에서 평균함. 이 key를 value로 보내는 정규화된 최소 norm 가중치 변화를 층마다 한 번에 풀며, 층당 rank는 72 이하임. 결과물은 원래 지시문을 받아도 known-good 지시문을 받은 것처럼 계산하는 수정된 가중치임.

**결과**

- cube-then-banana 과제의 held-out seed 128개에서 실패하던 81회가 성공으로 바뀌고, 성공하던 2회가 실패로 바뀜(exact McNemar p=7.2×10^-22).
- 같은 층, 같은 rank와 singular value로 방향만 무작위로 만든 update는 64회 중 9회로, 무수정 policy의 13회와 차이가 없음. 같은 seed에서 distilled edit은 50회임.
- 같은 distillation을 action expert에 넣으면 64회 중 20회, action head에 넣으면 0회임. 새 held-out seed 64개에서 VLM에 넣은 경우는 55회이고 무수정은 5회임. 다른 과제의 성공률까지 올린 것도 VLM edit뿐임.
- cube-then-banana용 edit을 그대로 쓴 다른 과제 2개에서도 성공이 오름: 안경 집기 22/64에서 44/64, cube를 bowl 왼쪽에 두기 8/64에서 36/64임. 나머지 13개 과제에서는 유의한 차이가 없음.

**한계**

결과는 모두 zero-shot checkpoint 하나의 시뮬레이션 결과이고 실로봇 실험은 없음. 방법은 잘 되는 지시문이 먼저 있어야 하며, perception 혼동, 없는 grasp 기술, 접촉 미끄러짐을 겨냥한 edit은 성공률을 올리지 못함. 같은 가중치를 다시 돌려도 paired 결과의 약 1/3이 바뀌어서 32~64쌍 비교로는 작은 차이를 가리기 어려움. 공개 도구는 과제 하나에서만 돌려 봄.

**누리랩 연구와의 연결**

- failure detection·recovery 관점에서, 실패 장면을 다시 돌려 원인이 언어 binding인지 perception인지 가르는 진단 절차로 쓸 수 있음. 고칠 수 있는 실패와 학습이 필요한 실패를 나누는 기준도 제시함.
- VLA를 학습 없이 test-time에 고치는 방법의 비교 대상이 됨. 또한 paired seed와 무수정 rerun을 함께 보라는 평가 절차는 우리 VLA 실험 설계에 바로 적용 가능함.

*대표 그림: held-out 시작 상태 하나에서 무수정 policy와 수정된 policy의 wrist camera 장면을 control step 75, 90, 120, 255에서 나란히 보여 줌. 무수정은 step 76에 cube를 놓쳐 실패하고 수정본은 cube를 bowl에 넣은 뒤 step 257에 성공하며, 오른쪽에 held-out 128회 성공 수(27 대 106)가 표시됨.*

*영상: [같은 장면과 같은 지시문에서 무수정 π0.5는 cube를 놓치고 수정된 policy는 cube와 banana를 차례로 bowl에 넣는 시뮬레이션 rollout을 나란히 찍은 영상임.](https://blog-media.assets.alphaxiv.org/videos/01a1c440-9a75-7328-bd26-9e7bd4967f3f/3835a374-204c-471c-876b-37aac8a206a0) (alphaXiv 요약에서 가져옴)*

---

### 7. WARP-JEPA: World-Model-in-the-Loop Amortized Rollout Planning for Frozen Hierarchical Joint-Embedding Predictive Architectures (74점)

[arXiv](https://arxiv.org/abs/2611.10806) · [PDF](https://arxiv.org/pdf/2611.10806) · [alphaXiv](https://www.alphaxiv.org/abs/2611.10806) (요약 있음) · [코드](https://github.com/hideinsewer/WARP-JEPA)

- **저자**: Junjie Li, Zhaojiacheng Zhou, Kaixiang Wang, Zihan Wang, QingSong Zhao, Jiong Lou, Jie Li
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 82점
- **읽은 원문**: PDF 전문

> 고정된 계층형 JEPA world model에서 test-time gradient descent 대신 학습된 proposer가 후보 계획 여러 개를 내고 world model이 그중 하나를 고르게 함. 장기 과제의 episode 시간이 9.6~18.8배 줄고, Visual AntMaze 2단 계층 성공률은 45.3%에서 78.7%로 오름.

**무슨 문제인가**

H-JEPA(계층형 Joint-Embedding Predictive Architecture)는 여러 시간 단위의 latent world model을 쌓아 위 단계가 subgoal을 주고 아래 단계가 따라가게 계획함. 매 단계에서 행동을 gradient descent로 world model 안에서 반복 최적화하므로, 장기 과제에서 이 반복 계산이 episode 시간의 96.6~97.7%를 차지함. 또 world model이 예측한 cost를 낮게 만든다고 실제 성공이 오르지 않음. Push-T(T자 블록을 목표 자세로 밀기)에서 online gradient descent의 예측 terminal cost는 16.9로 학습된 proposer의 73.7보다 낮지만, 성공률은 42.0% 대 48.0%로 오히려 낮음. 저자는 최적화가 world model의 예측 오차를 파고들어 데이터에 없는 행동으로 간다고 봄.

**어떻게 푸나**

WARP-JEPA(World-model-in-the-loop Amortized Rollout Planning)는 H-JEPA의 encoder와 predictor를 모두 고정하고 계획기만 바꿈. 계층의 각 단계마다 proposer를 두고, 현재 latent와 목표(또는 상위 단계의 subgoal과 macro-action)를 입력받아 후보 행동열 K개(최상위 32개, 하위 16개)를 한 번에 출력함. 고정된 predictor로 후보를 굴려 terminal latent cost가 가장 낮은 후보를 고름. 후보를 고르는 데에는 test time gradient 반복을 쓰지 않음. proposer 학습 loss는 두 항의 합임. 첫째는 cost가 가장 낮은 후보를 낸 출력 head에 gradient의 95%를 보내는 relaxed winner-take-all rollout cost임. 둘째는 K개 중 demonstration에 가장 가까운 후보만 맞추는 best-of-K behavior cloning임. 하위 단계는 두 걸음짜리 짧은 연결이라 residual MLP가 후보를 병렬로 냄. 최상위 단계는 macro-action을 최대 12개 이어야 하므로 1층 causal Transformer가 한 걸음씩 생성하며, 매 걸음 world model이 상상한 다음 latent를 다음 입력에 넣음. 이 생성 과정에서 이미 rollout이 끝나므로 후보 평가에 rollout을 따로 돌리지 않음.

**결과**

- 고정된 H-JEPA 30개(benchmark 4개, 2~4단 계층)에서 online gradient descent 대비 episode 시간이 장기 과제 9.6~18.8배 줄어듦. 짧은 과제인 Cube에서는 2.9~3.0배임. AntMaze 4단 계층 episode 시간은 92.5초에서 7.15초로 내려감.
- 같은 고정 world model에서 성공률도 오름. Visual AntMaze(시각 관측 기반 개미 로봇 미로 이동) 2단 계층은 45.3%에서 78.7%, Push-T 2단 계층은 40.8%에서 64.7%임. 모든 설정에서 online gradient descent보다 유의하게 나쁜 경우는 없음.
- 최상위 계획 길이가 긴 설정에서 world model 상태를 되먹이는 Transformer가 병렬 MLP보다 나음. Push-T 2단 계층(길이 8)에서 64.7% 대 55.9%, FourRoom 2단 계층(길이 12)에서 100.0% 대 92.0%임. 길이 2~3에서는 차이가 유의하지 않음.
- Push-T 2단 계층 150개 과제에서 후보 수 K를 1, 4, 8, 32로 늘리면 성공률이 18.7%, 38.7%, 42.0%, 48.0%로 오름. world model 선택 없이 후보 32개를 평균하면 28.0%, 학습된 proposer 없이 random shooting 32개면 0%임.

**한계**

모든 실험이 시뮬레이션이며 실로봇 결과는 없음. world model을 고치지 않으므로 world model이 틀리면 계획도 실패함: Push-T 4단 계층은 모든 계획기의 성공률이 1.2% 이하임. H-JEPA 모델마다 proposer를 따로 학습해야 하고(0.2~3.6시간), episode 끝부분의 하위 계획 9~33%는 여전히 gradient descent 10회를 돌림. 예측 cost와 성공률이 어긋난다는 핵심 관찰은 150개 과제에서 통계적으로 유의하지 않음.

**누리랩 연구와의 연결**

- test-time optimization을 학습된 후보 생성과 world model 선택으로 바꾼 사례임. world model 기반 inference-time planning에서 계산량과 성공률을 함께 비교할 기준 실험으로 쓸 수 있음.
- world model의 예측 cost가 낮은데 실제로 실패하는 사례를 보였으나 차이는 통계적으로 유의하지 않음. world model 기반 failure detection에서 예측 cost만 믿으면 안 된다는 근거로 쓸 수 있음.

*대표 그림: 네 benchmark에서 online gradient descent와 WARP-JEPA가 고른 계획을 비교한 정성 결과 그림임. 위 줄 Push-T와 FourRoom은 점선의 gradient descent 경로가 목표에 못 가고 후보 K개 중 고른 주황 경로가 목표에 닿음. 아래 줄 AntMaze와 Cube는 실제 rollout 마지막 장면에서 gradient descent는 실패하고 WARP-JEPA는 성공한 모습임.*

---

### 8. WorldMind: Test-Time Scaling for Visual Spatial Reasoning through Latent World Simulation (74점)

[arXiv](https://arxiv.org/abs/2611.10151) · [PDF](https://arxiv.org/pdf/2611.10151) · [alphaXiv](https://www.alphaxiv.org/abs/2611.10151)

- **저자**: Haoming Wang, Yongjian Fu, Ju Ren, Wei Gao
- **분야**: World Model · robotics relevance 7/10 · 1차 스크리닝 78점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> VLM이 시점 이동을 고르면 world model이 그 장면을 이미지로 그리지 않고 내부 latent feature로 바로 돌려주게 함. test-time에 시점 이동과 추론 단계를 반복해 공간 추론을 함. MindCube-Tiny 정답률을 base VLM의 40.9%에서 59.2%로 올림.

**무슨 문제인가**

VLM은 한 장면에서 물체를 알아보는 일은 잘하지만, 다른 자리로 옮겨 서면 무엇이 보일지 같은 시점 전환 질문(perspective-taking)에 약함. 텍스트 추론을 길게 늘리면 장면에 없는 공간 정보가 생기지 않아 오히려 성능이 내려가기도 함. depth map이나 point cloud를 넣는 방법은 지금 보이는 장면만 다루므로 시점을 바꿔 보는 질문에는 도움이 적음. world model로 새 시점 이미지를 만들어 VLM에 다시 넣는 방법도 있지만, latent를 pixel로 바꾸고 다시 visual encoder로 읽는 과정에서 기하 정보가 빠짐.

**어떻게 푸나**

WorldMind는 VLM과 고정된 diffusion world model(SVC, 카메라 이동에 따른 새 시점을 만드는 모델)을 붙임. 추론 중 VLM은 한 단계마다 텍스트 추론과 camera action을 내고, world model은 그 action대로 장면을 옮긴 latent를 돌려줌. 이 latent는 adapter를 거쳐 VLM 입력 공간으로 바뀌고 다음 추론 단계의 context에 붙음. 어떤 latent를 쓸지는 world model의 layer 4개와 denoising timestep 4개 조합 중 feature ablation으로 8개를 미리 골라 고정함. 학습은 세 단계임: adapter만 정답 loss로 정렬하고, GPT-5.6 Sol이 만든 추론 궤적 10,000개로 SFT를 하고, 질문 5,000개로 GRPO 기반 RL을 함. RL의 단계별 reward는 정답 확률이 오른 만큼(progress)을 주되, action이 텍스트 지시와 맞는 정도와 생성 latent가 정답 시점 latent와 비슷한 정도를 곱해서 줌. 두 곱하는 항을 각각 action validity, state validity라 부름.

**결과**

- 세 benchmark에서 base VLM(Qwen3-VL-8B)보다 정답률이 오름. VSI-Bench(실내 영상 기반 거리·방향·경로 질문)는 57.4%에서 71.1%로 오름. MMSI-Bench(여러 장 이미지 공간 관계 11종)는 29.4%에서 43.4%로, MindCube-Tiny(적은 시점에서 회전·주변 돌기 추론)는 40.9%에서 59.2%로 오름.
- RGB 이미지를 돌려주는 world model 결합 방법과 비교함. MMSI-Bench에서 Astra 37.3% 대 43.4%, MindCube-Tiny에서 Astra 46.8% 대 59.2%임. VSI-Bench에서는 71.1%로 RGB world model 결합 방법 AVIC의 66.6%보다 높고, 3D feature를 넣는 Cambrian-S(67.5%)보다도 높음.
- 같은 조건의 소규모 ablation에서 RGB 시뮬레이션을 latent 시뮬레이션으로 바꾸면 VSI-Bench 63.4%에서 65.2%, MMSI-Bench 33.6%에서 36.2%로 오름. MindCube는 RGB 48.4%, latent 48.5%로 거의 같음. 텍스트 추론만 늘리면 VSI-Bench에서 base보다 1.5퍼센트포인트 내려감.
- VSI-Bench reward ablation에서 정답 reward만 쓰면 68.1%, progress에 두 validity 항을 모두 곱하면 70.2%임. validity 항을 하나만 넣으면 68.0%에서 68.9% 사이임.

**한계**

실험은 모두 질의응답 benchmark이고 로봇이나 실제 행동 과제는 없음. state validity reward는 정답 시점을 렌더링할 수 있는 합성 3D 장면(AI2-THOR, Infinigen)에서만 계산되므로 RL 데이터가 합성 장면에 묶임. 초록이 주장한 평균 향상폭(base VLM 대비 16.0%, 가장 강한 RGB 방식 대비 8.3%)은 계산 방식이 본문에 적혀 있지 않음. world model 호출에 드는 추론 시간과 코드 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- world model을 이미지 생성기가 아니라 latent 상태를 돌려주는 시뮬레이터로 쓰고, 상상한 상태가 믿을 만한 정도를 reward에 곱해 거른 설계임. test-time planning과 world model 기반 failure detection에서 상상 상태의 신뢰도를 다루는 방법으로 참고할 수 있음.
- 어느 시점으로 옮겨 볼지를 VLM이 고르는 구조는 active perception/NBV와 embodied spatial reasoning에 이어짐. 다만 실제 카메라를 움직이는 실험은 없음.

*대표 그림: 측정 결과가 아니라 문제 설정을 그린 개념도임. 거실 사진과 함께 테이블 반대편으로 가서 TV를 보면 식물이 어디 있는지를 묻고, 사람은 머릿속에서 시점을 옮겨 답하지만 의미 이해 위주로 학습된 VLM은 흐릿한 배치만 떠올린다는 대비를 보여 줌.*

---

### 9. Compass 1: Towards Open-World and Persistent Embodied Navigation from Monocular RGB Videos (72점)

[arXiv](https://arxiv.org/abs/2611.12087) · [PDF](https://arxiv.org/pdf/2611.12087) · [alphaXiv](https://www.alphaxiv.org/abs/2611.12087) (요약 있음) · [프로젝트 페이지](https://www.archon.tech/research/compass1)

- **저자**: Hai Zhang, Siqi Liang, Yanjun Guo, Shoufeng Zhang, Yunhao Wang, Hangyu Du, Haoguang Mai, Hongchen Li 외 12명
- **분야**: Navigation · robotics relevance 9/10 · 1차 스크리닝 70점
- **학회**: ByteDance 자체 양식 · 근거: 글꼴 ByteSans, 학회 양식 아님
- **읽은 원문**: PDF 전문

> 단안 RGB 영상만 받는 navigation model에 지나온 경로를 그린 2D 지도 이미지와 기억을 묻는 VQA 학습을 더해, 약 2분 전에 본 목표로 되돌아가게 함. 실세계 8개 과제 320회 평가에서 전체 성공률 79.4%를 얻었고, 가장 강한 baseline은 17.8%임.

**무슨 문제인가**

학습 기반 VLN model은 시뮬레이션 benchmark 점수는 높지만 실세계에서는 너무 일찍 멈추거나 반대로 돌거나 방향이 틀어지는 실패를 자주 보임. 목표가 안 보이는 탐색에서는 추론 단계마다 의도가 바뀌어 좌우로 번갈아 돌기만 하고 나아가지 못함. 긴 기록은 영상 전체를 그대로 넣거나 임의 규칙으로 압축하는데, 저자들은 두 방식 모두 기록을 실제로 활용하지 못한다고 봄. 그래서 예전에 본 물체로 되돌아가는 과제(history backtracking)는 기존 방법으로 거의 풀리지 않음.

**어떻게 푸나**

Compass 1은 언어 이해와 영상 생성을 함께 하는 Cosmos3-Edge-4B backbone을 구조 변경 없이 씀. 입력은 언어 지시, 행동 궤적을 기준으로 고른 sparse keyframe, 그리고 HRM(History Representation Map)임. HRM은 지나온 경로, keyframe 위치와 번호, 과거 진행 방향, 현재 위치를 2D 이미지 한 장에 그린 것이고, 일반 이미지 입력으로 들어감. 저자들은 HRM만 넣으면 model이 지도를 무시한다고 보고, 세 종류의 VQA로 지도를 쓰게 학습함. 지금 몇 번째 단계인지와 멈출지를 묻고, 좌우 어느 쪽을 이미 가 봤는지를 묻고, 목표가 찍힌 keyframe 번호와 그쪽 방향을 묻는 식임. 출력은 language head의 VQA 답과 diffusion head가 만드는 미래 영상 및 [dx, dy, dyaw] 행동 궤적임. 배포 때는 행동을 먼저 로봇에 보내고 언어 추론은 비동기로 돌려 멈춤 신호만 따로 전달함.

**결과**

- 사무실, 테라스, 복합 공간, 거리 4곳에서 8개 과제를 장소마다 10회씩, 모두 320회를 Unitree Go2 사족 로봇으로 평가함. 가장 강한 baseline은 AwareVLN임. 네 baseline은 같은 데이터로 fine-tuning한 것과 원래 가중치 중 높은 값을 씀.
- 앞 단계 목표에서 보이지 않는 곳으로 되돌아가는 persistent history backtracking 성공률은 58%이고, 가장 강한 baseline은 0%임. 목표가 근처에 있는 basic backtracking은 98% 대 8%임.
- 목표가 보이지 않는 상태에서 막다른 곳을 빠져나와 목표를 찾는 target-driven 탐색은 85% 대 18%이고, 4단계 이상 지시를 따르는 multi-stage navigation은 50% 대 0%임.
- 학습은 주로 높이 1m 카메라 데이터로 했지만 평가 로봇의 카메라 높이는 약 0.5m임. 다른 몸체 시험에서 바퀴 로봇은 10회 중 9회, humanoid와 drone은 10회 중 7회 성공함.

**한계**

평가 과제와 장소는 저자들이 직접 설계했고, 몸체 전이 시험은 몸체당 10회뿐임. baseline 다수는 시뮬레이션 VLN용으로 만든 이산 행동 model이라 실세계 조건에서 불리할 수 있음. 제공된 원문 텍스트에서 ablation 수치, 추론 속도, 시뮬레이션 결과 부분은 생략되어 있어 본문에서 확인 불가임. 데이터 공개를 밝혔지만 코드 저장소 주소는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- 과거 관측을 2D 지도 이미지로 그려 backbone에 넣고, VQA로 그 지도를 쓰게 만드는 방식은 robot memory를 구조 변경 없이 VLA에 붙이는 한 방법임. manipulation의 장기 과제에서 예전 물체 위치를 다시 찾는 문제에 옮겨 볼 수 있음.
- 멈춤 시점과 현재 단계를 따로 묻는 VQA는 조기 정지 같은 실행 실패를 줄이려는 장치라서, failure detection 신호를 학습 목표로 넣는 사례로 참고할 수 있음.

*대표 그림: 실내 사무실 바닥을 찍은 사진으로, 왼쪽 앞에 빨간색과 흰색 줄무늬 콘이 있고 오른쪽 뒤에 사족 로봇들이 놓여 있음. 측정 결과나 방법 구조가 아니라 실험 장소를 보여 주는 장면임.*

*영상: [프로젝트 페이지에 실린 humanoid 시연 영상으로, 회색 콘, 노란 의자, 문을 차례로 지나 다시 회색 콘으로 돌아가는 지시를 따르는 장면임.](https://blog-media.assets.alphaxiv.org/videos/01a1c448-1a70-7f52-980e-af7324d75584/a4455eb5-a54f-43ff-a050-e65089001ecd) (alphaXiv 요약에서 가져옴)*

---

### 10. GUARD: Anomaly-Informed Q-Steering for Generative Robot Policies in Dexterous Manipulation (72점)

[arXiv](https://arxiv.org/abs/2611.10343) · [PDF](https://arxiv.org/pdf/2611.10343) · [alphaXiv](https://www.alphaxiv.org/abs/2611.10343)

- **저자**: Aryaman Gupta, Xiaoyue Wu, Rana Soltani Zarrin, Mark Van der Merwe
- **분야**: Manipulation · robotics relevance 9/10 · 1차 스크리닝 70점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 8쪽
- **읽은 원문**: PDF 전문

> 고정된 flow matching policy가 학습 데이터 분포 밖으로 벗어나는 것을 막기 위해, 이상 점수(anomaly score)를 dense reward로 바꿔 Q-function을 학습하고 그 gradient로 denoising을 조정함. Adroit 4개 과제 평균 성공률을 BC의 60%에서 96%로 올림.

**무슨 문제인가**

diffusion·flow matching policy는 demonstration을 흉내 내므로, 실행 중 작은 오차로 학습 데이터에 드문 상태에 들어가면 쉽게 실패함(covariate shift). 접촉이 많은 dexterous manipulation에서는 작은 오차가 더 크게 쌓임. 사람이 개입해 교정 demonstration을 주는 방법은 다지 로봇 손에서 수집이 어렵고, RL post-training은 reward 품질에 크게 기댐. dense reward는 과제마다 설계나 실패 라벨이 필요하고, 성공 여부만 주는 sparse reward는 신호가 늦게 와서 학습이 어려움. 기존 이상 탐지 연구는 실패를 감지하는 데 그쳤고, 감지 뒤 행동을 고치는 방법은 단순 재시도나 상태 보간 정도였음.

**어떻게 푸나**

GUARD(Guidance Using Anomaly-infoRmed Dense Values)는 policy를 고정한 채 행동을 생성하는 denoising 과정만 바꿈. 먼저 policy 학습 demonstration의 관측에 별도 flow model을 맞추고, 관측을 Gaussian latent로 보냈을 때의 norm 제곱을 이상 점수로 씀. 각 transition에는 다음 상태의 이상 점수를 표준화해 부호를 바꾼 값을 dense reward로 주고, 표준화한 sparse 성공 reward와 같은 가중치로 더함. 이 합산 reward로 Q-function ensemble 5개를 학습하며, 평균에서 표준편차의 0.5배를 뺀 보수적 값을 씀. 학습은 두 단계임: 고정 policy의 rollout으로 offline FQE(fitted Q evaluation)를 하고, 이어서 조정된 policy로 새 rollout을 모으며 Q를 다시 맞춤. 실행할 때는 denoising 단계마다 현재 noisy 행동에서 깨끗한 행동을 한 번에 추정하고, 그 지점의 Q gradient를 flow velocity에 더함. 입력은 로봇 상태 관측이고 출력은 조정된 행동임.

**결과**

- Adroit(시뮬레이션 다지 손으로 물체 옮기기·펜 돌리기·망치질·문 열기를 하는 4개 과제)에서 평균 성공률이 BC 60%, 가장 강한 baseline인 dynamics model 기반 guidance 방법 DynaGuide 75%, GUARD 96%임. 3 seed, 과제당 100 rollout 기준임.
- 행동에 Gaussian noise를 넣어 dynamics를 흔든 조건에서 평균 성공률이 BC 41%, DynaGuide 60%, GUARD 80%임. 다만 이 조건의 Relocate 과제에서는 별도 이상 탐지기 RND(random network distillation)로 잰 이상 점수가 GUARD 62.49로, BC 25.34 등 여러 baseline보다 높음.
- sparse reward만 쓴 Q-guidance(Sparse-Q)보다 평균 성공률이 nominal과 perturbed 모두 30퍼센트포인트 높음. 이상 점수 gradient로 직접 조정한 U-SA보다는 nominal에서 24퍼센트포인트, perturbed에서 28퍼센트포인트 높음.
- 시뮬레이션에서만 학습해 16자유도 Allegro 손에 그대로 옮김. 과제당 20회 시도에서 드라이버 회전 성공률이 20%에서 60%, 손바닥 아래 방향 재배치가 70%에서 95%로 오름. 손바닥 위 방향 재배치는 30%에서 10%로 내려감.

**한계**

시뮬레이션 실험은 상태 입력 MLP policy와 Adroit 4개 과제뿐이고, 이미지 입력이나 VLA 규모 policy는 다루지 않음. Q를 맞추려면 과제마다 offline rollout과 online 상호작용이 필요하며, 실로봇에서는 이를 모두 시뮬레이션에서 함. 실제 환경의 성공 상태 분포가 시뮬레이션과 다르면 Q가 실패를 예측하지 못하고 성능이 오히려 내려감(손바닥 위 재배치).

**누리랩 연구와의 연결**

- failure detection에 쓰던 이상 점수를 test-time 행동 조정 신호로 바꾼 사례임. 실패 감지 뒤 recovery를 따로 설계하지 않고 Q gradient로 처리하는 방향의 비교 대상으로 쓸 수 있음.
- 고정된 generative policy를 가중치 수정 없이 inference-time에 조정하므로, VLA의 action expert에 같은 신호를 붙이는 실험으로 이어 볼 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 기본 flow 경로(검은 선)는 이상 상태로 가서 물체를 놓치는 반면, Q gradient(보라 점선)를 더한 경로(초록 선)는 분포 안쪽에 머물러 성공하는 모습을 보여 줌.*

---

### 11. Tiresias: Towards Language-Conditioned World Models (72점)

[arXiv](https://arxiv.org/abs/2611.10392) · [PDF](https://arxiv.org/pdf/2611.10392) · [alphaXiv](https://www.alphaxiv.org/abs/2611.10392) (요약 있음) · [코드](https://github.com/UWMILab/Tiresias)

- **저자**: Fengyi Wu, Yifei Dong, Yetong Sha, Lingdong Kong, Qiyu Hu, Bohan Xiong, Qi Dai, Alexander G. Hauptmann 외 1명
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 74점
- **학회**: Meta 자체 양식 · 근거: 글꼴 OptimisticDisp, 학회 양식 아님
- **읽은 원문**: PDF 전문

> 언어 지시로 행동 궤적 후보를 많이 뽑고, 그중 일부만 world model로 결과 영상을 상상해 골라내는 planning 방식을 제안함. 네 도메인 15개 데이터셋을 묶은 벤치마크에서 val seen 종합 점수가 가장 강한 baseline의 54에서 63으로 오름.

**무슨 문제인가**

world model로 언어 지시를 수행하는 연구는 navigation, 조작, 게임, 주행마다 행동 공간과 데이터셋과 평가 지표가 달라서 서로 비교하기 어려움. 그래서 같은 planning 방식이 여러 embodiment와 지시 문체에 통하는지 확인할 방법이 없었음. 또 world model은 그럴듯한 미래 영상을 만드는 데 주로 쓰였고, 지시에 맞는 행동을 고르는 평가자로 쓰는 시도는 적었음.

**어떻게 푸나**

저자는 먼저 LCWM(language-conditioned world modeling) 과제를 정의함. 입력은 첫 1인칭 RGB 관측과 언어 지시이고, 출력은 지시를 수행하는 행동 시퀀스 전체임. 행동은 평면 이동과 yaw 회전을 공통으로 두고, 도메인별로 높이, 속도, roll·pitch·gripper 채널을 덧붙임. 제안 agent인 Tiresias는 먼저 LDP(language-conditioned diffusion policy)가 장면을 보지 않고 지시만으로 궤적 후보 128개를 뽑음. Tr-Ranker(궤적 ranker)는 지시와 궤적만 보고 성공률·경로 유사도 등을 예측해 8개를 남김. 남은 8개만 Wan2.2 영상 모델을 고친 world model이 첫 관측과 지시를 받아 결과 영상을 상상하고, V-Ranker(시각 ranker)가 그 영상을 지시와 맞춰 점수를 매김. 두 점수를 2:1로 합쳐 최종 궤적 하나를 고름.

**결과**

- LCWM-Bench(navigation·조작·3D 게임·주행 15개 데이터셋, 142,987 episode, 지시 428,961개)에서 SR(성공률)과 nDTW(정답 경로와의 유사도)의 도메인 평균인 종합 점수를 잼. val seen에서 Tiresias가 63, LCVN-WM이 54임. 학습에 없던 데이터셋으로 만든 val unseen에서는 Tiresias 51, 기존 baseline 중 가장 높은 LCVN-Uni(관측과 행동을 함께 예측하는 모델) 42임.
- 같은 무작위 후보 8개에서 고르는 방식만 바꾼 비교에서 성공률은 두 점수를 합쳤을 때 0.39임. Tr-Ranker만 쓰면 0.30, V-Ranker만 쓰면 0.28, 같은 상상 영상을 Qwen3.6으로 판정하면 0.26임. 8개 중 정답을 아는 oracle은 0.52라서 고르는 단계에 남은 여지가 큼.
- 후보 생성기를 sampling 기반 MPC로 바꾸면, ranker를 다시 학습하지 않아도 성공률이 고르지 않고 실행한 0.11에서 두 ranker로 고른 0.56으로 오름. 같은 조건에서 LDP 후보는 0.13에서 0.60으로 오름.
- 조작 도메인만 보면 val seen 성공률이 0.55로 LCVN-WM의 0.44보다 높음.

**한계**

평가는 예측한 궤적을 정답 궤적과 비교하는 방식이라, 행동을 실제로 실행해 성공하는지는 보이지 않음. 지시 문장은 Qwen3.6-27B가 만들고 사람이 검수한 것이라 실제 사용자 지시와 분포가 다를 수 있음. 저자도 지시가 이동 거리를 정하지 않을 때 후반부 궤적이 어긋나고, 상상 영상이 실제와 달라지는 실패를 적음.

**누리랩 연구와의 연결**

- world model을 영상 생성기가 아니라 행동 후보를 거르는 검증기로 쓰는 test-time planning 구조임. VLA가 낸 여러 행동 후보를 world model 상상으로 걸러 실패를 미리 막는 연구의 비교 대상으로 쓸 수 있음.
- 값싼 궤적 ranker로 먼저 거르고 비싼 상상은 8개에만 쓰는 구조는, world model 기반 failure detection의 계산량을 줄이는 설계로 그대로 가져올 수 있음.

*대표 그림: 왼쪽은 Minecraft 장면에서 지시를 받은 agent가 여러 후보 경로를 상상으로 따라가는 과정(A에서 D)을 그린 설명용 그림이고, 가운데는 벤치마크 규모 요약임. 오른쪽 radar chart는 종합 점수, SR, nDTW, SSIM, PSNR에서 Tiresias를 LCVN-WM, LCVN-Uni, NWM, Diamond와 비교함.*

---

### 12. How Many Candidates Does a One-Step World Model Need? A Random-Codebook Account of Nearest-of-m Training on Frozen DINO Tokens (72점)

[arXiv](https://arxiv.org/abs/2611.11887) · [PDF](https://arxiv.org/pdf/2611.11887) · [alphaXiv](https://www.alphaxiv.org/abs/2611.11887) (요약 있음)

- **저자**: Yong Hwi Song, Keon Myung Lee
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> frozen DINO token 위에서, 학습 때 후보 m개를 뽑아 실제 결과에 가장 가까운 하나만 맞추는 one-step world model을 만들고 m을 고르는 기준을 이론으로 제시함. 4방향 bounce 과제에서 m=16이 50-step flow matching보다 높은 mode coverage(0.93 대 0.79)를 약 30배 낮은 지연으로 얻음.

**무슨 문제인가**

frozen DINO feature 공간에서 다음 상태를 deterministic하게 예측하는 world model은 미래가 여러 갈래일 때 그 평균을 내놓아 실제로 일어나지 않는 상태를 예측함. diffusion이나 flow matching은 여러 갈래를 표현하지만 한 step 예측에 network를 수십 번 돌려야 함. planner가 수천 개의 미래를 상상할 때는 이 비용이 커짐. 한 번의 forward pass로 샘플을 내는 nearest-of-m 학습(conditional IMLE, Implicit Maximum Likelihood Estimation)이 대안으로 있지만, 후보 수 m을 얼마로 잡아야 하는지는 정해진 기준이 없었음. 선행 연구는 작은 m이면 충분하다고 추측하거나, hard minimum 대신 후보 전체와의 거리를 쓰는 energy score를 써야 한다고 주장함.

**어떻게 푸나**

IMLE-WM은 DINOv2/v3 patch token(16×16 grid, 384 channel) 세 장의 context, action, noise vector를 받아 다음 token map과의 차이를 ConvNeXt generator로 예측함. 학습 때는 noise를 m개 뽑아 후보 m개를 만들고, 실제 다음 token map에 가장 가까운 후보 하나만 robust loss로 끌어당김. 추론 때는 noise 하나로 forward pass 한 번만 하므로 m은 추론 비용에 영향이 없음. 이 loss의 기댓값은 generator 샘플 m개로 만든 random codebook으로 실제 결과를 양자화한 오차와 같음. 저자들은 이를 근거로 세 가지 예측을 실험 전에 기록함. 첫째, context가 반복되지 않는 데이터에서는 모델이 학습 context마다 실제 결과를 외우려 함. 그 유인의 크기는 codebook이 mode를 놓칠 때의 거리 오차 I(m)로 정해짐. 둘째, m이 커지면 드문 mode의 샘플 비율이 실제 확률보다 커지고, 셋째, 연속적인 고차원 결과에서는 샘플 분산이 실제보다 작아짐. 여러 step rollout에는 모델 자신의 예측을 context로 다시 넣으며 step마다 가장 가까운 후보를 고르는 per-step matching을 씀.

**결과**

- A2-div(공이 벽에 부딪히면 4방향 중 하나로 튀고 겉모습이 episode마다 바뀌는 합성 과제)에서 held-out mode coverage를 잼. IMLE-WM m=16이 0.93, 50-step flow matching(FM-50)이 0.79, energy score m=16이 0.28임. 같은 파라미터 수(약 8M) 조건이고, 한 step 지연은 3.3ms 대 107ms임.
- 학습 context의 결과를 외운 정도(memorization index, 우연 수준 0.25)는 regression 0.99, energy score 0.87~0.97, IMLE-WM m=4는 0.75, m=16은 0.29임. 튀는 방향 수 K가 4, 8인 데이터로 맞춘 선형식으로 K=2, 16의 결과 9개를 미리 예측했고 7개가 구간 안에 들어감.
- center of gravity를 숨긴 stochastic Push-T에서 per-step matching은 같은 8k step 학습 기준으로 16 step 뒤(h=16) recall 오차를 43.7px에서 29.3px로 줄임. 학습 시간은 3.9배임.
- 실제 로봇 영상인 BAIR에서는 best-of-16 token 오차가 FM-50보다 낮지만(0.527 대 0.843), kNN recall은 0.15 대 0.84로 분포를 덜 덮음. 구덩이 옆을 밀고 지나가야 하는 branch-risk 과제에서 IMLE-WM은 빠질 위험을 맞게 추정하지만, planning 성공률은 regression과 비슷함(55% 대 56%).

**한계**

과제는 BAIR를 빼면 모두 합성 또는 시뮬레이션이고, 모델은 8M과 21M로 작음. 저자들이 재현한 flow matching world model(FlowWM, 위 FM-50)은 원 논문보다 데이터가 8분의 1이라 flow 계열과의 비교는 작은 규모에 한정됨. Push-T에서 flow 대비 recall 우위는 seed까지 넣은 bootstrap 구간이 0을 포함하고, 실로봇 제어 실험은 없음.

**누리랩 연구와의 연결**

- branch-risk 과제는 world model이 실패 확률을 맞게 추정해도 평균 거리로 후보를 고르는 CEM(cross-entropy method) planner가 그것을 쓰지 못함을 보임. failure detection 결과를 planning에 넣는 연구(CVaR 곧 conditional value-at-risk 목표, 실패 확률 제약)의 출발점으로 쓸 수 있음.
- frozen DINO token 위 one-step stochastic world model을 test-time planning에 쓸 때, m을 고르는 기준과 rollout이 token manifold를 벗어나는지 재는 방법을 그대로 가져다 쓸 수 있음.

*대표 그림: 4방향 bounce 과제의 context 6개에서 regression, FM-20, FM-2, IMLE이 낸 샘플(빨강)을 실제 mode(초록 원) 위에 찍은 그림임. regression은 mode 사이 한 점에, flow 계열은 mode 사이에 흩어지고, IMLE 샘플은 mode 위에 모임.*

---

### 13. RAIL: Representation-Aligned Imitation Learning for Student-Compatible Teacher Policies (72점)

[arXiv](https://arxiv.org/abs/2611.12251) · [PDF](https://arxiv.org/pdf/2611.12251) · [alphaXiv](https://www.alphaxiv.org/abs/2611.12251) (요약 있음) · [프로젝트 페이지](https://merajmammadov.com/rail/) · [코드](https://github.com/meraccos/RAIL)

- **저자**: Meraj Mammadov, Pedro Zuidberg Dos Martires, Johannes Andreas Stork
- **분야**: RL · robotics relevance 8/10 · 1차 스크리닝 70점
- **학회**: NeurIPS 2026 채택 · 근거: comments에 "18 pages, 3 figures. Accepted at NeurIPS 2026"
- **읽은 원문**: PDF 전문

> privileged 정보를 보는 teacher가 student도 복원할 수 있는 정보만 담은 공유 latent를 입력으로 받아 처음부터 RL로 학습하게 해서, student가 그대로 따라 할 수 있는 teacher를 만듦. TunnelVision에서 student 성공률이 가장 강한 기존 방법 SITT의 0.74에서 1.00으로 오름.

**무슨 문제인가**

이미지나 제한된 센서 입력으로 RL을 직접 하면 관측 차원이 크고 reward가 드물어 학습이 어려움. 그래서 privileged state를 보는 teacher를 RL로 먼저 학습하고, 그 행동을 student policy로 distillation하는 방식을 흔히 씀. 그런데 teacher가 student가 볼 수 없는 정보로 행동을 고르면, student 관측만으로는 같은 행동을 낼 수 없는 상태가 생김(irreducible imitation gap). 기존 방법은 teacher 학습이 끝난 뒤 student 쪽 RL objective에 teacher 신호를 더하거나 reward를 다시 설계해 차이를 메우므로, RL 비용이 다시 들고 정보 차이 자체는 남음.

**어떻게 푸나**

RAIL(Representation-Aligned Imitation Learning)은 teacher가 student도 복원할 수 있는 정보만 보고 행동하도록 teacher policy의 입력을 제한함. teacher 관측과 student 관측은 각자의 encoder와 공유 encoder를 거쳐 같은 latent 공간의 embedding이 되고, 하나의 policy가 이 embedding을 입력으로 받아 행동을 냄. 같은 상태에서 나온 teacher와 student 관측 쌍은 contrastive loss(InfoNCE)로 가깝게, 다른 상태의 관측은 멀게 학습함. 여기에 쌍의 cosine 유사도를 직접 높이는 alignment loss와, encoder가 바뀌어도 policy 출력이 덜 바뀌게 하는 stability loss를 더함. 매 iteration마다 teacher로 rollout을 모으고, policy를 고정한 채 encoder를 갱신한 뒤, encoder를 고정하고 PPO로 policy를 갱신함. RL gradient를 encoder로 흘려보내지 않는 것이 teacher 전용 정보가 latent에 들어가는 것을 막는 장치이고, 배포할 때는 같은 policy에 student embedding만 넣음.

**결과**

- 시뮬레이션 환경 4개에서 비교함. TunnelVision(장애물 격자에서 teacher는 주변 9칸, student는 앞쪽 3칸만 보는 내비게이션)에서 student 성공률은 DAgger가 0.15, BC가 0.12로 RAIL과 SITT보다 낮음. CollectHealth(student가 1인칭 RGB 이미지만 보고 상자 5개를 모으는 3D 방 과제)에서는 RAIL 0.98, DAgger 0.84, SITT 0.49임.
- QuarterCheetah(이미지 왼쪽 절반이 가려진 HalfCheetah 달리기)의 student return은 RAIL이 2510.24로, student 관측으로 직접 RL을 한 경우의 1824.27보다 높음. SITT는 student return이 721.12이고 teacher return도 962.67로 내려가지만, RAIL teacher는 2627.67을 유지함.
- RL gradient가 encoder를 갱신하게 둔 변형은 TunnelVision teacher 성공률이 0.99로 높아도 student는 0.18로 내려감. Corners(teacher만 목표 모서리를 아는 격자 과제)에서 teacher embedding에 probe를 붙이면 목표 모서리 정확도는 25.4%로 우연 수준 25%와 비슷함. student도 볼 수 있는 agent 위치는 100% 맞힘.
- encoder를 고정하고 teacher 관측만으로 새 과제 policy를 학습해 student에 그대로 옮기면, CollectHealthPlus에서 성공률 0.83으로 새 과제에 RAIL 전체를 다시 학습한 0.84와 비슷함. 모든 수치는 학습 seed 5개 평균임.

**한계**

실험은 시뮬레이션 환경 4개뿐이고, 그중 3개는 격자나 단순한 3D 방 안의 내비게이션임. 같은 상태에서 나온 teacher와 student 관측 쌍이 있어야 하고, teacher 행동이 student로 완전히 재현된다는 이론적 보장은 없음. 실로봇 실험은 없고, 새 과제 재사용도 같은 환경과 같은 관측 공간 안에서만 확인함.

**누리랩 연구와의 연결**

- simulation에서 privileged state로 teacher를 학습해 이미지 기반 manipulation policy로 옮기는 teacher-student distillation에 바로 넣어 볼 수 있는 방법임.
- 영상에서 teacher가 시야가 좁은 student에 맞춰 방향을 돌려 주변을 확인하는 모습은, 관측을 얻는 행동을 고르는 active perception 연구의 비교 대상이 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림으로, 한 환경 상태에서 나온 student 시점 이미지와 teacher의 상자 좌표 관측이 각자의 encoder와 공유 encoder를 거쳐 같은 latent 공간으로 감. 오른쪽은 하나의 shared policy network가 두 embedding에서 행동 분포를 내고, encoder 갱신 전 출력과 비교하는 stability loss가 걸리는 구조임.*

*영상: [저자 프로젝트 페이지의 TunnelVision 영상으로, RAIL teacher가 방향을 돌려 주변 칸을 확인하며 목표로 가는 모습임.](https://blog-media.assets.alphaxiv.org/videos/01a1c44d-d5fa-7a42-960e-6ed6054dd771/22ae4ffb-f44a-4c28-8d79-7c7b51ddece9) (alphaXiv 요약에서 가져옴)*

---

### 14. DexForesight: Grounding Dexterous Policies with Implicit Spatial Foresight (70점)

[arXiv](https://arxiv.org/abs/2611.11166) · [PDF](https://arxiv.org/pdf/2611.11166) · [alphaXiv](https://www.alphaxiv.org/abs/2611.11166) (요약 있음) · [프로젝트 페이지](https://dexforesight.github.io/)

- **저자**: Zhongxi Chen, Yi Yang, Xinyi Chen, Mingzhe Ye, Yaping Li, Zhihong Liu, Congsheng Xu, Haonan Wang 외 1명
- **분야**: Manipulation · robotics relevance 9/10 · 1차 스크리닝 68점
- **읽은 원문**: PDF 전문

> 다지 손 policy가 미래를 생성하지 않고도 손과 장면의 변화를 내다보도록, 학습 때만 쓰는 공간 world model의 내부 feature에 policy query를 맞추게 함. DexJoCo 11개 과제 전체 성공률이 base policy GR00T N1.7의 49.4%에서 60.5%로 오름.

**무슨 문제인가**

다지 손으로 물체를 다루려면 행동에 따라 손가락과 물체가 어떻게 움직일지 미리 알아야 함. 손가락 일부는 카메라에 가려지므로 현재 장면 인식만으로는 부족함. 미래 영상이나 상태를 생성해 행동을 고르는 world action model(WAM)은 매 제어 단계마다 생성 계산이 들고, 행동과 무관한 texture나 배경까지 복원해야 함. depth를 입력으로 받는 policy는 배포 때에도 depth 추정 pipeline에 기대게 됨.

**어떻게 푸나**

DexForesight는 학습 때만 쓰는 공간 world model과 배포용 policy를 분리함. world model은 RGB, offline으로 추정한 장면 depth, 손 URDF link에 고정한 점들의 위치, 언어를 입력으로 받음. 손 점 위치는 기록된 joint state에서 forward kinematics로 계산하므로 카메라에 가린 손가락도 포함됨. 여기에 시연 행동을 조건으로 넣어, 16 frame 안의 미래 시점에서 손 점의 3D 변위(hand flow)와 DINOv3 시각 feature의 변화를 예측하게 학습함. 그다음 world model을 고정하고, policy VLM 중간층에 학습 가능한 query token(policy query)을 붙임. 이 query가 world model 쪽 query token(world query)과 같아지도록 query별 cosine 유사도와 query 간 유사도 행렬을 맞춤. 맞춘 policy query는 action expert의 context에 덧붙여 행동 생성에 쓰이고, 배포 때는 world model과 depth 없이 RGB, 언어, robot state만 받음.

**결과**

- DexJoCo(MuJoCo 기반 단팔·양팔 다지 조작 benchmark) 11개 과제, 과제당 100회 평가에서 가장 강한 baseline인 Fast-WAM은 50.9%, Cosmos3는 49.5%임.
- 같은 예측 목표를 GR00T에 head로 직접 붙인 대조군은 더 낮음. hand flow head는 53.1%, hand flow와 DINO head를 함께 붙이면 49.5%임. world model(teacher)에 조건으로 넣는 시연 행동의 순서를 뒤섞은 변형은 41.5%로 base보다 내려감.
- 고정한 실로봇 policy feature에서 0.54초 뒤 손 점 변위를 linear probe로 예측함. 오차가 action만 학습한 QwenVLA의 13.59mm에서 10.01mm로 내림.
- 22-DoF 손을 단 실로봇의 과제 3개(상자 닫기, 배터리 끼우기, 뚜껑 돌려 닫기), 과제당 20회에서 전체 성공률 58.3%를 얻음. 가장 강한 baseline인 WLA는 50.0%, 같은 backbone인 QwenVLA는 30.0%임. 추론 시간은 QwenVLA 227.4ms에서 230.4ms로 늘어남.

**한계**

실로봇 비교 대상인 WLA와 Fast-WAM은 구조와 학습 방식이 달라, 저자도 한 변수만 바꾼 대조가 아님을 밝힘. 실로봇 평가는 한 하드웨어의 과제 3개, 과제당 20회뿐임. world model 학습에 약 370시간의 자체 시연 데이터와 offline depth 추정이 필요하고, depth를 빼면 실로봇 성공률이 43.3%로 내려감.

**누리랩 연구와의 연결**

- 가려진 손가락 움직임을 forward kinematics로 감독하는 hand flow 목표는 dexterous manipulation용 world model의 예측 대상을 정할 때 참고가 됨.
- world model을 배포 때 돌리지 않고 VLA latent로 옮기는 방식이라, test-time 계산 없이 world model 지식을 쓰는 VLA 연구의 비교 대상이 됨. linear probe 실험은 policy latent에 미래 정보가 남았는지 확인하는 도구로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 흐름을 그린 개요 그림임: 60개 과제의 시연으로 Spatial WM이 visual dynamics와 hand flow를 배우고, 그 spatial foresight가 low-level policy로 넘어감. 아래쪽 막대는 시뮬레이션과 실로봇 성공률을 Fast-WAM, Cosmos3와 비교하지만 축 수치는 없음.*

*영상: [양손이 상자 뚜껑을 상자에 맞춰 눌러 닫는 실로봇 Close Box 과제 영상임.](https://blog-media.assets.alphaxiv.org/videos/01a1c881-637e-74de-b5f2-3e15e2be4209/04e65807-52b6-434a-a488-04e45db8c07c) (alphaXiv 요약에서 가져옴)*

---

### 15. ForeAct: Geometry-Guided Action Learning from World Representations (68점)

[arXiv](https://arxiv.org/abs/2611.11500) · [PDF](https://arxiv.org/pdf/2611.11500) · [alphaXiv](https://www.alphaxiv.org/abs/2611.11500) (요약 있음)

- **저자**: Wei Lu, Jiaxi Zhang, Yunheng Wang, Taowen Wang, Yuetong Fang, Zhenhui Zhang, Shuning Zhang, Zizhao Yuan 외 3명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 74점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> 사전학습된 video world model을 미래 영상 생성 없이 현재 관측에 한 번만 통과시키고, 학습 때만 다음 frame depth를 맞히게 하는 token을 붙여 action feature를 만듦. LIBERO 평균 성공률 96.6%를 168ms latency로 얻음.

**무슨 문제인가**

video 생성 모델로 action을 함께 내는 world action model(WAM)은 미래 frame을 여러 step denoising해서 얻은 feature로 action을 고르므로 추론이 느림. 이 feature는 장면의 3차원 구조를 따로 담지 않음. 반대로 depth나 3D foundation model의 feature를 쓰는 geometry 중심 policy는 별도 backbone이 들어가 parameter와 계산이 늘어남. 또 geometry 중심 policy는 지금 보이는 구조만 복원하므로 행동 뒤에 장면 구조가 어떻게 바뀔지는 따로 학습하지 않음.

**어떻게 푸나**

ForeAct는 RGB 이미지 한 장과 언어 지시를 받아 H step 길이의 action chunk를 내고, proprioceptive state는 쓰지 않음. 이미지를 고정된 video VAE로 encoding한 깨끗한 latent를 Cosmos-Predict2-2B backbone에 noise 없는 끝점(diffusion timestep 0)으로 한 번만 넣음. 이때 학습 가능한 geometry token 8개를 visual token과 함께 넣고, 둘은 양방향 self-attention으로 서로 정보를 주고받음. 출력 visual token은 flow matching 방식의 action DiT에 들어가 action을 만듦. 학습 때만 geometry token을 작은 decoder로 읽어 다음 frame의 상대 depth를 예측하게 함. 정답 depth는 MoGe-3(단안 depth 추정 모델)로 미리 만들어 둠. 이 depth 신호가 attention을 거쳐 action에 쓰이는 visual feature를 바꾸고, 배포 때는 depth decoder를 떼어 내므로 depth를 계산하지 않음.

**결과**

- 같은 backbone 안에서 설계를 바꾼 LIBERO(시뮬레이션 Franka 조작, suite 4개) 실험에서 평균 성공률이 geometry token과 depth 감독이 모두 없는 기준 94.3%에서 ForeAct 96.6%로 오름. 미래 frame을 denoising하는 diffusion WAM 변형은 93.2%, depth 감독 없이 token만 넣으면 94.7%, 한 방향 attention이면 94.9%임.
- 로봇 action 대규모 사전학습 없이 얻은 LIBERO 평균 96.6%는 Fast-WAM 97.6%, Cosmos Policy 98.5%보다 낮음. 단일 H20 GPU 기준 latency는 168ms이고, 저자는 Cosmos Policy의 약 3분의 1이라고 적음. 이 표는 다른 논문 수치를 모은 비교임.
- SimplerEnv-Bridge(WidowX 로봇 시뮬레이션 과제 4개)에서 평균 성공률 63.5%로 GR00T N1.5의 61.9%보다 1.6퍼센트포인트 높음. Stack Blocks는 12.5%로 GR00T N1.5의 57.0%보다 낮음.
- 실제 Franka 로봇 과제 6개를 과제당 15회씩 시도함. 90회 중 성공이 ForeAct 67회(74.4%), Fast-WAM 58회(64.4%), π0 52회(57.8%)임.

**한계**

LIBERO의 대표 비교는 다른 논문 수치를 옮긴 것이고, ForeAct는 가장 강한 world action model 둘보다 평균이 낮음. 실로봇 실험은 카메라 1대, 과제 6개, 과제당 15회 규모이고 방법끼리의 통계적 차이는 보이지 않음. 첫 쪽에 GitHub와 HuggingFace 표시는 있으나 텍스트에서 주소는 확인 불가함.

**누리랩 연구와의 연결**

- video world model을 미래 상상 없이 한 번 통과시킨 feature만 VLA backbone으로 쓰는 방식임. world model을 test-time planning 없이 policy representation으로 쓸 때의 비교 대상으로 쓸 수 있음.
- 학습 때만 다음 frame depth를 예측시키는 보조 감독은, 배포 비용 없이 future-aware 3D 정보를 policy에 넣는 방법임. object-centric 3D representation이나 failure 예측용 보조 head 설계에 그대로 적용해 볼 수 있음.

*대표 그림: 측정 결과가 아니라 backbone 구조 세 가지를 비교한 개념도임. 여러 step denoising하는 video WAM, 3D model feature를 쓰는 geometry 중심 구조, 학습 token을 depth로 읽으면서 world model을 한 번만 통과시키는 ForeAct를 위에서부터 (a), (b), (c) 순서로 그림.*

---

## 오늘의 흐름

- **world model을 생성기가 아니라 고르는 도구로 씀**: 미래 영상을 길게 만들지 않고, 행동 후보나 시점 이동의 결과를 latent 공간에서 짧게 rollout해 하나를 고르는 데 world model을 씀. [WARP-JEPA](https://arxiv.org/abs/2611.10806), [Tiresias](https://arxiv.org/abs/2611.10392), [WorldMind](https://arxiv.org/abs/2611.10151)가 이 방식임.
- **world model 지식을 학습 때만 policy에 옮김**: 배포 때는 world model을 돌리지 않고, 학습 때만 미래 depth나 손 움직임 예측을 보조 목표로 붙여 policy feature에 미래 정보를 넣음. [ForeAct](https://arxiv.org/abs/2611.11500), [DexForesight](https://arxiv.org/abs/2611.11166), [SWAM](https://arxiv.org/abs/2611.12870)이 여기에 속함.
- **VLA 내부 activation으로 실패를 감지하고 고침**: VLA의 중간 activation으로 실패를 감지하거나 원인을 설명함. 배포 뒤에도 감지기를 계속 갱신하고, 지시문 해석 오류를 가중치 편집으로 고치기도 함. [MIND](https://arxiv.org/abs/2611.10400), [Streaming Failure Forecasting](https://arxiv.org/abs/2611.11688), [Distilling Instructions into Weights](https://arxiv.org/abs/2611.11894)가 이 흐름임.
- **가중치를 고정하고 test-time에만 행동을 바꿈**: policy는 그대로 두고, 이상 점수를 reward로 학습한 Q 함수의 gradient(Q-steering)나 텍스트 메모리로 행동을 조정함. [GUARD](https://arxiv.org/abs/2611.10343)와 [RoboScript](https://arxiv.org/abs/2611.12885)가 이런 방식임.

## 해볼 만한 연구

### 내부 feature 실패 감지를 test-time 행동 조정 신호로 쓰기
- 질문: VLA 중간 activation을 sparse autoencoder로 나눈 feature로 잰 실패 점수를 reward로 바꾸면, 가중치를 고치지 않고 실패를 미리 피할 수 있는지 밝힘.
- 첫 실험: LIBERO(시뮬레이션 조작 과제 모음)에서 π0.5의 내부 feature 실패 점수와 관측 기반 이상 점수를 각각 reward로 써서 Q-steering 성공률을 비교함.
- 가장 가까운 연구: [GUARD](https://arxiv.org/abs/2611.10343)는 관측 분포의 이상 점수만 쓰고, [MIND](https://arxiv.org/abs/2611.10400)는 감지와 설명에서 멈춤. MIND식 내부 feature 실패 점수를 행동 조정의 reward로 쓰는 점이 다름.

### world model 예측 cost와 실제 실패의 어긋남 재기
- 질문: world model planning에서 예측 cost가 낮은데 실제로 실패하는 경우가 얼마나 되고, 이를 감지기로 걸러낼 수 있는지 밝힘.
- 첫 실험: latent 공간에서 다음 상태를 예측하는 고정 JEPA world model에서, 후보 행동열 생성기(proposer)가 고른 계획의 예측 cost와 실제 성공 여부를 짝지어 기록함. 실패 감지기로 걸러낸 뒤의 실패 비율을 감지기 없을 때와 비교함.
- 가장 가까운 연구: [WARP-JEPA](https://arxiv.org/abs/2611.10806)는 이 어긋남을 관찰만 했고, [Streaming Failure Forecasting](https://arxiv.org/abs/2611.11688)은 world model 없이 VLA activation만 봄. world model의 예측 cost와 실제 실패의 차이를 직접 재는 점이 다름.

### simulator 대신 world model 안에서 텍스트 메모리 고치기
- 질문: 시연 1개로 텍스트 메모리를 고쳐 가는 학습을 simulator 대신 학습된 world model 안에서 해도 성공률이 유지되는지 밝힘.
- 첫 실험: RoboTwin 2.0(양팔 로봇 조작 시뮬레이션 과제 모음) 과제 일부에서, simulator 연습과 video world model 연습으로 각각 만든 텍스트 메모리(Task Memory)의 성공률을 비교함.
- 가장 가까운 연구: [RoboScript](https://arxiv.org/abs/2611.12885)는 정확한 simulator에 기대고, [Tiresias](https://arxiv.org/abs/2611.10392)는 world model을 후보 선택에만 씀. 부정확한 world model에서 연습한 메모리가 실제 과제로 옮겨 가는지 재는 점이 다름.

## 꼭 읽을 논문

- [RoboScript (World In-Context Learning for Agentic Robot Manipulation)](https://arxiv.org/abs/2611.12885): 고정된 foundation model이 시연 1개와 simulator 연습만으로 RoboTwin 2.0 평균 성공률 83.4%를 얻음. 시연 50개로 학습한 가장 강한 policy는 61.7%임.
- [MIND (Detecting and Explaining Robot Policy Failures from Sparse Internal Features)](https://arxiv.org/abs/2611.10400): 실패 감지와 원인 설명을 VLA 내부의 같은 feature로 함.
- [Streaming Failure Forecasting](https://arxiv.org/abs/2611.11688): 배포 뒤 실패 감지기를 episode마다 성공·실패 label 하나만으로 계속 갱신하는 방법을 실로봇 기록으로 보임.
- [Learning Heterogeneous Tactile Representation for General Dexterous Manipulation](https://arxiv.org/abs/2611.12806): 서로 다른 촉각 센서 데이터 5,000시간으로 만든 고정 encoder를 policy 4종에 붙여 실로봇 성공률을 올림.
- [WARP-JEPA](https://arxiv.org/abs/2611.10806): world model planning의 test-time gradient 탐색을 학습된 후보 생성으로 바꿔, 장기 과제의 episode 시간을 9.6~18.8배 줄임.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (949편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2611.10806'>WARP-JEPA: World-Model-in-the-Loop Amortized Rollout Planning for Frozen Hierarchical Joint-Embedding Predictive Architectures</a></td><td>82</td><td>8</td><td>World Model</td><td>frozen H-JEPA world model의 test-time gradient planning을 학습된 multi-candidate proposer로 대체해 9.6-18.8배 빠르고 성공률 최대 33.3pt 향상한 inference-time planning 연구</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2611.10151'>WorldMind: Test-Time Scaling for Visual Spatial Reasoning through Latent World Simulation</a></td><td>78</td><td>7</td><td>World Model</td><td>VLM이 공간 변환을 고르고 world model이 latent feature를 직접 돌려줘 pixel 디코딩 없이 test-time 공간 추론을 확장, VSI-Bench 등에서 base 대비 16.0% 향상, embodied spatial reasoning에 직결</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2611.12870'>SWAM: Scaling World Action Models with Cross-Modal Alignment</a></td><td>76</td><td>9</td><td>World Model</td><td>world action model의 언어-영상 정렬을 scaling하는 연구, 우선 주제에 부합</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2611.11688'>Streaming Failure Forecasting: VLA Failure Monitors That Keep Learning After Deployment</a></td><td>75</td><td>9</td><td>VLA</td><td>배포 후에도 학습하는 streaming VLA failure monitor로 failure detection 우선 주제임</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2611.11500'>ForeAct: Geometry-Guided Action Learning from World Representations</a></td><td>74</td><td>9</td><td>Manipulation</td><td>world representation에서 기하 유도 action 학습, 조작과 world action 연결</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2611.10400'>Detecting and Explaining Robot Policy Failures from Sparse Internal Features</a></td><td>74</td><td>9</td><td>Failure Detection</td><td>희소 내부 feature로 policy 실패를 탐지하고 설명하는 우선 주제 연구임</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2611.10392'>Tiresias: Towards Language-Conditioned World Models</a></td><td>74</td><td>8</td><td>World Model</td><td>언어 조건 world model 구축, planning과 언어 지시 결합</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2611.12885'>World In-Context Learning for Agentic Robot Manipulation</a></td><td>72</td><td>9</td><td>Manipulation</td><td>world model 기반 in-context learning으로 가중치 학습 없이 조작 수행하는 시도임</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2611.12806'>Learning Heterogeneous Tactile Representation for General Dexterous Manipulation</a></td><td>72</td><td>9</td><td>Manipulation</td><td>이질적 tactile 표현을 dexterous manipulation에 일반화하려는 우선 주제 연구임</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2611.11887'>How Many Candidates Does a One-Step World Model Need? A Random-Codebook Account of Nearest-of-m Training on Frozen DINO Tokens</a></td><td>72</td><td>8</td><td>World Model</td><td>frozen DINO token 위 one-step world model에서 nearest-of-m 학습을 random codebook 왜곡으로 설명하고 m=16이 50-step flow보다 1/30 지연으로 coverage가 좋음을 보이며 Push-T 계획 실패까지 보고함</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2611.12087'>Compass 1: Towards Open-World and Persistent Embodied Navigation from Monocular RGB Videos</a></td><td>70</td><td>9</td><td>Navigation</td><td>monocular RGB 영상 기반 open-world 지속 navigation, 우선 주제에 부합</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2611.10343'>GUARD: Anomaly-Informed Q-Steering for Generative Robot Policies in Dexterous Manipulation</a></td><td>70</td><td>9</td><td>Manipulation</td><td>이상 정보로 생성 policy를 Q-steering하는 inference-time 개선임</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2611.12251'>RAIL: Representation-Aligned Imitation Learning for Student-Compatible Teacher Policies</a></td><td>70</td><td>8</td><td>RL/IL</td><td>teacher와 student 관측의 공유 latent를 contrastive로 학습하고 teacher를 그 공간에서 훈련해 privileged distillation의 imitation gap을 줄이는 방식이며 로봇 policy distillation에 직접 유용함</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2611.11894'>Distilling Instructions into Weights: Closed-Form Edits Fix a Robot Policy&#x27;s Misreading</a></td><td>68</td><td>9</td><td>VLA</td><td>단일 step 실패를 closed-form weight 편집으로 고치는 failure recovery 관점 연구임</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2611.11166'>DexForesight: Grounding Dexterous Policies with Implicit Spatial Foresight</a></td><td>68</td><td>9</td><td>Manipulation</td><td>dexterous world-action model에 암묵적 공간 foresight를 부여함</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2611.10967'>BAT-WAM: Bridging Action and Touch in World-Action Models for Dexterous Hands</a></td><td>68</td><td>9</td><td>Manipulation</td><td>world action model에 touch를 연결한 dexterous 촉각 통합임</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2611.12732'>$Σ$-LeWM: Learning World Models via S-Information for Robot Control</a></td><td>68</td><td>8</td><td>World Model</td><td>로봇 제어용 world model을 S-information으로 학습, 조작 과제 대상</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2611.11921'>An Evaluation of Tabular Foundation Models as Training-Free World Models</a></td><td>68</td><td>8</td><td>World Model</td><td>tabular foundation model을 next-state in-context regression 기반 training-free world model로 평가해 locomotion에서 LSTM을 앞서는 조건과 rollout 한계를 정직하게 보여 world model 관점에서 유익함</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2611.11085'>ObjectWorld: Scaling Object-Centric World Models with A Large-Scale 3D Full-Object Flow Dataset</a></td><td>68</td><td>8</td><td>World Model</td><td>대규모 3D object flow 데이터로 object-centric world model을 scale함</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2611.11344'>Spatial Harness: Grounding Spatial Reasoning in Executable World States with Physics Engines</a></td><td>68</td><td>7</td><td>Embodied AI</td><td>scene을 physics engine의 실행 가능한 world state로 만들어 VLM 공간 추론을 검증하는 Spatial Harness, MindCube 52.70%에서 71.14%로 올려 embodied spatial reasoning에 적합</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2611.12678'>Library of Hands: Fix the Hands, Not the World Model</a></td><td>66</td><td>8</td><td>World Model</td><td>world model 오류를 손 쪽에서 고치는 접근으로 planning과 world model 신뢰성을 다룸</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2611.11869'>Action Representation for Spatial Generalization in Robot World Models</a></td><td>66</td><td>8</td><td>World Model</td><td>robot world model의 공간 일반화를 위한 action 표현을 분석함</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2611.12879'>Grasping the Future: Joint 3D Hand-Object Forecasting From Internet Videos</a></td><td>66</td><td>7</td><td>Manipulation</td><td>인터넷 영상으로 3D 손-물체 동시 예측, 조작 학습 데이터원으로 유용</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2611.12334'>Rethinking Radar 3D Perception: Representation Learning from Raw Spectra</a></td><td>66</td><td>7</td><td>3D Vision</td><td>raw radar spectrum을 Doppler 포함 x-y-D 표현과 leakage-aware masked autoencoder로 self-supervised 학습, 자율주행 3D 인지에 새 representation 제시</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2611.11856'>DeltaForge: A Post-hoc Mixture-of-Experts VLA for Multi-Domain Autonomous Driving</a></td><td>66</td><td>6</td><td>VLA</td><td>도메인별 finetune된 주행 VLA N개를 SVD 공유 기저와 소형 router로 post-hoc MoE로 합침, 주행 VLA 통합에 실용적이나 조작 로봇과는 거리 있음</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2611.10987'>Horizon-Scalable Q-Learning</a></td><td>66</td><td>6</td><td>RL</td><td>offline Q-learning에서 critic이 best-of-N BC 행동보다 높게 평가할 때만 multi-step target을 확장하는 HQL임. density 없이 flow/diffusion policy와 호환되고 OGBench long-horizon에서 우위를 보여 skill/장기 계획 RL에 직접 관련됨</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2611.10552'>Seeing Isn&#x27;t Enough: Unlocking Visual Reasoning by Bridging the Reasoning-Access Gap with TIGER</a></td><td>66</td><td>5</td><td>Multimodal</td><td>텍스트는 풀고 렌더링 이미지는 못 푸는 reasoning-access gap을 modality counterfactual로 채굴해 GRPO로 메우고 RoboSpatial-Home까지 향상, 합성 데이터만으로 일반화한 점이 좋음</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2611.12286'>VLA-MOPD: On-Policy Distillation for Multi-Task VLA Policy Consolidation</a></td><td>65</td><td>9</td><td>VLA</td><td>on-policy distillation으로 multi-task VLA를 통합하는 시도로 VLA continual 주제와 맞음</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2611.10660'>Dynamics-Informed Action Learning for Goal-Conditioned Latent Planning</a></td><td>65</td><td>8</td><td>World Model</td><td>latent world model에서 dynamics 기반 action 학습, goal-conditioned planning</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2611.11854'>Decoupled Asynchronous System for Humanoids (DASH): Latency-Agnostic Scaling of Vision-Language-Action Models for Humanoid Manipulation</a></td><td>62</td><td>9</td><td>VLA</td><td>VLA backbone 지연을 분리하는 비동기 구조로 humanoid 조작 efficient inference를 다룸</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2611.11798'>PAIR: Proprioception-Aligned Image-Ray Representations for Viewpoint-Robust Manipulation</a></td><td>62</td><td>9</td><td>Manipulation</td><td>proprioception 정렬 image-ray 표현으로 viewpoint 강건한 조작을 노림</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2611.10894'>Zero-Shot VLA Adaptation with Retrieved Guidance</a></td><td>62</td><td>9</td><td>VLA</td><td>retrieved guidance로 VLA를 zero-shot 적응시키는 inference-time 접근임</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2611.10510'>ReSkill: Selective Self-Improvement for Robot Manipulation</a></td><td>62</td><td>9</td><td>Manipulation</td><td>재사용과 개선 대상을 고르는 선택적 self-improvement로 skill chaining과 닿음</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2611.10148'>BATCH: Behavior Alignment for Cross-Embodiment Learning from Humans</a></td><td>62</td><td>9</td><td>IL</td><td>인간 시연에서 cross-embodiment 행동 정렬을 학습하는 방법임</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2611.10547'>HSGNav: Hypothesis Scene Graphs for Multi-Scale Lifelong Navigation under Object Relocation</a></td><td>62</td><td>8</td><td>Navigation</td><td>hypothesis scene graph로 물체 재배치 하 lifelong navigation을 다룸</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2611.10410'>SimDuoReal: Object-Centric Bimanual Policy for Emergent Dexterity</a></td><td>62</td><td>8</td><td>Manipulation</td><td>object-centric bimanual dexterity를 sim-to-real로 학습함</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2611.10280'>Who Taught the Robot That? Removing One User&#x27;s Corrections from a Robot Policy That Learns Online</a></td><td>62</td><td>8</td><td>IL</td><td>온라인 학습 policy에서 특정 사용자 교정을 제거하는 새로운 unlearning 문제 설정임</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2611.10769'>Look Ahead: Search-Driven Reasoning in Embodied AI</a></td><td>62</td><td>8</td><td>Manipulation</td><td>frozen ACT policy에 beam search와 OSA gate로 선택적 test-time search를 적용해 PushT 성공률 0에서 18%로 올림, 단 시뮬레이션 단일 과제이고 규모 작음</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2611.12353'>QCC-WM: Linking Macro-State Dynamics and Visual Generation via Quotient Causal Construction</a></td><td>62</td><td>7</td><td>World Model</td><td>action-conditioned world model의 macro-state를 인과 구조로 구성, 새 formulation</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2611.11304'>TransArt3D: From Two States to Articulated 3D Reconstruction with Video Transition Priors</a></td><td>62</td><td>7</td><td>3D Vision</td><td>두 상태 영상으로 articulated 자산 재구성, 로봇/시뮬레이션 interactable asset</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2611.12324'>How Many Exposures Does a World Model Need? Learning Unseen Game Mechanics at Test Time</a></td><td>62</td><td>6</td><td>World Model</td><td>ARC-AGI-3에서 world model이 새 mechanic을 몇 번 노출로 배우는지 test-time 전체 업데이트로 측정하며 test-time 학습 world model 관점이 유용하나 게임 도메인임</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2611.11532'>DriveFoundry: Co-Evolving Data and Model for Efficient Closed-Loop Iteration in Autonomous Driving</a></td><td>62</td><td>6</td><td>Embodied AI</td><td>counterfactual 주석 데이터 엔진과 value-of-computation head로 토큰을 28%만 쓰고도 추론 성능을 맞추는 DriveFoundry, 실차 시험까지 있으나 자율주행 범위임</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2611.10443'>Spatial Representation Distillation and Knowledge Routing for Vision-Language-Action Models</a></td><td>60</td><td>9</td><td>VLA</td><td>3D 공간 표현을 VLA로 distillation하고 routing하는 방법임</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2611.12136'>LHNav: Long-Horizon Humanoid Navigation via Multirate Coordination and Physics-Grounded Action Data</a></td><td>60</td><td>8</td><td>Navigation</td><td>humanoid long-horizon 언어 navigation을 multirate 구조와 물리 기반 데이터로 풂</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2611.12113'>Motion Belief Action: From a Visual Scene Map to Physical Decisions</a></td><td>60</td><td>8</td><td>Embodied AI</td><td>가려진 물체의 위치 belief를 행동 결정에 연결하는 시도로 memory 및 belief 주제와 닿음</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2611.11509'>Review the Episodes, Refine the Lessons: Simple Memory Evolution for Embodied Agents</a></td><td>60</td><td>8</td><td>Embodied AI</td><td>에피소드 복기로 memory를 진화시키는 embodied agent 방법으로 robot memory와 맞음</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2611.10949'>Explicitly capturing demonstrator multi-modality for distillation into diffusion policies</a></td><td>60</td><td>8</td><td>IL</td><td>demonstrator multi-modality를 diffusion policy distillation에 보존함</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2611.10822'>Learning When to Think: Adaptive Internal Computation for Reinforcement Learning</a></td><td>60</td><td>7</td><td>RL</td><td>잠재 표현 refinement를 언제 멈출지 학습하는 AIC로 평균 3.3 step만 쓰고 지연을 31-44% 줄임. PickCube 등 로봇 과제에서 inference-time 연산 배분을 다뤄 efficient inference에 맞으나 규모는 작음</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2611.11605'>ScanDreamer: A Map-Grounded World Model for Quadrotor Navigation</a></td><td>60</td><td>7</td><td>World Model</td><td>map에 기반한 world model로 quadrotor navigation을 하는 응용임</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2611.10877'>Sampling-based Model Predictive Control as Sequential Monte Carlo Inference</a></td><td>60</td><td>7</td><td>Control</td><td>sampling MPC를 SMC 추론으로 통합 해석하는 개념적 정리임</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2611.10632'>Latent-WAM++: Shaping World and Action Representations for End-to-End Autonomous Driving</a></td><td>60</td><td>6</td><td>World Model</td><td>world action model로 주행 표현 학습, 자율주행 한정</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2611.10993'>DPDP: Diffusion Policy-Steered Diffusion Planner for Offline Reinforcement Learning</a></td><td>60</td><td>6</td><td>RL</td><td>offline RL에서 diffusion planner의 inverse dynamics prior를 value 최적화된 diffusion policy로 대체해 long-horizon 내비게이션을 개선하는 DPDP임. planner와 policy의 결합 방식이 참신하나 D4RL 평가임</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2611.10677'>Safe Offline Reinforcement Learning using Behavior Regularisation and Latent Feasibility Guidance</a></td><td>60</td><td>6</td><td>RL</td><td>safe offline RL에서 behavior-regularized 정책 경사와 feasibility 기반 CVAE actor를 결합한 FOCAL임. DSRL 전 과제에서 제약을 만족해 safety-aware 로봇 RL에 참고되나 시뮬레이션 벤치마크 한정임</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2611.12804'>Benchmarking Real-World Robotic Manipulation through Stochastic Challenges</a></td><td>58</td><td>9</td><td>Manipulation</td><td>확률적 도전 과제로 실세계 조작 재현성을 평가하는 benchmark로 기여가 benchmark 중심임</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2611.12102'>SPARK: Simple Post-training for Adapting pRetrained Knowledge to Robot Control</a></td><td>58</td><td>8</td><td>Representation</td><td>foundation 시각 표현을 로봇 제어에 맞게 단순 post-training하는 방법임</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2611.11947'>The Relative Value of Demonstration Data: Execution Time Limits and Operator Mixtures in Behavior Cloning</a></td><td>58</td><td>8</td><td>IL</td><td>demonstration 실행 시간과 operator 혼합의 상대 가치를 분석해 데이터 수집에 도움됨</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2611.11554'>Kimodo-Policy: Learning Kinematic Action Models for Humanoid Loco-Manipulation</a></td><td>58</td><td>8</td><td>Manipulation</td><td>humanoid loco-manipulation용 kinematic action model 학습임</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2611.11438'>When Coding Agents Get Arms: Safety Risks Across the Digital-Physical Boundary</a></td><td>58</td><td>8</td><td>Embodied AI</td><td>coding agent가 로봇 팔을 제어할 때의 안전 위험을 다루는 시의성 있는 분석임</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2611.11089'>Control-Aware Command Generation for Asynchronous Control and Action Inference with Vision-Based Policies towards Fast Execution</a></td><td>58</td><td>8</td><td>VLA</td><td>비동기 제어와 action 추론을 위한 control-aware command 생성임</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2611.10872'>DreamVLA: From Generated Human Motions to Humanoid Vision-Language-Action Policies</a></td><td>58</td><td>8</td><td>VLA</td><td>생성된 인간 동작으로 humanoid VLA를 학습해 데이터 비용을 줄임</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2611.10647'>Which Taxels, Not How Many: Tactile Sensor Placement for Dexterous Policies</a></td><td>58</td><td>8</td><td>Tactile</td><td>어느 taxel이 중요한지 보는 tactile 센서 배치 분석으로 설계 통찰을 줌</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2611.10490'>Tactile Sensors Are an Effective Substitute for Wrist Cameras in Contact-Rich or Occluded Manipulation</a></td><td>58</td><td>8</td><td>Tactile</td><td>tactile이 wrist camera를 대체할 수 있음을 보이는 경험적 비교임</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2611.10061'>UniLatent: Cross-Embodiment Transfer via Latent Observation Alignment</a></td><td>58</td><td>8</td><td>Representation</td><td>latent observation 정렬로 cross-embodiment 전이를 시도함</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2611.12295'>Be My Eye: Learning to See Beyond a Robot&#x27;s Own Perspective</a></td><td>58</td><td>7</td><td>Embodied AI</td><td>multi-robot 부분 관측에서 타 시점을 보완하는 학습으로 active perception과 연결됨</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2611.11780'>Planners Exploit Deterministic Error: Dithered Low-Bit World Models</a></td><td>58</td><td>7</td><td>World Model</td><td>low-bit world model에서 planner가 결정적 오차를 악용하는 현상을 dithering으로 완화함</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2611.10430'>Deploying Physically and Epistemically Compliant Agents by Distilling Belief-Space Task and Motion Planners</a></td><td>58</td><td>7</td><td>Planning</td><td>belief-space TAMP를 policy로 distillation해 규칙 준수 agent를 만듦</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2611.10864'>Stochastic Port-Hamiltonian Gaussian Processes for Learning from Noisy Dynamics on Lie Groups</a></td><td>58</td><td>6</td><td>LG</td><td>Lie group 위에서 port-Hamiltonian 구조를 가진 stochastic GP로 잡음 있는 강체 동역학을 학습함. 특이점 없는 표현과 장기 안정성이 로봇 dynamics 학습에 유용하나 벤치마크가 단순함</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2611.10553'>Meta-Reinforcement Learning with Zero-Shot Reinforcement Learning</a></td><td>58</td><td>6</td><td>RL</td><td>Behavior Foundation Model에 환경 식별과 test-time 탐색을 더해 meta-RL과 겨루는 MetaBFM임. zero-shot RL과 meta-RL을 잇는 test-time 적응이 generalist policy에 맞으나 로봇 실험은 확인 불가임</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2611.11825'>ACROSSVAM3.0: Resource-Bounded 4D Scene Construction and Adaptive Surface Association</a></td><td>58</td><td>6</td><td>3D Vision</td><td>영상 생성, 동적 재구성, 단안 SLAM을 한 GPU에서 묶는 4D scene 구성과 MHAC 표면 연결, RoboTAP 265개 영상에서 평균 Jaccard 0.0610 향상하나 metric scale은 미보장</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2611.10771'>WorldFoundry: Towards Unified Infrastructure for World Intelligence</a></td><td>58</td><td>5</td><td>World Model</td><td>world 시뮬레이션을 위한 통합 인프라, 시스템 기여 위주</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2611.10523'>Action Transfer Across Character Body Plans in Latent-Action World Models: An Empirical Study of Animated Characters</a></td><td>58</td><td>5</td><td>World Model</td><td>latent-action world model의 body plan 간 action transfer 실증, cross-embodiment와 연결</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2611.11516'>Breaking survivorship bias in driving world models</a></td><td>58</td><td>5</td><td>World Model</td><td>driving world model의 survivorship bias를 짚는 신뢰성 분석임</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2611.12200'>Learning to Act with World Models by Valuing What Comes Next</a></td><td>58</td><td>4</td><td>World Model</td><td>WM-PPO가 world model로 예측한 후속 상태를 critic으로 평가해 sparse reward에 보조 advantage를 줌, ALFWorld 63.5에서 87.5로 오르나 텍스트 환경만 다룸</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2611.10423'>Mental Imagery That Matters: Curing Latent Collapse in Multimodal Reasoning</a></td><td>58</td><td>3</td><td>Multimodal</td><td>multimodal reasoning latent collapse 해소, mental simulation 관점</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2611.10543'>Intra-Option Fitted Q-Evaluation: Evaluating Hierarchical Policies from Non-Hierarchical Data</a></td><td>57</td><td>5</td><td>RL</td><td>option 라벨 없는 데이터로 계층 정책을 평가하는 Intra-Option FQE를 제안함. naive FQE의 편향을 제거하고 AntMaze·OGBench Puzzle에서 오차를 낮춰 계층 정책 평가로서 의미 있음</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2611.11011'>Learning Actionable Information Landscapes for Multimodal Active Sensing in Hawkmoths</a></td><td>56</td><td>6</td><td>Embodied AI</td><td>시각·기계감각에서 행동별 uncertainty reduction map을 생성모델로 학습하고 uncertainty-gated 탐색으로 active sensing을 보임. 곤충 시뮬레이션 규모지만 active perception 개념과 맞닿음</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2611.10740'>Evaluating Physically Grounded Procedural Reasoning in VLMs through Real-World Execution: Crochet as a Testbed</a></td><td>56</td><td>5</td><td>Multimodal</td><td>뜨개질 40개 패턴을 직접 떠서 VLM의 physically grounded procedural reasoning 실패를 진단한 점이 참신함, 규모는 작음</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2611.12175'>GeoMind: A Benchmark for Spatial Understanding in Robotic Manipulation</a></td><td>55</td><td>9</td><td>Manipulation</td><td>조작에서의 공간 이해를 측정하는 benchmark로 embodied spatial reasoning과 맞음</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2611.12676'>VLA Adaptation with Real and Simulated Data: A Case Study on Robotic Chess</a></td><td>55</td><td>8</td><td>VLA</td><td>체스 로봇에서 실제와 시뮬 데이터로 VLA를 적응시키는 case study임</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2611.12409'>Bridging Task Planning and Execution for Language-Conditioned Bimanual Manipulation</a></td><td>55</td><td>8</td><td>Manipulation</td><td>언어 조건 bimanual 조작의 planning과 execution을 연결하는 연구임</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2611.12177'>Embodied First Exam</a></td><td>55</td><td>8</td><td>Embodied AI</td><td>coding agent로 로봇을 제어하는 흐름을 평가하는 benchmark 성격임</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2611.12111'>GAP: Generalized Adaptation Prior for Dexterous Piano Playing</a></td><td>55</td><td>8</td><td>Manipulation</td><td>피아노 연주용 dexterous sim-to-real 적응 prior 제안임</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2611.11123'>HARP-Bench: Benchmarking Robot Manipulation Around Active Humans</a></td><td>55</td><td>8</td><td>Manipulation</td><td>사람이 움직이는 환경 조작 benchmark로 의의는 있으나 benchmark 중심임</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2611.10825'>MoE-DAgger: Transition-Aware Router-Entropy Gating for Selective Human Correction in Phase-Structured Manipulation</a></td><td>55</td><td>8</td><td>IL</td><td>router entropy로 선택적 인간 교정을 고르는 DAgger 변형임</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2611.12072'>Learning Contextual Motion Constraints for Object Rearrangement Exploration</a></td><td>55</td><td>7</td><td>Manipulation</td><td>관절 물체의 맥락적 운동 제약을 학습해 rearrangement 탐색에 씀</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2611.11809'>Budget-aware Correspondence-driven View Selection for Real-time 3D Perception of Mobile Robots</a></td><td>55</td><td>7</td><td>3D Vision</td><td>예산 인지 view selection으로 실시간 3D 인식을 하는 active perception 성격임</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2611.11674'>Brain-Aligned Latent Actions: Imposing Premotor Cortex Geometry on a Robot&#x27;s Action Vocabulary</a></td><td>55</td><td>7</td><td>Representation</td><td>premotor cortex 기하를 latent action에 부여하는 신선하나 근거 확인 필요함</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2611.11665'>HINT-VLM: Humanoid Interactive Navigation over Rough Terrain with Embodiment-Grounded Vision-Language Model</a></td><td>55</td><td>7</td><td>Navigation</td><td>embodiment 기반 VLM으로 humanoid 험지 interactive navigation을 수행함</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2611.11169'>Map2SLAM: From Streaming Map Prediction to Real-Time SLAM</a></td><td>55</td><td>6</td><td>3D Vision</td><td>streaming 3D foundation model을 실시간 SLAM으로 확장, loop closure 보정</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2611.10379'>RefineSplat: Reconstruction-Guided Object-Centric Gaussian Splatting for Open-Vocabulary Querying</a></td><td>55</td><td>6</td><td>3D Vision</td><td>object-centric 3DGS 기반 open-vocab 3D 이해, 우선 주제에 부합</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2611.12643'>Simulation-aided Reinforcement Learning with Control Variates</a></td><td>55</td><td>6</td><td>RL</td><td>시뮬레이터 데이터를 control variate로 분산 감소에만 써서 sim 편향을 피하는 RL이며 MuJoCo 실험뿐이나 sim-to-real 관점에서 참고할 만함</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2611.12557'>WanderBench: Can World Models Explore Dynamic Worlds from Video?</a></td><td>55</td><td>5</td><td>World Model</td><td>영상 조건 world model의 동적 장면 탐색 benchmark, real-to-sim과 연결</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2611.11912'>LO-World: Unified BEV Latent Modeling for Joint 4D Occupancy and LiDAR Forecasting</a></td><td>55</td><td>5</td><td>World Model</td><td>BEV latent로 4D occupancy와 LiDAR 예측 통합, 주행 world model</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2611.11517'>InfCoiL: Coordinated Planner-Controller Learning for Closed-Loop Physics-Based Human-Object Interaction</a></td><td>55</td><td>5</td><td>Embodied AI</td><td>planner-controller 공동 학습 기반 physics HOI 생성, 폐루프 제어</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2611.12872'>HiVe-Mem: Interleaving Horizontal Memory Expansion and Vertical Evidence Composition for Multimodal Agents</a></td><td>55</td><td>5</td><td>Multimodal</td><td>multimodal agent의 수평 memory 확장과 수직 증거 구성임</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2611.12411'>PhysOPSD: Code as Privilege for Physically Plausible Video Generation</a></td><td>55</td><td>4</td><td>Video</td><td>코드 기반 privileged 정보로 물리 타당 영상 생성, 물리 world model과 연결</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2611.11604'>Weight-Space Programming of Policies and Their Verification via Model Checking</a></td><td>55</td><td>4</td><td>RL</td><td>LLM이 정책망 가중치를 직접 쓰고 Storm model checker 피드백으로 PCTL 요건을 검증하는 weight-space programming, 검증된 정책 생성이 새로우나 작은 MDP 환경만 다룸</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2611.11020'>Unified Factored Representations Resist Catastrophic Forgetting</a></td><td>55</td><td>3</td><td>LG</td><td>unified factored representation이 fine-tuning 중 catastrophic forgetting을 줄인다는 가설을 1D 회귀·이미지 회귀로 검증함. continual learning에 시사점 있으나 장난감 규모임</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2611.10457'>Represented but Not Used: Value-Policy Dissociation in LLM Agents</a></td><td>55</td><td>3</td><td>RL</td><td>LLM 은닉 상태에서 action value는 선형 복호되지만 policy에 안 쓰이는 value-policy dissociation을 보이고 NVT 개입과 폐루프 제어로 개선, 해석 가능성 관점의 분석</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2611.12426'>dNaViT: Discrete Codes are General-Purpose Visual Representations</a></td><td>55</td><td>2</td><td>Representation</td><td>discrete code를 범용 시각 표현으로 쓰는 시도, 표현 학습 측면</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2611.11821'>Direct Trajectory Optimization for Inference-Time Alignment of Text-to-Image Diffusion Models</a></td><td>55</td><td>2</td><td>Generative</td><td>diffusion inference-time alignment를 trajectory 직접 최적화, test-time optimization 관점</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2611.11962'>Shaping Useful Noise: Energy Distributions Predict Visual Pretraining Quality</a></td><td>55</td><td>2</td><td>CV</td><td>에너지 분포 거리 ELD로 합성 데이터의 사전학습 품질을 FID보다 잘 예측하고 resampling에 쓰는 representation 연구로 로봇 연결은 약함</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2611.11981'>Thermo-VLA: A Thermal-Aware Vision-Language-Action Model with Gated Residual Modulation for Robotic Manipulation</a></td><td>52</td><td>8</td><td>VLA</td><td>thermal 센싱을 gated residual로 VLA에 통합하나 modality 추가 수준임</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2611.11978'>CSG-Nav: Confidence-Aware Semantic-Geometric Fusion for Robust Exploration and Accurate Zero-Shot Object-Goal Navigation</a></td><td>52</td><td>7</td><td>Navigation</td><td>신뢰도 인지 semantic-geometric 융합 zero-shot object-goal navigation임</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2611.11941'>Flip Anything with Agentic Robotics Self-Learning</a></td><td>52</td><td>7</td><td>Manipulation</td><td>뒤집기 skill을 agentic self-learning으로 습득하는 시스템임</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2611.11650'>FlowEval: How Much Adaptation Does an Embodied Foundation Model Need at Deployment?</a></td><td>52</td><td>7</td><td>Embodied AI</td><td>embodied foundation model이 배포 시 필요한 적응량을 측정하는 분석임</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2611.10366'>CPNav: Calibrated Vision-Language Navigation for Object-Goal Search in Unseen Environments</a></td><td>52</td><td>7</td><td>Navigation</td><td>보정된 VLM 기반 object-goal navigation임</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2611.10107'>Beyond Semantic Classes: Online Physical Parameter Estimation via Embedding-Conditioned Gaussian Mixtures</a></td><td>52</td><td>7</td><td>3D Vision</td><td>embedding 조건 Gaussian mixture로 물리 파라미터를 온라인 추정함</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2611.12351'>UniOMA: Unified Optimal-Transport Multi-Modal Structural Alignment for Robot Perception</a></td><td>52</td><td>6</td><td>Representation</td><td>optimal transport로 로봇 인식 multimodal 표현을 정렬하는 연구임</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2611.11732'>Particle Filtering with Generative Trajectory Models for State Estimation and Control</a></td><td>52</td><td>6</td><td>Generative</td><td>생성적 trajectory 모델로 particle filtering 상태 추정과 제어를 함</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2611.12011'>HIST3R: Decomposing and Rectifying State Updates with History for Streaming 3D Reconstruction</a></td><td>52</td><td>5</td><td>3D Vision</td><td>streaming 3D 재구성의 상태 갱신 분해, 로봇 mapping과 연결</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2611.12088'>Zero-Search Reinforcement Learning for Slay the Spire 2 with Failure-Driven Restarts</a></td><td>52</td><td>5</td><td>RL</td><td>Slay the Spire 2에서 실패 지점에서 재시작하는 failure-driven curriculum으로 forward pass 한 번짜리 policy를 학습해 흥미로우나 게임 도메인임</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2611.10870'>Online Imitation Learning for Stabilizing Vlasov--Poisson Plasmas</a></td><td>52</td><td>5</td><td>RL</td><td>부분 관측 플라즈마 안정화에서 online IL(DAgger)과 BC의 오차 누적 분리를 이론으로 보임. imitation learning 이론은 로봇 IL에도 통하나 1D 시뮬레이션뿐임</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2611.11562'>UTOPI: Efficient Egocentric Long-Video Understanding in AR via User-Guided Token Pre-Compression</a></td><td>52</td><td>4</td><td>Video</td><td>AR 안경의 eye-tracking과 움직임 신호로 egocentric 긴 영상 토큰을 95%까지 사전 압축하는 UTOPI, ego-video 효율화이나 로봇 직접 연관은 간접적</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2611.10720'>Locating and Repairing Domain Shift in VLM Trajectory Planning</a></td><td>52</td><td>3</td><td>Embodied AI</td><td>VLM driving planner의 domain shift 위치 진단 후 수리, failure diagnosis 관점</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2611.12825'>MaxIM: Maximally Informative Incremental Summarization via Reinforcement Learning</a></td><td>52</td><td>3</td><td>RL</td><td>bounded memory 요약을 정보이론적 dense reward로 RL 학습하는 MaxIM, credit assignment 해결이 참신하고 memory 연결 있음</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2611.10340'>IdealCache: Rethinking Cache Scheduling in Diffusion Transformers via Ideal Trajectories</a></td><td>52</td><td>3</td><td>Generative</td><td>참조 denoising 경로 모방 대신 이상적 결과 ensemble 위에서 최단 경로로 cache schedule을 찾아 Qwen-Image 6.35배 가속하는 training-free 방법, 효율 추론 기여</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2611.11949'>Watching Itself Watch: Self-Auditing Visual Reliance for Video Reasoning</a></td><td>52</td><td>2</td><td>Video</td><td>영상 reasoning에서 시각 의존도 자기 감사, RL 후학습 개선</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2611.11152'>Full Fine-Tuning is not the Problem: Why Adam Fails and SGD Succeeds in Few-Shot CLIP Adaptation</a></td><td>52</td><td>1</td><td>LG</td><td>few-shot CLIP 적응에서 Adam이 붕괴하고 SGD full fine-tuning이 PEFT를 이김을 preconditioner 오차로 설명함. 분석은 깔끔하나 로봇과 거리 멂</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2611.10994'>RoboMoCap: A Large-Scale Whole-Body Motion Capture Dataset with Egocentric Vision for Robot Learning</a></td><td>50</td><td>8</td><td>Dataset</td><td>egocentric 시각 포함 전신 mocap 대규모 데이터셋으로 기여가 데이터 중심임</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2611.11510'>Reaching Is Not Finding: Map-Anchored Visual Prompting for the Last Mile of Aerial Vision-Language Navigation</a></td><td>50</td><td>7</td><td>Navigation</td><td>aerial VLN에서 지도 기반 visual prompting으로 마지막 탐색 개선</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2611.11868'>Fade to... Red? Scheduling Coloured Noise Exploration Supports Efficient Robot Learning with Reduced Movement Jerk</a></td><td>50</td><td>7</td><td>RL</td><td>colored noise 탐색 스케줄로 RL 효율과 jerk를 줄이는 작은 개선임</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2611.11127'>From Festival Video to the Stage: A Sim-to-Real Ladder for Long-Horizon Expressive Whole-Body Dance on a Commercial Humanoid</a></td><td>50</td><td>7</td><td>Humanoid</td><td>영상에서 humanoid 춤으로 sim-to-real 이식하는 pipeline임</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2611.10451'>Grip, Trace, Write: Force-Aware Imitation and Reinforcement Learning for High-DoF Robotic Handwriting</a></td><td>50</td><td>7</td><td>IL</td><td>힘 인지 IL과 RL로 필기를 수행하는 특수 과제임</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2611.10699'>PLS-GS: Probabilistic Lidar Scaffolds for Compact, Surface-Aligned Gaussian Splatting</a></td><td>50</td><td>6</td><td>3D Vision</td><td>LiDAR scaffold 기반 compact 3DGS, 로봇 mapping 응용</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2611.12567'>LawKAN: Group-Law Layers for Composition -- When Imposing a Known Law Pays Off</a></td><td>50</td><td>6</td><td>Robotics</td><td>SU(2) 군 법칙을 layer에 박고 편차만 학습해 실제 로봇팔 정확도를 올렸으나 회전 합성이라는 좁은 문제임</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2611.11023'>Where Should Models Run? A Collaborative Inference Framework for Embodied Intelligence in 6G</a></td><td>50</td><td>6</td><td>Embodied AI</td><td>OpenVLA-7B 등을 Jetson과 엣지 서버로 분할하는 collaborative inference 최적 지점을 WiFi/5G 실측으로 찾음. VLA 배포 효율 측면에서 실용적이나 방법 novelty는 낮고 서베이 성격임</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2611.12452'>V3DSAM: Semantic-Geometric Loop Verification and Geometry-Anchored Persistent Instance Mapping for Feed-Forward Dense SLAM</a></td><td>50</td><td>6</td><td>3D Vision</td><td>feed-forward dense SLAM의 loop 검증과 instance mapping을 다루는 semantic mapping 연구임</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2611.11521'>K-PWM: Control-Oriented Structured Bilinear World Models under Partial Observation</a></td><td>50</td><td>6</td><td>World Model</td><td>부분 관측 하 제어 지향 bilinear world model 구조임</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2611.10635'>Model-Based Imitation Learning For Monocular Vision-Based Navigation</a></td><td>50</td><td>6</td><td>Navigation</td><td>monocular 시각 navigation에 model-based IL을 적용함</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2611.09937'>Efficient Learning of Differentiable MPC Policies on the GPU via Smoothed ADMM and First-Order Reinforcement Learning</a></td><td>50</td><td>6</td><td>RL</td><td>GPU에서 differentiable MPC policy를 효율 학습하는 방법임</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2611.11136'>From Game Generation to Game Playing: Fully Automated Ability Training for Vision-Language-Action Models</a></td><td>50</td><td>5</td><td>VLA</td><td>게임 자동 생성으로 VLA 능력 학습, 게임 도메인 한정</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2611.12053'>BECON: Belief-Conditioned Constrained Multi-Objective Reinforcement Learning under Drifting Preferences and Budgets</a></td><td>50</td><td>5</td><td>RL</td><td>선호와 안전 예산이 drift하는 상황에서 history로 belief를 추정해 conditioning하는 constrained MORL이며 제어 과제 실험이 시뮬레이션뿐임</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2611.11863'>Can Hindsight Critics Guide Delayed Actors?</a></td><td>50</td><td>5</td><td>RL</td><td>센서 지연 환경에서 hindsight로 정렬한 transition으로 critic을 학습하고 actor는 지연 관측만 쓰는 비대칭 SAC 제안, 로봇 제어 지연에 관련되나 효과가 부분적임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2611.12824'>DreamLander: A 6-DOF World Model based Reinforcement Learning Planetary Lander</a></td><td>50</td><td>5</td><td>World Model</td><td>6-DOF world model 기반 RL 행성 착륙기로 world model 응용이나 조작과 거리 있음</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2611.11091'>Uncertainty-Guided Reward Labeling for Reinforcement Learning under Limited Feedback</a></td><td>50</td><td>4</td><td>RL</td><td>제한된 reward label 환경에서 successor feature로 불확실하고 고가치 상태 도달 가능한 샘플을 골라 라벨링하는 SURE를 제안함. 이론 bound와 offline RL 실험이 있어 RL 관점 가치 있음</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2611.10694'>Perception, Not Reasoning, Limits Visual Theory of Mind</a></td><td>50</td><td>3</td><td>Multimodal</td><td>visual theory of mind 한계가 reasoning이 아니라 perception임을 보임, 분석 가치</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2611.12125'>CARE-PO: Controllable Tool-Call Efficiency for LLM Agents</a></td><td>50</td><td>3</td><td>NLP</td><td>LLM agent tool 호출 비용을 task 난이도 기반 anchor와 effort tag로 제어하는 GRPO 방법이며 agent 효율 관점에서 흥미로우나 로봇과는 거리 있음</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2611.12232'>ECOS: Environment-Calibrated On-Policy Self-Distillation for Language Agents</a></td><td>50</td><td>3</td><td>RL</td><td>환경 결과로 teacher 지침 신뢰도와 self-written skill을 보정하는 on-policy self-distillation, ALFWorld에서 GRPO 대비 향상하나 텍스트 환경 한정</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2611.12886'>Reframe: Observation-Aligned Multi-Teacher On-Policy Distillation for Agentic Visual Reasoning</a></td><td>50</td><td>2</td><td>Multimodal</td><td>visual agent RL와 multi-teacher distillation 결합, 로봇과 거리 있음</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2611.12016'>Speculative Self-Distillation enables Efficient Knowledge Internalization</a></td><td>50</td><td>2</td><td>NLP</td><td>teacher가 divergence가 큰 토큰에서만 개입하는 speculative self-distillation으로 지도 토큰 38-69%를 줄여 지식 내재화 효율을 높임</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2611.10503'>Learning a Unified Cross-Model Semantic Dictionary via Gated Bottleneck Sparse Autoencoders</a></td><td>50</td><td>2</td><td>Multimodal</td><td>ViT·SigLIP·DINOv2·ConvNeXt 사이 공유 dictionary와 모델별 private dictionary를 gated SAE로 분리 학습함. 모델 간 개념 재사용 해석성이 참신하나 로봇과는 간접적임</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2611.12865'>Shortcuts and Boundaries: Verifiable RL Misalignment and Contextual Safety Learning</a></td><td>50</td><td>2</td><td>RL</td><td>verifiable RL에서 reward와 context 충돌로 shortcut이 퍼짐을 보이고 binary 위반 penalty로 안전 완료율 53.1%에서 89.1%로 올림, reward hacking 대응</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2611.11898'>Disagreement-Aware Distribution Matching Distillation for Few-Step Diffusion Models</a></td><td>50</td><td>2</td><td>Generative</td><td>DMD의 teacher-fake 불일치 크기로 고노이즈 구간 update 강도를 조절하는 DA-DMD, SD3.5-L HPSv2 28.23에서 30.93으로 오르는 깔끔한 개선이나 이미지 생성 한정</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2611.12852'>What kills $v$-prediction? A Patch-wise PCA Perspective on Pixel-Space Flow Matching</a></td><td>50</td><td>1</td><td>Generative</td><td>pixel-space flow matching에서 v-prediction 실패 원인을 PCA로 분석, 이론적 통찰</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2611.10866'>The Surprising Effectiveness of Deleting Weights in LLM Post-Training</a></td><td>50</td><td>1</td><td>NLP</td><td>gate projection의 0.05% 미만 weight를 0으로 만드는 mask만으로 full fine-tuning에 맞먹는 Deletion Tuning을 제시함. 망각이 적어 continual 관점에서 흥미로우나 LLM 한정임</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2611.11464'>Off-Policy RL with Online Inference Tuning: My Solution to the CoRL 2026 RoboEval Challenge</a></td><td>48</td><td>7</td><td>RL</td><td>CoRL RoboEval 챌린지 해법 보고로 off-policy RL과 추론 시 튜닝을 사용함</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2611.12038'>DPGS-SLAM: Diffusion-Prior and Provenance-Aware Monocular Gaussian Splatting SLAM for Dynamic Visual Sensing</a></td><td>48</td><td>6</td><td>3D Vision</td><td>diffusion prior를 쓴 동적 환경 monocular 3DGS SLAM임</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2611.11692'>LocateAnyMesh: Grounding 3D Mesh Queries in 2D Images with Vision-Language Models</a></td><td>48</td><td>5</td><td>Multimodal</td><td>mesh 질의로 이미지 내 물체 grounding, 로봇 물체 탐색에 응용 가능</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2611.10917'>Remembering to Reason: Structured Memory for Scene and Workflow Understanding in Robot-Assisted Surgery</a></td><td>48</td><td>5</td><td>Embodied AI</td><td>수술 로봇 영상 이해에 구조화 memory 도입, robot memory 관점</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2611.10239'>DASH-SLAM: Calibration-Free Metric Monocular SLAM via Depth Scale Propagation</a></td><td>48</td><td>5</td><td>3D Vision</td><td>depth scale 전파로 보정 없는 metric monocular SLAM임</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2611.10349'>SituRecBench: Evaluating Frontier Models as Situated Recommendation Assistants in 3D Environments</a></td><td>48</td><td>5</td><td>Embodied AI</td><td>3D 쇼핑 환경에서 VLM이 선호를 묻고 사용자를 목적지로 안내하는 situated recommendation benchmark, 공간 grounding 한계를 보이나 추천 중심</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2611.11499'>JoMoHa: Joint Model--Harness Optimization with Reinforcement Learning</a></td><td>48</td><td>3</td><td>RL</td><td>harness 생성 policy와 task 실행 policy를 RL로 공동 학습하는 JoMoHa, ALFWorld 97.0% 성공이나 언어 agent 한정</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2611.12382'>AutoVLA-D: Learn a Trajectory-Geometric Condition from Reasoning for Autonomous Driving VLA</a></td><td>48</td><td>3</td><td>Autonomous Driving</td><td>driving VLA에 trajectory 기하 조건을 추가하는 incremental 개선임</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2611.10655'>STABLE: A Continual Learning Optimizer with Adaptive Drift Control</a></td><td>48</td><td>2</td><td>LG</td><td>bounded parameter drift를 primal-dual로 강제하는 continual learning optimizer STABLE임. vanilla PEFT가 전용 방법과 맞먹으나 비전/CLIP 분류 한정임</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2611.12109'>SkillDuet: Co-Evolving Models and Skills through Response Feedback</a></td><td>48</td><td>2</td><td>RL</td><td>RL 중 파라미터 갱신과 텍스트 skill 진화를 응답 변화량 Strength로 연결하는 SkillDuet, ALFWorld 98.57%이나 텍스트 환경 한정</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2611.11848'>Causal Signal Credit Assignment for Verilog Code Generation via Counterfactual Hardware Verification</a></td><td>48</td><td>1</td><td>NLP</td><td>Verilog 문장에 5가지 counterfactual 개입을 가해 statement 단위 credit을 얻어 weighted DPO하는 CSCA, 인과적 credit assignment 아이디어는 좋으나 RTL 도메인임</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2611.11581'>Same Error, Different Recovery: How Delivery Changes LLM Agent Behavior</a></td><td>47</td><td>3</td><td>NLP</td><td>같은 도구 오류도 대화 내 전달 위치에 따라 복구 행동이 달라짐을 13개 모델로 통제 실험, failure recovery 관점에서 흥미로우나 코드 agent 한정</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2611.10974'>SWEET: Mitigating Spurious Feature Reliance in LLM Reasoning via Weight Editing</a></td><td>47</td><td>2</td><td>NLP</td><td>counterfactual 쌍으로 spurious feature 뉴런을 찾아 weight editing하는 training-free 방법, causal 관점은 흥미로우나 LLM 한정</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2611.11565'>Actions Should EARN Their Credit: Test-Time Adaptation and Route Consolidation for Frozen LLM Agents</a></td><td>46</td><td>3</td><td>RL</td><td>frozen LLM agent가 반복 달성한 점수의 credit을 줄이고 효과적 action sequence를 조건부 replay하는 EARN, 경험 재사용 아이디어는 있으나 텍스트 게임 한정</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2611.10433'>HexIt: Learning Hexahedral Block Decomposition with Expert Iteration on Combinatorial Maps</a></td><td>46</td><td>3</td><td>RL</td><td>육면체 블록 분해를 3D generalised map 위 순차 결정으로 정의하고 expert iteration으로 푸는 HexIt임. 순차 의사결정 formulation은 신선하나 PPO류는 오히려 성능을 악화시켰고 메시 생성 한정임</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2611.10840'>Simple Test-Time Refinement for Plot-to-Code Generation via Visual-Code Diagnostics</a></td><td>46</td><td>2</td><td>Multimodal</td><td>plot-to-code에서 시각 렌더 결과로 오류를 진단하는 discriminator로 test-time refinement를 수행, 진단 후 수정 구조는 failure diagnosis와 닮음</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2611.12017'>Grasp-Taxonomy Conditioning as a Mode Switch for Dexterous Grasping of Climbing Holds</a></td><td>45</td><td>7</td><td>Manipulation</td><td>grasp taxonomy 조건을 mode switch로 쓴 클라이밍 홀드 grasp 모델임</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2611.11789'>HolidayFactory 1.0: Simulating, Generating, and Evaluating Industrial Robot Tasks</a></td><td>45</td><td>7</td><td>Manipulation</td><td>산업 로봇 반복 작업 시뮬레이션과 평가 benchmark임</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2611.10664'>Task-Critical Part Alignment Improves Imitation of Object Interactions</a></td><td>45</td><td>7</td><td>IL</td><td>DINOBot에 task-critical part 정렬을 더한 incremental 개선임</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2611.12383'>PCTac: Mechanochromic Photonic-Crystal Tactile Sensor for Dexterous Manipulation</a></td><td>45</td><td>6</td><td>Tactile</td><td>photonic crystal 기반 tactile 센서 하드웨어 연구임</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2611.12099'>SAM-VTP: Video Memory and Measured Geometry for Continuous Traversability Segmentation</a></td><td>45</td><td>6</td><td>Navigation</td><td>비디오 memory와 측정 기하를 이용한 traversability segmentation임</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2611.11996'>OASIS: Optimization-Aware Subgoal Inference with Safety Constraints for Autonomous Mobile Robot Navigation</a></td><td>45</td><td>6</td><td>Navigation</td><td>최적화 인지 subgoal 추론으로 안전 navigation을 다룸</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2611.11148'>MOSU2: Long-range Navigation System with Multi-modal Scene Understanding</a></td><td>45</td><td>6</td><td>Navigation</td><td>다중모달 장면 이해 기반 장거리 outdoor navigation 시스템임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2611.10938'>BRACE: Belief-guided Residual Adaptive Control for Safe Navigation under Unknown Disturbances</a></td><td>45</td><td>6</td><td>Navigation</td><td>belief 기반 residual 제어로 미지 외란 하 안전 navigation임</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2611.10137'>A Unified Inertial Encoder for Human and Humanoid Motion</a></td><td>45</td><td>6</td><td>Representation</td><td>인간과 humanoid 관성 데이터를 통합 encoder로 처리함</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2611.10454'>Decentralised Drone Swarm Formation under Silent Failures with ACO Pheromone Claims and PSO Tuning</a></td><td>45</td><td>6</td><td>Multi-robot</td><td>silent failure 하의 분산 드론 군집 대형을 ACO pheromone claim 증발로 고장 감지하고 PSO로 비행, 증명도 제시하나 CBBA 변형이 동등 이상이고 시뮬레이션만</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2611.12526'>Galilean Robots, Aristotelian Sensors: Joint Spatiotemporal Trajectory Estimation and Extrinsic Calibration</a></td><td>45</td><td>5</td><td>State Estimation</td><td>시공간 궤적 추정과 extrinsic 보정을 결합한 센서 캘리브레이션 연구임</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2611.11648'>PA-SaR: Perception-Aware Learning, Control, and Coordination for Multi-Robot Search and Rescue</a></td><td>45</td><td>5</td><td>Multi-Robot</td><td>multi-robot 수색 구조에서 인식 인지 학습과 제어를 결합함</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2611.11242'>DeepSoMo: Deformable Object Motion Estimation under Proprioceptive Partial Observability via Predictive Latent Dynamics</a></td><td>45</td><td>5</td><td>Soft Robotics</td><td>soft 로봇 변형체 운동 추정에 predictive latent dynamics를 씀</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2611.10682'>Burden, Bounty, or Bliss? Muscle-Aware Retargeting and Null-Space Exploration for Whole-Body Musculoskeletal Control</a></td><td>45</td><td>5</td><td>Control</td><td>근골격 전신 제어의 muscle 인지 retargeting 연구임</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2611.10435'>Multi-Objective Adaptation After Deployment: A Position on World Models for Remote Robot Teams</a></td><td>45</td><td>5</td><td>World Model</td><td>원격 로봇 팀 world model position paper로 실험 증거 약함</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2611.12149'>EgoLabel: Zero-Shot Egocentric Auto-Labeling with Cross-Modal Consistency</a></td><td>45</td><td>4</td><td>3D Vision</td><td>egocentric 영상 zero-shot auto-labeling, 인간 영상 데이터화에 유용</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2611.10013'>From Video to Digital Twin: An Exploratory Study of World Models and Gaussian Splatting on In-the-Wild Video</a></td><td>45</td><td>4</td><td>World Model</td><td>world model과 3DGS로 영상에서 digital twin 구성 탐색 연구</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2611.12875'>Click3R: Interactive Stereo 3D Reconstruction with Sparse Correspondence Clicks</a></td><td>45</td><td>3</td><td>3D Vision</td><td>클릭 기반 상호작용 보정이 있는 stereo 3D 재구성, 실용적이나 incremental</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2611.11998'>Reward-Estimated Hypergradient for Bilevel Reinforcement Learning with Black-Box Follower</a></td><td>45</td><td>3</td><td>RL</td><td>follower 보상을 inverse RL로 복원해 bilevel RL hypergradient를 추정하며 shaping 편향이 상쇄됨을 증명한 이론 중심 연구임</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2611.12120'>SCALE: Small-Model-First Concept Abstraction with LLM-Guided Experience Internalization</a></td><td>45</td><td>3</td><td>Embodied AI</td><td>작은 모델이 일상 예측을 맡고 오류 때 LLM이 counterfactual 예시로 개념을 제안해 내재화하는 SCALE, 기억 아카이빙 아이디어는 흥미로우나 실험이 소규모임</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2611.11929'>Can LLM Agents Organize Their Own Memory?</a></td><td>45</td><td>3</td><td>NLP</td><td>agent가 연결된 문서로 스스로 memory를 조직하고 원본 증거를 링크하는 SoMem, LoCoMo 등에서 2~3점 향상, robot memory와 개념적으로만 이어짐</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2611.10884'>Keeping LLM Agents on Procedure: Executable Finite-State Control for Long-Horizon Instruction Fidelity</a></td><td>45</td><td>3</td><td>NLP</td><td>agent의 장기 SOP 이탈을 context 밖 실행형 FSM으로 도구 호출, 전이, 턴 종료에서 강제, 200계정에서 정확 판정이 48에서 139로 오르는 long-horizon 신뢰성 사례임</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2611.11421'>GenRM-Flow: Generators are Process-aware Reward Models in Flow Matching</a></td><td>45</td><td>2</td><td>Video</td><td>생성기를 process-aware reward model로 활용, 영상 reward 새 관점</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2611.12815'>Inversion-Free High-Dimensional Counterfactual Inference</a></td><td>45</td><td>2</td><td>LG</td><td>inversion-free 고차원 counterfactual 추론, 인과 이론</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2611.11979'>FireGate: Bounding Behaviour Change Before Training in Continual RL Fine-Tuning</a></td><td>45</td><td>2</td><td>LG</td><td>LoRA 업데이트를 gate 뒤에 두어 continual RL fine-tuning의 행동 변화를 사전에 PAC로 제한하며 forgetting 방지 아이디어는 흥미로우나 LLM 대상임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2611.09897'>Process then Retrieve: Investigating the Origins of the Modality Gap in Vision-Language Models</a></td><td>45</td><td>2</td><td>Multimodal</td><td>VLM modality gap의 원인을 분석하는 흥미로운 이해 연구이나 로봇 연결 약함</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2611.12869'>Where Does Alignment Emerge and What Does It Mean? A Closer Look at the Platonic Representation Hypothesis</a></td><td>45</td><td>1</td><td>Representation</td><td>Platonic 표현 가설에서 정렬 발생 위치 분석</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2611.11937'>Attention Is Only as Good as Its Witnesses: When Higher-Order Layers Help, and When They Do Not</a></td><td>45</td><td>1</td><td>LG</td><td>attention의 깊이와 크기 법칙을 witness 합으로 설명하고 소형 layer로 CLRS-30에서 큰 모델에 맞서 이론과 실험을 함께 보이나 로봇과 거리 있음</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2611.10634'>Coverage-Verified Sparse Attention: Closed-Loop Quality Control for Long-Context LLM Decoding</a></td><td>45</td><td>1</td><td>NLP</td><td>sparse attention의 coverage를 검증 신호로 써서 부족한 head만 복구하는 CVSA임. 128K에서 6.21배 속도 향상이며 LLM 효율화 한정임</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2611.10338'>On the universal structure in deterministic generative diffusion</a></td><td>45</td><td>1</td><td>Generative</td><td>결정론적 diffusion 샘플링 궤적이 모달리티 불변의 보편 기하 구조를 가진다고 보임. 최적 선형 denoiser로 설명하나 초록 분량이 짧아 근거 확인이 어려움</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2611.10240'>PACE: Keeping the Right Tokens in the KV Cache Is Not Enough for Long-Horizon LLM Agents</a></td><td>45</td><td>1</td><td>NLP</td><td>long-horizon LLM agent의 KV cache 축출 문제를 다루나 로봇 연결 약함</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2611.12587'>AgentOPSD: Turn-Level Credit Assignment via Recursive Belief Revision</a></td><td>45</td><td>1</td><td>RL</td><td>turn 단위 credit assignment을 belief 개정으로 푸는 agent RL임</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2611.10141'>Retrofitting Unbounded Context onto Stock Language Models</a></td><td>45</td><td>1</td><td>NLP</td><td>RoPE 느린 plane의 주소 특성을 이용해 stock LM에 1M token 문맥을 붙이는 기법, needle 99% 이상이나 RULER는 모델별로 엇갈림</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2611.12675'>Interpretability Is Not Model-Specific</a></td><td>45</td><td>1</td><td>LG</td><td>unlabeled prompt로 fit한 residual stream 선형 map으로 refusal 방향 등 interpretability 도구를 110쌍 모델 간 전이, 이론 포함</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2611.11621'>ODSA: Orchestrated Discovery and Self-Aggregation</a></td><td>45</td><td>1</td><td>NLP</td><td>orchestrator LLM이 discovery, 비교, 수락 검증을 행동으로 골라 test-time scaling을 배분하는 ODSA, HLE에서 4.7~18.0점 향상하나 텍스트 추론 한정</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2611.11319'>Verify Before You Fetch: Reliable KV Cache Compression for LLM Inference</a></td><td>45</td><td>1</td><td>LG</td><td>PoissonComp와 KVFetch로 attention 근사 오차 (epsilon, delta) 보장을 주며 CPU 전송을 최소화하는 KV cache 압축, efficient inference 기여이나 로봇과 무관함</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2611.11379'>Self-Supervised Collapse Prevention with Score-Based Entropy Maximization</a></td><td>44</td><td>2</td><td>LG</td><td>latent score 모델로 marginal entropy를 키워 SSL collapse를 막는 EBReg, ViT-L 75.57% linear probe와 score 기반 test-time 보정까지 제시</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2611.10439'>Who Remembers What? Multi-Granularity Memory Extraction for Multi-User, Multi-Agent Interaction</a></td><td>44</td><td>2</td><td>NLP</td><td>다중 사용자와 agent 간 교훈 공유 범위를 정하는 memory 시스템 MixUA, 프라이버시 유출 0.02% 이하이나 LLM agent 한정</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2611.11220'>EbbFlow: PINN-Inspired Progressive Curriculum for MeanFlow Training</a></td><td>44</td><td>1</td><td>Generative</td><td>MeanFlow의 diagonal/interior 감독을 점진적으로 스케줄하는 EbbFlow, ImageNet FID 44.82에서 39.65로 개선, one-step 생성 유용하나 DiT-B 단일 seed</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2611.10751'>Constrained Look-ahead Guidance for Interference-Aware Flow Editing</a></td><td>44</td><td>1</td><td>CV</td><td>flow 기반 이미지 편집에서 one-step look-ahead로 편집과 fidelity 목적의 gradient 간섭을 줄임. 생성 편집 개선이며 로봇 연관 낮음</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2611.10305'>Plug-and-Play Verifier for Decoupling Process Reward in Stabilizing Long-Horizon Agentic Reasoning</a></td><td>44</td><td>1</td><td>NLP</td><td>중간 추론 산출물을 domain verifier로 평가해 process reward로 쓰는 plug-and-play verifier임. HotpotQA에서 60.18% 대 57.73%로 소폭 개선하는 agentic reasoning임</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2611.10397'>Regularization Amplifies Subliminal Learning</a></td><td>44</td><td>0</td><td>NLP</td><td>regularization(LoRA 등)이 subliminal learning을 오히려 증폭시킴을 보임. 반직관적 발견이나 LLM 안전성 분석임</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2611.10175'>ASCENT: Scale-Complementary External State for Frozen Long-Context Language Models</a></td><td>43</td><td>2</td><td>NLP</td><td>고정된 LM에 외부 state를 붙이고 reader 규모와 함께 이득이 커진다는 scale complementarity를 인과적으로 검증, memory 관점은 흥미로움</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2611.10778'>Passivity-Guaranteed Variable Impedance and Compliance Control via Online Parameter Optimization</a></td><td>42</td><td>6</td><td>Control</td><td>passivity 보장 variable impedance 제어로 제어 계열임</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2611.12654'>Correctness Boundaries of Typed Plans for Natural-Language Robot Fleet Control</a></td><td>42</td><td>5</td><td>Embodied AI</td><td>자연어 로봇 fleet 제어 plan 검증의 정확성 경계 분석임</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2611.11718'>Accelerated Reinforcement Learning for Soft Robotics: Hours Instead of Years</a></td><td>42</td><td>5</td><td>RL</td><td>soft robot RL 가속으로 응용 특화 개선임</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2611.11489'>Beyond Memory Limits: A Hierarchical Spatio-Temporal Map Representation for Large-Scale 3D Autonomous Exploration</a></td><td>42</td><td>5</td><td>Mapping</td><td>UAV 대규모 탐사용 계층 시공간 map 표현임</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2611.11296'>Single-Radar Bilateral 3D Near-Field Imaging for Mobile Robots</a></td><td>42</td><td>5</td><td>Perception</td><td>단일 radar 양방향 3D 근거리 영상화 센서 연구임</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2611.09932'>Preference-Augmented Distributional Reinforcement Learning for Risk-Sensitive Navigation</a></td><td>42</td><td>5</td><td>RL</td><td>선호 증강 distributional RL로 위험 민감 navigation을 다룸</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2611.11334'>MoT3DVG: A Benchmark for Outdoor 3D Visual Grounding with Motion-Aware Descriptions and Temporal Cues</a></td><td>42</td><td>4</td><td>3D Vision</td><td>야외 동적 3D visual grounding benchmark</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2611.11087'>SoftPAT3D: Physics-Augmented Text-to-3D Scene Generation with Deformables</a></td><td>42</td><td>4</td><td>3D Vision</td><td>변형체 포함 physics-augmented 장면 생성, 시뮬레이션 자산 생성</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2611.10821'>AmodalBox: Automated 3D Bounding Box Annotation under Partial Visibility</a></td><td>42</td><td>4</td><td>3D Vision</td><td>부분 가림 3D box 자동 주석, 인지 데이터 구축</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2611.10199'>RigidGS: Geometry-Aware Object Decoupling for Rigid-Body Interaction in 3D Gaussian Splatting</a></td><td>42</td><td>4</td><td>3D Vision</td><td>강체 상호작용용 3DGS 객체 분리, 시뮬레이션 연결</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2611.11936'>Constrained Variational Policy Optimization for Hybrid Action Spaces</a></td><td>42</td><td>4</td><td>RL</td><td>이산 mode와 연속 제어가 섞인 hybrid action constrained RL에서 CVPO를 확장한 이론 중심 방법이며 시뮬레이션만 평가함</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2611.12624'>Towards Reconstructing and Recognizing Objects behind Fragmented Occlusion using Video</a></td><td>42</td><td>3</td><td>3D Vision</td><td>조각난 가림 뒤 물체 복원, active perception과 약하게 연결</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2611.11770'>Towards Rotation-Only Imaging Geometry: Multi-View Pose Estimation</a></td><td>42</td><td>3</td><td>3D Vision</td><td>SfM에서 다중 뷰 rotation 추정 통합, 기하학적 기여</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2611.11738'>Dense Flow from Adaptive Correspondence</a></td><td>42</td><td>3</td><td>CV</td><td>optical flow 적응 correspondence, 성능 개선 위주</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2611.11140'>SurgWorld: Learning Surgical Representations Beyond Observation via Latent Prediction</a></td><td>42</td><td>3</td><td>Video</td><td>수술 표현을 latent 예측으로 학습, 부분 관측 world model 성격</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2611.10652'>SHIN: Scalable Hierarchy for INcremental 3D Gaussian Splatting</a></td><td>42</td><td>3</td><td>3D Vision</td><td>incremental 3DGS 계층 구조, 예산별 배포</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2611.10347'>PoseBench: Probing Pose Awareness in Visual Foundation Models</a></td><td>42</td><td>3</td><td>Representation</td><td>visual foundation model pose awareness probing</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2611.11609'>Building heterogeneous multistep workflows in automated microscopy: reward design and knowledge transfer for autonomous structure property discovery</a></td><td>42</td><td>3</td><td>RL</td><td>자동 현미경에서 측정 행동 선택과 재보정 시점을 보상 설계로 학습하는 budget 제약 워크플로, active acquisition 관점은 있으나 도메인이 현미경임</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2611.10748'>REINS: A Self-Evolving Agent Harness for Real-Time Trajectory Planning</a></td><td>42</td><td>3</td><td>Agent</td><td>LLM agent harness가 궤적 planning에 자기진화하는 시스템임</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2611.10264'>Look Only Where You Plan for Real-Time End-to-End Urban Driving</a></td><td>42</td><td>3</td><td>Autonomous Driving</td><td>필요 영역만 BEV를 구성해 driving planner를 가볍게 함</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2611.12716'>Spaghetti Splatting: Differentiating Curvilinear Dirac Masses via Convolution</a></td><td>42</td><td>2</td><td>3D Vision</td><td>곡선형 primitive의 미분 가능 렌더링 아이디어, 로봇 연결 약함</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2611.12242'>Controlling Temporal Pseudo-Label Marginals for Stable Online Test-Time Adaptation</a></td><td>42</td><td>2</td><td>CV</td><td>pseudo-label 클래스 분포를 Sinkhorn으로 시간 창에서 균형 잡는 plug-in으로 CTTA 안정화에 쓰이나 분류 중심임</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2611.11145'>DISCOVER: Online Variance-Guided Data Discovery for Budgeted Multimodal GRPO</a></td><td>42</td><td>2</td><td>Multimodal</td><td>VLM GRPO에서 reward 분산 기반으로 annotation할 프롬프트를 고르는 데이터 효율화임. 수학 추론 한정이라 robotics 연결 약함</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2611.12068'>MIRIX-2.0: Multi-Agent Memory System</a></td><td>42</td><td>2</td><td>NLP</td><td>LLM agent multi-agent memory 시스템으로 robot memory와 약하게 닿음</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2611.10683'>TransMem: Transition-Aware Retrieval for Evolving Personal Memory</a></td><td>42</td><td>2</td><td>NLP</td><td>선호 변화를 transition record로 저장해 검색하는 개인 memory TransMem, memory 구조 아이디어는 있으나 대화 도메인</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2611.11840'>Correct Answers from Insufficient Histories: A Controlled Study of Agent Memory Evaluation</a></td><td>42</td><td>2</td><td>NLP</td><td>두 합법 history가 같은 visible context를 주는 경우로 증거 불충분을 인증해 agent memory 평가 오류를 진단, 평가 프로토콜 기여이며 기억 방법은 아님</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2611.11684'>Self-Indexing Latent Memories for Access-Aware Continual Instruction Tuning of LLMs</a></td><td>42</td><td>2</td><td>LG</td><td>task별 latent memory가 자체 routing key가 되는 replay-free continual instruction tuning TILA-CT, forgetting 1.38점이며 continual learning 관점에서 참고 가능함</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2611.11560'>LiveAsset: Learning Intent Assets from Corrective Interactions for Agent Runtime Control</a></td><td>42</td><td>2</td><td>NLP</td><td>사용자 교정 대화에서 intent asset을 학습해 runtime 검증에 쓰는 LiveAsset, language feedback 학습과 닮았으나 웹 agent 벤치마크 한정</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2611.10477'>PatternBloom: Empowering Agentic RAG with Externalized RL-Distilled Graph Patterns</a></td><td>42</td><td>2</td><td>NLP</td><td>RL 학습 agentic RAG에서 고보상 trajectory를 Graph Pattern Memory로 증류해 재사용, 절차 지식 외부화 아이디어는 흥미로우나 QA 중심</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2611.10448'>ESTRA: Enabling Extreme Attention Sparsity for Training-Free Video Diffusion Acceleration</a></td><td>42</td><td>1</td><td>Video</td><td>영상 DiT attention sparsity 가속, efficient inference</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2611.11504'>Data-informed Adaptation of Foundation Models for Causal Effect Estimation</a></td><td>42</td><td>1</td><td>LG</td><td>variogram을 counterfactual-free router로 쓰는 MoE 인과 효과 추정기, causal 주제이나 표 형식 인과추론이라 로봇과 거리 있음</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2611.11371'>D3Tree: Learning to Prune Block-Diffusion Draft Trees for Efficient Verification</a></td><td>42</td><td>1</td><td>LG</td><td>block-diffusion draft tree의 노드를 학습된 head로 pruning해 speculative decoding 가속, VLM 서빙 효율이나 로봇과 간접적</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2611.11260'>Primitives and Paths: Predicting What Post-Training Can Do from What the Base Model Already Has</a></td><td>42</td><td>1</td><td>NLP</td><td>RL이 새 능력을 가르치는지를 effective support와 primitive coverage 2축으로 구분, composition 관점은 흥미하나 소형 합성 과제</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2611.11001'>Elastic Representations via Hyperbolic Geometry</a></td><td>42</td><td>1</td><td>LG</td><td>hyperbolic 공간 adaptor로 임베딩 차원 압축·확장을 재학습 없이 지원하는 HERL임. MRL 계열 개선 수준이고 로봇 연관 낮음</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2611.10705'>AbductionBench: Benchmarking Abductive Reasoning in Large Language Models</a></td><td>42</td><td>1</td><td>NLP</td><td>abductive reasoning을 생성·판별·가설 수정·증거 탐색으로 분류해 27개 데이터셋으로 LLM을 평가함. interactive 정보 수집 분석은 흥미로우나 벤치마크 성격임</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2611.10514'>FADE: Fractional Anomalous Dynamics Extrapolation for Training-Free Diffusion Transformers Acceleration</a></td><td>42</td><td>1</td><td>Generative</td><td>DiT feature 궤적을 anomalous diffusion으로 모델링해 Mittag-Leffler 연산자로 caching 예측하는 FADE임. 학습 없는 가속이나 생성 효율 개선 범주임</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2611.10560'>Large Language Models without QK-Normalization</a></td><td>42</td><td>1</td><td>LG</td><td>QK-Norm 대신 magnitude를 위상으로 인코딩하는 QK-MAP, 190M-7B에서 loss 개선하나 아키텍처 미세 변경 수준</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2611.11995'>Infrathon: Benchmarking Language Agents for Real-World, Long-Horizon AI Infra Optimization</a></td><td>42</td><td>1</td><td>NLP</td><td>24시간 장기 AI infra 최적화 agent 벤치마크 Infrathon, 평가 horizon에 따라 순위가 바뀐다는 관찰은 있으나 로봇 무관함</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2611.12062'>Translating KV Caches Between Hybrid-Attention Language Models: MLA Latents, Linear-Attention States and Sparse-Attention Indexers</a></td><td>42</td><td>0</td><td>NLP</td><td>MLA latent와 선형 attention 상태 등 hybrid 모델 간 KV cache를 변환해 re-read 없이 이어 가는 효율 연구로 로봇 무관</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2611.11892'>When Answer Decodability Is Not a Decision: Separating Final-Answer and Imminent-Emission Signals in Chain-of-Thought</a></td><td>42</td><td>0</td><td>NLP</td><td>CoT hidden state에서 다음 언급 후보와 최종 답을 나눠 probing해 답 decodability가 결정의 증거가 아님을 보임</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2611.11005'>GradReason: LLMs as Meta-Learners that Replace Training Epochs with Training-Data-Free Weight Updates</a></td><td>42</td><td>0</td><td>LG</td><td>LLM이 weight/gradient 이력을 보고 일부 epoch를 virtual update로 대체해 데이터 epoch 32.8% 절감함. 신선하나 CIFAR 규모이고 지연이 절감 시간보다 큼</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2611.10996'>Toward a theory of Evaluability</a></td><td>42</td><td>0</td><td>LG</td><td>학습에 test가 섞였을 수 있는 black-box 모델의 evaluability를 sample complexity로 특성화함. 순수 이론임</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2611.10873'>BRAT: Bounded Residual-Aligned Training for Stable Multi-Pass LLM Post-Training</a></td><td>42</td><td>0</td><td>NLP</td><td>LLM RL post-training에서 rollout 다회 재사용 시 붕괴를 막는 bounded 가중 BRAT임. 정렬 분석은 흥미로우나 LLM 한정임</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2611.10237'>Implicit Bias in State Space Models and Linear Autoregressive Training</a></td><td>42</td><td>0</td><td>LG</td><td>SSM과 선형 autoregressive 학습의 implicit bias 이론 분석임</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2611.12464'>Phrase-Level Speculative Decoding on a Frozen Target</a></td><td>42</td><td>0</td><td>NLP</td><td>phrase 단위 speculative decoding으로 efficient inference 기여함</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2611.11901'>Adaptive Entropy-Sparing for Efficient Reasoning</a></td><td>42</td><td>0</td><td>NLP</td><td>entropy를 보존해 추론 길이를 줄이는 효율 방법임</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2611.11761'>BridgeKV: Large-Model Prefill and Small-Model Decoding for LLM Inference via KV Cache Translation</a></td><td>42</td><td>0</td><td>NLP</td><td>대형 모델 prefill과 소형 decoding을 KV cache 변환으로 잇는 inference 가속임</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2611.10263'>DAC-MACE: Context-Conditioned Expert Routing for Compact Scene Coordinate Regression in Camera Relocalization</a></td><td>40</td><td>5</td><td>3D Vision</td><td>scene coordinate regression 경량화, 로봇 relocalization</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2611.12378'>Safety-Constrained Intelligent Control of a 2-DOF Robotic Manipulator Using Control Barrier Functions</a></td><td>40</td><td>5</td><td>Control</td><td>CBF 기반 2-DOF 매니퓰레이터 안전 제어로 규모가 작음</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2611.10169'>Capturability-Aware Footstep Planning in Cluttered Environments: A Recursively Feasible Sequential MPC on Axis-Aligned Safe Corridors</a></td><td>40</td><td>5</td><td>Planning</td><td>humanoid footstep planning용 순차 MPC로 locomotion 계열임</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2611.12818'>Simulating Vein Compressibility for Ultrasound-Guided Femoral Access: Speed, Accuracy, and Phantom Validation</a></td><td>40</td><td>4</td><td>Manipulation</td><td>초음파 유도 접근용 정맥 압축 시뮬레이션과 phantom 검증임</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2611.10241'>OfficeTwin: Realizing 3D Reconstruction of Redundant Scenes through Partial Viewpoint Perception</a></td><td>40</td><td>4</td><td>3D Vision</td><td>부분 시점으로 중복 장면을 feed-forward 복원하는 응용임</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2611.11964'>3R-Adapter: Retrieval, Rewiring, and Refinement for Efficient Adaptation of 3D Reconstruction Model</a></td><td>40</td><td>3</td><td>3D Vision</td><td>feed-forward 3D 재구성 모델의 효율적 adaptation</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2611.11873'>Where Does Proposal Selection Fail? Diagnosing Frozen Vision-Language Queries over Detector Proposals</a></td><td>40</td><td>3</td><td>Multimodal</td><td>detector+VLM grounding 실패 지점 진단, 분석 위주</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2611.11697'>SurgTAP-3D: A Large-Scale Cross-Surgery Video Dataset with Contact-Aware 3D Motion Tracking</a></td><td>40</td><td>3</td><td>Video</td><td>수술 영상 3D motion tracking 데이터셋, 자율 수술과 연결</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2611.10506'>SRA: Spatial Reasoning Adapter via Evolving Social Interaction Graphs for Trajectory Prediction</a></td><td>40</td><td>3</td><td>Embodied AI</td><td>사회적 상호작용 그래프 기반 궤적 예측 adapter</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2611.10370'>ClearForm: Shared-Surface Gaussian Splatting for Transparent and Opaque Scenes</a></td><td>40</td><td>3</td><td>3D Vision</td><td>투명 표면 Gaussian splatting, 투명 물체 인지에 유용</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2611.11586'>FastGRT: Accelerating Training of 3D Gaussian Ray Tracing</a></td><td>40</td><td>2</td><td>3D Vision</td><td>Gaussian ray tracing 학습 가속, efficiency</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2611.10609'>Reason First, Retrieve What Matters: Hypothesis-Guided Keyframe Selection for Long Video Understanding</a></td><td>40</td><td>2</td><td>Video</td><td>가설 기반 keyframe 선택, long video 효율</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2611.10337'>TimeTraveler: Temporal Strategy Planning with Time Dictionary for Streaming Video Understanding</a></td><td>40</td><td>2</td><td>Video</td><td>streaming video 이해 시간 전략 planning</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2611.09951'>Video-DCI: How Far Are VLM Agents from Human Viewers in Direct Video Corpus Interaction?</a></td><td>40</td><td>2</td><td>Video</td><td>VLM agent의 영상 코퍼스 상호작용 평가, active 탐색 성격</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2611.12878'>Adaptive Quantization Preserves Fast Rates for TD Learning over Rate-Limited Channels</a></td><td>40</td><td>2</td><td>RL</td><td>통신 제약 TD learning 양자화 이론</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2611.12530'>K-prop: Deep Online Learning by Backpropagating Temporal Kernels</a></td><td>40</td><td>2</td><td>LG</td><td>leaky 네트워크용 online 학습 K-prop으로 RTRL 비용을 줄이나 로봇 적용은 RL 실험 일부뿐임</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2611.11365'>MG-Cache: Multi-Granularity Caching for Accelerating Diffusion Transformer Inference</a></td><td>40</td><td>2</td><td>Generative</td><td>DiT 추론을 timestep과 layer 단위로 캐싱하는 training-free MG-Cache, HunyuanVideo 4.18배 가속이나 incremental</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2611.11330'>When Credit Turns Against Tools: Transition-Aware Credit Assignment in Agentic Reinforcement Learning</a></td><td>40</td><td>2</td><td>RL</td><td>agentic RL에서 tool-call 토큰의 음의 credit을 Advantage Projection 등으로 교정하는 TACA, LLM 도구 사용에 한정</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2611.11009'>PIA: Agentic Physics-Informed Runtime Anomaly Detection</a></td><td>40</td><td>2</td><td>LG</td><td>LLM agent가 물리 residual로 구성된 이상 탐지기를 직접 작성해 BATADAL에서 F1 0.878을 얻음. 상수도 CPS 한정이며 로봇과는 간접적임</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2611.10469'>Hibana: Fast Agentic Inference on Unified-Memory Devices</a></td><td>40</td><td>2</td><td>LG</td><td>unified-memory 기기용 agent 추론 엔진 Hibana, 상태 보존과 speculation으로 처리량 3.9배, 엣지 로봇 추론에 참고 가능</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2611.10404'>Coding or Cheating? An Investigation of Frontier Coding LLMs</a></td><td>40</td><td>2</td><td>RL</td><td>frontier coding LLM이 정답 유출이 막힌 환경에서도 git 기록 등을 뒤져 reward hacking을 시도함을 보인 분석, RL reward 설계 교훈</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2611.09942'>MedToolFault and MedGuard: evaluating and improving clinical agent reliability</a></td><td>40</td><td>2</td><td>NLP</td><td>임상 agent에 tool 실패 6종을 주입하는 MedToolFault와 evidence 검증 MedGuard, fault recovery 구조는 failure recovery와 닮음</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2611.10737'>The Lagrangian Brain: A Constraint Mechanics of Mind and Machine</a></td><td>40</td><td>2</td><td>Theory</td><td>Lagrange 제약 역학으로 뇌를 설명하고 gradient 없이 Sudoku·미로 planning을 푼다는 야심찬 가설이나 검증 범위가 퍼즐에 국한됨</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2611.12069'>MPEG-Diffusion: Mixed-Resolution Video Generation</a></td><td>40</td><td>1</td><td>Video</td><td>혼합 해상도 영상 diffusion 효율화, efficient inference</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2611.11058'>Differentiable Virtual-Slot Partitioning for Adaptive Tokenization in Vision Transformers</a></td><td>40</td><td>1</td><td>Efficiency</td><td>ViT adaptive tokenization 미분 가능 분할, efficiency</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2611.10734'>Tiny Evidence Region Localization with Selective Contrastive On-Policy Self-Distillation</a></td><td>40</td><td>1</td><td>Multimodal</td><td>MLLM 작은 증거 영역 localization, on-policy self-distillation</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2611.11752'>Spectral Rank and Step-Direction Dynamics in Language-Model Post-Training</a></td><td>40</td><td>1</td><td>NLP</td><td>LM post-training 업데이트의 stable rank와 checkpoint 변위 cosine을 분석한 실증 연구, RL 동역학 이해에는 도움이나 로봇과 거리 있음</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2611.11165'>The Race Is Decided Early! A Kernel Law Predicts Lock-In in Majority-Vote Test-Time RL</a></td><td>40</td><td>1</td><td>RL</td><td>majority-vote test-time RL에서 어떤 답으로 lock-in될지를 kernel 법칙으로 초기에 예측, test-time RL 동역학 분석이나 LLM 한정</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2611.11068'>Discrete Diffusion Playground: A 2D Benchmark for Discrete Generative Models</a></td><td>40</td><td>1</td><td>LG</td><td>2D 분포를 이진 토큰으로 바꿔 discrete diffusion의 실패를 진단하는 벤치마크임. masked diffusion이 checkerboard에서 실패함을 보인 점은 유용하나 진단용 장난감 설정임</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2611.11034'>Prune to Probe: Causal Decision-Stability Probes for Efficient Reasoning</a></td><td>40</td><td>1</td><td>NLP</td><td>답 이후 후속 생성을 억제하는 MLP 좌표를 pruning해 추론 종료 시점을 탐지함. 토큰 절감 2.6%로 효과 작고 AUROC 0.502라 정확성 신호로는 못 씀</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2611.10945'>CoupledFlow: One-Step Neural Operators for Coupled Multi-Physics PDEs</a></td><td>40</td><td>1</td><td>LG</td><td>multi-physics PDE를 one-step flow matching으로 푸는 CoupledFlow임. 과학 ML이며 로봇과 거리 멂</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2611.10881'>Robust and Efficient Continual Model Merging via Global Singular Subspace Separation and Restoration</a></td><td>40</td><td>1</td><td>LG</td><td>continual model merging에서 singular subspace를 분리·복원해 병합 열화를 줄이는 GS3R임. merging 개선 수준이라 incremental임</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2611.10649'>MACaQ: Fast, Model Agnostic Calibrated Quantization for Low-Precision Weights and Activations</a></td><td>40</td><td>1</td><td>LG</td><td>MXFP4 W4A4 post-training 양자화를 layer-local하게 하는 MACaQ임. 양자화 시간을 11배 줄였으나 엔지니어링 성격임</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2611.09934'>Causal Discovery Bench: Can LLMs Autonomously Conduct Effective Experiments?</a></td><td>40</td><td>1</td><td>NLP</td><td>LLM agent의 자율 실험 능력을 보는 인과 발견 benchmark임</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2611.10577'>Global Context Guidance for Diffusion Large Language Models</a></td><td>40</td><td>1</td><td>Generative</td><td>diffusion LLM이 global context를 덜 쓴다는 분석 후 feature-space guidance GCG로 추가 forward 없이 개선</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2611.11177'>When Are Nearby Experts Composable? Cross-Task Model Merging in Neural Thickets</a></td><td>40</td><td>1</td><td>LG</td><td>무작위 섭동으로 얻은 expert 쌍의 병합 가능성을 spectral selection으로 고르는 방법, 합성 후 성능 보존 조건을 분석하나 LLM 과제 한정</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2611.12066'>Weight-Space Programming for Medical Imaging: Do We Still Need Training Data?</a></td><td>40</td><td>0</td><td>Medical</td><td>LLM이 학습 데이터 없이 분류기 가중치 생성, 아이디어 흥미로우나 의료 특화</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2611.12799'>Agentic-OPD: Recovering Forgotten Agent Capabilities via On-Policy Distillation for Agentic Tasks</a></td><td>40</td><td>0</td><td>NLP</td><td>agent 능력 복원 on-policy distillation</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2611.12206'>A Geometric Invariant of Attention Predicts Head Specialization from Weights Alone</a></td><td>40</td><td>0</td><td>NLP</td><td>RoPE head의 기하 불변량 rho로 weight만으로 induction head를 예측하는 해석 연구이며 extended abstract 수준임</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2611.11024'>Phase-Conditioned Reward Shaping for Token-Efficient LLM Reasoning</a></td><td>40</td><td>0</td><td>NLP</td><td>추론 단계를 reasoning/execution/revision으로 분류해 길이 페널티를 차등 부여하는 PCRS임. 길이 3.13% 감소로 개선 폭 작음</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2611.10895'>Robust Satisficing Ensemble: Scalable Model Aggregation Under Distribution Shifts</a></td><td>40</td><td>0</td><td>LG</td><td>분포 이동에 강한 앙상블 가중을 robust satisficing으로 유도해 효율적으로 푸는 RSE임. NLP 분류 평가라 로봇과 무관함</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2611.12763'>PORT: Preference Optimization via Robust Token-Level Reweighting</a></td><td>40</td><td>0</td><td>NLP</td><td>token 단위 재가중 강건 preference 최적화로 incremental함</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2611.12127'>Lost in Rounding: bf16 Recurrent State Makes Hybrid Reasoning Models Think Longer</a></td><td>40</td><td>0</td><td>NLP</td><td>bf16 recurrent state가 추론 길이를 늘리는 현상 분석임</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2611.11740'>Creative Priming: Decoupling Process from Product to Escape the Creative Paradox</a></td><td>40</td><td>0</td><td>NLP</td><td>창의성을 결과물이 아닌 과정으로 모델링해 priming 모델이 primer를 만들고 GRPO로 학습하는 Creative Priming, 아이디어는 신선하나 평가 근거가 약함</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2611.10961'>Improving Analytic Constants via Interpretable AI-Guided Lean Proof Refinement</a></td><td>40</td><td>0</td><td>AI</td><td>Lean blueprint 의존 그래프를 유지하며 agent가 증명 slack을 줄여 Grothendieck 상수 상한을 개선, 수학 발견이라 로봇 무관함</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2611.10110'>Homeopathic Learning: Diluting poisoned fine-tuning data can strengthen its effect</a></td><td>40</td><td>0</td><td>AI Safety</td><td>단독으론 무해한 poison 데이터가 clean 데이터와 섞이면 backdoor를 만드는 homeopathic learning 현상을 회귀 모델로 설명, 데이터 감사 한계를 보임</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2611.11934'>Scale-Consistent Monocular Fisheye Visual Odometry via Spherical Bundle Adjustment-Guided Unsupervised Depth Learning</a></td><td>38</td><td>6</td><td>Navigation</td><td>fisheye monocular VO scale drift 보정, 로봇 위치추정에 쓰임</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2611.12129'>RAPA: Ray-Aware Physics Augmentation for Robust Camera-LiDAR Calibration</a></td><td>38</td><td>5</td><td>3D Vision</td><td>camera-LiDAR calibration 강건화, 로봇 인지 기반이나 incremental</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2611.11755'>Graph-Sparse Distributed Predictive Control for Multi-Robot Motion Planning vianEdge-Consensus ADMM</a></td><td>38</td><td>5</td><td>Planning</td><td>분산 MPC 다중 로봇 충돌 회피로 고전 제어 계열임</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2611.11646'>ColNav: Uncertainty-Aware Spacetime Collision Checking with Bounding Volume Hierarchies</a></td><td>38</td><td>5</td><td>Planning</td><td>BVH 기반 불확실성 인지 시공간 충돌 검사임</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2611.11090'>Large-Scale Hierarchical Decision-Making in Robot Control via ADMM</a></td><td>38</td><td>5</td><td>Control</td><td>ADMM 기반 대규모 계층 결정 최적화로 제어 계열임</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2611.12226'>A Game-Theoretic MPC Planner for Cooperative and Adversarial Drone Coordination</a></td><td>38</td><td>4</td><td>Planning</td><td>게임이론 MPC 드론 협력 및 추격 planner임</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2611.10483'>They Can See It but Not Say It: Iterative Self Knowledge Re-expression in Visual Reasoning Relative Pose Identification</a></td><td>38</td><td>3</td><td>Multimodal</td><td>상대 pose 판별 시각 추론 self re-expression</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2611.12575'>From Likelihood Convergence to Parameter Convergence in POMDPs</a></td><td>38</td><td>3</td><td>RL</td><td>POMDP 파라미터 복원 오차를 likelihood gap으로 묶는 이론이며 로봇 belief 모델과 먼 간접 연결뿐임</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2611.10819'>Selective Cooperative Perception via Blind Spot Reasoning and Agentic Dialogue with Vision-Language Models</a></td><td>38</td><td>3</td><td>Multimodal</td><td>VLM 대화로 협력 인식을 선택적으로 수행하는 교통 응용임</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2611.10501'>Sampling Is Not Curiosity: Why LLM Agents Should Investigate</a></td><td>38</td><td>3</td><td>Agent</td><td>LLM agent는 curiosity가 아니라 확률적 탐색을 한다는 position paper로 RL curiosity 기준을 정의했으나 실험 없음</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2611.11531'>Probing Transformer Representations Layer by Layer, Module by Module</a></td><td>38</td><td>2</td><td>LG</td><td>vision foundation model과 LLM의 layer x module 단위 linear probing 14만 회 평가, 표현 선택 지침은 되나 새 원리는 약함</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2611.11342'>Agent Self-Improvement with Frozen Weights: The Added Value and Limits of Failure Traces</a></td><td>38</td><td>2</td><td>NLP</td><td>frozen agent의 harness 노트가 실패 trace에서 얼마나 배우는지 측정, 이득이 4.0퍼센트포인트로 제한적임을 정직하게 보인 작은 평가</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2611.11279'>How Efficient Is Your Agent? Online Predictive Bounds under Budget Constraints</a></td><td>38</td><td>2</td><td>LG</td><td>agent의 time-to-success 상한을 예산 제약 하에서 online calibration하는 PROBE, 효율 평가 방법이나 소프트웨어 agent 대상</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2611.10393'>Finite Time Analysis of Risk-Sensitive RL via Noisy Power Iteration</a></td><td>38</td><td>2</td><td>RL</td><td>risk-sensitive average-cost RL을 noisy power iteration으로 보고 유한 시간 bound를 증명함. 이론 기여이나 실험과 로봇 연결 약함</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2611.12041'>SMO: Compiling Natural Language Skills into Graphs of Reusable State-Move-Outcome Bricks</a></td><td>38</td><td>2</td><td>NLP</td><td>자연어 skill을 재사용 graph로 컴파일함</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2611.12883'>Beyond Modality Preference: Controlling Multimodal Arbitration under Modality Conflict in MLLMs</a></td><td>38</td><td>1</td><td>Multimodal</td><td>modality 충돌 시 MLLM arbitration 제어, 분석 위주</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2611.11890'>Training Vision Transformers to Focus: Emergence of Spatial Attention Head Specialization</a></td><td>38</td><td>1</td><td>Representation</td><td>ViT에서 spatial attention head 특화 분석</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2611.11452'>Semantically Aligned KV Cache Compression for Efficient Agentic Autoregressive Video Generation</a></td><td>38</td><td>1</td><td>Video</td><td>agentic 영상 생성 KV cache 압축, efficiency</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2611.11209'>Viscot-steer: Disentangling and Transferring Visual Chain-of-Thought via Activation Steering</a></td><td>38</td><td>1</td><td>Multimodal</td><td>visual CoT를 activation steering으로 전이</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2611.12422'>Two-Phase Rapid Simulation-Based Inference with Differentiable Simulators</a></td><td>38</td><td>1</td><td>LG</td><td>Schrodinger bridge 기반 one-shot proposal로 simulation-based inference를 빠르게 하나 과학 추론 중심임</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2611.12137'>Good Views Are Not Enough: Global Counterexamples for Gaussian-Regularized JEPAs</a></td><td>38</td><td>1</td><td>LG</td><td>Gaussian 정규화 JEPA의 전역 최적해가 nuisance를 유지하는 반례를 보인 표현학습 이론이며 JEPA world model 이해에 간접 참고임</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2611.11910'>Late but Valuable: Why Deadlines Change the Measured Value of LLM Reasoning</a></td><td>38</td><td>1</td><td>NLP</td><td>deadline 아래에서 LLM thinking 답변의 가치를 도착 시간과 함께 재야 함을 보인 평가 연구로 자동화 실험실 맥락임</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2611.11862'>Are UFOs Real? Introducing Unified Factored Organizers</a></td><td>38</td><td>1</td><td>LG</td><td>다른 네트워크의 표현 규칙성을 모델링하는 UFO로 grokking을 10배 이상 단축, 아이디어는 흥미하나 장난감 과제 위주</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2611.11450'>How Much Training-Inference Mismatch Can On-Policy Distillation Tolerate?</a></td><td>38</td><td>1</td><td>NLP</td><td>on-policy distillation이 quantization, 비동기 rollout 불일치를 얼마나 견디는지 측정하고 FP8 recipe 제시, LLM 학습 효율 실증</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2611.10511'>CALFA-KV: Joint Calibration and Fisher-Guided Anchors for 1-Bit KV Cache Compression</a></td><td>38</td><td>1</td><td>NLP</td><td>1-bit KV cache 압축에 joint calibration과 Fisher 기반 anchor를 더한 CALFA-KV임. BF16 격차를 0.90-2.01점으로 줄인 압축 엔지니어링임</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2611.11299'>EASE-KV: Diagnosing the Gap Between Memory Availability and Effective Use</a></td><td>38</td><td>1</td><td>NLP</td><td>KV memory 가용성과 실제 활용 격차를 진단함</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2611.11035'>Room to Reconsider: Reply Length Decides Whether Pushback Makes Language Models Sycophantic or Self-Correcting</a></td><td>38</td><td>1</td><td>NLP</td><td>LLM에 반박 prompt를 줄 때 답변 길이에 따라 sycophancy와 self-correction이 갈린다는 분석 연구, 로봇과 거리 멂</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2611.10486'>Test-Time Scaling for Diffusion Language Models with Frequency-Aware Remasking</a></td><td>38</td><td>1</td><td>Generative</td><td>diffusion LM test-time scaling에서 예측이 자주 바뀐 token을 확정하는 frequency-aware remasking, 쉬운 문제는 빠른 sampler로 분기</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2611.10369'>FEROM: Frontier Endogenous Reveal-Order Marginal Policy Optimization for Masked Diffusion LMs</a></td><td>38</td><td>1</td><td>RL</td><td>masked diffusion LM에서 reveal order를 latent로 marginalize하는 Rao-Blackwell policy gradient FEROM, 수학적이나 LM 한정</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2611.12293'>Depth as a Candidate Source: Portfolio Allocation for Recurrent Test-Time Scaling in Large Language Models</a></td><td>38</td><td>1</td><td>NLP</td><td>recurrent LLM의 깊이별 후보 해집합이 비중첩임을 보이고 budget 배분(DPA)으로 test-time scaling을 재구성함, 수학 벤치 한정</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2611.11710'>CASCoDe: A Closed-Loop Agentic Framework for Analog Sizing and Layout Co-Design</a></td><td>38</td><td>1</td><td>AI</td><td>analog 회로 sizing과 layout을 계층적 이산 행동공간에서 tree search하는 CASCoDe, 면적 71% 감소하나 EDA 도메인임</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2611.10857'>Polynomial Denoisers on the Image Manifold: Volterra Networks for Self-Contained Pixel Diffusion</a></td><td>38</td><td>1</td><td>Generative</td><td>Volterra layer로 attention을 대체한 pixel-space diffusion 구조를 이론으로 도출했으나 ImageNet 경쟁력 수준이고 로봇 연관 약함</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2611.10165'>AutoEMatic: Runtime-Adaptive Mixed-Precision LLM Inference via Automatic Exponent-Mantissa Refinement</a></td><td>38</td><td>1</td><td>Efficient Inference</td><td>엔트로피와 hidden state 변화량으로 layer별 정밀도를 런타임에 바꾸는 AutoEMatic과 NVFP4 기반 AutoFP 포맷, 가속기까지 co-design하나 LLM 한정</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2611.12436'>Patching Up Circuit Learning via Parameter Sharing</a></td><td>38</td><td>0</td><td>LG</td><td>probabilistic circuit의 recursive parameter sharing RePA로 효율을 높이나 로봇과 거리가 있음</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2611.11902'>Spectral Unlearning: Transformer Structure-Preserving Updates for Language Models</a></td><td>38</td><td>0</td><td>NLP</td><td>transformer weight 행렬 구조를 쓰는 spectral update를 unlearning에 얹어 baseline을 앞서는 방법임</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2611.11079'>When Calibration Data Matter in Sub-4-Bit Language Model Quantization</a></td><td>38</td><td>0</td><td>NLP</td><td>2비트 양자화에서 task 문서로 calibration하면 정확도가 오르는 조건을 분석함. 이득이 1.83pt로 작고 task 포함 여부에 의존함</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2611.10792'>Zeroth-Order Riemannian Optimization on Fixed-Rank Manifolds for LLM Fine-Tuning</a></td><td>38</td><td>0</td><td>LG</td><td>고정 rank manifold 위의 zeroth-order Riemannian 최적화로 LLM fine-tuning 메모리를 줄임. 최적화 기법이며 로봇 무관함</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2611.10760'>ConwayNet: Interpretability, Activation Coherence, and Noise Resilience via a Game-of-Life-Inspired Lateral Inhibition in Artificial Neural Networks</a></td><td>38</td><td>0</td><td>CV</td><td>Game-of-Life 규칙을 lateral inhibition으로 넣어 잡음 내성과 해석성을 높이는 ConwayNet임. 아이디어 독특하나 작은 규모 검증임</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2611.10750'>AERO: Adaptive Ensemble-Disagreement Routing for Oracle Feedback in Sample-Efficient Online RLHF</a></td><td>38</td><td>0</td><td>NLP</td><td>ensemble 불일치로 oracle 선호 라벨 질의를 줄이는 online RLHF AERO임. 라벨 효율 개선이고 LLM 한정임</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2611.10620'>What Do Collusion Probes Read? Three Pitfalls in Evaluating Multi-Agent Collusion Monitors</a></td><td>38</td><td>0</td><td>NLP</td><td>collusion probe가 지시 여부를 읽을 뿐 결정을 못 읽는다는 평가 함정을 보임. LLM 에이전트 안전성이며 로봇 무관함</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2611.10251'>TORNADO: Adaptive Latent Stochastic Transport for Calibrated Probabilistic PDE Forecasting</a></td><td>38</td><td>0</td><td>LG</td><td>PDE 확률 예측의 보정 개선 연구로 방법은 탄탄하나 로봇과 무관함</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2611.10096'>Coordinated Mixed-Precision KV Cache Quantization for Efficient LLM-based Multi-agent Systems</a></td><td>38</td><td>0</td><td>NLP</td><td>multi-agent LLM용 KV cache 혼합 정밀도 양자화로 efficient inference 성격임</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2611.12634'>How Far Does Second-Order Linear Response Predict Quantization Mismatch? Pre-Registered Measurements on Five Language Models</a></td><td>38</td><td>0</td><td>LG</td><td>양자화 불일치 예측 2차 응답 측정임</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2611.12012'>Robust Domain-Mixture Scheduling for Multi-Teacher On-Policy Distillation</a></td><td>38</td><td>0</td><td>NLP</td><td>multi-teacher on-policy distillation의 도메인 혼합 스케줄링임</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2611.11551'>When Should Diffusion Language Models Reconsider Their Commitments?</a></td><td>38</td><td>0</td><td>NLP</td><td>diffusion LM의 재고 시점 분석임</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2611.11725'>The Value of Not Knowing: How Fresh Eyes through Naive LLMs Fuel Creativity</a></td><td>38</td><td>0</td><td>NLP</td><td>주제를 모르게 만든 naive LLM이 낸 씨앗 아이디어를 강한 mentor가 다듬는 구조, 1B와 7B에서만 확인된 창의성 주장임</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2611.11368'>BiVerify: Closing the Loop Between Backward and Forward Verification for Mathematical Self-Correction</a></td><td>38</td><td>0</td><td>NLP</td><td>역방향과 정방향 검증을 번갈아 스케줄링하는 BiVerify, 수학 벤치마크 평균 13.5퍼센트포인트 향상이나 수학 추론 한정</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2611.11717'>Autonomous Continual Learning and Knowledge Transfer via Cortex-Inspired Neural Assemblies</a></td><td>36</td><td>2</td><td>LG</td><td>sparse binary routing mask를 support sample로 계산하는 FTN으로 continual learning 수행, catastrophic forgetting 관점은 있으나 소규모 검증</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2611.11398'>Decomposing Earth Embeddings with Sparse Autoencoders</a></td><td>36</td><td>1</td><td>CV</td><td>Earth observation embedding을 sparse autoencoder로 분해하고 평가 프로토콜 제안, 해석성 연구이나 위성 도메인</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2611.11336'>Where Should a Gate Look? Input vs. State Gating in Diagonal State Space Models</a></td><td>36</td><td>1</td><td>LG</td><td>diagonal SSM에서 input gating과 state gating의 expressivity 분리를 증명, 시퀀스 모델 이론으로 로봇 연관 약함</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2611.11114'>Compositional Conformal Risk Control for Multi-Stage LLM Cascades</a></td><td>36</td><td>1</td><td>LG</td><td>LLM cascade에 단계별 conformal risk control 보장을 줌. 이론은 있으나 MMLU류 평가라 로봇 연관 낮음</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2611.10982'>Think or Remember: The Exchange Rate of Agentic Inference</a></td><td>36</td><td>1</td><td>LG</td><td>agent 추론에서 reasoning 재전송 비용을 thinking과 memory 영역으로 나눈 비용 모델 분석, 로봇 연결은 약함</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2611.10319'>Prove What You Can: Hybrid Neurosymbolic Reasoning for Logical Natural Language Inference</a></td><td>36</td><td>1</td><td>NLP</td><td>LLM이 proof tree를 제안하고 prover가 단계별 검증하는 hybrid 추론, FOLIO 5.3점 향상, symbolic 검증 구조는 TAMP와 유사</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2611.09939'>Rethinking Supervision Targets for Multimodal LLM Unlearning: Less Private Information, Reduced Distribution Shift</a></td><td>36</td><td>1</td><td>Multimodal</td><td>MLLM unlearning에서 FFN 활성을 교란한 self-distillation 목표 FPD로 forgetting과 utility 균형, 로봇 무관</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2611.12552'>SciMARS: Multi-Agent Recursive Self-Improvement for Closed-Loop Scientific Discovery</a></td><td>36</td><td>1</td><td>NLP</td><td>shared evidence graph와 memory editor로 multi-agent harness를 재귀 개선하는 SciMARS, 과학 발견 도메인</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2611.12356'>DForkTree: Accelerating Speculative Decoding with Fork-Aware Block Diffusion Draft Trees</a></td><td>36</td><td>1</td><td>LG</td><td>block diffusion drafter의 분기 이후 오류를 n-gram PMI로 재앵커하는 DForkTree, 최대 4.75배 가속의 efficient inference</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2611.10658'>The Delta Gap: Cellular World Models for Perturbation Response Prediction Are Far Harder Than Global Correlation Implies</a></td><td>36</td><td>1</td><td>LG</td><td>세포 교란 반응 예측 모델이 global Pearson에 속아 delta Pearson은 낮음을 보이고 delta 정렬 학습을 제안, world model 명칭만 차용</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2611.11223'>SGA-Sparse: Training Native SwiGLU Gates for Activation-Sparse and Low-Bit LLMs</a></td><td>36</td><td>0</td><td>NLP</td><td>SwiGLU gate를 top-k router로 직접 학습해 75-85% FFN sparsity를 얻는 SGA-Sparse, LLM 효율 추론이나 로봇과 간접적</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2611.10860'>Structurally Separated DAG Learning with Multi-Scale Normalized Closure</a></td><td>36</td><td>0</td><td>LG</td><td>DAG 학습에 multi-scale closure logit을 더해 DAGMA를 개선함. 합성 벤치마크 한정이고 개선 폭이 제한적임</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2611.10627'>CONSTRAINER: Promptable Graph-Structured Optimization via Constraint Conditioning</a></td><td>36</td><td>0</td><td>LG</td><td>제약 조건을 operator graph로 파싱해 GNN으로 임베딩하는 CONSTRAINER임. 전력망·MILP 응용임</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2611.10389'>From Task Affinities to Optimal Allocations: Probabilistic Graphical Modelling for Supervised Finetuning</a></td><td>36</td><td>0</td><td>NLP</td><td>SFT task 혼합 비율을 Markov random field로 학습하는 TaskMixPGM임. 데이터 혼합 휴리스틱 개선임</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2611.10335'>Two-Sided Conformal Evidence Sets for Retrieval-Augmented Generation</a></td><td>36</td><td>0</td><td>NLP</td><td>RAG에서 근거와 반박 증거 집합을 conformal로 각각 보장하는 CES임. 커버리지 보장은 있으나 분포 이동에서 12.7pt 미달함</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2611.10223'>Lower-Level Agnostic Bilevel Optimization</a></td><td>36</td><td>0</td><td>LG</td><td>lower-level agnostic bilevel 최적화 이론 기여이나 로봇과 거리 있음</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2611.11965'>ChainCheck: Near-Perfect Evidence-Sufficiency Scores Can Conceal Sensitivity to Construction Artifacts -- Paired Conditional Contrasts that Expose an Evaluation Confound</a></td><td>36</td><td>0</td><td>NLP</td><td>HotpotQA 증거 충분성 점수가 편집 artifact에 민감함을 paired contrast로 폭로하는 평가 타당성 감사, 로봇 무관함</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2611.10045'>Don&#x27;t Blame The Preferences: Examining The Emergence of Sycophancy in LLM Training</a></td><td>36</td><td>0</td><td>NLP</td><td>sycophancy가 preference alignment가 아니라 SFT 단계에서 대부분 형성됨을 3개 모델군에서 보인 분석</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2611.11885'>Design of a hybrid tendon-linkage finger with coupled and adaptive motion</a></td><td>35</td><td>6</td><td>Hardware</td><td>건-링키지 하이브리드 손가락 설계로 하드웨어 연구임</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2611.12130'>Compact and Wide-Force-Range Magnetorheological Hand Exoskeleton for Kinesthetic Feedback in Teleoperation</a></td><td>35</td><td>5</td><td>Teleoperation</td><td>MR 유체 hand exoskeleton 촉각 피드백 하드웨어임</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2611.10498'>EmbodiedIntentBench: Benchmarking Intent-Driven Runtime Adaptation for Mobile Robotic Missions</a></td><td>35</td><td>5</td><td>Embodied AI</td><td>모바일 로봇 의도 기반 런타임 적응 benchmark임</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2611.12754'>Sliding into Balance: Benefits of a Sliding Payload for Load Distribution and Disturbance Rejection in Dual-UAV Transportation</a></td><td>35</td><td>4</td><td>Control</td><td>이중 UAV 슬라이딩 payload 운송 분석으로 제어 중심 연구임</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2611.12139'>BioMARS 2.0: a robotic biologist for formulating and adapting biological experiments</a></td><td>35</td><td>4</td><td>Robotic Lab</td><td>생물 실험 로봇 시스템으로 응용 중심임</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2611.11940'>Reliability-Adaptive Multimodal Relative Pose Tracking for Underwater Leader-Follower Robots</a></td><td>35</td><td>4</td><td>Marine Robotics</td><td>수중 leader-follower 상대 자세 추적으로 응용 특화임</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2611.11709'>Data-Driven Precision Control of Soft Helicoid Robots</a></td><td>35</td><td>4</td><td>Control</td><td>soft helicoid 로봇의 데이터 기반 정밀 제어임</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2611.11601'>Kinora: A Versioned Workflow for Text-to-Motion Generation, Robot Retargeting, and Interactive Validation</a></td><td>35</td><td>4</td><td>Motion</td><td>text-to-motion과 retargeting 버전 관리 워크플로 도구임</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2611.10566'>Online Geometric Consistency Assessment of LiDAR Measurements via Recursive Bayesian Comparison</a></td><td>35</td><td>4</td><td>Perception</td><td>LiDAR 측정 기하 일관성 온라인 평가임</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2611.11763'>LangDepth: Vision-Language Scene Priors for Semantic Binning and Cross-Domain Monocular Depth Estimation</a></td><td>35</td><td>3</td><td>3D Vision</td><td>언어 prior로 metric depth 일반화, 모듈 추가 수준</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2611.10729'>LIFT: Local Metric Alignment and Foundation-guided Propagation for Few-shot Depth Completion</a></td><td>35</td><td>3</td><td>3D Vision</td><td>few-shot depth completion, 로봇 깊이 센서와 연결 약함</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2611.12695'>TACTUS: A Robotic Palpation System for Spatially Heterogeneous Hardness Mapping of Woody Breast Myopathy</a></td><td>35</td><td>3</td><td>Tactile</td><td>닭가슴살 경도를 20개 tactuator 촉각 어레이로 지도화하는 시스템이나 식품 검사용이고 학습 기여가 약함</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2611.12205'>Graph-Based RL for Sequential Rendezvous Planning with Multiple Patrolling USVs</a></td><td>35</td><td>3</td><td>RL</td><td>다수 USV 순찰 rendezvous를 graph RL로 푸는 응용임</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2611.11690'>A Physical Testbed for Self-Driving Laboratories: Comparing Bayesian and Agentic Optimization in a Minimal Closed-Loop Color Formulation Task</a></td><td>35</td><td>3</td><td>Robotic Lab</td><td>자율 실험실 BO 대 agentic 최적화 testbed 비교임</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2611.10363'>LSRP*: Scalable and Anytime Planning for Multi-Agent Path Finding with Asynchronous Actions</a></td><td>35</td><td>3</td><td>Planning</td><td>비동기 action MAPF anytime 알고리즘으로 고전 planning임</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2611.11696'>Direct GPU Energy Measurements of Batch-Level Sharing in Mixture-of-Experts and Recurrent Models</a></td><td>35</td><td>2</td><td>LG</td><td>MARL 순환 policy와 MoE LLM에서 batch 공유 연산의 GPU 에너지를 직접 측정, 효율 측정이나 pilot 수준임</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2611.11064'>GARP: Real-Time Generative Agents on Local Hardware in a Game Engine</a></td><td>35</td><td>2</td><td>AI</td><td>Godot 게임 엔진에서 3B 로컬 모델로 감정, 기억, 관계를 갖는 generative agent를 실시간 구동하는 GARP, 시스템 시연 성격임</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2611.10768'>BlenderFORGE: Framework for Optimizing Reactive 3D-Graphics Editing Ability of MLLMs</a></td><td>35</td><td>2</td><td>Multimodal</td><td>Blender bpy 코드 생성으로 3D 편집하는 MLLM agent를 SFT+멀티턴 RL로 학습한 환경 프레임워크로 로봇 연결은 약함</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2611.11926'>Text Alone Predicts Which Classes a Segmentation Readout Keeps</a></td><td>35</td><td>1</td><td>CV</td><td>open-vocab segmentation에서 누락 class를 텍스트로 예측, 분석적</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2611.11062'>What Does Multiple Choice Actually Measure? Disentangling Video Understanding from Option Exploitation</a></td><td>35</td><td>1</td><td>Video</td><td>video MCQ가 무엇을 재는지 분석, benchmark 비평</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2611.10382'>From Reflection to Co-Evolution: Self-Evolving Agents with Locally Verified Memory</a></td><td>35</td><td>1</td><td>NLP</td><td>self-evolving agent 검증된 memory, LLM agent</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2611.10160'>Improving the Diffusability of Motion Tokenizer</a></td><td>35</td><td>1</td><td>Generative</td><td>motion tokenizer diffusability 개선</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2611.09949'>Counting Events, Not Seeing Them: Diagnosing and Repairing the Readout Failure in Video LLMs</a></td><td>35</td><td>1</td><td>Video</td><td>video LLM 카운팅 readout 실패 진단</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2611.12777'>Anchor Behavior, Not Parameters: Rehearsal-Free Continual Learning with a Single Shared Prompt</a></td><td>35</td><td>1</td><td>LG</td><td>rehearsal-free continual learning 행동 anchor</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2611.10999'>Differentiable Agent-Based Modeling for Multi-Echelon Supply Chains: Gradient-Based Optimization of Heterogeneous Policies at Scale</a></td><td>35</td><td>1</td><td>LG</td><td>미분 가능한 agent-based 시뮬레이션으로 공급망 정책 1만 개를 동시 최적화함. 도메인 응용이며 로봇과 무관함</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2611.12114'>OGDA: Ontology-Grounded Data Agents for Reliable Analysis over Heterogeneous Data Lakes</a></td><td>35</td><td>1</td><td>NLP</td><td>data lake를 ontology로 압축하고 task graph로 처리 행동을 제약하는 data agent, KramaBench에서 최대 10.82점 향상하나 로봇과 무관함</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2611.12048'>Evaluating AI Agents for Industrial-Level Chip Floorplanning: A Framework and Empirical Study</a></td><td>35</td><td>1</td><td>AI</td><td>산업용 chip floorplanning을 물리 측정으로 평가하는 agent 프레임워크, 단일 설계 사례 연구이고 공간 결정 평가라는 점만 약하게 연결됨</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2611.11907'>Layer Roles Matter: Mitigating Modality Imbalance in Multimodal Emotion Reasoning via Adaptive Layer Profiling</a></td><td>35</td><td>1</td><td>Multimodal</td><td>MLLM 층별 역할을 Modality Entropy와 Cross-modal Intensity로 프로파일링해 감정 추론의 modality 불균형을 줄이는 training-free 기법, 감정 도메인 한정</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2611.11470'>GOPR-CAD: Graph-of-Operations Progressive Reasoning for CAD Generation</a></td><td>35</td><td>1</td><td>CV</td><td>LLM이 CAD 연산 그래프를 점진 구성하고 컴파일러가 모델을 만드는 GOPR-CAD, MHCAD 300개에서 구조 수율 82.7%이며 CAD 도메인임</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2611.12880'>Kolmogorov-Chapman Maps: Trajectory-Free Learning for Simulating Molecular Dynamics</a></td><td>35</td><td>0</td><td>LG</td><td>분자동역학 궤적 없는 학습, 과학 응용</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2611.12310'>The Optimal Rate Constant of Heavy-Ball Momentum on Smooth Strongly Convex Functions</a></td><td>35</td><td>0</td><td>Optimization</td><td>heavy-ball의 최적 rate 상수가 8임을 증명한 최적화 이론으로 탄탄하나 로봇 무관</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2611.12248'>A method to automatically discover symbolic local learning rules</a></td><td>35</td><td>0</td><td>LG</td><td>local 손실의 단항식 사전을 회귀해 backprop 대체 규칙을 찾으나 작은 네트워크 실험에 그침</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2611.12024'>FocusBranch: Combinatorial Branch-and-Bound for $\ell_0$ Neural Network Robustness Verification</a></td><td>35</td><td>0</td><td>LG</td><td>l0 섭동 신경망 강건성 검증을 branch-and-bound로 가속한 FocusBranch로 검증 분야 한정임</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2611.10785'>Proximal Preference Optimization: A Unified Framework for Stable and Reward-Free Alignment</a></td><td>35</td><td>0</td><td>NLP</td><td>DPO에 clipped importance ratio를 넣어 데이터 재사용 안정성을 높이는 P2O/PKTO임. PPO와 DPO의 단순 결합이라 incremental임</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2611.10668'>Causal Heteroscedastic Structure Learning From Incomplete Temporal data</a></td><td>35</td><td>0</td><td>LG</td><td>결측·이분산 시계열의 인과 구조를 optimal transport로 학습하는 Cheesefill임. 시계열 인과 발견이며 로봇과 간접적임</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2611.10550'>Dual-Granularity Learning for Regression with Continuous Noisy Labels</a></td><td>35</td><td>0</td><td>LG</td><td>잡음 라벨 회귀에 residual 학습과 binning 대조 정규화를 결합한 GRAIN임. 일반 회귀 개선 수준임</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2611.10288'>A Clinical Evaluation of Conformal Prediction for Chest Radiograph Report Generation</a></td><td>35</td><td>0</td><td>Multimodal</td><td>흉부 X선 보고서 생성의 conformal prediction을 방사선사 주석으로 평가하고 자동 지표가 임상 오류를 놓침을 보임. 의료 평가이며 로봇 무관함</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2611.10267'>Match the Geometry Before the Surrogate: Extreme Low-Budget Optimization in High Dimensions</a></td><td>35</td><td>0</td><td>LG</td><td>분자 최적화용 저예산 고차원 BO 기하 정합 아이디어이나 로봇과 무관함</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2611.10051'>All roads lead to Markov kernel networks: A representation theorem for discretization-stable learning</a></td><td>35</td><td>0</td><td>LG</td><td>discretization 안정 학습의 Markov kernel 표현 정리 이론임</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2611.12864'>Is Persona Generalization Predictable?</a></td><td>35</td><td>0</td><td>NLP</td><td>persona generalization 예측 가능성 분석임</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2611.12538'>Language Defaults Before Content: A Causal Layer Map of Multilingual Generation</a></td><td>35</td><td>0</td><td>NLP</td><td>다국어 생성의 언어 선택 layer 인과 지도임</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2611.12240'>Prune, Don&#x27;t Merge: Expert Compression of Mixture-of-Experts LLMs on Multilingual Production Tasks</a></td><td>35</td><td>0</td><td>NLP</td><td>MoE 전문가 pruning이 merge보다 낫다는 압축 실험임</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2611.11695'>Language model capabilities fail in a shared, predictable order under compression and perturbation</a></td><td>35</td><td>0</td><td>NLP</td><td>압축 하 LM 능력 저하의 공통 순서 분석임</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2611.11598'>Perturbing Inputs Improves Pretraining Distillation</a></td><td>35</td><td>0</td><td>NLP</td><td>입력 섭동으로 pretraining distillation을 개선함</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2611.09945'>A Model Organism for Studying Unverbalized Evaluation Awareness</a></td><td>35</td><td>0</td><td>NLP</td><td>평가 인식을 말하지 않는 Qwen3.5-27B model organism을 만들고 interpretability probe 4종이 못 잡음을 보임</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2611.11558'>InfraRSI: Harnessing Recursive Self-Improvement for Training Infrastructure</a></td><td>35</td><td>0</td><td>LG</td><td>LLM 분산 학습의 launch 설정과 커널을 agent가 최적화하는 InfraRSI, MFU 17.4%에서 30.0%로 오르나 인프라 엔지니어링임</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2611.11201'>When Self-Consistency Hurts: The Hidden Cost of Majority Voting in Small Language Models</a></td><td>35</td><td>0</td><td>NLP</td><td>1B 이하 소형 모델에서 self-consistency가 맞은 답을 틀리게 바꾼다는 점을 보이고 gate로 연산을 줄임, 범위가 N=5 수학으로 좁음</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2611.11010'>Lightfoot: Graph Retrieval-Augmented Generation with Exact, Model-Free Document Deletion</a></td><td>35</td><td>0</td><td>NLP</td><td>문서 삭제가 모델 호출 없이 가능한 결정론적 GraphRAG Lightfoot, 인덱스 비용은 낮추나 2Wiki에서는 HippoRAG 2보다 낮음</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2611.10432'>D-REAL: Acceptance-Length Optimization with Unbiased Gradients for Speculative Decoding</a></td><td>35</td><td>0</td><td>NLP</td><td>speculative decoding에서 acceptance length를 직접 최적화하는 불편 gradient 추정기, 처리량 최대 9.4% 향상 수준</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2611.10602'>Agentic discrete-event simulation for manufacturing system design: an open 3D simulator, a benchmark and an industrial case</a></td><td>34</td><td>2</td><td>Agent</td><td>Unity 기반 3D DES 시뮬레이터 SimuLean에서 LLM agent가 제조 모델을 86% 유효하게 만든다는 응용으로 생산 라인 설계 쪽이며 로봇 학습과는 거리 있음</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2611.11649'>A Trust Region Approach for Learning Schrödinger Bridges</a></td><td>34</td><td>1</td><td>Generative</td><td>unnormalized density만 있을 때 KL trust region으로 Schrodinger Bridge IPF를 안정화, 생성 모델 방법론이나 로봇 연관 낮음</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2611.11525'>Boundary Mass in Feature Space as a Label-Budget Diagnostic for Representations</a></td><td>34</td><td>1</td><td>LG</td><td>frozen 표현의 decision boundary 근방 질량으로 label budget을 진단하는 지표, 표현 평가 도구이나 분류 중심</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2611.10972'>JUBILEE: A Benchmark Environment for Off-Policy Evaluation in Debt Collections</a></td><td>34</td><td>1</td><td>RL</td><td>부채 추심 도메인 off-policy evaluation 벤치마크 JUBILEE임. hidden confounding 하의 OPE 실패 분석은 있으나 특수 도메인임</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2611.10170'>Where Did the Evidence Go? Diagnosing Proof-Set Loss in Long-Term Conversational Memory</a></td><td>34</td><td>1</td><td>NLP</td><td>장기 대화 memory에서 보완 증거 turn이 검색 단계에서 사라지는 위치를 진단하고 EviCover 제안, 개선폭은 작음</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2611.12393'>AutoBuddy: Evaluating Proactive, Always-On Agents on Task Discovery and Execution in a Simulated Workplace</a></td><td>34</td><td>1</td><td>NLP</td><td>사용자 workspace에서 할 일을 스스로 찾아 실행하는 proactive agent 시뮬레이터 AutoBuddy-Bench, 발견과 실행 실패 단계 분석</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2611.11238'>FRESCO: A Novel Consistency Control for Asynchronous Pipeline Parallel Training</a></td><td>34</td><td>0</td><td>LG</td><td>비동기 pipeline parallel 학습의 불일치를 activation subspace 제약으로 보정하는 FRESCO, 시스템 효율 연구</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2611.11074'>System Prompts Affect Response Bias More Than Discriminability in LLM Safety</a></td><td>34</td><td>0</td><td>NLP</td><td>system prompt가 LLM 안전성에서 변별력보다 refusal 기준을 이동시킴을 신호탐지이론으로 보임. 로봇과 무관함</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2611.10455'>Bayesian Low-Rank Posteriors for Scalable Membership Inference</a></td><td>34</td><td>0</td><td>Multimodal</td><td>LoRA subspace의 SWAG 사후에서 virtual reference model을 뽑아 VLM membership inference 비용을 줄임. 프라이버시 공격이며 로봇 무관함</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2611.10352'>TripletAD: Weakly Supervised Anomaly Detection in Embedding Space with Rare Anomalies and Scarce Labels</a></td><td>34</td><td>0</td><td>LG</td><td>embedding 공간에서 소수 라벨 이상 탐지를 triplet margin으로 수행하는 TripletAD임. ADBench 평가이고 incremental임</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2611.10217'>Rethinking How to Leverage Cheap Physics for Data-Efficient Neural Operators</a></td><td>34</td><td>0</td><td>LG</td><td>저가 physics를 활용한 neural operator 데이터 효율 개선임</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2611.10188'>BiMuon: A Geometry-Aware Stochastic Bilevel Optimization Approach</a></td><td>34</td><td>0</td><td>LG</td><td>geometry-aware bilevel 최적화 알고리즘으로 로봇과 무관함</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2611.10646'>On the Geometric Bottlenecks of Cross-Lingual Knowledge Editing</a></td><td>34</td><td>0</td><td>NLP</td><td>cross-lingual knowledge editing 전파 실패를 anisotropy 기하로 분해해 분석, 이론적이나 로봇 무관</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2611.10463'>LongCapHarness: Capability-Guided Auto-Harnessing for Long-Context Reasoning</a></td><td>34</td><td>0</td><td>NLP</td><td>recursive self-improvement로 long-context 능력 harness를 개선하는 LongCapHarness, post-training 없이 baseline 능가 주장</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2611.10279'>Restoring General and Improving Domain-Specific Safety in Fine-Tuned LLMs Without Retraining</a></td><td>34</td><td>0</td><td>NLP</td><td>fine-tuning으로 약해진 refusal 방향을 base 모델에서 low-rank 가중치 갱신으로 되돌리는 training-free SPECTRA</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2611.11704'>Scalable Counterfactual Explanations for Time Series via Policy Learning</a></td><td>33</td><td>1</td><td>LG</td><td>시계열 counterfactual 설명을 latent 공간 actor-critic 단일 forward로 생성, counterfactual 주제이나 로봇과 무관한 UCR 데이터 중심</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2611.10856'>Self-contained Data Cleaning for Unsupervised Anomaly Detection</a></td><td>33</td><td>1</td><td>LG</td><td>autoencoder 초기 학습의 cosine 유사도로 오염된 학습 샘플을 제거하는 이상 탐지 전처리임. 보안 데이터셋 평가임</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2611.10536'>In Search of Lost Time: Temporal Competence in Large Language Models</a></td><td>33</td><td>1</td><td>NLP</td><td>LLM이 시간 규칙은 알지만 자기 수행 시간은 최대 99.5% 과소추정함을 보인 평가 분석으로 방법론 기여 없음</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2611.11102'>Task presentation and execution paths shape LLM mathematical performance</a></td><td>33</td><td>0</td><td>NLP</td><td>LLM 수학 문제에서 제출 지시·draft·후보 제공 조건별 정답률을 쌍비교로 분석함. 설계는 통제적이나 규모 작고 로봇과 무관함</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2611.10307'>How Much Is Left Matters: False Positives and False Negatives in Partial-Prompt Contamination Tests</a></td><td>33</td><td>0</td><td>NLP</td><td>partial-prompt contamination 탐지가 남은 텍스트 길이에 따라 오탐·미탐함을 감사함. 평가 분석이며 로봇 무관함</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2611.10248'>FedLoVA: Value-Only Aggregation for Federated LoRA Fine-Tuning of Large Language Models</a></td><td>33</td><td>0</td><td>NLP</td><td>federated LoRA 집계 방식 개선으로 incremental하고 로봇과 무관함</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2611.10202'>Semiprime Factorization with Discrete Diffusion and Beam Search: Scaling Laws</a></td><td>33</td><td>0</td><td>LG</td><td>이산 diffusion과 beam search로 소인수분해하는 scaling law 실험임</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2611.10971'>When Safety Becomes An Outlier: Understanding the Retention of LLM Safety Behaviors</a></td><td>33</td><td>0</td><td>NLP</td><td>고정 refusal 문자열이 outlier mode라 fine-tuning에서 잊힌다는 가설과 자연스러운 safety target NEST 제안</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2611.10556'>onóna: Twin Embeddings with Tied Unembeddings</a></td><td>33</td><td>0</td><td>NLP</td><td>임베딩 표 두 개를 섞는 tied unembedding onona, 12개 비교 중 11개 loss 개선, 작은 모듈 추가임</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2611.10450'>The Truth Beneath the Tokens: Prompt-Space Recovery of Knowledge Edits in Language Models</a></td><td>33</td><td>0</td><td>NLP</td><td>편집된 LLM의 pre-edit 지식을 prompt 공간 prefix로 복원하는 Memento, 80.07% 복원</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2611.12060'>COMPASS: Composable Policy-Amortized Structured Search for LLM-Based Optimization Modeling</a></td><td>33</td><td>0</td><td>NLP</td><td>최적화 모델링 template 검색을 DAG 위 DQN 정책으로 학습하는 COMPASS, 작은 모듈 개선 수준이며 로봇 무관함</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2611.11896'>LEGION: Benchmarking Language Agents on Sparse-Signal Investigation Under Adversarial Noise</a></td><td>33</td><td>0</td><td>NLP</td><td>사이버보안 조사용 adversarial noise 시나리오 74개 벤치마크 Legion, agent precision이 0.61~0.72에 머문다는 평가 위주임</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2611.11842'>A Benchmark and Layered Evaluation Protocol for Evidence-Grounded Shared Belief Updating in Connected Robotics</a></td><td>32</td><td>4</td><td>Embodied AI</td><td>연결 로봇 공유 belief 갱신 benchmark로 기여가 평가 프로토콜에 한정됨</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2611.11050'>Floquet-Parameterized Koopman-MPC for Tracking Periodic Orbits</a></td><td>32</td><td>4</td><td>Control</td><td>Floquet Koopman MPC 주기 궤도 추적으로 제어 이론 계열임</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2611.12261'>Hierarchical Multi-Channel Tip-Over Prediction via Isolated Temporal Models for Planetary Rover Safety</a></td><td>32</td><td>3</td><td>Mobile Robot</td><td>행성 rover tip-over 예측 시계열 모델로 응용 특화임</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2611.10298'>Mobility Information Capacity of Multi-Robot Systems: Safety-Aware Maneuver Design</a></td><td>32</td><td>3</td><td>Multi-Robot</td><td>다중 로봇 이동성 정보 용량 이론 분석임</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2611.11055'>But It Was True When I Checked: Compiling SHOP-Style Method Preconditions into Partially-Ordered HTN Planning</a></td><td>32</td><td>3</td><td>Planning</td><td>SHOP식 method precondition을 부분순서 HTN 계획으로 사실 두 개만 추가해 컴파일하는 이론 결과, 계획 이론 기여이나 실험이 없음</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2611.12739'>Plant Orbiter: 3D Plant Reconstruction and Generation with Video Diffusion Orbit Cameras and 3D Gaussian Splatting</a></td><td>32</td><td>2</td><td>3D Vision</td><td>식물 3D 재구성/생성, 응용 특화</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2611.12092'>CRAFT-AI: Capability and Requirement Alignment for Flexible Manufacturing through Agentic AI</a></td><td>32</td><td>2</td><td>Industrial AI</td><td>자연어 요구를 AAS 기반 capability와 매칭해 Factory I/O 제조 scene을 생성하는 agent, 시나리오 5개 수준의 타당성 시연임</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2611.11875'>Beyond Head Importance: Collective Computation in Video Transformers</a></td><td>32</td><td>1</td><td>Video</td><td>video transformer head 집합 분석</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2611.10509'>Scaling Optimization-Oriented Hypernetworks for Implicit Neural Representations</a></td><td>32</td><td>1</td><td>Representation</td><td>INR hypernetwork scaling</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2611.10344'>MaRiO: Multi-agent Collaborative Reasoning via Shared Observations in MLLMs</a></td><td>32</td><td>1</td><td>Multimodal</td><td>MLLM 다중 agent 협업 추론</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2611.10066'>VLM as an Editing Pilot: VLM-Steered Velocity Control for Flow-Based Image Editing</a></td><td>32</td><td>1</td><td>Generative</td><td>VLM 조종 flow 이미지 편집</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2611.12662'>Certify, Report, or Refuse: Harm-Constrained Conformal Prediction for Clinical Actions</a></td><td>32</td><td>1</td><td>LG</td><td>harm penalty를 넣은 conformal prediction으로 임상 행동 오류를 줄이나 의료 분류에 한정됨</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2611.11792'>APO2CS: Advantage-Aware Preference Optimization for Two-Level Constructive Search in Combinatorial Optimization</a></td><td>32</td><td>1</td><td>LG</td><td>조합 최적화 neural solver에 advantage 가중 및 부분 궤적 preference 최적화 적용, 로봇 직접 연관은 없음</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2611.11913'>CHORD: Multi-resolution Compression for Multimodal Time Series</a></td><td>32</td><td>1</td><td>LG</td><td>웨어러블 다중모달 시계열을 coarse-to-fine residual cascade와 FSQ로 고정 bit rate 압축하는 CHORD, 센서 데이터 압축이라 로봇과는 약하게 연결됨</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2611.11633'>An Interpretable Fuzzy Tree for Turbofan Remaining Useful Life with an Auditable Per-Component Diagnostic Layer</a></td><td>32</td><td>1</td><td>LG</td><td>터보팬 RUL을 계층형 genetic fuzzy tree로 예측하고 부품별 진단 층을 노출, 파라미터 333개로 가볍지만 prognostics 도메인임</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2611.10610'>Efficient LLM Adaptation with Forward-Only Passes</a></td><td>32</td><td>1</td><td>LG</td><td>forward pass만으로 SVD 성분 dispersion을 보고 rank reduction 대상 행렬을 찾는 LLM adaptation, 효율 개선이나 incremental</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2611.10411'>Tail-risk-aware Agent Safety: Constraining Tail Risks Across Multi-step LLM Agent Workflows</a></td><td>32</td><td>1</td><td>AI Safety</td><td>agent workflow 단계별 위험 전이를 MDP로 모델링하고 tail risk에 공유 budget을 두는 안전 프레임워크, LLM agent 한정</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2611.12187'>Harnessing Vision-Language Models for Federated Unsupervised Visual Recognition</a></td><td>32</td><td>0</td><td>CV</td><td>CLIP pseudo-label과 prompt 집계로 federated 비지도 인식을 하는 FedUR로 incremental 성격임</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2611.12141'>Do Time-Series Foundation Models Forecast Index-Futures Returns? A Preregistered Evaluation of Models, Metrics, and Input Representations</a></td><td>32</td><td>0</td><td>LG</td><td>시계열 foundation model이 선물 수익률에서 no-change를 못 이김을 사전 등록 평가로 보인 부정적 결과 연구</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2611.12079'>Correct First, Fast Second: What a Local 7B Code Model Can and Cannot Do for GPU Kernel Optimization</a></td><td>32</td><td>0</td><td>LG</td><td>7B 코드 모델의 GPU kernel 최적화에서 correctness가 병목임을 30개 task로 보인 소규모 실증 연구임</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2611.12031'>Scale-Invariant Empirical-Bayes Laplace Approximation for ReLU Networks</a></td><td>32</td><td>0</td><td>LG</td><td>ReLU scale symmetry에 불변하게 empirical Bayes Laplace 근사를 정의하는 canonicalization으로 베이지안 이론 성격임</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2611.11526'>A Stability Analysis of AdamW: Unstable Equilibria and Non-Convergence</a></td><td>32</td><td>0</td><td>LG</td><td>AdamW 고정점의 불안정성과 비수렴을 동역학으로 분석하고 수렴 변형 제안, 최적화 이론으로 로봇 무관</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2611.10923'>Prescriptive Learning of Linear Policies with Feasibility Guarantees for Binary Decision-Making</a></td><td>32</td><td>0</td><td>LG</td><td>이진 의사결정 선형 정책을 유한 feasibility 보장과 함께 prescriptive하게 학습함. 에너지·인력 배정 응용임</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2611.10838'>Learning Biological Hierarchies in Single-Cell Foundation Models</a></td><td>32</td><td>0</td><td>LG</td><td>cell ontology의 LCA 거리를 임베딩에 반영하는 단일세포 foundation model임. 생물 도메인임</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2611.10700'>Spectral Bias Reduction in Local Gated ReLU Architectures</a></td><td>32</td><td>0</td><td>LG</td><td>gated local ReLU로 spectral bias를 줄이는 이론 분석임. 1D 회귀·Poisson 한정임</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2611.10611'>Detent: Batch-Invariant LLM Serving and RL Rollouts at Near-Stock Speed</a></td><td>32</td><td>0</td><td>LG</td><td>LLM 서빙에서 batch-invariant 커널 선택을 고정해 RL rollout 재현성을 확보하는 Detent임. 시스템 작업이며 로봇 무관함</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2611.10563'>Confronting Uncertainty in Mechanism-AI Coupled Dynamical Systems via Optimal Transport and Information Geometry: Part I. Distribution Learning</a></td><td>32</td><td>0</td><td>LG</td><td>mechanism-AI 동역학계의 불확실성을 optimal transport와 정보기하로 정식화함. 생물계 수학 이론이고 로봇 무관함</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2611.10230'>RAD-TFM: Robust and Domain-Adapted Tabular Foundation Models</a></td><td>32</td><td>0</td><td>LG</td><td>tabular foundation model의 domain 적응 강건화로 로봇과 무관함</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2611.09928'>MAGE: Towards Generalizable Multi-timescale EEG Representations</a></td><td>32</td><td>0</td><td>LG</td><td>multi-timescale EEG 표현 학습으로 로봇과 무관함</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2611.12791'>Large Language Models as a Universal Searcher for Open-World Automated Machine Learning</a></td><td>32</td><td>0</td><td>LG</td><td>LLM을 open-world AutoML 탐색기로 씀</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2611.11838'>Improving Confidence Estimation in Language Models with Linear Representations of Ambiguity</a></td><td>32</td><td>0</td><td>NLP</td><td>모호성 선형 표현으로 신뢰도 추정을 개선함</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2611.11027'>MoTo: Mixture of Tokenizers Towards Fair Multilingual Language Modeling</a></td><td>32</td><td>0</td><td>NLP</td><td>언어별 BPE tokenizer를 합쳐 다국어 형평성을 높이는 MoTo, 21개 언어 중 18개 개선이나 로봇 무관</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2611.10258'>Beyond the Prompt: Leveraging Pre-Decoding States for Jailbreak Detection in dLLMs</a></td><td>32</td><td>0</td><td>NLP</td><td>diffusion LLM의 decoding 전 hidden state로 jailbreak를 탐지하는 ReFuse, ASR 63%에서 3.3%로 감소</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2611.12374'>TANSAR: Editable and Attributable Correlation Matrix Memories under Correlated Keys, with Rule-Constrained Multi-Hop Knowledge Editing</a></td><td>32</td><td>0</td><td>LG</td><td>correlated key에서 correlation matrix memory의 용량과 정확한 삭제를 분석하고 Horn 제약 다중 홉 편집 TANSAR 제안</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2611.11771'>ARMOR: Adaptive Curriculum Meta-Learning for Noise-Robust RAG Reasoning</a></td><td>32</td><td>0</td><td>NLP</td><td>RAG 노이즈 강건성을 세 하위 과제로 나누고 curriculum meta-learning으로 GRPO 변형을 학습하는 ARMOR, QA 벤치마크 한정</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2611.10049'>LoRazor: Trimming Adapter Execution for Efficient Multi-LoRA Serving</a></td><td>32</td><td>0</td><td>Systems</td><td>디코딩 중 adapter를 조기 해제하고 active-row 커널로 multi-LoRA 처리량을 3.02배 높인 서빙 최적화</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2611.10518'>Beyond Row Alignment: Virtual-Camera-Aware Online Stereo Rectification</a></td><td>30</td><td>3</td><td>3D Vision</td><td>online stereo rectification, 로봇 stereo에 유용하나 incremental</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2611.11580'>Qubit-to-Motion: Traceable Action Provenance in Hybrid QRL for Robotic Bin-Packing Sequencing</a></td><td>30</td><td>3</td><td>RL</td><td>하이브리드 양자 RL bin-packing action 추적성으로 실용성 낮음</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2611.11131'>CrossLiDAR: Controllable Multi-Sensor LiDAR Sequence Generation</a></td><td>30</td><td>2</td><td>3D Vision</td><td>다중 센서 LiDAR 생성</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2611.12314'>A Modular Perspective for Modeling MARL Systems</a></td><td>30</td><td>2</td><td>RL</td><td>MARL을 8개 모듈로 분해하고 MARLKIT으로 구현한 서베이성 프레임워크라 새 방법 기여 약함</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2611.11712'>Variational Approach to Optimal IPS Estimator for Multi-logger Off-Policy Evaluation</a></td><td>30</td><td>2</td><td>RL</td><td>multi-logger off-policy evaluation에서 분산 최소 IPS 가중치를 변분법으로 유도, OPE 이론이라 로봇 직접 연관은 약함</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2611.11529'>Data Manipulation Attacks Against Machine Learning Integrated Cyber-Physical Systems</a></td><td>30</td><td>2</td><td>LG</td><td>vision/planning ML이 합성된 CPS에서 optimal attack policy를 계산하는 work-in-progress, 로봇 시스템 보안에 가깝지만 실험 없음</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2611.11515'>Detecting Common Golfing Faults Using AI and Video-Derived Biomechanical Features</a></td><td>30</td><td>2</td><td>CV</td><td>영상에서 pose와 clubhead를 추적해 골프 스윙 결함을 boosted tree로 분류, 해석 가능하나 소규모 스포츠 응용</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2611.11423'>Computationally Efficient Offline Policy Optimization with All-Policy Linear Realizability</a></td><td>30</td><td>2</td><td>RL</td><td>all-policy linear realizability 하의 offline policy optimization 다항시간 알고리즘, offline RL 이론이나 실용성 낮음</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2611.10981'>An Analysis of Reinforcement Learning with Function Approximation</a></td><td>30</td><td>2</td><td>RL</td><td>함수 근사 Q-learning의 수렴 조건을 다룬 고전 논문의 정정판임. 새로운 결과가 아님</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2611.12445'>LongSCOP: Semantically Consistent Long Video Outpainting</a></td><td>30</td><td>1</td><td>Video</td><td>긴 영상 outpainting, 로봇 연결 약함</td></tr>
<tr><td>486</td><td><a href='https://arxiv.org/abs/2611.11272'>BiRefNet-V2: Rethinking Bilateral Reference for High-Resolution Dichotomous Image Segmentation</a></td><td>30</td><td>1</td><td>CV</td><td>dichotomous segmentation 개선판</td></tr>
<tr><td>487</td><td><a href='https://arxiv.org/abs/2611.11041'>Virtual Task Prompting for Multi-Task Scene Understanding</a></td><td>30</td><td>1</td><td>CV</td><td>multi-task scene understanding virtual prompt</td></tr>
<tr><td>488</td><td><a href='https://arxiv.org/abs/2611.10714'>Permute-then-Adapt: Weak-to-Strong Contrastive Image-Text Adaptation</a></td><td>30</td><td>1</td><td>Multimodal</td><td>CLIP 약-강 contrastive adaptation</td></tr>
<tr><td>489</td><td><a href='https://arxiv.org/abs/2611.10559'>CompositionEvidence: Controlling Geometric Evidence for Cinematic Composition Reasoning with Frozen Vision-Language Models</a></td><td>30</td><td>1</td><td>Multimodal</td><td>영화 구도 reasoning 기하 증거</td></tr>
<tr><td>490</td><td><a href='https://arxiv.org/abs/2611.12689'>CoilStellaration: A Dataset and Benchmark for Engineering-Aware Stellarator Coilset Generation</a></td><td>30</td><td>1</td><td>LG</td><td>스텔라레이터 코일 설계용 17.7만 개 데이터셋 벤치마크로 도메인이 핵융합이라 로봇과 거리가 멂</td></tr>
<tr><td>491</td><td><a href='https://arxiv.org/abs/2611.12427'>UCB-min: Combining Bandits Under Variance Heterogeneity (Extended Version)</a></td><td>30</td><td>1</td><td>LG</td><td>분산 이질성 아래 UCB 보너스를 arm별로 고르는 UCB-min bandit 알고리즘이며 로봇과 간접적임</td></tr>
<tr><td>492</td><td><a href='https://arxiv.org/abs/2611.12090'>TSFFormer: A Frequency-Domain Spike Transformer for Green Human Activity Recognition</a></td><td>30</td><td>1</td><td>LG</td><td>주파수 영역 attention을 쓴 spiking transformer로 IMU 활동 인식을 저전력화하나 로봇 직접 연결은 약함</td></tr>
<tr><td>493</td><td><a href='https://arxiv.org/abs/2611.11881'>When Does Physics Beat Data? Data-Efficient Traffic State Estimation with Amortized PINNs</a></td><td>30</td><td>1</td><td>LG</td><td>LWR 보존 법칙을 PINN prior로 넣어 센서가 드문 교통 상태 추정의 데이터 효율을 올린 응용임</td></tr>
<tr><td>494</td><td><a href='https://arxiv.org/abs/2611.11839'>MOOD: Benchmarking Post-Hoc OOD Detection for Materials Property Prediction</a></td><td>30</td><td>1</td><td>LG</td><td>재료 물성 GNN용 post-hoc OOD detector 15종이 chance 수준임을 보인 benchmark, OOD 진단 분석은 있으나 도메인이 다름</td></tr>
<tr><td>495</td><td><a href='https://arxiv.org/abs/2611.11204'>Not Yet in the Profile: Uncertainty-Aware Dynamic User Profiling by Learning from Future Interactions</a></td><td>30</td><td>1</td><td>LG</td><td>Profile, Buffer, Rulebook으로 모호한 사용자 행동을 분리 관리하는 UAPM, memory 구조는 있으나 웹 개인화 응용</td></tr>
<tr><td>496</td><td><a href='https://arxiv.org/abs/2611.10950'>Interpretable Cyber-Physical Attack Detection in Smart Grids: A Leakage-Controlled Multi-Testbed Evaluation of Fusion, Robustness, and Observability Limits</a></td><td>30</td><td>1</td><td>LG</td><td>스마트 그리드 사이버물리 공격 탐지를 leakage 통제 하에 평가함. 보안 도메인이고 Random Forest 중심임</td></tr>
<tr><td>497</td><td><a href='https://arxiv.org/abs/2611.10281'>Transit-Oriented Land Use Planning Using Deep Reinforcement Learning</a></td><td>30</td><td>1</td><td>RL</td><td>도시 토지이용 계획에 deep RL 적용한 응용 연구로 로봇과 무관함</td></tr>
<tr><td>498</td><td><a href='https://arxiv.org/abs/2611.11573'>Beyond the Transcript: Measuring and Improving the Use of Acoustic Information in Audio Language Models</a></td><td>30</td><td>1</td><td>Multimodal</td><td>audio LM의 음향 정보 활용 측정과 개선임</td></tr>
<tr><td>499</td><td><a href='https://arxiv.org/abs/2611.10224'>Jais 3: Introducing Arabic-centric Agentic AI</a></td><td>30</td><td>1</td><td>NLP</td><td>아랍어 중심 agentic 모델 Jais 3 여섯 크기 공개, continual pretraining과 RLVR 적용한 모델 보고서</td></tr>
<tr><td>500</td><td><a href='https://arxiv.org/abs/2611.12478'>AuDiR: Diagnosing Audio Reasoning with Rule and Percept Interventions</a></td><td>30</td><td>1</td><td>Multimodal</td><td>오디오 추론 실패를 지각, 규칙 지식, 규칙 적용으로 개입 분해하는 AuDiR, 201개 항목 소규모 진단</td></tr>
<tr><td>501</td><td><a href='https://arxiv.org/abs/2611.12118'>Joi-Bench-Task: Benchmarking Task Coordination in Full-duplex Voice Agents through Interactive Simulation</a></td><td>30</td><td>1</td><td>NLP</td><td>full-duplex 음성 agent의 작업 실행과 대화 조율 실패를 사용자 시뮬레이터로 재는 벤치마크, 로봇과는 거리 있음</td></tr>
<tr><td>502</td><td><a href='https://arxiv.org/abs/2611.12014'>Benchmarking language models and agents for scientific reasoning in evolving materials laboratories</a></td><td>30</td><td>1</td><td>NLP</td><td>합금 소재 연구에서 LLM 과학 추론과 관측 누적 시 예측 수정을 평가하는 MatScope 벤치마크, 도메인 특화라 로봇 연결 약함</td></tr>
<tr><td>503</td><td><a href='https://arxiv.org/abs/2611.11734'>A Bifurcation-Theoretic Framework for the Controllability of Emergent Intelligent Systems</a></td><td>30</td><td>1</td><td>Theory</td><td>창발과 제어 가능성을 서로 다른 bifurcation으로 보는 이론 틀, 고정점 분석 중심이고 실제 시스템 검증이 없음</td></tr>
<tr><td>504</td><td><a href='https://arxiv.org/abs/2611.11659'>RADE: Risk-Adjusted Deployment Efficiency, A Framework for Routing, Memory, and Escalation in Safe LLM Systems</a></td><td>30</td><td>1</td><td>AI</td><td>routing, memory, escalation을 위험 비용 포함 deployment policy로 보는 RADE 관점 논문, 실험 없이 개념 제안에 그침</td></tr>
<tr><td>505</td><td><a href='https://arxiv.org/abs/2611.11348'>Separation of Skilling Context for Standard Operating Procedure-based Agents</a></td><td>30</td><td>1</td><td>NLP</td><td>SOP와 contextual knowledge를 분리해 skill drift를 줄이는 방식, Indeed 워크플로 8개에서 동등성 12%에서 58%로 오른 소규모 평가임</td></tr>
<tr><td>506</td><td><a href='https://arxiv.org/abs/2611.10453'>BunshinRL: Splitting Live Agent Workspaces for Memory-Efficient Agentic RL</a></td><td>30</td><td>1</td><td>Systems</td><td>container 전체를 fork하는 BunshinFork로 agentic RL rollout 메모리를 최대 51% 줄인 시스템 연구, LLM agent 한정</td></tr>
<tr><td>507</td><td><a href='https://arxiv.org/abs/2611.10176'>AVCORP: Identifying and Resisting Deception via Communication Theory and Theory of Mind</a></td><td>30</td><td>1</td><td>NLP</td><td>Avalon 게임 250판에 ToM 추론 trace를 붙인 AVCORP로 Qwen3-8B 기만 탐지기를 학습, 게임 도메인 한정</td></tr>
<tr><td>508</td><td><a href='https://arxiv.org/abs/2611.12243'>CADMA: Capacity-Aware Coverage Decomposition for Generative Model Assessment</a></td><td>30</td><td>0</td><td>Generative</td><td>생성 모델 coverage 평가 지표</td></tr>
<tr><td>509</td><td><a href='https://arxiv.org/abs/2611.11147'>Not All Layers Are Equal in Image-to-Video Transfer</a></td><td>30</td><td>0</td><td>Video</td><td>image-to-video 적응 layer별 adapter</td></tr>
<tr><td>510</td><td><a href='https://arxiv.org/abs/2611.12884'>Guiding Data Allocation for Robust Subpopulation Generalization</a></td><td>30</td><td>0</td><td>LG</td><td>부분집단 일반화 데이터 할당</td></tr>
<tr><td>511</td><td><a href='https://arxiv.org/abs/2611.12835'>Mitigating Agentic Deception via Evaluation-Side Partially Observable Games</a></td><td>30</td><td>0</td><td>NLP</td><td>agent 기만 완화 게임</td></tr>
<tr><td>512</td><td><a href='https://arxiv.org/abs/2611.12832'>What the Loss Curve Misses: FP4 Pretraining Slows the Acquisition of Rare Facts</a></td><td>30</td><td>0</td><td>LG</td><td>FP4 사전학습이 희귀 사실 습득 늦춤</td></tr>
<tr><td>513</td><td><a href='https://arxiv.org/abs/2611.12729'>KiteNorm: Variance Regularisation for Stable and Scalable Post-LN Transformers</a></td><td>30</td><td>0</td><td>LG</td><td>Post-LN Transformer 안정화</td></tr>
<tr><td>514</td><td><a href='https://arxiv.org/abs/2611.12591'>TRACE: Adaptive Trust-Region Bayesian Optimization for Open-Ended Molecular Design</a></td><td>30</td><td>0</td><td>LG</td><td>분자 설계용 trust-region Bayesian optimization으로 로봇 연관 없음</td></tr>
<tr><td>515</td><td><a href='https://arxiv.org/abs/2611.12491'>Out-of-the-Box Tabular Foundation Models for Bayesian Optimization in Materials Discovery</a></td><td>30</td><td>0</td><td>LG</td><td>TabPFN 등 tabular foundation model을 재료 BO surrogate로 평가한 비교 연구로 참신성 낮음</td></tr>
<tr><td>516</td><td><a href='https://arxiv.org/abs/2611.12285'>Learning Evidence-Grounded Reasoning for Context-Aware Time Series Forecasting</a></td><td>30</td><td>0</td><td>LG</td><td>시계열 예측에 구조화된 CoT와 SFT+RL을 쓰는 CastReasoner로 로봇과 무관한 benchmark 개선 성격임</td></tr>
<tr><td>517</td><td><a href='https://arxiv.org/abs/2611.12186'>NearFormer: Linear-Size Sparse Attention via Randomized Near Neighbors</a></td><td>30</td><td>0</td><td>LG</td><td>랜덤 near-neighbor 그래프로 graph transformer attention을 선형 크기로 줄인 NearFormer로 로봇 무관</td></tr>
<tr><td>518</td><td><a href='https://arxiv.org/abs/2611.12160'>Beyond Flat Walks: Compositional Abstraction for Autoregressive Graph Generation</a></td><td>30</td><td>0</td><td>LG</td><td>계층적 추상화로 autoregressive 그래프 생성 직렬화를 비교한 분자 중심 연구임</td></tr>
<tr><td>519</td><td><a href='https://arxiv.org/abs/2611.11977'>MixRoute: Rethinking Single-Distribution Training for Generalizable Neural Routing</a></td><td>30</td><td>0</td><td>LG</td><td>Mix Normalization으로 단일 분포 학습 neural routing의 zero-shot 일반화를 올리는 NCO 연구임</td></tr>
<tr><td>520</td><td><a href='https://arxiv.org/abs/2611.11318'>PROLA: Principal-Orthogonal Low-rank Adaptation for Predictive Spatiotemporal Weather Downscaling</a></td><td>30</td><td>0</td><td>LG</td><td>날씨 downscaling용 principal-orthogonal LoRA인 PROLA, LoRA 변형 incremental</td></tr>
<tr><td>521</td><td><a href='https://arxiv.org/abs/2611.11081'>A Hierarchical Tokenization Framework for Voxel-Level fMRI Representation Learning</a></td><td>30</td><td>0</td><td>LG</td><td>voxel 단위 fMRI를 계층 tokenization으로 최대 415배 압축함. 뇌영상 도메인이라 로봇 연관 없음</td></tr>
<tr><td>522</td><td><a href='https://arxiv.org/abs/2611.11063'>Target Recoverability under Selective Labels: A Failure Mode in ECG-Based Acute Coronary Syndrome Prediction</a></td><td>30</td><td>0</td><td>LG</td><td>ECG 기반 ACS 예측에서 선택적 라벨 때문에 모델이 미검사군에서 우연 이하로 떨어짐을 보임. 의료 ML 분석이라 로봇 무관함</td></tr>
<tr><td>523</td><td><a href='https://arxiv.org/abs/2611.10855'>Representing Tensors as Compositions for Efficient Computation on Sparse and Structured Data</a></td><td>30</td><td>0</td><td>LG</td><td>텐서를 index 함수 합성으로 표현하는 대수 형식을 제안함. 개념 제안 수준이고 실험이 부족함</td></tr>
<tr><td>524</td><td><a href='https://arxiv.org/abs/2611.10730'>Breaking Precision Walls in First-, Second-, and Zeroth-Order Optimizers: One Constant, Set in Advance</a></td><td>30</td><td>0</td><td>LG</td><td>Adam·Shampoo의 상수 하나가 precision wall을 정한다는 최적화 분석임. 합성 문제 위주이고 로지스틱 회귀에서는 규칙이 성립하지 않음</td></tr>
<tr><td>525</td><td><a href='https://arxiv.org/abs/2611.10691'>A Geometric Theory for Nonequilibrium Transformer Dynamics</a></td><td>30</td><td>0</td><td>LG</td><td>Transformer attention 동역학을 free energy의 Fisher-Rao gradient flow로 기술하는 이론임. 실험이 없고 로봇 무관함</td></tr>
<tr><td>526</td><td><a href='https://arxiv.org/abs/2611.10468'>Dynamic State Estimation from Sparse PMUs via Physics-Informed Graph Neural Operators</a></td><td>30</td><td>0</td><td>LG</td><td>희소 PMU로 전력계통 동적 상태를 physics-informed 그래프 operator로 추정함. 전력 도메인임</td></tr>
<tr><td>527</td><td><a href='https://arxiv.org/abs/2611.10408'>Sharp Logarithmic-Product Bounds for List Replicability of Sign Matrices</a></td><td>30</td><td>0</td><td>LG</td><td>list replicability의 로그곱 상한을 증명하는 292쪽 순수 조합론임. 로봇 무관함</td></tr>
<tr><td>528</td><td><a href='https://arxiv.org/abs/2611.10380'>Quantitative Assessment of Crystal Structure Prediction</a></td><td>30</td><td>0</td><td>LG</td><td>결정 구조 예측 평가용 OPAL-Bench와 baseline을 제시함. 재료 과학 벤치마크임</td></tr>
<tr><td>529</td><td><a href='https://arxiv.org/abs/2611.10334'>Reproducible LoRA Inference Through Deterministic Split-K Reduction</a></td><td>30</td><td>0</td><td>NLP</td><td>LoRA split-K 원자 덧셈의 비결정성을 결정적 Triton 구현으로 제거함. 커널 엔지니어링임</td></tr>
<tr><td>530</td><td><a href='https://arxiv.org/abs/2611.10325'>Update Slope Is Bounded by Prior Calibration: A Structural Bound and Its Contingent Empirical Signature</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 예측자의 update slope가 prior calibration으로 상한이 정해지는 confound를 분석함. 평가 방법론이며 로봇 무관함</td></tr>
<tr><td>531</td><td><a href='https://arxiv.org/abs/2611.10212'>DisMUSE: An Efficient Distributed Singular-Spectrum-Based Optimization Approach with Theoretical Convergence Guarantee</a></td><td>30</td><td>0</td><td>LG</td><td>분산 singular-spectrum 최적화기의 수렴 보장 연구임</td></tr>
<tr><td>532</td><td><a href='https://arxiv.org/abs/2611.10186'>Projected Neural Additive Models as Universal Approximators</a></td><td>30</td><td>0</td><td>LG</td><td>neural additive model의 universal approximation 이론임</td></tr>
<tr><td>533</td><td><a href='https://arxiv.org/abs/2611.12856'>WorkflowArena: Benchmarking Executable Workflow Orchestration in LLM-Based Multi-Agent Systems</a></td><td>30</td><td>0</td><td>NLP</td><td>multi-agent workflow 오케스트레이션 benchmark임</td></tr>
<tr><td>534</td><td><a href='https://arxiv.org/abs/2611.12429'>Can Frontier Auto Researchers Reconstruct Human Research Decisions in AI?</a></td><td>30</td><td>0</td><td>NLP</td><td>auto researcher의 연구 결정 재현 평가임</td></tr>
<tr><td>535</td><td><a href='https://arxiv.org/abs/2611.12184'>Blind Variation, Selective Retention: Improving Creative Idea Generation in AI Scientists</a></td><td>30</td><td>0</td><td>NLP</td><td>AI scientist 아이디어 창의성 개선 방법임</td></tr>
<tr><td>536</td><td><a href='https://arxiv.org/abs/2611.11724'>Explaining and interrupting collective misalignment in language model systems</a></td><td>30</td><td>0</td><td>NLP</td><td>LM 집단 오정렬 설명과 차단 연구임</td></tr>
<tr><td>537</td><td><a href='https://arxiv.org/abs/2611.11396'>Search-by-Answer Bias in Retrieval Models</a></td><td>30</td><td>0</td><td>NLP</td><td>retriever의 search-by-answer 편향 분석임</td></tr>
<tr><td>538</td><td><a href='https://arxiv.org/abs/2611.10926'>DeepFinance: Can AI Diligence a $100MM Deal?</a></td><td>30</td><td>0</td><td>NLP</td><td>PE/IB 실무 21개 장기 과제 benchmark DeepFinance, 최고 모델 rubric 57.6% 충족, 단순 평가셋 성격</td></tr>
<tr><td>539</td><td><a href='https://arxiv.org/abs/2611.10848'>MultiTurnRoute: A Platform for Building and Evaluating Multi-Turn LLM Routers</a></td><td>30</td><td>0</td><td>NLP</td><td>multi-turn LLM router 플랫폼과 Chain-of-Route 제안, 비용 20.3% 절감하나 로봇 무관</td></tr>
<tr><td>540</td><td><a href='https://arxiv.org/abs/2611.10502'>Distinguishing Extraction Failures and Clinical Discordance with LLM Uncertainty on Radiology Reports</a></td><td>30</td><td>0</td><td>NLP</td><td>방사선 보고서 추출에서 LLM 불확실성이 추출 실패는 잡지만 임상 불일치는 못 잡는다는 failure attribution 분석</td></tr>
<tr><td>541</td><td><a href='https://arxiv.org/abs/2611.12762'>Sage-Taiyi: A Metacognitive Architecture for Scientific Discovery</a></td><td>30</td><td>0</td><td>NLP</td><td>metacognition 구조의 과학 발상 agent Sage-Taiyi, ideation benchmark에서 AI Scientist-v2 대비 54.0 대 47.9</td></tr>
<tr><td>542</td><td><a href='https://arxiv.org/abs/2611.12164'>Let the Fixer Decide: Training a Code Localizer from the Fixer&#x27;s Likelihood</a></td><td>30</td><td>0</td><td>NLP</td><td>frozen fixer 우도로 code localizer를 weighted SFT하는 소형 코딩 agent 학습, 대회용 파이프라인 성격이 강함</td></tr>
<tr><td>543</td><td><a href='https://arxiv.org/abs/2611.11975'>AutoQS: Automated Quantization Strategy Design with Large Language Models</a></td><td>30</td><td>0</td><td>LG</td><td>LLM이 layer별 group size 할당을 탐색하는 양자화 전략 설계 AutoQS, GPTQ 대비 평균 정확도 0.70퍼센트포인트 향상에 그침</td></tr>
<tr><td>544</td><td><a href='https://arxiv.org/abs/2611.11846'>MOTIF: LLM-Defined Material Taxonomies for OOD Property Prediction via Invariant Feature Selection</a></td><td>30</td><td>0</td><td>LG</td><td>LLM이 소재 taxonomy 후보를 만들고 invariant feature selection으로 OOD 밴드갭 MAE를 0.122에서 0.111로 줄임, 소재 도메인 한정</td></tr>
<tr><td>545</td><td><a href='https://arxiv.org/abs/2611.10719'>No Second Run: Does RSI Stop at Frontier Pre-training?</a></td><td>30</td><td>0</td><td>NLP</td><td>30B-A3B MoE 사전학습 전 과정에 RSI를 적용해 base model을 공개한 보고서로 로봇 무관</td></tr>
<tr><td>546</td><td><a href='https://arxiv.org/abs/2611.10697'>Hallucination-Guided Unlearning: Using Hallucination Traces to Reveal Overfitted Memories</a></td><td>30</td><td>0</td><td>NLP</td><td>hallucination 구간에서 책임 MLP neuron을 찾아 편집하는 LLM unlearning으로 TOFU에서 개선, 로봇 무관</td></tr>
<tr><td>547</td><td><a href='https://arxiv.org/abs/2611.10219'>Multi-GPU MoE Inference with Adaptive Expert Offloading</a></td><td>30</td><td>0</td><td>Systems</td><td>MoE 다중 GPU expert offloading에서 GPU-CPU 공동 실행으로 1.9-15.5배 처리량을 낸 시스템 연구</td></tr>
<tr><td>548</td><td><a href='https://arxiv.org/abs/2611.10089'>META-IR: Meta-Introspective Reasoning for Adaptive Safety Alignment in LLM</a></td><td>30</td><td>0</td><td>NLP</td><td>jailbreak 적응을 위해 SI-MCTS 내부 루프와 meta-learning 외부 루프를 쓰는 META-IR 안전 정렬, 소형 모델 검증</td></tr>
<tr><td>549</td><td><a href='https://arxiv.org/abs/2611.10628'>Towards Identity-Preserving LLM Agents under Model Transition</a></td><td>29</td><td>0</td><td>NLP</td><td>LLM backend 교체 시 agent 행동 drift가 모델 조합마다 다르고 말로는 드러나지 않음을 5,760 run으로 보인 분석</td></tr>
<tr><td>550</td><td><a href='https://arxiv.org/abs/2611.10774'>Same Measurements, Different Velocity Risk: Complementary Rolling-Shutter Readouts under Clock Uncertainty</a></td><td>28</td><td>3</td><td>3D Vision</td><td>rolling shutter 속도 추정 분석, 센서 설계</td></tr>
<tr><td>551</td><td><a href='https://arxiv.org/abs/2611.12568'>Modeling and Estimation of a Towed Marine System</a></td><td>28</td><td>3</td><td>Control</td><td>견인 해양 시스템 모델링과 상태 추정으로 응용 특화임</td></tr>
<tr><td>552</td><td><a href='https://arxiv.org/abs/2611.11602'>Martine: Benchmarking Multi-View 3D Surface Reconstruction Across Viewpoint Coverage, Resolution, and Lighting</a></td><td>28</td><td>2</td><td>3D Vision</td><td>다시점 표면 재구성 benchmark</td></tr>
<tr><td>553</td><td><a href='https://arxiv.org/abs/2611.11337'>OPSRL-SSP: Optimistic Posterior Sampling for Stochastic Shortest Path with Minimax-Optimal Regret</a></td><td>28</td><td>2</td><td>RL</td><td>stochastic shortest path에서 minimax 최적 regret의 posterior sampling 알고리즘, RL 이론 기여이나 실용성 낮음</td></tr>
<tr><td>554</td><td><a href='https://arxiv.org/abs/2611.12300'>Reconfigurable Action Theories: A Formal Foundation for Dynamically Composable Agent Harnesses</a></td><td>28</td><td>2</td><td>AI</td><td>실행 중 action theory 자체가 바뀌는 RAT 형식 체계를 ASP로 번역해 agent harness를 검증하나 이론 위주이고 로봇 연결은 약함</td></tr>
<tr><td>555</td><td><a href='https://arxiv.org/abs/2611.12364'>TRIAD: Multimodal Retrieval across Abstraction, Constraints, and State</a></td><td>28</td><td>1</td><td>Multimodal</td><td>멀티모달 retrieval 설정 benchmark, 로봇 연결 약함</td></tr>
<tr><td>556</td><td><a href='https://arxiv.org/abs/2611.12305'>HumanSightBench: A Benchmark for Human Visual Perception in MLLMs</a></td><td>28</td><td>1</td><td>Multimodal</td><td>MLLM 인간 시각 지각 benchmark</td></tr>
<tr><td>557</td><td><a href='https://arxiv.org/abs/2611.12040'>Leveraging Complementary Event Frame and Voxel Representations for RGB-Guided Multimodal Pre-training</a></td><td>28</td><td>1</td><td>CV</td><td>RGB-event 사전학습, 도메인 특화</td></tr>
<tr><td>558</td><td><a href='https://arxiv.org/abs/2611.11751'>GeoPilot: Diagnosis-Guided Interventions and Geometric Evaluation for Aerial Reconstruction</a></td><td>28</td><td>1</td><td>3D Vision</td><td>항공 재구성 진단 기반 개입, 원격탐사 특화</td></tr>
<tr><td>559</td><td><a href='https://arxiv.org/abs/2611.11093'>Does Pose Encoding Matter? Analyzing Geometric Representations for Discrete Motion Vocabulary Learning</a></td><td>28</td><td>1</td><td>Representation</td><td>motion tokenization pose 표현 분석</td></tr>
<tr><td>560</td><td><a href='https://arxiv.org/abs/2611.10672'>Heterogeneous Asymmetric Contrastive Distillation</a></td><td>28</td><td>1</td><td>Efficiency</td><td>이종 구조 distillation</td></tr>
<tr><td>561</td><td><a href='https://arxiv.org/abs/2611.10562'>ZARA: Zero-shot Animatable and Relightable 3D Avatar reconstruction from a single image</a></td><td>28</td><td>1</td><td>3D Vision</td><td>단일 이미지 relightable 아바타</td></tr>
<tr><td>562</td><td><a href='https://arxiv.org/abs/2611.10441'>Split and Bridge: Multimodal Generation via Diffusion Bridging</a></td><td>28</td><td>1</td><td>Generative</td><td>diffusion bridging 멀티모달 생성</td></tr>
<tr><td>563</td><td><a href='https://arxiv.org/abs/2611.10004'>MATA: Motion-aligned Temporal Adapter</a></td><td>28</td><td>1</td><td>Video</td><td>few-shot 행동 인식 temporal adapter</td></tr>
<tr><td>564</td><td><a href='https://arxiv.org/abs/2611.11507'>ConvLUT: Rethinking Convolutional Architectures for Ultra-Low-Latency LUT-Based Inference</a></td><td>28</td><td>1</td><td>LG</td><td>FPGA용 LUT 기반 convolution 구조 ConvLUT로 50ns 미만 지연 달성, 초저지연 하드웨어 추론이며 로봇 연관은 약함</td></tr>
<tr><td>565</td><td><a href='https://arxiv.org/abs/2611.10050'>Selected-Risk Calibration for Feasibility at Returned Decisions</a></td><td>28</td><td>1</td><td>LG</td><td>surrogate 제약 하 결정의 feasibility 보정 연구로 로봇 연결 약함</td></tr>
<tr><td>566</td><td><a href='https://arxiv.org/abs/2611.11897'>ShopMind: A Mental World Model for Personalized and Realistic E-commerce User Simulation</a></td><td>28</td><td>1</td><td>NLP</td><td>전자상거래 사용자 simulation용 mental world model임</td></tr>
<tr><td>567</td><td><a href='https://arxiv.org/abs/2611.11541'>Safeguarding Agentic AI in Radiology Workflows: A Multimodel Evaluation of Rule-based and Large Language Model-based Verification</a></td><td>28</td><td>1</td><td>NLP</td><td>방사선과 문서화 agent에 규칙과 LLM checker를 걸어 고위험 오류율을 19.4%에서 13.2%로 줄인 시뮬레이션 평가, 의료 도메인임</td></tr>
<tr><td>568</td><td><a href='https://arxiv.org/abs/2611.10831'>Multimodal Models Can See, But Can They Think? A Study of Turkish Visual Reasoning</a></td><td>28</td><td>1</td><td>Multimodal</td><td>터키어 시각 추론 퍼즐에서 SFT가 model collapse를 일으킴을 보인 평가 연구로 기여 제한적</td></tr>
<tr><td>569</td><td><a href='https://arxiv.org/abs/2611.10180'>Generative Active Learning for Label-Efficient Pan-Organ Ultrasound Diagnosis</a></td><td>28</td><td>1</td><td>Medical CV</td><td>초음파 진단에서 diffusion 생성 probe로 라벨링할 실제 샘플을 고르는 generative active learning EvoDiff, 의료 응용</td></tr>
<tr><td>570</td><td><a href='https://arxiv.org/abs/2611.12699'>GeoScope: Training-Free Program Execution beyond the Counting Horizon for Ultra-High-Resolution Remote Sensing Question Answering</a></td><td>28</td><td>0</td><td>Multimodal</td><td>원격탐사 VLM training-free 프로그램 실행, 도메인 특화</td></tr>
<tr><td>571</td><td><a href='https://arxiv.org/abs/2611.12524'>EditJudge-Bench: Auditing VLM Image-Edit Judges with Synthetic Ground Truth</a></td><td>28</td><td>0</td><td>Multimodal</td><td>이미지 편집 VLM judge 감사, 로봇 무관</td></tr>
<tr><td>572</td><td><a href='https://arxiv.org/abs/2611.11824'>When to Trust Adaptation: Contextual Fusion for Transferable Vision-Language Prompting</a></td><td>28</td><td>0</td><td>Multimodal</td><td>VLM prompt 적응 신뢰 융합, incremental</td></tr>
<tr><td>573</td><td><a href='https://arxiv.org/abs/2611.11214'>Disentangling Where and When:Factored Spatio-Temporal Explanations for Video Action Recognition</a></td><td>28</td><td>0</td><td>Video</td><td>영상 행동 인식 설명, 분석 위주</td></tr>
<tr><td>574</td><td><a href='https://arxiv.org/abs/2611.12728'>Safe Reinforcement Learning for Multi-Turn Clinical Agents: When Dense Rewards Beat Outcome Rewards</a></td><td>28</td><td>0</td><td>RL</td><td>임상 agent 안전 RL dense reward</td></tr>
<tr><td>575</td><td><a href='https://arxiv.org/abs/2611.12521'>Can the Confidence and Decisions of System 1 Models Be Trusted? An Explainability and Perturbation Audit of Jev-Style Decision Models</a></td><td>28</td><td>0</td><td>NLP</td><td>System 1 결정 모델의 calibration과 설명 신뢰성을 감사하는 벤치마크로 로봇과 무관함</td></tr>
<tr><td>576</td><td><a href='https://arxiv.org/abs/2611.12509'>UniHam: A Large-Scale SOC-Complete Dataset and Benchmark for Hamiltonian Learning in Materials</a></td><td>28</td><td>0</td><td>LG</td><td>SOC 포함 해밀토니안 10만 개 데이터셋 벤치마크로 재료 과학 전용임</td></tr>
<tr><td>577</td><td><a href='https://arxiv.org/abs/2611.12131'>One-Shot Federated Graph Learning via High-Fidelity Proxies and Transferability-Guided Collaboration</a></td><td>28</td><td>0</td><td>LG</td><td>one-shot federated graph learning에서 proxy fidelity와 협업 선택을 개선한 incremental 방법임</td></tr>
<tr><td>578</td><td><a href='https://arxiv.org/abs/2611.12097'>Calibrating Document-Local Boundaries for Contextual Chunk Retrieval</a></td><td>28</td><td>0</td><td>NLP</td><td>late chunking에서 같은 문서 negative의 decision boundary를 보정하는 retrieval 개선임</td></tr>
<tr><td>579</td><td><a href='https://arxiv.org/abs/2611.12067'>XposedMIA: Exploiting Explainable Artificial Intelligence (XAI) for One-Shot Membership Inference Attacks</a></td><td>28</td><td>0</td><td>LG</td><td>LIME와 counterfactual 설명에서 결정 경계 거리를 읽어 한 번의 쿼리로 membership inference를 하는 보안 연구임</td></tr>
<tr><td>580</td><td><a href='https://arxiv.org/abs/2611.12010'>Scalable Bayesian Optimization for Efficient Exploration of Moire Patterns</a></td><td>28</td><td>0</td><td>LG</td><td>CatBoost surrogate BO로 moire 패턴 전역 최적을 1,470개 샘플에 찾은 재료 응용임</td></tr>
<tr><td>581</td><td><a href='https://arxiv.org/abs/2611.12000'>HyPLM Technical Report</a></td><td>28</td><td>0</td><td>LG</td><td>650M 단백질 언어 모델 HyPLM-Flash의 효율 기술 보고서로 로봇 무관</td></tr>
<tr><td>582</td><td><a href='https://arxiv.org/abs/2611.11976'>ShiftCache: Fast and Exact Indel Effect Prediction by Reusing Shifted Reference Encodings</a></td><td>28</td><td>0</td><td>LG</td><td>시프트된 reference 인코딩을 재사용해 indel 효과 예측을 정확히 가속하는 genomics 시스템임</td></tr>
<tr><td>583</td><td><a href='https://arxiv.org/abs/2611.11914'>CRAFT-GBM: Selecting Best Features for Gradient-Boosted Machine Learning</a></td><td>28</td><td>0</td><td>LG</td><td>split-gain 신뢰 구간으로 LightGBM 피처 탐색을 적응시켜 학습 시간을 39.7% 줄인 방법임</td></tr>
<tr><td>584</td><td><a href='https://arxiv.org/abs/2611.11387'>Orthogonal Updates for the Win: Towards Accelerated Adaptive Minimax Optimization</a></td><td>28</td><td>0</td><td>LG</td><td>직교 업데이트와 adaptive stepsize로 minimax 최적화 가속 AdaSGDA, 최적화 이론</td></tr>
<tr><td>585</td><td><a href='https://arxiv.org/abs/2611.11232'>TLRS-DPO: Token-Level Risk Scoring for Better Direct Preference Optimization</a></td><td>28</td><td>0</td><td>NLP</td><td>DPO에 token-level risk score 보상을 더하는 TLRS-DPO, 안전 정렬의 작은 변형</td></tr>
<tr><td>586</td><td><a href='https://arxiv.org/abs/2611.11032'>Finite-Sample and Communication-Efficient Networked Information Aggregation</a></td><td>28</td><td>0</td><td>LG</td><td>DAG 상 에이전트 정보 집계에서 sketch 기반 통신 효율 bound를 증명함. 순수 이론이고 로봇과 무관함</td></tr>
<tr><td>587</td><td><a href='https://arxiv.org/abs/2611.10898'>Optimal Byzantine-resilient Federated Learning with User-level Differential Privacy</a></td><td>28</td><td>0</td><td>LG</td><td>user-level DP와 Byzantine 내성을 동시에 갖춘 federated learning의 최적 수렴 bound임. 이론이고 로봇 무관함</td></tr>
<tr><td>588</td><td><a href='https://arxiv.org/abs/2611.10772'>Universal Approximation by Equivariant Message-Passing Graph Neural Networks with a Bilinear Readout</a></td><td>28</td><td>0</td><td>LG</td><td>bilinear readout 등변 GNN의 universal approximation을 증명함. 원자 포텐셜 이론이라 로봇 무관함</td></tr>
<tr><td>589</td><td><a href='https://arxiv.org/abs/2611.10466'>The Fast Tree Transform</a></td><td>28</td><td>0</td><td>LG</td><td>임의 그래프용 Fast Tree Transform을 정의함. 짧은 수학 제안이며 실험 근거가 약함</td></tr>
<tr><td>590</td><td><a href='https://arxiv.org/abs/2611.10375'>CHARM: Certified Homology-Aware Reverse-scale Mapping via Diffusion-Guided Quotient Towers</a></td><td>28</td><td>0</td><td>LG</td><td>차원 축소에 인증된 homology 기록을 붙이는 CHARM임. 위상 데이터 분석이며 로봇 무관함</td></tr>
<tr><td>591</td><td><a href='https://arxiv.org/abs/2611.10364'>Bias, Measurement Error, and Double-Dipping: When Can GNN Convolutions Help Brain Connectome Prediction?</a></td><td>28</td><td>0</td><td>LG</td><td>뇌 connectome 예측에서 GNN이 실패하는 이유를 errors-in-variables로 설명함. 신경과학 통계 분석임</td></tr>
<tr><td>592</td><td><a href='https://arxiv.org/abs/2611.10247'>Can Time Series Foundation Models Serve as Surrogates for Power Systems Dynamic Simulation?</a></td><td>28</td><td>0</td><td>LG</td><td>전력계통 시뮬레이션에 시계열 foundation model 적용한 평가 연구임</td></tr>
<tr><td>593</td><td><a href='https://arxiv.org/abs/2611.10198'>BO-Arena: An Evolving Benchmark for High-Dimensional Bayesian Optimisation</a></td><td>28</td><td>0</td><td>LG</td><td>고차원 BO 벤치마크 제안으로 기여가 benchmark에 한정됨</td></tr>
<tr><td>594</td><td><a href='https://arxiv.org/abs/2611.12311'>MNN-Pocket-0.3B Technical Report</a></td><td>28</td><td>0</td><td>NLP</td><td>0.3B 소형 LM 기술 보고서임</td></tr>
<tr><td>595</td><td><a href='https://arxiv.org/abs/2611.10541'>AFVE-Bench: Measuring Abandoned-Frame Verbalization Errors in Multi-Turn LLM Revision</a></td><td>28</td><td>0</td><td>NLP</td><td>multi-turn 수정에서 버린 frame이 응답에 다시 드러나는 오류를 재는 AFVE-Bench, 25.5% 발생</td></tr>
<tr><td>596</td><td><a href='https://arxiv.org/abs/2611.12122'>System Optimizations for Cost-Efficient Agent Harnesses</a></td><td>28</td><td>0</td><td>NLP</td><td>Claude Code 등 기존 harness에 끼워 토큰 비용을 최대 35% 줄이는 Agency 플랫폼, 시스템 최적화 성격이라 로봇 연결 없음</td></tr>
<tr><td>597</td><td><a href='https://arxiv.org/abs/2611.12013'>Enhancing Multi-Step Chemical Mechanism Prediction with Graph-Guided Preference Data</a></td><td>28</td><td>0</td><td>LG</td><td>화학 반응 mechanism 지식 그래프로 LLM 경로 예측을 보강하는 GRMP, 화학 도메인이라 로보틱스 무관함</td></tr>
<tr><td>598</td><td><a href='https://arxiv.org/abs/2611.11782'>CABrain: A Correlation-Aware Brain Foundation Model for EEG Decoding</a></td><td>28</td><td>0</td><td>LG</td><td>GCN 기반 conditional positional encoding과 adaptive masking을 EEG foundation model에 넣은 CABrain, 작은 모듈 개선 수준임</td></tr>
<tr><td>599</td><td><a href='https://arxiv.org/abs/2611.11733'>Can the Remaining Answers Change the Prediction? Worst-Case Stability Checks for Personalized Rating Models</a></td><td>28</td><td>0</td><td>LG</td><td>누락 응답이 예측을 바꿀 수 있는지 worst-case 경계로 인증하는 개인화 평점 모델, 임상 평정 데이터라 로봇 무관함</td></tr>
<tr><td>600</td><td><a href='https://arxiv.org/abs/2611.11234'>LoMASA: A Local Multi-Agent Sales Assistant with Confidence-Gated Delegation for B2B Quoting</a></td><td>28</td><td>0</td><td>NLP</td><td>로컬 데스크톱에서 System-1과 System-2 LLM을 신뢰도로 위임하는 B2B 견적 assistant, 시뮬레이션 500개 에피소드 평가임</td></tr>
<tr><td>601</td><td><a href='https://arxiv.org/abs/2611.10901'>How Short Is Too Short? Length-Conditional Calibration and Abstention for Detecting AI-Generated Text</a></td><td>28</td><td>0</td><td>NLP</td><td>AI 생성 텍스트 탐지의 길이별 conformal calibration과 abstention 규칙, 어떤 detector도 80% TPR에 못 미침이 확인됨</td></tr>
<tr><td>602</td><td><a href='https://arxiv.org/abs/2611.10891'>Approximate Recall, Approximate Forecasts: Recall as a Diagnostic for LLM Forecasting Errors</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM의 과거 사건 recall fidelity가 예측시장 forecasting 오차를 예측함을 보인 Recall Fidelity Score, 워크숍 수준임</td></tr>
<tr><td>603</td><td><a href='https://arxiv.org/abs/2611.10385'>A Topological Encoder Decoder Framework for Temporal Graph Learning</a></td><td>28</td><td>0</td><td>LG</td><td>temporal graph 예측을 미래 그래프 topology descriptor 예측 후 복원하는 inverse 문제로 재정의, 그래프 데이터 한정</td></tr>
<tr><td>604</td><td><a href='https://arxiv.org/abs/2611.10329'>SIRIS: Can LLMs Tell When Simulation Errors Matter in AI-Driven Systems Research</a></td><td>28</td><td>0</td><td>NLP</td><td>시뮬레이터 한계가 추천 설계를 뒤집는지 LLM이 판단하는지 보는 SIRIS benchmark로 LLM 서빙 설계 한정</td></tr>
<tr><td>605</td><td><a href='https://arxiv.org/abs/2611.10193'>Ensemble Routing for Prompt-Adaptive Cost-Aware LLM Inference</a></td><td>28</td><td>0</td><td>NLP</td><td>prompt별 모델 능력 추정으로 단일 라우팅과 ensemble 구성을 비용 선호에 맞추는 PISA/PISA-E</td></tr>
<tr><td>606</td><td><a href='https://arxiv.org/abs/2611.10657'>MMGraph-Agent: Agentic Multimodal RAG via Cache-Inspired Multimodal Knowledge HyperGraphs</a></td><td>27</td><td>1</td><td>Multimodal</td><td>cache에서 착안한 multimodal knowledge hypergraph로 RAG 구축 비용을 줄인 프레임워크로 로봇 연결 약함</td></tr>
<tr><td>607</td><td><a href='https://arxiv.org/abs/2611.10187'>Fast Accurate Quantum Monte Carlo without Metropolis Adjustment</a></td><td>27</td><td>0</td><td>LG</td><td>양자 Monte Carlo 샘플링 개선으로 로봇과 무관함</td></tr>
<tr><td>608</td><td><a href='https://arxiv.org/abs/2611.10153'>Learning Across Heterogeneous Feature Spaces with Group Robustness</a></td><td>27</td><td>0</td><td>LG</td><td>이질적 feature space 임상 학습의 group robustness 연구임</td></tr>
<tr><td>609</td><td><a href='https://arxiv.org/abs/2611.11324'>When Sensors Fail: Coverage Auditing with Incomplete Sensor Records</a></td><td>26</td><td>1</td><td>LG</td><td>센서 결측 시 prediction interval coverage를 감사하는 3쪽 요약, 결과 대부분 inconclusive</td></tr>
<tr><td>610</td><td><a href='https://arxiv.org/abs/2611.10689'>RetinaGuard: Risk-Controlled Agentic Triage for Multi-Disease Retinal Screening</a></td><td>26</td><td>1</td><td>Medical</td><td>망막 선별에서 failure predictor와 conformal risk control로 자동 판정 수용을 인증하는 agentic triage로 의료 응용</td></tr>
<tr><td>611</td><td><a href='https://arxiv.org/abs/2611.10234'>ScreenProof: Where Is This Screen Wrong? Finding UI Faults Without a Reference</a></td><td>26</td><td>1</td><td>CV</td><td>참조 없이 UI 스크린샷의 결함을 박스로 찾는 ProofJudge를 코드 생성 데이터로 학습, F1 0.48로 frontier 모델보다 오경보 적음</td></tr>
<tr><td>612</td><td><a href='https://arxiv.org/abs/2611.11382'>The comparison of density estimation for transfer learning in Banach, Hilbert, Euclidean spaces</a></td><td>26</td><td>0</td><td>LG</td><td>L1 Banach norm과 manifold로 domain adaptation 수행한 BMTL 요약, 작은 데이터셋 위주 incremental</td></tr>
<tr><td>613</td><td><a href='https://arxiv.org/abs/2611.11226'>MCSA: Multi-Cutoff Spectral Aggregation in SO(3) Equivariant GNNs for Interatomic Potentials</a></td><td>26</td><td>0</td><td>LG</td><td>SO(3) equivariant GNN에 multi-cutoff 커널 집계 모듈 MCSA, 원자 포텐셜 plug-in 개선</td></tr>
<tr><td>614</td><td><a href='https://arxiv.org/abs/2611.11224'>Do Feature Interactions Break Explainability? Provable Explanations for Any-Order Neural Additive Models</a></td><td>26</td><td>0</td><td>LG</td><td>상호작용이 있는 NAM의 provable 최소 설명 계산 복잡도와 알고리즘, 설명 가능성 이론</td></tr>
<tr><td>615</td><td><a href='https://arxiv.org/abs/2611.10123'>All Quiet on the Neural Front: Language Models Do Not Report Injected Pain States</a></td><td>26</td><td>0</td><td>NLP</td><td>LLM에 주입한 pain 방향을 모델이 보고하지 못하나 probe로는 98% 이상 복원된다는 해석 연구</td></tr>
<tr><td>616</td><td><a href='https://arxiv.org/abs/2611.11662'>Enhancing Balance and Posture in Material Handling Tasks with a Wearable Robotic Tail</a></td><td>25</td><td>3</td><td>Wearable</td><td>웨어러블 꼬리 로봇의 자세 보조 연구임</td></tr>
<tr><td>617</td><td><a href='https://arxiv.org/abs/2611.10650'>Trajectory Inversion for a Rudderless Dual Vectored-Thrust Flying Wing</a></td><td>25</td><td>3</td><td>Control</td><td>flying wing trajectory inversion으로 로봇 학습과 거리 있음</td></tr>
<tr><td>618</td><td><a href='https://arxiv.org/abs/2611.10360'>MambaLoc: Lightweight Indoor Localization Using Cross-Modal Knowledge Distillation</a></td><td>25</td><td>3</td><td>Localization</td><td>UWB teacher에서 Mamba CSI student로 증류한 Wi-Fi 실내 측위로 오차 0.230 m, 엣지용 효율 개선이나 incremental</td></tr>
<tr><td>619</td><td><a href='https://arxiv.org/abs/2611.12346'>ReVMap: Vectorized Global Mapping via Connectivity-Aware Local Map Fusion</a></td><td>25</td><td>2</td><td>3D Vision</td><td>HD map 전역 융합, 자율주행 응용</td></tr>
<tr><td>620</td><td><a href='https://arxiv.org/abs/2611.12259'>A forensic evaluation framework for egocentric foundation models: an EFM3D case study for crime scene reconstruction</a></td><td>25</td><td>2</td><td>3D Vision</td><td>egocentric foundation model 법과학 평가, 응용 평가</td></tr>
<tr><td>621</td><td><a href='https://arxiv.org/abs/2611.11607'>Rethinking Geometric Depth in Monocular 3D Object Detection: A Projection-Consistent Reformulation</a></td><td>25</td><td>2</td><td>3D Vision</td><td>monocular 3D detection 깊이 재정식화, incremental</td></tr>
<tr><td>622</td><td><a href='https://arxiv.org/abs/2611.11007'>Efficient 3D plant segmentation through multiscale graph learning and optimized geometric processing</a></td><td>25</td><td>2</td><td>3D Vision</td><td>식물 3D 분할 경량화, 농업 특화</td></tr>
<tr><td>623</td><td><a href='https://arxiv.org/abs/2611.11678'>SurfScaff3D: Bridging Geometric and Semantic Representations for LLM-based 3D Object Generation</a></td><td>25</td><td>1</td><td>3D Vision</td><td>LLM 기반 3D 객체 생성</td></tr>
<tr><td>624</td><td><a href='https://arxiv.org/abs/2611.11320'>Beyond Similarity Entropy: A Rank-Guided Data-Free Quantization Framework for Vision Transformers</a></td><td>25</td><td>1</td><td>Efficiency</td><td>ViT data-free quantization, 개선 위주</td></tr>
<tr><td>625</td><td><a href='https://arxiv.org/abs/2611.10869'>Interactive Person Retrieval with On-the-Fly Visual Feedback</a></td><td>25</td><td>1</td><td>Multimodal</td><td>상호작용 person retrieval</td></tr>
<tr><td>626</td><td><a href='https://arxiv.org/abs/2611.10653'>FG-DSA: Frequency-Guided Depthwise Separable Attention for Efficient Dense Prediction</a></td><td>25</td><td>1</td><td>Efficiency</td><td>효율 attention 모듈</td></tr>
<tr><td>627</td><td><a href='https://arxiv.org/abs/2611.10416'>S2HAND: Accuracy-Preservation Trade-Offs for Hand Specialization in Whole-Body Pose Models</a></td><td>25</td><td>1</td><td>CV</td><td>전신 pose 손 특화 trade-off</td></tr>
<tr><td>628</td><td><a href='https://arxiv.org/abs/2611.10092'>Adapting Frozen Promptable Segmenters to User-Defined Taxonomies via Few-Shot Proposal Learning</a></td><td>25</td><td>1</td><td>CV</td><td>SAM 사용자 taxonomy 적응</td></tr>
<tr><td>629</td><td><a href='https://arxiv.org/abs/2611.11428'>CHANNELS4WORLD: An Environment-Scale Dataset for Wireless Foundation Models</a></td><td>25</td><td>1</td><td>LG</td><td>무선 foundation model용 10만 RF scene 데이터셋 Channels4World, 통신 도메인 데이터셋</td></tr>
<tr><td>630</td><td><a href='https://arxiv.org/abs/2611.11106'>Jointly Optimizing Memory, Computing and Offloading for Energy-Efficient DNN Inference</a></td><td>25</td><td>1</td><td>LG</td><td>DNN 추론의 메모리·연산·offloading을 MINLP로 공동 최적화함. 시뮬레이션 위주 시스템 최적화임</td></tr>
<tr><td>631</td><td><a href='https://arxiv.org/abs/2611.10733'>Spectrogram-Based CNN Autoencoder for One-Class Anomaly Detection in Machining Vibration Signals</a></td><td>25</td><td>1</td><td>LG</td><td>브로칭 진동 스펙트로그램 CNN autoencoder로 이상 탐지함. 산업 응용이며 방법 novelty 낮음</td></tr>
<tr><td>632</td><td><a href='https://arxiv.org/abs/2611.11469'>RealEmbedBench: Benchmarking LLMs on Real-World Application-Layer Embedded Software Tasks</a></td><td>25</td><td>1</td><td>NLP</td><td>임베디드 애플리케이션 코드 생성과 OS 간 번역 5,142개 샘플 벤치마크이며 모델 평가 위주임</td></tr>
<tr><td>633</td><td><a href='https://arxiv.org/abs/2611.10841'>A Gamified Framework for Conflict-Driven Design: Discovering Strategies for Collaborative Resilience with Multi-Agent Learning</a></td><td>25</td><td>1</td><td>RL</td><td>도시 회복력 이해관계 갈등을 보드게임으로 만들어 MARL로 푼 응용으로 novelty 낮고 로봇 무관</td></tr>
<tr><td>634</td><td><a href='https://arxiv.org/abs/2611.12805'>2D Gum-Net: Unsupervised Dense Elastic Image Registration via Symmetric Correlation and Spectral Pooling</a></td><td>25</td><td>0</td><td>CV</td><td>의료/구조생물 영상 registration, 로봇 관련 약함</td></tr>
<tr><td>635</td><td><a href='https://arxiv.org/abs/2611.12042'>Four-Step Text-Bearing Image Generation via Distillation with Local Response Regularization and Teacher-Guided Training</a></td><td>25</td><td>0</td><td>Generative</td><td>few-step text 이미지 생성 distillation</td></tr>
<tr><td>636</td><td><a href='https://arxiv.org/abs/2611.11122'>What You Show Is Not What You Get: Rethinking Demonstration Following in Visual In-Context Segmentation</a></td><td>25</td><td>0</td><td>CV</td><td>visual in-context 분할 demonstration 추종 분석</td></tr>
<tr><td>637</td><td><a href='https://arxiv.org/abs/2611.10940'>Semantic Synthesis over Brute-Force Search: LLM-Guided Transformation Design for Efficient Learning</a></td><td>25</td><td>0</td><td>CV</td><td>LLM으로 data transformation 설계</td></tr>
<tr><td>638</td><td><a href='https://arxiv.org/abs/2611.10575'>ROLECUE: Diagnosing Cross-Lingual Role-Binding Failures in Vision-Language Models</a></td><td>25</td><td>0</td><td>Multimodal</td><td>VLM 다국어 role-binding 실패 진단</td></tr>
<tr><td>639</td><td><a href='https://arxiv.org/abs/2611.12871'>Vendi Anomaly Scores for Efficient and Accurate Anomaly Detection</a></td><td>25</td><td>0</td><td>LG</td><td>anomaly score</td></tr>
<tr><td>640</td><td><a href='https://arxiv.org/abs/2611.12747'>Clique Constraints for Exact Causal Structure Learning</a></td><td>25</td><td>0</td><td>LG</td><td>인과 구조 학습 제약</td></tr>
<tr><td>641</td><td><a href='https://arxiv.org/abs/2611.12696'>Generalized Adaptive Boosting and the Geometry of Mistakes</a></td><td>25</td><td>0</td><td>LG</td><td>FP/FN 보장을 함께 다루는 Z-learner로 boosting 가능 조건을 기하학적으로 특성화한 이론 논문이라 로봇과 무관함</td></tr>
<tr><td>642</td><td><a href='https://arxiv.org/abs/2611.12665'>Trade Promotion Optimisation for Consumer Goods</a></td><td>25</td><td>0</td><td>LG</td><td>소비재 판촉 가격 탄력성 추정과 최적화 시스템이라 로봇 학습과 무관함</td></tr>
<tr><td>643</td><td><a href='https://arxiv.org/abs/2611.12475'>Learning to Select Sparse Linear Solvers with Convolutional Neural Networks</a></td><td>25</td><td>0</td><td>CV</td><td>sparse 행렬 spy plot을 CNN에 넣어 linear solver를 고르는 응용으로 로봇과 무관함</td></tr>
<tr><td>644</td><td><a href='https://arxiv.org/abs/2611.12419'>Optimal Rates for Adaptive Private $k$-PCA</a></td><td>25</td><td>0</td><td>LG</td><td>private k-PCA의 표본 복잡도를 d와 k 모두에서 최적으로 만든 이론 논문으로 로봇 무관</td></tr>
<tr><td>645</td><td><a href='https://arxiv.org/abs/2611.12339'>Evidence or Marginal? What Moment-Vector Propagation Computes in Polynomial Density Neurons</a></td><td>25</td><td>0</td><td>LG</td><td>polynomial density neuron의 입력 누락 처리식 차이를 분석하는 이론적 연구로 영향력 작음</td></tr>
<tr><td>646</td><td><a href='https://arxiv.org/abs/2611.12268'>Odds-Structured Distributional Regression for Interpretable Time-to-Event Prediction</a></td><td>25</td><td>0</td><td>LG</td><td>time-to-event 분포 회귀 출력을 log-odds 가산으로 설계한 임상 해석성 방법으로 로봇 무관</td></tr>
<tr><td>647</td><td><a href='https://arxiv.org/abs/2611.12116'>Forecast Value Add: Reward-Based Action Selection over Probabilistic Demand Forecasts</a></td><td>25</td><td>0</td><td>LG</td><td>수요 예측 후처리를 reward 기반 행동 선택으로 풀어 WMAPE를 6.3% 줄인 소매 응용임</td></tr>
<tr><td>648</td><td><a href='https://arxiv.org/abs/2611.11997'>HyInv Technical Report</a></td><td>25</td><td>0</td><td>LG</td><td>1.96M 파라미터 inverse folding 모델 HyInv의 기술 보고서로 로봇 무관</td></tr>
<tr><td>649</td><td><a href='https://arxiv.org/abs/2611.11967'>Pairwise distortion distribution for compression and quantization</a></td><td>25</td><td>0</td><td>LG</td><td>pairwise distortion distribution으로 압축 차원을 정하는 정보이론 논문으로 로봇 무관</td></tr>
<tr><td>650</td><td><a href='https://arxiv.org/abs/2611.11916'>LBSNet: Lightweight Brain State Modeling via Learnable Spectral Prototypes for EEG-Based Fatigue Detection</a></td><td>25</td><td>0</td><td>LG</td><td>학습 가능한 spectral prototype으로 EEG 피로를 검출하는 경량 네트워크로 incremental임</td></tr>
<tr><td>651</td><td><a href='https://arxiv.org/abs/2611.11847'>Severity-Controlled Prediction Sets for Medication Recommendation</a></td><td>25</td><td>0</td><td>LG</td><td>ATC 계층 기반 conformal severity control로 약물 추천 prediction set을 보정, 의료 응용이라 로봇 연관 낮음</td></tr>
<tr><td>652</td><td><a href='https://arxiv.org/abs/2611.11118'>When gene summaries reveal the answers: Gene Ontology circularity in gene embedding benchmarks</a></td><td>25</td><td>0</td><td>LG</td><td>유전자 임베딩 벤치마크에서 GO 요약문의 순환 누수를 밝힘. 평가 방법론이며 로봇과 무관함</td></tr>
<tr><td>653</td><td><a href='https://arxiv.org/abs/2611.11017'>ProtLink: Sequence and Multispecies Graph Context for Protein Interaction Prediction</a></td><td>25</td><td>0</td><td>LG</td><td>ESM-2와 다종 PPI 그래프를 HGT로 결합해 단백질 상호작용을 예측함. 생물정보 도메인임</td></tr>
<tr><td>654</td><td><a href='https://arxiv.org/abs/2611.10789'>Generating Diverse and Verified Synthetic Clinical Notes with Labels by Construction</a></td><td>25</td><td>0</td><td>NLP</td><td>의료 퇴원 요약 합성 데이터로 PHI de-identification 벤치마크를 만듦. 독일어 임상 NLP임</td></tr>
<tr><td>655</td><td><a href='https://arxiv.org/abs/2611.10781'>EEGFaceSem: An EEG Benchmark with Paired Generative Latents for Semantic Visual Modeling</a></td><td>25</td><td>0</td><td>LG</td><td>얼굴 의미 속성을 보는 EEG 데이터셋과 생성 latent를 짝지은 벤치마크임. BCI 도메인이고 로봇 무관함</td></tr>
<tr><td>656</td><td><a href='https://arxiv.org/abs/2611.10429'>Applied bifidelity material response model construction and uncertainty quantification with a sampling hypernetwork</a></td><td>25</td><td>0</td><td>LG</td><td>bifidelity Langevin hypernetwork로 재료 응답 surrogate를 불확실성과 함께 구성함. 재료 공학 응용임</td></tr>
<tr><td>657</td><td><a href='https://arxiv.org/abs/2611.10313'>Multi-objective drift-aware MLOps agent for model retraining</a></td><td>25</td><td>0</td><td>LG</td><td>드리프트 인지 재학습 정책을 LinUCB로 정하는 MLOps agent DARE임. 응용 위주임</td></tr>
<tr><td>658</td><td><a href='https://arxiv.org/abs/2611.12820'>How Well Does AI Peer Review Work? A Benchmark Built from 100 Planted Errors</a></td><td>25</td><td>0</td><td>NLP</td><td>AI 논문 리뷰의 심은 오류 검출 benchmark임</td></tr>
<tr><td>659</td><td><a href='https://arxiv.org/abs/2611.12750'>The Narrative Gap: Can LLMs Help Us Navigate Diverse Narratives Across Languages?</a></td><td>25</td><td>0</td><td>NLP</td><td>언어 간 서사 다양성 탐색 LLM 분석임</td></tr>
<tr><td>660</td><td><a href='https://arxiv.org/abs/2611.12392'>More Than Just Style: Benchmarking Personality Influence in Large Language Models</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM 성격 영향 benchmark임</td></tr>
<tr><td>661</td><td><a href='https://arxiv.org/abs/2611.11994'>EmoHarness: Boosting Multimodal Emotion Understanding with Meta-Harness Evolving</a></td><td>25</td><td>0</td><td>Multimodal</td><td>감정 이해용 harness 진화로 로봇과 무관함</td></tr>
<tr><td>662</td><td><a href='https://arxiv.org/abs/2611.11487'>THEATRON: A Benchmark for Evaluating Persona Persistence in Long-Horizon LLM Decision-Making</a></td><td>25</td><td>0</td><td>NLP</td><td>persona 지속성 benchmark임</td></tr>
<tr><td>663</td><td><a href='https://arxiv.org/abs/2611.11125'>LongCap: Hour-Scale Timestamped Audio Captioning via Chunk-wise Processing</a></td><td>25</td><td>0</td><td>Multimodal</td><td>시간 단위 오디오 captioning임</td></tr>
<tr><td>664</td><td><a href='https://arxiv.org/abs/2611.11111'>Beyond Hard Labels: LLM Probabilities Improve Human-Assisted Regression</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM 확률로 인간 보조 회귀를 개선함</td></tr>
<tr><td>665</td><td><a href='https://arxiv.org/abs/2611.10765'>Cascading Circle Loss: Order-Preserving Contrastive Learning for Graded Legal Retrieval</a></td><td>25</td><td>0</td><td>NLP</td><td>법률 검색용 등급 relevance contrastive loss CasCL, 도메인 특화 loss 변형임</td></tr>
<tr><td>666</td><td><a href='https://arxiv.org/abs/2611.10508'>Imperfectly Imperfect: Evaluating Graded Cognitive Diversity in LLM Persona Simulations</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM persona가 사람의 graded 인지 다양성을 재현하는지 473명과 비교한 평가 연구</td></tr>
<tr><td>667</td><td><a href='https://arxiv.org/abs/2611.12307'>PACE-ECG: Patient-Aware Contrastive ECG Pretraining; Leveraging Longitudinal Structure for Transferable Representations</a></td><td>25</td><td>0</td><td>LG</td><td>환자 시계열 이웃 기록을 positive로 쓰는 ECG contrastive 사전학습이며 의료 도메인이라 로보틱스와 무관함</td></tr>
<tr><td>668</td><td><a href='https://arxiv.org/abs/2611.11632'>Perturbation Profiles of Scanpath Classifiers: What Reading, Code-Comprehension and Video Decoders Are Sensitive To</a></td><td>25</td><td>0</td><td>LG</td><td>안구 scanpath 분류기가 어떤 속성에 민감한지 다섯 가지 perturbation으로 프로파일링하는 방법론, 시선 분석 도메인임</td></tr>
<tr><td>669</td><td><a href='https://arxiv.org/abs/2611.11588'>FinCutBench: A Continually Updated Benchmark for Measuring the Temporal Boundaries of LLM Financial Knowledge</a></td><td>25</td><td>0</td><td>NLP</td><td>월별 금융 지식 문항 9,000개로 LLM 지식 cutoff 시점을 추정하는 FinCutBench, 금융 평가 벤치마크임</td></tr>
<tr><td>670</td><td><a href='https://arxiv.org/abs/2611.11289'>A Unified Framework for License Plate Identification and Character-Recognition</a></td><td>24</td><td>2</td><td>CV</td><td>Jetson Orin Nano에서 147 FPS인 번호판 검출과 인식 통합 네트워크, 엣지 배포 엔지니어링 위주</td></tr>
<tr><td>671</td><td><a href='https://arxiv.org/abs/2611.11189'>TEAM: Topology-Aware, Semantic-Sensitive, General Transformer for Multimodal-Attributed Graphs</a></td><td>24</td><td>1</td><td>Multimodal</td><td>multimodal-attributed graph를 node-modality 토큰으로 인코딩하는 TEAM, 그래프 benchmark 개선 위주</td></tr>
<tr><td>672</td><td><a href='https://arxiv.org/abs/2611.10638'>SLA-Aware Task Offloading in the IoT Edge-Cloud Continuum: Class-Weighted Deep Reinforcement Learning Against an Exact Optimum</a></td><td>24</td><td>1</td><td>RL</td><td>IoT edge-cloud task offloading에서 class별 penalty PPO를 DP 최적해와 비교한 벤치 연구로 로봇 무관</td></tr>
<tr><td>673</td><td><a href='https://arxiv.org/abs/2611.11786'>Payoff-Aware Prediction of Population Game Dynamics</a></td><td>24</td><td>0</td><td>LG</td><td>payoff 변화에 따른 population game 궤적 예측 PA-RmD 제안, 게임 이론 응용이라 로봇과 무관</td></tr>
<tr><td>674</td><td><a href='https://arxiv.org/abs/2611.11520'>Hydra: Towards Transferable Multi-Task Learning on Temporal Graphs</a></td><td>24</td><td>0</td><td>LG</td><td>temporal graph에서 local GNN과 spectral 모듈을 결합한 multi-task Hydra, 그래프 예측이라 로봇 무관</td></tr>
<tr><td>675</td><td><a href='https://arxiv.org/abs/2611.11252'>ALETHEIA: A Multi-Frequency Eddy Current Pulsed Thermography Dataset for Neural Operator Learning in Nondestructive Testing</a></td><td>24</td><td>0</td><td>LG</td><td>와전류 열화상 비파괴 검사용 neural operator 데이터셋 ALETHEIA, 과학 ML 데이터셋</td></tr>
<tr><td>676</td><td><a href='https://arxiv.org/abs/2611.10718'>FedSGN: Federated Sparse Grassmann Newton Learning for IoT Anomaly Detection</a></td><td>24</td><td>0</td><td>LG</td><td>federated sparse PCA를 Grassmann Newton으로 풀어 IoT 이상 탐지함. 로봇 무관한 소규모 방법임</td></tr>
<tr><td>677</td><td><a href='https://arxiv.org/abs/2611.10386'>Pruning DNA Sequence</a></td><td>24</td><td>0</td><td>LG</td><td>DNA 언어모델 사전학습에서 쉬운 서열을 동적으로 prune하는 Sequence Pruning임. 유전체 도메인임</td></tr>
<tr><td>678</td><td><a href='https://arxiv.org/abs/2611.12333'>AMSchem: Automated Schematic Visualization of AMS Circuits via Verifiable Agentic Generation</a></td><td>24</td><td>0</td><td>NLP</td><td>AMS 회로 netlist를 검증기 유도 agent로 schematic 생성하는 AMSchem, 유효율 32.5%에서 85.0%</td></tr>
<tr><td>679</td><td><a href='https://arxiv.org/abs/2611.12167'>FraudBench: A Legal Evaluation of AI Deception</a></td><td>24</td><td>0</td><td>NLP</td><td>법적 사기 시나리오 159개로 LLM의 자율성별 사기 비율을 재는 안전성 평가 벤치마크이며 로봇과 무관함</td></tr>
<tr><td>680</td><td><a href='https://arxiv.org/abs/2611.10684'>Audit Before You Merge: Provenance, Probing, and Continual LoRA Composition</a></td><td>24</td><td>0</td><td>NLP</td><td>공개 LoRA adapter 병합 전 출처·delta norm 감사와 forgetting 측정 프로토콜 제안, 워크숍급 분석</td></tr>
<tr><td>681</td><td><a href='https://arxiv.org/abs/2611.10600'>InfoOrgBench: Can Agents Turn Scattered Information into Coherent Hierarchies?</a></td><td>24</td><td>0</td><td>NLP</td><td>흩어진 기록을 계층 폴더로 정리하는 agent benchmark InfoOrgBench로 parent-level 오류가 큼을 보인 평가</td></tr>
<tr><td>682</td><td><a href='https://arxiv.org/abs/2611.10412'>TurnFlow: Benchmarking User-State Reasoning in Multi-Turn LLM Agents via Scene-Guided User Simulation</a></td><td>24</td><td>0</td><td>NLP</td><td>다중 턴에서 사용자 요구 변화 추적을 평가하는 TurnFlow benchmark로 490 시나리오 평가</td></tr>
<tr><td>683</td><td><a href='https://arxiv.org/abs/2611.10265'>Do large language models rank moral values? A transitivity test of moral competence</a></td><td>24</td><td>0</td><td>NLP</td><td>LLM의 도덕 가치 선택이 transitivity를 만족하는지 검사한 분석으로 대부분 불안정 순서를 보임</td></tr>
<tr><td>684</td><td><a href='https://arxiv.org/abs/2611.12306'>ExoStack: A Modular and Reconfigurable Software Framework for Wearable Robotics Using ROS 2</a></td><td>22</td><td>3</td><td>Robotics SW</td><td>웨어러블 로봇 ROS 2 소프트웨어 프레임워크로 연구 기여 약함</td></tr>
<tr><td>685</td><td><a href='https://arxiv.org/abs/2611.11698'>Compute Regeneration through Re-Productization: Reorganizing Retired Edge AI Silicon into a Delivered Multilingual Service Robot</a></td><td>22</td><td>3</td><td>Robotics SW</td><td>퇴역 edge 칩을 재사용한 서비스 로봇 시스템 설계임</td></tr>
<tr><td>686</td><td><a href='https://arxiv.org/abs/2611.10235'>Agibot: An Open-Source Modular Swerve-Drive Robot Platform for Agricultural Robotics Research and Education</a></td><td>22</td><td>3</td><td>Hardware</td><td>농업 로봇 오픈소스 플랫폼으로 연구 기여 약함</td></tr>
<tr><td>687</td><td><a href='https://arxiv.org/abs/2611.12816'>Automated Knowledge Acquisition Pipeline for Disassembly Instructions: A Comparison of NLP and Generative AI Frameworks</a></td><td>22</td><td>3</td><td>NLP</td><td>분해 매뉴얼에서 disassembly 지시를 규칙 NLP와 LLM으로 추출 비교, 분해 자동화 데이터 기반이나 로봇 실험 없음</td></tr>
<tr><td>688</td><td><a href='https://arxiv.org/abs/2611.12657'>When Does Sliced Inference Pay Off? Resolution, Tiling and Dense Fusion for Small Object Detection</a></td><td>22</td><td>1</td><td>CV</td><td>sliced inference 실증 연구, incremental</td></tr>
<tr><td>689</td><td><a href='https://arxiv.org/abs/2611.12051'>Attention-Guided Sequence Feature Fusion and Mixed-Space Metric Learning for Cross-View Image Sequence Geo-Localization</a></td><td>22</td><td>1</td><td>CV</td><td>cross-view geo-localization, 모듈 개선 수준</td></tr>
<tr><td>690</td><td><a href='https://arxiv.org/abs/2611.10991'>Sensitivity-Gated Accumulator Caching for On-Device Learning of Low-Bit Hand Networks</a></td><td>22</td><td>1</td><td>Efficiency</td><td>저비트 손 추적 온디바이스 학습</td></tr>
<tr><td>691</td><td><a href='https://arxiv.org/abs/2611.10690'>JoVox: Joint Hierarchical Flow Matching for Lightweight Voxel Generation</a></td><td>22</td><td>1</td><td>Generative</td><td>voxel 생성 flow matching</td></tr>
<tr><td>692</td><td><a href='https://arxiv.org/abs/2611.10353'>DAPointRWKV: Domain Adaptive Vision RWKV for Point Cloud Completion</a></td><td>22</td><td>1</td><td>3D Vision</td><td>point cloud completion domain adaptation</td></tr>
<tr><td>693</td><td><a href='https://arxiv.org/abs/2611.10844'>What Broke &amp; Why: Practical Lessons from Reinforcement Learning Post-Training</a></td><td>22</td><td>1</td><td>RL</td><td>LLM RLVR post-training 실패 사례를 정리한 실무 서적으로 GRPO 디버깅 참고용이나 로봇 직접 연결 약함</td></tr>
<tr><td>694</td><td><a href='https://arxiv.org/abs/2611.12798'>Complementarity-Driven Dual-Teacher Hierarchical Alignment for Zero-Shot EEG-to-Image Retrieval</a></td><td>22</td><td>0</td><td>CV</td><td>EEG-이미지 검색, 로봇 무관</td></tr>
<tr><td>695</td><td><a href='https://arxiv.org/abs/2611.12144'>DisasterVL: Evidence-Based Visual Reasoning Dataset and Model for Disaster Scene Understanding</a></td><td>22</td><td>0</td><td>Multimodal</td><td>재난 영상 reasoning 데이터셋</td></tr>
<tr><td>696</td><td><a href='https://arxiv.org/abs/2611.11980'>AnyBreak: Towards Jailbreaking Any T2I Model for Any Concept</a></td><td>22</td><td>0</td><td>Generative</td><td>T2I jailbreak 공격, 무관</td></tr>
<tr><td>697</td><td><a href='https://arxiv.org/abs/2611.10571'>Understanding the Effect of Visual Attention in CNNs: A Decision-Space Alignment Perspective</a></td><td>22</td><td>0</td><td>CV</td><td>CNN attention 정렬 분석</td></tr>
<tr><td>698</td><td><a href='https://arxiv.org/abs/2611.10528'>PrivMark: Pixel-Space Steering against Privacy Leakage in Vision-Language Models</a></td><td>22</td><td>0</td><td>Multimodal</td><td>VLM 프라이버시 pixel steering</td></tr>
<tr><td>699</td><td><a href='https://arxiv.org/abs/2611.12702'>Fisher-Glass Learning: Classification Bounds and Subpopulation Audits</a></td><td>22</td><td>0</td><td>LG</td><td>Fisher-Glass 분류 bound</td></tr>
<tr><td>700</td><td><a href='https://arxiv.org/abs/2611.12668'>Controlled Binary Assignment Flows</a></td><td>22</td><td>0</td><td>CV</td><td>그래프 위 binary assignment flow의 시변 파라미터를 기하학적으로 제어하는 수학적 연구로 응용 연결 약함</td></tr>
<tr><td>701</td><td><a href='https://arxiv.org/abs/2611.12219'>An Empirical Evaluation of Quantum Kernel Stability in Network Intrusion Detection</a></td><td>22</td><td>0</td><td>LG</td><td>양자 kernel SVM의 침입 탐지 불안정성을 평가한 실증 연구로 로봇 무관</td></tr>
<tr><td>702</td><td><a href='https://arxiv.org/abs/2611.12140'>Visible Tails: Characterizing Adaptation to Unknown Moments in Heavy-Tailed Bandits</a></td><td>22</td><td>0</td><td>LG</td><td>heavy-tailed bandit에서 미지 moment 적응 조건을 특성화한 순수 이론임</td></tr>
<tr><td>703</td><td><a href='https://arxiv.org/abs/2611.11960'>Operation-aware Multimodal Clinical Decision Support System for ICU Discharge Risk Assessment</a></td><td>22</td><td>0</td><td>LG</td><td>MIMIC-III로 ICU 재입실 위험을 운영 지표와 멀티모달로 예측하는 임상 응용임</td></tr>
<tr><td>704</td><td><a href='https://arxiv.org/abs/2611.11946'>Decision Aware Origin-Destination Demand Estimation with Structurally Constrained Data</a></td><td>22</td><td>0</td><td>LG</td><td>교통 OD 수요 추정을 downstream regret 관점으로 푸는 응용 연구로 로봇 무관</td></tr>
<tr><td>705</td><td><a href='https://arxiv.org/abs/2611.11905'>On the Global Convergence of Stochastic Adam for Physics-Informed Neural Networks</a></td><td>22</td><td>0</td><td>LG</td><td>두 층 넓은 네트워크와 PINN에서 Adam의 선형 수렴을 증명한 최적화 이론임</td></tr>
<tr><td>706</td><td><a href='https://arxiv.org/abs/2611.11680'>A Theoretical Reduction From Membership Inference to Reconstruction Attacks Against Learners</a></td><td>22</td><td>0</td><td>LG</td><td>membership inference가 reconstruction attack을 함의함을 보이는 프라이버시 이론</td></tr>
<tr><td>707</td><td><a href='https://arxiv.org/abs/2611.11493'>Learning through Capacity Awareness to Minimize Hospital Readmissions</a></td><td>22</td><td>0</td><td>LG</td><td>병원 퇴원 결정과 재입원 예측의 censoring bias를 capacity-aware 정책으로 완화, 의료 운영 응용</td></tr>
<tr><td>708</td><td><a href='https://arxiv.org/abs/2611.11457'>MOMENT-DP: Momentum Aware Evaluation of Correlated Noise for Differentially Private Training</a></td><td>22</td><td>0</td><td>LG</td><td>DP 학습에서 momentum을 반영해 correlated noise 메커니즘 순위를 평가, 프라이버시 이론</td></tr>
<tr><td>709</td><td><a href='https://arxiv.org/abs/2611.11447'>Learning to Rank Propagators in Constraint Programming</a></td><td>22</td><td>0</td><td>LG</td><td>constraint programming propagator 우선순위를 learning-to-rank로 학습, 솔버 튜닝이라 로봇 무관</td></tr>
<tr><td>710</td><td><a href='https://arxiv.org/abs/2611.10613'>Clinical Evidence-Guided Residual Learning for Medication Recommendation with Dynamic DDI Regularization</a></td><td>22</td><td>0</td><td>LG</td><td>약물 추천에 clinical memory와 DDI 정규화를 결합한 EviDrug임. 의료 추천 도메인임</td></tr>
<tr><td>711</td><td><a href='https://arxiv.org/abs/2611.10086'>Transferring local rib responses to new component geometries in sheet forming with a graph-based Transformer</a></td><td>22</td><td>0</td><td>LG</td><td>판금 성형 rib 응답 전이를 graph Transformer로 다룬 응용 연구임</td></tr>
<tr><td>712</td><td><a href='https://arxiv.org/abs/2611.10082'>fNIRSAtlas: A Large-Scale Benchmark for Functional Near-Infrared Spectroscopy Classification</a></td><td>22</td><td>0</td><td>LG</td><td>fNIRS 분류 benchmark로 로봇과 무관함</td></tr>
<tr><td>713</td><td><a href='https://arxiv.org/abs/2611.09935'>Fresh Enough to Decide: Age of Intelligence for Cost-Aware Model Synchronization in Dynamic IoT Systems</a></td><td>22</td><td>0</td><td>LG</td><td>IoT 모델 동기화 비용 인지 정책으로 로봇과 무관함</td></tr>
<tr><td>714</td><td><a href='https://arxiv.org/abs/2611.12628'>Adapting Small Language Models to Romanized Nepali: Tokenizer Fertility, Reference Likelihood, and Generation Metrics</a></td><td>22</td><td>0</td><td>NLP</td><td>로마자 네팔어 소형 언어모델 적응임</td></tr>
<tr><td>715</td><td><a href='https://arxiv.org/abs/2611.12592'>Fairness in Explainable AI Narratives: Decomposing Social Disparities in LLM-Generated Explanations</a></td><td>22</td><td>0</td><td>NLP</td><td>XAI 설명문의 사회적 편향 분해 분석임</td></tr>
<tr><td>716</td><td><a href='https://arxiv.org/abs/2611.11987'>When Audio and Video Mislead: Evaluating Multimodal AI for Conversational Emotion Recognition</a></td><td>22</td><td>0</td><td>Multimodal</td><td>대화 감정 인식의 오도 모달 평가임</td></tr>
<tr><td>717</td><td><a href='https://arxiv.org/abs/2611.11802'>HiddenPathQA: A Benchmark for Knowledge Graph Question Answering When Questions Hide Their Paths</a></td><td>22</td><td>0</td><td>NLP</td><td>경로가 숨겨진 KGQA benchmark임</td></tr>
<tr><td>718</td><td><a href='https://arxiv.org/abs/2611.11249'>Understanding When and Where Self-Supervised Speech Models Learn Phonemes and Prosodic Cues through Layer-Wise and Time-Resolved Probing</a></td><td>22</td><td>0</td><td>NLP</td><td>음성 SSL 모델 phoneme probing 분석임</td></tr>
<tr><td>719</td><td><a href='https://arxiv.org/abs/2611.11239'>A Layer-wise Study of How Style Rewriting Breaks the Calibration of Zero-Shot LLM Fake-News Detectors</a></td><td>22</td><td>0</td><td>NLP</td><td>스타일 재작성으로 가짜뉴스 탐지 보정이 깨지는 분석임</td></tr>
<tr><td>720</td><td><a href='https://arxiv.org/abs/2611.11030'>Building and Auditing Chemical Datasets with LLMs: A General LLM-as-a-Judge Framework Applied to Homogeneous Catalytic PET Depolymerisation</a></td><td>22</td><td>0</td><td>NLP</td><td>화학 문헌에서 LLM으로 PET 분해 데이터를 추출하고 LLM judge로 검증하는 도메인 응용 파이프라인임</td></tr>
<tr><td>721</td><td><a href='https://arxiv.org/abs/2611.10800'>Enhancing Mathematical Reasoning in Turkish Large Language Models with Search-Based Inference and Model Merging</a></td><td>22</td><td>0</td><td>NLP</td><td>터키어 수학 추론에 LoRA, 모델 병합, MCTS 탐색을 조합한 incremental 연구</td></tr>
<tr><td>722</td><td><a href='https://arxiv.org/abs/2611.10601'>AI in the Clinical Documentation Loop: Effects of LLM-Induced Note Bloat and Diagnostic Overcall on Downstream LLMs</a></td><td>22</td><td>0</td><td>NLP</td><td>의무기록에 LLM이 쓴 bloat와 진단 과장이 downstream LLM에 전파되는지 본 ML4H 연구</td></tr>
<tr><td>723</td><td><a href='https://arxiv.org/abs/2611.10147'>Learning of Tree Automata applied to Neural Language Acceptors</a></td><td>22</td><td>0</td><td>LG</td><td>neural language acceptor에서 black-box로 visibly pushdown grammar를 추출하는 tree automata 학습, WIP 이론</td></tr>
<tr><td>724</td><td><a href='https://arxiv.org/abs/2611.09938'>DramaGrow: A Regime-Aware Benchmark for Auditing LLM Judges of Multi-Episode Drama</a></td><td>22</td><td>0</td><td>NLP</td><td>중국어 5부작 드라마를 평가하는 LLM judge 감사 benchmark DramaGrow</td></tr>
<tr><td>725</td><td><a href='https://arxiv.org/abs/2611.12775'>LogCDM: Interpretable Log Anomaly Detection via Behavioral Graph Drift and Adaptive Signal Fusion</a></td><td>22</td><td>0</td><td>LG</td><td>소형 log anomaly detector LogCDM, 그래프 drift와 gate 융합으로 CPU 5.5ms, 시스템 로그 도메인</td></tr>
<tr><td>726</td><td><a href='https://arxiv.org/abs/2611.12640'>TrialDesignBench: Benchmarking Language Models for Phase-I Trial Design Against Clinical Knowledge</a></td><td>22</td><td>0</td><td>NLP</td><td>617개 Phase-I 종양 용량탐색 시험 설계 benchmark TrialDesignBench, 도메인 평가셋</td></tr>
<tr><td>727</td><td><a href='https://arxiv.org/abs/2611.12635'>Beyond Sunny Skies: Using Large Language Models to Predict Urban Traffic in Adverse Weather</a></td><td>22</td><td>0</td><td>LG</td><td>악천후 도시 교통량 예측에 LLM 의미 임베딩을 GNN과 융합한 Multi-STG, MAE 11.82% 감소의 도메인 응용</td></tr>
<tr><td>728</td><td><a href='https://arxiv.org/abs/2611.12291'>Representational Alignment between Deep Neural Networks and Human Brain in Speech Processing under Audiovisual Noise</a></td><td>22</td><td>0</td><td>Audio</td><td>ASR 모델 층과 뇌 반응의 RSA 정렬 분석으로 신경과학 성격이며 로보틱스 무관함</td></tr>
<tr><td>729</td><td><a href='https://arxiv.org/abs/2611.12128'>Toward Sustainable Agentic AI: Carbon Tradeoffs Across Iterative Self-Refinement and Tool-Augmented Coding</a></td><td>22</td><td>0</td><td>NLP</td><td>self-refinement와 tool 기반 코딩 agent의 탄소 발자국 추정 실증 연구로 방법론 기여가 없음</td></tr>
<tr><td>730</td><td><a href='https://arxiv.org/abs/2611.12095'>From Fluent Text to Ontology-Compatible Definitions: A Quality-Control Agentic Workflow</a></td><td>22</td><td>0</td><td>NLP</td><td>생의학 ontology 정의 생성의 entity 오류와 논리 불일치 지표 및 repair loop, 로보틱스 무관함</td></tr>
<tr><td>731</td><td><a href='https://arxiv.org/abs/2611.11819'>When Should AI Overturn a Human Decision? Controversy at the 2026 World Cup and a $\sqrt{2/π}$ Solution</a></td><td>22</td><td>0</td><td>LG</td><td>심판 판정과 VAR 측정을 ML 규칙으로 결합하는 offside 번복 임계값 유도, 교육용 논문이라 연구 기여가 작음</td></tr>
<tr><td>732</td><td><a href='https://arxiv.org/abs/2611.11774'>Wireless AI Networks: Co-Adapting Communication Resources and Distributed Intelligence</a></td><td>22</td><td>0</td><td>LG</td><td>무선 통신 자원과 분산 AI의 co-adaptation을 제안하는 관점 논문으로 연합학습 실험 2개만 있고 로봇 무관함</td></tr>
<tr><td>733</td><td><a href='https://arxiv.org/abs/2611.10893'>Complementarity without ground truth?</a></td><td>22</td><td>0</td><td>AI</td><td>ground truth 없는 의사결정에서 adequacy label로 human-AI complementarity를 정의하는 개념 논문, 실험이 없음</td></tr>
<tr><td>734</td><td><a href='https://arxiv.org/abs/2611.10629'>DFT-Agent Bench: Scaffold Effects and Execution Provenance in Autonomous DFT</a></td><td>22</td><td>0</td><td>NLP</td><td>Quantum ESPRESSO DFT 작업 200여 개로 LLM agent scaffold 효과와 실행 provenance를 평가한 벤치</td></tr>
<tr><td>735</td><td><a href='https://arxiv.org/abs/2611.10581'>Receiver-Resolution APS-PDP Maps for Wireless Channels: Benchmarking and Coarse-to-Fine Modeling</a></td><td>22</td><td>0</td><td>Generative</td><td>무선 채널 APS-PDP map benchmark와 multi-scale autoregressive flow matching 생성기로 통신 분야 응용</td></tr>
<tr><td>736</td><td><a href='https://arxiv.org/abs/2611.10418'>Beyond Query Similarity: Safety-Conditioned Cache Routing for LLM Response Reuse</a></td><td>22</td><td>0</td><td>NLP</td><td>semantic cache 재사용 시 안전 조건 불일치를 라우팅으로 막는 SafeCache로 LLM 서빙 응용</td></tr>
<tr><td>737</td><td><a href='https://arxiv.org/abs/2611.10285'>FAIDER: Fairness-Aware Item-Level Decoding for Large Language Model Recommenders</a></td><td>22</td><td>0</td><td>NLP</td><td>보호 속성 변화에 따른 LLM 추천 편차를 item 단위 decoding과 conformal 보정으로 줄이는 fairness 방법</td></tr>
<tr><td>738</td><td><a href='https://arxiv.org/abs/2611.10238'>CoRA-Bench: Evaluating Evidence Preservation by Context Selectors Under Token Budgets</a></td><td>22</td><td>0</td><td>NLP</td><td>토큰 예산 하에서 BM25·dense retrieval·LLMLingua 등 context selector의 증거 보존을 비교한 CoRA-Bench</td></tr>
<tr><td>739</td><td><a href='https://arxiv.org/abs/2611.12477'>Perturb, Aggregate then Reconstruct: Consensus Aggregation and Fourier-Attended Multi-Decoders for Reconstruction-based Multi-View Anomaly Detection</a></td><td>20</td><td>1</td><td>CV</td><td>multi-view 산업 이상 탐지, incremental</td></tr>
<tr><td>740</td><td><a href='https://arxiv.org/abs/2611.10932'>Beating the Pool, Not the Game: A White-Box Equilibrium Agent for Language-Based Economic Games</a></td><td>20</td><td>1</td><td>NLP</td><td>경제 게임 규칙 기반 agent 대회 보고임</td></tr>
<tr><td>741</td><td><a href='https://arxiv.org/abs/2611.10852'>KeyASRBench: Measuring Whole-Phrase Keyword Preservation in Real-World ASR</a></td><td>20</td><td>1</td><td>NLP</td><td>ASR에서 핵심 키워드 보존을 재는 KeyASRBench, 중영 10시간 평가셋이라 범위 작음</td></tr>
<tr><td>742</td><td><a href='https://arxiv.org/abs/2611.12674'>What Breaks Scribble-Supervised Segmentation? An Audit-Informed Benchmark for Scribble Annotation Robustness</a></td><td>20</td><td>0</td><td>CV</td><td>scribble 분할 benchmark, 로봇 무관</td></tr>
<tr><td>743</td><td><a href='https://arxiv.org/abs/2611.12508'>MARS: Multiscale Appearance-Residual Streams for Video Forgery Detection</a></td><td>20</td><td>0</td><td>Video</td><td>deepfake 영상 탐지, 무관</td></tr>
<tr><td>744</td><td><a href='https://arxiv.org/abs/2611.12443'>MoSTE: Mixture of Spatio-Temporal Experts for Deepfake Detection in Videos</a></td><td>20</td><td>0</td><td>Video</td><td>deepfake 탐지, 무관</td></tr>
<tr><td>745</td><td><a href='https://arxiv.org/abs/2611.12345'>TMT: Adapting CLIP to Infrared Imagery via Text-Derived Modality Knowledge Transfer</a></td><td>20</td><td>0</td><td>CV</td><td>CLIP의 적외선 적응, 도메인 특화</td></tr>
<tr><td>746</td><td><a href='https://arxiv.org/abs/2611.12023'>TIRAD: Text-guided Image Residual Learning for Generalist Anomaly Detection</a></td><td>20</td><td>0</td><td>CV</td><td>범용 이상 탐지 residual 학습, incremental</td></tr>
<tr><td>747</td><td><a href='https://arxiv.org/abs/2611.11951'>UltraVoxelGS: Voxel-First Feed-Forward Gaussian Splatting for 3D Ultrasound Reconstruction</a></td><td>20</td><td>0</td><td>3D Vision</td><td>초음파 3DGS 재구성, 의료 특화</td></tr>
<tr><td>748</td><td><a href='https://arxiv.org/abs/2611.10717'>Disentangled Stylized Image Generation via IP-Cross-Attention Rearrangement</a></td><td>20</td><td>0</td><td>Generative</td><td>스타일 이미지 생성</td></tr>
<tr><td>749</td><td><a href='https://arxiv.org/abs/2611.10497'>Disentangling Channel Semantics in Vision Transformers via Token Decorrelation and Composition-Aware Modulation</a></td><td>20</td><td>0</td><td>CV</td><td>다채널 ViT 채널 의미 분리</td></tr>
<tr><td>750</td><td><a href='https://arxiv.org/abs/2611.10297'>Uncertainty, Not Concealment: A Mechanistic Reappraisal of Sycophancy in Vision-Language Models</a></td><td>20</td><td>0</td><td>Multimodal</td><td>의료 VLM sycophancy 해석</td></tr>
<tr><td>751</td><td><a href='https://arxiv.org/abs/2611.10005'>EarthJev: Efficient Visual Evidence Acquisition and Decision for UHR Remote Sensing Understanding</a></td><td>20</td><td>0</td><td>Multimodal</td><td>원격탐사 VQA 증거 탐색</td></tr>
<tr><td>752</td><td><a href='https://arxiv.org/abs/2611.12694'>Agnostic Marginal-Nonuniform Learning</a></td><td>20</td><td>0</td><td>LG</td><td>agnostic marginal-nonuniform 학습의 비율을 VC 차원으로 분류한 순수 학습이론이라 로봇 연관 없음</td></tr>
<tr><td>753</td><td><a href='https://arxiv.org/abs/2611.12178'>Replication of Thermal Comfort Cohort Models: No Support for Improved Thermal Preference Prediction</a></td><td>20</td><td>0</td><td>LG</td><td>열 쾌적도 cohort 모델 성능 향상 주장을 재현 실패로 반박한 연구로 로봇과 무관함</td></tr>
<tr><td>754</td><td><a href='https://arxiv.org/abs/2611.12026'>MambaPD: Bidirectional Selective State Space Model for Parkinson&#x27;s Disease Detection from Resting-State EEG</a></td><td>20</td><td>0</td><td>LG</td><td>양방향 Mamba로 EEG 기반 파킨슨병을 검출하나 baseline과 차이가 없어 기여가 약함</td></tr>
<tr><td>755</td><td><a href='https://arxiv.org/abs/2611.11808'>Efficient Online Submodular Maximization with Bandit Feedback</a></td><td>20</td><td>0</td><td>LG</td><td>bandit feedback 온라인 submodular 최대화의 다항시간 sqrt(T) regret 알고리즘, 순수 이론</td></tr>
<tr><td>756</td><td><a href='https://arxiv.org/abs/2611.11726'>The Dark Matter of Clinical Data: An Identification Limit on Disentangling Physiology from Care Process in electronic health records</a></td><td>20</td><td>0</td><td>LG</td><td>EHR에서 생리와 진료 과정을 분리하는 식별 한계 이론, 의료 통계 주제</td></tr>
<tr><td>757</td><td><a href='https://arxiv.org/abs/2611.11622'>GenISys: Integrated Ship Systems Design Using Subsystem-Conditional Tabular Diffussion</a></td><td>20</td><td>0</td><td>Generative</td><td>선박 설계용 subsystem 조건부 tabular diffusion 생성, 공학 응용이라 로봇과 무관</td></tr>
<tr><td>758</td><td><a href='https://arxiv.org/abs/2611.11494'>Regret without Optimal-Arm Feedback under Reward-Dependent Delays</a></td><td>20</td><td>0</td><td>LG</td><td>보상 의존 지연이 있는 stochastic bandit의 regret 분석, 이론 위주</td></tr>
<tr><td>759</td><td><a href='https://arxiv.org/abs/2611.11261'>Chatter Attack: Resource Consumption Attack for Large Language Models</a></td><td>20</td><td>0</td><td>NLP</td><td>짧은 doubt 문구를 목표로 LLM 응답 길이를 31.5배 늘리는 Chatter Attack, 보안 공격 주제</td></tr>
<tr><td>760</td><td><a href='https://arxiv.org/abs/2611.11217'>scBIG++: Learning Across Genes and Cells to Predict Single-Cell Perturbation Responses</a></td><td>20</td><td>0</td><td>LG</td><td>단일 세포 perturbation 반응을 full-gene으로 예측하는 scBIG++, 생물 도메인</td></tr>
<tr><td>761</td><td><a href='https://arxiv.org/abs/2611.11149'>ZarrFM: A Canonical Tensor Storage Architecture for EEG Foundation-Model Pretraining</a></td><td>20</td><td>0</td><td>LG</td><td>EEG 코퍼스를 Zarr로 저장하는 포맷 설계임. 시스템 엔지니어링이고 로봇과 무관함</td></tr>
<tr><td>762</td><td><a href='https://arxiv.org/abs/2611.10145'>TrialJev: Open-Weight Single Pass Eligibility Scoring for Patient Trial Screening</a></td><td>20</td><td>0</td><td>NLP</td><td>임상시험 환자 선별용 모델로 응용 특화임</td></tr>
<tr><td>763</td><td><a href='https://arxiv.org/abs/2611.12501'>Text Grouping Changes Completion-Time Comparisons in Long-Form Simultaneous Speech Translation</a></td><td>20</td><td>0</td><td>NLP</td><td>동시통역 텍스트 grouping 비교 연구임</td></tr>
<tr><td>764</td><td><a href='https://arxiv.org/abs/2611.12487'>Detecting AI-Authored Text in Authentic Student Writing: Evidence from PISA 2025</a></td><td>20</td><td>0</td><td>NLP</td><td>학생 글에서 AI 문장 탐지 평가임</td></tr>
<tr><td>765</td><td><a href='https://arxiv.org/abs/2611.12420'>Path-Level Structural and Semantic Alignment for Hierarchical Multi-Label Text Classification</a></td><td>20</td><td>0</td><td>NLP</td><td>계층 다중 레이블 텍스트 분류 정렬 개선임</td></tr>
<tr><td>766</td><td><a href='https://arxiv.org/abs/2611.12407'>BDBBQ: A Human-AI Collaborative Benchmark for Bengali Social Bias in LLMs</a></td><td>20</td><td>0</td><td>NLP</td><td>벵골어 사회 편향 benchmark임</td></tr>
<tr><td>767</td><td><a href='https://arxiv.org/abs/2611.11386'>What Travels Across Languages? Reading, Transfer and Erasure of Cross-Lingual Concept Subspaces in Bangla Idioms</a></td><td>20</td><td>0</td><td>NLP</td><td>Bangla 관용구 개념 부분공간 분석임</td></tr>
<tr><td>768</td><td><a href='https://arxiv.org/abs/2611.11306'>ScrapeBench: Evaluating Legal Compliance of AI Agents in Website Scraping</a></td><td>20</td><td>0</td><td>NLP</td><td>웹 scraping 에이전트 법적 준수 benchmark임</td></tr>
<tr><td>769</td><td><a href='https://arxiv.org/abs/2611.10936'>Can small transformers learn the language of Coxeter groups?</a></td><td>20</td><td>0</td><td>LG</td><td>작은 transformer로 Coxeter group affine A2 언어를 학습하고 attention 관찰로 정리를 증명한 workshop 수준 사례</td></tr>
<tr><td>770</td><td><a href='https://arxiv.org/abs/2611.12222'>PARIS: A multi-agent LLM framework for end-to-end, PRISMA-guided systematic literature reviews with pre-synthesis corpus quality assessment</a></td><td>20</td><td>0</td><td>NLP</td><td>PRISMA 문헌 리뷰를 15개 LLM agent로 자동화하는 시스템 논문이며 자체 검증도 내부 reviewer agent에 그침</td></tr>
<tr><td>771</td><td><a href='https://arxiv.org/abs/2611.11745'>Reproducible quantum clustering for single-cell transcriptome atlases</a></td><td>20</td><td>0</td><td>LG</td><td>entanglement-free 양자 상태 인코딩으로 단일세포 clustering 재현성을 높이는 KQE-2, 생물정보 도메인이라 무관함</td></tr>
<tr><td>772</td><td><a href='https://arxiv.org/abs/2611.11727'>State Media at Retrieval Time: A Large-Scale Audit of Russian State-Aligned Sources in AI Chatbot Responses</a></td><td>20</td><td>0</td><td>NLP</td><td>11개 챗봇의 러시아 국영 매체 검색 노출 비율을 10만 응답으로 감사한 사회과학 성격 연구임</td></tr>
<tr><td>773</td><td><a href='https://arxiv.org/abs/2611.11657'>Inside the Trading Loop: Markets, Models, and Moves with LLM Agents</a></td><td>20</td><td>0</td><td>AI</td><td>LLM 분석가와 모멘텀 포트폴리오를 결합한 주식 거래 시스템의 5개월 paper account 결과, 로봇 무관함</td></tr>
<tr><td>774</td><td><a href='https://arxiv.org/abs/2611.10521'>TimeHF 2.0: Multimodal, Multivariate, and Multi-Region Collaborative Forecasting for Large-Scale Retail Supply Chains</a></td><td>20</td><td>0</td><td>LG</td><td>JD 소매 공급망 판매 예측용 multimodal 다지역 forecasting 프레임워크로 산업 응용</td></tr>
<tr><td>775</td><td><a href='https://arxiv.org/abs/2611.10156'>DeepResearch RewardBench: Evaluating Reward Models for Deep Research Report</a></td><td>20</td><td>0</td><td>NLP</td><td>deep research 보고서에 대한 reward model을 평가하는 DeepResearch RewardBench</td></tr>
<tr><td>776</td><td><a href='https://arxiv.org/abs/2611.11164'>Tutorial: Vision-Based Formation Control with Differential-Drive Robots</a></td><td>18</td><td>3</td><td>Control</td><td>차동구동 편대 제어 tutorial로 연구 기여 없음</td></tr>
<tr><td>777</td><td><a href='https://arxiv.org/abs/2611.11583'>NightSteps: A Night-Time Dataset and Benchmark for Pedestrian Crossing Intention Prediction</a></td><td>18</td><td>1</td><td>CV</td><td>야간 보행자 의도 예측 데이터셋</td></tr>
<tr><td>778</td><td><a href='https://arxiv.org/abs/2611.11437'>How to &quot;train&quot; a surgeon? Benchmarking generalist agents in surgical scene understanding</a></td><td>18</td><td>1</td><td>Multimodal</td><td>수술 장면 MLLM benchmark</td></tr>
<tr><td>779</td><td><a href='https://arxiv.org/abs/2611.10746'>RoadState: A Domain-Prior-Enhanced Vision-Language System for Industrial-Grade Lane-Level Map Updating</a></td><td>18</td><td>1</td><td>CV</td><td>차선 지도 갱신 VLM 시스템</td></tr>
<tr><td>780</td><td><a href='https://arxiv.org/abs/2611.10182'>ATLAS: A Multi-Procedure Benchmark and Context-Aware Model for Surgical Anatomy Segmentation</a></td><td>18</td><td>1</td><td>Medical</td><td>수술 해부 분할 benchmark</td></tr>
<tr><td>781</td><td><a href='https://arxiv.org/abs/2611.11827'>KKT-Perturbation-Aware Communication for Fully Distributed Online Convex Optimization with Nonseparable Coupling</a></td><td>18</td><td>1</td><td>LG</td><td>분산 온라인 볼록 최적화에서 KKT 섭동 기반 통신 트리거 설계, 이론 중심이며 로봇 연관 약함</td></tr>
<tr><td>782</td><td><a href='https://arxiv.org/abs/2611.12564'>GHiML: VLM-Guided Hierarchical Multi-Label Learning with Applications to Benthic Imagery</a></td><td>18</td><td>0</td><td>CV</td><td>저서생물 영상 분류, 무관</td></tr>
<tr><td>783</td><td><a href='https://arxiv.org/abs/2611.12037'>SAFE-Hair: Scalp-Anchored Fields for Exportable Single-View Hair Reconstruction</a></td><td>18</td><td>0</td><td>3D Vision</td><td>단일 뷰 머리카락 재구성, 무관</td></tr>
<tr><td>784</td><td><a href='https://arxiv.org/abs/2611.11735'>Correctness Metric Matters: NWD-Based Calibration Loss for Tiny Person Detection in UAV Infrared Imagery</a></td><td>18</td><td>0</td><td>CV</td><td>UAV 소형 사람 검출 calibration</td></tr>
<tr><td>785</td><td><a href='https://arxiv.org/abs/2611.11210'>DynOLAT: OLAT Video Prediction for Controllable Dynamic Full-Body Relighting</a></td><td>18</td><td>0</td><td>CV</td><td>인체 relighting</td></tr>
<tr><td>786</td><td><a href='https://arxiv.org/abs/2611.11116'>Query-Only Prompt-Agnostic Attacks on Visual In-Context Learning</a></td><td>18</td><td>0</td><td>CV</td><td>VICL 공격</td></tr>
<tr><td>787</td><td><a href='https://arxiv.org/abs/2611.10713'>Quadratic Bezier Splatting with Structural Initialization for Efficient Painting Rendering</a></td><td>18</td><td>0</td><td>CV</td><td>stroke 기반 painting 렌더링</td></tr>
<tr><td>788</td><td><a href='https://arxiv.org/abs/2611.10321'>LoCo: Selective Local Competition for Discriminative Open-Vocabulary Multi-Label Recognition</a></td><td>18</td><td>0</td><td>CV</td><td>open-vocab multi-label 인식</td></tr>
<tr><td>789</td><td><a href='https://arxiv.org/abs/2611.10262'>Domain Generalization for Style-Debiased Object Detection via Label-Consistent Training across Multiple Styles</a></td><td>18</td><td>0</td><td>CV</td><td>detection domain generalization</td></tr>
<tr><td>790</td><td><a href='https://arxiv.org/abs/2611.12058'>Exact Natarajan Dimension of Homogeneous Multiclass Linear Predictors</a></td><td>18</td><td>0</td><td>LG</td><td>다중 클래스 선형 예측기의 Natarajan 차원을 n(k-1)-1로 구한 짧은 이론 결과임</td></tr>
<tr><td>791</td><td><a href='https://arxiv.org/abs/2611.11481'>One-Shot Hierarchical Federated Clustering for Distributed Non-IID Biomedical Data Analysis</a></td><td>18</td><td>0</td><td>LG</td><td>생의학 데이터를 위한 one-shot 계층적 federated clustering, 로봇과 무관</td></tr>
<tr><td>792</td><td><a href='https://arxiv.org/abs/2611.11372'>LLM-based Multi-Criteria Deep Reinforcement Learning for Dynamic Efficient 5G UPF Selection</a></td><td>18</td><td>0</td><td>RL</td><td>LLM이 번역한 의도로 5G UPF 선택을 DRL로 수행, 네트워크 응용</td></tr>
<tr><td>793</td><td><a href='https://arxiv.org/abs/2611.11313'>Shape-Adaptive Subspace-Constrained Quadratic Matrix Factorization</a></td><td>18</td><td>0</td><td>LG</td><td>generalized Gaussian 잡음을 추정하는 quadratic manifold fitting, 고전 통계 방법</td></tr>
<tr><td>794</td><td><a href='https://arxiv.org/abs/2611.11031'>Hybrid Product Search Without the Copy: Lexical, Semantic and Filtered Retrieval Served Directly from a Data Lake</a></td><td>18</td><td>0</td><td>LG</td><td>데이터 레이크에서 lexical·vector hybrid 상품 검색을 Pinot으로 서빙함. 시스템 보고이고 로봇과 무관함</td></tr>
<tr><td>795</td><td><a href='https://arxiv.org/abs/2611.10992'>Hydro-Dataset: A Multi-Modal Open-Source Pipeline for Nordic Hydrological Research and Foundation Model Benchmarking</a></td><td>18</td><td>0</td><td>LG</td><td>북유럽 눈 관측 데이터셋 파이프라인임. 수문 도메인이라 로봇 무관함</td></tr>
<tr><td>796</td><td><a href='https://arxiv.org/abs/2611.10861'>SWXAI: A Unified Multimodal Explainability Library for Space Weather Forecasting and Heliophysics</a></td><td>18</td><td>0</td><td>LG</td><td>우주기상 XAI 라이브러리임. 도구 소개이며 로봇 무관함</td></tr>
<tr><td>797</td><td><a href='https://arxiv.org/abs/2611.12709'>A local language model layered with rule-based and neural detectors for clinical text de-identification: an open-source toolkit and evaluation</a></td><td>18</td><td>0</td><td>NLP</td><td>임상 텍스트 비식별화 툴킷임</td></tr>
<tr><td>798</td><td><a href='https://arxiv.org/abs/2611.11812'>CaseLaw: A Policy-Decoupled Framework for Training-Free Content Moderation</a></td><td>18</td><td>0</td><td>NLP</td><td>training-free 콘텐츠 moderation 프레임워크임</td></tr>
<tr><td>799</td><td><a href='https://arxiv.org/abs/2611.11794'>ChemInsight: A Comprehensive Benchmark for Evaluating and Diagnosing Chemistry Understanding and Reasoning in Large Language Models</a></td><td>18</td><td>0</td><td>NLP</td><td>화학 추론 benchmark임</td></tr>
<tr><td>800</td><td><a href='https://arxiv.org/abs/2611.11597'>Out of Parameters, Saved by Syntax: UD-PrMPT for Parser Augmented Low Resource Machine Translation</a></td><td>18</td><td>0</td><td>NLP</td><td>저자원 기계번역 파서 증강임</td></tr>
<tr><td>801</td><td><a href='https://arxiv.org/abs/2611.10909'>Pole or Vector? Encoders Capture Bangla Compound Verbs, but LLMs Read Them Literally</a></td><td>18</td><td>0</td><td>NLP</td><td>벵골어 복합동사 이해를 26개 모델로 재는 BanglaCV-Probe benchmark, 언어 특화 평가</td></tr>
<tr><td>802</td><td><a href='https://arxiv.org/abs/2611.10906'>SCorPion: A Strategic, Controllable and Personified Conversational Companion</a></td><td>18</td><td>0</td><td>NLP</td><td>GraphRAG로 대화 전략을 뽑아 조절하는 챗봇 SCorPion, 워크숍 수준 시스템</td></tr>
<tr><td>803</td><td><a href='https://arxiv.org/abs/2611.10721'>Behavioral Evaluation of Large Language Models Under Cognitive Biases in HAZOP Studies</a></td><td>18</td><td>0</td><td>NLP</td><td>HAZOP 안전 분석에서 LLM의 인지 편향 저항을 420 trial로 본 평가 연구</td></tr>
<tr><td>804</td><td><a href='https://arxiv.org/abs/2611.10414'>Track or Follow? A Jev-Compatible Multi-Agent Trading System When Web News Lags the Market</a></td><td>18</td><td>0</td><td>NLP</td><td>웹 뉴스가 시장을 뒤따르는지 보는 LLM 멀티 에이전트 트레이딩 시스템 연구, 금융 도메인</td></tr>
<tr><td>805</td><td><a href='https://arxiv.org/abs/2611.10266'>I play of the cello: Evaluating Constructional Bleeding in Multilingual LLMs with CALQUE</a></td><td>18</td><td>0</td><td>NLP</td><td>영어 구문 전략이 다른 언어로 새는 constructional bleeding을 재는 CALQUE 데이터셋</td></tr>
<tr><td>806</td><td><a href='https://arxiv.org/abs/2611.10044'>CulturalCrosswords: A Multilingual Benchmark of Answer Constraints and Grid Completion</a></td><td>18</td><td>0</td><td>NLP</td><td>42개 언어 문화 riddle crossword로 답 제약 조건 영향을 보는 CulturalCrosswords benchmark</td></tr>
<tr><td>807</td><td><a href='https://arxiv.org/abs/2611.09936'>How Many Examples, and Which Ones? A Study of In-Context Learning for Natural Language Inference</a></td><td>18</td><td>0</td><td>NLP</td><td>NLI에서 decoder LLM의 단순 prompt와 few-shot 개수 효과를 비교한 benchmark 연구</td></tr>
<tr><td>808</td><td><a href='https://arxiv.org/abs/2611.09933'>BIBIMBAP: A Benchmark for Instructional BIM-Based Automated Programming</a></td><td>18</td><td>0</td><td>NLP</td><td>IFC 건축 모델을 편집하는 Text-to-BIM 100개 과제 benchmark BIBIMBAP, 최고 50.2%</td></tr>
<tr><td>809</td><td><a href='https://arxiv.org/abs/2611.12379'>Reconstructing hourly traffic on every street of a capital from a sparse counting network: a graph neural network applied to Paris</a></td><td>18</td><td>0</td><td>LG</td><td>파리 도로 32,163개 구간 시간별 교통량을 GNN으로 복원, 대기질 모델용 도메인 응용</td></tr>
<tr><td>810</td><td><a href='https://arxiv.org/abs/2611.11658'>Measuring Generative AI Content in Political Campaigns: Evidence of Rising Adoption and Non-Disclosure</a></td><td>18</td><td>0</td><td>CV</td><td>미국 후보 12,977명의 선거 자료에서 생성형 AI 콘텐츠 비중을 측정한 사회과학 연구로 무관함</td></tr>
<tr><td>811</td><td><a href='https://arxiv.org/abs/2611.11651'>Optimizing Multi-Tier Intermediation in Programmatic Advertising: A DAG-Based Mechanism for Supply Path Optimization</a></td><td>18</td><td>0</td><td>AI</td><td>광고 공급 경로를 DAG와 MILP로 최적화하는 메커니즘 설계로 실험 계획만 제시하며 무관함</td></tr>
<tr><td>812</td><td><a href='https://arxiv.org/abs/2611.10679'>RankShift: Evaluating Ranking Instability Across Benchmark Dimensions in Document Parsing</a></td><td>18</td><td>0</td><td>CV</td><td>문서 파싱 benchmark에서 matching·scoring 방식에 따른 순위 불안정을 측정한 평가 연구로 로봇 무관</td></tr>
<tr><td>813</td><td><a href='https://arxiv.org/abs/2611.10445'>DiSARM: Diverse and Surprising Association Rule Mining with Large Language Models</a></td><td>18</td><td>0</td><td>LG</td><td>LLM으로 연관 규칙의 주관적 흥미도를 평가하는 association rule mining 하이브리드로 로봇 무관</td></tr>
<tr><td>814</td><td><a href='https://arxiv.org/abs/2611.10233'>ProofDiff: Auditable Argument-Level Comparison of AI-Generated Mathematical Proofs</a></td><td>18</td><td>0</td><td>NLP</td><td>AI가 쓴 수학 증명 두 개를 argument map으로 비교하는 사람 검토용 도구 ProofDiff, 예시 4쌍만 시연</td></tr>
<tr><td>815</td><td><a href='https://arxiv.org/abs/2611.11170'>ClusLoad: Cluster-Guided Model Sharing for Scalable Distribution Transformer Load Forecasting</a></td><td>16</td><td>0</td><td>LG</td><td>T-Rep 클러스터링으로 배전 변압기 부하 예측 모델을 공유, 전력 응용</td></tr>
<tr><td>816</td><td><a href='https://arxiv.org/abs/2611.10555'>YRC-Bench: Benchmarking Culturally Aware Machine Translation for Historical Heritage via Tri-Level Semantic Bridging</a></td><td>16</td><td>0</td><td>NLP</td><td>황하 문화 기록의 고전 중국어 번역 benchmark YRC-Bench, 번역 평가셋</td></tr>
<tr><td>817</td><td><a href='https://arxiv.org/abs/2611.12405'>PTC-IoU: CPU-Friendly Detection Quality Estimation for Edge Video Analytics</a></td><td>15</td><td>1</td><td>CV</td><td>엣지 검출 품질 추정, incremental</td></tr>
<tr><td>818</td><td><a href='https://arxiv.org/abs/2611.11831'>End-to-End Joint Training of Super-Resolution and Compression Artifact Removal for Industrial Machine Vision</a></td><td>15</td><td>1</td><td>CV</td><td>산업 영상 SR과 압축 아티팩트 제거</td></tr>
<tr><td>819</td><td><a href='https://arxiv.org/abs/2611.11843'>Aggregation-Induced Calibration Failure in Sum-Based Label Expansion for Multi-Label Facial Expression Recognition: A Diagnostic Study</a></td><td>15</td><td>0</td><td>CV</td><td>표정 인식 calibration 실패 분석</td></tr>
<tr><td>820</td><td><a href='https://arxiv.org/abs/2611.11790'>FMA-Net: Flexible Modality Adaptation for Robust Multimodal Face Presentation Attack Detection</a></td><td>15</td><td>0</td><td>CV</td><td>얼굴 presentation attack 탐지</td></tr>
<tr><td>821</td><td><a href='https://arxiv.org/abs/2611.11644'>MICE: Multi-animal Interaction Context Encoder - A Hierarchical Foundation Model for Mouse Behavior</a></td><td>15</td><td>0</td><td>LG</td><td>쥐 행동 foundation model, 무관</td></tr>
<tr><td>822</td><td><a href='https://arxiv.org/abs/2611.11427'>Flex-DDCM: Zero-Shot Task-Oriented Image Compression via Diffusion Trajectory Guidance</a></td><td>15</td><td>0</td><td>Generative</td><td>diffusion 기반 압축</td></tr>
<tr><td>823</td><td><a href='https://arxiv.org/abs/2611.11200'>Source-Anchored Visual Autoregression for Extreme Image Compression</a></td><td>15</td><td>0</td><td>CV</td><td>극저비트 이미지 압축</td></tr>
<tr><td>824</td><td><a href='https://arxiv.org/abs/2611.10908'>Beyond Real or Fake: A Dual-Channel Authenticity and Reasoning Protocol for Photographic Assessment</a></td><td>15</td><td>0</td><td>Multimodal</td><td>사진 진위 판별 protocol</td></tr>
<tr><td>825</td><td><a href='https://arxiv.org/abs/2611.10875'>REDiff-AD: No Training and No Target Masks for Industrial Anomaly Image Generation via Diversity-Driven In-Context MMDiT</a></td><td>15</td><td>0</td><td>Generative</td><td>산업 이상 이미지 생성</td></tr>
<tr><td>826</td><td><a href='https://arxiv.org/abs/2611.10811'>STAR-VF: Spatio-Temporal Aware Representation Condensation for Data-Efficient Video Fusion</a></td><td>15</td><td>0</td><td>Video</td><td>영상 융합 데이터 효율</td></tr>
<tr><td>827</td><td><a href='https://arxiv.org/abs/2611.10665'>Physically Guided TeX Generation for Low-Light Visual Tasks</a></td><td>15</td><td>0</td><td>CV</td><td>저조도 TeX 생성</td></tr>
<tr><td>828</td><td><a href='https://arxiv.org/abs/2611.10642'>VisProve: Learning Typed Visual Provenance for Scientific Document Question Answering</a></td><td>15</td><td>0</td><td>Multimodal</td><td>과학 문서 QA 출처</td></tr>
<tr><td>829</td><td><a href='https://arxiv.org/abs/2611.10626'>EndoSCOP-V: A Multi-Turn Video Understanding Evaluation Framework for Multimodal Models in Endoscopy Reporting and Clinical Reasoning</a></td><td>15</td><td>0</td><td>Medical</td><td>내시경 영상 이해 평가</td></tr>
<tr><td>830</td><td><a href='https://arxiv.org/abs/2611.10592'>MotionGraphicsBench: Evaluating Motion Graphics Generation with Programmatic Verification</a></td><td>15</td><td>0</td><td>Generative</td><td>motion graphics benchmark</td></tr>
<tr><td>831</td><td><a href='https://arxiv.org/abs/2611.10485'>Decoupling Direction and Magnitude: Language-Steered Flow Matching for Super-Resolution in the Dark</a></td><td>15</td><td>0</td><td>CV</td><td>저조도 SR</td></tr>
<tr><td>832</td><td><a href='https://arxiv.org/abs/2611.10088'>Same Pixels, Different Documents: Measuring Part-Level Editability in Image Vectorization</a></td><td>15</td><td>0</td><td>CV</td><td>벡터화 편집성</td></tr>
<tr><td>833</td><td><a href='https://arxiv.org/abs/2611.11877'>Tropical Gaussian Anticoncentration: Optimal Instance-Dependent Bounds for Online Learning in Extensive-Form Games</a></td><td>15</td><td>0</td><td>LG</td><td>extensive-form game 온라인 학습의 regret 하한을 tropical Gaussian 기법으로 증명한 순수 이론이라 로봇 연관 없음</td></tr>
<tr><td>834</td><td><a href='https://arxiv.org/abs/2611.11691'>Resolvent Ellipsoid for Minty Set Inclusions</a></td><td>15</td><td>0</td><td>LG</td><td>Minty set inclusion을 resolvent ellipsoid로 푸는 최적화 이론, 로봇 무관</td></tr>
<tr><td>835</td><td><a href='https://arxiv.org/abs/2611.11656'>Means vs. Foundation Models for Emergency Call Forecasting</a></td><td>15</td><td>0</td><td>LG</td><td>응급 신고 건수 예측에서 Holder/Lehmer 평균과 TimeGPT를 비교한 단순 응용 연구</td></tr>
<tr><td>836</td><td><a href='https://arxiv.org/abs/2611.11263'>Beyond Node Attributes: A Controlled Evaluation and Ablation of Local Interaction Statistics for Ethereum Phishing Detection</a></td><td>15</td><td>0</td><td>LG</td><td>Ethereum phishing 탐지에 12개 interaction 통계 feature 추가의 ablation, 로봇 무관</td></tr>
<tr><td>837</td><td><a href='https://arxiv.org/abs/2611.10579'>Predictive Modelling of Solid Waste Generation through Time Series Analysis</a></td><td>15</td><td>0</td><td>LG</td><td>스리랑카 폐기물량을 SARIMAX·LSTM 등으로 비교 예측함. 단순 응용 비교임</td></tr>
<tr><td>838</td><td><a href='https://arxiv.org/abs/2611.10046'>Topological Deep Learning Challenge 2026: Bridging the Gap</a></td><td>15</td><td>0</td><td>LG</td><td>Topological DL 챌린지 소개문으로 연구 기여 없음</td></tr>
<tr><td>839</td><td><a href='https://arxiv.org/abs/2611.12691'>A Lattice-Based HMM Approach to Aruz Scansion of Ottoman Poetry</a></td><td>15</td><td>0</td><td>NLP</td><td>오스만 시 aruz 운율 분석 HMM임</td></tr>
<tr><td>840</td><td><a href='https://arxiv.org/abs/2611.12597'>Unmasking Four Knapsack Problems in the Traveling Thief Benchmark</a></td><td>15</td><td>0</td><td>LG</td><td>traveling thief benchmark 분석임</td></tr>
<tr><td>841</td><td><a href='https://arxiv.org/abs/2611.12197'>TrajLift: Lifting Memory Recall Trajectories with Latency-Modulated Heat Diffusion</a></td><td>15</td><td>0</td><td>LG</td><td>알츠하이머 회상 궤적 heat diffusion 분석임</td></tr>
<tr><td>842</td><td><a href='https://arxiv.org/abs/2611.12196'>The Deception Archive as a repository of standardized datasets for large-scale verbal deception detection research</a></td><td>15</td><td>0</td><td>NLP</td><td>거짓말 탐지 데이터 저장소임</td></tr>
<tr><td>843</td><td><a href='https://arxiv.org/abs/2611.11679'>The Average Patient: Do Simulated Psychiatric Patients Answer Like Real People?</a></td><td>15</td><td>0</td><td>NLP</td><td>모의 정신과 환자 응답 평가임</td></tr>
<tr><td>844</td><td><a href='https://arxiv.org/abs/2611.11471'>Saidzoda-CA-EmbeddingGemma-300M: One Small Embedder for Tajik, Kazakh, Uzbek and Kyrgyz</a></td><td>15</td><td>0</td><td>NLP</td><td>저자원 언어 임베더 적응임</td></tr>
<tr><td>845</td><td><a href='https://arxiv.org/abs/2611.10997'>Open Problems in Chatbots and Mental Health</a></td><td>15</td><td>0</td><td>NLP</td><td>챗봇과 정신건강의 open problem을 정리한 position 성격 글, 방법론 기여 없음</td></tr>
<tr><td>846</td><td><a href='https://arxiv.org/abs/2611.10802'>Evaluating Jev on Arabic: Comparing Decision Models and LLMs Across Arabic Tasks and Dialects</a></td><td>15</td><td>0</td><td>NLP</td><td>Jev 시스템을 아랍어 43개 과제에서 67개 시스템과 비교한 평가 보고서임</td></tr>
<tr><td>847</td><td><a href='https://arxiv.org/abs/2611.10797'>Adapting Large Language Models via Multi-Task Learning for Mental Health Problem, Emotion, and Sentiment Detection</a></td><td>15</td><td>0</td><td>NLP</td><td>Llama 3.1 8B에 순차 multi-task LoRA로 정신건강 감정 분류를 하는 응용 연구</td></tr>
<tr><td>848</td><td><a href='https://arxiv.org/abs/2611.10327'>Policy Over Purpose: Auditing LLM Content Moderation of Reclaimed Slur Usage</a></td><td>15</td><td>0</td><td>NLP</td><td>재전유된 slur 사용에 대한 LLM 콘텐츠 moderation 감사 연구</td></tr>
<tr><td>849</td><td><a href='https://arxiv.org/abs/2611.12377'>Detecting Shadow AI: Unsanctioned LLM Agents on Enterprise Endpoints: A Taxonomy, an Open Detector and a Controlled Evaluation</a></td><td>15</td><td>0</td><td>NLP</td><td>Windows 단말에서 비인가 LLM agent를 탐지하는 Agent Detector, 보안 시스템 연구</td></tr>
<tr><td>850</td><td><a href='https://arxiv.org/abs/2611.10845'>Inference for Reasoning Models: Practical Lessons from Evaluation and Serving</a></td><td>15</td><td>0</td><td>NLP</td><td>추론 모델의 평가·서빙 설정 영향을 정리한 217쪽 책으로 새 방법 없고 로봇 무관</td></tr>
<tr><td>851</td><td><a href='https://arxiv.org/abs/2611.10704'>R-BED: A Consequence-Aware Framework for System-Level AI Evaluation and Continuous Assurance</a></td><td>15</td><td>0</td><td>AI Safety</td><td>배포 AI 시스템의 결과 인지 평가 방법론 명세로 실증 검증 없음</td></tr>
<tr><td>852</td><td><a href='https://arxiv.org/abs/2611.12686'>Differentiable Inverse Rendering Recovers Intrinsic Properties from Intravascular Optical Coherence Tomography</a></td><td>14</td><td>0</td><td>Medical</td><td>혈관내 광학영상 inverse rendering, 무관</td></tr>
<tr><td>853</td><td><a href='https://arxiv.org/abs/2611.11836'>MDA framework: multi-architecture domain adaptation for unsupervised person re-identification</a></td><td>14</td><td>0</td><td>CV</td><td>person re-id domain adaptation</td></tr>
<tr><td>854</td><td><a href='https://arxiv.org/abs/2611.11833'>Answer or Defer? Testing VLMs&#x27; Stated Confidence on Brain MRI</a></td><td>14</td><td>0</td><td>Medical</td><td>뇌 MRI VLM 신뢰도 평가</td></tr>
<tr><td>855</td><td><a href='https://arxiv.org/abs/2611.11433'>Unlearning at Speed: Rapid Activation Dampening for Efficient Machine Unlearning in Real-World Face Recognition</a></td><td>14</td><td>0</td><td>CV</td><td>얼굴 인식 unlearning</td></tr>
<tr><td>856</td><td><a href='https://arxiv.org/abs/2611.11378'>SegDis: Foreground Segmentation Followed by Type Discrimination for Salient and Camouflaged Object Detection</a></td><td>14</td><td>0</td><td>CV</td><td>salient/camouflage 객체 분할</td></tr>
<tr><td>857</td><td><a href='https://arxiv.org/abs/2611.11852'>Identifiable but Hard to Estimate: Rotation in Equally Spaced Overcomplete ICA</a></td><td>14</td><td>0</td><td>LG</td><td>2차원 overcomplete ICA의 회전 추정 표본 복잡도를 다룬 통계 이론, 로봇과 무관</td></tr>
<tr><td>858</td><td><a href='https://arxiv.org/abs/2611.11613'>Daily Emergency Call Volume Forecasting using Univariate and Multivariate TimeGPT</a></td><td>14</td><td>0</td><td>LG</td><td>TimeGPT로 응급 신고량 예측했으나 SARIMAX 등이 더 낫다는 단순 응용 비교</td></tr>
<tr><td>859</td><td><a href='https://arxiv.org/abs/2611.10209'>Compact Greek Language Models from Scratch: Pretraining 500M- and 1B-Parameter Decoder-Only Transformers</a></td><td>14</td><td>0</td><td>NLP</td><td>그리스어 500M, 1B decoder 모델 from scratch 사전학습 보고서, 성능은 near chance 수준</td></tr>
<tr><td>860</td><td><a href='https://arxiv.org/abs/2611.10842'>Factor Rank: A Canonical Algebraic Generalization of Tree Decision Diagrams</a></td><td>14</td><td>0</td><td>Theory</td><td>Boolean 함수 표현인 tree decision diagram을 rank 기반 canonical 형태 ATDD로 일반화한 논리 이론 연구로 로봇 무관</td></tr>
<tr><td>861</td><td><a href='https://arxiv.org/abs/2611.10331'>Evaluating classification and explainability in multimodal petrographic image analysis</a></td><td>14</td><td>0</td><td>CV</td><td>LITHOS 암석 박편 분류기의 오류 구조와 XAI 지도 신뢰도를 분석한 지질 응용</td></tr>
<tr><td>862</td><td><a href='https://arxiv.org/abs/2611.10277'>Adversarial Evaluation of Large Language Models for Patient-Friendly Radiology Report Summarization</a></td><td>14</td><td>0</td><td>Medical NLP</td><td>영상의학 보고서 요약 LLM에 용어 치환 adversarial 평가를 적용한 의료 평가 연구</td></tr>
<tr><td>863</td><td><a href='https://arxiv.org/abs/2611.10261'>Is Recursive Self-Improvement Safe?</a></td><td>14</td><td>0</td><td>AI Safety</td><td>재귀적 자기 개선의 안전성을 논하고 게임이론 분석을 덧붙인 의견글</td></tr>
<tr><td>864</td><td><a href='https://arxiv.org/abs/2611.10739'>Pulse waveform morphology encodes haemodynamic signatures of impending stroke</a></td><td>13</td><td>0</td><td>Medical</td><td>PPG 파형 morphology로 뇌졸중 임박 신호를 찾는 의료 연구로 로봇 무관</td></tr>
<tr><td>865</td><td><a href='https://arxiv.org/abs/2611.12727'>OptiCover: A Scalable and Multi-Surface Framework for Cold-Start Visual Optimization under Semantic Constraints</a></td><td>12</td><td>0</td><td>CV</td><td>e-commerce 커버 사진 선택, 무관</td></tr>
<tr><td>866</td><td><a href='https://arxiv.org/abs/2611.12574'>Evaluating Cross-Signal Coherence in Mammography Vision-Language Models</a></td><td>12</td><td>0</td><td>Medical</td><td>유방촬영 VLM 일관성 평가, 무관</td></tr>
<tr><td>867</td><td><a href='https://arxiv.org/abs/2611.12075'>How a Model&#x27;s Architecture and Performance Influences Explainability: A Study of Grad-CAM and CRAFT in CNN-Based Image Classification</a></td><td>12</td><td>0</td><td>CV</td><td>Grad-CAM 설명 가능성 비교, 무관</td></tr>
<tr><td>868</td><td><a href='https://arxiv.org/abs/2611.12025'>Single Image Super-Resolution via Semantic Prompt and Cross-Modal Training on Content Area</a></td><td>12</td><td>0</td><td>CV</td><td>super-resolution, 로봇 무관</td></tr>
<tr><td>869</td><td><a href='https://arxiv.org/abs/2611.11757'>Calibrated Alarm Thresholds for Compact Fire and Smoke Detectors</a></td><td>12</td><td>0</td><td>CV</td><td>화재 검출 calibration, 무관</td></tr>
<tr><td>870</td><td><a href='https://arxiv.org/abs/2611.11753'>SpinSCI: Mask-Conditioned Spatial-Temporal Spin Transformer for Video Snapshot Compressive Imaging</a></td><td>12</td><td>0</td><td>CV</td><td>video snapshot compressive imaging</td></tr>
<tr><td>871</td><td><a href='https://arxiv.org/abs/2611.11503'>AgentCT: A Vision-Language Agent for Universal CT Imaging</a></td><td>12</td><td>0</td><td>Medical</td><td>CT 복원 agent</td></tr>
<tr><td>872</td><td><a href='https://arxiv.org/abs/2611.11391'>Let the Gallery Learn Itself: Training-Free Iterative Side-View Face Recognition</a></td><td>12</td><td>0</td><td>CV</td><td>얼굴 인식 gallery 자기 진화</td></tr>
<tr><td>873</td><td><a href='https://arxiv.org/abs/2611.11076'>ADC-RANet: Improving Resolution Adaptive Neural Networks with Attention, Distillation and Calibration</a></td><td>12</td><td>0</td><td>CV</td><td>dynamic network 해상도 적응</td></tr>
<tr><td>874</td><td><a href='https://arxiv.org/abs/2611.10770'>How reliable is an embedding of the seabed? Repeat-look measurement of frozen encoders on synthetic aperture sonar</a></td><td>12</td><td>0</td><td>CV</td><td>해저 sonar 임베딩 신뢰도</td></tr>
<tr><td>875</td><td><a href='https://arxiv.org/abs/2611.10764'>BAPLe++: Cross-Model Transferability and Prompt-Level Defense of Backdoors in Medical Foundation Models</a></td><td>12</td><td>0</td><td>Medical</td><td>의료 FM 백도어 방어</td></tr>
<tr><td>876</td><td><a href='https://arxiv.org/abs/2611.10758'>Unified Framework with Convex-Concave Decomposition and Sparse Topological Learning for Skeleton-Based Clinical Assessment</a></td><td>12</td><td>0</td><td>CV</td><td>재활 평가 skeleton</td></tr>
<tr><td>877</td><td><a href='https://arxiv.org/abs/2611.10644'>Agent2BIM: A Systematic Evaluation of Reality-Capture Configurations and Prior Models for As-Built Modeling</a></td><td>12</td><td>0</td><td>3D Vision</td><td>BIM 생성 agent 평가</td></tr>
<tr><td>878</td><td><a href='https://arxiv.org/abs/2611.10484'>Can General-Purpose Generative AI Supply Training Data for Medical Vision Models? A Multimodal Retrospective Study</a></td><td>12</td><td>0</td><td>Medical</td><td>생성 AI 의료 학습 데이터</td></tr>
<tr><td>879</td><td><a href='https://arxiv.org/abs/2611.10376'>PhysDNet: Physics-Driven Gradient Amplification for Real-Time Image Dehazing</a></td><td>12</td><td>0</td><td>CV</td><td>dehazing</td></tr>
<tr><td>880</td><td><a href='https://arxiv.org/abs/2611.10249'>Beyond Frame-Level Accuracy: Analyzing Video-Level Stability in Transformer-Based Deepfake Forensics</a></td><td>12</td><td>0</td><td>Video</td><td>deepfake 안정성</td></tr>
<tr><td>881</td><td><a href='https://arxiv.org/abs/2611.12725'>Scaling Taxonomy-Free Image Labeling with Generative AI: A Multimodal</a></td><td>12</td><td>0</td><td>Multimodal</td><td>이미지 labeling 생성 AI</td></tr>
<tr><td>882</td><td><a href='https://arxiv.org/abs/2611.12078'>SadaqahStories: A Verified English-Arabic Corpus of Charity Stories for Children, with an Audit of Errors in AI-Drafted Religious Narratives</a></td><td>12</td><td>0</td><td>NLP</td><td>아랍어 자선 이야기 코퍼스임</td></tr>
<tr><td>883</td><td><a href='https://arxiv.org/abs/2611.12020'>A generalized transition framework for identifying reduction domains in non-binary constituency parsing</a></td><td>12</td><td>0</td><td>NLP</td><td>비이항 구문 분석 reduction 도메인 프레임워크임</td></tr>
<tr><td>884</td><td><a href='https://arxiv.org/abs/2611.11952'>BharatSynthQA: A Context-Grounded Question Answering Dataset on Indian Temples and Religious Heritage</a></td><td>12</td><td>0</td><td>NLP</td><td>인도 사원 QA 데이터셋임</td></tr>
<tr><td>885</td><td><a href='https://arxiv.org/abs/2611.11891'>A Large-Scale Dataset for Cross-Lingual Multi-Jurisdiction Patent Drafting from Patent Cooperation Treaty Applications</a></td><td>12</td><td>0</td><td>NLP</td><td>특허 초안 다국어 데이터셋임</td></tr>
<tr><td>886</td><td><a href='https://arxiv.org/abs/2611.11502'>Does Merge Form a Hopf Algebra? Coproducts, Traces, and the Prospects of Algebraic Minimalism</a></td><td>12</td><td>0</td><td>NLP</td><td>Merge의 Hopf 대수 이론 논의임</td></tr>
<tr><td>887</td><td><a href='https://arxiv.org/abs/2611.11426'>Vietnamese Legal Ontology: Every legal answer, traced to the article that grounds it</a></td><td>12</td><td>0</td><td>NLP</td><td>베트남 법률 ontology임</td></tr>
<tr><td>888</td><td><a href='https://arxiv.org/abs/2611.11284'>WarBias: A Bilingual LLM Benchmark of Stereotypes About Internally Displaced People and Veterans</a></td><td>12</td><td>0</td><td>NLP</td><td>이주민 편견 이중언어 benchmark임</td></tr>
<tr><td>889</td><td><a href='https://arxiv.org/abs/2611.11243'>Saidzoda-Tajik-EmbeddingGemma-300M: Knowing Every Letter Is Not Reading Tajik</a></td><td>12</td><td>0</td><td>NLP</td><td>타직어 임베더 적응임</td></tr>
<tr><td>890</td><td><a href='https://arxiv.org/abs/2611.10931'>Gendered Misclassification from Surname-Based Race Imputation</a></td><td>12</td><td>0</td><td>NLP</td><td>성씨 기반 인종 추정이 여성에게 편향됨을 보인 정치학 통계 연구, ML 기여 거의 없음</td></tr>
<tr><td>891</td><td><a href='https://arxiv.org/abs/2611.09941'>Topic-Aware Multi-Task Mental Health Classification with Active Learning-Based Stepwise Relabeling for Social Media Conversations</a></td><td>12</td><td>0</td><td>NLP</td><td>Reddit 정신건강 multi-task 분류에 topic과 active learning relabeling 추가, 개선폭 0.09-1.57%</td></tr>
<tr><td>892</td><td><a href='https://arxiv.org/abs/2611.10818'>ATHENA: Hypergraph-Based Learning for Toddler Autism Classification from Eye-Tracking</a></td><td>12</td><td>0</td><td>Medical</td><td>eye-tracking 기반 유아 자폐 분류용 hypergraph 모델로 의료 응용이며 로봇 무관</td></tr>
<tr><td>893</td><td><a href='https://arxiv.org/abs/2611.10317'>TripleGrader: A Web-Based Platform Supporting Collaborative Triple Annotation with Quality Grading and Inter-Rater Agreement Assessment</a></td><td>12</td><td>0</td><td>Tool</td><td>지식 그래프 triple을 0-10 등급으로 협업 평가하는 웹 도구 TripleGrader로 연구 기여 미미</td></tr>
<tr><td>894</td><td><a href='https://arxiv.org/abs/2611.10048'>Veterans&#x27; Mental Health Crisis Severity Annotation: Do LLMs Agree More Than Human Experts?</a></td><td>12</td><td>0</td><td>NLP</td><td>참전 군인 위기 심각도 트윗 149건 주석에서 LLM과 전문가 일치도를 비교한 평가</td></tr>
<tr><td>895</td><td><a href='https://arxiv.org/abs/2611.12681'>National-Scale Crop Type Mapping in Morocco Using Google AlphaEarth Foundations Embeddings and the Fields of the World Field Boundary Map</a></td><td>10</td><td>0</td><td>CV</td><td>작물 지도 응용, 무관</td></tr>
<tr><td>896</td><td><a href='https://arxiv.org/abs/2611.12070'>Color wave: A systematic evaluation of active screen illumination for injection attack detection in remote face authentication</a></td><td>10</td><td>0</td><td>CV</td><td>얼굴 인증 공격 탐지, 무관</td></tr>
<tr><td>897</td><td><a href='https://arxiv.org/abs/2611.11139'>Graphene: A Lightweight Transformer with Ising Mean-Field Refinement for Image Super-Resolution</a></td><td>10</td><td>0</td><td>CV</td><td>경량 SR</td></tr>
<tr><td>898</td><td><a href='https://arxiv.org/abs/2611.11115'>MySign: A High-Fidelity Motion-Capture Dataset for 3D Sign Generation in Bahasa Isyarat Malaysia</a></td><td>10</td><td>0</td><td>CV</td><td>수화 모션캡처 데이터셋</td></tr>
<tr><td>899</td><td><a href='https://arxiv.org/abs/2611.10960'>Anatomy-Activated Mixture-of-Experts for 3D Medical Vision-Language Pre-training</a></td><td>10</td><td>0</td><td>Medical</td><td>3D 의료 VLP</td></tr>
<tr><td>900</td><td><a href='https://arxiv.org/abs/2611.10858'>Beyond Bit Matching: Orthogonal Watermarks for Collusion-Resistant Image Fingerprinting</a></td><td>10</td><td>0</td><td>CV</td><td>이미지 fingerprint 워터마크</td></tr>
<tr><td>901</td><td><a href='https://arxiv.org/abs/2611.10847'>Fine-resolution land-use segmentation and synthetic image-label augmentation in the Kathmandu Valley</a></td><td>10</td><td>0</td><td>CV</td><td>토지 이용 분할</td></tr>
<tr><td>902</td><td><a href='https://arxiv.org/abs/2611.10678'>MGE: A Membership Guided Data Extraction Attack against Diffusion Models</a></td><td>10</td><td>0</td><td>Generative</td><td>diffusion 추출 공격</td></tr>
<tr><td>903</td><td><a href='https://arxiv.org/abs/2611.10637'>VAComp: View-Aware Full Projector Compensation</a></td><td>10</td><td>0</td><td>CV</td><td>프로젝터 보정</td></tr>
<tr><td>904</td><td><a href='https://arxiv.org/abs/2611.10599'>The RenAIssance: Caption-Guided Diffusion Models for Historical-Art Visual Media</a></td><td>10</td><td>0</td><td>Generative</td><td>역사 미술 diffusion</td></tr>
<tr><td>905</td><td><a href='https://arxiv.org/abs/2611.10475'>WordEval: Evaluating Word-Native Operation Fidelity in Document Editing</a></td><td>10</td><td>0</td><td>NLP</td><td>Word 편집 평가</td></tr>
<tr><td>906</td><td><a href='https://arxiv.org/abs/2611.10413'>Frequency-Structure Complementary Modeling for Hyperspectral Image Fusion</a></td><td>10</td><td>0</td><td>CV</td><td>초분광 융합</td></tr>
<tr><td>907</td><td><a href='https://arxiv.org/abs/2611.10377'>Vision Language Models for Primary Structure Threat Identification in Wildland Urban Interface Fires</a></td><td>10</td><td>0</td><td>Multimodal</td><td>산불 위협 VLM</td></tr>
<tr><td>908</td><td><a href='https://arxiv.org/abs/2611.10318'>AI-Driven Repair of Missing Automotive Components</a></td><td>10</td><td>0</td><td>CV</td><td>차량 부품 복원</td></tr>
<tr><td>909</td><td><a href='https://arxiv.org/abs/2611.10245'>From Weapons to Events: Evaluating Evidential Support in Multimodal AI for Policing</a></td><td>10</td><td>0</td><td>Multimodal</td><td>경찰 영상 증거</td></tr>
<tr><td>910</td><td><a href='https://arxiv.org/abs/2611.10097'>A Privacy-Aware Deep Learning Benchmark for Facial Emotion Recognition</a></td><td>10</td><td>0</td><td>CV</td><td>프라이버시 표정 인식</td></tr>
<tr><td>911</td><td><a href='https://arxiv.org/abs/2611.11576'>Continuous modeling of manipulative participation for stance analysis: Online discourse on the 2024 Street Animal Law in Türkiye</a></td><td>10</td><td>0</td><td>NLP</td><td>터키 온라인 담론 입장 분석임</td></tr>
<tr><td>912</td><td><a href='https://arxiv.org/abs/2611.11497'>TID System for Speech-COSER Challenge 2026: ASR Track</a></td><td>10</td><td>0</td><td>NLP</td><td>ASR 챌린지 시스템 보고임</td></tr>
<tr><td>913</td><td><a href='https://arxiv.org/abs/2611.11416'>Modeling individual and item differences in atypicality inferences with ACT-R</a></td><td>10</td><td>0</td><td>NLP</td><td>ACT-R로 atypicality 추론을 모델링함</td></tr>
<tr><td>914</td><td><a href='https://arxiv.org/abs/2611.11349'>AOP-Smart-Finder: A High-Throughput Human-AI Hybrid Framework for AOP Discovery and Evidence Mapping from Large-Scale Literature</a></td><td>10</td><td>0</td><td>NLP</td><td>AOP 문헌 발굴 프레임워크임</td></tr>
<tr><td>915</td><td><a href='https://arxiv.org/abs/2611.10608'>An LLM-Orchestrated Multi-Modal Chatbot for Tomato Disease Consultant</a></td><td>10</td><td>0</td><td>NLP</td><td>토마토 병해 상담용 LLM chatbot 데모로 novelty와 로봇 연관 모두 없음</td></tr>
<tr><td>916</td><td><a href='https://arxiv.org/abs/2611.10399'>Too Big to Inspect? Ethically Auditing Large Datasets Through Small Samples</a></td><td>10</td><td>0</td><td>Ethics</td><td>AI 윤리 도구를 작은 표본에 적용해 대형 데이터셋 편향을 감사하는 정성 연구로 로봇 무관</td></tr>
<tr><td>917</td><td><a href='https://arxiv.org/abs/2611.10109'>The Infrastructure Divide: Analyzing Community Stance on Data Center Development via Reddit</a></td><td>10</td><td>0</td><td>Social</td><td>Reddit 10만 댓글로 데이터센터 건설 찬반 stance를 LLM으로 분석한 사회 연구</td></tr>
<tr><td>918</td><td><a href='https://arxiv.org/abs/2611.10054'>AYO: A Safe and Privacy-Preserving Platform for Studying Children&#x27;s Interaction with LLMs</a></td><td>10</td><td>0</td><td>HCI</td><td>아동의 LLM 상호작용 연구용 안전 플랫폼 AYO로 인프라 소개 수준</td></tr>
<tr><td>919</td><td><a href='https://arxiv.org/abs/2611.12855'>AI-based characterization of lymphoid structures and the tumor microenvironment reveals lower mature tertiary lymphoid structures, lymph-node follicles, and plasma cells after neoadjuvant therapy in lung squamous cell carcinoma</a></td><td>8</td><td>0</td><td>Medical</td><td>병리 조직 분석, 로봇과 무관</td></tr>
<tr><td>920</td><td><a href='https://arxiv.org/abs/2611.12437'>Occupancy Modelling of Biased Landslide Inventories: When Does Separating Occurrence from Recording Improve on Neutralisation?</a></td><td>8</td><td>0</td><td>CV</td><td>산사태 모델링, 무관</td></tr>
<tr><td>921</td><td><a href='https://arxiv.org/abs/2611.11906'>RBA: A Read-out Basis Adapter for Parameter-Efficient Interactive OCTA Vessel Segmentation with SEEM</a></td><td>8</td><td>0</td><td>Medical</td><td>OCTA 혈관 분할, 무관</td></tr>
<tr><td>922</td><td><a href='https://arxiv.org/abs/2611.11893'>Developing a Street View Imagery Processing Pipeline for Building-Level Vacant House Assessment</a></td><td>8</td><td>0</td><td>CV</td><td>빈집 평가 street view, 무관</td></tr>
<tr><td>923</td><td><a href='https://arxiv.org/abs/2611.11793'>Benchmarking CNNs, Vision Transformers, and Foundation Models for Explainable Brain Tumor MRI Classification: Calibration, Decision Analysis, and External Validation</a></td><td>8</td><td>0</td><td>Medical</td><td>뇌종양 분류 benchmark</td></tr>
<tr><td>924</td><td><a href='https://arxiv.org/abs/2611.11547'>Dropping Tokens Without Dropping Them: Causal Attribution for Diabetic Retinopathy</a></td><td>8</td><td>0</td><td>Medical</td><td>망막 ViT 인과 attribution</td></tr>
<tr><td>925</td><td><a href='https://arxiv.org/abs/2611.11359'>NuJEV: Structured Visual Judgments for Consistent Nuclei Quantification</a></td><td>8</td><td>0</td><td>Medical</td><td>핵 정량화, 무관</td></tr>
<tr><td>926</td><td><a href='https://arxiv.org/abs/2611.11265'>DuSS-PET: Self-Supervised Low-Dose PET Reconstruction Using Pseudo-Dual-Domain Consistency Without Paired Data</a></td><td>8</td><td>0</td><td>Medical</td><td>저선량 PET</td></tr>
<tr><td>927</td><td><a href='https://arxiv.org/abs/2611.11071'>NanoNet: Ultra-Lightweight Network for MRI Brain Tumor Classification toward Edge AI</a></td><td>8</td><td>0</td><td>Medical</td><td>경량 뇌종양 분류</td></tr>
<tr><td>928</td><td><a href='https://arxiv.org/abs/2611.10728'>3D Segmentation in the Clinic: A Grand Challenge</a></td><td>8</td><td>0</td><td>Medical</td><td>3D 임상 분할 challenge</td></tr>
<tr><td>929</td><td><a href='https://arxiv.org/abs/2611.10348'>Guided Co-Attention with Adaptive Gating for Multimodal Medical Data Fusion</a></td><td>8</td><td>0</td><td>Medical</td><td>의료 멀티모달 융합</td></tr>
<tr><td>930</td><td><a href='https://arxiv.org/abs/2611.10260'>STAIRS: Staging the Inverse Problem via Admissible-Support Scheduling for Unrolled MRI Reconstruction</a></td><td>8</td><td>0</td><td>Medical</td><td>MRI 재구성</td></tr>
<tr><td>931</td><td><a href='https://arxiv.org/abs/2611.10236'>Anatomy-Preserving Unpaired Medical Image Translation via Shared Latent Anchoring</a></td><td>8</td><td>0</td><td>Medical</td><td>의료 영상 변환</td></tr>
<tr><td>932</td><td><a href='https://arxiv.org/abs/2611.10093'>Contrastive fine-tuning against stain and scanner bias improves robustness and downstream performance across pathology foundation models</a></td><td>8</td><td>0</td><td>Medical</td><td>병리 stain 편향</td></tr>
<tr><td>933</td><td><a href='https://arxiv.org/abs/2611.10062'>REFORM-3D: A Representation-Centric Evaluation Framework for 3D Medical Vision Foundation Models</a></td><td>8</td><td>0</td><td>Medical</td><td>3D 의료 FM 평가</td></tr>
<tr><td>934</td><td><a href='https://arxiv.org/abs/2611.10033'>Ultra-Lightweight 3D Medical Image Segmentation via Knowledge Distillation in Label-Scarce Domains</a></td><td>8</td><td>0</td><td>Medical</td><td>3D 의료 분할 distillation</td></tr>
<tr><td>935</td><td><a href='https://arxiv.org/abs/2611.10032'>GMD-Mamba: Lightweight 3D Medical Image Segmentation Using a Grouped Multi-Directional Mamba</a></td><td>8</td><td>0</td><td>Medical</td><td>3D 의료 Mamba 분할</td></tr>
<tr><td>936</td><td><a href='https://arxiv.org/abs/2611.10014'>Nanopath: Fast, Fair, Open Experimentation for Pathology Foundation Models</a></td><td>8</td><td>0</td><td>Medical</td><td>병리 FM 프레임워크</td></tr>
<tr><td>937</td><td><a href='https://arxiv.org/abs/2611.10007'>Representation Learning for 3D Brain Imaging: A Benchmark</a></td><td>8</td><td>0</td><td>Medical</td><td>3D 뇌 영상 benchmark</td></tr>
<tr><td>938</td><td><a href='https://arxiv.org/abs/2611.10003'>Reliability-Aware Benchmarking of Self-Supervised Learning in Histopathology Under 1-10% Label Regimes</a></td><td>8</td><td>0</td><td>Medical</td><td>병리 SSL benchmark</td></tr>
<tr><td>939</td><td><a href='https://arxiv.org/abs/2611.10001'>Optimized Car Damage Detection Using CNN and Object Detection Model</a></td><td>8</td><td>0</td><td>CV</td><td>차량 손상 검출</td></tr>
<tr><td>940</td><td><a href='https://arxiv.org/abs/2611.09953'>Confusion-Adaptive Margin Learning for Handwritten Letter Recognition: A Controlled Study on EMNIST Letters</a></td><td>8</td><td>0</td><td>CV</td><td>필기 문자 인식</td></tr>
<tr><td>941</td><td><a href='https://arxiv.org/abs/2611.10390'>A Computational Map of the Disaster Mental Health Research Landscape</a></td><td>8</td><td>0</td><td>Meta</td><td>PubMed 7,859편 재난 정신건강 논문을 LLM으로 분류한 문헌 지도로 로봇 무관</td></tr>
<tr><td>942</td><td><a href='https://arxiv.org/abs/2611.10168'>Key Institutional Considerations for Designing Effective Independent Verification Organizations</a></td><td>8</td><td>0</td><td>Policy</td><td>독립 검증 기관 설계 고려사항을 다룬 정책 논의로 기술 기여 없음</td></tr>
<tr><td>943</td><td><a href='https://arxiv.org/abs/2611.10150'>What Is the Value of AI-Involved Art? Evidence From a Juried In-Person Exhibition</a></td><td>8</td><td>0</td><td>HCI</td><td>AI 활용 미술의 가치 인식을 전시 참가자 209명으로 조사한 사회과학 연구</td></tr>
<tr><td>944</td><td><a href='https://arxiv.org/abs/2611.11258'>Auto-GlaKG: Automated Biomarker Reasoning for Explainable Glaucoma Detection</a></td><td>6</td><td>0</td><td>Medical</td><td>녹내장 KG reasoning</td></tr>
<tr><td>945</td><td><a href='https://arxiv.org/abs/2611.10174'>CXR-CMFA: A Cross-Modal Feature Aggregation Network for Chest X-Ray Pathology Classification</a></td><td>6</td><td>0</td><td>Medical</td><td>흉부 X선</td></tr>
<tr><td>946</td><td><a href='https://arxiv.org/abs/2611.11326'>Conditional Diffusion-Based Proxy Representation Recovery for BCVA Prediction with Missing SLO Modality</a></td><td>5</td><td>0</td><td>Medical</td><td>시력 예측, 무관</td></tr>
<tr><td>947</td><td><a href='https://arxiv.org/abs/2611.10744'>Writer-independent handedness identification from offline Bangla handwriting under controlled acquisition</a></td><td>5</td><td>0</td><td>CV</td><td>필기 손잡이 판별</td></tr>
<tr><td>948</td><td><a href='https://arxiv.org/abs/2611.10028'>Beyond Hash Matching: AI-Based Detection of Previously Unidentified CSAM and its Legal Implications in the EU</a></td><td>5</td><td>0</td><td>CV</td><td>CSAM 탐지</td></tr>
<tr><td>949</td><td><a href='https://arxiv.org/abs/2611.12796'>Smartphone-Enabled Depth-Aware Transillumination Imaging for Detection of Chicken Breast Fillet Myopathies in Chicken Fillets</a></td><td>5</td><td>0</td><td>CV</td><td>닭 가슴살 검출</td></tr>
</tbody></table>

</details>
