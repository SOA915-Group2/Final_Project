import { useEffect, useState } from "react";
import Nav from "./Nav";

// const API_BASE = import.meta.env.API_BASE_PRODUCT;
const API_BASE = window.location + "/api/products";
const ORDER_API = window.location + "/api/orders";

import { Link } from "react-router-dom"; // Make sure this is at the top

const token = localStorage.getItem("token");
const isLoggedIn = !!token;

export default function ProductPage() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ name: "", price: "", description: "" });

  const fetchProducts = async () => {
    const res = await fetch(`${API_BASE}`);
    const data = await res.json();
    setProducts(data);
  };

  const handleInput = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const token = localStorage.getItem("token");

  const submit = async () => {
    const res = await fetch(`${API_BASE}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(form),
    });

    if (res.ok) {
      setForm({ name: "", price: "", description: "" });
      fetchProducts();
    } else {
      alert("Unauthorized or error");
    }
  };

  const remove = async (id) => {
    const res = await fetch(`${API_BASE}/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) fetchProducts();
  };

  const update = async (id) => {
    const updated = prompt("Enter new name:");
    if (!updated) return;
    const res = await fetch(`${API_BASE}/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ ...form, name: updated }),
    });
    if (res.ok) fetchProducts();
  };

  const placeOrder = async (productId) => {
    const token = localStorage.getItem("token");
    if (!token) return alert("You must be logged in to place an order.");
    const res = await fetch(`${ORDER_API}/orders`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        product_id: String(productId),
        quantity: 1,
      }),
    });

    try {
      const result = await res.json();
      if (res.ok) {
        alert("✅ Order placed!");
      } else {
        alert("❌ Order failed: " + (result.detail || JSON.stringify(result)));
      }
    } catch {
      alert("❌ Order failed: Invalid JSON response");
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      <Nav />

      <div className="max-w-3xl mx-auto px-4 py-6 space-y-6">
        <h2 className="text-2xl font-bold text-gray-800">Available Products</h2>

        {products.length === 0 ? (
          <p className="text-gray-600">No products available.</p>
        ) : (
	    <ul className="space-y-3">
              {products.map((p) => (
                <li
                  key={p.id}
                  className="bg-white p-4 rounded shadow flex items-center justify-between"
                >
                  {/* Left: Product details */}
                  <div>
                    <div className="font-bold text-lg">{p.name}</div>
                    <div className="text-sm text-gray-500">${p.price}</div>
                    <div className="text-sm text-gray-400">{p.description}</div>
                    <div className="text-xs text-gray-400 mt-1">
                      Owner: {p.owner_id}
                 </div>
               </div>

               {/* Right: Order button */}
               <div className="flex items-center h-full">
                 <button
                   onClick={() => placeOrder(p.id)}
                   className="text-green-600 hover:underline"
                 >
                   Add To Cart
                 </button>
               </div>
               </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
