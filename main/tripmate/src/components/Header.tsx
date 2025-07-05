import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Header.css';

function Header() {
  const navigate = useNavigate();

  // 「TripMate」クリックでトップページ(/)へ
  const handleTitleClick = () => {
    navigate('/');
  };

  return (
    <header className="header-container">
      <button className="header-title-button" onClick={handleTitleClick}>
        TripMate
      </button>
      <nav className="header-nav">
        <Link to="/login" className="header-link">ログイン</Link>
        <Link to="/signup" className="header-link">新規登録</Link>
      </nav>
    </header>
  );
}

export default Header;
