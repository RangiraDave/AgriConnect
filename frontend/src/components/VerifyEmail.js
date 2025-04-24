import React, { useState } from 'react';
import '../css/style.css';

const VerifyEmail = ({ verificationEmail }) => {
  const [verificationCode, setVerificationCode] = useState('');
  const [email, setEmail] = useState(verificationEmail);

  const handleVerify = (e) => {
    e.preventDefault();
    // Add logic to verify the email
  };

  const handleResend = (e) => {
    e.preventDefault();
    // Add logic to resend the verification code
  };

  return (
    <div className="container mt-4">
      <h1>Verify Your Email</h1>
      <p>Please enter the verification code sent to your email.</p>
      <form onSubmit={handleVerify}>
        <label htmlFor="verification_code">Verification Code:</label>
        <input
          type="text"
          id="verification_code"
          value={verificationCode}
          onChange={(e) => setVerificationCode(e.target.value)}
          required
        />
        <button type="submit">Verify</button>
      </form>
      <hr />
      <h2>Didn't receive the code?</h2>
      <form onSubmit={handleResend}>
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit">Resend Code</button>
      </form>
    </div>
  );
};

export default VerifyEmail;
