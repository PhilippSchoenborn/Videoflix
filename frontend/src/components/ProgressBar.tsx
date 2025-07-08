import React from 'react';
import styles from './ScrollableVideoList.module.css';

type ProgressBarProps = {
  percentage: number;
};

const ProgressBar: React.FC<ProgressBarProps> = ({ percentage }) => (
  <div className={styles.progressBar}>
    <div className={styles.progressFill} style={{ width: `${percentage}%` }} />
  </div>
);

export default ProgressBar;
