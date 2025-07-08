import React from 'react';
import styles from './VideoGrid.module.css';

type ViewAllButtonProps = {
  onClick?: () => void;
};

const ViewAllButton: React.FC<ViewAllButtonProps> = ({ onClick }) => (
  <button className={styles.viewAllButton} onClick={onClick}>
    View All →
  </button>
);

export default ViewAllButton;
