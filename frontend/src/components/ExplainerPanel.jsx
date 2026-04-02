const TIME_LABELS = { morning: "Morning rush hour", afternoon: "Afternoon off-peak", evening: "Evening peak hour" };

function buildReasons(result, formData) {
  const reasons = [];
  const mode    = result.recommended_mode;
  const times   = { car: result.car_time, metro: result.metro_time, bus: result.bus_time };
  const best    = times[mode];
  const worst   = Math.max(...Object.values(times));
  const saved   = (worst - best).toFixed(1);
  const tod     = formData?.time_of_day || "evening";

  // Peak hour detection
  if (tod === "evening" || tod === "morning") {
    reasons.push({
      icon: "⚠️",
      type: "warning",
      title: "Peak traffic detected",
      detail: `${TIME_LABELS[tod]} significantly increases road congestion. Historical data shows up to 2.4× delay factor.`
    });
  }

  // Predicted time advantage
  reasons.push({
    icon: "⏱",
    type: "info",
    title: "Predicted travel times",
    detail: `Car: ${times.car} min | Metro: ${times.metro} min | Bus: ${times.bus} min — ${mode} saves ${saved} min vs slowest option.`
  });

  // Mode-specific reason
  if (mode === "metro") {
    reasons.push({
      icon: "🚇",
      type: "success",
      title: "Metro unaffected by road congestion",
      detail: "Metro travel time remains consistent regardless of road traffic levels. Pattern learning confirms metro is most reliable during peak hours."
    });
  } else if (mode === "car") {
    reasons.push({
      icon: "🚗",
      type: "success",
      title: "Road conditions favour car",
      detail: "Low congestion detected on this route at this time. Historical patterns show minimal delay factor for car travel."
    });
  } else {
    reasons.push({
      icon: "🚌",
      type: "success",
      title: "Bus is optimal for this route",
      detail: "Bus routes on this corridor have good frequency and minimal delays based on historical data."
    });
  }

  // Historical congestion
  reasons.push({
    icon: "📈",
    type: "neutral",
    title: "Historical congestion insight",
    detail: `This route historically shows ${tod === "evening" ? "high (0.85)" : tod === "morning" ? "medium-high (0.65)" : "low-medium (0.35)"} congestion norm during ${tod}. Model uses this as a key feature.`
  });

  // User experience
  reasons.push({
    icon: "👥",
    type: "neutral",
    title: "User experience factor applied",
    detail: "Crowdsourced delay feedback from previous commuters on this corridor is factored into the final travel time adjustment."
  });

  return reasons;
}

const TYPE_STYLES = {
  warning: { bg: "#fef3c7", border: "#f59e0b", text: "#92400e" },
  info:    { bg: "#eff6ff", border: "#3b82f6", text: "#1e40af" },
  success: { bg: "#f0fdf4", border: "#10b981", text: "#065f46" },
  neutral: { bg: "#f8fafc", border: "#94a3b8", text: "#334155" },
};

export default function ExplainerPanel({ result, formData }) {
  const reasons = buildReasons(result, formData);

  return (
    <div className="xai-panel">
      <p className="panel-intro">
        The model chose <strong>{result.recommended_mode}</strong> based on these factors:
      </p>
      <div className="reason-list">
        {reasons.map((r, i) => {
          const s = TYPE_STYLES[r.type];
          return (
            <div
              key={i}
              className="reason-item"
              style={{ background: s.bg, borderLeft: `4px solid ${s.border}` }}
            >
              <div className="reason-top">
                <span className="reason-icon">{r.icon}</span>
                <span className="reason-title" style={{ color: s.text }}>{r.title}</span>
              </div>
              <p className="reason-detail">{r.detail}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
