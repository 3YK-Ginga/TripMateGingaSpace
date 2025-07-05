import React, { useState } from 'react';
import './SignUpPage.css';

function SignUpPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');

  const handleSignUp = () => {
    if (password !== confirm) {
      alert('パスワードが一致しません。');
      return;
    }
    alert(`新規登録情報\nEmail: ${email}\nPassword: ${password}`);
  };

  return (
    <div className="signup-container">
      <h2>新規登録</h2>
      <div className="signup-form">
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
        <label>
          パスワード(確認):
          <input
            type="password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
          />
        </label>
        <button onClick={handleSignUp}>登録</button>
      </div>
    </div>
  );
}

export default SignUpPage;
