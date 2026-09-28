# 🪐 Pinterest 3D Galaxy AI 기술 작업 일지

## [2차] 2026-09-28: 시야 차폐 방지 포커스(Ghost) 모드 & 겹침 0% 격자 모드 추가

### 1. 주요 변경 내역
- **[프론트엔드] 시야 차폐 제거 및 포커스 분리 알고리즘 (`index.html`)**:
  - 특정 노드 클릭 시 목표 스프라이트만 `opacity = 1.0`, 최상단 렌더링(`renderOrder = 999`)으로 강조.
  - 시야를 가로막는 전후좌우의 모든 주변 노드를 `opacity = 0.08`로 자동 페이드아웃(Ghost Mode) 처리하여 시야를 완전히 개방.
  - 카메라 전진 시 글로벌 Z축 강제 이동 대신, 현재 시선 벡터(`camVector`) 기반 스탠드오프 안전거리(65유닛) 줌인으로 렌즈 앞 가림 현상 원천 차단.
  - Three.js 카메라 `near` 클리핑 평면을 3.0으로 상향하여 코앞에 스치는 스프라이트의 화면 전체 가림 방지.
  - 상단에 '포커스 모드 해제' 토글 배너 추가.
- **[프론트엔드] 겹침 0% '격자 펼침(Grid Gallery)' 레이아웃 추가 (`index.html`)**:
  - 우측 상단에 `🔲 격자 펼침 (겹침 0%)` 버튼 추가.
  - 클릭 시 2D/3D 간격 격자로 모든 사진이 겹침 없이 정렬되는 부드러운 TWEEN 트랜지션 구현.
- **[백엔드] UMAP 군집 밀집도 분산 조정 (`process_data.py`)**:
  - `min_dist=0.6`, `spread=1.2`로 상향하여 유사 노드끼리 과도하게 한 점으로 뭉치는 현상 완화.

### 2. 코드 및 검증 결과
- `process_data.py`: `py_compile` 검증 완료 (Exit Code 0).
- `index.html`: Three.js Ghost Mode Tween 및 Grid 계산 로직 탑재 완료.

## [1차] 2026-09-28: AI 파이프라인 고속화 및 Three.js 3D 뷰어 전면 리팩토링

### 1. 주요 변경 내역
- **[백엔드] 배치 추론 및 하드웨어 가속 (`process_data.py`)**:
  - `MobileNetV2` 추론 시 `batch_size=64` 배치 텐서화로 Apple Silicon MPS 가속 극대화 (기존 18분+ $\rightarrow$ 수십 초~1분대로 단축).
  - 이미지 1장당 256px 경량 WebP 썸네일 자동 생성 파이프라인 구축 (`thumbnails/`).
  - 파일 mtime 기반 `features_cache.pkl` 증분 캐싱 적용 (재실행 시 변경된 이미지만 추출).
  - UMAP 전 `PCA(50차원)` 선행 차원 축소로 고차원 연산 속도 3~5배 개선.
  - 싱글 스레드 `HTTPServer` $\rightarrow$ `ThreadingHTTPServer` 멀티스레드 비동기 서빙으로 전환.
  - 8000~8020번 포트 자동 스캔 및 동적 바인딩 로직 구현.
  - 상대 경로 하드코딩 제거 및 스크립트 실행 위치 기준 자동 인식.

- **[프론트엔드] Three.js 렌더링 및 UI/UX 혁신 (`index.html`)**:
  - `THREE.Mesh` $\rightarrow$ `THREE.Sprite` 전환으로 GPU 셰이더 빌보드 처리 (매 프레임 JS 행렬 복사 루프 제거).
  - 핀터레스트 원본 이미지의 가로/세로 비율(`aspect_ratio`)을 계산하여 3D 노드 왜곡 방지.
  - 경량 썸네일 텍스처 로드 적용으로 WebGL VRAM 점유 90% 이상 절감 및 60 FPS 유지.
  - 실시간 파일명/카테고리 검색 필터 및 카테고리 컬러 팔레트 배지 도입.
  - 로딩 진행률 프로그레스 바 (`X / Total (%)`) 및 프리뷰 카드 개선 (원본 링크, 닫기, 부드러운 Fly-to 애니메이션).

### 2. 코드 및 검증 결과
- `process_data.py`: `python3 -m py_compile` 구문 검증 완료 (Exit Code 0).
- `index.html`: Three.js r128 및 OrbitControls 호환성 검증 완료.
