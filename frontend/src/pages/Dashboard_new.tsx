import React, { useEffect, useState } from 'react';
import { useToast } from '../hooks/useToast';
import type { Video, WatchProgress } from '../types';
import apiService from '../services/api';
import { Clock } from 'lucide-react';
import VideoDetailModal from '../components/VideoDetailModal';
import Header from '../components/Header';
import Footer from '../components/Footer';
import ScrollableVideoList from '../components/ScrollableVideoList';
import styles from './Dashboard.module.css';

const DashboardPage: React.FC = () => {
  const { showToast } = useToast();
  
  // State
  const [allVideos, setAllVideos] = useState<Video[]>([]);
  const [featuredVideos, setFeaturedVideos] = useState<Video[]>([]);
  const [continueWatching, setContinueWatching] = useState<WatchProgress[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);
  const [currentHeroIndex, setCurrentHeroIndex] = useState(0);

  // Hero video rotation
  useEffect(() => {
    if (featuredVideos.length > 1) {
      const interval = setInterval(() => {
        setCurrentHeroIndex((prev) => (prev + 1) % featuredVideos.length);
      }, 5000); // Change every 5 seconds

      return () => clearInterval(interval);
    }
  }, [featuredVideos.length]);

  // Load dashboard data
  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setIsLoading(true);
        const [videos, featured, watchProgress] = await Promise.all([
          apiService.getVideos().catch(() => []),
          apiService.getFeaturedVideos().catch(() => []),
          apiService.getContinueWatching().catch(() => []),
        ]);
        
        setAllVideos(videos);
        setFeaturedVideos(featured);
        setContinueWatching(watchProgress);
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
        showToast('Failed to load dashboard data', 'error');
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, [showToast]);

  // Handle video actions
  const handleVideoClick = (video: Video) => {
    setSelectedVideo(video);
  };

  const handleResumeClick = async (video: Video, progress: WatchProgress) => {
    try {
      // Update watch progress to current position
      await apiService.updateWatchProgress(video.id, progress.progress_seconds);
      setSelectedVideo(video);
      showToast(`Resuming "${video.title}" from ${Math.round(progress.progress_percentage || 0)}%`, 'success');
    } catch (error) {
      console.error('Failed to resume video:', error);
      showToast('Failed to resume video', 'error');
    }
  };

  const currentHeroVideo = featuredVideos[currentHeroIndex];

  if (isLoading) {
    return (
      <div className={styles.container}>
        <Header />
        <div className={styles.loading}>Loading videos...</div>
        <Footer />
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
              {currentHeroVideo.thumbnail && (
                <>
                  <img 
                    src={currentHeroVideo.thumbnail} 
                    alt={currentHeroVideo.title}
                    className={styles.heroVideo}
                  />
                  <div className={styles.videoOverlay}></div>
                </>
              )}
              
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
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M8 5v14l11-7z" fill="currentColor"/>
                </svg>
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

          {/* Featured Videos */}
          {featuredVideos.length > 0 && (
            <ScrollableVideoList
              title="Featured Content"
              videos={featuredVideos}
              onVideoClick={handleVideoClick}
            />
          )}
          
          {/* All Videos */}
          <ScrollableVideoList
            title="All Videos"
            videos={allVideos}
            onVideoClick={handleVideoClick}
          />
        </section>
      </main>

      <Footer />

      {/* Video Detail Modal */}
      {selectedVideo && (
        <VideoDetailModal
          video={selectedVideo}
          isOpen={!!selectedVideo}
          onClose={() => setSelectedVideo(null)}
          onPlayVideo={async (video, resolution) => {
            try {
              // Start tracking watch progress
              await apiService.updateWatchProgress(video.id, 0);
              
              setSelectedVideo(null);
              showToast(`Starting "${video.title}" in ${resolution}`, 'success');
            } catch (error) {
              console.error('Failed to start video:', error);
              showToast('Failed to start video', 'error');
            }
          }}
        />
      )}
    </div>
  );
};

export default DashboardPage;
