import { useState, useEffect } from "react";
import Nav from "./Nav.jsx";

const API_BASE = window.location.origin.replace("5173", "8002") + "/api";

export default function EditProductPage() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ name: "", price: "", description: "", id: null });
  const token = localStorage.getItem("token");

  const fetchProducts = async () => {
    const res = await fetch(`${API_BASE}/products`);
    const data = await res.json();
    setProducts(data);
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const saveProduct = async () => {
    const method = form.id ? "PUT" : "POST";
    const url = form.id
      ? `${API_BASE}/products/${form.id}`
      : `${API_BASE}/products`;

    await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(form),
    });

    setForm({ name: "", price: "", description: "", id: null });
    fetchProducts();
  };

  const deleteProduct = async (id) => {
    await fetch(`${API_BASE}/products/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchProducts();
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Nav />
      <div className="max-w-3xl mx-auto px-4 py-6">
        <h2 className="text-2xl font-bold mb-4">Edit Products</h2>

        <div className="bg-white p-4 rounded shadow space-y-4 mb-8">
          <input
            type="text"
            placeholder="Product Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="w-full border px-3 py-2 rounded"
          />
          <input
            type="number"
            placeholder="Price"
            value={form.price}
            onChange={(e) => setForm({ ...form, price: e.target.value })}
            className="w-full border px-3 py-2 rounded"
          />
          <input
            type="text"
            placeholder="Description"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            className="w-full border px-3 py-2 rounded"
          />

          <button
            onClick={saveProduct}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            {form.id ? "Update" : "Add"} Product
          </button>
        </div>

        <ul className="space-y-3">
          {products.map((p) => (
            <li key={p.id} className="bg-white p-4 rounded shadow flex justify-between items-center">
              <div>
                <div className="font-bold">{p.name}</div>
                <div className="text-sm text-gray-500">${p.price}</div>
                <div className="text-sm text-gray-400">{p.description}</div>
              </div>
              <div className="space-x-2">
                <button
                  onClick={() => setForm(p)}
                  className="text-blue-600 hover:underline"
                >
                  Edit
                </button>
                <button
                  onClick={() => deleteProduct(p.id)}
                  className="text-red-600 hover:underline"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
