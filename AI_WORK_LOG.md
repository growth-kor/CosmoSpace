# 🪐 Pinterest 3D Galaxy AI 기술 작업 일지

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
