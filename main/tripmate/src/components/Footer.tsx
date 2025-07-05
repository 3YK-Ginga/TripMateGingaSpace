import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
  return (
    <footer className="footer-container">
      <span className="footer-updated">最終更新日: 2024-12-20</span>
      <Link to="/support" className="footer-support">
        サポートはこちら
      </Link>
    </footer>
  );
}

export default Footer;
