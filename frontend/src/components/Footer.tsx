import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Footer.module.css';

const Footer: React.FC = () => (
  <footer className={styles.footer}>
    <Link to="/datenschutz" className={styles.footerLink}>
      Datenschutz
    </Link>
    <Link to="/impressum" className={styles.footerLink}>
      Impressum
    </Link>
  </footer>
);

export default Footer;
