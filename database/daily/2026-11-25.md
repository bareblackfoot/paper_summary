# 오늘의 arXiv Top 15: 2026-11-25 (수)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**

**신규 논문 수: 전체 675편 → 중복 제거 후 675편 (이번 평가 대상 675편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 264 |
| cs.LG | 144 |
| cs.RO | 91 |
| cs.CL | 74 |
| cs.AI | 102 |

---

## Top 15

### 1. Any2Act: Scaling In-Context Robot Learning from Heterogeneous Demonstrations (85점)

[arXiv](https://arxiv.org/abs/2611.32353) · [PDF](https://arxiv.org/pdf/2611.32353) · [alphaXiv](https://www.alphaxiv.org/abs/2611.32353) · [프로젝트 페이지](https://any2act.github.io)

- **저자**: Ziang Ren, Zifan Wang, Zhuoyang Li, Benhao Qin, Haoyang Li, Qingtao Liu, Xuchuan Chen, Zekun Qi 외 3명
- **분야**: Embodied AI · robotics relevance 10/10 · 1차 스크리닝 78점
- **읽은 원문**: PDF 전문

> 사람 영상, 시뮬레이션, UMI, 다른 로봇의 demonstration을 모두 실행 로봇의 카메라 배치와 action space로 옮겨 하나의 in-context policy가 따라 하게 함. 학습에 없던 실로봇 과제 6개를 demonstration 1개만 보고 fine-tuning 없이 평균 57.5% 성공함.

**무슨 문제인가**

Robot in-context learning(ICL)은 policy가 demonstration을 보고 fine-tuning 없이 새 과제를 수행하는 설정임. 사람 영상을 조건으로 받는 기존 방법은 같은 과제를 사람과 로봇이 함께 수행한 짝 데이터가 필요하고, 이런 짝은 몇천 개 수준으로 적음. 로봇 demonstration을 조건으로 받는 방법은 짝 문제는 없지만 합성 데이터나 benchmark 규모로만 학습되어 따라 할 수 있는 과제 범위가 좁음. 또 기존 방법마다 받을 수 있는 demonstration 종류가 한두 가지뿐이라, 새 종류를 받으려면 큰 짝 데이터와 재학습이 다시 필요함.

**어떻게 푸나**

Any2Act는 과제를 수행하는 로봇을 executor, demonstration을 제공한 쪽을 demonstrator로 나눔. 모든 demonstration은 executor의 머리 카메라 1개와 손목 카메라 2개, executor의 팔과 이동 base action으로 바꿔 표현함(embodiment-grounded representation). 따라 하는 능력은 executor 자신의 teleoperation 기록으로만 배움. 같은 과제를 다른 장면에서 두 번 기록한 것을 demonstration과 실행의 짝으로 쓰며, 1.2M 궤적(10,000시간, 과제 10,000개)에서 짝을 만듦. 새 출처는 변환 파이프라인으로 이 형식에 맞춤. 사람 영상은 ego2sim(손과 물체 자세를 추정해 시뮬레이터에서 executor로 다시 실행하는 파이프라인)으로 변환함. UMI(손에 드는 gripper로 기록하는 장치)와 다른 로봇 데이터는 이미 머리 시점 1개와 손목 시점 2개를 담고 있어, action만 executor 공간으로 옮김. 변환 후 남는 외형과 동작 차이는 source-routed adapter(SRA: 출처마다 하나씩 두고 그 출처의 demonstration token에만 켜지는 LoRA)가 흡수하며, 본 모델은 고정함. 긴 과제에서는 DINOv3 특징으로 현재 관측과 가장 비슷한 demonstration 시점을 학습 없이 단조 정렬로 찾고, 그 주변 구간만 입력함. 실패로 장면이 이전 단계와 비슷해지면 이 구간을 앞으로 되돌려(rollback) 실패한 단계를 다시 수행함. 모델은 Cosmos-Predict2 영상 모델 위에 action expert를 붙인 world action model이며, 출력은 2초 길이의 action chunk와 미래 프레임임.

**결과**

- 실로봇 Task Generalization(사전학습 skill을 새 순서와 물체 조합으로 엮은 처음 보는 과제 6개)에서 Any2Act는 fine-tuning 없이 평균 57.5% 성공함. 과제당 50개 demonstration으로 fine-tuning한 GR00T N1.7은 47.5%, π0.5는 43.0%임.
- 같은 로봇 짝 데이터로 다시 학습한 기존 in-context policy인 HOST와 Zero-WAM은 같은 benchmark에서 15.7%와 19.7%에 그침. 사전학습 데이터를 400시간에서 10,000시간으로 늘리면 이 benchmark 평균이 13.3%에서 57.5%로 오름.
- 출처별 SRA를 200쌍으로 학습한 뒤 실로봇 12개 과제 평균 성공률은 시뮬레이션 59.1%, 사람 영상 57.9%, UMI 55.1%, 다른 로봇 2종 51.0%와 48.2%임. executor 자신의 demonstration을 쓸 때의 65.1% 대비 74~91% 수준이며, SRA가 없으면 다른 로봇 출처는 1.5% 이하임.
- 같은 200쌍으로 모델 전체를 fine-tuning하면 처음 보는 과제에서 사람 영상 9.3%, UMI 13.5%로 내려감. SRA는 같은 조건에서 49.3%와 46.3%를 유지함. 10,000시간 모델에서 rollback을 끄면 실로봇 12개 과제 전체 평균이 65.1%에서 54.1%로 내림.

**한계**

모든 실로봇 평가는 저자 소속 회사의 Galbot G1 한 기종을 executor로 쓰며, 다른 executor는 RoboTwin 2.0(시뮬레이션 양팔 조작 benchmark)에서만 확인함. 사전학습에 없던 skill을 요구하는 Skill Extension 과제에서는 in-context policy도 과제당 20개 demonstration으로 먼저 적응시켜야 하므로, demonstration 하나만으로 사전학습에 없던 skill을 배우지는 못함. 1.2M 궤적 데이터와 코드 공개 여부는 본문에서 확인 불가하며, 힘과 촉각이 필요한 접촉 과제는 표현에 담지 못함.

**누리랩 연구와의 연결**

- DINOv3 특징으로 demonstration 진행 시점을 학습 없이 맞추고, 실패하면 demonstration 구간을 이전 단계로 되돌려 다시 시도하게 함. 이 구조는 failure detection과 recovery를 별도 데이터 없이 world action model에 붙이는 사례로 비교 대상이 됨.
- 출처별 adapter만 바꿔 사람 영상과 다른 로봇 demonstration을 받는 방식은 VLA에 새 데이터 출처를 붙일 때 본 모델을 고정한 채 적응하는 설계로 참고할 수 있음.

*대표 그림: 측정 결과가 아니라 데이터 구성과 출처 변환 구조를 그린 그림임. 위쪽은 teleoperation 기록을 VLM으로 거르고 같은 과제끼리 짝지은 사전학습 데이터(1.2M 궤적, 10,000시간)와 과제 종류 비율을, 아래쪽은 UMI, ego2sim, 다른 로봇 데이터가 각각 변환된 뒤 출처별 SRA로 들어가는 과정을 보여 줌.*

---

### 2. RetraQ: Manifold-Constrained Critic Guidance for Flow Policies in RL (82점)

[arXiv](https://arxiv.org/abs/2611.32148) · [PDF](https://arxiv.org/pdf/2611.32148) · [alphaXiv](https://www.alphaxiv.org/abs/2611.32148) · [프로젝트 페이지](https://2027ICLR.github.io/retraq/)

- **저자**: Xuanzhuo Liu, Wu Chen, Ruixiang Wu, Shuai Yuan, Chuankang Li, Tongxin Li, Maoqing Yao, Guanghui Ren
- **분야**: RL · robotics relevance 10/10 · 1차 스크리닝 83점
- **읽은 원문**: PDF 전문

> critic gradient를 따라 flow policy의 action을 고칠 때, 고정된 BC flow의 denoising map으로 gradient의 방향을 거르고 결과 action을 데이터 근처로 되돌리는 RetraQ를 제안함. 실로봇 플러그 꽂기에서 π0.5 BC policy의 성공률을 파라미터 수정 없이 55.0%에서 76.7%로, online 학습 1시간 뒤 100%로 올림.

**무슨 문제인가**

학습된 critic Q의 action gradient를 따라 pretrained flow policy의 action을 고치는 방식은 RL로 BC policy를 개선하는 흔한 방법임. 그런데 행동 데이터가 action 공간의 저차원 manifold 위에 있다면, critic 값은 manifold 위에서만 데이터로 맞춰짐. manifold 위에서 값이 같은 두 critic도 manifold에 수직인 gradient 성분은 마음대로 다를 수 있음. 이 수직 성분을 따라가면 action이 데이터 밖으로 나가고, 거기서 높게 예측된 값은 실제 개선이 아니라 critic의 외삽 오차일 수 있음. 방향만 걸러도 manifold가 휘어 있으면 유한한 step은 manifold를 벗어나므로, 방향과 도착점을 함께 제약해야 함.

**어떻게 푸나**

RetraQ(Retraction-based Q-guidance)는 이상적인 갱신을 manifold 위 Riemannian gradient ascent로 봄. 여기에 필요한 tangent projection과 retraction(벗어난 점을 manifold 위로 되돌리는 연산)을 pretrained flow로 근사함. flow의 noise 수준을 나타내는 시점 tg(guidance level)를 0.9로 고정함. 이 시점에서 고정된 BC flow의 velocity를 한 번 계산해, noisy action을 clean action 추정으로 보내는 denoising map R을 정의함. 저자는 이론상 R이 manifold로의 nearest-point projection을, R의 Jacobian JR이 tangent projection을 근사함을 보임. 갱신은 세 단계임: critic gradient g를 구하고, JR·g로 수직 성분을 줄이고, a+ηJR·g에 R을 적용해 되돌림. JR·g는 Jacobian-vector product 한 번이라 sampling chain 전체를 역전파하지 않음. 입력은 context와 policy가 낸 action chunk, 출력은 고친 action이며, 이것을 바로 실행하거나 stop-gradient target으로 써서 BC anchor가 붙은 flow-matching loss로 actor에 distill함. 실로봇 test-time guidance에 쓰는 critic은 forked rollout으로 학습함. 과제상 중요한 몇 지점(fork state)에서 같은 앞부분을 재생하고 그 지점의 action chunk만 바꾼 뒤, 나머지는 고정 policy가 끝내게 함.

**결과**

- 실로봇 test-time guidance: AgiBot G02 양팔 로봇의 휴대폰 충전 플러그 꽂기에서 π0.5 BC policy의 성공률이 60회 시행 기준 55.0%에서 76.7%로 오름. BC 대비 차이는 Fisher 검정 p=0.02임. FlowDPG는 one-step clean action 추정에서 critic gradient를 따라 올린 action으로 velocity를 회귀하는 방법임. action을 옮기는 step 크기를 RetraQ와 같게 맞춘 baseline 중 가장 높은 FlowDPG는 63.3%이고, RetraQ와의 차이는 p≥0.16으로 유의하지 않음.
- 실로봇 offline-to-online: 같은 BC policy와 IQL critic에서 시작해 30분 뒤 98.3%, 1시간 뒤 100%에 이름. 값은 학습 3회의 평균이고 각 시점마다 60회씩 평가함. 비교 방법 중 최고는 Q-VGM(FlowDPG처럼 회귀하되 여러 번 올린 뒤 Q가 가장 높은 action을 고르는 방법)의 95.0%(30분)와 93.3%(1시간)임. policy 가중치는 두고 입력 noise를 RL로 고르는 DSRL은 86.7%와 93.3%임.
- LIBERO(시뮬레이션 조작 과제 모음) online 학습: 최종 성공률이 Spatial 중 BC 성공률이 가장 낮은 6과제 63.3%에서 78.1%, Goal 10과제 69.0%에서 81.3%, Object 10과제 55.3%에서 66.4%로 오름. 각 suite의 가장 강한 baseline보다 5.5에서 7.8퍼센트포인트 높음.
- 요소 분리: 이득의 대부분은 retraction에서 나옴. 방향만 거르는 filter-only는 RetraQ보다 8.6에서 14.6퍼센트포인트 낮고, retraction만 쓰는 Raw+R에 filter를 더하면 1.9에서 4.3퍼센트포인트가 오르나 3 seed 편차 안에 있음.

**한계**

action 차원이 커지면 학습된 filter가 약해져, 512차원 제어 실험에서는 수직 성분이 거의 걸러지지 않음. 이때 normal gain(1이면 거르지 않음)은 0.84에서 0.97임. 새 상호작용 없이 offline distillation을 반복하면 LIBERO에서 RetraQ 성능이 AWR이나 FlowDPG보다 더 크게 내려감. 고치는 범위도 고정된 BC flow가 덮는 영역 안으로 묶임. 실로봇은 과제 1개뿐임. retraction만 쓰는 Raw+R도 실로봇 test-time에서 73.3%에 이름. 코드는 공개 예정으로만 적힘.

**누리랩 연구와의 연결**

- π0.5 같은 flow 기반 VLA를 critic으로 test-time에 고치거나 짧은 online RL로 개선하는 연구에서 바로 비교 대상이 됨. BC policy 자체를 데이터 manifold의 기하 정보로 써서 critic 외삽 오차를 막는 방식은 test-time optimization에 그대로 옮길 수 있음.
- 실패가 잦은 결정적 지점(fork state)에서만 action을 바꿔 다시 굴려 critic을 학습하는 forked rollout은, failure detection 뒤 recovery action을 고르는 문제와 이어짐.

*대표 그림: 왼쪽은 raw critic ascent가 action을 manifold 밖 높은 예측값 쪽으로 보내는 반면, RetraQ는 JR로 걸러 한 걸음 간 뒤 R로 manifold 위로 되돌리는 과정을 그린 개념도이고, 가운데는 π0.5 policy에 붙인 방법 구조도임. 오른쪽은 실로봇 플러그 꽂기 성공률 막대로 BC 55.0%, test-time guidance 76.7%, online 30분 98.3%, 1시간 100.0%를 보임.*

---

### 3. OmniAct: One Policy, One Million Embodiments (82점)

[arXiv](https://arxiv.org/abs/2611.33158) · [PDF](https://arxiv.org/pdf/2611.33158) · [alphaXiv](https://www.alphaxiv.org/abs/2611.33158) · [프로젝트 페이지](https://omniact.github.io/)

- **저자**: Xiang Fan, Yuheng Wang, Jiayuan Yan, Bohan Fang, Wisdom Oluchi Ikezogwo, Ainaz Eftekhar, Max Argus, Jason Ren 외 2명
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 76점
- **읽은 원문**: PDF 전문

> 로봇 팔의 관절 구조를 카메라 좌표계의 kinematic graph로 넣고, 절차적으로 생성한 팔 약 80만 개의 시뮬레이션 궤적으로 단일 manipulation policy를 학습함. 학습에 없던 팔과 장면 2,000 episode에서 성공률 63.0%로, 가장 강한 baseline 57.9%와 π0.5 17.8%보다 높음.

**무슨 문제인가**

여러 로봇을 하나로 다루는 기존 VLA는 end-effector 명령이나 공통 action token처럼 로봇 사이에 공유되는 표현으로 과제 지식을 옮김. 그러나 목표가 같아도 관절 배치, 작업 반경, 자유도가 다르면 잡는 방향과 궤적이 달라져야 함. URDF나 kinematic graph를 입력으로 넣는 기존 방법은 로봇을 장면과 따로 인코딩했고, 몇 안 되는 팔 사이의 전이만 보였음. 수백 가지 형태로 학습을 늘린 연구도 주로 locomotion이었고 manipulation에서는 드물었음.

**어떻게 푸나**

OmniAct는 로봇을 관절, gripper 끝점, TCP(tool center point)를 node로 하는 그래프로 나눔. 각 node는 forward kinematics와 카메라 extrinsic으로 구한 카메라 좌표계의 3D 위치, 운동축, 6D 자세와 관절 종류, 정규화된 관절값을 담음. 이를 scene-grounded kinematic graph라 부르며, node 토큰은 같은 카메라의 이미지 토큰과 view embedding을 공유해 몸과 장면의 관계를 attention으로 배우게 함. node 사이 최단 경로 거리는 Transformer attention bias로 들어감. 입력은 다시점 RGB(SigLIP 2), 언어 지시(Qwen2.5-VL 텍스트 부분), node 토큰이고 출력은 31 step action chunk임. node는 고정된 12개 slot에 채워 넣고, 출력도 입력과 같은 slot 순서를 따르며, node마다 상대 관절 변화량과 end-effector 자세 변화를 flow matching으로 함께 예측함. 그래서 6~8 자유도 팔을 한 network로 다룸. 학습 데이터는 random seed로 팔 형태, 관절 한계, 동역학을 만들고 자기충돌과 IK 기반 파지 가능성 검사를 통과한 팔만 남김. 남은 팔을 MolmoSpaces(실내 장면 조작 시뮬레이션 환경)에 넣고 planner로 궤적을 만들어 성공한 것만 모음. 이렇게 만든 OmniAct-1M은 팔 800,196개의 궤적 1,029,605개이고, 모델 크기는 400M parameter임.

**결과**

- OmniAct-Bench(학습에서 뺀 팔과 장면이 함께 나오는 시뮬레이션 평가 모음) 2,000 episode, 500 step 제한에서 성공률이 63.0%임. embodiment 일반화용 기존 policy인 UMI(Universal Manipulation Interface)를 같은 데이터와 3시점 카메라로 학습한 UMI(all views)는 57.9%, π0.5-DROID는 17.8%임. 5 step마다 다시 계획하는 GPT-6 Astra와 둘 다 평가한 과제 종류만 보면 64.7% 대 41.1%이고, GPT-6 Astra에 1,000 step을 줘도 54.8%임.
- MolmoSpaces 평가(Franka Panda DROID 설정, 2,622 episode)에서 Franka를 학습에서 본 적 없는 OmniAct가 69.1%임. Franka로 학습한 MolmoBot은 63.0%, MolmoAct2-DROID는 22.5%임.
- 실로봇 pick-and-place를 fine-tuning 없이 로봇당 20회 수행함. Franka에서는 14/20으로 MolmoAct2-DROID와 같고 DreamZero 15/20보다 1회 적음. 학습 분포 가장자리에 있고 처음 보는 fine-tip gripper를 단 OpenYAM 팔에서는 13/20임. YAM으로 학습한 MolmoAct2-BimanualYAM은 7/20, UMI(all views)는 0/20임.
- 학습 팔 수를 1/8(10만 개)로 줄이면 500 step 성공률이 26.8퍼센트포인트 내려감. kinematic graph 토큰을 빼면 5.1퍼센트포인트 내려감.

**한계**

시뮬레이션에서 kinematic graph의 기여는 5.1퍼센트포인트로 작고, 큰 차이는 팔 수와 다시점 카메라에서 나옴. graph가 분포 가장자리 팔에서 크게 기여한다는 주장은 실로봇 OpenYAM 한 대의 pick-and-place 20회 결과에 기댐. 단팔 gripper와 pick, place, open, close 과제만 다루고 bimanual 팔이나 dexterous hand는 보이지 않음. 카메라 extrinsic과 정확한 kinematic model을 안다고 가정하며, 코드 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- 로봇 형태 정보를 action 공간이 아니라 카메라 좌표계 토큰으로 VLA에 주는 방식임. 여러 팔을 쓰는 VLA 실험에서 embodiment conditioning의 비교 대상으로 쓸 수 있음.
- 같은 과제에서도 팔의 작업 반경에 따라 위에서 잡기와 옆에서 잡기를 바꾸는 관찰이 있음. manipulation 실패를 작업 반경, 관절 한계 같은 몸 제약 탓으로 나누어 진단하는 failure detection 연구에 참고가 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 다시점 관측 위에 카메라별 관절 node와 운동축을 그린 kinematic graph를 보여 줌. 이를 시각·언어·proprioception 토큰과 함께 받는 Diffusion Transformer와, node별 관절 action과 end-effector 자세(EE pose) 출력도 그려져 있음.*

---

### 4. FoveaWAM: Role-Aware 4D World-Action Modeling for Dynamic Manipulation (82점)

[arXiv](https://arxiv.org/abs/2611.31705) · [PDF](https://arxiv.org/pdf/2611.31705) · [alphaXiv](https://www.alphaxiv.org/abs/2611.31705) · [프로젝트 페이지](https://foveawam.github.io/)

- **저자**: Jiaqi Yin, Baoyue Zhang, Jiyuan Zhang, Wenxuan Liu, Zhaofei Yu, Yue Deng, Tiejun Huang
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 74점
- **읽은 원문**: PDF 전문

> 움직이는 물체를 다루는 policy가 무엇을 얼마나 정밀하게 예측할지를 물체의 역할별로 나눈 4D world-action model을 제안함. 추론 중에도 장면이 계속 움직이는 새 benchmark에서 성공률 82.1%로 가장 강한 baseline PUMA(61.4%)보다 20.8퍼센트포인트 높고, p95 추론 지연은 15.1 ms임.

**무슨 문제인가**

움직이는 물체를 잡으려면 policy가 관측 시점이 아니라 행동이 실행되는 시점의 장면을 예측해야 함. 그런데 예측에 시간을 쓸수록 그 시점은 더 멀어짐. 0.9 m/s로 미끄러지는 물체는 200 ms 추론 동안 18 cm를 이동함. 영상 world-action model(WAM: 미래 영상과 행동을 함께 예측하는 policy)처럼 장면 전체를 예측하면 계산이 비싸고 target의 자세는 픽셀 속에 암묵적으로만 남음. 반대로 target만 예측하면 접근 경로를 막거나 target을 미는 주변 물체를 놓침. 또 기존 dynamic manipulation benchmark인 DOMINO는 추론 중에 시뮬레이션을 멈춰서 느린 policy가 지연 비용 없이 평가됨.

**어떻게 푸나**

FoveaWAM은 장면을 접촉 대상인 target, target을 막거나 움직이는 context, 나머지 static 부분의 세 역할로 나눔. 입력은 현재 RGB-D 한 장, target의 최근 350 ms SE(3) 자세 이력 8개, 로봇 end-effector 상태 이력 8개임. RGB는 고정된 MAE ViT-B/16으로 patch token 196개가 되고, 각 patch는 depth로 얻은 base frame 3D 좌표로 위치가 매겨짐. 자세 이력은 이동량·회전·속도·가속도를 물리 단위로 담은 token 8개로 들어감. 여기에 end-effector 상태 token 8개를 더해, 이미지 이력 대신 저차원 token 16개로 움직임을 표현함. 학습 때 world stream은 미래 400 ms까지 8개 시점에 대해 target의 SE(3) 궤적은 정밀하게, 장면 전체는 patch 단위 sparse 3D flow로 거칠게 예측하도록 선형 decoder로 감독받음. action stream은 같은 attention을 공유하며 flow matching으로 8개 명령 chunk를 생성함. 추론 때는 예측 decoder를 끄고 world stream을 한 번만 돌려 key/value를 캐시한 뒤 action stream이 Euler 5 step으로 행동을 냄. 저자들은 함께 OnTimeBench(14개 dynamic 조작 과제에서 각 policy의 실제 추론 지연만큼 물리를 진행시키며 평가하는 MuJoCo benchmark)를 만듦.

**결과**

- OnTimeBench 실제 지연(Native) 조건 14개 과제 평균 성공률이 82.1%로, target의 미래 feature를 감독받는 dynamic VLA인 PUMA 61.4%, π0.5 54.4%, 영상 WAM OpenWAM-α 46.1%보다 높음. p95 time-to-action은 15.1 ms로 OpenWAM-α의 151.7 ms의 약 10분의 1임.
- 같은 SE(3) 자세 이력을 입력으로 넣은 π0.5+SE(3)와 비교하면, 시뮬레이션을 멈춘 Paused 조건에서도 90.3% 대 76.0%로 14.3퍼센트포인트 앞섬. Native에서는 차이가 23.4퍼센트포인트로 벌어짐.
- 추론 중 물리를 멈추는 DOMINO 단일 팔 과제 24개에서 성공률 46.8%로 가장 강한 baseline인 dynamic WAM DynamicWAM 26.9%보다 19.9퍼센트포인트 높음. 다만 단일 접촉 과제 8개(Intercept)에서는 PUMA가 36.3% 대 29.4%로 앞섬.
- 실제 Flexiv 로봇의 dynamic 과제 6개(과제당 20회)에서 평균 성공률이 48.3%로 π0.5 30.8%, ACT 1.7%보다 높음. 비교 대상은 이 두 방법뿐임.

**한계**

시뮬레이션에서 FoveaWAM은 simulator가 주는 정답 target 자세를 입력으로 받고, 실로봇에서는 FoundationPose 기반 추적기에 기댐. 그래서 target이 강체이고 자세를 실시간 추적할 수 있다는 가정이 필요하며, 관절체나 변형체는 다루지 않음. OnTimeBench는 저자들이 만든 benchmark이고, 실로봇 평가는 과제 6개에 baseline 2개이며 가장 어려운 과제의 성공은 20회 중 2회임.

**누리랩 연구와의 연결**

- 추론 시간이 행동 시점을 바꾸는 문제를 world model 설계와 평가 양쪽에서 다룬 사례임. 실시간 VLA나 test-time planning 연구에서 지연을 포함해 평가하는 기준으로 OnTimeBench 방식을 쓸 수 있음.
- target은 SE(3) 궤적, 주변은 sparse 3D flow로 나누는 표현은 object-centric 3D/4D 표현을 manipulation world model에 넣는 구체적 설계임. 예측 head를 배포 때 꺼도 미래 감독이 성능을 올린다는 ablation은 world model을 표현 학습 보조로 쓰는 근거가 됨.

*대표 그림: 측정 결과가 아니라 무엇을 예측하는지를 비교한 개념도임. 장면 전체 예측(a), target 궤적만 예측(b)과 달리 FoveaWAM(c)은 target의 SE(3) 궤적(빨간 윤곽)과 격자점 위 sparse 3D flow 화살표(0~400 ms)를 함께 그림.*

---

### 5. G0.7: Scaling Up a Fast World Action Model with Long Context (80점)

[arXiv](https://arxiv.org/abs/2611.31822) · [PDF](https://arxiv.org/pdf/2611.31822) · [alphaXiv](https://www.alphaxiv.org/abs/2611.31822) (요약 있음)

- **저자**: Tianyuan Yuan, Baijun Ye, Shicheng Cao, Xing Nie, Xiaopeng Yu, Ke Dong, Zijie Zhao, Shenling Qiu 외 17명
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 74점
- **읽은 원문**: PDF 전문

> 미래 영상 생성 없이 행동을 바로 뽑을 수도 있는 world action model(WAM)에 최대 5분 길이의 관측 기록을 넣고, 로봇 데이터와 사람 1인칭 영상으로 크게 사전학습함. 숨긴 물체를 추적하는 컵 섞기 과제의 분포 밖(OOD) 조건 성공률이 80.0%로, 장기 기억용 WAM인 Long-WAM의 26.7%보다 높음.

**무슨 문제인가**

world action model(WAM)은 사전학습된 video generator에서 출발해 미래 카메라 frame과 로봇 행동을 함께 예측하는 policy임. 대부분의 WAM은 행동마다 미래 frame을 먼저 만들어서 chunk 하나에 수백 ms가 걸리고, 그만큼 closed-loop 제어가 멈춤. 또 최근 frame 한두 장만 보므로 가려진 물체의 위치나 사람이 앞서 보여 준 시연의 뜻처럼 지금 화면에 없는 정보를 쓰지 못함. 저자들의 이전 연구 Fast-WAM은 미래 영상 생성이 학습에만 필요하고 추론에는 필요 없다고 보였지만, 단일 frame 입력과 작은 데이터에서만 확인했음.

**어떻게 푸나**

G0.7은 language expert와 vision/action expert 두 개로 된 dual-expert 구조이고, language expert가 지시문을 인코딩해 매 층에서 vision/action expert를 조건화함. 입력은 최대 5분 분량의 실제 카메라 관측 latent, 고유감각 상태, 지시문이고, 출력은 16-step action chunk임. 관측은 sliding-window KV cache에 깨끗한 video latent로 쌓이고, chunk를 실행할 때마다 새 frame이 들어오고 가장 오래된 frame이 빠짐. 사람 시연 영상을 이 cache 앞에 넣으면 과제를 예시로 지정하는 in-context learning(ICL)이 됨. 사전학습부터 여러 chunk를 이어 autoregressive하게 학습하고, 별도 memory module은 쓰지 않음. 학습 때 샘플마다 절반 확률로 action token이 미래 video latent를 보게 하거나 못 보게 가려서, 한 checkpoint가 두 추론 경로를 모두 지원함. IDM mode(imagine-then-act)는 미래 영상을 먼저 denoise한 뒤 그 영상을 조건으로 행동을 만들고, Fast mode는 영상 생성 없이 cache에서 행동만 5 step으로 denoise함. 사람 1인칭(ego) 영상은 3D 손 자세를 추출해 저자들의 Galaxea R1 로봇(R1 Pro, R1 Lite) gripper 좌표 규약에 맞춘 손목 6-DoF 자세와 손끝 5개 위치로 바꿔 또 하나의 embodiment로 학습함.

**결과**

- 컵 섞기 과제(shell game: 컵 밑에 숨긴 물체를 섞은 뒤 찾아 듦)에서 G0.7의 학습 분포 안(ID)/분포 밖(OOD) 성공률은 93.3%/80.0%이고, Long-WAM은 53.3%/26.7%임. 시연 따라 분류하기(sorting by example)에서는 93.3%/66.7% 대 60.0%/40.0%임. 설정마다 15회 시도이고, 여러 frame을 넣어 준 π0.5는 두 과제 모두 26.7% 이하임.
- 같은 checkpoint에서 Fast mode와 IDM mode의 점수는 비슷함. 시뮬레이션 benchmark 5개(LIBERO 계열, RoboTwin 2.0, VLABench, RMBench, RoboDojo) 평균 점수는 70.8 대 70.3임. 실로봇 post-training 6개 과제 progress는 87.3 대 87.8임. 한 대의 RTX 5090에서 BF16으로 잰 chunk당 시간은 156 ms 대 457 ms이고, FP8로 배포한 Fast mode는 60 ms임.
- 같은 구조에서 사전학습 데이터만 바꾼 비교에서, 로봇 데이터만 쓴 G0.7-Robot의 R1 Lite zero-shot 집기·놓기 성공률은 12%(50회 중 6회)이고 ego 영상을 더한 G0.7은 54%(50회 중 27회)임.
- 실로봇 post-training 7개 과제의 평균 task progress(과제 단계 중 완료한 비율)가 G0.7 86.9%, 저자들의 이전 VLA인 G0.5 64.3%, π0.5 41.7%, 공개 WAM인 OpenWAM 18.6%임. 도구 사용 4개는 도구당 시연 20개, 상자 접기·레몬차 만들기·상품 포장 3개는 과제당 약 5시간 데이터로 학습함.

**한계**

초록의 7.6배 속도 향상은 FP8 Fast mode와 BF16 IDM mode를 비교한 값이고, 같은 정밀도 비교는 2.9배임. ego 영상을 더한 효과는 전체 사전학습 데이터 양이 같이 늘어난 비교라서 사람 영상이라는 종류의 효과만 따로 떼어 보이지 못함. ICL 결과는 과제 2개, 설정당 15회이고 해당 과제 시연으로 post-training한 뒤의 값이며, 코드·가중치 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- world model을 추론 때 상상에 쓰지 않고 학습 신호로만 써도 성능이 유지된다는 같은 checkpoint 비교는, world model 기반 test-time planning이 실제로 이득을 주는 조건을 따질 때 기준선이 됨.
- 별도 memory module 없이 KV cache에 5분 관측을 쌓는 방식은 robot memory와 사람 시연 기반 과제 지정 연구에서 비교 대상으로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 G0.7의 구조와 제어 루프를 그린 그림임. 사람 시연과 로봇 기록 frame이 5분 context에 들어가고, vision/action expert가 16-step action chunk를 내며 IDM mode에서만 미래 frame을 먼저 상상하는 흐름을 보여 줌.*

---

### 6. Exploratory Midtraining for Robot Policies (80점)

[arXiv](https://arxiv.org/abs/2611.33130) · [PDF](https://arxiv.org/pdf/2611.33130) · [alphaXiv](https://www.alphaxiv.org/abs/2611.33130) · [프로젝트 페이지](https://kshitiz-1225.github.io/exploratory-midtraining-robot-policies/)

- **저자**: Kshitiz, Zheyuan Hu, Robyn Wu, Yizhou Li, Yunchu Zhang, Vattanary Tevy, Kavya Tayal, Shawn Yin 외 6명
- **분야**: Manipulation · robotics relevance 10/10 · 1차 스크리닝 74점
- **읽은 원문**: PDF 전문

> 사람 한 명이 환경을 계속 흐트러뜨리고 다른 한 명이 리셋 없이 과제를 이어 가는 방식으로 데이터(β-Data)를 모음. 이 데이터로 π0.5를 사전학습과 과제별 finetuning 사이에 한 번 더 학습(midtraining)시켜, 실패 뒤 다시 시도하고 이어 가는 low-level 행동을 넓힘. 시뮬레이션 양손 packing 20개 과제(ID 8개, OOD 12개)의 성공률이 standard demonstration으로 midtraining했을 때의 54.7%에서 69.7%로 오름.

**무슨 문제인가**

generalist robot policy는 주로 사람이 모은 demonstration으로 배우는데, 이 데이터는 대부분 잘 해낸 행동으로 채워져 있음. 실수와 복구 장면이 일부 들어 있어도 어떤 어려운 상태가 담길지는 수집 중에 우연히 생긴 상황에 달려 있음. 그래서 demonstration을 더 모아도 어려운 상태에서 다시 진행할 수 있는 상태로 넘어가는 행동은 크게 늘지 않음. 기존의 intervention 기반 수집은 특정 policy가 낸 실수에 묶이고, action noise 주입은 의미 있는 어려운 상태를 고르지 못함.

**어떻게 푸나**

저자는 데이터가 서로 다른 상태 전이를 얼마나 덮는지를 재는 CBC(connected behavioral coverage)를 정의하고, β-Data가 이 값을 늘린다고 봄. CBC는 데이터 구간마다 시작과 끝을 추상 상태(예: 물체가 어느 tray에 있는지)로 바꾸고, 방향이 있는 서로 다른 전이의 개수로 셈. 데이터는 기존 adversarial teleoperation 규약으로 모음. operator는 과제 완수만 목표로 하고, adversary는 물체를 꺼내 놓거나 돌리거나 목표를 바꾸는 식으로 되돌릴 수 있는 방해를 넣음. operator는 방해된 상태에서 리셋 없이 이어 가므로, 방해에서 적응과 진행 재개까지 이어진 긴 궤적이 쌓임. 시뮬레이션에서는 adversary를 프로그램으로 구현함. 학습할 때는 각 궤적을 국소 결과 단위로 잘라 자연어로 다시 라벨링함. 또 직전 120개 action을 4개 token으로 넣어 policy가 지금 어느 시도 단계인지 알게 함. 입력은 영상·proprioception·subtask 문장·action history이고 출력은 action chunk이며, 평가 때는 high-level planner가 subtask 문장을 줌. 이렇게 midtraining한 policy를 새 과제에서 filtered BC(성공한 rollout만 모아 behavior cloning)로 online finetuning함.

**결과**

- 시뮬레이션 packing(MuJoCo에서 양손 xArm7이 여러 식료품을 크기가 다른 tray에 담는 과제)의 OOD long 과제 성공률이 39.2%에서 57.6%로 오름. OOD 12개 과제 평균은 62.7%에서 79.2%로 오르고, 같은 standard demonstration으로 학습한 PostBC(demonstrator action의 불확실성을 모델링해 policy 행동을 넓히려는 기존 방법)는 64.0%에 그침.
- 데이터 양을 바꾼 비교에서 β-Data 2.6시간은 60.3%를 얻어, 두 배인 standard demonstration 5.2시간의 58.7%와 비슷함. 5.2시간 학습 policy의 rollout 시간 제한을 2분에서 6분으로 늘리면 β-Data는 55.5%에서 69.3%로, standard는 47.8%에서 58.7%로 오름. 가장 적은 0.65시간에서는 standard가 16.5% 대 6.0%로 앞섬.
- 로봇 3종의 OOD 과제 5개(과제당 20회)에서 모두 standard demonstration policy보다 성공 횟수가 많음. 예를 들어 양손 YAM LEGO 분해(interlock)는 5회에서 19회로, xArm packing은 4회에서 12회로, 바지 개기는 3회에서 14회로 오름.
- 두 policy에 같은 subtask 문장을 줘도 β-Data policy가 standard보다 OOD Medium(중간 길이 과제)과 Long(긴 과제)에서 각각 20.5퍼센트포인트, 18.4퍼센트포인트 높음. action history를 빼면 β-Data의 OOD long 성공률이 57.6%에서 41.6%로 내림.

**한계**

online finetuning에서 rollout 수가 줄고 성공률이 오른다는 저자 주장의 수치는 본문에서 확인 불가임. 가장 어려운 OOD 재배치 과제에서는 두 policy 모두 성공률 16% 이하에 머묾. 수집에 사람 두 명이 필요하고, adversary가 어디를 방해할지는 사람 판단에 기대며 base policy는 π0.5 하나만 실험함.

**누리랩 연구와의 연결**

- 실패 뒤 다시 잡기·재배치 같은 recovery 행동을 데이터 수집 단계에서 늘리는 방법이라, failure detection/recovery를 policy 쪽에서 다루는 VLA 연구의 비교 대상이 됨.
- action history 조건과 rollout 시간을 늘릴수록 성공률이 오르는 결과는 rollout 시간을 늘려 재시도 기회를 주면 성공률이 오르는 manipulation policy 설계와 robot memory 연구에 바로 이어짐.

*대표 그림: 실제 양손 YAM 로봇이 같은 LEGO 조립체와 같은 목표 문장에서 시작해 세 rollout에서 서로 다른 잡기·기울이기·뒤집기 순서로 벽돌을 분해하는 장면을 보여 줌. 측정 수치가 아니라 β-Data로 학습한 policy의 행동 다양성을 보여 주는 정성 예시임.*

---

### 7. Seeing Is Not Reaching: Instruction Shortcuts Override Visual Grounding in Vision-Language-Action Models (79점)

[arXiv](https://arxiv.org/abs/2611.32206) · [PDF](https://arxiv.org/pdf/2611.32206) · [alphaXiv](https://www.alphaxiv.org/abs/2611.32206) · [코드](https://github.com/QZhang2111/psg)

- **저자**: Qing Zhang, Xuesong Li, Zhaoyuan Yang, Changlin Song, Xinyu Tian, Jing Zhang
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 78점
- **읽은 원문**: PDF 전문

> π0.5는 옮겨진 물체를 attention으로는 찾지만, instruction이 물체의 학습 때 위치를 불러오는 경로가 이를 덮어씀을 attention 경로 차단 실험으로 밝힘. 두 경로의 효과를 따로 조절하는 학습 없는 sampling guidance로 LIBERO-PRO Object 위치 교란에서 성공률을 16.6%에서 40.8%로 올림.

**무슨 문제인가**

VLA는 VLM에서 visual grounding(이름으로 이미지 속 물체를 찾는 능력)을 물려받을 것으로 기대되지만, 물체를 옮기면 팔이 그 물체의 학습 때 위치로 가는 경우가 많음. 기존 연구는 이를 장면 정보 의존이나 instruction이 익숙한 궤적을 불러오는 현상으로 설명했음. 그러나 행동만 보아서는 모델이 grounding을 잃은 것인지, 갖고 있지만 쓰지 않는 것인지, 다른 경로에 의해 덮어써지는 것인지 구분할 수 없음. 원인에 따라 고칠 방법이 달라지므로 이 구분이 필요함.

**어떻게 푸나**

먼저 VLA 6개를 LIBERO-Object 과제 5개에서 시험하고, 성공률 대신 gripper가 처음 닫히는 위치를 기록함. 같은 장면에 다른 물체를 요청하면 OpenVLA-OFT 등 3개는 장면의 원래 과제 위치로 가고(scene shortcut), π0 계열은 요청한 물체의 학습 때 위치로 감(instruction shortcut). π0.5에서는 물체 이름 token의 attention이 옮겨진 물체를 따라가는데도 팔은 학습 때 위치로 가며, 저자는 이를 Seeing Is Not Reaching이라 부름. 이어서 instruction이 action에 닿는 두 경로를 attention mask로 따로 끊음. grounding pathway는 이미지 token이 instruction을 읽고 action token이 그 이미지 token을 읽는 경로임. direct pathway는 action token이 instruction을 직접 읽는 경로임. PSG(Pathway-Separated Guidance)는 각 경로를 끊었을 때 flow matching의 예측 velocity가 바뀌는 양을 그 경로의 효과로 정의함. Euler step마다 grounding 효과에는 a배(a=5)를 더하고 direct 효과에는 b배(b=1, 전부)를 빼서 velocity를 고침. 입력은 카메라 이미지와 instruction이고 출력은 action chunk임. 학습, 물체 좌표, segmentation mask, detector를 쓰지 않음. 대신 action chunk마다 prefix 계산 1회와 Euler step마다 action expert 계산 2회가 추가됨.

**결과**

- 위치 교란(Position) 200 episode에서 π0.5가 옮겨진 물체를 처음 집으려 한 횟수가 29회임. grounding pathway를 끊으면 0회로 내리고, direct pathway를 끊으면 64회로 오름. 원래 장면에서는 direct pathway를 끊어도 200회 중 199회를 유지함.
- LIBERO-PRO(LIBERO 장면에서 물체 위치나 지시를 바꾸는 교란 benchmark)의 Object Position에서 Reach(첫 grasp가 요청 물체에 닿은 비율)가 22.0%에서 52.6%로 오름. 성공률은 16.6%에서 40.8%로 오름. 원래 LIBERO 평균 성공률은 96.7%에서 95.2%로 조금 내림.
- LIBERO-PRO Position의 Object·Goal·Spatial 평균 Reach에서 PSG는 π0.5의 62.6%를 76.5%로 올림. 지시 전체를 빼고 대조하는 학습 없는 guidance인 CAG는 이 값을 61.1%로 내리고, 원래 LIBERO 성공률도 87.7%로 내림. vision-only 예측과 대조해 language 조건을 강화하는, 학습이 필요한 기존 방법 RSS는 같은 평균에서 Reach 78.7%, 성공률 46.1%이고 PSG는 76.5%, 44.7%임.
- LIBERO-Goal(서랍 열기, 물건 놓기 등 목표가 다른 조작 과제 모음)에서 물체를 30cm 넘게 옮기면 Reach가 24%에서 50%로 오름. grounding 효과 대신 정답 방향을 넣는 oracle은 81%임. 모든 실험은 시뮬레이션이며 실로봇 실험은 없음.

**한계**

경로 차단은 π0.5와 π0에만, PSG는 사실상 π0.5에만 적용했고 LIBERO 계열 시뮬레이션과 단일 noise seed로만 평가함. BBQ sauce처럼 이름 attention이 물체를 가려내지 못하면 PSG도 효과가 없으므로, 이미 grounding이 남아 있는 모델에서만 쓸 수 있음. a와 b는 개발용 과제 11개에서 골랐는데, 이때 쓴 start state 6~15번이 평가 episode의 start state와 겹침.

**누리랩 연구와의 연결**

- VLA의 실패를 행동만이 아니라 내부 경로 차단으로 원인별로 가르는 방법이라 failure diagnosis와 counterfactual reasoning 연구의 진단 도구로 바로 쓸 수 있음.
- 학습 없이 flow matching sampling 중 velocity를 고치는 방식이라 test-time optimization과 inference-time steering 연구에서 π0.5 기반 비교 대상으로 쓸 수 있음.

*대표 그림: 같은 장면에 다른 물체(cream cheese)를 요청했을 때 OpenVLA-OFT, π0, π0.5의 첫 gripper 닫힘 위치 비율과 attention 배율을 비교한 표임. 위치는 장면 과제 자리, 요청 물체의 학습 위치, 실제 요청 물체로 나뉨. π0.5는 요청 물체에 이름 attention이 4.5배로 몰리지만 첫 닫힘의 78%는 학습 위치에서 일어남.*

---

### 8. One Phase Is Enough: Sim-to-Real Transfer with Direct Visual Reinforcement Learning (74점)

[arXiv](https://arxiv.org/abs/2611.31588) · [PDF](https://arxiv.org/pdf/2611.31588) · [alphaXiv](https://www.alphaxiv.org/abs/2611.31588) · [프로젝트 페이지](https://jmarangola.github.io/one-phase-visual-rl)

- **저자**: John Marangola, Antonia Bronars, Younghyo Park, Stephen Andrews, Kushal Kedia, Pulkit Agrawal
- **분야**: RL · robotics relevance 10/10 · 1차 스크리닝 79점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 10쪽
- **읽은 원문**: PDF 전문

> 시뮬레이션에서 privileged teacher를 거치지 않고 카메라 영상 policy를 RL로 바로 학습하는 DRIFT를 제안함. 고정된 DINOv3 encoder와 빠른 rasterized 렌더링으로 학습을 감당할 만하게 만들었고, 실로봇 3개 과제 평균 성공률이 teacher-student distillation의 51.1%에서 81.1%로 오름.

**무슨 문제인가**

시뮬레이션 RL로 만든 조작 policy는 대개 물체 pose 같은 상태값을 입력으로 받으므로, 카메라 영상만으로 쓰려면 별도 처리가 필요함. 흔한 방법은 상태값을 보는 teacher를 RL로 먼저 학습하고, 영상을 보는 student가 그 행동을 imitation으로 따라 하게 하는 두 단계 방식임. 이 방식에서는 teacher가 쓴 정보를 student가 영상에서 알아낼 수 없는 경우가 생기고(realizability gap), imitation으로 배운 student는 시뮬레이션 밖에서 일반화가 약할 수 있음. 반대로 영상 policy를 처음부터 RL로 학습하면 vision encoder까지 reward로 배워야 해서 계산량이 너무 큼.

**어떻게 푸나**

DRIFT(Direct Reinforcement Learning from Images For Transfer)는 영상 policy를 PPO로 바로 학습함. 입력은 배포 때 쓰는 손목 카메라 RGB 영상과 proprioception이고, 출력은 관절 위치 목표와 gripper 명령임. 영상은 고정된 DINOv3 ViT-S/16에 넣어 196개 patch feature를 얻고, gradient는 encoder로 흘려보내지 않음. MAP head(학습되는 query가 patch feature에 cross-attention을 거는 attention pooling)가 patch feature를 소수의 visual token으로 줄임. 이 token과 proprioception token을 3층 transformer actor가 함께 처리해 행동을 냄. critic만 시뮬레이터의 privileged state를 보는 asymmetric actor-critic 구조이고, 배포 때는 actor만 씀. encoder가 고정이므로 patch feature를 한 번 계산해 PPO epoch 4번에 재사용하고, 사전학습 표현에 기대어 ray tracing 대신 빠른 rasterized 렌더링으로 학습함. 시뮬레이션은 ManiSkill이고, 카메라 보정, actuator system identification, 조명·질감·배경 이미지 randomization을 함께 씀.

**결과**

- 실로봇 Franka FR3에서 zero-shot 전이를 잼. Peg-Insertion과 Push-T는 과제당 30회, Pick-Cube는 20회 평가함. Peg-Insertion(틈새 2mm 구멍에 사각 peg 끼우기) 성공률은 DRIFT 66.7%, 같은 고정 encoder를 쓴 two-phase distillation 23.3%임. Push-T(T자 블록을 밀어 목표 자세에 맞추기)는 76.7% 대 30.0%임. 시뮬레이션 성공률 차이는 3.8~5.7퍼센트포인트로 작았음.
- Pick-Cube(정육면체 집어 올리기)는 두 방법 모두 실로봇 100%임. 학습에 없던 물체 4개에서 20회씩 재면 평균 성공률이 DRIFT 88.8%, two-phase distillation 50.0%임.
- 같은 150 GPU 시간(L40S 기준) 시뮬레이션 평가에서 분포 안 성공률은 그림 5 기준 DRIFT 약 91%, two-phase distillation 약 84%로, DRIFT가 상대적으로 8.6% 높음. 물체 질량·크기, 초기 위치 범위, 시점, 외력을 바꾼 분포 밖 조건에서 two-phase distillation은 분포 안 성공률의 약 42%를 잃고, DRIFT는 약 14%를 잃음.
- Peg-Insertion에서 고정 encoder 7종을 비교함. SigLIP2 ViT-B/16은 시뮬레이션 73.2%였지만 실로봇 10.0%이고, DINOv3 ConvNeXt-B는 시뮬레이션 73.4%, 실로봇 3.3%임. DINOv3 ViT-S/16은 시뮬레이션 82.2%, 실로봇 66.7%임.

**한계**

실로봇 과제는 Franka 한 대와 손목 카메라 한 대로 한 3개뿐이고, 표 1의 실로봇 수치는 seed 3개 중 실로봇 성공률이 가장 높은 seed를 보고한 값임. checkpoint 선택에도 실로봇 rollout 5회를 썼으므로 순수한 시뮬레이션 기준 선택은 아님. distillation 쪽 baseline은 DAgger 방식 하나뿐임. 분포 밖에서 차이가 나는 원인은 latent likelihood 분석으로 정황만 보임. 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- manipulation sim-to-real에서 teacher-student distillation 대신 고정 foundation encoder 위에서 RL을 바로 돌리는 선택지를 같은 계산량 조건으로 비교한 자료임. 랩에서 시뮬레이션 RL로 조작 policy를 만들 때 baseline 설계와 encoder 선택(DINOv3 ViT-S/16, MAP head)의 출발점으로 쓸 수 있음.
- 시뮬레이션 rollout의 transformer latent에 GMM을 맞추고 실로봇 latent의 likelihood로 분포 이탈을 재는 분석은 failure detection 신호로 바로 시험해 볼 수 있음.

*대표 그림: 측정 결과가 아니라 기존 두 단계 방식(왼쪽)과 DRIFT(오른쪽)의 구조를 그린 그림임. 왼쪽은 privileged state로 PPO 학습한 teacher를 RGB student로 옮기고, 오른쪽은 고정된 DINOv3 patch feature로 actor를 바로 PPO 학습하며 privileged state는 critic에만 넣음.*

---

### 9. DexWAC: A Unified World-Actor-Critic Model for Dexterous Robot Manipulation (74점)

[arXiv](https://arxiv.org/abs/2611.32654) · [PDF](https://arxiv.org/pdf/2611.32654) · [alphaXiv](https://www.alphaxiv.org/abs/2611.32654)

- **저자**: Hongjia Liu, Dacheng Zhou, Minghao Fu, Chuanjun Guo, Tianze Wang, Qingtao Liu, He Wang, Li Yi
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 78점
- **읽은 원문**: PDF 전문

> dexterous manipulation용 policy·action-conditioned world model·TD critic을 한 번의 사전학습에서 한 모델로 함께 학습하고, 이 world model 안에서 PPO로 policy를 더 개선할 수 있게 함. 사전학습만 한 모델로 실로봇 과제 2개 평균 성공률이 π0.5의 45%에서 75%로 오름.

**무슨 문제인가**

WAM(world-action model: 행동과 미래 관측을 함께 예측하는 모델)은 미래 예측을 policy 학습의 보조 loss로만 씀. 사전학습된 policy를 더 개선하려는 방법들은 world model과 reward·value model을 따로 학습함. generalist policy라면 이 모델들도 같은 범위의 과제와 embodiment에 일반화해야 하므로, 따로 사전학습하면 계산이 겹치고 같은 표현을 다시 배우게 됨. 또 따로 학습하면 동역학 예측과 가치 예측이 actor가 쓰는 표현에 함께 영향을 주지 못함.

**어떻게 푸나**

DexWAC(unified World-Actor-Critic model)은 이미지 편집용 생성 모델 FLUX.2-klein(4B)을 world backbone으로 씀. 여기에 작은 actor-critic expert를 MoT(Mixture-of-Transformers: 가중치는 나누고 attention으로 특징만 공유하는 구조)로 붙임. backbone은 언어 지시, 현재 관측의 VAE latent, proprioception을 인코딩하고 expert는 이 K/V를 읽음. 사전학습에서 actor는 16 step 길이의 action chunk를 behavior cloning으로 배움. 같은 단계에서 world model은 action chunk가 주어졌을 때 chunk 끝 시점의 latent와 proprioception을 flow matching으로 예측함. reward는 성공 신호를 성공 직전 구간에 Gaussian 모양으로 나눠 준 dense reward임. critic은 이 reward와 value bootstrapping을 이어 갈지 나타내는 값(continuation)을 예측하고, chunk 단위 TD로 state value를 학습함. 중간 frame을 만들지 않고 chunk 끝점만 예측하므로 상상 rollout 한 단계가 예측 한 번으로 끝남. 다음 단계에서는 사전학습 actor의 성공·실패 rollout으로 world model과 critic만 다시 맞추고, 마지막으로 고정된 world model 안에서 2 chunk 길이의 상상 rollout을 돌려 BC 정규화를 건 PPO로 actor를 갱신함. 대안으로 상상 전이로 학습한 Q critic이 actor가 낸 후보 32개 중 하나를 고르는 best-of-N도 씀.

**결과**

- DexJoCo(MuJoCo 기반 손 조작 benchmark, 장기 기억이 필요한 3개를 뺀 8개 과제)에서 3 seed 평균 성공률임. 사전학습만 한 DexWAC은 65.50%로 π0.5의 57.92%보다 높고, 대규모 사전학습 WAM인 Motus의 66.83%와 비슷함.
- 과제당 실행 50회로 world model과 critic을 맞춘 뒤 상상 속 PPO를 500 update 하면 같은 8개 과제 평균이 65.50%에서 67.75%로 오름. 양손 과제 평균은 47.78%에서 52.89%로 오르고, 한 팔 과제는 76.13%에서 76.67%로 거의 유지됨.
- 보지 않은 DexJoCo 궤적 40개에서 16 step 뒤 관측을 예측할 때 6개 화질 지표 모두 가장 좋음. wrist view LPIPS는 value 예측을 함께 하는 기존 world-action model인 FACT의 0.1373에서 0.0853으로 내려가고, 예측 한 번에 0.214초로 FACT보다 약 8.5배 빠름.
- 실로봇 과제 2개에서 과제당 30회 시도한 성공률이 계란 옮기기 50% 대 20%, 양손 컵 빼기 100% 대 70%로 π0.5보다 높음. 실로봇 결과는 상상 속 policy 개선 없이 사전학습만 한 모델임.

**한계**

상상 속 PPO의 이득은 2.25퍼센트포인트로 seed 간 표준편차(1.8에서 2.2퍼센트포인트)와 크기가 비슷하고, 과제별로는 오르는 과제와 내리는 과제가 섞임. 저자도 학습을 오래 하면 policy와 critic이 world model 오차를 이용하는 문제가 생기고, best-of-N에서 더 심하다고 밝힘. ablation 표의 DexWAC 성공률 68.00%는 seed 0 한 번의 값이라, 3 seed 평균인 65.50%와 직접 비교하기 어려움. 대규모 사전학습 규모에서의 검증과 코드 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- 한 모델 안에 world model과 TD critic이 같이 들어 있어, test-time에 critic으로 후보 행동을 고르거나 성공 여부를 판정하는 failure detection 실험의 기반으로 쓸 수 있음.
- chunk 끝점만 예측하는 world model은 상상 rollout 비용을 크게 줄이므로, dexterous manipulation에서 world model 기반 test-time optimization을 시도할 때 비교 대상이 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 개념도임. 실로봇·DexJoCo·RoboTwin 데이터로 World와 Actor/Critic을 함께 사전학습하는 단계, 성공·실패 실행으로 World와 Critic을 맞추는 단계를 차례로 보여 줌. 오른쪽은 고정된 world model 안에서 actor가 reward를 받으며 개선되는 단계임.*

---

### 10. Ground, Guide, Act: Improving VLA Spatial Generalization with Multimodal Foundation Models (74점)

[arXiv](https://arxiv.org/abs/2611.31452) · [PDF](https://arxiv.org/pdf/2611.31452) · [alphaXiv](https://www.alphaxiv.org/abs/2611.31452) · [프로젝트 페이지](https://tom-zgt.github.io/MFM-VLA)

- **저자**: Guangting Zheng, Shaoxuan Wang, Yu Yuan, Zhipeng Tang, Jiajun Deng, Yanyong Zhang
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 76점
- **읽은 원문**: PDF 전문

> VLA가 위치·목표가 바뀐 과제에서 실패하는 주된 원인이 목표 물체 선택과 큰 이동 경로라는 분석을 바탕으로, 이 두 부분만 multimodal foundation model(MFM)과 controller가 맡고 접촉 조작은 VLA에 남기는 MFM-VLA를 제안함. LIBERO-PRO 전체 성공률을 54.9%에서 69.8%로, 실로봇 atomic 과제 평균을 π0.5의 15.3%에서 54.4%로 올림.

**무슨 문제인가**

π0.5 같은 VLA는 학습 장면에서는 잘 하지만 물체 위치나 지시한 목표 물체가 바뀌면 성공률이 크게 내려감. 저자들이 LIBERO-PRO(LIBERO 과제에 문장·외형·위치·목표 물체 교란을 건 benchmark)에서 재 보니 π0.5는 문장 교란에서 92.0%, 위치 교란에서 22.2%였음. 지시를 바꾸거나 빈 문장을 줘도 학습 때 집던 물체를 그대로 집는 경우가 많아서, 저자들은 이를 visual scene shortcut이라 부름. MFM에게 직접 action을 내게 하면 느리고 접촉 조작이 부정확하므로, MFM을 VLA의 어느 단계에 붙여야 하는지가 문제임.

**어떻게 푸나**

먼저 PDIS(Phase-Decoupled Intervention Staircase: 집기·놓기를 접근, 집기, 운반, 내려놓기 단계로 나눠 일부 단계만 정답 경로로 대신 움직이는 분석 절차)로 VLA 4종을 분석함. 접근 단계만 정답으로 대신해 줘도 π0.5의 목표 물체 들어 올리기 비율이 크게 오르므로, 저자들은 국소 조작 능력은 남아 있다고 결론 냄. 이에 따라 MFM-VLA에서는 MFM(주로 GPT-6 Astra)이 RGB 두 시점에서 집을 점과 놓을 점을 고르고 삼각측량으로 3D 좌표를 구함. Cartesian controller가 그 좌표 위의 handoff 자세까지 빈 공간 이동을 하고, VLA가 정렬·집기·내려놓기를 맡음. VLA는 action chunk마다 목표까지의 상대 위치와 다음 움직임을 적은 dense geometric caption과, 팔을 궤적 밖으로 밀었다가 되돌아오는 recovery 데이터로 다시 fine-tuning됨. 마지막으로 development set에서 VLA 단독 실행과 MFM 보조 실행의 성공률을 비교해 suite 단위로 어느 쪽을 쓸지 정해 고정하는 router를 둠. 별도 monitor가 잘못 집기나 떨어뜨림을 감지하면 최대 두 번까지 다시 집게 함.

**결과**

- LIBERO-PRO 8,000 episode 전체 성공률이 π0.5의 54.9%에서 69.8%로 오름. 위치 교란은 22.2%에서 47.5%, 목표 물체 교란은 25.2%에서 52.6%로 오름. router 보정에 쓴 seed를 뺀 7,200 episode에서도 54.8%에서 69.3%로 비슷함.
- 같은 GPT-6 Astra가 VLA 없이 직접 로봇을 움직이면 LIBERO-PRO 171 episode 성공률이 3.5%임. 같은 episode에서 MFM-VLA는 74.3%임. 다만 이 비교는 router 보정 seed에서 잰 값임.
- ALOHA-Sim-PRO(양팔 큐브 전달 과제에 4종 교란을 건 시뮬레이션)에서 교란 4종 평균 성공률이 π0의 23.5%에서 97.5%로 오름. 가장 높은 baseline인 ACT는 42.0%임.
- 실제 Franka 팔과 XHand 손으로 유리 기구를 다루는 과제(과제·설정당 20회)에서 atomic 과제 평균이 π0.5의 15.3%에서 MFM-VLA의 54.4%로 오름. 여러 단계 과제 평균은 0.8%에서 31.7%로 오름.

**한계**

성능은 calibration된 RGB 두 시점과 강한 MFM에 크게 기댐. grounding을 두 시점 대신 한 시점으로 하면 MFM 보조 episode 성공률이 73.6%에서 45.6%로 내림. 3D grounding을 GroundingDINO로 바꾸면 16.4%로 내림. RoboCasa365(주방 mobile manipulation 50개 과제)에서는 전체가 16.9%에서 20.5%로만 오르고 처음 보는 복합 과제는 1.2%에서 2.4%임. router는 같은 benchmark의 앞쪽 seed로 보정됨. 논문이 제시한 LIBERO-PRO 전체 84.4%는 과제별로 만든 code policy를 더한 확장판의 값임. 코드 공개 여부는 본문에서 확인 불가임.

**누리랩 연구와의 연결**

- VLA 실패를 단계별 개입으로 쪼개 원인을 찾는 PDIS 절차는 failure diagnosis 연구에서 그대로 가져다 쓸 수 있는 분석 도구임.
- 성공률 차이로 VLA 단독과 MFM 보조를 고르는 router와 잘못 집기 감지 후 재시도는 failure detection/recovery와 VLA 조합 연구에서 비교 대상으로 쓸 수 있음.

*대표 그림: PDIS 분석 결과를 그린 그림으로, 집기·놓기 과정을 시작부터 성공까지 6개 시점 장면으로 그리고, 개입 설정 5개마다 정답 경로(GT)와 VLA가 맡는 구간을 막대로 보여 줌. 오른쪽 숫자는 위치·목표 물체 교란 episode 390개에서 잰 π0.5 성공률로, VLA만 쓸 때 44.1%, 접근·운반·내려놓기를 모두 대신할 때 82.8%임.*

---

### 11. ReFocus: Progress-Guided Adaptive Practice for Long-Horizon Robotic Manipulation Reinforcement Learning (74점)

[arXiv](https://arxiv.org/abs/2611.32639) · [PDF](https://arxiv.org/pdf/2611.32639) · [alphaXiv](https://www.alphaxiv.org/abs/2611.32639) · [프로젝트 페이지](https://refocus-robotics.github.io/)

- **저자**: Haoyuan Li, Wei Huang, Jiehong Lin, Shengrong Zhang, Chenzhi Liu, Shengchao Zhou, Hehe Fan, Xiaojuan Qi 외 1명
- **분야**: RL · robotics relevance 10/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> 긴 조작 과제를 하위 과제 그래프로 나눠 단계마다 같은 몫의 진행 reward를 주고, LLM이 찾은 병목 구간만 따로 더 연습시키는 online RL 방법을 제안함. SFT로 학습한 π0.5의 RoboCasa365 과제 16개 평균 성공률을 39.3%에서 51.3%로 올림.

**무슨 문제인가**

VLA policy를 online RL로 더 학습시킬 때 대부분의 방법은 과제 전체를 처음부터 끝까지 수행한 rollout에 성공/실패 reward 하나만 줌. 긴 과제에서는 그릇을 옮기다 실패한 episode와 선반에 놓다 실패한 episode가 똑같이 reward 0을 받아서, 어디까지 했고 어디서 막혔는지가 학습 신호에 남지 않음. 하위 과제 완료마다 reward를 주는 기존 방법은 하위 과제가 많은 단계에 reward가 몰리는 불균형이 있음. 또 정해진 상호작용 예산 안에서 뒤쪽 병목 단계는 앞 단계를 다 성공해야만 연습 기회가 생기므로 연습 횟수가 적음.

**어떻게 푸나**

ReFocus는 과제 전체를 학습하는 Global RL과 병목 구간만 연습하는 Local RL을 여러 round 번갈아 돌리며 하나의 VLA policy를 PPO로 갱신함. 먼저 LLM Scheduler가 과제 지시문으로부터 하위 과제와 선행 조건을 DAG(directed acyclic graph)로 만들고, 선행 조건이 같은 하위 과제를 한 단계(stage)로 묶음. Global RL에서는 진행 reward 총량 2를 단계 수로 똑같이 나누고, 각 단계 몫을 그 안의 하위 과제 수로 다시 나눠 하위 과제를 처음 완료할 때 줌(DAG-based Progress Reward). 여기에 과제 전체 성공 reward를 더함. Scheduler는 검증 rollout들의 진행 기록과 영상을 비교해 진행이 반복해서 멈추는 가장 이른 단계를 병목으로 진단하고, 시작 단계·목표 단계·상호작용 예산으로 이뤄진 연습 구간(Adaptive Practice Window)을 고름. Local RL에서는 시뮬레이터 중간 상태를 복원해 그 구간만 연습하는 normal, 처음부터 목표 단계까지 가는 prefix, 복원 상태에서 과제 끝까지 가는 suffix 세 가지 rollout을 섞어 씀. 목표 하위 과제의 reward는 Scheduler가 정한 더 잘게 나눈 중간 목표(milestone) reward로 바꿈. round가 끝나면 전체 과제 평가 결과와 연습 비용을 History Buffer에 기록하고, Scheduler가 이를 보고 다음 round에서 연습 구간을 유지·수정·생략할지 정함.

**결과**

- RoboCasa365 Composite-Seen(시뮬레이션 주방에서 물건 운반과 가전 조작이 이어지는 장기 과제 16개)에서 과제당 100회로 평균 성공률을 잼. SFT π0.5 39.3%, 가장 강한 baseline StructRL(하위 과제마다 같은 reward를 주는 방법) 45.8%, ReFocus 51.3%임. 1,400~2,900 step 과제군에서는 StructRL 39.4%, ReFocus 46.4%임. LIBERO-Long(탁상 다중 물체 장기 과제 10개)에서는 90.6%, 96.2%, 97.8% 순임.
- LIBERO-Long 구성 요소 ablation에서 성공/실패 reward만 쓰는 PPO가 92.6%임. 진행 reward만 더하면 96.8%, 연습 구간만 더하면 93.4%, 둘 다 쓰면 97.8%임. 성능 향상의 대부분은 진행 reward에서 나오고, 연습 구간은 진행 reward와 함께 쓸 때 400~550 step 과제군에서 91.0%를 93.0%로 올림.
- 연습 구간 고르는 방식을 바꾼 LIBERO-Long 비교에서 첫 round 구간 고정 94.8%, 가장 이른 실패 단계를 고르는 규칙 95.6%, History 없는 LLM 97.2%, History 있는 LLM 97.8%임. RoboCasa365에서 Scheduler를 오픈 모델 Qwen3.8-27B로 바꾸면 51.3%가 48.8%로 내리고, 과제당 비용은 1.28달러에서 0.05달러로 줄어듦.
- Unitree G1-D 휴머노이드의 실제 과제 3개에서 과제당 demonstration 50개와 자율 rollout 50개로 학습함. 토스터에 빵 넣고 스위치 누르기(BreadBaker)의 20회 성공률이 SFT 30%, RECAP(advantage 조건부 지도학습 방식의 실로봇 RL) 70%, ReFocus 95%임. 실로봇에서는 PPO 대신 RECAP의 return에 진행 reward를 더하고 병목 구간 데이터를 더 자주 뽑는 변형을 씀.

**한계**

Local RL의 normal과 suffix rollout은 시뮬레이터 중간 상태 복원에 기대므로 실로봇에서는 같은 방법을 쓸 수 없어 RECAP 기반 변형으로 대신함. LIBERO-Long에서 StructRL과의 차이는 1.6퍼센트포인트이고 3회 학습 표준편차가 0.6퍼센트포인트 수준이며, RoboCasa365의 다중 seed 결과는 checkpoint 하나를 평가 seed만 바꿔 잰 것임. 하위 과제 완료 판정과 milestone 판정이 실제 환경에서 얼마나 정확히 자동화되는지는 실험으로 보이지 않았고, 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- 검증 rollout의 진행 기록과 영상으로 반복해서 멈추는 단계를 LLM이 진단하고 그 결과로 학습 분포를 바꾸는 구조임. failure detection/diagnosis를 RL 학습 루프 안에 넣는 연구에서 비교 대상이 되고, 규칙 기반 진단(95.6%)과 LLM 진단(97.2%)의 차이도 참고 수치가 됨.
- 저자가 다음 단계로 제시한 것은 실행 중 병목에서 recovery skill을 골라 개입하는 online 보조자임. VLA의 failure recovery와 long-horizon manipulation 연구와 직접 이어짐.

*대표 그림: 왼쪽은 성공/실패 reward만 쓰는 기존 방식과 ReFocus의 진행 reward·연습 구간을 비교한 개념도이고, 측정 결과가 아니라 방법 구조를 그린 부분임. 오른쪽은 실로봇 과제 3개의 20회 중 성공 횟수(SFT, RECAP, ReFocus)와 LIBERO-Long·RoboCasa365 성공률(SFT, 성공/실패 reward만 쓰는 PPO인 Sparse-RL, ReFocus)을 막대로 보여 줌.*

---

### 12. CriticJEPA: World Models Are Better Critics Than Optimizers (74점)

[arXiv](https://arxiv.org/abs/2611.32357) · [PDF](https://arxiv.org/pdf/2611.32357) · [alphaXiv](https://www.alphaxiv.org/abs/2611.32357)

- **저자**: Xvyuan Liu, Jianjie Fang, Honglin Zhang, Zhaolu Wang, Xin Zhang, Wei Wu, Fengli Xu, Chen Gao 외 1명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 77점
- **읽은 원문**: PDF 전문

> H-JEPA라는 고정된 hierarchical world model을 gradient로 행동을 최적화하는 데 쓰지 않고, 학습된 flow 생성기가 낸 후보 계획을 rollout으로 비교해 고르는 데 씀. Visual AntMaze 성공률이 67.6%에서 89.1%로 오르고 planning 계산량은 26분의 1로 줄어듦.

**무슨 문제인가**

H-JEPA(시간 척도별로 여러 층을 둔 JEPA 계열 world model과 그 gradient planner)는 예측된 goal 거리 비용을 AdamW로 최대 90번 줄여 행동을 만듦. 저자들이 같은 시뮬레이터 상태에서 실제로 실행해 보니, 실행 후 도달한 영상의 latent와 goal 사이의 실제 거리 오차는 처음 10번 반복에서 25.3에서 23.0으로 줄지만, 30번과 90번 반복 뒤에는 22.8, 23.4로 더 줄지 않음. 반면 예측 오차는 계속 줄어 예측과 실제의 차이(optimism)가 8.6에서 16.7로 커짐. 같은 모델로 3번 다시 돌리면 단일 실행 성공률은 평균 72%인데 셋 중 하나라도 성공한 과제는 92%여서, 모델이 풀 수 있는 과제를 search가 안정적으로 찾지 못하는 것이 문제임.

**어떻게 푸나**

CriticJEPA는 world model의 가중치를 모두 고정하고, 계획을 만드는 일과 평가하는 일을 나눔. 먼저 level마다 conditional flow 생성기(proposer)를 reward 없는 학습 궤적에서 hindsight 방식으로 학습함. 입력은 현재 latent 상태, 목표까지의 latent 변위, horizon, 목표가 속한 level이고 출력은 그 level의 행동 시퀀스 한 묶음임. 계획할 때는 proposer가 후보 N개를 Euler 4 step으로 뽑고, 고정된 predictor가 각 후보를 rollout해 H-JEPA와 같은 비용으로 가장 낮은 것을 고름. 위 level에서 고른 계획의 첫 예측 상태가 아래 level의 subgoal이 되고, 맨 아래 level은 제어 입력을 실행함. 변형인 CriticJEPA-K는 선택 전에 모든 후보를 K번의 짧은 gradient step으로 다듬되, 원래 proposal에서 멀어지면 penalty(anchor)를 줌.

**결과**

- 진단 실험: AntMaze 300개 상태에서 H-JEPA search, 학습 데이터에서 가까운 상태의 기록 행동, flow proposal의 세 출처에서 각각 후보 8개를 뽑아 같은 상태에서 실행함. 고정된 predictor의 예측 순위와 실제 순위의 Spearman 상관은 H-JEPA search 결과에서 -0.03이고 top-1 선택률 12.0%로 우연 수준(12.5%)임. 같은 predictor가 flow proposal에서는 상관 0.28이고, 고른 행동의 실제 오차가 23.0으로 세 출처 중 가장 낮음.
- Visual AntMaze(64×64 top-down 영상과 proprioception으로 4족 로봇이 미로를 지나 목표 영상에 도달하는 과제): world model 3개의 평균 성공률이 H-JEPA 67.6%에서 CriticJEPA-5 89.1%로 오름. episode당 계산량은 131.0 TFLOPs 대 5.11 TFLOPs임. 개발 이후 만든 새 과제 50개에서도 74.7%에서 92.0%로 오름.
- 같은 설정을 다른 환경에 그대로 옮김. OGBench Cube(6-DoF 로봇 팔 큐브 조작) 3-level에서 48.7%에서 100%로, Push-T(T자 블록을 목표 자세로 미는 과제) 2-level에서 43.3%에서 57.3%로 오름. 환경과 level 수를 조합한 6개 설정 모두에서 계산량이 13배에서 79배 줄어듦.
- Cube와 FourRoom(좁은 문으로 이어진 여러 방을 지나는 navigation 과제)에서는 rollout 선택 없이 proposal 하나만 실행해도 100%여서, 이 두 환경의 향상은 주로 proposer에서 나옴. 반면 AntMaze 진단 모델에서는 proposal 하나가 52.0%이고 rollout 선택을 더하면 86.7%로 오름.

**한계**

모든 실험이 시뮬레이션이고 실로봇 실험은 없음. 본문 1쪽에 프로젝트 페이지와 코드 표시는 있으나 텍스트에서 주소는 확인 불가함. 3-level Push-T 성공률은 22.7%로 여전히 낮고, 설정은 AntMaze 모델 하나에서 정한 뒤 옮긴 것임. proposer는 world model의 학습 궤적에서 배우므로, 그 데이터에 없는 행동이 필요한 과제에서 어떻게 되는지는 보이지 않음.

**누리랩 연구와의 연결**

- world model을 optimizer가 아니라 후보 평가자(critic)로 쓰는 test-time planning 구조임. VLA가 낸 여러 action chunk를 world model rollout으로 골라 실행하는 inference-time selection 연구의 비교 대상이 됨.
- 같은 predictor라도 후보 분포에 따라 순위의 신뢰도가 달라진다는 진단은, world model 기반 failure detection에서 평가 대상 행동의 분포를 통제해야 한다는 근거가 됨.

*대표 그림: (a)는 같은 고정 모델로 H-JEPA를 3번 돌린 AntMaze 50개 과제의 성공과 실패를 과제별로 칠한 그림으로, 각 실행은 68%, 80%, 68%이고 셋 중 하나라도 성공한 비율은 92%임. (b)는 episode당 planning TFLOPs와 성공률을 찍은 그림임. CriticJEPA-5(89.1%, 5.11 TFLOPs)와 CriticJEPA-0(78.7%, 1.62 TFLOPs)이 H-JEPA(67.6%, 131.0 TFLOPs)보다 왼쪽 위에 놓임.*

---

### 13. VLAs Execute, Code Recovers: 3D Skill Envelopes Bridge the Compositional Gap in Agentic Manipulation (74점)

[arXiv](https://arxiv.org/abs/2611.32245) · [PDF](https://arxiv.org/pdf/2611.32245) · [alphaXiv](https://www.alphaxiv.org/abs/2611.32245)

- **저자**: Jiajie Zhang, Yankai Xiang, Changhao Chen
- **분야**: Manipulation · robotics relevance 9/10 · 1차 스크리닝 76점
- **학회**: ICRA·IROS·RA-L 계열 양식 (추정) · 근거: IEEE 2단 양식, 6쪽
- **읽은 원문**: PDF 전문

> 고정된 VLA skill을 이어 붙일 때 앞 skill이 남긴 물체에 팔이 부딪히는 실패를, skill이 지나가는 3D 공간을 미리 재서 막힘을 찾고 코드로 치우는 방식으로 줄임. 서랍이 낀 3~4단계 chain에서 성공률이 무작위 순서와 re-homing 조합의 29.7%에서 envelope 기반 순서 선택과 코드 repair를 함께 쓴 조건의 93.8%로 오름.

**무슨 문제인가**

long-horizon 조작을 end-to-end demonstration으로 다 모으기는 어려워서, LLM planner가 고정된 VLA skill을 차례로 부르는 agentic composition이 대안으로 쓰임. 그런데 혼자서는 잘 되는 skill도 앞 skill이 끝난 직후의 전환 지점(seam)에서 자주 실패함. LIBERO-Goal(시뮬레이션 주방 조작 과제 모음)의 skill 쌍 64개에서 π0.5의 성공률은 단독 98.0%, 바로 이어 붙이면 14.2%, 팔을 초기 자세로 되돌려도(re-homing) 82.8%임. 기존 방법은 로봇 자세만 되돌리거나 LLM이 언어로 진입 조건을 추측하게 해서, policy가 실제로 무엇에 막히는지는 확인하지 않음.

**어떻게 푸나**

먼저 같은 640개 전환 상태에서 세 가지 개입을 비교해 실패 원인을 가름함: 팔 자세 복원(Body), 남은 물체를 카메라 영상에서만 지우기(View Reset), 물체를 물리적으로 원위치시키기(World Reset). 그 결과 re-homing 뒤 남는 실패는 시각 변화가 아니라 고정된 VLA가 늘 쓰던 궤적을 그대로 따라가다 남은 물체에 부딪히는 충돌이 주원인으로 나옴. 이 경직성을 이용해 각 skill을 단독으로 실행하고 성공한 rollout 37~89개만 남김. forward kinematics로 팔, gripper, 잡은 물체가 지나간 1cm voxel을 기록해 voxel별 점유 확률을 구한 것이 Skill Envelope임. 실패 데이터나 사람 demonstration이 필요 없고, envelope 측정 비용은 skill 쌍이 아니라 skill 수에 비례해 늘어남. agent에게는 두 도구로 제공됨: CHECK는 남은 물체가 차지한 voxel에서 다음 skill envelope 점유 확률의 최댓값이 τ=0.05 이상이면 막힘으로 판정하고, FREE는 남은 skill들의 envelope 밖에서 물체를 옮길 위치를 돌려줌. 막힘이 있으면 서랍 닫기 같은 짧은 analytic primitive로 장면을 고친 뒤 VLA를 실행함.

**결과**

- 640개 전환에서 실행 전 충돌 예측 AUROC는 simulator 상태 기준 0.946이고, RGB-D 카메라 한 대의 depth 차이만 써도 0.944임. 실패 데이터 없이 성공 rollout의 겹침만으로 얻은 값임.
- 다음 skill 성공 여부 예측(429개 전환)에서 envelope 겹침과 re-homing 자세 오차를 성공 확률로 바꾸는 readiness 모델의 AUROC는 0.902임. 이미지만 주거나, 기존 방법 BATON처럼 진입 조건을 언어 규칙으로 적어 물은 VLM 중 최고는 0.793임.
- 2단계 seam 640개에서 CHECK로 막힘을 판정해 코드로 고친 조건의 성공률은 re-homing만 한 82.8%에서 92.3%로 오름. 물체를 순간이동시켜 원위치하는 privileged World Reset은 92.8%임. 서랍 닫기는 π0.5에 언어로 시키면 280회 중 1회, primitive 코드는 140회 중 138회 성공함.
- 서랍이 낀 3~4단계 chain 128개에서 무작위 순서와 re-homing 조합은 29.7%, envelope 기반 순서 선택과 repair는 93.8%, World Reset은 90.6%임.

**한계**

실험은 LIBERO-Goal 시뮬레이션 주방 하나, 고정된 policy π0.5 하나, 서랍 primitive 두 개, offline depth 검사, 미리 정한 deterministic 계획으로만 이뤄졌고 실로봇 결과는 없음. LLM이 CHECK, repair, 실행 절차를 스스로 돌리는 orchestration, 자유 물체를 옮기는 코드 합성, 다른 policy와 어지러운 장면으로의 전이는 저자가 다음 단계 계획으로만 제시함. policy가 매번 같은 궤적을 따른다는 가정에 기대므로, 궤적이 다양한 policy에서 envelope가 얼마나 넓어질지는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- skill chaining과 failure detection/recovery를 실패가 일어나기 전에 다루는 사례임. VLA의 성공 rollout만으로 precondition을 재는 방식은 우리 VLA long-horizon 실험에서 seam 실패 분석 도구로 바로 쓸 수 있음.
- View Reset과 World Reset을 같은 상태에서 비교하는 개입 설계는 counterfactual 원인 분석의 실험 틀로 가져올 만함.

*대표 그림: LLM agent가 서랍 열기 뒤 접시 밀기를 부를 때 seam에서 0/10으로 실패하는 예와, Body·View·World 개입 비교, 팔이 쓸고 지나가는 3D envelope가 열린 서랍과 겹치는 모습, CHECK·FREE 기반 코드 구조를 한 장에 담은 개요도임. 오른쪽 아래 표에 2단계 82.8%에서 92.3%, 3~4단계 29.7%에서 93.8%, 서랍 닫기 0.4%에서 98.6% 같은 본문 수치가 요약되어 있음.*

---

### 14. Verify then Steer: Progress Hallucination-Aware Recovery for Continuous Vision-and-Language Navigation (74점)

[arXiv](https://arxiv.org/abs/2611.32400) · [PDF](https://arxiv.org/pdf/2611.32400) · [alphaXiv](https://www.alphaxiv.org/abs/2611.32400)

- **저자**: Jiewen Hou, Guanxiang Qi, Meina Kan, Shiguang Shan, Xilin Chen
- **분야**: Navigation · robotics relevance 9/10 · 1차 스크리닝 74점
- **읽은 원문**: PDF 전문

> VLM 기반 VLN agent가 경로를 벗어난 뒤 엉뚱한 곳에서 멈추는 실패를, 멈추려는 순간 내부 상태로 실패를 판정하고 앞쪽 시각 기록을 잘라 지시문 진행 위치를 되돌리는 방식으로 test-time에 복구함. VLM을 고정한 채 NaVIDA의 R2R-CE val-unseen 성공률을 61.4%에서 67.0%로 올림.

**무슨 문제인가**

VLM 기반 VLN(vision-and-language navigation) agent는 행동 하나만 틀려도 경로를 벗어나고, 기존 방법은 학습 단계에서 이탈 궤적을 더 모아 imitation learning이나 RL로 복구를 가르침. 저자는 기존 VLM 기반 VLN agent인 NaVIDA의 실패 궤적 100개를 분석해 복구가 안 되는 원인을 progress hallucination이라고 이름 붙임. progress hallucination은 agent가 경로 밖에서 본 장면을 과제 진행의 증거로 잘못 읽어, 내부의 지시문 진행 위치가 실제 단계보다 앞서 나가는 현상임. 진행 위치가 이미 마지막 sub-instruction에 가 있으므로, agent는 앞쪽 sub-instruction을 기준으로 다시 움직이지 못하고 일찍 멈춤.

**어떻게 푸나**

PHAR(Progress Hallucination-Aware Recovery)는 agent 밖에 붙는 test-time 모듈이며 VLM 가중치는 건드리지 않음. 지시문 진행 위치는 첫 action token 직전 위치의 VLM 상태가 각 sub-instruction에 주는 attention 분포로 정의하고, 그 무게중심을 progress pointer라 부름. agent가 STOP을 내면 verifier가 매 decision step의 VLM 상태를 GRU로 누적해 실패 점수를 냄. 이 temporal probe는 학습 궤적의 성공·실패 결과(성공 2,000개, 실패 2,000개)로 학습하고, 경보 임계값은 성공 궤적에 split conformal calibration을 적용해 오경보 수준 3%로 정함. 경보가 뜨면 STOP을 막고 시각 기록의 앞쪽 비율 ρ(0.4~1.0 중 5개)를 지워 progress pointer를 앞 단계로 되돌림. ρ의 선택은 contextual bandit 문제로 보고 LinUCB로 고르며, 입력은 probe 상태와 남은 step 예산이고 reward는 다음 STOP의 verifier 통과 여부와 추가 step 비용으로 정함.

**결과**

- 분석 실험: R2R-CE(연속 3D 실내 환경에서 영어 지시를 따라 목표까지 가는 벤치마크)의 NaVIDA 실패 궤적 100개에서, 경로 밖 기록을 회색 이미지로 바꾸면 91% 이상의 개입에서 progress pointer가 뒤로 감. 같은 100개에 ρ를 하나로 고정하면 최대 28개가 복구되고, ρ를 궤적마다 맞게 고르면 40개까지 복구될 수 있음.
- 주 결과: val-unseen 성공률이 VLM 기반 VLN agent 세 개(NaVILA, NaVIDA, AwareVLN)에서 R2R-CE 기준 6.7, 5.6, 3.3퍼센트포인트 오름. RxR-CE(더 길고 3개 언어 지시가 있는 연속 환경 벤치마크) 기준으로는 10.0, 5.8, 3.0퍼센트포인트 오름. AwareVLN에 붙였을 때 R2R-CE 성공률은 저자 재현값 65.2%에서 68.5%로 오름.
- verifier: 실패 판정 AUROC가 STOP 확률 기반 NLL·entropy의 52% 안팎에서 85.09%(R2R-CE), 88.16%(RxR-CE)로 오름. 종료 시점 상태만 쓰는 MLP는 78.35%, 80.11%임.
- 구성요소 제거(NaVIDA, R2R-CE): 경보 후 기록을 그대로 두고 다시 가게 하면 성공률 63.3%, ρ를 무작위로 고르면 64.7%, PHAR는 67.0%임.

**한계**

실로봇 결과는 Unitree Go2 사족 로봇에서 녹색 의자 두 개를 둔 과제 1개의 성공 사례 1건을 정성적으로 보고한 것이고 반복 횟수나 성공률은 본문에서 확인 불가함. verifier는 agent마다 학습 궤적 4,000개로 따로 학습해야 하고, 경로 효율까지 반영한 성공률인 SPL(success weighted by path length)은 NaVIDA에서 54.7%에서 54.8%로 거의 그대로임. 성공은 늘었지만 복구에 추가 이동이 듦. 방법은 STOP 시점에만 개입하므로 멈추지 않고 헤매는 실패나 시간 예산 소진에는 손대지 못하며, 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- failure detection/recovery를 VLM 내부 상태 probe, conformal 임계값, bandit 기반 개입 선택으로 나눈 test-time 구조임. VLA 조작 policy의 조기 종료나 하위 과제 건너뛰기 실패에 같은 구조를 옮겨 볼 수 있음.
- 시각 기록의 앞부분을 지우는 것이 진행 단계 인식을 되돌린다는 결과는 robot memory 설계에서 기록을 얼마나 남길지 정하는 문제와 이어짐.

*대표 그림: 지도 위의 실패 경로(빨간 점선)와 정답 경로(초록 점선), 그리고 t-2, t-1, t 시점의 관측·sub-instruction별 attention 막대·행동 계획을 시점별 한 줄씩 그린 progress hallucination 설명 그림임. 실제 단계는 S2에 머무는데 attention 최고점이 S3, S4로 넘어가 실내에서 stop을 내는 과정을 보여 주며, 성능 측정 결과가 아니라 현상을 그린 개념도임.*

---

### 15. EffectWAM: Learning Action-Grounded Effects for Robot Manipulation (62점)

[arXiv](https://arxiv.org/abs/2611.32053) · [PDF](https://arxiv.org/pdf/2611.32053) · [alphaXiv](https://www.alphaxiv.org/abs/2611.32053) · [코드](https://github.com/haocui1715/xx-wam-mem-0.5-preview)

- **저자**: Yuan Zhang, Hao Cui, Jingfei Ni, Meiyi Wang, Xin Nie, Chi Liu, Wenjie Xu, Lin Gao 외 6명
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 72점
- **학회**: ByteDance 자체 양식 · 근거: 글꼴 ByteSans, 학회 양식 아님
- **읽은 원문**: PDF 전문

> world-action model이 미래 영상 대신 현재 관측 대비 시각 변화(Effect)를 action과 함께 예측하게 하고, 그 변화 표현을 측정된 end-effector·gripper 변화로 학습시킴. RoboTwin 2.0에서 장면 무작위화가 없는 Clean 데이터만으로 학습했을 때, Clean·무작위화(Randomized) 평가 평균 성공률이 가장 가까운 baseline InternW0-Δ의 81.0%에서 83.02%로 오름.

**무슨 문제인가**

world-action model(WAM)은 action과 함께 미래 영상을 예측해 시각 dynamics를 학습하지만, 결정마다 영상을 합성하면 closed-loop 제어가 느려짐. 영상을 학습 때만 쓰는 Fast-WAM 방식은 지연은 없지만 일반화가 떨어진다는 보고가 있음. 그래서 compact한 latent를 action과 함께 예측하는 쪽이 대안이 되었는데, 이때 latent를 어떤 feature 공간에서 만드느냐가 policy가 무엇을 예측하도록 배우는지를 정함. 고정된 V-JEPA 2.1 같은 video feature는 gripper 개폐나 end-effector의 작은 움직임처럼 제어에 중요한 변화를 보존하도록 감독받지 않음.

**어떻게 푸나**

EffectWAM은 미래 영상 대신 Effect를 예측하는 WAM임. Effect는 미래 프레임 feature에서 현재 프레임 feature를 뺀 차이로 시각 변화를 나타내는 표현임. 학습 때 ViT와 attention pooling 모듈(OBE: observation endpoint encoder)이 현재 프레임과 4·8·12·16 프레임 뒤 프레임을 각각 256차원 벡터로 만들고, 그 차이를 Effect token으로 씀. Action Grounding은 이 차이에서 실제 측정된 end-effector 위치·회전과 gripper 상태 변화를 예측하는 보조 head를 붙여 encoder가 로봇 움직임 정보를 보존하게 하는 손실임. CaPE(camera positional encoding)는 camera extrinsics가 있을 때 현재 대비 상대 camera pose를 pooling의 key에 곱해 camera 움직임과 장면 변화를 구분하게 함. extrinsics가 없는 궤적은 같은 가중치로 pose 없이 pooling함. flow matching이 예측하는 Effect의 정답 target은 encoder의 EMA 사본이 만든 Effect임. semantic expert와 generation expert로 된 mixture-of-transformers가 현재 관측과 instruction을 입력받음. 현재 관측은 학습되는 ViT feature로 semantic expert에, 고정된 video VAE latent로 generation expert에 들어감. 이 모델이 flow matching으로 Effect 시퀀스와 action chunk를 함께 sampling함. 미래 영상은 요청할 때만 같은 generation expert가 sampling된 Effect·action 쌍을 조건으로 생성하므로 제어 경로에서 빠짐. 34개 출처 약 25,293시간의 로봇·사람·egocentric 데이터로 사전학습하고 benchmark마다 적응시키며, 모델은 Small(8B)과 Large(26B) 두 크기임.

**결과**

- RoboTwin 2.0(양팔 조작 50과제, 장면 무작위화 평가 포함)에서 Clean 데이터만으로 학습함. Small의 Clean 성공률은 91.82%, Randomized는 74.22%로 InternW0-Δ보다 각각 1.82, 2.32퍼센트포인트 높음. 평균 83.02%는 PICA-WAM의 82.7%보다도 높음.
- RoboCasa365(주방 시뮬레이션의 단일·복합 과제 50개)에서 전체 성공률이 저자가 직접 돌린 InternW0-Δ의 48.33%에서 49.27%로 오름. 처음 보는 과제 조합(Composite-Unseen)에서는 17.29%에서 19.38%로 올라 개선폭이 가장 큼. 다만 Xiaomi-Robotics-1의 57.4%보다는 낮음.
- RoboDojo(일반화·정밀도·장기 과제·기억·개방형 5개 능력별 42과제)에서 Large의 전체 성공률은 3 seed 평균 34.01%로 VPP2의 32.26%, PrismWAM Large의 29.30%보다 높음. Small은 단일 seed로 27.87%임.
- LIBERO와 LIBERO-Plus(LIBERO에 camera·조명·배치 등 7종 교란을 넣은 판)에서는 99.20%, 93.10%로 InternW0-Δ와의 차이가 각각 0.2, 0.3퍼센트포인트에 그침.

**한계**

모든 평가가 시뮬레이션 benchmark이고 실로봇 실험은 없음. Effect, CaPE, Action Grounding 각각을 빼 보는 ablation이 본문에 없고, 초록에서 말한 여러 baseline에 Action Grounding을 붙인 비교 결과도 본문에서 확인 불가함. 가장 가까운 baseline인 InternW0-Δ와의 차이는 대부분 1~2퍼센트포인트이고 Small은 단일 seed라서, 개선이 Effect 설계에서 온 것인지 데이터·학습 설정 차이에서 온 것인지 가르기 어려움.

**누리랩 연구와의 연결**

- 미래 영상 대신 측정된 로봇 상태 변화로 감독한 시각 변화 latent를 action과 함께 예측하는 설계는, world model 기반 VLA에서 예측 대상을 무엇으로 둘지 정할 때 비교 대상이 됨.
- 결정마다 예측한 Effect와 실제 관측 변화의 차이를 failure detection 신호로 쓸 수 있는지는 저자가 다루지 않았으나 확장해 볼 만함.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. instruction, ViT image token, frozen VAE의 현재 프레임 token이 36층 World-Action Model에 들어감. generation module이 Effect와 action chunk를 내고 미래 영상은 선택적으로 생성하는 흐름을 보여 줌.*

---

## 오늘의 흐름

- **world action model의 예측 대상 바꾸기**: 미래 영상 전체를 만드는 대신 행동에 필요한 것만 예측하는 world action model이 여럿 나옴. 미래 영상을 만들지 않고 행동만 뽑거나([G0.7](https://arxiv.org/abs/2611.31822)), 물체 역할별로 예측 정밀도를 나누거나([FoveaWAM](https://arxiv.org/abs/2611.31705)), 로봇 상태 변화로 감독한 시각 변화를 예측함([EffectWAM](https://arxiv.org/abs/2611.32053)).
- **world model을 optimizer가 아니라 평가자로 쓰기**: world model 안에서 행동을 gradient로 고치는 대신, 후보 행동을 rollout으로 비교해 고르는 데 씀([CriticJEPA](https://arxiv.org/abs/2611.32357)). 상상 rollout 속 PPO와 critic 기반 best-of-N으로 policy를 고치기도 함([DexWAC](https://arxiv.org/abs/2611.32654)).
- **VLA 실패를 원인별로 쪼개 진단하기**: 실패율만 보고하지 않고 attention 경로 차단, 단계별 개입, 3D 경로 측정, LLM의 병목 단계 진단으로 실패 원인을 가름. [Seeing Is Not Reaching](https://arxiv.org/abs/2611.32206), [Ground, Guide, Act](https://arxiv.org/abs/2611.31452), [3D Skill Envelopes](https://arxiv.org/abs/2611.32245), [ReFocus](https://arxiv.org/abs/2611.32639)가 여기에 속함.
- **고정된 policy를 test-time에 고치기**: π0.5나 VLM 가중치를 그대로 두고 critic guidance, sampling guidance, 앞쪽 시각 기록 지우기로 실행 중 행동만 바꿈. [RetraQ](https://arxiv.org/abs/2611.32148), [Seeing Is Not Reaching](https://arxiv.org/abs/2611.32206), [Verify then Steer](https://arxiv.org/abs/2611.32400)가 이 방식임.
- **데이터 출처와 embodiment 넓히기**: 사람 영상, 다른 로봇, 절차적으로 만든 팔 80만 개, 일부러 방해한 시연처럼 기존 시연과 다른 데이터로 policy를 넓힘. [Any2Act](https://arxiv.org/abs/2611.32353), [OmniAct](https://arxiv.org/abs/2611.33158), [Exploratory Midtraining](https://arxiv.org/abs/2611.33130)이 이 흐름임.

## 해볼 만한 연구

### world model rollout으로 VLA action chunk 고르기

- 질문: π0.5가 낸 여러 action chunk를 world model rollout으로 비교해 고르면, 위치가 바뀐 장면에서 실패를 실행 전에 피할 수 있는지 밝힘.
- 첫 실험: LIBERO-PRO(LIBERO 과제에 물체 위치·목표·문장 교란을 건 benchmark)의 위치 교란 과제에서 실험함. π0.5 sample N개를 action-conditioned world model로 rollout해 목표 도달 비용이 가장 낮은 것을 고른 경우를 비교함. 비교 대상은 무작위 선택, PSG(경로별 sampling guidance), Q critic 기반 선택임.
- 가장 가까운 연구: [CriticJEPA](https://arxiv.org/abs/2611.32357)는 같은 구조를 시뮬레이션 maze, 큐브 조작, Push-T에서만 보였고 VLA의 action chunk에는 적용하지 않았음. [RetraQ](https://arxiv.org/abs/2611.32148)는 world model 대신 Q critic으로 action을 고침.

### VLA 내부 상태로 하위 과제 건너뛰기 실패 감지하기

- 질문: VLN에서 쓴 내부 상태 probe와 conformal 임계값(성공 궤적으로 오경보율을 정해 둔 경보 기준)이 조작 VLA의 조기 종료와 하위 과제 건너뛰기도 잡아내는지 밝힘.
- 첫 실험: LIBERO-Long(탁상 다중 물체 장기 과제 10개)에서 π0.5 hidden state에 probe를 학습해 하위 과제 완료 오판을 탐지함. 탐지 정확도와 복구 뒤 성공률을 ReFocus식 하위 과제 완료 판정과 비교함.
- 가장 가까운 연구: [Verify then Steer](https://arxiv.org/abs/2611.32400)는 내비게이션에서 STOP 시점에만 개입함. 조작 과제의 중간 단계 실패는 다루지 않음.

### 진단된 실패 지점에 맞춰 recovery 데이터 모으기

- 질문: 단계별 개입으로 찾은 실패 지점에 방해를 몰아서 모은 데이터가, 같은 양의 무작위 방해 데이터보다 recovery 행동을 더 늘리는지 밝힘.
- 첫 실험: 일부 단계만 정답 동작으로 대신 움직여 보는 단계별 개입으로 π0.5의 실패 단계를 찾음. 그 단계에 방해를 집중한 데이터와 무작위 방해 데이터로 각각 midtraining(사전학습 뒤 과제 fine-tuning 전에 하는 추가 학습)함. 같은 과제 묶음에서 성공률과 재시도 횟수를 비교함.
- 가장 가까운 연구: [Exploratory Midtraining](https://arxiv.org/abs/2611.33130)은 어디를 방해할지 사람 판단에 맡김. [Ground, Guide, Act](https://arxiv.org/abs/2611.31452)는 진단 결과를 주로 MFM(multimodal foundation model)과 VLA의 역할 분담에 씀.

## 꼭 읽을 논문

- [Any2Act](https://arxiv.org/abs/2611.32353): 사람 영상과 다른 로봇 시연을 실행 로봇 형식으로 옮겨, 처음 보는 실로봇 과제를 시연 1개로 따라 하는 구조임.
- [Seeing Is Not Reaching](https://arxiv.org/abs/2611.32206): π0.5가 물체를 attention으로 찾고도 instruction 경로 때문에 학습 때 위치로 가는 현상을 경로 차단 실험으로 보임.
- [RetraQ](https://arxiv.org/abs/2611.32148): 고정된 behavior cloning flow로 critic gradient를 거르고 action을 데이터 근처로 되돌려, π0.5의 행동을 파라미터 수정 없이 실로봇에서 고침.
- [OmniAct](https://arxiv.org/abs/2611.33158): 절차적으로 만든 팔 약 80만 개로 학습해 처음 보는 팔에도 policy 하나로 대응함. 팔 구조 graph의 기여는 시뮬레이션에서 5.1퍼센트포인트임.
- [FoveaWAM](https://arxiv.org/abs/2611.31705): 추론 지연까지 포함해 움직이는 물체 조작을 평가하는 benchmark와 역할별 4D 예측을 함께 제시함.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (675편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2611.32148'>RetraQ: Manifold-Constrained Critic Guidance for Flow Policies in RL</a></td><td>83</td><td>10</td><td>RL</td><td>사전학습 flow policy의 denoising map으로 critic gradient를 접선 방향으로 걸러 데이터 manifold로 retraction하는 RetraQ. 실로봇 plug insertion에서 π0.5가 55.0%에서 76.7%로, online RL로 100%에 도달함. LIBERO와 OGBench에서도 baseline보다 높음. 이론과 실로봇 증거가 함께 있음.</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2611.31588'>One Phase Is Enough: Sim-to-Real Transfer with Direct Visual Reinforcement Learning</a></td><td>79</td><td>10</td><td>RL</td><td>frozen pretrained vision encoder로 teacher-student distillation 없이 one-phase visual RL을 sim-to-real 전이함. 실로봇 조작 3과제에서 two-phase 대비 평균 성공률이 58.8% 상대 향상. 단순한 recipe이나 증거가 직접적임.</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2611.32206'>Seeing Is Not Reaching: Instruction Shortcuts Override Visual Grounding in Vision-Language-Action Models</a></td><td>78</td><td>10</td><td>VLA</td><td>6개 VLA에서 instruction shortcut이 시각 grounding을 덮어씀을 두 pathway masking으로 규명하고 학습 없는 PSG로 LIBERO-PRO 물체 이동 조건 성공률을 16.6%에서 40.8%로 올림. VLA 실패 원인 진단과 inference-time 개입이라 우선 주제에 정확히 맞고 인과적 분석이 강함. 시뮬레이션 중심이고 개선 후에도 절대 성공률은 낮음.</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2611.32353'>Any2Act: Scaling In-Context Robot Learning from Heterogeneous Demonstrations</a></td><td>78</td><td>10</td><td>VLA</td><td>demonstration을 demonstrator가 아닌 executor의 카메라 배치와 action space로 표현한다는 통일 표현이 핵심임. 1.2M 궤적으로 한 번 학습하고 human video·UMI는 소량 adapter로 흡수해, 1개 demonstration으로 미지 과제 57.5%를 내 과제별 50개 fine-tuned VLA를 넘음</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2611.32654'>DexWAC: A Unified World-Actor-Critic Model for Dexterous Robot Manipulation</a></td><td>78</td><td>10</td><td>World Model</td><td>actor, action-conditioned world model, bootstrapped critic을 한 번의 pretraining으로 통합 학습하고 action chunk 끝점만 예측해 imagined rollout을 효율화함. 상상 PPO나 best-of-N으로 개선해 실로봇 2과제 평균 75%로 π0.5 45%를 넘음</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2611.32357'>CriticJEPA: World Models Are Better Critics Than Optimizers</a></td><td>77</td><td>9</td><td>World Model</td><td>world model이 prolonged gradient 최적화보다 goal-conditioned flow proposal의 ranking에 더 신뢰할 만하다는 관찰로 critic 방식 planner CriticJEPA를 제안함. 시각 navigation과 조작에서 planning 연산을 줄이며 성공률이 오름. test-time planning 관점에서 새롭고 world model 가중치를 고정함.</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2611.31452'>Ground, Guide, Act: Improving VLA Spatial Generalization with Multimodal Foundation Models</a></td><td>76</td><td>10</td><td>VLA</td><td>VLA 실패를 atomic-stage intervention으로 분석해 target grounding과 공간 routing이 병목임을 밝히고, MFM이 grounding을 맡고 VLA가 정밀 조작을 맡는 router 구조를 제안함. LIBERO-PRO 등 4개 환경과 실로봇에서 개선을 보이나 router가 development set 보정에 의존함</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2611.33158'>OmniAct: One Policy, One Million Embodiments</a></td><td>76</td><td>10</td><td>Manipulation</td><td>로봇 kinematic graph에 직접 조건화하는 flow-matching 정책을 100만 procedurally 생성한 embodiment로 학습함. held-out 2,000 에피소드 63.0%로 π0.5의 17.8%를 크게 넘고 미지 실로봇에서도 우위를 보임. 시뮬레이션 학습 위주 증거임</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2611.32245'>VLAs Execute, Code Recovers: 3D Skill Envelopes Bridge the Compositional Gap in Agentic Manipulation</a></td><td>76</td><td>9</td><td>VLA</td><td>frozen VLA가 습관적 궤적을 따른다는 것을 causal intervention으로 밝히고 3D skill envelope로 충돌을 AUROC 0.946으로 예측해 코드로 복구하며 3-4단계 chain 성공률을 29.7에서 93.8%로 올림</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2611.31822'>G0.7: Scaling Up a Fast World Action Model with Long Context</a></td><td>74</td><td>10</td><td>World Model</td><td>WAM을 5분 context와 로봇 teleoperation 및 ego video 사전학습으로 scale함. 미래 프레임 합성 없이 60ms에 action chunk를 내면서 imagine-then-act와 같은 성능이고 human ego video가 OOD 일반화를 가장 크게 올림. 실로봇 7개 과제 평균 진행도 86.9%이나 Fast-WAM 위의 scale-up 성격이 강함</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2611.33130'>Exploratory Midtraining for Robot Policies</a></td><td>74</td><td>10</td><td>Imitation Learning</td><td>적대적 teleoperation으로 교란과 복구를 담은 β-Data로 midtraining해 연결된 행동 coverage를 늘림. 데이터 scaling, zero-shot 일반화, online finetuning 효율이 좋아졌다고 시뮬과 실로봇 3종에서 보임. 자율 개선 관점의 새 데이터 formulation임</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2611.32400'>Verify then Steer: Progress Hallucination-Aware Recovery for Continuous Vision-and-Language Navigation</a></td><td>74</td><td>9</td><td>Navigation</td><td>VLN 에이전트가 경로 이탈 관측을 진행으로 오인하는 progress hallucination을 규명하고, VLM residual stream 검증기와 split conformal 보정, contextual bandit rewind로 test-time 복구하는 PHAR를 제안함. 실패 진단과 복구, inference-time 개입이라 우선 주제에 잘 맞음. 개선폭은 초록에서 확인 불가이고 R2R-CE, RxR-CE 시뮬레이션만 평가함.</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2611.31705'>FoveaWAM: Role-Aware 4D World-Action Modeling for Dynamic Manipulation</a></td><td>74</td><td>9</td><td>World Model</td><td>역할별로 대상 SE(3) 궤적과 주변 sparse 3D flow만 예측해 15.1ms로 동작하며 동적 조작 OnTimeBench에서 20.8포인트 앞서므로 latency를 고려한 world action model 설계가 참신함</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2611.32639'>ReFocus: Progress-Guided Adaptive Practice for Long-Horizon Robotic Manipulation Reinforcement Learning</a></td><td>72</td><td>10</td><td>RL</td><td>task를 subtask DAG로 쪼개 progress reward로 병목을 진단하고 그 구간만 추가 연습하는 VLA online RL임. LIBERO-Long 90.6→97.8%, RoboCasa365 39.3→51.3%, 실로봇 BreadBaker 30→95%로 π0.5 대비 증거가 강함</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2611.32053'>EffectWAM: Learning Action-Grounded Effects for Robot Manipulation</a></td><td>72</td><td>10</td><td>World Model</td><td>시각 변화를 현재 관측 anchor와의 차이(Effect)로 표현하고 action chunk와 flow matching으로 함께 예측하는 world-action model임. 2만 시간 이상 embodied 데이터와 5개 manipulation benchmark 평가가 강점이나 초록만으로 개별 수치와 실로봇 증거는 확인 불가함</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2611.31740'>LeanWAM: Learning Latent World Action Models from Frozen Video Models</a></td><td>72</td><td>9</td><td>World Model</td><td>WAM이 정책에 필요한 미래 표현을 probing으로 분석해 32개 token으로 압축하고 frozen video generator에서 경량 정책으로 distillation함. 1.4B로 LIBERO, RoboTwin 2.0에서 강한 baseline을 넘고 추론이 12.3-41.5배 빠름. 실로봇 검증은 초록에서 확인 불가</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2611.31850'>Two-Stage Post-Training for Flow-Based Embodied Foundation Models</a></td><td>72</td><td>9</td><td>VLA</td><td>flow-based embodied model에 multi-teacher distillation 후 실패 trajectory에만 teacher distillation을 더한 RL로 teacher 합산 성공률을 넘김. VLA post-training 설계로 실용적이나 시뮬레이션 벤치마크 중심으로 보임.</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2611.31894'>RESET: One Demonstration, One Verified World, Self-Improved Skills Across Embodiments</a></td><td>72</td><td>9</td><td>Manipulation</td><td>실제 시연 하나에서 world와 성공 기준을 재구성하고 코딩 agent가 skill을 자기개선해 시뮬레이션 97%, 실로봇 4대 280회 80% 성공을 얻으며 이종 로봇 전이까지 보여 설계가 강함</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2611.31511'>Near-Zero Forgetting Is Not Enough: Out-of-Distribution Robustness in Continual Learning of Pretrained VLAs</a></td><td>70</td><td>9</td><td>VLA</td><td>Pi0 continual learning에서 in-domain forgetting이 거의 0이어도 OOD 성능이 무너지고 multimodal·action feature drift로 설명함. workshop 규모의 진단 연구이나 VLA 배포 문제를 정확히 짚음.</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2611.32260'>EgoLoAF: Learning Humanoid Loco-Manipulation from Egocentric Demonstrations with Hand-Object Affordances</a></td><td>70</td><td>9</td><td>VLA</td><td>착용형 tracker와 teleoperation 없이 egocentric 영상만으로 humanoid VLA를 post-training하고 hand-object affordance를 action expert에 cross-attention으로 넣음. 실로봇 4과제에서 teleoperation 73.1 대 74.4에 근접하고 1,000시간 데이터를 공개함</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2611.31954'>Perception Is Enough, at the Right Scale: Scale-Adaptive Token Pruning for Vision-Language-Action Models</a></td><td>70</td><td>9</td><td>VLA</td><td>VLA token pruning의 semantic scale을 perception temperature τ로 온라인 조절하고 pruning을 비동기로 돌려 1.86배 속도를 얻음. training-free이고 실로봇 2종 검증이 있어 실용성이 높으나 개념적 도약은 중간임</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2611.31715'>Sparks of Weight-Space Programming for Robot Foundation Models</a></td><td>68</td><td>9</td><td>VLA</td><td>LLM agent가 pi0.5의 거의 쓰이지 않는 뉴런 약 0.0002%를 직접 써서 반복 실패를 교정하는 weight-space programming으로 failure recovery 관점이 새로우나 시뮬레이션만 평가함</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2611.32256'>RoboDemo: Reconciling Demonstration Intent and Execution Progress for Long-Horizon Manipulation</a></td><td>68</td><td>9</td><td>Manipulation</td><td>Dual test-time-training fast-weight memory로 demonstration 의도와 실행 진행을 분리해 저장하는 long-horizon 구조가 참신함. Imitator Game 90.7%, 실로봇 3과제 73.3%지만 baseline 대비 격차는 초록에서 확인 불가임</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2611.32786'>Simulator-as-Proxy World Model for Robot Manipulation</a></td><td>68</td><td>9</td><td>World Model</td><td>simulator 상태를 명시적 proxy로 두고 물체 상태를 고정하는 intervention으로 video world model이 proxy를 실제로 따르는지 검증함. 팔은 따르지만 물체는 base model에 따라 다르다는 counterfactual 진단이 가치 있음</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2611.32152'>RoboProbe: Benchmarking Physical Plausibility of Robot World Models</a></td><td>68</td><td>8</td><td>World Model</td><td>로봇 world model이 만든 영상의 물리 타당성을 접촉·물체 지속성 등 5개 법칙별 metric과 agentic 평가로 검증하고 RP-Bench(761개 라벨 영상)에서 AUROC 0.85 이상을 보임. world model 기반 계획의 신뢰성 평가 도구로 유용하나 benchmark 성격임.</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2611.32776'>Learning World Models through Contrastive Identification of Actions</a></td><td>68</td><td>8</td><td>World Model</td><td>latent world model에서 behavior proposal 속 대안 행동 중 실행된 행동을 contrastive하게 식별해 행동 정보를 보존시킴. regression inverse dynamics가 놓치는 정보를 보이는 이론 근거와 5개 시각 제어 benchmark 개선이 있으나 시뮬레이션 위주로 보임</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2611.32705'>Knocked Off Course: Tracing Uncommanded Motion from Perception to Action in Embodied VLAs</a></td><td>66</td><td>9</td><td>VLA</td><td>tracking VLA 3종이 바람, 지형 같은 uncommanded egomotion에서 어디서 실패하는지 pixel에서 action까지 추적해 representation gap과 action gap을 찾아냄. 원래 학습 데이터 1.7%만으로 Uni-NaVid를 fine-tuning해 target-loss 후 성공률이 5~22점 오름. failure diagnosis 방식이 우리 주제와 맞음</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2611.32967'>VidForce: Predicting Force-Aware Articulation by Observing Humans</a></td><td>66</td><td>9</td><td>Manipulation</td><td>third-person 비디오에서 interaction trajectory와 force profile을 함께 추정하고, 장비 측정 force를 learned prototype prior로 활용함. 추정된 trajectory와 force로 Spot 로봇의 articulated object manipulation을 구동한 실로봇 결과까지 있음. human video에서 force를 얻는 점이 신선하나 성공률 수치는 초록에서 확인 불가임</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2611.32665'>DiffGR00T: Execution-Aware Differentiable Training for Humanoid Whole-Body Vision-Language-Action Models</a></td><td>66</td><td>9</td><td>VLA</td><td>고정된 whole-body controller 뒤에서 learned world model로 simulator를 대체해 execution loss를 VLA action head까지 역전파하는 구조가 새로움. HumanoidArena 4과제 평균 59.2→71.7%지만 시뮬레이션만 확인함</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2611.32797'>Supply Geometry, Learn Execution: Screw Attention for Zero-Shot Policy Transfer in Robot Manipulation</a></td><td>66</td><td>9</td><td>Manipulation</td><td>객체 pose, 상대 SE(3), joint screw axis를 명시 입력으로 주고 실행만 학습하는 30K 파라미터 정책임. LIBERO 96%, 미지 로봇 팔 5종 80.2%, 실로봇 24회 중 21회로 zero-shot embodiment 전이를 보여 기하 입력의 가치를 주장함</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2611.33141'>iWAM: Efficient Action Prediction from World Models without Explicit Future Prediction</a></td><td>66</td><td>9</td><td>World Model</td><td>미래 프레임을 생성하지 않고 flow-matching 역변환과 bidirectional flow map으로 video backbone 1회 forward만으로 action을 조건화하는 WAM임. 추론 비용을 크게 줄이면서 일반화 이점을 유지한다고 주장하나 정량값은 초록에서 확인 불가임</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2611.32304'>Sparse Poison, Strong Hijack: Efficient Trajectory-Level Backdoors in Vision-Language-Action Models with Only 1\% Poisoning</a></td><td>66</td><td>9</td><td>VLA</td><td>VLA에 1% 오염 데이터로 trajectory 수준 backdoor를 심는 공격으로 3D trigger 최적화와 dual-LoRA를 씀. OpenVLA, π0, π0.5와 실로봇 hijack까지 보여 VLA 안전성 문제를 구체화하나 공격 논문이라 방어 기여는 없음</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2611.32198'>MoGe-4D: Efficient, Flexible, and Unified Dense 4D Reconstruction and Tracking</a></td><td>66</td><td>6</td><td>3D Vision</td><td>동적 장면의 geometry와 dense 3D tracking을 egocentric/allocentric point map 질의로 feed-forward 통합하고 RigIDTrack 데이터로 감독함. 4D 표현과 tracking은 object-centric 4D 인식에 쓸모 있으나 로봇 실험은 없음.</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2611.32884'>Lazy Agents Answer Against Their Own Beliefs: Reinforcement Learning with Verifiable Beliefs Teaches Them to Act on What They Believe</a></td><td>66</td><td>6</td><td>RL</td><td>simulator의 정확한 posterior로 충분한 근거가 모일 때까지 탐색하고 commit하게 하는 RLVB를 제안함. 부분 관측 VLM agent의 active evidence 탐색으로 일반화 가능하고 9개 설정 모두 개선하나 로봇 실험은 없음</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2611.31910'>ReJEPA: Bounded Predictive Regulation for Latent World Models</a></td><td>65</td><td>7</td><td>World Model</td><td>latent world model 학습 loss를 L2에서 log-cosh로 바꾸면 V-JEPA 2.1 등에서 조작과 NAVSIM 주행까지 이득이 커진다고 보임. 한 줄짜리 loss 교체라 기여가 작으나 world model 학습 안정성에 실용적 시사가 있음.</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2611.33010'>Embodied AI Fails the Mirror Test: How a Simple Mirror Breaks Robot Policies</a></td><td>64</td><td>9</td><td>Manipulation</td><td>거울이 있는 장면에서 VLA, World Action Model, agentic policy 5종의 성공률이 10.8~56.7퍼센트포인트 하락함을 보임. 거울이 단순 장애물이 아니라 반사된 물체를 목표로 삼는 현상을 접촉 분석으로 확인하고 실로봇에서도 확인함. benchmark이지만 failure diagnosis 관점이 명확함</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2611.32226'>Relation Before Action: Explicit Relation Modeling for Latent Action Pretraining</a></td><td>64</td><td>8</td><td>Embodied AI</td><td>latent action 사전학습에서 전이의 relation 구조 모델링과 action 추상화를 분리하는 RELACT를 제안함. 내비게이션과 goal-conditioned manipulation planning에서 이득을 보였다 하나 수치는 초록에서 확인 불가임. latent action 설계가 VLA 사전학습과 직결됨.</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2611.32445'>A Mesh to Remember: Persistent Appearance for Interactive Video Worlds</a></td><td>64</td><td>6</td><td>World Model</td><td>mesh를 주소로 삼아 표면별 feature를 저장하고 재방문 시 불러오는 causal video renderer M2R임. 합성 데이터만으로 학습해 실내 스캔에 zero-shot 전이하고 object permanence를 두 배 이상, 40 FPS 실시간 렌더함. 영속 appearance memory 설계가 world model 장기 일관성에 직결되나 로봇 policy 평가는 없음.</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2611.32017'>Learning Agent States for Latent Action Modeling</a></td><td>62</td><td>9</td><td>World Model</td><td>latent action model이 배경과 agent 외형에 끌리지 않고 agent 상태를 배우도록 spatially matched temporal discrimination을 제안함. distracting control과 실로봇 영상 6종에서 action 복원, 제어, world model 예측 개선을 보임. 정책 사전학습 규모의 검증은 확인 불가</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2611.31535'>Hi3R-VLA: Grounding Semantics and Actions in 3D</a></td><td>62</td><td>9</td><td>VLA</td><td>vision, language, action을 point cloud 3D 좌표계에 정렬하는 3D VLA로 5개 benchmark에서 250M 미만 파라미터로 SOTA를 주장하나 구조는 점진적 조합 성격임</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2611.32081'>KeyMemVLA: Subtask-Guided Key Memory for Long-Horizon Robotic Manipulation</a></td><td>62</td><td>9</td><td>VLA</td><td>subtask 기반 keyframe으로 VLA의 memory 쓰기 시점을 학습해 장기 조작 history 의존 과제를 푸는 robot memory 방법이며 KMBench를 추가하고 실로봇을 포함함</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2611.32101'>Ego2Real: Learning Bimanual Dexterous Manipulation from Egocentric Visuo-Tactile Demonstrations</a></td><td>62</td><td>9</td><td>Manipulation</td><td>촉각 장갑 시연으로 hand-object 재구성을 보정하고 접촉 보상 RL로 dexterous hand에 전이해 tactile 활용이 새로우나 수치는 초록에서 확인 불가함</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2611.32476'>ViTacLab: Physically Consistent Visuo-Tactile Simulation, Benchmarking, and Representation Learning for Robotic Manipulation</a></td><td>62</td><td>9</td><td>Manipulation</td><td>PhysX contact solver에 정합한 tri-modal tactile 시뮬레이션, gripper·dexterous hand·bimanual을 아우르는 benchmark와 policy를 함께 냄. 법선·접선 힘 RMSE를 2.31/1.85N에서 0.42/0.53N으로 낮췄으나 촉각 중심 과제 성공률은 여전히 낮음</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2611.32622'>RoboRecast: Intent-Preserving Demonstration Augmentation via Diagnosis-Driven Optimization</a></td><td>62</td><td>9</td><td>Manipulation</td><td>시뮬레이션 피드백으로 실패 원인을 진단하고 scene·motion 파라미터를 고치는 agentic demonstration augmentation임. 새 배치·물체·embodiment로 옮기는 범용성이 장점이나 구체 수치는 초록에서 확인 불가임</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2611.32218'>PoseVLN: Learning Geometric State Evolution for Vision-Language Navigation</a></td><td>62</td><td>9</td><td>Navigation</td><td>VLN에서 다음 K개 행동과 ΔPose를 함께 예측해 기하 상태를 재귀 전파함. 단일 RGB로 R2R-CE, RxR-CE 성공률이 2.6, 2.9퍼센트포인트 높으나 개선폭은 작고 module 성격이 있음</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2611.32649'>ICLWorld: Benchmarking In-Context Learning of Agents from Digital to Physical Worlds</a></td><td>62</td><td>8</td><td>Embodied AI</td><td>computer use와 robot use를 잇는 online ICL benchmark로 160개 과제를 구성함. 규칙을 98% 맞히고도 로봇 과제는 20%만 수행하는 identify-act 격차를 보여 줌. benchmark이지만 frontier agent 평가 설계가 충실함</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2611.32944'>DynaMimic: A Physics-Informed World Model for Humanoid Motion Tracking</a></td><td>62</td><td>8</td><td>World Model</td><td>contact wrench와 residual force를 예측해 Lagrangian forward dynamics로 다음 상태를 계산하는 physics-informed world model임. SuperMimic 대비 LAFAN1 MPJPE 18.6% 감소와 A3 실로봇 cartwheel 등으로 증거가 탄탄하나 humanoid tracking 범위임</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2611.32297'>MaskedVGGT: Masked Multi-View Transformers Are Scalable 3D Learners</a></td><td>62</td><td>5</td><td>3D Vision</td><td>frozen 2D encoder 위에서 multi-view transformer만 masked self-distillation으로 사전학습해 supervised VGGT-Omega와 E-RayZer 등을 앞섬. 라벨 없는 3D 사전학습의 분업 설계가 설득력 있고 3D 표현 기반으로 쓸 만하나 로봇 실험은 없음.</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2611.32016'>RoboHarness-RL: Agentic Reinforcement Learning for VLM-Based Robot Manipulation</a></td><td>60</td><td>8</td><td>VLA</td><td>VLM이 tool call로 조작하도록 multi-turn RL을 적용해 RoboTwin 2.0에서 31.2에서 44.0%로 올리며 compact VLM harness의 RL 학습을 보이나 절대 성능은 낮음</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2611.32858'>What Does a Skill Vocabulary Cost? A Closed-Loop Decomposition over Demonstrated Motions</a></td><td>60</td><td>8</td><td>Imitation Learning</td><td>정책 뒤에 시연 동작 library를 두고 가장 가까운 항목으로 치환하는 MPQ로, 이산 skill 정책의 실패 원인을 선택·배치·보정으로 분해함. 7B VLA 포함 6개 구조에서 원 정책과 동등하고 offline 재구성 지표가 격차를 예측 못 한다는 진단이 유용함</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2611.31903'>Beyond Expert Replay: Cross-Instruction Anchoring for Continual Vision-Language-Action Learning</a></td><td>58</td><td>9</td><td>VLA</td><td>limited replay에서 옛 instruction이 새로 배운 목표를 유발하는 실패를 관찰하고, 이전 policy를 teacher로 old instruction과 현재 관측의 응답을 맞추는 XIA를 제안함. 여러 VLA와 LIBERO, RoboCasa, 실로봇에서 forgetting 감소를 보이나 distillation 항을 더한 수준의 방법임</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2611.31901'>PreWAM: Exploring the Design of Latent Future Prediction for World-Action Modeling</a></td><td>58</td><td>9</td><td>World Model</td><td>DINO feature 공간에서 잔차와 시간 척도 예측을 쓰는 world action model로 여러 benchmark와 실로봇을 평가하나 설계 탐색 성격이 강함</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2611.33144'>PyRUA-Dex: Learning Programmatic Policies for Dexterous Bimanual Manipulation with Coding Agents</a></td><td>58</td><td>9</td><td>Manipulation</td><td>coding agent가 demonstration 없이 양손 dexterous programmatic policy를 탐색·증류함. Bench2Dex 72.9, DexJoCo 81.0%로 학습 정책을 넘고 22-DoF 양손 실로봇 시연을 보임. 학습이 아닌 프로그램 정책이라 일반화 범위는 확인 불가임</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2611.32650'>LaWanle: Why Can&#x27;t Leading Driving Models Make a Simple Turn?</a></td><td>58</td><td>8</td><td>Embodied AI</td><td>SOTA end-to-end 주행 모델이 NAVSIM에서는 높지만 폐루프 90도 회전을 못 하는 현상을 진단하고 DAgger post-training으로 통과율을 19%에서 76%로 올림. open-loop 점수와 closed-loop 실패 괴리를 보인 분석이 가치 있음. 시뮬레이션 한정임</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2611.32369'>Visual-State Graph Memory for Streaming Video Understanding</a></td><td>58</td><td>6</td><td>Video</td><td>스트리밍 영상 기억을 객체-관계 그래프와 이벤트 로그(동적 scene graph)로 저장하는 training-free 메모리 VSG임. 고정 입력 예산에서 과거 추론을 개선했다 하나 수치는 초록에서 확인 불가임. robot memory와 scene graph 주제에 직접 연결됨.</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2611.31782'>Many Senses, One World: Learning Hierarchical Multimodal World Representations for Bimanual Dexterous Manipulation</a></td><td>56</td><td>9</td><td>Manipulation</td><td>촉각, force-torque, 오디오를 통합한 계층적 world-state 표현으로 양손 5개 실로봇 과제에서 강한 baseline보다 32.0포인트 높음</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2611.32564'>MXI-MemICL: Towards In-Context Robot Manipulation through Self-Retrieved Interaction Memory</a></td><td>56</td><td>9</td><td>VLA</td><td>demonstration과 완료된 상호작용을 retrievable memory로 두고 intention predictor로 질의하는 VLA in-context 방식임. RoboCasa365 +8.2%, RoboTwin 2.0 +14.4%, 실로봇 +9.0%로 개선 폭은 중간 수준임</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2611.32098'>ActiveBridge: Scaling Active Prior for Robots through Egocentric Perception-Interaction Modeling</a></td><td>56</td><td>8</td><td>World Model</td><td>사람 egocentric 영상에서 머리 시점 행동을 포함한 active prior를 world action modeling으로 전이해 active perception을 학습하나 초록에 수치가 없음</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2611.32228'>Disentangling Visual Dynamics for World Model Planning</a></td><td>56</td><td>8</td><td>World Model</td><td>counterfactual 쌍으로 agent와 외생 dynamics를 분리하는 FactorWorld로 world model planning의 성공률을 높이나 MiniGrid와 Push-T 등 시뮬레이션만 평가함</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2611.32533'>Next-Manip: On-Demand Agent-Policy Collaboration for Robotic Manipulation</a></td><td>55</td><td>9</td><td>Manipulation</td><td>agent와 policy 중 누가 실행할지를 가벼운 classifier로 정해 agent 추론 비용을 줄이는 협업 구조임. failure recovery와 연결되나 구체 수치가 초록에 없고 컴포넌트 조합 성격이 강함</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2611.32119'>CoverMem: Coverage-Constrained Visual Memory for Budgeted Embodied Question Answering</a></td><td>55</td><td>7</td><td>Embodied AI</td><td>embodied QA의 episodic 시각 memory를 coverage 제약으로 구성, 증분 갱신, 예산 내 프레임 선택함. robot memory 주제와 직접 닿고 3개 benchmark 검증이나 개선은 예산 조건 위주임</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2611.32645'>TeamFlowRL: Online Policy Optimization of Decentralized Flow Policies for Multi-Agent Coordination</a></td><td>55</td><td>6</td><td>RL</td><td>분산 flow policy를 denoising trajectory 전체에 대해 team advantage로 online fine-tuning하는 MARL이며 양손 조작 6개 과제에서 Gaussian 대비 성공률이 오름</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2611.32483'>CodeWAM: A Code World Action Model for End-to-End Autonomous Driving</a></td><td>55</td><td>6</td><td>World Model</td><td>실행 가능한 code를 driving world model의 ego dynamics 표현으로 쓰는 시도가 새로움. NAVSIM v1 93.6 PDMS를 내지만 자율주행 한정이고 benchmark 점수 개선 성격이 큼</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2611.32238'>Boundary-Aware Policy Learning for Agent-Orchestrated Robot Manipulation</a></td><td>54</td><td>8</td><td>Manipulation</td><td>agent와 visuomotor policy 사이 handoff boundary를 명시적으로 학습하고 넓혀 RoboTwin 2.0에서 98.4% 성공하고 API 비용을 41.3% 줄임</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2611.31658'>Collision Rendering: GPU-Accelerated Trajectory Planning on Sparse Voxel Radiance Fields with Risk-Bounded Collision Checking</a></td><td>54</td><td>7</td><td>3D Vision</td><td>sparse voxel radiance field의 렌더링을 충돌 확률 상한 근사기로 써서 risk-bounded 충돌 검사와 미분 가능 cost를 얻는 점이 신선하나 정적 장면 계획 한정임</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2611.31689'>GeoMVGen: Joint Appearance-Geometry Modeling for Multi-View Video Generation in Robotic Manipulation</a></td><td>52</td><td>8</td><td>World Model</td><td>로봇 조작용 multi-view RGB와 pointmap 비디오를 함께 생성하는 video diffusion 모델임. 기하 일관성을 다루는 점은 world model 관점에서 유효하나 기술 보고서 수준이고 정책 활용 검증이 약함</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2611.32241'>Motion Chain of Thought: Disentangling Motion Semantics from Visual Appearance for Robotic Manipulation</a></td><td>52</td><td>8</td><td>VLA</td><td>상태 전이 토큰을 motion chain of thought로 두어 world action model의 표현 얽힘을 줄이나 초록에서 구체적 수치를 확인할 수 없음</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2611.32534'>EmbodiedStudio: A Task-Driven Simulation Generation Platform for Embodied Learning and Evaluation</a></td><td>52</td><td>8</td><td>Embodied AI</td><td>scene·task·behavior·rubric 프로그램을 closed-loop 시뮬레이션 피드백으로 공동 생성하는 환경 생성 platform임. 정책 학습용 실행 경험도 부산물로 얻는다는 점은 좋으나 정량 수치는 초록에서 확인 불가임</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2611.32473'>OmniPersist: Persistent Dynamic World Modeling via Coupled Panoramic Evolution</a></td><td>52</td><td>7</td><td>World Model</td><td>시점이 돌아섰다 돌아올 때 화면 밖 동적 물체가 사라지거나 변형되는 문제를 파노라마 evolution stream 결합으로 풀어 action-conditioned world model의 object persistence를 개선함. 로봇과 자율주행 world model 핵심 문제이나 정량 수치는 초록에서 확인 불가이고 자체 benchmark임.</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2611.32696'>RestPose: Canonicalization for Open Object Pose Estimation</a></td><td>52</td><td>7</td><td>3D Vision</td><td>reference model 없이 단일 이미지에서 mesh를 만들고 기하와 물리 분석으로 canonical frame을 도출해 category-level pose를 추정함. 관례 의존이라는 문제 설정이 새롭고 학습 없이 supervised SOTA를 18.3점 앞섬. manipulation의 open object pose에 직접 쓸 수 있음</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2611.31925'>Learning When a Robot Should Ask For Help: Adaptive Intervention Requests in Human-Robot Teaming</a></td><td>52</td><td>7</td><td>Embodied AI</td><td>과거 개입의 유용성으로 offline RL을 학습해 로봇이 도움을 요청할 시점을 정하며 사용자 연구까지 수행하나 navigation 한정임</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2611.32727'>Support2Sim: Visually Faithful Real2Sim with Stable Object Supports</a></td><td>52</td><td>7</td><td>3D Vision</td><td>단일 RGB 이미지에서 support graph를 추정하고 physics rollout으로 포즈를 정제하는 Real2Sim임. 지지 관계 실현 87.1% 대 73.2%로 개선했으나 정적 장면 재구성 범위임</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2611.32285'>SofaSpace: A Benchmark for Executable Visual Spatial Reasoning in Continuous Motion and Environment Construction</a></td><td>52</td><td>6</td><td>Embodied AI</td><td>rigid body 연속 이동 계획과 환경 구성을 실행 가능한 geometric verifier로 검사하는 SofaSpace benchmark임. 끝점은 맞아도 연속 경로 유효성이 크게 떨어짐(Claude 97.2%에서 52.8%)을 보여 공간 추론 평가에 의미 있으나 benchmark 기여임.</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2611.32396'>PRC4D: Physical Relation-Constrained Persistent 4D Reconstruction</a></td><td>52</td><td>6</td><td>3D Vision</td><td>접촉과 상대 운동 일관성으로 지속적 rigid 관계를 가려내 가려진 물체의 4D 재구성을 유지하는 PRC4D임. 물체 간 관계 그래프로 occlusion 중 운동을 전파하는 설계가 object-centric 4D에 닿으나 정량 수치는 초록에서 확인 불가임.</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2611.32765'>EviCraft: Can Minecraft Agents Find What They Cannot See?</a></td><td>52</td><td>6</td><td>Embodied AI</td><td>Minecraft 도구가 시야 밖 정보를 쓰는 누출을 evidence closure로 정의하고 benchmark로 강제함. 다이아몬드 도달률이 76-94%에서 32-40%로 떨어져 평가 결함을 강하게 보임. embodied 평가 방법론이나 게임 환경 한정임</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2611.31601'>RePT: 3D Geometry Emerges from 2D Relational Pretraining</a></td><td>52</td><td>5</td><td>Representation</td><td>3D 예측 target 없이 2D cross-view 점 관계 예측만으로 3D 기하가 representation에 생김을 보임. 선형 readout으로 held-out scene에서 r=0.72를 얻음. spatial representation 학습에 새 관점을 주나 규모와 downstream 로봇 검증이 없음</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2611.32811'>Interactive Neural Computers</a></td><td>52</td><td>3</td><td>World Model</td><td>데스크톱 화면을 world model로 학습하고 surprise-gated slot memory(MEMORY-JEPA)로 화면 밖 내용을 기억함. 가려진 파일 회상 64.2% 대 56.0%이고 explicit memory 이식이 흥미로우나 GUI 도메인이라 로봇 직접 연결은 약함</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2611.33145'>Lost on Campus: Evaluating Embodied Spatial Reasoning of Vision-Language Models in the Wild</a></td><td>50</td><td>9</td><td>Embodied AI</td><td>3DGS로 복원한 실외 캠퍼스에서 VLM의 embodied spatial reasoning을 diagnostic QA와 closed-loop navigation으로 평가함. 6개 능력 중 spatial foresight와 ego-allocentric localization이 병목임을 보임. benchmark이나 실제 환경 기반이고 진단 설계가 구체적임</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2611.33013'>RFW-W: Scaling Physical Asset Universes for Generative Embodied Simulation</a></td><td>50</td><td>8</td><td>Embodied AI</td><td>rigid, articulated, deformable asset 101만 개를 task 조건 scene 구성에 연결한 simulation asset 모음임. RoboTwin 5개 과제에서 RFW-R 학습 policy가 randomization 하 성공률 41.8%로 baseline보다 10.6퍼센트포인트 높음. 규모 중심 resource이나 policy 일반화 근거는 있음</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2611.31868'>CALVIN-MAX: When Does a Mid-Execution Change Hurt a Robot Policy?</a></td><td>50</td><td>8</td><td>VLA</td><td>CALVIN에서 mid-execution 변화를 3회 실행 대조로 분리해 10개 policy의 손실과 후속 지시 영향을 측정한 진단 benchmark로 failure 분석에 유용하나 방법 제안은 아님</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2611.32722'>AG-WAM: Attention-Guided World Action Model for Accurate and Efficient Robot Manipulation</a></td><td>50</td><td>8</td><td>World Model</td><td>WAM 내부 attention에 명시적 guidance를 주는 모듈 3개를 붙여 LIBERO-X, RoboTwin-2.0에서 SOTA를 주장함. 모듈 추가형 개선이라 개념적 도약은 작고 수치는 초록에서 확인 불가임</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2611.32788'>Keypose or Dense? A Controlled Comparison of Action Representations for Stage-Structured Manipulation</a></td><td>50</td><td>8</td><td>Imitation Learning</td><td>keypose와 dense action 표현을 동일 조건에서 통제 비교한 분석 연구임. demonstration 속도 변화에 keypose가 강하고 executor 의존이 크다는 결과가 유용하나 설정이 좁고 실로봇은 서랍 열기 하나임</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2611.33143'>ROAM-Bench: Evaluating Embodied Active Spatial Intelligence through Evidence Verification</a></td><td>50</td><td>8</td><td>Embodied AI</td><td>시뮬레이션 상태로 기하·coverage·배치를 독립 검증하는 active spatial intelligence benchmark임. 결과와 요구 충족이 어긋나는 두 실패 유형 진단이 유용하나 250개 과제 규모의 benchmark 기여임</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2611.32216'>NativeDrive: Native Multimodal Foundations for Autonomous Driving</a></td><td>50</td><td>7</td><td>VLA</td><td>native 멀티모달 모델을 구동 policy로 쓰고 generation expert의 editing으로 dense 구조 supervision을 주는 자율주행 VLA임. NAVSIM에서 unified 모델 중 경쟁력 있다는 수준이라 개념적 도약은 제한적임.</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2611.32876'>MemHand: Memory-Enhanced World-Space Hand Motion Reconstruction from Egocentric Videos</a></td><td>50</td><td>7</td><td>3D Vision</td><td>egocentric 영상에서 손의 world-space motion을 단기 event memory와 장기 scale memory로 복원함. W-MPJPE를 ARCTIC에서 57%, HOT3D에서 70% 줄임. human-to-robot policy transfer에 쓸 hand trajectory 소스이고 memory 설계가 문제 구조에 맞음</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2611.31844'>BendGS: Observation-Conditioned Gaussian Self-Modeling for Continuum Robots</a></td><td>50</td><td>7</td><td>3D Vision</td><td>관측에서 추정한 가상 backbone으로 3D Gaussian을 변형해 continuum robot의 다음 형상, 외관, 끝 위치를 예측하며 3DGS 기반 self-model로 참신하나 특수 로봇임</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2611.32093'>MARGIN: A Risk-Aware Agent for Robot Program Refinement</a></td><td>50</td><td>7</td><td>Manipulation</td><td>성공 rollout의 near-miss margin으로 로봇 프로그램의 취약성을 예측하고 수정을 유도하며 AUC 0.774로 held-out 실패를 예측하나 프로그램 합성 영역임</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2611.32493'>CoFiNav: VLM-Guided Coarse-to-Fine Semantic Navigation for Open-Ended Last-Mile UAV Delivery</a></td><td>50</td><td>7</td><td>Navigation</td><td>VLM이 다음에 검증할 entity·관계를 정하고 geometry 모듈이 viewpoint로 바꾸는 coarse-to-fine UAV semantic navigation임. active observation 요소는 좋으나 구성이 모듈 조합 수준이고 수치는 초록에서 확인 불가임</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2611.32029'>Do Occupancy World Models Really Follow Actions?</a></td><td>50</td><td>6</td><td>World Model</td><td>occupancy world model이 반사실 ego action을 실제로 따르는지 묻고, 상대 ego 변환에 정렬한 ReCast와 counterfactual faithfulness benchmark를 제안함. OOD 궤적에서 이득이 뚜렷하나 nuScenes 주행 한정임</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2611.32491'>X-3DComposer: Feed-Forward 3D Scene Composition with Any Assets from Any Views</a></td><td>50</td><td>6</td><td>3D Vision</td><td>에셋과 scene 이미지를 view로 다뤄 VGGT-Omega 기반으로 모든 물체의 pose와 scale을 1초 feed-forward 예측하는 X-3DComposer임. SceneMaker 대비 Chamfer 52% 감소로 scene composition에 강함. 물체 배치 추정은 object-centric 장면 이해에 쓸 만하나 로봇 평가는 없음.</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2611.31998'>ADE: A Zero-Training Unlearning Method for Latent World Models</a></td><td>50</td><td>6</td><td>World Model</td><td>latent world model(DreamerV1)의 backdoor와 낡은 transition을 closed-form으로 제거하는 zero-training unlearning ADE. 새로운 문제 설정이나 MuJoCo 3개 과제에 한정됨.</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2611.31446'>Learning from Human Corrections through Temporal Preferences</a></td><td>50</td><td>6</td><td>RL</td><td>사람 개입의 시점과 교정 내용을 모두 preference pair로 바꿔 value function을 학습하는 formulation이며 goal inference와 correction forecasting에서 상호 보완 효과를 보임</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2611.31656'>BRAG: Bayesian Retrieval Augmented Generation</a></td><td>50</td><td>3</td><td>LG</td><td>chunk별 von Mises-Fisher 생성 모델과 시간 변동 utility로 RAG 피드백 방법들을 특수 사례로 통합하는 이론이 참신함. agent memory 검색에는 닿지만 로봇 적용은 없음</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2611.32900'>Motion Conditioned World Modeling for Embodied Visual Tracking</a></td><td>48</td><td>8</td><td>World Model</td><td>target 움직임 분포와 robot ego-motion을 latent transition에 넣는 motion-conditioned world model을 embodied visual tracking에 적용함. Geometry-Progress module이 경로와 이동 거리의 의존성을 함께 모델링함. 0.5B로 3개 benchmark에서 일반화가 개선되나 수치는 초록에서 확인 불가임</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2611.32162'>Reading Geometric Anchors: Viewpoint Generalization in Imitation Learning for Robotic Manipulation with RGB-Only Deployment</a></td><td>48</td><td>8</td><td>Manipulation</td><td>base frame과 gripper frame anchor로 시점 일반화를 노린 imitation learning이며 MetaWorld와 ManiSkill3 시뮬레이션만 평가해 실로봇 근거가 없음</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2611.32813'>Atomic Policy: Composing Atomic Manipulation Skills with Agentic Reasoning</a></td><td>48</td><td>8</td><td>Manipulation</td><td>VLM이 symbolic state를 추정하고 PDDL로 skill plan을 짠 뒤 agentic harness가 결과를 검증해 replanning하는 구조임. TAMP와 recovery 방향은 맞으나 기존 구성요소 조합이고 수치는 초록에서 확인 불가임</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2611.31826'>VG-GP: Uncertainty-Gated Visuo-Geometric Memory for Negative-Transfer-Resistant Grasp Adaptation</a></td><td>48</td><td>7</td><td>Manipulation</td><td>불확실성 게이트가 있는 GP memory로 pretrained grasp에 residual을 얹고 counterfactual curation으로 negative transfer를 막아 성공률이 38.6에서 53.4%로 오르나 grasp 한정 시뮬레이션임</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2611.32447'>ObsBridge: Observation-Grounded Conditioning for Ego Trajectory Prediction</a></td><td>48</td><td>6</td><td>Navigation</td><td>ego 관측의 가림과 tracking 오류로 손상된 보행자 history를 복원값과 원 관측 증거로 함께 conditioning하는 flow 예측기임. EgoTraj-TBD에서 minADE@20 6.5%, minFDE@20 8.7% 감소를 보여 로봇 내비게이션에 유용하나 개선폭은 incremental임.</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2611.31765'>Dreamcatcher: Remembering What Surprises a World Model in Video Streams</a></td><td>48</td><td>5</td><td>Video</td><td>frozen video world model의 예측 오차로 놀라운 부분만 골라 streaming video 메모리를 만드는 training-free 방법임. world model을 memory 선택에 쓰는 발상이 robot memory에 시사점이 있고 OVO-Bench에서 입력 token을 80% 넘게 줄임. 로봇 실험은 없음</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2611.32337'>Get the Next Moment Right: Short-Term Event Planning for Physically Plausible Video Generation</a></td><td>48</td><td>5</td><td>World Model</td><td>영상 생성을 짧은 clip 단위 closed-loop(grounding, event planning, 생성, verification)로 제어해 물리 타당성을 높이는 training-free 방법임. 물리 world model 추론 계획 관점에서 흥미로우나 로봇 평가는 없고 Physics-IQ 등 영상 benchmark만 씀.</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2611.33011'>MESSI: Multi-Expert Soccer Skill Integration for Physics-Based Character Control</a></td><td>46</td><td>8</td><td>RL</td><td>8개 soccer expert를 transformer로 distillation하고 skill 전환 때만 켜지는 low-rank adapter를 online RL로 학습해 원 policy를 보존함. dribbling에서 shooting 전환 성공률이 19.8%에서 61.8%로 오름. skill chaining 설계가 명료하나 시뮬레이션 character 한정임</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2611.31577'>FabricBench: A Standardized Policy Benchmark for Bimanual Fabric Manipulation with a Contact-Driven Deformable Simulator</a></td><td>46</td><td>8</td><td>Manipulation</td><td>양손 fabric 조작 benchmark와 접촉 기반 simulator로 VLA와 world action model의 한계를 보이고 실로봇 순위 상관 0.94를 확인했으나 benchmark 성격임</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2611.32108'>Duo: Towards Spatiotemporal Action Coordination in Bimanual Policies</a></td><td>46</td><td>8</td><td>Manipulation</td><td>양손을 시간당 토큰 하나가 아닌 둘로 나눠 cross-arm attention을 주는 단순 설계로 RoboTwin 2.0에서 성공률이 9에서 12.5포인트 오르나 모듈 수준 개선임</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2611.32233'>Roboclock: A Unified Benchmark for Time-Aware Robotic Intelligence</a></td><td>46</td><td>8</td><td>Manipulation</td><td>시간 제약 조작 60개 과제의 benchmark로 latency 정렬 평가를 도입하고 최고 VLA도 쉬운 과제에서 8.3%에 그침을 보였으나 benchmark 성격임</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2611.32510'>GeoVLDrive: Geometry-Grounded Vision-Language Reasoning for Autonomous Driving</a></td><td>46</td><td>7</td><td>VLA</td><td>3D foundation model feature를 gated cross-attention으로 넣고 미래 geometry, 에이전트 움직임, meta-action을 latent CoT로 구조화한 자율주행 VLA임. NAVSIM v1 PDMS 91.8, v2 EPDMS 90.9로 강한 수치이나 구성 요소 조합 성격이 커서 개념적 도약은 제한적임.</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2611.31863'>Ada-BFM: Adapting Behavior Foundation Models for Humanoid Scene Interaction</a></td><td>46</td><td>7</td><td>Humanoid</td><td>사전학습 behavior foundation model에 가벼운 adapter를 붙여 휴머노이드 장면 상호작용으로 확장하며 실로봇을 포함하나 구체적 수치는 초록에서 확인 불가함</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2611.32482'>COHERE4D: Training-Free Dense Surface Alignment for Coherent Metric 4D Human-Scene Reconstruction</a></td><td>46</td><td>5</td><td>3D Vision</td><td>human foundation model과 scene foundation model이 공통으로 예측하는 사람 표면을 dense하게 정합해 metric 4D human-scene을 training-free로 복원함. 프레임당 4ms 추가로 14 FPS를 냄. 인간 영상에서 로봇 시연 추출 쪽으로 쓸 수 있으나 로봇 직접 평가는 없음.</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2611.32214'>EvoSearch: Self-Evolving Active Perception for Wide-Area Geospatial Search</a></td><td>46</td><td>4</td><td>Embodied AI</td><td>정책과 exploration program을 함께 진화시켜 광역 지리 탐색에서 관측 trajectory를 줄이는 active perception 연구임. 대상이 위성 영상이라 로봇 직접 적용은 약하나 stop/retain 판단 학습 아이디어는 NBV와 닿음.</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2611.31475'>SpatialCraft: Evolving Procedural Intelligence from Experience and Skills for Spatial Reasoning Agents</a></td><td>46</td><td>4</td><td>Embodied AI</td><td>frozen tool-using agent가 rollout 대조로 Experience를 증류하고 Skill로 통합해 3D 재구성 등 spatial tool 조합을 스스로 개선함. 5개 spatial benchmark와 4개 backbone 전체 설정에서 최고이나 로봇 실행은 없음</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2611.31919'>DUALingo: A Dual-Hand Instruction-Guided Dataset for Affordance Grounding on 3D Objects</a></td><td>45</td><td>7</td><td>Manipulation</td><td>양손 협응 affordance를 task 조건 heatmap으로 근거화하는 271K 과제 dataset을 자동 파이프라인으로 만듦. aIoU가 zero-shot 10.3에서 37.8로 오르고 로봇 시연이 있으나 dataset 중심이고 정량적 로봇 평가는 확인 불가</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2611.32335'>GOLD-SLAM: Gaussian-splatting Omnidirectional LiDAR-Depth SLAM</a></td><td>45</td><td>7</td><td>3D Vision</td><td>파노라마 카메라와 LiDAR 시야 불일치를 다루는 Gaussian splatting SLAM임. 기존 panoramic baseline 대비 PSNR 5.56~9.10dB 상승, Jetson Orin NX 온라인 구동까지 보임. UAV 매핑에 실용적이나 시스템 엔지니어링 성격이 강함.</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2611.33054'>EmbodiSafety: Benchmarking Risk Understanding and Response in Embodied AI</a></td><td>45</td><td>7</td><td>Embodied AI</td><td>embodied 모델의 위험 이해와 6가지 대응 모드를 보는 안전 benchmark임. 1,092+540 과제와 40k 정렬 데이터를 만들었으나 최고 모델 정확도 56.1%의 평가 위주 기여임</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2611.31757'>Xtream: An Explicit Metric State for Large-Scale Streaming Reconstruction</a></td><td>45</td><td>6</td><td>3D Vision</td><td>3D foundation model을 front end로 쓰고 factor graph로 explicit metric state를 유지해 streaming 복원의 drift를 줄임. VBR, KITTI 등에서 ATE를 낮추며 로봇 SLAM에 가깝지만 모듈 결합 성격임</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2611.32642'>BARE: Body-Aware Reflexive Evasion for Humanoid Robots</a></td><td>45</td><td>6</td><td>RL</td><td>위협받는 신체 부위에 맞춰 인간 회피 모션을 고르고 위상을 조절한 뒤 RL로 전신 안정화를 학습하는 humanoid 회피임. 시뮬·실로봇 검증은 있으나 정량 비교가 초록에 없고 범위가 좁음</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2611.32803'>MRBench: Benchmarking Physical Necessity Reasoning in Heterogeneous Multi-Robot Manipulation</a></td><td>45</td><td>6</td><td>Embodied AI</td><td>이종 multi-robot 조작에서 어떤 로봇이 실제로 필요한지 추론하는 benchmark와 MRScissors를 제시함. 팀 선택 정확도 85.4%, 91.2%로 baseline보다 높지만 팀 선택 문제로 범위가 좁음</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2611.33040'>At the Limit: Autonomous Vehicle Drifting under Generative Policies</a></td><td>45</td><td>6</td><td>RL</td><td>SDE sampling 탐색과 value 기반 최적화를 결합한 flow policy online RL을 자동차 drifting에 적용함. F1TENTH 디지털 트윈 결과만 있고 flow policy RL 자체의 새로움은 제한적임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2611.32932'>HARI4D: Hand-Articulation Aware 4D Reconstruction of Human-Object Interaction</a></td><td>44</td><td>7</td><td>3D Vision</td><td>monocular RGB에서 손 articulation을 반영해 4D human-object interaction을 복원함. 물체 오차 56% 감소, hand contact F1 0.866에서 0.921로 상승함. robot learning용 human video 활용과 닿으나 기존 tracker와 network 조합 성격이 있음</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2611.31694'>CATWAY: Cost-sensitive agentic three-way robot decisions with calibrated language-model confidence</a></td><td>44</td><td>6</td><td>Embodied AI</td><td>LLM 로봇 agent의 실행, 질문, 거절을 손실 행렬로 정하는 cost-sensitive gate로 unsafe 142건 모두 차단했으나 텍스트 수준 평가임</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2611.32183'>ThinkMorph-SSL: Scaling Interleaved Multimodal Reasoning with Pretext Tasks</a></td><td>44</td><td>3</td><td>Multimodal</td><td>image colorization 등 pretext task를 interleaved 추론 trace로 바꿔 12개 benchmark 평균 11.33점 올리는 학습 recipe임. 중간 이미지 생성 추론은 embodied reasoning에 이어질 수 있으나 로봇 실험은 없음.</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2611.32431'>NRG-Twins: Pixel-Level Ground Truth for Rigidity Violations in Generated Videos</a></td><td>44</td><td>3</td><td>3D Vision</td><td>생성 영상과 실제 영상 쌍(twin)에서 픽셀별 rigidity 위반 각도를 라벨로 만든 NRG-Twins(871쌍)와 detector임. AUROC 0.85 대 기존 0.40~0.74이며 3DGS 개선까지 보임. 영상 생성의 3D 일관성 진단이라 world model 평가와 닿으나 로봇 실험은 없음.</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2611.32940'>Do Vision-Language Models Know Their Own Visual Weaknesses? Probing Capability-Level Metacognition</a></td><td>44</td><td>3</td><td>Multimodal</td><td>VLM이 자신의 시각적 약점을 사전에 아는지 capability-level로 측정해, 선언적 예측은 부정확하지만 답변 확률에는 모델별 약점 정보가 있음을 보임. self-knowledge 문제 설정이 좋아 failure prediction과 간접 연결되나 로봇 실험은 없음</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2611.33137'>Physicl Scenes: An Artist-created 3D Dataset for Learning Perception and Action</a></td><td>42</td><td>7</td><td>Embodied AI</td><td>예술가가 만든 3D 장면 6,499개 dataset으로 inverse rendering, 3D 재구성, mobile manipulation 학습을 지원함. VLA pick-and-place benchmark와 grasp 부위 채점이 포함됨. dataset 기여이고 manipulation 개선폭은 초록에서 확인 불가임</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2611.32883'>3D Tracking Any Point with Events and Frames</a></td><td>42</td><td>6</td><td>3D Vision</td><td>event camera와 RGB frame을 결합해 프레임 사이에도 2D, 3D point를 추적하는 TrackAnyMotion임. 3D endpoint error 70% 감소, independent-motion decoder가 새로움. 빠른 동작 manipulation이나 dynamic scene 인식에 닿으나 합성 dataset 중심임</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2611.31814'>Beyond the Benchmark: Localizing Released Autonomous Driving Models to Real Vehicles</a></td><td>42</td><td>6</td><td>Robotics</td><td>공개된 자율주행 모델을 새 차량에 맞추는 R2R 방법론이며 폐루프 성공률 82.2에서 95.2%로 오르나 주행 도메인 특화임</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2611.31766'>RoMo Hands: A Large Scale Richly Organized Text to Hand Motion Dataset</a></td><td>42</td><td>5</td><td>Manipulation</td><td>542K 시퀀스의 text-hand motion dataset과 393차원 양손 representation을 제안함. dexterous 동작 생성의 데이터 기반이 되나 로봇 실행 검증은 없고 dataset 기여임</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2611.32251'>CaveBench: Benchmarking Abductive Physical Reasoning from Internal Observations</a></td><td>42</td><td>5</td><td>Embodied AI</td><td>내부 관측만으로 숨은 외부 제어를 추론하는 abductive 물리 추론 benchmark(10,200 episode)임. 6-event exact match가 최고 closed 모델 68.0%, open 12.5%로 격차를 보임. 인과 추론 주제와 닿으나 시뮬레이션 benchmark라 중간 점수임.</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2611.32351'>LookAnything: A Foundation Model for Holistic Gaze Following</a></td><td>42</td><td>5</td><td>Multimodal</td><td>시선 추종을 points, boxes, heatmap, 언어 출력으로 통합한 foundation model과 HoliGaze(311K QA)임. HRI와 실로봇 배포 검증을 언급하나 범위가 초록에서 확인 불가이고 인간 시선 인식 도메인임.</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2611.32523'>AirLeg: A Robust and Accurate Self-Supervised Visual-Inertial-Leg SLAM System</a></td><td>42</td><td>5</td><td>SLAM</td><td>imperative learning으로 simulation 사전학습한 leg odometry를 정답 없이 적응시키는 self-supervised visual-inertial-leg SLAM임. GrandTour 17개 시퀀스 평균 오차 0.19m로 강하지만 state estimation 영역이라 주제와 거리 있음</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2611.32209'>XMind: Thinking Twice via Cross-Memory Reasoning for LLM-Based Autonomous Driving</a></td><td>42</td><td>5</td><td>Embodied AI</td><td>LLM 운전 agent가 working memory와 counterfactual rollout으로 만든 위험 capsule을 대조해 두 번째 결정을 내림. counterfactual memory 아이디어는 주제와 맞으나 고속도로 시뮬레이션 위주이고 성공률 개선은 평균 6.6퍼센트포인트임</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2611.31800'>Learning Compact State Abstractions for LLM Agents</a></td><td>42</td><td>4</td><td>Embodied AI</td><td>LLM agent state를 task 성능을 보존하는 compact 프로그램으로 LLM 유도 genetic search로 학습함. ALFWorld에서 입력을 최대 71% 줄이고 성능은 유지함. robot memory와 state abstraction 관점에서 참고할 만함.</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2611.32672'>Text Is Just Another Shot in Vision-Language Models: Simple Probes on Frozen Encoders Do It</a></td><td>42</td><td>2</td><td>Multimodal</td><td>class name을 kappa개 labeled image와 같은 가치로 보는 Bayesian 해석과 convex probe TASP를 제안함. 복잡한 few-shot VLM 적응 방법들이 frozen feature 위 단순 probe보다 낫지 않다는 통제 비교가 설득력 있음</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2611.32683'>DeCoNav-Act: Benchmarking Collective Physical Capability in Multi-Robot Mobile Manipulation</a></td><td>40</td><td>7</td><td>Embodied AI</td><td>multi-robot 이동 조작에서 handoff 가능한 물리 상태를 만드는지 평가하는 benchmark임. 어떤 방법도 과제를 못 끝낸다는 진단은 있으나 새 방법 기여는 약함</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2611.31812'>Generalizable Feed-Forward 3D Hand-Object Reconstruction with Coarse-to-Fine Contact Estimation</a></td><td>40</td><td>6</td><td>Manipulation</td><td>단일 이미지에서 손과 물체 pose 및 contact를 feed-forward로 함께 추정함. contact를 복원 기하와 함께 푸는 coarse-to-fine 구조가 manipulation 이해에 쓸 만하나 7개 benchmark 개선 중심임</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2611.32186'>SkillHarness: Execution-Aware Coordination with Plug-and-Play Skills for Long-Horizon Traversal</a></td><td>40</td><td>6</td><td>Navigation</td><td>VLM 기반 Harness가 plug-and-play locomotion skill을 조율해 지형을 횡단하나 초록에 정량 결과가 없음</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2611.32579'>Follow-Bench 2.0: An End-to-End 3D Benchmark for Socially-Aware Robot Person Following</a></td><td>40</td><td>6</td><td>Navigation</td><td>사회적 인지 person following을 perception-planning 결합으로 평가하는 Unreal 기반 benchmark임. modular가 end-to-end보다 낫다는 진단은 있으나 새 방법은 없고 benchmark 한정 기여임</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2611.32986'>CAPER: PartGround and PlanRefine for Reliable Manual-Guided Robotic Assembly Planning</a></td><td>40</td><td>6</td><td>Planning</td><td>VLM이 매뉴얼에서 부품 ID를 고르는 오류를 inventory 제약으로 걸러내는 조립 계획 구성임. 과잉 사용 9→0이지만 IKEA 데이터셋 평가에 그치고 로봇 실행은 없음</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2611.31803'>SceneMemBench: A Benchmark for Scene Memory in Interactive Video World Models</a></td><td>40</td><td>5</td><td>World Model</td><td>interactive video world model의 scene memory를 seen-view와 novel-view 기준으로 진단하는 benchmark임. 실패 양상 분리는 유용하나 benchmark 기여이고 로봇 task는 아님</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2611.31958'>SPAR: Self-Referenced World-Model Rewards for Physical Alignment in Video Generation</a></td><td>40</td><td>5</td><td>World Model</td><td>world model 예측 오차를 정지 클립 기준으로 보정해 영상의 물리 타당성 reward로 씀. 쉬운 장면이 높은 점수를 받는 편향을 분리하는 발상이 좋으나 영상 생성 평가이고 로봇 실험은 없음</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2611.32094'>Clinical3D-Bench: Evaluating and Improving Spatial Intelligence of Multimodal LLMs in Hospital Environments</a></td><td>40</td><td>5</td><td>Embodied AI</td><td>병원 환경의 공간 추론 benchmark이고 fine-tuned MLLM이 3D map을 거의 쓰지 않는다는 관찰을 보임. 3D 연산을 MLLM이 호출하는 GeoJeV가 scene memory를 쓰는 점은 embodied spatial reasoning과 닿으나 시뮬레이션 QA 범위임</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2611.32513'>DiffAnchor: Anchor-Space Diffusion for Monocular 3D Hand Pose Estimation</a></td><td>40</td><td>5</td><td>Manipulation</td><td>손 자세 추정에서 관절 대신 anchor를 diffusion하여 few-step 단일 가설로 정확도와 효율을 냄. HO-3D V2, NYU, ICVL에서 SOTA라 하나 구체 수치는 초록에서 확인 불가임. dexterous manipulation 인식 모듈이나 로봇 적용은 보이지 않음.</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2611.32529'>ContinualDrive: A Deployment-Anchored, Multi-Axis Benchmark for Continual Updates of Learned Driving Planners</a></td><td>40</td><td>5</td><td>Autonomous Driving</td><td>배포된 planner 대비 갱신 여부를 판정하는 continual learning benchmark임. open-loop와 closed-loop 평가가 엇갈린다는 지적은 유용하나 benchmark 성격이고 자율주행 한정임</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2611.32202'>SplatTok: Data-Driven Compression of 3D Gaussian Splats with Scene-Level Tokens</a></td><td>40</td><td>3</td><td>3D Vision</td><td>3DGS를 scene-level token으로 인코딩하고 새 primitive 집합으로 재합성하는 codec으로 FCGS 대비 4~6.5배 작은 파일을 냄. 압축 개념은 참신하나 로봇 직접 관련은 약함.</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2611.31522'>One Step, Four Clocks: How GUI Agents Fall Out of Step</a></td><td>40</td><td>3</td><td>Embodied AI</td><td>GUI agent 실패를 환경 변화, 관측, 결정, 행동 수신의 네 시점(EODA)으로 모델링하고 대기 중 행동을 갱신하는 Chronotope를 제안함. 비동기 실시간 제어 문제 설정은 로봇 reactive control과 통하나 GUI 환경 한정임</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2611.31817'>Compressible Representations: Functional Spines in Deep Neural Networks</a></td><td>40</td><td>2</td><td>LG</td><td>task에 민감한 표현 부분공간(Fisher형 행렬)으로 압축성, 견고성, continual learning을 분석한 표현 학습 연구임. 일반 도구로 쓸 만하나 로봇 직접 검증은 없음</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2611.31892'>Cheap Memory Costs Future Compute: Co-Designing Persistent KV and GPU Execution for Efficient Streaming Video Diffusion</a></td><td>40</td><td>2</td><td>Video</td><td>block-causal video diffusion의 KV cache 갱신을 일부 재구성으로 대체해 DiT 지연 20.9%를 줄임. 장기 영상 생성 효율은 world model 추론 가속에 참고되나 로봇 직접 실험은 없음</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2611.32745'>MemAnchorWorld: A Sparse World Model with Horizon-Conditioned Memory Retrieval for Autonomous Driving</a></td><td>38</td><td>6</td><td>World Model</td><td>sparse occupancy world model에서 forecast 시점별로 과거 geometry와 semantic 증거를 명시적으로 retrieval하는 memory anchor를 도입함. 오차 누적 문제를 짚은 점은 robot memory와 닿으나 mIoU 13.55%로 향상 폭이 작고 driving 한정임</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2611.32185'>OVOK: A Recursive Self-Improving Agentic Framework for Video-Based Articulated Robot State Estimation</a></td><td>38</td><td>6</td><td>3D Vision</td><td>agentic 도구 진화 loop로 영상에서 articulated robot 상태를 추정해 DREAM-V에서 SOTA를 주장하나 추정 보조 작업이며 수치는 초록에서 확인 불가함</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2611.32502'>MRCT: An Object-Centric Two-Layer Control Architecture for Heavy-Payload Multi-Robot Transportation</a></td><td>38</td><td>6</td><td>Manipulation</td><td>MPC 물체 수준 힘 참조와 whole-body impedance 제어를 confidence로 섞는 다중 로봇 운반 제어 구조임. 실하드웨어 검증은 있으나 고전 제어 조합 수준임</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2611.32718'>Seeing to Drive on a Single Board: Attention-Free Depth for Onboard Robot Navigation</a></td><td>38</td><td>6</td><td>Navigation</td><td>Depth Anything V2를 attention 없는 ResNet-34 U-Net으로 distillation해 Pi 5와 Hailo-8L에서 27.1 FPS로 돌림. int8 attention 열화 원인 분석은 좋으나 효율화 공학 성격이 강함</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2611.31902'>MIFLOW: Dynamic Recent-Behavior Priors for Reference-Calibrated Online Flow-Policy Reinforcement Learning</a></td><td>38</td><td>5</td><td>RL</td><td>최근 행동에 맞춘 flow-matching prior로 online flow-policy RL의 critic 외삽 오류를 완화하는 MIFLOW이나 MuJoCo 6개 과제이고 일부 과제에서만 우세함.</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2611.32547'>Contact Geometry for Generative Models: An Unbalanced Optimal Transport Formulation</a></td><td>38</td><td>3</td><td>LG</td><td>contact geometry 기반 unbalanced OT로 WFR의 고밀도 편향을 줄인 생성 모델 이론이며 비디오 생성 실험이 있으나 로봇은 간접 언급임</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2611.32147'>ARS-VLM: Visually Aligned Augmented Random Search for Vision-Language Models</a></td><td>38</td><td>2</td><td>LG</td><td>VLM 후처리를 forward-only zeroth-order 탐색(ARS)으로 하되 시각 정렬과 forgetting 억제를 넣어 GRPO와 동급 OOD 정확도를 7.5배 적은 step으로 냄. 로봇과 직접 관계 없고 VLM 효율 학습 기법임.</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2611.33102'>Reinforcement Learning Can Be Recovered From Its Own Rollouts</a></td><td>38</td><td>2</td><td>RL</td><td>RL 후처리 rollout을 순서대로 maximum likelihood 학습하면 online RL 성능이 회복됨을 보여 RL이 sampling 분포 발견에 쓰인다는 해석을 줌</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2611.31795'>Constructive Causal Abstraction and a Case Study in Mechanistic Interpretability</a></td><td>38</td><td>1</td><td>LG</td><td>micro 개입이 macro에서 정의되지 않는 문제를 보완 변수 q로 구성적으로 해결하는 causal abstraction 이론임. 개념은 탄탄하나 로봇 연결은 간접적임</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2611.32846'>DOPER: Deep Object Pose Estimation Revisited</a></td><td>36</td><td>7</td><td>3D Vision</td><td>검출, segmentation, keypoint를 공유 backbone으로 학습하고 multi-view 기하 제약으로 real 관측에 적응하는 RGB 6D pose임. HANDAL, HOPEv2, HOT3D, T-LESS에서 detection AP 최고이고 35Hz임. manipulation에 쓸 수 있으나 새로운 개념은 적음</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2611.32821'>PhysMend: Verification-Guided Program Refinement for Physics-Aware Video Generation</a></td><td>36</td><td>5</td><td>Generative</td><td>물리 program을 simulation rollout과 depth control 위에서 검증, 수리한 뒤 한 번만 생성하는 training-free video 생성임. Physics-IQ를 27.33에서 39.40으로 올림. 물리 인식 생성은 world model과 닿으나 로봇 평가는 없음</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2611.31561'>Sampling at Scale: Distributed Multi-Agent Trajectory Optimization</a></td><td>36</td><td>5</td><td>Navigation</td><td>각 agent가 자기 제어 공간에서만 sampling하는 분산 trajectory optimization으로 1024 agent까지 확장하나 학습 요소는 약함</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2611.31676'>Exact Collision Gradients for Ellipsoids in Differentiable Simulation</a></td><td>36</td><td>5</td><td>Robotics</td><td>타원체 충돌의 time of impact를 연속 충돌 검출로 구해 differentiable simulation에서 정확한 gradient를 얻는 기여는 명확하나 범위가 좁음</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2611.31835'>POISE: Curvature-Aware Critic Regularization for Smooth Actor-Critic Control</a></td><td>36</td><td>5</td><td>RL</td><td>critic의 curvature 가중 에너지를 정규화해 actor-critic 행동 진동을 줄이는 방법이며 6개 연속 제어 과제에서 smoothness 개선을 보임</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2611.32816'>SpatialArena: Where Do Geometric Foundation Models Stand?</a></td><td>36</td><td>4</td><td>3D Vision</td><td>geometric foundation model 52개를 23개 dataset에서 같은 metric과 robust alignment로 비교하는 SpatialArena임. 기존 보고 수치가 비교 불가능하다는 점을 정량으로 보인 평가 인프라이나 새 방법은 없음</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2611.32432'>Video Models are Excellent Motion Models</a></td><td>36</td><td>3</td><td>Video</td><td>video foundation model이 전용 motion 모델보다 자연스럽고 의미 있는 인간 동작을 만든다는 position을 3D skeleton 비교로 주장함. 로봇 모션 prior 관점에서 흥미로우나 인간 애니메이션 평가이고 실로봇 연결은 없음.</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2611.32175'>LoopFit: Retrofitting Pretrained Diffusion Transformers with Recurrent Refinement</a></td><td>36</td><td>2</td><td>Generative</td><td>pretrained DiT에 recurrent refinement를 이식해 추론 연산을 깊이 방향으로 늘리는 test-time compute 아이디어임. 평가가 maze 등 퍼즐 12종이고 로봇 적용은 없음.</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2611.32316'>ASTERISM: Do Multimodal LLMs Actually Look at All the Images?</a></td><td>36</td><td>2</td><td>Multimodal</td><td>multi-image benchmark 19종 중 24.2% 항목이 단일 이미지로 풀림을 감사하고 cross-image credit assignment로 RLVR의 shortcut 보상을 줄임(ASTERISM 점수 2.6~6.0점 상승). shortcut 진단은 탄탄하나 로봇과 거리 있음.</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2611.33005'>Leto: Utility-Centric Agent Memory</a></td><td>36</td><td>2</td><td>Embodied AI</td><td>agent memory를 과거 충실도가 아니라 미래 응답 효용으로 평가하는 Leto를 제안함. 기억 색인, 예측 replay, utility loop 구성은 robot memory와 개념적으로 닿으나 대화 LLM benchmark 한정임</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2611.32472'>STAR: Counterfactual Dual-World Rollouts and Spatial Target Adaptive Reconstruction for Visual On-Policy Distillation</a></td><td>36</td><td>1</td><td>Multimodal</td><td>국소 증거를 가린 반사실 dual-world rollout으로 VLM의 맥락 shortcut을 드러내고 on-policy distillation하는 STAR임. 평균 정확도 최대 8.04퍼센트포인트 상승. counterfactual 아이디어는 닿으나 대상이 VLM 세부 인식이고 로봇 실험은 없음.</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2611.32582'>Design, Control, and Teleoperation of a Dexterous Robotic Hand with Soft-Rigid Hybrid Fingers</a></td><td>35</td><td>7</td><td>Manipulation</td><td>soft-rigid hybrid 손가락 5지 손으로 33개 grasp 자세 중 28개를 달성하고 teleoperation 시연을 보임. 하드웨어 설계 위주이며 학습 정책과의 연결은 약함</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2611.32937'>Self-Sensing Compliant Anthropomorphic Hand for Speed-Dictated Shared Force Control in Teleoperation</a></td><td>35</td><td>6</td><td>Manipulation</td><td>compliant 손의 직렬 스프링을 센서로 써 힘을 추정하고 속도 기반 shared control을 구현함. 하드웨어·teleoperation 중심이고 취약·중량 물체의 grasp 성공률 개선 폭은 초록에서 확인 불가임</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2611.31952'>VLG-Drive: Unifying Vision-Language and Geometric Priors for Autonomous Driving</a></td><td>35</td><td>5</td><td>Embodied AI</td><td>frozen VLM과 geometry foundation model 특징을 셀 단위로 융합하고 가벼운 planner만 학습하는 자율주행 구조임. NavHard와 HUGSIM closed-loop에서 이기나 융합 interface 수준의 기여임</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2611.32025'>View Management with Gaussian Placement and Opacity Regularization for Online 3DGS</a></td><td>35</td><td>5</td><td>3D Vision</td><td>online 3DGS SLAM에서 non-keyframe을 점진적으로 쓰고 opacity regularization을 더해 map 품질을 높임. 로봇 매핑에 쓸 만하나 기존 SLAM에 얹는 module 조합 성격임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2611.31428'>Enhancing Sparse-View Gaussian Splatting with Feed-Forward Priors via Spectral Fusion and Distillation</a></td><td>35</td><td>3</td><td>3D Vision</td><td>sparse-view 3DGS와 feed-forward 모델이 주파수 대역에서 상보적임을 보이고 low-pass 가중치로 융합 후 distillation함. 아이디어는 깔끔하나 NVS 품질 개선 범위임</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2611.32443'>PVWander: 3D Memory-guided Panoramic Video Wandering with Path-Facing Canonicalization</a></td><td>35</td><td>3</td><td>Video</td><td>온라인 point cloud 메모리를 reproject해 파노라마 영상 장기 wandering을 안정화함. 3D memory 사용은 흥미로우나 생성 품질 개선 위주이고 로봇 과제 평가는 없음.</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2611.31797'>A Generative AI Agent to Emulate Interactive Human-driven Vehicles for Automated Driving Testing in Urban Areas</a></td><td>35</td><td>3</td><td>RL</td><td>가시 범위 모델링과 residual RL로 상호작용 운전자 행동을 생성해 자율주행 안전 시험에 씀. INTERACTION 데이터 위주이고 로봇 manipulation과는 거리 있음</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2611.32088'>From Memory Access to Evidence Sufficiency: Diagnosing and Addressing Demand--Evidence Misalignment</a></td><td>35</td><td>2</td><td>NLP</td><td>장기 기억 검색에서 관련성과 근거 충분성의 불일치를 MemPath로 진단하고 BiDE-Mem으로 개선함. memory 주제와 닿으나 LoCoMo 같은 대화 benchmark 위주임</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2611.32292'>VC-OPD: Learning to See What Matters via Visual Cue On-Policy Self-Distillation</a></td><td>35</td><td>2</td><td>Multimodal</td><td>질문 조건부 visual cue를 teacher에게만 주는 on-policy self-distillation으로 4B MLLM 성능을 올림. 시각 추론 학습 방식 개선이나 로봇과는 간접적임</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2611.31488'>Embodied Neuro-symbolic AI: Making Robot Behavior Auditable, Safe, and Scalable</a></td><td>34</td><td>6</td><td>VLA</td><td>neuro-symbolic AI로 VLA의 감사 가능성과 안전성을 높이자는 position 성격 글이며 실험 근거는 제한적임</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2611.31843'>Co-DRIS: Physics-Informed Predictive Belief and Variable-Impedance Learning for Reactive Catching under Coupled Uncertainty</a></td><td>34</td><td>6</td><td>Manipulation</td><td>물리 기반 world model과 variable impedance로 던진 물체 잡기의 결합 불확실성 강건성을 높이나 단일 과제 특화 시스템임</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2611.31341'>EvoMisty: Building, Optimizing, and Evolving Capabilities on a Social Robot</a></td><td>34</td><td>4</td><td>Embodied AI</td><td>코딩 에이전트가 Misty II 로봇의 capability를 만들고 최적화해 skill library에 증류함을 보이나 소셜 로봇 단일 플랫폼 중심의 시스템 구성임</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2611.32171'>Mind the Band: The Hidden Frequency Variable in Geometric RoPE</a></td><td>34</td><td>3</td><td>3D Vision</td><td>geometric RoPE의 frequency band 설정이 novel view synthesis 순위를 뒤집을 수 있음을 분석하고 forward-backward 비대칭을 규명함. 다시점 3D 학습에 쓸 만한 진단이나 로봇 직접 관련은 약함.</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2611.32461'>ViDM: Efficient and Order-Robust Parallel Visual Decision Making</a></td><td>34</td><td>2</td><td>Multimodal</td><td>같은 이미지에 대한 여러 질문을 한 번의 forward로 병렬 답변하는 ViDM임. 평균 정확도 73.49%에서 77.55%, throughput 8.4배로 효율 추론은 좋으나 로봇 직접 관련은 약함.</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2611.33037'>Linear Probes Can Guide: Training-Free Control of Representation Generators</a></td><td>34</td><td>2</td><td>Generative</td><td>VFM 표현 공간에서 linear probe가 denoiser 예측의 정확한 posterior mean을 준다는 관찰로 training-free guidance를 Bayesian 선형 역문제로 정식화함. 일반적 이론 도구이나 이미지 생성 제어에 한정되고 로봇 연결은 약함</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2611.33148'>CoT-Proxy: Cross-Format Transfer for Distilling Long-Horizon Policies</a></td><td>34</td><td>2</td><td>LG</td><td>teacher의 행동만으로 CoT를 비운 채 long-horizon policy를 distill하고 CoT-proxy 요약을 붙이는 방법임. AppWorld에서 Qwen3-4B가 7%에서 35%로 오르나 LLM agent 한정이고 imitation 관점의 시사점만 있음</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2611.31554'>Agent Recovery Gone Wrong: Measuring Harm Beyond Duplicate Calls</a></td><td>34</td><td>2</td><td>Embodied AI</td><td>code agent가 실패 후 재시도할 때 외부 상태를 해치는 비율을 AppWorld 궤적에서 24.6%로 추정함. failure recovery의 부작용 측정이라는 문제 설정은 흥미로우나 API 쓰기 한정이고 표본 200개임</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2611.31516'>InitFree-SfM: When Initialization-Free Bundle Adjustment meets Learned Structure-from-Motion</a></td><td>33</td><td>3</td><td>3D Vision</td><td>initialization-free BA에 learned metric depth와 depth 제약 dOSE를 넣어 SfM pipeline을 만듦. surrogate objective 중심 기존 연구의 한계를 분석하나 SfM 범위에 머묾</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2611.32231'>ST-SfM: Spatio-Temporal Structure-from-Motion for Initialising 4D Gaussian Splatting</a></td><td>33</td><td>3</td><td>3D Vision</td><td>동기화된 multi-camera 영상에서 static과 동적 4D 점을 구해 4DGS를 초기화하는 ST-SfM임. N3DV에서 random 초기화 대비 PSNR 등이 오르나 작은 module 수준 개선이고 로봇 연결은 약함.</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2611.32549'>MinPair: Measured Minimal Pairs for Fine-Grained Control in Text-to-Motion Generation</a></td><td>33</td><td>3</td><td>Generative</td><td>측정된 minimal pair와 contrastive pair loss로 text-to-motion의 속성 단어 반영률을 11%에서 60%로 올림. 표준 metric이 잡지 못하는 control 실패를 짚은 점은 좋으나 humanoid motion 생성과 간접 연결임</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2611.32938'>Efficient Video Retrieval Augmented Generation via Token Allocation</a></td><td>33</td><td>2</td><td>Multimodal</td><td>video RAG를 frame과 subtitle 간 token 배분 문제로 정식화하고 water-filling으로 풂. 정확도 최대 7.2퍼센트포인트 상승이고 수렴 보장이 있으나 video QA 효율화에 한정됨</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2611.32566'>Evaluating Latent Knowledge Stability in Multimodal Large Language Models</a></td><td>33</td><td>2</td><td>Multimodal</td><td>MLLM의 image viewpoint와 질문 표현 변화에 따른 latent knowledge 안정성을 margin 기반 MRS, KSS로 측정함. viewpoint 강건성은 embodied에 간접적으로 닿으나 평가 지표와 벤치마크 위주임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2611.33109'>RenGen: Generating Images with as Many Tokens as the Scene Needs</a></td><td>33</td><td>1</td><td>Generative</td><td>region 인코더 latent에서 장면 복잡도에 따라 token 수를 달리하는 이미지 생성 RenGen임. ImageNet gFID 1.34, token 88개이고 2.5배 지연 감소함. 설계는 새로우나 로봇과 무관함</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2611.31427'>Learning What vs. Learning How: Decomposing Task and Interface Competence in Agentic Training</a></td><td>33</td><td>1</td><td>LG</td><td>agent 실패를 task competence와 interface competence로 분해하고 harness rehearsal을 제안함. BFCL V3에서 두 신호를 함께 쓸 때 58.8%로 단독 합보다 큼. embodiment 전이와 유사한 관찰이나 LLM tool agent 한정임</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2611.31976'>CodeHOI: Code with Agents for Physically Plausible 4D Hand-Object Interaction</a></td><td>32</td><td>5</td><td>Manipulation</td><td>코딩 agent가 물질별 물리 solver로 4D hand-object interaction을 프로그램으로 작성함. 접촉 기반 손 명세가 흥미로우나 로봇 policy 연결과 실물 검증은 없음</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2611.32735'>AnyPrune: Optimization-Free Pruning for Any Feedforward 3D Gaussian Splatting Pipeline</a></td><td>32</td><td>4</td><td>3D Vision</td><td>feedforward 3DGS 위에 붙는 optimization-free pruning module AnyPrune임. 1.6M Gaussian을 5초에 pruning하며 여러 pipeline에 적용됨. 실용적이나 효율화 module 수준임</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2611.32496'>Assessing Robustness to Catastrophic Forgetting in Continual Deep Reinforcement Learning for Cyber-Physical Systems</a></td><td>32</td><td>4</td><td>RL</td><td>자율 주차 환경에서 PPO, SAC, Drama의 continual RL forgetting 강건성을 비교한 경험 연구로 새 방법은 없고 off-policy replay 이점이 확인됨</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2611.32013'>To Critic Or Not To Critic</a></td><td>32</td><td>3</td><td>RL</td><td>PPO와 GRPO의 critic 유무를 batch size, 과제 복잡도별로 1,200회 넘게 비교함. 실증은 탄탄하나 LLM과 control 위주이고 로봇 직접 연결은 약함.</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2611.32691'>Load Balancing Neurons: Firing-Rate Control Sustains Plasticity in Continual Learning</a></td><td>32</td><td>3</td><td>RL</td><td>ReLU 발화율을 목표 범위로 유지해 continual learning의 plasticity 손실을 막는 가벼운 방법이며 Atari RL에서도 소폭 개선됨</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2611.32423'>Factorized Context Attention: From Emulated to Native Grid Probing</a></td><td>32</td><td>2</td><td>Multimodal</td><td>grid probing을 prompt로 흉내 내지 않고 block-sparse attention으로 네이티브 실행해 비용을 줄이는 FCA임. 긴 영상과 긴 문맥 효율 추론으로 로봇 직접 관련은 약함.</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2611.32539'>Avalon-M1: Reinforcement Learning from Collective Rewards</a></td><td>32</td><td>1</td><td>RL</td><td>CEO와 최대 8 specialist가 한 policy를 공유하고 공통 advantage로 학습하는 RLCR을 제안함. 지연 제약 아래 multi-agent 조직 학습은 새로우나 LLM agent 대상이고 로봇 적용은 없음</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2611.33157'>PointX: Multi-View Consistent Intrinsics by Querying Surface Points</a></td><td>31</td><td>3</td><td>3D Vision</td><td>view별 pixel 대신 3D 표면 점마다 intrinsics를 한 번 예측해 multi-view 일관성을 구조적으로 보장함. 재조명과 편집에 쓰이나 robot 과제 평가는 없음</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2611.31680'>Curvature-Equilibrated Policy Optimization for Deep Reinforcement Learning</a></td><td>30</td><td>5</td><td>RL</td><td>actor loss의 curvature를 균형 맞춰 SAC를 개선하는 EQUIP이나 MuJoCo 6개 과제에 한정되고 incremental 최적화 수준임.</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2611.31478'>Which Way Is Up? Rotated Photos Silently Hurt Multi-View 3D Foundation Models</a></td><td>30</td><td>4</td><td>3D Vision</td><td>회전된 사진이 multi-view 3D foundation model 5종의 pose 정확도를 조용히 떨어뜨림을 측정함. 로봇 SLAM 파이프라인에 쓸모 있는 진단이나 해법 기여는 약함</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2611.31944'>DraftKV: Protecting Persistent Worlds through Hierarchical Streaming Retrieval</a></td><td>30</td><td>4</td><td>World Model</td><td>interactive world model의 historical KV cache를 기하 기반으로 검색하고 CPU offloading으로 지연을 줄임. 3.27배 속도 향상이 있으나 효율 엔지니어링 성격이 강함</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2611.32716'>SplatSeg3D: Efficient Zero-Shot 3D Segmentation via Point Cloud Surfelization and Splatting</a></td><td>30</td><td>4</td><td>3D Vision</td><td>image, pose 없이 point cloud를 surfelize하고 splatting으로 view를 렌더링해 zero-shot open-vocabulary 3D segmentation을 함. 4개 benchmark에서 SOTA 수준이고 효율적이나 기존 2D foundation model 파이프라인 조합임</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2611.32964'>Benchmarking Evidence Sufficiency in Vision-Language Models for Autonomous Driving</a></td><td>30</td><td>4</td><td>Multimodal</td><td>주행 VLM이 증거 충분성을 판단해 abstain하는지를 strong, weak evidence 쌍 20,151문항으로 평가함. 정답, 기권, grounding 동시 충족이 21.55%뿐이라는 점은 의미 있으나 benchmark 기여임</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2611.31735'>BEARING: Who Is Talking to Whom? Grounding Acoustic Direction in Vision for Online Multi-Party Conversation</a></td><td>30</td><td>3</td><td>Multimodal</td><td>마이크 배열 방향을 카메라에 정합해 화자와 청자를 찾는 기하 중심 방법이고 verifiable reward로 정렬함. 로봇 대화 상황에는 연결되나 로봇 task 실험은 없음</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2611.32361'>Sub-Riemannian structure for Oriented Point Clouds</a></td><td>30</td><td>3</td><td>3D Vision</td><td>oriented point cloud에 sub-Riemannian contact metric을 정의해 얇은 표면 간 feature 누출을 줄이는 이론적 도구임. PointNet++ drop-in으로 분할 개선을 보이나 규모가 작고 로봇 연결은 약함.</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2611.32548'>SetCon: Setup-Conditioned IMU-Language Learning from 3D Human Motion</a></td><td>30</td><td>3</td><td>Multimodal</td><td>IMU-text 정렬에서 mounting 완전 불변 대신 setup 조건부 표현을 쓰고 3D motion 시뮬레이션으로 학습함. 13개 dataset zero-shot 평균 56.6%로 AnyMo 41.8%보다 높아 wearable 쪽 근거는 강하나 로봇과는 간접적임</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2611.32554'>PartAgent: Agentic 3D Part Segmentation via Expert Integration and Closed-Loop Refinement</a></td><td>30</td><td>3</td><td>3D Vision</td><td>3D expert와 2D expert를 agent가 closed-loop로 정제하는 training-free 3D part segmentation임. 5개 dataset mIoU 최고지만 manipulation affordance와의 연결은 간접적임</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2611.32998'>First-Hit Photoconsistency for Neural Surface Reconstruction</a></td><td>30</td><td>3</td><td>3D Vision</td><td>volumetric rendering과 appearance model 없이 sphere tracing 첫 교점의 patch photoconsistency만으로 neural surface를 복원함. 모호성을 제거하는 발상은 흥미로우나 BMVS, DTU의 표면 복원 한정임</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2611.33135'>BriConstrain: Geometrically Constrained Decoding for Autoregressive Brick Assembly Generation</a></td><td>30</td><td>3</td><td>Generative</td><td>LEGO 조립 생성에서 geometric oracle로 부착 방식을 제약하는 constrained decoding임. 충돌 없는 build 비율이 31%에서 91%로 오름. 조립 계획과 닿으나 로봇 실행은 없음</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2611.31431'>CaLA: Causal Latent Adjustment for World Models under Adaptive Policies</a></td><td>30</td><td>3</td><td>World Model</td><td>adaptive policy로 수집된 rollout의 confounding을 DAG 제약 latent로 보정하는 world model CaLA임. what-if 인과 추론 관점은 좋으나 Match-3 게임 SCM 한정이고 로봇 검증은 없음</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2611.31397'>CoRe: Jointly Learning Contextual Representations for Understanding and Generation</a></td><td>30</td><td>2</td><td>Multimodal</td><td>이해와 생성이 한 representation을 공유하도록 처음부터 학습함. 383M 규모에서 FID 10.10을 보이나 로봇 직접 연결은 약함</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2611.32982'>When Repair Accuracy Misleads: Training a VLM on Its Own Failures</a></td><td>30</td><td>2</td><td>Multimodal</td><td>VLM의 자체 failure로 fine-tuning할 때 repair accuracy가 오해를 부름을 보임. 라벨 오류 37%, 질문 문장 shortcut 73.2%, negation 성능 하락을 드러낸 평가 분석임. 실험 범위는 한 모델 중심임</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2611.32439'>See the Answer, Learn to Embed: Learning Universal Multimodal Embeddings from Hindsight</a></td><td>30</td><td>2</td><td>Multimodal</td><td>정답 후보를 teacher 문맥으로 보게 한 뒤 추론 비용 없는 student embedder로 distill하는 UME 학습으로 효율은 좋으나 retrieval 한정임</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2611.33022'>RecordRoute: Auditing Agent Failures with Localization-Guided Diagnosis</a></td><td>30</td><td>2</td><td>NLP</td><td>실패한 agent 실행에서 책임 주체, 결정적 단계, 오류 유형을 비교 순위로 진단하는 RecordRoute임. failure diagnosis 주제와 닿으나 LLM agent 로그 대상이고 로봇 시스템은 아님</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2611.32463'>Describe, Don&#x27;t Ask: Caption-Driven On-Policy Distillation for Fine-Grained Visual Perception</a></td><td>30</td><td>1</td><td>Multimodal</td><td>질문 대신 image-agnostic caption prompt로 crop-view 교사의 on-policy distillation을 하는 CaptionOPD임. 세부 인식 개선이고 로봇 무관함.</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2611.32687'>Are We Rewarding the Wrong Module? Module-Specific Policy Optimization for Multimodal Reinforcement Learning</a></td><td>30</td><td>1</td><td>Multimodal</td><td>GRPO에서 vision encoder에 perception checklist 기반 advantage를 따로 주는 module-specific credit 분리임. 수학 reasoning 7개 benchmark 평균 개선이고 로봇 적용은 없음</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2611.31870'>Subliminal Learning Crosses Modalities</a></td><td>30</td><td>1</td><td>Multimodal</td><td>텍스트 subliminal learning이 VLM의 이미지 생성으로 cross-modal 전이됨을 보이고 weight lens를 제안함. 흥미로운 현상이나 로봇과 직접 연결 약함.</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2611.32991'>On Potentiality and Actuality Of Foundation Models</a></td><td>30</td><td>1</td><td>LG</td><td>adaptation 이득 대부분이 입력과 무관한 상수 shift로 재현된다는 potentiality 원리를 제시하며 LoRA 대체 가능성을 보임</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2611.31621'>Self-Improving Long-Horizon Reasoning by Learning Summaries from Local Continuations</a></td><td>30</td><td>1</td><td>LG</td><td>추론 trace를 잘라 요약하고 frozen 모델의 continuation에 대한 Delta-KL로 summarizer를 학습함. 정답과 teacher 없이 long-horizon 상태 압축을 학습하는 점은 좋으나 수학 추론 한정임</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2611.32055'>More Powerful, Less Verifiable? Mitigating Hard-to-Verify Hallucinations in MLLM&#x27;s Reinforcement Learning</a></td><td>30</td><td>1</td><td>Multimodal</td><td>RL이 사람이 찾기 어려운 hallucination을 늘리는 문제를 verifiability 예산 제약 reward(DAPO-V)로 줄임. RL 보상 설계 관점은 흥미로우나 MLLM 대상이고 로봇과 무관함</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2611.33017'>E-MAPS: Event-Based Promptable Video Segmentation with Memory-as-Prompt</a></td><td>29</td><td>3</td><td>Video</td><td>event 스트림에서 prompt 가능한 video segmentation을 memory-as-prompt로 수행하고 EViM dataset을 만듦. 3개 benchmark에서 우세하나 event 특화 segmentation임</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2611.32054'>SurgGenesis: A Generative Surgical World Model for Future-Aware Surgical Understanding</a></td><td>28</td><td>4</td><td>World Model</td><td>수술 영상의 미래 상태를 생성하는 world model로 long-tail 데이터를 보강함. action-faithful 검증 방식은 좋으나 수술 도메인 한정이고 제어 사용은 없음</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2611.31973'>Visual Thinking: Training-Free Active Perception for Counting and Localizing Hard-to-Find Objects</a></td><td>28</td><td>3</td><td>CV</td><td>VLM과 SAM 3를 반복 루프로 묶은 training-free active perception임. 작은 물체 counting에서 MAE를 크게 줄이나 2D 이미지 내 탐색이고 실제 시점 이동은 없음</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2611.32793'>Back to Raw Motion: Latent-Free Diffusion Transformers for Text-to-Motion and Exact Conditional Generation</a></td><td>28</td><td>3</td><td>Generative</td><td>latent codec 없이 raw motion 공간에서 diffusion transformer로 text-to-motion을 생성하고 조건을 정확히 보존함. HumanML3D, KIT-ML에서 text alignment 최고이나 motion quality는 경쟁 수준임</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2611.31964'>Sounding the Black Box: Online Training of Embedded Neural Networks in Forward-Only Physical Simulators</a></td><td>28</td><td>3</td><td>LG</td><td>forward-only 시뮬레이터에 내장된 신경망을 Gauss-Newton 응답 추정으로 online 학습하는 FORGE이고 PDE 모델링 응용이라 로봇 관련성 약함.</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2611.31586'>SecondChance: Benchmarking Reliable Error Recovery in AI Agents</a></td><td>28</td><td>3</td><td>NLP</td><td>agent가 자신의 오류에서 회복하는 행동을 checkpoint에서 재개해 측정하는 benchmark임. 최고 모델 자력 회복 16%, repair guidance 27%라는 진단은 failure recovery 관점에서 참고할 만하나 텍스트 agent 한정임</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2611.32410'>TESS: Query-Guided Temporal Event-Structured Frame Selection for Long-Video Understanding</a></td><td>28</td><td>2</td><td>Video</td><td>질의 기준으로 기준 이벤트와 질문 이벤트를 시간 순서대로 고르는 training-free frame selection TESS임. 고정 frame 예산에서 4.0~5.5퍼센트포인트 우위이나 incremental이고 로봇 연결 약함.</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2611.32037'>Online Environment Repair for Coding Agents</a></td><td>28</td><td>2</td><td>RL</td><td>coding agent RL에서 reward hacking을 환경을 실시간 수리해 막는 방법으로 해킹률이 36.9%에서 0.06%로 줄었음. 신선하나 로봇과는 거리 있음.</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2611.31570'>Off-the-Shelf Autonomous Agents for Game Playtesting</a></td><td>28</td><td>2</td><td>Embodied AI</td><td>off-the-shelf LLM으로 미지의 3D RPG를 탐험하며 푸는 playtesting agent Buddy임. long-horizon 탐험과 trace의 HTN 변환은 있으나 정량 근거가 약한 시스템 시연임</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2611.31576'>Lit Up but Not Needed: Scoped Lesions Show Where Multimodal Mixture-of-Experts Depend on Their Experts</a></td><td>28</td><td>1</td><td>Multimodal</td><td>MoE VLM에서 lesion으로 expert 의존성을 측정해, 활성 지도가 필요성을 말하지 않음을 보임. 분석은 탄탄하나 로봇 연결은 약함</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2611.31673'>Medical Image Segmentation Is Now Just Another Coding Task</a></td><td>28</td><td>1</td><td>LG</td><td>coding agent가 의료 segmentation 모델을 스스로 만들고 quality blind spot이 병목임을 보임. 흥미로운 관찰이나 의료 영상 한정이고 로봇과 거리 있음</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2611.32802'>Sample-Efficient In-Context Adaptation via Sleep</a></td><td>28</td><td>1</td><td>NLP</td><td>recurrent forward pass 기반 sleep으로 in-context 적응 효율을 높인 1.2B 사전학습 연구이며 로봇과 거리가 있음</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2611.31677'>Look Before You Commit: Visual-Evidence-Guided Decoding for Multimodal Diffusion Language Models</a></td><td>28</td><td>1</td><td>Multimodal</td><td>diffusion MLLM의 confidence commit이 이미지 근거와 무관함을 ablation으로 진단하고 training-free 디코딩을 제안함. 진단은 흥미롭지만 로봇 연결이 약하고 benchmark 개선 위주임</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2611.32663'>Economic World Model</a></td><td>28</td><td>1</td><td>World Model</td><td>경제 시스템의 world model을 정의하고 가계 행동과 거시 전이를 학습해 counterfactual 시뮬레이션함. world model 정의는 흥미로우나 경제 도메인이고 로봇과 무관함</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2611.32562'>Sol$^{3}$: Accelerating Video Diffusion for Free via Hierarchical Sparse Attention Routing</a></td><td>27</td><td>2</td><td>Generative</td><td>video diffusion attention을 계층적 sparse routing으로 3.07배 가속함. world simulation도 평가했으나 training-free 효율화 공학에 가까움</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2611.32951'>OmniHarness-RSI: Modality-Aware Harness Evolution for Omnimodal Understanding</a></td><td>27</td><td>2</td><td>Multimodal</td><td>omnimodal 이해용 agent harness를 modality별로 인수분해해 코드 수정으로 진화시킴. 3개 benchmark에서 6~9퍼센트포인트 상승이나 agent workflow 튜닝 성격임</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2611.32151'>Let The Pixels Through: Rethinking Long Skip Connections for Scalable Pixel Diffusion</a></td><td>27</td><td>1</td><td>CV</td><td>pixel diffusion의 long skip을 비대칭화하고 adaGLU를 넣어 ImageNet FID 1.62를 냄. 이미지 생성 아키텍처 개선이라 로봇 연결 약함.</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2611.31513'>How to build and train your recurrent-depth model: A fixed-point perspective</a></td><td>27</td><td>1</td><td>LG</td><td>input injection이 Halpern iteration임을 보여 recurrent-depth 학습을 설명하고 Sparrow optimizer를 제안했으나 로봇 연결은 없음.</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2611.33014'>Training Lightweight Gaze Models without Target Gaze Annotation: What Makes a Good Teacher?</a></td><td>26</td><td>5</td><td>CV</td><td>gaze target estimation에서 teacher label 품질이 student에 미치는 영향을 11개 조건으로 통제 비교함. 검증 label 오류가 student 오차를 예측함(rho 0.91)이나 좁은 과제 분석임</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2611.32970'>FocusAnchor: Zero-Shot Metric Depth by Anchoring a Depth Foundation Prior to Focus Cues</a></td><td>26</td><td>4</td><td>3D Vision</td><td>depth foundation prior를 focus cue에 반복 정렬하는 zero-shot metric depth임. NYU AbsRel 36% 감소지만 depth-from-focus 특화 개선임</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2611.33101'>GREMLIN: Generating Random Environments for Meta-Learning with Interacting Networks</a></td><td>26</td><td>3</td><td>RL</td><td>무작위 신경 환경에서 RL 규칙을 meta-learning하는 시도이며 DQN보다 낮고 untrained teacher 대비 개선만 확인되어 결과가 약함</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2611.31463'>Geometric Control Analysis of an Internally Actuated Flying Wing</a></td><td>26</td><td>3</td><td>Control</td><td>moving mass 구동 비행 날개의 Lie bracket 기반 제어 가능성 분석과 MPC로 학습 요소가 없는 제어 이론임</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2611.32281'>StreamCoach: Proactive Sports Coaching via Continuous Visual Reasoning</a></td><td>26</td><td>2</td><td>Video</td><td>Ego-Exo4D 기반 스트리밍 스포츠 코칭 모델과 데이터셋임. 연속 추론과 개입 시점 학습은 흥미로우나 인간 동작 평가 도메인임.</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2611.32131'>Rethinking Reasoning Effort Training in Large Language Models: On-Policy Distillation or Reinforcement Learning?</a></td><td>26</td><td>1</td><td>NLP</td><td>reasoning effort 학습에서 RL과 on-policy distillation을 비교한 분석임. 신호 차이 설명은 유용하나 LLM 한정임.</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2611.32801'>Scaling Laws of Ensemble Uncertainty in Language Models</a></td><td>26</td><td>1</td><td>LG</td><td>LLM ensemble의 epistemic uncertainty가 세 가지 power law를 따른다고 보인 이론 분석이며 로봇 실험은 없음</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2611.31539'>Agent Evaluation Without Ground Truth: A Null Proportion Perspective</a></td><td>26</td><td>1</td><td>LG</td><td>ground truth 없이 e-value로 agent 결정의 질을 추정하는 통계 프레임워크임. 이론적 보장은 있으나 사례가 Python 최적화 하나이고 로봇 평가와는 간접적임</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2611.31559'>COGENT: A Modular Cognitive Architecture for Agentic User Simulation</a></td><td>26</td><td>1</td><td>Embodied AI</td><td>ACT-R 등 인지 이론으로 desktop 사용자 행동을 모듈식으로 시뮬레이션하는 COGENT임. memory와 intention 모듈 개입은 있으나 GUI 사용자 시뮬레이션 한정임</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2611.32585'>Understanding the Importance of Massive Activations through Adversarial Robustness</a></td><td>26</td><td>0</td><td>LG</td><td>massive activation이 adversarial robustness와 region migration에 연결됨을 보인 해석 연구로 로봇 연결 없음</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2611.32042'>Instant LiDAR: Feed-Forward Gaussian Reconstruction for LiDAR Simulation</a></td><td>25</td><td>4</td><td>3D Vision</td><td>LiDAR scan을 feed-forward Gaussian asset으로 분 단위에 복원함. 주행 시뮬레이션 비용을 낮추나 속도 개선 중심임</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2611.32409'>Delay-Tolerant Formation Tracking for Multi-AGV Systems via Reference-Shift Coupling</a></td><td>25</td><td>4</td><td>Control</td><td>지연이 있는 multi-AGV 대형 추종에 대해 Lyapunov 기반 수렴 증명을 준 제어 이론 논문임. 증명은 탄탄하지만 학습 기반 로봇 연구와는 거리가 멈</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2611.32475'>ROVO: Robust Rotation-Only Visual Odometry for UAVs at Low and Moderate Altitudes</a></td><td>25</td><td>4</td><td>Visual Odometry</td><td>UAV 단안 영상에서 회전만 추정해 depth 불확실성 전파를 막는 VO임. 아이디어는 단순하고 translation을 포기하는 설정이라 활용 범위가 좁음</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2611.33118'>Neural Implicit Representation for Bathymetry Estimation using Sidescan Sonar Imagery</a></td><td>25</td><td>4</td><td>3D Vision</td><td>sidescan sonar의 elevation 모호성을 반영한 differentiable neural rendering으로 수심을 추정함. 수중 센싱 응용이고 정량 수치는 초록에서 확인 불가임</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2611.31720'>EventSSM: Causal Spatial-State Modelling for Asynchronous Events Event-Depth Estimation</a></td><td>25</td><td>3</td><td>CV</td><td>event camera 입력으로 metric depth를 recurrent state로 추정함. 로봇 인식에 쓰일 수 있으나 benchmark 개선 중심임</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2611.31924'>Decompose, Verify, Evolve: Physically Grounded Shape Decomposition</a></td><td>25</td><td>3</td><td>3D Vision</td><td>VLM agent가 물리 검증을 거쳐 재질 포함 primitive 분해를 만듦. 시뮬레이션용 형상 표현에 쓸 수 있으나 로봇 task 검증은 없음</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2611.32311'>SynAVID: A Synthetic Audio-Visual Immersive Dataset of Dynamic Scenes</a></td><td>25</td><td>2</td><td>3D Vision</td><td>시점 의존 binaural 오디오를 포함한 합성 audio-visual 장면 dataset임(장면 8개). 오디오-시각 재구성 평가용 dataset이라 로봇 연결은 약함.</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2611.31258'>RECAP: Training Long-horizon LLM Agents with Context Compaction</a></td><td>25</td><td>2</td><td>NLP</td><td>요약이 원래 이력이 유발하는 행동을 보존해야 한다는 behavior distortion 목적으로 LLM agent의 context compaction을 RL로 학습함. BrowseComp-plus +4.6%, SWE-bench +4.3%로 개선 폭은 작고 memory 관점의 간접 시사점만 있음</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2611.31974'>Coding4Games: Can Modern Coding Agents Play Modern Video Games?</a></td><td>25</td><td>2</td><td>Embodied AI</td><td>coding agent가 게임 프로그램을 짜서 시각 입력으로 플레이하는 Coding4Games benchmark임. 게임 15종 평가로 embodied와 간접적이고 benchmark 성격임</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2611.31755'>RVLM-X: Towards a Universal VLM Harness</a></td><td>25</td><td>1</td><td>Multimodal</td><td>VLM이 code REPL로 고해상도 이미지를 재귀적으로 탐색하는 harness임. 고정 절차보다 유연하다는 관찰은 있으나 로봇과 직접 연결은 약함</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2611.32085'>ExpGuard: Guarding Long-Horizon LLM Agents against Corrupted Experience</a></td><td>25</td><td>1</td><td>NLP</td><td>agent가 재사용하는 경험의 오염 위험을 그래프로 예측하고 counterfactual replay로 라벨을 만듦. memory 안전성 관점이 있으나 LLM agent 대상이고 로봇과 무관함</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2611.31350'>GHC:Expanding Residual Interfaces in Hyper-Connections</a></td><td>25</td><td>0</td><td>LG</td><td>Hyper-Connections의 residual interface를 group별로 확장하는 GHC임. 학습 효율 35% 향상이나 LLM architecture 미세 개선이고 robotics 무관함</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2611.32588'>CoReQ: Condition-Aware Cross-Modal Repair and Quality-Guided Robust Collaborative Perception</a></td><td>24</td><td>5</td><td>CV</td><td>LiDAR와 4D Radar 간 조건 인지 cross-modal repair와 품질 기반 fusion으로 악천후 협력 인식을 개선함. 자율주행 인식 모듈 조합 수준의 기여임</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2611.31667'>Exteroceptive Sensor Faults in Autonomous Vehicles: A Cross-Modal Taxonomy and Fault Injection Toolkit</a></td><td>24</td><td>4</td><td>Robotics</td><td>자율주행 외부 센서 결함 taxonomy와 94개 fault injection toolkit이며 방법론 기여가 약함</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2611.32540'>Smooth Essential-Manifold Residuals for View-Graph Calibration</a></td><td>24</td><td>3</td><td>3D Vision</td><td>essential manifold 거리를 2x2 행렬 등거리 환원으로 다시 써 Gauss-Newton이 full rank가 되게 함. view-graph calibration의 수학적으로 깔끔한 개선이나 robot policy와는 거리 있음</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2611.33020'>GRAPE-Bench: When Vision Degrades, Does Video Reasoning Hold?</a></td><td>24</td><td>3</td><td>Video</td><td>visual degradation 하 video reasoning을 평가하는 GRAPE-Bench임. synthetic과 real의 ranking 역전을 보이나 benchmark 위주임</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2611.32817'>Beyond Image-Text Pairs: Aligning Semantic Changes for Fine-Grained Visual Understanding</a></td><td>24</td><td>2</td><td>Multimodal</td><td>시각, 텍스트 표현 변화의 방향을 맞추는 SDA loss와 VarFamily-40K로 CLIP류를 post-training함. compositional understanding 개선이나 작은 loss 추가 수준임</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2611.33009'>Train What You Run: Probabilistic Convolutions for Learning Token Compaction in State Space Models</a></td><td>24</td><td>2</td><td>Efficiency</td><td>token 제거로 바뀌는 이웃을 반영해 Mamba convolution의 기대값을 정확히 계산하는 ProbConv임. 강한 압축에서 이점이 커지나 비전 효율화 기법임</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2611.31856'>Start Where the Data Are: Statistical Priors for One-Step Generation on Manifolds</a></td><td>24</td><td>2</td><td>LG</td><td>통계적 prior와 posterior coupling으로 SO(3), torus 위 one-step generation을 개선함. 다양체 생성 방법이고 단백질 응용이 중심이라 로봇 연결은 약함.</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2611.32196'>What to Change, What to Keep: Experience-Evolving Agents for Video Recasting</a></td><td>24</td><td>1</td><td>Video</td><td>frozen 모델 위에서 경험을 원칙으로 쌓는 video recasting agent임. 경험 누적 아이디어는 흥미로우나 영상 편집 도메인이고 로봇 연결 약함.</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2611.31582'>LatentLens: Rethinking Latent Interface in Multi-Agent Systems</a></td><td>24</td><td>1</td><td>NLP</td><td>multi-agent latent interface를 harness와 분리해 보니 정확도가 오르지 않고 오히려 떨어진다는 부정적 결과를 보인 분석임. 로봇과 무관함.</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2611.32390'>Evolve to Learn: Gradient-aligned experience evolution for model self-improvement</a></td><td>24</td><td>1</td><td>NLP</td><td>경험 중 gradient 정렬이 높은 것만 self-distillation하는 LLM 자기개선 틀로 로봇과 무관하고 기여가 분석 중심임</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2611.33124'>SAG-Mem-1.0 Technical Report</a></td><td>24</td><td>1</td><td>NLP</td><td>대화 원문을 chunk로 보존하고 BM25와 lexical expansion으로 검색하는 SAG-Mem임. 구성이 단순하고 LoCoMo 점수 개선 중심이며 robot memory와는 거리가 있음</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2611.31939'>Beyond the Last Loop: Reinforcement Learning with a Teacher Extrapolated from the Model Itself</a></td><td>24</td><td>0</td><td>NLP</td><td>looped LM에서 첫 loop부터 마지막 loop까지 외삽한 분포를 teacher로 쓰는 ELGO이고 수학 벤치마크 평균 62.32에서 64.20으로 오른 소폭 개선임.</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2611.32782'>Measuring Layer-wise Intrinsic Dimensionality of FFNs in LLMs via PCA</a></td><td>24</td><td>0</td><td>NLP</td><td>LLM FFN 층별 intrinsic dimensionality를 58개 모델에서 측정해 pruning 폭 배분에 쓴 분석임</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2611.31950'>Beyond Rigid Hands: Deforming Skin into Contact-Consistent Hand Meshes</a></td><td>22</td><td>4</td><td>3D Vision</td><td>rigid hand mesh를 접촉이 일관된 skin 변형 mesh로 바꾸는 최적화임. grasp 안정성 개선은 있으나 hand-object 데이터 후처리 수준임</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2611.32184'>Wind-Aware Trajectory Planning for Deformable Aerial Formations</a></td><td>22</td><td>4</td><td>Robotics</td><td>도시 바람장을 고려한 변형 가능한 드론 편대 궤적 최적화로 시뮬레이션뿐인 고전 계획 연구임</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2611.32413'>A Face Robot which Imitates Human Musculoskeletal Skin System and Its Evaluation on Basic Movement of Facial Expression</a></td><td>22</td><td>4</td><td>Hardware</td><td>FACS 47개 AU 중 근육만으로 40개, 피부 부착 후 30개를 재현한 해부학 기반 얼굴 로봇 하드웨어임. 하드웨어 기여이며 학습·제어 방법론은 없음</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2611.32550'>Self-supervised quality evaluation of grid maps without ground truth</a></td><td>22</td><td>4</td><td>Mapping</td><td>occupancy grid patch의 autoencoder 재구성 오차로 지도 품질을 self-supervised로 평가함. 단순 이상치 탐지 수준이고 정량 지표가 초록에 없음</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2611.31918'>HiGS: A Hierarchical Architecture for Fast Differentiable 3D Gaussian Splatting</a></td><td>22</td><td>3</td><td>3D Vision</td><td>3DGS 렌더링과 학습의 tile 분할을 계층화해 속도와 메모리를 줄임. 시스템 최적화 기여이고 로봇 문제와 직접 연결은 약함</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2611.32628'>Completion-Aware Compression for Progressive 3D Gaussian Splatting</a></td><td>22</td><td>3</td><td>3D Vision</td><td>progressive 3DGS codec으로 임의 byte 예산에서 부분 복원을 지원하고 62~88배 압축함. 전송 측면 3DGS 연구로 로봇 응용과는 거리 있음</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2611.32981'>NEST: Uncovering and Nesting Unknown Objects in Open-World Object Detection</a></td><td>22</td><td>3</td><td>CV</td><td>top-k에서 버려지는 unknown 객체를 class-agnostic ranker로 살리고 Euler diagram으로 상위 범주에 배정함. open-world detection 개선이고 incremental임</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2611.32113'>PhysRF-WorldJEPA: Transforming Heterogeneous Large Language Models into Manifold-Decoupled Millimeter-Wave Radar World Models</a></td><td>22</td><td>3</td><td>World Model</td><td>mmWave radar를 LLM에 붙이는 JEPA 구조로 소규모 자체 데이터에서 검증함. 센서 도메인은 흥미로우나 world model 명칭에 비해 근거 범위가 좁음.</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2611.31836'>Gaze World Model</a></td><td>22</td><td>2</td><td>Video</td><td>world model 예측을 gaze 이동 탐지와 예측에 co-train함. 사람 주의 추정이 대상이라 로봇과의 연결은 약함</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2611.31883'>Rethinking Video Agents: When and Why Video Harnesses Work</a></td><td>22</td><td>2</td><td>Video</td><td>video harness가 언제 왜 도움이 되는지 Video-Relook으로 분석함. 적응적 관찰의 이득이 모델과 과제마다 갈린다는 분석은 active perception과 닿으나 로봇 환경은 아님</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2611.32675'>TokenMatte: Unlocking T2V Diffusion Priors for Pixel-Native Video Matting</a></td><td>22</td><td>2</td><td>Video</td><td>video DiT를 pixel-native linear readout으로 alpha matting에 적용함. VAE 우회로 1.51배 빠르나 matting 한정 방법임</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2611.32812'>Breaking the Joint Action Space Dependence in Distributionally Robust Multi-Agent Reinforcement Learning</a></td><td>22</td><td>2</td><td>RL</td><td>distributionally robust 다중 에이전트 Markov game의 표본 복잡도가 joint action 수에 의존하지 않음을 보인 순수 이론임</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2611.31589'>Spec$^2$R: Recovering Emergent Properties in Supervised Vision Transformers</a></td><td>22</td><td>1</td><td>CV</td><td>supervised ViT의 MLP가 고주파를 넣어 patch 표현 구조를 해친다는 spectral 분석과 가벼운 regularizer를 제안함. 로봇 직접 연결은 약함</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2611.31627'>What You See Is What You Certify: Concept-Based Certificates for Unseen Compositions</a></td><td>22</td><td>1</td><td>CV</td><td>concept bottleneck 모델이 unseen 조합에서 93-94% 틀린 인증을 한다는 점을 보이고 국소 crop 기반 설계를 제안함. 신뢰성 분석은 좋으나 로봇과는 거리 있음</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2611.31770'>ET: Efficient Transfer from Softmax to Hybrid Attention</a></td><td>22</td><td>1</td><td>LG</td><td>softmax attention을 gradient 없이 hybrid attention으로 바꾸는 효율 변환임. DiT와 SD3.5에서 속도 이득을 보이나 로봇 문제와 직접 연결은 없음</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2611.32227'>Relational Bottleneck Models</a></td><td>22</td><td>1</td><td>Multimodal</td><td>LVLM을 triplet 근거에 인과적으로 묶어 해석 가능하게 만드는 training-free 프레임워크임. 해석성 주제이고 로봇 관련은 약함.</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2611.32462'>MAGPIE: Agentic Multi-Reference Image Generation via Executable Scene Construction</a></td><td>22</td><td>1</td><td>Generative</td><td>다중 참조 이미지 생성을 Blender 프로그램 기반 3D scene 계획으로 제어하는 agentic 파이프라인임. 이미지 생성 도메인이고 로봇 연결 약함.</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2611.32617'>VenusOCR2.0: Towards Efficient and Effective Document Parsing</a></td><td>22</td><td>1</td><td>Multimodal</td><td>1B VLM 문서 파싱기에 self-improvement data engine과 parallel draft module을 더해 2.96배 가속함. 문서 OCR이라 robotics와 무관하고 공학 중심임</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2611.32971'>Teaching Time Without Losing General Retrieval: Adapting Multimodal Embeddings for Time-Sensitive Video Retrieval</a></td><td>22</td><td>1</td><td>Video</td><td>시간 민감 video retrieval에서 general retrieval을 유지하는 keep loss, pair loss, middle-layer LoRA를 제안함. 설계 근거 분석은 있으나 retrieval 한정임</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2611.31271'>Chain-of-Thought Is Not Explainability</a></td><td>22</td><td>1</td><td>NLP</td><td>CoT가 설명 가능성의 근거가 될 수 없다는 position paper로, CoT 중심 논문 1,000편 중 21.7%가 이를 설명 근거로 삼는다고 분석함. 새 실험 없이 기존 증거 종합이 중심임</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2611.31481'>SwiftLoop: Selective Refinement for Adaptive Implicit Reasoning in Looped Transformers</a></td><td>22</td><td>1</td><td>NLP</td><td>looped transformer의 position-wise freezing으로 추론 연산을 줄이는 방법이고 효율 기여는 있으나 LLM 추론 한정임.</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2611.31670'>Neural Interoperability Protocols: Specifying Compatibility Before Training</a></td><td>22</td><td>1</td><td>LG</td><td>신경망 모듈 간 호환성을 공개 인터페이스 명세로 정의하는 NIP 프레임워크로 개념은 있으나 통제 실험이 작고 로봇과 거리 있음.</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2611.32063'>Integral DeltaNet: Improved Linear Attention with Adaptive Memory Integration</a></td><td>22</td><td>1</td><td>NLP</td><td>delta state와 integral state를 함께 두는 linear attention Integral DeltaNet이고 언어 모델링 한정의 소폭 개선임.</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2611.32380'>The Activity Geometry of Discrete Generative Sampling</a></td><td>22</td><td>1</td><td>LG</td><td>discrete diffusion 샘플러의 coupling 비용을 activity로 정식화한 이론 논문이나 언어 생성 실험뿐이며 로봇 연결 없음</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2611.32515'>Branch and Consolidate: A Unified Recipe for Multi-Teacher On-Policy Distillation</a></td><td>22</td><td>1</td><td>Multimodal</td><td>발산한 specialist를 multi-teacher on-policy distillation으로 한 모델에 합치는 레시피이며 로봇 연결 없음</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2611.31727'>fork() for Agents: Agent Kernel for Non-blocking LLM Orchestration</a></td><td>22</td><td>1</td><td>NLP</td><td>agent 실행 중 노드가 실패하면 후손 노드만 다시 실행하는 Sub-Graph Recovery를 LLM runtime에 이식함. failure recovery 아이디어는 닿지만 툴 호출 workflow 수준이고 분산시스템 기존 패턴의 이식임</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2611.31641'>E2SIM: Long-Horizon Simulation of Everyday Human Behavior with Evolving States</a></td><td>22</td><td>1</td><td>Embodied AI</td><td>행위자 상태와 공유 환경이 서로 갱신되는 60일 장기 사용자 시뮬레이션 E2SIM임. 지연된 결과의 feedback loop 설계는 있으나 평가가 evaluator 판단과 1회 시뮬레이션뿐임</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2611.31736'>Reproducing History Is Not Enough: Intervention-Level Assurance for LLM-Generated Simulators</a></td><td>22</td><td>1</td><td>LG</td><td>LLM이 만든 시뮬레이터의 what-if 답을 개입 수준에서 검증하는 Vouch 제안임. 개입 기반 신뢰도 판정은 counterfactual 주제와 약하게 닿지만 로봇 시뮬레이션은 아님</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2611.32199'>Steerable by Design: Conditional Pretraining for Robust Control of Language Models</a></td><td>22</td><td>0</td><td>NLP</td><td>제어 channel을 분리한 steerable LM Mancelle-3B이고 LLM 제어 연구라 로봇과 무관함.</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2611.32866'>Weight Scale Rebalancing: Transferable Training Recipes for Transformers</a></td><td>22</td><td>0</td><td>LG</td><td>UDV 재매개변수화로 Transformer 학습 hyperparameter를 규모 간 전이시키는 방법이며 로봇과 무관함</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2611.32728'>Diving Deeper into Dense Keypoint Localization in Object Pose Estimation</a></td><td>20</td><td>5</td><td>3D Vision</td><td>Gray-binary encoding과 local refinement로 dense keypoint 6D pose를 개선함. LM-O ADD(-S) 1.4~1.9% 향상으로 incremental임</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2611.31956'>TACTUS: Unifying Surgical Action Understanding in Time and Space</a></td><td>20</td><td>4</td><td>CV</td><td>수술 행동의 도구, 접촉, 궤적을 통합 주석한 22,995 clip dataset임. 수술 자동화 기반 자료이나 dataset과 benchmark 기여에 머묾</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2611.31637'>A Self-Organizing Swarm Control Model for Underwater Robots Based on Turing-Type Reaction-Diffusion Principles</a></td><td>20</td><td>4</td><td>Robotics</td><td>Turing 패턴 원리를 쓴 수중 swarm 분산 제어로 2D 시뮬레이션만 검증함</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2611.31392'>Look Where Camouflage Breaks: Concealment-Guided Observation for Camouflaged Object Detection</a></td><td>20</td><td>2</td><td>CV</td><td>위장 물체 탐지에서 어느 crop을 다시 볼지 정하는 active observation 구조임. 이미지 안 crop 선택이라 실제 active perception은 아니고 적용 범위가 좁음</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2611.32542'>Align or Fail: The Hidden Gap in Cross-Domain Panoptic Segmentation</a></td><td>20</td><td>2</td><td>CV</td><td>DINOv3 backbone 교체 시 CLIP과의 grouping-recognition 불일치로 cross-domain이 무너지는 현상을 진단함. 분석은 유용하나 새 방법은 작은 LoRA 수준임</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2611.32828'>SAVERA: Bridging Frozen Vision and Language Models via Sparse Alignment and Visual Evidence Reuse</a></td><td>20</td><td>2</td><td>Multimodal</td><td>frozen vision과 language model을 sparse space에서 정렬하는 SPARE, BEAM, PRIVA 조합임. captioning과 VQA에서 경쟁 수준이고 module 구성이 복잡함</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2611.33096'>EventDiffusion: Learning Native Event Stream Distribution from Videos</a></td><td>20</td><td>2</td><td>Generative</td><td>RGB 영상에서 native event stream 분포를 사건 수, 공간 배분, 시간 세 단계 diffusion으로 학습함. event simulator의 가정 의존을 줄이나 event camera 데이터 생성 특화임</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2611.31479'>Transferable, Time-Parallel Graph Dynamics via Space-Time Factorization</a></td><td>20</td><td>2</td><td>LG</td><td>공간 mixer와 시간 연산자를 분리해 unseen graph에 zero-shot 전이하는 PDE surrogate이나 홍수, 교통 도메인이라 로봇과 거리 있음.</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2611.32092'>A Fused Gaussian Process Bandit Framework for Multi-Fidelity Bayesian Optimization</a></td><td>20</td><td>2</td><td>LG</td><td>multi-fidelity Bayesian optimization을 fused GP bandit으로 정식화하고 regret 보장을 줌. 이론은 있으나 로봇 응용 근거가 없음.</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2611.31265'>SD-Cache: Learnable Memory Consolidation with State-Guided Dynamic Caching</a></td><td>20</td><td>2</td><td>LG</td><td>고정 LLM 옆에서 KV state를 고정 크기 working memory로 통합하는 query-agnostic 캐시임. memory 압축 아이디어이나 RAG QA 대상이고 로봇 memory와는 거리 있음</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2611.31590'>GoldiBench: Right Tools, Wrong Amount -- Benchmarking Agents on Effect Judgement in Professional Editing</a></td><td>20</td><td>1</td><td>Multimodal</td><td>전문 편집 도구에서 agent가 효과의 양을 판단하지 못함을 benchmark로 보임. 반복 확인과 비교를 강제하면 성공률이 오르는 관찰은 흥미롭지만 로봇과는 거리 있음</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2611.31651'>Anchoring VAE Fine-Tuning to Its Latent Diffusion Prior</a></td><td>20</td><td>1</td><td>Generative</td><td>VAE fine-tuning을 latent diffusion prior에 anchoring하는 score-distillation regularizer임. depth, normal 등에서 오차를 4-7% 줄이나 로봇과는 간접적임</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2611.32045'>SegPFN: Training-Free In-Context Segmentation with Tabular Prior-Data Fitted Networks</a></td><td>20</td><td>1</td><td>CV</td><td>tabular PFN으로 in-context segmentation을 training-free로 풂. 발상은 신선하나 segmentation benchmark 범위임</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2611.32153'>SoccerNarrate: Event-Grounded Streaming Soccer Commentary with Macro-Window Preference Alignment</a></td><td>20</td><td>1</td><td>Video</td><td>스트리밍 축구 중계 생성에 macro-window preference alignment와 counterfactual negative를 쓴 도메인 특화 연구임. 로봇과 거리 있음.</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2611.32345'>LRQ-Cache: Compressing Feature Caches in Video Diffusion via Low-Rank Approximation and Quantization</a></td><td>20</td><td>1</td><td>Generative</td><td>video DiT feature cache를 low-rank와 양자화로 42~71배 압축하는 효율 추론 기법임. 로봇 관련성 약함.</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2611.32399'>Not All Pairs Align: Caption-Guided Audio-Visual Contrastive Learning</a></td><td>20</td><td>1</td><td>Multimodal</td><td>caption으로 audio-visual 쌍의 정렬도를 추정해 contrastive loss 가중치로 쓰는 작은 loss 개선임</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2611.32452'>The Teacher Is Already Inside: Self-Distilling Looped Language Models Beyond Their Last Loop</a></td><td>20</td><td>1</td><td>NLP</td><td>looped LM의 첫 loop에서 외삽한 분포를 self-distillation 타깃으로 쓰는 방법이며 수학 5개 benchmark의 소폭 개선임</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2611.32810'>EPRO: Robust Policy Optimization Through an Imperfect Execution-Policy Predictor</a></td><td>20</td><td>1</td><td>RL</td><td>LLM RL에서 rollout 엔진과 학습 엔진 policy 불일치를 보정하는 정책 최적화이며 수학 추론만 평가함</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2611.31821'>Exploring Multi-Player Social Games as Verifiable Training Grounds for Large Language Models</a></td><td>20</td><td>1</td><td>NLP</td><td>다인 사회 게임의 승패를 verifiable reward로 써서 Qwen3-4B 승률을 33%에서 81%로 올림. RLVR 적용 사례이나 언어 모델 사회 지능 한정임</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2611.33012'>Can LLM Judges Catch Unsafe Clinical Actions? A Fault-Injection Study</a></td><td>20</td><td>1</td><td>NLP</td><td>임상 agent trajectory에 오류를 주입해 LLM judge의 위험 행동 검출력을 평가함. failure detection 관점은 있으나 EHR 도메인이고 로봇과 무관함</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2611.31605'>Noise-Level Adjacency in Diffusion Training</a></td><td>20</td><td>0</td><td>CV</td><td>diffusion 학습에서 noise level 인접성이 weight sharing 이득의 원인임을 밝히는 분석이고 로봇과 거리 있음.</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2611.32324'>When Exact Token Importance Is Not Enough: Limits of Top-K Selection in LLM Attention</a></td><td>20</td><td>0</td><td>NLP</td><td>attention top-K 선택에서 개별 중요도 순위가 최적 쌍을 보장하지 않음을 보인 분석이고 로봇과 무관함.</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2611.32762'>SGD with Large Learning Rates: General Analysis &amp; Improved Rates</a></td><td>20</td><td>0</td><td>LG</td><td>큰 learning rate의 SGD가 확률적 환경에서도 가속됨을 보인 최적화 이론으로 로봇 연결 없음</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2611.32969'>Eliciting the Recall Capacity of Linear Attention</a></td><td>20</td><td>0</td><td>NLP</td><td>linear attention의 associative recall 부족을 학습 개입으로 줄인 언어 모델 연구임</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2611.33031'>Can a Frontier LLM Repair a Quantized Network by Tool-Free Weight-Space Programming?</a></td><td>20</td><td>0</td><td>LG</td><td>Claude 계열 LLM이 도구 없이 4-bit CNN 가중치를 고쳐 정확도를 회복하는지 본 소규모 실험이며 20k 파라미터 CNN 한정임</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2611.33062'>Understanding Clipping In Zeroth-Order Optimization</a></td><td>20</td><td>0</td><td>LG</td><td>zeroth-order 최적화에서 per-sample clipping이 성능을 높이는 현상을 분석한 LLM fine-tuning 연구임</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2611.31966'>On the Information Loss of Multi-Token Prediction: Origin and Solution</a></td><td>19</td><td>0</td><td>NLP</td><td>multi-token prediction의 누적 정보 손실을 분석하고 dual-context 학습으로 보완함. 점수 개선은 최대 2.46점으로 작음.</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2611.31922'>TANDEM: Temporal Anchor Densification With Reliability-Aware Memory for Lightweight Sparse Depth Completion in Endoscopic Robotic Navigation</a></td><td>18</td><td>3</td><td>CV</td><td>내시경 로봇용 sparse depth completion에 신뢰도 기반 temporal memory를 둠. 도메인이 의료 영상으로 좁고 benchmark 개선 중심임</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2611.31729'>DAA for an Autonomous Delivery Drone: Maneuver Selection Policies for Near-Collision Risk Avoidance</a></td><td>18</td><td>3</td><td>Robotics</td><td>배달 드론 near-collision 회피 기동을 기하 기반으로 비교한 연구로 학습 요소가 없음</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2611.32381'>Does Research-Paper Context Improve LLM-Generated Quadruped Navigation? An Exploratory Simulation Study</a></td><td>18</td><td>3</td><td>Embodied AI</td><td>논문 context 제공이 LLM 생성 사족보행 navigation 코드를 개선하는지 본 소규모 탐색 연구임. 컨트롤러 8개 수준 표본에서 오히려 악화(2/8 대 7/8)를 보고했고 로봇 학습 기여는 약함</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2611.32099'>PreferenceScene: Personalized Indoor Scene Synthesis from Feedback</a></td><td>18</td><td>2</td><td>Embodied AI</td><td>사용자의 부분 feedback에서 숨은 선호를 추정해 실내 3D scene을 바꿔 가는 방법임. language feedback 활용은 있으나 장면 생성이고 로봇 task가 아님</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2611.32332'>GUI-WEdit and GUI-SkillEvo: Gradient-Free Adaptation of Small GUI Agents</a></td><td>18</td><td>2</td><td>Embodied AI</td><td>소형 GUI agent를 MLP 일부 closed-form 갱신이나 skill 개선으로 gradient-free 적응함(OSWorld 부분집합 48.02%). 로봇 아닌 데스크톱 agent이고 개선폭 비교 대상이 초록에 없음.</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2611.31435'>Tornado4D: Physics-Guided 4D Gaussian Reconstruction of a Laboratory Tornado from Sparse One-Sided Videos</a></td><td>18</td><td>1</td><td>3D Vision</td><td>실험실 토네이도를 물리 기반 airflow prior로 4DGS 복원함. 특수 대상이고 로봇 활용은 거의 없음</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2611.31471'>PromptSMC: Enabling Particle Exploration in Flow Matching via LLM-Based Prompt Rejuvenation</a></td><td>18</td><td>1</td><td>Generative</td><td>flow matching에서 LLM이 prompt를 고쳐 SMC particle을 탐색하는 inference-time 정렬임. 이미지 생성 한정이라 로봇 연결은 약함</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2611.31891'>Open-OmniCoach: Evidence-Enhanced Trajectory Learning for Omni Video Agents</a></td><td>18</td><td>1</td><td>Video</td><td>omni video agent를 evidence 기반 trajectory와 step-level RL로 학습함. 영상 이해 benchmark 개선 중심이고 로봇과는 거리 있음</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2611.31987'>InCue: Making Better Use of What Multimodal LLMs Already See at Test Time</a></td><td>18</td><td>1</td><td>Multimodal</td><td>MLLM 내부 attention과 entropy gradient로 visual token offset을 test time에 최적화함. 아이디어는 흥미로우나 VQA 범위임</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2611.32407'>Every Edit Its Own Budget: Per-Instruction Token Freezing for Training-Free Acceleration of Multi-Edit Image Editing</a></td><td>18</td><td>1</td><td>Generative</td><td>multi-edit 이미지 편집에서 instruction part별 token freezing 예산을 주는 training-free 가속임(최대 4.89배). 이론 분석은 있으나 로봇 무관함.</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2611.31730'>Tokenization and Architecture Jointly Allocate Component Roles in Time Series Transformers</a></td><td>18</td><td>1</td><td>LG</td><td>시계열 transformer에서 attention과 FFN의 feature 구성 역할을 probing으로 분석함. 해석 연구이고 로봇과 무관함.</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2611.32064'>Fix How It Acts, Not How It Thinks: Surgical Fine-Tuning of Frontier LLMs</a></td><td>18</td><td>1</td><td>NLP</td><td>LoRA 업데이트가 양자화 merge에서 사라지는 문제를 merge-aware fine-tuning으로 해결함. coding agent 한정 엔지니어링임.</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2611.33064'>U-Statistics-Powered LLM Reasoning</a></td><td>18</td><td>1</td><td>RL</td><td>GRPO group size를 U-statistic 분산비 추정으로 적응 선택하는 방법이며 LLM 추론 과제만 평가함</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2611.32660'>Bathys: Advancing Deep Search Agents</a></td><td>18</td><td>1</td><td>NLP</td><td>검증 가능한 질문 합성, SFT, KTO, context compression 하의 online RL로 deep search agent를 학습함. 장기 agent RL recipe이나 웹 검색 한정이고 로봇 연관 낮음</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2611.33106'>Temporal Conditioning for Human Behavioral Cloning in Chess</a></td><td>18</td><td>1</td><td>LG</td><td>체스 인간 behavioral cloning에 남은 시간 조건을 추가함. 인간 모방 모델링 관점은 있으나 개선폭이 작고 로봇과 무관함</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2611.32989'>AVQ-Attention-2: Adaptive Vector-Quantized Attention with Exact Local Blocks and Linear-Cost Training</a></td><td>18</td><td>0</td><td>LG</td><td>vector-quantized attention에 exact local block을 더해 선형 비용 학습을 하는 효율 개선임</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2611.33133'>A Bias in Disguise: Tiny Gradient Edits Stop a Small Language Model&#x27;s Thinking Loops and Complement a Frontier Model&#x27;s Weight Edit</a></td><td>18</td><td>0</td><td>NLP</td><td>작은 LM의 thinking loop를 소수 가중치 gradient 편집으로 멈추는 실험이며 로봇과 무관함</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2611.31595'>LUCID: Statistically Grounded Self-Correction for LLM Reasoning Evaluation</a></td><td>18</td><td>0</td><td>NLP</td><td>LLM step rater의 편향을 소량 전문가 라벨과 prompt self-correction으로 보정하는 평가 방법이며 로봇과 무관함. 통계적 보정(DSL) 설계는 깔끔하나 reasoning 평가 한정임</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2611.32384'>Can AI Design a Better nnU-Net? A Hypothesis-Driven Architecture Discovery Loop from Failures to Design Rules</a></td><td>18</td><td>0</td><td>CV</td><td>LLM agent가 실패 분석으로 nnU-Net 설계 규칙을 도출하는 탐색 루프임. 실패 기반 가설 검증 아이디어는 있으나 의료 분할 대상임</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2611.32621'>ShapeQuest: Towards Granularity-Controlled Edit-Conditioned 3D Asset Retrieval</a></td><td>17</td><td>2</td><td>3D Vision</td><td>편집 지시 조건의 3D asset retrieval benchmark와 baseline 모델임. mAP 48.6에서 50.4로 오른 수준이라 기여 폭이 작음</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2611.33016'>RePix-VFI: Re-rendering Observed Pixels for Video Frame Interpolation with Generative Priors from One-Step Diffusion</a></td><td>17</td><td>1</td><td>Video</td><td>one-step video diffusion과 keyframe 픽셀 재렌더링으로 frame interpolation을 함. SNU-FILM에서 PSNR이 오르고 32~42배 빠르나 VFI 특화임</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2611.33153'>DiaCap: Jointly Learning Who Speaks When for Audiovisual Dialogue Captioning</a></td><td>17</td><td>1</td><td>Multimodal</td><td>발화, 시간, 화자를 함께 내는 audiovisual dialogue captioning 모델임. 2단계 학습과 RL 구성이지만 robotics 무관함</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2611.31558'>Denoising Diffusion with Progressive Posterior Sampling</a></td><td>17</td><td>1</td><td>CV</td><td>diffusion prior 기반 noisy inverse problem에서 SVD 없이 noise 분산을 추정하는 posterior sampling이고 복원 벤치마크 개선 수준임.</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2611.31575'>Latent Channel Completion for Forecasting in Sensor Networks with Failed Detectors</a></td><td>17</td><td>1</td><td>LG</td><td>고장 난 센서의 latent를 JEPA식으로 복원해 교통 예측을 지키는 방법이나 도로 detector 데이터에 한정됨. sensor dropout 대응 아이디어는 로봇 센서 고장에 일부 참고됨.</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2611.31790'>Byte Patches versus BPE at Matched Data: A Matched-Twin Comparison at 350M Parameters</a></td><td>17</td><td>0</td><td>NLP</td><td>350M byte-patch와 BPE를 매칭 비교한 결과 BPE가 우세함. 단일 크기, 단일 seed라 범위가 좁고 로봇과 무관함.</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2611.32143'>Calibrated Reading of Latent Reasoning and Communication</a></td><td>17</td><td>0</td><td>NLP</td><td>latent reasoning을 읽는 conformal 보정 reader CLR이고 로봇과 무관함.</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2611.32416'>On the Importance of Hidden-State Refinement in Masked Diffusion Language Models</a></td><td>17</td><td>0</td><td>NLP</td><td>masked diffusion LM의 layer 및 denoising step 간 hidden state 정련을 분석하고 CSRR로 step 간 hidden state를 전달함. diffusion 생성 일반에 시사점은 있으나 텍스트 한정임</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2611.32551'>UnifiedAD: One-Shot Anomaly Detection across Modalities via Evidence Calibration</a></td><td>16</td><td>1</td><td>CV</td><td>한 장의 normal reference로 단일, 다중 modality 이상 탐지를 통합하는 training-free 방법임. 산업 이상 탐지 benchmark 개선 위주임</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2611.31533'>JevBench: Metamorphic Coherence Testing for Typed Probabilistic Decision Models</a></td><td>16</td><td>1</td><td>LG</td><td>typed probabilistic decision model의 확률 coherence를 metamorphic relation 50개로 검사하는 벤치마크이고 로봇 관련성 낮음.</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2611.32269'>Pando: Noise-Coupled Parallel Draft Trees for Efficient Edge Speculative Decoding</a></td><td>16</td><td>1</td><td>NLP</td><td>edge speculative decoding용 draft tree Pando로 AR 대비 5.3배 속도를 냄. LLM 추론 효율이고 로봇 직접 관련은 약함.</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2611.32815'>E(n)-Equivariant Spherical Decision Surfaces</a></td><td>16</td><td>1</td><td>LG</td><td>E(n) 등변 구형 decision surface를 닫힌 형태로 유도한 workshop 수준 이론이며 실험이 얕음</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2611.31921'>Rethinking Universal Time Series Foundation Models from Unified Representations to Shared Dynamics (UniTFU)</a></td><td>16</td><td>0</td><td>LG</td><td>반복되는 지역 동역학을 재사용 단위로 쓰는 시계열 foundation model이고 로봇과 무관함.</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2611.32504'>InducedTFMs: A Family of Sub-Quadratic Tabular Foundation Models Using Induced Attention</a></td><td>16</td><td>0</td><td>LG</td><td>tabular foundation model의 attention을 induced attention으로 바꿔 비용을 줄인 효율 개선임</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2611.33048'>Latent Merger: Latent-Space Composition of Hypernetwork-Generated LoRAs</a></td><td>16</td><td>0</td><td>NLP</td><td>hypernetwork가 만든 LoRA를 latent 공간에서 합성하는 LLM 지식 주입 연구임</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2611.33111'>Draft Calibration for Speculative Decoding: Accelerating LLM Serving by Matching Draft and Target Distributions</a></td><td>16</td><td>0</td><td>NLP</td><td>speculative decoding draft에 temperature scaling을 적용해 acceptance length를 약 10% 올린 사후 보정임</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2611.32584'>An XR-Based System for Enhanced Spatial Awareness in Mobile Robot Teleoperation</a></td><td>15</td><td>4</td><td>Teleoperation</td><td>XR 이중 카메라와 LiDAR 기반 haptic 진동 피드백으로 원격조작 인지 부하를 줄임. 참가자 20명 사용성 평가 수준이고 학습 요소가 없음</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2611.32760'>Risk-Informed Path Planning: Collision and Grounding Avoidance Application for Autonomous Surface Vessels</a></td><td>15</td><td>3</td><td>Planning</td><td>Bayesian belief network 위험 지수를 RRT*에 넣은 선박 경로 계획임. 해양 도메인의 고전 planning이고 단일 시뮬레이션 시나리오로만 시연함</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2611.31977'>Distill to Loop: Turning Pretrained Diffusion Transformers into Looped Models with Adjustable Depth</a></td><td>15</td><td>1</td><td>Generative</td><td>pretrained diffusion transformer를 looped 모델로 distillation해 test time 깊이를 조절함. 효율 기법이나 이미지 생성 범위임</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2611.31988'>Describe, Don&#x27;t Decide: Correcting Answer Bias in Multimodal LLMs</a></td><td>15</td><td>1</td><td>Multimodal</td><td>MLLM이 각 대상을 따로 묘사한 뒤 이미지 없이 결정하는 training-free 편향 교정임. 로봇과 직접 연결은 약함</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2611.32536'>RSReasoner: Reformulating and Auditing Geospatial Reasoning Segmentation</a></td><td>15</td><td>1</td><td>Multimodal</td><td>지리공간 reasoning segmentation의 질의 유형을 재정의하고 대규모 데이터와 진단 benchmark를 만듦. 원격탐사 한정 benchmark 기여임</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2611.32825'>EEG-World: Context-Conditioned Dynamics of the Watching Brain</a></td><td>15</td><td>1</td><td>World Model</td><td>EEG 대역 power 동역학을 recurrent world model로 예측함. 신경과학 응용이고 로봇 연결 약함</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2611.31492'>Trust-Region Optimization for Performative Prediction without Response Modeling</a></td><td>15</td><td>1</td><td>LG</td><td>반응 모델 없이 performative risk를 최적화하는 trust-region 이론으로 수렴 보장은 있으나 로봇 관련성 낮음.</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2611.32948'>Beyond Expected Value: PPO with Distributional Critics for Systematic Conservation Planning</a></td><td>15</td><td>1</td><td>RL</td><td>보존 계획에서 ES를 PPO와 분포형 critic(IQN)으로 교체함. 저자도 이득이 granularity 때문이라 밝혀 기여가 훈련 효율에 그치고 로봇과 무관함</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2611.32302'>Query-Guided Visual Minimization for Selective Disclosure to Cloud VLMs</a></td><td>15</td><td>0</td><td>Multimodal</td><td>클라우드 VLM에 보내기 전 질의 관련 시각 정보만 남기는 프라이버시 기법임. 로봇과 거리가 멂.</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2611.31995'>Metric-Dependent Scaling Laws for Sketched Multiclass Softmax Regression</a></td><td>15</td><td>0</td><td>LG</td><td>sketched softmax regression의 metric 의존 scaling law 이론이고 로봇과 무관함.</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2611.31931'>Scoring What Matters: Exact Feedback Reduction for Language Model Comparison</a></td><td>15</td><td>0</td><td>LG</td><td>GRPO 등에서 평균 비교에 불필요한 scoring query를 정확히 제거하는 CAFA를 제안함. 평가 비용 절감 통계 도구이며 로봇 연관은 간접적임</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2611.32161'>Making Evaluation Explicit Is Not Enough: Supervising the Evaluation Process in Generative Reward Models</a></td><td>15</td><td>0</td><td>NLP</td><td>rubric 기반 generative reward model의 중간 평가 과정까지 supervision하는 STEP-GRM임. reward model 정확도 개선 위주이며 로봇 reward와는 거리가 있음</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2611.32166'>RightDiff: Learning Generative Reward Models to Judge by the Right Differences</a></td><td>15</td><td>0</td><td>NLP</td><td>pairwise 차이를 찾아 pair-specific rubric을 만드는 generative reward model RightDiff임. RewardBench 개선 위주이고 로봇 무관함</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2611.31794'>AGL-SKILL: Coding Harnesses as Agentic Optimizers</a></td><td>15</td><td>0</td><td>NLP</td><td>coding agent가 skill을 스스로 최적화하면 기존 skill 최적화 방법보다 낫다는 관찰임. 새 방법론이 약하고 로봇과 무관함</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2611.31932'>Contrastive On-Policy Self-Distillation for LLM Unlearning</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM unlearning을 counterfactual 목표 분포로 on-policy self-distillation하는 방법임. 로봇과 무관하고 NPO 대비 개선 위주임</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2611.31498'>XRL4T1D: A Post-hoc Explainability Framework for Reinforcement Learning in Type 1 Diabetes Management</a></td><td>14</td><td>2</td><td>RL</td><td>인슐린 투여 RL policy를 SHAP로 사후 설명하는 XRL4T1D임. RL policy 해석 사례이나 시뮬레이터 당뇨 제어이고 controller 간 일관된 구분은 없음</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2611.32046'>From Rule-based to Agentic: LLM Agent based Real-time Control of Urban Drainage Systems for Flooding and Sewer Overflow Mitigation</a></td><td>14</td><td>2</td><td>RL</td><td>LLM agent 두 개로 기상 경보를 반영해 배수 시스템을 제어함. 제어 문제이나 시뮬레이션 10개 강우 사건 검증이고 로봇과는 거리 있음</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2611.32035'>DeCo-Attention: Decompose to Compensate for Low-Precision Attention</a></td><td>14</td><td>1</td><td>LG</td><td>FP4 attention의 양자화 오차를 주성분 방향으로 보정해 video DiT를 빠르게 함. 시스템 최적화이고 로봇과는 거리 있음</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2611.32096'>Rethinking Post-Training Quantization for Large Vision-Language Models</a></td><td>14</td><td>1</td><td>Multimodal</td><td>LVLM의 W4A4 양자화에서 outlier 문제를 Hadamard 변환과 group quantization으로 완화함. efficient inference이나 로봇 특화 요소는 없음</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2611.32518'>HS-OVSeg: Multi-Granularity Open-Vocabulary Semantic Segmentation in Remote Sensing via Heterogeneous Supervision</a></td><td>14</td><td>1</td><td>CV</td><td>SAM3 pseudo-label과 LoRA로 원격탐사 open-vocabulary segmentation을 이종 supervision으로 학습함. 도메인 특화 데이터 활용이라 robotics 연결 약함</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2611.32658'>Attack-Inference Aligned Universal Adversarial Attacks on Video Object Segmentation</a></td><td>14</td><td>1</td><td>CV</td><td>VOS의 initialization-propagation 두 단계에 맞춘 universal adversarial perturbation임. 공격 성능은 높으나 robotics 연결 약함</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2611.32890'>Biomechanically Grounded Prediction of Selective Motor Control and Clinical Outcomes from Infant Video</a></td><td>14</td><td>1</td><td>CV</td><td>영아 영상에서 관절각을 추정해 뇌성마비 선택 운동 제어를 예측함. 임상 응용이라 robotics 무관함</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2611.31439'>Transformers with Signatures: Towards Universal In-Context Learning in Path Space</a></td><td>14</td><td>1</td><td>LG</td><td>path signature 기반 in-context learning 이론으로 유한표본 오차 한계를 보였으나 금융 예측 중심이라 로봇 연결 약함.</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2611.31256'>Directly Maximizing On-policy Expected Accepted Length for Speculative Decoding</a></td><td>14</td><td>1</td><td>LG</td><td>speculative decoding에서 accepted length를 직접 최대화하는 on-policy draft 학습임. LLM 추론 효율 기법이라 로봇 직접 연결은 약함</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2611.31884'>HEAR, SEE, SPIKE ONCE: Highly Efficient NeuroAI Temporal Neural Networks for Low-Precision Multimodal Audio-Visual Classification and Online Learning</a></td><td>14</td><td>1</td><td>LG</td><td>4비트 정수와 spike timing 학습으로 오디오-비주얼 분류를 하는 저전력 SNN임. 효율은 인상적이나 로봇 정책과 무관한 분류 benchmark임</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2611.32242'>Can You Find the Edit When Nothing Looks Wrong? A Paired Benchmark for Text-Driven Image Manipulation Localization Beyond Semantic Abnormality</a></td><td>14</td><td>0</td><td>CV</td><td>텍스트 기반 편집 위치 탐지 benchmark로 plausible edit에서 IoU가 낮은 격차를 보임. 로봇 무관하고 benchmark 기여임.</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2611.32532'>Rescuing Discarded Boundary Samples in Semi-Supervised Learning</a></td><td>14</td><td>0</td><td>LG</td><td>confidence threshold로 버려진 boundary sample을 soft pseudo-label로 되살리는 SSL add-on임. 분류 오류 4.97퍼센트포인트 감소지만 incremental임</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2611.32903'>IMPACT-Seg: Consistent Anatomical Segmentation and Representation Learning Across CT, CBCT, and MRI</a></td><td>14</td><td>0</td><td>CV</td><td>CT, CBCT, MRI 126개 구조 segmentation과 cross-modality 표현 학습임. 의료 영상 특화이고 robotics 무관함</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2611.33003'>One, No One and One Hundred Thousand CTs: Testing Anatomical Control in Text-to-CT Generation</a></td><td>14</td><td>0</td><td>Generative</td><td>text-to-CT 생성기의 credibility와 control을 시험하는 toolkit임. 의료 생성 평가이고 robotics 무관함</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2611.33147'>One Take, Many Cameras: Audio-Grounded Shot Synthesis for Dialogue Re-Cinematography</a></td><td>14</td><td>0</td><td>Video</td><td>단일 wide 대화 영상에서 audio-grounded로 다른 카메라 shot을 합성함. 영상 후반 작업용이고 robotics 무관함</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2611.33151'>BioLoom: Scaling Biomedical Vision-Language Models by Learning from the Structure of Scientific Articles</a></td><td>14</td><td>0</td><td>Multimodal</td><td>논문 figure 구조를 contrastive supervision에 넣은 biomedical CLIP임. 의료 도메인 scaling이고 robotics 무관함</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2611.31615'>Eliciting sandbagged LLM capability via structural interventions on attention-head functional networks</a></td><td>14</td><td>0</td><td>NLP</td><td>attention head 기능 그래프로 LLM sandbagging을 분석하고 능력을 되살리는 연구이고 로봇 관련성 없음.</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2611.32039'>FlashQLA: Efficient Context Parallelism for Gated DeltaNet</a></td><td>14</td><td>0</td><td>LG</td><td>Gated DeltaNet의 context parallel 커널 최적화이고 시스템 엔지니어링 성격임.</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2611.32041'>Spec-CoFrGeNet: Reparametrizing Continued Fraction Networks for Stable and Accurate Training</a></td><td>14</td><td>0</td><td>LG</td><td>continued fraction network의 pole 문제를 reparametrization으로 완화함. 아키텍처 효율 연구이고 로봇과 무관함.</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2611.32294'>DAiSy: Online Data Selection by Adaptive Utility Estimation for LLM Pretraining</a></td><td>14</td><td>0</td><td>NLP</td><td>선형 보조 모델로 LLM 사전학습 data utility를 예측하는 DAiSy이고 로봇과 무관함.</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2611.32624'>HiCal: Offline Calibration for Hierarchical Scale Encoding in Accurate HiF4 Quantization</a></td><td>14</td><td>0</td><td>LG</td><td>HiF4 block floating-point 양자화의 scale 인코딩을 offline 보정하는 LLM 추론 효율 개선임</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2611.32873'>MXFP4 for LLM Inference: Complementary Post-Training Quantization Techniques and Their Interactions</a></td><td>14</td><td>0</td><td>LG</td><td>MXFP4와 NVFP4 양자화 기법 조합을 비교하고 scale 선택 Midmax를 제안한 LLM 추론 효율 연구임</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2611.33004'>LEGOSpec: A Composable and Efficient Framework for Speculative Draft Design and Training</a></td><td>14</td><td>0</td><td>NLP</td><td>speculative decoding draft 설계 요소를 분해하고 acceptance length를 개선한 LLM 서빙 공학임</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2611.33023'>PAC-style Bounds on the Conditional Validity of Conformal Predictors</a></td><td>14</td><td>0</td><td>LG</td><td>conformal predictor의 conditional coverage에 PAC형 하한을 도출한 통계 이론임</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2611.33080'>Shifter Quantization: Compact Representations for Native Integer Computation</a></td><td>14</td><td>0</td><td>LG</td><td>Shifter Quantization으로 LLM groupwise 정수 추론 처리량을 높인 양자화 공학임</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2611.31771'>SPARQL-Planned Single-Hop Traversal over a Live Knowledge Graph for Multi-Hop Question Answering</a></td><td>14</td><td>0</td><td>NLP</td><td>dense retrieval과 Wikidata 순회를 섞어 multi-hop QA를 개선함. SPARQL을 실행하지 않고 파싱만 하는 점이 특이하나 QA 벤치마크 개선 위주임</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2611.31979'>Reading, Writing and Repairing Game-Theoretic Policies in Weight Space</a></td><td>14</td><td>0</td><td>LG</td><td>LM이 반복 게임 policy network의 weight를 읽고 쓰고 고치는 능력을 시험함. weight space 조작은 흥미로우나 1,218 weight 장난감 문제이고 repair는 4/18에 그침</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2611.32246'>SkillCore: Internalizing Generalizable Skills via Scaffolding-Removed Fine-Tuning</a></td><td>14</td><td>0</td><td>NLP</td><td>runtime skill을 scaffolding 제거 fine-tuning으로 모델에 내재화하는 SkillCore임. agent skill 개념은 닿으나 코드 agent SFT recipe 수준임</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2611.31301'>MOZAIC: An Audio-Video Deepfake Benchmark for Telling What Is Fake</a></td><td>14</td><td>0</td><td>CV</td><td>audio-video deepfake를 4-way label로 나눈 MOZAIC 벤치마크임. 모달리티 기여를 분리 측정하는 설계는 좋으나 deepfake 탐지 도메인임</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2611.31571'>Safe Autoformalization: Sufficiency and Necessity with Entailment Graphs</a></td><td>14</td><td>0</td><td>LG</td><td>entailment graph로 autoformalization의 충분, 필요 frontier를 증명 가능하게 구함. Lean 검증 이론은 견고하나 AWS 정책 20건 평가이고 로봇 무관함</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2611.31638'>Wavefront: Low-Rank Drafting with Parallel Causal Refinement for Speculative Decoding</a></td><td>14</td><td>0</td><td>LG</td><td>low-rank base와 parallel Jacobi refinement로 speculative decoding drafter를 가속하는 Wavefront임. 처리량 이득이 2.6%에서 28.9% 수준이고 엔지니어링 성격임</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2611.31747'>FN-Prune: Training-Free Expert Pruning with Finite RMSNorm Perturbations</a></td><td>14</td><td>0</td><td>LG</td><td>RMSNorm 섭동으로 MoE expert를 가지치기하는 training-free 기준임. efficient inference이나 로봇 문제와 연결 없고 LLM perplexity 개선 위주임</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2611.31938'>CAPE: Coordinating Calibration and Search for Tool-Use Policies</a></td><td>14</td><td>0</td><td>NLP</td><td>도구 호출 설정 불일치에서 calibration과 search를 함께 컴파일하는 CAPE임. 기호적 tool-use 정책 문제로 로봇과 무관함</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2611.31969'>DexOPD: Dual-Extrapolation On-Policy Distillation for Diffusion Models</a></td><td>14</td><td>0</td><td>CV</td><td>text-to-image diffusion의 multi-teacher on-policy distillation에 student self-extrapolation을 더함. 이미지 생성 benchmark 개선 위주이고 로봇과 무관함</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2611.31990'>How Much Dependency Can a Marginal Rule See? Total Correlation in Diffusion LM Parallel Decoding</a></td><td>14</td><td>0</td><td>NLP</td><td>diffusion LM 병렬 디코딩에서 total correlation 예측 정확도를 측정하는 분석임. 로봇과 무관하고 NeurIPS workshop 규모의 분석임</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2611.32918'>InstructReplay: Replaying Assistant Turns to Preserve General Behavior During Factual Fine-Tuning</a></td><td>14</td><td>0</td><td>NLP</td><td>사실 fine-tuning 중 일반 능력 소실을 자기 응답 replay로 막음. 간단하고 효과는 크나 LLM 대상이고 로봇과 무관함</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2611.33065'>Auditing the Judge: Human-Derived Bias Discovery, Quantification, and Mitigation in LLM Judges</a></td><td>14</td><td>0</td><td>NLP</td><td>사람 판단 불일치에서 LLM judge의 편향 요인을 찾고 회귀로 보정하는 HUB-J임. 로봇과 무관함</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2611.32863'>CityRecast: Suppressing Persistent Artifacts in Generative Satellite 3D Reconstruction</a></td><td>13</td><td>1</td><td>3D Vision</td><td>위성 3DGS의 ghosting을 warm-up과 replacement로 줄임. 위성 재구성 특화이고 incremental임</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2611.32996'>PAVE: Preference-Aligned Visual Egocentric Learning for the Blind and Low-Vision Users</a></td><td>13</td><td>1</td><td>Multimodal</td><td>시각장애인 egocentric QA를 선호 정렬 dataset과 Filter-GRPO로 개선함. assistive 응답 품질 중심이고 로봇과 거리 있음</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2611.32823'>Reliable and grounded reporting of any computed tomography scan with FORA</a></td><td>13</td><td>0</td><td>CV</td><td>CT 1,028개 concept 인식과 report 생성 모델 FORA임. 의료 영상이라 robotics 무관함</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2611.32993'>Decision-Native Multimodal Clinical Modeling via Anatomical Grounding and Confidence Calibration</a></td><td>13</td><td>0</td><td>Multimodal</td><td>CT 의사결정용 counterfactual confidence supervision과 anatomy 압축 token을 쓴 의료 VLM임. robotics 무관함</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2611.31320'>Layer-Readout Interfaces in EEG Foundation Models: Predictive Accessibility and Cross-Dataset Transfer</a></td><td>13</td><td>0</td><td>LG</td><td>EEG foundation model의 중간 layer readout 효과를 분석함. EEG 한정임</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2611.31486'>CHORD: Learning Latent Spaces for Constrained Stellarator Design</a></td><td>13</td><td>0</td><td>LG</td><td>스텔러레이터 설계용 constrained CVAE이고 로봇과 무관한 과학 설계 응용임.</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2611.31515'>Synthetic Augmentation for Data-Scarce Object Detection: Allocation, Dose, and Filtering Across Six Datasets</a></td><td>12</td><td>3</td><td>CV</td><td>위성 포획과 산업 검사 같은 로봇 인식에서 합성 증강 효과를 6개 dataset으로 봄. 결과가 dataset마다 갈리고 방법 기여가 약함</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2611.31604'>Adapt, Label, Distill: Foundation-Model Supervision for Efficient Object Detection</a></td><td>12</td><td>2</td><td>CV</td><td>SAM3를 적응시켜 pseudo-label을 만들고 YOLO로 distillation함. 엔지니어링 파이프라인 성격이 강하고 domain별 효과도 불균일함</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2611.32011'>Distractors are the Real Enemy: Visual Distraction Adversarial Perturbations on SAM2-Based Video Tracking and Segmentation</a></td><td>12</td><td>2</td><td>CV</td><td>SAM2 tracker에 distractor를 이용한 adversarial 공격을 제안함. 로봇 추적 안전성 관점은 있으나 공격 기법 중심임</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2611.32715'>Semidefinite Programming for Cold-Start GNSS Doppler-Based Alignment: A Comparison with Nonlinear Least Squares</a></td><td>12</td><td>2</td><td>State Estimation</td><td>GNSS Doppler 정렬에서 NLS 해를 dual SDP로 인증하는 항법 최적화 연구임. 로봇 학습과 무관하고 항법 필터 범위에 머뭄</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2611.31909'>Your VLM Knows What to Inspect: Semantic Probe-Guided Adaptive Focusing for GUI Grounding</a></td><td>12</td><td>1</td><td>Multimodal</td><td>GUI grounding에서 VLM 설명을 이용해 crop 위치를 정하는 training-free test-time 방법임. 로봇과는 거리 있음</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2611.33042'>Spectrify: Framework for Hyperspectral Image Generation Using Computer Graphics</a></td><td>12</td><td>1</td><td>CV</td><td>3D scene dataset을 물리 기반 spectral rendering으로 hyperspectral 영상으로 변환하는 합성 데이터 framework임. 저수준 이미징 특화임</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2611.31526'>Diagnosing Epistemic Uncertainty in Neural Operators: Effects of Initialization, Discretization, and Function Sampling</a></td><td>12</td><td>1</td><td>LG</td><td>neural operator 약 46,000개 모델로 epistemic uncertainty 원천을 분해한 실증 연구이나 PDE 한정이라 로봇 연결 약함.</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2611.31661'>Boundary Representation-Driven Graph Transformer Modeling for Machining Operation Sequencing</a></td><td>12</td><td>1</td><td>LG</td><td>B-Rep graph transformer로 합성 부품 2,991개에서 가공 공정 순서를 예측함. 제조 계획 응용이고 합성 데이터라 로봇 연결 약함.</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2611.31875'>EEG-Jev: A Unified Single-Pass Decision Model for EEG</a></td><td>12</td><td>1</td><td>LG</td><td>EEG 35개 데이터셋을 한 checkpoint로 처리하는 typed decision model이고 로봇과 거리 있음.</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2611.31496'>Reading Between the Layers: Where Representation Quality Lives, and What Geometry Reveals</a></td><td>12</td><td>1</td><td>LG</td><td>25개 모델에서 층별 표현 품질을 분석하고 label-free layer 선택 지표 SGI를 제안함. 표현 학습 일반론이나 텍스트 모델 한정이고 로봇 연결은 약함</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2611.32657'>GeoSurge: Geometry-Grounded Multimodal Reasoning for Auditable Liver Resection Planning</a></td><td>12</td><td>1</td><td>CV</td><td>간 절제 수술 계획 표면을 기하 grammar로 생성하고 검증함. 제약 만족률은 올랐으나 의료 도메인이고 로봇 수술과는 직접 연결이 없음</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2611.33035'>Hybrid AI for AI-Native RAN Control: A Functional Perspective</a></td><td>12</td><td>1</td><td>LG</td><td>AI 기반 RAN 제어 의사결정의 기능 taxonomy survey임. world model 등을 언급하나 통신 도메인이고 로봇과 무관함</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2611.32172'>MediaStormBench-CameraLog: Can Multimodal Models Identify a Camera&#x27;s Log Curve?</a></td><td>12</td><td>0</td><td>Multimodal</td><td>영상 제작용 카메라 Log curve 식별 benchmark로 로봇과 무관함. 분석 설계는 깔끔하나 범위가 좁음.</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2611.32344'>DiCT: Teaching X-ray Vision-Language Models to Reason via Imagining CT</a></td><td>12</td><td>0</td><td>Multimodal</td><td>X-ray VLM이 CT를 상상하게 하는 증류 프레임워크로 의료 영상 도메인임. 로봇 무관함.</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2611.32501'>Déjà-VAE: Training-Free Consistent Editing with Pseudo-Invertible Encoders and Latent Back-Projection</a></td><td>12</td><td>0</td><td>Generative</td><td>VAE를 pseudo-invertible 구조로 바꿔 반복 편집 drift를 줄이는 training-free 방법으로 로봇 무관함.</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2611.32632'>HazeFlux: Few-Step Generative Priors for Real-World Image Dehazing</a></td><td>12</td><td>0</td><td>CV</td><td>flow-matching 모델에 LoRA와 decoder skip connection을 붙인 dehazing임. 영상 복원 incremental임</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2611.32736'>Qwen-Image-HD: Autoregressive Diffusion for High Definition Image Generation</a></td><td>12</td><td>0</td><td>Generative</td><td>Qwen-Image를 tile 단위 autoregressive로 4K 생성에 적응시킴. 이미지 생성 공학이고 robotics 무관함</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2611.32877'>Simultaneously Boosting Efficiency and Capability for Linear Attention via Adaptive Channel Compression and Activation Purification</a></td><td>12</td><td>0</td><td>CV</td><td>linear attention에 channel compression과 gating을 넣어 ViT 효율을 올림. ImageNet 수준의 architecture 공학임</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2611.31905'>OrangeTree: A Linear and Tree-based Time Series Forecasting Model Supporting Multiple Input and Output Lengths</a></td><td>12</td><td>0</td><td>LG</td><td>segment tree 기반 시계열 예측 모델 OrangeTree로 입출력 길이 변화에 대응하는 incremental 구조임.</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2611.31970'>Predict Backbone, Graft Dynamics: A Decoupled Paradigm for Time Series Forecasting</a></td><td>12</td><td>0</td><td>LG</td><td>시계열 예측에서 backbone 예측 후 지역 동역학을 복원하는 GRAFT이고 평균 MSE 개선이 4.6%인 incremental 방법임.</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2611.32274'>CoMNO: Commutator Memory Neural Operators for Long-Horizon PDE Prediction</a></td><td>12</td><td>0</td><td>LG</td><td>commutator memory로 장기 PDE 예측을 개선하는 neural operator이고 저자가 이전 보고 수치 오류를 정정한 판임.</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2611.32347'>Beyond Hard Tokens: Predictive Memory for Multimodal Protein Generation</a></td><td>12</td><td>0</td><td>LG</td><td>단백질 co-generation용 training-free predictive memory PredMem이고 로봇과 무관함.</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2611.32600'>Gated Concept Adapters: Layer-Wise Concept Bottlenecks for Auditable Text Understanding</a></td><td>12</td><td>0</td><td>NLP</td><td>Transformer 층별 concept bottleneck adapter로 텍스트 분류를 감사 가능하게 하는 해석성 연구임</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2611.31254'>The Date You Didn&#x27;t Set: The System-Prompt Date as a Hidden Variable in LLM Evaluation</a></td><td>12</td><td>0</td><td>NLP</td><td>system prompt 날짜가 LLM 평가 결과를 중앙값 6.6% 뒤집는다는 재현성 지적임. 평가 위생 측면에서 유익하나 로봇과 무관함</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2611.31260'>Capability and Interpretability of Transformers on Multi-task Recurrence</a></td><td>12</td><td>0</td><td>LG</td><td>순환군 선형 recurrence 과제로 Transformer의 규칙 식별 능력을 분석한 해석성 연구임. 장난감 설정이고 로봇과 무관함</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2611.31268'>AhaPro: A Process-level Rebus benchmark for probing Aha moments in LLM reasoning</a></td><td>12</td><td>0</td><td>NLP</td><td>rebus 퍼즐로 LLM의 Aha moment 추론 과정을 보는 benchmark임. 로봇과 무관함</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2611.31668'>Provenance Loss and Repair in Multilingual Compaction</a></td><td>12</td><td>0</td><td>NLP</td><td>대화 요약 후 원문을 지울 때 스페인어 성 표지가 사라지는 문제를 학습 없이 고치는 연구임. agent memory와 약하게 닿으나 언어 한정 현상이라 로봇 관련성 낮음</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2611.31975'>Localizing Cross-Lingual Generalization in Parameter Space</a></td><td>12</td><td>0</td><td>NLP</td><td>LoRA adapter 간 linear mode connectivity로 cross-lingual 전이의 성패를 설명함. 분석은 흥미로우나 다국어 NLP 한정임</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2611.33078'>FOL-Proof: Verifying LLM Text-to-Logic Translations via Deterministic Semantics</a></td><td>12</td><td>0</td><td>NLP</td><td>LLM이 만든 FOL 번역을 ERG 해석과 SMT로 검증하는 FOL-Proof임. 형식 검증은 TAMP와 먼 연결이 있으나 텍스트 번역 한정임</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2611.33093'>AIChipBench: Benchmarking LLM Agents for Automated AI Accelerator Design</a></td><td>12</td><td>0</td><td>LG</td><td>LLM coding agent의 RTL 가속기 설계를 평가하는 AIChipBench임. 첫 state mismatch 피드백이 효과적이라는 관찰은 있으나 하드웨어 설계 도메인임</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2611.31756'>TACT-Bench: Testing Adaptive Conversational Threats against Tool-Use Agents</a></td><td>12</td><td>0</td><td>NLP</td><td>tool-use agent에 대한 적응형 대화 공격 benchmark임. 안전성 평가이나 로봇과 무관함</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2611.32365'>The Control-Flow Tax: Specialized Decision Routing for LLM Agent Workflows</a></td><td>12</td><td>0</td><td>NLP</td><td>LLM agent 워크플로의 제어 흐름 비용을 전용 라우터로 줄임. 로봇과 무관함</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2611.32480'>VISE: Verifier-Independent Skill Self-Evolution with Feedback from Tool Implementations</a></td><td>12</td><td>0</td><td>NLP</td><td>도구 구현 코드로 agent skill을 수정하는 VISE임. 로봇과 무관함</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2611.33098'>Delegent: A Multi-Agent Harness That Reduces Cost without Sacrificing Performance</a></td><td>12</td><td>0</td><td>NLP</td><td>frontier 모델이 쉬운 하위 작업을 소형 모델에 위임해 비용을 줄이는 harness임. 로봇과 무관함</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2611.32896'>DualSpec: Spectral Reconstruction with Optimized Stereo Cameras</a></td><td>11</td><td>1</td><td>CV</td><td>두 개의 광학 filter와 복원망을 함께 최적화하는 stereo 스펙트럼 복원임. 이미징 특화임</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2611.32777'>Beyond Static Semantics: Instance-Adaptive Vision-Language Alignment for Building Damage Assessment</a></td><td>11</td><td>0</td><td>Multimodal</td><td>건물 피해 평가를 위한 instance-adaptive text-visual alignment임. 원격탐사 특화 module 조합임</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2611.32941'>ProX-MAD: Aggregating Spatial Context into Representative Proxies for Few-shot Medical Anomaly Detection</a></td><td>11</td><td>0</td><td>CV</td><td>의료 이상 탐지를 proxy token으로 통합하는 방법임. 6개 의료 dataset 평가이고 robotics 무관함</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2611.31470'>CRAB-H: Task-Centric Certification for Healthcare Autonomous Systems</a></td><td>10</td><td>2</td><td>Robotics</td><td>의료 자율 시스템용 task 중심 인증 방법론으로 개념 제안뿐이고 실험 근거가 없음</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2611.32116'>The Old Scene Lives in the Cache: Diagnosing and Shedding Stale History in Streaming Video Generation</a></td><td>10</td><td>1</td><td>Video</td><td>streaming 영상 생성에서 cache에 남은 이전 장면을 진단하고 Molt Forcing으로 재구성함. cache 진단은 명확하나 영상 생성 범위임</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2611.32500'>CalibTrack: Exploring Learned Heteroscedastic Covariance for Robust Multi-Camera Pedestrian Tracking</a></td><td>10</td><td>1</td><td>CV</td><td>다중 카메라 보행자 tracking에서 learned heteroscedastic covariance 효과를 분석함. 추적 필터 보정 연구이나 개선이 제한적이라 저자도 밝힘.</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2611.31252'>DAGGER: Deployment-Free Quality Estimation for Generative AI Workflows</a></td><td>10</td><td>1</td><td>LG</td><td>생성 AI workflow 품질을 graph 분해와 SVD matrix completion으로 추정하는 LLM 파이프라인 연구임. 프로파일링 비용 10.2배 절감이나 로봇과 무관함</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2611.31358'>Nemotron-Labs-VisualCreation: Pixel as Code for Agentic Visual Creation</a></td><td>10</td><td>0</td><td>Multimodal</td><td>래스터 토큰과 코드를 합친 시각 콘텐츠 생성 agent 시스템임. tokenizer PSNR 개선은 있으나 로봇과 무관한 생성 제품 보고서에 가까움</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2611.31647'>MSW: a Multi-Scale Sliced Wasserstein Distance Between Image Distributions</a></td><td>10</td><td>0</td><td>CV</td><td>사전학습 network 없는 multi-scale sliced Wasserstein 이미지 분포 거리임. 로봇과 무관한 평가 지표 제안임</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2611.31714'>NOBODY Was There: Bridging the Human-VLM Gap in Unwarranted Person Attribution Bias</a></td><td>10</td><td>0</td><td>Multimodal</td><td>VLM이 사람이 없는 장면에 사람을 귀속시키는 편향을 DPO로 정렬함. 로봇과 무관함</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2611.32176'>DocPristine: Content-Aware Document Appearance Enhancement under Real-World Mixed Degradations</a></td><td>10</td><td>0</td><td>CV</td><td>문서 사진 화질 개선 모듈 조합으로 로봇 관련성 없음. incremental engineering임.</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2611.32899'>Label leakage through file headers: geometry and batch confounds in public mammography datasets, and a pre-training acceptance gate</a></td><td>10</td><td>0</td><td>LG</td><td>mammography 공개 dataset에서 파일 header와 geometry로 label이 유출됨을 진단함. 평가 위생 점검이고 robotics 무관함</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2611.31319'>Conformalized Tree-Based Gradient Ensembles for Out-of-Distribution Detection and Plausible Recourse</a></td><td>10</td><td>0</td><td>LG</td><td>표 형식 데이터의 counterfactual recourse에 conformal OOD gate를 건 분석임. robotics 무관함</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2611.31619'>What a Forecasting Leaderboard Can Establish: Resolution Reporting for Zero-Shot Time-Series Models</a></td><td>10</td><td>0</td><td>LG</td><td>시계열 foundation model 리더보드의 해상도를 계산하는 Vernier 도구이고 평가 방법론 중심이며 로봇과 무관함.</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2611.32170'>Multi-view Random-set Learning</a></td><td>10</td><td>0</td><td>CV</td><td>multi-view random-set learning으로 view 열화를 다루는 분류 방법이고 로봇과 무관함.</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2611.32372'>From the ELBO to Maximum Likelihood: Convergence of Variational Autoencoders for Nonlinear Mixed-Effects Modeling</a></td><td>10</td><td>0</td><td>LG</td><td>VAE-NLME 알고리즘의 수렴 증명으로 약리 모델링 용도이고 로봇과 무관함.</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2611.32573'>Boiling Down Uncertainty: Deep Generative Scenario Search with Decision-Guided Evolution Strategies for Two-Stage Stochastic Optimization</a></td><td>10</td><td>0</td><td>LG</td><td>2단계 stochastic programming의 scenario 생성 gradient를 이중성으로 유도한 최적화 논문으로 로봇과 무관함</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2611.32708'>Contrastive Proxy Forests: Completeness-Preserving Proxy Learning from Multimodal Records</a></td><td>10</td><td>0</td><td>LG</td><td>다중모달 기록에서 proximal causal inference의 proxy를 contrastive로 학습하는 의료 통계 논문임</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2611.32830'>PtychoFM: A Foundation Model for Ptychographic Imaging</a></td><td>10</td><td>0</td><td>LG</td><td>ptychography 영상 복원 foundation model로 로봇과 무관함</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2611.33024'>Best Arm Identification with Unknown Post-Action Context Distribution</a></td><td>10</td><td>0</td><td>LG</td><td>post-action context가 있는 best arm identification의 표본 복잡도 이론임</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2611.31264'>How Persona Conditioning Changes Open-Ended Task Execution: A Paired Evaluation of Behavioral Gains and Reliability Costs</a></td><td>10</td><td>0</td><td>NLP</td><td>persona 조건화가 지시 이행 정확도를 17~30포인트 낮춘다는 LLM 평가 연구임. 로봇과 무관함</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2611.31999'>Grounding Language Models in Revealed Audience Behavior</a></td><td>10</td><td>0</td><td>NLP</td><td>실제 클릭 기록으로 fine-tuning한 LM이 질문형 prompting보다 audience 행동을 잘 맞춘다는 연구임. 로봇 연관 없음</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2611.32471'>BCP: A Lightweight Boundary-Controlled Framework for Online Sign Language Recognition and Translation</a></td><td>10</td><td>0</td><td>CV</td><td>사인 언어 인식 모델을 frozen 상태로 online화하는 boundary adapter BCP임. streaming 결정 시점 학습이 있으나 수어 번역 한정임</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2611.32807'>From Grammar Deltas to Token Masks: Incremental Constrained Decoding under Runtime Grammar Evolution</a></td><td>10</td><td>0</td><td>NLP</td><td>grammar-constrained decoding에서 runtime grammar 갱신을 증분 처리하는 GramDelta임. 디코딩 효율 개선이나 코드 생성 한정임</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2611.31424'>ContextLure: Exploiting Benign Conversation History for Indirect Prompt Injection</a></td><td>10</td><td>0</td><td>NLP</td><td>무해한 대화 기록의 증거를 이용해 indirect prompt injection을 만드는 ContextLure임. 공격 프레임워크라 로봇 무관함</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2611.31610'>Monitorable-by-design architectures for a post-Astra world: a compartmentalization-based approach</a></td><td>10</td><td>0</td><td>LG</td><td>위험 능력을 compartmentalize해 monitoring하는 LLM 구조를 제안한 개념 글임. 실험이 없고 로봇 무관함</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2611.31682'>LimoBench: How Street Smart Are Large Language Models?</a></td><td>10</td><td>0</td><td>NLP</td><td>LLM의 지도 위치 질의 benchmark 82문항과 PostGIS MCP 도구 부착임. 로봇 navigation과 무관한 GIS 질의 평가임</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2611.31833'>Not All Interpretation Methods Are Created Equal: Tiered Evaluation of AI Interpretability</a></td><td>10</td><td>0</td><td>LG</td><td>해석 방법을 5단계로 평가하는 TRUST 프레임워크 제안임. 실험 증거가 약한 position 성격이고 로봇과 무관함</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2611.31864'>No Fixed Configuration Is Best: Context- and Cost-Aware Tuning of LLM Pipelines, with an Application to Schema Matching and Mapping</a></td><td>10</td><td>0</td><td>LG</td><td>LLM 파이프라인의 schema matching 튜닝 분석임. 로봇과 무관함</td></tr>
<tr><td>486</td><td><a href='https://arxiv.org/abs/2611.32508'>RecurSciBench: Benchmarking Recursive Self-Improvement in Data-Driven Scientific Research</a></td><td>10</td><td>0</td><td>NLP</td><td>과학 연구 agent의 재귀 자기개선 평가 benchmark임. 로봇과 무관함</td></tr>
<tr><td>487</td><td><a href='https://arxiv.org/abs/2611.32835'>Aqua2CAD : Observation-Guided Point Cloud Correction and Completion for CAD Reconstruction from Underwater Stereo Images</a></td><td>9</td><td>1</td><td>3D Vision</td><td>수중 stereo에서 point cloud를 보정, 완성해 CAD를 복원함. 합성 benchmark 위주이고 응용 범위가 좁음</td></tr>
<tr><td>488</td><td><a href='https://arxiv.org/abs/2611.32310'>CREDIT: Compositional Reliability Learning for Noisy Composed Image Retrieval</a></td><td>9</td><td>0</td><td>CV</td><td>noisy composed image retrieval에 evidential 학습과 diffusion refinement를 붙인 incremental 연구임. 로봇 무관함.</td></tr>
<tr><td>489</td><td><a href='https://arxiv.org/abs/2611.32625'>On the Capabilities and Limitations of Zero-Shot Open-Vocabulary Cloud Segmentation</a></td><td>9</td><td>0</td><td>CV</td><td>12개 OVSS 모델을 6개 cloud dataset에서 zero-shot 비교한 평가 연구임. 새 방법 없고 robotics 무관함</td></tr>
<tr><td>490</td><td><a href='https://arxiv.org/abs/2611.33032'>SHARPnP: Self-Supervised and Plug-and-Play Hyperspectral Super-Resolution from Real Noisy Unaligned Camera Measurements</a></td><td>9</td><td>0</td><td>CV</td><td>noisy, unaligned 측정에서 RGB 유도 hyperspectral 초해상을 self-supervised로 수행함. 이미징 특화임</td></tr>
<tr><td>491</td><td><a href='https://arxiv.org/abs/2611.31292'>Hidden Clues in WM-811K: Uncovering the Spatial Signals Behind Wafer Map Prediction</a></td><td>9</td><td>0</td><td>CV</td><td>WM-811K wafer map 성능이 layout과 위치 신호에서 오는지 shuffle로 분해함. 반도체 dataset 분석이고 robotics 무관함</td></tr>
<tr><td>492</td><td><a href='https://arxiv.org/abs/2611.31333'>Fusion Gains Depend on the Implementation and the Calibration Target: An 18-Task Study of Prediction Intervals with a Single-Source Fallback</a></td><td>9</td><td>0</td><td>LG</td><td>18개 회귀 과제에서 prediction interval fusion 이득이 구현과 calibration에 의존함을 비교함. 표 형식 데이터 분석임</td></tr>
<tr><td>493</td><td><a href='https://arxiv.org/abs/2611.31525'>SOTS: Signature-based Optimal Transport Selection</a></td><td>9</td><td>0</td><td>LG</td><td>불규칙 시계열 coreset 선택을 path signature와 Wasserstein으로 하는 산업 응용 연구이고 로봇 관련성 없음.</td></tr>
<tr><td>494</td><td><a href='https://arxiv.org/abs/2611.31880'>Multi Agent Reinforcement Learning enhanced Federated Learning for Predicting Remaining Useful Lifetime</a></td><td>9</td><td>0</td><td>RL</td><td>패킷 손실 환경의 federated learning에 MARL로 전송 layer를 고르는 RUL 예측 연구이고 로봇과 무관함.</td></tr>
<tr><td>495</td><td><a href='https://arxiv.org/abs/2611.31914'>Meta-Amortized Cognitive Modeling</a></td><td>9</td><td>0</td><td>LG</td><td>인지 모델링용 meta-amortized 베이즈 추론 CogFormerV2이고 로봇과 무관함.</td></tr>
<tr><td>496</td><td><a href='https://arxiv.org/abs/2611.32033'>Scale-Robust and Global-Aware Representation Learning for Multivariate Time Series Anomaly Detection</a></td><td>9</td><td>0</td><td>LG</td><td>다변량 시계열 이상 탐지용 STAGER이고 benchmark 순위 개선 수준임.</td></tr>
<tr><td>497</td><td><a href='https://arxiv.org/abs/2611.32118'>Monte Carlo Tree Search for Classifier Chains</a></td><td>9</td><td>0</td><td>LG</td><td>multi-label classifier chain에 MCTS를 적용하는 TSCC이고 로봇과 무관함.</td></tr>
<tr><td>498</td><td><a href='https://arxiv.org/abs/2611.32174'>A Unified Control Framework for Gradient Inversion Defense in Federated Learning</a></td><td>9</td><td>0</td><td>LG</td><td>federated learning gradient inversion 방어 NODE이고 로봇과 무관함.</td></tr>
<tr><td>499</td><td><a href='https://arxiv.org/abs/2611.32373'>Metamorphic Testing of Learned Spatial Surrogates for Transit Accessibility</a></td><td>9</td><td>0</td><td>LG</td><td>교통 접근성 surrogate의 metamorphic testing이고 로봇과 무관함.</td></tr>
<tr><td>500</td><td><a href='https://arxiv.org/abs/2611.31345'>Beyond Static Charts: Benchmarking Interactive Chart-to-Code Generation for MLLMs</a></td><td>9</td><td>0</td><td>Multimodal</td><td>interactive chart-to-code 벤치마크 ChartInt임. 벤치마크 신규성 위주이고 로봇 무관함</td></tr>
<tr><td>501</td><td><a href='https://arxiv.org/abs/2611.31346'>What People Choose Not to Say: A Multimodal Benchmark for Fine-Grained Information Manipulation in Conversations</a></td><td>9</td><td>0</td><td>Multimodal</td><td>대화 속 정보 은폐, 누설 등 6가지 전략을 라벨링한 멀티모달 벤치마크 InfoCon임. 사회 이해 평가이고 로봇 무관함</td></tr>
<tr><td>502</td><td><a href='https://arxiv.org/abs/2611.32308'>Putting a Robot on a Phone Call: Layered Signaling, Bounded Occupancy and Turn Arbitration over WebRTC</a></td><td>8</td><td>3</td><td>Embodied AI</td><td>로봇에 WebRTC 음성통화를 붙이는 시스템 엔지니어링 측정 보고임. 학습·정책 기여가 없고 한 플랫폼의 지연 측정에 그침</td></tr>
<tr><td>503</td><td><a href='https://arxiv.org/abs/2611.31437'>Which Ellipses Are Outlines of a Given Ellipsoid? A Ratio Test with Unknown Focal Length</a></td><td>8</td><td>1</td><td>3D Vision</td><td>타원이 타원체의 윤곽일 조건을 focal length 기준으로 유도한 기하 이론임. 수학적으로는 정돈되나 로봇 학습과 거리 멂</td></tr>
<tr><td>504</td><td><a href='https://arxiv.org/abs/2611.31877'>Don&#x27;t Miss the Forest for the Trees: Zero-Shot Skeleton Action Recognition with Hyperbolic Hierarchical Semantic Prototypes</a></td><td>8</td><td>1</td><td>CV</td><td>zero-shot skeleton 행동 인식을 hyperbolic 계층 prototype으로 확장함. 행동 taxonomy 평가가 대상이고 로봇과는 거리 있음</td></tr>
<tr><td>505</td><td><a href='https://arxiv.org/abs/2611.33088'>The Radar-based Activities of Daily Living (R-ADL) Dataset</a></td><td>8</td><td>1</td><td>LG</td><td>radar 기반 일상 활동 인식 dataset임. 규모와 장소 확장이 기여이고 새 방법 없음</td></tr>
<tr><td>506</td><td><a href='https://arxiv.org/abs/2611.31466'>AdProducer: Towards Agentic Advertising Video Generation</a></td><td>8</td><td>0</td><td>Video</td><td>광고 영상 생성 agent와 benchmark를 제안함. 로봇과 무관한 응용임</td></tr>
<tr><td>507</td><td><a href='https://arxiv.org/abs/2611.31776'>ReCAP: Sequential Concept Acquisition with Guarantees under Imperfect Concept Predictors</a></td><td>8</td><td>0</td><td>CV</td><td>의료 영상 concept 획득에 submodular 보장을 줌. 로봇과 무관함</td></tr>
<tr><td>508</td><td><a href='https://arxiv.org/abs/2611.31780'>VISOR: A Vision-Language Selector for Multimodal Time-Series Forecasting</a></td><td>8</td><td>0</td><td>LG</td><td>시계열 예측에서 VLM이 후보 미래 하나를 고르는 구조임. 로봇과 무관함</td></tr>
<tr><td>509</td><td><a href='https://arxiv.org/abs/2611.31895'>Loupe: Reinforcing Knowledge-Intensive Video Generation Agents</a></td><td>8</td><td>0</td><td>Video</td><td>지식 집약 영상 생성 agent를 rubric 기반 credit으로 RL 학습함. 로봇과 무관함</td></tr>
<tr><td>510</td><td><a href='https://arxiv.org/abs/2611.32022'>Beyond Before-and-After Images: Evaluating Temporal Grounding in a Lightweight VLM for Disaster Assessment</a></td><td>8</td><td>0</td><td>CV</td><td>재난 위성 영상에서 VLM의 temporal grounding을 진단해 pre-event 이미지 이득이 없음을 보임. 로봇과 무관한 분석임</td></tr>
<tr><td>511</td><td><a href='https://arxiv.org/abs/2611.32067'>LoopDVR: Looped Transformer for Efficient Dense Visual Recognition</a></td><td>8</td><td>0</td><td>CV</td><td>dense recognition 모델을 looped 구조로 바꿔 파라미터를 28% 줄임. 로봇과 무관한 효율 기법임</td></tr>
<tr><td>512</td><td><a href='https://arxiv.org/abs/2611.32097'>GUI-PRISM: Efficient Action Decoding for GUI Agents</a></td><td>8</td><td>0</td><td>Multimodal</td><td>GUI agent의 action을 직접 예측하는 hybrid decoder로 3.8배 빠름. GUI 범위이고 로봇과 무관함</td></tr>
<tr><td>513</td><td><a href='https://arxiv.org/abs/2611.32102'>RISE: Reasoning with Implicit State Embeddings for GUI Agents</a></td><td>8</td><td>0</td><td>Multimodal</td><td>GUI agent의 implicit state embedding 추론으로 OSWorld-G 정확도를 4.3점 올림. 로봇과 무관함</td></tr>
<tr><td>514</td><td><a href='https://arxiv.org/abs/2611.32220'>FaceNet versus VGG Features in Wasserstein Distortion for Face Image Compression</a></td><td>8</td><td>0</td><td>CV</td><td>얼굴 이미지 압축에서 WD 특징망을 FaceNet으로 바꿔 20장으로 예비 사용자 연구한 소규모 결과임. 로봇 무관함.</td></tr>
<tr><td>515</td><td><a href='https://arxiv.org/abs/2611.32299'>Towards a Multimodal Aesthetic Agent for Photographic Reference Grading</a></td><td>8</td><td>0</td><td>Multimodal</td><td>사진 color grading용 agent로 로봇 무관함. 학습 파이프라인 조합 수준임.</td></tr>
<tr><td>516</td><td><a href='https://arxiv.org/abs/2611.32325'>A recursive self-improvement framework for electron microscopy analysis</a></td><td>8</td><td>0</td><td>CV</td><td>전자현미경 분석용 자기개선 agent 프레임워크로 로봇 무관함.</td></tr>
<tr><td>517</td><td><a href='https://arxiv.org/abs/2611.32327'>FlowVecFont: Scalable Vector Font Generation via Latent Flow Matching</a></td><td>8</td><td>0</td><td>Generative</td><td>vector font 생성을 latent flow matching으로 스케일한 연구로 로봇 무관함.</td></tr>
<tr><td>518</td><td><a href='https://arxiv.org/abs/2611.32424'>One Subspace Is Not Enough: LocalSubspaceAD for Training-Free Few-Shot Anomaly Detection</a></td><td>8</td><td>0</td><td>CV</td><td>산업 이상 탐지에서 subspace를 k-means 혼합으로 확장한 작은 개선(AUROC 1.2~1.8점)임. 로봇 무관함.</td></tr>
<tr><td>519</td><td><a href='https://arxiv.org/abs/2611.32450'>Which Parameters to Update? An Instance-Specific Adaptation Framework for Real-World Pansharpening</a></td><td>8</td><td>0</td><td>CV</td><td>pansharpening에 instance별 test-time adaptation으로 일부 파라미터만 갱신함. test-time 기법이나 위성 영상 도메인이라 로봇 무관함.</td></tr>
<tr><td>520</td><td><a href='https://arxiv.org/abs/2611.32742'>A Morphological Approach to Inverse Lithography</a></td><td>8</td><td>0</td><td>LG</td><td>반도체 inverse lithography의 mask 제조 제약을 수학적으로 정식화하고 regularizer로 씀. robotics 무관함</td></tr>
<tr><td>521</td><td><a href='https://arxiv.org/abs/2611.31436'>Is 4 Bits Enough for EEG Sleep Staging? A Subject-Level Benchmark of MXFP4, NVFP4 and FP8</a></td><td>8</td><td>0</td><td>LG</td><td>웨어러블 EEG 수면 단계 분류에 MXFP4/NVFP4 양자화를 비교한 벤치마크이고 로봇과 무관함.</td></tr>
<tr><td>522</td><td><a href='https://arxiv.org/abs/2611.31640'>Reward Basis Decomposition for Interpreting Preference Heterogeneity</a></td><td>8</td><td>0</td><td>NLP</td><td>reward model 선호 이질성을 population/user 항으로 분해했으나 사용자별 구조가 없다는 결과이고 로봇과 무관함.</td></tr>
<tr><td>523</td><td><a href='https://arxiv.org/abs/2611.31731'>Geo-SMILE: Statistical Model-Agnostic Interpretability with Local Explanations for Geospatial Machine Learning</a></td><td>8</td><td>0</td><td>LG</td><td>지리 공간 ML용 모델 불가지 설명 기법 Geo-SMILE이고 로봇과 무관함.</td></tr>
<tr><td>524</td><td><a href='https://arxiv.org/abs/2611.32019'>PFedHASNet: A Personalized Federated Hybrid Analog-Spike Network for Multi-Subject Motor Imagery EEG Decoding</a></td><td>8</td><td>0</td><td>LG</td><td>federated 방식의 motor imagery EEG 디코딩 모델이고 로봇과 무관함.</td></tr>
<tr><td>525</td><td><a href='https://arxiv.org/abs/2611.32200'>Who gets the information? An $α$-fair label-coverage framework for multi-label feature selection</a></td><td>8</td><td>0</td><td>LG</td><td>multi-label feature selection에 alpha-fair welfare를 쓰는 FLIC이고 로봇과 무관함.</td></tr>
<tr><td>526</td><td><a href='https://arxiv.org/abs/2611.32393'>Fractal Neural Synthesis: Constant-Storage Procedural Weight Derivation via Complex Quadratic Boundary Dynamics</a></td><td>8</td><td>0</td><td>LG</td><td>복소 이차 함수 경계에서 가중치를 절차적으로 생성해 microcontroller flash를 줄이나 표 형태 소규모 benchmark만 평가함</td></tr>
<tr><td>527</td><td><a href='https://arxiv.org/abs/2611.32402'>Optimal Transport Meets t-SNE: Integrated Visualization without Batch Effects in OT-tSNE</a></td><td>8</td><td>0</td><td>LG</td><td>단일세포 데이터 batch effect 제거용 OT 기반 t-SNE로 로봇과 무관함</td></tr>
<tr><td>528</td><td><a href='https://arxiv.org/abs/2611.32403'>A Framework for Graph Node Symmetric Quantification under Dataset Shift</a></td><td>8</td><td>0</td><td>LG</td><td>graph node quantification을 node 분류기 없이 풀어 내는 프레임워크로 로봇과 무관함</td></tr>
<tr><td>529</td><td><a href='https://arxiv.org/abs/2611.32543'>Beyond Robust Algorithmic Recourse: Sharing the Burden of Validity through Model Multiplicity</a></td><td>8</td><td>0</td><td>LG</td><td>algorithmic recourse의 robustness 부담을 model multiplicity로 분담하는 공정성 논문으로 로봇과 무관함</td></tr>
<tr><td>530</td><td><a href='https://arxiv.org/abs/2611.32598'>On the Effectiveness of Resampling for Supervised Graph Anomaly Detection</a></td><td>8</td><td>0</td><td>LG</td><td>graph anomaly detection의 oversampling 효과 재검증 benchmark 논문으로 로봇과 무관함</td></tr>
<tr><td>531</td><td><a href='https://arxiv.org/abs/2611.32602'>ST-GNN-AAAS: Spatio-Temporal Graph Neural Networks for Anytime Automatic Algorithm Selection in the Traveling Salesman Problem</a></td><td>8</td><td>0</td><td>LG</td><td>TSP 풀이 알고리즘 선택을 ST-GNN으로 예측하는 소규모 응용으로 로봇과 무관함</td></tr>
<tr><td>532</td><td><a href='https://arxiv.org/abs/2611.32651'>LATEC: Learned Axial TEnsor Compression for High-Dimensional Scientific Data</a></td><td>8</td><td>0</td><td>LG</td><td>과학 데이터용 error-bounded learned 압축 codec으로 로봇과 무관함</td></tr>
<tr><td>533</td><td><a href='https://arxiv.org/abs/2611.32714'>FourStat: A Dual AutoEncoder Leveraging Frequency and Stationarity for Time Series Anomaly Detection</a></td><td>8</td><td>0</td><td>LG</td><td>단변량 시계열 이상 탐지용 Fourier 및 stationary autoencoder 조합으로 로봇과 무관함</td></tr>
<tr><td>534</td><td><a href='https://arxiv.org/abs/2611.32859'>Tabra Blends: Improving the Accuracy--Latency Trade-off with Complementary Tabular Models</a></td><td>8</td><td>0</td><td>LG</td><td>tabular 모델 두 개를 blend해 정확도와 지연의 trade-off를 개선한 4쪽 보고임</td></tr>
<tr><td>535</td><td><a href='https://arxiv.org/abs/2611.32892'>Shared information governs multi-view planted matching</a></td><td>8</td><td>0</td><td>LG</td><td>다중 view planted matching의 정보이론적 임계값을 증명한 순수 이론임</td></tr>
<tr><td>536</td><td><a href='https://arxiv.org/abs/2611.32979'>File Size as a Potential Dataset Bias in Audio-Visual Deepfake Data</a></td><td>8</td><td>0</td><td>CV</td><td>audio-visual deepfake 데이터셋에서 파일 크기 편향을 지적한 데이터셋 감사임</td></tr>
<tr><td>537</td><td><a href='https://arxiv.org/abs/2611.33026'>Score-Based Diffusion for Hypergraph Signals in the t-Spectral Domain</a></td><td>8</td><td>0</td><td>LG</td><td>hypergraph 신호의 t-spectral 영역 score 기반 diffusion으로 로봇과 무관함</td></tr>
<tr><td>538</td><td><a href='https://arxiv.org/abs/2611.33056'>Local Indices Are Not Enough: Synchrony and Global Information in Bandit Algorithms</a></td><td>8</td><td>0</td><td>LG</td><td>비동기 local index bandit 알고리즘의 regret 한계를 증명한 순수 이론임</td></tr>
<tr><td>539</td><td><a href='https://arxiv.org/abs/2611.31253'>Instantiation of Human Values in Image Generation</a></td><td>8</td><td>0</td><td>CV</td><td>T2I 모델이 인간 가치를 시각화하는 방식의 편향을 28,000장으로 분석한 사회과학적 연구임. 로봇 관련성 없음</td></tr>
<tr><td>540</td><td><a href='https://arxiv.org/abs/2611.31266'>Agentic Systems Need Multi-Run Evaluation: A Study of Retrieval and Response Variability in a Deployed Enterprise RAG System</a></td><td>8</td><td>0</td><td>NLP</td><td>enterprise agentic RAG의 run-to-run 변동을 739개 질문 10회 반복으로 측정함. 로봇과 무관함</td></tr>
<tr><td>541</td><td><a href='https://arxiv.org/abs/2611.31495'>ModernELECTRA: Replaced-Token Detection with Boundary-Window Reconstruction for Compact Encoders that Classify and Embed</a></td><td>8</td><td>0</td><td>NLP</td><td>ELECTRA 방식 compact encoder에 boundary-window reconstruction을 더한 사전학습 레시피임. 텍스트 encoder 개선이라 로봇과 무관함</td></tr>
<tr><td>542</td><td><a href='https://arxiv.org/abs/2611.31613'>Training decision models for simulating human respondents</a></td><td>8</td><td>0</td><td>NLP</td><td>LLM을 설문 응답자 대용으로 쓸 때 생기는 treatment-effect 편향을 choice 데이터 학습으로 줄이는 연구임. 계량경제 응용이라 로봇 연관 없음</td></tr>
<tr><td>543</td><td><a href='https://arxiv.org/abs/2611.31686'>Right Destination, Wrong Journey: Synthetic Counseling Dialogues Miss Human Interactional Dynamics</a></td><td>8</td><td>0</td><td>NLP</td><td>합성 상담 대화가 사람 대화의 turn 단위 반응성을 못 따라간다는 평가 연구임. 정신건강 대화 도메인이라 로봇 연관 없음</td></tr>
<tr><td>544</td><td><a href='https://arxiv.org/abs/2611.31848'>Faithful Persona Steering under Incongruity via Dual-Stream Refinement</a></td><td>8</td><td>0</td><td>NLP</td><td>LLM persona의 비일관적 특성을 dual-stream latent로 유지하는 QuirkyMind 제안임. 개인화 도메인이라 로봇과 무관함</td></tr>
<tr><td>545</td><td><a href='https://arxiv.org/abs/2611.32211'>ArEssays: Towards Robust Arabic Handwritten Text Understanding in Educational Settings</a></td><td>8</td><td>0</td><td>CV</td><td>아랍어 학생 손글씨 에세이 데이터셋과 34개 모델 벤치마크임. 특정 언어 OCR 데이터셋 기여라 로봇 무관함</td></tr>
<tr><td>546</td><td><a href='https://arxiv.org/abs/2611.32446'>When Ink Meets Pixel: Intent-Aware OCR with VLMs for Human-Corrected Financial Documents When Ink Meets Pixel: Intent-Aware OCR with VLMs for Human-Corrected Financial Documents</a></td><td>8</td><td>0</td><td>CV</td><td>사람이 손으로 고친 금융 문서의 편집 의도를 읽는 intent-aware OCR 데이터셋과 3B/7B VLM임. 문서 도메인 dataset fine-tuning 위주임</td></tr>
<tr><td>547</td><td><a href='https://arxiv.org/abs/2611.32455'>Phoneme-identity depth profiles do not reliably predict LoRA placement for dysarthric ASR</a></td><td>8</td><td>0</td><td>NLP</td><td>phoneme probe로 dysarthric ASR의 LoRA 위치를 정할 수 없다는 부정적 결과임. 음성 도메인이고 로봇 무관함</td></tr>
<tr><td>548</td><td><a href='https://arxiv.org/abs/2611.32614'>When &quot;Neutral&quot; Means Irrelevant: A Construct-Validity Audit of NormAd-ETI</a></td><td>8</td><td>0</td><td>NLP</td><td>NormAd-ETI 점수가 규범 적용 여부와 부합 여부를 섞어 잰다는 construct validity 감사임. 로봇 무관함</td></tr>
<tr><td>549</td><td><a href='https://arxiv.org/abs/2611.32623'>REBEAL: Human References Are No Longer the Best Translation, and Metrics Do Not Notice</a></td><td>8</td><td>0</td><td>NLP</td><td>번역 평가 지표가 오염된 reference에 어떻게 반응하는지 보는 REBEAL 벤치마크임. 로봇 무관함</td></tr>
<tr><td>550</td><td><a href='https://arxiv.org/abs/2611.32631'>Generating Schema-Aligned Synthetic Dialogues and Measuring Their Diversity</a></td><td>8</td><td>0</td><td>NLP</td><td>schema-valid 기록을 먼저 뽑고 대화를 생성하는 합성 의료 대화 데이터 방식임. 로봇 무관함</td></tr>
<tr><td>551</td><td><a href='https://arxiv.org/abs/2611.32685'>Social Bias Neurons in Multilingual Language Models: A Mechanistic Interpretability Analysis</a></td><td>8</td><td>0</td><td>NLP</td><td>다국어 LM의 social bias neuron을 integrated gap gradients로 찾음. 로봇 무관함</td></tr>
<tr><td>552</td><td><a href='https://arxiv.org/abs/2611.32778'>Beyond Fixed-Context Likelihood: Zero-Shot AI-Generated Text Detection via Context Perturbation Discrepancy</a></td><td>8</td><td>0</td><td>NLP</td><td>문맥 길이 변화에 따른 log probability 증가량으로 AI 생성 텍스트를 zero-shot 탐지하는 CPD임. 로봇 무관함</td></tr>
<tr><td>553</td><td><a href='https://arxiv.org/abs/2611.33030'>SALSA: Sampling Adversarial Suffixes from Learned Distributions for LLM Safety Assessment</a></td><td>8</td><td>0</td><td>NLP</td><td>jailbreak suffix 분포를 학습해 sampling으로 공격하는 SALSA임. 안전성 red-team 도구이고 로봇 무관함</td></tr>
<tr><td>554</td><td><a href='https://arxiv.org/abs/2611.31284'>Irreducible Governance Structure for Autonomous Agent Systems: Fair Allocation, Strategy-Proofness, and Multi-Scale Composition</a></td><td>8</td><td>0</td><td>LG</td><td>agent governance의 불가능성 결과와 irreducibility 정리를 주장함. 이론 위주이고 실험 근거가 약하며 로봇 무관함</td></tr>
<tr><td>555</td><td><a href='https://arxiv.org/abs/2611.31347'>Antares-Smaug: Adversarial Names, Tokens and Attack Rewrites: Sanitisers Miss Unseen Generalisations</a></td><td>8</td><td>0</td><td>NLP</td><td>decision model Laya에 대한 prompt injection과 문자 공격 평가임. 합성 데이터, 단일 backbone, 일부 run 미실시라 근거가 약함</td></tr>
<tr><td>556</td><td><a href='https://arxiv.org/abs/2611.31457'>Taxi: Analyzing Agents at (Real) Scale</a></td><td>8</td><td>0</td><td>NLP</td><td>agent 궤적을 clustering과 SQL로 분석하는 도구 기술 보고서임. 연구 기여가 아닌 시스템 소개임</td></tr>
<tr><td>557</td><td><a href='https://arxiv.org/abs/2611.31480'>Evaluating Frontier-Model Agent Skills with Open-Weight Models in a Science Gateway</a></td><td>8</td><td>0</td><td>NLP</td><td>Pegasus 워크플로 skill을 open-weight 모델용으로 적응시키는 평가 사례임. 과학 gateway 도메인이고 로봇 무관함</td></tr>
<tr><td>558</td><td><a href='https://arxiv.org/abs/2611.31521'>PatientFlowSynth: Evaluating FHIR Agents with Matched Patient Charts</a></td><td>8</td><td>0</td><td>NLP</td><td>FHIR 환자 차트 agent 평가용 합성 벤치마크 PatientFlowSynth임. 의료 도메인이고 로봇 무관함</td></tr>
<tr><td>559</td><td><a href='https://arxiv.org/abs/2611.31579'>Provably Near-Optimal PQ in the Extended Zador Model</a></td><td>8</td><td>0</td><td>LG</td><td>Gaussian 가정 하에 product quantization의 SVD 회전 최적성과 EZPQ를 제시함. 벡터 양자화 이론이고 로봇 무관함</td></tr>
<tr><td>560</td><td><a href='https://arxiv.org/abs/2611.31611'>Multi-agent System for Automatic Discovery of Pareto-optimal Meta-solvers for PDEs</a></td><td>8</td><td>0</td><td>LG</td><td>LLM agent와 진화 알고리즘으로 PDE 선형 solver 조합의 Pareto front를 찾음. 수치해석 도메인이라 로봇 무관함</td></tr>
<tr><td>561</td><td><a href='https://arxiv.org/abs/2611.31653'>Constructing physical mechanisms with artificial intelligence</a></td><td>8</td><td>0</td><td>LG</td><td>arXiv 수식에서 물리 메커니즘을 조합해 구성하는 시스템임. 검증된 실험이 없고 로봇 무관함</td></tr>
<tr><td>562</td><td><a href='https://arxiv.org/abs/2611.31654'>Stranded Compute in AI Inference Workloads: Recovering Value Through Demand Aggregation</a></td><td>8</td><td>0</td><td>LG</td><td>AI 추론 인프라의 자본 회수 비용과 수요 풀링의 경제성 분석임. 로봇·embodied AI와 무관하고 방법론 기여도 없음</td></tr>
<tr><td>563</td><td><a href='https://arxiv.org/abs/2611.31737'>GreenDynaMix: Thermal-Aware Dynamic Mixed-Precision MoE LLM Inference Systems</a></td><td>8</td><td>0</td><td>LG</td><td>MoE LLM 추론의 GPU 온도와 혼합 정밀도 제어 시스템임. 로봇과 무관한 서버 최적화임</td></tr>
<tr><td>564</td><td><a href='https://arxiv.org/abs/2611.31873'>RepoEviAgent: Scalable Synthesis of Evidence-Grounded Repository-Level Question Answering Tasks</a></td><td>8</td><td>0</td><td>NLP</td><td>저장소 수준 질의응답 SWE 데이터 합성과 benchmark 구축임. 로봇과 무관함</td></tr>
<tr><td>565</td><td><a href='https://arxiv.org/abs/2611.32848'>Measurement Artifacts in Trustworthiness Evaluations of Quantized Small Language Models</a></td><td>8</td><td>0</td><td>NLP</td><td>양자화 소형 LLM 평가의 측정 아티팩트 분석임. 로봇과 무관함</td></tr>
<tr><td>566</td><td><a href='https://arxiv.org/abs/2611.32931'>Reading Decisions Before Spans: Efficient Generative Verification</a></td><td>8</td><td>0</td><td>NLP</td><td>생성형 verifier의 결정 토큰 이후 생성을 생략해 서비스 비용을 줄임. 로봇과 무관함</td></tr>
<tr><td>567</td><td><a href='https://arxiv.org/abs/2611.32946'>ShellBench: What Matters More for AI Agents, Models, or Harness for Everyday Tasks</a></td><td>8</td><td>0</td><td>NLP</td><td>일상 task agent의 모델 대 harness 효과를 비교하는 ShellBench임. 로봇과 무관함</td></tr>
<tr><td>568</td><td><a href='https://arxiv.org/abs/2611.32954'>LoomKV: Lossless KV Cache Compression from GPU Memory to SSD for LLM Serving</a></td><td>8</td><td>0</td><td>LG</td><td>LLM serving의 KV cache를 무손실 압축함. 시스템 최적화로 로봇과 무관함</td></tr>
<tr><td>569</td><td><a href='https://arxiv.org/abs/2611.33119'>MetaFORGE: A Meta-Learning Framework for Harness Optimization in Automated Code Generation for Parallel Computing</a></td><td>8</td><td>0</td><td>NLP</td><td>MPI 코드 생성 skill을 execution reward로 최적화함. 로봇과 무관함</td></tr>
<tr><td>570</td><td><a href='https://arxiv.org/abs/2611.32406'>BEACON: Learning Observation-Conditioned Starting Points for Guided Conditional Flow Matching in Microscopy</a></td><td>7</td><td>0</td><td>Generative</td><td>현미경 복원용 flow matching에서 관측 조건부 시작점을 학습하는 coupling 개선임. 도메인이 생명과학이고 로봇 무관함.</td></tr>
<tr><td>571</td><td><a href='https://arxiv.org/abs/2611.31245'>Local subspace encoding for spectral prediction: from TabPFN to operator-adaptive calibration</a></td><td>7</td><td>0</td><td>LG</td><td>TabPFN 스펙트럼 예측용 LVSE 표현을 재분석함. 분광 데이터 분석이고 robotics 무관함</td></tr>
<tr><td>572</td><td><a href='https://arxiv.org/abs/2611.31249'>Actionwave: A Systematic Benchmark for Waveform-Centric Clinical Prediction Across Care Scenarios</a></td><td>7</td><td>0</td><td>LG</td><td>임상 파형 예측 benchmark임. 의료 평가이고 robotics 무관함</td></tr>
<tr><td>573</td><td><a href='https://arxiv.org/abs/2611.31321'>Flagging Batch Shift in Flow Cytometry using Jeffreys Divergence between Gaussian Mixtures</a></td><td>7</td><td>0</td><td>LG</td><td>flow cytometry 배치 이동을 Jeffreys divergence로 탐지함. 임상 응용이고 robotics 무관함</td></tr>
<tr><td>574</td><td><a href='https://arxiv.org/abs/2611.31527'>ECLIPSE: Embedding-Centered Foundation-Model Federated Knowledge Transfer for Data-Free Edge Intelligence</a></td><td>7</td><td>0</td><td>LG</td><td>data-free federated knowledge transfer를 embedding 정렬로 하는 edge 분류 연구이고 로봇과 무관함.</td></tr>
<tr><td>575</td><td><a href='https://arxiv.org/abs/2611.32018'>Structure-Aware Transformers for Hierarchical Authorization in Personal AI Agents</a></td><td>7</td><td>0</td><td>LG</td><td>개인 AI agent의 계층적 권한 승인 예측용 transformer이고 로봇과 무관함.</td></tr>
<tr><td>576</td><td><a href='https://arxiv.org/abs/2611.32317'>SPRUNN: Structural Proximity for Pruning in Deep Neural Networks</a></td><td>7</td><td>0</td><td>CV</td><td>CNN 필터 pruning용 SPRUNN이고 일반 압축 기법으로 새로움이 낮음.</td></tr>
<tr><td>577</td><td><a href='https://arxiv.org/abs/2611.32734'>ASCENT: A Benchmark for Evaluating and Advancing Stepwise Diagnostic Reasoning in Large Language Models on Common Clinical Scenarios</a></td><td>7</td><td>0</td><td>NLP</td><td>MedQA에서 파생한 단계적 진단 추론 벤치마크 ASCENT임. 의료 LLM 평가라 로봇 무관함</td></tr>
<tr><td>578</td><td><a href='https://arxiv.org/abs/2611.32006'>TableRouter: Query-Aware Evidence Construction for Long-Table Question Answering</a></td><td>7</td><td>0</td><td>NLP</td><td>긴 표 질의응답에서 계산 경로와 coverage 경로를 고르는 TableRouter임. 로봇과 무관함</td></tr>
<tr><td>579</td><td><a href='https://arxiv.org/abs/2611.31703'>E-Waste-Bench: A Large-Scale Benchmark for Visual Triage of Data-Center Hardware</a></td><td>6</td><td>1</td><td>CV</td><td>데이터센터 폐기 하드웨어 분류 benchmark임. 로봇 분류 응용 가능성은 있으나 dataset 기여에 머묾</td></tr>
<tr><td>580</td><td><a href='https://arxiv.org/abs/2611.32138'>VIDE : Training-Free Video Anomaly Detection via Visual Intrinsic Distribution Estimation</a></td><td>6</td><td>1</td><td>Video</td><td>video anomaly detection을 training-free로 개선함. 로봇과 무관한 benchmark 개선임</td></tr>
<tr><td>581</td><td><a href='https://arxiv.org/abs/2611.31520'>Your Codec, Your Generator: Idempotent Generative Compression without Retraining</a></td><td>6</td><td>0</td><td>CV</td><td>사전학습 codec을 재학습 없이 idempotent 생성 압축으로 바꿈. 로봇과 무관함</td></tr>
<tr><td>582</td><td><a href='https://arxiv.org/abs/2611.31666'>A Piecewise-Linear Activation Function for Implicit Neural Representations</a></td><td>6</td><td>0</td><td>CV</td><td>INR용 piecewise-linear activation을 제안함. 로봇과 무관한 소규모 기법임</td></tr>
<tr><td>583</td><td><a href='https://arxiv.org/abs/2611.31849'>JECT: Addressing the Context Shortcut in Joint-Embedding Predictive Learning for Chest CT</a></td><td>6</td><td>0</td><td>CV</td><td>흉부 CT용 JEPA 사전학습의 context shortcut을 report 예측으로 완화함. 로봇과 무관함</td></tr>
<tr><td>584</td><td><a href='https://arxiv.org/abs/2611.32232'>MYSTIQUE: Few-Shot Facial Identity Transfer with Performance Preservation</a></td><td>6</td><td>0</td><td>CV</td><td>VFX용 얼굴 identity transfer로 로봇 무관함.</td></tr>
<tr><td>585</td><td><a href='https://arxiv.org/abs/2611.32383'>Improving Character Identity Consistency in Diffusion-Based Visual Story Generation through Identity Memory and Automatic Reranking</a></td><td>6</td><td>0</td><td>Generative</td><td>SDXL 기반 스토리 생성 캐릭터 일관성 파이프라인으로 기존 도구 조합임. 로봇 무관함.</td></tr>
<tr><td>586</td><td><a href='https://arxiv.org/abs/2611.32467'>TDD: Target-Discrepancy Distillation for Underwater Image Enhancement</a></td><td>6</td><td>0</td><td>CV</td><td>수중 이미지 향상을 target-discrepancy distillation으로 한 incremental 연구로 로봇 직접 관련 약함.</td></tr>
<tr><td>587</td><td><a href='https://arxiv.org/abs/2611.32474'>Progressive Reliable Supervision for Black-Box Universal Domain Adaptation</a></td><td>6</td><td>0</td><td>LG</td><td>black-box universal domain adaptation 의사 라벨 설계로 로봇 무관함.</td></tr>
<tr><td>588</td><td><a href='https://arxiv.org/abs/2611.32538'>Advanced Synthetic Image Detection Using Hybrid Feature Extraction</a></td><td>6</td><td>0</td><td>CV</td><td>CBAM과 ResNet50, DCT patch 선택으로 합성 이미지를 분류하는 흔한 조합임. 새로운 원리 없음</td></tr>
<tr><td>589</td><td><a href='https://arxiv.org/abs/2611.32591'>FewRef-5: Fixed-Reference Test-Time Adaptation for Virtual Staining</a></td><td>6</td><td>0</td><td>CV</td><td>virtual staining test-time adaptation에서 5개 reference 통계를 맞추는 loss를 더함. 의료 영상 한정이고 PSNR이 오히려 감소함</td></tr>
<tr><td>590</td><td><a href='https://arxiv.org/abs/2611.33061'>SUPRA: Synthesizing Amyloid PET from MRI and Plasma Biomarkers with an Explicit Regional SUVR Prior</a></td><td>6</td><td>0</td><td>CV</td><td>MRI와 혈장 biomarker로 amyloid PET를 합성함. 의료 응용이고 robotics 무관함</td></tr>
<tr><td>591</td><td><a href='https://arxiv.org/abs/2611.31354'>Detecting Harmful Short Videos in Toxic Diet Culture: A Governance-Ready Evidence Framework with Sparse Autoencoders</a></td><td>6</td><td>0</td><td>Multimodal</td><td>TikTok 유해 영상 탐지용 SAE 기반 증거 framework임. 콘텐츠 moderation이라 robotics 무관함</td></tr>
<tr><td>592</td><td><a href='https://arxiv.org/abs/2611.32225'>Joint Classification and Generation on Tabular Data: an Empirical Study</a></td><td>6</td><td>0</td><td>LG</td><td>tabular 데이터 joint classification and generation의 실증 비교이고 로봇과 무관함.</td></tr>
<tr><td>593</td><td><a href='https://arxiv.org/abs/2611.32489'>When Knowledge-Tracing Rankings Depend on Available History: A Source-Correction and Matched-Information Audit on ASSISTments 2009 and 2015</a></td><td>6</td><td>0</td><td>LG</td><td>knowledge tracing benchmark의 데이터 출처와 history 길이 감사로 로봇과 무관함</td></tr>
<tr><td>594</td><td><a href='https://arxiv.org/abs/2611.32568'>Representation and Model Contributions on Small Molecular Benchmarks: Controlled Comparisons and External Evaluation</a></td><td>6</td><td>0</td><td>LG</td><td>분자 특성 예측에서 representation과 model 기여를 분리한 benchmark 감사로 로봇과 무관함</td></tr>
<tr><td>595</td><td><a href='https://arxiv.org/abs/2611.32959'>Polynomial-Time Learning of Random Automata from One Label per Word</a></td><td>6</td><td>0</td><td>LG</td><td>무작위 automata를 단어당 레이블 하나로 다항시간에 학습하는 학습이론 논문임</td></tr>
<tr><td>596</td><td><a href='https://arxiv.org/abs/2611.33044'>When Is Product Decoding of ECOC MAP-Consistent? Pair Structure and the n-vs-Rest Codes</a></td><td>6</td><td>0</td><td>LG</td><td>ECOC product decoder의 MAP 일관성 조건을 Lean으로 증명한 이론임</td></tr>
<tr><td>597</td><td><a href='https://arxiv.org/abs/2611.31255'>INCLUDE-2.0: Disentangling Knowledge Gaps in Multilingual LLM Evaluation</a></td><td>6</td><td>0</td><td>NLP</td><td>91개 언어의 지역 지식 평가 benchmark임. 로봇과 무관한 다국어 평가 데이터 구축임</td></tr>
<tr><td>598</td><td><a href='https://arxiv.org/abs/2611.31257'>scOPD: Routed On-Policy Self-Distillation for LLM-Based Single-Cell Annotation</a></td><td>6</td><td>0</td><td>NLP</td><td>단일세포 annotation용 LLM on-policy self-distillation임. 생물 도메인이라 로봇과 무관함</td></tr>
<tr><td>599</td><td><a href='https://arxiv.org/abs/2611.31261'>Does Item Response Theory Generalize Across Languages? Evidence from Cross-Lingual LLM Benchmarks</a></td><td>6</td><td>0</td><td>NLP</td><td>IRT가 다국어 benchmark에서 일반화되는지 본 평가 방법론 연구임. 로봇과 무관함</td></tr>
<tr><td>600</td><td><a href='https://arxiv.org/abs/2611.31269'>Reliability of Language-Model Judges for Quantitative Scientific Question Answering: Evidence from Perovskite Photovoltaics</a></td><td>6</td><td>0</td><td>NLP</td><td>페로브스카이트 QA에서 LLM judge 신뢰도를 본 평가 연구임. 로봇과 무관함</td></tr>
<tr><td>601</td><td><a href='https://arxiv.org/abs/2611.31569'>CLAIMGATE: Cautious On-Device Checking of Spoken Legal and Clinical Claims</a></td><td>6</td><td>0</td><td>NLP</td><td>법률·의료 발화의 주장을 on-device에서 검증하는 시스템임. 로봇과 무관함</td></tr>
<tr><td>602</td><td><a href='https://arxiv.org/abs/2611.32368'>Decision Models: An Introduction and Capability Evaluation</a></td><td>6</td><td>0</td><td>NLP</td><td>typed 출력을 내는 decision model 서비스의 정확도와 지연 평가 보고임. 자사 모델 평가 성격이고 로봇 무관함</td></tr>
<tr><td>603</td><td><a href='https://arxiv.org/abs/2611.32525'>What If Chinese Were Latinized? A Counterfactual Study of Input Representation, Tokenization, and Language Modeling</a></td><td>6</td><td>0</td><td>NLP</td><td>중국어를 병음으로 바꾸면 tokenization과 LM 성능이 떨어짐을 보인 counterfactual 연구임. 로봇 무관함</td></tr>
<tr><td>604</td><td><a href='https://arxiv.org/abs/2611.32710'>Red-Teaming a Sovereign LLM, Its Reasoning and Its Training Stages</a></td><td>6</td><td>0</td><td>NLP</td><td>sovereign LLM의 system prompt 기밀 유지 실패를 red-teaming으로 보임. 로봇 무관함</td></tr>
<tr><td>605</td><td><a href='https://arxiv.org/abs/2611.31581'>Frequency-Conditioned Privacy Auditing of Fine-Tuned Language Models</a></td><td>6</td><td>0</td><td>LG</td><td>fine-tuning 데이터 내 반복 횟수에 따른 개인정보 추출 가능성을 측정함. 로봇 무관함</td></tr>
<tr><td>606</td><td><a href='https://arxiv.org/abs/2611.31851'>Modeling Event-Conditioned Emotional Expression Response with LLM Agents in a Synthetic Social Simulation</a></td><td>6</td><td>0</td><td>NLP</td><td>LLM agent의 사건 조건부 감정 반응 사회 시뮬레이션임. 로봇과 무관함</td></tr>
<tr><td>607</td><td><a href='https://arxiv.org/abs/2611.31983'>Discovering Bandwidth-Efficient Prefetchers to Shrink the Cache Hierarchy</a></td><td>6</td><td>0</td><td>LG</td><td>에이전트로 CPU prefetcher를 탐색하는 DuoArchitect임. 로봇과 무관한 컴퓨터 구조 연구임</td></tr>
<tr><td>608</td><td><a href='https://arxiv.org/abs/2611.32772'>RubikSQL-HB: Agentic Text-to-SQL with Knowledge in the Loop</a></td><td>6</td><td>0</td><td>NLP</td><td>knowledge workspace를 가진 text-to-SQL agent임. 로봇과 무관함</td></tr>
<tr><td>609</td><td><a href='https://arxiv.org/abs/2611.32792'>Accuracy of Noise Ceiling Estimators for Brain Scores</a></td><td>6</td><td>0</td><td>LG</td><td>뇌 점수 noise ceiling 추정기 정확도의 통계 분석임. 로봇과 무관함</td></tr>
<tr><td>610</td><td><a href='https://arxiv.org/abs/2611.31465'>A dataset of clinically similar image pairs from citation-linked case reports for medical image retrieval</a></td><td>5</td><td>0</td><td>CV</td><td>인용 연결로 의료 영상 유사 쌍 데이터셋을 만듦. 로봇과 무관한 데이터셋 기여임</td></tr>
<tr><td>611</td><td><a href='https://arxiv.org/abs/2611.31487'>GDD: A Remote Sensing Image Deepfake Detection and Manipulation Localization Dataset</a></td><td>5</td><td>0</td><td>CV</td><td>원격탐사 deepfake 탐지 데이터셋임. 로봇과 무관함</td></tr>
<tr><td>612</td><td><a href='https://arxiv.org/abs/2611.31524'>Fast Anatomy-Aware Diffeomorphic Augmentation for Brain MRI</a></td><td>5</td><td>0</td><td>CV</td><td>뇌 MRI용 해부학 기반 augmentation임. 로봇과 무관함</td></tr>
<tr><td>613</td><td><a href='https://arxiv.org/abs/2611.31882'>RELAY: Learning Compatible Representations One Encoder at a Time</a></td><td>5</td><td>0</td><td>CV</td><td>검색용 embedding을 점진적으로 교체할 때 호환성을 유지하는 학습법임. 로봇과 무관함</td></tr>
<tr><td>614</td><td><a href='https://arxiv.org/abs/2611.32014'>DynaCue: Comparing Motion and Timing Between Groups of Videos</a></td><td>5</td><td>0</td><td>Video</td><td>생성 영상 그룹의 움직임 차이를 검정하는 permutation test임. 로봇과 무관한 평가 지표임</td></tr>
<tr><td>615</td><td><a href='https://arxiv.org/abs/2611.32021'>HuluOPD: Unifying Heterogeneous Medical Specialists into One Lightweight Model with Unlabeled Prompts</a></td><td>5</td><td>0</td><td>Multimodal</td><td>의료 전문 VLM을 unlabeled prompt로 하나의 경량 모델에 distillation함. 로봇과 무관함</td></tr>
<tr><td>616</td><td><a href='https://arxiv.org/abs/2611.32135'>Interpretable Orthogonal Latent Diffusion with Scale-Selective Uncertainty for Medical Image Super-Resolution</a></td><td>5</td><td>0</td><td>CV</td><td>뇌 MRI super-resolution에서 불확실성을 분해해 hallucination 위험을 표시함. 로봇과 무관함</td></tr>
<tr><td>617</td><td><a href='https://arxiv.org/abs/2611.32193'>SolarFilNet-V4: Multi-Scale Transformer Vision with Physics-Informed Adaptive Post-Processing for Solar Filament Segmentation</a></td><td>5</td><td>0</td><td>CV</td><td>태양 filament segmentation 챌린지용 technical report로 로봇과 무관하고 기여가 대회 엔지니어링임.</td></tr>
<tr><td>618</td><td><a href='https://arxiv.org/abs/2611.32290'>$ε$-Seg++: Ensembling Across Hierarchy and Training Time for Label-Efficient EM Segmentation</a></td><td>5</td><td>0</td><td>CV</td><td>전자현미경 segmentation 앙상블 개선으로 로봇 무관함.</td></tr>
<tr><td>619</td><td><a href='https://arxiv.org/abs/2611.32329'>Cross-Version Compatibility of TESSERA Embeddings Through Lightweight Translation</a></td><td>5</td><td>0</td><td>CV</td><td>TESSERA 위성 embedding 버전 간 변환기 연구로 로봇 무관함.</td></tr>
<tr><td>620</td><td><a href='https://arxiv.org/abs/2611.32343'>Part-Set Prototypes for Explainable Mountain Gazelles Sex Classification</a></td><td>5</td><td>0</td><td>CV</td><td>산양 성별 분류용 prototype 설명 모델로 로봇 무관함.</td></tr>
<tr><td>621</td><td><a href='https://arxiv.org/abs/2611.32394'>Adaptive and Detection-Aware Super-Resolution for Small Object Detection</a></td><td>5</td><td>0</td><td>CV</td><td>SRCNN 계열 super-resolution과 소물체 검출 영향을 보는 소규모 분석임. 로봇 무관함.</td></tr>
<tr><td>622</td><td><a href='https://arxiv.org/abs/2611.32952'>FedTumor-IoMT: Federated Learning-Aided Brain Tumor Diagnosis on Resource-Constrained Edge IoMT Devices</a></td><td>5</td><td>0</td><td>CV</td><td>edge 기기용 federated 뇌종양 분할, 분류 프레임워크임. robotics 무관함</td></tr>
<tr><td>623</td><td><a href='https://arxiv.org/abs/2611.31442'>Small Learned Projections for Semantic-Reversal-Aware Retrieval with Spectral Acceleration: A Four-Domain Empirical Study</a></td><td>5</td><td>0</td><td>LG</td><td>신중히 선택한 trap 사례에만 성립하는 소형 투영 retrieval 연구이고 일부 구현이 비공개 상업 요소라 재현성과 로봇 관련성 모두 낮음.</td></tr>
<tr><td>624</td><td><a href='https://arxiv.org/abs/2611.32257'>Seldon TFM family: Seldon-Mini, Seldon and Seldon+</a></td><td>5</td><td>0</td><td>LG</td><td>tabular foundation model Seldon 기술 보고서이고 로봇과 무관함.</td></tr>
<tr><td>625</td><td><a href='https://arxiv.org/abs/2611.31262'>RegioZH: Unveiling Comprehension Disparities across Regional Chinese Varieties in LLMs</a></td><td>5</td><td>0</td><td>NLP</td><td>중국어 지역 변종 이해 benchmark임. 로봇과 무관함</td></tr>
<tr><td>626</td><td><a href='https://arxiv.org/abs/2611.31267'>ToneMamaba: Learning Contextualized Tonal Contours with Boundary-Reset State Space Models</a></td><td>5</td><td>0</td><td>Audio</td><td>표준 중국어 성조 인식용 boundary-reset state space model임. 로봇과 무관함</td></tr>
<tr><td>627</td><td><a href='https://arxiv.org/abs/2611.31614'>Tablassert: Declarative Extraction of Knowledge Graphs from Biomedical Tables</a></td><td>5</td><td>0</td><td>NLP</td><td>바이오메디컬 표를 YAML 선언으로 knowledge graph로 바꾸는 도구 보고서임. 연구 기여가 약하고 로봇과 무관함</td></tr>
<tr><td>628</td><td><a href='https://arxiv.org/abs/2611.32630'>MargEmbed-Akan: Bridging Twi Questions and English Knowledge through Cross-Lingual Score Distillation</a></td><td>5</td><td>0</td><td>NLP</td><td>Twi 질문과 영어 문서 검색용 임베딩 distillation 모델임. 저자원 언어 검색 한정이고 로봇 무관함</td></tr>
<tr><td>629</td><td><a href='https://arxiv.org/abs/2611.31684'>CROSS-Calib: Selective Channel Calibration for Ultrasound Reconstruction</a></td><td>5</td><td>0</td><td>CV</td><td>초음파 채널 보정 모델임. 의료 영상 신호 처리로 로봇과 무관함</td></tr>
<tr><td>630</td><td><a href='https://arxiv.org/abs/2611.31787'>SciFig2Data: A Workflow for Recovering Structured Data from Scientific Figures</a></td><td>5</td><td>0</td><td>CV</td><td>과학 논문 그림에서 데이터를 복원하는 파이프라인임. 엔지니어링 워크플로이고 로봇과 무관함</td></tr>
<tr><td>631</td><td><a href='https://arxiv.org/abs/2611.31823'>GaokaoMathGen: Chinese Gaokao Mathematics Finale Problem Generation Controlled by Latent Reasoning Structures</a></td><td>5</td><td>0</td><td>NLP</td><td>가오카오 수학 최종 문제 생성 프레임워크임. 로봇과 무관함</td></tr>
<tr><td>632</td><td><a href='https://arxiv.org/abs/2611.32247'>Refining and Aligning Clinical Reasoning with Health Guidelines via Formal Constraints</a></td><td>5</td><td>0</td><td>NLP</td><td>임상 가이드라인을 형식 제약으로 추론하는 VerClin임. 로봇과 무관함</td></tr>
<tr><td>633</td><td><a href='https://arxiv.org/abs/2611.32320'>Alpha-Beta Pruning via Monadic Continuations</a></td><td>5</td><td>0</td><td>LG</td><td>alpha-beta pruning을 monad로 형식화함. 로봇과 무관한 프로그래밍 이론임</td></tr>
<tr><td>634</td><td><a href='https://arxiv.org/abs/2611.32686'>CAPTA: Identifying LLMs Behind AI Agents</a></td><td>5</td><td>0</td><td>NLP</td><td>AI agent 뒤의 LLM을 선택형 질문으로 식별하는 CAPTA임. 로봇과 무관한 보안 연구임</td></tr>
<tr><td>635</td><td><a href='https://arxiv.org/abs/2611.33086'>Uncertainty-Aware Candidate Generation for Entity Linking in Cyber Threat Intelligence</a></td><td>5</td><td>0</td><td>NLP</td><td>사이버 위협 정보 entity linking의 불확실성 활용임. 로봇과 무관함</td></tr>
<tr><td>636</td><td><a href='https://arxiv.org/abs/2611.31506'>HyMTS: A Multiscale Tensor Factorization-Based Network for Hyperspectral Image Restoration</a></td><td>4</td><td>0</td><td>CV</td><td>hyperspectral 영상 복원용 텐서 분해 네트워크임. 로봇과 무관한 incremental 구조 제안임</td></tr>
<tr><td>637</td><td><a href='https://arxiv.org/abs/2611.31690'>GRUN: Generalized Retinex Unfolding Network for Image Restoration</a></td><td>4</td><td>0</td><td>CV</td><td>Retinex 기반 이미지 복원 unfolding network임. 로봇과 무관한 low-level vision 기법임</td></tr>
<tr><td>638</td><td><a href='https://arxiv.org/abs/2611.31989'>Reconstructing Natural Images from Brain Activity during Natural Vision</a></td><td>4</td><td>0</td><td>CV</td><td>원숭이 신경 신호로 자연 이미지를 복원함. 로봇과 무관함</td></tr>
<tr><td>639</td><td><a href='https://arxiv.org/abs/2611.32074'>Not the Scalar, but Its Evolution: Robust Source Attribution for Generated Images</a></td><td>4</td><td>0</td><td>CV</td><td>생성 이미지 출처 귀속을 spectral contraction으로 풂. 로봇과 무관함</td></tr>
<tr><td>640</td><td><a href='https://arxiv.org/abs/2611.32208'>FlashSegmentator: High-Throughput TotalSegmentator Inference without Loss of Accuracy</a></td><td>4</td><td>0</td><td>CV</td><td>TotalSegmentator 의료 CT 추론 속도 최적화 엔지니어링으로 로봇과 무관함.</td></tr>
<tr><td>641</td><td><a href='https://arxiv.org/abs/2611.31908'>TQ-HQNet: A Trainability-Aware and Qubit-Efficient Hybrid Quantum Neural Network for Cross-Domain Learning on Heterogeneous Data</a></td><td>4</td><td>0</td><td>LG</td><td>hybrid quantum neural network의 trainability 개선이고 로봇과 무관하며 고전 baseline이 일부 앞섬.</td></tr>
<tr><td>642</td><td><a href='https://arxiv.org/abs/2611.31251'>Validation Bias in Large Language Model Responses to Cancer Treatment Queries: A Factorial Cross-Sectional Study</a></td><td>4</td><td>0</td><td>NLP</td><td>암 치료 질의에 대한 LLM validation bias를 본 의료 안전 연구임. 로봇·embodied와 무관함</td></tr>
<tr><td>643</td><td><a href='https://arxiv.org/abs/2611.31259'>RecipeADQA: A User-aware Question-Answering Dataset for Multi-Constraint Recipe Recommendation</a></td><td>4</td><td>0</td><td>NLP</td><td>레시피 추천 QA 데이터셋 구축임. 로봇과 무관함</td></tr>
<tr><td>644</td><td><a href='https://arxiv.org/abs/2611.31263'>Evaluating Large Language Models on Iranian Doctoral Entrance Exams in Electrical and Computer Engineering</a></td><td>4</td><td>0</td><td>NLP</td><td>이란 박사 입학시험으로 LLM 4종을 평가한 보고임. 로봇과 무관함</td></tr>
<tr><td>645</td><td><a href='https://arxiv.org/abs/2611.31276'>Lexical Tone and Word Order Matter in Translation: Prosodic Correspondence Across Languages</a></td><td>4</td><td>0</td><td>Audio</td><td>번역 음성의 운율 대응을 언어별로 분석한 연구임. 로봇과 무관함</td></tr>
<tr><td>646</td><td><a href='https://arxiv.org/abs/2611.31532'>Can LLM-Simulated Respondents Pre-Test Survey Questions? Evidence From Preregistered Prospective Validation</a></td><td>4</td><td>0</td><td>NLP</td><td>LLM 시뮬레이션 응답자로 설문 문항을 사전 검사하는 사회과학 연구임. 로봇과 무관함</td></tr>
<tr><td>647</td><td><a href='https://arxiv.org/abs/2611.31578'>PazaBench: Large-Scale ASR Benchmark for Low-Resource Languages in Africa</a></td><td>4</td><td>0</td><td>Audio</td><td>아프리카 저자원 언어 ASR benchmark임. 로봇과 무관함</td></tr>
<tr><td>648</td><td><a href='https://arxiv.org/abs/2611.32303'>ArabFake: A multitask deep learning framework for Arabic fake news Detection, Categorization, and risk prediction</a></td><td>4</td><td>0</td><td>NLP</td><td>아랍어 가짜 뉴스 탐지 multitask 모델과 2,495건 데이터셋임. 로봇 무관하고 incremental임</td></tr>
<tr><td>649</td><td><a href='https://arxiv.org/abs/2611.32359'>Implementation of Machine Translation for the Uzbek Language Based on Transformer Models</a></td><td>4</td><td>0</td><td>NLP</td><td>Uzbek 기계번역을 T5/mT5 fine-tuning으로 구현함. 새로운 방법이 없고 로봇 무관함</td></tr>
<tr><td>650</td><td><a href='https://arxiv.org/abs/2611.32795'>Is Prosody Encoded in the Neural Audio Codec Mimi?</a></td><td>4</td><td>0</td><td>NLP</td><td>neural audio codec Mimi가 prosody를 담는지 보는 5쪽짜리 분석임. 로봇 무관함</td></tr>
<tr><td>651</td><td><a href='https://arxiv.org/abs/2611.32889'>Joint Detection of Constructive Speech, Hate Speech and Agreement in Online Conversations</a></td><td>4</td><td>0</td><td>NLP</td><td>영어와 덴마크어 댓글의 혐오, 건설적 발언 분류 데이터셋임. 로봇 무관함</td></tr>
<tr><td>652</td><td><a href='https://arxiv.org/abs/2611.32997'>Modelling Billingual Learning Through LLM Training: A Critical-Period Exploration</a></td><td>4</td><td>0</td><td>NLP</td><td>2-layer GPT-2로 bilingual critical period를 탐색한 예비 연구이며 run이 조건당 1회임. 로봇 무관함</td></tr>
<tr><td>653</td><td><a href='https://arxiv.org/abs/2611.33050'>Worth the Wait? How Response Time and Streaming Shape Judgments of Generative AI Answers and Chatbot Engagement</a></td><td>4</td><td>0</td><td>NLP</td><td>응답 지연과 streaming이 챗봇 투표에 미치는 영향을 본 HCI 분석임. 로봇 무관함</td></tr>
<tr><td>654</td><td><a href='https://arxiv.org/abs/2611.31708'>PRETZEL: A Benchmark for Cyclic Peptide Structure Prediction</a></td><td>4</td><td>0</td><td>LG</td><td>고리형 펩타이드 구조 예측 benchmark임. 단백질 구조 평가로 로봇과 무관함</td></tr>
<tr><td>655</td><td><a href='https://arxiv.org/abs/2611.31855'>Explainable Deep Learning for Malaria Parasite Detection and Species Differentiation in Thick Blood Smear Images: A Pilot Feasibility Study</a></td><td>4</td><td>0</td><td>CV</td><td>말라리아 기생충 검출과 설명 방법 합의 분석 pilot 연구임. 로봇과 무관함</td></tr>
<tr><td>656</td><td><a href='https://arxiv.org/abs/2611.32012'>Marketing-Bench: Evaluating Frontier Models and Agents on Real-World Marketing Capabilities</a></td><td>4</td><td>0</td><td>NLP</td><td>마케팅 능력 평가 benchmark임. 로봇과 무관함</td></tr>
<tr><td>657</td><td><a href='https://arxiv.org/abs/2611.32321'>FigmaEval: A Benchmark for Evaluating AI Agents in Professional UI Design</a></td><td>4</td><td>0</td><td>NLP</td><td>Figma UI 디자인 agent benchmark임. 로봇과 무관함</td></tr>
<tr><td>658</td><td><a href='https://arxiv.org/abs/2611.32646'>A Text-to-SQL Benchmark for Official Statistics</a></td><td>4</td><td>0</td><td>NLP</td><td>통계청 데이터 text-to-SQL benchmark임. 로봇과 무관함</td></tr>
<tr><td>659</td><td><a href='https://arxiv.org/abs/2611.31299'>PEACE-TEST-PROTOCOL: Polarization-Keyed Examination Papers and Mandatory Issued Eyewear that Displace AI Glasses and Extend Universal Design</a></td><td>3</td><td>0</td><td>CV</td><td>편광 필터 안경으로 시험지를 보호하는 보안 프로토콜이고 시뮬레이션만 있음. 로봇 학습과 무관함</td></tr>
<tr><td>660</td><td><a href='https://arxiv.org/abs/2611.31664'>LineEX: Data Extraction from Scientific Line Charts</a></td><td>3</td><td>0</td><td>CV</td><td>과학 line chart 데이터 추출 모델과 합성 dataset임. 로봇과 무관함</td></tr>
<tr><td>661</td><td><a href='https://arxiv.org/abs/2611.31774'>BODYBENCH: Evaluating Adversarial Image Defenses Against AI Nudification Inpainting</a></td><td>3</td><td>0</td><td>CV</td><td>nudification inpainting 방어를 평가하는 benchmark임. 로봇과 무관함</td></tr>
<tr><td>662</td><td><a href='https://arxiv.org/abs/2611.31777'>A Well-Posed Fourth-Order Navier-Stokes Model for Image Inpainting: Theory, Order Selection, and Stripe Decomposition</a></td><td>3</td><td>0</td><td>CV</td><td>Navier-Stokes 기반 inpainting PDE 모델의 이론 확장임. 로봇과 무관함</td></tr>
<tr><td>663</td><td><a href='https://arxiv.org/abs/2611.31984'>WaveSR: Physics-Inspired Wave Evolution Attention for Efficient Image Super-Resolution</a></td><td>3</td><td>0</td><td>CV</td><td>wave 방정식 기반 attention으로 이미지 super-resolution을 함. 로봇과 무관함</td></tr>
<tr><td>664</td><td><a href='https://arxiv.org/abs/2611.32002'>Change the Base, Change the Game: Rethinking Pan-sharpening</a></td><td>3</td><td>0</td><td>CV</td><td>원격탐사 pan-sharpening의 기준 이미지를 개선함. 로봇과 무관함</td></tr>
<tr><td>665</td><td><a href='https://arxiv.org/abs/2611.32034'>BodyWeave: Native Body-Conditioned 3D Garment Generation</a></td><td>3</td><td>0</td><td>3D Vision</td><td>body 조건 3D 의상 생성임. 로봇과 무관함</td></tr>
<tr><td>666</td><td><a href='https://arxiv.org/abs/2611.32266'>Unjamming Deferrals: Supporting Students Through JAMN Bot, a Mobile RAG-Grounded Policy Assistant</a></td><td>3</td><td>0</td><td>NLP</td><td>대학 시험 연기 안내용 RAG 챗봇 앱 사례임. 연구 기여 약하고 로봇 무관함</td></tr>
<tr><td>667</td><td><a href='https://arxiv.org/abs/2611.31329'>Conservative Overlap Fuzzy Rough Sets for Incomplete Data</a></td><td>3</td><td>0</td><td>LG</td><td>결측 데이터용 fuzzy rough set 속성 축소 방법이고 정확도 이득이 없음을 저자도 인정함. 로봇 무관함</td></tr>
<tr><td>668</td><td><a href='https://arxiv.org/abs/2611.31762'>Verified Proof Refactoring with Codex and Qwen</a></td><td>3</td><td>0</td><td>LG</td><td>Lean 4 증명 리팩터링 대회 시스템 보고임. 로봇과 무관함</td></tr>
<tr><td>669</td><td><a href='https://arxiv.org/abs/2611.32114'>An Automated Framework Integrating Deep Learning and Anatomical Reasoning for Cardiac Phenotyping From CCTA</a></td><td>2</td><td>0</td><td>CV</td><td>CCTA에서 심장 phenotyping을 자동화하는 의료 파이프라인임. 로봇과 무관함</td></tr>
<tr><td>670</td><td><a href='https://arxiv.org/abs/2611.32134'>EditText: Structure-Aware Generation and Selective Visual Transport for Fine-Grained Text Editing</a></td><td>2</td><td>0</td><td>CV</td><td>텍스트 편집용 생성 프레임워크임. 로봇과 무관함</td></tr>
<tr><td>671</td><td><a href='https://arxiv.org/abs/2611.32140'>LiteSTAR: Low-Rank Channel Modulation for Temporally Consistent CVD Video Compensation</a></td><td>2</td><td>0</td><td>CV</td><td>색각 이상 보정용 영상 recoloring 경량 모델임. 로봇과 무관함</td></tr>
<tr><td>672</td><td><a href='https://arxiv.org/abs/2611.32144'>CSC-Mamba: Bridging multimodal convolutional sparse coding and state space models for multi-contrast MRI super-resolution</a></td><td>2</td><td>0</td><td>CV</td><td>multi-contrast MRI super-resolution용 Mamba 구조임. 로봇과 무관함</td></tr>
<tr><td>673</td><td><a href='https://arxiv.org/abs/2611.32326'>Longitudinal Characterization of Personalized Hydration Dynamics Using a Facial-Video Digital Hydration Biomarker</a></td><td>2</td><td>0</td><td>CV</td><td>성인 5명 대상 얼굴 영상 수분 지표 탐색 연구로 로봇 무관함.</td></tr>
<tr><td>674</td><td><a href='https://arxiv.org/abs/2611.32159'>Breaking the Binary-Lifting Barrier for DNA Minimizer Density: Exact Optimization of a Native 4-ary Order at (w, k) = (12, 5)</a></td><td>2</td><td>0</td><td>LG</td><td>DNA minimizer 순서 최적화임. 로봇과 무관함</td></tr>
<tr><td>675</td><td><a href='https://arxiv.org/abs/2611.32505'>An Integrated Remote Sensing and Machine Learning Framework for Mapping Hazard Associated with Leached Metals</a></td><td>1</td><td>0</td><td>CV</td><td>석탄재 부지 금속 용출 위험을 위성 영상과 머신러닝으로 매핑한 환경 연구로 로봇 무관함.</td></tr>
</tbody></table>

</details>
