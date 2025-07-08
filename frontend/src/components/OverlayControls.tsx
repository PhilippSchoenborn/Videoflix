import React from 'react';
import styles from './VideoOverlay.module.css';

interface OverlayControlsProps {
  resolution: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}

/**
 * Auswahl der Videoauflösung.
 */
const OverlayControls: React.FC<OverlayControlsProps> = ({ resolution, onChange }) => (
  <div className={styles.overlayControls}>
    <label htmlFor="resolution-select" className={styles.resolutionLabel}>
      Resolution:
    </label>
    <select
      id="resolution-select"
      value={resolution}
      onChange={onChange}
      className={styles.resolutionSelect}
    >
      <option value="480p">480p</option>
      <option value="720p">720p</option>
      <option value="1080p">1080p</option>
    </select>
  </div>
);

export default OverlayControls;
