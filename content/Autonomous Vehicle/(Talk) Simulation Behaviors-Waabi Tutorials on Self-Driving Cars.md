---
title: (Talk) Simulation Behaviors-Waabi Tutorial on Self-Driving Cars
created: 2025-11-21 14:00
modified: 2025-11-23 13:50
tags:
    - AV
    - Talk
keywords:
    - Simulation
    - AD-Trend
type: literature-note
kanban: in-progress
published: CVPR-2024
affiliations:
    - waabi
mocs: []
---

# (Talk) Simulation Behaviors-Waabi Tutorial on Self-Driving Cars

## Overview

## Scenarios란?

시나리오는 시뮬레이션의 콘텐츠를 형성하며 다음을 명시한 것이다.

- 시나리오로 기술하는 장면(**scene**)에 어떤 행위자 (**actor**)가 있는가?
- 장면은 어떤 환경과 교통 구성요소를 가지고 있는가?
- 행위자들이 어떤 초기 위치에 있고 시간이 지남에 따라 어떤 행동을 하는가?

### 시나리오 구성 요소

시나리오의 구성요소는 다음과 같다.

- 환경 (Environment): 자차의 위치, 도로 지형(road topology), 도로 형태, 기상 조건 등
- 초기 조건(Initial condition): 행위자들의 종류, 초기 위치/속도/방향 등
- 행위자 행동 (Actor behavior): 행위자들이 시간이 지남에 따라 수행하는 행동 혹은 자차와의 상호작용 시 행동 전략

### 시나리오 유형

일반적인 시나리오의 유형은 다음과 같다.

- 표준 교통 시나리오 (Nominal Traffic Scenarios)
    - 도심 혹은 고속도로에서 흔히 접할 수 있는 일반적인 교통상황에 대한 시나리오
    - AV가 도로에서 일반적으로 마주칠 상황을 훈련하거나 테스트하는데 활용할 수 있다.
- 구조화된 테스트 시나리오 (Structured Test Scenarios)
    - 실제로는 드물게 발행하는 상황(**corner case**)을 시뮬레이션을 통해 통제 및 반복가능한 상태에서 테스트하기 위해 사용하는 시나리오
    - 시뮬레이션을 통해 드물고 위험한 상황에서 개발한 SW가 어떤 성능을 보이는지 더 안전하고 정밀하며 확장가능하게 테스트할 수 있다.
    - 매개변수 공간 내에서 다양한 변형을 지능적으로 샘플링하여 성능 결정 경계(decision boundary)를 파악하는데 활용한다.
- 희소하지만 안전 관련 중요 시나리오 (Rare but Safety Critical Scenarios)
    - 희소하고 위험한 상황에서 AV가 어떻게 행동하는지 검증하고 안전 문제를 조기에 발견하기 위해 사용하는 시나리오
    - 구조화된 테스트 시나리오와 달리 극도로 위험하고 공격적인 상황(**long-tail case**)에서 안전 문제가 있는지 확인하기 위해 사용된다.
        - 롱테일 케이스는 코너 케이스 중에서 성능 결정 경계에서 멀리 떨어져서 샘플링된 케이스로 이해하도록 하자.
        - 이런 경우에 AV SW가 안정적으로 동작하느냐보다는 안전문제가 발행하지 않느냐를 테스트하는 목적으로 사용된다고 이해하자.
- 로그 기반 반응형 폐루프 시뮬레이션과 변 (Reactive closed-loop simulation from logs + variations)
    - 실제 수집된 로그를 기반으로 폐루프 시뮬레이션을 수행하며 다양한 변형에 대한 **what-if** 시나리오를 테스트할 수 있다.

## Scenario Creation

시나리오를 생성하는 방법에는 크게 다음의 4가지 접근 방식이 있다.

- 수동 생성([[#Manual Creation]])
- 절차적 생성 ([[#Procedural Generation]]
- 실자 로그에서 추출 ([[#Extract from Real Logs]]
- 생성형 모델로 생성 ([[#Generation using Generative Models]])

### 시나리오 생성 방식

#### Manual Creation

- 사람이 직접 특정 양식(e.g. XML)이나 도메인 특정 언어(DSL, Domain Specipic Language)로 시나리오의 다양한 측면을 하나하나 지정하여 생성한다.
- 다음의 장/단점을 갖는다.
    - (+) 시나리오에 대한 정확한 제어가 가능하다.
    - (+) 중요한 시나리오를 정밀하게 재현할 수 있다.
    - (-) 시뮬레이터가 지원하는 측면만 제어 가능하여 현실성이 떨어지며 다양성이 제한된다.
    - (-) 생성의 자동화가 어려워 대규모 생성에 많은 제약이 있다.
- 참고 사례/논문
    - ASAM OpenSCENARIO 1.0/2.0
    - SCENIC: A Language for Scenario Specification and Scene Generation (PLDI19)
    - Large-Scale Simulation and Variation with CARLA (Applied-Intuition 2022)
    - Waymo Simulated Driving Behavior in Reconstructed Fatal Crashes within an Autonomous Vehicle Operating Domain (2021)

#### Procedural Generation

- 미리 정의된 규칙이나 상황과 매개변수를 조합하여 시나리오를 대규모로 생성한다.
    - 주로 장면 레이아웃과 맵을 자동으로 생성하는데 집중한 연구가 많다.
- 다음의 장/단점을 갖는다.
    - (+) 대규모의 변형 시나리오를 빠르고 손쉽게 생성할 수 있다.
    - (+) 필요한 시나리오에 대한 사전 정보를 반영할 수 있다.
    - (-) 좋은 규칙과 사전 상황을 설계하는 것은 어렵고 많은 시간을 요구한다.
    - (-) 절차적 생성을 지원하는 툴에 따라 시나리오의 현실성과 다양성이 제약된다.
- 참고 사례/논문
    - Structured Domain Randomization: Bridging the Reality Gap by Context-Aware Synthetic Data (2018)
        - 사실적인 장면 레이아웃과 지도를 동시에 절차적으로 생성한다.
    - Initial Scene Configuration for Highway Traffic Propagation (ITSC15)
        - 사실적인 장면 레이아웃을 절차적으로 생성한다.
    - MetaDrive: Composing Diverse Driving Scenarios for Generalizable Reinforcement Learning (PAIM22)
        - 사실적인 지도를 절차적으로 생성한다.
    - Scaling Simulation (Aurora 2022)

#### Extract from Real Logs

- 실제 주행을 통해 수집한 로그에서 시나리오를 추출하고 다양한 변형을 가미하여 시나리오를 생성한다.
    - 행위자의 매개변수를 변경하거나 행위자의 행동을 변형 혹은 추가할 수 있다.
    - **fuzzing**을 통해서 변형을 만들 수 있다.
- 다음의 장/단점을 갖는다.
    - (+) 손쉽게 현실적인 시나리오를 생성할 수 있다.
    - (-) 수집한 로그에서 데이터를 추출하므로 희소한 시나리오를 생성하는데 본질적인 제약이 있다.
- 참고 사례/논문
    - How Simulation turns one flashing yellow light into thousands fo hours of experience (waymo 2017)
    - NuPlan: A Closed-loop ML-based Planning benchmark for autonomous vehicles (motional, 2021)
    - Nocturne: A Scalable Driving Benchmark for bringing multi-agent learning one step closer to the real-world (arXiv22)
    - Waymax: An Accelerated, Data-Driven Simulation for Large-Scale Autonomous Driving Research (NeurIPS24)

#### Generation using Generative Models

- 생성 모델을 사용하여 현실적인 시나리오를 대규모로 자동 생성한다.
- 다음의 장단점을 갖는다.
    - (+) 데이터 기반으로 수작업이나 사전 작업 규칙에 의존하지 않는다.
    - (+) 데이터가 많을 수록 현실성과 다양성이 개선될 수 있다.
    - (-) 모델 구조에 따라 제어가능성이 제약된다.
        - 현재 연구는 행위자 배치에 집중되어 있다.
        - 학습한 데이터에 따라 시나리오가 편향되어 생성된다.
        - 원하는 시나리오를 생성하는 것이 쉽지 않다.
    - (-) 데이터 기반이므로 구조화된 테스트나 희소 안전 관련 테스트에 부적합하다.
- 참고 사례/논문
    - SceneGen: Learnging to Generate Realistic Traffic Scenes (CVPR21)
        - Autoregressive 방식
    - SimNet: Learning Reactive Self-driving Simulation form Real-world Observations (ICRA21)
        - GAN 기반
    - Conditional Permutation Invariant Flows (arXiv22)
        - Normalizing Flow 기반
    - TorchDriveEnv: A Reinforcement Learning Benchmark for Autonomous Driving with Reactive, Realistic and Diverse Non-Playable Characters (arXiv24)
        - Normalizing Flow 기반
    - Scenario Diffusion: Controllable Driving Scenario Generation with Diffusion (NeurIPS24)
        - Diffusion 기반
    - SLEDGE: Synthesizing Simulation Environments for Driving Agents with Generative Models (axXiv24)
        - Diffusion 기반

##### Controllability of Generative Models

생성 모델을 이용하여 시나리오를 생성하는 경우 크게 다음의 3가지 접근 방식을 사용한다.

- Guidence Functions
    - 안내 함수를 이용하여 생성 모델의 샘플링 과정을 현실성과 제약 충족도가 높은 (e.g. 행위자 수나 종류, 밀도와 배치 등)쪽으로 유도한다.
    - SceneControl: Diffusion for Controllable Traffic Scene Generation (ICRA24)
- Templates
    - 현실 시나리오 DB에서 주어진 조건에 따라 일련의 템플릿 시나리오를 검색하고 이를 조합하여 유사한 새로운 시나리오를 생성하는 방식이다.
    - Foretellix의 시나리오 snippet을 조합한 방식으로 이해된다.
    - RealGen: Retrieval Augmented Generation for Controllable Traffic Scenarios (arXiv24)
- Natural Languages
    - [[LLM]]을 사용하여 사용자의 자연어 설명을 구조화된 설명으로 변환하고 이를 기반으로 시나리오를 생성한다.
    - 가장 유연하고 사용자 친화적인 인터페이스를 제공한다.
    - Language-contioned Traffic Generation (CoRL23)
    - ChatSim: Editable Scene Simulation for Autonomous Driving via LLM-Agent Collaboration (CVPR24)
    - ChatScene: Knowledge-enabled Safety-Critical Scenario Generation for Autonomous Vehicles (CVPR24)

### Maximizing Coverage

- 실세계의 시나리오는 방대하고 복잡하며 모든 시나리오에 대해서 시뮬레이션 테스트를 수행하는 것은 불가능하다.
- 자율주행 SW 배포 시 안전성을 검증하기 위해서
    - 실제 발생할 수 있고 유의미한 테스트 커버리지를 찾고
    - 해당 커버리지에서 분석할 수 있는 성능 지표를 식별해야 한다.
- 효율적으로 테스트 커버리지를 최대화하며 성능을 특징짓는 지능형 알고리즘이 필요하다.
- 현재의 연구는 지능형 샘플링(**intelligent sampling**)에 기반하며, 다음의 과정을 거쳐 이뤄진다.
    - 랜덤 샘플링된 시나리오를 통해 성능을 분석한다.
    - 기존 샘플을 기반으로 최대의 정보 이득(information gain)을 얻을 수 있도록 새로운 시나리오를 생성한다.
    - 이를 반복하며 커버리지가 최대가 되고 결정 경계를 구축할 수 있도록 반복적으로 테스트한다.
- 참고 논문
    - GUARD: Towards Scalable Coverage-Based Testing of Autonomous Vehicles (CoRL23)
    - HiddenGems: Efficient safety boundary detection with active learing (IROS22)

## Actor Simulation

### Actor Simulation 특징

- 행위자 시뮬레이션은 맵과 시나리오 초기 상태가 주어졌을 때, 장면 내의 행위자들이 시간이 지나거나 행위자들끼리 상호작용하며 각자의 동적 상태가 어떻게변하는지를 시뮬레이션한다.
- 행위자 시뮬레이션은 다음을 만족해야 한다.
    - 현실성 (Realism): 현실과 시뮬레이션 사이의 도메인 간극이 낮아야 한다.
    - 다양성 (Diversity): 현실 세계의 다양한 상황을 모사할 수 있어야 한다.
    - 제어가능성 (Controllability): 원하는 상황과 조건에서 시뮬레이션할 수 있어야 한다.
- 모델링해야하는 행위자는 크게 강체 행위자(rigid acctor)와 변형 가능 행위자(deformable actor)가 있다.
    - Rigid actor 관련 연구
        - Symphony (ICRA22)
        - MixSim (CVPR23)
    - Deformable actor 관련 연구
        - PFNN (SIGGRAPH17)
        - AMP (SIGGRAPH21)
        - Trace and Pac (CVPR23)
- 동작 계획(**Motion Planning**)과 동작 예측(**Motion Forecasting**)과의 차이는 아래의 표와 같다.
    - 동작 예측의 경우 개루프이기 때문에 예측이 미래의 입력에 영향을 미지치 않는다.
    - 행위자 시뮬레이션의 경우는 폐푸프이므로 예측이 미래의 입력에 영향을 끼친다.

| 구분 | Actor Simulation                                       | Motion Planning                        | Motion Forecasting                   |
| ---- | :----------------------------------------------------- | :------------------------------------- | ------------------------------------ |
| 목표 | 운전행동 분포에 기반한 시뮬레이션 수행                 | 안전하고 효율적인 최적의 운전행동 학습 | 운전 행동의 분포 예측                |
| 정보 | 행위자의 목표와 의도를 포함한 완벽한 상태정보 활용가능 | 부분적이고 노이즈가 섞인 센서 관측치   | 부분적이고 노이즈가 섞인 센서 관측치 |
| 루프 | 폐루프                                                 | 폐루프                                 | 개루프                               |

### Realistic Actor Behaviors

현실적인 행위자의 행동을 모사하기 위해서 다음과 같은 접근 방식이 있다.

- [[#Rule-based Behaviors]]
- [[#Behavior Cloning with Differentiable Simulation]]
- [[#Behavior Cloning with Interactive Experts]]
- [[#Behavior Cloning with Reinforcement Learning]]
- [[#Behavior Cloning with Data Augmentaion]]

#### Rule-based Behaviors

- 기존에는 룰기반으로 행위자의 행동을 모델링하였다.
- 개념적으로 간단하고 구현하기 쉽지만, 규칙으로 표현할 수 있는 상황이 제한되어 비현실적이고 다양성이 떨어진다.
- 특히, 롱테일 행동을 룰 기반으로 다루기는 어렵다.
    - 비정형 행동 (non-compliant behavior), 다양한 행위자 스타일, 행위자들 사이의 다양한 상호작용 등
- 관련 연구
    - IDM: Congested Traffic States in Empirical Observation and Microscopic Simulations (2000)
    - MOBIL: General Lane-Changing Model MOBIL for Car-Following Modles (2007)

#### Simple Behavior Cloning

- 행동 복제는 인간의 운전 데이터셋(상태-행동 쌍)을 수집하고 지도학습을 통해 다음 스텝의 정책(policy)를 학습하는 것을 말한다.
- 다음의 장/단점을 갖는다.
    - (+) 간단하고 구현이 쉽고 별도의 개발자 노력없이 데이터 셋의 크기로 성능을 향상시킬 수 있다.
    - (-) 행동 복제 모델이 학습한 행동 분포가 실제 분포와 다른 공변량 변화 (**covariate shift**, [[Batch Normalization|링크]])가 발생할 수 있다.
        - 분포 외 (OoD, Out-of-Distribution) 상태에서 대해서 잘못된 정책을 출력할 수 있다.
    - (-) 폐루프 상에서 정책 오류가 복합적으로 누적될 수 있다.
- 참고 논문
    - SimNet: Learning Reactive Self-driving Simulation from Real-world Observation (ICRA21)
    - PredictionNet: Real-Time Joint Probabilistic Traffic Prediction for Planning, Control and Simulation (ICRA22)

#### Advanced Behavior Cloning

##### Behavior Cloning with Auxiliary Losses

- 행동 복제 모델에 보조 손실함수를 추가하여 정규화(**regularization**)를 수행한다.
    - 손실함수를 메인 손실함수(**imitation loss**)와 정규화를 위한 보조 손실함수(**common sense loss**)로 구성한다.
    - 보조 손실함수는 해당 모델이 교통 규칙을 준수하거나 충돌을 피할 수 있도록 설계하거나 정책의 불확실성이 증가하는 행동에 대해서 페널티를 부여한다.
- 다음의 장/단점을 갖는다.
    - (+) 기존 행동 모델의 변형을 최소화하면서 간단하게 성능을 개선할 수 있다.
    - (+) 손실 함수를 통해서 일반적인 상식을 모델에 인코딩할 수 있다.
    - (-) 손실함수 설계가 까다롭다.
    - (-) 정책 불확실성이 커지는 것을 막는 과정에서 필요한 롱테일 행동을 취하는 것을 막을 수 있다.
- 참고 논문
    - ChaufferNet: Learning to Drive by Imitating the Best and Synthesizing the Worst (RSS19)
    - TrafficSim: Learning to Simulate Realistic Multi-Agent Behavior (CVPR21)
    - Model-Predictive Policy Learning with Uncertainty Regularization for Driving in Dense Traffic (ICLR19)

##### Behavior Cloning with Data Augmentaion

- 행위자의 궤적에 섭동(perturbation)을 추가하 생성한 합성 시나리오롤 통해 학습하거나 입력 데이터에 변형을 가하여 모델이 분포 외 상태에 강건하게 만든다.
- 다음의 장단점을 갖는다.
    - (+) 간단하고 기존 행동 모델의 변경을 최소화할 수 있다.
    - (-) 데이터 증강을 개발자가 손수 만들어야 한다.
- 참고 논문
    - ChauffeurNet: Learning to Drive by imitating the Best and Synthesizing the Worst (RSS19)
    - End-to-End Learning for Self-Driving Cars (2016)
    - ALVINN: An Autonomous Land Vehicle in a Neural Network (NeurIPS 1988)

##### Behavior Cloning with Differentiable Simulation

- 행동 모델이 분포 외 상태를 마주칠 수 있도록 폐루프 시뮬레이션을 통해 정책을 학습시킨다.
    - 전문가 초기 상태(**Expert initial state**)로 미분가능한 폐루프 시뮬레이션을 시작한다.
    - 폐루프 시뮬레이션 과정에서 섭동을 추가하며 이 때 전문가 행동 정책과 모델의 예측정책의 차이가 최소가 되도록 학습한다.
- 다음의 장/단점을 갖는다.
    - (+) 미분가능한 폐루프 시뮬레이션을 통해 각 스텝의 정책을 unroll하며 모델이 자신의 실수를 회복하는 방법을 학습할 수 있다.
    - (-) 전문가 정책과의 차이를 학습하는 과정에 반영되는 편향이 현실성과 다양성을 저하할 수 있다.
- 참고 논문
    - TrafficSim: Learning to Simulate Realistic Multi-Agent Behavior (CVPR22)
    - Urban Driver: Learning to Drive from Real-world Demonstations Using Policy Gradients (CoRL21)
    - Imagining The Road Ahead: Multi-Agent Trajectory Prediction via Differentialble Simulation (ITSC21)

##### Behavior Cloning with Interactive Experts

- 행동 복제 모델의 훈련과 새로운 데이터셋 수집을 전문가의 상호작용 아래에서 반복적으로 수행한다.
    - 전문가는 폐루프 시뮬레이션 과정에서 상호작용하며 행동 레이블(**action lable**)을 정책을 감독한다.
    - 대표적으로 DAGGER 알고리즘이 있다.
- 다음의 장/단점을 갖는다.
    - (+) 행동 복제 모델이 전문가의 감독 아래에서 잘못된 정책을 회복하는 방법을 학습할 수 있다.
    - (-) 전문가 상호작용은 어려우며 비용이 높다.
- 참고 논문
    - A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning (AISTATS11)
    - An Algorithmic Prespective on Imitation Learning (2018)

##### Behavior Cloning with Reinforcement Learning

- 행동 복제와 강화학습을 결합하여 강건성과 현실성을 향상시킨다.
    - 행동 복제는 강화학습을 통해 현실성에 기반한 강한 지도 학습을 수행한다.
    - 강화 학습은 분포 외 상황에서의 강건성을 향상시킬 수 있다.
- 다음의 장/단점을 갖는다.
    - (+) 행동 모델이 사람과 유사한 정책을 학습할 수 있다.
    - (+) 분포 외 상태로 발생하는 공변량 변화에 강인하다.
    - (-) 강화학습을 위한 보상함수 설계가 까다롭다.
    - (-) 행동모델과 보상학습 사이의 균형을 유지하기 어렵다.
- 참고 논문
    - Imitation is Not Enough: Robustifying Imitation with Reinforcement Learning for Challenging Driving Scenarios (NeurIPS22)
    - Learning Realistic Traffic Agents in Closed-loop (CoRL23)
    - Human-compatible Driving Parthers through Data-regularized Self-play Reinforcement Learning (arXiv24)
    - Reinforcement Learning with Human Feedback for Realistic Traffic Simulation (arXiv24)

##### Adversarial Imitation Learning

- [[Generative Adeversarial Network|GAN]]과 유사하게 행동 복제 모델이 예측한 정책과 전문가 정책을 구분하는 판별자(discriminator)를 행동 모델과 동시에 학습시킨다.
    - 잘못된 정책을 제외하는 판별자를 학습시킬 수도 있다.
- 다음의 장/단점을 갖는다.
    - (+) 폐루프 시뮬레이션을 통해 학습할 수 있다.
    - (+) 데이터 증강이나 손실/보상 함수의 설계를 직접할 필요가 없다.
    - (-) 두 개의 모델(행동 복제, 판별자)을 동시에 학습시키므로 학습이 불안정하고 어렵다.
- 참고 논문
    - Generative Adversarial Imitation Learning (NeurIPS16)
    - Multi-Agent Imitation Learning for Driving Simulation (arXiv18)
    - Learning from Demonstration in the Wild (arXiv19)
    - Symphony: Learning Realistic and Diverse Agents for Autonomous Driving Simulation (ICRA22)

### Diverse Actor Behaviors

#### Hierarchical Policies

- 운전의 고수준 목표 (waypoint goal, route goal, latent variables)를 저수준의 제어와 분리하여 모델링한다.
- 다음의 장/단점을 갖는다.
    - (+) 운전이라는 행동이 보유한 다중 모드 분포 (**multi-modal distribution**)을 더 잘 반영할 수 있다.
    - (+) 명시적인 계층 구조는 해석이 용이하다.
    - (-) 고수준 목표를 설계하는 것이 어렵다.
    - (-) 잠재변수의 계층 구조는 해석불가능하거나 만들기가 어려울 수 있다.
- 참고 논문
    - Nocturne: a scalable driving benchmark for bringing multi-agent learning one step closer to the real world (2022)
    - BITS: Bi-level Imitation for Traffic Simulation (ICRA23)
    - Symphony: Learning Realistic and Diverse Agents for Autonomous Driving Simulation (ICRA22)
    - MixSim: A Hierarchical Framework for Mixed Reality Traffic Simulation (CVPR23)
    - TrafficSim: Learning to Simulate Realistic Multi-Agent Behaviors (CVPR21)
    - Hierarchical Imitation Learning for Stochastic Environments (IROS23)

#### Generative Modesl

- 확산 모델([[Diffusion Model]]) 혹은 자기회귀 모델 ([[Auto-regressive Model]])을 운전 행동의 다중 모드 분포를 포착할 수 있도록 학습시킨다.
- 참고 논문
    - TrafficSim: Learning to Simulate Realistic Multi-Agent Behaviors (CVPR21)
    - Hierarchical Imitation Learning for Stochastic Environments (IROS23)
    - MotionLM: Multi-Agent Motion Forecasting as Language Modeling (ICCV23)
    - Trajeglish: Traffic Modeling as Next-Token Prediction (ICLR24)
    - Guided Conditional Diffusion for Controllable Traffic Simulation (ICRA23)
    - MotionDiffuser: Controllable Multi-Agent Motion Prediction using Diffusion (CVPR23)

#### Multi-agent Self-play

- 자가 실행 (**Self-play**)를 통해 다수의 강화학습 에이전트를 학습시킨다.
    - 시뮬레이션 환경에서 다양한 인센티브와 역량을 가진 RL 에이전트들을 서로 경쟁시키며 훈련시킨다.
    - 다양하고 복잡한 시나리오를 구성할 수 있는 행위자 집합을 생성한다.
- 다음의 장/단점을 갖는다.
    - (+) 다양한 정책을 학습할 수 있다.
    - (-) 보상 함수만을 통해 사람과 같은 정책을 학습시키기 어렵다.
- 참고 논문
    - Towards Learning Multi-agent Negotiations via Self-Play (ICCV19)
    - Energent Road Rules in Multi-Agent Driving Environments (ICLR21)
    - Learning to Simulate Self-driven Particles System with Coordinated Policy Optimization (NeurIPS21)
    - Evaluating driving performance in Diverse Simulated Worlds (Wayve23)

### Controllable Actor Behaviors

- 시뮬레이션 내의 행동에 대한 제어가능성을 높이기 위해서 시나리오 작성자가 지정한 고수준의 제어 요구에 대응할 수 있어야 한다.
- 이를 위해 크게 4가지 접근 방식을 사용하고 있다.

#### Goal-Conditional Policies

- 운전 명령(좌회전/우회전), Waypoint 목표 또는 경로를 조건으로 목표 조건부 정책 (Goal Conditional Policies)을 학습한다.
- 다음의 장/단점을 갖는다.
    - (+) 행위자가 무엇을 할지 제어할 수 있다.
    - (+) 조작하기 단순하고 해석 가능하다.
    - (-) 목표가 무엇인지 학습단계에서 명확해야 하며 복잡한 목표에 대해서는 학습이 어렵다.
- 참고 논문
    - End-to-End Driving via Conditional Imitation Learning (ICRA18)
    - Nocturne: a scalable driving benchmark for bringing multi-agent learning one step closer to the real world (2022)
    - BITS: Bi-level Imitation for Traffic Simulation (ICRA23)
    - Symphony: Learning Realistic and Diverse Agents for Autonomous Driving Simulation (ICRA22)
    - MixSim: A Hierarchical Framework for Mixed Reality Traffic Simulation (CVPR23)

#### Style Control

- 행위자의 공격성 또는 신중함 같은 운전 스타일과 연관된 정책을 학습한다.
- 스타일은 아래의 기준으로 구분될 수 있다.
    - 행위자가 다른 행위자에게 행동을 얼마나 조정하게 만드는지를 측정하는 예의(courtesy)
    - 행위자가 자신과 타인에게 가치를 어떻게 배분하는지를 측정하는 사회적 가치 지향(Social Value Orientation)
    - 정보 탐색과 안전과 운전 목표 사이에서 어떻게 조율하는지에 대한 비중
    - 운전스타일을 잠재공간에서 표현하기
- 다음의 장/단점을 갖는다.
    - (+) 행위자가 어떤 행동을 할지 제어할 수 있다.
    - (-) 스타일이란 것 자체를 정의하기 가 어렵다.
    - (-) 복합적인 스타일을 학습하기 어렵다.
- 참고 논문
    - Editing Driver Character: Socially-Controllable Behavior Generation for Interactive Traffic Simulation (arXiv23)
    - Social behavior for autonomous vehicles (PNAS18)
    - Learning to Simulate Self-driven Particles System with Coordinated Policy Optimization (NeurIPS21)
    - Resolving uncertainty on the fly (Frontiers in Neurorobitics24)
    - CtRL-Sim: Reactive and Controllable Driving Agents with Offline Reinforcement Learning (arXiv24)
    - TrafficBots: Towards World Models for Autonomous Driving Simulation and Motion Prediction (ICRA23)

#### Reward Function Specification

- 행위자가 특정 행동을 하도록 유도하는 보상 함수를 지정한다.
- 다음의 장/단점을 갖는다.
    - (+) 매우 유연하고 구성 가능(composable)하여 복잡한 행동을 생성할 수 있다.
    - (-) 최적화를 반복해야 하므로 추론 속도가 느리다.
    - (-) 보상 함수를 정의하거나 조정하는 것이 어렵다.
- 참고 논문
    - AdvSim:Generating Safety-Critical Scenarios for Self-Driving Vehicles (CVPR21)
        - 충돌을 유도하는 적대 시나리오 생성
    - Generating Useful Accdient-Prone Driving Scenarios via Learned Traffic Prior (CVPR22)
        - 잠재 공간 최적화를 통한 현실적인 적대 시나리오 탐색 가능함.
    - Guided Conditional Diffusion for Controllable Traffic Simulation (ICRA23)
    - Failure-Scenario Maker for Rule-Based Agent using Multi-Agent Adversarial Reinforcement Learning and its Application to Autonomous Driving (IJCAI19)

#### Natural Language Interface

- [[LLM]]을 사용하여 자연어 설명을 보상 함수, 가이던스 함수 또는 저수준 궤(maneuver)으로 변환하여 정책을 제어한다.
  ◦ 장점: 가장 유연하고 시나리오 저자에게 인체공학적(ergonomic)입니다.
  ◦ 단점: 복잡한 행동 및 폐쇄 루프 시뮬레이션 설정에서의 효과에 대한 연구는 아직 초기 단계입니다.

- 다음의 장/단점을 갖는다.
    - (+) 가장 유연하고 시나리오 생성이 용이하다.
    - (-) 아직 초기 연구 단계이며 언어로 시나리오를 생성할 때 발생하는 모호성을 개선해야 한다.
- 참고 논문
    - Diffusion-ES: Gradient-free Planning with Diffusion for Autonomous Driving and Zero-Shot Instruction Following (arXiv24)
    - Language-Guided Traffic Simulation via Scene-level Diffusion (CoRL23)
    - Conditional Driving from Natural Languae (CoRL19)
    - Language Conditioned Traffic Generation (CoRL23)

## Reference

1. [(09) Simulation Behavior (Waabi CVPR 24 Tutorials on Self-Driving Cars)](https://youtu.be/khRLKQXVwy4?si=ojsOZzYsa8-_Yr36)
1. [NotebookLM](https://notebooklm.google.com/notebook/e41d6bea-6f75-4642-ad7b-d53497de7cf1)
