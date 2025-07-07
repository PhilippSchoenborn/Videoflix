import React from 'react';
import { Play, Star } from 'lucide-react';
import type { Video, WatchProgress } from '../types';
import styles from './VideoGrid.module.css';

interface VideoCardProps {
  video: Video;
  watchProgress?: WatchProgress;
  showProgress?: boolean;
  onVideoClick: (video: Video) => void;
  onResumeClick?: (video: Video, progress: WatchProgress) => void;
}

interface VideoGridProps {
  title: string;
  videos: Video[];
  watchProgress?: WatchProgress[];
  showProgress?: boolean;
  maxItems?: number;
  icon?: React.ComponentType<any>;
  onVideoClick: (video: Video) => void;
  onResumeClick?: (video: Video, progress: WatchProgress) => void;
  emptyMessage?: string;
}

const VideoCard: React.FC<VideoCardProps> = ({
  video,
  watchProgress,
  showProgress = false,
  onVideoClick,
  onResumeClick
}) => {
  // Convert duration string to seconds for progress calculation
  const getDurationInSeconds = (duration: string): number => {
    if (!duration) return 0;
    // Parse duration string (e.g., "01:30:00" -> 5400 seconds)
    const parts = duration.split(':');
    if (parts.length === 3) {
      const hours = parseInt(parts[0]) || 0;
      const minutes = parseInt(parts[1]) || 0;
      const seconds = parseInt(parts[2]) || 0;
      return hours * 3600 + minutes * 60 + seconds;
    }
    return 0;
  };

  const durationInSeconds = getDurationInSeconds(video.duration);
  const progressPercentage = watchProgress && durationInSeconds > 0
    ? Math.min((watchProgress.progress_seconds / durationInSeconds) * 100, 100)
    : 0;

  return (
    <div className={styles.videoCard}>
      <div className={styles.videoThumbnail}>
        {video.thumbnail ? (
          <img 
            src={video.thumbnail} 
            alt={video.title}
            className={styles.thumbnailImage}
          />
        ) : (
          <div className={styles.placeholderThumbnail}>
            <Play className="w-12 h-12" />
          </div>
        )}
        
        {/* Play Button Overlay */}
        <div className={styles.playOverlay}>
          <div className={styles.playButton}>
            <Play className="w-8 h-8 text-white ml-1" />
          </div>
        </div>

        {/* Progress Bar */}
        {showProgress && watchProgress && progressPercentage > 0 && (
          <div className={styles.progressBar}>
            <div 
              className={styles.progressFill}
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
        )}

        {/* Resume Button */}
        {showProgress && watchProgress && progressPercentage > 0 && onResumeClick && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onResumeClick(video, watchProgress);
            }}
            className={styles.resumeButton}
          >
            Resume
          </button>
        )}
      </div>
      
      <div 
        className={styles.videoInfo} 
        onClick={() => onVideoClick(video)}
      >
        <h3 className={styles.videoTitle}>
          {video.title}
        </h3>
        <p className={styles.videoDescription}>
          {video.description}
        </p>
        
        <div className={styles.videoMeta}>
          <div className={styles.genreInfo}>
            <span className={styles.starIcon}>★</span>
            <span className={styles.genreText}>
              {video.genre?.name || 'New'}
            </span>
          </div>
          
          {showProgress && watchProgress && (
            <div className={styles.progressText}>
              {Math.round(progressPercentage)}% watched
            </div>
          )}
        </div>

        <div className={styles.videoTags}>
          <span className={styles.ageRating}>
            {video.age_rating}
          </span>
          
          {video.is_featured && (
            <div className={styles.featuredTag}>
              <Star className="w-3 h-3 mr-1" />
              Featured
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const VideoGrid: React.FC<VideoGridProps> = ({
  title,
  videos,
  watchProgress = [],
  showProgress = false,
  maxItems,
  icon: Icon,
  onVideoClick,
  onResumeClick,
  emptyMessage = "No videos available"
}) => {
  const displayVideos = maxItems ? videos.slice(0, maxItems) : videos;
  const progressMap = new Map(
    watchProgress.map(wp => [wp.video.id, wp])
  );

  if (videos.length === 0) {
    return (
      <section className={styles.videoSection}>
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>
            {Icon && <Icon className="w-6 h-6 mr-2 text-purple-400" />}
            {title}
          </h2>
        </div>
        <div className={styles.emptyState}>
          <div className={styles.emptyMessage}>{emptyMessage}</div>
        </div>
      </section>
    );
  }

  return (
    <section className={styles.videoSection}>
      <div className={styles.sectionHeader}>
        <h2 className={styles.sectionTitle}>
          {Icon && <Icon className="w-6 h-6 mr-2 text-purple-400" />}
          {title}
          <span className={styles.videoCount}>
            ({videos.length} {videos.length === 1 ? 'video' : 'videos'})
          </span>
        </h2>
        
        {maxItems && videos.length > maxItems && (
          <button className={styles.viewAllButton}>
            View All →
          </button>
        )}
      </div>
      
      <div className={styles.videoGrid}>
        {displayVideos.map((video) => (
          <VideoCard
            key={video.id}
            video={video}
            watchProgress={progressMap.get(video.id)}
            showProgress={showProgress}
            onVideoClick={onVideoClick}
            onResumeClick={onResumeClick}
          />
        ))}
      </div>
    </section>
  );
};

export default VideoGrid;
export { VideoCard };
