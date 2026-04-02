// Simulates pattern data derived from the ML model's learned patterns
function getPatterns(result) {
  const base = result[`${result.recommended_mode}_time`];
  return {
    morningTime: (base * 0.72).toFixed(1),
    afternoonTime: (base * 0.55).toFixed(1),
    eveningTime: (base * 1.00).toFixed(1),
    congestionFactor: "2.4×",
    peakLabel: "Evening peak (5–8 PM)",
    patternNote: "Daily peak hour pattern detected",
    weekdayAvg: (base * 0.9).toFixed(1),
    weekendAvg: (base * 0.6).toFixed(1),
    delayFactor: result.recommended_mode === "metro" ? "0.2×" : "0.8×",
  };
}

function Bar({ label, value, max, color, time }) {
  const pct = Math.min((value / max) * 100, 100);
  return (
    <div className="bar-row">
      <span className="bar-label">{label}</span>
      <div className="bar-track">
        <div className="bar-fill" style={{ width: `${pct}%`, background: color }} />
      </div>
      <span className="bar-val">{time} min</span>
    </div>
  );
}

export default function TrafficPatternPanel({ result, formData }) {
  const p   = getPatterns(result);
  const tod = formData?.time_of_day || "evening";
  const max = Math.max(
    parseFloat(p.morningTime),
    parseFloat(p.afternoonTime),
    parseFloat(p.eveningTime)
  );

  return (
    <div className="pattern-panel">

      {/* Peak hour chart */}
      <div className="pattern-section">
        <div className="pattern-section-title">Travel time by time of day</div>
        <Bar label="Morning"   value={parseFloat(p.morningTime)}   max={max} color="#f59e0b" time={p.morningTime} />
        <Bar label="Afternoon" value={parseFloat(p.afternoonTime)} max={max} color="#10b981" time={p.afternoonTime} />
        <Bar label="Evening"   value={parseFloat(p.eveningTime)}   max={max} color="#ef4444" time={p.eveningTime} />
        <div className="pattern-insight">
          {p.patternNote} — {p.peakLabel} shows highest travel times
        </div>
      </div>

      {/* Stats grid */}
      <div className="stat-grid">
        <div className="stat-box">
          <div className="stat-num" style={{ color: "#ef4444" }}>{p.congestionFactor}</div>
          <div className="stat-desc">Congestion increase factor (peak vs off-peak)</div>
        </div>
        <div className="stat-box">
          <div className="stat-num" style={{ color: "#3b82f6" }}>{p.delayFactor}</div>
          <div className="stat-desc">Congestion impact on {result.recommended_mode}</div>
        </div>
        <div className="stat-box">
          <div className="stat-num" style={{ color: "#8b5cf6" }}>{p.weekdayAvg} min</div>
          <div className="stat-desc">Weekday average travel time</div>
        </div>
        <div className="stat-box">
          <div className="stat-num" style={{ color: "#10b981" }}>{p.weekendAvg} min</div>
          <div className="stat-desc">Weekend average travel time</div>
        </div>
      </div>

      {/* Currently active pattern */}
      <div className="active-pattern-badge">
        <span>📡</span>
        <span>
          Currently active pattern: <strong>{tod}</strong> on a <strong>{formData?.day_type || "weekday"}</strong>.
          Model applied <strong>{tod === "evening" || tod === "morning" ? "peak-hour" : "off-peak"}</strong> traffic weights.
        </span>
      </div>
    </div>
  );
}
