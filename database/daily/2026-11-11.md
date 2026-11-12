# 오늘의 arXiv Top 15: 2026-11-11 (수)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**

**신규 논문 수: 전체 476편 → 중복 제거 후 476편 (이번 평가 대상 476편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 117 |
| cs.LG | 134 |
| cs.RO | 57 |
| cs.CL | 63 |
| cs.AI | 105 |

---

## Top 15

### 1. Is Your Robot's Memory Just a Clock? Temporal Shortcuts in Memory-Augmented VLA Policies (82점)

[arXiv](https://arxiv.org/abs/2611.14488) · [PDF](https://arxiv.org/pdf/2611.14488) · [alphaXiv](https://www.alphaxiv.org/abs/2611.14488) (요약 있음) · [코드](https://github.com/bennidict23/memory-clock)

- **저자**: Chubin Zhang, Bo An
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 70점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> 시간 순으로 frame을 뽑아 기억하는 memory VLA가 반복 횟수 대신 흐른 시간을 보고 진행 정도를 판단한다는 것을, 아무 변화 없는 멈춤을 끼워 넣는 실험으로 보임. 5초 멈춤 두 번에 PickXtimes(정육면체를 K번 옮긴 뒤 버튼 누르기) 성공이 50회 중 47회에서 16회로 내려가고, 같은 멈춤을 memory에서 숨기면 45회로 돌아옴.

**무슨 문제인가**

물체를 세 번 옮긴 뒤 버튼을 누르는 과제처럼 현재 장면만으로 진행 정도를 알 수 없는 과제에서는 policy가 지나온 과정을 기억해야 함. 그래서 memory를 붙인 VLA가 늘고 있고, 가장 흔한 방식은 episode 전체에서 frame을 시간 간격대로 고르고 각 frame에 time step을 붙여 두는 것임. 실제 로봇은 planner나 운영자를 기다리며 멈추거나 손목을 움직였다가 제자리로 돌아오는 일이 잦음. 이런 구간은 시간을 쓰지만 과제 상태를 바꾸지 않으므로, 시간으로 채운 memory가 이 구간을 진행으로 셀 위험이 있는데 이를 직접 검증한 연구는 없었음.

**어떻게 푸나**

저자는 과제 상태를 바꾸지 않는 구간을 null event라 부르고, 멈춤(pause), 손목 흔들기(fidget), 물체 위 허공 잡기(air-grasp) 세 가지를 rollout 도중에 끼워 넣음. 같은 null event를 memory에 넣는 visible 조건과, 로봇은 똑같이 움직이되 해당 frame을 memory에서 빼고 time step도 진행시키지 않는 hidden 조건을 같은 episode 50개로 짝지어 비교함. 대상은 RoboMME(기억이 필요한 시뮬레이션 조작 benchmark)의 반복 세기 과제 두 개와, RoboMME가 공개한 π0.5 기반 memory VLA 계열(MME-VLA) 중 가장 강한 FrameSamp-Modul policy임. 이 계열의 memory(FrameSamp)는 32개 frame을 시간 간격대로 뽑고 각 frame에 절대 time step의 sinusoidal encoding을 붙임. 원인을 가리기 위해 time step만 s배로 바꾸는 실험, time encoding을 뺀 모델(NoClock)을 처음부터 학습하는 실험, 다른 memory 설계들과의 비교를 차례로 수행함. 마지막으로 로봇 자세·주변 장면·접촉이 이전 상태로 돌아온 구간을 frame 하나로 합치는 event index를 재학습 없이 test time에 적용함.

**결과**

- 공개 FrameSamp-Modul policy에서 5초 pause 두 번을 넣으면 PickXtimes 성공이 47회에서 16회로 내려감. SwingXtimes(정육면체를 두 목표 사이로 K번 옮기기)는 44회에서 10회로 내려감. hidden 조건에서는 각각 45회, 47회로 돌아오고, 실패는 대부분 반복을 덜 하고 버튼을 일찍 누른 경우임.
- null event 없이 time step만 1.5배로 늘리면 PickXtimes 성공이 47회에서 18회로 내려가고 실패 32건이 모두 이른 누름임. 0.5배로 줄이면 성공이 24회이고 실패 대부분(23건)이 반복을 더 한 경우임.
- time encoding을 뺀 NoClock도 pause에서 성공이 PickXtimes 42회에서 21회, SwingXtimes 47회에서 14회로 내려감. pause 없이 똑같은 frame으로 된 묶음을 memory 12칸에 끼워 넣기만 해도 PickXtimes 성공이 42회에서 24회로 내려가서, frame이 memory 칸을 차지하는 것만으로 같은 실패가 생김을 보임.
- event index는 time encoding을 유지한 채 처음부터 학습한 CLOCK checkpoint에 test time으로 적용함. 그 결과 pause에서 PickXtimes 17회가 34회로, SwingXtimes 10회가 30회로 오르고, SwingXtimes air-grasp는 13회에서 43회로 오름. null event 없는 PickXtimes는 41회에서 36회로 내려감. pause를 넣은 데이터로 재학습하는 방법은 null event 없는 SwingXtimes 성공을 46회에서 19회로 떨어뜨려 해결책이 되지 못함.

**한계**

모든 실험이 시뮬레이션이고 null event도 스크립트로 만든 것이라, 실제 배치에서 이런 구간이 얼마나 자주 생기는지는 재지 않음. event index의 검출기는 simulator의 로봇 silhouette, gripper 폭, 외력 신호를 쓰고 판정 기준도 null event를 만든 방식과 같아서, 실로봇에서 쓸 수 있는 방법으로 보인 것은 아님. 인과 분석은 MME-VLA 계열 하나에 집중되어 있고, 대부분 모델은 seed 하나로 학습했으며 같은 조건을 두 번 돌려도 50회 중 8회까지 차이가 났음.

**누리랩 연구와의 연결**

- robot memory 연구에서 memory가 사건을 세는지 시간을 세는지 가르는 평가 절차(visible/hidden 비교, time step 배율 조정, 똑같은 frame 묶음 삽입)를 바로 가져다 쓸 수 있음. 우리가 만드는 memory VLA를 RoboMME 등에서 평가할 때 같은 probe를 추가할 근거가 됨.
- 이른 버튼 누름이라는 실패가 memory 구성에서 생긴다는 진단은 failure detection/diagnosis 관점과 이어짐. 실로봇 센서로 상태 변화(물체 이동, 접촉)를 검출해 memory를 쌓는 문제는 object-centric representation이나 scene graph 연구와 연결되는 후속 과제임.

*대표 그림: 위쪽(a)은 SwingXtimes 장면의 pause, fidget, air-grasp 전·중·후 frame과, null event frame이 32개 frame memory에 들어가는 visible 조건과 빠지는 hidden 조건을 그림. 아래쪽(b)은 50회 중 성공 횟수로, PickXtimes에서 visible 16회 대 hidden 45·46회, SwingXtimes에서 visible 10·10·23회 대 hidden 47·45·47회를 보여 줌.*

---

### 2. ExRL: Sample-Efficient Online Adaptation of Long-Chunk Policies via Execution Length Control (78점)

[arXiv](https://arxiv.org/abs/2611.13482) · [PDF](https://arxiv.org/pdf/2611.13482) · [alphaXiv](https://www.alphaxiv.org/abs/2611.13482) (요약 있음) · [프로젝트 페이지](https://exrl-project.github.io)

- **저자**: Xu Luo, Jiaying Yang, Hao Wu, Junlin Xie, Zijin Hong, Ji Zhang, Lianli Gao, Jingkuan Song
- **분야**: RL · robotics relevance 8/10 · 1차 스크리닝 66점
- **학회**: IEEE 학술지 계열 양식 (추정) · 근거: IEEE 2단 양식, 21쪽
- **읽은 원문**: PDF 전문

> 긴 action chunk를 내는 policy를 online RL로 고칠 때, action은 그대로 두고 chunk 중 몇 개를 실행할지만 배우게 해서 필요한 online 데이터를 줄임. 고정된 π0.5를 LIBERO 과제 하나에서 200,000 environment step 안에 성공률 거의 0%에서 90% 넘게 올림.

**무슨 문제인가**

π0.5, π0-FAST 같은 최근 VLA는 한 번에 20~50 step 길이의 action chunk를 예측하고 open-loop로 실행함. 이런 policy도 실제 배치에서는 demonstration 범위 밖에서 실패하므로 online RL로 고칠 필요가 있음. 그런데 chunk 전체나 그 latent noise를 최적화하는 기존 RL은 chunk가 길수록 최적화할 차원이 커져서 online 데이터가 많이 듦. 실로봇에서는 데이터 수집이 느리고 비싸므로, chunk 길이와 무관하게 차원이 작은 adaptation 방법이 필요함.

**어떻게 푸나**

ExRL(Execution at the Right Length)은 base policy를 고정하고, 예측된 chunk의 앞쪽 몇 개를 실행할지 정하는 작은 policy만 학습함. 입력은 현재 state와 base policy가 낸 chunk이고, 출력은 1부터 H(chunk 길이) 사이의 정수 k임. 로봇은 앞의 k개 action을 실행한 뒤 새 state에서 base policy에 다시 chunk를 요청함. k개 step 동안의 reward를 할인해 더하고 다음 state 가치는 γ^k로 할인하는 duration-aware TD target으로 critic을 학습함. 구현은 critic만 쓰는 ExRL-Q와 discrete SAC를 쓰는 ExRL-SAC 두 가지이고, 둘 다 CQL(conservative Q-learning)로 과대평가를 억제함. 선택 사항으로 성공한 online rollout을 H-step 단위로 잘라 base policy를 behavior cloning으로 다시 학습시킬 수 있음(Online BC). 사람 demonstration도 임의 구간을 가상의 chunk로 보고 길이별 prefix를 replay buffer에 넣어 쓸 수 있음.

**결과**

- LIBERO(시뮬레이션 조작 과제 모음)의 한 과제에서 chunk 길이 50인 고정 π0.5의 성공률이 200,000 environment step 안에 거의 0%에서 90% 넘게 오름. 같은 방식이 π0, π0-FAST, world action model인 Cosmos Policy에도 그대로 적용됨.
- Robomimic Tool Hang(도구를 고리에 거는 장기 과제)에서 Diffusion Policy에 ExRL-SAC를 쓰면 성공률이 90%를 넘음. 같은 조건에서 latent noise를 고치는 DSRL, action에 residual을 더하는 ResFiT·DICE-RL 등 다른 baseline은 모두 20% 안팎이나 그 아래에 머묾.
- 실로봇에서 chunk 길이 50인 π0.5를 고정한 채 ExRL-Q로 과제 4개를 학습함. 고정 k 중 가장 좋은 설정 대비 cube 쌓기는 9/20에서 17/20, 옷 접기는 12/20에서 17/20으로 오름. 전원 플러그 꽂기는 10/25에서 22/25, 부품 정리는 완료 단계 69/125에서 104/125로 오름.
- Robomimic Square에서 ExRL-Q가 고른 실행 길이 집합은 그대로 두고 어느 state에 어느 길이를 쓸지만 무작위로 뒤섞으면 Diffusion Policy 성공률이 95.8%에서 37.5%로 내림. 어떤 길이를 쓰는지보다 언제 쓰는지가 성능을 정한다는 해석을 뒷받침함.

**한계**

실로봇 실험은 base policy를 고정한 채로만 했고 Online BC를 쓰지 않아, base policy가 내지 못하는 action은 만들 수 없음. 과제마다 따로 학습했고 multi-task 학습, 처음 보는 과제로의 일반화, real-time chunking 같은 비동기 추론과의 결합은 시험하지 않음. 시뮬레이션 base checkpoint는 RL로 오를 여지가 있는 것을 일부러 골랐으므로, 이미 잘 학습된 policy에서 이득이 얼마인지는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- VLA를 다시 학습하지 않고 실행 시점에 언제 replanning할지만 배워 성능을 올린 사례임. test-time optimization과 VLA online adaptation 연구에서 action 수정 계열 방법과 비교할 baseline으로 쓸 수 있음.
- 학습된 policy가 물체 근처에서 짧게 실행하고 부적절한 chunk를 거르는 행동을 보임. 이 critic 값을 chunk 단위 failure detection이나 recovery 시점 판단 신호로 쓰는 방향을 시험해 볼 수 있음.

*대표 그림: 실험에 쓴 시뮬레이션 과제 장면을 모은 그림이며 측정 결과는 담겨 있지 않음. 위 줄은 Robomimic 5개(Lift, Can, Square, Tool Hang, Transport), 아래 줄은 Adroit 손 조작 4개(Door, Hammer, Pen, Relocate)와 LIBERO pick and place 과제임.*

*영상: [저자가 올린 실로봇 옷 접기 rollout 영상으로, 잡는 구간에서는 실행 길이가 짧고 천을 들어 옮기는 구간에서는 길어지는 모습을 담음.](https://blog-media.assets.alphaxiv.org/videos/01a1c871-3291-7cfd-a337-1bce10c81139/1490ec19-4b91-4e46-b04b-98f194ede5bf) (alphaXiv 요약에서 가져옴)*

---

### 3. LaST0.5: A Generalist World Action Model with Interaction-Centric Latent Reasoning (74점)

[arXiv](https://arxiv.org/abs/2611.14048) · [PDF](https://arxiv.org/pdf/2611.14048) · [alphaXiv](https://www.alphaxiv.org/abs/2611.14048) (요약 있음)

- **저자**: Xuheng Zhang, Yiming Zhang, Jialin Gao, Hao Chen, Jiaming Liu, Ji Li, Runzhong Huang, Yinxi Wang 외 9명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 68점
- **읽은 원문**: PDF 전문

> video world model이 예측한 미래 장면과 action 생성 사이에, 로봇과 물체의 접촉에 맞춘 latent 단계를 끼운 World Action Model을 제안함. 실로봇 양팔 과제 4개 평균 성공률이 63.8%로 π0.5의 52.5%보다 높음.

**무슨 문제인가**

World Action Model(WAM: 미래 장면 예측과 로봇 action 생성을 함께 하는 policy)은 미래 frame을 먼저 만들고 inverse dynamics로 action을 구하거나, 둘을 한 모델에서 같이 예측함. 두 방식 모두 장면 전체의 변화를 맞히도록 학습된 표현을 action 생성에 그대로 넘김. 저자들은 이 표현이 배경 같은 넓은 장면 특징에 끌려서 gripper와 물체 사이의 국소 접촉 정보를 덜 담는다고 봄. 또 world model이 그린 미래가 틀리면(예: 그릇을 못 집은 장면) 그 미래에 맞춘 action이 closed-loop에서 오류를 쌓음.

**어떻게 푸나**

LaST0.5는 world expert, latent expert, action expert 셋을 Mixture-of-Transformers 안에 두고 미래 영상, latent, action 순서로 추론함. world expert는 Cosmos-Predict2.5-2B이며 과거 5 frame과 지시문을 받아 미래 12 frame을 denoising으로 만듦. latent expert(Janus에서 초기화)는 learnable query로 이 미래 표현에서 4 frame 구간마다 하나씩, 모두 3개의 latent token을 한 번에 뽑음. 학습 target은 구간 끝 frame에 end-effector 궤적을 투영한 2D 곡선과 Grounding DINO로 찾은 대상 물체 box를 그려 넣고 SigLIP으로 encoding한 값이며, cosine loss로 맞춤. 이 그림 표시는 학습 데이터 준비 때만 쓰고 추론 때는 쓰지 않음. action expert는 미래 장면과 latent를 받아 flow matching으로 12 step action chunk를 출력함. AWAT(Adaptive World-to-Action Transfer)는 world expert feature 위의 value head로 구간별 진행도(episode 안에서의 시점 비율)를 예측하고, 진행도가 오르는 구간의 action만 실행함. 진행도가 내려가면 실행을 멈추고 다시 관측하며, 첫 구간부터 이전 값보다 낮으면 미래를 여러 개 sampling해 value가 가장 높은 것을 고름.

**결과**

- 실로봇 Tianji Marvin 양팔 과제 4개(가방 지퍼 잠그기, 물건 정리, 나사 체결, 상자 포장)에서 과제당 20회 평가함. 전체 과제 완료 기준 평균 성공률이 π0.5 52.5%, Cosmos Policy 43.8%, LaST0(latent 시공간 chain-of-thought를 쓰는 이전 VLA) 43.8% 대비 63.8%임. 나사 삽입 단계 성공률은 50%로 π0.5의 30%보다 높음.
- 위치를 바꾼 out-of-distribution 평가(가방, 정리 과제 2개)에서 평균 성공률이 π0.5 15%, Cosmos Policy 17.5% 대비 40%임. 물체를 바꾼 조건에서는 π0.5와 같은 55%임.
- RLBench(시뮬레이션 Franka 조작 과제, 여기서는 10개 선택) 평균 성공률이 이전 최고인 LaST0 82%, Cosmos Policy 77% 대비 88%임(3회 실행 평균, 표준편차 3.0). AWAT를 빼면 85%임.
- LIBERO-Spatial은 시뮬레이션 조작 benchmark LIBERO의 4개 suite 중 하나임. 여기서 latent target의 궤적 곡선과 물체 box를 모두 빼면 성공률이 99.6%에서 98.6%로 내리고, latent expert 자체를 빼면 97.8%로 내림. LIBERO 4개 suite 평균은 99.5%로 Cosmos Policy 98.5%보다 높음.

**한계**

LIBERO 수치는 학습 중 가장 좋았던 값이고 반복 실행 평균이 아니며, 이미 99%대라 ablation 차이가 1퍼센트포인트 안팎임. RLBench의 AWAT 유무 차이(88% 대 85%)는 표준편차 3.0과 비슷한 크기임. 14k시간이 넘는 로봇 데이터 사전학습의 기여와 latent expert의 기여를 나눈 실험, 추론 속도나 resampling 비용, 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- 진행도 value가 내려가면 실행을 끊고 미래를 다시 sampling하는 AWAT는 world model 기반 failure detection과 test-time 재계획의 간단한 형태임. 우리 failure detection/recovery 연구에서 진행도 회귀 기준의 baseline으로 쓸 수 있음.
- 궤적과 affordance box를 그려 넣은 frame을 latent target으로 쓰는 방식은, world model 표현을 manipulation에 필요한 접촉 영역으로 좁히는 방법임. object-centric 표현을 VLA에 넣는 연구와 비교 대상이 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 개요 그림에 결과 막대그래프를 붙인 그림임. 왼쪽은 장면 변화에서 바로 action을 예측하는 기존 WAM과 상호작용 단계(motion, affordance cue)와 진행도 값을 더한 LaST0.5를 보여 줌. 오른쪽은 실로봇 4개 과제와 LIBERO, RLBench 성공률을 π0.5, LaST0, Cosmos Policy와 비교함.*

---

### 4. DexSeed: Expanding Human Hand-Object Interactions into Robot Demonstrations for Dexterous Policy Learning (74점)

[arXiv](https://arxiv.org/abs/2611.14092) · [PDF](https://arxiv.org/pdf/2611.14092) · [alphaXiv](https://www.alphaxiv.org/abs/2611.14092) (요약 있음) · [프로젝트 페이지](https://robbyant-research.github.io/DexSeed/)

- **저자**: Huaijin Pi, Zehong Shen, Yong Wang, Kechun Xu, Changpeng Wang, Dingkun Wei, Xueyang Wang, Wenjia Wang 외 3명
- **분야**: Manipulation · robotics relevance 9/10 · 1차 스크리닝 66점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> 사람 손-물체 상호작용 19개 sequence를 잡는 방식(grasp)은 유지한 채 물체 모양과 팔 궤적을 바꿔 시뮬레이션에서 실행시키고, 성공한 rollout 25,270개로 dexterous VLA를 학습함. 이 데이터만으로 학습한 VLA는 layout·모양·외관이 모두 처음인 시뮬레이션 조건에서 성공률 91.25%, 실로봇 8개 grasp mode 평균 성공률 55%를 보임.

**무슨 문제인가**

dexterous hand용 VLA를 학습하려면 팔과 손가락 동작, 카메라 관측, 언어 지시가 짝지어진 demonstration이 많이 필요함. 기존 demonstration 생성 방법(MimicGen, DexMimicGen 등)은 teleoperation으로 모은 시연을 출발점으로 삼는데, 관절이 많은 손을 원격 조종하며 접촉을 유지하는 일은 비용이 큼. 사람 손-물체 dataset(GRAB 등)을 로봇으로 옮기는 retargeting과 physics-based imitation 연구도 있지만, 주로 주어진 상호작용 하나를 재현하는 데 그침. VLA 학습용으로 쓰려면 물체 모양과 집고 놓는 위치를 바꿔도 같은 grasp가 유지되고, 팔 추종 오차가 있어도 실제로 실행되는 데이터여야 함.

**어떻게 푸나**

DexSeed는 사람 sequence를 grasp mode별로 묶고, 각 sequence를 다양한 로봇 demonstration으로 늘린 뒤 시뮬레이션에서 실행 가능한 것만 남김. 먼저 물체가 움직이기 시작하는 frame에서 손가락 굽힘, 관절 위치, 물체 표면까지의 벡터 등을 담은 170차원 grasp descriptor를 계산하고, 거리 기준으로 묶어 8개 대표 mode를 사람이 고름. mode마다 GPT로 잡는 방법을 설명하는 문장을 만들고, 같은 mode의 데이터는 모두 이 문장을 공유함. 다음으로 InteractionMesh retargeting으로 손 landmark 21개와 물체 표면 anchor를 Delaunay 사면체로 연결함. 각 꼭짓점의 이웃 대비 상대 위치(Laplacian coordinate)가 사람 시연과 같아지도록 Wuji 로봇 손의 wrist pose와 20-DoF 손가락을 최적화함. 다른 물체로 옮길 때는 Diff3F 특징으로 대응점을 찾아 대상 물체를 정렬함. 이어 시작 wrist pose, 물체 위치, 놓을 위치를 샘플링해 접근·집기·운반·놓기·후퇴 궤적을 만들고, IK 해가 없는 것은 버림. Franka 팔은 이 관절 궤적을 PD 제어로 따라가고, RL로 학습한 손가락 policy가 542차원 관측을 받아 20차원 residual action을 냄. 성공한 rollout을 실제 작업 공간을 복원한 3D Gaussian Splatting 장면에서 head-view와 wrist 카메라 영상으로 렌더링하고, 행동·grasp 설명과 짝지어 LingBot-VLA를 fine-tuning함.

**결과**

- 팔을 붙인 채 평가한 physics-based 실행(FR3 팔이 wrist 궤적을 추종)에서 성공률이 95.50%임. 같은 policy를 떠 있는 손(floating hand)으로 학습한 w/o Arm 변형은 28.02%이고, 사람 손 시연을 물리 시뮬레이션에서 로봇 손으로 옮기는 기존 방법인 ManipTrans는 34.25%, Dexplore는 24.81%임. 이 세 방법은 떠 있는 손으로 평가하면 71.32~98.04%여서, 팔 추종 오차를 학습에 넣은 것이 차이를 만든 것으로 보임.
- 시뮬레이션 pick-and-place에서 layout·물체 모양·외관이 모두 처음인 조건(grasp mode 8개 × 10회 = 80회)의 VLA 성공률이 91.25%임. 같은 VLA를 ManipTrans로 만든 데이터로 학습하면 51.25%, Dexplore 데이터는 32.50%, 물리 실행 없이 kinematic reference를 렌더링한 데이터는 5.00%임.
- grasp 설명 문장을 빼고 과제 지시만 주면 같은 조건 성공률이 70.00%로 내림. 같은 사과에 G1(비스듬히 옆에서 손 전체로 잡기)과 G4(위에서 손 전체로 잡기) 지시를 줬을 때 10회 모두 요청한 grasp에 더 가까운 손가락 자세가 나왔고, 설명이 없으면 10회 모두 G1 쪽으로 감.
- 실로봇(Franka 팔 + Wuji 손)에서 mode마다 물체 1개로 10회씩 평가함. 성공률은 mode별로 20%(handle threading)에서 80%(two-finger hook) 사이이고 8개 평균은 55%임. 실로봇 action demonstration은 쓰지 않음.

**한계**

실로봇 평가는 mode당 물체 1개, 10회뿐이라 처음 보는 물체로의 일반화는 실로봇에서 보이지 않음. 원천 데이터는 GRAB의 pick-and-place 19개 sequence이고, 대표 mode 선택은 사람이 함. 과제가 집고 옮기기에 한정되어 in-hand manipulation이나 양손 작업은 다루지 않았고, source sequence마다 손가락 policy를 따로 학습해야 함.

**누리랩 연구와의 연결**

- dexterous manipulation용 VLA 데이터를 teleoperation 없이 사람 시연과 시뮬레이션, 3DGS 렌더링으로 만드는 경로를 보임. 손 장착 VLA나 grasp 조건부 policy 연구에서 데이터 생성 기준선으로 쓸 수 있음.
- 운동학적으로 맞는 reference도 팔 추종 오차가 들어가면 실패한다는 결과(kinematic 데이터 5.00%, w/o Arm 28.02%)는 failure detection에서 실행 단계 실패 원인을 나눌 때 참고가 됨.

*대표 그림: 왼쪽은 사람이 빨간 사과를 위에서 잡는 시연과 옆에서 감싸 잡는 시연이 DexSeed를 거쳐 로봇 손 렌더링 데이터로 바뀌는 과정임. 오른쪽은 학습된 VLA가 실로봇에서 사과·노란 물체 위에서 잡기, 사과·병 옆에서 감싸 잡기, 빨간 도넛형 물체 두 손가락 걸기, 머그 손잡이에 손가락 넣기를 하는 사진임.*

---

### 5. OnlyAct: Extracting Action Representations from Foundation Models for World Models (74점)

[arXiv](https://arxiv.org/abs/2611.14420) · [PDF](https://arxiv.org/pdf/2611.14420) · [alphaXiv](https://www.alphaxiv.org/abs/2611.14420) (요약 있음) · [프로젝트 페이지](https://runjiali-rl.github.io/onlyact/) · [코드](https://github.com/runjiali-rl/onlyact)

- **저자**: Runjia Li, Minghao Chen, Junyu Xie, Philip Torr, Andrea Vedaldi, Tomas Jakab
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 76점
- **학회**: NeurIPS 2026 채택 · 근거: 1쪽에 "40th Conference on Neural Information Processing Systems (NeurIPS 2026)"
- **읽은 원문**: PDF 전문

> action label 없는 영상에서 action을 뽑을 때 encoder를 처음부터 학습하지 않고, 사전학습된 V-JEPA 2를 contrastive 학습으로 action 쪽으로 조정함. 연속 action dataset 12개의 linear probe 평균 R²가 0.490으로, 기존 latent-action 모델 최고값 0.211보다 높음.

**무슨 문제인가**

action-conditioned video world model을 학습하려면 action label이 필요하지만, label이 붙은 영상은 적고 로봇 관절각과 게임 입력처럼 형식도 서로 다름. 그래서 Genie, AdaWorld 같은 latent-action 모델은 label 없는 영상의 프레임 쌍에서 latent action을 스스로 학습함. 이 모델들은 이전 프레임과 latent로 다음 프레임을 복원하게 하고, latent 크기를 작게 제한해 장면 정보가 latent에 들어가지 않게 함. 이 제한을 조이면 action의 세밀한 차이가 사라지고 풀면 장면 정보가 새어 들어가며, 처음부터 학습한 encoder는 학습 때 못 본 domain에 잘 일반화되지 않음.

**어떻게 푸나**

OnlyAct는 V-JEPA 2(대규모 영상으로 사전학습된 ViT-L video encoder)를 action encoder로 씀. 두 프레임을 2-frame clip 하나로 묶어 encoder에 넣고, 출력 token을 평균한 뒤 고정된 random projection으로 640차원으로 줄이고 정규화함. 사전학습 가중치는 고정하고 LoRA adapter만 contrastive loss(InfoNCE)로 학습함. positive는 optical flow로 찾은 움직이는 영역을 잘라 다른 장면의 배경 위 다른 위치에 붙여 만들어서, 움직임은 같고 장면은 다르게 함. 카메라가 움직이는 영상에서는 이 방식이 성립하지 않아 같은 프레임 쌍에 색 변환만 다르게 준 것을 positive로 씀. hard negative는 같은 영상의 겹치지 않는 다른 시간 구간에서 뽑아, 장면은 같고 움직임은 다른 쌍으로 씀. 학습이 끝난 encoder를 고정하고, 연속 프레임 쌍마다 뽑은 action embedding을 조건으로 AdaWorld 구조의 autoregressive video world model을 학습함. 데모 영상의 action을 새 장면에 그대로 옮기거나(action transfer), 소량의 label로 실제 action을 이 공간에 대응시켜 조종함(real-action control).

**결과**

- encoder 학습에 쓴 168K 프레임 쌍으로 비교 모델도 다시 학습해 같은 조건에서 비교함. linear probe로 실제 action을 맞히는 실험에서 평가 dataset 13개 중 연속 action이 있는 12개의 평균 R²가 OnlyAct 0.490, DreamDojo(기존 latent-action 모델 중 최고) 0.211, AdaWorld 0.067임. 나머지 하나인 Procgen은 이산 action이라 평균에서 빠짐. 13개 중 10개 dataset은 encoder 학습 때 못 본 것임.
- 같은 조건에서 adaptation 전의 V-JEPA 2는 평균 R² 0.347이고, RoboCasa에서 -0.368로 내려감. adaptation 후 RoboCasa는 0.322로 오름. 장면 정보 누출 LPIPS(action embedding만으로 다음 프레임을 복원한 값, 높을수록 누출이 적음)는 OnlyAct 0.304로, adaptation 전 V-JEPA 2의 0.275보다 높고 DreamDojo 0.299와 비슷함.
- 같은 world model 구조와 data로 학습해, 한 영상의 action으로 다른 장면을 움직인 뒤 생성 영상과 원본의 optical flow 방향 cosine을 잼. encoder가 못 본 RLBench(시뮬레이션 로봇 조작 benchmark)에서 OnlyAct 0.686, DreamDojo 0.572이고, 5개 설정 모두에서 OnlyAct가 가장 높음.
- 소량 label로 fine-tuning한 뒤 지시한 action이 생성 영상에 나타나는지 재는 Follow 점수가 4개 domain(DMLab, Minecraft, Habitat, nuScenes 자율주행 영상) 모두에서 가장 높음. nuScenes에서 0.928 대 DreamDojo 0.722임. Habitat에서는 Control 점수(지시한 action과 다른 action으로 생성한 영상의 PSNR 차이)의 차이가 noise 범위 안임.

**한계**

모든 평가가 영상 생성과 probe 같은 offline 실험이고, 실로봇 policy나 closed-loop 제어 결과는 없음. world model 학습과 fine-tuning은 계산량 때문에 run 하나씩만 돌려서 학습 seed에 따른 분산은 보고되지 않음. 장면 교체 positive는 카메라가 고정된 영상에서만 쓸 수 있어, 주행이나 1인칭 영상에서는 색 변환만으로 장면 불변성을 학습함.

**누리랩 연구와의 연결**

- world model과 VLA를 action label 없는 대규모 영상으로 사전학습할 때 latent action encoder를 고르는 기준이 됨. 사람 영상과 로봇 영상의 action을 한 공간에 놓는 cross-embodiment 실험의 출발점으로 쓸 수 있음.
- action 표현력, 장면 누출, action transfer 세 축의 평가 방식은 다른 latent action이나 world model 조건 신호를 비교할 때 그대로 가져다 쓸 수 있음.

*대표 그림: 왼쪽 네 줄의 입력 영상(손 동작, 식물 앞 카메라 이동, 게임 화면 등)에서 OnlyAct가 action embedding을 뽑고, 오른쪽에서 다른 장면의 첫 관측에 그 action을 적용해 생성한 미래 프레임을 보여 줌. 가운데 action embedding은 아이콘으로 그린 개념도이고, 측정 결과가 아닌 정성적 예시임.*

---

### 6. CIALLO: Learning Shared Intent Representations for Cross-Embodiment Manipulation (74점)

[arXiv](https://arxiv.org/abs/2611.13732) · [PDF](https://arxiv.org/pdf/2611.13732) · [alphaXiv](https://www.alphaxiv.org/abs/2611.13732) (요약 있음)

- **저자**: Choo Sin Wai, Dake Zhong, Jingye Zhang, Zhifang Liu, Siyao Xiao, Zirong Ding, Yuhong Zhang, Kangjie Chen 외 5명
- **분야**: Manipulation · robotics relevance 8/10 · 1차 스크리닝 60점
- **읽은 원문**: PDF 전문

> 로봇마다 다른 action 좌표계를 짧은 구간의 공통 intent 표현으로 압축하고 로봇별 embedding으로 다시 풀어내는 action codec CIALLO를 제안함. 새 로봇은 10초 이하 녹화 하나로 embedding만 맞춘 뒤 codec을 고정하고 policy를 학습하며, 실로봇 2대에서 과제 3개씩, 6개 과제·로봇 조합의 평균 성공률이 76.7%로 fully finetuned π0의 70.0%보다 높음.

**무슨 문제인가**

로봇 demonstration에 담긴 조작 지식을 다른 로봇에 옮기려면 서로 다른 control interface를 이어 줄 표현이 필요함. 같은 동작도 end effector 변위나 joint angle로 기록되고, action 차원과 팔 개수와 제어 주기가 로봇마다 다름. 기존 방법은 통합 action 공간에 padding을 하거나 embodiment별 module을 붙여 이질적인 데이터를 받음. 그러나 action 복원만 학습하면 로봇이 달라도 비슷한 행동이 비슷한 표현을 갖도록 강제되지 않음.

**어떻게 푸나**

CIALLO(Cross-embodiment Intent All in One Space)는 action chunk를 2개 token(폭 512)짜리 intent로 압축하는 action codec임. 입력 경로는 세 개임. 첫째는 action chunk와 proprioception임. 둘째는 frozen DINOv2로 본 현재 frame과 미래 frame의 변화임. 셋째는 frozen BERT로 읽고 현재 frame으로 grounding한 instruction임. 세 경로의 intent는 InfoNCE contrastive loss로 맞추고, 하나의 공유 action decoder가 각 intent에서 실제 action을 L1 loss로 복원하게 함. 로봇마다 128차원 essential vector E와 arm·axis embedding을 두고, 이를 conditional normalization으로 encoder와 decoder에 넣음. decoder는 목표 실행 시각과 action schema(출력할 action 차원과 팔·축 구성)를 입력으로 받아 차원, 제어 주기, 단일·양팔 구성이 달라도 같은 가중치로 출력함. 각 action 값은 [-1,1]의 256개 bin에 대한 softmax 기댓값으로 한 번에 계산함. policy인 Qwen-CIALLO는 Qwen3.5-4B가 관측과 instruction에서 intent를 예측하고, frozen action encoder의 intent와 cosine loss로, 복원 action과 L1 loss로 학습함. 새 로봇은 공유 가중치를 고정한 채 E와 arm·axis embedding만 10초 이하 녹화 하나로 약 30분(GPU 1장) 맞추고, 이후 codec 전체를 고정함.

**결과**

- 실로봇 SO-101과 단일팔 Piper(둘 다 pretraining에 없던 구성)에서 과제당 demonstration 20개, 평가 20회로 3개 과제를 비교함. 6개 과제·로봇 조합 평균 성공률은 calibration 후 codec을 고정한 Qwen-CIALLO가 76.7%, fully finetuned π0가 70.0%임. 얇은 드라이버를 잡아 목어를 치는 과제에서 70% 대 35%(SO-101), 40% 대 20%(Piper)로 차이가 났고, 물병 놓기는 π0가 5~10퍼센트포인트 높았으며 맥주 따르기는 같음.
- essential vector가 실제로 쓰이는지 보려고 held-out 2,048개 샘플에서 다른 로봇의 E로 바꿔 넣음. action에서 action을 복원하는 MAE가 0.00761에서 encoder만 바꾸면 0.04506, decoder만 바꾸면 0.19124로 오름. 시각 intent 경로는 encoder E만 바꿀 때 0.01853에서 0.02189로 덜 오름.
- LIBERO(시뮬레이션 조작 과제 4개 suite) 평균 성공률은 policy 10k step 학습으로 97.3%이며, 30k step을 쓴 CLAP-RF의 97.2%, OpenVLA-OFT의 97.1%와 거의 같음. 같은 checkpoint를 추가 학습 없이 LIBERO-Plus(카메라·조명·배경 등 7종 교란을 넣은 LIBERO)에 넣으면 80.8%로 DreamWAM의 74.6%보다 높음.
- RoboTwin 2.0(양팔 시뮬레이션 과제 50개) clean-to-clean 조건에서 50개 과제를 함께 학습한 checkpoint 하나가 52.7%로, 함께 학습한 StarVLA 46.5%, 과제별로 학습한 π0 46.4%보다 높음.

**한계**

실로봇 실험은 로봇 2대, 과제 3개, 조건당 20회라 통계적 차이를 말하기 어렵고, π0와의 비교는 backbone·pretraining·finetuning 방식이 모두 달라 codec의 효과만 떼어 보여 주지 못함. 시뮬레이션에서는 action decoder도 함께 finetuning해서, codec을 고정한 채 쓰는 조건은 실로봇에서만 확인됨. LIBERO 비교는 baseline마다 seed 수와 출처가 다르고 Qwen-CIALLO는 seed 1개 결과이며, 코드 공개 주소는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- VLA의 action head를 로봇별 embedding과 공통 intent로 나누는 설계라, 새 로봇에 VLA를 옮길 때 action 표현만 짧게 calibration하는 manipulation 실험의 비교 대상으로 쓸 수 있음.
- action, 시각 변화, grounding된 언어가 같은 intent 공간에 놓이므로, 예측 intent와 관측된 시각 변화 intent의 불일치를 failure detection 신호로 쓰는 실험을 해 볼 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림으로, A에는 세 encoder가 공통 intent 공간에 넣은 표현을 공유 decoder가 action으로 복원하는 pretraining이 있음. B에는 Qwen3.5-4B의 intent 예측 학습이, C에는 10초 이하 녹화로 E와 arm·axis embedding을 약 30분 맞추는 절차와 SO-101·Piper 성공률 막대가 있음.*

---

### 7. UGG: Unified Generative Geometry Model (74점)

[arXiv](https://arxiv.org/abs/2611.14440) · [PDF](https://arxiv.org/pdf/2611.14440) · [alphaXiv](https://www.alphaxiv.org/abs/2611.14440) (요약 있음) · [프로젝트 페이지](https://ugg-model.github.io) · [코드](https://github.com/amanikiruga/UGG)

- **저자**: Amani Kiruga, Zhiyi Li, Ruojin Cai, Hansen Lillemark, Xiaoshan Wu, Ayush Tewari, Yilun Du
- **분야**: 3D Vision · robotics relevance 7/10 · 1차 스크리닝 66점
- **학회**: NeurIPS 2026 채택 · 근거: comments에 "Accepted at NeurIPS 2026. 31 pages, 7 figures, 6 tables. Project page: this https URL"
- **읽은 원문**: PDF 전문

> RGB video, depth, camera pose를 한 diffusion 모델에서 같이 다루고, 어떤 modality를 noise로 비우느냐로 영상 생성과 기하 추정을 모두 처리함. 첫 프레임과 마지막 프레임만 주는 RealEstate10K(실제 촬영 영상 데이터셋) camera pose 추정에서 translation 방향 오차가 가장 좋은 baseline의 39.8도에서 8.3도로 내려감.

**무슨 문제인가**

장면의 depth와 camera pose를 추정하는 feedforward 모델은 한 번에 정답 하나만 내놓으므로, 관측이 적거나 학습 분포를 벗어나면 틀리기 쉬움. 반대로 video generation 모델은 빠진 장면을 그럴듯하게 채우지만 3D 기하와 맞지 않는 영상을 만들기도 함. 두 계열을 잇는 기존 연구(Geo4D, One4D 등)도 입력과 출력 방향이 정해져 있어서, 생성과 추정을 같은 장면 모델의 서로 다른 질의로 다루지 못했음. 또 기하 추정 모델은 RGB, depth, pose가 모두 갖춰진 데이터를 요구하는 경우가 많음.

**어떻게 푸나**

UGG(Unified Generative Geometry model)는 프레임마다 RGB, depth, camera를 같은 해상도의 이미지 형태로 맞춤. camera는 픽셀마다 시선 방향과 moment를 담은 6차원 Plücker ray map으로 바꿈. 세 modality의 token은 modality별 projection과 feed-forward layer를 따로 가지고, self-attention만 공유하는 mixture-of-transformers에 들어감. 각 token은 modality와 시간 위치마다 다른 noise level을 가지며, 이는 token이나 frame마다 noise level을 따로 주는 Diffusion Forcing을 modality 축으로 넓힌 것임. 관측된 token은 noise 0으로 고정하고 빠진 token만 denoise하므로, 마스크 패턴만 바꿔서 text-to-4D, camera 조건 영상 생성, depth와 pose 추정을 같은 모델로 수행함. 학습에서는 데이터에 없는 modality를 loss에서 빼므로 RGB와 pose만 있는 RealEstate10K 같은 데이터도 함께 씀. 추론에서는 후보 장면을 최대 16개 뽑음. 관측 RGB에서 RAFT optical flow로 얻은 대응점과 각 후보의 depth, pose가 얼마나 맞는지 재서 가장 잘 맞는 후보를 고름(test-time search, TTS). 모델은 Wan2.2-TI2V-5B에서 시작해 8개 데이터셋의 50프레임 288×384 clip으로 fine-tuning함.

**결과**

- 첫 프레임과 마지막 프레임만 주는 sparse camera pose 추정에서 RealEstate10K translation 방향 오차(tAE)가 UGG 단일 sample 8.260도, TTS 3.475도임. 가장 좋은 baseline인 Aether는 39.834도임. 5개 데이터셋 모두에서 tAE와 회전 오차가 baseline보다 낮음.
- 전체 video를 주는 dense pose 추정에서 ScanNet++ 궤적 오차(ATE)가 Geo4D의 0.190에서 0.087로 내려감. sparse depth 추정의 ScanNet++ Abs Rel(상대 depth 오차)은 가장 좋은 baseline Marigold 0.169 대비 UGG 0.101, TTS 0.082임.
- 우세가 고르지는 않음. dense depth에서 Sintel Abs Rel은 Geo4D 0.247, UGG 0.303이고 7-Scenes도 Geo4D가 앞섬. 2-view camera 조건 생성에서 DL3DV PSNR은 diffusion 기반 novel view synthesis 모델 SEVA 17.61, UGG 16.61임.
- Wan2.1-1.3B로 한 ablation에서 RGB 생성 학습을 빼면 KITTI depth Abs Rel이 0.152에서 0.322로 오름. depth 정답이 없는 RealEstate10K를 학습에 더하면 Bonn Abs Rel이 0.239에서 0.135로 내려감.

**한계**

TTS 선택 기준은 RGB 재투영 오차라서 정답과 어긋날 때가 있음. 같은 16개 후보 중 정답 대비 오차가 가장 작은 것을 고르는 oracle과의 차이가 커서, 예를 들어 RealEstate10K sparse tAE는 TTS 3.475도, oracle 1.550도임. dense depth 일부와 2-view novel view synthesis에서는 전용 모델이 더 좋음. 해상도가 288×384로 낮고, 로봇 과제나 실시간 추론 비용은 다루지 않음.

**누리랩 연구와의 연결**

- RGB, depth, camera를 같이 생성하는 모델은 geometry를 갖춘 world model로 쓸 수 있음. 손목 카메라 몇 장만 있는 manipulation 장면에서 depth와 pose를 보완하는 용도로 시험해 볼 만함.
- 여러 후보를 뽑고 관측 영상과의 일치도로 고르는 TTS는 test-time optimization의 사례임. 같은 verifier 점수가 낮은 경우를 기하 추정 실패 감지 신호로 쓰는 실험으로 이어질 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 왼쪽에 text prompt, 첫·마지막 RGB와 camera, 전체 RGB, RGB와 depth와 camera 순으로 관측량이 늘어나는 입력을 두고, UGG가 오른쪽의 전체 RGB, depth sequence, camera 궤적을 채워 넣는 구성을 보여 줌.*

*영상: [부분 관측을 조건으로 RGB, depth, camera geometry를 함께 채워 넣는 과정을 보여 주는 저자 데모 영상임.](https://blog-media.assets.alphaxiv.org/videos/01a1c91c-6a18-74bf-8e73-b2c8df68731d/5d83476c-32b8-402f-9aab-40cf724fcd9a) (alphaXiv 요약에서 가져옴)*

---

### 8. From Video Frames to Robot Meta-Frames: A Unified Latent Interface for World Action Models (72점)

[arXiv](https://arxiv.org/abs/2611.14365) · [PDF](https://arxiv.org/pdf/2611.14365) · [alphaXiv](https://www.alphaxiv.org/abs/2611.14365) (요약 있음) · [코드](https://github.com/showlab/MetaWAM)

- **저자**: Guoqiang Liang, Yiqi Lin, Yanzhe Chen, Kevin Yuchen Ma, Mike Zheng Shou
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 86점
- **학회**: CoRL 2026 채택 · 근거: 1쪽에 "10th Conference on Robot Learning (CoRL 2026)"
- **읽은 원문**: PDF 전문

> video diffusion model 기반 World Action Model에 로봇 신호를 넣을 때, 신호마다 latent frame을 하나씩 쓰지 않고 DCT 주파수 대역에 나눠 담은 frame 하나로 합침. RoboCasa에서 frame 수를 11개에서 8개로 줄여 추론 지연을 39% 줄이면서 성공률은 67.1%에서 68.9%로 오름.

**무슨 문제인가**

World Action Model(WAM)은 사전학습된 video diffusion model(VDM)을 고쳐 행동과 미래 관측을 함께 예측하는 모델임. 이때 proprioception, action, value 같은 저차원 로봇 신호를 자연 영상으로 학습된 latent 공간에 넣어야 함. Cosmos Policy는 신호마다 값을 공간에 복제한 latent frame을 하나씩 추가함. 그래서 sequence가 길어지고 attention 비용이 제곱으로 늘어남. DreamZero처럼 전용 action encoder·decoder를 붙이면 사전학습된 backbone을 고쳐야 함. 저자들은 신호를 넣는 방식이 단순한 형식 문제가 아니라, 넣은 latent가 VDM의 사전 분포에 얼마나 맞는지의 문제라고 봄.

**어떻게 푸나**

먼저 진단 실험으로 표현 방식을 고름. 고정된 Cosmos-Predict2 denoiser가 주입된 latent를 얼마나 고쳐 쓰는지를 상대 복원 오차(denoising residual을 깨끗한 latent 크기로 나눈 값)로 재고, 작을수록 사전 분포에 가깝다고 봄. 이 진단에서 주파수 영역 표현이 공간 복제나 VAE 인코딩보다 오차가 작게 나옴. 이를 바탕으로 MetaWAM은 모든 로봇 신호를 meta-frame이라는 latent frame 하나에 담음. task one-hot, 현재·미래 proprioception, action chunk, value는 각각 서로 겹치지 않는 channel 대역의 고정된 DCT 계수 자리에 쓰임. 이 계수에 channel마다 2D inverse DCT를 적용해 공간 latent로 바꿈. 입력 meta-frame(task, 현재 proprioception)은 tokenizer가 원래 비워 두는 맨 앞 latent frame 자리를 재사용하고, 출력 meta-frame이 action·미래 proprioception·value를 예측함. 출력은 2D DCT 후 정해진 자리를 읽어 바로 복원하므로 학습되는 decoder가 없음. 하나의 모델이 band 단위 mask로 각 신호를 조건 입력 또는 denoising target으로 바꿔 가며 policy, world model, value 예측을 함께 학습함.

**결과**

- RoboCasa(주방 조작 과제 24개, 과제당 demonstration 50개)에서 평균 성공률이 68.9%로, 같은 데이터 조건의 Cosmos Policy 67.1%보다 1.8퍼센트포인트 높음. 3 seed, 총 3600회 평가 기준이며 통계적 유의성 검정은 없음.
- 비교 대상은 DCT 없이 신호를 한 frame의 공간 영역에 나눠 담은 두 변형임. Meta-Quadrants는 신호마다 같은 크기의 영역을 주고, Meta-Compact는 신호 차원에 따라 크기를 달리한 영역을 줌. 같은 8 frame, 같은 지연(0.291초)에서 성공률은 Meta-Quadrants 65.9%, Meta-Compact 68.1%, MetaWAM 68.9%임. 신호별 frame을 쓰는 11 frame 방식은 0.479초이므로 지연 감소는 frame 수를 줄인 데서 옴. 같은 frame 수에서는 DCT 배치가 두 공간 배치보다 성공률이 0.8~3.0퍼센트포인트 높음.
- diffusion noise 수준 σ=1.0에서 고정 denoiser의 상대 복원 오차가 MetaWAM 0.5613, Meta-Compact 0.6234, 신호별 frame 방식 0.6178임. Wan2.1-14B, Wan2.2-5B backbone에서도 다중 신호 배치는 MetaWAM이 가장 낮음.
- 실제 Franka에서 과제 3개(쓸기, 컵 놓기, 블록 쌓기)를 과제당 20회 평가함. 평균 성공률이 분포 내 85.0%, 분포 밖(방해물·배치·배경 변화) 68.3%이고, Cosmos Policy는 78.3%, 63.3%임.

**한계**

RoboCasa와 LIBERO(조작 과제 suite 4개로 된 시뮬레이션 benchmark)에서 가장 강한 baseline과의 차이가 작음. LIBERO 평균은 98.1%로 Cosmos Policy 98.5%보다 낮고, LIBERO-Plus(교란 7종에 대한 강건성 평가)에서는 배경 변화(72.6%)와 로봇 초기 상태 변화(59.9%)에서 Cosmos Policy보다 낮음. 상대 복원 오차는 저자도 성공률의 정량 예측값이 아니라고 밝힘. 실로봇은 팔 하나에 과제 3개이며, 대역 배치와 loss 가중치는 고정이라 신호 크기가 크게 다르면 다시 맞춰야 함.

**누리랩 연구와의 연결**

- 사전학습된 video model을 world model 겸 VLA로 쓸 때 action·value 같은 신호를 구조 변경 없이 넣는 방법임. 같은 모델에서 policy, world model, value를 mask로 바꿔 부를 수 있어 test-time planning이나 value 기반 failure detection에 그대로 쓸 수 있는 구조임.
- 고정 denoiser의 상대 복원 오차로 입력 표현이 사전 분포에 맞는지 학습 전에 비교하는 진단은, 우리가 video world model에 새 조건 신호(접촉, 3D 정보 등)를 넣을 때 후보를 고르는 기준으로 쓸 수 있음.

*대표 그림: 방법 구조를 그린 개념도 (a)와 상대 복원 오차를 잰 진단 결과 (b)로 이뤄진 그림임. 왼쪽 (a)는 task, 현재·미래 proprioception, action chunk, value가 DCT를 거쳐 meta-frame 하나에 담기는 구조임. policy·world model·value function마다 어느 칸이 조건 입력이고 어느 칸이 denoising target인지 표시함. 오른쪽 (b)는 상대 복원 오차 막대그래프로 DCT 인코딩이 약 0.6으로 VAE 인코딩, 공간 복제보다 낮음.*

---

### 9. How Much of Your VLA Is kNN (68점)

[arXiv](https://arxiv.org/abs/2611.13160) · [PDF](https://arxiv.org/pdf/2611.13160) · [alphaXiv](https://www.alphaxiv.org/abs/2611.13160) (요약 있음) · [코드](https://github.com/sereact/lerobot_knn)

- **저자**: Denis Grachev, Damien LaRocque, Omar Moured
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: CoRL 2026 채택 · 근거: comments에 "21 pages, 10 figures, accepted to the CoRL 2026 G2A/TAG workshop"
- **읽은 원문**: PDF 전문

> 지금 장면과 가까운 시연 장면을 찾아 그 뒤의 action chunk를 섞어 쓰는 kNN policy만으로, action policy 학습 없이 LIBERO 평균 성공률 91.7%를 얻음. 같은 방법으로 공개 VLA 9개의 성능과 backbone을 비교해, LIBERO 점수 중 시연 검색으로 설명되는 부분을 측정함.

**무슨 문제인가**

최근 VLA는 LIBERO(Franka 팔 조작 과제를 모은 시뮬레이션 benchmark)에서 95%가 넘는 성공률을 보고함. LIBERO는 과제마다 시연 50개를 주고 정해진 초기 상태에서 평가함. 그래서 높은 점수가 시연을 넘어선 일반화인지 시연을 따라 한 결과인지 가리기 어려움. 실제로 LIBERO-Plus(카메라 시점, 로봇 초기 자세, 언어, 조명, 배경, noise, 배치의 7종 교란을 준 LIBERO)에서는 같은 VLA의 성공률이 크게 낮아짐이 보고됨. 그래서 학습 없이 시연을 찾아 쓰는 것만으로 benchmark 성능이 얼마나 나오는지를 기준선으로 잴 필요가 있음.

**어떻게 푸나**

저자들은 LIBERO 시연 1693개에서 두 frame마다 관측과 그 뒤의 action chunk를 묶어 약 137k개 항목의 memory를 만듦. 실행 중에는 현재 관측을 같은 공간에 embedding하고 거리가 가장 가까운 항목 k개를 찾음. 거리는 ResNet-18 이미지 특징, robot state, CLIP 언어 embedding, episode 시간, 최근 관측 이력의 거리를 더한 값임. 각 항은 같은 과제 안 거리의 median으로 나눠 단위를 맞춤. 한 시연에서는 항목을 하나만 고르고, 거리에 softmax를 씌운 가중치로 이웃들의 action chunk를 평균해 다음 action으로 출력함. LAC(Local Action Consistency)는 rollout 없이 retrieval key의 질을 재는 지표임. 표현 공간에서 가까운 이웃 k개와의 미래 action 거리를 같은 과제 전체와의 평균 action 거리로 나누고 1에서 뺀 값임. 변형은 이미지 거리만 쓰는 ResNet 변형(k=8), 모든 거리를 쓰는 multimodal 변형(k=13), multimodal 변형의 이미지 특징에 학습한 선형 투영을 붙인 LAC key 변형 세 가지임. 같은 kNN에 VLA의 VLM 은닉 상태를 key로 넣어, 각 VLA backbone을 LIBERO fine-tuning 전후로 비교함.

**결과**

- LIBERO 4개 suite 40개 과제의 평균 성공률(정책당 2000 rollout)은 multimodal kNN이 91.7%임. π0-FAST 90.6%, SmolVLA 82.2%, π0 71.9%보다 높고, 가장 높은 π0.5의 97.7%보다는 낮음.
- LIBERO-Plus의 고정된 교란 420개에서 multimodal kNN은 82.4%로 VLA 9개 중 7개보다 높음. LIBERO 대비 하락폭은 9.3퍼센트포인트로 평가한 정책 중 가장 작음. VLA-JEPA는 LIBERO 97.2%에서 LIBERO-Plus 74.0%로 내림.
- VLA가 rollout 중 낸 action chunk를 ResNet kNN의 예측과 비교한 R²는 0.63~0.93이며, 절대 자세를 예측하는 X-VLA를 뺀 8개를 비교함. 같은 kNN 예측과 held-out 시연 정답 chunk의 R²는 0.78이고, 8개 중 5개 VLA의 chunk가 이보다 kNN 예측에 더 가까움.
- VLM backbone을 key로 쓴 LIBERO-Plus 검색 성공률은 fine-tuning 후 8개 중 7개 모델에서 오름(VLM을 고정하는 GR00T 제외). LIBERO-Plus에서 4개 모델은 검색만으로 전체 VLA보다 높음(SmolVLA 69.3% 대 27.9%). π0 backbone을 key로 쓴 LIBERO 검색 성공률은 fine-tuning 전 86.9%에서 후 17.9%로 내림.

**한계**

실험은 LIBERO와 LIBERO-Plus 시뮬레이션뿐이고 실로봇 결과는 없음. LIBERO는 시연 밀도가 높고 LIBERO-Plus 교란은 과제의 해 궤적을 거의 바꾸지 않아 검색 방식에 유리할 수 있다고 저자도 적음. 공개 checkpoint를 그대로 평가해 π0, SmolVLA 등은 원 논문 수치보다 낮게 나왔고, LAC는 비슷한 수준의 key끼리 순위를 잘 가리지 못함(Pearson r=0.78, Spearman ρ=0.61).

**누리랩 연구와의 연결**

- VLA 연구에서 LIBERO 성능을 주장할 때 함께 보고할 학습 없는 kNN 기준선으로 쓸 수 있음. 평가 코드와 사용한 VLA checkpoint 목록이 공개되어 있음.
- LAC는 rollout 없이 표현이 action과 맞는지 재는 지표라, robot memory 검색 key 설계와 failure detection용 표현 점검에 가져다 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 평가 파이프라인의 구조를 그린 그림임. 시연(이미지, 언어 지시, robot state, action chunk)은 두 경로로 들어감. (a)는 ResNet-18+CLIP 또는 VLM 특징의 embedding memory에서 k개 이웃의 가중 action chunk를 만들고, (b)는 VLM backbone과 action head로 action chunk를 바로 예측함. 두 경로는 같은 rollout으로 평가됨.*

---

### 10. Elastic-WAM: Adaptive Spatiotemporal Imagination for Efficient Robot Control (68점)

[arXiv](https://arxiv.org/abs/2611.14257) · [PDF](https://arxiv.org/pdf/2611.14257) · [alphaXiv](https://www.alphaxiv.org/abs/2611.14257) (요약 있음) · [프로젝트 페이지](https://lihaitian.com/Elastic-WAM)

- **저자**: Haitian Li, Tianfu Li, Xuxi Zhao, Zizheng Liu, Yangcheng Yu, Yiwen Hou, Zeyu Xiao, Mutian Xu 외 3명
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 62점
- **읽은 원문**: PDF 전문

> 미래 영상과 행동을 함께 denoising하는 World-Action Model에서, 미래 영상을 몇 단계·얼마만큼·어느 영역까지 다듬을지를 상태마다 학습된 함수로 정함. RoboCasa-GR1에서 Joint-WAM보다 성공률은 55.0%에서 57.4%로 오르고 추론 지연은 32.2% 줄어듦.

**무슨 문제인가**

World-Action Model(WAM)은 미래 영상을 예측해 그 표현을 행동 생성의 조건으로 씀. 미래 영상을 diffusion으로 여러 번 denoising해야 해서 추론이 느림. 기존 가속 방법은 미래 영상을 덜 다듬어도 행동이 잘 나온다는 점을 이용하지만, 몇 단계 다듬을지를 과제와 상태에 상관없이 고정함. 저자들은 LIBERO-Plus(카메라·조명·노이즈 등 7종 교란을 건 LIBERO 평가) 과제 10개에서 성공률이 가장 높은 denoising 단계 수가 과제마다 1~4로 다르고, 같은 과제 안에서도 상태마다 다르다는 관찰을 제시함. 행동 token이 미래 영상의 일부 영역에만 attention을 몰아 준다는 관찰도 함께 제시함.

**어떻게 푸나**

Elastic-WAM은 baseline인 Joint-WAM(미래 영상과 행동을 반복 denoising으로 함께 다듬는 사전학습 WAM)을 그대로 고정하고, 남은 미래 영상 정제 수요를 나타내는 작은 함수만 학습함. 미래 영상 token 196개를 시점과 카메라 경계를 지키는 64개 group으로 나누고, 각 group의 수요를 group별 크기와 공유 Beta 분포의 곱으로 표현함. 이 함수에서 세 가지 결정이 나옴. 전체 수요를 누적한 commit 확률이 0.5를 넘으면 영상 정제를 멈추고(WHEN), Beta 분포의 mode로 다음 denoising 보폭을 정하고(HOW FAR), group별 상대 점수 순으로 정확히 96개 token만 새로 계산함(WHERE). 학습은 보폭 분포, 영역별 상대 점수, 전체 수요의 offset을 차례로 맞추는 세 단계로 나뉨. 보폭과 정지 시점은 여러 후보를 실제로 돌려 최종 행동 오차가 작은 쪽을 정답으로 삼고, 영역 점수는 전체 token을 갱신한 결과를 teacher로 삼아 sparse 갱신 결과를 맞추도록 학습함. 추론 때는 첫 단계만 전체 token을 갱신하고, 이후에는 고른 token만 다시 계산하되 attention은 전체 KV cache를 봄. 영상 정제를 멈춘 뒤에는 cache된 영상 표현으로 행동 denoising만 이어감.

**결과**

- RoboCasa-GR1(물체 재배치와 서랍·전자레인지 같은 관절 물체 조작을 포함한 탁상 과제 24개 모음)에서 성공률이 Joint-WAM의 55.0%에서 57.4%로 오름. 같은 H800 GPU에서 추론 지연은 572.6ms에서 388.2ms로 줄어듦. 다만 Fast-WAM(331.1ms)보다는 느리고, π0.5 등 VLA(77~82ms)보다 약 5배 느림.
- 같은 RoboCasa-GR1에서 학습된 영역 선택의 효과를 따로 잼. 같은 96 token을 무작위로 고르면 전체 성공률이 57.42%에서 53.83%로 내려감. 갱신 token 수를 128개로 늘린 all-active 설정은 55.17%, 첫 단계의 영상 cache만 재사용하면 54.50%임.
- LIBERO-Plus에서 LIBERO로만 학습한 policy의 평균 성공률이 73.7%로, Joint-WAM 66.3%보다 7.4퍼센트포인트 높음. 정지 시점과 보폭을 모두 고정한 WHERE-only 설정은 71.71%임.
- 실제 양팔 xArm 7 로봇의 4단계 차 준비 과제를 조건마다 20회 시행함. 전체 성공률은 평상 조건과 조명 변화에서 50%로 Joint-WAM의 30%보다 높고, 컵 교체 조건에서는 둘 다 30%임. Fast-WAM은 세 조건 모두 0%임.

**한계**

LIBERO와 LIBERO-Pro(물체·위치·지시 의미·과제 구성을 바꾼 LIBERO 평가)에서는 Joint-WAM 대비 차이가 평균 0.3~1.3퍼센트포인트에 그치고, 반복 실행에 따른 분산은 보고하지 않음. 지연은 RoboCasa-GR1 한 곳에서만 쟀고, 영상 token 수 96개는 학습되지 않은 외부 설정값임. 실로봇 실험은 과제 1개에 조건별 20회이며, 코드 저장소 주소는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- world model 기반 policy에서 상태마다 추론 계산량을 다르게 쓰는 사례임. test-time optimization 연구에서 계산 예산을 언제 더 쓸지 정하는 기준(최종 행동 오차로 학습한 정지 확률)의 비교 대상이 됨.
- 행동에 쓰이는 미래 영상 영역만 골라 갱신하는 구조는, world model 예측 중 어느 부분이 조작에 쓰이는지 보는 분석 도구로 활용할 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 위쪽은 "Pour tea" 지시·영상·proprio를 넣고 첫 단계만 전체 token을 갱신한 뒤 단계마다 보폭(0.08, 0.11, 0.06)과 갱신할 token이 바뀌다가 commit하는 추론 과정임. 아래쪽은 temporal branch(Beta 분포)와 spatial branch(group별 크기)가 합쳐져 WHEN·HOW FAR·WHERE를 정하는 구조임.*

---

### 11. Few-Shot Residual Adaptation of Pretrained Latent World Models (66점)

[arXiv](https://arxiv.org/abs/2611.13592) · [PDF](https://arxiv.org/pdf/2611.13592) · [alphaXiv](https://www.alphaxiv.org/abs/2611.13592) (요약 있음)

- **저자**: Jakub Suliga, Pankhuri Vanjani, Nisarga Nilavadi, Wolfram Burgard, Rudolf Lioutikov
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 62점
- **학회**: NeurIPS 2026 채택 · 근거: 1쪽에 "40th Conference on Neural Information Processing Systems (NeurIPS 2026)"
- **읽은 원문**: PDF 전문

> 물체의 무게중심이나 마찰이 바뀌어 planning이 실패할 때, 고정된 latent world model 안팎에 작은 residual 보정 모듈을 붙이고 상호작용 3 episode의 예측 오차로만 학습시킴. 실로봇 상자 밀기에서 무게중심 이동 조건의 성공률이 0%에서 90%로 오름.

**무슨 문제인가**

latent world model은 학습 때와 다른 물리 조건에서 쓰이면 같은 행동의 결과를 틀리게 예측하고 planning이 실패함. 상자 안에 숨긴 추로 무게중심을 옮기거나 바닥 절반에 천을 깔기만 해도 과제와 controller가 그대로인데 성공률이 0% 근처로 내려감. 기존 대응은 모델 재학습, 시뮬레이터 기반 물리 파라미터 추정, 학습 때 dynamics randomization 등임. 이 방법들은 데이터가 많이 들거나, 학습 과정이나 dynamics의 파라미터화, 바뀔 조건에 대한 사전 지식을 요구함.

**어떻게 푸나**

기반 모델은 DUET-DINO(V-JEPA 2-AC 계열로, 측면 카메라와 손목 카메라의 DINOv3 latent를 행동 조건으로 한 step 앞까지 예측하는 모델)임. 계획은 one-step CEM(cross-entropy method)으로 하며, 샘플한 행동마다 다음 latent를 예측하고 목표 이미지 latent와의 거리로 순위를 매겨 실행함. 저자는 encoder, predictor 가중치, CEM controller를 모두 고정하고 보정 모듈 두 종류만 추가함. 첫째는 Adapter+(bottleneck residual branch에 채널별 scale을 곱하는 모듈)임. 측면·손목 두 predictor head의 Transformer block 24개마다 두 곳씩 넣어 총 96개임. 둘째는 predictor가 낸 latent token에 더해지는 token 단위 residual MLP이며 측면·손목 두 카메라가 공유함. 이 두 모듈을 합친 구성을 dual-site adapter라 부름. 두 모듈은 0으로 초기화되어 처음에는 원래 모델과 같고, 학습 parameter는 합쳐서 29.2M으로 predictor의 4.53%임. 첫 3 episode가 끝날 때마다 실제 다음 관측의 latent를 정답으로 하는 L1 예측 오차로 학습하며, reward나 바뀐 물리량은 쓰지 않음. 내부 adapter를 먼저 25 step 학습해 고정한 뒤 외부 MLP를 25 step 학습하는 순차 방식을 씀.

**결과**

- 실로봇(Franka Panda, 조건당 30회)에서 고정 모델의 성공률은 무게중심 이동에서 0%, 마찰 변경에서 3.3%임. 제안한 dual-site adapter로 3 episode 적응 뒤 각각 90.0%와 100.0%로 오름. 같은 조건에서 LoRA는 30.0%와 66.7%, 전체 fine-tuning은 20.0%와 100.0%임.
- 시뮬레이션(RoboLab 시뮬레이터, 무게중심 이동, seed 3개 각 50회)에서 성공률은 dual-site adapter 56.7%, 내부만 보정한 최선인 LoRA 32.7%, 출력만 보정한 최선인 residual MLP 24.0%임. 두 모듈을 동시에 학습하면 44.0%로 순차 학습보다 낮음.
- 원래 조건 데이터로 같은 절차를 거쳐 학습한 adapter도 무게중심 이동 adapter가 줄인 예측 오차의 95.3%(측면 카메라), 71.7%(손목 카메라)만큼을 줄임. 그런데 무게중심 이동 조건의 성공률은 6.0%로, 무게중심 이동 adapter의 72.0%보다 낮음. 이 비교는 adaptation seed 1개로 50회 평가한 값이라 seed 3개 평균인 56.7%와 다름. 예측 오차를 줄이는 것만으로는 제어 성능이 나오지 않음을 보인 진단임.
- 무게중심 이동 adapter를 원래 조건에 다시 쓰면 성공률이 54.0%로, 고정 모델의 85.3%보다 낮아짐. 시뮬레이션에서 학습한 adapter를 실로봇에 쓰거나 그 반대로 쓰면 성공률은 0~10%임.

**한계**

과제는 상자 밀기 하나, 물리 변화는 무게중심과 마찰 두 가지이며, 마찰 변경은 실로봇에서만 평가함. 조건마다 adapter를 따로 학습하고, 적응 후 원래 조건으로 돌아가면 성능이 낮아지며 여러 보정을 보관·재사용하는 방법은 없음. adapter가 어떤 물리 정보를 담는지는 저자도 밝히지 못했고, 실로봇은 제어 한 step에 약 28초가 걸림. 본문에 코드 공개 주소는 없음.

**누리랩 연구와의 연결**

- world model 기반 planning에서 dynamics shift로 생긴 실패를 배포 중 몇 episode의 예측 오차로 복구하는 test-time adaptation 사례임. 예측 오차를 failure detection 신호로 쓰고 같은 신호로 recovery까지 잇는 연구의 baseline이 됨.
- 예측 오차를 비슷하게 줄인 두 adapter의 성공률이 6.0%와 72.0%로 갈린 결과는 world model 평가 지표를 정할 때 참고할 결과임.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 행동 샘플을 고정된 predictor에 넣어 latent를 예측하고 목표 이미지 latent와의 거리로 최선 행동을 실행한 뒤, 다음 관측과의 L1 오차로 predictor 안쪽 adapter와 바깥쪽 residual adapter만 학습하는 흐름을 보임. 오른쪽에는 24개 Transformer block 안에 Adapter+가 들어가는 위치와 그 내부 구성(Layer Norm, down/up projection, GELU, channel-wise scaling)이 그려져 있음.*

---

### 12. PhysMoE: Fast Spatial Grounding with Single-Token Coordinate Representation in Modality-Decoupled VLMs (66점)

[arXiv](https://arxiv.org/abs/2611.13000) · [PDF](https://arxiv.org/pdf/2611.13000) · [alphaXiv](https://www.alphaxiv.org/abs/2611.13000) (요약 있음)

- **저자**: Ruimeng Liu, Denan Liang, Ruofei Bai, Fuming Zhang, Kuan Xu, Shenghai Yuan, Lihua Xie
- **분야**: Embodied AI · robotics relevance 7/10 · 1차 스크리닝 60점
- **읽은 원문**: PDF 전문

> embodied VLM이 좌표를 숫자 문자열로 쓰지 않고 좌표 하나를 token 하나로 바로 regression하게 바꿈. 9B 모델의 좌표 출력 처리량이 가장 빠른 비교 모델보다 8.31배 높고, 좌표 grounding 9개 benchmark 평균은 초기화 모델의 64.1에서 74.2로 오름.

**무슨 문제인가**

기존 embodied VLM은 "[342, 518]" 같은 좌표를 숫자·쉼표·괄호 token으로 쪼개 한 개씩 생성함. 그래서 점 하나에 8~10번의 decoding이 필요하고, 좌표가 이미지 위치라는 연속성이 token 단위에서 끊김. 또 잡을 수 있는 손잡이나 놓을 수 있는 자리는 영역 안 여러 점이 모두 정답인데, 보통은 영역 중심 한 점에 L1 regression을 걸어 학습함. 이러면 정답 후보가 여러 곳일 때 예측이 그 평균으로 끌려가 영역 밖에 떨어질 수 있음.

**어떻게 푸나**

PhysMoE는 decoder 아래층을 모든 token이 공유하고, 위쪽 K개 층(K=8)에서만 FFN을 언어용과 좌표용 두 개로 나눔. 이 층들에서 self-attention은 계속 공유하고, 작은 router MLP가 token마다 언어 FFN과 좌표 FFN 중 하나를 고름. 출력도 두 갈래로, 언어 token은 LM head가 vocabulary 위 logit을 내고 좌표 token은 MLP head가 0~1로 정규화된 (x, y)를 바로 regression함. 생성된 좌표를 다음 입력으로 넣을 때는 vision encoder의 학습된 2D positional embedding 격자에서 그 위치를 bilinear 보간으로 읽고 linear layer로 언어 hidden 차원에 맞춤. 영역형 정답에는 마스크로 만든 ESDF(Euclidean Signed Distance Field: 경계까지의 거리, 안쪽은 음수, 바깥은 양수) 지도를 씀. 예측 좌표에서 이 값을 미분 가능하게 샘플링해, 밖이면 거리에 따라 커지는 loss를 주고 안쪽이면 깊이에 따라 0에 가까워지는 작은 loss만 줌. 점·박스만 있는 데이터는 SAM3로 마스크를 만들어 쓰고, 약 1,200만 개 샘플로 두 단계 LoRA 학습을 함.

**결과**

- 좌표 grounding 9개 benchmark(affordance 지점 찍기, 지시 대상 위치 찾기, 2D 궤적 예측) 평균이 74.2임. 초기화 모델 RynnBrain 1.1-9B는 64.1, 30B MoE인 HY-Embodied-VLM은 69.2임. 다만 PIOBench, RoboRefit 등 일부 과제에서는 다른 모델이 더 높음.
- 좌표 출력 문항 1,000개를 RTX 5090에서 처리한 속도가 9B 기준 초당 23.34개임. 같은 크기에서 가장 빠른 Embodied-R1.5-8B는 2.81개이고, 4B는 31.88개 대 5.28개(RynnBrain 1.0-4B)임.
- 4B 모델에서 데이터와 구조를 같게 두고 중심점 L1 regression을 ESDF loss로 바꾸면 RoboRefit(지시 대상 위치 찾기)이 79.2에서 82.0으로, Part-Affordance(affordance 지점 찍기)가 55.5에서 57.2로 오름.
- 텍스트 답변형 embodied 추론 11개 benchmark 평균은 9B에서 70.9로 초기화 모델의 71.4와 비슷함. 4B는 평균이 61.3에서 62.7로 올랐지만 공간 관계 질의응답 benchmark인 CV-Bench는 86.2에서 78.2로, EmbSpatial은 77.3에서 68.9로 내림.

**한계**

모든 평가가 정지 이미지 위 benchmark이고 실로봇 실험은 없음. 언어·좌표 FFN 분리가 gradient 간섭을 없앤다는 주장은 같은 조건의 dense decoder와 비교한 ablation이 없어 실험으로 확인되지 않음. 일부 baseline 점수는 다른 논문(HY-Embodied-VLM-1.0)에서 가져왔고, 코드 공개 주소는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- VLA가 2D affordance 점이나 end-effector 궤적을 중간 표현으로 쓸 때, 좌표를 token 하나로 내는 방식은 inference 지연을 줄이는 선택지가 됨. 실제 closed-loop 제어 이득은 직접 확인해야 함.
- ESDF loss는 정답이 영역인 manipulation 지점 학습에 그대로 가져다 쓸 수 있고, 3D SDF나 object-centric 표현으로 넓히는 실험의 출발점이 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 도넛 이미지와 "Locate the donut" 입력에서 router가 Language FFN과 Spatial FFN 중 하나를 골라 Point head가 p=(0.82, 0.50)을 내는 흐름을 그림. 아래쪽은 도넛 마스크의 SDF 지도로 예측점을 안쪽으로 당기는 학습과, 좌표를 positional embedding 격자에서 bilinear로 읽어 다음 입력으로 넣는 과정임.*

---

### 13. Ego Guidance: Enhancing Robot Policy Learning with Action-Free Human Egocentric Videos (62점)

[arXiv](https://arxiv.org/abs/2611.13685) · [PDF](https://arxiv.org/pdf/2611.13685) · [alphaXiv](https://www.alphaxiv.org/abs/2611.13685) (요약 있음) · [프로젝트 페이지](https://llong-cs.github.io/EgoGuidance)

- **저자**: Lin Long, Tianren Ma, Zhong Chu, Di Wu, Maosong Cao, Qixiang Ye, Junbo Zhao, Shanghang Zhang
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 64점
- **학회**: NeurIPS 양식 (추정) · 근거: 1단 구성, 1쪽 꼬리말 'Preprint.'
- **읽은 원문**: PDF 전문

> 행동 label이 없는 사람 1인칭 영상으로, VLA backbone이 미래 장면의 visual feature를 예측하는 보조 과제를 학습시킴. 예측 대상을 SigLIP2 feature로 두면 LIBERO-Plus 평균 성공률이 76.2%로, 픽셀 복원용 Wan-VAE latent를 예측할 때의 60.0%보다 높음.

**무슨 문제인가**

Ego4D 같은 사람 1인칭 영상은 양이 많고 모으기 쉽지만, 로봇이 낼 관절·gripper 명령 같은 action label이 없음. 기존 연구는 영상에서 손 자세나 latent action을 복원해 action label 대신 쓰거나, 미래 영상을 생성하는 World Action Model(WAM)을 policy로 씀. 이 논문은 action을 복원하지 않고도 action-free 영상이 robot policy 학습에 도움이 되는지, 된다면 어떤 예측 대상과 어떤 데이터가 중요한지를 묻는 실험 연구임.

**어떻게 푸나**

SPAR(Shared Prediction on Action and Representation)는 사전학습된 VLM(Qwen3.5-2B)에 두 개의 transformer expert를 붙인 구조임. 두 expert는 VLM의 layer별 hidden state에 cross-attention하고, 서로는 attention하지 않음. action expert는 현재 관측과 지시문을 받아 flow matching으로 action chunk를 출력함. generation expert는 같은 hidden state에서 action chunk 끝 시점의 미래 카메라 영상을 고정된 encoder(SigLIP2 등)로 뽑은 feature를 예측함. 로봇 데이터는 두 loss를 모두 주고, 1인칭 영상은 generation loss만 줌. 따라서 영상의 효과는 공유 backbone의 표현을 바꾸는 경로로만 action에 전달됨. 학습은 DROID 로봇 데이터와 1인칭 영상으로 함께 사전학습한 뒤, 하위 과제 demonstration으로 fine-tuning하는 2단계임. 추론 때는 generation expert를 떼어 내므로 배포 구조와 비용은 일반 VLA와 같음.

**결과**

- LIBERO-Plus(LIBERO 과제에 카메라·초기 상태·언어·조명·texture·sensor noise·물체 배치 7종 분포 변화를 준 평가)에서 예측 대상을 비교함. 평균 성공률은 SigLIP2 76.2%, Qwen-ViT 75.6%, DINOv2 74.9%이고, 복원용 Wan-VAE latent는 60.0%임. 미래 1프레임 예측은 74.32%, 4프레임 예측은 74.62%로 차이가 0.30퍼센트포인트임.
- Ego4D 3,976시간을 카메라 움직임 gate와 손 노출 gate로 걸러 975시간을 남김. 거르지 않은 영상을 섞으면 로봇 데이터만 쓴 경우보다 LIBERO-Plus 성공률이 낮고, 두 gate를 통과한 영상은 fine-tuning 16k·20k step에서 로봇 데이터만 쓴 경우를 넘음. 정확한 수치는 그림에만 있고 본문에서 확인 불가임.
- Open-AoE는 8,000개 과제, 약 2,000시간 분량의 clip·caption 약 100만 쌍을 담은 1인칭 영상 데이터셋임. 이 영상을 0, 150, 450, 1,500시간으로 늘리면 LIBERO-Plus 성공률이 계속 오르고, 분포 변화가 없는 LIBERO 성공률은 거의 유지됨. 같은 200K clip 예산 안에서 장면·물체·상호작용 다양성을 높이는 것은 일관된 이득이 없었음.
- 실제 AgileX 양팔 로봇의 과제 5개에서 과제당 10회 평가한 성공 횟수가 20/50으로, π0.5의 22/50과 비슷함. 오이 옮기기 과제의 조명·배경·방해 물체 변화에서는 9·8·5회로 π0.5의 7·7·4회보다 높음. 꽃 건네기 과제의 조명·방해 물체 변화에서는 2·0회로 π0.5의 5·3회보다 낮음.

**한계**

1인칭 영상을 넣은 효과는 주로 LIBERO-Plus 시뮬레이션에서 보였고, 실로봇에서는 같은 모델의 영상 없는 학습과 비교하지 않아 영상의 기여를 따로 확인할 수 없음. WAM이나 latent action 기반 방법과 직접 비교하지 않았고, 다양성·규모 실험은 저자 스스로 예비 결과라고 밝힘. 실로봇 성능은 π0.5와 비슷한 수준이며, 정밀 grasp·양팔 회전·긴 과제는 두 방법 모두 대부분 실패함.

**누리랩 연구와의 연결**

- action label 없는 영상을 미래 visual feature 예측으로 VLA backbone에 넣는 방식이라, 사람 영상으로 generalist policy의 시각 강건성을 높이려는 VLA 연구에서 baseline 설계로 쓸 수 있음.
- 미래 feature를 예측하는 generation expert는 추론 때 버려지지만, 남겨 두고 예측한 미래 feature와 실제 관측을 비교하면 failure detection용 world model 신호로 쓸 여지가 있음. 이 용도는 논문에서 다루지 않음.

*대표 그림: 측정 결과가 아니라 SPAR의 방법 구조를 그린 그림임. 가운데 VLM backbone의 layer별 hidden state에 왼쪽 action expert와 오른쪽 generation expert가 cross-attention함. 왼쪽 로봇 데이터(w/ action)와 오른쪽 사람 1인칭 영상(w/o action)이 각각 어느 loss를 주는지 색 점으로 표시함.*

---

### 14. Persistent Metric-Semantic Maritime Scene Memory from Open-Vocabulary 3D Scene Graphs (58점)

[arXiv](https://arxiv.org/abs/2611.13903) · [PDF](https://arxiv.org/pdf/2611.13903) · [alphaXiv](https://www.alphaxiv.org/abs/2611.13903)

- **저자**: Kim Alexander Christensen, Dina Zimmermann, Martin Steinert, Eleni Kelasidi
- **분야**: 3D Vision · robotics relevance 8/10 · 1차 스크리닝 66점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> 육상용 open-vocabulary 3D scene graph를 해상 환경에 옮기고, VLM 기반 조각 합치기와 장소·지역 계층을 덧붙여 반복 운항에서 쓰는 장면 기억으로 만듦. 두 번 운항한 자료를 함께 묻는 검색의 F1이 위치 반경 baseline의 0.378에서 0.810으로 오름.

**무슨 문제인가**

3D scene graph(3DSG)는 기하와 의미를 함께 담아 로봇에게 오래 유지되는 지도를 주지만, 기존 방법은 실내나 육상 환경을 전제로 만들어짐. 실내는 방과 층으로, 육상 야외는 도로와 차선으로 계층을 나누는데, 무인 수상선(ASV)이 다니는 운하와 항구에는 이런 구조가 맞지 않음. 같은 수역을 반복해서 다니는 선박은 고정 구조물과 잠시 머무는 선박을 구분해 기억해야 함. 그런데 육상용 open-vocabulary 3DSG 가운데 어느 층이 해상으로 그대로 옮겨지고 어느 층을 고쳐야 하는지는 확인된 적이 없음.

**어떻게 푸나**

저자는 야외용 RGB-LiDAR open-vocabulary 3DSG인 OpenGraph의 인식·지도 작성 부분을 그대로 쓰고, 그 결과물을 사후 처리함. 입력은 위치가 맞춰진 RGB와 LiDAR 관측이고, OpenGraph가 이를 형상·의미 속성·관측 이력을 가진 지도 조각(fragment)들로 만듦. 첫 단계 C050은 bounding box 간격, 의미 feature cosine 유사도, 점 겹침 비율 기준을 모두 넘는 조각 쌍만 합치는 보수적 통합임. 다음 단계에서는 남은 후보 조각 묶음을 기록된 RGB 영상 3장에 다시 투영해 번호를 붙이고, VLM(GPT-6 Astra)이 같은 물체인지 제안한 뒤 따로 검증해 물리적 개체(entity)로 묶음. 같은 방식으로 영상 6장을 보여 주고 선박을 뺐을 때 남는 고정 시설이 무엇인지 물어 개체와 관측을 지역 장소(place)로 묶음. 이와 별도로 OpenStreetMap 지도와 카메라 수면 마스크, LiDAR 구조물 증거를 2m 격자에 모아 수로 폭 변화를 기준으로 큰 해역(macro region)을 나눔. 마지막으로 두 운항에서 따로 만든 장소를 고정 시설 voxel의 겹침 비율로 서로 짝지음.

**결과**

- MUT(항구 환경 해상 추적 데이터셋)의 평가용 남쪽 강변 선박 50척에서, 복원된 선박 하나당 평균 노드 수가 OpenGraph 1.957개에서 1.298개로 내림. 여러 노드로 쪼개진 선박은 25척에서 11척으로 줄었고, 복원된 선박 수는 46척에서 47척으로 거의 같음.
- 같은 비교에서 C050만 쓰면 노드 수가 1.413개, 쪼개진 선박이 15척임. VLM 단계가 기하·의미 통합만으로 남는 조각을 추가로 줄인 것으로 보임.
- Pohang Canal Dataset(약 7.5km 운하를 반복 운항한 자료)의 두 운항 P00과 P03에서 장소를 따로 만들고 비교함. 10개 지역에서 양방향으로 일치하는 장소 대응 12쌍을 얻었고, 두 운항의 큰 해역 나눔이 공통 수면 격자에서 얼마나 일치하는지 잰 ARI는 0.965임.
- 사람이 검토한 질의 검색에서 계층 표현의 평균 F1이 단일 운항 질의 20개에서 0.787로, 위치 반경 baseline의 0.487보다 높음. 두 운항을 함께 묻는 질의 4개에서는 0.810 대 0.378임.

**한계**

평가는 데이터셋 두 개와 운항 두 번에 그치고, 검색 평가는 질의 24개(두 운항 질의 4개)라 표본이 작음. 큰 해역은 OpenStreetMap 지도에 기대며, 이동하는 물체는 다루지 않고 두 운항이 같은 world frame에 있다고 가정함. 지도 작성 후 사후 처리 방식이라 온라인 동작은 보이지 않았고, 원문에 코드 공개 주소가 없음.

**누리랩 연구와의 연결**

- 지도 조각을 기록된 영상에 다시 투영해 VLM에게 같은 물체인지 묻는 방식은 scene graph 기반 robot memory에서 객체 중복을 줄이는 사후 처리로 그대로 옮겨 쓸 수 있음.
- 고정 시설로 장소 정체성을 정하고 움직이는 물체는 상태로만 다루는 설계는, 반복 방문 환경에서 장면 변화를 감지하는 memory 연구의 비교 대상이 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 위에서부터 RGB와 LiDAR로 만든 OpenGraph 지도와 C050 통합 결과를 보여 줌. 이어서 조각 F1~F4에 번호를 붙인 영상으로 VLM이 같은 물체인지와 같은 장소인지 판단하는 단계, 지도 위 해역 R0~R3와 region-place-entity-fragment 4층 계층을 그림.*

---

### 15. One Trajectory, Two Requirements: Accuracy and Local Stability in Euler Sampling for Flow Matching Policies (45점)

[arXiv](https://arxiv.org/abs/2611.13311) · [PDF](https://arxiv.org/pdf/2611.13311) · [alphaXiv](https://www.alphaxiv.org/abs/2611.13311)

- **저자**: Mahindra Rautela
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: CoRL 2026 채택 · 근거: 1쪽에 "10th Conference on Robot Learning (CoRL 2026)"
- **읽은 원문**: PDF 전문

> flow matching policy의 Euler step 수를 정할 때 끝점 정확도와 국소 안정성이 서로 다른 요구치를 낼 수 있음을 통제 실험으로 보이고, 고정된 π0.5-LIBERO에서는 어느 쪽이 step 수를 정하는지 점검함. 입력 30개 모두 안정성 조건을 넘지 않았고, 입력 5개에서 필요한 step 수는 정확도 기준에 따라 5% 오차에서 4~9개, 1% 오차에서 87~112개로 정해짐.

**무슨 문제인가**

π0 계열 VLA는 noise에서 action chunk까지 학습된 ODE를 Euler로 적분해 행동을 만들고, step 수는 보통 오프라인에서 끝점 오차를 재어 하나로 고정함. 그런데 관측, 로봇 상태, 언어 지시, noise가 달라지면 적분 궤적과 그 위의 Jacobian도 달라짐. 끝점이 정확해도 궤적 주변에서 빠르게 수축하는 방향이 있으면, step이 클 때 Euler가 그 방향의 작은 섭동을 오히려 키울 수 있음. 끝점 오차만으로 고른 step 수가 이 국소 안정성 요구까지 만족하는지는 따로 확인된 적이 없음.

**어떻게 푸나**

저자는 필요한 step 수를 정확도 요구치와 안정성 요구치 중 큰 값으로 봄. 정확도 요구치는 RK4로 정밀하게 푼 끝점과 Euler 끝점의 상대 오차가 허용치 이하로 계속 유지되는 최소 step 수로 정의함. 안정성 요구치는 Jacobian 고유값 µ 중 수축하는 mode에 대해 Euler 배율 |1−µ/N|이 1을 넘지 않는 최소 step 수로 정의함. 여기서 χ(t)는 시점 t에서 수축 mode가 요구하는 국소 step 수임. Euler 시점은 정수 m≥1에 대해 t=m/N으로 쓸 수 있어, t·χ(t)≤1이면 그 시점에서 χ≤N/m≤N이 성립함. 그래서 N마다 다시 계산하지 않도록 G(t)=t·χ(t)라는 척도를 둠. 모든 t에서 G≤1이면 어떤 N에서도 수축 mode가 커지지 않음. 검증은 세 단계임. 먼저 정확히 풀리는 2차원 ODE를 보고, 다음으로 학습된 2차원 flow 모델 6개(목표 분포 2개 × 학습 seed 3개)에 수축 좌표 하나를 덧붙여 봄. 마지막으로 가중치를 바꾸지 않은 π0.5-LIBERO checkpoint를 봄. π0.5에서는 320차원 action-flow 상태의 Jacobian 고유값을 JVP와 Arnoldi iteration으로 추정함.

**결과**

- 정확히 풀리는 2차원 ODE에서 허용 오차 0.2일 때, 가속 계수 β=0.1, 수축률 κ=50이면 정확도는 1 step으로 충분함. 같은 조건에서 안정성은 25 step을 요구함. β=10, κ=1이면 반대로 정확도가 25 step을 요구함. β∈{0.1, 10}, κ∈{1, 50}의 네 조합 모두에서 1~128 step 전수 실험이 이론값과 일치함.
- 학습된 flow 모델(Eight-Gaussians: 원 위 8개 Gaussian 분포, bistable Langevin: 이중 우물 확산 분포)에 κ=50 수축 좌표를 붙임. 원래 궤적은 바뀌지 않음. 5% 오차 기준 끝점 정확도는 Eight-Gaussians에서 18 step, Langevin에서 약 22 step에 충족됨. 안정성 기준 때문에 필요한 step 수는 25로 오름. 안정성 경계인 25 step 바로 아래에서 덧붙인 수축 좌표 방향의 섭동은 6.83배로 커짐.
- 고정된 π0.5-LIBERO에서 LIBERO-10(시뮬레이션 장기 조작 과제 10개) 과제마다 입력 3개, 총 30개를 봄. 최대 G 값은 0.5088~0.5252로 모두 경계 1 아래임. task 00의 전체 320×320 Jacobian에서 χ는 t=1의 0.51에서 t=1/32의 16.41로 커지지만, 실제 Euler 시점 기준으로는 조건을 넘지 않음.
- 정확도를 함께 잰 입력 5개에서 필요한 step 수는 5% 오차에서 4~9개, 2%에서 27~39개, 1%에서 87~112개임. 같은 입력의 최대 G 값은 0.5088~0.5171로 거의 변하지 않음. 저자는 이 입력들에서 step 수가 정확도로 정해진다고 해석함.

**한계**

안정성이 step 수를 정하는 경우는 사람이 수축 좌표를 덧붙인 통제 실험에서만 보였고, 실제 사전학습 policy에서는 관찰되지 않음. π0.5 분석은 시뮬레이션 rollout 초반 입력 30개, noise 1개뿐이고 정확도 측정은 입력 5개뿐임. 고유값은 일부만 표본으로 계산했고 t<1/32 구간은 다루지 않으며, 오차 1%가 과제 성공률에 미치는 영향은 재지 않음.

**누리랩 연구와의 연결**

- VLA의 flow matching 추론 step 수를 줄이거나 시점마다 바꾸는 efficient inference·test-time 연구에서, step 수 판단을 끝점 오차와 국소 안정성 두 기준으로 나누어 점검하는 도구로 쓸 수 있음.
- action-flow ODE의 Jacobian 고유값을 JVP와 Arnoldi iteration으로 추정하는 절차는, policy 출력이 noise와 입력 섭동에 얼마나 민감한지 재는 failure 분석에 참고할 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 개념도임. (a) noise에서 action까지 N번의 Euler step, (b) 정확도와 국소 안정성이라는 두 요구, (c) 정확도 제한과 안정성 제한 상황의 차이, (d) 고정된 π0.5-LIBERO에서 Euler 시점마다 두 기준을 점검하는 절차를 나누어 보여 줌.*

---

## 오늘의 흐름

- **World Action Model의 계산량 줄이기**: video diffusion으로 미래 장면과 action을 함께 만드는 모델에서, 미래 장면을 얼마나 만들지 줄이는 논문이 셋 나옴. action·proprioception·value 같은 로봇 신호를 latent frame 하나에 합치거나([MetaWAM](https://arxiv.org/abs/2611.14365)), 접촉 중심 latent만 예측함([LaST0.5](https://arxiv.org/abs/2611.14048)). 상태마다 미래 영상의 denoising step 수와 다시 계산할 영역을 고르기도 함([Elastic-WAM](https://arxiv.org/abs/2611.14257)).
- **action label 없는 데이터에서 action 표현 얻기**: 사람 영상과 다른 로봇의 데이터를 공통 action 공간에 놓으려는 시도가 이어짐. [OnlyAct](https://arxiv.org/abs/2611.14420)는 사전학습 video encoder를 action 쪽으로 조정하고, [Ego Guidance](https://arxiv.org/abs/2611.13685)는 1인칭 영상의 미래 feature 예측을 보조 과제로 씀. [CIALLO](https://arxiv.org/abs/2611.13732)는 로봇별 embedding과 공통 intent로 action을 나누고, [DexSeed](https://arxiv.org/abs/2611.14092)는 사람 손 시연을 시뮬레이션에서 늘려 dexterous VLA 데이터를 만듦.
- **VLA benchmark 점수 다시 읽기**: 점수가 실제 능력을 재는지 따지는 진단 논문이 나옴. [kNN 기준선](https://arxiv.org/abs/2611.13160)은 학습 없는 시연 검색만으로 LIBERO(시뮬레이션 조작 benchmark) 평균 성공률 91.7%를 얻음. [memory VLA 진단](https://arxiv.org/abs/2611.14488)은 memory가 사건 대신 흐른 시간을 센다는 것을 보임. [Euler step 분석](https://arxiv.org/abs/2611.13311)은 flow matching policy의 step 수를 정확도와 안정성 두 기준으로 나눠 점검함.
- **고정된 모델 위에 작은 모듈만 학습해 적응하기**: 큰 policy나 world model은 그대로 두고 작은 부분만 배우는 방식이 여럿 나옴. [ExRL](https://arxiv.org/abs/2611.13482)은 chunk 중 몇 step을 실행할지만 배우고, [residual world model 적응](https://arxiv.org/abs/2611.13592)은 상호작용 3 episode로 dynamics 변화를 보정함.
- **로봇이 쓰는 3D 기하와 장면 기억**: [UGG](https://arxiv.org/abs/2611.14440)는 RGB, depth, camera pose를 한 diffusion 모델에서 생성함. [선박 운항용 scene graph memory](https://arxiv.org/abs/2611.13903)는 반복 운항에서 같은 물체를 묶어 기억함. [PhysMoE](https://arxiv.org/abs/2611.13000)는 VLM이 좌표를 token 하나로 바로 출력하게 함.

## 해볼 만한 연구

### 사건 단위로 쌓는 memory VLA
- 질문: frame을 시간 간격 대신 상태 변화가 생길 때만 memory에 넣으면, 멈춤이 끼어들어도 반복 횟수 과제의 성공률이 유지되는지 밝힘.
- 첫 실험: RoboMME(memory를 시험하는 조작 benchmark)의 PickXtimes(정육면체를 K번 옮긴 뒤 버튼 누르기)에서 시간 간격 sampling과 물체 위치·접촉 변화 기반 sampling을 비교함. 멈춤 길이를 0초, 5초, 10초로 바꿔 과제 성공률을 잼.
- 가장 가까운 연구: [memory VLA 진단](https://arxiv.org/abs/2611.14488)은 문제를 진단하고, 멈춤 구간을 memory에서 빼는 방법만 시험함. 이 연구는 상태 변화 검출로 memory를 쌓는 방법 자체를 만듦.

### world model 예측 오차로 실패를 감지하고 바로 복구하기
- 질문: 배포 중 world model의 예측 오차가 커지는 시점을 failure 신호로 쓰고, 같은 오차로 residual 모듈을 고치면 실패 직후 복구까지 이어지는지 밝힘.
- 첫 실험: 무게중심을 바꾼 상자 밀기에서 오차 임계값 기반 감지와 진행도 value 기반 감지를 비교함. 감지 시점, 오탐률, 복구 후 성공률을 잼.
- 가장 가까운 연구: [residual world model 적응](https://arxiv.org/abs/2611.13592)은 실패 감지 없이 3 episode를 모은 뒤 적응함. [LaST0.5](https://arxiv.org/abs/2611.14048)는 진행도 value로 재계획만 하고 모델은 고치지 않음.

### chunk 실행 길이 critic을 failure 예측 신호로 쓰기
- 질문: 실행 길이를 고르는 critic의 값이 낮아지는 시점이 실제 실패보다 먼저 오는지 밝힘.
- 첫 실험: LIBERO에서 고정 π0.5와 ExRL critic을 함께 돌리고, critic 값과 이후 실패 여부의 관계를 AUROC로 잼. 같은 rollout에서 action 분산 기반 감지기와 비교함.
- 가장 가까운 연구: [ExRL](https://arxiv.org/abs/2611.13482)은 critic을 실행 길이 선택에만 쓰고 실패 예측력은 재지 않음.

## 꼭 읽을 논문

- [Is Your Robot's Memory Just a Clock?](https://arxiv.org/abs/2611.14488): memory VLA를 평가할 때 바로 가져다 쓸 수 있는 진단 절차가 있음.
- [ExRL](https://arxiv.org/abs/2611.13482): 고정된 VLA를 다시 학습하지 않고 실행 길이만 배워 online 적응하는 방법임.
- [How Much of Your VLA Is kNN](https://arxiv.org/abs/2611.13160): LIBERO 성능을 주장할 때 함께 보고할 학습 없는 기준선을 제공함.
- [Few-Shot Residual Adaptation of Pretrained Latent World Models](https://arxiv.org/abs/2611.13592): 예측 오차만으로 world model을 실로봇에서 적응시키고, 예측 오차가 줄어도 제어 성공률이 함께 오르지는 않는다는 결과를 보임.
- [LaST0.5](https://arxiv.org/abs/2611.14048): 접촉 중심 latent와 진행도 기반 재계획을 함께 쓰는 World Action Model임.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (476편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2611.14365'>From Video Frames to Robot Meta-Frames: A Unified Latent Interface for World Action Models</a></td><td>86</td><td>10</td><td>VLA</td><td>Video diffusion 기반 World Action Model에 로봇 meta-frame 통합 latent 인터페이스 제안임. WAM, VLA, world model 핵심 주제와 직접 일치</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2611.14420'>OnlyAct: Extracting Action Representations from Foundation Models for World Models</a></td><td>76</td><td>8</td><td>World Model</td><td>Foundation model에서 action 표현을 추출해 action 라벨 없이 world model 학습함. 행동 감독 부족 문제에 직접 대응</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2611.13311'>One Trajectory, Two Requirements: Accuracy and Local Stability in Euler Sampling for Flow Matching Policies</a></td><td>72</td><td>9</td><td>Manipulation</td><td>flow matching robot policy의 Euler step 수를 입력별 정확도와 국소 안정성으로 정하는 inference 효율 분석, 로봇 policy 직접 관련임</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2611.13160'>How Much of Your VLA Is kNN</a></td><td>72</td><td>9</td><td>VLA</td><td>LIBERO에서 demonstration 검색·재사용만으로 91.7% 달성함을 보여 VLA 평가 benchmark를 비판함. 분석 가치가 높음.</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2611.14488'>Is Your Robot&#x27;s Memory Just a Clock? Temporal Shortcuts in Memory-Augmented VLA Policies</a></td><td>70</td><td>9</td><td>VLA</td><td>memory-augmented VLA가 시간 shortcut에 의존하는지 비판 분석함. robot memory 주제에 직접 부합하고 통찰이 큼.</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2611.14048'>LaST0.5: A Generalist World Action Model with Interaction-Centric Latent Reasoning</a></td><td>68</td><td>9</td><td>World Model</td><td>상호작용 중심 latent 추론을 갖춘 generalist world action model임. WAM의 전역 표현 전이 한계를 짚어 관련성 높음.</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2611.14092'>DexSeed: Expanding Human Hand-Object Interactions into Robot Demonstrations for Dexterous Policy Learning</a></td><td>66</td><td>9</td><td>Manipulation</td><td>인간 hand-object 상호작용을 dexterous 로봇 demonstration으로 확장해 VLA를 학습함. 데이터 생성 관점에서 관련 깊음.</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2611.13903'>Persistent Metric-Semantic Maritime Scene Memory from Open-Vocabulary 3D Scene Graphs</a></td><td>66</td><td>8</td><td>Scene Graph</td><td>해양 환경 open-vocabulary 3D scene graph 지속 메모리임. scene graph와 robot memory에 직접 연결</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2611.13482'>ExRL: Sample-Efficient Online Adaptation of Long-Chunk Policies via Execution Length Control</a></td><td>66</td><td>8</td><td>RL</td><td>long action chunk policy를 실행 길이 제어로 sample 효율적으로 RL 적응시킴. 핵심 문제가 현실적이고 관련성 높음.</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2611.14440'>UGG: Unified Generative Geometry Model</a></td><td>66</td><td>7</td><td>3D Vision</td><td>4D 장면 기하, 외형, 동역학을 통합 생성하는 geometry 모델임. 4D 표현과 world model 연결</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2611.13685'>Ego Guidance: Enhancing Robot Policy Learning with Action-Free Human Egocentric Videos</a></td><td>64</td><td>9</td><td>VLA</td><td>action 없는 인간 egocentric 영상을 미래 시각 예측으로 policy 학습에 활용하는 SPAR 구조임. VLA 학습과 직접 연결됨.</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2611.13592'>Few-Shot Residual Adaptation of Pretrained Latent World Models</a></td><td>62</td><td>8</td><td>World Model</td><td>사전학습 latent world model을 few-shot residual로 변화한 동역학에 적응시킴. world model 활용과 test-time 적응에 부합함.</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2611.14257'>Elastic-WAM: Adaptive Spatiotemporal Imagination for Efficient Robot Control</a></td><td>62</td><td>8</td><td>World Model</td><td>World-Action Model 추론 비용을 적응적 미래 denoising로 줄임. efficient inference 관점에서 유용함.</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2611.13732'>CIALLO: Learning Shared Intent Representations for Cross-Embodiment Manipulation</a></td><td>60</td><td>8</td><td>Manipulation</td><td>행동·시각·언어 정렬로 cross-embodiment 공유 intent 표현을 학습하는 action codec임. generalist policy에 관련 깊음.</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2611.13000'>PhysMoE: Fast Spatial Grounding with Single-Token Coordinate Representation in Modality-Decoupled VLMs</a></td><td>60</td><td>7</td><td>VLA</td><td>Embodied VLM에서 single-token 좌표 grounding과 affordance 다중 접촉 예측임. 조작 연관 높으나 증거 확인 필요</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2611.13227'>Latent Barrier Steering: Hierarchical Safety for Generative Planning</a></td><td>60</td><td>7</td><td>Planning</td><td>flow matching planner에 잠재 공간 barrier 조향으로 계층적 안전성을 부여함. 생성 policy 안전성 측면에서 참신함.</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2611.13003'>Branch-and-Commit for Frozen RL Agents: When and Where to Spend Test-Time Compute</a></td><td>60</td><td>5</td><td>RL</td><td>고정 RL agent에 test-time branching으로 compute를 쓰는 inference-time planning 분석, 디지털 환경 한정임</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2611.13030'>APS-VLA: Action-Guided and Future-Aware Token Pruning for Efficient Vision-Language-Action Models</a></td><td>58</td><td>8</td><td>VLA</td><td>VLA 시각 토큰 pruning, action 유도와 미래 인지. 효율 추론이 VLA에 직접 적용되나 incremental 성격</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2611.13229'>Incorporating World Models in Decision Making for Next Best View Selection in Active Sensing</a></td><td>58</td><td>7</td><td>3D Vision</td><td>world model로 NBV를 고르고 실제 센서 조건에 맞게 보정함. active perception과 직접 연결됨.</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2611.14274'>From Prediction to Action: Learning Physical Context for Deformable Linear Object Manipulation</a></td><td>58</td><td>7</td><td>Manipulation</td><td>예측 효용과 결정 효용이 다름을 DLO 조작에서 분석함. 표현 관점의 문제 제기가 좋으나 설정이 좁음.</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2611.13453'>Camera3R: Feed-Forward 3D Reconstruction from Heterogeneous Camera Models</a></td><td>58</td><td>6</td><td>3D Vision</td><td>다양한 카메라 모델용 feed-forward 3D reconstruction임. 로봇 인지 기반으로 실용적</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2611.14135'>Sim(3)-TurboReg: Robust and Efficient Scale-Aware Registration via Tri-Scale Consistency</a></td><td>56</td><td>6</td><td>3D Vision</td><td>Feed-forward 3D 스트리밍용 Sim(3) 정합임. 장시간 SLAM/재구성과 연결</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2611.13034'>RoboACE: Adversarial Co-Evolution for Robot Self-Improvement</a></td><td>55</td><td>7</td><td>Embodied AI</td><td>실행 피드백으로 skill·복구 전략을 개선하고 연습 과제 생성기도 적대적으로 공진화시킴. failure 기반 self-improvement로 관련 깊으나 증거 확인 필요함.</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2611.14111'>Model-Free Runtime Measurement of Task-Relevant Information</a></td><td>55</td><td>6</td><td>Failure Detection</td><td>정보 수집 과정이 제대로 작동하는지 model-free로 runtime 측정함. 모니터링·failure detection과 연결됨.</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2611.13113'>Building World Models from Intrinsic Motivation</a></td><td>55</td><td>6</td><td>World Model</td><td>intrinsic motivation이 world model 표현에 미치는 영향 연구. world model·탐색 주제와 연결, 실험 범위 불확실</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2611.14060'>Where Do Vision-Language Models Get Left and Right? Position-Code Counterfactuals in Qwen2.5-VL, Qwen3-VL and InternVL3</a></td><td>54</td><td>3</td><td>Multimodal</td><td>VLM의 좌우 정보 출처를 position code counterfactual로 분석함. 공간 추론 해석 연구로 유용</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2611.12983'>CAFE: Closed-Loop Autonomous Task Formulation and Execution without Instance-Specific Instructions</a></td><td>52</td><td>7</td><td>Embodied AI</td><td>객체·기능 영역·실행 상태 online memory로 지시 없이 과제를 정하고 실행함. memory 관련성은 있으나 규칙 기반 비중이 큼.</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2611.13669'>A computational framework for understanding embodied plans</a></td><td>52</td><td>6</td><td>Embodied AI</td><td>embodied 장기 계획에 대한 목표 추론 계산 프레임워크(GenEA). cooperative embodied AI와 연결, 실증 확인 필요</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2611.13993'>Temporal Behavior Trees for Reinforcement Learning: Specifications as Rewards, Curricula, and Diagnostics</a></td><td>52</td><td>5</td><td>RL</td><td>temporal behavior tree로 reward, curriculum, 진단을 통합하는 RL 사양 틀, 로봇 task spec과 연결 가능임</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2611.13576'>PhyRubric: Rubric-Grounded Diagnostic Evaluation of Physical Commonsense in Text-to-Video Generation</a></td><td>52</td><td>4</td><td>World Model</td><td>T2V 물리 상식 rubric 평가임. world simulator 관점의 진단 평가로 의미 있음</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2611.14113'>Looking One Step Ahead: An Anticipation-guided Agent for Object State Readout in Videos</a></td><td>52</td><td>4</td><td>Video</td><td>예측 기반 agent로 object state 읽기임. 활동 진행 이해로 manipulation과 간접 연결</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2611.13907'>EVAThink: Evidence Sufficiency-Guided Training for Adaptive Thinking in Video Understanding</a></td><td>52</td><td>3</td><td>Video</td><td>증거 충분성 기반 adaptive thinking video 이해임. 추론 효율 아이디어이나 로봇 연관 약함</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2611.12978'>Trajectory-Regularized Distribution Distillation for One-Step Generation</a></td><td>52</td><td>1</td><td>Generative</td><td>Flow matching one-step distillation에 trajectory 정규화 결합임. 방법론은 의미 있으나 로봇 연관 약함</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2611.13610'>From Egocentric Human Video to Robot Manipulation in the Era of Embodied Intelligence</a></td><td>50</td><td>8</td><td>Survey</td><td>egocentric 인간 영상에서 로봇 조작으로의 전이를 다룬 서베이임. 관련 주제이나 방법 기여는 아님.</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2611.13499'>DeRep: Learning Depth Representations for End-to-End Navigation in Cluttered Environments</a></td><td>50</td><td>6</td><td>Navigation</td><td>깊이 표현을 명시적으로 학습해 clutter 환경 end-to-end 항법을 개선함. 표현 학습 관점이 유용함.</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2611.13028'>GTAGym: Real AAA Game Tasks Environment for Evaluation and Reinforcement Learning</a></td><td>50</td><td>5</td><td>RL</td><td>GTA 게임 과제 환경과 RL 평가용 gym임. 에이전트 평가 인프라로 유용하나 로봇 직접 연결 약함</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2611.13039'>Robo-MLT: Dual-System Robotic Manipulation for Long-Horizon Medical Laboratory Tasks</a></td><td>48</td><td>7</td><td>Manipulation</td><td>workflow 모니터링과 학습 policy를 결합한 의료 실험실 long-horizon 조작 시스템임. 응용 특화 성격이 강함.</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2611.13819'>Game-Enhanced Embodied Learning with Event and Foresight Pretraining</a></td><td>48</td><td>7</td><td>VLA</td><td>게임 플레이 event·foresight 사전학습으로 InternVLA-A1.5를 보강함. 데이터 소스는 새로우나 효과 증거는 확인 필요함.</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2611.13769'>From Depth to Safe Depth: Uncertainty-Aware Monocular Perception for Mobile Robot Navigation</a></td><td>48</td><td>6</td><td>Navigation</td><td>단안 깊이 모델의 위험한 과대 추정을 불확실성 인지로 보정해 항법 충돌을 줄임. 문제 지적은 좋으나 시뮬레이션 중심임.</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2611.13486'>Hand-Object Contact Transition Detection in Egocentric Video</a></td><td>48</td><td>5</td><td>Video</td><td>Egocentric 손-물체 접촉 전이 탐지임. manipulation 데이터 분석과 연결 가능</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2611.13700'>CJRR-Net: A Candidate-Joint Reprojection Ranking for Future-View Selection in Human Pose Estimation</a></td><td>48</td><td>5</td><td>Active Perception</td><td>후보 관절 재투영으로 다음 시점 선택임. active perception/NBV와 직접 연결</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2611.13013'>FaST: Factored Synthesis of Transitions for Offline Reinforcement Learning</a></td><td>48</td><td>5</td><td>RL</td><td>offline RL용 transition을 factor별로 합성하는 생성 증강, 로봇 직접 검증은 불확실임</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2611.13182'>Making Strides in Symbolic Imitation Learning: Offline Demonstrations, Online Tuning</a></td><td>48</td><td>5</td><td>IL</td><td>continuous control용 symbolic imitation learning 및 online tuning, 해석 가능 policy 시도임</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2611.14099'>Opportunity-Cost Option-Critic: Adaptive Switching Costs for Robust Hierarchical Reinforcement Learning</a></td><td>48</td><td>5</td><td>RL</td><td>hierarchical RL option-critic의 adaptive switching cost, skill 계층과 연결임</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2611.13596'>Towards Reliable VLM Judges: State-Conditional Invariance and Presentation-Aware Diagnostics</a></td><td>48</td><td>5</td><td>Multimodal</td><td>embodied 과제용 VLM judge의 상태 조건 불변성 진단. 평가 신뢰성 문제는 로봇 평가에 유용</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2611.13782'>Integrating Action Prefix Prediction and Alignment Across Modalities for Multimodal Reinforcement Learning</a></td><td>48</td><td>5</td><td>RL</td><td>멀티모달 RL 표현 학습에 action prefix 예측과 정렬 추가. 표현 학습이나 기존 방법의 개선 수준</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2611.13654'>EgoHMP: Achieving Precise Human Motion Prediction in 3D Scenes via Egocentric Cues</a></td><td>46</td><td>4</td><td>Embodied AI</td><td>Egocentric 단서로 3D 장면 인간 동작 예측임. human-robot 상호작용과 연결 가능</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2611.13496'>Reasoning-Aware Relational Representation Learning for Open-Vocabulary Scene Graph Generation</a></td><td>46</td><td>3</td><td>Scene Graph</td><td>Open-vocabulary scene graph generation 관계 표현 학습임. scene graph 주제이나 benchmark 개선 위주</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2611.13785'>The Target Is a Predicate: Predicate-State Grounding for Semantic-Level Video Reasoning Segmentation</a></td><td>46</td><td>3</td><td>Video</td><td>Predicate 기반 video reasoning segmentation임. 새 task 정의이나 로봇 연관 약함</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2611.13150'>VIGOR: Benchmarking Visual Rationale Correctness in Multimodal Large Language Models</a></td><td>46</td><td>2</td><td>Multimodal</td><td>MLLM 시각 근거 정확성 benchmark임. 평가 관점은 좋으나 로봇 연관 약함</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2611.14033'>Few-Step Streaming Video Generation via Condition Shifting</a></td><td>46</td><td>2</td><td>Video</td><td>Few-step streaming video 생성 조건 이동임. 생성 효율 개선</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2611.12956'>ADIndex: Layer-Adaptive Sparse Attention Indexing via Group-Level Distillation</a></td><td>46</td><td>1</td><td>LG</td><td>Sparse attention indexer layer 적응 distillation임. 효율 추론이나 로봇 연관 약함</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2611.13120'>Just Image Transformers with Late-Stage Pixel Refinement</a></td><td>46</td><td>0</td><td>Generative</td><td>Latent-free diffusion transformer의 후단 pixel refinement임. 생성 모델 개선, 로봇 무관</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2611.14115'>LEASH: Stay Safe in Agentic Robotics</a></td><td>45</td><td>6</td><td>Safety</td><td>foundation model 기반 로봇 agent의 안전 위험과 평가를 다룸. 안전 benchmark 성격임.</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2611.13382'>Discrete Model-Based Diffusion for Combinatorial Optimization in Multi-Robot Task Allocation</a></td><td>45</td><td>5</td><td>Planning</td><td>이산 변수용 model-based diffusion으로 다중 로봇 task allocation을 풂. 방법은 타당하나 조합 최적화 특화임.</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2611.14183'>An Augmented Lagrangian Approach to Lifted Bellman Linear Programming</a></td><td>45</td><td>4</td><td>RL</td><td>lifted Bellman LP의 augmented Lagrangian 적용, offline RL. 이론적 개선이나 로봇 실험 불명확</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2611.14009'>Coding Agent Memory Post-Training II: Unlocking the Memory Potential of Pre-trained File Operations for Long-Horizon Tasks via On-Policy Distillation</a></td><td>45</td><td>3</td><td>Agent</td><td>장기 과제용 coding agent memory post-training, robot memory 관점 참고 가능임</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2611.14066'>Generalizing Causal Decision-Making: Markov Equivalence, Transportability and Counterfactuals</a></td><td>45</td><td>3</td><td>Causal</td><td>causal bandit의 transportability와 counterfactual 확장, 이론 중심임</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2611.13006'>Seeing Is Not Believing: Counterfactual Lesion Erasure Teaches a Small Medical Vision-Language Agent to Report Only What the Image Shows</a></td><td>45</td><td>1</td><td>Multimodal</td><td>counterfactual lesion erasure로 의료 VLM 환각 억제. counterfactual 아이디어는 흥미로우나 의료 한정</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2611.14025'>HiPFuse: Real-Time LiDAR Semantic Segmentation for Robotic Perception on Edge Devices</a></td><td>44</td><td>6</td><td>3D Vision</td><td>엣지 로봇용 실시간 LiDAR 의미 분할임. 로봇 인지 효율 중심이나 incremental</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2611.14076'>ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision</a></td><td>44</td><td>2</td><td>Multimodal</td><td>Global-zoom 지각 격차로 fine-grained 감독 구성임. 데이터 생성 아이디어이나 VLM 한정</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2611.13161'>Cognitive Multi-Agent Search and Rescue: Language-Grounded Hierarchical Reinforcement Learning for Collaborative Robotics</a></td><td>42</td><td>7</td><td>RL</td><td>언어 grounded 계층 RL 다중 로봇 SAR. 로봇이나 시뮬레이션 위주로 보이고 novelty 보통</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2611.13370'>AHEADance: Anticipatory Humanoid Dance from Streaming Audio</a></td><td>42</td><td>6</td><td>Humanoid</td><td>스트리밍 음악 예측으로 humanoid 춤을 생성함. 흥미로우나 응용 범위가 좁음.</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2611.13810'>Camera equalisation of an 11.5x drop in environmental illuminance: four imitation-learning policies on an SO-101 arm</a></td><td>42</td><td>6</td><td>IL</td><td>저가 SO-101에서 조명 변화가 IL policy 4종에 미치는 영향을 실측함. 실로봇 평가 분석이나 규모가 작음.</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2611.14049'>RedirectMimic: Local Motion Content Redaction for Humanoid Whole-Body Control</a></td><td>42</td><td>6</td><td>Humanoid</td><td>원본 reference를 받으면서 일부 동작을 대체하는 humanoid 제어기임. 문제 정의는 흥미로우나 범위가 좁음.</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2611.13203'>Audited Gradients, Anchored Policies: Model-Based Reinforcement Learning for Efficient Flow Control</a></td><td>42</td><td>4</td><td>RL</td><td>flow control용 model-based RL, surrogate 오류 감사 아이디어는 흥미로우나 유체 제어 한정임</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2611.14374'>Uncertainty-Aware Hybrid Offline Reinforcement Learning with Online Action Selection Enabled by Sparse Gaussian-Process Critics</a></td><td>42</td><td>4</td><td>RL</td><td>sparse GP critic 기반 hybrid offline RL과 online 행동 선택, 공정 제어 응용임</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2611.13280'>RetinexGS: Retinex-Inspired Gaussian Splatting for Low-Light RAW Reconstruction</a></td><td>42</td><td>3</td><td>3D Vision</td><td>저조도 RAW용 Retinex 3DGS임. 3DGS 응용이나 특화된 개선</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2611.13626'>FlashMotion: Ultra-Fast Long-Term 3D Motion Generation</a></td><td>42</td><td>3</td><td>Generative</td><td>초고속 장기 3D 인간 모션 생성임. embodied 시뮬레이션과 일부 연결</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2611.13628'>DepthGS: Depth-Guided Gaussian Splatting with Adaptive Regularization for High-Quality Surface Reconstruction</a></td><td>42</td><td>3</td><td>3D Vision</td><td>깊이 가이드 3DGS 표면 재구성임. incremental</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2611.12964'>Exploration via Exploitation: The Blessing of Reward Diversity in Personalized Federated RL</a></td><td>42</td><td>3</td><td>RL</td><td>개인화 federated RL에서 reward 다양성 활용임. 이론 성격 RL이나 로봇 연관 약함</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2611.13254'>Dependable Long-Horizon LLM Agents: A Trajectory-Centered Empirical Study of Where Errors Enter and Which Controls Reach Them</a></td><td>42</td><td>3</td><td>NLP</td><td>장기 LLM agent 오류 유입 경로 궤적 분석. failure 진단 관점은 연결되나 LLM 한정</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2611.13213'>Before Words, Beyond Speech: Evaluating Nonverbal Social Reasoning in Early Childhood</a></td><td>42</td><td>2</td><td>Video</td><td>유아 비언어 사회 추론 video benchmark임. 새 평가 축이나 로봇 연관 약함</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2611.13324'>Robust Flow Matching under Target Corruption and Label Noise</a></td><td>42</td><td>2</td><td>Generative</td><td>label noise에 강한 flow matching 학습, 생성 모델 일반 방법론임</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2611.13334'>Disentangling Multimodal Rotary Positional Embedding in Vision-Language Models</a></td><td>42</td><td>2</td><td>Multimodal</td><td>MRoPE에서 텍스트 위치 효과 분리. VLM 구조 개선이나 incremental</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2611.13818'>WAM is capable in BEHAVIOR-1K: the 2nd-place solution to the 2026 BEHAVIOR Challenge</a></td><td>40</td><td>7</td><td>VLA</td><td>BEHAVIOR 챌린지 2위 솔루션으로 world action model을 개선함. 엔지니어링 중심이나 성능 증거는 있음.</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2611.13929'>ReACT: Reflection-Consistent Modulation and Cross-Load Consistency for Humanoid Velocity Tracking Under Asymmetric Loads</a></td><td>40</td><td>6</td><td>Humanoid</td><td>비대칭 하중에서 humanoid 속도 추적을 반사 일관성으로 개선함. locomotion 특화 개선임.</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2611.13142'>DOBB: Dynamic Oriented Bounding Boxes for Multi-Agent Collision Avoidance under State Uncertainty and Heterogeneous Dynamics</a></td><td>40</td><td>5</td><td>RL</td><td>불확실성 하에서 oriented bounding box로 다중 에이전트 충돌 회피를 학습함. 표현 설계는 타당하나 범위가 좁음.</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2611.13712'>Broad-Persistent Advising in Interactive Reinforcement Learning via Latent State Encoding</a></td><td>40</td><td>5</td><td>RL</td><td>interactive RL 조언의 잠재 상태 기반 지속 활용. human feedback RL과 연결, incremental</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2611.12932'>URL-Sim: Unified and Regulated LiDAR Simulation for High-Fidelity Reconstruction of Dynamic Driving Scenes</a></td><td>40</td><td>3</td><td>3D Vision</td><td>LiDAR 3DGS 주행 장면 시뮬레이션임. 동적 장면 재구성이나 incremental 성격 강함</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2611.13177'>GroundCascade: Selective Second Opinions for GUI Grounding</a></td><td>40</td><td>3</td><td>Multimodal</td><td>GUI grounding에서 전체/확대 view 일치도로 선택적 재검토함. training-free, 에이전트 연관 낮음</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2611.13480'>Sharp Sample Complexity of KL-Regularized Reinforcement Learning</a></td><td>40</td><td>3</td><td>RL</td><td>KL-regularized RL sample complexity 이론, 이론 기여는 있으나 로봇과 거리임</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2611.14309'>MMDM: Measuring Massive Multitask Decision Making</a></td><td>40</td><td>3</td><td>Decision</td><td>System-1 decision model 대규모 benchmark, 의사결정 평가이나 로봇 직접성 약함</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2611.13615'>Synapse-Control: Making Agent Experience Actionable with Lightweight Runtime Control</a></td><td>40</td><td>3</td><td>Agent</td><td>LLM agent 경험을 런타임 제어로 활용함. 실패 진단과 비슷한 개념이나 로봇 아님.</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2611.14019'>Program-Aided Patchable Skill Evolution</a></td><td>40</td><td>3</td><td>Agent</td><td>프로그램 보조 patchable skill 진화임. 로봇 skill 개선과 개념이 유사하나 LLM agent임.</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2611.13127'>Activation-Guided Graph Retrieval for Cognitive Memory Reconstruction in Language Model Systems</a></td><td>40</td><td>3</td><td>NLP</td><td>활성화 기반 그래프 memory 검색 아키텍처. memory 주제는 맞으나 LLM 시스템 한정</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2611.14307'>TaoMate-R1: Temporal Role Specialization for Streaming Multi-Reference Video Generation</a></td><td>40</td><td>2</td><td>Video</td><td>Streaming 다중 reference 비디오 생성임. 생성 응용</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2611.14469'>C$^2$-Routing: Complementary Cropping and Compression for Efficient Vision-Language Inference</a></td><td>40</td><td>2</td><td>Multimodal</td><td>VLM 입력 crop과 압축 효율 추론임. 효율 방법이나 로봇 연관 약함</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2611.14328'>Forward-Value Discretization: Faster Stochastic Diffusion Sampling Without High-Order Approximation</a></td><td>40</td><td>2</td><td>Generative</td><td>stochastic diffusion sampler NFE 감소, diffusion policy 효율에 간접 연결임</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2611.14505'>Continual-ARC: Measuring Skill Acquisition over a Working Lifetime</a></td><td>40</td><td>2</td><td>Agent</td><td>agent harness continual learning 평가 benchmark, 로봇과 거리 있음</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2611.14326'>When Should Agents Remember? Falsification-Gated Self-Evolution for LLM Agents</a></td><td>40</td><td>2</td><td>NLP</td><td>falsification 기반 memory 기록 게이팅. memory 쓰기 기준 아이디어, LLM 한정</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2611.13384'>How Hyperbolic Are Hyperbolic Vision-Language Models?</a></td><td>40</td><td>1</td><td>Multimodal</td><td>Hyperbolic VLM의 exponential map 분석 연구임. 분석은 의미 있으나 로봇 무관</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2611.12988'>Third Eye: Beyond Immediate Gains in Recursive Self-Improvement</a></td><td>40</td><td>1</td><td>LG</td><td>재귀 자기 개선 후속 업데이트 유효성 평가임. 흥미로운 문제이나 LLM 수학 위주</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2611.14432'>One Policy for 100 Household Tasks: Our Solution for the 2026 BEHAVIOR Challenge</a></td><td>38</td><td>7</td><td>VLA</td><td>BEHAVIOR 챌린지 9위 단일 policy 솔루션임. 보고서 성격이며 기여는 엔지니어링임.</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2611.13850'>Taxonomy-Agnostic Neurosymbolic Grounding of Robot Kinematics</a></td><td>38</td><td>6</td><td>Embodied AI</td><td>URDF를 ontology로 변환하는 neurosymbolic 프레임워크. 로봇 task allocation에 유용하나 기여 범위 작음</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2611.13517'>Differentiable Filtering for Inertial Odometry</a></td><td>38</td><td>4</td><td>Estimation</td><td>필터 업데이트를 학습에 포함한 미분 가능 관성 오도메트리임. 방법은 타당하나 센싱 특화임.</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2611.13163'>High Probability Risk Control for Online Policy Learning</a></td><td>38</td><td>3</td><td>RL</td><td>online policy learning의 high-probability risk control, 이론 중심임</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2611.13275'>Off-policy Learning with Excursion Policies</a></td><td>38</td><td>3</td><td>RL</td><td>excursion policy 기반 off-policy RL 이론, 로봇 적용 증거 불명임</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2611.13135'>Which Successes Make Good References? Action-Sequence Alignment for Multi-Turn On-Policy Distillation</a></td><td>38</td><td>2</td><td>NLP</td><td>tool-use agent용 multi-turn on-policy distillation, 로봇 직접성 약함</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2611.14407'>Causal Concept Explanations for Deep Neural Models</a></td><td>38</td><td>2</td><td>XAI</td><td>causal concept explanation, 로봇과 거리 있음</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2611.13410'>SteerDistill: Quantizing LLM Agents via Closed-Loop Teacher Steering</a></td><td>38</td><td>2</td><td>NLP</td><td>양자화 LLM agent teacher steering 증류. 행동 괴리 보정 아이디어는 있으나 LLM 한정</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2611.14017'>Personalized Memory Rubrics: Learning What to Remember per User via Rubric-Guided Credit Assignment</a></td><td>38</td><td>2</td><td>NLP</td><td>사용자별 memory 갱신을 rubric credit assignment로 학습. memory 정책 학습 아이디어, LLM 한정</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2611.14320'>Don&#x27;t Just Trust Your Memory: Evidence-Linked Memory Reduces Memory-Induced Degradation in LLM Agents</a></td><td>38</td><td>2</td><td>NLP</td><td>증거 연결 memory로 memory 유발 성능 저하 감소. agent memory 신뢰성 관점, LLM 한정</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2611.14419'>Evaluating LLM-Generated World Models for Neuro-Symbolic Reasoning</a></td><td>38</td><td>2</td><td>AI</td><td>LLM 생성 world model 평가(POSG). 형식 world model 관점이나 로봇과 거리 있음</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2611.13530'>UniWeaver: Harnessing Unified Multimodal Models for Interleaved Text-Image Generation</a></td><td>38</td><td>1</td><td>Multimodal</td><td>Unified multimodal model의 interleaved 생성임. 로봇 무관</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2611.13004'>G-STAR: Group-Scaled Token Capacity for Deeply Compressed Autoregressive Generation</a></td><td>38</td><td>0</td><td>Generative</td><td>Autoregressive 이미지 생성 토큰 압축 개선임. 로봇 무관</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2611.13304'>DUO: Dual Readouts of Diffusion Models for OOD Detection</a></td><td>36</td><td>2</td><td>Generative</td><td>Diffusion OOD 탐지용 이중 readout임. 안전성 관련이나 로봇 연관 약함</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2611.13772'>RF3DGS: Reflection-Free 3D Gaussian Splatting with Self-Priors</a></td><td>36</td><td>2</td><td>3D Vision</td><td>반사 제거 3DGS임. 응용 특화</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2611.13808'>FastWild-GS: Minutes-Scale In-the-Wild Gaussian Splatting via Compact Per-Image Appearance Adaptation</a></td><td>36</td><td>2</td><td>3D Vision</td><td>In-the-wild 3DGS 빠른 외형 적응임. 효율 개선 위주</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2611.13523'>Parallel Broyden Methods for Efficiently Evaluating Nonlinear State Space Models</a></td><td>36</td><td>2</td><td>LG</td><td>비선형 state space model 병렬 평가용 Broyden 방법, 효율 방법론임</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2611.13172'>Continuous Angular Control in Text-to-Image Generation via Geometric Token Encoding</a></td><td>36</td><td>1</td><td>Generative</td><td>T2I 시계 각도 제어를 geometric token으로 해결함. 문제 정의 흥미로우나 범위 좁음</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2611.13251'>Curie&#x27;s Jarvis: Autonomous Robotic Chemistry Experiments from Printed Protocols</a></td><td>35</td><td>5</td><td>Manipulation</td><td>인쇄된 프로토콜을 읽어 화학 실험을 수행하는 시스템임. 통합 시스템 위주이고 학습 기여는 약함.</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2611.13528'>GEMOR-GS: Global Extrinsic-calibration-refined Mapping and Online Relocalization for 3D Gaussian-Splatting SLAM</a></td><td>35</td><td>5</td><td>3D Vision</td><td>LiDAR-관성-시각 3DGS SLAM에 외부 파라미터 보정과 재위치 추정을 더함. 공학적 통합 중심임.</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2611.14186'>Koopman Model-Based Reinforcement Learning</a></td><td>35</td><td>5</td><td>RL</td><td>Koopman 기반 model-based RL임. 고전적 설정이고 novelty 제한적임.</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2611.13344'>PneuGen: Task-Driven Agentic Co-Design of Soft Pneumatic Robots</a></td><td>35</td><td>4</td><td>Design</td><td>LLM agent로 soft pneumatic robot을 co-design함. 설계 자동화 응용임.</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2611.12958'>Embodied Science Agents: Making Embodied Experimental Design Learnable</a></td><td>35</td><td>4</td><td>Embodied AI</td><td>자율 실험실용 embodied 실험 설계 학습 포지션. 로봇 연관 있으나 실증 불명확</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2611.13946'>TreeAgent: Structure-Aware Memory Agent for Processing Long Hierarchical Data</a></td><td>35</td><td>2</td><td>NLP</td><td>구조 인지 memory agent. memory 주제나 LLM 텍스트 한정</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2611.13198'>Structured Kernel Surrogate Models for Multimodal Attribution</a></td><td>35</td><td>1</td><td>Multimodal</td><td>multimodal modality attribution용 kernel surrogate, 로봇 연결 약함</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2611.13218'>Wrong the Same Way: Cross-Prompt Sharing Both Suppresses and Amplifies Reward Hacking in RLVR</a></td><td>35</td><td>1</td><td>RL</td><td>RLVR reward hacking 분석, LLM 한정임</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2611.13524'>The RSI Tax: When Recursive Self-Improvement Is Not Worth the Cost</a></td><td>35</td><td>1</td><td>Agent</td><td>recursive self-improvement 비용 평가, LLM agent 한정임</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2611.14467'>A Theory of Policy Optimization in Post-Training: Coverage Collapse and Reference Resets</a></td><td>35</td><td>1</td><td>RL</td><td>post-training policy optimization 이론, LLM 한정임</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2611.12901'>Rethinking in Spikes: Mitigating Hallucinations in MDLMs with Step-Aware Decoding</a></td><td>35</td><td>1</td><td>Multimodal</td><td>MDLM 환각을 step-aware decoding으로 줄임. 로봇 무관하나 방법은 타당함.</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2611.13144'>Teaching the Harness: Student-Aware Skill Transfer for LLM Agents</a></td><td>35</td><td>1</td><td>NLP</td><td>LLM agent skill 전이에서 학생 인지 교수. 로봇 직접 연결 약함</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2611.14311'>Multimodal Abstention That Preserves Acquired Correct Answers</a></td><td>35</td><td>1</td><td>Multimodal</td><td>멀티모달 모델 abstention에서 정답 보존. 로봇 직접 연결 약함</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2611.13017'>Multi-Future Drafting: Mixture Block Drafters for Tree-Verified Speculative Decoding</a></td><td>35</td><td>0</td><td>LG</td><td>speculative decoding drafter 개선. 효율 추론이나 로봇 무관</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2611.13594'>Transformers Provably Learn Graph Search: Training Dynamics and the Exponential Power of Depth</a></td><td>35</td><td>0</td><td>LG</td><td>Transformer 그래프 탐색 학습 이론. 이론은 탄탄할 수 있으나 로봇 무관</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2611.13192'>Multimodal Road Closure Mapping via Cross-Modal Graph Attention</a></td><td>34</td><td>3</td><td>Navigation</td><td>교차 모달 graph attention으로 도로 폐쇄 지도화함. 내비게이션 인접이나 응용 중심</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2611.13820'>CASCADE: Constraint-Aware SCAffolded DEcomposition for Logical Anomaly Detection</a></td><td>34</td><td>2</td><td>CV</td><td>논리 이상 탐지 제약 분해임. 제조 검사 응용, 로봇 연관 약함</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2611.14436'>Metric-Aligned Group Relative Policy Optimization for Explainable Deepfake Detection</a></td><td>34</td><td>1</td><td>Multimodal</td><td>Deepfake 설명용 metric 정렬 GRPO임. RL 기법 적용이나 로봇 무관</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2611.14397'>A Margin Perspective on LoRA: Robustness to Catastrophic Forgetting and Adapter Merging (MaLoRA)</a></td><td>34</td><td>1</td><td>LG</td><td>LoRA margin 관점 forgetting 및 merging, 로봇 적용 증거 없음</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2611.13863'>Learn-To-Propagate: Distributionally Robust Motion Planning for Nonlinear Uncertain Systems</a></td><td>32</td><td>4</td><td>Planning</td><td>분포 강건 확률적 운동 계획을 위한 전파 학습임. 이론 중심이고 로봇 학습 연결은 약함.</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2611.14470'>TanCRAFT: Context-Reasoned Anticipatory Feedback for Assembly Tasks</a></td><td>32</td><td>4</td><td>HRI</td><td>조립 오류를 사전 개입하는 보조 시스템임. HRI 응용임.</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2611.13890'>DroneSegEdit: Adapting Pretrained Generative Editors for UAV Segmentation with Language-Grounded Verification</a></td><td>32</td><td>3</td><td>Multimodal</td><td>UAV 분할용 생성 편집기 적응임. 특정 dataset 위주</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2611.14286'>ForeseeDrive: Future-Token Conditioning for Anticipatory Generative Driving</a></td><td>32</td><td>3</td><td>Driving</td><td>미래 token 조건화로 생성형 주행 후보를 형성함. 자율주행 특화임.</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2611.14262'>Recurrent Modular Structure in Spiking Neural Network Reinforcement Learning</a></td><td>32</td><td>3</td><td>RL</td><td>모듈형 recurrent SNN RL. 흥미로우나 제한적 과제</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2611.14118'>TAMEing the Open-World Personalization: Towards Open-Set Personalized MLLM Assistant</a></td><td>32</td><td>2</td><td>Multimodal</td><td>Open-set 개인화 MLLM assistant임. 로봇 연관 약함</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2611.14153'>Unipolar Neuron Networks Trained by Recirculation for Reward-Based Continual Learning</a></td><td>32</td><td>2</td><td>RL</td><td>octopus 영감 unipolar 신경망 reward 기반 continual learning, 생물학 영감 소규모임</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2611.13560'>Are Dense Rewards Worth Their Tokens in GRPO?</a></td><td>32</td><td>2</td><td>RL</td><td>GRPO에서 dense reward 효용을 검증함. RL 일반론이나 LLM 한정임.</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2611.14256'>A Cross-Scenario Survey and Analysis of Self-Evolving Multimodal Agents</a></td><td>32</td><td>2</td><td>Multimodal</td><td>self-evolving 멀티모달 agent 서베이. 정리 위주</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2611.12997'>TIB: Sample-wise Tempered Information Bottleneck for Multimodal Attribution beyond Alignment Assumption</a></td><td>32</td><td>1</td><td>Multimodal</td><td>Multimodal attribution용 information bottleneck 개선임. 해석 연구, 로봇 연관 약함</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2611.13180'>X Marks the Spot: Diffusion for Image Geolocalization with Location Representations</a></td><td>32</td><td>1</td><td>CV</td><td>Diffusion 기반 geolocalization임. 로봇 연관 약함</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2611.13995'>Lipschitz-Controlled Flow Matching for Robust Image Restoration</a></td><td>32</td><td>1</td><td>Generative</td><td>Lipschitz 제어 flow matching 복원임. 안정성 아이디어이나 복원 과제 한정</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2611.13389'>AdjointFlow: Accelerating Scientific Inverse Problems with Physics-Based Transport</a></td><td>32</td><td>1</td><td>Generative</td><td>과학 역문제용 adjoint flow, 로봇 연결 약함</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2611.13414'>Free Lunch Uncertainty: Sequence-Level Rényi Entropy from Particle Decoding for Adaptive LLM Reasoning</a></td><td>32</td><td>1</td><td>NLP</td><td>LLM 추론 uncertainty와 adaptive compute, 로봇과 거리 있음</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2611.13498'>Evaluating Compositional Generalization in Transformers: The Role of Composition Equivalence and Module Coverage</a></td><td>32</td><td>1</td><td>LG</td><td>Transformer compositional generalization 평가, 로봇과 거리 있음</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2611.14387'>Blurring the Block Boundaries: Overlapping Block Denoising for Efficient Diffusion Language Models</a></td><td>32</td><td>1</td><td>NLP</td><td>diffusion LM 중첩 블록 denoising 효율화임. 로봇 무관함.</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2611.13016'>Permutation-Based Pre-trained Model Merging via Reciprocal Orthogonality</a></td><td>32</td><td>0</td><td>LG</td><td>model merging 이론, 로봇과 무관임</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2611.13249'>Domain-Routed Delta Optimization for Multi-Teacher On-Policy Distillation</a></td><td>32</td><td>0</td><td>NLP</td><td>multi-teacher on-policy distillation 파라미터 라우팅, 로봇과 무관임</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2611.13378'>Looping Deeper Without Growing the KV Cache: Recurrent Depth for Causal Encoder-Decoders</a></td><td>32</td><td>0</td><td>NLP</td><td>looped LM의 KV cache 효율화, 로봇과 무관임</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2611.13680'>Bootstrapped On-Policy Distillation</a></td><td>32</td><td>0</td><td>NLP</td><td>bootstrapped on-policy distillation, 로봇과 무관임</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2611.13714'>TRUER: Test-Time Reward Correction Using an Error-Aware Rectifier for Reinforcement Learning</a></td><td>32</td><td>0</td><td>NLP</td><td>test-time RL reward 보정, LLM 한정임</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2611.13742'>Plug-and-Play ADMM for Inverse Problems with Flow Matching Denoiser</a></td><td>32</td><td>0</td><td>Generative</td><td>flow matching denoiser PnP-ADMM 역문제, 로봇과 무관임</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2611.14015'>Margin-Guided Token Credit for Reinforcement Learning with Verifiable Rewards</a></td><td>32</td><td>0</td><td>NLP</td><td>RLVR token credit 할당, LLM 한정임</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2611.14246'>SinkState: On-the-Fly SVD of Recurrent States for Efficient Hybrid LLM Serving</a></td><td>32</td><td>0</td><td>NLP</td><td>hybrid LLM recurrent state SVD, 효율화이나 로봇과 거리임</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2611.14515'>AutoScaffold: AI-Guided Scaffolding for Reinforcement Learning of Language Models</a></td><td>32</td><td>0</td><td>NLP</td><td>RLVR scaffold 지원, LLM 한정임</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2611.13662'>NIF-VIO: Visual--Inertial Odometry Across Inertial and Non-Inertial Reference Frames</a></td><td>30</td><td>3</td><td>SLAM</td><td>비관성 좌표계에서의 VIO임. 특수 환경 상태 추정임.</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2611.13790'>RiSE-Drive: Risk-Sensitive Long-Horizon Candidate Evaluation for End-to-End Autonomous Driving</a></td><td>30</td><td>3</td><td>Driving</td><td>위험 민감 long-horizon 후보 평가 자율주행임. 도메인 특화임.</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2611.13540'>AgenticConflictLens: From Long Traffic Videos to Verifiable Conflict Evidence</a></td><td>30</td><td>2</td><td>Video</td><td>교통 영상 충돌 증거 agent임. 응용 중심</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2611.13870'>Spatial-Spectral Coupling as Attention: Scaling Shape Correspondence to High-Resolution Surfaces</a></td><td>30</td><td>2</td><td>3D Vision</td><td>고해상도 shape correspondence 확장임. 기하 처리, 로봇 연관 약함</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2611.13057'>Continuous-Time Set-Transformers for Asynchronous WiFi-IMU Indoor Localization</a></td><td>30</td><td>2</td><td>LG</td><td>WiFi-IMU 실내 측위, 센서 융합이나 일반 측위 수준임</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2611.12976'>Partition, Refine, and Detect: Preserving Novel Category Capacity in Open-Vocabulary Object Detection</a></td><td>30</td><td>1</td><td>CV</td><td>Open-vocabulary detection 표현 분할 개선임. 벤치마크 개선 위주</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2611.13262'>Adaptive Residual Quantization for Memory-Efficient Temporal Action Segmentation</a></td><td>30</td><td>1</td><td>Video</td><td>시간적 action segmentation 메모리 효율 양자화임. incremental</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2611.13997'>Specify Privacy Yourself: Assessing Inference-Time Personalized Privacy Preservation Ability of Large Vision-Language Models</a></td><td>30</td><td>1</td><td>Multimodal</td><td>LVLM 개인화 privacy 평가임. 로봇 무관</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2611.13356'>When Are Predictions Enough? An Evaluation Protocol for Frozen Expert Composition</a></td><td>30</td><td>1</td><td>LG</td><td>frozen expert 조합 평가 protocol, 로봇 연결 약함</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2611.13448'>Fermat ProbCover: Coverage-Based Active Learning on Fermat Distance Graphs</a></td><td>30</td><td>1</td><td>LG</td><td>Fermat distance 기반 active learning, 로봇과 무관임</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2611.13457'>Deep Personalization: Continuous Context Observation for Local Proactive Agents</a></td><td>30</td><td>1</td><td>Agent</td><td>로컬 proactive agent 맥락 관찰, 로봇과 거리 있음</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2611.13599'>Unified Optimization of Traffic Signal and Lane Channelization for an Isolated Intersection Using Reinforcement Learning</a></td><td>30</td><td>1</td><td>RL</td><td>교통신호 및 차선 RL 최적화, 로봇과 무관임</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2611.14263'>Chain of Physics: Supporting Fault Diagnosis with Engineering-Inspired Large Language Model Reasoning</a></td><td>30</td><td>1</td><td>Agent</td><td>LLM 기반 물리 fault diagnosis, 산업 설비 응용임</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2611.14323'>Auditing the Judge: Internal Signals for LLM Reasoning Assurance</a></td><td>30</td><td>1</td><td>NLP</td><td>LLM judge 내부 신호 보증, failure detection 관점에서 약하게 연결임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2611.14424'>DnNP: Denoising Input Uncertainty in Neural Processes</a></td><td>30</td><td>1</td><td>LG</td><td>입력 노이즈 neural process, 로봇과 거리 있음</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2611.13107'>Catch It Where It Happens: Real Time Error Correction During LLM Reasoning</a></td><td>30</td><td>1</td><td>NLP</td><td>LLM 추론 중 실시간 오류 교정임. 로봇 무관하나 test-time 개념은 있음.</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2611.13552'>How Post-Training Influences Verbalized Algorithmic Computation in Language Models</a></td><td>30</td><td>1</td><td>NLP</td><td>post-training이 verbalized 계산에 미치는 영향 분석임. 로봇 무관함.</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2611.13675'>OpticalRAG: Pixel-Space Compression for Token-Efficient Retrieval-Augmented Generation</a></td><td>30</td><td>1</td><td>Multimodal</td><td>픽셀 공간 압축으로 RAG 토큰 효율을 높임. 로봇 무관함.</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2611.12992'>ZeroPoint: Lightweight Energy-Based Decision Model</a></td><td>30</td><td>1</td><td>LG</td><td>경량 energy-based 결정 모델. 아이디어 흥미롭지만 실증 제한적</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2611.13015'>From Questions to Decisions: Benchmarking How LLM Agents Acquire Decision-Relevant Information from Human Beings</a></td><td>30</td><td>1</td><td>NLP</td><td>LLM agent의 질문을 통한 정보 획득 benchmark. 로봇 무관</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2611.13336'>Veritas: A Verifier Generation Harness for Agent Tasks</a></td><td>30</td><td>1</td><td>NLP</td><td>agent task 검증기 자동 생성 harness. 로봇 직접 연결 약함</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2611.14418'>Precision on Demand: Escalating Weight Bits at Uncertain Decoding Steps in a Small Local Model</a></td><td>30</td><td>1</td><td>LG</td><td>불확실 step에서만 가중치 비트 상승. 효율 추론 아이디어나 소형 실험</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2611.12998'>Linear Probes to Bayesian Manifolds: Geometry of Arithmetic in Large Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 산술 표현의 기하 구조 분석, probe 해석 방법론으로 로봇과 무관임</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2611.13005'>The Shape of a Program: Path Signatures for Trace-to-Program Induction</a></td><td>30</td><td>0</td><td>LG</td><td>trace에서 program 유도하는 path signature, 로봇과 거리 있음</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2611.13077'>One Temperature to Rule Them All?</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM sampling temperature 분석, 로봇과 무관임</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2611.13276'>An Analytical Model of Compute-limited Multistage Training Pipelines</a></td><td>30</td><td>0</td><td>LG</td><td>multistage 학습 compute 배분 해석 모델, 로봇과 무관임</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2611.13545'>Closing the BF16-FP16 Convergence Speed Gap in RL Post-Training with Stochastic Rounding</a></td><td>30</td><td>0</td><td>NLP</td><td>RL post-training BF16 stochastic rounding, 로봇과 무관임</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2611.13647'>CP-MLPs: A Tensor-Rank Theory of Tied and Untied MLP Blocks</a></td><td>30</td><td>0</td><td>LG</td><td>MLP tensor rank 이론, 로봇과 무관임</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2611.13868'>Mechanistic Interpretability of Deep Neural Networks: Methods, Frameworks, and Perspectives</a></td><td>30</td><td>0</td><td>LG</td><td>mechanistic interpretability survey, 로봇과 무관임</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2611.13885'>Are Causal Neuron Circuits Unique and Transferable?</a></td><td>30</td><td>0</td><td>NLP</td><td>causal neuron circuit 유일성 분석, 로봇과 무관임</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2611.13955'>RB-LDC: Redundancy-Balanced Latent Coding for Noise-Robust Diffusion Latents</a></td><td>30</td><td>0</td><td>Generative</td><td>diffusion latent 노이즈 강건 coding, 로봇과 무관임</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2611.14399'>REAL Loss: Optimizing Real Expected Acceptance Length for Speculative Decoding</a></td><td>30</td><td>0</td><td>NLP</td><td>speculative decoding 손실 설계, 로봇과 무관임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2611.14168'>Representational Atoms in Neural Networks</a></td><td>30</td><td>0</td><td>LG</td><td>신경망 representational atoms 분석임. 로봇 무관함.</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2611.12937'>Tracing Psychometric Inference in Large Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 내부 심리측정 구조 분석. 로봇 무관, 분석 위주</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2611.12954'>Physics2Weight: Direct Neural Network Architecture and Weight Generation from Physical Laws Using Large Language Models</a></td><td>30</td><td>0</td><td>LG</td><td>LLM으로 PDE용 신경망 가중치 직접 생성. 아이디어는 새로우나 로봇 무관</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2611.13140'>Agreeing on the Answer but Not the Reason: Measurement Limits of LLM Reasoning Failure Taxonomies</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 추론 실패 taxonomy 측정 한계 분석. 로봇 무관</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2611.13975'>Understanding Mixture-of-Experts Language Models Beyond Expert Boundaries</a></td><td>30</td><td>0</td><td>NLP</td><td>MoE 뉴런 수준 전문화 분석. 로봇 무관</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2611.13268'>Force-Closure Condition for Cooperative Multi-robot Pushing of Rectangular Objects</a></td><td>28</td><td>4</td><td>Manipulation</td><td>직사각형 물체 다중 로봇 push의 force closure 필요충분조건을 유도함. 이론은 깔끔하나 좁은 문제임.</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2611.13766'>FAME-QP: A GPU-Accelerated Quadratic-Programming Solver for Real-Time Model Predictive Control</a></td><td>28</td><td>4</td><td>Control</td><td>MPC용 GPU 가속 QP solver임. 시스템 엔지니어링 위주임.</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2611.13494'>Route-Time Conflict Maps for Cooperative End-to-End Autonomous Driving</a></td><td>28</td><td>3</td><td>Driving</td><td>협력 자율주행에서 route-time 충돌 지도로 진행 시점을 계획함. 자율주행 특화임.</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2611.14414'>SIGMO: Sigmoid Gated Interaction-Aware Motion Planning</a></td><td>28</td><td>3</td><td>Planning</td><td>상호작용 인지 sigmoid gating 운동 계획임. 자율주행 계획 특화임.</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2611.12933'>Auditable Human-Agent Teams for Autonomous X-ray Experimentation</a></td><td>28</td><td>3</td><td>Agent</td><td>X선 실험을 위한 감사 가능 인간-agent 팀임. 실험 자동화 응용임.</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2611.13906'>Target Selection with a Disappearing-Stimulus Mixed-Reality P300 Interface: Feasibility and Object-Distinguishable Versus Uniform Cues</a></td><td>28</td><td>2</td><td>HCI</td><td>MR P300 BCI 목표 선택, 휠체어 목표 지정 응용임</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2611.14247'>Personalized Affective Perception via Continual Learning in Human-Agent Negotiation</a></td><td>28</td><td>2</td><td>CV</td><td>협상용 개인화 표정 인식 continual learning. HRI 약한 연결</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2611.13759'>Exploring Synchrony for Communication in Modular Neural Networks</a></td><td>28</td><td>1</td><td>LG</td><td>Modular network 동기성 통신 탐색임. 로봇 연관 약함</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2611.13565'>Investigating Composite Modeling in Multi-Objective Bayesian Optimization for Scientific Design</a></td><td>28</td><td>1</td><td>LG</td><td>과학 설계용 multi-objective BO, 로봇과 거리 있음</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2611.13862'>Where to Approximate in Neurosymbolic Inference?</a></td><td>28</td><td>1</td><td>Neurosymbolic</td><td>neurosymbolic WMC 근사 위치 분석, 로봇과 거리 있음</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2611.14425'>Quantifying the Sampling Frequency Invariance of Time-Series Foundation Models for Sensor Data Applications</a></td><td>28</td><td>1</td><td>TimeSeries</td><td>센서 TSFM 샘플링 주파수 불변성, 로봇과 거리 있음</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2611.12902'>TimeOmni-o1: Bidirectionally Coupling Time Series Foundation Models and LLMs for Multimodal Reasoning and Forecasting</a></td><td>28</td><td>1</td><td>LG</td><td>시계열 FM과 LLM 결합 추론임. 로봇 관련성 낮음.</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2611.13855'>Beyond Passive Imitation: On-Policy Mid-Training Distillation for Language Models</a></td><td>28</td><td>1</td><td>NLP</td><td>on-policy mid-training distillation임. 로봇 무관함.</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2611.14383'>An Energy-Based Perspective on Machine Learning</a></td><td>28</td><td>1</td><td>LG</td><td>energy-based 관점 튜토리얼. 새 방법 아님</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2611.13306'>Train High, Ship Low: Efficient LoRA Synchronization for Distributed On-Policy Post-Training</a></td><td>28</td><td>0</td><td>LG</td><td>분산 post-training LoRA 동기화 효율화, 로봇과 무관임</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2611.13322'>MicroLens: Read, Trace, and Rewire the Residual Stream with Two Lenses</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM residual stream 해석 도구, 로봇과 무관임</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2611.13331'>Stochastic Projections and Rank-Aware Learning Rates for Federated LoRA</a></td><td>28</td><td>0</td><td>LG</td><td>federated LoRA 학습률, 로봇과 무관임</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2611.13431'>You Don&#x27;t Need Feature Learning to Do In-Context Learning</a></td><td>28</td><td>0</td><td>LG</td><td>ICL에 feature learning 불필요함을 보인 이론, 로봇과 무관임</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2611.13452'>SLIC: Reinforcement Fine-Tuning Small LMs for Multi-Turn Analog Circuit Optimization</a></td><td>28</td><td>0</td><td>NLP</td><td>아날로그 회로 최적화 RL fine-tuning, 로봇과 무관임</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2611.13477'>Leveraging Psychophysical Attentional Distribution for Gaze-Augmented Reward Modeling</a></td><td>28</td><td>0</td><td>NLP</td><td>gaze 기반 reward modeling, 로봇과 무관임</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2611.13534'>Beyond the Log-Linear Frontier: Pre-Asymptotic Analysis of Finite-Budget Neural Scaling Laws</a></td><td>28</td><td>0</td><td>LG</td><td>scaling law 해석 이론, 로봇과 무관임</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2611.13543'>Sanity Checks for Attention Surgery: Null Models and Matched Interventions for Representation-Motivated Design</a></td><td>28</td><td>0</td><td>NLP</td><td>attention 수정 sanity check, 로봇과 무관임</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2611.13548'>Massive Activations Confound Sparse Autoencoders</a></td><td>28</td><td>0</td><td>NLP</td><td>SAE와 massive activation, 로봇과 무관임</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2611.13572'>Market-Conditioned JEPA: Learning from Unpredictable Market Shocks</a></td><td>28</td><td>0</td><td>LG</td><td>금융 시계열 JEPA, 로봇과 무관임</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2611.13730'>Deterministic, Reproducible Inference in Exact Integer Arithmetic, and Verifiable Distributed Inference as Its Consequence</a></td><td>28</td><td>0</td><td>LG</td><td>정수 연산 결정적 추론, 로봇과 무관임</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2611.13748'>When Covariance Is Not Enough: Kernel-Based Regularization for Single-Cell Counterfactuals</a></td><td>28</td><td>0</td><td>Bio</td><td>단일세포 counterfactual 편집, 로봇과 무관임</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2611.13777'>Omni-JEV: Text and Dual-Stream Speech Decisions</a></td><td>28</td><td>0</td><td>Speech</td><td>full-duplex 대화 결정 모델, 로봇과 거리 있음</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2611.13913'>Learning from First Discrepancies with Joint Reset and Pilot Guarantees</a></td><td>28</td><td>0</td><td>LG</td><td>first discrepancy 학습 이론, 로봇과 무관임</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2611.14046'>Structured Confidence Perturbation via Fisher Geometry for Adversarial Training</a></td><td>28</td><td>0</td><td>CV</td><td>adversarial training Fisher 기하, 로봇과 무관임</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2611.14134'>Right for the Wrong Reasons? Evaluating Plausibility and Behavioral Change in Explanation-Guided Learning</a></td><td>28</td><td>0</td><td>LG</td><td>explanation-guided learning 평가, 로봇과 무관임</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2611.14357'>The Unused Input: The Initial State as a Conditioning Interface for Recurrent TSFMs</a></td><td>28</td><td>0</td><td>TimeSeries</td><td>recurrent TSFM 초기 상태 conditioning, 로봇과 무관임</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2611.13270'>What drives the emergence of symbolic mechanisms in large language models?</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM 상징 메커니즘 출현 요인 분석임. 로봇 무관함.</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2611.12938'>Graph Visualizations in Prompts for Knowledge Graph Question Answering</a></td><td>28</td><td>0</td><td>Multimodal</td><td>KGQA에 그래프 이미지 추가 효과 평가. 로봇 무관, 경험적 분석</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2611.14514'>Contrastive Discovery: Open-Ended Scientific Discovery over Competing Explanations</a></td><td>28</td><td>0</td><td>NLP</td><td>경쟁 설명 대조 과학 발견 agent. 로봇 무관</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2611.12950'>SetPrint: Black-Box LLM Fingerprinting via Setwise Correspondence of Response Changes</a></td><td>27</td><td>0</td><td>NLP</td><td>블랙박스 LLM 지문 식별. 로봇 무관, 방법은 무난</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2611.13510'>Distribution Shift Detection in Remote Sensing Imagery using Machine Learning Models</a></td><td>26</td><td>2</td><td>CV</td><td>UAV 원격탐사 distribution shift 탐지임. 응용 중심</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2611.13310'>ABRR: Transforming Temporal Sentence Grounding with Wasserstein-Adaptive Refinement and Precision Ranking</a></td><td>26</td><td>0</td><td>Video</td><td>Temporal sentence grounding 개선임. benchmark 개선 위주</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2611.13620'>When to Start Denoising? Adaptive Denoising Entry for Generative Video Compression</a></td><td>26</td><td>0</td><td>Video</td><td>생성 비디오 압축 denoising 시작점 선택임. 로봇 무관</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2611.12955'>Predictive Surprise as Self-Grounding Concept Bottleneck for Interpretable Time Series</a></td><td>26</td><td>0</td><td>LG</td><td>시계열 개념 병목 해석 모델임. 로봇 무관</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2611.12949'>Maze Runner: Autonomous Maze Navigation with Line-Based Localization and Control Barrier Functions</a></td><td>25</td><td>5</td><td>Navigation</td><td>LiDAR 선 추출과 CBF 기반 미로 주행 스택임. 시뮬레이션 한정이고 공학적 통합 위주임.</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2611.14062'>A human-in-the-loop Control Paradigm for Construction Robotics: From VR-Guided Teleoperation to Semi-Autonomous Dual-Arm Operation</a></td><td>25</td><td>5</td><td>Teleop</td><td>VR 원격조작에서 반자율 이중 팔로 전환하는 건설 로봇 제어 패러다임임. 시스템 위주임.</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2611.13204'>Ground Reaction Force-Aware Model Predictive Control for Underactuated Upright Physical Assistance</a></td><td>25</td><td>4</td><td>Control</td><td>GRF 인지 MPC로 재활 보조 로봇을 제어함. 도메인 특화 제어 연구임.</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2611.13472'>Rhythmic-Semantic Co-Speech Gestures for Emotional Dialogue in Robots</a></td><td>25</td><td>4</td><td>HRI</td><td>감정 인지 리듬·의미 제스처 생성 시스템임. HRI 응용이고 조작과 무관함.</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2611.14373'>Gaussian Process-Augmented Model Predictive Contouring Control for 6-DoF Trajectory Tracking with a Holonomic AUV</a></td><td>25</td><td>3</td><td>Control</td><td>홀로노믹 AUV용 GP 보강 MPCC임. 도메인 특화 제어임.</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2611.13271'>RaMOD: Moving-Object Detection from Raw mmWave Radar Cubes under Ego Motion</a></td><td>25</td><td>2</td><td>CV</td><td>raw mmWave 레이더 큐브에서 이동 물체를 검출함. 자율주행 센싱 특화임.</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2611.13426'>BioMem: Agentic Memory for Biomedical LLM Agents</a></td><td>25</td><td>2</td><td>NLP</td><td>생의학 LLM agent memory임. 도메인 특화임.</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2611.13563'>Benchmarking Vendor-Guided Optimizations on Edge NPUs: From NPU Only to End-to-End Performance. Extended technical report</a></td><td>25</td><td>2</td><td>LG</td><td>엣지 NPU 최적화 benchmark. 온디바이스 배포 참고 수준</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2611.13646'>MouldIt: Data Efficiency of Multi-Task Temporal Representation Learning in Injection Moulding</a></td><td>25</td><td>1</td><td>LG</td><td>사출성형 표현학습 data efficiency, 산업 응용 한정임</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2611.14266'>Physics-Constrained Autoencoder for Interpretable Health Representation Learning in Turbofan Engines</a></td><td>25</td><td>1</td><td>LG</td><td>터보팬 health index autoencoder, 로봇과 무관임</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2611.12903'>SELD: Detecting Silent Evidence Loss in Context Compression beyond the Answer</a></td><td>25</td><td>1</td><td>NLP</td><td>컨텍스트 압축의 증거 손실 탐지임. 로봇 무관함.</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2611.14100'>Sckwoky at SHROOM-Visions: Character-Level Hallucination-Span Detection in Image-Conditioned VLMs via Dual-Prompted LoRA Decoders</a></td><td>25</td><td>1</td><td>Multimodal</td><td>VLM 환각 span 탐지 shared task 시스템임. 로봇 무관함.</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2611.14364'>ARE-bench: Benchmarking Agents&#x27; Research Ability in Real-World Researcher Sessions and Workspaces</a></td><td>25</td><td>1</td><td>Agent</td><td>연구 agent benchmark임. 로봇 무관함.</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2611.12940'>Reinforcement Learning based control of Cancer Chemotherapy treatments</a></td><td>25</td><td>1</td><td>RL</td><td>항암 치료 RL 제어. 새로움 약하고 로봇 무관</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2611.13001'>One Table, Many Queries: Benchmarking Generalist Tabular Models Across Generation, Imputation, and Prediction</a></td><td>25</td><td>0</td><td>LG</td><td>tabular 모델 benchmark, 로봇과 무관임</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2611.13137'>Byzantine-Robust Muon: Resilient Momentum Orthogonalization for Distributed Learning</a></td><td>25</td><td>0</td><td>LG</td><td>분산 학습용 Byzantine-robust Muon optimizer, 로봇과 무관임</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2611.13186'>Prediction-Powered LLM Ranking with Adaptively Collected Human Feedback</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM 랭킹용 prediction-powered 추정, 로봇과 무관임</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2611.13199'>XAI-Driven Confidence Estimation for OOD-Resilient Runtime Prediction</a></td><td>25</td><td>0</td><td>LG</td><td>OOD 런타임 예측 confidence, 자원관리 응용임</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2611.13383'>Settling the Burn-in Gap: Sharp Risk Bounds for Tail-Averaged SGD in Linear Regression</a></td><td>25</td><td>0</td><td>LG</td><td>SGD 선형회귀 risk bound 이론, 로봇과 무관임</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2611.13758'>Mixed Signals: Weight-Space Programming for EEG and ECG</a></td><td>25</td><td>0</td><td>LG</td><td>EEG/ECG weight-space programming, 로봇과 무관임</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2611.13794'>AnchorMTS: Multi-View Signal Representation and Forecast-Anchored Fusion for Long-Term Time-Series Forecasting</a></td><td>25</td><td>0</td><td>TimeSeries</td><td>장기 시계열 예측 multi-view 융합, 로봇과 무관임</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2611.14491'>TimeSeek: Multi-Task and Multi-Domain Pretraining for Generalized Time Series Analytics</a></td><td>25</td><td>0</td><td>TimeSeries</td><td>시계열 foundation model 사전학습, 로봇과 무관임</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2611.12995'>Capacity Allocation at the Source: Sparse Target Optimization for LLM Knowledge Editing</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM 지식 편집용 sparse target 최적화임. 무관함.</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2611.13607'>One Byte, One Token: Byteifying a 27B Hybrid-Attention LLM with Self-Generated Data</a></td><td>25</td><td>0</td><td>NLP</td><td>27B LLM byte 단위 변환임. 무관함.</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2611.12935'>Train on prefill, monitor at decode: Using sparse autoencoders for topic monitoring</a></td><td>25</td><td>0</td><td>NLP</td><td>SAE 기반 topic 모니터링임. 무관함.</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2611.12959'>Monitoring One Channel Is Not Communication Control: Causal Evidence for Adaptive Reallocation of Joint Message--Route Codes</a></td><td>25</td><td>0</td><td>RL</td><td>학습된 통신 프로토콜 모니터링 분석. 로봇 무관</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2611.12961'>RBLA+: Efficient Rank-Specific LoRA Adapter Extraction for Federated Fine-Tuning with Heterogeneous Clients</a></td><td>25</td><td>0</td><td>LG</td><td>federated LoRA 집계 개선. incremental, 로봇 무관</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2611.13232'>W-ISA: Transactional Execution of Weight-Space Intervention Programs</a></td><td>25</td><td>0</td><td>NLP</td><td>가중치 개입 프로그램 실행 런타임. 로봇 무관</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2611.13233'>Decisions by Discrimination: Differential Evidence for Medical Reasoning</a></td><td>25</td><td>0</td><td>NLP</td><td>의료 MCQ 차별 증거 추론. 로봇 무관</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2611.13236'>NCP: Verifier-Guided Optimization of Weight-Space Control Policies</a></td><td>25</td><td>0</td><td>NLP</td><td>가중치 개입 정책 검증기 최적화. 로봇 무관</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2611.13325'>F3-AGI v4.0: Bioenergetically-Gated Active Inference, Metaplastic Preconditioning, and Residual Program Synthesis for Sample-Efficient Abstract Reasoning</a></td><td>25</td><td>0</td><td>AI</td><td>ARC-AGI 추론용 복합 기법. 로봇 무관</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2611.13541'>Agent Benchmarks Stop Ranking Before They Run Out of Tasks</a></td><td>25</td><td>0</td><td>NLP</td><td>agent benchmark 포화 분석. 로봇 무관</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2611.13701'>Topological Dynamics Under Non-Stationary Supervision: Persistent Homology of Neural Network Weight Evolution</a></td><td>25</td><td>0</td><td>LG</td><td>가중치 위상 동역학 분석. 로봇 무관</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2611.14122'>Hx2Dx: From Anamnesis to Diagnosis - A Multimodal Arena for Conversational Clinical Reasoning in LLMs</a></td><td>25</td><td>0</td><td>NLP</td><td>대화형 임상 추론 arena. 로봇 무관</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2611.14171'>BARS: Budget-Aware Sequential Sampling with Refusal for Majority Identification under Unknown Distributions</a></td><td>25</td><td>0</td><td>LG</td><td>majority 식별 순차 샘플링. 로봇 무관</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2611.14355'>CLADE: Category-Level Answering from Deficient Evidence in Retrieval-Augmented Language Models</a></td><td>25</td><td>0</td><td>NLP</td><td>RAG 범주 수준 답변. 로봇 무관</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2611.14492'>ReTrace: Distilling Tool-Using Agents into Planner-Free Workflows</a></td><td>25</td><td>0</td><td>NLP</td><td>SOP agent를 workflow로 증류. 로봇 무관</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2611.13511'>TMAL: Topology-preserving Multi-offset Affinity Learning for Curvilinear Structure Segmentation</a></td><td>24</td><td>1</td><td>CV</td><td>곡선 구조 분할용 affinity 학습임. 도메인 특화</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2611.12975'>Attribute-Evidence Learning with Multimodal Prompt for Generalized Category Discovery</a></td><td>24</td><td>0</td><td>CV</td><td>Generalized category discovery 속성 prompt 추가임. 로봇 무관, incremental</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2611.13784'>Marrying Capacity and Precision for Efficient 2D Gaussian Image Representation</a></td><td>24</td><td>0</td><td>CV</td><td>2D Gaussian 이미지 표현 효율화임. 로봇 무관</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2611.13807'>Relaxing Cross-Modal Correspondence for Multimodal Remote Sensing Pretraining</a></td><td>24</td><td>0</td><td>CV</td><td>원격탐사 pretraining 대응 완화임. 로봇 무관</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2611.13992'>Pulse or Provenance? What rPPG-Based Deepfake Detectors Learn</a></td><td>24</td><td>0</td><td>CV</td><td>rPPG deepfake 탐지 분석임. 로봇 무관</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2611.14097'>Stylization as Geodesic Navigation on Diffusion Manifolds</a></td><td>24</td><td>0</td><td>Generative</td><td>Diffusion manifold 얼굴 stylization임. 로봇 무관</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2611.14496'>RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval</a></td><td>24</td><td>0</td><td>CV</td><td>원격탐사 JEPA 교차 센서 검색임. 로봇 무관</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2611.14498'>Measuring Robustness and Efficiency in a Connectome-Constrained Fly Visual System Model: Linking an Adversarial and a Perceptual Illusion</a></td><td>24</td><td>0</td><td>CV</td><td>초파리 시각계 모델 견고성 분석임. 로봇 연관 약함</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2611.13114'>ASPIRE: An Agentic System-Identification Platform for Iterative Reasoning and Exploration</a></td><td>22</td><td>3</td><td>LG</td><td>LLM agent가 system identification 방법을 고르는 프레임워크임. 로봇 학습과 거리 있음.</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2611.13292'>Large Language Model Explainability for Planning Lunar Rover Trajectories under Uncertainty</a></td><td>22</td><td>3</td><td>Planning</td><td>달 탐사 로버 경로 계획에 LLM 설명을 붙임. 로봇 학습 관련성 낮음.</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2611.13957'>AVCC: Audio-Visual Conversation Corpus for Turn-Taking Prediction with a Human Benchmark</a></td><td>22</td><td>3</td><td>HRI</td><td>대화 turn-taking 예측 오디오-비주얼 코퍼스임. 소셜 로봇 응용에 한정됨.</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2611.12911'>Uncovering the Blind Spots of OKS-mAP: A Unified Protocol for Occlusion, Joint-Angle, and Temporal Evaluation of 2D Pose Estimators</a></td><td>22</td><td>1</td><td>CV</td><td>2D pose 평가 지표 보완 프로토콜임. 로봇 연관 약하고 기여가 평가 수준에 그침</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2611.13488'>When Reconstruction Helps Event-Camera Person Triggers</a></td><td>22</td><td>1</td><td>CV</td><td>Event camera 사람 trigger용 복원 비교임. 소규모 비교</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2611.14218'>ViGA-FLAME: Aligning Latent Visual and Geometric Representations for Robust 3D Head Expression Estimation</a></td><td>22</td><td>1</td><td>3D Vision</td><td>3D 머리 표정 추정임. 로봇 무관</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2611.13726'>Weighted-AoI-Driven UAV Trajectory and Reporting for Dynamic CKM Tracking</a></td><td>22</td><td>1</td><td>Network</td><td>UAV 궤적과 CKM tracking, 통신 응용임</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2611.14196'>Joint Quantization and Dynamic Partitioning for Context-Aware Edge Vision Transformers</a></td><td>22</td><td>1</td><td>CV</td><td>차량 엣지 ViT 분할 추론. 시스템 최적화</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2611.12974'>StatPrompt-LLM: A Lightweight Statistical Refinement for Foundation-Style Time-Series Forecasting</a></td><td>22</td><td>0</td><td>LG</td><td>시계열 예측 통계 prompt 보정임. incremental</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2611.12990'>Multimodal Graph Learning: A Survey of Models, Benchmarks, and Frontiers</a></td><td>22</td><td>0</td><td>LG</td><td>Multimodal graph learning 서베이임. 로봇 무관</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2611.13052'>Explanation-Aware Fairness Beyond Output Parity: Joint Output-Attribution Regularization for Medical Image Classification</a></td><td>22</td><td>0</td><td>CV</td><td>의료영상 fairness 정규화, 로봇과 무관임</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2611.13561'>Discovering Structurally Plausible and Interpretable Cognitive Models with Large Language Models</a></td><td>22</td><td>0</td><td>Cognitive</td><td>LLM으로 인지 모델 탐색, 로봇과 무관임</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2611.13624'>Multifidelity Operator Inference for Non-intrusive Model Reduction under Data Scarcity</a></td><td>22</td><td>0</td><td>LG</td><td>multifidelity operator inference, 로봇과 무관임</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2611.13708'>FedVP: Federated Learning across Heterogeneous Models by Pooling Locally Trained Verifiers</a></td><td>22</td><td>0</td><td>NLP</td><td>이종 모델 federated learning, 로봇과 무관임</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2611.13765'>Beyond Interaction Scores: Selecting Feature Interactions via Independent Replication</a></td><td>22</td><td>0</td><td>LG</td><td>feature interaction 선택, 로봇과 무관임</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2611.13994'>BioXArena-Pro: a research-grade benchmark for autonomous biomedical machine learning agents</a></td><td>22</td><td>0</td><td>Agent</td><td>생의학 ML agent benchmark, 로봇과 무관임</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2611.14126'>Hierarchical Graph Representation Learning with Pooling-Induced Substructures</a></td><td>22</td><td>0</td><td>LG</td><td>graph pooling 계층 표현, 로봇과 무관임</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2611.14210'>Tree-Ising: Repairing Language Models with Bit-Level Ising Edits</a></td><td>22</td><td>0</td><td>NLP</td><td>weight-space programming 기반 LLM 수정, 로봇과 무관임</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2611.14312'>PSL-RGHA: Parallel Split Learning with Reference Gradient Half-Space Alignment for Mitigating Gradient Divergence</a></td><td>22</td><td>0</td><td>LG</td><td>split learning gradient 정렬, 로봇과 무관임</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2611.12953'>Agent Architecture Cost-Success Trade-offs: A Controlled Evaluation across Enterprise-Style SOPs</a></td><td>22</td><td>0</td><td>NLP</td><td>엔터프라이즈 agent 아키텍처 비교 평가. 로봇 무관</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2611.13020'>ChipOmni: A General-Purpose AI Agent for Electronic Design Automation</a></td><td>22</td><td>0</td><td>NLP</td><td>EDA용 범용 agent. 로봇 무관</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2611.13246'>ExpertCrowd-SWE: Measuring Frontier Coding Agents on Expert-Authored Engineering Tasks in Unfamiliar Codebases</a></td><td>22</td><td>0</td><td>NLP</td><td>전문가 작성 SWE benchmark. 로봇 무관</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2611.13329'>Agent-Guided Discovery of Exchange-Correlation Functionals with Physics-based Validation</a></td><td>22</td><td>0</td><td>AI</td><td>DFT 함수 탐색 LLM agent. 로봇 무관</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2611.13914'>From Counterfactual Edits to Human Narratives: LLM-Driven Interpretations for Recommender System Explanations</a></td><td>22</td><td>0</td><td>LG</td><td>추천 counterfactual 설명 LLM 서술. 로봇 무관</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2611.13926'>Beyond Proxy Metrics: MLLMs as Human Surrogates for Explainable AI Evaluation</a></td><td>22</td><td>0</td><td>CV</td><td>MLLM을 XAI 평가 대리자로 사용. 로봇 무관</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2611.14209'>Breakdown of Autoregressive Multi-Step Reasoning Under Concentrated vs. Diffuse Attention Head Dropout</a></td><td>22</td><td>0</td><td>NLP</td><td>attention head dropout 추론 붕괴 분석. 로봇 무관</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2611.14382'>Cognitive Mapping of Learning by Thinking Mechanisms in Large Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM의 사고를 통한 학습 인지 매핑</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2611.14487'>Re-Search: Dissecting LLM Ideation Through a Two-Player Questioning Game</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM 연구 아이디어 탐색 질문 게임</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2611.13983'>Optimization-Based Path Planning for Industrial Manipulators: Experimental Validation in Additive Manufacturing</a></td><td>20</td><td>3</td><td>Planning</td><td>적층 제조용 산업 로봇 경로 최적화임. 고전 방법 응용임.</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2611.12980'>MADSNet: A Multi-Scale Axial-Attentive Dense Spiking Network for Spike Camera Image Reconstruction</a></td><td>20</td><td>1</td><td>CV</td><td>Spike camera 복원 SNN임. 로봇 연관 약함</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2611.13223'>Deletion Sensitivity Is a Property of the Model: A Three-Condition Measurement across Seven Open Reasoning Models</a></td><td>20</td><td>1</td><td>NLP</td><td>추론 모델의 삭제 민감도 측정임. 로봇 무관함.</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2611.12960'>IIT Patna at &quot;ICPR 2026 TVRID Competition on Privacy-Preserving Person Re-Identification from Top-View RGB-Depth Camera&quot;</a></td><td>20</td><td>1</td><td>CV</td><td>ICPR 대회 person Re-ID 참가 보고. incremental</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2611.14176'>SpecValley: Aggregation as Spectral Valley in Dense Heterophilic Graphs</a></td><td>20</td><td>0</td><td>LG</td><td>이종 그래프 노드 분류임. 로봇 무관</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2611.14281'>UniFlow-RS: Unified Generative Prediction for Heterogeneous Remote-Sensing Tasks</a></td><td>20</td><td>0</td><td>CV</td><td>원격탐사 통합 생성 예측임. 로봇 무관</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2611.13069'>INTENT: Out-of-Sample, Out-of-Time, and Cold-Start Evaluation on User Event Sequences</a></td><td>20</td><td>0</td><td>LG</td><td>금융 이벤트 시퀀스 평가 benchmark, 로봇과 무관임</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2611.13070'>IC-GNN: Modeling Individualized Brain Community Organization for Disease Prediction</a></td><td>20</td><td>0</td><td>LG</td><td>뇌 네트워크 GNN 질병 예측, 로봇과 무관임</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2611.13168'>RadRef: A Reference-Free Metric for Radiology Report Generation</a></td><td>20</td><td>0</td><td>NLP</td><td>방사선 리포트 평가 지표, 로봇과 무관임</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2611.13346'>Advancing Mass-Conserving Deep Learning for Distributed Hydrologic Modeling: A Case Study in a Snow-Dominated Watershed</a></td><td>20</td><td>0</td><td>LG</td><td>수문 모델링 mass-conserving DL, 로봇과 무관임</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2611.13536'>Adaptive catalyst discovery emerges from composable scientific intelligence</a></td><td>20</td><td>0</td><td>Science</td><td>촉매 발견 agent 시스템, 로봇과 무관임</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2611.13826'>JAX-WAVE: A Differentiable Physics-Supervised Framework for Inverse Wave Design in Heterogeneous Media</a></td><td>20</td><td>0</td><td>Science</td><td>파동 설계 differentiable physics, 로봇과 무관임</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2611.13893'>Conformal Risk Control for QoT-Aware Lightpath Feasibility Under Technology-Driven Domain Shift</a></td><td>20</td><td>0</td><td>Network</td><td>광망 conformal risk control, 로봇과 무관임</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2611.13938'>Dual-Core Tensor Wheel Decomposition with Structure-Cached Acceleration for Tensor Recovery</a></td><td>20</td><td>0</td><td>LG</td><td>tensor wheel decomposition, 로봇과 무관임</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2611.13952'>Geometry-Dependent Approximation and Stability Properties of Shallow ReLU$^k$ Networks on Bounded Euclidean Domains</a></td><td>20</td><td>0</td><td>LG</td><td>ReLU^k 네트워크 근사 이론, 로봇과 무관임</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2611.14035'>ScaleBrain: A Scale-Consistent Framework for EEG Foundation Models</a></td><td>20</td><td>0</td><td>Signal</td><td>EEG foundation model, 로봇과 무관임</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2611.14459'>When does text encoding matter for language modeling?</a></td><td>20</td><td>0</td><td>NLP</td><td>텍스트 인코딩이 언어 모델링에 미치는 영향임. 무관함.</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2611.14483'>Mechanistic Interpretability Needs a Logic of Inference</a></td><td>20</td><td>0</td><td>LG</td><td>mechanistic interpretability에 추론 논리 필요성을 주장함. 로봇 무관함.</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2611.12966'>BuySideFlow: A Point-in-Time Benchmark for LLM Agents in Investment Research</a></td><td>20</td><td>0</td><td>NLP</td><td>투자 리서치 LLM agent benchmark. 로봇 무관</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2611.12970'>TrustMod-SM: A Multi-Axis Benchmark for Evaluating Trustworthiness of LLMs in Social Media Content Moderation</a></td><td>20</td><td>0</td><td>NLP</td><td>콘텐츠 moderation LLM 신뢰성 benchmark. 로봇 무관</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2611.13024'>GRAP: Gender Rubric-Aware Probing for Analyzing Gender Bias in LLMs</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 성별 편향 probing. 로봇 무관</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2611.13196'>From Process Models to Composable Agentic Workflows: Combining BPMN, Agents and Enterprise Knowledge</a></td><td>20</td><td>0</td><td>NLP</td><td>BPMN 기반 agent workflow. 로봇 무관</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2611.13367'>No finite rulebook can certify every safe program: an impossibility theorem for gatekeeping AI agents</a></td><td>20</td><td>0</td><td>AI</td><td>agent 게이트키퍼 불가능성 정리. 이론적이나 로봇 무관</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2611.13454'>SafeRoute-MAS: Coverage-Aware and Risk-Calibrated Message Routing for Multi-Agent Scientific Reasoning</a></td><td>20</td><td>0</td><td>NLP</td><td>다중 agent 메시지 라우팅. 로봇 무관</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2611.13557'>Darmok: Championship Cryptic Crossword Solving via Constraint Tightening and Resilient Orchestration</a></td><td>20</td><td>0</td><td>NLP</td><td>암호 십자말풀이 시스템. 로봇 무관</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2611.13710'>AutoManifold: Agentic Design of Data Visualisation Algorithms via Manifold Embedding</a></td><td>20</td><td>0</td><td>LG</td><td>agent 기반 시각화 알고리즘 설계. 로봇 무관</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2611.13713'>Toward Autonomous RTL and Synthesis Optimization: Benchmarking and Self-Improving Agents</a></td><td>20</td><td>0</td><td>AI</td><td>RTL 최적화 agent 개요. 로봇 무관</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2611.13831'>Ceci n&#x27;est pas une pipe -- Toward a Symbolic Solver for the Abstraction and Reasoning Corpus Using Evolutionary Computation</a></td><td>20</td><td>0</td><td>AI</td><td>ARC 진화적 심볼릭 solver. 로봇 무관</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2611.14493'>Comparative Analysis of Agent Evaluation Frameworks: Stability, Detection, and Discovery in Enterprise Analytics Agents</a></td><td>20</td><td>0</td><td>NLP</td><td>엔터프라이즈 agent 평가 프레임워크 비교</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2611.13779'>Softness is something you also need! Why compliance helps control: information metrics of a passive walker with compliant ankle</a></td><td>18</td><td>3</td><td>Control</td><td>수동 보행기 compliant ankle의 정보 지표 분석임. 학습 관련성 낮음.</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2611.13920'>CAppleNet: A Coordinate Attention-Based YOLO11 for Real-Time Apple Stem Cavity and Calyx Detection</a></td><td>18</td><td>2</td><td>CV</td><td>사과 줄기 검출 YOLO 변형임. 과일 분류 응용, 작은 module 수준</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2611.13690'>Joint-State Inference for Autonomous Excavators Using Cab-View Vision-Control Fusion</a></td><td>18</td><td>2</td><td>Perception</td><td>굴착기 관절 상태를 카메라 융합으로 추정함. 응용 특화임.</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2611.14074'>Obscured Wildfire Flame Detection by Spatio-temporal Analysis of Smoke Patterns Using Frame-wise Transformers</a></td><td>18</td><td>1</td><td>CV</td><td>산불 연기 패턴 탐지임. 응용 중심</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2611.12918'>IntentTwin: Deconfounding Candidate Support and the Oracle-to-Deployment Gap in Offline Web Behavior Prediction</a></td><td>18</td><td>1</td><td>NLP</td><td>웹 행동 예측 benchmark 교란 분석임. 로봇 무관함.</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2611.12934'>EarthRecord: From Pixels to Land Change with Multimodal Agents over Four Decades of Satellite Imagery</a></td><td>18</td><td>1</td><td>Multimodal</td><td>위성 영상 land change multimodal agent benchmark임. 무관에 가까움.</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2611.13046'>SpatialSR: Spatial Resolution-Centric Pipeline for Arbitrary-Scale Remote Sensing Super-Resolution</a></td><td>18</td><td>0</td><td>CV</td><td>원격탐사 임의 배율 super-resolution임. 로봇 무관</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2611.13504'>Dark Matters: VAE-Aware HDR Encoding for SDR-to-HDR Video Reconstruction</a></td><td>18</td><td>0</td><td>Video</td><td>SDR-HDR 영상 복원임. 로봇 무관</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2611.13621'>PUMA: Probability-Constrained Sequential Interaction for Forensic Localization</a></td><td>18</td><td>0</td><td>CV</td><td>이미지 조작 위치화 forensic임. 로봇 무관</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2611.13849'>Satellite Pretraining Is Not One Thing: A Matched-Pair Study of Generic and Earth-Observation Foundation Models for Scene Classification</a></td><td>18</td><td>0</td><td>CV</td><td>위성 pretraining 비교 연구임. 로봇 무관</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2611.14124'>CroCoMAE: Cross-modal self-supervised collaborative representation learning for SAR-optical remote sensing data</a></td><td>18</td><td>0</td><td>CV</td><td>SAR-광학 자기지도 학습임. 로봇 무관</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2611.14254'>Location Matters: Sparse Latent-Variance Attacks for Face Privacy against Diffusion Personalization</a></td><td>18</td><td>0</td><td>Generative</td><td>Diffusion 개인화 방어 공격임. 로봇 무관</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2611.14519'>Medical Image Segmentation: Foundation Model Adaptation versus Task-Specific Training</a></td><td>18</td><td>0</td><td>Medical</td><td>의료 분할 foundation model 비교임. 로봇 무관</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2611.13243'>GigaEdge Spench: An SDK for Practical Streaming Speech Enhancement</a></td><td>18</td><td>0</td><td>Audio</td><td>음성 향상 SDK, 로봇과 무관임</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2611.13298'>Neural Network-Assisted CLEAN for Efficient Multipath Parameter Estimation in MIMO Systems</a></td><td>18</td><td>0</td><td>Signal</td><td>MIMO 다중경로 추정, 로봇과 무관임</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2611.13359'>Reconstructing Boundary Layer Wind Profiles with Machine Learning: A Comparative Study on IGRA Radiosonde Data</a></td><td>18</td><td>0</td><td>LG</td><td>풍속 프로파일 복원 비교 연구, 로봇과 무관임</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2611.13566'>Metamorphic testing of learned AC optimal power flow surrogates reveals representation dependence</a></td><td>18</td><td>0</td><td>LG</td><td>전력망 surrogate metamorphic testing, 로봇과 무관임</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2611.13945'>Chem World: A Large-Scale Benchmark and Physics-Aware Framework for Trustworthy Molecular Property Prediction</a></td><td>18</td><td>0</td><td>Chem</td><td>분자 속성 예측 benchmark, 로봇과 무관임</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2611.13991'>Universal Approximation Theorem for Metaplectic Neural Operators</a></td><td>18</td><td>0</td><td>LG</td><td>neural operator 범용 근사 증명, 로봇과 무관임</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2611.14136'>HaiRuo: Forecasting Ocean Eddies as Fields and Objects with a Satellite-Altimetry Foundation Model</a></td><td>18</td><td>0</td><td>Science</td><td>해양 eddy 예측 foundation model, 로봇과 무관임</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2611.14211'>Verifiable Agentic Traffic Class: A Policed Quality-of-Service Mechanism for Agentic AI Traffic, Evaluated from Simulation to Real-Kernel Adversarial Testing</a></td><td>18</td><td>0</td><td>Network</td><td>agentic traffic QoS, 로봇과 무관임</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2611.14508'>When Does the Real Wiring Win? Testing connectome structure-function claims against unmeasured physiology</a></td><td>18</td><td>0</td><td>Neuro</td><td>connectome 구조-기능 검증, 로봇과 무관임</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2611.13744'>Do Language Models Feel the Sentiment? Investigating Emotion Vectors</a></td><td>18</td><td>0</td><td>NLP</td><td>감정 벡터와 감성 분류 분석임. 무관함.</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2611.14221'>Stagewise and interpretable emergence of inside-outside computation in Transformer-based language models</a></td><td>18</td><td>0</td><td>NLP</td><td>Transformer의 inside-outside 계산 출현 분석임. 무관함.</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2611.14252'>Semantic Chains: From Reachable Facts to Justified Answers</a></td><td>18</td><td>0</td><td>NLP</td><td>논리 사실 그래프 기반 근거 사슬임. 무관함.</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2611.12942'>Tabular Foundation Models vs Tuned Gradient Boosting for Telecom Churn: A Profit- and Calibration-Aware Evaluation</a></td><td>18</td><td>0</td><td>LG</td><td>통신사 이탈 예측 tabular 모델 비교. 로봇 무관</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2611.13042'>Trust, but verify, audit and attribute: a human-in-the-loop framework for checking AI-produced research results</a></td><td>18</td><td>0</td><td>AI</td><td>AI 생성 연구 결과 검증 프레임워크 입장문</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2611.13312'>Towards Scalable Network-Based Interventions for HIV Treatment and Prevention via R2C-Agent</a></td><td>18</td><td>0</td><td>AI</td><td>HIV 네트워크 개입 agent. 로봇 무관</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2611.13333'>Do AI Agents need Preventive Care? An Epidemiologic Cohort Design for Agentic AI</a></td><td>18</td><td>0</td><td>AI</td><td>agentic AI 코호트 설계 제안. 로봇 무관</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2611.13352'>Multi-Stage Phase-Aware Self-Supervised Reconstruction for Multi-Echo Gradient-Echo MRI</a></td><td>18</td><td>0</td><td>CV</td><td>MRI 자기지도 재구성. 로봇 무관</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2611.13388'>Online-Adaptive Fuzzy Cognitive Maps for Neuro-symbolic Financial Forecasting</a></td><td>18</td><td>0</td><td>LG</td><td>금융 예측 fuzzy cognitive map. 로봇 무관</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2611.13487'>The WoW: A Large-Scale World Knowledge Corpus for Full-Lifecycle LLM Training</a></td><td>18</td><td>0</td><td>NLP</td><td>중국어 교육 코퍼스. 데이터셋 위주</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2611.13612'>Earth Embeddings in Environmental Remote Sensing</a></td><td>18</td><td>0</td><td>CV</td><td>지구 임베딩 원격탐사 서베이</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2611.13613'>Megrez: A Knowledge-Guided Agent for Formal Mathematics over MK Set Theory</a></td><td>18</td><td>0</td><td>NLP</td><td>형식 수학 agent. 로봇 무관</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2611.13704'>SeqFold: Timestamp-Addressable Compressed States for User Action Sequence Backbones</a></td><td>18</td><td>0</td><td>LG</td><td>사용자 행동 시퀀스 압축 상태. 로봇 무관</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2611.14285'>LM-SimBench: A Unified Framework, Dataset, and Benchmark for Large Language Model Training Simulation</a></td><td>18</td><td>0</td><td>LG</td><td>LLM 학습 시뮬레이션 benchmark. 로봇 무관</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2611.14413'>Bits or permutations? Spending a fixed inference budget on weight precision or on option-order averaging in small local language models</a></td><td>18</td><td>0</td><td>LG</td><td>소형 LM 비트 대 순서 평균 비교. 로봇 무관</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2611.13638'>picoEmergencyNet : Attention-Enhanced Ultra-Small Deep Learning Model for Aerial Image Classification in Emergency Monitoring</a></td><td>16</td><td>1</td><td>CV</td><td>초소형 항공 이미지 분류 모델임. 도메인 특화</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2611.13851'>Towards Text-Only Remote Sensing Scene Classification via Semantic Proxy</a></td><td>16</td><td>0</td><td>CV</td><td>텍스트만으로 원격탐사 분류임. 로봇 무관</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2611.14279'>AutoThreshold: Joint Confusion-Profile Learning for Adaptive Mask Binarization</a></td><td>16</td><td>0</td><td>CV</td><td>마스크 이진화 임계값 학습임. 작은 module 수준</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2611.14516'>TorchCurves: Differentiable Parametric Curves</a></td><td>15</td><td>2</td><td>LG</td><td>미분 가능한 곡선 라이브러리 소프트웨어 논문임. 방법론 novelty 거의 없음.</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2611.13379'>Fastener-centric acquisition and AND/OR graph representation of state-dependent disassembly knowledge from CAD-derived virtual assemblies</a></td><td>15</td><td>2</td><td>Robotics</td><td>CAD 기반 분해 지식을 AND/OR 그래프로 표현함. 로봇 학습과 거리 있음.</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2611.12977'>Selective Surgical Action-Center Localization:Retaining Localization Gains through Supervised Scoring</a></td><td>15</td><td>1</td><td>CV</td><td>수술 행동 중심점 localization 선택 파이프라인임. 도메인 특화</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2611.13009'>Instance-preserving graded semantic reporting for surgical action triplets</a></td><td>15</td><td>1</td><td>CV</td><td>수술 triplet 보고 방식 개선임. 도메인 특화</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2611.13509'>Mobile AI Factory: Building Specialized Language Models for Your Mobile Device</a></td><td>15</td><td>1</td><td>NLP</td><td>모바일용 소형 언어모델 구축 파이프라인임. 무관함.</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2611.12936'>LandslideFM: A Foundation Model Towards Unified Landslide Perception and Understanding</a></td><td>15</td><td>1</td><td>CV</td><td>산사태 foundation model임. 도메인 특화임.</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2611.12981'>Evidence-Grounded Iterative Reasoning for the Diagnosis of Diffuse Cystic Lung Diseases</a></td><td>15</td><td>0</td><td>Medical</td><td>폐질환 진단용 MLLM 추론 파이프라인임. 로봇 무관</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2611.13550'>Tabular Foundation Models in Financial Predictions</a></td><td>15</td><td>0</td><td>LG</td><td>회계 예측용 tabular foundation model, 로봇과 무관임</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2611.13661'>SepsisFlow: an event-stream foundation model for continuous risk warning and trajectory modelling in ICU sepsis</a></td><td>15</td><td>0</td><td>LG</td><td>ICU 패혈증 foundation model, 로봇과 무관임</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2611.13941'>PARDIG: Global Precipitation Estimates Learned from Sparse Satellite Observations</a></td><td>15</td><td>0</td><td>LG</td><td>강수 추정, 로봇과 무관임</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2611.14141'>Deviation-Aware Pretraining for Cardiovascular Disease Detection from Electrocardiograms</a></td><td>15</td><td>0</td><td>LG</td><td>심전도 사전학습, 로봇과 무관임</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2611.14272'>Federated Learning for Cross-Regional Epidemic Forecasting with Asynchronous Outbreaks</a></td><td>15</td><td>0</td><td>LG</td><td>역학 forecasting federated, 로봇과 무관임</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2611.14401'>Discovering Equations for the Thermodynamics of South Asian Monsoon Precipitation</a></td><td>15</td><td>0</td><td>Science</td><td>몬순 강수 식 발견, 로봇과 무관임</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2611.14462'>Accurate predictions of properties of energetic materials with tabular foundation models</a></td><td>15</td><td>0</td><td>Chem</td><td>에너지 물질 TabPFN 예측, 로봇과 무관임</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2611.14504'>Emergent Biological Capabilities in a Foundation Model for Molecular Interactions</a></td><td>15</td><td>0</td><td>Bio</td><td>분자 상호작용 foundation model, 로봇과 무관임</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2611.14511'>Pyrite: Building and Benchmarking Protein-Ligand Pose Ranking Agents</a></td><td>15</td><td>0</td><td>Chem</td><td>protein-ligand pose ranking agent, 로봇과 무관임</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2611.13564'>A Concept-Based Interpretable Framework for Clinical Text-based Prediction via Token-Concept Attention without Concept Supervision</a></td><td>15</td><td>0</td><td>NLP</td><td>임상 텍스트 개념 기반 해석 프레임워크임. 무관함.</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2611.14116'>Visual Similarity in Adult Word Extension and Artificial Word Learning</a></td><td>15</td><td>0</td><td>Cognitive</td><td>시각 유사도와 단어 확장 인지 연구임. 무관함.</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2611.12941'>AI Governance Should Prioritize Control and Knowledge Boundaries Over Limiting Intelligence</a></td><td>15</td><td>0</td><td>LG</td><td>AI 거버넌스 입장문. 기술 기여 없음</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2611.13022'>Understanding-First AI Engineering: Purposes, Reference Architecture, and Architectural Patterns for Human Understanding</a></td><td>15</td><td>0</td><td>AI</td><td>이해 중심 AI 엔지니어링 개념 제안. 실증 없음</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2611.13215'>Counting Under Disagreement: Dollar-Weighted Measurement, Selective Machine Labelling and Budgeted Human Review from Disagreeing AI Readers of Administrative Text</a></td><td>15</td><td>0</td><td>LG</td><td>행정 텍스트 측정 통계 연구. 로봇 무관</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2611.13217'>Reliability of Claude Code as an Agentic AI Grading System for Handwritten University Exams</a></td><td>15</td><td>0</td><td>NLP</td><td>Claude Code 시험 채점 신뢰성 연구. 로봇 무관</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2611.13361'>A Technique to Model Product Information and User Reviews (MPIUR)</a></td><td>15</td><td>0</td><td>LG</td><td>멀티모달 추천 모델. 로봇 무관</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2611.13456'>When Reasoning looks like Hidden Understanding: How Chain-of-Thought Fosters Anthropomorphism, Perceptions of Epistemic Superiority, and Cognitive Deference</a></td><td>15</td><td>0</td><td>NLP</td><td>CoT의 의인화 인식 사용자 연구. 로봇 무관</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2611.13651'>DrugCoding: A Scientific Programming Agent for Drug Discovery</a></td><td>15</td><td>0</td><td>NLP</td><td>신약 탐색 프로그래밍 agent. 로봇 무관</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2611.13667'>Benchmarking LLM Next-Step Recommendations with Knowledge Space Theory</a></td><td>15</td><td>0</td><td>NLP</td><td>교육용 LLM 다음 단계 추천 benchmark</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2611.13705'>Agentic AI Meets Formal Verification in the Era of Agentic Hardware Development</a></td><td>15</td><td>0</td><td>AI</td><td>하드웨어 형식 검증 개요 초청 논문</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2611.13892'>A 10K drone image dataset with component-level annotations for rooftop photovoltaic inspection</a></td><td>14</td><td>1</td><td>CV</td><td>태양광 점검 드론 dataset임. 도메인 특화</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2611.13010'>Preserving Cultural Records: A Large-Scale Benchmark and Visual-Prior Routing Network for Ancient Book Image Restoration</a></td><td>14</td><td>0</td><td>CV</td><td>고서 이미지 복원 benchmark와 네트워크임. 로봇 무관</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2611.13045'>MICRO: A Surgery-Phase Retinal Image Rigid Registration Benchmark and One-Step Frequency-Structure Similarity Registration Learning</a></td><td>14</td><td>0</td><td>Medical</td><td>망막 영상 등록 benchmark임. 로봇 무관</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2611.13178'>Multimodal Judges Flag, Humans Decide: A Review-and-Edit Framework for AI-Generated Product Video Ads</a></td><td>14</td><td>0</td><td>Multimodal</td><td>광고 영상 검수 프레임워크임. 로봇 무관</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2611.13711'>Hint, Not Hole: Localization-Robust Video Overlay Removal</a></td><td>14</td><td>0</td><td>Video</td><td>영상 overlay 제거임. 로봇 무관</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2611.13776'>DisasterAgent: An Evidence-Driven Agent for Verifiable Disaster Report Generation From Remote Sensing Imagery</a></td><td>14</td><td>0</td><td>Multimodal</td><td>재난 보고서 생성 agent임. 로봇 무관</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2611.13935'>MEOW: Medical Open-World Interactive Segmentation</a></td><td>14</td><td>0</td><td>Medical</td><td>의료 open-world interactive 분할임. 로봇 무관</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2611.14018'>Interleaving anatomical inspection and diagnostic reasoning for explainable radiology report generation</a></td><td>14</td><td>0</td><td>Medical</td><td>영상의학 보고서 생성임. 로봇 무관</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2611.14380'>What Factors Matter for Collection-Level Counting with Human-AI Collaboration?</a></td><td>14</td><td>0</td><td>CV</td><td>컬렉션 단위 객체 계수 인간-AI 협업 요인 분석임. 로봇 무관</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2611.14451'>A Lightweight Differentiable Method for Real-Time Skin Rendering and Digitization</a></td><td>14</td><td>0</td><td>CV</td><td>피부 렌더링 미분 가능 방법임. 로봇 무관</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2611.13307'>Does Haptic Connection to a Healthy Partner Improve Motor Learning in Chronic Stroke? A Pilot Study of Robot-Based Dyadic Training</a></td><td>12</td><td>2</td><td>HRI</td><td>뇌졸중 환자 haptic dyad 재활 파일럿 연구임. 우리 연구 주제와 무관함.</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2611.13245'>Rethinking Evaluation for Video Capsule Endoscopy: Validation Protocol, Source-Video Diversity, and Cross-Dataset Shift</a></td><td>12</td><td>0</td><td>Medical</td><td>캡슐 내시경 검증 프로토콜임. 로봇 무관</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2611.13330'>Uni-Loc: Weakly Supervised 3D CT Pathology Localization via Spatially Grounded Vision-Language Classification</a></td><td>12</td><td>0</td><td>Medical</td><td>3D CT 병변 weakly supervised 위치화임. 로봇 무관</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2611.13425'>Prompt2Echo (P2Echo): Text-Prompted Multi-View Echocardiography Segmentation with One Model</a></td><td>12</td><td>0</td><td>Medical</td><td>심초음파 prompt 분할임. 로봇 무관</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2611.13513'>Evidential Deep Learning with conditional entropy for glaucoma detection</a></td><td>12</td><td>0</td><td>Medical</td><td>녹내장 evidential learning임. 로봇 무관</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2611.13514'>Seeing the Small: Deformable Duality Mamba for Retinal Lesion Segmentation</a></td><td>12</td><td>0</td><td>Medical</td><td>망막 병변 분할 Mamba임. 로봇 무관</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2611.14207'>DailyWildfireCAN: A Dataset and Benchmark for Next-Day Wildfire Spread Prediction in Canada</a></td><td>12</td><td>0</td><td>LG</td><td>산불 확산 예측 dataset임. 로봇 무관</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2611.14518'>Toward Foundation Detection Models via Example-Based Grounding in EM-DETR</a></td><td>12</td><td>0</td><td>Medical</td><td>EM-DETR 의료 검출임. 로봇 무관</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2611.12904'>Actionable Feedback: Improving Model Capabilities from User Edit Data on Clinical Documentation</a></td><td>12</td><td>0</td><td>NLP</td><td>임상 문서 사용자 편집 데이터 활용임. 무관함.</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2611.13059'>A Multi-Word Tokenizer for 204 Languages That Needs Fewer Tokens Than GPT-4o&#x27;s, Including on English</a></td><td>12</td><td>0</td><td>NLP</td><td>204개 언어 multi-word tokenizer임. 무관함.</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2611.13562'>An evidence-traceable benchmark of clinical reasoning in large language models</a></td><td>12</td><td>0</td><td>NLP</td><td>임상 추론 benchmark임. 무관함.</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2611.14010'>One Sequence Is Enough: Fingerprinting Language Models from Fixed-Length Integer Sequences</a></td><td>12</td><td>0</td><td>NLP</td><td>모델 지문 식별임. 무관함.</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2611.13062'>Elicitation of the parameters of a multi-criteria sorting model</a></td><td>12</td><td>0</td><td>AI</td><td>다기준 정렬 모델 파라미터 도출. 로봇 무관</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2611.13167'>AI Alignment Is Neither Solvable nor Sufficient</a></td><td>12</td><td>0</td><td>AI</td><td>AI alignment 입장문. 기술 기여 없음</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2611.13402'>Living constitutions: Participatory alignment for sovereign foundation models</a></td><td>12</td><td>0</td><td>AI</td><td>참여형 alignment 입장문</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2611.13512'>Nepali-English Code-Mixed Speech Recognition: Data Preparation and Adaptation of a Speech Foundation Model</a></td><td>12</td><td>0</td><td>NLP</td><td>네팔어 코드혼합 ASR 적응. dataset fine-tuning</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2611.14174'>Cross-Border Fulfillment Center Selection via Doubly Robust Estimation and Linear Programming</a></td><td>12</td><td>0</td><td>LG</td><td>물류 센터 선택 최적화. 로봇 무관</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2611.13739'>Effects of Laser Beam Width and Measurement Noise on Tree Diameter Estimation in Laser Scanning</a></td><td>10</td><td>1</td><td>3D Vision</td><td>레이저 스캔 나무 직경 오차 분석임. 로봇 무관</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2611.12969'>Evaluation protocols for historical script classification: the cost of manuscript-level leakage and the role of soft labels</a></td><td>10</td><td>0</td><td>CV</td><td>필사본 문자 분류 평가 프로토콜임. 로봇 무관</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2611.13191'>Comparative Evaluation of Deep Learning Models for Geographic Atrophy Segmentation in En Face OCT Images</a></td><td>10</td><td>0</td><td>Medical</td><td>GA 분할 모델 비교 연구임. 로봇 무관</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2611.13297'>Domain adaptation of a video Foundation model for Heart Failure Diagnosis from Echocardiography</a></td><td>10</td><td>0</td><td>Medical</td><td>심초음파 video foundation model 도메인 적응임. 로봇 무관</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2611.13911'>Adapting a Vision Foundation Model for Fracture Characterization in Acoustic Image Logs</a></td><td>10</td><td>0</td><td>Medical</td><td>음향 영상 균열 foundation model 적응임. 로봇 무관</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2611.14476'>BoviShift: A Six-Year Multi-Attribute Audit of Visual Cattle Phenotyping Across Animals and Time</a></td><td>10</td><td>0</td><td>CV</td><td>소 표현형 장기 감사임. 로봇 무관</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2611.12927'>An ensemble of graph generative models for assisted history matching of the Brugge field case</a></td><td>10</td><td>0</td><td>LG</td><td>저류층 history matching 그래프 생성 모델임. 로봇 무관</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2611.13339'>Measuring Definition Sensitivity in LLM Annotation of Social Science Concepts</a></td><td>10</td><td>0</td><td>NLP</td><td>LLM 주석의 정의 민감도 측정임. 무관함.</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2611.13441'>Inherited Weights: Measuring the Tokenization Premium and the Sovereignty Cost of Language Models for the Global South</a></td><td>10</td><td>0</td><td>NLP</td><td>파생 모델 tokenization 비용 측정임. 무관함.</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2611.13788'>LLM Validation Makes Minimal-Pair Benchmarks Easier for Language Models</a></td><td>10</td><td>0</td><td>NLP</td><td>minimal-pair benchmark LLM 검증 분석임. 무관함.</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2611.13811'>Antalia-2 Mini: A 7.6-million-parameter Turkish text-to-speech model trained entirely on synthetic speech</a></td><td>10</td><td>0</td><td>Speech</td><td>터키어 TTS 소형 모델임. 무관함.</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2611.13845'>Alania-2: Turkish text-to-speech with instant and fine-tuned voice cloning</a></td><td>10</td><td>0</td><td>Speech</td><td>터키어 TTS 음성 복제 시스템임. 무관함.</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2611.13894'>Beyond Fluent Responses: Finding User Dissatisfaction in Human-AI Interactions</a></td><td>10</td><td>0</td><td>NLP</td><td>사용자 불만족 탐지임. 무관함.</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2611.13990'>On the information rate of phones, syllables and words</a></td><td>10</td><td>0</td><td>Speech</td><td>음소·음절·단어 정보율 분석임. 무관함.</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2611.14236'>StaRSE: Compact Russian Sentence Embeddings with a Sign-Coded Static Encoder</a></td><td>10</td><td>0</td><td>NLP</td><td>러시아어 정적 sentence encoder임. 무관함.</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2611.13634'>An IoT Based Approach for Platform Independent Positioning Service</a></td><td>8</td><td>1</td><td>IoT</td><td>실내 측위 IoT 아키텍처 확장임. 무관함.</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2611.13200'>Image Quality and the Reliability of Fabric-Density Measurement: Counting Threads from Smartphone Photos Through a Pick Glass</a></td><td>8</td><td>0</td><td>CV</td><td>직물 밀도 측정 연구임. 로봇 무관</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2611.13308'>Domain-Adversarial Adaptation from MURA to In-House Radiographs for Improved Adult Elbow Fracture Classification</a></td><td>8</td><td>0</td><td>Medical</td><td>팔꿈치 골절 domain adaptation임. 로봇 무관</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2611.13581'>Lightweight Deep Learning Framework for Astrocyte-Centric 3D Reconstruction across Normal and Stress-associated Ultrastructural States</a></td><td>8</td><td>0</td><td>Medical</td><td>성상세포 3D 재구성임. 로봇 무관</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2611.13649'>Predicting Single-Cell Spatial Gene Expression from H&amp;E using Pathology Foundation Models</a></td><td>8</td><td>0</td><td>Medical</td><td>H&amp;E 유전자 발현 예측임. 로봇 무관</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2611.13883'>The BRIDGE dataset: paired brightfield whole-slide images of prostate core-needle biopsies in paraffin, after deparaffinization and H&amp;E staining</a></td><td>8</td><td>0</td><td>Medical</td><td>병리 슬라이드 데이터셋임. 로봇 무관</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2611.13884'>Region-Wise Logit Fusion and Utility-Gated Refinement for Brain Metastasis Segmentation</a></td><td>8</td><td>0</td><td>Medical</td><td>뇌 전이 분할 챌린지임. 로봇 무관</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2611.13912'>MicroBT: Centroid-Guided Synergistic Learning for Multi-Modal Micro Brain Tumor Segmentation and Counting</a></td><td>8</td><td>0</td><td>Medical</td><td>뇌종양 분할과 계수임. 로봇 무관</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2611.14013'>A Stage-Wise Explainable Pipeline for Arteriolar-to-Venular Ratio Estimation and Retinopathy Screening</a></td><td>8</td><td>0</td><td>Medical</td><td>망막 AVR 추정 파이프라인임. 로봇 무관</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2611.14058'>CURRENT: A Recurrent Neural Network for Concurrent Spatial and Temporal Super-Resolution of 4D Flow MRI</a></td><td>8</td><td>0</td><td>Medical</td><td>4D flow MRI 초해상도임. 로봇 무관</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2611.14129'>Continuous 3D Spatial Transcriptomics Reconstruction via Histology-Informed Implicit Neural Representations</a></td><td>8</td><td>0</td><td>Medical</td><td>3D 공간 전사체 재구성임. 로봇 무관</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2611.12900'>From Relevant Posts to Attributable Spans: Explicit Symptom Evidence for Depression Questionnaire Inference</a></td><td>8</td><td>0</td><td>NLP</td><td>우울 설문 추론용 증거 span 연구임. 무관함.</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2611.12906'>Brasilidade: Measuring Brazilian Identity for Large Language Models</a></td><td>8</td><td>0</td><td>NLP</td><td>브라질 정체성 LLM benchmark임. 무관함.</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2611.13058'>The Indic Token Tax in 2026: Measuring Tokenizer. Disparity and Its Cost for the Languages of India</a></td><td>8</td><td>0</td><td>NLP</td><td>인도어 tokenizer 비용 측정임. 무관함.</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2611.13207'>HiCAP: Hierarchical Cultural Adaptation via Personality for Dialogue Generation</a></td><td>8</td><td>0</td><td>NLP</td><td>문화 적응 대화 생성임. 무관함.</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2611.13531'>Framing-Induced Vulnerability in Large Language Models: Evidence from Chinese News Headlines</a></td><td>8</td><td>0</td><td>NLP</td><td>뉴스 헤드라인 프레이밍 취약성 분석임. 무관함.</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2611.13595'>IFRS Compliance Verification: An Open Multi-LLM Benchmark and Content-Conditioned Ensemble Classifier</a></td><td>8</td><td>0</td><td>NLP</td><td>IFRS 준수 검증 benchmark임. 무관함.</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2611.13609'>Post-OCR Correction of Mixed-Script Uzbek Text: Byte-Level ByT5 with an Empirical Homoglyph Noise Matrix</a></td><td>8</td><td>0</td><td>NLP</td><td>우즈베크어 OCR 후처리임. 무관함.</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2611.13843'>PolyRoute: A Twelve-Language and Code-Mixed Benchmark for Typed-Decision Routing, with Baselines and a Leaderboard</a></td><td>8</td><td>0</td><td>NLP</td><td>다국어 typed-decision routing benchmark임. 무관함.</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2611.14059'>HandsOnAid: Building and Evaluating an Offline First-Aid Assistant for Emergency Response Scenarios</a></td><td>8</td><td>0</td><td>NLP</td><td>오프라인 응급처치 어시스턴트임. 무관함.</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2611.14241'>Dyship: Leveraging Acoustic Features For Speaker Relationship Classification From Dyadic Conversations</a></td><td>8</td><td>0</td><td>Speech</td><td>화자 관계 분류임. 무관함.</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2611.14325'>Point-in-Time Encoders for Earnings Calls</a></td><td>8</td><td>0</td><td>NLP</td><td>실적 발표 point-in-time encoder임. 무관함.</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2611.14480'>Pterodactyl: Pushing the Limits of Efficient Automated Translation Evaluation</a></td><td>8</td><td>0</td><td>NLP</td><td>WMT26 번역 평가 제출임. 무관함.</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2611.13933'>The Case for AI-Enabled Gate Monitoring as Farm Security in the UK: A PRISMA-Guided Review of the Evidence on Rural Crime, Livestock Predation and Farm Access</a></td><td>6</td><td>0</td><td>Other</td><td>농장 보안 리뷰임. 로봇 무관</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2611.13012'>khammoon: From a Linguistic Guideline to a Thai Morpheme Segmenter</a></td><td>6</td><td>0</td><td>NLP</td><td>태국어 형태소 분절기임. 무관함.</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2611.13752'>Word-Level Alignment of OCR and Ground Truth under Zoning and Reading-Order Errors</a></td><td>6</td><td>0</td><td>NLP</td><td>OCR 단어 정렬임. 무관함.</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2611.13358'>Understanding Students&#x27; Rationales for AI-Mediated Cheating: An Instructor Perspective from Online Forums Analysis</a></td><td>5</td><td>0</td><td>NLP</td><td>AI 부정행위 인식 포럼 분석임. 무관함.</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2611.13366'>Mapping Instructors&#x27; Attitudes Towards Cheating with AI: An Exploratory Analysis Using Forum Analysis</a></td><td>5</td><td>0</td><td>NLP</td><td>AI 부정행위 교수 태도 분석임. 무관함.</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2611.13597'>Compute the Interactions, Not the Attributes: What a Fact Layer Must Supply in the Chinese Sexagenary System</a></td><td>5</td><td>0</td><td>NLP</td><td>사주 체계 fact layer 측정임. 무관함.</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2611.13686'>You Are What You Read: Indian Political News Media Bias Dataset for Hindi Language</a></td><td>5</td><td>0</td><td>NLP</td><td>힌디어 뉴스 편향 데이터셋임. 무관함.</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2611.14079'>From Bias to Positionality: A critical grammar for Large Language Models</a></td><td>5</td><td>0</td><td>NLP</td><td>LLM bias 비평 논문임. 무관함.</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2611.13636'>An Interpretable Stylometric Framework for Early Chinese Buddhist Translator Styles: A Case Study on the Attribution of Disputed Works of An Shigao</a></td><td>4</td><td>0</td><td>NLP</td><td>불교 번역가 문체 분석임. 무관함.</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2611.14036'>MISO-BR: An Open Corpus for Misogyny Detection in Brazilian Portuguese</a></td><td>4</td><td>0</td><td>NLP</td><td>브라질어 여성혐오 코퍼스임. 무관함.</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2611.14244'>An AI Assistant for Automating Anti-Corruption Expertise of Draft Legislation Based on the TRACE Framework</a></td><td>4</td><td>0</td><td>NLP</td><td>반부패 법안 검토 AI 어시스턴트임. 무관함.</td></tr>
</tbody></table>

</details>
