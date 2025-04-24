import React, { useEffect } from 'react';
import '../css/style.css';
import Chart from 'chart.js/auto';

const MarketInsights = ({ totalProducts, activeFarmers, avgRating, topProducts, topFarmers }) => {
  useEffect(() => {
    const productsChart = new Chart(document.getElementById('productsChart'), {
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

    const farmersChart = new Chart(document.getElementById('farmersChart'), {
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

    return () => {
      productsChart.destroy();
      farmersChart.destroy();
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
          <div className="stat-value">{avgRating.toFixed(1)}</div>
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
