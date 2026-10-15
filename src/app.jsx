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
const FUEL_TYPES = ["Pb95", "Pb98", "E10", "Inne"];

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
function useCarData() {
  const [data, setDataState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (raw) setDataState(sanitize(JSON.parse(raw)));else {
        const seed = sanitize(null);
        setDataState(seed);
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(seed));
      }
    } catch (e) {
      setError("Nie udało się wczytać zapisanych danych z pamięci telefonu. Startuję z danymi przykładowymi.");
      setDataState(sanitize(null));
    } finally {
      setLoading(false);
    }
  }, []);
  const setData = useCallback(next => {
    const clean = sanitize(next);
    setDataState(clean);
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(clean));
    } catch (e) {
      setError("Zmiana zapisana tymczasowo, ale nie udało się jej utrwalić na dysku.");
    }
  }, []);
  return {
    data,
    setData,
    loading,
    error
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
  accent
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
          color: C.text
        }}
      >
        {value}
      </div>
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
        {status && (
          <div
            style={{
              marginTop: 4
            }}
          >
            <Pill text={status.label} color={status.color} />
          </div>
        )}
      </div>
    </div>
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
  settings
}) {
  const chartData = agg.monthly.filter(m => m.total > 0);
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
        <KPI icon={Icon.money} label="Koszt całkowity" value={pln(agg.totalCost)} />
        <KPI icon={Icon.gauge} label="Dystans" value={`${num(agg.totalDistance, 0)} km`} />
        <KPI
          icon={Icon.trend}
          label="Koszt / km"
          value={agg.costPerKm ? `${num(agg.costPerKm, 2)} zł` : "—"}
        />
        <KPI
          icon={Icon.drop}
          label="Śr. cena / l"
          value={agg.avgPricePerL ? `${num(agg.avgPricePerL, 2)} zł` : "—"}
        />
        <KPI
          icon={Icon.alert}
          label="Alerty spalania"
          value={agg.alerts}
          accent={agg.alerts ? C.red : C.green}
        />
        <KPI
          icon={Icon.shield}
          label="Ostatni serwis"
          value={agg.lastService ? dateFmt(agg.lastService.date) : "—"}
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

/* ---------- TAB: TANKOWANIA ---------- */
function TankowaniaTab({
  data,
  setData
}) {
  const [open, setOpen] = useState(false);
  const {
    tankowania,
    settings
  } = data;
  const sorted = [...tankowania].sort((a, b) => a.date < b.date ? 1 : -1);
  const lastMileage = sorted[0]?.mileage || "";
  const [form, setForm] = useState(null);
  const startNew = () => {
    setForm({
      date: new Date().toISOString().slice(0, 10),
      fuelType: "Pb98",
      liters: "",
      cost: "",
      mileage: ""
    });
    setOpen(true);
  };
  const save = () => {
    const liters = parseFloat(form.liters),
      cost = parseFloat(form.cost),
      mileage = parseInt(form.mileage, 10);
    if (!liters || !cost || !mileage || !form.date) return;
    const prev = sorted[0];
    const distance = prev && prev.mileage ? mileage - prev.mileage : null;
    const consumption = distance && distance > 0 ? +(liters / distance * 100).toFixed(2) : null;
    const entry = {
      id: uid(),
      date: form.date,
      fuelType: form.fuelType,
      liters,
      cost,
      pricePerL: +(cost / liters).toFixed(3),
      mileage,
      distance,
      consumption,
      note: form.note || ""
    };
    setData({
      ...data,
      tankowania: [...tankowania, entry]
    });
    setOpen(false);
  };
  const remove = id => setData({
    ...data,
    tankowania: tankowania.filter(t => t.id !== id)
  });
  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 12
        }}
      >
        <div
          style={{
            color: C.textDim,
            fontSize: 12
          }}
        >
          {sorted.length}
          {" tankowań · ostatni przebieg "}
          {num(lastMileage, 0)}
          {" km"}
        </div>
        <button onClick={startNew} style={addBtnStyle}>
          <Icon.plus />
          Dodaj
        </button>
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 8
        }}
      >
        {sorted.map(t => {
          const status = statusOf(t.consumption, settings);
          return (
            <Card
              key={t.id}
              style={{
                padding: 12
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "flex-start"
                }}
              >
                <div>
                  <div
                    style={{
                      color: C.text,
                      fontWeight: 600,
                      fontSize: 14
                    }}
                  >
                    {t.fuelType}
                    {" · "}
                    {num(t.liters, 2)}
                    {" l"}
                  </div>
                  <div
                    style={{
                      color: C.textDim,
                      fontSize: 12
                    }}
                  >
                    {dateFmt(t.date)}
                    {" · "}
                    {num(t.mileage, 0)}
                    {" km"}
                    {t.distance ? ` (+${num(t.distance, 0)} km)` : ""}
                  </div>
                </div>
                <div
                  style={{
                    textAlign: "right"
                  }}
                >
                  <div
                    style={{
                      color: C.text,
                      fontFamily: "'JetBrains Mono', monospace",
                      fontWeight: 600
                    }}
                  >
                    {pln(t.cost)}
                  </div>
                  <div
                    style={{
                      color: C.textFaint,
                      fontSize: 11
                    }}
                  >
                    {num(t.pricePerL, 2)}
                    {" zł/l"}
                  </div>
                </div>
              </div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginTop: 8
                }}
              >
                {status ? (
                  <Pill
                    text={`${num(t.consumption, 2)} l/100km · ${status.label}`}
                    color={status.color}
                  />
                ) : <span />}
                {!t.id.startsWith("seed") && (
                  <button onClick={() => remove(t.id)} style={trashBtn}>
                    <Icon.trash />
                  </button>
                )}
              </div>
            </Card>
          );
        })}
      </div>
      {open && (
        <SheetModal title="Nowe tankowanie" onClose={() => setOpen(false)}>
          <Field label="Data">
            <input
              type="date"
              style={inputStyle}
              value={form.date}
              onChange={e => setForm({
                ...form,
                date: e.target.value
              })}
            />
          </Field>
          <Field label="Paliwo">
            <select
              style={inputStyle}
              value={form.fuelType}
              onChange={e => setForm({
                ...form,
                fuelType: e.target.value
              })}
            >
              {FUEL_TYPES.map(f => (
                <option key={f} value={f}>
                  {f}
                </option>
              ))}
            </select>
          </Field>
          <Field label="Litry">
            <input
              type="number"
              inputMode="decimal"
              style={inputStyle}
              value={form.liters}
              onChange={e => setForm({
                ...form,
                liters: e.target.value
              })}
              placeholder="np. 52.30"
            />
          </Field>
          <Field label="Koszt (zł)">
            <input
              type="number"
              inputMode="decimal"
              style={inputStyle}
              value={form.cost}
              onChange={e => setForm({
                ...form,
                cost: e.target.value
              })}
              placeholder="np. 410.50"
            />
          </Field>
          <Field label="Przebieg (km)">
            <input
              type="number"
              inputMode="numeric"
              style={inputStyle}
              value={form.mileage}
              onChange={e => setForm({
                ...form,
                mileage: e.target.value
              })}
              placeholder={`ostatni: ${lastMileage}`}
            />
          </Field>
          <Field label="Notatka (opcjonalnie)">
            <input
              type="text"
              style={inputStyle}
              value={form.note || ""}
              onChange={e => setForm({
                ...form,
                note: e.target.value
              })}
            />
          </Field>
          <PrimaryButton onClick={save} disabled={!form.liters || !form.cost || !form.mileage}>
            Zapisz tankowanie
          </PrimaryButton>
        </SheetModal>
      )}
    </div>
  );
}

/* ---------- TAB: SERWISY ---------- */
function SerwisyTab({
  data,
  setData
}) {
  const [open, setOpen] = useState(false);
  const {
    serwisy
  } = data;
  const sorted = [...serwisy].sort((a, b) => a.date < b.date ? 1 : -1);
  const [form, setForm] = useState(null);
  const startNew = () => {
    setForm({
      date: new Date().toISOString().slice(0, 10),
      mileage: "",
      description: "",
      price: "",
      warranty: false
    });
    setOpen(true);
  };
  const save = () => {
    if (!form.description || !form.date) return;
    const price = parseFloat(form.price) || 0;
    const entry = {
      id: uid(),
      date: form.date,
      mileage: parseInt(form.mileage, 10) || null,
      description: form.description,
      price,
      warranty: form.warranty,
      paidCost: form.warranty ? 0 : price,
      note: form.note || ""
    };
    setData({
      ...data,
      serwisy: [...serwisy, entry]
    });
    setOpen(false);
  };
  const remove = id => setData({
    ...data,
    serwisy: serwisy.filter(s => s.id !== id)
  });
  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 12
        }}
      >
        <div
          style={{
            color: C.textDim,
            fontSize: 12
          }}
        >
          {sorted.length}
          {" wpisów serwisowych"}
        </div>
        <button onClick={startNew} style={addBtnStyle}>
          <Icon.plus />
          Dodaj
        </button>
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 8
        }}
      >
        {sorted.map(s => (
          <Card
            key={s.id}
            style={{
              padding: 12
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start"
              }}
            >
              <div>
                <div
                  style={{
                    color: C.text,
                    fontWeight: 600,
                    fontSize: 14
                  }}
                >
                  {s.description}
                </div>
                <div
                  style={{
                    color: C.textDim,
                    fontSize: 12
                  }}
                >
                  {dateFmt(s.date)}
                  {s.mileage ? ` · ${num(s.mileage, 0)} km` : ""}
                </div>
                {s.note && (
                  <div
                    style={{
                      color: C.textFaint,
                      fontSize: 11,
                      marginTop: 3
                    }}
                  >
                    {s.note}
                  </div>
                )}
              </div>
              <div
                style={{
                  textAlign: "right"
                }}
              >
                <div
                  style={{
                    color: C.text,
                    fontFamily: "'JetBrains Mono', monospace",
                    fontWeight: 600
                  }}
                >
                  {pln(s.price)}
                </div>
              </div>
            </div>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginTop: 8
              }}
            >
              <Pill
                text={s.warranty ? "Gwarancja" : "Płatny"}
                color={s.warranty ? C.green : C.amber}
              />
              {!s.id.startsWith("seed") && (
                <button onClick={() => remove(s.id)} style={trashBtn}>
                  <Icon.trash />
                </button>
              )}
            </div>
          </Card>
        ))}
      </div>
      {open && (
        <SheetModal title="Nowy wpis serwisowy" onClose={() => setOpen(false)}>
          <Field label="Data">
            <input
              type="date"
              style={inputStyle}
              value={form.date}
              onChange={e => setForm({
                ...form,
                date: e.target.value
              })}
            />
          </Field>
          <Field label="Przebieg (km)">
            <input
              type="number"
              inputMode="numeric"
              style={inputStyle}
              value={form.mileage}
              onChange={e => setForm({
                ...form,
                mileage: e.target.value
              })}
            />
          </Field>
          <Field label="Co było wykonane">
            <input
              type="text"
              style={inputStyle}
              value={form.description}
              onChange={e => setForm({
                ...form,
                description: e.target.value
              })}
              placeholder="np. Olej + filtr"
            />
          </Field>
          <Field label="Cena (zł)">
            <input
              type="number"
              inputMode="decimal"
              style={inputStyle}
              value={form.price}
              onChange={e => setForm({
                ...form,
                price: e.target.value
              })}
            />
          </Field>
          <Field label="Naprawa gwarancyjna?">
            <div
              style={{
                display: "flex",
                gap: 8
              }}
            >
              <button
                onClick={() => setForm({
                  ...form,
                  warranty: true
                })}
                style={toggleBtn(form.warranty)}
              >
                Tak
              </button>
              <button
                onClick={() => setForm({
                  ...form,
                  warranty: false
                })}
                style={toggleBtn(!form.warranty)}
              >
                Nie
              </button>
            </div>
          </Field>
          <Field label="Notatka (opcjonalnie)">
            <input
              type="text"
              style={inputStyle}
              value={form.note || ""}
              onChange={e => setForm({
                ...form,
                note: e.target.value
              })}
            />
          </Field>
          <PrimaryButton onClick={save} disabled={!form.description}>
            Zapisz serwis
          </PrimaryButton>
        </SheetModal>
      )}
    </div>
  );
}

/* ---------- TAB: KOSZTY ---------- */
function KosztyTab({
  data,
  setData
}) {
  const [open, setOpen] = useState(false);
  const {
    koszty
  } = data;
  const sorted = [...koszty].sort((a, b) => a.date < b.date ? 1 : -1);
  const [form, setForm] = useState(null);
  const startNew = () => {
    setForm({
      date: new Date().toISOString().slice(0, 10),
      type: "Inne",
      description: "",
      amount: "",
      oneTime: true
    });
    setOpen(true);
  };
  const save = () => {
    const amount = parseFloat(form.amount);
    if (!amount || !form.date) return;
    const entry = {
      id: uid(),
      date: form.date,
      type: form.type,
      description: form.description || form.type,
      amount,
      oneTime: form.oneTime,
      note: form.note || ""
    };
    setData({
      ...data,
      koszty: [...koszty, entry]
    });
    setOpen(false);
  };
  const remove = id => setData({
    ...data,
    koszty: koszty.filter(k => k.id !== id)
  });
  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 12
        }}
      >
        <div
          style={{
            color: C.textDim,
            fontSize: 12
          }}
        >
          {sorted.length}
          {" pozycji kosztowych"}
        </div>
        <button onClick={startNew} style={addBtnStyle}>
          <Icon.plus />
          Dodaj
        </button>
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 8
        }}
      >
        {sorted.map(k => (
          <Card
            key={k.id}
            style={{
              padding: 12
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start"
              }}
            >
              <div>
                <div
                  style={{
                    color: C.text,
                    fontWeight: 600,
                    fontSize: 14
                  }}
                >
                  {k.description}
                </div>
                <div
                  style={{
                    color: C.textDim,
                    fontSize: 12
                  }}
                >
                  {dateFmt(k.date)}
                </div>
              </div>
              <div
                style={{
                  textAlign: "right"
                }}
              >
                <div
                  style={{
                    color: C.text,
                    fontFamily: "'JetBrains Mono', monospace",
                    fontWeight: 600
                  }}
                >
                  {pln(k.amount)}
                </div>
              </div>
            </div>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginTop: 8
              }}
            >
              <Pill text={k.type} color={C.copper} />
              {!k.id.startsWith("seed") && (
                <button onClick={() => remove(k.id)} style={trashBtn}>
                  <Icon.trash />
                </button>
              )}
            </div>
          </Card>
        ))}
      </div>
      {open && (
        <SheetModal title="Nowy koszt" onClose={() => setOpen(false)}>
          <Field label="Data">
            <input
              type="date"
              style={inputStyle}
              value={form.date}
              onChange={e => setForm({
                ...form,
                date: e.target.value
              })}
            />
          </Field>
          <Field label="Typ kosztu">
            <select
              style={inputStyle}
              value={form.type}
              onChange={e => setForm({
                ...form,
                type: e.target.value
              })}
            >
              {KOSZTY_TYPES.map(t => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </Field>
          <Field label="Opis">
            <input
              type="text"
              style={inputStyle}
              value={form.description}
              onChange={e => setForm({
                ...form,
                description: e.target.value
              })}
            />
          </Field>
          <Field label="Kwota (zł)">
            <input
              type="number"
              inputMode="decimal"
              style={inputStyle}
              value={form.amount}
              onChange={e => setForm({
                ...form,
                amount: e.target.value
              })}
            />
          </Field>
          <PrimaryButton onClick={save} disabled={!form.amount}>
            Zapisz koszt
          </PrimaryButton>
        </SheetModal>
      )}
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

/* ---------- TAB: USTAWIENIA ---------- */
function UstawieniaTab({
  data,
  setData
}) {
  const [local, setLocal] = useState(data.settings);
  const dirty = JSON.stringify(local) !== JSON.stringify(data.settings);
  const save = () => setData({
    ...data,
    settings: local
  });
  const fileInputRef = React.useRef(null);
  const [status, setStatus] = useState(null); // { type: 'ok'|'error', text }

  const handleExport = async () => {
    setStatus(null);
    const res = await exportBackup(data);
    if (res.ok && res.method !== "cancelled") {
      setStatus({
        type: "ok",
        text: res.method === "share" ? "Gotowe — wybierz Dysk Google w oknie udostępniania." : "Plik pobrany. Możesz go teraz przenieść na Dysk Google."
      });
    }
  };
  const handleImportClick = () => fileInputRef.current && fileInputRef.current.click();
  const handleFileChange = async e => {
    const file = e.target.files && e.target.files[0];
    e.target.value = "";
    if (!file) return;
    try {
      const imported = await readBackupFile(file);
      setData(imported);
      setStatus({
        type: "ok",
        text: "Dane wczytane z kopii zapasowej."
      });
    } catch (err) {
      setStatus({
        type: "error",
        text: err.message
      });
    }
  };
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 4
      }}
    >
      <Card>
        <Field label="Nazwa auta (nagłówek)">
          <input
            type="text"
            style={inputStyle}
            value={local.carName}
            onChange={e => setLocal({
              ...local,
              carName: e.target.value
            })}
            placeholder="np. CUPRA TERRAMAR"
          />
        </Field>
        <Field label="Podtytuł nagłówka">
          <input
            type="text"
            style={inputStyle}
            value={local.carSubtitle}
            onChange={e => setLocal({
              ...local,
              carSubtitle: e.target.value
            })}
            placeholder="np. DZIENNIK POKŁADOWY"
          />
        </Field>
        <Field label="Próg spalania — OK do (l/100km)">
          <input
            type="number"
            step="0.1"
            style={inputStyle}
            value={local.consumptionOkTo}
            onChange={e => setLocal({
              ...local,
              consumptionOkTo: +e.target.value
            })}
          />
        </Field>
        <Field label="Próg spalania — wysokie od (l/100km)">
          <input
            type="number"
            step="0.1"
            style={inputStyle}
            value={local.consumptionHighFrom}
            onChange={e => setLocal({
              ...local,
              consumptionHighFrom: +e.target.value
            })}
          />
        </Field>
        <Field label="Wzrost cen paliwa (rocznie, np. 0.05 = 5%)">
          <input
            type="number"
            step="0.01"
            style={inputStyle}
            value={local.fuelPriceGrowth}
            onChange={e => setLocal({
              ...local,
              fuelPriceGrowth: +e.target.value
            })}
          />
        </Field>
        <Field label="Przebieg miesięczny do symulacji (km)">
          <input
            type="number"
            style={inputStyle}
            value={local.monthlyKmPlan}
            onChange={e => setLocal({
              ...local,
              monthlyKmPlan: +e.target.value
            })}
          />
        </Field>
        <Field label="Cena auta / baza amortyzacji (zł)">
          <input
            type="number"
            style={inputStyle}
            value={local.carPrice}
            onChange={e => setLocal({
              ...local,
              carPrice: +e.target.value
            })}
          />
        </Field>
        <PrimaryButton onClick={save} disabled={!dirty}>
          Zapisz ustawienia
        </PrimaryButton>
      </Card>
      <Card
        style={{
          marginTop: 10
        }}
      >
        <div
          style={{
            fontSize: 13,
            fontWeight: 600,
            color: C.text,
            marginBottom: 4
          }}
        >
          Kopia zapasowa
        </div>
        <div
          style={{
            fontSize: 11.5,
            color: C.textFaint,
            marginBottom: 12,
            lineHeight: 1.5
          }}
        >
          Zapisz wszystkie dane do pliku i przenieś go np. na Dysk Google, albo wczytaj wcześniej zapisaną kopię.
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
            onClick={handleImportClick}
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
        {status && (
          <div
            style={{
              marginTop: 10,
              fontSize: 12,
              color: status.type === "error" ? C.red : C.green
            }}
          >
            {status.text}
          </div>
        )}
      </Card>
      <div
        style={{
          fontSize: 11.5,
          color: C.textFaint,
          padding: "10px 4px",
          lineHeight: 1.5
        }}
      >
        Dane są zapisywane bezpośrednio w pamięci tej przeglądarki na Twoim telefonie (localStorage) — zostają nawet po zamknięciu aplikacji. Kopia zapasowa to jedyny sposób, by przenieść je na inne urządzenie.
      </div>
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
    error
  } = useCarData();
  const [tab, setTab] = useState("dashboard");
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
            <div
              style={{
                width: 38,
                height: 38,
                borderRadius: 10,
                background: C.copper + "22",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                border: `1px solid ${C.copperDim}`
              }}
            >
              <Icon.car size={19} color={C.copper} />
            </div>
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
              {tab === "dashboard" && <Dashboard agg={agg} settings={data.settings} />}
              {tab === "tankowania" && <TankowaniaTab data={data} setData={setData} />}
              {tab === "serwisy" && <SerwisyTab data={data} setData={setData} />}
              {tab === "koszty" && <KosztyTab data={data} setData={setData} />}
              {tab === "prognoza" && <PrognozaTab agg={agg} settings={data.settings} />}
              {tab === "ustawienia" && <UstawieniaTab data={data} setData={setData} />}
            </>
          )}
        </main>
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
