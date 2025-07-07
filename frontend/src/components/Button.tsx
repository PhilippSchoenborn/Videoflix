import React from 'react';
import styles from './Button.module.css';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'small';
}

const Button: React.FC<ButtonProps> = ({ children, className = '', variant = 'primary', ...props }) => {
  const variantClass = variant === 'small' ? styles.buttonSmall :
                      variant === 'secondary' ? styles.buttonSecondary :
                      styles.button;
  
  return (
    <button className={`${variantClass} ${className}`} {...props}>
      <span className={styles.buttonText}>{children}</span>
    </button>
  );
};

export default Button;
