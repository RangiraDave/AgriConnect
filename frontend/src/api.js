import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api'; // Update with your backend URL

// Create an Axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add Authorization header for protected calls
const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

// API methods
const signup = (data) => api.post('/auth/signup/', data);

const login = (data) => api.post('/auth/login/', data);

const getProducts = () => api.get('/products/');

const createProduct = (data, token) => {
  setAuthToken(token);
  return api.post('/products/', data);
};

const rateProduct = (id, rating, token) => {
  setAuthToken(token);
  return api.post(`/products/${id}/rate/`, { rating });
};

const getMarketInsights = () => api.get('/market-insights/');

export { signup, login, getProducts, createProduct, rateProduct, getMarketInsights, setAuthToken };
