import ExplainerPanel from "./ExplainerPanel";
import FeedbackForm   from "./FeedbackForm";

const MODE_ICONS = { car: "🚗", metro: "🚇", bus: "🚌" };

export default function ResultCard({ result }) {
  if (!result) return null;

  return (
    <div className="card result-card">
      <h2>Recommendation — {result.area}, {result.road}</h2>

      <div className="recommended-badge">
        <span className="mode-icon">{MODE_ICONS[result.recommended_mode]}</span>
        {result.recommended_mode.toUpperCase()} RECOMMENDED
      </div>

      <div className="times-grid">
        {["car", "metro", "bus"].map(mode => (
          <div key={mode} className={`time-box ${result.recommended_mode === mode ? "best" : ""}`}>
            <div className="time-icon">{MODE_ICONS[mode]}</div>
            <div className="mode-name">{mode}</div>
            <div className="time-value">{result[`${mode}_time`]}</div>
            <div className="time-unit">minutes</div>
            {result.recommended_mode === mode &&
              <div style={{ fontSize: "0.7rem", color: "#38a169", marginTop: 4, fontWeight: 600 }}>
                BEST
              </div>
            }
          </div>
        ))}
      </div>

      <ExplainerPanel explanation={result.explanation} />
      <FeedbackForm result={result} />
    </div>
  );
}