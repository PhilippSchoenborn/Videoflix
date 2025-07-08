import React from 'react';
import styles from './VideoPlayer.module.css';

type Quality = '120p' | '360p' | '480p' | '720p' | '1080p';

interface QualitySelectorProps {
  current: Quality;
  available: Quality[];
  showMenu: boolean;
  onToggle: () => void;
  onSelect: (q: Quality) => void;
}

const QualitySelector: React.FC<QualitySelectorProps> = ({ current, available, showMenu, onToggle, onSelect }) => (
  <div className={styles.qualitySelector}>
    <button className={styles.qualityButton} onClick={onToggle} aria-label="Change quality">{current}</button>
    {showMenu && (
      <div className={styles.qualityMenu}>
        {available.map(q => (
          <button key={q} className={`${styles.qualityOption} ${q === current ? styles.active : ''}`} onClick={() => onSelect(q)}>{q}</button>
        ))}
      </div>
    )}
  </div>
);

export default QualitySelector;
