# 오늘의 arXiv Top 15: 2026-11-26 (목)

> 대상: cs.CV, cs.LG, cs.RO, cs.CL, cs.AI 의 **New submissions 전수 평가**

**신규 논문 수: 전체 625편 → 중복 제거 후 625편 (이번 평가 대상 625편)**

| 카테고리 | New submissions |
|---|---|
| cs.CV | 242 |
| cs.LG | 143 |
| cs.RO | 89 |
| cs.CL | 74 |
| cs.AI | 77 |

---

## Top 15

### 1. SplatWAM: Splatting World Action Models for Real-Time 3D Imagination (78점)

[arXiv](https://arxiv.org/abs/2611.33467) · [PDF](https://arxiv.org/pdf/2611.33467) · [alphaXiv](https://www.alphaxiv.org/abs/2611.33467)

- **저자**: Frank Tsu-Fang Lu, Karthik Sundar Senthilkumar, Christopher Thirgood, Oscar Mendez, Simon Hadfield
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> 로봇 world model이 미래를 픽셀이나 latent가 아니라 3D Gaussian 2,048개로 된 상태로 직접 예측하게 해서, 예측한 장면을 어느 시점에서든 rasterization만으로 그려 볼 수 있게 함. OGBench Scene(시뮬레이션 조작 환경)에서 새 시점 rollout을 video world model보다 약 12배 빠르게(약 80 FPS) 그리고 더 높은 PSNR로 만들고, 같은 backbone의 policy가 LIBERO 평균 성공률 92.3%를 냄.

**무슨 문제인가**

video 생성 기반 world model은 픽셀을 먼저 만들기 때문에 그리퍼가 테이블을 뚫는 것처럼 기하적으로 불가능한 장면을 만들 수 있음. 새 시점을 보려면 시점마다 다시 sampling하거나 생성된 video를 따로 3D로 올려야 하고, 시점끼리 기하가 어긋나는 것을 구조적으로 막지 못함. latent world model은 3D 상태를 드러내지 않아 새 시점을 보려면 별도 decoder가 필요함. 4D Gaussian splatting은 렌더링 가능한 상태를 갖지만 장면마다 최적화하는 재구성이라 action에 따라 미래를 생성하지 못함.

**어떻게 푸나**

SplatWAM(Splatting World Action Model)은 tokenizer, dynamics, policy 세 부분이 같은 Gaussian 상태를 주고받는 구조임. SplatWAM-T는 카메라 pose가 없는 RGB 여러 장을 fine-tuning한 VGGT backbone에 넣고, 학습된 query 2,048개를 각각 Gaussian 하나(위치, 회전, 크기, 불투명도, 색)로 decode함. query가 장면과 시간에 걸쳐 공유되므로 i번째 Gaussian은 매 frame 같은 index를 가짐. SplatWAM-D는 과거 Gaussian 상태들과 action을 받아 다음 상태를 생성하는 causal transformer임. 학습에는 frame마다 noise 수준을 따로 주는 diffusion forcing과, 큰 denoising step 하나를 작은 step 두 개에 맞추는 Dreamer 4의 shortcut-forcing 목적함수를 씀. 공분산은 quaternion과 scale 대신 log-Euclidean 6차원 좌표로 표현해 부호 모호성을 없애고, 예측 상태를 held-out 시점에서 렌더링한 이미지 loss를 더함. SplatWAM-P는 같은 backbone에 agent token과 flow-matching action head를 붙여, 관측된 Gaussian 상태 이력과 목표(goal 상태 또는 CLIP 문장 embedding)를 읽고 action chunk를 출력함. 학습은 T 단독, T를 고정한 D, D와 P 공동 학습 순서로 진행됨.

**결과**

- OGBench(오프라인 goal-conditioned 조작 benchmark) Scene에서 16-step open-loop rollout을 held-out 새 시점 3개로 렌더링한 PSNR이 23.37 dB임. video world model인 Cosmos3-Edge(NVIDIA Cosmos 3)의 출력을 SplatWAM-T로 3D로 올린 경우는 21.82 dB, Gaussian 기반 world model인 GWM은 9.18 dB임. 속도는 RTX 5090 batch 1에서 78.8 FPS 대 Cosmos3-Edge 6.6 FPS임. 입력 시점에서는 Cosmos3-Edge가 앞섬(PSNR 25.30 대 24.57 dB, FVD 26 대 173).
- 같은 시작 상태에 정해진 action을 넣고 예측 frame으로 성공을 판정한 반사실 action 시험(과제당 32회)을 함. cube를 서랍에 넣고 서랍을 밀어 넣은 뒤 다시 여는 과제에서 cube가 다시 보이는 비율이 SplatWAM-D 100%, Cosmos3-Edge 38%, iVideoGPT 3%임. cube 밀기 과제는 SplatWAM-D 41%, 두 video model 0%로 모든 모델에게 가장 어려운 과제임.
- 같은 action head와 두 시점 입력으로 model-free policy를 비교함. OGBench 4개 환경 평균 성공률이 Gaussian token 63.4%, 픽셀 49.3%임. LIBERO에서는 65.3% 대 63.0%로 차이가 작고, Object와 Goal suite에서는 픽셀이 앞섬.
- SplatWAM-P(약 1B)는 LIBERO(시뮬레이션 언어 조건 조작 suite 4개) 평균 성공률 92.3%를 냄. robot pretraining 없는 OpenVLA-OFT(약 7B, wrist camera와 proprioception 사용) 91.9%와 비슷하고 WorldVLA 79.1%보다 높음. robot pretraining한 OpenVLA-OFT 97.1%에는 못 미침. OGBench Scene에서는 52%로 물체 keypoint 기반 latent world model인 LPWM 40%보다 높고 value function을 쓰는 HIQL 49%와 비슷함.

**한계**

모든 실험이 OGBench와 LIBERO 시뮬레이션이고 실로봇 실험은 없음. 학습에 시뮬레이터 상태를 재생해 카메라 9대로 렌더링한 다시점 영상을 쓰므로, 실제 환경에서 같은 감독 신호를 얻기 어려움. policy는 관측된 이력만 읽고 상상한 rollout을 planning에 쓰지 않아, world model의 예측 능력이 control에 얼마나 기여하는지는 직접 보이지 않음. D와 P를 공동 학습하면 입력 시점 16-step rollout PSNR이 24.02 dB에서 22.00 dB로 내려가고, 코드와 checkpoint는 공개 예정이라고만 밝힘.

**누리랩 연구와의 연결**

- action 조건으로 3DGS 상태를 예측하고 임의 시점에서 렌더링하므로, active perception(NBV)에서 후보 시점을 상상 렌더링으로 미리 평가하는 world model로 쓸 수 있음. object-centric 3DGS world model 연구의 비교 대상임.
- 반사실 action 시험(접촉 시 관통 여부, 서랍 속 물체 유지)은 world model 기반 failure prediction과 counterfactual reasoning의 평가 프로토콜로 그대로 가져다 쓸 수 있음. 상상 rollout을 test-time planning에 쓰는 실험은 이 논문에 없어 직접 검증이 필요함.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. SplatWAM-T가 context view를 Gaussian 상태로 바꾸고, SplatWAM-D가 action을 받아 다음 상태를 H번 예측함. rasterizer가 예측 상태에서 새 시점 이미지를 그림. 아래쪽 SplatWAM-P는 goal 상태나 CLIP 문장 token을 읽어 action chunk를 내고, 세 학습 단계의 loss가 점선으로 표시됨.*

---

### 2. Long-Horizon Planning with Latent World Models via Graph Anchors (74점)

[arXiv](https://arxiv.org/abs/2611.34509) · [PDF](https://arxiv.org/pdf/2611.34509) · [alphaXiv](https://www.alphaxiv.org/abs/2611.34509)

- **저자**: Syed Nazmus Sakib, Abdul Monaf Chowdhury, Peizhen Li, Nafiul Haque, Chandak Chakma, Md Mehedi Hasan, Zehong Cao, Shifat E. Arman
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 66점
- **학회**: CoRL 양식 (추정) · 근거: 1단 구성, 초록 아래 'Keywords:' 줄
- **읽은 원문**: PDF 전문

> frozen latent world model의 planner가 먼 목표 이미지 대신 기록된 경로 위 몇 걸음 앞의 학습 frame을 겨누게 하는 training-free planner Graph Anchors를 제안함. 200 step 떨어진 PointMaze-Medium(점 agent가 미로를 지나 목표로 가는 과제) 목표에서 기존 latent world model LeWM의 성공률을 13%에서 85%로 올림.

**무슨 문제인가**

latent world model planner는 예측한 마지막 latent와 목표 이미지 latent의 거리가 가장 작은 action sequence를 고름. 이 방식은 25 step 정도 가까운 목표에서는 잘 되지만, 목표가 멀어지면 LeWM(LeWorldModel: pixel에서 encoder와 predictor를 함께 학습한 latent world model)의 성공률이 크게 내림. 저자들은 원인을 두 가지로 나눔. 첫째는 range 실패로, latent 거리가 목표 근처 몇 걸음 밖에서는 어느 쪽이 목표에 가까운지 구분하지 못함. 둘째는 focus 실패로, 이미지 전체 거리가 작은 조작 물체보다 큰 로봇 팔의 위치를 더 크게 반영해 접촉 과제에서 물체를 놓고 팔만 맞춤.

**어떻게 푸나**

먼저 기록된 데이터에서 planner 없이 진단을 함. 목표에서 h hop 떨어진 상태의 두 이웃 중 실제로 더 가까운 쪽의 latent 거리가 더 작게 나오는 비율(ranking accuracy ρ)을 잼. 이 진단을 바탕으로 Graph Anchors는 world model의 학습 frame을 5 step마다 node로 삼아 sparse graph를 한 번 만듦. 같은 episode의 연속 frame은 방향 있는 temporal edge로, 다른 episode의 가까운 latent(10-NN, 한 action block 거리의 중앙값 이내)는 neighbour edge로 잇음. 매 replanning마다 현재 관측과 목표 이미지를 가장 가까운 node에 붙이고, 최단 경로에서 K hop 앞의 node를 anchor로 골라 CEM(Cross-Entropy Method, 샘플링 기반 action 최적화)의 목표로 씀. 접촉 과제에서는 다른 episode로 건너뛰는 edge에 가중치 λ=3을 매겨 기록된 밀기 동작이 이어지는 경로를 고름. 마지막으로 rollout을 마지막 step이 아니라 anchor에 가장 가까이 간 step으로 평가해 anchor를 지나쳐 가게 함. encoder, predictor, CEM 설정은 LeWM 그대로이고 바뀌는 것은 목표와 점수 규칙뿐임.

**결과**

- 진단: 모든 navigation 환경에서 ρ가 목표 바로 옆에서는 1에 가깝다가 6 hop 안에 우연 수준(0.5)에 가까운 0.50~0.59로 내림. raw pixel부터 V-JEPA 2까지 encoder 6종에서 같은 양상임. Meta-World(시뮬레이션 로봇 팔 조작 과제 모음) 9개 과제에서 손만 5cm 옮긴 비용이 물체만 목표에서 벗어난 비용보다 2.6~14배 큼. 원래 cost는 물체 episode 72개 중 0개를 풀고, demonstration에서 20 step 앞 frame을 겨누면 65개를 풂.
- 먼 목표 성공률(목표까지 step 수의 2배 budget, 50쌍 3 seed): PointMaze-Large(점 agent가 큰 미로를 지나 목표 이미지 위치로 가는 과제) 400 step에서 LeWM 8%가 87%로 오름. Push-T(평면에서 T자 블록을 밀어 목표 자세에 맞추는 과제) 150 step에서는 LeWM 5%가 접촉 설정 71%로 오름.
- 같은 LeWM 탐색을 anchor로 겨누기만 해도 PointMaze-Medium 200 step 성공률이 12%에서 85%로 오름. 이 12%는 구성 요소 제거 실험의 별도 실행 값이고, 본 비교표의 LeWM 값은 13%임. 마지막 step 대신 최근접 step으로 평가하는 탐색을 먼 목표에 그대로 쓰면 9%임. horizon을 2배, CEM sample을 3배 넘게 늘려도 28%에 그침.
- 다시 구현한 training-free planner와 같은 checkpoint·같은 목표 쌍으로 비교함. Push-T 150 step에서 AP(Anchored Planning: 실제 step 수 d를 받아 학습 episode 한 구간을 검색하는 방법)는 65%임. 같은 조건에서 다른 training-free planner인 NGC는 11%, Metro-WM은 33%임. AP는 d를 0.5배로 잘못 주면 16%로 내림. OGBench-Cube(블록 집기·옮기기)에서는 Graph Anchors의 contact 설정이 navigation 설정의 26%에서 39%로 오르지만 AP의 53%보다 낮음. 모든 실험은 시뮬레이션이고 실로봇 실험은 없음.

**한계**

anchor를 쓰려면 학습 데이터가 목표까지의 경로를 덮어야 하고, 과제마다 navigation(K=6, λ=1)과 contact(K=2, λ=3) 설정을 골라야 함. contact 설정은 Reacher에서 68%를 54%로 낮추고, 6 hop 앞 anchor에 정확히 도달하지 못하는 다른 latent world model PLDM과 DINO-WM은 PointMaze-Medium에서 4%, 20%에 그침. 환경은 2D 미로, Push-T, Cube, Reacher 같은 시뮬레이션뿐이고, 본문에 프로젝트 페이지와 코드가 있다고 적혀 있으나 주소는 텍스트에서 확인 불가임.

**누리랩 연구와의 연결**

- world model 기반 test-time planning에서 goal cost가 언제 방향 정보를 잃는지를 planner 없이 offline으로 재는 진단 방법(ρ, graph 거리와 성공률의 Spearman −0.90)임. world model planner의 실패를 미리 예측하는 failure diagnosis 도구로 가져다 쓸 수 있음.
- 학습 데이터의 frame graph를 subgoal 기억으로 쓰는 방식은 robot memory, long-horizon planning 연구와 바로 이어짐. 손 대 물체 비용 비율을 잰 focus 분석은 object-centric 표현이 manipulation planning cost에 필요한 이유를 보여 주는 근거로 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 개념도임. 학습 episode frame을 frozen encoder로 embedding해 temporal edge와 nearest neighbour edge로 graph를 만드는 단계가 왼쪽에 있음. 가운데는 실제 PointMaze-Medium node 위의 최단 경로와 6 hop 앞 anchor를, 오른쪽은 CEM rollout을 anchor 최근접 거리로 평가하는 과정을 보여 줌.*

---

### 3. Keep or Roll Back? Out-of-Loop Judges for Self-Improving VLA and End-to-End Embodied Policies (73점)

[arXiv](https://arxiv.org/abs/2611.33794) · [PDF](https://arxiv.org/pdf/2611.33794) · [alphaXiv](https://www.alphaxiv.org/abs/2611.33794) · [프로젝트 페이지](https://zilin-huang.github.io/SealedLoop/)

- **저자**: Zilin Huang, Zhengyang Wan, Kangan Qian, Zihao Sheng, Sikai Chen
- **분야**: Embodied AI · robotics relevance 9/10 · 1차 스크리닝 70점
- **읽은 원문**: PDF 전문

> VLA·주행 policy의 self-improvement loop에서 새 policy를 남길지 정하는 판정을 학습용 judge에서 떼어 내, improver가 볼 수 없는 sealed judge 위의 sequential test로 결정하게 함. 실제 gain이 알려진 주행 policy 쌍 76개(gain 12개, 손실 59개, 차이가 0에 가까운 5개)에서 이 test는 gain 12개 중 11개를 받아들이고, 손실 59개와 0에 가까운 5개는 하나도 받아들이지 않음.

**무슨 문제인가**

Self-improvement loop는 policy가 rollout하고, judge가 episode를 채점하고, 좋게 채점된 데이터로 policy를 다시 학습하는 과정을 반복함. 대부분의 loop에서는 학습 신호를 주는 judge가 새 policy를 남길지(keep) 되돌릴지(roll back)도 정하므로, 판정 근거가 policy와 독립적이지 않음. 저자들은 loop가 보고한 gain이 독립 평가와 어긋나는 원인을 둘로 나눔. judge가 loop 자신의 데이터에서 성능을 잘못 재는 judge error와, loop 데이터에서의 진짜 gain이 처음 보는 조건으로 이어지지 않는 transfer gap임. 저자들이 조사한 embodied loop 56개 중 세대별 성능 곡선과 judge exploitation 사례를 함께 정량화한 연구는 없었음.

**어떻게 푸나**

SealedLoop은 loop 바깥에 sealed judge를 둠. sealed judge는 평가 조건 pool, judge 파라미터, 표본 추출 규칙이 improver(후보 policy를 학습하는 loop 쪽 과정)에게 숨겨진 평가자이며, 세대마다 improver가 돌기 전에 고정됨. improver는 in-loop judge(success classifier, 학습된 critic, VLM 등)만 써서 후보 policy를 만듦. 판정 단계에서는 이전 policy와 후보를 같은 조건 쌍에서 돌리고, 쌍별 점수 차이로 betting confidence sequence(언제 멈춰 읽어도 신뢰수준이 유지되는 구간 추정)를 갱신함. 구간 하한이 0보다 크면 accept, 상한이 0보다 작으면 reject, budget까지 결론이 안 나면 roll back함. 조건이 policy와 독립으로 뽑히면 손해인 후보를 받아들일 확률이 α(실험에서 0.05) 이하로 묶임(Proposition 1). 같은 loop를 in-loop judge가 결정하는 경우와 sealed judge가 결정하는 경우로 따로 돌리고, 두 judge가 모든 세대를 채점함. 그래서 보고된 gain과 sealed gain의 차이(judge gap)를 세대마다 judge error와 transfer gap으로 나눠 잼.

**결과**

- LIBERO-Object(시뮬레이션에서 물체를 집어 바구니에 넣는 조작 과제 모음) 3개 과제에서 OpenVLA-OFT를 rejection-sampling fine-tuning으로 개선함. 한 세대에서 success classifier가 실패 196개 중 65개를 성공으로 판정함(물체가 바구니 가장자리에 걸린 경우). sealed judge가 결정하면 후보 45개 중 12개가 남음. sealed test가 확인한 이들의 성공률 상승(certified gain)은 평균 0.147임. classifier가 결정하면 sealed test가 손해로 확인한 후보 1개를 남기고, certified gain이 있는 후보 3개를 버림.
- 기성 judge로 바꿔도 해결되지 않음. 가장 큰 Qwen3-VL-32B는 같은 세대에서 실패를 3%만 받아들여 classifier의 33%보다 낮음. 대신 진짜 성공도 많이 거부해(true-positive rate 0.69) 시뮬레이터의 성공 판정 규칙(success predicate)과 결정이 일치한 세대가 38개 중 26개로, classifier의 35개보다 적음.
- NAVSIM(기록된 주행 로그에서 계획 궤적을 채점하는 driving benchmark) DiffusionDrive loop에서 transfer gap이 나타남. 공개 checkpoint에서 시작한 run의 PDMS(NAVSIM의 0~1 rule-based 주행 점수)가 loop 평가 frame에서 0.047~0.058 오르고, 학습에 없던 Boston에서 0.075~0.107 내림. loop frame의 진짜 점수로 판정해도, 공개 checkpoint에서 시작한 이 control run의 세대 15개 중 8개를 받아들임. 개선이 실제로 일어나는 loop에서 최종 Boston PDMS는 0.638에서 sealed judge 결정 시 0.674, critic 결정 시 0.649가 됨.
- 실차 실험은 loop가 아니라 공개된 개선 단계 하나(ReCogDrive의 IL 버전에서 RL 버전으로, NAVSIM 점수가 0.861에서 0.904로 오름)를 실제 도로에서 비교함. 전기 밴으로 144 m 좌회전 경로를 blind pair 6쌍 주행했고, 12회 모두 경로를 완주하지 못함. RL 버전이 6쌍 모두 커브에 더 깊이 들어가 첫 개입 지점이 평균 41.2 m에서 51.6 m로 늘었음(one-sided sign test p=0.016). 다만 sequential test는 6쌍으로 결론을 내지 못함.

**한계**

self-improvement loop는 모두 시뮬레이션에서만 돌렸고, 짧은 조작 과제 3개와 다른 차량이 반응하지 않는 로그 재생 driving benchmark 하나, 각각 improver 하나뿐임. 조작 실험의 sealed judge는 시뮬레이터의 success predicate로, 실제 로봇에는 이것이 없음. success predicate를 대신할 sealed judge로 시험한 Qwen2.5-VL-7B는 false-positive rate가 0.24로 오차가 큼. 실차 실험은 차량 하나에서 개선 단계 하나를 장애물 없는 경로로 시험했고, 코드 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- VLA를 RL이나 자기 데이터로 계속 fine-tuning하는 연구에서 success classifier·VLM judge가 겉보기 성공(look-alike failure)을 받아들이는 정도를 세대별로 재는 평가 절차로 바로 쓸 수 있음. failure detection용 VLM judge를 만들 때 false-positive와 true-positive를 함께 보고해야 하는 근거가 됨.
- 학습용 judge와 수용 판정을 분리하고 anytime-valid sequential test로 평가량을 줄이는 방식임. 실로봇 평가 횟수가 적은 test-time adaptation이나 world model 기반 policy 개선의 keep/roll back 판정에 옮겨 쓸 수 있음.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. 왼쪽은 in-loop judge와 기성 VLM judge가 각각 결정하는 기존 방식임. 오른쪽은 Seal, Improve, Decide(sequential test), Reveal 네 단계와 judge gap을 judge error와 transfer gap으로 나누는 식을 보여 줌.*

---

### 4. Most of the Way There: Turning a Strong Video Prior into an Action-Conditioned World Model (72점)

[arXiv](https://arxiv.org/abs/2611.34435) · [PDF](https://arxiv.org/pdf/2611.34435) · [alphaXiv](https://www.alphaxiv.org/abs/2611.34435) · [프로젝트 페이지](https://xmz111.github.io/Dianjing/)

- **저자**: Zanyi Wang, Xia Chen, Liu Liu, Xianglong Guo, Dengyang Jiang, Haodong Li, Tingyang Xiao, Wenhao Hu 외 1명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> 33B video 생성 모델을 고정한 채 0.34% 파라미터만 학습해 로봇 행동을 조건으로 미래 영상을 예측하는 world model로 바꿈. 학습을 높은 noise 구간에 몰아준 것만으로 validation 평균 점수가 52.69에서 61.15로 오름.

**무슨 문제인가**

최근 video 생성 모델은 그럴듯한 장면은 잘 만들지만, 특정 로봇 행동이 낳는 물리적 결과까지 맞히지는 못함. 같은 '잡아라' 지시라도 실제 실행에 따라 성공, 빗나감, 물체 무반응으로 갈리므로 action-conditioned world model(ACWM)은 행동별 결과를 예측해야 함. 기존 로봇 ACWM은 full fine-tuning, 카메라 calibration이 필요한 렌더링 action map, 별도 memory module, 수천 시간 로봇 데이터를 더해 왔음. 이 설계들은 모두 14B 이하 prior 위에서 나왔고, 더 강한 prior에서는 무엇이 꼭 필요한지 따져 본 연구가 없었음.

**어떻게 푸나**

Dianjing은 MiniMax H3(33B video foundation model)를 고정하고 rank-32 LoRA와 action projection만 학습함(약 114M, 0.34%). 입력은 첫 이미지, 선택적 text, 로봇 action 열이고 출력은 미래 영상임. 먼저 AgiBot G2(52차원)와 YAM(14차원)의 명령을 forward kinematics로 양팔 end-effector 상대·절대 pose와 gripper 값의 30차원 벡터(EEF30)로 바꿈. 이 벡터는 블록마다 zero-init 선형층을 거쳐 기존 AdaLN(noise 수준에 따라 layer norm을 조절하는 경로)의 shift·scale·gate에 더해짐. 학습은 flow-matching 목적을 그대로 두고 timestep 분포를 높은 noise 쪽으로 옮겨, 학습 신호의 절반 이상이 σ≥0.9에 오게 함. 긴 rollout은 124 frame 단위로 이어 만들며, 앞 구간의 마지막 clean latent 3개를 H3의 기존 reference 경로로 다음 구간에 넘김.

**결과**

- WorldOracle(예측 영상을 같은 action의 실제 로봇 실행 영상과 비교하는 benchmark) 공식 test의 SV 점수로 잼. SV(single-view score)는 물리 상태 정확도, 상호작용 영역 충실도, 상호작용 공간 정렬 점수의 평균임. 5개 track 중 4개에서 1위이고, AgiBot-Core는 73.48로 GE-Sim 2.0의 73.20과 거의 같음. YAM-Core는 70.71로 2위보다 7.7점 높음. 사람이 조작한 긴 rollout을 평가하는 AgiBot-Long track에서는 56.43으로 GE-Sim 2.0의 62.57보다 낮음.
- 학습 데이터는 약 65시간으로, 기존 로봇 world model인 GE-Sim 2.0(>1k 시간), GigaWorld-1(12,980시간), DreamDojo(44.7k 시간)보다 훨씬 적음.
- validation 47 episode 단계별 ablation에서 평균 SV가 zero-shot 24.49, 영상만 학습 38.65, EEF30 action 추가 52.69, high-noise 학습 61.15, 기존 reference 경로 사용 63.33으로 오름.
- 같은 backbone에 기존 설계를 옮겨 붙인 비교에서 trajectory map은 1.5점, action에 classifier-free guidance를 거는 action CFG는 3.6점 내림. 별도 action token은 high-noise 학습 뒤 0.4점 내림.

**한계**

평가는 기록된 실제 실행 영상과의 offline 비교뿐이고, 이 world model로 policy를 평가하거나 planning에 쓴 실험은 없음. 긴 rollout에서 Core 대비 점수가 크게 내리고 물체 위치·자세 오차가 누적됨. 본문에 코드 공개 언급이 없고, 33B backbone을 H20 GPU 32장으로 학습해 재현 비용이 큼.

**누리랩 연구와의 연결**

- 강한 video prior 위에서는 action 주입 방식보다 학습을 어느 noise 구간에 몰아주는지가 더 중요하다는 ablation은 world model 기반 policy 평가와 test-time planning을 설계할 때 바로 참고할 수 있음.
- 팔 동작은 맞아도 물체 상태가 틀리는 사례(수건 걸기)는 world model로 failure detection을 할 때 무엇을 검증해야 하는지 보여 줌.

*대표 그림: 측정 결과가 아니라 논문의 문제 설정과 방법 구조를 그린 개요 그림임. 왼쪽은 video prior의 일반 영상 생성 예시와 물리 오류 사례이고, 오른쪽은 과일 집기 장면을 위에서부터 zero-shot 예측, Dianjing 예측, 실제 실행(GT) 순서로 세 줄에 보여 줌.*

---

### 5. Beyond the Happy Path: Generalizing Robot World Models from Simulated Failures (72점)

[arXiv](https://arxiv.org/abs/2611.33925) · [PDF](https://arxiv.org/pdf/2611.33925) · [alphaXiv](https://www.alphaxiv.org/abs/2611.33925) · [프로젝트 페이지](https://aim-uofa.github.io/WorldReforge/)

- **저자**: Zhiyue Zhao, Mingyu Liu, Bolin Zhang, Liyang Li, Guangyu Huang, Canyu Zhao, Jinchuan Shi, Haokai Zhang 외 2명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 70점
- **읽은 원문**: PDF 전문

> 성공 demonstration 위주로 학습된 로봇 world model이 잡기 실패 장면을 못 그리는 문제를, 시뮬레이션에서 일부러 만든 실패 궤적 약 62,000개와 물리 정답 기반 보조 loss 두 개로 post-training해 줄임. 사전학습된 영상 world model인 Cosmos3 Nano의 물체 궤적 평균 픽셀 오차(object ADE)를 9.07픽셀에서 6.51픽셀로 28.2% 낮춤.

**무슨 문제인가**

action-conditioned world model은 policy 평가와 planning에서 실제 rollout을 대신하는 용도로 쓰이므로, 행동이 다르면 결과가 다르게 나와야 함. 그런데 로봇 학습 데이터는 성공 demonstration이 대부분이라, 잡기가 조금 어긋나 물체가 밀리거나 기울거나 미끄러지는 장면을 거의 보지 못함. 저자 측정에서 사전학습 모델 5개의 물체 궤적 오차는 첫 frame을 그대로 복사하는 static baseline보다 많아야 10.4% 낮았고, 2개는 오히려 더 나빴음. 실패 데이터로 fine-tuning한 기존 연구도 있으나, 접촉 영역은 화면의 작은 부분이라 전역 reconstruction loss에서 비중이 작음. 또 성공·실패 같은 결과 수준 신호는 물체가 어떻게 움직였는지는 알려 주지 않음.

**어떻게 푸나**

먼저 Reforge dataset을 만듦. 시뮬레이션에서 RoboLab과 motion planner cuRobo로 성공하는 기준 잡기 궤적을 만든 뒤, end-effector 위치, 회전, gripper closure 시점을 흔들어 성공·실패 궤적 62,125개(물체 96종)를 얻음. 각 궤적에는 RGB 영상과 함께 물체 pose, 접촉 여부, 물체 표면 점의 위치가 정답으로 기록됨. 실제 실패 궤적 300개(물체 10종, Reforge-Real)는 평가에만 씀. WorldReforge는 이 정답으로 기존 flow matching 생성 loss에 보조 loss 두 개를 더하는 post-training 방법임. 입력은 첫 관측 영상과 기록된 end-effector pose·gripper 상태이고, 출력은 카메라 3대(wrist, 왼쪽 어깨, 오른쪽 어깨)에서 본 미래 16 frame의 RGB 영상임. Interaction Alignment(IA)는 물체와 접촉 주변을 덮는 soft mask 안에서만 복원 오차를 재고, mask 면적으로 나눠 작은 영역도 따로 학습 신호를 받게 함. Surface Correspondence(SC)는 backbone 중간 feature에서 첫 frame의 표면 점 feature를 뽑아 미래 wrist-view feature와 cosine 유사도로 soft matching함. 이렇게 찾은 위치가 시뮬레이터로 투영한 정답 궤적과 맞도록 학습시킴. 두 loss 모두 학습 때만 쓰이므로 추론 시 파라미터나 구조는 바뀌지 않음.

**결과**

- 물체 궤적 오차(object ADE, 생성 영상에 CoTracker를 돌려 시뮬레이터 정답과 비교한 픽셀 오차)를 Reforge-Eval(시뮬레이션 평가 clip)에서 잼. Cosmos3 Nano 기준 사전학습 9.07, 같은 데이터에 생성 loss만 쓴 Reforge 6.81, WorldReforge 6.51임. 데이터만으로 오차가 약 25% 줄고, IA·SC가 4.4%를 더 줄임. post-training에 없던 물체에서는 9.86픽셀에서 6.41픽셀로 내림.
- 같은 첫 장면에서 다른 행동을 준 100쌍으로, 두 미래의 차이를 얼마나 맞게 그리는지 RDE(Response Difference Error)로 잼. 사전학습 Cosmos3 Nano는 7.35로 static baseline 6.06보다 나쁨. WorldReforge는 4.17로 사전학습보다 43.3% 낮고 Reforge 4.34와는 차이가 작음.
- segment 6,400개로 돌린 소규모 ablation에서 object ADE는 Reforge 7.02, IA만 6.84, SC만 6.81, 둘 다 6.59임. SC 정답을 CoTracker pseudo-label로 바꾸면 6.87로 오름.
- 시뮬레이션에서만 학습했는데 실제 영상 복원 PSNR이 DROID(실제 로봇 조작 영상 모음)에서 20.38에서 21.42dB로, Reforge-Real에서 20.80에서 21.48dB로 오름. 실제 영상에서는 물체 궤적 정답이 없어 PSNR·SSIM과 VLM 판정 품질만 잼.

**한계**

world model을 policy 평가, planning, closed-loop 제어에 실제로 써서 나아지는지는 보이지 않았고, 저자도 향후 과제로 남김. 실제 데이터는 평가에만 쓰였고 지표가 PSNR 위주라 실제 실패 상황의 물체 움직임 정확도는 확인되지 않음. 사람 영상의 지식을 로봇으로 옮기는 다른 world model인 DreamDojo는 같은 post-training 후 object ADE가 9.57에서 11.62로 오히려 나빠짐. IA·SC가 Reforge 대비 더하는 이득은 2~5% 수준임. 반복 실행 편차는 본문에서 확인 불가함. 데이터·코드는 공개 시 내놓겠다고 적혀 있음.

**누리랩 연구와의 연결**

- world model이 실패 장면을 못 그리면 이를 쓰는 policy 평가와 failure detection이 성공 쪽으로 치우침. 이 진단과 paired-action RDE 지표는 world model 기반 failure 예측 연구의 평가 설계에 바로 쓸 수 있음.
- 성공 데이터는 잡은 상태 유지를, 실패 접촉 데이터는 물체 반응을 가르친다는 데이터 구성 분석은 counterfactual rollout용 world model 학습 데이터를 어떻게 섞을지 정할 때 근거가 됨.

*대표 그림: Reforge dataset의 구성을 요약한 그림이며, 모델 성능 측정 결과는 아님. 위쪽은 흔든 실행 요소별 궤적 수(위치 51,964, 회전 5,720, closure 시점 4,356)를, 아래쪽은 gripper가 열린 채 또는 오므린 채 접촉한 실패, 물체 이동·기울어짐, 잡기 유지·놓침 같은 결과 유형별 예시 frame과 개수를 보여 줌.*

---

### 6. Skeptic: Grounding Failure Diagnosis for Robot Skill Discovery (72점)

[arXiv](https://arxiv.org/abs/2611.33560) · [PDF](https://arxiv.org/pdf/2611.33560) · [alphaXiv](https://www.alphaxiv.org/abs/2611.33560)

- **저자**: Wenfang Sun, Jianghao Deng, Wenzhe Yin, Yingjun Du, Cees G. M. Snoek
- **분야**: Embodied AI · robotics relevance 8/10 · 1차 스크리닝 66점
- **읽은 원문**: PDF 전문

> 로봇 프로그램을 고쳐 가며 skill을 쌓는 코딩 agent가 실패 한 번을 '물리적으로 불가능함'으로 잘못 결론 내리는 문제를, 센서로 잰 동작 결과 기록과 성공 기반 skill 등록 규칙으로 줄임. 가중치를 고정한 Qwen3.8-27B의 LIBERO-Pro 80개 과제 held-out 성공률이 63.4%에서 78.3%로 오름.

**무슨 문제인가**

code-as-policy 방식의 agentic skill discovery에서는 언어 모델이 로봇 프로그램을 실행하고, 실패 기록을 보고 고치고, 교훈을 공유 skill library에 남김. 그런데 API 호출이 완료되었다는 반환값은 의도한 접촉이 실제로 일어났다는 뜻이 아님. 저자들이 관찰한 Qwen3.8-27B는 gripper가 허공을 잡은 실패를 '서랍이 기계적으로 막힘'으로 해석하고, 같은 서랍을 쓰는 다른 과제까지 같은 이유로 종료함. 이런 잘못된 불가능 판정은 수정 예산이 남았는데도 탐색을 끝내고, library에 들어가면 뒤 과제의 시도까지 막음.

**어떻게 푸나**

SKEPTIC은 학습 없이 기존 ASPIRE 프로토콜에 두 장치를 더함. ASPIRE는 coordinator·worker·verifier가 같은 언어 모델로 과제별 프로그램을 고치고, verifier가 재현한 교훈을 공유 skill library에 쌓는 방식임. 첫 장치인 grounded event log는 실패한 개발 실행의 primitive 호출 기록, 매 step proprioception, 동작 시점 depth 영상을 입력으로 받아 텍스트 로그를 만듦. 로그에는 이동이 목표에 닿았는지와 남은 거리, gripper jaw가 멈춘 폭과 손가락 사이 표면 유무, 분할된 물체가 최종적으로 어디 있는지가 적힘. 항목마다 [proprio]·[vision]·[inferred] 표시를 달아 센서 관측과 추론된 진단을 구분함. 두 번째 장치인 verified promotion은 skill 제안을 등록할 때 verifier 재현에 더해, 제안을 낸 원래 프로그램이 개발 seed에서 기준 이상 성공했는지를 요구함(LIBERO-Pro에서 15개 중 8개 이상). 등록 판정은 agent가 수정할 수 없는 별도 서비스가 실행 기록에서 성공률을 계산해 내림.

**결과**

- LIBERO-Pro(LIBERO 조작 과제에 물체 위치와 지시 문장 변형을 넣은 시뮬레이션 benchmark) 80개 과제에서 과제당 held-out seed 50개의 성공률을 잼. ASPIRE 63.4%에서 SKEPTIC 78.3%로 14.9퍼센트포인트 오름(과제 bootstrap 95% CI 8.4~21.6). 같은 모델·시작 library·수정 예산이며, 프로토콜마다 campaign 2회의 평균임. campaign은 80개 과제를 정해진 순서로 풀며 skill library를 따로 쌓는 실행 한 번임.
- 저자들이 Object·Goal·Spatial 60개 과제의 실패 기록을 직접 읽어 셈한 결과, 잘못된 불가능 판정이 나온 과제가 campaign당 19.5개에서 8.5개로 줄어듦. 그 판정 뒤 80% 미만으로 끝난 과제는 14.0개에서 4.5개로 줄어듦. verified promotion만 넣으면 잘못된 판정은 16개로 거의 그대로이고, 판정 자체를 줄인 것은 event log임.
- 같은 60개 과제의 ablation에서 성공률은 ASPIRE 70.1%, verified promotion만 81.3%, event log만 80.8%, 전체 86.9%임.
- Robosuite(단일 팔 5개와 양팔 2개로 된 시뮬레이션 조작 과제) 7개에서 과제당 100 seed 평균 성공률이 35.3%에서 47.0%로 오름. 상승분 대부분은 큐브 다시 쌓기(62%에서 97%)와 양팔 들기(0%에서 29%)에서 나오고, nut assembly는 두 방법 모두 0%임. 모든 실험은 시뮬레이션이며 실로봇 과제는 없음.

**한계**

실험은 Qwen3.8-27B 한 모델과 시뮬레이션 benchmark 2개뿐이고, 비슷한 크기의 다른 open-weight 모델 5개는 원래 discovery loop 자체를 돌리지 못해 비교에서 빠짐. log는 손 움직임·jaw 폭·분할 물체의 depth 변화만 재므로 knob 각도 같은 관절 상태나 지시가 뜻하는 목표 영역은 잡지 못함. 그래서 ASPIRE가 풀던 과제 2개를 SKEPTIC campaign이 불가능으로 판정하고 끝낸 사례가 있음. 본문 1쪽에 'Project Page & Code' 문구는 있으나 텍스트에서 주소는 확인 불가임.

**누리랩 연구와의 연결**

- failure diagnosis를 VLM의 추론이 아니라 실행 측정값에 묶은 사례임. 센서 관측과 추론을 표시로 나누는 로그 형식은 VLA rollout의 실패 원인 분석과 recovery 연구에 바로 가져다 쓸 수 있음.
- 실패 경험이 '불가능' 교훈으로 memory에 들어가 뒤 과제를 막는 현상과, source 프로그램 성공률로 등록을 막는 규칙은 robot memory·skill library 설계에서 비교 대상이 됨.

*대표 그림: 같은 서랍 과제의 실제 실행 기록을 위쪽에 ASPIRE, 아래쪽에 SKEPTIC으로 보인 그림임. 위는 허공을 잡은 실패를 '기계적 정지'로 해석해 다른 과제까지 실패로 끝내는 과정이고, 아래는 event log가 빈 그립을 알려 손잡이 잡는 방향을 바꿔 서랍을 15 cm 열고 크림치즈를 넣는 과정임.*

---

### 7. Dynamic Forcing: Learning Action-Grounded Sparse Dynamic Representations with Dense Future Guidance for World Action Models (71점)

[arXiv](https://arxiv.org/abs/2611.33799) · [PDF](https://arxiv.org/pdf/2611.33799) · [alphaXiv](https://www.alphaxiv.org/abs/2611.33799)

- **저자**: Ziqiang Li, Shisheng Chen, Yunnan Wang, Wenyao Zhang, Zili Lin, Yuyang Zhang, Xudong Yang, Fangzhuo Jin 외 3명
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> world action model이 미래 영상 전체를 만들지 않고, 현재 관측 옆에 변화만 담는 소수의 dynamic token을 붙여 행동을 만들게 함. LIBERO-Plus 성공률 77.9%로 같은 계열 WAM 중 가장 높았고, 지연시간은 Faster-WAM의 172.8ms에서 158.5ms로 줄어듦.

**무슨 문제인가**

world action model(WAM)은 미래 장면을 예측하는 video model 위에서 행동을 만드는 policy임. 미래 영상을 촘촘히 만들면 시공간 token이 많아져 추론 비용이 큼. 미래 예측을 추론에서 빼 버린 Fast-WAM은 빠르지만, 후속 평가에서 분포 이동에 약해진다는 보고가 있었음. Faster-WAM은 영상 expert를 한 번만 통과시켜 미래 조건을 유지하는 후속 방법이고, Fast-WAM-Joint는 Fast-WAM 논문의 변형임. 저자들은 dense future가 현재 관측에 이미 있는 정적 배경을 반복해 담고, action expert의 attention은 물체가 움직이는 좁은 영역에 몰린다는 관찰에서 출발함.

**어떻게 푸나**

CompactWAM은 Wan2.2-TI2V-5B video backbone 하나를 dense 경로와 sparse 경로가 공유하는 구조임. 입력은 현재 관측과 언어 지시이고, 출력은 32-step action chunk임. sparse 경로의 compact dynamic token은 현재 관측을 겹치지 않는 영역 R개로 평균 낸 값에 noise를 섞어 만들고, 영역 중심 좌표와 미래 시점을 3D rotary position embedding(3D-RoPE)으로 붙임. 학습 때 dense 경로는 미래 영상과 행동을 예측하고, sparse 경로는 영상 복원 loss 없이 자기 action expert의 행동 loss로만 학습됨. attention mask로 sparse token이 dense future feature를 보지 못하게 막음. 여기에 Dynamic Forcing이라는 두 가지 보조 loss를 더함. FG(action functional guidance)는 두 action expert의 attention 출력에서 예측 문맥이 기여한 부분만 떼어 sparse 쪽을 dense 쪽에 맞춤. DA(dynamics-aware distribution matching)는 다른 시점 간 feature 유사도를 같은 시점 유사도로 원소별로 나눈 뒤 정규화한 분포를 만들고, sparse 분포를 dense 분포에 KL로 맞춤. 추론 때는 dense 경로를 버리고 현재 관측과 dynamic token을 한 번의 visual forward로 encode한 뒤 KV cache로 행동을 denoising함.

**결과**

- LIBERO-Plus(LIBERO 학습 policy를 카메라·로봇·조명·배경 등 7종 교란 아래 추가 학습 없이 평가)에서 CompactWAM 77.9%, Faster-WAM 73.6%, Fast-WAM-Joint 66.3%, Fast-WAM 49.1%임. LIBERO(조작 과제 40개) 평균은 98.4%로 Faster-WAM 99.0%보다 0.6퍼센트포인트 낮음. 기본 dynamic token 36개 기준임.
- 같은 학습 augmentation으로 baseline을 다시 학습한 부록 비교에서는 LIBERO-Plus 차이가 줄어듦. CompactWAM 77.9%, Faster-WAM 74.3%, Fast-WAM 64.1%임. 본문 표의 Fast-WAM 대비 28.8퍼센트포인트 향상에는 학습 설정 차이가 섞여 있음.
- 같은 checkpoint에서 추론 경로만 바꾼 비교에서 LIBERO-Plus 성공률은 sparse 경로 77.9%, dense 경로 79.4%, dynamic token 제거 5.7%임. dynamic token 18개(dense future token의 9.2%)로도 76.6%를 유지함. H20 GPU 지연시간은 158.5ms로 Faster-WAM 172.8ms, Fast-WAM-Joint 537.5ms보다 짧음.
- 실제 AGIBOT G2 양팔 로봇 과제 3개(과일 집기, 블록 쌓기, 책상 정리)를 과제당 시연 200개로 학습함. 평균 성공률이 in-distribution에서 86% 대 Faster-WAM 75%, out-of-distribution에서 74% 대 56%임.

**한계**

실로봇은 과제 3개뿐이고, 본문에서 과제당 시행 횟수와 OOD 조건 구성은 확인 불가함. LIBERO-Plus 본문 표의 baseline 수치 일부는 학습 augmentation이 다른 보고값이라 공정 비교로 보기 어렵고, 저자도 이 벤치마크 지시문에 장면 metadata가 섞여 있다고 밝힘. 학습 때는 dense 경로 전체를 함께 돌려야 하므로 학습 비용은 줄지 않고, 코드 공개 주소는 본문에 없음.

**누리랩 연구와의 연결**

- world model을 행동 생성에 쓸 때 미래를 얼마나, 어떤 형태로 상상해야 하는지를 token 예산과 ablation으로 잰 사례임. world model 기반 VLA의 추론 비용을 줄이는 연구에서 baseline으로 쓸 수 있음.
- dynamic token을 지우면 성공률이 5.7%로 내려감. 부록에서는 고정된 dynamic token만 읽는 probe가 미래 frame의 움직임을 복원함. 두 결과는 이 token을 예측 실패 감지나 counterfactual rollout용 압축 상태로 쓰는 실험의 출발점이 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 그림임. (a)는 현재 관측, compact dynamic token, 미래 영상 token이 video-action joint attention backbone을 공유하고 두 action expert가 각각 action chunk를 내는 구조임. (b)와 (c)는 FG loss와 DA loss의 계산 과정을 보여 줌.*

---

### 8. Can Visual World Models See Force? (68점)

[arXiv](https://arxiv.org/abs/2611.34422) · [PDF](https://arxiv.org/pdf/2611.34422) · [alphaXiv](https://www.alphaxiv.org/abs/2611.34422)

- **저자**: Felix Tristram, Benjamin D. Killeen, Nassir Navab
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 78점
- **읽은 원문**: PDF 전문

> 영상 world model, VLA, 영상·이미지 encoder의 고정된 feature에 선형 probe를 붙여 조작 중 접촉력을 읽어 낼 수 있는지 잰 분석 논문임. 대부분 접촉 시점은 맞히지만 힘의 크기는 못 읽고, 가장 나은 V-JEPA 2.1도 Hoi! gripper 시점에서 접촉 중 힘 분산의 17%만 설명함(R² 0.166).

**무슨 문제인가**

world model과 VLA는 장면이 어떻게 바뀌고 어떤 행동을 할지 예측하지만, 힘 제어는 저수준 제어기에 맡기는 경우가 많음. 접촉이 많은 과제에서 힘을 잘못 주는 것이 robot foundation model의 실패 원인으로 보고되어 있음. 냉장고 문과 찬장 문처럼 궤적은 비슷해도 필요한 힘이 다른 경우가 있어서, 영상만으로 학습한 representation에 힘 정보가 들어 있는지가 문제임. 기존 probing 연구는 기하, 물리적 그럴듯함, 탄성·마찰 같은 성질을 다뤘지만 관측된 상호작용의 힘은 재지 않았음.

**어떻게 푸나**

저자는 force awareness를 세 능력으로 나눔: 접촉 시점 탐지, 접촉 중 힘 변화 추적, 힘 크기 복원임. 입력은 64 frame(7.5 Hz, 8.5초) 영상 구간이고, 2 frame씩 묶은 32개 time step마다 측정된 힘 벡터 크기의 평균(N)을 회귀 목표로 둠. 모델 weight는 고정하고, 중간 layer의 공간 token마다 같은 affine map으로 점수를 매긴 뒤 max pooling해 time step별 힘을 냄. 이 probe의 파라미터는 feature 차원 d에 bias 1개를 더한 d+1개이고, 시간 module이 없음. 영상 world model은 video autoencoder latent를 noise 0과 빈 text prompt로 diffusion transformer에 통과시켜 feature를 뽑음. VLA는 vision encoder부터 language model 각 block까지 image token을 뽑음. 세 능력은 각각 AUROC(접촉 step 판별), 접촉 구간 안의 Pearson r(변화 추적), 접촉 step 전체의 R²(크기 복원)로 잼. R²가 음수면 평균 접촉력을 상수로 내는 것보다 못하다는 뜻임. 같은 모델의 기본 checkpoint와 로봇 데이터로 추가 학습한 checkpoint 4쌍(예: Wan 2.1 I2V 14B와 이를 바탕으로 한 DreamZero)도 비교함.

**결과**

- Hoi!(사람이 힘 센서 달린 gripper로 서랍·문·찬장을 조작하는 영상과 힘 측정 dataset) gripper 시점에서 접촉 구간 안 힘 변화 상관 r은 V-JEPA 2.1이 0.527로 가장 높음. 14B world model Wan 2.1 I2V는 0.353, OpenVLA-7B는 0.152임. 힘 크기 R²가 0보다 2 표준오차 이상 높은 모델은 V-JEPA 2.1(0.166)뿐이고, 사람 시점에서는 모든 모델의 R²가 음수임.
- RH20T(손목 force-torque 센서가 있는 원격조작 로봇 조작 dataset, 140개 이상 과제)에서도 순서가 유지됨. V-JEPA 2.1의 r은 0.203, R²는 0.133이고, 영상 없이 과제별 평균 힘을 내는 task prior는 r 0.023임. π0와 GR00T N1.7의 r은 0.069와 0.032이고, 예측 힘의 변동폭이 측정값의 0.17배와 0.18배에 그침.
- 로봇 데이터 추가 학습은 힘 추적을 일관되게 올리지 못함. 4쌍 중 3쌍은 차이가 1 표준오차 안임. DreamZero는 Hoi! gripper 시점 r이 0.46으로 Wan I2V 14B의 0.35보다 높지만, RH20T에서는 0.15로 0.18보다 낮음.
- V-JEPA 2.1을 RH20T 힘 label로 LoRA fine-tuning하면 RH20T r이 0.19에서 0.33으로, R²가 0.10에서 0.23으로 오름. 이 실험은 마지막 block을 probe하므로 시작값이 둘째 불릿의 주 표 값과 다름. RH20T에서 학습한 readout을 Hoi! gripper 시점에 그대로 쓰면 r이 LoRA encoder에서 0.21, 고정 encoder에서 0.03임. 다만 LoRA encoder의 R²는 -0.92로, 힘의 시간 변화만 옮겨 가고 크기는 옮겨 가지 않음.

**한계**

오프라인 dataset 두 개에서 probe 정확도만 쟀고, 실로봇 제어나 policy 성능과의 관계는 실험하지 않음. Hoi!는 사람이 손으로 gripper를 든 데이터이고 평가 window가 260개라 R² 표준오차가 모델 간 차이만큼 큼. 선형 probe만 써서 비선형 readout으로 더 많은 힘 정보가 나오는지는 확인하지 않았고, V-JEPA 2.1과 DreamZero가 나은 이유는 저자의 가설로만 제시됨. 코드 공개 여부는 본문에서 확인 불가.

**누리랩 연구와의 연결**

- 현재 영상 world model과 VLA feature에 힘 크기 정보가 거의 없다는 결과는, contact-rich manipulation의 failure detection을 영상 world model만으로 하기 어렵다는 근거가 됨. 힘·tactile 신호를 world model 학습 목표에 넣는 연구의 동기로 쓸 수 있음.
- 고정 feature, max pooling 선형 probe, AUROC·r·R² 세 지표로 이뤄진 평가 절차는 우리가 학습한 world model이나 VLA encoder에 물리량이 들어 있는지 점검하는 도구로 그대로 쓸 수 있음.

*대표 그림: 위쪽은 서랍을 여는 장면의 영상을 고정된 foundation model과 linear probe에 넣어 힘을 읽는 구조를 그린 개념도임. 아래쪽은 Hoi! gripper 시점 접촉 하나에서 측정 힘(약 21 N 정점)과 V-JEPA 2.1·Wan 14B probe 예측(약 8~9 N 정점)을 겹친 그래프로, 접촉 시점은 맞지만 크기는 못 따라감을 보임.*

---

### 9. DriftWAM: Faster World-Action Models via Action-Aware Video Drifting (68점)

[arXiv](https://arxiv.org/abs/2611.33797) · [PDF](https://arxiv.org/pdf/2611.33797) · [alphaXiv](https://www.alphaxiv.org/abs/2611.33797)

- **저자**: Minyang Li, Siyu Xu, Yunke Wang, Ying-Cong Chen, Chang Xu, Daochang Liu
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 74점
- **읽은 원문**: PDF 전문

> 영상을 먼저 예측하고 그 영상에 맞춰 행동을 만드는 world-action model을 1단계 생성기로 증류할 때, 영상끼리의 유사도를 그 영상이 만드는 행동까지 함께 보고 재도록 바꿈. RoboTwin 2.0 50개 과제에서 영상·행동을 각각 1단계로 생성하는 설정(1v/1a, teacher 대비 21.46배 빠름)의 평균 성공률이 Flash-WAM의 76.21%에서 82.19%로 오름.

**무슨 문제인가**

WAM(world-action model)은 미래 영상을 diffusion이나 flow matching으로 예측하고 그 영상을 조건으로 robot action을 만듦. 영상과 행동을 모두 수십 단계 denoising으로 뽑으므로 행동 한 덩어리를 만드는 데 RTX 4090에서 약 4.8초가 걸려 closed-loop 제어에 느림. 기존 few-step 증류인 Flash-WAM은 영상 쪽에 LCM(latent consistency model) 계열 consistency distillation을 그대로 써서 teacher 영상과 겉모습이 닮도록만 학습함. 저자들은 영상이 행동을 이끄는 중간 표현일 뿐인데, 겉보기에 가까운 영상과 행동을 비슷하게 만드는 영상이 자주 다르다고 지적함. 부록 실험에서 후보 2개 중 시각적으로 가까운 영상과 행동이 가까운 영상이 41.37%의 경우에서 서로 달랐음.

**어떻게 푸나**

DriftWAM은 drifting(생성 샘플을 학습 중 kernel 가중치로 목표 샘플 쪽으로 끌고 다른 생성 샘플에서 밀어내어 1단계 생성기를 학습하는 분포 정합 방법)을 영상 증류에 씀. 입력은 관측·이전 행동·언어 지시로 된 context이고, 1단계 student가 영상 후보 4개를 만들며 teacher가 미리 offline으로 뽑은 영상-행동 쌍 4개를 목표로 둠. 두 영상의 시각 거리는 고정된 teacher 영상 branch의 19번째 Transformer block 특징으로 잼. 행동 거리는 고정된 teacher 행동 branch에 같은 noisy action을 넣고 두 영상을 조건으로 했을 때 나온 flow velocity의 차이로 잼(action response). 두 거리를 합친 joint kernel이 끌어당김과 밀어냄의 가중치를 정하는 것이 action-aware video drifting임. 같은 kernel로 student 영상마다 가장 잘 맞는 teacher 영상을 고르고, 둘의 action response 차이를 줄이는 손실(action-guided video regularization)로 행동 수준 gradient를 영상 생성기에 직접 흘림. 행동 branch는 Flash-WAM과 같은 consistency distillation과 flow matching 손실로 따로 학습함.

**결과**

- RoboTwin 2.0(양팔 조작 과제 50개, 장면·조명·배경을 흔드는 Randomized split 포함)에서 영상 1단계·행동 1단계(1v/1a) 평균 성공률이 Flash-WAM 76.21%, DriftWAM 82.19%임. 같은 조건 teacher LingBot-VA(25v/50a)는 90.77%이고, 두 증류 모델의 속도는 teacher 대비 21.46배로 같음. 과제 길이 구분(Horizon 1~3) 중 가장 긴 Horizon=3 과제의 Randomized split에서는 44.40%에서 65.80%로 21.4퍼센트포인트 차이가 남.
- 추가 학습량 효과를 가른 대조 실험에서, 같은 Flash-WAM checkpoint를 원래 목적함수로 500 step 더 학습하면 1v/1a 평균 76.40%, DriftWAM 목적함수로 500 step 학습하면 83.20%임(1,000 episode 평가).
- 구성요소 ablation(1v/1a)에서 단순 video drifting만 쓰면 79.10%이고, joint kernel을 더하면 80.57%, action-guided video regularization까지 더하면 82.19%임. 시각 거리로만 짝을 고른 regularizer는 79.33%로 거의 오르지 않아, 행동을 보고 짝을 고르는 부분이 효과의 대부분을 냄.
- LIBERO(시뮬레이션 단일팔 조작 과제 4개 suite, 각 10개)에서 1v/1a 평균이 96.9%로 Flash-WAM 논문 보고값 95.1%보다 높음. 실로봇 AgileX Piper 팔 과제 3개(과제당 20회)에서 1v/2a 평균 성공률이 DriftWAM 45.0%, Flash-WAM 40.0%, 단계만 줄인 teacher 25.0%, 3v/10a teacher 53.3%임.

**한계**

실로봇은 과제 3개·과제당 20회이고 Flash-WAM과의 차이는 과제당 1~2회 성공 차이라 통계적으로 약함. LIBERO 비교는 Flash-WAM checkpoint가 없어 초기화가 다르고 상대 논문 보고값과 비교함. 검증은 영상을 먼저 만들고 행동을 뒤에 만드는 cascade WAM인 LingBot-VA 하나뿐이고, 학습 시간이 Flash-WAM의 약 3배(24시간 대 8시간)이며 teacher 쌍 생성에 127 GPU 시간이 별도로 듦. 본문에 코드 공개 주소는 없음.

**누리랩 연구와의 연결**

- world model이 만든 영상을 픽셀 충실도가 아니라 그 영상이 policy 출력에 주는 영향으로 평가하는 거리(action response)를 제시함. world model 기반 test-time planning이나 failure detection에서 상상 rollout의 품질을 재는 지표로 가져다 쓸 수 있음.
- WAM 계열 policy를 실로봇에 올릴 때 행동 생성 지연을 약 4.8초에서 약 0.22초로 줄이는 증류 방법이라, 누리랩이 video 기반 VLA를 쓸 때 추론 속도 문제의 비교 기준이 됨.

*대표 그림: 같은 context에서 만든 영상 후보 v1, v2, v3를 위쪽 면(영상 특징 공간)과 아래쪽 면(induced-action 공간)에 점으로 찍은 개념도임. 영상 특징으로는 v2가 기준 v1에 더 가깝지만 행동 공간에서는 v3의 행동 a3가 a1에 더 가깝다는 어긋남을 그린 것이며, 측정 결과가 아니라 방법의 동기를 그린 그림임.*

---

### 10. When to Respond, Where to Ground: Streaming 3D Affordance Grounding (68점)

[arXiv](https://arxiv.org/abs/2611.34067) · [PDF](https://arxiv.org/pdf/2611.34067) · [alphaXiv](https://www.alphaxiv.org/abs/2611.34067)

- **저자**: Wenting Luan, Weilong Yan, Siqi Lu, Ming Li, Beibei Lin, Yongbin Zheng, Robby T. Tan
- **분야**: 3D Vision · robotics relevance 8/10 · 1차 스크리닝 68점
- **읽은 원문**: PDF 전문

> RGB-D 영상이 계속 들어오는 중에 요청을 받으면, 언제 답할지와 어느 프레임의 어느 3D 부품을 가리킬지를 grounding 모델의 patch 점수 하나로 함께 정하는 문제와 방법을 제시함. 제때 맞는 프레임으로 답했을 때만 mask IoU를 인정하는 StreamIoU가 15초 스트림에서 30.14%로, 답할 시점을 Qwen3-VL-4B에 맡긴 조합의 21.43%보다 높음.

**무슨 문제인가**

기존 3D affordance grounding(손잡이, 스위치처럼 과제 수행에 필요한 기능 부품을 3D로 찾는 일)은 장면 전체를 다 본 뒤에 답한다고 가정함. 실제 로봇은 방을 둘러보는 도중에 요청을 받고, 그 순간 목표 부품은 이미 지나갔거나 아직 안 보였을 수 있음. 너무 일찍 답하면 엉뚱한 부품을 고르고, 불필요하게 기다리면 응답이 늦어짐. streaming VLM은 답할 시점을 정하지만 출력이 텍스트뿐이고, 별도 판단 모델을 grounding 모델 앞에 붙이면 판단 모델은 실제로 mask를 만들 근거와 무관하게 시점을 정함.

**어떻게 푸나**

StreamAff는 Ground3D-LMM(Qwen3-VL-4B 기반 3D grounding 모델)을 스트림 입력으로 확장함. 각 RGB-D 프레임은 들어올 때 한 번 3D 정보가 섞인 visual token 176개로 저장됨. 요청이 오면 pointing head가 읽은 프레임들의 모든 patch와 '기다림' 선택지를 한 softmax로 함께 점수 매김. patch 확률의 합이 기다림 확률보다 크면 답하고, 가장 높은 patch가 속한 프레임을 근거 프레임으로 고름. 읽는 순서는 conditional look-back policy를 따름: 요청 시점에 현재 프레임만 먼저 보고, 기다림이 나오면 저장된 과거 프레임 전체를 한 번 훑고, 그래도 기다림이면 이후 새 프레임만 하나씩 봄. 답이 정해지면 답 문장 속 부품 구절의 hidden state로 근거 프레임의 3D 점 위에 mask를 만듦. 이때 zoom-and-refine grounding이 구절과 잘 맞는 영역을 고해상도로 다시 encoding하고, 주변 26개 voxel과 정보를 주고받아 voxel별로 mask를 보정함.

**결과**

- StreamFun3D는 저자들이 SceneFun3D 실내 RGB-D 스캔으로 만든 benchmark로, 목표가 현재·과거·미래에 보이거나 끝까지 안 보이는 네 경우로 나뉨. 지표 StreamIoU는 제때 답하고 근거 프레임이 맞을 때만 mask IoU를 인정함. 15초 스트림에서 StreamAff 30.14%, 같은 mask decoder를 쓰고 시점·프레임 결정만 Qwen3-VL-4B에 맡긴 조합은 21.43%임. 30초 스트림은 28.46% 대 19.14%임.
- 15초 스트림에서 요구 시점에 정확히 답한 비율은 76.9%로, Qwen3-VL-8B 판단기 52.9%, 4B 판단기 57.1%보다 높음. 목표가 요청 뒤에야 보이는 Future 경우의 StreamIoU는 23.30% 대 13.95%(4B)이고, 요청 시점에 바로 답하는 방식은 0%임. 반면 끝까지 안 보이는 경우 올바르게 기다린 비율은 76.5%로 8B 판단기의 79.5%보다 낮음.
- wait supervision은 프레임별 가시성 라벨로 답할 때와 기다릴 때를 가르치는 학습임. 구성 요소 제거 실험(15초)에서 이것만 더하면 StreamIoU가 14.51%에서 18.94%로, zoom-and-refine만 더하면 23.31%로 오름. 둘 다 쓰면 30.14%임. zoom-and-refine은 시점과 무관한 mIoU를 23.62%에서 36.16%로 올림.
- ScanNet++ 평가(56개 장면, 답할 수 있는 요청 220개)에서 StreamIoU는 24.17%로 기존 3D affordance grounding 방법 Fun3DU의 16.63%, 8B 판단기 15.30%보다 높음. 실험은 기록된 실내 스캔 영상 재생만이고 실로봇 실험은 없음. 본문에 코드·프로젝트 주소는 없음.

**한계**

요청 이후에는 새 프레임을 하나씩만 읽으므로, 요청 전에 본 기준 물체와 나중에 나타나는 목표 부품을 엮어야 하는 요청은 풀지 못함. 15초 스트림 앞에 프레임 60개를 붙여 75초로 늘리면 Future StreamIoU가 6.66퍼센트포인트, 올바른 기다림 비율이 14.8퍼센트포인트 내려감(각각 42개, 27개 요청). 전체 모델의 mIoU도 37.25%(15초 스트림)에 그치고, 평가 시점 라벨은 카메라 pose와 깊이로 자동 생성한 가시성 판정에 기댐.

**누리랩 연구와의 연결**

- 로봇이 탐색 중에 요청을 받아 과거 관측을 다시 꺼내 쓸지, 더 볼 때까지 기다릴지 정하는 문제로, robot memory와 active perception 연구의 평가 틀로 쓸 수 있음. 다만 카메라 궤적은 고정이라 시점을 직접 고르는 NBV로 확장하는 것은 남은 과제임.
- '기다림'을 patch 점수와 같은 softmax에 넣어 근거 없이는 답하지 못하게 한 설계는, manipulation 전 단계에서 목표 부품 grounding이 불확실할 때 실행을 미루는 failure detection 장치로 옮겨 볼 만함.

*대표 그림: 측정 결과가 아니라 StreamFun3D benchmark를 만드는 과정과 예시를 그린 그림임. 왼쪽은 3D 부품 주석을 각 프레임에 투영해 valid/absent를 붙이고, 응답 시점과 참조 답을 정한 뒤 사람이 검수하는 흐름임. 오른쪽은 Current, History, Future, Unobserved 네 경우에서 언제 기다리고 어느 프레임으로 답하는지를 보여 줌.*

---

### 11. Event-WAM: Learning to Act with Event-Derived Futures (66점)

[arXiv](https://arxiv.org/abs/2611.33917) · [PDF](https://arxiv.org/pdf/2611.33917) · [alphaXiv](https://www.alphaxiv.org/abs/2611.33917)

- **저자**: Jongseong Bae, Hyunwoo Kim, Yeongin Lee, Eubin So, Ha Young Kim
- **분야**: World Model · robotics relevance 9/10 · 1차 스크리닝 66점
- **읽은 원문**: PDF 전문

> RGB 시연 영상에서 합성한 event(픽셀 밝기 변화) 프레임을 world action model의 미래 예측 목표로 RGB와 함께 학습시킴. 실제 SO-101 로봇 4개 과제의 평균 성공률이 RGB만 쓰는 Simple-WAM의 65.5%에서 79.0%로 오름.

**무슨 문제인가**

WAM(World Action Model)은 미래 영상 예측을 함께 학습해 로봇 action 생성을 돕는 모델임. 최근 Simple-WAM처럼 추론 때 미래 영상을 만들지 않고 학습 때만 미래 예측을 쓰는 방식이 나오면서, 무엇을 미래 목표로 삼아야 action 학습에 도움이 되는지가 질문이 됨. RGB 미래 예측은 바뀌지 않는 배경까지 촘촘히 맞춰야 해서 움직임과 변화를 따로 강조하지 않음. event camera 신호는 변화만 남기지만, 기존 로봇 연구는 event를 추론 때 입력으로 써서 event camera가 필요했음.

**어떻게 푸나**

Event-WAM은 Simple-WAM 위에 event 기반 미래 목표를 더한 모델임. 먼저 RGB 시연 영상을 v2e(영상을 event stream으로 바꾸는 simulator)로 변환하고, 미래 구간을 시간 bin으로 나눠 픽셀마다 ON과 OFF event 개수를 셈. 이 개수에 log를 씌워 ON, OFF, 합의 3채널 pseudo-RGB 프레임으로 만들고, 고정된 Wan2.2 RGB video VAE로 그대로 인코딩함. 그래서 event 전용 encoder를 따로 학습하지 않음. video DiT는 RGB 미래 latent와 event 미래 latent를 채널 방향으로 이어 붙인 입력을 받고, 둘 각각에 flow matching loss를 줌. action DiT는 video DiT의 key/value를 받아 32-step action chunk를 denoising함. 추론 때는 미래 RGB와 event 자리를 순수 noise로 채워 video DiT를 한 번만 통과시키므로 event camera도, 미래 영상 생성도 필요 없음.

**결과**

- 실제 SO-101 팔로 과제 4개(펜을 컵에 넣기, 인형 3개 모으기, 서랍 열기, 큐브 쌓기)를 과제당 시연 100개로 학습함. 표준 조건 평균 성공률이 Simple-WAM 65.5%에서 79.0%로 오름(방법당 200회). 서랍 열기는 48.0%에서 74.0%로 오름.
- 같은 실로봇에서 학습 때 없던 교란 4종(카메라 위치, 배경, 센서 noise, 방해 물체)을 줌. 평균 성공률이 26.9%에서 45.0%로 오름(방법당 160회). 표준 조건과 교란 조건의 전체 평균 차이는 둘 다 Fisher exact test에서 p<0.01임. 평가는 blind가 아님.
- LIBERO-Plus(LIBERO 조작 과제에 카메라·조명·배경 등 교란을 건 강건성 평가 모음)의 지시문 수정 버전에서 평균 성공률이 84.0%에서 85.9%로 오름. 원래 LIBERO(조작 과제 40개) 성공률은 Event-WAM 98.8%, Simple-WAM 98.9%로 같은 수준임. RGB 미래 loss를 빼고 event loss만 쓴 경우도 85.8%임.
- 시뮬레이션 이득은 benchmark에 따라 다름. RoboTwin 2.0(양팔 조작 과제 50개)의 깨끗한 환경 학습, 무작위 환경 평가에서는 2.7%에서 1.9%로 내림. 교란 7종을 건 RoboTwin 2.0-Plus에서는 평균 43.6%에서 46.1%로 오름.

**한계**

event는 실제 event camera가 아니라 RGB에서 합성한 것이고, bin 안의 세밀한 시간 순서는 버림. 시뮬레이션 이득은 많아야 2.5퍼센트포인트이고, seed 반복이나 신뢰구간은 본문에서 확인 불가함. 그래서 RGB 프레임 차이를 미래 목표로 쓴 변형(RGB-Diff, LIBERO-Plus 85.2%)과의 차이는 가르기 어려움. 실로봇은 SO-101 팔 한 대의 과제 4개뿐이고, 코드 공개 주소는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- WAM에서 미래 예측 정확도가 아니라 어떤 미래 목표를 주느냐가 policy 강건성을 바꾼다는 결과임. Event 목표에서 미래 예측 PSNR은 RGB-only와 같지만 성공률은 오름. world model을 VLA 보조 학습 신호로 쓰는 연구에서 목표 설계 비교 대상으로 쓸 수 있음.
- 센서 noise에서 미래 key/value를 깨끗한 값으로 바꾸면 Simple-WAM 성공률이 33%에서 92%로 오른다는 분석이 있음. 교란 아래 실패의 원인을 내부 feature 단위로 찾는 failure diagnosis 방법으로 참고할 만함.

*대표 그림: 측정 결과가 아니라 Event-WAM의 구조를 그린 개념도임. 현재 RGB, 언어, proprioception(관절 상태) 입력과 함께 미래 RGB와 미래 event를 고정 VAE로 인코딩해 video DiT에 넣고, 그 K/V로 action DiT가 action chunk를 만드는 흐름을 보여 줌. 미래 RGB·event 경로는 학습 때만 쓰는 점선으로 표시됨.*

---

### 12. A Failure-Driven Data Flywheel for Post-Training Vision-Language-Action Models (63점)

[arXiv](https://arxiv.org/abs/2611.34698) · [PDF](https://arxiv.org/pdf/2611.34698) · [alphaXiv](https://www.alphaxiv.org/abs/2611.34698)

- **저자**: Yuhao Luo, Zihao Sheng, Zilin Huang, Zhengyang Wan, Boyue Wang, Ruolin Yang, Shuai Wang, Sikai Chen
- **분야**: VLA · robotics relevance 10/10 · 1차 스크리닝 75점
- **읽은 원문**: PDF 전문

> 주행 VLA가 실패하는 조건을 3DGS로 복원한 실제 장면에 보행자·표지판을 넣어 만들고, 실패율이 높은 조건에 데이터를 더 배정하는 반복 post-training을 제안함. 가려진 보행자 돌출 시험 세트의 충돌 없는 비율이 ReCogDrive에서 0.390에서 0.765로 오름.

**무슨 문제인가**

공개된 pretrained VLA를 자기 플랫폼에 맞춰 쓰는 팀은 모델이 특정 행동 요구사항을 못 지키는 경우를 자주 만남. 기존의 실패 기반 데이터 수집 방법은 이미 가진 주행 로그나 그 로그 위의 policy 행동에서 실패를 찾음. 그래서 필요한 사건이 로그에 아예 없으면 실패가 드러나지 않고, 대규모 차량 fleet가 없는 팀은 데이터를 모을 방법이 없음. 또 성공률 같은 집계 지표는 어떤 세부 행동이 부족한지 가리고, 학습이 진행되면 실패 양상도 바뀜.

**어떻게 푸나**

목표 능력을 장면 template, 장면 parameter 공간, 시범을 주는 expert, 행동별 metric 묶음으로 정의함. nuScenes 로그를 OmniRe(3D Gaussian Splatting 기반 동적 도시 장면 복원)로 복원하고, 가리는 차량과 그 뒤에서 튀어나오는 보행자 같은 3D asset을 넣어 로그에 없던 target 장면을 만듦. 난이도는 보행자가 처음 보일 때의 TTC(time to collision)로 정하고, 보행자만 뺀 paired control 장면을 함께 만듦. rule-based expert가 두 장면에서 궤적을 만들고, 그 궤적을 따라 렌더링한 카메라 관측과 이후 waypoint를 지도 학습 쌍으로 씀. 생성 데이터는 원래 nuScenes 데이터와 섞어 학습하고, 매 round 개발 세트에서 감속·제동·정지 유지·재출발·불필요 제동을 따로 평가해 제약을 만족하는 checkpoint를 고름. TTC 구간별 실패율로 failure map을 갱신하고, 다음 round의 생성 할당량을 실패율에 비례해 나눔. post-training 대상은 주행 VLA인 AutoVLA(Qwen2.5-VL-3B 기반)와 ReCogDrive(고정된 InternVL3-2B에 diffusion planner를 붙인 모델)임.

**결과**

- 가려진 보행자 돌출 과제의 open-loop 결과임. 주 지표는 가려진 곳에 다가가 보행자가 나타나고 제동하기까지의 구간(critical phase)에서 충돌하지 않은 비율임. 시험 세트(학습·선택에 쓰지 않은 nuScenes 장면 20개, target 200개)에서 이 비율이 5 round 뒤 AutoVLA 0.261에서 0.579로, ReCogDrive 0.390에서 0.765로 오름. paired control의 불필요 제동 비율은 최대 0.013임. 향상은 주로 가려진 곳에 닿기 전 미리 감속하는 행동에서 나옴. 보행자가 나온 뒤의 추가 제동 지표는 ReCogDrive 기준 0.045에서 0.185로 올랐지만 여전히 낮음.
- 같은 누적 학습 step(100k)에서 ReCogDrive를 비교함. 매 round failure map을 갱신하는 방식이 0.751로, 균등 할당과 무작위 할당(둘 다 0.691)보다 0.060 높음. 첫 round map을 고정한 방식은 0.723임. 다만 이 ablation 수치는 한 번 실행 결과이고 seed 반복은 본문에서 확인 불가함.
- paired control 샘플을 빼면 충돌 없는 비율이 0.751에서 0.944로 오름. 그러나 control 장면 진행률이 0.669에서 0.224로 내려가, policy가 보행자 유무와 상관없이 제동하도록 학습된 것으로 보임. 세부 행동 평가가 없으면 이런 policy를 개선으로 오인함을 보인 결과임.
- 실차(Ford E-Transit, 주차장, 어린이 크기 보행자 더미) closed-loop에서 추가 실제 학습 없이 ReCogDrive를 배치함. 안전 통과가 base 1/5회에서 open-loop post-training 후 4/5회로 늘었음. 렌더링한 복원 장면 안에서 closed-loop로 2 round post-training한 checkpoint는 실차에서 2/5회에 그침.

**한계**

실험은 자율주행 두 시나리오(가려진 보행자, 정지 표지판 교차로)와 rule-based expert에 한정되고, 로봇 조작 적용은 문제 정의 수준의 언급뿐임. 실차 평가는 한 모델, 한 장면, 조건당 5회라 통계적 근거가 약함. 보행자 과제를 배운 checkpoint에서 정지 표지판 과제를 이어 배우면, 정지선 앞 정지 비율이 base에서 바로 배운 경우보다 낮음(ReCogDrive 0.358 대 0.667). 코드·데이터 공개 여부는 본문에서 확인 불가함.

**누리랩 연구와의 연결**

- 실패율 map으로 다음 데이터 생성량을 정하는 루프는 manipulation VLA의 failure detection과 targeted data collection에 그대로 옮겨 볼 수 있는 구조임. 3DGS로 복원한 장면에 물체를 넣어 실패 조건을 만드는 방식은 object-centric 3DGS 기반 데이터 증강과 이어짐.
- paired control 없이는 지나치게 보수적인 policy가 지표상 좋아 보인다는 결과는, 로봇 policy의 failure recovery 평가를 설계할 때 대조 장면을 함께 두어야 하는 근거가 됨.

*대표 그림: 측정 결과가 아니라 방법 구조를 그린 개념도임. 복원한 장면에 차량·보행자 asset을 넣어 target 장면과 paired control 장면을 만드는 단계부터 그림. 이어서 expert 궤적으로 만든 데이터를 원래 데이터와 섞어 학습하고, 개발 세트의 failure map이 다음 round 생성 할당량으로 돌아가는 흐름을 보여 줌.*

---

### 13. Loop4D: Embodied World Modeling with 4D VAEs and Looped Diffusion Transformers (62점)

[arXiv](https://arxiv.org/abs/2611.34199) · [PDF](https://arxiv.org/pdf/2611.34199) · [alphaXiv](https://www.alphaxiv.org/abs/2611.34199)

- **저자**: Gen Li, Fan Luo, Mengjun Lin, Shu Han, Bohan Li, Hao Zhao
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 78점
- **읽은 원문**: PDF 전문

> 로봇 조작 장면의 미래 RGB 영상과 3D 좌표 지도(pointmap)를 함께 생성하는 4D world model로, 로봇 팔 움직임을 보존하는 VAE와 중간 Transformer 층을 반복 적용하는 diffusion 구조를 결합함. 1.3B 모델의 시뮬레이션 과제 생성 영상 품질(gFVD)이 449.33으로, 같은 data로 fine-tuning한 Wan2.1-14B의 574.92보다 좋음.

**무슨 문제인가**

로봇 조작 결과를 미리 보려면 world model이 겉모습과 3D 형상 변화를 함께 예측해야 함. 범용 video VAE는 시공간 압축 과정에서 빠르게 움직이는 로봇 팔 주변에 artifact를 만들고, RGB 복원 loss만으로는 metric 형상을 직접 학습하지 않음. RGB와 형상을 함께 예측하려면 생성 용량이 커야 하는데, 기존 4D 생성 모델은 14B급 큰 backbone에 기대는 경우가 많음. 그래서 저자들은 parameter 수를 늘리지 않고 계산을 더 써서 품질을 올리는 길을 찾음.

**어떻게 푸나**

Loop4D는 첫 RGB-D 관측과 텍스트 지시를 받아 미래 RGB frame과 카메라 좌표계 XYZ 지도 영상을 출력함. RGB VAE는 전체 clip 복원과 함께, 앞부분 frame의 latent 뒤에 0을 붙여 뒷부분 frame을 맞히는 predictive reconstruction을 확률적으로 섞어 학습함. 여기에 정답 depth와 camera calibration으로 한 시점의 복원 영상을 다른 시점으로 warp해, 두 시점 모두에서 보이는 로봇 픽셀의 RGB 오차를 줄이는 loss를 더함. 형상용 geometry VAE는 학습된 RGB VAE의 encoder와 decoder를 고정하고, latent에 더하는 작은 residual adapter만 학습함. 두 VAE를 고정한 뒤 학습하는 Dual-Stream Looped Diffusion Transformer(LoopDiT)는 RGB와 XYZ의 hidden state를 따로 두되 가중치는 공유하고, 층마다 RGB 특징을 XYZ 쪽에 선형으로 더함. 한 번의 denoising 호출 안에서 중간 층 묶음을 R번 반복하며, 반복마다 예측을 supervise하고 로봇 영역 오차가 이전 반복보다 커지면 penalty를 주고, 작은 gate network가 RGB와 XYZ 각각의 갱신 크기를 0~1 사이로 정함.

**결과**

- Robot4DGen dataset(시뮬레이션 3개, 실제 4개 조작 과제의 multi-view RGB-D 시연 모음)에서 미래 영상을 생성함. 시뮬레이션 과제 gFVD(생성 영상과 실제 영상 분포의 거리, 낮을수록 좋음)는 Loop4D-1.3B 449.33, Wan2.1-14B 574.92, LTX-2.3 22B 502.82임. 실제 과제에서는 Wan2.1-14B가 668.84로 Loop4D-1.3B(738.77)와 5B(721.24)보다 좋음. 비교한 video 모델들은 RGB만 생성함.
- 형상 정확도인 depth AbsRel(depth 상대 오차, 낮을수록 좋음)은 시뮬레이션 과제에서 Loop4D-5B 0.0483, dataset과 같은 논문에서 나온 4D 생성 모델 Robot4DGen 0.1131임. 실제 과제에서는 0.0831 대 0.1473임.
- 반복 ablation 표(5B 모델)에서 중간 층을 2번 반복하면 gFVD가 618.03에서 511.16으로 내림. 이 표의 시뮬레이션·실제 과제 구분은 본문에서 확인 불가함. 대신 sample당 학습 계산량은 111.59에서 184.96 TFLOPs로, 50-step 추론 시간은 영상당 21.84초에서 29.40초로 늘어남. 로봇 영역 제약과 gate 없이 그냥 반복하면 581.69이고, 반복을 3회 이상으로 늘려도 일관된 개선은 없음.
- 생성 영상에서 궤적을 복원해 실행하는 Robot4DGen의 평가 절차를 따른 시뮬레이션 과제 3개, 과제당 10회 시행에서 평균 성공률은 Loop4D 33.3%, Robot4DGen 16.7%, Diffusion Policy 10.0%임. 30회 중 각각 10회, 5회, 3회 성공한 셈임.

**한계**

로봇 실행 평가는 시뮬레이션 과제 3개에 과제당 10회뿐이고 성공률도 낮아, 차이의 통계적 신뢰도가 약함. 실제 로봇 data는 영상 생성 지표로만 평가했고, Loop4D VAE의 RGB rFVD(복원 영상 분포 거리)는 22.77로, fine-tuning 전 사전학습 RGB VAE의 13.29보다 나빠짐. 실험은 Robot4DGen dataset 하나에서만 했고, 코드 공개 주소는 본문에 없음.

**누리랩 연구와의 연결**

- 예측 출력이 RGB와 metric pointmap 쌍이므로, 예측 형상과 실제 관측을 3D에서 비교해 조작 실패를 찾는 failure detection 연구의 world model로 쓸 수 있음.
- denoising step을 늘리는 대신 내부 층 반복으로 계산을 더 쓰는 구조라, world model 기반 test-time planning에서 계산 예산을 어디에 쓸지 정할 때 비교 대상이 됨. 같은 계산량에서 2회 반복이 step 증가보다 낫다는 결과는 그림으로만 제시됨.

*대표 그림: 측정 결과가 아니라 4D VAE 학습 구조를 그린 그림임(논문 Figure 2). 위는 전체 clip 복원과 0을 붙여 다음 frame을 맞히는 RGB VAE임. 가운데는 정답 XYZ와 calibration으로 시점 A 복원을 시점 B로 warp해 로봇 픽셀의 RGB 오차 loss(L_Geo)를 거는 과정이고, 아래는 고정된 RGB encoder·decoder에 학습하는 adapter만 더한 geometry VAE임.*

---

### 14. Best-of-$N$ Test-Time Steering Can Lead to Reward Hacking in Vision-Language-Action Models (60점)

[arXiv](https://arxiv.org/abs/2611.33398) · [PDF](https://arxiv.org/pdf/2611.33398) · [alphaXiv](https://www.alphaxiv.org/abs/2611.33398)

- **저자**: Vanshaj Khattar, Jing Liu, Toshiaki Koike-Akino, Ming Jin, Ye Wang
- **분야**: VLA · robotics relevance 8/10 · 1차 스크리닝 68점
- **학회**: NeurIPS 2026 (comments 표기) · 근거: comments에 "17 pages, 11 figures, to be presented at 1st Workshop on Physical World AI at NeurIPS 2026"
- **읽은 원문**: PDF 전문

> 고정된 π0.5에서 행동 후보 N개를 뽑고 verifier로 하나를 고르는 best-of-N steering에서, verifier에 오차가 있으면 N을 늘릴수록 verifier 점수만 오르고 실제 품질은 따라오지 않음을 시뮬레이션에서 보임. 프라이팬 놓기 과제에서 N을 5에서 75로 늘리자 예측 reward는 0.119에서 0.196으로 올랐고, 오차 없는 시뮬레이터로 다시 잰 reward(clean reward)는 0.0036에서 -0.0014로 내림.

**무슨 문제인가**

RoboMonkey, VERITAS 같은 best-of-N test-time steering은 VLA를 다시 학습하지 않고 행동 후보 여러 개 중 verifier가 가장 높게 매긴 것을 실행함. 이 방식의 이득은 verifier가 후보 순위를 얼마나 정확히 매기느냐에 달려 있음. LLM에서는 불완전한 reward model로 고르면 N이 커질수록 실제 품질이 오르다가 내리는 현상이 알려져 있고, 이를 inference-time reward hacking이라 부름. 로봇에서 verifier 오차가 safety 위반과 과제 완료에 어떻게 이어지는지는 오차를 통제한 조건에서 잰 적이 없었음.

**어떻게 푸나**

LIBERO-Safety(안전 제약을 지키며 조작하는 시뮬레이션 benchmark)로 fine-tuning된 공개 π0.5 checkpoint를 고정하고, 재계획 시점마다 action chunk 후보 N개를 뽑음. verifier는 MuJoCo 시뮬레이터로 각 후보를 5 control step 굴린 예측 rollout을 만듦. 이 rollout에서 safety 점수(제약 위반 횟수에 비례한 감점)와 task-progress 점수(물체 접근·잡기·들기·목표로 옮기기의 dense 항, sparse reward, 성공 보너스의 합)를 계산함. 두 점수를 0.5씩 더한 proxy reward가 가장 높은 후보를 5 step 실행하고 다시 뽑음. policy와 실행 환경은 그대로 두고 verifier 안에만 오차를 넣음. 첫째 오차는 예측 물체 위치에 표준편차 0.1m Gaussian noise를 더하는 output noise임. 나머지 둘은 actuator 세기·감쇠·마찰·물체 질량을 바꿔 팔이 약하게 또는 강하게 반응하게 하는 under-responsive·over-responsive dynamics임. 선택된 행동을 오차 없는 시뮬레이터로 다시 채점한 값을 clean reward라 부르고, N이 커질 때 proxy reward만 오르고 clean reward나 episode 결과가 따라오지 않으면 reward hacking으로 판정함. 완화책으로 점수에 softmax를 씌워 확률적으로 고르는 soft best-of-N과, clean reward 기대값이 최대가 되게 safety·task 가중치를 맞추는 shared-weight calibration을 시험함.

**결과**

- LIBERO-Safety(물체 잡는 방식 제약과 장애물·사람 손 회피 제약을 지키며 조작하는 시뮬레이션 benchmark)의 60개 과제-난이도 조합 전체를 봄. N을 1에서 75로 늘릴 때 안전 완료율(과제 완료와 무위반을 함께 만족한 episode 비율)은 perfect verifier에서 43.8%에서 49.8%로, 오차 있는 verifier에서 43.8%에서 47.0%로 오름. 위반율은 각각 10.3%에서 4.5%, 10.3%에서 9.1%로 내림. 평균으로는 성능이 내려가지 않고 이득이 줄어드는 정도임.
- 성능이 실제로 내려간 사례는 저자가 결과를 보고 고른 그룹에서 나옴. over-responsive dynamics에서 사람 안전(human safety) 과제 중 난이도 3단계(L0~L2)의 L2 과제 5개를 봄(N 값마다 50 episode). 안전 완료율이 N=30의 82%에서 N=75의 70%로 내리고, 위반율은 10%에서 18%로 오름. 저자도 이 그룹들이 사후 선택이라 독립적 확인이 아니라고 밝힘.
- 원인 분석은 난이도 L0~L1인 40개 조합에서 함. output noise에서 verifier가 안전하다고 예측했지만 실제로 위반한 선택이 N=5의 95회에서 N=75의 161회로 늘어남. dynamics 오차에서도 같은 수가 under-responsive에서 17회에서 50회로, over-responsive에서 16회에서 42회로 늘어남. 예측 위반을 걸러내는 safety-first 규칙으로는 이런 선택을 막을 수 없음.
- N=75에서 soft best-of-N(β=16, β가 클수록 hard max에 가까워짐)은 under-responsive dynamics의 안전 완료율을 hard max의 48.7%에서 53.0%로 올림. output noise에서는 44.5%에서 45.8%로 차이가 작음. calibration은 held-out 57개 조합에서 over-responsive는 52.3%에서 53.9%로 조금 오르고, under-responsive는 54.2%에서 48.8%로 오히려 내림.

**한계**

모든 실험이 시뮬레이션이고 실로봇 실험은 없으며, policy도 π0.5 하나뿐임. verifier 오차는 MuJoCo 파라미터와 위치 noise로 인위적으로 넣은 것이라, 실제로 쓰이는 학습된 verifier의 오차 구조와 같다는 근거는 없음. 60개 조합 평균에서는 N을 늘려도 안전 완료율이 내려가지 않았고, 뚜렷한 역전은 사후에 고른 10~50 episode 규모 그룹에서만 보임. 코드 공개 주소는 본문에 없음.

**누리랩 연구와의 연결**

- test-time optimization 연구에서 후보 샘플링과 verifier 선택을 쓸 때, N을 키우며 proxy 점수와 정답 점수의 차이를 함께 재는 진단 절차로 가져다 쓸 수 있음. world model을 verifier로 쓰면 그 world model의 오차가 같은 방식으로 선택에 이용될 수 있다는 근거가 됨.
- failure detection 관점에서, verifier가 안전하다고 했지만 실제로 위반한 선택(missed unsafe choice)을 따로 세는 방식은 detector가 놓친 실패를 측정하는 지표로 쓸 수 있음.

*대표 그림: 측정 결과 그림임. 위 줄은 사람이 든 접시에 사과를 놓는 과제(예측 위치에 0.1m noise), 아래 줄은 책을 caddy에 넣는 과제(over-responsive dynamics)에서 후보 수 N에 따른 값을 그림. 오차 있는 verifier가 고른 행동은 예측 reward가 N과 함께 오르지만 clean reward는 오르지 않고, 큰 N에서 안전 완료율은 perfect verifier보다 낮아지며 위반율은 오름.*

---

### 15. WhatIf: Counterfactual World Models over Action-Grounded Causal Graphs for Robotic Manipulation (46점)

[arXiv](https://arxiv.org/abs/2611.33745) · [PDF](https://arxiv.org/pdf/2611.33745) · [alphaXiv](https://www.alphaxiv.org/abs/2611.33745)

- **저자**: Xu Yang, Kailai Sun, Qianchuan Zhao
- **분야**: World Model · robotics relevance 10/10 · 1차 스크리닝 72점
- **읽은 원문**: PDF 전문

> 후보 행동들의 미래를 하나의 공유된 물리 상황 아래에서 함께 굴려 보는 counterfactual world model(WhatIf)을 제안함. 이 위에서 같은 상황 안의 기대 이득과 계획 변경이 해가 될 확률을 함께 보고 계획을 고르는 planner(CAP)도 제안함. 다만 실험 결과는 하나도 없고 실험 계획만 적혀 있음.

**무슨 문제인가**

기존 world model은 실제로 실행한 행동의 전이만으로 학습하므로, 행동마다 미래의 주변 분포(marginal)만 따로 표현함. 그런데 로봇의 결정은 같은 물리 상황에서 다른 행동을 했으면 더 나았을지를 비교하는 일임. 행동마다 따로 예측하면 행동 차이와 상황(질량, 마찰, 잡음) 차이가 섞여 비교가 흔들림. 기존 causal world model은 고정된 latent DAG나 전역 context 벡터를 써서, 물체 수가 바뀌거나 행동이 새 접촉을 만드는 경우를 표현하기 어렵다고 저자는 지적함.

**어떻게 푸나**

WhatIf는 과거 관측과 행동 기록에서 계층형 latent physics(장면, 물체별 질량·관성, 물체 쌍별 마찰·compliance)와 전이 잡음을 추론함(abduction). 후보 행동마다 물체 노드 위에 sparse graph를 새로 만들며, gate가 어떤 경로가 켜지는지를, weight가 그 경로의 부호 있는 세기를 정함. 이 그래프는 물체 단위에서 상태 factor 단위로 한 번 더 나뉘고, 물체 type별로 공유된 함수로 만들어져 물체 수가 달라도 쓸 수 있음. 모든 후보 행동은 같은 물리 상황 하나를 공유한 채 각자의 그래프로 rollout되며, 반사실 예측은 실제 관측된 다음 상태에 행동 간 차이를 더하는 방식으로 고정함(anchoring). counterfactual 정답 없이 학습하려고, 다른 행동의 반사실에서 상황을 다시 추론해 실제 결과가 복원되게 하는 round-trip loss를 둠. CAP(Counterfactual Advantage Planning)는 샘플 기반 궤적 최적화기(CEM, MPPI) 안에서 현재 계획 대비 이득을 같은 상황 표본들로 짝지어 추정하고, 해가 될 확률이 ε를 넘는 계획 변경은 거부함. 실행 뒤에는 사후 최적 행동과 regret을 계산해 재시도 계획, 물리 posterior, critic 없는 advantage-weighted regression policy 학습에 씀.

**결과**

- 4절은 CausalWorld(질량·크기 등을 제어해 바꿀 수 있는 시뮬레이션 조작 benchmark)와 Meta-World·ManiSkill 계열 환경에서 simulator를 복제해 짝지은 반사실을 만드는 평가 계획만 적음. 수치, 표, 그림 결과는 본문에서 확인 불가임.
- 이론 결과 하나: 실제 행동 데이터는 행동별 주변 분포와 평균 효과만 정하고, 개별 효과와 해가 될 확률은 정하지 못함을 두 모델 반례로 보임. 평균 효과로 anchoring하면 오차가 개별 효과의 조건부 분산과 같아짐.
- 이론 결과 둘: 두 계획을 같은 상황 표본으로 비교하면 독립 표본보다 추정 분산이 1−ρ배로 줄어듦(ρ는 두 계획 return의 상관, 두 분산이 같을 때). 행동과 무관한 모델 오차는 비교에서 상쇄됨.
- 관측 전이가 개입 전이와 같아지는 조건(숨은 행동 confounding 없음, positivity 등)을 backdoor 논증으로 정리함. 세 결과 모두 표준 인과추론 도구를 이 설정에 옮긴 것임.

**한계**

모델이 실제로 학습되는지, 반사실 정확도나 제어 성공률이 오르는지는 전혀 보이지 않았고 결론도 이를 검증할 연구 질문으로 남김. 시뮬레이션·실로봇 실험 모두 없고 코드 공개 언급도 없음. 짝지은 반사실 감독은 simulator 복제와 같은 random seed를 전제로 하므로 실로봇에서는 round-trip loss만 남는데, 이것만으로 coupling이 맞게 잡히는지는 보이지 않음.

**누리랩 연구와의 연결**

- counterfactual reasoning과 failure diagnosis에 바로 닿는 설계임. 사후 regret으로 행동 선택 때문에 생긴 실패와 어떤 행동으로도 못 피한 실패를 가르는 기준은 failure detection·recovery 연구의 정의로 가져다 쓸 만함.
- 같은 상황 표본으로 짝지어 후보를 비교하는 방식은 world model 기반 test-time planning에서 rollout 수를 줄이는 장치로 바로 실험해 볼 수 있음. 다만 논문 자체는 실험이 없어 근거로 인용하기 어려움.

---

## 오늘의 흐름

- **world action model의 미래 표현 바꾸기**: world action model(WAM)은 미래 장면을 예측한 뒤 그것을 바탕으로 행동을 만드는 모델임. 행동 전에 상상하는 미래를 전체 영상 대신 다른 형태로 바꾼 논문이 넷임. 움직이는 부분만 담은 소수의 token, 3D Gaussian으로 나타낸 장면 상태, RGB에서 합성한 event(픽셀 밝기 변화) 프레임이 각각 제안됨. 여러 단계 teacher WAM을 1단계 생성기로 줄이면서 영상이 만드는 행동까지 맞추는 증류도 나옴. [Dynamic Forcing](https://arxiv.org/abs/2611.33799), [SplatWAM](https://arxiv.org/abs/2611.33467), [Event-WAM](https://arxiv.org/abs/2611.33917), [DriftWAM](https://arxiv.org/abs/2611.33797)
- **world model이 실패와 물리량을 담는지 점검**: 영상 world model이 접촉력의 크기를 거의 담지 못하고, 성공 시연 위주로 배우면 잡기 실패 장면을 못 그린다는 결과가 함께 나옴. 큰 video prior를 행동 조건 world model로 바꾼 연구도 팔 동작은 맞히지만 물체 상태 오차가 남음. RGB와 3D 좌표 지도를 함께 생성하는 Loop4D도 실제 로봇 data에서는 영상 지표로만 평가됨. [Can Visual World Models See Force?](https://arxiv.org/abs/2611.34422), [Beyond the Happy Path](https://arxiv.org/abs/2611.33925), [Most of the Way There](https://arxiv.org/abs/2611.34435), [Loop4D](https://arxiv.org/abs/2611.34199)
- **판정자와 verifier를 믿어도 되는지**: policy 개선 루프에서 새 policy를 남길지 정하는 judge, best-of-N에서 후보를 고르는 verifier, 실패 원인을 적는 코딩 agent의 오판을 각각 측정함. 실패율이 높은 조건에 학습 데이터를 더 배정하는 주행 VLA 연구도 실패 판정에 기대는 루프임. [Keep or Roll Back?](https://arxiv.org/abs/2611.33794)은 학습에 쓰는 판정과 채택을 정하는 판정을 나눠야 한다고 결론냄. [Best-of-N Test-Time Steering](https://arxiv.org/abs/2611.33398), [Skeptic](https://arxiv.org/abs/2611.33560), [Failure-Driven Data Flywheel](https://arxiv.org/abs/2611.34698)
- **기억을 써서 먼 목표와 늦게 오는 정보를 다루기**: 학습 데이터의 frame graph를 subgoal 기억으로 써서 frozen world model의 장기 planning 성공률을 올린 연구가 있음. 영상이 들어오는 중에 받은 요청에 언제 답할지를 정하는 streaming affordance grounding도 같은 흐름임. 같은 물리 상황에서 후보 행동의 미래를 함께 굴려 계획을 고르는 WhatIf는 실험 없이 설계만 제시함. [Graph Anchors](https://arxiv.org/abs/2611.34509), [Streaming 3D Affordance Grounding](https://arxiv.org/abs/2611.34067), [WhatIf](https://arxiv.org/abs/2611.33745)

## 해볼 만한 연구

### 학습된 world model을 verifier로 쓸 때의 reward hacking
- 질문: best-of-N 선택의 verifier를 학습된 world model로 바꾸면, N을 늘릴수록 world model의 오차를 이용하는 후보가 뽑히는지 밝힘.
- 첫 실험: LIBERO(시뮬레이션 조작 과제 모음)에서 VLA 후보 행동 N개를 world model rollout으로 점수 매겨 고름. N을 1에서 64까지 늘리며 world model 점수와 시뮬레이터 실제 성공률의 차이를 재고, 실패 데이터로 post-training한 world model과 원래 world model을 비교함.
- 가장 가까운 연구: [Best-of-N Test-Time Steering](https://arxiv.org/abs/2611.33398)은 verifier 오차를 MuJoCo 파라미터로 인위적으로 넣었음. 이 연구는 실제 학습된 world model의 오차 구조를 대상으로 함.

### 실패 데이터로 고친 world model이 failure detection에 주는 이득
- 질문: 실패 궤적으로 post-training한 world model이 영상 지표뿐 아니라 VLA rollout의 실패 예측 정확도도 올리는지 밝힘.
- 첫 실험: 같은 VLA rollout 묶음에 대해 post-training 전후 world model의 예측 장면과 실제 관측 차이로 실패를 예측하고, AUROC와 실패 발생 전 경고 시점을 비교함.
- 가장 가까운 연구: [Beyond the Happy Path](https://arxiv.org/abs/2611.33925)는 물체 궤적 오차와 PSNR만 쟀고 policy 평가나 failure detection에 쓰지 않았음.

### 측정 기반 실행 로그를 sealed judge로 쓰는 실로봇 개선 루프
- 질문: 시뮬레이터 success predicate가 없는 실로봇에서, 센서로 잰 실행 로그를 policy를 고치는 쪽(improver)이 볼 수 없는 판정자(sealed judge)로 쓰면 keep/roll back 판정의 오채택이 줄어드는지 밝힘.
- 첫 실험: 실로봇 조작 과제 3개에서 VLA를 5세대까지 fine-tuning함. 세대마다 VLM judge 단독 판정과, 측정 로그로 표본을 하나씩 더하며 채택 여부를 검정하는 sequential test 판정의 false-positive rate를 사람 라벨과 비교함.
- 가장 가까운 연구: [Keep or Roll Back?](https://arxiv.org/abs/2611.33794)은 조작 실험의 sealed judge가 시뮬레이터 predicate였음. [Skeptic](https://arxiv.org/abs/2611.33560)이 실패 원인을 적을 때 근거로 쓰는 센서 측정 로그를 그 자리에 넣는 것이 차이임.

## 꼭 읽을 논문

- [SplatWAM](https://arxiv.org/abs/2611.33467): action 조건으로 3D Gaussian 상태를 예측해 임의 시점 렌더링이 되는 world model이라 active perception과 object-centric 3DGS 연구의 비교 대상임.
- [Keep or Roll Back?](https://arxiv.org/abs/2611.33794): VLA self-improvement에서 judge 오판을 세대별로 재는 절차와, 표본을 하나씩 더하며 채택을 검정하는 sequential test를 함께 제시함.
- [Graph Anchors](https://arxiv.org/abs/2611.34509): goal cost(현재 상태가 목표에서 얼마나 먼지 매기는 값)가 어디서 틀리는지 planner 없이 offline으로 진단함. 추가 학습 없이 PointMaze-Medium 200 step 목표의 성공률을 13%에서 85%로 올림.
- [Beyond the Happy Path](https://arxiv.org/abs/2611.33925): world model 학습 데이터에 실패를 넣어야 하는 이유를, 같은 장면에서 행동만 바꾼 쌍의 미래 차이를 재는 지표와 수치로 보임.
- [Can Visual World Models See Force?](https://arxiv.org/abs/2611.34422): world model과 VLA feature에 힘 정보가 있는지 재는 probe 절차를 그대로 가져다 쓸 수 있음.

---

<details>
<summary><strong>전체 1차 스크리닝 결과 (625편, 점수순)</strong></summary>

<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>
<tr><td>1</td><td><a href='https://arxiv.org/abs/2611.34199'>Loop4D: Embodied World Modeling with 4D VAEs and Looped Diffusion Transformers</a></td><td>78</td><td>10</td><td>World Model</td><td>4D VAE와 looped DiT로 조작 결과의 RGB와 3D 기하를 예측하는 embodied world model로 강한 관련성임</td></tr>
<tr><td>2</td><td><a href='https://arxiv.org/abs/2611.34422'>Can Visual World Models See Force?</a></td><td>78</td><td>10</td><td>World Model</td><td>visual world model이 힘을 인식하는지 묻는 진단으로 manipulation world model의 근본 한계를 다룸</td></tr>
<tr><td>3</td><td><a href='https://arxiv.org/abs/2611.34698'>A Failure-Driven Data Flywheel for Post-Training Vision-Language-Action Models</a></td><td>75</td><td>10</td><td>VLA</td><td>실패 기반 data flywheel로 VLA post-training, failure recovery·VLA 직접 해당함</td></tr>
<tr><td>4</td><td><a href='https://arxiv.org/abs/2611.33797'>DriftWAM: Faster World-Action Models via Action-Aware Video Drifting</a></td><td>74</td><td>9</td><td>World Model</td><td>world-action model의 few-step 증류에 action-aware drifting을 써서 로봇 제어 추론 효율을 높임</td></tr>
<tr><td>5</td><td><a href='https://arxiv.org/abs/2611.33745'>WhatIf: Counterfactual World Models over Action-Grounded Causal Graphs for Robotic Manipulation</a></td><td>72</td><td>10</td><td>World Model</td><td>행동 기반 인과 그래프 위 counterfactual world model로 로봇 조작 행동 비교, 우선 주제 직접 해당함</td></tr>
<tr><td>6</td><td><a href='https://arxiv.org/abs/2611.33467'>SplatWAM: Splatting World Action Models for Real-Time 3D Imagination</a></td><td>72</td><td>9</td><td>World Model</td><td>action-conditioned 3D Gaussian 기반 world action model로 실시간 3D 상상이 강한 관련성임</td></tr>
<tr><td>7</td><td><a href='https://arxiv.org/abs/2611.33799'>Dynamic Forcing: Learning Action-Grounded Sparse Dynamic Representations with Dense Future Guidance for World Action Models</a></td><td>72</td><td>9</td><td>World Model</td><td>WAM에서 행동 관련 sparse dynamic 표현과 dense future guidance를 결합하여 로봇 제어 world model을 개선함</td></tr>
<tr><td>8</td><td><a href='https://arxiv.org/abs/2611.34435'>Most of the Way There: Turning a Strong Video Prior into an Action-Conditioned World Model</a></td><td>72</td><td>9</td><td>World Model</td><td>강한 video prior를 action-conditioned world model로 전환하는 방법을 다룸</td></tr>
<tr><td>9</td><td><a href='https://arxiv.org/abs/2611.33925'>Beyond the Happy Path: Generalizing Robot World Models from Simulated Failures</a></td><td>70</td><td>9</td><td>World Model</td><td>시뮬레이션 실패 데이터로 robot world model의 off-happy-path 일반화를 높임, failure 주제와 world model에 직결됨</td></tr>
<tr><td>10</td><td><a href='https://arxiv.org/abs/2611.33794'>Keep or Roll Back? Out-of-Loop Judges for Self-Improving VLA and End-to-End Embodied Policies</a></td><td>70</td><td>9</td><td>VLA</td><td>자기 개선 VLA에서 out-of-loop judge로 롤백 여부 결정, failure/평가 관점에서 직접 해당함</td></tr>
<tr><td>11</td><td><a href='https://arxiv.org/abs/2611.34067'>When to Respond, Where to Ground: Streaming 3D Affordance Grounding</a></td><td>68</td><td>8</td><td>Embodied AI</td><td>streaming RGB-D에서 응답 시점과 3D affordance 위치를 함께 푸는 새 문제 설정임</td></tr>
<tr><td>12</td><td><a href='https://arxiv.org/abs/2611.33398'>Best-of-$N$ Test-Time Steering Can Lead to Reward Hacking in Vision-Language-Action Models</a></td><td>68</td><td>8</td><td>VLA</td><td>VLA의 Best-of-N test-time steering이 reward hacking을 일으킴을 보임, test-time 주제와 직결되고 중요한 경고임</td></tr>
<tr><td>13</td><td><a href='https://arxiv.org/abs/2611.33917'>Event-WAM: Learning to Act with Event-Derived Futures</a></td><td>66</td><td>9</td><td>World Model</td><td>event 파생 미래를 쓰는 WAM으로 로봇 행동 학습에 새 보조 목표를 제안함</td></tr>
<tr><td>14</td><td><a href='https://arxiv.org/abs/2611.34509'>Long-Horizon Planning with Latent World Models via Graph Anchors</a></td><td>66</td><td>9</td><td>World Model</td><td>그래프 anchor로 latent world model의 장기 planning 한계를 보완함, planning 거리 실패를 짚은 점이 의미 있음</td></tr>
<tr><td>15</td><td><a href='https://arxiv.org/abs/2611.33560'>Skeptic: Grounding Failure Diagnosis for Robot Skill Discovery</a></td><td>66</td><td>8</td><td>Embodied AI</td><td>로봇 skill discovery에서 실패 원인을 grounding하여 진단함, failure diagnosis 주제와 맞음</td></tr>
<tr><td>16</td><td><a href='https://arxiv.org/abs/2611.34288'>Rehearse in 3D, Render in 2D: Physically Consistent and Editable Robot World Models</a></td><td>65</td><td>9</td><td>World Model</td><td>3D에서 예측하고 2D로 렌더링하는 물리 일관 편집 가능 world model, 새 표현이며 관련성 높음</td></tr>
<tr><td>17</td><td><a href='https://arxiv.org/abs/2611.33650'>Linear-Time Online Visual Geometry Transformer with Hybrid Architecture</a></td><td>65</td><td>7</td><td>3D Vision</td><td>VGGT 계열을 선형 시간 online 모델로 바꿔 스트리밍 3D 재구성에 유용함</td></tr>
<tr><td>18</td><td><a href='https://arxiv.org/abs/2611.33710'>$\mathrm{M}^{2}$-WAM: Efficient Hierarchical Memory Across Modalities and Timescales for World-Action Models</a></td><td>64</td><td>9</td><td>World Model</td><td>world-action model에 모달리티·시간 척도 계층 memory를 도입함, robot memory와 장기 조작에 직결됨</td></tr>
<tr><td>19</td><td><a href='https://arxiv.org/abs/2611.34560'>M$^{2}$AdaptVLA: Multimodal Memory-Augmented Vision-Language-Action Model with Predictive Test-Time Adaptation</a></td><td>64</td><td>9</td><td>VLA</td><td>멀티모달 memory와 predictive test-time adaptation을 갖춘 VLA, memory와 TTA 주제에 직결됨</td></tr>
<tr><td>20</td><td><a href='https://arxiv.org/abs/2611.34914'>Cairn: Object-Centric 3D Trajectory Priors for Steering Frozen VLAs</a></td><td>64</td><td>9</td><td>VLA</td><td>object-centric 3D trajectory prior로 frozen VLA를 steering함, object-centric 표현과 inference-time 제어에 맞음</td></tr>
<tr><td>21</td><td><a href='https://arxiv.org/abs/2611.33591'>VivaWorld: Long-Horizon Video World Model With Compositional 3D Priors</a></td><td>64</td><td>7</td><td>World Model</td><td>3D prior 기반 long-horizon video world model로 기하 일관성과 카메라 제어를 다룸</td></tr>
<tr><td>22</td><td><a href='https://arxiv.org/abs/2611.34117'>CoTacWAM: Joint Modeling of Vision and Touch for Robotic Manipulation</a></td><td>63</td><td>9</td><td>World Model</td><td>wrist vision과 touch의 공유 contact semantics를 학습한 WAM, tactile 주제와 맞음</td></tr>
<tr><td>23</td><td><a href='https://arxiv.org/abs/2611.33914'>X-World: Transferring Video Priors to Cross-Embodiment Robot Control</a></td><td>62</td><td>9</td><td>World Model</td><td>video prior를 cross-embodiment 제어로 전이하는 world model 접근, 사람/로봇 영상 활용에 의미 있음</td></tr>
<tr><td>24</td><td><a href='https://arxiv.org/abs/2611.34280'>Escapingthe instruction blackhole of vision-language-action policies via optimal-transport wormholes</a></td><td>62</td><td>9</td><td>VLA</td><td>VLA가 지시 변경을 무시하는 instruction black hole을 정의하고 optimal transport로 해결함, 새 문제 설정임</td></tr>
<tr><td>25</td><td><a href='https://arxiv.org/abs/2611.33511'>ArtLang-4D: Articulation-Aware Dynamic Language Fields from Monocular Videos</a></td><td>62</td><td>7</td><td>3D Vision</td><td>articulation-aware 4D language field로 관절 물체 상태 질의를 가능케 하여 manipulation과 관련 높음</td></tr>
<tr><td>26</td><td><a href='https://arxiv.org/abs/2611.33779'>DuoWM:Integrating Dual 6-DoF Visual Flows into Action-Conditioned Drone World Model</a></td><td>62</td><td>7</td><td>World Model</td><td>드론 6-DoF flow를 넣은 action-conditioned world model로 행동 정렬을 개선함</td></tr>
<tr><td>27</td><td><a href='https://arxiv.org/abs/2611.34257'>CamAct: Learning Robotic Manipulation from In-the-Wild Videos via Camera Motion</a></td><td>60</td><td>9</td><td>VLA</td><td>카메라 움직임으로 in-the-wild 영상에서 manipulation을 학습함, 데이터 스케일링에 새 관점이나 검증 확인 필요함</td></tr>
<tr><td>28</td><td><a href='https://arxiv.org/abs/2611.34302'>Co-World Model for Human-Video-to-Robot Transfer via Co-Constructed Shared Latent Dynamics</a></td><td>60</td><td>9</td><td>World Model</td><td>사람 영상에서 공유 latent dynamics를 공동 구성해 로봇으로 전이함, 가치 있으나 제한된 증거일 수 있음</td></tr>
<tr><td>29</td><td><a href='https://arxiv.org/abs/2611.33352'>Why Does Sensor Depth Fail Learned Manipulation Policies? Finding the Failure Mode with ACT</a></td><td>60</td><td>8</td><td>Manipulation</td><td>ACT에서 sensor depth가 policy를 실패시키는 원인을 분석함, 실용적 진단 연구이나 방법 novelty는 제한적임</td></tr>
<tr><td>30</td><td><a href='https://arxiv.org/abs/2611.33769'>FailPoint-X: A Policy-Matched, Failure-Anchored Benchmark for Offline VLA Post-Training from Human Takeovers</a></td><td>60</td><td>8</td><td>VLA</td><td>human takeover에서 failure 중심 offline VLA post-training 벤치마크를 제시함, 교정 학습 주제와 맞음</td></tr>
<tr><td>31</td><td><a href='https://arxiv.org/abs/2611.33915'>SEEK: Self-Evolution through Execution Knowledge for Agentic Robot Manipulation</a></td><td>60</td><td>8</td><td>Embodied AI</td><td>실행 지식을 보존하는 자기 진화 agentic manipulation을 제안함, memory 관련이나 foundation model 의존임</td></tr>
<tr><td>32</td><td><a href='https://arxiv.org/abs/2611.34347'>AIRIS: Benchmarking Social Embodied Intelligence in Egocentric Streaming Videos</a></td><td>60</td><td>7</td><td>Embodied AI</td><td>egocentric 스트리밍에서 사회적 개입 시점과 방식을 판단하는 embodied benchmark임</td></tr>
<tr><td>33</td><td><a href='https://arxiv.org/abs/2611.34644'>Motion Beyond Pixels: Learning Future Visual Representations for Object-Centric Dynamics</a></td><td>60</td><td>7</td><td>World Model</td><td>embodied world model용 물체 중심 미래 시각 표현 학습으로 RGB 재구성 대신 의미와 기하를 예측함</td></tr>
<tr><td>34</td><td><a href='https://arxiv.org/abs/2611.34739'>Was the Model Given the Right Action? Auditing and Repairing Action Interfaces in Navigation World Models</a></td><td>60</td><td>7</td><td>World Model</td><td>navigation world model의 행동 인터페이스 불일치를 감사하고 복구함, 평가 방법론 측면에서 참신함</td></tr>
<tr><td>35</td><td><a href='https://arxiv.org/abs/2611.34054'>CARE-WM: Same-Horizon Self-Conditioning with Constraint-Adaptive Regularization for Latent World Models</a></td><td>60</td><td>7</td><td>World Model</td><td>latent world model 계획을 위한 같은 horizon self-conditioning과 제약 적응 정규화를 제안함</td></tr>
<tr><td>36</td><td><a href='https://arxiv.org/abs/2611.33655'>Recall4D: Forgetting, Not Misalignment, Limits Long-Horizon Feed-Forward 4D Reconstruction</a></td><td>60</td><td>6</td><td>3D Vision</td><td>장기 4D 재구성의 한계가 정렬이 아닌 forgetting임을 보이는 분석이 설득력 있음</td></tr>
<tr><td>37</td><td><a href='https://arxiv.org/abs/2611.33513'>Learning to Reason in Real-Time</a></td><td>60</td><td>5</td><td>RL</td><td>실시간 제약 하에서 추론 시간을 고려해 학습, 실세계 agent에 중요한 문제 설정임</td></tr>
<tr><td>38</td><td><a href='https://arxiv.org/abs/2611.33993'>Aegis-VLA: Reliability-Gated Action Refinement via a Trajectory World Model for Dynamic Object Manipulation</a></td><td>58</td><td>8</td><td>VLA</td><td>궤적 world model로 reliability를 게이팅해 동적 물체 조작 action을 보정함, 관련성 높으나 모듈 조합 성격임</td></tr>
<tr><td>39</td><td><a href='https://arxiv.org/abs/2611.34043'>WISER-RL: A Wake-Sleep Learning Mechanism for Robot Reinforcement Learning from One Demonstration</a></td><td>58</td><td>8</td><td>RL</td><td>하나의 데모에서 wake-sleep 루프로 RL을 개선함, 데모 효율적 학습이며 실험 범위 확인 필요함</td></tr>
<tr><td>40</td><td><a href='https://arxiv.org/abs/2611.34124'>WAtcher: Watching Ahead for Safe Robotic Manipulation with Efficient World-Action Models</a></td><td>58</td><td>8</td><td>World Model</td><td>WAM에 안전 감지를 추가해 위험 action chunk를 걸러냄, safety 측면에서 관련됨</td></tr>
<tr><td>41</td><td><a href='https://arxiv.org/abs/2611.34741'>ELMO: Emergent Representations In Imitation Learning Via Dynamic Hierarchical Action Chunking</a></td><td>58</td><td>8</td><td>Manipulation</td><td>동적 hierarchical action chunking으로 imitation learning 표현을 창발시킴, 학습 구조 측면에서 의미 있음</td></tr>
<tr><td>42</td><td><a href='https://arxiv.org/abs/2611.34936'>DexLink: Synthesizing Dexterous Behaviors from Chained Hand-object Poses</a></td><td>58</td><td>8</td><td>Manipulation</td><td>chained hand-object pose로 dexterous 행동을 합성함, 데모 없이 확장하는 점이 의미 있음</td></tr>
<tr><td>43</td><td><a href='https://arxiv.org/abs/2611.34139'>An Image Detectability Field as a Viewpoint Utility for 2D-3D Localization in Sparse Maps</a></td><td>58</td><td>7</td><td>3D Vision</td><td>image detectability field를 viewpoint utility로 써서 능동 시점 선택과 연결됨</td></tr>
<tr><td>44</td><td><a href='https://arxiv.org/abs/2611.34224'>EgoMyo: Physical Hand State Estimation from Egocentric Video and Wrist Electromyography</a></td><td>58</td><td>7</td><td>Manipulation</td><td>egocentric 영상과 손목 EMG로 접촉/힘 포함 hand state를 추정하여 dexterous 데이터 수집과 연결됨</td></tr>
<tr><td>45</td><td><a href='https://arxiv.org/abs/2611.34811'>HOG-WAM: Improving Visual Robustness through Future Gradient Prediction</a></td><td>58</td><td>7</td><td>World Model</td><td>world-action model에 미래 HOG 구조 supervision을 더해 시각 교란에 강인하게 함</td></tr>
<tr><td>46</td><td><a href='https://arxiv.org/abs/2611.34830'>Not all world models can doubt: how training objective and architecture shape epistemic uncertainty in JEPA and RSSM world models</a></td><td>58</td><td>7</td><td>World Model</td><td>JEPA와 RSSM world model의 epistemic uncertainty 능력 차이를 분석함, 신뢰 가능한 planning에 시사점 있음</td></tr>
<tr><td>47</td><td><a href='https://arxiv.org/abs/2611.33687'>Read Before You Use: Improving Visual Memory Utilization in Vision-Language Models</a></td><td>58</td><td>6</td><td>Multimodal</td><td>VLM이 시각 memory를 제대로 쓰지 못하는 문제를 다루어 robot memory와 연결됨</td></tr>
<tr><td>48</td><td><a href='https://arxiv.org/abs/2611.33822'>MetaDecomp: Adaptive Task Decomposition via Meta-Learned Procedural Memory</a></td><td>58</td><td>5</td><td>Embodied AI</td><td>meta-learned procedural memory로 적응적 task 분해, 장기 계획·memory 관점이 이어짐</td></tr>
<tr><td>49</td><td><a href='https://arxiv.org/abs/2611.33635'>FreshVLA: Frequency-Regularized Time Scale Hierarchical Latent Actions for Vision-Language-Action Models</a></td><td>57</td><td>8</td><td>VLA</td><td>주파수 정규화와 시간 계층 latent action으로 VLA 학습을 개선함, latent action 설계 측면에서 관련됨</td></tr>
<tr><td>50</td><td><a href='https://arxiv.org/abs/2611.34014'>Hetero-Associative Visuomotor Memory: Soft Recall as a Base for Learned Residuals in Few-Demonstration Imitation</a></td><td>56</td><td>8</td><td>Manipulation</td><td>few-demo imitation에서 soft recall memory와 residual 학습을 분석함, robot memory와 연결됨</td></tr>
<tr><td>51</td><td><a href='https://arxiv.org/abs/2611.33403'>ArtKit: Motion-Driven Re-Segmentation and Link Re-Generation for Articulated Objects from RGB-D Video</a></td><td>56</td><td>6</td><td>3D Vision</td><td>RGB-D 영상에서 articulated model과 kinematic tree를 복원하여 manipulation 연관 높음</td></tr>
<tr><td>52</td><td><a href='https://arxiv.org/abs/2611.33810'>FlipVLA: Backdoor Attacks on Vision-Language-Action(VLA) Models Only Through Bit Flips</a></td><td>55</td><td>8</td><td>VLA</td><td>VLA 가중치 bit flip만으로 backdoor를 심는 안전성 연구로 신선하나 방어는 미흡함</td></tr>
<tr><td>53</td><td><a href='https://arxiv.org/abs/2611.33579'>DexEngine: Scaling Human Demonstrations into Physically Executable Whole-Robot Data</a></td><td>55</td><td>8</td><td>Manipulation</td><td>사람 hand-object 데모를 실행 가능한 whole-robot 데이터로 변환함, 데이터 스케일링 엔지니어링 성격이 강함</td></tr>
<tr><td>54</td><td><a href='https://arxiv.org/abs/2611.33816'>$\widetilde{\varepsilon}$: Does Initial Noise Induce Directional Bias in Vision-Language-Action Models?</a></td><td>55</td><td>8</td><td>VLA</td><td>diffusion VLA의 초기 noise가 방향성 편향을 일으키는지 분석함, 흥미로운 진단이나 범위 확인 필요함</td></tr>
<tr><td>55</td><td><a href='https://arxiv.org/abs/2611.33963'>Targeted Adaptation of World-Action Models via Interaction and Motion Heads</a></td><td>55</td><td>8</td><td>World Model</td><td>WAM에 interaction head와 motion head로 표적 적응함, 모듈 추가 성격이나 관련 주제임</td></tr>
<tr><td>56</td><td><a href='https://arxiv.org/abs/2611.34130'>WorldPhy: Benchmarking Fine-Grained Physical Plausibility of World Models in Robotics</a></td><td>55</td><td>8</td><td>World Model</td><td>로봇 world model의 물리적 타당성 세부 벤치마크를 제시함, 평가 기여이나 world model 주제 적합함</td></tr>
<tr><td>57</td><td><a href='https://arxiv.org/abs/2611.34148'>Ground Your Steps: Optimizing Sampling Schedules in Flow Matching Robot Policies</a></td><td>55</td><td>8</td><td>Manipulation</td><td>flow matching policy의 sampling schedule을 NFE 예산에서 최적화함, inference 효율 측면에서 유용하나 incremental임</td></tr>
<tr><td>58</td><td><a href='https://arxiv.org/abs/2611.34416'>CHASE: Curiosity-Guided Skill Acquisition for Embodied Task Execution</a></td><td>55</td><td>8</td><td>Embodied AI</td><td>호기심 기반 가설 수립과 skill 습득을 제안함, active 탐색 측면에서 관련됨</td></tr>
<tr><td>59</td><td><a href='https://arxiv.org/abs/2611.34655'>Nav4Manip: From Navigation to Dexterous Mobile Manipulation through Co-Evolution</a></td><td>55</td><td>8</td><td>Manipulation</td><td>navigation과 dexterous mobile manipulation의 co-evolution을 제안함, 시스템 통합 성격임</td></tr>
<tr><td>60</td><td><a href='https://arxiv.org/abs/2611.34745'>How Well Do Vision-Language Scene Graphs Serve as Memory for Embodied Question Answering?</a></td><td>55</td><td>8</td><td>Embodied AI</td><td>scene graph를 EQA memory로 쓸 때의 answerability를 분석함, scene graph/memory 주제에 직결됨</td></tr>
<tr><td>61</td><td><a href='https://arxiv.org/abs/2611.34884'>FineDex: Bridging Fine-Grained Human-Object Interaction Generation to Dexterous Humanoid Manipulation</a></td><td>55</td><td>8</td><td>Manipulation</td><td>fine-grained HOI 생성을 dexterous humanoid 조작에 연결함, dexterous 주제와 맞음</td></tr>
<tr><td>62</td><td><a href='https://arxiv.org/abs/2611.34249'>Navigent: A Geometry-Grounded Agentic Framework for Vision Language Navigation</a></td><td>55</td><td>8</td><td>Navigation</td><td>기하 grounding agent 구조로 MLLM VLN 수행, training-free 접근이나 navigation 우선 주제임</td></tr>
<tr><td>63</td><td><a href='https://arxiv.org/abs/2611.33934'>Towards 360$^\circ$ Embodied UAV Tracking Without Turning</a></td><td>55</td><td>7</td><td>Navigation</td><td>360도 전방위 인식으로 heading 분리한 embodied UAV tracking 패러다임임</td></tr>
<tr><td>64</td><td><a href='https://arxiv.org/abs/2611.33460'>Fast Muscle-Driven Whole-Body Motion Tracking with a Differentiable World Model</a></td><td>55</td><td>7</td><td>RL</td><td>미분 가능한 world model로 근골격 전신 모션 트래킹을 빠르게 학습함, 제어 연관됨</td></tr>
<tr><td>65</td><td><a href='https://arxiv.org/abs/2611.33382'>ArtTet: Watertight Part Meshes of Articulated Objects from Rigid-Body Rules and Partitioned Marching Tetrahedra</a></td><td>55</td><td>6</td><td>3D Vision</td><td>articulated object의 part mesh와 joint 복원으로 manipulation용 asset과 관련됨</td></tr>
<tr><td>66</td><td><a href='https://arxiv.org/abs/2611.33964'>Embodied-VGGT: Preserving Reliable Local Geometry for Long-Sequence Reconstruction</a></td><td>55</td><td>6</td><td>3D Vision</td><td>embodied 획득의 반복 구조를 활용해 VGGT 장기 재구성 drift를 줄임</td></tr>
<tr><td>67</td><td><a href='https://arxiv.org/abs/2611.34115'>A Simple Yet Effective Agent for Open-World Aerial Object Search</a></td><td>55</td><td>6</td><td>Navigation</td><td>frozen 모델만으로 open-world 항공 객체 탐색을 하는 단순 agent로 강한 baseline 성격임</td></tr>
<tr><td>68</td><td><a href='https://arxiv.org/abs/2611.34152'>Lost in the Grid: Where Multimodal LLMs Fail Between Seeing and Planning</a></td><td>55</td><td>6</td><td>Embodied AI</td><td>MLLM이 보기와 계획 사이 어디서 실패하는지 grid 환경에서 분해해 공간 추론 진단임</td></tr>
<tr><td>69</td><td><a href='https://arxiv.org/abs/2611.34480'>ProManO: Beyond Sim(3) for Metric Upgrade of Feed-Forward Geometry with Visual-Inertial Anchors</a></td><td>55</td><td>6</td><td>3D Vision</td><td>feed-forward 기하를 VIO 앵커로 metric 보정하는 Sim(3) 이상의 정렬이라 로봇 SLAM에 유용함</td></tr>
<tr><td>70</td><td><a href='https://arxiv.org/abs/2611.34894'>What a Drop Reveals: Sim-to-Real Material Estimation for Deformable Objects from Video</a></td><td>55</td><td>6</td><td>3D Vision</td><td>낙하 영상에서 변형체의 물성을 sim-to-real로 추정함, 변형체 조작에 유용함</td></tr>
<tr><td>71</td><td><a href='https://arxiv.org/abs/2611.33229'>Effect-Driven Skill Abstractions for Offline Reinforcement Learning</a></td><td>55</td><td>6</td><td>RL</td><td>effect 기반 discrete skill abstraction으로 long-horizon offline RL을 다룸, 새로운 skill 정의 방식이나 벤치마크 한정임</td></tr>
<tr><td>72</td><td><a href='https://arxiv.org/abs/2611.34931'>DynMF2: Rigid Motion Factorization by Expectation-Maximization for Monocular 4D Reconstruction and Motion Segmentation</a></td><td>55</td><td>5</td><td>3D Vision</td><td>강체 모션 분해 EM으로 단안 4D 복원과 모션 분할을 수행함, 동적 장면 표현에 연관됨</td></tr>
<tr><td>73</td><td><a href='https://arxiv.org/abs/2611.34943'>Tracking Any Point with Agentic Visual Reasoning</a></td><td>55</td><td>5</td><td>Video</td><td>VLM의 agentic 시각 추론으로 임의 점 추적을 수행함, 접근이 새로움</td></tr>
<tr><td>74</td><td><a href='https://arxiv.org/abs/2611.33872'>Normalizing Flows are Capable World Models</a></td><td>55</td><td>5</td><td>World Model</td><td>Normalizing flow를 world model로 활용해 상상 rollout 기반 의사결정을 제시함</td></tr>
<tr><td>75</td><td><a href='https://arxiv.org/abs/2611.34641'>Distractor-Robust Reinforcement Learning via Variational Bisimulation</a></td><td>55</td><td>5</td><td>World Model</td><td>bisimulation 기반으로 distractor에 강한 MBRL world model 학습함, 관련성 있으나 벤치마크 범위 제한적임</td></tr>
<tr><td>76</td><td><a href='https://arxiv.org/abs/2611.33728'>Asset4D-Bench: Benchmarking Coding Agents for Editable 3D and 4D Reconstruction</a></td><td>55</td><td>5</td><td>3D Vision</td><td>coding agent가 편집 가능한 3D/4D 재구성을 하는지 평가하는 benchmark, 동역학 일관성 점검이 흥미로움</td></tr>
<tr><td>77</td><td><a href='https://arxiv.org/abs/2611.33706'>EVA: Evidence-seeking Visual Agent for Hallucination-Resistant Multimodal Reasoning</a></td><td>55</td><td>4</td><td>Multimodal</td><td>증거를 찾아 확인하는 visual agent로 MLLM 환각 완화, active perception 관점이 있음</td></tr>
<tr><td>78</td><td><a href='https://arxiv.org/abs/2611.33612'>Failure Broadens, Success Sharpens: Continual Adaptation of Tool-Use Agents Across Diverse Tasks with Dual-Polarity Memory</a></td><td>55</td><td>3</td><td>NLP</td><td>성공/실패 기억의 서로 다른 효용을 분리한 tool-use agent 지속 적응, failure memory 관점이 참고됨</td></tr>
<tr><td>79</td><td><a href='https://arxiv.org/abs/2611.33304'>The Platonic Representation Hypothesis in Jacobian-Space: Language and Vision Models Agree Approximately Up to a Rotation</a></td><td>55</td><td>3</td><td>Multimodal</td><td>Platonic Representation 가설을 Jacobian 공간에서 검증, 표현 수렴 이론 관점에서 의미 있음</td></tr>
<tr><td>80</td><td><a href='https://arxiv.org/abs/2611.34360'>One Patch, Many Policies: Object-Associated Physical Patch Attacks on Robotic Manipulation</a></td><td>52</td><td>8</td><td>VLA</td><td>VLA와 WAM을 겨냥한 객체 부착 물리 patch 공격으로 안전성 평가에 쓰임</td></tr>
<tr><td>81</td><td><a href='https://arxiv.org/abs/2611.33733'>PROVE: Predict-to-Specify and Observe-to-Verify for Human-Aligned Evaluation of Mobile Manipulation</a></td><td>52</td><td>8</td><td>Manipulation</td><td>mobile manipulation 평가에서 예측-명세 후 관찰-검증으로 사람과 정렬된 평가를 제안함, 평가 신뢰성에 의미 있음</td></tr>
<tr><td>82</td><td><a href='https://arxiv.org/abs/2611.34352'>Beyond Natural-Language Instructions: Temporal Logic as a Task Language for VLA Models with Visual-Logical Fusion</a></td><td>52</td><td>8</td><td>VLA</td><td>temporal logic을 VLA 과제 언어로 쓰는 TL-VLA 제안함, 새 task language 관점이나 범위 확인 필요함</td></tr>
<tr><td>83</td><td><a href='https://arxiv.org/abs/2611.34675'>RoboEvo$^2$: Recursive Robot Self-Improvement via Harness-Policy Co-Evolution</a></td><td>52</td><td>8</td><td>VLA</td><td>harness와 policy의 공진화로 robot 자기 개선을 제안함, 개념은 흥미로우나 근거 확인 필요함</td></tr>
<tr><td>84</td><td><a href='https://arxiv.org/abs/2611.34864'>RePace: Reasoning about Demonstration Speedup for Faster Vision-Language-Action Policies</a></td><td>52</td><td>8</td><td>VLA</td><td>데모 속도 향상 추론으로 더 빠른 VLA를 얻음, 실용적이나 incremental임</td></tr>
<tr><td>85</td><td><a href='https://arxiv.org/abs/2611.33878'>Off the Driven Path: Transferable Road Understanding in Driving VLAs</a></td><td>52</td><td>7</td><td>VLA</td><td>driving VLA가 내재화한 도로 지식을 탐침하는 Road-KSU 분석임</td></tr>
<tr><td>86</td><td><a href='https://arxiv.org/abs/2611.34915'>Memory Is Not Ground Truth: Revising Navigation Authority under Unreliable VLM Evidence for Persistent Semantic Navigation</a></td><td>52</td><td>7</td><td>Navigation</td><td>VLM 증거가 불확실할 때 navigation 권한을 수정하는 persistent semantic navigation 제안함, memory 관련됨</td></tr>
<tr><td>87</td><td><a href='https://arxiv.org/abs/2611.34932'>MERLoc: Robust Robot Localization in Dynamic Environments with Pose-Based Retrieval over 3D Gaussian Splatting References</a></td><td>52</td><td>7</td><td>3D Vision</td><td>3DGS reference 위 pose 기반 retrieval로 동적 환경 localization함, 3DGS 활용이나 localization 응용임</td></tr>
<tr><td>88</td><td><a href='https://arxiv.org/abs/2611.34108'>Detectable by Design: Learning a Continuous 3D Saliency Field from 2D Detector Responses</a></td><td>52</td><td>6</td><td>3D Vision</td><td>2D detector 반응으로 3D saliency field를 학습해 sparse map 위치추정에 쓰는 새 정의임</td></tr>
<tr><td>89</td><td><a href='https://arxiv.org/abs/2611.33378'>DreamTour: Layout Steering for Training-Free World Exploration</a></td><td>52</td><td>5</td><td>World Model</td><td>training-free 카메라 경로 제어 world exploration으로 world model 응용과 연결됨</td></tr>
<tr><td>90</td><td><a href='https://arxiv.org/abs/2611.34693'>ShowNow: Fine-Grained Speculative Streaming for Responsive World Models</a></td><td>52</td><td>5</td><td>World Model</td><td>인터랙티브 world model의 투기적 스트리밍으로 행동 입력 지연을 줄임</td></tr>
<tr><td>91</td><td><a href='https://arxiv.org/abs/2611.34449'>HoloBrain-0.5 Technical Report</a></td><td>50</td><td>8</td><td>VLA</td><td>여러 embodiment용 VLA 기술 보고서로 scale-up 위주임</td></tr>
<tr><td>92</td><td><a href='https://arxiv.org/abs/2611.34538'>Dynamic Task Update Benchmark (DTU-Bench): Evaluating Runtime Task Adaptation in Robotic Manipulation</a></td><td>50</td><td>8</td><td>VLA</td><td>실행 중 지시 변경 적응 벤치마크 DTU-Bench를 제시함, 평가 기여이나 문제 설정 유용함</td></tr>
<tr><td>93</td><td><a href='https://arxiv.org/abs/2611.34778'>Toward Agentic Robotics: A Large-Scale Study of Harness Design for Robot-Use Agents</a></td><td>50</td><td>7</td><td>Embodied AI</td><td>robot-use agent의 하네스 설계를 대규모로 연구함, 경험적 분석 기여임</td></tr>
<tr><td>94</td><td><a href='https://arxiv.org/abs/2611.34862'>BOP-Refer: Benchmark for Monocular 3D and 2D Object Grounding</a></td><td>50</td><td>6</td><td>3D Vision</td><td>BOP 9개 데이터셋 기반 단안 3D/2D 객체 grounding 벤치마크로 6D pose 조작에 연관됨</td></tr>
<tr><td>95</td><td><a href='https://arxiv.org/abs/2611.33922'>iMFPO: Improving Mean Flow Policy Optimization with Drift-Aware Velocity Alignment for Embodied Control</a></td><td>50</td><td>6</td><td>RL</td><td>drift-aware velocity 정렬로 mean flow policy 최적화를 개선함, 정책 학습 기법 개선 성격임</td></tr>
<tr><td>96</td><td><a href='https://arxiv.org/abs/2611.34064'>SPARC: Geometry-Guided Attention Pruning for Long-Horizon Camera-Controlled Video Generation</a></td><td>50</td><td>5</td><td>World Model</td><td>기하 유도 attention pruning으로 카메라 제어와 persistent scene memory를 구현함</td></tr>
<tr><td>97</td><td><a href='https://arxiv.org/abs/2611.33813'>Ensuring Deployment-Time Safety of Neural Network Controlled Systems via Localized Certificate Repair</a></td><td>50</td><td>5</td><td>RL</td><td>신경망 제어 시스템 국소 barrier certificate로 배포 시 안전 보장, 제어 안전성 방법임</td></tr>
<tr><td>98</td><td><a href='https://arxiv.org/abs/2611.33368'>Searching Ultra-Long Videos with Decision Models</a></td><td>50</td><td>4</td><td>Video</td><td>초장편 영상 증거 검색에 decision model을 써서 embodied memory 검색과 연결 가능함</td></tr>
<tr><td>99</td><td><a href='https://arxiv.org/abs/2611.34079'>WorldBridge: Bridging Scattered Views for Coherent 3D World Generation</a></td><td>50</td><td>4</td><td>3D Vision</td><td>겹침 없는 흩어진 뷰에서 일관된 3D world를 생성하는 문제를 다룸</td></tr>
<tr><td>100</td><td><a href='https://arxiv.org/abs/2611.34128'>FoundSurface: Feedforward Ray-Based 3D Scene Surface Reconstruction from Unposed Images</a></td><td>50</td><td>4</td><td>3D Vision</td><td>unposed 이미지에서 ray 기반 feed-forward 표면 재구성을 함</td></tr>
<tr><td>101</td><td><a href='https://arxiv.org/abs/2611.34907'>Agentic LongLive: Asynchronous Agentic Memory for Long Video Generation</a></td><td>50</td><td>4</td><td>Video</td><td>장기 비디오 생성용 비동기 에이전트 메모리로 memory 개념이 로봇 메모리와 연관됨</td></tr>
<tr><td>102</td><td><a href='https://arxiv.org/abs/2611.33162'>Attributing Agentic Failure in Reasoning Vision-Language Models with Interactive 2D Environments</a></td><td>50</td><td>4</td><td>Embodied AI</td><td>agentic VLM 실패 원인을 인터랙티브 2D 환경에서 귀속하는 분석으로 failure diagnosis와 연관됨</td></tr>
<tr><td>103</td><td><a href='https://arxiv.org/abs/2611.34046'>End-to-End Image-Goal Navigation for Agile Quadrotors via Recurrent State Distillation</a></td><td>48</td><td>7</td><td>Navigation</td><td>recurrent state distillation으로 quadrotor image-goal navigation 수행함, 응용 성격이 강함</td></tr>
<tr><td>104</td><td><a href='https://arxiv.org/abs/2611.34297'>BOT-Scale: A Traceable Evaluation Methodology for Robotic Manipulation</a></td><td>48</td><td>7</td><td>Manipulation</td><td>추적 가능한 manipulation 평가 방법론을 제시함, 평가 도구 기여임</td></tr>
<tr><td>105</td><td><a href='https://arxiv.org/abs/2611.34750'>SOLVE: Sparse, Ordered Keyposes Make LLM Agents Versatile and Efficient Robot Manipulator</a></td><td>48</td><td>7</td><td>Manipulation</td><td>희소 keypose로 LLM agent manipulation을 효율화함, training-free 접근이나 agent 파이프라인임</td></tr>
<tr><td>106</td><td><a href='https://arxiv.org/abs/2611.33255'>CriticalScenes: Scalable Photorealistic Critical-Scenario Generation for Closed-Loop Driving Adaptation</a></td><td>48</td><td>5</td><td>Embodied AI</td><td>재구성 기반 critical scenario 생성으로 driving planner 폐루프 적응을 다룸</td></tr>
<tr><td>107</td><td><a href='https://arxiv.org/abs/2611.33380'>FOCI: Trajectory Optimization on Gaussian Splats for Gaussian Robots</a></td><td>48</td><td>5</td><td>3D Vision</td><td>Gaussian splat 위의 Gaussian robot trajectory optimization으로 3DGS planning을 다룸, 적용 범위 제한적임</td></tr>
<tr><td>108</td><td><a href='https://arxiv.org/abs/2611.34545'>Recalling the Past to Answer the Present: Context-Aware Multi-Evidence Reasoning for Streaming Video Question Answering</a></td><td>48</td><td>4</td><td>Video</td><td>스트리밍 비디오 QA에서 과거 다중 근거 회상으로 embodied memory와 일부 연관됨</td></tr>
<tr><td>109</td><td><a href='https://arxiv.org/abs/2611.34730'>WorldInteract: Controllable Streaming Video Generation for Multi-Material Interactions</a></td><td>48</td><td>4</td><td>World Model</td><td>다중 재료 상호작용을 제어하는 스트리밍 비디오 생성으로 물리 world model에 연관됨</td></tr>
<tr><td>110</td><td><a href='https://arxiv.org/abs/2611.34248'>EXPOSURE: Explaining Sources of Uncertainty in Reinforcement Learning</a></td><td>48</td><td>4</td><td>RL</td><td>RL 불확실성 원천을 Shapley로 설명, 설명가능 RL 도구임</td></tr>
<tr><td>111</td><td><a href='https://arxiv.org/abs/2611.34608'>DuCo: Exploiting Dual Cross-Layer Consistency for Sparse Geometric Attention</a></td><td>48</td><td>3</td><td>3D Vision</td><td>visual geometry 모델의 희소 attention으로 장기 시퀀스 추론 효율화함</td></tr>
<tr><td>112</td><td><a href='https://arxiv.org/abs/2611.34762'>TASK Memory: Beyond Text-Only Memory with Activation Steering and Knowledge Editing against Memory Hallucination</a></td><td>48</td><td>2</td><td>LG</td><td>activation steering과 knowledge editing 기반 agent memory, memory 관점이나 LLM 중심임</td></tr>
<tr><td>113</td><td><a href='https://arxiv.org/abs/2611.34549'>CADENCE: Sensor-GroundedWorld-Consistent Gaussian SLAM for Collaborative Mobile Reconstruction</a></td><td>47</td><td>5</td><td>3D Vision</td><td>협업 모바일 Gaussian SLAM으로 기기 신뢰도를 반영함, 로봇 매핑에 연관됨</td></tr>
<tr><td>114</td><td><a href='https://arxiv.org/abs/2611.33374'>VersionGS: Compact and Motion-Robust Dynamic Gaussian Splatting via Versioned Gaussians</a></td><td>47</td><td>3</td><td>3D Vision</td><td>빠른 움직임에 강한 versioned Gaussian 동적 3DGS로 4D 표현 측면에서 관련됨</td></tr>
<tr><td>115</td><td><a href='https://arxiv.org/abs/2611.33390'>RoboARC: Physical Puzzles for Robotic Manipulation under Spatial Constraints</a></td><td>45</td><td>7</td><td>Manipulation</td><td>공간 제약 manipulation puzzle 벤치마크로 어려운 과제를 제시하나 벤치마크 기여임</td></tr>
<tr><td>116</td><td><a href='https://arxiv.org/abs/2611.33772'>Triage Before Fine-Tuning: Feasibility-Gated Selection and Monitored Adaptation of Embodied Foundation Models for a Fixed Physical Platform</a></td><td>45</td><td>7</td><td>Embodied AI</td><td>embodied foundation model 선택과 fine-tuning 전 feasibility triage를 제안함, 실용적이나 incremental임</td></tr>
<tr><td>117</td><td><a href='https://arxiv.org/abs/2611.34561'>Compact Vision-Language Navigation in Continuous Environmentsvia On-Policy Training and Route-Bearing Output</a></td><td>45</td><td>7</td><td>Navigation</td><td>on-policy 학습과 route-bearing 출력으로 compact VLN-CE를 구현함, 효율 중심 개선임</td></tr>
<tr><td>118</td><td><a href='https://arxiv.org/abs/2611.33739'>RegHarness: Regulating What Code-as-Policy Agents Keep from Steps to Skills</a></td><td>45</td><td>6</td><td>Embodied AI</td><td>Code-as-Policy agent가 유지할 코드를 규율하는 하네스 제안함, memory/skill 축적 주제와 관련됨</td></tr>
<tr><td>119</td><td><a href='https://arxiv.org/abs/2611.34485'>SkySearcher: High-Altitude Onboard VLM Reasoning for Aerial Semantic Search</a></td><td>45</td><td>6</td><td>Navigation</td><td>UAV VLM 기반 고고도 semantic search로 응용 성격이나 navigation 관련됨</td></tr>
<tr><td>120</td><td><a href='https://arxiv.org/abs/2611.33565'>EgoCARBS: Egocentric Video Meets Active Acoustics for Kitchen Action Understanding</a></td><td>45</td><td>4</td><td>Egocentric</td><td>egocentric 영상과 능동 음향으로 손/팔 동작을 복원하는 새 센서 조합임</td></tr>
<tr><td>121</td><td><a href='https://arxiv.org/abs/2611.33693'>GeoTex: Geometry-as-Texture Encoding and History-Grounded 4D Occupancy Forecasting</a></td><td>45</td><td>4</td><td>World Model</td><td>자율주행 4D occupancy 예측에서 기하-텍스처 인코딩을 제안함</td></tr>
<tr><td>122</td><td><a href='https://arxiv.org/abs/2611.33835'>3D CoCa v3: Contrastive Learners with Scene Graphs for Urban Scene Understanding</a></td><td>45</td><td>4</td><td>3D Vision</td><td>scene graph와 contrastive 학습으로 도시 3D scene 이해를 다룸</td></tr>
<tr><td>123</td><td><a href='https://arxiv.org/abs/2611.34614'>Commit2Drive: Perception-Grounded Language Decisions as Commitments for Trajectory Planning in Vision-Language-Action Driving Models</a></td><td>45</td><td>4</td><td>VLA</td><td>주행 VLA에서 언어 결정을 궤적 계획의 commitment로 묶음, 로봇 VLA와 간접 연관됨</td></tr>
<tr><td>124</td><td><a href='https://arxiv.org/abs/2611.34783'>SceneDesigner3D: Agentic Evolutionary Search for Principled Rearrangement of 3D Indoor Scenes</a></td><td>45</td><td>4</td><td>3D Vision</td><td>에이전트 진화 탐색의 3D 실내 장면 재배치로 rearrangement 계획과 간접 연관됨</td></tr>
<tr><td>125</td><td><a href='https://arxiv.org/abs/2611.34656'>Do We Still Need Reinforcement Learning When We Can Read the World Model?</a></td><td>45</td><td>4</td><td>RL</td><td>world model을 읽어 RL 필요성을 따지는 논의로 문제의식은 좋으나 근거 강도는 불확실함</td></tr>
<tr><td>126</td><td><a href='https://arxiv.org/abs/2611.34799'>Split-RL: Local Conflict Resolution in Reinforcement Learning</a></td><td>45</td><td>4</td><td>RL</td><td>국소 충돌 피드백을 분리하는 RL로 로봇 속도/정밀도 예시를 들었으나 검증 범위는 제한적임</td></tr>
<tr><td>127</td><td><a href='https://arxiv.org/abs/2611.33474'>Streaming Tax: Can Streaming VLMs Replace Their Offline Parents?</a></td><td>45</td><td>3</td><td>Video</td><td>streaming VLM이 offline VLM을 대체 가능한지 분석하며 실시간 embodied 인식에 참고됨</td></tr>
<tr><td>128</td><td><a href='https://arxiv.org/abs/2611.33698'>Efficient Scene-Distribution-Aware Second-Order Optimization for 3D Gaussian Splatting</a></td><td>45</td><td>3</td><td>3D Vision</td><td>3DGS 최적화에 scene 분포 고려 2차 최적화를 적용한 효율 개선임</td></tr>
<tr><td>129</td><td><a href='https://arxiv.org/abs/2611.33841'>The Missing Root: Geometric Imagination Without Images in Large Language Models</a></td><td>45</td><td>3</td><td>Multimodal</td><td>이미지 없이 LLM에 기하 상상을 부여하는 새 패러다임을 주장하나 검증 범위 불확실함</td></tr>
<tr><td>130</td><td><a href='https://arxiv.org/abs/2611.33948'>Where to Approximate: Understanding and Accelerating Looped Multi-View Reconstruction</a></td><td>45</td><td>3</td><td>3D Vision</td><td>looped 다시점 재구성에서 근사 위치를 분석하고 가속하는 방법임</td></tr>
<tr><td>131</td><td><a href='https://arxiv.org/abs/2611.34223'>AnyCam4D: Ray-Based 4D Gaussian Rendering for Arbitrary Camera Models</a></td><td>45</td><td>3</td><td>3D Vision</td><td>임의 카메라 모델용 ray 기반 4D Gaussian 렌더링으로 fisheye 로봇 영상에 유용함</td></tr>
<tr><td>132</td><td><a href='https://arxiv.org/abs/2611.34939'>A Mesh for Every Moment</a></td><td>45</td><td>3</td><td>3D Vision</td><td>다시점 동기 영상에서 동적 장면 메시 복원으로 4D 표현 연관됨</td></tr>
<tr><td>133</td><td><a href='https://arxiv.org/abs/2611.34935'>Can image generation help visual reasoning? An empirical study</a></td><td>45</td><td>3</td><td>Multimodal</td><td>이미지 생성이 visual reasoning에 도움 되는지 실증 연구로 embodied 연결은 간접적임</td></tr>
<tr><td>134</td><td><a href='https://arxiv.org/abs/2611.33764'>Improving Building Energy Efficiency with an Indoor Environmental World Model and Counterfactual Adaptive Learning</a></td><td>45</td><td>3</td><td>World Model</td><td>실내 환경 world model과 counterfactual 활용한 에너지 최적화, 제어 응용임</td></tr>
<tr><td>135</td><td><a href='https://arxiv.org/abs/2611.33437'>ViCARD: Visual Credit Assignment with Reward-Gated Distillation for Multimodal Reasoning</a></td><td>45</td><td>2</td><td>Multimodal</td><td>시각 credit assignment와 reward-gated distillation으로 multimodal RL 추론 개선함</td></tr>
<tr><td>136</td><td><a href='https://arxiv.org/abs/2611.34393'>Plausible Is Not Proven: Testing Failure Explanations in Monocular Depth Estimation</a></td><td>45</td><td>2</td><td>CV</td><td>단안 depth 실패 원인 설명을 검증하는 audit으로 failure diagnosis 방법론임</td></tr>
<tr><td>137</td><td><a href='https://arxiv.org/abs/2611.33174'>MGMem: An Efficient, Deterministic, and Provenance-Preserving Framework for Long-Horizon Agent Memory</a></td><td>45</td><td>2</td><td>NLP</td><td>LLM agent 장기 기억 framework, 결정적·출처 보존 설계가 robot memory에 약하게 참고됨</td></tr>
<tr><td>138</td><td><a href='https://arxiv.org/abs/2611.34398'>When Skills Fail to Compose: Compatibility and Retention in Language Models</a></td><td>45</td><td>2</td><td>NLP</td><td>독립 학습된 soft-prompt skill의 합성 호환성 분석, skill composition 관점이 skill chaining과 이어짐</td></tr>
<tr><td>139</td><td><a href='https://arxiv.org/abs/2611.34756'>Collect for Coverage, Replay with Evidence: Adaptive and Efficient On-Policy Distillation for Long-Horizon Agents</a></td><td>45</td><td>2</td><td>RL</td><td>장기 agent on-policy distillation을 prefix replay로 효율화, RL 효율 기법임</td></tr>
<tr><td>140</td><td><a href='https://arxiv.org/abs/2611.34440'>vSFT: Learning to Verbally Tune Agents at Test Time</a></td><td>45</td><td>2</td><td>LG</td><td>test time 언어로 agent를 조정하는 vSFT, language feedback 관점이 있음</td></tr>
<tr><td>141</td><td><a href='https://arxiv.org/abs/2611.34801'>Guidance as Variance Matching</a></td><td>45</td><td>1</td><td>LG</td><td>diffusion guidance를 분산 매칭으로 해석하는 이론적 기여임</td></tr>
<tr><td>142</td><td><a href='https://arxiv.org/abs/2611.33468'>Learning from Recurrence: Internalizing Depth-Induced Preferences in Looped Language Models</a></td><td>45</td><td>1</td><td>NLP</td><td>looped LM에서 깊이 선호를 내재화하는 학습, 효율 추론 측면에서 흥미로움</td></tr>
<tr><td>143</td><td><a href='https://arxiv.org/abs/2611.33670'>Rethinking Knowledge Distillation for Diffusion Language Models</a></td><td>45</td><td>1</td><td>NLP</td><td>diffusion LM KD 최초 체계 연구, 일반 생성모델 관점에서 참고됨</td></tr>
<tr><td>144</td><td><a href='https://arxiv.org/abs/2611.34051'>Stable Gated DeltaNet-2: Understanding and Mitigating Recurrent State Instability</a></td><td>45</td><td>1</td><td>LG</td><td>Gated DeltaNet-2 recurrent state 불안정 분석·완화, 선형 attention 효율 연구임</td></tr>
<tr><td>145</td><td><a href='https://arxiv.org/abs/2611.33731'>RoboJackVR: Turning Robot Tasks into VR Games for Scalable Demonstration Collection</a></td><td>42</td><td>7</td><td>Manipulation</td><td>VR 게임화로 teleoperation 데모 수집을 확장함, 데이터 수집 도구 기여임</td></tr>
<tr><td>146</td><td><a href='https://arxiv.org/abs/2611.34671'>DemoFoundry: Toward Scalable Photorealistic Robot Data with Coding Agents and Generative Rendering</a></td><td>42</td><td>7</td><td>Manipulation</td><td>coding agent와 generative rendering으로 사실적 데모 데이터를 합성함, 데이터 파이프라인 성격임</td></tr>
<tr><td>147</td><td><a href='https://arxiv.org/abs/2611.33721'>A general-purpose safe manipulator planning framework for diverse environments without retraining</a></td><td>42</td><td>6</td><td>Manipulation</td><td>재학습 없이 환경 변화에 대응하는 범용 안전 manipulator planning 제안함, 주장 대비 검증 범위가 관건임</td></tr>
<tr><td>148</td><td><a href='https://arxiv.org/abs/2611.33828'>Learning a Whole-Body Pivot-Walking Gait for Heavy-Box Transport with a Humanoid</a></td><td>42</td><td>5</td><td>RL</td><td>humanoid pivot-walking으로 무거운 상자를 운반하는 whole-body 학습함, 응용 성격임</td></tr>
<tr><td>149</td><td><a href='https://arxiv.org/abs/2611.33911'>CoTAMP: Cooperative Task and Motion Planning for Quadruped Robots with Large Language Models</a></td><td>42</td><td>5</td><td>Embodied AI</td><td>LLM 기반 quadruped 협력 TAMP를 제안함, 평가 범위 제한적임</td></tr>
<tr><td>150</td><td><a href='https://arxiv.org/abs/2611.33991'>QK-Bench: Benchmarking Quantitative Kinematic Understanding for Dynamic Spatial Intelligence</a></td><td>42</td><td>5</td><td>Embodied AI</td><td>정량적 kinematic 이해 벤치마크로 spatial reasoning을 평가함, 벤치마크 기여임</td></tr>
<tr><td>151</td><td><a href='https://arxiv.org/abs/2611.33586'>DFLAT: Model-based Diffusion on Differentially Flat Spaces for Long-Horizon Trajectory Optimization</a></td><td>42</td><td>4</td><td>Manipulation</td><td>differentially flat 공간의 model-based diffusion으로 장기 trajectory 최적화함, 일반 플래닝 기여임</td></tr>
<tr><td>152</td><td><a href='https://arxiv.org/abs/2611.33452'>HumblePRM: Improving VLM Abstention in Ambiguous Situations through Process Reward Modeling</a></td><td>42</td><td>3</td><td>Multimodal</td><td>VLM이 모호한 상황에서 abstain하도록 PRM을 쓰며 failure 인지와 일부 연결됨</td></tr>
<tr><td>153</td><td><a href='https://arxiv.org/abs/2611.33824'>Revisiting Monocular In-Hand Object Scanning: Dataset, Pose Estimation, and Surface Reconstruction</a></td><td>42</td><td>3</td><td>3D Vision</td><td>단안 in-hand 객체 스캔 dataset과 자세/표면 복원임</td></tr>
<tr><td>154</td><td><a href='https://arxiv.org/abs/2611.34078'>Projector Subspace Optimization for Multimodal Continual Instruction Tuning</a></td><td>42</td><td>3</td><td>Multimodal</td><td>projector subspace 최적화로 multimodal continual tuning을 다룸</td></tr>
<tr><td>155</td><td><a href='https://arxiv.org/abs/2611.34126'>Out of Sight, Not Out of Clues: Can Video LLMs Guess from Partial Evidence?</a></td><td>42</td><td>3</td><td>Video</td><td>일부 증거만 있을 때 Video LLM의 추측/기권 행동 평가임</td></tr>
<tr><td>156</td><td><a href='https://arxiv.org/abs/2611.34476'>TACC: Target-Aware Carrier Compression for Dense-Context Novel View Synthesis</a></td><td>42</td><td>3</td><td>3D Vision</td><td>feed-forward 신규 뷰 합성의 컨텍스트 압축으로 효율 개선 위주임</td></tr>
<tr><td>157</td><td><a href='https://arxiv.org/abs/2611.34813'>Solve Vision with Code: Coding Agents Are Stronger Visual Reasoners Than Video Models</a></td><td>42</td><td>3</td><td>Video</td><td>비디오 모델 대신 코딩 에이전트가 시각 추론에 강함을 보이는 분석임</td></tr>
<tr><td>158</td><td><a href='https://arxiv.org/abs/2611.33751'>VAPOR: Improving Multimodal Reasoning with Sparse Visual Updates</a></td><td>42</td><td>2</td><td>Multimodal</td><td>sparse visual update로 MLLM 추론 효율을 높이는 방법임</td></tr>
<tr><td>159</td><td><a href='https://arxiv.org/abs/2611.33886'>DeltaRAE: Derivative Tokenization for Long Video Generation</a></td><td>42</td><td>2</td><td>Video</td><td>미분 기반 tokenizer로 장편 영상 생성을 다루는 신선한 시도임</td></tr>
<tr><td>160</td><td><a href='https://arxiv.org/abs/2611.33957'>RefMix: Expanding Endpoint Proposals for Diversity-Preserving Reward Fine-Tuning</a></td><td>42</td><td>2</td><td>Generative</td><td>online forward matching의 reward fine-tuning에서 다양성 보존을 다룸</td></tr>
<tr><td>161</td><td><a href='https://arxiv.org/abs/2611.33615'>Learning from Natural Images Untangles Number Sense</a></td><td>42</td><td>2</td><td>Multimodal</td><td>자연 이미지 학습이 VLM 수 감각을 푸는지 분석, 인식 표현 진단임</td></tr>
<tr><td>162</td><td><a href='https://arxiv.org/abs/2611.33232'>How Many Samples Is RL Worth? Best-of-N versus RL Post-Training for Text-to-Image Models</a></td><td>42</td><td>1</td><td>Generative</td><td>RL post-training과 best-of-N의 sample 효율 비교 분석이 흥미로우나 T2I 한정임</td></tr>
<tr><td>163</td><td><a href='https://arxiv.org/abs/2611.33316'>What Does RL Post-Training Teach Text-to-Image Models? A Skill-Wise Analysis of Flow-GRPO</a></td><td>42</td><td>1</td><td>Generative</td><td>Flow-GRPO 이득을 pass@k로 분해한 분석이 유익하나 T2I 한정임</td></tr>
<tr><td>164</td><td><a href='https://arxiv.org/abs/2611.33640'>Sparse-to-Sparse Feature Learning for Cross-Layer Analysis and Steering</a></td><td>42</td><td>1</td><td>LG</td><td>SAE 교차 레이어 sparse feature 분석·steering, 해석 도구로 의미 있으나 robotics 간접적임</td></tr>
<tr><td>165</td><td><a href='https://arxiv.org/abs/2611.34492'>FlyingStart: Learned Cross-Token Warm Starts for Fixed-Point Decoding in Recurrent-Depth Language Models</a></td><td>42</td><td>0</td><td>NLP</td><td>recurrent-depth LM warm start로 고정점 디코딩 가속, 효율 추론임</td></tr>
<tr><td>166</td><td><a href='https://arxiv.org/abs/2611.33865'>Measuring the Value of One Shared Image at Robot Handoffs in Vision-and-Language Navigation</a></td><td>40</td><td>6</td><td>Navigation</td><td>VLN handoff에서 공유 이미지 한 장의 가치를 측정함, 분석 연구이나 범위 제한적임</td></tr>
<tr><td>167</td><td><a href='https://arxiv.org/abs/2611.34569'>Riding the Wave: Sim-to-Real Humanoid Control on Elastic Terrain</a></td><td>40</td><td>5</td><td>RL</td><td>탄성 지형 humanoid sim-to-real 제어로 응용 성격임</td></tr>
<tr><td>168</td><td><a href='https://arxiv.org/abs/2611.34597'>$μ$MPC: Microsecond-Scale Nonlinear and World Model Control from Edge to GPU via Koopman-Linearized Precompilation</a></td><td>40</td><td>5</td><td>World Model</td><td>Koopman 선형화로 world model MPC를 마이크로초로 가속함, 효율 기여이나 범용성은 확인 필요함</td></tr>
<tr><td>169</td><td><a href='https://arxiv.org/abs/2611.34849'>Real2SimLab: A Unified Platform for Real-to-Simulation Transfer</a></td><td>40</td><td>5</td><td>Embodied AI</td><td>real-to-sim 전이 통합 플랫폼으로 엔지니어링 성격임</td></tr>
<tr><td>170</td><td><a href='https://arxiv.org/abs/2611.34489'>Who Is Ego? Scaling Cross-View Camera Wearer Identification and Segmentation beyond Humans</a></td><td>40</td><td>4</td><td>CV</td><td>ego-exo 카메라 착용자 식별 확장으로 egocentric 이해에 일부 연관됨</td></tr>
<tr><td>171</td><td><a href='https://arxiv.org/abs/2611.33407'>An Adversarial Multi-Agent Pursuit Game for Locomotor Agility Pretraining</a></td><td>40</td><td>4</td><td>RL</td><td>adversarial pursuit game으로 humanoid locomotion 사전학습함, 응용 위주 개선임</td></tr>
<tr><td>172</td><td><a href='https://arxiv.org/abs/2611.34519'>AGLR: Attribute-Guided Latent Refinement for Fine-Grained Humanoid Motion Generation and Editing</a></td><td>40</td><td>4</td><td>Embodied AI</td><td>속성 가이드 latent refinement로 humanoid 모션 생성 편집함, 생성 기법 개선 성격임</td></tr>
<tr><td>173</td><td><a href='https://arxiv.org/abs/2611.34232'>OS-Omni: Benchmarking Generalist Computer-Using Agents on Long-Horizon Workflows Across Platforms</a></td><td>40</td><td>3</td><td>Embodied AI</td><td>플랫폼 횡단 장기 computer-use agent benchmark임</td></tr>
<tr><td>174</td><td><a href='https://arxiv.org/abs/2611.34810'>WorldExpand: Building Coherent 3D Worlds via Sparse Joint Panoramic Expansion</a></td><td>40</td><td>3</td><td>3D Vision</td><td>단일 파노라마에서 3D 월드 확장으로 시뮬레이션 환경 생성에 쓸 수 있음</td></tr>
<tr><td>175</td><td><a href='https://arxiv.org/abs/2611.33850'>Mitigating Overgeneralization in RND via Spectral Target Design</a></td><td>40</td><td>3</td><td>RL</td><td>RND 과일반화를 spectral target 설계로 완화함, 탐험 RL에 일부 연관됨</td></tr>
<tr><td>176</td><td><a href='https://arxiv.org/abs/2611.34466'>EgoUseBench: Benchmarking Computer-Use Agents under Evolving First-Person Contexts</a></td><td>40</td><td>3</td><td>Multimodal</td><td>1인칭 변화 context 하 computer-use agent benchmark, egocentric 요소 있음</td></tr>
<tr><td>177</td><td><a href='https://arxiv.org/abs/2611.33296'>CoSMo: A Compact Spectral Space of Body Motion in Video</a></td><td>40</td><td>2</td><td>Video</td><td>body motion의 compact spectral 표현이 참신하나 로봇 연결은 간접적임</td></tr>
<tr><td>178</td><td><a href='https://arxiv.org/abs/2611.33387'>Synchronizing Cameras via 3D Object Relationships</a></td><td>40</td><td>2</td><td>3D Vision</td><td>3D 객체 관계로 다중 카메라를 동기화하는 방식이 새로우나 응용이 좁음</td></tr>
<tr><td>179</td><td><a href='https://arxiv.org/abs/2611.33475'>Memory as the Backbone: A Dual-Store Associative Memory Architecture for Visual Recognition</a></td><td>40</td><td>2</td><td>Representation</td><td>dual-store associative memory 백본이 참신하나 인식 benchmark 중심임</td></tr>
<tr><td>180</td><td><a href='https://arxiv.org/abs/2611.33492'>EvOrderBench: When do sampled frames establish event order?</a></td><td>40</td><td>2</td><td>Video</td><td>샘플 프레임으로 사건 순서가 확정되는지 보는 benchmark로 시간 추론 진단임</td></tr>
<tr><td>181</td><td><a href='https://arxiv.org/abs/2611.33796'>SprintGS: Eliminating Redundancy for Fast 3D Gaussian Splatting Training</a></td><td>40</td><td>2</td><td>3D Vision</td><td>3DGS 학습 중복 제거 가속이며 engineering 성격임</td></tr>
<tr><td>182</td><td><a href='https://arxiv.org/abs/2611.34521'>PURA: Video Token Pruning via Unified Spatiotemporal Redundancy Assessment</a></td><td>40</td><td>2</td><td>Video</td><td>비디오 LLM 토큰 가지치기로 효율 개선 위주의 incremental 기여임</td></tr>
<tr><td>183</td><td><a href='https://arxiv.org/abs/2611.34680'>Neural Rendering Compiler: Generative Video Models as Programmable Renderers</a></td><td>40</td><td>2</td><td>Video</td><td>생성 비디오 모델을 프로그래머블 렌더러로 제어하는 인터페이스 제안함</td></tr>
<tr><td>184</td><td><a href='https://arxiv.org/abs/2611.34777'>When Every Rollout Fails: Splicing Learner-Conditioned Options into Long-Horizon Agent RL</a></td><td>40</td><td>2</td><td>RL</td><td>all-fail 그룹에서 option splicing으로 long-horizon agent RL을 개선함, LLM agent 대상이라 간접적임</td></tr>
<tr><td>185</td><td><a href='https://arxiv.org/abs/2611.33621'>Greedy Decoding Hides Good Plans: Sample-and-Verify Planning for Vision-Language Driving Models</a></td><td>40</td><td>2</td><td>Embodied AI</td><td>VLM 주행 플래닝에서 sample-and-verify로 greedy 한계를 보완함, 주행 도메인 한정임</td></tr>
<tr><td>186</td><td><a href='https://arxiv.org/abs/2611.34036'>Few-Shot Adaptation of Vision-Language Models via Agentic Model Editing</a></td><td>40</td><td>2</td><td>Multimodal</td><td>agentic model editing으로 VLM few-shot 적응, 적응 방법 incremental임</td></tr>
<tr><td>187</td><td><a href='https://arxiv.org/abs/2611.34112'>Not Every Input Needs Everything: Unifying Expert Gating, Model Cascades, and Agent Orchestration</a></td><td>40</td><td>2</td><td>LG</td><td>expert gating·cascade·agent 오케스트레이션을 통합해 입력별 적응 계산, 효율 추론 관점임</td></tr>
<tr><td>188</td><td><a href='https://arxiv.org/abs/2611.34635'>ZeroHero: Training Small Language Agents from Scratch</a></td><td>40</td><td>2</td><td>RL</td><td>처음부터 작은 언어 agent 학습, 상호작용 과제 학습 연구임</td></tr>
<tr><td>189</td><td><a href='https://arxiv.org/abs/2611.33339'>Temporal Weight Surgery: Repairing Video Grounding with LLM Editors</a></td><td>40</td><td>1</td><td>Multimodal</td><td>LLM이 가중치를 읽고 video grounding 오류를 수리하는 발상이 신선하나 적용 범위 좁음</td></tr>
<tr><td>190</td><td><a href='https://arxiv.org/abs/2611.34782'>Generation as Reverse Encoding</a></td><td>40</td><td>1</td><td>LG</td><td>표현에서 픽셀로의 역방향 생성 관점이나 로봇 연관 약함</td></tr>
<tr><td>191</td><td><a href='https://arxiv.org/abs/2611.34579'>Tune for Retention, Not Just Gain: SFT Forgets Far Less than You Think</a></td><td>40</td><td>1</td><td>NLP</td><td>SFT가 생각보다 덜 잊는다는 forgetting 분석이나 LLM 대상이라 로봇과는 간접적임</td></tr>
<tr><td>192</td><td><a href='https://arxiv.org/abs/2611.33919'>DiCALM: Converting Autoregressive Convolution-Attention Language Models into Discrete Diffusion Language Models</a></td><td>40</td><td>1</td><td>NLP</td><td>AR hybrid LM을 discrete diffusion으로 변환하는 recipe, 효율 아키텍처 관점임</td></tr>
<tr><td>193</td><td><a href='https://arxiv.org/abs/2611.34624'>HoMe: Toward Practical Harness Optimization of Memory Systems for AI Assistants</a></td><td>40</td><td>1</td><td>LG</td><td>AI assistant memory harness 최적화, memory 시스템 관점임</td></tr>
<tr><td>194</td><td><a href='https://arxiv.org/abs/2611.34183'>Lightweight Reasoning Transfer via Chain-of-Thought Vector Projection</a></td><td>40</td><td>0</td><td>NLP</td><td>CoT vector projection으로 작은 모델에 추론 전이, 가벼운 접근이나 범위 제한적임</td></tr>
<tr><td>195</td><td><a href='https://arxiv.org/abs/2611.34776'>DFly2: Turbocharging Long-Context Speculative Decoding by Sharing the Target&#x27;s Sparsity</a></td><td>40</td><td>0</td><td>NLP</td><td>sparse 모델 long-context speculative decoding 가속, 효율 추론임</td></tr>
<tr><td>196</td><td><a href='https://arxiv.org/abs/2611.34928'>Diverse Alternative Reasoning Traces for Hard Math Problems</a></td><td>40</td><td>0</td><td>NLP</td><td>어려운 수학 문제용 다양한 대안 추론 trace 생성, 추론 학습 기법임</td></tr>
<tr><td>197</td><td><a href='https://arxiv.org/abs/2611.33679'>Faster and Better Query (FBQ): Learning Future-Position Probes from the First Generated Token</a></td><td>40</td><td>0</td><td>LG</td><td>prefill 후 KV 제거를 위한 미래 위치 probe 학습, 효율 추론임</td></tr>
<tr><td>198</td><td><a href='https://arxiv.org/abs/2611.34328'>LUDIUS: A Benchmark for Embodied Social Intelligence in Everyday Human-Robot Interactions</a></td><td>38</td><td>5</td><td>Embodied AI</td><td>로봇의 사회 지능 벤치마크 LUDIUS로 평가 위주 기여임</td></tr>
<tr><td>199</td><td><a href='https://arxiv.org/abs/2611.34370'>MoCA4D: Monocular 3D Bounding Box Lifting and Tracking with Camera and Object Motion</a></td><td>38</td><td>4</td><td>3D Vision</td><td>단안 3D box 추적에서 카메라/객체 운동을 분리함</td></tr>
<tr><td>200</td><td><a href='https://arxiv.org/abs/2611.33705'>Lab2Sim: Agentic Generation of Interactive Laboratory Equipment from Operation Videos</a></td><td>38</td><td>4</td><td>Embodied AI</td><td>작동 영상에서 실험실 장비 sim asset을 agentic 생성함, 응용/asset 파이프라인임</td></tr>
<tr><td>201</td><td><a href='https://arxiv.org/abs/2611.33682'>WorldUAV: Scaling UAV Data Synthesis via World Models</a></td><td>38</td><td>3</td><td>World Model</td><td>world model로 UAV 학습 데이터를 합성하나 검출/추적 데이터 목적임</td></tr>
<tr><td>202</td><td><a href='https://arxiv.org/abs/2611.34544'>HAS: Hierarchical Adaptive Frame Sampling for Video Understanding</a></td><td>38</td><td>2</td><td>Video</td><td>비디오 MLLM용 계층적 프레임 샘플링으로 incremental임</td></tr>
<tr><td>203</td><td><a href='https://arxiv.org/abs/2611.34903'>ProbFaS: Probabilistic Video Frame Selection for MLLMs via Multi-Fidelity Calibration</a></td><td>38</td><td>2</td><td>Video</td><td>MLLM용 확률적 프레임 선택으로 incremental임</td></tr>
<tr><td>204</td><td><a href='https://arxiv.org/abs/2611.34132'>Agent-as-a-Verifier: From Scores to Evidence for General Verification</a></td><td>38</td><td>2</td><td>NLP</td><td>에이전트 기반 검증자로 점수 대신 근거를 제공함, test-time 검증에 연관됨</td></tr>
<tr><td>205</td><td><a href='https://arxiv.org/abs/2611.33176'>Psychophysics of Duration Perception in Multimodal Large Language Models</a></td><td>38</td><td>2</td><td>Multimodal</td><td>MLLM의 지속시간 인지를 psychophysics로 분석함, 진단 성격이고 robotics 연결 약함</td></tr>
<tr><td>206</td><td><a href='https://arxiv.org/abs/2611.33268'>JetDiffusion: Pushing the Speed Limits of Video Generation with NVFP4 Sparse Attention</a></td><td>38</td><td>1</td><td>Video</td><td>NVFP4 sparse attention 기반 영상 생성 가속으로 효율 추론 측면만 있음</td></tr>
<tr><td>207</td><td><a href='https://arxiv.org/abs/2611.33388'>Measuring and Predicting Image-Token Repair Boundaries in Vision-Language Models</a></td><td>38</td><td>1</td><td>Multimodal</td><td>VLM의 image token 복구 경계 분석이며 로봇 연관 약함</td></tr>
<tr><td>208</td><td><a href='https://arxiv.org/abs/2611.33903'>RelPRM: Grounding Visual Process Reward Models in Relational Evidence</a></td><td>38</td><td>1</td><td>Multimodal</td><td>관계 증거에 기반한 visual PRM이며 도메인 일반임</td></tr>
<tr><td>209</td><td><a href='https://arxiv.org/abs/2611.34220'>Variation-aware Temporal Correspondence for Self-Supervised Video Representation Learning</a></td><td>38</td><td>1</td><td>Video</td><td>variation 고려 시간 대응 비디오 표현 학습으로 일부 일반적임</td></tr>
<tr><td>210</td><td><a href='https://arxiv.org/abs/2611.34941'>Improving and Expanding Video Editing Capabilities Without Videos</a></td><td>38</td><td>1</td><td>Video</td><td>비디오 없이 비디오 편집 능력을 확장하는 학습 방식임</td></tr>
<tr><td>211</td><td><a href='https://arxiv.org/abs/2611.34703'>Maco-RL: Scaling Agent Capabilities with Mixed-Task Reinforcement Learning</a></td><td>38</td><td>1</td><td>RL</td><td>LLM agent용 mixed-task RL 스케일링으로 로봇 관련성 약함</td></tr>
<tr><td>212</td><td><a href='https://arxiv.org/abs/2611.34147'>Letting Models Manage Their Own Context: Where We Stand</a></td><td>38</td><td>1</td><td>LG</td><td>모델이 자기 context를 관리하는 현황 정리, position 성격임</td></tr>
<tr><td>213</td><td><a href='https://arxiv.org/abs/2611.34400'>EvoLink-Bench: A Benchmark for Evaluating Self-Evolving Agents in Long-Horizon Interdependent Task Streams</a></td><td>38</td><td>1</td><td>LG</td><td>장기 상호의존 환경 self-evolving agent benchmark임</td></tr>
<tr><td>214</td><td><a href='https://arxiv.org/abs/2611.34841'>Knowledge-Base Gradient Descent: Self-Structuring Learning through Question Answering</a></td><td>38</td><td>1</td><td>LG</td><td>질문 응답으로 knowledge base 자기 구조화하는 gradient descent식 학습임</td></tr>
<tr><td>215</td><td><a href='https://arxiv.org/abs/2611.33823'>Pitfalls of Dependency-Ready Decoding for Masked Diffusion Language Models</a></td><td>38</td><td>0</td><td>NLP</td><td>masked diffusion LM 디코딩 함정 분석, 일반 생성 연구임</td></tr>
<tr><td>216</td><td><a href='https://arxiv.org/abs/2611.33943'>What Does Skill Lift Actually Measure? A Source-Code-Level Audit and Noise-Aware Reanalysis of SkillsBench</a></td><td>38</td><td>0</td><td>LG</td><td>agent skill lift 측정 감사, 평가 방법 연구임</td></tr>
<tr><td>217</td><td><a href='https://arxiv.org/abs/2611.33880'>Integration of Vision-Language-Action Control for Autonomous Forklift Unloading with Limited Real-World Data</a></td><td>35</td><td>6</td><td>VLA</td><td>제한된 실데이터로 forklift 하역에 VLA를 적용함, 응용 중심임</td></tr>
<tr><td>218</td><td><a href='https://arxiv.org/abs/2611.34020'>Ask to Land: Learning a Mask-Conditioned Open-Vocabulary Landing Policy via Differentiable Physics</a></td><td>35</td><td>4</td><td>Navigation</td><td>mask 조건 open-vocabulary 드론 착륙 policy를 differentiable physics로 학습함, 응용 위주임</td></tr>
<tr><td>219</td><td><a href='https://arxiv.org/abs/2611.34764'>Anytime-Valid Sequential Verification for Sensing-Efficient Robot Navigation under Perception Uncertainty</a></td><td>35</td><td>4</td><td>Navigation</td><td>anytime-valid 순차 검증으로 감지 효율 navigation을 제안함, 그리드 설정 위주임</td></tr>
<tr><td>220</td><td><a href='https://arxiv.org/abs/2611.34925'>One Ocean, Many Tasks: A Data-Grounded Simulation Suite and Benchmark for Marine Robotics</a></td><td>35</td><td>4</td><td>Embodied AI</td><td>해양 로봇 시뮬레이션 벤치마크로 도메인 특화 스위트임</td></tr>
<tr><td>221</td><td><a href='https://arxiv.org/abs/2611.33654'>Fine-Grained Ego-Vehicle Action Recognition from Driving Video</a></td><td>35</td><td>3</td><td>CV</td><td>주행 영상 ego 행동 인식으로 dataset 중심임</td></tr>
<tr><td>222</td><td><a href='https://arxiv.org/abs/2611.34084'>TaCo: Rethinking Correlation for Visual Tracking on Edge Devices</a></td><td>35</td><td>3</td><td>CV</td><td>edge 기기용 tracker에서 attention을 correlation으로 되돌리는 효율 설계임</td></tr>
<tr><td>223</td><td><a href='https://arxiv.org/abs/2611.34121'>Unstable Action Boundaries in Lethal Drone Agents</a></td><td>35</td><td>3</td><td>Embodied AI</td><td>도구 사용 LLM 에이전트의 드론 행동 경계 불안정성 안전 평가임</td></tr>
<tr><td>224</td><td><a href='https://arxiv.org/abs/2611.34136'>SOC-Net: Second-Order-Cone-Constrained Neural Networks</a></td><td>35</td><td>3</td><td>LG</td><td>2차 원뿔 제약 신경망으로 안전 제약 제어에 일부 연관됨</td></tr>
<tr><td>225</td><td><a href='https://arxiv.org/abs/2611.33462'>FoamSurf: A Voronoi-Surfel Representation for Differentiable Rendering</a></td><td>35</td><td>2</td><td>3D Vision</td><td>산란 매질용 Voronoi-surfel 미분 렌더링이며 수중 로봇 정도에 연결됨</td></tr>
<tr><td>226</td><td><a href='https://arxiv.org/abs/2611.33507'>Separating Environment and Sensor Shift from Acquisition Protocol in Physical Vision Benchmarks</a></td><td>35</td><td>2</td><td>CV</td><td>물리 vision benchmark에서 환경/센서 shift와 획득 protocol 분리 분석임</td></tr>
<tr><td>227</td><td><a href='https://arxiv.org/abs/2611.34005'>ScaleCurve: From Constant Scale to Consistent Motion for World-Space Human Mesh Recovery</a></td><td>35</td><td>2</td><td>3D Vision</td><td>world-space 인체 mesh 복원의 scale 일관성 개선임</td></tr>
<tr><td>228</td><td><a href='https://arxiv.org/abs/2611.34022'>MoSk: A Unified Motion-Skeleton Foundation Model for Human Motion Understanding and Generation</a></td><td>35</td><td>2</td><td>Generative</td><td>motion-skeleton 통합 foundation model로 인간 모션 이해/생성함</td></tr>
<tr><td>229</td><td><a href='https://arxiv.org/abs/2611.34100'>When Position Favors the Wrong Part: Evaluating Left-Right Discrimination in Semantic Correspondence</a></td><td>35</td><td>2</td><td>CV</td><td>semantic correspondence의 좌우 구분 실패 평가로 진단 가치는 있음</td></tr>
<tr><td>230</td><td><a href='https://arxiv.org/abs/2611.34457'>ProxyGenBench: Benchmarking Proxy-Guided Video Generation</a></td><td>35</td><td>2</td><td>Video</td><td>proxy 유도 영상 생성 benchmark로 제어 평가임</td></tr>
<tr><td>231</td><td><a href='https://arxiv.org/abs/2611.34461'>SceneDesigner++: A Unified 9-DoF Pose Control Framework for T2I and T2V Generation</a></td><td>35</td><td>2</td><td>CV</td><td>T2I/T2V 9-DoF 포즈 제어 통합 프레임워크로 생성 제어 중심이며 로봇 연결 약함</td></tr>
<tr><td>232</td><td><a href='https://arxiv.org/abs/2611.34912'>LiveVAE: Causal Window Attention Makes Efficient Streaming Video VAE</a></td><td>35</td><td>2</td><td>Video</td><td>스트리밍 비디오 VAE를 인과 window attention으로 효율화하는 엔지니어링임</td></tr>
<tr><td>233</td><td><a href='https://arxiv.org/abs/2611.34944'>AnyCam: Anything Can Represent Camera for Video Generation</a></td><td>35</td><td>2</td><td>Video</td><td>카메라 표현 일반화 기반 카메라 제어 비디오 생성임</td></tr>
<tr><td>234</td><td><a href='https://arxiv.org/abs/2611.33184'>Semantic Density Does Not Predict Agent-Memory Collapse</a></td><td>35</td><td>2</td><td>LG</td><td>LLM 에이전트 메모리 붕괴 예측 여부 실증으로 memory 연관은 약함</td></tr>
<tr><td>235</td><td><a href='https://arxiv.org/abs/2611.34826'>Gradient TD($λ$) for Non-Linear Function Approximation</a></td><td>35</td><td>2</td><td>RL</td><td>non-linear 근사용 gradient TD(lambda) 이론으로 RL 기초 연구임</td></tr>
<tr><td>236</td><td><a href='https://arxiv.org/abs/2611.33793'>LSRP*-LA: Scalable and Anytime Multi-Agent Path Finding for Large Agents with Asynchronous Actions</a></td><td>35</td><td>2</td><td>Navigation</td><td>큰 agent용 anytime MAPF 알고리즘으로 고전 플래닝 위주임</td></tr>
<tr><td>237</td><td><a href='https://arxiv.org/abs/2611.33777'>Agentic Reinforcement Learning with Immediate and Prospective Credit Assignment for Medical Visual Reasoning</a></td><td>35</td><td>1</td><td>RL</td><td>의료 VQA agentic RL의 credit assignment이며 도메인 한정임</td></tr>
<tr><td>238</td><td><a href='https://arxiv.org/abs/2611.33808'>EvoVAU: Tool Evolution for Video Anomaly Understanding</a></td><td>35</td><td>1</td><td>Video</td><td>비디오 이상 이해에 tool evolution을 쓰는 agent이며 로봇 연관 약함</td></tr>
<tr><td>239</td><td><a href='https://arxiv.org/abs/2611.33861'>OmniMeld: Enhancing Audio-Visual Understanding via Multi-Teacher On-Policy Distillation</a></td><td>35</td><td>1</td><td>Multimodal</td><td>멀티 teacher on-policy 증류로 audio-visual 이해를 개선하는 incremental 연구임</td></tr>
<tr><td>240</td><td><a href='https://arxiv.org/abs/2611.34056'>Understanding Diffusion Acceleration: Methods, Trade-Offs, and Open Questions</a></td><td>35</td><td>1</td><td>Generative</td><td>diffusion 가속 기법 survey로 정리 가치는 있으나 새 방법은 아님</td></tr>
<tr><td>241</td><td><a href='https://arxiv.org/abs/2611.34105'>What Makes a Gavagai? Learning Visual Concepts from One Positive and Few Negatives</a></td><td>35</td><td>1</td><td>CV</td><td>양성 하나와 소수 음성으로 시각 개념을 배우는 문제 설정임</td></tr>
<tr><td>242</td><td><a href='https://arxiv.org/abs/2611.34252'>Detector Operating Behavior Inference via Data-Space Sampling</a></td><td>35</td><td>1</td><td>CV</td><td>검출기 operating behavior를 추정하는 이차 추론 문제 설정이 참신함</td></tr>
<tr><td>243</td><td><a href='https://arxiv.org/abs/2611.33302'>Two Timescales of Forgetting in Fine-tuning of Language Models: Fast Behavioral Suppression and Slow Representational Drift</a></td><td>35</td><td>1</td><td>NLP</td><td>LLM fine-tuning 망각의 두 시간 척도 분석으로 continual 관점 참고됨</td></tr>
<tr><td>244</td><td><a href='https://arxiv.org/abs/2611.34363'>Single-Database Rewards Are Hackable: Counterfactual Execution for Trustworthy Text-to-SQL RL</a></td><td>35</td><td>1</td><td>RL</td><td>text-to-SQL RL에서 counterfactual execution으로 reward hacking을 줄임, 로봇과는 거리 있음</td></tr>
<tr><td>245</td><td><a href='https://arxiv.org/abs/2611.34746'>BRIAR: Martingale Belief Smoothing on Bifurcation-Guided Reasoning Trees</a></td><td>35</td><td>1</td><td>RL</td><td>RLVR reasoning tree에서 credit 배분을 개선하나 LLM 추론 중심임</td></tr>
<tr><td>246</td><td><a href='https://arxiv.org/abs/2611.33848'>ChemDeduce: Benchmarking LLMs for Unknown Chemical Identification through Interactive Simulated Experiments</a></td><td>35</td><td>1</td><td>NLP</td><td>상호작용 시뮬레이션으로 미지 화학물질 식별 LLM benchmark, 능동 탐색 요소 약간 있음</td></tr>
<tr><td>247</td><td><a href='https://arxiv.org/abs/2611.33394'>Confidence scores for gated automation of large language models</a></td><td>35</td><td>1</td><td>LG</td><td>LLM 자동화 게이트용 confidence score, 신뢰도 보정 연구임</td></tr>
<tr><td>248</td><td><a href='https://arxiv.org/abs/2611.33402'>Partial Routing: Trace-Tuned Delegation for Resource-Efficient Agentic Workflows</a></td><td>35</td><td>1</td><td>LG</td><td>agent workflow 부분 라우팅으로 비용 절감, 엔지니어링 성격임</td></tr>
<tr><td>249</td><td><a href='https://arxiv.org/abs/2611.33707'>P-FedSkill: A Personalized Federated Skill Learning Framework under Task Heterogeneity</a></td><td>35</td><td>1</td><td>LG</td><td>개인화 federated skill 학습, agent skill 관점이나 일반적임</td></tr>
<tr><td>250</td><td><a href='https://arxiv.org/abs/2611.34093'>Exploring the Design Factors of Pixel-space Diffusion</a></td><td>35</td><td>0</td><td>Generative</td><td>pixel-space diffusion 설계 요소 탐색이며 로봇 연관 약함</td></tr>
<tr><td>251</td><td><a href='https://arxiv.org/abs/2611.34923'>Mixture-of-Loops Transformer</a></td><td>35</td><td>0</td><td>NLP</td><td>Mixture-of-Loops Transformer로 looped LM 효율 개선이며 로봇과 무관함</td></tr>
<tr><td>252</td><td><a href='https://arxiv.org/abs/2611.33676'>Interactive Proofs as a Unified Framework for Evaluating and Leveraging Verifiable Proof Generation by LLM Agents</a></td><td>35</td><td>0</td><td>LG</td><td>검증 가능 증명을 interactive proof로 통합, 이론 프레임이나 robotics 무관함</td></tr>
<tr><td>253</td><td><a href='https://arxiv.org/abs/2611.33760'>GlassGround: GUI Grounding Beyond Native Screenshots with Egocentric Wearable Vision</a></td><td>33</td><td>2</td><td>Multimodal</td><td>웨어러블 시점 GUI grounding benchmark임</td></tr>
<tr><td>254</td><td><a href='https://arxiv.org/abs/2611.34515'>Decoder-as-a-Probe: Verbalizing and Steering Visual Representations in LVLMs</a></td><td>33</td><td>2</td><td>Multimodal</td><td>LVLM 시각 표현 해석 및 steering 연구로 해석성 위주임</td></tr>
<tr><td>255</td><td><a href='https://arxiv.org/abs/2611.34351'>Inverse Reinforcement Learning with State-Dependent Foresight for Human Decision-Making</a></td><td>33</td><td>2</td><td>RL</td><td>상태 의존 foresight를 둔 IRL로 인간 행동 모델링에 초점을 둠</td></tr>
<tr><td>256</td><td><a href='https://arxiv.org/abs/2611.33725'>VTK-Bench: A Diagnostic Benchmark for Distinguishing Language Priors and Text Modal Bias in Visual Language Models</a></td><td>33</td><td>1</td><td>Multimodal</td><td>VLM 언어 prior와 텍스트 편향 진단 benchmark임</td></tr>
<tr><td>257</td><td><a href='https://arxiv.org/abs/2611.34576'>Procedure Inference as Memory: Learning Recruiter Decision Procedures from OKF-Structured Episodes in Multi-Session Hiring Assistants</a></td><td>33</td><td>1</td><td>LG</td><td>절차 추론을 memory로 보는 채용 assistant, 응용임</td></tr>
<tr><td>258</td><td><a href='https://arxiv.org/abs/2611.33261'>Same Tokenizer, Better Tokens: Choosing Image Tokens by MAP Inference</a></td><td>33</td><td>0</td><td>Generative</td><td>VQ 토큰을 MAP 추론으로 고르는 tokenizer 개선이며 로봇 연관 약함</td></tr>
<tr><td>259</td><td><a href='https://arxiv.org/abs/2611.33414'>Beyond Random Starts: Amortized Initialization for Adversarial Attacks on Vision-Language Models</a></td><td>33</td><td>0</td><td>Multimodal</td><td>VLM 적대 공격의 amortized 초기화로 로봇 연관 약함</td></tr>
<tr><td>260</td><td><a href='https://arxiv.org/abs/2611.33197'>Extraneous Cognitive Load in Large Language Models</a></td><td>33</td><td>0</td><td>NLP</td><td>LLM extraneous load 분석, 현상 보고 위주임</td></tr>
<tr><td>261</td><td><a href='https://arxiv.org/abs/2611.33250'>Focus On Facts: Stylistically Invariant and Factually Sensitive Text Embeddings</a></td><td>33</td><td>0</td><td>NLP</td><td>사실 민감 text embedding 학습, 소규모 개선임</td></tr>
<tr><td>262</td><td><a href='https://arxiv.org/abs/2611.33692'>Rethinking Sequential Locate-Then-Edit: Optimality and Stability</a></td><td>33</td><td>0</td><td>NLP</td><td>순차 locate-then-edit 최적성 분석, 지식 편집 연구임</td></tr>
<tr><td>263</td><td><a href='https://arxiv.org/abs/2611.34188'>MINE: A Training-Free Defense against Indirect Prompt Injection via Mutual Information and Embedding Variance</a></td><td>33</td><td>0</td><td>NLP</td><td>mutual information 기반 prompt injection 방어, 보안 응용임</td></tr>
<tr><td>264</td><td><a href='https://arxiv.org/abs/2611.34373'>Under the Influence -- of What? A Controlled Evaluation of Influence Functions</a></td><td>33</td><td>0</td><td>NLP</td><td>influence function 통제 평가, 분석 연구임</td></tr>
<tr><td>265</td><td><a href='https://arxiv.org/abs/2611.34725'>Bigger Model or Bigger Table? How Much Backbone a Chorus N-gram Module Replaces</a></td><td>33</td><td>0</td><td>NLP</td><td>n-gram table이 backbone을 얼마나 대체하는지 분석임</td></tr>
<tr><td>266</td><td><a href='https://arxiv.org/abs/2611.33161'>Constraint-Aware Test-Time Scoring for LLM and VLM Candidate Selection</a></td><td>33</td><td>0</td><td>LG</td><td>제약 인지 test-time 후보 선택, 작은 점수화 기법임</td></tr>
<tr><td>267</td><td><a href='https://arxiv.org/abs/2611.33757'>TransHarness: From Benchmark Overfitting to Transferable Harness Evolution</a></td><td>33</td><td>0</td><td>LG</td><td>coding agent harness 진화의 전이성, 평가 중심임</td></tr>
<tr><td>268</td><td><a href='https://arxiv.org/abs/2611.33897'>EATS: Scaling Tool-Use Experience for Medical Reasoning Agents</a></td><td>33</td><td>0</td><td>LG</td><td>의료 추론 agent tool-use 경험 scaling, 응용임</td></tr>
<tr><td>269</td><td><a href='https://arxiv.org/abs/2611.33909'>EGSE: Evidence-Grounded Skill Evolution for Medical Reasoning Agents</a></td><td>33</td><td>0</td><td>LG</td><td>의료 agent 증거 기반 skill 진화, 응용임</td></tr>
<tr><td>270</td><td><a href='https://arxiv.org/abs/2611.34215'>PROVE: Mitigating Long-Horizon LLM Collusion with Reinforcement Learning from Verified Evidence</a></td><td>33</td><td>0</td><td>RL</td><td>장기 LLM 담합을 검증 가능 보상 RL로 완화함</td></tr>
<tr><td>271</td><td><a href='https://arxiv.org/abs/2611.34327'>MeterRouter: Budget-Aware Dynamic Routing for Multi-Agent Systems</a></td><td>33</td><td>0</td><td>LG</td><td>multi-agent 예산 인지 라우팅임</td></tr>
<tr><td>272</td><td><a href='https://arxiv.org/abs/2611.34287'>DataForgeVLA: Fully Synthetic Manipulation Demonstrations for Vision-Language-Action Training</a></td><td>32</td><td>7</td><td>VLA</td><td>합성 데모 340개 데이터셋으로 규모가 작은 데이터 기여임</td></tr>
<tr><td>273</td><td><a href='https://arxiv.org/abs/2611.34155'>OceanFix: Reference-Guided Diffusion for Sparse-View Underwater 3D Reconstruction</a></td><td>32</td><td>2</td><td>3D Vision</td><td>수중 sparse-view 3DGS 보정으로 응용 특화임</td></tr>
<tr><td>274</td><td><a href='https://arxiv.org/abs/2611.34601'>You Only Look Multiple Times: YoloMT, a Real-Time Streaming Model on a T4</a></td><td>32</td><td>2</td><td>Video</td><td>T4 단일 GPU 실시간 스트리밍 캡셔너로 엔지니어링 위주임</td></tr>
<tr><td>275</td><td><a href='https://arxiv.org/abs/2611.34863'>Focus Only on What&#x27;s Important: Training-Free Focus Maps for Frozen Vision Transformers in Long-Video Object Segmentation</a></td><td>32</td><td>2</td><td>CV</td><td>ViT 학습 불필요 focus map으로 장기 비디오 객체 분할 효율화함</td></tr>
<tr><td>276</td><td><a href='https://arxiv.org/abs/2611.33716'>Flipping the Coins: Training Physical Simulators through Hard Switches</a></td><td>32</td><td>2</td><td>LG</td><td>hybrid 물리 시뮬레이터를 hard switch로 학습함, 시뮬레이션 연관됨</td></tr>
<tr><td>277</td><td><a href='https://arxiv.org/abs/2611.34678'>Provably Efficient Concave Utility Reinforcement Learning with Linear Function Approximation</a></td><td>32</td><td>2</td><td>RL</td><td>concave utility RL의 선형 근사 이론 결과로 imitation 포함하나 이론 중심임</td></tr>
<tr><td>278</td><td><a href='https://arxiv.org/abs/2611.34723'>Robust Recourse under Causal Graph Ambiguity</a></td><td>32</td><td>2</td><td>LG</td><td>causal graph 모호성 하의 robust recourse로 counterfactual 추론 이론이나 로봇과는 거리 있음</td></tr>
<tr><td>279</td><td><a href='https://arxiv.org/abs/2611.34840'>Provably Efficient Offline Discounted Reinforcement Learning under Recursive Entropic Risk</a></td><td>32</td><td>2</td><td>RL</td><td>재귀 entropic risk 하의 offline RL 이론 보장으로 이론 중심임</td></tr>
<tr><td>280</td><td><a href='https://arxiv.org/abs/2611.33722'>Practice Makes Fluent: Learning to Use Earlier Predictions in Looped Models</a></td><td>32</td><td>2</td><td>LG</td><td>looped model이 앞선 예측을 쓰도록 학습해 early exit을 얻음, 로봇 연결 약함</td></tr>
<tr><td>281</td><td><a href='https://arxiv.org/abs/2611.34403'>Recoverability policy editing for closed-loop safety in autonomous driving</a></td><td>32</td><td>2</td><td>RL</td><td>주행 policy 편집으로 복구 가능 교란 하 안전 보장함, 로봇 manipulation과는 거리 있음</td></tr>
<tr><td>282</td><td><a href='https://arxiv.org/abs/2611.33498'>A 3D Simulator for Passive SPAD Imaging</a></td><td>32</td><td>1</td><td>CV</td><td>passive SPAD 3D 시뮬레이터로 특수 센서 데이터 생성임</td></tr>
<tr><td>283</td><td><a href='https://arxiv.org/abs/2611.34162'>Modality-Shift Contrastive Decoding for Temporally Grounded Audio-Visual Understanding</a></td><td>32</td><td>1</td><td>Multimodal</td><td>AV-LLM 시간 정합 contrastive decoding이며 incremental함</td></tr>
<tr><td>284</td><td><a href='https://arxiv.org/abs/2611.34657'>Counting Beyond Frames: Codec Motion Tells Frozen Diffusion VLMs How Many</a></td><td>32</td><td>1</td><td>Video</td><td>코덱 모션을 이용한 비디오 카운팅으로 로봇 연관 약함</td></tr>
<tr><td>285</td><td><a href='https://arxiv.org/abs/2611.33257'>One Token, Many Lessons: Sliding-Window Attention within Gated Delta Networks</a></td><td>32</td><td>1</td><td>LG</td><td>Gated Delta Network에 sliding-window attention 결합한 시퀀스 모델임</td></tr>
<tr><td>286</td><td><a href='https://arxiv.org/abs/2611.33399'>Sequentially Acquiring Concept Knowledge to Guide Continual Learning</a></td><td>32</td><td>1</td><td>LG</td><td>개념 지식을 순차 획득하는 continual learning으로 일반 방법임</td></tr>
<tr><td>287</td><td><a href='https://arxiv.org/abs/2611.33625'>State Space Attention: Learning Context-Dependent Memory Retention</a></td><td>32</td><td>1</td><td>LG</td><td>context 의존 메모리 유지를 학습하는 state space attention임</td></tr>
<tr><td>288</td><td><a href='https://arxiv.org/abs/2611.33594'>Aligned Machine: A Benchmark for Evaluating Multimodal Embedding Similarity via Human Comparative Judgements</a></td><td>32</td><td>1</td><td>Multimodal</td><td>멀티모달 embedding 유사도의 인간 정렬 benchmark임</td></tr>
<tr><td>289</td><td><a href='https://arxiv.org/abs/2611.33315'>Large-scale Model Merging via Recovery-aware Task Weighting</a></td><td>32</td><td>0</td><td>LG</td><td>model merging 가중치 조정으로 incremental함</td></tr>
<tr><td>290</td><td><a href='https://arxiv.org/abs/2611.33580'>LLMVC: Large Language Model-Guided Generative Video Compression</a></td><td>32</td><td>0</td><td>Video</td><td>LLM 유도 생성형 영상 압축이며 로봇 연관 약함</td></tr>
<tr><td>291</td><td><a href='https://arxiv.org/abs/2611.33761'>ScanAR: Parallel Row-Scan Decoding for Efficient Image Generation in Unified Autoregressive Models</a></td><td>32</td><td>0</td><td>Generative</td><td>unified AR 모델의 병렬 row-scan 디코딩 가속임</td></tr>
<tr><td>292</td><td><a href='https://arxiv.org/abs/2611.33895'>TWIST: Teacher-Weighted Initial-Noise Spherical Transform for Quality-Preserving Diversity in Distilled Diffusion Models</a></td><td>32</td><td>0</td><td>Generative</td><td>증류 diffusion의 다양성 복원이며 incremental함</td></tr>
<tr><td>293</td><td><a href='https://arxiv.org/abs/2611.34261'>TORE: Token-Wise Taylor Order Selection via Decomposed Residual Error Estimation for Diffusion Acceleration</a></td><td>32</td><td>0</td><td>Generative</td><td>diffusion Taylor order 선택 가속이며 incremental함</td></tr>
<tr><td>294</td><td><a href='https://arxiv.org/abs/2611.34839'>Diffusion Steering via Adaptive Reward Estimation and Resampling</a></td><td>32</td><td>0</td><td>Generative</td><td>T2I 확산 steering을 보상 추정으로 수행하나 로봇 무관함</td></tr>
<tr><td>295</td><td><a href='https://arxiv.org/abs/2611.34276'>Scaling Looped MoE Language Models under Matched Budgets: Information Flow and Parameter Allocation</a></td><td>32</td><td>0</td><td>NLP</td><td>looped MoE LM의 예산 대비 설계 원칙 연구로 로봇 관련성 없음</td></tr>
<tr><td>296</td><td><a href='https://arxiv.org/abs/2611.34877'>Towards Closing the Performance Gap in Cross-Modal Place Recognition</a></td><td>30</td><td>3</td><td>CV</td><td>언어 기반 cross-modal place recognition 성능 격차 축소로 incremental임</td></tr>
<tr><td>297</td><td><a href='https://arxiv.org/abs/2611.34453'>DynaRC: Dynamics-Robust 4-D Radar Relocalization with Rate-Adaptive Sequence Matching</a></td><td>30</td><td>3</td><td>Navigation</td><td>4D radar relocalization으로 SLAM 응용임</td></tr>
<tr><td>298</td><td><a href='https://arxiv.org/abs/2611.34027'>ContextHands: Completing Hand Motion with Learned Context and Joint-Specific Body Kinematics</a></td><td>30</td><td>2</td><td>Generative</td><td>body kinematics 기반 손 모션 완성이며 incremental함</td></tr>
<tr><td>299</td><td><a href='https://arxiv.org/abs/2611.33527'>Casper: A Projection-Based Neurosymbolic Layer for Scalable &amp; Guaranteed Constraint Satisfaction</a></td><td>30</td><td>2</td><td>LG</td><td>투영 기반 neurosymbolic 레이어로 제약 만족 보장함, 안전 제어에 일부 연관됨</td></tr>
<tr><td>300</td><td><a href='https://arxiv.org/abs/2611.34818'>Deep Reinforcement Learning for Multi-UAV Data Harvesting Under Variable Team Sizes and Agent Loss</a></td><td>30</td><td>2</td><td>RL</td><td>가변 팀 크기와 agent 손실에 강한 multi-UAV RL이나 응용 위주임</td></tr>
<tr><td>301</td><td><a href='https://arxiv.org/abs/2611.33409'>A Semantics-First Approach to Multimodal Video Captioning with Frozen Encoders and Stabilized Reinforcement Learning</a></td><td>30</td><td>1</td><td>Multimodal</td><td>오디오-비주얼 captioning 모델과 SCST 안정화로 incremental함</td></tr>
<tr><td>302</td><td><a href='https://arxiv.org/abs/2611.33532'>AVERT: Anomalous Value Erasure with Response Testing against Visual Prompt Injection</a></td><td>30</td><td>1</td><td>Multimodal</td><td>VLM visual prompt injection 방어이며 안전성 측면만 있음</td></tr>
<tr><td>303</td><td><a href='https://arxiv.org/abs/2611.33756'>Show Me the Change You Want: Visual Example-Guided Change Detection</a></td><td>30</td><td>1</td><td>CV</td><td>예시 기반 change detection이며 incremental함</td></tr>
<tr><td>304</td><td><a href='https://arxiv.org/abs/2611.33842'>SPiXSeg: Rethinking MLLM-based Image Segmentation as Superpixel Classification</a></td><td>30</td><td>1</td><td>CV</td><td>MLLM segmentation을 superpixel 분류로 재정의하나 incremental함</td></tr>
<tr><td>305</td><td><a href='https://arxiv.org/abs/2611.33885'>LayoutRecall: Preserving Appearance in Multi-Round 3D Layout-Controlled Image Editing</a></td><td>30</td><td>1</td><td>Generative</td><td>다회 3D layout 편집에서 외형 보존 기법이며 incremental함</td></tr>
<tr><td>306</td><td><a href='https://arxiv.org/abs/2611.34598'>SEAM: A Self-Evolving and Adaptive Probing Framework for Automatic MLLM Hallucination Evaluation</a></td><td>30</td><td>1</td><td>Multimodal</td><td>MLLM 환각 자동 평가 프레임워크로 벤치마크 성격임</td></tr>
<tr><td>307</td><td><a href='https://arxiv.org/abs/2611.33308'>Change Partners at Every Layer: Balanced Random Regrouping for Model Merging</a></td><td>30</td><td>1</td><td>LG</td><td>모델 병합 레이어별 그룹 재분할로 incremental임</td></tr>
<tr><td>308</td><td><a href='https://arxiv.org/abs/2611.33487'>The Geometry Is the Memory: Task-Density Routing for Continual LoRA</a></td><td>30</td><td>1</td><td>LG</td><td>continual LoRA의 task-density 라우팅으로 어댑터 선택 방법임</td></tr>
<tr><td>309</td><td><a href='https://arxiv.org/abs/2611.33827'>FEAST: Fair and Efficient Adaptive Sampling for Task-Free On-Policy Learning</a></td><td>30</td><td>1</td><td>RL</td><td>언어 에이전트 on-policy 학습의 rollout 예산 적응 샘플링임</td></tr>
<tr><td>310</td><td><a href='https://arxiv.org/abs/2611.33939'>CondUQ: Calibrated Conditional Uncertainty Quantification Using Distribution Matching</a></td><td>30</td><td>1</td><td>LG</td><td>분포 매칭 기반 조건부 불확실성 정량화로 안전 응용에 일부 활용됨</td></tr>
<tr><td>311</td><td><a href='https://arxiv.org/abs/2611.34767'>When to Trust a PFN: Detecting Harmful Shift in Tabular Foundation Models</a></td><td>30</td><td>1</td><td>LG</td><td>tabular PFN의 해로운 분포 shift 탐지로 failure 감지 아이디어는 있으나 tabular 한정임</td></tr>
<tr><td>312</td><td><a href='https://arxiv.org/abs/2611.34690'>PoVi: Agentic Poetry-to-Video Generation with Knowledge Grounding and Figurative Understanding</a></td><td>30</td><td>1</td><td>Video</td><td>시를 영상으로 만드는 agentic 생성, 응용 파이프라인임</td></tr>
<tr><td>313</td><td><a href='https://arxiv.org/abs/2611.34920'>$μ$-Bench: Benchmarking Multi-User Task Completion in Shared Interaction Voice Agents</a></td><td>30</td><td>1</td><td>NLP</td><td>다중 사용자 voice agent benchmark, 공유 공간 상호작용 요소 있음</td></tr>
<tr><td>314</td><td><a href='https://arxiv.org/abs/2611.33190'>General-Purpose Decision Models for AI Configuration Tuning</a></td><td>30</td><td>1</td><td>LG</td><td>AI 설정 튜닝용 범용 decision model, 응용 성격임</td></tr>
<tr><td>315</td><td><a href='https://arxiv.org/abs/2611.33818'>Spectral Optimal Transport for Dynamics-Aware Sign Language Generation</a></td><td>30</td><td>1</td><td>Video</td><td>spectral optimal transport 수어 생성, pose 생성 응용임</td></tr>
<tr><td>316</td><td><a href='https://arxiv.org/abs/2611.33252'>MonoQPM: Splitting Features into Concepts for Inherent Interpretability and Predictive Performance</a></td><td>30</td><td>0</td><td>CV</td><td>개념 기반 해석가능성 모델 개선이며 incremental함</td></tr>
<tr><td>317</td><td><a href='https://arxiv.org/abs/2611.33331'>Do Not Let the Prior Heal the Anomaly: Selective Anchoring for Detection from Incomplete Measurements</a></td><td>30</td><td>0</td><td>CV</td><td>의료 영상 이상 탐지의 selective anchoring이며 로봇과 무관함</td></tr>
<tr><td>318</td><td><a href='https://arxiv.org/abs/2611.33344'>LGCount: Layout-Guided Diffusion for Zero-Shot Object Counting</a></td><td>30</td><td>0</td><td>CV</td><td>layout 유도 diffusion 기반 zero-shot counting이며 incremental함</td></tr>
<tr><td>319</td><td><a href='https://arxiv.org/abs/2611.33567'>ProPolar: Progressive Polar Decomposition for Implicit Neural Representations</a></td><td>30</td><td>0</td><td>CV</td><td>INR용 optimizer 개선이며 incremental함</td></tr>
<tr><td>320</td><td><a href='https://arxiv.org/abs/2611.33982'>FasterGRN: Reducing the Refinement Redundancy for Accelerating Generative Refinement Networks</a></td><td>30</td><td>0</td><td>Generative</td><td>GRN 중복 refinement 가속이며 incremental함</td></tr>
<tr><td>321</td><td><a href='https://arxiv.org/abs/2611.34091'>From Diagnosing Alignment to Joint Supervision in Multimodal Draft Training</a></td><td>30</td><td>0</td><td>Multimodal</td><td>multimodal draft 모델 정렬 진단이며 speculative decoding 보조 연구임</td></tr>
<tr><td>322</td><td><a href='https://arxiv.org/abs/2611.34140'>Benefit of Structured Representations: When Equivariance Helps in Image Classification</a></td><td>30</td><td>0</td><td>Representation</td><td>equivariance 이득 분석이나 분류 한정임</td></tr>
<tr><td>323</td><td><a href='https://arxiv.org/abs/2611.34279'>Semantic State Reading for Joint Image-Semantic Diffusion Transformers</a></td><td>30</td><td>0</td><td>Generative</td><td>joint image-semantic DiT 의미 상태 읽기로 incremental함</td></tr>
<tr><td>324</td><td><a href='https://arxiv.org/abs/2611.33719'>Understanding Mode Collapse in Diffusion Models under Classifier-Free Guidance</a></td><td>30</td><td>0</td><td>Generative</td><td>CFG 하 diffusion 모드 붕괴 이론 분석임</td></tr>
<tr><td>325</td><td><a href='https://arxiv.org/abs/2611.33896'>Looped Models are Fast Multi-Token Predictors</a></td><td>30</td><td>0</td><td>NLP</td><td>looped 언어모델 다중 토큰 예측으로 추론 속도 향상함</td></tr>
<tr><td>326</td><td><a href='https://arxiv.org/abs/2611.34275'>LatentCP-DPO: Conformal Pessimism for DPO with Finite-Sample Guarantees</a></td><td>30</td><td>0</td><td>NLP</td><td>DPO에 conformal pessimism을 붙인 정렬 기법으로 로봇과 거리 있음</td></tr>
<tr><td>327</td><td><a href='https://arxiv.org/abs/2611.33195'>Verified experience improves materials prediction with large language models</a></td><td>30</td><td>0</td><td>LG</td><td>검증된 경험으로 재료 예측하는 LLM, 도메인 특화 응용임</td></tr>
<tr><td>328</td><td><a href='https://arxiv.org/abs/2611.33428'>When the Knowledge Runs Out: A Part-Level Pilot Evaluation of How Language Models Handle Partially Covered Questions</a></td><td>30</td><td>0</td><td>NLP</td><td>부분 정보 부족 상황의 QA 평가, pilot 수준임</td></tr>
<tr><td>329</td><td><a href='https://arxiv.org/abs/2611.33844'>When Rerankers Work Together: Better and Faster Reranking without Joint Training</a></td><td>30</td><td>0</td><td>NLP</td><td>reranker 조합 연구, RAG 엔지니어링 성격임</td></tr>
<tr><td>330</td><td><a href='https://arxiv.org/abs/2611.33972'>Fine-Tuning Without Gradients? Closed-Form, LLM-Written Classifiers on a Frozen Encoder</a></td><td>30</td><td>0</td><td>LG</td><td>frozen encoder 위 closed-form 분류기, 소규모 연구임</td></tr>
<tr><td>331</td><td><a href='https://arxiv.org/abs/2611.34044'>Reliable User Simulation in Complex Multi-Step Workflows</a></td><td>30</td><td>0</td><td>NLP</td><td>multi-step workflow 사용자 시뮬레이터 신뢰성, 평가 도구임</td></tr>
<tr><td>332</td><td><a href='https://arxiv.org/abs/2611.34341'>Learning from Unreliable Operator References: Claim-Level Rewards for Customer Support Agents</a></td><td>30</td><td>0</td><td>NLP</td><td>신뢰 낮은 reference에 claim 단위 reward, 고객지원 응용임</td></tr>
<tr><td>333</td><td><a href='https://arxiv.org/abs/2611.34831'>Repairing the Trustworthiness of Distilled Language Models</a></td><td>30</td><td>0</td><td>NLP</td><td>distillation 후 신뢰성 회복, 일반 LLM 연구임</td></tr>
<tr><td>334</td><td><a href='https://arxiv.org/abs/2611.34852'>DRBench Pro: A Knowledge-Centric Benchmark for Professional Deep Research Agents</a></td><td>30</td><td>0</td><td>NLP</td><td>deep research agent 지식 중심 benchmark임</td></tr>
<tr><td>335</td><td><a href='https://arxiv.org/abs/2611.33165'>AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics</a></td><td>30</td><td>0</td><td>LG</td><td>Lean 형식화 benchmark, robotics 무관함</td></tr>
<tr><td>336</td><td><a href='https://arxiv.org/abs/2611.33303'>Certify What You Plant: Shortcut-Free Proof Depth in Logical Reasoning Data</a></td><td>30</td><td>0</td><td>LG</td><td>논리 추론 데이터 shortcut 제거 검증, 데이터 생성 연구임</td></tr>
<tr><td>337</td><td><a href='https://arxiv.org/abs/2611.34751'>What Is a Theory Worth to an LLM Solver? Measuring, Inducing, and Merging Theories in Context</a></td><td>30</td><td>0</td><td>LG</td><td>이론 가치 측정·병합, 수학 LLM 연구임</td></tr>
<tr><td>338</td><td><a href='https://arxiv.org/abs/2611.34463'>Least Restrictive Halfplane Control Barrier Functions for an Autonomous Hydrofoil Boat with Moving Obstacles</a></td><td>28</td><td>3</td><td>Navigation</td><td>수상 보트용 CBF 제안으로 제어 이론 위주임</td></tr>
<tr><td>339</td><td><a href='https://arxiv.org/abs/2611.34586'>Geometric Acceleration Obstacles: Physical Boundary Structure and Affine Safety Certificates</a></td><td>28</td><td>3</td><td>Navigation</td><td>geometric acceleration obstacle 안전 인증으로 고전 회피 이론임</td></tr>
<tr><td>340</td><td><a href='https://arxiv.org/abs/2611.34881'>Stranger Things: When Objects Appear Without Their Typical Neighbors</a></td><td>28</td><td>2</td><td>CV</td><td>전형적 이웃 없는 객체 인식 분석으로 로봇 연관 약함</td></tr>
<tr><td>341</td><td><a href='https://arxiv.org/abs/2611.33819'>MMotion: Collaborative Cross-Scale Memory for Text-to-Motion Generation</a></td><td>28</td><td>1</td><td>Generative</td><td>text-to-motion memory 기법이며 incremental함</td></tr>
<tr><td>342</td><td><a href='https://arxiv.org/abs/2611.33905'>Tortho-Gaussian++: Suppressing Geometric Drift and Floaters for Robust Gravity-Aligned TDOM Generation in Large-Scale Aerial Scenes</a></td><td>28</td><td>1</td><td>3D Vision</td><td>항공 3DGS TDOM 생성의 drift 억제로 응용 특화임</td></tr>
<tr><td>343</td><td><a href='https://arxiv.org/abs/2611.34640'>PRAM: Activating Latent Multimodal Knowledge through Partwise Reasoning</a></td><td>28</td><td>1</td><td>Multimodal</td><td>부분 단위 추론의 교차 모달 분류 검색으로 incremental임</td></tr>
<tr><td>344</td><td><a href='https://arxiv.org/abs/2611.34681'>Find the Clue, Not the Scene: Rethinking Reasoning for Entity Recognition in Vision-Language Models</a></td><td>28</td><td>1</td><td>Multimodal</td><td>VLM 개체 인식에서 추론 길이 재고찰로 지식 VQA 한정임</td></tr>
<tr><td>345</td><td><a href='https://arxiv.org/abs/2611.34397'>Strong Starts, Simple Recipes: Unified Multi-Teacher On-Policy Distillation from Multimodal Specialists</a></td><td>28</td><td>1</td><td>Multimodal</td><td>멀티모달 multi-teacher distillation 초기화 레시피 연구로 간단한 개선 수준임</td></tr>
<tr><td>346</td><td><a href='https://arxiv.org/abs/2611.33953'>PINN-Slicer: Exploiting Rotational Symmetry to Solve the Photon Orbit Equation Around a Black Hole</a></td><td>28</td><td>1</td><td>LG</td><td>PINN 대칭 활용 블랙홀 궤도 풀이, 물리 응용임</td></tr>
<tr><td>347</td><td><a href='https://arxiv.org/abs/2611.33160'>Context Scaling: A New Frontier of AI Scaling</a></td><td>28</td><td>1</td><td>LG</td><td>context scaling 개념 제안 position 성격, 실증 근거 약함</td></tr>
<tr><td>348</td><td><a href='https://arxiv.org/abs/2611.33946'>Should Service Requirements Be Scalarized or Constrained When Minimizing Costs? A Case Study on HVAC Control</a></td><td>28</td><td>1</td><td>RL</td><td>서비스 요건을 scalarize할지 제약할지 사례 연구임</td></tr>
<tr><td>349</td><td><a href='https://arxiv.org/abs/2611.33323'>StyleID++: Position-Decoupled and Structure-Coherent Style Retrieval across Diffusion Architectures</a></td><td>28</td><td>0</td><td>CV</td><td>training-free style transfer 개선으로 incremental함</td></tr>
<tr><td>350</td><td><a href='https://arxiv.org/abs/2611.33457'>Playfulness as Feedback for Agentic Game Development</a></td><td>28</td><td>0</td><td>LG</td><td>게임 개발 agent의 playfulness 피드백이며 로봇 연관 없음</td></tr>
<tr><td>351</td><td><a href='https://arxiv.org/abs/2611.33894'>SIA: Selective Image Analogy</a></td><td>28</td><td>0</td><td>Generative</td><td>선택적 image analogy로 incremental함</td></tr>
<tr><td>352</td><td><a href='https://arxiv.org/abs/2611.34207'>Beyond Logits: Coherent Hallucination Mitigation via Attention Contrastive Decoding</a></td><td>28</td><td>0</td><td>Multimodal</td><td>attention contrastive decoding 환각 완화로 incremental함</td></tr>
<tr><td>353</td><td><a href='https://arxiv.org/abs/2611.34290'>StateWeaver: Multi-Agent Coordination of Story-State Transitions for Long-Horizon Video Generation</a></td><td>28</td><td>0</td><td>Video</td><td>long video 생성 multi-agent 조율이며 로봇 연관 약함</td></tr>
<tr><td>354</td><td><a href='https://arxiv.org/abs/2611.33353'>The Marauder&#x27;s Map: Bézier Manifolds Reveal Hidden Surfaces for Model Merging and Ensembling</a></td><td>28</td><td>0</td><td>LG</td><td>Bézier 다양체로 모델 병합과 앙상블을 다룸</td></tr>
<tr><td>355</td><td><a href='https://arxiv.org/abs/2611.34816'>Transferring Architecture as an Optimization Prior</a></td><td>28</td><td>0</td><td>LG</td><td>architecture를 최적화 prior로 전이하는 초기화 연구로 일반 학습 이론임</td></tr>
<tr><td>356</td><td><a href='https://arxiv.org/abs/2611.33307'>Lost in Translation, Not in Confidence: Benchmarking and Calibrating Multilingual Decision Models</a></td><td>28</td><td>0</td><td>NLP</td><td>다국어 decision model 보정 benchmark, robotics 무관함</td></tr>
<tr><td>357</td><td><a href='https://arxiv.org/abs/2611.33668'>Verifiable but Not Predictable: What Sentence Embeddings Know About Propositional Decomposition</a></td><td>28</td><td>0</td><td>NLP</td><td>문장 embedding의 proposition 분해 분석, 진단 연구임</td></tr>
<tr><td>358</td><td><a href='https://arxiv.org/abs/2611.33789'>Multimodal Safety Evaluation of Vision-Language Models in Japanese</a></td><td>28</td><td>0</td><td>Multimodal</td><td>일본어 VLM 안전 평가 확장, benchmark 번역 성격임</td></tr>
<tr><td>359</td><td><a href='https://arxiv.org/abs/2611.34686'>Technical Report MEG2text: Beyond Alignment in Non-Invasive Brain-to-Text</a></td><td>28</td><td>0</td><td>NLP</td><td>MEG 뇌-텍스트 디코딩 기술 보고임</td></tr>
<tr><td>360</td><td><a href='https://arxiv.org/abs/2611.33497'>CA-RAG: Constraint-Aligned Retrieval for Structurally Faithful Long-Form Generation</a></td><td>28</td><td>0</td><td>LG</td><td>제약 정렬 RAG, 작은 개선임</td></tr>
<tr><td>361</td><td><a href='https://arxiv.org/abs/2611.33966'>PatternMiner: Automated Mathematical Discovery Through LLM-Guided Training and Interpretation of Small Models</a></td><td>28</td><td>0</td><td>LG</td><td>LLM 유도 수학 패턴 발견 도구임</td></tr>
<tr><td>362</td><td><a href='https://arxiv.org/abs/2611.34250'>MedSkill-E$^{2}$: Evaluating and Evolving Skills for Medical Agents</a></td><td>28</td><td>0</td><td>LG</td><td>의료 agent skill 평가·진화임</td></tr>
<tr><td>363</td><td><a href='https://arxiv.org/abs/2611.34254'>Crucible: Evaluating LLM Agents in Executable Chemistry Research Environments</a></td><td>28</td><td>0</td><td>LG</td><td>화학 연구 실행 환경 agent 평가임</td></tr>
<tr><td>364</td><td><a href='https://arxiv.org/abs/2611.34612'>Do We Really Need an LLM for Weight-Space Programming? A Deterministic Forward-Only Paradigm and Its Capability Boundaries</a></td><td>28</td><td>0</td><td>LG</td><td>weight-space programming을 LLM 없이 결정적으로 수행함</td></tr>
<tr><td>365</td><td><a href='https://arxiv.org/abs/2611.34536'>Kant-Q: A Q-Learning Algorithm for Kantian Equilibrium in Symmetric Markov Games</a></td><td>27</td><td>1</td><td>RL</td><td>대칭 Markov game의 Kantian equilibrium Q-learning으로 MARL 이론임</td></tr>
<tr><td>366</td><td><a href='https://arxiv.org/abs/2611.33371'>MotifFlow: Training-Free, Self-Contained Style Transfer from Color to Motif in Rectified Flow Transformers</a></td><td>27</td><td>0</td><td>CV</td><td>FLUX용 training-free style transfer이며 incremental함</td></tr>
<tr><td>367</td><td><a href='https://arxiv.org/abs/2611.34591'>ADClaw: A Programmable Visual Agent for Industrial Anomaly Detection and Understanding</a></td><td>26</td><td>1</td><td>Multimodal</td><td>산업 이상 탐지용 프로그래머블 비주얼 에이전트로 응용 위주임</td></tr>
<tr><td>368</td><td><a href='https://arxiv.org/abs/2611.34402'>Any-Rate: Half-Bit Multi-Precision LLM Quantization with Coded Bit-Planes</a></td><td>26</td><td>1</td><td>LG</td><td>LLM 다중 정밀도 양자화로 효율 추론 기법이나 로봇 관련성 약함</td></tr>
<tr><td>369</td><td><a href='https://arxiv.org/abs/2611.33514'>Model Predictive Control of a Multirotor UAV with a Cable-Suspended Payload: A Comparison of Shifted and Transformer-Based Warm Starts</a></td><td>25</td><td>3</td><td>Manipulation</td><td>UAV 케이블 payload MPC의 warm start 비교로 incremental 성격임</td></tr>
<tr><td>370</td><td><a href='https://arxiv.org/abs/2611.34053'>xFORM: Accelerating Fixed-Lag LiDAR Odometry with Exact Factor Compression</a></td><td>25</td><td>3</td><td>Navigation</td><td>LiDAR odometry 계산 가속 기법으로 SLAM 엔지니어링임</td></tr>
<tr><td>371</td><td><a href='https://arxiv.org/abs/2611.34670'>Autonomous Ergodic Robotic Palpation for Elastic Mapping of Curved Soft Tissues</a></td><td>25</td><td>3</td><td>Manipulation</td><td>곡면 연조직 ergodic palpation로 의료 응용임</td></tr>
<tr><td>372</td><td><a href='https://arxiv.org/abs/2611.34724'>LiDAR Intensity Reconstruction with Limited Real Data: An Architecture Benchmark under Fixed-Epoch Training</a></td><td>25</td><td>2</td><td>CV</td><td>LiDAR intensity 복원 아키텍처 벤치마크로 소규모 비교임</td></tr>
<tr><td>373</td><td><a href='https://arxiv.org/abs/2611.34658'>FeaXDrive2: Body-Scene Spatial Grounding for Feasibility-Aware Generative Driving</a></td><td>25</td><td>2</td><td>Embodied AI</td><td>body-scene 공간 grounding 생성 주행 플래닝으로 주행 도메인임</td></tr>
<tr><td>374</td><td><a href='https://arxiv.org/abs/2611.33826'>MotionODE: Enhancing Autoregressive Text-to-Motion Generation with Continuous-Depth Modeling</a></td><td>25</td><td>1</td><td>Generative</td><td>autoregressive text-to-motion에 ODE 도입한 incremental 개선임</td></tr>
<tr><td>375</td><td><a href='https://arxiv.org/abs/2611.34163'>Admoab-DETR: Resolution-Tiered Fusion for Infrared-Visible Object Detection with Missing Modalities</a></td><td>25</td><td>1</td><td>CV</td><td>적외선-가시광 검출의 missing modality 처리로 incremental함</td></tr>
<tr><td>376</td><td><a href='https://arxiv.org/abs/2611.34430'>One Representation to Rule Them All -- Open-Vocabulary Change Detection from Text or Visual Examples</a></td><td>25</td><td>1</td><td>CV</td><td>open-vocabulary change detection 통합 표현이며 incremental함</td></tr>
<tr><td>377</td><td><a href='https://arxiv.org/abs/2611.34795'>CIRKDV2: Cross-Image Relational Knowledge Distillation with Contextual Modeling for Efficient Semantic Segmentation</a></td><td>25</td><td>1</td><td>CV</td><td>semantic segmentation 지식 증류로 incremental임</td></tr>
<tr><td>378</td><td><a href='https://arxiv.org/abs/2611.34828'>Beyond Feature Fusion: Sensor-Grounded Semantic-Spiking Learning for Robust Object Detection</a></td><td>25</td><td>1</td><td>CV</td><td>스파이크 카메라 객체 검출로 특수 센서 응용임</td></tr>
<tr><td>379</td><td><a href='https://arxiv.org/abs/2611.33333'>A Hierarchy of Risk Certificates for Representation-Based Prediction</a></td><td>25</td><td>1</td><td>LG</td><td>표현 기반 예측 위험 인증서 계층으로 이론 위주임</td></tr>
<tr><td>380</td><td><a href='https://arxiv.org/abs/2611.33469'>Differentially Private Policy Optimization in Linear MDPs with Adversarial Rewards</a></td><td>25</td><td>1</td><td>RL</td><td>선형 MDP 차분 프라이버시 정책 최적화로 이론 위주임</td></tr>
<tr><td>381</td><td><a href='https://arxiv.org/abs/2611.33439'>OnCue: Generating Safety-Critical Driving Scenarios under Occlusion with Temporal Control</a></td><td>25</td><td>1</td><td>CV</td><td>occlusion 안전-critical 주행 시나리오 생성으로 로봇 manipulation과는 거리 있음</td></tr>
<tr><td>382</td><td><a href='https://arxiv.org/abs/2611.33617'>Controllable CAD Generation and Interactive Editing of Fluid Rotors</a></td><td>25</td><td>1</td><td>LG</td><td>유체 로터 CAD 생성·편집, 도메인 응용임</td></tr>
<tr><td>383</td><td><a href='https://arxiv.org/abs/2611.33358'>DDxBasis: Explaining Frozen Foundation Encoder-based Medical Classification by Exact Differential Diagnosis</a></td><td>25</td><td>0</td><td>CV</td><td>의료 분류기 설명 방법으로 로봇 연관 없음</td></tr>
<tr><td>384</td><td><a href='https://arxiv.org/abs/2611.33588'>SEEL: Towards End-to-End 3D Sign Generation with Language Models</a></td><td>25</td><td>0</td><td>Generative</td><td>수화 3D 생성 end-to-end 학습이며 로봇 연관 약함</td></tr>
<tr><td>385</td><td><a href='https://arxiv.org/abs/2611.33636'>What Is Redundant at High Resolution? Efficient Attention and Feed-Forward Design for All-in-One Image Restoration</a></td><td>25</td><td>0</td><td>CV</td><td>all-in-one 복원의 효율 설계로 incremental함</td></tr>
<tr><td>386</td><td><a href='https://arxiv.org/abs/2611.33749'>Teaching Students to Stand on Their Own: Distilling Vision Foundation Models for Fine-Grained Few-Shot Class-Incremental Learning</a></td><td>25</td><td>0</td><td>CV</td><td>fine-grained few-shot class-incremental 증류이며 incremental함</td></tr>
<tr><td>387</td><td><a href='https://arxiv.org/abs/2611.33874'>X-Matte: VAE-Free Pixel-Space Flow Matching for Single-Step Image Matting</a></td><td>25</td><td>0</td><td>CV</td><td>pixel-space flow matching matting이며 incremental함</td></tr>
<tr><td>388</td><td><a href='https://arxiv.org/abs/2611.33947'>A Computational Model of Continuous Recognition Memory for Natural Images</a></td><td>25</td><td>0</td><td>CV</td><td>인간 연속 recognition memory 계산 모델로 로봇 연관 약함</td></tr>
<tr><td>389</td><td><a href='https://arxiv.org/abs/2611.34032'>Counter-DECEIVR: Counterfactual Explanations for Deepfake Detectors using Detector-Guided Rectified Flow Inversion</a></td><td>25</td><td>0</td><td>CV</td><td>deepfake 탐지기 counterfactual 설명이며 로봇 무관함</td></tr>
<tr><td>390</td><td><a href='https://arxiv.org/abs/2611.34075'>Hijacking 3D Generation: Targeted Adversarial Attacks against Image-to-3D Models via Prefix Trajectory Alignment</a></td><td>25</td><td>0</td><td>3D Vision</td><td>image-to-3D 적대 공격이며 로봇 연관 없음</td></tr>
<tr><td>391</td><td><a href='https://arxiv.org/abs/2611.34141'>Spe3DUp: Faithful Trajectory Distillation for Fast Image-to-3D Generation</a></td><td>25</td><td>0</td><td>3D Vision</td><td>image-to-3D 증류 가속이며 incremental함</td></tr>
<tr><td>392</td><td><a href='https://arxiv.org/abs/2611.34237'>VibeVideoAgent: Closing the Perceptual Loop for Code-Driven Video Generation</a></td><td>25</td><td>0</td><td>Video</td><td>코드 기반 영상 생성 agent이며 로봇 연관 없음</td></tr>
<tr><td>393</td><td><a href='https://arxiv.org/abs/2611.34446'>PreserveReward: Reliable Consistency Reward Modeling for Image Editing via Dual-Teacher On-Policy Self-Distillation</a></td><td>25</td><td>0</td><td>Generative</td><td>이미지 편집 consistency reward 모델이며 incremental함</td></tr>
<tr><td>394</td><td><a href='https://arxiv.org/abs/2611.34478'>Feed-Forward Adaptive Gaussian Splatting for Interactive Medical Volume Rendering</a></td><td>25</td><td>0</td><td>3D Vision</td><td>의료 볼륨 렌더링용 feed-forward 3DGS로 응용 특화임</td></tr>
<tr><td>395</td><td><a href='https://arxiv.org/abs/2611.33182'>Neighbor Crowding Predicts Feature Stability in Sparse Autoencoders</a></td><td>25</td><td>0</td><td>LG</td><td>SAE feature 안정성 해석 연구로 로봇 무관함</td></tr>
<tr><td>396</td><td><a href='https://arxiv.org/abs/2611.33183'>REI: Learning Ideation from Repository Evolution</a></td><td>25</td><td>0</td><td>LG</td><td>저장소 진화에서 아이디어 생성 학습으로 자동 연구 주제임</td></tr>
<tr><td>397</td><td><a href='https://arxiv.org/abs/2611.33962'>DLaR: Dynamic Stochasticity Control for Latent Reasoning in Large Language Models</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM latent reasoning 확률성 제어임</td></tr>
<tr><td>398</td><td><a href='https://arxiv.org/abs/2611.34228'>Change Point Detection with Generative Models</a></td><td>25</td><td>0</td><td>LG</td><td>생성모델 기반 change point detection으로 시계열 일반 방법임</td></tr>
<tr><td>399</td><td><a href='https://arxiv.org/abs/2611.34667'>Learning to Be Truncated: Preparing LLM Checkpoints for SVD Compression</a></td><td>25</td><td>0</td><td>LG</td><td>SVD 압축을 위한 LLM 체크포인트 준비로 로봇과 무관함</td></tr>
<tr><td>400</td><td><a href='https://arxiv.org/abs/2611.34758'>Reading Fine-Tuning Diffs Through Lenses: Model Diffing for Backdoor Detection</a></td><td>25</td><td>0</td><td>NLP</td><td>fine-tuning diff 기반 backdoor 탐지 모델 diffing으로 로봇과 무관함</td></tr>
<tr><td>401</td><td><a href='https://arxiv.org/abs/2611.34821'>LoopTitan: What Does Parameter Revisit Buy a Mixture-of-Experts?</a></td><td>25</td><td>0</td><td>LG</td><td>looped MoE의 parameter revisit 효과 분석으로 로봇과 무관함</td></tr>
<tr><td>402</td><td><a href='https://arxiv.org/abs/2611.33327'>Who Attributes a Mind to Whom? Mutual Theory of Mind in Simulated User-Assistant Conversation</a></td><td>25</td><td>0</td><td>NLP</td><td>사용자-assistant 상호 mind attribution 분석, robotics 무관함</td></tr>
<tr><td>403</td><td><a href='https://arxiv.org/abs/2611.33510'>LogToPersona: New Benchmark and Efficient Persona Prediction through Semantic Log Filtering</a></td><td>25</td><td>0</td><td>NLP</td><td>로그 기반 persona 예측 benchmark, 응용 중심임</td></tr>
<tr><td>404</td><td><a href='https://arxiv.org/abs/2611.33700'>Sports Agent: A Self-Evolving System for Conversational Data Analytics</a></td><td>25</td><td>0</td><td>NLP</td><td>스포츠 분석 agent 자기 진화 시스템, 응용 위주임</td></tr>
<tr><td>405</td><td><a href='https://arxiv.org/abs/2611.34303'>IRTIQA: Evolving in English, Evaluated in Urdu -- Does Agent Self-Evolution Transfer from English to Urdu and Code-Switched Input?</a></td><td>25</td><td>0</td><td>NLP</td><td>Urdu 대상 agent 자기 진화 전이 benchmark임</td></tr>
<tr><td>406</td><td><a href='https://arxiv.org/abs/2611.34331'>Puzzling-Bench: Evaluating Language Models on 23,777 Human-Written Puzzles with Community-Verified Answers</a></td><td>25</td><td>0</td><td>NLP</td><td>퍼즐 benchmark 23,777개, 평가 자원임</td></tr>
<tr><td>407</td><td><a href='https://arxiv.org/abs/2611.34505'>Know the Design, Pick the Attack: Sentence-Keyed Watermarks for LLMs</a></td><td>25</td><td>0</td><td>NLP</td><td>LLM watermark 공격 설계 분석, robotics 무관함</td></tr>
<tr><td>408</td><td><a href='https://arxiv.org/abs/2611.34529'>AliceAI-Foundation-80B-A3B-Base</a></td><td>25</td><td>0</td><td>NLP</td><td>80B MoE 기반 LM 공개, scale-up 성격임</td></tr>
<tr><td>409</td><td><a href='https://arxiv.org/abs/2611.34938'>Tokenisation is not in APX</a></td><td>25</td><td>0</td><td>NLP</td><td>tokenisation APX 불가 증명, 이론 결과이나 robotics 무관함</td></tr>
<tr><td>410</td><td><a href='https://arxiv.org/abs/2611.33639'>How Much Effort Does an AI Code Reviewer Need? Evidence from Claude 5.5 Models on Plausible-but-Wrong Patches</a></td><td>25</td><td>0</td><td>LG</td><td>AI 코드 리뷰어 노력 수준 실증임</td></tr>
<tr><td>411</td><td><a href='https://arxiv.org/abs/2611.34646'>REE: A Scientific Research Entrance Exam for AI Agents</a></td><td>25</td><td>0</td><td>LG</td><td>연구 agent 입시 benchmark임</td></tr>
<tr><td>412</td><td><a href='https://arxiv.org/abs/2611.34359'>RAWPrism: A Three-Task Dataset and a Unified Model for RAW-Domain Image Fusion</a></td><td>24</td><td>1</td><td>CV</td><td>RAW 영역 이미지 융합 데이터셋과 모델로 incremental 성격임</td></tr>
<tr><td>413</td><td><a href='https://arxiv.org/abs/2611.34246'>Autonomous Vineyard Exploration using LiDAR Sensing: A Field Evaluation on Legged-Wheeled Quadruped Robot</a></td><td>22</td><td>3</td><td>Navigation</td><td>포도밭 LiDAR 탐사 현장 평가로 응용 보고 성격임</td></tr>
<tr><td>414</td><td><a href='https://arxiv.org/abs/2611.33809'>Probabilistic Monocular Biomechanical Reconstruction via Guided Flow Matching</a></td><td>22</td><td>1</td><td>3D Vision</td><td>단안 영상 생체역학 재구성 flow matching이며 로봇 연관 약함</td></tr>
<tr><td>415</td><td><a href='https://arxiv.org/abs/2611.34021'>Rethinking Unsupervised Cross-Modal Homography Estimation:Spatially Aware Representations and Geometric Consistency Learning</a></td><td>22</td><td>1</td><td>CV</td><td>cross-modal homography 비지도 추정이며 incremental함</td></tr>
<tr><td>416</td><td><a href='https://arxiv.org/abs/2611.34226'>LiveRelight: Sub-Second Global Illumination Editing for Gaussian Interiors</a></td><td>22</td><td>1</td><td>3D Vision</td><td>Gaussian 실내 장면 relighting 속도 개선이며 로봇 연관 약함</td></tr>
<tr><td>417</td><td><a href='https://arxiv.org/abs/2611.34465'>Evidence-Aligned Benchmarking and Learning for Medical Video Language Models</a></td><td>22</td><td>1</td><td>Multimodal</td><td>의료 비디오 언어모델 근거 정렬 벤치마크로 로봇 관련성 거의 없음</td></tr>
<tr><td>418</td><td><a href='https://arxiv.org/abs/2611.34854'>TIDE-Flow: Fine-Grained Temporal Evidence and Structured Displacement Matching for Spike Optical Flow</a></td><td>22</td><td>1</td><td>CV</td><td>스파이크 광학 흐름 추정으로 특수 센서임</td></tr>
<tr><td>419</td><td><a href='https://arxiv.org/abs/2611.33735'>JOVE ICE: Intent Guided Cloud Edge Device Collaboration for AI Glasses</a></td><td>22</td><td>1</td><td>LG</td><td>AI 안경 클라우드-엣지 협업, 시스템 응용임</td></tr>
<tr><td>420</td><td><a href='https://arxiv.org/abs/2611.33455'>Recovering What Matters, Transferring Only What Is Reliable: Toward Precise Reference-Based Super-Resolution</a></td><td>22</td><td>0</td><td>CV</td><td>reference 기반 super-resolution이며 incremental함</td></tr>
<tr><td>421</td><td><a href='https://arxiv.org/abs/2611.33857'>Hybrid Reinforcement Learning for One-step Degraded Infrared and Visible Image Fusion</a></td><td>22</td><td>0</td><td>CV</td><td>적외선-가시광 융합 hybrid RL이며 incremental함</td></tr>
<tr><td>422</td><td><a href='https://arxiv.org/abs/2611.33935'>BayesPath: Reliability-Aware Bayesian Reasoning for Whole-Slide Pathology Agents</a></td><td>22</td><td>0</td><td>Multimodal</td><td>병리 슬라이드 agent의 Bayesian 추론이며 무관함</td></tr>
<tr><td>423</td><td><a href='https://arxiv.org/abs/2611.34143'>Non-Linear Motion from Two Frames: Cubic Hermite Trajectories for Video Frame Interpolation</a></td><td>22</td><td>0</td><td>Video</td><td>프레임 보간 trajectory 개선이며 incremental함</td></tr>
<tr><td>424</td><td><a href='https://arxiv.org/abs/2611.34319'>PostMesh: Self-Rewarded Preference Post-Training for Flow-Based Artist Mesh Generation</a></td><td>22</td><td>0</td><td>3D Vision</td><td>artist mesh 생성 preference post-training으로 무관함</td></tr>
<tr><td>425</td><td><a href='https://arxiv.org/abs/2611.34575'>Sage-Med: Scaling Medical Multimodal Intelligence</a></td><td>22</td><td>0</td><td>Multimodal</td><td>의료 MLLM 스케일링 연구로 도메인 특화임</td></tr>
<tr><td>426</td><td><a href='https://arxiv.org/abs/2611.34603'>VisualMontage: Manipulating the Beliefs of Vision-Language Agents with Authentic Image Sequences</a></td><td>22</td><td>0</td><td>Multimodal</td><td>VLM 에이전트 신념 조작 공격으로 소셜 미디어 맥락임</td></tr>
<tr><td>427</td><td><a href='https://arxiv.org/abs/2611.34637'>Carrying Feature Ablations Across Sparse Autoencoder Seeds</a></td><td>22</td><td>0</td><td>CV</td><td>SAE 시드 간 feature ablation 분석으로 해석성 연구임</td></tr>
<tr><td>428</td><td><a href='https://arxiv.org/abs/2611.34719'>Reading, Not Adapting: Unlocking Frozen Visual Knowledge for AI-Generated Image Detection</a></td><td>22</td><td>0</td><td>CV</td><td>AI 생성 이미지 탐지로 로봇 무관함</td></tr>
<tr><td>429</td><td><a href='https://arxiv.org/abs/2611.33236'>KiRA: Kronecker Input-Gated Rank Adaptation for Parameter-Efficient Fine-Tuning of Pretrained Models</a></td><td>22</td><td>0</td><td>LG</td><td>PEFT 어댑터 변형으로 incremental임</td></tr>
<tr><td>430</td><td><a href='https://arxiv.org/abs/2611.33589'>Amortizing Exact Orthogonality: Drift-Triggered Restoration for Orthogonal Fine-Tuning</a></td><td>22</td><td>0</td><td>LG</td><td>orthogonal fine-tuning 복원 효율화로 incremental임</td></tr>
<tr><td>431</td><td><a href='https://arxiv.org/abs/2611.33648'>PRIOR: Pre-Call Reasoning in SFT and Its Influence on Tool-Use Retention under RL</a></td><td>22</td><td>0</td><td>NLP</td><td>SFT pre-call 추론이 RL 단계 tool-use 유지에 미치는 영향임</td></tr>
<tr><td>432</td><td><a href='https://arxiv.org/abs/2611.33825'>On Grokking and the Dynamics of Generalization</a></td><td>22</td><td>0</td><td>LG</td><td>grokking 일반화 역학 이론임</td></tr>
<tr><td>433</td><td><a href='https://arxiv.org/abs/2611.33887'>The Gradient Difference Induced by Detaching the Denominator in QK Normalization</a></td><td>22</td><td>0</td><td>LG</td><td>QK normalization 분모 detach의 gradient 차이 분석임</td></tr>
<tr><td>434</td><td><a href='https://arxiv.org/abs/2611.34092'>Improving Tail-Augmented Speculative Drafting with Hidden State Mixing and Gradient Detach</a></td><td>22</td><td>0</td><td>NLP</td><td>투기적 디코딩 drafter 개선으로 incremental임</td></tr>
<tr><td>435</td><td><a href='https://arxiv.org/abs/2611.34298'>RAP: Radial-Angular Random Projection for Hyperbolic Representations</a></td><td>22</td><td>0</td><td>LG</td><td>쌍곡 표현용 random projection 이론으로 로봇과 무관함</td></tr>
<tr><td>436</td><td><a href='https://arxiv.org/abs/2611.34707'>When the Proxy Is Wrong: Mismatch-Corrected Bandits for Adaptive Data Sampling</a></td><td>22</td><td>0</td><td>LG</td><td>proxy 불일치 보정 bandit 데이터 샘플링으로 LLM 학습 효율화에 한정됨</td></tr>
<tr><td>437</td><td><a href='https://arxiv.org/abs/2611.34726'>Hierarchical Graph Metanetworks</a></td><td>22</td><td>0</td><td>LG</td><td>hierarchical graph metanetwork로 weight space 학습이며 로봇과 무관함</td></tr>
<tr><td>438</td><td><a href='https://arxiv.org/abs/2611.34760'>One Model, Many Modes: Evolving System Prompt Ensembles for Creative Generation</a></td><td>22</td><td>0</td><td>NLP</td><td>system prompt ensemble로 창의적 생성의 mode collapse를 완화함, 로봇과 무관함</td></tr>
<tr><td>439</td><td><a href='https://arxiv.org/abs/2611.34934'>Attack Policy Selection can Mislead Monitor Evaluators</a></td><td>22</td><td>0</td><td>LG</td><td>attack policy 선택이 AI monitor 평가를 왜곡함, 안전 평가이나 로봇과 거리 있음</td></tr>
<tr><td>440</td><td><a href='https://arxiv.org/abs/2611.33175'>Feature-Based Explainability of Transformer Scoring Models: A Fidelity-First Framework for Automated Writing Assessment</a></td><td>22</td><td>0</td><td>NLP</td><td>작문 채점 모델 설명가능성 연구, robotics와 무관함</td></tr>
<tr><td>441</td><td><a href='https://arxiv.org/abs/2611.33499'>Evaluating Large Language Models on conversational African American English: Feature classification and next-turn generation</a></td><td>22</td><td>0</td><td>NLP</td><td>AAE LLM 평가, robotics 무관함</td></tr>
<tr><td>442</td><td><a href='https://arxiv.org/abs/2611.33726'>NORMCRAFT: Cultural Norm Generation for Context-Aware Language Model Alignment</a></td><td>22</td><td>0</td><td>NLP</td><td>문화 규범 생성 alignment, robotics 무관함</td></tr>
<tr><td>443</td><td><a href='https://arxiv.org/abs/2611.33747'>Tells of a Lying Machine: Analyzing LLM-Generated Strategic Dialogue in Chinese Werewolf</a></td><td>22</td><td>0</td><td>NLP</td><td>Werewolf 대화 기만 분석, robotics 무관함</td></tr>
<tr><td>444</td><td><a href='https://arxiv.org/abs/2611.34042'>Too Smart for Its Own Good? Cognitive Fidelity and Competence Leakage in LLM Simulations of Young Learners</a></td><td>22</td><td>0</td><td>NLP</td><td>LLM 학습자 시뮬레이터 인지 충실도, 교육 응용임</td></tr>
<tr><td>445</td><td><a href='https://arxiv.org/abs/2611.34785'>PersonaFactory: Stylistic User Prompt Augmentation with Synthetic Persona Bank</a></td><td>22</td><td>0</td><td>NLP</td><td>합성 persona 기반 프롬프트 증강임</td></tr>
<tr><td>446</td><td><a href='https://arxiv.org/abs/2611.33411'>Collaborative Language Models for Semantic IoT Data Processing: Validation through Zero-Shot Human Activity Recognition</a></td><td>22</td><td>0</td><td>LG</td><td>IoT 시맨틱 처리용 협업 LM, 응용임</td></tr>
<tr><td>447</td><td><a href='https://arxiv.org/abs/2611.33563'>FIG-MAC: A Fine-grained Inspiration Graph Empowered Multi-Agent Collaboration for Automated Scientific Hypothesis Generation</a></td><td>22</td><td>0</td><td>LG</td><td>과학 가설 생성 multi-agent, robotics 무관함</td></tr>
<tr><td>448</td><td><a href='https://arxiv.org/abs/2611.33775'>CHD-Bench: Diagnosing Congenital Heart Disease through Interactive Examination</a></td><td>22</td><td>0</td><td>Multimodal</td><td>선천성 심장병 진단 interactive benchmark, 의료 응용임</td></tr>
<tr><td>449</td><td><a href='https://arxiv.org/abs/2611.34190'>SOLO: Towards Sample-Faithful and Detectable LLM Watermarking under Repeated Sampling via Content-Anchored Single-Owner Contexts</a></td><td>22</td><td>0</td><td>LG</td><td>반복 샘플링 하 watermark임</td></tr>
<tr><td>450</td><td><a href='https://arxiv.org/abs/2611.34708'>From Shared Patterns to Individual Evidence: Two-Stage Reasoning for Emerging Entities in Temporal Knowledge Graphs</a></td><td>22</td><td>0</td><td>LG</td><td>temporal KG 신규 entity 추론임</td></tr>
<tr><td>451</td><td><a href='https://arxiv.org/abs/2611.34540'>Reference-Model-Guided Distributed MPC for UAV Swarm Formation Flying Under Switching Directed Graphs</a></td><td>20</td><td>2</td><td>Navigation</td><td>UAV swarm 분산 MPC 제어로 고전 제어 위주임</td></tr>
<tr><td>452</td><td><a href='https://arxiv.org/abs/2611.33866'>MAFNet-UR$^3$: Mask-Aware Fusion Network for Unified Raindrop and Reflection Removal</a></td><td>20</td><td>1</td><td>CV</td><td>빗방울/반사 제거 네트워크로 incremental함</td></tr>
<tr><td>453</td><td><a href='https://arxiv.org/abs/2611.34096'>FoMNet: Adaptive Kernels Meet Contextual Matching for Cross-Modal Homography Estimation</a></td><td>20</td><td>1</td><td>CV</td><td>cross-modal homography 추정이며 incremental함</td></tr>
<tr><td>454</td><td><a href='https://arxiv.org/abs/2611.34622'>Beyond Pose Control: Anatomically Consistent Ultrasound Video Generation</a></td><td>20</td><td>1</td><td>Video</td><td>초음파 영상 생성으로 의료 특화임</td></tr>
<tr><td>455</td><td><a href='https://arxiv.org/abs/2611.33210'>Confidence-Based Adaptive Retrieval Fails Where It Matters Most: A Paradox in Biomedical Question Answering</a></td><td>20</td><td>0</td><td>NLP</td><td>biomedical RAG의 confidence 기반 검색 분석이며 로보틱스와 무관함</td></tr>
<tr><td>456</td><td><a href='https://arxiv.org/abs/2611.33465'>OrdiHand-GS: Ordinal-Guided Tracking and Hand-Refined Gaussian Avatars for Digital Signers</a></td><td>20</td><td>0</td><td>3D Vision</td><td>수화 아바타 Gaussian이며 로봇 연관 없음</td></tr>
<tr><td>457</td><td><a href='https://arxiv.org/abs/2611.34284'>ReMeDi: Single-Image PBR Material Estimation via Reparameterization between Metal and Dielectric Hypotheses</a></td><td>20</td><td>0</td><td>3D Vision</td><td>단일 이미지 PBR 재질 추정으로 로봇 연관 약함</td></tr>
<tr><td>458</td><td><a href='https://arxiv.org/abs/2611.34414'>SemProxy: Semantic 3D Proxies for Controllable Agentic 3D Modeling</a></td><td>20</td><td>0</td><td>3D Vision</td><td>agentic 3D 모델링 제어로 로봇 무관함</td></tr>
<tr><td>459</td><td><a href='https://arxiv.org/abs/2611.34467'>Attacking Hard-Label Large Vision-Language Models with Model-Sensitive Adversarial Patch Designs</a></td><td>20</td><td>0</td><td>Multimodal</td><td>LVLM 하드라벨 적대 패치 공격으로 로봇 관련성 낮음</td></tr>
<tr><td>460</td><td><a href='https://arxiv.org/abs/2611.34700'>Seeing the Right Context: Grounded On-Policy Distillation for Remote Sensing</a></td><td>20</td><td>0</td><td>Multimodal</td><td>원격탐사 MLLM on-policy distillation으로 도메인 특화임</td></tr>
<tr><td>461</td><td><a href='https://arxiv.org/abs/2611.34940'>LuxAvatar: Real-Time Relightable Head Avatars via Causal Neural Shading of 3D Intrinsic Proxies</a></td><td>20</td><td>0</td><td>3D Vision</td><td>실시간 relightable 아바타로 로봇 무관함</td></tr>
<tr><td>462</td><td><a href='https://arxiv.org/abs/2611.33417'>Temporal Selective Exploration for Reinforcement Learning-Guided Continuous-Discrete Flow Matching in 3D Molecular Design</a></td><td>20</td><td>0</td><td>RL</td><td>3D 분자 설계 flow matching RL로 도메인 특화임</td></tr>
<tr><td>463</td><td><a href='https://arxiv.org/abs/2611.33525'>Deletion You Can Check: Auditing LLM Unlearning</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM unlearning 감사로 무관함</td></tr>
<tr><td>464</td><td><a href='https://arxiv.org/abs/2611.34472'>DiversePlace: Diversity-Seeking Curriculum Reinforcement Learning for Macro Placement</a></td><td>20</td><td>0</td><td>RL</td><td>macro placement용 curriculum RL로 로봇과 무관함</td></tr>
<tr><td>465</td><td><a href='https://arxiv.org/abs/2611.34711'>Spec2Weights: Certifying Networks that a Language Model Writes from a Specification</a></td><td>20</td><td>0</td><td>LG</td><td>LM이 작성한 네트워크 가중치 인증으로 로봇과 무관함</td></tr>
<tr><td>466</td><td><a href='https://arxiv.org/abs/2611.34848'>Put the World Back: Timestamps Matter in Time Series Reasoning</a></td><td>20</td><td>0</td><td>NLP</td><td>시계열 추론에서 timestamp 순서의 중요성 평가로 로봇과 거리 있음</td></tr>
<tr><td>467</td><td><a href='https://arxiv.org/abs/2611.33459'>AI-human hybrid conversations: Can AI Agents Improve Discourse Quality?</a></td><td>20</td><td>0</td><td>NLP</td><td>AI-인간 혼합 토론 품질 연구, robotics 무관함</td></tr>
<tr><td>468</td><td><a href='https://arxiv.org/abs/2611.33503'>Using AI to Simulate the Behaviour of European Populations</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 기반 유럽 인구 응답 시뮬레이션, robotics 무관함</td></tr>
<tr><td>469</td><td><a href='https://arxiv.org/abs/2611.33690'>Refusal Is Not Scored: A Coverage Limit in Content-Based Bias Evaluation</a></td><td>20</td><td>0</td><td>NLP</td><td>편향 평가에서 거절 처리 문제 지적, robotics 무관함</td></tr>
<tr><td>470</td><td><a href='https://arxiv.org/abs/2611.34015'>Residual Cross-Model Narrative Convergence under Shared Prompts: Auditing Prompt Controls and Narrative Measurement</a></td><td>20</td><td>0</td><td>NLP</td><td>LLM 서사 수렴 분석, robotics 무관함</td></tr>
<tr><td>471</td><td><a href='https://arxiv.org/abs/2611.34427'>Mitigating Hallucinations in Medical Question Answering on ESC Cardiology Guidelines: Evaluation and Retrieval Optimization</a></td><td>20</td><td>0</td><td>NLP</td><td>심장학 지침 QA 환각 완화, 의료 응용임</td></tr>
<tr><td>472</td><td><a href='https://arxiv.org/abs/2611.34491'>Where Does the Asymmetry Enter? Staging a Fairness Audit Across a Fused Multimodal Moderation Pipeline</a></td><td>20</td><td>0</td><td>Multimodal</td><td>멀티모달 moderation 공정성 감사, robotics 무관함</td></tr>
<tr><td>473</td><td><a href='https://arxiv.org/abs/2611.34819'>VulnSafe: Measuring Vulnerability-Aware Relational Safety in Large Language Models</a></td><td>20</td><td>0</td><td>NLP</td><td>취약성 인식 안전 benchmark, robotics 무관함</td></tr>
<tr><td>474</td><td><a href='https://arxiv.org/abs/2611.33712'>PowerFix: Physics-Guided Iterative Repair for LLM-Assisted Power Converter Design</a></td><td>20</td><td>0</td><td>LG</td><td>전력 변환기 설계 LLM 수리, 도메인 응용임</td></tr>
<tr><td>475</td><td><a href='https://arxiv.org/abs/2611.33836'>Can Its Own Misses Teach an MLLM to Find Small Brain Metastases?</a></td><td>20</td><td>0</td><td>Multimodal</td><td>MLLM의 작은 뇌전이 탐지, 의료 응용임</td></tr>
<tr><td>476</td><td><a href='https://arxiv.org/abs/2611.33879'>FORK: Co-Evolving Safe Disclosure and Decision Skills Against Attackers Who Read Every Refusal</a></td><td>20</td><td>0</td><td>LG</td><td>agent 안전 공개 skill 공진화, 보안 연구임</td></tr>
<tr><td>477</td><td><a href='https://arxiv.org/abs/2611.34408'>Embodied Lower-limb Exoskeleton Assistance: Survey, Challenges, and Perspectives</a></td><td>18</td><td>2</td><td>Embodied AI</td><td>하지 외골격 survey로 연구 주제와 거리 있음</td></tr>
<tr><td>478</td><td><a href='https://arxiv.org/abs/2611.34211'>Compute-Aware Submodular Online Learning in Open Multi-Agent Systems</a></td><td>18</td><td>1</td><td>LG</td><td>다중 에이전트 submodular 온라인 학습 이론으로 로봇 학습과 거리 있음</td></tr>
<tr><td>479</td><td><a href='https://arxiv.org/abs/2611.33392'>BreathSplat: Grounding One Smooth Motion in the Breathing Phase for 4D Cone-Beam CT</a></td><td>18</td><td>0</td><td>3D Vision</td><td>4D CBCT 의료 재구성이며 로봇과 무관함</td></tr>
<tr><td>480</td><td><a href='https://arxiv.org/abs/2611.33734'>DualCast: Dual-Image Conditioned Diffusion Transformers for Digital Human E-Commerce Video Generation</a></td><td>18</td><td>0</td><td>Video</td><td>디지털 휴먼 커머스 영상 생성이며 로봇 연관 없음</td></tr>
<tr><td>481</td><td><a href='https://arxiv.org/abs/2611.33990'>geo-eval-harness: An Evaluation Harness for Geospatial Foundation Models</a></td><td>18</td><td>0</td><td>CV</td><td>지리공간 foundation model 평가 harness로 무관함</td></tr>
<tr><td>482</td><td><a href='https://arxiv.org/abs/2611.34062'>Surf-Style: Surface-Based Scene Stylization</a></td><td>18</td><td>0</td><td>3D Vision</td><td>표면 기반 3D 스타일화이며 로봇 무관함</td></tr>
<tr><td>483</td><td><a href='https://arxiv.org/abs/2611.34344'>SPARC: Semantic Calibration with Latent Multimodal Knowledge for Robust Image-Text Retrieval</a></td><td>18</td><td>0</td><td>Multimodal</td><td>강건 image-text retrieval이며 incremental함</td></tr>
<tr><td>484</td><td><a href='https://arxiv.org/abs/2611.34418'>SPGSR: A Small Pixel-Space Generator for One-Step Super-Resolution</a></td><td>18</td><td>0</td><td>CV</td><td>one-step super-resolution 소형 생성기로 incremental함</td></tr>
<tr><td>485</td><td><a href='https://arxiv.org/abs/2611.34523'>Rank Before You Encode: Reading a Few Percent of a Whole-Slide Image</a></td><td>18</td><td>0</td><td>CV</td><td>병리 슬라이드 효율 추론으로 로봇과 무관함</td></tr>
<tr><td>486</td><td><a href='https://arxiv.org/abs/2611.34564'>Score-based Black-box Attack via Adversarial Condition Guided Diffusion Model</a></td><td>18</td><td>0</td><td>CV</td><td>확산 모델 기반 블랙박스 적대 공격으로 무관함</td></tr>
<tr><td>487</td><td><a href='https://arxiv.org/abs/2611.34645'>A Hard Background Pairing Transfers across Classifiers and Images</a></td><td>18</td><td>0</td><td>CV</td><td>분류기 배경 쌍 적대 전이 분석으로 로봇 무관함</td></tr>
<tr><td>488</td><td><a href='https://arxiv.org/abs/2611.34843'>Probing Visual Idiosyncrasies in Text-to-Image Models</a></td><td>18</td><td>0</td><td>Generative</td><td>T2I 모델 고유 특성 탐색으로 로봇 무관함</td></tr>
<tr><td>489</td><td><a href='https://arxiv.org/abs/2611.34929'>High-Fidelity Image Matting with Pixel-Space Diffusion Transformers</a></td><td>18</td><td>0</td><td>CV</td><td>pixel-space DiT 이미지 매팅으로 무관함</td></tr>
<tr><td>490</td><td><a href='https://arxiv.org/abs/2611.33259'>Fast and Scalable Abstract Interpretation for Deep Neural Networks</a></td><td>18</td><td>0</td><td>LG</td><td>DNN 추상 해석 가속으로 검증 도구임</td></tr>
<tr><td>491</td><td><a href='https://arxiv.org/abs/2611.33426'>Scalpel and Brush: Pruning and Targeted Weight Editing of a Small Language Model by a Single LLM Agent</a></td><td>18</td><td>0</td><td>LG</td><td>LLM 에이전트의 소형 언어모델 가중치 편집 분석임</td></tr>
<tr><td>492</td><td><a href='https://arxiv.org/abs/2611.33515'>Evaluation and Restoration of Safety in Reasoning-Tuned LLMs</a></td><td>18</td><td>0</td><td>NLP</td><td>추론 튜닝 LLM 안전성 평가 및 복원임</td></tr>
<tr><td>493</td><td><a href='https://arxiv.org/abs/2611.33951'>BReD: Block Replay Dithering for Stable Low-Bit EMA Optimizer States</a></td><td>18</td><td>0</td><td>LG</td><td>저비트 optimizer state EMA 안정화임</td></tr>
<tr><td>494</td><td><a href='https://arxiv.org/abs/2611.33952'>DuoMI: Dual Mutual Information Regularization for Expert Reuse in Looped Transformers</a></td><td>18</td><td>0</td><td>LG</td><td>looped MoE expert 라우팅 정규화임</td></tr>
<tr><td>495</td><td><a href='https://arxiv.org/abs/2611.33983'>Quaternion-Tucker ZigZag Networks: Halving Transformer Backbone Parameters and Enabling Exact 2D Zero-Loss Continual Scaling</a></td><td>18</td><td>0</td><td>LG</td><td>Quaternion-Tucker 파라미터 압축 트랜스포머임</td></tr>
<tr><td>496</td><td><a href='https://arxiv.org/abs/2611.34493'>Auditing Identity and Timing Signals in Operational Logs</a></td><td>18</td><td>0</td><td>LG</td><td>운영 로그의 identity/timing 누출 감사로 로봇과 무관함</td></tr>
<tr><td>497</td><td><a href='https://arxiv.org/abs/2611.34734'>From NP-Hardness to Exact Tractability Through Sample Abundance</a></td><td>18</td><td>0</td><td>LG</td><td>NP-hard 문제의 표본 풍부성 하 tractability 이론으로 로봇과 무관함</td></tr>
<tr><td>498</td><td><a href='https://arxiv.org/abs/2611.34805'>Barron Smoothness for Layers in Deep Neural Networks</a></td><td>18</td><td>0</td><td>LG</td><td>Barron smoothness 근사 이론으로 로봇과 무관함</td></tr>
<tr><td>499</td><td><a href='https://arxiv.org/abs/2611.34858'>From Prediction to Decision: Decision-Focused Fine-Tuning of Autoregressive Tabular Transformers for Cost-Sensitive Financial Events</a></td><td>18</td><td>0</td><td>LG</td><td>금융 이벤트 decision-focused fine-tuning으로 로봇과 무관함</td></tr>
<tr><td>500</td><td><a href='https://arxiv.org/abs/2611.33266'>FrIdéo: French News Outlet Ideology Scoring via Multi-Source Evidence Fusion and Distancing-Aware Lexical Scoring</a></td><td>18</td><td>0</td><td>NLP</td><td>프랑스 언론 이념 점수화, 사회과학 응용임</td></tr>
<tr><td>501</td><td><a href='https://arxiv.org/abs/2611.33715'>KeyDeck: Multi-Paper-to-Slide Generation via Cross-Paper Synthesis and Reference-Guided Personalization</a></td><td>18</td><td>0</td><td>LG</td><td>multi-paper 슬라이드 생성임</td></tr>
<tr><td>502</td><td><a href='https://arxiv.org/abs/2611.34122'>MUSE: Multi-Task Uncertainty-Aware Self-Supervised Encoder for mmWave ISAC</a></td><td>15</td><td>1</td><td>LG</td><td>mmWave ISAC 자기지도 인코더로 통신 도메인임</td></tr>
<tr><td>503</td><td><a href='https://arxiv.org/abs/2611.34428'>Calibration of Neuromusculoskeletal Models Using Differentiable Physics: Recommendations for Improving Model Accuracy</a></td><td>15</td><td>1</td><td>LG</td><td>신경근골격 모델 보정 recommendation으로 로봇 학습과 거리 있음</td></tr>
<tr><td>504</td><td><a href='https://arxiv.org/abs/2611.34563'>On Utilization of Edge-AI for condition monitoring towards predictive maintenance: A use case in dairy processing using explainable AI</a></td><td>15</td><td>1</td><td>LG</td><td>엣지 AI 예지 보전 서베이임</td></tr>
<tr><td>505</td><td><a href='https://arxiv.org/abs/2611.33369'>Benchmarking Segmentation Models for Scalable Mangrove Mapping with Sentinel-1/2 Imagery</a></td><td>15</td><td>0</td><td>CV</td><td>맹그로브 위성 영상 segmentation benchmark로 로보틱스와 무관함</td></tr>
<tr><td>506</td><td><a href='https://arxiv.org/abs/2611.33425'>Anatomy-Aware Pseudo-Labels and Homotopy-Annealed Hausdorff Supervision for Semi-Supervised Pancreas Segmentation</a></td><td>15</td><td>0</td><td>CV</td><td>췌장 CT semi-supervised segmentation이며 로봇과 무관함</td></tr>
<tr><td>507</td><td><a href='https://arxiv.org/abs/2611.33577'>DoseSteer: Steering diffusion-based dose prediction models towards clinical targets via Dual-Response Guidance</a></td><td>15</td><td>0</td><td>CV</td><td>방사선 선량 예측 diffusion steering이며 로봇과 무관함</td></tr>
<tr><td>508</td><td><a href='https://arxiv.org/abs/2611.33671'>Look at What Matters: Learning Lesion Prototypes from Severity Labels for Domain-Generalized Diabetic Retinopathy Grading</a></td><td>15</td><td>0</td><td>CV</td><td>당뇨망막병증 등급 분류이며 로봇과 무관함</td></tr>
<tr><td>509</td><td><a href='https://arxiv.org/abs/2611.33790'>Bridging Transferability and Discriminability via Positive-Unlabeled Domain Adaptation for Building Damage Mapping Across Disaster Events</a></td><td>15</td><td>0</td><td>CV</td><td>재난 건물 피해 domain adaptation이며 로봇과 무관함</td></tr>
<tr><td>510</td><td><a href='https://arxiv.org/abs/2611.33870'>Concept Generalization in Visual Brain Decoding via Encoder-Generated fMRI</a></td><td>15</td><td>0</td><td>CV</td><td>fMRI 시각 decoding 개념 일반화로 무관함</td></tr>
<tr><td>511</td><td><a href='https://arxiv.org/abs/2611.33920'>UPP-Gauss: Ultrasound Propagation Physics-informed Gaussian Splatting for B-mode Novel-View Synthesis</a></td><td>15</td><td>0</td><td>3D Vision</td><td>초음파 B-mode novel-view Gaussian이며 로봇 연관 약함</td></tr>
<tr><td>512</td><td><a href='https://arxiv.org/abs/2611.34218'>GeoCAM: Self-Supervised Sonar-Optical Representation Learning via Geographic Overlap Supervision</a></td><td>15</td><td>0</td><td>CV</td><td>sonar-optical 자기지도 학습이며 해양 서식지 응용임</td></tr>
<tr><td>513</td><td><a href='https://arxiv.org/abs/2611.34292'>WebVibe: Multimodal Interactive Website Generation via Reverse Synthesis and Visual Self-Distillation</a></td><td>15</td><td>0</td><td>NLP</td><td>웹사이트 생성 MLLM으로 무관함</td></tr>
<tr><td>514</td><td><a href='https://arxiv.org/abs/2611.33238'>Sequential Testing on Complex and High Dimensional Data Streams Leveraging Unsupervised Model Errors</a></td><td>15</td><td>0</td><td>LG</td><td>순차 가설 검정 통계량으로 무관함</td></tr>
<tr><td>515</td><td><a href='https://arxiv.org/abs/2611.33249'>FERRETS: A Scalable Symbolic Transform for Time Series Classification</a></td><td>15</td><td>0</td><td>LG</td><td>시계열 분류 기호 변환으로 무관함</td></tr>
<tr><td>516</td><td><a href='https://arxiv.org/abs/2611.33351'>Understanding Failure Patterns in LLM-Based Mathematical Optimization Modeling</a></td><td>15</td><td>0</td><td>NLP</td><td>LLM 최적화 모델링 실패 패턴 분석임</td></tr>
<tr><td>517</td><td><a href='https://arxiv.org/abs/2611.33571'>Trigger-Invariant Contrastive Unlearning for Backdoor Removal</a></td><td>15</td><td>0</td><td>NLP</td><td>NLP 백도어 제거 unlearning으로 무관함</td></tr>
<tr><td>518</td><td><a href='https://arxiv.org/abs/2611.33875'>Random Voronoi Networks</a></td><td>15</td><td>0</td><td>LG</td><td>Random Voronoi 네트워크 최근접 이웃 변형임</td></tr>
<tr><td>519</td><td><a href='https://arxiv.org/abs/2611.33889'>On the Learnability of Model Reprogramming: A Reachability and Relabeling Perspective</a></td><td>15</td><td>0</td><td>LG</td><td>model reprogramming 학습 가능성 이론임</td></tr>
<tr><td>520</td><td><a href='https://arxiv.org/abs/2611.33900'>Correlation-Aware Evidential Fusion for Trusted Multi-View Classification</a></td><td>15</td><td>0</td><td>LG</td><td>신뢰 다중 뷰 분류 증거 융합으로 무관함</td></tr>
<tr><td>521</td><td><a href='https://arxiv.org/abs/2611.33998'>The Reference Matters: Displacement Probing for Weight-Space Learning</a></td><td>15</td><td>0</td><td>LG</td><td>weight-space 학습 probing 기준점 분석임</td></tr>
<tr><td>522</td><td><a href='https://arxiv.org/abs/2611.34581'>ChemoMAE: Self-Supervised Spectral Representation Learning Reveals Chemical Heterogeneity in Historical Wood</a></td><td>15</td><td>0</td><td>CV</td><td>역사 목재 스펙트럼 표현 학습 응용으로 로봇과 무관함</td></tr>
<tr><td>523</td><td><a href='https://arxiv.org/abs/2611.34627'>DecisionReplay: A Corpus and Offline Simulator for Ensembling Decision Models</a></td><td>15</td><td>0</td><td>LG</td><td>앙상블/라우터 평가용 코퍼스로 로봇과 무관함</td></tr>
<tr><td>524</td><td><a href='https://arxiv.org/abs/2611.34687'>Evacuation Traffic Prediction for Dynamic Transportation Networks over Multiple Hurricanes: A Generalized Graph Learning Approach</a></td><td>15</td><td>0</td><td>LG</td><td>허리케인 대피 교통 예측 응용으로 로봇과 무관함</td></tr>
<tr><td>525</td><td><a href='https://arxiv.org/abs/2611.34702'>Effect of class proportion shifts on classifier curvature</a></td><td>15</td><td>0</td><td>CV</td><td>class 비율 변화가 curvature에 미치는 영향으로 CIFAR-10 소규모 분석임</td></tr>
<tr><td>526</td><td><a href='https://arxiv.org/abs/2611.34721'>Privileged On-Policy Distillation for Calibrated Alzheimer&#x27;s Diagnosis With Missing Modalities</a></td><td>15</td><td>0</td><td>LG</td><td>알츠하이머 진단용 distillation으로 로봇과 무관함</td></tr>
<tr><td>527</td><td><a href='https://arxiv.org/abs/2611.34825'>Routeability Before Routing: Routeability Audit Protocol (RAP) and RouteabilityBench for Audited LLM Model Selection</a></td><td>15</td><td>0</td><td>LG</td><td>LLM routing 벤치마크 감사 프로토콜로 로봇과 무관함</td></tr>
<tr><td>528</td><td><a href='https://arxiv.org/abs/2611.34887'>Interpretable and Accurate Hybrid Decision Trees with Selective Case-Based Splits</a></td><td>15</td><td>0</td><td>LG</td><td>case-based split을 쓴 hybrid decision tree로 로봇과 무관함</td></tr>
<tr><td>529</td><td><a href='https://arxiv.org/abs/2611.34930'>A gene informed benchmark for BioScoring of pathology foundation models</a></td><td>15</td><td>0</td><td>LG</td><td>병리 foundation model BioScoring 벤치마크로 로봇과 무관함</td></tr>
<tr><td>530</td><td><a href='https://arxiv.org/abs/2611.33831'>Teaching a Multilingual Translation Model Regional Varieties: Castilian and Latin American Spanish, Asturian, Aragonese and Aranese with MADLAD-400-3B-MT</a></td><td>15</td><td>0</td><td>NLP</td><td>번역 모델 지역 변종 fine-tuning, 기여 작음</td></tr>
<tr><td>531</td><td><a href='https://arxiv.org/abs/2611.34016'>Evaluating Ukrainian Grammatical Competence in Language Models: Probability Versus Prompting</a></td><td>15</td><td>0</td><td>NLP</td><td>우크라이나어 문법 평가, robotics 무관함</td></tr>
<tr><td>532</td><td><a href='https://arxiv.org/abs/2611.34024'>JHealthBench-L: Clinician-Reviewed Localization of HealthBench for Rubric-Based Medical LLM Evaluation in Japan</a></td><td>15</td><td>0</td><td>NLP</td><td>HealthBench 일본어 현지화, robotics 무관함</td></tr>
<tr><td>533</td><td><a href='https://arxiv.org/abs/2611.34090'>Disciplined Anthropomorphism: How to Extend Cognitive Language to Artificial Intelligence</a></td><td>15</td><td>0</td><td>NLP</td><td>AI 인지 언어 사용에 대한 철학적 논의임</td></tr>
<tr><td>534</td><td><a href='https://arxiv.org/abs/2611.34120'>From Data Room to Report: End-to-End AI Support for M&amp;A Legal Due Diligence</a></td><td>15</td><td>0</td><td>NLP</td><td>M&amp;A 실사 AI 지원 시스템, 응용임</td></tr>
<tr><td>535</td><td><a href='https://arxiv.org/abs/2611.34179'>Familiar Words, Unfamiliar Minds: Conventionalization without Calibration in the Vocabulary of Mind</a></td><td>15</td><td>0</td><td>NLP</td><td>마음 어휘 확장에 대한 철학적 논의임</td></tr>
<tr><td>536</td><td><a href='https://arxiv.org/abs/2611.33263'>What, Who, and When: Structured Harm Assessment for Mental Health Safety via Short Reasoning</a></td><td>15</td><td>0</td><td>LG</td><td>정신건강 안전 평가, robotics 무관함</td></tr>
<tr><td>537</td><td><a href='https://arxiv.org/abs/2611.33470'>Dynamic Reasoning in Next-Gen Detection and Response: An Empirical Study of LLM Triage, Reinforcement Tuning, and Adversarial Evasion</a></td><td>15</td><td>0</td><td>LG</td><td>보안 탐지 대응 LLM triage 실증 연구임</td></tr>
<tr><td>538</td><td><a href='https://arxiv.org/abs/2611.33555'>PeerReveal: Learning to Generalize in AI Peer Review Detection</a></td><td>15</td><td>0</td><td>NLP</td><td>AI 리뷰 탐지 일반화임</td></tr>
<tr><td>539</td><td><a href='https://arxiv.org/abs/2611.33748'>REFORGE: LLM-Assisted RTL Bug Repair with Structured Context and Verification Feedback</a></td><td>15</td><td>0</td><td>LG</td><td>RTL 버그 수리 LLM임</td></tr>
<tr><td>540</td><td><a href='https://arxiv.org/abs/2611.33791'>ExtractBench Pro: The Long Tail of Document Extraction</a></td><td>15</td><td>0</td><td>LG</td><td>문서 추출 benchmark임</td></tr>
<tr><td>541</td><td><a href='https://arxiv.org/abs/2611.33821'>RadOncGym: An Agent-Based Framework for Radiotherapy Dose-Mimicking Optimization</a></td><td>15</td><td>0</td><td>RL</td><td>방사선 치료 dose 최적화 환경, 의료 응용임</td></tr>
<tr><td>542</td><td><a href='https://arxiv.org/abs/2611.34068'>Budget, Readout or Reasoning? Where Small Reasoning Models Lose Value in Auction Bidding</a></td><td>15</td><td>0</td><td>LG</td><td>경매 입찰 소형 추론 모델 분석임</td></tr>
<tr><td>543</td><td><a href='https://arxiv.org/abs/2611.34247'>Did the Model Forecast It, or Already Know It? Evaluating Large Language Models for Novel Drug-Target Prioritisation with a Temporal Knowledge-Graph Oracle</a></td><td>15</td><td>0</td><td>LG</td><td>약물 표적 예측 LLM 평가임</td></tr>
<tr><td>544</td><td><a href='https://arxiv.org/abs/2611.33643'>CariesBench: A Hierarchical Multi-view Benchmark for Dental Caries Screening and Diagnostic Reasoning from 3D Intraoral Scans</a></td><td>14</td><td>0</td><td>CV</td><td>치아 우식 3D 스캔 benchmark이며 로봇과 무관함</td></tr>
<tr><td>545</td><td><a href='https://arxiv.org/abs/2611.34310'>Interpretable identification of constitutive parameter field for three-dimensional heterogeneous and graded hyperelastic materials from full-field displacements</a></td><td>14</td><td>0</td><td>LG</td><td>재료 구성 매개변수 역추정으로 로봇 학습과 무관함</td></tr>
<tr><td>546</td><td><a href='https://arxiv.org/abs/2611.34527'>Resilience Analysis Through Automated Stage Identification and Quantitative Assessment</a></td><td>14</td><td>0</td><td>LG</td><td>시스템 resilience 단계 식별 ML로 로봇과 무관함</td></tr>
<tr><td>547</td><td><a href='https://arxiv.org/abs/2611.34602'>Learning from Crowds with Unsupervised Item Response Models</a></td><td>14</td><td>0</td><td>LG</td><td>crowd labeling용 IRT 모델로 로봇과 무관함</td></tr>
<tr><td>548</td><td><a href='https://arxiv.org/abs/2611.33231'>A comprehensive survey of deep face verification systems adversarial attacks and defense strategies</a></td><td>12</td><td>0</td><td>CV</td><td>face verification 적대 공격 survey로 로보틱스 연관 없음</td></tr>
<tr><td>549</td><td><a href='https://arxiv.org/abs/2611.33539'>Frame geometry, fascicle extrapolation and leaderboard overfitting in muscle ultrasound</a></td><td>12</td><td>0</td><td>CV</td><td>근육 초음파 측정 geometry 분석이며 로봇과 무관함</td></tr>
<tr><td>550</td><td><a href='https://arxiv.org/abs/2611.33673'>MOVR-SAR: A Multi-resolution SAR Registration Dataset under Orbit-crossing and View-variant Imaging Differences</a></td><td>12</td><td>0</td><td>CV</td><td>SAR 정합 dataset이며 로봇과 무관함</td></tr>
<tr><td>551</td><td><a href='https://arxiv.org/abs/2611.33843'>Continuous Foundation-Guided Pseudo-Label Weighting for Breast Ultrasound Domain Adaptation</a></td><td>12</td><td>0</td><td>CV</td><td>유방 초음파 domain adaptation이며 무관함</td></tr>
<tr><td>552</td><td><a href='https://arxiv.org/abs/2611.33958'>Where Does Free-Text 3D Grounding Fail? An Error Analysis of Report-Sentence Segmentation in Chest CT</a></td><td>12</td><td>0</td><td>CV</td><td>흉부 CT 3D grounding 오류 분석으로 무관함</td></tr>
<tr><td>553</td><td><a href='https://arxiv.org/abs/2611.34134'>A Calibration-Referenced Protocol for Measuring Decision Stability under Reference Bank Compression</a></td><td>12</td><td>0</td><td>CV</td><td>산업 검사 reference bank 압축 protocol이며 무관함</td></tr>
<tr><td>554</td><td><a href='https://arxiv.org/abs/2611.34240'>Analemma $\infty$: A Temporal Benchmark for Geospatial Foundation Models</a></td><td>12</td><td>0</td><td>CV</td><td>위성 시계열 benchmark로 무관함</td></tr>
<tr><td>555</td><td><a href='https://arxiv.org/abs/2611.34420'>DocSEAM: Bidirectional Cross-Page Encoding for Multi-Page Document Understanding</a></td><td>12</td><td>0</td><td>Multimodal</td><td>다중 페이지 문서 이해로 무관함</td></tr>
<tr><td>556</td><td><a href='https://arxiv.org/abs/2611.34508'>Angular Interpolation in Sparse-View Low-Dose CT Reconstruction: Placement Effects and Data-Consistency Step-Size Scaling</a></td><td>12</td><td>0</td><td>CV</td><td>저선량 CT 재구성 분석으로 로봇과 무관함</td></tr>
<tr><td>557</td><td><a href='https://arxiv.org/abs/2611.34649'>Atunda: Building an Afrogenic Dance Movement Dataset for AI-Driven Classification</a></td><td>12</td><td>0</td><td>CV</td><td>아프리카 춤 동작 데이터셋으로 로봇 무관함</td></tr>
<tr><td>558</td><td><a href='https://arxiv.org/abs/2611.34899'>Enhancing Maritime Domain Awareness using Latent Space Representations</a></td><td>12</td><td>0</td><td>CV</td><td>해양 영역 인식 위성 임베딩 응용임</td></tr>
<tr><td>559</td><td><a href='https://arxiv.org/abs/2611.33168'>Temporal Exposure to Byzantine Vulnerability Under Intermittent Participation in Federated Learning</a></td><td>12</td><td>0</td><td>LG</td><td>연합학습 비잔틴 취약성 분석으로 무관함</td></tr>
<tr><td>560</td><td><a href='https://arxiv.org/abs/2611.33325'>Sparse Adaptation for In-Context Learning on Data Streams</a></td><td>12</td><td>0</td><td>LG</td><td>IoT 스트림 in-context 학습으로 무관함</td></tr>
<tr><td>561</td><td><a href='https://arxiv.org/abs/2611.33937'>InstructTTS-OPD: On-Policy Distillation for Multi-Objective Instruction-Following TTS</a></td><td>12</td><td>0</td><td>Audio</td><td>instruction TTS on-policy distillation임</td></tr>
<tr><td>562</td><td><a href='https://arxiv.org/abs/2611.34206'>Text-Conditioned Low-Rank Adaptation of Time-Series Foundation Models for Multimodal Forecasting</a></td><td>12</td><td>0</td><td>LG</td><td>텍스트 조건 시계열 LoRA 예측임</td></tr>
<tr><td>563</td><td><a href='https://arxiv.org/abs/2611.34270'>LLM-coupled interpretable tool wear monitoring with multi-evidence reasoning in CNC machining</a></td><td>12</td><td>0</td><td>LG</td><td>CNC 공구 마모 모니터링 응용으로 로봇 학습과 무관함</td></tr>
<tr><td>564</td><td><a href='https://arxiv.org/abs/2611.33432'>Open-Source FUTO Keyboard Layouts and Predictive Text for a Few Endangered Languages</a></td><td>12</td><td>0</td><td>NLP</td><td>소수 언어 키보드 자원 공개, 연구 기여 작음</td></tr>
<tr><td>565</td><td><a href='https://arxiv.org/abs/2611.33871'>Contextual language representations link narrative processing to language and literacy in children</a></td><td>12</td><td>0</td><td>NLP</td><td>fMRI 서사 처리 연구, robotics 무관함</td></tr>
<tr><td>566</td><td><a href='https://arxiv.org/abs/2611.33974'>Auto-Features: An LLM-Assisted Corpus for Contextual Recognition of Standard and Optional Car Features</a></td><td>12</td><td>0</td><td>NLP</td><td>자동차 광고 feature corpus, 응용임</td></tr>
<tr><td>567</td><td><a href='https://arxiv.org/abs/2611.34823'>The Linguistic Knowledge Benchmark: Do Language Models Know the Foundations of Early-Grade Literacy?</a></td><td>12</td><td>0</td><td>NLP</td><td>초기 문해 언어 지식 benchmark임</td></tr>
<tr><td>568</td><td><a href='https://arxiv.org/abs/2611.34832'>Proverbs As A Window On Collective Prescriptions</a></td><td>12</td><td>0</td><td>NLP</td><td>속담 집단 규범 분석임</td></tr>
<tr><td>569</td><td><a href='https://arxiv.org/abs/2611.33788'>InterGenEHR$^+$: An Interactive Framework for Natural Language-Conditioned Generation of Longitudinal Patient Trajectories</a></td><td>12</td><td>0</td><td>LG</td><td>EHR 생성 interactive 프레임워크, 의료 응용임</td></tr>
<tr><td>570</td><td><a href='https://arxiv.org/abs/2611.34407'>Agentic Waterfall: An Intent-Driven Information Discovery Framework for Reclaiming User Control in the Attention Economy</a></td><td>12</td><td>0</td><td>LG</td><td>개인화 정보 탐색 agentic feed임</td></tr>
<tr><td>571</td><td><a href='https://arxiv.org/abs/2611.34432'>Evaluating Aviation Safety Knowledge Extraction with SmolLM2: From Zero-Shot to Retrieval-Grounded Prompting</a></td><td>12</td><td>0</td><td>NLP</td><td>항공 안전 지식 추출임</td></tr>
<tr><td>572</td><td><a href='https://arxiv.org/abs/2611.34490'>An Exact Branch-Price-and-Cut Algorithm for the Vehicle Routing Problem with Floating Targets</a></td><td>10</td><td>1</td><td>LG</td><td>VRP 정확해 알고리즘으로 최적화 일반 문제임</td></tr>
<tr><td>573</td><td><a href='https://arxiv.org/abs/2611.33860'>Structured Noise Diffusion for Echocardiography Haze Removal</a></td><td>10</td><td>0</td><td>CV</td><td>심초음파 haze 제거로 무관함</td></tr>
<tr><td>574</td><td><a href='https://arxiv.org/abs/2611.34006'>Manga Page Parser: Comprehensive Visual Parsing through Local Story Understanding</a></td><td>10</td><td>0</td><td>CV</td><td>만화 페이지 파싱으로 무관함</td></tr>
<tr><td>575</td><td><a href='https://arxiv.org/abs/2611.34025'>Incorporating the Knowledge Distillation to Improve the EfficientNet Transfer Learning Capability</a></td><td>10</td><td>0</td><td>CV</td><td>EfficientNet 증류로 신규성 낮음</td></tr>
<tr><td>576</td><td><a href='https://arxiv.org/abs/2611.34153'>HSTTA: Hierarchical Selective Test-Time Adaptation for Label-Free Cross-Subject EEG-to-Image Retrieval</a></td><td>10</td><td>0</td><td>CV</td><td>EEG-image 검색 TTA로 무관함</td></tr>
<tr><td>577</td><td><a href='https://arxiv.org/abs/2611.34568'>Physics-Guided Generative Modelling of Oxy-Combustion Flame Images: From Conditional LSGANs to Denoising Diffusion Models</a></td><td>10</td><td>0</td><td>CV</td><td>연소 화염 이미지 생성으로 로봇과 무관함</td></tr>
<tr><td>578</td><td><a href='https://arxiv.org/abs/2611.34860'>DocDUR-Net: Degradation-Aware Unified Document Image Restoration</a></td><td>10</td><td>0</td><td>CV</td><td>문서 이미지 복원으로 로봇 무관함</td></tr>
<tr><td>579</td><td><a href='https://arxiv.org/abs/2611.33167'>Code availability is not enough: schemas for documenting and extending data analysis</a></td><td>10</td><td>0</td><td>LG</td><td>데이터 분석 문서화 스키마로 무관함</td></tr>
<tr><td>580</td><td><a href='https://arxiv.org/abs/2611.33178'>Geophysics-informed invertible operator network for Bayesian geophysical inversion</a></td><td>10</td><td>0</td><td>LG</td><td>지구물리 베이지안 역문제로 무관함</td></tr>
<tr><td>581</td><td><a href='https://arxiv.org/abs/2611.33179'>Deep Learning-Based Mesoscopic Emission Modeling</a></td><td>10</td><td>0</td><td>LG</td><td>교통 배출 모델링으로 무관함</td></tr>
<tr><td>582</td><td><a href='https://arxiv.org/abs/2611.33395'>Federated Learning with Uncertainty Quantification on Pseudo Label Exchange</a></td><td>10</td><td>0</td><td>LG</td><td>SPDE 연합 연산자 학습으로 무관함</td></tr>
<tr><td>583</td><td><a href='https://arxiv.org/abs/2611.33424'>Yet Another Concept Drift Benchmark? A Principled Framework for Evaluating Drift Detectors</a></td><td>10</td><td>0</td><td>LG</td><td>concept drift 탐지기 평가 프레임워크임</td></tr>
<tr><td>584</td><td><a href='https://arxiv.org/abs/2611.33523'>A Perturbation-Driven Framework for Sensitivity Analysis of Dimensionality Reduction</a></td><td>10</td><td>0</td><td>LG</td><td>차원 축소 민감도 분석으로 무관함</td></tr>
<tr><td>585</td><td><a href='https://arxiv.org/abs/2611.33557'>DiffER$^2$: Diffusion Ensembles for Retrosynthesis Prediction with SMILES Adapted Particle Guidance</a></td><td>10</td><td>0</td><td>LG</td><td>역합성 예측 확산 앙상블로 화학 도메인임</td></tr>
<tr><td>586</td><td><a href='https://arxiv.org/abs/2611.33652'>Self-supervised Clipped-objective Reinforcement Leaning Framework for Risk-aware Portfolio Management</a></td><td>10</td><td>0</td><td>RL</td><td>포트폴리오 관리 RL 금융 응용임</td></tr>
<tr><td>587</td><td><a href='https://arxiv.org/abs/2611.33732'>CovNovBench: A Benchmark for Evaluating Time Series Foundation Models under Covariate Novelty</a></td><td>10</td><td>0</td><td>LG</td><td>시계열 foundation model 공변량 벤치마크임</td></tr>
<tr><td>588</td><td><a href='https://arxiv.org/abs/2611.33766'>Don&#x27;t Waste the Population: Post-Anneal Refinement for Combinatorial Optimization</a></td><td>10</td><td>0</td><td>LG</td><td>조합 최적화 후처리 개선으로 무관함</td></tr>
<tr><td>589</td><td><a href='https://arxiv.org/abs/2611.34101'>AlignPre: Skill-Aligned Post-Training for Latent-Free Generative Precipitation Nowcasting</a></td><td>10</td><td>0</td><td>LG</td><td>강수 nowcasting 생성 post-training임</td></tr>
<tr><td>590</td><td><a href='https://arxiv.org/abs/2611.34258'>Train-Only-Constrained LM for Synthetic Clinical Trajectories: Leak-Safe Calibration and Auditable Dynamics</a></td><td>10</td><td>0</td><td>LG</td><td>임상 시계열 합성 파이프라인으로 로봇과 무관함</td></tr>
<tr><td>591</td><td><a href='https://arxiv.org/abs/2611.34629'>Predicting acute food crises and discovering actionable drivers with causal machine learning</a></td><td>10</td><td>0</td><td>LG</td><td>식량 위기 예측 causal ML 응용으로 로봇과 무관함</td></tr>
<tr><td>592</td><td><a href='https://arxiv.org/abs/2611.34779'>Adaptive Reliability Reserves for Residential Battery Fleets</a></td><td>10</td><td>0</td><td>LG</td><td>주거용 배터리 reserve 최적화로 로봇과 무관함</td></tr>
<tr><td>593</td><td><a href='https://arxiv.org/abs/2611.34137'>How resampling method can help us: Improving the Delta model</a></td><td>10</td><td>0</td><td>NLP</td><td>Delta 저자 판별 resampling 개선임</td></tr>
<tr><td>594</td><td><a href='https://arxiv.org/abs/2611.34539'>EPPC-CARE: Staged Hierarchical Annotation of Communication Behaviors in Secure Patient-Provider Messages</a></td><td>10</td><td>0</td><td>NLP</td><td>환자 메시지 annotation, 의료 응용임</td></tr>
<tr><td>595</td><td><a href='https://arxiv.org/abs/2611.33322'>Brand Recall and Category Accuracy in Language Models: An Audit of 1,000 B2B SaaS Brands</a></td><td>10</td><td>0</td><td>LG</td><td>B2B SaaS 브랜드 회상 감사임</td></tr>
<tr><td>596</td><td><a href='https://arxiv.org/abs/2611.33664'>SlicePlanner: Logic-Guided Agentic AI for Online QoS-Aware Network Slicing in Open RAN</a></td><td>10</td><td>0</td><td>LG</td><td>O-RAN 네트워크 슬라이싱 agent, robotics 무관함</td></tr>
<tr><td>597</td><td><a href='https://arxiv.org/abs/2611.33713'>Nepali Currency Denomination Classification Using Convolutional Neural Networks (CNNs) and MobileNetV2: An Experimental Comparison</a></td><td>8</td><td>0</td><td>CV</td><td>네팔 지폐 분류 CNN 비교로 신규성이 없음</td></tr>
<tr><td>598</td><td><a href='https://arxiv.org/abs/2611.33750'>Spectral Colorimetry Based on GMoE for Temperature Measurement in Explosion Fields</a></td><td>8</td><td>0</td><td>CV</td><td>폭발 영역 온도 측정으로 로봇과 무관함</td></tr>
<tr><td>599</td><td><a href='https://arxiv.org/abs/2611.33792'>Spatial Transcriptomics Prediction from Histology via Topology-Informed Graph Attention and Gene-Semantics Conditioning</a></td><td>8</td><td>0</td><td>CV</td><td>조직 이미지 기반 spatial transcriptomics 예측이며 무관함</td></tr>
<tr><td>600</td><td><a href='https://arxiv.org/abs/2611.33940'>TAT-Det: A Dataset for Testicular Appendage Torsion Detection and Segmentation in Ultrasound Images</a></td><td>8</td><td>0</td><td>CV</td><td>고환 부속기 염전 초음파 dataset이며 무관함</td></tr>
<tr><td>601</td><td><a href='https://arxiv.org/abs/2611.34781'>Comparative Study of Deep Learning Architectures for Brain Tumour Classification</a></td><td>8</td><td>0</td><td>CV</td><td>뇌종양 분류 아키텍처 비교로 무관함</td></tr>
<tr><td>602</td><td><a href='https://arxiv.org/abs/2611.33163'>Quantum Machine Learning for Signature Forgery Detection</a></td><td>8</td><td>0</td><td>LG</td><td>양자 ML 서명 위조 탐지로 무관함</td></tr>
<tr><td>603</td><td><a href='https://arxiv.org/abs/2611.33237'>Resource-Efficient Multimodal Fusion for Early Rice Blast Forecasting in Sustainable Agriculture</a></td><td>8</td><td>0</td><td>LG</td><td>벼 도열병 예측 응용임</td></tr>
<tr><td>604</td><td><a href='https://arxiv.org/abs/2611.33248'>Typical Angina, Reversed: A Long-Standing Documentation Error in the UCI Heart Disease Data</a></td><td>8</td><td>0</td><td>LG</td><td>UCI 심장 데이터 문서 오류 지적임</td></tr>
<tr><td>605</td><td><a href='https://arxiv.org/abs/2611.33332'>Online Prediction System for Proactive Autoscaling</a></td><td>8</td><td>0</td><td>LG</td><td>오토스케일링 시계열 예측 시스템임</td></tr>
<tr><td>606</td><td><a href='https://arxiv.org/abs/2611.33335'>FlowersBench: A FluidFlower-Inspired Dataset for Benchmarking Carbon Storage Surrogates Across Geological Structures</a></td><td>8</td><td>0</td><td>LG</td><td>탄소 저장 surrogate 벤치마크로 무관함</td></tr>
<tr><td>607</td><td><a href='https://arxiv.org/abs/2611.33364'>Discovering Explicit Magnetic Core-Loss Equations via Symbolic Sparse Identification</a></td><td>8</td><td>0</td><td>LG</td><td>자성 코어 손실 방정식 발견으로 무관함</td></tr>
<tr><td>608</td><td><a href='https://arxiv.org/abs/2611.33645'>Pretraining for Forecasting in Relational Databases</a></td><td>8</td><td>0</td><td>LG</td><td>관계형 DB 예측 사전학습으로 무관함</td></tr>
<tr><td>609</td><td><a href='https://arxiv.org/abs/2611.33647'>The Danger of Double Precision: Working Precision as a Hidden Constraint in Gaussian Process Maximum Likelihood</a></td><td>8</td><td>0</td><td>LG</td><td>GP 배정밀도 문제 수치 분석임</td></tr>
<tr><td>610</td><td><a href='https://arxiv.org/abs/2611.33973'>Kolpona: An Agentic Framework with Gradient-Free Neuron Programming for RTL Generation</a></td><td>8</td><td>0</td><td>NLP</td><td>RTL 생성 에이전트로 무관함</td></tr>
<tr><td>611</td><td><a href='https://arxiv.org/abs/2611.33985'>MolGPAO: Molecular Generative Pre-trained Autoregressive Octree with Speculative Decoding and Sub-Millisecond Seam Healing for 3D Molecules</a></td><td>8</td><td>0</td><td>LG</td><td>3D 분자 옥트리 생성으로 무관함</td></tr>
<tr><td>612</td><td><a href='https://arxiv.org/abs/2611.34012'>CARROT: Competitive Adaptive Graph Clustering via Semi-Relaxed Optimal Transport</a></td><td>8</td><td>0</td><td>LG</td><td>그래프 클러스터링 optimal transport임</td></tr>
<tr><td>613</td><td><a href='https://arxiv.org/abs/2611.34019'>Assessing the Physical Interpretability of AlphaEarth Foundation Embeddings Through Multi-Sensor Satellite Time-Series Benchmarking for Agricultural Mapping</a></td><td>8</td><td>0</td><td>LG</td><td>농업 매핑 위성 임베딩 벤치마크임</td></tr>
<tr><td>614</td><td><a href='https://arxiv.org/abs/2611.34088'>Feature Engineered Reinforcement Learning for S-pair Selection in Buchberger&#x27;s Algorithm</a></td><td>8</td><td>0</td><td>RL</td><td>Buchberger S-pair 선택 RL로 무관함</td></tr>
<tr><td>615</td><td><a href='https://arxiv.org/abs/2611.34106'>SysBio-SR: Benchmarking Symbolic Regression for Trajectory Fidelity and Mechanism Recovery in Systems Biology</a></td><td>8</td><td>0</td><td>LG</td><td>시스템 생물학 symbolic regression 벤치마크임</td></tr>
<tr><td>616</td><td><a href='https://arxiv.org/abs/2611.34511'>SMOTE 25 Years of Magic: What Has Been Done, What the Evidence Shows, and Whom It Reached</a></td><td>8</td><td>0</td><td>LG</td><td>SMOTE 25년 리뷰로 로봇과 무관함</td></tr>
<tr><td>617</td><td><a href='https://arxiv.org/abs/2611.34573'>Investigating the efficacy of vortex beam speckle patterns for the recognition of atmospheric turbulence and fractional topological charge with a deep learning model</a></td><td>8</td><td>0</td><td>LG</td><td>대기 난류 하의 vortex beam 인식으로 로봇과 무관함</td></tr>
<tr><td>618</td><td><a href='https://arxiv.org/abs/2611.34618'>Automated Batch-Variable Selection for ComBat-Based Radiomic Harmonization</a></td><td>8</td><td>0</td><td>LG</td><td>radiomic harmonization 변수 선택으로 로봇과 무관함</td></tr>
<tr><td>619</td><td><a href='https://arxiv.org/abs/2611.34131'>Is Sara Omar the true author of Dødevaskeren (The Dead Washer)? Authorship attribution in Danish literature</a></td><td>8</td><td>0</td><td>NLP</td><td>소설 저자 판별 사례 연구임</td></tr>
<tr><td>620</td><td><a href='https://arxiv.org/abs/2611.34011'>Honest but Wrong: Formalizing Retraction in the Ethics of Speech Acts</a></td><td>8</td><td>0</td><td>LG</td><td>철회의 윤리 형식화, 철학 논의임</td></tr>
<tr><td>621</td><td><a href='https://arxiv.org/abs/2611.34049'>Decentralized Clustered Federated Learning for Cellular Traffic Forecasting over LEO Constellations</a></td><td>5</td><td>0</td><td>LG</td><td>LEO 연합학습 트래픽 예측으로 무관함</td></tr>
<tr><td>622</td><td><a href='https://arxiv.org/abs/2611.34104'>Do Machine Learning Ensembles Beat Published Quotas? Target Parameterization, Censored Baselines, and Conformal Intervals Under Admissions Reform</a></td><td>5</td><td>0</td><td>LG</td><td>입학 정원 예측 앙상블 비교임</td></tr>
<tr><td>623</td><td><a href='https://arxiv.org/abs/2611.34154'>When High Capacity Becomes Undeployable: Pore-Filling Constraints for Multi-Objective Optimization of Direct Air Capture Sorbents</a></td><td>5</td><td>0</td><td>LG</td><td>CO2 흡착제 최적화로 무관함</td></tr>
<tr><td>624</td><td><a href='https://arxiv.org/abs/2611.34166'>Cell-Type-Specific Expression Is Hard to Predict from Bulk, but It Is Still Useful</a></td><td>5</td><td>0</td><td>LG</td><td>단일세포 deconvolution 응용임</td></tr>
<tr><td>625</td><td><a href='https://arxiv.org/abs/2611.33173'>The Bundesrat corpus: A dataset of political discourse in the German Federal Council</a></td><td>5</td><td>0</td><td>NLP</td><td>독일 연방참사원 담론 코퍼스로 로봇과 무관함</td></tr>
</tbody></table>

</details>
