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
import queue
import sys
import threading
import time
import uuid
import webbrowser
import datetime as dt
import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageTk

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

FUEL_TYPES = ["Pb95", "Pb98"]
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


_TK_ICON_CACHE = {}


def tk_icon(widget, name, color=C["text_dim"], size=16):
    """The same glyph as icon(), as a PhotoImage for plain tk widgets (scaled like CTk images)."""
    scale = ctk.ScalingTracker.get_widget_scaling(widget)
    key = (name, color, size, scale)
    if key not in _TK_ICON_CACHE:
        img = icon(name, color, size)
        px_size = round(size * scale)
        _TK_ICON_CACHE[key] = (ImageTk.PhotoImage(img.cget("light_image").resize((px_size, px_size), Image.LANCZOS))
                               if img is not None else None)
    return _TK_ICON_CACHE[key]


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


class ScrollArea(ctk.CTkScrollableFrame):
    """Scrollable column whose content follows the new width only once a resize settles:
    every row redraws its rounded background on a width change, which made dragging the window stutter."""

    def __init__(self, master):
        super().__init__(master, fg_color="transparent", scrollbar_button_color=C["line"],
                         scrollbar_button_hover_color=C["text_faint"])
        self._fit_job = None
        self._fitted = False
        self._parent_canvas.bind("<Configure>", self._fit_later)

    def _fit_later(self, event):
        if not self._fitted:  # first layout: fit at once, so the list never shows at its natural width
            self._fitted = True
            return self._fit_frame_dimensions_to_canvas(event)
        if self._fit_job is not None:
            self.after_cancel(self._fit_job)
        self._fit_job = self.after(120, lambda: self._fit_now(event))

    def _fit_now(self, event):
        self._fit_job = None
        if self.winfo_exists():
            self._fit_frame_dimensions_to_canvas(event)


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
def style_titlebar(window, color):
    """Dark title bar (Windows 10+) in the given colour (Windows 11), applied before the window is shown.

    Replaces CTk's own approach, which hides and re-shows the window and makes it flash white."""
    if os.name != "nt":
        return
    try:
        import ctypes
        window.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        dwm = ctypes.windll.dwmapi
        on = ctypes.c_int(1)
        for attr in (20, 19):  # DWMWA_USE_IMMERSIVE_DARK_MODE (and its pre-20H1 id)
            if dwm.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(on), ctypes.sizeof(on)) == 0:
                break
        r, g, b = _rgb(color)
        colorref = ctypes.c_int(r | g << 8 | b << 16)
        dwm.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(colorref), ctypes.sizeof(colorref))  # DWMWA_CAPTION_COLOR
    except Exception:
        pass


def set_app_icon(window):
    ico = ASSET_DIR / "app.ico"
    if os.name == "nt" and ico.exists():
        window.iconbitmap(str(ico))  # also stops CTk from installing its default icon later


class Dialog(ctk.CTkToplevel):
    """Modal dialog centred over the main window, Esc closes."""
    _deactivate_windows_window_header_manipulation = True  # see style_titlebar()

    def __init__(self, app, title, icon_name=None, width=480):
        super().__init__(app, fg_color=C["surface"])
        self.app = app
        self.withdraw()  # shown in _present() once laid out, so it never appears half-drawn
        self.title(title)
        self.resizable(False, False)
        self.transient(app)
        set_app_icon(self)

        bg = C["surface"]
        head = tk.Frame(self, bg=bg)
        head.pack(fill="x", padx=24, pady=(20, 4))
        if icon_name:
            chip = ctk.CTkLabel(head, text="", width=36, height=36, corner_radius=10, fg_color=C["copper_soft"],
                                image=icon(icon_name, C["copper"], 18))
            chip.pack(side="left", padx=(0, 12))
        tk.Label(head, text=title, fg=C["text"], bg=bg, font=tk_font(self, 18, "semibold", True)).pack(side="left")
        # no close button here: the title bar already has one (and Esc / Anuluj close too)

        self.body = tk.Frame(self, bg=bg)
        self.body.pack(fill="both", expand=True, padx=24, pady=(8, 0))
        tk.Frame(self.body, bg=bg, width=round(width * ctk.ScalingTracker.get_widget_scaling(self)),
                 height=1).pack()  # minimum width
        self.footer = tk.Frame(self, bg=bg)
        self.footer.pack(fill="x", padx=24, pady=(16, 20))

        self.bind("<Escape>", lambda e: self.on_escape())
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.after(1, self._present)

    def on_escape(self):
        self.close()

    def _present(self):
        style_titlebar(self, C["surface"])
        self.update_idletasks()
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        ax, ay, aw, ah = self.app.winfo_rootx(), self.app.winfo_rooty(), self.app.winfo_width(), self.app.winfo_height()
        self.geometry(f"+{max(0, ax + (aw - w) // 2)}+{max(0, ay + (ah - h) // 3)}")
        self.deiconify()
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


class CalendarPopover(ctk.CTkFrame):
    """Month grid that drops down inside the form (no separate window). Day cells are plain tk.Labels:
    42 CTk buttons took about half a second to build."""
    BG = C["surface2"]

    def __init__(self, window, anchor_widget, initial_iso, on_pick):
        super().__init__(window, fg_color=self.BG, corner_radius=14, border_width=1, border_color=C["line"])
        try:
            d = dt.date.fromisoformat(initial_iso)
        except (TypeError, ValueError):
            d = dt.date.today()
        self.selected = d
        self.year, self.month = d.year, d.month
        self.on_pick = on_pick
        inner = tk.Frame(self, bg=self.BG)
        inner.pack(padx=12, pady=12)
        nav = tk.Frame(inner, bg=self.BG)
        nav.pack(fill="x")
        icon_button(nav, "prev", lambda: self.shift(-1), size=30).pack(side="left")
        self.title_lbl = tk.Label(nav, fg=C["text"], bg=self.BG, font=tk_font(self, 14, "semibold"))
        self.title_lbl.pack(side="left", expand=True)
        icon_button(nav, "next", lambda: self.shift(1), size=30).pack(side="right")
        self.grid_frame = tk.Frame(inner, bg=self.BG)
        self.grid_frame.pack(pady=(8, 4))
        today = tk.Label(inner, text="Dziś", fg=C["copper"], bg=self.BG, cursor="hand2",
                         font=tk_font(self, 12, "semibold"))
        today.pack(anchor="w", padx=4)
        today.bind("<Button-1>", lambda e: self.pick(dt.date.today()))
        self._cell_font = tk_font(self, 12)
        self._cell_bold = tk_font(self, 12, "semibold")
        self._head_font = tk_font(self, 11)
        self.draw()
        self.place(in_=anchor_widget, relx=1.0, rely=1.0, y=6, anchor="ne")
        self.lift()

    def shift(self, delta):
        m = self.month - 1 + delta
        self.year, self.month = self.year + m // 12, m % 12 + 1
        self.draw()

    def pick(self, d):
        self.destroy()
        self.on_pick(d.isoformat())

    def draw(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.title_lbl.configure(text=f"{MONTHS_FULL[self.month - 1]} {self.year}")
        for i, name in enumerate(["Pn", "Wt", "Śr", "Cz", "Pt", "Sb", "Nd"]):
            tk.Label(self.grid_frame, text=name, fg=C["text_faint"], bg=self.BG, width=4,
                     font=self._head_font).grid(row=0, column=i, pady=(0, 4))
        first = dt.date(self.year, self.month, 1)
        start = first - dt.timedelta(days=first.weekday())
        today = dt.date.today()
        for i in range(42):
            d = start + dt.timedelta(days=i)
            is_sel = d == self.selected
            fg = "#140D08" if is_sel else (C["copper"] if d == today else
                                           (C["text"] if d.month == self.month else C["text_faint"]))
            bg = C["copper"] if is_sel else self.BG
            cell = tk.Label(self.grid_frame, text=str(d.day), fg=fg, bg=bg, width=4, pady=5, cursor="hand2",
                            font=self._cell_bold if is_sel or d == today else self._cell_font)
            cell.grid(row=1 + i // 7, column=i % 7, padx=1, pady=1)
            cell.bind("<Button-1>", lambda e, d=d: self.pick(d))
            if not is_sel:
                cell.bind("<Enter>", lambda e, c=cell: c.configure(bg=C["surface3"]))
                cell.bind("<Leave>", lambda e, c=cell: c.configure(bg=self.BG))


class Field:
    """Labelled entry with optional unit suffix, hint and inline error message.
    Only the entry is a CTk widget; labels and containers are plain tk (much cheaper to create)."""

    def __init__(self, parent, title, value="", suffix=None, hint=None, placeholder="", bg=C["surface"]):
        self.frame = tk.Frame(parent, bg=bg)
        top = tk.Frame(self.frame, bg=bg)
        top.pack(fill="x")
        tk.Label(top, text=title, fg=C["text_dim"], bg=bg, font=tk_font(parent, 12)).pack(side="left")
        # CTkEntry ignores placeholder_text when a textvariable is set, so the example goes next to the title
        self.hint = tk.Label(top, text=hint or placeholder, fg=C["text_faint"], bg=bg, font=tk_font(parent, 11))
        self.hint.pack(side="right")
        self.var = tk.StringVar(value=value)
        self.row = tk.Frame(self.frame, bg=bg)
        self.row.pack(fill="x", pady=(4, 0))
        self.entry = ctk.CTkEntry(self.row, textvariable=self.var, height=40, corner_radius=10, border_width=1,
                                  fg_color=C["surface2"], border_color=C["line"], text_color=C["text"],
                                  font=font(14))
        self.entry.pack(side="left", fill="x", expand=True)
        if suffix:
            tk.Label(self.entry, text=suffix, fg=C["text_faint"], bg=C["surface2"],
                     font=tk_font(parent, 12)).place(relx=1.0, rely=0.5, x=-12, anchor="e")
        self.error = tk.Label(self.frame, fg=C["red"], bg=bg, font=tk_font(parent, 11))
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

        self.calendar = None

    def open_calendar(self):
        if self.calendar is not None and self.calendar.winfo_exists():
            return self.close_calendar()
        try:
            iso = parse_date(self.get())
        except ValueError:
            iso = None
        self.calendar = CalendarPopover(self.frame.winfo_toplevel(), self.row, iso, lambda v: self.set(date_fmt(v)))

    def close_calendar(self):
        """Returns True if a calendar was open (Esc then closes only the calendar)."""
        if self.calendar is not None and self.calendar.winfo_exists():
            self.calendar.destroy()
            self.calendar = None
            return True
        return False

    def value(self):
        return parse_date(self.get())


class EntryForm(Dialog):
    """Base for add/edit forms. Subclasses build fields and implement collect()."""
    collection = None
    noun = None  # e.g. "tankowanie"

    def __init__(self, app, entry, title_new, title_edit, icon_name):
        self.entry = entry
        # the entry as it was when the form opened: saving writes only what the user changed since then
        self.initial = json.loads(json.dumps(entry)) if entry is not None else None
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

    def on_escape(self):
        f_date = getattr(self, "f_date", None)
        if f_date is not None and f_date.close_calendar():
            return
        self.close()

    def focus_first(self):
        first = getattr(self, "first_field", None)
        if first is not None:
            first.entry.focus_set()
            first.entry._entry.icursor("end")

    def save(self):
        values = self.collect()
        if values is None:
            return False
        saved = self.app.upsert(self.collection, self.entry, values, initial=self.initial)
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
    row = tk.Frame(parent, bg=C["surface"])
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
        tk.Label(self.body, text="Paliwo", fg=C["text_dim"], bg=C["surface"],
                 font=tk_font(self, 12)).pack(anchor="w")
        fuel = e.get("fuelType", (last or {}).get("fuelType", "Pb98"))
        self.v_fuel = tk.StringVar(value=fuel)
        # an older entry may use a type that is no longer offered; keep it selectable for that entry
        fuels = FUEL_TYPES + ([fuel] if fuel not in FUEL_TYPES else [])
        ctk.CTkSegmentedButton(self.body, values=fuels, variable=self.v_fuel, height=36, corner_radius=10,
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
        bg = C["surface2"]
        for i, (key, title) in enumerate((("price", "Cena za litr"), ("dist", "Dystans"), ("cons", "Spalanie"))):
            cell = tk.Frame(self.summary, bg=bg)
            cell.grid(row=0, column=i, sticky="w", padx=14, pady=10)
            tk.Label(cell, text=title, fg=C["text_faint"], bg=bg, font=tk_font(self, 11)).pack(anchor="w")
            self.sum_vals[key] = tk.Label(cell, text="—", fg=C["text"], bg=bg,
                                          font=tk_font(self, 15, "semibold", True))
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
                                        fg=C["red"] if dist is not None and dist <= 0 else C["text"])
        cons = liters / dist * 100 if liters and dist and dist > 0 else None
        st = status_of(cons, self.app.data["settings"])
        self.sum_vals["cons"].configure(text=f"{numf(cons, 2)} l/100" if cons else "—",
                                        fg=st[1] if st else C["text"])

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
        # matplotlib redraws the whole figure on every <Configure>; while the window is being dragged
        # that is dozens of full renders, so the resize is applied once the size settles
        w.bind("<Configure>", self._on_configure)
        self._resize_event = None
        self._resize_job = None
        self.canvas.mpl_connect("motion_notify_event", self._hover)
        self.canvas.mpl_connect("figure_leave_event", lambda e: self._show_point(None))
        self.active = None
        self._marks = None  # bar patches or the scatter collection, recoloured on hover without a rebuild

    def _on_configure(self, event):
        self._resize_event = event
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(150, self._apply_resize)

    def _apply_resize(self):
        self._resize_job = None
        if self._resize_event is not None and self.winfo_exists():
            self.canvas.resize(self._resize_event)

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
            self._marks = None
            self.canvas.draw_idle()
            return
        if self.kind == "bar":
            self._marks = ax.bar(xs, self.values, color=C["copper_dim"], width=0.62, zorder=2).patches
        else:
            ax.fill_between(xs, self.values, min(self.values) * 0.92, color=self.color, alpha=0.10, zorder=1)
            ax.plot(xs, self.values, color=self.color, linewidth=2.2, zorder=2)
            self._marks = ax.scatter(xs, self.values, s=14, color=self.color,
                                     edgecolor=C["surface"], linewidth=1.5, zorder=3)
            lo = min(self.values + [g[0] for g in self.guides])
            top = max(self.values + [g[0] for g in self.guides])
            ax.set_ylim(lo - (top - lo) * 0.15, top + (top - lo) * 0.15)
        self._highlight()
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

    def _highlight(self):
        if not self.values or self._marks is None:
            return
        hi = self.active if self.active is not None else len(self.values) - 1
        if self.kind == "bar":
            for i, patch in enumerate(self._marks):
                patch.set_facecolor(self.color if i == hi else C["copper_dim"])
        else:
            self._marks.set_sizes([42 if i == hi else 14 for i in range(len(self.values))])

    def _show_point(self, i):
        if i != self.active:
            self.active = i
            self._highlight()
            self.canvas.draw_idle()
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
        self.list = ScrollArea(self)
        self.list.pack(fill="both", expand=True, padx=(32, 18), pady=(0, 20))
        self.container = None
        self.items = {}   # key -> (signature, widget) for what is on screen
        self.rows = {}    # entry id -> row widget
        self._generation = 0

    def sort_key(self, e):
        return e["date"]

    def entry_by_id(self, eid):
        return next((x for x in self.app.data[self.collection] if x["id"] == eid), None)

    FIRST_BATCH, BATCH = 10, 8
    HEADER_PACK = dict(fill="x", pady=(14, 6), padx=(4, 16))
    ROW_PACK = dict(fill="x", pady=(0, 6), padx=(0, 12))

    def _layout(self, entries):
        """What should be on screen, in order: (key, signature, builder, pack options)."""
        items, month = [], None
        for e in entries:
            if month_key(e["date"]) != month:
                month = month_key(e["date"])
                group = [x for x in entries if month_key(x["date"]) == month]
                items.append(("h:" + month, (month, self.group_summary(group)),
                              lambda m=month, g=group: self.month_header(m, g), self.HEADER_PACK))
            items.append(("r:" + e["id"], (e["date"], self.row_text(e), self.row_right(e)),
                          lambda e=e: self.make_row(e), self.ROW_PACK))
        return items

    def refresh(self):
        """Bring the list up to date. After an edit only the rows whose content changed are rebuilt
        (creating and destroying CTk widgets is what makes Tk slow); a first build or a large change
        renders the first rows at once and the rest in small batches."""
        self._generation += 1
        gen = self._generation
        entries = sorted(self.app.data[self.collection], key=self.sort_key, reverse=True)
        self.subtitle_lbl.configure(text=self.summary(entries))
        layout = self._layout(entries) if entries else []
        changed = [it for it in layout if self.items.get(it[0], (None,))[0] != it[1]]

        if self.container is None or not entries or len(changed) > self.FIRST_BATCH:
            self._rebuild(layout, gen)
            return

        wanted = {key for key, *_ in layout}
        for key, (sig, w) in list(self.items.items()):
            if key not in wanted or any(key == c[0] for c in changed):
                w.destroy()
                del self.items[key]
        for key, sig, builder, _ in changed:
            self.items[key] = (sig, builder())
        for w in self.container.pack_slaves():
            w.pack_forget()
        for key, _, _, pack_kw in layout:
            self.items[key][1].pack(**pack_kw)
        self.rows = {k[2:]: w for k, (_, w) in self.items.items() if k.startswith("r:")}

    def _rebuild(self, layout, gen):
        old = self.container
        if old is not None:
            old.pack_forget()
            self.after(200, old.destroy)  # destroying many CTk widgets is slow; do it after the new list shows
        self.container = tk.Frame(self.list, bg=C["bg"])
        self.container.pack(fill="both", expand=True)
        self.items, self.rows = {}, {}
        if not layout:
            tk.Label(self.container, text=self.empty_text, fg=C["text_faint"], bg=C["bg"],
                     font=tk_font(self, 14)).pack(pady=60)
            return

        def run(start, count):
            if gen != self._generation or not self.winfo_exists():
                return  # a newer refresh started
            for key, sig, builder, pack_kw in layout[start:start + count]:
                w = builder()
                w.pack(**pack_kw)
                self.items[key] = (sig, w)
                if key.startswith("r:"):
                    self.rows[key[2:]] = w
            if start + count < len(layout):
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
        h = tk.Frame(self.container, bg=C["bg"])
        tk.Label(h, text=f"{MONTHS_FULL[int(m) - 1]} {y}", fg=C["text_dim"], bg=C["bg"],
                 font=tk_font(h, 13, "semibold")).pack(side="left")
        tk.Label(h, text=self.group_summary(group), fg=C["text_faint"], bg=C["bg"],
                 font=tk_font(h, 12)).pack(side="right")
        return h

    def make_row(self, e):
        # rounded parts are CTk widgets; plain text uses tk.Label, which is several times cheaper to create
        eid = e["id"]  # handlers look the entry up by id: the row may outlive the dict (e.g. after an import)
        row = ctk.CTkFrame(self.container, fg_color=C["surface"], corner_radius=14)
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
        buttons = []
        def edit():
            current = self.entry_by_id(eid)
            if current is not None:
                self.form(self.app, current)

        def delete():
            current = self.entry_by_id(eid)
            if current is not None:
                self.app.confirm_delete(self.collection, current)

        for name, cmd, color in (("edit", edit, C["text_dim"]), ("delete", delete, C["text_faint"])):
            b = tk.Label(actions, image=tk_icon(row, name, color), bg=C["surface"], cursor="hand2", padx=9, pady=9)
            b.pack(side="left", padx=(4, 0))
            b.bind("<Button-1>", lambda ev, cmd=cmd: cmd())
            tinted.append(b)
            buttons.append(b)

        right = tk_frame(row)
        right.pack(side="right", padx=(10, 4))
        amount, badge = self.row_right(e)
        text(right, amount, 15, weight="semibold", display=True).pack(anchor="e")
        if badge:
            pill(right, *badge).pack(anchor="e", pady=(3, 0))

        state = {"bg": C["surface"]}

        def paint(color):
            if state["bg"] == color:
                return
            state["bg"] = color
            row.configure(fg_color=color)
            for w in tinted:
                w.configure(bg=color)
            for w in right.winfo_children():
                if isinstance(w, ctk.CTkBaseClass):
                    w.configure(bg_color=color)

        def enter(_):
            paint(C["surface3"])

        def leave(ev):
            w = row.winfo_containing(ev.x_root, ev.y_root)
            if w is None or not is_descendant(w, row):
                paint(C["surface"])

        bind_tree(row, "<Enter>", enter)
        bind_tree(row, "<Leave>", leave)
        for b in buttons:  # bound after the row handlers so the button highlight wins
            b.bind("<Enter>", lambda ev, b=b: b.configure(bg=C["line"]), add="+")
            b.bind("<Leave>", lambda ev, b=b: b.configure(bg=state["bg"]), add="+")
        bind_tree(mid, "<Double-Button-1>", lambda ev: edit())
        bind_tree(db, "<Double-Button-1>", lambda ev: edit())
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
        scroll = ScrollArea(self)
        scroll.pack(fill="both", expand=True, padx=(32, 18), pady=(0, 20))
        grid = ctk.CTkFrame(scroll, fg_color="transparent")
        grid.pack(fill="x", padx=(0, 12))
        grid.columnconfigure((0, 1), weight=1, uniform="s")

        def section(r, c, title, desc, ic, span=1):
            box = card(grid)
            box.grid(row=r, column=c, columnspan=span, sticky="nsew",
                     padx=(0 if c == 0 else 6, 0 if c + span == 2 else 6), pady=(0, 12))
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

        sy = section(2, 0, "Arkusz Google", "wspólne dane z aplikacją na telefon — „Cupra Terramar - dane”",
                     "export", span=2)
        info = ctk.CTkFrame(sy, fg_color="transparent")
        info.pack(fill="x")
        self.sync_vals = {}
        for i, (key, title) in enumerate((("state", "Stan"), ("last", "Ostatnia synchronizacja"),
                                          ("pending", "Zmiany do wysłania"))):
            cell = ctk.CTkFrame(info, fg_color="transparent")
            cell.grid(row=0, column=i, sticky="w", padx=(0, 40))
            label(cell, title, 11, C["text_faint"]).pack(anchor="w")
            self.sync_vals[key] = label(cell, "—", 14, weight="semibold")
            self.sync_vals[key].pack(anchor="w")
        self.sync_msg = label(sy, "", 12, C["amber"], wraplength=760, justify="left", anchor="w")
        self.sync_buttons = ctk.CTkFrame(sy, fg_color="transparent")
        self.sync_buttons.pack(fill="x", pady=(12, 12))

    def _fields(self):
        """(setting key, field, value as shown in the field)"""
        s = self.app.data["settings"]
        return ((("carName", self.f_name, s["carName"]), ("carSubtitle", self.f_sub, s["carSubtitle"]),
                 ("carPrice", self.f_price, num_in(s["carPrice"])),
                 ("consumptionOkTo", self.f_ok, num_in(s["consumptionOkTo"])),
                 ("consumptionHighFrom", self.f_high, num_in(s["consumptionHighFrom"])),
                 ("monthlyKmPlan", self.f_km, num_in(s["monthlyKmPlan"])),
                 ("fuelPriceGrowth", self.f_growth, num_in(round(s["fuelPriceGrowth"] * 100, 4)))))

    def refresh(self):
        # values synced from the sheet replace a field only if the user has not started editing it
        loaded = getattr(self, "loaded", {})
        for key, f, v in self._fields():
            if key not in loaded or f.get() == loaded[key]:
                f.set(v)
                f.set_error(None)
                loaded[key] = v
        self.loaded = loaded
        self.refresh_sync()

    def refresh_sync(self):
        app, st = self.app, self.app.sync_state
        state, msg = app.sync_status
        self.sync_vals["state"].configure(text=sync_label(app), text_color=sync_color(app))
        self.sync_vals["last"].configure(text=time.strftime("%d.%m, %H:%M", time.localtime(st["lastSync"]))
                                         if st.get("lastSync") else "jeszcze nie")
        self.sync_vals["pending"].configure(text=str(len(st["ops"])))
        if msg:
            self.sync_msg.configure(text=msg, text_color=C["red"] if state == "error" else C["amber"])
            self.sync_msg.pack(anchor="w", pady=(10, 0), before=self.sync_buttons)
        else:
            self.sync_msg.pack_forget()
        for w in self.sync_buttons.winfo_children():
            w.destroy()
        if not st["connected"]:
            label(self.sync_buttons, "Przy pierwszym połączeniu wpisy, których nie ma w arkuszu, zostaną do niego dopisane; "
                  "te same wpisy są rozpoznawane po treści.", 12, C["text_dim"], wraplength=560,
                  justify="left").pack(side="left")
            primary_button(self.sync_buttons, "Połącz z Google", app.sync_connect, "export").pack(side="right")
            return
        if state == "auth":
            primary_button(self.sync_buttons, "Zaloguj do Google", app.sync_connect, "export").pack(side="left")
        else:
            primary_button(self.sync_buttons, "Synchronizuj teraz", app.sync_now, "import").pack(side="left")
        ghost_button(self.sync_buttons, "Otwórz arkusz",
                     lambda: webbrowser.open(f"https://docs.google.com/spreadsheets/d/{sheet_id()}/edit")
                     ).pack(side="left", padx=(8, 0))
        ctk.CTkButton(self.sync_buttons, text="Odłącz", width=90, height=38, corner_radius=10, fg_color="transparent",
                      hover_color=C["surface3"], text_color=C["text_faint"], font=font(13),
                      command=app.sync_disconnect).pack(side="right")

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
        new = {"carName": self.f_name.get() or "MOJE AUTO", "carSubtitle": self.f_sub.get() or "DZIENNIK POKŁADOWY",
               "carPrice": price, "consumptionOkTo": ok_to, "consumptionHighFrom": high,
               "monthlyKmPlan": km, "fuelPriceGrowth": growth / 100}
        # only the fields edited on this page; the rest keep their current (possibly freshly synced) values
        edited = [key for key, f, _ in self._fields() if f.get() != self.loaded.get(key)]
        self.app.data["settings"].update({k: new[k] for k in edited})
        self.loaded = {}  # reload every field from the saved settings
        self.app.data_changed()
        self.app.toast.show("Ustawienia zapisane")
        return True


# ----------------------------------------------------------------------
# GOOGLE SHEETS SYNC (same rules as the web app)
# ----------------------------------------------------------------------
# The Google Sheet is the shared source of truth. Local changes are queued as numbered operations; a sync
# pulls the sheet, applies the queue on top, recomputes distances, writes back only the tabs that changed
# and adopts the result. Network work runs in a background thread; results reach Tk through a queue.
GOOGLE_SHEET_ID = "1qIYl3xkVN4EK62Zd_z_w_QyJvh-HVQv5-0ZD4WCvWgw"
GOOGLE_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CLIENT_SECRET_FILE = os.path.join(DATA_DIR, "client_secret.json")
TOKEN_FILE = os.path.join(DATA_DIR, "google_token.json")
SYNC_FILE = os.path.join(DATA_DIR, "sync.json")
COLLECTIONS = ("tankowania", "serwisy", "koszty")
SETTING_KEYS = ("carName", "carSubtitle", "consumptionOkTo", "consumptionHighFrom", "fuelPriceGrowth",
                "monthlyKmPlan", "carPrice")


def sheet_id():
    return os.environ.get("CUPRA_SHEET_ID") or GOOGLE_SHEET_ID  # override for tests on a copy


class SyncAuthError(Exception):
    pass


class SyncDataError(Exception):
    pass


def load_sync_state():
    try:
        with open(SYNC_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    except Exception:
        state = {}
    return {"connected": bool(state.get("connected")), "firstDone": bool(state.get("firstDone")),
            "ops": state.get("ops") or [], "seq": int(state.get("seq") or 0), "lastSync": state.get("lastSync")}


def save_sync_state(state):
    os.makedirs(DATA_DIR, exist_ok=True)
    tmp = SYNC_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)
    os.replace(tmp, SYNC_FILE)


# --- auth (google-auth-oauthlib, imported lazily so the app runs without it) ---
def google_credentials(interactive=False):
    """Stored credentials, refreshed if needed; with interactive=True the browser sign-in is started."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
    except ImportError:
        raise SyncAuthError("Brak biblioteki google-auth-oauthlib (py -m pip install -r requirements.txt).")
    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, GOOGLE_SCOPES)
        except Exception:
            creds = None
    if creds and not creds.valid and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception:
            creds = None
    if creds and creds.valid:
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        return creds
    if not interactive:
        raise SyncAuthError("Zaloguj się do Google, żeby zsynchronizować dane.")
    if not os.path.exists(CLIENT_SECRET_FILE):
        raise SyncAuthError(f"Brak pliku {CLIENT_SECRET_FILE} (klient OAuth „Cupra desktop”).")
    from google_auth_oauthlib.flow import InstalledAppFlow
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, GOOGLE_SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True, timeout_seconds=300,
                                  success_message="Gotowe — możesz zamknąć tę kartę i wrócić do aplikacji.")
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(creds.to_json())
    return creds


class SheetsClient:
    def __init__(self, creds):
        from google.auth.transport.requests import AuthorizedSession
        self.session = AuthorizedSession(creds)
        self.base = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id()}"

    def _call(self, method, path, **kw):
        r = self.session.request(method, self.base + path, timeout=30, **kw)
        if r.status_code == 401:
            raise SyncAuthError("Sesja Google wygasła — zaloguj się ponownie.")
        if not r.ok:
            try:
                msg = r.json()["error"]["message"]
            except Exception:
                msg = r.text[:200]
            raise SyncDataError(f"Błąd Google Sheets ({r.status_code}): {msg}")
        return r.json()

    def batch_get(self, ranges):
        params = [("ranges", x) for x in ranges] + [("valueRenderOption", "UNFORMATTED_VALUE"),
                                                    ("dateTimeRenderOption", "SERIAL_NUMBER")]
        return self._call("GET", "/values:batchGet", params=params)["valueRanges"]

    def batch_clear(self, ranges):
        self._call("POST", "/values:batchClear", json={"ranges": ranges})

    def batch_update(self, data):
        self._call("POST", "/values:batchUpdate", json={"valueInputOption": "RAW", "data": data})


# --- sheet <-> app rows ---
SERIAL_EPOCH = dt.date(1899, 12, 30)


def iso_to_serial(iso):
    return (dt.date.fromisoformat(iso) - SERIAL_EPOCH).days


def cell_date(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
        return (SERIAL_EPOCH + dt.timedelta(days=round(v))).isoformat()
    s = cell_text(v)
    try:
        return parse_date(s) if s else None
    except ValueError:
        return None


def cell_number(v, optional=False):
    """Number from a cell; None if empty and optional; NaN if unreadable."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return v
    if cell_text(v) == "":
        return None if optional else float("nan")
    try:
        return parse_number(str(v))
    except ValueError:
        return float("nan")


def cell_text(v):
    return "" if v is None else str(v).strip()


def is_nan(v):
    return isinstance(v, float) and math.isnan(v)


def yes(v):
    return cell_text(v).lower() in ("tak", "t", "yes", "true", "1")


def _num_or_blank(v):
    return "" if v is None else v


def _tank_from(r):
    e = {"id": cell_text(r[0]), "date": cell_date(r[1]), "fuelType": cell_text(r[2]) or "Pb98",
         "liters": cell_number(r[3]), "cost": cell_number(r[4]), "mileage": cell_number(r[6]),
         "note": cell_text(r[9])}
    if not e["date"] or is_nan(e["liters"]) or not e["liters"] > 0 or is_nan(e["cost"]) or is_nan(e["mileage"]):
        return None
    if isinstance(e["mileage"], float) and e["mileage"].is_integer():
        e["mileage"] = int(e["mileage"])
    # as stored in the sheet; recalc_tankowania / with_prices bring them in line afterwards
    e.update(pricePerL=cell_number(r[5], True), distance=cell_number(r[7], True), consumption=cell_number(r[8], True))
    return e


def _serw_from(r):
    price = cell_number(r[4], True)
    price = 0 if price is None else price
    warranty = yes(r[5])
    mileage = cell_number(r[2], True)
    e = {"id": cell_text(r[0]), "date": cell_date(r[1]), "mileage": mileage, "description": cell_text(r[3]),
         "price": price, "warranty": warranty, "paidCost": 0 if warranty else price, "note": cell_text(r[7])}
    if not e["date"] or not e["description"] or is_nan(price) or is_nan(mileage):
        return None
    return e


def _koszt_from(r):
    typ = cell_text(r[2]) or "Inne"
    e = {"id": cell_text(r[0]), "date": cell_date(r[1]), "type": typ, "description": cell_text(r[3]) or typ,
         "amount": cell_number(r[4]), "oneTime": yes(r[5]) if cell_text(r[5]) else True, "note": cell_text(r[6])}
    if not e["date"] or is_nan(e["amount"]):
        return None
    return e


SHEET_TABLES = [
    {"coll": "tankowania", "tab": "Tankowania", "last": "J", "width": 10,
     "key": lambda t: (t["date"], t["mileage"]),
     "to_row": lambda t: [t["id"], iso_to_serial(t["date"]), t["fuelType"], t["liters"], t["cost"], t["pricePerL"],
                          t["mileage"], _num_or_blank(t.get("distance")), _num_or_blank(t.get("consumption")),
                          t.get("note") or ""],
     "from_row": _tank_from},
    {"coll": "serwisy", "tab": "Serwisy", "last": "H", "width": 8,
     "key": lambda s: s["date"],
     "to_row": lambda s: [s["id"], iso_to_serial(s["date"]), _num_or_blank(s.get("mileage")), s["description"],
                          s["price"], "TAK" if s["warranty"] else "NIE", s["paidCost"], s.get("note") or ""],
     "from_row": _serw_from},
    {"coll": "koszty", "tab": "Koszty", "last": "G", "width": 7,
     "key": lambda k: k["date"],
     "to_row": lambda k: [k["id"], iso_to_serial(k["date"]), k["type"], k["description"], k["amount"],
                          "NIE" if k.get("oneTime") is False else "TAK", k.get("note") or ""],
     "from_row": _koszt_from},
]

# the same real event recorded on two devices (different IDs)
SAME_EVENT = {
    "tankowania": lambda a, b: a["mileage"] == b["mileage"],
    "serwisy": lambda a, b: a["date"] == b["date"] and (
        a["description"] == b["description"] or bool(a.get("mileage")) and a.get("mileage") == b.get("mileage")),
    "koszty": lambda a, b: a["date"] == b["date"] and a["type"] == b["type"] and a["amount"] == b["amount"],
}


def pull_sheet(client):
    ranges = [f"{t['tab']}!A2:{t['last']}" for t in SHEET_TABLES] + ["Ustawienia!A2:B"]
    res = client.batch_get(ranges)
    out = {"data": {"settings": {}}, "rows": {}, "needs_rewrite": set(), "invalid": [], "setting_rows": {}}
    for t, vr in zip(SHEET_TABLES, res):
        rows = vr.get("values", [])
        out["rows"][t["tab"]] = len(rows)
        out["data"][t["coll"]] = []
        for j, r in enumerate(rows):
            r = list(r) + [""] * (t["width"] - len(r))
            if not any(cell_text(c) for c in r):
                continue
            e = t["from_row"](r)
            if e is None:
                out["invalid"].append(f"{t['tab']}, wiersz {j + 2}")
                continue
            if not e["id"]:
                e["id"] = new_id()  # typed by hand in the sheet: give it an ID and write it back
                out["needs_rewrite"].add(t["tab"])
            out["data"][t["coll"]].append(e)
    for j, r in enumerate(res[len(SHEET_TABLES)].get("values", [])):
        key = cell_text(r[0]) if r else ""
        if key not in SETTING_KEYS:
            continue
        out["setting_rows"][key] = j + 2
        v = r[1] if len(r) > 1 else ""
        out["data"]["settings"][key] = cell_text(v) if key in ("carName", "carSubtitle") else cell_number(v)
    return out


# recomputed from the other fields, so they never decide what a change overwrites
DERIVED_FIELDS = ("distance", "consumption", "pricePerL", "paidCost")


def same_value(a, b):
    return ("" if a is None else a) == ("" if b is None else b)


def changed_fields(a, b):
    return [k for k in {**a, **b} if k not in DERIVED_FIELDS and not same_value(a.get(k), b.get(k))]


def diff_ops(prev, nxt):
    """An edit records only the fields that changed: applied to the sheet's current version of the entry,
    it cannot undo a change made to another field on another device in the meantime."""
    ops = []
    for coll in COLLECTIONS:
        before = {e["id"]: e for e in prev.get(coll, [])}
        after = {e["id"]: e for e in nxt[coll]}
        for eid, e in after.items():
            entry = json.loads(json.dumps(e))
            if eid not in before:
                ops.append({"type": "upsert", "coll": coll, "entry": entry})
            else:
                fields = changed_fields(before[eid], e)
                if fields:
                    ops.append({"type": "upsert", "coll": coll, "entry": entry, "fields": fields})
        for eid in before:
            if eid not in after:
                ops.append({"type": "delete", "coll": coll, "id": eid})
    keys = [k for k in nxt["settings"] if not same_value(prev.get("settings", {}).get(k), nxt["settings"][k])]
    if keys:
        ops.append({"type": "settings", "settings": {k: nxt["settings"][k] for k in keys}})
    return ops


def op_key(op):
    if op["type"] == "settings":
        return "settings"
    return f"{op['coll']}:{op['id'] if op['type'] == 'delete' else op['entry']['id']}"


def compact_ops(ops):
    """One operation per entry: the latest wins, edits of the same entry merge their field lists."""
    last = {}
    for op in ops:
        key = op_key(op)
        prev = last.pop(key, None)
        merged = op
        if prev and prev["type"] == op["type"] == "upsert":
            merged = dict(op)
            if prev.get("fields") is not None and op.get("fields") is not None:
                merged["fields"] = list(dict.fromkeys(prev["fields"] + op["fields"]))
            else:
                merged.pop("fields", None)
        elif prev and prev["type"] == op["type"] == "settings":
            merged = {**op, "settings": {**prev["settings"], **op["settings"]}}
        last[key] = merged
    return list(last.values())


def apply_ops(data, ops):
    d = {c: [dict(e) for e in data[c]] for c in COLLECTIONS}
    d["settings"] = dict(data["settings"])
    for op in ops:
        if op["type"] == "settings":
            d["settings"].update(op["settings"])
        elif op["type"] == "delete":
            d[op["coll"]] = [e for e in d[op["coll"]] if e["id"] != op["id"]]
        else:
            items = d[op["coll"]]
            idx = next((i for i, e in enumerate(items) if e["id"] == op["entry"]["id"]), None)
            if idx is None:
                items.append(dict(op["entry"]))
            elif op.get("fields") is not None:
                items[idx].update({k: op["entry"].get(k) for k in op["fields"]})
            else:
                items[idx] = dict(op["entry"])
    for s in d["serwisy"]:
        s["paidCost"] = 0 if s.get("warranty") else s.get("price", 0)
    recalc_tankowania(d["tankowania"])
    return d


def with_prices(tankowania):
    for t in tankowania:
        t["pricePerL"] = round(t["cost"] / t["liters"], 3)


def sync_with_sheet(client, local, ops, first_connect):
    remote = pull_sheet(client)
    if remote["invalid"]:
        more = "…" if len(remote["invalid"]) > 3 else ""
        raise SyncDataError(f"W arkuszu są wiersze, których nie da się odczytać ({'; '.join(remote['invalid'][:3])}{more}). "
                            "Popraw je — do tego czasu nic nie zostanie nadpisane.")
    good_settings = {k: v for k, v in remote["data"]["settings"].items()
                     if v not in ("", None) and not is_nan(v)}
    base = sanitize({**remote["data"], "settings": {**local["settings"], **good_settings}})
    pending = ops
    if first_connect:
        # first connection: keep entries that exist only on this device (matched by ID or content);
        # the sheet wins for everything else
        def in_sheet(coll, e):
            return any(r["id"] == e["id"] or SAME_EVENT[coll](r, e) for r in base[coll])

        extra = [{"type": "upsert", "coll": c, "entry": e} for c in COLLECTIONS for e in local[c]
                 if not in_sheet(c, e)]

        def known(op):
            return (op["type"] == "upsert" and not any(r["id"] == op["entry"]["id"] for r in base[op["coll"]])
                    and in_sheet(op["coll"], op["entry"]))

        pending = extra + [op for op in ops if op["type"] != "settings" and not known(op)]
    merged = apply_ops(base, pending)
    with_prices(merged["tankowania"])

    clears, data = [], []
    for t in SHEET_TABLES:
        rows = [t["to_row"](e) for e in sorted(merged[t["coll"]], key=t["key"])]
        current = [t["to_row"](e) for e in remote["data"][t["coll"]]]
        gaps = remote["rows"][t["tab"]] != len(remote["data"][t["coll"]])
        if t["tab"] not in remote["needs_rewrite"] and not gaps and rows == current:
            continue
        if rows:
            data.append({"range": f"{t['tab']}!A2", "values": rows})
        if remote["rows"][t["tab"]] > len(rows):
            clears.append(f"{t['tab']}!A{len(rows) + 2}:{t['last']}{remote['rows'][t['tab']] + 1}")
    next_row = max([1, *remote["setting_rows"].values()]) + 1
    for k in SETTING_KEYS:
        if merged["settings"].get(k) == remote["data"]["settings"].get(k):
            continue
        row = remote["setting_rows"].get(k)
        if row is None:
            row, next_row = next_row, next_row + 1
        data.append({"range": f"Ustawienia!A{row}:B{row}", "values": [[k, merged["settings"][k]]]})
    if clears:
        client.batch_clear(clears)
    if data:
        client.batch_update(data)
    return merged


# ----------------------------------------------------------------------
# MAIN APPLICATION
# ----------------------------------------------------------------------
SYNC_LONG = {"syncing": "Synchronizacja…", "auth": "Zaloguj do Google", "error": "Błąd synchronizacji"}


def sync_label(app):
    state, _ = app.sync_status
    pending = len(app.sync_state["ops"])
    if not app.sync_state["connected"]:
        return "Niepołączono"
    if state in SYNC_LONG:
        return SYNC_LONG[state]
    if pending:
        return f"Do wysłania: {pending}"
    return "Zsynchronizowano" if app.sync_state.get("lastSync") else "Połączono"


def sync_color(app):
    state, _ = app.sync_status
    if not app.sync_state["connected"]:
        return C["text_faint"]
    if state == "error":
        return C["red"]
    if state == "auth":
        return C["amber"]
    if state == "ok" and not app.sync_state["ops"]:
        return C["green"]
    return C["text_dim"]


class CarApp(ctk.CTk):
    PAGES = [("dashboard", "Pulpit", "home", DashboardPage), ("tankowania", "Tankowania", "fuel", TankowaniaPage),
             ("serwisy", "Serwisy", "wrench", SerwisyPage), ("koszty", "Koszty", "card", KosztyPage),
             ("prognoza", "Prognoza", "chart", PrognozaPage), ("ustawienia", "Ustawienia", "settings", UstawieniaPage)]
    _deactivate_windows_window_header_manipulation = True  # see style_titlebar()

    def __init__(self):
        ctk.set_appearance_mode("dark")
        super().__init__(fg_color=C["bg"])
        self.withdraw()  # shown at the end of __init__, fully built and with the dark title bar
        self.data = load_data()
        self.sync_state = load_sync_state()
        self.sync_status = ("idle", None)
        self._snapshot = json.loads(json.dumps(self.data))
        self._sync_thread = None
        self._sync_job = None
        self._sync_again = False
        self._sync_results = queue.Queue()
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
        # only the visible page is gridded: hidden pages would otherwise be re-laid out (charts included)
        # on every window resize
        for key, _, _, cls in self.PAGES:
            self.pages[key] = cls(self)
        self.dirty = set(self.pages)
        self.current = None
        self.toast = Toast(self)
        self.bind("<Control-n>", lambda e: self.new_entry())
        self.show("dashboard")
        style_titlebar(self, C["bg"])
        self.deiconify()
        self._refresh_sync_badge()
        self.after(200, self._poll_sync)
        if self.sync_state["connected"]:
            self.after(800, self.sync_now)
        self.after(10 * 60 * 1000, self._periodic_sync)

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
        self.sync_badge = ctk.CTkButton(sb, text="", anchor="w", height=30, corner_radius=8, font=font(12),
                                        fg_color="transparent", hover_color=C["surface2"],
                                        command=self._sync_badge_click)
        self.sync_badge.pack(side="bottom", fill="x", padx=14, pady=(0, 4))

    def _refresh_brand(self):
        self.brand_title.configure(text=self.data["settings"]["carName"].title()
                                   if self.data["settings"]["carName"].isupper() else self.data["settings"]["carName"])
        self.brand_sub.configure(text=self.data["settings"]["carSubtitle"])

    def _style_nav(self, key, active):
        b, ic = self.nav[key]
        b.configure(fg_color=C["copper_soft"] if active else "transparent",
                    text_color=C["text"] if active else C["text_dim"],
                    image=icon(ic, C["copper"] if active else C["text_dim"], 18),
                    font=font(14, "semibold" if active else "normal"))

    def show(self, key):
        previous = self.current
        if previous != key:
            if previous is not None:
                self._style_nav(previous, False)
                self.pages[previous].grid_remove()
            self._style_nav(key, True)
        self.current = key
        page = self.pages[key]
        if key in self.dirty:
            page.refresh()
            self.dirty.discard(key)
        page.grid(row=0, column=0, sticky="nsew")

    def new_entry(self):
        forms = {"tankowania": TankowanieForm, "serwisy": SerwisForm, "koszty": KosztForm}
        forms.get(self.current, TankowanieForm)(self)

    # ---------------- data operations ----------------
    def data_changed(self):
        recalc_tankowania(self.data["tankowania"])
        save_data(self.data)
        self._record_ops()
        self._refresh_views()

    def _refresh_views(self):
        self._refresh_brand()
        self._refresh_sync_badge()
        self.dirty = set(self.pages)
        self.show(self.current)

    def upsert(self, collection, entry, values, initial=None):
        target = None
        if entry is not None:
            # a sync may have replaced the data since the form was opened: write into the current copy,
            # and only the fields the user changed compared with what the form was opened with
            target = next((e for e in self.data[collection] if e["id"] == entry["id"]), None)
            if target is not None and initial is not None:
                values = {k: v for k, v in values.items() if not same_value(initial.get(k), v)}
        if target is None:
            target = {**(initial or {}), "id": entry["id"] if entry is not None else new_id()}
            self.data[collection].append(target)
        target.update(values)
        self.data_changed()
        return target

    # ---------------- Google Sheets sync ----------------
    def _record_ops(self):
        # nothing is queued while not connected: a stale edit could otherwise overwrite the sheet much later,
        # on connecting (entries that exist only here are still added then, matched by content)
        ops = diff_ops(self._snapshot, self.data) if self.sync_state["connected"] else []
        if ops:
            for op in ops:
                self.sync_state["seq"] += 1
                op["seq"] = self.sync_state["seq"]
            self.sync_state["ops"] = compact_ops(self.sync_state["ops"] + ops)
            save_sync_state(self.sync_state)
            self._schedule_sync(1500)
        self._snapshot = json.loads(json.dumps(self.data))

    def _schedule_sync(self, ms):
        if not self.sync_state["connected"]:
            return
        if self._sync_job:
            self.after_cancel(self._sync_job)
        self._sync_job = self.after(ms, self.sync_now)

    def _periodic_sync(self):
        if self.sync_state["connected"]:
            self.sync_now()
        self.after(10 * 60 * 1000, self._periodic_sync)

    def sync_now(self, interactive=False):
        self._sync_job = None
        if not self.sync_state["connected"]:
            return
        if self._sync_thread is not None and self._sync_thread.is_alive():
            self._sync_again = True
            return
        local = json.loads(json.dumps(self.data))
        ops = json.loads(json.dumps(self.sync_state["ops"]))
        first = not self.sync_state["firstDone"]
        max_seq = max((op.get("seq", 0) for op in ops), default=0)
        results = self._sync_results

        def work():
            try:
                creds = google_credentials(interactive)
                results.put(("ok", sync_with_sheet(SheetsClient(creds), local, ops, first), max_seq))
            except SyncAuthError as exc:
                results.put(("auth", str(exc), max_seq))
            except SyncDataError as exc:
                results.put(("error", str(exc), max_seq))
            except Exception as exc:  # network down, timeouts...
                results.put(("error", f"Synchronizacja nie powiodła się ({exc.__class__.__name__}). "
                                      "Zmiany czekają w kolejce.", max_seq))

        self._set_sync_status("syncing")
        self._sync_thread = threading.Thread(target=work, daemon=True)
        self._sync_thread.start()

    def _poll_sync(self):
        try:
            while True:
                self._finish_sync(*self._sync_results.get_nowait())
        except queue.Empty:
            pass
        if self.winfo_exists():
            self.after(200, self._poll_sync)

    def _finish_sync(self, kind, payload, max_seq):
        if kind == "ok":
            # edits made while the request was running stay queued and are applied on top
            later = [op for op in self.sync_state["ops"] if op.get("seq", 0) > max_seq]
            self.data = sanitize(apply_ops(payload, later) if later else payload)
            recalc_tankowania(self.data["tankowania"])
            save_data(self.data)
            self._snapshot = json.loads(json.dumps(self.data))
            self.sync_state.update(ops=later, firstDone=True, lastSync=time.time())
            save_sync_state(self.sync_state)
            self.sync_status = ("ok", None)
            self._refresh_views()
            if later:
                self._schedule_sync(500)
        else:
            self._set_sync_status(kind, payload)
        if self._sync_again:
            self._sync_again = False
            self._schedule_sync(300)

    def _set_sync_status(self, state, message=None):
        self.sync_status = (state, message)
        self._refresh_sync_badge()
        if "ustawienia" not in self.dirty:
            self.pages["ustawienia"].refresh_sync()

    def _refresh_sync_badge(self):
        self.sync_badge.configure(text=f"●  {sync_label(self)}", text_color=sync_color(self))

    def _sync_badge_click(self):
        if not self.sync_state["connected"]:
            self.show("ustawienia")
        elif self.sync_status[0] == "auth":
            self.sync_connect()
        else:
            self.sync_now()

    def sync_connect(self):
        if not self.sync_state["connected"]:
            self.sync_state.update(connected=True, firstDone=False, ops=[])
        save_sync_state(self.sync_state)
        self.toast.show("Otwieram logowanie Google w przeglądarce…")
        self.sync_now(interactive=True)

    def sync_disconnect(self):
        def do():
            self.sync_state.update(connected=False, firstDone=False)
            save_sync_state(self.sync_state)
            if os.path.exists(TOKEN_FILE):
                os.remove(TOKEN_FILE)
            self._set_sync_status("idle")
            self.toast.show("Odłączono od arkusza Google", "warn")

        ConfirmDialog(self, "Odłączyć arkusz?", "Dane zostaną na komputerze, ale zmiany przestaną trafiać do arkusza "
                      "Google. Możesz połączyć się ponownie w każdej chwili.", "Odłącz", do)

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
                      f"{plural(len(new['koszty']), 'koszt', 'koszty', 'kosztów')})."
                      + (" Zmiana trafi też do arkusza Google." if self.sync_state["connected"] else ""),
                      "Wczytaj", apply, danger=False)


if __name__ == "__main__":
    if sys.platform == "win32":
        # own taskbar identity: shown with the app icon (not Python's) and pinnable on its own
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("CupraTerramar.Dziennik")
    app = CarApp()
    app.mainloop()
