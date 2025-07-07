import React, { useRef, useEffect, useState } from 'react';
import { useToast } from '../hooks/useToast';
import apiService from '../services/api';
import type { Video } from '../types';
import styles from './VideoPlayer.module.css';

interface VideoPlayerProps {
  video: Video;
  resolution: '120p' | '360p' | '480p' | '720p' | '1080p';
  isOpen: boolean;
  onClose: () => void;
  resumeTime?: number;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({
  video,
  resolution: initialResolution,
  isOpen,
  onClose,
  resumeTime = 0
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentResolution, setCurrentResolution] = useState(initialResolution);
  const [showQualityMenu, setShowQualityMenu] = useState(false);
  const [hasSetResumeTime, setHasSetResumeTime] = useState(false);
  const { showToast } = useToast();

  const availableQualities: Array<'120p' | '360p' | '480p' | '720p' | '1080p'> = [
    '1080p', '720p', '480p', '360p', '120p'
  ];

  // Reset resume time state when new video or resolution changes
  useEffect(() => {
    setHasSetResumeTime(false);
  }, [video.id, currentResolution]);

  // Load video when component mounts or resolution changes
  useEffect(() => {
    if (!isOpen) return;

    const videoElement = videoRef.current;
    if (!videoElement) return;

    const streamUrl = `http://localhost:8000/api/videos/${video.id}/stream/${currentResolution}/`;
    
    setIsLoading(true);
    setError(null);
    videoElement.src = streamUrl;

    const handleCanPlay = () => {
      setIsLoading(false);
      
      // Auto-play only if no resume time, otherwise wait for loadedmetadata
      if (resumeTime === 0 || hasSetResumeTime) {
        videoElement.play().catch(err => {
          if (err.name !== 'AbortError') {
            console.error('Error playing video:', err);
            setError('Failed to play video');
            showToast('Failed to play video', 'error');
          }
        });
      }
    };

    const handleLoadedMetadata = () => {
      // Set resume time when metadata is loaded (better timing for currentTime)
      if (resumeTime > 0 && !hasSetResumeTime) {
        
        // Pause first to ensure we can set currentTime reliably
        videoElement.pause();
        
        // Use a small delay to ensure the video is fully ready
        setTimeout(() => {
          videoElement.currentTime = resumeTime;
          
          // Wait for the seek to complete
          const waitForSeek = () => {
            if (Math.abs(videoElement.currentTime - resumeTime) < 1) {
              setHasSetResumeTime(true);
              
              // Start playing after setting currentTime
              videoElement.play().catch(err => {
                if (err.name !== 'AbortError') {
                  console.error('Error playing video:', err);
                  setError('Failed to play video');
                  showToast('Failed to play video', 'error');
                }
              });
            } else {
              setTimeout(waitForSeek, 50);
            }
          };
          
          waitForSeek();
        }, 100); // 100ms delay
      }
    };

    const handleError = () => {
      setError('Failed to load video');
      setIsLoading(false);
      showToast('Failed to load video', 'error');
    };

    const handleSeeked = () => {
      // This event fires when seeking (setting currentTime) is complete
    };

    const handleTimeUpdate = () => {
      if (videoElement.currentTime > 0) {
        const currentTime = Math.floor(videoElement.currentTime);
        const duration = videoElement.duration;
        
        // Check if video is nearly finished (>=90% or last 30 seconds)
        const isNearEnd = duration > 0 && (
          (currentTime / duration) >= 0.9 || 
          (duration - currentTime) <= 30
        );
        
        // Save progress every 5 seconds instead of 10 for more frequent saves
        if (currentTime % 5 === 0) {
          apiService.updateWatchProgress(video.id, currentTime, isNearEnd, currentResolution).catch(console.error);
        }
      }
    };

    const handlePause = () => {
      // Save progress immediately when video is paused
      if (videoElement.currentTime > 0) {
        const currentTime = Math.floor(videoElement.currentTime);
        const duration = videoElement.duration;
        
        // Check if video is nearly finished (>=90% or last 30 seconds)
        const isNearEnd = duration > 0 && (
          (currentTime / duration) >= 0.9 || 
          (duration - currentTime) <= 30
        );
        
        apiService.updateWatchProgress(video.id, currentTime, isNearEnd, currentResolution).catch(console.error);
      }
    };

    const handlePlay = () => {
      // Update last watched time when video starts playing
      if (videoElement.currentTime > 0) {
        const currentTime = Math.floor(videoElement.currentTime);
        const duration = videoElement.duration;
        
        // Check if video is nearly finished (>=90% or last 30 seconds)
        const isNearEnd = duration > 0 && (
          (currentTime / duration) >= 0.9 || 
          (duration - currentTime) <= 30
        );
        
        apiService.updateWatchProgress(video.id, currentTime, isNearEnd, currentResolution).catch(console.error);
      }
    };

    // Save progress when user leaves the page
    const handleBeforeUnload = () => {
      if (videoElement.currentTime > 0) {
        const currentTime = Math.floor(videoElement.currentTime);
        const duration = videoElement.duration;
        
        // Check if video is nearly finished (>=90% or last 30 seconds)
        const isNearEnd = duration > 0 && (
          (currentTime / duration) >= 0.9 || 
          (duration - currentTime) <= 30
        );
        
        // Use sendBeacon for reliable saving when page is closing
        const data = JSON.stringify({
          video_id: video.id,
          progress_seconds: currentTime,
          last_resolution: currentResolution,
          completed: isNearEnd
        });
        navigator.sendBeacon(`http://localhost:8000/api/videos/${video.id}/progress/`, data);
      }
    };

    const handleEnded = () => {
      // Mark video as completed when it reaches the end
      if (videoElement.currentTime > 0) {
        const currentTime = Math.floor(videoElement.currentTime);
        apiService.updateWatchProgress(video.id, currentTime, true, currentResolution).catch(console.error);
      }
    };

    videoElement.addEventListener('canplay', handleCanPlay);
    videoElement.addEventListener('loadedmetadata', handleLoadedMetadata);
    videoElement.addEventListener('seeked', handleSeeked);
    videoElement.addEventListener('error', handleError);
    videoElement.addEventListener('timeupdate', handleTimeUpdate);
    videoElement.addEventListener('pause', handlePause);
    videoElement.addEventListener('play', handlePlay);
    videoElement.addEventListener('ended', handleEnded);
    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      videoElement.removeEventListener('canplay', handleCanPlay);
      videoElement.removeEventListener('loadedmetadata', handleLoadedMetadata);
      videoElement.removeEventListener('seeked', handleSeeked);
      videoElement.removeEventListener('error', handleError);
      videoElement.removeEventListener('timeupdate', handleTimeUpdate);
      videoElement.removeEventListener('pause', handlePause);
      videoElement.removeEventListener('play', handlePlay);
      videoElement.removeEventListener('ended', handleEnded);
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, [video.id, currentResolution, isOpen, showToast]);

  const handleResolutionChange = (newResolution: '120p' | '360p' | '480p' | '720p' | '1080p') => {
    const videoElement = videoRef.current;
    if (!videoElement) return;

    const currentTime = videoElement.currentTime;
    setCurrentResolution(newResolution);
    setShowQualityMenu(false);
    setIsLoading(true);
    
    // Wait for new video to load then set time
    const handleNewVideoCanPlay = () => {
      videoElement.currentTime = currentTime;
      videoElement.play().catch(console.error);
      setIsLoading(false);
      videoElement.removeEventListener('canplay', handleNewVideoCanPlay);
    };
    
    videoElement.addEventListener('canplay', handleNewVideoCanPlay);
    showToast(`Switching to ${newResolution}...`, 'info');
  };

  const handleClose = () => {
    if (videoRef.current) {
      // Save current progress before closing
      if (videoRef.current.currentTime > 0) {
        const currentTime = Math.floor(videoRef.current.currentTime);
        const duration = videoRef.current.duration;
        
        // Check if video is nearly finished (>=90% or last 30 seconds)
        const isNearEnd = duration > 0 && (
          (currentTime / duration) >= 0.9 || 
          (duration - currentTime) <= 30
        );
        
        apiService.updateWatchProgress(video.id, currentTime, isNearEnd, currentResolution).catch(console.error);
      }
      
      videoRef.current.pause();
      videoRef.current.src = '';
    }
    setHasSetResumeTime(false);
    setError(null);
    setIsLoading(true);
    onClose();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      handleClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div 
      className={styles.playerOverlay} 
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      <div className={styles.playerContainer}>
        <button 
          className={styles.closeButton}
          onClick={handleClose}
          aria-label="Close player"
        >
          ✕
        </button>
        
        {/* Quality Selector */}
        <div className={styles.qualitySelector}>
          <button 
            className={styles.qualityButton}
            onClick={() => setShowQualityMenu(!showQualityMenu)}
            aria-label="Change quality"
          >
            {currentResolution}
          </button>
          
          {showQualityMenu && (
            <div className={styles.qualityMenu}>
              {availableQualities.map((quality) => (
                <button
                  key={quality}
                  className={`${styles.qualityOption} ${quality === currentResolution ? styles.active : ''}`}
                  onClick={() => handleResolutionChange(quality)}
                >
                  {quality}
                </button>
              ))}
            </div>
          )}
        </div>
        
        {isLoading && (
          <div className={styles.loadingOverlay}>
            <div className={styles.spinner}></div>
            <p>Loading video...</p>
          </div>
        )}
        
        {error && (
          <div className={styles.errorOverlay}>
            <p>{error}</p>
            <button onClick={handleClose}>Close</button>
          </div>
        )}
        
        <video
          ref={videoRef}
          className={styles.videoElement}
          controls
          playsInline
          autoPlay
          onError={() => setError('Video playback failed')}
        />
        
        <div className={styles.videoInfo}>
          <h3>{video.title}</h3>
          <p>Quality: {currentResolution}</p>
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;
