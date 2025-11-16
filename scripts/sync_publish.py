#!/usr/bin/env python3
import re
import shutil
import sys
from pathlib import Path

# Obsidian 볼트 루트
VAULT_ROOT = Path("~/Github/docs/obsidian-sync").expanduser()

# Quartz 루트
QUARTZ_ROOT = Path("~/Github/docs/quartz").expanduser()

# 공개용 문서 폴더
PUBLISH_DIR = VAULT_ROOT / "Publish"

# 모든 첨부 이미지가 모여 있는 폴더
ATTACH_DIR = VAULT_ROOT / "Attachments"

# Quartz content 폴더
CONTENT_DIR = QUARTZ_ROOT / "content"

# Quartz에서 이미지가 위치할 폴더
OUT_ATTACH_DIR = CONTENT_DIR / "Attachments"

# ====== 여기부터는 그대로 써도 됨 ======
# 예: ![Metric of Self-Driving Simulation|center|700](20251110-201618.png)
MD_IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def log(msg: str):
    print(msg, file=sys.stderr)


def collect_images_from_text(text: str) -> set[str]:
    found: set[str] = set()

    # ![alt](path) 패턴에서 path만 추출
    for m in MD_IMAGE_PATTERN.finditer(text):
        raw_path = m.group(1).strip()  # "20251110-201618.png" 같은 부분

        # 웹 URL은 무시
        if raw_path.startswith("http://") or raw_path.startswith("https://"):
            continue

        # 쿼리스트링 제거 (혹시 모를 경우)
        raw_path = raw_path.split("?", 1)[0]

        # 마지막 컴포넌트만 파일명으로 사용
        name = Path(raw_path).name
        if name:
            found.add(name)

    return found


def find_in_attachments(filename: str) -> Path | None:
    """Attachments 디렉토리(하위 포함)에서 파일명을 검색."""
    for p in ATTACH_DIR.rglob(filename):
        if p.is_file():
            return p
    return None


def sync_publish_to_quartz():
    if not PUBLISH_DIR.exists():
        raise SystemExit(f"Publish 디렉토리를 찾을 수 없음: {PUBLISH_DIR}")

    log(f"Vault root: {VAULT_ROOT}")
    log(f"Quartz root: {QUARTZ_ROOT}")
    log(f"Publish dir: {PUBLISH_DIR}")
    log(f"Attachments dir: {ATTACH_DIR}")
    log(f"Quartz content dir: {CONTENT_DIR}")

    # 1) content 비우고 Publish 전체 복사
    if CONTENT_DIR.exists():
        log(f"기존 content 제거: {CONTENT_DIR}")
        shutil.rmtree(CONTENT_DIR)

    log("Publish -> content 복사")
    shutil.copytree(PUBLISH_DIR, CONTENT_DIR)

    # 2) content 아래 모든 .md에서 사용된 이미지 파일명 수집
    used_filenames: set[str] = set()

    for md_path in CONTENT_DIR.rglob("*.md"):
        text = md_path.read_text(encoding="utf-8")
        imgs = collect_images_from_text(text)
        if imgs:
            rel = md_path.relative_to(CONTENT_DIR)
            log(f"[{rel}] 이미지 참조: {', '.join(sorted(imgs))}")
        used_filenames |= imgs

    log(f"총 참조된 이미지 파일 수: {len(used_filenames)}")

    # 3) content/Attachments 폴더 초기화
    if OUT_ATTACH_DIR.exists():
        shutil.rmtree(OUT_ATTACH_DIR)
    OUT_ATTACH_DIR.mkdir(parents=True, exist_ok=True)

    # 4) 실제 사용된 이미지 파일만 Attachments에서 찾아 복사
    missing: list[str] = []

    for filename in sorted(used_filenames):
        src = find_in_attachments(filename)
        if not src:
            log(f"⚠ Attachments에서 찾을 수 없는 파일: {filename}")
            missing.append(filename)
            continue

        dst = OUT_ATTACH_DIR / src.name
        shutil.copy2(src, dst)
        log(f"복사: {src.relative_to(VAULT_ROOT)} -> {dst.relative_to(QUARTZ_ROOT)}")

    if missing:
        log("\n다음 파일은 Attachments에서 찾지 못했습니다:")
        for name in missing:
            log(f"  - {name}")


if __name__ == "__main__":
    sync_publish_to_quartz()
