#!/usr/bin/env python3
"""生成 Edge 商店素材：logo 300×300、小宣传图 440×280、大宣传图 1400×560。

输入使用仓库内的 icons/icon128.png，保持与扩展图标一致。
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "icons" / "icon128.png"
OUT = ROOT / "store-assets"
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
FONT_REG = Path(r"C:\Windows\Fonts\msyh.ttc")

BLUE_TOP = (17, 65, 144)
BLUE_BOTTOM = (28, 96, 185)
LIGHT = (205, 220, 238)
WHITE = (255, 255, 255)


def gradient(size: tuple[int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGBA", size)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        color = tuple(round(BLUE_TOP[i] + (BLUE_BOTTOM[i] - BLUE_TOP[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = (*color, 255)
    return img


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.is_file():
        raise SystemExit(f"字体不存在：{path}")
    return ImageFont.truetype(str(path), size)


def logo_300() -> None:
    icon = Image.open(ICON).convert("RGBA").resize((300, 300), Image.LANCZOS)
    icon.save(OUT / "logo-300.png")


def small_tile() -> None:
    w, h = 440, 280
    img = gradient((w, h))
    icon = Image.open(ICON).convert("RGBA").resize((120, 120), Image.LANCZOS)
    img.alpha_composite(icon, (28, 80))
    d = ImageDraw.Draw(img)
    d.text((174, 92), "团务助手", font=font(FONT_BOLD, 42), fill=WHITE)
    d.text((176, 154), "团员信息管理", font=font(FONT_REG, 18), fill=LIGHT)
    d.text((176, 188), "名单 · 评议 · 录入", font=font(FONT_REG, 15), fill=LIGHT)
    img.convert("RGB").save(OUT / "small-promotional-tile-440x280.png")


def large_tile() -> None:
    w, h = 1400, 560
    img = gradient((w, h))
    icon = Image.open(ICON).convert("RGBA").resize((300, 300), Image.LANCZOS)
    img.alpha_composite(icon, (80, 130))
    d = ImageDraw.Draw(img)
    d.text((430, 160), "团务助手", font=font(FONT_BOLD, 96), fill=WHITE)
    d.text((434, 292), "团员信息管理 · 教育评议 · 批量录入", font=font(FONT_REG, 34), fill=LIGHT)
    d.text((434, 368), "本地处理 · 数据不上传 · 确认后提交", font=font(FONT_REG, 26), fill=LIGHT)
    img.convert("RGB").save(OUT / "large-promotional-tile-1400x560.png")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    OUT.mkdir(exist_ok=True)
    logo_300()
    small_tile()
    large_tile()
    for p in sorted(OUT.glob("*.png")):
        with Image.open(p) as im:
            print(f"[ok] {p.name} {im.size} {p.stat().st_size} B")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
