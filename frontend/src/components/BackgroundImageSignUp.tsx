import React from 'react';
import styles from './BackgroundImageSignUp.module.css';

interface BackgroundImageSignUpProps {
  children?: React.ReactNode;
}

const BackgroundImageSignUp: React.FC<BackgroundImageSignUpProps> = ({ children }) => (
  <div className={styles.backgroundWrapper}>
    <div className={styles.background} />
    {children}
  </div>
);

export default BackgroundImageSignUp;
