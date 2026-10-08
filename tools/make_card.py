"""印刷用カード（マーカー画像 + QRコード）を作るスクリプト。

使い方: python tools/make_card.py [公開URL]
出力:  targets/card.png（印刷用・マーカー兼用）
       targets/qr.png（QRコード単体）
"""
import io
import random
import sys
from pathlib import Path

import segno
from PIL import Image, ImageDraw, ImageFont

URL = sys.argv[1] if len(sys.argv) > 1 else "https://okazakiy84-bit.github.io/ar-avatar/"
OUT = Path(__file__).resolve().parent.parent / "targets"
W, H = 1000, 1400
PALETTE = ["#0a66ff", "#ff4d6d", "#ffb703", "#2ec4b6", "#8338ec", "#1d1d1f", "#fb5607"]


def load_font(size):
    for name in ["DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def draw_pattern(draw, box, rng):
    # 画像認識しやすいよう、大きさ・形・色がばらばらの図形を重ねる（繰り返し模様は認識しにくい）
    x0, y0, x1, y1 = box
    for _ in range(140):
        cx, cy = rng.uniform(x0, x1), rng.uniform(y0, y1)
        r = rng.uniform(12, 90)
        color = rng.choice(PALETTE)
        kind = rng.random()
        if kind < 0.35:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color, outline="#000", width=4)
        elif kind < 0.7:
            pts = [(cx + rng.uniform(-r, r), cy + rng.uniform(-r, r)) for _ in range(3)]
            draw.polygon(pts, fill=color, outline="#000")
        else:
            draw.rectangle([cx - r, cy - r / 2, cx + r, cy + r / 2], fill=color, outline="#000", width=4)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(42)
    card = Image.new("RGB", (W, H), "#ffffff")
    draw = ImageDraw.Draw(card)

    # 枠からはみ出さないよう、別キャンバスに描いてから貼り付ける
    art = Image.new("RGB", (W - 80, 940), "#ffffff")
    draw_pattern(ImageDraw.Draw(art), (0, 0, art.width, art.height), rng)
    card.paste(art, (40, 40))
    draw.rectangle([20, 20, W - 21, H - 21], outline="#000", width=12)

    draw.text((60, 1030), "AR AVATAR", font=load_font(72), fill="#1d1d1f")
    draw.text((60, 1150), "1. Scan QR code", font=load_font(40), fill="#1d1d1f")
    draw.text((60, 1210), "2. Point camera at", font=load_font(40), fill="#1d1d1f")
    draw.text((60, 1260), "   this card", font=load_font(40), fill="#1d1d1f")

    buf = io.BytesIO()
    segno.make(URL, error="m").save(buf, kind="png", scale=8, border=2)
    qr = Image.open(buf).convert("RGB")
    qr.save(OUT / "qr.png")
    qr = qr.resize((330, 330), Image.NEAREST)
    card.paste(qr, (W - 330 - 50, H - 330 - 50))

    card.save(OUT / "card.png")
    print(f"QR: {URL}\nsaved: {OUT / 'card.png'}")


if __name__ == "__main__":
    main()
