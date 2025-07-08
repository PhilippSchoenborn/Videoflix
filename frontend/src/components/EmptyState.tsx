import React from 'react';
import styles from './VideoGrid.module.css';

type EmptyStateProps = {
  message: string;
};

const EmptyState: React.FC<EmptyStateProps> = ({ message }) => (
  <div className={styles.emptyState}>
    <div className={styles.emptyMessage}>{message}</div>
  </div>
);

export default EmptyState;
