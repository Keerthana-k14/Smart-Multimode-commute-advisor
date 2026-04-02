import { useState } from "react";
import ExplainerPanel      from "./ExplainerPanel";
import TrafficPatternPanel from "./TrafficPatternPanel";
import UserExperiencePanel from "./UserExperiencePanel";
import ModelInfoPanel      from "./ModelInfoPanel";
import FeedbackForm        from "./FeedbackForm";
import MapView             from "./MapView";

const MODE_ICONS = { car: "🚗", metro: "🚇", bus: "🚌" };
const MODE_COLOR = { car: "#f59e0b", metro: "#3b82f6", bus: "#10b981" };

function getConfidence(times, mode) {
  const best  = times[`${mode}_time`];
  const worst = Math.max(times.car_time, times.metro_time, times.bus_time);
  const gap   = worst - best;
  if (gap > 15) return { label: "High",     pct: 92 };
  if (gap > 7)  return { label: "Medium",   pct: 74 };
  return           { label: "Moderate",  pct: 58 };
}

export default function ResultDashboard({ result, formData }) {
  const [activeTab, setActiveTab] = useState("explain");
  const conf  = getConfidence(result, result.recommended_mode);
  const color = MODE_COLOR[result.recommended_mode];

  return (
    <div className="result-dashboard">

      {/* ── A. RECOMMENDATION CARD ── */}
      <div className="rec-card" style={{ "--accent": color }}>

        {/* Route label */}
        <div className="rec-route-label">
          <span className="route-from">{result.source}</span>
          <span className="route-arrow">→</span>
          <span className="route-to">{result.destination}</span>
          {result.distance_km && (
            <span className="route-dist" style={{ marginLeft: "10px", fontSize: "0.85em", opacity: 0.8 }}>
              • {result.distance_km} km
            </span>
          )}
        </div>

        <div className="rec-header">
          <div className="rec-mode-badge">
            <span className="rec-icon">{MODE_ICONS[result.recommended_mode]}</span>
            <div>
              <div className="rec-label">Recommended Mode</div>
              <div className="rec-mode" style={{ color }}>
                {result.recommended_mode.toUpperCase()}
              </div>
            </div>
          </div>
          <div className="rec-time-block">
            <div className="rec-time-num">
              {result[`${result.recommended_mode}_time`]}
            </div>
            <div className="rec-time-unit">min estimated</div>
          </div>
        </div>

        {/* Confidence bar */}
        <div className="conf-row">
          <span className="conf-label">Confidence</span>
          <div className="conf-bar-wrap">
            <div
              className="conf-bar"
              style={{ width: `${conf.pct}%`, background: color }}
            />
          </div>
          <span className="conf-pct">{conf.label} ({conf.pct}%)</span>
        </div>

        {/* All 3 mode times */}
        <div className="mode-compare">
          {["car", "metro", "bus"].map(m => (
            <div
              key={m}
              className={`mode-tile ${result.recommended_mode === m ? "mode-tile-best" : ""}`}
              style={result.recommended_mode === m ? { borderColor: color } : {}}
            >
              <span className="mode-tile-icon">{MODE_ICONS[m]}</span>
              <span className="mode-tile-name">{m}</span>
              <span
                className="mode-tile-time"
                style={result.recommended_mode === m ? { color } : {}}
              >
                {result[`${m}_time`]} min
              </span>
              {result.recommended_mode === m && (
                <span
                  className="mode-tile-best-tag"
                  style={{ background: color }}
                >
                  BEST
                </span>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* ── MAP ── */}
      <MapView
        source={result.source}
        destination={result.destination}
      />

      {/* ── TABS: B, C, D ── */}
      <div className="tabs-card">
        <div className="tabs-header">
          {[
            { key: "explain", label: "🧠 Explainable AI"      },
            { key: "pattern", label: "📊 Traffic Patterns"    },
            { key: "users",   label: "👥 User Experience"     },
          ].map(tab => (
            <button
              key={tab.key}
              className={`tab-btn ${activeTab === tab.key ? "tab-active" : ""}`}
              onClick={() => setActiveTab(tab.key)}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="tab-body">
          {activeTab === "explain" && (
            <ExplainerPanel result={result} formData={formData} />
          )}
          {activeTab === "pattern" && (
            <TrafficPatternPanel result={result} formData={formData} />
          )}
          {activeTab === "users" && (
            <UserExperiencePanel result={result} />
          )}
        </div>
      </div>

      {/* ── E. MODEL INFO ── */}
      <ModelInfoPanel />

      {/* ── FEEDBACK ── */}
      <FeedbackForm result={result} />

    </div>
  );
}