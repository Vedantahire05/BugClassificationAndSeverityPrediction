import React from "react";

function AnalyticsPanel({ history }) {
  if (!history || history.length === 0) {
    return (
      <div className="analytics">
        <h2>📊 Analytics</h2>
        <p>No data yet.</p>
      </div>
    );
  }

  // ---- COUNT SEVERITIES ----
  const severityCount = {};
  const typeCount = {};

  history.forEach((bug) => {
    // severity stats
    const sev = bug.severity || "Unknown";
    severityCount[sev] = (severityCount[sev] || 0) + 1;

    // type stats
    if (bug.type) {
      bug.type.forEach((t) => {
        typeCount[t] = (typeCount[t] || 0) + 1;
      });
    }
  });

  const total = history.length;

  return (
    <div className="analytics">
      <h2>📊 Analytics Overview</h2>

      <div className="analytics-grid">
        <div className="analytics-card">
          <h3>Total Bugs</h3>
          <p>{total}</p>
        </div>

        <div className="analytics-card">
          <h3>Severity Distribution</h3>
          {Object.entries(severityCount).map(([k, v]) => (
            <p key={k}>
              {k}: {v}
            </p>
          ))}
        </div>

        <div className="analytics-card">
          <h3>Type Distribution</h3>
          {Object.entries(typeCount).map(([k, v]) => (
            <p key={k}>
              {k}: {v}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}

export default AnalyticsPanel;