#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cupra Terramar — Dziennik pokładowy (wersja desktopowa)
=========================================================
Aplikacja okienkowa (tkinter) do monitorowania tankowań, serwisów
i kosztów samochodu. Dane zapisują się automatycznie w pliku JSON
w katalogu domowym użytkownika.

Uruchomienie:
    python cupra_terramar_gui.py

Wymagania:
    pip install matplotlib
    (tkinter jest częścią standardowej biblioteki Pythona; na Linuksie
     czasem trzeba go doinstalować osobno, np. `sudo apt install python3-tk`)
"""

import json
import os
import uuid
import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------------------------------------------------------------
# THEME
# ----------------------------------------------------------------------
C = {
    "bg": "#0F0D0C",
    "surface": "#1A1613",
    "surface2": "#221D19",
    "line": "#332C26",
    "copper": "#C96A34",
    "copper_dim": "#8A5330",
    "amber": "#D9A438",
    "green": "#5FAE7C",
    "red": "#C4483C",
    "text": "#F3EEE7",
    "text_dim": "#9C948B",
    "text_faint": "#665F58",
}
FONT_FAMILY = "Segoe UI" if os.name == "nt" else "Helvetica"
FONT_MONO = "Consolas" if os.name == "nt" else "Courier"

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
# STYLE SETUP
# ----------------------------------------------------------------------
def setup_style(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    root.configure(bg=C["bg"])
    style.configure(".", background=C["bg"], foreground=C["text"], fieldbackground=C["surface"],
                     font=(FONT_FAMILY, 10))
    style.configure("TFrame", background=C["bg"], bordercolor=C["bg"], darkcolor=C["bg"], lightcolor=C["bg"])
    style.configure("Surface.TFrame", background=C["surface"], bordercolor=C["surface"],
                     darkcolor=C["surface"], lightcolor=C["surface"])
    style.configure("TLabel", background=C["bg"], foreground=C["text"])
    style.configure("Surface.TLabel", background=C["surface"], foreground=C["text"])
    style.configure("Dim.TLabel", background=C["surface"], foreground=C["text_dim"], font=(FONT_FAMILY, 9))
    style.configure("Faint.TLabel", background=C["bg"], foreground=C["text_faint"], font=(FONT_FAMILY, 9))
    style.configure("Header.TLabel", background=C["bg"], foreground=C["text"],
                     font=(FONT_FAMILY, 16, "bold"))
    style.configure("Sub.TLabel", background=C["bg"], foreground=C["text_dim"], font=(FONT_FAMILY, 9))
    style.configure("KPIValue.TLabel", background=C["surface"], foreground=C["text"],
                     font=(FONT_MONO, 17, "bold"))
    style.configure("KPILabel.TLabel", background=C["surface"], foreground=C["text_dim"], font=(FONT_FAMILY, 9))

    style.configure("TNotebook", background=C["bg"], borderwidth=0,
                     bordercolor=C["bg"], darkcolor=C["bg"], lightcolor=C["bg"])
    style.configure("TNotebook.Tab", background=C["surface"], foreground=C["text_dim"],
                     padding=(14, 8), font=(FONT_FAMILY, 10, "bold"), borderwidth=0)
    style.map("TNotebook.Tab",
              background=[("selected", C["copper"])],
              foreground=[("selected", "#100C09")])

    style.configure("Copper.TButton", background=C["copper"], foreground="#100C09",
                     font=(FONT_FAMILY, 10, "bold"), padding=(12, 8), borderwidth=0)
    style.map("Copper.TButton", background=[("active", "#dd7a3f")])
    style.configure("Ghost.TButton", background=C["bg"], foreground=C["text"],
                     font=(FONT_FAMILY, 10), padding=(12, 8), borderwidth=1)
    style.map("Ghost.TButton", background=[("active", C["surface"])])
    style.configure("Danger.TButton", background=C["surface"], foreground=C["red"],
                     font=(FONT_FAMILY, 9), padding=(6, 4), borderwidth=0)

    style.configure("TEntry", fieldbackground=C["surface2"], foreground=C["text"],
                     insertcolor=C["text"], borderwidth=1)
    style.configure("TCombobox", fieldbackground=C["surface2"], foreground=C["text"], background=C["surface2"])
    style.configure("TCheckbutton", background=C["surface"], foreground=C["text"])

    style.configure("Treeview", background=C["surface"], fieldbackground=C["surface"],
                     foreground=C["text"], rowheight=26, borderwidth=0, font=(FONT_FAMILY, 9))
    style.configure("Treeview.Heading", background=C["surface2"], foreground=C["text_dim"],
                     font=(FONT_FAMILY, 9, "bold"), borderwidth=0)
    style.map("Treeview", background=[("selected", C["copper_dim"])])

    return style


# ----------------------------------------------------------------------
# REUSABLE WIDGETS
# ----------------------------------------------------------------------
class ScrollableFrame(ttk.Frame):
    """A vertically-scrollable container (Canvas + inner Frame)."""
    def __init__(self, parent, **kw):
        super().__init__(parent, style="TFrame", **kw)
        self.canvas = tk.Canvas(self, bg=C["bg"], highlightthickness=0)
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas, style="TFrame")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self._win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self._win, width=e.width))
        self.canvas.configure(yscrollcommand=vsb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        def _wheel(e):
            delta = -1 * (e.delta // 120) if e.delta else (1 if e.num == 5 else -1)
            self.canvas.yview_scroll(int(delta), "units")
        self.canvas.bind_all("<MouseWheel>", _wheel, add="+")
        self.canvas.bind_all("<Button-4>", _wheel, add="+")
        self.canvas.bind_all("<Button-5>", _wheel, add="+")


class Card(ttk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, style="Surface.TFrame", padding=14, **kw)


class KPI(Card):
    def __init__(self, parent, label, value, **kw):
        super().__init__(parent, **kw)
        ttk.Label(self, text=label.upper(), style="KPILabel.TLabel").pack(anchor="w")
        ttk.Label(self, text=value, style="KPIValue.TLabel").pack(anchor="w", pady=(4, 0))


class Pill(tk.Label):
    def __init__(self, parent, text, color, **kw):
        super().__init__(parent, text=text, fg=color, bg=C["surface"],
                          font=(FONT_FAMILY, 8, "bold"), padx=8, pady=2, **kw)


def styled_entry(parent, textvariable=None, width=20):
    e = tk.Entry(parent, textvariable=textvariable, width=width, bg=C["surface2"], fg=C["text"],
                 insertbackground=C["text"], relief="flat", highlightthickness=1,
                 highlightbackground=C["line"], highlightcolor=C["copper"])
    return e


def field(parent, label_text, widget_factory):
    wrap = ttk.Frame(parent, style="Surface.TFrame")
    wrap.pack(fill="x", pady=4)
    ttk.Label(wrap, text=label_text, style="Dim.TLabel").pack(anchor="w")
    w = widget_factory(wrap)
    w.pack(fill="x", pady=(2, 0))
    return w


# ----------------------------------------------------------------------
# GAUGE CANVAS (consumption ring, like the web app)
# ----------------------------------------------------------------------
class GaugeCanvas(tk.Canvas):
    def __init__(self, parent, size=150, **kw):
        super().__init__(parent, width=size, height=size, bg=C["surface"], highlightthickness=0, **kw)
        self.size = size

    def draw(self, value, settings):
        self.delete("all")
        s = self.size
        pad = 14
        status = status_of(value, settings)
        color = status[1] if status else C["text_faint"]
        high = settings["consumptionHighFrom"]
        vmax = max(high * 1.4, (value * 1.15) if value else 12)
        pct = min(value / vmax, 1) if value else 0

        self.create_oval(pad, pad, s - pad, s - pad, outline=C["line"], width=10)
        if pct > 0:
            self.create_arc(pad, pad, s - pad, s - pad, start=90, extent=-360 * pct,
                             style="arc", outline=color, width=10)

        self.create_text(s / 2, s / 2 - 10, text=(numf(value, 1) if value else "—"),
                          fill=C["text"], font=(FONT_MONO, 20, "bold"))
        self.create_text(s / 2, s / 2 + 14, text="l / 100km", fill=C["text_dim"], font=(FONT_FAMILY, 8))
        if status:
            self.create_text(s / 2, s / 2 + 32, text=status[0], fill=color, font=(FONT_FAMILY, 8, "bold"))


# ----------------------------------------------------------------------
# MAIN APPLICATION
# ----------------------------------------------------------------------
class CarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.data = load_data()
        self.title("Dziennik pokładowy")
        self.geometry("880x680")
        self.minsize(760, 560)
        self.style = setup_style(self)

        self._build_header()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.tab_dashboard = ttk.Frame(self.notebook, style="TFrame")
        self.tab_tankowania = ttk.Frame(self.notebook, style="TFrame")
        self.tab_serwisy = ttk.Frame(self.notebook, style="TFrame")
        self.tab_koszty = ttk.Frame(self.notebook, style="TFrame")
        self.tab_prognoza = ttk.Frame(self.notebook, style="TFrame")
        self.tab_ustawienia = ttk.Frame(self.notebook, style="TFrame")

        for tab, label in [
            (self.tab_dashboard, "Pulpit"), (self.tab_tankowania, "Tankowania"),
            (self.tab_serwisy, "Serwisy"), (self.tab_koszty, "Koszty"),
            (self.tab_prognoza, "Prognoza"), (self.tab_ustawienia, "Ustawienia"),
        ]:
            self.notebook.add(tab, text=label)

        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.refresh_current_tab())

        self._build_dashboard()
        self._build_tankowania()
        self._build_serwisy()
        self._build_koszty()
        self._build_prognoza()
        self._build_ustawienia()

        self.refresh_all()

    # ---------------- persistence ----------------
    def persist(self):
        save_data(self.data)

    def refresh_all(self):
        self.refresh_dashboard()
        self.refresh_tankowania()
        self.refresh_serwisy()
        self.refresh_koszty()
        self.refresh_prognoza()

    def refresh_current_tab(self):
        idx = self.notebook.index(self.notebook.select())
        [self.refresh_dashboard, self.refresh_tankowania, self.refresh_serwisy,
         self.refresh_koszty, self.refresh_prognoza, lambda: None][idx]()

    # ---------------- header ----------------
    def _build_header(self):
        header = tk.Frame(self, bg=C["bg"])
        header.pack(fill="x", padx=16, pady=(16, 8))
        badge = tk.Frame(header, bg=C["copper_dim"], width=42, height=42)
        badge.pack(side="left")
        badge.pack_propagate(False)
        tk.Label(badge, text="⛟", bg=C["copper_dim"], fg=C["copper"], font=(FONT_FAMILY, 18)).pack(expand=True)

        text_wrap = tk.Frame(header, bg=C["bg"])
        text_wrap.pack(side="left", padx=10)
        self.header_title = ttk.Label(text_wrap, text=self.data["settings"]["carName"], style="Header.TLabel")
        self.header_title.pack(anchor="w")
        self.header_sub = ttk.Label(text_wrap, text=self.data["settings"]["carSubtitle"], style="Sub.TLabel")
        self.header_sub.pack(anchor="w")

    def _refresh_header(self):
        self.header_title.config(text=self.data["settings"]["carName"])
        self.header_sub.config(text=self.data["settings"]["carSubtitle"])

    # ---------------- DASHBOARD ----------------
    def _build_dashboard(self):
        outer = ttk.Frame(self.tab_dashboard, style="TFrame", padding=12)
        outer.pack(fill="both", expand=True)

        top = ttk.Frame(outer, style="TFrame")
        top.pack(fill="x")

        gauge_card = Card(top)
        gauge_card.pack(side="left", padx=(0, 10), pady=4)
        ttk.Label(gauge_card, text="ŚREDNIE SPALANIE", style="Dim.TLabel").pack()
        self.gauge = GaugeCanvas(gauge_card)
        self.gauge.pack(pady=6)

        kpi_grid = ttk.Frame(top, style="TFrame")
        kpi_grid.pack(side="left", fill="both", expand=True)
        self.kpi_vars = {}
        kpi_defs = [
            ("cost", "Koszt całkowity"), ("dist", "Dystans"),
            ("costkm", "Koszt / km"), ("price", "Śr. cena / l"),
            ("alerts", "Alerty spalania"), ("service", "Ostatni serwis"),
        ]
        for i, (key, label) in enumerate(kpi_defs):
            k = KPI(kpi_grid, label, "—")
            k.grid(row=i // 2, column=i % 2, sticky="nsew", padx=4, pady=4)
            self.kpi_vars[key] = k
        kpi_grid.columnconfigure(0, weight=1)
        kpi_grid.columnconfigure(1, weight=1)

        charts = ttk.Frame(outer, style="TFrame")
        charts.pack(fill="both", expand=True, pady=(10, 0))

        self.fig_cost = Figure(figsize=(5.2, 2.1), dpi=100, facecolor=C["surface"])
        self.ax_cost = self.fig_cost.add_subplot(111)
        self.canvas_cost = FigureCanvasTkAgg(self.fig_cost, master=charts)
        self.canvas_cost.get_tk_widget().pack(fill="both", expand=True, pady=(0, 8))

        self.fig_cons = Figure(figsize=(5.2, 2.1), dpi=100, facecolor=C["surface"])
        self.ax_cons = self.fig_cons.add_subplot(111)
        self.canvas_cons = FigureCanvasTkAgg(self.fig_cons, master=charts)
        self.canvas_cons.get_tk_widget().pack(fill="both", expand=True)

    def _style_ax(self, ax, fig):
        fig.patch.set_facecolor(C["surface"])
        ax.set_facecolor(C["surface"])
        ax.tick_params(colors=C["text_faint"], labelsize=7)
        for spine in ax.spines.values():
            spine.set_color(C["line"])
        ax.grid(True, color=C["line"], linewidth=0.6, axis="y")
        ax.set_axisbelow(True)

    def refresh_dashboard(self):
        agg = compute_aggregates(self.data)
        settings = self.data["settings"]
        self.gauge.draw(agg["weightedConsumption"], settings)

        self.kpi_vars["cost"].winfo_children()[1].config(text=pln(agg["totalCost"]))
        self.kpi_vars["dist"].winfo_children()[1].config(text=f"{numf(agg['totalDistance'],0)} km")
        self.kpi_vars["costkm"].winfo_children()[1].config(
            text=f"{numf(agg['costPerKm'],2)} zł" if agg["costPerKm"] else "—")
        self.kpi_vars["price"].winfo_children()[1].config(
            text=f"{numf(agg['avgPricePerL'],2)} zł" if agg["avgPricePerL"] else "—")
        self.kpi_vars["alerts"].winfo_children()[1].config(text=str(agg["alerts"]))
        self.kpi_vars["service"].winfo_children()[1].config(
            text=date_fmt(agg["lastService"]["date"]) if agg["lastService"] else "—")

        monthly = [m for m in agg["monthly"] if m["total"] > 0]

        self.ax_cost.clear()
        self._style_ax(self.ax_cost, self.fig_cost)
        self.ax_cost.set_title("Koszty miesięczne", color=C["text_dim"], fontsize=9, loc="left")
        if monthly:
            labels = [m["label"] for m in monthly]
            vals = [m["total"] for m in monthly]
            self.ax_cost.bar(labels, vals, color=C["copper"])
        self.canvas_cost.draw()

        self.ax_cons.clear()
        self._style_ax(self.ax_cons, self.fig_cons)
        self.ax_cons.set_title("Spalanie w czasie (l/100km)", color=C["text_dim"], fontsize=9, loc="left")
        cons_pts = [(m["label"], m["consumption"]) for m in monthly if m["consumption"] is not None]
        if len(cons_pts) > 1:
            labels = [p[0] for p in cons_pts]
            vals = [p[1] for p in cons_pts]
            self.ax_cons.plot(labels, vals, color=C["amber"], marker="o", markersize=4, linewidth=2)
        self.canvas_cons.draw()

    # ---------------- TANKOWANIA ----------------
    def _build_tankowania(self):
        outer = ttk.Frame(self.tab_tankowania, style="TFrame", padding=12)
        outer.pack(fill="both", expand=True)

        bar = ttk.Frame(outer, style="TFrame")
        bar.pack(fill="x", pady=(0, 8))
        self.tank_count_lbl = ttk.Label(bar, text="", style="Faint.TLabel")
        self.tank_count_lbl.pack(side="left")
        ttk.Button(bar, text="+ Dodaj tankowanie", style="Copper.TButton",
                   command=self.open_tankowanie_form).pack(side="right")

        cols = ("date", "fuel", "liters", "cost", "price", "mileage", "consumption", "status")
        headers = ["Data", "Paliwo", "Litry", "Koszt", "Zł/l", "Przebieg", "Spalanie", "Status"]
        self.tank_tree = ttk.Treeview(outer, columns=cols, show="headings", height=14)
        for c, h in zip(cols, headers):
            self.tank_tree.heading(c, text=h)
            self.tank_tree.column(c, width=90, anchor="center")
        self.tank_tree.pack(fill="both", expand=True)
        self.tank_tree.tag_configure("high", foreground=C["red"])
        self.tank_tree.tag_configure("warn", foreground=C["amber"])
        self.tank_tree.tag_configure("ok", foreground=C["green"])

        btns = ttk.Frame(outer, style="TFrame")
        btns.pack(fill="x", pady=(6, 0))
        ttk.Button(btns, text="Usuń zaznaczone", style="Ghost.TButton",
                   command=self.delete_tankowanie).pack(side="left")

    def refresh_tankowania(self):
        for row in self.tank_tree.get_children():
            self.tank_tree.delete(row)
        rows = sorted(self.data["tankowania"], key=lambda t: t["date"], reverse=True)
        settings = self.data["settings"]
        for t in rows:
            status = status_of(t.get("consumption"), settings)
            tag = ""
            status_text = "—"
            if status:
                status_text = status[0]
                tag = {"Wysokie": "high", "Uwaga": "warn", "OK": "ok"}[status[0]]
            self.tank_tree.insert("", "end", iid=t["id"], values=(
                date_fmt(t["date"]), t["fuelType"], numf(t["liters"], 2), pln(t["cost"]),
                numf(t["pricePerL"], 2), numf(t["mileage"], 0),
                numf(t["consumption"], 2) if t["consumption"] is not None else "—", status_text,
            ), tags=(tag,))
        self.tank_count_lbl.config(text=f"{len(rows)} tankowań")

    def delete_tankowanie(self):
        sel = self.tank_tree.selection()
        if not sel:
            return
        if not messagebox.askyesno("Usuń", "Usunąć zaznaczone tankowanie(a)?"):
            return
        ids = set(sel)
        self.data["tankowania"] = [t for t in self.data["tankowania"] if t["id"] not in ids]
        self.persist()
        self.refresh_tankowania()
        self.refresh_dashboard()

    def open_tankowanie_form(self):
        win = tk.Toplevel(self)
        win.title("Nowe tankowanie")
        win.configure(bg=C["surface2"])
        win.geometry("340x420")

        last = sorted(self.data["tankowania"], key=lambda t: t["date"], reverse=True)
        last_mileage = last[0]["mileage"] if last else 0

        v_date = tk.StringVar(value=dt.date.today().isoformat())
        v_fuel = tk.StringVar(value="Pb98")
        v_liters = tk.StringVar()
        v_cost = tk.StringVar()
        v_mileage = tk.StringVar()
        v_note = tk.StringVar()

        pad = ttk.Frame(win, style="Surface.TFrame", padding=16)
        pad.pack(fill="both", expand=True)

        field(pad, "Data (RRRR-MM-DD)", lambda p: styled_entry(p, v_date))
        cb = field(pad, "Paliwo", lambda p: ttk.Combobox(p, textvariable=v_fuel, values=FUEL_TYPES, state="readonly"))
        field(pad, "Litry", lambda p: styled_entry(p, v_liters))
        field(pad, "Koszt (zł)", lambda p: styled_entry(p, v_cost))
        field(pad, f"Przebieg (km) — ostatni: {numf(last_mileage,0)}", lambda p: styled_entry(p, v_mileage))
        field(pad, "Notatka (opcjonalnie)", lambda p: styled_entry(p, v_note))

        def save():
            try:
                liters = float(v_liters.get().replace(",", "."))
                cost = float(v_cost.get().replace(",", "."))
                mileage = int(v_mileage.get())
                date_s = v_date.get().strip()
                dt.datetime.strptime(date_s, "%Y-%m-%d")
            except Exception:
                messagebox.showerror("Błąd", "Sprawdź poprawność danych (data RRRR-MM-DD, liczby w litrach/koszcie/przebiegu).")
                return
            distance = mileage - last_mileage if last else None
            consumption = round(liters / distance * 100, 2) if distance and distance > 0 else None
            entry = {
                "id": new_id(), "date": date_s, "fuelType": v_fuel.get(), "liters": liters, "cost": cost,
                "pricePerL": round(cost / liters, 3), "mileage": mileage, "distance": distance,
                "consumption": consumption, "note": v_note.get(),
            }
            self.data["tankowania"].append(entry)
            self.persist()
            self.refresh_tankowania()
            self.refresh_dashboard()
            win.destroy()

        btn_row = ttk.Frame(pad, style="Surface.TFrame")
        btn_row.pack(fill="x", pady=(12, 0))
        ttk.Button(btn_row, text="Zapisz", style="Copper.TButton", command=save).pack(fill="x")

    # ---------------- SERWISY ----------------
    def _build_serwisy(self):
        outer = ttk.Frame(self.tab_serwisy, style="TFrame", padding=12)
        outer.pack(fill="both", expand=True)

        bar = ttk.Frame(outer, style="TFrame")
        bar.pack(fill="x", pady=(0, 8))
        self.serw_count_lbl = ttk.Label(bar, text="", style="Faint.TLabel")
        self.serw_count_lbl.pack(side="left")
        ttk.Button(bar, text="+ Dodaj wpis serwisowy", style="Copper.TButton",
                   command=self.open_serwis_form).pack(side="right")

        cols = ("date", "mileage", "desc", "price", "warranty")
        headers = ["Data", "Przebieg", "Opis", "Cena", "Gwarancja"]
        self.serw_tree = ttk.Treeview(outer, columns=cols, show="headings", height=14)
        for c, h, w in zip(cols, headers, (90, 90, 240, 90, 90)):
            self.serw_tree.heading(c, text=h)
            self.serw_tree.column(c, width=w, anchor="center" if c != "desc" else "w")
        self.serw_tree.pack(fill="both", expand=True)

        btns = ttk.Frame(outer, style="TFrame")
        btns.pack(fill="x", pady=(6, 0))
        ttk.Button(btns, text="Usuń zaznaczone", style="Ghost.TButton",
                   command=self.delete_serwis).pack(side="left")

    def refresh_serwisy(self):
        for row in self.serw_tree.get_children():
            self.serw_tree.delete(row)
        rows = sorted(self.data["serwisy"], key=lambda s: s["date"], reverse=True)
        for s in rows:
            self.serw_tree.insert("", "end", iid=s["id"], values=(
                date_fmt(s["date"]), numf(s.get("mileage"), 0) if s.get("mileage") else "—",
                s["description"], pln(s["price"]), "Tak" if s["warranty"] else "Nie",
            ))
        self.serw_count_lbl.config(text=f"{len(rows)} wpisów serwisowych")

    def delete_serwis(self):
        sel = self.serw_tree.selection()
        if not sel:
            return
        if not messagebox.askyesno("Usuń", "Usunąć zaznaczony wpis?"):
            return
        ids = set(sel)
        self.data["serwisy"] = [s for s in self.data["serwisy"] if s["id"] not in ids]
        self.persist()
        self.refresh_serwisy()
        self.refresh_dashboard()

    def open_serwis_form(self):
        win = tk.Toplevel(self)
        win.title("Nowy wpis serwisowy")
        win.configure(bg=C["surface2"])
        win.geometry("340x420")

        v_date = tk.StringVar(value=dt.date.today().isoformat())
        v_mileage = tk.StringVar()
        v_desc = tk.StringVar()
        v_price = tk.StringVar()
        v_warranty = tk.BooleanVar(value=False)
        v_note = tk.StringVar()

        pad = ttk.Frame(win, style="Surface.TFrame", padding=16)
        pad.pack(fill="both", expand=True)

        field(pad, "Data (RRRR-MM-DD)", lambda p: styled_entry(p, v_date))
        field(pad, "Przebieg (km)", lambda p: styled_entry(p, v_mileage))
        field(pad, "Co było wykonane", lambda p: styled_entry(p, v_desc))
        field(pad, "Cena (zł)", lambda p: styled_entry(p, v_price))
        chk_wrap = ttk.Frame(pad, style="Surface.TFrame")
        chk_wrap.pack(fill="x", pady=6)
        ttk.Checkbutton(chk_wrap, text="Naprawa gwarancyjna", variable=v_warranty).pack(anchor="w")
        field(pad, "Notatka (opcjonalnie)", lambda p: styled_entry(p, v_note))

        def save():
            try:
                price = float(v_price.get().replace(",", ".")) if v_price.get() else 0.0
                date_s = v_date.get().strip()
                dt.datetime.strptime(date_s, "%Y-%m-%d")
            except Exception:
                messagebox.showerror("Błąd", "Sprawdź poprawność danych.")
                return
            if not v_desc.get().strip():
                messagebox.showerror("Błąd", "Podaj opis wykonanej czynności.")
                return
            entry = {
                "id": new_id(), "date": date_s,
                "mileage": int(v_mileage.get()) if v_mileage.get().strip() else None,
                "description": v_desc.get().strip(), "price": price, "warranty": v_warranty.get(),
                "paidCost": 0 if v_warranty.get() else price, "note": v_note.get(),
            }
            self.data["serwisy"].append(entry)
            self.persist()
            self.refresh_serwisy()
            self.refresh_dashboard()
            win.destroy()

        ttk.Button(pad, text="Zapisz", style="Copper.TButton", command=save).pack(fill="x", pady=(12, 0))

    # ---------------- KOSZTY ----------------
    def _build_koszty(self):
        outer = ttk.Frame(self.tab_koszty, style="TFrame", padding=12)
        outer.pack(fill="both", expand=True)

        bar = ttk.Frame(outer, style="TFrame")
        bar.pack(fill="x", pady=(0, 8))
        self.koszt_count_lbl = ttk.Label(bar, text="", style="Faint.TLabel")
        self.koszt_count_lbl.pack(side="left")
        ttk.Button(bar, text="+ Dodaj koszt", style="Copper.TButton",
                   command=self.open_koszt_form).pack(side="right")

        cols = ("date", "type", "desc", "amount")
        headers = ["Data", "Typ", "Opis", "Kwota"]
        self.koszt_tree = ttk.Treeview(outer, columns=cols, show="headings", height=14)
        for c, h, w in zip(cols, headers, (90, 120, 260, 100)):
            self.koszt_tree.heading(c, text=h)
            self.koszt_tree.column(c, width=w, anchor="center" if c != "desc" else "w")
        self.koszt_tree.pack(fill="both", expand=True)

        btns = ttk.Frame(outer, style="TFrame")
        btns.pack(fill="x", pady=(6, 0))
        ttk.Button(btns, text="Usuń zaznaczone", style="Ghost.TButton",
                   command=self.delete_koszt).pack(side="left")

    def refresh_koszty(self):
        for row in self.koszt_tree.get_children():
            self.koszt_tree.delete(row)
        rows = sorted(self.data["koszty"], key=lambda k: k["date"], reverse=True)
        for k in rows:
            self.koszt_tree.insert("", "end", iid=k["id"], values=(
                date_fmt(k["date"]), k["type"], k["description"], pln(k["amount"]),
            ))
        self.koszt_count_lbl.config(text=f"{len(rows)} pozycji kosztowych")

    def delete_koszt(self):
        sel = self.koszt_tree.selection()
        if not sel:
            return
        if not messagebox.askyesno("Usuń", "Usunąć zaznaczoną pozycję?"):
            return
        ids = set(sel)
        self.data["koszty"] = [k for k in self.data["koszty"] if k["id"] not in ids]
        self.persist()
        self.refresh_koszty()
        self.refresh_dashboard()

    def open_koszt_form(self):
        win = tk.Toplevel(self)
        win.title("Nowy koszt")
        win.configure(bg=C["surface2"])
        win.geometry("340x360")

        v_date = tk.StringVar(value=dt.date.today().isoformat())
        v_type = tk.StringVar(value="Inne")
        v_desc = tk.StringVar()
        v_amount = tk.StringVar()

        pad = ttk.Frame(win, style="Surface.TFrame", padding=16)
        pad.pack(fill="both", expand=True)

        field(pad, "Data (RRRR-MM-DD)", lambda p: styled_entry(p, v_date))
        field(pad, "Typ kosztu", lambda p: ttk.Combobox(p, textvariable=v_type, values=KOSZTY_TYPES, state="readonly"))
        field(pad, "Opis", lambda p: styled_entry(p, v_desc))
        field(pad, "Kwota (zł)", lambda p: styled_entry(p, v_amount))

        def save():
            try:
                amount = float(v_amount.get().replace(",", "."))
                date_s = v_date.get().strip()
                dt.datetime.strptime(date_s, "%Y-%m-%d")
            except Exception:
                messagebox.showerror("Błąd", "Sprawdź poprawność danych.")
                return
            entry = {
                "id": new_id(), "date": date_s, "type": v_type.get(),
                "description": v_desc.get().strip() or v_type.get(), "amount": amount, "note": "",
            }
            self.data["koszty"].append(entry)
            self.persist()
            self.refresh_koszty()
            self.refresh_dashboard()
            win.destroy()

        ttk.Button(pad, text="Zapisz", style="Copper.TButton", command=save).pack(fill="x", pady=(12, 0))

    # ---------------- PROGNOZA ----------------
    def _build_prognoza(self):
        outer = ttk.Frame(self.tab_prognoza, style="TFrame", padding=12)
        outer.pack(fill="both", expand=True)

        kpi_row = ttk.Frame(outer, style="TFrame")
        kpi_row.pack(fill="x")
        self.prog_kpi_total = KPI(kpi_row, "Prognoza 12 mies.", "—")
        self.prog_kpi_total.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.prog_kpi_avg = KPI(kpi_row, "Śr. miesięcznie", "—")
        self.prog_kpi_avg.pack(side="left", fill="x", expand=True, padx=(4, 0))

        self.prog_assump = ttk.Label(outer, text="", style="Faint.TLabel", wraplength=760)
        self.prog_assump.pack(anchor="w", pady=(10, 4))

        self.fig_prog = Figure(figsize=(6, 2.6), dpi=100, facecolor=C["surface"])
        self.ax_prog = self.fig_prog.add_subplot(111)
        self.canvas_prog = FigureCanvasTkAgg(self.fig_prog, master=outer)
        self.canvas_prog.get_tk_widget().pack(fill="both", expand=True, pady=(6, 0))

    def refresh_prognoza(self):
        agg = compute_aggregates(self.data)
        settings = self.data["settings"]
        base_consumption = agg["weightedConsumption"] or settings["consumptionOkTo"]
        base_price = agg["avgPricePerL"] or 6.5

        today = dt.date.today()
        rows = []
        for i in range(12):
            month_idx = today.month - 1 + i
            year = today.year + month_idx // 12
            month = month_idx % 12 + 1
            growth = (1 + settings["fuelPriceGrowth"]) ** (i / 12)
            fuel = (settings["monthlyKmPlan"] / 100) * base_consumption * base_price * growth
            label = f"{MONTHS_PL[month-1]} {str(year)[2:]}"
            rows.append((label, fuel))

        total12 = sum(r[1] for r in rows)
        avg_month = total12 / 12

        self.prog_kpi_total.winfo_children()[1].config(text=pln(total12))
        self.prog_kpi_avg.winfo_children()[1].config(text=pln(avg_month))
        self.prog_assump.config(text=(
            f"Założenia: {numf(settings['monthlyKmPlan'],0)} km/mies., "
            f"spalanie {numf(base_consumption,2)} l/100km, "
            f"wzrost cen {numf(settings['fuelPriceGrowth']*100,1)}%/rok"
        ))

        self.ax_prog.clear()
        self._style_ax(self.ax_prog, self.fig_prog)
        self.ax_prog.set_title("Prognoza kosztów paliwa", color=C["text_dim"], fontsize=9, loc="left")
        labels = [r[0] for r in rows]
        vals = [r[1] for r in rows]
        self.ax_prog.plot(labels, vals, color=C["copper"], marker="o", markersize=3, linewidth=2)
        self.ax_prog.tick_params(axis="x", rotation=45)
        self.fig_prog.tight_layout()
        self.canvas_prog.draw()

    # ---------------- USTAWIENIA ----------------
    def _build_ustawienia(self):
        scroll = ScrollableFrame(self.tab_ustawienia)
        scroll.pack(fill="both", expand=True)
        outer = ttk.Frame(scroll.inner, style="TFrame", padding=12)
        outer.pack(fill="both", expand=True)

        card = Card(outer)
        card.pack(fill="x", pady=(0, 10))

        s = self.data["settings"]
        self.v_car_name = tk.StringVar(value=s["carName"])
        self.v_car_sub = tk.StringVar(value=s["carSubtitle"])
        self.v_ok_to = tk.StringVar(value=str(s["consumptionOkTo"]))
        self.v_high_from = tk.StringVar(value=str(s["consumptionHighFrom"]))
        self.v_growth = tk.StringVar(value=str(s["fuelPriceGrowth"]))
        self.v_km_plan = tk.StringVar(value=str(s["monthlyKmPlan"]))
        self.v_car_price = tk.StringVar(value=str(s["carPrice"]))

        field(card, "Nazwa auta (nagłówek)", lambda p: styled_entry(p, self.v_car_name))
        field(card, "Podtytuł nagłówka", lambda p: styled_entry(p, self.v_car_sub))
        field(card, "Próg spalania — OK do (l/100km)", lambda p: styled_entry(p, self.v_ok_to))
        field(card, "Próg spalania — wysokie od (l/100km)", lambda p: styled_entry(p, self.v_high_from))
        field(card, "Wzrost cen paliwa rocznie (np. 0.05 = 5%)", lambda p: styled_entry(p, self.v_growth))
        field(card, "Przebieg miesięczny do symulacji (km)", lambda p: styled_entry(p, self.v_km_plan))
        field(card, "Cena auta / baza amortyzacji (zł)", lambda p: styled_entry(p, self.v_car_price))

        ttk.Button(card, text="Zapisz ustawienia", style="Copper.TButton",
                   command=self.save_settings).pack(fill="x", pady=(10, 0))

        backup_card = Card(outer)
        backup_card.pack(fill="x")
        ttk.Label(backup_card, text="Kopia zapasowa danych", style="Surface.TLabel",
                  font=(FONT_FAMILY, 11, "bold")).pack(anchor="w")
        ttk.Label(backup_card,
                  text="Dane są zapisane lokalnie w pliku na tym komputerze:\n" + DATA_FILE,
                  style="Dim.TLabel", wraplength=600, justify="left").pack(anchor="w", pady=(4, 10))
        row = ttk.Frame(backup_card, style="Surface.TFrame")
        row.pack(fill="x")
        ttk.Button(row, text="Eksportuj kopię (.json)", style="Ghost.TButton",
                   command=self.export_backup).pack(side="left", padx=(0, 8))
        ttk.Button(row, text="Wczytaj kopię", style="Ghost.TButton",
                   command=self.import_backup).pack(side="left")

    def save_settings(self):
        try:
            s = self.data["settings"]
            s["carName"] = self.v_car_name.get().strip() or "MOJE AUTO"
            s["carSubtitle"] = self.v_car_sub.get().strip() or "DZIENNIK POKŁADOWY"
            s["consumptionOkTo"] = float(self.v_ok_to.get().replace(",", "."))
            s["consumptionHighFrom"] = float(self.v_high_from.get().replace(",", "."))
            s["fuelPriceGrowth"] = float(self.v_growth.get().replace(",", "."))
            s["monthlyKmPlan"] = float(self.v_km_plan.get().replace(",", "."))
            s["carPrice"] = float(self.v_car_price.get().replace(",", "."))
        except Exception:
            messagebox.showerror("Błąd", "Sprawdź poprawność wpisanych liczb.")
            return
        self.persist()
        self._refresh_header()
        self.refresh_all()
        messagebox.showinfo("Zapisano", "Ustawienia zostały zapisane.")

    def export_backup(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=f"cupra-terramar-backup-{dt.date.today().isoformat()}.json",
            filetypes=[("Plik JSON", "*.json")],
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Gotowe", f"Kopia zapisana:\n{path}\n\nMożesz ją przenieść na Dysk Google ręcznie.")

    def import_backup(self):
        path = filedialog.askopenfilename(filetypes=[("Plik JSON", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception:
            messagebox.showerror("Błąd", "Nie udało się wczytać pliku.")
            return
        self.data = sanitize(raw)
        self.persist()
        self._refresh_header()
        self._sync_settings_fields()
        self.refresh_all()
        messagebox.showinfo("Gotowe", "Dane zostały zaimportowane.")

    def _sync_settings_fields(self):
        s = self.data["settings"]
        self.v_car_name.set(s["carName"])
        self.v_car_sub.set(s["carSubtitle"])
        self.v_ok_to.set(str(s["consumptionOkTo"]))
        self.v_high_from.set(str(s["consumptionHighFrom"]))
        self.v_growth.set(str(s["fuelPriceGrowth"]))
        self.v_km_plan.set(str(s["monthlyKmPlan"]))
        self.v_car_price.set(str(s["carPrice"]))


if __name__ == "__main__":
    app = CarApp()
    app.mainloop()
