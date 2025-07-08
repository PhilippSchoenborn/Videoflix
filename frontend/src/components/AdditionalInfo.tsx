import React from 'react';
import type { Video } from '../types';
import styles from './VideoDetailModal.module.css';

type AdditionalInfoProps = {
  video: Video;
  availableResolutions: string[];
};

const AdditionalInfo: React.FC<AdditionalInfoProps> = ({ video, availableResolutions }) => (
  <div className={styles.additionalInfo}>
    <div className={styles.infoRow}><strong>Genre:</strong> {video.genre?.name || 'Unbekannt'}</div>
    <div className={styles.infoRow}><strong>Laufzeit:</strong> {video.duration || 'Unbekannt'}</div>
    <div className={styles.infoRow}><strong>Erscheinungsjahr:</strong> {new Date(video.created_at).getFullYear()}</div>
    <div className={styles.infoRow}><strong>Altersfreigabe:</strong> {video.age_rating}</div>
    <div className={styles.infoRow}><strong>Verfügbare Qualitäten:</strong> {availableResolutions.join(', ')}</div>
  </div>
);

export default AdditionalInfo;
