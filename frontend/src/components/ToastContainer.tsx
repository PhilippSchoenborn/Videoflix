import { useToastContext } from '../context/ToastContext';
import type { ToastMessage } from '../hooks/useToast';
import styles from './ToastContainer.module.css';

export default function ToastContainer() {
  const { toasts, removeToast } = useToastContext();

  if (toasts.length === 0) {
    return null;
  }

  const getToastIcon = (type: ToastMessage['type']) => {
    switch (type) {
      case 'success':
        return '✓';
      case 'error':
        return '✕';
      case 'warning':
        return '⚠';
      default:
        return 'ℹ';
    }
  };

  return (
    <div className={styles.toastContainer}>
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`${styles.toast} ${styles[toast.type]}`}
          onClick={() => removeToast(toast.id)}
        >
          <div className={styles.toastLeft}>
            <span className={styles.toastIcon}>
              {getToastIcon(toast.type)}
            </span>
          </div>
          <div className={styles.toastRight}>
            <h3 className={styles.toastTitle}>
              {toast.type === 'error' ? 'Error' : 'Success'}
            </h3>
            <p className={styles.toastMessage}>{toast.message}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
