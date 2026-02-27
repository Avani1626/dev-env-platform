import React, { useEffect, useState } from "react";

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:9100/metrics/summary")
      .then((res) => res.json())
      .then((data) => {
        setSummary(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching summary:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading dashboard...</div>;
  if (!summary) return <div>No data available</div>;

  return (
    <div style={{ padding: "40px" }}>
      <h1>Dev Environment Dashboard</h1>

      <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
        <Card title="Total Scans" value={summary.total_scans} />
        <Card title="Processed" value={summary.processed} />
        <Card title="Failed" value={summary.failed} />
        <Card title="Average Score" value={summary.average_score} />
      </div>
    </div>
  );
};

const Card = ({ title, value }) => {
  return (
    <div
      style={{
        background: "#f4f4f4",
        padding: "20px",
        borderRadius: "10px",
        width: "200px",
        textAlign: "center",
        boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
      }}
    >
      <h3>{title}</h3>
      <p style={{ fontSize: "24px", fontWeight: "bold" }}>{value}</p>
    </div>
  );
};

export default Dashboard;