// src/Orders.jsx
import { useEffect, useState } from "react";
import jwtDecode from "jwt-decode";
import Nav from "./Nav";

const ORDER_API = window.location + "/api/orders";

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState("");

  const token = localStorage.getItem("token");

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await fetch(`${ORDER_API}/orders`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!res.ok) throw new Error("Failed to fetch orders");
        const data = await res.json();
        setOrders(data);
      } catch (err) {
        setError(err.message);
      }
    };

    if (token) fetchOrders();
  }, [token]);

  if (!token) return <div className="p-6 text-red-500">You must log in to view orders.</div>;

  return (
    <div className="min-h-screen bg-gray-100">
      <Nav />
      <div className="max-w-3xl mx-auto px-4 py-6 space-y-6">
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">My Orders</h2>
      {error && <p className="text-red-500">{error}</p>}
      {orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        <ul className="space-y-4">
	    {orders.map((order) => (
                <div key={order._id} className="p-4 bg-white rounded shadow mb-2">
                  <p><strong>Product:</strong> {order.product_id}</p>
                  <p><strong>Quantity:</strong> {order.quantity}</p>
                  <p><strong>Last Ordered:</strong> {order.last_ordered}</p>
                </div>
            ))}
        </ul>
      )}
    </div>
    </div>
  </div>
  );
}
