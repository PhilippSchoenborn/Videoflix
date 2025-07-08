import React from 'react';
import styles from './VideoPlayer.module.css';

const LoadingOverlay: React.FC = () => (
  <div className={styles.loadingOverlay}>
    <div className={styles.spinner}></div>
    <p>Loading video...</p>
  </div>
);

export default LoadingOverlay;
