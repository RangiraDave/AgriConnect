import React from 'react';
import '../css/style.css';

const ProductListings = ({ products, userCount, totalProducts, welcomeMessage }) => {
  return (
    <div className="container mt-4">
      <h1 className="text-center">{welcomeMessage}</h1>
      <p>
        Ngibi ibicuruzwa bikeneye abaguzi byashyizweho n'abahinzi bo mu Rwanda bagera kuri {userCount}.
      </p>
      <div className="row mb-4">
        <div className="col-md-6">
          <p>Byose hamwe ni: {totalProducts}</p>
        </div>
      </div>
      <h2>Ibicuruzwa bihari</h2>
      <div className="row product-list-row">
        {products.map((product) => (
          <div className="col-md-4 mb-4" key={product.id}>
            <div className="card h-100 card-product">
              {product.media ? (
                product.media.url.toLowerCase().endsWith('.mp4') ? (
                  <video controls className="card-img-top img-fluid">
                    <source src={product.media.url} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                ) : (
                  <img
                    src={product.media.url}
                    alt={product.name}
                    className="card-img-top img-fluid"
                  />
                )
              ) : (
                <img
                  src="/static/img/no_image.png"
                  alt={product.name}
                  className="card-img-top img-fluid"
                />
              )}
              <div className="product-card">
                <h5>{product.name}</h5>
                {product.description && <p>{product.description}</p>}
                <small>
                  <strong>Owner:</strong> {product.owner.profile.role} - {product.owner.username}
                </small>
                <br />
                <small>
                  <strong>Contacts:</strong> {product.owner.profile.phone}
                </small>
                {product.location && (
                  <small>
                    <strong>Location:</strong> {product.location}
                  </small>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductListings;
