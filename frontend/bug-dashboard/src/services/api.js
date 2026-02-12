const API = "https://bug-classification-api.onrender.com";

export const analyzeBug = async (text) => {
  const res = await fetch(`${API}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  return res.json();
};

export const fetchHistory = async () => {
  const res = await fetch(`${API}/bugs`);
  return res.json();
};