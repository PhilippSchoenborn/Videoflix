import React, { useRef } from 'react';
import type { Video, WatchProgress } from '../types';
import styles from './ScrollableVideoList.module.css';

interface ScrollableVideoListProps {
  title: string;
  description?: string;
  videos: Video[];
  onVideoClick: (video: Video) => void;
  onVideoHover?: (video: Video) => void;
  watchProgress?: WatchProgress[];
  showProgress?: boolean;
  onResumeClick?: (video: Video, progress: WatchProgress) => Promise<void>;
}

const ScrollableVideoList: React.FC<ScrollableVideoListProps> = ({ 
  title, 
  description,
  videos, 
  onVideoClick, 
  onVideoHover,
  watchProgress = [],
  showProgress = false,
  onResumeClick
}) => {
  const scrollContainerRef = useRef<HTMLUListElement>(null);

  const scrollHorizontally = (amount: number) => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollBy({
        left: amount,
        behavior: 'smooth'
      });
    }
  };

  const getVideoProgress = (videoId: number): WatchProgress | undefined => {
    return watchProgress.find(progress => progress.video.id === videoId);
  };

  return (
    <section className={styles.videoList}>
      <div className={styles.titleSection}>
        <h2 className={styles.title}>{title}</h2>
        {description && (
          <p className={styles.description}>{description}</p>
        )}
      </div>
      <div className={styles.scrollWrapper}>
        <button 
          className={`${styles.scrollButton} ${styles.scrollLeft}`}
          onClick={() => scrollHorizontally(-300)}
          aria-label="Scroll left"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M15 18l-6-6 6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
        
        <ul ref={scrollContainerRef} className={styles.videoContainer}>
          {videos.map((video) => {
            const progress = getVideoProgress(video.id);
            const progressPercentage = progress?.progress_percentage || 0;
            
            return (
              <li 
                key={video.id} 
                className={styles.videoItem}
                onClick={() => onVideoClick(video)}
                onMouseEnter={() => onVideoHover?.(video)}
              >
                <div className={styles.videoThumbnail}>
                  {video.thumbnail ? (
                    <img 
                      src={video.thumbnail} 
                      alt={video.title}
                      className={styles.thumbnailImage}
                    />
                  ) : (
                    <div className={styles.placeholderThumbnail}>
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                        <path d="M8 5v14l11-7z" fill="currentColor"/>
                      </svg>
                    </div>
                  )}
                  
                  {/* Progress Bar */}
                  {showProgress && progress && progressPercentage > 0 && (
                    <div className={styles.progressBar}>
                      <div 
                        className={styles.progressFill}
                        style={{ width: `${progressPercentage}%` }}
                      />
                    </div>
                  )}
                  
                  <div className={styles.videoOverlay}>
                    {showProgress && progress && onResumeClick ? (
                      <button
                        className={styles.resumeButton}
                        onClick={(e) => {
                          e.stopPropagation();
                          onResumeClick(video, progress);
                        }}
                      >
                        Resume
                      </button>
                    ) : (
                      <div className={styles.playIcon}>
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                          <path d="M8 5v14l11-7z" fill="currentColor"/>
                        </svg>
                      </div>
                    )}
                  </div>
                </div>
                <div className={styles.videoInfo}>
                  <h3 className={styles.videoTitle}>{video.title}</h3>
                  <p className={styles.videoDescription}>{video.description}</p>
                  {showProgress && progress && (
                    <p className={styles.progressText}>
                      {Math.round(progressPercentage)}% watched
                    </p>
                  )}
                </div>
              </li>
            );
          })}
        </ul>
        
        <button 
          className={`${styles.scrollButton} ${styles.scrollRight}`}
          onClick={() => scrollHorizontally(300)}
          aria-label="Scroll right"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M9 18l6-6-6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </section>
  );
};

export default ScrollableVideoList;
