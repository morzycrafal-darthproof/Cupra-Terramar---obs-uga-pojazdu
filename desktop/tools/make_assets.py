"""Builds the app graphics for both apps.

    py desktop/tools/make_assets.py <flat-logo.png> <emblem-3d.png> <background.jpg>

    flat-logo.png    flat CUPRA logo (emblem + lettering), transparent or on white — gives the sidebar lettering
    emblem-3d.png    3D copper emblem on a transparent background (Cupra_vortex.png)
    background.jpg   square artwork: the 3D emblem on brushed metal (the launcher icon, "variant C")

Outputs (desktop):
    desktop/assets/emblem.png     3D emblem for the sidebar
    desktop/assets/wordmark.png   "CUPRA" lettering, app copper colour
    desktop/assets/app.ico        16-48 px: emblem on the app's dark background ("variant A");
                                  64-256 px: the brushed-metal artwork
    desktop/assets/app_icon.png   brushed-metal artwork (window icon outside Windows)
Outputs (web app, repo root):
    icon-192.png, icon-512.png    home-screen icons (maskable: full-bleed artwork)
    apple-touch-icon.png          180 px, iOS home screen
    favicon-16.png, favicon-32.png  browser tab ("variant A")
    emblem.png                    3D emblem for the app header
"""
import io
import struct
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent.parent
ASSETS = HERE / "assets"
REPO = HERE.parent
COPPER = (201, 106, 52)  # C["copper"]
BG = (15, 13, 12)        # C["bg"], also the PWA theme colour


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


def ink_bands(alpha):
    """Row bands that contain ink, separated by empty rows."""
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


def wordmark_from(flat_logo):
    logo = recolor(Image.open(flat_logo))
    bands = ink_bands(logo.getchannel("A"))
    emblem_band = max(bands, key=lambda b: b[1] - b[0])  # the emblem is the tallest band, the lettering below it
    word_band = next(b for b in bands if b[0] > emblem_band[1])
    return crop_to_ink(logo.crop((0, word_band[0], logo.width, word_band[1])))


def small_icon(emblem, size):
    """Variant A: the emblem on the app's dark background, rounded tile, readable at 16-48 px."""
    s = size * 4
    tile = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(tile).rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * 0.22), fill=BG + (255,))
    e = emblem.copy()
    e.thumbnail((int(s * 0.80), int(s * 0.80)), Image.LANCZOS)
    tile.alpha_composite(e, ((s - e.width) // 2, (s - e.height) // 2 + s // 40))
    return tile.resize((size, size), Image.LANCZOS)


def write_ico(path, images):
    """ICO with a different picture per size (PNG-compressed entries)."""
    entries = []
    for im in images:
        buf = io.BytesIO()
        im.save(buf, "PNG")
        entries.append((im.width, im.height, buf.getvalue()))
    offset = 6 + 16 * len(entries)
    header = struct.pack("<HHH", 0, 1, len(entries))
    table, blobs = b"", b""
    for w, h, data in entries:
        table += struct.pack("<BBBBHHII", w % 256, h % 256, 0, 0, 1, 32, len(data), offset + len(blobs))
        blobs += data
    path.write_bytes(header + table + blobs)


def main(flat_logo, emblem_3d, background):
    ASSETS.mkdir(exist_ok=True)
    emblem = crop_to_ink(Image.open(emblem_3d).convert("RGBA"))
    art = Image.open(background).convert("RGBA")
    side = min(art.size)
    art = art.crop(((art.width - side) // 2, (art.height - side) // 2,
                    (art.width + side) // 2, (art.height + side) // 2))
    big = lambda size: art.resize((size, size), Image.LANCZOS)

    # desktop
    sidebar = emblem.copy()
    sidebar.thumbnail((10_000, 160), Image.LANCZOS)  # shown 40 px high, sharp at 300% scaling
    sidebar.save(ASSETS / "emblem.png", optimize=True)
    wordmark_from(flat_logo).save(ASSETS / "wordmark.png")
    write_ico(ASSETS / "app.ico", [small_icon(emblem, s) for s in (16, 20, 24, 32, 40, 48)] +
              [big(s) for s in (64, 128, 256)])
    big(256).save(ASSETS / "app_icon.png", optimize=True)

    # web app
    for size in (192, 512):
        big(size).convert("RGB").save(REPO / f"icon-{size}.png", optimize=True)
    big(180).convert("RGB").save(REPO / "apple-touch-icon.png", optimize=True)
    for size in (16, 32):
        small_icon(emblem, size).save(REPO / f"favicon-{size}.png", optimize=True)
    header = emblem.copy()
    header.thumbnail((10_000, 96), Image.LANCZOS)  # shown 30 px high, sharp up to 3x displays
    header.save(REPO / "emblem.png", optimize=True)
    print("emblem", emblem.size, "| artwork", art.size)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
