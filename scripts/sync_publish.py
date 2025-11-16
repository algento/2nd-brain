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
      ![Title|center|700](image.png)

    변환 결과(Quartz에서 쓰일 HTML):

      <p class="img-center">
        <img src="image.png"
             alt="Title"
             style="max-width:700px; width:100%;">
      </p>

    - | 뒤의 토큰 중:
      * 숫자만 있는 건 width(px)로
      * center/left/right 는 정렬 정보로 사용
    """

    def _replace(m: re.Match) -> str:
        raw_alt = m.group(1)  # "Title|center|700"
        path = m.group(2).strip()  # "image.png" 같은 부분 (원본 그대로 유지)

        # alt / 옵션 분해
        parts = [p.strip() for p in raw_alt.split("|")] if raw_alt else []
        alt = parts[0] if parts else ""

        align = None  # 'center', 'left', 'right' 중 하나
        width = None  # 숫자(px)

        for p in parts[1:]:
            low = p.lower()
            if low in ("center", "left", "right"):
                align = low
            elif p.isdigit():
                width = int(p)

        # <img> 태그 구성
        style_parts = []
        if width is not None:
            style_parts.append(f"max-width:{width}px")
            style_parts.append("width:100%")
        style_attr = ""
        if style_parts:
            style_attr = f' style="{"; ".join(style_parts)}"'

        img_html = f'<img src="{path}" alt="{alt}"{style_attr}>'

        # 정렬에 따라 감싸는 태그 결정
        if align == "center":
            # 중앙 정렬용 래퍼
            return f'<p class="img-center">\n  {img_html}\n</p>'
        elif align in ("left", "right"):
            # 필요하면 나중에 CSS로 제어 가능
            return f'<p class="img-{align}">\n  {img_html}\n</p>'
        else:
            # 정렬 정보 없으면 그냥 img만
            return img_html

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
            # 변환된 텍스트에서 이미지 파일명 수집
            original = src.read_text(encoding="utf-8")
            imgs = collect_images_from_text(original)
            if imgs:
                log(f"[{rel}] 이미지 참조: {', '.join(sorted(imgs))}")
            used_filenames |= imgs

            # 마크다운: 내용 읽고, 이미지 문법 변환 후 저장
            converted = convert_obsidian_image_syntax(original)

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
