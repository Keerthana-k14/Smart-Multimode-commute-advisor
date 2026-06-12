import { useState } from "react";
import RouteForm from "./components/RouteForm";
import ResultDashboard from "./components/ResultDashboard";
import "./index.css";

export default function App() {
  const [result, setResult]   = useState(null);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState(null);

  const handleResult = (data, form) => {
    setResult(data);
    setFormData(form);
  };

  return (
    <div className="app">
      {/* Background grid */}
      <div className="bg-grid" />

      <header className="site-header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">⬡</span>
            <span className="logo-text">CommuteIQ</span>
          </div>
          <div className="header-meta">
            <span className="pill">Bangalore</span>
            <span className="pill pill-green">ML Live</span>
          </div>
        </div>
      </header>

      <main className="layout">
        {/* LEFT — input */}
        <aside className="panel-left">
          <div className="panel-label">01 — Route Input</div>
          <RouteForm
            onResult={handleResult}
            loading={loading}
            setLoading={setLoading}
          />


        </aside>

        {/* RIGHT — output */}
        <section className="panel-right">
          {!result && !loading && (
            <div className="empty-state">
              <div className="empty-icon">🗺</div>
              <p className="empty-title">Ready to analyse your commute</p>
              <p className="empty-sub">Fill in the route details and click Get Recommendation</p>
              <div className="feature-list">
                {[
                  ["⚡", "ML-based prediction", "Random Forest trained on real Bangalore data"],
                  ["🧠", "Explainable AI", "Clear reasons for every recommendation"],
                  ["📊", "Traffic patterns", "Peak-hour and congestion learning"],
                  ["👥", "User experience", "Crowdsourced delay feedback"],
                ].map(([icon, title, desc]) => (
                  <div className="feature-item" key={title}>
                    <span className="feature-icon">{icon}</span>
                    <div>
                      <div className="feature-title">{title}</div>
                      <div className="feature-desc">{desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {loading && (
            <div className="loading-state">
              <div className="loader-ring" />
              <p>Running ML prediction...</p>
              <span>Analysing traffic patterns</span>
            </div>
          )}

          {result && !loading && (
            <ResultDashboard result={result} formData={formData} />
          )}
        </section>
      </main>
    </div>
  );
}