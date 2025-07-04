import React from 'react';
import styles from './Button.module.css';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({ children, className = '', ...props }) => {
  return (
    <button className={`${styles.button} ${className}`} {...props}>
      <span className={styles.buttonText}>{children}</span>
    </button>
  );
};

export default Button;
