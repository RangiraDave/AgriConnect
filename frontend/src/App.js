import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';
import ProductListings from './components/ProductListings';
import MarketInsights from './components/MarketInsights';
import VerifyEmail from './components/VerifyEmail';

function App() {
  // Example props for demonstration
  const products = []; // Replace with actual product data
  const userCount = 100; // Replace with actual user count
  const totalProducts = 50; // Replace with actual total products
  const welcomeMessage = 'Welcome to AgriConnect!';
  const topProducts = []; // Replace with actual top products
  const topFarmers = []; // Replace with actual top farmers
  const verificationEmail = 'user@example.com'; // Replace with actual email

  return (
    <Router>
      <Navbar />
      <div className="App">
        <Routes>
          {/* Route for Product Listings */}
          <Route
            path="/products"
            element={
              <ProductListings
                products={products}
                userCount={userCount}
                totalProducts={totalProducts}
                welcomeMessage={welcomeMessage}
              />
            }
          />

          {/* Route for Market Insights */}
          <Route
            path="/market-insights"
            element={
              <MarketInsights
                totalProducts={totalProducts}
                activeFarmers={10}
                avgRating={4.5}
                topProducts={topProducts}
                topFarmers={topFarmers}
              />
            }
          />

          {/* Route for Verify Email */}
          <Route
            path="/verify-email"
            element={<VerifyEmail verificationEmail={verificationEmail} />}
          />

          {/* Default Route (Homepage or Redirect) */}
          <Route
            path="/"
            element={
              <div className="container mt-4">
                <h1>Welcome to AgriConnect</h1>
                <p>Select a page from the navigation menu.</p>
              </div>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
