import React, { useEffect, useState } from 'react';
import { useToast } from '../hooks/useToast';
import type { Video, WatchProgress, GenreWithVideos } from '../types';
import apiService from '../services/api';
import { Clock } from 'lucide-react';
import VideoDetailModal from '../components/VideoDetailModal';
import VideoPlayer from '../components/VideoPlayer';
import Header from '../components/Header';
import DashboardFooter from '../components/DashboardFooter';
import ScrollableVideoList from '../components/ScrollableVideoList';
import styles from './Dashboard.module.css';

const DashboardPage: React.FC = () => {
  const { showToast } = useToast();
  
  // State
  const [allVideos, setAllVideos] = useState<Video[]>([]);
  const [featuredVideos, setFeaturedVideos] = useState<Video[]>([]);
  const [genreVideos, setGenreVideos] = useState<GenreWithVideos[]>([]);
  const [continueWatching, setContinueWatching] = useState<WatchProgress[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);
  const [currentHeroIndex, setCurrentHeroIndex] = useState(0);
  
  // Video player state
  const [isPlayerOpen, setIsPlayerOpen] = useState(false);
  const [playerVideo, setPlayerVideo] = useState<Video | null>(null);
  const [playerResolution, setPlayerResolution] = useState<'120p' | '360p' | '480p' | '720p' | '1080p'>('720p');
  const [playerResumeTime, setPlayerResumeTime] = useState(0);

  // Hero video auto-play state
  const [isHeroPlaying, setIsHeroPlaying] = useState(false);
  const [heroVideoRef, setHeroVideoRef] = useState<HTMLVideoElement | null>(null);

  // Hero video rotation with auto-play
  useEffect(() => {
    if (featuredVideos.length > 1) {
      const interval = setInterval(() => {
        setCurrentHeroIndex((prev) => {
          const nextIndex = (prev + 1) % featuredVideos.length;
          return nextIndex;
        });
      }, 8000); // Change every 8 seconds (longer for video preview)

      return () => clearInterval(interval);
    }
  }, [featuredVideos.length]);

  // Get current hero video
  const currentHeroVideo = featuredVideos[currentHeroIndex];

  // Auto-play hero video preview
  useEffect(() => {
    if (currentHeroVideo && heroVideoRef) {
      const playHeroVideo = async () => {
        try {
          setIsHeroPlaying(true);
          // Start video from beginning with low volume
          heroVideoRef.currentTime = 0;
          heroVideoRef.volume = 0.3;
          heroVideoRef.muted = false;
          await heroVideoRef.play();
          
          // Stop video after 6 seconds
          setTimeout(() => {
            if (heroVideoRef) {
              heroVideoRef.pause();
              setIsHeroPlaying(false);
            }
          }, 6000);
        } catch (error) {
          setIsHeroPlaying(false);
        }
      };

      // Start autoplay after 1 second delay
      const timeout = setTimeout(playHeroVideo, 1000);
      return () => clearTimeout(timeout);
    }
  }, [currentHeroVideo, heroVideoRef]);

  // Load dashboard data function
  const loadDashboardData = async (showLoadingState = true) => {
    try {
      if (showLoadingState) {
        setIsLoading(true);
      }
      const [videos, featured, watchProgress, genreWithVideos] = await Promise.all([
        apiService.getVideos().catch(() => []),
        apiService.getFeaturedVideos().catch(() => []),
        apiService.getContinueWatching().catch(() => []),
        apiService.getVideosByGenre().catch(() => []),
      ]);
      
      setAllVideos(videos);
      setFeaturedVideos(featured);
      setContinueWatching(watchProgress);
      setGenreVideos(genreWithVideos);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      showToast('Failed to load dashboard data', 'error');
    } finally {
      if (showLoadingState) {
        setIsLoading(false);
      }
    }
  };

  // Load dashboard data on mount
  useEffect(() => {
    loadDashboardData();
  }, [showToast]);

  // Debug effect for selectedVideo
  useEffect(() => {
    // Video selection tracking (silent)
  }, [selectedVideo]);

  // Handle video actions
  const handleVideoClick = (video: Video) => {
    setSelectedVideo(video);
  };

  const handleResumeClick = async (video: Video, progress: WatchProgress) => {
    try {
      // Calculate resume time in seconds from progress_seconds directly
      const resumeSeconds = progress.progress_seconds || 0;
      
      // Use saved resolution or default to 720p
      const savedResolution = progress.last_resolution || '720p';
      
      // Start the video player directly (skip modal)
      setPlayerVideo(video);
      setPlayerResolution(savedResolution as '120p' | '360p' | '480p' | '720p' | '1080p');
      setPlayerResumeTime(resumeSeconds);
      setIsPlayerOpen(true);
      
      showToast(`Resuming "${video.title}" from ${Math.round(progress.progress_percentage || 0)}% in ${savedResolution}`, 'success');
    } catch (error) {
      console.error('Failed to resume video:', error);
      showToast('Failed to resume video', 'error');
    }
  };

  // Handle video player close with data refresh
  const handlePlayerClose = async () => {
    setIsPlayerOpen(false);
    setPlayerVideo(null);
    setPlayerResumeTime(0);
    
    // Refresh dashboard data silently (without loading state)
    await loadDashboardData(false);
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <Header />
        <div className={styles.loading}>Loading videos...</div>
        <DashboardFooter />
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <Header />
      
      <main className={styles.main}>
        {/* Hero Section */}
        {currentHeroVideo && (
          <section className={styles.previewSection}>
            <div className={styles.previewVideo}>
              {/* Background image */}
              {currentHeroVideo.thumbnail && (
                <img 
                  src={currentHeroVideo.thumbnail} 
                  alt={currentHeroVideo.title}
                  className={styles.heroVideo}
                />
              )}
              
              {/* Auto-playing video preview */}
              <video
                ref={setHeroVideoRef}
                className={styles.heroVideo}
                src={`http://localhost:8000/api/videos/${currentHeroVideo.id}/stream/480p/`}
                muted
                playsInline
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                  opacity: isHeroPlaying ? 1 : 0,
                  transition: 'opacity 0.3s ease',
                  zIndex: 1
                }}
              />
              
              {/* Gradient overlay - always present */}
              <div className={styles.videoOverlay}></div>
              
              {/* Hero Indicators */}
              {featuredVideos.length > 1 && (
                <div className={styles.heroIndicators}>
                  {featuredVideos.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentHeroIndex(index)}
                      className={`${styles.indicator} ${index === currentHeroIndex ? styles.active : ''}`}
                      aria-label={`Go to video ${index + 1}`}
                    />
                  ))}
                </div>
              )}
            </div>
            
            <article className={styles.heroContent}>
              <h1 className={styles.videoTitle}>
                {currentHeroVideo.title}
              </h1>
              <p className={styles.videoDescription}>
                {currentHeroVideo.description}
              </p>
              <div className={styles.videoMeta}>
                <span className={styles.genreTag}>
                  {currentHeroVideo.genre?.name}
                </span>
                <span className={styles.ageRating}>
                  {currentHeroVideo.age_rating}
                </span>
              </div>
              <button 
                className={styles.playButton}
                onClick={() => handleVideoClick(currentHeroVideo)}
                aria-label="Play video"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" style={{ marginRight: '6px' }}>
                  <path d="M8 5v14l11-7z" fill="currentColor"/>
                </svg>
                Play
              </button>
            </article>
          </section>
        )}

        {/* Video Lists */}
        <section className={styles.listSection}>
          {/* Continue Watching Section */}
          {continueWatching.length > 0 && (
            <div className={styles.continueWatchingSection}>
              <h2 className={styles.sectionTitle}>
                <Clock className={styles.sectionIcon} />
                Continue Watching
              </h2>
              <ScrollableVideoList
                title=""
                videos={continueWatching.map(progress => progress.video)}
                watchProgress={continueWatching}
                showProgress={true}
                onVideoClick={handleVideoClick}
                onResumeClick={handleResumeClick}
              />
            </div>
          )}

          {/* All Videos */}
          <ScrollableVideoList
            title="All Videos"
            videos={allVideos}
            onVideoClick={handleVideoClick}
          />

          {/* Videos by Genre */}
          {genreVideos.map((genreGroup) => (
            <ScrollableVideoList
              key={genreGroup.id}
              title={genreGroup.name}
              description={genreGroup.description}
              videos={genreGroup.videos}
              onVideoClick={handleVideoClick}
            />
          ))}
        </section>
      </main>

      <DashboardFooter />

      {/* Video Detail Modal */}
      {selectedVideo && (
        <VideoDetailModal
          video={selectedVideo}
          isOpen={!!selectedVideo}
          onClose={() => {
            setSelectedVideo(null);
          }}
          onPlayVideo={async (video, resolution) => {
            try {
              // Start tracking watch progress with initial resolution
              await apiService.updateWatchProgress(video.id, 0, false, resolution);
              
              // Close modal and open video player
              setSelectedVideo(null);
              setPlayerVideo(video);
              setPlayerResolution(resolution);
              setPlayerResumeTime(0); // New video, no resume time
              setIsPlayerOpen(true);
              
              showToast(`Starting "${video.title}" in ${resolution}`, 'success');
            } catch (error) {
              console.error('Failed to start video:', error);
              showToast('Failed to start video', 'error');
            }
          }}
        />
      )}

      {/* Video Player */}
      {isPlayerOpen && playerVideo && (
        <VideoPlayer
          video={playerVideo}
          resolution={playerResolution}
          isOpen={isPlayerOpen}
          onClose={handlePlayerClose}
          resumeTime={playerResumeTime}
        />
      )}
    </div>
  );
};

export default DashboardPage;
