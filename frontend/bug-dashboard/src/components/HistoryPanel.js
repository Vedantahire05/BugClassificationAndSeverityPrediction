export default function HistoryPanel({ history }) {
  return (
    <div className="history">
      <h2>Recent Bugs</h2>

      {history.map((bug, i) => (
        <div key={i} className="history-card">
          <p className="bug-text">{bug.text}</p>
          <p className={`sev-${bug.severity.toLowerCase()}`}>
            {bug.severity}
          </p>
        </div>
      ))}
    </div>
  );
}