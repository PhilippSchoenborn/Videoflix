import { useEffect, useState } from 'react';
import apiService from '../services/api';
import type { Video, Genre } from '../types';

export function useDashboardPageData() {
  const [featuredVideos, setFeaturedVideos] = useState<Video[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [continueWatching, setContinueWatching] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [featured, genreList, watchProgress] = await Promise.all([
          apiService.getFeaturedVideos().catch(() => []),
          apiService.getGenres().catch(() => []),
          apiService.getContinueWatching().catch(() => []),
        ]);
        setFeaturedVideos(featured);
        setGenres(genreList);
        setContinueWatching(watchProgress);
      } finally {
        setIsLoading(false);
      }
    }
    load();
  }, []);

  return { featuredVideos, genres, continueWatching, isLoading };
}
