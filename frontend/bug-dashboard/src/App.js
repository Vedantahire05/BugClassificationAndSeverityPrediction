import React, { useState, useEffect } from "react";
import "./App.css";

import BugInput from "./components/BugInput";
import ResultCard from "./components/ResultCard";
import HistoryPanel from "./components/HistoryPanel";
import Loader from "./components/Loader";
import AnalyticsPanel from "./components/AnalyticsPanel";

import { analyzeBug, fetchHistory } from "./services/api";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  // ---------- LOAD HISTORY ----------
  const loadHistory = async () => {
    try {
      const data = await fetchHistory();

      const bugs = Array.isArray(data)
        ? data
        : data?.bugs || [];

      // avoid mutating original array
      setHistory([...bugs].reverse());
    } catch (err) {
      console.error("Failed to load history:", err);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  // ---------- ANALYZE ----------
  const handleAnalyze = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const data = await analyzeBug(text);
      setResult(data);
      await loadHistory();
    } catch (err) {
      alert("API Error");
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <h1>🐞 Bug Intelligence Dashboard</h1>

      <div className="dashboard">

        {/* LEFT PANEL */}
        <div className="left-panel">
          <HistoryPanel history={history} />
          <AnalyticsPanel history={history} />
        </div>

        {/* RIGHT PANEL */}
        <div className="right-panel">
          <BugInput
            text={text}
            setText={setText}
            onAnalyze={handleAnalyze}
            loading={loading}
          />

          {loading && <Loader />}

          <ResultCard result={result} />
        </div>

      </div>
    </div>
  );
}

export default App;