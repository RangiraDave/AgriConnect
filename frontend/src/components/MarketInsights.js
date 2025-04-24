import React, { useEffect, useState } from 'react';
import '../css/style.css';
import Chart from 'chart.js/auto';
import { getMarketInsights } from '../api';

const MarketInsights = () => {
  const [totalProducts, setTotalProducts] = useState(0);
  const [activeFarmers, setActiveFarmers] = useState(0);
  const [avgRating, setAvgRating] = useState(0); // Default to 0
  const [topProducts, setTopProducts] = useState([]);
  const [topFarmers, setTopFarmers] = useState([]);

  useEffect(() => {
    // Fetch market insights from the API
    getMarketInsights()
      .then((response) => {
        setTotalProducts(response.data.total_products || 0); // Fallback to 0
        setActiveFarmers(response.data.active_farmers || 0); // Fallback to 0
        setAvgRating(response.data.avg_rating || 0); // Fallback to 0
        setTopProducts(response.data.top_products || []); // Fallback to empty array
        setTopFarmers(response.data.top_farmers || []); // Fallback to empty array
      })
      .catch((error) => {
        console.error('Error fetching market insights:', error);
      });
  }, []);

  useEffect(() => {
    let productsChart = null;
    let farmersChart = null;

    if (topProducts.length > 0) {
      const productsCanvas = document.getElementById('productsChart');
      if (productsCanvas) {
        productsChart = new Chart(productsCanvas, {
          type: 'bar',
          data: {
            labels: topProducts.map((product) => product.name),
            datasets: [
              {
                label: 'Average Rating',
                data: topProducts.map((product) => product.avg_rating),
                backgroundColor: '#28a745',
              },
            ],
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                max: 5,
              },
            },
          },
        });
      }
    }

    if (topFarmers.length > 0) {
      const farmersCanvas = document.getElementById('farmersChart');
      if (farmersCanvas) {
        farmersChart = new Chart(farmersCanvas, {
          type: 'bar',
          data: {
            labels: topFarmers.map((farmer) => farmer.username),
            datasets: [
              {
                label: 'Average Product Rating',
                data: topFarmers.map((farmer) => farmer.avg_product_rating),
                backgroundColor: '#007bff',
              },
            ],
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                max: 5,
              },
            },
          },
        });
      }
    }

    // Cleanup function to destroy charts
    return () => {
      if (productsChart) {
        productsChart.destroy();
      }
      if (farmersChart) {
        farmersChart.destroy();
      }
    };
  }, [topProducts, topFarmers]);

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Market Insights</h2>
      </div>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{totalProducts}</div>
          <div className="stat-label">Total Products</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{activeFarmers}</div>
          <div className="stat-label">Active Farmers</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{avgRating.toFixed(1)}</div> {/* Ensure avgRating is a number */}
          <div className="stat-label">Average Rating</div>
        </div>
      </div>
      <div className="row">
        <div className="col-md-6">
          <div className="insights-card">
            <h4 className="mb-3">Top Rated Products</h4>
            <canvas id="productsChart" height="200"></canvas>
          </div>
        </div>
        <div className="col-md-6">
          <div className="insights-card">
            <h4 className="mb-3">Top Performing Farmers</h4>
            <canvas id="farmersChart" height="200"></canvas>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketInsights;
