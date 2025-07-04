import React from 'react';
import styles from './BackgroundImage.module.css';

interface BackgroundImageProps {
  children?: React.ReactNode;
}

const BackgroundImage: React.FC<BackgroundImageProps> = ({ children }) => (
  <div className={styles.backgroundWrapper}>
    <div className={styles.background} />
    {children}
  </div>
);

export default BackgroundImage;
