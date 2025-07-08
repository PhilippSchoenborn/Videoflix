import React from 'react';
import styles from './VideoOverlay.module.css';

interface OverlayHeaderProps {
  title: string;
  onClose: () => void;
}

/**
 * Header mit Titel, Logo und Close-Button.
 */
const OverlayHeader: React.FC<OverlayHeaderProps> = ({ title, onClose }) => (
  <div className={styles.overlayHeader}>
    <button className={styles.backButton} onClick={onClose} aria-label="Close video">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M19 12H5M12 19l-7-7 7-7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    </button>
    <h1 id="video-title" className={styles.overlayTitle}>{title}</h1>
    <img src="/assets/icons/logo_icon_small.svg" alt="Videoflix Logo" className={styles.logo} />
  </div>
);

export default OverlayHeader;
