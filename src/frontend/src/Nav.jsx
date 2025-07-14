// src/Nav.jsx
import { Link, useLocation, useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

export default function Nav() {
  const location = useLocation();
  const navigate = useNavigate();

  const token = localStorage.getItem("token");
  let username = null;

  if (token) {
    try {
      const decoded = jwtDecode(token); // Access .default if using import *
      username = decoded.username || decoded.sub || "User";
    } catch (err) {
      console.warn("Invalid token:", err);
      username = null;
    }
  }

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const NavLink = ({ to, label }) => (
    <Link
      to={to}
      className={`${
        location.pathname === to ? "text-blue-700 font-bold underline" : "text-blue-600"
      } hover:underline`}
    >
      {label}
    </Link>
  );

  return (
    <nav className="bg-white shadow-md px-6 py-4 flex justify-between items-center">
      <div className="text-xl font-semibold text-gray-800">SOA Group2's Store</div>

      <div className="flex items-center gap-6 text-sm">
	{!token && (
        <NavLink to="/login" label="Login" />
	)}
        <NavLink to="/products" label="Products" />
	{token && (
	<NavLink to="/edit-products" label="Edit Products" />
	)}
        {username && (
          <>
            <span className="text-gray-700">Welcome, {username}</span>
            <button
              onClick={handleLogout}
              className="text-red-600 hover:underline"
            >
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  );
}
