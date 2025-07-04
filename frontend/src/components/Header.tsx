import React from 'react';
import logoSvg from '../assets/Logo.svg';
import styles from './Header.module.css';

const Header: React.FC = () => (
  <header className={styles.header}>
    <img src={logoSvg} alt="Videoflix Logo" />
  </header>
);

export default Header;
