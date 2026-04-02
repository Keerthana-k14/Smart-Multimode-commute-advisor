// FeedbackForm.jsx
import { useState } from "react";
import { postFeedback } from "../api/client";

export default function FeedbackForm({ result }) {
  const [time, setTime]   = useState("");
  const [level, setLevel] = useState("medium");
  const [sent, setSent]   = useState(false);
  const [err, setErr]     = useState("");

  const submit = async () => {
    if (!time) { setErr("Please enter your actual travel time."); return; }
    try {
      await postFeedback({
        area:          result.area,
        road:          result.road,
        mode:          result.recommended_mode,
        actual_time:   parseFloat(time),
        traffic_level: level,
      });
      setSent(true);
    } catch {
      setErr("Could not submit feedback. Check backend.");
    }
  };

  return (
    <div className="feedback-card">
      <div className="feedback-header">
        <span>📝</span>
        <span>Submit your commute experience</span>
      </div>
      {sent ? (
        <div className="feedback-success">
          ✅ Thank you! Your feedback improves future predictions.
        </div>
      ) : (
        <div className="feedback-body">
          <div className="feedback-row">
            <div className="feedback-field">
              <label>Actual travel time (min)</label>
              <input
                type="number"
                placeholder="e.g. 38"
                value={time}
                onChange={e => setTime(e.target.value)}
                className="feedback-input"
              />
            </div>
            <div className="feedback-field">
              <label>Traffic level experienced</label>
              <select
                value={level}
                onChange={e => setLevel(e.target.value)}
                className="feedback-select"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <button className="feedback-submit-btn" onClick={submit}>Submit</button>
          </div>
          {err && <p className="feedback-err">{err}</p>}
        </div>
      )}
    </div>
  );
}
