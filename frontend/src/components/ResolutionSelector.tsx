import React from 'react';
import styles from './VideoDetailModal.module.css';

type ResolutionSelectorProps = {
  resolutions: string[];
  value: string;
  onChange: (v: string) => void;
};

const order = ['1080p', '720p', '480p', '360p', '120p'];

const ResolutionSelector: React.FC<ResolutionSelectorProps> = ({ resolutions, value, onChange }) => (
  <div className={styles.resolutionSelector}>
    <label htmlFor="resolution-select" className={styles.resolutionLabel}>
      Auflösung wählen:
    </label>
    <select
      id="resolution-select"
      value={value}
      onChange={e => onChange(e.target.value)}
      className={styles.resolutionDropdown}
    >
      {resolutions
        .sort((a, b) => order.indexOf(a) - order.indexOf(b))
        .map(quality => (
          <option key={quality} value={quality}>
            {quality === '1080p' && '1080p HD'}
            {quality === '720p' && '720p HD'}
            {quality === '480p' && '480p'}
            {quality === '360p' && '360p'}
            {quality === '120p' && '120p'}
          </option>
        ))}
    </select>
  </div>
);

export default ResolutionSelector;
