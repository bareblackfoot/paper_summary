# 오늘의 arXiv Top 15: 2026-11-13 (금)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**

**신규 논문 수: 전체 646편 → 중복 제거 후 646편 (이번 평가 대상 646편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 170 |
| cs.LG | 186 |
| cs.RO | 91 |
| cs.CL | 86 |
| cs.AI | 113 |

---

## Top 15

### 1. ActionCodec2: A Streaming Action Tokenizer (84점)

[arXiv](https://arxiv.org/abs/2611.15490) · [PDF](https://arxiv.org/pdf/2611.15490) · [alphaXiv](https://www.alphaxiv.org/abs/2611.15490) (요약 있음) · [프로젝트 페이지](https://zibindong.github.io/actioncodec2-page/)

- **저자**: Zibin Dong, Yicheng Liu, Shiduo Zhang, Tianyuan Yuan, Baijun Ye, Jinqiu Wang, Hang Zhao
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 70점
- **읽은 원문**: PDF 전문

> autoregressive VLA의 action tokenizer를 chunk 단위가 아니라 제어 step마다 action을 내보내는 streaming 방식으로 바꾸고, 복원 궤적 오차를 정해진 허용치 안에 묶음. 같은 VLA에 tokenizer만 바꿔 처음 보는 장면의 실제 Franka 과제 4종을 돌리면 task progress가 FAST 50.8%에서 73.9%로 오름.

**무슨 문제인가**

기존 action tokenizer(FAST, VQ-VAE 계열)는 1~2초 분량의 action을 chunk 하나로 압축하므로, chunk 전체를 decoding해야 실행할 수 있음. 그래서 로봇은 chunk 경계에서만 새 관측에 반응하고, token 하나가 틀리면 chunk 안의 여러 action이 함께 틀어짐. 차원마다 token 하나를 쓰는 binning은 step 단위로 내보낼 수 있지만 7차원 15 Hz에서 초당 105 token이 필요해 decoding이 느림. 또 step마다 따로 양자화하면 작은 오차가 시간에 따라 쌓임. LIBERO(시뮬레이션 조작 benchmark) demonstration 재생 실험에서 FAST는 step당 복원 오차가 1 mm 이내인데도 episode당 약 40 mm가 어긋남.

**어떻게 푸나**

ActionCodec2는 gradient 학습 없이 만드는 tokenizer이며, 입력은 연속 action 궤적이고 출력은 VLA가 예측할 token열임. decoder는 매 step 고정된 상대 이동(motion primitive)을 지금까지 복원한 상태에 더함. encoder는 decoder와 같은 복원 상태를 유지하고, 남은 오차와 다음 이동을 합친 값에 가장 가까운 primitive를 고름. 그래서 각 step이 앞 step의 양자화 오차를 보정하고, 복원 궤적이 허용 오차(위치 5 mm 등) 안에 머무름. 저자는 필요한 최소 primitive 수를 covering 문제로 정식화함: 한 step 이동 범위를 허용 오차 영역들로 빈틈없이 덮는 문제임. translation은 정확한 최솟값을, rotation은 상수배 안의 상하한을 증명함. 다음으로 Set-BPE(좌표 순서에 매이지 않는 BPE)가 좌표 간, 인접 step 간에 함께 나타나는 primitive 기호를 손실 없이 하나의 token으로 합침. primitive 격자는 이동 범위와 허용 오차로 규칙에 따라 정하고, Set-BPE의 병합 규칙만 데이터에서 기호가 함께 나타나는 횟수를 세어 정함. token 순서 규칙만으로 step 경계를 복원할 수 있어서 step 하나가 완성되는 즉시 action을 실행함.

**결과**

- 같은 backbone G0.5(사전학습된 autoregressive VLA)에 tokenizer만 바꿔 비교함. 범용 tokenizer는 24개 embodiment 약 2만 시간 데이터로 맞추며, step별 이동을 부호화하는 1차 버전 ACodec2+와 속도 변화를 부호화하는 2차 버전 ACodec2+II가 있음. ACodec2+II가 LIBERO(4개 suite) 평균 98.2%를 기록함. SimplerEnv(WidowX 시뮬레이션 과제 4개)는 93.8%, LIBERO-Plus(7종 교란을 건 LIBERO)는 79.5%로 세 benchmark 모두 비교 대상 중 가장 높음.
- 20 Hz 실시간 제어 시계로 LIBERO를 돌리면, 같은 ACodec2+ checkpoint의 평균 성공률이 chunk 단위 실행 73.1%에서 streaming 실행 91.0%로 오름. chunk tokenizer 중 가장 높은 OATaligned(기존 OAT tokenizer를 ActionCodec2의 token 속도에 맞춘 것)는 87.2%임.
- DROID(실제 Franka 조작 데이터셋)로 학습하고 처음 보는 장면의 실제 Franka 과제 4종에서 policy당 50회 평가함. ACodec2+의 task progress(완료한 milestone 비율)는 73.9%이고 비교한 기존 chunk tokenizer인 FAST는 50.8%, X-Tokenizer는 52.8%임. 관측에서 action이 나오기까지 지연은 ACodec2+ 약 50 ms, FAST 607 ms임.
- chunk 생성 중간에 로봇 상태를 넣어 주는 closed-loop 설정을 PPO로 학습함. 물리 파라미터를 무작위로 바꾼 LIBERO 과제 6개에서 성공률이 open-loop 64.7%에서 79.0%로 오름. 물체가 움직이는 설정의 grasp 성공률은 27.6%에서 46.2%로 오름.

**한계**

오차 보장은 tokenizer 복원 궤적에 대한 것이며 실제 로봇이 명령을 그 오차 안에서 따른다는 뜻은 아님. 범용 tokenizer는 end-effector 속도 약 1.2 m/s까지만 덮고, 빠른 동작에서는 압축률이 chunk tokenizer보다 낮을 수 있다고 저자가 밝힘. chunk 중간에 로봇 상태를 넣는 closed-loop 실험은 시뮬레이션뿐임. VLM agent가 성공한 token열을 macro로 저장해 다시 쓰는 실험은 조건당 episode 하나 수준임.

**누리랩 연구와의 연결**

- autoregressive VLA에서 chunk 중간에 관측을 반영할 수 있게 하므로, 실행 중 failure detection 후 즉시 recovery하는 연구의 action 표현으로 바로 쓸 수 있음. 저자가 범용 tokenizer를 HuggingFace AutoProcessor 형식으로 공개했다고 밝혀서, 기존 VLA에 갈아 끼워 비교하기 쉬움.
- step마다 복원 오차를 피드백하는 covering 기반 설계는 manipulation policy의 action 표현과 test-time 재계획 간격을 정할 때 이론적 기준으로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 chunk tokenizer와 streaming tokenizer의 차이를 그린 개념도임. 대기 지연, token 하나의 오류가 퍼지는 범위, 실행 중 관측 반영 가능 여부를 위아래로 비교함. 오른쪽은 VQ codebook과 ActionCodec2 격자가 분포 밖(OOD) 동작을 덮는 방식을 대비함.*

*영상: [저자 프로젝트 페이지의 실로봇 시연 영상으로, 같은 VLA와 과제에서 ActionCodec2가 FAST, X-Tokenizer보다 먼저 과제를 끝내는 장면을 5배속으로 보여 줌.](https://blog-media.assets.alphaxiv.org/videos/01a1d304-992c-7234-adc5-34e8ac8f1545/373555fb-5da9-4f5d-ad2a-4699db253889) (alphaXiv 요약에서 가져옴)*

---

### 2. Recover, Don't Just Continue: Learning from Feedback for Physical Failure Understanding and Correction (74점)

[arXiv](https://arxiv.org/abs/2611.15651) · [PDF](https://arxiv.org/pdf/2611.15651) · [alphaXiv](https://www.alphaxiv.org/abs/2611.15651) (요약 있음) · [프로젝트 페이지](https://pm1255.github.io/embodied-corrector/)

- **저자**: Miao Pan, Kaixiang Yao, Xiaohe Zhou, Xu Wang, Qinfeng Li, Wenqi Zhang, Xuhong Zhang
- **분야**: Failure Recovery · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> 성공 궤적에 실패 요인 하나를 주입해 만든 데이터로, 실행 결과 판정·원인·다음 subtask·세부 복구 계획을 한 번에 내는 교정용 multimodal 모델을 학습함. 고정된 GPT-5.5 code 생성기에 이 교정을 넣으면 실행 조건 10개 평균 성공률이 학습 전 모델 대비 13.9퍼센트포인트 오름.

**무슨 문제인가**

Multimodal LLM 기반 embodied planner는 계획은 그럴듯하게 세우지만, 실행이 의도와 어긋났을 때 무엇이 진행을 막았는지 찾지 못함. EB-ALFRED(시뮬레이션 가정 환경에서 언어 지시를 고수준 행동으로 수행하는 benchmark)의 실패 실행을 보여 주면, RoboBrain 2.5, MiMo-Embodied, InternVL3의 실패 원인 정답률은 모두 30% 이하임. 같은 benchmark에서 실패 사실만 다시 알려 주면 성공률이 거의 오르지 않고, 실패 원인을 알려 주면 오름(MiMo-Embodied-7B 기준 20%에서 27%). 그래서 저자들은 원인을 찾아 남은 계획을 고치는 능력을 따로 학습시켜야 한다고 봄.

**어떻게 푸나**

Embodied-Corrector는 RynnBrain-8B를 바탕으로 한 VQA 모델로, 과제 목표·실행한 workflow·실행 전후 관측·실행 trace를 입력받음. 출력은 Judge(현재 subtask 성공 여부), Cause(관측으로 확인되는 실패 원인), Sub(다음으로 진행할지 현재 subtask를 다시 할지), Fine(Sub를 어떻게 실행할지의 순서가 정해진 행동과 확인 단계) 네 칸임. 학습 데이터는 RoboCasa365(시뮬레이션 주방 과제 300개)와 OmniBehavior(장기 과제 50개)의 성공 궤적에서 만듦. 궤적을 subtask 경계에서 복제하고, 이동·도달 가능성·grasp 자세·제어 timing 등 7종 중 하나의 요인만 바꿔 같은 subtask를 다시 실행해 만듦. 실패가 관측으로 식별되고 현재 상태에서 복구 가능한 경우만 남기며, 복구 실행을 다시 돌려 얻은 궤적을 비공개 모델이 요약해 Fine 정답으로 씀. 학습은 먼저 Judge·Cause를 SFT로 배우고, 정답 Judge·Cause를 앞에 둔 채 Sub·Fine을 배움. 배포 때는 스스로 만든 Judge·Cause 뒤에 계획을 써야 하므로, NEPO(엔트로피 gate를 단 on-policy distillation)로 이 차이를 줄임. 모델이 자기 판정 뒤에 쓴 계획 token마다, 정답 판정을 앞에 뒀을 때의 확률을 기준으로 씀. 기준보다 높은 token은 강화하고 낮은 token은 억제하되, entropy가 높은 위치의 억제는 약하게 함.

**결과**

- EmbodiedDiag-Bench(학습에 쓰지 않은 궤적으로 만든 실패 판정·원인·복구 계획 평가셋)에서 Cause 정확도가 이동 과제 58.2%, 조작 과제 54.6%임. 같은 평가에서 GPT-5.5는 39.8%와 43.2%임. 엔트로피 gate를 빼면 이동 과제 Cause가 50.8%로 내림.
- 고정된 GPT-5.5 code 생성기·로봇 함수·실행 예산으로 OmniBehavior와 LIBERO-PRO(LIBERO 과제를 물체·목표·공간 배치 변형으로 바꾼 평가셋) 10개 조건을 돌림. 교정 모델만 바꿨을 때 평균 성공률이 학습 전 RynnBrain의 55.0%에서 68.9%로 오름. GPT-5.5 자기 교정의 평균은 65.2%이고, 10개 중 2개 조건에서는 GPT-5.5가 더 높음.
- RoboCasa365에서 고정된 π0.5에 교정 모델이 짧은 subtask 지시를 주면, 여러 subtask를 묶은 처음 보는 과제(Composite-Unseen)의 성공률이 1.2%에서 7.3%로 오름. 반면 짧은 단일 과제(Atomic-Seen)에서는 π0.5가 39.6%에서 35.6%로, π0가 34.6%에서 24.4%로 내림.
- 실제 Piper 로봇의 탁상 과제 5개(과제당 20회)에서 과제 평균 성공률이 π0.5 기준 45%에서 62%로, LingBot-VLA 기준 51%에서 70%로 오름. 교정 모델은 episode당 최대 10회의 복구 지시를 낼 수 있음.

**한계**

실로봇 실험은 한 플랫폼의 탁상 과제 5개뿐이고, 교정 없는 조건에 같은 횟수의 단순 재시도를 주는 baseline이 없어 원인 진단의 기여와 재시도 횟수의 기여가 분리되지 않음. 짧은 단일 과제에서는 VLA 성공률이 오히려 내려가서, 교정 모델의 지시 언어가 VLA 학습 분포와 맞지 않는 문제가 남음. Fine 정답은 비공개 모델이 요약해 만들었고 일부 Fine 채점은 사람 평가에 기대며, 코드 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- failure detection/recovery 연구에서 실패 데이터를 성공 궤적의 단일 요인 개입으로 만들고 원인 라벨을 개입에서 바로 얻는 방식은, 원인 라벨을 사람이 달지 않아도 되는 데이터 생성법으로 그대로 쓸 수 있음.
- 고정된 VLA 위에 교정 모델이 subtask 지시를 다시 쓰는 구조라서, VLA 가중치를 건드리지 않는 test-time 복구 방법의 비교 대상이 됨. Atomic 과제 하락은 지시 언어 정렬 문제를 따로 다룰 연구 거리임.

*대표 그림: 측정 결과가 아니라 학습 데이터 구성을 그린 그림임. RoboCasa365(300개 과제, 6,210 episode)와 OmniBehavior(50개 과제, 328 episode) 성공 궤적을 복제·요인 주입·재실행해 Judge·Cause·Sub·Fine 정답을 만드는 5단계를 보여 줌. 걸러진 1,583,014 round로 SFT 후 NEPO를 하는 학습 단계와 Sub·Judge 정답 예시 두 개도 함께 실림.*

*영상: [저자 소개 영상으로, 시뮬레이터 로봇이 그릇을 너무 높게 잡은 뒤 가장자리를 다시 잡아 접시로 옮기는 교정 장면이 담겨 있으며, 이 시연은 학습된 모델이 아니라 GPT와 시뮬레이터 상태 보조 제어로 만든 것임.](https://blog-media.assets.alphaxiv.org/videos/01a1d2ee-8912-7514-9c13-127018d46eb7/8db7c51a-6130-4dc4-8297-ee9e521be514) (alphaXiv 요약에서 가져옴)*

---

### 3. Driving World Models Move the Camera, Not the Scene (74점)

[arXiv](https://arxiv.org/abs/2611.15260) · [PDF](https://arxiv.org/pdf/2611.15260) · [alphaXiv](https://www.alphaxiv.org/abs/2611.15260)

- **저자**: Yuqiao Feng, Xiaoyu Ao
- **분야**: World Model · robotics relevance 6/10 · 1차 스크리닝 68점
- **읽은 원문**: PDF 전문

> 주행 world model에 다른 계획을 주면 카메라 경로는 바뀌지만 장면 속 거리는 거의 바뀌지 않음을, 녹화 로그로 만든 실제 정답과 비교해 보임. 학습 없이 계획을 기하로 넣는 ReTime-Compose를 쓰면, 0.54 m 측면 이동 계획에서 실제 장면 변화를 재현한 비율이 기존 모델 최대 0.23에서 0.93~1.04로 오름.

**무슨 문제인가**

계획 조건부 주행 world model은 후보 계획을 비교하는 데 쓰이므로, 계획이 바뀌면 예측 장면도 실제처럼 바뀌어야 함. 기존 제어 지표(ACT-Bench, DrivingGen, Orbis 논문의 평가 등)는 생성 영상에서 ego 경로를 추정해 명령과 비교하므로 카메라만 검사함. 실제로 달리지 않은 계획의 결과는 녹화되어 있지 않아서, 장면이 계획을 따르는지는 지금까지 측정되지 않았음.

**어떻게 푸나**

저자들은 먼저 녹화 로그에서 달리지 않은 계획의 실제 정답을 만듦. 같은 경로를 느리게 또는 빠르게 지나는 계획은 로그의 시각을 다시 매겨(retiming) 해당 위치에서 녹화된 영상과 LiDAR를 정답으로 씀. 오른쪽으로 0.54 m 옮긴 계획은 KITTI stereo의 오른쪽 카메라가 정답이 됨. 평가 지표 scene response α는 실제 깊이 변화 중 예측이 재현한 비율로, 0이면 계획 무시, 1이면 실제와 같은 변화임. 속도 계획의 α는 깊이 추정기로 깊이를 읽으므로 실제 영상도 1보다 낮은 0.64~0.73이 나오며, 이 값이 사실상 상한임. 생성기 내부 계산을 하나씩 바꾸는 개입 실험으로 원인을 찾고, 이를 바탕으로 ReTime-Compose를 제안함. 이 방법은 고정된 생성기로 기록 속도 rollout을 한 번 만들고, VGGT(영상에서 깊이와 카메라 pose를 추정하는 모델)로 읽은 값으로 그 frame들을 계획된 카메라 위치로 옮김(forward splatting). 옮긴 frame이 덮지 못한 영역만 고정 생성기가 채우고, 덮인 latent token은 고정한 뒤 refiner로 이음매를 다듬음.

**결과**

- 공개된 world model 5개(DrivingWorld, Vista, Epona, Orbis 2, GEM)는 KITTI 속도 계획에서 α가 최대 0.23으로, 실제 영상의 0.64~0.73에 못 미침. 0.54 m 측면 이동에서도 최대 0.23으로 실제 stereo의 0.99와 차이가 큼.
- 기존 지표인 scale-aligned ADE(추정 경로의 scale을 맞춘 뒤 잰 평균 위치 오차)는 실제 영상이 속도 명령을 더 많이 실행해도 내려가지 않음. 공개 모델 5개와 이를 fine-tuning한 변형 10개, 합계 15개 모델에서 이 점수와 α의 Kendall 순위 상관은 +0.16과 -0.03임.
- DrivingWorld에 계획의 실제 frame을 context로 주면 0.5배 속도 계획의 α가 0.19에서 0.61로, 1.5배 계획은 0.09에서 0.56으로 오름. 이때 plan token을 기록 속도로 바꿔도 0.61, 0.59로 거의 변하지 않음.
- ReTime-Compose는 Epona에서 측면 이동 반응을 KITTI 7개 세트 모두에서 0.93~1.04로 올림. 속도를 0.5배, 1.5배로 바꾼 계획의 α가 rollout frame만 재배치하는 re-sampling보다 각각 0.17, 0.16 높음(validation과 test 세트 1~4 합산).

**한계**

속도 정답은 정적 장면에만 성립하고, 회전, 차선 변경 동작, 다른 차량의 반응은 다루지 않음. rollout이 계획된 위치까지 닿아야 하며, 예측을 실제 closed-loop planning에 쓴 실험은 없음. 맥락 하나(계획 3개, seed 2개)에 RTX 4080 SUPER 한 장으로 최대 12분이 걸리고, 코드는 공개 예정이라고만 적혀 있음.

**누리랩 연구와의 연결**

- world model로 후보 행동을 비교하는 test-time planning에서, 행동 조건이 생성 결과의 기하에 실제로 반영되는지 확인하는 counterfactual 평가 방식으로 가져올 수 있음.
- 행동 token보다 context frame이 기하를 정한다는 진단은 로봇 조작용 action-conditioned world model에도 같은 개입 실험으로 확인해 볼 만함.

*대표 그림: ReTime-Compose의 세 단계 구조를 그린 그림으로, 측정 결과가 아니라 방법 구조임. 고정 world model의 한 번 rollout, VGGT로 읽은 깊이와 pose로 계획 위치에 frame을 옮긴 composite(검은 영역은 소스 없음), 덮인 token은 고정하고 나머지만 생성한 뒤 refiner를 거치는 흐름을 보여 줌.*

---

### 4. Fast Inference-Time Policy Refinement via Action-Affine World Models (72점)

[arXiv](https://arxiv.org/abs/2611.15011) · [PDF](https://arxiv.org/pdf/2611.15011) · [alphaXiv](https://www.alphaxiv.org/abs/2611.15011)

- **저자**: Run Wang, Yilin Mo, Liang Wu
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 74점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> 고정된 diffusion policy의 행동 제안 주변에서 작은 보정이 미래 상태를 어떻게 바꾸는지 선형으로 예측하는 world model을 배워, 매 제어 step의 보정을 볼록 QP 하나로 풂. 시뮬레이션 조작 과제 4개의 평균 성공률을 27.2%에서 59.5%로 올렸고, 보정 계산은 step당 평균 3.8ms임.

**무슨 문제인가**

Diffusion Policy 같은 imitation policy는 실행 중 작은 오차가 쌓이면 demonstration 분포를 벗어나 실패함. 이를 고치는 한 방법은 residual policy를 on-policy RL로 추가 학습하는 것인데, 과제당 대략 10만 episode 규모의 상호작용이 듦. 다른 방법은 고정된 world model로 추론 시점에 행동을 고르거나 최적화하는 것임. 기존 GPC(world model로 diffusion policy 제안을 순위 매기거나 gradient로 고치는 방법)는 후보 100개를 평가하거나 world model을 반복 미분해야 해서 step당 수십에서 수백 ms가 듦.

**어떻게 푸나**

A2WM(action-affine world model)은 상호작용 이력과 고정된 policy의 H step 행동 제안을 입력으로 받아 두 가지를 출력함. 하나는 보정이 없을 때의 미래 궤적(nominal prediction)이고, 다른 하나는 보정 수열이 미래 값을 얼마나 바꾸는지 나타내는 action-response matrix F임. 예측 대상에 로봇과 물체 상태뿐 아니라 부품 간 상대 자세 같은 과제 기하량을 넣어, 과제 오차가 보정에 대해 affine이 되게 함. 전체 horizon을 한 번에 직접 예측하므로 중간 예측을 모델에 다시 넣지 않음. 학습은 고정된 policy에 행동 perturbation을 넣어 모은 rollout으로 오프라인에서 하고, horizon 전체 예측 오차와 F가 nominal 예측의 유한차분과 맞도록 하는 항 등을 함께 씀. 배포 시에는 매 step 모델을 한 번 부르고, 이차 과제 비용과 보정 크기 상하한 제약(box constraint)으로 된 convex QP를 HPIPM solver로 풀어 첫 보정만 실행하며 policy와 모델 가중치는 고정임.

**결과**

- FurnitureBench(Isaac Gym에서 가구 부품을 잡고 옮겨 조립하는 과제 모음)의 OneLeg, RoundTable, Lamp와 PushT(T자 블록을 목표 자세로 미는 평면 과제)에서 평가함. 과제당 3 seed, 768 episode 기준 4개 과제 평균 성공률이 고정된 Diffusion Policy(DP)의 27.18%에서 59.51%로 오름.
- 가장 강한 baseline인 GPC-QP(신경망 world model의 Jacobian으로 QP를 만드는 저자 구현 baseline)의 평균 성공률은 47.07%임. RoundTable에서는 A2WM 42.97%, GPC-QP 15.23%이고, Lamp에서는 41.02% 대 25.91%임.
- step당 보정 시간(base policy 샘플링 제외)은 평균 3.80ms로, GPC-QP 39.47ms와 GPC-OPT 401.05ms보다 짧음. PushT에서는 GPC-OPT와 성공률이 78.78%로 같고 보정 시간은 3.40ms 대 346.47ms임.
- 8 step 뒤 위치 RMSE를 직접 예측 값을 1로 두고 비교하면, 재귀 예측은 1-step 감독 17.77, 8-step 감독 1.72임. 모델 계산 시간은 직접 예측 1.0~1.2ms, 재귀 예측 2.1~2.3ms임.

**한계**

모든 실험이 시뮬레이션이고 실로봇 결과는 없음. 로봇과 물체 상태를 측정값으로 받고 과제 목표 기하량을 사람이 지정한다고 가정하므로, 이미지 입력이나 상태 추정 오차가 있는 경우는 다루지 않음. PushT 예시에서 보정 범위 밖에서는 선형 예측이 틀렸고, 예측 정확도 비교는 모델 용량을 맞추지 않은 채 이루어짐.

**누리랩 연구와의 연결**

- test-time optimization 관점에서, world model 출력 형태를 최적화가 쉬운 affine 꼴로 정하면 후보 샘플링이나 미분 없이 ms 단위 보정이 된다는 사례임. VLA action chunk를 실행 중 고치는 연구의 baseline이나 설계 참고로 쓸 수 있음.
- 측정 상태와 손으로 정한 기하 목표에 기대므로, 시각 입력 policy에 붙이려면 object-centric 상태 추정이나 학습된 과제 비용이 먼저 필요함.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 고정된 base policy가 K step마다 action chunk를 내고, A2WM이 nominal 궤적과 causal action-response matrix F를 출력해 QP로 보정을 구한 뒤 첫 보정만 실행하는 흐름을 보여 줌.*

---

### 5. Bind-WAM: Binding-Uncertainty-Guided Selective Future Imagination in World Action Models (72점)

[arXiv](https://arxiv.org/abs/2611.15368) · [PDF](https://arxiv.org/pdf/2611.15368) · [alphaXiv](https://www.alphaxiv.org/abs/2611.15368)

- **저자**: Chenhao Qiu, Shuyi Chen, Songen Gu, Shufeng Nan, Tianyu Wang, Siyu Lin, Yifan Li, Bingwen Zhu 외 1명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 68점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 9쪽
- **읽은 원문**: PDF 전문

> World action model이 미래 영상을 매 replanning마다 만들지 않고, 지시문의 물체와 화면 속 물체의 대응이 불안정할 때만 만들게 함. LIBERO에서 미래 생성을 40.6%의 replanning에서만 쓰고도 성공률 98.6%를 얻고, 매번 생성할 때보다 완료 시간을 25.6% 줄임.

**무슨 문제인가**

World action model(WAM)은 미래 영상과 action을 함께 예측해 policy를 돕지만, 미래 영상 생성은 계산이 큼. 기존 방법은 미래를 매번 상상하거나(Fast-WAM-Joint), 배포 시 아예 빼거나(Fast-WAM) 둘 중 하나를 고름. 그런데 현재 관측만으로 대상 물체와 action이 분명한 상태도 많고, 물체가 가려지거나 비슷한 물체가 섞인 상태도 있음. 어느 상태에서 미래 상상이 필요한지 판단할 해석 가능한 신호가 없었음.

**어떻게 푸나**

Bind-WAM은 language-object binding uncertainty(지시문이 가리키는 물체 역할이 현재 화면의 물체에 안정적으로 대응되는지의 불확실성)를 그 신호로 씀. 먼저 오프라인에서 demonstration마다 32 frame을 뽑아 Qwen3-VL-32B로 과제 관련 물체를 찾고, SAM 3.1로 mask를 추적하고, DINOv3 feature로 정체성 유지를 잼. 참조 frame에서 Qwen이 확인한 참조 mask와 원래 후보 track의 IoU가 0.3 미만이거나, 물체가 안 보이거나, feature 유사도가 0.9 미만이면 그 frame을 불확실(1)로 표시함. 이 pseudo-label로 RGB 이미지와 지시문만 받아 불확실성 U를 내는 6.65M parameter predictor를 학습함. 실행 중에는 U가 기준값 이상이거나 직전 replanning 대비 U의 변화량이 기준값 이상이면 joint path를 고름. Joint path는 미래 영상 latent와 action chunk를 함께 denoising함. 그 밖의 경우에는 현재 frame만 보고 action을 denoising하는 direct path를 고름. 두 path는 같은 WAM(Wan2.2-5B 기반)을 공유하고 action-to-video attention mask만 다름.

**결과**

- LIBERO(시뮬레이션 단일 팔 조작, Spatial·Object·Goal·Long 4개 suite 각 10과제, 과제당 50회)의 평균 성공률이 98.6%임. 같은 설정으로 재현한 Fast-WAM은 97.1%, Fast-WAM-Joint는 98.4%임. 성공 episode의 평균 완료 시간은 Fast-WAM-Joint의 15.73초에서 11.71초로 줄어듦.
- 같은 비율(약 40.6%)로 joint path를 쓰는 routing 비교에서 불확실성 기반 routing이 98.6%, 무작위 routing이 97.4%, 일정 간격 routing이 97.5%임. 완료 시간은 14.58~14.64초에서 11.71초로 줄어듦.
- RoboTwin 2.0(시뮬레이션 양팔 조작) 7과제 평균 성공률이 clean 조건 88.3%, randomized 조건 87.0%임. Fast-WAM-Joint 대비 각각 0.58, 0.86퍼센트포인트 높고, clean에서는 action만, 시각 추론, 텍스트 추론 중 하나를 고르는 기존 적응형 방법 AdaWAM(88.4%)보다 약간 낮음.
- 실제 양팔 로봇 과제 3개(수건 접기, 병 건네 상자에 넣기, 모양 맞춰 끼우기)에서 과제당 11회 평가함. 평균 성공률이 66.6%로 Fast-WAM-Joint 57.6%, Fast-WAM 42.4%보다 높고, 미래 생성은 replanning의 28.4%에서만 씀.

**한계**

LIBERO와 RoboTwin에서 Fast-WAM-Joint 대비 성공률 차이는 1퍼센트포인트 이하라서, 이득의 대부분은 성공률보다 시간 절감임. 실로봇은 과제당 11회뿐이라 1회 차이가 약 9퍼센트포인트에 해당함. Pseudo-label은 물체 grounding 실패만 반영하고 실제로 미래 상상이 결과를 바꿨는지는 학습에 쓰지 않으며, 기준값은 benchmark마다 정해야 함. 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- World model 추론을 상태에 따라 켜고 끄는 test-time compute 배분 연구에서 비교 대상이 됨. 같은 비율의 무작위 routing을 baseline으로 둔 ablation 설계도 참고할 만함.
- Binding 불확실성 신호는 failure detection과 active perception의 trigger로도 쓸 수 있음. 가려짐이나 비슷한 물체 혼동을 감지해 시점을 바꾸거나 재확인하는 정책과 결합해 볼 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림이며, 왼쪽은 Qwen3-VL과 SAM 3.1·DINOv3로 pseudo-label을 만드는 학습용 파이프라인임. 가운데는 불확실성 U를 내는 predictor와 router, 오른쪽은 두 path가 공유하는 WAM과 attention mask를 보여 줌.*

---

### 6. AFTER: A World Model with Adaptive Fast--Slow Timescales for Error-Driven Retention (68점)

[arXiv](https://arxiv.org/abs/2611.15215) · [PDF](https://arxiv.org/pdf/2611.15215) · [alphaXiv](https://www.alphaxiv.org/abs/2611.15215)

- **저자**: Haoyi Zhang, Qi Zhang, Yunfan Ren, Yi Bin, Lei Zhu, Heng Tao Shen
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 76점
- **읽은 원문**: PDF 전문

> 로봇 dynamics가 갑자기 바뀌어도 world model이 예측 오차로 빠르게 따라가고 그 적응을 rollout 끝까지 유지하도록, 사라지는 fast 보정과 남는 slow 보정을 나눠 둠. 시뮬레이션 5개 데이터셋에서 1~40스텝 예측 오차의 평균이 가장 강한 비교 모델보다 16.4~33.7% 낮음.

**무슨 문제인가**

로봇이 무게를 모르는 물체를 들거나 관절이 고장 나면 dynamics가 갑자기 바뀌고 그 상태가 계속됨. world model이 이를 따라가지 못하면 open-loop rollout에서 예측 오차가 쌓여 planning이 틀어짐. 저자는 세 가지 요구를 제시함: 변화에 바로 반응하는 responsiveness, 일시적 충격과 지속적 변화를 가리는 stability, 새 관측 없이도 적응을 유지하는 persistence. 기존 online-adaptive world model(GrBAL, ReBAL, MOLe 등)은 step size나 history 길이 같은 한 가지 timescale로만 적응하므로 반응 속도와 안정성을 맞바꾸게 됨.

**어떻게 푸나**

AFTER-WM(Adaptive Fast-slow Timescales for Error-driven Retention World Model)은 사전학습 후 고정한 MLP expert 3개와 router로 이루어진 mixture of experts를 base로 씀. 입력은 최근 64스텝의 상태·행동 전이(context)와 앞으로 40스텝의 행동이고, 출력은 40스텝 상태 예측임. context를 한 스텝씩 읽으며 각 expert의 one-step 예측 오차를 계산하고, 이 오차로 gradient 없이 세 가지 online memory를 갱신함. fast state는 감쇠 계수로 매 스텝 줄어드는 보정이고, slow state는 Kalman filter 형태의 학습된 gain으로 오차를 누적하는 보정임. routing memory는 오차에 따라 expert 조합 가중치를 바꾸되 expert 자체는 고치지 않음. rollout 중에는 fast state만 계속 줄고 slow state와 가중치는 고정되므로, 앞 스텝은 fast 보정이, 뒤 스텝은 slow 보정과 routing이 맡게 됨.

**결과**

- 시뮬레이션 5개 데이터셋(MuJoCo의 HalfCheetah 2종, Panda·UR5e 팔, Hopper에서 payload·마찰·모터 세기 등을 바꿈)에서 10개 비교 모델과 비교함. multi-step 평균 오차(1·5·10·20·40스텝 평균 오차의 평균)가 가장 강한 모델(ReBAL 또는 MOLe)보다 16.4~33.7% 낮고, 5개 seed 모두에서 낮음.
- Panda에서 multi-step 평균 오차가 MOLe의 0.0711에서 0.0473으로 내려감. 변화 직후 1~4스텝 구간에서도 가장 가까운 모델보다 최소 15.6% 낮음.
- 변화 후 20~30스텝 구간의 40스텝 앞 예측에서, online memory 갱신으로 줄어든 오차 비율이 AFTER-WM 33%, 가장 강한 비교 모델 14%임. 갱신을 끄면 비교 모델보다 나아지지 않음.
- 실제 고정익 UAV 고장 비행 데이터 ALFA에서 multi-step 평균 오차가 모든 비교 모델보다 최소 13.1% 낮음. JSHC(HalfCheetah 다리 관절 하나가 100스텝마다 힘을 잃는 데이터셋)의 control 과제에서도 평가함. 모든 모델이 같은 cross-entropy method planner를 쓸 때 평균 return이 93.1로 2위 MOLe보다 13.8 높음.

**한계**

입력은 이미지가 아니라 관절 각도·속도 같은 저차원 상태이고, 실로봇 실험은 없음. 실데이터(ALFA)는 기록된 행동에 대한 예측 평가만 했고, control은 시뮬레이션 과제 하나뿐임. 코드와 데이터셋은 공개 예정이라고만 적혀 있음.

**누리랩 연구와의 연결**

- 예측 오차를 사라지는 성분과 남는 성분으로 나눠 쌓는 구조는, 조작 중 payload 변화나 관절 이상을 감지하고 world model 기반 planner를 그대로 이어 쓰는 failure recovery 연구의 baseline으로 쓸 수 있음.
- gradient 없이 context만으로 적응하는 test-time adaptation 방식이라, VLA나 world model에 붙이는 test-time optimization 비교 대상이 됨. 다만 이미지 입력으로 확장되는지는 확인되지 않음.

*대표 그림: 왼쪽은 측정 결과가 아니라, 사람이 예상보다 무거운 컵을 들 때의 predictive coding을 그려 AFTER-WM의 세 설계와 대응시킨 개념도임. 오른쪽은 실제 측정값으로, 변화 후 경과 스텝 구간별로 AFTER-WM의 오차가 가장 가까운 비교 모델보다 몇 % 낮은지를 JSHC·Panda·UR5e·Hopper에 대해 보인 heatmap임.*

---

### 7. Learning Low-Latency Action Verification for Frozen Vision-Language-Action Models (68점)

[arXiv](https://arxiv.org/abs/2611.14834) · [PDF](https://arxiv.org/pdf/2611.14834) · [alphaXiv](https://www.alphaxiv.org/abs/2611.14834) · [프로젝트 페이지](https://wen-hanhsieh.github.io/hdh/)

- **저자**: Wen-Han Hsieh, Ken Jiankun Zheng, Chia-Chien Chen, David M. Chan, Trevor Darrell
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 72점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 10쪽
- **읽은 원문**: PDF 전문

> 고정된 VLA가 뽑은 action chunk 후보 2개 중 하나를, 자기 rollout의 최종 성공·실패만으로 학습한 작은 verifier가 골라 실행함. 실로봇 과제 3개 평균 성공률이 44.7%에서 67.3%로 오름.

**무슨 문제인가**

π0.5 같은 flow matching 기반 VLA는 같은 관측에서도 매번 다른 action chunk를 뽑고, 그 품질 차이가 큼. 그런데 보통은 한 번 뽑은 chunk를 그대로 실행하므로 이 분포를 활용하지 못함. 여러 후보를 뽑아 고르는 기존 방법은 큰 VLM으로 후보를 평가하거나 expert demonstration에서 합성 선호 데이터를 만들어야 했음. 큰 VLM 평가는 query마다 지연이 커서 실시간 제어에 쓰기 어려움.

**어떻게 푸나**

HDH(Hindsight Decision Model with History)는 policy 가중치를 바꾸지 않고 후보 선택만 학습하는 verifier임. 먼저 고정된 VLA를 과제마다 그대로 돌려 rollout을 모으고, 각 query의 관측과 실제 실행한 action 8스텝에 그 episode의 최종 성공·실패를 label로 붙임. verifier는 VLA 내부의 SigLIP 이미지 feature 128 token, proprioception, 후보 action을 입력으로 받아 최종 성공 확률을 출력함. action token이 관측 token에 cross-attention하는 작은 transformer이고, 직전 query 최대 3개의 관측과 실행 action을 GRU로 요약한 history token 하나를 더함. history가 없는 판은 HDM이라 부름. parameter 수는 HDM 481K, HDH 845K임. 실행 시에는 VLA가 noise seed만 달리해 chunk 후보 2개를 뽑고, verifier 점수가 높은 후보의 앞 8스텝을 실행함.

**결과**

- LIBERO-10(여러 단계로 된 시뮬레이션 조작 과제 10개 모음) 중 4개 과제에서 평균 성공률이 후보 하나를 그대로 실행하는 고정 π0.5 78.8%, 같은 후보에서 무작위 선택 77.5%, HDH 82.3%임. 과제당 50개 초기 상태를 3회 돌린 결과임.
- history를 뺀 HDM은 평균 80.3%이고, GPT-6를 verifier로 쓰면 80.7%, GPT-5는 78.3%임. query당 중간값 지연은 baseline 681ms, HDH 718ms, GPT-6 7,403ms, GPT-5 27,674ms임.
- Franka Panda 실로봇 과제 3개(인형을 접시에 놓기, 서랍에서 큐브 꺼내고 닫기, 딸기를 장에 넣고 문 닫기)를 과제당 50회씩 평가함. 평균 성공률이 44.7%에서 67.3%로 오름.
- 실로봇 과제별 Fisher exact test에서 인형 과제(64%에서 94%)와 장 과제(32%에서 56%)는 유의함. 서랍 과제(38%에서 52%)는 p=0.23으로 유의하지 않음.

**한계**

verifier를 과제마다 따로 학습하므로 새 과제마다 rollout을 다시 모아야 함(시뮬레이션은 과제당 100개). 후보 수는 2개로만 실험했고, 시뮬레이션 이득 3.5퍼센트포인트는 4개 과제 3회 실행 기준이라 실로봇보다 근거가 약함. 지연 측정에 simulator 시간이 포함되고 실로봇 지연 분해는 보이지 않음.

**누리랩 연구와의 연결**

- 최종 성공·실패 label만으로 action 단위 성공 확률을 예측하는 구조라 failure detection과 test-time action selection을 한 모델로 묶는 baseline으로 쓸 수 있음.
- 고정된 VLA 위에 붙이는 작은 verifier이므로, 우리 VLA 실험에서 후보 수를 늘리거나 history 대신 robot memory 표현을 넣는 비교 실험을 바로 설계할 수 있음.

*대표 그림: 측정 결과가 아니라 HDH의 동작 구조를 그린 개념도임. 관측과 지시문을 받은 고정 VLA가 후보 chunk 2개를 만들고, verifier가 성공 확률 0.16과 0.72를 매겨 높은 쪽을 실행하는 흐름을 보여 줌.*

---

### 8. Remember What Changes the Odds: Critic-Gated Event Memory for Long-Horizon Manipulation (68점)

[arXiv](https://arxiv.org/abs/2611.16386) · [PDF](https://arxiv.org/pdf/2611.16386) · [alphaXiv](https://www.alphaxiv.org/abs/2611.16386)

- **저자**: Xuanzhuo Liu, Chuankang Li, Maoqing Yao, Guanghui Ren
- **분야**: Robot Memory · robotics relevance 9/10 · 1차 스크리닝 68점
- **읽은 원문**: PDF 전문

> 같은 관측에서 다른 행동이 필요한 long-horizon 조작에서, critic이 예측한 성공 확률이 크게 바뀐 순간만 기억에 남기는 방식을 제안함. 정확한 성공 확률을 계산할 수 있는 10단계 진단 과제에서 성공률 88.0%를 냄.

**무슨 문제인가**

long-horizon 조작에서는 같은 관측이 시도 전, 실패 후, 성공 후에 모두 나올 수 있음. 저자들은 이를 decision aliasing이라 부름. 현재 관측과 지시문만 보는 π0 계열 VLA는 이 셋을 구분하지 못함. 기존 event memory 방법은 화면 변화, 의미 정보, 팔·gripper 움직임으로 기억할 순간을 고르는데, 접촉 실패처럼 흔적이 남지 않지만 다음 행동을 바꾸는 사건을 놓칠 수 있음.

**어떻게 푸나**

CGEM(Critic-Gated Event Memory)은 critic이 예측한 최종 성공 확률이 한 step 사이에 δ 이상 바뀌면 그 순간을 기억에 씀. 기억할 후보 순간은 critic 점수의 급변, force/torque 변화점(BOCPD로 검출), gripper 개폐에서 뽑음. force는 화면이나 gripper 상태에 드러나지 않는 접촉 결과를 알려 줌. 확률이 오르면 progress record, 내리면 failure record로 저장하고, 어느 subtask와 어떤 시도 방식에 관한 것인지도 함께 적음. failure record는 해당 subtask가 완료되면 지움(consolidation). 기억 용량 K를 넘으면 가장 오래된 record를 버림. policy는 현재 관측, 지시문, 기억을 입력으로 받아 행동을 냄. 이론으로는 고정된 reference policy에서 성공 확률이 martingale이므로, δ 이상 변화의 기대 횟수가 과제 길이와 무관하게 1/(4δ²) 이하임을 보임. π0.5에 gated cross-attention으로 기억을 읽게 하는 구조도 제안하지만 이것은 구현·평가되지 않음.

**결과**

- ASC(Aliased Stage Chain: 같은 home 자세로 돌아오며 순서가 정해진 subtask N개를 반복 수행하는 표 형태 진단 환경)에서 측정함. N=10일 때 CGEM 성공률은 88.0%이고, 36 step 관측 window와, gripper 개폐와 화면 변화로 순간을 고르는 kinematic event memory는 둘 다 0.0%임. 과제 상태를 그대로 저장한 oracle은 97.3%임.
- 같은 N=10에서 failure record를 빼면 성공률이 1.7%로 내림. 완료된 subtask의 failure record를 지우지 않으면 47.7%로 내림.
- force 정보를 빼면 N=10 성공률이 14.2%로 내림. N=6에서 progress·failure 구분 정확도가 99.3%에서 68.3%로 내린 것이 원인으로 제시됨.
- 실제 양팔 로봇의 충전기 꽂기 데이터(테스트 87개 episode, 실패 구간 42개)에서 학습된 critic을 실패 검출기로 평가함. 사람 실패 라벨 없이 VLM reward로 학습한 IQL critic이 step 단위 AUROC 0.86, 분당 오경보 0.12회에서 recall 76%를 냄.

**한계**

주 실험은 정확한 성공 확률로 맞춘 lookup table과 tabular behavior cloning을 쓰는 인공 환경 하나뿐임. π0.5 통합과 LIBERO-Long·실로봇 평가는 계획으로만 적혀 있고, 실제 데이터 실험도 실패 검출만 재고 기억을 쓰는 policy는 돌리지 않음. 이론의 충분성 결과는 모든 과제 상태 변화가 큰 성공 확률 변화와 일치한다는 가정에 기댐.

**누리랩 연구와의 연결**

- robot memory에서 무엇을 기억할지를 성공 확률 변화로 정한 기준임. failure record를 retry 전략 선택에 쓰는 구조는 failure detection과 recovery 연구에 바로 붙일 수 있음.
- 실제 데이터에서 TD residual을 실패 검출 신호로 쓴 비교(사람 라벨 유무, Monte Carlo return 회귀 대 IQL critic)는 VLA용 critic 기반 failure detector를 만들 때 기준선으로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 입력을 받은 critic이 성공 확률 변화가 δ 이상일 때 progress·failure record를 최대 K개 기억에 쓰고, π0.5 policy가 이 기억을 읽어 행동하는 흐름을 보여 줌.*

---

### 9. Topology-Aware 4D Gaussian Splatting for Egocentric Videos (68점)

[arXiv](https://arxiv.org/abs/2611.16012) · [PDF](https://arxiv.org/pdf/2611.16012) · [alphaXiv](https://www.alphaxiv.org/abs/2611.16012) (요약 있음) · [프로젝트 페이지](https://topoego.github.io)

- **저자**: Leonardo Vanni, Stefano Gasperini, Federico Tombari, Chiara Plizzari
- **분야**: 3D Vision · robotics relevance 7/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> 1인칭 영상에서 물체가 잘리거나 열리는 순간 이후를, 부분별 rigid motion 분기와 Gaussian 켜고 끄기로 다시 만드는 Topo-4DGS를 제안함. 사건 이후 프레임의 물체 영역 PSNR이 가장 강한 baseline 19.83dB에서 24.30dB로 오름.

**무슨 문제인가**

4D Gaussian Splatting(4DGS) 계열 동적 복원은 고정된 Gaussian 집합을 시간에 따라 변형하는 방식임. 그래서 자르기, 조립, 열기, 닫기처럼 물체의 연결 구조가 바뀌는 사건(topological event)을 표현하지 못함. 한 덩어리였던 부분이 따로 움직이기 시작하거나 처음 보이는 단면이 생기면 ghosting이나 빠진 형상이 나옴. 저자 분석으로 Ego4D 주석 영상의 68.8% 이상, EPIC-KITCHENS의 80.0% 이상에 이런 사건이 있는데, 이를 따로 평가하는 1인칭 영상 benchmark도 없었음.

**어떻게 푸나**

입력은 단안 1인칭 RGB 영상, 카메라 pose, 물체·손 mask, 그리고 사건 시각·조각 수 K·조각의 분리 관계를 담은 event tree임. 출력은 정적 배경과 여러 동적 물체의 4D Gaussian 표현임. Motion Bifurcation은 각 조각에 별도의 rigid 궤적을 주고, 각 Gaussian이 어느 조각을 따를지를 확률로 섞어 위치를 정함. 이 확률은 위치만 보는 MLP(spatial branch)와, 사건 전후로 0에서 1로 바뀌는 sigmoid gate(temporal branch)를 더해 정함. 시간은 이 gate로만 들어가므로 사건 사이에는 조각 배정이 바뀌지 않음. Topological Boundary Resolution은 두 조각이 갈라지는 접촉면에 평면을 맞춰 새 Gaussian으로 단면을 채움. 각 Gaussian의 opacity에 시간 창을 곱해 새 면은 사건 시각에 켜고 가려지는 면은 끔. 붙이기와 닫기는 영상을 거꾸로 돌려 분리 문제로 바꿔 같은 방식으로 풂.

**결과**

- TopoEgo(EPIC-KITCHENS·Ego4D에서 고른 1인칭 클립 24개, 분리·결합·열기·닫기 사건 34개)에서 사건 이후 프레임의 물체 영역 PSNR이 24.30dB임. 가장 강한 baseline인 손 영역을 빼고 학습한 Deformable 3D Gaussians(Def-3DGS)는 19.83dB, 가장 가까운 선행 연구 EgoGaussian은 16.79dB임.
- 사건 종류 4개 × 데이터 출처 2개, 모두 8개 묶음에서 전체 프레임 물체 영역 PSNR로 모두 1위임. 사건 이후 프레임만 잰 위 수치와 다른 지표이며, 묶음별 최강 baseline과의 차이는 최대 1.26dB임. 열기와 분리에서 차이가 크고 결합과 닫기에서는 작음.
- 8개 클립 ablation에서 event gate 대신 시간에 따라 자유롭게 바뀌는 MLP를 쓰면 사건 이후 PSNR이 26.77dB에서 19.41dB로 내림. 구성 요소를 하나씩 더하면 Motion Bifurcation으로 19.07dB에서 23.05dB, 단면 채우기로 23.27dB, 시간 창 활성화로 26.77dB까지 오름.
- 구조 변화가 없는 클립 6개(Rigid Objects Control)에서도 물체 PSNR이 27.92dB로 EgoGaussian 27.34dB보다 높음.

**한계**

사건 시각, 조각 수, event tree를 사람이 준 값으로 받으며, 자동 추정 모듈은 보조 자료의 전처리 단계로만 있고 본 평가에 쓰이지 않음. 평가는 같은 클립의 프레임을 번갈아 학습·평가에 나눈 영상 재현 PSNR이라, 새 시점이나 3D 형상 정확도는 재지 않음. 조각이 대략 rigid라고 가정하므로 반죽처럼 크게 변형되는 물체에서는 실패함.

**누리랩 연구와의 연결**

- 조작 중 물체가 갈라지거나 열리는 순간을 object-centric 3DGS로 표현하는 방법임. 자르기, 뚜껑 열기 같은 조작 과제의 4D scene 표현이나 human video에서 조작 장면을 복원하는 연구의 비교 대상으로 쓸 수 있음.
- 사건 시각과 event tree가 주어져야 동작하므로, 로봇이 이를 스스로 찾아내는 문제(사건 검출, scene graph 갱신)와 묶으면 연구 질문이 됨.

*대표 그림: TopoEgo의 사건 종류 4개(분리, 결합, 열기, 닫기)마다 실제 1인칭 클립 2개의 사건 전후 프레임을 보여 줌. 피자 자르기, 주전자 조립, 도시락 열고 닫기 등에서 바뀌는 물체를 청록색 윤곽으로 표시했고, 복원 결과가 아니라 benchmark 예시임.*

---

### 10. HeMeR: Heterogeneous Memory Reconciliation for Embodied Agents via Structured KV Reuse (66점)

[arXiv](https://arxiv.org/abs/2611.16487) · [PDF](https://arxiv.org/pdf/2611.16487) · [alphaXiv](https://www.alphaxiv.org/abs/2611.16487)

- **저자**: Saehun Chun, Wonje Choi, Jinwoo Jang, Taeyoon Kwack, Honguk Woo
- **분야**: Embodied AI · robotics relevance 8/10 · 1차 스크리닝 76점
- **학회**: NeurIPS 2026 채택 · 근거: comments에 "Accepted at NeurIPS 2026 (Oral)"
- **읽은 원문**: PDF 전문

> embodied agent가 여러 memory를 합쳐 쓸 때, 바뀐 memory 부분의 KV cache만 다시 계산하고 나머지는 재사용하는 추론 방식을 제안함. ALFWorld에서 step당 추론 시간을 가장 강한 baseline MemRL의 0.90초에서 0.18초로 줄임.

**무슨 문제인가**

foundation model 기반 embodied agent는 declarative(명시적 지식), procedural(행동 절차), working(최근 관측) memory에서 꺼낸 내용을 하나의 memory context로 묶어 입력함. 기존 memory 연구는 무엇을 저장하고 꺼낼지에 집중하고, 묶인 context를 model이 어떻게 처리할지는 다루지 않음. 그래서 결정 step마다 context 일부만 바뀌어도 전체를 새 입력으로 보고 KV cache를 처음부터 다시 계산함. 기존 KV 재사용 기법은 segment 단위 재사용이나 LoRA adapter 전환 중 하나만 다루므로, 내용 변경과 adapter 전환이 함께 일어나는 경우를 처리하지 못함.

**어떻게 푸나**

HeMeR(Heterogeneous Memory Reconciliation)는 memory context를 token 열이 아니라 memory chunk의 열로 관리함. 각 chunk에는 ID, memory 종류, 역할, 내용, 의존 관계, 위치, 대응하는 KV 범위, adapter ID를 적은 index(memory schema)가 붙음. 매 step마다 이전 context와 현재 context의 chunk를 ID로 맞춰 보고, 위치를 뺀 schema 항목이 모두 같은 chunk만 KV 재사용 대상으로 둠. 새 chunk는 prefill하고 빠진 chunk의 KV는 지우며, 위치만 바뀐 chunk는 RoPE 회전을 다시 적용해 key의 위치 정보만 고침(RoPE remapping). procedural memory는 LoRA adapter로 구현되어 있어, adapter가 바뀌면 해당 chunk와 그에 의존하는 chunk의 KV만 다시 계산함. adapter 간 KV 차이를 줄이려고 LRAgent의 shared-attention LoRA 설계(down-projection과 key 경로 공유)를 따르고, 나머지 KV는 근사적으로 재사용함. 입력은 관측, 목표, memory context이고 출력은 다음 행동임.

**결과**

- ALFWorld(텍스트로 집안일 과제를 수행하는 환경, Llama-3.2-3B 사용)의 처음 보는 과제에서 성공률이 71.43%임. 가장 강한 baseline인 MemRL(과거 궤적을 검색해 쓰는 memory agent)은 52.86%임. step당 추론 시간은 0.90초에서 0.18초로 줄어듦.
- EmbodiedBench Habitat(RGB 관측으로 3D 집 환경에서 물체를 옮기는 과제, Qwen3-VL-4B 사용)에서 성공률은 HeMeR 76.27%, MemRL 61.80%이고, step당 시간은 1.82초 대 2.68초임. KV를 재사용하는 CacheBlend·KEEP·LRAgent의 KV 재사용 비율은 42.96~46.25%이고, HeMeR는 72.81%임.
- ALFWorld의 memory 갱신 기록을 재생한 비용 분석에서, 다시 계산한 token은 4,219개로 전체 재계산(Full Rebuild)의 74,784개 대비 5.6%임. cache 처리 시간 합계는 199.4초에서 25.8초로 줄어듦.
- 실제 UR7e 팔로 탁상 장기 과제 2개를 과제당 5회 반복함(방법당 10회). 목표 단위 성공률은 83.20%로 MemRL의 64.28%보다 18.92퍼센트포인트 높고, step당 시간은 2.94초에서 1.87초로 줄어듦.

**한계**

KV 재사용은 전체 재계산의 근사인데, 성공률이 오른 이유가 cache 처리인지 baseline과의 memory 구성 차이인지 가려지지 않음. 같은 memory 구성에서 전체 재계산을 했을 때의 성공률은 본문에서 확인 불가함. 실로봇 실험은 과제 2개, 방법당 10회이고, procedural memory가 shared-attention LoRA로 구현된다는 가정과 단일 agent 설정에 기댐.

**누리랩 연구와의 연결**

- robot memory를 무엇을 저장할지가 아니라 추론 비용 관점에서 다룬 사례임. 여러 memory를 쓰는 VLM 기반 planner를 실로봇에 올릴 때 step당 지연을 줄이는 방법의 비교 대상으로 쓸 수 있음.
- 성공률 향상과 cache 재사용의 관계가 분리되지 않았으므로, 같은 memory 구성에서 전체 재계산과 비교하는 실험으로 먼저 확인할 필요가 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 왼쪽은 환경 변화로 세 종류 memory가 바뀔 때 KV cache 전체를 다시 계산하는 단순 방식이고, 오른쪽은 HeMeR가 영향받은 KV만 다시 계산하고 나머지는 재사용하는 구조임.*

---

### 11. What Makes a VLA Reactive? A Study of Execution Strategies for Dynamic Manipulation (63점)

[arXiv](https://arxiv.org/abs/2611.15491) · [PDF](https://arxiv.org/pdf/2611.15491) · [alphaXiv](https://www.alphaxiv.org/abs/2611.15491) (요약 있음)

- **저자**: Zhuoyue Li, Zhendong Han, Pankhuri Vanjani, Wenting Li, Rudolf Lioutikov
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 68점
- **학회**: CoRL 2026 채택 · 근거: 1쪽에 "10th Conference on Robot Learning (CoRL 2026)"
- **읽은 원문**: PDF 전문

> 움직이는 물체를 다루는 VLA의 반응성을 policy만이 아니라 실행 방식(horizon, 비동기 추론, chunk 연결)까지 묶어 π0.5로 비교한 실증 연구임. 실로봇 컨베이어 과제 9개 조건의 평균 성공률이 execution horizon만 s=5로 바꿔도 71.1%로, latent RL로 policy를 고친 결과(64.4~68.9%)와 비슷하거나 높았음.

**무슨 문제인가**

VLA는 관측 하나에서 미래 행동 여러 개를 묶은 action chunk를 예측함. 물체가 움직이면 chunk를 다 실행하기 전에 그 계획이 낡은 관측에 기댄 것이 됨. 더 자주 다시 예측하면 될 것 같지만, 추론 호출이 늘고 chunk 사이 궤적이 끊길 수 있음. 빠른 추론, 비동기 실행, chunk 연결, 움직임 정보 같은 처방이 따로따로 나왔으나 같은 조건에서 함께 비교된 적이 없었음.

**어떻게 푸나**

저자들은 새 방법을 내지 않고 π0.5를 공통 base policy로 두고 기존 처방들을 옮겨 심어 비교함. 입력은 카메라 관측, 언어 지시, proprioception이고 출력은 길이 H(prediction horizon)의 Cartesian action chunk이며, 그중 앞의 s개(execution horizon)만 실행한 뒤 다시 예측함. 첫째로 H는 fine-tuning 때, s는 배포 때 바꾸고, action entropy로 s를 고르는 AAC(Adaptive Action Chunking)도 시험함. 둘째로 동기 실행(chunk를 다 실행하고 다음 예측을 기다림)과 비동기 실행(실행 중에 다음 chunk를 추론)을 비교함. 비동기 실행 쪽에서는 첫 행동을 일찍 내주는 FASTER·DynamicVLA와, 이전 chunk와 이어지게 만드는 RTC(inference-time inpainting)·ABPolicy(B-spline 제어점 예측과 연속성 보정)를 비교함. 셋째로 policy 자체를 바꾸는 쪽으로 PUMA(과거 optical flow와 미래 물체 feature 감독)와 DSRL(VLA는 고정하고 입력 noise를 고르는 latent actor-critic 학습)을 시험함.

**결과**

- 시뮬레이션 DOM(굴러가는 레몬을 집어 그릇에 넣는 과제)에서 같은 policy(H=25)의 성공률은 s=2일 때 동기 19%, 비동기 32%임. horizon이 짧을수록 두 실행 방식의 차이가 커짐.
- 실로봇 컨베이어 과제(움직이는 벨트 위 빨간 큐브 집기, 설정당 20회)에서 s=10일 때 동기 π0.5와 동기 PUMA는 20%, 비동기 방법들은 60~75%임. RTC와 FASTER는 둘 다 75%로, 첫 행동까지 시간이 약 0.1초인 FASTER가 약 0.33초인 RTC보다 낫지 않았음. 최고는 ABPolicy 95%이나 s=9에서만 평가됨.
- 빠른 벨트(5 cm/s)에서 행동 실행 주기를 20 Hz에서 30 Hz로 올리면 ABPolicy가 13%에서 93%로, FASTER가 0%에서 33%로 오름(조건당 15회).
- DSRL은 겨냥한 조건에서 DOM 성공률을 32%에서 47%로, 가장 어려운 컨베이어 조건의 성공 횟수를 5회 중 0회에서 15회 중 9회(60%)로 올림. 9개 컨베이어 조건 평균은 원래 48.9%에서 64.4~68.9%가 됨. DSRL 적용 전의 1k checkpoint(π0.5를 1,000 step fine-tuning한 것)를 학습 없이 s=5로만 실행해도 71.1%임.

**한계**

각 처방은 원래 시스템을 그대로 재현한 것이 아니라 π0.5 위에 일부 기법만 옮긴 것이라, 원 논문 성능에 대한 판단으로 읽으면 안 됨. 실로봇 비교는 설정당 15~20회임. 굴러오는 캔 집기와 움직이는 컵에 넣기 과제는 사람이 물체를 움직여서 방법마다 물체 궤적이 같지 않음. ABPolicy는 action 표현과 학습까지 바뀌어서 연속성만의 효과로 분리되지 않으며, 코드 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- VLA 실험에서 성공률만이 아니라 execution horizon, 동기·비동기, chunk 연결 방식을 함께 보고해야 한다는 근거임. 우리 VLA·manipulation 실로봇 평가 프로토콜에 observation age, 첫 행동까지 시간, chunk 연속성을 기록 항목으로 넣을 때 참고할 수 있음.
- DSRL 같은 test-time steering의 이득은 실행 설정만 바꿔 얻는 이득과 비슷했음. test-time optimization이나 failure recovery 방법을 평가할 때 실행 파이프라인 baseline부터 맞춰야 함.

*대표 그림: 측정 결과가 아니라 연구 구조를 그린 개념도임. 왼쪽은 컨베이어 위 큐브에 대해 낡은 관측으로 짠 궤적과 새 관측으로 다시 짠 궤적을 대비함. 가운데는 긴 execution horizon과 짧은 horizon의 재계획을 비교함. 오른쪽은 π0.5를 중심으로 관측 신선도·추론 스케줄링·chunk 연속성·policy가 서로 얽힌 관계와 해당 방법 이름을 보여 줌.*

---

### 12. Prediction or Persistence? What Future-Prediction Scores Miss About World Models (63점)

[arXiv](https://arxiv.org/abs/2611.15082) · [PDF](https://arxiv.org/pdf/2611.15082) · [alphaXiv](https://www.alphaxiv.org/abs/2611.15082) (요약 있음)

- **저자**: Animesh Maheshwari
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 72점
- **학회**: CoRL 2026 채택 · 근거: comments에 "Accepted at the CoRL 2026 Workshop "Do Robots Need World Models?""
- **읽은 원문**: PDF 전문

> world model의 future-prediction 점수를, predictor만 끈 같은 모델(persistence control)의 점수와 짝지어 predictor의 몫만 따로 잼. 같은 27,000개 시행에서 V-JEPA 2의 predictor는 top-1을 0.03~0.04만 올리고 V-JEPA 2.1의 predictor는 0.291 올림.

**무슨 문제인가**

로봇 학습에 쓸 사전학습 video world model(V-JEPA 2, DINO-WM 등)은 주로 future-prediction 점수로 비교되고 선택됨. 이 점수에는 encoder가 장면을 잘 표현하는 정도, 가까운 미래가 방금 본 장면과 닮은 정도, predictor가 다음 장면을 실제로 예상하는 정도가 함께 들어 있음. predictor가 아무 일도 하지 않아도 앞의 두 요인만으로 점수가 chance보다 높게 나올 수 있음. 그래서 점수 하나로는 예측 구조가 일을 하는지 알 수 없는데, world model 비교에는 이를 가를 trivial baseline이 대개 빠져 있음.

**어떻게 푸나**

평가 과제는 future retrieval임. 모델은 가정 egocentric 영상에서 A초 길이의 관측 구간(anchor)을 보고, 같은 영상에서 자른 W초 후보 11개 중 실제로 이어지는 구간을 고름(chance 0.091). 후보가 모두 같은 영상에서 나오므로 장면 인식만으로는 맞힐 수 없음. 각 모델은 고정된 encoder로 anchor를 embedding하고, 고정된 predictor로 W초 뒤 표현을 만든 뒤, 자기 training criterion(energy)이 가장 낮은 후보를 고름. 추가 학습은 없음(zero-shot). persistence control은 predictor를 identity로 바꾼 같은 모델이며, 방금 본 장면과 가장 닮은 후보를 고르는 셈임. 두 top-1의 차이를 predictor contribution으로 정의하고, 음수면 예측하지 않는 것보다 못한 predictor로 판정함. 가정 영상 1,094개(479시간)로 시행을 만들고, 5개 모델이 모두 채점한 27,000개 시행(영상 704개, (A, W) 조합 25개)을 비교에 씀.

**결과**

- V-JEPA 2 ViT-H와 ViT-L의 top-1은 0.437과 0.424로 chance의 4배를 넘음. 같은 encoder의 persistence control이 0.396이라 predictor contribution은 0.0408과 0.0284에 그침.
- V-JEPA 2.1 ViT-g는 같은 시행에서 top-1 0.736, persistence control 0.444로 predictor contribution이 0.291임. V-JEPA 2의 약 7~10배이며, 모든 contribution 구간은 video 단위 cluster bootstrap 95% 신뢰구간에서 0을 포함하지 않음.
- 시뮬레이션 PushT(블록 밀기 과제)로 학습한 action-conditioned 모델 DINO-WM은 top-1 0.136으로 chance보다 높지만, predictor를 끄면 0.315로 오름. action을 0으로 넣은 학습 분포 밖 측정이라 저자도 크기는 참고용으로만 다룸.
- DINO-WM과 달리 학습 분포 안에 있는 V-JEPA 2에서도, 예측 horizon 1초에서는 ViT-L이 0.452로 persistence control 0.500보다 낮음. V-JEPA 2.1은 horizon 1초에서 4초로 늘 때 0.824에서 0.590으로 내리며 control과 0.27~0.31 차이를 유지함.

**한계**

로봇이 없는 passive video 실험이라 planning, control, 실로봇 성능에 대한 결론은 나오지 않음. 11개 후보 중 고르기는 시간 위치를 맞히는 과제라 미래 장면 생성보다 쉽고, 도메인은 가정 영상 하나뿐임. V-JEPA 2.1은 checkpoint 하나만 평가했고 두 계열은 여러 요인이 함께 달라 차이의 원인을 특정하지 못함. 코드는 공개 예정으로만 적혀 있음.

**누리랩 연구와의 연결**

- world model을 사전학습 출발점이나 planning용으로 고를 때, predictor를 끈 같은 모델과의 차이를 forward pass 한 번으로 함께 재는 점검 절차로 바로 쓸 수 있음.
- world model 예측 오차를 failure detection 신호로 쓰는 연구에서, 그 신호가 predictor에서 오는지 단순한 장면 연속성에서 오는지 가르는 대조군 설계로 쓸 수 있음.

*대표 그림: 같은 영상에서 자른 4초 anchor와 4초 후보 11개(-24초~+20초)를 시간순으로 놓고, 모델별 energy 막대와 선택한 후보를 표시한 예시 시행 두 개임. (a) 오이 껍질 벗기기에서는 V-JEPA 2.1만 정답(+0초)을 고르고 persistence control과 V-JEPA 2 ViT-L은 +4초, DINO-WM은 +8초를 고르며, (b) 바닥에 물 붓기에서는 모든 모델이 틀림.*

---

### 13. VBot Exo2Ego Policy: Lightweight Data Collection and Exocentric-to-Egocentric Video Generation (62점)

[arXiv](https://arxiv.org/abs/2611.16417) · [PDF](https://arxiv.org/pdf/2611.16417) · [alphaXiv](https://www.alphaxiv.org/abs/2611.16417) (요약 있음)

- **저자**: Tong Rao, Zhihao Zhang, Yuntian Wang, Siyu Zhou, Hailong Qin, Yinan Yu
- **분야**: Video · robotics relevance 8/10 · 1차 스크리닝 74점
- **읽은 원문**: PDF 전문

> 3인칭 조작 영상을 골라 준 사람의 1인칭 영상으로 바꾸는 video diffusion 모델과, 이를 학습시킬 짝 영상 수집 방식을 함께 내놓음. 546개 검증 clip에서 기존 EgoX보다 PSNR이 12.630에서 15.856으로 오르고 FVD가 306.90에서 191.55로 내려감.

**무슨 문제인가**

1인칭(EGO) 영상은 손과 조작 물체, 작업 공간을 한 화면에 담아 조작 학습에 쓸모가 큼. 그러나 1인칭 영상을 다양하게 모으려면 착용 장비와 참가자 노력이 많이 듦. 3인칭(EXO) 영상은 인터넷에 많지만 시점을 바꾸면서 행위자와 손-물체 상호작용을 보존해야 함. 가장 가까운 기존 방법 EgoX는 목표 시점으로 렌더링한 기하 prior가 있어야 하므로, 카메라 보정 정보가 없는 인터넷 영상에는 쓰기 어려움.

**어떻게 푸나**

VBot Exo2Ego Policy는 EXO clip, 텍스트, 선택적 행위자 참조 이미지를 받아 141 frame짜리 EGO RGB 영상을 출력함. 먼저 Qwen3.8-VL이 EXO frame과 손·물체 영역, 상호작용 기록을 읽고 대상 행위자의 동작과 순서를 텍스트로 씀. 생성기는 사전학습된 video diffusion transformer(MiniMax-H3 Ref2VA)를 고정하고 RGB LoRA만 flow-matching으로 학습함. 학습 중에는 보정된 목표 카메라의 각 pixel 광선을 6차원으로 나타낸 Plücker ray를 clip마다 확률적으로 EGO token에 더하고, 이 확률을 학습 70~80% 구간에서 0으로 줄임. 그래서 추론 때는 목표 카메라 보정이 필요 없음. 추가로 손·팔·물체 semantic mask를 예측하는 branch와, 손 keypoint 추출기 ACE-Ego-Hand의 feature와 2D keypoint를 맞추는 손 loss가 RGB LoRA에 gradient를 보냄. 학습용 짝 데이터는 LiDAR가 달린 iPhone 두 대로 같은 동작을 EGO와 EXO에서 동시에 찍어 얻고, 녹화 시작 때 두 카메라가 같은 영역을 찍게 해 시점 간 기하 정렬을 잡음.

**결과**

- 자체 검증 세트 546 clip(86회 촬영, 학습에 없던 장소 71 clip 포함)에서 49 frame 기준 PSNR이 공개 EgoX의 12.630에서 15.856으로 오름. FVD는 306.90에서 191.55로 37.6% 내려감. EgoX는 추론 때 목표 시점 기하 prior를 쓰고 이 방법은 쓰지 않음.
- 학습에 없던 장소 71 clip에서도 PSNR·SSIM·LPIPS·CLIP-I·FVD 5개 지표가 모두 나아짐. FVD는 1146.71에서 908.01로 내려갔지만 학습한 장소(199.79)보다 훨씬 높음.
- 생성 영상에 손 keypoint 추출기 ACE-Ego-Hand를 따로 돌려 손 관절을 읽으면, 이미지 폭 5% 이내로 맞은 관절 비율(PCK@5%)이 RGB만 학습한 모델의 11.52%에서 손 loss를 넣은 모델(ACEaux)의 20.02%로 오름. 관절 평균 오차는 57.09에서 47.42 pixel로 내려감.
- semantic mask 공동 학습으로 PCK@5%가 5.0퍼센트포인트 오르고, 공식 annotation 기준 물체 IoU가 5.5%에서 7.8%로 오름. 관절 검출 비율은 92.4%에서 90.8%로 내려감.

**한계**

생성 영상의 화질과 손·물체 판독만 평가했고, 생성 데이터로 로봇 policy를 학습해 성공률이 오르는지는 보이지 않음. EgoX 비교는 입력 frame 수와 학습 방식이 다른 전체 시스템끼리의 비교이고, 손 loss 비교도 RGB-only 기준 모델과 학습 예산이 달라 각 구성 요소의 효과를 분리하지 못함. 검증 세트를 checkpoint 선택에도 썼고, 학습에 없던 물체에서의 개선은 확인되지 않았으며 코드 공개 정보도 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- 인터넷 3인칭 조작 영상을 1인칭 손-물체 데이터로 바꿔 manipulation pretraining이나 VLA 학습 데이터를 늘리는 경로임. 실제 policy 성능 향상은 직접 검증해야 할 부분임.
- 생성 영상에서 손 keypoint와 물체 mask를 함께 뽑을 수 있어, 사람 영상에서 손 궤적을 얻어 로봇 행동으로 옮기는 연구의 입력으로 비교해 볼 만함.

*대표 그림: 논문 1쪽 대표 그림으로, 인터넷 영화 장면, 공개 데이터셋, 자체 수집 데이터에서 고른 3인칭 입력과 생성된 원형 어안 1인칭 frame을 한데 모아 보여 줌. 저자가 고른 예시이며 측정 결과는 아님.*

---

### 14. Does Your World Model Know Actions Have Consequences? (58점)

[arXiv](https://arxiv.org/abs/2611.15048) · [PDF](https://arxiv.org/pdf/2611.15048) · [alphaXiv](https://www.alphaxiv.org/abs/2611.15048) (요약 있음)

- **저자**: Ayush Gaggar, Jared Berry, Todd D. Murphey
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 70점
- **학회**: CoRL 2026 (comments 표기) · 근거: comments에 "Presented at "Do Robots Need World Models?" Workshop at Conference on Robot Learning (CoRL) 2026"
- **읽은 원문**: PDF 전문

> world model이 행동을 조금 바꿨을 때 결과가 어떻게 달라지는지 맞히는지를 재는 지표 AP(Action Perturbation)를 제안함. 시뮬레이션 peg 삽입 과제에서 상태 예측 오차가 비슷한 두 dynamics head의 AP가 1.39와 0.75로 갈림.

**무슨 문제인가**

world model은 실제로 움직이지 않고도 다른 행동을 했을 때의 결과를 상상할 수 있다는 점에서 다른 end-to-end 학습 방법과 구별됨. 그런데 지금 쓰는 평가 지표는 복원 영상의 선명도, 상태 예측 오차, 과제 성공률이라서 이 능력을 직접 재지 않음. 복원이 흐린 모델도 planning에는 쓸 만할 수 있고, 학습 분포 안에서 성공률이 높은 모델도 분포 밖 행동에는 취약할 수 있음. 저자는 world model로 counterfactual 행동을 검토(counterfactual auditing)하려면 행동 변화에 대한 반응을 맞히는지부터 확인해야 한다고 주장함.

**어떻게 푸나**

저자는 system identification처럼 world model을 입출력 함수로 보고, 알려진 입력 변화에 대한 반응(forced response)을 검사함. 같은 초기 상태에서 원래 행동열과 첫 행동만 δ만큼 바꾼 행동열을 각각 굴려서 두 결과의 차이를 구함. 시뮬레이터가 준 차이와 world model이 예측한 차이를 비교하고, 상대 오차를 실제 차이의 크기로 가중 평균한 값이 AP임. latent를 상태로 옮기는 데는 encoder latent에 ridge regression으로 맞춘 linear probe를 씀. 차이의 차이를 보므로 상태 예측의 일정한 bias는 상쇄됨. AP는 낮을수록 좋고, 1이면 바뀐 행동을 무시한 것과 같으며, 1보다 크면 무시하는 것보다 나쁨. 실험은 공개된 TD-MPC2(latent dynamics 기반 model-based RL) checkpoint에서 dynamics head만 다시 학습해 비교함. 학습 데이터는 작업공간 격자 탐색, 전문가 시연, 시연에 Gaussian 행동 noise를 넣은 것 세 가지이며 각각 100k interaction임.

**결과**

- 시뮬레이션 과제 Peg(상자 옆면에 peg 꽂기)의 on-policy 궤적 50개에서 측정함. ∥δ∥=0.2, 5 step 예측 기준 상태 오차는 시연 학습 head 0.154, noise 주입 head 0.120으로 비슷함. 같은 조건의 AP는 1.39 대 0.75로, 시연 학습 head는 행동 변화를 무시하는 것보다 나쁨.
- Push(큐브 밀기)에서 같은 조건의 AP는 시연 학습 0.72, noise 주입 0.62, 격자 탐색 2.28임. probe 오차만으로 생기는 하한(probe floor)은 0.37임. 1 step 예측에서는 noise 주입 head의 AP가 1.31로 시연 학습 head의 0.76보다 나빴음.

**한계**

AP는 같은 상태에서 여러 행동을 굴려 봐야 하므로 시뮬레이터 reset이 필요하고, 실로봇 실험은 없음. 과제는 2개, 모델은 TD-MPC2 하나이고, AP가 낮을수록 planning 성능이 좋아지는지는 보이지 않음. noise 주입 head는 여러 크기의 noise를 섞어 학습했고, noise 크기에 따라 AP가 어떻게 바뀌는지는 따로 보이지 않음.

**누리랩 연구와의 연결**

- world model 기반 test-time planning이나 counterfactual reasoning을 할 때, 상태 예측 오차와 별도로 행동 민감도를 맞히는지 점검하는 평가 항목으로 바로 가져다 쓸 수 있음.
- world model을 failure detection이나 recovery 판단에 쓰는 연구라면, 학습 데이터에 시연 밖 행동을 섞어야 하는 근거로 이 결과를 참고할 수 있음.

*대표 그림: 측정 결과가 아니라 기존 지표의 한계를 보여 주는 예시 그림임. 왼쪽은 흐린 decoder 복원과 실제 장면을 옆에 놓아 복원 품질과 planning 품질이 별개임을 보이고, 오른쪽은 분포 안에서 성공률 100%인 policy가 분포 밖 목표에서 실패하는 모습을 보임.*

---

### 15. Where to Generate Touch: Do Image Latents Preserve Material Recognition? (58점)

[arXiv](https://arxiv.org/abs/2611.15834) · [PDF](https://arxiv.org/pdf/2611.15834) · [alphaXiv](https://www.alphaxiv.org/abs/2611.15834) (요약 있음)

- **저자**: Wanghao Ye, Aarosh Das, Sihan Chen, Yiting Wang, Bowei Tian, Guoheng Sun, Shwai He, Zheyu Shen 외 21명
- **분야**: Tactile Perception · robotics relevance 8/10 · 1차 스크리닝 68점
- **읽은 원문**: PDF 전문

> 촉감 이미지 생성기를 어느 latent space에서 학습할지를, 실제 촉감으로 학습한 재질 분류기가 encode-decode 복원본도 읽어 내는지로 고름. ObjectFolder Real에서 SD-VAE 복원은 재질 정확도를 0.3퍼센트포인트, 16배 압축 이산 tokenizer 3종은 6.5~9.7퍼센트포인트 낮춤.

**무슨 문제인가**

촉감 데이터는 녹화할 때마다 물체를 실제로 눌러야 해서 양이 적음. 물체 사진에서 촉감을 생성하면 데이터를 늘릴 수 있지만, 실제 촉감으로 학습한 모델이 생성된 촉감을 읽을 수 있어야 쓸모가 있음. GelSight와 DIGIT는 젤 표면의 변형을 RGB 이미지로 찍으므로, 이미지 생성 모델의 autoencoder나 tokenizer를 그대로 생성기의 latent space로 쓸 수 있음. 그런데 복원 이미지가 눈으로 비슷해 보여도 재질을 가르는 정보가 남는지는 따로 확인된 적이 없고, PSNR만으로는 가까운 후보끼리 순위가 갈리지 않음.

**어떻게 푸나**

저자들은 생성기를 학습하기 전에 후보 latent space를 고르는 transfer test를 제안함. 실제 press(센서를 물체에 한 번 누른 프레임 열)를 후보 모델로 encode한 뒤 다시 decode함. 실제 press로 학습한 재질 분류기의 정확도가 원본에서 복원본으로 바뀔 때 얼마나 내려가는지(drop)를 잼. 분류기는 고정된 DINOv2-base feature 위의 class-balanced logistic regression이고, CLIP과 Sparsh(촉감 전용 self-supervised encoder) feature 위의 분류기로도 같은 측정을 반복함. 같은 제품의 크기·색 변형이 학습과 평가에 나뉘지 않도록 제품군 단위로 fold를 나누고, 제품군 bootstrap 90% 구간의 하한이 0보다 크면 유의한 drop으로 봄. 후보는 이산 tokenizer(MAGVIT-v2, Janus-Pro, Cosmos DI 16배·8배)와 연속 autoencoder(SD-VAE 8배, Cosmos CI 16배·8배)이고, GelSight로 fine-tuning한 MAGVIT-v2도 넣음. 분류기 학습 데이터 일부를 같은 label의 복원본으로 바꿔 다시 학습하는 probe retraining으로 손실 중 얼마가 입력 분포 차이인지도 봄. 마지막으로 고른 SD-VAE latent에서 물체 사진, 접촉 부위 형상, 고정된 누르기 policy를 조건으로 8프레임 press를 만드는 rectified-flow 생성기를 학습함.

**결과**

- ObjectFolder Real(로봇이 GelSight로 71개 물체를 누른 2,093개 press, 재질 7종)에서 원본 정확도는 34.0%임(chance 14.3%). 16배 이산 tokenizer 복원본에서 drop은 MAGVIT-v2 6.5, Janus-Pro 9.7, Cosmos DI 8.1퍼센트포인트이고 모두 유의함. SD-VAE는 0.3퍼센트포인트로 유의하지 않음. Touch and Go(사람이 야외에서 GelSight로 찍은 재질 14종, 3,082개 touch)에서도 이산 3종은 7.5~11.8퍼센트포인트, SD-VAE는 0.7퍼센트포인트 내려감.
- 다른 센서인 DIGIT의 YCB-Slide(물체 10개 위를 미끄러뜨린 50개 궤적, 3,000 프레임) 물체 인식에서 원본 정확도는 77.3%임. 이산 3종은 21.1~28.0퍼센트포인트, SD-VAE는 1.2퍼센트포인트(90% 구간 -0.4~2.8) 내려감.
- 압축 배율을 맞춘 Cosmos 이산·연속 쌍에서 이산 쪽 drop이 16배에서 7.6퍼센트포인트, 8배에서 1.0퍼센트포인트 더 큼. GelSight로 fine-tuning하거나 decoder만 다시 학습한 MAGVIT-v2도 4.0~5.1퍼센트포인트 drop이 남음. 저자들은 16배 손실의 대부분이 양자화에서 온다고 해석함.
- 18개 물체의 535개 실제 press로 물체를 맞히는 gallery matching 정확도가 원본 gallery 78.9%, SD-VAE 복원 76.7%, MAGVIT-v2 복원 67.0%임. probe retraining은 새 label 없이 16배 이산 tokenizer 정확도를 31.6~32.7%까지 올림(원본 34.0%).

**한계**

생성기는 생성 예시 3개를 보여 주는 데 그치고, 생성 촉감의 정량 평가나 robot policy 학습에 써서 나아지는지는 보이지 않음. 결론이 분류기에 따라 바뀜: Touch and Go에서 CLIP 분류기를 쓰면 SD-VAE도 13.0퍼센트포인트 내려감. 기준 분류기의 원본 정확도 자체가 34.0%로 낮아 재질 정보 보존을 재는 도구로서 민감도가 제한적이고, 코드는 accept 후 공개 예정임.

**누리랩 연구와의 연결**

- tactile perception 데이터를 생성으로 늘리려 할 때, 생성기를 만들기 전에 latent space를 고르는 저비용 점검 절차로 쓸 수 있음. visuo-tactile manipulation policy의 촉감 입력을 압축하거나 생성할 때 SD-VAE와 16배 이산 tokenizer 중 무엇을 쓸지 판단 근거가 됨.
- 복원 이미지 화질 대신 하위 분류기 성능으로 latent를 비교하는 방식은 world model latent가 접촉·재질 정보를 남기는지 점검하는 데도 옮겨 쓸 수 있음.

*대표 그림: 논문 Figure 1로, 왼쪽은 ObjectFolder Real 로봇과 GelSight press 프레임, 가운데는 SD-VAE 8배(43.5 dB)와 MAGVIT-v2 16배(36.0 dB) 복원본과 오차 지도를 보여 줌. 아래 막대는 측정된 재질 정확도(원본 34.0%, SD-VAE 33.6%, MAGVIT-v2 27.4%)이고, 오른쪽은 사진·RGB-D·policy를 받는 rectified-flow 생성기의 구조도와 생성 예시 3개를 실제 촉감 옆에 놓은 것임.*

---

## 오늘의 흐름

- **world model이 행동을 정말 반영하는지 따로 재기**: 예측 점수가 높아도 행동을 바꿨을 때 결과가 바뀌는지는 별개라는 점검 논문이 세 편 나옴. predictor를 끈 같은 모델과 비교하거나, 행동을 조금 흔들거나, 녹화 로그로 만든 정답과 비교하는 방식임. [Prediction or Persistence?](https://arxiv.org/abs/2611.15082), [Does Your World Model Know Actions Have Consequences?](https://arxiv.org/abs/2611.15048), [Driving World Models Move the Camera, Not the Scene](https://arxiv.org/abs/2611.15260)
- **고정된 policy 위에서 고르고 고치기**: policy 가중치는 그대로 두고, 작은 verifier나 선형 world model로 행동을 고르거나 고침. 교정 모델로 실패 뒤 복구 지시를 내는 방법도 나옴. [Action-Affine World Models](https://arxiv.org/abs/2611.15011), [Low-Latency Action Verification](https://arxiv.org/abs/2611.14834), [Recover, Don't Just Continue](https://arxiv.org/abs/2611.15651)
- **비싼 추론을 필요할 때만 켜기**: Bind-WAM은 지시문 물체와 화면 물체의 대응이 불안정할 때만 미래 영상을 만듦. HeMeR는 바뀐 memory 부분의 KV cache만 다시 계산함. [Bind-WAM](https://arxiv.org/abs/2611.15368), [HeMeR](https://arxiv.org/abs/2611.16487)
- **action을 어떻게 쪼개고 언제 실행하는지**: 같은 VLA라도 action 표현과 실행 설정을 바꾸면 성공률이 크게 달라진다는 결과가 두 편 나옴. 한 편은 step마다 action을 내보내는 tokenizer를 만듦. 다른 한 편에서는 execution horizon(추론한 chunk 중 실제로 실행하는 step 수)만 바꿔도 71.1%가 나와, latent RL로 policy를 고친 64.4~68.9%와 비슷하거나 높았음. [ActionCodec2](https://arxiv.org/abs/2611.15490), [What Makes a VLA Reactive?](https://arxiv.org/abs/2611.15491)
- **무엇을 기억하고 얼마나 오래 유지할지**: Critic-Gated Event Memory는 critic의 성공 확률이 크게 바뀐 순간만 기억함. AFTER는 로봇 dynamics 변화에 대한 world model 보정을 빨리 사라지는 부분과 오래 남는 부분으로 나눔. [Critic-Gated Event Memory](https://arxiv.org/abs/2611.16386), [AFTER](https://arxiv.org/abs/2611.15215)

## 해볼 만한 연구

### world model의 행동 민감도를 failure detection 신호로 쓰기

- 질문: 조작 중 실패를 미리 잡는 데, world model의 예측 오차보다 행동을 흔들었을 때의 결과 변화량이 더 나은 신호인지 밝힘.
- 첫 실험: 같은 action-conditioned world model에서 세 신호의 LIBERO rollout 실패 검출 AUROC를 비교함. 세 신호는 예측 오차, predictor를 끈 같은 모델 대비 오차, AP(행동을 조금 바꿨을 때 결과 변화를 맞히는 정도)임.
- 가장 가까운 연구: [Does Your World Model Know Actions Have Consequences?](https://arxiv.org/abs/2611.15048)는 AP를 world model 평가 지표로만 썼고, 실패 검출 신호로 쓰지 않았음.

### chunk 중간에 verifier를 돌려 바로 복구하기

- 질문: streaming action tokenizer로 chunk 중간에 관측을 다시 볼 수 있을 때, step 단위 verifier가 실패를 더 일찍 잡고 복구 성공률을 올리는지 확인함.
- 첫 실험: ActionCodec2 기반 VLA에서 chunk 끝에서만 후보를 고르는 verifier와 매 step 고르는 verifier를 같은 실로봇 과제로 비교함. 성공률과 실패 검출 시점을 함께 잼.
- 가장 가까운 연구: [Low-Latency Action Verification](https://arxiv.org/abs/2611.14834)은 chunk 단위로 후보 2개 중 하나만 고르고, 실행 도중의 검출과 복구는 다루지 않음.

### 불확실할 때만 world model로 행동 보정하기

- 질문: world model 보정을 매 step 켤 때와, 지시문 물체와 화면 물체의 대응이 불안정할 때만 켤 때의 성공률·계산량 차이를 밝힘.
- 첫 실험: 고정 diffusion policy에 선형 world model 기반 QP 보정(Action-Affine 방식)을 붙임. 항상 켜기, 무작위로 40% 켜기, 대응 불안정 신호로 켜기를 비교함.
- 가장 가까운 연구: [Bind-WAM](https://arxiv.org/abs/2611.15368)은 미래 영상 생성만 켜고 끄며, 행동 자체를 고치는 보정은 하지 않음.

## 꼭 읽을 논문

- [ActionCodec2: A Streaming Action Tokenizer](https://arxiv.org/abs/2611.15490): 처음 보는 장면의 실제 Franka 과제 4종에서 task progress(완료한 milestone 비율)가 기존 tokenizer FAST의 50.8%에서 73.9%로 오름. tokenizer가 HuggingFace로 공개돼 바로 비교해 볼 수 있음.
- [Recover, Don't Just Continue](https://arxiv.org/abs/2611.15651): 성공 궤적에 실패 요인 하나를 넣어 원인 라벨이 붙은 실패 데이터를 만드는 방식이라 failure recovery 데이터 구축에 참고할 수 있음.
- [Driving World Models Move the Camera, Not the Scene](https://arxiv.org/abs/2611.15260): 주행 계획을 바꾸면 카메라 경로만 바뀌고 장면 속 거리는 거의 안 바뀜을, 녹화 주행 로그로 만든 정답과 비교해 보인 평가 방식임.
- [Fast Inference-Time Policy Refinement via Action-Affine World Models](https://arxiv.org/abs/2611.15011): 시뮬레이션 조작 과제 4개의 평균 성공률을 27.2%에서 59.5%로 올렸고, 보정 계산은 step당 평균 3.8 ms임(실로봇 결과 없음).
- [Learning Low-Latency Action Verification for Frozen VLA Models](https://arxiv.org/abs/2611.14834): 최종 성공·실패만으로 과제마다 학습한 verifier로 실로봇 과제 3개의 평균 성공률을 44.7%에서 67.3%로 올림.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (646편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2611.15215'>AFTER: A World Model with Adaptive Fast--Slow Timescales for Error-Driven Retention</a></td><td>76</td><td>9</td><td>World Model</td><td>payload 변화 같은 갑작스러운 동역학 변화에 대해 fast 보정은 사라지고 slow 보정은 유지되며 pre-trained expert 가중치를 동적으로 섞는 world model AFTER-WM을 제안함, 5개 로봇 시뮬레이션에서 다단계 오차가 최강 baseline보다 16-34% 낮고 UAV 실데이터도 검증함, 로봇 동역학 적응에 직접 관련됨</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2611.16487'>HeMeR: Heterogeneous Memory Reconciliation for Embodied Agents via Structured KV Reuse</a></td><td>76</td><td>8</td><td>Embodied AI</td><td>HeMeR는 declarative, procedural, working memory 내용이 바뀔 때 바뀐 부분의 KV state만 다시 계산하고 나머지는 재사용하는 추론 틀임. ALFWorld, Habitat, 실로봇에서 MemRL 대비 step당 추론 시간을 2.94초에서 1.87초로 줄이면서 성공률 83.20%를 보임. robot memory와 효율적 추론이 만나는 실용적 기여임</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2611.15011'>Fast Inference-Time Policy Refinement via Action-Affine World Models</a></td><td>74</td><td>9</td><td>Manipulation</td><td>pretrained policy를 action-affine world model로 inference-time에 빠르게 refine하는 접근임</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2611.16417'>VBot Exo2Ego Policy: Lightweight Data Collection and Exocentric-to-Egocentric Video Generation</a></td><td>74</td><td>8</td><td>Embodied AI</td><td>3인칭 영상을 선택한 행위자의 1인칭 관측으로 바꾸는 Exo2Ego 영상 생성 모델과 경량 수집 앱을 제안함. 풍부한 영상으로 1인칭 조작 데이터를 늘리는 현실적 경로임</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2611.14834'>Learning Low-Latency Action Verification for Frozen Vision-Language-Action Models</a></td><td>72</td><td>9</td><td>VLA</td><td>frozen VLA의 sampled action을 hindsight로 학습한 경량 verifier로 저지연 선택함</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2611.15651'>Recover, Don&#x27;t Just Continue: Learning from Feedback for Physical Failure Understanding and Correction</a></td><td>72</td><td>9</td><td>Failure Recovery</td><td>물리적 실패 이해와 교정을 feedback 학습으로 다루는 MLLM 연구임</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2611.15082'>Prediction or Persistence? What Future-Prediction Scores Miss About World Models</a></td><td>72</td><td>8</td><td>World Model</td><td>world model의 미래 예측 점수가 predictor 기여와 persistence를 섞는다고 지적하고, predictor를 호출하지 않는 동일 복사본 대조로 V-JEPA 2.1은 +0.291, V-JEPA 2는 +0.03 정도임을 분리해 보인 평가 방법론임</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2611.16012'>Topology-Aware 4D Gaussian Splatting for Egocentric Videos</a></td><td>72</td><td>7</td><td>3D Vision</td><td>egocentric 영상에서 절단·조립·개폐 같은 topology 변화를 다루는 4DGS와 TopoEgo 벤치마크를 만듦. 고정 표현 변형의 한계를 짚어 embodied 장면 표현에 새 문제 설정이 됨</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2611.15048'>Does Your World Model Know Actions Have Consequences?</a></td><td>70</td><td>9</td><td>World Model</td><td>embodied world model이 행동 결과를 반영하는지 counterfactual 관점으로 진단함</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2611.15490'>ActionCodec2: A Streaming Action Tokenizer</a></td><td>70</td><td>9</td><td>VLA</td><td>streaming 디코딩 가능한 VLA action tokenizer로 지연을 줄이는 설계임</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2611.15368'>Bind-WAM: Binding-Uncertainty-Guided Selective Future Imagination in World Action Models</a></td><td>68</td><td>9</td><td>World Model</td><td>binding 불확실성으로 선택적 미래 imagination을 수행하는 world action model임</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2611.15491'>What Makes a VLA Reactive? A Study of Execution Strategies for Dynamic Manipulation</a></td><td>68</td><td>9</td><td>VLA</td><td>동적 조작에서 VLA action chunk의 stale 문제와 execution 전략을 체계 분석함</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2611.16386'>Remember What Changes the Odds: Critic-Gated Event Memory for Long-Horizon Manipulation</a></td><td>68</td><td>9</td><td>Robot Memory</td><td>critic이 gating하는 event memory로 long-horizon 조작 기억을 구성함</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2611.15834'>Where to Generate Touch: Do Image Latents Preserve Material Recognition?</a></td><td>68</td><td>8</td><td>Tactile</td><td>생성 촉각용 latent 선택을 위해 GelSight 재질 분류기가 이미지 tokenizer 재구성에서 얼마나 유지되는지 측정함. SD-VAE는 0.3점 하락, 16x tokenizer는 6.5~9.7점 하락으로 촉각 생성의 latent 선택 근거가 됨</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2611.15260'>Driving World Models Move the Camera, Not the Scene</a></td><td>68</td><td>6</td><td>World Model</td><td>driving world model이 카메라만 움직이고 장면 반응은 실제의 3분의 1 이하임을 log retiming과 stereo 참조로 보이고, 계획을 기하로 전달하는 training-free ReTime-Compose로 보완한 진단 연구임</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2611.15585'>Marginal-Preserving Coupled Diffusion Composition for Long-Horizon Planning</a></td><td>68</td><td>6</td><td>Planning</td><td>사전학습 compositional diffusion planner의 chunk별 초기 noise에 marginal은 표준 Gaussian으로 유지하고 이웃끼리 양의 상관을 주는 training-free 추론법이며, OGBench stitch 과제에서 추론 시간 증가 없이 성공률을 올림. long-horizon planning에 가볍게 붙는 아이디어이나 로봇 실험은 없음</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2611.15317'>BiPOP: Partial-Order Planning for Long-Horizon Bimanual Robotic Manipulation</a></td><td>66</td><td>9</td><td>Manipulation</td><td>partial-order planning으로 long-horizon bimanual 협응을 구성하는 접근임</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2611.14840'>SPIRE: Task-agnostic embodied continual learning through autonomous situation inference and causal motor-primitive reuse</a></td><td>66</td><td>8</td><td>RL</td><td>신호 label 없이 상황을 추론하고 motor primitive를 재사용하는 continual control 방법임. 평가가 좌표, 3관절, hidden force 제어로 단순하고 baseline이 spiking 계열 위주임</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2611.15429'>IncR-3DSGG: Incremental Posed RGB Image Based 3D Scene Graph Generation via Privileged Depth Supervision</a></td><td>66</td><td>7</td><td>3D Vision</td><td>depth 센서 없이 posed RGB 이미지로 3D scene graph를 점진 생성하고 학습 때만 depth를 privileged supervision으로 씀. embodied agent용 scene graph에 직접 연결됨</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2611.15287'>Track4D: Representing Dense 3D Tracking for Video Diffusion Models</a></td><td>66</td><td>6</td><td>3D Vision</td><td>frozen Wan video diffusion에 LoRA를 붙이고 RTV와 NCMV 두 표현으로 dense 3D point tracking을 생성하게 해 zero-shot 4개 benchmark에서 경쟁력을 보인 4D 표현 연구임</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2611.16213'>Visibility-Aware Task and Motion Planning with Task-Centric Perception</a></td><td>65</td><td>9</td><td>TAMP</td><td>visibility 인지 TAMP로 불확실 환경 long-horizon 조작을 계획함</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2611.17110'>SALA: Semantically Aligned Latent Actions Enable Dual-Axis Scaling of Embodied Foundation Models</a></td><td>65</td><td>9</td><td>VLA</td><td>semantic 정렬된 latent action으로 human 영상과 로봇 데이터를 함께 scaling함</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2611.16259'>Reconstruct What You Can: Distractor-free 4D Gaussian Splatting</a></td><td>64</td><td>6</td><td>3D Vision</td><td>4DGS에서 deformation field의 Jacobian 민감도 점수로 유효한 피사체 움직임과 일시적 occluder·그림자를 분리하는 ReCan-GS임. casual video 동적 재구성에 실용적임</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2611.16400'>FuGIBench: Evaluating Reliable Preparation in Streaming Video</a></td><td>64</td><td>6</td><td>Video</td><td>streaming video에서 대기, 되돌릴 수 있는 준비, 응답 중 하나를 고르는 FuGIBench로 미리 준비하는 보조 능력을 잼. 로봇 보조와 anticipation 설계에 참고됨</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2611.16424'>PhysCapBench: A Cross-Domain Benchmark for Physically Grounded Video Captioning</a></td><td>63</td><td>7</td><td>Video</td><td>물리 상호작용과 상태 전이를 담았는지 보는 cross-domain video captioning 벤치마크 PhysCapBench임. embodied demonstration 영상 supervision 품질 측정에 연결됨</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2611.14781'>Robust Task-Aware State Estimation from Pre-trained Perception</a></td><td>63</td><td>7</td><td>Embodied AI</td><td>VLM token 확률로 누적 확률이 임계 이상인 최소 상태 집합 MBS를 만들고 PRaVaSS로 다항 복잡도로 구하며 task planning의 하류 의사결정을 개선함, perception 불확실성을 planning에 넘기는 방식이라 TAMP와 failure 예방에 관련됨</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2611.16728'>EgoX: Egocentric Cross-Embodiment Manipulation with Embodiment Dreaming</a></td><td>62</td><td>9</td><td>Manipulation</td><td>embodiment dreaming으로 egocentric human 영상을 cross-embodiment 조작에 활용함</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2611.16020'>Imitating the Imperfect: Offline-to-Online Robust Imitation Learning from Heterogeneous Demonstrators</a></td><td>62</td><td>8</td><td>RL</td><td>질이 섞인 demonstration에서 demonstrator별 expertise와 optimality score를 학습해 online 개선하는 IL 방법임. 이론 보장이 있으나 평가가 continuous control benchmark뿐임</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2611.17321'>BrickFlow: Connectivity-Guided Brick Reconstruction</a></td><td>62</td><td>6</td><td>Manipulation</td><td>LEGO 부품 집합과 이미지에서 부품별 SE(3) pose를 flow model로 추정하고 test time에 analytic connectivity-field guidance로 연결성을 강제하는 조립 복원임, 이산 물리 제약이 조립 로봇 계획과 닿음</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2611.15602'>CoCode-World: Shared 3D Proxy Representation for Multi-Player World Models</a></td><td>62</td><td>5</td><td>World Model</td><td>2인 게임 영상 생성에서 공유 3D proxy로 구조 제어와 외관 합성을 분리해 시점 간 일관성을 확보하는 multi-player world model임</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2611.16450'>A Recipe for Physical Action Model Training</a></td><td>60</td><td>9</td><td>VLA</td><td>로봇 모델 용량과 demonstration 예산 배분을 conditional distribution 관점의 이론으로 다룸. 실증은 PushT 궤적 206개의 정보 기준 분석뿐이고 policy 학습은 하지 않는 분석임</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2611.16589'>STVLA: Spatial-aware and Temporal-memory forVision-Language-Action Models</a></td><td>60</td><td>9</td><td>VLA</td><td>공간 인지와 시간 memory를 결합한 VLA이나 모듈 추가 성격이 강함</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2611.15078'>CrowdMAPS: Crowdsourcing Multiple Actions per State for Real-World Imitation Learning</a></td><td>60</td><td>8</td><td>IL</td><td>crowdsourcing으로 state당 다중 action label을 증강하는 새 데이터 paradigm임</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2611.15093'>Decide Before You Move: Diffusion-Generated Search Reference for Zero-Shot Open-Vocabulary Object Navigation in Semi-Static Environments</a></td><td>60</td><td>8</td><td>Navigation</td><td>diffusion 생성 search reference로 semi-static 환경 zero-shot object navigation 수행함</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2611.14838'>Sophon: A Procedural Diagnostic for Spatial Reasoning in Vision-Language Models</a></td><td>60</td><td>6</td><td>Multimodal</td><td>점 구름 자극을 절차적으로 생성한 Sophon으로 VLM 공간 추론 실패를 probing과 LoRA로 중간층 routing 병목에 국한시킨 분석이며 embodied spatial reasoning 이해에 참고됨</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2611.15640'>MemInStream: Memorizing or Merely Recognizing? Rethinking Streaming Video Memory Evaluation</a></td><td>60</td><td>6</td><td>Video</td><td>streaming video 메모리 평가에서 시각 이해 실패와 망각을 분리해 재는 MemInStream 벤치마크임. robot memory 평가 설계에 참고할 만함</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2611.14955'>The Posterior-Prior Epistemic Gap: When World Model Imagination Fails to Carry Task-Relevant Signals</a></td><td>58</td><td>8</td><td>World Model</td><td>world model imagination이 task 신호를 잃는 posterior-prior gap 진단이나 single-seed 사례 연구임</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2611.15802'>RUMI: A Robotiq-Matched Universal Manipulation Interface for Robot Learning with Augmented Reality and Haptic Feedback</a></td><td>58</td><td>8</td><td>Manipulation</td><td>force 인지 UMI 데이터 수집 장치로 AR과 haptic feedback을 결합함</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2611.15974'>Video-Action Models for Data-Efficient Industrial Manipulation</a></td><td>58</td><td>8</td><td>Manipulation</td><td>video-action model로 산업 조작의 data efficiency를 높이는 시도임</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2611.16312'>Alloy: A Multi-Material Physics Engine for Robot Learning</a></td><td>58</td><td>7</td><td>Simulation</td><td>다중 재질 physics engine으로 로봇 학습용 simulator를 확장함</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2611.15437'>SteinPnP: Non-Parametric Uncertainty Quantification in the Perspective-N-Point Problem</a></td><td>58</td><td>6</td><td>3D Vision</td><td>Stein Variational Inference로 PnP의 6-DoF pose posterior를 입자 집합으로 추정하고 다중 hypothesis를 찾는 보정을 넣음. 로봇 pose 불확실성에 쓸 만함</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2611.16579'>ActWorld-JEPA: Action-Conditioned JEPA World Models Meet Latent Planning for End-to-End Autonomous Driving</a></td><td>58</td><td>6</td><td>World Model</td><td>action-conditioned JEPA world model로 후보 궤적의 잠재 미래를 예측하고 계획 품질을 상대 비교하는 ActWorld-JEPA임. 주행 한정이나 latent planning 구성이 world model 관점에서 관련됨</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2611.16840'>Kosmo-GFM: A Production-Ready Geometry Foundation Model</a></td><td>58</td><td>6</td><td>3D Vision</td><td>카메라, depth, 대응점, 동적 3D 점을 예측하는 geometry foundation model과 pose 최적화 PoseEngine을 묶어 3D/4D Gaussian Splatting 재구성 속도를 GLUEMAP의 약 20%로 줄인 시스템임</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2611.15744'>Latent Imagination for Parameterized Action Spaces</a></td><td>58</td><td>6</td><td>World Model</td><td>parameterized action MDP에서 world model 상상 속 학습과 counterfactual mode evaluation으로 sample efficiency를 높임. 7개 benchmark에서 model-free baseline 수준이고 계획형 대비 67배 빠르나 실로봇 평가는 없는 상태임</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2611.14815'>BirdDreams: Joint Perspective and BEV Video Generation for a Plausible, Reactive Driving World Model</a></td><td>58</td><td>5</td><td>World Model</td><td>perspective 영상과 BEV 영상을 두 video diffusion transformer로 함께 생성해 ego trajectory 제어를 높인 driving world model이나 로봇 조작이 아닌 주행 도메인임</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2611.17334'>Unbundling Multimodal Vision Encoding</a></td><td>58</td><td>5</td><td>Multimodal</td><td>멀티모달 LM의 vision encoder를 visual prior, 전용 vision 용량, pre-fusion 배치로 분리해 동일 데이터와 compute로 처음부터 학습 비교한 통제 실험이며 prior는 불필요하고 용량이 중요함을 보임</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2611.17068'>Discovering Effective Agent Memory Designs through Program Evolution</a></td><td>58</td><td>5</td><td>Embodied AI</td><td>program evolution으로 agent memory 프로그램 전체를 탐색해 LoCoMo에서 수작업 대비 최대 12% 정확도를 35% 비용으로 얻고 raw 대화 보존과 query 의도별 구성이라는 설계 원리를 밝힘, robot memory 설계에 참고할 만함</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2611.14942'>Emergent Vision-Shaped Thinking in Text-Only Reasoning through Multimodal Training</a></td><td>58</td><td>4</td><td>Multimodal</td><td>text-only 추론에서 vision-language 축을 inference에 ablate하면 BBH navigate가 27.6포인트 떨어지고 boolean 과제는 유지되는 이중 해리를 보임, 멀티모달 학습이 spatial 추론 표현을 바꾼다는 인과 증거임</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2611.17309'>Classical Energies Learn to Reason 1,000x Faster than Looped Models</a></td><td>58</td><td>2</td><td>Reasoning</td><td>CRAM은 Hopfield-Tank 에너지를 학습해 Sudoku-Extreme 99.996%, Maze-Unique 100%를 looped model보다 1,000배 이상 빠르게 풀며 추론 FLOPs도 282배 이상 적음. 에너지 하강 기반 추론은 참신하나 평가가 풀기 쉬운 퍼즐에 한정되어 일반화 근거는 약함</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2611.17297'>Goal Encoding in LLMs</a></td><td>57</td><td>4</td><td>Embodied AI</td><td>코딩 과제에서 소수 attention head가 다음 sub-goal을 인코딩하고 인과적으로 행동을 좌우함을 보이며 non-recurrent goal-seeking 설명을 개입 실험으로 검증함, agent의 goal representation 해석에 참고됨</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2611.17060'>Ropedia Xperience 2: A Gold Standard for Scaling Physical AI Environments and Behaviors</a></td><td>56</td><td>7</td><td>Embodied AI</td><td>3D scan 1,589개와 egocentric 영상 4,230개(131시간)를 공개하고 장면을 시뮬레이션 환경으로, 인간 동작을 whole-body 로봇 궤적으로 바꾸는 physical AI 데이터 파이프라인이나 policy 학습 결과는 초록에 없음</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2611.15459'>Fear of Memorizing Objects: End-to-End Zero-Shot Model-Based Object Detection</a></td><td>56</td><td>6</td><td>CV</td><td>template 정보를 초기에 주입하는 end-to-end transformer로 zero-shot model-based 물체 검출을 하는 FOMO임. 6D pose 조작 파이프라인의 앞단으로 유용함</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2611.14654'>Cleaning an Agent&#x27;s History Hurts When the World Still Holds the Error</a></td><td>56</td><td>6</td><td>Embodied AI</td><td>에이전트 이력을 정리할 때 세계에 오류가 남아 있으면 오히려 복구율이 낮아짐을 world state를 고정한 개입 실험으로 보임, 성공 receipt가 효과 부재 시 AppWorld 성공률을 45%에서 28%로 낮춤, failure recovery에서 이력과 세계 상태 정합성에 시사점이 큼</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2611.16010'>Iris-Z: Scaling One Generative Model Past Specialist Geometry Models</a></td><td>56</td><td>4</td><td>3D Vision</td><td>단일 generative 모델로 monocular depth 등 기하 과제를 통합해 specialist 모델을 넘으려는 Iris-Z임. scale-up 주장이 크나 로봇 직접 평가는 없음</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2611.15565'>Generalized Inverse Kinematics via Conditional Flow</a></td><td>55</td><td>8</td><td>Kinematics</td><td>conditional flow로 IK를 일반화한 생성적 접근임</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2611.15689'>What World Model Does Active Object Search Need? A Study under Imperfect Detection</a></td><td>55</td><td>8</td><td>Active Perception</td><td>불완전 검출 하 active object search에 필요한 world model을 비교 분석함</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2611.16439'>HALO: Human-Aligned Data Collection for WhoLe-body MObile Manipulation</a></td><td>55</td><td>8</td><td>Mobile Manip</td><td>인간 정렬 whole-body 모바일 조작 데이터 수집 시스템임</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2611.16645'>Rethinking Actions: Continuity-Aware Priors for World-Model Planning</a></td><td>55</td><td>8</td><td>World Model</td><td>행동 연속성 prior를 world model planning에 도입하는 아이디어임</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2611.15296'>APG-Planner: Learning Vision-Based High-Speed Trajectory Planning via Analytic Policy Gradient</a></td><td>55</td><td>7</td><td>Navigation</td><td>analytic policy gradient 기반 시각 고속 궤적 planner로 학습 효율을 개선함</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2611.15964'>COMBS: Concealed Object Multi-modal Bayesian Search</a></td><td>55</td><td>7</td><td>Active Perception</td><td>가려진 물체 탐색을 multimodal Bayesian search로 정식화함</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2611.16221'>BWM-Forge: Agentic World Programming for Embodied Intelligence</a></td><td>55</td><td>7</td><td>World Model</td><td>agentic world programming으로 제어 가능한 로봇 영상을 생성함</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2611.16056'>Sub-actions in Action: Text-Guided Hand-Role Alignment for Sub-Action Recognition</a></td><td>55</td><td>6</td><td>Video</td><td>egocentric 행동에서 좌우 손의 역할과 조작 물체를 인식하는 sub-action detection 과제와 BiScopeNet을 제안함. video-LLM 모듈 추가 형태이나 조작 이해에 연결됨</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2611.15079'>SAVE: Less is More in Agentic Video Reasoning</a></td><td>55</td><td>4</td><td>Video</td><td>agentic video reasoning 기법들을 Gemini 3 Flash와 Gemma 4에서 비용까지 통제해 비교하고, 최소 Active Exploration Baseline에서 출발한 SAVE가 6개 설정 중 5개에서 앞섬을 보인 평가 겸 방법 논문임</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2611.17240'>Objects as Addresses: Instance Binding in Vision Transformer Attention</a></td><td>55</td><td>4</td><td>CV</td><td>여덟 개 pretrained ViT에서 같은 객체 patch들이 공유하는 attention address를 찾아 query 성분 편집으로 attention을 다른 개체로 돌리는 object binding 해석 연구임, object-centric 표현에 시사점 있음</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2611.16816'>Outcome-Mass Alignment: Controlling Length-Dependent Trajectory Influence in Multi-Turn LLM Agent Reinforcement Learning</a></td><td>55</td><td>4</td><td>RL</td><td>multi-turn LLM agent GRPO에서 trajectory 확장으로 outcome 통계가 중복 집계되는 문제를 짚고 OMA로 보정해 ALFWorld 성공률을 7.0-9.4퍼센트포인트 올림, embodied agent RL에 적용 가능한 회계 관점임</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2611.15600'>MemCredit: From Relevance to Utility for Decision-Time Memory in Long-Horizon Web Agents</a></td><td>55</td><td>3</td><td>Agent Memory</td><td>MemCredit은 counterfactual intervention으로 개별 memory의 결정 기여도를 추정해 utility estimator로 증류하고 토큰 예산 안에서 memory를 고르며, ALFWorld에서 BM25 대비 SR@50을 올림. 의미 유사도 대신 결정 효용으로 고르는 원리는 robot memory에 참고할 만함</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2611.16913'>CADET: Construction of PCB Routing Instances with Executable Demonstrations</a></td><td>55</td><td>3</td><td>IL/RL</td><td>CADET는 EDA 엔진 행동으로 만든 합성 PCB 10만 장과 시연을 만들고 behavior cloning 뒤 RL로 fine-tuning해, 실제 보드의 DRV 없는 라우팅 성공률을 RL 단독 38.0%에서 67.2%로 올림. 시연 합성 후 BC+RL 파이프라인은 robot learning과 닮았으나 도메인이 PCB 배선임</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2611.16666'>Natural Gradient Learning in Predictive Coding through Lateral Circuits</a></td><td>55</td><td>2</td><td>LG</td><td>Natural PC는 predictive coding에 lateral circuit을 넣어 Fisher 정보 행렬의 역을 국소적으로 암묵 계산하는 natural gradient 학습이며, ImageNet 재구성에서 AdamW 기반 BP와 비슷한 성능을 더 낮은 비용으로 냄. 학습 이론으로 참신하나 분류 이외 과제와 로봇 연결은 검증되지 않음</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2611.17031'>Your Vision Foundation Model Is Secretly an EEG Foundation Model</a></td><td>55</td><td>2</td><td>Representation</td><td>SeeEEG는 EEG를 이미지로 렌더링해 frozen DINOv3 ViT를 쓰고 표시 파라미터 최대 1,113개만 학습하며, 8개 dataset 모두에서 EEG foundation model 7종보다 balanced accuracy가 높음. 무작위 초기화 ViT는 15.2점 낮아 시각 사전학습의 전이 효과를 보임. 표현 학습 관점에서 흥미로우나 로봇과는 간접적임</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2611.15766'>Prior-as-Skill: Remember Outside and Read Inside with On-Policy Self-Distillation for Self-Evolving VLM Agents</a></td><td>54</td><td>5</td><td>Embodied AI</td><td>self-evolving VLM agent의 skill을 on-policy self-distillation으로 내재화하되 프레임 누락·순서 변경에 견디게 함. skill memory 관점은 흥미로우나 로봇 실험은 없음</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2611.15659'>GraSLA: A Lightweight Spatial-Language-Action Model with Grasp Hypotheses as Geometric Priors</a></td><td>52</td><td>8</td><td>VLA</td><td>grasp hypothesis를 geometric prior로 쓰는 경량 spatial-language-action 모델임</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2611.15937'>MOSAIC: Modular Obstacle and Spatial-Aware Framework for Manipulation In Cluttered Scenes</a></td><td>52</td><td>8</td><td>VLA</td><td>3D 장애물 인지 모듈로 cluttered 장면 VLA 조작을 보강하는 모듈형 구성임</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2611.17159'>Inner Product Regularization for Imitation Learning</a></td><td>52</td><td>8</td><td>IL</td><td>inner product 정규화로 imitation learning 외삽을 개선하는 기법임</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2611.15277'>DroneDiffusion: Uncertainty-Guided Diffusion Path Planner for UAV Navigation</a></td><td>52</td><td>7</td><td>Navigation</td><td>불확실성 안내 diffusion UAV planner로 failure zone 회피함</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2611.16246'>What Can a VLA Learn from the Agent That Calls It? Task-Level Experience Distillation for Embodied Navigation</a></td><td>52</td><td>7</td><td>Navigation</td><td>LLM이 호출하는 VLA에 task-level experience를 distill하는 navigation 연구임</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2611.16419'>I See What You Want: Decoding Hierarchical Operator Intent from Visual Teleoperation History</a></td><td>52</td><td>7</td><td>HRI</td><td>teleoperation 시각 이력에서 계층적 operator 의도를 해석함</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2611.17142'>FORGE: Force-Aware Multi-Granularity Control for Efficient Humanoid Loco-Manipulation</a></td><td>52</td><td>7</td><td>Humanoid</td><td>force 인지 multi-granularity 제어 humanoid loco-manipulation임</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2611.17330'>ProtoVis-Nav: Prototypical Visual Imagination for Visual-Spatial Aligned UAV Navigation</a></td><td>52</td><td>7</td><td>VLN</td><td>prototype 시각 상상으로 UAV VLN의 공간 정렬을 개선함</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2611.16590'>AstroMemBench: A Benchmark for Memory Systems in Embodied Spacecraft Agents</a></td><td>52</td><td>6</td><td>Embodied AI</td><td>AstroMemBench는 행성 표면, 궤도 정비, 심우주 과제 9개에서 memory 하위 과제 16종을 2,240개 인스턴스로 시험하는 우주선 embodied agent용 benchmark임. 재시작 후 Mem0가 RAG보다 12.25점 높다는 비교를 보였으나 결정론적 환경이고 benchmark 기여 위주임</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2611.15435'>ThermalSplat: Generalizable Pose-Free Gaussian Splatting for Sparse-View Thermal 3D Reconstruction</a></td><td>52</td><td>5</td><td>3D Vision</td><td>열화상 sparse-view에서 pose-free feed-forward 3DGS 재구성을 하는 ThermalSplat을 제안함. 수색구조·주행 응용이 있으나 증분적 확장임</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2611.16727'>From Foundation VLM to Versatile Driving VLM: A Triplet Incremental Training Approach</a></td><td>52</td><td>5</td><td>Multimodal</td><td>일반 VLM에 image, depth, QA triplet과 frozen twin KL distillation을 써서 3D 기하 인식을 넣고 추론 시 depth 분기를 버리는 자율주행 VLM 적응법임</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2611.14763'>RECALL: Real-Time Recalibration of Multi-Camera Rigs via Learned OEM-Anchored Residuals</a></td><td>52</td><td>4</td><td>3D Vision</td><td>OEM 보정값을 anchor로 삼아 multi-camera rig의 intrinsics와 extrinsics를 feed-forward로 0.12ms에 재보정하며 bundle adjustment보다 정확함을 보인 방법임</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2611.15844'>Open Vision Banana: A Fully Open Recipe for Generative Visual Perception</a></td><td>52</td><td>4</td><td>CV</td><td>Vision Banana를 재현하는 공개 recipe로, 사전학습 생성 모델을 조건부 편집 형태의 다중 과제 perception 모델로 바꿈. 설계 선택 분석이 유용하나 로봇 직접성은 낮음</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2611.16452'>Can an LVLM Perceive Event Boundaries Like a Human?</a></td><td>52</td><td>4</td><td>Video</td><td>LVLM이 사람처럼 이벤트 경계를 인식하는지 GEBD로 분석함. 직접 예측은 경계를 놓치고 비지도 후보 정제는 잘함. video 이해 분석으로 task segmentation에 참고됨</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2611.15039'>Back to the Question: Tracing Visual Distraction Through Text Tokens</a></td><td>52</td><td>3</td><td>Multimodal</td><td>VLM이 distractor 이미지에 흔들리는 경로를 중간층 distractor-to-text attention knockout으로 찾고 answer consistency 정규화로 16퍼센트포인트 올린 기전 분석임</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2611.17331'>TTB: Test-time Baking for Efficient Rendering of Decoder-only View Synthesis Models</a></td><td>52</td><td>3</td><td>3D Vision</td><td>decoder-only view synthesis에서 cross-view attention 매핑을 경량 MLP로 학습해 구워 넣는 Test-Time Baking으로 렌더링을 최대 23배 빠르게 하며 품질은 SOTA와 비슷함</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2611.16321'>From Large Language Models to Efficient System One Models via Adaptive Computation</a></td><td>52</td><td>3</td><td>LG</td><td>decision model에서 최종 6개 layer를 빼도 손실이 없음을 보이고 self-distillation prefix sub-model과 exit gate로 adaptive depth를 구현함, 로봇 policy의 efficient inference에 응용 여지 있음</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2611.15178'>HyperSkill: Training-Free Omnimodal GRPO via Hypergraph-Indexed Skill-Library Evolution</a></td><td>52</td><td>3</td><td>Multimodal</td><td>backbone을 고정하고 counterfactual로 검증한 skill을 hypergraph 색인 라이브러리에 넣는 training-free GRPO HyperSkill이며 11개 벤치마크에서 평균 F1 13.0포인트 앞섬, 실패에서 protocol skill을 학습하는 점이 skill memory와 닿음</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2611.15835'>Controlling the Probability of Unknown Unknowns in Pre-Deployment Testing of AI Systems</a></td><td>52</td><td>3</td><td>LG</td><td>anytime-valid 상한 신뢰 sequence로 아직 보지 못한 failure mode가 나올 확률을 인증하는 알고리즘이며, Good-Turing 기반 baseline보다 tight한 bound를 보임. failure 발견의 중단 시점을 정하는 이론이라 로봇 배포 전 테스트에 응용 여지가 있으나 실험은 coding agent trace뿐임</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2611.16961'>The Value of Thinking: Learning When to Reason in Hybrid Decision Models</a></td><td>52</td><td>2</td><td>Efficient Inference</td><td>hybrid decision model은 forward pass 한 번의 암묵 추론으로 답하거나 T 토큰의 명시 추론을 쓸지 &#x27;thinking의 가치&#x27;를 추정하는 routing block으로 정하고, 에피소드 반환으로 이를 학습하는 CDPO를 제안함. MiniWoB에서 토큰 비용을 80.1% 줄임. 추론 시점 연산 배분 원리는 efficient inference 관점에서 참고할 만함</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2611.15381'>Low-Cost Mobile Bimanual Manipulation for Long-Horizon Toilet Cleaning</a></td><td>50</td><td>8</td><td>VLA</td><td>저비용 mobile bimanual로 화장실 청소 long-horizon을 VLA로 수행한 시스템임</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2611.15650'>Single-View RGB-D Force--Deformation Estimation for Robotic Manipulation of Elasto-Plastic Materials</a></td><td>50</td><td>7</td><td>Manipulation</td><td>단일 RGB-D로 elasto-plastic 재료 force-deformation을 추정함</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2611.15981'>DexRemo: A Force-Sensing Hand Platform and Task Suite for Contact-Rich Removal Manipulation</a></td><td>50</td><td>7</td><td>Manipulation</td><td>force 센싱 hand 플랫폼과 접촉 제거 조작 task suite임</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2611.16188'>PERA: Plug-in Experts for Robotic Actions in Continual Whole-Body Control</a></td><td>50</td><td>7</td><td>Humanoid</td><td>plug-in expert로 continual whole-body control의 forgetting을 줄임</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2611.16346'>MotionSkill: From Bipedal Motion Video to Control across Embodiments</a></td><td>50</td><td>7</td><td>Locomotion</td><td>이족 보행 영상에서 embodiment 간 제어로 옮기는 MotionSkill임</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2611.16423'>VOKE: Visual Object Kinematics Estimator for Dexterous In-Hand Manipulation</a></td><td>50</td><td>7</td><td>Dexterous</td><td>in-hand 조작용 물체 kinematics 시각 추정기임</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2611.16671'>NSDL: Neuro-Symbolic Division of Labor for Multi-Robot Task Planning</a></td><td>50</td><td>7</td><td>Task Planning</td><td>neuro-symbolic 분업으로 multi-robot task planning을 수행함</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2611.16872'>ACE-CaP-0: Real-World Code-as-Policies in the Era of Experience</a></td><td>50</td><td>7</td><td>Agent</td><td>경험 기반 code-as-policies 실로봇 적용으로 agent harness 의존임</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2611.14895'>HeadIO: Body-Frame Heading Decomposition for Neural Inertial Odometry on Head-Mounted Devices</a></td><td>50</td><td>6</td><td>Embodied AI</td><td>머리 착용 기기용 IMU odometry에서 tilt 성분만 쓰는 body-frame 분해와 bidirectional Mamba로 EqNIO 대비 FLOPs 3배 절감하며 RTE를 낮춘 방법임</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2611.15692'>CGOcc: Learning Cross-Gaussian Dependencies for 3D Semantic Occupancy Prediction</a></td><td>50</td><td>6</td><td>3D Vision</td><td>Gaussian 기반 occupancy 예측에서 겹치는 primitive 간 cross-Gaussian 의존성을 모델링해 voxel 분류를 개선함. 주행 occupancy 벤치마크 중심 증분임</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2611.16162'>GOOSELoc: A Multimodal Benchmark for Ground-to-Aerial Localization in Unstructured Off-Road Terrain</a></td><td>50</td><td>6</td><td>Navigation</td><td>숲 등 비정형 off-road에서 지상 센서와 항공 영상을 맞춰 pose를 추정하는 GOOSELoc 벤치마크임. GNSS 불가 환경 localization 평가용 데이터 기여임</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2611.17318'>Spatial Foundry: A Multimodal Dataset for Spatial Intelligence</a></td><td>50</td><td>6</td><td>Embodied AI</td><td>가구가 배치된 주거 3D 장면 5,280개에 RGB, depth, 점군, 3D box, 카메라 궤적을 정렬한 Spatial Foundry 데이터셋이며 world model과 장면 편집 연구에 쓸 수 있으나 방법 검증은 없음</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2611.14599'>StructRL: Model-Free Reinforcement Learning with Replay Graphs</a></td><td>50</td><td>6</td><td>RL</td><td>경험을 replay graph로 만들고 동적계획법 경로를 DQN 행동 선호와 SAC 목표 방향으로 전이해 sparse reward MiniGrid 성공률을 0.10에서 0.90 등으로 올리나 장난감급 환경에서만 검증됨</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2611.15153'>MatrixSplat: Matrix-Parallel and Feature-Scalable 3D Gaussian Splatting Rendering on GPUs</a></td><td>50</td><td>5</td><td>3D Vision</td><td>3DGS feature 렌더링의 순서 의존을 order-independent 가중 누적으로 바꿔 Tensor Core 행렬 연산에 올린 MatrixSplat으로 고차원 feature 렌더링 커널을 최대 36.7배 줄임</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2611.15216'>Where is My Mug? Training-Free Framework for Personalized Image Segmentation</a></td><td>50</td><td>5</td><td>CV</td><td>같은 범주 look-alike가 섞인 장면에서 기존 PIS가 proposal recall 때문에 무너짐을 보이고, class-agnostic detector, BLIP-2 매칭, top-K Sinkhorn, SAM으로 최대 약 48 mIoU를 올린 training-free 파이프라인임</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2611.15315'>MIGRO: A Decoupled and Portable Long-Term Memory System for Language Models</a></td><td>50</td><td>5</td><td>LG</td><td>관찰은 정확히 보존하고 색인은 근사로 구성하며 질문이 정해진 뒤에 선택하는 비대칭 충실도의 장기 memory MIGRO이며 LoCoMo에서 7.3% 높고 private memory 99.3% 절감함, robot memory 설계 원리로 참고됨</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2611.16217'>WorldDraft: If Code Builds the World, Can Video Models Just Render It?</a></td><td>50</td><td>4</td><td>World Model</td><td>코드로 만든 4D 세계를 video model이 렌더만 할 수 있는지 world preservation과 visual realization으로 평가함. 코드 기반 world 구성과 생성 렌더러 분리라는 틀이 눈에 띔</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2611.17048'>AURA 2.0: From User-Driven Responses to Model-Initiated Conversations in Streaming Video</a></td><td>50</td><td>4</td><td>Video</td><td>streaming video LLM이 사용자 질의 없이 먼저 대화를 시작하는 Model-Initiated Conversation, tool call, grounding, 장기 interaction memory를 더한 AURA 2.0이며 embodied 상호작용과 닿음</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2611.15069'>DiFiT: Distribution-Fidelity-guided Visual Token Pruning for Multimodal Large Language Models</a></td><td>50</td><td>3</td><td>Multimodal</td><td>MLLM visual token pruning을 응답 분포 보존 관점에서 Dual-View Distillation과 differentiable Top-K로 학습하며 30% 유지에서 MME 98.74%를 보존함</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2611.17324'>K2V: Generative Keyframing For Physically Plausible Video Generation</a></td><td>50</td><td>3</td><td>Video</td><td>언어 모델이 물리 추론을 맡아 keyframe을 만들고 video 모델은 그 사이 보간만 하게 해 Physics-IQ Verified와 PhyGenBench에서 SOTA를 낸 물리 일관 영상 생성임</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2611.15276'>Verify by Doing: Co-Evolving Agent Execution and Evaluation without External Feedback</a></td><td>50</td><td>3</td><td>LG</td><td>가중치를 고정한 채 Actor와 Evaluator 하네스를 함께 진화시키고 Evaluator가 도구로 환경 상태를 직접 검사해 외부 피드백 없이 성공 여부를 판정함, 개선폭은 2.3-4.1포인트로 작으나 self-verification 설계가 failure detection에 연결됨</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2611.16466'>How Should Planning Agents ReSHAPE Their Search Space?</a></td><td>50</td><td>3</td><td>Planning</td><td>ReSHAPE는 사용자 요청 specification을 고정하지 않고 search space를 수정하는 과제를 정식화하고, 계획안을 보여 주는 방식이 질문하는 방식보다 F1이 9.7점 높음을 보임. 계획 에이전트의 요구 재구성 관점은 language feedback 기반 planning과 이어지나 여행, 쇼핑 도메인임</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2611.17167'>Actor, Judge, or Teacher? Understanding Decision Models in Long-Horizon Agents</a></td><td>50</td><td>3</td><td>RL</td><td>decision model JEV가 actor로는 약해도 행동 이후 결과를 보는 teacher로는 강하다는 분석이며, Qwen2.5-1.5B policy의 ALFWorld 성공률을 GRPO 72.8%에서 82.9%로 올림. 에피소드 종료 후 행동 단위 판단으로 credit을 주는 관점이 embodied RL과 이어짐</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2611.16882'>Pretraining Data Statistics Shape the Phases of Learning Entity Comparison in Language Models</a></td><td>50</td><td>2</td><td>LG</td><td>entity 비교 과제에서 frequency, position, 정답 선택의 세 학습 단계가 pretraining 데이터 통계로 인과 결정됨을 소형 LM 통제 실험과 OLMo-2 32B로 보임, 학습 dynamics 이해에 유용하나 로봇과 직접 연결은 약함</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2611.14969'>Scaling VLA Serving Under Robotic Execution Constraints</a></td><td>48</td><td>7</td><td>VLA</td><td>VLA fleet serving 시스템 보고로 실용적이나 방법론 novelty는 작음</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2611.15117'>PolyMorphWBC: Whole-Body Control from End-Effector Trajectories for Quadrupedal Mobile Manipulation across Arm Morphologies with Extended Reach</a></td><td>48</td><td>7</td><td>Mobile Manip</td><td>다양한 arm 형태의 quadruped whole-body control로 엔지니어링 중심임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2611.16282'>Robot Navigation and Obstacle Avoidance from Randomly Positioned External Cameras</a></td><td>48</td><td>7</td><td>Navigation</td><td>무작위 배치 외부 카메라로 로봇 항법을 수행하는 설정임</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2611.16632'>Reins: Frontier Multimodal Models Driving Real Robot Arms on Long-Horizon Tasks, Zero-Shot</a></td><td>48</td><td>7</td><td>Agent</td><td>frontier 모델이 실로봇 arm을 zero-shot 구동하는 평가 시연임</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2611.17160'>XBot-Omni: An Omni-Modal Model for Embodied Understanding and Interaction</a></td><td>48</td><td>7</td><td>Multimodal</td><td>embodied 상호작용용 omni-modal 모델로 규모 중심 접근임</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2611.17163'>UAV-Flow++: A Unified Suite for Benchmarking and Learning Language-Guided UAV Flight</a></td><td>48</td><td>7</td><td>Navigation</td><td>UAV 언어 유도 비행 benchmark와 학습 suite임</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2611.17238'>HEIR: Harness Egocentric Intent for Human-Robot Interactions</a></td><td>48</td><td>7</td><td>HRI</td><td>egocentric 의도를 활용한 human-robot 상호작용 틀임</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2611.15680'>SpaceMCP: Vision Language Model Spatial Reasoning via Model Context Protocol</a></td><td>48</td><td>6</td><td>Multimodal</td><td>feed-forward 3D 복원과 open-vocabulary segmentation으로 만든 scene graph를 VLM이 function call로 질의함. 학습 없이 VSI-Bench 등에서 base VLM을 15~22점 올린 spatial reasoning 방법이며 로봇 평가는 없는 상태임</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2611.15339'>Interactive Perception of Granular Materials via Robotic Scooping and Force-Torque Sensing</a></td><td>48</td><td>6</td><td>Manipulation</td><td>granular 물질 scooping과 FT 센싱 기반 interactive perception임</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2611.16422'>BlinkMimic: Training a Humanoid Motion Tracker in Minutes on a Single GPU</a></td><td>48</td><td>6</td><td>Humanoid</td><td>단일 GPU에서 수 분 만에 humanoid tracker를 학습하는 효율화임</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2611.16339'>Hand in Silhouette: Synthetic-to-Real Multi-View Hand Reconstruction via Binary Masks</a></td><td>48</td><td>5</td><td>3D Vision</td><td>binary mask만 입력으로 써서 synthetic에서 real로 넘어가는 다중 시점 손 재구성 SilHand임. 외관 격차를 피한 설계이나 손 재구성 한정임</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2611.16583'>ReFineR: Single image to dense point cloud registration at pixel level with point splatting</a></td><td>48</td><td>5</td><td>3D Vision</td><td>LiDAR 점군과 단일 이미지의 카메라 pose를 point splatting 미분 렌더링과 GOM 손실로 픽셀 단위까지 보정하는 offline 방법이며, 로봇 센서 보정 오차에 쓸모 있으나 응용 범위가 좁음</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2611.15143'>Multi-View 3D Reconstruction Using V-JEPA Features</a></td><td>48</td><td>4</td><td>3D Vision</td><td>V-JEPA 특징으로 RGB 다시점 3D 복원을 시도하고 CO3D에서 카메라 회귀 구성별 오차 상충을 정직하게 보인 분석이나 identity pose나 상수 깊이보다 못한 항목이 있어 성능 근거가 약함</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2611.15059'>Test-Time Selective Adaptation for Cross-Modal UAV Object Tracking with Token Shift</a></td><td>48</td><td>3</td><td>CV</td><td>UAV cross-modal 추적에 token shift와 시간 역방향 예측 보조 과제로 test-time adaptation을 하고 신뢰도 gating을 둔 방법이며 도메인이 좁음</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2611.15569'>TraceKV: Policy-Preserving Low-Rank KV Cache Compression for Reasoning Vision-Language Models</a></td><td>48</td><td>3</td><td>Multimodal</td><td>reasoning VLM의 low-rank KV cache 압축에서 on-policy 상태와 calibration 불일치로 생기는 policy drift를 줄임. efficient inference 방법이나 로봇 직접성은 낮음</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2611.16748'>PhysLoop: Harnessing LLMs&#x27; Physics Awareness for Self-Improving Video Generation Models</a></td><td>48</td><td>3</td><td>Video</td><td>LLM이 물리 지식으로 영상 생성, 선택, 수리를 이끌어 video generation 모델을 self-improve시키는 PhysLoop이며 100K 영상을 공개함, 물리 일관성은 world model과 닿음</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2611.17320'>Learning When Diffusion Language Models Should Regenerate</a></td><td>48</td><td>3</td><td>LG</td><td>diffusion LM의 hidden state에 오류 정보가 있다는 진단에서 출발해 verifier DiVR이 블록 재생성 시점과 대안을 고르게 함, LLaDA-8B 평균 정확도 35.3%에서 43.4%로 오름, test-time verification 관점에서 참고됨</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2611.15729'>DISCERN: Preserve at Write, Resolve at Read for Persistent LLM-Agent Memory</a></td><td>48</td><td>3</td><td>Agent Memory</td><td>DISCERN은 쓰기 시점에 bi-temporal provenance graph를 덧붙이기만 하고 읽기 시점에 graph를 탐색해 답변 또는 abstain을 결정하는 agent memory 구조이며, 자체 합성 benchmark ENT-310에서 abstention F1이 baseline보다 높음. 엔터프라이즈 대화 도메인이고 실험이 자체 benchmark 중심임</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2611.16126'>Split-and-scale Latent 3D Representations</a></td><td>47</td><td>3</td><td>3D Vision</td><td>latent 3D 표현을 분할하고 추론 때 latent 수를 늘려 세부를 살리는 split-and-scale 방식임. 형상 생성 품질 개선이고 로봇 연결은 약함</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2611.15968'>DuoJEPA: Cross-Modal Translation Between Unaligned Self-Supervised Embedding Spaces</a></td><td>46</td><td>3</td><td>LG</td><td>LeJEPA로 모달리티별 encoder를 따로 학습하고 transformer 한 층으로 상대 임베딩 공간으로 번역하는 DuoJEPA임. 정렬 없는 cross-modal 표현 학습 아이디어이나 검색·분류 평가임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2611.16402'>Teach with Blinks: Breaking Linguistic Momentum in On-Policy Distillation for Fine-Grained Multimodal Perception</a></td><td>46</td><td>3</td><td>Multimodal</td><td>on-policy distillation에서 teacher가 매 token마다 접두를 두 번 읽어 linguistic momentum을 끊는 BlinkOPD임. fine-grained 지각 post-training 개선임</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2611.17323'>AgentSSL: Can MLE Agents Leverage Unlabeled Data?</a></td><td>46</td><td>2</td><td>Semi-supervised</td><td>AgentSSL은 semi-supervised learning을 program search로 보고 agent가 만든 코드가 12개 설정 중 8개에서 사람 baseline을 넘는 것을 보임. 선택 기준이 agent 피드백일 때 성능이 최대 47% 떨어지는 병목을 ProgramSelectBench로 분석함. 자동 연구 agent 관점은 흥미로우나 로봇과는 간접적임</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2611.15589'>EMS-Nav: Embodied Multi-Scale Navigation</a></td><td>45</td><td>7</td><td>Navigation</td><td>산업 점검용 multi-scale embodied navigation 시스템임</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2611.16374'>ManiLadder: Benchmarking Robot Manipulation Through a Categorized and Multi-Difficulty Level Task Ladder</a></td><td>45</td><td>7</td><td>Benchmark</td><td>난이도별 조작 benchmark ladder로 평가 도구 기여임</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2611.14981'>From a Single RGB Image to Robot Execution: Metric Scene Alignment and Contact-Guided Retargeting</a></td><td>45</td><td>6</td><td>Humanoid</td><td>단일 RGB 장면 복원과 contact 기반 retargeting 파이프라인으로 엔지니어링 중심임</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2611.15280'>Autonomous Trail Racing with a Bicycle Robot</a></td><td>45</td><td>6</td><td>Locomotion</td><td>bicycle robot 트레일 레이싱 시스템으로 시연 중심임</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2611.16877'>Informative Path Planning with Gaussian Processes: Error Bounds, Algorithms, and Benchmarks</a></td><td>45</td><td>6</td><td>Active Perception</td><td>GP 기반 informative path planning의 오차 한계와 benchmark를 제시함</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2611.14903'>Epigraph Form Reinforcement Learning-based Safe Trajectory Tracking Control for Connected and Autonomous Vehicles</a></td><td>45</td><td>5</td><td>RL</td><td>epigraph form RL로 Lagrangian RL의 학습 불안정을 줄인 자율주행 안전 trajectory tracking 방법임. Vehicle-in-the-Loop 실험이 있으나 기존 기법 적용 범위임</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2611.15225'>Can MLLMs Reason over Surround-View Driving Videos? A Multi-View Autonomous Driving QA Benchmark</a></td><td>45</td><td>5</td><td>Embodied AI</td><td>surround-view 주행 영상에 12개 범주 QA를 붙인 MVDriveBench로 23개 MLLM을 평가하고 AlpaSim closed-loop 성능과 상관을 보임, 벤치마크 기여이며 주행 도메인임</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2611.15360'>CARE-Drive: Coupled Alternating Refinement for Ego-trajectories</a></td><td>45</td><td>4</td><td>VLA</td><td>자율주행 VLA의 궤적 refinement에서 position과 heading을 번갈아 정제하는 구조를 제안함. 물리량 분리는 참신하나 주행 한정 증분임</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2611.16861'>Visual Cipher Bench: Benchmarking LLM Agents on Long-Horizon Visual Reasoning</a></td><td>45</td><td>4</td><td>Multimodal</td><td>이미지에서만 규칙을 찾아야 하는 시각 퍼즐 40개로 agent의 long-horizon 시각 추론을 평가하며 최고 정확도 26.7%이고 힌트 하나로 7.8%에서 55.6%로 오름을 보임</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2611.17336'>Back to Pixels: Lifting Latent Video Diffusion into Pixel Space</a></td><td>45</td><td>3</td><td>Video</td><td>latent video diffusion의 VAE decoder를 convolutional head로 바꿔 Wan2.1-14B를 pixel 공간 생성으로 끌어올리는 PixVid이며 프레임 단위 action 반응이 가능해 interactive world model에 쓸 수 있음</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2611.15507'>ReShap: Interpretable Reinforcement Learning for High-Dimensional Multi-Action Settings</a></td><td>45</td><td>3</td><td>RL</td><td>고차원 이미지 입력 multi-action RL policy를 SHAP 기반 해석 surrogate로 distillation함. Atari와 Box2D만 평가해 로봇 적용은 불명함</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2611.16639'>Asymmetric Multimodal Learning with Decomposed JEPAs</a></td><td>45</td><td>3</td><td>Multimodal</td><td>alignment만으로는 modality 고유 정보가 사라진다는 bound를 증명하고 shared와 private latent를 나눈 D-JEPA를 제안함. VQA 중심 평가이며 로봇 검증은 없는 상태임</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2611.16627'>Folio: Recoverable Multi-Resolution Context Folding for Long-Horizon Language Agents</a></td><td>45</td><td>3</td><td>LLM Agent</td><td>Folio는 장기 agent 기록을 turn note, event manifest, 원본 기록의 세 단계로 남기고 오래된 turn을 거친 단계로 프로그램적으로 접으며 handle로 복구하는 context manager임. LOCA-bench 75개 중 66개를 풀어 모델 요약 방식의 54개를 넘음. long-horizon memory 관리 아이디어는 참고할 만하나 언어 agent 대상임</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2611.16981'>Compiling Known Rules into Compact Neural Agents: Weight-Space Programming on Unseen Games</a></td><td>45</td><td>3</td><td>Agent</td><td>언어모델이 게임 규칙 소스를 읽고 57k 파라미터 recurrent 네트워크 weight를 직접 작성해, 보지 못한 level에서 최대 56% 성공을 얻음. Python player보다 못하고 PPO fine-tuning을 거치면 성능이 사라져 한계가 뚜렷함. 규칙을 policy로 컴파일하는 발상은 신선하나 실용성은 입증되지 않음</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2611.14686'>What Entropy-Based View Selection Cannot See: An Audit of Test-Time Adaptation for Vision-Language Models</a></td><td>45</td><td>2</td><td>Multimodal</td><td>CLIP test-time adaptation에서 이득이 gradient 갱신이 아니라 view 선택에서 나옴을 보이고, entropy 대신 crop 비율로 view를 고르면 15개 중 14개에서 좋아짐을 보인 분석 연구임</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2611.15100'>Keep Images in Sight: Visual Position Re-Anchoring for Long-Context MLLMs</a></td><td>45</td><td>2</td><td>Multimodal</td><td>long-context MLLM에서 KV cache의 이미지 key rotary phase를 짧은 문맥 기준으로 되돌리는 training-free VPR로 100개 점수 중 97개를 올림</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2611.14912'>Rethinking &quot;RL Generalizes, SFT Memorizes&quot;: The Role of SFT Data</a></td><td>45</td><td>1</td><td>NLP</td><td>RL이 일반화하고 SFT가 암기한다는 통념을 SFT 데이터 관점에서 재검토함. LLM 한정임</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2611.16356'>DIAGNO: Diagonal Spherical Neural Operators for Heterogeneous Earth Dynamics Modeling</a></td><td>45</td><td>1</td><td>Scientific ML</td><td>DIAGNO는 rotation equivariance 가정을 버리고 구면 spectral 모드 간 상호작용 kernel을 명시적으로 두는 spherical neural operator이며 지구 시스템 예측에서 SOTA를 보임. 기상 예측 도메인이라 로봇과 거리가 멂</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2611.14766'>Rational Use of Time for Social Coordination in Humans and AI</a></td><td>44</td><td>4</td><td>Embodied AI</td><td>The Mind 카드 게임에서 침묵 시간만으로 협력하는 150명 인간과 CUA, LLM을 비교해 모델은 파트너 적응이 약함을 보임, implicit signal 해석은 human-robot coordination에 연결됨</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2611.15448'>Semantic Consistency of Vision Tokens: A Vision-Centric Perspective on Multimodal Large Language Models</a></td><td>44</td><td>3</td><td>Multimodal</td><td>MLLM의 vision token 의미 일관성을 분석하고 self-supervised encoder 도입 가능성을 보는 분석 논문임. vision-centric 과제 개선 중심임</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2611.16517'>UniSpark: Exploring Hybrid Attention for Multimodal Understanding and Generation</a></td><td>44</td><td>2</td><td>Multimodal</td><td>full attention과 GatedDeltaNet linear attention을 섞은 9B Mixture-of-Transformer-Experts 통합 이해·생성 모델 UniSpark임. 구조 탐색이고 로봇 평가 없음</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2611.17316'>CoReMem: Cost-Internalizing Memory for Successive Coding Tasks with Prospective Valuation</a></td><td>44</td><td>2</td><td>Agent Memory</td><td>CoReMem은 다음 과제에 대한 측정된 memory 가치로 memory를 설계하고, 에피소드 segment를 넣고 뺀 실행을 비교해 anchor 중심의 compact memory를 만듦. ChainSWE에서 27B actor 해결률을 21.0%에서 25.7%로 올림. memory 효용 평가의 counterfactual 구성은 참고할 만하나 coding agent 한정임</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2611.16502'>SignRot: LLM Quantization with Massive Outlier-Aware Sign-Adjusted Rotation</a></td><td>44</td><td>1</td><td>Efficiency</td><td>SignRot은 massive outlier 채널을 찾아 Hadamard 행의 부호를 맞춰 bimodal 분포를 unimodal로 만들고 비대칭 activation 양자화와 묶는 LLM 양자화법이며, QuaRot에 붙여 LLaMA3-70B에서 SpinQuant를 넘음. 완성도 높은 drop-in 개선이나 로봇 직접 관련은 약함</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2611.14985'>ILA: A Transferable Interface-Level Adapter for Compliant Humanoid Motion Tracking</a></td><td>42</td><td>6</td><td>Humanoid</td><td>humanoid compliant tracking용 interface-level adapter로 작은 모듈 추가 성격임</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2611.15020'>Genie Sim Benchmark: Real-to-Sim Fidelity and Evaluation</a></td><td>42</td><td>6</td><td>Benchmark</td><td>Genie Sim의 real-sim 상관 평가 보고로 benchmark 검증 성격임</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2611.15658'>Embedded Sim-to-Real Visual Servoing: Learned Reaching and Force-Guided Placement</a></td><td>42</td><td>6</td><td>Visuomotor</td><td>임베디드 sim-to-real visual servoing 시스템으로 incremental임</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2611.15781'>Prediction-Error-Tightened MPC for Socially Compliant Crowd Navigation</a></td><td>42</td><td>6</td><td>Social Nav</td><td>예측 오차 반영 MPC로 군중 항법을 개선하는 incremental 기법임</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2611.16337'>Memory-Efficient Parallel Policy Learning for Collapse-Reactive Retreat via Hybrid Terrain Modeling</a></td><td>42</td><td>6</td><td>RL</td><td>붕괴 지형 후퇴용 메모리 효율 병렬 정책 학습으로 응용 중심임</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2611.14953'>RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence</a></td><td>42</td><td>5</td><td>Embodied AI</td><td>실제 UAV 영상을 주기적으로 추가해 항공 공간 지능을 평가하는 continually evolving VLM benchmark이며 30개 모델을 평가했으나 dataset 중심 기여임</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2611.15488'>FloCOS: Predicting Compact Forward Occupancy Sets of Surrounding Vehicles via Conditional Flow Matching</a></td><td>42</td><td>5</td><td>Driving</td><td>conditional flow matching으로 주변 차량 occupancy set을 예측하나 응용 중심임</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2611.16218'>A Coupled Control Barrier Function Approach to Deadlock-Free Multi-Robot Conflict Resolution</a></td><td>42</td><td>5</td><td>Multi-Robot</td><td>coupled CBF로 multi-robot deadlock 해소하는 제어 기법임</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2611.15777'>SO-Arena: Benchmarking the Capability Spectrum and Reliability of System One Models</a></td><td>42</td><td>5</td><td>Embodied AI</td><td>System One 모델의 능력과 신뢰성 benchmark로 로봇 정책 평가와 연결됨</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2611.15579'>FoveaDet: Software-Hardware Co-Design of Foveated CNN-Transformer for Object Detection</a></td><td>42</td><td>4</td><td>CV</td><td>시선 고정점 예측과 ViT patch pruning을 하드웨어와 함께 설계한 foveated 검출기 FoveaDet임. 엣지 로봇 효율에 쓸 수 있으나 검출 한정임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2611.15789'>VibePrevisBench: Evaluating Agentic Coding for 4D Scene Generation in Blender</a></td><td>42</td><td>3</td><td>Embodied AI</td><td>Blender 코딩 agent가 brief에서 4D 장면을 만들고 proxy video를 렌더하는 과제 242개 벤치마크 VibePrevisBench임. 평가 중심이고 로봇과 간접적임</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2611.16984'>ElasticDino: Dense Semantic Features Using Elastic Deformations</a></td><td>42</td><td>3</td><td>CV</td><td>ViT 특징의 채널 간 일관된 artifact를 공간 deformation으로 보정하는 경량 adapter ElasticDino로 pixel 정렬 고해상도 dense feature를 만들며 dense 인식에 쓸 수 있음</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2611.15389'>A physics-constrained deep reinforcement learning method for autonomous mission planning of Titan deep space probes</a></td><td>42</td><td>3</td><td>RL</td><td>물리 제약 action mask를 둔 maskable PPO로 타이탄 탐사선 자율 임무 계획을 학습하는 PCM-PPO이며 실행 불가능한 행동을 배제하는 구조이나 우주 임무 도메인 한정임</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2611.17007'>Skill Adapter: Personalized Modification and Online Routing of General-Purpose Skills</a></td><td>42</td><td>3</td><td>Skill Library</td><td>Skill Adapter는 범용 skill에 사용자별 Adapter를 붙이고 라우팅 agent가 현재 하위 과제에 맞는 skill을 RL로 고르며, SkillRL 대비 성공률이 평균 11.43퍼센트포인트 오름. skill pool 1,000개에서도 유지되고 skill chaining 관점의 참고가 되나 LLM agent 환경 한정임</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2611.15195'>A General Concept-based Decomposition for Vision-Language Embeddings</a></td><td>42</td><td>2</td><td>Multimodal</td><td>VLM embedding을 개념 단위로 분해하되 샘플 간 기하 관계를 보존하도록 feature 공간에서 학습하는 GRACE로 해석성을 높인 연구임</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2611.16307'>DEDCA: Test-Time Adaptation for Generalized AI-Generated Image Detection</a></td><td>42</td><td>2</td><td>CV</td><td>AI 생성 이미지 탐지기를 라벨 없이 test-time adaptation으로 새 generator에 맞추는 DEDCA임. test-time 적응 아이디어이나 로봇과 무관함</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2611.17298'>Consistent Video-to-Video Translation via Explicit Correspondences</a></td><td>42</td><td>2</td><td>Video</td><td>입력 영상의 patch 대응으로 과거 생성 출력을 검색해 correspondence cross-attention으로 넣는 vid2vid-long이며 실시간 영상 변환의 장기 일관성을 높임</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2611.14656'>Thompson Sampling using Prior-fitted Diffusion Transformers</a></td><td>42</td><td>1</td><td>LG</td><td>Prior-fitted diffusion transformer로 Thompson sampling을 하는 black-box 최적화 방법이며 로봇 연결은 약함</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2611.15404'>Is the Importance Ratio Necessary for Stable Reinforcement Learning in LLMs?</a></td><td>42</td><td>1</td><td>RL</td><td>LLM RL에서 importance ratio가 필요한지 검토함. LLM 한정임</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2611.15493'>The Illusion of Diversity: Aligning LLM Exploration via Effective Entropy</a></td><td>42</td><td>1</td><td>RL</td><td>LLM RL의 exploration을 effective entropy로 정렬함. LLM 한정임</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2611.16306'>Overcoming Spurious Correlations in Conditional Diffusion Models via Doubly Robust Target Correction</a></td><td>42</td><td>1</td><td>Generative</td><td>conditional diffusion의 spurious correlation을 doubly robust 목표로 줄임. 로봇 연결 약함</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2611.16206'>Turning Multi-Agent Communication into Token-Level Credit with On Policy Self Distillation</a></td><td>42</td><td>1</td><td>RL</td><td>OPSD4MAS는 다중 LLM agent의 통신에서 사실을 추출하고 leave-one-out으로 거른 뒤 token 단위 credit을 만들어 GRPO와 결합하며, 수학 pass@4를 GRPO 대비 최대 20퍼센트포인트 올림. credit assignment 아이디어는 흥미로우나 수학 추론 LLM에 한정됨</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2611.17241'>Ballad: Bandit-Based LLM Routing for Automated Heuristic Discovery</a></td><td>42</td><td>1</td><td>Optimization</td><td>Ballad는 LLM 풀에서 heuristic 탐색 단계마다 모델을 고르는 bandit 알고리즘으로 genealogy DAG credit 전파와 오래된 관측 할인을 쓰며, 최고 모델 단독 대비 API 비용을 최대 65.6% 줄임. 큰 모델이 항상 낫지 않다는 관찰은 유용하나 조합 최적화 도메인임</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2611.14958'>Adapting Monocular Depth Estimation in Novel Scenes through Disparity Refinement and Robot Ego-Motion</a></td><td>40</td><td>6</td><td>3D Vision</td><td>단안 depth 모델을 ego-motion으로 새 장면에 적응시키는 기법으로 incremental임</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2611.16205'>QVS-LIVO RiskMap: Health- and Information-Aware View Selection for Multi-Camera LIVO and Off-Road Risk Mapping</a></td><td>40</td><td>5</td><td>SLAM</td><td>multi-camera LIVO view selection과 위험 지도로 엔지니어링 중심임</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2611.16507'>Input-output characterization of robotic grasping: Connecting design parameters to grasp behavior through the admittance</a></td><td>40</td><td>5</td><td>Grasping</td><td>grasp 동역학 입출력 특성화 이론 분석임</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2611.17020'>Maximizing LLM Utility While Managing LLM Fallibility</a></td><td>40</td><td>5</td><td>Agent</td><td>LLM 오류 관리하며 활용을 극대화하는 의사결정 틀임</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2611.15238'>Towards Robust Vision-Language Reasoning: A Multi-Stage Optimization Pipeline with Masked Diffusion Model</a></td><td>40</td><td>5</td><td>Embodied AI</td><td>masked diffusion VLM에 planning 입력 표현, metric-guided diversity filtering, 장면 복잡도별 디코딩 DAD를 더한 MD-Drive가 NAVSIM에서 미최적화 대비 29.7% 개선함, 다단계 엔지니어링 조합 성격임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2611.16793'>EG360: Efficient and Generalizable $360^\circ$ Depth Estimation via Adaptive Panorama-Perspective Distillation and Spherical Cross-Level Feature Fusion</a></td><td>40</td><td>4</td><td>3D Vision</td><td>경량 모델에 panorama-perspective distillation과 spherical feature fusion을 넣어 Jetson에서 35 FPS로 도는 360도 depth 추정이며 임베디드 로봇에 쓸모 있으나 incremental함</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2611.15131'>Duo: A Reciprocal World Model for Full-Duplex Interaction</a></td><td>40</td><td>3</td><td>World Model</td><td>Intent와 Realization 두 모듈을 한 timeline에 묶어 음성과 영상을 실시간 full-duplex로 생성하는 Duo v1 기술 보고서이며 정량 근거가 약하고 로봇 연결도 약함</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2611.16382'>RADIANT: Redundancy-Aware Information Allocation for Universal Multi-Modal Fusion</a></td><td>40</td><td>3</td><td>Multimodal</td><td>중복 증거 억제, 모달리티 고유 정보 보존, 시너지 활성화 세 역할로 정보를 배분하는 multi-modal fusion RADIANT임. 일반 fusion 구조 제안이나 증분적임</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2611.16581'>Do the Details Help the Whole? One-Way Transfer from Person Actions to Group Intent in VLMs on JRDB-Social</a></td><td>40</td><td>3</td><td>Multimodal</td><td>JRDB-Social에서 개인 행동 학습이 집단 의도에 도움이 되는지 Qwen 계열 8개 조건으로 검증함. 단방향 전이를 밝힌 분석이나 소규모임</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2611.16523'>RESYNC: Residual Latent-State Synchronization for Deadline-Bound Streaming Inference</a></td><td>40</td><td>3</td><td>LG</td><td>큰 모델의 stale latent state를 빠른 경로로 갱신해 1ms 도착 스트림에서 99.4% 이상 제때 서빙함. 실시간 제어 추론에 참고할 수 있으나 시계열 예측만 평가함</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2611.14960'>Termination Lag: Coding Agents Solve Early but Stop Late</a></td><td>40</td><td>3</td><td>LG</td><td>코딩 agent가 첫 정답 patch 이후에도 35-60% 단계를 더 쓰고 1-8%는 정답을 되돌린다는 termination lag를 측정함, 종료 판단과 failure 관점에서 참고되나 SWE-bench 한정임</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2611.15047'>Saying No by Asking Yes: Affirmative Decomposition and Evidence Reflection for Frozen CLIP</a></td><td>40</td><td>2</td><td>Multimodal</td><td>부정 문장을 긍정 질의로 분해하고 evidence를 반사해 frozen CLIP의 negation 처리를 높인 NAES로 COCO-MCQ 82.4%를 냄</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2611.15420'>Learning Motion-Appearance Coupling Priors for Solving Video Inverse Problems</a></td><td>40</td><td>2</td><td>Video</td><td>video inverse problem에서 motion과 appearance의 결합 prior를 학습해 occlusion·조명 변화에 대응함. 복원 문제 중심이라 로봇과 간접적임</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2611.16000'>Predicting the Needle in a Petabyte Scale Haystack: Open-Vocabulary Event Anticipation in Satellite Imagery</a></td><td>40</td><td>2</td><td>CV</td><td>위성 영상에서 변화를 벡터로 표현해 어디서 무엇이 언제 끝날지 open-vocabulary로 예측하는 event anticipation 과제임. 로봇과 거리가 있음</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2611.14880'>FOE-Dreamer: Deployment-Efficient Learning of Cyber Defense Policies in Operational Networks</a></td><td>40</td><td>2</td><td>RL</td><td>실제 네트워크에서 world model 기반 cyber defense RL을 배포 효율적으로 학습함. 대상이 로봇이 아니라 네트워크 방어 환경임</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2611.15041'>AROMA: Adaptive Representation-Oriented Multimodal Actuation for Vision-Language Model Control</a></td><td>40</td><td>2</td><td>Multimodal</td><td>frozen VLM의 cross-attention head를 조작해 개수 세기를 제어하는 mechanistic 연구임. 로봇 제어와는 거리가 먼 연구임</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2611.16677'>Manifold Attracting Flow Matching: Physics-Constrained Sampling via Continuous Geometric Dynamics</a></td><td>40</td><td>2</td><td>Generative</td><td>물리 제약을 만족하는 flow matching 샘플링임. 제약 생성 관점이나 로봇 검증은 없는 상태임</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2611.16433'>daVinci-Prover: Agent-Native Mid-Training for Formal Theorem Proving</a></td><td>40</td><td>2</td><td>NLP</td><td>33.7B 토큰 agent-native mid-training 코퍼스와 Lean verifier 상호작용 trajectory로 정리 증명 agent를 만듦, long-horizon 대화형 구성은 흥미로우나 로봇과 거리가 있음</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2611.16211'>One Fuzzer, Many Reasoners: Adaptive Neuro-Symbolic Fuzzing with Reliability-Calibrated and Context-Gated Guidance</a></td><td>40</td><td>2</td><td>Testing</td><td>NSAI-Fuzz는 boundary pressure, grounding uncertainty 등 다섯 위험 신호로 neuro-symbolic 시스템의 실패를 찾는 fuzzing 틀이고 RCW와 CSG로 신호 가중치를 조정함. failure 탐색 관점은 로봇 failure diagnosis와 닿으나 대상은 추론 파이프라인임</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2611.16378'>Evidence-Governed Adoption of Self-Generated Updates in Autonomous AI Agents</a></td><td>40</td><td>2</td><td>Agent Safety</td><td>EGE는 agent가 스스로 만든 수정안을 fresh paired audit과 non-inferiority 검정을 거쳐 채택하도록 하는 통계 틀이며 adaptive 후보에 대한 simultaneous lower bound를 증명함. Monte Carlo 모의실험만 있어 실제 agent 검증은 없음</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2611.17103'>Joint Null-Space Projection for Data-Free Model Merging</a></td><td>40</td><td>1</td><td>LG</td><td>task vector마다 상위 특이 부분공간을 구해 다른 task의 부분공간 성분을 제거하는 closed-form data-free model merging이며 CLIP 8개 과제 평균 89.45%이나 로봇과는 거리거리가 멀음</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2611.15009'>From Forecasting to World Modeling: Can Temporal Foundation Models Recover Causal Response?</a></td><td>40</td><td>1</td><td>LG</td><td>시계열 foundation model이 인과 반응을 복원하는지 평가함. world model 용어를 쓰나 로봇과 거리가 있는 예측 문제임</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2611.15150'>Knowledge Transfer for Conditional Flow Matching: Frozen Estimation and Adaptation</a></td><td>40</td><td>1</td><td>Generative</td><td>conditional flow matching의 지식 전이 이론임. 로봇 연결 약함</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2611.16345'>DRAMA: Dissecting Attention Redundancy for Accelerating Multimodal Diffusion Large Language Models</a></td><td>40</td><td>1</td><td>Multimodal</td><td>multimodal diffusion LLM의 attention redundancy를 줄여 가속함. 효율 추론이나 로봇 검증이 없는 상태임</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2611.16694'>When Expert Disagreement Hurts: Prestige and Selectivity in LLM Decision Revision</a></td><td>40</td><td>1</td><td>LLM Eval</td><td>전문가 반박 맥락에서 LLM이 정답을 뒤집는 비율을 a/(1-a) 기준으로 계산해 선택성을 따지는 감사 틀이며, 5개 모델 모두 기준을 못 넘고 정확도가 최대 16.1점 떨어짐. 분석 설계가 명확하나 언어 판단 한정이라 로봇 관련성 낮음</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2611.14683'>Trait Hitchhiking in LLM Post-Training</a></td><td>40</td><td>0</td><td>NLP</td><td>LLM RL post-training 중 trait 전이를 분석함. 분석 대상이 LLM 한정이라 로봇 연결이 없는 분석임</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2611.15779'>Honesty Is a Race: Predicting When Verifiable-Reward RL Teaches a Model to Bluff</a></td><td>40</td><td>0</td><td>NLP</td><td>verifiable reward RL에서 모델이 bluff하는 시점을 예측함. LLM 한정임</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2611.16009'>JustRUA: A Controlled Study of GPT-6 Robot-Use Agents</a></td><td>38</td><td>6</td><td>Agent</td><td>GPT-6 robot-use agent 통제 비교 연구로 harness 의존성이 큼</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2611.15112'>Elastra: A Simulation Framework for Elastic Bodies</a></td><td>38</td><td>5</td><td>Simulation</td><td>탄성체 상호작용 simulation framework로 도구 성격이 강함</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2611.16725'>Safe and Efficient Navigation Considering Texting Pedestrians via Attention-Aware Cost-map Tuning</a></td><td>38</td><td>5</td><td>Social Nav</td><td>주의 인지 cost-map 튜닝으로 보행자 회피를 개선하는 incremental 기법임</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2611.16918'>CT-SGAL-LIO: Causal Continuous Time Refinement of Discrete LiDAR Inertial Odometry</a></td><td>38</td><td>5</td><td>SLAM</td><td>연속시간 LiDAR 관성 odometry 정제로 incremental임</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2611.15966'>Subject-Held-Out Evaluation of Deep Ground Reaction Force Estimators Across Two Laboratories: Leakage and Cross-Laboratory Transfer</a></td><td>38</td><td>3</td><td>LG</td><td>지면반력 추정기를 trial 분할, 피험자 held-out, 실험실 간 전이로 평가해 분할 방식이 구조보다 큰 영향을 줌을 보임. 보행 생체역학 평가 연구임</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2611.15756'>How Far Can Frozen Vision-Language Models Go on Event Data? A Training-Free Study on EventBench</a></td><td>38</td><td>2</td><td>Multimodal</td><td>EventBench 챌린지에서 RGB 사전학습 VLM을 event 데이터에 학습 없이 렌더링과 prompt만으로 적용해 한계를 재는 보고서임</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2611.16701'>Sprint3D: Accelerating End-to-End 3D Asset Generation through Pipeline Optimization</a></td><td>38</td><td>2</td><td>3D Vision</td><td>Pixal3D 파이프라인의 mesh 후처리를 GPU로 옮기고 flow를 8회 평가로 distillation해 에셋당 133초를 4.05초로 줄인 공학적 가속임</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2611.15246'>Dual Representation Enhanced Diffusion Policy for Flexible Job Shop Scheduling</a></td><td>38</td><td>2</td><td>RL</td><td>job shop scheduling에 dual representation과 diffusion policy를 쓰는 RL scheduler임. makespan을 최대 5.44% 줄이나 로봇 조작과는 다른 조합 최적화 문제임</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2611.16039'>Improved Elastic Weight Consolidation as an Optimization Constraint for Continual Learning</a></td><td>38</td><td>2</td><td>LG</td><td>EWC를 optimization constraint로 재해석해 sample 가중 결함을 고친 IEWC임. 분류, 분할, diffusion에서 ImageNet-R 2.0퍼센트포인트 개선이며 로봇 검증은 없는 상태임</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2611.16174'>JudgeMix: Judge-Guided Mixed-Rollout Data Synthesis for LLM Agents</a></td><td>38</td><td>2</td><td>NLP</td><td>judge로 mixed rollout 데이터를 합성해 LLM agent SFT를 함. LLM agent 한정임</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2611.16384'>Beyond Compressing Everything: Contrastive Memory Learning for Selective Context Compression</a></td><td>38</td><td>2</td><td>NLP</td><td>query 조건 contrastive compressor와 같은 문서 다중 query hard negative로 선택적 context 압축을 하며 agent memory 쪽에 약하게 연결되나 NLP QA 벤치마크 위주임</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2611.14931'>Hint-Informed Self-Distillation for Reasoning Segmentation</a></td><td>38</td><td>1</td><td>Multimodal</td><td>reasoning segmentation에서 hint를 조건으로 한 EMA teacher가 token 단위로 credit을 주는 HISD로 ReasonSeg를 올린 RL 후학습 개선임</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2611.17194'>eDMD: Endpoint Distribution Matching for Few-Step Diffusion Distillation</a></td><td>38</td><td>1</td><td>Generative</td><td>few-step diffusion distillation에서 fake model을 student 최종 출력에만 학습시키는 eDMD로 분포 일치 조건을 증명하나 로봇과 직접 연결은 약함</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2611.16304'>StateAlign: Internalizing State-Aware Decision-Making for Reliable Multi-Turn Tool Agents via Reinforcement Learning</a></td><td>38</td><td>1</td><td>NLP</td><td>multi-turn tool agent의 state-aware 의사결정 RL임. LLM agent 한정임</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2611.14965'>Early Signals, Strong Decisions: Prefix-Guided Sampling for Parallel Test-Time Scaling</a></td><td>38</td><td>1</td><td>LG</td><td>짧은 prefix의 내부 confidence로 후보를 거른 뒤 유망한 경로만 완성하는 PreG로 parallel test-time scaling의 토큰을 줄임, 결정 경계 근처 질문에서 confidence가 중요하다는 분석 포함임</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2611.15885'>Reward-Driven Collider Physics Challenges for Self-Improving Agentic AI via Reinforcement Learning</a></td><td>38</td><td>1</td><td>RL</td><td>고에너지 물리 과제에 연속 reward를 주는 open-ended RL 환경을 만들고 소형 언어모델이 자동 피드백만으로 개선되는 것을 개념 검증함. 검증 가능한 reward 설계는 흥미로우나 로봇과 거리가 멂</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2611.17161'>Cited but Unused: Parametric Provenance in Retrieval-Augmented Generation</a></td><td>38</td><td>1</td><td>LLM Analysis</td><td>retrieved passage의 사실을 거짓으로 바꾸는 counterfactual value substitution으로 RAG 인용 중 1.2~15.7%가 parametric memory 유래임을 측정하고 NLI 검증이 우연 수준임을 보임. counterfactual 개입으로 provenance를 재는 발상이 흥미로우나 로봇과 거리가 멂</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2611.14704'>Code as Explanations: Executable and Verifiable LLM Explanations</a></td><td>38</td><td>0</td><td>NLP</td><td>LLM 설명을 실행 가능한 코드로 만들어 검증함. 로봇 연결 약함</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2611.16212'>SPEM: Scan-Prior Entropy Modeling for LiDAR Point Cloud Compression</a></td><td>36</td><td>3</td><td>3D Vision</td><td>LiDAR scan 구조 prior를 좌표 변환이 아닌 확률 모델링에 써서 point cloud를 압축하는 SPEM임. 압축 효율 개선 중심임</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2611.15530'>MAGIC: Modality-Aware Gini Inspection for Clinical Hallucination Detection in LMMs</a></td><td>36</td><td>2</td><td>Multimodal</td><td>modality 간 attention 분포의 불균형을 Gini 계수로 재서 의료 LMM의 hallucination을 탐지함. 의료 한정이나 탐지 아이디어는 failure detection과 닮음</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2611.17052'>Auditing AI peer reviewers: a benchmark on real scientific papers</a></td><td>36</td><td>1</td><td>NLP</td><td>논문에 수식, 수치, 인용 오류를 주입해 12개 AI reviewer의 검출률을 재는 벤치마크와 multi-agent reviewer Skepthical을 제시함, 평가 설계는 탄탄하나 로봇과 거리가 있음</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2611.14850'>Effective Teacher Support for Reasoning Distillation</a></td><td>36</td><td>1</td><td>LG</td><td>teacher 상위 0.01% vocabulary만 남겨 Qwen3 4B에서 1.7B로 distillation해도 MMLU-Pro가 유지되고 step time 38% 감소함, 효율 개선이나 모델 계열별 cutoff 의존성이 있음</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2611.15481'>SkillEarth: Teaching General-Purpose Agents to Act on Earth via Skill Evolution</a></td><td>36</td><td>1</td><td>LG</td><td>원격 탐사 tool-call 지식을 시연 trajectory에서 skill 파일로 뽑고 실제 도구 실행 관찰에 근거해 component 단위로 고치는 SkillEarth이며 OpenEarth-Bench 도메인 한정임</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2611.16628'>Safety as a Budget: Calibrating the Control Channel of Constrained GRPO for Vision-Language Models</a></td><td>36</td><td>1</td><td>Safety RL</td><td>constrained GRPO에서 scorer의 mean 편향과 그룹 정규화가 Lagrange multiplier를 무력화함을 분석하고 단조 map으로 보정하는 2-channel 방법을 제안함. Qwen3-VL-2B에서 유해 응답률을 8.9%에서 4.8%로 낮춤. 제약 RL 분석은 탄탄하나 VLM 안전 정렬 한정임</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2611.16789'>ScrewSense: Mapping the Invisible - Anomaly Detection and Error Classification in Screwdriving Processes</a></td><td>35</td><td>5</td><td>LG</td><td>나사 체결 공정 이상 탐지와 오류 분류로 산업 응용이나 방법 novelty 작음</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2611.15217'>Are We Ready for Snow-tonomous Driving? Challenges Toward Robust Automated Driving in Extreme Weather</a></td><td>35</td><td>5</td><td>Driving</td><td>극한 날씨 자율주행 과제 정리로 survey 성격임</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2611.15928'>Runtime Safety and Emergency Stops on a Full-Size Humanoid: Deployment Lessons and a Case for Graduated Force Authority</a></td><td>35</td><td>5</td><td>Humanoid</td><td>full-size humanoid 런타임 안전과 e-stop 배포 교훈 보고임</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2611.17213'>Collaborative Task Allocation for Heterogeneous Multi-Robot Systems Through Iterative Clustering</a></td><td>35</td><td>5</td><td>Multi-Robot</td><td>반복 clustering 기반 이종 로봇 task 할당으로 고전적 기법임</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2611.16473'>Robots That Talk Too Much and Don&#x27;t Listen Enough</a></td><td>35</td><td>4</td><td>HRI</td><td>사회 로봇 음성 상호작용 문제 제기 관점 논문임</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2611.16767'>Evaluating Video LLMs&#x27; Understanding of Corner Cases in Autonomous Driving</a></td><td>35</td><td>3</td><td>Multimodal</td><td>Video LLM 25종을 운전 corner case 영상 1,709개로 평가한 DashBench이며 모두 안전 기준에 못 미침을 보였으나 벤치마크 위주임</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2611.17267'>LiveGeo: Benchmarking Geographic Agents in Continuously Evolving Worlds</a></td><td>35</td><td>3</td><td>Agent Benchmark</td><td>GeoWorld는 지리 상태가 시간에 따라 변하는 환경이고 LiveGeo는 agent가 근거를 다시 확인하고 계획을 고치는 능력을 재며 최신 LLM도 동적 신뢰성이 낮음을 보임. 변하는 세계에서의 재계획이라는 관점은 있으나 LLM 지리 과제 benchmark임</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2611.15526'>SCR-Mamba: Skeleton-conditioned Mamba with cross-scale incremental refinement for efficient 3D human pose estimation</a></td><td>35</td><td>2</td><td>CV</td><td>skeleton 조건 Mamba와 다중 해상도 refinement로 효율적인 video 3D human pose estimation을 하는 SCR-Mamba임. 증분적 구조 개선임</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2611.14980'>CoLFA: Collaboration-Guided Lightweight Failure Attribution for LLM-Based Multi-Agent Systems</a></td><td>35</td><td>2</td><td>NLP</td><td>multi-agent LLM failure attribution의 경량 기법으로 실패 진단 관점은 있으나 로봇 아님</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2611.17107'>Disentangling Spurious Correlations: How IRM Handles Diverse Shortcuts in Text Classification</a></td><td>35</td><td>2</td><td>LG</td><td>label-generated, confounding, selection bias 세 shortcut 구조에서 IRM이 spurious 상관을 억제함을 인과 틀로 평가함, causal 관점은 흥미로우나 텍스트 분류 한정임</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2611.16175'>Stack more levels: how to get general and human-like Mario playing</a></td><td>35</td><td>2</td><td>RL</td><td>PCG로 만든 Mario 레벨 수를 늘리며 PPO 일반화를 측정하고 DRAIL로 사람다운 행동을 입히는 게임 AI 연구임. RL 일반화의 학습 환경 다양성 효과는 참고할 만하나 새로운 방법은 아님</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2611.16526'>Lost in Delegation: Studying the Effectiveness of Task Orchestration in Generative Search</a></td><td>35</td><td>2</td><td>LLM Agent</td><td>생성형 검색에서 orchestrator LLM이 하위 agent에 위임하는 방식이 직접 tool 사용보다 낫지 않고 post-cutoff 정보에서는 정확도가 크게 떨어짐을 보이며 질의 왜곡 등 실패 유형을 분석함. 분석 중심이고 로봇 관련성 낮음</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2611.15168'>MAST: Medoid-Anchored Subspace Steering for Visual Grounding in Multimodal LLMs</a></td><td>35</td><td>1</td><td>Multimodal</td><td>MLLM activation steering에서 전역 평균 대신 task별 cluster medoid와 low-rank 부분공간을 쓰는 training-free MAST를 제안한 기법임</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2611.15572'>Learning a calibrated decision head from logged bandit feedback</a></td><td>35</td><td>1</td><td>RL</td><td>logged bandit feedback으로 calibrated decision head를 학습함. 로봇 연결 약함</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2611.15829'>Training Calibrated Conditional Generative Models with a Sample-Only Coverage Loss</a></td><td>35</td><td>1</td><td>Generative</td><td>conditional generative model의 coverage 보정 loss임. 로봇 연결 약함</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2611.16182'>Same-State Pairs Make One JEPA Proof of the Platonic Representation Hypothesis Vacuous</a></td><td>35</td><td>1</td><td>LG</td><td>JEPA 기반 Platonic representation 증명이 공허함을 보임. 이론 비판이며 로봇 연결 약함</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2611.17287'>Negative-Only Policy Optimization for One-Sided Verifiable Rewards</a></td><td>35</td><td>1</td><td>RL</td><td>한쪽 검증만 가능한 RLVR의 negative-only 최적화로 LLM 중심이며 로봇 연결 약함</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2611.16843'>Shortcuts or Memorisation? Revisiting Data Corruption in Natural Language Understanding with Large Language Models</a></td><td>35</td><td>1</td><td>NLP</td><td>명사 제거 같은 입력 교란에 대한 LLM 견고성이 contamination이 아니라 데이터셋 shortcut 때문임을 새 368개 문항으로 보임, 평가 방법론 분석임</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2611.15029'>Mask-Pattern Position Augmentation: Training-Free Long-Context Extrapolation for Diffusion LLMs</a></td><td>35</td><td>0</td><td>NLP</td><td>diffusion LLM의 training-free 길이 외삽 기법임</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2611.15479'>DETER: Suppression During Pretraining for Tamper Resistance</a></td><td>35</td><td>0</td><td>NLP</td><td>pretraining 중 위험 지식을 억제하는 tamper resistance임</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2611.15842'>Fewer Expert Transfers Without Changing Routing: Expert Eviction for MoE Offloading</a></td><td>35</td><td>0</td><td>NLP</td><td>MoE offloading에서 expert eviction으로 전송을 줄임. LLM 추론 효율 개선임</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2611.16072'>KVPath: Connecting Key-Value Representations Across Transformer Layers</a></td><td>35</td><td>0</td><td>NLP</td><td>Transformer layer 간 KV 표현을 연결함</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2611.16265'>Rectified Looped Transformer</a></td><td>35</td><td>0</td><td>LG</td><td>Looped Transformer 개선임</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2611.16375'>Recursive State-Augmented Language Models: Persistent Latent-State Adaptation of Pretrained Language Models</a></td><td>35</td><td>0</td><td>NLP</td><td>LM에 지속 latent state를 붙여 긴 문맥을 처리함</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2611.15983'>TRACE: Trajectory Synchronization for Training-Free Resolution Extension in Video Generation</a></td><td>34</td><td>1</td><td>Video</td><td>저해상도와 고해상도 denoising 궤적을 동기화해 학습 없이 text-to-video 해상도를 확장하는 TRACE임. 생성 품질 개선 위주임</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2611.16956'>Lara Mini Base: Language Diversity as a Resource, Not a Trade-off</a></td><td>34</td><td>1</td><td>NLP</td><td>6T 토큰, 45개 언어로 7.2B 총 0.6B active MoE base model Lara Mini를 학습해 언어 간 용량 경쟁이 줄어듦을 보임, scale 위주 기술 보고임</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2611.14844'>AutoAssumption: Searching over Assumptions Discovers ML-Systems Algorithms</a></td><td>34</td><td>1</td><td>LG</td><td>알고리즘을 Lean proof graph로 쓰고 가정 하나를 완화해 KV-cache eviction과 pruning 알고리즘을 재도출하는 AutoAssumption이며 아이디어는 새로우나 ML 시스템 영역임</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2611.15049'>Science Prediction Universe</a></td><td>34</td><td>1</td><td>LG</td><td>화학, 재료, 생물 실험 결과를 순위로 예측하는 Science Prediction Universe 벤치마크이며 최고 Spearman 0.478로 agent가 과학적 판단에서 막힘을 보임</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2611.17115'>CapLite: Prompt-Injection Defense for Small Language Model Agents without Model-Written Security Artifacts</a></td><td>34</td><td>1</td><td>Agent Security</td><td>CapLite는 tool schema에서 정책을 만들고 write 호출을 도구 결과를 읽기 전에 확정해 사용자 요청에 없는 인자의 write를 막으며, AgentDojo 13,935회 공격에서 성공 0건임. 보장 방식은 명확하나 LLM agent 보안 한정임</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2611.15457'>WaveFlow-UIE: A Single-Pipeline Wavelet-Domain Flow Model for Efficient Underwater Image Restoration</a></td><td>33</td><td>2</td><td>CV</td><td>wavelet 영역에서 단일 파이프라인 flow model로 수중 영상을 복원하는 WaveFlow-UIE임. 수중 로봇 인지에 간접적이고 증분적임</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2611.14736'>When Should Semantic Priors Enter Partially-Identified Causal Discovery?</a></td><td>33</td><td>2</td><td>LG</td><td>causal discovery에서 LLM 의미 사전지식을 쿼리 배치, 제안 수용, 그래프 유지 세 결정으로 나눠 분석함, 불안정 edge 타깃팅이 무작위 대비 이점이 없다는 부정적 결과가 중심임</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2611.16408'>Gravity and Flight: Learning to Navigate Fine-Grained Remote Sensing Scenes</a></td><td>33</td><td>1</td><td>Multimodal</td><td>원격탐사 VLM에 Evidence-of-Thought SFT와 RTPO 정책 최적화를 결합한 장면 특화 방법임. 도메인 특화 fine-tuning 위주임</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2611.14970'>Poison-then-Hide: Finetuning-Activated Backdoor Attack on Pretrained Vision Encoders</a></td><td>33</td><td>1</td><td>CV</td><td>pretrained vision encoder에 fine-tuning 시 활성화되는 backdoor 공격임. 보안 주제임</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2611.17162'>Symmetry in Time: A Representation Theory of Linear Recurrent Memory</a></td><td>33</td><td>1</td><td>LG</td><td>선형 recurrent 메모리의 표현론 분석으로 이론적 흥미는 있으나 로봇 연결 약함</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2611.16895'>Human or Synthetic? What a Fixed Budget Buys for Post-Training</a></td><td>33</td><td>1</td><td>NLP</td><td>같은 달러 예산에서 human과 synthetic preference 데이터의 DPO 효과를 비교해 합성 데이터가 비용 효율적임을 보인 실증 분석이며 로봇과 거리가 멂</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2611.16744'>Scale-Induced Semantic Shift in Visual Prompt Injection Against VLMs and Web Agents</a></td><td>33</td><td>1</td><td>Multimodal Safety</td><td>이미지를 강하게 축소하면 숨은 텍스트 지시가 읽히는 Scale-Induced Semantic Shift를 정의하고 closed-loop black-box 공격과 ScaleGuard 탐지기를 제안함. VLM 보안 주제이고 실제 web agent 침해율은 약 4%에 그침</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2611.16991'>AnalogLayoutWorld: An Open Benchmark for Agentic Analog Layout Design</a></td><td>33</td><td>1</td><td>Agent Benchmark</td><td>아날로그 회로 layout을 netlist에서 생성하는 40개 과제 benchmark이며 13개 구성 중 acceptance 통과가 23.0%에 그침. 기하 제약 하의 long-horizon 작업 평가이나 EDA 도메인이라 로봇 관련성 낮음</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2611.14729'>SunLightBots: Turning sunlight into self-sustained, high-power motion in soft robots</a></td><td>32</td><td>5</td><td>Soft Robot</td><td>태양광 구동 soft robot 소재 연구로 학습 측면 기여 없음</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2611.14918'>DIVAL: Diffeomorphic Vector-Field Alignment for Nonholonomic Motion Planning</a></td><td>32</td><td>5</td><td>Planning</td><td>nonholonomic vector field 정렬 planner로 제어 기법이며 학습 연관 약함</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2611.15809'>Fine-Grained Generative Hallucination Detection and Correction for Aerial Image Captioning</a></td><td>32</td><td>2</td><td>Multimodal</td><td>항공 이미지 captioning에서 MLLM의 세부 hallucination을 탐지하고 교정하는 방법임. UAV 응용이나 captioning 한정임</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2611.16515'>PiLLVD: A Real-World Low-Light Video Dataset for Dynamic Scenes Captured with Off-the-Shelf Cameras</a></td><td>32</td><td>2</td><td>CV</td><td>실제 off-the-shelf 카메라로 찍은 동적 장면 low-light 쌍 영상 데이터셋 PiLLVD임. 데이터 기여 중심임</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2611.16803'>Detection Is Not Early Warning: Evaluating Token-Level Alarms on Language Model Failures</a></td><td>32</td><td>2</td><td>NLP</td><td>LLM 실패 시작 token 경보 평가 지표 제안이나 로봇 failure와 연결 약함</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2611.16662'>MuSeToM: Multi-Sensory Evaluation of Belief Revision with Textual Cues Across Six Senses</a></td><td>32</td><td>2</td><td>NLP</td><td>시각 등 6개 감각 단서로 믿음 수정 여부를 묻는 텍스트 ToM 벤치마크 MuSeToM을 만들고 LLM이 단서에 과잉 갱신함을 보임, 사회적 추론 평가 한정임</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2611.15161'>CineMME: From Dialogue Grounding to Narrative Reasoning in Multimodal Video Understanding</a></td><td>32</td><td>1</td><td>Video</td><td>대사, 화자, 줄거리 증거 사슬을 975개 클립으로 진단하는 영화 서사 video benchmark이며 Gemini-3 Pro의 active-speaker vIoU가 7.74%에 그침을 보인 dataset 기여임</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2611.15617'>WaveletLoRA: Frequency-Aware Content-Style Decomposition for Personalized Image Generation</a></td><td>32</td><td>1</td><td>CV</td><td>wavelet 영역 supervision으로 content와 style을 분해하는 WaveletLoRA 개인화 이미지 생성임. 로봇과 무관한 생성 기법임</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2611.16650'>Learning the Missing Derivative: Neural Multiple-Scattering Operators for Inverse Volume Rendering</a></td><td>32</td><td>1</td><td>CV</td><td>다중 산란 필드를 neural operator로 예측해 inverse volume rendering의 미분을 얻고 inversion 궤적으로 fine-tuning하는 방법이나 로봇과 거리거리가 멀음</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2611.15227'>MOON-RL: Multi-Objective Optimization via Objective Space Navigation with Reinforcement Learning</a></td><td>32</td><td>1</td><td>RL</td><td>multi-objective 설계 최적화에 RL을 적용함. 로봇 연결 약함</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2611.15237'>Regret Bounds for Quantum Linear Bandits</a></td><td>32</td><td>1</td><td>RL</td><td>quantum linear bandit regret bound 이론임</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2611.16426'>SoScale: Second-Order Scale Search for FP4 Quantization</a></td><td>32</td><td>1</td><td>LG</td><td>FP4 양자화 scale 탐색임. 효율 추론이나 로봇 무관함</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2611.17191'>Maximizing Capacity Utilization of LoRA Adapters for Mitigating the Learning-Forgetting Trade-off</a></td><td>32</td><td>1</td><td>NLP</td><td>LoRA 용량 활용 개선으로 forgetting 완화하나 incremental임</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2611.14997'>Same Task, Different Statement: When and How Reformulation Helps LLM Problem Solving</a></td><td>32</td><td>1</td><td>NLP</td><td>decomposition, typed reformulation, concept reduction 세 재서술이 수학, 논리, 코드 문제에서 oracle 선택 시 정확도를 27.6% 올림을 보인 프롬프트 분석이며 고정 규칙 이득은 11.0%에 그침</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2611.15309'>Where Autonomy Belongs: A Separation of Powers for Agentic Program Evolution</a></td><td>32</td><td>1</td><td>LG</td><td>program evolution을 govern, propose, judge 세 결정으로 나눠 권한을 분리한 EvoTrias 구조이며 토큰 비용 64% 감소를 보이나 코드 탐색 시스템 설계 위주임</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2611.16414'>Small Language Models for Inference-Capability Routing: Effects of Model Capacity and Prompt Optimization on Downstream Quality and Efficiency</a></td><td>32</td><td>1</td><td>LLM Efficiency</td><td>Qwen2.5 소형 router 1.5B에서 14B를 prompt 최적화와 함께 비교해 추론 capability 활성화를 결정하고, 14B router로 downstream 토큰을 68.7퍼센트 줄임. 라우팅 설계 비교 연구이고 로봇과 거리가 멂</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2611.16591'>Singularity-Bench: Can Agents Build Agents?</a></td><td>32</td><td>1</td><td>Agent Benchmark</td><td>pre-training부터 cluster orchestration까지 6개 과제로 agent가 AI 시스템을 직접 구축하는 능력을 재는 Singularity-Bench이며 Harbor의 reward hacking 취약점을 막는 Breakwater를 만듦. 주장이 과장된 편이고 로봇과 거리가 멂</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2611.15603'>Are Scaling Laws of Universal MLIPs Universal?</a></td><td>32</td><td>0</td><td>LG</td><td>MLIP scaling law 분석임</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2611.15607'>FADO: Learning Causal Explanations with Prior-Fitted Networks</a></td><td>32</td><td>0</td><td>LG</td><td>prior-fitted network로 인과 설명을 학습함. 표 데이터 중심임</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2611.15621'>Data-Free Metrics Don&#x27;t Work: The Missing Invariance Under Functionally Preserving Reparameterisations</a></td><td>32</td><td>0</td><td>LG</td><td>data-free 지표가 reparameterization 불변성이 없음을 보임</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2611.16069'>&quot;It&#x27;s Just a Small Weapon&quot;: What Rewarding Misbehavior During RL Does to Character-Trained Models</a></td><td>32</td><td>0</td><td>NLP</td><td>RL에서 misbehavior 보상이 character 모델에 미치는 영향임</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2611.16317'>Wanda-Guided Sparse Perturbations for Efficient Zeroth-Order Optimization</a></td><td>32</td><td>0</td><td>LG</td><td>Wanda 기반 sparse perturbation으로 zeroth-order fine-tuning을 가속함</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2611.16409'>Experience-Handoff Reinforcement Learning for Recursive Self-Improvement</a></td><td>32</td><td>0</td><td>RL</td><td>LLM agent의 recursive self-improvement용 RL임</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2611.14685'>Terrain-Aware Thompson Sampling for Multi-Drone Search and Rescue</a></td><td>30</td><td>5</td><td>Navigation</td><td>지형 정보 활용 multi-drone Thompson sampling 탐색으로 응용 중심 incremental임</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2611.15135'>ARTS: An Open-Source, Reproducible Three-Arm Platform for Autonomy Research in Minimally Invasive Surgery</a></td><td>30</td><td>5</td><td>Surgical</td><td>3-arm 수술 자율성 오픈 플랫폼으로 하드웨어 재현성 기여임</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2611.15066'>MiniPose: Miniature-Based Real Data Collection for 6D Pose Estimation of Large Industrial Pipe Segments</a></td><td>30</td><td>4</td><td>3D Vision</td><td>산업 배관 6D pose용 miniature 데이터 수집으로 응용 중심임</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2611.15386'>Actuation and Control of Passive Tendon-Driven Soft Extensions Through Rigid Manipulator Motion</a></td><td>30</td><td>4</td><td>Soft Robot</td><td>tendon 구동 soft extension의 manipulator 구동 제어로 하드웨어 중심임</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2611.15314'>AcrossPlace: Do Vision--Language Models Recognize Places Beyond Their Source Views? A Comprehensive Benchmark</a></td><td>30</td><td>3</td><td>Multimodal</td><td>GSV-Cities 기반 5만 6천 장소의 언어-이미지 place recognition benchmark이며 source 이미지에서 독립 target으로 가면 Recall@1이 19.69%에서 12.31%로 떨어짐을 보인 dataset 기여임</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2611.16061'>Pothole Risk Assessment with Geometrically Grounded Vision Language Models</a></td><td>30</td><td>2</td><td>CV</td><td>검출된 pothole을 perspective 변환, SAM 분할, 기하 특징, Gemini 심각도 판단의 5단계로 평가하는 모듈 파이프라인임</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2611.16574'>HALight: Heterogeneous Multi-Agent Reinforcement Learning for Traffic Signal Control under Lane-Level Missing Observations</a></td><td>30</td><td>2</td><td>RL</td><td>교통 신호 제어 heterogeneous MARL이며 로봇과 거리가 있는 예측 문제임</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2611.17116'>Bellman Contraction under MMD: A Unified Framework</a></td><td>30</td><td>2</td><td>RL</td><td>distributional Bellman의 MMD contraction 이론으로 RL 이론이나 로봇과 거리 있음</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2611.15655'>Can Agents Relive Past Experiences? Diagnosing Event-Affect Decoupling in Affective-Episodic Retrospection</a></td><td>30</td><td>2</td><td>NLP</td><td>memory agent의 정서 episodic 회상 진단으로 memory 주제와 약하게 연결됨</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2611.15460'>Read and Ignore: What Self-Directed LLM Agents Do in Public Service Scenarios</a></td><td>30</td><td>2</td><td>LG</td><td>공공 서비스 4개 시나리오에서 10개 LLM의 2,400개 trajectory를 모아 목표가 불명확하면 18.7%만 산출물을 만듦을 보임, 행동 관찰 연구이며 로봇과 거리가 있음</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2611.15187'>OT-BLS: Optimal-Transport-based Backbone Layer Selection for Frozen DINOv3 in Cross-Domain Few-Shot Segmentation</a></td><td>30</td><td>1</td><td>CV</td><td>cross-domain few-shot segmentation에서 query와 support patch 사이 optimal transport 질량으로 DINOv3 층을 고르는 OT-BLS로 mIoU 55.72를 57.62로 올린 작은 개선임</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2611.15433'>Verifier Choice is a Benchmark Design Variable: Auditing Structural Counting Evaluation in Text-to-Image Models</a></td><td>30</td><td>1</td><td>Multimodal</td><td>text-to-image 개수 세기 평가에서 verifier 선택이 점수를 바꾼다는 audit 연구로 로봇과 무관한 평가 방법론임</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2611.15449'>Reading the Unreadable: Text-Aware Image Super-Resolution Needs Reasoning</a></td><td>30</td><td>1</td><td>CV</td><td>text-aware super-resolution에 reasoning이 필요한지 진단하는 ReasonText 벤치마크를 만듦. 로봇과 거리가 먼 복원 과제임</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2611.16310'>Selective Generative Restoration for Video Deraining via Uncertainty-Aware Diffusion</a></td><td>30</td><td>1</td><td>Video</td><td>불확실성 지도로 신뢰 영역은 충실 복원하고 가려진 영역만 diffusion prior로 생성하는 video deraining임. 로봇과 거리가 있음</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2611.16630'>When Chekhov&#x27;s Gun Fires Anyway: Over-Realization in Text-to-Image Models</a></td><td>30</td><td>1</td><td>Multimodal</td><td>text-to-image에서 부정문 등에 언급된 대상이 그려지는 over-realization을 OverReal 벤치마크로 측정하고 attention 원인을 분석했으나 로봇과 거리거리가 멀음</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2611.15945'>Reinforcement Learning for Inventory Control under Regime-Switching Demand: A Controlled Comparison of LSTM, MLP, and (s,S) Policies</a></td><td>30</td><td>1</td><td>RL</td><td>재고 관리에 RL을 적용해 비교함</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2611.16905'>Factored One-sided Adam-Moment for Practical and Scalable SOAP</a></td><td>30</td><td>1</td><td>LG</td><td>SOAP optimizer 메모리 축소 기법으로 로보틱스 연관 약함</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2611.16934'>Time Flies When You Parallelise: Pareto-efficient Time Series Foundation Models with Linear Recurrences</a></td><td>30</td><td>1</td><td>LG</td><td>시계열 foundation model 효율화로 로봇 연관 약함</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2611.17134'>Support-Constrained Offline Policy Improvement for Pediatric ECMO from Limited Clinical Data</a></td><td>30</td><td>1</td><td>RL</td><td>소아 ECMO용 support 제약 offline RL로 의료 응용이며 로봇 무관함</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2611.17314'>Linking Rapid Learning to Compositional Structure in Neural Networks: Evidence from Additive Analogies in Meta-Learned Parameter Spaces</a></td><td>30</td><td>1</td><td>LG</td><td>meta-learning 파라미터 공간의 compositional 구조 분석으로 로봇 연관 약함</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2611.14996'>Breaking Bad: &quot;Going Badly&quot; Activations Drive Reward Hacking</a></td><td>30</td><td>1</td><td>NLP</td><td>reward hacking과 activation 연관 분석임</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2611.16714'>Towards Green Text Generation: Memory-Based Speculative Decoding</a></td><td>30</td><td>1</td><td>NLP</td><td>4-token window memory 기반 CPU 분류기를 speculative decoding의 draft로 써서 에너지를 줄임, 아이디어는 재미있으나 로봇과 거리가 멀고 도메인 한정 이득임</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2611.16929'>SPADE: Soft Prompts for Ai-text DEtection</a></td><td>30</td><td>1</td><td>NLP</td><td>PMI로 prompt의 설명력을 재서 클래스별 soft prompt로 AI 텍스트를 판별하는 탐지기이며 OOD 성능은 좋으나 로봇과 무관함</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2611.14681'>Together Compiler: Continual Compilation for AI Inference</a></td><td>30</td><td>1</td><td>LG</td><td>agent hill-climbing으로 추론 forward pass를 지속 컴파일하는 Together Compiler이며 Llama 1B에서 hand-written megakernel 대비 최대 1.7배, 시스템 엔지니어링 성격이 강하고 로봇과 거리가 있음</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2611.14794'>When Is Proof-Step Verification Worth Its Cost? Operating Requirements of Certify-or-Decline Verification for Open-Weight Mathematical Reasoning</a></td><td>30</td><td>1</td><td>NLP</td><td>proof-step verification이 GPQA, AIME에서 정밀도를 31, 46포인트 올리지만 coverage가 크게 줄고 self-consistency와 차이가 불확실함을 보인 수학 추론 평가임</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2611.15109'>Expanding the Decision Space of Pretrained Models through Structured Re-Decoding</a></td><td>30</td><td>1</td><td>LG</td><td>사전학습 모델의 국소 후보를 재조합해 KL 예산 내에서 reward를 올리는 training-free Structured Re-Decoding이며 분자, 단백질 설계에 적용되고 coherent Ising machine 예비 실험이 있음</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2611.15592'>Small Heads, Strong Decisions: A Controlled Study of Typed-Decision Models</a></td><td>30</td><td>1</td><td>NLP</td><td>typed-decision 모델의 readout head 5종을 같은 backbone과 데이터로 재학습해 비교한 통제 실험이며, head 복잡도보다 backbone 크기가 중요하다는 결론임. 텍스트 분류 중심이라 로봇과 거리가 멂</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2611.16318'>Benchmarking AI risk behaviors</a></td><td>30</td><td>1</td><td>LLM Eval</td><td>LLM의 위험 선호와 일관성을 여러 조건에서 측정하는 toolkit이며 최신 모델이 expected value 최대화에 가까워짐을 관찰함. 의사결정 성향 분석이라 로봇 직접 관련은 약함</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2611.16478'>One Model, Two Precisions: Does Disagreement Between Quantized Copies Tell You When a Small Model Is Wrong?</a></td><td>30</td><td>1</td><td>LLM Uncertainty</td><td>같은 weight의 8-bit와 저정밀 양자화 복사본 사이 불일치를 오답 점수로 쓰는 실험이며, entropy 대비 AUROC 향상이 거의 없고 Gaussian noise로도 비슷해 양자화 특이성이 없다고 보고함. 부정적 결과를 솔직히 밝힌 점은 좋으나 소형 LLM 객관식에 한정됨</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2611.16493'>ReA-Bench: Benchmarking Responsible Agent Auditing</a></td><td>30</td><td>1</td><td>Agent Safety</td><td>실제 production trajectory 기반으로 agent 감사 능력을 6단계(모순 탐지, 장문 증거 검색, 정보 누락 등)로 진단하는 ReA-Bench임. 위험 행동 탐지 관점은 failure diagnosis와 닿으나 LLM agent 안전 benchmark임</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2611.16621'>Studies on Sign Language Retrieval in Low-Resource Dictionary Settings</a></td><td>30</td><td>1</td><td>Video</td><td>ASL 사전학습 pose encoder를 6개 다른 수어에 frozen으로 적용해 one-shot 검색 정확도를 보고하고, 몸과 양손 사이 attention 차단이 최대 5.1점 올림을 보임. 저자원 수어 검색 연구라 로봇과 거리가 멂</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2611.14856'>Honest Fusion Evaluation for Cross-Domain Deepfake Detection: Leakage Audits and Tail Robustness</a></td><td>30</td><td>0</td><td>CV</td><td>deepfake 탐지에서 expert routing과 feature fusion의 이득이 fold 누수로 생긴 평가 artifact임을 보인 평가 감사 연구이며 로봇 연결은 없음</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2611.14659'>Closing the Loop: Co-Evolving EM for Irregular Time Series Generation in Lifted Representations</a></td><td>30</td><td>0</td><td>LG</td><td>불규칙 시계열 생성을 EM으로 보완하는 방법임</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2611.15053'>PhysXAI: A Theoretical Framework for Diagnosing Physical Hallucinations in Weather Foundation Models</a></td><td>30</td><td>0</td><td>LG</td><td>날씨 foundation model의 physical hallucination 진단 이론임</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2611.15062'>Probabilistic State Space Enumeration in Neural Network Computation</a></td><td>30</td><td>0</td><td>LG</td><td>신경망 연산의 확률적 상태 열거 이론임</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2611.15197'>Anytime-Valid Empirical Likelihood Inference from LLM Annotations with Adaptive Human Auditing</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM annotation에 대한 통계 추론임</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2611.15234'>Schedule-Calibrated Commitment Order in Blockwise Masked Diffusion Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>block 마스크 diffusion LM의 commit 순서 보정임</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2611.15262'>CastWorld: Benchmarking Context-Aware Agentic Time Series Forecasting Beyond Predictive Accuracy</a></td><td>30</td><td>0</td><td>LG</td><td>agentic 시계열 예측 benchmark임</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2611.15291'>Learning Rate Transfer and Feature Learning Across Depth for Constrained Spectral Optimizers: Complete Scion</a></td><td>30</td><td>0</td><td>LG</td><td>깊이 간 learning rate 전이 이론임</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2611.15965'>PhysICL: In-Context Learning of Physical Fields on Unstructured Meshes from Procedural Priors</a></td><td>30</td><td>0</td><td>LG</td><td>비정형 mesh 물리장 in-context learning임</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2611.16053'>Wayfinder: Adaptive Resource Routing from Agent Citations</a></td><td>30</td><td>0</td><td>NLP</td><td>agent citation으로 자원 routing을 함</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2611.16257'>Few-Shot Cross-Subject Neural--Image Retrieval via Stimulus-Anchored Latent Bias Calibration</a></td><td>30</td><td>0</td><td>LG</td><td>few-shot 뇌 신호 이미지 검색 보정임</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2611.16369'>Bait: Mitigating Harmful Agentic Reinforcement Learning via Probing Reward Function</a></td><td>30</td><td>0</td><td>RL</td><td>agentic RL의 유해 학습을 reward probing으로 막음. LLM 안전 주제임</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2611.16642'>Dataset Distillation via Drifting</a></td><td>30</td><td>0</td><td>CV</td><td>dataset distillation 방법임</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2611.16736'>On the Difficulty of Sequence-Level Supervised Learning for Autoregressive Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>autoregressive LM sequence-level 지도학습 난점 분석임</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2611.14910'>MuEdit: An efficient multi-task editing method towards inter-domain knowledge conflicts</a></td><td>30</td><td>0</td><td>NLP</td><td>다중 도메인 편집에서 null space 공유 축소를 Conflict Index로 재고 ordering과 동적 low-rank로 완화하는 MuEdit이며 LLM knowledge editing 한정임</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2611.14853'>Can I join you? Extended Social Force Based Model with Predictive Control and Barrier Functions for Humanoid Group Repositioning Amidst Obstacles</a></td><td>28</td><td>5</td><td>Social Nav</td><td>humanoid 그룹 재배치용 social force와 MPC 결합으로 incremental임</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2611.15524'>Reading the Table: Sim-to-Real Game State Detection for the Chef&#x27;s Hat Card Game</a></td><td>28</td><td>4</td><td>Perception</td><td>카드 게임 상태 검출 sim-to-real로 응용 중심 incremental임</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2611.16472'>RGB-D SLAM on the Edge: Benchmarking and Profiling RTAB-Map and ORB-SLAM3 on the Raspberry Pi 5</a></td><td>28</td><td>4</td><td>SLAM</td><td>RTAB-Map과 ORB-SLAM3 Raspberry Pi 벤치마킹으로 측정 보고임</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2611.16752'>AgriSense: Vision-Language Decision Support and Robotic Intervention in a Virtual Greenhouse Copy title</a></td><td>28</td><td>4</td><td>Agriculture</td><td>가상 온실 VLM 의사결정 지원 응용 시스템임</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2611.15342'>MechBench: A Domain-Specific LLM Benchmark for Parallel Mechanisms</a></td><td>28</td><td>2</td><td>NLP</td><td>parallel mechanism 지식을 묻는 LLM benchmark임. 기구학 관련하나 단순 benchmark임</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2611.17108'>LazyWeights: Decode-on-Demand Edge LLMs</a></td><td>28</td><td>2</td><td>LG</td><td>엣지 LLM 가중치 디코딩 기법으로 efficient inference이나 로봇 직접 연결 없음</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2611.15328'>Vision-Grounded Semantic Learning and Alignment for Scalable Multilingual Text-Based Person Retrieval</a></td><td>28</td><td>1</td><td>CV</td><td>다국어 text-based person retrieval용 대규모 사전학습 데이터와 언어별 인코더 정렬을 제안한 retrieval 논문으로 로보틱스와 거리가 먼 과제임</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2611.16418'>Model Distribution-Aware Multimodal Dataset Distillation</a></td><td>28</td><td>1</td><td>LG</td><td>학습 단계가 다른 모델 큐로 supervision을 줘 multimodal dataset distillation의 일반화를 높이는 MDA-DD임. 로봇과 거리가 먼 주제임</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2611.16897'>TokenStream: Multi-Subject Personalized Video Generation with Token-wise LoRA and Guided Attention</a></td><td>28</td><td>1</td><td>Video</td><td>subject 단어 토큰의 cross-attention value에만 LoRA를 거는 ToRA로 다중 subject 맞춤 비디오 생성을 하며 DreamBooth 대비 identity 0.422에서 0.467로 오름을 보임</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2611.17019'>Temporal Regularized Learning: Self-Supervised Learning Local in Space and Time</a></td><td>28</td><td>1</td><td>LG</td><td>시공간 local self-supervised 학습 규칙 제안이나 규모와 증거 제한적임</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2611.17214'>Introducing Feedback Delays to Non-Delayed Adversarial MDPs: Optimal $\sqrt S$ and $\sqrt K$ Dependencies in Tabular and Linear AMDPs</a></td><td>28</td><td>1</td><td>RL</td><td>adversarial MDP regret 이론의 최적 의존성 결과로 로봇 연관 약함</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2611.15268'>Knowledge in the Harness, Reliability in the Weights: Teacher-Free Co-Evolution of an LLM Agent</a></td><td>28</td><td>1</td><td>NLP</td><td>고객 상담 LLM agent 공진화 학습임</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2611.16264'>Label-Efficient Document-Grounded Factuality Detection via Cross-Paraphrastic Invariance Learning</a></td><td>28</td><td>1</td><td>NLP</td><td>paraphrase view 쌍과 semi-hard negative mining으로 적은 라벨에서 factuality detector를 학습하는 Siamese 방식이나 문서 사실성 검출 한정이라 로봇과 거리가 멂</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2611.14949'>RSI-PDEbench: A Benchmark for Self-Improving Agents in PDE Solving</a></td><td>28</td><td>1</td><td>LG</td><td>PDE 식 발견과 해석 과제 1,001건 벤치마크와 validation gate가 있는 recursive self-improving 하네스 RSI-PDE를 제안함, 과학 계산 agent 응용임</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2611.15838'>Before AI Agents Negotiate for Us: A Competitive Tournament of Rule-Based, Search, Optimization, Learned, and Language-Model Negotiators Under Scarcity</a></td><td>28</td><td>1</td><td>Multi-Agent</td><td>규칙, 탐색, 최적화, imitation, RL, LLM 협상 agent 9종을 Gale-Shapley 매칭 시장에서 동시에 겨룬 tournament 연구임. 평가 설계는 꼼꼼하나 화물 중개 도메인이라 로봇 관련성 낮음</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2611.16485'>Contain, Conform, Compare (Extended Version): A Red-Teamed Evaluation Kit for Small Coding Agents and the Full Record of Its Experiments</a></td><td>28</td><td>1</td><td>Agent Eval</td><td>소형 coding agent 평가용 drydock-eval 키트와 9,660건 실행 기록을 공개하며, prompt 변경 효과가 사전 등록 실험에서 확인되지 않았음을 보임. 재현성 태도는 좋으나 coding agent 평가 인프라라 로봇과 거리가 멂</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2611.15311'>Arbor: When Labels Are Not Coarsened at Random</a></td><td>28</td><td>0</td><td>CV</td><td>taxonomy 병합으로 생긴 coarse label에서 novel class를 가상 클래스와 logistic gate로 모델링하는 Arbor로 iNaturalist-2019 novel 정확도를 46%에서 68%로 올림</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2611.16451'>HIFC-IQA: Train-Free Cross-Domain Image Quality Assessment via Dual-Process Cognition</a></td><td>28</td><td>0</td><td>CV</td><td>dual-process 인지에서 착안해 학습 없이 cross-domain 영상 품질을 평가하는 HIFC-IQA임. 로보틱스 관련 없음</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2611.14697'>Beyond Row-Level Prediction: Evaluating and Learning Composition for Reusable Table Representations</a></td><td>28</td><td>0</td><td>LG</td><td>table embedding 평가와 학습임</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2611.14750'>From Nodes to Pixels: Topological and Structural Two-View Graph Imaging</a></td><td>28</td><td>0</td><td>LG</td><td>그래프를 이미지로 바꿔 입력하는 방법임</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2611.15004'>A Cardiorespiratory Foundation Model Pretrained on Ten Physiological Signals for Perioperative and Critical Care</a></td><td>28</td><td>0</td><td>LG</td><td>생리 신호 foundation model임</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2611.15073'>When Does Causality Help in Multivariate Time-Series Anomaly Detection?</a></td><td>28</td><td>0</td><td>LG</td><td>시계열 이상 탐지에서 causality 효과를 분석함</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2611.15300'>Sharp Covering-Number Bounds for Feedforward ReLU Networks via Parameter Symmetries</a></td><td>28</td><td>0</td><td>LG</td><td>ReLU 네트워크 covering number 이론임</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2611.15653'>A Mechanistic Interpretability Study of an Astronomy Foundation Model</a></td><td>28</td><td>0</td><td>LG</td><td>천문 foundation model 해석 연구임</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2611.15707'>Efficient Knowledge Transfer in Federated Bayesian Optimization through Neural Network Surrogates</a></td><td>28</td><td>0</td><td>LG</td><td>federated Bayesian optimization 지식 전이임</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2611.15895'>Your Hypergradient is Skewed: Antithetic Neumann Estimation for Bilevel Optimization</a></td><td>28</td><td>0</td><td>LG</td><td>bilevel optimization hypergradient 추정임</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2611.15990'>Characterizing the Edge of Stability in Variational Training Without Priors</a></td><td>28</td><td>0</td><td>LG</td><td>variational 학습의 edge of stability 분석임</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2611.16184'>Flow-CAD: Flow Matching for Contextual Anomaly Detection and Explanation in Tabular Data</a></td><td>28</td><td>0</td><td>LG</td><td>flow matching 표 데이터 이상 탐지임</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2611.16190'>When can an interpretability claim be trusted? Stability and certification of feature dimensionality, ridge leverage and the feature recovery rate</a></td><td>28</td><td>0</td><td>LG</td><td>interpretability 주장의 안정성과 인증임</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2611.15735'>Where Is Uncertainty Observed? A Mechanistic Understanding of Uncertainty Quantification in LLMs</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM 불확실성 정량화의 mechanistic 이해임</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2611.14769'>Leaderboard Hacking: Preference-Based Model Evaluations are Vulnerable to Manipulation</a></td><td>28</td><td>0</td><td>LG</td><td>Arena식 Bradley-Terry 리더보드가 전략적 투표, 프롬프트, 모델 삽입으로 최대 45위까지 조작됨을 보임, 평가 취약성 분석이며 로봇과 무관함</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2611.16935'>Universal Infectious Disease Forecasting with Mantis 2</a></td><td>28</td><td>0</td><td>Time Series</td><td>시뮬레이션 데이터와 관측 데이터의 비율을 바꿔 전염병 예측 foundation model Mantis 2를 학습했고, 지역 이력이 적을 때 시뮬레이션 비중이 큰 학습이 유리함을 보임. sim 데이터 활용 관찰은 흥미로우나 로봇과 거리가 멂</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2611.15610'>Contrastive Bootstrap Representation Learning for Label-Efficient Agricultural Image Classification</a></td><td>27</td><td>1</td><td>CV</td><td>농업 이미지 분류에서 contrastive와 bootstrap 신호를 한 경로에서 쓰는 CBRL의 label-efficient 사전학습 연구임. 로봇과 거리 있음</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2611.15443'>SPARC: RoboCup Standard Platform for Autonomous Rescue Competition with Initial Datasets, Software, and Simulation Environments</a></td><td>26</td><td>3</td><td>Competition</td><td>RoboCup rescue 대회 소개와 데이터셋 보고임</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2611.15941'>Lang-SVG: Hierarchical Image Vectorization with Language Priors</a></td><td>26</td><td>1</td><td>CV</td><td>SVG primitive를 의미 label이 붙은 트리로 조직해 객체-부분 계층을 맞추는 Lang-SVG 이미지 벡터화임. 로봇과 거리가 먼 과제임</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2611.16269'>FlowIR: Depth-driven Rectified Flow for Resolving Thermal Ambiguity in Infrared Super-Resolution</a></td><td>26</td><td>1</td><td>CV</td><td>pseudo-3D depth를 rectified flow에 넣어 열 방출원 모호성을 푸는 적외선 super-resolution FlowIR임. 복원 과제 증분임</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2611.14804'>GenPFN: An In-Context Tabular Foundation Model Approach for Augmenting Small Datasets in Engineering</a></td><td>26</td><td>1</td><td>LG</td><td>TabPFN 분류기 gradient로 desired 설계 후보를 생성해 공학 소규모 데이터를 증강하는 training-free GenPFN이며 14개 공학 문제 적용임</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2611.15094'>A frontier machine intelligence for human neuroimaging</a></td><td>26</td><td>1</td><td>Multimodal</td><td>약 100만 건 임상 신경영상으로 학습한 vision-language 모델 Neuro-VL이 진단, 보고서 생성, 경과 비교를 수행함, 의료 영상 응용이며 로봇과 거리가 있음</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2611.15515'>Incentive-Responsive Agents: A Principal-Agent Framework, Metric Suite, and Runtime Architecture for Long-Lived Personal AI Agents</a></td><td>26</td><td>1</td><td>LG</td><td>장기 개인 agent에 principal-agent 모델로 runtime 인센티브 계층을 제안하고 240회 실험에서 prompt 수준 유인은 효과가 없고 runtime 자원 할당이 어려운 과제를 0.60에서 1.00으로 올림, 이론 틀은 있으나 로봇과 거리가 있음</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2611.15760'>Image Deblending with Diffusion Models</a></td><td>26</td><td>0</td><td>CV</td><td>합성된 이미지를 두 원본으로 분리하는 deblending을 diffusion posterior sampling의 joint inverse problem으로 풂. 로봇과 무관함</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2611.16413'>RICapBench: A Fine-Grained Visual Understanding Benchmark Dataset for Vision-Language Models in Remote Sensing</a></td><td>26</td><td>0</td><td>Multimodal</td><td>원격탐사 fine-grained 이해를 평가하는 RICapBench 벤치마크로 로봇과 무관함</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2611.15638'>Helping Hand: A Continuum Robotic Grasper for Traction in Single-Channel Endoscopic Submucosal Dissection</a></td><td>25</td><td>3</td><td>Surgical</td><td>내시경 ESD continuum grasper 하드웨어 설계임</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2611.16742'>Fog-FWL: A Large-Scale Full-Waveform LiDAR Dataset for Recovering Fog-Hidden Objects</a></td><td>25</td><td>2</td><td>3D Vision</td><td>안개 속 물체 복원을 위한 full-waveform LiDAR 실측 7,527 프레임과 합성 12,000 프레임 데이터셋이며 방법 기여는 없음</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2611.16925'>Report of the 8th LSVOS Challenge: Mobile Unified Multimodal Understanding</a></td><td>25</td><td>2</td><td>Multimodal</td><td>0.5B 파라미터 제한에서 tagging, open-vocabulary detection, captioning을 함께 푸는 ECCV 챌린지 결과 보고서이며 상위 팀은 모두 Florence-2-base 기반임</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2611.14608'>FreeDeshadow: Shadow Removal for User-Specified Objects With Multimodal Prompts</a></td><td>25</td><td>1</td><td>CV</td><td>사용자가 지정한 물체의 그림자만 지우는 prompt 기반 shadow removal과 15만 장 규모 데이터셋을 만들었으나 로봇 연결은 거의 없는 이미지 편집 연구임</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2611.15025'>Federated Class Incremental Learning: A Pseudo Feature Based Approach Without Exemplars</a></td><td>25</td><td>1</td><td>LG</td><td>federated class incremental learning에서 prototype으로 만든 pseudo feature로 망각을 줄이는 CIFAR-100 중심의 작은 개선임</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2611.17146'>HiVE-VQA: Hierarchical Interaction via Volumetric Embedding for Video Quality Assessment</a></td><td>25</td><td>1</td><td>Video</td><td>고정된 V-JEPA 2.1의 여러 층 token을 3D conv head로 융합해 영상 품질 평가를 하는 방법이며 로봇 연결은 약함</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2611.17109'>Near-Optimal Regret for Oracle-Efficient Adversarial Contextual Bandits</a></td><td>25</td><td>1</td><td>LG</td><td>contextual bandit regret 이론 결과로 로보틱스 연관 약함</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2611.17141'>ISLA: A Coordinate-Free, Measure-Weighted Transformer for Boundary-Driven PDEs</a></td><td>25</td><td>1</td><td>LG</td><td>좌표 불변 transformer PDE surrogate로 로보틱스 무관함</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2611.15130'>Read Once, Answer Many: Parallel Prompting for Shared-Context LLM Inference</a></td><td>25</td><td>1</td><td>NLP</td><td>공유 context LLM 병렬 prompting 추론 효율화임</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2611.15341'>Janus-MOPD: Tracing the Student Learning Dynamics in Multi-Teacher On-Policy Distillation</a></td><td>25</td><td>1</td><td>NLP</td><td>multi-teacher on-policy distillation 학습 동역학 분석임</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2611.16223'>We Are What We Remember: Mental-State-Driven Memory for Long-Term Character Dialogue</a></td><td>25</td><td>1</td><td>NLP</td><td>mental-state 기반 캐릭터 대화 장기 메모리임</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2611.16270'>SMIC: Shared Multiscale Input-Reference Conditioning across Transformer Layers for Natural Language Inference</a></td><td>25</td><td>1</td><td>NLP</td><td>모든 Transformer layer에 공유 multiscale reference를 주입해 NLI의 lexical 민감도를 줄이는 구조이며 ANLI 중심의 작은 모듈 변경임</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2611.14765'>SynthCorp: A Platform for Creating Benchmarks for Data Agents</a></td><td>25</td><td>1</td><td>LG</td><td>비즈니스 이벤트 시뮬레이션으로 data estate와 gold program이 있는 data agent 벤치마크를 생성하는 SynthCorp이며 기업 데이터 에이전트 평가 한정임</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2611.15006'>EvoX: Rethinking the Agent Harness as a Runtime Policy</a></td><td>25</td><td>1</td><td>LG</td><td>Rust 기반 agent runtime EvoX가 Action Realization 등 세 기제로 하네스를 operational policy로 다루며 691개 쌍에서 56.2% 성공률을 얻음, 엔지니어링 위주이고 평균 대비 이득이 3.0포인트임</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2611.15831'>NIBench: benchmarking autonomous AI agents for execution, skill evolution and scientific judgment in neuroimaging</a></td><td>25</td><td>1</td><td>Agent Benchmark</td><td>신경영상 분석 agent의 workflow 재구성, skill distillation, 과학적 판단을 평가하는 NIBench이며 LLM 19종을 비교함. 의료 영상 도메인 benchmark라 로봇과 거리가 멂</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2611.16492'>Time and Space: A Dual-Axis, Evidence-Grounded Context Substrate for Personal Agents</a></td><td>25</td><td>1</td><td>Agent Memory</td><td>개인 agent용 context를 event time, validity interval, 관계 그래프의 두 축으로 표현하는 STC 틀을 제안하나 분석 계층은 구현하지 못했고 정량 평가가 약함. 로봇과 거리가 멂</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2611.16937'>S1-Evo: Experience-Guided Evidence Competition Attacks on Typed System-1 Decision Models</a></td><td>25</td><td>1</td><td>Agent Security</td><td>S1-Evo는 typed System-1 decision model의 option 경쟁과 margin 피드백을 이용해 경험 카드로 교란을 만드는 공격이며 jev-1.14에서 평균 공격 성공률 71.99%를 보임. LLM agent 보안 도메인이고 로봇과 무관함</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2611.14941'>Reality Perception Gap: Are AI-Manipulated Video Detectors Ready for the Real World?</a></td><td>25</td><td>0</td><td>Video</td><td>18개 AI 영상 탐지기가 repost 압축을 거친 1만 개 영상에서 1% 오탐 기준 15% 이하만 잡음을 보인 benchmark이며 로봇과 무관함</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2611.15514'>Real Pairs Are Not Enough: Physically Anchored Supervision for Volumetric CT Super-Resolution</a></td><td>25</td><td>0</td><td>CV</td><td>CT super-resolution에서 real pair를 두 역할로 분리하는 physically anchored 학습을 제안한 의료영상 논문임</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2611.14760'>Graph Label Alignment: A Diagnostic Atlas for Graph Classification</a></td><td>25</td><td>0</td><td>LG</td><td>graph classification benchmark 진단임</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2611.14956'>Binding Mode Matters: Hotspot-Aware Drug Discovery via Explorative Preferences</a></td><td>25</td><td>0</td><td>LG</td><td>약물 탐색 생성 모델임</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2611.15067'>CoLaX: Context-Aware Local Explanations for Time Series Classification</a></td><td>25</td><td>0</td><td>LG</td><td>시계열 분류 설명 방법임</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2611.15247'>Protected Unbiased Sparsification: A Sharp Loewner Curve</a></td><td>25</td><td>0</td><td>LG</td><td>sparsification 이론임</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2611.15413'>MORA: Correcting Time Series Forecasts with Coarse Future Signals</a></td><td>25</td><td>0</td><td>LG</td><td>시계열 예측 보정임</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2611.15671'>The Noise Floor of a Quantization Comparison: Engine, restart, batch and kernel drift, measured against 8-bit and 4-bit effects in two decision models</a></td><td>25</td><td>0</td><td>LG</td><td>양자화 비교의 noise floor 측정임</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2611.15771'>SAME: Semantic Watermark Embedding for Open-Source Large Pretrained Models</a></td><td>25</td><td>0</td><td>LG</td><td>대형 사전학습 모델의 watermark 삽입임</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2611.16003'>Fit-LRP: Fitting Linear Relaxations to Polytopes for Neural Network Verification over Non-Convex Regions</a></td><td>25</td><td>0</td><td>LG</td><td>신경망 검증 linear relaxation 개선임</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2611.16031'>Robustness Within a Fairness Budget: Parity Frontiers and Equal-Opportunity Reversal</a></td><td>25</td><td>0</td><td>LG</td><td>공정성과 adversarial robustness trade-off 분석임</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2611.16063'>Vocabulary-Free Next-Event Prediction on Temporal Graphs</a></td><td>25</td><td>0</td><td>LG</td><td>temporal graph 다음 사건 예측임</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2611.16073'>Agentic Computational Algebra</a></td><td>25</td><td>0</td><td>NLP</td><td>AI agent로 computational algebra 문제 풀이에 적용함</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2611.16097'>A Matching Lower Bound for Online Smooth Calibration</a></td><td>25</td><td>0</td><td>LG</td><td>online smooth calibration 하한 이론임</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2611.17230'>Two mathematical models of knowledge distillation</a></td><td>25</td><td>0</td><td>LG</td><td>knowledge distillation의 수학 모델 분석으로 로봇 무관함</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2611.14661'>Abstention Is Not Threshold Compliance: Stated Scoring Rules in Open Language Models</a></td><td>25</td><td>0</td><td>NLP</td><td>스코어링 규칙 명시에 따른 LLM abstention 평가임</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2611.15267'>A Closer Look at Language Model Introspection: Probing Information and Reporting</a></td><td>25</td><td>0</td><td>NLP</td><td>LM introspection 정보와 보고 탐침 분석임</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2611.15717'>Outside the Purview of the Reward: Capability Drift in Multilingual Post-Training</a></td><td>25</td><td>0</td><td>NLP</td><td>다국어 post-training capability drift 분석임</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2611.16064'>Privileged Information Does Not Guarantee Privileged Guidance: Auditing On-Policy Self-Distillation for Reasoning Models</a></td><td>25</td><td>0</td><td>NLP</td><td>on-policy self-distillation 감사 분석임</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2611.15574'>RipBench: A Unified Benchmark for Multi-Level Rip Current Detection, Classification and Segmentation</a></td><td>24</td><td>1</td><td>CV</td><td>이안류 검출·분류·분할을 통합 평가하는 RipBench 벤치마크 논문으로 로보틱스 관련 낮음</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2611.17059'>Capacity-Constrained Delayed Feedback for Online Conformal Risk Control</a></td><td>24</td><td>1</td><td>LG</td><td>지연 feedback 하 online conformal risk control 이론으로 로봇 연결 약함</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2611.16224'>Disentangled Embedding Optimization for Diffusion-Based Dataset Distillation</a></td><td>24</td><td>0</td><td>CV</td><td>dataset distillation에서 diffusion 입력 embedding을 disentangle해 최적화하는 방법임. 로봇과 무관한 분류 효율화임</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2611.17053'>Evaluating Pretrained Language Semantics for Structured EHR Prediction Tasks</a></td><td>24</td><td>0</td><td>LG</td><td>EHR 이벤트를 자연어 설명으로 바꿔 Mistral-7B를 continued pretraining과 LoRA로 환자 encoder로 쓰는 tEHR이며 MIMIC-IV 의료 예측 응용임</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2611.15475'>Loyalty Capture: Reporting Relationships and Structural Sycophancy in Frontier AI Models</a></td><td>24</td><td>0</td><td>LG</td><td>보고 관계만으로 모델이 상사 보너스 목표에 맞춰 투자 삭감을 권하는 loyalty capture를 보인 sycophancy 행동 분석이며 로봇과 무관함</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2611.14762'>Open-Source Transtibial Prosthetic Bypass Preserving Joint Alignment: Gait Learning and Kinematic Evaluation</a></td><td>22</td><td>3</td><td>Prosthetics</td><td>의족 bypass 하드웨어와 보행 평가로 우선 주제와 거리 있음</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2611.17190'>Consensus Capture in Reference-Based UAV Video Stabilization: A Benchmark on Dynamic Urban Scenes</a></td><td>22</td><td>2</td><td>CV</td><td>드론 영상 안정화에서 움직이는 차량이 homography 추정을 끌어당기는 consensus capture를 측정하는 벤치마크이며 로봇 응용은 간접적임</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2611.16655'>MuViRL: Multimodal View-Invariant Visual Speech Representation Learning via Calibrated View Aggregation</a></td><td>22</td><td>1</td><td>Multimodal</td><td>3D Gaussian view synthesis와 view 효용 기반 aggregation으로 시점 불변 visual speech 표현을 학습하는 방법으로 로봇 연결은 약함</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2611.16871'>DPA: Decentralized Primal Averaging with Quasi-Global Momentum for Highly Heterogeneous Data</a></td><td>22</td><td>1</td><td>LG</td><td>decentralized 학습 optimizer 개선으로 incremental임</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2611.14700'>Probe What-If Worlds Before You Ship: Persona Simulation for Real-World Decision Making</a></td><td>22</td><td>1</td><td>NLP</td><td>persona 시뮬레이션으로 의사결정 검증하는 응용임</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2611.15426'>SimRec: Learning to Search, Ask, and Recommend from Simulated Interaction</a></td><td>22</td><td>1</td><td>NLP</td><td>시뮬레이션 상호작용으로 추천 agent를 학습함</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2611.16477'>Where in the Input Does a One-Pass Decision Encoder Look?</a></td><td>22</td><td>1</td><td>NLP</td><td>512 토큰 window 밖 evidence에서 one-pass 모델 정확도가 추측 수준으로 떨어짐을 진단한 분석이며 합성 문서와 단일 backbone 한정이라 일반성이 낮음</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2611.14889'>Can an AI Agent Be Epistemically Akratic? Higher-Order Evidence &amp; the Limits of Self-Correction</a></td><td>22</td><td>1</td><td>AI</td><td>자기 평가와 결론의 일치를 강제해도 self-correction이 나아지지 않는다는 철학적 논증이며 실험이 없음</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2611.15189'>WordInferBench: Can Agents Infer How to Edit from Word Document Context?</a></td><td>22</td><td>1</td><td>LG</td><td>Word 문서 편집에서 문맥으로 속성을 추론해야 하는 WordInferBench를 만들어 Claude Code 성공률이 descriptive 62.9%에서 inferential 40.7%로 내려감을 보임, 도메인 한정 벤치마크임</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2611.16609'>A Dual-Branch Graph and Convolutional Network for Interpretable Movement EEG Classification</a></td><td>22</td><td>1</td><td>BCI</td><td>61개 EEG 전극을 해부학적 영역 graph로 묶는 LGGNet식 branch와 EEGNet식 convolution branch를 결합해 팔 움직임을 분류하며 F1 0.74를 얻음. 소규모 dataset 중심의 incremental 모델이고 로봇 제어 연결은 약함</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2611.14851'>Paired Geometric Supervision for Generalizable Deepfake Detection</a></td><td>22</td><td>0</td><td>CV</td><td>DINOv3 위에 짝지은 real/fake의 직교 분해와 hyperspherical 정규화를 얹은 deepfake 탐지 incremental 개선임</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2611.14898'>From Pixels to Prompts: Physics-Guided Language Enhancement for AI-Generated Image Detection</a></td><td>22</td><td>0</td><td>CV</td><td>Laplacian 분산 같은 물리 특징 5개를 문장으로 만들어 CLIP LoRA에 넣는 AI 생성 이미지 탐지 기법으로 incremental임</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2611.15149'>From Concepts to Interactions: Dynamic Graph Semantic Recomposition for Safe Visual Generation</a></td><td>22</td><td>0</td><td>Generative</td><td>생성 중 text-visual 상태로 semantic interaction graph를 갱신해 맥락별로 유해 개념만 억제하는 DGSR로 T2I와 T2V 안전 정렬을 다룸</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2611.15418'>ChartGalaxy++: A Richly Annotated Dataset for Chart Understanding and Generation</a></td><td>22</td><td>0</td><td>CV</td><td>infographic chart 21만 건에 계층·공간 관계 주석을 붙인 데이터셋 논문으로 로보틱스 관련 없음</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2611.16236'>ATune: Unsupervised Photo Retouching Through Image-Editor Controls</a></td><td>22</td><td>0</td><td>CV</td><td>좋은 사진만으로 열화 쌍을 만들어 편집 컨트롤 값을 예측하는 비지도 photo retouching ATune임. 로보틱스 관련 없음</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2611.14748'>UniPipe: Unified Inference Serving and Fine-Tuning for Deadline-Constrained DNN Surrogate Workflows</a></td><td>22</td><td>0</td><td>LG</td><td>과학 workflow용 DNN surrogate 서빙 시스템임</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2611.15155'>PRELUDE: Separating Common Components from Target-Specific Dependencies for Multivariate Time Series Forecasting</a></td><td>22</td><td>0</td><td>LG</td><td>다변량 시계열 예측임</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2611.15224'>DGPExplainer: Generating Prototype Sequence Explanations for Dynamic Graph Neural Networks</a></td><td>22</td><td>0</td><td>LG</td><td>동적 GNN 설명 방법임</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2611.15523'>An Approach to Hinton&#x27;s Mother-Child Proposal: Neural Networks Learning and Preserving Care in a Finite World</a></td><td>22</td><td>0</td><td>LG</td><td>Hinton의 maternal instinct 제안을 신경망으로 구현해 봄. 개념 수준임</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2611.15529'>One Hierarchy, Many Sports: Hierarchy-Aligned Multi-Task Learning for Next-Shot Prediction</a></td><td>22</td><td>0</td><td>LG</td><td>라켓 스포츠 다음 샷 예측임</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2611.15668'>Beyond Reweighting: Certified Improvements from New Transitions in Discrete MCMC</a></td><td>22</td><td>0</td><td>LG</td><td>discrete MCMC 이론임</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2611.15750'>Sensitivity-Aware Surrogate Modeling with Random Feature Expansions</a></td><td>22</td><td>0</td><td>LG</td><td>random feature surrogate 모델링임</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2611.15778'>From Link Prediction to Linear Community Detection: A Finite-Sample Guarantee for Graph Pretraining</a></td><td>22</td><td>0</td><td>LG</td><td>graph pretraining 이론 보장임</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2611.16038'>Continual Event Recognition for Autonomous Optical Network Monitoring</a></td><td>22</td><td>0</td><td>LG</td><td>광 네트워크 continual event recognition임</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2611.16301'>LoCoJAX: Host-Local Coordination for Small-Model RL on TPUs</a></td><td>22</td><td>0</td><td>RL</td><td>TPU에서 작은 LM RL 조정 시스템임</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2611.16461'>Helgason-Fourier Random Features for Scalable Hyperbolic Latent Variables</a></td><td>22</td><td>0</td><td>LG</td><td>hyperbolic latent variable random feature임</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2611.17030'>Similar but Not Redundant: Embedding-Gated Refinement for High-Granularity Topic Models</a></td><td>22</td><td>0</td><td>NLP</td><td>embedding 유사도로 후보를 뽑고 LLM이 진짜 중복만 합치는 EGIM으로 고해상도 topic model을 정제하는 방법이며 특허와 법률 코퍼스에 한정됨</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2611.17332'>ArchSpace: Recording, Reviewing, and Referencing LLM Architecture Research</a></td><td>22</td><td>0</td><td>LG</td><td>LLM 구조 연구를 기록, 리뷰, 참조하는 ArchSpace 플랫폼과 scaling law 기반 소규모 실험 예측이며 커뮤니티 인프라 제안임</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2611.16300'>SAGE-QA: Semantic-Aware, Grounded Evaluation for Closed-Context Question Answering on SQuAD 2.0</a></td><td>22</td><td>0</td><td>NLP</td><td>SQuAD 2.0에서 Exact Match의 한계를 보완하는 의미 동등성 점수 SAGE-QA와 LLM 평가를 제안하고 fine-tuning 효과를 측정함. 평가 지표 개선 수준이며 로봇과 무관함</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2611.16445'>FPSRG: Heterogeneous User Simulation First-Person Post-Training and Multidimensional Semantic Response Grids</a></td><td>22</td><td>0</td><td>LLM Simulation</td><td>FPSRG는 사용자 시뮬레이션용으로 first-person post-training 후 control vector 조합을 측정해 catalog로 저장하는 방법이며 5축 target 커버리지 92.2퍼센트를 보임. 로봇과 무관한 persona 제어 연구임</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2611.15743'>Robot-Induced Bias in Movement Smoothness Metrics for Rehabilitation: Quantification and Correction in Simulation</a></td><td>20</td><td>3</td><td>Rehab</td><td>재활 로봇의 smoothness 지표 편향 보정으로 우선 주제와 거리 있음</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2611.15125'>Toward Cross-Rubric Surgical Skill Assessment via Joint Embedding Prediction</a></td><td>20</td><td>1</td><td>Video</td><td>수술 영상의 숙련도를 rubric 문장 embedding 경로에 사영해 점수화하는 PRA를 AIxSuture와 JIGSAWS에서 평가한 의료 영상 연구임</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2611.17172'>SpotDiff: A Plug-and-Play Framework for Zero-Shot Change Detection in Remote Sensing Imagery</a></td><td>20</td><td>1</td><td>CV</td><td>DINOv3, AnyUp, SAM 3를 조합한 training-free 원격탐사 zero-shot 변화 검출이며 foundation model 조립 위주로 로봇과 거리거리가 멀음</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2611.16623'>DySR-GNN: Dynamic Sensor-Relationship Graph Neural Network for Root Cause Analysis in Automotive HiL Multivariate Time Series</a></td><td>20</td><td>1</td><td>LG</td><td>자동차 HiL 근본 원인 분석 GNN이며 로봇과 거리가 있는 예측 문제임</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2611.14774'>An LLM Is All You Need: Data-Efficient Adaptation to Full-Duplex, Word-Level Spoken Dialogue</a></td><td>20</td><td>1</td><td>NLP</td><td>full-duplex 음성 대화 LLM 적응으로 로봇 연관 약함</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2611.14925'>ToolTurns: Benchmarking LLM Agents in Multi-Turn Dialogue</a></td><td>20</td><td>1</td><td>NLP</td><td>multi-turn 대화 tool 사용 benchmark임</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2611.16267'>Causals: An Open Knowledge Graph for Research on Causal Reasoning</a></td><td>20</td><td>1</td><td>Knowledge Graph</td><td>뉴스에서 만든 노드 36만 개 규모의 causal reasoning용 지식 그래프 Causals를 공개한 데이터셋 논문임. 금융 뉴스 도메인이라 로봇과 무관하고 방법 기여도 작음</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2611.16561'>SPARC: Accurate Photonic Matrix Multiplication via Representative Vectors</a></td><td>20</td><td>1</td><td>Hardware</td><td>SPARC는 유사한 activation 벡터 그룹의 대표 벡터를 디지털로 정밀 계산하고 잔차만 photonic 가속기에 넘겨 양자화와 analog noise 영향을 줄임. 광 가속기 하드웨어 주제라 로봇과 거리가 멂</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2611.16647'>InertiaMPDD: Multimodal Personalized Depression Detection via Emotional Inertia-Inspired Dynamics Modeling</a></td><td>20</td><td>1</td><td>Multimodal</td><td>InertiaMPDD는 건강한 사람의 다음 상태 패턴을 world model 유사 latent predictor로 학습해 기준 이탈을 우울증 지표로 쓰는 멀티모달 모델임. 임상 응용 도메인이고 world model 표현은 이름만 빌린 수준이라 로봇과 거리가 멂</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2611.15146'>Reframing Video Inverse Tone Mapping as Blind Posterior Inference via Latent Luminance Supervision</a></td><td>20</td><td>0</td><td>Video</td><td>SDR 영상을 HDR로 바꿀 때 video diffusion latent의 log-luminance에 expectile 손실을 걸어 밝기 편향을 줄이는 영상 복원 연구임</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2611.15601'>Cat Royale Comprehensive Dataset: A Dataset for Pose Detection, Segmentation, Animal Action Recognition and Scene Understanding</a></td><td>20</td><td>0</td><td>CV</td><td>고양이 500시간 영상으로 pose·분할·행동 인식 주석을 만든 데이터셋 논문으로 로봇과 무관함</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2611.15652'>Taming Neural Fields with a Frequency-Lipschitz Curriculum for Sparse-View CT Reconstruction</a></td><td>20</td><td>0</td><td>CV</td><td>sparse-view CT에서 neural field의 고주파 노출 시점을 frequency-Lipschitz curriculum으로 제어하는 의료영상 복원 논문임</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2611.16373'>Description-Guided CLIP Adaptation with Local Evidence Calibration for Few-Shot Plant Disease Recognition</a></td><td>20</td><td>0</td><td>CV</td><td>CLIP에 질병 설명과 국소 증거 보정을 적용한 few-shot 식물 병해 인식 논문으로 로봇과 무관함</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2611.14894'>Machine Learning Moment Closure for the Boltzmann Transport Equation: Enforcing Hyperbolicity</a></td><td>20</td><td>0</td><td>LG</td><td>Boltzmann 방정식 moment closure 학습임</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2611.15162'>Stealthy, High-Impact False Data Injection Attacks in Smart Grid Using Physics-Constrained GAN</a></td><td>20</td><td>0</td><td>LG</td><td>스마트 그리드 공격 생성임</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2611.15427'>Overcoming the Resolution Limit: Significance-Aware Regularization for Intersectional Fairness</a></td><td>20</td><td>0</td><td>LG</td><td>intersectional fairness 정규화임</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2611.15566'>Observations Drift, Structures Remain: Structural Pretraining with Time Alignment for Electromagnetic Signals</a></td><td>20</td><td>0</td><td>LG</td><td>전자기 신호 사전학습임</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2611.15609'>GLCR: Global-Local Collaborative Routing for Multi-Task Electromagnetic Signal Processing</a></td><td>20</td><td>0</td><td>LG</td><td>전자기 신호 multi-task routing임</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2611.15718'>Orbit: An Evidence-Grounded Benchmark for Evaluating LLMs on IT Operations Reasoning</a></td><td>20</td><td>0</td><td>NLP</td><td>IT 운영 추론 LLM benchmark임</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2611.16027'>A Unified Interpretable Semantic Framework for Multi-Modal Fiber Sensing Under Data Scarcity</a></td><td>20</td><td>0</td><td>LG</td><td>광섬유 센싱 해석 프레임워크임</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2611.16514'>Learning Temporal Dynamics with Derivative Representations for Time Series Forecasting</a></td><td>20</td><td>0</td><td>LG</td><td>시계열 예측 미분 표현임</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2611.16678'>Edge-Gradient Augmentation under Reinforcement Learning for Temporal Graph</a></td><td>20</td><td>0</td><td>LG</td><td>temporal graph 링크 예측 augmentation임</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2611.17303'>Towards a Theory of Learnability via Debate</a></td><td>20</td><td>0</td><td>LG</td><td>debate 기반 learnability 이론으로 무관함</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2611.16228'>Indic-Task Gains and Regressions after Reinforcement Learning</a></td><td>20</td><td>0</td><td>NLP</td><td>Indic 과제 RL 후 이득과 퇴행 분석임</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2611.16359'>IsharaBART: An efficient BART-Based Framework for Low-Resource Bangla Sign Language Translation</a></td><td>20</td><td>0</td><td>NLP</td><td>BART 기반 방글라 수화 gloss-문장 양방향 번역과 1,000쌍 데이터 증강이 기여이며 로봇과 무관한 저자원 번역 응용임</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2611.17128'>Parameter-Efficient Conciseness Adaptation: Differentiable Length Control for Concise Clinical Reasoning in Smaller Language Models</a></td><td>20</td><td>0</td><td>NLP</td><td>EOS 확률을 token budget 초과 시 높이는 미분 가능한 항을 QLoRA SFT에 더해 임상 답변 길이를 72.8% 줄임, 소형 모델 임상 응용임</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2611.17280'>Synthesis Smuggling: Maliciously Hiding Inferred Personal Attributes in LLM Outputs</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM이 사용자 성별과 나이를 추론해 보이지 않는 문자나 단어 선택으로 출력에 숨기는 Synthesis Smuggling 위협 모델 시연이며 보안 쪽 주제임</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2611.14928'>Provably Optimal HBT Legalization in Seconds: Certified Optima Reveal Where the Headroom Really Lies</a></td><td>20</td><td>0</td><td>LG</td><td>3D IC HBT legalization에 정확한 GEO-Exact 솔버와 dual certificate를 붙여 RL legalizer 보고 이득이 과대일 수 있음을 보임, 칩 설계 영역이라 로봇과 무관함</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2611.15097'>GuardianAgentFlow: Multi-Agent Coordination for Web Privacy Protection</a></td><td>20</td><td>0</td><td>LG</td><td>외부로 나가는 웹 요청을 release contract로 중재하는 multi-agent 프라이버시 보호 GuardianAgentFlow이며 웹 에이전트 응용임</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2611.16460'>Fine-Tuned Small Language Model for Synthetic Clinical Data Generation and Predictive Healthcare Analytics</a></td><td>20</td><td>0</td><td>NLP</td><td>Phi-2를 QLoRA로 MedQuad에 fine-tuning해 합성 생체신호 데이터를 만들고 LSTM 정확도를 89.0에서 93.7퍼센트로 올림. 특정 dataset fine-tuning 위주의 incremental 연구임</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2611.14846'>Open Challenges and Opportunities in Human-Agent Systems</a></td><td>18</td><td>2</td><td>Embodied AI</td><td>AAMAS 커뮤니티의 human-agent 시스템 서베이로 ToM, inverse planning, shared autonomy 등을 정리한 포지션 글이며 새 방법이나 실험이 없음</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2611.16724'>What Limits Thermal Infrared Drone Detection? A Cross-Dataset Benchmark Analysis</a></td><td>18</td><td>1</td><td>CV</td><td>열화상 드론 검출 데이터셋의 artifact를 분류하고 YOLO 일반화를 교차 데이터셋으로 분석한 감시용 벤치마크 연구임</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2611.15051'>A Time-Frequency-Condition Multimodal Fusion Foundation Model for Universal Rotating-Machinery Fault Diagnosis under Multi-Element Heterogeneous Scenarios</a></td><td>18</td><td>1</td><td>LG</td><td>회전 기계 고장 진단 foundation model로 응용 중심임</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2611.14821'>From Classification to Generation: Vision-Language Models for Roman Imperial Coin Description</a></td><td>18</td><td>0</td><td>Multimodal</td><td>Qwen3-VL을 LoRA로 로마 동전 명문 전사와 도상 설명에 맞춘 특정 dataset fine-tuning 응용 연구임</td></tr>
<tr><td>486</td><td><a href='https://arxiv.org/abs/2611.15614'>Learning-Based Interpolation of Detector Gaps in Photon-Counting X-ray Imaging</a></td><td>18</td><td>0</td><td>CV</td><td>광자계수 X선 검출기 gap을 WGAN-GP와 Pix2Pix로 보간하는 응용 논문으로 로보틱스 관련 없음</td></tr>
<tr><td>487</td><td><a href='https://arxiv.org/abs/2611.15764'>AIFR: Adaptive Identity Feature Recovery for Diffusion-Based Makeup and Anime Portraits</a></td><td>18</td><td>0</td><td>CV</td><td>화장·애니 스타일 초상화에서 frozen 얼굴인식 모델 내부의 identity feature를 복원하는 AIFR임. 로보틱스 관련 없음</td></tr>
<tr><td>488</td><td><a href='https://arxiv.org/abs/2611.16442'>DesignTaste: Benchmarking AI-Generator Visual Design Against Award-Wining Works</a></td><td>18</td><td>0</td><td>Multimodal</td><td>수상작과 비교해 text-to-image 모델의 디자인 능력을 재는 DesignTaste 벤치마크로 로봇과 무관함</td></tr>
<tr><td>489</td><td><a href='https://arxiv.org/abs/2611.14604'>KernelMosaic: An Open Dataset and Agentic Framework for CUDA Kernel Generation</a></td><td>18</td><td>0</td><td>NLP</td><td>CUDA kernel 과제와 검증된 풀이 궤적을 담은 KernelMosaic 데이터셋으로 소형 모델을 SFT해 KernelBench L1 정확도를 4%에서 88%로 올린 코드 생성 연구로 로봇과 무관함</td></tr>
<tr><td>490</td><td><a href='https://arxiv.org/abs/2611.14922'>A Transferable Pretrained 3D Model for Impedance Inversion with Sparse-Well Prior Conditioning</a></td><td>18</td><td>0</td><td>LG</td><td>지진 impedance inversion 사전학습 모델임</td></tr>
<tr><td>491</td><td><a href='https://arxiv.org/abs/2611.14990'>EASTAR: Event-Anchored Semantic and Task-Adaptive Region Representation Learning</a></td><td>18</td><td>0</td><td>LG</td><td>도시 region representation learning임</td></tr>
<tr><td>492</td><td><a href='https://arxiv.org/abs/2611.15002'>AI4Plasma I: Data-Efficient Surrogate Modeling of Capacitively Coupled Plasma Fields</a></td><td>18</td><td>0</td><td>LG</td><td>plasma 필드 surrogate 비교임</td></tr>
<tr><td>493</td><td><a href='https://arxiv.org/abs/2611.15502'>Selective State-Space Neural Tucker Factorization for Temporal-aware Traffic Imputation</a></td><td>18</td><td>0</td><td>LG</td><td>교통 데이터 결측 보간임</td></tr>
<tr><td>494</td><td><a href='https://arxiv.org/abs/2611.15584'>AI4Plasma II: Geometry-Aware Surrogate Modeling for Variable Electrode Gap GEC Plasmas</a></td><td>18</td><td>0</td><td>LG</td><td>plasma 형상 surrogate임</td></tr>
<tr><td>495</td><td><a href='https://arxiv.org/abs/2611.15705'>Characterizing Predictive Multiplicity in Ranking and Its Fairness Implications</a></td><td>18</td><td>0</td><td>LG</td><td>ranking predictive multiplicity와 공정성 분석임</td></tr>
<tr><td>496</td><td><a href='https://arxiv.org/abs/2611.15917'>Owned Edits to a Shared Decision Rule: Learning Private Exceptions as Typed, Gated, Withdrawable Weight Edits</a></td><td>18</td><td>0</td><td>LG</td><td>결정 규칙 예외 학습임</td></tr>
<tr><td>497</td><td><a href='https://arxiv.org/abs/2611.15963'>WELP : Weighted Ensemble in the LooP for committor learning</a></td><td>18</td><td>0</td><td>LG</td><td>분자 committor 학습임</td></tr>
<tr><td>498</td><td><a href='https://arxiv.org/abs/2611.16093'>Measuring Preferred Representation in AI-generated Images with Community Scorers</a></td><td>18</td><td>0</td><td>CV</td><td>생성 이미지의 대표성을 측정함</td></tr>
<tr><td>499</td><td><a href='https://arxiv.org/abs/2611.16169'>Feature-Aware Edge Sampling for Approximate One-Step Laplacian Propagation</a></td><td>18</td><td>0</td><td>LG</td><td>Laplacian propagation 근사임</td></tr>
<tr><td>500</td><td><a href='https://arxiv.org/abs/2611.17152'>AeroZoo: A Benchmark of Well-Posed Flow Problems for Foundation Models of Aerodynamics</a></td><td>18</td><td>0</td><td>LG</td><td>공력 CFD foundation model benchmark로 로보틱스 무관함</td></tr>
<tr><td>501</td><td><a href='https://arxiv.org/abs/2611.14758'>Benchmarking Multilingual Document Understanding in Vision-Language Models</a></td><td>18</td><td>0</td><td>Multimodal</td><td>다국어 문서 이해 VLM benchmark로 로봇 무관함</td></tr>
<tr><td>502</td><td><a href='https://arxiv.org/abs/2611.15538'>Faithful in Steps: Improving Generalization and Citation in RAG via Query Decomposition</a></td><td>18</td><td>0</td><td>NLP</td><td>query 분해를 통한 RAG 인용 개선임</td></tr>
<tr><td>503</td><td><a href='https://arxiv.org/abs/2611.15568'>Can We Make an LLM Dumber, or Is It Just Playing Dumb? An Empirical Study of Believable Performance Throttling</a></td><td>18</td><td>0</td><td>NLP</td><td>LLM 성능 의도적 저하의 believable throttling 연구임</td></tr>
<tr><td>504</td><td><a href='https://arxiv.org/abs/2611.15989'>What Roles Do System Prompts Really Assign? Validating and Steering Occupational Role Vectors in LLMs</a></td><td>18</td><td>0</td><td>NLP</td><td>system prompt 직업 역할 벡터 검증임</td></tr>
<tr><td>505</td><td><a href='https://arxiv.org/abs/2611.16183'>Data-Efficient LLM Safety Alignment Guided by Interpretable Features</a></td><td>18</td><td>0</td><td>NLP</td><td>해석 가능한 feature 기반 안전 정렬 데이터 효율화임</td></tr>
<tr><td>506</td><td><a href='https://arxiv.org/abs/2611.16919'>Beyond Word Error Rate: A Failure Taxonomy of Streaming Dictation ASR</a></td><td>18</td><td>0</td><td>NLP</td><td>11개 streaming dictation ASR의 오류를 인식, 포맷, 언어 처리 단계로 분류한 실패 분류 연구이며 속삭임 음성에서 시스템별 차이를 보임, 로봇과 무관함</td></tr>
<tr><td>507</td><td><a href='https://arxiv.org/abs/2611.17169'>Parsed, Plausible, Wrong: Output Format Controls Silent Errors in Small-Model Semantic Parsing</a></td><td>18</td><td>0</td><td>NLP</td><td>PIZZA 주문 파싱에서 6가지 출력 포맷을 비교해 평범한 단어 인코딩이 silent error를 줄임을 보인 소형 모델 파싱 실험이며 로봇과 무관함</td></tr>
<tr><td>508</td><td><a href='https://arxiv.org/abs/2611.15091'>Advancing Weighted Partial MaxSAT Solving via Differentiable GPU Guidance</a></td><td>18</td><td>0</td><td>LG</td><td>WPMaxSAT에서 계층적 미분 손실로 hard clause 만족을 우선하는 GPU 최적화를 CPU 솔버에 warm start로 전달함, 조합 최적화 솔버 개선이며 로봇과 무관함</td></tr>
<tr><td>509</td><td><a href='https://arxiv.org/abs/2611.15223'>guardscope: Measuring Which Actions Runtime Controls Check in LLM Agent Systems</a></td><td>18</td><td>0</td><td>LG</td><td>LLM agent의 15개 행동 경로 중 runtime control이 실제로 검사하는 범위를 커널 수준 ground truth와 대조해 재는 guardscope이며 보안 도구임</td></tr>
<tr><td>510</td><td><a href='https://arxiv.org/abs/2611.16498'>How many LLM-labelled rows does a decision encoder need, and how wrong can the labels be?</a></td><td>18</td><td>0</td><td>NLP</td><td>Laya decision encoder에 LLM 라벨 행이 얼마나 필요한지와 라벨 오염 내성을 합성 데이터 19회 fine-tuning으로 측정한 연구임. 단일 backbone과 합성 데이터라 일반성이 낮고 로봇과 무관함</td></tr>
<tr><td>511</td><td><a href='https://arxiv.org/abs/2611.16527'>AI has its own style in mathematical proving</a></td><td>18</td><td>0</td><td>LLM Analysis</td><td>LLM 3종에게 유클리드 원론 465개 명제를 다시 증명시켜 인용 구조가 사람 증명과 다름을 Jaccard 유사도로 보인 분석임. 흥미로운 관찰이나 로봇과 무관함</td></tr>
<tr><td>512</td><td><a href='https://arxiv.org/abs/2611.16586'>Large Language Models as Digital Twins: a Distribution-Aware Questionnaire-Based Evaluation</a></td><td>18</td><td>0</td><td>LLM Eval</td><td>소셜 미디어 글을 보고 LLM이 특정 사용자의 Big Five 설문 응답을 재현하는지 평가하며 사용자 텍스트가 일관되게 도움 되지 않는다고 결론냄. 로봇과 무관함</td></tr>
<tr><td>513</td><td><a href='https://arxiv.org/abs/2611.16722'>Mind the Accuracy-Approval Gap: How Users Evaluate Sycophantic AI in Everyday Tasks</a></td><td>18</td><td>0</td><td>LLM Eval</td><td>sycophancy 페르소나 4종을 benchmark와 사용자 연구 두 건으로 비교해 정확한 AI가 덜 호감 받는 불일치를 보임. 사용자 연구 결과는 흥미로우나 로봇과 무관함</td></tr>
<tr><td>514</td><td><a href='https://arxiv.org/abs/2611.17072'>Reasoning Supervision and Capability Retention in LoRA Domain Adaptation</a></td><td>18</td><td>0</td><td>NLP</td><td>Qwen3-8B를 금융 도메인에 LoRA로 fine-tuning할 때 reasoning trace 포함 여부별로 도메인 성능과 일반 능력 유지를 비교한 ablation임. 도메인 fine-tuning 위주라 로봇과 무관함</td></tr>
<tr><td>515</td><td><a href='https://arxiv.org/abs/2611.16368'>ReliaGuard: Reconstruction-Aware Watermarking for Source Attribution and Blind Edit Localization</a></td><td>16</td><td>0</td><td>CV</td><td>VAE 재구성을 고려한 watermark로 출처 귀속과 blind 편집 위치 탐지를 하는 ReliaGuard임. 로보틱스 관련 없음</td></tr>
<tr><td>516</td><td><a href='https://arxiv.org/abs/2611.16534'>Context-Predictive Low-Rank Adaptation for Face Presentation Attack Detection</a></td><td>16</td><td>0</td><td>CV</td><td>CLIP LoRA에 JEPA식 context 예측을 붙인 얼굴 presentation attack 탐지 CP-JEPA임. 로보틱스 관련 없음</td></tr>
<tr><td>517</td><td><a href='https://arxiv.org/abs/2611.17329'>Internalizing Investment Mandates: A Neurosymbolic RL Approach to Portfolio Allocation</a></td><td>16</td><td>0</td><td>RL</td><td>투자 mandate를 내재화한 포트폴리오 RL로 무관함</td></tr>
<tr><td>518</td><td><a href='https://arxiv.org/abs/2611.16297'>Hibikino-Musashi@Home 2026 Team Description Paper</a></td><td>15</td><td>3</td><td>Team Paper</td><td>RoboCup@Home 팀 기술 설명 문서임</td></tr>
<tr><td>519</td><td><a href='https://arxiv.org/abs/2611.16250'>Direct-Ink-Writing of Soft Thin Film Force-Sensitive Resistors with Velostat and Printed-Carbon Sensing Elements</a></td><td>15</td><td>2</td><td>Sensor</td><td>인쇄형 Velostat 힘 센서 제작으로 소재 중심임</td></tr>
<tr><td>520</td><td><a href='https://arxiv.org/abs/2611.16869'>Raysemble: Metric 3D Bone Reconstruction from a Single X-ray</a></td><td>15</td><td>1</td><td>CV</td><td>단일 X-ray에서 요추와 골반 뼈 8개의 metric 3D 형상을 복원하는 의료 영상 방법으로 로봇과 무관함</td></tr>
<tr><td>521</td><td><a href='https://arxiv.org/abs/2611.14677'>Fast Slice-Wise Deep Learning Motion Correction for Spinal Cord Functional MRI</a></td><td>15</td><td>0</td><td>CV</td><td>척수 fMRI의 slice별 평행이동을 CNN으로 회귀해 SCT보다 30배 빠르게 움직임을 보정하는 의료영상 연구라 로봇과 무관함</td></tr>
<tr><td>522</td><td><a href='https://arxiv.org/abs/2611.14832'>Neural Compression for Scientific Particle Data: Perspectives on How Learning Can Help</a></td><td>15</td><td>0</td><td>LG</td><td>과학 입자 데이터에서 neural point cloud 압축이 G-PCC 대비 이득이 작음을 fractal dimension 차이로 설명한 관점 논문이라 로봇과 무관함</td></tr>
<tr><td>523</td><td><a href='https://arxiv.org/abs/2611.14907'>Lines Are Ideas: Visual Creativity Assessment in Hyperbolic Space</a></td><td>15</td><td>0</td><td>CV</td><td>그림 쌍의 의미 편차를 hyperbolic 공간 측지 거리로 재서 창의성을 평가하는 방법이며 로봇과 무관함</td></tr>
<tr><td>524</td><td><a href='https://arxiv.org/abs/2611.15165'>Bridging Update Coordination and Flatness in Federated Learning</a></td><td>15</td><td>0</td><td>LG</td><td>federated learning에서 update coordination과 flatness 보정을 같은 local trajectory 위에서 합치는 프레임워크로 로봇과 무관한 최적화 개선임</td></tr>
<tr><td>525</td><td><a href='https://arxiv.org/abs/2611.15306'>Beyond the Explicit: Benchmarking and Detecting Implicit Harm in Short Videos</a></td><td>15</td><td>0</td><td>Video</td><td>암시적 유해 숏폼 영상 7,110개 dataset과 2단계 추론 탐지 모델 DeepHarm-VL을 낸 콘텐츠 검열 연구라 로봇과 무관함</td></tr>
<tr><td>526</td><td><a href='https://arxiv.org/abs/2611.15325'>CaseScope: A Multi-Field Benchmark for Case-Level Pathology Diagnosis with Multimodal LLMs</a></td><td>15</td><td>0</td><td>Multimodal</td><td>여러 현미경 시야로 병리 진단하는 MLLM benchmark CaseScope이며 의료 평가 dataset이라 로봇과 무관함</td></tr>
<tr><td>527</td><td><a href='https://arxiv.org/abs/2611.15645'>Ultrasound Elastography: Excitation Methods and Low-Cost Alternative</a></td><td>15</td><td>0</td><td>CV</td><td>초음파 elastography의 가진 방법과 저가 대안을 정리한 의료 리뷰성 글로 로보틱스 관련 없음</td></tr>
<tr><td>528</td><td><a href='https://arxiv.org/abs/2611.16393'>TransXplainRRG: A Radiologist-Evaluated LVLM for Chest Radiograph Report Generation</a></td><td>15</td><td>0</td><td>CV</td><td>Swin과 text encoder로 흉부 X-ray 보고서를 생성하고 방사선과 의사가 평가한 LVLM 논문으로 로봇 관련 없음</td></tr>
<tr><td>529</td><td><a href='https://arxiv.org/abs/2611.17077'>SALT: State-Aligned Low-Rank Transfer for Single-Temporal Cross-Dataset Structural Localization in Remote Sensing</a></td><td>15</td><td>0</td><td>CV</td><td>DINOv3를 고정하고 rank-2 low-rank 보정으로 원격탐사 건물 변화 위치를 단일 시점에서 cross-dataset 전이하는 방법으로 로봇과 무관함</td></tr>
<tr><td>530</td><td><a href='https://arxiv.org/abs/2611.14594'>Adversarial Risk in the Generative AI Era Necessitates Dropping the Small Epsilon Ball</a></td><td>15</td><td>0</td><td>LG</td><td>adversarial 연구가 l_p epsilon ball에 집착하는 것이 위험 인식을 왜곡한다고 주장하는 position paper이며 로봇과 무관함</td></tr>
<tr><td>531</td><td><a href='https://arxiv.org/abs/2611.14849'>Generalize Then Personalize: Wearable-Based Heart Rate Forecasting Under Scarce Ruck-March Data</a></td><td>15</td><td>0</td><td>LG</td><td>웨어러블 심박 예측 응용임</td></tr>
<tr><td>532</td><td><a href='https://arxiv.org/abs/2611.14897'>Social Engineering Attack Detection in Corporate Communications</a></td><td>15</td><td>0</td><td>LG</td><td>사회공학 공격 탐지 응용임</td></tr>
<tr><td>533</td><td><a href='https://arxiv.org/abs/2611.15284'>A hybrid machine learning-analog framework for downscaling unprecedented climate extremes</a></td><td>15</td><td>0</td><td>LG</td><td>기후 downscaling 응용임</td></tr>
<tr><td>534</td><td><a href='https://arxiv.org/abs/2611.15329'>TabOmics: A Small, Open Tabular Foundation Model for Wide Omics Data</a></td><td>15</td><td>0</td><td>LG</td><td>omics tabular foundation model임</td></tr>
<tr><td>535</td><td><a href='https://arxiv.org/abs/2611.15555'>What Conformal Selection Can Certify in CRISPR Off-Target Design:Benchmark Leakage, Free Baselines, and a Finite-Sample Cohort Requirement</a></td><td>15</td><td>0</td><td>LG</td><td>CRISPR off-target conformal selection임</td></tr>
<tr><td>536</td><td><a href='https://arxiv.org/abs/2611.15578'>Constructing and Validating Memorisation Audits for EHR Foundation Models</a></td><td>15</td><td>0</td><td>LG</td><td>EHR foundation model 암기 감사임</td></tr>
<tr><td>537</td><td><a href='https://arxiv.org/abs/2611.15710'>Curiosity-0826-4B: Generative Medical Event Sequence Modeling Across Pediatric and Adult Populations</a></td><td>15</td><td>0</td><td>LG</td><td>의료 event sequence 생성 모델임</td></tr>
<tr><td>538</td><td><a href='https://arxiv.org/abs/2611.15810'>Sparse PCA with Overlapping Supports: NP-Hardness and an FPTAS</a></td><td>15</td><td>0</td><td>LG</td><td>sparse PCA 계산 복잡도 이론임</td></tr>
<tr><td>539</td><td><a href='https://arxiv.org/abs/2611.15814'>Large Payments Model</a></td><td>15</td><td>0</td><td>LG</td><td>결제 도메인 foundation model임</td></tr>
<tr><td>540</td><td><a href='https://arxiv.org/abs/2611.15954'>Riordan Arrays as Structured Operators for Artificial Intelligence</a></td><td>15</td><td>0</td><td>LG</td><td>Riordan array 구조 연산자임</td></tr>
<tr><td>541</td><td><a href='https://arxiv.org/abs/2611.16013'>Runtime Analysis of Cartesian Genetic Programming on Max: A Proven Exponential Speedup</a></td><td>15</td><td>0</td><td>LG</td><td>Cartesian GP 실행 시간 이론임</td></tr>
<tr><td>542</td><td><a href='https://arxiv.org/abs/2611.16018'>Protocol-Aware Auditing of Domain-Blind Feature Attribution in Network Intrusion Detection</a></td><td>15</td><td>0</td><td>LG</td><td>침입 탐지 feature attribution 감사임</td></tr>
<tr><td>543</td><td><a href='https://arxiv.org/abs/2611.16088'>Subsurface schematisation from sparse CPT data using the tabular foundation model TabPFN</a></td><td>15</td><td>0</td><td>LG</td><td>CPT 지반 단면 TabPFN 응용임</td></tr>
<tr><td>544</td><td><a href='https://arxiv.org/abs/2611.16323'>Does Deep Knowledge Tracing Learn Semantic Relations Between Knowledge Components?</a></td><td>15</td><td>0</td><td>LG</td><td>knowledge tracing 의미 관계 분석임</td></tr>
<tr><td>545</td><td><a href='https://arxiv.org/abs/2611.16361'>MutAtlas: A PDB-Wide Energy-Guided Atlas of Protein Mutation Effects</a></td><td>15</td><td>0</td><td>LG</td><td>단백질 mutation atlas임</td></tr>
<tr><td>546</td><td><a href='https://arxiv.org/abs/2611.16726'>From Data to Wisdom: Rethinking AI Through an Epistemic Lens</a></td><td>15</td><td>0</td><td>LG</td><td>Data-to-Wisdom 철학적 AI 구조 제안이며 실증이 없는 제안임</td></tr>
<tr><td>547</td><td><a href='https://arxiv.org/abs/2611.16772'>Class-Competence Aggregation: Output-Layer Routing for Federated Multiclass DDoS Detection under Class-Concentrated Non-IID Data</a></td><td>15</td><td>0</td><td>LG</td><td>federated DDoS 탐지의 output layer 집계 기법으로 로보틱스 연관 없음</td></tr>
<tr><td>548</td><td><a href='https://arxiv.org/abs/2611.17129'>Paper-Faithful Federated Learning: Scientific Checks for Practitioner and Agent Development</a></td><td>15</td><td>0</td><td>LG</td><td>federated 학습 실험 재현성 검사 도구로 무관함</td></tr>
<tr><td>549</td><td><a href='https://arxiv.org/abs/2611.17143'>A Convex-Analytic Reformulation for Poisoning Attacks on Logistic Regression</a></td><td>15</td><td>0</td><td>LG</td><td>logistic regression poisoning 공격의 convex 재구성으로 무관함</td></tr>
<tr><td>550</td><td><a href='https://arxiv.org/abs/2611.17196'>Physically Interpretable Basin Selection in Discrete-Variable Origami Design</a></td><td>15</td><td>0</td><td>LG</td><td>origami 이산 설계 basin 선택 분석으로 무관함</td></tr>
<tr><td>551</td><td><a href='https://arxiv.org/abs/2611.14675'>MITRA-Swarm: Injecting Explicit Linguistic Structure into Foundation Models for Classical Machine Translation</a></td><td>15</td><td>0</td><td>NLP</td><td>산스크리트 기계번역용 구조 주입으로 무관함</td></tr>
<tr><td>552</td><td><a href='https://arxiv.org/abs/2611.14801'>Distributionally Robust BEST-RQ For Speech Representation Learning</a></td><td>15</td><td>0</td><td>Speech</td><td>BEST-RQ distributionally robust 음성 표현학습임</td></tr>
<tr><td>553</td><td><a href='https://arxiv.org/abs/2611.15346'>Towards Better Legal Reasoning LLMs: Signal Balancing and Reward Scheduling</a></td><td>15</td><td>0</td><td>NLP</td><td>법률 추론 LLM의 신호 균형과 reward 스케줄링임</td></tr>
<tr><td>554</td><td><a href='https://arxiv.org/abs/2611.15597'>When Local Definitions Are Missing: Stable Errors in Language Models</a></td><td>15</td><td>0</td><td>NLP</td><td>국소 정의 부재 시 LM 오류 분석임</td></tr>
<tr><td>555</td><td><a href='https://arxiv.org/abs/2611.15642'>Differential Backpack Language Models: Sense Inhibition via Signed Contextualization Weights</a></td><td>15</td><td>0</td><td>NLP</td><td>Backpack LM의 sense 억제 변형임</td></tr>
<tr><td>556</td><td><a href='https://arxiv.org/abs/2611.15925'>ShadowBench: Exposing Lexical Anchoring and the Illusion of Forgetting in Large Language Models</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM 망각 착시와 어휘 anchoring benchmark임</td></tr>
<tr><td>557</td><td><a href='https://arxiv.org/abs/2611.16399'>Saidzoda-Kazakh-EmbeddingGemma-300M: How Far One Epoch of Generated Questions Takes a Small Kazakh Embedder</a></td><td>15</td><td>0</td><td>NLP</td><td>EmbeddingGemma-300M을 생성 질문 16만 쌍으로 한 epoch fine-tuning해 카자흐어 retrieval을 올린 기술 보고서이며 특정 언어 fine-tuning 위주임</td></tr>
<tr><td>558</td><td><a href='https://arxiv.org/abs/2611.16500'>EvenVLM: A Text and Multimodal Dataset for the Even Language with Vision-Language Fine-Tuning</a></td><td>15</td><td>0</td><td>NLP</td><td>멸종 위기 Even어 사전 기반 데이터셋과 tokenizer 확장, Qwen3-VL-4B LoRA 적응이 내용이며 로봇 관련성이 없는 저자원 언어 자원 구축임</td></tr>
<tr><td>559</td><td><a href='https://arxiv.org/abs/2611.17091'>Optimal Single-History Tokenization Disambiguation for Provably Secure Linguistic Steganography</a></td><td>15</td><td>0</td><td>NLP</td><td>tokenization 모호성 아래서 single-history 수신자가 stop entropy를 포기해야 함을 증명하고 coin projection으로 언어적 steganography 용량을 올림, 암호 이론 응용이라 로봇과 무관함</td></tr>
<tr><td>560</td><td><a href='https://arxiv.org/abs/2611.14544'>Zugwise: Domain-Aware Game Reconstruction for Digitizing Handwritten Chess Scoresheets</a></td><td>15</td><td>0</td><td>CV</td><td>필기 체스 기록지 디지털화를 legal-but-wrong 오류를 잡는 game reconstruction으로 재정의하고 체스 엔진 기법을 재활용함, 로봇과 무관한 도메인 응용임</td></tr>
<tr><td>561</td><td><a href='https://arxiv.org/abs/2611.15843'>Food Critic: An Agentic Visualization System for Auditable Restaurant-Safety Reasoning</a></td><td>15</td><td>0</td><td>HCI</td><td>식당 위생 검사 기록과 리뷰를 근거로 agent 추론 과정을 시각화하는 Food Critic 시스템임. 시스템 데모 성격이고 로봇과 무관함</td></tr>
<tr><td>562</td><td><a href='https://arxiv.org/abs/2611.16335'>From More to Better: Causal Inference and Digital Experimentation in the Age of AI</a></td><td>15</td><td>0</td><td>Stat</td><td>AI 시대에 causal inference와 온라인 실험 담당자의 역할을 논하는 roundtable 기반 perspective 글임. 실험 결과가 없고 로봇과 무관함</td></tr>
<tr><td>563</td><td><a href='https://arxiv.org/abs/2611.14857'>In-orbit demonstration of object-based change detection applied to the maritime domain</a></td><td>14</td><td>1</td><td>CV</td><td>위성에 탑재해 선박 분할과 Hungarian 및 RANSAC 매칭으로 변화 탐지를 궤도에서 시연한 원격탐사 응용임</td></tr>
<tr><td>564</td><td><a href='https://arxiv.org/abs/2611.16538'>Pl@ntNet machine-to-machine identification service with Pl@ntNet API: enabling automated biodiversity monitoring through large-scale plant identification</a></td><td>14</td><td>1</td><td>CV</td><td>Pl@ntNet 식물 식별을 API로 자동 워크플로에 연결하는 서비스 설명 논문으로 연구적 novelty 낮음</td></tr>
<tr><td>565</td><td><a href='https://arxiv.org/abs/2611.17126'>STeP-C: Real-Time Neural Compression for Distributed Fiber-Optic Sensing at Scale</a></td><td>14</td><td>0</td><td>LG</td><td>분산 광섬유 센싱 데이터를 공간 인코딩, 시간 예측, 엔트로피 잔차 코딩으로 실시간 압축하는 시스템이며 로봇과 무관함</td></tr>
<tr><td>566</td><td><a href='https://arxiv.org/abs/2611.16821'>Calibration and Conformal Prediction for Medical Question Answering in Arabic and English: Evidence from Two Non-Parallel Benchmarks</a></td><td>14</td><td>0</td><td>NLP</td><td>아랍어 의료 QA의 calibration과 conformal prediction 평가로 무관함</td></tr>
<tr><td>567</td><td><a href='https://arxiv.org/abs/2611.16856'>Sustainable Federated Fine-Tuning with LoRA: Environmental Impact and Performance Footprint</a></td><td>14</td><td>0</td><td>LG</td><td>federated LoRA의 에너지 소비 측정 연구로 무관함</td></tr>
<tr><td>568</td><td><a href='https://arxiv.org/abs/2611.17145'>Enhancing Preference Detection using Eye Movement Cascade and Multilayer Combinatorial Fusion</a></td><td>14</td><td>0</td><td>LG</td><td>시선 움직임 기반 선호 예측으로 로보틱스 무관함</td></tr>
<tr><td>569</td><td><a href='https://arxiv.org/abs/2611.14823'>Discharge Summary Generation Is Not Just Summarization: A Reality Check for Evaluation</a></td><td>14</td><td>0</td><td>NLP</td><td>퇴원 요약 평가 재검토로 무관함</td></tr>
<tr><td>570</td><td><a href='https://arxiv.org/abs/2611.14828'>LLMs and the Homogenization of Teaching</a></td><td>14</td><td>0</td><td>NLP</td><td>LLM의 교육 획일화 분석으로 무관함</td></tr>
<tr><td>571</td><td><a href='https://arxiv.org/abs/2611.14861'>Is Jev a Good Multilingual Judge?</a></td><td>14</td><td>0</td><td>NLP</td><td>다국어 LLM judge 평가임</td></tr>
<tr><td>572</td><td><a href='https://arxiv.org/abs/2611.14908'>Hy ASR 3.0 Technical Report</a></td><td>14</td><td>0</td><td>Speech</td><td>Hy ASR 3.0 기술 보고서임</td></tr>
<tr><td>573</td><td><a href='https://arxiv.org/abs/2611.15467'>AutoOntic: Automatic Ontology Induction from Text for Knowledge Graph Construction</a></td><td>14</td><td>0</td><td>NLP</td><td>텍스트에서 ontology 자동 유도하는 KG 구성임</td></tr>
<tr><td>574</td><td><a href='https://arxiv.org/abs/2611.16704'>Forecasting Sales Delay through Time-aware Analysis of Sales Events in Textual Reports</a></td><td>14</td><td>0</td><td>NLP</td><td>영업 보고서 텍스트에서 예정 수주일 지연을 예측하는 confidence feature 기반 B2B 응용이며 로봇과 무관함</td></tr>
<tr><td>575</td><td><a href='https://arxiv.org/abs/2611.14924'>Edge-Native Multimodal RAG: Hardware-Aware Quantization and Architectural Optimization for Consumer GPUs</a></td><td>14</td><td>0</td><td>LG</td><td>T4급 소비자 GPU에서 NF4 양자화와 Florence-2를 묶은 multimodal RAG 구성의 엔지니어링 평가이며 새 방법론 기여가 약함</td></tr>
<tr><td>576</td><td><a href='https://arxiv.org/abs/2611.16710'>Acoustic Respiratory Phase Detection on Mobile Devices</a></td><td>14</td><td>0</td><td>Audio</td><td>스마트폰 소리로 호흡 단계를 분류하는 CNN-Transformer를 LOSO 평가하고 ONNX로 20ms 미만 추론을 구현함. 응용 중심의 incremental 연구이고 로봇과 무관함</td></tr>
<tr><td>577</td><td><a href='https://arxiv.org/abs/2611.16831'>A Modular Framework for ESG Prediction through Domain-Specific Language Modeling and Graph Learning</a></td><td>14</td><td>0</td><td>Finance</td><td>기업 ESG 점수를 도메인 언어모델과 기업 관계 graph learning으로 예측하는 ESGPred임. 응용 도메인의 incremental 연구이고 로봇과 무관함</td></tr>
<tr><td>578</td><td><a href='https://arxiv.org/abs/2611.14728'>SyntheIce: A Synthetic Radargram Annotation Benchmark for Englacial Layer Reconstruction</a></td><td>12</td><td>0</td><td>CV</td><td>빙하 radargram의 끊긴 층을 slope 예측으로 잇는 알고리즘과 합성 benchmark를 낸 지구과학 응용이라 로봇과 무관함</td></tr>
<tr><td>579</td><td><a href='https://arxiv.org/abs/2611.15044'>Estimating Image Creativity</a></td><td>12</td><td>0</td><td>CV</td><td>novelty, surprise, arousal 세 차원을 지도학습으로 예측해 이미지 창의성 점수를 추정하는 구식 설정의 연구임</td></tr>
<tr><td>580</td><td><a href='https://arxiv.org/abs/2611.15107'>From Seeing to Remembering: Brain-Informed Agentic Text-to-Video Generation for Enhancing Memorability</a></td><td>12</td><td>0</td><td>Video</td><td>fMRI 유사 신경 반응 예측으로 영상 기억 용이성을 높이도록 prompt를 반복 수정하는 text-to-video 응용이라 로봇과 무관함</td></tr>
<tr><td>581</td><td><a href='https://arxiv.org/abs/2611.15194'>The Neighbour&#x27;s Label: Opposite Subgroup Effects of Same-Dialogue Exposure in Next-Act Evaluation</a></td><td>12</td><td>0</td><td>NLP</td><td>next-act 평가에서 같은 대화의 앞선 라벨 노출이 continuation과 transition 부분군에 반대 효과를 낸다는 평가 누수 분석이며 로봇과 무관함</td></tr>
<tr><td>582</td><td><a href='https://arxiv.org/abs/2611.16608'>Towards Democratising Low-Data Medical Image Classification: CPU-Trainable ZACH-ViT and Its Geometric Variants</a></td><td>12</td><td>0</td><td>CV</td><td>파라미터 26만 개 미만의 ZACH-ViT 변형을 MedMNIST+에서 CPU로 학습해 비교한 의료 영상 분류 평가로 로봇과 무관함</td></tr>
<tr><td>583</td><td><a href='https://arxiv.org/abs/2611.16749'>ORCA:Orthogonal Residual Consensus Alignment for Multi-View Clustering</a></td><td>12</td><td>0</td><td>LG</td><td>multi-view clustering에서 orthogonal residual 융합과 consensus 가중 contrastive 정렬을 쓰는 incremental 방법으로 로봇과 무관함</td></tr>
<tr><td>584</td><td><a href='https://arxiv.org/abs/2611.16764'>Efficient Periocular Recognition through Model Scaling and Cross Spectral VIS NIR Verification</a></td><td>12</td><td>0</td><td>CV</td><td>periocular 인식에서 입력 크기와 backbone 폭 축소의 정확도와 연산량을 비교한 규모 조절 연구로 로봇과 무관함</td></tr>
<tr><td>585</td><td><a href='https://arxiv.org/abs/2611.17176'>Validation-Guided Prompt Selection for Differential Morphing Attack Detection</a></td><td>12</td><td>0</td><td>Multimodal</td><td>얼굴 morph 공격 검출에서 frozen VLM의 prompt 후보 50개를 validation 손실로 고르는 연구로 로봇과 무관함</td></tr>
<tr><td>586</td><td><a href='https://arxiv.org/abs/2611.17302'>FLEX-LBP: Learning Local Binary Patterns with Exact Binary Inference for Texture Classification</a></td><td>12</td><td>0</td><td>CV</td><td>LBP의 반경, 각도, 임계값을 straight-through estimator로 학습하는 FLEX-LBP 질감 분류이며 로봇과 무관함</td></tr>
<tr><td>587</td><td><a href='https://arxiv.org/abs/2611.14589'>CAFIN: CUDA-accelerated Adaptive Fisher Information Matrix Network Optimization via GPU-Native Kernel Fusion</a></td><td>12</td><td>0</td><td>LG</td><td>AdaFisher의 Fisher 행렬 계산을 CUDA kernel fusion으로 묶어 optimizer step 지연을 2.1에서 26.9% 줄인 구현 최적화로 로봇과 무관함</td></tr>
<tr><td>588</td><td><a href='https://arxiv.org/abs/2611.15023'>SkinAdvisor: An AI-Driven Decision Framework for Skin Production Planning via Multi-Modal Transformer Sales Forecasting</a></td><td>12</td><td>0</td><td>LG</td><td>게임 skin 판매 예측 응용임</td></tr>
<tr><td>589</td><td><a href='https://arxiv.org/abs/2611.15137'>Serving-Aligned Entire-Space Conversion Modeling via Click-Through Rate Knowledge Distillation</a></td><td>12</td><td>0</td><td>LG</td><td>추천 시스템 전환율 모델임</td></tr>
<tr><td>590</td><td><a href='https://arxiv.org/abs/2611.15241'>KQML-Liver: Interpretable Hybrid Quantum Machine Learning with Kolmogorov-Arnold Networks for Liver Disease Classification</a></td><td>12</td><td>0</td><td>LG</td><td>양자 ML 간 질환 예측임</td></tr>
<tr><td>591</td><td><a href='https://arxiv.org/abs/2611.15348'>Breath-Dx: A Time Series Classification Benchmark for Disease Screening with eNose</a></td><td>12</td><td>0</td><td>LG</td><td>eNose 질병 선별 benchmark임</td></tr>
<tr><td>592</td><td><a href='https://arxiv.org/abs/2611.15598'>Imputing Missing Near-Surface Air Temperature using Graph Attention Networks with Distance-Aware Edge Features</a></td><td>12</td><td>0</td><td>LG</td><td>기온 결측 보간임</td></tr>
<tr><td>593</td><td><a href='https://arxiv.org/abs/2611.16065'>Tokenized Reward Systems for Federated Learning: The Privacy vs. Fairness Tradeoff</a></td><td>12</td><td>0</td><td>LG</td><td>federated learning 토큰 보상 설계임</td></tr>
<tr><td>594</td><td><a href='https://arxiv.org/abs/2611.16100'>Hiding a Gap Does Not Close It: The Price of Removing the Mean Group Contrast from Learned Models of Learning Dynamics</a></td><td>12</td><td>0</td><td>LG</td><td>학생 모델 공정성 분석임</td></tr>
<tr><td>595</td><td><a href='https://arxiv.org/abs/2611.16172'>Self-Supervised Attention-Based Virtual Metrology for CMP MRR Prediction</a></td><td>12</td><td>0</td><td>LG</td><td>반도체 공정 virtual metrology임</td></tr>
<tr><td>596</td><td><a href='https://arxiv.org/abs/2611.16322'>Climate Temporal Temperature Prediction via an Adaptive Stacked Bidirectional Residual Mamba Network</a></td><td>12</td><td>0</td><td>LG</td><td>기온 예측 Mamba 응용임</td></tr>
<tr><td>597</td><td><a href='https://arxiv.org/abs/2611.16756'>Beyond Binary Classification: Multiclass Machine Learning for Diabetes and Prediabetes Risk Prediction Using NHANES</a></td><td>12</td><td>0</td><td>LG</td><td>NHANES 기반 당뇨 위험 다중분류로 로보틱스와 무관한 표준 ML 적용임</td></tr>
<tr><td>598</td><td><a href='https://arxiv.org/abs/2611.17294'>Metal Sandbox: Isolated Execution and Command Scheduling for GPU Coding Agents on Apple Silicon</a></td><td>12</td><td>0</td><td>LG</td><td>Apple Silicon GPU coding agent 샌드박스 시스템으로 무관함</td></tr>
<tr><td>599</td><td><a href='https://arxiv.org/abs/2611.14818'>What Do Tokenizer Comparisons Measure? Disentangling Granularity, Root Assignment, and Word-Level Readout across Amharic and Hausa</a></td><td>12</td><td>0</td><td>NLP</td><td>tokenizer 비교 분석으로 무관함</td></tr>
<tr><td>600</td><td><a href='https://arxiv.org/abs/2611.15058'>FIBER: Bayesian Fusion of Fast-DetectGPT and IRT-Informed Detector Evidence for LLM-Generated Text Detection</a></td><td>12</td><td>0</td><td>NLP</td><td>LLM 생성 텍스트 검출 Bayesian 융합임</td></tr>
<tr><td>601</td><td><a href='https://arxiv.org/abs/2611.16051'>Human-Likeness and Conversational Preference Diverge for Synthesized Agent Speech in Customer-Service Calls</a></td><td>12</td><td>0</td><td>Speech</td><td>합성 음성 인간다움과 선호 분리 분석임</td></tr>
<tr><td>602</td><td><a href='https://arxiv.org/abs/2611.16104'>Show Your Work in Swahili: Reinforcement Learning for Native-Language Mathematical Reasoning</a></td><td>12</td><td>0</td><td>NLP</td><td>스와힐리어 수학 추론 RL 레시피임</td></tr>
<tr><td>603</td><td><a href='https://arxiv.org/abs/2611.16968'>Morphological Simplification in Alzheimer&#x27;s Disease: Computational Analysis and Identification From Connected Speech</a></td><td>12</td><td>0</td><td>NLP</td><td>Cookie Theft 발화에서 형태론 지표로 알츠하이머를 구분하는 언어학 분석이며 로봇과 무관함</td></tr>
<tr><td>604</td><td><a href='https://arxiv.org/abs/2611.15716'>A Reliability Study of Explainable AI for Freight Mode Classification</a></td><td>12</td><td>0</td><td>LG</td><td>화물 운송 수단 분류에서 SHAP, LIME 설명의 안정성과 faithfulness를 점검한 응용 연구임. 로봇 관련성 없고 방법론 기여도 작음</td></tr>
<tr><td>605</td><td><a href='https://arxiv.org/abs/2611.16455'>Rational Alignments of Superintelligences via Debates</a></td><td>12</td><td>0</td><td>Theory</td><td>debate 프레임워크에서 subgame perfect equilibrium으로 ASI 정렬을 논하는 게임이론 이론 글임. 실험이 없고 로봇과 무관함</td></tr>
<tr><td>606</td><td><a href='https://arxiv.org/abs/2611.16499'>Recalibrating a Typed-Decision Model in an Afternoon: A Hands-On Recipe for Laya&#x27;s Confidence Scores</a></td><td>12</td><td>0</td><td>NLP</td><td>Laya 확신도 점수를 bucket별 temperature scaling으로 보정하는 numpy 튜토리얼이며 저자도 새로운 방법이 없다고 밝힘. 로봇과 무관함</td></tr>
<tr><td>607</td><td><a href='https://arxiv.org/abs/2611.17186'>Cortex-FL: Agent-Mediated Collaboration for Federated Learning</a></td><td>12</td><td>0</td><td>Federated</td><td>Cortex-FL은 자연어 목표를 받아 agent가 협력자 탐색과 계약, 학습, 블록체인 정산까지 진행하는 federated learning 시스템이며 4노드 시연만 있음. 시스템 소개 수준이고 로봇과 무관함</td></tr>
<tr><td>608</td><td><a href='https://arxiv.org/abs/2611.17235'>Al-Ghasali: A Computational Framework for Simulating Islamic Jurisprudential Rulings via Finite State Automata and Large Language Models</a></td><td>12</td><td>0</td><td>Formal Methods</td><td>이슬람 법 규정을 finite state automata로 정식화하고 grammar-guided decoding으로 LLM 환각을 막는다고 증명하는 형식 이론 글임. 실험 검증이 없고 로봇과 무관함</td></tr>
<tr><td>609</td><td><a href='https://arxiv.org/abs/2611.15991'>Adaptive Distance Detection and Adaptive Instance Segmentation</a></td><td>10</td><td>0</td><td>CV</td><td>Counter Strike 게임에서 YOLOv5s 검출과 semantic segmentation의 추론 시간을 비교한 소규모 기술 보고임</td></tr>
<tr><td>610</td><td><a href='https://arxiv.org/abs/2611.16620'>Improved CNN-Transformer Network for Neutron Image Super-Resolution</a></td><td>10</td><td>0</td><td>CV</td><td>중성자 영상 초해상도를 위해 CRAFT 기반 CNN-Transformer에 모듈 세 개를 얹은 incremental 연구로 로봇과 무관함</td></tr>
<tr><td>611</td><td><a href='https://arxiv.org/abs/2611.16907'>Automated PD-L1 Tumor Proportion Scoring with Uncertainty-Guided Triage in Non-Small Cell Lung Cancer</a></td><td>10</td><td>0</td><td>CV</td><td>PD-L1 종양 비율 점수를 세포 계수와 모델 불일치 기반 uncertainty triage로 산출하는 병리 영상 연구로 로봇과 무관함</td></tr>
<tr><td>612</td><td><a href='https://arxiv.org/abs/2611.16955'>A Disease-specific Retinal Aging Biomarker for Predicting Progression to Late Age-related Macular Degeneration</a></td><td>10</td><td>0</td><td>CV</td><td>안저 영상으로 AMD 진행을 예측하는 retinal age 지표 FAA를 학습해 Cox 모델 C-index를 0.836에서 0.888로 올린 의료 연구로 로봇과 무관함</td></tr>
<tr><td>613</td><td><a href='https://arxiv.org/abs/2611.17105'>Predicting Ethanol Drinking Status from Nonhuman Primate Liver Histology: A Proof of Concept for Parameter-efficient Fine-tuning in Few-Shot Vision-Language Modeling</a></td><td>10</td><td>0</td><td>Multimodal</td><td>원숭이 간 조직 WSI로 음주 여부를 few-shot VLM과 PEFT adapter로 예측하는 3쪽짜리 의료 개념 검증으로 로봇과 무관함</td></tr>
<tr><td>614</td><td><a href='https://arxiv.org/abs/2611.17199'>MALNISI-Infused Graph Construction and Weighted Contrastive Loss based GAT for Unsupervised Representation Learning in HSI</a></td><td>10</td><td>0</td><td>CV</td><td>초분광 영상 픽셀 유사도 지수 MALNISI로 그래프를 만들고 GAT와 weighted contrastive loss로 표현을 학습하는 incremental 연구로 로봇과 무관함</td></tr>
<tr><td>615</td><td><a href='https://arxiv.org/abs/2611.15106'>Profile-Based Auditing of Domestic Violence Survey Selection Across South Asia</a></td><td>10</td><td>0</td><td>LG</td><td>설문 선택 편향 감사임</td></tr>
<tr><td>616</td><td><a href='https://arxiv.org/abs/2611.16058'>Human Capital in Context: What Employment Survival Reveals About Worker-Firm Match</a></td><td>10</td><td>0</td><td>LG</td><td>노동 시장 생존 분석임</td></tr>
<tr><td>617</td><td><a href='https://arxiv.org/abs/2611.16201'>An Extensive Evaluation of Machine Learning and Deep Learning Approaches for Sentiment Analysis: Insights from Amazon Customer Reviews</a></td><td>10</td><td>0</td><td>NLP</td><td>감성 분석 ML 비교 평가임</td></tr>
<tr><td>618</td><td><a href='https://arxiv.org/abs/2611.16239'>Optimal feature selection for firewall log analysis using Machine learning and Hybrid Metaheuristic algorithms</a></td><td>10</td><td>0</td><td>LG</td><td>방화벽 로그 feature selection임</td></tr>
<tr><td>619</td><td><a href='https://arxiv.org/abs/2611.16648'>GNN-Enhanced TCN Algorithms for ECG Anomaly Detection</a></td><td>10</td><td>0</td><td>LG</td><td>ECG 이상 탐지 GNN TCN임</td></tr>
<tr><td>620</td><td><a href='https://arxiv.org/abs/2611.17121'>Using an energy pixels approach to estimate the size a 2nd Generation DEL must be to train a high-resolution binding model</a></td><td>10</td><td>0</td><td>LG</td><td>DNA-encoded library 모델 크기 추정으로 무관함</td></tr>
<tr><td>621</td><td><a href='https://arxiv.org/abs/2611.14935'>Do Large Language Models Show Racial and Sex Bias in Pain Management? A Counterfactual Audit of GPT, Claude, Gemini, Llama, DeepSeek and Qwen</a></td><td>10</td><td>0</td><td>NLP</td><td>통증 관리 LLM 편향 counterfactual 감사임</td></tr>
<tr><td>622</td><td><a href='https://arxiv.org/abs/2611.15114'>What Does Each Part of Speech Need? Contexts, Subspaces and Dimensions in Static Word Embeddings</a></td><td>10</td><td>0</td><td>NLP</td><td>정적 word embedding 품사별 분석임</td></tr>
<tr><td>623</td><td><a href='https://arxiv.org/abs/2611.15904'>HeriKGQA: Grounded Knowledge-Graph Question Answering over Cultural Heritage Sensor Data</a></td><td>10</td><td>0</td><td>NLP</td><td>문화유산 센서 데이터 KGQA임</td></tr>
<tr><td>624</td><td><a href='https://arxiv.org/abs/2611.16612'>Unibuc - NLP at &quot;Voight-Kampff&quot; Generative AI Detection PAN 2025</a></td><td>10</td><td>0</td><td>NLP</td><td>PAN 2025 생성 AI 텍스트 탐지 대회 참가 보고로 LLM embedding에 LightGBM 등 앙상블을 붙인 표준적 접근임</td></tr>
<tr><td>625</td><td><a href='https://arxiv.org/abs/2611.17098'>Speed-to-Power Dominates Energy Costs for AI Data Centers: Technoeconomic Analysis of Powering AI in the Continental United States</a></td><td>10</td><td>0</td><td>Energy</td><td>AI 데이터센터의 전력 조달을 grid, 태양광 저장, 가스 발전으로 비교해 배치 속도를 반영한 에너지 비용을 계산한 기술경제 분석임. 로봇 연구와 무관함</td></tr>
<tr><td>626</td><td><a href='https://arxiv.org/abs/2611.14993'>Validation of a Facial-Video Digital Hydration Biomarker Score for Tracking Hydration State Transitions in a Real-World Fasting Model</a></td><td>8</td><td>0</td><td>CV</td><td>얼굴 영상 점수로 단식 후 수분 상태 변화를 추적한 임상 검증 연구라 로봇과 무관함</td></tr>
<tr><td>627</td><td><a href='https://arxiv.org/abs/2611.15184'>GingivitisSeg: A Public Dataset and Comparative Benchmark for Gingivitis Segmentation in Intraoral Images</a></td><td>8</td><td>0</td><td>CV</td><td>구강 사진 961장의 치은염 분할 dataset과 7개 segmentation 모델 비교 benchmark라 로봇과 무관함</td></tr>
<tr><td>628</td><td><a href='https://arxiv.org/abs/2611.15278'>PCLSegNet: Anatomy-Aware Deep Learning Framework for MRI-based Pancreatic Cyst Segmentation and Size Assessment</a></td><td>8</td><td>0</td><td>CV</td><td>췌장 낭종의 MRI 분할을 위한 anatomy-aware 2단계 네트워크와 class 가중 손실이라 로봇과 무관한 의료 영상 연구임</td></tr>
<tr><td>629</td><td><a href='https://arxiv.org/abs/2611.17104'>TuMAP: A Dual-View, Morphotype-Aware Pathomics Pipeline for Quantifying Renal Tubular Remodeling</a></td><td>8</td><td>0</td><td>CV</td><td>신장 조직 세뇨관 456,158개를 foundation model 표현으로 morphotype 분류하는 병리 분석 파이프라인으로 로봇과 무관함</td></tr>
<tr><td>630</td><td><a href='https://arxiv.org/abs/2611.14590'>An Asynchronous Federated Learning Platform for Lung Adenocarcinoma Grading via Foundation Models and Structural Pruning</a></td><td>8</td><td>0</td><td>LG</td><td>폐 선암 등급 분류를 위해 UNI2와 CLAM-SB를 쓰는 비동기 federated learning 웹 플랫폼과 가지치기 비교로 로봇과 무관함</td></tr>
<tr><td>631</td><td><a href='https://arxiv.org/abs/2611.15232'>Winter wheat improves soil carbon sequestration with reduced gains in warmer climates</a></td><td>8</td><td>0</td><td>LG</td><td>밀 재배와 토양 탄소 분석임</td></tr>
<tr><td>632</td><td><a href='https://arxiv.org/abs/2611.15378'>A Modified Glicko Model for Rating Soccer Clubs and National Teams Worldwide</a></td><td>8</td><td>0</td><td>LG</td><td>축구 팀 rating 모델임</td></tr>
<tr><td>633</td><td><a href='https://arxiv.org/abs/2611.16750'>Interpretable machine learning diagnosis of degradation mechanisms in lead-free $RbSn_{0.5}Ge_{0.5}I_{3}$ solar cells from temperature- and illumination-dependent electrical measurements</a></td><td>8</td><td>0</td><td>LG</td><td>태양전지 열화 ML 진단임</td></tr>
<tr><td>634</td><td><a href='https://arxiv.org/abs/2611.15172'>Where Language-Model Vocabulary Rose on Stack Exchange</a></td><td>8</td><td>0</td><td>NLP</td><td>Stack Exchange 어휘 변화 분석임</td></tr>
<tr><td>635</td><td><a href='https://arxiv.org/abs/2611.15408'>AraCrypto-ML: A Multi-Label Corpus of Communicative Functions in Arabic Facebook Cryptocurrency Discourse</a></td><td>8</td><td>0</td><td>NLP</td><td>아랍어 암호화폐 담론 코퍼스임</td></tr>
<tr><td>636</td><td><a href='https://arxiv.org/abs/2611.15587'>VWEN: A Curated Small Language Model for Vietnamese Paraphrasing</a></td><td>8</td><td>0</td><td>NLP</td><td>베트남어 paraphrase 소형 모델임</td></tr>
<tr><td>637</td><td><a href='https://arxiv.org/abs/2611.15639'>ChJGBench: A Comprehensive Benchmark for Chinese Legal Judgment Generation with Diagnostic Evaluation</a></td><td>8</td><td>0</td><td>NLP</td><td>중국 법률 판결 생성 benchmark임</td></tr>
<tr><td>638</td><td><a href='https://arxiv.org/abs/2611.15691'>Dynamic Block-Online Streaming ASR for Low-Resource Agglutinative Code-Switching Speech with Morphology-Aware Evaluation</a></td><td>8</td><td>0</td><td>Speech</td><td>저자원 교착어 streaming ASR임</td></tr>
<tr><td>639</td><td><a href='https://arxiv.org/abs/2611.15804'>Computational Explanations of Semantic Universals</a></td><td>8</td><td>0</td><td>NLP</td><td>의미 보편성의 계산적 설명임</td></tr>
<tr><td>640</td><td><a href='https://arxiv.org/abs/2611.15971'>Better Boundary Prediction Does Not Guarantee Better Structural Representation</a></td><td>8</td><td>0</td><td>NLP</td><td>경계 예측과 구조 표현의 관계 분석임</td></tr>
<tr><td>641</td><td><a href='https://arxiv.org/abs/2611.16139'>Temporal Context-Aware Spam Detection Using Transformer-Based NLP Models</a></td><td>8</td><td>0</td><td>NLP</td><td>시간 맥락 스팸 탐지임</td></tr>
<tr><td>642</td><td><a href='https://arxiv.org/abs/2611.16260'>Low Language Transfer Speech-to-Text</a></td><td>8</td><td>0</td><td>Speech</td><td>저전이 음성 인식 전이 분석임</td></tr>
<tr><td>643</td><td><a href='https://arxiv.org/abs/2611.16173'>Between Niti and Nyaya: A Society-Centered Framework for AI Governance</a></td><td>8</td><td>0</td><td>Policy</td><td>AI 거버넌스 정책을 notice, challenge, correction 기준으로 평가하는 프레임워크를 노스캐롤라이나 사례에 적용한 사회과학 연구임. 로봇 연구와 무관함</td></tr>
<tr><td>644</td><td><a href='https://arxiv.org/abs/2611.16986'>Primer: An AI Framework for Instructor-Centered Educational Simulation Creation</a></td><td>8</td><td>0</td><td>Education</td><td>교육자가 LLM 다중 agent로 교육 시뮬레이션을 만드는 오픈소스 시스템 Primer임. 평가 실험이 없는 시스템 소개이고 로봇과 무관함</td></tr>
<tr><td>645</td><td><a href='https://arxiv.org/abs/2611.15661'>ALMeD: Medieval French Gold-Standard</a></td><td>5</td><td>0</td><td>NLP</td><td>중세 프랑스어 gold-standard 코퍼스임</td></tr>
<tr><td>646</td><td><a href='https://arxiv.org/abs/2611.15961'>Is Spoken Hungarian Low-resource?: A Quantitative Survey of Hungarian Speech Data Sets</a></td><td>5</td><td>0</td><td>Speech</td><td>헝가리어 음성 데이터셋 조사임</td></tr>
</tbody></table>

</details>
