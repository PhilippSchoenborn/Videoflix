import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './BackArrow.module.css';
import arrowSvg from '../assets/arrow.svg';

interface BackArrowProps {
  to?: string | number; // string for path, number for history steps
  className?: string;
  style?: React.CSSProperties;
  'aria-label'?: string;
}

const BackArrow: React.FC<BackArrowProps> = ({ to = -1, className = '', style, ...props }) => {
  const navigate = useNavigate();
  const handleClick = () => {
    if (typeof to === 'number') navigate(to);
    else navigate(to);
  };
  return (
    <button
      className={`${styles.arrowButton} ${className}`}
      style={style}
      onClick={handleClick}
      aria-label={props['aria-label'] || 'Back'}
      type="button"
    >
      <span className={styles.arrowIconWrapper}>
        <img src={arrowSvg} alt="Back" className={styles.arrowIcon} />
        <span className={styles.arrowOverlay} />
      </span>
    </button>
  );
};

export default BackArrow;
