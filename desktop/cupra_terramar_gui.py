#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cupra Terramar — Dziennik pokładowy (wersja desktopowa)
=========================================================
Aplikacja okienkowa (CustomTkinter) do monitorowania tankowań, serwisów
i kosztów samochodu. Dane zapisują się automatycznie w pliku JSON
w katalogu domowym użytkownika.

Uruchomienie:
    py cupra_terramar_gui.py

Wymagania:
    pip install -r requirements.txt   (customtkinter, matplotlib, pillow)
    (tkinter jest częścią standardowej biblioteki Pythona; na Linuksie
     czasem trzeba go doinstalować osobno, np. `sudo apt install python3-tk`)
"""

import json
import math
import os
import uuid
import datetime as dt
import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------------------------------------------------------------
# THEME
# ----------------------------------------------------------------------
C = {
    "bg": "#0F0D0C",
    "sidebar": "#141110",
    "surface": "#1A1613",
    "surface2": "#221D19",
    "surface3": "#2B241F",
    "line": "#332C26",
    "copper": "#C96A34",
    "copper_hover": "#DD7A3F",
    "copper_dim": "#8A5330",
    "copper_soft": "#2E1E15",
    "amber": "#D9A438",
    "amber_soft": "#30271A",
    "green": "#5FAE7C",
    "green_soft": "#1B2B21",
    "red": "#C4483C",
    "red_soft": "#33191A",
    "text": "#F3EEE7",
    "text_dim": "#9C948B",
    "text_faint": "#665F58",
}
SOFT = {C["green"]: C["green_soft"], C["amber"]: C["amber_soft"], C["red"]: C["red_soft"],
        C["copper"]: C["copper_soft"], C["text_dim"]: C["surface2"]}

ASSET_DIR = Path(__file__).resolve().parent / "assets"
WIN_FONTS = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"

# ----------------------------------------------------------------------
# DATA FILE + SEED DATA (imported from CupraTerramar.xlsx)
# ----------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.expanduser("~"), ".cupra_terramar")
DATA_FILE = os.path.join(DATA_DIR, "data.json")

_RAW_TANKOWANIA = [
    ("2026-01-17", "Pb95", 44.00, 236.71, 6715, None),
    ("2026-01-23", "Pb98", 55.00, 336.92, 7305, 590),
    ("2026-01-30", "Pb98", 52.00, 322.77, 8055, 750),
    ("2026-02-06", "Pb98", 55.00, 337.57, 8805, 750),
    ("2026-02-14", "Pb98", 53.00, 329.02, 9409, 604),
    ("2026-02-19", "Pb98", 53.00, 340.84, 10043, 634),
    ("2026-02-27", "Pb98", 55.00, 357.92, 10725, 682),
    ("2026-03-06", "Pb98", 55.00, 403.73, 11410, 685),
    ("2026-03-11", "Pb98", 50.00, 358.79, 12030, 620),
    ("2026-03-19", "Pb95", 55.00, 382.19, 12709, 679),
    ("2026-04-24", "Pb98", 49.00, 296.48, 13107, 398),
    ("2026-05-09", "Pb98", 51.00, 340.72, 13626, 519),
    ("2026-05-24", "Pb98", 53.00, 360.40, 14182, 556),
    ("2026-06-07", "Pb98", 50.00, 325.01, 14687, 505),
    ("2026-06-21", "Pb98", 54.83, 352.43, 15230, 543),
    ("2026-06-29", "Pb98", 55.76, 373.59, 15848, 618),
    ("2026-07-08", "Pb98", 51.26, 395.21, 16444, 596),
    ("2026-07-14", "Pb98", 52.40, 399.80, 17093, 649),
    ("2026-07-21", "Pb98", 46.98, 389.46, 17675, 582),
    ("2026-07-23", "Pb98", 49.75, 392.03, 18226, 551),
    ("2026-08-02", "Pb98", 52.29, 426.69, 18807, 581),
    ("2026-08-09", "Pb98", 47.53, 377.39, 19386, 579),
    ("2026-08-17", "Pb98", 53.83, 387.43, 20016, 630),
    ("2026-08-26", "Pb98", 49.09, 362.82, 20609, 593),
    ("2026-09-13", "Pb98", 47.63, 421.05, 21063, 454),
    ("2026-09-22", "Pb98", 51.58, 455.98, 21680, 617),
    ("2026-10-02", "Pb98", 51.34, 451.55, 22280, 600),
    ("2026-10-10", "Pb98", 53.97, 408.66, 22880, 600),
]


def _seed_tankowania():
    out = []
    for i, (date, fuel, liters, cost, mileage, distance) in enumerate(_RAW_TANKOWANIA):
        consumption = round((liters / distance) * 100, 2) if distance else None
        out.append({
            "id": f"seed-t-{i}", "date": date, "fuelType": fuel, "liters": liters,
            "cost": cost, "pricePerL": round(cost / liters, 3), "mileage": mileage,
            "distance": distance, "consumption": consumption, "note": "",
        })
    return out


def _seed_serwisy():
    return [
        {"id": "seed-s-0", "date": "2026-01-19", "mileage": 6992, "description": "Olej + filtr",
         "price": 0, "warranty": True, "paidCost": 0, "note": "W cenie zakupu auta"},
        {"id": "seed-s-1", "date": "2026-04-28", "mileage": 13150, "description": "Wymiana opon",
         "price": 250, "warranty": False, "paidCost": 250, "note": ""},
        {"id": "seed-s-2", "date": "2026-08-11", "mileage": 19531,
         "description": "Olej + filtr oleju + filtr powietrza + filtr kabinowy + śruba spustu oleju",
         "price": 932.5, "warranty": False, "paidCost": 932.5, "note": "Serwis w Bosh Dunst Kartuzy"},
    ]


def _seed_koszty():
    return [
        {"id": "seed-k-0", "date": "2026-01-14", "type": "Zakup auta", "description": "Cena zakupu auta",
         "amount": 189500, "note": "Przebieg: 6715 km"},
        {"id": "seed-k-1", "date": "2026-01-16", "type": "Ubezpieczenie", "description": "Polisa OC/AC",
         "amount": 3693, "note": ""},
        {"id": "seed-k-2", "date": "2026-01-16", "type": "Akcesoria", "description": "Kamera + karta SD",
         "amount": 640.99, "note": ""},
        {"id": "seed-k-3", "date": "2026-04-28", "type": "Opony", "description": "Wulkanizacja: przełożenie opon",
         "amount": 250, "note": ""},
    ]


DEFAULT_SETTINGS = {
    "consumptionOkTo": 8.5,
    "consumptionHighFrom": 10.0,
    "fuelPriceGrowth": 0.05,
    "monthlyKmPlan": 1500,
    "carPrice": 189500,
    "carName": "CUPRA TERRAMAR",
    "carSubtitle": "DZIENNIK POKŁADOWY",
}

FUEL_TYPES = ["Pb95", "Pb98", "E10", "Inne"]
KOSZTY_TYPES = ["Zakup auta", "Ubezpieczenie", "Serwis", "Opony", "Myjnia", "Akcesoria", "Parking", "Inne"]


def seed_data():
    return {
        "tankowania": _seed_tankowania(),
        "serwisy": _seed_serwisy(),
        "koszty": _seed_koszty(),
        "settings": dict(DEFAULT_SETTINGS),
    }


def sanitize(raw):
    raw = raw if isinstance(raw, dict) else {}
    settings = dict(DEFAULT_SETTINGS)
    if isinstance(raw.get("settings"), dict):
        settings.update(raw["settings"])
    return {
        "tankowania": raw.get("tankowania") if isinstance(raw.get("tankowania"), list) else _seed_tankowania(),
        "serwisy": raw.get("serwisy") if isinstance(raw.get("serwisy"), list) else _seed_serwisy(),
        "koszty": raw.get("koszty") if isinstance(raw.get("koszty"), list) else _seed_koszty(),
        "settings": settings,
    }


def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return sanitize(json.load(f))
    except Exception:
        pass
    data = seed_data()
    save_data(data)
    return data


def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DATA_FILE)


# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------
def pln(v):
    try:
        return f"{v:,.2f} zł".replace(",", " ").replace(".", ",")
    except Exception:
        return "— zł"


def numf(v, d=1):
    if v is None:
        return "—"
    try:
        return f"{v:,.{d}f}".replace(",", " ").replace(".", ",")
    except Exception:
        return "—"


def date_fmt(s):
    try:
        d = dt.datetime.strptime(s, "%Y-%m-%d")
        return d.strftime("%d.%m.%Y")
    except Exception:
        return s or "—"


def month_key(s):
    return s[:7]


MONTHS_PL = ["sty", "lut", "mar", "kwi", "maj", "cze", "lip", "sie", "wrz", "paź", "lis", "gru"]


def month_label(key):
    y, m = key.split("-")
    return f"{MONTHS_PL[int(m) - 1]} {y[2:]}"


def status_of(consumption, settings):
    if consumption is None:
        return None
    if consumption >= settings["consumptionHighFrom"]:
        return ("Wysokie", C["red"])
    if consumption > settings["consumptionOkTo"]:
        return ("Uwaga", C["amber"])
    return ("OK", C["green"])


def new_id():
    return uuid.uuid4().hex[:8]


def recalc_tankowania(tankowania):
    """Distance and consumption follow from the mileage difference to the previous fill-up (as in the xlsx)."""
    prev = None
    for t in sorted(tankowania, key=lambda t: (t["date"], t["mileage"])):
        distance = t["mileage"] - prev["mileage"] if prev else None
        t["distance"] = distance
        t["consumption"] = round(t["liters"] / distance * 100, 2) if distance and distance > 0 else None
        prev = t


def num_in(v):
    """Number -> text for a form field (Polish decimal comma)."""
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).replace(".", ",")


# ----------------------------------------------------------------------
# AGGREGATION
# ----------------------------------------------------------------------
def compute_aggregates(data):
    tankowania = data["tankowania"]
    serwisy = data["serwisy"]
    koszty = data["koszty"]
    settings = data["settings"]

    valid_dist = [t for t in tankowania if t.get("distance")]
    total_liters = sum(t["liters"] for t in tankowania)
    total_fuel_cost = sum(t["cost"] for t in tankowania)
    total_distance = sum(t["distance"] for t in valid_dist)
    liters_for_distance = sum(t["liters"] for t in valid_dist)
    weighted_consumption = (liters_for_distance / total_distance * 100) if total_distance else None
    avg_price_per_l = (total_fuel_cost / total_liters) if total_liters else None

    paid_service = sum(s.get("paidCost", 0) for s in serwisy)
    koszty_total = sum(k.get("amount", 0) for k in koszty)
    total_cost = total_fuel_cost + paid_service + koszty_total
    cost_per_km = (total_cost / total_distance) if total_distance else None

    alerts = sum(1 for t in tankowania if (status_of(t.get("consumption"), settings) or (None,))[0] == "Wysokie")
    last_service = max(serwisy, key=lambda s: s["date"]) if serwisy else None

    month_map = {}

    def bucket(k):
        return month_map.setdefault(k, {"fuelCost": 0, "distance": 0, "litersForDist": 0, "paidService": 0, "extra": 0})

    for t in tankowania:
        b = bucket(month_key(t["date"]))
        b["fuelCost"] += t["cost"]
        if t.get("distance"):
            b["distance"] += t["distance"]
            b["litersForDist"] += t["liters"]
    for s in serwisy:
        if not s.get("date"):
            continue
        b = bucket(month_key(s["date"]))
        b["paidService"] += s.get("paidCost", 0)
    for k in koszty:
        if k.get("type") == "Zakup auta":
            continue
        b = bucket(month_key(k["date"]))
        b["extra"] += k.get("amount", 0)

    monthly = []
    for k in sorted(month_map.keys()):
        v = month_map[k]
        total = v["fuelCost"] + v["paidService"] + v["extra"]
        consumption = (v["litersForDist"] / v["distance"] * 100) if v["distance"] else None
        monthly.append({
            "key": k, "label": month_label(k), "fuelCost": v["fuelCost"], "distance": v["distance"],
            "consumption": consumption, "paidService": v["paidService"], "extra": v["extra"], "total": total,
        })

    return {
        "totalLiters": total_liters, "totalFuelCost": total_fuel_cost, "totalDistance": total_distance,
        "weightedConsumption": weighted_consumption, "avgPricePerL": avg_price_per_l,
        "paidService": paid_service, "kosztyTotal": koszty_total, "totalCost": total_cost,
        "costPerKm": cost_per_km, "alerts": alerts, "lastService": last_service, "monthly": monthly,
    }


# ----------------------------------------------------------------------
# INPUT PARSING / FORMATTING
# ----------------------------------------------------------------------
MONTHS_FULL = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień",
               "Wrzesień", "Październik", "Listopad", "Grudzień"]


def plural(n, one, few, many):
    if n == 1:
        return f"{n} {one}"
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return f"{n} {few}"
    return f"{n} {many}"


def parse_date(s):
    """'10.10.2026', '1.2.2026' or '2026-10-10' -> ISO date string; ValueError otherwise."""
    s = s.strip()
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d.%m.%y"):
        try:
            return dt.datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    raise ValueError("Podaj datę w formacie DD.MM.RRRR")


def parse_number(s, *, integer=False, allow_empty=False, minimum=None):
    s = s.strip().replace(" ", "").replace(" ", "").replace(",", ".")
    if not s:
        if allow_empty:
            return None
        raise ValueError("To pole jest wymagane")
    try:
        v = int(s) if integer else float(s)
    except ValueError:
        raise ValueError("Wpisz liczbę całkowitą" if integer else "Wpisz liczbę, np. 52,4")
    if minimum is not None and v < minimum:
        raise ValueError(f"Wartość musi być ≥ {numf(minimum, 0)}")
    return v


# ----------------------------------------------------------------------
# FONTS, ICONS, IMAGES
# ----------------------------------------------------------------------
_FONT_CACHE = {}
_FAMILIES = None


def _family(*candidates):
    global _FAMILIES
    if _FAMILIES is None:
        _FAMILIES = set(tkfont.families())
    for c in candidates:
        if c in _FAMILIES:
            return c
    return "Segoe UI" if os.name == "nt" else "Helvetica"


def font(size, weight="normal", display=False):
    """weight: normal | semibold. Segoe UI Variable exposes semibold as separate families."""
    key = (size, weight, display)
    if key not in _FONT_CACHE:
        if weight == "semibold":
            fam = (_family("Segoe UI Variable Display Semib", "Segoe UI Semibold") if display
                   else _family("Segoe UI Variable Text Semibold", "Segoe UI Semibold"))
            if fam in ("Segoe UI", "Helvetica"):
                _FONT_CACHE[key] = ctk.CTkFont(family=fam, size=size, weight="bold")
                return _FONT_CACHE[key]
        else:
            fam = _family("Segoe UI Variable Display" if display else "Segoe UI Variable Text", "Segoe UI")
        _FONT_CACHE[key] = ctk.CTkFont(family=fam, size=size)
    return _FONT_CACHE[key]


def tk_font(widget, size, weight="normal", display=False):
    """Font tuple for plain tk widgets, scaled the way CTk scales its own fonts."""
    f = font(size, weight, display)
    px = -abs(round(size * ctk.ScalingTracker.get_widget_scaling(widget)))
    return (f.cget("family"), px, f.cget("weight"))


ICONS = {
    "home": "", "fuel": "", "wrench": "", "card": "", "chart": "",
    "settings": "", "add": "", "edit": "", "delete": "", "calendar": "",
    "close": "", "check": "", "warning": "", "export": "", "import": "",
    "car": "", "clock": "", "info": "", "flame": "", "prev": "",
    "next": "", "road": "", "save": "",
}
_ICON_FONT_FILE = next((p for p in (WIN_FONTS / "SegoeIcons.ttf", WIN_FONTS / "segmdl2.ttf") if p.exists()), None)
_ICON_CACHE = {}


def icon(name, color=C["text_dim"], size=18):
    """Icon glyph from the Windows icon font as a CTkImage (None if the font is unavailable)."""
    key = (name, color, size)
    if key in _ICON_CACHE:
        return _ICON_CACHE[key]
    img = None
    if _ICON_FONT_FILE is not None:
        s = size * 4
        pil = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        f = ImageFont.truetype(str(_ICON_FONT_FILE), int(s * 0.86))
        d = ImageDraw.Draw(pil)
        x0, y0, x1, y1 = d.textbbox((0, 0), ICONS[name], font=f)
        d.text(((s - (x1 - x0)) / 2 - x0, (s - (y1 - y0)) / 2 - y0), ICONS[name], font=f, fill=color)
        img = ctk.CTkImage(light_image=pil, dark_image=pil, size=(size, size))
    _ICON_CACHE[key] = img
    return img


def asset_image(filename, height):
    path = ASSET_DIR / filename
    if not path.exists():
        return None
    pil = Image.open(path)
    return ctk.CTkImage(light_image=pil, dark_image=pil, size=(round(pil.width * height / pil.height), height))


def _pil_font(size, weight="Semibold"):
    var = WIN_FONTS / "SegUIVar.ttf"
    try:
        f = ImageFont.truetype(str(var), size)
        try:
            f.set_variation_by_name(weight)
        except Exception:
            pass
        return f
    except Exception:
        try:
            return ImageFont.truetype("segoeuib.ttf" if weight != "Regular" else "segoeui.ttf", size)
        except Exception:
            return ImageFont.load_default()


def _rgb(hex_color):
    return tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))


def render_gauge(value, settings, size=190):
    """Anti-aliased 270° consumption ring (drawn 4x and scaled down)."""
    scale = 4
    S = size * scale
    img = Image.new("RGBA", (S, S), _rgb(C["surface"]) + (0,))
    d = ImageDraw.Draw(img)
    width = 13 * scale
    pad = width // 2 + 4 * scale
    box = (pad, pad, S - pad, S - pad)
    status = status_of(value, settings)
    color = status[1] if status else C["text_faint"]
    vmax = max(settings["consumptionHighFrom"] * 1.4, (value * 1.15) if value else 12)
    pct = min(value / vmax, 1) if value else 0

    def cap(angle, col):
        r = (S - 2 * pad) / 2
        cx = cy = S / 2
        x = cx + r * math.cos(math.radians(angle))
        y = cy + r * math.sin(math.radians(angle))
        d.ellipse((x - width / 2, y - width / 2, x + width / 2, y + width / 2), fill=col)

    d.arc(box, 135, 405, fill=C["surface3"], width=width)
    cap(135, C["surface3"]), cap(405, C["surface3"])
    for thr, col in ((settings["consumptionOkTo"], C["amber"]), (settings["consumptionHighFrom"], C["red"])):
        a = 135 + 270 * min(thr / vmax, 1)
        d.arc(box, a - 0.8, a + 0.8, fill=col, width=width // 3)
    if pct > 0:
        end = 135 + 270 * pct
        d.arc(box, 135, end, fill=color, width=width)
        cap(135, color), cap(end, color)

    big = _pil_font(46 * scale)
    small = _pil_font(13 * scale, "Regular")
    txt = numf(value, 1) if value else "—"
    w = d.textlength(txt, font=big)
    d.text(((S - w) / 2, S * 0.30), txt, font=big, fill=C["text"])
    unit = "l / 100 km"
    w = d.textlength(unit, font=small)
    d.text(((S - w) / 2, S * 0.62), unit, font=small, fill=C["text_dim"])
    return img.resize((size * 2, size * 2), Image.LANCZOS)


matplotlib.rcParams.update({
    "font.family": ["Segoe UI", "DejaVu Sans"],
    "font.size": 8,
    "axes.edgecolor": C["line"],
    "xtick.color": C["text_faint"],
    "ytick.color": C["text_faint"],
})


# ----------------------------------------------------------------------
# SMALL WIDGETS
# ----------------------------------------------------------------------
def card(master, **kw):
    kw.setdefault("fg_color", C["surface"])
    kw.setdefault("corner_radius", 16)
    return ctk.CTkFrame(master, **kw)


def label(master, text="", size=13, color=C["text"], weight="normal", display=False, **kw):
    return ctk.CTkLabel(master, text=text, text_color=color, font=font(size, weight, display), **kw)


def pill(master, text, color):
    return ctk.CTkLabel(master, text=text, text_color=color, fg_color=SOFT.get(color, C["surface2"]),
                        corner_radius=8, font=font(11, "semibold"), height=22, padx=10)


def primary_button(master, text, command, icon_name=None, **kw):
    return ctk.CTkButton(master, text=text, command=command, height=38, corner_radius=10,
                         fg_color=C["copper"], hover_color=C["copper_hover"], text_color="#140D08",
                         font=font(13, "semibold"), image=icon(icon_name, "#140D08", 16) if icon_name else None,
                         **kw)


def ghost_button(master, text, command, icon_name=None, color=C["text"], **kw):
    kw.setdefault("height", 38)
    return ctk.CTkButton(master, text=text, command=command, corner_radius=10,
                         fg_color="transparent", hover_color=C["surface3"], border_width=1,
                         border_color=C["line"], text_color=color, font=font(13),
                         image=icon(icon_name, color, 16) if icon_name else None, **kw)


def icon_button(master, name, command, color=C["text_dim"], size=34):
    return ctk.CTkButton(master, text="", width=size, height=size, corner_radius=9, command=command,
                         fg_color="transparent", hover_color=C["surface3"], image=icon(name, color, 16))


def bind_tree(widget, sequence, handler):
    """Bind on a widget and all of its descendants (CTk widgets are made of several tk widgets)."""
    widget.bind(sequence, handler, add="+")
    for child in widget.winfo_children():
        # a CTk widget's bind() already covers its internal tk parts; only recurse into real children
        if isinstance(child, ctk.CTkBaseClass) or not isinstance(widget, ctk.CTkBaseClass):
            bind_tree(child, sequence, handler)


def is_descendant(widget, ancestor):
    while widget is not None:
        if widget == ancestor:
            return True
        widget = widget.master
    return False


class Toast:
    """Short confirmation in the bottom-right corner of the main window."""

    def __init__(self, app):
        self.app = app
        self.frame = None
        self.job = None

    def show(self, text, kind="ok"):
        color = {"ok": C["green"], "warn": C["amber"], "error": C["red"]}[kind]
        if self.frame is not None:
            self.frame.destroy()
        if self.job:
            self.app.after_cancel(self.job)
        self.frame = ctk.CTkFrame(self.app, fg_color=C["surface2"], corner_radius=12,
                                  border_width=1, border_color=C["line"])
        row = ctk.CTkFrame(self.frame, fg_color="transparent")
        row.pack(padx=16, pady=12)
        ctk.CTkLabel(row, text="", image=icon("check" if kind == "ok" else "warning", color, 16)).pack(side="left")
        label(row, text, 13).pack(side="left", padx=(10, 0))
        self.frame.place(relx=1.0, rely=1.0, x=-24, y=-24, anchor="se")
        self.frame.lift()
        self.job = self.app.after(2600, self.hide)

    def hide(self):
        if self.frame is not None:
            self.frame.destroy()
            self.frame = None
        self.job = None


# ----------------------------------------------------------------------
# DIALOGS
# ----------------------------------------------------------------------
class Dialog(ctk.CTkToplevel):
    """Modal dialog centred over the main window, Esc closes."""

    def __init__(self, app, title, icon_name=None, width=480):
        super().__init__(app)
        self.app = app
        # hidden via alpha, not withdraw(): CTk keeps a window withdrawn after its dark-titlebar redraw
        # if withdraw() was called, and the dialog would never appear
        self.attributes("-alpha", 0.0)
        self.title(title)
        self.configure(fg_color=C["surface"])
        self.resizable(False, False)
        self.transient(app)

        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=24, pady=(20, 4))
        if icon_name:
            chip = ctk.CTkLabel(head, text="", width=36, height=36, corner_radius=10, fg_color=C["copper_soft"],
                                image=icon(icon_name, C["copper"], 18))
            chip.pack(side="left", padx=(0, 12))
        label(head, title, 18, weight="semibold", display=True).pack(side="left")
        icon_button(head, "close", self.close).pack(side="right")

        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=24, pady=(8, 0))
        ctk.CTkFrame(self.body, fg_color="transparent", width=width, height=1).pack()  # minimum width
        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        self.footer.pack(fill="x", padx=24, pady=(16, 20))

        self.bind("<Escape>", lambda e: self.close())
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.after(20, self._present)
        ico = ASSET_DIR / "app.ico"
        if os.name == "nt" and ico.exists():
            self.after(260, lambda: self.iconbitmap(str(ico)))  # CTkToplevel sets its own icon at ~200 ms

    def _present(self):
        self.update_idletasks()
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        ax, ay, aw, ah = self.app.winfo_rootx(), self.app.winfo_rooty(), self.app.winfo_width(), self.app.winfo_height()
        self.geometry(f"+{max(0, ax + (aw - w) // 2)}+{max(0, ay + (ah - h) // 3)}")
        self.attributes("-alpha", 1.0)
        self.lift()
        try:
            self.grab_set()
        except tk.TclError:
            pass
        self.focus_first()

    def focus_first(self):
        self.focus_force()

    def close(self):
        try:
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()


class ConfirmDialog(Dialog):
    def __init__(self, app, title, message, confirm_text, on_confirm, danger=True):
        super().__init__(app, title, "warning" if danger else "info", width=420)
        label(self.body, message, 13, C["text_dim"], wraplength=400, justify="left").pack(anchor="w")
        ghost_button(self.footer, "Anuluj", self.close, width=110).pack(side="right")
        btn = ctk.CTkButton(self.footer, text=confirm_text, height=38, corner_radius=10, width=130,
                            fg_color=C["red"] if danger else C["copper"],
                            hover_color="#D85A4D" if danger else C["copper_hover"],
                            text_color="#FFFFFF" if danger else "#140D08", font=font(13, "semibold"),
                            command=lambda: (self.close(), on_confirm()))
        btn.pack(side="right", padx=(0, 8))
        self.bind("<Return>", lambda e: btn.invoke())


class CalendarPopup(Dialog):
    """Month grid date picker; calls on_pick(iso_date)."""

    def __init__(self, app, initial_iso, on_pick):
        super().__init__(app, "Wybierz datę", "calendar", width=300)
        try:
            d = dt.date.fromisoformat(initial_iso)
        except (TypeError, ValueError):
            d = dt.date.today()
        self.selected = d
        self.year, self.month = d.year, d.month
        self.on_pick = on_pick
        nav = ctk.CTkFrame(self.body, fg_color="transparent")
        nav.pack(fill="x")
        icon_button(nav, "prev", lambda: self.shift(-1)).pack(side="left")
        self.title_lbl = label(nav, "", 14, weight="semibold")
        self.title_lbl.pack(side="left", expand=True)
        icon_button(nav, "next", lambda: self.shift(1)).pack(side="right")
        self.grid_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.grid_frame.pack(pady=(8, 0))
        ghost_button(self.footer, "Dziś", lambda: self.pick(dt.date.today()), width=90).pack(side="left")
        ghost_button(self.footer, "Anuluj", self.close, width=90).pack(side="right")
        self.draw()

    def shift(self, delta):
        m = self.month - 1 + delta
        self.year, self.month = self.year + m // 12, m % 12 + 1
        self.draw()

    def pick(self, d):
        self.close()
        self.on_pick(d.isoformat())

    def draw(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.title_lbl.configure(text=f"{MONTHS_FULL[self.month - 1]} {self.year}")
        for i, name in enumerate(["Pn", "Wt", "Śr", "Cz", "Pt", "Sb", "Nd"]):
            label(self.grid_frame, name, 11, C["text_faint"], width=36).grid(row=0, column=i, pady=(0, 4))
        first = dt.date(self.year, self.month, 1)
        start = first - dt.timedelta(days=first.weekday())
        today = dt.date.today()
        for i in range(42):
            d = start + dt.timedelta(days=i)
            in_month = d.month == self.month
            is_sel = d == self.selected
            b = ctk.CTkButton(
                self.grid_frame, text=str(d.day), width=36, height=32, corner_radius=8,
                font=font(12, "semibold" if is_sel or d == today else "normal"),
                fg_color=C["copper"] if is_sel else "transparent",
                hover_color=C["copper_hover"] if is_sel else C["surface3"],
                text_color="#140D08" if is_sel else (C["copper"] if d == today else
                                                      (C["text"] if in_month else C["text_faint"])),
                command=lambda d=d: self.pick(d))
            b.grid(row=1 + i // 7, column=i % 7, padx=1, pady=1)


class Field:
    """Labelled entry with optional unit suffix, hint and inline error message."""

    def __init__(self, parent, title, value="", suffix=None, hint=None, placeholder=""):
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        top = ctk.CTkFrame(self.frame, fg_color="transparent")
        top.pack(fill="x")
        label(top, title, 12, C["text_dim"]).pack(side="left")
        # CTkEntry ignores placeholder_text when a textvariable is set, so the example goes next to the title
        self.hint = label(top, hint or placeholder, 11, C["text_faint"])
        self.hint.pack(side="right")
        self.var = tk.StringVar(value=value)
        self.row = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.row.pack(fill="x", pady=(4, 0))
        self.entry = ctk.CTkEntry(self.row, textvariable=self.var, height=40, corner_radius=10, border_width=1,
                                  fg_color=C["surface2"], border_color=C["line"], text_color=C["text"],
                                  placeholder_text=placeholder, placeholder_text_color=C["text_faint"],
                                  font=font(14))
        self.entry.pack(side="left", fill="x", expand=True)
        if suffix:
            label(self.entry, suffix, 12, C["text_faint"], fg_color=C["surface2"]).place(
                relx=1.0, rely=0.5, x=-12, anchor="e")
        self.error = label(self.frame, "", 11, C["red"])
        self._has_error = False
        self.entry.bind("<FocusIn>", lambda e: self._border())
        self.entry.bind("<FocusOut>", lambda e: self._border())
        self.var.trace_add("write", lambda *a: self.set_error(None) if self._has_error else None)

    def _border(self):
        try:
            focused = self.entry.focus_get() == self.entry._entry
        except (KeyError, tk.TclError):
            focused = False
        color = C["red"] if self._has_error else (C["copper"] if focused else C["line"])
        self.entry.configure(border_color=color)

    def pack(self, **kw):
        kw.setdefault("fill", "x")
        kw.setdefault("pady", (0, 12))
        self.frame.pack(**kw)
        return self

    def grid(self, **kw):
        self.frame.grid(**kw)
        return self

    def get(self):
        return self.var.get().strip()

    def set(self, value):
        self.var.set(value)

    def set_error(self, msg):
        self._has_error = bool(msg)
        if msg:
            self.error.configure(text=msg)
            self.error.pack(anchor="w", pady=(3, 0))
        else:
            self.error.pack_forget()
        self._border()


class DateField(Field):
    def __init__(self, parent, app, title="Data", iso=None):
        super().__init__(parent, title, date_fmt(iso or dt.date.today().isoformat()), placeholder="DD.MM.RRRR")
        self.app = app
        for text, days in (("Dziś", 0), ("Wczoraj", 1)):
            ctk.CTkButton(self.row, text=text, width=70, height=40, corner_radius=10, font=font(12),
                          fg_color=C["surface2"], hover_color=C["surface3"], text_color=C["text_dim"],
                          command=lambda d=days: self.set(date_fmt((dt.date.today() - dt.timedelta(days=d)).isoformat()))
                          ).pack(side="left", padx=(6, 0))
        ctk.CTkButton(self.row, text="", width=40, height=40, corner_radius=10, fg_color=C["surface2"],
                      hover_color=C["surface3"], image=icon("calendar", C["text_dim"], 16),
                      command=self.open_calendar).pack(side="left", padx=(6, 0))

    def open_calendar(self):
        try:
            iso = parse_date(self.get())
        except ValueError:
            iso = None
        CalendarPopup(self.app, iso, lambda v: self.set(date_fmt(v)))

    def value(self):
        return parse_date(self.get())


class EntryForm(Dialog):
    """Base for add/edit forms. Subclasses build fields and implement collect()."""
    collection = None
    noun = None  # e.g. "tankowanie"

    def __init__(self, app, entry, title_new, title_edit, icon_name):
        self.entry = entry
        super().__init__(app, title_edit if entry else title_new, icon_name)
        self.build()
        if entry is not None:
            ctk.CTkButton(self.footer, text="Usuń", width=90, height=38, corner_radius=10, fg_color="transparent",
                          hover_color=C["red_soft"], text_color=C["red"], font=font(13),
                          image=icon("delete", C["red"], 16), command=self.delete).pack(side="left")
        primary_button(self.footer, "Zapisz zmiany" if entry else "Zapisz", self.save, "check",
                       width=150).pack(side="right")
        ghost_button(self.footer, "Anuluj", self.close, width=100).pack(side="right", padx=(0, 8))
        self.bind("<Return>", lambda e: self.save())

    def focus_first(self):
        first = getattr(self, "first_field", None)
        if first is not None:
            first.entry.focus_set()
            first.entry._entry.icursor("end")

    def save(self):
        values = self.collect()
        if values is None:
            return False
        saved = self.app.upsert(self.collection, self.entry, values)
        self.close()
        self.app.toast.show(self.saved_message(saved))
        return True

    def delete(self):
        self.app.confirm_delete(self.collection, self.entry, on_done=self.close)

    @staticmethod
    def check(field, fn):
        """Run a parser for one field; show its error inline. Returns (ok, value)."""
        try:
            v = fn()
            field.set_error(None)
            return True, v
        except ValueError as exc:
            field.set_error(str(exc))
            return False, None


def required(value, message):
    if not value:
        raise ValueError(message)
    return value


def two_columns(parent):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x")
    row.columnconfigure((0, 1), weight=1, uniform="col")
    return row


class TankowanieForm(EntryForm):
    collection = "tankowania"

    def __init__(self, app, entry=None):
        super().__init__(app, entry, "Nowe tankowanie", "Edycja tankowania", "fuel")

    def _previous(self, date_iso, mileage):
        e = self.entry
        before = [t for t in self.app.data["tankowania"] if t is not e and
                  (t["date"], t["mileage"]) < (date_iso, mileage)]
        return max(before, key=lambda t: (t["date"], t["mileage"]), default=None)

    def build(self):
        e = self.entry or {}
        last = max(self.app.data["tankowania"], key=lambda t: (t["date"], t["mileage"]), default=None)
        self.f_date = DateField(self.body, self.app, iso=e.get("date")).pack()
        label(self.body, "Paliwo", 12, C["text_dim"]).pack(anchor="w")
        self.v_fuel = tk.StringVar(value=e.get("fuelType", (last or {}).get("fuelType", "Pb98")))
        ctk.CTkSegmentedButton(self.body, values=FUEL_TYPES, variable=self.v_fuel, height=36, corner_radius=10,
                               font=font(13), fg_color=C["surface2"], selected_color=C["copper"],
                               selected_hover_color=C["copper_hover"], unselected_color=C["surface2"],
                               unselected_hover_color=C["surface3"], text_color=C["text"]
                               ).pack(fill="x", pady=(4, 12))
        row = two_columns(self.body)
        self.f_liters = Field(row, "Litry", num_in(e.get("liters")), "l", placeholder="np. 52,4").grid(
            row=0, column=0, sticky="ew", padx=(0, 6), pady=(0, 12))
        self.f_cost = Field(row, "Kwota", num_in(e.get("cost")), "zł", placeholder="np. 412,80").grid(
            row=0, column=1, sticky="ew", padx=(6, 0), pady=(0, 12))
        self.f_mileage = Field(self.body, "Przebieg", num_in(e.get("mileage")), "km",
                               placeholder=f"np. {(last or {}).get('mileage', 0) + 600}").pack()
        self.f_note = Field(self.body, "Notatka", e.get("note", ""), placeholder="opcjonalnie").pack()

        self.summary = ctk.CTkFrame(self.body, fg_color=C["surface2"], corner_radius=12)
        self.summary.pack(fill="x", pady=(4, 0))
        self.summary.columnconfigure((0, 1, 2), weight=1, uniform="s")
        self.sum_vals = {}
        for i, (key, title) in enumerate((("price", "Cena za litr"), ("dist", "Dystans"), ("cons", "Spalanie"))):
            cell = ctk.CTkFrame(self.summary, fg_color="transparent")
            cell.grid(row=0, column=i, sticky="w", padx=14, pady=10)
            label(cell, title, 11, C["text_faint"]).pack(anchor="w")
            self.sum_vals[key] = label(cell, "—", 15, weight="semibold", display=True)
            self.sum_vals[key].pack(anchor="w")
        for f in (self.f_date, self.f_liters, self.f_cost, self.f_mileage):
            f.var.trace_add("write", lambda *a: self.update_summary())
        self.update_summary()
        self.first_field = self.f_liters if self.entry is None else self.f_date

    def update_summary(self):
        def num(f, **kw):
            try:
                return parse_number(f.get(), **kw)
            except ValueError:
                return None
        liters, cost = num(self.f_liters), num(self.f_cost)
        mileage = num(self.f_mileage, integer=True)
        try:
            date_iso = parse_date(self.f_date.get())
        except ValueError:
            date_iso = None
        self.sum_vals["price"].configure(text=f"{numf(cost / liters, 2)} zł" if liters and cost else "—")
        prev = self._previous(date_iso, mileage) if date_iso and mileage is not None else None
        anchor = prev or (max(self.app.data["tankowania"], key=lambda t: (t["date"], t["mileage"]), default=None)
                          if self.entry is None else self._previous(self.entry["date"], self.entry["mileage"]))
        self.f_mileage.hint.configure(text=f"poprzednio {numf(anchor['mileage'], 0)} km" if anchor else "")
        dist = mileage - prev["mileage"] if prev and mileage is not None else None
        self.sum_vals["dist"].configure(text=f"{numf(dist, 0)} km" if dist is not None else "—",
                                        text_color=C["red"] if dist is not None and dist <= 0 else C["text"])
        cons = liters / dist * 100 if liters and dist and dist > 0 else None
        st = status_of(cons, self.app.data["settings"])
        self.sum_vals["cons"].configure(text=f"{numf(cons, 2)} l/100" if cons else "—",
                                        text_color=st[1] if st else C["text"])

    def collect(self):
        ok1, date_iso = self.check(self.f_date, self.f_date.value)
        ok2, liters = self.check(self.f_liters, lambda: parse_number(self.f_liters.get(), minimum=0.01))
        ok3, cost = self.check(self.f_cost, lambda: parse_number(self.f_cost.get(), minimum=0))
        ok4, mileage = self.check(self.f_mileage, lambda: parse_number(self.f_mileage.get(), integer=True, minimum=0))
        if not (ok1 and ok2 and ok3 and ok4):
            return None
        return {"date": date_iso, "fuelType": self.v_fuel.get(), "liters": liters, "cost": cost,
                "pricePerL": round(cost / liters, 3), "mileage": mileage, "note": self.f_note.get()}

    @staticmethod
    def saved_message(t):
        return f"Zapisano tankowanie z {date_fmt(t['date'])}"


class SerwisForm(EntryForm):
    collection = "serwisy"

    def __init__(self, app, entry=None):
        super().__init__(app, entry, "Nowy wpis serwisowy", "Edycja wpisu serwisowego", "wrench")

    def build(self):
        e = self.entry or {}
        self.f_date = DateField(self.body, self.app, iso=e.get("date")).pack()
        self.f_desc = Field(self.body, "Co zostało wykonane", e.get("description", ""),
                            placeholder="np. wymiana oleju i filtrów").pack()
        row = two_columns(self.body)
        self.f_mileage = Field(row, "Przebieg", num_in(e.get("mileage")), "km", placeholder="opcjonalnie").grid(
            row=0, column=0, sticky="ew", padx=(0, 6), pady=(0, 12))
        self.f_price = Field(row, "Cena", num_in(e.get("price")), "zł", placeholder="0").grid(
            row=0, column=1, sticky="ew", padx=(6, 0), pady=(0, 12))
        self.v_warranty = tk.BooleanVar(value=e.get("warranty", False))
        sw = ctk.CTkFrame(self.body, fg_color=C["surface2"], corner_radius=12)
        sw.pack(fill="x", pady=(0, 12))
        txt = ctk.CTkFrame(sw, fg_color="transparent")
        txt.pack(side="left", padx=14, pady=10)
        label(txt, "Naprawa gwarancyjna", 13, weight="semibold").pack(anchor="w")
        label(txt, "nie wlicza się do kosztów", 11, C["text_faint"]).pack(anchor="w")
        self.switch = ctk.CTkSwitch(sw, text="", variable=self.v_warranty, onvalue=True, offvalue=False,
                                    progress_color=C["copper"], button_color=C["text"],
                                    button_hover_color="#FFFFFF", fg_color=C["line"], width=46)
        self.switch.pack(side="right", padx=14)
        self.f_note = Field(self.body, "Notatka", e.get("note", ""), placeholder="opcjonalnie, np. nazwa serwisu").pack()
        self.first_field = self.f_desc if self.entry is None else self.f_date

    def collect(self):
        ok1, date_iso = self.check(self.f_date, self.f_date.value)
        ok2, _ = self.check(self.f_desc, lambda: required(self.f_desc.get(), "Opisz, co zostało zrobione"))
        ok3, mileage = self.check(self.f_mileage, lambda: parse_number(
            self.f_mileage.get(), integer=True, allow_empty=True, minimum=0))
        ok4, price = self.check(self.f_price, lambda: parse_number(self.f_price.get(), allow_empty=True, minimum=0))
        if not (ok1 and ok2 and ok3 and ok4):
            return None
        price = price or 0.0
        warranty = bool(self.v_warranty.get())
        return {"date": date_iso, "mileage": mileage, "description": self.f_desc.get(), "price": price,
                "warranty": warranty, "paidCost": 0 if warranty else price, "note": self.f_note.get()}

    @staticmethod
    def saved_message(s):
        return f"Zapisano serwis z {date_fmt(s['date'])}"


class KosztForm(EntryForm):
    collection = "koszty"

    def __init__(self, app, entry=None):
        super().__init__(app, entry, "Nowy koszt", "Edycja kosztu", "card")

    def build(self):
        e = self.entry or {}
        self.f_date = DateField(self.body, self.app, iso=e.get("date")).pack()
        label(self.body, "Kategoria", 12, C["text_dim"]).pack(anchor="w")
        self.v_type = tk.StringVar(value=e.get("type", "Inne"))
        ctk.CTkOptionMenu(self.body, values=KOSZTY_TYPES, variable=self.v_type, height=40, corner_radius=10,
                          font=font(14), dropdown_font=font(13), fg_color=C["surface2"],
                          button_color=C["surface2"], button_hover_color=C["surface3"], text_color=C["text"],
                          dropdown_fg_color=C["surface2"], dropdown_hover_color=C["surface3"],
                          dropdown_text_color=C["text"]).pack(fill="x", pady=(4, 12))
        self.f_desc = Field(self.body, "Opis", e.get("description", ""), placeholder="np. polisa OC/AC").pack()
        self.f_amount = Field(self.body, "Kwota", num_in(e.get("amount")), "zł", placeholder="np. 250").pack()
        self.f_note = Field(self.body, "Notatka", e.get("note", ""), placeholder="opcjonalnie").pack()
        self.first_field = self.f_desc if self.entry is None else self.f_date

    def collect(self):
        ok1, date_iso = self.check(self.f_date, self.f_date.value)
        ok2, amount = self.check(self.f_amount, lambda: parse_number(self.f_amount.get(), minimum=0))
        if not (ok1 and ok2):
            return None
        return {"date": date_iso, "type": self.v_type.get(),
                "description": self.f_desc.get() or self.v_type.get(), "amount": amount, "note": self.f_note.get()}

    @staticmethod
    def saved_message(k):
        return f"Zapisano koszt: {k['description']}"


# ----------------------------------------------------------------------
# CHARTS
# ----------------------------------------------------------------------
class ChartCard(ctk.CTkFrame):
    """Matplotlib chart in a card, with a hover read-out in the card header."""

    def __init__(self, master, title, kind, color, fmt, height=2.5):
        super().__init__(master, fg_color=C["surface"], corner_radius=16)
        self.kind, self.color, self.fmt = kind, color, fmt
        self.labels, self.values, self.guides = [], [], []
        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=18, pady=(14, 0))
        label(head, title, 14, weight="semibold").pack(side="left")
        self.readout = label(head, "", 12, C["text_dim"])
        self.readout.pack(side="right")
        self.fig = Figure(figsize=(4.4, height), dpi=100, facecolor=C["surface"])
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        w = self.canvas.get_tk_widget()
        w.configure(bg=C["surface"], highlightthickness=0)
        w.pack(fill="both", expand=True, padx=12, pady=(4, 12))
        self.canvas.mpl_connect("motion_notify_event", self._hover)
        self.canvas.mpl_connect("figure_leave_event", lambda e: self._show_point(None))
        self.active = None

    def set_data(self, labels, values, guides=()):
        self.labels, self.values, self.guides = labels, values, guides
        self.active = None
        self._render_chart()
        self._show_point(None)

    def _render_chart(self):
        ax = self.ax
        ax.clear()
        ax.set_facecolor(C["surface"])
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(C["line"])
        ax.tick_params(length=0, labelsize=8, pad=6)
        ax.grid(True, axis="y", color=C["line"], linewidth=0.6)
        ax.set_axisbelow(True)
        xs = list(range(len(self.values)))
        if not xs:
            self.canvas.draw_idle()
            return
        hi = self.active if self.active is not None else len(xs) - 1
        if self.kind == "bar":
            colors = [self.color if i == hi else C["copper_dim"] for i in xs]
            ax.bar(xs, self.values, color=colors, width=0.62, zorder=2)
        else:
            ax.fill_between(xs, self.values, min(self.values) * 0.92, color=self.color, alpha=0.10, zorder=1)
            ax.plot(xs, self.values, color=self.color, linewidth=2.2, zorder=2)
            ax.scatter(xs, self.values, s=[42 if i == hi else 14 for i in xs], color=self.color,
                       edgecolor=C["surface"], linewidth=1.5, zorder=3)
            lo = min(self.values + [g[0] for g in self.guides])
            top = max(self.values + [g[0] for g in self.guides])
            ax.set_ylim(lo - (top - lo) * 0.15, top + (top - lo) * 0.15)
        for y, col in self.guides:
            ax.axhline(y, color=col, linewidth=1, linestyle=(0, (4, 4)), alpha=0.7, zorder=1)
        ax.set_xticks(xs, [l.replace(" ", "\n") for l in self.labels])
        ax.set_xlim(-0.6, len(xs) - 0.4)
        self.fig.subplots_adjust(left=0.1, right=0.98, top=0.95, bottom=0.2)
        self.canvas.draw_idle()

    def _hover(self, event):
        if event.inaxes is not self.ax or event.xdata is None or not self.values:
            return self._show_point(None)
        i = int(round(event.xdata))
        if 0 <= i < len(self.values):
            self._show_point(i)

    def _show_point(self, i):
        if i != self.active:
            self.active = i
            self._render_chart()
        k = len(self.values) - 1 if i is None else i
        self.readout.configure(text=f"{self.labels[k]}  ·  {self.fmt(self.values[k])}" if self.values else "")


# ----------------------------------------------------------------------
# PAGES
# ----------------------------------------------------------------------
class Page(ctk.CTkFrame):
    title = ""
    subtitle = ""

    def __init__(self, app):
        super().__init__(app.content, fg_color="transparent")
        self.app = app
        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=32, pady=(28, 18))
        tt = ctk.CTkFrame(head, fg_color="transparent")
        tt.pack(side="left")
        label(tt, self.title, 26, weight="semibold", display=True).pack(anchor="w")
        self.subtitle_lbl = label(tt, self.subtitle, 13, C["text_dim"])
        self.subtitle_lbl.pack(anchor="w")
        self.actions = ctk.CTkFrame(head, fg_color="transparent", width=1, height=1)  # CTk default is 200x200
        self.actions.pack(side="right")
        self.build()

    def build(self):
        pass

    def refresh(self):
        pass


class DashboardPage(Page):
    title = "Pulpit"

    def build(self):
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=32, pady=(0, 28))
        body.columnconfigure(0, weight=0)
        body.columnconfigure((1, 2, 3), weight=1, uniform="kpi")
        body.rowconfigure(2, weight=1)

        g = card(body)
        g.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 12), pady=(0, 12))
        label(g, "ŚREDNIE SPALANIE", 11, C["text_dim"], weight="semibold").pack(pady=(18, 0))
        self.gauge = ctk.CTkLabel(g, text="")
        self.gauge.pack(padx=24, pady=(4, 0))
        self.gauge_pill = pill(g, "", C["amber"])
        self.gauge_pill.pack(pady=(0, 6))
        self.gauge_note = label(g, "", 11, C["text_faint"])
        self.gauge_note.pack(pady=(0, 16))

        self.kpis = {}
        defs = [("cost", "Koszt całkowity", "card"), ("dist", "Przejechany dystans", "road"),
                ("costkm", "Koszt / km", "chart"), ("price", "Śr. cena paliwa", "fuel"),
                ("alerts", "Alerty spalania", "flame"), ("service", "Ostatni serwis", "wrench")]
        for i, (key, title, ic) in enumerate(defs):
            c = card(body)
            c.grid(row=i // 3, column=1 + i % 3, sticky="nsew", padx=(0 if i % 3 == 0 else 6, 0 if i % 3 == 2 else 6),
                   pady=(0, 12))
            top = ctk.CTkFrame(c, fg_color="transparent")
            top.pack(fill="x", padx=18, pady=(16, 0))
            ctk.CTkLabel(top, text="", width=32, height=32, corner_radius=9, fg_color=C["copper_soft"],
                         image=icon(ic, C["copper"], 16)).pack(side="left")
            label(top, title, 12, C["text_dim"]).pack(side="left", padx=(10, 0))
            val = label(c, "—", 24, weight="semibold", display=True)
            val.pack(anchor="w", padx=18, pady=(10, 0))
            sub = label(c, "", 11, C["text_faint"])
            sub.pack(anchor="w", padx=18, pady=(0, 16))
            self.kpis[key] = (val, sub)

        charts = ctk.CTkFrame(body, fg_color="transparent")
        charts.grid(row=2, column=0, columnspan=4, sticky="nsew")
        charts.columnconfigure((0, 1), weight=1, uniform="chart")
        charts.rowconfigure(0, weight=1)
        self.chart_cost = ChartCard(charts, "Koszty miesięczne", "bar", C["copper"], pln)
        self.chart_cost.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        self.chart_cons = ChartCard(charts, "Spalanie (l/100 km)", "line", C["amber"], lambda v: f"{numf(v, 2)} l/100 km")
        self.chart_cons.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

    def refresh(self):
        data, s = self.app.data, self.app.data["settings"]
        agg = compute_aggregates(data)
        t = sorted(data["tankowania"], key=lambda x: (x["date"], x["mileage"]))
        if t:
            self.subtitle_lbl.configure(text=f"Od {date_fmt(t[0]['date'])} do {date_fmt(t[-1]['date'])}  ·  "
                                             f"przebieg {numf(t[-1]['mileage'], 0)} km")
        cons = agg["weightedConsumption"]
        img = render_gauge(cons, s)
        self.gauge.configure(image=ctk.CTkImage(light_image=img, dark_image=img, size=(190, 190)))
        st = status_of(cons, s)
        if st:
            self.gauge_pill.configure(text={"OK": "W normie", "Uwaga": "Podwyższone", "Wysokie": "Wysokie"}[st[0]],
                                      text_color=st[1], fg_color=SOFT[st[1]])
            self.gauge_pill.pack(pady=(0, 6))
        else:
            self.gauge_pill.pack_forget()
        self.gauge_note.configure(text=f"norma do {numf(s['consumptionOkTo'], 1)}  ·  wysokie od {numf(s['consumptionHighFrom'], 1)}")

        fuel_km = agg["totalFuelCost"] / agg["totalDistance"] if agg["totalDistance"] else None
        last_t = t[-1] if t else None
        ls = agg["lastService"]
        vals = {
            "cost": (pln(agg["totalCost"]), f"paliwo {pln(agg['totalFuelCost'])}"),
            "dist": (f"{numf(agg['totalDistance'], 0)} km", plural(len(t), "tankowanie", "tankowania", "tankowań")),
            "costkm": (f"{numf(agg['costPerKm'], 2)} zł" if agg["costPerKm"] else "—",
                       f"samo paliwo {numf(fuel_km, 2)} zł/km" if fuel_km else ""),
            "price": (f"{numf(agg['avgPricePerL'], 2)} zł/l" if agg["avgPricePerL"] else "—",
                      f"ostatnio {numf(last_t['pricePerL'], 2)} zł/l" if last_t else ""),
            "alerts": (str(agg["alerts"]), f"tankowania ≥ {numf(s['consumptionHighFrom'], 1)} l/100 km"),
            "service": (date_fmt(ls["date"]) if ls else "—",
                        (f"{numf(ls['mileage'], 0)} km  ·  " if ls and ls.get("mileage") else "") +
                        (("gwarancja" if ls["warranty"] else pln(ls["price"])) if ls else "")),
        }
        for k, (v, sub) in vals.items():
            self.kpis[k][0].configure(text=v)
            self.kpis[k][1].configure(text=sub)
        self.kpis["alerts"][0].configure(text_color=C["red"] if agg["alerts"] else C["text"])

        monthly = [m for m in agg["monthly"] if m["total"] > 0]
        self.chart_cost.set_data([m["label"] for m in monthly], [m["total"] for m in monthly])
        cons_m = [m for m in monthly if m["consumption"] is not None]
        self.chart_cons.set_data([m["label"] for m in cons_m], [m["consumption"] for m in cons_m],
                                 guides=[(s["consumptionOkTo"], C["amber"]), (s["consumptionHighFrom"], C["red"])])


class ListPage(Page):
    """Entries grouped by month, newest first; each row has edit/delete actions."""
    collection = None
    add_text = ""
    empty_text = ""
    form = None

    def build(self):
        primary_button(self.actions, self.add_text, lambda: self.form(self.app), "add").pack()
        self.list = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color=C["line"],
                                           scrollbar_button_hover_color=C["text_faint"])
        self.list.pack(fill="both", expand=True, padx=(32, 18), pady=(0, 20))
        self.rows = {}
        self._generation = 0

    def sort_key(self, e):
        return e["date"]

    FIRST_BATCH, BATCH = 10, 8

    def refresh(self):
        """Rebuild the list; the first rows are drawn at once, the rest in small batches so the UI stays responsive."""
        self._generation += 1
        gen = self._generation
        for w in self.list.winfo_children():
            w.destroy()
        self.rows = {}
        entries = sorted(self.app.data[self.collection], key=self.sort_key, reverse=True)
        self.subtitle_lbl.configure(text=self.summary(entries))
        if not entries:
            label(self.list, self.empty_text, 14, C["text_faint"]).pack(pady=60)
            return
        jobs, month = [], None
        for e in entries:
            if month_key(e["date"]) != month:
                month = month_key(e["date"])
                group = [x for x in entries if month_key(x["date"]) == month]
                jobs.append(lambda m=month, g=group: self.month_header(m, g))
            jobs.append(lambda e=e: self.rows.__setitem__(e["id"], self.make_row(e)))

        def run(start, count):
            if gen != self._generation or not self.winfo_exists():
                return  # a newer refresh started
            for job in jobs[start:start + count]:
                job()
            if start + count < len(jobs):
                self.after(1, lambda: run(start + count, self.BATCH))

        run(0, self.FIRST_BATCH)

    def finish_rendering(self):
        """Draw any rows still waiting in the batch queue (used by tests)."""
        for _ in range(500):
            if len(self.rows) == len(self.app.data[self.collection]):
                return
            self.update()

    def month_header(self, key, group):
        y, m = key.split("-")
        h = tk.Frame(self.list, bg=C["bg"])
        h.pack(fill="x", pady=(14, 6), padx=(4, 16))
        tk.Label(h, text=f"{MONTHS_FULL[int(m) - 1]} {y}", fg=C["text_dim"], bg=C["bg"],
                 font=tk_font(h, 13, "semibold")).pack(side="left")
        tk.Label(h, text=self.group_summary(group), fg=C["text_faint"], bg=C["bg"],
                 font=tk_font(h, 12)).pack(side="right")

    def make_row(self, e):
        # rounded parts are CTk widgets; plain text uses tk.Label, which is several times cheaper to create
        row = ctk.CTkFrame(self.list, fg_color=C["surface"], corner_radius=14)
        row.pack(fill="x", pady=(0, 6), padx=(0, 12))
        tinted = []  # tk widgets whose background follows the row colour

        def tk_frame(master):
            f = tk.Frame(master, bg=C["surface"])
            tinted.append(f)
            return f

        def text(master, s, size, color=C["text"], weight="normal", display=False, bg=C["surface"]):
            lbl = tk.Label(master, text=s, fg=color, bg=bg, font=tk_font(row, size, weight, display),
                           bd=0, padx=0, pady=0)
            if bg == C["surface"]:
                tinted.append(lbl)
            return lbl

        d = dt.date.fromisoformat(e["date"])
        db = ctk.CTkFrame(row, fg_color=C["surface2"], corner_radius=10, width=52, height=52)
        db.pack(side="left", padx=(12, 14), pady=10)
        db.pack_propagate(False)
        text(db, str(d.day), 17, weight="semibold", display=True, bg=C["surface2"]).pack(pady=(7, 0))
        text(db, MONTHS_PL[d.month - 1], 9, C["text_faint"], bg=C["surface2"]).pack()

        mid = tk_frame(row)
        mid.pack(side="left", fill="x", expand=True)
        title, sub = self.row_text(e)
        text(mid, title, 14, weight="semibold").pack(anchor="w")
        text(mid, sub, 12, C["text_dim"]).pack(anchor="w", pady=(2, 0))

        actions = tk_frame(row)
        actions.pack(side="right", padx=(6, 10))
        icon_button(actions, "edit", lambda: self.form(self.app, e)).pack(side="left")
        icon_button(actions, "delete", lambda: self.app.confirm_delete(self.collection, e),
                    color=C["text_faint"]).pack(side="left", padx=(2, 0))

        right = tk_frame(row)
        right.pack(side="right", padx=(10, 4))
        amount, badge = self.row_right(e)
        text(right, amount, 15, weight="semibold", display=True).pack(anchor="e")
        if badge:
            pill(right, *badge).pack(anchor="e", pady=(3, 0))

        def paint(color):
            row.configure(fg_color=color)
            for w in tinted:
                w.configure(bg=color)
            for b in actions.winfo_children() + right.winfo_children():
                if isinstance(b, ctk.CTkBaseClass):
                    b.configure(bg_color=color)

        def enter(_):
            paint(C["surface3"])

        def leave(ev):
            w = row.winfo_containing(ev.x_root, ev.y_root)
            if w is None or not is_descendant(w, row):
                paint(C["surface"])

        bind_tree(row, "<Enter>", enter)
        bind_tree(row, "<Leave>", leave)
        bind_tree(mid, "<Double-Button-1>", lambda ev: self.form(self.app, e))
        bind_tree(db, "<Double-Button-1>", lambda ev: self.form(self.app, e))
        return row


class TankowaniaPage(ListPage):
    title = "Tankowania"
    collection = "tankowania"
    add_text = "Dodaj tankowanie"
    empty_text = "Brak tankowań — dodaj pierwsze."

    form = TankowanieForm

    def sort_key(self, e):
        return (e["date"], e["mileage"])

    def summary(self, entries):
        if not entries:
            return ""
        return (f"{plural(len(entries), 'tankowanie', 'tankowania', 'tankowań')}  ·  "
                f"{pln(sum(t['cost'] for t in entries))}  ·  {numf(sum(t['liters'] for t in entries), 0)} l")

    def group_summary(self, group):
        return f"{numf(sum(t['liters'] for t in group), 1)} l  ·  {pln(sum(t['cost'] for t in group))}"

    def row_text(self, t):
        dist = f"  (+{numf(t['distance'], 0)} km)" if t.get("distance") else ""
        return (f"{t['fuelType']}  ·  {numf(t['liters'], 2)} l",
                f"{numf(t['mileage'], 0)} km{dist}  ·  {numf(t['pricePerL'], 2)} zł/l"
                + (f"  ·  {t['note']}" if t.get("note") else ""))

    def row_right(self, t):
        st = status_of(t.get("consumption"), self.app.data["settings"])
        badge = (f"{numf(t['consumption'], 2)} l/100", st[1]) if st else None
        return pln(t["cost"]), badge


class SerwisyPage(ListPage):
    title = "Serwisy"
    collection = "serwisy"
    add_text = "Dodaj serwis"
    empty_text = "Brak wpisów serwisowych."

    form = SerwisForm

    def summary(self, entries):
        if not entries:
            return ""
        paid = sum(s.get("paidCost", 0) for s in entries)
        return f"{plural(len(entries), 'wpis', 'wpisy', 'wpisów')}  ·  płatne {pln(paid)}"

    def group_summary(self, group):
        return pln(sum(s.get("paidCost", 0) for s in group))

    def row_text(self, s):
        parts = [f"{numf(s['mileage'], 0)} km"] if s.get("mileage") else []
        if s.get("note"):
            parts.append(s["note"])
        return s["description"], "  ·  ".join(parts) or "—"

    def row_right(self, s):
        return pln(s["price"]), ("Gwarancja", C["green"]) if s["warranty"] else ("Płatny", C["text_dim"])


class KosztyPage(ListPage):
    title = "Koszty"
    collection = "koszty"
    add_text = "Dodaj koszt"
    empty_text = "Brak kosztów."

    form = KosztForm

    def summary(self, entries):
        if not entries:
            return ""
        running = sum(k["amount"] for k in entries if k.get("type") != "Zakup auta")
        return f"{plural(len(entries), 'pozycja', 'pozycje', 'pozycji')}  ·  bez zakupu auta {pln(running)}"

    def group_summary(self, group):
        return pln(sum(k["amount"] for k in group))

    def row_text(self, k):
        return k["description"], k["type"] + (f"  ·  {k['note']}" if k.get("note") else "")

    def row_right(self, k):
        return pln(k["amount"]), (k["type"], C["copper"] if k["type"] == "Zakup auta" else C["text_dim"])


class PrognozaPage(Page):
    title = "Prognoza"
    subtitle = "Szacowane koszty paliwa na najbliższe 12 miesięcy"

    def build(self):
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=32, pady=(0, 28))
        body.columnconfigure((0, 1, 2), weight=1, uniform="p")
        body.rowconfigure(1, weight=1)
        self.kpi = {}
        for i, (key, title, ic) in enumerate((("total", "Prognoza 12 miesięcy", "chart"),
                                              ("avg", "Średnio miesięcznie", "clock"),
                                              ("assump", "Założenia", "info"))):
            c = card(body)
            c.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 6, 0 if i == 2 else 6), pady=(0, 12))
            top = ctk.CTkFrame(c, fg_color="transparent")
            top.pack(fill="x", padx=18, pady=(16, 0))
            ctk.CTkLabel(top, text="", width=32, height=32, corner_radius=9, fg_color=C["copper_soft"],
                         image=icon(ic, C["copper"], 16)).pack(side="left")
            label(top, title, 12, C["text_dim"]).pack(side="left", padx=(10, 0))
            val = label(c, "—", 15 if key == "assump" else 24, weight="semibold", display=key != "assump",
                        justify="left", anchor="w")
            val.pack(anchor="w", padx=18, pady=(10, 0))
            sub = label(c, "", 11, C["text_faint"])
            sub.pack(anchor="w", padx=18, pady=(0, 16))
            self.kpi[key] = (val, sub)
        self.chart = ChartCard(body, "Prognozowany koszt paliwa", "bar", C["copper"], pln, height=3)
        self.chart.grid(row=1, column=0, columnspan=3, sticky="nsew")

    def refresh(self):
        agg = compute_aggregates(self.app.data)
        s = self.app.data["settings"]
        base_cons = agg["weightedConsumption"] or s["consumptionOkTo"]
        base_price = agg["avgPricePerL"] or 6.5
        today = dt.date.today()
        labels, vals = [], []
        for i in range(12):
            idx = today.month - 1 + i
            year, month = today.year + idx // 12, idx % 12 + 1
            growth = (1 + s["fuelPriceGrowth"]) ** (i / 12)
            vals.append(s["monthlyKmPlan"] / 100 * base_cons * base_price * growth)
            labels.append(f"{MONTHS_PL[month - 1]} {str(year)[2:]}")
        total = sum(vals)
        self.kpi["total"][0].configure(text=pln(total))
        self.kpi["total"][1].configure(text=f"{numf(s['monthlyKmPlan'] * 12, 0)} km w roku")
        self.kpi["avg"][0].configure(text=pln(total / 12))
        self.kpi["avg"][1].configure(text=f"{numf(total / 12 / s['monthlyKmPlan'], 2)} zł/km" if s["monthlyKmPlan"] else "")
        self.kpi["assump"][0].configure(text=f"{numf(s['monthlyKmPlan'], 0)} km/mies.  ·  {numf(base_cons, 2)} l/100 km\n"
                                             f"{numf(base_price, 2)} zł/l  ·  +{numf(s['fuelPriceGrowth'] * 100, 1)}%/rok")
        self.kpi["assump"][1].configure(text="zmienisz w Ustawieniach")
        self.chart.set_data(labels, vals)


class UstawieniaPage(Page):
    title = "Ustawienia"
    subtitle = "Dane pojazdu, progi spalania, prognoza i kopia zapasowa"

    def build(self):
        primary_button(self.actions, "Zapisz ustawienia", self.save, "check").pack()
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color=C["line"],
                                        scrollbar_button_hover_color=C["text_faint"])
        scroll.pack(fill="both", expand=True, padx=(32, 18), pady=(0, 20))
        grid = ctk.CTkFrame(scroll, fg_color="transparent")
        grid.pack(fill="x", padx=(0, 12))
        grid.columnconfigure((0, 1), weight=1, uniform="s")

        def section(r, c, title, desc, ic):
            box = card(grid)
            box.grid(row=r, column=c, sticky="nsew", padx=(0 if c == 0 else 6, 6 if c == 0 else 0), pady=(0, 12))
            top = ctk.CTkFrame(box, fg_color="transparent")
            top.pack(fill="x", padx=20, pady=(18, 12))
            ctk.CTkLabel(top, text="", width=32, height=32, corner_radius=9, fg_color=C["copper_soft"],
                         image=icon(ic, C["copper"], 16)).pack(side="left")
            tt = ctk.CTkFrame(top, fg_color="transparent")
            tt.pack(side="left", padx=(10, 0))
            label(tt, title, 14, weight="semibold").pack(anchor="w")
            label(tt, desc, 11, C["text_faint"]).pack(anchor="w")
            inner = ctk.CTkFrame(box, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=20, pady=(0, 8))
            return inner

        car = section(0, 0, "Pojazd", "nazwa w nagłówku i cena zakupu", "car")
        self.f_name = Field(car, "Nazwa auta").pack()
        self.f_sub = Field(car, "Podtytuł").pack()
        self.f_price = Field(car, "Cena auta", suffix="zł").pack()

        thr = section(0, 1, "Progi spalania", "kolory statusów w listach i na pulpicie", "flame")
        self.f_ok = Field(thr, "W normie do", suffix="l/100 km").pack()
        self.f_high = Field(thr, "Wysokie od", suffix="l/100 km").pack()
        legend = ctk.CTkFrame(thr, fg_color="transparent")
        legend.pack(anchor="w", pady=(0, 12))
        for txt, col in (("W normie", C["green"]), ("Podwyższone", C["amber"]), ("Wysokie", C["red"])):
            pill(legend, txt, col).pack(side="left", padx=(0, 6))

        prog = section(1, 0, "Prognoza", "założenia do symulacji kosztów", "chart")
        self.f_km = Field(prog, "Przebieg miesięczny", suffix="km").pack()
        self.f_growth = Field(prog, "Wzrost cen paliwa", suffix="% / rok").pack()

        bk = section(1, 1, "Kopia zapasowa", "plik .json zgodny z aplikacją na telefon", "save")
        label(bk, "Dane są zapisywane automatycznie w pliku:", 12, C["text_dim"]).pack(anchor="w")
        label(bk, DATA_FILE, 11, C["text_faint"], wraplength=380, justify="left").pack(anchor="w", pady=(2, 14))
        row = ctk.CTkFrame(bk, fg_color="transparent")
        row.pack(fill="x", pady=(0, 12))
        ghost_button(row, "Eksportuj kopię", self.app.export_backup, "export").pack(side="left")
        ghost_button(row, "Wczytaj kopię", self.app.import_backup, "import").pack(side="left", padx=(8, 0))

    def refresh(self):
        s = self.app.data["settings"]
        for f, v in ((self.f_name, s["carName"]), (self.f_sub, s["carSubtitle"]),
                     (self.f_price, num_in(s["carPrice"])), (self.f_ok, num_in(s["consumptionOkTo"])),
                     (self.f_high, num_in(s["consumptionHighFrom"])), (self.f_km, num_in(s["monthlyKmPlan"])),
                     (self.f_growth, num_in(round(s["fuelPriceGrowth"] * 100, 4)))):
            f.set(v)
            f.set_error(None)

    def save(self):
        chk = EntryForm.check
        results = [
            chk(self.f_price, lambda: parse_number(self.f_price.get(), minimum=0)),
            chk(self.f_ok, lambda: parse_number(self.f_ok.get(), minimum=0.1)),
            chk(self.f_high, lambda: parse_number(self.f_high.get(), minimum=0.1)),
            chk(self.f_km, lambda: parse_number(self.f_km.get(), minimum=0)),
            chk(self.f_growth, lambda: parse_number(self.f_growth.get())),
        ]
        if not all(ok for ok, _ in results):
            return False
        price, ok_to, high, km, growth = (v for _, v in results)
        if high <= ok_to:
            self.f_high.set_error("Musi być większe niż próg „w normie”")
            return False
        s = self.app.data["settings"]
        s.update({"carName": self.f_name.get() or "MOJE AUTO", "carSubtitle": self.f_sub.get() or "DZIENNIK POKŁADOWY",
                  "carPrice": price, "consumptionOkTo": ok_to, "consumptionHighFrom": high,
                  "monthlyKmPlan": km, "fuelPriceGrowth": growth / 100})
        self.app.data_changed()
        self.app.toast.show("Ustawienia zapisane")
        return True


# ----------------------------------------------------------------------
# MAIN APPLICATION
# ----------------------------------------------------------------------
class CarApp(ctk.CTk):
    PAGES = [("dashboard", "Pulpit", "home", DashboardPage), ("tankowania", "Tankowania", "fuel", TankowaniaPage),
             ("serwisy", "Serwisy", "wrench", SerwisyPage), ("koszty", "Koszty", "card", KosztyPage),
             ("prognoza", "Prognoza", "chart", PrognozaPage), ("ustawienia", "Ustawienia", "settings", UstawieniaPage)]

    def __init__(self):
        ctk.set_appearance_mode("dark")
        super().__init__(fg_color=C["bg"])
        self.data = load_data()
        self.title("Cupra Terramar — Dziennik pokładowy")
        scale = ctk.ScalingTracker.get_window_scaling(self)
        w = min(1280, int(self.winfo_screenwidth() / scale * 0.92))
        h = min(820, int(self.winfo_screenheight() / scale * 0.88))
        self.geometry(f"{w}x{h}")
        self.minsize(1100, 700)
        ico = ASSET_DIR / "app.ico"
        if os.name == "nt" and ico.exists():
            self.iconbitmap(str(ico))
        elif (ASSET_DIR / "app_icon.png").exists():
            self.iconphoto(True, tk.PhotoImage(file=str(ASSET_DIR / "app_icon.png")))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self.content = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for key, _, _, cls in self.PAGES:
            page = cls(self)
            page.grid(row=0, column=0, sticky="nsew")
            self.pages[key] = page
        self.dirty = set(self.pages)
        self.current = None
        self.toast = Toast(self)
        self.bind("<Control-n>", lambda e: self.new_entry())
        self.show("dashboard")

    # ---------------- layout ----------------
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, fg_color=C["sidebar"], corner_radius=0, width=232)
        sb.grid(row=0, column=0, sticky="nsw")
        sb.grid_propagate(False)
        sb.pack_propagate(False)
        brand = ctk.CTkFrame(sb, fg_color="transparent")
        brand.pack(fill="x", padx=22, pady=(26, 6))
        emblem = asset_image("emblem.png", 40)
        if emblem:
            ctk.CTkLabel(brand, text="", image=emblem).pack(anchor="w")
        else:
            ctk.CTkLabel(brand, text="", width=40, height=40, corner_radius=10, fg_color=C["copper_soft"],
                         image=icon("car", C["copper"], 20)).pack(anchor="w")
        self.brand_title = label(brand, "", 17, weight="semibold", display=True)
        self.brand_title.pack(anchor="w", pady=(12, 0))
        self.brand_sub = label(brand, "", 11, C["text_faint"])
        self.brand_sub.pack(anchor="w")
        self._refresh_brand()

        ctk.CTkFrame(sb, fg_color=C["line"], height=1).pack(fill="x", padx=22, pady=(18, 14))
        self.nav = {}
        for key, text, ic, _ in self.PAGES:
            b = ctk.CTkButton(sb, text=text, anchor="w", height=42, corner_radius=10, font=font(14),
                              fg_color="transparent", hover_color=C["surface2"], text_color=C["text_dim"],
                              image=icon(ic, C["text_dim"], 18), compound="left",
                              command=lambda k=key: self.show(k))
            b.pack(fill="x", padx=12, pady=2)
            self.nav[key] = (b, ic)

        foot = ctk.CTkFrame(sb, fg_color="transparent")
        foot.pack(side="bottom", fill="x", padx=22, pady=20)
        wm = asset_image("wordmark.png", 11)
        if wm:
            ctk.CTkLabel(foot, text="", image=wm).pack(anchor="w")
        label(foot, "Ctrl+N — nowy wpis", 11, C["text_faint"]).pack(anchor="w", pady=(8, 0))

    def _refresh_brand(self):
        self.brand_title.configure(text=self.data["settings"]["carName"].title()
                                   if self.data["settings"]["carName"].isupper() else self.data["settings"]["carName"])
        self.brand_sub.configure(text=self.data["settings"]["carSubtitle"])

    def show(self, key):
        for k, (b, ic) in self.nav.items():
            active = k == key
            b.configure(fg_color=C["copper_soft"] if active else "transparent",
                        text_color=C["text"] if active else C["text_dim"],
                        image=icon(ic, C["copper"] if active else C["text_dim"], 18),
                        font=font(14, "semibold" if active else "normal"))
        self.current = key
        page = self.pages[key]
        if key in self.dirty:
            page.refresh()
            self.dirty.discard(key)
        page.tkraise()

    def new_entry(self):
        forms = {"tankowania": TankowanieForm, "serwisy": SerwisForm, "koszty": KosztForm}
        forms.get(self.current, TankowanieForm)(self)

    # ---------------- data operations ----------------
    def data_changed(self):
        recalc_tankowania(self.data["tankowania"])
        save_data(self.data)
        self._refresh_brand()
        self.dirty = set(self.pages)
        self.show(self.current)

    def upsert(self, collection, entry, values):
        target = entry if entry is not None else {"id": new_id()}
        target.update(values)
        if entry is None:
            self.data[collection].append(target)
        self.data_changed()
        return target

    def delete_entry(self, collection, entry):
        self.data[collection] = [e for e in self.data[collection] if e["id"] != entry["id"]]
        self.data_changed()

    def confirm_delete(self, collection, entry, on_done=None):
        what = {"tankowania": f"tankowanie z {date_fmt(entry['date'])}",
                "serwisy": f"wpis „{entry.get('description', '')}”",
                "koszty": f"koszt „{entry.get('description', '')}”"}[collection]

        def do():
            if on_done:
                on_done()
            self.delete_entry(collection, entry)
            self.toast.show("Usunięto " + what, "warn")

        ConfirmDialog(self, "Usunąć wpis?", f"Czy na pewno usunąć {what}? Tej operacji nie można cofnąć.",
                      "Usuń", do)

    def export_backup(self):
        path = filedialog.asksaveasfilename(
            parent=self, defaultextension=".json",
            initialfile=f"cupra-terramar-kopia-{dt.date.today().isoformat()}.json",
            filetypes=[("Plik JSON", "*.json")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        self.toast.show("Kopia zapisana: " + os.path.basename(path))

    def import_backup(self):
        path = filedialog.askopenfilename(parent=self, filetypes=[("Plik JSON", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                raw = json.load(f)
        except Exception:
            self.toast.show("Nie udało się wczytać pliku", "error")
            return
        new = sanitize(raw)

        def apply():
            self.data = new
            self.data_changed()
            self.toast.show(f"Wczytano {plural(len(new['tankowania']), 'tankowanie', 'tankowania', 'tankowań')}")

        ConfirmDialog(self, "Wczytać kopię?",
                      f"Obecne dane zostaną zastąpione zawartością pliku {os.path.basename(path)} "
                      f"({plural(len(new['tankowania']), 'tankowanie', 'tankowania', 'tankowań')}, "
                      f"{plural(len(new['serwisy']), 'serwis', 'serwisy', 'serwisów')}, "
                      f"{plural(len(new['koszty']), 'koszt', 'koszty', 'kosztów')}).",
                      "Wczytaj", apply, danger=False)


if __name__ == "__main__":
    app = CarApp()
    app.mainloop()
