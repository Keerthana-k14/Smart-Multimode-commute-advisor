import { useState } from "react";
import { getPredict } from "../api/client";

const TIME_OPTIONS = [
  { value: "morning",   label: "Morning",   sub: "8 – 10 AM", icon: "🌅" },
  { value: "afternoon", label: "Afternoon", sub: "12 – 5 PM", icon: "☀️" },
  { value: "evening",   label: "Evening",   sub: "5 – 8 PM",  icon: "🌆" },
];

const DAY_OPTIONS = [
  { value: "weekday", label: "Weekday", icon: "💼" },
  { value: "weekend", label: "Weekend", icon: "🏖" },
];

// Bangalore location suggestions
const SUGGESTIONS = [
  "Koramangala", "Indiranagar", "Whitefield", "MG Road",
  "Hebbal", "Electronic City", "Jayanagar", "JP Nagar",
  "Marathahalli", "HSR Layout", "Bannerghatta Road",
  "Yeshwanthpur", "Rajajinagar", "Malleshwaram",
  "BTM Layout", "Bellandur", "Sarjapur Road"
];

function LocationInput({ label, marker, value, onChange, placeholder }) {
  const [showSug, setShowSug] = useState(false);
  const filtered = SUGGESTIONS.filter(s =>
    s.toLowerCase().includes(value.toLowerCase()) && value.length > 0
  );

  return (
    <div className="form-field" style={{ position: "relative" }}>
      <label className="field-label">
        <span className="label-num">{marker}</span> {label}
      </label>
      <input
        className="field-input"
        type="text"
        placeholder={placeholder}
        value={value}
        onChange={e => { onChange(e.target.value); setShowSug(true); }}
        onFocus={() => setShowSug(true)}
        onBlur={() => setTimeout(() => setShowSug(false), 150)}
        autoComplete="off"
      />
      {showSug && filtered.length > 0 && (
        <div className="suggestion-box">
          {filtered.map(s => (
            <div
              key={s}
              className="suggestion-item"
              onMouseDown={() => { onChange(s); setShowSug(false); }}
            >
              📍 {s}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function RouteForm({ onResult, loading, setLoading }) {
  const [form, setForm] = useState({
    source: "", destination: "",
    time_of_day: "evening", day_type: "weekday"
  });
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!form.source.trim() || !form.destination.trim()) {
      setError("Please enter both source and destination.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      // Map free text to backend payload
      // area = source, road = destination
      const payload = {
        area:       form.source.trim(),
        road:       form.destination.trim(),
        time_of_day: form.time_of_day,
        day_type:   form.day_type,
        congestion: "auto"
      };
      const { data } = await getPredict(payload);
      // Attach source/destination for display
      onResult({ ...data, source: form.source, destination: form.destination }, form);
    } catch {
      setError("Cannot connect to backend. Make sure uvicorn is running.");
    }
    setLoading(false);
  };

  return (
    <div className="route-form">
      <LocationInput
        label="Source"
        marker="A"
        value={form.source}
        onChange={v => setForm({ ...form, source: v })}
        placeholder="e.g. Koramangala"
      />

      <LocationInput
        label="Destination"
        marker="B"
        value={form.destination}
        onChange={v => setForm({ ...form, destination: v })}
        placeholder="e.g. Whitefield"
      />

      <div className="form-field">
        <label className="field-label">Time of Day</label>
        <div className="toggle-group">
          {TIME_OPTIONS.map(opt => (
            <button
              key={opt.value}
              className={`toggle-btn ${form.time_of_day === opt.value ? "active" : ""}`}
              onClick={() => setForm({ ...form, time_of_day: opt.value })}
              type="button"
            >
              <span className="toggle-icon">{opt.icon}</span>
              <span className="toggle-label">{opt.label}</span>
              <span className="toggle-sub">{opt.sub}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="form-field">
        <label className="field-label">Day Type</label>
        <div className="toggle-group toggle-group-2">
          {DAY_OPTIONS.map(opt => (
            <button
              key={opt.value}
              className={`toggle-btn ${form.day_type === opt.value ? "active" : ""}`}
              onClick={() => setForm({ ...form, day_type: opt.value })}
              type="button"
            >
              <span className="toggle-icon">{opt.icon}</span>
              <span className="toggle-label">{opt.label}</span>
            </button>
          ))}
        </div>
      </div>


      {error && <p className="form-error">{error}</p>}

      <button
        className="submit-btn"
        onClick={handleSubmit}
        disabled={loading || !form.source || !form.destination}
      >
        {loading
          ? <><span className="btn-spinner" /> Predicting...</>
          : "Get Recommendation →"
        }
      </button>
    </div>
  );
}