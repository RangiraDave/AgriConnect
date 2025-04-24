// frontend/src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: '/api',              // thanks to "proxy": "http://localhost:8000"
  headers: { 'Content-Type': 'application/json' },
});

// Example endpoint wrappers:
export function fetchProducts() {
  return api.get('/products/');  // GET  /api/products/
}

export function createProduct(data, token) {
  return api.post('/products/', data, {
    headers: { Authorization: `Bearer ${token}` }
  });
}

// Export the instance for custom calls:
export default api;
