from __future__ import annotations

import re
import shutil
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any


_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')


def normalize_one_line(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def sanitize_filename(title: str, *, max_len: int = 120) -> str:
    cleaned = _INVALID_FILENAME_CHARS.sub("-", (title or "").strip())
    cleaned = re.sub(r"-{2,}", "-", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip().rstrip(".")
    if not cleaned:
        cleaned = "Untitled"
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len].rstrip()
    return cleaned


def _escape_markdown_label(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )


def _looks_remote(target: str) -> bool:
    return bool(re.match(r"^https?://", target, flags=re.IGNORECASE))


def _stringify_target(value: Any) -> str:
    return normalize_one_line(str(value or ""))


def _source_url_from_image(image: Any) -> tuple[str, str, str]:
    if isinstance(image, str):
        target = _stringify_target(image)
        if not target:
            return "", "", "Image"
        if _looks_remote(target):
            return "", target, "Image"
        return target, "", Path(target).stem or "Image"

    if not isinstance(image, Mapping):
        return "", "", "Image"

    local_target = _stringify_target(
        image.get("path")
        or image.get("local_path")
        or image.get("file")
        or image.get("target")
    )
    remote_target = _stringify_target(
        image.get("data_src")
        or image.get("data-src")
        or image.get("url")
        or image.get("source_url")
        or image.get("image_url")
    )
    label = _stringify_target(image.get("alt") or image.get("title") or Path(local_target or remote_target).stem)
    return local_target, remote_target, label or "Image"


def _unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for idx in range(1, 1000):
        candidate = path.with_name(f"{stem}-{idx}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Unable to find free filename for {path}")


def download_remote_image(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response, destination.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def render_image_markdown(
    image: Any,
    *,
    vault_root: str | Path,
    note_title: str,
    download_image: Callable[[str, Path], None] | None = None,
) -> str | None:
    local_target, remote_target, label = _source_url_from_image(image)
    vault_root = Path(vault_root)
    note_dir = sanitize_filename(note_title)
    asset_dir = vault_root / "assets" / note_dir

    if local_target:
        source_path = Path(local_target).expanduser()
        if source_path.exists() and source_path.is_file():
            destination = _unique_path(asset_dir / source_path.name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination)
            rel_path = destination.relative_to(vault_root).as_posix()
            return f"![{_escape_markdown_label(label)}]({rel_path})"
        if _looks_remote(local_target):
            remote_target = local_target
        else:
            rel_path = Path(local_target).as_posix()
            return f"![{_escape_markdown_label(label)}]({rel_path})"

    if remote_target:
        filename = Path(urllib.parse.urlparse(remote_target).path).name or "image"
        if not Path(filename).suffix:
            filename = f"{Path(filename).stem or 'image'}.png"
        destination = _unique_path(asset_dir / filename)
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            (download_image or download_remote_image)(remote_target, destination)
        except Exception:
            if destination.exists():
                try:
                    destination.unlink()
                except OSError:
                    pass
            for candidate in (destination.parent, asset_dir.parent):
                try:
                    if candidate.exists() and candidate.is_dir() and not any(candidate.iterdir()):
                        candidate.rmdir()
                except OSError:
                    pass
            return f"![{_escape_markdown_label(label)}](<{remote_target}>)"
        rel_path = destination.relative_to(vault_root).as_posix()
        return f"![{_escape_markdown_label(label)}]({rel_path})"

    return None
