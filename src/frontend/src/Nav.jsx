// src/Nav.jsx
import { Link, useLocation, useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { useEffect, useState } from "react";

export default function Nav() {
  const [username, setUsername] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const decoded = jwtDecode(token);
        const user = { ...decoded }; // ✅ clone before using
        setUsername(user.username || user.sub);
        setIsLoggedIn(true);
      } catch (err) {
        console.warn("Invalid token:", err);
        setUsername("");
        setIsLoggedIn(false);
      }
    } else {
      setUsername("");
      setIsLoggedIn(false);
    }
  }, [location]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav className="bg-white shadow px-4 py-3 flex justify-between items-center">
      <div className="text-lg font-semibold">SOA Group2's Store</div>
      <div className="flex gap-4 items-center text-sm">
        <Link
          to="/products"
          className={location.pathname === "/products" ? "font-bold text-blue-600" : ""}
        >
          Products
        </Link>
        {isLoggedIn && (
          <Link
            to="/orders"
            className={location.pathname === "/orders" ? "font-bold text-blue-600" : ""}
          >
            Orders
          </Link>
        )}
	{isLoggedIn && (
          <Link
            to="/edit-products"
            className={location.pathname === "/edit-products" ? "font-bold text-blue-600" : ""}
          >
            Edit Products
          </Link>
        )}
        {!isLoggedIn && (
          <Link
            to="/login"
            className={location.pathname === "/login" ? "font-bold text-blue-600" : ""}
          >
            Login
          </Link>
        )}
        {isLoggedIn && (
          <>
            <span className="text-gray-700">Welcome, {username}</span>
            <button onClick={handleLogout} className="text-red-500">Logout</button>
          </>
        )}
      </div>
    </nav>
  );
}
