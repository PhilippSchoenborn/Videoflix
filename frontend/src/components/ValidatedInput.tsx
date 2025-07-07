import { useState } from 'react';
import styles from './ValidatedInput.module.css';
import ErrorMessage from './ErrorMessage';
import visibilityOffSvg from '../assets/visibility_off.svg';
import visibilitySvg from '../assets/visibility.svg';

interface ValidatedInputProps {
  type: 'text' | 'email' | 'password';
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.FocusEvent<HTMLInputElement>) => void;
  placeholder: string;
  icon: string;
  iconAlt: string;
  required?: boolean;
  hasError?: boolean;
  errorMessage?: string;
  className?: string;
  autoComplete?: string;
  showPasswordToggle?: boolean;
  variant?: 'default' | 'landing'; // New variant prop
}

export default function ValidatedInput({
  type,
  name,
  value,
  onChange,
  onBlur,
  placeholder,
  icon,
  iconAlt,
  required = false,
  hasError = false,
  errorMessage = '',
  className = '',
  autoComplete,
  showPasswordToggle = false,
  variant = 'default'
}: ValidatedInputProps) {
  const [showPassword, setShowPassword] = useState(false);
  
  const inputType = type === 'password' && showPasswordToggle 
    ? (showPassword ? 'text' : 'password')
    : type;

  const inputClasses = `
    ${styles.inputField}
    ${hasError ? styles.inputFieldError : ''}
    ${showPasswordToggle ? styles.inputFieldPassword : ''}
    ${className}
  `.trim();

  const containerClasses = variant === 'landing' 
    ? `${styles.inputRowLanding} ${hasError ? styles.inputRowError : ''}`
    : `${styles.inputRow} ${hasError ? styles.inputRowError : ''}`;

  return (
    <div className={containerClasses}>
      <img src={icon} alt={iconAlt} className={styles.inputIcon} />
      <input
        type={inputType}
        name={name}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        placeholder={placeholder}
        required={required}
        className={inputClasses}
        autoComplete={autoComplete}
      />
      {showPasswordToggle && (
        <img 
          src={showPassword ? visibilityOffSvg : visibilitySvg}
          alt="Toggle password visibility" 
          className={styles.visibilityIcon}
          onClick={() => setShowPassword(!showPassword)}
        />
      )}
      <ErrorMessage 
        message={errorMessage}
        isVisible={hasError}
        className={styles.errorContainer}
      />
    </div>
  );
}
