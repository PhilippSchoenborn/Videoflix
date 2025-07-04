import React from 'react';
import styles from './BackgroundImageLanding.module.css';

interface BackgroundImageLandingProps {
  children?: React.ReactNode;
}

const BackgroundImageLanding: React.FC<BackgroundImageLandingProps> = ({ children }) => (
  <div className={styles.backgroundWrapper}>
    <div className={styles.background} />
    {children}
  </div>
);

export default BackgroundImageLanding;
