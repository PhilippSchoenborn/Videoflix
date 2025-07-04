import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import type { Video, Genre } from '../types';
import apiService from '../services/api';
import { Play, Plus, Clock, Star } from 'lucide-react';

const DashboardPage: React.FC = () => {
  const { user, logout } = useAuth();
  const [featuredVideos, setFeaturedVideos] = useState<Video[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [continueWatching, setContinueWatching] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const [featured, genreList, watchProgress] = await Promise.all([
          apiService.getFeaturedVideos().catch(() => []),
          apiService.getGenres().catch(() => []),
          apiService.getContinueWatching().catch(() => []),
        ]);
        
        setFeaturedVideos(featured);
        setGenres(genreList);
        setContinueWatching(watchProgress);
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-videoflix-black">
      {/* Header */}
      <header className="bg-videoflix-dark shadow-lg border-b border-videoflix-gray">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-videoflix-red">Videoflix</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-300">
                Welcome, {user?.first_name || user?.username}!
              </span>
              <button
                onClick={handleLogout}
                className="bg-videoflix-red hover:bg-videoflix-red-hover text-white px-4 py-2 rounded-lg transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <section className="mb-12">
          <div className="bg-gradient-to-r from-videoflix-red to-videoflix-red-hover rounded-xl p-8 text-white">
            <h2 className="text-3xl font-bold mb-4">
              Welcome to Your Entertainment Hub
            </h2>
            <p className="text-xl mb-6 opacity-90">
              Discover amazing movies and shows. Start watching now!
            </p>
            <button className="bg-white text-videoflix-red px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors flex items-center">
              <Play className="w-5 h-5 mr-2" />
              Start Watching
            </button>
          </div>
        </section>

        {/* Continue Watching */}
        {continueWatching.length > 0 && (
          <section className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white flex items-center">
                <Clock className="w-6 h-6 mr-2 text-videoflix-red" />
                Continue Watching
              </h2>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {continueWatching.slice(0, 4).map((item) => (
                <div key={item.id} className="bg-videoflix-dark rounded-lg overflow-hidden hover:bg-videoflix-gray transition-colors cursor-pointer">
                  <div className="aspect-video bg-videoflix-gray flex items-center justify-center">
                    <Play className="w-12 h-12 text-white opacity-60" />
                  </div>
                  <div className="p-4">
                    <h3 className="text-white font-semibold truncate">
                      {item.video?.title || 'Video Title'}
                    </h3>
                    <div className="w-full bg-videoflix-gray rounded-full h-2 mt-2">
                      <div 
                        className="bg-videoflix-red h-2 rounded-full" 
                        style={{ width: `${(item.progress_seconds / (item.video?.duration || 100)) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Featured Videos */}
        <section className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-white flex items-center">
              <Star className="w-6 h-6 mr-2 text-yellow-400" />
              Featured Content
            </h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {featuredVideos.length > 0 ? (
              featuredVideos.slice(0, 8).map((video) => (
                <div key={video.id} className="bg-gray-800 rounded-lg overflow-hidden hover:bg-gray-700 transition-colors cursor-pointer group">
                  <div className="aspect-video bg-gray-700 flex items-center justify-center relative overflow-hidden">
                    {video.thumbnail ? (
                      <img 
                        src={video.thumbnail} 
                        alt={video.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    ) : (
                      <Play className="w-12 h-12 text-white opacity-60" />
                    )}
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center">
                      <Play className="w-12 h-12 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    </div>
                  </div>
                  <div className="p-4">
                    <h3 className="text-white font-semibold truncate">
                      {video.title}
                    </h3>
                    <p className="text-gray-400 text-sm mt-1 truncate">
                      {video.description}
                    </p>
                    <div className="flex items-center mt-2">
                      <span className="text-yellow-400 text-sm">★</span>
                      <span className="text-gray-400 text-sm ml-1">
                        {video.genre?.name || 'New'}
                      </span>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              // Placeholder cards when no featured videos
              Array.from({ length: 8 }).map((_, index) => (
                <div key={index} className="bg-gray-800 rounded-lg overflow-hidden">
                  <div className="aspect-video bg-gray-700 flex items-center justify-center">
                    <Plus className="w-12 h-12 text-gray-500" />
                  </div>
                  <div className="p-4">
                    <h3 className="text-gray-500 font-semibold">
                      Coming Soon
                    </h3>
                    <p className="text-gray-600 text-sm mt-1">
                      New content will be available here
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        </section>

        {/* Genres */}
        <section className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-white">Browse by Genre</h2>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {genres.length > 0 ? (
              genres.map((genre) => (
                <button
                  key={genre.id}
                  className="bg-gray-800 hover:bg-gray-700 text-white py-3 px-4 rounded-lg transition-colors text-center"
                >
                  {genre.name}
                </button>
              ))
            ) : (
              // Placeholder genre buttons
              ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Romance'].map((genre) => (
                <button
                  key={genre}
                  className="bg-gray-800 hover:bg-gray-700 text-white py-3 px-4 rounded-lg transition-colors text-center"
                >
                  {genre}
                </button>
              ))
            )}
          </div>
        </section>

        {/* Quick Stats */}
        <section>
          <div className="bg-gray-800 rounded-xl p-6">
            <h2 className="text-xl font-bold text-white mb-4">Your Activity</h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-400 mb-2">
                  {continueWatching.length}
                </div>
                <div className="text-gray-400">In Progress</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-400 mb-2">
                  {featuredVideos.length}
                </div>
                <div className="text-gray-400">Available</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-400 mb-2">
                  {genres.length}
                </div>
                <div className="text-gray-400">Genres</div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default DashboardPage;
