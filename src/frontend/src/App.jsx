import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from 'react-router-dom';
import Nav from "./Nav";


// const API_BASE = import.meta.env.VITE_API_BASE;
//const API_BASE = "http://localhost:8001/api";
const API_BASE = window.location.origin.replace("5173", "8001") + "/api";

export default function App() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [status, setStatus] = useState({ msg: "", type: "neutral" });

  const setStatusMessage = (msg, type = "neutral") => {
    setStatus({ msg, type });
  };

  const handleRegister = async () => {
    if (!username || !password) {
      setStatusMessage("Username and password required", "error");
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
	body: JSON.stringify({
            username: username,   // must match FastAPI model
            password: password,   // must match FastAPI model
        }),
      });
      const result = await res.json();
      if (res.ok) {
        setStatusMessage("✅ Registered successfully", "success");
      } else {
        setStatusMessage(`❌ ${result.detail}`, "error");
      }
    } catch {
      setStatusMessage("❌ Registration failed", "error");
    }
  };

  const handleLogin = async () => {
    if (!username || !password) {
      setStatusMessage("Username and password required", "error");
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const result = await res.json();
      if (res.ok) {
        localStorage.setItem("token", result.access_token);
        setToken(result.access_token);
        setStatusMessage("✅ Login successful", "success");
	navigate("/products");
      } else {
        setStatusMessage(`❌ ${result.detail}`, "error");
      }
    } catch {
      setStatusMessage("❌ Login failed", "error");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setStatusMessage("Logged out", "neutral");
  };

  const statusColor = {
    success: "text-green-600",
    error: "text-red-600",
    neutral: "text-gray-500",
  }[status.type];

  return (
    <div className="min-h-screen bg-gray-100">
    <Nav />  {/* ✅ add nav bar back */}
    <div className="flex justify-center items-center min-h-[80vh]">
      <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
        <h1 className="text-3xl font-bold text-center text-gray-800">SOA Final Project</h1>
        <h2 className="text-lg text-center text-gray-600">User Login</h2>

        <input
          className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring focus:border-blue-500"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring focus:border-blue-500"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <div className="flex gap-3">
          <button
            className="w-1/2 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded"
            onClick={handleRegister}
          >
            Register
          </button>
          {!token ? (
            <button
              className="w-1/2 bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded"
              onClick={handleLogin}
            >
              Login
            </button>
          ) : (
            <button
              className="w-1/2 bg-red-500 hover:bg-red-600 text-white font-semibold py-2 rounded"
              onClick={handleLogout}
            >
              Logout
            </button>
          )}
        </div>

        {status.msg && (
          <div className={`text-center text-sm font-medium ${statusColor}`}>
            {status.msg}
          </div>
        )}
      </div>
    </div>
    </div>
  );
}
