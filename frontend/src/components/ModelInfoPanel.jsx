// ModelInfoPanel.jsx
const FEATURES = [
  { name: "Hour of day",     importance: 88, color: "#3b82f6" },
  { name: "Is peak hour",    importance: 82, color: "#8b5cf6" },
  { name: "Congestion norm", importance: 76, color: "#f59e0b" },
  { name: "Day of week",     importance: 61, color: "#10b981" },
  { name: "Is weekend",      importance: 45, color: "#06b6d4" },
  { name: "Time of day enc", importance: 38, color: "#ec4899" },
];

export default function ModelInfoPanel() {
  return (
    <div className="model-info-card">
      <div className="model-info-header">
        <span className="model-info-title">Model Info</span>
        <span className="model-info-badge">Random Forest · 100 trees · n_jobs=-1</span>
      </div>

      <div className="model-meta-row">
        <div className="model-meta-item">
          <span className="meta-label">Dataset</span>
          <span className="meta-val">8,936 Bangalore records</span>
        </div>
        <div className="model-meta-item">
          <span className="meta-label">Train/Test split</span>
          <span className="meta-val">80% / 20%</span>
        </div>
        <div className="model-meta-item">
          <span className="meta-label">Car MAE</span>
          <span className="meta-val">1.80 min</span>
        </div>
        <div className="model-meta-item">
          <span className="meta-label">Metro MAE</span>
          <span className="meta-val">1.34 min</span>
        </div>
        <div className="model-meta-item">
          <span className="meta-label">Bus MAE</span>
          <span className="meta-val">2.03 min</span>
        </div>
        <div className="model-meta-item">
          <span className="meta-label">Algorithm</span>
          <span className="meta-val">Random Forest Regressor</span>
        </div>
      </div>

      {/* Feature importance */}
      <div className="feature-importance">
        <div className="fi-title">Key feature importance</div>
        {FEATURES.map(f => (
          <div className="fi-row" key={f.name}>
            <span className="fi-name">{f.name}</span>
            <div className="fi-track">
              <div className="fi-fill" style={{ width: `${f.importance}%`, background: f.color }} />
            </div>
            <span className="fi-val">{f.importance}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}
