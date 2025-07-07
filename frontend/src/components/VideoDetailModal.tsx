import React from 'react';
import type { Video } from '../types';
import styles from './VideoDetailModal.module.css';

interface VideoDetailModalProps {
  video: Video;
  isOpen: boolean;
  onClose: () => void;
  onPlayVideo: (video: Video, resolution: '120p' | '360p' | '480p' | '720p' | '1080p') => void;
}

const VideoDetailModal: React.FC<VideoDetailModalProps> = ({
  video,
  isOpen,
  onClose,
  onPlayVideo
}) => {
  const [selectedResolution, setSelectedResolution] = React.useState<'120p' | '360p' | '480p' | '720p' | '1080p'>('720p');
  
  if (!isOpen) {
    return null;
  }

  const availableResolutions = video.video_files?.map(vf => vf.quality) || [];

  // Set default resolution to highest available or 720p if available
  React.useEffect(() => {
    if (availableResolutions.length > 0) {
      const resolutionOrder = ['1080p', '720p', '480p', '360p', '120p'] as const;
      const bestAvailable = resolutionOrder.find(res => availableResolutions.includes(res));
      if (bestAvailable) {
        setSelectedResolution(bestAvailable);
      } else {
        setSelectedResolution(availableResolutions[0] as any);
      }
    }
  }, [video.id, availableResolutions.join(',')]);

  const handlePlayClick = () => {
    onPlayVideo(video, selectedResolution);
    onClose();
  };

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className={styles.modalBackdrop} onClick={handleBackdropClick}>
      <div className={styles.modalContent}>
        <button 
          className={styles.closeButton}
          onClick={onClose}
          aria-label="Close detail view"
        >
          ×
        </button>
        
        <div className={styles.videoInfo}>
          <div className={styles.thumbnailContainer}>
            {video.thumbnail ? (
              <img 
                src={video.thumbnail} 
                alt={video.title}
                className={styles.thumbnail}
              />
            ) : (
              <div className={styles.placeholderThumbnail}>
                <span>No Thumbnail</span>
              </div>
            )}
          </div>
          
          <div className={styles.detailsContainer}>
            <h2 className={styles.title}>{video.title}</h2>
            
            <div className={styles.metaInfo}>
              <span className={styles.genre}>{video.genre?.name}</span>
              <span className={styles.duration}>{video.duration}</span>
              <span className={styles.ageRating}>{video.age_rating}</span>
            </div>
            
            <p className={styles.description}>{video.description}</p>
            
            <div className={styles.playSection}>
              <h3>Video abspielen</h3>
              <div className={styles.playControls}>
                <div className={styles.resolutionSelector}>
                  <label htmlFor="resolution-select" className={styles.resolutionLabel}>
                    Auflösung wählen:
                  </label>
                  <select 
                    id="resolution-select"
                    value={selectedResolution}
                    onChange={(e) => setSelectedResolution(e.target.value as '120p' | '360p' | '480p' | '720p' | '1080p')}
                    className={styles.resolutionDropdown}
                  >
                    {availableResolutions
                      .sort((a, b) => {
                        // Sort resolutions in descending order
                        const order = ['1080p', '720p', '480p', '360p', '120p'];
                        return order.indexOf(a) - order.indexOf(b);
                      })
                      .map(quality => (
                        <option key={quality} value={quality}>
                          {quality === '1080p' && '1080p HD'}
                          {quality === '720p' && '720p HD'}
                          {quality === '480p' && '480p'}
                          {quality === '360p' && '360p'}
                          {quality === '120p' && '120p'}
                        </option>
                      ))
                    }
                  </select>
                </div>
                <button 
                  className={styles.mainPlayButton}
                  onClick={handlePlayClick}
                  title={`Video in ${selectedResolution} abspielen`}
                >
                  ▶
                </button>
              </div>
            </div>

            <div className={styles.additionalInfo}>
              <div className={styles.infoRow}>
                <strong>Genre:</strong> {video.genre?.name || 'Unbekannt'}
              </div>
              <div className={styles.infoRow}>
                <strong>Laufzeit:</strong> {video.duration || 'Unbekannt'}
              </div>
              <div className={styles.infoRow}>
                <strong>Erscheinungsjahr:</strong> {new Date(video.created_at).getFullYear()}
              </div>
              <div className={styles.infoRow}>
                <strong>Altersfreigabe:</strong> {video.age_rating}
              </div>
              <div className={styles.infoRow}>
                <strong>Verfügbare Qualitäten:</strong> {availableResolutions.join(', ')}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoDetailModal;
