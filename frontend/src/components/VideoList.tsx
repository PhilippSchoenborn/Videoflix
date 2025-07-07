import React, { useRef } from 'react';
import styles from './VideoList.module.css';

interface Video {
  id: number;
  title: string;
  description: string;
  video_file?: string;
  thumbnail: string;
  created_at: string;
}

interface VideoListProps {
  title: string;
  videos: Video[];
  onVideoClick: (video: Video) => void;
}

const VideoList: React.FC<VideoListProps> = ({ title, videos, onVideoClick }) => {
  const scrollContainerRef = useRef<HTMLUListElement>(null);

  const scrollHorizontally = (amount: number) => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollBy({
        left: amount,
        behavior: 'smooth'
      });
    }
  };

  return (
    <section className={styles.videoList}>
      <h2 className={styles.title}>{title}</h2>
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
          {videos.map((video) => (
            <li 
              key={video.id} 
              className={styles.videoItem}
              onClick={() => onVideoClick(video)}
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
                <div className={styles.videoOverlay}>
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                    <path d="M8 5v14l11-7z" fill="currentColor"/>
                  </svg>
                </div>
              </div>
              <div className={styles.videoInfo}>
                <h3 className={styles.videoTitle}>{video.title}</h3>
                <p className={styles.videoDescription}>{video.description}</p>
              </div>
            </li>
          ))}
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

export default VideoList;
