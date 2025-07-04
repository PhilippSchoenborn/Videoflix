import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import logoSvg from '../assets/Logo.svg';
import styles from './Header.module.css';
import Button from './Button';

const Header: React.FC = () => {
  const location = useLocation();
  const isLoginPage = location.pathname === '/';

  return (
    <header className={styles.header}>
      <img src={logoSvg} alt="Videoflix Logo" />
      {!isLoginPage && (
        <Link to="/" className={styles.loginLink}>
          <Button>Login</Button>
        </Link>
      )}
    </header>
  );
};

export default Header;
