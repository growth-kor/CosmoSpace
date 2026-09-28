# 🪐 CosmoSpace 3D Studio

> **수천 장의 사진을 웹 브라우저 안에서 멈춤 없이 3D 우주 은하계로 펼쳐내는 차세대 인터랙티브 포토 스페이스**  
> Pure Client-Side 3D Planetary Galaxy Image Gallery powered by Three.js

[![GitHub Pages](https://img.shields.io/badge/Live_Demo-GitHub_Pages-6366f1?style=for-the-badge&logo=github)](https://growth-kor.github.io/CosmoSpace/)
[![Three.js](https://img.shields.io/badge/Three.js-r128-black?style=for-the-badge&logo=three.js)](https://threejs.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

---

## 🌌 Overview (프로젝트 소개)

**CosmoSpace**는 서버 업로드나 개인정보 유출 걱정 없이, 내 컴퓨터의 사진 폴더를 브라우저에 끌어다 놓는 즉시 100% 클라이언트 환경에서 아름다운 3D 우주 은하계 행성계로 변환해 주는 혁신적인 웹 애플리케이션입니다.

수천, 수만 장의 대용량 사진도 브라우저 멈춤(Freezing) 없이 매끄럽게 탐색할 수 있도록 설계된 **인메모리 고속 압축 캔버스 엔진**과 **피보나치 구면 알고리즘**을 탑재하여, 압도적인 비주얼과 극강의 성능을 동시에 제공합니다.

🔗 **라이브 데모 바로가기**: [https://growth-kor.github.io/CosmoSpace/](https://growth-kor.github.io/CosmoSpace/)

---

## ✨ Key Features (핵심 기능)

### 🪐 1. 폴더별 3D 독립 행성계 (Planetary Galaxy)
* **피보나치 구면 알고리즘(Fibonacci Hollow Sphere)**: 사진들이 구체 안쪽에 묻히지 않고, 오차 0% 완벽한 균등 간격으로 행성 표면에 아름답게 펼쳐집니다.
* **황금비 나선 성간 궤도**: 각 폴더가 가진 사진 수량에 비례하여 행성 반지름과 충돌 방지 안전거리를 자동 계산, 우주 은하 나선 궤도에 조화롭게 분산 배치합니다.

### 📁 2. 무제한 파일 트리 재귀 탐색 & 스마트 분류
* **브라우저 드래그 앤 드롭 (`webkitGetAsEntry`) 지원**: 복잡한 다중 하위 폴더 구조도 폴더를 통째로 화면에 던져 넣으면 재귀적으로 모든 사진을 완벽 추출합니다.
* **스마트 카테고리 분리**: 루트 직속 사진과 하위 폴더 사진을 자동으로 지능 식별하여 각각 독립된 우주 행성으로 분리 구축합니다.

### ⚡ 3. 100% 클라이언트 인메모리 압축 (Zero VRAM Leak)
* **Offscreen Canvas 경량화 엔진**: 원본 이미지를 브라우저 내부에서 실시간 300px 고화질 WebP로 인메모리 압축하여 VRAM 폭발과 메인 스레드 멈춤을 원천 차단합니다.
* **LRU-10 고화질 캐시**: 전체 탐색은 경량화된 텍스처로 60fps를 유지하며, 더블 클릭으로 포커스한 사진만 원본 고해상도로 즉시 스왑합니다.

### 🔀 4. 3가지 차원 레이아웃 실시간 전환
* **폴더 행성계 (`Galaxy`)**: 각 폴더가 우주 은하의 독립 행성으로 군집을 이루는 기본 모드.
* **단일 거대 구체 (`Sphere`)**: 모든 사진을 하나의 웅장한 거대 구체 표면으로 재배치하는 조망 모드.
* **2D 정밀 그리드 (`Grid`)**: 오차 없는 바둑판 수직/수평 정렬로 모든 사진을 한눈에 검토하는 정렬 모드.

### 🎮 5. 심우주 자유 비행 & WASD 네비게이션
* **OrbitControls 360도 회전**: 마우스 드래그를 통한 자유로운 궤도 선회 및 줌 인/아웃.
* **WASD 비행 제어**: 우주선 조종석에 앉은 듯 시선 방향으로 직접 전진/후진/좌우 유영.
* **실시간 물리 슬라이더**: 은하 팽창(Spread), 노드 크기(Size), 배경 흐림(Dimming), 회전 속도(Auto-Rotate)를 실시간 조절.

### 🎵 6. 인터랙티브 음향 시스템 & 온보딩 가이드
* **선명한 글래스 사운드**: 모든 버튼과 카드 조작 시 경쾌한 오디오 풀 기반의 딸깍 사운드 피드백.
* **고조 사토루 영역전개 BGM**: 스폰서 카드 진입 시 몰입감을 극대화하는 사운드 연출.
* **5단계 인터랙티브 온보딩 가이드**: 첫 방문자도 10초 만에 완벽하게 조작법을 익힐 수 있는 튜토리얼 카드 제공.

---

## 🕹️ Controls (조작법 안내)

| 동작 | 조작 방법 | 설명 |
|---|---|---|
| **3D 시점 회전** | **마우스 좌클릭 + 드래그** | 은하계 공간을 360도 자유롭게 둘러봅니다. |
| **화면 평면 이동 (Pan)** | **마우스 우클릭 + 드래그** | 카메라 중심을 상하좌우로 이동합니다. |
| **줌 인 / 줌 아웃** | **마우스 휠 스크롤** or **`[` / `]` 키** | 카메라 거리를 당기거나 멀어지게 조절합니다. |
| **사진 포커스 모드** | **사진 더블 클릭 (Double Click)** | 대상 사진을 고화질로 확대하고 상세 카드(미리보기/비율/카테고리)를 엽니다. |
| **심우주 자유 비행** | **키보드 `W`, `A`, `S`, `D`** | 시선 방향을 기준으로 공간을 직접 날아다닙니다. |
| **다중 폴더 필터링** | **상단 폴더 버튼 클릭** | 원하는 폴더들을 중복 선택하여 해당 행성들만 집중 탐색합니다. |
| **전체 조망 복귀** | **`[전체보기]` 버튼 클릭** or **`ESC` 키** | 즉시 은하계 전체 중심 `(0, 0, 0)` 조망 시점으로 스무스하게 줌아웃 복귀합니다. |

---

## 🛠️ Technology Stack (기술 스택)

* **Core Engine**: HTML5, Vanilla JavaScript (ES6+), WebGL
* **3D Library**: [Three.js (r128)](https://threejs.org/)
* **Animation**: [Tween.js](https://github.com/tweenjs/tween.js/)
* **Control**: Three.js OrbitControls
* **Styling**: Vanilla CSS3 (Glassmorphism, Backdrop Blur, Neumorphic Glow)
* **Audio**: HTML5 Web Audio API

---

## 🚀 Getting Started (시작하기)

별도의 백엔드 서버나 빌드 과정 없이, HTML 파일 하나로 즉시 실행할 수 있습니다.

```bash
# 1. 저장소 복제 (Clone Repository)
git clone https://github.com/growth-kor/CosmoSpace.git

# 2. 프로젝트 디렉터리 이동
cd CosmoSpace

# 3. 로컬 브라우저에서 index.html 열기 (또는 Live Server 실행)
open index.html
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 **growth-kor**. All rights reserved.
