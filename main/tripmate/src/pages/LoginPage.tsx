import React, { useState } from 'react';
import './LoginPage.css';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    alert(`ログイン情報\nEmail: ${email}\nPassword: ${password}`);
  };

  return (
    <div className="login-container">
      <h2>ログイン</h2>
      <div className="login-form">
        <label>
          メールアドレス:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label>
          パスワード:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <button onClick={handleLogin}>ログイン</button>
      </div>
    </div>
  );
}

export default LoginPage;
