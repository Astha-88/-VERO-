import { useEffect, useState } from "react";
import "./App.css";

type Route =
  | { kind: "home" }
  | { kind: "about" }
  | { kind: "check" }
  | { kind: "vehicle"; id: number }
  | { kind: "not-found" };

type Vehicle = {
  id: number;
  registration_number: string;
  created_at?: string;
};

type VehicleDetails = {
  make?: string | null;
  model?: string | null;
  variant?: string | null;
  manufacturing_year?: number | null;
  fuel_type?: string | null;
};

type Ownership = {
  id: number;
  owner_sequence: number;
  owner_name?: string | null;
  purchase_date?: string | null;
  transfer_date?: string | null;
};

type ServiceRecord = {
  id: number;
  service_date: string;
  service_type: string;
  odometer_reading?: number | null;
  description?: string | null;
  service_center?: string | null;
  cost?: number | string | null;
};

type Incident = {
  id: number;
  incident_type: string;
  incident_date: string;
  severity: string;
  description?: string | null;
  reported_by?: string | null;
  repair_cost?: number | string | null;
};

type VehicleProfile = {
  vehicle: Vehicle;
  details?: VehicleDetails | null;
  ownership?: Ownership[];
  service_records?: ServiceRecord[];
  incidents?: Incident[];
};

type RiskAssessment = {
  risk_score: number;
  risk_level: string;
  red_flags: string[];
  positive_signals: string[];
};

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000").replace(/\/$/, "");

function getRoute(pathname = window.location.pathname): Route {
  const path = pathname.replace(/\/+$/, "") || "/";

  if (path === "/") return { kind: "home" };
  if (path === "/about") return { kind: "about" };
  if (path === "/check") return { kind: "check" };

  const vehicleMatch = path.match(/^\/vehicles\/(\d+)$/);
  if (vehicleMatch) return { kind: "vehicle", id: Number(vehicleMatch[1]) };

  return { kind: "not-found" };
}

function navigate(path: string) {
  window.history.pushState({}, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
  if (window.location.hash) {
    window.setTimeout(() => {
      document.querySelector(window.location.hash)?.scrollIntoView({ behavior: "smooth" });
    }, 0);
  } else {
    window.scrollTo({ top: 0, behavior: "instant" });
  }
}

function App() {
  const [route, setRoute] = useState<Route>(() => getRoute());

  useEffect(() => {
    const handlePopState = () => setRoute(getRoute());
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  return (
    <div className="app-shell">
      <Header />
      <main className="page-content">
        {route.kind === "home" && <HomePage />}
        {route.kind === "about" && <AboutPage />}
        {route.kind === "check" && <CheckPage />}
        {route.kind === "vehicle" && <VehiclePage vehicleId={route.id} />}
        {route.kind === "not-found" && <NotFoundPage />}
      </main>
      <Footer />
    </div>
  );
}

function Header() {
  return (
    <header className="navbar">
      <button className="brand" onClick={() => navigate("/")} aria-label="VERO home">
        VERO
      </button>
      <nav className="nav-links" aria-label="Primary navigation">
        <button onClick={() => navigate("/#how-it-works")}>How it works</button>
        <button onClick={() => navigate("/about")}>About</button>
      </nav>
    </header>
  );
}

function HomePage() {
  const [registrationNumber, setRegistrationNumber] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submit = async () => {
    const registration = registrationNumber.trim().toUpperCase();
    if (!registration) {
      setError("Enter a vehicle registration number first.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const response = await fetch(
        `${API_BASE_URL}/vehicles?registration_number=${encodeURIComponent(registration)}`,
      );
      if (!response.ok) {
        throw new Error(response.status === 404 ? "Vehicle not found." : "Unable to check this vehicle right now.");
      }

      const payload: unknown = await response.json();
      const vehicles = extractVehicles(payload);
      const vehicle = vehicles.find(
        (item) => item.registration_number.toUpperCase() === registration,
      ) ?? vehicles[0];

      if (!vehicle) throw new Error("Vehicle not found.");
      navigate(`/vehicles/${vehicle.id}`);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to check this vehicle right now.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <section className="hero-section">
        <div className="hero-content">
          <p className="eyebrow">VEHICLE DUE DILIGENCE</p>
          <h1>Know the car<br />before you buy it.</h1>
          <p className="hero-description">
            Get a complete picture of a used vehicle&apos;s history, ownership,
            service records, incidents, and risk — all in one place.
          </p>

          <div className="search-box">
            <input
              value={registrationNumber}
              onChange={(event) => setRegistrationNumber(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") void submit();
              }}
              placeholder="Enter vehicle registration number"
              aria-label="Vehicle registration number"
              autoComplete="off"
            />
            <button type="button" onClick={() => void submit()} disabled={loading}>
              {loading ? "Checking…" : "Check vehicle"}
            </button>
          </div>
          <p className="search-hint">Example: DL01AB1234</p>
          {error && <p className="form-error" role="alert">{error}</p>}
        </div>
      </section>

      <section id="how-it-works" className="features-section">
        <div className="section-heading">
          <p className="eyebrow">WHAT VERO CHECKS</p>
          <h2>Everything you need before saying yes.</h2>
        </div>
        <div className="feature-grid">
          <Feature number="01" title="Vehicle details">Core information about the vehicle, including make, model, variant, year, and fuel type.</Feature>
          <Feature number="02" title="Ownership history">Understand how many owners the vehicle has had and how its ownership changed over time.</Feature>
          <Feature number="03" title="Service & incidents">Review recorded maintenance, accidents, incidents, repairs, costs, and other warning signals.</Feature>
          <Feature number="04" title="Risk assessment">VERO combines the available history into an easy-to-understand vehicle risk assessment.</Feature>
        </div>
      </section>
    </>
  );
}

function Feature({ number, title, children }: { number: string; title: string; children: string }) {
  return (
    <article className="feature-card">
      <span>{number}</span>
      <h3>{title}</h3>
      <p>{children}</p>
    </article>
  );
}

function CheckPage() {
  const [registrationNumber, setRegistrationNumber] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submit = async () => {
    const registration = registrationNumber.trim().toUpperCase();
    if (!registration) {
      setError("Enter a vehicle registration number first.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE_URL}/vehicles?registration_number=${encodeURIComponent(registration)}`);
      if (!response.ok) throw new Error(response.status === 404 ? "Vehicle not found." : "Unable to check this vehicle right now.");
      const vehicles = extractVehicles(await response.json());
      const vehicle = vehicles[0];
      if (!vehicle) throw new Error("Vehicle not found.");
      navigate(`/vehicles/${vehicle.id}`);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to check this vehicle right now.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="inner-page check-page">
      <p className="eyebrow">CHECK A VEHICLE</p>
      <h1>Look before you buy.</h1>
      <p className="lead">Enter the registration number to retrieve the vehicle&apos;s recorded history and VERO risk assessment.</p>
      <div className="search-box search-box-large">
        <input value={registrationNumber} onChange={(event) => setRegistrationNumber(event.target.value)} placeholder="DL01AB1234" aria-label="Vehicle registration number" />
        <button type="button" disabled={loading} onClick={() => void submit()}>{loading ? "Checking…" : "Check vehicle"}</button>
      </div>
      {error && <p className="form-error" role="alert">{error}</p>}
    </section>
  );
}

function VehiclePage({ vehicleId }: { vehicleId: number }) {
  const [profile, setProfile] = useState<VehicleProfile | null>(null);
  const [risk, setRisk] = useState<RiskAssessment | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      setError("");
      try {
        const [profileResponse, riskResponse] = await Promise.all([
          fetch(`${API_BASE_URL}/vehicles/${vehicleId}/profile`),
          fetch(`${API_BASE_URL}/vehicles/${vehicleId}/risk-assessment`),
        ]);
        if (!profileResponse.ok) throw new Error(profileResponse.status === 404 ? "Vehicle not found." : "Could not load the vehicle profile.");
        if (!riskResponse.ok) throw new Error("Could not load the vehicle risk assessment.");

        const profilePayload = normalizeProfile(await profileResponse.json(), vehicleId);
        const riskPayload = (await riskResponse.json()) as RiskAssessment;
        if (!cancelled) {
          setProfile(profilePayload);
          setRisk(riskPayload);
        }
      } catch (requestError) {
        if (!cancelled) setError(requestError instanceof Error ? requestError.message : "Could not load this vehicle.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    void load();
    return () => { cancelled = true; };
  }, [vehicleId]);

  if (loading) return <LoadingState message="Building your vehicle report…" />;
  if (error) return <ErrorState message={error} />;
  if (!profile || !risk) return <ErrorState message="The vehicle report could not be loaded." />;

  const details = profile.details;
  const ownership = profile.ownership ?? [];
  const services = profile.service_records ?? [];
  const incidents = profile.incidents ?? [];

  return (
    <section className="inner-page results-page">
      <button className="back-link" onClick={() => navigate("/check")}>← Check another vehicle</button>
      <div className="results-header">
        <div>
          <p className="eyebrow">VEHICLE REPORT</p>
          <h1>{details?.make || "Vehicle"} {details?.model || ""}</h1>
          <p className="registration-pill">{profile.vehicle.registration_number}</p>
        </div>
        <RiskBadge level={risk.risk_level} score={risk.risk_score} />
      </div>

      <div className="results-grid">
        <InfoCard title="Vehicle details">
          <DataRow label="Make" value={details?.make} />
          <DataRow label="Model" value={details?.model} />
          <DataRow label="Variant" value={details?.variant} />
          <DataRow label="Manufacturing year" value={details?.manufacturing_year?.toString()} />
          <DataRow label="Fuel type" value={details?.fuel_type} />
        </InfoCard>

        <InfoCard title="Risk assessment">
          <div className="risk-score"><strong>{risk.risk_score}</strong><span>/ 100</span></div>
          <div className="risk-meter"><span style={{ width: `${Math.min(Math.max(risk.risk_score, 0), 100)}%` }} /></div>
          <div className="signal-columns">
            <SignalList title="Red flags" items={risk.red_flags} negative />
            <SignalList title="Positive signals" items={risk.positive_signals} />
          </div>
        </InfoCard>
      </div>

      <InfoCard title={`Ownership history · ${ownership.length} recorded`}>
        {ownership.length ? <div className="timeline">{ownership.map((owner) => <div className="timeline-item" key={owner.id}><strong>Owner {owner.owner_sequence}</strong><span>{owner.owner_name || "Name unavailable"}</span><small>{formatDate(owner.purchase_date)}{owner.transfer_date ? ` → ${formatDate(owner.transfer_date)}` : " → Current/last recorded owner"}</small></div>)}</div> : <EmptyState text="No ownership records are currently available." />}
      </InfoCard>

      <InfoCard title={`Service records · ${services.length} recorded`}>
        {services.length ? <div className="record-list">{services.map((service) => <div className="record" key={service.id}><div><strong>{service.service_type}</strong><span>{formatDate(service.service_date)}{service.service_center ? ` · ${service.service_center}` : ""}</span></div><strong>{formatMoney(service.cost)}</strong></div>)}</div> : <EmptyState text="No service records are currently available." />}
      </InfoCard>

      <InfoCard title={`Incidents · ${incidents.length} recorded`}>
        {incidents.length ? <div className="record-list">{incidents.map((incident) => <div className="record" key={incident.id}><div><strong>{incident.incident_type} · {incident.severity}</strong><span>{formatDate(incident.incident_date)}{incident.description ? ` · ${incident.description}` : ""}</span></div><strong>{formatMoney(incident.repair_cost)}</strong></div>)}</div> : <EmptyState text="No incidents have been reported." />}
      </InfoCard>
    </section>
  );
}

function RiskBadge({ level, score }: { level: string; score: number }) {
  const tone = level.toLowerCase().replace(/\s+/g, "-");
  return <div className={`risk-badge ${tone}`}><span>RISK</span><strong>{level}</strong><small>{score}/100</small></div>;
}

function InfoCard({ title, children }: { title: string; children: React.ReactNode }) {
  return <section className="info-card"><h2>{title}</h2>{children}</section>;
}

function DataRow({ label, value }: { label: string; value?: string | null }) {
  return <div className="data-row"><span>{label}</span><strong>{value || "Not available"}</strong></div>;
}

function SignalList({ title, items, negative = false }: { title: string; items: string[]; negative?: boolean }) {
  return <div className={`signal-list ${negative ? "negative" : ""}`}><h3>{title}</h3>{items.length ? <ul>{items.map((item) => <li key={item}>{item}</li>)}</ul> : <p>None recorded.</p>}</div>;
}

function EmptyState({ text }: { text: string }) { return <p className="empty-state">{text}</p>; }
function LoadingState({ message }: { message: string }) { return <section className="state-page"><div className="spinner" /><p>{message}</p></section>; }
function ErrorState({ message }: { message: string }) { return <section className="state-page"><p className="eyebrow">SOMETHING WENT WRONG</p><h1>We couldn&apos;t load this report.</h1><p className="lead">{message}</p><button className="primary-button" onClick={() => navigate("/check")}>Back to vehicle check</button></section>; }

function AboutPage() {
  return <section className="inner-page about-page"><p className="eyebrow">ABOUT VERO</p><h1>Know what you&apos;re buying.</h1><p className="lead">VERO is a vehicle due-diligence experience designed to bring a used car&apos;s recorded history into one clear picture before a buyer commits.</p><div className="about-grid"><InfoCard title="What we bring together"><p>Vehicle details, ownership history, service records, incidents, repair information, and a transparent risk assessment.</p></InfoCard><InfoCard title="Why it matters"><p>A used vehicle can look perfect on the outside while its history tells a very different story. VERO helps you inspect the information that deserves a closer look.</p></InfoCard></div></section>;
}

function NotFoundPage() { return <section className="state-page"><p className="eyebrow">404</p><h1>That page doesn&apos;t exist.</h1><p className="lead">The route you entered isn&apos;t part of VERO.</p><button className="primary-button" onClick={() => navigate("/")}>Go home</button></section>; }

function Footer() { return <footer className="footer"><span>VERO</span><span>Vehicle due diligence, made clearer.</span></footer>; }

function extractVehicles(payload: unknown): Vehicle[] {
  const candidates = Array.isArray(payload) ? payload : isRecord(payload) ? (Array.isArray(payload.items) ? payload.items : Array.isArray(payload.data) ? payload.data : [payload]) : [];
  return candidates.filter(isRecord).map((item) => ({ id: Number(item.id), registration_number: String(item.registration_number ?? ""), created_at: typeof item.created_at === "string" ? item.created_at : undefined })).filter((item) => Number.isFinite(item.id) && item.registration_number);
}

function normalizeProfile(payload: unknown, vehicleId: number): VehicleProfile {
  const root = isRecord(payload) ? payload : {};
  const vehicle = isRecord(root.vehicle) ? root.vehicle : root;
  return {
    vehicle: { id: Number(vehicle.id ?? vehicleId), registration_number: String(vehicle.registration_number ?? "Unknown") },
    details: isRecord(root.details) ? root.details as VehicleDetails : null,
    ownership: Array.isArray(root.ownership) ? root.ownership as Ownership[] : [],
    service_records: Array.isArray(root.service_records) ? root.service_records as ServiceRecord[] : [],
    incidents: Array.isArray(root.incidents) ? root.incidents as Incident[] : [],
  };
}

function isRecord(value: unknown): value is Record<string, unknown> { return typeof value === "object" && value !== null && !Array.isArray(value); }
function formatDate(value?: string | null) { if (!value) return "Date unavailable"; const date = new Date(value); return Number.isNaN(date.getTime()) ? value : date.toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }); }
function formatMoney(value?: number | string | null) { if (value === null || value === undefined || value === "") return ""; const amount = Number(value); return Number.isFinite(amount) ? `₹${amount.toLocaleString("en-IN", { maximumFractionDigits: 2 })}` : String(value); }

export default App;
