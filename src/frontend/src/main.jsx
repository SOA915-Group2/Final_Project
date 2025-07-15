// src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import App from './App.jsx'; // Login
import ProductPage from './Product.jsx';
import EditProductPage from "./EditProductPage.jsx";
import Orders from "./Orders";
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProductPage />} />         {/* ✅ default */}
        <Route path="/login" element={<App />} />
        <Route path="/products" element={<ProductPage />} />
	<Route path="/edit-products" element={<EditProductPage />} />
	<Route path="/orders" element={<Orders />} />
        <Route path="*" element={<Navigate to="/" />} />      {/* fallback */}
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
