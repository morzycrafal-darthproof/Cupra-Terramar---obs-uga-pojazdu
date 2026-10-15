"""Builds desktop/assets/ from the source logo (copper on white).

    py tools/make_assets.py <logo.png>

Outputs:
    assets/emblem.png     emblem only, transparent background, app copper colour
    assets/wordmark.png   "CUPRA" lettering, transparent background
    assets/app.ico        window / taskbar icon (emblem on a dark rounded tile)
    assets/app_icon.png   the same icon as PNG (window icon outside Windows)
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent.parent
ASSETS = HERE / "assets"
COPPER = (201, 106, 52)  # C["copper"]
TILE = (26, 22, 19)      # C["surface"]


def recolor(img):
    """Keep the logo's shape (alpha) and paint it in the app's copper."""
    if img.mode != "RGBA":  # opaque source: derive alpha from darkness on white
        gray = img.convert("L")
        alpha = gray.point(lambda v: max(0, min(255, int((255 - v) * 255 / (255 - 90)))))
    else:
        alpha = img.getchannel("A")
    out = Image.new("RGBA", img.size, COPPER + (0,))
    out.putalpha(alpha)
    return out


def split_rows(alpha):
    """Return (top, bottom) row bands that contain ink, separated by empty rows."""
    w, h = alpha.size
    px = alpha.load()
    inked = [any(px[x, y] > 8 for x in range(0, w, 2)) for y in range(h)]
    bands, start = [], None
    for y, on in enumerate(inked + [False]):
        if on and start is None:
            start = y
        elif not on and start is not None:
            bands.append((start, y))
            start = None
    return bands


def crop_to_ink(img):
    return img.crop(img.getchannel("A").getbbox())


def main(src):
    ASSETS.mkdir(exist_ok=True)
    logo = recolor(Image.open(src))
    bands = split_rows(logo.getchannel("A"))
    # the emblem is the tallest band, the wordmark the band below it
    emblem_band = max(bands, key=lambda b: b[1] - b[0])
    word_band = next(b for b in bands if b[0] > emblem_band[1])
    emblem = crop_to_ink(logo.crop((0, emblem_band[0], logo.width, emblem_band[1])))
    word = crop_to_ink(logo.crop((0, word_band[0], logo.width, word_band[1])))
    emblem.save(ASSETS / "emblem.png")
    word.save(ASSETS / "wordmark.png")

    # icon: emblem centred on a dark rounded tile with margin for small sizes
    size = 256
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(tile).rounded_rectangle((0, 0, size - 1, size - 1), radius=56, fill=TILE + (255,))
    e = emblem.copy()
    e.thumbnail((int(size * 0.72), int(size * 0.72)), Image.LANCZOS)
    tile.alpha_composite(e, ((size - e.width) // 2, (size - e.height) // 2 + 6))
    tile.save(ASSETS / "app.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    tile.save(ASSETS / "app_icon.png")
    print("emblem", emblem.size, "wordmark", word.size)


if __name__ == "__main__":
    main(sys.argv[1])
