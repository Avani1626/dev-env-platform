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

  // ---------------------------------------------------
  // 1️⃣ On Page Load: Check for auth code or token
  // ---------------------------------------------------
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

  // ---------------------------------------------------
  // 2️⃣ Exchange Authorization Code for Access Token
  // ---------------------------------------------------
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

  // ---------------------------------------------------
  // 3️⃣ Fetch Scan History From Backend
  // ---------------------------------------------------
  const fetchScans = async (token) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        "http://localhost:8000/scan/history",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch scans");
      }

      const data = await response.json();
      console.log("SCAN DATA:", data);

      setScans(data);
    } catch (err) {
      console.error("Fetch error:", err);
      setError("Could not load scan history");
    } finally {
      setLoading(false);
    }
  };

  // ---------------------------------------------------
  // 4️⃣ Logout
  // ---------------------------------------------------
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("code_verifier");
    setIsLoggedIn(false);
    setScans([]);
  };

  // ---------------------------------------------------
  // 5️⃣ Login Redirect
  // ---------------------------------------------------
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

  // ---------------------------------------------------
  // 6️⃣ UI
  // ---------------------------------------------------
    return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>Dev Environment Platform</h1>

      {!isLoggedIn && (
        <button onClick={handleLogin}>Login</button>
      )}

      {isLoggedIn && (
        <>
          <button
            onClick={handleLogout}
            style={{ marginBottom: "20px" }}
          >
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
                <li key={scan.scan_id} style={{ marginBottom: "15px" }}>
                  <div>
                    <strong>Date:</strong> {scan.timestamp}
                  </div>
                  <div>
                    <strong>Status:</strong>{" "}
                    <span
                      style={{
                        color:
                          scan.status === "PASS" ? "green" : "red",
                      }}
                    >
                      {scan.status}
                    </span>
                  </div>
                  <div>
                    <strong>OS:</strong> {scan.os}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </div>
  );
  }

export default App;

