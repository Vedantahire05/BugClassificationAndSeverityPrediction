export default function ResultCard({ result }) {
  if (!result) return null;

  return (
    <div className="result">
      <h2>Prediction Result</h2>

      <p><b>Type:</b> {result.type.join(", ")}</p>

      <p>
        <b>Severity:</b>{" "}
        <span className={`sev-${result.severity.toLowerCase()}`}>
          {result.severity}
        </span>
      </p>

      <p><b>Score:</b> {result.severity_score}</p>

      {result.explanation && (
        <p>
          <b>Explanation:</b>{" "}
          {result.explanation.join(", ")}
        </p>
      )}
    </div>
  );
}