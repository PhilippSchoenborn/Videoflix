import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../hooks/useToast';
import type { Video, Genre, WatchProgress, GenreWithVideos, SearchFilters } from '../types';
import apiService from '../services/api';
import { Play, Plus, Clock, Star, Upload, TrendingUp, Video as VideoIcon } from 'lucide-react';
import VideoGrid from '../components/VideoGrid';
import SearchBar from '../components/SearchBar';
import VideoDetailModal from '../components/VideoDetailModal';

const DashboardPage: React.FC = () => {
  const { user, logout } = useAuth();
  const { showToast } = useToast();
  
  // State
  const [allVideos, setAllVideos] = useState<Video[]>([]);
  const [filteredVideos, setFilteredVideos] = useState<Video[]>([]);
  const [featuredVideos, setFeaturedVideos] = useState<Video[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [genreVideos, setGenreVideos] = useState<GenreWithVideos[]>([]);
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
        const [videos, featured, genreList, watchProgress, genreWithVideos] = await Promise.all([
          apiService.getVideos().catch(() => []),
          apiService.getFeaturedVideos().catch(() => []),
          apiService.getGenres().catch(() => []),
          apiService.getContinueWatching().catch(() => []),
          apiService.getVideosByGenre().catch(() => []),
        ]);
        
        setAllVideos(videos);
        setFilteredVideos(videos);
        setFeaturedVideos(featured);
        setGenres(genreList);
        setContinueWatching(watchProgress);
        setGenreVideos(genreWithVideos);
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
        showToast('Failed to load dashboard data', 'error');
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, [showToast]);

  // Handle search and filtering
  const handleFiltersChange = useCallback((filters: SearchFilters) => {
    let filtered = [...allVideos];

    if (filters.search) {
      const searchTerm = filters.search.toLowerCase();
      filtered = filtered.filter(video => 
        video.title.toLowerCase().includes(searchTerm) ||
        video.description.toLowerCase().includes(searchTerm) ||
        video.genre?.name.toLowerCase().includes(searchTerm)
      );
    }

    if (filters.genre) {
      filtered = filtered.filter(video => video.genre?.id === filters.genre);
    }

    if (filters.age_rating) {
      filtered = filtered.filter(video => video.age_rating === filters.age_rating);
    }

    if (filters.featured) {
      filtered = filtered.filter(video => video.is_featured);
    }

    setFilteredVideos(filtered);
  }, [allVideos]);

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

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
      showToast('Logout failed', 'error');
    }
  };

  const currentHeroVideo = featuredVideos[currentHeroIndex];

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <header className="bg-gray-900 shadow-lg border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-purple-500">Videoflix</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-300">
                Welcome, {user?.first_name || user?.username}!
              </span>
              <button
                onClick={handleLogout}
                className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        {currentHeroVideo && (
          <section className="mb-12">
            <div className="relative bg-gradient-to-r from-purple-900 to-black rounded-xl overflow-hidden">
              <div className="absolute inset-0">
                {currentHeroVideo.thumbnail && (
                  <img 
                    src={currentHeroVideo.thumbnail} 
                    alt={currentHeroVideo.title}
                    className="w-full h-full object-cover opacity-50"
                  />
                )}
                <div className="absolute inset-0 bg-gradient-to-r from-black/80 to-transparent" />
              </div>
              
              <div className="relative z-10 p-8 md:p-12">
                <h2 className="text-4xl md:text-6xl font-bold text-white mb-4">
                  {currentHeroVideo.title}
                </h2>
                <p className="text-lg md:text-xl text-gray-200 mb-6 max-w-2xl">
                  {currentHeroVideo.description}
                </p>
                <div className="flex items-center gap-4 mb-8">
                  <span className="bg-purple-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                    {currentHeroVideo.genre?.name}
                  </span>
                  <span className="bg-gray-700 text-white px-3 py-1 rounded-full text-sm">
                    {currentHeroVideo.age_rating}
                  </span>
                </div>
                <button 
                  onClick={() => handleVideoClick(currentHeroVideo)}
                  className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-colors flex items-center"
                >
                  <Play className="w-6 h-6 mr-2" />
                  Watch Now
                </button>
              </div>

              {/* Hero Indicators */}
              {featuredVideos.length > 1 && (
                <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2 flex space-x-2">
                  {featuredVideos.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentHeroIndex(index)}
                      className={`w-3 h-3 rounded-full transition-colors ${
                        index === currentHeroIndex ? 'bg-purple-500' : 'bg-gray-400'
                      }`}
                    />
                  ))}
                </div>
              )}
            </div>
          </section>
        )}

        {/* Search and Filters */}
        <SearchBar
          genres={genres}
          onFiltersChange={handleFiltersChange}
        />

        {/* Continue Watching */}
        {continueWatching.length > 0 && (
          <VideoGrid
            title="Continue Watching"
            videos={continueWatching.map(wp => wp.video)}
            watchProgress={continueWatching}
            showProgress={true}
            icon={Clock}
            onVideoClick={handleVideoClick}
            onResumeClick={handleResumeClick}
            maxItems={8}
          />
        )}

        {/* Featured Videos */}
        <VideoGrid
          title="Featured Content"
          videos={featuredVideos}
          icon={Star}
          onVideoClick={handleVideoClick}
          maxItems={10}
        />

        {/* All Videos / Search Results */}
        <VideoGrid
          title={filteredVideos.length === allVideos.length ? "All Movies & Shows" : "Search Results"}
          videos={filteredVideos}
          icon={VideoIcon}
          onVideoClick={handleVideoClick}
          emptyMessage="No videos found matching your criteria"
        />

        {/* Videos by Genre */}
        {genreVideos.map((genreGroup) => (
          <VideoGrid
            key={genreGroup.id}
            title={genreGroup.name}
            videos={genreGroup.videos}
            onVideoClick={handleVideoClick}
            maxItems={8}
          />
        ))}

        {/* Quick Actions */}
        <section className="mb-12">
          <div className="bg-gray-900 rounded-xl p-8">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <Plus className="w-6 h-6 mr-2 text-purple-400" />
              Quick Actions
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <button className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-lg hover:from-blue-700 hover:to-blue-800 transition-colors">
                <Upload className="w-8 h-8 mb-3" />
                <h3 className="text-lg font-semibold mb-2">Upload Video</h3>
                <p className="text-sm opacity-90">Share your content with the community</p>
              </button>
              
              <button className="bg-gradient-to-r from-green-600 to-green-700 text-white p-6 rounded-lg hover:from-green-700 hover:to-green-800 transition-colors">
                <Star className="w-8 h-8 mb-3" />
                <h3 className="text-lg font-semibold mb-2">Browse Favorites</h3>
                <p className="text-sm opacity-90">Explore your saved videos</p>
              </button>
              
              <button className="bg-gradient-to-r from-purple-600 to-purple-700 text-white p-6 rounded-lg hover:from-purple-700 hover:to-purple-800 transition-colors">
                <Clock className="w-8 h-8 mb-3" />
                <h3 className="text-lg font-semibold mb-2">Watch History</h3>
                <p className="text-sm opacity-90">Review your viewing history</p>
              </button>
            </div>
          </div>
        </section>

        {/* Quick Stats */}
        <section className="mt-16 mb-8">
          <div className="bg-gray-900 rounded-xl p-8">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <TrendingUp className="w-6 h-6 mr-2 text-purple-400" />
              Your Stats
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-400 mb-2">
                  {allVideos.length}
                </div>
                <div className="text-gray-400">Total Videos</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-400 mb-2">
                  {continueWatching.length}
                </div>
                <div className="text-gray-400">In Progress</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-400 mb-2">
                  {continueWatching.filter(wp => wp.completed).length}
                </div>
                <div className="text-gray-400">Completed</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-yellow-400 mb-2">
                  {genres.length}
                </div>
                <div className="text-gray-400">Genres</div>
              </div>
            </div>
          </div>
        </section>
      </main>

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
              
              // Here you would integrate with the actual video player
              // and update progress as the user watches
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
