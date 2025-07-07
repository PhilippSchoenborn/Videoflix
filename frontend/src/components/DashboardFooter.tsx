import React from 'react';
import { Link } from 'react-router-dom';
import styles from './DashboardFooter.module.css';

const DashboardFooter: React.FC = () => (
  <footer className={styles.footer}>
    <div className={styles.footerContent}>
      <div className={styles.footerLinks}>
        <Link to="/datenschutz" className={styles.footerLink}>
          Datenschutz
        </Link>
        <Link to="/impressum" className={styles.footerLink}>
          Impressum
        </Link>
      </div>
    </div>
  </footer>
);

export default DashboardFooter;
