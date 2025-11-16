---
title: (Talk) Simulation-Waabi Tutorial on Self-Driving Cars
created: 2025-11-10 19:29
modified: 2025-11-16 11:56
tags:
  - AV
  - Talk
keywords:
  - Simulation
  - Sensor
  - World-Model
  - AD-Trend
type: literature-note
kanban: done
published: CVPR-2024
affiliations:
  - waabi
mocs:
  - "[[Autonomous Vehicle]]"
---

# (Talk) Simulation-Waabi Tutorial on Self-Driving Cars

## Overview

- 자율주행 자동차 시뮬레이션에 필요한 요소를 잘 식별해 놓음.
    - 자율 주행 시뮬레이션 필요 요소와 폐루프 시뮬레이션에 필요한 요소를 식별함.
- 자율주행 시뮬레이션에 필요한 요소 기술을 잘 범주화하고 이에 대한 현재 (2024년)의 기술 동향을 잘 분석해 놓음.

## Deploying Self-Driving Car

- 자율주행 SW를 배포하는 것은 매우 어려운 일이다.
- 안전하게 운전을 하는 것은 복잡하고(complex) 미묘한(nuanced) 의사결정을 요구한다.
- 운전하는 동안 발생할 수 있는 상황은 매우 다양하지만 집중을 요하거나 위험한 상황은 드물게 발생한다.
- 자율주행 차량이 이러한 모든 상황에 대응할 수 있도록(**learning**), 그리고 그것을 우리가 확신할 수 있도록(**testing**) 해당 상황을 시스템에 노출시켜야 한다.

## Types of Simulation in AV Industry

### Log-Replay Simulation

- 이전 주행에서 수집된 센서 데이터를 이용해서 직접적으로 리플레이를 하며 자율주행 SW를 평가한다.
- 차량은 주변 환경과 상호작용할 수 없다. (**영화**를 보는 것처럼)
- 개루프(**open-loop**) 평가만 가능하며 모든 시나리오에 대응하려면 실제 데이트 수집이 필요하다.

### Motion Planning-Only Simulation

- Motion Plannig SW가 Ground Truth 인지/예측 결과를 입력받아 폐루프(**closed-loop**)로 시뮬레이션을 수행한다.
- 센서 레벨 데이터를 사용하지 않기 때문에 인지/예측 결과의 오류가 무시되며, End-to-End SW를 평가(**evaluate**)할 수 없다.

### Data Generation

- 인지/예측을 위해 합성 센서 데이터 (영상, 라이다)를 그래픽 엔진을 통해 랜더링한다.
- 다양성과 확장성을 확보하기 어렵고, 게임 엔진을 사용하기 때문에 발생하는 **domain-gap**이 존재한다.
- 그래픽스 엔진을 통해 센서 데이터를 생성하는 과정이 느리기 때문에 전체 시스템 테스트에 비효율적인 면이 존재한다.

#### World Model

- [[Generative AI]]에 기반하여 [[Diffusion Model]]과 [[Transformer]]로 데이터를 생성할 수 있다.
- 게임 엔진 기반의 접근 방식보다 확장성과 다양성을 확보하기 좋지만, 생성 속도가 현재로서는 느리고, 데이터의 일관성, 제어가능성, 피드백 관점에서는 발전이 필요하다.
    - 피드백 관점에서 현재의 world model은 물리 정보를 암시적으로 인코딩하기 때문 정확한 3D 물리 정보를 제공하기 힘들다는 한계를 가지고 있다.

## What Do We want for Self-Driving Simulation?

- 자율주행 시뮬레이터가 갖춰야할 속성으 다음과 같다.
    - 다양성 (Diversity): 현실 세계의 가능한 모든 시나리오를 포착할 수 있어야 함.
    - 속도 (Speed): 다수의 시나리오를 빠르게 실행할 수 있어야 함.
    - 제어 가능성 (Controlability): 현실에서 발생할 수 있는 다양한 상황과 유형을 정확히 설정할 수 있어야 함.
    - 현실성 (Realism): 현실 세계와 유사한 상황, 행동, 센서 데이터를 만들 수 있어야 함.
    - 몰입성 (Immersiveness): 궤적뿐만 아니라 센서 데이터를 시뮬레이션할 수 있어야 함.
    - 반응성 (Reactivity): 폐루프 평가를 지원해야 하며, 자차의 행동에 다른 액터들이 반응할 수 있어야 함.
    - 피드백 (Feedback): 충돌, 안전, 편안함, 정확 등의 평가지표 계산하여 시스템 성능을 평가하고 실패 지점을 식별할 수 있어야 함.
    - 확장성 (Scalable): 낮은 비용으로 실행할 수 있어야 함.

<p class="img-center">
  <img src="20251110-201618.png" alt="Metric of Self-Driving Simulation" style="max-width:700px; width:100%">
</p>

## Waabi World Engine

### Waabi World Engine Overview

- 자신들은 위의 모든 측면에서 장점을 가진다고 주장하며, 명시적으로 물리에 근간을 두며 실제 3D 표현을 다루는 것을 목표로 하고 있다고 말한다.
    - 기본적으로 그래픽스 엔진을 이용한 시뮬레이터이지만 시간 동기화나 평가 측면에서는 **data-driven**이라고 주장하고 있다.
    - 컨텐츠, 에셋 그리고 행동 모델을 만들 때 생성형 AI를 활용하며, 이를 그래픽스 엔진에 입력하여 3D 공간에서 다루기 때문에 자신들의 시뮬레이터가 빠르고 제어가능하다고 주장한다.
- 다음의 3가지 목적으로 사용 가능하다.
    - 전체 자율주행 시스템의 성능을 평가하기 위한 개루프 시뮬레이션
    - 현실적인 인지/예측 결과에 기반한 Motion-Planner 폐루프 시뮬레이션
    - 인지 모듈 학습용 데이터 생성
- 다른 시뮬레이션 툴체인 대비 추가로 고려하고 있는 것은 **Latency simulation**이다.
    - 현실적인 센서 입력이나 제어 출력을 모사하기 위한 모듈로 보이며, 좀 더 현실적인 시뮬레이션이 가능하도록 만들 것으로 예상된다.
    - 실제로 어떻게 latency를 모델링하고 주입하는지에 대해서는 자세히 설명하지는 않는다.

<p class="img-center">
  <img src="Attachments/20251110-203337.png" alt="Waabi World Engine" style="max-width:700px; width:100%">
</p>

#### Full Open Loop Simulation

<p class="img-center">
  <img src="Attachments/20251110-204605.png" alt="Full Open-loop Simulation" style="max-width:700px; width:100%">
</p>

#### Motion Planner Closed-Loop Simulation

<p class="img-center">
  <img src="Attachments/20251110-204625.png" alt="Motion-Planner Closed-Loop Simulation" style="max-width:700px; width:100%">
</p>

#### Perception Training Data Generation

<p class="img-center">
  <img src="Attachments/20251110-204657.png" alt="Synthetic Data Generation" style="max-width:700px; width:100%">
</p>

### Action Model & Scenario Configuration

- 다양한 Scene 초기화와 다양한 에셋을 지원하는 ActorZoo를 입력받아 자율주행 SW의 학습과 시험에 활용할 수 있다고 주장한다.
- 이를 통해 특정 타입의 actor 행동에 과적합되는 것을 방지할 수 있다고 한다.
  <p class="img-center">
  <img src="Attachments/20251110-205024.png" alt="Actor Model and Scenario Configuration" style="max-width:700px; width:100%">
</p>

## What Do We Need for Closed-loop Simulation?

- 폐루프 시뮬레이션을 위해서는 다음의 기술이 확보되어야 한다.
    - [[#Virtual World Creation]]: 가상 세계를 구성한 요소들을 만들고 이를 통해 센서 데이터를 만드는 기술
    - [[#Vehicle Platform Modelling]]: 자차의 동적 모델을 모델링하고 실제 차량 플랫폼과 연계하는 기술
    - Virtual World Dynamics: 가상 세계에서 자차가 처할 상황을 시나리오로 표현하고 해당 상황에 존재하는 타 액터들의 행동을 정하는 기술

## Virtual World Creation

### Asset Libraries

- 에셋은 다음의 조건을 가지고 있어야 한다. (**Asset Desideraata**)
    - 랜더링과 동적 모델 생성에 적합해야 한다.
    - 고수준의 기하 모델링
    - 현실적이고 수정가능한 외관 표현
    - DoF(Degree of Freedom) 정의 (애니메이션 등을 위함)
    - 물리와 GT 생성에 적합한 메타 정의
- 실제 수집된 데이터를 이용해서 디지털 트윈을 구축하는 것은 Artist-based CAD 모델과 애니메이션으로 3D 컨텐츠를 구축하는 것과 비교해서 많은 장점을 갖는다고 주장한다.
- 에셋 라이브러리에 수집하는 에셋은 크게 3가지로 구분할 수 있다.
    - 배경 에셋 (**Backgroud Asset**): 정지 객체, 환경
    - 강체 액터 에셋 (**Rigid Actor Asset**): 차량 등
    - 변형 액터 에셋 (**Deformable Actor Asset**): 보행자 등

#### Background Assets

- 배경 에셋을 만드는 방법은 크게 3가지가 존재한다.
    - [[#Explicit-based Aggregation/SfM Approach]]
    - [[#Neural Optimization-based Approach]]
    - [[#Generalizable Neural Reconstruction]]

##### Explicit-based Aggregation/SfM Approach

- 라이다 포인트를 모아서 혹은 SfM (Structure-from-Motion)으로3D 환경을 복원한 후 텍스쳐 매핑한 mesh를 생성할 수 있다.
- 간단하고 확장가능하며 mesh와 texture를 기반으로 3D를 표현하므로 랜더링과 데이터 크기 측면에서 효율적이다.
- 라이다 포인트 통합 과정에서 빈 곳이나 오차가 큰 곳이 발생할 수 있으며, 먼 객체나 동적 객에대 품질 저하가 발생하기 쉽다.
- 다음을 참고하자.
    - LiDARSim: Realistic LiDAR Simulation by Leveraging the Real World (CVPR20)
    - SfM (CVPR16)
    - Poisson Surface Reconstruction for LiDAR Odometry and Mappint(ICRA21)
    - SurfelGAN: Synthesizing realistic sensor data for autonomous driving (CVPR20)
    - Mesh-based 3D Texture Urban Mapping (IROS17)
    - Robust Dense Mapping for Large-Scale Dyanamic Environment (ICRA18)

##### Neural Optimization-based Approach

- 센서 데이터를 입력받아서 volume rendering을 통해 NeRF를 학습하고 에셋을 추출한다.
- 정확한 geometry와 texture 복원을 통해 좀 더 현실적인 센서 데이터 랜더링이 가능하다.
- 3D 정보를 복원하기 때문에 큰 내삽(interpolation)과 외삽(extrapolation)에 강인하다.
- sparse 데이터를 처리하는데 어려움이 있으며, frame 단위의 최적화가 아닌 scene 단위의 최적화만 가능하다. 특히 연산 비용이 크다.
- 다음의 논문을 참고하자.
    - Urban Radiance Field (CVPR22)
    - BakedSDF (SIGGRAPH23)
    - UniSim: A Neural Closed-Loop Sensor Simulator (CVPR23)
    - Neuralangelo: High Fiedelity Neural Surface Reconstruction (CVPR23)

##### Generalizable Neural Reconstruction

- 표면 복원(surface reconstruction)을 수행하는 일반화된 모델을 학습하여 사용한다.
    - scene 단위로 최적화된 모델을 사용하는 것이 아니라 일반화 모델을 사용하는 것을 말한다.
- 노이즈에 강인하며 확장성을 가지고 있으며 정확한 geometry와 appearance를 제공할 수 있다.
- 학습 비용이 비싸고 GT로 사용하기에는 신뢰성이 낮을 수 있다.
- 정확한 normal 추정이 필요하다.
- 다음의 논문을 참고하자.
    - Neural Kernel Surface Reconstruction (CVPR23): NVIDIA 논문?
    - ExtraNeRF: Visibility-Aware Extrapolation of Neural Radiance Fields with Diffusion Models (CVPR24)
    - PixelSplat: 3D Gaussian Splats from Image Pairs for Scalable Generalization 3D Reconstruction (CVPR24)

#### Rigid Actor Assets

강체 액터 에셋을 만드는 방법에는 크게 5가지가 존재한다.
- [[#Explicit-based Aggregation/SfM Approach]]
- [[#Explicit Inverse Rendering Approach]]
- [[#Implicit-based Inverse Rendering Approach]]
- [[#Generative Approach]]
- [[#Adverasial Assets]]

##### Explicit-based Aggregation/SfM Approach

- 라이다 포인트를 통합(aggregation)하거나 SfM을 통해 해당 액터에 대한 3D 정보를 확보하고 이를 활용한다.
    - 이 과정에서 측위 정보나 bbox나 segmentaion같은 annotation 정보를 활용할 수 있다.
- 다음의 장/단점을 갖는다.
    - (+) 간단하고 확장가능하며 정확한 기하 정보를 손쉽게 얻을 수 있다는 장점을 가지고 있다.
    - (-) 노이즈가 통합 과정에 주입되거나 빈 곳이 있는 경우 품질이 열화될 수 있다.
    - (-) 3D 정보가 충분하지 않은 경우 형상이 불완전할 수 있다.
    - (-) 각 에셋마다 충분한 3D 정보를 저장하기 위해서 높은 저장 비용이 든다.
- 다음의 논문을 참고하자.
    - LiDARSim: Realistic LiDAR Simulation by Leveraging the Real World (CVPR20)
    - SurfelGAN: Synthesizing realistic sensor data for autonomous driving (CVPR20)
    - SfM (CVPR16)

##### Explicit Inverse Rendering Approach

- 실제 데이터에 맞도록 해당 강체의 명시적인 mesh representation을 예측하거나 최적화한다.
    - 이 과정에서 segmentation annotation이나 CAD 모델을 보조 정보로 활용한다.
- 다음의 장/단점을 갖는다.
    - (+) 간단하고 확장가능하다.
    - (+) 노이즈가 있거나 부족한 3D관측 정보로부터 에셋 생성을 하더라도 강인하다.
    - (+) 의미론적 사전 정보를 최대한 활용한다.
    - (-) 잘 알려진 범주의 에셋에 대해서 과적합되어 다양성이 부족할 수 있다.
    - (-) 생성 결과가 GT로 사용하기 애매할 수 있다.
- 다음의 논문을 참고하자.
    - GeoSim: Realistic Video Simulation via Geometry-Aware Composition for Self-Driving (CVPR21)
    - CADSim: Robust and Scalable in-the-wild 3D Reconstruction for Controllable Sensor Simulation (CoRL22)
    - Neural Fields meets Explict Geometric Representation for Inverse Rendering of Urban Scene (CVPR23)

##### Implicit-based Inverse Rendering Approach

- 실제 센서 데이터를 입력받아 **inverse rendering**을 통해 occupancy fiedl나 signed distance field와 같은 **neural scene representation**을 학습한다.
    - 이 과정에서 segmentaion이나 bbox annotation을 활용한다.
    - Inverse rendering 과정을 geometry, material, apperance, light condition 등으로 분해해서 접근하기도 한다.
- 다음의 장/단점을 갖는다.
    - (+) 임의의 형상에 대응가능하며 데이터가 희박한 경우나 노이즈가 있는 경우에 강인하다. 또한 현실적인 랜더링이 가능하다.
    - (-) 학습 혹은 최적화하는데 연산 비용이 많이 든다.
    - (-) 객체 추출에 segmentation 정보에 전적으로 의존하는 경우가 있다.
- 다음의 논문을 참고하자.
    - NeuSim: Reconstructing Objects in-the-wild for Realistic Sensor Simulation (ICRA23)
    - AutoRF: Learning 3D Object Radiance Field from Single View Observations (CVPR22)
    - Shape, Pose and Appearance from a Single Image via Bootstrapped Radiance Field Inversion (CVPR23)
    - SuGaR: Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction and High-Quality Rendering (CVPR24)

##### Generative Approach

- Image-to-asset 방식과 text-to-asset 방식이 존재한다.
    - Image-to-asset 방식은 조건부 생성 모델을 통해 다중 시점 이미지에서 3D 표현을 학습하고 이를 통해 에셋을 생성한다.
    - Text-to-asset 방식은 **score distillation sampling**을 사용하는 텍스트 기반의 생성 모델을 통해 3D 표현을 샘플링한다.
- 다음의 장/단점을 갖는다.
    - (+) 확장가능성이 높고 이미 개발된 생성형 모델을 활용할 수 있다는 장점이 있다.
    - (-) 데이터의 품질과 현실성이 낮을 수 있고, 제어가능성이 낮은 편이다. 조명 조건이 학습 데이터에 따라 위화감이 발생하기 쉽다.
- 다음의 논문을 참고하자.
    - GINA-3D: Learning to Generate Implicit Neural Assets in the Wild (CVPR23)
    - Zero-1-to-3: Zero-shot One Image to 3D Object (ICCV23)
    - ReconFusion: 3D Reconstruction with Diffusion Process (CVPR24)
    - LRM: Large Reconstruction Model for Single Image to 3D (ICRL24)
    - DreamFusion: Text-to-3D using 2D Diffusion (ICRL23)
    - Magic3D: High Resolution Text-to-3D Content Creation (CVPR23)
    - Instant3D: Fast Text-to-3D with Sparse View Generation and Large Reconstruction Model (ICRL24)
    - Align Your Gausssian: Text-to-4D with Dynamic 3D Gaussians and Composed Diffusion Models (CVPR24)

##### Adverasial Assets

- Out-of-Distribution 에셋을 생성하여 코너 케이스에 대응할 수 있다.
- 다음의 장/단점을 갖는다.
    - (+) 물리적으로 가능하며 일반적이며 이동가능한 에셋을 만드는 것이 목적이다.
    - (-) 단, 일반적이거나 현실적이지 않은 경우를 충분히 잘 모사할 수 있는지는 의문이다.
- 다음의 논문을 참고하자.
    - Invisible for both Camera and LiDAR
    - Physically Realizable Adversarial Examples for LiDAR Object Deteciton (CVPR20)
    - Exploring Adersarial Robustness of Multi-sensor Perception System for Self-Driving (CoRL21)
    - Generating Transferable Adversarial Simulation Scenarios for Self-Driving via Neural Rendering (CoRL23)

#### Deformable Actor Assets

- 관절을 가지고 움직일 수 있는 보행자 등의 변형 가능한 에셋을 생성하는 기술은 다음과 같다.
    - [[#Model-based Approach]]
    - [[#Model-free and Hybrid Approaches]]

##### Model-based Approach

- 이미지, 라이다 등을 통해 측정된 2D/3D 정보를 이용하여 특정 parametric model을 추정하는 방식이다.
    - 이 과정에서 2D keypoints/segmentation 정보 혹은 human model인 SMPL 등에 의존한다.
- 다음의 장/단점을 갖는다.
    - (+) Parametric model을 사용하는 만큼 구조적인 사전 정보(structural prior)를 활용하여 측정치로 부터 빈 곳이나 결함 없이 예측할 수 있다.
    - (+) 사용하는 정보 사이의 연결 지점 사이의 정확한 매칭 관계인 dense correspondence를 찾는 것이 중요하다.
    - (-) 구조적 관계를 복원하는데 집중하기 때문에 세밀한 디테일이 무시되며, 복원한 3D 모델과 이미지 정보가 일치하지 않을 수 있다.
- 다음의 논문을 참고하자.
    - LiME: Recovering and Simulating Pedestrians in the Wild (CoRL20)
    - PHOSA: Perceiving 3D Human-Object Spatial Arrangemennts from a Single Image in the Wild (ECCV20)
    - VAREN: Very Accurate and Realistic Equine Network (CVPR24)
    - WHAM: Reconstructing World-grounded Humans with Accurate 3D Motion (CVPR24)
    - TokenHMR: Advancing Human Mesh Recovery with a Tokenized Pose Representation (CVPR24)

##### Model-free and Hybrid Approaches

- 실제 측정 정보에서 형상을 표현하는 암묵적 표현(implicit representation) 을 학습한다.
    - 이 과정에서 2D segmentation이나 3D supervision 정보를 활용한다.
- 다음의 장/단점을 갖는다.
    - (+) 임의의 topology나 형상을 다룰 수 있으며 별도의 형상 템플릿 정보가 불필요하다.
    - (-) 정상적이고 완전한 형상이 나온다고 장담할 수 없다.
    - (-) 모델을 학습시키기 위해 많은 데이터가 필요하거나 생성이 매우 느리다.

### Sensor Simulation

- 센서 시뮬레이션에서는 현실성, 제어가능성, 다양성, 속도가 중요한 지표이다.
- 센서 시뮬레이션은 크게 3가지 범주로 구분할 수 있다.
    - Physics
    - Data
    - Neural Nets
- 위의 범주를 기반으로 범주를 추가하면 다음과 같다.
    - Data + Physics: Data-driven physics
    - Data + Neural Nets: Generative Models

#### LiDAR

- 물리기반 라이다 시뮬레이션은 빛과 객체 간의 상호작용을 물리 기반으로 모델링한다.
    - 대표적인 기법으로 **raytracing**, **rasterization**, **volumenn rendering**, waveform modeling, material modeling 등이 있다.
- 데이터 기반 라이다 시뮬레이션은 데이터를 사용하여 parametric model을 추정하고 이를 랜더링한다.
    - 대표적으로 추정하는 파라미터는 센서 parameter나 geometry, material, noise, view-warping observation (라이다 출력에서 발생하는 왜곡)등이 있다.
    - 참고 논문
        - LiDAR with data-driven primitives (ICRA18)
        - Modelling on Material and Lidar Capabilities (Sensors20)
        - Physics-based Simulation of Continuous-Wave LiDAR (ICRA20)
        - Augmented LiDAR Simulator for Autonomous Driving (RA-L20)
- 뉴럴넷 기반 라이다 시뮬레이션은 데이터에서 라이다 출력을 생성하는 생성형 모델(unsuperviesd)이나 스타일 변환(paired/unpaired), 뉴럴 랜더링(supervised) 모델을 학습한다.
- 물리 + 데이터 + NN 방식을 통해 성능을 향상시키기 위해 다양한 센서 시뮬레이션 연구가 진행되고 있다. 

##### Simple Physics

- 그래픽스 엔진을 이용해서 3D 가상 공간에 에셋을 배치하고 이를 통해 라이다 데이터를 생성한다.
    - 3D 가상 공간에서 라이다 센서를 위한 **raycasting**을 수행한다.
- 다음의 장/단점을 갖는다.
    - (+) 장면 전체에 대한 전체 제어권을 가지고 간단하고 빠르게 데이터를 생성할 수 있다.
    - (-) 물리 모델이 간단할 경우 현실과의 domain-gap이 발생한다.
- 다음의 논문을 참고하자.
    - CARLA (CoRL17)

##### Complex Physics

- 그래픽스 엔진을 이용하기 하지만 복잡한 물리 모델과 센서 모델을 사용한다.
- 다음의 장/단점을 갖는다.
    - (+) 전체 장면과 센서에 대한 전체 제어권을 갖는다.
    - (+) 현실과의 domain-gap을 최대한 줄일 수 있다.
    - scene과 센서 모델을 구축하기 위해 많은 지식과 노력이 필요하다.
    - 복잡한 모델을 사용하는 만큼 랜더링 시간이 오래 걸린다.
- 다음의 논문을 참고하자.
    - DIRSIG5 (SPIE12)

##### Data + NN

- 생성형 모델을 이용하여 노이즈와 조건부 표현(conditioned representation)을 입력받아 라이다 출력을 생성한다.
    - 생성형 모델을 통해 장면 표현을 암묵적으로 학습하고 이로 부터 라이다 센서 출력을 생성한다.
- 다음의 장/단점을 갖는다.
    - (+) 간단하고 빠르며 보지 못한 곳도 생성할 수 있다는 장점을 가지고 있다.
    - (-) 모델이 센서 출력을 직접 생성하므로 제어가능성이 낮다.
    - (-) 학습에 사용한 특정 라이다 센서의 특성에 과적합될 수 있다.
    - (-) 물리적 타당성(physicial plausibiilty)를 보장할 수 없다.
- 다음의 논문을 참고하자.
    - VISTA 2.0 (ICRA22)
    - Deep Generative Modeling of LiDAR Data (IROS19)
    - DUSty (IROS21), DUSty v2 (WACV23)
    - LiDARGen (ECCV22)
    - UltraLiDAR (CVPR23)
    - LiDAR Diffusion Models (CVPR24)
    - RangeLDM (Arxiv24)

##### Physics + Data + NN

- 실제 라이다 데이터를 기반으로 3D 가상 공간의 에셋에 대한 raycasting 방식을 개선하여 라이다 출력을 생성한다.
    - 다음의 장/단점을 갖는다.
        - (+) 3D 가상 공간에서 에셋을 배치하므로 scene에 대한 전체 제어권이 있으며, 실제 라이다 센서에 가까운 출력을 만들 수 있다.
        - (-) 실제 라이다 센서 데이터를 통해 학습할 때, 보지 못한 객체에 대해서는 출력 생성이 어렵고 데이터 수집과정에서 들어간 노이즈를 처리하기 어렵다.
    - 참고 논문
        - LiDARsim (CVPR20)
        - PCGen (arXiv22)
        - Learning to Simulate Realistic LiDARs (IROS22)
- 실제 라이다 데이터를 학습하여 에셋과 객체 배치, raycasting 방식 등을 모두 생성형 모델로 만드는 방식도 있다.
    - (+) 별도로 에셋과 시나리오를 준비할 필요가 없으며 필요한 경우 traffic layout을 입력받아 활용할 수 있다.
    - (-) 학습 데이터에 없는 객체에 대해서는 출력을 생성하기 어려우며 상대적으로 부정확하다.
    - 참고 논문
        - LidarDM (arXiv24)
- 뉴럴 랜더링을 통해 실제 라이다 출력과 일치하는 출력을 생성할 수 있는 암묵적 표현을 학습하거나 volume rendering을 개선하는 방식도 있다.
    - (+) scene reconstruction과 랜더링 품질이 좋다.
    - (-) scene단위로 최적화를 해야하며 랜더링 속도가 느리며 큰 시점이동 시 성능이 저하될 수 있다.
    - 참고 논문
        - LiDAR-NeRF (arXiv23)
        - Dynamic LiDAR Re-simulation (CVPR24)

#### Radar

- 일반적으로 모델링하기 가장 어려운 자율주행 센서에 해당한다.
    - 라이다나 카메라에 비해 노이즈가 많고 주변 환경에 의한 파동전파(wave propagation)을 많이 받기 때문이다.
    - 또한 형상 정보(appearance, geometry) 정보 이외에 **도플러 정보(속도)** 도 제공하애 한다.
- 물리 기반 레이더 시뮬레이션은 그래픽스 엔진과 에셋을 활용하여 raycasting을 통해 ray를 방출하고 그것이 반사되는 파장 변화를 시뮬레이션한다.
    - 이 과정에서 레이더 센서에 대한 시뮬레이션을 수행할 때, 공개되지 않은 후처리 과정을 모델링해야하는 어려움이 있다.
- 데이터 기반 레이더 시뮬레이션은 실제 수집된 데이터를 객체 단위로 재활용하는 것을 말한다.
    - 수집된 데이터에서 최대한 유사한 상황을 찾아 해당 측정 데이터를 활용하는 것이다.
    - NVIDIA에서 이야기한 **Radar reprojection**이 이에 해당한다.
- 뉴럴넷 기반 레이더 시뮬레이션은 데이터에서 레이더 출력을 생성하는 생성형 모델(unsuperviesd)이나 스타일 변환(paired/unpaired), 뉴럴 랜더링(supervised) 모델을 학습한다.
- 물리 + 데이터 + NN 방식으로는 라이다나 카메라 센서를 통해 학습된 volume rendering 모델을 레이더 스캐닝을 다룰 수 있도록 변형하는 방식이 있다.
    - 아직까지는 다양한 자율주행 상황과 환경에 적용하기에 부족한 면이 많다.
    - 참고 논문
        - DART: Implicit Doppler Tomography for Radar Novel View Synthesis (CVPR24)
        - Radar Fields (arXiv24)
        - SAR-NeRF (arXiv24)

#### Camera

카메라는 라이다나 레이더와 달리 광원으로부터 발생하는 가시광선 파장 스펙트럼을 수신하는 **수동형 센서**이다.
카메라 시뮬레이션에서는 이렇게 수신된 빛 정보를 이미지로 변환하는 과정인 ISP (Image Signal Processing)에서 어려움이 있다.
다른 센서 시뮬레이션과 마찬가지로 물리, 데이터, 뉴럴넷 방식을 결합하여 현실적이며 확장성을 높이는 쪽으로 진화하고 있다.

- 물리 기반 카메라 시뮬레이션은 그래픽스 엔진과 에셋을 활용하여 raytracing이나 rasterization을 수행한다.
- 데이터 기반 카메라 시뮬레이션은 실차에서 취득된 이미지를 시뮬레이션에 활용하는 것을 말한다.
- 뉴럴넷 기반 카메라 시뮬레이션은 실차에서 취득된 이미지를 통해 새로운 이미지를 생성하는 생성형 모델(unsuperviesd)이나 스타일 변환(paired/unpaired), 뉴럴 랜더링(supervised) 모델을 학습한다.

자율주행을 위해 학습 기반의 **Neural reconstruction**에 기반한 **Novel view synthesis**나 **Dynamic actor simulation**과 같은 목적 특화 연구가 진행되었으며 최근에는 **Full camera simulation**에 대한 연구가 활발히 진행되고 있다.

##### Graphcis-Based Methods

###### Standard Graphics

- Carla나 GTA와 같은 그래픽스 엔진을 사용한다.
    - 일반적으로 실시간 랜더링이 이뤄지려면 이미지 품질이 낮아진다.
    - 각 에셋이 정확한 물성이 설정되어 있어야 현실적인 센서 데이터 생성이 가능하다.
    - 제어 가능성이 높지만 현실과의 domain-gap이 발생한다.

###### Graphics + NN

- 그래픽스 엔진에서 semantic segmentation이나 관련 frame buffer를 만들어내고 NN을 이용해서 현실적으로 랜더링한다.
- 그래픽스 엔진의 제어가능성과 NN을 통한 현실성 강화를 동시에 얻을 수 있다.
- 그래픽스 엔진이 만들 수 있는 장면과 상황이 제한적일 수 있으며 다중 시점 이미지 생성 시 일관성 문제가 발생할 수 있다.
- 참고 논문
    - CRN (ICCV17)
    - pix2pixHD (CVPR18)
    - vid2vid (NeurIPS18)
    - SPADE (CVPR19)
    - CyCADA (ICML18)
    - Enhancing Photorealism Enhancement (EuroGraphics21)

###### NeRF + 3DGS

- 주행 환경에 대해서 NeRF나 3DGS를 통해 3D 환경과 에셋을 복원하고 이를 랜더링한다.
    - 제어가능성과 현실적인 이미지를 얻을 수 있다는 장점이 있다.
    - NeRF의 경우 랜더링 속도가 느리지만 (< 1FPS), 3DGS는 실시간 랜더링이 가능하다. (> 60FPS)
    - 불완전한 복원으로 인해 시점 변화가 제한될 수 있다.
    - 3DGS는 LiDAR 데이터를 활용하여 기하학적 구조를 초기화함으로써 고품질 장면 복원이 가능하다.
- NeRF를 통해 장면의 기하(geometry), 물질(material), 외관(appearance), 조명 조건(lighting condition)$을 역으로 복원하는 것을 **inverese rendering**이라 한다.
    - 역 랜더링을 통해 조명 조건을 변화시킬 수도 있다.
- 참고 논문
    - UniSim (CVPR23)
    - SUDS (CVPR23)
    - MARS (CICAI23)
    - StreetSurf (arXiv23)
    - EmerNeRF (ICRL24)
    - Multi-level NSG (arXiv24)
    - Driving Gaussian: Composite Gaussian Splatting for Surrounding Dynamic Autonomous Driving Scenes (CVPR24)
    - Street Gaussians for Modeling Dynamic Urban Scene Reconstruction and Real-time Rendering (arXiv24)
    - Periodic Vibration Gaussian: Dynamic Urban Scene Reconstruction and Real-time Rendering (arXiv24)
    - S3Gaussian: Self-Supervised Street Gaussians for Autonomous Driving (arXiv24)
    - FEGR: Neural Fields meet Explicit Geometric Representation for Inverse Rendering of Urban Scenes (CVPR23)
    - LightSim: Neural Lighting Simulation for Urban Scenes (NeurIPS23)
    - UrbanIR: Large-Scale Urban Scene Inverse Rendering from a Single Video (arXiv23)

##### Diffusion Model (World Model)

- 대규모 데이터로 월드 모델을 학습시키고 이를 이용하여 고품질의 카메라 데이터를 생성할 수 있다.
    - 현실 세계의 물리와 외관 정보를 암묵적으로 학습한 모델이 월드 모델이다.
- 일반적인 센서 시뮬레이션 방식 대비 더 다양성이 높은 데이터를 생성할 수 있다.
- Scene Rconstruction 기법 대비 외삽 (extrapolation) 성능이 더 좋을 수 있다.
- 액터의 정확한 위치나 궤적 같은 세밀한 제어가 어려우며, 학습 데이터 분포에서 벗어나는 경우, 데이터 분포에 맞추기 위해 액터를 사라지거나 흐릿하게 표현 할 수 있다.
    - 결국 평가 지표 등도 제공하지 못하는 경우가 많다.
- 일반적으로 생성 속도가 느린 편이며 높은 훈련 비용이 필요하다.
- 위의 단점들로 인해 일반적으로는 폐루프 시뮬레이션에 활용하기 어렵다고 판단된다.
    - **(Comment)** [[(Talk) Tesla-Building Foundation Model For AD|테슬라의 Talk]]에서는 WorldSim NN을 만들어 사용하고 있으므로 리서치가 필요하다.

<p class="img-center">
  <img src="Attachments/20251115-124451.png" alt="Sensor Simulator vs World Model" style="max-width:700px; width:100%">
</p>

- 참고 논문
    - Align your Latents: High-Resolution Video Synthesis with Latent Diffusion Models (CVPR23)
    - GAIA-1: A Generative World Model for Autonomous Driving (arXiv23)
    - Copilot4D: Learning Unsupervised World Models for Autonomous Driving via Discrete Diffusion (ICLR24)
        - 라이다 포인트 생성 가능
    - Sora: Creating video from text(https://openai.com/sora)
    - DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving (arXiv23)
    - MagicDrive: Street View Generation with Diverse 3D Geometry Control (arXiv23)
    - DrivingDiffusion: Layout-Guided multi-view driving scene video generation with latent diffusion model (arXiv23)
    - ADriver-I: A General World Model for Autonomous Driving (arxiv23)
    - Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability (arXiv24)
        - 자유주행 특화 비디오 생성

##### Etc.

- 카메라와 라이다 데이터를 함께 생성할 수 있는 연구는 다음과 같다.
    - UniSim: A Neural Closed-loop Sensor Simulator (CVPR23)
    - NeuRAD: Neural Rendering for Autonomous Driving (CVPR24)
    - AlignMiF: Geometry-Aligned Multi-modal Implicit Field for LiDAR-Camera Joint Synthesis (CVPR24)
- NN 기반 이미지 생성과 시나리오 시뮬레이션을 결합한 연구는 다음과 같다.
    - ChatSim: Editable Scene Simulation for Autonomous Driving via LLM-Agent Collaboration (CVPR24)
    - OASim: an Open and Adaptvie Simulator based on Neural Rendering for Autonomous Driving (arXiv24)
- 현실적인 이미지를 이용한 폐루프 안전 시험과 관련된 연구는 다음과 같다.
    - UniSim: A Neural Closed-loop Sensor Simulator (CVPR23)
    - NeuroNCAP: Photorealistic Closed-loop Safety Testing for Autonomous Driving (arXiv24)

##### Novel View Synthesis

###### Image Warping

- 실제 차량에서 취득한 데이터로 부터 3D 깊이 정보를 추정하고 이를 기반으로 새로운 시점의 영상을 다시 랜더링한다.
    - 이 과정에서 bilinear interpolation이나 in-painting 기법등을 이용한다.
    - 빠르고 합리적이게 현실적인 데이터를 생성할 수 있다.
    - 큰 시점 변환은 어려우며, 깊이 추정이 부정확하면 성능이 열화된다. 또한 날씨 같은 환경변화도 불가능하다.
- 참고 논문
    - Learning Rubust Control Policies for End-to-End Autonomous Driving from Data-Driven Simulation (RA-L20)
    - AADS: Augmented autonomous driving simulation using data-driven algorithms (Sciene Robotics20)

###### NeRF, 3D Gaussian Splatting

- 실제 차량에서 취득된 데이터를 이용하여 센서 데이터를 랜더링할 수 있는 메쉬 모델이나 가우시안을 만들다.
    - NeRF는 volumetric representation을 통해 라이다, 레이더 데이터도 생성할 수 있다.
        - Gaussian Splatting 대비 상대적으로 학습과 생성에 대한 비용이 높다.
    - Gaussian Splatting은 장면을 sparse point set으로 표현하고 이를 빠르게 카메라 이미지로 변환할 수 있다.
        - NeRF 대비 상대적으로 높은 frame rate을 가지고 있지만, 다른 센서 데이터 생성은 제약이 있다.
- 이를 이용해 새로운 시점 변화를 랜더링한다.
- 큰 공간에 대한 현실적인 랜더링이 가능하다.
- 3D 복원이나 랜더링에 큰 자원소모 (시간 + 연산)이 필요하다.
- 참고 논문
    - Block-NeRF: Scalable Large Scene Neural View Synthesis (CVPR22)
    - Vast Gaussian: Vast 3D Gaussians for Large Scene Reconstruction (CVPR24)
    - Real-Time Neural Rasterization for Large Scenes (ICCV23)
    - Inovis: Instant Novel-View Synthesis (SIGGRAPH23)

###### Scene Editing

- 단순한 장면 재구성을 넘어서 재구성된 장면에서 조명이나 날씨를 변경하는 장면 편집 연구가 시도되고 있다.
    - 눈이나 안개 등을 모사하기 위해 파티클을 활용하여 원본 배경과 융합하여 랜더링을 수행한다.
    - NeRF 등으로 추출한 메쉬에 그래픽스 엔진을 활용하여 조명 조건을 변경한다.
- 참고 논문
    - ClimateNeRF: Physically-based Neural Rendering for Extreme Climate Synthesis (arXiv23)
    - Neural Field meets Geometric Representation for Inverse Rendering of Urban Scene (CVPR23)

##### Actor Insertion

- CAD 에셋을 기존에 취득된 이미지의 조명 조건에 맞게 랜더링하고 이를 이미지에 삽입한다.
    - 삽입을 원하는 이미지의 조명 조건에 맞게 CAD 에셋의 조명 조건을 변경하지 위해 주변 환경과 material정보가 필요하다.
    - 다수의 객체를 삽입할 경우 가림을 처리하기 어렵다.
- 가림에 대한 처리를 위해 장면에 대한 dense depth map을 추정하여 삽입하려는 객체의 가림을 결정한 후 NN을 통해 객체를 삽입하는 연구도 있다.
    - GeoSim: Realistic Video Simulation via Geometry-Aware Composition for Self-Driving (CVPR21)

## Vehicle Platform Modeling

### Vehicle Dynamics

- 현실적이며 동시에 효율적인 자차의 동적 모델을 모델링해야 한다.
- 대표적인 모델에는 다음이 있다.
    - Kinematic bicycle model
    - Dynamic bicycle model
- CommonRoad: Vehicle Models (2020)을 참고하자.

#### Kinematic Bicycle Model

- 차량을 자전거와 같이 앞바퀴와 뒷바퀴만 있는 형태로 모델링한다.
    - 차량 전방과 후방의 바퀴들이 각각 하나의 바퀴로 조합된다.
- 차량 움직임이 2차원 평면에서 발생하고 타이어 슬립은 고려하지 않는다.
- 간단하고 추정할 파라미터가 적다.
- 차량의 중량, 관성, 타이어 슬립 등을 고려하지 않기 때문에 현실과 동떨어진 결과가 나오는 경우가 많다.

<p class="img-center">
  <img src="Attachments/20251115-130451.png" alt="Kinematic Bicycle Model" style="max-width:300px; width:100%">
</p>

#### Dynamic Bicycle Model

- 차량을 자전거와 같이 앞바퀴와 뒷바퀴만 있는 형태로 모델링한다.
    - 차량 전방과 후방의 바퀴들이 각각 하나의 바퀴로 조합된다.
- 차량의 중량, 관성, 타이어 강성 등을 고려한 복잡한 모델이다. - 여전히 많은 가정이 들어가기 때문에 현실과 동떨어진 결과가 나오기도 한다.
  <p class="img-center">
  <img src="Attachments/20251115-130641.png" alt="Dynamic Bicycle Model" style="max-width:300px; width:100%">
</p>

## HIL

- HIL(Hardware-In-the-Loop) 시뮬레이션은 전체 자율주행 SW를 실제 차량의 computing hardware와 통신 네트워크를 이용하여 시뮬레이션하는 것을 말한다.
    - 이 과정에서 실제 센서 데이터 혹은 현실적으로 합성된 센서 데이터를 입력한다.
- SIL(Software-In-the-Loop) 시뮬레이션 과의 차이는 다음과 같다.
    - SIL이 대규모의 병렬 테스트를 위해 클라우드 컴퓨팅을 수행한다면, HIL은 현실적인 테스트를 위해 실제 차량에 탑재될 연산장치와 설정을 사용한다.
    - SIL이 가속 시뮬레이션을 통해 실시간보다 빠르게 시뮬레이션을 수행한다면, HIL은 실시간 성능을 확인하는 것이 목표이다.
    - SIL은 실제 차량의 연산 장치와 상호작용하며 SW를 테스트하지 않지만, HIL은 해당 상호작용까지 잘 동작하는 것을 확인하는 것이 목표이다.
        - HIL은 별도의 테스트 벤치 구축이 필요하다.

## Reference

1. [(08) Simulation (Waabi CVPR24 Tutorial on Self-Driving Cars)](https://youtu.be/0jQnNxaqiSU?si=3FDQYQF2epnx3QqA)
1. [NotebookLM](https://notebooklm.google.com/notebook/64c8d7e9-2e85-4acf-83a9-ab879271cd80)
