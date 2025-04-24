import React from 'react';

const Home = ({ isAuthenticated }) => {
  return (
    <div>
      <div className=" jumbotron text-center bg-success text-white p-5">
        <h1 className="display-4">Murakaza neza kuri AgriConnect!</h1>
        <p className="lead">Dufasha abahinzi kugera ku isoko rikwiye muburyo bworoshye.</p>
        <div className="mt-4">
          {isAuthenticated ? (
            <>
              <a className="btn btn-primary btn-lg" href="/products/">Ibihari</a>
              <a className="btn btn-primary btn-lg" href="/profile/">Konte yawe</a>
            </>
          ) : (
            <>
              <a className="btn btn-primary btn-lg" href="/signup/">Kora Konti</a>
              <a className="btn btn-primary btn-lg" href="/login/">Injira</a>
            </>
          )}
        </div>
      </div>

      <div className="container mt-5">
        {/* <h2 className="text-center mb-4">Hitamo Icyiciro</h2> */}
        <div className="row text-center">
          <div className="col-md-4">
            <a href="/signup/" className="btn btn-outline-success btn-lg w-99">Kora Konti</a>
          </div>
          <div className="col-md-4">
            <a href="/login/" className="btn btn-outline-primary btn-lg w-100">Injira</a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;