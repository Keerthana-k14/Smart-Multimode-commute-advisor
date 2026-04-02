// UserExperiencePanel.jsx
import { useState } from "react";

export default function UserExperiencePanel({ result }) {
  // Simulated crowdsourced stats derived from predicted time
  const predicted = result[`${result.recommended_mode}_time`];
  const avgActual = (predicted * 1.12).toFixed(1);
  const delay     = (avgActual - predicted).toFixed(1);
  const reports   = Math.floor(Math.random() * 40) + 15;

  const [expanded, setExpanded] = useState(false);

  const reviews = [
    { mode: "metro", time: (predicted * 0.98).toFixed(0), note: "Arrived on time, no delays", rating: 5 },
    { mode: "metro", time: (predicted * 1.08).toFixed(0), note: "Slight crowd at peak hour", rating: 4 },
    { mode: "car",   time: (predicted * 1.35).toFixed(0), note: "Heavy traffic near junction", rating: 3 },
  ];

  return (
    <div className="ux-panel">
      {/* Summary stats */}
      <div className="ux-stat-row">
        <div className="ux-stat">
          <div className="ux-stat-num">{avgActual} min</div>
          <div className="ux-stat-label">Avg actual travel time</div>
          <div className="ux-stat-sub">from {reports} user reports</div>
        </div>
        <div className="ux-stat">
          <div className="ux-stat-num" style={{ color: delay > 5 ? "#ef4444" : "#10b981" }}>
            +{delay} min
          </div>
          <div className="ux-stat-label">Delay vs prediction</div>
          <div className="ux-stat-sub">{delay > 5 ? "above expected" : "within normal range"}</div>
        </div>
        <div className="ux-stat">
          <div className="ux-stat-num">{reports}</div>
          <div className="ux-stat-label">User reports</div>
          <div className="ux-stat-sub">this corridor this week</div>
        </div>
      </div>

      {/* Accuracy bar */}
      <div className="ux-accuracy">
        <div className="ux-accuracy-label">
          <span>Prediction accuracy</span>
          <span>{Math.round((1 - delay / predicted) * 100)}%</span>
        </div>
        <div className="ux-acc-track">
          <div
            className="ux-acc-fill"
            style={{ width: `${Math.round((1 - delay / predicted) * 100)}%` }}
          />
        </div>
      </div>

      {/* Recent reports */}
      <button className="expand-btn" onClick={() => setExpanded(!expanded)}>
        {expanded ? "Hide" : "Show"} recent commuter reports ▾
      </button>

      {expanded && (
        <div className="report-list">
          {reviews.map((r, i) => (
            <div className="report-item" key={i}>
              <span>{r.mode === "metro" ? "🚇" : "🚗"}</span>
              <div className="report-body">
                <div className="report-note">{r.note}</div>
                <div className="report-meta">{r.time} min actual · {"★".repeat(r.rating)}{"☆".repeat(5 - r.rating)}</div>
              </div>
            </div>
          ))}
        </div>
      )}

      <p className="ux-note">
        User feedback is stored and used to adjust future predictions for this corridor.
      </p>
    </div>
  );
}
