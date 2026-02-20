import { useEffect, useState } from "react";

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
  // Fetch Full Scan Details
  // ---------------------------------------
  const fetchFullScan = async (scanId) => {
    const token = localStorage.getItem("access_token");

    try {
      const response = await fetch(
        `http://localhost:9100/scan/${scanId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch full scan");
      }

      const data = await response.json();
      setSelectedScan(data);
    } catch (err) {
      console.error("Full scan fetch error:", err);
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
      }
    }
  }, []);

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
          code: code,
          redirect_uri: REDIRECT_URI,
          code_verifier: codeVerifier,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error("Token exchange failed");
      }

      localStorage.setItem("access_token", data.access_token);
      window.history.replaceState({}, document.title, "/");

      setIsLoggedIn(true);
      fetchScans(data.access_token);
    } catch (err) {
      console.error("Token exchange error:", err);
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

      if (!response.ok) {
        throw new Error("Failed to fetch scans");
      }

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
  // Logout
  // ---------------------------------------
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("code_verifier");
    setIsLoggedIn(false);
    setScans([]);
    setSelectedScan(null);
  };

  // ---------------------------------------
  // Login Redirect
  // ---------------------------------------
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
  // Render Sections
  // ---------------------------------------

  const sectionStyle = {
    background: "#f5f5f5",
    padding: "15px",
    marginBottom: "20px",
    borderRadius: "8px",
  };

  const tableStyle = {
    width: "100%",
    borderCollapse: "collapse",
  };

  const renderSystem = () => {
    if (!selectedScan?.system) return null;
    const sys = selectedScan.system;

    return (
      <div style={sectionStyle}>
        <h3>🖥 System Information</h3>
        <p><strong>OS:</strong> {sys.os}</p>
        <p><strong>Release:</strong> {sys.os_release}</p>
        <p><strong>Architecture:</strong> {sys.architecture}</p>
        <p><strong>Processor:</strong> {sys.processor}</p>
        <p><strong>Hostname:</strong> {sys.hostname}</p>
        <p><strong>Python Version:</strong> {sys.python_version}</p>
      </div>
    );
  };

  const renderPython = () => {
    if (!selectedScan?.python) return null;
    const py = selectedScan.python;

    return (
      <div style={sectionStyle}>
        <h3>🐍 Python</h3>
        <p><strong>Python Version:</strong> {py.python_version}</p>

        {py.packages?.length > 0 && (
          <table style={tableStyle}>
            <thead>
              <tr>
                <th>Package</th>
                <th>Version</th>
              </tr>
            </thead>
            <tbody>
              {py.packages.map((pkg, index) => (
                <tr key={index}>
                  <td>{pkg.name}</td>
                  <td>{pkg.version}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    );
  };

  const renderNode = () => {
    if (!selectedScan?.node) return null;
    const node = selectedScan.node;

    return (
      <div style={sectionStyle}>
        <h3>🟢 Node</h3>
        <p><strong>Node Version:</strong> {node.node_version || "Not Installed"}</p>
        <p><strong>NPM Version:</strong> {node.npm_version || "Not Installed"}</p>
      </div>
    );
  };

  const renderDocker = () => {
    if (!selectedScan?.docker) return null;
    const docker = selectedScan.docker;

    return (
      <div style={sectionStyle}>
        <h3>🐳 Docker</h3>
        <p><strong>Installed:</strong> {docker.installed ? "Yes" : "No"}</p>
        <p><strong>Version:</strong> {docker.version || "N/A"}</p>

        {docker.images?.length > 0 && (
          <ul>
            {docker.images.map((img, index) => (
              <li key={index}>{img}</li>
            ))}
          </ul>
        )}
      </div>
    );
  };

  const renderCLI = () => {
    if (!selectedScan?.cli_tools) return null;

    return (
      <div style={sectionStyle}>
        <h3>🔧 CLI Tools</h3>
        {Object.entries(selectedScan.cli_tools).map(([tool, data]) => (
          <p key={tool}>
            <strong>{tool}:</strong>{" "}
            {data.installed
              ? `Installed (${data.version})`
              : "Not Installed"}
          </p>
        ))}
      </div>
    );
  };

  // ---------------------------------------
  // UI
  // ---------------------------------------
  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>Dev Environment Platform</h1>

      {!isLoggedIn && (
        <button onClick={handleLogin}>Login</button>
      )}

      {isLoggedIn && (
        <>
          <button onClick={handleLogout} style={{ marginBottom: "20px" }}>
            Logout
          </button>

          <h2>Your Scan History</h2>

          {loading && <p>Loading scans...</p>}
          {error && <p style={{ color: "red" }}>{error}</p>}

          {!loading && scans.length === 0 && (
            <p>No scans found.</p>
          )}

          {!loading && scans.length > 0 && (
            <ul>
              {scans.map((scan) => (
                <li key={scan.scan_id} style={{ marginBottom: "20px" }}>
                  <div>
                    <strong>Date:</strong>{" "}
                    {formatDate(scan.timestamp)}
                  </div>
                  <div>
                    <strong>Status:</strong>{" "}
                    <span
                      style={{
                        color:
                          scan.status === "PASS"
                            ? "green"
                            : "red",
                      }}
                    >
                      {scan.status}
                    </span>
                  </div>
                  <div>
                    <strong>OS:</strong> {scan.os}
                  </div>

                  <button
                    onClick={() => fetchFullScan(scan.scan_id)}
                    style={{ marginTop: "8px" }}
                  >
                    View Details
                  </button>
                </li>
              ))}
            </ul>
          )}

          {selectedScan && (
            <div style={{ marginTop: "40px" }}>
              <h3>Full Scan Details</h3>
              {renderSystem()}
              {renderPython()}
              {renderNode()}
              {renderDocker()}
              {renderCLI()}
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default App;
