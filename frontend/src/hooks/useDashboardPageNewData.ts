import { useEffect, useState } from 'react';
import apiService from '../services/api';
import type { Video, Genre, WatchProgress, GenreWithVideos } from '../types';

export function useDashboardPageNewData(
  showToast: (msg: string, type?: 'success' | 'error' | 'info' | 'warning', duration?: number) => void
) {
  const [allVideos, setAllVideos] = useState<Video[]>([]);
  const [featuredVideos, setFeaturedVideos] = useState<Video[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [genreVideos, setGenreVideos] = useState<GenreWithVideos[]>([]);
  const [continueWatching, setContinueWatching] = useState<WatchProgress[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function load() {
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
        setFeaturedVideos(featured);
        setGenres(genreList);
        setContinueWatching(watchProgress);
        setGenreVideos(genreWithVideos);
      } catch (error) {
        showToast('Failed to load dashboard data', 'error');
      } finally {
        setIsLoading(false);
      }
    }
    load();
  }, [showToast]);

  return { allVideos, featuredVideos, genres, genreVideos, continueWatching, isLoading };
}
