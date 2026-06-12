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

// 50+ Bangalore location suggestions (matches backend KNOWN_LOCATIONS)
const SUGGESTIONS = [
  // Central
  "MG Road", "Brigade Road", "Majestic", "Shivajinagar", "Ulsoor",
  "Cubbon Park", "Richmond Town",
  // East
  "Indiranagar", "Domlur", "Koramangala", "HSR Layout", "BTM Layout",
  "Bellandur", "Sarjapur Road", "Marathahalli", "Whitefield",
  "HAL", "Old Airport Road", "Varthur", "Kadugodi", "Kadugodi Tree Park", 
  "Hopefarm", "Kr Puram", "Mahadevapura",
  // South
  "Jayanagar", "JP Nagar", "Bannerghatta Road", "Electronic City",
  "Silk Board", "Bommanahalli", "Basavanagudi", "Banashankari",
  "Kumaraswamy Layout", "Kanakapura Road", "Uttarahalli", "Arekere",
  "Wilson Garden", "Lalbagh",
  // North
  "Hebbal", "Yeshwanthpur", "Rajajinagar", "Malleshwaram",
  "Sadashivanagar", "Yelahanka", "Thanisandra", "Nagawara",
  "Rt Nagar", "Banaswadi", "Hennur", "Kalyan Nagar",
  // West
  "Vijayanagar", "Basaveshwaranagar", "Nagarbhavi", "Kengeri",
  "Peenya", "Magadi Road", "Mysore Road", "Rr Nagar", "Nayandahalli",
  // Outer / IT Corridors
  "Hosur Road", "Tumkur Road", "Outer Ring Road", "Devanahalli",
  "Kempegowda Airport", "Hoskote", "Anekal", "Begur", "Hulimavu",
  "Jp Nagar 6Th Phase", "Gottigere", "Konanakunte"
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