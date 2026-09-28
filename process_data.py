import os
import sys
import subprocess
import threading
import time
import webbrowser
import pickle
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

# -------------------------------------------------------------
# 1. 작업 디렉터리 동적 설정 (스크립트 위치 기준 자동 인식)
# -------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)
print(f"[*] 기준 작업 디렉터리: {CURRENT_DIR}")

# -------------------------------------------------------------
# 2. 필수 라이브러리 확인 및 자동 설치
# -------------------------------------------------------------
REQUIRED_PACKAGES = {
    "torch": "torch",
    "torchvision": "torchvision",
    "PIL": "pillow",
    "numpy": "numpy",
    "umap": "umap-learn",
    "sklearn": "scikit-learn"
}

def install_and_import(module_name, package_name):
    try:
        __import__(module_name)
    except ImportError:
        print(f"[*] '{package_name}' 패키지가 없어 자동 설치를 진행합니다...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"[+] '{package_name}' 설치 완료!")

print("\n[단계 1/4] 필수 라이브러리 검증 중...")
for module, package in REQUIRED_PACKAGES.items():
    install_and_import(module, package)

import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from PIL import Image
import numpy as np
from sklearn.decomposition import PCA
import umap
import json

# -------------------------------------------------------------
# 3. 이미지 수집 및 썸네일/비율 계산 / 고속 배치 AI 임베딩
# -------------------------------------------------------------
print("\n[단계 2/4] 이미지 파일 스캔 및 AI 가속 모델 준비...")
BASE_DIR = CURRENT_DIR
OUTPUT_FILE = os.path.join(CURRENT_DIR, "galaxy_data.json")
CACHE_FILE = os.path.join(CURRENT_DIR, "features_cache.pkl")
THUMB_DIR = os.path.join(CURRENT_DIR, "thumbnails")
os.makedirs(THUMB_DIR, exist_ok=True)

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
print(f"[*] AI 연산 가속 장치: {device}")

weights = MobileNet_V2_Weights.DEFAULT
model = mobilenet_v2(weights=weights).to(device)
model.classifier = torch.nn.Identity()
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.avif')
images_to_process = []

# 이미지 탐색 (thumbnails 디렉터리는 제외)
for root, dirs, files in os.walk(BASE_DIR):
    if "thumbnails" in root or ".git" in root:
        continue
    for f in files:
        if f.startswith('.'):
            continue
        if f.lower().endswith(valid_extensions):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, BASE_DIR)
            rel_dir = os.path.dirname(rel_path)
            category = rel_dir.split(os.sep)[0] if rel_dir else "default"
            mtime = os.path.getmtime(full_path)
            
            images_to_process.append({
                "filename": f,
                "full_path": full_path,
                "rel_path": rel_path,
                "category": category,
                "mtime": mtime
            })

total_count = len(images_to_process)
print(f"[*] 총 {total_count}장의 이미지 발견.")

if total_count == 0:
    print(f"[!] 오류: '{BASE_DIR}' 경로에 유효한 이미지가 없습니다.")
    sys.exit(1)

# 캐시 로드
cache = {}
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "rb") as f:
            cache = pickle.load(f)
        print(f"[*] 기존 피처 캐시 {len(cache)}개 항목 로드 완료.")
    except Exception as e:
        print(f"[!] 캐시 파일 읽기 실패 (새로 생성): {e}")
        cache = {}

# 썸네일 생성 및 신규/수정 이미지 필터링
print("\n[단계 3/4] 썸네일 생성 및 AI 피처 추출(배치 고속화)...")
items_to_infer = []
valid_entries = []

for item in images_to_process:
    rel_p = item["rel_path"]
    full_p = item["full_path"]
    
    # 썸네일 경로 구성
    thumb_rel_dir = os.path.join("thumbnails", os.path.dirname(rel_p))
    os.makedirs(os.path.join(BASE_DIR, thumb_rel_dir), exist_ok=True)
    thumb_name = os.path.splitext(item["filename"])[0] + ".webp"
    thumb_rel_path = os.path.join(thumb_rel_dir, thumb_name)
    thumb_full_path = os.path.join(BASE_DIR, thumb_rel_path)
    
    # 캐시 검증
    cached = cache.get(rel_p)
    if cached and cached.get("mtime") == item["mtime"] and os.path.exists(thumb_full_path):
        item["feat"] = cached["feat"]
        item["aspect_ratio"] = cached.get("aspect_ratio", 1.0)
        item["thumb_path"] = thumb_rel_path
        valid_entries.append(item)
    else:
        item["thumb_path"] = thumb_rel_path
        item["thumb_full_path"] = thumb_full_path
        items_to_infer.append(item)

# 캐시되지 않은 항목들 배치 추론 및 썸네일 저장
if items_to_infer:
    print(f"[*] 신규/수정 이미지 {len(items_to_infer)}장 배치 추론 시작 (Batch Size: 64)...")
    BATCH_SIZE = 64
    
    with torch.no_grad():
        for b_idx in range(0, len(items_to_infer), BATCH_SIZE):
            batch_items = items_to_infer[b_idx:b_idx + BATCH_SIZE]
            batch_tensors = []
            valid_batch_items = []
            
            for it in batch_items:
                try:
                    with Image.open(it["full_path"]) as img:
                        w, h = img.size
                        aspect = round(w / max(h, 1), 4)
                        it["aspect_ratio"] = aspect
                        
                        # 썸네일 생성 (최대 256px)
                        if not os.path.exists(it["thumb_full_path"]):
                            thumb_img = img.copy()
                            thumb_img.thumbnail((256, 256), Image.Resampling.LANCZOS)
                            thumb_img.save(it["thumb_full_path"], "WEBP", quality=80)
                        
                        img_rgb = img.convert("RGB")
                        t = transform(img_rgb)
                        batch_tensors.append(t)
                        valid_batch_items.append(it)
                except Exception as e:
                    print(f"[!] 건너뜀 [{it['filename']}]: {e}")
            
            if batch_tensors:
                stacked = torch.stack(batch_tensors).to(device)
                feats = model(stacked).squeeze(-1).squeeze(-1).cpu().numpy()
                if len(valid_batch_items) == 1 and feats.ndim == 1:
                    feats = feats[np.newaxis, :]
                
                for it, feat in zip(valid_batch_items, feats):
                    it["feat"] = feat
                    cache[it["rel_path"]] = {
                        "mtime": it["mtime"],
                        "feat": feat,
                        "aspect_ratio": it["aspect_ratio"]
                    }
                    valid_entries.append(it)
            
            progress = min(b_idx + BATCH_SIZE, len(items_to_infer))
            print(f"[*] 추출 진행도: {progress} / {len(items_to_infer)} ({progress / len(items_to_infer) * 100:.1f}%)")

    # 캐시 파일 저장
    try:
        with open(CACHE_FILE, "wb") as f:
            pickle.dump(cache, f)
        print(f"[+] 피처 캐시 저장 완료: {CACHE_FILE}")
    except Exception as e:
        print(f"[!] 캐시 저장 실패: {e}")
else:
    print("[*] 모든 이미지가 캐시되어 있어 AI 추론을 즉시 완료했습니다.")

# -------------------------------------------------------------
# 4. PCA 차원 축소 + UMAP 3차원 배치 좌표 연산
# -------------------------------------------------------------
if not valid_entries:
    print("[!] 유효하게 처리된 이미지가 없습니다.")
    sys.exit(1)

features = np.array([e["feat"] for e in valid_entries])
n_samples = len(features)
print(f"\n[*] 3D 공간 좌표 계산 중... (총 {n_samples}개 노드)")

if n_samples >= 15:
    # PCA 선행 축소 (1280차원 -> 50차원)
    pca_dims = min(50, n_samples - 1, features.shape[1])
    pca = PCA(n_components=pca_dims, random_state=42)
    features_pca = pca.fit_transform(features)
    
    # UMAP 3D 차원 축소
    n_neighbors = min(15, n_samples - 1)
    reducer = umap.UMAP(n_components=3, random_state=42, n_neighbors=n_neighbors, min_dist=0.1)
    coords_3d = reducer.fit_transform(features_pca)
elif n_samples >= 4:
    reducer = umap.UMAP(n_components=3, random_state=42, n_neighbors=n_samples - 1, min_dist=0.1)
    coords_3d = reducer.fit_transform(features)
else:
    coords_3d = np.random.uniform(-50, 50, (n_samples, 3))

# 좌표 정규화 및 스케일링
coords_3d = (coords_3d - coords_3d.mean(axis=0)) / (coords_3d.std(axis=0) + 1e-6) * 180

output_data = []
for entry, (x, y, z) in zip(valid_entries, coords_3d):
    output_data.append({
        "filename": entry["filename"],
        "path": entry["rel_path"],
        "thumb_path": entry["thumb_path"],
        "category": entry["category"],
        "aspect_ratio": entry.get("aspect_ratio", 1.0),
        "x": round(float(x), 2),
        "y": round(float(y), 2),
        "z": round(float(z), 2)
    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"[+] 은하 데이터 생성 완료: {OUTPUT_FILE} (총 {len(output_data)}개)")

# -------------------------------------------------------------
# 5. 멀티스레드 웹 서버 시작 (포트 충돌 방지 및 브라우저 오픈)
# -------------------------------------------------------------
print("\n[단계 4/4] 멀티스레드 로컬 웹 서버 시작 및 뷰어 오픈...")

def find_available_port(start_port=8000, max_port=8020):
    for p in range(start_port, max_port):
        try:
            server = ThreadingHTTPServer(('', p), SimpleHTTPRequestHandler)
            return server, p
        except OSError:
            continue
    raise RuntimeError("사용 가능한 포트를 찾을 수 없습니다.")

httpd, PORT = find_available_port(8000)

def start_server():
    print(f"\n=======================================================")
    print(f"  🌌 Pinterest 3D Galaxy 서버 실행 중!")
    print(f"  👉 접속 주소: http://localhost:{PORT}/index.html")
    print(f"  👉 종료 방법: 터미널에서 Ctrl + C")
    print(f"=======================================================\n")
    httpd.serve_forever()

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

time.sleep(1)
webbrowser.open(f"http://localhost:{PORT}/index.html")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[*] 서버를 정상 종료합니다.")