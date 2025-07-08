import React from 'react';
import styles from './VideoGrid.module.css';

type ResumeButtonProps = {
  onClick: (e: React.MouseEvent) => void;
};

const ResumeButton: React.FC<ResumeButtonProps> = ({ onClick }) => (
  <button onClick={onClick} className={styles.resumeButton}>
    Resume
  </button>
);

export default ResumeButton;
