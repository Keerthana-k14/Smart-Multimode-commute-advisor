import { useState } from "react";
import ExplainerPanel      from "./ExplainerPanel";
import TrafficPatternPanel from "./TrafficPatternPanel";
import UserExperiencePanel from "./UserExperiencePanel";
import ModelInfoPanel      from "./ModelInfoPanel";
import FeedbackForm        from "./FeedbackForm";
import MapView             from "./MapView";

const MODE_ICONS = { car: "🚗", bike: "🏍️", metro: "🚇", bus: "🚌" };
const MODE_COLOR = { car: "#f59e0b", bike: "#ec4899", metro: "#3b82f6", bus: "#10b981" };

function getConfidence(times, mode) {
  const best  = times[`${mode}_time`];
  const worst = Math.max(times.car_time, times.bike_time || 0, times.metro_time, times.bus_time);
  const gap   = worst - best;
  if (gap > 15) return { label: "High",     pct: 92 };
  if (gap > 7)  return { label: "Medium",   pct: 74 };
  return           { label: "Moderate",  pct: 58 };
}

export default function ResultDashboard({ result, formData }) {
  const [activeTab, setActiveTab] = useState("explain");
  const conf  = getConfidence(result, result.recommended_mode);
  const color = MODE_COLOR[result.recommended_mode];

  // Extract distance_info if available (from the new /predict response)
  const distInfo = result.distance_info || null;
  const modes = distInfo ? distInfo.modes : null;

  return (
    <div className="result-dashboard">

      {/* ── A. RECOMMENDATION CARD ── */}
      <div className="rec-card" style={{ "--accent": color }}>

        {/* Route label */}
        <div className="rec-route-label">
          <span className="route-from">{result.source || result.area}</span>
          <span className="route-arrow">→</span>
          <span className="route-to">{result.destination || result.road}</span>
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
                {result.recommended_mode === "bike" ? "TWO-WHEELER" : result.recommended_mode.toUpperCase()}
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

        {/* All 4 mode times — now with distance & travel time breakdown */}
        <div className="mode-compare" style={{ gridTemplateColumns: "repeat(4, 1fr)" }}>
          {["car", "bike", "metro", "bus"].map(m => {
            const modeInfo = modes ? modes[m] : null;
            const modeName = m === "bike" ? "Two-Wheeler" : m;
            return (
              <div
                key={m}
                className={`mode-tile ${result.recommended_mode === m ? "mode-tile-best" : ""}`}
                style={result.recommended_mode === m ? { borderColor: color } : {}}
              >
                <div className="mode-tile-top">
                  <span className="mode-tile-icon">{MODE_ICONS[m]}</span>
                  <span className="mode-tile-name">{modeName}</span>
                </div>
                <span
                  className="mode-tile-time"
                  style={result.recommended_mode === m ? { color } : {}}
                >
                  {result[`${m}_time`] || "—"} min
                </span>

                {/* Per-mode distance & time from distance engine */}
                {modeInfo && (
                  <div className="mode-tile-dist">
                    <span className="mode-dist-value">
                      📏 {modeInfo.distance_km} km
                    </span>
                    <span className="mode-time-value">
                      ⏱ {modeInfo.time_mins} min
                    </span>
                  </div>
                )}

                {/* Metro route details - moved to a standardized hover/small section or just kept but with tile height matched */}
                {m === "metro" && modeInfo && modeInfo.details && (
                  <div className="mode-tile-detail">
                    {modeInfo.details}
                  </div>
                )}

                {result.recommended_mode === m && (
                  <span
                    className="mode-tile-best-tag"
                    style={{ background: color }}
                  >
                    BEST
                  </span>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* ── DISTANCE BREAKDOWN CARD ── */}
      {distInfo && (
        <div className="distance-card">
          <div className="distance-card-header">
            <span className="distance-card-icon">📊</span>
            <span className="distance-card-title">Distance & Time Breakdown</span>
          </div>
          <div className="distance-card-body">
            <table className="distance-table">
              <thead>
                <tr>
                  <th>Mode</th>
                  <th>Distance</th>
                  <th>Est. Travel Time</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {["car", "bike", "bus", "metro"].map(m => {
                  const info = distInfo.modes[m];
                  if (!info) return null;
                  const isBest = distInfo.recommended === m;
                  const isMetroViable = m === "metro" ? info.is_viable : true;
                  return (
                    <tr key={m} className={isBest ? "distance-row-best" : ""}>
                      <td>
                        <span className="distance-mode-icon">{MODE_ICONS[m]}</span>
                        {m === "bike" ? "Two-Wheeler" : m.charAt(0).toUpperCase() + m.slice(1)}
                      </td>
                      <td>{info.distance_km} km</td>
                      <td className="distance-time-cell">
                        {info.time_mins < 999 ? `${info.time_mins} min` : "—"}
                      </td>
                      <td>
                        {isBest && (
                          <span className="distance-best-badge" style={{ background: MODE_COLOR[m] }}>
                            ⚡ Fastest
                          </span>
                        )}
                        {m === "metro" && !isMetroViable && (
                          <span className="distance-not-viable">Not viable</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            {distInfo.modes.metro && distInfo.modes.metro.details && (
              <div className="distance-metro-detail">
                🚇 Metro route: {distInfo.modes.metro.details}
              </div>
            )}
          </div>
        </div>
      )}

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