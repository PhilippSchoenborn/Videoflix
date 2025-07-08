import React from 'react';
import styles from './ScrollableVideoList.module.css';

type ScrollButtonProps = {
  direction: 'left' | 'right';
  onClick: () => void;
};

const icons = {
  left: (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M15 18l-6-6 6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  right: (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M9 18l6-6-6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
};

const ScrollButton: React.FC<ScrollButtonProps> = ({ direction, onClick }) => (
  <button
    className={`${styles.scrollButton} ${direction === 'left' ? styles.scrollLeft : styles.scrollRight}`}
    onClick={onClick}
    aria-label={`Scroll ${direction}`}
  >
    {icons[direction]}
  </button>
);

export default ScrollButton;
