import React from "react";

export default function BugInput({ text, setText, onAnalyze, loading }) {
  return (
    <>
      <textarea
        placeholder="Describe the bug..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={onAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Bug"}
      </button>
    </>
  );
}