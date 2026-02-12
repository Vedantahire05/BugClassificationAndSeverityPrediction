import React, { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_URL =
    "https://bug-classification-api.onrender.com/predict";

  const handlePredict = async () => {
    if (!text) return;

    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("API Error");
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: 40, fontFamily: "Arial" }}>
      <h1>🐞 Bug Classification Dashboard</h1>

      <textarea
        rows="6"
        style={{ width: "100%", padding: 10 }}
        placeholder="Enter bug description..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        onClick={handlePredict}
        style={{
          marginTop: 10,
          padding: "10px 20px",
          cursor: "pointer"
        }}
      >
        {loading ? "Predicting..." : "Predict"}
      </button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Prediction Result</h3>
          <p>
            <b>Type:</b> {result.type.join(", ")}
          </p>
          <p>
            <b>Severity:</b> {result.severity}
          </p>
          <p>
            <b>Severity Score:</b> {result.severity_score}
          </p>
          <p>
            <b>Explanation:</b>{" "}
            {result.explanation?.join(", ")}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;