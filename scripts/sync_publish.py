#!/usr/bin/env python3
import re
import shutil
import sys
from pathlib import Path

VAULT_ROOT = Path("~/Github/docs/obsidian-sync").expanduser()
QUARTZ_ROOT = Path("~/Github/docs/quartz").expanduser()
PUBLISH_DIR = VAULT_ROOT / "Publish"
ATTACH_DIR = VAULT_ROOT / "Attachments"
CONTENT_DIR = QUARTZ_ROOT / "content"
OUT_ATTACH_DIR = CONTENT_DIR / "Attachments"
MD_IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def log(msg: str):
    print(msg, file=sys.stderr)


def convert_obsidian_image_syntax(text: str) -> str:
    """
    옵시디언 스타일:
      ![Title|center|700](20251110-201618.png)
    -> Quartz/Markdown 스타일:
      ![Title](20251110-201618.png){ width=700 .center }
    """

    def _replace(m: re.Match) -> str:
        raw_alt = m.group(1)  # "Title|center|700"
        path = m.group(2).strip()

        # alt 파싱: "제목|center|700" 형태
        parts = [p.strip() for p in raw_alt.split("|")]

        alt = parts[0] if parts else ""
        align = None
        width = None

        for p in parts[1:]:
            low = p.lower()
            if low in ("center", "left", "right"):
                align = low
            elif p.isdigit():
                width = int(p)

        # 기본 Markdown
        base = f"![{alt}]({path})"

        # 속성(Pandoc-style attribute)
        attrs = []
        if width is not None:
            attrs.append(f"width={width}")
        if align == "center":
            attrs.append(".center")
        # left/right도 필요하면 여기서 클래스 추가 가능

        if attrs:
            return f"{base}{{ {' '.join(attrs)} }}"
        else:
            return base

    return MD_IMAGE_PATTERN.sub(_replace, text)


def collect_images_from_text(text: str) -> set[str]:
    found: set[str] = set()

    # ![alt](path) 패턴에서 path만 추출
    for m in MD_IMAGE_PATTERN.finditer(text):
        raw_path = m.group(2).strip()  # "20251110-201618.png" 같은 부분

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

    # 2) Publish 아래 파일을 하나씩 처리
    used_filenames: set[str] = set()

    for src in PUBLISH_DIR.rglob("*"):
        rel = src.relative_to(PUBLISH_DIR)
        dst = CONTENT_DIR / rel

        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
            continue

        if src.suffix.lower() == ".md":
            # 마크다운: 내용 읽고, 이미지 문법 변환 후 저장
            text = src.read_text(encoding="utf-8")
            converted = convert_obsidian_image_syntax(text)

            # 변환된 텍스트에서 이미지 파일명 수집
            imgs = collect_images_from_text(converted)
            if imgs:
                log(f"[{rel}] 이미지 참조: {', '.join(sorted(imgs))}")
            used_filenames |= imgs

            dst.write_text(converted, encoding="utf-8")
        else:
            # 기타 파일(pdf 등)은 그대로 복사
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

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
