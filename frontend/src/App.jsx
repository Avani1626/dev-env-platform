import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

// -------------------------------
// Cognito Configuration
// -------------------------------
const COGNITO_DOMAIN =
  "https://devplatform123.auth.us-east-1.amazoncognito.com";

const CLIENT_ID = "3ag53fg3iotu032h6tohf5c5pt";
const REDIRECT_URI = "http://localhost:3000";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedScan, setSelectedScan] = useState(null);
  const [summary, setSummary] = useState(null);
  const [trends, setTrends] = useState(null);

  // ---------------------------------------
  // Format Timestamp for UI
  // ---------------------------------------
  const formatDate = (ts) => {
    if (!ts || ts.length !== 14) return ts;

    const year = ts.slice(0, 4);
    const month = ts.slice(4, 6);
    const day = ts.slice(6, 8);
    const hour = ts.slice(8, 10);
    const min = ts.slice(10, 12);
    const sec = ts.slice(12, 14);

    return `${day}/${month}/${year} ${hour}:${min}:${sec}`;
  };

  // ---------------------------------------
  // Fetch Dashboard Summary
  // ---------------------------------------
  const fetchSummary = async (token) => {
    try {
      const response = await fetch(
        "http://localhost:9100/metrics/summary",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();
      setSummary(data);
    } catch (err) {
      console.error("Summary fetch error:", err);
    }
  };

  // ---------------------------------------
  // Fetch Trends
  // ---------------------------------------
  const fetchTrends = async (token) => {
    try {
      const response = await fetch(
        "http://localhost:9100/metrics/trends",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();
      setTrends(data);
    } catch (err) {
      console.error("Trends fetch error:", err);
    }
  };

  // ---------------------------------------
  // Fetch Scan History
  // ---------------------------------------
  const fetchScans = async (token) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        "http://localhost:9100/scan/history",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();
      setScans(data);
    } catch (err) {
      console.error("Fetch error:", err);
      setError("Could not load scan history");
    } finally {
      setLoading(false);
    }
  };

  // ---------------------------------------
  // Exchange Code for Token
  // ---------------------------------------
  const exchangeCodeForToken = async (code) => {
    try {
      const codeVerifier = localStorage.getItem("code_verifier");

      const response = await fetch(`${COGNITO_DOMAIN}/oauth2/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          grant_type: "authorization_code",
          client_id: CLIENT_ID,
          code,
          redirect_uri: REDIRECT_URI,
          code_verifier: codeVerifier,
        }),
      });

      const data = await response.json();

      localStorage.setItem("access_token", data.access_token);
      window.history.replaceState({}, document.title, "/");

      setIsLoggedIn(true);
      fetchScans(data.access_token);
      fetchSummary(data.access_token);
      fetchTrends(data.access_token);
    } catch (err) {
      console.error("Token exchange error:", err);
    }
  };

  // ---------------------------------------
  // On Page Load
  // ---------------------------------------
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");

    if (code) {
      exchangeCodeForToken(code);
    } else {
      const token = localStorage.getItem("access_token");
      if (token) {
        setIsLoggedIn(true);
        fetchScans(token);
        fetchSummary(token);
        fetchTrends(token);
      }
    }
  }, []);

  // ---------------------------------------
  // Logout
  // ---------------------------------------
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("code_verifier");
    setIsLoggedIn(false);
    setScans([]);
    setSummary(null);
    setTrends(null);
  };

  const handleLogin = () => {
    const loginUrl =
      `${COGNITO_DOMAIN}/login?` +
      new URLSearchParams({
        response_type: "code",
        client_id: CLIENT_ID,
        redirect_uri: REDIRECT_URI,
        scope: "openid email",
      }).toString();

    window.location.href = loginUrl;
  };

  // ---------------------------------------
  // Transform trends for chart
  // ---------------------------------------
  const chartData =
    trends &&
    Object.keys(trends.daily_scans).map((date) => ({
      date,
      scans: trends.daily_scans[date] || 0,
      failures: trends.daily_failures[date] || 0,
    }));

  const MetricCard = ({ title, value }) => (
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
      <h4>{title}</h4>
      <p style={{ fontSize: "22px", fontWeight: "bold" }}>{value}</p>
    </div>
  );

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>Dev Environment Platform</h1>

      {!isLoggedIn && <button onClick={handleLogin}>Login</button>}

      {isLoggedIn && (
        <>
          <button onClick={handleLogout}>Logout</button>

          {/* Dashboard Cards */}
          {summary && (
            <div style={{ margin: "40px 0" }}>
              <h2>Dashboard</h2>
              <div style={{ display: "flex", gap: "20px" }}>
                <MetricCard title="Total Scans" value={summary.total_scans} />
                <MetricCard title="Processed" value={summary.processed} />
                <MetricCard title="Failed" value={summary.failed} />
                <MetricCard
                  title="Average Score"
                  value={summary.average_score}
                />
              </div>
            </div>
          )}

          {/* Charts */}
          {chartData && (
            <>
              <h2>Scan Trends</h2>
              <div style={{ width: "100%", height: 300 }}>
                <ResponsiveContainer>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="scans"
                      stroke="#8884d8"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <h2 style={{ marginTop: "40px" }}>Failure Trends</h2>
              <div style={{ width: "100%", height: 300 }}>
                <ResponsiveContainer>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="failures" fill="#ff4d4f" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </>
          )}

          {/* Scan History */}
          <h2 style={{ marginTop: "40px" }}>Your Scan History</h2>
          {loading && <p>Loading scans...</p>}
          {error && <p style={{ color: "red" }}>{error}</p>}

          {scans.map((scan) => (
            <div key={scan.scan_id} style={{ marginBottom: "20px" }}>
              <div>
                <strong>Date:</strong> {formatDate(scan.timestamp)}
              </div>
              <div>
                <strong>Status:</strong>{" "}
                <span
                  style={{
                    color:
                      scan.status === "COMPLETED" ? "green" : "red",
                  }}
                >
                  {scan.status}
                </span>
              </div>
              <div>
                <strong>OS:</strong> {scan.os}
              </div>
            </div>
          ))}
        </>
      )}
    </div>
  );
}

export default App;