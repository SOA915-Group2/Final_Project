import { useState, useEffect } from "react";

const API_BASE = "http://localhost:8001/api";

export default function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [userId, setUserId] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [status, setStatus] = useState({ msg: "", type: "neutral" });
  const [loading, setLoading] = useState(false);

  const setStatusMessage = (msg, type = "neutral") => {
    setStatus({ msg, type }); // type: "success", "error", "neutral"
  };

  // Check token on load
  useEffect(() => {
    if (token) {
      fetch(`${API_BASE}/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => res.ok ? res.json() : Promise.reject())
        .then((data) => {
          setUserId(data.user_id);
          setStatusMessage("âœ… Token valid", "success");
        })
        .catch(() => {
          handleLogout();
          setStatusMessage("âŒ Invalid token", "error");
        });
    }
  }, []);

  const handleRegister = async () => {
    if (!username || !password) {
      setStatusMessage("âŒ Username and password required", "error");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const result = await res.json();
      if (res.ok) {
        setStatusMessage(`âœ… Registered! ID: ${result.user_id}`, "success");
      } else {
        setStatusMessage(`âŒ ${result.detail}`, "error");
      }
    } catch {
      setStatusMessage("âŒ Registration failed", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async () => {
    if (!username || !password) {
      setStatusMessage("âŒ Username and password required", "error");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username, password }),
      });
      const result = await res.json();
      if (res.ok) {
        localStorage.setItem("token", result.access_token);
        setToken(result.access_token);
        setUserId(result.user_id || "Logged in");
        setStatusMessage("âœ… Login successful", "success");
      } else {
        setStatusMessage(`âŒ ${result.detail}`, "error");
      }
    } catch {
      setStatusMessage("âŒ Login failed", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUserId(null);
    setStatusMessage("í ½íºª Logged out", "neutral");
  };

  const statusColor = {
    success: "text-green-600",
    error: "text-red-600",
    neutral: "text-gray-600",
  }[status.type];

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-md p-6 bg-white rounded shadow space-y-6">
        <h1 className="text-2xl font-bold text-center text-gray-800">Identity Service</h1>

        <input
          className="w-full border border-gray-300 rounded px-3 py-2"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={loading}
        />
        <input
          className="w-full border border-gray-300 rounded px-3 py-2"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
        />

        <div className="flex gap-2">
          <button
            onClick={handleRegister}
            className="w-1/2 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
            disabled={loading}
          >
            {loading ? "Registering..." : "Register"}
          </button>
          {!token ? (
            <button
              onClick={handleLogin}
              className="w-1/2 bg-green-600 text-white py-2 rounded hover:bg-green-700 disabled:opacity-50"
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          ) : (
            <button
              onClick={handleLogout}
              className="w-1/2 bg-red-500 text-white py-2 rounded hover:bg-red-600"
            >
              Logout
            </button>
          )}
        </div>

        {status.msg && (
          <div className={`text-sm mt-2 ${statusColor}`}>
            {status.msg}
          </div>
        )}

        {token && (
          <div className="text-xs text-gray-400 break-all mt-2">
            <strong>Token:</strong> {token}
          </div>
        )}
      </div>
    </div>
  );
}
