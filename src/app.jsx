const {
  useState,
  useEffect,
  useMemo,
  useCallback,
  useRef
} = React;

/* ---------- THEME ---------- */
const C = {
  bg: "#0F0D0C",
  surface: "#1A1613",
  surface2: "#221D19",
  line: "#332C26",
  copper: "#C96A34",
  copperDim: "#8A5330",
  amber: "#D9A438",
  green: "#5FAE7C",
  red: "#C4483C",
  text: "#F3EEE7",
  textDim: "#9C948B",
  textFaint: "#665F58"
};

/* ---------- ICONS (inline SVG, no external deps) ---------- */
const Icon = {
  gauge: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 18}
      height={p.size || 18}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <path d="M12 14l3-3M4 12a8 8 0 1116 0" />
    </svg>
  ),
  fuel: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 18}
      height={p.size || 18}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <path d="M3 22V7a2 2 0 012-2h6a2 2 0 012 2v15M3 22h10M15 8h2l3 3v7a1 1 0 01-1 1h-1" />
      <circle cx="16.5" cy="16.5" r="1.5" />
    </svg>
  ),
  wrench: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 18}
      height={p.size || 18}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <path d="M14.7 6.3a4 4 0 11-5.4 5.4L3 18v3h3l6.3-6.3a4 4 0 015.4-5.4z" />
    </svg>
  ),
  receipt: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 18}
      height={p.size || 18}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <path d="M4 2h16v20l-3-2-3 2-3-2-3 2-3-2-3 2V2z" />
    </svg>
  ),
  trend: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 18}
      height={p.size || 18}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <path d="M3 17l6-6 4 4 8-8M17 7h4v4" />
    </svg>
  ),
  settings: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 18}
      height={p.size || 18}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <circle cx="12" cy="12" r="3" />
      <path
        d="M19.4 15a1.7 1.7 0 00.3 1.9l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.7 1.7 0 00-1.9-.3 1.7 1.7 0 00-1 1.5V21a2 2 0 01-4 0v-.1a1.7 1.7 0 00-1-1.6 1.7 1.7 0 00-1.9.3l-.1.1a2 2 0 11-2.8-2.8l.1-.1a1.7 1.7 0 00.3-1.9 1.7 1.7 0 00-1.5-1H3a2 2 0 010-4h.1a1.7 1.7 0 001.5-1 1.7 1.7 0 00-.3-1.9l-.1-.1a2 2 0 112.8-2.8l.1.1a1.7 1.7 0 001.9.3H9a1.7 1.7 0 001-1.5V3a2 2 0 014 0v.1a1.7 1.7 0 001 1.6 1.7 1.7 0 001.9-.3l.1-.1a2 2 0 112.8 2.8l-.1.1a1.7 1.7 0 00-.3 1.9V9a1.7 1.7 0 001.5 1H21a2 2 0 010 4h-.1a1.7 1.7 0 00-1.5 1z"
      />
    </svg>
  ),
  plus: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 16}
      height={p.size || 16}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2.5"
    >
      <path d="M12 5v14M5 12h14" />
    </svg>
  ),
  x: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 20}
      height={p.size || 20}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <path d="M18 6L6 18M6 6l12 12" />
    </svg>
  ),
  car: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 20}
      height={p.size || 20}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <path
        d="M5 17h14M5 17a2 2 0 01-2-2v-2l2-5a2 2 0 012-2h6a2 2 0 012 2l2 5v2a2 2 0 01-2 2M5 17a2 2 0 002 2 2 2 0 002-2M17 17a2 2 0 002 2 2 2 0 002-2M6 12h12"
      />
    </svg>
  ),
  alert: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 18}
      height={p.size || 18}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <path
        d="M12 9v4M12 17h.01M10.3 3.9L2.4 18a2 2 0 001.7 3h15.8a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z"
      />
    </svg>
  ),
  drop: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 18}
      height={p.size || 18}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <path d="M12 2s7 8 7 13a7 7 0 11-14 0c0-5 7-13 7-13z" />
    </svg>
  ),
  money: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 18}
      height={p.size || 18}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <rect x="2" y="6" width="20" height="12" rx="2" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  ),
  shield: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 18}
      height={p.size || 18}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
  ),
  calendar: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 18}
      height={p.size || 18}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <rect x="3" y="4" width="18" height="18" rx="2" />
      <path d="M16 2v4M8 2v4M3 10h18" />
    </svg>
  ),
  trash: p => (
    <svg
      viewBox="0 0 24 24"
      width={p.size || 14}
      height={p.size || 14}
      fill="none"
      stroke={p.color || "currentColor"}
      strokeWidth="2"
    >
      <path
        d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2m3 0l-1 14a2 2 0 01-2 2H7a2 2 0 01-2-2L4 6"
      />
    </svg>
  )
};

/* ---------- SEED DATA ---------- */
const SEED_TANKOWANIA = [["2026-01-17", "Pb95", 44.00, 236.71, 6715, null], ["2026-01-23", "Pb98", 55.00, 336.92, 7305, 590], ["2026-01-30", "Pb98", 52.00, 322.77, 8055, 750], ["2026-02-06", "Pb98", 55.00, 337.57, 8805, 750], ["2026-02-14", "Pb98", 53.00, 329.02, 9409, 604], ["2026-02-19", "Pb98", 53.00, 340.84, 10043, 634], ["2026-02-27", "Pb98", 55.00, 357.92, 10725, 682], ["2026-03-06", "Pb98", 55.00, 403.73, 11410, 685], ["2026-03-11", "Pb98", 50.00, 358.79, 12030, 620], ["2026-03-19", "Pb95", 55.00, 382.19, 12709, 679], ["2026-04-24", "Pb98", 49.00, 296.48, 13107, 398], ["2026-05-09", "Pb98", 51.00, 340.72, 13626, 519], ["2026-05-24", "Pb98", 53.00, 360.40, 14182, 556], ["2026-06-07", "Pb98", 50.00, 325.01, 14687, 505], ["2026-06-21", "Pb98", 54.83, 352.43, 15230, 543], ["2026-06-29", "Pb98", 55.76, 373.59, 15848, 618], ["2026-07-08", "Pb98", 51.26, 395.21, 16444, 596], ["2026-07-14", "Pb98", 52.40, 399.80, 17093, 649], ["2026-07-21", "Pb98", 46.98, 389.46, 17675, 582], ["2026-07-23", "Pb98", 49.75, 392.03, 18226, 551], ["2026-08-02", "Pb98", 52.29, 426.69, 18807, 581], ["2026-08-09", "Pb98", 47.53, 377.39, 19386, 579], ["2026-08-17", "Pb98", 53.83, 387.43, 20016, 630], ["2026-08-26", "Pb98", 49.09, 362.82, 20609, 593], ["2026-09-13", "Pb98", 47.63, 421.05, 21063, 454], ["2026-09-22", "Pb98", 51.58, 455.98, 21680, 617], ["2026-10-02", "Pb98", 51.34, 451.55, 22280, 600], ["2026-10-10", "Pb98", 53.97, 408.66, 22880, 600]].map((r, i) => {
  const [date, fuelType, liters, cost, mileage, distance] = r;
  const consumption = distance ? +(liters / distance * 100).toFixed(2) : null;
  return {
    id: `seed-t-${i}`,
    date,
    fuelType,
    liters,
    cost,
    pricePerL: +(cost / liters).toFixed(3),
    mileage,
    distance,
    consumption,
    note: ""
  };
});
const SEED_SERWISY = [{
  id: "seed-s-0",
  date: "2026-01-19",
  mileage: 6992,
  description: "Olej + filtr",
  price: 0,
  warranty: true,
  paidCost: 0,
  note: "W cenie zakupu auta"
}, {
  id: "seed-s-1",
  date: "2026-04-28",
  mileage: 13150,
  description: "Wymiana opon",
  price: 250,
  warranty: false,
  paidCost: 250,
  note: ""
}, {
  id: "seed-s-2",
  date: "2026-08-11",
  mileage: 19531,
  description: "Olej + filtr oleju + filtr powietrza + filtr kabinowy + śruba spustu oleju",
  price: 932.5,
  warranty: false,
  paidCost: 932.5,
  note: "Serwis w Bosh Dunst Kartuzy"
}];
const SEED_KOSZTY = [{
  id: "seed-k-0",
  date: "2026-01-14",
  type: "Zakup auta",
  description: "Cena zakupu auta",
  amount: 189500,
  oneTime: true,
  note: "Przebieg: 6715 km"
}, {
  id: "seed-k-1",
  date: "2026-01-16",
  type: "Ubezpieczenie",
  description: "Polisa OC/AC",
  amount: 3693,
  oneTime: true,
  note: ""
}, {
  id: "seed-k-2",
  date: "2026-01-16",
  type: "Akcesoria",
  description: "Kamera + karta SD",
  amount: 640.99,
  oneTime: true,
  note: ""
}, {
  id: "seed-k-3",
  date: "2026-04-28",
  type: "Opony",
  description: "Wulkanizacja: przełożenie opon",
  amount: 250,
  oneTime: true,
  note: ""
}];
const SEED_SETTINGS = {
  consumptionOkTo: 8.5,
  consumptionHighFrom: 10,
  fuelPriceGrowth: 0.05,
  monthlyKmPlan: 1500,
  carPrice: 189500,
  carName: "CUPRA TERRAMAR",
  carSubtitle: "DZIENNIK POKŁADOWY"
};
const KOSZTY_TYPES = ["Zakup auta", "Ubezpieczenie", "Serwis", "Opony", "Myjnia", "Akcesoria", "Parking", "Inne"];
const FUEL_TYPES = ["Pb95", "Pb98"];

/* ---------- HELPERS ---------- */
const pln = n => (n ?? 0).toLocaleString("pl-PL", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
}) + " zł";
const num = (n, d = 1) => n === null || n === undefined || isNaN(n) ? "—" : n.toLocaleString("pl-PL", {
  minimumFractionDigits: d,
  maximumFractionDigits: d
});
const dateFmt = d => d ? new Date(d).toLocaleDateString("pl-PL", {
  day: "2-digit",
  month: "2-digit",
  year: "numeric"
}) : "—";
const monthKey = d => d.slice(0, 7);
const monthLabel = key => {
  const [y, m] = key.split("-");
  return new Date(+y, +m - 1, 1).toLocaleDateString("pl-PL", {
    month: "short",
    year: "2-digit"
  });
};
const uid = () => Math.random().toString(36).slice(2, 10);
function statusOf(consumption, settings) {
  if (consumption === null || consumption === undefined) return null;
  if (consumption >= settings.consumptionHighFrom) return {
    label: "Wysokie",
    color: C.red
  };
  if (consumption > settings.consumptionOkTo) return {
    label: "Uwaga",
    color: C.amber
  };
  return {
    label: "OK",
    color: C.green
  };
}
function sanitize(raw) {
  const safe = raw && typeof raw === "object" ? raw : {};
  return {
    tankowania: Array.isArray(safe.tankowania) ? safe.tankowania : SEED_TANKOWANIA,
    serwisy: Array.isArray(safe.serwisy) ? safe.serwisy : SEED_SERWISY,
    koszty: Array.isArray(safe.koszty) ? safe.koszty : SEED_KOSZTY,
    settings: {
      ...SEED_SETTINGS,
      ...(safe.settings && typeof safe.settings === "object" ? safe.settings : {})
    }
  };
}
const STORAGE_KEY = "cupra-terramar-data-v1";

/* ---------- BACKUP: export / import via native share sheet or file picker ---------- */
async function exportBackup(data) {
  const filename = `cupra-terramar-kopia-${new Date().toISOString().slice(0, 10)}.json`;
  const payload = JSON.stringify(data, null, 2);
  const blob = new Blob([payload], {
    type: "application/json"
  });
  if (navigator.share && navigator.canShare) {
    try {
      const file = new File([blob], filename, {
        type: "application/json"
      });
      if (navigator.canShare({
        files: [file]
      })) {
        await navigator.share({
          files: [file],
          title: "Kopia zapasowa Cupra Terramar"
        });
        return {
          ok: true,
          method: "share"
        };
      }
    } catch (e) {
      if (e && e.name === "AbortError") return {
        ok: false,
        method: "cancelled"
      };
      // fall through to plain download
    }
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  return {
    ok: true,
    method: "download"
  };
}
function readBackupFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        resolve(sanitize(JSON.parse(reader.result)));
      } catch (e) {
        reject(new Error("Plik nie wygląda na poprawną kopię zapasową (zły format JSON)."));
      }
    };
    reader.onerror = () => reject(new Error("Nie udało się odczytać pliku."));
    reader.readAsText(file);
  });
}
/* ---------- GOOGLE SHEETS SYNC ----------
 * The Google Sheet is the shared source of truth (phone + desktop). The app keeps working on its local
 * copy; every change is queued as an operation. A sync pulls the sheet, applies the queued operations on
 * top of it, recomputes distances, writes back the tabs that changed and adopts the result locally — so an
 * entry added on another device in the meantime is never overwritten.
 * Sign-in uses the OAuth implicit flow with a full-page redirect (popups are unreliable in an installed
 * PWA on Android); the access token lives for an hour and is renewed with prompt=none.
 */
const GOOGLE = {
  clientId: "381548523018-sva56q3badtq0tuaqipd44elv1u33nj9.apps.googleusercontent.com",
  sheetId: "1qIYl3xkVN4EK62Zd_z_w_QyJvh-HVQv5-0ZD4WCvWgw",
  scope: "https://www.googleapis.com/auth/spreadsheets"
};
const SYNC_KEY = "cupra-terramar-sync-v1"; // { connected, firstDone, ops, lastSync }
const TOKEN_KEY = "cupra-terramar-google-token"; // { token, exp }
const AUTH_STATE_KEY = "cupra-terramar-google-state";
const SILENT_KEY = "cupra-terramar-google-silent-at";
const COLLECTIONS = ["tankowania", "serwisy", "koszty"];
const readJson = (key, fallback) => {
  try {
    return JSON.parse(window.localStorage.getItem(key)) ?? fallback;
  } catch (e) {
    return fallback;
  }
};
const writeJson = (key, value) => {
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch (e) {/* storage full or blocked: the in-memory state still works */}
};
const sheetId = () => window.localStorage.getItem("cupra-terramar-sheet-override") || GOOGLE.sheetId;

/* --- auth --- */
function validToken() {
  const t = readJson(TOKEN_KEY, null);
  return t && t.exp > Date.now() ? t.token : null;
}
function redirectUri() {
  return window.location.origin + window.location.pathname;
}
function startGoogleLogin(silent) {
  const state = uid() + uid();
  window.localStorage.setItem(AUTH_STATE_KEY, state);
  if (silent) window.localStorage.setItem(SILENT_KEY, String(Date.now()));
  const params = new URLSearchParams({
    client_id: GOOGLE.clientId,
    redirect_uri: redirectUri(),
    response_type: "token",
    scope: GOOGLE.scope,
    include_granted_scopes: "true",
    state
  });
  if (silent) params.set("prompt", "none");
  window.location.assign(`https://accounts.google.com/o/oauth2/v2/auth?${params}`);
}

// back from Google: #access_token=...&expires_in=...&state=... or #error=...
function consumeAuthRedirect() {
  const hash = window.location.hash.slice(1);
  if (!hash || !/(access_token|error)=/.test(hash)) return null;
  const p = new URLSearchParams(hash);
  window.history.replaceState(null, "", window.location.pathname + window.location.search);
  const expected = window.localStorage.getItem(AUTH_STATE_KEY);
  window.localStorage.removeItem(AUTH_STATE_KEY);
  if (!expected || p.get("state") !== expected) return {
    error: "state_mismatch"
  };
  if (p.get("error")) return {
    error: p.get("error")
  };
  writeJson(TOKEN_KEY, {
    token: p.get("access_token"),
    exp: Date.now() + (Number(p.get("expires_in")) || 3600) * 1000 - 60000
  });
  return {
    ok: true
  };
}

/* --- sheet <-> app rows --- */
const SERIAL_EPOCH = Date.UTC(1899, 11, 30);
const isoToSerial = iso => {
  const [y, m, d] = iso.split("-").map(Number);
  return (Date.UTC(y, m - 1, d) - SERIAL_EPOCH) / 86400000;
};
function cellDate(v) {
  if (typeof v === "number" && v > 0) {
    const d = new Date(SERIAL_EPOCH + Math.round(v) * 86400000);
    return d.toISOString().slice(0, 10);
  }
  const s = String(v ?? "").trim();
  let m = s.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (m) return s;
  m = s.match(/^(\d{1,2})[./](\d{1,2})[./](\d{4})$/);
  if (m) return `${m[3]}-${m[2].padStart(2, "0")}-${m[1].padStart(2, "0")}`;
  return null;
}
function cellNumber(v, optional = false) {
  if (typeof v === "number") return v;
  if (v === undefined || v === null || String(v).trim() === "") return optional ? null : NaN;
  const n = tryNumber(String(v));
  return n === null ? NaN : n;
}
const cellText = v => v === undefined || v === null ? "" : String(v).trim();
const yes = v => /^(tak|t|yes|true|1)$/i.test(cellText(v));
const TABLES = [{
  coll: "tankowania",
  tab: "Tankowania",
  lastCol: "J",
  order: (a, b) => byDateMileage(a, b), // defined further down; resolved at call time
  toRow: t => [t.id, isoToSerial(t.date), t.fuelType, t.liters, t.cost, t.pricePerL, t.mileage, t.distance ?? "", t.consumption ?? "", t.note || ""],
  fromRow: r => {
    const e = {
      id: cellText(r[0]),
      date: cellDate(r[1]),
      fuelType: cellText(r[2]) || "Pb98",
      liters: cellNumber(r[3]),
      cost: cellNumber(r[4]),
      mileage: cellNumber(r[6]),
      note: cellText(r[9])
    };
    if (!e.date || !(e.liters > 0) || Number.isNaN(e.cost) || Number.isNaN(e.mileage)) return null;
    // as stored in the sheet; recalcTankowania / withPrices bring them in line afterwards
    return {
      ...e,
      pricePerL: cellNumber(r[5], true),
      distance: cellNumber(r[7], true),
      consumption: cellNumber(r[8], true)
    };
  }
}, {
  coll: "serwisy",
  tab: "Serwisy",
  lastCol: "H",
  order: (a, b) => a.date < b.date ? -1 : a.date > b.date ? 1 : 0,
  toRow: s => [s.id, isoToSerial(s.date), s.mileage ?? "", s.description, s.price, s.warranty ? "TAK" : "NIE", s.paidCost, s.note || ""],
  fromRow: r => {
    const price = cellNumber(r[4], true) ?? 0;
    const warranty = yes(r[5]);
    const e = {
      id: cellText(r[0]),
      date: cellDate(r[1]),
      mileage: cellNumber(r[2], true),
      description: cellText(r[3]),
      price,
      warranty,
      paidCost: warranty ? 0 : price,
      note: cellText(r[7])
    };
    if (!e.date || !e.description || Number.isNaN(e.price) || Number.isNaN(e.mileage)) return null;
    return e;
  }
}, {
  coll: "koszty",
  tab: "Koszty",
  lastCol: "G",
  order: (a, b) => a.date < b.date ? -1 : a.date > b.date ? 1 : 0,
  toRow: k => [k.id, isoToSerial(k.date), k.type, k.description, k.amount, k.oneTime === false ? "NIE" : "TAK", k.note || ""],
  fromRow: r => {
    const type = cellText(r[2]) || "Inne";
    const e = {
      id: cellText(r[0]),
      date: cellDate(r[1]),
      type,
      description: cellText(r[3]) || type,
      amount: cellNumber(r[4]),
      oneTime: cellText(r[5]) ? yes(r[5]) : true,
      note: cellText(r[6])
    };
    if (!e.date || Number.isNaN(e.amount)) return null;
    return e;
  }
}];
const SETTING_KEYS = ["carName", "carSubtitle", "consumptionOkTo", "consumptionHighFrom", "fuelPriceGrowth", "monthlyKmPlan", "carPrice"];

/* --- Sheets API --- */
async function sheetsApi(token, path, init = {}) {
  const res = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${sheetId()}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json"
    }
  });
  if (res.status === 401) {
    window.localStorage.removeItem(TOKEN_KEY);
    const err = new Error("Sesja Google wygasła — zaloguj się ponownie.");
    err.auth = true;
    throw err;
  }
  if (!res.ok) {
    let msg = `Błąd Google Sheets (${res.status})`;
    try {
      msg += `: ${(await res.json()).error.message}`;
    } catch (e) {/* no JSON body */}
    throw new Error(msg);
  }
  return res.json();
}
async function pullSheet(token) {
  const ranges = [...TABLES.map(t => `${t.tab}!A2:${t.lastCol}`), "Ustawienia!A2:B"];
  const q = new URLSearchParams({
    valueRenderOption: "UNFORMATTED_VALUE",
    dateTimeRenderOption: "SERIAL_NUMBER"
  });
  ranges.forEach(r => q.append("ranges", r));
  const res = await sheetsApi(token, `/values:batchGet?${q}`);
  const out = {
    data: {
      settings: {}
    },
    rowCount: {},
    needsRewrite: {},
    invalid: [],
    settingRows: {}
  };
  TABLES.forEach((t, i) => {
    const rows = res.valueRanges[i].values || [];
    out.rowCount[t.tab] = rows.length;
    out.data[t.coll] = [];
    rows.forEach((r, j) => {
      if (!r.some(c => cellText(c) !== "")) return; // empty row
      const e = t.fromRow(r);
      if (!e) return out.invalid.push(`${t.tab}, wiersz ${j + 2}`);
      if (!e.id) {
        e.id = uid(); // typed by hand in the sheet: give it an ID and write it back
        out.needsRewrite[t.tab] = true;
      }
      out.data[t.coll].push(e);
    });
  });
  (res.valueRanges[TABLES.length].values || []).forEach((r, j) => {
    const key = cellText(r[0]);
    if (!SETTING_KEYS.includes(key)) return;
    out.settingRows[key] = j + 2;
    const v = r[1];
    out.data.settings[key] = key === "carName" || key === "carSubtitle" ? cellText(v) : cellNumber(v);
  });
  return out;
}

/* --- operations queue --- */
const sameEntry = (a, b) => JSON.stringify(a) === JSON.stringify(b);
function diffOps(prev, next) {
  const ops = [];
  COLLECTIONS.forEach(coll => {
    const before = new Map((prev?.[coll] || []).map(e => [e.id, e]));
    const after = new Map(next[coll].map(e => [e.id, e]));
    after.forEach((e, id) => {
      if (!sameEntry(before.get(id), e)) ops.push({
        type: "upsert",
        coll,
        entry: e
      });
    });
    before.forEach((e, id) => {
      if (!after.has(id)) ops.push({
        type: "delete",
        coll,
        id
      });
    });
  });
  if (prev && !sameEntry(prev.settings, next.settings)) ops.push({
    type: "settings",
    settings: next.settings
  });
  return ops;
}
const opKey = op => op.type === "settings" ? "settings" : `${op.coll}:${op.type === "delete" ? op.id : op.entry.id}`;
// only the latest operation per entry matters
const compactOps = ops => {
  const last = new Map();
  ops.forEach(op => {
    last.delete(opKey(op));
    last.set(opKey(op), op);
  });
  return [...last.values()];
};
function applyOps(data, ops) {
  const d = {
    ...data,
    settings: {
      ...data.settings
    }
  };
  COLLECTIONS.forEach(c => {
    d[c] = [...data[c]];
  });
  ops.forEach(op => {
    if (op.type === "settings") d.settings = {
      ...d.settings,
      ...op.settings
    };else if (op.type === "delete") d[op.coll] = d[op.coll].filter(e => e.id !== op.id);else {
      const i = d[op.coll].findIndex(e => e.id === op.entry.id);
      if (i >= 0) d[op.coll][i] = op.entry;else d[op.coll].push(op.entry);
    }
  });
  d.tankowania = recalcTankowania(d.tankowania);
  return d;
}

/* --- one sync round --- */
const withPrices = list => list.map(t => {
  const p = +(t.cost / t.liters).toFixed(3);
  return t.pricePerL === p ? t : {
    ...t,
    pricePerL: p
  };
});
// the same real event recorded on two devices (different IDs)
const SAME_EVENT = {
  tankowania: (a, b) => a.mileage === b.mileage,
  serwisy: (a, b) => a.date === b.date && (a.description === b.description || !!a.mileage && a.mileage === b.mileage),
  koszty: (a, b) => a.date === b.date && a.type === b.type && a.amount === b.amount
};
async function syncWithSheet(localData, ops, firstConnect, token) {
  const remote = await pullSheet(token);
  if (remote.invalid.length) {
    throw new Error(`W arkuszu są wiersze, których nie da się odczytać (${remote.invalid.slice(0, 3).join("; ")}${remote.invalid.length > 3 ? "…" : ""}). Popraw je — do tego czasu nic nie zostanie nadpisane.`);
  }
  const remoteSettings = Object.fromEntries(Object.entries(remote.data.settings).filter(([, v]) => v !== "" && !Number.isNaN(v)));
  const base = sanitize({
    ...remote.data,
    settings: {
      ...localData.settings,
      ...remoteSettings
    }
  });
  let pending = ops;
  if (firstConnect) {
    // first connection: keep entries that exist only on this device; the sheet wins for everything else.
    // An entry typed separately on each device has different IDs, so it is also matched by content.
    const inSheet = (c, e) => base[c].some(r => r.id === e.id || SAME_EVENT[c](r, e));
    const extra = [];
    COLLECTIONS.forEach(c => {
      localData[c].forEach(e => {
        if (!inSheet(c, e)) extra.push({
          type: "upsert",
          coll: c,
          entry: e
        });
      });
    });
    const known = op => op.type === "upsert" && !base[op.coll].some(r => r.id === op.entry.id) && inSheet(op.coll, op.entry);
    pending = [...extra, ...ops.filter(op => op.type !== "settings" && !known(op))];
  }
  const merged = applyOps(base, pending);
  merged.tankowania = withPrices(merged.tankowania);

  // rewrite a tab only when its sorted, recomputed rows differ from what the sheet holds now
  const clears = [],
    data = [];
  TABLES.forEach(t => {
    const rows = [...merged[t.coll]].sort(t.order).map(t.toRow);
    const current = remote.data[t.coll].map(t.toRow);
    const gaps = remote.rowCount[t.tab] !== remote.data[t.coll].length;
    if (!remote.needsRewrite[t.tab] && !gaps && sameEntry(rows, current)) return;
    if (rows.length) data.push({
      range: `${t.tab}!A2`,
      values: rows
    });
    if (remote.rowCount[t.tab] > rows.length) clears.push(`${t.tab}!A${rows.length + 2}:${t.lastCol}${remote.rowCount[t.tab] + 1}`);
  });
  let nextRow = Math.max(1, ...Object.values(remote.settingRows)) + 1;
  SETTING_KEYS.forEach(k => {
    if (sameEntry(merged.settings[k], remote.data.settings[k])) return;
    const row = remote.settingRows[k] || nextRow++;
    data.push({
      range: `Ustawienia!A${row}:B${row}`,
      values: [[k, merged.settings[k]]]
    });
  });
  if (clears.length) await sheetsApi(token, "/values:batchClear", {
    method: "POST",
    body: JSON.stringify({
      ranges: clears
    })
  });
  if (data.length) await sheetsApi(token, "/values:batchUpdate", {
    method: "POST",
    body: JSON.stringify({
      valueInputOption: "RAW",
      data
    })
  });
  return {
    data: merged,
    wrote: data.length + clears.length > 0
  };
}
function useCarData() {
  const [data, setDataState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [meta, setMeta] = useState(() => readJson(SYNC_KEY, {
    connected: false,
    firstDone: false,
    ops: [],
    lastSync: null
  }));
  const [syncStatus, setSyncStatus] = useState({
    state: "idle",
    message: null
  });
  const dataRef = useRef(null);
  const metaRef = useRef(meta);
  const busyRef = useRef(false);
  const updateMeta = useCallback(patch => {
    const next = {
      ...metaRef.current,
      ...(typeof patch === "function" ? patch(metaRef.current) : patch)
    };
    metaRef.current = next;
    writeJson(SYNC_KEY, next);
    setMeta(next);
  }, []);
  const adopt = useCallback(clean => {
    dataRef.current = clean;
    setDataState(clean);
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(clean));
    } catch (e) {
      setError("Zmiana zapisana tymczasowo, ale nie udało się jej utrwalić na dysku.");
    }
  }, []);
  useEffect(() => {
    const auth = consumeAuthRedirect();
    if (auth?.ok) updateMeta({
      connected: true
    });
    if (auth?.error && auth.error !== "state_mismatch") {
      setSyncStatus({
        state: "auth",
        message: auth.error === "access_denied" ? "Nie udzielono dostępu do arkusza." : "Zaloguj się do Google, żeby zsynchronizować dane."
      });
    }
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (raw) adopt(sanitize(JSON.parse(raw)));else {
        const seed = sanitize(null);
        adopt(seed);
      }
    } catch (e) {
      setError("Nie udało się wczytać zapisanych danych z pamięci telefonu. Startuję z danymi przykładowymi.");
      adopt(sanitize(null));
    } finally {
      setLoading(false);
    }
  }, []);
  const setData = useCallback(next => {
    const sane = sanitize(next);
    const clean = {
      ...sane,
      tankowania: recalcTankowania(sane.tankowania)
    };
    const ops = diffOps(dataRef.current, clean);
    if (ops.length) updateMeta(m => ({
      ops: compactOps([...m.ops, ...ops])
    }));
    adopt(clean);
  }, []);
  const sync = useCallback(async () => {
    const m = metaRef.current;
    if (!m.connected || busyRef.current || !dataRef.current) return;
    const token = validToken();
    if (!token) return setSyncStatus({
      state: "auth",
      message: "Zaloguj się do Google, żeby zsynchronizować dane."
    });
    if (!navigator.onLine) return setSyncStatus({
      state: "offline",
      message: null
    });
    busyRef.current = true;
    setSyncStatus({
      state: "syncing",
      message: null
    });
    const sentOps = m.ops;
    try {
      const res = await syncWithSheet(dataRef.current, sentOps, !m.firstDone, token);
      // edits made while the request was running stay queued and are applied on top
      const later = metaRef.current.ops.slice(sentOps.length);
      adopt(later.length ? applyOps(res.data, later) : res.data);
      updateMeta({
        ops: later,
        firstDone: true,
        lastSync: Date.now()
      });
      setSyncStatus({
        state: "ok",
        message: null
      });
    } catch (e) {
      setSyncStatus({
        state: e.auth ? "auth" : "error",
        message: e.message || "Synchronizacja nie powiodła się."
      });
    } finally {
      busyRef.current = false;
    }
  }, []);
  const connect = useCallback(() => {
    updateMeta({
      connected: true
    });
    startGoogleLogin(false);
  }, []);
  const disconnect = useCallback(() => {
    window.localStorage.removeItem(TOKEN_KEY);
    updateMeta({
      connected: false,
      firstDone: false
    });
    setSyncStatus({
      state: "idle",
      message: null
    });
  }, []);

  // after start-up: sync now, or renew an expired token without user interaction (one redirect)
  useEffect(() => {
    if (loading || !meta.connected) return;
    if (validToken()) {
      sync();
      return;
    }
    const lastSilent = Number(window.localStorage.getItem(SILENT_KEY) || 0);
    const stale = !meta.lastSync || Date.now() - meta.lastSync > 10 * 60 * 1000 || meta.ops.length > 0;
    if (navigator.onLine && stale && Date.now() - lastSilent > 5 * 60 * 1000) startGoogleLogin(true);else setSyncStatus({
      state: "auth",
      message: "Zaloguj się do Google, żeby zsynchronizować dane."
    });
  }, [loading]);
  // queued changes go out shortly after they are made
  useEffect(() => {
    if (loading || !meta.connected || !meta.ops.length || !validToken()) return undefined;
    const t = setTimeout(sync, 1500);
    return () => clearTimeout(t);
  }, [meta.ops, loading]);
  // back online / back to the app
  useEffect(() => {
    const again = () => {
      if (document.visibilityState === "visible" && metaRef.current.connected && validToken()) sync();
    };
    window.addEventListener("online", again);
    document.addEventListener("visibilitychange", again);
    return () => {
      window.removeEventListener("online", again);
      document.removeEventListener("visibilitychange", again);
    };
  }, []);
  return {
    data,
    setData,
    loading,
    error,
    sync: {
      ...syncStatus,
      connected: meta.connected,
      pending: meta.ops.length,
      lastSync: meta.lastSync,
      run: sync,
      connect,
      login: () => startGoogleLogin(false),
      disconnect
    }
  };
}

/* ---------- ERROR BOUNDARY ---------- */
class ErrorBoundary extends React.Component {
  constructor(p) {
    super(p);
    this.state = {
      hasError: false
    };
  }
  static getDerivedStateFromError() {
    return {
      hasError: true
    };
  }
  render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            minHeight: "100vh",
            background: C.bg,
            color: C.text,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            padding: 28,
            textAlign: "center",
            fontFamily: "Inter, sans-serif"
          }}
        >
          <Icon.alert size={34} color={C.red} />
          <div
            style={{
              fontSize: 16,
              fontWeight: 700,
              margin: "14px 0 6px"
            }}
          >
            Coś poszło nie tak
          </div>
          <div
            style={{
              fontSize: 13,
              color: C.textDim,
              marginBottom: 18,
              maxWidth: 320
            }}
          >
            Aplikacja napotkała błąd renderowania. Twoje zapisane dane są bezpieczne w pamięci telefonu.
          </div>
          <button
            onClick={() => this.setState({
              hasError: false
            })}
            style={{
              background: C.copper,
              color: "#100C09",
              border: "none",
              borderRadius: 10,
              padding: "11px 22px",
              fontWeight: 700
            }}
          >
            Spróbuj ponownie
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

/* ---------- UI PRIMITIVES ---------- */
function Card({
  children,
  style,
  onClick
}) {
  return (
    <div
      onClick={onClick}
      style={{
        background: C.surface,
        border: `1px solid ${C.line}`,
        borderRadius: 14,
        padding: 16,
        ...style
      }}
    >
      {children}
    </div>
  );
}
function KPI({
  icon: Ico,
  label,
  value,
  accent,
  sub,
  valueColor
}) {
  return (
    <Card
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 6,
        minHeight: 92
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 6,
          color: C.textDim,
          fontSize: 11,
          textTransform: "uppercase",
          letterSpacing: 0.6
        }}
      >
        <Ico size={13} color={accent || C.copper} />
        {label}
      </div>
      <div
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 21,
          fontWeight: 600,
          color: valueColor || C.text
        }}
      >
        {value}
      </div>
      {sub && (
        <div
          style={{
            fontSize: 11,
            color: C.textFaint,
            marginTop: -2
          }}
        >
          {sub}
        </div>
      )}
    </Card>
  );
}
function Pill({
  text,
  color
}) {
  return (
    <span
      style={{
        fontSize: 11,
        fontWeight: 600,
        color,
        background: color + "22",
        border: `1px solid ${color}55`,
        borderRadius: 999,
        padding: "2px 8px",
        whiteSpace: "nowrap"
      }}
    >
      {text}
    </span>
  );
}
function SheetModal({
  title,
  onClose,
  children
}) {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "#000000cc",
        zIndex: 50,
        display: "flex",
        alignItems: "flex-end",
        justifyContent: "center"
      }}
      onClick={onClose}
    >
      <div
        onClick={e => e.stopPropagation()}
        style={{
          background: C.surface2,
          width: "100%",
          maxWidth: 480,
          maxHeight: "88vh",
          overflowY: "auto",
          borderRadius: "20px 20px 0 0",
          border: `1px solid ${C.line}`,
          borderBottom: "none",
          padding: "18px 18px 28px"
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: 16
          }}
        >
          <h3
            style={{
              margin: 0,
              color: C.text,
              fontSize: 17
            }}
          >
            {title}
          </h3>
          <button
            onClick={onClose}
            style={{
              background: "none",
              border: "none",
              color: C.textDim
            }}
          >
            <Icon.x />
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}
function Field({
  label,
  children
}) {
  return (
    <label
      style={{
        display: "block",
        marginBottom: 12
      }}
    >
      <div
        style={{
          fontSize: 12,
          color: C.textDim,
          marginBottom: 5
        }}
      >
        {label}
      </div>
      {children}
    </label>
  );
}
const inputStyle = {
  width: "100%",
  boxSizing: "border-box",
  background: C.bg,
  border: `1px solid ${C.line}`,
  borderRadius: 10,
  padding: "10px 12px",
  color: C.text,
  fontSize: 14,
  outline: "none"
};
function PrimaryButton({
  children,
  onClick,
  disabled
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        width: "100%",
        padding: 13,
        borderRadius: 12,
        border: "none",
        background: disabled ? C.copperDim : C.copper,
        color: "#100C09",
        fontWeight: 700,
        fontSize: 14.5,
        cursor: disabled ? "not-allowed" : "pointer",
        marginTop: 6
      }}
    >
      {children}
    </button>
  );
}
const addBtnStyle = {
  display: "flex",
  alignItems: "center",
  gap: 5,
  background: C.copper,
  color: "#100C09",
  border: "none",
  borderRadius: 10,
  padding: "8px 12px",
  fontWeight: 700,
  fontSize: 13,
  cursor: "pointer"
};
const trashBtn = {
  background: "none",
  border: "none",
  color: C.textFaint,
  cursor: "pointer",
  padding: 4
};
const toggleBtn = active => ({
  flex: 1,
  padding: 9,
  borderRadius: 9,
  border: `1px solid ${active ? C.copper : C.line}`,
  background: active ? C.copper + "22" : "transparent",
  color: active ? C.copper : C.textDim,
  fontWeight: 600,
  fontSize: 13,
  cursor: "pointer"
});

/* ---------- INTERACTIVE CHART (no external chart library) ---------- */
function niceMaxOf(v) {
  if (v <= 0) return 1;
  const mag = Math.pow(10, Math.floor(Math.log10(v)));
  const norm = v / mag;
  const step = norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 5 ? 5 : 10;
  return step * mag;
}
function MiniChart({
  data,
  valueKey,
  labelKey,
  type = "bar",
  color,
  formatValue,
  unit
}) {
  const [active, setActive] = useState(null);
  const values = data.map(d => d[valueKey]).filter(v => v !== null && v !== undefined);
  if (!values.length) return null;
  const fmt = formatValue || (v => num(v, 0));
  const rawMax = Math.max(...values, 0);
  const niceMax = niceMaxOf(rawMax * 1.1);
  const w = 320,
    h = 170,
    padL = 40,
    padR = 8,
    padT = 10,
    padB = 24;
  const plotW = w - padL - padR,
    plotH = h - padT - padB;
  const yFor = v => padT + plotH - Math.max(0, v) / niceMax * plotH;
  const xFor = i => padL + (data.length <= 1 ? plotW / 2 : i / (data.length - 1) * plotW);
  const yTicks = 4;
  const grid = Array.from({
    length: yTicks + 1
  }, (_, i) => {
    const v = niceMax / yTicks * i;
    return {
      v,
      y: yFor(v)
    };
  });
  const handlePick = i => setActive(prev => prev === i ? null : i);
  return (
    <div>
      <svg viewBox={`0 0 ${w} ${h}`} width="100%" height={h}>
        {grid.map((g, i) => (
          <g key={i}>
            <line x1={padL} y1={g.y} x2={w - padR} y2={g.y} stroke={C.line} strokeWidth="1" />
            <text x={padL - 6} y={g.y + 3} fontSize="8" fill={C.textFaint} textAnchor="end">
              {fmt(g.v)}
            </text>
          </g>
        ))}
        {type === "bar" ? data.map((d, i) => {
          const v = d[valueKey] || 0;
          const bw = Math.max(6, plotW / data.length * 0.55);
          const x = xFor(i) - bw / 2;
          const y = yFor(v);
          const isActive = active === i;
          return (
            <g
              key={i}
              onClick={() => handlePick(i)}
              style={{
                cursor: "pointer"
              }}
            >
              <rect
                x={xFor(i) - plotW / data.length / 2}
                y={padT}
                width={plotW / data.length}
                height={plotH}
                fill="transparent"
              />
              <rect
                x={x}
                y={y}
                width={bw}
                height={Math.max(1, padT + plotH - y)}
                rx="3"
                fill={color}
                opacity={isActive ? 1 : 0.78}
              />
            </g>
          );
        }) : (
          <>
            <path
              d={data.map((d, i) => {
                const v = d[valueKey];
                if (v === null || v === undefined) return null;
                return `${i === 0 || data[i - 1][valueKey] == null ? "M" : "L"}${xFor(i)},${yFor(v)}`;
              }).filter(Boolean).join(" ")}
              fill="none"
              stroke={color}
              strokeWidth="2"
            />
            {data.map((d, i) => {
              const v = d[valueKey];
              if (v === null || v === undefined) return null;
              const isActive = active === i;
              return (
                <g
                  key={i}
                  onClick={() => handlePick(i)}
                  style={{
                    cursor: "pointer"
                  }}
                >
                  <circle cx={xFor(i)} cy={yFor(v)} r="11" fill="transparent" />
                  <circle
                    cx={xFor(i)}
                    cy={yFor(v)}
                    r={isActive ? 5 : 2.5}
                    fill={isActive ? C.text : color}
                    stroke={color}
                    strokeWidth={isActive ? 2 : 0}
                  />
                </g>
              );
            })}
          </>
        )}
        {data.map((d, i) => {
          const show = i === 0 || i === data.length - 1 || i === active;
          if (!show) return null;
          return (
            <text
              key={i}
              x={xFor(i)}
              y={h - 6}
              fontSize="8"
              fill={active === i ? C.text : C.textFaint}
              textAnchor="middle"
            >
              {d[labelKey]}
            </text>
          );
        })}
        {active !== null && (
          <line
            x1={xFor(active)}
            y1={padT}
            x2={xFor(active)}
            y2={padT + plotH}
            stroke={color}
            strokeWidth="1"
            strokeDasharray="3,3"
            opacity="0.5"
          />
        )}
      </svg>
      <div
        style={{
          textAlign: "center",
          marginTop: 2,
          fontSize: 12,
          minHeight: 16,
          fontFamily: "'JetBrains Mono', monospace",
          color: active !== null ? C.text : "transparent"
        }}
      >
        {active !== null && data[active] ? `${data[active][labelKey]} · ${fmt(data[active][valueKey])}${unit ? " " + unit : ""}` : "—"}
      </div>
    </div>
  );
}

/* ---------- GAUGE ---------- */
function ConsumptionGauge({
  value,
  settings
}) {
  const max = Math.max(settings.consumptionHighFrom * 1.4, value ? value * 1.15 : 12);
  const pct = value ? Math.min(value / max, 1) : 0;
  const r = 54,
    circ = 2 * Math.PI * r;
  const status = statusOf(value, settings);
  const color = status ? status.color : C.textFaint;
  return (
    <>
    <div
      style={{
        position: "relative",
        width: 140,
        height: 140,
        margin: "0 auto"
      }}
    >
      <svg
        width="140"
        height="140"
        viewBox="0 0 140 140"
        style={{
          transform: "rotate(-90deg)"
        }}
      >
        <circle cx="70" cy="70" r={r} fill="none" stroke={C.line} strokeWidth="10" />
        <circle
          cx="70"
          cy="70"
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeDasharray={circ}
          strokeDashoffset={circ * (1 - pct)}
          strokeLinecap="round"
          style={{
            transition: "stroke-dashoffset 0.6s ease"
          }}
        />
      </svg>
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center"
        }}
      >
        <div
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 26,
            fontWeight: 700,
            color: C.text
          }}
        >
          {value ? num(value, 1) : "—"}
        </div>
        <div
          style={{
            fontSize: 10.5,
            color: C.textDim
          }}
        >
          l / 100km
        </div>
      </div>
    </div>
    {status && (
      // below the ring: the longer labels ("Podwyższone") would overlap the arc inside it
      <div
        style={{
          marginTop: 8
        }}
      >
        <Pill text={STATUS_TEXT[status.label]} color={status.color} />
      </div>
    )}
    </>
  );
}

/* ---------- AGGREGATION ---------- */
function useAggregates(data) {
  return useMemo(() => {
    const {
      tankowania,
      serwisy,
      koszty,
      settings
    } = data;
    const validDist = tankowania.filter(t => t.distance);
    const totalLiters = tankowania.reduce((s, t) => s + t.liters, 0);
    const totalFuelCost = tankowania.reduce((s, t) => s + t.cost, 0);
    const totalDistance = validDist.reduce((s, t) => s + t.distance, 0);
    const litersForDistance = validDist.reduce((s, t) => s + t.liters, 0);
    const weightedConsumption = totalDistance ? litersForDistance / totalDistance * 100 : null;
    const avgPricePerL = totalLiters ? totalFuelCost / totalLiters : null;
    const paidService = serwisy.reduce((s, x) => s + (x.paidCost || 0), 0);
    const kosztyTotal = koszty.reduce((s, x) => s + (x.amount || 0), 0);
    const totalCost = totalFuelCost + paidService + kosztyTotal;
    const costPerKm = totalDistance ? totalCost / totalDistance : null;
    const alerts = tankowania.filter(t => statusOf(t.consumption, settings)?.label === "Wysokie").length;
    const lastService = serwisy.slice().sort((a, b) => a.date < b.date ? 1 : -1)[0];
    const monthMap = {};
    tankowania.forEach(t => {
      const k = monthKey(t.date);
      monthMap[k] = monthMap[k] || {
        fuelCost: 0,
        liters: 0,
        distance: 0,
        litersForDist: 0,
        paidService: 0,
        extra: 0
      };
      monthMap[k].fuelCost += t.cost;
      monthMap[k].liters += t.liters;
      if (t.distance) {
        monthMap[k].distance += t.distance;
        monthMap[k].litersForDist += t.liters;
      }
    });
    serwisy.forEach(s => {
      if (!s.date) return;
      const k = monthKey(s.date);
      monthMap[k] = monthMap[k] || {
        fuelCost: 0,
        liters: 0,
        distance: 0,
        litersForDist: 0,
        paidService: 0,
        extra: 0
      };
      monthMap[k].paidService += s.paidCost || 0;
    });
    koszty.forEach(c => {
      if (c.type === "Zakup auta") return;
      const k = monthKey(c.date);
      monthMap[k] = monthMap[k] || {
        fuelCost: 0,
        liters: 0,
        distance: 0,
        litersForDist: 0,
        paidService: 0,
        extra: 0
      };
      monthMap[k].extra += c.amount || 0;
    });
    const monthly = Object.entries(monthMap).sort(([a], [b]) => a < b ? -1 : 1).map(([k, v]) => {
      const total = v.fuelCost + v.paidService + v.extra;
      return {
        key: k,
        label: monthLabel(k),
        fuelCost: v.fuelCost,
        distance: v.distance,
        consumption: v.distance ? v.litersForDist / v.distance * 100 : null,
        paidService: v.paidService,
        extra: v.extra,
        total,
        costPerKm: v.distance ? total / v.distance : null
      };
    });
    return {
      totalLiters,
      totalFuelCost,
      totalDistance,
      weightedConsumption,
      avgPricePerL,
      paidService,
      kosztyTotal,
      totalCost,
      costPerKm,
      alerts,
      lastService,
      monthly
    };
  }, [data]);
}

/* ---------- TAB: DASHBOARD ---------- */
function Dashboard({
  agg,
  settings,
  tankowania
}) {
  const chartData = agg.monthly.filter(m => m.total > 0);
  const lastFill = [...tankowania].sort(byDateMileage).pop();
  const fuelPerKm = agg.totalDistance ? agg.totalFuelCost / agg.totalDistance : null;
  const ls = agg.lastService;
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 14
      }}
    >
      <Card
        style={{
          textAlign: "center",
          paddingTop: 20,
          paddingBottom: 12
        }}
      >
        <div
          style={{
            fontSize: 11,
            color: C.textDim,
            textTransform: "uppercase",
            letterSpacing: 1,
            marginBottom: 4
          }}
        >
          Średnie spalanie
        </div>
        <ConsumptionGauge value={agg.weightedConsumption} settings={settings} />
      </Card>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 10
        }}
      >
        <KPI
          icon={Icon.money}
          label="Koszt całkowity"
          value={pln(agg.totalCost)}
          sub={`paliwo ${pln(agg.totalFuelCost)}`}
        />
        <KPI
          icon={Icon.gauge}
          label="Dystans"
          value={`${num(agg.totalDistance, 0)} km`}
          sub={plural(tankowania.length, "tankowanie", "tankowania", "tankowań")}
        />
        <KPI
          icon={Icon.trend}
          label="Koszt / km"
          value={agg.costPerKm ? `${num(agg.costPerKm, 2)} zł` : "—"}
          sub={fuelPerKm ? `samo paliwo ${num(fuelPerKm, 2)} zł` : null}
        />
        <KPI
          icon={Icon.drop}
          label="Śr. cena / l"
          value={agg.avgPricePerL ? `${num(agg.avgPricePerL, 2)} zł` : "—"}
          sub={lastFill ? `ostatnio ${num(lastFill.pricePerL, 2)} zł` : null}
        />
        <KPI
          icon={Icon.alert}
          label="Alerty spalania"
          value={agg.alerts}
          accent={agg.alerts ? C.red : C.green}
          valueColor={agg.alerts ? C.red : null}
          sub={`≥ ${num(settings.consumptionHighFrom, 1)} l/100km`}
        />
        <KPI
          icon={Icon.shield}
          label="Ostatni serwis"
          value={ls ? dateFmt(ls.date) : "—"}
          sub={ls ? [ls.mileage ? `${num(ls.mileage, 0)} km` : null, ls.warranty ? "gwarancja" : pln(ls.price)].filter(Boolean).join(" · ") : null}
        />
      </div>
      {chartData.length > 0 && (
        <Card>
          <div
            style={{
              fontSize: 12.5,
              color: C.textDim,
              marginBottom: 2,
              fontWeight: 600
            }}
          >
            Koszty miesięczne
          </div>
          <div
            style={{
              fontSize: 10.5,
              color: C.textFaint,
              marginBottom: 6
            }}
          >
            Stuknij słupek, żeby zobaczyć dokładną kwotę
          </div>
          <MiniChart
            data={chartData}
            valueKey="total"
            labelKey="label"
            type="bar"
            color={C.copper}
            formatValue={v => `${Math.round(v)} zł`}
          />
        </Card>
      )}
      {chartData.length > 1 && (
        <Card>
          <div
            style={{
              fontSize: 12.5,
              color: C.textDim,
              marginBottom: 2,
              fontWeight: 600
            }}
          >
            Spalanie w czasie
          </div>
          <div
            style={{
              fontSize: 10.5,
              color: C.textFaint,
              marginBottom: 6
            }}
          >
            Stuknij punkt, żeby zobaczyć wartość dla danego miesiąca
          </div>
          <MiniChart
            data={chartData}
            valueKey="consumption"
            labelKey="label"
            type="line"
            color={C.amber}
            formatValue={v => num(v, 1)}
            unit="l/100km"
          />
        </Card>
      )}
    </div>
  );
}

/* ---------- FORM HELPERS ---------- */
const MONTHS_FULL = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"];
const MONTHS_SHORT = ["sty", "lut", "mar", "kwi", "maj", "cze", "lip", "sie", "wrz", "paź", "lis", "gru"];
const STATUS_TEXT = {
  OK: "W normie",
  Uwaga: "Podwyższone",
  Wysokie: "Wysokie"
};
const plural = (n, one, few, many) => {
  if (n === 1) return `${n} ${one}`;
  const few_ = n % 10 >= 2 && n % 10 <= 4 && !(n % 100 >= 12 && n % 100 <= 14);
  return `${n} ${few_ ? few : many}`;
};
const localIso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
const todayIso = (daysAgo = 0) => {
  const d = new Date();
  d.setDate(d.getDate() - daysAgo);
  return localIso(d);
};
const numIn = v => v === null || v === undefined ? "" : String(v).replace(".", ",");

// "1 234,5" -> 1234.5; throws an Error with a message shown under the field
function parseNumber(raw, {
  integer = false,
  optional = false,
  min = null
} = {}) {
  const s = String(raw ?? "").replace(/[\s ]/g, "").replace(",", ".");
  if (!s) {
    if (optional) return null;
    throw new Error("To pole jest wymagane");
  }
  if (!(integer ? /^-?\d+$/ : /^-?\d+(\.\d+)?$/).test(s)) {
    throw new Error(integer ? "Wpisz liczbę całkowitą" : "Wpisz liczbę, np. 52,4");
  }
  const v = integer ? parseInt(s, 10) : parseFloat(s);
  if (min !== null && v < min) throw new Error(`Wartość musi być ≥ ${num(min, 0)}`);
  return v;
}
const tryNumber = (raw, opts) => {
  try {
    return parseNumber(raw, opts);
  } catch (e) {
    return null;
  }
};

// runs every rule, collecting values and per-field error messages
function validate(rules) {
  const values = {},
    errors = {};
  Object.entries(rules).forEach(([key, fn]) => {
    try {
      values[key] = fn();
    } catch (e) {
      errors[key] = e.message;
    }
  });
  return {
    values,
    errors,
    ok: Object.keys(errors).length === 0
  };
}
const byDateMileage = (a, b) => a.date === b.date ? a.mileage - b.mileage : a.date < b.date ? -1 : 1;

// distance and consumption follow from the mileage difference to the previous fill-up (as in the xlsx)
function recalcTankowania(list) {
  const order = list.map((t, i) => [t, i]).sort((a, b) => byDateMileage(a[0], b[0]));
  const out = list.slice();
  let prev = null;
  order.forEach(([t, i]) => {
    const distance = prev ? t.mileage - prev.mileage : null;
    const consumption = distance && distance > 0 ? +(t.liters / distance * 100).toFixed(2) : null;
    out[i] = t.distance === distance && t.consumption === consumption ? t : {
      ...t,
      distance,
      consumption
    };
    prev = t;
  });
  return out;
}
const upsertEntry = (data, coll, entry, values) => ({
  ...data,
  [coll]: entry ? data[coll].map(x => x.id === entry.id ? {
    ...x,
    ...values
  } : x) : [...data[coll], {
    id: uid(),
    ...values
  }]
});
const removeEntry = (data, coll, entry) => ({
  ...data,
  [coll]: data[coll].filter(x => x.id !== entry.id)
});

/* ---------- FORM PRIMITIVES ---------- */
function FormField({
  label,
  hint,
  error,
  children
}) {
  return (
    <div
      style={{
        marginBottom: 12
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          fontSize: 12,
          color: C.textDim,
          marginBottom: 5
        }}
      >
        <span>{label}</span>
        {hint && (
          <span
            style={{
              color: C.textFaint,
              fontSize: 11
            }}
          >
            {hint}
          </span>
        )}
      </div>
      {children}
      {error && (
        <div
          style={{
            color: C.red,
            fontSize: 11.5,
            marginTop: 4
          }}
        >
          {error}
        </div>
      )}
    </div>
  );
}
function TextInput({
  value,
  onChange,
  suffix,
  error,
  inputMode = "text",
  placeholder
}) {
  return (
    <div
      style={{
        position: "relative"
      }}
    >
      <input
        type="text"
        inputMode={inputMode}
        value={value}
        placeholder={placeholder}
        onChange={e => onChange(e.target.value)}
        style={{
          ...inputStyle,
          border: `1px solid ${error ? C.red : C.line}`,
          paddingRight: suffix ? 44 : 12
        }}
      />
      {suffix && (
        <span
          style={{
            position: "absolute",
            right: 12,
            top: "50%",
            transform: "translateY(-50%)",
            color: C.textFaint,
            fontSize: 12,
            pointerEvents: "none"
          }}
        >
          {suffix}
        </span>
      )}
    </div>
  );
}
function DateInput({
  value,
  onChange,
  error
}) {
  const chip = (text, daysAgo) => {
    const iso = todayIso(daysAgo);
    return (
      <button
        type="button"
        onClick={() => onChange(iso)}
        style={{
          ...toggleBtn(value === iso),
          flex: "none",
          padding: "9px 12px"
        }}
      >
        {text}
      </button>
    );
  };
  return (
    <div
      style={{
        display: "flex",
        gap: 6
      }}
    >
      <input
        type="date"
        value={value}
        onChange={e => onChange(e.target.value)}
        style={{
          ...inputStyle,
          flex: 1,
          minWidth: 0,
          border: `1px solid ${error ? C.red : C.line}`,
          colorScheme: "dark"
        }}
      />
      {chip("Dziś", 0)}
      {chip("Wczoraj", 1)}
    </div>
  );
}
function Segmented({
  options,
  value,
  onChange
}) {
  return (
    <div
      style={{
        display: "flex",
        gap: 6
      }}
    >
      {options.map(o => (
        <button key={o} type="button" onClick={() => onChange(o)} style={toggleBtn(o === value)}>
          {o}
        </button>
      ))}
    </div>
  );
}
function SwitchRow({
  label,
  sub,
  checked,
  onChange
}) {
  return (
    <button
      type="button"
      onClick={() => onChange(!checked)}
      style={{
        width: "100%",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        background: C.bg,
        border: `1px solid ${C.line}`,
        borderRadius: 12,
        padding: "10px 12px",
        marginBottom: 12,
        cursor: "pointer",
        textAlign: "left"
      }}
    >
      <span>
        <span
          style={{
            display: "block",
            color: C.text,
            fontSize: 13.5,
            fontWeight: 600
          }}
        >
          {label}
        </span>
        <span
          style={{
            display: "block",
            color: C.textFaint,
            fontSize: 11
          }}
        >
          {sub}
        </span>
      </span>
      <span
        style={{
          width: 42,
          height: 24,
          borderRadius: 99,
          background: checked ? C.copper : C.line,
          position: "relative",
          transition: "background .2s",
          flex: "none"
        }}
      >
        <span
          style={{
            position: "absolute",
            top: 3,
            left: checked ? 21 : 3,
            width: 18,
            height: 18,
            borderRadius: 99,
            background: C.text,
            transition: "left .2s"
          }}
        />
      </span>
    </button>
  );
}
function SummaryBox({
  items
}) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: `repeat(${items.length}, 1fr)`,
        background: C.bg,
        border: `1px solid ${C.line}`,
        borderRadius: 12,
        padding: "10px 12px",
        marginBottom: 8
      }}
    >
      {items.map(([label, value, color]) => (
        <div key={label}>
          <div
            style={{
              fontSize: 10.5,
              color: C.textFaint
            }}
          >
            {label}
          </div>
          <div
            style={{
              fontFamily: "'Space Grotesk', sans-serif",
              fontWeight: 700,
              fontSize: 15,
              color: color || C.text,
              marginTop: 2
            }}
          >
            {value}
          </div>
        </div>
      ))}
    </div>
  );
}
function ConfirmSheet({
  title,
  message,
  confirmText,
  danger = true,
  onConfirm,
  onCancel
}) {
  return (
    <SheetModal title={title} onClose={onCancel}>
      <div
        style={{
          color: C.textDim,
          fontSize: 13.5,
          lineHeight: 1.5,
          marginBottom: 16
        }}
      >
        {message}
      </div>
      <div
        style={{
          display: "flex",
          gap: 8
        }}
      >
        <button
          type="button"
          onClick={onCancel}
          style={{
            ...toggleBtn(false),
            padding: 12,
            color: C.text
          }}
        >
          Anuluj
        </button>
        <button
          type="button"
          onClick={onConfirm}
          style={{
            ...toggleBtn(false),
            padding: 12,
            background: danger ? C.red : C.copper,
            border: "none",
            color: danger ? "#FFFFFF" : "#100C09"
          }}
        >
          {confirmText}
        </button>
      </div>
    </SheetModal>
  );
}

// add/edit sheet with Anuluj / Zapisz and, when editing, Usuń behind a confirmation
function EntrySheet({
  title,
  entry,
  deleteLabel,
  onClose,
  onSave,
  onDelete,
  children
}) {
  const [confirming, setConfirming] = useState(false);
  return (
    <>
      <SheetModal title={title} onClose={onClose}>
        {children}
        <div
          style={{
            display: "flex",
            gap: 8,
            marginTop: 8,
            alignItems: "center"
          }}
        >
          {entry && (
            <button
              type="button"
              onClick={() => setConfirming(true)}
              style={{
                background: "none",
                border: "none",
                color: C.red,
                display: "flex",
                alignItems: "center",
                gap: 5,
                fontSize: 13.5,
                padding: "10px 4px",
                cursor: "pointer"
              }}
            >
              <Icon.trash />
              Usuń
            </button>
          )}
          <div
            style={{
              flex: 1
            }}
          />
          <button
            type="button"
            onClick={onClose}
            style={{
              ...toggleBtn(false),
              flex: "none",
              padding: "12px 16px",
              color: C.text
            }}
          >
            Anuluj
          </button>
          <button
            type="button"
            onClick={onSave}
            style={{
              ...addBtnStyle,
              padding: "12px 18px",
              fontSize: 14
            }}
          >
            {entry ? "Zapisz zmiany" : "Zapisz"}
          </button>
        </div>
      </SheetModal>
      {confirming && (
        <ConfirmSheet
          title="Usunąć wpis?"
          message={`Czy na pewno usunąć ${deleteLabel}? Tej operacji nie można cofnąć.`}
          confirmText="Usuń"
          onCancel={() => setConfirming(false)}
          onConfirm={onDelete}
        />
      )}
    </>
  );
}

/* ---------- LISTS ---------- */
function ListHeader({
  text,
  onAdd
}) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 4,
        gap: 10
      }}
    >
      <div
        style={{
          color: C.textDim,
          fontSize: 12
        }}
      >
        {text}
      </div>
      <button onClick={onAdd} style={addBtnStyle}>
        <Icon.plus />
        Dodaj
      </button>
    </div>
  );
}
function EmptyList({
  text
}) {
  return (
    <div
      style={{
        textAlign: "center",
        color: C.textFaint,
        fontSize: 13,
        padding: "48px 0"
      }}
    >
      {text}
    </div>
  );
}

// newest first, grouped by month with a per-month summary
function MonthGroups({
  entries,
  compare,
  groupSummary,
  renderRow
}) {
  const sorted = [...entries].sort((a, b) => -compare(a, b));
  const groups = [];
  sorted.forEach(e => {
    const k = monthKey(e.date);
    if (!groups.length || groups[groups.length - 1].key !== k) groups.push({
      key: k,
      items: []
    });
    groups[groups.length - 1].items.push(e);
  });
  return groups.map(g => {
    const [y, m] = g.key.split("-");
    return (
      <div key={g.key}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "baseline",
            padding: "14px 2px 7px"
          }}
        >
          <span
            style={{
              color: C.textDim,
              fontSize: 12.5,
              fontWeight: 600
            }}
          >
            {MONTHS_FULL[+m - 1]} {y}
          </span>
          <span
            style={{
              color: C.textFaint,
              fontSize: 11.5
            }}
          >
            {groupSummary(g.items)}
          </span>
        </div>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 8
          }}
        >
          {g.items.map(renderRow)}
        </div>
      </div>
    );
  });
}
function EntryRow({
  date,
  title,
  sub,
  amount,
  badge,
  onOpen
}) {
  const [, m, d] = date.split("-").map(Number);
  return (
    <Card
      onClick={onOpen}
      style={{
        padding: 10,
        display: "flex",
        alignItems: "center",
        gap: 12,
        cursor: "pointer"
      }}
    >
      <div
        style={{
          width: 46,
          height: 46,
          borderRadius: 10,
          background: C.surface2,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          flex: "none"
        }}
      >
        <div
          style={{
            fontFamily: "'Space Grotesk', sans-serif",
            fontWeight: 700,
            fontSize: 17,
            lineHeight: 1,
            color: C.text
          }}
        >
          {d}
        </div>
        <div
          style={{
            fontSize: 9.5,
            color: C.textFaint,
            marginTop: 3
          }}
        >
          {MONTHS_SHORT[m - 1]}
        </div>
      </div>
      <div
        style={{
          flex: 1,
          minWidth: 0
        }}
      >
        <div
          style={{
            color: C.text,
            fontWeight: 600,
            fontSize: 14,
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis"
          }}
        >
          {title}
        </div>
        <div
          style={{
            color: C.textDim,
            fontSize: 12,
            marginTop: 2,
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis"
          }}
        >
          {sub}
        </div>
      </div>
      <div
        style={{
          textAlign: "right",
          flex: "none"
        }}
      >
        <div
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontWeight: 600,
            color: C.text,
            fontSize: 13.5
          }}
        >
          {amount}
        </div>
        {badge && (
          <div
            style={{
              marginTop: 4
            }}
          >
            <Pill text={badge.text} color={badge.color} />
          </div>
        )}
      </div>
    </Card>
  );
}
const sumBy = (list, key) => list.reduce((s, x) => s + (x[key] || 0), 0);

/* ---------- TAB: TANKOWANIA ---------- */
function TankowaniaTab({
  data,
  setData,
  notify
}) {
  const {
    tankowania,
    settings
  } = data;
  const [editing, setEditing] = useState(null);
  return (
    <div>
      <ListHeader
        text={tankowania.length ? `${plural(tankowania.length, "tankowanie", "tankowania", "tankowań")} · ${pln(sumBy(tankowania, "cost"))}` : ""}
        onAdd={() => setEditing({
          entry: null
        })}
      />
      {tankowania.length === 0 ? <EmptyList text="Brak tankowań — dodaj pierwsze." /> : (
        <MonthGroups
          entries={tankowania}
          compare={byDateMileage}
          groupSummary={g => `${num(sumBy(g, "liters"), 1)} l · ${pln(sumBy(g, "cost"))}`}
          renderRow={t => {
            const st = statusOf(t.consumption, settings);
            return (
              <EntryRow
                key={t.id}
                date={t.date}
                title={`${t.fuelType} · ${num(t.liters, 2)} l`}
                sub={`${num(t.mileage, 0)} km${t.distance ? ` (+${num(t.distance, 0)} km)` : ""} · ${num(t.pricePerL, 2)} zł/l${t.note ? ` · ${t.note}` : ""}`}
                amount={pln(t.cost)}
                badge={st && {
                  text: `${num(t.consumption, 2)} l/100`,
                  color: st.color
                }}
                onOpen={() => setEditing({
                  entry: t
                })}
              />
            );
          }}
        />
      )}
      {editing && (
        <TankowanieSheet
          data={data}
          setData={setData}
          notify={notify}
          entry={editing.entry}
          onClose={() => setEditing(null)}
        />
      )}
    </div>
  );
}
function TankowanieSheet({
  data,
  setData,
  notify,
  entry,
  onClose
}) {
  const latest = [...data.tankowania].sort(byDateMileage).pop();
  const [f, setF] = useState(() => entry ? {
    date: entry.date,
    fuelType: entry.fuelType,
    liters: numIn(entry.liters),
    cost: numIn(entry.cost),
    mileage: String(entry.mileage),
    note: entry.note || ""
  } : {
    date: todayIso(),
    fuelType: latest?.fuelType || "Pb98",
    liters: "",
    cost: "",
    mileage: "",
    note: ""
  });
  const [errors, setErrors] = useState({});
  const set = key => value => {
    setF(prev => ({
      ...prev,
      [key]: value
    }));
    setErrors(prev => ({
      ...prev,
      [key]: undefined
    }));
  };
  // an older entry may use a fuel type that is no longer offered; keep it selectable for that entry
  const fuels = FUEL_TYPES.includes(f.fuelType) ? FUEL_TYPES : [...FUEL_TYPES, f.fuelType];

  // live preview of price per litre, distance and consumption
  const others = data.tankowania.filter(t => !entry || t.id !== entry.id);
  const previousOf = (date, mileage) => others.filter(t => byDateMileage(t, {
    date,
    mileage
  }) < 0).sort(byDateMileage).pop();
  const liters = tryNumber(f.liters),
    cost = tryNumber(f.cost),
    mileage = tryNumber(f.mileage, {
      integer: true
    });
  const prev = f.date && mileage !== null ? previousOf(f.date, mileage) : null;
  const hintPrev = prev || (entry ? previousOf(entry.date, entry.mileage) : latest);
  const dist = prev && mileage !== null ? mileage - prev.mileage : null;
  const cons = liters && dist > 0 ? liters / dist * 100 : null;
  const st = statusOf(cons, data.settings);
  const save = () => {
    const r = validate({
      date: () => {
        if (!f.date) throw new Error("Wybierz datę");
        return f.date;
      },
      liters: () => parseNumber(f.liters, {
        min: 0.01
      }),
      cost: () => parseNumber(f.cost, {
        min: 0
      }),
      mileage: () => parseNumber(f.mileage, {
        integer: true,
        min: 0
      })
    });
    if (!r.ok) return setErrors(r.errors);
    const v = r.values;
    setData(upsertEntry(data, "tankowania", entry, {
      date: v.date,
      fuelType: f.fuelType,
      liters: v.liters,
      cost: v.cost,
      pricePerL: +(v.cost / v.liters).toFixed(3),
      mileage: v.mileage,
      note: f.note.trim()
    }));
    notify(`Zapisano tankowanie z ${dateFmt(v.date)}`);
    onClose();
  };
  const remove = () => {
    setData(removeEntry(data, "tankowania", entry));
    notify(`Usunięto tankowanie z ${dateFmt(entry.date)}`, "warn");
    onClose();
  };
  return (
    <EntrySheet
      title={entry ? "Edycja tankowania" : "Nowe tankowanie"}
      entry={entry}
      deleteLabel={entry ? `tankowanie z ${dateFmt(entry.date)}` : ""}
      onClose={onClose}
      onSave={save}
      onDelete={remove}
    >
      <FormField label="Data" error={errors.date}>
        <DateInput value={f.date} onChange={set("date")} error={errors.date} />
      </FormField>
      <FormField label="Paliwo">
        <Segmented options={fuels} value={f.fuelType} onChange={set("fuelType")} />
      </FormField>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 10
        }}
      >
        <FormField label="Litry" hint="np. 52,4" error={errors.liters}>
          <TextInput
            value={f.liters}
            onChange={set("liters")}
            suffix="l"
            inputMode="decimal"
            error={errors.liters}
          />
        </FormField>
        <FormField label="Kwota" hint="np. 412,80" error={errors.cost}>
          <TextInput
            value={f.cost}
            onChange={set("cost")}
            suffix="zł"
            inputMode="decimal"
            error={errors.cost}
          />
        </FormField>
      </div>
      <FormField
        label="Przebieg"
        hint={hintPrev ? `poprzednio ${num(hintPrev.mileage, 0)} km` : ""}
        error={errors.mileage}
      >
        <TextInput
          value={f.mileage}
          onChange={set("mileage")}
          suffix="km"
          inputMode="numeric"
          error={errors.mileage}
        />
      </FormField>
      <FormField label="Notatka" hint="opcjonalnie">
        <TextInput value={f.note} onChange={set("note")} />
      </FormField>
      <SummaryBox
        items={[["Cena za litr", liters && cost ? `${num(cost / liters, 2)} zł` : "—"], ["Dystans", dist !== null ? `${num(dist, 0)} km` : "—", dist !== null && dist <= 0 ? C.red : null], ["Spalanie", cons ? `${num(cons, 2)} l/100` : "—", st?.color]]}
      />
    </EntrySheet>
  );
}

/* ---------- TAB: SERWISY ---------- */
function SerwisyTab({
  data,
  setData,
  notify
}) {
  const {
    serwisy
  } = data;
  const [editing, setEditing] = useState(null);
  const byDate = (a, b) => a.date < b.date ? -1 : a.date > b.date ? 1 : 0;
  return (
    <div>
      <ListHeader
        text={serwisy.length ? `${plural(serwisy.length, "wpis", "wpisy", "wpisów")} · płatne ${pln(sumBy(serwisy, "paidCost"))}` : ""}
        onAdd={() => setEditing({
          entry: null
        })}
      />
      {serwisy.length === 0 ? <EmptyList text="Brak wpisów serwisowych." /> : (
        <MonthGroups
          entries={serwisy}
          compare={byDate}
          groupSummary={g => pln(sumBy(g, "paidCost"))}
          renderRow={s => (
            <EntryRow
              key={s.id}
              date={s.date}
              title={s.description}
              sub={[s.mileage ? `${num(s.mileage, 0)} km` : null, s.note || null].filter(Boolean).join(" · ") || "—"}
              amount={pln(s.price)}
              badge={s.warranty ? {
                text: "Gwarancja",
                color: C.green
              } : {
                text: "Płatny",
                color: C.textDim
              }}
              onOpen={() => setEditing({
                entry: s
              })}
            />
          )}
        />
      )}
      {editing && (
        <SerwisSheet
          data={data}
          setData={setData}
          notify={notify}
          entry={editing.entry}
          onClose={() => setEditing(null)}
        />
      )}
    </div>
  );
}
function SerwisSheet({
  data,
  setData,
  notify,
  entry,
  onClose
}) {
  const [f, setF] = useState(() => entry ? {
    date: entry.date,
    description: entry.description,
    mileage: entry.mileage ? String(entry.mileage) : "",
    price: numIn(entry.price),
    warranty: !!entry.warranty,
    note: entry.note || ""
  } : {
    date: todayIso(),
    description: "",
    mileage: "",
    price: "",
    warranty: false,
    note: ""
  });
  const [errors, setErrors] = useState({});
  const set = key => value => {
    setF(prev => ({
      ...prev,
      [key]: value
    }));
    setErrors(prev => ({
      ...prev,
      [key]: undefined
    }));
  };
  const save = () => {
    const r = validate({
      date: () => {
        if (!f.date) throw new Error("Wybierz datę");
        return f.date;
      },
      description: () => {
        if (!f.description.trim()) throw new Error("Opisz, co zostało zrobione");
        return f.description.trim();
      },
      mileage: () => parseNumber(f.mileage, {
        integer: true,
        optional: true,
        min: 0
      }),
      price: () => parseNumber(f.price, {
        optional: true,
        min: 0
      })
    });
    if (!r.ok) return setErrors(r.errors);
    const v = r.values;
    const price = v.price || 0;
    setData(upsertEntry(data, "serwisy", entry, {
      date: v.date,
      mileage: v.mileage,
      description: v.description,
      price,
      warranty: f.warranty,
      paidCost: f.warranty ? 0 : price,
      note: f.note.trim()
    }));
    notify(`Zapisano serwis z ${dateFmt(v.date)}`);
    onClose();
  };
  const remove = () => {
    setData(removeEntry(data, "serwisy", entry));
    notify(`Usunięto wpis „${entry.description}”`, "warn");
    onClose();
  };
  return (
    <EntrySheet
      title={entry ? "Edycja wpisu serwisowego" : "Nowy wpis serwisowy"}
      entry={entry}
      deleteLabel={entry ? `wpis „${entry.description}”` : ""}
      onClose={onClose}
      onSave={save}
      onDelete={remove}
    >
      <FormField label="Data" error={errors.date}>
        <DateInput value={f.date} onChange={set("date")} error={errors.date} />
      </FormField>
      <FormField label="Co zostało wykonane" hint="np. wymiana oleju" error={errors.description}>
        <TextInput value={f.description} onChange={set("description")} error={errors.description} />
      </FormField>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 10
        }}
      >
        <FormField label="Przebieg" hint="opcjonalnie" error={errors.mileage}>
          <TextInput
            value={f.mileage}
            onChange={set("mileage")}
            suffix="km"
            inputMode="numeric"
            error={errors.mileage}
          />
        </FormField>
        <FormField label="Cena" error={errors.price}>
          <TextInput
            value={f.price}
            onChange={set("price")}
            suffix="zł"
            inputMode="decimal"
            error={errors.price}
          />
        </FormField>
      </div>
      <SwitchRow
        label="Naprawa gwarancyjna"
        sub="nie wlicza się do kosztów"
        checked={f.warranty}
        onChange={set("warranty")}
      />
      <FormField label="Notatka" hint="opcjonalnie, np. nazwa serwisu">
        <TextInput value={f.note} onChange={set("note")} />
      </FormField>
    </EntrySheet>
  );
}

/* ---------- TAB: KOSZTY ---------- */
function KosztyTab({
  data,
  setData,
  notify
}) {
  const {
    koszty
  } = data;
  const [editing, setEditing] = useState(null);
  const byDate = (a, b) => a.date < b.date ? -1 : a.date > b.date ? 1 : 0;
  const running = sumBy(koszty.filter(k => k.type !== "Zakup auta"), "amount");
  return (
    <div>
      <ListHeader
        text={koszty.length ? `${plural(koszty.length, "pozycja", "pozycje", "pozycji")} · bez zakupu auta ${pln(running)}` : ""}
        onAdd={() => setEditing({
          entry: null
        })}
      />
      {koszty.length === 0 ? <EmptyList text="Brak kosztów." /> : (
        <MonthGroups
          entries={koszty}
          compare={byDate}
          groupSummary={g => pln(sumBy(g, "amount"))}
          renderRow={k => (
            <EntryRow
              key={k.id}
              date={k.date}
              title={k.description}
              sub={k.type + (k.note ? ` · ${k.note}` : "")}
              amount={pln(k.amount)}
              badge={{
                text: k.type,
                color: k.type === "Zakup auta" ? C.copper : C.textDim
              }}
              onOpen={() => setEditing({
                entry: k
              })}
            />
          )}
        />
      )}
      {editing && (
        <KosztSheet
          data={data}
          setData={setData}
          notify={notify}
          entry={editing.entry}
          onClose={() => setEditing(null)}
        />
      )}
    </div>
  );
}
function KosztSheet({
  data,
  setData,
  notify,
  entry,
  onClose
}) {
  const [f, setF] = useState(() => entry ? {
    date: entry.date,
    type: entry.type,
    description: entry.description,
    amount: numIn(entry.amount),
    note: entry.note || ""
  } : {
    date: todayIso(),
    type: "Inne",
    description: "",
    amount: "",
    note: ""
  });
  const [errors, setErrors] = useState({});
  const set = key => value => {
    setF(prev => ({
      ...prev,
      [key]: value
    }));
    setErrors(prev => ({
      ...prev,
      [key]: undefined
    }));
  };
  const types = KOSZTY_TYPES.includes(f.type) ? KOSZTY_TYPES : [...KOSZTY_TYPES, f.type];
  const save = () => {
    const r = validate({
      date: () => {
        if (!f.date) throw new Error("Wybierz datę");
        return f.date;
      },
      amount: () => parseNumber(f.amount, {
        min: 0
      })
    });
    if (!r.ok) return setErrors(r.errors);
    const v = r.values;
    const description = f.description.trim() || f.type;
    setData(upsertEntry(data, "koszty", entry, {
      date: v.date,
      type: f.type,
      description,
      amount: v.amount,
      // new costs count towards monthly totals; an edited entry keeps its flag
      oneTime: entry ? entry.oneTime ?? true : true,
      note: f.note.trim()
    }));
    notify(`Zapisano koszt: ${description}`);
    onClose();
  };
  const remove = () => {
    setData(removeEntry(data, "koszty", entry));
    notify(`Usunięto koszt „${entry.description}”`, "warn");
    onClose();
  };
  return (
    <EntrySheet
      title={entry ? "Edycja kosztu" : "Nowy koszt"}
      entry={entry}
      deleteLabel={entry ? `koszt „${entry.description}”` : ""}
      onClose={onClose}
      onSave={save}
      onDelete={remove}
    >
      <FormField label="Data" error={errors.date}>
        <DateInput value={f.date} onChange={set("date")} error={errors.date} />
      </FormField>
      <FormField label="Kategoria">
        <select
          style={{
            ...inputStyle,
            colorScheme: "dark"
          }}
          value={f.type}
          onChange={e => set("type")(e.target.value)}
        >
          {types.map(t => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
      </FormField>
      <FormField label="Opis" hint="np. polisa OC/AC">
        <TextInput value={f.description} onChange={set("description")} />
      </FormField>
      <FormField label="Kwota" error={errors.amount}>
        <TextInput
          value={f.amount}
          onChange={set("amount")}
          suffix="zł"
          inputMode="decimal"
          error={errors.amount}
        />
      </FormField>
      <FormField label="Notatka" hint="opcjonalnie">
        <TextInput value={f.note} onChange={set("note")} />
      </FormField>
    </EntrySheet>
  );
}

/* ---------- TOAST ---------- */
function Toast({
  toast
}) {
  if (!toast) return null;
  const color = toast.kind === "warn" ? C.amber : toast.kind === "error" ? C.red : C.green;
  return (
    <div
      style={{
        position: "fixed",
        left: "50%",
        transform: "translateX(-50%)",
        bottom: "calc(env(safe-area-inset-bottom, 0px) + 84px)",
        zIndex: 60,
        background: C.surface2,
        border: `1px solid ${C.line}`,
        borderRadius: 12,
        padding: "10px 14px",
        display: "flex",
        gap: 9,
        alignItems: "center",
        fontSize: 13,
        color: C.text,
        boxShadow: "0 8px 24px #00000088",
        maxWidth: "calc(100% - 32px)",
        width: "max-content"
      }}
    >
      <span
        style={{
          width: 8,
          height: 8,
          borderRadius: 99,
          background: color,
          flex: "none"
        }}
      />
      {toast.text}
    </div>
  );
}

/* ---------- TAB: PROGNOZA ---------- */
function PrognozaTab({
  agg,
  settings
}) {
  const baseConsumption = agg.weightedConsumption || settings.consumptionOkTo;
  const basePrice = agg.avgPricePerL || 6.5;
  const rows = useMemo(() => {
    const out = [];
    const now = new Date();
    for (let i = 0; i < 12; i++) {
      const d = new Date(now.getFullYear(), now.getMonth() + i, 1);
      const growthFactor = Math.pow(1 + settings.fuelPriceGrowth, i / 12);
      const fuel = settings.monthlyKmPlan / 100 * baseConsumption * basePrice * growthFactor;
      out.push({
        label: d.toLocaleDateString("pl-PL", {
          month: "short",
          year: "2-digit"
        }),
        fuel
      });
    }
    return out;
  }, [settings, baseConsumption, basePrice]);
  const total12 = rows.reduce((s, r) => s + r.fuel, 0);
  const avgMonth = total12 / 12;
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 14
      }}
    >
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 10
        }}
      >
        <KPI icon={Icon.trend} label="Prognoza 12 mies." value={pln(total12)} />
        <KPI icon={Icon.calendar} label="Śr. miesięcznie" value={pln(avgMonth)} />
      </div>
      <Card>
        <div
          style={{
            fontSize: 12.5,
            color: C.textDim,
            marginBottom: 4,
            fontWeight: 600
          }}
        >
          Prognoza kosztów paliwa
        </div>
        <div
          style={{
            fontSize: 11,
            color: C.textFaint,
            marginBottom: 6
          }}
        >
          {"Założenia: "}
          {num(settings.monthlyKmPlan, 0)}
          {" km/mies., spalanie "}
          {num(baseConsumption, 2)}
          {" l/100km, wzrost cen "}
          {num(settings.fuelPriceGrowth * 100, 1)}
          %/rok
        </div>
        <div
          style={{
            fontSize: 10.5,
            color: C.textFaint,
            marginBottom: 6
          }}
        >
          Stuknij punkt, żeby zobaczyć prognozę na dany miesiąc
        </div>
        <MiniChart
          data={rows}
          valueKey="fuel"
          labelKey="label"
          type="line"
          color={C.copper}
          formatValue={v => `${Math.round(v)} zł`}
        />
      </Card>
    </div>
  );
}

/* ---------- SYNC UI ---------- */
const SYNC_LABEL = {
  syncing: "Synchronizacja…",
  offline: "Offline",
  auth: "Zaloguj do Google",
  error: "Błąd synchronizacji"
};
function syncLabel(sync) {
  if (SYNC_LABEL[sync.state]) return SYNC_LABEL[sync.state] + (sync.state === "offline" && sync.pending ? ` · ${sync.pending}` : "");
  if (sync.pending) return `Do wysłania: ${sync.pending}`;
  return sync.lastSync ? "Zsynchronizowano" : "Arkusz Google";
}
// the header badge has little room next to the car name
const SYNC_SHORT = {
  syncing: "Synchr.…",
  offline: "Offline",
  auth: "Zaloguj",
  error: "Błąd"
};
function syncShortLabel(sync) {
  if (sync.state === "offline" && sync.pending) return `Offline · ${sync.pending}`;
  if (SYNC_SHORT[sync.state]) return SYNC_SHORT[sync.state];
  return sync.pending ? `↑ ${sync.pending}` : "Arkusz";
}
function syncColor(sync) {
  if (sync.state === "error") return C.red;
  if (sync.state === "auth" || sync.state === "offline") return C.amber;
  if (sync.state === "ok" && !sync.pending) return C.green;
  return C.textDim;
}
function SyncBadge({
  sync
}) {
  if (!sync.connected) return null;
  const color = syncColor(sync);
  return (
    <button
      onClick={sync.state === "auth" ? sync.login : sync.run}
      style={{
        marginLeft: "auto",
        display: "flex",
        alignItems: "center",
        gap: 6,
        background: "none",
        border: `1px solid ${C.line}`,
        borderRadius: 999,
        padding: "5px 10px",
        color,
        fontSize: 11.5,
        cursor: "pointer",
        whiteSpace: "nowrap"
      }}
    >
      <span
        style={{
          width: 7,
          height: 7,
          borderRadius: 99,
          background: color,
          opacity: sync.state === "syncing" ? 0.5 : 1
        }}
      />
      {syncShortLabel(sync)}
    </button>
  );
}
function SyncCard({
  sync
}) {
  const [confirmOff, setConfirmOff] = useState(false);
  const row = (label, value, color) => (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        fontSize: 12.5,
        padding: "4px 0"
      }}
    >
      <span
        style={{
          color: C.textDim
        }}
      >
        {label}
      </span>
      <span
        style={{
          color: color || C.text
        }}
      >
        {value}
      </span>
    </div>
  );
  const last = sync.lastSync ? new Date(sync.lastSync).toLocaleString("pl-PL", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit"
  }) : "jeszcze nie";
  return (
    <Card>
      <SectionTitle>Arkusz Google</SectionTitle>
      {!sync.connected ? (
        <>
          <div
            style={{
              fontSize: 12,
              color: C.textFaint,
              lineHeight: 1.5,
              marginTop: -6,
              marginBottom: 10
            }}
          >
            Połącz aplikację z arkuszem „Cupra Terramar - dane” na Twoim Dysku Google. Wpisy z telefonu i komputera będą się wzajemnie uzupełniać. Przy pierwszym połączeniu wpisy, które są tylko na tym telefonie, zostaną dopisane do arkusza.
          </div>
          <PrimaryButton onClick={sync.connect}>Połącz z Google</PrimaryButton>
        </>
      ) : (
        <>
          {row("Stan", syncLabel(sync), syncColor(sync))}
          {row("Ostatnia synchronizacja", last)}
          {row("Zmiany do wysłania", sync.pending)}
          {sync.message && (
            <div
              style={{
                color: sync.state === "error" ? C.red : C.amber,
                fontSize: 12,
                lineHeight: 1.45,
                margin: "6px 0 2px"
              }}
            >
              {sync.message}
            </div>
          )}
          <div
            style={{
              display: "flex",
              gap: 8,
              marginTop: 10
            }}
          >
            <button
              onClick={sync.state === "auth" ? sync.login : sync.run}
              style={{
                ...addBtnStyle,
                flex: 1,
                justifyContent: "center"
              }}
            >
              {sync.state === "auth" ? "Zaloguj do Google" : "Synchronizuj teraz"}
            </button>
            <a
              href={`https://docs.google.com/spreadsheets/d/${sheetId()}/edit`}
              target="_blank"
              rel="noopener"
              style={{
                ...toggleBtn(false),
                flex: 1,
                textAlign: "center",
                textDecoration: "none"
              }}
            >
              Otwórz arkusz
            </a>
          </div>
          <button
            onClick={() => setConfirmOff(true)}
            style={{
              background: "none",
              border: "none",
              color: C.textFaint,
              fontSize: 12,
              marginTop: 10,
              padding: 0,
              cursor: "pointer"
            }}
          >
            Odłącz od arkusza
          </button>
        </>
      )}
      {confirmOff && (
        <ConfirmSheet
          title="Odłączyć arkusz?"
          message="Dane zostaną na telefonie, ale zmiany przestaną trafiać do arkusza Google. Możesz połączyć się ponownie w każdej chwili."
          confirmText="Odłącz"
          onCancel={() => setConfirmOff(false)}
          onConfirm={() => {
            sync.disconnect();
            setConfirmOff(false);
          }}
        />
      )}
    </Card>
  );
}

/* ---------- TAB: USTAWIENIA ---------- */
const settingsToForm = s => ({
  carName: s.carName,
  carSubtitle: s.carSubtitle,
  consumptionOkTo: numIn(s.consumptionOkTo),
  consumptionHighFrom: numIn(s.consumptionHighFrom),
  fuelPriceGrowth: numIn(+(s.fuelPriceGrowth * 100).toFixed(4)),
  monthlyKmPlan: numIn(s.monthlyKmPlan),
  carPrice: numIn(s.carPrice)
});
function SectionTitle({
  children
}) {
  return (
    <div
      style={{
        fontSize: 13,
        fontWeight: 600,
        color: C.text,
        margin: "4px 0 12px"
      }}
    >
      {children}
    </div>
  );
}
function UstawieniaTab({
  data,
  setData,
  notify,
  sync
}) {
  const [f, setF] = useState(() => settingsToForm(data.settings));
  const [errors, setErrors] = useState({});
  const [pendingImport, setPendingImport] = useState(null);
  const fileInputRef = React.useRef(null);
  const dirty = JSON.stringify(f) !== JSON.stringify(settingsToForm(data.settings));
  const set = key => value => {
    setF(prev => ({
      ...prev,
      [key]: value
    }));
    setErrors(prev => ({
      ...prev,
      [key]: undefined
    }));
  };
  const save = () => {
    const r = validate({
      consumptionOkTo: () => parseNumber(f.consumptionOkTo, {
        min: 0.1
      }),
      consumptionHighFrom: () => parseNumber(f.consumptionHighFrom, {
        min: 0.1
      }),
      fuelPriceGrowth: () => parseNumber(f.fuelPriceGrowth),
      monthlyKmPlan: () => parseNumber(f.monthlyKmPlan, {
        min: 0
      }),
      carPrice: () => parseNumber(f.carPrice, {
        min: 0
      })
    });
    if (r.ok && r.values.consumptionHighFrom <= r.values.consumptionOkTo) {
      r.errors.consumptionHighFrom = "Musi być większe niż próg „w normie”";
      r.ok = false;
    }
    if (!r.ok) return setErrors(r.errors);
    const v = r.values;
    setData({
      ...data,
      settings: {
        ...data.settings,
        carName: f.carName.trim() || "MOJE AUTO",
        carSubtitle: f.carSubtitle.trim() || "DZIENNIK POKŁADOWY",
        consumptionOkTo: v.consumptionOkTo,
        consumptionHighFrom: v.consumptionHighFrom,
        fuelPriceGrowth: v.fuelPriceGrowth / 100,
        monthlyKmPlan: v.monthlyKmPlan,
        carPrice: v.carPrice
      }
    });
    notify("Ustawienia zapisane");
  };
  const handleExport = async () => {
    const res = await exportBackup(data);
    if (res.ok && res.method !== "cancelled") {
      notify(res.method === "share" ? "Wybierz Dysk Google w oknie udostępniania" : "Plik kopii pobrany");
    }
  };
  const handleFileChange = async e => {
    const file = e.target.files && e.target.files[0];
    e.target.value = "";
    if (!file) return;
    try {
      setPendingImport({
        name: file.name,
        data: await readBackupFile(file)
      });
    } catch (err) {
      notify(err.message, "error");
    }
  };
  const applyImport = () => {
    setData(pendingImport.data);
    setF(settingsToForm(pendingImport.data.settings));
    notify(`Wczytano ${plural(pendingImport.data.tankowania.length, "tankowanie", "tankowania", "tankowań")}`);
    setPendingImport(null);
  };
  const field = (key, label, suffix, inputMode = "decimal") => (
    <FormField label={label} error={errors[key]}>
      <TextInput
        value={f[key]}
        onChange={set(key)}
        suffix={suffix}
        inputMode={inputMode}
        error={errors[key]}
      />
    </FormField>
  );
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 10
      }}
    >
      <SyncCard sync={sync} />
      <Card>
        <SectionTitle>Pojazd</SectionTitle>
        {field("carName", "Nazwa auta", null, "text")}
        {field("carSubtitle", "Podtytuł", null, "text")}
        {field("carPrice", "Cena auta", "zł")}
      </Card>
      <Card>
        <SectionTitle>Progi spalania</SectionTitle>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 10
          }}
        >
          {field("consumptionOkTo", "W normie do", "l/100")}
          {field("consumptionHighFrom", "Wysokie od", "l/100")}
        </div>
        <div
          style={{
            display: "flex",
            gap: 6,
            flexWrap: "wrap"
          }}
        >
          <Pill text="W normie" color={C.green} />
          <Pill text="Podwyższone" color={C.amber} />
          <Pill text="Wysokie" color={C.red} />
        </div>
      </Card>
      <Card>
        <SectionTitle>Prognoza</SectionTitle>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 10
          }}
        >
          {field("monthlyKmPlan", "Przebieg miesięczny", "km", "numeric")}
          {field("fuelPriceGrowth", "Wzrost cen paliwa", "%/rok")}
        </div>
      </Card>
      <PrimaryButton onClick={save} disabled={!dirty}>
        Zapisz ustawienia
      </PrimaryButton>
      <Card
        style={{
          marginTop: 6
        }}
      >
        <SectionTitle>Kopia zapasowa</SectionTitle>
        <div
          style={{
            fontSize: 11.5,
            color: C.textFaint,
            marginTop: -6,
            marginBottom: 12,
            lineHeight: 1.5
          }}
        >
          Zapisz wszystkie dane do pliku (np. na Dysk Google) albo wczytaj wcześniej zapisaną kopię. Plik jest zgodny z wersją desktopową.
        </div>
        <div
          style={{
            display: "flex",
            gap: 8
          }}
        >
          <button
            onClick={handleExport}
            style={{
              ...addBtnStyle,
              flex: 1,
              justifyContent: "center"
            }}
          >
            Eksportuj dane
          </button>
          <button
            onClick={() => fileInputRef.current && fileInputRef.current.click()}
            style={{
              ...toggleBtn(false),
              flex: 1
            }}
          >
            Wczytaj kopię
          </button>
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept="application/json,.json"
          style={{
            display: "none"
          }}
          onChange={handleFileChange}
        />
      </Card>
      <div
        style={{
          fontSize: 11.5,
          color: C.textFaint,
          padding: "4px 4px 10px",
          lineHeight: 1.5
        }}
      >
        Dane są zapisywane bezpośrednio w pamięci tej przeglądarki na Twoim telefonie (localStorage) — zostają nawet po zamknięciu aplikacji. Kopia zapasowa to jedyny sposób, by przenieść je na inne urządzenie.
      </div>
      {pendingImport && (
        <ConfirmSheet
          title="Wczytać kopię?"
          message={`Obecne dane zostaną zastąpione zawartością pliku ${pendingImport.name} (${plural(pendingImport.data.tankowania.length, "tankowanie", "tankowania", "tankowań")}, ${plural(pendingImport.data.serwisy.length, "serwis", "serwisy", "serwisów")}, ${plural(pendingImport.data.koszty.length, "koszt", "koszty", "kosztów")}).${sync.connected ? " Zmiana trafi też do arkusza Google." : ""}`}
          confirmText="Wczytaj"
          danger={false}
          onCancel={() => setPendingImport(null)}
          onConfirm={applyImport}
        />
      )}
    </div>
  );
}

/* ---------- APP SHELL ---------- */
const TABS = [{
  key: "dashboard",
  label: "Pulpit",
  icon: Icon.gauge
}, {
  key: "tankowania",
  label: "Tankowania",
  icon: Icon.fuel
}, {
  key: "serwisy",
  label: "Serwisy",
  icon: Icon.wrench
}, {
  key: "koszty",
  label: "Koszty",
  icon: Icon.receipt
}, {
  key: "prognoza",
  label: "Prognoza",
  icon: Icon.trend
}];
const EMPTY_DATA = {
  tankowania: [],
  serwisy: [],
  koszty: [],
  settings: SEED_SETTINGS
};
function CarDashboardApp() {
  const {
    data,
    setData,
    loading,
    error,
    sync
  } = useCarData();
  const [tab, setTab] = useState("dashboard");
  const [toast, setToast] = useState(null);
  const notify = useCallback((text, kind = "ok") => setToast({
    text,
    kind,
    at: Date.now()
  }), []);
  useEffect(() => {
    if (!toast) return undefined;
    const t = setTimeout(() => setToast(null), 2600);
    return () => clearTimeout(t);
  }, [toast]);
  const agg = useAggregates(data || EMPTY_DATA);
  // data is null on the first render (loaded in useEffect)
  const settings = (data || EMPTY_DATA).settings;
  return (
    <div
      style={{
        minHeight: "100vh",
        background: C.bg,
        color: C.text,
        fontFamily: "Inter, -apple-system, sans-serif",
        display: "flex",
        justifyContent: "center"
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: 480,
          paddingBottom: 84,
          position: "relative"
        }}
      >
        <header
          style={{
            padding: "22px 18px 14px",
            position: "sticky",
            top: 0,
            background: C.bg,
            zIndex: 10,
            borderBottom: `1px solid ${C.line}`
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10
            }}
          >
            <img
              src="emblem.png"
              alt=""
              style={{
                height: 30,
                width: "auto",
                display: "block"
              }}
            />
            <div>
              <div
                style={{
                  fontFamily: "'Space Grotesk', sans-serif",
                  fontSize: 18,
                  fontWeight: 700,
                  letterSpacing: 0.2
                }}
              >
                {settings.carName || "MOJE AUTO"}
              </div>
              <div
                style={{
                  fontSize: 11,
                  color: C.textDim,
                  letterSpacing: 1.5
                }}
              >
                {settings.carSubtitle || "DZIENNIK POKŁADOWY"}
              </div>
            </div>
            <SyncBadge sync={sync} />
          </div>
        </header>
        <main
          style={{
            padding: "16px 16px 8px"
          }}
        >
          {loading && (
            <div
              style={{
                textAlign: "center",
                color: C.textDim,
                padding: 40
              }}
            >
              Wczytywanie danych…
            </div>
          )}
          {!loading && error && (
            <div
              style={{
                background: C.red + "22",
                border: `1px solid ${C.red}55`,
                color: C.red,
                borderRadius: 10,
                padding: 10,
                fontSize: 12.5,
                marginBottom: 12
              }}
            >
              {error}
            </div>
          )}
          {!loading && data && (
            <>
              {tab === "dashboard" && <Dashboard agg={agg} settings={data.settings} tankowania={data.tankowania} />}
              {tab === "tankowania" && <TankowaniaTab data={data} setData={setData} notify={notify} />}
              {tab === "serwisy" && <SerwisyTab data={data} setData={setData} notify={notify} />}
              {tab === "koszty" && <KosztyTab data={data} setData={setData} notify={notify} />}
              {tab === "prognoza" && <PrognozaTab agg={agg} settings={data.settings} />}
              {tab === "ustawienia" && <UstawieniaTab data={data} setData={setData} notify={notify} sync={sync} />}
            </>
          )}
        </main>
        <Toast toast={toast} />
        <nav
          style={{
            position: "fixed",
            bottom: 0,
            left: "50%",
            transform: "translateX(-50%)",
            width: "100%",
            maxWidth: 480,
            background: C.surface,
            borderTop: `1px solid ${C.line}`,
            display: "flex",
            justifyContent: "space-around",
            padding: "9px 4px calc(env(safe-area-inset-bottom, 0px) + 9px)"
          }}
        >
          {TABS.map(({
            key,
            label,
            icon: Ico
          }) => {
            const active = tab === key;
            return (
              <button
                key={key}
                onClick={() => setTab(key)}
                style={{
                  background: "none",
                  border: "none",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 3,
                  color: active ? C.copper : C.textFaint,
                  fontSize: 10.5,
                  cursor: "pointer",
                  padding: "4px 6px",
                  flex: 1
                }}
              >
                <Ico size={19} />
                {label}
              </button>
            );
          })}
          <button
            onClick={() => setTab("ustawienia")}
            style={{
              background: "none",
              border: "none",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 3,
              color: tab === "ustawienia" ? C.copper : C.textFaint,
              fontSize: 10.5,
              cursor: "pointer",
              padding: "4px 6px",
              flex: 1
            }}
          >
            <Icon.settings size={19} />
            Ustawienia
          </button>
        </nav>
      </div>
    </div>
  );
}
function App() {
  return (
    <ErrorBoundary>
      <CarDashboardApp />
    </ErrorBoundary>
  );
}
ReactDOM.createRoot(document.getElementById("root")).render(<App />);
