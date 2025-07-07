import styles from './ErrorMessage.module.css';

interface ErrorMessageProps {
  message: string;
  isVisible: boolean;
  className?: string;
}

export default function ErrorMessage({ message, isVisible, className = '' }: ErrorMessageProps) {
  if (!isVisible || !message) {
    return null;
  }

  return (
    <div className={`${styles.errorMessage} ${className}`}>
      <span className={styles.errorIcon}></span>
      <span className={styles.errorText}>{message}</span>
    </div>
  );
}
