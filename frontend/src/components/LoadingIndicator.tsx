import React from 'react';
import styles from './VideoOverlay.module.css';

/**
 * Zeigt einen Ladeindikator für das Video an.
 */
const LoadingIndicator: React.FC = () => (
  <div className={styles.loadingIndicator}>
    <div className={styles.spinner}></div>
    <p>Loading video...</p>
  </div>
);

export default LoadingIndicator;
