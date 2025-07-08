import React from 'react';
import styles from './VideoPlayer.module.css';

interface ErrorOverlayProps {
  message: string;
  onClose: () => void;
}

const ErrorOverlay: React.FC<ErrorOverlayProps> = ({ message, onClose }) => (
  <div className={styles.errorOverlay}>
    <p>{message}</p>
    <button onClick={onClose}>Close</button>
  </div>
);

export default ErrorOverlay;
