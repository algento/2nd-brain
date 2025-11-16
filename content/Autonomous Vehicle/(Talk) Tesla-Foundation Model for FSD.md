---
title: (Talk) Tesla-Foundation Model for FSD
created: 2025-10-30 21:23
modified: 2025-11-08 08:51
tags:
  - AD-E2E
keywords:
  - Tesla
  - WorldSim
type: literature-note
kanban: done
published: ICCV-2025
affiliations:
  - Tesla
mocs: []
---

# (Talk) Tesla-Foundation Model for FSD

## Overview

- 테슬라가 ICCV2025에서 자신들의 E2E 모델과 NN기반 시뮬레이션 모델 (**WorldSim NN**)을 통해 closed-loop simulation을 수행하는 것을 소개함.
- 테슬라는 E2E 모델로 전환한 이후, 해당 모델을 효율적으로 학습시키기 위해 해당 시뮬레이션 프로세스를 적극적으로 사용 중임.

## AV 1.0의 한계점

- 인간의 가치나 선호도에 의해 발생하는 행동을 코드화하는 것은 매우 어려운 일이다.
- `Perecption`, `Prediction`, `Planning` 간의 인터페이스를 정의하는 것은 어렵다.
    - 중간 인터페이스를 정의하며 손실되는 정보가 생기며 이로 인한 불확실성이 시스템 전체에 전파된다.
- 룰 기반의 로직은 예측가능하고 균일 연산시간으로 동작하기 어렵다.
    - 전통적인 룰 기반 로직은 상황에 따라 연산 브랜치의 길이가 달라지기 때문에 deterministic latency를 가질 수 없다.
- `Fat and long-tail case`에 대해서 스케일링하기 어렵다.

> Codifying human values is incredibly difficult.
> Real-world is filled with tiny trolly problems
> Interface between perception, prediction, and planning is ill-defined.

## 테슬라의 AV 2.0

테슬라는 AV 1.x의 한계를 극복하기 위해 AV 2.0 즉, E2E로의 전환을 수행했다.
이를 통해 SW 구조와 개발/평가 방법론을 다음과 같이 변화시켰다.

- 모듈러 네트워크를 하나의 대규모 네트워크로 통합
- 명시적인 인지 미수행
    - 학습 시 보조적으로 인지 결과를 제공할 수는 있음.

테슬라의 Large E2E FM (Foundation Model)은 다음의 입력을 받는다.

- 8 camera images
- Naivgation maps
- Vehicle Kinematics (IMU, odometry, etc.)
- Audio (음성 입력을 말하는지, 주변 소리를 듣는 것인지, 초음파인지 불명확함)

테슬라의 Large E2E 모델의 출력은 다음의 중간 출력을 Reasoning에 활용하여 next control action을 '36 Hz'로 출력한다.

- Panotic segmentation
- 3D Occupancy
- 3D Gaussian (3D Gaussian Splatting의 그 Gaussian이다.)
    - 주변 환경을 3차원으로 표현하는데 사용되지만 정확한 사용 방안은 미지수이다.
- Language
    - 자연어 출력을 **system 2 thinking**을 하는데 활용한다.

[[#Remarks (Interpretability)]]에서 언급하였듯이 추론에서는 중간 출력을 사용하지 않을 것으로 생각된다.
아래의 그림은 정확한 아키텍처는 아니고 컨셉으로 이해해야 한다.

<p class="img-center">
  <img src="20251101-123946.png" alt="Telsa FM" style="max-width:700px; width:100%">
</p>

## Curse of Dimensionality

현재 테슬라의 E2E FM은 **2b tokens**를 입렵받아서 control action(steering + acceleration)에 해당하는 **2 tokens**을 출력한다.
입출력의 차이가 너무나 차원의 차이가 크기 때문에 데이터가 많아도 학습시키기 어렵다.

입력 시 tokenize하는 것은 다음과 같다.

- 7 cameras $\times$ 36 fps $\times$ 5Mpx $\times$ 30 sec history/(5$\times$5 pixel patch)
- Navigation map and route for few miles
- 100 Hz kinetic data such as speed, IMU, odometry
- 48KHz Audio data

이러한 차원의 저주를 극복하기 위해 테슬라는 신중한 데이터 필터링과 희귀 시나리오 활용 전략을 통해 학습에 필요한 전체 분포를 커버하는 필수적인 양의 데이터를 정제하고 이는 최상 일반화 성능과 안전성을 제공한다.

### 이벤트 트리거 기반 데이터 수집 및 정제

테슬라는 방대한 양의 데이터 (500년)에 해당하는 데이터를 매일 수집하지만 대부분은 지루한(**boring**) 데이터이다.
따라서 수집 시점부터 corner case를 골라내는 별도의 작은 NN을 운용한다.
데이터 수집 트리거는 다음과 같다. - 운전자가 개입 - 상태 공간에서 큰 변화 발생
이렇게 수집된 데이터는 실제 운전자 주행과 모델 예측이 다른 경우에 대해서 평가하는데 활용한다.

## Interpretability and Safety Guarantess

테슬라의 Foundation Model은 다음과 같은 추가 정보를 예측해서 CoT (chain-of-thought)로 Reasoning을 수행한다.
이와 같은 추가 정보 학습 뿐만 아니라 상황 분석과 디버깅에 활용할 수 있다.
이를 통해 테슬라는 시스템에 선제적 안전성(proactive safety)를 확보할 수 있었다.

- 3D Occupancy and flow
- Object (vehicles, pedestrians, bicyclists, etc.)
- Traffic Control
- Road boundary (lanes and semantics)
- Traffic attributes (speed limit, etc.)
- Decision (text)

위의 보조 정보를 정확히 어떤 주기로 어느 시점(학습, 추론 , 평가)에서 활용하는지 불명확하다.
위의 정보를 실시간으로 출력하는 것은 어렵다고 생각되기 때문에 학습이나 평가에서만 활용하지 않을까라고 예상한다.

### Generative 3D-GS

테슬라의 FM은 3D-GS (Gaussian Splats)를 생성하여 출력한다.
테슬라의 생성형 3D-GS는 기존의 3D-GS 대비 다음의 특징을 가진다.

- 짧은 최적화 주기: 약 5 fps
- 초기화에 3D point 필요없음
- 동적 객체 대응 가능
- 더 넓은 시점이동 대응

개인적으로 봤을 때 3D-GS가 엄청난 고품질은 아니지만 로직개발에 잘 활용하고 있는 것으로 보인다.

<p class="img-center">
  <img src="Attachments/20251101-130847.png" alt="Tesla Generative GS" style="max-width:700px; width:100%">
</p>

### Remarks (Interpretability)

## Evaluation

테슬라는 녹화된 데이터 상에서의 예측 성능이 아니라 실제 주행 상황에서의 예측 성능을 끌어올리기를 원한다.
따라서 **World Simulator NN**를 구축하고 closed-loop 시뮬레이션을 수행하여 행동의 결과(**consquence-of-actions**)를 평가한다.
그 이유는 실패를 피하는 다양한 주행 방법이 있기 때문에 이러한 **multi-modality**를 반영한 지표를 통해 평가하기를 원하기 때문이다.

이 때, E2E FM의 성능을 정확히 검증하기 위해서는 **균형잡히고 철저한** 검증 데이터 셋을 사용한다.
이는 소모적인 일이지만 성능에 큰 영향을 끼친다고 한다.

### World Simulator

테슬라는 학습 기반의 신경망 시뮬레이터를 구축해서 closed-loop 시뮬레이션을 통한 평가에 사용 중이다.
이 신경망은 수월하게 수집 가능한 `상태-행동` 쌍을 반전하여 만든 `행동-상태` 쌍을 통해서 학습시킬 수 있다.
이 신경망은 현재 시점의 상태(멀티 카메라 영상 등)와 현재 시점의 행동을 입력받아 다음 시점의 상태를 생성한다.
이를 통해 이전의 실패 사례를 시뮬레이터로 재현하여 평가하거나 적대적(**adversarial**) 상황으로 변형하여 코너 케이스 평가에 활용할 수 있다.

<p class="img-center">
  <img src="20251101-134353.png" alt="Tesla WorldSim" style="max-width:700px; width:100%">
</p>

#### Image Generation

하나의 신경망이 8개의 영상을 동시에 (**simultaneously**) 생성하며 그 길이는 일반적으로 1분에서 1분 30초 정도 이다.
하지만 최대 6분의 비디오도 생성할 수 있다고 한다.

<p class="img-center">
  <img src="20251101-142531.png" alt="Tesla WorldSim Generated Image" style="max-width:700px; width:100%">
</p>

영상 생성 시간은 실시간에 준하며, 이를 통해 휠을 연결한 시뮬레이션이 가능하다.
큰 시점 변환과 길이 아닌 곳으로 주행하는데도 영상 생성 품질이 높은 편으로 보인다.
해당 카메라들 사이의 물리적 일관성이 유지되며 교통 표지만, 교통 신호와 같은 교통 체계의 생성에서도 일관성이 유지된다.
다른 플랫폼, 다른 장소 그리고 다른 날씨에서도 잘 동작하는 것으로 보인다.

<img src="20251101-145146.png" alt="wheel-based virtual driving">

#### Closed Loop Simulation

이 시뮬레이터는 평가 목적 이외에도 **closed-loop 강화 학습**에 활용될 수 있다.
아래의 그림에서 policy NN이 E2E FM으로 예상된다.
즉, WorldSim NN은 Policy NN과 구분되는 별도의 모델이며, 행동에 따른 다음 영상을 생성하는 능력에 특화된 모델로 예상된다.

<p class="img-center">
  <img src="20251101-142716.png" alt="Tesla closed loop simulation" style="max-width:700px; width:100%">
</p>

## Q&A

- Ashok Elluswamy는 gradient flow가 처음부터 끝까지 흐르기만 하면 E2E라고 Q&A세션에서 이야기하고 있다.
    - 실제로는 모듈러 구조인데 gridient가 흐르게 한 구조일 수 도 있수도?

## Reference

1. [ICCV25 WFM-AD](https://wdfm-ad.github.io/iccv25/)
    - [A Peek into Tesla’s Autonomous Future: Core Tech Revealed by VP Ashok Elluswamy at ICCV25 WDFM-AD](https://youtu.be/IRu-cPkpiFk?si=b_qkMh9AgWcRutGd)
1. [NotebookLM](https://notebooklm.google.com/notebook/22b3ff9e-2237-44bb-8ce4-f7f15e441878)
