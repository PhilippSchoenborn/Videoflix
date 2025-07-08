import React from 'react';
import type { Video, WatchProgress } from '../types';
import styles from './ScrollableVideoList.module.css';
import ProgressBar from './ProgressBar';

type VideoListItemProps = {
  video: Video;
  progress?: WatchProgress;
  showProgress: boolean;
  onClick: (video: Video) => void;
  onHover?: (video: Video) => void;
  onResumeClick?: (video: Video, progress: WatchProgress) => Promise<void>;
};

const VideoListItem: React.FC<VideoListItemProps> = ({
  video,
  progress,
  showProgress,
  onClick,
  onHover,
  onResumeClick
}) => {
  const progressPercentage = progress?.progress_percentage || 0;
  return (
    <li
      className={styles.videoItem}
      onClick={() => onClick(video)}
      onMouseEnter={() => onHover?.(video)}
    >
      <div className={styles.videoThumbnail}>
        {video.thumbnail ? (
          <img src={video.thumbnail} alt={video.title} className={styles.thumbnailImage} />
        ) : (
          <div className={styles.placeholderThumbnail}>
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
              <path d="M8 5v14l11-7z" fill="currentColor"/>
            </svg>
          </div>
        )}
        {showProgress && progress && progressPercentage > 0 && (
          <ProgressBar percentage={progressPercentage} />
        )}
        <div className={styles.videoOverlay}>
          {showProgress && progress && onResumeClick ? (
            <button
              className={styles.resumeButton}
              onClick={e => {
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
};

export default VideoListItem;
