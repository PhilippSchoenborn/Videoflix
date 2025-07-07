import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import logoSvg from '../assets/Logo.svg';
import styles from './Header.module.css';
import Button from './Button';
import LogoutButton from './LogoutButton';
import BurgerMenu from './BurgerMenu';

const Header: React.FC = () => {
  const location = useLocation();
  const { isAuthenticated } = useAuth();
  
  const hideCTAButton = location.pathname === '/login' || 
                        location.pathname === '/impressum' || 
                        location.pathname === '/datenschutz';

  return (
    <header className={styles.header}>
      <img src={logoSvg} alt="Videoflix Logo" />
      {!hideCTAButton && (
        <div className={styles.headerRight}>
          {isAuthenticated ? (
            <LogoutButton />
          ) : (
            <>
              <div className={styles.rightSection + ' ' + styles.hideOnMobile}>
                <Link to="/login" className={styles.loginLink}>
                  <Button>Login</Button>
                </Link>
              </div>
              <BurgerMenu />
            </>
          )}
        </div>
      )}
    </header>
  );
};

export default Header;
