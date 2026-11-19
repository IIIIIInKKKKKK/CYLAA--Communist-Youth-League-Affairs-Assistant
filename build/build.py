#!/usr/bin/env python3
"""构建 GitHub / Edge 两个互相隔离的发布包。

用法：
    python build/build.py --target edge
    python build/build.py --target github
    python build/build.py --target all --node "C:/.../node.exe"

Edge 包会被强制检查：
- manifest.json 在 zip 根目录；
- permissions 只有 storage，host_permissions 只有 zhtj；
- 不包含 update.js / version.json；
- 全包不出现 github / jsdelivr / gitee / releases / version.json 字样；
- 图标尺寸与 manifest 一致；
- JS 通过 node --check。

任何一项不通过都会以非 0 退出，不会产出 zip。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDGE_MANIFEST_TEMPLATE = ROOT / "build" / "manifest.edge.json"
EDGE_VERSION_FILE = ROOT / "edge" / "VERSION"
FORBIDDEN = re.compile(r"github|jsdelivr|gitee|releases|version\.json|update\.js", re.I)
VERSION_RE = re.compile(r"^\d+(\.\d+){0,3}$")
TARGETS = ("edge", "github")


class BuildError(RuntimeError):
    pass


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(msg: str) -> None:
    raise BuildError(msg)


def copy_icons(manifest: dict, dist: Path) -> None:
    icons = manifest.get("icons") or {}
    if not icons:
        fail("manifest 没有 icons")
    for size, rel in icons.items():
        src = ROOT / rel
        if not src.is_file():
            fail(f"图标不存在：{rel}")
        dst = dist / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        from PIL import Image

        with Image.open(dst) as im:
            if im.size != (int(size), int(size)):
                fail(f"图标 {rel} 尺寸 {im.size}，应为 {(int(size), int(size))}")


def check_forbidden(dist: Path) -> None:
    for p in dist.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".js", ".json", ".html", ".css", ".txt", ".md"}:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        m = FORBIDDEN.search(text)
        if m:
            fail(f"Edge 包出现禁止字样：{p.relative_to(dist)} -> {m.group(0)}")


def node_check(files: list[Path], node: str | None) -> None:
    if not node:
        print("[warn] 未指定 --node，跳过 JS 语法检查")
        return
    for f in files:
        subprocess.run([node, "--check", str(f)], check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build(target: str, out_root: Path, node: str | None) -> Path:
    if target not in TARGETS:
        fail(f"未知 target：{target}")

    if target == "edge":
        version = EDGE_VERSION_FILE.read_text(encoding="utf-8").strip()
        manifest = read_json(EDGE_MANIFEST_TEMPLATE)
        manifest["version"] = version
    else:
        manifest = read_json(ROOT / "manifest.json")
        version = str(manifest["version"])

    if not VERSION_RE.fullmatch(version):
        fail(f"版本号格式不合法：{version}")

    out_root = out_root.resolve()
    dist = out_root / target
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir(parents=True)

    content = (ROOT / "content.js").read_text(encoding="utf-8")
    if target == "edge":
        content, count = re.subn(r"const HAS_UPDATER = true;", "const HAS_UPDATER = false;", content)
        if count != 1:
            fail("未能在 content.js 中唯一定位 HAS_UPDATER 开关")
        js_files = ["content.js"]
    else:
        update_js = ROOT / "update.js"
        if not update_js.is_file():
            fail("GitHub 版缺少 update.js")
        shutil.copy2(update_js, dist / "update.js")
        js_files = ["content.js", "update.js"]
        js = manifest.get("content_scripts", [{}])[0].get("js", [])
        if "update.js" not in js:
            fail("GitHub manifest 的 content_scripts 未包含 update.js")

    (dist / "content.js").write_text(content, encoding="utf-8", newline="\n")
    copy_icons(manifest, dist)
    (dist / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    # ---- 隔离校验 ----
    if target == "edge":
        if manifest.get("permissions") != ["storage"]:
            fail(f"Edge permissions 不是 ['storage']：{manifest.get('permissions')}")
        if manifest.get("host_permissions") != ["https://zhtj.youth.cn/*"]:
            fail(f"Edge host_permissions 不是仅 zhtj：{manifest.get('host_permissions')}")
        if manifest["content_scripts"][0].get("js") != ["content.js"]:
            fail("Edge content_scripts 不应包含 update.js")
        if (dist / "update.js").exists() or (dist / "version.json").exists():
            fail("Edge 包不应包含 update.js / version.json")
        expected = {"manifest.json", "content.js", *manifest["icons"].values()}
        actual = {p.relative_to(dist).as_posix() for p in dist.rglob("*") if p.is_file()}
        if actual != expected:
            fail(f"Edge 包文件不符合预期：多出 {actual - expected}，缺少 {expected - actual}")
        check_forbidden(dist)

    node_check([dist / name for name in js_files], node)

    zip_path = out_root / f"CYLAA-{target}-{version}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(dist.rglob("*")):
            if p.is_file():
                zf.write(p, p.relative_to(dist).as_posix())

    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if "manifest.json" not in names:
            fail(f"{zip_path.name} 根目录没有 manifest.json")
        if any(n.startswith("/") or ".." in n.split("/") for n in names):
            fail(f"{zip_path.name} 含不安全路径")

    size_kb = zip_path.stat().st_size / 1024
    print(f"[ok] {target:6s} v{version}  {zip_path}  ({size_kb:.1f} KB)")
    for p in sorted(dist.rglob("*")):
        if p.is_file():
            print(f"       {p.relative_to(dist).as_posix():24s} {p.stat().st_size:>7d} B")
    print(f"       sha256 {sha256(zip_path)}")
    return zip_path


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=[*TARGETS, "all"], required=True)
    parser.add_argument("--out", default=str(ROOT / "dist"))
    parser.add_argument("--node", default=None, help="node 可执行文件路径，用于语法检查")
    args = parser.parse_args()

    out_root = Path(args.out).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    targets = TARGETS if args.target == "all" else (args.target,)
    for t in targets:
        build(t, out_root, args.node)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        print(f"[fail] {exc}", file=sys.stderr)
        raise SystemExit(1)
