import React, { useState, useRef, useEffect } from 'react';
import styles from './VideoOverlay.module.css';

interface Video {
  id: number;
  title: string;
  description: string;
  video_file?: string;
  thumbnail: string;
  created_at: string;
}

interface VideoOverlayProps {
  video: Video;
  onClose: () => void;
}

const VideoOverlay: React.FC<VideoOverlayProps> = ({ video, onClose }) => {
  const [resolution, setResolution] = useState('480p');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (videoRef.current && video) {
      loadVideo();
    }
  }, [video, resolution]);

  const loadVideo = async () => {
    if (!videoRef.current) return;
    
    setIsLoading(true);
    setError('');
    
    try {
      // Construct video URL with resolution parameter
      const videoUrl = `${video.video_file || ''}?resolution=${resolution}`;
      videoRef.current.src = videoUrl;
      
      // Wait for video to load
      await new Promise((resolve, reject) => {
        if (!videoRef.current) return reject('Video element not found');
        
        const handleLoad = () => {
          setIsLoading(false);
          resolve(true);
        };
        
        const handleError = () => {
          setError('Failed to load video');
          setIsLoading(false);
          reject('Video failed to load');
        };
        
        videoRef.current.addEventListener('loadeddata', handleLoad);
        videoRef.current.addEventListener('error', handleError);
        
        // Cleanup function
        return () => {
          if (videoRef.current) {
            videoRef.current.removeEventListener('loadeddata', handleLoad);
            videoRef.current.removeEventListener('error', handleError);
          }
        };
      });
    } catch (err) {
      console.error('Error loading video:', err);
      setError('Failed to load video');
      setIsLoading(false);
    }
  };

  const handleResolutionChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setResolution(event.target.value);
  };

  const handleOverlayClick = (event: React.MouseEvent) => {
    if (event.target === event.currentTarget) {
      onClose();
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Escape') {
      onClose();
    }
  };

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown as any);
    return () => {
      document.removeEventListener('keydown', handleKeyDown as any);
    };
  }, []);

  return (
    <div 
      className={styles.videoOverlay} 
      onClick={handleOverlayClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="video-title"
    >
      <div className={styles.overlayContent}>
        <div className={styles.overlayHeader}>
          <button 
            className={styles.backButton}
            onClick={onClose}
            aria-label="Close video"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M19 12H5M12 19l-7-7 7-7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
          
          <h1 id="video-title" className={styles.overlayTitle}>
            {video.title}
          </h1>
          
          <img 
            src="/assets/icons/logo_icon_small.svg" 
            alt="Videoflix Logo" 
            className={styles.logo}
          />
        </div>

        <div className={styles.videoWrapper}>
          {isLoading && (
            <div className={styles.loadingIndicator}>
              <div className={styles.spinner}></div>
              <p>Loading video...</p>
            </div>
          )}
          
          {error && (
            <div className={styles.errorMessage}>
              <p>{error}</p>
              <button 
                className={styles.retryButton}
                onClick={loadVideo}
              >
                Retry
              </button>
            </div>
          )}
          
          <video
            ref={videoRef}
            controls
            className={styles.overlayVideo}
            style={{ display: isLoading || error ? 'none' : 'block' }}
          >
            <source src={video.video_file || ''} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>

        <div className={styles.overlayControls}>
          <label htmlFor="resolution-select" className={styles.resolutionLabel}>
            Resolution:
          </label>
          <select
            id="resolution-select"
            value={resolution}
            onChange={handleResolutionChange}
            className={styles.resolutionSelect}
          >
            <option value="480p">480p</option>
            <option value="720p">720p</option>
            <option value="1080p">1080p</option>
          </select>
        </div>

        <div className={styles.videoDescription}>
          <p>{video.description}</p>
        </div>
      </div>
    </div>
  );
};

export default VideoOverlay;
