# 오늘의 arXiv Top 15: 2026-11-23 (월)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**

**신규 논문 수: 전체 442편 → 중복 제거 후 442편 (이번 평가 대상 442편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 132 |
| cs.LG | 96 |
| cs.RO | 69 |
| cs.CL | 58 |
| cs.AI | 87 |

---

## Top 15

### 1. Beyond Linear Decodability: Understanding and Improving Instruction Following in World Action Models (78점)

[arXiv](https://arxiv.org/abs/2611.27401) · [PDF](https://arxiv.org/pdf/2611.27401) · [alphaXiv](https://www.alphaxiv.org/abs/2611.27401) (요약 있음) · [프로젝트 페이지](https://ruflect-intelligence.github.io/LDS-Homepage/)

- **저자**: Bokai Ji, Jiapeng Chen, Yi Zhang, Zeyuan Ding, Yong Dai, Xiaozhu Ju, Jian Tang, Lemao Liu 외 2명
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> world action model이 말로 지정한 물체를 무시하고 학습 때 익힌 물체로 가는 문제를, 중간 표현에서 지시 대상을 선형으로 읽어 내게 하는 보조 loss로 줄임. LIBERO-CF 평균 성공률이 InternW0-Δ 기준 23.5%에서 74.6%로 오름.

**무슨 문제인가**

world action model(WAM: 영상 생성 모델 위에서 미래 영상과 action을 함께 생성하는 robot policy)은 조작은 잘하지만, 같은 장면에서 다른 지시를 주면 학습 때의 행동을 되풀이함. 앞선 연구는 이런 모델 내부에도 지시 대상 정보가 들어 있지만 행동을 바꾸지는 못한다고 보고했음(encoded but not in control). 이 해석이 맞다면 표현을 고쳐도 소용이 없고, 다른 지시마다 새 demonstration을 모아야 함. 공개 dataset은 원래 장면을 다시 만들 수 없는 경우가 많아 이 방법은 쓰기 어려움.

**어떻게 푸나**

저자들은 먼저 같은 장면에 지시만 다른 demonstration(counterfactual demonstration)으로 fine-tuning한 지시 따르는 모델과 원래 모델을 비교함. 두 모델 모두 지시 대상 정보를 담고 있었지만, linear probe로 읽은 정확도는 원래 모델 51.5%, 지시 따르는 모델 77.5%로 차이가 났음. 이를 근거로 LDS(Linear Decodability Supervision)를 만듦. LDS는 Wan 기반 DiT의 9, 19, 29번째 block 출력에 공유 linear head를 붙임. head는 첫 denoising step의 visual token마다 4×4 격자로 지시 대상, 다른 후보 물체, 배경을 가려 냄. 이 loss를 원래 flow-matching loss에 0.25 가중치로 더함. 추가 데이터는 기존 관측에 다른 지시와 대상 mask만 짝지은 것이고 action이나 미래 영상은 없음. head는 추론 때 떼어 냄. 저자들은 결과를 설명하려고 표현 안에 학습 습관 쪽 신호(prior tag P)와 지시 쪽 신호(instruction tag I)가 더해져 경쟁한다는 가설을 세움.

**결과**

- LIBERO-CF(LIBERO 장면에 다른 실행 가능한 목표를 지시해 학습 과제를 되풀이하는지 보는 benchmark) 평균 지시 성공률이 InternW0-Δ에서 23.5%에서 74.6%로, OpenWAM에서 5.1%에서 65.1%로 오름. 가장 강한 VLA baseline(π0.5 + SAM)의 47.8%보다 26.8퍼센트포인트 높음. 원래 LIBERO 40개 과제 성공률은 96.0%에서 96.8%로 유지됨.
- 학습 없이 OpenWAM 8번째 block 표현만 고친 실험도 가설을 뒷받침함. LIBERO-CF 물체 집기 subset에서 성공률이 3.8%에서 I를 32배 더하면 53.0%로, P 방향을 지시 대상으로 옮기면 50.8%로 오름. 이 편집은 정답 mask를 써서 넣은 진단용임.
- RoboTwin-IF(저자들이 만든 양팔 조작 benchmark, 같은 첫 관측에 지시만 다름)에서 trajectory가 없는 지시의 평균 성공률이 OpenWAM 7.6%에서 54.4%로 오름. 다른 WAM인 LingBot-VA는 LDS를 적용해도 놓기 과제 성공률이 14.4%에서 13.2%로 내려감.
- 실제 AgileX 양팔 로봇에서 빨간 버튼 누르기만 학습시키고 초록·파란 버튼을 지시함. OpenWAM, LingBot-VA, InternW0-Δ 세 WAM 모두 LDS 후 10회 중 10회 성공함. LDS 전에는 0%, 0%, 40%였음.

**한계**

표현 분석과 학습 없는 편집은 OpenWAM LIBERO checkpoint 하나, 두 후보 장면 132개, 장면당 rollout 1회로 한 것임. prior 신호와 연관된 성분(U)에는 prior 신호와 물체 외형 차이가 섞여 있어 둘을 따로 떼어 내지 못함. 처음 보는 장면에서는 성공률이 LIBERO-CF 67.7%, LangGap(지시 일반화 benchmark) 45.8%로 내려감. 실로봇은 과제 2개, 과제당 10회뿐이고 Wan 기반 WAM에만 해당한다고 저자가 밝힘. RoboTwin-IF는 아직 공개되지 않았음.

**누리랩 연구와의 연결**

- 지시를 무시하는 실패를 내부 표현의 두 성분 경쟁으로 진단하고, 표현 편집으로 원인을 확인하는 절차를 보여 줌. failure detection·diagnosis 연구에서 실패 원인을 표현 수준에서 찾는 방법으로 가져다 쓸 수 있음.
- action label 없이 대상 mask만으로 VLA/WAM의 grounding을 고침. 같은 장면에서 지시만 바꾼 counterfactual 평가와 학습 없는 표현 편집은 test-time steering 연구와 바로 이어짐.

*대표 그림: 세 칸으로 된 개요 그림임. (a)는 지시 따르는 모델이 층과 연산 위치 전반에서 probe 정확도가 높게 나온 heatmap과, LDS 후 LIBERO-CF 성공률 5.1%에서 65.1%, grounding 14.4%에서 90.3%로 오른 막대를 보여 줌. (b)와 (c)는 지시 신호 I와 prior 신호 P의 경쟁 가설과 LDS가 I를 키운다는 해석을 그린 개념도이고, 막대 일부만 측정값임.*

---

### 2. LoCo-WAM: Test-Time Training as Long Context for World-Action Models (78점)

[arXiv](https://arxiv.org/abs/2611.26853) · [PDF](https://arxiv.org/pdf/2611.26853) · [alphaXiv](https://www.alphaxiv.org/abs/2611.26853)

- **저자**: Sheng Cheng, Deqian Kong
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 70점
- **읽은 원문**: PDF 전문

> world-action model이 실행 중에 방금 관측한 frame으로 video 예측 부분을 조금씩 학습하게 해서, 짧은 history만 보는 모델이 긴 history 모델만큼 행동하게 함. RoboCasa GR-1에서 2.4초 history 모델의 성공률이 67.9%에서 73.6%로 올라 9.6초 history 모델(73.5%)과 같아짐.

**무슨 문제인가**

world-action model은 다음 장면을 영상으로 예측하고 그 예측을 보고 행동을 고르는 robot policy임. 대부분 짧은 관측 history만 입력으로 받으므로, 이미 끝낸 단계처럼 화면에서 사라진 정보는 행동에 반영하지 못함. history를 늘리면 결정마다 처리할 token이 늘고, history 길이마다 모델을 따로 학습해야 하는 경우도 있음. history를 골라 쓰거나 압축하는 방법은 그 module을 policy와 함께 학습해야 함.

**어떻게 푸나**

LoCo-WAM(Long Context World-Action Model)은 모델 구조와 history 길이는 그대로 두고, 실행 중에 test-time training을 함. test-time training은 정답 label 없이 self-supervised loss로 test 입력마다 모델을 갱신하는 방법임. 대상 모델은 다음 frame의 latent를 예측하는 video expert와, history와 이 예측을 보고 action chunk를 만드는 action expert로 나뉨. 결정마다 이미 관측이 끝난 가장 최근 구간을 골라, 그 앞 history로 그 구간의 frame을 예측하도록 video expert에 붙인 LoRA(low-rank adapter)를 gradient 한 step 갱신함. loss는 사전학습 때 쓴 video flow matching loss를 그대로 씀. 갱신된 video expert는 상상한 미래와 action expert가 읽는 feature를 모두 바꾸고, action expert 자체는 고정함. adapter는 episode 안에서 누적되고 episode가 시작할 때마다 0으로 되돌림. 그래서 입력 창을 벗어난 과거 관측도 adapter 가중치를 통해 행동에 영향을 줌.

**결과**

- RoboCasa GR-1(GR-1 humanoid의 탁상 조작 과제 24개)에서 긴 history용으로 나온 기존 world-action model인 Long-WAM에 적용해 성공률을 잼. 4.8초 history 모델은 71.1%에서 78.3%로 올라, 따로 학습한 9.6초 history 모델(73.5%)보다 4.8퍼센트포인트 높음. 결정당 지연은 9.6초 모델 0.67초 대비 0.77초이고, 비동기 갱신을 쓰면 0.64초임.
- 같은 2.4초 history 조건에서 다른 test-time 방법과 비교함. LoCo-WAM은 5.7퍼센트포인트를 올리고, 여러 episode에 걸쳐 world model을 적응시키는 AdaWorldPolicy는 2.5, fast-weight layer를 meta-training하는 RoboTTT는 3.8퍼센트포인트를 올림. RoboTTT는 약 136 GPU-hour의 meta-training이 필요함.
- LIBERO-Mem(같은 물체를 반복 조작해서 현재 화면만으로는 진행 단계를 알 수 없는 Franka 과제 10개)에서 LingBot-VA로 잼. 8-chunk history 모델 성공률이 27.5%에서 32.2%로 올라 기본 30-chunk history 모델(32.2%)과 같아짐.
- 관측 frame 대신 모델 자신의 예측을 학습 target으로 쓰면 성공률이 70.8%로 base model(71.1%) 수준에 머묾. 갱신을 4번째 결정 뒤에 멈추면 72.9%로 내려가므로, 성능 향상은 episode 내내 실제 관측으로 학습하는 데서 나옴.

**한계**

실험은 시뮬레이션 benchmark 4개뿐이고 실로봇 결과는 없음. RoboCasa365와 RoboTwin 2.0(양팔 조작 과제 50개 중 가장 어려운 8개)에서는 향상이 0.8에서 1.4퍼센트포인트로 작고, 표준편차와 비슷한 크기임. learning rate를 3분의 1로 줄이면 72.8%로 내려가는 등 benchmark마다 learning rate를 따로 골라야 하며, 본문에 코드 공개 주소는 없음.

**누리랩 연구와의 연결**

- 실제 관측과 예측의 차이로 실행 중에 world model을 고치는 방식이라, 누리랩의 test-time optimization과 robot memory 연구에서 바로 비교 대상이 됨. adapter 가중치를 episode memory로 쓰는 구조는 history 압축 방식과 대조 실험을 짜기 좋음.
- 결정마다 계산하는 video loss 감소량은 예측이 실제와 어긋나는 정도를 나타냄. 이 값을 failure detection 신호로 쓸 수 있는지 시험해 볼 만함.

*대표 그림: RoboCasa GR-1의 두 과제(캔을 서랍에 넣기, 피망을 바구니로 옮기기)를 같은 초기 상태에서 실행한 그림임. LoCo-WAM을 쓰지 않은 실행을 위 줄에, 쓴 실행을 아래 줄에 2초 간격으로 보여 줌. 두 실행이 처음 갈라지는 시점(4초, 6초)은 주황색으로, LoCo-WAM이 성공한 frame(11초, 12초)은 초록색으로 표시했고, 갱신 없는 실행은 끝내 실패함.*

---

### 3. Tripwire: Robot Agents that Program Their Own Interrupts under Human Disturbance (74점)

[arXiv](https://arxiv.org/abs/2611.27182) · [PDF](https://arxiv.org/pdf/2611.27182) · [alphaXiv](https://www.alphaxiv.org/abs/2611.27182)

- **저자**: Sunli Chen, Yun Zong, Qinhong Zhou, Xiaowen Qiu, Jiaben Chen, Zeyuan Yang, Chuang Gan
- **분야**: Embodied AI · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> agent가 VLA를 호출할 때마다 실행 중 상황을 감시하는 작은 Python 프로그램(tripwire)을 직접 써서 붙이고, 조건이 맞으면 policy를 즉시 멈추고 agent를 깨우게 함. 사람이 방해하는 시뮬레이션 주방에서 같은 agent를 쓴 turn 단위 방식 대비 사람과 닿지 않은 episode 비율이 61.3%에서 81.3%로 오름.

**무슨 문제인가**

VLM agent가 사전학습된 VLA를 tool로 부르는 기존 harness는 turn 단위로 동작함. agent는 policy 호출이 끝나야 다시 판단할 수 있으므로, 호출 도중 사람이 길을 막거나 잡으려던 물체를 옮겨도 알지 못함. agent를 더 자주 부르면 이 공백은 줄지만, 판단 한 번에 몇 초가 걸리고 대부분의 control step에서는 새 판단이 필요 없음. 저자들이 RoboCasa365(가정 주방 시뮬레이션 조작 과제 모음) 과제에 반응형 사람 avatar를 넣자 가장 강한 policy의 성공률이 61.9%에서 20.8%로 내려가고, 약 절반의 episode에서 사람과 닿음.

**어떻게 푸나**

TRIP은 학습 없이 기존 policy를 그대로 감싸는 event 기반 harness임. agent는 매 호출마다 실행할 동작(VLA 호출, base·arm 직접 이동, 대기)과 함께 tripwire를 씀. tripwire는 RGB-D 관측과 자기 memory를 입력으로 받아, 계속 진행이면 false를, 멈춰야 하면 이유를 적은 문장을 내는 stateful Python 함수임. tripwire 안에서는 작은 VLM(Qwen3.5-9B)에 사람 위치 같은 짧은 질문을 하고, 그 답을 depth·이전 거리·timer와 엮어 사람이 다가오는지 판단함. tripwire가 발동하면 harness가 action chunk 중간이라도 policy를 멈추고, 이유와 memory를 agent에게 넘김. agent는 상황을 다시 보고 피하기·기다리기·재개 중 하나를 고르며, 그 결정에 맞게 tripwire를 새로 씀. 예를 들어 기다리기로 하면 사람이 떠나는 순간을 감시하는 tripwire로 바꿈. 평가용으로 RoboHD(RoboCasa365 과제 42개에 사람 방해 4종을 넣은 장면 168개, 사람과 닿으면 실패)도 새로 만듦.

**결과**

- RoboHD에서 가장 강한 policy인 Xiaomi-Robotics-1(XR)을 감쌌을 때, 사람과 닿지 않은 episode 비율(safety)이 turn 단위 agent harness의 61.3%에서 81.3%로 오름. 두 방식은 agent·tool·prompt가 같고 agent를 부르는 시점만 다름.
- 같은 조건에서 사람이 있을 때 과제 성공률은 31.0%에서 38.7%로 오르고, 사람이 없을 때는 73.8% 대 73.2%로 비슷함. 분당 agent tool 호출은 30.3회에서 19.4회로 줄어듦.
- agent가 첫 turn에 쓴 tripwire를 끝까지 고정하면 safety가 61.3%, 성공률이 33.3%로 내려감. 사람이 0.6m 안에 있으면 무조건 멈추는 고정 규칙은 safety 86.0%를 얻지만 성공률이 16.1%로 내려감.
- 실제 xArm 7에서 π0.5로 머그 걸기·수건 걸기를 시험함. 과제 2개와 방해 조건 2개(사람이 팔을 막기, 물체를 옮기기)를 합친 40회 중 TRIP은 25회 성공했고, turn 단위 harness는 5회, policy 단독은 1회 성공함.

**한계**

사람은 motion-capture clip을 재생하는 avatar이고 충돌 body가 없어서 접촉을 기하 계산으로 판정함. 시뮬레이션에서는 agent와 VLM이 계산하는 동안 physics를 멈추므로, 로봇 시간 1.5분에 실제로는 약 12분이 걸리고 agent 지연은 결과에 반영되지 않음. 실로봇은 단일 과제 policy 2개와 저자 본인이 방해하는 조건뿐이고, 코드 공개 주소는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- failure detection/recovery를 학습된 detector가 아니라 agent가 상황마다 다시 쓰는 감시 프로그램으로 푼 사례임. VLA 실행 중 실패 징후 감지와 복구 시점 결정 연구에서 비교 대상으로 쓸 수 있음.
- tripwire memory가 호출 사이에 지워지고 agent가 필요한 정보를 코드 상수로 넘기는 구조는, robot memory를 어디에 둘지 설계할 때 참고할 수 있음.

*대표 그림: TRIP의 구성을 그린 개념도로, 측정 결과가 아니라 방법 구조를 그린 그림임. agent가 호출(policy, 직접 이동, 대기)과 tripwire를 함께 내리고, tripwire가 작은 VLM에 질문해 발동하면 harness가 호출을 멈추고 agent를 다시 부르는 흐름을 보여 줌.*

---

### 4. Coherent Moment Propagation: Epistemic Uncertainty for Pre-trained Robot Policies (74점)

[arXiv](https://arxiv.org/abs/2611.26855) · [PDF](https://arxiv.org/pdf/2611.26855) · [alphaXiv](https://www.alphaxiv.org/abs/2611.26855) · [프로젝트 페이지](https://comp-uq.github.io/comp-uq)

- **저자**: Miguel Saavedra-Ruiz, Anqi Li, Claudia D'Arpino, Alperen Degirmenci, Tucker Hermans, Fabio Ramos
- **분야**: Failure Detection · robotics relevance 9/10 · 1차 스크리닝 70점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> 학습이 끝난 flow matching 로봇 policy에서 epistemic uncertainty를 재는 기존 방법이 ODE 적분 step을 늘릴수록 0으로 줄어드는 문제를 증명하고, 상태와 가중치의 공분산을 함께 넘기는 방식으로 고침. LIBERO-90 실패 예측에서 timestep-wise accuracy가 0.643으로 비교한 post-hoc 방법 중 가장 높음.

**무슨 문제인가**

π0.5나 SmolVLA 같은 flow matching VLA는 행동을 내놓기만 하고, 그 행동을 믿어도 되는지는 알려 주지 않음. policy를 여러 개 학습하는 ensemble은 foundation policy 규모에서 비용이 커서, 학습된 policy 하나에서 불확실성을 뽑는 방법이 필요함. BayesDiff는 마지막 layer 가중치에 Laplace 근사로 Gaussian posterior를 두고, 적분 과정에서 상태의 평균과 분산을 함께 넘기는 기존 방법임. 그런데 BayesDiff는 매 step 가중치를 따로 적분해 없애므로, 같은 가중치가 궤적 전체를 만든다는 상관을 버림.

**어떻게 푸나**

저자는 먼저 BayesDiff가 계산하는 전체 분산(공분산 행렬의 trace)이 Euler step 수 T에 대해 O(1/T)로 줄어듦을 증명함. velocity field가 Lipschitz이고 예측 분산이 유계라는 두 가정만 씀. CoMP(Coherent Moment Propagation)는 Euler update를 평균 궤적과 MAP 가중치 주변에서 상태와 가중치 둘 다에 대해 선형화함. 그래서 상태 평균, 상태 공분산, 상태와 가중치 사이의 교차 공분산 세 가지를 step마다 행렬 곱으로 정확히 갱신함. 이 교차 공분산을 넘기면 전체 분산의 상한이 T와 무관해짐. CoMP-EKF(extended Kalman filter 방식)는 상태 Jacobian을 autodiff로 구함. CoMP-UKF(unscented Kalman filter 방식)는 action chunk를 펼친 차원 D에 대해 2D+1개 sigma point를 Euler map에 통과시킴. 여기에 VLA backbone이 이미 계산한 이미지·언어·proprioception embedding을 마지막 layer 입력에 붙이고 그 출력 가중치를 0으로 둔 augmented head를 씀. 이렇게 하면 policy를 다시 학습하지 않고 행동도 바꾸지 않으면서 posterior가 관측 차이를 반영함. 입력은 관측과 초기 noise이고, 출력은 action chunk와 그 공분산의 trace로 만든 uncertainty score임.

**결과**

- robomimic(시뮬레이션 조작 과제 모음)의 Lift, Can, Square에서 posterior 표본 6000개로 만든 기준 공분산과 비교함. BayesDiff는 과제에 따라 기준 분산의 6%에서 23%만 되살림. CoMP 두 방식은 기준 분산과 0.2% 안으로 맞음.
- LIBERO-90(시뮬레이션 조작 과제 90개 모음) 중 성공률 0.3에서 0.7인 과제 9개에서 π0.5의 실패를 미리 알아내는 실험을 함. CoMP-UKF의 timestep-wise accuracy(늦은 감지에 벌점을 주는 정확도)가 0.643임. 가장 강한 baseline인 VFD(적분 경로에서 ensemble 구성원 velocity field의 불일치를 더하는 방법)는 0.635, BayesDiff는 0.533임. 감지 정확도는 0.794로 GU(Gaussian entropy 기반 uncertainty 점수)의 0.770보다 높음.
- SmolVLA를 LIBERO-10에 fine-tuning할 demonstration을 uncertainty로 고르는 실험에서 CoMP-UKF는 무작위 선택보다 평균 3.5퍼센트포인트 높은 성공률을 얻음. augmented head를 쓴 BayesDiff는 선택 점수를 매길 때 적분 step을 10에서 50으로 늘리면 이득이 2.7에서 -2.9퍼센트포인트로 내려감. CoMP-UKF는 같은 조건에서 3.3에서 3.7퍼센트포인트를 유지함.

**한계**

모든 실험이 시뮬레이션이고 실로봇 결과는 없으며, 코드는 게재 후 공개 예정임. 연산 비용이 크고 action chunk 차원에 따라 늘어남. CoMP-UKF는 π0.5에서 결정당 1.85초가 걸리고, chunk가 5배 큰 SmolVLA에서는 3.38초와 4.6GB가 듦. robomimic에서는 따로 학습한 ensemble 두 개가 timestep-wise accuracy 0.687로 CoMP-UKF의 0.648보다 높음. 방법은 마지막 layer가 선형이라는 가정에 기댐.

**누리랩 연구와의 연결**

- VLA를 다시 학습하지 않고 실패 감지용 uncertainty를 얻는 방법이라 failure detection/recovery 연구의 baseline으로 바로 쓸 수 있음. step 수에 따라 BayesDiff 계열 점수가 줄어드는 문제는 우리 실험에서 점수를 비교할 때 확인해야 할 항목임.
- 모호한 언어 지시에서 uncertainty가 오르는 augmented head 결과는, 실패 직전에 사람에게 되묻거나 active perception으로 정보를 더 모으는 시점을 정하는 신호로 쓸 수 있음.

*대표 그림: 2차원 두 봉우리 분포를 배운 flow matching 모델에서 적분이 끝난 상태의 공분산을 방법별 타원으로 비교한 그림임. BayesDiff 타원은 기준보다 46배 작고 CoMP-EKF/UKF는 기준의 99%와 100%를 되살리며, 오른쪽 그래프는 step을 10에서 400으로 늘릴 때 BayesDiff 분산만 줄어드는 모습을 보임.*

---

### 5. A Plan or an Adversarial Example? A Round-Trip Check for Latent World Models (74점)

[arXiv](https://arxiv.org/abs/2611.27124) · [PDF](https://arxiv.org/pdf/2611.27124) · [alphaXiv](https://www.alphaxiv.org/abs/2611.27124) (요약 있음)

- **저자**: Huiyuan Tian, Chih-Yung Wen, Shijian Li
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 68점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> latent world model로 plan을 오래 탐색하면 model은 목표에 닿는다고 예측하지만 실제로는 실패하는 plan이 생김을 측정하고, 예측 상태에서 행동을 다시 읽어 어긋나면 벌점을 주는 round-trip check로 고침. DINO-WM의 Wall 과제에서 재계획 없는 최종 plan 성공률이 0.39에서 0.76으로 오름.

**무슨 문제인가**

DINO-WM, LeWM 같은 latent world model은 visual encoder의 feature 공간에서 행동열의 미래를 예측하고, CEM(cross-entropy method) 같은 planner가 예측된 미래가 목표에 가장 가까운 행동열을 찾음. 이 탐색은 classifier 점수가 오르도록 이미지를 최적화하는 것과 구조가 같아서, model 오차를 파고드는 plan이 나올 수 있음. 저자는 model이 성공을 예측하지만 실행하면 실패하는 plan을 adversarial plan이라 부름. 기존 benchmark는 재계획을 포함한 episode 성공률만 보고하므로, 한 번의 탐색이 이런 plan으로 끝나는 빈도는 드러나지 않았음.

**어떻게 푸나**

먼저 진단 test를 둠: planner를 한 번 돌리며 매 반복의 plan을 simulator에서 실행하고, 어떤 반복에서 풀었다가 최종 plan이 놓친 문제의 비율(adversarial rate)을 잼. 수리에는 inverse-dynamics model(IDM: 연속한 두 상태에서 그 사이 행동을 추정하는 network)을 씀. 대상 world model들은 환경 행동 5개 묶음(block)마다 latent 상태 하나를 예측하므로, 두 상태가 정하는 것은 block 안 행동들의 합뿐임. 그래서 IDM은 개별 행동 대신 block 행동 합을 예측하는 2층 MLP로 만들고, world model의 학습 데이터로 학습함. planning 중에는 후보 plan의 예측 상태 쌍마다 IDM이 읽은 합과 계획한 합의 제곱 차이를 평균해 residual r을 구함. r은 후보들 사이 표준편차의 비로 정규화해 예측 cost에 더하고, 조절할 hyperparameter는 가중치 β 하나임. world model은 다시 학습하지 않음.

**결과**

- world model·과제·planner 조합 13개 중 7개에서, 어떤 반복에서 풀었던 문제의 14~68%를 최종 plan이 잃음. DINO-WM Wall의 CEM 성공률은 11번째 반복의 0.56에서 30번째 반복의 0.39로 내려감. 예측 cost, OOD 점수, 행동 크기 점수 중 어느 것도 실패 plan을 가려내는 AUROC가 0.63을 넘지 못함.
- 재계획 없이 CEM 30회 반복 뒤 최종 plan을 실행한 성공률은 Wall(DINO-WM, 벽의 문을 지나 목표로 가는 2D navigation)에서 0.39에서 0.76으로 오름. Cube(LeWM, 로봇 팔로 큐브를 목표 위치로 옮기는 조작)에서는 0.64에서 0.79로 오름. 행동 하나하나를 맞추는 기존 방법 ACID의 per-action target(IDM이 개별 행동을 맞추게 함)은 같은 조건에서 0.64와 0.71임.
- JEPA-WM의 Wall에서 MPPI(sampling 기반 trajectory 최적화 planner) 성공률이 0.56에서 0.94로 오름. 재계획(MPC)을 하는 Cube에서는 CEM 성공률이 0.70에서 0.81로 오름. 추가 planning 시간은 0.2~3.1%임.
- Wall의 실패 원인은 학습 데이터의 공개된 학습 데이터의 위치 label이 frame과 맞지 않는 것이었음. label을 고쳐 fine-tuning한 model은 0.82이고, check는 label 수정 없이 0.76에 도달함.

**한계**

실험은 모두 시뮬레이션의 2D navigation과 단순 조작 과제이고 실로봇 결과는 없음. adversarial rate가 8% 이하인 planner 6개에서는 이득이 없고, DINO-WM PointMaze는 1.00에서 0.92로, JEPA-WM PushT는 0.67에서 0.52로 내려감. block 합 target은 행동이 block 안에서 더해지는 과제를 가정하며, 관절 torque를 쓰는 Reacher에서는 0.37에서 0.41로 이득이 작음. 재계획을 하는 Wall에서는 0.88 대 0.89로 차이가 없음.

**누리랩 연구와의 연결**

- 탐색을 더 할수록 실행 성공률이 내려가는 현상과 매 반복 plan을 실행해 재는 adversarial rate는, world model 기반 test-time planning 연구에서 planner를 평가하는 지표로 바로 쓸 수 있음.
- 예측 상태에서 행동을 다시 읽는 일관성 residual은 world model rollout의 failure detection 신호 후보임. 다만 저자는 r을 개별 plan 판별기로 평가하지 않았으므로 그 용도는 따로 검증해야 함.

*대표 그림: 측정 결과 그래프가 아니라 round-trip check의 구조를 그린 그림임: (a)는 고정된 world model의 예측 상태 쌍에서 inverse dynamics network가 행동 합을 읽어 residual r을 cost에 더하는 흐름임. (b)는 Wall 문제에서 CEM 단독 plan(r=20.2)과 check를 쓴 plan(r=0.17)의 예측 상태와 행동 합을 비교하고, (c)는 여러 행동열이 같은 두 상태를 잇지만 그 합만 정해짐을 보임.*

---

### 6. Skill-JEPA: Learning Planner-Aligned Action Spaces for World Models (74점)

[arXiv](https://arxiv.org/abs/2611.26825) · [PDF](https://arxiv.org/pdf/2611.26825) · [alphaXiv](https://www.alphaxiv.org/abs/2611.26825)

- **저자**: Tomás Couso Coddou, Christ Devia, Rex G. Liu, Rodrigo Toro Icarte
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 68점
- **읽은 원문**: PDF 전문

> JEPA world model이 raw action 대신 Gaussian prior를 가진 latent skill을 입력으로 받게 바꿔서, planner가 뽑는 후보가 model의 학습 분포 안에 들어오게 함. planner를 고치지 않고도 80 step 떨어진 목표의 평균 성공률이 42%에서 62%로 오름.

**무슨 문제인가**

JEPA(Joint-Embedding Predictive Architecture) world model은 이미지를 latent로 바꾸고 action을 넣었을 때 다음 latent를 예측함. 목표에 가려면 CEM 같은 sampling 기반 planner가 Gaussian에서 action 후보를 많이 뽑고 model로 결과를 예측해 가장 좋은 것을 고름. 그런데 model은 데이터에 있던 구조적이고 상태에 따라 달라지는 action만 보았으므로, Gaussian 후보에 대한 예측은 믿기 어려움. 이 예측 오차가 rollout을 따라 쌓여서, raw action 기준 성공률은 20 step 목표에서 87%이던 것이 80 step 목표에서 42%로 내림.

**어떻게 푸나**

Skill-JEPA는 world model에 state-conditioned VAE 하나를 더함. VAE encoder는 현재 latent 관측과 4 step 길이의 action chunk를 받아 latent code(skill)로 바꾸고, decoder는 skill과 현재 latent 관측을 받아 action chunk를 다시 만듦. skill의 prior는 모든 상태에서 같은 표준 Gaussian N(0, I)로 고정함. predictor는 action chunk 대신 skill을 입력으로 받아 4 step 뒤 latent를 예측하고, 예측 오차·action 복원 오차·KL 항·기존 collapse 방지 항을 함께 end-to-end로 학습함. 추론 때는 planner를 그대로 두고 탐색 변수만 skill로 바꾸며, 첫 후보를 N(0, I)에서 뽑음. 고른 skill 계획은 predictor가 예측한 중간 latent를 decoder에 넣어 skill 하나씩 action으로 풀어 냄. 저자는 planner 첫 후보에 대한 예측 오차가 상한을 가짐을 이론으로 보임. 그 상한은 학습 데이터에서의 예측 오차와 KL 항으로 정해지는 penalty의 합임.

**결과**

- 표준 과제 4개(Cube: 로봇 팔 블록 조작, Push-T: T자 블록 밀기, Reacher: 2관절 팔 제어, Two-Rooms: 방 두 개 사이 이동)와 JEPA world model 3개의 평균 성공률임. 세 model(LeWM, PLDM, SMWM)은 encoder를 end-to-end로 학습하고 collapse 방지 방식만 다름. 80 step 목표에서 raw action 42%, skill 62%로 오름. 차이는 20 step의 5퍼센트포인트에서 80 step의 20퍼센트포인트로 커지고, Reacher에서는 차이가 없음.
- OGBench-AntMaze(관절 8개 4족 로봇이 미로를 건너는 과제)에서 world model 3개 평균임. 미로 두 칸 거리 목표의 성공률이 raw action 0.4%에서 skill 38%로 오름. 세 칸은 0%에서 21%로 오름.
- LeWM에서 skill 학습의 KL 항을 뺀 deterministic autoencoder skill은 Cube에서 raw action과 비슷하고 나머지 3개 과제에서 더 낮음. 이 skill에 맞춘 Gaussian에서 planner를 시작해도 VAE skill 수준까지 오르지 않음.
- LeWM에서 planner 4개 모두 skill 쪽이 높음. 과제와 거리 평균으로 CEM 17.5, iCEM(시간 상관 noise를 쓰는 CEM 변형) 29.8, MPPI 28.1, Predictive Sampling 20.8퍼센트포인트 오름. 한 번만 뽑고 고르는 Predictive Sampling은 Two-Rooms 80 step에서 skill 94%, raw action 44%임.

**한계**

실험은 모두 시뮬레이션이고 실로봇 결과는 없음. 이론은 planner의 첫 후보와 한 step 예측만 다루며, Two-Rooms에서는 skill 위 iterative CEM(69%)이 한 번 sampling(94%)보다 낮아 refinement 단계는 설명하지 못함. skill 길이는 4로 고정했고 비교 대상은 raw action baseline뿐이라 subgoal·hierarchy 기반 방법과의 비교는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- world model 기반 test-time planning에서 실패 원인을 planner가 아니라 action 표현에서 찾은 사례임. VLA의 action chunk를 latent skill로 바꿔 world model 위에서 inference-time search를 할 때 바로 가져다 쓸 수 있는 설계임.
- planner 후보에서의 예측 오차와 데이터에서의 예측 오차를 나눠 잰 분석은, world model 예측을 failure detection 신호로 쓸 때 어디서 오차가 커지는지 확인하는 방법으로 쓸 수 있음.

*대표 그림: 평가에 쓴 표준 과제 4개의 환경 화면임. 왼쪽부터 Cube(로봇 팔과 빨간 블록), Push-T(초록 T 블록과 회색 T 목표), Reacher(노란 2관절 팔), Two-Rooms(벽으로 나뉜 공간의 빨간 점)이며, 측정 결과가 아닌 과제 환경을 보여 주는 그림임.*

---

### 7. Efficient VLA Reinforcement Learning via Subchunk Rollouts in Latent World Models (72점)

[arXiv](https://arxiv.org/abs/2611.27645) · [PDF](https://arxiv.org/pdf/2611.27645) · [alphaXiv](https://www.alphaxiv.org/abs/2611.27645)

- **저자**: Nan Tang, Han-Tao Zhang, Jing-Cheng Pang, Hao-Nan Wang, Hao-Xiang Ren, Yi-Fei Sheng, Jun-Yin Ye, Tian Xu 외 3명
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 78점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> VLA를 world model 안에서 RL로 개선할 때 이미지를 만드는 대신 압축된 latent 공간에서 상상 rollout을 돌리고, 고정된 VLA 위에 작은 residual policy만 학습함. LIBERO-Long 성공률이 71.2%로, 4×H100에서 전체 VLA를 fine-tuning한 VLA-MBPO의 64.4%보다 높음.

**무슨 문제인가**

world model로 VLA를 RL 학습시키는 기존 방법(VLA-MBPO, WMPO 등)은 미래 장면을 픽셀 단위로 생성하는 큰 video model을 쓰고, VLA 가중치 전체를 fine-tuning함. 그래서 계산과 메모리 비용이 큼. latent world model은 이미지를 만들지 않아 가볍지만 두 가지가 막힘. 첫째, 한 걸음 예측으로 학습한 모델이 자기 예측을 다시 입력으로 받으면 오차가 쌓임(compounding error). 둘째, VLA는 이미지를 입력으로 받으므로 예측된 latent를 VLA에 바로 넣을 수 없음.

**어떻게 푸나**

LS-MBPO(Latent Subchunk rollout for Model-Based Policy Optimization)는 세 단계로 동작함. 먼저 여러 카메라 이미지를 ViT encoder로 latent로 바꾸고, action을 조건으로 다음 latent를 예측하는 dynamics predictor를 학습함. 이때 Hierarchical Forcing을 씀: 정답 latent K개로 시작한 입력 창이 반복할수록 모델 예측으로 채워지고, 창 안의 모든 위치에 다음 latent 정답을 감독 신호로 줌. 다음으로 고정된 π0.5가 branch 시작점 이미지에서 action chunk 50 step을 한 번 만들고, 이를 5 step짜리 subchunk 10개로 나눔(Latent Subchunk Rollout). residual policy는 현재 예측 latent, 해당 subchunk, 언어 지시를 입력받아 action 보정량을 내고, 보정된 subchunk로 world model이 다음 latent를 예측함. 그래서 상상 rollout 동안 VLA를 다시 부르지 않음. reward는 latent에서 과제 성공 여부를 판정하는 success detector의 0/1 값이고, residual policy는 TD3+BC(TD3 RL 목표에 behavior cloning 항을 더한 offline RL 방법)로 학습함. 끝으로 PBC(Progress-Conditioned Branch-Start Curriculum)가 과제 진행도 예측값을 써서 처음에는 완료 직전 상태에서, 학습이 진행되면 점점 이른 상태에서 상상 rollout을 시작하게 함.

**결과**

- LIBERO(시뮬레이션 조작 benchmark, Spatial·Object·Goal·Long 4개 suite) 성공률이 Spatial 92.0%, Long 71.2%임. 같은 residual 구조의 Dreamer식 latent world model baseline은 88.0%, 69.6%이고, 시작점인 π0.5-SFT는 78.4%, 52.0%임.
- 전체 VLA를 fine-tuning하는 VLA-MBPO와 LIBERO-Long에서 비교함. 성공률은 71.2% 대 64.4%임. RL 단계 학습 시간은 RTX 5090 1장에서 1.5시간, VLA-MBPO는 H100 4장에서 12시간임.
- Hierarchical Forcing을 빼고 한 걸음 예측만 학습한 LeWM 방식(기존 latent world model)의 world model을 쓰면 LIBERO-Long 성공률이 61.4%로 내려감. 100 step 상상 후 마지막 장면 복원 PSNR도 25.22dB에서 15.53dB로 내려감.
- 실제 ALOHA 양팔 로봇에서 과제 2개(펜꽂이에 펜 넣기, 충전기 플러그 꽂기)를 과제당 20회 평가함. LS-MBPO가 π0.5-SFT와 Dreamer보다 높다고 보고하지만 정확한 수치는 본문에서 확인 불가함.

**한계**

상상 rollout 길이는 VLA가 한 번 만든 action chunk 길이(50 step)를 넘지 못하므로 긴 과제 전체를 상상 속에서 풀지 못함. 실로봇은 과제 2개, 20회 평가뿐이고 결과는 막대그래프로만 제시됨. 모든 비교가 residual 구조 안에서 이루어졌고, VLA 가중치를 직접 고치는 방법과의 비교는 VLA-MBPO 한 건뿐임. 코드 공개 여부는 본문에 없음.

**누리랩 연구와의 연결**

- VLA를 건드리지 않고 latent world model 안에서 residual policy로 action 보정을 학습하는 구조임. VLA failure recovery를 가벼운 보정 모듈로 붙이는 연구의 baseline으로 쓸 수 있음.
- 상상 rollout의 오차 누적을 학습 목표로 줄이는 Hierarchical Forcing은 world model 기반 failure prediction이나 counterfactual rollout에서 긴 예측이 필요할 때 그대로 적용해 볼 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 위 칸은 latent world model 학습이고, 가운데 칸은 고정 VLA의 action chunk를 residual policy가 subchunk 단위로 보정하는 상상 rollout임. 빨간 점선 VLA 궤적이 초록 실선으로 고쳐지는 모습과, 아래 칸의 success detector reward와 TD3+BC 갱신 단계가 함께 그려짐.*

---

### 8. EgoLAM: Learning Latent Actions from Hand and Head Motion (72점)

[arXiv](https://arxiv.org/abs/2611.27290) · [PDF](https://arxiv.org/pdf/2611.27290) · [alphaXiv](https://www.alphaxiv.org/abs/2611.27290)

- **저자**: Ziyi Ding, Yiwei Wang, Zhongxing Wei, Xianxin Lai, Yechi Liu, Xiaodi Huang, Jinghua Hou, Xiaoquan Sun 외 6명
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 70점
- **읽은 원문**: PDF 전문

> 1인칭 영상에서 latent action을 뽑을 때 손목 움직임은 정답으로 가르치고 머리 움직임은 따로 넣어, 고개를 돌린 변화가 조작 동작으로 섞이지 않게 함. 이렇게 뽑은 latent action code로 policy를 사전학습하면 LIBERO 3개 suite 평균 성공률이 79.38%로, expert demonstration만 쓴 behavior cloning보다 28.73퍼센트포인트 높음.

**무슨 문제인가**

latent action model은 연속한 두 frame 사이의 변화를 code 하나로 압축하고, policy는 이 code를 행동 정답 삼아 로봇 명령 없는 영상에서 배움. 머리에 단 카메라로 찍은 1인칭 영상에서는 컵이 화면에서 움직인 이유가 손이 밀어서일 수도, 착용자가 고개를 돌려서일 수도 있음. 다음 frame 픽셀을 복원하는 LAPA나 object slot을 예측하는 방법은 두 경우 모두 예측에 도움이 되므로 둘을 가르지 않음. 그래서 code에 머리 움직임이 섞이거나, 복원은 잘 되는데 손목의 이동과 회전은 빠질 수 있음.

**어떻게 푸나**

EgoLAM은 두 단계로 학습함. 첫 단계에서는 고정된 DINOv2 feature를 slot attention으로 묶어 frame마다 object slot 8개를 만들고, 이 front end를 고정함. 둘째 단계에서 inverse dynamics model(IDM: 두 frame을 보고 그 사이의 행동을 추정하는 모델)이 두 frame의 slot을 받음. 왼손·오른손 query가 손 주변 slot feature를 모으고, 두 frame 사이의 query 차이를 128차원 code로 바꿈. 이 code에서 두 손목의 이동과 회전을 앞 frame의 머리 좌표계 기준으로 읽어 내도록 측정값으로 직접 감독함. forward dynamics model(FDM: 현재 상태와 행동으로 다음 상태를 예측하는 모델)에는 측정된 머리 움직임을 따로 넣어, 고개 돌림에 따른 화면 변화는 code 없이 설명되게 함. 여기에 code에서 머리 움직임을 읽지 못하게 하는 adversarial loss와, 이미지를 2D로 비틀어도 code가 같게 유지되게 하는 loss를 더함. 추론 때는 RGB frame 두 장만 넣으면 code가 나옴.

**결과**

- 고정된 code에서 손목 움직임을 MLP로 얼마나 읽어 낼 수 있는지 잰 R2가 0.5343으로, 비교한 8개 모델 중 가장 높음. 다음은 GeoLAM 0.4312, LAOM 0.0564임. LAOM은 사람 행동 분류 정확도가 70.56%인데도 손목 정보는 거의 남기지 않음.
- 2D warp에 대한 code 변화량을 실제 움직임에 대한 변화량으로 나눈 값이 0.7673으로 8개 모델 중 유일하게 1보다 낮음. 2D warp 불변 loss를 빼면 이 값이 1.1276으로 오름.
- LIBERO(시뮬레이션 로봇팔 조작 benchmark) Spatial·Object·Goal suite에서 성공률이 81.40%, 77.33%, 79.40%임. suite마다 가장 강한 다른 latent action model보다 7.07, 11.47, 10.73퍼센트포인트 높음. suite당 과제 10개, seed 3개, 초기 상태 50개로 평가함.
- 손목 움직임 감독을 빼는 ablation에서 손목 R2가 0.5592에서 0.3502로 내림. 이 ablation의 기준 0.5592는 head 구성이 같은 짝 모델 값이라 첫 불릿의 0.5343과 다름.

**한계**

policy 실험은 LIBERO 시뮬레이션뿐이고 실로봇 실험은 없음. 학습할 때는 손 keypoint와 머리 자세 측정값이 있는 데이터(EgoVerse 등)가 필요함. 고개를 크게 돌린 장면에서 LAPA보다 손목 이동 오차가 작다는 결과는 저자 스스로 탐색적 분석이라고 밝힘. 회전 오차 차이는 신뢰구간이 0을 포함함.

**누리랩 연구와의 연결**

- 사람 1인칭 영상을 VLA 사전학습 데이터로 쓸 때 카메라 움직임을 행동과 분리하는 방법임. 영상 기반 VLA 사전학습이나 world model의 행동 조건을 설계할 때 비교 대상으로 쓸 수 있음.
- 손 query가 object slot을 모으는 구조는 object-centric 표현을 행동 추출에 쓴 사례로, slot 기반 manipulation 표현 연구와 이어짐.

*대표 그림: 위에서부터 LAPA의 픽셀 복원, LAPO-Slots의 slot 예측, EgoLAM의 손 감독 학습 구조를 차례로 그린 개념도로, 측정 결과가 아니라 방법 구조를 그린 그림임. EgoLAM 칸에서는 slot과 손 query로 만든 code가 손 움직임 readout과 forward model로 갈라지고, 측정된 머리 움직임은 forward model에만 들어감.*

---

### 9. MomentMem: Memorizing Key Moments for Robot Manipulation (72점)

[arXiv](https://arxiv.org/abs/2611.26745) · [PDF](https://arxiv.org/pdf/2611.26745) · [alphaXiv](https://www.alphaxiv.org/abs/2611.26745) · [코드](https://github.com/PKU-VaLuE-Lab/MomentMem)

- **저자**: Guangyu Zhao, Yongchang Zhang, Ruizhang Jiang, Zhihong Yu, Yuhao Zhang, Tao Wu, Qimin Zhou, Kunsong Shi 외 5명
- **분야**: Manipulation · robotics relevance 9/10 · 1차 스크리닝 66점
- **읽은 원문**: PDF 전문

> 로봇이 잠깐 보였다 사라지는 시각 정보를 기억해야 하는 조작 과제에서, VLM이 고른 몇 장의 원본 이미지만 VLA에 넘기는 방식으로 성공률을 올림. 새로 만든 9개 과제 평균 성공률이 가장 강한 baseline의 18.2%에서 49.9%로 오름.

**무슨 문제인가**

물체의 원래 위치나 잠깐 드러난 무늬처럼 지금은 보이지 않는 정보를 기억해야 끝낼 수 있는 조작 과제가 많음. 대부분의 VLA는 현재 관측이나 짧은 context window만 입력으로 받아 이런 과제를 못함. 기존 memory 방법은 관측 기록 전체를 넣거나 압축 token으로 줄이는데, 기록이 길어지면 중복이 많고 압축 과정에서 시각 세부가 사라짐. 글로 요약하는 방법은 "큐브를 원래 자리로" 같은 지시에 필요한 정확한 위치나 질감 같은 세부를 담지 못함.

**어떻게 푸나**

MomentMem은 기억할 장면을 고르는 memorizer와 행동을 내는 executor를 따로 둔 계층 구조임. memorizer는 Qwen3-VL-4B를 fine-tuning한 VLM으로, 지금까지 저장한 keyframe, 최근 관측 몇 장, 지시문을 받아 현재 프레임을 저장할지 Yes/No로 출력함. executor는 π0.5에서 시작한 VLA로, 저장된 keyframe을 시간 순으로 받고 현재 관측, 로봇 상태, 지시문과 함께 action chunk를 출력함. memorizer 학습에서는 증거가 보이는 구간(key segment)을 통째로 정답 후보로 두고, epoch마다 그 구간에서 한 프레임(anchor)을 뽑아 양성으로 씀. anchor 앞의 프레임은 loss에서 빼고 anchor 뒤의 프레임은 음성으로 두어, 한 번 놓쳐도 같은 구간의 다음 프레임을 고르게 함. 또 scheduled sampling으로 자기 예측이 섞인 memory 기록에서도 학습시켜 앞선 선택 실수에 대응하게 함. executor는 학습을 마치고 고정한 memorizer가 실제로 고른 keyframe을 입력으로 받아 demonstration action을 따라 배움.

**결과**

- VMBench(저자가 만든 시뮬레이션 과제 9개 모음: 잠깐 보인 위치, 무늬, 위치와 색의 짝을 기억해야 하는 조작)에서 과제당 100회 평가함. 평균 성공률이 MomentMem 49.9%, EventVLA(행동 예측과 함께 keyframe을 고르는 기존 방법) 18.2%, memory 없는 π0.5 7.0%임. Mine Sweeper는 MomentMem 93% 대 baseline 최고 1%, Placement Imitation은 99% 대 baseline 최고 6%임.
- memorizer 학습 방식을 바꾼 ablation에서 평균 성공률이 크게 내림. 구간 대신 한 프레임만 정답으로 두면 6.9%, scheduled sampling을 빼면 19.0%임.
- 잠깐 나타난 표지 위치로 큐브를 옮기는 Flash Beacon 과제로 일반화를 시험함. 나머지 8개 과제로 학습한 memorizer를 Flash Beacon 주석 5개로 fine-tuning하면 성공률 43.7%임. 주석 100개를 다 쓴 경우는 44.3%, 사전학습 Qwen3-VL을 바로 주석 5개로 fine-tuning한 경우는 29.0%임.
- 실제 Franka Panda 로봇에서 과제 2개를 30회씩 평가함. 위치 따라 놓기는 14/30(π0.5 3/30, EventVLA 6/30), 컵 속 큐브 찾기는 17/30(π0.5 11/30, EventVLA 10/30)임.

**한계**

무늬를 비교해야 하는 Appearance 과제 3개에서는 baseline보다 낫지 않음. probe 분석에서 executor feature는 무늬 종류를 99% 맞히지만 짝이 맞는 상자는 40%만 맞혀, 기억한 이미지를 비교하는 능력이 부족함. 기존 benchmark인 RMBench에서는 EventVLA보다 평균 1.9퍼센트포인트 높은 데 그치고 과제별 차이가 큼. memorizer 학습에는 key segment 주석이 필요하고, 시뮬레이션은 로봇 한 종류와 고정 카메라만 써서 시점 변화는 검증하지 않음.

**누리랩 연구와의 연결**

- robot memory를 "무엇을 언제 저장할지"를 따로 학습하는 문제로 떼어 내고, keyframe 선택 정확도를 성공률과 별도로 잼. 실패가 기억 탓인지 실행 탓인지 가르는 방식이라 failure diagnosis 연구에 바로 가져다 쓸 수 있음.
- 좌표 memory와의 비교에서 위치만 필요하면 좌표가, 위치와 색의 짝이 필요하면 원본 이미지가 나았음. object-centric memory나 scene graph로 무엇을 저장할지 정할 때 비교 기준이 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 위쪽은 memorizer가 고른 keyframe이 memory stack에 쌓이고 executor가 그 stack으로 행동을 내는 흐름임. 아래쪽은 key segment 안에서 anchor 이전 프레임은 loss에서 빼고(mask 0), anchor만 양성, 그 뒤는 음성으로 두는 학습 라벨임.*

---

### 10. Ego4Gen: Generating Geometry-Grounded Motion Tokens as a World-Action Interface (70점)

[arXiv](https://arxiv.org/abs/2611.27513) · [PDF](https://arxiv.org/pdf/2611.27513) · [alphaXiv](https://www.alphaxiv.org/abs/2611.27513)

- **저자**: Yang Liu, Chao Ye, Jiahao Zhang, Zeyuan Hou, Ruijie Fang, Xiyin Ni, Xinyang Ren, Weiyang Lin
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> world model이 RGB 영상과 함께 3D 형상·3D 움직임 latent를 생성하게 하고, 이 latent를 바로 robot action으로 바꾸는 interface로 씀. action label 없는 영상으로 world model만 다시 학습하자, 시뮬레이션 randomized 장면 5개 과제의 평균 성공률이 15.2%에서 26.4%로 오름.

**무슨 문제인가**

video world model의 예측을 action으로 바꿀 때 RGB에는 색·질감·조명·배경처럼 제어와 무관한 정보가 섞여 있음. 그래서 공간 관계와 움직임이 같은 장면도 겉모습이 바뀌면 controller가 흔들림. 영상 변화를 압축한 latent action도 action과 무관한 시각 변화를 함께 담는다는 분석이 있음. 형상을 명시적으로 복원해 쓰는 방법은 계산이 늘고, world model 내부 feature를 쓰는 방법은 입력 분포 변화에 여전히 영향을 받음.

**어떻게 푸나**

저자는 먼저 MotionCrafter(영상에서 point map과 3D scene flow를 복원하는 4D VAE)의 latent가 action 예측용 interface로 쓸 만한지 확인함. 이어 Ego4Gen(Egocentric 4D Future Generation)을 만듦. 입력은 1인칭 이미지 한 장과 text prompt이고, 출력은 앞으로 4초 동안의 RGB 영상, point map(픽셀마다 3D 좌표), scene flow(점마다 3D 이동량)임. 사전학습된 video 생성 모델 Cosmos3-Nano를 고정하고, RGB·형상·움직임마다 따로 LoRA를 붙여 token의 종류에 따라 골라 씀. RGB token은 text와 RGB만 보고, 형상·움직임 token은 RGB를 gradient 없이 참고하게 attention을 비대칭으로 막아 RGB 생성 품질을 지킴. FlowInverse는 생성된 형상·움직임 latent와 로봇 관절 상태를 받아 관절 증분과 gripper 상태를 내는 작은 inverse dynamics network임. 실제 영상의 latent로 50개 과제를 사전학습한 뒤, 과제마다 Ego4Gen이 만든 latent로 fine-tuning함.

**결과**

- RoboTwin 2.0(양팔 로봇 시뮬레이션 조작 benchmark, Hard는 배경·물체를 무작위로 바꾼 장면)에서 전문가 영상의 latent를 그대로 넣어 interface만 비교함. Place Empty Cup Hard 성공률이 형상·움직임 latent는 51%, DreamDojo latent action은 0%, UniVLA는 0%, Wan2.2 video latent는 0%임. Easy에서는 DreamDojo가 88%로 형상·움직임 latent의 82%보다 높음.
- 같은 benchmark의 5개 과제 closed-loop 평가에서 clean 장면만으로 학습한 Ego4Gen의 Hard 평균 성공률은 15.2%임. π0는 21.4%, Fast-WAM은 0.2%, starVLA는 9.6%임. Easy 평균은 Ego4Gen 46.6%로 Fast-WAM 85.0%보다 낮음.
- FlowInverse를 고정한 채 clean·randomized 영상(action label 없음)으로 world model만 5k step 다시 학습함. Hard 평균 성공률이 15.2%에서 26.4%로 오르고, Easy 평균은 46.6%에서 37.2%로 내림.
- 학습에 쓰지 않은 TACO(1인칭 양손 조작 영상 dataset)에서 4초 예측의 depth AbsRel(깊이 상대 오차, 낮을수록 좋음)이 0.153으로 TesserAct 0.160, RynnWorld-4D 0.184보다 낮음.

**한계**

control 실험은 모두 RoboTwin 2.0 시뮬레이션이고 실로봇 결과는 없음. world model 재학습에 randomized 장면 영상을 썼고 비교 baseline은 clean 데이터만 썼으므로, Hard 비교에서 데이터 조건이 다름. Easy 성능은 강한 baseline보다 낮고, 재학습 뒤에는 더 내려감. 코드와 프로젝트 주소는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- world model 출력과 policy 사이에 무엇을 둘지라는 질문을 형상·움직임 latent로 답한 사례임. world model 기반 VLA나 test-time planning에서 RGB 대신 쓸 interface의 비교 대상이 됨.
- action label 없는 영상으로 world model만 고쳐 policy 일반화를 올린 결과는, 실패 장면 영상을 모아 world model을 보정하는 failure recovery 연구에 실험 설계로 쓸 수 있음.

*대표 그림: 1인칭 조건 이미지와 text prompt 두 쌍(사람 손이 컵을 꽂는 장면, 로봇 gripper가 토스트를 접시에 놓는 장면)에 대한 생성 결과임. 각 쌍의 오른쪽에 Ego4Gen이 만든 RGB·point map·scene flow가 위에서부터 한 줄씩 시간 순으로 놓임. 아래 줄은 생성된 point map을 3D로 그린 장면과 움직이는 손·gripper 영역에 색으로 칠한 scene flow임.*

---

### 11. Latent Space Planning with Sequential Monte Carlo (70점)

[arXiv](https://arxiv.org/abs/2611.26706) · [PDF](https://arxiv.org/pdf/2611.26706) · [alphaXiv](https://www.alphaxiv.org/abs/2611.26706) · [코드](https://github.com/HrishikeshVish/smcplan)

- **저자**: Hrishikesh Viswanath, Anindita Ghosh, Uttaran Bhattacharya, Aniket Bera
- **분야**: World Model · robotics relevance 8/10 · 1차 스크리닝 68점
- **학회**: ICLR 양식 (추정) · 근거: 제목 전체 대문자, 1단 구성
- **읽은 원문**: PDF 전문

> 학습된 world model 위에서 action sequence를 찾는 planning을, 후보 여러 개를 확률적으로 옮기며 고르는 SMC(Sequential Monte Carlo)와 계획을 한 걸음씩 고치는 optimizer를 번갈아 돌리는 방식으로 바꿈. 시뮬레이션 12개 설정 평균 성공률 79.8%로 가장 강한 baseline MPPI보다 7.4퍼센트포인트 높음.

**무슨 문제인가**

world model로 planning할 때는 예측한 마지막 latent가 goal latent에 가까워지는 action sequence를 찾아야 함. CEM 같은 sampling 방식은 horizon이 길어지고 action 차원이 커지면 성능이 낮아짐. world model을 미분해 gradient로 고치는 방식은 local minimum에 걸림. MPPI는 매 반복 Gaussian에서 sample을 새로 뽑고 importance weight로만 목표 분포에 다가가므로, 앞 반복에서 찾은 좋은 후보를 이어 쓰지 못함.

**어떻게 푸나**

SMC(Sequential Monte Carlo: 가중치가 붙은 sample 집단을 바뀌는 목표 분포에 맞춰 옮기는 방법)로 action sequence 12개를 particle로 들고 다님. 각 particle은 horizon 전체의 action sequence 하나임. 목표 분포는 현재 계획을 중심으로 한 Gaussian에 cost가 낮을수록 큰 가중치를 곱한 것임. 매 반복에서 각 particle은 world model을 통과한 cost gradient로 Langevin 한 걸음을 움직이고, 가중치를 다시 매기며, 가중치가 소수 particle에 몰리면 resampling됨. 그다음 Adam이 가중 평균 쪽으로 계획을 한 걸음 옮기고, 이 계획이 다음 반복의 목표 분포 중심이 됨. cost에는 goal latent와의 L2 거리 외에 PDE cost-to-go를 더함. offline dataset의 latent를 꼭짓점으로, 실제로 관찰된 전이를 간선으로 하는 roadmap 그래프를 만들고 goal에서 heat equation을 한 번 풀어 각 latent가 goal에서 얼마나 먼지 순위로 매김.

**결과**

- 5개 환경(Reacher, Point maze, Wall, Push-T, Cube)을 horizon별로 나눈 12개 설정에서 같은 후보 12개, 반복 150회 조건으로 비교함. 평균 성공률이 79.8%로 gradient descent(GD)보다 28.8, 병렬 stochastic gradient planner인 GRASP보다 49.8, CEM보다 34.5, MPPI보다 7.4퍼센트포인트 높음. 가장 높은 설정은 12개 중 8개이고, 통계적으로 유의하게 앞선 것은 Reacher 3개와 Wall 1개임.
- 가장 강한 baseline MPPI와 seed 단위로 짝지어 보면, 이 방법만 푼 seed가 142개, MPPI만 푼 seed가 53개임. MPPI는 planning horizon H(world model 예측 step 수)가 Point maze H=15인 설정과 Wall H=10, H=15에서 1~6퍼센트포인트 앞섬.
- 같은 planner에서 cost만 바꾸면 Reacher H=15 성공률이 L2 cost 27%에서 PDE cost 89%로 오름. 반대로 Wall H=10, H=15에서는 L2 cost가 8, 7퍼센트포인트 높음(유의하지 않음).
- offline dataset으로 별도 network를 학습해 탐색을 돕는 planner와도 비교함. OGBench Cube(블록을 목표 위치로 옮기는 조작 과제) H=5 성공률이 88%로, LeFlow(sample 경로 64개) 62%와 GC-IDM 56%보다 높음.

**한계**

모든 실험이 시뮬레이션의 open-loop planning이고 실로봇 결과는 없음. wall-clock 시간과 memory는 비교하지 않았고, 이 방법은 GD처럼 world model을 거꾸로 미분해야 함. PDE cost는 offline dataset이 상태 공간을 얼마나 덮는지에 기대며, Push-T H=15처럼 긴 조작 과제에서는 모든 planner가 성공률 5% 이하임.

**누리랩 연구와의 연결**

- world model 위 test-time optimization 연구에서 CEM·MPPI 대신 써 볼 planner임. particle 집단과 ESS(effective sample size: 가중치가 몇 개 particle에 몰렸는지 재는 값)를 같이 얻으므로, 계획 단계의 불확실성을 failure detection 신호로 쓰는 실험으로 이어 볼 수 있음.
- Wall 실패 분석에서 latent goal 거리는 작은데 실제 위치 오차가 큰 경우가 나옴. world model latent와 실제 상태가 어긋나는 failure를 진단하는 사례로 참고할 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 위쪽은 DINO-WM(proprioceptive latent)과 LeWM(visual latent)이 장면을 latent로 바꾸는 모습과, U자 미로에서 goal(별) 근처일수록 낮은 cost-to-go 지도를 보여 줌. 아래쪽은 처음 퍼져 있던 particle이 propose, resample, update를 거치며 cost가 낮은 세 영역으로 모이는 과정을 그림.*

---

### 12. ReActWAM: Action-Consistent Caching for Efficient World-Action Models (70점)

[arXiv](https://arxiv.org/abs/2611.27372) · [PDF](https://arxiv.org/pdf/2611.27372) · [alphaXiv](https://www.alphaxiv.org/abs/2611.27372)

- **저자**: Zhaochen Guo, Yunke Wang, Siyu Xu, Zijian Wang, Chenghao Xia, Chengbin Du, Shinan Liu, Chang Xu
- **분야**: VLA · robotics relevance 8/10 · 1차 스크리닝 68점
- **읽은 원문**: PDF 전문

> world-action model이 이전 chunk의 denoising 계산을 다시 쓸 때, 다음 행동의 방향과 gripper 명령이 바뀌는지 먼저 확인하고 재사용 상태를 보정하는 학습 없는 가속법을 제안함. LingBot-VA 기준 LIBERO-Long 추론이 5.44배 빨라지고 성공률은 96.6%에서 96.2%로 거의 유지됨.

**무슨 문제인가**

world-action model(WAM: 미래 영상과 로봇 행동을 함께 생성하는 policy)은 매 제어 주기마다 diffusion이나 flow matching의 denoising을 여러 번 반복하므로 지연이 큼. 연속한 chunk는 비슷한 행동을 예측하므로, 이전 chunk의 중간 계산을 재사용해 앞쪽 denoising 단계를 건너뛰는 training-free 방법들이 나옴. 기존 방법은 현재 관측이 이전 관측과 비슷한지만 보고 재사용을 허락함. 장면이 거의 그대로여도 다음 행동은 gripper를 close로 바꾸거나 이동 방향을 뒤집어야 할 수 있음. 이때 이전 계산을 그대로 쓰면 물체를 잡지 못하고 미는 식으로 예전 행동이 이어짐.

**어떻게 푸나**

ReActWAM은 입력으로 현재 관측, 로봇 상태, 언어 지시를 받고, 고정된 WAM의 출력인 행동 chunk와 미래 영상을 더 적은 계산으로 만듦. 먼저 세 단계 gate로 이전 chunk 재사용 여부를 정함. 첫 gate는 최근 end-effector 이동 거리가 줄었는지 보고, 줄었으면 정밀 조작 구간으로 보고 재사용을 막음. 둘째 gate는 현재 관측과, 계산을 재사용할 이전 chunk의 관측(참조 관측)의 차이를 전체 화면과 변화가 큰 국소 영역에서 비교함. 셋째 gate는 참조와 같은 초기 noise로 network를 한 번 돌려 첫 velocity를 깨끗한 latent로 외삽하고, 이를 decoder에 넣어 대략의 다음 행동을 얻음. 이 예측이 참조 행동과 반대 방향으로 움직이거나 gripper 개폐가 다르면 재사용을 거부함. 통과하면 현재와 참조의 첫 단계 velocity 차이로 저장된 latent와 residual을 보정해 뒤쪽 denoising 단계부터 시작함. 남은 단계에서는 최근 두 velocity의 cosine similarity가 높을수록 같은 velocity를 더 여러 단계 재사용함.

**결과**

- RoboTwin 2.0(양팔 조작 과제 50개 시뮬레이션 benchmark)에서 LingBot-VA의 chunk당 지연이 2424.65ms에서 496.34ms로 줄어 4.885배 빨라짐. 성공률은 86.30%에서 86.35%로 유지됨. chunk 안 재사용만 하는 DiT Caching은 4.440배, 85.60%임.
- LIBERO-Long(긴 순서의 시뮬레이션 조작 과제 10개)에서 LingBot-VA ablation 결과, 재사용 상태 보정을 빼면 성공률이 96.2%에서 79.4%로 내림. 전체 방법은 5.44배 빨라짐. gate 셋을 모두 빼면 6.643배로 더 빨라지지만 성공률은 89.2%로 내림.
- FastWAM처럼 미래 영상을 만들지 않는 backbone에서는 가속이 LIBERO-Long 1.413배에 그침. 궤적과 중간 상태를 관측에 맞춰 재사용하는 기존 가속법 WAMachine(1.635배)보다 느림.
- 실제 Franka Research 3 로봇의 과제 3개(꽃 꽂기, 책 꽂기, 물 주기)에서 과제당 20회 시행함. 평균 수행 시간이 244.8초에서 167.9초로 줄어 1.458배 빨라졌고 평균 성공률은 50.0%로 가속하지 않은 원래 추론(Native)과 같음.

**한계**

gate 임계값, 보정 크기, 재사용 간격 같은 설정값이 많고, 설정값에 대한 민감도 분석은 본문에서 확인 불가함. 가속 폭은 계산 대부분이 denoising에 몰린 backbone에서만 크고, encoding 비중이 큰 FastWAM에서는 작음. 실로봇 실험은 과제 3개이고 base policy 성공률 자체가 50%라 성공률 유지 주장의 근거가 약하며, 코드 공개 주소는 본문에 없음.

**누리랩 연구와의 연결**

- 한 번의 forward pass로 다음 행동의 방향과 gripper 변화를 미리 읽는 action-intent 예측은, VLA 실행 중 행동 전환 시점을 싸게 감지하는 failure detection 신호로 바꿔 쓸 수 있음.
- world model 기반 test-time planning에서 rollout 비용을 줄일 때, 관측 유사도 대신 행동 일관성으로 재사용을 정하는 기준을 그대로 옮겨 볼 수 있음.

*대표 그림: LIBERO 장면에서 이전 chunk는 gripper를 연 채 끝났고 현재 chunk는 gripper close를 예측하는 상황을 보여 주는 설명용 그림임. 이전 계산을 재사용한 왼쪽 아래는 주전자를 살짝 앞으로 밀고, 재사용하지 않은 오른쪽 아래는 예측대로 gripper를 close함.*

---

### 13. Learning from Incomplete Actions: Interval Motion Supervision for Vision-Language-Action Policies (68점)

[arXiv](https://arxiv.org/abs/2611.27171) · [PDF](https://arxiv.org/pdf/2611.27171) · [alphaXiv](https://www.alphaxiv.org/abs/2611.27171)

- **저자**: Yunpeng Mei, Chenyu Wang, Xiaowen Zhu, Chenbo Xin, Hongjie Cao, Yiyuan Li, Chengye Zhang, YuAn Wang 외 1명
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 66점
- **읽은 원문**: PDF 전문

> 사람 egocentric 영상에서 뽑은 action label에 빈 구간이 생겨도, 구간 양 끝 pose가 알려 주는 순이동량으로 빠진 action들의 합을 제약해 VLA를 학습함. 실로봇 5개 과제 평균 성공률이 빈 구간을 학습에서 빼는 방식(Mask)의 48.8%에서 59.6%로 오름.

**무슨 문제인가**

사람 egocentric demonstration은 영상에서 손 pose를 추정해 robot action label로 바꿔 씀. 손이 가려지거나 tracking이 실패하면 연속된 구간의 label을 믿을 수 없어 걸러 내야 함. 기존 처리는 마지막 pose를 유지하는 Hold, 양 끝 사이를 직선으로 잇는 Linear, 해당 구간의 loss를 빼는 Mask임. Hold는 정지 뒤 급한 점프를, Linear는 실제와 다를 수 있는 내부 경로를 target으로 주고, Mask는 양 끝 pose가 알려 주는 순이동량까지 버림.

**어떻게 푸나**

π0.5를 초기값으로 쓰는 flow matching(FM) policy가 10-step action chunk를 내는 구조는 그대로 둠. 믿을 만한 action은 원래 FM loss로 학습함. 같은 action expert에 interval token을 더해, 구간 시작 관측에서 그 구간의 6차원 순이동량(이동 3, 회전 3)을 FM으로 예측하게 함(interval branch). 빈 구간 안의 action 추정값은 시간 순서대로 합성해 순이동량으로 만들고, 이 값이 interval branch 예측과 맞도록 composition loss를 줌. 이때 예측값은 stop-gradient로 고정해 target으로만 씀. 그래서 빠진 action 하나하나에는 target이 없고 합만 제약받음. 빈 구간이 10 step보다 길면 구간을 덮는 여러 window가 각자 관측을 읽은 채 하나의 제약을 함께 받음. 추론 때는 현재 관측만 넣고 action과 interval을 함께 10번의 Euler step으로 denoising함.

**결과**

- LIBERO(시뮬레이션 단일 팔 조작 benchmark) 40개 과제의 시연 20%(339개)에서 action의 70.5%를 1.2초짜리 구간으로 지운 조건임. 세 번 학습한 평균 성공률이 87.9%임. 한 번 학습 기준으로 Mask는 76.4%, label이 다 있는 Clean은 92.4%임.
- 같은 조건에서 관측을 읽는 횟수와 학습 비용(약 279 GPU-hours)을 맞춘 Mask 대조군은 77.9%이고 이 방법은 88.4%임. 두 모델 모두 한 번씩 학습한 비교임.
- RoboTwin 2.0(양팔 조작 시뮬레이션) 10개 과제에 실제 Ego 데이터의 빈 구간 패턴을 옮겨 학습함. 성공률은 45.4%로 Mask 40.3%, interval branch만 쓴 경우 42.8%보다 높고 Clean 49.5%보다는 낮음.
- 실제 양팔 로봇 5개 과제에서 과제당 로봇 시연 20개와 Ego 시연 160개로 학습하고 50회씩 평가함. 평균 성공률은 59.6%로 interval branch만 쓴 경우 54.8%, Mask 48.8%, 로봇 시연만 쓴 경우 42.0%보다 높음.

**한계**

LIBERO 표 대부분과 실로봇 결과가 설정당 한 번 학습한 값이라 수 퍼센트포인트 차이는 분산과 구분하기 어려움. interval branch의 이득은 빈 구간 action 자리에 넣는 입력에 따라 달라짐. 양 끝 사이 직선 보간값을 넣는 주 설정에서는 interval branch를 빼도 성공률이 0.3퍼센트포인트만 내림. 방법은 구간 양 끝 pose가 정확하다는 가정에 기대며, 코드 공개 주소는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- 사람 영상을 VLA 학습 데이터로 쓸 때 생기는 label 결손을 버리지 않고 구간 단위 제약으로 쓰는 방법임. 누리랩 VLA·manipulation 연구에서 human video co-training을 할 때 Mask 대신 비교해 볼 수 있음.
- 개별 action 대신 여러 step의 합성 결과를 감독하는 구조는, 짧은 구간의 결과 상태만 아는 failure recovery 데이터를 학습에 쓸 때도 응용 가능함.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 왼쪽은 실제 Ego 영상 프레임 5장에 양손 label의 믿을 만한 구간(초록)·빈 구간(빨강) 트랙을 붙이고, Hold·Linear·Mask·이 방법의 빈 구간 처리를 비교함. 오른쪽은 빈 구간에서 합성한 끝점과 관측 끝점의 차이(L_B), chunk 전체 순이동량 예측(L_D)을 그림. 본문의 주 방법은 L_B의 target으로 관측 끝점 대신 interval branch 예측값을 씀.*

---

### 14. NavTTT: Adaptive Parametric Memory via Hierarchical Test-Time Training for Vision-and-Language Navigation (68점)

[arXiv](https://arxiv.org/abs/2611.27219) · [PDF](https://arxiv.org/pdf/2611.27219) · [alphaXiv](https://www.alphaxiv.org/abs/2611.27219) · [프로젝트 페이지](https://gamepeopleplay.github.io/NavTTT/)

- **저자**: Xiaoyu Luo, Chengxing Lin, Jiaxin Huang, Jiale Liu, Jingyu Guo, Sirui Chen, Aolin Li, Shaoli Huang 외 2명
- **분야**: Navigation · robotics relevance 8/10 · 1차 스크리닝 68점
- **읽은 원문**: PDF 전문

> 언어 지시 navigation에서 지나간 관측을 token으로 쌓지 않고, 고른 일부만 test-time training으로 fast weight에 써 넣어 기억하게 함. R2R-CE 성공률이 비교 대상 중 가장 높던 JanusVLN의 60.5%에서 66.7%로 오름.

**무슨 문제인가**

VLN(vision-and-language navigation)에서 agent는 지시를 따라 걸으며 지나온 장소와 landmark를 기억해야 다음 행동을 정할 수 있음. 기존 방법은 지도·graph 같은 explicit memory나 지난 관측을 token으로 들고 다니는 implicit memory를 씀. token 방식은 기억을 늘릴수록 붙잡고 attention할 token이 늘어나서, 긴 경로에서는 기억 범위와 계산량 사이에서 타협해야 함. 관측이 들어올 때마다 작은 신경망 가중치(fast weight)를 갱신해 기억하는 test-time training(TTT)이 대안이지만, 비슷한 장면이 반복되는 navigation 영상을 다 써 넣으면 중요한 landmark가 묻힘.

**어떻게 푸나**

NavTTT(Navigation-Conditioned Test-Time Training)는 Qwen3-VL-8B를 바탕으로 한 VLN 모델에 episode마다 새로 시작하는 fast weight 기억을 붙임. 이 기억을 APM(Adaptive Parametric Memory)이라 부름. 매 결정마다 먼저 현재 RGB 이미지의 visual token 가운데 써 넣을 것을 고름. 지시·자세·step을 담은 navigation state와 decoder의 결정 token을 합쳐 각 token의 관련도를 매기고, 이미 고른 token과 겉모습이 비슷하면 감점하며 하나씩 고름. 고른 token은 시각 특징을 key로, 시각 특징·patch 좌표·로봇 자세·navigation state를 합친 것을 value로 만들어 fast weight에 gradient 한 번으로 써 넣음. fast weight는 36층 decoder 중 6개 층에 따로 두고, 각 층의 hidden state가 query로 기억을 읽어 self-attention 출력에 더함. 기억은 읽기 먼저, 쓰기 나중 순서로 다뤄서 현재 행동은 이전 결정까지의 기억만 보고 정함. 출력은 FORWARD·LEFT·RIGHT·STOP 중 최대 4개로 된 행동 묶음임.

**결과**

- R2R-CE(연속 3D 실내 환경에서 영어 지시를 따라 걷는 benchmark)의 처음 보는 환경 split에서 성공률 66.7%, SPL(경로 효율을 반영한 성공률) 59.4%를 얻음. 가장 강한 비교 대상 JanusVLN은 60.5%와 56.8%임.
- 더 길고 자세한 다국어 지시를 쓰는 RxR-CE에서 성공률이 JanusVLN의 56.2%에서 63.6%로, 기준 경로와의 일치도 nDTW가 62.1%에서 71.0%로 오름.
- 같은 checkpoint에서 기억 쓰기만 끄면 R2R-CE 성공률이 66.7%에서 63.3%로 내림. 경로 길이 상위 3분의 1 구간에서는 쓰기를 켜면 성공률이 9.97퍼센트포인트 오름.
- 실제 휴머노이드 로봇에서 실환경 데이터로 fine-tuning하지 않고 40회 시도 중 11회 성공함(27.5%). 비교 대상 없는 단독 결과임.

**한계**

NavTTT는 RGB에 더해 odometry 자세를 입력으로 쓰지만, JanusVLN과 StreamVLN은 RGB만 써서 입력 조건이 같지 않음. 기존 TTT 방식(LaCT)을 그대로 붙인 경우의 R2R-CE 성공률은 63.3%로, NavTTT보다 3.4퍼센트포인트 낮을 뿐이고, RxR-CE에서는 SPL이 오히려 1.0퍼센트포인트 낮음. 쓴 내용을 다시 꺼내는 시험에서 정답 1위 적중률이 6.22%에 그쳐, 기억에서 무엇을 다시 꺼낼 수 있는지는 분명하지 않음.

**누리랩 연구와의 연결**

- robot memory를 token이나 지도가 아니라 실행 중 갱신되는 가중치에 두는 설계이고, 무엇을 쓸지 고르는 기준을 학습함. manipulation VLA의 긴 과제 기억이나 test-time optimization 연구에서 비교 대상으로 쓸 수 있음.
- 엉뚱한 경로의 기억 상태를 넣었을 때 정답 행동 likelihood가 낮아지는지 재는 진단 방식은, 기억이 실제로 행동에 쓰이는지 확인하는 실험 설계로 가져올 만함.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 위쪽은 거실을 걷는 휴머노이드 로봇 장면임. 아래 왼쪽은 지도형 explicit memory와 token을 쌓는 implicit memory이고, 오른쪽은 고른 token을 여러 decoder 층의 fast weight에 써 넣는 이 논문의 방식임.*

---

### 15. FoRe: A Force-Guided Framework for Autonomous Grasp Recovery in Vision-Language-Action Models (66점)

[arXiv](https://arxiv.org/abs/2611.27011) · [PDF](https://arxiv.org/pdf/2611.27011) · [alphaXiv](https://www.alphaxiv.org/abs/2611.27011)

- **저자**: Shuai Peng, Yongkai Liao, Yuxin Cheng, Haoyuan Wang, Jian Huang
- **분야**: VLA · robotics relevance 9/10 · 1차 스크리닝 66점
- **읽은 원문**: PDF 전문

> VLA policy가 잡기에 실패하고도 그대로 운반을 이어 가는 문제를, 힘 센서 값으로 실패를 감지해 다시 잡기 전용 policy로 바꾸는 방식으로 줄임. 실로봇 흡착 pick-and-place에서 VLA-Adapter의 평균 성공률이 26.7%에서 51.7%로 오름.

**무슨 문제인가**

imitation learning으로 학습한 VLA policy는 pick-and-place에서 물체를 놓친 뒤에도 다시 잡지 않고 운반 동작을 계속하는 경우가 있음. 저자들은 원인을 두 가지로 봄. 성공 demonstration에서는 로봇 관절 상태(proprioception)만 보아도 과제 진행 단계를 알 수 있음. 그래서 policy가 실제 잡기 결과 대신 관절 상태만 보고 운반 단계로 넘어감. 또 끊김 없는 성공 demonstration만으로는 실패 뒤 다시 접근하는 행동을 배울 데이터가 없음. 기존 복구 방법은 사람의 언어 교정이나 VLM 감시에 기대거나 demonstration을 늘리는 방식이라, 사람 참여나 추론 지연이 따름.

**어떻게 푸나**

FoRe(Force-guided Recovery)는 같은 VLA backbone으로 policy 세 개를 만들고 힘 신호로 전환함. 먼저 demonstration의 각 시점에 단계 표시를 붙임. 잡기 명령이 켜져 있고 힘 크기가 임계값을 넘으면 접근·잡기 단계에서 운반·놓기 단계로 넘어가고, 놓기 명령이 들어오고 힘이 사라지면 다시 첫 단계로 돌아감. 두 구간의 demonstration으로 접근·잡기 policy M1과 운반·놓기 policy M2를 따로 fine-tuning함. 다시 잡기 policy M3는 M1에서 시작해 RL로 다듬음. 이때 운반 초반의 로봇 자세에 로봇을 두고 물체는 원래 자리에 둔 장면을 실패 직후 상태로 씀. 같은 장면에서 여러 번 시도해 들어 올리기 시험의 성공 여부를 0/1 reward로 주고, 묶음 평균과의 차이를 advantage로 써서 갱신함. 추론 때는 M2 실행 중 잡기 명령이 켜져 있는데 힘이 임계값 아래로 내려가면 실패로 보고 M3로 바꾸며, 힘이 다시 잡히면 M2로 돌아감.

**결과**

- LIBERO-SUCTION(저자들이 LIBERO에 흡착 그리퍼와 힘 센서를 붙여 만든 22개 과제 benchmark)에서 과제당 50회 평가함. 평균 성공률이 VLA-Adapter는 69.2%에서 87.6%로, π0.5는 85.9%에서 92.4%로 오름.
- 원래 LIBERO(시뮬레이션 조작 과제 모음, 여기서는 suite 4개 40개 과제)에서 VLM으로 하위 과제를 되돌려 다시 시도하는 CycleVLA와 비교함. 평균 성공률이 VLA-Adapter 기준 FoRe 98.6%, CycleVLA 97.6%이고, π0.5 기준 FoRe 98.3%, CycleVLA 97.9%로 차이는 1퍼센트포인트 이하임.
- ablation에서 힘 신호를 빼고 잡기 명령만으로 전환하면 M3가 호출되지 않고 평균 성공률이 87.6%에서 74.3%로 내림. RL 없이 M1을 그대로 다시 잡기에 쓰면 82.4%임.
- 실제 DOBOT 6축 로봇과 진공 흡착 그리퍼로 과제 범주 3개(단순, 방해물, 여러 물체 쌓기)를 과제당 40회 평가함. 평균 성공률이 VLA-Adapter는 26.7%에서 51.7%로, π0.5는 48.3%에서 70.0%로 오름.

**한계**

복구 대상은 잡았다가 놓친 경우뿐이고, 처음부터 물체에 닿지 못하면 힘 신호가 없어 실패를 감지하지 못함. 힘 임계값은 데이터셋마다 사람이 통계를 보고 정함. 실로봇 결과는 과제 범주 3개로만 보고되어, 범주별 과제 수와 과제별 수치는 본문에서 확인 불가하고, 코드 공개 주소도 본문에 없음.

**누리랩 연구와의 연결**

- failure detection/recovery에서 VLM 대신 힘 신호와 그리퍼 명령만으로 실패를 감지하는 단순한 기준선임. 실패 직후 상태를 demonstration 자세로 만들어 RL을 돌리는 방식은 recovery policy 데이터 생성에 바로 쓸 수 있음.
- proprioception만 보고 단계를 넘기는 문제를 제기했으므로, VLA의 단계 판단을 물리 결과에 묶는 counterfactual 연구의 비교 대상이 됨.

*대표 그림: 위 줄은 평가 rollout, 아래 줄은 성공 demonstration의 접근·잡기·운반·놓기 장면임. 위 줄에서는 물체를 놓쳤는데도 policy가 아래 줄과 비슷한 관절 상태를 따라 운반 동작을 이어 가고, 녹색 화살표는 바람직한 다시 잡기 방향을 표시함.*

---

## 오늘의 흐름

- **world model 위 planning의 신뢰성**: planner가 world model의 학습 분포 밖 행동을 고르면 예측은 목표에 닿지만 실제 실행은 실패함. 오늘은 이 문제를 예측 상태에서 행동을 다시 읽는 검사, 학습 분포 안에서만 후보를 뽑는 latent skill, 여러 후보를 확률적으로 옮기는 SMC(Sequential Monte Carlo) 세 방향으로 다룸. [A Plan or an Adversarial Example?](https://arxiv.org/abs/2611.27124), [Skill-JEPA](https://arxiv.org/abs/2611.26825), [Latent Space Planning with Sequential Monte Carlo](https://arxiv.org/abs/2611.26706)
- **test-time training을 memory로 씀**: 지난 관측을 token으로 계속 쌓는 대신, 실행 중에 adapter나 fast weight를 갱신해 그 가중치에 기억을 남김. 조작에서는 짧은 history로 긴 history 모델 성능에 맞추고, navigation에서는 기존 최고 방법보다 성공률을 올림. [LoCo-WAM](https://arxiv.org/abs/2611.26853), [NavTTT](https://arxiv.org/abs/2611.27219)
- **실행 중 실패 감지와 복구**: 기존 policy를 다시 학습하지 않고 그 위에 감지 장치를 붙이는 방식이 셋 나옴. flow matching policy의 epistemic uncertainty 계산, agent가 직접 쓰는 감시 프로그램, 힘 신호로 잡기 실패를 알아채는 방식임. [Coherent Moment Propagation](https://arxiv.org/abs/2611.26855), [Tripwire](https://arxiv.org/abs/2611.27182), [FoRe](https://arxiv.org/abs/2611.27011)
- **world-action model 다듬기**: 영상과 행동을 함께 예측하는 world-action model과, world model 안에서 VLA를 개선하는 방법의 약점을 하나씩 고치는 연구가 모임. 지시 대상 grounding, 추론 속도, RGB와 함께 생성한 3D 형상 latent를 쓰는 action interface, latent 공간 RL이 각각 다뤄짐. [Beyond Linear Decodability](https://arxiv.org/abs/2611.27401), [ReActWAM](https://arxiv.org/abs/2611.27372), [Ego4Gen](https://arxiv.org/abs/2611.27513), [Efficient VLA Reinforcement Learning via Subchunk Rollouts](https://arxiv.org/abs/2611.27645)
- **사람 1인칭 영상으로 VLA 학습**: 정확한 로봇 action label이 없는 사람 1인칭 영상에서 행동 신호를 뽑아 VLA를 학습함. 하나는 머리 움직임과 손목 움직임을 나누고, 다른 하나는 label이 빈 구간을 양 끝 pose의 순이동량으로 제약함. [EgoLAM](https://arxiv.org/abs/2611.27290), [Learning from Incomplete Actions](https://arxiv.org/abs/2611.27171)

## 해볼 만한 연구

### world model 예측 오차를 VLA 실패 예측 신호로 쓰기

- 질문: world model이 실행 중에 내는 예측 오차가 policy 자체의 uncertainty보다 실패를 더 일찍, 더 정확히 알려 주는지 밝힘.
- 첫 실험: LIBERO-90에서 같은 VLA를 돌리며 세 신호의 실패 예측 정확도를 비교함. 첫째 신호는 CoMP(Coherent Moment Propagation: flow matching policy의 epistemic uncertainty 계산법) uncertainty임. 나머지 둘은 LoCo-WAM식 video 예측 loss와 예측 상태에서 행동을 다시 읽은 residual임.
- 가장 가까운 연구: [Coherent Moment Propagation](https://arxiv.org/abs/2611.26855)은 policy 가중치의 불확실성만 봄. [A Plan or an Adversarial Example?](https://arxiv.org/abs/2611.27124)는 residual을 plan 선택에만 쓰고 실패 판별기로 평가하지 않았음.

### 원본 이미지 memory와 가중치 memory 비교

- 질문: 조작 과제에서 기억을 원본 이미지 몇 장으로 남기는 방식과 adapter 가중치에 써 넣는 방식이 어떤 과제에서 각각 나은지 밝힘.
- 첫 실험: MomentMem이 새로 만든 9개 기억 과제(잠깐 보였다 사라지는 시각 정보를 기억해야 하는 조작 과제)에서 같은 VLA에 두 memory를 붙여 성공률과 추론 계산량을 비교함. 하나는 VLM이 고른 key frame, 다른 하나는 test-time training으로 갱신하는 LoRA임.
- 가장 가까운 연구: [MomentMem](https://arxiv.org/abs/2611.26745)은 이미지 선택만 시험함. [LoCo-WAM](https://arxiv.org/abs/2611.26853)은 짧은 history를 보완하는 효과만 보였고, 잠깐 보였다 사라지는 정보를 기억하는 과제는 다루지 않음.

### agent가 쓰는 감시 프로그램에 uncertainty 넣기

- 질문: agent가 상황마다 새로 쓰는 감시 조건에 policy uncertainty를 입력으로 주면, 사람 방해뿐 아니라 조작 실패도 잡을 수 있는지 밝힘.
- 첫 실험: Tripwire 논문의 실행 환경(TRIP harness)에서 tripwire가 읽을 수 있는 값에 CoMP uncertainty를 더하고, 잡기 실패가 섞인 주방 과제에서 복구 성공률을 비교함.
- 가장 가까운 연구: [Tripwire](https://arxiv.org/abs/2611.27182)는 VLM 질문과 depth로 사람 접근만 감시함. [FoRe](https://arxiv.org/abs/2611.27011)는 힘 신호라는 고정된 감지 규칙 하나만 씀.

## 꼭 읽을 논문

- [Beyond Linear Decodability](https://arxiv.org/abs/2611.27401): 지시를 무시하는 실패를 내부 표현에서 진단하고, 지시 대상을 선형으로 읽게 하는 보조 loss로 고치는 절차를 보여 줌. 추가 데이터에는 action 없이 대상 mask만 씀.
- [A Plan or an Adversarial Example?](https://arxiv.org/abs/2611.27124): 탐색을 더 할수록 실행 성공률이 내려가는 현상을 재는 방법을 줌. world model planning 실험을 설계할 때 먼저 확인할 지표임.
- [LoCo-WAM](https://arxiv.org/abs/2611.26853): 실행 중 test-time training으로 짧은 history 모델이 긴 history 모델 성능에 맞춤. test-time optimization과 robot memory 연구의 비교 대상임.
- [Coherent Moment Propagation](https://arxiv.org/abs/2611.26855): 기존 uncertainty 계산이 ODE 적분 step을 늘릴수록 0으로 줄어듦을 증명함. 실패 감지 실험에서 점수를 비교할 때 확인할 항목을 알려 줌.
- [Tripwire](https://arxiv.org/abs/2611.27182): 학습 없이 agent가 감시 프로그램을 써서 VLA를 멈추고 복구 행동을 고르는 구조임.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (442편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2611.27645'>Efficient VLA Reinforcement Learning via Subchunk Rollouts in Latent World Models</a></td><td>78</td><td>9</td><td>VLA</td><td>VLA를 latent world model 내 subchunk rollout으로 효율적으로 RL 하는 방법으로 핵심 주제와 직결됨</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2611.27182'>Tripwire: Robot Agents that Program Their Own Interrupts under Human Disturbance</a></td><td>72</td><td>9</td><td>Embodied AI</td><td>agent가 VLA 호출 중 스스로 interrupt를 프로그램해 외란에 반응함. failure 대응 관점에서 문제 설정이 새로움</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2611.27513'>Ego4Gen: Generating Geometry-Grounded Motion Tokens as a World-Action Interface</a></td><td>72</td><td>9</td><td>World Model</td><td>RGB, point map, scene flow를 함께 생성하는 4D world model로 조작 인터페이스를 만듦. 기하 기반 표현이 새로움</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2611.27401'>Beyond Linear Decodability: Understanding and Improving Instruction Following in World Action Models</a></td><td>72</td><td>9</td><td>VLA</td><td>world action model이 언어 지시를 따르지 않는 원인을 분석하고 개선함. 실패 진단 관점에서 관련성 높음.</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2611.27290'>EgoLAM: Learning Latent Actions from Hand and Head Motion</a></td><td>70</td><td>9</td><td>VLA</td><td>egocentric 영상에서 손과 머리 움직임으로 latent action을 학습함. 카메라 움직임 혼동 문제를 짚어 로봇 학습 데이터 활용에 직접 관련됨</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2611.26853'>LoCo-WAM: Test-Time Training as Long Context for World-Action Models</a></td><td>70</td><td>9</td><td>World Model</td><td>world-action model에 test-time training을 long context로 써서 기억 길이 문제를 다룸</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2611.26855'>Coherent Moment Propagation: Epistemic Uncertainty for Pre-trained Robot Policies</a></td><td>70</td><td>9</td><td>Manipulation</td><td>pre-trained flow matching policy의 epistemic uncertainty 추정으로 failure detection과 연결됨</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2611.27124'>A Plan or an Adversarial Example? A Round-Trip Check for Latent World Models</a></td><td>68</td><td>8</td><td>World Model</td><td>latent world model planning 결과가 adversarial example인지 round-trip으로 검증하는 test-time 검사 아이디어가 참신함</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2611.26706'>Latent Space Planning with Sequential Monte Carlo</a></td><td>68</td><td>8</td><td>World Model</td><td>world model 위 latent planning을 SMC로 수행하는 inference-time planning 방법임</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2611.26825'>Skill-JEPA: Learning Planner-Aligned Action Spaces for World Models</a></td><td>68</td><td>8</td><td>World Model</td><td>JEPA world model에서 planner 정렬 skill action space를 학습해 planning 효율화함</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2611.27219'>NavTTT: Adaptive Parametric Memory via Hierarchical Test-Time Training for Vision-and-Language Navigation</a></td><td>68</td><td>8</td><td>Navigation</td><td>VLN에서 test-time training으로 fast-weight 기억을 만듦. memory와 TTT 결합이 흥미로우나 성능 개선 중심임</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2611.27372'>ReActWAM: Action-Consistent Caching for Efficient World-Action Models</a></td><td>68</td><td>8</td><td>VLA</td><td>world-action model 추론에서 action 일관 caching으로 계산을 줄임. 효율 추론이나 증분적 기여 성격임.</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2611.26745'>MomentMem: Memorizing Key Moments for Robot Manipulation</a></td><td>66</td><td>9</td><td>Manipulation</td><td>핵심 순간만 기억하는 robot manipulation memory 방법으로 memory 주제와 직결됨</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2611.27011'>FoRe: A Force-Guided Framework for Autonomous Grasp Recovery in Vision-Language-Action Models</a></td><td>66</td><td>9</td><td>VLA</td><td>force 기반으로 VLA의 grasp 실패를 복구하는 failure recovery 방법임</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2611.27171'>Learning from Incomplete Actions: Interval Motion Supervision for Vision-Language-Action Policies</a></td><td>66</td><td>9</td><td>VLA</td><td>action 구간이 빠진 egocentric demonstration에서 구간 합성 목적함수로 VLA를 학습함. 실용적 문제 설정이나 증분적 기여임</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2611.26865'>FlowScope: 3D Scene Flow Pretraining Improves Surgical Robot Policies</a></td><td>66</td><td>8</td><td>Manipulation</td><td>수술 stereo 영상에서 3D scene flow pretraining으로 imitation policy를 개선함. 표현 학습 아이디어가 좋고 로봇 직접 관련임</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2611.26981'>ViewDreamer: A Robot World Model beyond Fixed Camera Setups</a></td><td>66</td><td>8</td><td>World Model</td><td>카메라 수가 달라도 쓰는 robot world model임. multi-view 생성 formulation이 실용적임</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2611.26744'>FORTH: Grounding Tactile VLA Execution via Forward-Only Proxy-Control Pairing</a></td><td>66</td><td>8</td><td>VLA</td><td>tactile VLA가 실제 force를 학습하는지 문제를 제기하고 proxy-control pairing으로 grounding함</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2611.27552'>S-BFM: A Behavioral Foundation Model for Humanoid Control from Sparse Spatiotemporal Goals</a></td><td>66</td><td>8</td><td>Humanoid</td><td>희소한 시공간 목표만으로 humanoid를 제어하는 behavioral foundation model임. 문제 설정이 실용적임</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2611.27306'>$γ$-Scape: An Agent-Centric World for Mobile Embodied Intelligence</a></td><td>66</td><td>8</td><td>Embodied</td><td>AI 이동 조작을 위한 에이전트 중심 물리 world임. 실행 가능 program 기반 embodied agent 연구용 환경임.</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2611.27963'>Non-penetrating World Models</a></td><td>66</td><td>7</td><td>World Model</td><td>world model의 물체 관통 문제를 새 문제로 정의하고 benchmark를 제시함</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2611.27149'>Where Structure Enters a World Model: From Predictive Fit to Physical Rollout</a></td><td>66</td><td>7</td><td>World</td><td>Model 물리 구조가 world model의 장기 rollout 일관성에 들어가는 위치를 분석함. world model 주제와 직접 닿음.</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2611.27639'>SOAR: Training-Free Rank-Consistent Rollout Compression for Latent World Model Planning</a></td><td>65</td><td>8</td><td>World Model</td><td>latent world model planning에서 rank 일관성을 유지하며 rollout을 압축함. inference-time planning 효율화로 관련성이 높음</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2611.27418'>Beyond Future Views: Exploring Future-State World Models for Vision-Language Navigation</a></td><td>64</td><td>8</td><td>Navigation</td><td>VLN에서 미래 view 대신 future-state world model을 탐색함. 방향은 좋으나 benchmark 개선 중심임</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2611.27222'>Bel: Step-Level Policy Improvement of Visual Agents Without Training</a></td><td>64</td><td>7</td><td>Embodied</td><td>AI 학습 없이 visual agent의 step 단위 policy를 개선함. 로봇 pointing 포함하며 test-time 개선 주제와 닿음.</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2611.27338'>Latent Jacobian Steer: Eliciting Contact-Rich Out-of-Distribution Behaviors from Pretrained Humanoid Controllers</a></td><td>63</td><td>8</td><td>Humanoid</td><td>사전학습 humanoid 컨트롤러의 latent를 Jacobian으로 조향해 접촉 동작을 끌어냄. behavior foundation model 활용 아이디어임</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2611.27223'>LiDAR Signals for Robot Locomotion: Spherical Range Images Enable Robust Sim-to-Real Transfer</a></td><td>63</td><td>8</td><td>Locomotion</td><td>LiDAR 구형 range image로 sim-to-real 강건한 보행 policy를 만듦. 실용적이나 locomotion 중심임.</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2611.27446'>GenPA: Image Generators as Efficient Robot Policies</a></td><td>62</td><td>9</td><td>Manipulation</td><td>이미지 생성 모델을 미래 예측 없이 robot policy로 직접 씀. 효율적 policy 관점이 흥미로움</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2611.27689'>Embodied-Harness: Towards Recursive Self-Improvement for Robotic Manipulation</a></td><td>62</td><td>9</td><td>Manipulation</td><td>manipulation harness를 이중 agent로 자기 개선함. 실패 귀인과 memory를 다루나 harness 계열 증분성이 있음</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2611.27187'>SCAP: Stochastic Context for Action Expert Pretraining</a></td><td>62</td><td>8</td><td>VLA</td><td>VLA 적응 전 action expert pretraining에서 stochastic context를 쓰는 방법임. VLA 학습 문제를 직접 다룸</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2611.27047'>BeyondEgo: Learning to Act Beyond Egocentric Perception via Humanoid Ego-Exo Foresight</a></td><td>62</td><td>8</td><td>VLA</td><td>humanoid loco-manipulation에서 ego-exo foresight로 egocentric VLA 한계를 보완함</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2611.26883'>TouchBench: Can Vision-Language Models Feel Invisible Physical Properties?</a></td><td>62</td><td>7</td><td>Embodied AI</td><td>촉각 속성을 VLM이 인지하는지 보는 benchmark임. tactile 관련 새 평가 관점임</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2611.27166'>Mem-X: A Memory-Dependent Cross-Episode Benchmark for Vision-and-Language Navigation</a></td><td>62</td><td>7</td><td>Navigation</td><td>cross-episode VLN의 memory 의존성을 분리 평가하는 benchmark임. robot memory와 직접 관련됨</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2611.27012'>Many Plans at Once: Diverse Top-Quality Planning in Continuous Time</a></td><td>62</td><td>6</td><td>Planning</td><td>연속 시간에서 다양한 고품질 plan 집합을 미리 계산하는 방법임. 제약 변화에 대한 대안 확보 측면에서 로봇 planning과 닿음.</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2611.27344'>Learning Interaction Dynamics via Motion-Region Guidance for Robotic Video World Models</a></td><td>60</td><td>8</td><td>World Model</td><td>상호작용 영역에 집중하는 motion-region guidance로 로봇 video world model을 개선함. 모듈 수준 개선임</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2611.26867'>SonoAtlasWorld: Anatomy-Grounded Ultrasound World Models for Wide-Range Scanning</a></td><td>60</td><td>7</td><td>World Model</td><td>해부학 기반 초음파 world model임. 로봇 초음파 policy 학습 환경을 제공함</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2611.27282'>HermiteTwin: Bicubic Hermite Shell Digital Twins for Contact-Rich Deformable Manipulation</a></td><td>60</td><td>7</td><td>Manipulation</td><td>이중 3차 Hermite shell로 변형 물체 digital twin을 재구성함. 접촉과 굽힘 표현 분리가 새로움</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2611.27915'>StereoVLM: Binocular Vision-Language Models for Metric 3D Spatial Reasoning</a></td><td>60</td><td>6</td><td>Multimodal</td><td>스테레오 입력으로 metric 3D spatial reasoning을 하는 VLM으로 embodied 공간추론과 연결됨</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2611.27870'>Beyond Visual Fidelity: Comparing Categorical and Continuous World Models</a></td><td>60</td><td>6</td><td>World Model</td><td>categorical과 continuous world model을 dynamics 충실도로 체계적 비교한 분석임</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2611.27173'>PACE-WM: Parallel World Modeling with Action History for Visual Planning</a></td><td>58</td><td>8</td><td>World Model</td><td>JEPA world model에 실행 action history를 넣어 visual planning을 개선함. 모듈 추가 수준임</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2611.26764'>TacHOI: Contact-Aware Object Reconstruction and Tracking for Egocentric Videos</a></td><td>58</td><td>7</td><td>3D Vision</td><td>egocentric 영상에서 접촉 인식 물체 복원과 추적으로 로봇 demonstration 활용에 유용함</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2611.26992'>Geo-Force: A Theory of Force Sensing from Object Geometry</a></td><td>58</td><td>7</td><td>Tactile</td><td>물체 기하에서 contact force를 추정하는 virtual touch 이론으로 참신함</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2611.27648'>Trust What Repeats: Capped World-Model Policy Gradients for Humanoid Motion Tracking</a></td><td>58</td><td>7</td><td>RL</td><td>world model policy gradient에서 큰 gradient를 제한해 humanoid tracking을 안정화함. 분석이 유용하나 범위가 좁음</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2611.27797'>EvoTER: Evolving Embodied Agents via Tool-Use Experience and Reflection</a></td><td>58</td><td>7</td><td>Embodied AI</td><td>도구 사용 경험과 reflection으로 embodied agent를 진화시킴. 실패 복구 관점이나 LLM agent 흐름의 증분임</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2611.27489'>Efficient Natural Language to Temporal Logic Translation for Real-Time Physical AI</a></td><td>58</td><td>7</td><td>Planning</td><td>자연어를 temporal logic으로 번역하는 효율적 방법임. 로봇 task specification과 직접 연결됨.</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2611.26902'>Perceive Once, Escalate on Demand: Handing Off Visual KV Memory from Small to Large VLMs</a></td><td>58</td><td>6</td><td>Multimodal</td><td>작은 VLM에서 큰 VLM으로 visual KV memory를 넘기는 cascade임. embodied 효율 추론에 의미 있음</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2611.27164'>PhysForce: Physics-aware Force Control for Interactive Video World Model</a></td><td>58</td><td>6</td><td>World Model</td><td>힘 입력을 반영하는 interactive video world model임. 물리 상호작용 모델링이 조작과 연결됨</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2611.27398'>Taking Apart and Putting Together: Tracking Objects Through Physical Transformations</a></td><td>58</td><td>6</td><td>Video</td><td>조립과 분해 중 물체를 추적하는 TTU 과제 제안임. 조작 중 object tracking에 직접 관련됨</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2611.26779'>Tracktail: Multi-View 3D Point Tracking without Depth Input</a></td><td>58</td><td>5</td><td>3D Vision</td><td>depth 없이 multi-view 3D point tracking하는 구조임. 조작과 4D 표현에 활용 가능함</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2611.26954'>Learning Video Foresight Reasoning from Unlabeled Videos via On-Policy Self-Distillation</a></td><td>58</td><td>5</td><td>Video</td><td>unlabeled video로 foresight reasoning을 on-policy self-distillation함. 행동 예측과 연결됨</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2611.26787'>Spatial Query Execution as Verifiable Rewards for Multi-step Spatial Reasoning</a></td><td>56</td><td>5</td><td>Embodied AI</td><td>spatial query 실행을 verifiable reward로 쓰는 RL임. embodied spatial reasoning과 연결됨</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2611.27467'>ROSWORLD: When Digital Task Competence Meets Physical Execution</a></td><td>55</td><td>8</td><td>Embodied AI</td><td>로봇이 실제 GUI 데스크톱을 물리적으로 조작하는 benchmark임. 새 설정이나 benchmark 기여임</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2611.27499'>NavRSI: Recursive Harness Self-Improvement for Vision-and-Language Navigation</a></td><td>55</td><td>7</td><td>Navigation</td><td>LLM VLN harness를 재귀적으로 자기 개선함. 아이디어는 유행 흐름이며 증분적임</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2611.27121'>Portable Active Recovery under Timed and Position-Dependent Visual Outages</a></td><td>55</td><td>6</td><td>Navigation</td><td>위치 의존 시각 단절에서 쿼드로터의 능동 복구 방법임. 실패 복구 주제와 닿으나 규모 작음.</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2611.27459'>Ego2Ego: Generative Visual Perspective Taking Across Collaborators</a></td><td>55</td><td>5</td><td>Embodied AI</td><td>협업자 시점을 생성하는 visual perspective taking임. 다중 agent 공간 추론에 의미 있음</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2611.27516'>PhiJEPA: Denoising Latent Predictions for Visual Representation Learning</a></td><td>55</td><td>5</td><td>World Model</td><td>JEPA 계열 latent 예측 denoising과 planning 연결임. 표현 학습 아이디어가 있음</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2611.27074'>Hindsight Forcing: Learning Better History from the Future in Autoregressive Video Diffusion</a></td><td>55</td><td>4</td><td>Video</td><td>autoregressive video diffusion에서 미래로 history를 개선하는 학습임. world model 장기 생성에 관련됨</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2611.26858'>Staleness Deadlines for Motion Plans during Onboard Reasoning</a></td><td>54</td><td>7</td><td>Planning</td><td>onboard LLM 추론 지연 중 motion plan 유효기간 결정 문제를 다룸</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2611.26969'>RoboDyna: A Benchmark for Evaluating Robotic Manipulation under Physically Grounded Dynamics</a></td><td>52</td><td>8</td><td>Manipulation</td><td>동역학 기반 manipulation benchmark로 benchmark 기여 위주임</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2611.26763'>Search-Informed MPPI for Kinodynamic Motion Planning via Monte Carlo Tree Expansion</a></td><td>52</td><td>7</td><td>Planning</td><td>MCTS와 MPPI를 결합한 kinodynamic planning으로 고전 planning 개선임</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2611.26807'>NitroGen: Observations on the Action Dynamics, Visual Instruction Following, and Spatial Exploration</a></td><td>52</td><td>6</td><td>VLA</td><td>게임용 vision-action foundation model의 행동 특성 분석으로 로봇 policy에 시사점 있으나 분석 위주임</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2611.27327'>Embodied Interaction Policy: A Unified Model for Full-Duplex Human-Robot Interaction</a></td><td>52</td><td>6</td><td>Embodied AI</td><td>음성과 동작을 함께 내는 full-duplex 상호작용 policy를 제안함. HRI 통합 모델이나 로봇 조작 연관은 약함</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2611.27330'>GGDriver: Glance at What Is Shared, Gaze at What Differs for Perception-Free Planning</a></td><td>52</td><td>6</td><td>Autonomous</td><td>Driving 후보 궤적별로 장면의 다른 부분을 보는 perception-free planner임. 주행 도메인 개선임.</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2611.27136'>TrajRealm: A Large-Scale Point Tracking Dataset with Diverse Dynamics</a></td><td>52</td><td>5</td><td>3D Vision</td><td>대규모 point tracking dataset임. tracking 학습 자원으로 유용하나 dataset 기여임</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2611.27919'>SUAF: Spectral Universal Advantage Features for Zero-Shot Policy Improvement</a></td><td>52</td><td>5</td><td>RL</td><td>reward-independent 표현으로 zero-shot policy improvement를 다루는 RL 이론적 접근임</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2611.27381'>VMSA: Video Memory Skill Agent for Long Video Understanding</a></td><td>52</td><td>4</td><td>Video</td><td>long video 이해용 memory skill agent임. memory 구조 면에서 참고 가능함</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2611.27603'>Synthesizing Expressive Human-Object Interactions via Test-time Latent Adaptation</a></td><td>52</td><td>4</td><td>Motion</td><td>test-time latent adaptation으로 표현력 있는 human-object interaction을 합성함. TTO 아이디어는 흥미로우나 로봇 거리 있음</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2611.27226'>Trailblazer-F: Speculative Action-Flow Inference for Autonomous Driving</a></td><td>52</td><td>3</td><td>Driving</td><td>speculative inference로 driving world-action model의 지연을 줄임. 효율화 기법이며 주행 중심임</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2611.26809'>Search From the Start: Search-Native Pretraining for Language Models</a></td><td>52</td><td>0</td><td>NLP</td><td>search를 pretraining 단계에 넣는 아이디어임. 새롭지만 로봇 무관함</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2611.26971'>RoboPRO: A Perturbation-Resilient and Obstacle-Aware Benchmark for Robotic Manipulation</a></td><td>50</td><td>8</td><td>Manipulation</td><td>섭동과 장애물 대응 manipulation benchmark로 benchmark 기여 위주임</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2611.27305'>ManipScope: A Diagnostic Benchmark for Instruction Following and Generalization in Robotic Manipulation</a></td><td>50</td><td>8</td><td>Manipulation</td><td>instruction following 진단용 benchmark를 RoboTwin 위에 구축함. 평가 관점은 유용하나 benchmark 기여임</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2611.26996'>PonderPounce-WM: When Does Predicting the Future Help Context-Dependent Robot Control?</a></td><td>50</td><td>7</td><td>World Model</td><td>미래 token 예측이 context-dependent 제어에 도움되는지 분석한 소규모 연구임</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2611.27061'>PACE: Policy Augmentation and Compensation With Explicit Disturbance Estimation for Robust Locomotion</a></td><td>50</td><td>7</td><td>RL</td><td>명시적 외란 추정으로 quadruped locomotion 강건성을 높이는 incremental 개선임</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2611.27362'>NormFlowSDE: Normalizing Flows for Amortized Bayesian State Estimation</a></td><td>50</td><td>6</td><td>LG</td><td>normalizing flow로 amortized Bayesian 상태 추정을 함. 접촉 조작 맥락이나 응용 범위가 제한적임</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2611.27515'>Beyond a Single Human Demonstration: Learning from Scored Trajectory Alternatives for End-to-End Driving</a></td><td>50</td><td>5</td><td>RL</td><td>점수 있는 대안 궤적으로 end-to-end 주행 supervision을 확장함. IL 한계를 다루나 주행 한정임</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2611.27939'>What Must a Model Tell a Planner? Outcome Interfaces for Risk-Aware Planning After Robot Damage</a></td><td>50</td><td>5</td><td>Planning</td><td>손상된 로봇의 위험 인지 계획을 위한 model 인터페이스를 논함. 관점은 새로우나 실험 범위 제한적임</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2611.26937'>Looking Right Is Not Being Right: Evaluating the Geometry of Agent-Built 3D Scenes</a></td><td>50</td><td>4</td><td>3D Vision</td><td>agent가 만든 3D scene의 기하 정확도 평가임. 지적은 유용하나 benchmark 성격임</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2611.27024'>ReactDrive: Self-Reactive Driving World Model</a></td><td>50</td><td>4</td><td>World Model</td><td>상호작용 반응하는 driving world model임. 로봇 일반화는 불확실함</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2611.27289'>InterBand-EMG: A Cross-Band Foundation Model for Generalizable Hand-Pose Estimation</a></td><td>50</td><td>4</td><td>LG</td><td>sEMG 손 자세 foundation model임. 의수와 teleop에 연결 가능함</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2611.27638'>Seeing Is Not Steering: Where Verifiable Reasoning Can Enter an End-to-End Driving Planner</a></td><td>50</td><td>4</td><td>Driving</td><td>VLM 추론이 planner에 반영되는 위치를 분석함. 분석은 흥미로우나 주행 한정임</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2611.26897'>ProbeAgent: Principled Diagnosis of Agent Failures in Verifiable Environments</a></td><td>50</td><td>2</td><td>NLP</td><td>agent 실패를 검증 가능한 환경에서 진단함. failure diagnosis 관점은 관련되나 LLM agent 한정임</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2611.26916'>RoboCap-10k: A Metrically Accurate Egocentric Dataset for Robot Learning</a></td><td>48</td><td>7</td><td>Manipulation</td><td>metric 정확 egocentric 데이터셋으로 dataset 기여 위주임</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2611.26676'>One Behavior, Out of Order: Deterministic Execution and Parallel Simulation of ROS 2 Applications</a></td><td>48</td><td>6</td><td>Robotics</td><td>ROS 2 결정론적 실행과 병렬 시뮬레이션 도구로 로봇 시스템에 유용하나 학습 연구는 아님</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2611.27179'>Inject, Encode, Navigate: Feature-Wise Time Injection for Rectified Flow with Bidirectional Feature Encoding</a></td><td>48</td><td>6</td><td>Navigation</td><td>rectified flow와 time injection으로 navigation policy 속도를 높임. 엔지니어링 개선 위주임</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2611.27756'>Ref-YOLO-World: Decoupling Text-Side Computation for Efficient Referring Expression Comprehension on Edge Devices</a></td><td>48</td><td>5</td><td>Multimodal</td><td>edge에서 referring expression을 효율화하는 text 계산 분리임. 로봇 grounding 효율에 유용함</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2611.27509'>Self-Supervised Continuous-Time Depth Learning and Ego-Motion Estimation from Asynchronous Events</a></td><td>48</td><td>4</td><td>3D Vision</td><td>event에서 self-supervised depth와 ego-motion을 연속시간으로 학습함. 로봇 인지에 활용 가능함</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2611.27529'>Fix Where It Fails: Root-Cause-Guided Agentic Harness Optimization for Scene Graph Generation</a></td><td>48</td><td>4</td><td>Embodied AI</td><td>scene graph generation의 root cause 기반 harness 최적화임. scene graph 연관이나 agent 공학 성격임</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2611.27804'>Generalist Action Critic: Harnessing Frontier Models in Autonomous Driving</a></td><td>48</td><td>4</td><td>Driving</td><td>frontier 모델을 action critic으로 활용함. 주행 중심이며 증분적임</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2611.26904'>What Does a Zoom Actually Add? Decomposing Fine-Grained Perception Failures in Vision-Language Models</a></td><td>48</td><td>3</td><td>Multimodal</td><td>zoom이 주는 이득을 분해 분석함. 분석은 깔끔하나 방법 기여는 작음</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2611.26994'>SceneRuler: Measuring Physical Quantities in Video via Minimal Sufficient Reconstruction</a></td><td>48</td><td>3</td><td>Video</td><td>video에서 물리량을 재는 minimal reconstruction임. 정량 추론 새 과제임</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2611.27070'>$R^2$: Recognizing and Reducing Redundant Visual Tool Use</a></td><td>48</td><td>3</td><td>Multimodal</td><td>불필요한 visual tool 사용을 줄이는 방법임. agent 효율성 관점은 유용함</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2611.27715'>Recoverable Symbols, Unstable Execution: Auditing Internal Pathways and Decision Identity in Visual State Tracking</a></td><td>48</td><td>3</td><td>Multimodal</td><td>시각 state tracking에서 상징은 복원되나 실행이 불안정한 간극을 감사함. 분석 중심임.</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2611.27064'>Dynamic Token Merging for Efficient Vision-Language Models</a></td><td>48</td><td>2</td><td>Multimodal</td><td>VLM 시각 token을 동적으로 병합하는 효율화임. VLA에 적용 가능성은 있으나 직접 검증 없음.</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2611.27973'>MemOnce: A Scalable Memory Architecture for Large Language Models</a></td><td>48</td><td>1</td><td>LG</td><td>LLM 장기 상호작용용 재사용 memory 구조 제안임. memory 주제와 약하게 닿음.</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2611.27373'>GeoSDF-Diff: Geometry-Aware Diffusion Planning for Collision-Free Trajectories</a></td><td>47</td><td>5</td><td>Planning</td><td>SDF 기하 정보를 넣은 diffusion planner로 충돌 회피를 개선함. 증분적 개선임</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2611.27042'>RoboColiseum: Co-evolution of Simulation, Evaluation, and Models</a></td><td>46</td><td>7</td><td>Embodied AI</td><td>시뮬레이션 평가 플랫폼 구축으로 engineering 성격이 큼</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2611.27068'>Decision Models Are General-Purpose Process Reward Models</a></td><td>46</td><td>1</td><td>RL</td><td>decision model을 step 단위 process reward model로 씀. LLM agent 대상이고 로봇 연결 약함.</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2611.27397'>AnyBodyCodec: A Shared Native Interface for Body-Model Conversion, Extension, and Humanoid Control</a></td><td>45</td><td>5</td><td>Humanoid</td><td>SMPL-X, MHR 등 body model 간 변환 공통 인터페이스를 제공함. 도구 성격이 강함</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2611.27967'>Task2Hand: A Contact-Grounded Skill for Parametric Dexterous-Hand Morphology Design</a></td><td>45</td><td>5</td><td>Manipulation</td><td>dexterous hand 설계를 skill 패키지로 자동화함. 도구 성격이 강함</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2611.26910'>AstronautBench: Measuring Agent Self-Improvement Across Episodes Through Knowledge, Evidence, and Progress</a></td><td>45</td><td>4</td><td>Embodied</td><td>AI 에이전트의 에피소드 간 self-improvement를 재는 embodied benchmark임. 측정 설계는 유용하나 benchmark 기여임.</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2611.26730'>SparseHPS: A Unified Model for Human Pose and Shape across Depth Cameras and LiDARs</a></td><td>45</td><td>3</td><td>3D Vision</td><td>depth/LiDAR 통합 human pose/shape 모델임. 로봇 인지에 일부 유용함</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2611.27336'>Zing-1.0: A Playable World System Built on Controllable Rendering</a></td><td>45</td><td>3</td><td>World Model</td><td>제어 가능한 rendering 기반 playable world 시스템임. 게임 중심이나 world model 요소가 있음</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2611.27719'>VeilGS: Solving Darkness as a Veil of 2D Basis Maps over Retinex 3DGS</a></td><td>45</td><td>3</td><td>3D Vision</td><td>어두운 장면용 Retinex 3DGS임. 저조도 복원에 유용하나 incremental함</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2611.27127'>OpenRing: Deadlock-Free Execution of Any Planner on AGV Floors with One-Way Lanes</a></td><td>45</td><td>3</td><td>Navigation</td><td>AGV 일방통행 차선에서 deadlock을 막는 guard를 증명과 함께 제시함. 이론은 탄탄하나 학습 기반 로봇과는 거리 있음</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2611.27741'>Can Vision-Language Models Synthesize Executable Game-Playing Programs?</a></td><td>45</td><td>3</td><td>Multimodal</td><td>VLM이 실행 가능한 게임 플레이 program을 합성하는지 평가함. benchmark 성격임.</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2611.27865'>SLICR: Strategy Logic-Guided Multi-Agent Reinforcement Learning</a></td><td>45</td><td>3</td><td>RL</td><td>strategy logic으로 multi-agent RL을 유도함. formal specification 기반이나 로봇 검증 없음.</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2611.26933'>Tokenize Moments, Not Frames: Tokenizer-Aware Budget Allocation for Training-Free Video LLM Acceleration</a></td><td>45</td><td>2</td><td>Video</td><td>video LLM token 가속 기법임. training-free 효율화 수준임</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2611.27056'>A Continuous Relaxation of Quantization-Aware Training</a></td><td>45</td><td>1</td><td>LG</td><td>극저비트 quantization-aware training의 연속 완화임. 효율 추론이나 로봇 연결 약함.</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2611.26832'>Neural Geometry as a Learning Signal</a></td><td>45</td><td>0</td><td>NLP</td><td>신경 표현 기하를 학습 신호로 씀. 흥미로우나 근거가 제한적임</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2611.26841'>Weight-Space Programming Writes In-Context Learning and Matches Fine-Tuning in Language Models</a></td><td>45</td><td>0</td><td>NLP</td><td>예시로 weight 갱신을 써서 ICL이 fine-tuning에 맞먹음을 보임. 개념은 흥미로움</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2611.26797'>Memorization and Generalization in Generative Models: A Perspective From Energy-based Modeling and Associative Memory</a></td><td>45</td><td>0</td><td>LG</td><td>energy-based modeling과 associative memory로 생성모델의 암기와 일반화를 다룬 학위논문임. 이론 가치는 있으나 로봇 연결 약함.</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2611.27924'>BioEmu2: Scalable Emulation of Biomolecular Dynamics</a></td><td>45</td><td>0</td><td>LG</td><td>생체분자 동역학 생성 emulator임. 로봇 무관함.</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2611.27125'>When Students Fail to Learn from Teachers: Learning Dynamics of On-Policy Distillation</a></td><td>44</td><td>0</td><td>LG</td><td>on-policy distillation 학습 동역학 분석임. 로봇 무관함.</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2611.27048'>A Learning-Enhanced Control Scheme for Aerial Manipulator Under Composite Disturbances</a></td><td>42</td><td>6</td><td>Control</td><td>aerial manipulator 학습 보강 제어로 특정 플랫폼 제어 개선임</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2611.27263'>AELF: Active Terrain-Aware UAV Exploration Using a Lightweight Framework</a></td><td>42</td><td>5</td><td>Navigation</td><td>2.5D 지도로 UAV 탐사를 경량화함. 전형적인 시스템 엔지니어링임</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2611.27633'>Instant-LIVO: Efficient LiDAR-Inertial-Visual Odometry with Compact Geometry and a Bounded Single-Reference-Frame Map</a></td><td>42</td><td>5</td><td>SLAM</td><td>경량 LiDAR-IMU-Visual odometry임. 엔지니어링 중심임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2611.27101'>EgoSurgHands: An Egocentric 3D Hand Pose Dataset &amp; Benchmark for Open Surgery Training</a></td><td>42</td><td>3</td><td>CV</td><td>수술 egocentric 3D 손 자세 dataset임. demonstration 학습에 간접 유용함</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2611.27646'>MoHA: Model-Conditioned Harness Adaptation for Long-Video Agents</a></td><td>42</td><td>3</td><td>Video</td><td>long-video agent harness를 모델에 맞춰 적응함. agent 공학 성격임</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2611.27901'>QuantStream3D: Geometry-Aligned Low-Bit KV Cache Quantization for Streaming Visual Geometry Transformers</a></td><td>42</td><td>3</td><td>3D Vision</td><td>streaming geometry transformer의 KV cache 양자화로 효율화 기여는 있으나 incremental 수준임</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2611.26972'>When Perception Collides with Priors: Diagnosing Modal Polarization in Video Understanding Models</a></td><td>42</td><td>2</td><td>Video</td><td>video MLLM의 prior와 perception 충돌 진단임. 분석 위주임</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2611.27224'>EAST: Event-Anchored Surface Transport for Event-Based Gaussian Reconstruction</a></td><td>42</td><td>2</td><td>3D Vision</td><td>event 기반 Gaussian 표면 복원임. 센서 특화 기법임</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2611.26917'>What Does the Visual Encoder Buy? Visual Information Gain in Encoder-Free Multimodal Pretraining</a></td><td>42</td><td>1</td><td>Multimodal</td><td>encoder-free 사전학습의 visual information gain 분석임. 로봇 연관 약함</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2611.27288'>Preserving Pretrained CFG Structure in RL for Diffusion Models with Conditional Contrast Regularization</a></td><td>42</td><td>1</td><td>Generative</td><td>diffusion RL에서 CFG 구조 보존 regularization으로 incremental임</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2611.27570'>WEIR: Watershed Exploration and Drift-Aware Prefix Shrinkage for Multi-Turn Agent Reinforcement Learning</a></td><td>42</td><td>1</td><td>RL</td><td>multi-turn agent RL의 credit assignment 개선이나 LLM agent 중심임</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2611.27159'>From Acting to Learning: Experience Selection toward Continually Learning Agents</a></td><td>42</td><td>1</td><td>LG</td><td>연속 학습 에이전트의 경험 선택 연구임. 4B 언어 에이전트 대상임.</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2611.27365'>WePM: Hierarchical Conflict Reconciliation for Unified MLLMs</a></td><td>42</td><td>1</td><td>Multimodal</td><td>온디바이스 통합 MLLM의 충돌 조정 병합임. 효율 중심이고 로봇 연결 약함.</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2611.27201'>Backbone-Specific LoRA Geometry: Orthogonality, Superposition, and Provenance</a></td><td>42</td><td>0</td><td>LG</td><td>LoRA 기하와 backbone 특이성 분석임. 이론적 관찰이나 로봇 무관함</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2611.26863'>LLMs Memorize Their Own Hallucinations During Post-Training</a></td><td>42</td><td>0</td><td>NLP</td><td>post-training 중 LLM이 자기 hallucination을 암기함을 분석함. 분석 연구임</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2611.27233'>LongCat Recall Sparse Attention: Co-Designing Key Organization and Retrieval for Long-Context Inference</a></td><td>42</td><td>0</td><td>NLP</td><td>sparse attention의 key 조직과 검색을 공동 설계함. 효율적 추론이나 로봇 무관함</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2611.27764'>Enhancing Attention with Higher-Order Attention</a></td><td>42</td><td>0</td><td>LG</td><td>attention에 고차 항을 넣는 LLM 구조 변형임. 효과 검증 제한적이고 로봇 무관함.</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2611.27911'>Functional Depth Is Learned: Isolating the Computation That Layers Produce Only Together</a></td><td>42</td><td>0</td><td>LG</td><td>transformer 깊이가 실제 순차 계산을 만드는지 분석함. 로봇 무관함.</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2611.26950'>Mechanistic Analysis of Unified Proximity-Tactile Observation by a Capacitive Fingertip Array Constrained by a Metal Phalanx</a></td><td>40</td><td>6</td><td>Tactile</td><td>용량성 fingertip 센서의 기전 분석으로 하드웨어 특성 위주임</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2611.27181'>HumanoidPose: Monocular 3D Pose Estimation for Humanoid Robots</a></td><td>40</td><td>5</td><td>CV</td><td>휴머노이드 로봇의 단안 3D pose estimation 데이터와 방법을 제시함. 로봇 학습과의 연결은 약함</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2611.27423'>ADEPT: Adaptive Monocular Depth Estimation via Model-In-The-Loop Photometric Tuning with Capture Risk Prediction</a></td><td>40</td><td>4</td><td>CV</td><td>depth 모델 feedback으로 노출과 gain을 조절함. 응용 범위가 좁고 증분적임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2611.26783'>CADENCE:Temporally Coherent Whole-Body Human Mesh Recovery that Preserves Expressive Hand Motion</a></td><td>40</td><td>2</td><td>3D Vision</td><td>시간적으로 일관된 whole-body mesh 복원임. 손 동작 보존은 유용하나 incremental함</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2611.26842'>3D Open-Vocabulary Detection via Visual Alignment and Generative Captions</a></td><td>40</td><td>2</td><td>3D Vision</td><td>야외 open-vocabulary 3D detection임. 2D VLM 지식 전이 방식은 흔함</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2611.27030'>TSIR: Ray-Traced Triangle Splats for Inverse Rendering</a></td><td>40</td><td>2</td><td>3D Vision</td><td>ray-traced triangle splat inverse rendering임. 렌더링 기술 중심임</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2611.27029'>Mind World Models: Joint Learning of Motor EEG Representations and Action-Conditioned World Dynamics</a></td><td>40</td><td>2</td><td>World Model</td><td>EEG 운동 디코딩에 action-conditioned world dynamics를 쓰나 BCI 응용임</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2611.27044'>Action-Conditioned Spatio-Temporal Forecasting</a></td><td>40</td><td>2</td><td>World Model</td><td>action-conditioned 시공간 예측에서 불필요한 변화 억제 문제를 다루나 로봇 직접 연결 약함</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2611.26803'>Don&#x27;t Discard Your Rollouts: Reusing Teacher RL Traces for Student Distillation</a></td><td>40</td><td>1</td><td>RL</td><td>teacher RL trace를 distillation에 재사용하는 효율화 기법임</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2611.27148'>Structure Over Scale: Rethinking Adaptation for Reinforcement Learning with Verifiable Rewards</a></td><td>40</td><td>1</td><td>RL</td><td>RLVR에서 adaptation 구조 분석이나 LLM 중심임</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2611.27875'>From Gist to Verbatim: The Controllable Path of One Image Through a Diffusion Prior</a></td><td>40</td><td>1</td><td>Generative</td><td>diffusion prior의 기억 회상 제어 분석이나 로봇 연결 약함</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2611.26806'>MedicalRSI: Medical Recursive Self-Improving Agents via Clinical Model-Harness Co-Evolution</a></td><td>40</td><td>1</td><td>NLP</td><td>의료 agent의 harness 공진화임. 로봇 무관하며 유행 흐름의 증분임</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2611.27750'>RoSci: Exploring Robustness in Science VLMs</a></td><td>40</td><td>1</td><td>Multimodal</td><td>과학 VLM의 입력 결함 강건성을 재는 benchmark 성격임. 로봇 연관 없음.</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2611.26976'>MixFold: Sub-4-Bit Mixed-Precision LLM Inference via Output-Channel Grouping on Mobile NPUs</a></td><td>40</td><td>1</td><td>LG</td><td>모바일 NPU용 sub-4bit mixed-precision LLM 추론임. 시스템 최적화 중심임.</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2611.26756'>Reinforcement Learning Unlearns Corrupted SFT Reasoning</a></td><td>40</td><td>0</td><td>NLP</td><td>corrupt된 SFT 추론을 RL이 교정함을 보임. 분석은 흥미로우나 로봇 무관함</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2611.27217'>CoPyro: Feeding Copy Proposals to Parallel Drafters</a></td><td>40</td><td>0</td><td>NLP</td><td>복사 제안을 병렬 drafter에 넣어 speculative decoding을 개선함. 효율 개선임</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2611.27317'>Do Language Models Know Which Words Steer Their Reasoning?</a></td><td>40</td><td>0</td><td>NLP</td><td>CoT를 유도하는 단어를 분석함. 해석 연구임</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2611.27348'>Breaking the Long Horizon: Short-Horizon Process Supervision for Long-Form Generation in LLMs</a></td><td>40</td><td>0</td><td>NLP</td><td>단기 horizon process supervision으로 장문 생성 RL을 개선함. 증분적임</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2611.27286'>Belief-State Management Meets Rubric Rewards for Agentic Forecasting</a></td><td>40</td><td>0</td><td>NLP</td><td>belief-state 관리와 rubric reward로 forecasting 에이전트를 개선함. 로봇 무관함.</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2611.27891'>Speculative Decoding Is Less Speculative Than You Think</a></td><td>40</td><td>0</td><td>LG</td><td>speculative decoding 효율 분석임. 로봇 무관함.</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2611.27845'>Humanoid robots for safety-critical electrical switching: A perception-informed runtime constraint filter</a></td><td>38</td><td>4</td><td>Safety</td><td>휴머노이드 전기 스위치 작업의 runtime safety filter임. 응용 사례 중심임</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2611.27932'>Interactive Semi-Parametric On-Track Learning for Vehicle Dynamics in Autonomous Racing</a></td><td>38</td><td>3</td><td>Driving</td><td>레이싱용 차량 dynamics 온트랙 학습임. 응용 한정임</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2611.27003'>S2D-Splat: Static-First Gaussian Reconstruction of Dynamic Driving Scenes with Layer-Wise Feature Guidance</a></td><td>38</td><td>2</td><td>3D Vision</td><td>동적 주행 장면 static-first Gaussian 복원임. 주행 특화 incremental함</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2611.27383'>PanoUAV-Track: Full-Spherical UAV Visual Tracking in the Wild</a></td><td>38</td><td>2</td><td>CV</td><td>전방위 UAV tracking benchmark임. dataset 기여임</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2611.27547'>GameScrub: Learning HUD Removal from Real Gameplay with Recovered Targets</a></td><td>38</td><td>2</td><td>Video</td><td>게임 영상 HUD 제거 학습임. world model 데이터 정제에 간접 관련됨</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2611.27788'>When Does Looking Closer Pay Off? Simple Foveated ViTs for Fine-Grained Recognition</a></td><td>38</td><td>2</td><td>CV</td><td>foveated ViT 세밀 인식 분석임. active perception과 약하게 연결됨</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2611.27631'>Learning Inside Types: Epistemic Typestates for Safe Multi-Agent Reinforcement Learning</a></td><td>38</td><td>2</td><td>RL</td><td>다중 에이전트 RL에 epistemic typestate를 도입함. 안전 RL이나 로봇 검증 없음.</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2611.26734'>INCISE: Training-Free In-Context Segmentation of Surgical Videos</a></td><td>38</td><td>1</td><td>CV</td><td>수술 영상 training-free in-context segmentation임. 응용 도메인 한정임</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2611.27089'>Writing Weights or Training Them? Spatial Reasoning through Weight-Space Programming and Low-Rank Adaptation</a></td><td>38</td><td>1</td><td>LG</td><td>weight-space programming과 LoRA로 공간 추론을 비교함. 작은 모델 소규모 실험임.</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2611.26702'>Model the Annotation, Not the Noise: Semantic Annotation-Channel Prompt Learning against Noisy Labels</a></td><td>38</td><td>0</td><td>Multimodal</td><td>VLM prompt learning의 noisy label 대응임. 로봇 연관 없고 incremental함</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2611.27252'>Beyond Prompt Imitation: Capability-Aware Video Generation with Smaller Models</a></td><td>38</td><td>0</td><td>Generative</td><td>작은 video generator 추론 시 보강의 oracle ladder 평가임. 로봇 무관함</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2611.26920'>Partially canonical axes in large language model representations</a></td><td>38</td><td>0</td><td>NLP</td><td>LLM 표현 축의 의미를 분석함. 해석 연구임</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2611.27326'>Reasoning in Fewer Tokens: Concept-Normalized Multilingual Scratchpads and Reversible Model-Adaptive Reasoning Codes</a></td><td>38</td><td>0</td><td>NLP</td><td>다국어 scratchpad로 추론 토큰을 줄임. 효율 개선임</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2611.26975'>Run One, Get Two: Near-Free Streaming Safety Checks for Local LLMs</a></td><td>38</td><td>0</td><td>LG</td><td>로컬 LLM decoding 중 안전 검사를 거의 공짜로 하는 방법임. 효율 아이디어지만 로봇 무관함.</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2611.27032'>Disentangling Verbalized Evaluation Awareness and Refusal through Neuron-Level Intervention</a></td><td>38</td><td>0</td><td>NLP</td><td>평가 인식과 refusal을 neuron 수준에서 분리함. 로봇 무관함.</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2611.27622'>Benchmarks&#x27; Last Exam</a></td><td>38</td><td>0</td><td>NLP</td><td>benchmark 과제 검증 문제 제기임. 로봇 무관함.</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2611.27738'>Average-Depth Variable Execution via Request-Local Token Routing</a></td><td>38</td><td>0</td><td>LG</td><td>token별 layer 실행량을 정하는 라우팅 효율화임. 로봇 무관함.</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2611.27375'>Gumbel Substitution: Removing Sampler Drift from RL Without Trusting the Sampler</a></td><td>36</td><td>1</td><td>RL</td><td>sampler drift 보정 RL 기법으로 LLM RL 효율 관련임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2611.27443'>Learning When to Ask: Advisor-Aware Post-Training for SLM Agents</a></td><td>36</td><td>1</td><td>NLP</td><td>SLM agent가 advisor에게 묻는 시점을 학습하나 LLM 중심임</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2611.27077'>Accelerating Muon with Spectral Residual Correction</a></td><td>36</td><td>0</td><td>LG</td><td>Muon optimizer 가속 기법으로 incremental임</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2611.27131'>Distillation with Errors: Sparse Unbiased Backpropagation for Knowledge Distillation</a></td><td>36</td><td>0</td><td>LG</td><td>KD backprop 희소화로 효율화 기법임</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2611.27227'>CreditFilter: Calibrated Token Weights over the Within-Response Entropy Rank for RLVR</a></td><td>36</td><td>0</td><td>RL</td><td>RLVR token weighting 개선으로 incremental임</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2611.27477'>Cannot Wait to Verify: Parallel Drafting to Eliminate Verifier Idle Time in Speculative Decoding</a></td><td>36</td><td>0</td><td>LG</td><td>speculative decoding 병렬 drafting 효율화로 incremental임</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2611.27653'>Late-Time Dynamics of Flow Matching: Distance Geometry and Learning</a></td><td>36</td><td>0</td><td>Generative</td><td>flow matching 후반 dynamics 이론으로 로봇 연결 약함</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2611.27759'>DPMA: Learning to Compress Mixture-of-Experts Models</a></td><td>36</td><td>0</td><td>LG</td><td>MoE 압축 학습 방법으로 incremental임</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2611.26906'>Budget-Aware Predict-and-Verify Theorem Proving with Heterogeneous LLM Solvers</a></td><td>36</td><td>0</td><td>NLP</td><td>비용 인지 theorem proving 라우팅임. 로봇 무관함.</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2611.27100'>Reasoning in Two Dimensions: Quantifying Chain-of-Thought Faithfulness and Efficiency</a></td><td>36</td><td>0</td><td>NLP</td><td>CoT 충실도와 효율을 정량화함. 로봇 무관함.</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2611.27350'>GRACE: Controlled Evidence Interventions for Diagnosing and Improving Knowledge Integration in GraphRAG</a></td><td>36</td><td>0</td><td>NLP</td><td>GraphRAG 증거 개입 진단임. 로봇 무관함.</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2611.27369'>AMARIS: Merging Generalist and Specialist LLMs via Adaptive Subspace Inheritance</a></td><td>36</td><td>0</td><td>NLP</td><td>범용과 전문 LLM 병합 방법임. 로봇 무관함.</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2611.27554'>Vega-Fafnir: Is Greedy Decoding the Same Decoding? Where Rounding Noise in Speculative Verification Comes From and What Removing It Costs</a></td><td>36</td><td>0</td><td>LG</td><td>greedy decoding의 반올림 잡음 분석임. 로봇 무관함.</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2611.27782'>An Autonomous Adaptive Learning System for Robotic Grasping in the Circular Factory</a></td><td>35</td><td>6</td><td>Manipulation</td><td>순환 제조 환경의 적응형 grasping 시스템임. 응용 시스템 중심임</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2611.27667'>GeoScaffold: From Latent to Realized Geometry in Collaborative Detection</a></td><td>35</td><td>3</td><td>3D Vision</td><td>협력 3D detection의 기하 보강임. 주행 한정 incremental함</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2611.27540'>Where Delay Compensation Belongs in a Decentralized Mean-Field-Game Swarm with a Control-Barrier Safety Filter</a></td><td>35</td><td>3</td><td>Multi-robot</td><td>MFG 군집에서 지연 보상 위치를 분석함. 이론 위주이고 범위가 좁음</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2611.27453'>AppCon-Bench: Perception and Misperception of Material Appearance in Vision-Language Models</a></td><td>35</td><td>2</td><td>Multimodal</td><td>재질 appearance constancy를 VLM으로 평가함. benchmark 성격임</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2611.27299'>Re-JEPA: Coupling Representation Prediction and Signal Reconstruction for State-Conditioned EMG Tracking</a></td><td>35</td><td>2</td><td>LG</td><td>EMG 손 추적에 JEPA를 결합함. 로봇 조작과 직접 연결 약함</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2611.27128'>Analyzing Multi-Layer Visual Representations of Large Vision-Language Models for Anomaly Detection</a></td><td>35</td><td>1</td><td>Multimodal</td><td>LVLM multi-layer feature의 이상 탐지 분석임. 분석 위주임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2611.27264'>EAGLE: Entity-Aware Grounding with Layered Evidence for High-Resolution Image Understanding</a></td><td>35</td><td>1</td><td>Multimodal</td><td>고해상도 이미지 grounding MLLM임. incremental함</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2611.27389'>Beyond What They Say: Cue Acknowledgment and Robustness in Vision-Language Models</a></td><td>35</td><td>1</td><td>Multimodal</td><td>VLM의 cue 인정과 robustness 분석임. 로봇 연관 낮음</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2611.27780'>Search-RSI: Expanding Search Worlds Along Multimodal Agents&#x27; Capability Frontier</a></td><td>35</td><td>1</td><td>Multimodal</td><td>multimodal search agent 확장임. 로봇 연관 낮음</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2611.27931'>DiTraR: Diverse Scorers and Transcript-Guided Re-ranking for Video Corpus Moment Retrieval</a></td><td>35</td><td>1</td><td>Video</td><td>video moment retrieval re-ranking 개선으로 incremental임</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2611.26978'>Affine-Image Propagation for Tight and Scalable Neural Network Verification</a></td><td>35</td><td>1</td><td>LG</td><td>l2 신경망 검증 bound 개선으로 이론 기여가 있으나 로봇 연결 약함</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2611.27216'>Correct Precedents Induce Policy Violations in On-Device LLM Agents</a></td><td>35</td><td>1</td><td>NLP</td><td>on-device agent가 선례에 유도돼 정책을 위반하는 실패를 보임. 안전 분석임</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2611.27698'>Spatiotemporal Graph Neural Networks for Fault Detection and Structural Learning in Chemical Processes: Use Case on the Tennessee Eastman Process</a></td><td>35</td><td>1</td><td>LG</td><td>화학 공정 fault detection용 spatiotemporal GNN임. 응용 도메인임.</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2611.26726'>Decomposing images in a PRISM: A Single-Source Multi-View Framework for Image Representation</a></td><td>35</td><td>0</td><td>CV</td><td>단일 입력에서 multi-view를 만드는 표현 학습임. 아이디어는 있으나 영향 제한적임</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2611.27142'>How Does SAM-3 Adapt? Capacity, Update Geometry, and Domain Transfer</a></td><td>35</td><td>0</td><td>CV</td><td>SAM-3 fine-tuning 분석임. 로봇 연관 낮음</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2611.27266'>PP-CFG: Polarity-Preserving Guidance for Controllable Few-Step Image and Video Generation</a></td><td>35</td><td>0</td><td>Generative</td><td>few-step 생성의 CFG 보존 구조임. 로봇 무관함</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2611.27285'>SIR-Agent: Skill-Augmented Image Restoration Agent with Recursive Self-Improvement</a></td><td>35</td><td>0</td><td>Multimodal</td><td>이미지 복원 agent 자기개선임. 로봇 무관함</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2611.26747'>SkillPrivus: Uncovering PRIVacy of USe Harms in Agentic Skills</a></td><td>35</td><td>0</td><td>NLP</td><td>agent skill의 privacy 위험을 분석함. 로봇과 무관함</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2611.26835'>Non-Expanding Gated Continued Fraction Architecture for Feedforward Layers in Language Models</a></td><td>35</td><td>0</td><td>LG</td><td>continued fraction feedforward 구조 개선임. 소폭 개선임</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2611.26874'>How Language Models Compress and Compare: Understanding Selection with Token Covariance Maps</a></td><td>35</td><td>0</td><td>NLP</td><td>token covariance map으로 선택 과제를 분석함. 해석 연구임</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2611.27139'>Do Senior Agents Do Their Job? Measuring Role Integrity in How LLM Agents Use Subordinate Material</a></td><td>35</td><td>0</td><td>NLP</td><td>multi-agent LLM의 senior agent 역할 이행 측정임. 평가 위주임</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2611.27353'>WaXup: Weight Averaging of Experts as Data Augmentation for Robust Introspection</a></td><td>35</td><td>0</td><td>NLP</td><td>weight averaging으로 introspection을 강건화함. 소폭 개선임</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2611.27445'>Structurally Different, Functionally Persistent: Capability Regions Under Model Optimization</a></td><td>35</td><td>0</td><td>NLP</td><td>최적화 후에도 capability 영역이 유지됨을 분석함. 범위 좁음</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2611.27762'>From Novel Combinations to Informative Absence: Structural permission, communicative opportunity, and form choice in language learning</a></td><td>35</td><td>0</td><td>NLP</td><td>언어 학습의 counterfactual 표현 기회 이론임. 이론적 흥미는 있으나 로봇 무관함.</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2611.27329'>H-MSAE: Hierarchical Sparse Concept Coverage for Efficient and Diverse Instruction Data Selection</a></td><td>35</td><td>0</td><td>NLP</td><td>명령 데이터 선택 기법임. 로봇 무관함.</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2611.26752'>Depth-Linked Residual Tokens for Multimodal Retrieval and Generation</a></td><td>34</td><td>1</td><td>Multimodal</td><td>looped 구조와 special token 결합으로 retrieval 효율을 높이는 기법임</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2611.27087'>ORION: Exact Canonical-State Supervision for Systematic Generalization in Transformers</a></td><td>34</td><td>0</td><td>LG</td><td>Transformer 체계적 일반화 supervision으로 로봇 연결 약함</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2611.27500'>Turnout: Adaptive Attention Switching for Efficient Reasoning</a></td><td>34</td><td>0</td><td>LG</td><td>linearized attention 전환 효율화로 로봇과 무관함</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2611.27962'>Model Carving: Training Transformers That Optimize Their Own Topology</a></td><td>34</td><td>0</td><td>LG</td><td>학습 중 Transformer topology를 최적화하나 로봇 연결 약함</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2611.27133'>MAPES: Multi-Value Alignment Pipeline via Expert Specialization</a></td><td>34</td><td>0</td><td>NLP</td><td>다중 가치 정렬 파이프라인임. 로봇 무관함.</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2611.27710'>Abstract What Varies, Reuse Longer Patterns: Efficient Offline Chain-of-Thought Compression</a></td><td>34</td><td>0</td><td>NLP</td><td>오프라인 CoT 압축 방법임. 로봇 무관함.</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2611.27921'>ESSI: Computationally Efficient Semantic Search for Sparse Autoencoder Concepts</a></td><td>33</td><td>1</td><td>Generative</td><td>SAE 개념 검색 효율화로 로봇 연관 약함</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2611.26931'>Improving the Optimisation Landscape for Particle Mixtures</a></td><td>33</td><td>0</td><td>LG</td><td>particle mixture 최적화 이론으로 로봇과 무관함</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2611.27092'>PLoQ: A Prompt-Specific Low-Rank Basis for 4-bit Quantization of LLM Activations</a></td><td>33</td><td>0</td><td>LG</td><td>LLM activation 4-bit 양자화 기법으로 incremental임</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2611.26717'>Coherence by Construction: Synthesizing CTI Knowledge Graphs and the Formal Limits of Coherence Validation</a></td><td>33</td><td>0</td><td>NLP</td><td>LLM으로 CTI knowledge graph를 합성하는 방법임. 로봇 무관함.</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2611.26794'>Beyond Final Answers: Interpretable Tumor Immune Microenvironment Reasoning from H&amp;E and mIF</a></td><td>33</td><td>0</td><td>Multimodal</td><td>병리 이미지 기반 종양 면역 추론임. 의료 응용이고 로봇 무관함.</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2611.26998'>Reward Integrity in Adversarial Reinforcement Learning for LLM Guardrail Red-Teaming</a></td><td>33</td><td>0</td><td>RL</td><td>LLM guardrail red-teaming에서 reward 무결성 문제를 다룸. 로봇 무관함.</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2611.27138'>Double counting in LLM evidence fusion: exact posteriors separate rule compliance from posterior gain</a></td><td>33</td><td>0</td><td>LG</td><td>LLM 증거 융합의 이중 계산 분석임. 로봇 무관함.</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2611.27424'>Jagged Robustness: Uneven Safety Transfer and Emerging Vulnerabilities under LLM Quantization</a></td><td>33</td><td>0</td><td>NLP</td><td>quantization이 LLM 안전성에 미치는 영향 감사임. 로봇 무관함.</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2611.27686'>Learning in Symbiosis: Heterogeneous Federated Learning with ANNs and SNNs</a></td><td>33</td><td>0</td><td>LG</td><td>ANN과 SNN 이종 federated learning임. 로봇 무관함.</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2611.27129'>Opto-Electronic Hybrid Reinforcement Learning Based on MZI for Robotic Manipulator Control</a></td><td>32</td><td>3</td><td>RL</td><td>광전 하이브리드 하드웨어로 manipulator RL 제어를 함. 특수 하드웨어 중심이고 과제가 단순 reaching임</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2611.27539'>Joint Optimization of Fleet Size, Localization Infrastructure, and Trajectories for Multi-AUV Persistent Monitoring</a></td><td>32</td><td>3</td><td>Planning</td><td>다수 AUV의 fleet 규모와 궤적을 최적화함. 최적화 응용이며 학습 요소 약함</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2611.27063'>V2VFusion: Text-Controlled Video-to-Video Diffusion for Degradation-Aware Video Fusion</a></td><td>32</td><td>1</td><td>Video</td><td>degradation-aware video fusion diffusion임. 로봇 연관 낮음</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2611.27339'>Unimodal Shortcuts and Joint Scene-Intent Dependence in Vision-Language Safety Representations</a></td><td>32</td><td>1</td><td>Multimodal</td><td>VLM 안전성 표현의 shortcut 분석임. 로봇 연관 낮음</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2611.27811'>Redesigning Neural Networks to Not be Confidently Wrong even to Strong Adversarial Attacks</a></td><td>32</td><td>1</td><td>CV</td><td>적대 공격에 자신 있게 틀리지 않는 구조 재설계임. 로봇 연관 낮음</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2611.26722'>TOUMAII: A 4.5M-Pair Tool-Calling Preference Dataset and Its Source-Agnostic Generator</a></td><td>32</td><td>1</td><td>NLP</td><td>tool-calling 선호 데이터셋과 생성기임. 데이터 규모 중심 기여임.</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2611.27161'>Real-Anchored Complementary Evidence for Generalizable AI-Generated Image Detection</a></td><td>32</td><td>0</td><td>CV</td><td>AI 생성 이미지 탐지 일반화임. 로봇 무관함</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2611.26711'>Parasite Features: Causal Abstraction Through Spurious Pathways</a></td><td>32</td><td>0</td><td>LG</td><td>causal abstraction의 spurious pathway 분석으로 해석가능성 이론임</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2611.27155'>The Vulnerability Window: Decision Instability in Quantized Reward Models</a></td><td>32</td><td>0</td><td>LG</td><td>양자화 reward model 불안정성 분석으로 로봇과 무관함</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2611.27193'>cmHC: Balancing Stream Mixing in Hyper-Connections via Geometric Contraction</a></td><td>32</td><td>0</td><td>LG</td><td>hyper-connection 변형 안정화로 incremental임</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2611.27258'>A preference for local interaction between layers emerges during training</a></td><td>32</td><td>0</td><td>LG</td><td>층 간 local interaction 학습 현상 분석으로 로봇과 무관함</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2611.27376'>Composable Soft-Prompt Distillation of RL Experts: Toward Continual Post-Training</a></td><td>32</td><td>0</td><td>RL</td><td>RL expert를 soft prompt로 증류하는 continual post-training임</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2611.27578'>PRISM: Validation-Free Online Batch Selection for LLM Fine-Tuning via Preconditioned Conic Ghost Matching</a></td><td>32</td><td>0</td><td>LG</td><td>LLM fine-tuning batch selection으로 incremental임</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2611.27951'>Topology Hub Optimal Transport: Eliminating Long Context Dilution at Flash Speed</a></td><td>32</td><td>0</td><td>LG</td><td>long-context attention 최적수송 기법으로 incremental임</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2611.27083'>How Far Does Lossless Re-tokenization Move an RLVR Update?</a></td><td>32</td><td>0</td><td>RL</td><td>re-tokenization이 RLVR 갱신에 미치는 영향 분석임. 범위 좁음</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2611.27444'>Silent Arbitration: How Large Language Models Resolve Co-Authoritative Conflicting Instructions</a></td><td>32</td><td>0</td><td>NLP</td><td>동등 권한 지시 충돌 해소 분석임. 분석 연구임</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2611.26935'>Self-similar Organization of Information in Language</a></td><td>32</td><td>0</td><td>NLP</td><td>언어의 predictive information 자기유사 구조 분석임. 로봇 무관함.</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2611.27116'>CoEvoBench: Can LLMs Drive Recursive Co-Evolution of Agentic Systems?</a></td><td>32</td><td>0</td><td>NLP</td><td>LLM의 에이전트 시스템 공진화 benchmark임. 로봇 무관함.</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2611.27294'>HookEvo: A Framework for Coordinated Plugin Evolution on Hook-Enabled Agent Runtimes</a></td><td>32</td><td>0</td><td>NLP</td><td>에이전트 runtime plugin 공진화 프레임워크임. 로봇 무관함.</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2611.27495'>Trained on Harm, Still Refusing: A Training-Time Defense for Code Generation</a></td><td>32</td><td>0</td><td>NLP</td><td>코드 LM 안전 학습 방어임. 로봇 무관함.</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2611.27817'>BRINA: Bottom-Referenced Inertial Navigation with AKAZE, a Sonar SLAM for Autonomous Marine Vehicles</a></td><td>30</td><td>3</td><td>SLAM</td><td>sonar SLAM 방법임. 수중 특화이고 기여가 작음</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2611.27953'>Real-time neuromorphic audio and vision perception for autonomous robotic applications: Integration and experimental evaluation on a rover platform</a></td><td>30</td><td>3</td><td>Robotics</td><td>뉴로모픽 오디오 비전을 rover에 통합함. 시스템 평가 위주임</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2611.27435'>Learned Network Dynamics for Model Predictive Traffic Signal Control under Incidents</a></td><td>30</td><td>2</td><td>LG</td><td>교통 신호 MPC용 학습 dynamics로 로봇 연결 약함</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2611.27447'>Mechanism Parity for Simulation-Based Validation of Autonomous-Driving Perception</a></td><td>30</td><td>2</td><td>Driving</td><td>합성과 실제 주행 인식의 mechanism parity를 검증함. 로봇 학습과 거리 있음</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2611.26715'>SCATR-ITS: a scalable transformer for large-area individual tree segmentation from LiDAR point clouds</a></td><td>30</td><td>1</td><td>3D Vision</td><td>LiDAR 나무 분할용 transformer임. 응용 특화 성격 강함</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2611.27110'>RemoteEvolver: Expanding Earth Observation Capabilities through Agent Harness Evolution</a></td><td>30</td><td>1</td><td>Multimodal</td><td>원격탐사 agent harness 진화임. 응용 특화함</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2611.27135'>Crafting the Difference, Grounding the Evidence: Discriminative Concept Learning for Zero-Shot Skeleton Action Recognition</a></td><td>30</td><td>1</td><td>CV</td><td>zero-shot skeleton 행동 인식 개념 학습임. incremental함</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2611.27341'>ReSA: Preserving Reference-Specified Foreground in In-Context Segmentation</a></td><td>30</td><td>1</td><td>CV</td><td>in-context segmentation 전경 보존임. incremental함</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2611.26966'>Keep the Process, Change the Supplier: Runtime Governance for Tool-Using AI Agents</a></td><td>30</td><td>1</td><td>NLP</td><td>tool 사용 에이전트의 runtime governance 설계임. 로봇 무관함.</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2611.27102'>One state, many questions: Opsis gives a frontier model typed eyes for pathology</a></td><td>30</td><td>0</td><td>Multimodal</td><td>병리 보고용 typed 인터페이스임. 로봇 무관함</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2611.27229'>Prune to Expand: Training Prompt Enhancers with Less to Imitate</a></td><td>30</td><td>0</td><td>Generative</td><td>prompt enhancer 학습 데이터 정리임. 로봇 무관함</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2611.27268'>Budgeted Safety Verification for Streaming Video Generation</a></td><td>30</td><td>0</td><td>Video</td><td>streaming 영상 생성 안전 검증임. 로봇 무관함</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2611.27855'>Anchors That Move Without Collapsing: Exclusive-Region Anchor Routing for Vision Transformers</a></td><td>30</td><td>0</td><td>CV</td><td>ViT anchor routing임. incremental함</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2611.26856'>Self-Supervised Learning with Recursive Quadrature Filters for Neural Time Series</a></td><td>30</td><td>0</td><td>LG</td><td>시계열 self-supervised filter 학습으로 로봇과 무관함</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2611.27104'>Reliable Behavior Discovery via False Discovery Rate Control</a></td><td>30</td><td>0</td><td>LG</td><td>생성 모델 behavior discovery의 FDR 제어로 로봇과 무관함</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2611.27203'>Improved Accuracy Scaling with Problem Complexity in LLM Arithmetic Reasoning Using Executable Symbolic Representations</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 산술 추론 symbolic 표현 분석으로 로봇과 무관함</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2611.27243'>More Bits Won&#x27;t Fix It: Diagnosing and Treating an Ill-Conditioned Backward Pass (A Case Study on Gemma-4)</a></td><td>30</td><td>0</td><td>LG</td><td>Gemma LoRA 역전파 수치 문제 사례 연구임</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2611.27377'>HR-Merge: Model Merging with Headroom-Weighted Residual Refinement</a></td><td>30</td><td>0</td><td>LG</td><td>model merging 변형으로 incremental임</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2611.27610'>Circular Predictive Coding Unlocks Effective Depth</a></td><td>30</td><td>0</td><td>LG</td><td>predictive coding 깊이 문제 개선으로 로봇과 무관함</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2611.27656'>Beyond Sample Hardness: Adaptive Data Selection through Learning Dynamics</a></td><td>30</td><td>0</td><td>LG</td><td>학습 dynamics 기반 data selection으로 incremental임</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2611.27808'>$\mathtt{DistP}$: Scaling Local-Update Training with Zero-Shot Hyperparameter Transfer</a></td><td>30</td><td>0</td><td>LG</td><td>local-update 학습의 하이퍼파라미터 전이로 로봇과 무관함</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2611.27823'>Mixture of Latent Recursions for Low-Rank Adaptation</a></td><td>30</td><td>0</td><td>LG</td><td>LoRA 재귀 mixture로 incremental임</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2611.26881'>Your Judge Inherits Your Prompt: In-Context Label Bias in an LLM-as-Judge Is Directional, Not Symmetric</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM judge의 in-context label bias 분석임. 범위 좁음</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2611.27053'>Isolating the Language Shell: A Content-Controlled Study of Multilingual Reasoning</a></td><td>30</td><td>0</td><td>NLP</td><td>다국어 추론 증류를 통제 비교함. 증분적 분석임</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2611.27211'>Explicit Style Extraction for Personalized Long-Form Text Generation</a></td><td>30</td><td>0</td><td>NLP</td><td>개인화 장문 생성용 스타일 추출임. 증분적임</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2611.27434'>No Audio, No Transcripts, No Problem: LLM-based ASR Adaptation Using Only Domain Documents</a></td><td>30</td><td>0</td><td>NLP</td><td>문서만으로 ASR을 도메인 적응함. 실용적이나 증분적임</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2611.27491'>Alignment without Transfer: Tokenization Impacts Cross-lingual Representations during Multilingual Language Model Pretraining</a></td><td>30</td><td>0</td><td>NLP</td><td>tokenization이 다국어 표현에 미치는 영향 분석임</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2611.27504'>The Assistant Persona Differs Across Languages in Activation Space</a></td><td>30</td><td>0</td><td>NLP</td><td>언어별 assistant persona 활성 방향 차이 분석임</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2611.26663'>Adding One More Agent: How AI Team Size and Formation Shape Productivity and Diversity in Human-AI Brainstorming Teams</a></td><td>30</td><td>0</td><td>AI</td><td>에이전트 팀 규모가 생산성에 미치는 영향을 본 인간 실험임. 로봇 무관함.</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2611.26782'>ChatAtom: A Multi-Agent LLM System for Molecular Dynamics Simulation and Visualization</a></td><td>30</td><td>0</td><td>AI</td><td>분자동역학용 multi-agent LLM 시스템임. 응용 엔지니어링임.</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2611.26870'>Beyond Demographic Discrimination: Benchmarking Normative-Descriptive Calibration in LLMs</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM의 규범/서술 추론 calibration benchmark임. 로봇 무관함.</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2611.26912'>Self-Evolving Beyond Human-Crafted Experience for EDA Scripting</a></td><td>30</td><td>0</td><td>NLP</td><td>EDA 스크립팅용 self-evolving 에이전트임. 로봇 무관함.</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2611.27007'>Scalable Evaluation of Medical AI using Evidence-based Practice Recommendations</a></td><td>30</td><td>0</td><td>NLP</td><td>의료 AI 평가 확장 방법임. 로봇 무관함.</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2611.27016'>Same Facts, Different Decision: Fact-Invariant Manipulation and Provenance-Based Defense in Typed Decision Models</a></td><td>30</td><td>0</td><td>NLP</td><td>typed decision model에 대한 입력 조작과 방어임. 로봇 무관함.</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2611.27018'>Integral Multipliers and Arithmetic Obstructions for Two-Hidden-Layer ReLU Maxima</a></td><td>30</td><td>0</td><td>LG</td><td>ReLU 네트워크 maximum 표현의 정수 이론 결과임. 로봇 무관함.</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2611.27046'>Actions Speak Louder than Words: Stateful Privacy Sniffing of LLM Agents via Behavioral Covert Channels in Web Interactions</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 에이전트의 행동 기반 privacy 유출 탐지임. 로봇 무관함.</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2611.27180'>Learning Adaptive Defense Strategies: Fine-Tuned LLMs for Network Security Games under Network Mobility</a></td><td>30</td><td>0</td><td>LG</td><td>네트워크 보안 게임용 fine-tuned LLM임. 로봇 무관함.</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2611.27186'>What Does Matching a Human Intervention Effect Establish? Benchmark Checks for LLM Simulations</a></td><td>30</td><td>0</td><td>NLP</td><td>LLM 시뮬레이션 검증 benchmark 점검임. 로봇 무관함.</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2611.27196'>EDAGoat: An EDA-Aware Agent for Project-Level GPU Optimization</a></td><td>30</td><td>0</td><td>NLP</td><td>EDA GPU 최적화 coding agent임. 로봇 무관함.</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2611.27283'>DermKG: A Concept-Centric Knowledge Graph for Interpretable Skin Disease Diagnosis from Dermatological Morphology</a></td><td>30</td><td>0</td><td>CV</td><td>피부질환 개념 knowledge graph임. 의료 응용임.</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2611.27390'>Evidence sufficiency assessment enables cost-effective review allocation in on-premise clinical AI agents</a></td><td>30</td><td>0</td><td>NLP</td><td>임상 AI 증거 충분성 평가임. 로봇 무관함.</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2611.27550'>Altair-Nidhogg: Which Model-Merging Theories Hold for a One-Pass Decision Encoder? Soups, Task Arithmetic, TIES and DARE Against Joint Training and Prediction Ensembling</a></td><td>30</td><td>0</td><td>LG</td><td>한 번에 답하는 decision encoder 모델 병합 이론 검증임. 로봇 무관함.</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2611.27712'>When Are Images Needed in Multimodal Machine Translation? Text-Only Routing for On-Demand Visual Context</a></td><td>30</td><td>0</td><td>NLP</td><td>번역 시 이미지 필요 여부를 text로 라우팅함. 로봇 무관함.</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2611.27810'>SLP-Bench: Evaluating and Improving Acoustic Claims of Reasoning Audio Language Models on Clinical Speech</a></td><td>30</td><td>0</td><td>Audio</td><td>임상 음성 ALM의 acoustic claim 평가임. 로봇 무관함.</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2611.27839'>Beyond Self-Critique: Epistemic Convergence Control for Multi-Agent Research Verification</a></td><td>30</td><td>0</td><td>NLP</td><td>다중 에이전트 연구 검증의 수렴 제어임. 로봇 무관함.</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2611.27308'>Frontier Voltage Boost Laplacian Path Planning</a></td><td>28</td><td>3</td><td>Navigation</td><td>Harmonic potential field 경로 계획의 변형임. 고전 방법의 소폭 개선임</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2611.27293'>A Vision-Based Framework for Manual Assembly Verification and Adaptive Operator Assistance</a></td><td>28</td><td>2</td><td>CV</td><td>조립 검증용 vision 프레임워크임. 응용 시스템 성격임</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2611.27097'>UDA-Restoration: Bridging Unsupervised Domain Adaptation and Multi-Degradation Denoising for Enhanced AV Semantic Segmentation</a></td><td>28</td><td>1</td><td>CV</td><td>자율주행 도메인 적응과 복원 결합임. incremental함</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2611.27281'>GAAFormer: Geometry-Anchored Attention Transformer for Joint Point Cloud Denoising and Upsampling</a></td><td>28</td><td>1</td><td>3D Vision</td><td>point cloud denoise와 upsampling transformer임. incremental함</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2611.27913'>Star Panoptic Quality: Selectively Evaluating Split and Merged Instances</a></td><td>28</td><td>1</td><td>CV</td><td>panoptic 평가 지표 변형으로 기여가 작음</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2611.27218'>A Stationarity-Based Regret Framework for Time-Varying Nonconvex Composite Optimization</a></td><td>28</td><td>1</td><td>LG</td><td>시변 비볼록 최적화 regret 이론으로 로봇 연결 약함</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2611.27572'>Minimax-Optimal Small-Loss Regret in Online Convex Optimization and Applications to Contextual Search and Online Inverse Optimization</a></td><td>28</td><td>1</td><td>LG</td><td>OCO regret bound 이론으로 로봇 연결 약함</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2611.26773'>FACET: A Data-Efficient Regional Parametric Head Model</a></td><td>28</td><td>0</td><td>3D Vision</td><td>데이터 효율적 head model임. 로봇 연관 없음</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2611.26936'>SecretAgent: A Multi-Agent Framework for Privacy Protection against Vision Language Models</a></td><td>28</td><td>0</td><td>Multimodal</td><td>VLM 대상 프라이버시 보호 multi-agent임. 로봇 무관함</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2611.27269'>MODULE: A Mutual-Promoting Deep Unfolding Framework Towards Degradation-Robust Multi-modal Image Fusion</a></td><td>28</td><td>0</td><td>CV</td><td>열화에 강한 이미지 융합 unfolding임. 로봇 무관함</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2611.27302'>Can Reasoning and Image Description Enhance Yes/No Visual Mathematical Understanding?</a></td><td>28</td><td>0</td><td>Multimodal</td><td>수학 이미지 yes/no reasoning 평가임. 로봇 무관함</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2611.27630'>Segment Everything, Materialize Nothing: Exact Streaming Inference for Many-Class 3D Segmentation</a></td><td>28</td><td>0</td><td>CV</td><td>many-class 3D segmentation streaming 추론임. 의료 효율화임</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2611.27806'>Refrain: Learning Multi-Shot Consistency from Inconsistent References for A$^2$O Video Generation</a></td><td>28</td><td>0</td><td>Video</td><td>다중 shot 일관성 영상 생성임. 로봇 무관함</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2611.26929'>Large Reported CHB-MIT Adaptation Gains Disappear with Pretrained Encoders and Matched Probes</a></td><td>28</td><td>0</td><td>LG</td><td>EEG 논문의 재현 실패 보고로 로봇과 무관함</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2611.26986'>Distributional Algebro-Geometric Persistence (dAGP): Wasserstein-Stable Polynomial-Relation Signatures</a></td><td>28</td><td>0</td><td>LG</td><td>대수기하 persistence signature 이론으로 로봇과 무관함</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2611.27436'>THRIFTY: Cost-Constrained Reasoning-Data Synthesis for Small Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>SLM 추론 데이터 합성 비용 제약으로 로봇과 무관함</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2611.27889'>Renormalized Entropy from Symmetries: Simplicity Bias and Neural Heat Death</a></td><td>28</td><td>0</td><td>LG</td><td>파라미터 대칭과 simplicity bias 이론으로 로봇과 무관함</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2611.27075'>When Do LLM-Elicited Priors Help? A Controlled Audit of Language Models as Priors for Small-Sample Bayesian Regression</a></td><td>28</td><td>0</td><td>LG</td><td>LLM prior의 베이지안 회귀 효과 감사임. 로봇 무관함</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2611.27156'>Co-Evolving Behavioral Agents and Detectors for Adaptive Information Operations</a></td><td>28</td><td>0</td><td>NLP</td><td>정보 작전 탐지기와 agent 공진화임. 로봇 무관함</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2611.27421'>ORBIT: Offset-based Activation Steering for Cross-lingual Multimodal Fact Verification</a></td><td>28</td><td>0</td><td>NLP</td><td>다국어 fact verification용 activation steering임. 응용 한정임</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2611.27536'>Open CDLM: A Benchmark and Library for Continuous Diffusion Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>continuous diffusion LM benchmark와 라이브러리임. 도구 성격임</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2611.27607'>Tasklets: A Unit-Test Benchmark for Language Model Architectures</a></td><td>28</td><td>0</td><td>LG</td><td>sequence-mixing 구조용 unit-test benchmark임. benchmark 기여임</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2611.27734'>AutoOntologyBench: A Task-Grounded Benchmark for Agentic Knowledge Engineering</a></td><td>28</td><td>0</td><td>NLP</td><td>agentic 지식공학 benchmark임. 로봇 무관함</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2611.27807'>Evaluating Prompting Strategies for Zero-Shot Multilingual Aspect-Based Sentiment Analysis with Large Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>다국어 ABSA prompt 전략 평가임. 단순 평가 연구임.</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2611.26903'>Towards Robust Partial-Edit Deepfake Localization: An edit and Generator Conditioned Analysis</a></td><td>28</td><td>0</td><td>Audio</td><td>음성 deepfake 부분 편집 탐지 분석임. 로봇 무관함.</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2611.26942'>CodeReviewBench: An Automated Benchmark for Evaluating the Software Factory</a></td><td>28</td><td>0</td><td>NLP</td><td>코드 리뷰 benchmark임. 로봇 무관함.</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2611.26988'>From Letter-of-Credit Requirements to Executable Specifications: Evaluating Verification Accuracy and Completeness</a></td><td>28</td><td>0</td><td>NLP</td><td>신용장 요건 검증 평가임. 로봇 무관함.</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2611.27260'>No Perfect Guardrail &amp; No Perfect Guard: On the Decidability of Output Policies for Large Language Models</a></td><td>28</td><td>0</td><td>NLP</td><td>LLM 출력 정책의 결정 불가능성 논증임. 로봇 무관함.</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2611.27483'>From Manufacturing Event Logs to Simulation: Enabling SMEs with Agentic AI for SimPy Simulation Generation</a></td><td>28</td><td>0</td><td>AI</td><td>제조 이벤트 로그에서 SimPy 시뮬레이션을 생성하는 agent임. 응용임.</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2611.27559'>Can Language Models See the Circuit in Pixelated RFIC Passives?</a></td><td>28</td><td>0</td><td>Multimodal</td><td>RFIC 소자 회로 이해 LM 평가임. 로봇 무관함.</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2611.27713'>MetaRigor: From Agentic Automation to Verifiable End-to-End Meta-Analysis Through Scientific Decision Boundaries</a></td><td>28</td><td>0</td><td>NLP</td><td>메타분석 자동화 시스템임. 로봇 무관함.</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2611.27778'>QuASAR: Toward an LLM-Assisted Framework for Screening, Prototyping, and Assessing Quantum-Advantage Opportunities in Scientific Computing</a></td><td>28</td><td>0</td><td>AI</td><td>양자 이점 후보 탐색용 LLM 프레임워크임. 로봇 무관함.</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2611.27835'>Auditable Financial Knowledge Graphs: Schema-Driven Construction and Intrinsic Quality Evaluation</a></td><td>28</td><td>0</td><td>NLP</td><td>재무 knowledge graph 구축임. 로봇 무관함.</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2611.27696'>Comparative Performance of Machine Learning Architectures for Fault Detection and Diagnosis in Chemical Processes</a></td><td>27</td><td>1</td><td>LG</td><td>화학 공정 fault detection 아키텍처 비교임. 단순 비교임.</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2611.26805'>LEAN: Library-Based Adaptation for Asynchronous, Federated Fine-Tuning</a></td><td>27</td><td>0</td><td>LG</td><td>federated LoRA 병합 방법으로 로봇과 무관함</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2611.26968'>Right Numbers, Wrong Story: When LLMs Narrate Financial Changes Beyond Their Inputs</a></td><td>27</td><td>0</td><td>NLP</td><td>LLM 재무 서술의 unsupported framing 분석임. 로봇 무관함.</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2611.27783'>A Benchmark Protocol and Fairness Analysis Towards Open-Set EEG Seizure Type Classification</a></td><td>27</td><td>0</td><td>LG</td><td>EEG 발작 유형 open-set benchmark임. 로봇 무관함.</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2611.26770'>Who Should Verify? Reviewer Selection with Partial Information and Outcome Audits</a></td><td>26</td><td>0</td><td>LG</td><td>AI reviewer 선택 통계 문제로 로봇과 무관함</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2611.27028'>Toward a digital twin of the ICU patient: Forecasting and treatment response in a generative event model</a></td><td>26</td><td>0</td><td>LG</td><td>ICU 환자 digital twin 응용으로 로봇과 무관함</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2611.27109'>Recurrent Amplification and Exact Nonexpansiveness Criteria for Query-Driven Erasure</a></td><td>26</td><td>0</td><td>LG</td><td>linear attention 소거 안정성 이론으로 로봇과 무관함</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2611.27404'>Degradation of Language Models under Controlled Load: Synchronization, Rule Execution and Misfires on the Background</a></td><td>26</td><td>0</td><td>NLP</td><td>LM 부하 증가 시 오류 유형 분석으로 로봇과 무관함</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2611.27487'>Verifying and Strengthening Neural Tangent Kernel Theory</a></td><td>26</td><td>0</td><td>LG</td><td>NTK 이론 증명 보강으로 로봇과 무관함</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2611.27543'>On the Limits of Observability for Evaluating Coverage in Machine Unlearning</a></td><td>26</td><td>0</td><td>LG</td><td>machine unlearning 평가 한계 이론으로 로봇과 무관함</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2611.27618'>Potential emergence in LLM agents: a statistical physics perspective</a></td><td>26</td><td>0</td><td>NLP</td><td>LLM agent 통계물리 해석으로 로봇과 무관함</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2611.27826'>Graph Signal Generation via Graph-Aware Diffusion Models</a></td><td>26</td><td>0</td><td>Generative</td><td>그래프 신호 diffusion 생성으로 로봇과 무관함</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2611.27017'>Real-Time On-Drone Hyperspectral Anomaly Detection for Wilderness Search and Rescue</a></td><td>25</td><td>2</td><td>CV</td><td>드론 hyperspectral 이상 탐지 시스템임. 응용 중심임</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2611.27379'>A Lightweight Method for Validating Simulated LiDAR Configurations Based on Point Density over Distance</a></td><td>25</td><td>2</td><td>Simulation</td><td>시뮬레이션 LiDAR의 point density를 검증하는 경량 방법임. 기여가 작음</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2611.27579'>Adesktop learning factory for smart and resilient manufacturing based on digital twin and AI</a></td><td>25</td><td>2</td><td>Manufacturing</td><td>소형 오픈소스 learning factory 구축 보고임. 연구 novelty 낮음</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2611.26758'>ConRef: Auditing Reference Reliability in 2D/3D Registration Benchmarks</a></td><td>25</td><td>1</td><td>CV</td><td>2D/3D registration benchmark 신뢰도 감사임. 의료 특화임</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2611.27407'>BladeR: Scalable, Shape-Guided 3D Reconstruction of Wind Turbine Blades from UAV Imagery</a></td><td>25</td><td>1</td><td>3D Vision</td><td>풍력 터빈 블레이드 3D 복원임. 응용 특화함</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2611.27412'>Projector Time Map Calibration for Event-based Structured Light</a></td><td>25</td><td>1</td><td>3D Vision</td><td>event 구조광 projector 보정임. 센서 특화임</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2611.26963'>Causal Diffusion for Extreme Super-Resolution in Interactive Games</a></td><td>25</td><td>0</td><td>Generative</td><td>게임 초해상도 diffusion임. 로봇 무관함</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2611.27050'>Towards Text-Mask Consistency in Medical Image Segmentation</a></td><td>25</td><td>0</td><td>CV</td><td>의료 영상 text-mask 일관성임. 응용 특화함</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2611.27170'>FedQCal: Quadratic Programming with Dual-Space Calibration for One-Shot Federated Learning</a></td><td>25</td><td>0</td><td>LG</td><td>one-shot federated learning 보정임. 로봇 무관함</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2611.27208'>Parameter-Efficient Adaptation of Qwen3-VL for Handwritten Mathematical Expression Recognition</a></td><td>25</td><td>0</td><td>Multimodal</td><td>Qwen3-VL 수식 인식 적응임. fine-tuning 위주임</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2611.27352'>PAVE: A Harness for Geometrically Consistent Road Network Modeling with Vision-Language Models</a></td><td>25</td><td>0</td><td>Multimodal</td><td>VLM으로 도로망 모델링임. 로봇 연관 낮음</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2611.27360'>Borrow the Style, Follow the Prompt: Progressive Reference-Guided Stylization</a></td><td>25</td><td>0</td><td>Generative</td><td>reference 기반 stylization임. 로봇 무관함</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2611.27501'>Solar-Conditioned Flow Matching for Multitemporal Aerial Visible-to-Infrared Image Translation</a></td><td>25</td><td>0</td><td>Generative</td><td>항공 가시광-적외선 변환 flow matching임. 로봇 무관함</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2611.27542'>When Visually Rich Documents Meet Multi-Vector Retrieval for Region-level Retrieval-Augmented Generation</a></td><td>25</td><td>0</td><td>Multimodal</td><td>문서 region 검색 RAG임. 로봇 무관함</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2611.27585'>Leakage-Free Is Not Confounder-Free: What a Patient-Level Split Cannot Certify About a Medical Imaging Benchmark</a></td><td>25</td><td>0</td><td>CV</td><td>의료 benchmark confounder 분석임. 로봇 무관함</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2611.27720'>PAWS: A Parametric Model of Canine Pose and Shape</a></td><td>25</td><td>0</td><td>3D Vision</td><td>개 자세 형상 parametric model임. 로봇 무관함</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2611.26671'>On the loss landscape of the linear neural network: beyond critical points</a></td><td>25</td><td>0</td><td>LG</td><td>선형 신경망 loss landscape 이론으로 로봇과 무관함</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2611.26818'>Realistic Robustness Evaluation of Tabular Data Driven Models</a></td><td>25</td><td>0</td><td>LG</td><td>tabular 모델 robustness 평가로 로봇과 무관함</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2611.27065'>COMPASS: Cross-modal Observation with Multi-Path Adaptive Stopping and Selection for Early Time Series Classification</a></td><td>25</td><td>0</td><td>LG</td><td>early time-series classification 방법으로 로봇과 무관함</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2611.27067'>Online Learning for Minimizing Maximum Tardiness in Single-Machine Scheduling</a></td><td>25</td><td>0</td><td>LG</td><td>스케줄링 online learning 이론으로 로봇과 무관함</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2611.26775'>Know Your Context Bank: Repairing Inconsistency and Measuring Generalization in Context-Aware Text-to-SQL</a></td><td>25</td><td>0</td><td>NLP</td><td>text-to-SQL context bank 정리임. 로봇 무관함</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2611.26776'>What Helps Language-Model Agents Review Violent Video? A Controlled Comparison with a Human Evidence Reference</a></td><td>25</td><td>0</td><td>NLP</td><td>폭력 영상 검토용 LLM agent 비교 연구임. 로봇 무관함</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2611.26875'>How Long Will My Language Model Run? A Benchmark for Pre-Execution Runtime Prediction</a></td><td>25</td><td>0</td><td>LG</td><td>학습 job 런타임 예측 benchmark임. 로봇 무관함</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2611.26965'>Beyond Prompt Heuristics: Assessing Child Safety Alignment in LLMs</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM 아동 안전 정렬 평가임. 로봇 무관함</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2611.27652'>Auditing Post-Training Unlearning in Diffusion Language Models using Sparse Autoencoders</a></td><td>25</td><td>0</td><td>NLP</td><td>diffusion LM unlearning 감사임. 로봇 무관함</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2611.27673'>Hy-MT3: More Accurate, Robust and Practical Multilingual Translation Models in the Wild</a></td><td>25</td><td>0</td><td>NLP</td><td>번역 모델 3세대 릴리스임. 엔지니어링임</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2611.27349'>EcomWriteBench: A Real-World Benchmark for E-commerce Writing Tasks</a></td><td>25</td><td>0</td><td>NLP</td><td>전자상거래 글쓰기 benchmark임. 로봇 무관함.</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2611.27463'>Supervaluationism about vagueness and indeterminacy: A judgment-aggregation perspective</a></td><td>25</td><td>0</td><td>AI</td><td>vagueness에 대한 supervaluationism 이론임. 로봇 무관함.</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2611.27899'>The Dual-Tier Sentiment Framework: Scalable Multimodal UX Attribution in Web Search</a></td><td>25</td><td>0</td><td>AI</td><td>웹 검색 UX 감성 프레임워크임. 로봇 무관함.</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2611.26731'>Cross-Attack Robust Aggregation for Federated Learning</a></td><td>24</td><td>0</td><td>LG</td><td>federated learning 강건 집계로 로봇과 무관함</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2611.26940'>CENTRY: A Probabilistic Latent-State Model for Continual AI Risk Estimation, Monitoring, and Regulation</a></td><td>24</td><td>0</td><td>LG</td><td>AI 위험 추정 프레임워크로 로봇과 무관함</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2611.27084'>Auditing and Adapting kNNGuard for Long-Context Prompts</a></td><td>24</td><td>0</td><td>NLP</td><td>LLM guardrail 감사로 로봇과 무관함</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2611.27191'>Lift Out, Kick In: Decoupling Event Effects for Time Series Forecasting</a></td><td>24</td><td>0</td><td>LG</td><td>시계열 이벤트 효과 분리로 로봇과 무관함</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2611.27492'>Learning Unknown Oscillators From Bandit Feedback</a></td><td>24</td><td>0</td><td>LG</td><td>oscillator bandit 이론으로 로봇과 무관함</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2611.27605'>Adapting AI Weather Foundation Models to a Changing Climate</a></td><td>24</td><td>0</td><td>LG</td><td>기후 변화에 대한 weather model continual 적응으로 로봇과 무관함</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2611.27700'>Geometrically Constrained Learning II: Agnostic Proper Learning of Lipschitz Functions</a></td><td>24</td><td>0</td><td>LG</td><td>Lipschitz 함수 학습 이론으로 로봇과 무관함</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2611.27722'>Beyond Math, Code, and Logic: Do Reasoning Models Transfer to Scientific Argumentation?</a></td><td>24</td><td>0</td><td>NLP</td><td>reasoning model의 과학 논증 전이 평가로 로봇과 무관함</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2611.27959'>Ranking-Preserving Coreset Selection for Efficient Evolutionary Hyperparameter Optimization</a></td><td>24</td><td>0</td><td>LG</td><td>HPO coreset 선택으로 로봇과 무관함</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2611.26868'>Effectiveness of Synthetic Defects for Anomaly Detection in Industrial Small Load Carriers</a></td><td>22</td><td>1</td><td>CV</td><td>산업 이상 탐지 합성 결함 효과 분석임. incremental함</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2611.27858'>ENC-QA: A Diagnostic Benchmark for Vision-Language Models on Electronic Navigational Charts</a></td><td>22</td><td>1</td><td>Multimodal</td><td>해도 이해 VLM benchmark임. 응용 특화함</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2611.26712'>Forehead ROI Localization under Real-World Imaging Degradations via Cross-View Pseudo-Labeling</a></td><td>22</td><td>0</td><td>CV</td><td>이마 ROI 위치 추정 응용임. 신규성과 로봇 연관 낮음</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2611.27057'>Learning 3D MRI Representations with Generative Adversarial Networks</a></td><td>22</td><td>0</td><td>CV</td><td>3D MRI GAN 표현 학습임. 로봇 무관함</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2611.27093'>PIU-CR: Physics-Informed Deep Unfolding with SAR-Optical Image Fusion for Cloud Removal</a></td><td>22</td><td>0</td><td>CV</td><td>SAR-광학 구름 제거임. 로봇 무관함</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2611.27183'>GEG-SAM: Gaze Exploration-Guided Segment Anything Model for Weakly Supervised Polyp Segmentation</a></td><td>22</td><td>0</td><td>CV</td><td>시선 기반 polyp segmentation임. 로봇 무관함</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2611.27319'>SAVIOR: Sample-efficient Adaptation of Vision-Language Models for OCR Representation</a></td><td>22</td><td>0</td><td>Multimodal</td><td>OCR 표현의 sample 효율 적응임. 로봇 무관함</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2611.27340'>CoGITAtion: Collaborative Gaze-based Interpretable Task-adaptive Representation for Privacy-sensitive Applications</a></td><td>22</td><td>0</td><td>LG</td><td>시선 기반 개인정보 보호 표현 학습임. 로봇 무관함</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2611.27388'>What Stays in the Picture? From Redundant Instructions to Dependency-Aware Image Editing</a></td><td>22</td><td>0</td><td>Generative</td><td>redundant instruction 이미지 편집임. 로봇 무관함</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2611.27620'>Sketch2TikZ: Multi-Reward Reinforcement Learning for Converting Hand-Drawn Sketches to Executable TikZ</a></td><td>22</td><td>0</td><td>Multimodal</td><td>스케치 TikZ 변환 RL임. 로봇 무관함</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2611.27876'>LesionAgent: Training-Free Agentic Tumor Tracking and Response Assessment in Longitudinal CT</a></td><td>22</td><td>0</td><td>Multimodal</td><td>CT 종양 추적 agent임. 로봇 무관함</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2611.27905'>AnimalFarm: Auditing the Generation and Detection of Hateful Images Featuring Anthropomorphic Characters</a></td><td>22</td><td>0</td><td>CV</td><td>hateful image 감사 연구로 로봇과 무관함</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2611.26828'>Graph-XGB: A Hybrid GNN Framework for Outdoor-to-Indoor 5G Signal Reconstruction via Aerial-Only UAV RF Sensing</a></td><td>22</td><td>0</td><td>LG</td><td>5G 신호 복원 GNN 응용으로 로봇과 무관함</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2611.26847'>A Sparsity Analysis of Traffic Forecasting Architectures: How Much Missing Data is Too Much?</a></td><td>22</td><td>0</td><td>LG</td><td>교통 예측 결측 분석으로 로봇과 무관함</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2611.27043'>Hypergraph Structural Entropy-Enhanced Hierarchy-Aware Semi-Supervised Graph Classification</a></td><td>22</td><td>0</td><td>LG</td><td>그래프 분류 반지도 학습으로 로봇과 무관함</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2611.27058'>Structural Agreement Indicates Prediction Accuracy For Protein-Ligand Co-Folding</a></td><td>22</td><td>0</td><td>LG</td><td>단백질-리간드 co-folding 신뢰도 분석으로 로봇과 무관함</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2611.27143'>GaLF-ST: Gaussian Latent Fields for Spatial Transcriptomics Reconstruction</a></td><td>22</td><td>0</td><td>CV</td><td>spatial transcriptomics 복원으로 로봇과 무관함</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2611.27162'>Hierarchical Hybrid-Coordinate Flow Matching for Accurate and Physically Plausible Apo-to-Holo Protein Generation</a></td><td>22</td><td>0</td><td>LG</td><td>단백질 conformation flow matching으로 로봇과 무관함</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2611.27167'>BusemannFormer: Horospherical Self-Attention for Hyperbolic Graph Transformers</a></td><td>22</td><td>0</td><td>LG</td><td>hyperbolic graph transformer로 로봇과 무관함</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2611.27206'>LingSante-Pulse: Unified Physiological Pretraining through Random-Feature Prediction and Cross-Modal Alignment</a></td><td>22</td><td>0</td><td>LG</td><td>생체신호 pretraining으로 로봇과 무관함</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2611.27511'>Breaking the Barrier of Hard Samples: A Data-Centric Approach to Synthetic Data for Medical Tasks</a></td><td>22</td><td>0</td><td>LG</td><td>의료 합성 데이터로 로봇과 무관함</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2611.27718'>Solving the pre-image problem in kernel PCA: The reproducing property is all you need</a></td><td>22</td><td>0</td><td>LG</td><td>kernel PCA pre-image 문제로 로봇과 무관함</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2611.27831'>DistDNA: Language Model Fingerprinting under Stochastic Decoding</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM fingerprinting으로 로봇과 무관함</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2611.27946'>The Optimal Sample Complexity of Agnostic PAC Learning for Partial Concept Classes</a></td><td>22</td><td>0</td><td>LG</td><td>PAC learning 샘플 복잡도 이론으로 로봇과 무관함</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2611.26833'>Rethinking Full-Weight LoRA with Domain and Task Adapter Scaling for Question Answering over Portuguese Well Drilling Reports</a></td><td>22</td><td>0</td><td>NLP</td><td>포르투갈어 시추 보고서 QA용 LoRA 조정임. 도메인 특화 증분임</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2611.27094'>Separating Automation Gains from Agent Contributions in AI-Assisted Model Validation</a></td><td>22</td><td>0</td><td>NLP</td><td>은행 모델 검증용 agent 평가 분리임. 로봇 무관함</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2611.27301'>Observed, Curated, Reused: Observation Bias in Clinical AI Evaluation</a></td><td>22</td><td>0</td><td>NLP</td><td>임상 AI 평가의 관찰 편향 논의임. 로봇 무관함</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2611.27494'>Typhoon OCR 2: From Thai Document Transcription to Multilingual, Multi-Task OCR</a></td><td>22</td><td>0</td><td>NLP</td><td>Thai OCR 모델 버전업임. 엔지니어링임</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2611.27799'>ChildAI-Gov: An Evidence-Linked AI System for Assessing EdTech Policies Against Children&#x27;s Digital Rights</a></td><td>22</td><td>0</td><td>AI</td><td>EdTech 정책의 아동 권리 평가 시스템임. 로봇 무관함.</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2611.26849'>Scoliosis5K: Multimodal Gait Analysis via Clip-Conditioned RGB-Silhouette Fusion</a></td><td>20</td><td>0</td><td>CV</td><td>척추측만 gait 분석 데이터셋임. 로봇 무관함</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2611.27060'>Rethinking Cross-Sensor Domain Adaptation for Bridge Point Cloud Semantic Segmentation</a></td><td>20</td><td>0</td><td>3D Vision</td><td>교량 point cloud 도메인 적응 재검토임. 응용 특화함</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2611.27198'>DepthMSA: Combinatorial Training and Budget-Aware Depth Allocation for Multimodal Sentiment Analysis</a></td><td>20</td><td>0</td><td>Multimodal</td><td>감정 분석 depth 할당임. 로봇 무관함</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2611.27316'>BioCL-POS: Biological Completer-aware Learning with Predictive Observation Selection - A Wild Ginseng Study</a></td><td>20</td><td>0</td><td>3D Vision</td><td>인삼 point cloud completion임. 응용 특화임</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2611.27415'>Pose-based Co-speech Gesture Detection</a></td><td>20</td><td>0</td><td>CV</td><td>pose 기반 co-speech gesture 검출임. 로봇 무관함</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2611.27490'>Which Dwarf Is This? Doppeldwarf-306 and Near-Identical Instance Retrieval</a></td><td>20</td><td>0</td><td>CV</td><td>난쟁이 조각상 instance retrieval benchmark임. 로봇 무관함</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2611.27512'>PGS-PCQA: Perceptually Gated Synthetic Supervision for No-Reference Point Cloud Quality Assessment</a></td><td>20</td><td>0</td><td>3D Vision</td><td>point cloud 품질 평가임. 로봇 무관함</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2611.27517'>EchoAlign: Echocardiography foundation model with multilevel report alignment</a></td><td>20</td><td>0</td><td>Multimodal</td><td>심초음파 foundation model임. 로봇 무관함</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2611.27521'>PaMuk-Bench: A Parallel Multilingual Multitask Benchmark for Vision-Language Tasks</a></td><td>20</td><td>0</td><td>Multimodal</td><td>다국어 VLM benchmark임. 로봇 무관함</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2611.26914'>Multi-Tier Edge Triage: Optimizing Latency for Safe Clinical Agents</a></td><td>20</td><td>0</td><td>LG</td><td>임상 agent 안전 triage 시스템으로 로봇과 무관함</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2611.26999'>JevRisk: Zero-Shot Financial Risk Assessment with a Language Decision Model</a></td><td>20</td><td>0</td><td>NLP</td><td>금융 위험 평가 응용으로 로봇과 무관함</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2611.27015'>Ruby: State-of-the-Art Potency Prediction across Discovery Regimes Using Learned Structural Representations</a></td><td>20</td><td>0</td><td>LG</td><td>약물 potency 예측으로 로봇과 무관함</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2611.27114'>Federated and Balanced $k$-means: Communication Efficiency, Privacy, and Heterogeneity</a></td><td>20</td><td>0</td><td>LG</td><td>federated k-means로 로봇과 무관함</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2611.27141'>Dynamic Memory-enhanced Pattern Relevance Prediction for Long-tailed Graph Classification</a></td><td>20</td><td>0</td><td>LG</td><td>long-tailed 그래프 분류로 로봇과 무관함</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2611.27609'>Quantum-Informed Regularized Poisson Learning for Graph-Based Semi-Supervised Classification</a></td><td>20</td><td>0</td><td>LG</td><td>quantum-informed 그래프 반지도 학습으로 로봇과 무관함</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2611.26837'>Cross-Linguistic Distinctive-Feature Constraints on Segmental Triphones: Evidence for Contrastive Dispersion</a></td><td>20</td><td>0</td><td>NLP</td><td>음소 triphone 언어학 분석임. 로봇 무관함</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2611.26900'>Modeling Attributional Style at Scale: A Dataset and Analysis for Psychological Attribution Assessment and Reframing</a></td><td>20</td><td>0</td><td>NLP</td><td>귀인 양식 dataset임. 로봇 무관함</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2611.27544'>Alliance Rupture and Repair in Simulating Cognitive Behavioral Therapy Dialogues</a></td><td>20</td><td>0</td><td>NLP</td><td>CBT 대화 시뮬레이션의 관계 파열 모델링임. 로봇 무관함</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2611.26810'>Acoustic Markers of Engagement in Children with Autism Spectrum Disorder and Their Caregivers</a></td><td>18</td><td>1</td><td>LG</td><td>자폐 아동 음향 참여도 분석으로 로봇 연결 약함</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2611.27469'>PathOPEN: A pathologist-curated histopathology dataset for visual question answering</a></td><td>18</td><td>0</td><td>Multimodal</td><td>병리 VQA dataset임. 로봇 무관함</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2611.27624'>Points, Not Pixels: Keypoints, Masks and Oblique Geometry for Floating-Roof Tank Fill Estimation from Overhead Imagery</a></td><td>18</td><td>0</td><td>CV</td><td>저장 탱크 충전량 추정임. 응용 특화함</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2611.27674'>CanopyFormer: Attention-Guided SegFormer for Explainable Forest Cover Segmentation</a></td><td>18</td><td>0</td><td>CV</td><td>산림 분할 attention 지도임. 응용 특화함</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2611.27753'>SUPERVISE: A Unified Framework for Standardized and Reproducible Superpixel Evaluation</a></td><td>18</td><td>0</td><td>CV</td><td>superpixel 평가 프레임워크임. 로봇 무관함</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2611.27796'>$\varepsilon$-SegFormer: Multi-Resolution Vision Transformers for Sparsely Supervised Segmentation in Electron Microscopy</a></td><td>18</td><td>0</td><td>CV</td><td>전자현미경 sparse 분할임. 로봇 무관함</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2611.27862'>OpenAHBU: Open-sourced Automatic Human Behaviour Understanding Toolkit Through Facial Behaviour Analysis</a></td><td>18</td><td>0</td><td>CV</td><td>얼굴 행동 분석 toolkit임. 로봇 무관함</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2611.27881'>Interpretable Tissue Architecture Complements Pathology Foundation Models</a></td><td>18</td><td>0</td><td>CV</td><td>병리 조직 구조 보완임. 로봇 무관함</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2611.27009'>Fair Property Tax: Reducing Regressivity in Machine-Learning Valuation</a></td><td>18</td><td>0</td><td>LG</td><td>부동산 세금 valuation 공정성으로 로봇과 무관함</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2611.27661'>SMSD: A Semantic Misinformation Spreader Detection Approach</a></td><td>18</td><td>0</td><td>NLP</td><td>misinformation spreader 탐지로 로봇과 무관함</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2611.27894'>FairITR: Fairness-Aware Learning of Multicategory Individualized Treatment Rules</a></td><td>18</td><td>0</td><td>LG</td><td>치료 규칙 공정성으로 로봇과 무관함</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2611.27059'>NightmareDiscourseBench: A Benchmark Dataset for Fictional Direct Discourse Identification Pipelines</a></td><td>18</td><td>0</td><td>NLP</td><td>소설 직접화법 benchmark임. 기여 작음</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2611.27137'>Cross-Platform Production Signatures of State-Linked Information Operations</a></td><td>18</td><td>0</td><td>NLP</td><td>정보 작전의 플랫폼 간 signature 분석임. 로봇 무관함</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2611.27506'>How Many Bytes Has a BPE Model Seen? Estimating Byte-Token Exposure in Pretraining from Corpus Statistics and Embedding Norms</a></td><td>18</td><td>0</td><td>NLP</td><td>BPE byte 토큰 노출량 추정임. 로봇 무관함</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2611.27721'>Decision Models for Multilingual Emotion Classification: A Comparative Study Against LLMs and Encoders</a></td><td>18</td><td>0</td><td>NLP</td><td>다국어 감정 분류 모델 비교임. 로봇 무관함</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2611.27868'>Integrating Generative Artificial Intelligence with Learning Style Models: Opportunities, Challenges, and Future Directions</a></td><td>18</td><td>0</td><td>AI</td><td>생성 AI와 학습 스타일 리뷰임. 로봇 무관함.</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2611.27726'>A Switching Mechanism for Selecting Environment-Adaptive Personalized Gains in Hearing Aids</a></td><td>16</td><td>0</td><td>LG</td><td>보청기 gain 전환 기법으로 로봇과 무관함</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2611.27970'>On the Complete Feature Set for ADHD Classification in Children and Adolescents Based on EEG Signals</a></td><td>16</td><td>0</td><td>LG</td><td>ADHD EEG 특징 분류로 로봇과 무관함</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2611.27241'>WINSO: A Large-Size Very-High-Resolution Remote Sensing Dataset for Wind Turbine Detection and Solar Panel Segmentation</a></td><td>15</td><td>0</td><td>CV</td><td>풍력 태양광 원격탐사 dataset임. 로봇 무관함</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2611.27465'>Cecilia: Towards Layout-Inclusive Optical Music Recognition</a></td><td>15</td><td>0</td><td>CV</td><td>악보 인식 layout임. 로봇 무관함</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2611.27621'>Automating Multi-View Quality Assessment of 3D Annotation Layouts</a></td><td>15</td><td>0</td><td>CV</td><td>3D 주석 layout 품질 평가임. 로봇 무관함</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2611.27728'>Quantitative Measurement of Pavement Distress based on Vehicle Camera and Perspective Correction</a></td><td>15</td><td>0</td><td>CV</td><td>도로 균열 정량 측정임. 응용 특화함</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2611.27854'>DGC-Net: A Depth-Geometric Conditioning Network for Projection-Supervised OCTA Segmentation</a></td><td>15</td><td>0</td><td>CV</td><td>OCTA 분할임. 로봇 무관함</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2611.27192'>How Much of a Calculation-Error Rate Is Not Arithmetic: Auditing the FinReason Cup 2026 Task 3 Metric with a Deterministic Rule System</a></td><td>15</td><td>0</td><td>NLP</td><td>FinReason Cup 지표 감사 보고임. 기여 작음</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2611.27273'>Do Companies Deliver on Their IPO Claims?</a></td><td>15</td><td>0</td><td>NLP</td><td>IPO 주장 이행 benchmark임. 로봇 무관함</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2611.27978'>A Methodologically Rigorous Benchmark of Linear Regression,RNN, and LSTM for S&amp;P 500 Forecasting:Identifying Sources of Performance Inflation in Financial DeepLearning</a></td><td>14</td><td>0</td><td>LG</td><td>주가 예측 벤치마크로 로봇과 무관함</td></tr>
</tbody></table>

</details>
