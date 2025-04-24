import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import BaseLayout from './components/BaseLayout';
import ProductListings from './components/ProductListings';
import MarketInsights from './components/MarketInsights';
import VerifyEmail from './components/VerifyEmail';

function App() {
  const [token] = useState(null); // Removed setToken since it's unused
  const user = {
    isAuthenticated: true, // Replace with actual authentication logic
    profile: { role: 'umuhinzi' }, // Replace with actual user profile data
  };

  return (
    <Router>
      <BaseLayout user={user}>
        <Routes>
          <Route path="/products" element={<ProductListings token={token} />} />
          <Route path="/market-insights" element={<MarketInsights />} />
          <Route path="/verify-email" element={<VerifyEmail />} />
          <Route
            path="/"
            element={
              <div className="home-page">
                <div className="jumbotron text-center">
                  <h1>Welcome to AgriConnect</h1>
                  <p>Your one-stop platform for connecting farmers and buyers.</p>
                  <div className="btn-group mt-4">
                    <a href="/products" className="btn btn-primary">
                      Explore Products
                    </a>
                    <a href="/signup" className="btn btn-success">
                      Join Us
                    </a>
                  </div>
                </div>
              </div>
            }
          />
        </Routes>
      </BaseLayout>
    </Router>
  );
}

export default App;
