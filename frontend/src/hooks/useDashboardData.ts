import { useEffect, useState } from 'react';
import apiService from '../services/api';
import type { Video, WatchProgress, GenreWithVideos } from '../types';

export function useDashboardData(
  showToast: (msg: string, type?: 'success' | 'error' | 'info' | 'warning', duration?: number) => void
) {
  const [allVideos, setAllVideos] = useState<Video[]>([]);
  const [featuredVideos, setFeaturedVideos] = useState<Video[]>([]);
  const [genreVideos, setGenreVideos] = useState<GenreWithVideos[]>([]);
  const [continueWatching, setContinueWatching] = useState<WatchProgress[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  async function loadDashboardData(showLoadingState = true) {
    try {
      if (showLoadingState) setIsLoading(true);
      const [videos, featured, watch, genreWithVideos] = await Promise.all([
        apiService.getVideos().catch(() => []),
        apiService.getFeaturedVideos().catch(() => []),
        apiService.getContinueWatching().catch(() => []),
        apiService.getVideosByGenre().catch(() => []),
      ]);
      setAllVideos(videos);
      setFeaturedVideos(featured);
      setContinueWatching(watch);
      setGenreVideos(genreWithVideos);
    } catch {
      showToast('Failed to load dashboard data', 'error');
    } finally {
      if (showLoadingState) setIsLoading(false);
    }
  }

  useEffect(() => {
    loadDashboardData();
  }, [showToast]);

  return { allVideos, featuredVideos, genreVideos, continueWatching, isLoading, loadDashboardData };
}
