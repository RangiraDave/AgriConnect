import React, { useEffect, useState } from 'react';
import '../css/style.css';
import { getProducts } from '../api';

const ProductListings = ({ token }) => {
  const [products, setProducts] = useState([]);
  const [userCount, setUserCount] = useState(0);
  const [welcomeMessage, setWelcomeMessage] = useState('Welcome to AgriConnect!');
  const [error, setError] = useState(null);

  useEffect(() => {
    getProducts()
      .then((response) => {
        const data = response.data;
        setProducts(data.products || []);
        setUserCount(data.user_count || 0);
        setWelcomeMessage(data.welcome_message || 'Welcome to AgriConnect!');
      })
      .catch((error) => {
        console.error('Error fetching products:', error);
        setError('Failed to load products. Please try again later.');
      });
  }, []);

  if (error) {
    return (
      <div className="container mt-4">
        <h1 className="text-center">Error</h1>
        <p className="text-center text-danger">{error}</p>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <h1 className="text-center">{welcomeMessage}</h1>
      <p className="text-center">
        Discover products listed by {userCount} farmers across Rwanda.
      </p>
      <div className="row">
        {products.map((product) => (
          <div className="col-md-4 mb-4" key={product.id}>
            <div className="card h-100 shadow-sm">
              {product.media ? (
                <img
                  src={product.media.url}
                  alt={product.name}
                  className="card-img-top"
                />
              ) : (
                <img
                  src="/static/img/no_image.png"
                  alt={product.name}
                  className="card-img-top"
                />
              )}
              <div className="card-body">
                <h5 className="card-title">{product.name}</h5>
                <p className="card-text">
                  {product.description || 'No description available.'}
                </p>
                <p className="text-muted">
                  <strong>Owner:</strong> {product.owner.profile.role} -{' '}
                  {product.owner.username}
                </p>
                <p className="text-muted">
                  <strong>Contacts:</strong> {product.owner.profile.phone}
                </p>
                <a href={`/products/${product.id}`} className="btn btn-primary">
                  View Details
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductListings;
