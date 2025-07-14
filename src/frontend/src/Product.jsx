import { useEffect, useState } from "react";

// const API_BASE = import.meta.env.API_BASE_PRODUCT;
const API_BASE = window.location.origin.replace("5173", "8002") + "/api";

import { Link } from "react-router-dom"; // Make sure this is at the top

const token = localStorage.getItem("token");
const isLoggedIn = !!token;

const Nav = () => (
  <nav className="flex justify-between items-center mb-6 text-sm">
    <Link to="/login" className="text-blue-600 hover:underline">
      Login
    </Link>
    <Link to="/products" className="text-blue-600 hover:underline">
      Products
    </Link>
  </nav>
);

export default function ProductPage() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ name: "", price: "", description: "" });

  const fetchProducts = async () => {
    const res = await fetch(`${API_BASE}/products`);
    const data = await res.json();
    setProducts(data);
  };

  const handleInput = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const token = localStorage.getItem("token");

  const submit = async () => {
    const res = await fetch(`${API_BASE}/products`, {
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
    const res = await fetch(`${API_BASE}/products/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) fetchProducts();
  };

  const update = async (id) => {
    const updated = prompt("Enter new name:");
    if (!updated) return;
    const res = await fetch(`${API_BASE}/products/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ ...form, name: updated }),
    });
    if (res.ok) fetchProducts();
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 bg-white shadow rounded space-y-6">
      <Nav />
      <h2 className="text-xl font-bold text-gray-800">í ½í»’ Products</h2>

      {products.map((p) => (
        <div key={p.id} className="border p-3 rounded shadow-sm bg-gray-50 space-y-1">
          <div className="font-semibold">{p.name}</div>
          <div>${p.price}</div>
          <div className="text-sm text-gray-500">{p.description}</div>
          <div className="text-xs text-gray-400">Owner: {p.owner_id}</div>
	{isLoggedIn && (
          <div className="flex gap-2 mt-2">
            <button onClick={() => update(p.id)} className="text-blue-600 text-sm">Edit</button>
            <button onClick={() => remove(p.id)} className="text-red-500 text-sm">Delete</button>
          </div>
        )}
        </div>
      ))}

  {isLoggedIn && (
    <>
      <h3 className="text-lg font-semibold">âž• Add Product</h3>
      <input
        className="w-full border rounded px-3 py-2 mb-2"
        name="name"
        placeholder="Name"
        value={form.name}
        onChange={handleInput}
      />
      <input
        className="w-full border rounded px-3 py-2 mb-2"
        name="price"
        placeholder="Price"
        type="number"
        value={form.price}
        onChange={handleInput}
      />
      <input
        className="w-full border rounded px-3 py-2 mb-4"
        name="description"
        placeholder="Description"
        value={form.description}
        onChange={handleInput}
      />
      <button
        onClick={submit}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
      >
        Add Product
      </button>
    </>
  )}
    </div>
  );
}
